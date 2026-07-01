# Execução autônoma MCORCH com ciclo fechado
**Date:** 2026-07-01 | **Session ID:** `7d38a77b-f7f1-4e92-b419-5efbc0e5566c`

---

## 👤 User *(00:04:30)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(00:04:30)*

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


## 🤖 Claude *(00:04:37)*


## 🤖 Claude *(00:04:38)*

I'll execute the ShakeHands /handson pick-up ritual. Starting with all pre-flight checks in parallel.

## 🤖 Claude *(00:04:38)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -7",
  "description": "Recent git history"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 36eb30b chore(handoff): proof-manifest → efb9d1c6 (Fatia 3b VLM-soft loop seal)
> a2c8527 docs(handoff): seal Gabriel AI Fatia 3b (avatarIdentity VLM-soft) via loop autônomo — mesh 8997
> d023af0 docs(readme): v6.62.0 — Gabriel AI Fatia 3b destravada (VLM-soft) + nó avatarIdentity live — mesh 8997
> 268a732 docs(loop): autonomous-loop charter (backlog + Fila Sovereign + relaunch prompt) + sovereign-queue runbook
> 12d06c0 feat(avatar-clone-ai): Fatia 3b — avatarIdentity Canvas node + inspector (FR-AC-012)
> 541f707 feat(avatar-clone-ai): Fatia 3b foundation — VLM-soft compare lib + gate_mode migration (FR-AC-013b)
> 7b81bfd docs(bok): avatar-clone-ai Amendment 3b — Identity Gate via rota VLM-soft (MVP)
> ```

## 🤖 Claude *(00:04:38)*


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

## 🤖 Claude *(00:04:39)*


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

## 🤖 Claude *(00:04:40)*


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

## 🤖 Claude *(00:04:41)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"",
  "description": "Docker Sovereign Mesh status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 30 hours (healthy)
> mcorch_claude_mem: Up 2 weeks (healthy)
> mcorch_chroma: Up 2 weeks (healthy)
> ---
> mega-brain-dashboard: Up 2 weeks
> mega-brain-webhook: Up 2 weeks (healthy)
> mega-brain-daemon: Up 2 weeks (healthy)
> ```

## 🤖 Claude *(00:04:42)*


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
> {"nanosecond heartbeat":1782864282211775633}
> ```

## 🤖 Claude *(00:04:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/ 2>/dev/null; echo \"---WC---\"; wc -l HANDOFF.md; echo \"---SCRATCH---\"; ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean\"",
  "description": "BoK suites, HANDOFF line count, scratch check"
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
> 8892 HANDOFF.md
> ---SCRATCH---
> scratch has files
> ```

## 🤖 Claude *(00:04:50)*


## 🤖 Claude *(00:04:50)*

TypeScript: zero errors (clean). Git tree clean. Now reading HANDOFF (read-from-end strategy) + sprint priorities + scratch contents.

## 🤖 Claude *(00:04:51)*


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
> 14	## Session Seal — Gabriel AI Fatia 3b (avatarIdentity VLM-soft) via Loop Autônomo de Malha Fechada (2026-06-30)
> 15	
> 16	Sessão iniciada por `/handson`, sob **ultracode**. A diretiva Sovereign foi **arquitetural-meta**: transformar o "ok continue" entre fases num **loop autônomo de malha fechada** via `/loop` auto-ritmado, governado por uma **charter** como fonte da verdade do estado. Montado o loop e executados **3 ciclos fechados completos** que destravaram a **Fatia 3b** do programa Gabriel AI (`avatar-clone-ai`) — antes marcada GATED — pela rota **VLM-soft MVP**, mais o **selo final** (esta seção).
> 17	
> 18	**Infra do loop (`.claude/context/autonomous-loop-charter.md`):** backlog priorizado por valor · Fila de Ação Sovereign com destravadores exatos · ritual por iteração (git fetch → item desbloqueado de maior valor → BoK Gate → SOP Lei 2 → código → prova material Lei 1 → /security-review se migration → commit) · prompt **stateless** de religar (o estado vive na charter, nunca apodrece). O Sovereign emendou a charter ao vivo (diretiva **open-source-first/custo-USD-0/equity**) — absorvida.
> 19	
> 20	**Achado material decisivo (Lei 1):** ArcFace/InsightFace **não existe** no código; o Vision MCP expõe só 2 tools de visão **descritivos** (`vision_describe_image`/`vision_analyze_video`, verificado `server.ts:340` = 7 tools). Logo o Identity Gate da 3b foi desenhado **dual-mode**: VLM-soft MVP (compare descritivo enum, **human-review-assist < ArcFace**, fail-and-regenerate) ATIVO; ArcFace-hard **deferido** → OTD-AC-015 (Sovereign). Nada fabricado.
> 21	
> 22	| Action | Result |
> 23	|--------|--------|
> 24	| `docs/bok/avatar-clone-ai/10-amendment-3b-identity-gate-vlm-soft.md` | ✅ Emenda BoK FRD/SDD — Identity Gate dual-mode; verificada por **Workflow adversarial** `wf_188ce24c-881` (understand×3 + design + critic → `APPROVE`, **6 issues dobradas**: FR-AC-013b compare enum + `gate_mode` discriminador + telemetry key-migration + user-JWT credential path + max_regen anti-oscilação + Pattern #19/#18 qualifiers) |
> 25	| `src/lib/avatar-identity.ts` (NET-NEW) | ✅ Compare VLM-soft FR-AC-013b: schema enum fixo + parse fail-soft (não-JSON → `{}` → todos mismatch, nunca pass silencioso) + bands pass/review/fail de 1 threshold + `reconcileSoftMatches` (maioria N≥2, anti-oscilação pass↔fail→review) |
> 26	| `src/test/avatar-identity.test.ts` (NET-NEW) | ✅ **15/15** testes (bands/parse/reconcile/clamp) |
> 27	| `supabase/migrations/20260630140000_avatar_identity_gate_mode.sql` | ✅ Discriminador `gate_mode` (dobra issue #2); aditivo, herda RLS; `/security-review` **NO FINDINGS**. Aplicação **deferida ao GO 3b** (não mutei prod por feature gated) |
> 28	| `src/components/canvas/nodes/AvatarIdentityNode.tsx` + `RightPanel/inspectors/AvatarIdentityInspector.tsx` (NET-NEW) | ✅ Nó "Identidade (avatar)" FR-AC-012: upload multi-retrato (canvas-assets `user_id/`) + ConsentWizard (train_lora+face_embedding Art.11) + provider/tier + "Treinar" **fail-closed honesto** (OTD-AC-017) |
> 29	| `src/types/canvas.ts` · `canvas-node-registry.ts` · `CanvasEditorPage.tsx` · `RightPanel/index.tsx` | ✅ kind+AvatarIdentityData+factory+guard+cost + registry/nodeTypes/dispatch wiring |
> 30	| Browser-verify (Usuário Zero, preview do dist) | ✅ Nó no palette Cmd+K (Inputs) + render no canvas + inspector íntegro + **zero crash/console-error**; node count 3→4 |
> 31	| Deploy (`rsync` build verificado → `dist/` servido) | ✅ Chunk `CanvasEditorPage-DEjSoHib.js` (165.844B) contém o nó · env baked · LIVE em login.mcorch.com |
> 32	| `tsc --noEmit` / `eslint` / `vite build` | ✅ **0 erros** · 0 lint · build OK (chunk bundlado) |
> 33	
> 34	| Commit | Conteúdo |
> 35	|--------|----------|
> 36	| `7b81bfd` | docs(bok): emenda 3b Identity Gate VLM-soft (Workflow APPROVE, 6 issues dobradas) |
> 37	| `541f707` | feat: lib compare FR-AC-013b (15/15) + migration gate_mode (/security-review SAFE) |
> 38	| `12d06c0` | feat: nó Canvas avatarIdentity + inspector (FR-AC-012) — browser-verificado + deployed |
> 39	| `268a7325` | docs(loop): charter do loop autônomo + sovereign-queue runbook |
> 40	| `d023af0` | docs(readme): v6.62.0 — mesh 8997 |
> 41	
> 42	Handoff node `efb9d1c6-fed2-42e5-b991-cbc277f14df8` inserido + embedado (768d). Mesh **8997 nós**.
> 43	
> 44	### Arquitetura — Loop Autônomo + Identity Gate VLM-soft (3b)
> 45	```
> 46	/loop (auto-ritmado, dynamic mode) → ScheduleWakeup re-agenda cada ciclo
> 47	  └ charter (fonte da verdade: backlog + Fila Sovereign + ritual)
> 48	      └ por iteração: BoK Gate → SOP Lei 2 → código → prova Lei 1 → /security-review → commit
> 49	          └ portão físico Sovereign → registra na Fila + pula (NÃO improvisa)
> 50	
> 51	Identity Gate (3b, VLM-soft MVP — src/lib/avatar-identity.ts):
> 52	  ref portraits → vision_describe_image (enum JSON) → cache descrição canônica
> 53	  frame gerado → describe (N≥2 passes) → compareIdentityAttributes (enum-a-enum)
> 54	    → soft_match {pass/review/fail} vs arcface_threshold (CONFIG)
> 55	    → fail: regenerate seed-fixo (capped max_regen) · review: human-review-assist · pass: segue
> 56	  [ArcFace-hard deferido OTD-AC-015 · train deferido OTD-AC-017 — Fila Sovereign]
> 57	```
> 58	
> 59	## Session Seal — Gabriel AI: Fatia 2 (Clone de Voz) + Fatia 3a (Consentimento + Erasure LGPD) (2026-06-30)
> 60	
> 61	Sessão iniciada por `/handson` sob **ultracode**. Diretiva Sovereign: continuar o programa **Gabriel AI** (`avatar-clone-ai`) — BoK 10/10 já selada (gate ABERTO). Entregues duas fatias completas, verificadas em todas as camadas (DB · edge · smoke · `/security-review` · build · browser · Vision QA), e levantado honestamente o gate da Fatia 3b.
> 62	
> 63	**Arco 1 — Fatia 2 (Clone de Voz):** nó `voiceClone` no Canvas Studio existente (reuse-first, 6º node type) + edge fn `generate-voice` net-new (paralelo a `generate-image`): ações `clone`+`synthesize`, **ElevenLabs IVC/`eleven_multilingual_v2` + Cartesia `sonic-3.5` BYOK per-user fail-closed (402)**, **guard de code-switching** (FM-AC-013: gate-duro `profile.language===request.language` + heurística `detectCodeSwitch` espelhada client/edge), sentinel, débito atômico 36 mco **depois** dos gates + refund-on-fail, telemetria `service='avatar-clone-ai'` em todo path. Migration `20260630120000`: `voice_profiles` (RLS own, voiceprint cifrado no Vault) + RPCs `store/resolve_voice_profile` (SECURITY DEFINER service-role tenant-guarded) + `creative_assets.source_module += 'avatar-studio'`. Achado material: `elevenlabs`/`cartesia` keys **já existiam** no BYOK (Fatia 1) → zero migration de chave.
> 64	
> 65	**Arco 2 — Fatia 3a (Consentimento + Erasure):** backbone LGPD Art. 11/18. Migration `20260630130000`: `avatar_identities` (RLS own, embedding/HNSW, `arcface_threshold`/`identity_storage_key` staged-nullable p/ 3b) + `avatar_consents` **imutável** (trigger: só `revoked_at` muda) + `erase_avatar_artifacts` (SECURITY DEFINER, guard de tenant por linha, **revoga voiceprint no Vault in-RPC**, devolve `storage_keys`). Edge fns `avatar-consent` (grant, IP server-capturado, INSERT service-role) + `erase-avatar-artifacts` (Art. 18: RPC-como-user tenant-guarded + Storage API delete + atestado telemetria). **ConsentWizard** (3 checkboxes separados + atestado de titularidade, FR-AC-030) trava o "Clonar voz" até consent ativo; "Apagar dados de voz" (Art. 18). A `generate-voice` ganhou o **gate de consent** (clone exige consent ativo; síntese fail-closes em revogação total) — **sem regressão** no smoke da Fatia 2.
> 66	
> 67	**Fatia 3b (avatarIdentity + Identity Gate) — GATED (Lei 1, honesto):** probe de viabilidade provou ArcFace/InsightFace **ausente** no código; a BoK (FR-AC-013/014) exige ArcFace calibrado em **frames reais do Gabriel**; treino Soul ID exige plano pago Higgsfield + as fotos do Sovereign. Requer **emenda BoK** (ArcFace→VLM-soft MVP via Vision MCP, ou provisionar credencial face-verify — AWS Rekognition/Azure/Face++) + dados biométricos do Sovereign. NÃO improvisado (Closed-Loop Protocol).
> 68	
> 69	| Action | Result |
> 70	|--------|--------|
> 71	| `supabase/functions/generate-voice/` (NET-NEW) + `config.toml` | ✅ clone+synthesize BYOK fail-closed + code-switch guard + consent gate + refund · deployed 140kB ACTIVE |
> ```

## 🤖 Claude *(00:04:52)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 8492,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 8492	    └── DropdownMenu → "Monetizar Links ML"
> 8493	          → handleMonetizeLinks(item):
> 8494	               match(ML_URL_RE) → unique URLs
> 8495	               for url of unique:
> 8496	                 POST process-affiliate-link → affiliate_url
> 8497	                 body.split(url).join(affiliate_url)
> 8498	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 8499	          → Badge 💰 ML (emerald) exibido após monetização
> 8500	```
> 8501	
> 8502	---
> 8503	
> 8504	## Pending Actions (Commercial Launch)
> 8505	
> 8506	### CRITICAL — Must complete before first client
> 8507	
> 8508	🎯. **[✅ ATIVADO + VÍDEO 9:16 AUTÔNOMO — 2026-06-24 · pendente só: editor Studio (módulo-container) + postback ML + publish vertical] Viral Autopilot** — BoK 9/9 selada (`b3398294`). **✅ VÍDEO 9:16 (seal video-9x16-motor-and-autopilot, 2026-06-24):** (C) **RESOLVIDO** — motor HyperFrames determinístico VIVO (Fatia VS-2: `video-bridge.service` render 1080×1920 sha256-idêntico) + integração Autopilot (Fatia VA-V1: `orchestrate-step` enfileira render do ângulo viral REAL, custo no pré-débito do ciclo OTD-VA-010, attach content_library+creative_metrics OTD-VA-014) — provado E2E real (artigo Roborock → render 9:16 → biblioteca, saldo intacto prepaid). BoK Amendment v0.2 (FR-VA-022..026 + SOP `autopilot-video-9x16.md`) + flip OTD-VS-005 A→C (editor = módulo-container open-design, embed in-SPA inviável por React 19/18). `/security-review` SAFE ×2. **Próximo do vídeo:** **editor HyperFrames Studio** (módulo-container: deepsearch da API `@hyperframes/studio` → app React 19 → bridge → módulo frontend → vhost `studio.mcorch.com` [DNS Sovereign]) + **1º ciclo pago de vídeo witnessed** (habilitar `video_enabled` + GO) + (D) postback ML real + publish vertical TikTok/IG/YT (PR-VA-021, OAuth+App Review). **— histórico v6.48.0:** **✅ ATIVAÇÃO (seal autopilot-activation-security-hardening):** (A) heartbeat pg_cron `autopilot-cadence */15` jobid 3 `active` (migration `20260623040000`) + **1º ciclo PAGO real** `947ef8b5` (débito 22/refund 2, saldo 5096→5076) DONE; (B) **FR-VA-018** trend-informed angle com gate de fonte `sanitizeTrendTitle` + paridade pt-BR no sentinel (OTD-VA-018) DONE. Restam só (C) mídia 9:16 + (D) postback ML real. **Motor autônomo R1+R2+R3+R4 COMPLETO e provado zero-cost.** ✅ **Fatia 2 (cadência R2 + loop R3 + UI, commits `686bae3`→`bfd178b`):** SOP Lei 2 `autopilot-cron-identity.md` (OTD-VA-008 fechado) · migrations `20260620120000..120300` (`autopilot_plans`/`autopilot_cycles` FK composta tenant + RPCs `begin`/`finalize_autopilot_cycle` atômicos sob advisory-lock, service-role-only) · 6 edge fns deployadas (`autopilot-run` executor + `-cadence-cron` driver pg_cron + `-analyze` FR-VA-010 + `-collect` FR-VA-008 + `orchestrate-content` FR-VA-016 prepaid + `orchestrate-step` FR-VA-011 inject) · UI `/dashboard/autopilot` (`useAutopilot`+`AutopilotPage`). `/security-review` SAFE 3× · 3 smokes zero-cost (31 gates) · render ocular. **PENDENTE:** **(A)** ⚠️ **ação Sovereign** — ativar o **`pg_cron` schedule** que chama `autopilot-cadence-cron` (a função existe+provada; só o JOB pg_cron é ativação Sovereign-side, `Bearer SB_SECRET_KEY` via Vault) + rodar o **1º ciclo PAGO real** (mco real), gated nos 2 blockers de saída visível diagnosticados na Fatia 1b: **CF WAF skip `/wp-json/*`** + **OpenAI image model access**; **(B)** `fetch-trends`/`vm_trends`→pauta do ângulo viral (FR-VA-018, último item autônomo); **(C)** mídia viral 9:16 + TikTok/IG/YT (fase 2); **(D)** provar postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER). Constraints chave (cravados no código): `N_runs=prod×rede×ab_variants`, imagem no bundle de 10, refund crédito-positivo (NUNCA deduct negativo — anti-mint `20260603220000:45`), FK composta tenant-escopada, analyze inline=prepaid (reserva de 2 só vira actual com dado real).
> 8509	
> 8510	🌌. **[EM ANDAMENTO — Phase Epsilon V9] Unified Sensorial Canvas — Fases 3.5-3.10** — Fases 3.1-3.4 ✅ (scaffold rota/store/shell 72-28 + Code Network R3F InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; E2E ocular nos 3 modos; commits `210b90d`/`d832084`/`4940b4d`/`38d9760`/`769acb1`). **Restam:** **3.5** Sinapses inter-rede (arestas **REAIS** de `mcorch_edges` cruzando código↔memória, lit só no modo Universo — nunca fabricar) · **3.6** fly-to (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.7** layout/perf (`OTD-UCANVAS-PERF` — a query do código leva **~30s** com 2 canvases; considerar Louvain em Web Worker / streaming do grafo / lazy do backdrop) · **3.8** executar a poda do squad-coloring (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`. BoK selada (PR-025 · FR-043..049 · NFR-023/024 · SDD §9). **3 páginas legadas (matrix/memory/core-fable) preservadas como backup até 3.9.**
> 8511	
> 8512	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 8513	
> 8514	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 8515	
> 8516	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 8517	
> 8518	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 8519	
> 8520	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 8521	
> 8522	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 8523	
> 8524	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 8525	
> 8526	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 8527	
> 8528	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 8529	
> 8530	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 8531	   ```bash
> 8532	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 8533	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 8534	   ```
> 8535	
> 8536	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 8537	
> 8538	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 8539	
> 8540	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 8541	
> 8542	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 8543	
> 8544	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 8545	
> 8546	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 8547	
> 8548	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 8549	
> 8550	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 8551	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 8552	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 8553	
> 8554	### SOCIAL — Next steps
> 8555	
> 8556	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 8557	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 8558	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 8559	
> 8560	### NON-CRITICAL
> 8561	
> 8562	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 8563	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 8564	- `browserslist` — ✅ updated (2026-04-26)
> 8565	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 8566	
> 8567	### GITNEXUS MCP — Next steps
> 8568	
> 8569	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 8570	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 8571	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 8572	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 8573	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 8574	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 8575	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 8576	
> 8577	### PHASE EPSILON — Next iterations
> 8578	
> 8579	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 8580	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 8581	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 8582	
> 8583	### CORE — Next iterations
> 8584	
> 8585	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 8586	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 8587	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 8588	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 8589	
> 8590	### PHASE DELTA — Next iterations
> 8591	
> 8592	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 8593	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 8594	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 8595	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 8596	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 8597	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 8598	
> 8599	### USUÁRIO ZERO — Checklist de validação
> 8600	
> 8601	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 8602	- ✅ Stripe sandbox secrets no vault
> 8603	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 8604	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 8605	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 8606	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 8607	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 8608	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 8609	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 8610	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 8611	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 8612	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 8613	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 8614	
> 8615	---
> 8616	
> 8617	## Infrastructure
> 8618	
> 8619	| Service | Container | Port | Status |
> 8620	|---------|-----------|------|--------|
> 8621	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 8622	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 8623	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 8624	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 8625	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 8626	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 8627	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 8628	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 8629	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 8630	
> 8631	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 8632	
> 8633	```bash
> 8634	docker compose up -d
> 8635	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 8636	```
> 8637	
> 8638	---
> 8639	
> 8640	## Security Model (Post-Go-Live)
> 8641	
> 8642	| Table | Isolation |
> 8643	|-------|-----------|
> 8644	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 8645	| `mcorch_edges` | Same pattern |
> 8646	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 8647	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 8648	
> 8649	---
> 8650	
> 8651	## Billing Architecture
> 8652	
> 8653	| Decision | Value |
> 8654	|----------|-------|
> 8655	| Canonical billing ledger | `profiles.mco_balance` |
> 8656	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 8657	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 8658	| Orchestration cost | 10 mcoCoins/run |
> 8659	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 8660	| Stripe | Sandbox keys active — swap to live before first client |
> 8661	
> 8662	---
> 8663	
> 8664	## GraphRAG State
> 8665	
> 8666	- **8996 total nodes** (verificado live 2026-06-30 via REST count=exact, avatar-fatia2-voice-fatia3a-consent-erase seal: +handoff `c138539f-0365-436a-ad56-c65e013793c6` embedded 768d + milestone Fatia 2 `b51d8de6-e574-42aa-93b7-8fd75d85a717` — Gabriel AI **Fatia 2 (Clone de Voz)** [nó voiceClone + edge `generate-voice` BYOK ElevenLabs/Cartesia fail-closed + code-switch guard FM-AC-013 + voice_profiles RLS-own Vault + RPCs tenant-guarded; migration `20260630120000`; smoke 10/10; browser+VisionQA PASS] + **Fatia 3a (Consent+Erasure LGPD Art.11/18)** [avatar_identities/avatar_consents imutável + erase_avatar_artifacts tenant-guarded + edge `avatar-consent`/`erase-avatar-artifacts` + consent gate na generate-voice + ConsentWizard/erase UI; migration `20260630130000`; smoke 11/11]; Fatia 3b GATED (ArcFace ausente → emenda BoK + biometria Sovereign); 11 commits `d6515e9`..`7913546`; `/security-review` NO FINDINGS ×2; prev 8993)
> 8667	- **8993 total nodes** (verificado live 2026-06-30 via REST count=exact, gabriel-ai-fatia1-spaces-p0-kanban-live seal: +handoff `aba1458e-2df1-4813-a71b-34360bf7417e` embedded 768d — Programa Gabriel AI [deepsearch força-total → BoK `avatar-clone-ai` 10/10 selada nó `ee81987d` GO-HYBRID + Fatia 1 BYOK hedra/cartesia/fal] + Spaces canvas Phase 0 (scaffold promovido) + Kanban painel-de-detalhe + reconciliador vivo não-destrutivo + cron */15; 6 commits `a5814d2`..`71f4c47`; prev 8992 = BoK seal `ee81987d` `documentation_suite` avatar-clone-ai DERIVES_FROM video-studio `c99b7875`)
> 8668	- **8991 total nodes** (verificado live 2026-06-29 via REST count=exact, product-miner-vision-reliability-async seal: +handoff `1c100e2a-34f4-4b0a-a324-d89cba7ab0a8` embedded 768d — reparo de confiabilidade do Minerador (Vision MCP): Gemini Files API 20-100MB + cover-image fallback (rejeita stub <50KB) + `shouldDownloadVideos:true` vídeo rico em todo vídeo + `:free` 429→pago BYOK + síntese audience-fit/confidence/parser tolerante + extração ASSÍNCRONA timeout-proof [`vm_miner_jobs` RLS-owner/realtime + action `mine-async` EdgeRuntime.waitUntil + hook `useMinerJob` Realtime+polling + barra de progresso + notificação]; 10 commits prod-live; prev 8982 verificado live 2026-06-28 via REST count=exact, privacy-policy-google-oauth-compliance seal: +handoff `d5476bb8-c5ea-4dc4-a3c0-86d1e0895456` embedded 768d — política de privacidade endurecida p/ verificação Google OAuth: cláusula treino-IA Limited Use + §6 revogação/exclusão de tokens + §8 aviso de alterações + §5 segurança concreta [criptografia trânsito/repouso]; grounded na política Google + revisão adversarial 4/4; deployed login.mcorch.com/privacy + render browser-verificado; prev 8973 verificado live 2026-06-27 via REST count=exact, social-connect-tiktok-youtube-pinterest seal: +handoff `311a55b1-fb7b-410f-9582-625fb4721619` embedded 768d — conectar redes TikTok/YouTube/Pinterest: gate BoK post-engine + migration social_app_config Vault-cifrada aplicada/provada + helper fail-closed + 4 edge fns OAuth/publisher [deno 8/8, deployadas, 3×402 live] + UI browser-verified Vision-QA-high; FR-PE-013 video-cadence deferido; prev 8969 gabriel-ai-moodboard-vision-qa seal: +handoff `5501a101-f4fb-4431-a9d8-34f551353c95` embedded 768d — 1º ciclo pago vídeo 9:16 witnessed + billing/CTA fixes + LinkedIn cadence E2E + virada brand-persona Gabriel AI/CCIO + blueprint YT/TikTok + nó mood-board multi-foto + mood board 4 retratos Vision-QA-gated + 2 animações DoP + regra Vision QA + canvas prompt.length hardening; prev 8960 creative-assets-spine-fatia1 seal: +handoff `8eb84bce-f0d5-4463-a79b-9de9ab5892b9` embedded 768d — HyperFrames editor LIVE [video-studio.service + vhost SSO + iframe /dashboard/canvas/video] + auth gating ?devLogin + Canvas hydration-race bug fix + projeto 63d406fe recuperado + creative_assets SPINE [migration+RPC service-role-only, dual-write video-bridge/canvas-execute/generate-image, backfill 73, Biblioteca de Assets UI]; prev 8959 hyperframes-studio-blueprint-and-video-billing-fix seal: +handoff `b42e89f9-3636-4ff0-a86e-674ed479d3c5` embedded 768d via trigger — blueprint de integração do HyperFrames Studio [deepsearch `ae8b94c5`, StudioApp zero-props + seam StudioApiAdapter → módulo-container VS-UI] + fix do gap de billing OTD-VA-010 [crédito compensatório idempotente `refund_autopilot_video_enqueue` migration `20260624140000`, smoke 8/8 net-debit-exclui-12, /security-review SAFE]; prev 8958 video-9x16-motor-and-autopilot seal: +handoff `5e470dff-d7b3-4936-a130-2c34350d56c8` embedded 768d via trigger — vídeo 9:16 autônomo: VS-2 motor HyperFrames determinístico vivo [render-core Playwright+FFmpeg 1080×1920 sha256-idêntico, video-bridge.service, bucket, edge poll://] + VA-V1 integração Autopilot [orchestrate-step enfileira render do ângulo real, custo no pré-débito do ciclo, attach content_library+creative_metrics] + flip editor OTD-VS-005 A→C módulo-container; prev 8954 autopilot-activation-security-hardening seal: +handoff `bc175ac9-e8a8-483b-a32f-4660dd0b90ba` embedded 768d via trigger — 3 arcos: Viral Autopilot ATIVADO [1º ciclo pago `947ef8b5` + pg_cron jobid 3] + FR-VA-018 trend angle hardened + segurança social-auth [state HMAC + webhook IG sig] + paridade pt-BR Cyber-Sentinel OTD-VA-018; prev 8946 alertas-video-fatia1-de-n8n seal: +handoff `bb23b9dc-265e-4338-9709-d320371908b4` embedded 768d — alertas CF/security-drift + Vídeo Fatia 1 [video_renders/video_assets/finalize_video_render + edge video-render/poll] + Fatia 1b UI + emenda BoK SDD v1.2 De-n8n; prev 8935 viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 8669	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 8670	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 8671	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 8672	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 8673	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 8674	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 8675	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 8676	- HNSW cosine index operational
> 8677	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 8678	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 8679	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 8680	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 8681	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 8682	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 8683	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 8684	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 8685	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 8686	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 8687	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 8688	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 8689	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 8690	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 8691	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 8692	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 8693	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 8694	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 8695	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 8696	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 8697	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 8698	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 8699	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 8700	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 8701	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 8702	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 8703	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 8704	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 8705	
> 8706	### Embedding Model
> 8707	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 8708	Schema: `vector(768)` — HNSW cosine index.
> 8709	
> 8710	### Embedding Pipeline (Autônomo — 2026-05-03)
> 8711	Três camadas eliminam intervenção manual:
> 8712	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 8713	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 8714	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 8715	
> 8716	### Comandos de manutenção da Mesh
> 8717	```bash
> 8718	# Verificar nós sem embedding (deveria retornar array vazio):
> 8719	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 8720	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 8721	
> 8722	# Backfill manual (Bun-native — requer .env):
> 8723	bun run scripts/backfill-embeddings.ts
> 8724	
> 8725	# Backfill de código-fonte nos nós AST:
> 8726	bun run scripts/backfill-node-content.ts
> 8727	
> 8728	# Re-sync AST completo:
> 8729	cd packages/gitnexus-core && npm run sync-mesh
> 8730	
> 8731	# Acompanhar re-ingesta pós-commit:
> 8732	tail -f /tmp/mcorch-ingest.log
> 8733	```
> 8734	
> 8735	---
> 8736	
> 8737	## Video Rescue Protocol
> 8738	
> 8739	When a video generation operation (Google Veo) times out or client disconnects:
> 8740	```bash
> 8741	# Via edge function (production):
> 8742	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 8743	  -H "Authorization: Bearer <user_jwt>" \
> 8744	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 8745	
> 8746	# Via local script (admin/debug):
> 8747	source .env && bun run rescue.ts <operation_id> <content_id>
> 8748	```
> 8749	
> 8750	---
> 8751	
> 8752	## Architecture Pillars
> 8753	
> 8754	| Layer | Implementation |
> 8755	|-------|---------------|
> 8756	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 8757	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 8758	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 8759	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 8760	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 8761	
> 8762	---
> 8763	
> 8764	## Phase Delta — Architecture
> 8765	
> 8766	```
> 8767	OrchestrationPage (full-canvas, p-0)
> 8768	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 8769	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 8770	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 8771	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 8772	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 8773	        ├── nodes/PublishNode.tsx    ← final distribution output
> 8774	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 8775	        └── NodePalette.tsx          ← top toolbar to add nodes
> 8776	
> 8777	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 8778	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 8779	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 8780	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 8781	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 8782	```
> 8783	
> 8784	### Canvas State Architecture (Hybrid)
> 8785	
> 8786	```
> 8787	User interaction → ReactFlow internal state (positions, drag)
> 8788	                         ↓ (debounced 600ms)
> 8789	                   localStorage (positions persist across refresh)
> 8790	                         ↑
> 8791	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 8792	     ↓ (status changes sync to ReactFlow via useEffect)
> 8793	ReactFlow renders visual status (idle/running/done/error/blocked)
> 8794	```
> 8795	
> 8796	## Key Files
> 8797	
> 8798	| Purpose | Path |
> 8799	|---------|------|
> 8800	| Architecture rules | `CLAUDE.md` |
> 8801	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 8802	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 8803	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 8804	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 8805	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 8806	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 8807	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 8808	| **Node types** | `src/components/orchestrator/nodes/` |
> 8809	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 8810	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 8811	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 8812	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 8813	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 8814	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 8815	| Billing utilities | `src/lib/billing.ts` |
> 8816	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 8817	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 8818	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 8819	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 8820	| Video rescue (local) | `rescue.ts` |
> 8821	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 8822	| Backfill script | `scripts/backfill-embeddings.ts` |
> 8823	| Deploy harness | `scripts/harness-deploy.sh` |
> 8824	
> 8825	---
> 8826	
> 8827	## First Client Onboarding Checklist
> 8828	
> 8829	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 8830	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 8831	3. ~~Activate watchdog cron~~ ✅ Done
> 8832	4. ~~Deploy rescue-video function~~ ✅ Done
> 8833	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 8834	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 8835	7. Monitor `infra_health_logs` for first 24h.
> 8836	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 8837	
> 8838	---
> 8839	
> 8840	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 8841	
> 8842	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 8843	
> 8844	| Action | Result |
> 8845	|--------|--------|
> 8846	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 8847	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 8848	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 8849	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 8850	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 8851	
> 8852	| Commit | Conteúdo |
> 8853	|--------|----------|
> 8854	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 8855	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 8856	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 8857	
> 8858	### Arquitetura Matrix Intelligence
> 8859	
> 8860	```
> 8861	ConstellationMatrix (Stabilized Engine)
> 8862	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 8863	  └── NodeDetailsPanel (Tabbed Navigation)
> 8864	        ├── Tab Meta: Neighbor exploration + Net Context
> 8865	        ├── Tab Code: Source code preview (Supabase sync)
> 8866	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 8867	
> 8868	useNodeIntelligence Hook:
> 8869	  - contentQuery: fetch nodes.content column
> 8870	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 8871	  - state: isAnalyzing, analysisResult, progress
> 8872	```
> 8873	
> 8874	---
> 8875	
> 8876	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 8877	
> 8878	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 8879	
> 8880	| Action | Result |
> 8881	|--------|--------|
> 8882	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 8883	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 8884	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 8885	
> 8886	**Output da análise (estruturado em pt-BR):**
> 8887	- Visão Geral — papel do módulo no sistema
> 8888	- Padrões Detectados — design patterns, antipatterns
> 8889	- Acoplamento & Dependências — análise In/Out-Degree
> 8890	- Recomendações — 1-3 ações priorizadas
> 8891	
> ```

## 🤖 Claude *(00:04:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat .claude/context/sprint-priorities.md 2>/dev/null | head -80 || echo \"NO SPRINT FILE\"; echo \"===SCRATCH===\"; ls -la scratch/ 2>/dev/null",
  "description": "Sprint priorities and scratch contents"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> <persisted-output>
> Output too large (70.2KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/7d38a77b-f7f1-4e92-b419-5efbc0e5566c/tool-results/b8a4pukw6.txt
> 
> Preview (first 2KB):
> # 🧠 Sprint Priorities — Constellation Orchestra
> 
> **Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 
> **90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 
> **Sprint v6.53.0 — Doutrina Agêntica AGI→ASI + Learning & Adaptation + analytics honesto (2026-06-27)** — sessão-maratona multi-arco. **7 commits.** **(1)** Doutrina `agentic-vision.md` (21 padrões × maturidade + tese Via 4-produto/Via 3-micro) + **Pattern Conformance gate vinculante** no CLAUDE.md §1 + BoK `agentic-governance` 10/10 (seal `34748570`) + 2 docs stale deprecados. **(2)** **Collective Efficiency Ledger** (`81210ab`) — VIEW security_invoker + RPC service-role medem mco/resultado anti-Goodhart (G6 isolamento provado; rollup real 334s vs 2.4s). **(3)** **Learning & Adaptation** (o único padrão fraco) atacado: nervo sensorial (`publication_metrics` + coletor fail-soft IG/FB + painel "Por Publicação" browser-provado) + reward multi-métrica brand-first (mata `totalClicks` Goodhart, prova policy `7d9856d0`) + realocação ε-greedy (`1371094`/`47474ac`). **(4)** Analytics honesto — demo-kill (`b6abff1`) + zeramento dos perfis sociais antigos (marca **Gabriel AI**/**@gabrielOrchAI** começam do zero). **Prova:** tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8971** · handoff `326949f1`. **Pending:** re-OAuth IG insights (destrava o payoff visível) · B4 EWMA · B5 pauta de receita · V4-2 experimento · postback ML · emenda BoK post-engine (YT/TikTok). **Lição:** "não avançamos apesar do dev incrível" = o motor aprendia sobre **placar em branco**; medir o desfecho real é o que faz capacidade virar avanço.
> 
> ...
> </persisted-output>
> ```

## 🤖 Claude *(00:04:59)*


## 🤖 Claude *(00:05:00)*

Let me check the scratch/ contents (flagged as non-empty) and confirm the BoK gate for the active module.

## 🤖 Claude *(00:05:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null; echo \"===AVATAR BoK===\"; ls docs/bok/avatar-clone-ai/ 2>/dev/null",
  "description": "Scratch contents and avatar-clone-ai BoK docs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun 30 01:44 .
> drwx------ 31 ubuntu ubuntu 4096 Jun 30 21:00 ..
> ===AVATAR BoK===
> 00b-fatia0-viability-format-probe.md
> 00c-fatia0-fronts-closure.md
> 00-[[deepsearch-blueprint|deepsearch-blueprint]].md
> 00-index.md
> 01-mrd.md
> 02-brd.md
> 03-prd.md
> 04-frd.md
> 05-sdd.md
> 06-data-model.md
> 07-process-flow.md
> 08-quality-metrics.md
> 09-pattern-conformance.md
> 10-amendment-3b-identity-gate-vlm-soft.md
> ```

## 🤖 Claude *(00:05:21)*


## 🤖 Claude *(00:05:45)*

Contexto reunido. `scratch/` está de fato vazio (o `&&` disparou num diretório vazio — falso alarme). BoK do módulo ativo (`avatar-clone-ai`) completa (10/10 + emendas 3b). Segue o brief.

```
═══════════════════════════════════════════════════════════
  HANDSON — Gabriel AI · Fatia 3b (avatarIdentity VLM-soft) (2026-06-30)
═══════════════════════════════════════════════════════════
```

🏁 **ESTADO ATUAL**
- **Fase selada:** Gabriel AI **Fatia 3b** (`avatar-clone-ai`) — nó Canvas `avatarIdentity` + Identity Gate **VLM-soft MVP**, destravada via **loop autônomo de malha fechada** (`/loop` auto-ritmado governado por charter).
- **Últimos commits:**
  - `36eb30b` — chore(handoff): proof-manifest → efb9d1c6 (Fatia 3b seal)
  - `a2c8527` — docs(handoff): seal Gabriel AI Fatia 3b VLM-soft (mesh 8997)
  - `d023af0` — docs(readme): v6.62.0 — Fatia 3b destravada + nó avatarIdentity live
  - `268a732` — docs(loop): autonomous-loop charter + sovereign-queue runbook
  - `12d06c0` — feat(avatar-clone-ai): Fatia 3b — avatarIdentity Canvas node + inspector (FR-AC-012)

📂 **MUDANÇAS PENDENTES** — Worktree limpo ✅ (nada em staging/untracked)

🏗️ **INFRA**
- `mcorch_chroma`: Up 2 semanas (healthy) — Chroma API v2: **OK** (`heartbeat` respondeu)
- `mcorch_claude_mem`: Up 2 semanas (healthy)
- `mcorch_vision_mcp`: Up 30h (healthy) — *olho criativo/Identity Gate VLM-soft depende dele*
- `mega-brain-daemon` / `-webhook`: healthy · `-dashboard`: up

🧠 **KNOWLEDGE MESH**
- **8997 nós** (fonte: HANDOFF header pós-seal — handoff `efb9d1c6` embedado 768d) · 100% embedded HNSW cosine
- Aresta count snapshot: 9070+ (DERIVES_FROM/observes/ATTRIBUTES_REVENUE_TO)

🔧 **TYPESCRIPT** — Zero erros ✅

📚 **BoK SUITES** (MCORCH Master Execution Protocol)
- **25 suítes** em `docs/bok/`. Módulo ativo `avatar-clone-ai`: **completo** (00→09 + emenda `10-amendment-3b-identity-gate-vlm-soft.md`, aprovada por Workflow adversarial `wf_188ce24c`).
- **Gate:** ABERTO para as próximas fatias do Gabriel AI. Nenhum bloqueio de documentação.

📌 **SPRINT**
- **Goal:** Distribuição social autônoma operacional (LinkedIn publicando; Twitter/IG gated em tier/App Review).
- **Backlog vivo (fonte da verdade):** [`.claude/context/autonomous-loop-charter.md`](.claude/context/autonomous-loop-charter.md) — priorizado por valor + Fila de Ação Sovereign.

⚡ **PRÓXIMOS PASSOS** (prioridade)
1. **Puxar o próximo item desbloqueado da charter** (ritual do loop: git fetch → item de maior valor → BoK Gate → SOP Lei 2 → código → prova Lei 1). O `avatarIdentity`/Fatia 3b já está VIVO em VLM-soft; itens de maior valor visível pendentes incluem o **editor HyperFrames Studio (módulo-container)** e o **loop de receita** (postback ML real).
2. **Fila de Ação Sovereign** (destravadores físicos — NÃO improvisar, só registrar+pular): aplicar migration `20260630140000_avatar_identity_gate_mode.sql` no GO da 3b (não mutada em prod por ser feature gated) · **OTD-AC-015** ArcFace-hard (biometria do Sovereign) · **OTD-AC-017** treino Soul ID (plano pago Higgsfield + fotos).
3. **Viral Autopilot** — publish vertical TikTok/IG/YT (OAuth + App Review) + postback ML (atribuição de receita real).

⚠️ **ALERTAS** — Nenhum bloqueador ✅
- `scratch/` limpo (falso alarme do `ls` — diretório vazio).
- ℹ️ Migration `20260630140000` (gate_mode) **escrita mas não aplicada** — intencional (deferida ao GO da Fatia 3b; `/security-review` já passou NO FINDINGS).
- ℹ️ Diretiva Sovereign viva na memória: **open-source-first / custo USD externo = 0 / equity** + "entregar valor visível ao Usuário Zero, menos plumbing" — orienta a escolha do próximo item.

```
═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════
```

Contexto absorvido, Maestro. A última sessão fechou a **Fatia 3b** do Gabriel AI pela rota VLM-soft e formalizou o **loop autônomo** como infraestrutura. Infra 100% saudável, TS zero-erro, malha em 8997 nós, worktree limpo.

Quer que eu **religue o loop autônomo** e puxe o próximo item de maior valor da charter, ou tem uma direção específica para esta sessão?

## 👤 User *(00:07:37)*

<command-message>loop</command-message>
<command-name>/loop</command-name>
<command-args>Você é o MCORCH Master Execution Agent em MALHA FECHADA AUTÔNOMA. Leia .claude/context/autonomous-loop-charter.md (fonte da verdade do estado) + git fetch + Pending Actions do HANDOFF.md, e CONTINUE de onde a charter está. A cada iteração: (1) escolha o item de MAIOR valor DESBLOQUEADO no backlog; (2) ciclo fechado — BoK Gate → SOP Lei 2 → código → prova material Lei 1 → /security-review se houver migration → commit granular (Workflow p/ tarefas substantivas); (3) ao bater em portão Sovereign (biometria/DNS/OAuth/GO/decisão), NÃO improvise — registre na Fila de Ação Sovereign e pule; (4) Survival self-audit; (5) /handoff incremental ao fechar Fatia; selo final + PARE quando janela ~95% OU backlog desbloqueado vazio OU GO/stop. Reporte em PT-BR cada iteração.</command-args>

## 👤 User *(00:07:37)*

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

## 🤖 Claude *(00:07:44)*


## 🤖 Claude *(00:07:45)*

Entrando em **modo dinâmico auto-ritmado** (sem intervalo). Vou ler a charter (fonte da verdade), fazer `git fetch`, e executar o primeiro ciclo fechado agora. Começando pela leitura de estado.

## 🤖 Claude *(00:07:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git fetch origin 2>&1 | tail -3; echo \"---LOCAL vs ORIGIN---\"; git rev-parse HEAD; git rev-parse origin/main 2>/dev/null; echo \"---BEHIND/AHEAD---\"; git rev-list --left-right --count origin/main...HEAD 2>/dev/null || echo \"no upstream diff\"",
  "description": "Git fetch and compare local vs origin"
}
```

## 🤖 Claude *(00:07:47)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/autonomous-loop-charter.md"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ---LOCAL vs ORIGIN---
> 36eb30b9c2d32c5452c017d38794778715294631
> 36eb30b9c2d32c5452c017d38794778715294631
> ---BEHIND/AHEAD---
> 0	0
> ```

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
> 34	### 1. Gabriel AI — Fatia 3b (avatarIdentity + Identity Gate)  ⟶ programa-topo, estende a seal de hoje
> 35	- ✅ **Emenda BoK VLM-soft SHIPPED (it.1, commit `7b81bfd`):** `10-amendment-3b-identity-gate-vlm-soft.md` — Identity Gate dual-mode (VLM-soft MVP / ArcFace-hard deferido), verificado adversarialmente (wf_188ce24c-881 APPROVE, 6 issues dobradas). FR-AC-013b compare enum + gate_mode discriminador + telemetry key-migration definidos.
> 36	- ✅ **Fundação 3b SHIPPED (it.2, commit `541f707`):** lib de compare VLM-soft `src/lib/avatar-identity.ts` (FR-AC-013b — parse fail-soft + bands + reconcile N≥2 anti-oscilação, 15/15 testes) + migration `gate_mode` `20260630140000` (§4b, /security-review NO FINDINGS, aplicação deferida ao GO 3b). tsc 0.
> 37	- ✅ **Nó avatarIdentity SHIPPED + DEPLOYED (it.3, commit `12d06c0`):** FR-AC-012 — type+factory+componente+inspector+registry+nodeTypes+dispatch; upload multi-retrato (canvas-assets `user_id/`), ConsentWizard (train_lora+face_embedding Art.11), provider/tier, botão "Treinar" fail-closed honesto (OTD-AC-017). tsc 0 · eslint 0 · vite build 0. **Browser-verificado** (Usuário Zero, preview): nó no palette Cmd+K + render no canvas + inspector íntegro + zero crash/console-error. **Deployed** ao `dist/` servido (chunk `CanvasEditorPage-DEjSoHib.js` 165.844B contém o nó; env baked). Valor visível ao Sovereign LIVE.
> 38	- 🔒 **3b DESBLOQUEADO ESGOTADO** — o que resta é todo Sovereign-gated: edge `avatar-identity-train` (OTD-AC-017), gate-into-pipeline + telemetry migration §4b.2 (dependem do train+geração), calibração biométrica (OTD-AC-015). Próximo item do loop = **backlog #2 (YT/TikTok)** OU /handoff seal se janela ~95%.
> 39	- **HALT (Fila Sovereign):** edge `avatar-identity-train` (OTD-AC-017 Higgsfield) · treino/calibração com **frames biométricos reais do Gabriel** (OTD-AC-015) · GO de produção.
> 40	
> 41	### 2. Brand-persona YT/TikTok (post-engine)  ⟶ serve diretiva brand-first + distribuição/receita
> 42	- **DESBLOQUEADO:** emenda BoK `post-engine` (YT/TikTok); 3 branches net-new (`publish-social` · `social-auth` init+callback · refresh); fechar gap `auto-publish` não passar `video_url` + `VIDEO_FLOW_PLATFORMS`. Blueprint: `.claude/context/yt-tiktok-brand-persona-integration-prep-2026-06-26.md`.
> 43	- **HALT (Fila Sovereign):** audit OAuth YouTube (`videos.insert` nasce private) + TikTok (SELF_ONLY) — ação Sovereign + revisão de plataforma.
> 44	
> 45	### 3. Viral Autopilot — editor HyperFrames Studio (módulo-container)
> 46	- **DESBLOQUEADO:** `McorchAdapter.startRender` → edge `video-render`; bridge/app React 19 container; gate #1 render-parity (`frame=floor(time*fps)`). Blueprint: `.claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md`.
> 47	- **HALT (Fila Sovereign):** vhost `studio.mcorch.com` (DNS + cert + symlink).
> 48	
> 49	### 4. Unified Sensorial Canvas — Fases 3.5-3.10  ⟶ engenharia pura, SEM portão Sovereign (filler sempre disponível)
> 50	- 3.5 sinapses inter-rede (arestas reais `mcorch_edges`) · 3.6 fly-to · 3.7 perf (`OTD-UCANVAS-PERF`, query ~30s) · 3.8 podar squad-coloring · 3.9 paridade + gate E2E 1920×1080 · 3.10 seal. Plano: `.claude/context/unified-core-sensorial-canvas-plan.md`.
> 51	- **HALT:** nenhum até cutover de nav (3.9) — aí confirmar com Sovereign.
> 52	
> 53	### 5. Security — OTD-SEC-006 (sentinel-wiring) + OTD-SEC-007 (lefthook/gitleaks)  ⟶ hardening, desbloqueado
> 54	- BoK security 4/4 selada; resta implementação.
> 55	
> 56	---
> 57	
> 58	## Fila de Ação Sovereign (SÓ você destrava — preenchida pelo loop)
> 59	- [ ] **OTD-AC-015 (Gabriel AI 3b — ArcFace-HARD):** decidir/provisionar motor de embedding facial (InsightFace self-host no Mesh OU API paga Rekognition/Azure/Face++) + custo/credencial. Sem isso o Identity Gate fica VLM-soft (human-review-assist, não anti-impersonation automático).
> 60	- [ ] **OTD-AC-015b — biometria calibração-grade:** frames reais do Gabriel rotulados (mesma/diferente) p/ FAR/FRR/EER — só após o motor ArcFace existir.
> 61	- [ ] **OTD-AC-017 (Soul ID train):** credencial Higgsfield + confirmar API self-serve de treino (≥20 fotos); senão fallback Tier1/Tier2 ou LoRA-FLUX (gated commercial-license).
> 62	- [ ] **Licença comercial (FM-AC-001/OTD-AC-011):** confirmar checkpoint comercial da base de geração (FLUX.1-dev é non-commercial) — Sovereign + jurídico flipam `commercial_license_ok`.
> 63	- [ ] **GO de produção 3b** sobre o Usuário Zero + GO de gasto do loop de verificação caso não use BYOK openrouter (com BYOK = cost 0).
> 64	- [ ] **GO de gasto:** 1º ciclo PAGO de vídeo (`video_enabled` + GO) — testemunho. **Pipeline verificado end-to-end PRONTO** (render `8b0787e0` done, MP4 748KB no bucket, reconciliação FR-VA-025 OK); falta só `UPDATE autopilot_plans SET video_enabled=true WHERE id='640b3b67...'` + GO. **GATED pela doutrina open-source-first:** render HyperFrames já é self-hosted (USD≈0); antes do GO, auditar que os passos LLM (script/analyze) rodam BYOK-grátis → custo USD externo = 0. Custo interno ~24 mco/vídeo (saldo 4669 cobre).
> 65	- [ ] **DNS/vhost:** `studio.mcorch.com` (editor) e pendente `design.mcorch.com`.
> 66	- [ ] **OAuth/App Review:** YouTube (private default) · TikTok (SELF_ONLY) · Instagram App Review · Twitter Basic tier · re-OAuth IG insights (destrava analytics visível).
> 67	- [ ] **Postback ML definitivo:** IP residencial / portal ML (matt_tool/meli.la).
> 68	- [ ] **Stripe live keys:** ao primeiro cliente externo.
> 69	
> 70	---
> 71	
> 72	## Parar quando
> 73	janela ~95% (selo final) · OU backlog desbloqueado vazio · OU GO/stop explícito do Sovereign.
> 74	
> 75	---
> 76	
> 77	## Como religar / continuar o loop (prompt canônico STATELESS)
> 78	
> 79	> O loop se re-agenda sozinho via `ScheduleWakeup` ao fechar cada ciclo — **não precisa re-colar entre ciclos**. Cole o prompt abaixo SÓ para **religar após um stop**. É *stateless* de propósito: o estado vive nesta charter + no HANDOFF.md, então este texto nunca apodrece (nunca embuta "Estado: it.X / Próximo = …", que fica obsoleto).
> 80	
> 81	```
> 82	/loop Você é o MCORCH Master Execution Agent em MALHA FECHADA AUTÔNOMA. Leia
> 83	.claude/context/autonomous-loop-charter.md (fonte da verdade do estado) + git
> 84	fetch + Pending Actions do HANDOFF.md, e CONTINUE de onde a charter está. A cada
> 85	iteração: (1) escolha o item de MAIOR valor DESBLOQUEADO no backlog; (2) ciclo
> 86	fechado — BoK Gate → SOP Lei 2 → código → prova material Lei 1 → /security-review
> 87	se houver migration → commit granular (Workflow p/ tarefas substantivas); (3) ao
> 88	bater em portão Sovereign (biometria/DNS/OAuth/GO/decisão), NÃO improvise —
> 89	registre na Fila de Ação Sovereign e pule; (4) Survival self-audit; (5) /handoff
> 90	incremental ao fechar Fatia; selo final + PARE quando janela ~95% OU backlog
> 91	desbloqueado vazio OU GO/stop. Reporte em PT-BR cada iteração.
> 92	```
> 93	
> 94	**Redirecionar/parar:** mande PT-BR normal ("pula pra YT/TikTok", "para e mostra a Fila Sovereign", "stop") — interrompe o laço e reabsorvo a direção.
> 95	
> ```

## 🤖 Claude *(00:08:41)*


## 🤖 Claude *(00:08:47)*

Estado confirmado: local == `origin/main` (`36eb30b`), worktree limpo. Charter lida.

**Análise da charter:**
- **#1 Gabriel AI 3b** — DESBLOQUEADO ESGOTADO (resto é Sovereign-gated: OTD-AC-015/017). ✅ fechado na seal de hoje.
- **#2 Brand-persona YT/TikTok (post-engine)** — marcado DESBLOQUEADO, MAIOR valor (brand-first + receita). **Mas** uma seal posterior (`311a55b1`, mesh 8973) já entregou "4 edge fns OAuth/publisher TikTok/YT/Pinterest deployadas". Risco de charter parcialmente stale → **preciso verificar materialmente antes de abrir um ciclo substantivo** (Lei 1).
- **#3 HyperFrames Studio editor** — HALT vhost DNS (Sovereign).
- **#4 Unified Canvas 3.5-3.10** — engenharia pura, sem portão (filler).
- **#5 Security OTD-SEC-006/007** — hardening, desbloqueado.

Antes de escolher o ciclo, vou **provar o estado real do #2** (evita reconstruir o que a seal 8973 já fez). Probe read-only:

## 🤖 Claude *(00:08:59)*


🛠️ **Tool Call**: `Agent`
```json
{
  "description": "Probe YT/TikTok publish state",
  "subagent_type": "Explore",
  "prompt": "I need a precise, material map of the current state of YouTube/TikTok/Pinterest social publishing in this repo (constellation-orchestra), to decide what is ALREADY built vs. genuinely missing. Do NOT guess \u2014 cite exact file paths + line numbers for every claim. Search breadth: very thorough.\n\nAnswer these specific questions:\n\n1. **publish-social edge function** (`supabase/functions/publish-social/index.ts` and any siblings): Which social platforms does it currently handle (switch/if branches by platform)? Specifically does it have branches for `youtube`, `tiktok`, `pinterest`? Does it handle video vs. text/image differently? Does it read `video_url`?\n\n2. **social-auth / OAuth flows**: Search `supabase/functions/` for any OAuth init + callback + refresh functions for youtube/tiktok/pinterest. The prior seal (mesh 8973, commit 311a55b1) reportedly deployed \"4 edge fns OAuth/publisher\" for TikTok/YouTube/Pinterest and a migration `social_app_config` (Vault-encrypted). Find and list: which edge functions exist, what they do, and whether the `social_app_config` table/migration exists (search `supabase/migrations/` for `social_app_config`).\n\n3. **auto-publish function** (`supabase/functions/auto-publish/index.ts`): Does it pass `video_url` to publish-social? Is there a constant like `VIDEO_FLOW_PLATFORMS`? The charter claims a gap: \"auto-publish n\u00e3o passa video_url + add VIDEO_FLOW_PLATFORMS\". Verify whether this gap still exists by reading the actual code.\n\n4. **enum social_platform**: Search migrations for the postgres enum `social_platform` \u2014 does it already include `youtube`, `tiktok`, `pinterest`? Cite the migration.\n\n5. **BoK post-engine amendment for YT/TikTok video cadence**: List files in `docs/bok/post-engine/`. Is there an amendment doc covering YouTube/TikTok video publishing or `FR-PE-013 video-cadence`? Read any amendment/SDD file that mentions youtube/tiktok/video-cadence and summarize what FR-PE-013 covers and whether it's marked deferred/shipped.\n\n6. **social_accounts / social_credentials tables**: What columns exist for storing per-platform tokens (access_token, refresh_token, platform_user_id, expires_at)? Do youtube/tiktok rows fit the existing schema?\n\nReturn a structured summary: for each of the 3 platforms (youtube, tiktok, pinterest), state what EXISTS (connect/OAuth, token storage, publisher) and what is MISSING, with file:line citations. Then explicitly state whether the charter's \"3 branches net-new + auto-publish video_url gap\" is still accurate or already partially/fully done."
}
```

> **Tool Result (Agent)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': "Async agent launched successfully.\nagentId: a6f1724f20405073a (internal ID - do not mention to user. Use SendMessage with to: 'a6f1724f20405073a', summary: '<5-10 word recap>' to continue this agent.)\nThe agent is working in the background. You will be notified automatically when it completes.\nDo not duplicate this agent's work — avoid working with the same files or topics it is using.\noutput_file: /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/7d38a77b-f7f1-4e92-b419-5efbc0e5566c/tasks/a6f1724f20405073a.output\nDo NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification."}]
> ```

## 🤖 Claude *(00:09:17)*


## 🤖 Claude *(00:09:22)*

Probe lançado em background (harness-tracked — serei re-invocado ao completar). Este é o gate de decisão da **iteração 1**: não abro um Workflow substantivo no #2 até saber materialmente o que já existe (evita reconstruir o que a seal 8973 entregou).

**Modo dinâmico — auto-ritmado:**
- Rodei a tarefa agora (probe de estado do #2 em execução).
- Sem Monitor: o sinal primário de retomada é a **conclusão do agente Explore** (me re-invoca automaticamente).
- Fallback de segurança: agendo um wakeup longo caso o agente trave/não notifique.

Assim que o probe voltar, escolho o corte exato desbloqueado do #2 (ou reordeno para #4/#5 se o #2 estiver stale/já-feito) e executo o ciclo fechado.

## 🤖 Claude *(00:09:27)*


🛠️ **Tool Call**: `ScheduleWakeup`
```json
{
  "delaySeconds": 1500,
  "reason": "Fallback enquanto o probe Explore do estado YT/TikTok roda; a conclus\u00e3o do agente \u00e9 o sinal prim\u00e1rio de retomada do loop.",
  "prompt": "/loop Voc\u00ea \u00e9 o MCORCH Master Execution Agent em MALHA FECHADA AUT\u00d4NOMA. Leia .claude/context/autonomous-loop-charter.md (fonte da verdade do estado) + git fetch + Pending Actions do HANDOFF.md, e CONTINUE de onde a charter est\u00e1. A cada itera\u00e7\u00e3o: (1) escolha o item de MAIOR valor DESBLOQUEADO no backlog; (2) ciclo fechado \u2014 BoK Gate \u2192 SOP Lei 2 \u2192 c\u00f3digo \u2192 prova material Lei 1 \u2192 /security-review se houver migration \u2192 commit granular (Workflow p/ tarefas substantivas); (3) ao bater em port\u00e3o Sovereign (biometria/DNS/OAuth/GO/decis\u00e3o), N\u00c3O improvise \u2014 registre na Fila de A\u00e7\u00e3o Sovereign e pule; (4) Survival self-audit; (5) /handoff incremental ao fechar Fatia; selo final + PARE quando janela ~95% OU backlog desbloqueado vazio OU GO/stop. Reporte em PT-BR cada itera\u00e7\u00e3o."
}
```

> **Tool Result (ScheduleWakeup)** - ✅ Success
>
> ```
> Next wakeup scheduled for 21:35:00 (in 1532s). Nothing more to do this turn — the harness re-invokes you when the wakeup fires or a task-notification arrives.
> ```

## 🤖 Claude *(00:09:31)*

Iteração 1 em andamento — probe de estado do #2 rodando em background. Aguardando a conclusão do agente para escolher o corte exato e executar o ciclo fechado. Reporto o resultado assim que o probe voltar.

## 👤 User *(00:10:46)*

<task-notification>
<task-id>a6f1724f20405073a</task-id>
<tool-use-id>toolu_01TV1kRJVixVVN2eqd8ML1hX</tool-use-id>
<output-file>/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/7d38a77b-f7f1-4e92-b419-5efbc0e5566c/tasks/a6f1724f20405073a.output</output-file>
<status>completed</status>
<summary>Agent "Probe YT/TikTok publish state" finished</summary>
<note>A task-notification fires each time this agent stops with no live background children of its own. The user can send it another message and resume it, so the same task-id may notify more than once.</note>
<result>---

## PRECISE MATERIAL MAP: YouTube/TikTok/Pinterest Social Publishing

I have conducted a thorough audit of the constellation-orchestra codebase. Below is the exact state of the three platforms, with file paths and line numbers for every claim.

---

### 1. **PUBLISH-SOCIAL EDGE FUNCTION** (`/supabase/functions/publish-social/index.ts`)

**Platforms Implemented (ALL THREE + ALREADY FULLY BUILT):**

| Platform | Branch | Handles Video? | Key Lines |
|----------|--------|-------------------|-----------|
| **TikTok** | `if (platform === "tiktok")` | **YES** — `content.video_url` | Lines 263–390 |
| **YouTube** | `else if (platform === "youtube")` | **YES** — `content.video_url` | Lines 392–477 |
| **Pinterest** | `else if (platform === "pinterest")` | **YES** — `content.video_url` **OR** `content.image_url` | Lines 479–616 |

**Video URL Handling Details:**

- **TikTok** (lines 263–272): Fetches `videoUrl = content.video_url`; throws `PLATFORM_PUBLISH_FAILED` if missing (line 271).
- **YouTube** (lines 392–399): Fetches `videoUrl = content.video_url`; throws if missing.
- **Pinterest** (lines 479–488): Fetches `videoUrl = content.video_url`; also handles image fallback via `content.image_url` (line 485).

**Transfer Mechanisms:**
- **TikTok**: FILE_UPLOAD chunked (lines 299–357) — fetches bytes once, PUT with Content-Range headers.
- **YouTube**: Resumable upload (lines 410–450) — initiates resumable session, captures Location header, PUTs bytes.
- **Pinterest**: Multipart form-data upload (lines 541–556) — multipart POST with all upload parameters verbatim, file field last.

**Fallback &amp; Error Handling:**
All three emit telemetry to `infra_health_logs` via `pulse()` function (lines 117–121). Example: TikTok on missing video (line 270): `pulse("degraded", "tiktok_no_video")`.

---

### 2. **SOCIAL AUTH / OAUTH FLOWS**

**Edge Functions Deployed (4 core functions × 3 platforms):**

#### 2.1 **social-auth-init** (`/supabase/functions/social-auth-init/index.ts`)

| Platform | Auth URL | Lines | Credential Resolution |
|----------|----------|-------|------------------------|
| **TikTok** | `https://www.tiktok.com/v2/auth/authorize/` | 103–121 | `resolveSocialAppCreds(serviceClient, userId, "tiktok")` (line 112) |
| **YouTube** | `https://accounts.google.com/o/oauth2/v2/auth` | 123–140 | `resolveSocialAppCreds(serviceClient, userId, "youtube")` (line 131) |
| **Pinterest** | `https://www.pinterest.com/oauth/` | 142–159 | `resolveSocialAppCreds(serviceClient, userId, "pinterest")` (line 150) |

**Scope Handling:**
- TikTok (line 120): `"video.publish,user.info.basic"` (comma-separated — **CRITICAL**, space fails silently).
- YouTube (line 139): `"https://www.googleapis.com/auth/youtube.upload"` + `access_type=offline&amp;prompt=consent` (line 140).
- Pinterest (line 158): `"boards:read,boards:write,pins:read,pins:write,user_accounts:read"`.

#### 2.2 **social-auth-callback** (`/supabase/functions/social-auth-callback/index.ts`)

| Platform | Token Exchange URL | Lines | Platform ID Resolution |
|----------|---------------------|-------|----------------------|
| **TikTok** | `https://open.tiktokapis.com/v2/oauth/token/` | 179–205 | `tokenData.open_id` (line 203) |
| **YouTube** | `https://oauth2.googleapis.com/token` | 207–243 | `channels?mine=true` + `.id` (lines 235–241) |
| **Pinterest** | `https://api.pinterest.com/v5/oauth/token` (Basic auth) | 245–282 | `GET /v5/user_account` → `.username` (lines 277–282) |

**Token Storage (upsert to social_accounts):**
All three use identical upsert pattern (lines 293–309):
```sql
.upsert({
  user_id, platform, access_token, refresh_token, 
  token_expires_at, platform_user_id, platform_username, scopes, metadata
}, { onConflict: "user_id,platform" })
```

#### 2.3 **refresh-social-token** (`/supabase/functions/refresh-social-token/index.ts`)

| Platform | Refresh URL | Rotation Behavior | Lines |
|----------|-------------|-------------------|-------|
| **TikTok** | `https://open.tiktokapis.com/v2/oauth/token/` | **ROTATES** on every refresh | 143–177 |
| **YouTube** | `https://oauth2.googleapis.com/token` | Typically **NOT rotated** (COALESCE guard) | 178–212 |
| **Pinterest** | `https://api.pinterest.com/v5/oauth/token` | **ROTATES** on every refresh | 213–255 |

**Rotation Logic:**
- **TikTok** (line 171): `if (data.refresh_token) { await admin.from("social_accounts").update({ refresh_token: data.refresh_token })` — re-store new token atomically.
- **YouTube** (lines 206–210): COALESCE guard — `if (data.refresh_token) { ... update(...) }` **only if present** (never null over good token).
- **Pinterest** (lines 243–253): Atomic update + metadata rotation (`refresh_token_expires_at`).

#### 2.4 **Shared Credential Resolution** (`/supabase/functions/_shared/social-app-config.ts`)

**Export:** `resolveSocialAppCreds()` function (lines 53–91) implements **API Tenancy Model** with resolution order:
1. **Per-user** from `decrypted_social_app_config` (lines 62–79) — `user_id` + `platform` + `is_active=true`.
2. **Env fallback** (lines 83–86) — `TIKTOK_CLIENT_KEY/SECRET`, `GOOGLE_CLIENT_ID/SECRET`, `PINTEREST_CLIENT_ID/SECRET`.
3. **Hard fail** — throws `SocialAppConfigError(402)` (line 90) — "Configure em /dashboard/settings".

**Platforms Supported** (line 28–32):
```typescript
const ENV_MAP: Record&lt;SocialAppPlatform, { idEnv: string; secretEnv: string; label: string }&gt; = {
  tiktok: { idEnv: "TIKTOK_CLIENT_KEY", secretEnv: "TIKTOK_CLIENT_SECRET", label: "TikTok" },
  youtube: { idEnv: "GOOGLE_CLIENT_ID", secretEnv: "GOOGLE_CLIENT_SECRET", label: "YouTube" },
  pinterest: { idEnv: "PINTEREST_CLIENT_ID", secretEnv: "PINTEREST_CLIENT_SECRET", label: "Pinterest" },
};
```

---

### 3. **AUTO-PUBLISH FUNCTION** (`/supabase/functions/auto-publish/index.ts`)

**Video URL Transport — ALREADY IMPLEMENTED (gap CLOSED):**

The auto-publish function **DOES** pass `video_url` to publish-social:

- **Lines 74–102**: Resolves `video_url` from sibling `content_library` row:
  - Searches for row matching `campaign_id` + `type='video'` + `status='approved'` (lines 77–85).
  - Fetches media from private bucket with 6h signed URL (lines 87–96).
  - Passes as `content.video_url` to payload (line 111).

- **Lines 113–135**: Alternative path via **channel_variants** asset resolution:
  - Reads from `channel_variants.asset_bucket` + `asset_key` (per-row asset ref, fixes collision — line 124).
  - Determines asset type: `if (cv?.asset_kind === "video") native.video_url = url` (line 130).

**Payload Construction** (line 111):
```typescript
let contentPayload: unknown = videoUrl 
  ? { text: contentText, video_url: videoUrl } 
  : contentText;
```

**VIDEO_FLOW_PLATFORMS Constant** (`/supabase/functions/autopilot-run/index.ts`):

- **Line 114**: `const VIDEO_FLOW_PLATFORMS = new Set(["wordpress"]);`
- **Status**: Currently **wordpress-only**; the amendment prescribes adding `'youtube'`, `'tiktok'`, `'pinterest'` (docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md, line 87).
- **Usage** (lines 115, 250): Filters platforms to enqueue render + charge `VIDEO_COST`.

**Verdict on Charter Gap:** The charter stated "auto-publish não passa video_url + add VIDEO_FLOW_PLATFORMS" is now **PARTIALLY RESOLVED**:
- ✅ Video URL **IS** passed (lines 74–111).
- ⚠️ `VIDEO_FLOW_PLATFORMS` still needs `youtube`/`tiktok`/`pinterest` added to the Set (currently line 114 has only `"wordpress"`).

---

### 4. **ENUM social_platform**

**Location &amp; Definition** (`/supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql`):

**Line 12:**
```sql
CREATE TYPE public.social_platform AS ENUM ('linkedin', 'instagram', 'facebook', 'twitter', 'tiktok', 'youtube', 'pinterest', 'wordpress');
```

**Status:** ✅ **Already includes youtube, tiktok, pinterest** — **ZERO migration required**.

---

### 5. **SOCIAL_ACCOUNTS / SOCIAL_CREDENTIALS TABLES** (Token Storage)

**Base Table: social_accounts_table** (`/supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql`, lines 82–96):

```sql
CREATE TABLE public.social_accounts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  platform social_platform NOT NULL,
  platform_user_id TEXT,
  platform_username TEXT,
  access_token TEXT,                    -- Vault-encrypted
  refresh_token TEXT,                   -- Vault-encrypted
  token_expires_at TIMESTAMPTZ,
  scopes TEXT[],
  is_active BOOLEAN DEFAULT TRUE,
  metadata JSONB DEFAULT '{}',          -- Platform extras
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

**Schema Fits All Three Platforms:**
- ✅ `platform_user_id`: TikTok `open_id`, YouTube `channel_id`, Pinterest `username`.
- ✅ `access_token` + `refresh_token`: All three store both (Vault-encrypted).
- ✅ `token_expires_at`: TikTok 24h, YouTube ~1h, Pinterest 30d — all nullable.
- ✅ `metadata`: YouTube `channel_id`, Pinterest `refresh_token_expires_at` (per amendment line 273 in callback).

**Vault Encryption** (`/supabase/migrations/20260601000000_credential_encryption.sql`):
- Tokens stored as Vault secret UUIDs (never plaintext in base table).
- `decrypted_social_accounts` view (service-role only) exposes plaintext.
- Masked public view shows `'••••••••••••'`.

---

### 6. **social_app_config TABLE** (App Credentials per-user)

**Location** (`/supabase/migrations/20260627120000_social_app_config.sql`):

- **Base table** (lines 30–42): `social_app_config_table`
- **Columns** (lines 33–40):
  - `user_id`, `platform`, `client_id`, `client_secret` (Vault-encrypted), `scopes`, `metadata`, `is_active`.
- **UNIQUE constraint** (line 41): `(user_id, platform)`.
- **Encryption trigger** (lines 64–96): `trg_encrypt_social_app_config` mirrors `meta_config` pattern.
- **VIEW + INSTEAD OF** (lines 101–165): Masked view + tenant-guard (`auth.uid()=user_id`).
- **Decrypted view** (lines 170–188): Service-role only.

**Migration Status:** ✅ **20260627120000_social_app_config.sql** — deployed.

---

### 7. **BoK POST-ENGINE AMENDMENTS** (Video Cadence &amp; FR Status)

**Amendment Document:** `/docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md` (2026-06-27)

**FR-PE-013 through FR-PE-016 (Publish + Materiality):**

| FR | Title | Status | Lines in Amendment |
|----|-------|--------|-------------------|
| **FR-PE-013** | Publish TikTok (Direct Post) | ✅ SHIPPED (code complete) | Line 156; code at publish-social:263–390 |
| **FR-PE-014** | Publish YouTube (resumable) | ✅ SHIPPED (code complete) | Line 157; code at publish-social:392–477 |
| **FR-PE-015** | Publish Pinterest (video pin) | ✅ SHIPPED (code complete) | Line 158; code at publish-social:479–616 |
| **FR-PE-016** | Materiality + telemetry | ✅ SHIPPED | Line 159; code at publish-social:117–121 (pulse) + health logs |

**FR-PE-011 (Video Cadence):**
- **Line 154 in amendment:** "youtube/tiktok/pinterest entram em VIDEO_FLOW_PLATFORMS (autopilot-run:109)".
- **Current code state** (autopilot-run:114): Only `"wordpress"` in Set.
- **Status:** ⚠️ **DEFERRED** — not yet added to the constant, pending migration enablement.

**Video Transport Gap (amendment line 161):**
&gt; "Gap de transporte `video_url` (`auto-publish`): … **Decisão: resolver+assinar `content_library.media_url`→`video_url` no dispatch (sem migration)** …"

- **Status:** ✅ **CLOSED** — auto-publish lines 74–111 implement this.

---

### 8. **SUMMARY TABLE: PLATFORMS × IMPLEMENTATION STATUS**

| Aspect | TikTok | YouTube | Pinterest |
|--------|--------|---------|-----------|
| **Publish Branch** | ✅ Lines 263–390 | ✅ Lines 392–477 | ✅ Lines 479–616 |
| **OAuth Init** | ✅ Lines 103–121 | ✅ Lines 123–140 | ✅ Lines 142–159 |
| **OAuth Callback** | ✅ Lines 179–205 | ✅ Lines 207–243 | ✅ Lines 245–282 |
| **Token Refresh** | ✅ Lines 143–177 | ✅ Lines 178–212 | ✅ Lines 213–255 |
| **Enum Defined** | ✅ `social_platform` line 12 of 20260402014040 | ✅ Same | ✅ Same |
| **Token Storage (social_accounts)** | ✅ Fits schema | ✅ Fits schema | ✅ Fits schema |
| **App Config (social_app_config)** | ✅ Deployed 20260627120000 | ✅ Deployed | ✅ Deployed |
| **Video URL Passed in auto-publish** | ✅ Line 111 | ✅ Line 111 | ✅ Line 111 |
| **VIDEO_FLOW_PLATFORMS** | ⚠️ Not yet in Set | ⚠️ Not yet in Set | ⚠️ Not yet in Set |

---

### 9. **PRECISE VERDICT ON CHARTER CLAIMS**

**Charter stated:** "3 branches net-new (publish) + auto-publish video_url gap"

**Audit Result:**

1. **3 branches net-new for PUBLISH** ✅ **SHIPPED**
   - TikTok (publish-social:263–390): FILE_UPLOAD chunked 4-step (creator_info → init → PUT → status/fetch).
   - YouTube (publish-social:392–477): Resumable 4-step (initiate → Location → PUT → verify privacyStatus).
   - Pinterest (publish-social:479–616): 4-step (board cache → register → multipart → poll → create) + image fallback.

2. **auto-publish video_url gap** ✅ **CLOSED**
   - auto-publish DOES pass `video_url` (line 111).
   - Resolves from sibling `content_library` (lines 74–102) OR `channel_variants` asset (lines 113–135).
   - Signed URL TTL (6h) survives async fetch by Pinterest/IG.

3. **VIDEO_FLOW_PLATFORMS** ⚠️ **DEFERRED (not critical path)**
   - Charter gap confirmed: Set currently only `["wordpress"]` (autopilot-run:114).
   - Amendment prescribes adding `youtube`, `tiktok`, `pinterest` (amendment line 87).
   - This is **NOT blocking** publish; only affects **enqueue logic** (render + billing cadence).

4. **Migration table `social_app_config`** ✅ **DEPLOYED**
   - Migration 20260627120000 complete (lines 30–189).
   - Vault-encrypted, tenant-guarded, per-user resolution order.

5. **OAuth flows (4 functions × 3 platforms)** ✅ **DEPLOYED**
   - social-auth-init (3 branches: lines 103–159).
   - social-auth-callback (3 branches: lines 179–282).
   - refresh-social-token (3 branches: lines 143–255).
   - Shared credential resolution in _shared/social-app-config.ts.

---

### 10. **NO GAPS IN CONNECT/TOKEN STORAGE/PUBLISHER FOR ANY PLATFORM**

**YouTube:** ✅ Connect (OAuth init/callback/refresh) + Token storage (social_accounts) + Publisher (publish-social:392–477) + App creds (social_app_config).

**TikTok:** ✅ Connect + Token storage + Publisher (publish-social:263–390) + App creds.

**Pinterest:** ✅ Connect + Token storage + Publisher (publish-social:479–616 video OR 604–615 image) + App creds.

---

**Bottom Line:** The three platforms are **99% production-ready**. The only actionable gap is adding `youtube`, `tiktok`, `pinterest` to `VIDEO_FLOW_PLATFORMS` Set in autopilot-run.ts:114 (a 3-line change). The **real blockers are outside code**: app registration, OAuth audits, and tier gates (TikTok Content Posting audit ~2–6 weeks; YouTube gates A+B ~weeks; Pinterest Trial→Standard ~days).</result>
<usage><subagent_tokens>80677</subagent_tokens><tool_uses>21</tool_uses><duration_ms>106681</duration_ms></usage>
</task-notification>

## 🤖 Claude *(00:11:22)*


## 🤖 Claude *(00:11:27)*

O probe é **decisivo**. A charter #2 está ~99% já entregue pela seal 8973:

- ✅ `publish-social` — TikTok/YouTube/Pinterest completos com vídeo (linhas 263–616)
- ✅ OAuth init/callback/refresh — os 3 (`social-auth-*`)
- ✅ enum `social_platform`, `social_accounts`, `social_app_config` — todos presentes
- ✅ **auto-publish video_url gap CLOSED** — já passa `video_url` (linha 111)
- ✅ BoK `10-amendment-social-connect-tiktok-youtube-pinterest.md` — FR-PE-013..016 shipped

**Único gap de código real:** `VIDEO_FLOW_PLATFORMS` em `autopilot-run/index.ts:114` = `new Set(["wordpress"])` — a emenda prescreve adicionar `youtube`/`tiktok`/`pinterest`. O resto é Sovereign-gated (OAuth audits/App Review).

Antes de tocar a constante, preciso verificar **materialmente** a intenção da emenda + a implicação de billing (render/charge por plataforma vs. por ciclo — o Sovereign é sensível a cobrança-sem-valor). Lendo o código real:

## 🤖 Claude *(00:11:29)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-run/index.ts",
  "offset": 95,
  "limit": 180
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 95	    if (nRuns < 1) return json({ error: "plan_has_no_targets", detail: "plano sem produtos/redes válidos" }, 422);
> 96	
> 97	    // FR-VA-022/024 (Amendment v0.2): when the plan opts in, each sub-run enqueues ONE HyperFrames 9:16 render.
> 98	    // The cost rides on the cycle pre-debit (OTD-VA-010): projected/actual += N×VIDEO_COST. The render itself
> 99	    // never self-bills (charged_mco marker only); a FAILED render refunds via finalize_video_render.
> 100	    const videoEnabled = plan.video_enabled === true;
> 101	    const videoFormat = typeof plan.video_format === "string" ? plan.video_format : "9:16";
> 102	
> 103	    // Video charge accuracy (OTD-VA-010 follow-up — billing bug witnessed 2026-06-26, cycle 2403bfcb): a 9:16 render
> 104	    // is enqueued ONLY by the article_generation flow, which orchestrate-content runs solely for the 'wordpress'
> 105	    // platform (index.ts:231-232). A linkedin/twitter sub-run never reaches video_generation, so charging it
> 106	    // VIDEO_COST is charge-without-value — and uncaught by the orchestrate-step refund (orchestrate-step:454), which
> 107	    // fires only on a FAILED enqueue ATTEMPT, never for a flow that has no video step at all. So count video sub-runs
> 108	    // by the article-flow platform, not by every sub-run (was: nRuns × VIDEO_COST → over-charged non-wordpress runs).
> 109	    // FR-PE-013 (post-engine social-connect amendment) — DEFERRED: youtube/tiktok/pinterest ARE vertical-video
> 110	    // platforms, but the 9:16 render is enqueued ONLY by the article_generation step (gated on 'wordpress' above), and
> 111	    // autopilot fans out one platform per sub-run, so a youtube/tiktok/pinterest sub-run enqueues NO render. Adding
> 112	    // them here would charge VIDEO_COST with no video_renders row to refund (charge-without-value). Re-add ONLY with
> 113	    // the orchestrate-content/-step enqueue-gate extension (its own slice). Until then they stay out of the pre-debit.
> 114	    const VIDEO_FLOW_PLATFORMS = new Set(["wordpress"]);
> 115	    const videoPlatformCount = platforms.filter((p) => VIDEO_FLOW_PLATFORMS.has(p)).length;
> 116	    const nVideoRuns = videoEnabled ? products.length * videoPlatformCount * abVariants : 0;
> 117	
> 118	    const projected = nRuns * ORCH_COST + nVideoRuns * VIDEO_COST + ANALYZE_COST;
> 119	
> 120	    // ── FR-VA-018: trend-informed angle (cycle-level). Reconnects the trends island: pick a trend from vm_trends
> 121	    // (a GLOBAL shared catalog — no tenant scope) to steer THIS cycle's viral angle. Trend text is UNTRUSTED
> 122	    // (Apify/RapidAPI-mined) → the Cyber-Sentinel gates it BEFORE it reaches any prompt (NFR-VA-008), mirroring the
> 123	    // per-product gate in orchestrate-content (skip-and-continue: a blocked trend is dropped, not the whole angle).
> 124	    // Relevance: prefer a trend whose niche overlaps the cycle's products; else the freshest top-viral active trend.
> 125	    // Defense-in-depth: orchestrate-content re-inspects the full topic, so this is the first of two gates.
> 126	    // Graceful: empty vm_trends (the steady state until fetch-trends runs) → angle stays the plain product topic.
> 127	    let viralTopic = plan.name;
> 128	    let trendApplied: string | null = null;
> 129	    try {
> 130	      const { data: prodRows } = await admin
> 131	        .from("vm_affiliate_products").select("niches").in("external_id", products).eq("is_active", true);
> 132	      const productNiches = [...new Set(((prodRows ?? []) as Array<{ niches?: string[] | null }>)
> 133	        .flatMap((p) => p.niches ?? []).filter((n): n is string => typeof n === "string" && n.length > 0))];
> 134	      const fetchTrends = async (filterNiche: boolean) => {
> 135	        let q = admin.from("vm_trends").select("title, niche, viral_score")
> 136	          .eq("is_active", true).order("viral_score", { ascending: false }).limit(5);
> 137	        if (filterNiche && productNiches.length > 0) q = q.in("niche", productNiches);
> 138	        const { data } = await q;
> 139	        return (data ?? []) as Array<{ title: string | null; niche: string | null }>;
> 140	      };
> 141	      let candidates = await fetchTrends(true);
> 142	      if (candidates.length === 0) candidates = await fetchTrends(false);
> 143	      for (const t of candidates) {
> 144	        const clean = sanitizeTrendTitle(String(t.title ?? ""));
> 145	        if (!clean) { console.warn(`[autopilot-run] trend in niche '${t.niche}' rejected by trend gate (unsafe/empty) — skipped`); continue; }
> 146	        // Defense-in-depth: the generic Cyber-Sentinel still runs on the SANITIZED string we will interpolate.
> 147	        const v = inspectPrompt(clean, userId, { rateLimit: false });
> 148	        if (!v.allow) { console.warn(`[autopilot-run] trend in niche '${t.niche}' blocked by sentinel (${v.code}) — skipped`); continue; }
> 149	        trendApplied = clean;
> 150	        // Inert framing: the sanitized keyword is rendered as DATA ("tema em alta"), never as free instruction text.
> 151	        viralTopic = `${plan.name} (tema em alta: ${clean})`;
> 152	        break;
> 153	      }
> 154	    } catch (e) { console.warn(`[autopilot-run] trend angle skipped: ${e}`); }
> 155	
> 156	    // dry_run: return the cost projection (+ resolved trend angle) WITHOUT opening a cycle or deducting (zero-cost).
> 157	    if (dryRun) {
> 158	      return json({ ok: true, dry_run: true, n_runs: nRuns, projected_mco: projected,
> 159	        trend_applied: trendApplied, viral_topic: viralTopic,
> 160	        video: { enabled: videoEnabled, format: videoFormat, cost_each: VIDEO_COST, n_video: nVideoRuns },
> 161	        breakdown: { products: products.length, platforms: platforms.length, ab_variants: abVariants } });
> 162	    }
> 163	
> 164	    // ── begin_autopilot_cycle: ATOMIC cap-check + single pre-debit (or abort reason, no deduct). ────────────────
> 165	    const { data: begun, error: beginErr } = await admin.rpc("begin_autopilot_cycle", {
> 166	      p_plan_id: planId, p_user_id: userId, p_projected_mco: projected, p_planned_units: nRuns,
> 167	    });
> 168	    if (beginErr) { logHealth("error"); return json({ error: "begin_failed", detail: beginErr.message }, 500); }
> 169	    if (!begun?.ok) {
> 170	      const reason = begun?.reason ?? "aborted";
> 171	      // Hard stop (budget too low / insufficient balance) → pause the plan so it stops re-firing every tick.
> 172	      if (reason === "aborted_budget" || reason === "insufficient_balance") {
> 173	        await admin.from("autopilot_plans").update({ is_active: false }).eq("id", planId).eq("user_id", userId);
> 174	      }
> 175	      logHealth("degraded");
> 176	      return json({ ok: false, reason, projected_mco: projected }, reason === "insufficient_balance" ? 402 : 409);
> 177	    }
> 178	    const cycleId = begun.cycle_id as string;
> 179	
> 180	    // ── R3 loop (FR-VA-010/011): analyze the PREVIOUS completed cycle to steer THIS cycle's generation. ─────────
> 181	    // collect (sync the live click ledger → creative_metrics) then analyze (→ optimization_policy). Both inline and
> 182	    // PREPAID — the cycle reserved ANALYZE_COST(2); analyzeCharged consumes it only when real data produced a policy
> 183	    // (else finalize refunds the 2). Best-effort — a missing/empty previous cycle just means no steering this round.
> 184	    let analyzeCharged = 0;
> 185	    const svcCall = (fn: string, payload: unknown) => fetch(`${url}/functions/v1/${fn}`, {
> 186	      method: "POST",
> 187	      headers: { Authorization: `Bearer ${serviceKey}`, "Content-Type": "application/json" },
> 188	      body: JSON.stringify(payload),
> 189	    });
> 190	    try {
> 191	      const { data: prev } = await admin.from("autopilot_cycles")
> 192	        .select("id").eq("plan_id", planId).eq("user_id", userId).eq("status", "completed")
> 193	        .neq("id", cycleId).order("cycle_number", { ascending: false }).limit(1).maybeSingle();
> 194	      if (prev?.id) {
> 195	        await svcCall("autopilot-collect", { cycle_id: prev.id }).catch(() => {});
> 196	        const ar = await svcCall("autopilot-analyze", { previous_cycle_id: prev.id, prepaid: true })
> 197	          .then((r) => r.json()).catch(() => null);
> 198	        if (ar?.has_real_data) analyzeCharged = ANALYZE_COST;
> 199	      }
> 200	    } catch (e) { console.warn(`[autopilot-run] R3 analyze skipped: ${e}`); }
> 201	
> 202	    // ── Reallocation (FR-VA-030): bias the fan-out toward the policy winner, BUDGET-NEUTRAL (Σ variants stays nRuns
> 203	    // so the pre-debit holds). Winner product×platform gets +1 variant; the last non-winner pair gives up 1 (floor 1
> 204	    // = ε-greedy exploration — never collapse a pair to 0). No-op when ab_variants==1 (no room to move). The policy
> 205	    // is read scoped to THIS plan (mirrors the orchestrate-step fix). This is the lever: the policy now moves the
> 206	    // execution plan, not just the prompt hint.
> 207	    let winProd: string | null = null, winPlat: string | null = null;
> 208	    try {
> 209	      const { data: pol } = await admin.from("optimization_policy")
> 210	        .select("action_details").eq("user_id", userId).eq("action_type", "viral_autopilot")
> 211	        .eq("context->>scope", `viral_autopilot:${planId}`)
> 212	        .order("created_at", { ascending: false }).limit(1).maybeSingle();
> 213	      const ad = (pol as { action_details?: Record<string, unknown> } | null)?.action_details;
> 214	      winProd = (ad?.top_product_id as string) ?? null; winPlat = (ad?.top_platform as string) ?? null;
> 215	    } catch { /* policy read best-effort — never block the cycle */ }
> 216	
> 217	    const pairs: Array<{ product: string; platform: string; n: number }> = [];
> 218	    for (const productId of products) for (const platform of platforms) pairs.push({ product: productId, platform, n: abVariants });
> 219	    if (winProd && winPlat && abVariants >= 2) {
> 220	      const winner = pairs.find((p) => p.product === winProd && p.platform === winPlat);
> 221	      const donor = [...pairs].reverse().find((p) => !(p.product === winProd && p.platform === winPlat) && p.n > 1);
> 222	      if (winner && donor) { winner.n += 1; donor.n -= 1; }   // budget-neutral: Σ n stays = nRuns
> 223	    }
> 224	
> 225	    // ── Fan-out: (product × platform) × reallocated variants → orchestrate-content (prepaid → NO self-bill). ──────
> 226	    let succeeded = 0;
> 227	    let succeededVideo = 0;   // succeeded sub-runs whose flow enqueues a 9:16 render (article-flow / wordpress) — billing reconciliation
> 228	    const tasks: Array<() => Promise<void>> = [];
> 229	    for (const pair of pairs) {
> 230	      for (let v = 0; v < pair.n; v++) {
> 231	        tasks.push(async () => {
> 232	          try {
> 233	            const r = await fetch(`${url}/functions/v1/orchestrate-content`, {
> 234	              method: "POST",
> 235	              headers: {
> 236	                Authorization: `Bearer ${serviceKey}`,
> 237	                "x-autopilot-user-id": userId,
> 238	                "Content-Type": "application/json",
> 239	              },
> 240	              body: JSON.stringify({
> 241	                topic: viralTopic, platforms: [pair.platform], product_ids: [pair.product],
> 242	                prepaid: true, cycle_id: cycleId, wp_status: "draft",
> 243	                video_enabled: videoEnabled, video_format: videoFormat,
> 244	                // Publish opt-in (FR-CP-003): the autopilot auto-publishes UNLESS the plan requires human review.
> 245	                auto_publish: plan.hitl_required !== true,
> 246	              }),
> 247	            });
> 248	            if (r.ok) {
> 249	              succeeded++;
> 250	              if (videoEnabled && VIDEO_FLOW_PLATFORMS.has(pair.platform)) succeededVideo++;
> 251	            } else console.warn(`[autopilot-run] sub-run ${pair.product}/${pair.platform} → HTTP ${r.status}`);
> 252	          } catch (e) {
> 253	            console.warn(`[autopilot-run] sub-run ${pair.product}/${pair.platform} error: ${e}`);
> 254	          }
> 255	        });
> 256	      }
> 257	    }
> 258	    for (let i = 0; i < tasks.length; i += CONCURRENCY) {
> 259	      await Promise.all(tasks.slice(i, i + CONCURRENCY).map((t) => t()));
> 260	    }
> 261	
> 262	    // actual = successful runs × 10 + successful ARTICLE-FLOW runs × 12 (only those enqueue a render) + analyzeCharged.
> 263	    // Each succeeded article-flow sub-run enqueued one HyperFrames render (charged_mco marker, no self-bill); a FAILED
> 264	    // render later refunds its 12 via finalize_video_render. The reserved ANALYZE_COST(2) is consumed only when R3
> 265	    // produced a policy from real data; otherwise finalize refunds it. Zero successes → actual = analyzeCharged.
> 266	    const actual = succeeded * ORCH_COST + succeededVideo * VIDEO_COST + analyzeCharged;
> 267	    const status = succeeded > 0 ? "completed" : "failed";
> 268	    const { data: fin } = await admin.rpc("finalize_autopilot_cycle", {
> 269	      p_cycle_id: cycleId, p_actual_mco: actual, p_status: status,
> 270	    });
> 271	
> 272	    // ── Re-arm cadence (every_n_days) or deactivate after a single all_at_once run. ─────────────────────────────
> 273	    if (plan.mode === "every_n_days") {
> 274	      const days = Math.min(30, Math.max(1, Number(plan.interval_days ?? 3)));
> ```

## 🤖 Claude *(00:11:29)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md",
  "offset": 78,
  "limit": 95
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 78	1. `POST https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status` — headers `Authorization: Bearer`, `X-Upload-Content-Length=<bytes>`, `X-Upload-Content-Type=video/mp4`; body `{ snippet:{ title, description, tags, categoryId:'22' }, status:{ privacyStatus:'public', selfDeclaredMadeForKids:false, containsSyntheticMedia:true } }`.
> 79	2. capturar session URI do header `Location` (200).
> 80	3. PUT bytes (chunks múltiplos de 256KB + `Content-Range`; `308`=Resume Incomplete → retomar do byte do `Range`; tolerar `Range` AUSENTE = restart do 0; session-URI expira ~1 semana = re-iniciar).
> 81	4. sucesso = **`201`** com video resource id → `result.id`. Shorts é IMPLÍCITO (1080×1920 + ≤3min auto-classifica).
> 82	- **MATERIALIDADE (Lei 1):** `201` **NÃO** significa público — projeto não-verificado FORÇA todo upload a `private` ignorando o `privacyStatus` pedido. **Verificar `GET videos?id=&part=status` `privacyStatus='public'` antes de afirmar 'público'.** Cap diário do bucket `videos.insert` (~100 units/dia atualmente — **ler a Quota Calculator viva**, modelo de bucket é recente/móvel; Dec-2025 o custo caiu de ~1600 → ~100 units/call).
> 83	
> 84	**Refresh** (`refresh-social-token:133`) → `POST https://oauth2.googleapis.com/token` `grant_type=refresh_token` → novo `access_token` + `expires_in`; `token_expires_at=now()+3600s`.
> 85	- Google geralmente **não** rotaciona refresh tokens não-DPoP, mas tolerar um novo em re-consent e **NUNCA sobrescrever um token bom com null**. `invalid_grant` no dia 8 = app ainda em **Testing** (scope sensível → refresh expira 7d); fix é o gate A (In production), não retry-loop.
> 86	
> 87	**Cadência** (`autopilot-run:109`): `VIDEO_FLOW_PLATFORMS` (hoje `new Set(['wordpress'])`) ganha `'youtube'` (e `'tiktok'`/`'pinterest'` quando seus flows pousarem) → enfileira render 9:16 + cobra `VIDEO_COST`. Reconciliar billing em `:111` e `:243` (FR-VA-022/024).
> 88	
> 89	### 2.3 Pinterest — API v5 (video pin, 4 passos async) — **NET-NEW**
> 90	
> 91	**OAuth init** (`social-auth-init:95`) → `https://www.pinterest.com/oauth/`
> 92	- params: `client_id`, `redirect_uri` (match EXATO, sem wildcard), `response_type=code`, `scope=boards:read,boards:write,pins:read,pins:write,user_accounts:read`, `state`.
> 93	- **Planejar o set COMPLETO de scopes de cara** — adicionar scope depois força re-autorização total (refresh token existente não ganha). Sem PKCE (v5 é confidential-client Authorization-Code).
> 94	
> 95	**OAuth callback** (`social-auth-callback:171`) → `POST https://api.pinterest.com/v5/oauth/token`
> 96	- body: `grant_type=authorization_code` + `code` + `redirect_uri`; header `Authorization: Basic base64(client_id:client_secret)`.
> 97	- resposta: `access_token` (2592000s=30d), `refresh_token` (contínuo, **rotativo**), `refresh_token_expires_at`.
> 98	- identidade: `GET https://api.pinterest.com/v5/user_account`.
> 99	- upsert: `token_expires_at=now()+2592000s` + `metadata.refresh_token_expires_at`.
> 100	
> 101	**Publish** (`publish-social:233`) — VIDEO pin, 4 passos (+0 board):
> 102	0. **garantir board destino** — `GET https://api.pinterest.com/v5/boards` (achar `board_id`) senão `POST .../v5/boards` **UMA vez**; **cachear o `board_id` em `social_app_config.metadata.board_id` (NÃO criar por run)**.
> 103	1. **register**: `POST https://api.pinterest.com/v5/media { media_type:'video' }` → `media_id` + `upload_url` + `upload_parameters`.
> 104	2. **upload**: `POST` o MP4 no `upload_url` como `multipart/form-data` com TODOS os `upload_parameters` **VERBATIM** e o **campo `file` por ÚLTIMO** (ordenação de presigned-POST S3; ordem errada/param mutado → 403), **SEM Bearer**, sucesso = `204`.
> 105	3. **poll**: `GET https://api.pinterest.com/v5/media/{media_id}` com backoff até `status='succeeded'`.
> 106	4. **create**: `POST https://api.pinterest.com/v5/pins { board_id, title ≤100, description ≤800, link, media_source:{ source_type:'video_id', media_id, cover_image_url:'<URL https PÚBLICA>' } }` → `201` com pin id = `result.id`.
> 107	- **`cover_image_url` é OBRIGATÓRIA e é PUXADA async pela Pinterest** → a cover precisa sobreviver num URL público/signed-de-TTL-longo (TTL curto expira antes do fetch → pin falha em silêncio); o binário do vídeo é **enviado** (não puxado).
> 108	- **PATHS CORRETOS:** `/v5/pins`, `/v5/boards`, `/v5/media` (NÃO `/v5/pins/create` etc. — slugs de doc dão 404).
> 109	- **MATERIALIDADE (Lei 1):** sob **Trial** o pin é sandbox/creator-only — sem URL público resolvível — não afirmar 'publicado ao vivo' até **Standard**. Backoff em 429 contra `org_write` (300/dia Trial, 100/min Standard).
> 110	
> 111	**Refresh** (`refresh-social-token:133`) → `POST https://api.pinterest.com/v5/oauth/token` `grant_type=refresh_token`, header Basic.
> 112	- **ROTATIVO — cada refresh retorna NOVO access_token E NOVO refresh_token**; persistir ambos **ATOMICAMENTE** (advisory-lock / SELECT-FOR-UPDATE em torno do refresh→persist, espelhando `begin_autopilot_cycle`) p/ evitar lost-update entre cron e run manual que quebra a cadeia e força re-OAuth. Refrescar dentro da janela de 60d mantém a cadeia viva indefinidamente.
> 113	
> 114	---
> 115	
> 116	## 3. Fatos fundamentados — tokens, audit gates, specs (verificado HIGH)
> 117	
> 118	| | TikTok | YouTube | Pinterest |
> 119	|---|---|---|---|
> 120	| **Access token (lifetime)** | 24h (86400s) | ~1h (3600s) | 30d (2592000s) |
> 121	| **Refresh token** | 365d, **rotativo** | longo (prod-verified); **7d em Testing** | 60d-from-last-use, **rotativo contínuo** |
> 122	| **Gate 1 (conexão)** | registrar app + Content Posting API Direct Post + add conta como sandbox target user | criar/converter canal Brand + OAuth consent (External) | Business account + Developer Terms + privacy-policy URL → Trial |
> 123	| **Gate 2 (público)** | **audit** Content Posting (~2–6 sem) — sem ele: SELF_ONLY + conta privada + ≤5 users/24h | **(A)** OAuth verification de scope sensível (~10 dias) + **(B)** API Audit & Quota Extension (semanas, **serial+independente** de A) — sem B: upload FORÇADO a private | **Trial→Standard** (demo OAuth + ação API ao vivo) — sem ele: sandbox/creator-only |
> 124	| **Transfer de mídia** | FILE_UPLOAD chunked (signed URL não passa no PULL_FROM_URL) | resumable PUT (fetch bytes → PUT; sem ingest remoto) | register→multipart(params verbatim, file last)→poll→create + cover PÚBLICA |
> 125	| **Rate/cap** | init 6/min · ~15 posts/dia/criador | `videos.insert` ~100/dia (bucket próprio, modelo móvel) | `org_write` 300/dia Trial · 100/min Standard |
> 126	
> 127	> **Gates A+B do YouTube são SERIAIS+independentes → prontidão total = a SOMA (~10d + semanas), não o máximo.** Submeter **ambos no dia 1**.
> 128	
> 129	---
> 130	
> 131	## 4. Resolução de credencial de app + OTD do deferimento (API Tenancy Model)
> 132	
> 133	**Resolution order (UNBREAKABLE — espelha o API Tenancy Model do CLAUDE.md):**
> 134	1. `social_app_config` per-user (`user_id=auth.uid()` AND `is_active=true`) — `client_id` + `client_secret` (Vault) + `scopes` + `metadata`.
> 135	2. **Env fallback** (default Sovereign-only de onboarding): `TIKTOK_CLIENT_KEY`/`TIKTOK_CLIENT_SECRET`, `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET`, `PINTEREST_CLIENT_ID`/`PINTEREST_CLIENT_SECRET`.
> 136	3. **Hard fail** — `HTTP 402/501 { error:"<platform>_not_configured", action:"Configure suas credenciais de <plataforma> em /dashboard/settings" }`. NUNCA shared key silenciosa.
> 137	
> 138	**OTD-PE-SOCIAL-APPCREDS (deferimento de credencial env · RPN moderado · SLA: antes do 2º tenant):** as 3 slices probe rodam com **env creds** (Usuário Zero é o único tenant e os 3 audits são o caminho crítico real, não a tabela de config). A coluna `is_active` per-user em `social_app_config` é o caminho primário; o env só é alcançado quando não há linha per-user ativa. **Promover env→per-user (UI Settings + `is_active`) antes de onboardar o 2º tenant** — senão vira dívida silenciosa de credencial compartilhada. (Decisão aberta #1 do blueprint.) Os **tokens de usuário** já vão per-user para `social_accounts` em qualquer caso.
> 139	
> 140	---
> 141	
> 142	## 5. Novos Functional Requirements (FR-PE-005..016)
> 143	
> 144	> A FRD v0.1 (`04-frd.md`) usa FR-PE-001..004. Esta emenda **continua a partir de FR-PE-005** (próximo id livre confirmado).
> 145	
> 146	| ID | Title | Description | Priority | Category |
> 147	|----|-------|-------------|----------|----------|
> 148	| **FR-PE-005** | App credentials per-user (`social_app_config`) | Tabela única `(user_id, platform)` UNIQUE com `client_secret` Vault-cifrado + column-REVOKE + INSTEAD OF tenant-guard; resolution order per-user→env→hard-fail (§4). | Critical | DB / Edge |
> 149	| **FR-PE-006** | OAuth init TikTok | Branch `social-auth-init:95` → authorize URL `tiktok.com/v2/auth/authorize/`, scope `video.publish,user.info.basic` (vírgula), `state` assinado. | Critical | Edge Function |
> 150	| **FR-PE-007** | OAuth init YouTube | Branch → `accounts.google.com/o/oauth2/v2/auth`, scope `youtube.upload`, `access_type=offline`+`prompt=consent`. | Critical | Edge Function |
> 151	| **FR-PE-008** | OAuth init Pinterest | Branch → `pinterest.com/oauth/`, scope completo `boards:*,pins:*,user_accounts:read`, redirect match-exato. | Critical | Edge Function |
> 152	| **FR-PE-009** | OAuth callback (3 plataformas) | Branches `social-auth-callback:171` trocam `code`→token e fazem upsert em `social_accounts` (TikTok `open_id`; YouTube `channel_id` via `channels?mine=true`, COALESCE-guard no refresh; Pinterest Basic auth + `user_account`). | Critical | Edge Function |
> 153	| **FR-PE-010** | Refresh rotativo atômico | Branches `refresh-social-token:133` re-armazenam o `refresh_token` retornado quando rotaciona (TikTok/Pinterest rotativos; Pinterest persiste access+refresh **atomicamente** com advisory-lock); nunca sobrescrever token bom com null (YouTube). | Critical | Edge Function |
> 154	| **FR-PE-011** | Cadência de vídeo nas novas plataformas | `youtube`/`tiktok`/`pinterest` entram em `VIDEO_FLOW_PLATFORMS` (`autopilot-run:109`); render 9:16 enfileirado + `VIDEO_COST` cobrado/reconciliado (`:111`/`:243`). | High | Cron / Billing |
> 155	| **FR-PE-012** | Disclosure AIGC obrigatório | Todo publish marca conteúdo IA-gerado: TikTok `is_aigc=true`, YouTube `containsSyntheticMedia=true` (compliance, não opcional); `brand_content_toggle` suprimido quando SELF_ONLY. | Critical | Edge Function |
> 156	| **FR-PE-013** | Publish TikTok (Direct Post) | 4 passos `creator_info→init(FILE_UPLOAD)→PUT chunks→status/fetch` com guard de idempotência (content/run id antes do init) + `fail_reason` switch. | Critical | Edge Function |
> 157	| **FR-PE-014** | Publish YouTube (resumable) | initiate→`Location`→PUT(256KB,308-resume)→`201`→**verificar `privacyStatus`** antes de afirmar público. | Critical | Edge Function |
> 158	| **FR-PE-015** | Publish Pinterest (video pin) | board cache→`/v5/media` register→multipart(params verbatim, file last, 204)→poll `succeeded`→`/v5/pins` com `cover_image_url` pública. | Critical | Edge Function |
> 159	| **FR-PE-016** | Materialidade + telemetria + mesh node | Sucesso ≠ 2xx: TikTok `PUBLISH_COMPLETE`+`publicaly_available_post_id` · YouTube `privacyStatus='public'` · Pinterest URL público (pós-Standard). Cada path emite `infra_health_logs` `service='publish-<platform>'`; 1º sucesso por plataforma insere observation node + edge `PUBLISHED_ON` na mesh. | Critical | Edge Function / Mesh |
> 160	
> 161	**Gap de transporte `video_url` (`auto-publish`):** não há coluna `video_url` em `scheduled_posts`; o `auto-publish` nunca resolve/assina `media_url`. **Decisão (blueprint #4):** resolver+assinar `content_library.media_url`→`video_url` no dispatch (sem migration), signed URL de TTL longo (horas) p/ sobreviver ao fetch async de Pinterest/IG. Fecha o gap (hoje passa só texto) e também conserta o IG Reel agendado. (Coberto por FR-PE-011.)
> 162	
> 163	---
> 164	
> 165	## 6. ⚠️ Ações Sovereign — CAMINHO CRÍTICO (fora do código, lead-time de semanas)
> 166	
> 167	> **Sem o registro do app não há `client_id`/`secret` → nenhum OAuth começa.** Começar HOJE; os audits têm o maior lead-time e correm em paralelo ao código.
> 168	
> 169	| # | Ação | Plataforma | Destrava | Lead-time |
> 170	|---|---|---|---|---|
> 171	| 1 | Registrar app TikTok + Content Posting API (Direct Post) + add a conta da persona como sandbox target user | TikTok | client_key/secret + teste E2E pré-audit | horas–2 dias |
> 172	| 2 | Submeter **TikTok Content Posting API audit** (usage-estimates + walkthrough/screencast de UX compliant) | TikTok | posts PÚBLICOS (levanta SELF_ONLY/privado/≤5 users) | **~2–6 semanas** (sem SLA) |
> ```

## 🤖 Claude *(00:13:44)*


## 🤖 Claude *(00:13:51)*

O probe expõe um **detalhe crítico** que muda a decisão. O código em `autopilot-run:103-113` documenta explicitamente **por que** yt/tiktok/pinterest NÃO estão em `VIDEO_FLOW_PLATFORMS`:

> *"Adding them here would charge VIDEO_COST with no video_renders row to refund (charge-without-value). Re-add ONLY with the orchestrate-content/-step enqueue-gate extension (its own slice)."*

Ou seja: a mudança de 3 linhas é **ativamente errada** (cobrança-sem-valor — o exato bug que o Sovereign odeia). O render 9:16 só é enfileirado pelo `article_generation` (gated em `wordpress`); um sub-run youtube/tiktok não produz `video_renders` → cobra sem linha p/ refund. O slice real é **render-decoupling** (substantivo), e seu valor de publish é **OAuth-gated por semanas** — e o **app nem foi registrado** (amendment §6 step 1: sem `client_id`, nada roda).

**Veredito da iteração 1 (material):** a charter #2 é um *false-high* — 99% já entregue pela seal 8973, e o que resta ou é um trap de billing ou tem valor travado no físico do Sovereign. Vou **corrigir a charter** (Lei 1/Lei 2: registrar o achado + o trap documentado), afiar a Fila Sovereign (app-registration = o unlock real), commitar, e **pivotar para o próximo item desbloqueado+visível**.

Atualizando a charter:

## 🤖 Claude *(00:14:02)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/autonomous-loop-charter.md",
  "old_string": "### 2. Brand-persona YT/TikTok (post-engine)  \u27f6 serve diretiva brand-first + distribui\u00e7\u00e3o/receita\n- **DESBLOQUEADO:** emenda BoK `post-engine` (YT/TikTok); 3 branches net-new (`publish-social` \u00b7 `social-auth` init+callback \u00b7 refresh); fechar gap `auto-publish` n\u00e3o passar `video_url` + `VIDEO_FLOW_PLATFORMS`. Blueprint: `.claude/context/yt-tiktok-brand-persona-integration-prep-2026-06-26.md`.\n- **HALT (Fila Sovereign):** audit OAuth YouTube (`videos.insert` nasce private) + TikTok (SELF_ONLY) \u2014 a\u00e7\u00e3o Sovereign + revis\u00e3o de plataforma.",
  "new_string": "### 2. Brand-persona YT/TikTok (post-engine)  \u27f6 serve diretiva brand-first + distribui\u00e7\u00e3o/receita\n- \u2705 **QUASE TODO SHIPPED (seal 8973, `311a55b1`) \u2014 verificado por probe material (loop it.1, 2026-06-30):** `publish-social` TikTok/YouTube/Pinterest com v\u00eddeo (linhas 263\u2013616) \u00b7 OAuth init/callback/refresh dos 3 (`social-auth-*`) \u00b7 enum `social_platform` j\u00e1 tem yt/tiktok/pinterest \u00b7 `social_accounts`/`social_app_config` (migration `20260627120000`) \u00b7 **gap `auto-publish` video_url CLOSED** (resolve+assina content_library/channel_variants \u2192 `auto-publish:111`) \u00b7 BoK `10-amendment-social-connect-*` FR-PE-005..016. Publish/OAuth/refresh/tables = SHIPPED.\n- \ud83e\udea4 **\u00daNICO gap de c\u00f3digo = render-decoupling slice (N\u00c3O o 3-line `VIDEO_FLOW_PLATFORMS`):** adicionar yt/tiktok/pinterest a `VIDEO_FLOW_PLATFORMS` (`autopilot-run:114`) HOJE \u00e9 **charge-without-value** \u2014 documentado no pr\u00f3prio c\u00f3digo (`:103-113`): o render 9:16 s\u00f3 \u00e9 enfileirado pelo `article_generation` (gated em `wordpress`), e o autopilot fana 1 plataforma/sub-run, ent\u00e3o um sub-run youtube/tiktok N\u00c3O produz `video_renders` \u2192 cobraria VIDEO_COST sem linha p/ refund. Slice real = estender `orchestrate-content`/`-step` p/ enfileirar o render 9:16 em sub-run de plataforma-v\u00eddeo **ou** reusar 1 render/ciclo (campaign_id compartilhado) com billing correto (charge 1\u00d7, refund-on-fail). Substantivo \u2192 Workflow quando priorizado.\n- \ud83d\udd12 **VALOR OAuth-GATED (por que o loop pula):** mesmo com o render-decoupling, publish vis\u00edvel trava nos audits (TikTok Content Posting ~2-6sem \u00b7 YouTube gates A+B ~semanas \u00b7 Pinterest Trial\u2192Standard) \u2014 **e o app nem foi registrado** (amendment \u00a76 step 1) \u2192 sem `client_id` nada roda. App-registration \u00e9 O unlock. C\u00f3digo roda em paralelo aos audits, mas N\u00c3O \u00e9 test\u00e1vel E2E at\u00e9 o OAuth existir (Lei 1). \u2192 registrado na Fila; loop segue pro pr\u00f3ximo desbloqueado+vis\u00edvel."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/.claude/context/autonomous-loop-charter.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:14:06)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/autonomous-loop-charter.md",
  "old_string": "- [ ] **OAuth/App Review:** YouTube (private default) \u00b7 TikTok (SELF_ONLY) \u00b7 Instagram App Review \u00b7 Twitter Basic tier \u00b7 re-OAuth IG insights (destrava analytics vis\u00edvel).",
  "new_string": "- [ ] **App registration (STEP 0 \u2014 o unlock de TODO o #2, ainda N\u00c3O feito, lead ~horas-2d):** registrar apps TikTok (Content Posting API Direct Post + add persona como sandbox user) \u00b7 YouTube/Google Cloud (canal Brand + OAuth consent External) \u00b7 Pinterest (Business + Developer Terms + privacy URL \u2192 Trial). Sem `client_id`/`secret` nenhum OAuth come\u00e7a. Submeter os audits no MESMO dia (lead-time corre em paralelo ao c\u00f3digo).\n- [ ] **OAuth/App Review (ap\u00f3s registration, lead semanas):** TikTok Content Posting audit (~2-6sem \u2014 levanta SELF_ONLY) \u00b7 YouTube gate A (OAuth verify ~10d) + gate B (API Audit & Quota, serial+independente) \u00b7 Pinterest Trial\u2192Standard \u00b7 Instagram App Review \u00b7 Twitter Basic tier \u00b7 re-OAuth IG insights (analytics vis\u00edvel)."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/.claude/context/autonomous-loop-charter.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:14:12)*


## 🤖 Claude *(00:14:13)*

Charter corrigida. Commitando o achado material (Lei 1/Lei 2 — corrige o roadmap + documenta o trap de billing):

## 🤖 Claude *(00:14:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git add .claude/context/autonomous-loop-charter.md && git commit -q -m \"docs(loop): charter it.1 \u2014 #2 YT/TikTok \u00e9 false-high (probe material)\n\nProbe read-only (Explore) provou que a seal 8973 (311a55b1) j\u00e1 entregou\npublish-social (tik/yt/pin com v\u00eddeo), OAuth init/callback/refresh, enum,\nsocial_accounts/social_app_config e o gap auto-publish video_url (CLOSED).\nO \u00fanico gap de c\u00f3digo restante N\u00c3O \u00e9 o 3-line VIDEO_FLOW_PLATFORMS \u2014 isso\nseria charge-without-value (documentado em autopilot-run:103-113): render\n9:16 s\u00f3 \u00e9 enfileirado pelo article_generation (gated wordpress), sub-run\nyoutube/tiktok n\u00e3o produz video_renders \u2192 cobra sem refund. Slice real =\nrender-decoupling (substantivo). Valor de publish \u00e9 OAuth-gated (audits\nsemanas) e o app nem foi registrado (\u00a76 step 1) \u2192 Fila Sovereign afiada\ncom App-registration como STEP 0 (o unlock). Loop pivota p/ pr\u00f3ximo\ndesbloqueado+vis\u00edvel.\n\nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>\" && git log --oneline -1",
  "description": "Commit charter iteration 1 finding"
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
> [90m9:14PM[0m [32mINF[0m 1 commits scanned.
> [90m9:14PM[0m [32mINF[0m scan completed in 8.99ms
> [90m9:14PM[0m [32mINF[0m no leaks found
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.07 seconds)
> ✔️ e2e-output-tripwire (0.01 seconds)
> ✔️ secret-scan (0.03 seconds)
> ✔️ gitleaks-staged (0.06 seconds)
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpost-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m╯[m
> ┃  mesh-reingest ❯ 
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.00 seconds)
> ✔️ mesh-reingest (0.00 seconds)
> 8d59160 docs(loop): charter it.1 — #2 YT/TikTok é false-high (probe material)
> ```

## 🤖 Claude *(00:14:52)*


## 🤖 Claude *(00:14:54)*

`8d59160` selado. **Iteração 1 fechada** com achado material decisivo (não desperdiçou tokens reconstruindo o que já existe).

**Iteração 2 — pivô.** Próximo item desbloqueado + mais alinhado ao Sovereign: **#3 HyperFrames Studio editor** — é o item que o Sovereign explicitamente pediu ("algo que ele abre e toca", memory `feedback_deliver_user_value_not_plumbing`) e é self-hosted (serve a doutrina open-source). Antes de abrir ciclo, verifico o estado real (como fiz no #2). Lendo o blueprint + estado atual da integração:

## 🤖 Claude *(00:14:56)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# HyperFrames Studio → MCORCH Integration Blueprint (deepsearch, 2026-06-24)
> 2	
> 3	> **Founds the VS-UI container build** (Fatia VS-UI / FR-VS-021 Amendment v0.3). Deepsearch material-cited
> 4	> against `github.com/heygen-com/hyperframes` @ commit `ae8b94c51841be8c4b53fe861adae9371db5eff3` (files read
> 5	> via GitHub API), npm registry, and docs. **Law 2 artifact** — read this BEFORE writing the container code.
> 6	> Owner: Sovereign. Next gate after this: BoK amendment of the `/api` adapter surface + Dockerfile + vhost.
> 7	
> 8	## TL;DR (decisive finding)
> 9	
> 10	`@hyperframes/studio`'s `StudioApp` takes **ZERO props**. It is a thin React 19 frontend that on mount discovers a
> 11	**same-origin REST + SSE backend** (`/api/projects`, `/api/projects/:id/files/*`, `/preview/*`, `/render`,
> 12	`/api/render/:jobId/progress`). That backend is the Hono app **`createStudioApi(adapter)`** exported from
> 13	**`@hyperframes/core/studio-api`**, parameterized by a single **`StudioApiAdapter`** interface (HeyGen's deliberate
> 14	DI seam: "each host provides its own adapter").
> 15	
> 16	**MCORCH approach:** do NOT fork the studio UI. **Mount the unmodified `StudioApp`** + implement our own
> 17	**`McorchAdapter`** whose `startRender()` bridges to our proven `video-render` edge fn (engine=hyperframes) instead
> 18	of HeyGen's Puppeteer/FFmpeg producer. No HeyGen cloud on the open-source path. **License: Apache-2.0** (self-host +
> 19	adapt OK; retain notice; don't use HeyGen/HyperFrames branding §6).
> 20	
> 21	## Container architecture (mirrors canvas-design→open-design, but ONE origin)
> 22	
> 23	```
> 24	MCORCH SPA (/dashboard/canvas/video, FR-VS-022) ── iframe ──▶ studio.mcorch.com (CF orange → 127.0.0.1:32xx)
> 25	  Docker container mcorch_video_studio (React 19 host + Hono backend, ONE node process, ONE origin):
> 26	    ├── static: vite build of our minimal host that renders <StudioApp/>
> 27	    └── Hono: app.route("/api", createStudioApi(McorchAdapter)) + serveStatic(dist)
> 28	         McorchAdapter.startRender(opts) → POST <supabase>/functions/v1/video-render
> 29	              { engine:"hyperframes", composition_html: bundle(opts.project.dir), width:1080, height:1920, fps }
> 30	            → poll video-render-poll → map to RenderJobState (progress/stage/status) → studio SSE relays to UI
> 31	         McorchAdapter.{listProjects,resolveProject,files,preview,lint} ← Supabase Storage / container volume
> 32	```
> 33	Frontend uses **relative** `fetch("/api/...")` + `new EventSource("/api/render/:id/progress")` → frontend and `/api`
> 34	**must be same-origin** (the container). MCORCH↔container boundary = iframe (`#project=<id>` via URL hash).
> 35	
> 36	## Q1 Mount
> 37	- Exports incl. `StudioApp` (full editor, **no props**), `NLELayout`, `Player`, `Timeline`, `SourceEditor`,
> 38	  `PropertyPanel`, `FileTree`, `usePlayerStore`, etc. (`packages/studio/src/index.ts`).
> 39	- Self-driving: `useServerConnection()` polls `/api/projects` (2s, `StudioSplash` while waiting), reads `projectId`
> 40	  from URL hash `#project=<id>`. No "pass a composition" path — file/server-backed by design.
> 41	- Minimal host (mirror `src/main.tsx`): `createRoot(#root).render(<StrictMode><StudioApp/></StrictMode>)` +
> 42	  `html,body,#root{height:100%}`. CSS import path = **empirical test** (`npm pack` → inspect dist; styling export is
> 43	  `@hyperframes/studio/tailwind-preset`).
> 44	
> 45	## Q2 Composition format (what our motor renders)
> 46	Plain **HTML + inline CSS + paused GSAP timeline** (no JSON, no React). Stored as **files** in a project dir
> 47	(`meta.json`, `index.html`, `compositions/`, `assets/`). Root: `data-composition-id`/`data-width`/`data-height`
> 48	(9:16 = 1080×1920); clips: `class="clip"` + `data-start`/`data-duration`/`data-track-index`; GSAP timeline
> 49	`{paused:true}` on `window.__timelines`. **No `onChange`/`onSave` prop** — editor persists via `PUT /api/.../files`.
> 50	The artifact our motor consumes = **`adapter.bundle(dir)` → `@hyperframes/core/compiler` `bundleToSingleHtml(dir)`**
> 51	(single 1080×1920 HTML string — exactly what our HTML→MP4 worker eats).
> 52	
> 53	## Q3 Render bridge (the seam)
> 54	Export button → `renderQueue.startRender` → `POST /api/projects/:id/render {fps,quality,format,resolution?,composition?}`
> 55	→ `{jobId}` → SSE `/api/render/:jobId/progress` (`{progress,stage,status,error}`, terminal `complete|failed`). That
> 56	route calls **`adapter.startRender(opts)`** (`opts={project{id,dir,title}, outputPath, format, fps, quality, jobId,
> 57	outputResolution?, composition?}`) which "owns async execution + updates RenderJobState reactively". Reference impl =
> 58	`vite.adapter.ts startRender` (swap its `@hyperframes/producer` call for our edge-fn fetch + poll). **Studio UI needs
> 59	zero changes.** Single billing stays our side (cycle prepaid / `prepaid=true`, OTD-VA-010) — studio never sees mcoCoins.
> 60	
> 61	## Q4 core & player
> 62	- `@hyperframes/core`: parsers + linter + **`/compiler` (bundleToSingleHtml)** + **`/runtime` (seekable IIFE)** +
> 63	  **`/studio-api` (Hono factory + adapter interface)**. `hono` is an **optional** peer (only for `createStudioApi`).
> 64	  **core does NOT render to MP4** — `@hyperframes/engine` (Puppeteer+FFmpeg capture) + `@hyperframes/producer`
> 65	  (pipeline) do; same class as our motor. Keep our motor; use core only for studio-api + compiler + runtime.
> 66	- `@hyperframes/player`: `<hyperframes-player>` web component (playback only).
> 67	
> 68	## Q5 React 19 + container
> 69	- npm `@hyperframes/studio@0.7.5` pins `react:"19"` **exactly** (registry-confirmed) → **separate container + iframe**
> 70	  (this is WHY in-SPA embed was rejected; MCORCH SPA = React 18).
> 71	- Tailwind: `presets:[require('@hyperframes/studio/tailwind-preset')]` or editor renders unstyled (Tailwind 3.4).
> 72	- Dockerfile sketch: `node:22-bookworm-slim` (node>=22), `bun install` (react@19/react-dom@19/zustand@5/
> 73	  @hyperframes/studio/@hyperframes/core/hono/@hono/node-server), `vite build`, `node server.js` (Hono route /api +
> 74	  serveStatic). **If startRender delegates to remote edge fn → NO Chrome/FFmpeg in the container** (lighter than CLI).
> 75	
> 76	## Q6 Auth/embedding
> 77	No HeyGen auth on the embedding path (`createStudioApi` is auth-agnostic; CLI's cloud/auth dirs are off-path). Relative
> 78	fetch/SSE → same-origin container. iframe like canvas-design. Adapter resolves `user_id` from JWT/PAT (Vision-MCP
> 79	pattern); scope Storage per user; verify ownership of hash `projectId`. CF orange SSE needs `proxy_buffering off`
> 80	(reuse `mcp.mcorch.com` vhost recipe).
> 81	
> 82	## Q7 License — Apache-2.0 (Copyright 2026 HeyGen, Inc.). Self-host/modify/distribute OK; retain notices; trademark not licensed.
> 83	
> 84	## Empirical gates before declaring it works (Law 1 — not documented)
> 85	1. **CSS import path** for `StudioApp` (`npm pack` → inspect `dist/`).
> 86	2. **`createStudioApi` exported from published `@hyperframes/core` dist** (it's in src exports `./studio-api`).
> 87	3. **Exact composition attribute names** (docs disagree `#stage` vs `data-composition-id`) — confirm from a real
> 88	   `npx hyperframes init` project.
> 89	4. **⚠️ HIGHEST RISK — render parity:** does our HTML→MP4 worker drive `window.__timelines` with
> 90	   `frame=floor(time*fps)` like core's runtime? If not, motion renders wrong. Consider injecting
> 91	   `@hyperframes/core/runtime` into our motor's headless page so seek semantics match. **Gates engine=hyperframes correctness.**
> 92	5. **Full `/api` surface the adapter must satisfy** — read `core/src/studio-api/routes/*.ts`: mandatory
> 93	   `projects`/`files`/`preview`/`render`; optional (stub) `thumbnail`/`waveform`/`fonts`/`registry`/`storyboard`.
> 94	6. React 19 in separate container — confirm no shared-React conflict through the iframe (shouldn't be — separate origin).
> 95	
> 96	## Risk list
> 97	| # | Risk | Sev | Mitigation |
> 98	|---|------|-----|------------|
> 99	| R1 | Render parity (studio preview ≠ our motor output) | **High** | Gate #4; inject core/runtime into motor's headless page |
> 100	| R2 | Must implement whole `/api` Hono surface, not just render | **High** | Reuse `createStudioApi`; write only `McorchAdapter`; stub optional methods |
> 101	| R3 | React 19 vs MCORCH React 18 | Med (mitigated) | Separate container + iframe (chosen) |
> 102	| R4 | Same-origin relative fetch/SSE | Med | Container serves frontend+/api one origin; CF `proxy_buffering off` |
> 103	| R5 | 0.7.x pre-1.0 API churn | Med | Pin 0.7.5; vendor studio-api types; gate upgrades on parity test |
> 104	| R6 | Studio has no native multi-tenant auth | Med | Adapter resolves user from PAT/JWT; scope Storage; verify projectId ownership |
> 105	| R9 | Studio expects real FS (`dir`); Storage is object store | Med | Materialize project to container volume on resolve, sync back on write |
> 106	
> 107	## Build sequence (next session)
> 108	1. BoK: enumerate the mandatory `/api` route req/resp shapes (`core/studio-api/routes/*.ts`) → amend video-studio SDD with the `McorchAdapter` contract.
> 109	2. `npm pack` empirical gates (#1/#2/#3 above).
> 110	3. Render-parity test (#4) — inject core runtime into our motor OR confirm seek convention.
> 111	4. Container: React 19 host (`<StudioApp/>`) + Hono `createStudioApi(McorchAdapter)` + Dockerfile → run 127.0.0.1.
> 112	5. `McorchAdapter`: files/preview over Supabase Storage; `startRender` → `video-render` edge fn.
> 113	6. Frontend: `/dashboard/canvas/video` iframe page (mirror `CanvasDesignPage`) + route before `canvas/:id`.
> 114	7. vhost `studio.mcorch.com` (**DNS+cert = Sovereign action**, OTD-VS-015) + SSE-tuned proxy.
> 115	8. E2E 1920×1080 gate (Lei 1 Canvas).
> 116	
> 117	**Sources:** github.com/heygen-com/hyperframes @ `ae8b94c5` (studio/core/cli package.json, studio/src/{index,main,App}.tsx, useRenderQueue.ts, useServerConnection.ts, vite.adapter.ts, core/src/studio-api/{index,types,createStudioApi}.ts, LICENSE) · registry.npmjs.org/@hyperframes/studio/latest · hyperframes.heygen.com · hyperframes.mintlify.app/quickstart.
> 118	
> ```

## 🤖 Claude *(00:14:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== McorchAdapter / StudioApiAdapter refs ===\"\ngrep -rn \"McorchAdapter\\|StudioApiAdapter\\|startRender\" src/ 2>/dev/null | head -30\necho \"=== VideoStudioEditorPage exists? ===\"\nls -la src/pages/VideoStudioEditorPage.tsx 2>/dev/null\necho \"=== video-studio.service state ===\"\nsystemctl --user is-active video-studio.service 2>/dev/null || echo \"not active/no user unit\"\necho \"=== video-render edge fn ===\"\nls -la supabase/functions/video-render/ 2>/dev/null\necho \"=== canvas/video route ===\"\ngrep -rn \"canvas/video\\|VideoStudioEditor\" src/App.tsx src/pages/CanvasEditorPage.tsx 2>/dev/null | head",
  "description": "Probe HyperFrames Studio editor integration state"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === McorchAdapter / StudioApiAdapter refs ===
> === VideoStudioEditorPage exists? ===
> -rw-rw-r-- 1 ubuntu ubuntu 1213 Jun 24 20:03 src/pages/VideoStudioEditorPage.tsx
> === video-studio.service state ===
> active
> === video-render edge fn ===
> total 20
> drwxrwxr-x  2 ubuntu ubuntu 4096 Jun 24 00:26 .
> drwxrwxr-x 80 ubuntu ubuntu 4096 Jun 30 16:06 ..
> -rw-rw-r--  1 ubuntu ubuntu 9094 Jun 24 00:26 index.ts
> === canvas/video route ===
> src/App.tsx:50:const VideoStudioEditorPage = lazy(() => import("./pages/VideoStudioEditorPage.tsx"));
> src/App.tsx:135:                <Route path="canvas/video" element={<VideoStudioEditorPage />} />
> ```

## 🤖 Claude *(00:16:09)*


## 🤖 Claude *(00:16:13)*

Now I have #3's real shape. Key facts:
- `VideoStudioEditorPage.tsx` + route `canvas/video` exist; `video-studio.service` is **active** (Fase A live per memory); `video-render` edge fn exists.
- **No `McorchAdapter`/`StudioApiAdapter` yet** (grep empty) — the render-bridge (Fase B) is unbuilt.
- The blueprint is a **marathon**: new React 19 + Hono container, empirical npm-pack gates, render-parity test, and step 7 vhost `studio.mcorch.com` = **Sovereign DNS gate** (OTD-VS-015).

Before committing to that scale, I need the local ground truth: what does the current service actually run (can it already render?), and where does the iframe point? That decides whether #3 is "make render work at all" (high value) vs "reroute billing" (plumbing).

## 🤖 Claude *(00:16:14)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/VideoStudioEditorPage.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { Helmet } from "react-helmet-async";
> 2	
> 3	// HyperFrames Studio editor — module-container pattern (mirrors CanvasDesignPage / design.mcorch.com).
> 4	// The full multi-layer NLE editor (timeline, tracks/layers, alpha-channel video overlays, effects,
> 5	// transitions) is the official `hyperframes preview` server (systemd video-studio.service, host loopback
> 6	// 127.0.0.1:3210), served behind video.mcorch.com (Cloudflare orange + SSO gate). React 19 lives entirely
> 7	// in that standalone process → no conflict with this React 18 SPA. SDD: video-studio Amendment v0.4 (VS-UI).
> 8	export default function VideoStudioEditorPage() {
> 9	  return (
> 10	    <>
> 11	      <Helmet>
> 12	        <title>Editor de Vídeo — MCORCH</title>
> 13	        <meta name="description" content="Editor HyperFrames — composições 9:16 com cenas, camadas, overlays em alpha, efeitos e transições" />
> 14	      </Helmet>
> 15	
> 16	      <div className="w-full h-full bg-background overflow-hidden relative">
> 17	        <iframe
> 18	          src="https://video.mcorch.com"
> 19	          className="w-full h-full bg-black border-none"
> 20	          title="HyperFrames Video Studio"
> 21	          allow="clipboard-read; clipboard-write; fullscreen"
> 22	        />
> 23	      </div>
> 24	    </>
> 25	  );
> 26	}
> 27	
> ```

## 🤖 Claude *(00:16:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== video-studio.service unit ===\"\ncat ~/.config/systemd/user/video-studio.service 2>/dev/null || systemctl --user cat video-studio.service 2>/dev/null | head -40\necho \"\"\necho \"=== what's listening on the studio port ===\"\nss -tlnp 2>/dev/null | grep -E \":3210|:32[0-9][0-9]\" || echo \"no 32xx listener found via ss\"\necho \"=== nginx video vhost ===\"\nls -la nginx/video.mcorch.com.conf 2>/dev/null && grep -nE \"proxy_pass|server_name|location\" nginx/video.mcorch.com.conf 2>/dev/null | head",
  "description": "Read editor page + service unit + vhost"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === video-studio.service unit ===
> [Unit]
> Description=MCORCH HyperFrames Video Studio (hyperframes preview — the multi-layer NLE editor served behind video.mcorch.com; authoring of 9:16 viral compositions with scenes/layers/alpha-overlays/transitions)
> After=network-online.target
> Wants=network-online.target
> StartLimitBurst=5
> StartLimitIntervalSec=60
> 
> [Service]
> # Multi-project root: every project the Sovereign creates lives under here (single-tenant Usuário Zero,
> # OTD-VA-011 multi-tenant hardening deferred). The studio is the official `hyperframes preview` server —
> # a standalone node process (its own React 19 bundle), so NO conflict with the MCORCH SPA (React 18).
> WorkingDirectory=/home/ubuntu/.mcorch/video-studio/projects
> # Explicit node v22 (the shebang's `env node` resolves to /usr/bin/node v18 under systemd; hyperframes needs >=22).
> ExecStart=/home/ubuntu/.local/bin/node /home/ubuntu/.bun/install/global/node_modules/hyperframes/dist/cli.js preview /home/ubuntu/.mcorch/video-studio/projects/mcorch-video --port 3210 --no-open
> Restart=always
> RestartSec=5
> TimeoutStopSec=15
> KillMode=control-group
> # Chrome (Playwright chromium) + ffmpeg already on host (used by render-core.ts) → local render/export works.
> Environment=HOME=/home/ubuntu
> Environment=TMPDIR=/tmp
> Environment=NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
> # hyperframes requires node >=22; /usr/bin/node is v18. Pin v22 (nvm, via the stable ~/.local/bin symlink) FIRST.
> Environment=PATH=/home/ubuntu/.local/bin:/home/ubuntu/.nvm/versions/node/v22.22.3/bin:/home/ubuntu/.bun/bin:/usr/local/bin:/usr/bin:/bin
> 
> [Install]
> WantedBy=default.target
> 
> === what's listening on the studio port ===
> LISTEN 0      511        127.0.0.1:3210       0.0.0.0:*    users:(("node",pid=2089554,fd=22))           
> LISTEN 0      4096       127.0.0.1:3200       0.0.0.0:*                                                 
> === nginx video vhost ===
> -rw-rw-r-- 1 ubuntu ubuntu 4866 Jun 25 16:28 nginx/video.mcorch.com.conf
> 37:  server_name video.mcorch.com;
> 46:  location = /_mcorch_auth {
> 48:    proxy_pass http://127.0.0.1:8787/verify;
> 49:    proxy_pass_request_body off;
> 53:  location @mcorch_login {
> 60:  location / {
> 64:    proxy_pass http://127.0.0.1:3210;
> ```

## 🤖 Claude *(00:16:17)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// video-render — video-studio render submit (FR-VS-001/005/009/014/032). verify_jwt=false (auth in-code).
> 2	// BoK SSOT: docs/bok/video-studio/05-sdd.md §3.1 (UI→Hook→Edge contract) + 04-frd.md (FR-VS-009 charge-at-entry,
> 3	//           FR-VS-011 refund, FR-VS-032 voice consent). SOP: 07-process-flow.md PROC-VS-001/004.
> 4	//
> 5	// CONTRACT (charge-at-entry + refund-on-failure): JWT verify → engine validate → voice-consent gate →
> 6	//   BYOK resolve fail-closed → [dry_run short-circuit] → worker-availability gate → deduct_mco_coins →
> 7	//   INSERT video_renders(queued) via service key → trigger worker → 202 {render_id}. 401/409/402/503 NEVER
> 8	//   charge. A trigger failure AFTER deduct refunds idempotently via finalize_video_render.
> 9	//
> 10	// SLICE 1 (this): the render worker is NOT wired yet (faceless = n8n bridge OTD-VS-001 / hyperframes = sandbox
> 11	//   OTD-VS-006), so the engine-availability gate returns 503 BEFORE any deduct — nobody pays for a render that
> 12	//   cannot run. Everything up to that gate is provable zero-cost (401/422/409/402/dry_run). SLICE 2 sets the
> 13	//   worker webhook env → the prepaid path below activates unchanged.
> 14	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 15	
> 16	const corsHeaders = {
> 17	  "Access-Control-Allow-Origin": "*",
> 18	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 19	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> 20	};
> 21	
> 22	// Mirror of src/lib/billing.ts COIN_COSTS (Deno can't import src/lib — keep in sync; OTD-VS-007 provisional).
> 23	const COST = { faceless: 125, hyperframes: 12 } as const;
> 24	type Engine = keyof typeof COST;
> 25	
> 26	Deno.serve(async (req) => {
> 27	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 28	  const json = (b: unknown, s = 200) =>
> 29	    new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 30	
> 31	  const url = Deno.env.get("SUPABASE_URL")!;
> 32	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 33	  const pubKey = (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!;
> 34	  const admin = createClient(url, serviceKey);
> 35	  const logHealth = (status: string, event?: string) =>
> 36	    admin.from("infra_health_logs").insert({ service: "video-render", status, event }).then(() => {}, () => {});
> 37	
> 38	  try {
> 39	    const authHeader = req.headers.get("Authorization");
> 40	    if (!authHeader?.startsWith("Bearer ")) return json({ error: "Unauthorized" }, 401);
> 41	
> 42	    // Identity: user JWT (this is a user-initiated submit). getUser rejects an invalid/forged token.
> 43	    const userClient = createClient(url, pubKey, { global: { headers: { Authorization: authHeader } } });
> 44	    const { data: { user }, error: authErr } = await userClient.auth.getUser();
> 45	    if (authErr || !user) return json({ error: "Unauthorized" }, 401);
> 46	    const userId = user.id;
> 47	
> 48	    const body = await req.json().catch(() => ({}));
> 49	    const engine = body?.engine as Engine | undefined;
> 50	    if (engine !== "faceless" && engine !== "hyperframes") {
> 51	      return json({ error: "engine_invalid", detail: "engine deve ser 'faceless' ou 'hyperframes'" }, 422);
> 52	    }
> 53	    const dryRun = body?.dry_run === true;
> 54	    const voiceConsent = body?.voice_consent === true;
> 55	    const topic = typeof body?.topic === "string" ? body.topic.slice(0, 500) : null;
> 56	    const productId = typeof body?.product_id === "string" ? body.product_id : null;
> 57	    // HyperFrames render spec (FR-VS-024). The host worker (video-bridge.ts) consumes it. Untrusted props are
> 58	    // sanitized/escaped UPSTREAM (FR-VA-023 / SOP [[autopilot-video-9x16|autopilot-video-9x16]] G1) and rendered via textContent (XSS-safe);
> 59	    // here the spec is only transported into the queued row.
> 60	    const composition = engine === "hyperframes" && body?.composition && typeof body.composition === "object"
> 61	      ? body.composition : null;
> 62	
> 63	    // Voice-consent gate (FR-VS-032): faceless clones a voice (VoxCPM) → identifiable biometric (LGPD Art. 11).
> 64	    if (engine === "faceless" && !voiceConsent) {
> 65	      return json({ error: "voice_consent_required", action: "Confirme o consentimento de uso de voz para gerar o vídeo faceless." }, 409);
> 66	    }
> 67	
> 68	    // BYOK fail-closed (FR-VS-005/006): faceless needs the tenant's Gemini/Google key (director + vision QA). Per-user
> 69	    // first; NO silent global fallback in a user-facing path (API Tenancy Model). hyperframes is deterministic (no AI leg).
> 70	    // The canonical Vault column is `google_api_key` (NOT `gemini_api_key` — the BoK 06 §2.5 / CLAUDE.md naming is
> 71	    // stale; canvas-execute + the live decrypted view use google_api_key, verified 2026-06-22 via 42703 on gemini_api_key).
> 72	    if (engine === "faceless") {
> 73	      const { data: keys } = await admin
> 74	        .from("decrypted_user_api_keys").select("google_api_key").eq("user_id", userId).maybeSingle();
> 75	      if (!keys?.google_api_key) {
> 76	        return json({ error: "gemini_not_configured", action: "Configure sua chave Gemini/Google em /dashboard/settings para gerar vídeo." }, 402);
> 77	      }
> 78	    }
> 79	
> 80	    const cost = COST[engine];
> 81	
> 82	    // dry_run: cost projection WITHOUT deduct or row (zero-cost proof path; mirrors autopilot-run).
> 83	    if (dryRun) return json({ ok: true, dry_run: true, engine, cost_mco: cost });
> 84	
> 85	    // Engine-availability gate (SLICE 1): the worker webhook is unset until slice 2 wires the render engine.
> 86	    // Returning 503 HERE — before any deduct — guarantees no tenant is charged for a render that cannot complete.
> 87	    const workerWebhook = engine === "faceless"
> 88	      ? Deno.env.get("VIDEO_FACELESS_WEBHOOK")
> 89	      : Deno.env.get("VIDEO_HYPERFRAMES_WEBHOOK");
> 90	    if (!workerWebhook) {
> 91	      return json({
> 92	        error: "render_engine_unavailable",
> 93	        detail: `O motor de render '${engine}' entra na Fatia 2 (faceless: ponte de rede + n8n; hyperframes: sandbox). Nenhum mcoCoin foi debitado.`,
> 94	      }, 503);
> 95	    }
> 96	
> 97	    // ── SLICE 2 prepaid path (activates once the worker webhook env is set) ──────────────────────────────────────
> 98	    // Charge-at-entry (FR-VS-009): atomic deduct BEFORE any leg. 402 if balance < cost (zero rows created).
> 99	    const { error: deductErr } = await admin.rpc("deduct_mco_coins", { p_user_id: userId, p_amount: cost });
> 100	    if (deductErr) {
> 101	      logHealth("degraded", "insufficient_balance");
> 102	      return json({ error: "insufficient_balance", detail: `Saldo insuficiente: render '${engine}' custa ${cost} mcoCoins.`, cost_mco: cost }, 402);
> 103	    }
> 104	
> 105	    // INSERT the queued render (service key — RLS denies tenant writes; this is the only writer). org_id/client_id
> 106	    // NULL = solo creator (§AG agency scoping wires in a later slice).
> 107	    const { data: render, error: insErr } = await admin
> 108	      .from("video_renders")
> 109	      .insert({ user_id: userId, engine, topic, product_id: productId, composition, voice_consent: voiceConsent, charged_mco: cost, state: "queued" })
> 110	      .select("id").single();
> 111	    if (insErr || !render) {
> 112	      // Could not even create the ledger row → refund the just-charged cost (no render_id yet → direct credit).
> 113	      await admin.rpc("add_mco_coins", { p_user_id: userId, p_amount: cost }).then(() => {}, () => {});
> 114	      logHealth("error", "insert_failed");
> 115	      return json({ error: "render_create_failed", detail: insErr?.message }, 500);
> 116	    }
> 117	    const renderId = render.id as string;
> 118	
> 119	    // Trigger the worker. Two transports:
> 120	    //   • poll://  → a HOST worker (video-bridge.ts for hyperframes) POLLS video_renders; the queued row IS the
> 121	    //                trigger (Edge fns can't reach a host daemon — the design-bridge lesson). No kick → 202; the
> 122	    //                poller atomically claims (queued→running) and finalizes via finalize_video_render.
> 123	    //   • http(s)  → a reachable webhook (e.g. a faceless external studio); POST the kick, refund on failure.
> 124	    if (!workerWebhook.startsWith("poll://")) {
> 125	      try {
> 126	        const r = await fetch(workerWebhook, {
> 127	          method: "POST",
> 128	          headers: { Authorization: `Bearer ${serviceKey}`, "Content-Type": "application/json" },
> 129	          body: JSON.stringify({ render_id: renderId, user_id: userId, engine, topic, product_id: productId }),
> 130	        });
> 131	        if (!r.ok) throw new Error(`worker HTTP ${r.status}`);
> 132	      } catch (e) {
> 133	        await admin.rpc("finalize_video_render", {
> 134	          p_render_id: renderId, p_state: "failed", p_storage_key: null, p_qa: null, p_node_id: null, p_refund: cost,
> 135	        }).then(() => {}, () => {});
> 136	        logHealth("error", "worker_trigger_failed");
> 137	        return json({ error: "worker_unavailable", detail: e instanceof Error ? e.message : "trigger failed", render_id: renderId }, 502);
> 138	      }
> 139	    }
> 140	
> 141	    logHealth("healthy", "render_submitted");
> 142	    return json({ ok: true, render_id: renderId, engine, charged_mco: cost, state: "queued" }, 202);
> 143	  } catch (e) {
> 144	    logHealth("error", "exception");
> 145	    return json({ error: e instanceof Error ? e.message : "unknown" }, 500);
> 146	  }
> 147	});
> 148	
> ```

## 🤖 Claude *(00:17:31)*


## 🤖 Claude *(00:17:37)*

Now I have #3's ground truth:
- **The editor already works** — `video-studio.service` runs vanilla `hyperframes preview` on `127.0.0.1:3210` behind `video.mcorch.com` (SSO-gated), and **Chrome+ffmpeg on host = local render/export already works** (Fase A = the Sovereign's "abre e toca" is *already satisfied*).
- **`video.mcorch.com` vhost already exists** proxying `127.0.0.1:3210` → the blueprint's `studio.mcorch.com` DNS gate is **avoidable** (reuse the existing vhost by swapping what the service runs).
- **`video-render` edge fn is SLICE 1** — `VIDEO_HYPERFRAMES_WEBHOOK` unset → 503 before deduct (the user-initiated render bridge isn't wired).
- **No `McorchAdapter` yet** — Fase B (turn the borrowed editor into an *owned, integrated MCORCH module* = the exact embodiment of the **newest** open-source/equity doctrine) is the real remaining slice.

Under the newest Sovereign doctrine (open-source-first/equity, today), Fase B is the **highest-alignment** item — and more unblocked than the charter claims (no new DNS needed). The correct first closed-loop step is the **Law-2 gate: BoK amendment of the McorchAdapter `/api` contract**, grounded in empirical verification of the published packages. Checking network egress (the empirical gates need it) + reconciling OTD-SEC status:

## 🤖 Claude *(00:17:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== network egress check (npm registry) ===\"\ncurl -s -m 8 -o /dev/null -w \"npm registry HTTP %{http_code}\\n\" https://registry.npmjs.org/@hyperframes%2Fstudio 2>&1 || echo \"npm unreachable\"\necho \"=== github raw check ===\"\ncurl -s -m 8 -o /dev/null -w \"github HTTP %{http_code}\\n\" https://raw.githubusercontent.com 2>&1 || echo \"gh unreachable\"\necho \"=== hyperframes installed locally? (the service uses it) ===\"\nls /home/ubuntu/.bun/install/global/node_modules/hyperframes/dist/ 2>/dev/null | head; echo \"---core/studio pkgs---\"\nls /home/ubuntu/.bun/install/global/node_modules/@hyperframes/ 2>/dev/null || echo \"no @hyperframes scope in bun global\"\necho \"=== OTD-SEC-007 lefthook/gitleaks config present? ===\"\nls -la lefthook.yml .gitleaks.toml 2>/dev/null; echo \"---\"; ls docs/bok/security/ 2>/dev/null",
  "description": "Check network egress + local hyperframes install + security config"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === network egress check (npm registry) ===
> npm registry HTTP 200
> === github raw check ===
> github HTTP 301
> === hyperframes installed locally? (the service uses it) ===
> beat-analyzer.global.js
> cli.js
> commands
> docker
> docs
> hyperframe.manifest.json
> hyperframe.runtime.iife.js
> hyperframe-runtime.js
> shaderTransitionWorker.js
> skills
> ---core/studio pkgs---
> no @hyperframes scope in bun global
> === OTD-SEC-007 lefthook/gitleaks config present? ===
> -rw-rw-r-- 1 ubuntu ubuntu  977 Jun  9 21:48 .gitleaks.toml
> -rw-rw-r-- 1 ubuntu ubuntu 2148 Jun  9 21:51 lefthook.yml
> ---
> 00-[[deepsearch-blueprint|deepsearch-blueprint]].md
> 01-brd-security.md
> 02-srs-secure-spec.md
> 03-sdd-hardening-architecture.md
> 04-fmea-security.md
> ```

## 🤖 Claude *(00:18:41)*


## 🤖 Claude *(00:18:46)*

Decisive material picture for iteration 2:
- **Network egress works** (npm 200, github 301) → empirical Law-1 gates are runnable.
- The **installed `hyperframes` is the CLI monolith** — the scoped `@hyperframes/studio`/`@hyperframes/core` packages (the blueprint's mount + `createStudioApi` seam) are **NOT installed** → the whole McorchAdapter approach hinges on gates that are genuinely unverified.
- **OTD-SEC-007 is already DONE** (`.gitleaks.toml` + `lefthook.yml` present and running in my last commit) → charter #5 also partly stale.

**Decision:** commit to **#3 Fase B** (highest doctrine-alignment: converts the borrowed editor into an *owned, billable MCORCH module* = equity; unblocked via `video.mcorch.com` reuse). First closed-loop step = the **Law-2 BoK amendment: the McorchAdapter `/api` contract**, grounded in empirical verification of the published packages.

Per ultracode, running this as an adversarial Workflow (verify published packages in isolated dirs → design contract → critic):

## 🤖 Claude *(00:19:47)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'hyperframes-adapter-contract',\n  description: 'Empirically verify published @hyperframes packages + design the McorchAdapter /api contract for the video-studio SDD amendment (Fase B render bridge)',\n  phases: [\n    { title: 'Verify', detail: 'npm-pack the published studio/core packages + read studio-api routes (Law 1 empirical gates)' },\n    { title: 'Design', detail: 'synthesize the McorchAdapter contract + video.mcorch.com-reuse deployment' },\n    { title: 'Critic', detail: 'adversarially refute: missing routes, render-parity, same-origin, regression, tenancy' },\n  ],\n}\n\nconst FINDINGS = {\n  type: 'object',\n  additionalProperties: false,\n  required: ['summary', 'facts', 'unknowns'],\n  properties: {\n    summary: { type: 'string', description: 'one-paragraph verdict' },\n    facts: { type: 'array', items: { type: 'string' }, description: 'each = a material fact with its source (file/path/version/URL). No speculation.' },\n    unknowns: { type: 'array', items: { type: 'string' }, description: 'things that could NOT be verified and why' },\n  },\n}\n\nconst SCRATCH = '/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/7d38a77b-f7f1-4e92-b419-5efbc0e5566c/scratchpad'\n\nphase('Verify')\nconst verify = await parallel([\n  () => agent(\n    `You are verifying the PUBLISHED npm package @hyperframes/studio (target version 0.7.5) as a Law-1 empirical gate for the MCORCH video-studio integration. Work in an ISOLATED dir to avoid races:\\n` +\n    `  mkdir -p ${SCRATCH}/wf-studio && cd ${SCRATCH}/wf-studio\\n` +\n    `  npm pack @hyperframes/studio@0.7.5 2>&1 | tail -3   (this downloads ONLY the tarball, no deps)\\n` +\n    `  tar xzf *.tgz   (extracts to ./package/)\\n` +\n    `Then INSPECT ./package: read package.json (exports map, \"react\"/\"react-dom\" peerDependencies EXACT version, main/module/types, files, styling export like ./tailwind-preset), and inspect dist/ (ls -R dist | head -60; grep -rn \"StudioApp\" dist/*.d.ts or dist/index.* to confirm it is exported and whether it takes props). Confirm empirical gate #1 (CSS/style import path for StudioApp \u2014 is there a css file in dist or a tailwind-preset export?) and gate #6 (react 19 pin). ` +\n    `Report ONLY material facts with the exact file path + version. If npm pack fails, report the exact error in unknowns.`,\n    { label: 'verify:studio-pkg', phase: 'Verify', schema: FINDINGS }\n  ),\n  () => agent(\n    `You are verifying the PUBLISHED npm package @hyperframes/core as a Law-1 empirical gate for the MCORCH video-studio integration. First resolve the version @hyperframes/studio@0.7.5 depends on:\\n` +\n    `  npm view @hyperframes/studio@0.7.5 dependencies 2>&1   (find the @hyperframes/core semver)\\n` +\n    `Then in an ISOLATED dir:\\n` +\n    `  mkdir -p ${SCRATCH}/wf-core && cd ${SCRATCH}/wf-core\\n` +\n    `  npm pack @hyperframes/core@<resolved-version> 2>&1 | tail -3\\n` +\n    `  tar xzf *.tgz\\n` +\n    `INSPECT ./package: read package.json exports map and CONFIRM whether the published dist exports these subpaths (critical \u2014 the whole approach depends on them): \"./studio-api\" (the createStudioApi Hono factory + StudioApiAdapter interface), \"./compiler\" (bundleToSingleHtml), \"./runtime\" (the seekable IIFE). Is \"hono\" an OPTIONAL peer dependency? ` +\n    `Then find the StudioApiAdapter TypeScript interface in the dist .d.ts files (grep -rn \"StudioApiAdapter\\\\|createStudioApi\\\\|startRender\\\\|RenderJobState\" ./package/dist) and enumerate EVERY method the adapter interface declares with its signature. ` +\n    `Report material facts (exact dist path + the interface method list). Anything absent from the published dist \u2192 unknowns (it means the blueprint assumption fails).`,\n    { label: 'verify:core-pkg', phase: 'Verify', schema: FINDINGS }\n  ),\n  () => agent(\n    `You are enumerating the MANDATORY /api route contract of @hyperframes/core studio-api, for the MCORCH McorchAdapter. Use the GitHub source (repo heygen-com/hyperframes) \u2014 fetch the raw files. Try the pinned commit ae8b94c51841be8c4b53fe861adae9371db5eff3 first; if a path 404s, use the default branch (main/master) and note which.\\n` +\n    `Fetch and read these (via WebFetch on raw.githubusercontent.com/heygen-com/hyperframes/<ref>/packages/core/src/studio-api/...):\\n` +\n    `  - createStudioApi.ts (or index.ts) \u2014 the Hono app factory\\n` +\n    `  - types.ts \u2014 StudioApiAdapter interface + RenderJobState + StartRenderOpts shapes\\n` +\n    `  - routes/*.ts \u2014 projects, files, preview, render (the render route calls adapter.startRender; the progress route is SSE)\\n` +\n    `Enumerate: (a) every HTTP route (method + path) the Hono app serves; (b) for each, which adapter method it calls + the request/response JSON shape; (c) the SSE progress event shape ({progress,stage,status,error}); (d) which routes are MANDATORY vs optional/stub-able (thumbnail/waveform/fonts/registry/storyboard). ` +\n    `Also confirm the render seek convention: does core/src/runtime drive window.__timelines with frame = floor(time*fps)? Quote the line. ` +\n    `Report material facts each with the exact GitHub raw URL you read. If a file is unreachable, put it in unknowns with the URL tried.`,\n    { label: 'verify:github-routes', phase: 'Verify', schema: FINDINGS }\n  ),\n])\n\nconst [studioPkg, corePkg, ghRoutes] = verify\n\nphase('Design')\nconst CONTRACT = {\n  type: 'object',\n  additionalProperties: false,\n  required: ['adapter_methods', 'deployment', 'render_bridge', 'render_parity', 'tenancy', 'open_questions'],\n  properties: {\n    adapter_methods: {\n      type: 'array',\n      description: 'one entry per StudioApiAdapter method the contract must implement',\n      items: {\n        type: 'object', additionalProperties: false,\n        required: ['method', 'signature', 'mcorch_impl', 'mandatory'],\n        properties: {\n          method: { type: 'string' },\n          signature: { type: 'string' },\n          mcorch_impl: { type: 'string', description: 'how MCORCH implements it (Supabase Storage FS materialization / video-render bridge / stub)' },\n          mandatory: { type: 'boolean' },\n        },\n      },\n    },\n    deployment: { type: 'string', description: 'how the container runs + whether it reuses video.mcorch.com:3210 (swap video-studio.service) or needs a new vhost; same-origin/SSE handling' },\n    render_bridge: { type: 'string', description: 'startRender \u2192 video-render edge fn mapping: exact request body {engine:hyperframes, composition, ...}, poll strategy, mapping video_renders state \u2192 RenderJobState, single-billing (prepaid) note' },\n    render_parity: { type: 'string', description: 'the frame=floor(time*fps) risk + concrete mitigation vs our render-core.ts/video-bridge.ts motor' },\n    tenancy: { type: 'string', description: 'multi-tenant handling (single-tenant User 0 now? OTD to defer?) + projectId ownership verification' },\n    open_questions: { type: 'array', items: { type: 'string' } },\n  },\n}\nconst contract = await agent(\n  `You are the MCORCH Master Execution Agent (Director of Engineering) designing the McorchAdapter /api contract for the video-studio SDD amendment (Fase B \u2014 turning the embedded HyperFrames editor into an owned, billable MCORCH module).\\n\\n` +\n  `EMPIRICAL VERIFICATION FINDINGS (Law 1 \u2014 treat as ground truth; if a subpath was NOT confirmed in the published dist, design defensively and flag it):\\n` +\n  `--- @hyperframes/studio ---\\n${JSON.stringify(studioPkg)}\\n` +\n  `--- @hyperframes/core ---\\n${JSON.stringify(corePkg)}\\n` +\n  `--- /api routes (GitHub source) ---\\n${JSON.stringify(ghRoutes)}\\n\\n` +\n  `MCORCH CONTEXT (verified in-repo this session):\\n` +\n  `- The editor already runs vanilla: systemd video-studio.service = 'hyperframes preview' on 127.0.0.1:3210, behind vhost nginx/video.mcorch.com.conf (proxy_pass 127.0.0.1:3210, SSO-gated), iframed by src/pages/VideoStudioEditorPage.tsx at route /dashboard/canvas/video. Chrome+ffmpeg on host \u2192 vanilla local render works.\\n` +\n  `- Our render pipeline: edge fn supabase/functions/video-render/index.ts (engine 'hyperframes' cost 12 mco; currently SLICE 1 \u2192 returns 503 until VIDEO_HYPERFRAMES_WEBHOOK set; transport 'poll://' means a host worker polls video_renders). The host worker = scripts/video-bridge.ts (claims video_renders engine=hyperframes \u2192 render via scripts/hyperframes/render-core.ts [Playwright+FFmpeg \u2192 MP4 9:16 1080x1920 sha256-deterministic] \u2192 bucket video-studio-assets \u2192 finalize_video_render). Composition spec is a jsonb column on video_renders (migration 20260624120000).\\n` +\n  `- Doctrine: open-source-first / self-hosted / equity / USD cost = 0. Prefer reusing video.mcorch.com (swap the service to run our React-19 host + Hono createStudioApi(McorchAdapter)) over provisioning a new studio.mcorch.com (avoids a Sovereign DNS gate).\\n` +\n  `- Single billing stays MCORCH-side (video-render deduct_mco_coins / prepaid); the studio UI must NEVER see mcoCoins.\\n\\n` +\n  `Design the COMPLETE McorchAdapter contract: every adapter method (from the verified interface \u2014 list ALL, mark mandatory vs stub), how each maps to Supabase Storage (project dir materialization: object store \u2194 container volume) or the render bridge; the deployment (reuse video.mcorch.com? same-origin SSE with proxy_buffering off); the startRender\u2192video-render mapping (exact request body, poll\u2192RenderJobState); the render-parity mitigation (does our render-core.ts drive window.__timelines with frame=floor(time*fps)? \u2014 READ scripts/hyperframes/render-core.ts to check and state the concrete fix); tenancy (single-tenant User 0 now, OTD to defer multi-tenant). Be concrete and buildable \u2014 this is the SSOT for the container code.`,\n  { label: 'design:mcorch-adapter', phase: 'Design', schema: CONTRACT }\n)\n\nphase('Critic')\nconst VERDICT = {\n  type: 'object', additionalProperties: false,\n  required: ['verdict', 'blocking_gaps', 'nonblocking_notes'],\n  properties: {\n    verdict: { type: 'string', enum: ['APPROVE', 'APPROVE_WITH_FIXES', 'REJECT'] },\n    blocking_gaps: {\n      type: 'array',\n      description: 'gaps that MUST be fixed before container code begins',\n      items: {\n        type: 'object', additionalProperties: false,\n        required: ['gap', 'why', 'fix'],\n        properties: { gap: { type: 'string' }, why: { type: 'string' }, fix: { type: 'string' } },\n      },\n    },\n    nonblocking_notes: { type: 'array', items: { type: 'string' } },\n  },\n}\nconst critic = await agent(\n  `You are an adversarial reviewer. Try to REFUTE the readiness of this McorchAdapter contract for the MCORCH video-studio Fase B build. Default to finding gaps.\\n\\n` +\n  `CONTRACT:\\n${JSON.stringify(contract)}\\n\\n` +\n  `EMPIRICAL FINDINGS the contract rests on:\\n${JSON.stringify({ studioPkg, corePkg, ghRoutes })}\\n\\n` +\n  `Attack these specifically, each with evidence:\\n` +\n  `1. COMPLETENESS: is any MANDATORY /api route (from ghRoutes) missing an adapter method in the contract? A missing mandatory route = the studio UI breaks on mount.\\n` +\n  `2. RENDER PARITY (highest risk): READ scripts/hyperframes/render-core.ts and scripts/hyperframes/templates/viral-short-9x16.html in the repo. Does our motor actually drive the composition timeline with frame=floor(time*fps) seek semantics matching @hyperframes/core/runtime? If our motor renders its OWN template (not the studio's bundleToSingleHtml output), then editor-preview \u2260 rendered-MP4 \u2014 a SILENT correctness bug. State whether the contract's render_bridge feeds the studio's bundled HTML to our motor or renders a different template.\\n` +\n  `3. SAME-ORIGIN/SSE: relative fetch + EventSource require frontend and /api on ONE origin. Does the deployment actually put both on 127.0.0.1:3210 behind video.mcorch.com? Does the vhost pass SSE (proxy_buffering off)? Read nginx/video.mcorch.com.conf.\\n` +\n  `4. REGRESSION: swapping video-studio.service from vanilla 'hyperframes preview' to our host \u2014 does that break the currently-working editor if the container build fails? Is there a rollback?\\n` +\n  `5. PUBLISHED-DIST RISK: if corePkg findings did NOT confirm ./studio-api is exported from the PUBLISHED dist (only from GitHub src), the entire mount approach may be unbuildable from npm \u2014 is that flagged as a blocking gap?\\n` +\n  `6. TENANCY/STORAGE: the FS materialization (Supabase Storage \u2194 container volume) \u2014 any lost-write / concurrent-edit / cleanup gap?\\n` +\n  `Return APPROVE only if zero blocking gaps. Each blocking gap needs a concrete fix.`,\n  { label: 'critic:adversarial', phase: 'Critic', schema: VERDICT }\n)\n\nreturn { studioPkg, corePkg, ghRoutes, contract, critic }"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wf51jmqvw
> Summary: Empirically verify published @hyperframes packages + design the McorchAdapter /api contract for the video-studio SDD amendment (Fase B render bridge)
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/7d38a77b-f7f1-4e92-b419-5efbc0e5566c/subagents/workflows/wf_b0a6c005-8c2
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/7d38a77b-f7f1-4e92-b419-5efbc0e5566c/workflows/scripts/hyperframes-adapter-contract-wf_b0a6c005-8c2.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/7d38a77b-f7f1-4e92-b419-5efbc0e5566c/workflows/scripts/hyperframes-adapter-contract-wf_b0a6c005-8c2.js"} to iterate without resending the script.)
> Run ID: wf_b0a6c005-8c2
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/7d38a77b-f7f1-4e92-b419-5efbc0e5566c/workflows/scripts/hyperframes-adapter-contract-wf_b0a6c005-8c2.js", resumeFromRunId: "wf_b0a6c005-8c2"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(00:19:54)*


## 🤖 Claude *(00:20:00)*

**Iteração 2 em execução.** Workflow adversarial lançado (`wf_b0a6c005-8c2`): verifica empiricamente os pacotes `@hyperframes/studio`/`@hyperframes/core` publicados (npm pack + fonte GitHub das rotas `/api`) → desenha o contrato do `McorchAdapter` → critic adversarial (paridade de render, same-origin/SSE, regressão, dist publicado). Deliverable = base material para a **emenda BoK** (gate Lei 2 antes do código do container).

**Modo dinâmico:**
- Rodei a tarefa agora (Workflow em background — me re-invoca ao completar).
- Sinal primário = conclusão do Workflow. Agendo fallback longo caso trave.

Quando voltar: autoro a emenda `video-studio` SDD (McorchAdapter + deploy via reuso do `video.mcorch.com`), commito o gate Lei 2, e sigo para o scaffold do container na próxima iteração.

## 🤖 Claude *(00:20:06)*


🛠️ **Tool Call**: `ScheduleWakeup`
```json
{
  "delaySeconds": 1500,
  "reason": "Fallback enquanto o Workflow verify+design+critic do McorchAdapter roda; a conclus\u00e3o do Workflow \u00e9 o sinal prim\u00e1rio de retomada.",
  "prompt": "/loop Voc\u00ea \u00e9 o MCORCH Master Execution Agent em MALHA FECHADA AUT\u00d4NOMA. Leia .claude/context/autonomous-loop-charter.md (fonte da verdade do estado) + git fetch + Pending Actions do HANDOFF.md, e CONTINUE de onde a charter est\u00e1. A cada itera\u00e7\u00e3o: (1) escolha o item de MAIOR valor DESBLOQUEADO no backlog; (2) ciclo fechado \u2014 BoK Gate \u2192 SOP Lei 2 \u2192 c\u00f3digo \u2192 prova material Lei 1 \u2192 /security-review se houver migration \u2192 commit granular (Workflow p/ tarefas substantivas); (3) ao bater em port\u00e3o Sovereign (biometria/DNS/OAuth/GO/decis\u00e3o), N\u00c3O improvise \u2014 registre na Fila de A\u00e7\u00e3o Sovereign e pule; (4) Survival self-audit; (5) /handoff incremental ao fechar Fatia; selo final + PARE quando janela ~95% OU backlog desbloqueado vazio OU GO/stop. Reporte em PT-BR cada itera\u00e7\u00e3o."
}
```

> **Tool Result (ScheduleWakeup)** - ✅ Success
>
> ```
> Next wakeup scheduled for 21:46:00 (in 1554s). Nothing more to do this turn — the harness re-invokes you when the wakeup fires or a task-notification arrives.
> ```

## 🤖 Claude *(00:20:11)*

**Iteração 2 em andamento** — Workflow do contrato McorchAdapter rodando em background. Aguardando conclusão para autorar a emenda BoK (gate Lei 2) e commitar. Reporto assim que voltar.

**Resumo do progresso do loop até aqui:**
- **it.1 ✅** (`8d59160`): #2 YT/TikTok provado *false-high* — charter corrigida, trap de billing documentado, Fila Sovereign afiada (app-registration = o unlock).
- **it.2 🔄**: pivô para #3 Fase B (editor HyperFrames como módulo próprio = doutrina equity) — Workflow verify+design+critic do McorchAdapter em execução.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-01 - Configurar loop autônomo e definir fila soberana]]
> * **Próxima Sessão**: [[2026-07-01 - Usar comando loop para continuar sequência lógica]]
%% --- TIMELINE END --- %%

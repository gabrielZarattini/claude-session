# Usar comando /loop para continuar sequência lógica
**Date:** 2026-06-30 | **Session ID:** `229e84c1-28e5-4039-822d-8abc44633657`

---

## 👤 User *(22:41:53)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(22:41:53)*

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


## 🤖 Claude *(22:41:59)*


## 🤖 Claude *(22:41:59)*

I'll execute the ShakeHands /handson pick-up ritual. Starting with the pre-flight checks in parallel.

## 🤖 Claude *(22:42:00)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git fetch --quiet 2>&1 | tail -3; echo \"---LOG---\"; git log --oneline -7; echo \"---STATUS---\"; git status --short; echo \"---DIFFSTAT---\"; git diff HEAD --stat",
  "description": "Git fetch + recent history, status, diff scope"
}
```

## 🤖 Claude *(22:42:01)*


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
> ---LOG---
> 16e42f1 chore(handoff): proof-manifest → c138539f (Fatia 2 + 3a seal)
> 0f4f5ea docs(handoff): seal Gabriel AI Fatia 2 (Voice Clone) + Fatia 3a (Consent+Erasure LGPD) — mesh 8996
> 7913546 docs(readme): v6.61.0 — Avatar Voice Clone (Fatia 2) + Consent/Erasure (Fatia 3a) — mesh 8996
> 941607d docs(bok): avatar-clone-ai blueprint — YouTube account-config execution log
> cc5afc3 test(avatar-clone-ai): consent+erase zero-cost smoke (11 gates, Fatia 3a)
> c09c222 feat(avatar-clone-ai): consent wizard + erasure UI in VoiceClone inspector (Fatia 3a)
> fabf7ae feat(avatar-clone-ai): avatar-consent + erase-avatar-artifacts edge fns + consent gate (Fatia 3a)
> ---STATUS---
> ---DIFFSTAT---
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> (Bash completed with no output)
> ```

## 🤖 Claude *(22:42:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"; echo \"---CHROMA---\"; curl -s --max-time 5 http://localhost:8001/api/v2/heartbeat || echo \"CHROMA-UNREACHABLE\"",
  "description": "Docker mesh + Chroma health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 29 hours (healthy)
> mcorch_claude_mem: Up 2 weeks (healthy)
> mcorch_chroma: Up 2 weeks (healthy)
> ---
> mega-brain-dashboard: Up 2 weeks
> mega-brain-webhook: Up 2 weeks (healthy)
> mega-brain-daemon: Up 2 weeks (healthy)
> ---CHROMA---
> {"nanosecond heartbeat":1782859323833119300}
> ```

## 🤖 Claude *(22:42:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"---BOK---\"; ls docs/bok/ 2>/dev/null; echo \"---HANDOFF-LINES---\"; wc -l HANDOFF.md; echo \"---SCRATCH---\"; ls scratch/ 2>/dev/null && echo \"WARN scratch has files\" || echo \"scratch clean\"",
  "description": "BoK suites, HANDOFF line count, scratch check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ---BOK---
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
> ---HANDOFF-LINES---
> 8847 HANDOFF.md
> ---SCRATCH---
> WARN scratch has files
> ```

## 🤖 Claude *(22:42:08)*


## 🤖 Claude *(22:42:09)*

Now reading HANDOFF (head + tail via read-from-end), sprint-priorities, and running the BoK gate check + scratch contents.

## 🤖 Claude *(22:42:10)*


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
> 14	## Session Seal — Gabriel AI: Fatia 2 (Clone de Voz) + Fatia 3a (Consentimento + Erasure LGPD) (2026-06-30)
> 15	
> 16	Sessão iniciada por `/handson` sob **ultracode**. Diretiva Sovereign: continuar o programa **Gabriel AI** (`avatar-clone-ai`) — BoK 10/10 já selada (gate ABERTO). Entregues duas fatias completas, verificadas em todas as camadas (DB · edge · smoke · `/security-review` · build · browser · Vision QA), e levantado honestamente o gate da Fatia 3b.
> 17	
> 18	**Arco 1 — Fatia 2 (Clone de Voz):** nó `voiceClone` no Canvas Studio existente (reuse-first, 6º node type) + edge fn `generate-voice` net-new (paralelo a `generate-image`): ações `clone`+`synthesize`, **ElevenLabs IVC/`eleven_multilingual_v2` + Cartesia `sonic-3.5` BYOK per-user fail-closed (402)**, **guard de code-switching** (FM-AC-013: gate-duro `profile.language===request.language` + heurística `detectCodeSwitch` espelhada client/edge), sentinel, débito atômico 36 mco **depois** dos gates + refund-on-fail, telemetria `service='avatar-clone-ai'` em todo path. Migration `20260630120000`: `voice_profiles` (RLS own, voiceprint cifrado no Vault) + RPCs `store/resolve_voice_profile` (SECURITY DEFINER service-role tenant-guarded) + `creative_assets.source_module += 'avatar-studio'`. Achado material: `elevenlabs`/`cartesia` keys **já existiam** no BYOK (Fatia 1) → zero migration de chave.
> 19	
> 20	**Arco 2 — Fatia 3a (Consentimento + Erasure):** backbone LGPD Art. 11/18. Migration `20260630130000`: `avatar_identities` (RLS own, embedding/HNSW, `arcface_threshold`/`identity_storage_key` staged-nullable p/ 3b) + `avatar_consents` **imutável** (trigger: só `revoked_at` muda) + `erase_avatar_artifacts` (SECURITY DEFINER, guard de tenant por linha, **revoga voiceprint no Vault in-RPC**, devolve `storage_keys`). Edge fns `avatar-consent` (grant, IP server-capturado, INSERT service-role) + `erase-avatar-artifacts` (Art. 18: RPC-como-user tenant-guarded + Storage API delete + atestado telemetria). **ConsentWizard** (3 checkboxes separados + atestado de titularidade, FR-AC-030) trava o "Clonar voz" até consent ativo; "Apagar dados de voz" (Art. 18). A `generate-voice` ganhou o **gate de consent** (clone exige consent ativo; síntese fail-closes em revogação total) — **sem regressão** no smoke da Fatia 2.
> 21	
> 22	**Fatia 3b (avatarIdentity + Identity Gate) — GATED (Lei 1, honesto):** probe de viabilidade provou ArcFace/InsightFace **ausente** no código; a BoK (FR-AC-013/014) exige ArcFace calibrado em **frames reais do Gabriel**; treino Soul ID exige plano pago Higgsfield + as fotos do Sovereign. Requer **emenda BoK** (ArcFace→VLM-soft MVP via Vision MCP, ou provisionar credencial face-verify — AWS Rekognition/Azure/Face++) + dados biométricos do Sovereign. NÃO improvisado (Closed-Loop Protocol).
> 23	
> 24	| Action | Result |
> 25	|--------|--------|
> 26	| `supabase/functions/generate-voice/` (NET-NEW) + `config.toml` | ✅ clone+synthesize BYOK fail-closed + code-switch guard + consent gate + refund · deployed 140kB ACTIVE |
> 27	| `supabase/migrations/20260630120000_*.sql` | ✅ `voice_profiles` RLS-own Vault + RPCs tenant-guarded + `creative_assets` avatar-studio (HTTP 201, verificado) |
> 28	| `supabase/migrations/20260630130000_*.sql` | ✅ `avatar_identities`+`avatar_consents` imutável + `erase_avatar_artifacts` (HTTP 201, verificado: 2 tabelas RLS · 2 policies · RPC · trigger · HNSW) |
> 29	| `supabase/functions/{avatar-consent,erase-avatar-artifacts}/` | ✅ deployadas ACTIVE (grant IP-server + erasure Art.18) |
> 30	| `src/components/canvas/nodes/VoiceCloneNode.tsx` + `inspectors/VoiceCloneInspector.tsx` | ✅ nó + inspector (upload→consent→clone→synth→playback + erase) |
> 31	| `src/components/avatar/ConsentWizard.tsx` + `src/hooks/{useAvatarVoice,useAvatarConsent,useAvatarErasure}.ts` | ✅ wizard 3-checkbox + hooks Harness |
> 32	| `src/types/canvas.ts` · `src/lib/{avatar,billing,canvas-node-registry}.ts` · `src/integrations/supabase/types.ts` | ✅ VoiceCloneData/factory/guard + VOICE 36 + detectCodeSwitch + types regen (additive) |
> 33	| `scripts/qa/smoke-generate-voice.ts` (10) + `smoke-avatar-consent-erase.ts` (11) | ✅ **21 gates zero-cost** verdes (live edge fns) |
> 34	| `docs/processes/avatar-{voice-credential-resolution,biometric-retention-erasure}.md` | ✅ 2 SOPs Lei 2 (antes do código) |
> 35	| `tsc --noEmit` / `bun run test` / `/security-review` ×2 | ✅ 0 erros · **303 passed** · NO FINDINGS ×2 |
> 36	| Browser-verify (logado) + Vision QA | ✅ nó "Clone de Voz" renderiza + inspector íntegro (cost 0, high) |
> 37	
> 38	| Commit | Conteúdo |
> 39	|--------|----------|
> 40	| `d6515e9` | docs: SOP credential-resolution voz (Lei 2) |
> 41	| `e3fc4d6` | feat: voice_profiles + store/resolve RPCs + creative_assets avatar-studio |
> 42	| `957dd97` | feat: generate-voice edge fn (BYOK clone+synthesize + code-switch) |
> 43	| `e9ebc1e` | feat: voiceClone Canvas node + inspector + useAvatarVoice |
> 44	| `984fb22` | test: code-switch unit (8) + generate-voice smoke (10) |
> 45	| `4f6d1c5` | docs: SOP consent+retention+erasure (Lei 2) |
> 46	| `2d371b3` | feat: avatar_identities + avatar_consents + erase RPC |
> 47	| `fabf7ae` | feat: avatar-consent + erase-avatar-artifacts edge fns + consent gate |
> 48	| `c09c222` | feat: consent wizard + erasure UI no VoiceClone inspector |
> 49	| `cc5afc3` | test: consent+erase smoke (11 gates) |
> 50	| `941607d` | docs(bok): blueprint YouTube account-config execution log (Cowork paralelo) |
> 51	| `7913546` | docs(readme): v6.61.0 — mesh 8996 |
> 52	
> 53	Handoff node `c138539f-0365-436a-ad56-c65e013793c6` inserido + embedado (768d). Milestone Fatia 2 `b51d8de6`. Mesh **8996 nós**.
> 54	
> 55	### Arquitetura Fatia 2/3a (Voz + Consent)
> 56	```
> 57	Canvas Studio (reuse) → nó voiceClone → VoiceCloneInspector
> 58	   │ (sem consent voice_clone) → ConsentWizard (3 checkboxes, FR-AC-030) → avatar-consent fn (IP server) → avatar_consents (imutável)
> 59	   │ (consent ativo) → upload amostra (canvas-assets) → useAvatarVoice.clone → generate-voice(action=clone)
> 60	   │      BYOK 402 → consent 403 → IVC provider → store_voice_profile (voiceprint→Vault) → voice_profiles
> 61	   │ → useAvatarVoice.synthesize → generate-voice(action=synthesize)
> 62	   │      resolve_voice_profile (tenant-guard) → 422 lang/code-switch → sentinel → BYOK → consent-revoked 403
> 63	   │      → deduct 36 (atômico) → TTS → bucket video-studio-assets → register_creative_asset(audio,avatar-studio) → signed URL
> 64	   └ "Apagar dados de voz" → useAvatarErasure → erase-avatar-artifacts (RPC-como-user tenant-guard
> 65	          → erase_avatar_artifacts: DELETE voice_profiles + revoga voiceprint Vault in-RPC → Storage API delete → atestado)
> 66	```
> 67	
> 68	## Session Seal — Programa "Gabriel AI": BoK avatar-clone-ai + Fatia 1 BYOK + Spaces Phase 0 + Kanban vivo (2026-06-30)
> 69	
> 70	Sessão-maratona iniciada por `/handson`, sob **ultracode** (orquestração via Workflow). Da diretiva Sovereign "criar estratégias de conteúdo + cadência 30d + avatar treinado fiel à minha pessoa/voz" até **código verificado em produção**, mais duas tarefas encadeadas (Spaces Phase 0 + Kanban detalhado/vivo).
> 71	
> ```

## 🤖 Claude *(22:42:11)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 8447,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 8447	    └── DropdownMenu → "Monetizar Links ML"
> 8448	          → handleMonetizeLinks(item):
> 8449	               match(ML_URL_RE) → unique URLs
> 8450	               for url of unique:
> 8451	                 POST process-affiliate-link → affiliate_url
> 8452	                 body.split(url).join(affiliate_url)
> 8453	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 8454	          → Badge 💰 ML (emerald) exibido após monetização
> 8455	```
> 8456	
> 8457	---
> 8458	
> 8459	## Pending Actions (Commercial Launch)
> 8460	
> 8461	### CRITICAL — Must complete before first client
> 8462	
> 8463	🎯. **[✅ ATIVADO + VÍDEO 9:16 AUTÔNOMO — 2026-06-24 · pendente só: editor Studio (módulo-container) + postback ML + publish vertical] Viral Autopilot** — BoK 9/9 selada (`b3398294`). **✅ VÍDEO 9:16 (seal video-9x16-motor-and-autopilot, 2026-06-24):** (C) **RESOLVIDO** — motor HyperFrames determinístico VIVO (Fatia VS-2: `video-bridge.service` render 1080×1920 sha256-idêntico) + integração Autopilot (Fatia VA-V1: `orchestrate-step` enfileira render do ângulo viral REAL, custo no pré-débito do ciclo OTD-VA-010, attach content_library+creative_metrics OTD-VA-014) — provado E2E real (artigo Roborock → render 9:16 → biblioteca, saldo intacto prepaid). BoK Amendment v0.2 (FR-VA-022..026 + SOP `autopilot-video-9x16.md`) + flip OTD-VS-005 A→C (editor = módulo-container open-design, embed in-SPA inviável por React 19/18). `/security-review` SAFE ×2. **Próximo do vídeo:** **editor HyperFrames Studio** (módulo-container: deepsearch da API `@hyperframes/studio` → app React 19 → bridge → módulo frontend → vhost `studio.mcorch.com` [DNS Sovereign]) + **1º ciclo pago de vídeo witnessed** (habilitar `video_enabled` + GO) + (D) postback ML real + publish vertical TikTok/IG/YT (PR-VA-021, OAuth+App Review). **— histórico v6.48.0:** **✅ ATIVAÇÃO (seal autopilot-activation-security-hardening):** (A) heartbeat pg_cron `autopilot-cadence */15` jobid 3 `active` (migration `20260623040000`) + **1º ciclo PAGO real** `947ef8b5` (débito 22/refund 2, saldo 5096→5076) DONE; (B) **FR-VA-018** trend-informed angle com gate de fonte `sanitizeTrendTitle` + paridade pt-BR no sentinel (OTD-VA-018) DONE. Restam só (C) mídia 9:16 + (D) postback ML real. **Motor autônomo R1+R2+R3+R4 COMPLETO e provado zero-cost.** ✅ **Fatia 2 (cadência R2 + loop R3 + UI, commits `686bae3`→`bfd178b`):** SOP Lei 2 `autopilot-cron-identity.md` (OTD-VA-008 fechado) · migrations `20260620120000..120300` (`autopilot_plans`/`autopilot_cycles` FK composta tenant + RPCs `begin`/`finalize_autopilot_cycle` atômicos sob advisory-lock, service-role-only) · 6 edge fns deployadas (`autopilot-run` executor + `-cadence-cron` driver pg_cron + `-analyze` FR-VA-010 + `-collect` FR-VA-008 + `orchestrate-content` FR-VA-016 prepaid + `orchestrate-step` FR-VA-011 inject) · UI `/dashboard/autopilot` (`useAutopilot`+`AutopilotPage`). `/security-review` SAFE 3× · 3 smokes zero-cost (31 gates) · render ocular. **PENDENTE:** **(A)** ⚠️ **ação Sovereign** — ativar o **`pg_cron` schedule** que chama `autopilot-cadence-cron` (a função existe+provada; só o JOB pg_cron é ativação Sovereign-side, `Bearer SB_SECRET_KEY` via Vault) + rodar o **1º ciclo PAGO real** (mco real), gated nos 2 blockers de saída visível diagnosticados na Fatia 1b: **CF WAF skip `/wp-json/*`** + **OpenAI image model access**; **(B)** `fetch-trends`/`vm_trends`→pauta do ângulo viral (FR-VA-018, último item autônomo); **(C)** mídia viral 9:16 + TikTok/IG/YT (fase 2); **(D)** provar postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER). Constraints chave (cravados no código): `N_runs=prod×rede×ab_variants`, imagem no bundle de 10, refund crédito-positivo (NUNCA deduct negativo — anti-mint `20260603220000:45`), FK composta tenant-escopada, analyze inline=prepaid (reserva de 2 só vira actual com dado real).
> 8464	
> 8465	🌌. **[EM ANDAMENTO — Phase Epsilon V9] Unified Sensorial Canvas — Fases 3.5-3.10** — Fases 3.1-3.4 ✅ (scaffold rota/store/shell 72-28 + Code Network R3F InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; E2E ocular nos 3 modos; commits `210b90d`/`d832084`/`4940b4d`/`38d9760`/`769acb1`). **Restam:** **3.5** Sinapses inter-rede (arestas **REAIS** de `mcorch_edges` cruzando código↔memória, lit só no modo Universo — nunca fabricar) · **3.6** fly-to (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.7** layout/perf (`OTD-UCANVAS-PERF` — a query do código leva **~30s** com 2 canvases; considerar Louvain em Web Worker / streaming do grafo / lazy do backdrop) · **3.8** executar a poda do squad-coloring (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`. BoK selada (PR-025 · FR-043..049 · NFR-023/024 · SDD §9). **3 páginas legadas (matrix/memory/core-fable) preservadas como backup até 3.9.**
> 8466	
> 8467	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 8468	
> 8469	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 8470	
> 8471	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 8472	
> 8473	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 8474	
> 8475	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 8476	
> 8477	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 8478	
> 8479	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 8480	
> 8481	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 8482	
> 8483	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 8484	
> 8485	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 8486	   ```bash
> 8487	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 8488	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 8489	   ```
> 8490	
> 8491	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 8492	
> 8493	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 8494	
> 8495	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 8496	
> 8497	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 8498	
> 8499	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 8500	
> 8501	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 8502	
> 8503	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 8504	
> 8505	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 8506	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 8507	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 8508	
> 8509	### SOCIAL — Next steps
> 8510	
> 8511	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 8512	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 8513	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 8514	
> 8515	### NON-CRITICAL
> 8516	
> 8517	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 8518	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 8519	- `browserslist` — ✅ updated (2026-04-26)
> 8520	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 8521	
> 8522	### GITNEXUS MCP — Next steps
> 8523	
> 8524	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 8525	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 8526	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 8527	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 8528	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 8529	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 8530	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 8531	
> 8532	### PHASE EPSILON — Next iterations
> 8533	
> 8534	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 8535	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 8536	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 8537	
> 8538	### CORE — Next iterations
> 8539	
> 8540	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 8541	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 8542	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 8543	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 8544	
> 8545	### PHASE DELTA — Next iterations
> 8546	
> 8547	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 8548	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 8549	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 8550	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 8551	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 8552	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 8553	
> 8554	### USUÁRIO ZERO — Checklist de validação
> 8555	
> 8556	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 8557	- ✅ Stripe sandbox secrets no vault
> 8558	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 8559	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 8560	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 8561	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 8562	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 8563	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 8564	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 8565	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 8566	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 8567	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 8568	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 8569	
> 8570	---
> 8571	
> 8572	## Infrastructure
> 8573	
> 8574	| Service | Container | Port | Status |
> 8575	|---------|-----------|------|--------|
> 8576	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 8577	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 8578	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 8579	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 8580	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 8581	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 8582	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 8583	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 8584	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 8585	
> 8586	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 8587	
> 8588	```bash
> 8589	docker compose up -d
> 8590	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 8591	```
> 8592	
> 8593	---
> 8594	
> 8595	## Security Model (Post-Go-Live)
> 8596	
> 8597	| Table | Isolation |
> 8598	|-------|-----------|
> 8599	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 8600	| `mcorch_edges` | Same pattern |
> 8601	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 8602	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 8603	
> 8604	---
> 8605	
> 8606	## Billing Architecture
> 8607	
> 8608	| Decision | Value |
> 8609	|----------|-------|
> 8610	| Canonical billing ledger | `profiles.mco_balance` |
> 8611	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 8612	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 8613	| Orchestration cost | 10 mcoCoins/run |
> 8614	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 8615	| Stripe | Sandbox keys active — swap to live before first client |
> 8616	
> 8617	---
> 8618	
> 8619	## GraphRAG State
> 8620	
> 8621	- **8996 total nodes** (verificado live 2026-06-30 via REST count=exact, avatar-fatia2-voice-fatia3a-consent-erase seal: +handoff `c138539f-0365-436a-ad56-c65e013793c6` embedded 768d + milestone Fatia 2 `b51d8de6-e574-42aa-93b7-8fd75d85a717` — Gabriel AI **Fatia 2 (Clone de Voz)** [nó voiceClone + edge `generate-voice` BYOK ElevenLabs/Cartesia fail-closed + code-switch guard FM-AC-013 + voice_profiles RLS-own Vault + RPCs tenant-guarded; migration `20260630120000`; smoke 10/10; browser+VisionQA PASS] + **Fatia 3a (Consent+Erasure LGPD Art.11/18)** [avatar_identities/avatar_consents imutável + erase_avatar_artifacts tenant-guarded + edge `avatar-consent`/`erase-avatar-artifacts` + consent gate na generate-voice + ConsentWizard/erase UI; migration `20260630130000`; smoke 11/11]; Fatia 3b GATED (ArcFace ausente → emenda BoK + biometria Sovereign); 11 commits `d6515e9`..`7913546`; `/security-review` NO FINDINGS ×2; prev 8993)
> 8622	- **8993 total nodes** (verificado live 2026-06-30 via REST count=exact, gabriel-ai-fatia1-spaces-p0-kanban-live seal: +handoff `aba1458e-2df1-4813-a71b-34360bf7417e` embedded 768d — Programa Gabriel AI [deepsearch força-total → BoK `avatar-clone-ai` 10/10 selada nó `ee81987d` GO-HYBRID + Fatia 1 BYOK hedra/cartesia/fal] + Spaces canvas Phase 0 (scaffold promovido) + Kanban painel-de-detalhe + reconciliador vivo não-destrutivo + cron */15; 6 commits `a5814d2`..`71f4c47`; prev 8992 = BoK seal `ee81987d` `documentation_suite` avatar-clone-ai DERIVES_FROM video-studio `c99b7875`)
> 8623	- **8991 total nodes** (verificado live 2026-06-29 via REST count=exact, product-miner-vision-reliability-async seal: +handoff `1c100e2a-34f4-4b0a-a324-d89cba7ab0a8` embedded 768d — reparo de confiabilidade do Minerador (Vision MCP): Gemini Files API 20-100MB + cover-image fallback (rejeita stub <50KB) + `shouldDownloadVideos:true` vídeo rico em todo vídeo + `:free` 429→pago BYOK + síntese audience-fit/confidence/parser tolerante + extração ASSÍNCRONA timeout-proof [`vm_miner_jobs` RLS-owner/realtime + action `mine-async` EdgeRuntime.waitUntil + hook `useMinerJob` Realtime+polling + barra de progresso + notificação]; 10 commits prod-live; prev 8982 verificado live 2026-06-28 via REST count=exact, privacy-policy-google-oauth-compliance seal: +handoff `d5476bb8-c5ea-4dc4-a3c0-86d1e0895456` embedded 768d — política de privacidade endurecida p/ verificação Google OAuth: cláusula treino-IA Limited Use + §6 revogação/exclusão de tokens + §8 aviso de alterações + §5 segurança concreta [criptografia trânsito/repouso]; grounded na política Google + revisão adversarial 4/4; deployed login.mcorch.com/privacy + render browser-verificado; prev 8973 verificado live 2026-06-27 via REST count=exact, social-connect-tiktok-youtube-pinterest seal: +handoff `311a55b1-fb7b-410f-9582-625fb4721619` embedded 768d — conectar redes TikTok/YouTube/Pinterest: gate BoK post-engine + migration social_app_config Vault-cifrada aplicada/provada + helper fail-closed + 4 edge fns OAuth/publisher [deno 8/8, deployadas, 3×402 live] + UI browser-verified Vision-QA-high; FR-PE-013 video-cadence deferido; prev 8969 gabriel-ai-moodboard-vision-qa seal: +handoff `5501a101-f4fb-4431-a9d8-34f551353c95` embedded 768d — 1º ciclo pago vídeo 9:16 witnessed + billing/CTA fixes + LinkedIn cadence E2E + virada brand-persona Gabriel AI/CCIO + blueprint YT/TikTok + nó mood-board multi-foto + mood board 4 retratos Vision-QA-gated + 2 animações DoP + regra Vision QA + canvas prompt.length hardening; prev 8960 creative-assets-spine-fatia1 seal: +handoff `8eb84bce-f0d5-4463-a79b-9de9ab5892b9` embedded 768d — HyperFrames editor LIVE [video-studio.service + vhost SSO + iframe /dashboard/canvas/video] + auth gating ?devLogin + Canvas hydration-race bug fix + projeto 63d406fe recuperado + creative_assets SPINE [migration+RPC service-role-only, dual-write video-bridge/canvas-execute/generate-image, backfill 73, Biblioteca de Assets UI]; prev 8959 hyperframes-studio-blueprint-and-video-billing-fix seal: +handoff `b42e89f9-3636-4ff0-a86e-674ed479d3c5` embedded 768d via trigger — blueprint de integração do HyperFrames Studio [deepsearch `ae8b94c5`, StudioApp zero-props + seam StudioApiAdapter → módulo-container VS-UI] + fix do gap de billing OTD-VA-010 [crédito compensatório idempotente `refund_autopilot_video_enqueue` migration `20260624140000`, smoke 8/8 net-debit-exclui-12, /security-review SAFE]; prev 8958 video-9x16-motor-and-autopilot seal: +handoff `5e470dff-d7b3-4936-a130-2c34350d56c8` embedded 768d via trigger — vídeo 9:16 autônomo: VS-2 motor HyperFrames determinístico vivo [render-core Playwright+FFmpeg 1080×1920 sha256-idêntico, video-bridge.service, bucket, edge poll://] + VA-V1 integração Autopilot [orchestrate-step enfileira render do ângulo real, custo no pré-débito do ciclo, attach content_library+creative_metrics] + flip editor OTD-VS-005 A→C módulo-container; prev 8954 autopilot-activation-security-hardening seal: +handoff `bc175ac9-e8a8-483b-a32f-4660dd0b90ba` embedded 768d via trigger — 3 arcos: Viral Autopilot ATIVADO [1º ciclo pago `947ef8b5` + pg_cron jobid 3] + FR-VA-018 trend angle hardened + segurança social-auth [state HMAC + webhook IG sig] + paridade pt-BR Cyber-Sentinel OTD-VA-018; prev 8946 alertas-video-fatia1-de-n8n seal: +handoff `bb23b9dc-265e-4338-9709-d320371908b4` embedded 768d — alertas CF/security-drift + Vídeo Fatia 1 [video_renders/video_assets/finalize_video_render + edge video-render/poll] + Fatia 1b UI + emenda BoK SDD v1.2 De-n8n; prev 8935 viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 8624	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 8625	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 8626	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 8627	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 8628	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 8629	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 8630	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 8631	- HNSW cosine index operational
> 8632	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 8633	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 8634	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 8635	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 8636	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 8637	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 8638	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 8639	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 8640	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 8641	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 8642	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 8643	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 8644	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 8645	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 8646	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 8647	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 8648	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 8649	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 8650	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 8651	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 8652	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 8653	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 8654	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 8655	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 8656	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 8657	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 8658	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 8659	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 8660	
> 8661	### Embedding Model
> 8662	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 8663	Schema: `vector(768)` — HNSW cosine index.
> 8664	
> 8665	### Embedding Pipeline (Autônomo — 2026-05-03)
> 8666	Três camadas eliminam intervenção manual:
> 8667	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 8668	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 8669	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 8670	
> 8671	### Comandos de manutenção da Mesh
> 8672	```bash
> 8673	# Verificar nós sem embedding (deveria retornar array vazio):
> 8674	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 8675	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 8676	
> 8677	# Backfill manual (Bun-native — requer .env):
> 8678	bun run scripts/backfill-embeddings.ts
> 8679	
> 8680	# Backfill de código-fonte nos nós AST:
> 8681	bun run scripts/backfill-node-content.ts
> 8682	
> 8683	# Re-sync AST completo:
> 8684	cd packages/gitnexus-core && npm run sync-mesh
> 8685	
> 8686	# Acompanhar re-ingesta pós-commit:
> 8687	tail -f /tmp/mcorch-ingest.log
> 8688	```
> 8689	
> 8690	---
> 8691	
> 8692	## Video Rescue Protocol
> 8693	
> 8694	When a video generation operation (Google Veo) times out or client disconnects:
> 8695	```bash
> 8696	# Via edge function (production):
> 8697	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 8698	  -H "Authorization: Bearer <user_jwt>" \
> 8699	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 8700	
> 8701	# Via local script (admin/debug):
> 8702	source .env && bun run rescue.ts <operation_id> <content_id>
> 8703	```
> 8704	
> 8705	---
> 8706	
> 8707	## Architecture Pillars
> 8708	
> 8709	| Layer | Implementation |
> 8710	|-------|---------------|
> 8711	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 8712	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 8713	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 8714	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 8715	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 8716	
> 8717	---
> 8718	
> 8719	## Phase Delta — Architecture
> 8720	
> 8721	```
> 8722	OrchestrationPage (full-canvas, p-0)
> 8723	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 8724	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 8725	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 8726	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 8727	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 8728	        ├── nodes/PublishNode.tsx    ← final distribution output
> 8729	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 8730	        └── NodePalette.tsx          ← top toolbar to add nodes
> 8731	
> 8732	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 8733	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 8734	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 8735	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 8736	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 8737	```
> 8738	
> 8739	### Canvas State Architecture (Hybrid)
> 8740	
> 8741	```
> 8742	User interaction → ReactFlow internal state (positions, drag)
> 8743	                         ↓ (debounced 600ms)
> 8744	                   localStorage (positions persist across refresh)
> 8745	                         ↑
> 8746	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 8747	     ↓ (status changes sync to ReactFlow via useEffect)
> 8748	ReactFlow renders visual status (idle/running/done/error/blocked)
> 8749	```
> 8750	
> 8751	## Key Files
> 8752	
> 8753	| Purpose | Path |
> 8754	|---------|------|
> 8755	| Architecture rules | `CLAUDE.md` |
> 8756	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 8757	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 8758	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 8759	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 8760	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 8761	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 8762	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 8763	| **Node types** | `src/components/orchestrator/nodes/` |
> 8764	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 8765	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 8766	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 8767	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 8768	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 8769	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 8770	| Billing utilities | `src/lib/billing.ts` |
> 8771	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 8772	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 8773	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 8774	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 8775	| Video rescue (local) | `rescue.ts` |
> 8776	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 8777	| Backfill script | `scripts/backfill-embeddings.ts` |
> 8778	| Deploy harness | `scripts/harness-deploy.sh` |
> 8779	
> 8780	---
> 8781	
> 8782	## First Client Onboarding Checklist
> 8783	
> 8784	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 8785	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 8786	3. ~~Activate watchdog cron~~ ✅ Done
> 8787	4. ~~Deploy rescue-video function~~ ✅ Done
> 8788	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 8789	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 8790	7. Monitor `infra_health_logs` for first 24h.
> 8791	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 8792	
> 8793	---
> 8794	
> 8795	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 8796	
> 8797	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 8798	
> 8799	| Action | Result |
> 8800	|--------|--------|
> 8801	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 8802	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 8803	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 8804	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 8805	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 8806	
> 8807	| Commit | Conteúdo |
> 8808	|--------|----------|
> 8809	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 8810	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 8811	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 8812	
> 8813	### Arquitetura Matrix Intelligence
> 8814	
> 8815	```
> 8816	ConstellationMatrix (Stabilized Engine)
> 8817	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 8818	  └── NodeDetailsPanel (Tabbed Navigation)
> 8819	        ├── Tab Meta: Neighbor exploration + Net Context
> 8820	        ├── Tab Code: Source code preview (Supabase sync)
> 8821	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 8822	
> 8823	useNodeIntelligence Hook:
> 8824	  - contentQuery: fetch nodes.content column
> 8825	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 8826	  - state: isAnalyzing, analysisResult, progress
> 8827	```
> 8828	
> 8829	---
> 8830	
> 8831	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 8832	
> 8833	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 8834	
> 8835	| Action | Result |
> 8836	|--------|--------|
> 8837	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 8838	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 8839	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 8840	
> 8841	**Output da análise (estruturado em pt-BR):**
> 8842	- Visão Geral — papel do módulo no sistema
> 8843	- Padrões Detectados — design patterns, antipatterns
> 8844	- Acoplamento & Dependências — análise In/Out-Degree
> 8845	- Recomendações — 1-3 ações priorizadas
> 8846	
> ```

## 🤖 Claude *(22:42:12)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat .claude/context/sprint-priorities.md 2>/dev/null | head -60 || echo \"NO sprint-priorities.md\"; echo \"===SCRATCH===\"; ls -la scratch/ 2>/dev/null",
  "description": "Read sprint priorities + scratch contents"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> <persisted-output>
> Output too large (50.5KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/229e84c1-28e5-4039-822d-8abc44633657/tool-results/bic8smwap.txt
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

## 🤖 Claude *(22:42:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for slug in $(ls docs/bok/ 2>/dev/null); do\n  if [ \"$slug\" = \"security\" ]; then\n    required_sec=(00-deepsearch-blueprint 01-brd-security 02-srs-secure-spec 03-sdd-hardening-architecture 04-fmea-security)\n    missing=()\n    for doc in \"${required_sec[@]}\"; do\n      [ -f \"docs/bok/security/$doc.md\" ] || missing+=(\"$doc\")\n    done\n    [ ${#missing[@]} -eq 0 ] && echo \"OK security (ciso-4-artifact)\" || echo \"WARN security missing: ${missing[*]}\"\n    continue\n  fi\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"OK $slug\" || echo \"WARN $slug missing: ${missing[*]}\"\ndone",
  "description": "BoK gate completeness check across all suites"
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
> OK conteudo-v2
> OK e2e-user-zero
> OK gamificacao-nodes
> OK identity-fabric
> OK marketing-hub
> OK mcorch-constellation
> OK mcorch-qa-healing
> OK mercado-livre-api
> OK meta-api
> OK openclaw
> OK post-engine
> OK security (ciso-4-artifact)
> WARN spaces-evolution missing: 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics
> OK video-studio
> OK viral-autopilot
> OK viral-daily-canvas
> OK viralmind
> OK vision-mcp
> ```

## 🤖 Claude *(22:42:34)*


## 🤖 Claude *(22:42:35)*

Worktree limpo, TS zero erros, mesh saudável. Só preciso confirmar o conteúdo de `scratch/` (flagged) antes de fechar o brief.

## 🤖 Claude *(22:42:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null | head -30; echo \"---SPACES-BOK---\"; ls docs/bok/spaces-evolution/ 2>/dev/null",
  "description": "List scratch files + spaces-evolution BoK contents"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun 30 01:44 .
> drwx------ 31 ubuntu ubuntu 4096 Jun 30 16:46 ..
> ---SPACES-BOK---
> 00-index.md
> 01-mrd-spaces.md
> 02-brd-spaces.md
> 03-prd-spaces.md
> 04-frd-spaces.md
> 05-sdd-spaces.md
> 09-live-recon-spaces.md
> 10-ui-inventory-spaces.md
> 11-node-registry-spaces.md
> 12-node-anatomy-spaces.md
> IMPLEMENTATION-PROMPT.md
> scaffold
> ```

## 🤖 Claude *(22:42:45)*


## 🤖 Claude *(22:43:11)*

Tudo coletado. `scratch/` está limpo (o WARN foi falso-positivo do `&&` sobre diretório vazio). Segue o brief.

```
═══════════════════════════════════════════════════════════
  HANDSON — Gabriel AI · Fatia 2 (Clone de Voz) + Fatia 3a (Consent+Erasure LGPD) — 2026-06-30
═══════════════════════════════════════════════════════════
```

🏁 **ESTADO ATUAL**
Fase selada: **Gabriel AI — Fatia 2 (Clone de Voz) + Fatia 3a (Consentimento + Erasure LGPD)**
Últimos commits:
- `16e42f1` — chore(handoff): proof-manifest → c138539f (Fatia 2 + 3a seal)
- `0f4f5ea` — docs(handoff): seal Gabriel AI Fatia 2 (Voice Clone) + Fatia 3a (Consent+Erasure LGPD) — mesh 8996
- `7913546` — docs(readme): v6.61.0 — Avatar Voice Clone + Consent/Erasure
- `cc5afc3` — test(avatar-clone-ai): consent+erase zero-cost smoke (11 gates, Fatia 3a)

📂 **MUDANÇAS PENDENTES**
Worktree limpo ✅ — `git status` vazio, sem diffs.

🏗️ **INFRA**
- `mcorch_chroma`: Up 2 weeks (healthy) — Chroma API v2: ✅ OK (`heartbeat` respondeu)
- `mcorch_claude_mem`: Up 2 weeks (healthy)
- `mcorch_vision_mcp`: Up 29h (healthy)
- `mega-brain-{daemon,webhook,dashboard}`: ✅ healthy/up

🧠 **KNOWLEDGE MESH**
**8996 nós** · ~9070 arestas · 100% embedded (768d HNSW cosine)
Último nó: handoff `c138539f` (Fatia 2/3a) + milestone Fatia 2 `b51d8de6`.

🔧 **TYPESCRIPT** — Zero erros ✅ (`tsc --noEmit` limpo)

📚 **BoK SUITES** (MCORCH Master Execution Protocol)
- **24 suítes seladas** ✅ (avatar-clone-ai 10/10 incluído — gate ABERTO).
- ⚠️ **1 incompleta no gate:** `spaces-evolution` — tem MRD→SDD presentes mas com sufixo `-spaces` (`01-mrd-spaces`…`05-sdd-spaces`) + supplementares 09-12 + IMPLEMENTATION-PROMPT. Faltam os genéricos `06-data-model`/`07-process-flow`/`08-quality-metrics`. **Não é blocker real** — é descasamento de convenção de nome no script do gate; o núcleo MRD→SDD existe. Spaces está em **Phase 0** (scaffold promovido, seal anterior).

📌 **SPRINT**
Goal: *Distribuição social autônoma operacional* (LinkedIn ✅; Twitter gated em API tier; IG gated em App Review).
Programa ativo real: **Gabriel AI / brand-persona CCIO** + **Viral Autopilot** (motor R1-R4 vivo, vídeo 9:16 autônomo provado).

⚡ **PRÓXIMOS PASSOS** (prioridade)
1. **Gabriel AI — Fatia 3b (avatarIdentity + Identity Gate)** — continuação natural da seal. **GATED por Lei 1 (honesto):** ArcFace/InsightFace ausente no código; a BoK (FR-AC-013/014) exige ArcFace calibrado em frames reais do Gabriel + treino Soul ID (plano pago Higgsfield). Requer **emenda BoK** (ArcFace→VLM-soft MVP via Vision MCP, *ou* provisionar face-verify AWS Rekognition/Azure/Face++) **+ dados biométricos do Sovereign**. Não improvisável.
2. **Viral Autopilot** — pendente: **editor HyperFrames Studio** (módulo-container, vhost `studio.mcorch.com` = ação Sovereign) + **1º ciclo pago de vídeo witnessed** (habilitar `video_enabled` + GO) + **postback ML real** + **publish vertical TikTok/IG/YT** (OAuth + App Review).
3. **Brand-persona YT/TikTok** — ~3 branches net-new (publish-social / social-auth init+callback / refresh) + gap `auto-publish` não passa `video_url`; **amendar BoK post-engine antes de codar** (blueprint pronto em `.claude/context/yt-tiktok-brand-persona-integration-prep-2026-06-26.md`).

⚠️ **ALERTAS**
- `scratch/` limpo ✅ (WARN do checklist foi falso-positivo — diretório vazio).
- `spaces-evolution` BoK com naming não-canônico (ver acima) — só vira bloqueador se a sessão tocar Spaces materialmente; nesse caso, renomear/completar 06-08 antes de código.
- Nenhum erro de TS, nenhum container unhealthy, nenhuma mudança não-commitada.

```
═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════
```

A continuação mais óbvia é a **Fatia 3b do Gabriel AI**, mas ela está travada por dois bloqueios materiais (emenda BoK + biometria do Sovereign). Se quiser seguir por ela, posso draftar a emenda BoK (rota VLM-soft MVP). Senão, há trilha pronta no **Viral Autopilot** (1º ciclo de vídeo pago / editor Studio) ou na **integração YT/TikTok**. Qual frente seguimos?

## 👤 User *(22:55:45)*

Para continuar aqui como podemos usar o comando /loop para continuar toda a sequencia lógica que montamos de malha fechada? Pois temos tudo o planejado mas agora por exemplo eu fiz o handson e teria que mandar um simples ok continue, mas poderia ter algo mais sofisticado e acertivo do que isso?

## 🤖 Claude *(22:57:09)*


## 🤖 Claude *(22:57:34)*

Boa pergunta — e a resposta curta é: o `/loop` tem exatamente o modo que você quer, mas o "mais sofisticado e assertivo" não está no comando, está na **diretiva que você dá pra ele**. "ok continue" é um prompt vazio; o salto de qualidade é encodar o nosso Protocolo de Malha Fechada *dentro* do loop.

## Os dois modos do `/loop`

| Modo | Sintaxe | Quando |
|------|---------|--------|
| **Intervalo fixo** | `/loop 30m <prompt>` | Polling de estado externo — testemunhar o 1º ciclo pago de vídeo, postback ML, um deploy. Dispara a cada 30 min independente. |
| **Auto-ritmado (dynamic)** | `/loop <prompt>` (sem intervalo) | **É o que você quer.** Eu mesmo decido *quando* continuar e sigo trabalhando até esgotar o backlog ou bater num portão. Sem você digitar "ok" entre as fatias. |

## Por que isso vence o "ok continue" (5 pontos)

1. **Auto-pacing** — não preciso da sua confirmação entre iterações; eu agendo o próximo passo sozinho.
2. **Política de prioridade escrita** — em vez de eu re-adivinhar o que vem depois a cada turno, o loop lê uma *charter* (arquivo) com o backlog priorizado e as condições de parada. Decisão determinística e inspecionável, não no "feeling".
3. **Portões respeitados** — a charter define o que eu executo sozinho vs. o que **HALT + escalo pra você** (Lei 4: Reviewer = Sovereign). Biometria, DNS/vhost, App Review, GO de gasto, decisão arquitetural → entram numa **Fila de Ação Sovereign**, não viram improviso.
4. **Selo automático** — `/handoff` incremental ao fechar cada Fatia, e selo final + parada quando a janela chegar a ~95% (Lei 3 calibrada). Progresso sempre durável.
5. **Survival Laws no laço** — prova material (Lei 1) + SOP-antes-de-código (Lei 2) + self-audit a cada iteração, embutidos.

## O comando (versão assertiva)

```
/loop Você é o MCORCH Master Execution Agent em malha fechada autônoma.
A cada iteração: (1) git fetch + releia o Pending Actions do HANDOFF.md e a
charter em .claude/context/autonomous-loop-charter.md; (2) pegue o item de
MAIOR valor que esteja DESBLOQUEADO; (3) rode o ciclo fechado — BoK Gate →
SOP Lei 2 → código → prova material Lei 1 → /security-review se houver
migration → commit granular; (4) se exigir ação do Sovereign (biometria,
DNS, App Review, GO de gasto, decisão arquitetural), registre na Fila de
Ação Sovereign e pule pro próximo; (5) Survival self-audit; (6) /handoff
incremental ao fechar cada Fatia, selo final + parar a ~95% da janela OU
backlog desbloqueado esgotado. Reporte em PT-BR a cada iteração: o que
entregou (com prova) e o que entrou na Fila Sovereign.
```

A charter (`.claude/context/autonomous-loop-charter.md`) é o upgrade real — ela guarda o backlog ordenado, as condições de HALT e a Fila Sovereign, e eu a atualizo a cada fatia. Esqueleto:

```markdown
# Autonomous Loop Charter
## Backlog (ordem de valor, só DESBLOQUEADOS executam)
1. Gabriel AI 3b — emenda BoK (rota VLM-soft via Vision MCP)  [DESBLOQUEADO: drafting]
   └─ HALT no treino face: exige frames reais do Sovereign
2. YT/TikTok — emenda BoK post-engine + 3 branches publish/auth  [DESBLOQUEADO até OAuth audit]
3. Viral Autopilot — McorchAdapter/bridge do editor Studio  [HALT no vhost studio.mcorch.com]
## Fila de Ação Sovereign (o que SÓ você destrava)
- (preenchida pelo loop conforme bate nos portões)
## Parar quando: janela ~95% · OU backlog desbloqueado vazio · OU GO seu
```

**Caveat honesto (Lei 1):** vários itens de topo são Sovereign-gated *na ponta física* (biometria do 3b, GO do ciclo pago, DNS do Studio, App Review). O loop faz **toda a engenharia desbloqueada até o portão** — drafta as emendas BoK, scaffolda os nós/edges, escreve SOPs+smokes, roda `/security-review` — e te entrega uma fila de decisão enxuta no lugar dos itens travados. Ele não vai *shipar* o que depende dos seus dados/credenciais/GO. Isso está alinhado com a sua diretiva de força-total autônoma.

**Controle:** pra parar, é só me mandar qualquer mensagem (interrompe o laço) ou desligar o `/loop`. Eu seloo antes da janela encher, então nunca perde estado.

Deixa eu te perguntar o modo de arranque:

## 🤖 Claude *(22:57:39)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "Como voc\u00ea quer arrancar o loop de malha fechada?",
      "header": "Arranque do loop",
      "multiSelect": false,
      "options": [
        {
          "label": "Charter + lan\u00e7ar agora",
          "description": "Eu escrevo a charter (.claude/context/autonomous-loop-charter.md) com o backlog priorizado + condi\u00e7\u00f5es de HALT, e disparo o /loop auto-ritmado. Trabalho aut\u00f4nomo at\u00e9 a janela ~95% ou um port\u00e3o Sovereign, selando cada Fatia. Voc\u00ea recebe relat\u00f3rio PT-BR por itera\u00e7\u00e3o + a Fila de A\u00e7\u00e3o Sovereign."
        },
        {
          "label": "S\u00f3 o comando, sem lan\u00e7ar",
          "description": "Eu te entrego o /loop pronto pra colar e a charter como arquivo, mas N\u00c3O inicio nada. Voc\u00ea dispara quando quiser, no seu tempo."
        },
        {
          "label": "Loop de testemunho (intervalo)",
          "description": "Em vez de queimar backlog de dev, um /loop por intervalo focado em POLLING externo \u2014 testemunhar o 1\u00ba ciclo pago de v\u00eddeo, postback ML, deploy. Dispara a cada N min e reporta mudan\u00e7a de estado."
        }
      ]
    }
  ]
}
```

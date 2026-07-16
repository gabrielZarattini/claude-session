# Configure Pinterest API credentials and global auth keys
**Date:** 2026-07-16 | **Session ID:** `30b8024d-52b5-4c1c-883b-b168f94313b7`

---

## 👤 User *(20:02:12)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(20:02:12)*

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


## 🤖 Claude *(20:02:28)*


## 🤖 Claude *(20:02:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -7 && echo \"---STATUS---\" && git status --short && echo \"---DIFFSTAT---\" && git diff HEAD --stat | tail -5 && echo \"---WC---\" && wc -l HANDOFF.md",
  "description": "Estado git + tamanho do HANDOFF.md"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 0fc3c40 docs(handoff): seal loop MAPE-K — UX-Explorer + landing-bundler + BoKs 9/9 retroativas + swarm:read (malha 9127)
> 1068c8b docs(readme): v6.105.0 — BoK 9/9 retroativas (32/32) + landing-bundler + UX-Explorer (malha 9127)
> 1b30fc3 feat(predictive-swarm): swarm:read no allowlist do PAT — sub-fatia da Fatia 2 (FR-PSW-002)
> 76e5a8a fix(scripts): idempotência CHECK-BEFORE-INSERT nos 13 seed seals restantes (anticorpo 0718101 completo)
> 4d59f69 docs(loop): charter — it.0-it.3 fechadas (diretiva 2026-07-16 drenada até it.4)
> 0718101 chore(mesh): seal nodes das BoKs retroativas + anticorpo de idempotência
> a8265eb docs(bok): video-repurpose + youtube-studio — suítes 9/9 RETROATIVAS seladas (32/32 famílias verdes)
> ---STATUS---
> ---DIFFSTAT---
> ---WC---
> 10202 HANDOFF.md
> ```

## 🤖 Claude *(20:02:30)*


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

## 🤖 Claude *(20:02:33)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"; echo \"---CHROMA---\"; curl -s --max-time 5 http://localhost:8001/api/v2/heartbeat; echo; echo \"---BOK---\"; ls docs/bok/ 2>/dev/null; echo \"---SCRATCH---\"; ls scratch/ 2>/dev/null && echo \"\u26a0\ufe0f scratch/ has files\" || echo \"scratch/ clean\"",
  "description": "Infra Docker + Chroma + BoK dirs + scratch"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 24 hours (healthy)
> mcorch_claude_mem: Up 4 weeks (healthy)
> mcorch_chroma: Up 4 weeks (healthy)
> mega-brain-dashboard: Up 4 weeks
> mega-brain-webhook: Up 4 weeks (healthy)
> mega-brain-daemon: Up 4 weeks (healthy)
> ---CHROMA---
> {"nanosecond heartbeat":1784232153353883954}
> ---BOK---
> agentic-governance
> agentic-workspace
> aios-sql-bridge
> authenticated-browser-operator
> avatar-clone-ai
> canvas-design
> constellation-v2
> content-provenance
> conteudo-v2
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
> post-engine
> predictive-swarm
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
> ---SCRATCH---
> ⚠️ scratch/ has files
> ```

## 🤖 Claude *(20:02:37)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for slug in $(ls docs/bok/ 2>/dev/null); do\n  if [ \"$slug\" = \"security\" ]; then\n    required_sec=(00-deepsearch-blueprint 01-brd-security 02-srs-secure-spec 03-sdd-hardening-architecture 04-fmea-security)\n    missing=()\n    for doc in \"${required_sec[@]}\"; do\n      [ -f \"docs/bok/security/$doc.md\" ] || missing+=(\"$doc\")\n    done\n    [ ${#missing[@]} -eq 0 ] && echo \"\u2705 security \u2014 BoK complete (ciso-4-artifact)\" || echo \"\u26a0\ufe0f security \u2014 missing: ${missing[*]}\"\n    continue\n  fi\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug \u2014 BoK complete\" || echo \"\u26a0\ufe0f $slug \u2014 missing: ${missing[*]}\"\ndone",
  "description": "BoK Gate check \u2014 completude das suites"
}
```

## 🤖 Claude *(20:02:38)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "limit": 71
}
```

## 🤖 Claude *(20:02:38)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md"
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
> ✅ content-provenance — BoK complete
> ✅ conteudo-v2 — BoK complete
> ✅ e2e-user-zero — BoK complete
> ✅ gamificacao-nodes — BoK complete
> ✅ identity-fabric — BoK complete
> ✅ landing-factory — BoK complete
> ✅ marketing-hub — BoK complete
> ✅ mcorch-constellation — BoK complete
> ✅ mcorch-qa-healing — BoK complete
> ✅ mercado-livre-api — BoK complete
> ✅ meta-api — BoK complete
> ✅ openclaw — BoK complete
> ✅ post-engine — BoK complete
> ✅ predictive-swarm — BoK complete
> ✅ security — BoK complete (ciso-4-artifact)
> ✅ spaces-cadence — BoK complete
> ✅ spaces-evolution — BoK complete
> ✅ tiktok-login — BoK complete
> ✅ video-repurpose — BoK complete
> ✅ video-studio — BoK complete
> ✅ viral-autopilot — BoK complete
> ✅ viral-daily-canvas — BoK complete
> ✅ viralmind — BoK complete
> ✅ vision-mcp — BoK complete
> ✅ youtube-studio — BoK complete
> ```

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
> 14	| **Loop MAPE-K: UX-Explorer + landing-bundler + BoKs 9/9 retroativas + swarm:read PAT (2026-07-16)** | ✅ Loop GO'd pelo Sovereign ("pode armar o loop para atacar os próximos passos") + pedido paralelo de auditoria de prontidão BoK 9/9. Drenou it.0→it.4 da diretiva. **(it.0) UX-Explorer enxerga pela 1ª vez da vida** — o auditor nightly nunca tivera run verde (exit 4 maiden + exit 3 ×9 dias); o "auth expirado" era FALSO diagnóstico em cadeia de **4 causas**: PATH do cron sem `agent-browser` (spawn ENOENT), regex do runner casando `/auth` da URL, `wait networkidle` sem `--load` (CLI tratava como seletor → timeout 30s), cron sem `--state` (tour DESLOGADO). Fix + auth state via magiclink (PROC-E2E-006) → cron simulado 6/7 verdes + **1º finding P1 REAL da história** (Vision QA: Controls do ReactFlow brancos sobre o void → `INC-8cba901a` RESOLVIDO `7a00511`: vars `--xy-*` MIV, override de classe perde pro chunk lazy; Vision re-run APROVADO). 2 incidentes fechados, fila zerada. **(it.1) landing-bundler core (`762c641`)** — o P0 da landing-factory: SOP Lei 2 ANTES do código → `scripts/landing-bundler/{bundle-core,public-url,cli}.ts` (magic-bytes mandam · CSS recursivo `@font-face` · fail-open por ref/fail-closed estrutural · guard anti-SSRF host re-valida cada 3xx · seam `injectHead` FR-LF-003); **15/15 unit** (G1 SSRF-302 sem emissão interna · G3 CF-challenge · G4 idempotência) + **G5 run real** 331B→150.802B, data:image+data:font REAIS (Google Fonts recursivo), 0 refs externas. **(it.2) witness cadência 7/7 (`885fa77`)** — dispatch real `cadence_dispatches`→`scheduled_posts` queued linkados, re-arm UTC, idempotência, tenant-bind, cleanup 0 resíduo (fecha ressalva do seal `c994c363`; smoke que o SOP nomeava agora existe). **(it.3) BoKs 9/9 retroativas — 32/32 famílias (`a8265eb`+`0718101`)** — método audit-first (`wf_2998d4c7`, 4 agentes, 18 drifts verificados adversarialmente, ground truth em `.claude/context/bok-readiness-audit-2026-07-16.json`) → micro-reparos `a729f83` (mesh mandate youtube-data + gate Gemini-only detector) → 6 writers + 2 critics (`wf_182e0145`; video-repurpose APPROVE 0 violations · youtube-studio 2 violations corrigidas) → verificação mecânica independente. YTS = **guarda-chuva 2 tracks** (GO Sovereign AskUserQuestion): Track A painel SHIPADO + Track B fábrica ROADMAP; estado vivo DATADO (gate Y3 satisfeito, rows=[[61]]). Seals malha `a6df1548`/`9a923887`. **(it.4) swarm:read no PAT allowlist (`1b30fc3`)** — predictive-swarm Fatia 2 sub-fatia; migration `20260716190000` estende o CHECK de vocabulário fechado (fail-closed: scope só entra com tool vivo); `/security-review` NO FINDINGS. **Task idempotência (`76e5a8a`)** — `mcorch_nodes.name` SEM UNIQUE → 24 seed scripts migrados p/ CHECK-BEFORE-INSERT (23/23 re-executados, malha estável). **11 commits** `50bd550..1b30fc3` · tsc 0 · vitest **601** verde · gitleaks clean · milestone `3a23fe00` embedado (768d) · malha **9127**. ⚠️ Pendente Sovereign: aplicar migration `swarm:read` em prod; predictive-swarm Fatia 2-resto (OTD-PSW-001 GPU decision); rotação de credenciais (SA Vertex/Gemini/Telegram); registrar `gcrux.com`+wildcard; 3 chaves Gmail; reconexão X + app-audit IG/TikTok. |
> 15	| **landing-factory BoK 9/9 + fix imagem quebrada + fix egress (2026-07-16)** | ✅ Sessão-maratona interativa (2 vídeos Maestros da IA → operação de marketing agêntica no Spaces; motor de conteúdo de 2 máquinas). **(1) landing-factory** — fábrica de landing pages AUTO-OTIMIZÁVEIS (loop CRO governado), beachhead do norte agência-dentro-da-plataforma; deepsearch verify-adversarial (`wf_1f7d1113`→`wf_b8cb767d`) → blueprint v0.2 (superset gate PASS) → **BoK Scribe 9/9** (`wf_d540ceb4`; MR14→BR18→PR18→FR20+NFR10+OTD15+FM14; **Pattern Conformance 15/5/1**; seal `b65e94b1` DERIVES_FROM constellation, embedado). Decisões Owner: Open Design **v0.10.0 pinado** (export single-file NÃO existe upstream — issue #368, `inline-assets.ts` byte-idêntico v0.10→main) → **asset-bundler próprio** (`landing-bundler` host worker) é o P0 da Fatia 1; hosting em **`gcrux.com`** (domínio registrável SEPARADO cookie-isolado, `<slug>.gcrux.com`; NUNCA `*.mcorch.com` — cookie SSO `sb-mcorch-session` `.mcorch.com`-scoped + access token + não-`HttpOnly` [`sso-cookie.ts:13,44`] = account takeover, FM-LF-013 RPN280) + Netlify/Vercel BYOK; WordPress-page-first; PostHog self-host/BYOK (gate humano→autônomo). **Gate Closed-Loop ABERTO** pro código. **(2) fix imagem quebrada** — inspetores Gerar Imagem/Vídeo re-assinam bucket privado (`useDisplayUrl`/`StorageVideo`, superfície faltante do Fix Assets; objeto do nó `n_8rsn4w3l` 400→200 image/png 1,1MB). **(3) fix egress** — signed URL reusável 24h (cache localStorage por uid, clear no logout) vs re-assinar a cada render → corta o cache-buster; `/security-review` NO FINDINGS · 13/13 testes. **(4) roadmap** artefato 2-máquinas salvo como asset do User 0. **6 commits** `9ccfeb7..10444b7` · tsc 0 · suíte **586** verde · gitleaks clean · milestone `56670e5c` · malha **9122**. ⚠️ Pendente: código do `landing-bundler` (Fatia 1); registrar wildcard `*.gcrux.com`; OTD-LF-001/003/014 + gate CRO 95%; provisionar 3 chaves Gmail (fila anterior); auditoria de agentes OpenClaw (free-first). |
> 16	| **Loop autônomo: Cadência + Enxame Fatia 1 em PROD + AI Act BoK (2026-07-15)** | ✅ Loop GO'd pelo Sovereign (migration+deploy autorizados) drenou os 4 itens da Fila. **(1) Veo via Vertex PROVADO REAL** — role Vertex AI User concedida → witness pago (gen `2659d78b`, `engine=veo-vertex`, 267 mco exatos 4263→3996, identidade preservada Read+Vision MCP; nó `4e8902d2`) + UI multi-key Vertex (preview do SA JSON, `8772f0d`). **(2) Cadência Fatia 1 SHIPPADA** (`spaces-cadence`, FR-CAD-001..011): motor de recorrência que ESTENDE `autopilot_plans` (plan_kind/recurrence/program/quiet_hours/…) + tabela `cadence_dispatches` (RLS default-deny + índice único parcial de idempotência) + roteia o tick vivo por `plan_kind` (**ZERO pg_cron novo**); `cadence-plan`/`cadence-run` (verify_jwt=false Bearer SB_SECRET_KEY, user_id da linha, drain FOR UPDATE SKIP LOCKED, dispatch→scheduled_posts) + node `kind:cadence`; migration `20260716120000` **aplicada+verificada** · `/security-review` NO FINDINGS · smoke 7/7 · nó `c994c363`. **(3) Enxame Sensorial Fatia 1 SHIPPADA** (`predictive-swarm`, FR-PSW-002/004/005/011/012): Tier 1 gates determinísticos (loudnessGate ffmpeg EBU R128 + contrastGate WCAG/APCA + verdictFor) + tool MCP `vision.parse_sensory_gate` **VIVOS** no container `mcorch_vision_mcp` (ffmpeg 8.0.1 instalado + rebuild, /health anuncia); SSRF por redirect do ffmpeg **FECHADO** (host-pin Supabase + `-protocol_whitelist`, auditor adversarial 7 vetores); tsc 0 · vitest **121/121** · nó `9ecba7fa`. **(4) content-provenance BoK 9/9 selada** (AI Act Art.50, FR-CP-001..013): blueprint deepsearch `531e2b0` + suite `c569416`; **3 camadas** C2PA (c2pa-rs) + watermark (TrustMark/VideoSeal/AudioSeal) + metadata IPTC (ExifTool), USD=0; integra no spine `creative_assets`; nó `825088c0`. **Órfãos FK** diagnosticados (`user_provider_keys`/`user_api_keys` sem cascade; fix GO-gated). **Crítico adversarial pegou 6 bugs born-dead/SSRF pré-deploy**; contagem de Pattern Conformance das 3 BoKs conferida **MATERIALMENTE** (armadilha fechada). **12 commits** `b15554d..a33bdd7` · 2 `/security-review` NO FINDINGS + 1 auditor SSRF focado · migration aplicada + 3 fns + container deployados (GO Sovereign) · malha **9119** · nó `eed9128f`. ⚠️ Ressalvas: Cadência falta witness E2E de despacho (throwaway/UI); Enxame `swarm:read` fora do PAT allowlist (Fatia 2); rotacionar as chaves expostas. |
> 17	
> 18	| **Veo 3.1 com avatar por referência (Gemini API + Vertex service account) + blueprints cadência/enxame (2026-07-14/15)** | ✅ Sessão-maratona interativa (Sovereign ao vivo fornecendo chaves e diagnosticando billing). **(A) Motor Veo 3.1** (Amendment 25, FR-SPACES-086..091): nó Imagem→Vídeo ganha o único motor com **referências de identidade** (≤3 fotos do mood board → mesmo rosto); ledger-first + `veo-poll` (LRO owner-scoped) + failover de chave por 429. **Witness pago PROVADO E2E** (gen `02994319`, 720×1280 9:16 8s, identidade preservada Vision QA, 178 mco exatos). **(B) Veo via Vertex AI** (Amendment 26, FR-SPACES-092..096): 2º caminho de auth por **service account** (JWT RS256→token, `_shared/google-sa-auth.ts` WebCrypto, sem lib Google) p/ usar os créditos GCP (trial não cobre Gemini API/429, só Vertex — documentado no README do repo GabrielAI). Roteamento por `metadata.auth_type`; custo Vertex **267 mco** (0,15/s); poll `fetchPredictOperation` + vídeo inline base64; UI de colar SA JSON no pool. **Witness Vertex PROVADO REAL E2E em prod** (role Vertex AI User concedida 2026-07-15 → gen `2659d78b`, `engine=veo-vertex`, 720×1280 9:16 8s com áudio, **identidade preservada** por Read ocular + Vision MCP independente, débito exato **267 mco** 4263→3996; asset `bb0ec719`, nó `4e8902d2`). Credencial no pool (id `d3c99581`, cifrada). **(C)** 2× SSRF pegos e FECHADOS pelo `/security-review` (redirect A25 + location/project no host A26 via `buildVertexUrl`); anticorpos 9+8 testes. **(D)** Blueprints selados (Fatia 0, BoK-first): nó de **Cadência** ("além do ManyChat", `docs/bok/spaces-cadence/`) + **Enxame Sensorial-Preditivo** (`docs/bok/predictive-swarm/`) — ambos via deepsearch com crítico adversarial (10+4 bloqueios corrigidos). **~14 commits** `11dafd0..541c2c4` · 3× `/security-review` (NO FINDINGS ×2 + 1 HIGH fechado) · smokes 13/13 · **584 testes** · tsc 0 · lint 0 · malha **9111** · nó `91a3f1ec`. ⚠️ SA privada colada no chat → rotacionar após o teste. |
> 19	
> 20	| **YouTube Fatia 2 + débito eslint ZERADO + roadmap não-gated + branding OAuth Google (2026-07-14)** | ✅ Sessão-maratona pós-v6.100.0 (loop autônomo GO'd + Sovereign ao vivo na verificação Google). **(A) Roadmap não-gated drenado:** carrossel IG pelo caminho AGENDADO (Amendment 22, fecha OTD-SPACES-044 — marcador de grupo `carousel_render_id` resolvido owner-scoped, FMEA-011 por construção; smoke 9/9) · reframe server-side no publish (Amendment 23, fecha OTD-SPACES-043 imagem — motor `reframeToJpeg` extraído p/ `supabase/functions/_shared/reframe.ts`, px do seed channel_profiles, fail-open; smoke 8/8 geometria 1080×1350 por decode SOF real) · trilhos de mídia LinkedIn imagem + IG Stories + X media (Amendment 24, FR-SPACES-082..085) + hardening `supabase/functions/_shared/public-url.ts` `assertPublicHttpUrl` (fecha classe SSRF pré-existente nos 5 fetch de mídia caller-controlada) · UI dos trilhos (toggle reframe no AssetDetailDialog + "Agendar carrossel" no VideoRepurposePage). **(B) Débito eslint ZERADO 448→0** (`bun run lint` exit 0; 26 warnings restantes): fan-out 1-agente-por-arquivo (122 arqs) types-only, tipos reais (Tables<>, interfaces por SELECT, catch narrowing, remoção de casts `as any` supérfluos), tsc+test verdes por lote, 6 commits + ignore de vendored/worktrees. **(C) YouTube Studio Fatia 2** (Amendment 12): editar (videos.update) + excluir permanentemente (videos.delete) vídeo via `force-ssl` + receita (revenue_metrics) via `yt-analytics-monetary.readonly` → os **4 escopos ficam demonstráveis** p/ a verificação Google (não aprova uso futuro); `social-auth-init` +escopo monetário; UI card Receita + Editar/Excluir por vídeo gated; smoke 9/9 fail-closed sem tocar canal; `/security-review` NO FINDINGS. **(D) Branding OAuth Google FIXADO** (marca verificada ✅): home era iframe-only (DOM do pai vazio) → verificador sem-JS não via nome/info → home crawlável login-free (HTML estático no `#root` do index.html + header React visível "MCORCH" + descrição + links Entrar/Privacidade/Termos; provado por curl do HTML cru servido). **21 commits** `1c59da5..08f49c5` · 2 `/security-review` NO FINDINGS · smokes 9/9+8/8+9/9 · guard-sweep +2 anticorpos · malha **9108** · nó `5f75a568`. |
> 21	
> 22	| **Assets: seletor de formato + pré-visualização fiel + modal responsivo (2026-07-14)** | ✅ Diretiva Sovereign "UI ruim nos assets, imagens gigantes estragando o modal, no mobile não é app responsivo; faltam opções de publicação + previsualização perfeita por tipo (IG stories/feed/carrossel/reels, YouTube shorts/comunidade)". **BoK-first:** Amendment 21 `21-amendment-publication-format-preview.md` (FR-SPACES-075..078 + OTD-SPACES-043/044 defer + Pattern Conformance inline #13 Human-in-the-Loop) + SOP leve `space-publish-format-preview.md`. **`src/lib/format-specs.ts`** = SSOT client de formato (canal×superfície → aspect/px/safe-zone/caption/publicabilidade; números DERIVADOS do seed `channel_profiles` — Lei 1; paridade 15/15). **`PublicationPreview.tsx`** = 10 chromes fiéis (Reels/Stories/Short **9:16** action-rail+safe-zones · Feed **4:5**/1:1 · Carrossel · Pin **2:3** · link-card · YT vídeo/comunidade · text-post; render 17/17; caveat honesto "prévia aproximada"). **`AssetDetailDialog`** reescrito: picker de formato + preview vivo, publica **imagem E vídeo** via `publish-space-asset` (migra do `publish-social` legado só-vídeo), badges honestos (Publicável/Privado até auditoria/Em breve); modal full-screen app-like no mobile (dvh/gutter/rounded/tap-44) + mídia contida. **Vision QA ocular pegou+corrigiu** um blowout de CSS Grid `min-width:auto` que estourava a imagem no mobile (fix `grid-cols-1`+`min-w-0`). Play affordance nos tiles de vídeo + título no toque; `PublishSocialInspector` do canvas reusa o mesmo preview (formatId + resolveAssetUrl). **4 commits** `56bf601..0f543af` · tsc 0 · eslint 0 · **+32 testes** · 4 deploys ao edge público (serve entry novo) · **E2E wire** (corpo da UI → publish-space-asset → linha `space_publish_variants` draft owner-scoped, limpa) · malha **9107** · nó `66952b93`. **Uncommitted→selado nesta sessão.** |
> 23	
> 24	| **Motor Viral Quality + ASR self-host + pool multi-key BYOK (2026-07-14)** | ✅ sessão-maratona interativa (Sovereign testando ao vivo, GO'ing deploys). **(1) Motor Viral Quality** (video-repurpose, BoK `10-frd-sdd-viral-quality.md` selada c/ Pattern Conformance): detector `detect-viral-moments` (Hormozi sobre o SRT, janelas 15-45s, `text_beats` = cues VERBATIM, LLM só escolhe índices — zero fabricação Lei 1, JSON-mode + parse defensivo) + overlay motion-graphic (`viral-caption-overlay-9x16.html` Montserrat premium sem botão + `renderAlphaFrames` RGBA + FFmpeg overlay sobre footage reenquadrado; anticorpo do `-t` multi-input). UI "Gerar cortes virais" 1-clique (barra ancorada em sinais reais) + botão Distribuir (`publish-space-asset`) + badge SRT. **3 shorts EP01 provados E2E em prod** (abertura 9.0/finale 9.5/conspiração 8.5, Vision 7-8/10). **(2) ASR self-host** whisper.cpp US$0 + reconciliação roteiro-autoritativa (o áudio da IA erra nomes: Austin→Boston Dynamics; roteiro do GitHub GabrielAI via MCP é a verdade). **(3) Rota host-media** streaming Range (206 seek) — master 1,3GB abre na biblioteca; infra host versionada. **(4) Pool multi-key BYOK** (Amendment 20): `user_provider_keys` Vault-cifrada + `resolveProviderKey` (explícita→prioridade→legado→402) + Settings card + seletor Spaces — 3 Gmails × créditos free-tier. **6 commits** `d4972c7..23f6e65` · `/security-review` **NO FINDINGS ×4** · malha **9105** · nó `d98767ea`. **Gated Sovereign:** aplicar migration `user_provider_keys` + deploy `canvas-execute` + cadastrar 3 chaves + aprovar cadência. |
> 25	
> 26	| **YouTube Studio (Fatia 1) + front-door host-local do Repurpose (2026-07-13)** | ✅ sessão interativa "colocar a ferramenta pra funcionar" (Usuário Zero). **(1) Painel YouTube** `/dashboard/youtube` — edge fn `youtube-data` lê vídeos+métricas (Data v3 + Analytics v2) com token per-user de `social_accounts` server-side; escopos alinhados aos 3 registrados no Google (analytics adiado até habilitar a YouTube Analytics API); mapa exaustivo da API (`docs/bok/youtube-studio/11-api-surface-map.md`: 13 recursos·175 props·52 métricas·33 ações + Pattern Conformance 21 padrões) + SOP. **(2) Front-door host-local do Repurpose (admin-only)** `/dashboard/repurpose` — o Sovereign sobe o master pela UI e gera cortes; cap de 50MB do Supabase free → master (1,3GB) vai pro **disco do host** via `host-upload-server` (loopback 3220 atrás de nginx `/api/host-upload`, **upload chunked** 80MB/pedaço furando o cap de 100MB do CF, JWT+admin-gate, streaming); `ingest-external-asset` +sign_upload +provider `local` ADMIN-ONLY; `video-repurpose-run` +source `local` ADMIN-ONLY; worker lê `bucket=local` realpath-contido **sem copiar 1,3GB**. yt-dlp do host CONFIRMADO bloqueado pelo YouTube (bot-check). **(3)** fix legenda drawtext (truncagem por bytes-extra UTF-8 → padding). **EP01 real 1,3GB → 5 shorts 9:16** (1080×1920) provados por Vision QA (reframe centralizado + legenda completa). 5 commits `e174988..f10fba4` (+README `adcab9a`) · `/security-review` **NO FINDINGS ×3** · malha **9102** · nó `9f7b191a` |
> 27	| **Motor de repurpose de vídeo — Fatias 1-3 (1 master → N shorts + carrossel IG) + OTD-SPACES-036 + witness LoRA (2026-07-12)** | ✅ sessão-maratona interativa (Sovereign aplicou 3 migrations ao vivo + testou cada gate). **A metade que faltava: o MCORCH agora PRODUZ cortes, não só distribui.** BoK-first (Closed-Loop): blueprint `docs/bok/video-repurpose/00-deepsearch-blueprint.md` fundamentado em 10 pointers verificados file:line + no mapa do pipeline validado do repo `gabrielZarattini/GabrielAI` (o INVERSO — N takes Veo→1 master; fonte do master + schema de metadados `episodios/epNN.json` + filosofia cut-spec data-driven). **Correções ao snapshot:** segmenter é **FR-CP-012** (não OTD-CP-011; SDD já o gateava em "quando entrar INPUT de vídeo longo" → esta capacidade é o gatilho); OTD-CP-009 FECHADA (imagem, vídeo é gap); youtube Pilar I=montagem (concat), segmentação=inverso; carrossel existente=PDF/LinkedIn (IG image-children=gap, contrato Meta confirmado). **(Fatia 1 VIVA)** `source_module='external'` no spine `creative_assets` (migration aditiva aplicada) + seam `ingest-external-asset` (owner-scoped `${uid}/` + bucket allowlist + no-`..`; upload MP4 + metadados episódio + SRT inline; YouTube gated OTD-VR-001) · smoke 5/5 · `/security-review` NO FINDINGS. **(Fatia 2 VIVA E2E)** worker host `video-repurpose-bridge` (fila `video_renders` engine `repurpose` aditivo, rail FFmpeg **grátis** charged 0) → `segment-core` (trim `-ss/-t` frame-accurate + reframe 16:9→9:16/1:1 center-safe expression-crop + legenda queimada drawtext-textfile) · guarda **OTD-VR-006** re-valida source no READ (o controle decisivo tenant-safe) · **provado E2E na produção**: master→3 clipes reais (Vision QA: CENTRO preservado, ESQ/DIR cortados, **timestamp 00:00:04.000 prova o trim**, legenda queimada) · `/security-review` NO FINDINGS. **(Fatia 3 E2E provada)** `carousel-core` (key-frames dos capítulos → slides 1080×1350 4:5 + legenda wrapped + handle; **OTD-VR-007** wrap conservador, legendas curtas limpas, pixel-perfect via render-core diferido) + worker branch `mode='carousel'` + enqueue `slides[{t_sec,caption}]`≤10 + branch **media_type=CAROUSEL** no `publish-social` (contrato Meta) + seam `publish-space-carousel` (resolve slides owner-scoped→assina→publica) · **provado E2E**: master→3 slides 1080×1350 image assets + Vision QA no slide real · `/security-review` NO FINDINGS. **Distribuição reusada (não reconstruída):** cortes/slides nascem `creative_assets` que o nó **"Publicar em Rede Social"** (`publish-space-asset`/`space_publish_variants` — **OTD-SPACES-036** decisão (b) landada nesta sessão: tabela dedicada owner-scoped, money-path intocado, migration aplicada + smoke) já consome. **Witness LoRA:** treino real→402 Insufficient credit na conta Replicate BYOK do User 0 (plumbing 100% provado até o passo pago; bloqueado só em crédito — não código; inferência-com-LoRA é fatia futura inexistente). **Gates externos honestos:** publish real na IG/TikTok gated na auditoria de app (ação Sovereign). 6 commits `ac5ca86..831f5cc` · 3 migrations aplicadas · rail 100% grátis US$ 0 · Malha **9097** · nó `f050959c` |
> 28	| **Voz clonada self-host COMPLETA + Modo Expressivo + motion design do canvas (2026-07-09/10)** | ✅ sessão-maratona interativa (Sovereign testando ao vivo, 12 commits `578f02e..aa4041f`). **(1) Rail de voz US$ 0 VIVO** (OTD-VOICE-001 fechada por veredito auditivo): motor Qwen3-TTS no host (`/home/ubuntu/.mcorch/voice-engine/`, witness RTF 6,4/RAM 3,15 GB) · migration `20260709234000` (fila `video_renders` reusada engine `qwen3-voice` + provider `qwen3-local` owner-prefixed; `/security-review` NO FINDINGS; **anticorpo WAF**: Management API devolve HTML-challenge em payload grande com `DO $$` → apply em chunks + prova material sempre) · worker `voice-bridge.service` (claim atômico + **heartbeat anti-reaper** 4 min — bug witnessed: job de 5000 chars era re-claimado no meio) · edge `generate-voice` keyless async 202 (consent Art.11/sentinel INTACTOS) · nó default "MCORCH · grátis" pt-BR + poll `useVoiceRenderPoll` · **multi-amostra FR-SPACES-059** (1 principal + até 5 clipes ≤7s, ffprobe fail-closed nomeando o clipe, referência composta ffmpeg-concat) · perfil **ICL `.qvoice`** (máx fidelidade; x-vector rejeitado pelo ouvido) + `-ref.wav` ao lado (grafts são model-bound) · **smoke 12/12** `smoke-voice-qwen3-local.ts`. **(2) Modo Expressivo** (`7c20895`/`aa4041f`): 1.7B (4,3 GB) + assets `.expr` · witness **RTF 13,9 "composed 3 spans"** · **normalizador da sintaxe do Sovereign** (`{happy}…{/happy}` · `<#0.5#>` · `(gasps)` → gramática real do engine; tag desconhecida NUNCA falada; 0.6B recebe texto 100% limpo) · roteiro 5000→**20000** chars · **"Gerar roteiro com IA"** no nó (select de modelos pela regra perene: Nemotron free/Gemini Pro/Claude via openrouter · Gemini Flash direto; prompt-checklist embutido em `expressive-prompt.ts`). **(3) Reparos materiais**: reunion migration `20260710170000` (a `20260707230000` derrubara `avatar-studio` do guard `register_creative_asset` — TODO áudio fora do spine em silêncio; worker agora CHECA `error` do rpc — `supabase.rpc` não lança) · enum `generate_voice` + INSERT no Histórico (`vm_canvas_executions`, nascido terminal) + backfills (2 assets + 2 execuções do `b57a59f7`) · **aba Áudios** na Biblioteca (tile de onda + player; `<img>` de .wav era invisível). **(4) Motion design Amendment 19** (`d964b2e`): motion = telemetria — nó processando (glow pulsante + anel conic girando), edge transmitindo (partículas `animateMotion`+`mpath`), **fio neon established** quando `output.generatedAt` existe; `FlowEdge` como edge default; 1 seam (useMemo no CanvasEditorPage) cobre os 12 node types sem persistir estado visual; frame-diff provou animação viva; `prefers-reduced-motion` ok. **(5) Regra perene BYOK** (`f5e290f`, memória `feedback_byok_only_available_options`): `useConfiguredProviders()` deriva booleans da view mascarada (bullets/NULL, zero segredo no browser); seletor de motor dinâmico; **ElevenLabs IVC multi-amostra** (`f56e49d`); **F5-TTS/Fish Speech V1.5 REJEITADOS por licença** (pesos CC-BY-NC/-SA — produto é comercial; Amendment 18); zoom 0.02–12; fixes borda-sob-neon + thumb via `StorageImg`; OTD-SPACES-037 reconciliada não-issue (SpaceCanvasPage sem rota viva). 2× `/security-review` NO FINDINGS (e o aside do 2º pegou o CHECK `success` vs `completed` — corrigido pré-commit). Malha **9094** · nó `8c1f0e7b` |
> 29	| **Creative Studio — nós Roteiro + Criativo Cinematográfico vivos + cadeia completa (2026-07-09)** | ✅ maratona autônoma (loop armado pelo Sovereign, ~10 wakeups) — graduou a PoC de vídeo em MVP no Spaces. **(1) Roteiro** (`scriptGenerator`): v1 script SSE (`0d1714a`) + v2 **storyboard estruturado** `{scenes[],ttsPrompt}` via edge fn nova `generate-script-package` (`/security-review` SAFE, `508cda7`/`41483c4`) + **fan-out** "Criar N nós de imagem" (`e44df93`). **(2) Criativo Cinematográfico** (`cinematicVideo`, `4d8b80b`): renderiza MP4 9:16 MIV pela fila `video-render`/`video-bridge` (FFmpeg grátis) — **rail provado E2E** (enqueue 202→worker→done→MP4 1080×1920) + **Vision ocular** (pegou worker stale rodando template errado → restart → template MIV confirmado, `36b256d`; lição `reference_hyperframes_worker_restart`). **(3) Fundação**: 3 primitivos FFmpeg grátis (`encodeImageSequence`/`encodeKenBurns` + template `cinematic-9x16` MIV) · Amendment 17 + agente `creative-director` + 4 skills · **hotfix zip** do treino LoRA (`canvas-assets` aceita `application/zip`, `f0743de`). **(4) Decisões de motor**: TTS multi-motor **VoxCPM2** (Apache-2.0, pt-BR, clone) · identidade multi-motor (char-ref default) · **Duix rejeitado** (licença/GPU/pt-BR). **2 correções Lei 1** (503 stale + template stale, pegas por prova ocular/material). Malha **9086** · nó `6f2a5a90` |
> 30	| **Spaces robustez — treino LoRA grátis REAL + nó WordPress + blueprint YouTube Studio (2026-07-08/09)** | ✅ loop autônomo 9 commits + seal. **(1) LoRA grátis (foco #1)** — `handleTrain` engine-aware + LoRA default (`a0e8590`) · Amendment 11 (30 fontes, **fecha OTD-AC-017**; FR-AC-016 aprovação-condicional Replicate↔BFL on-platform+no-export, `5c63c7b`) · edge fn `avatar-identity-train` (Replicate `ostris/flux-dev-lora-trainer` BYOK **USD 0**, async start+poll, consent Art.11, migration `20260708130000` aplicada, `06261b9`) · **plumbing provado zero-custo** (guard 422/401 · consent+BYOK do User 0 passam · chave Replicate autentica na training API, latest_version.id do trainer Replicate (prefixo 26dce37a, NÃO é commit git)) · `/security-review` **SAFE**. **(2) 1º nó social** — "Publicar no WordPress" (Post+Landing Page, categoria Publish no registry VIVO, embute imagem upstream, default rascunho opt-in, `07689e2`) · Amendment 15 família Publish/Social (`6c80cd1`) · **media-social BLOQUEADO OTD-SPACES-036** (channel_variants NOT NULL pillar-coupled → decisão de schema Sovereign, `8e51482`). **(3) YouTube Studio (ask #3)** — blueprint deepsearch `docs/bok/youtube-studio/00-deepsearch-blueprint.md` (`wf_baad6dbe-9e5`: 6 frentes + verify adversarial, 96 URLs, 27 OTDs; **monetização gated** inauthentic-content + synthetic-media disclosure; lipsync MuseTalk MIT/SadTalker Apache self-host USD-0, Wav2Lip bloqueado, `6fa1652`). **(4) Higgsfield** Platform key testável (botão custo-zero) + card MCP honesto créditos-vs-assinatura (`44e625c`). Malha **9082** · nó `f0aa8111` |
> 31	| **TikTok Login + Higgsfield MCP DCR + Senior UX/UI Loop + Universe 3.10 seal (2026-07-08)** | ✅ sessão-maratona. **(1) Universe 3.10** — Phase Epsilon V9 SELADA (verif adversarial 8-frentes `wf_98c9d432`, 7 PASS + re-escopo 3.2 honesto; tsc 0 · vitest 496/498 · E2E Vision; nó `c20153c1`, commit `2841683`). **(2) TikTok Login Kit v2** — BoK 9/9 selada (`299b9f36`) + SOP Lei 2 + 3 edge fns `verify_jwt=false` + migration `tiktok_identities`/`tiktok_login_codes` + botão gated `?devLogin` + SPA callback; **/security-review: 1 HIGH login-CSRF FECHADO** (browser-binding sessionStorage→state→binding_hash); **2 correções de reuso Sovereign**: mesma chave do connect via `social_app_config` (`2461fa2`) + reusa `social-auth-callback` já registrado por `intent` assinado (`aa7c2a0`, elimina gate redirect_uri); smoke 8/8 · browser-verify · connect íntegro. **(3) Higgsfield** — Platform key nas Settings (`989e560`, browser-verify logado) + **MCP OAuth DESTRAVADO via DCR programático** (client público em `mcp.higgsfield.ai/oauth2/register`, sem Clerk manual; oauth-init→authorization_url). **(4) Senior UX/UI Loop** (`5a0f695`) — auditor de jornada + grader `senior-rubric.ts` 8-dim SCORED + runner + SOP+skill+RUBRIC; unit 5/5 + prova live (P2 contraste "ou"). **(5) User 1** (`user1@teste.com`, `c515c035`) p/ QA. **(6) it.4b editor** = HyperFrames (`3e45e08`). Malha **9081** · nó `17e8921b` |
> 32	| **Spaces v2 — consolidação Canvas Studio + money path ledger-first + nós Lista/Upscale (2026-07-07)** | ✅ 11 commits `efaf190..ad42170`: **it.1** rename Canvas Studio→"Spaces" (`/dashboard/spaces` takeover, redirects **5/5** provados `verify-spaces-redirects.ts`, nav única, UI v1 aposentada — retorno ao contrato BoK `spaces-evolution`, **Amendment 14**) · **it.2a/b/c money path ledger-first** (project-dispatch em `generations`: migration `20260707220000` FK composta+XOR+RPC 9-args aditiva · edge fn catálogo fail-closed + style_transfer engine-fix + campaign-context + GAP-8 · cliente `useCanvasExecute` minta node_run_id + dual-read HistoryTab/StatusBar · watchdog cron 2º passe sobre `generations` + entrada de resgate service-role no webhook · `self-heal` exclui async; **/security-review NO FINDINGS**; smoke **40/40** + watchdog **6/6**; **witness pago** 4519→4518 exato, zero rows legadas → **OTD-SPACES-012 fechada**) · **it.4a nó Lista + lote template×produtos** (o "Lists" do Magnific; `product-list.ts` unit 10/10; witness 2 produtos→2 imgs, 20 mco exatos) · **it.3 thumbnails home** (URL re-assinável via StorageImg; witness + Vision APROVADO) · **it.4c nó Upscale REAL** (Replicate real-esrgan, money-safe auto-refund provado E2E, mensagem acionável de crédito) · **it.0a** fix preço sceneCompose 18→10. **2 bugs pré-existentes consertados** (style_transfer ignorava imagem-fonte; `creative_assets` rejeitava `source_module='spaces'` → registro falhava em silêncio desde Fase 1b, migration `20260707230000`). **Higgsfield resolvido:** nós usam a API key do vault (`keys.higgsfield`), MCP é opcional. guard-sweep **9/9**. Malha **9077** · nó `6a70b82b` |
> 33	| **Arco 8 — Laço Autonômico MAPE-K enterprise-grade VIVO (2026-07-07)** | ✅ 19 commits `9538e09..c197054`: M+A mecânicos perpétuos (guardian-tick */5 T1-T5 + heartbeat + incidentes dedup/cooldown/auto-resolve · guard-sweep 6/6h runner destacado · watchdog=monitor-do-monitor provado ao segundo · UX-Explorer nightly → `--ingest-findings`) + P+E em escada (L1 Telegram · **L2 ARMADO toggle --arm/--disarm, engine `nvidia/nemotron-3-ultra-550b-a55b:free` USD-0** [claude -p preservado via REMEDIATE_ENGINE] · L3 sessão event-driven via Monitor) · /security-review **BLOCK→4 must-fixes** (allowlist sem exec · git diff out · flock<budget · run-dir 0700) · **1º ciclo real fechado**: video-bridge render_failed → L2 diagnóstico validado → `422 composition_required` pré-débito (`f678cb3`) → resolvido · +2 incidentes de estreia corrigidos (PATH cron · dogfood inexistente) → sweep **7/7 auto-resolve**. SOP `autonomic-loop-mape-k.md`. Sessão Claude = bancada de dev pura. Malha **9071** · nó `d149d017` |
> 34	| **Loop (arco 7) — vizinhos on-select + OTD-SPACES-010 + backlog-drenado + hardening 478 testes (2026-07-06)** | ✅ 12 commits `235d7a2..828e492`: vizinhos semânticos on-select (verify browser PASS live) · OTD-SPACES-010 reconciliada (OIDC §3.1.3.7 — JWKS redundante no code-flow TLS; +check exp; vitest 17/17; deploy callback) · **varredura 7-agentes atesta backlog autônomo de feature DRENADO** (nó `aaf7a126`) · dead code `monetizationStats` removido · Fatia hardening GO-continue: **+53 testes** (semantic-synapses DRY 14 · universe-layout 9 · orientação 4 · canvas-utils 14 · sso-cookie anti-open-redirect 7 · asset-url 9), suite **448→478**, zero produção alterada. Anticorpo: nunca filtrar output de `git commit` (secret-scan bloqueou fixture; pego por git log). Malha **9067** · nó `3a145a46` |
> 35	| **Loop (arco 6) — Universo sinapses semânticas 768d + perf reconciliada (2026-07-05)** | ✅ 6 commits: `OTD-UCANVAS-PERF` reconciliada (não-issue: ~30s headless SwiftShader, real 2,5s — medição material, zero code churn) + **sinapses Fase B `OTD-SYNAPSE-EMBEDDING` SHIPPED** (RPC `match_memory_code_synapses` SECURITY DEFINER user_id-NULL-hardcoded LATERAL k-NN HNSW → **148 sinapses por similaridade 768d** código↔memória na fusão primária, ciano tracejada vs fúcsia sólida real, contadores separados [Lei 1]; /security-review NO FINDINGS; gate E2E Vision-APROVADO; smoke anticorpo 8/8). Loop **adiado p/ 2026-07-06 11:01** (cron `0f94aff2` session-only). Malha **9062** · nó `9afacad2` |
> 36	| **Loop FINAL (arco 5) — conector Higgsfield MCP server-side+UI COMPLETO + parada natural (2026-07-05)** | ✅ sub-fatia 7 UI card `217b4e3` (Settings→Conectores + callback page, browser-verify ocular) fecha o conector; 7 sub-fatias totais; parada natural (backlog desbloqueado esgotado, restante gated no Sovereign); malha **9060** · nó `dc47da77` |
> 37	| **Loop autônomo — brand-tail + Unified cutover + vídeo recorrente + conector Higgsfield MCP (2026-07-05)** | ✅ 12 commits: cauda de brand 100% `6af3181` + Unified Canvas 3.9 cutover `4729dd4` + cadência de vídeo recorrente FR-VA-022 `c5eaf1c` + **conector Higgsfield MCP OAuth server-side COMPLETO** (sub-fatias 1-6: sentinel G1 `268d436` · migration `0c9d182` · init `17597ab` · callback `988b1b9` · refresh/resolve `97b1e2f` · disconnect RPC `99d543a`); ciclo de credencial per-user fail-closed (connect·refresh·resolve·disconnect); **2× /security-review SAFE 9/10**; malha **9059**; E2E gated no consent Clerk (Fila 175) |
> 38	| **Loop it.1 — Anticorpo de assinatura owner-scoped (Fix Assets)** | ✅ `scripts/qa/smoke-asset-owner-signing.ts` 6/6 LIVE hermético (owner-sign 200 · cross-sign BLOCKED · enumeração 0 · id-squat neutralizado · is_public=0); fecha Mandato Obstáculo→Síntese |
> 39	| **Loop it.2 — BoK amendment Higgsfield MCP OAuth connector** | ✅ `docs/bok/spaces-evolution/13-amendment-higgsfield-mcp-connector.md` — gate Closed-Loop 3.5 fechado; contrato vivo provado (401 OAuth · 201 DCR · discovery Clerk); FR-SPACES-015..021 + OTD-SPACES-007; código gated na aprovação Sovereign |
> 40	| **Fix Assets — mídia privada assinável só pelo dono (regressão FECHADA)** | ✅ migration `20260703030000` (3 policies owner-scoped + triggers de id anti-claim + data-repair) + normalizador durável em 13 superfícies; `/security-review` CLOSED 9/10; E2E Vision-APROVADO; 90 assets do User 0 vivos |
> 41	| **Spaces 2d compose — drift FECHADO (OTD-SPACES-003)** | ✅ compose vivo E2E via OpenRouter Nano Banana (10 mco) + bucket privado assinado + sentinel de contrato Higgsfield |
> 42	| **Retema MIV do ecossistema + landing fiel + gate TikTok (2026-07-04)** | ✅ design system global MIV (void/cyan/gold/nebula · Playfair/JetBrains) revestindo 47 páginas + login + shell; landing 100% fiel ao original (hero WebGL cinematográfico + texto honesto, iframe); favicon do sigilo consistente + Privacidade/Termos MIV (footer único, conteúdo preservado); 44 páginas polidas via workflow 9-subagentes, E2E 0-erros |
> 43	| **brand-100 — emoji→lucide + data-viz→MIV em ~40 superfícies (2026-07-05)** | ✅ workflow de 7 subagentes: ~90 emoji→lucide (Minerador/Blog/canvas/crew/páginas; avatares→`AVATAR_ICON_MAP` compartilhado), data-viz→MIV (Louvain/node-types/territórios cyan/gold/nebula/teal; blobs magenta→cyan). Minerador+Matrix verificados. mesh **9057** · commits `855a4ad`/`8d65bb2`. Pendente cross-file: pickers de campanha/space |
> 44	| **Brand-everything (Orquestrador/Core-Fable → MIV) + /miv/ completo (2026-07-05)** | ✅ diretiva "tudo vira brand": Orquestrador Visual violet/fuchsia/magenta→cyan + ícones emoji→lucide (`NodeIcon`); Core-Fable amber→cyan; **`/miv/` serve o MIV completo** (site-miv, era 404). mesh **9056** · commits `b92c367`/`cbe5730`. Pendente honesto: emoji de templates/miner + paletas data-viz |
> 45	| **Certificação E2E User Browser + fechamento pt-BR (2026-07-05)** | ✅ E2E de 8 jornadas de usuário real (fresh, ambiente verificado limpo): **flow_works 8/8 · MIV-conformant 8/8 · 0 P0/P1/P2** (2 pass + 6 warn só-P3); anticorpo Lei 1 (squat de `python -m http.server` na porta contaminou o 1º run — subagentes flagaram, fix = verificar o bind antes de rodar). pt-BR fechado em toda a cauda (Arena/Economia/Orquestrador/Matrix/Memory/Video/3D). mesh **9055** · commits `94df8d0`/`63fee7b`/`becf373` |
> 46	| **Conformidade MIV pós-rebrand + tooling ECC-nativo (2026-07-04)** | ✅ auditoria visual E2E de 44 páginas (workflow 8 subagentes agent-browser — real-user nav, hovers, triggers, badges, widgets); 3 fixes sistêmicos (`--accent` cyan · mcoCoins gold · glow CTA) + regressões de marca (onboarding MCORCH · 404/miner/legenda pt-BR · Trial cyan) verificados ao vivo; tooling ECC-nativo (doctor · supply-chain sentinel · session-inspect) + SOP. mesh **9051** · commits `aaa2351`/`75077f6`/`8af7268` |
> 47	
> 48	## Loop MAPE-K: UX-Explorer + landing-bundler + BoKs 9/9 retroativas + swarm:read PAT Record (2026-07-16)
> 49	
> 50	**ORO:** Operator = MCORCH Master Execution Agent · Reviewer = `/security-review` (NO FINDINGS na it.4) + 2 critics adversariais das BoKs + verificação mecânica independente + Vision QA ocular · Owner = Sovereign (decisões de escopo YTS, apply da migration, gates de credencial/domínio).
> 51	
> 52	Loop autônomo MAPE-K re-armado pelo Sovereign, mais o pedido paralelo de auditoria de prontidão BoK 9/9 de video-repurpose/youtube-studio. O ritual (git fetch → incidentes → Fila) rodou a cada retomada. A sessão fechou **it.0 a it.4** da diretiva 2026-07-16 + a task de idempotência dos seed scripts, tudo com prova material (Lei 1) e commit granular. Selada por `/handoff` explícito do Sovereign após a pergunta "precisamos fazer /handoff oficialmente aqui?" — ponto de parada natural (bloco coeso fechado + cluster de gates Sovereign à frente).
> 53	
> 54	| Frente | Resultado |
> 55	|--------|-----------|
> 56	| it.0 — UX-Explorer (INC-39626fcd) | ✅ 4 causas empilhadas (PATH cron · regex `/auth` · `wait` sem `--load` · sem `--state`) → 6/7 flows verdes; nunca tivera run verde antes (`50bd550`) |
> 57	| it.0 — P1 real (INC-8cba901a) | ✅ Controls ReactFlow brancos → vars `--xy-*` MIV (override de classe perde pro chunk lazy); Vision re-run APROVADO (`7a00511`) |
> 58	| it.1 — landing-bundler | ✅ FR-LF-002/003; 15/15 unit + G5 real (331B→150KB, data:image+data:font, 0 refs externas); SOP Lei 2 primeiro (`762c641`) |
> 59	| it.2 — witness cadência | ✅ 7/7 dispatch real→scheduled_posts sem publicar; fecha ressalva `c994c363` (`885fa77`) |
> 60	| it.3 — BoK video-repurpose 9/9 | ✅ critic APPROVE 0 violations; seal `a6df1548` DERIVES_FROM landing-factory |
> 61	| it.3 — BoK youtube-studio 9/9 | ✅ guarda-chuva 2 tracks (GO Sovereign); 2 violations do critic corrigidas; seal `9a923887` |
> 62	| it.4 — swarm:read PAT | ✅ migration `20260716190000` fail-closed; `/security-review` NO FINDINGS (`1b30fc3`) |
> 63	| Task idempotência | ✅ 24 seed scripts CHECK-BEFORE-INSERT; 23/23 re-run malha estável (`76e5a8a`) |
> 64	
> 65	| Commit | Conteúdo |
> 66	|--------|----------|
> 67	| `50bd550` | fix(qa): UX-Explorer enxerga — 4 causas do INC-39626fcd |
> 68	| `7a00511` | fix(ui): ReactFlow Controls MIV via --xy-* vars (INC-8cba901a) |
> 69	| `a729f83` | fix(edge): micro-reparos pré-BoK (mesh mandate youtube-data + gate Gemini-only) |
> 70	| `762c641` | feat(landing-factory): landing-bundler core (FR-LF-002/003) |
> 71	| `885fa77` | test(spaces-cadence): witness E2E de despacho 7/7 |
> ```

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
> 11	| 1b | **Veo via Vertex AI (service account)** — Amendment 26, FR-SPACES-092..096 (2026-07-15) | ✅ **PROVADO REAL E2E 2026-07-15** (role concedida → witness pago gen `2659d78b`, `engine=veo-vertex`, 720×1280 9:16 8s, identidade preservada Read+Vision MCP, **267 mco** exatos 4263→3996, asset `bb0ec719`, nó `4e8902d2`). code-complete + `/security-review` (1 HIGH SSRF FECHADO) · 584 testes · a chave `AQ.` do Sovereign é Gemini API mas o trial GCP só cobre o Vertex (429 na AI Studio, documentado no README do repo GabrielAI). O pipeline local usa gcloud ADC; servidor usa service account. Auth SA JWT RS256→token (WebCrypto), custo Vertex 267 mco (0,15/s), poll fetchPredictOperation, UI de colar o JSON no pool. | 🔒 **Sovereign:** criar service account no projeto `gabrielai-veo` (role Vertex AI User) → JSON → cadastrar no pool nomeado. Depois: `npx supabase functions deploy canvas-execute veo-poll` + `bun run build` + witness pago com o crédito Vertex real |
> 12	| 1 | **Vídeo com avatar/referências no Spaces (Veo 3.1)** — Amendment 25, FR-SPACES-086..091 | ✅ **PROVADO E2E EM PROD 2026-07-14** — deploy (Sovereign) + build (feito) + smoke **12/12** + **witness pago** (gen `02994319`, 720×1280 9:16 8s, **178 mco exatos** 4441→4263, **identidade facial preservada** Vision QA ocular; failover GabrielAI-429→legada funcionou) · nó malha `ccd5dba5` | ⚠️ **OTD-SPACES-046 aberta**: chave nova "GabrielAI" (a do Vertex) com prepaid AI Studio ZERADO (429); o witness rodou na chave legada via failover. Sovereign decide se recarrega a nova em ai.studio/projects |
> 13	| 2 | **Nó de Cadência no Spaces — "além do ManyChat"** (diretiva 2026-07-14) — cadência + automação conversacional p/ TODOS os usuários, BYOK obrigatório, encaixado nos trilhos vivos (autopilot · sequences/nurture-dispatch · scheduled_posts), sem reconstruir | ✅ **BoK 9/9 SELADA 2026-07-15** (`4602b0f`, nó `d0b4fdc8`) — 10 docs + Pattern Conformance (12y/5d/4na); ESTENDE `autopilot_plans` + roteia o tick por `plan_kind` (zero pg_cron novo), reusa `scheduled_posts`/`sequences`/`nurture-dispatch`; inbound IG PROBE-GATED · **✅ Fatia 1 SHIPPADA 2026-07-15** (`6b5412a`, nó `c994c363`): migration `20260716120000` aplicada+verificada · `cadence-plan`/`cadence-run`/tick roteado deployados · `/security-review` NO FINDINGS · smoke 7/7 · build · crítico pegou 2 bugs born-dead pré-deploy | ⏳ Falta: **witness E2E de despacho** (arm→scheduled_posts, via throwaway/UI p/ não publicar real) + Fatia 2 inbound IG (PROBE-GATED FM-CAD-02) |
> 14	| 3 | **Enxame Sensorial-Preditivo (`predictive-swarm`)** — diretiva 2026-07-14, executar **após** o loop atual. Engine de QA sensorial/psicoacústico: design·cinema·marketing como veículos sensoriais integrados. 3 superfícies MCP: `swarm.initialize_sensory_simulation` (enxames paralelos pontuam deriva de percepção) · `vision.parse_sensory_gate` (Tier 1 varredura periférica CPU-bound / pop-out da Feature Integration Theory → Tier 2 foveal só com sinal de alto valor; expande a "Essência Humana") · `mesh.consolidate_sensory_insight` (traços cognitivos → `mcorch_nodes`/`mcorch_edges`, sem PII bruta, proveniência estrita). Gates duros: telemetria+medição por execução atômica · cobrança SÓ via `deduct_mco_coins` per-tenant (ES256 JWKS contra o `sub`) · hard-fail 402/501 estruturado. Fecha com dashboard 🔄 SYNC UPDATE | ✅ **BoK 9/9 SELADA 2026-07-15** (`dc263fc`, nó `485c0f6e`) — 11 docs + Pattern Conformance (15y/6d/0na); MCP molde vision-mcp (ES256 JWKS), 3 superfícies (initialize/parse-gate Tier1 model-free→Tier2 foveal/consolidate), honesto por construção (score=predição, verdade=`creative_metrics.revenue_cents`) · **✅ Fatia 1 SHIPPADA 2026-07-15** (`65a537b`, nó `9ecba7fa`): Tier 1 gates (loudness ffmpeg + contraste WCAG/APCA + verdict) + tool `vision.parse_sensory_gate` VIVOS no container `mcorch_vision_mcp` (healthy, /health anuncia) · crítico pegou 2 blockers (ffmpeg ausente + SSRF redirect) → fechados + hardened · tsc 0 · vitest 121/121 | ⏳ Falta: `swarm:read` no CHECK do PAT allowlist (migration Fatia 2) p/ PAT externo alcançar; Fatia 2 (fan-out/job store) + Fatia 3 (retrieval) |
> 15	| 4 | **AI Act Art. 50(2)** — marcação machine-readable de conteúdo sintético (imagem Nano Banana · vídeo HyperFrames · voz Qwen3) publicado em redes | ✅ **Escopo decidido (3 camadas) + BoK 9/9 SELADA 2026-07-15** (blueprint `531e2b0` + suite `c569416`, nó `825088c0`): C2PA (c2pa-rs) + watermark invisível (TrustMark/VideoSeal/AudioSeal) + metadata IPTC (ExifTool) — todas open-source comercial-safe USD=0; integra no spine `creative_assets` (5 colunas aditivas). Pattern Conformance 12/3/6. | ✅ Gate Closed-Loop ABERTO. **Código = fatia futura com GO Sovereign** (prazo AI Act **2026-08-02**, multa Art.99 €15M/3%) |
> 16	| 5 | **landing-factory** — fábrica de landing pages AUTO-OTIMIZÁVEIS (loop CRO governado), beachhead do norte "agência dentro da plataforma" (2 vídeos Maestros da IA); build → publish → instrumenta PostHog → reverte-se-piora | ✅ **BoK 9/9 SELADA 2026-07-16** (blueprint deepsearch v0.2 + suite `11a5adb`, seal `b65e94b1`; MR14→BR18→PR18→FR20; Pattern Conformance 15/5/1). Decisões Owner: Open Design **v0.10.0 pinado** (single-file export não existe upstream #368) → **asset-bundler próprio** é o P0; hosting **`gcrux.com`** (domínio separado cookie-isolado, nunca `*.mcorch.com`); WordPress-page-first; PostHog self-host/BYOK. **Gate Closed-Loop ABERTO**. | ⏳ **Fatia 1 = código do `landing-bundler`** (inlina img/fonts/@import → data:); registrar wildcard `*.gcrux.com`; OTD-LF-001/003/014 + gate CRO 95% |
> 17	
> 18	**Sprint v6.100.0 — Assets: seletor de formato + pré-visualização fiel + modal responsivo (2026-07-14)** — diretiva Sovereign "UI ruim nos assets + previsualização perfeita por tipo". Amendment 21 (FR-SPACES-075..078) + SOP; `format-specs.ts` SSOT (números do seed channel_profiles, paridade 15/15); `PublicationPreview` 10 chromes fiéis (Reels/Stories/Short 9:16 + Feed 4:5/1:1 + Carrossel + Pin 2:3 + link-card + YT vídeo/comunidade + text-post, render 17/17); `AssetDetailDialog` picker + preview publicando imagem+vídeo via publish-space-asset; modal mobile-app-like (Vision QA pegou grid blowout); inspector do canvas reusa o preview. 4 commits `56bf601..0f543af` · tsc 0 · eslint 0 · +32 testes · SEAL ALLOWED (7/7) · malha 9107 · nó `66952b93`. **Próximo:** OTD-SPACES-044 (carrossel IG agendado) · OTD-SPACES-043 (reframe server-side p/ pixel-parity) · trilhos Stories/YT-comunidade (app-audit).
> 19	
> 20	**Sprint v6.99.0 — Motor Viral Quality + ASR self-host + pool multi-key BYOK (2026-07-14)** — repurpose completo (detector Hormozi + overlay motion-graphic, 3 shorts EP01 provados prod); ASR whisper.cpp US$0 + reconciliação roteiro-autoritativa; rota host-media (206 seek); pool multi-key BYOK (Amendment 20) p/ mineração a ~US$0; estratégia de cadência v1. 6 commits `d4972c7..623fad9` · /security-review NO FINDINGS ×4 · SEAL ALLOWED (8/8) · malha 9105 · nó `d98767ea`. **Pendente Sovereign:** aplicar migration pool + deploy canvas-execute + 3 chaves Gmail + aprovar cadência + GO publicar EP01 no YouTube.
> 21	
> 22	**Sprint v6.98.0 — YouTube Studio (Fatia 1) + front-door host-local do Repurpose (2026-07-13)** — sessão interativa "colocar a ferramenta pra funcionar" com o Usuário Zero. **(1)** Painel `/dashboard/youtube` (`youtube-data` lê vídeos+métricas Data v3+Analytics v2, token per-user server-side; escopos alinhados aos 3 registrados no Google, analytics adiado até habilitar a YouTube Analytics API; mapa API exaustivo 13rec/175props/52metrics/33ações via workflow multi-agente + Pattern Conformance 21 padrões + SOP). **(2)** Front-door host-local do Repurpose **admin-only** `/dashboard/repurpose`: o master (documentário 1,3GB) vai pro **disco do host** furando o cap de 50MB do Supabase free; `host-upload-server` (loopback 3220, nginx `/api/host-upload`) recebe **upload chunked** de 80MB furando o cap de 100MB do Cloudflare; JWT+admin-gate+streaming; worker lê `bucket=local` realpath-contido **sem copiar 1,3GB**. **yt-dlp do host CONFIRMADO bloqueado** pelo YouTube (bot-check no IP de datacenter). **(3)** fix legenda drawtext (truncagem por bytes-extra UTF-8 → padding). **EP01 real 1,3GB → 5 shorts 9:16 (1080×1920) provados por Vision QA** (reframe centralizado + legenda completa). 6 commits `e174988..1730c4a` · `/security-review` **NO FINDINGS ×3** · Phase 5c **SEAL ALLOWED** (8/8) · malha **9102** · handoff `9f7b191a`. **Pendente (próxima):** cadência TikTok com os 5 cortes (sai **privada até a auditoria de rebranding aprovar**) + manual LinkedIn/IG · reconectar YouTube (test-user) + habilitar YouTube Analytics API p/ métricas · reframe subject-aware (OTD-VR-002) p/ planos letterboxed · BoK youtube-studio 9/9. **Lições:** (a) Vision QA em mídia REAL é o detector honesto — pegou legenda truncada que passou em toda checagem estrutural (5 clips 9:16, durações exatas) mas estava visualmente cortada; (b) caps de plataforma (Supabase 50MB, Cloudflare 100MB) exigem furá-los materialmente (host-disk + chunked), não assumir; (c) o gate de segurança do harness bloqueou editar nginx de produção — respeitei (Lei 4), o Sovereign colou o bloco, eu validei (`nginx -t`) + reload + provei a rota E2E.
> 23	
> 24	**Sprint v6.97.0 — Motor de repurpose de vídeo: 1 master → N shorts + carrossel IG (2026-07-12)** — diretiva Sovereign "construa a metade que falta reusando a que existe": o MCORCH distribuía mas não produzia cortes. Sessão-maratona interativa (Sovereign aplicou 3 migrations ao vivo + testou cada gate). **BoK-first (Closed-Loop):** blueprint `docs/bok/video-repurpose/` fundamentado em 10 pointers verificados file:line + no mapa do repo `gabrielZarattini/GabrielAI` (o INVERSO — N takes Veo→1 master; fonte do master + schema de metadados + filosofia data-driven). Correções ao snapshot: segmenter=**FR-CP-012** (não OTD-CP-011); OTD-CP-009 fechada (imagem); youtube Pilar I=montagem; carrossel existente=PDF/LinkedIn. **(Fatia 1 VIVA)** `source_module='external'` + `ingest-external-asset` owner-scoped + smoke 5/5. **(Fatia 2 VIVA E2E)** worker `video-repurpose-bridge` + `segment-core` (trim frame-accurate + reframe 16:9→9:16/1:1 center-safe + legenda queimada; guarda OTD-VR-006 no read-time); **3 clipes reais provados por Vision QA** (timestamp confirma o trim). **(Fatia 3 E2E provada)** `carousel-core` (key-frames→slides 4:5) + branch `media_type=CAROUSEL` no publish-social + seam `publish-space-carousel`; **3 slides reais**. **Distribuição reusada:** cortes/slides viram `creative_assets` que o nó "Publicar em Rede Social" (**OTD-SPACES-036** `space_publish_variants`, também landado) consome. **Witness LoRA** bloqueado só em crédito Replicate BYOK (plumbing provado). Rail 100% grátis US$ 0 · `/security-review` **NO FINDINGS ×3** · Phase 5c **SEAL ALLOWED** (8/8) · mesh **9097** · handoff `f050959c` · 6 commits `ac5ca86..831f5cc`. **Pendente (ação Sovereign):** deploy Fatia 3 (`npx supabase functions deploy video-repurpose-run publish-social publish-space-carousel`) · subir master real do EP01 via Fatia 1 → rodar worker → ver cortes+carrossel do documentário real · auditoria de app IG/TikTok destrava o publish real. **Próximas fatias:** 4=mapeador metadado→legenda nativa+HTML WP · 5=fiar na distribuição E2E. **Lições:** (a) verificar cada pointer materialmente pegou que o repo andou (FR-CP-012, OTD-CP-009 fechada) e que o GabrielAI é o INVERSO — não molde do segmenter; (b) Vision QA em mídia REAL de produção é o único detector honesto (pegou truncamento de legenda longa → OTD-VR-007); (c) reusar os trilhos (o sink que eu tinha acabado de criar) fechou o loop ingest→corte→publicação sem reconstruir nada.
> 25	**Sprint v6.96.0 — Voz clonada self-host COMPLETA + Modo Expressivo + motion design do canvas (2026-07-09/10)** — sessão-maratona interativa (Sovereign testando ao vivo; 13 commits `578f02e..eb422fd`). **(1) Rail de voz US$ 0 VIVO** no nó Clone de Voz (OTD-VOICE-001 fechada por veredito auditivo): Qwen3-TTS 0.6B+1.7B no host · fila `video_renders` engine `qwen3-voice` · worker `voice-bridge.service` com heartbeat anti-reaper (bug witnessed: reaper de 45min re-claimava job vivo) · multi-amostra FR-SPACES-059 (principal + 5 clipes ≤7s, ffprobe fail-closed) · perfil ICL `.qvoice` + `-ref.wav` (x-vector reprovado pelo ouvido; grafts são model-bound) · smoke **12/12**. **(2) Modo Expressivo**: 1.7B + assets `.expr`, witness RTF 13,9 "composed 3 spans", normalizador da sintaxe do Sovereign (`{happy}`/`<#0.5#>`/`(gasps)` → gramática real; tag desconhecida NUNCA falada), roteiro 20k, "Gerar roteiro com IA" (select pela regra perene). **(3) Reparos**: reunion migration `20260710170000` (drift de 07/jul derrubara `avatar-studio` do guard — áudio fora do spine EM SILÊNCIO; anticorpo: SEMPRE checar `error` de `supabase.rpc`, ele não lança) + aba Áudios na Biblioteca + Histórico `generate_voice` + backfills. **(4) Motion design Amendment 19**: motion=telemetria (processing/transmitting/established), FlowEdge com partículas, 1 seam p/ 12 node types, frame-diff provou. **(5) Regra perene BYOK** (`useConfiguredProviders` da view mascarada; memória `feedback_byok_only_available_options`) + ElevenLabs IVC multi-amostra + **F5-TTS/Fish Speech REJEITADOS** (pesos non-commercial). 2× `/security-review` NO FINDINGS · Phase 5c **SEAL ALLOWED** (15/15) · mesh **9094** · handoff `8c1f0e7b`. **Lições:** (a) o aside do /security-review pegou enum CHECK errado no INSERT do histórico — reviewer independente paga sempre; (b) o WAF do Management API devolve HTML-challenge (não JSON-error) em DDL grande com `DO $$` — gate de apply DEVE validar o corpo + prova material; (c) fail-soft sem log = falso-sucesso de um dia inteiro.
> 26	**Sprint v6.83.1 — Fix Assets: exibição de mídia privada owner-scoped em TODO o ecossistema (2026-07-03)** — diretiva direta do Sovereign ("a maioria das mídias sumiu; garanta E2E que aparecem em todos os lugares"). **Diagnóstico refutou a hipótese de lixo de smoke (Lei 1):** os 90 assets são TODOS do User 0 (`ada39fae`, saldo 4571). Causa real: buckets viraram privados+owner-scoped (correto — fechou enumeração cross-tenant), mas o app resolvia URL **pública** (400 em bucket privado) e o cliente não assinava objeto com prefixo ≠ uid (`owner=NULL` service-role). Escopo: 84 creative_assets + 68 vm_canvas_executions + 32 graphs + 1 space. **Fix:** migration `20260703030000` (3 policies owner-scoped 4-rotas `=auth.uid()` + triggers de id server-side INSERT+UPDATE anti-claim/PK-swap + data-repair is_public) + fix bug vivo `canvas-execute:555` + lib `asset-url.ts` (`toDisplayUrl`/`useDisplayUrl` re-assina no render, cura pública-morta E assinada-expirada) + `<StorageImg/Video/Audio>` em **13 superfícies** + `resolveAssetUrl` chaveia pelo bucket real. **Segurança:** `/security-review` independente **CLOSED 9/10** — achou e me fez fechar 1 HIGH cross-tenant que a 1ª versão introduziu (claim via `vm_canvas_projects` id-squat + PK-swap). Cross-tenant **BLOCKED ao vivo** (throwaway: sign/claim/PK-swap). **Prova:** signing antes FAIL→SIGNED 200 · tsc 0 · build+deploy · deploy canvas-execute · **E2E local determinístico: Biblioteca 67/71 imgs+19 vídeos, Canvas 17/17+4 vídeos, 0 dead-public, Vision-QA APROVADO ×2 + confirmação ocular (90 assets)** · Phase 5c **SEAL ALLOWED** (6/6) · mesh **9047** · handoff `6e2b32b2` · commits `6e5e005`/`459cd25`. **Lição:** o classificador do harness bloqueou o apply de DDL sob /loop genérico → respeitei o gate (Lei 4), o Sovereign rodou `!`, e o `/security-review` ANTES do apply-final pegou meu próprio HIGH — o gate de RLS provou seu valor de novo (FMEA-011). SOP `private-bucket-asset-signing.md`.
> 27	
> 28	**Sprint v6.83.0 — Spaces 2d compose VIVO E2E: drift do Higgsfield resolvido (OTD-SPACES-003) (2026-07-03)** — loop autônomo fechou a única pendência real da Fase 2d. **Nunca chutei semântica de provider (Lei 1):** sonda 422 zero-custo (type-poisoning revela schema Pydantic sem enfileirar job pago) provou que `soul/compose` **nunca existiu** — path é `soul/{mode}` (mode literal `reference|character|standard`), refs exigem `custom_reference_id` cunhado async (`/v1/custom-references`, fila de minutos, incompatível com janela sync). **Fix:** compose migrado p/ **OpenRouter Nano Banana multimodal** (motor da 2b já provado), custo re-pinado 18→10 (o 18 precificava ficção), BYOK openrouter fail-closed (gate C4), `generateHiggsfield` throw honesto p/ compose (OTD-SPACES-005). **Achado colateral P1:** `canvas-assets` privado desde a criação → `getPublicUrl` = URLs 400 mortas em 4 call-sites → tudo assina (server 7d, refs client 365d). **Anticorpo:** `smoke-higgsfield-schema.ts` 7/7 pina o contrato vivo (drift = exit 1). **Prova:** smoke Spaces **31/31** (C3 refund+pinned 10 · C4 402 pré-débito) · vitest **398** · tsc 0 · deno check · **E2E pago** (space `4909d024`, generation `cc789ada` done, PNG 919KB URL assinada HTTP 200, saldo 4581→4571 exato, Vision QA high) · review 3-lentes inline (Opus, após créditos Fable esgotarem) · Phase 5c **SEAL ALLOWED** (6/6) · mesh **9045** · handoff `8733cab`. **Direção Sovereign registrada — OTD-SPACES-007:** conector per-user do **MCP oficial Higgsfield** (`mcp.higgsfield.ai`; Bearer BYOK=catálogo, conta=OAuth com DCR+refresh provados) → 30+ modelos auto-descritivos atrás de 1 integração; BoK-gated antes do código. **Pending:** OTD-SPACES-004/006/007 · Workflow Apps/FX/multi-page (Fase 2) · voz clonada (biometria) · app-registration YT/TikTok · Universe cutover. **Lição:** a sonda de schema por payload-inválido é a técnica canônica p/ fechar drift de provider externo sem gastar — e vira sentinel permanente, não one-off.
> 29	
> 30	**Sprint v6.82.1 — Sprint Spaces 1b→2d SELADO: canvas pago com 4 modalidades (2026-07-02)** — 6 iterações autônomas do loop pós-GO Sovereign. **(1b LIVE)** GO executado: migration `20260702190000` aplicada+registrada+provada (DDL 8/8) · **drift do ledger de migrations FECHADO** (10 registradas por sonda DDL, audit exit 0) · fix ordem de guards · smoke 13/13 · E2E pago magic_prompt (saldo −1 exato, Vision QA high). **(2a vídeo)** ledger-first no submit + webhook hash-safe (SHA-256-only, migration `20260702210000`) + supressão do deduct legado; review **NO P0/HIGH** (MEDIUM+2 LOW corrigidos); **canvas→vídeo REAL** MP4 11.3MB via webhook Higgsfield, saldo −40 exato, Vision QA no vídeo (space-demo `51b229cf` vivo). **(2b)** References picker upload real, cap honesto 4 = verdade do server. **(2c voz)** 8 vozes stock via `tts-speak` com JWT do usuário; review **APPROVED** + F1 pinado (gate A4); WAV 9s real, saldo −2 exato (space-demo `1d77b500` vivo). **(2d composer)** código-completo + **ACHADO**: Higgsfield dropou `mode=compose` → compose legado do Canvas Studio quebrado por API drift; estorno integral provado; **OTD-SPACES-003**. **Prova:** smoke **30/30** · vitest **398** · tsc 0 · SOPs S14-S32 ANTES do código · Phase 5c **SEAL ALLOWED** · mesh **9043** · handoff `f85d3cf4`. **Pending:** OTD-SPACES-001/002/003 · Workflow Apps/FX/multi-page (Fase 2) · voz clonada (biometria, Fila) · app-registration YT/TikTok (Fila). **Lição:** parar no erro material do provider (compose 422) em vez de chutar semântica = Lei 1 aplicada a APIs externas; e o pin de custo contra payload forjado (F1/A4/C3) virou padrão obrigatório de todo custo declarado.
> 31	
> 32	**Sprint v6.76.0 — Spaces Fase 1b: execução runGraph + ledger generations CÓDIGO-COMPLETO, apply em prod GATED (2026-07-02)** — loop re-armado, ciclo fechado completo até o portão de produção: mapeamento ultracode `wf_b4abf175-410` (24 contradições BoK↔código resolvidas) → SOP Lei 2 `spaces-graph-execution.md` (S1-S13) → migration `20260702190000` (ledger `generations` + RPCs atômicas `begin/finalize_space_generation` service-role-only, **NÃO aplicada**) → branch ledger-first exclusivo no `canvas-execute` (422 pré-débito · cap IN-list · `refund_pending` honesto · done-fallback) → client `useGenerationLedger`/clusters/Estimar+Rodar → **/security-review independente SOUND** (4 achados corrigidos, incl. `self-heal-spaces.sh`). **Prova:** vitest **17/17** (+ mirror-parity mecânico) · deno check · eslint 0 · tsc 0 · Phase 5c **SEAL ALLOWED** (11/11) · mesh **9034** · handoff `209cbcd8`. **🔒 Pendente GO Sovereign:** apply da migration (classificador negou 4× sob modo auto — `! bash scripts/qa/apply-spaces-1b-migration.sh` destrava) → deploy fn → smoke 8 gates → E2E+Vision QA. **Achado:** 6 migrations `202607*` aplicadas-mas-não-registradas no ledger remoto (db push INSEGURO). **Lição:** o portão de permissão do harness é um Owner-gate real — 4 recusas respeitadas sem contorno é o protocolo de Lei 4 funcionando.
> 33	
> 34	**Sprint v6.75.0 — loop it.2-3 (selo final): reward_weights config-as-data + Spaces Fase 1a canvas vivo (2026-07-02)** — **(it.2)** NFR-VA-010: pesos do reward do Viral Autopilot viram DADO por plano (`autopilot_plans.reward_weights` jsonb; `resolveRewardConfig` valida+normaliza, inválido→fail-safe; auditoria `weights_source`). /security-review NO FINDINGS · smoke **16/16** (`6058e78`). **(it.3)** Spaces Fase 1a: **canvas infinito 72/28 VIVO** em `/dashboard/spaces` (home + `:id`), Spotlight 26 tipos, conexão tipada, persistência `spaces.graph` jsonb RLS-own — zero execução/ledger (Fase 1b depois). /security-review NO FINDINGS · vitest 5/5 · **E2E browser User 0 (DB graph=2 nós) + Vision-QA APROVADO** (`9ea6ac0`). **Prova:** tsc 0 · Phase 5c **SEAL ALLOWED** (6/6) · mesh **9033** · handoff `13fd6fe0`. **Loop PARADO** (janela alta + Fatia 1b grande à frente). **Pending:** Spaces Fase 1b (`runGraph`→`canvas-execute`+ledger+clusters — fecha canvas→conteúdo pago) · Universe cutover (Sovereign) · V4-2 (experiment-gated). **Lição:** selar antes de uma Fatia grande protege trabalho durável sem desperdício (Lei 3 calibrada).
> 35	
> 36	**Sprint v6.74.0 — spaces-evolution BoK 9/9 + loop re-armado it.1: B5 Pauta de Receita (2026-07-02)** — **(1)** A pedido direto do Sovereign, a única suíte BoK incompleta foi fechada ANTES de continuar o roadmap: 06/07/08 grounded no scaffold Phase 0 promovido + **Pattern Conformance §11** (4 yes · 8 deferred nomeados · 9 n-a) + renames canônicos → **25/25 suítes verdes**, seal `8f5fd3fd` DERIVES_FROM viralmind, **BoK Gate do Spaces Fase 1 ABERTO** (`4a8fee0`). Verificação mecânica corrigiu 2 imprecisões pré-commit (Lei 1). **(2)** Loop autônomo re-armado (prompt canônico) — it.1 = **B5 Pauta de Receita FR-VA-031 (HITL)**: SOP Lei 2 → ranking puro vitest 7/7 → seção na AutopilotPage → browser-verify User 0 (linha #1 ↔ `content_library e27a09e7`) → **Vision-QA APROVADO high** (`367db9b`). **Prova:** tsc 0 · Phase 5c **SEAL ALLOWED** (8/8) · mesh **9032** · handoff `10d8c70b`. ⚠️ Workflows quota-blocked até 4:20am → execução inline. **Pending:** `reward_weights` config-as-data (NFR-VA-010) · Spaces Fase 1 MVP · V4-2 · witness G7 imagem multi-canal no próximo ciclo pago.
> 37	
> 38	**Sprint v6.73.4 — Loop it.4 (selo final): B4 EWMA multi-ciclo no analyze (2026-07-02)** — reward sobre janela M=5 ciclos peso 0.5^idade (anti-thrash; janela lembra, plano virgem não inventa; auditoria `reward_vector.ewma`). Smoke **13/13** (L7: evidência acumulada 7 vence recente 3 — single-cycle flipava) · deployado · SOP amendada · Phase 5c SEAL ALLOWED · mesh **9023** · handoff `1ddd4e86`. **Loop PARADO (janela ~95%).** Restam desbloqueados: B5 pauta de receita (FR-VA-031) · V4-2 · `reward_weights` config-as-data.
> 39	
> 40	**Sprint v6.73.3 — Loop it.2-3: Vision-gate mecânico nos 2 harnesses (2026-07-02)** — diretiva 2026-06-26 fechada: `audit-canvas-ui` (veredito APROVADO obrigatório, fail-closed sem PAT, print público `dist/canvas_e2e_latest.png` REMOVIDO — era dashboard logado em URL pública) + `e2e-user-zero` (`lib/vision-gate.ts`, REPROVADO→Finding P1/ux→NO-GO, fecha heurística deferida (c)). **Prova:** run E2E prod APROVADO high cost 0 · **adversarial: PNG branco→REPROVADO→P1** · vitest 6/6 · tsc 0 · Phase 5c SEAL ALLOWED · mesh **9022** · handoff `8ddca90b`. Commits `8a41457`/`e511862`/`adf849b`. **Pending:** B4 EWMA · B5 pauta de receita · V4-2.
> 41	
> 42	**Sprint v6.73.2 — Loop it.1: render-decoupling resolvido por arquitetura + G7 imagem-pilar + fan-out hygiene (2026-07-02)** — iteração 1 do loop re-armado (instância standby assumiu após o stop limpo da primária v6.73.1; anticorpo de concorrência: Monitor 30s + cessão enquanto a primária vivia — zero colisão). **(1) Achado material:** o item "render-decoupling YT/TikTok" da charter era STALE — o ciclo pago `77e02fca` já produzia `channel_variants` de vídeo `reused_master` p/ 7 canais (1 master 9:16/ciclo via reshaper + kick do video-bridge); último salto = OAuth/app-registration (Fila). **(2) Fatia G7** (`d16ca88`): imagem-pilar resolvida por âncora `metadata.pillar_run_id` (fix do `gap` das 5 surfaces de imagem — autopilot nunca cunha campaign; `campaigns` é FK) + fallback de campanha preservado. **(3) Fan-out hygiene** (`autopilot-run`): plataformas sem step não pré-debitam (antes: 10 mco em run knowledge_mesh-only) + telemetria. **Prova:** SOPs Lei 2 amendadas ANTES do código · deno check 3/3 · tsc 0 · 3 fns deployadas · smoke-reframe-image **18/18** (cenário B campaign-NULL draft-only) · regressão reshape-pillar PASS · Phase 5c **SEAL ALLOWED** (4/4) · mesh **9021** · handoff `b31c1336`. **Pending:** próximo ciclo pago testemunha imagem multi-canal `ready` em prod · confirmar sumiço dos 4 scheduled_posts do ciclo (limpeza manual?) · B4 EWMA · B5 pauta de receita · V4-2 experimento · wirar Vision QA em audit-canvas-ui/e2e. **Lição:** provar o estado no DB vivo ANTES de codar matou uma fatia inteira planejada errada (re-render por sub-run) e revelou os 2 bugs reais que valiam o código.
> 43	
> 44	**Sprint v6.53.0 — Doutrina Agêntica AGI→ASI + Learning & Adaptation + analytics honesto (2026-06-27)** — sessão-maratona multi-arco. **7 commits.** **(1)** Doutrina `agentic-vision.md` (21 padrões × maturidade + tese Via 4-produto/Via 3-micro) + **Pattern Conformance gate vinculante** no CLAUDE.md §1 + BoK `agentic-governance` 10/10 (seal `34748570`) + 2 docs stale deprecados. **(2)** **Collective Efficiency Ledger** (`81210ab`) — VIEW security_invoker + RPC service-role medem mco/resultado anti-Goodhart (G6 isolamento provado; rollup real 334s vs 2.4s). **(3)** **Learning & Adaptation** (o único padrão fraco) atacado: nervo sensorial (`publication_metrics` + coletor fail-soft IG/FB + painel "Por Publicação" browser-provado) + reward multi-métrica brand-first (mata `totalClicks` Goodhart, prova policy `7d9856d0`) + realocação ε-greedy (`1371094`/`47474ac`). **(4)** Analytics honesto — demo-kill (`b6abff1`) + zeramento dos perfis sociais antigos (marca **Gabriel AI**/**@gabrielOrchAI** começam do zero). **Prova:** tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8971** · handoff `326949f1`. **Pending:** re-OAuth IG insights (destrava o payoff visível) · B4 EWMA · B5 pauta de receita · V4-2 experimento · postback ML · emenda BoK post-engine (YT/TikTok). **Lição:** "não avançamos apesar do dev incrível" = o motor aprendia sobre **placar em branco**; medir o desfecho real é o que faz capacidade virar avanço.
> 45	
> 46	**Sprint v6.52.0 — Gabriel AI mood board + Vision QA gate + 1º ciclo pago de vídeo 9:16 witnessed + billing/CTA fixes + virada brand-persona (2026-06-26)** — sessão-maratona "faça tudo", Usuário 00 sobre Usuário 0. **6 commits.** **(1)** Ciclo pago de vídeo 9:16 witnessed E2E (render real `8b0787e0` 1080×1920) + 2 bugs de receita (`df7505b`): billing cobrava vídeo por sub-run mas só article-flow renderiza → fix por `nVideoRuns`+refund; CTA-leak `mcorch.com` texto-puro → guard bare-text nos 2 formatos. **LinkedIn cadence E2E** (post real `urn:li:share:7476089362896732160`). **(2)** Virada **brand-persona Gabriel AI/CCIO** (plano produto pausado) + blueprint fundamentado YouTube/TikTok (`58e0389`, infra ~90% reusável, gates audit Sovereign). **(3)** Nó `characterReference` vira **mood-board multi-foto** (`549e4dd`) + mood board Gabriel AI gerado E2E (4 retratos face-consistentes Vision-QA-gated + 2 animações DoP) no projeto `b57a59f7`. **(4)** **Vision QA** gate visual sempre-on + canvas `prompt.length` hardening (`a482132`). **Prova:** tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8969** · handoff `5501a101`. **Pending:** emenda BoK post-engine + 3 branches OAuth YT/TikTok (audit = ação Sovereign) · URLs referência 7-dias→públicas (persona durável) · wirar Vision QA dentro de `audit-canvas-ui.ts`/e2e · animações DoP finalizam async · postback ML real. **Lição:** o witness de um ciclo pago expôs 2 bugs de billing/atribuição invisíveis no código estático — rodar o fluxo real (Lei 1) é o melhor detector.
> 47	
> 48	**Sprint v6.51.0 — Fatia 2 vídeo→Instagram Reel PROVADO E2E + Notificações P0 + malha criativa cross-módulo + receita destravada (2026-06-25)** — sessão-maratona "força total pelo primeiro R$", Usuário 00 sobre Usuário 0. **9 commits.** **(1) Receita** (`1ad04c5`): cron auto-publish morto (`/var/log` inacessível)→durável+telemetria; link **meli.la assinado** publicado (sale-attributable, Roborock+Family Hub); CTA-leak fechado; 2 posts injection removidos do LinkedIn. **(2) Canvas white-screen fix** (`46f18ca`): `MODEL_INFO[id].coinCost` em modelId fora do catálogo → `getImageModelInfo`/`getVideoModelInfo` com fallback; **verificação por browser real** (agent-browser+preview+sessão injetada) virou diretiva durável. **(3) Malha cross-módulo:** asset clicável→handoff Canvas (`8c00f88`); white-label HyperFrames nginx sub_filter (`5d58b15`); Biblioteca scroll+filtro-data+metadados (`8fdb435`); starter MCORCH 9:16 **lint 0/0** substitui demo HeyGen (`3efbe75`, AskUserQuestion). **(4) Fatia 2 — vídeo→Reel PROVADO E2E** (`9d9ec03`/`3be06ee`): User 0 **já conectado** (IG `magicorch` MEDIA_CREATOR); `publish-social` IG via `graph.instagram.com`+REELS+id do `/me` (stored id app-scoped rejeitava 100/33). **Reel real: `instagram.com/reel/DaBtVAQkiuz`.** **(5) P0 Notificações** (`bfb0ba3`): sino era placeholder morto (badge "3" hardcoded) + nada escrevia na tabela → `useNotifications`+`NotificationBell`+`_shared/notify.ts`+seed 4 eventos; browser badge "5". **Prova:** tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8962** · handoff `468c15dc`. **Pending:** camada **push** (browser/OS — sem infra) · **Fatia 3 faceless long-form** (filosofia Sovereign: vender mostrando produto útil no momento certo, redes=entretenimento não venda) · CF público liberado (404=challenge caiu) mas WP posts são draft + Autopilot dormente → flip wp_status+ativar cadência (GO de gasto) · FB Reel (precisa Page). **Lição:** checar a conexão REAL (Lei 1) revelou que o IG já publicava — o publisher só apontava pro lugar errado.
> 49	
> 50	**Sprint v6.50.0 — HyperFrames editor LIVE + creative_assets spine (Fatia 1 bidirecional) + auth gating + Canvas bug fix (2026-06-25)** — `/handson` → editor HyperFrames → pedidos do Sovereign, sob **ultracode**. **4 arcos:** **(1) Editor HyperFrames VIVO** (`video.mcorch.com`): o servidor oficial `hyperframes preview` (NLE multi-camada) roda como serviço host systemd `video-studio.service` (node v22; achado: `hyperframes preview` é processo standalone → conflito React 19/18 some sem Docker) atrás do vhost SSO-gated, módulo iframe `/dashboard/canvas/video`; contrato `/api` selado dos `.d.ts` (SDD §VS-UI v0.4 + SOP); Sovereign fez os 2 sudo (cert+symlink), provado pela screenshot dele. **(2) Auth gating `?devLogin`** (público só email/senha; param libera Google+Cadastrar). **(3) Bug de perda de nós do Canvas** (race load/save → guard empty-over-nonempty no `useSaveCanvasGraph`) + projeto `63d406fe` recuperado das execuções. **(4) `creative_assets` SPINE** (diretiva "poder das saídas" bidirecional): tabela canônica fina + RPC `register_creative_asset` (SECURITY DEFINER service-role-only idempotente, guard cross-tenant); /security-review SAFE; smoke 5/5; dual-write em video-bridge/canvas-execute/generate-image; backfill 73 assets; UI Biblioteca de Assets `/dashboard/canvas/assets`. **Prova:** tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8960** · handoff `8eb84bce` · 11 commits. **Decisão arquitetural (AskUserQuestion):** híbrido bidirecional (Canvas autora · HyperFrames renderiza [FFmpeg long-form, n8n fez 51s] · Meta/Orquestra publica). **Ordem das fatias decidida:** ~~Fatia 1 creative_assets~~ ✅ → Fatia 2 vídeo→Meta Reels → Fatia 3 faceless long-form nativo (receita n8n 51s, `.claude/context/faceless-pipeline-reference-2026-06-25.md`) → Fatia 4 handoff Canvas↔HyperFrames (`onSelect` da galeria pronto). **Pending:** Fatia 2-4 + produtor `design-bridge` · ⚠️ Sovereign rotacionar chave Gemini + token Telegram do n8n colado. **Lição:** Management API bane UA Python-urllib (1010) → curl; `hyperframes preview` standalone elimina o Docker do plano original.
> 51	
> 52	**Sprint v6.49.0/v6.49.1 — Vídeo viral 9:16 autônomo + motor HyperFrames vivo → Studio blueprint + gap de billing fechado (2026-06-24)** — `/handson` → "fichar o vídeo 9:16 com a UI editor do hyperframer assim como o open design" → sob **ultracode**. **v6.49.0:** decisão Sovereign (AskUserQuestion) = motor HyperFrames + worker single-tenant, alvo Autopilot-primeiro → BoK gate (Amendment v0.2, FR-VA-022..026 + SOP) → **motor HyperFrames VIVO** (`render-core.ts` Playwright+FFmpeg → MP4 9:16 1080×1920 sha256-idêntico NFR-VS-016; worker `video-bridge.ts` systemd active; bucket; edge `poll://`) → integração Autopilot (custo no pré-débito do ciclo OTD-VA-010; E2E real "Roborock S8…" render 9:16, saldo intacto). **v6.49.1:** **(1)** deepsearch do HyperFrames Studio (`ae8b94c5`, Apache-2.0) → flip OTD-VS-005 A→C **módulo-container** (StudioApp zero-props + seam `StudioApiAdapter`; embed in-SPA inviável React 19 vs 18); blueprint `.claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md`. **(2)** gap de billing OTD-VA-010 fechado: crédito compensatório idempotente `refund_autopilot_video_enqueue` (migration `20260624140000`) no fail-open do enqueue (actual otimista contava 12 sem linha → cobrança-sem-valor); smoke **8/8** net-debit-exclui-12. **Prova:** `/security-review` SAFE (motor + billing) · tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8959** · handoff `b42e89f9`. **Pending (próxima):** **Fatia VS-UI** editor Studio módulo-container (API `/api` → container React 19 → `McorchAdapter` → vhost `studio.mcorch.com` [DNS Sovereign] → render-parity gate) · 1º ciclo pago de vídeo witnessed · Unified Canvas 3.5-3.10 · postback ML real · Security BoK suite (diferida). **Lição:** o achado material (orchestrate-content é async → autopilot-run finaliza ANTES dos enqueues) inviabilizou a Option 1 do diretivo e decidiu o design do fix; o deepsearch pré-código achou o seam zero-props que evita forkar a UI HeyGen.
> 53	
> 54	**Sprint v6.48.0 — Viral Autopilot ATIVADO + FR-VA-018 + segurança social-auth + paridade sentinel pt-BR (2026-06-23)** — `/handson` → "vamos com os próximos passos" → "continue" (×N) sob **ultracode** (4 workflows adversariais). 3 arcos. **(1) Viral Autopilot ATIVADO:** heartbeat pg_cron `autopilot-cadence */15` jobid 3 `active` (migration `20260623040000`) + **1º ciclo PAGO real** (cycle `947ef8b5` completed, débito 22/refund 2, saldo 5096→5076, 2 sub-runs `done`) — GO Sovereign respeitado; trap material: produto resolve por `external_id`, não UUID. **(2) FR-VA-018** trend-informed angle: `autopilot-run` lê `vm_trends` (fonte global não-confiável) → gate `sanitizeTrendTitle` (whitelist destrói URLs/payloads + reject de verbos) → DADO inerte; red-team `wf_6cc97c75` pegou MEDIUM (sentinel English-only → injection pt-BR cross-tenant), hardened. **(3) Segurança social-auth** (auditoria per-user): state OAuth **HMAC** fail-closed + janela ts 10min (`_shared/oauth-state.ts`) + `instagram-webhook` **X-Hub-Signature-256**; 8/8 gates. **(4) OTD-VA-018-SENTINEL-PTBR:** 7 famílias pt-BR no Cyber-Sentinel, **0 FP real** em 58 amostras (loop `wf_0459e1c1` → tunei f3/f4/f5), live 403 `score=2` sem regressão do inglês. **Prova:** `/security-review` SAFE múltiplo · tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8954** · handoff `bc175ac9` · 6 commits. **Pending (próxima):** Unified Canvas 3.5-3.10 (gate visual 1920×1080) · mídia viral 9:16 · postback ML real · Security BoK suite (diferida). **Lição:** o sentinel é TRIAGE score≥2 — single-intent passa por design (=inglês), defesa cross-tenant é o gate de fonte; testar FP contra copy real é o make-or-break ao tocar o pipeline vivo.
> ```

## 🤖 Claude *(20:02:57)*


## 🤖 Claude *(20:02:57)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 9802,
  "limit": 400
}
```

> **Tool Result (Read)** - ❌ Error
>
> ```
> File content (27827 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
> ```

## 🤖 Claude *(20:02:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null | head -15; echo \"---GAPS---\"; grep -n -A 8 \"Top 3 Gap\" .claude/context/sprint-priorities.md | head -20",
  "description": "Conte\u00fado de scratch/ + se\u00e7\u00e3o Top 3 Gaps do sprint"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 8
> drwxrwxr-x  2 gcrUX gcrUX 4096 Jun 30 01:44 .
> drwxrwx--- 33 gcrUX gcrUX 4096 Jul 16 16:08 ..
> ---GAPS---
> ```

## 🤖 Claude *(20:03:07)*


## 🤖 Claude *(20:03:08)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n -E \"^## (Pending Actions|GraphRAG State|Infrastructure|Key Files|Session Metrics)\" HANDOFF.md | tail -10",
  "description": "Localizar se\u00e7\u00f5es de cauda do HANDOFF.md"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 9798:## Pending Actions (Commercial Launch)
> 9911:## Infrastructure
> 9958:## GraphRAG State
> 10106:## Key Files
> ```

## 🤖 Claude *(20:03:15)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 9798,
  "limit": 180
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 9798	## Pending Actions (Commercial Launch)
> 9799	
> 9800	### CRITICAL — Must complete before first client
> 9801	
> 9802	🎯. **[✅ ATIVADO + VÍDEO 9:16 AUTÔNOMO — 2026-06-24 · pendente só: editor Studio (módulo-container) + postback ML + publish vertical] Viral Autopilot** — BoK 9/9 selada (`b3398294`). **✅ VÍDEO 9:16 (seal video-9x16-motor-and-autopilot, 2026-06-24):** (C) **RESOLVIDO** — motor HyperFrames determinístico VIVO (Fatia VS-2: `video-bridge.service` render 1080×1920 sha256-idêntico) + integração Autopilot (Fatia VA-V1: `orchestrate-step` enfileira render do ângulo viral REAL, custo no pré-débito do ciclo OTD-VA-010, attach content_library+creative_metrics OTD-VA-014) — provado E2E real (artigo Roborock → render 9:16 → biblioteca, saldo intacto prepaid). BoK Amendment v0.2 (FR-VA-022..026 + SOP `autopilot-video-9x16.md`) + flip OTD-VS-005 A→C (editor = módulo-container open-design, embed in-SPA inviável por React 19/18). `/security-review` SAFE ×2. **Próximo do vídeo:** **editor HyperFrames Studio** (módulo-container: deepsearch da API `@hyperframes/studio` → app React 19 → bridge → módulo frontend → vhost `studio.mcorch.com` [DNS Sovereign]) + **1º ciclo pago de vídeo witnessed** (habilitar `video_enabled` + GO) + (D) postback ML real + publish vertical TikTok/IG/YT (PR-VA-021, OAuth+App Review). **— histórico v6.48.0:** **✅ ATIVAÇÃO (seal autopilot-activation-security-hardening):** (A) heartbeat pg_cron `autopilot-cadence */15` jobid 3 `active` (migration `20260623040000`) + **1º ciclo PAGO real** `947ef8b5` (débito 22/refund 2, saldo 5096→5076) DONE; (B) **FR-VA-018** trend-informed angle com gate de fonte `sanitizeTrendTitle` + paridade pt-BR no sentinel (OTD-VA-018) DONE. Restam só (C) mídia 9:16 + (D) postback ML real. **Motor autônomo R1+R2+R3+R4 COMPLETO e provado zero-cost.** ✅ **Fatia 2 (cadência R2 + loop R3 + UI, commits `686bae3`→`bfd178b`):** SOP Lei 2 `autopilot-cron-identity.md` (OTD-VA-008 fechado) · migrations `20260620120000..120300` (`autopilot_plans`/`autopilot_cycles` FK composta tenant + RPCs `begin`/`finalize_autopilot_cycle` atômicos sob advisory-lock, service-role-only) · 6 edge fns deployadas (`autopilot-run` executor + `-cadence-cron` driver pg_cron + `-analyze` FR-VA-010 + `-collect` FR-VA-008 + `orchestrate-content` FR-VA-016 prepaid + `orchestrate-step` FR-VA-011 inject) · UI `/dashboard/autopilot` (`useAutopilot`+`AutopilotPage`). `/security-review` SAFE 3× · 3 smokes zero-cost (31 gates) · render ocular. **PENDENTE:** **(A)** ⚠️ **ação Sovereign** — ativar o **`pg_cron` schedule** que chama `autopilot-cadence-cron` (a função existe+provada; só o JOB pg_cron é ativação Sovereign-side, `Bearer SB_SECRET_KEY` via Vault) + rodar o **1º ciclo PAGO real** (mco real), gated nos 2 blockers de saída visível diagnosticados na Fatia 1b: **CF WAF skip `/wp-json/*`** + **OpenAI image model access**; **(B)** `fetch-trends`/`vm_trends`→pauta do ângulo viral (FR-VA-018, último item autônomo); **(C)** mídia viral 9:16 + TikTok/IG/YT (fase 2); **(D)** provar postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER). Constraints chave (cravados no código): `N_runs=prod×rede×ab_variants`, imagem no bundle de 10, refund crédito-positivo (NUNCA deduct negativo — anti-mint `20260603220000:45`), FK composta tenant-escopada, analyze inline=prepaid (reserva de 2 só vira actual com dado real).
> 9803	
> 9804	🌌. **[EM ANDAMENTO — Phase Epsilon V9] Unified Sensorial Canvas — Fases 3.5-3.10** — Fases 3.1-3.4 ✅ (scaffold rota/store/shell 72-28 + Code Network R3F InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; E2E ocular nos 3 modos; commits `210b90d`/`d832084`/`4940b4d`/`38d9760`/`769acb1`). **Restam:** **3.5** Sinapses inter-rede (arestas **REAIS** de `mcorch_edges` cruzando código↔memória, lit só no modo Universo — nunca fabricar) · **3.6** fly-to (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.7** layout/perf (`OTD-UCANVAS-PERF` — a query do código leva **~30s** com 2 canvases; considerar Louvain em Web Worker / streaming do grafo / lazy do backdrop) · **3.8** executar a poda do squad-coloring (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`. BoK selada (PR-025 · FR-043..049 · NFR-023/024 · SDD §9). **3 páginas legadas (matrix/memory/core-fable) preservadas como backup até 3.9.**
> 9805	
> 9806	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 9807	
> 9808	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 9809	
> 9810	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 9811	
> 9812	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 9813	
> 9814	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 9815	
> 9816	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 9817	
> 9818	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 9819	
> 9820	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 9821	
> 9822	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 9823	
> 9824	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 9825	   ```bash
> 9826	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 9827	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 9828	   ```
> 9829	
> 9830	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 9831	
> 9832	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 9833	
> 9834	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 9835	
> 9836	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 9837	
> 9838	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 9839	
> 9840	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 9841	
> 9842	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 9843	
> 9844	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 9845	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 9846	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 9847	
> 9848	### SOCIAL — Next steps
> 9849	
> 9850	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 9851	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 9852	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 9853	
> 9854	### NON-CRITICAL
> 9855	
> 9856	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 9857	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 9858	- `browserslist` — ✅ updated (2026-04-26)
> 9859	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 9860	
> 9861	### GITNEXUS MCP — Next steps
> 9862	
> 9863	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 9864	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 9865	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 9866	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 9867	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 9868	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 9869	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 9870	
> 9871	### PHASE EPSILON — Next iterations
> 9872	
> 9873	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 9874	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 9875	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 9876	
> 9877	### CORE — Next iterations
> 9878	
> 9879	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 9880	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 9881	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 9882	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 9883	
> 9884	### PHASE DELTA — Next iterations
> 9885	
> 9886	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 9887	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 9888	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 9889	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 9890	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 9891	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 9892	
> 9893	### USUÁRIO ZERO — Checklist de validação
> 9894	
> 9895	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 9896	- ✅ Stripe sandbox secrets no vault
> 9897	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 9898	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 9899	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 9900	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 9901	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 9902	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 9903	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 9904	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 9905	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 9906	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 9907	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 9908	
> 9909	---
> 9910	
> 9911	## Infrastructure
> 9912	
> 9913	| Service | Container | Port | Status |
> 9914	|---------|-----------|------|--------|
> 9915	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 9916	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 9917	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 9918	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 9919	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 9920	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 9921	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 9922	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 9923	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 9924	
> 9925	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 9926	
> 9927	```bash
> 9928	docker compose up -d
> 9929	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 9930	```
> 9931	
> 9932	---
> 9933	
> 9934	## Security Model (Post-Go-Live)
> 9935	
> 9936	| Table | Isolation |
> 9937	|-------|-----------|
> 9938	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 9939	| `mcorch_edges` | Same pattern |
> 9940	| `infra_health_logs` | **Admin-only read** (`has_role('admin')`, migration `20260701040000`) — was read-all-authenticated but writers leaked per-tenant `user_id`; the HUD reads via the service-role `get-infra-status` edge fn; write only service_role |
> 9941	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 9942	
> 9943	---
> 9944	
> 9945	## Billing Architecture
> 9946	
> 9947	| Decision | Value |
> 9948	|----------|-------|
> 9949	| Canonical billing ledger | `profiles.mco_balance` |
> 9950	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 9951	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 9952	| Orchestration cost | 10 mcoCoins/run |
> 9953	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 9954	| Stripe | Sandbox keys active — swap to live before first client |
> 9955	
> 9956	---
> 9957	
> 9958	## GraphRAG State
> 9959	
> 9960	- **9102 total nodes** (verificado live 2026-07-13 via REST count=exact, youtube-panel-repurpose-frontdoor seal: +handoff `9f7b191a-ec4a-45ef-9906-7a1f4e0b2c01` embedded 768d — Painel YouTube Studio Fatia 1 [`youtube-data` read Data v3+Analytics v2 token per-user server-side + escopos alinhados + mapa API 13rec/175props/52metrics/33ações + Pattern Conformance] + front-door host-local do Repurpose admin-only [drag-drop chunked 80MB furando o cap 100MB do CF → `host-upload-server` 3220 nginx `/api/host-upload` JWT+admin → ingest/run/worker fonte-local realpath-contido; **EP01 real 1,3GB → 5 shorts 9:16 Vision-QA-provados**] + fix legenda drawtext UTF-8→padding; 5 commits `e174988..f10fba4` +README `adcab9a`; /security-review NO FINDINGS ×3; prev 9097 do video-repurpose-engine seal `f050959c`)
> 9961	- **9097 total nodes** (verificado live 2026-07-12 via REST count=exact, video-repurpose-engine seal: +handoff `f050959c-5b05-4518-9142-2cf62ece1816` embedded 768d — Motor de repurpose de vídeo Fatias 1-3 [ingest externo `source_module='external'` VIVO + cortes 9:16/1:1 worker FFmpeg VIVO E2E + carrossel IG provado E2E, reusando a distribuição existente; 3 migrations aplicadas pelo Sovereign; cortes+carrossel provados por Vision QA em mídia real de produção] + OTD-SPACES-036 `space_publish_variants`/nó Publicar-em-Rede-Social + witness LoRA bloqueado em crédito Replicate BYOK; 6 commits `ac5ca86..831f5cc`; /security-review NO FINDINGS ×3; prev 9094 do voice-rail seal `8c1f0e7b`)
> 9962	- **9094 total nodes** (verificado live 2026-07-10 via REST count=exact, voice-rail-expressive-canvas-motion seal: +handoff `8c1f0e7b-fad5-4726-982c-a69ceacf2e13` embedded 768d — rail de voz clonada self-host COMPLETO no nó Clone de Voz [Qwen3-TTS 0.6B+1.7B, fila qwen3-voice, worker heartbeat, multi-amostra, .qvoice, Modo Expressivo com normalizador da sintaxe do Sovereign, IA-roteiro, smoke 12/12] + reparos assets/histórico [reunion avatar-studio + aba Áudios] + motion design Amendment 19 + regra perene BYOK; 12 commits `578f02e..aa4041f` + seal; prev 9086 do Creative Studio seal `6f2a5a90`)
> 9963	- **9082 total nodes** (verificado live 2026-07-09 via REST count=exact, spaces-lora-social-youtube-bok seal: +handoff `f0aa8111-bf5d-4fa8-928d-cb284d15f97a` embedded 768d — Spaces robustez: treino LoRA grátis REAL [`avatar-identity-train` Replicate BYOK USD 0, Amendment 11 fecha OTD-AC-017, migration `20260708130000`, plumbing zero-custo provado] + 1º nó social "Publicar no WordPress" [Post+Landing, Amendment 15, media-social gated OTD-SPACES-036] + blueprint deepsearch youtube-studio [`wf_baad6dbe-9e5`, 96 URLs, 27 OTDs] + Higgsfield Platform testável; 9 commits `44e625c..ed91311`; prev 9081 do TikTok seal `17e8921b`, 9077 do spaces-v2 `6a70b82b`)
> 9964	- **9077 total nodes** (verificado live 2026-07-07 via REST count=exact, spaces-v2-consolidation-arc seal: +handoff `6a70b82b-63a4-4e21-9627-05072f8d211d` embedded 768d — Spaces v2: Canvas Studio consolidado como "Spaces" [rename+redirects 5/5] + money path ledger-first unificado na superfície [it.2a/b/c: project-dispatch migration `20260707220000` + refund automático + watchdog `generations`, /security-review NO FINDINGS, smoke 40/40+6/6, OTD-SPACES-012 fechada] + nó Lista/lote template×produtos [it.4a] + thumbnails home [it.3] + nó Upscale REAL real-esrgan money-safe [it.4c] + fix preço sceneCompose [it.0a] + 2 bugs pré-existentes [style_transfer imagem-fonte · creative_assets source_module=spaces `20260707230000`]; Amendment 14 BoK; 11 commits `efaf190..ad42170`; guard-sweep 9/9; prev 9072 do arco-8b session-note `17b4027d`)
> 9965	- **9071 total nodes** (verificado live 2026-07-07 via REST count=exact, arco-8 mape-k-autonomic-loop seal: +handoff `d149d017-3683-4078-b3e6-7ad849ce4986` embedded 768d + milestone `f165f509` [MAPE-K live] — laço autonômico MAPE-K enterprise-grade: M+A mecânicos perpétuos [tick */5 + sweep 6h + watchdog monitor-do-monitor + UX-Explorer nightly] + P+E escada [L1 Telegram · L2 Nemotron-free ARMADO c/ toggle · L3 sessão event-driven] + review BLOCK→4 fixes + 1º ciclo real fechado [video-bridge 422 pré-débito `f678cb3`]; 19 commits `9538e09..c197054`; prev 9067)
> 9966	- **9067 total nodes** (verificado live 2026-07-06 via REST count=exact, arco-7 neighbors-otd010-hardening seal: +handoff `3a145a46-719e-4770-997e-206a9b22ef0c` embedded 768d + observation `1a431906` [vizinhos it.3] + decision `0f86ef8d` [OTD-SPACES-010 OIDC §3.1.3.7] + observation `aaf7a126` [backlog drenado, varredura `wf_f4481b27`] — vizinhos on-select + OTD-010 reconciliada + dead code removido + hardening 53 testes [suite 448→478]; 12 commits `235d7a2..828e492`; prev 9062)
> 9967	- **9062 total nodes** (verificado live 2026-07-05 via REST count=exact, arco-6 universe-synapse-embedding seal: +handoff `9afacad2-6fe0-4ffc-803c-0a359c2ad5b7` embedded 768d + observação `6d3d896b` — Unified Sensorial Canvas sinapses semânticas Fase B `OTD-SYNAPSE-EMBEDDING`: RPC `match_memory_code_synapses` [SECURITY DEFINER user_id-NULL-hardcoded, LATERAL k-NN HNSW, /security-review NO FINDINGS, migration `20260705230000`] desenha 148 sinapses por similaridade 768d código↔memória na fusão primária [ciano tracejada vs fúcsia real, Lei 1], gate E2E Vision-APROVADO + smoke anticorpo 8/8; + `OTD-UCANVAS-PERF` reconciliada não-issue; commits `61ead6b`/`eca97dc`/`5111f31`/`b572fad`/`bdcc440`/`6614fe2`; prev 9060 do arco 5 `dc47da77` [conector Higgsfield MCP], 9059/9057/9056/9055/9051 dos arcos anteriores)
> 9968	- **9047 total nodes** (verificado live 2026-07-03 via REST count=exact, fix-assets-private-bucket-signing seal: +handoff `6e2b32b2-d3fe-461f-b656-9c022927bc03` embedded 768d — Fix Assets: exibição de mídia privada owner-scoped em todo o ecossistema [migration `20260703030000` aplicada 3-policies+2-triggers+data-repair; `/security-review` CLOSED 9/10; cross-tenant BLOCKED ao vivo; E2E Biblioteca+Canvas Vision-APROVADO; 90 assets do User 0 vivos]; commits `6e5e005`/`459cd25`/`e3f6f9e`; prev 9045 do seal Spaces 2d compose `a49aa10`)
> 9969	- **9034 total nodes** (verificado live 2026-07-02 via REST count=exact, spaces-1b-code-complete-apply-gated seal: +handoff `209cbcd8-14ca-4fe2-aad3-3ef7a9409d93` embedded 768d — Spaces Fase 1b CÓDIGO-COMPLETO: SOP S1-S13 + migration ledger `20260702190000` (NÃO aplicada — GO gated) + branch canvas-execute ledger-first + client runGraph/clusters + /security-review SOUND c/ 4 fixes + smoke 8 gates pronto; commits `717abcd`..`ef33b67`; prev 9033)
> 9970	- **9033 total nodes** (verificado live 2026-07-02 via REST count=exact, loop-it2-3-reward-weights-spaces-fase1a-final-seal: +handoff `13fd6fe0-372d-4065-a5ae-b25b208718cf` embedded 768d — NFR-VA-010 reward_weights config-as-data no autopilot-analyze [migration `20260702150000` aplicada; resolveRewardConfig fail-safe; smoke 16/16; /security-review NO FINDINGS] + Spaces Fase 1a canvas 72/28 vivo [tabela `spaces` RLS-own migration `20260702170000`; useSpaces+SpaceNodeCard/Spotlight/ParamHUD; vitest 5/5; E2E DB graph=2 nós; Vision-QA APROVADO]; commits `6058e78`/`9ea6ac0`/`271770e`/`3bedef9`; prev 9032)
> 9971	- **9032 total nodes** (verificado live 2026-07-02 via REST count=exact, spaces-bok-seal-and-loop-it1-b5 seal: +handoff `10d8c70b-1e6a-4ca5-a8bf-83687b3f6b28` embedded 768d — suíte BoK spaces-evolution 9/9 completada [seal `8f5fd3fd` documentation_suite + DERIVES_FROM `c4247ef6`→viralmind; 25/25 suítes verdes; Pattern Conformance §11] + B5 Pauta de Receita FR-VA-031 HITL na AutopilotPage [vitest 7/7 · browser-verify User 0 · Vision-QA APROVADO]; commits `4a8fee0`/`367db9b`/`707d9ab`; prev 9023)
> 9972	- **9023 total nodes** (verificado live 2026-07-02 via REST count=exact, loop-it4-b4-ewma-final-seal: +handoff `1ddd4e86-7b89-4d13-9330-b5877c96df32` embedded 768d — B4 EWMA multi-ciclo no analyze [janela M=5 decay 0.5, smoke 13/13 gate L7 de estabilização] + selo final da sessão de loop [it.1 G7/fan-out · it.2-3 vision-gate · it.4 B4]; commit `bbc7ad9`; prev 9022)
> 9973	- **9022 total nodes** (verificado live 2026-07-02 via REST count=exact, loop-it2-3-vision-gate-both-harnesses seal: +handoff `8ddca90b-decb-4ca6-a857-89addf5134bb` embedded 768d — Vision QA gate mecânico nos 2 harnesses [audit-canvas-ui exit-block + e2e-user-zero Finding P1/ux; prova adversarial PNG branco→REPROVADO] + fix print público dist/; commits `8a41457`/`e511862`/`adf849b`; prev 9021)
> 9974	- **9021 total nodes** (verificado live 2026-07-02 via REST count=exact, loop-it1-reshaper-image-anchor-fanout-hygiene seal: +handoff `b31c1336-e693-4dac-9b10-7a743caf2863` embedded 768d — render-decoupling provado resolvido por arquitetura [channel_variants `reused_master` 7 canais no ciclo `77e02fca`] + fatia G7 imagem-pilar por `metadata.pillar_run_id` [smoke 18/18] + fan-out hygiene no autopilot-run; commits `d16ca88`/`b52ea4f`/`75a6e1c`; prev 9020 = seal final it.9 da primária `345cc2a7` [paridade total universo, v6.73.1]; prev 9018/9017 = seals it.5-6/Fase-B; prev 9003)
> 9975	- **9003 total nodes** (verificado live 2026-06-30 via REST count=exact, loop-editor-render-security-hardening seal: +handoff `d02a8570-5195-4206-a918-df3a42423aba` embedded 768d — Loop autônomo 8 iterações: FR-VS-047 editor→pipeline MCORCH [wrap `hyperframes render`, paridade provada 3 níveis + guard smoke + fix TDZ do dual-write de vídeo] + OTD-SEC-006/007 sentinel-wiring [generate-content+lead-score, injeção→403 LIVE] + FR-SEC-014 pt1 [ledger imutável `security_events`, /security-review NO FINDINGS, provado LIVE] + #2 YT/TikTok false-high corrigido; achado npm `hyperframes` license:None; 10 commits `8d59160`..`145f106`; +6 vs prev 8997 [inclui nó video-render `9069bb7d` + atividade Sovereign]; prev 8996)
> 9976	- **8996 total nodes** (verificado live 2026-06-30 via REST count=exact, avatar-fatia2-voice-fatia3a-consent-erase seal: +handoff `c138539f-0365-436a-ad56-c65e013793c6` embedded 768d + milestone Fatia 2 `b51d8de6-e574-42aa-93b7-8fd75d85a717` — Gabriel AI **Fatia 2 (Clone de Voz)** [nó voiceClone + edge `generate-voice` BYOK ElevenLabs/Cartesia fail-closed + code-switch guard FM-AC-013 + voice_profiles RLS-own Vault + RPCs tenant-guarded; migration `20260630120000`; smoke 10/10; browser+VisionQA PASS] + **Fatia 3a (Consent+Erasure LGPD Art.11/18)** [avatar_identities/avatar_consents imutável + erase_avatar_artifacts tenant-guarded + edge `avatar-consent`/`erase-avatar-artifacts` + consent gate na generate-voice + ConsentWizard/erase UI; migration `20260630130000`; smoke 11/11]; Fatia 3b GATED (ArcFace ausente → emenda BoK + biometria Sovereign); 11 commits `d6515e9`..`7913546`; `/security-review` NO FINDINGS ×2; prev 8993)
> 9977	- **8993 total nodes** (verificado live 2026-06-30 via REST count=exact, gabriel-ai-fatia1-spaces-p0-kanban-live seal: +handoff `aba1458e-2df1-4813-a71b-34360bf7417e` embedded 768d — Programa Gabriel AI [deepsearch força-total → BoK `avatar-clone-ai` 10/10 selada nó `ee81987d` GO-HYBRID + Fatia 1 BYOK hedra/cartesia/fal] + Spaces canvas Phase 0 (scaffold promovido) + Kanban painel-de-detalhe + reconciliador vivo não-destrutivo + cron */15; 6 commits `a5814d2`..`71f4c47`; prev 8992 = BoK seal `ee81987d` `documentation_suite` avatar-clone-ai DERIVES_FROM video-studio `c99b7875`)
> ```

## 🤖 Claude *(20:04:08)*


## 🤖 Claude *(20:04:08)*

═══════════════════════════════════════════════════════════
  HANDSON — Loop MAPE-K: UX-Explorer + [[landing-bundler|landing-bundler]] + BoKs 9/9 retroativas + swarm:read PAT (2026-07-16)
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
  Fase selada: **Loop MAPE-K 2026-07-16** — it.0→it.4 da diretiva drenadas (UX-Explorer enxergou pela 1ª vez + 1º finding P1 real da história · [[landing-bundler|landing-bundler]] core · witness cadência 7/7 · BoKs retroativas 32/32 · swarm:read no PAT)
  Últimos commits:
    `0fc3c40` — docs(handoff): seal loop MAPE-K (malha 9127)
    `1068c8b` — docs(readme): v6.105.0 — BoK 9/9 retroativas (32/32)
    `1b30fc3` — feat(predictive-swarm): swarm:read no allowlist do PAT (FR-PSW-002)

📂 **MUDANÇAS PENDENTES**
  Worktree limpo ✅ (`git status` vazio, diff HEAD vazio)

🏗️ **INFRA**
  mcorch_chroma:      Up 4 weeks (healthy) — Chroma API v2: **OK** (heartbeat respondeu)
  mcorch_claude_mem:  Up 4 weeks (healthy)
  mcorch_vision_mcp:  Up 24 hours (healthy)
  mega-brain-*:       daemon/webhook healthy · dashboard up — tudo verde ✅

🧠 **KNOWLEDGE MESH**
  **9127 nós** (fonte: seal 2026-07-16 no Task State; milestone `3a23fe00` embedado 768d)
  ⚠️ Nota honesta (Lei 1): a seção `GraphRAG State` do HANDOFF.md está desatualizada — última entrada detalhada é 9102 (2026-07-13); contagem de arestas não consta no snapshot mais recente.

🔧 **TYPESCRIPT**
  Zero erros ✅ (`npx tsc --noEmit` sem output)

📚 **BoK SUITES (v3 — MCORCH Master Execution Protocol)**
  Sealed: **32/32 famílias completas** ✅ (inclui as 2 retroativas da última sessão: video-repurpose + youtube-studio; security no formato ciso-4-artifact)
  Incomplete: nenhum
  Mesh seal nodes recentes:
    landing-factory → `b65e94b1` · video-repurpose → `a6df1548` · youtube-studio → `9a923887`
    spaces-cadence → `d0b4fdc8` · predictive-swarm → `485c0f6e` · content-provenance → `825088c0`

📌 **SPRINT**
  Goal: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente; Twitter/Instagram gated em tier/App Review
  Top gap: não definido (seção "Top 3 Gap Closures" ausente do sprint-priorities.md — rodar `/audit` se quiser recalibrar)

⚡ **PRÓXIMOS PASSOS (prioridade)**
  1. **AI Act Art.50 — código das 3 camadas** (C2PA + watermark + IPTC no spine `creative_assets`): BoK 9/9 selada, Gate Closed-Loop ABERTO, e o **prazo legal é 2026-08-02** (~17 dias; multa Art.99 €15M/3%). É o item com deadline externo real — só falta GO Sovereign.
  2. **predictive-swarm Fatia 2** (fan-out/job store): a migration `20260716190000` (swarm:read) está commitada + `/security-review` NO FINDINGS, mas **falta aplicar em prod** (ação Sovereign) antes de PAT externo alcançar a tool.
  3. **landing-factory continuação**: bundler core shipado 15/15 + G5 real; próximo salto (publish em `<slug>.gcrux.com`) está gated em **registrar `gcrux.com` + wildcard** (ação Sovereign) + OTD-LF-001/003/014.

⚠️ **ALERTAS**
  1. 🔴 **Rotação de credenciais pendente** (fila desde 2026-07-14/15): SA Vertex colada no chat + chave Gemini + token Telegram — risco real de exposição, é a ação Sovereign mais urgente do cluster.
  2. 🔒 **Cluster de gates Sovereign acumulado**: apply da migration swarm:read em prod · registrar gcrux.com+wildcard · 3 chaves Gmail · reconexão X · app-audit IG/TikTok · OTD-PSW-001 (decisão GPU).
  3. scratch/ vazio ✅ (o `ls` retornou exit 0 mas o diretório não tem arquivos) · containers todos healthy · tsc 0 · 32/32 BoKs verdes — **nenhum bloqueador técnico**.

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

## 👤 User *(20:44:54)*

<local-command-caveat>Caveat: The messages below were generated by the user while running local commands. DO NOT respond to these messages or otherwise consider them in your response unless the user explicitly asks you to.</local-command-caveat>

## 👤 User *(20:44:54)*

<command-name>/model</command-name>
            <command-message>model</command-message>
            <command-args>claude-fable-5</command-args>

## 👤 User *(20:44:54)*

<local-command-stdout>Set model to claude-fable-5</local-command-stdout>

## 👤 User *(20:47:01)*

ótimo temos duas ótimas noticias, os escopos estão funcionando e aprovados pelo google, e tambem agora temos o pinterest aprovado tenho a Chave secreta do aplicativo e o id do aplicativo.:

Chaves da API
A chave secreta e o ID do aplicativo são strings exclusivas que identificam o seu aplicativo.
Essa chave deve ser um segredo conhecido apenas pelo cliente e o servidor.
Trate-a como uma senha.

Redefinir o segredo do aplicativo
ID do aplicativo
ID_APLICATIVO
Chave secreta do aplicativo
MINHA_CHAVE


Gerar tokens de acesso
Use este token para testar e explorar nossa API v5.
Copiar este token imediatamente, antes de sair do navegador
Tratar este token como uma senha
Oferece acesso limitado a 3 escopos
(pins:read, boards:read, user_accounts:read, ads:read and catalogs:read)

Selecionar ambiente

Produção limitada

Sandbox

Gerar token
URIs de redirecionamento
Depois que seu aplicativo for autorizado, o usuário será direcionado para esse URI. Os URIs de redirecionamento precisam usar https, um esquema específico para aplicativos, ou http com um localhost.
Link de redirecionamento
Adicione link de redirecionamento usando vírgula, espaço, ponto e vírgula ou pressionando "Enter" ou "Adicionar"

Adicionar
Escopos da API
Você precisa solicitar pelo menos um escopo durante o fluxo do OAuth. Solicite apenas os escopos exigidos para o seu produto.
Acesso atual
Acesso Trial ativo
Atualizar acesso
Documentos
; Abre uma nova aba
Scopes table
Entity	
read
 permissions	
write
 permissions
ads
See all data related to advertising, such as ads, ad groups and campaigns.
Create, update or delete ads, ad groups and campaigns.
billing
See all of your billing data, such as your billing profile.	Create, update or delete billing data.
biz_access
See all business access data.	Create, update or delete business access data.
boards
See public boards, including group boards, with 
boards:read
 or secret boards with 
boards:read_secret
.
Create, update or delete public boards with 
boards:write
 or secret boards with 
boards:write_secret
.
catalogs
See all catalog data.	Create, update or delete catalogs.
pins
See public pins with 
pins:read
 or secret pins with 
pins:read_secret
.
Create, update or delete public pins with 
pins:write
 or secret pins with 
pins:write_secret
.
user_accounts
See user accounts and followers.	Update user accounts and followers.


--

Preciso preencher o Link de redirecionamento e você adicionar todas as chaves globais principalmente essas de aplicativos como google *login e outros, tiktok tiktok login e outros, agora pinterest tambem para que os usuários consigam conectar em https://login.mcorch.com/dashboard/social eu preciso adicionar a chave em https://login.mcorch.com/dashboard/admin assim nã preciso .env nem rodar comando npx supabase pra adicionar o segredo no vault. 

Não tem problema sobre a rotação de credenciais pendente mas deve ter uma notificação na pagina de admin para lembrar que isso precisa ser feito. E então assim posso rotacionar e adicionar diretamente no dashboard/admin tendo uma experiencia paarecida com o BYOK per user mas nesse caso é somente ADMIN para as chaves secretas de aplicativos outra coisas globais.

E pode continuar com a migration swarm:red e os passos que depender de mim você me fala, para wildcard por exemplo e tambem reconexão X e app audit IG/Tiktok OTD-PSW-001 vamos usar mais para frente quando os creditos gratuitos do vertex acabarem. E então pode armar o loop para os próximos passos (PRIORIDADE).

## 🤖 Claude *(20:50:29)*

API Error: 529 Overloaded. This is a server-side issue, usually temporary — try again in a moment. If it persists, check https://status.claude.com.

## 👤 User *(20:50:35)*

<local-command-caveat>Caveat: The messages below were generated by the user while running local commands. DO NOT respond to these messages or otherwise consider them in your response unless the user explicitly asks you to.</local-command-caveat>

## 👤 User *(20:50:35)*

<command-name>/model</command-name>
            <command-message>model</command-message>
            <command-args>claude-opus-4-8</command-args>

## 👤 User *(20:50:35)*

<local-command-stdout>Set model to claude-opus-4-8</local-command-stdout>

## 👤 User *(20:50:35)*

ótimo temos duas ótimas noticias, os escopos estão funcionando e aprovados pelo google, e tambem agora temos o pinterest aprovado tenho a Chave secreta do aplicativo e o id do aplicativo.:

Chaves da API
A chave secreta e o ID do aplicativo são strings exclusivas que identificam o seu aplicativo.
Essa chave deve ser um segredo conhecido apenas pelo cliente e o servidor.
Trate-a como uma senha.

Redefinir o segredo do aplicativo
ID do aplicativo
ID_APLICATIVO
Chave secreta do aplicativo
MINHA_CHAVE


Gerar tokens de acesso
Use este token para testar e explorar nossa API v5.
Copiar este token imediatamente, antes de sair do navegador
Tratar este token como uma senha
Oferece acesso limitado a 3 escopos
(pins:read, boards:read, user_accounts:read, ads:read and catalogs:read)

Selecionar ambiente

Produção limitada

Sandbox

Gerar token
URIs de redirecionamento
Depois que seu aplicativo for autorizado, o usuário será direcionado para esse URI. Os URIs de redirecionamento precisam usar https, um esquema específico para aplicativos, ou http com um localhost.
Link de redirecionamento
Adicione link de redirecionamento usando vírgula, espaço, ponto e vírgula ou pressionando "Enter" ou "Adicionar"

Adicionar
Escopos da API
Você precisa solicitar pelo menos um escopo durante o fluxo do OAuth. Solicite apenas os escopos exigidos para o seu produto.
Acesso atual
Acesso Trial ativo
Atualizar acesso
Documentos
; Abre uma nova aba
Scopes table
Entity	
read
 permissions	
write
 permissions
ads
See all data related to advertising, such as ads, ad groups and campaigns.
Create, update or delete ads, ad groups and campaigns.
billing
See all of your billing data, such as your billing profile.	Create, update or delete billing data.
biz_access
See all business access data.	Create, update or delete business access data.
boards
See public boards, including group boards, with 
boards:read
 or secret boards with 
boards:read_secret
.
Create, update or delete public boards with 
boards:write
 or secret boards with 
boards:write_secret
.
catalogs
See all catalog data.	Create, update or delete catalogs.
pins
See public pins with 
pins:read
 or secret pins with 
pins:read_secret
.
Create, update or delete public pins with 
pins:write
 or secret pins with 
pins:write_secret
.
user_accounts
See user accounts and followers.	Update user accounts and followers.


--

Preciso preencher o Link de redirecionamento e você adicionar todas as chaves globais principalmente essas de aplicativos como google *login e outros, tiktok tiktok login e outros, agora pinterest tambem para que os usuários consigam conectar em https://login.mcorch.com/dashboard/social eu preciso adicionar a chave em https://login.mcorch.com/dashboard/admin assim nã preciso .env nem rodar comando npx supabase pra adicionar o segredo no vault. 

Não tem problema sobre a rotação de credenciais pendente mas deve ter uma notificação na pagina de admin para lembrar que isso precisa ser feito. E então assim posso rotacionar e adicionar diretamente no dashboard/admin tendo uma experiencia paarecida com o BYOK per user mas nesse caso é somente ADMIN para as chaves secretas de aplicativos outra coisas globais.

E pode continuar com a migration swarm:red e os passos que depender de mim você me fala, para wildcard por exemplo e tambem reconexão X e app audit IG/Tiktok OTD-PSW-001 vamos usar mais para frente quando os creditos gratuitos do vertex acabarem. E então pode armar o loop para os próximos passos (PRIORIDADE).

## 🤖 Claude *(20:56:15)*

**ORO triplet desta sessão:**
- Operator: MCORCH Master Execution Agent
- Reviewer: `/security-review` (migrations/edge fns) + Sovereign (gates externos: console Pinterest, apply GO'd)
- Owner: Sovereign (blast radius: credenciais globais de app + trilho OAuth social)

Excelente notícia dupla — Google aprovado + Pinterest aprovado destrava o 8º canal. Plano do loop (prioridade declarada):

1. **swarm:read em prod** (GO dado) — apply + prova material.
2. **Pinterest OAuth + Admin Global App Keys** em `/dashboard/admin` (BYOK-like, admin-only, Vault, zero `.env`/CLI) + lembrete de rotação — BoK gate primeiro (amendment), depois SOP Lei 2, depois código.
3. Te devolvo o **redirect URI exato** para colar no console Pinterest assim que o reconhecimento confirmar o registrado no trilho `social-auth-callback`.

Armando o reconhecimento ultracode + apply em paralelo:

🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat supabase/migrations/20260716190000*.sql; echo \"---APPLY-SCRIPTS---\"; ls scripts/qa/apply-*.sh scripts/apply-*.sh 2>/dev/null; echo \"---ENV-KEYS---\"; grep -l \"MANAGEMENT\" scripts/qa/*.sh scripts/*.sh 2>/dev/null | head -5",
  "description": "Ler migration swarm:read + localizar mecanismo de apply em prod"
}
```

🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'recon-pinterest-admin-keys',\n  description: 'Mapear trilhos OAuth social + social_app_config + AdminPage + publish rails + apply mechanism para a fatia Pinterest/Admin Global Keys',\n  phases: [\n    { title: 'Recon', detail: '6 leitores paralelos sobre os subsistemas afetados' },\n  ],\n}\n\nphase('Recon')\n\nconst FRONTS = [\n  {\n    key: 'oauth-rails',\n    prompt: `Repo: /home/gcrUX/htdocs/constellation-orchestra. Read supabase/functions/social-auth-init/index.ts and supabase/functions/social-auth-callback/index.ts COMPLETELY (and any _shared helpers they import, e.g. oauth-state.ts).\nAnswer with precision (file:line refs):\n1. For EACH platform supported (linkedin, twitter, instagram, youtube/google, tiktok, others): where do client_id and client_secret come from? (Deno.env key names? social_app_config table lookup? per-user?) Give the exact resolution code.\n2. What is the EXACT redirect_uri value sent to each provider's authorize URL? (literal string or how it's constructed \u2014 I need the exact URL an external console must whitelist).\n3. How does the signed \"intent\" mechanism work in social-auth-callback (the TikTok reuse pattern)? How is a new intent/platform added?\n4. How are tokens stored after callback (social_accounts? social_credentials? columns, encryption)?\n5. List everything needed to add a NEW platform \"pinterest\" to this rail (enums, switch branches, scope strings, token exchange specifics).`,\n  },\n  {\n    key: 'app-config-vault',\n    prompt: `Repo: /home/gcrUX/htdocs/constellation-orchestra. Investigate the table social_app_config: grep supabase/migrations/ for social_app_config (read the full migration(s) that create/alter it), and grep supabase/functions/ and src/ for all readers/writers.\nAnswer (file:line refs):\n1. Full schema of social_app_config (columns, constraints, platform values allowed).\n2. RLS policies on it \u2014 who can SELECT/INSERT/UPDATE? Is there any admin-scoped write path from the client today?\n3. Is there a Vault encryption pattern on it (triggers like vault_upsert_secret / encrypted views)? Read supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql and describe the canonical pattern for encrypting a secret column.\n4. Which platforms have rows/are expected (tiktok? google? linkedin?) \u2014 grep for how each edge fn resolves app credentials: which use social_app_config vs Deno.env (list env var names per platform: TWITTER_CLIENT_ID/SECRET, LINKEDIN_CLIENT_ID/SECRET, GOOGLE_*, TIKTOK_*, META_*).\n5. Any existing UI (src/) that reads/writes social_app_config?`,\n  },\n  {\n    key: 'admin-page',\n    prompt: `Repo: /home/gcrUX/htdocs/constellation-orchestra. Read src/pages/AdminPage.tsx (or whatever serves route /dashboard/admin \u2014 check src/App.tsx routing) plus its hooks/components.\nAnswer (file:line refs):\n1. Component structure: sections/cards/tabs on the admin page today.\n2. How admin gating works (has_role single-arg gotcha \u2014 confirm exact usage) both client-side and on any admin edge fns.\n3. Existing hooks pattern for admin data (useAdminData?).\n4. Where a new \"Chaves de Aplicativo (Global)\" card + a \"rota\u00e7\u00e3o pendente\" reminder banner would slot in (naming/layout conventions, pt-BR UI).\n5. Any existing notification/reminder mechanism on admin page.`,\n  },\n  {\n    key: 'social-page',\n    prompt: `Repo: /home/gcrUX/htdocs/constellation-orchestra. Read the page serving /dashboard/social (check src/App.tsx; likely src/pages/SocialPage.tsx or similar) + hooks (useSocialAccounts?) + connect-button components.\nAnswer (file:line refs):\n1. Which platforms are listed for connection today and how each connect flow starts client-side (invoke social-auth-init? URL?).\n2. How connection state/badges are shown (is_active pattern).\n3. Exactly what must change to add a Pinterest connect card (icon availability in lucide-react 1.11 \u2014 verify Pinterest icon exists: grep \"as Pinterest\" node_modules/lucide-react/dist/esm/lucide-react.mjs \u2014 CLAUDE.md warns brand icons were REMOVED; if absent, note the fallback pattern used for other brands e.g. AVATAR_ICON_MAP or custom svg).\n4. How disconnect works (disconnect_social RPC).`,\n  },\n  {\n    key: 'publish-rails',\n    prompt: `Repo: /home/gcrUX/htdocs/constellation-orchestra. Investigate Pinterest's existing footprint in the publish/reshape rails:\n1. grep -ri pinterest supabase/ src/ scripts/ docs/bok/post-engine/ --include='*.ts' --include='*.tsx' --include='*.sql' --include='*.md' -l, then read the relevant hits.\n2. Does channel_profiles seed include a pinterest row (transform_recipe, Pinterest-SEO FR-CP-008)? Full recipe details.\n3. Does publish-social or publish-channel-variant have a pinterest branch? What would publishing a Pin require (API endpoint expectations coded anywhere)?\n4. What are format specs for pinterest in src/lib/format-specs.ts (2:3 pin)?\nReturn a map of what EXISTS vs what's MISSING for pinterest end-to-end (connect \u2192 variant \u2192 publish).`,\n  },\n  {\n    key: 'apply-mechanism',\n    prompt: `Repo: /home/gcrUX/htdocs/constellation-orchestra. Determine the canonical way migrations are applied to PROD in this project:\n1. Read scripts/qa/apply-*.sh (any that exist) \u2014 extract the mechanism (Supabase Management API? psql? supabase db push?), env vars needed (SUPABASE_ACCESS_TOKEN? project ref?), and the WAF gotcha handling (HTML-challenge on big DO $$ payloads \u2192 chunked apply + material proof).\n2. Read supabase/migrations/20260716190000*.sql fully (swarm:read PAT allowlist) and assess: is it small enough for single-shot apply? What is the material proof query to verify it applied (the CHECK constraint definition on which table)?\n3. How is the migrations ledger kept in sync (schema drift audit expects registered migrations \u2014 how did past sessions register applied migrations in supabase_migrations.schema_migrations)?\nReturn: exact commands/steps to apply 20260716190000 to prod + verify + register in ledger.`,\n  },\n]\n\nconst RESULT_SCHEMA = {\n  type: 'object',\n  properties: {\n    findings: { type: 'string', description: 'Structured findings in markdown with file:line refs' },\n    key_facts: { type: 'array', items: { type: 'string' }, description: 'Bullet list of load-bearing facts (exact values: env var names, redirect URIs, column names)' },\n    gaps_or_risks: { type: 'array', items: { type: 'string' } },\n  },\n  required: ['findings', 'key_facts'],\n}\n\nconst results = await parallel(FRONTS.map(f => () =>\n  agent(f.prompt, { label: `recon:${f.key}`, phase: 'Recon', schema: RESULT_SCHEMA })\n    .then(r => ({ key: f.key, ...r }))\n))\n\nreturn { fronts: results.filter(Boolean) }"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> -- 20260716190000_pat_allowlist_swarm_read.sql
> -- predictive-swarm Fatia 2 (sub-fatia PAT) — FR-PSW-002 / NFR-PSW-005 / BoK 00-index §"Scopes novos".
> --
> -- WHY: the Tier 1 sensory gate tool (`vision.parse_sensory_gate`, scope `swarm:read`) shipped LIVE in
> -- the mcorch_vision_mcp container on 2026-07-15 (Fatia 1) and is already reachable by internal tenant
> -- JWTs (ALL_SCOPES in identity.ts:17 includes swarm:read). But an EXTERNAL PAT cannot carry the scope:
> -- the closed-vocabulary allowlist CHECK on mcp_access_tokens (migration 20260615180000, constraint
> -- `scopes_allowed`) predates the swarm surface and rejects the write. This migration extends the
> -- vocabulary with `swarm:read` ONLY — `swarm:run`/`swarm:write` enter with their own tools
> -- (swarm-initialize / consolidate-sensory-insight, Fatias 2-full/3), never before a live tool exists
> -- (fail-closed: no PAT may carry a scope that gates nothing).
> --
> -- Security posture unchanged: still an ALLOWLIST (not blocklist); still `scopes <@ ARRAY[...]` with
> -- array_length >= 1; RLS and every other constraint untouched. The constraint name is DECLARED in the
> -- original migration (not auto-generated), so drop-by-name is deterministic; IF EXISTS keeps the
> -- migration re-runnable.
> 
> ALTER TABLE public.mcp_access_tokens
>   DROP CONSTRAINT IF EXISTS scopes_allowed;
> 
> ALTER TABLE public.mcp_access_tokens
>   ADD CONSTRAINT scopes_allowed CHECK (
>     scopes <@ ARRAY['vision:read','deepsearch:run','mesh:read','mesh:write','swarm:read']
>     AND array_length(scopes, 1) >= 1
>   );
> 
> COMMENT ON CONSTRAINT scopes_allowed ON public.mcp_access_tokens IS
>   'Closed scope vocabulary (allowlist, never blocklist). swarm:read added 2026-07-16 (predictive-swarm '
>   'Fatia 2 sub-fatia PAT — Tier 1 gate tool live since Fatia 1); swarm:run/swarm:write enter only with '
>   'their own live tools.';
> ---APPLY-SCRIPTS---
> scripts/qa/apply-asset-signing-migration.sh
> scripts/qa/apply-creative-assets-external-migration.sh
> scripts/qa/apply-host-media-nginx.sh
> scripts/qa/apply-it2a-project-dispatch.sh
> scripts/qa/apply-it4a-creative-assets-spaces.sh
> scripts/qa/apply-space-publish-variants-migration.sh
> scripts/qa/apply-spaces-1b-migration.sh
> scripts/qa/apply-tiktok-login-migration.sh
> scripts/qa/apply-user-provider-keys-migration.sh
> scripts/qa/apply-video-renders-repurpose-migration.sh
> scripts/qa/apply-voice-qwen3-local-migration.sh
> ---ENV-KEYS---
> ```

> **Tool Result (Workflow)** - ❌ Error
>
> ```
> claude-opus-4-8 is temporarily unavailable, so auto mode cannot determine the safety of Workflow right now. Wait briefly and then try this action again. If it keeps failing, continue with other tasks that don't require this action and come back to it later. Note: reading files, searching code, and other read-only operations do not require the classifier and can still be used.
> ```

## 🤖 Claude *(20:56:29)*


## 🤖 Claude *(20:56:29)*


## 🤖 Claude *(20:56:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat scripts/qa/apply-tiktok-login-migration.sh | head -60",
  "description": "Ler mecanismo can\u00f4nico de apply de migration em prod"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> #!/usr/bin/env bash
> # apply-tiktok-login-migration.sh — applies 20260708100000_tiktok_login_identities.sql to production via the
> # Supabase Management API (single-statement channel) and registers it in the schema_migrations ledger.
> # SOP: docs/processes/tiktok-login-oauth.md. Run with GO: bash scripts/qa/apply-tiktok-login-migration.sh
> set -euo pipefail
> cd "$(dirname "$0")/../.."
> 
> TOKEN=$(cat ~/.supabase/access-token)
> REF=bcyvddsykvehvpwstlfa
> API="https://api.supabase.com/v1/projects/${REF}/database/query"
> VER=20260708100000
> NAME=tiktok_login_identities
> 
> echo "[1/3] applying migration DDL..."
> python3 - <<'PY' > /tmp/tiktok-mig.json
> import json
> sql = open('supabase/migrations/20260708100000_tiktok_login_identities.sql').read()
> print(json.dumps({'query': sql}))
> PY
> RES=$(curl -s -X POST "$API" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" --data-binary @/tmp/tiktok-mig.json)
> echo "apply result: ${RES:0:300}"
> echo "$RES" | grep -qi '"error"' && { echo "❌ apply failed"; exit 1; }
> 
> echo "[2/3] registering in schema_migrations ledger..."
> curl -s -X POST "$API" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
>   -d "{\"query\":\"INSERT INTO supabase_migrations.schema_migrations (version, name) VALUES ('$VER', '$NAME') ON CONFLICT DO NOTHING;\"}"
> echo
> 
> echo "[3/3] material proof (Lei 1): tables + RLS enabled + binding_hash NOT NULL + RPC..."
> curl -s -X POST "$API" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
>   -d "{\"query\":\"SELECT (SELECT count(*) FROM pg_tables WHERE schemaname='public' AND tablename IN ('tiktok_identities','tiktok_login_codes')) AS tables, (SELECT count(*) FROM pg_class WHERE relname IN ('tiktok_identities','tiktok_login_codes') AND relrowsecurity) AS rls_enabled, (SELECT count(*) FROM information_schema.columns WHERE table_name='tiktok_login_codes' AND column_name='binding_hash' AND is_nullable='NO') AS binding_notnull, (SELECT count(*) FROM pg_proc WHERE proname='disconnect_tiktok_identity') AS rpc, (SELECT count(*) FROM pg_policies WHERE tablename IN ('tiktok_identities','tiktok_login_codes')) AS client_policies;\"}"
> echo
> echo "✅ done — expected: tables=2, rls_enabled=2, binding_notnull=1, rpc=1, client_policies=0 (service-role only)"
> ```

## 🤖 Claude *(20:56:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n -E \"redirect_uri|social_app_config|Deno.env.get\" supabase/functions/social-auth-init/index.ts | head -40; echo \"---CALLBACK---\"; grep -n -E \"redirect_uri|social_app_config|intent\" supabase/functions/social-auth-callback/index.ts | head -30",
  "description": "Mapear resolu\u00e7\u00e3o de credenciais e redirect_uri nos trilhos OAuth"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 37:      Deno.env.get("SUPABASE_URL")!,
> 38:      (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!,
> 51:    const { platform, redirect_uri } = await req.json();
> 53:    if (!platform || !redirect_uri) {
> 54:      return new Response(JSON.stringify({ error: "platform and redirect_uri required" }), {
> 60:    const callbackUrl = `${Deno.env.get("SUPABASE_URL")}/functions/v1/social-auth-callback`;
> 63:    const stateKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 64:    const state = await signState({ userId, platform, redirect_uri, ts: Date.now() }, stateKey);
> 69:      const clientId = Deno.env.get("LINKEDIN_CLIENT_ID");
> 77:      authUrl = `${LINKEDIN_AUTH_URL}?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}`;
> 80:      const appId = Deno.env.get("INSTAGRAM_APP_ID");
> 88:      authUrl = `${INSTAGRAM_AUTH_URL}?client_id=${appId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}&response_type=code`;
> 91:      const clientId = Deno.env.get("TWITTER_CLIENT_ID");
> 103:      authUrl = `${TWITTER_AUTH_URL}?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}&code_challenge=${codeChallenge}&code_challenge_method=plain`;
> 107:      // Service-role client reads the decrypted_social_app_config view (mirrors social-auth-callback).
> 109:        Deno.env.get("SUPABASE_URL")!,
> 110:        (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
> 123:      authUrl = `${TIKTOK_AUTH_URL}?client_key=${encodeURIComponent(creds.clientId)}&response_type=code&redirect_uri=${encodeURIComponent(callbackUrl)}&scope=${encodeURIComponent(scopes)}&state=${encodeURIComponent(state)}`;
> 128:        Deno.env.get("SUPABASE_URL")!,
> 129:        (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
> 157:      authUrl = `${YOUTUBE_AUTH_URL}?client_id=${encodeURIComponent(creds.clientId)}&redirect_uri=${encodeURIComponent(callbackUrl)}&response_type=code&scope=${encodeURIComponent(scopes)}&state=${encodeURIComponent(state)}&access_type=offline&prompt=consent`;
> 162:        Deno.env.get("SUPABASE_URL")!,
> 163:        (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
> 174:      // (doc 10 §Pinterest). redirect_uri must match EXACTLY (no wildcard).
> 176:      authUrl = `${PINTEREST_AUTH_URL}?client_id=${encodeURIComponent(creds.clientId)}&redirect_uri=${encodeURIComponent(callbackUrl)}&response_type=code&scope=${encodeURIComponent(scopes)}&state=${encodeURIComponent(state)}`;
> ---CALLBACK---
> 46:  // TikTok LOGIN reuses this already-registered redirect_uri. Dispatch by the signed intent (HMAC-tamper-proof)
> 67:    const state = await verifyState<{ userId: string; platform: string; redirect_uri: string }>(
> 74:    const { userId, platform, redirect_uri } = state;
> 103:          redirect_uri: callbackUrl,
> 135:          redirect_uri: callbackUrl,
> 175:          redirect_uri: callbackUrl,
> 208:          redirect_uri: callbackUrl,
> 235:          redirect_uri: callbackUrl,
> 275:          redirect_uri: callbackUrl,
> 350:      const frontendUrl = redirect_uri || "https://login.mcorch.com";
> ```

## 🤖 Claude *(20:56:51)*


## 🤖 Claude *(20:56:51)*


## 🤖 Claude *(20:56:52)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-init/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 2	import { signState } from "../_shared/oauth-state.ts";
> 3	import {
> 4	  resolveSocialAppCreds,
> 5	  SocialAppConfigError,
> 6	  socialAppConfigErrorResponse,
> 7	} from "../_shared/social-app-config.ts";
> 8	
> 9	const corsHeaders = {
> 10	  "Access-Control-Allow-Origin": "*",
> 11	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 12	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-user-token, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version",
> 13	};
> 14	
> 15	const LINKEDIN_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization";
> 16	const INSTAGRAM_AUTH_URL = "https://api.instagram.com/oauth/authorize";
> 17	const TWITTER_AUTH_URL = "https://twitter.com/i/oauth2/authorize";
> 18	const TIKTOK_AUTH_URL = "https://www.tiktok.com/v2/auth/authorize/";
> 19	const YOUTUBE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth";
> 20	const PINTEREST_AUTH_URL = "https://www.pinterest.com/oauth/";
> 21	
> 22	Deno.serve(async (req) => {
> 23	  if (req.method === "OPTIONS") {
> 24	    return new Response("ok", { headers: corsHeaders });
> 25	  }
> 26	
> 27	  try {
> 28	    const authHeader = req.headers.get("Authorization");
> 29	    if (!authHeader?.startsWith("Bearer ")) {
> 30	      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 31	        status: 401,
> 32	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 33	      });
> 34	    }
> 35	
> 36	    const supabase = createClient(
> 37	      Deno.env.get("SUPABASE_URL")!,
> 38	      (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!,
> 39	      { global: { headers: { Authorization: authHeader } } }
> 40	    );
> 41	
> 42	    const { data: { user }, error: userError } = await supabase.auth.getUser();
> 43	    if (userError || !user) {
> 44	      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 45	        status: 401,
> 46	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 47	      });
> 48	    }
> 49	
> 50	    const userId = user.id;
> 51	    const { platform, redirect_uri } = await req.json();
> 52	
> 53	    if (!platform || !redirect_uri) {
> 54	      return new Response(JSON.stringify({ error: "platform and redirect_uri required" }), {
> 55	        status: 400,
> 56	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 57	      });
> 58	    }
> 59	
> 60	    const callbackUrl = `${Deno.env.get("SUPABASE_URL")}/functions/v1/social-auth-callback`;
> 61	    // Signed state (HMAC-SHA256, SB_SECRET_KEY) — the callback has no user JWT, so the signature is the only proof
> 62	    // that THIS userId actually initiated the connect (closes cross-tenant account-linking). `ts` bounds replay.
> 63	    const stateKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 64	    const state = await signState({ userId, platform, redirect_uri, ts: Date.now() }, stateKey);
> 65	
> 66	    let authUrl: string;
> 67	
> 68	    if (platform === "linkedin") {
> 69	      const clientId = Deno.env.get("LINKEDIN_CLIENT_ID");
> 70	      if (!clientId) {
> 71	        return new Response(JSON.stringify({ error: "LinkedIn not configured" }), {
> 72	          status: 500,
> 73	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 74	        });
> 75	      }
> 76	      const scopes = "openid profile email w_member_social";
> 77	      authUrl = `${LINKEDIN_AUTH_URL}?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}`;
> 78	
> 79	    } else if (platform === "instagram" || platform === "facebook") {
> 80	      const appId = Deno.env.get("INSTAGRAM_APP_ID");
> 81	      if (!appId) {
> 82	        return new Response(JSON.stringify({ error: "Instagram/Facebook not configured" }), {
> 83	          status: 500,
> 84	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 85	        });
> 86	      }
> 87	      const scopes = "instagram_business_basic,instagram_business_content_publish,instagram_business_manage_comments,instagram_business_manage_messages";
> 88	      authUrl = `${INSTAGRAM_AUTH_URL}?client_id=${appId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}&response_type=code`;
> 89	
> 90	    } else if (platform === "twitter") {
> 91	      const clientId = Deno.env.get("TWITTER_CLIENT_ID");
> 92	      if (!clientId) {
> 93	        return new Response(JSON.stringify({ error: "Twitter/X not configured" }), {
> 94	          status: 500,
> 95	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 96	        });
> 97	      }
> 98	      // Twitter OAuth 2.0 with PKCE
> 99	      const codeChallenge = state.slice(0, 43); // simple challenge for demo; production should use S256
> 100	      // media.write (FR-SPACES-084): image/video upload for tweets. Connections made BEFORE this scope was
> 101	      // added lack it — publish-social fails those with an actionable "reconecte a conta X" error.
> 102	      const scopes = "tweet.read tweet.write users.read offline.access media.write";
> 103	      authUrl = `${TWITTER_AUTH_URL}?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}&code_challenge=${codeChallenge}&code_challenge_method=plain`;
> 104	
> 105	    } else if (platform === "tiktok") {
> 106	      // App creds resolve per-user → env fallback → hard-fail (API Tenancy Model · FR-PE-006).
> 107	      // Service-role client reads the decrypted_social_app_config view (mirrors social-auth-callback).
> 108	      const serviceClient = createClient(
> 109	        Deno.env.get("SUPABASE_URL")!,
> 110	        (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
> 111	      );
> 112	      let creds;
> 113	      try {
> 114	        creds = await resolveSocialAppCreds(serviceClient, userId, "tiktok");
> 115	      } catch (err) {
> 116	        const failClosed = socialAppConfigErrorResponse(err, corsHeaders);
> 117	        if (failClosed) return failClosed;
> 118	        throw err;
> 119	      }
> 120	      // Scope MUST be COMMA-separated — a space silently fails the consent (doc 10 §TikTok).
> 121	      // video.publish = Direct Post (autonomous); NEVER video.upload (draft-to-inbox needs a human).
> 122	      const scopes = "video.publish,user.info.basic";
> 123	      authUrl = `${TIKTOK_AUTH_URL}?client_key=${encodeURIComponent(creds.clientId)}&response_type=code&redirect_uri=${encodeURIComponent(callbackUrl)}&scope=${encodeURIComponent(scopes)}&state=${encodeURIComponent(state)}`;
> 124	
> 125	    } else if (platform === "youtube") {
> 126	      // App creds resolve per-user → env fallback → hard-fail (API Tenancy Model · FR-PE-007).
> 127	      const serviceClient = createClient(
> 128	        Deno.env.get("SUPABASE_URL")!,
> 129	        (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
> 130	      );
> 131	      let creds;
> 132	      try {
> 133	        creds = await resolveSocialAppCreds(serviceClient, userId, "youtube");
> 134	      } catch (err) {
> 135	        const failClosed = socialAppConfigErrorResponse(err, corsHeaders);
> 136	        if (failClosed) return failClosed;
> 137	        throw err;
> 138	      }
> 139	      // access_type=offline + prompt=consent are CRITICAL: without prompt=consent a re-auth
> 140	      // returns a NULL refresh_token silently (doc 10 §YouTube).
> 141	      //
> 142	      // The 4 scopes registered on the OAuth consent screen for Google verification (Amendment 12):
> 143	      //  • youtube.readonly — read channel/videos/stats (panel, Fatia 1);
> 144	      //  • youtube — publish the user's own videos (videos.insert, publish-social);
> 145	      //  • youtube.force-ssl — the user EDITS (videos.update) and DELETES (videos.delete) their own videos
> 146	      //    from the panel (Fatia 2);
> 147	      //  • yt-analytics-monetary.readonly — revenue + non-monetary performance reports (superset: it also
> 148	      //    grants the non-monetary metrics, so a single analytics scope covers video_metrics AND
> 149	      //    revenue_metrics). Requires the "YouTube Analytics API" enabled in the Cloud project.
> 150	      // Each scope maps to a demonstrable in-app operation (the Google review video shows all four).
> 151	      const scopes = [
> 152	        "https://www.googleapis.com/auth/youtube.readonly",
> 153	        "https://www.googleapis.com/auth/youtube",
> 154	        "https://www.googleapis.com/auth/youtube.force-ssl",
> 155	        "https://www.googleapis.com/auth/yt-analytics-monetary.readonly",
> 156	      ].join(" ");
> 157	      authUrl = `${YOUTUBE_AUTH_URL}?client_id=${encodeURIComponent(creds.clientId)}&redirect_uri=${encodeURIComponent(callbackUrl)}&response_type=code&scope=${encodeURIComponent(scopes)}&state=${encodeURIComponent(state)}&access_type=offline&prompt=consent`;
> 158	
> 159	    } else if (platform === "pinterest") {
> 160	      // App creds resolve per-user → env fallback → hard-fail (API Tenancy Model · FR-PE-008).
> 161	      const serviceClient = createClient(
> 162	        Deno.env.get("SUPABASE_URL")!,
> 163	        (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
> 164	      );
> 165	      let creds;
> 166	      try {
> 167	        creds = await resolveSocialAppCreds(serviceClient, userId, "pinterest");
> 168	      } catch (err) {
> 169	        const failClosed = socialAppConfigErrorResponse(err, corsHeaders);
> 170	        if (failClosed) return failClosed;
> 171	        throw err;
> 172	      }
> 173	      // Plan the FULL scope set up-front — adding a scope later forces a full re-authorization
> 174	      // (doc 10 §Pinterest). redirect_uri must match EXACTLY (no wildcard).
> 175	      const scopes = "boards:read,boards:write,pins:read,pins:write,user_accounts:read";
> 176	      authUrl = `${PINTEREST_AUTH_URL}?client_id=${encodeURIComponent(creds.clientId)}&redirect_uri=${encodeURIComponent(callbackUrl)}&response_type=code&scope=${encodeURIComponent(scopes)}&state=${encodeURIComponent(state)}`;
> 177	
> 178	    } else {
> 179	      return new Response(JSON.stringify({ error: `Platform ${platform} not yet supported for OAuth` }), {
> 180	        status: 400,
> 181	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 182	      });
> 183	    }
> 184	
> 185	    return new Response(JSON.stringify({ url: authUrl }), {
> 186	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 187	    });
> 188	  } catch (err) {
> 189	    console.error("social-auth-init error:", err);
> 190	    return new Response(JSON.stringify({ error: err instanceof Error ? err.message : String(err) }), {
> 191	      status: 500,
> 192	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 193	    });
> 194	  }
> 195	});
> 196	
> ```

## 🤖 Claude *(20:57:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -euo pipefail\nTOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\nAPI=\"https://api.supabase.com/v1/projects/${REF}/database/query\"\necho \"[1/3] applying 20260716190000_pat_allowlist_swarm_read.sql...\"\npython3 - <<'PY' > /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/scratchpad/swarm-mig.json 2>/dev/null || python3 - <<'PY2' > /tmp/swarm-mig.json\nimport json\nsql = open('supabase/migrations/20260716190000_pat_allowlist_swarm_read.sql').read()\nprint(json.dumps({'query': sql}))\nPY\nimport json\nsql = open('supabase/migrations/20260716190000_pat_allowlist_swarm_read.sql').read()\nprint(json.dumps({'query': sql}))\nPY2\nBODY=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/scratchpad/swarm-mig.json\n[ -s \"$BODY\" ] || BODY=/tmp/swarm-mig.json\nRES=$(curl -s -X POST \"$API\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" --data-binary @$BODY)\necho \"apply result: ${RES:0:300}\"\necho \"$RES\" | grep -qi '\"error\"' && { echo \"\u274c apply failed\"; exit 1; }\necho \"[2/3] registering in ledger...\"\ncurl -s -X POST \"$API\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"{\\\"query\\\":\\\"INSERT INTO supabase_migrations.schema_migrations (version, name) VALUES ('20260716190000', 'pat_allowlist_swarm_read') ON CONFLICT DO NOTHING;\\\"}\"\necho\necho \"[3/3] material proof \u2014 constraint definition:\"\ncurl -s -X POST \"$API\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"{\\\"query\\\":\\\"SELECT pg_get_constraintdef(oid) AS def FROM pg_constraint WHERE conname='scopes_allowed' AND conrelid='public.mcp_access_tokens'::regclass;\\\"}\"\necho",
  "description": "Aplicar migration swarm:read em prod via Management API + registrar ledger + prova material"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> claude-opus-4-8 is temporarily unavailable, so auto mode cannot determine the safety of Bash right now. Wait briefly and then try this action again. If it keeps failing, continue with other tasks that don't require this action and come back to it later. Note: reading files, searching code, and other read-only operations do not require the classifier and can still be used.
> ```

## 🤖 Claude *(20:57:18)*


## 🤖 Claude *(20:57:18)*


## 🤖 Claude *(20:57:19)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/social-app-config.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// Shared: per-user OAuth APP credential resolution for TikTok / YouTube / Pinterest.
> 2	// API Tenancy Model (CLAUDE.md): resolve credentials per-user first, env fallback as a
> 3	// Sovereign-only onboarding default (OTD-PE-SOCIAL-APPCREDS), hard-fail otherwise — never a
> 4	// silent shared key. BoK SSOT: docs/bok/post-engine/10-amendment-social-connect-*.md (FR-PE-005..009).
> 5	//
> 6	// Resolution order:
> 7	//   (1) social_app_config per-user (is_active=true) — read via the service-role decrypted_* view.
> 8	//   (2) env fallback — TIKTOK_CLIENT_KEY/SECRET · GOOGLE_CLIENT_ID/SECRET · PINTEREST_CLIENT_ID/SECRET.
> 9	//   (3) SocialAppConfigError(402) {error:"<platform>_not_configured", action:"Configure ... /dashboard/settings"}.
> 10	//
> 11	// SECURITY: client_secret lives encrypted in Vault; only the service-role decrypted_social_app_config view
> 12	// exposes plaintext. NEVER read the masked public view for the secret (it returns '••••••••••••').
> 13	
> 14	import type { SupabaseClient } from "https://esm.sh/@supabase/supabase-js@2";
> 15	
> 16	export type SocialAppPlatform = "tiktok" | "youtube" | "pinterest";
> 17	
> 18	export interface SocialAppCreds {
> 19	  clientId: string;
> 20	  clientSecret: string;
> 21	  scopes: string[] | null;
> 22	  metadata: Record<string, unknown>;
> 23	  source: "per-user" | "env";
> 24	}
> 25	
> 26	// Values are env-var NAMES (looked up in Deno.env), NOT secret values. The `*Env` suffix keeps them
> 27	// unambiguous to the secret-scan hook (a `secret: "..."` literal would false-positive).
> 28	const ENV_MAP: Record<SocialAppPlatform, { idEnv: string; secretEnv: string; label: string }> = {
> 29	  tiktok: { idEnv: "TIKTOK_CLIENT_KEY", secretEnv: "TIKTOK_CLIENT_SECRET", label: "TikTok" },
> 30	  youtube: { idEnv: "GOOGLE_CLIENT_ID", secretEnv: "GOOGLE_CLIENT_SECRET", label: "YouTube" },
> 31	  pinterest: { idEnv: "PINTEREST_CLIENT_ID", secretEnv: "PINTEREST_CLIENT_SECRET", label: "Pinterest" },
> 32	};
> 33	
> 34	/** Structured fail-closed error → maps to a 402 JSON body the client can act on. */
> 35	export class SocialAppConfigError extends Error {
> 36	  readonly httpStatus = 402;
> 37	  readonly body: { error: string; action: string };
> 38	  constructor(platform: string, label: string) {
> 39	    super(`${platform}_not_configured`);
> 40	    this.name = "SocialAppConfigError";
> 41	    this.body = {
> 42	      error: `${platform}_not_configured`,
> 43	      action: `Configure suas credenciais de app ${label} em /dashboard/settings`,
> 44	    };
> 45	  }
> 46	}
> 47	
> 48	/**
> 49	 * Resolve OAuth app credentials for a platform, scoped to a user.
> 50	 * @param supabase a SERVICE-ROLE client (reads the decrypted_social_app_config view).
> 51	 * @throws SocialAppConfigError(402) when neither per-user nor env credentials resolve.
> 52	 */
> 53	export async function resolveSocialAppCreds(
> 54	  supabase: SupabaseClient,
> 55	  userId: string,
> 56	  platform: SocialAppPlatform,
> 57	): Promise<SocialAppCreds> {
> 58	  const env = ENV_MAP[platform];
> 59	  if (!env) throw new SocialAppConfigError(platform, platform);
> 60	
> 61	  // (1) per-user
> 62	  if (userId) {
> 63	    const { data, error } = await supabase
> 64	      .from("decrypted_social_app_config")
> 65	      .select("client_id, client_secret, scopes, metadata, is_active")
> 66	      .eq("user_id", userId)
> 67	      .eq("platform", platform)
> 68	      .eq("is_active", true)
> 69	      .maybeSingle();
> 70	
> 71	    if (!error && data && data.client_id && data.client_secret) {
> 72	      return {
> 73	        clientId: String(data.client_id),
> 74	        clientSecret: String(data.client_secret),
> 75	        scopes: (data.scopes as string[] | null) ?? null,
> 76	        metadata: (data.metadata as Record<string, unknown>) ?? {},
> 77	        source: "per-user",
> 78	      };
> 79	    }
> 80	  }
> 81	
> 82	  // (2) env fallback (Sovereign-only onboarding default — OTD-PE-SOCIAL-APPCREDS)
> 83	  const envId = Deno.env.get(env.idEnv);
> 84	  const envSecret = Deno.env.get(env.secretEnv);
> 85	  if (envId && envSecret) {
> 86	    return { clientId: envId, clientSecret: envSecret, scopes: null, metadata: {}, source: "env" };
> 87	  }
> 88	
> 89	  // (3) hard fail
> 90	  throw new SocialAppConfigError(platform, env.label);
> 91	}
> 92	
> 93	/** Build a fail-closed Response from a thrown SocialAppConfigError (or rethrow others). */
> 94	export function socialAppConfigErrorResponse(err: unknown, corsHeaders: Record<string, string>): Response | null {
> 95	  if (err instanceof SocialAppConfigError) {
> 96	    return new Response(JSON.stringify(err.body), {
> 97	      status: err.httpStatus,
> 98	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 99	    });
> 100	  }
> 101	  return null;
> 102	}
> 103	
> ```

## 🤖 Claude *(20:57:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n -i \"pinterest\" supabase/functions/social-auth-callback/index.ts | head -20; echo \"---PUBLISH---\"; grep -rn -il \"pinterest\" supabase/functions/publish-social/ supabase/functions/publish-channel-variant/ 2>/dev/null; echo \"---MIGRATIONS---\"; grep -rln \"social_app_config\" supabase/migrations/ | sort; echo \"---UI---\"; grep -rln -i \"pinterest\\|social_app_config\" src/ --include=\"*.tsx\" --include=\"*.ts\" | head -20",
  "description": "Mapear footprint Pinterest no callback/publish + migrations e UI de social_app_config"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 90:    // Pinterest refresh_token_expires_at). Empty for platforms that don't need it.
> 261:    } else if (platform === "pinterest") {
> 263:      const creds = await resolveSocialAppCreds(supabase, userId, "pinterest");
> 265:      // Pinterest v5: client creds go in HTTP Basic auth, not the form body.
> 266:      const tokenRes = await fetch("https://api.pinterest.com/v5/oauth/token", {
> 280:        throw new Error(tokenData.error_description || tokenData.message || tokenData.error || "Pinterest token exchange failed");
> 293:      const meRes = await fetch("https://api.pinterest.com/v5/user_account", {
> ---PUBLISH---
> supabase/functions/publish-social/index.ts
> ---MIGRATIONS---
> supabase/migrations/20260627120000_social_app_config.sql
> ---UI---
> src/integrations/supabase/types.ts
> src/pages/SocialAccountsPage.tsx
> src/pages/CampaignWizard.tsx
> src/lib/publish-destinations.ts
> src/lib/social-app-config.ts
> src/pages/SettingsPage.tsx
> src/lib/smart-delete.ts
> src/test/format-specs.test.ts
> src/lib/format-specs.ts
> src/components/calendar/SmartDeleteDialog.tsx
> src/components/landing/FAQSection.tsx
> src/components/landing/FeaturesSection.tsx
> src/lib/canvas-node-registry.ts
> src/pages/DashboardHome.tsx
> src/pages/AnalyticsPage.tsx
> src/pages/CalendarPage.tsx
> src/components/creative/PublicationPreview.tsx
> src/components/icons/brand-icons.tsx
> src/components/canvas/RightPanel/inspectors/CadenceInspector.tsx
> src/components/settings/SocialAppConfigCard.tsx
> ```

## 🤖 Claude *(20:58:04)*


## 🤖 Claude *(20:58:04)*


## 🤖 Claude *(20:58:05)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260627120000_social_app_config.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: social_app_config — per-user OAuth APP credentials for TikTok / YouTube / Pinterest
> 2	--            (client_id + Vault-encrypted client_secret), keyed UNIQUE(user_id, platform).
> 3	-- ─────────────────────────────────────────────────────────────────────────────
> 4	-- BoK SSOT: docs/bok/post-engine/06-data-model.md (social_app_config) + 10-amendment-social-connect-*.md (FR-PE-005).
> 5	-- SOPs (Lei 2, written before this migration): docs/processes/{tiktok,youtube,pinterest}-publish-credential-resolution.md.
> 6	-- API Tenancy Model (CLAUDE.md): per-user credentials, RLS-isolated, Vault-encrypted secret, tenant-guarded writes.
> 7	-- Resolution order in edge functions: (1) social_app_config per-user (is_active) → (2) env fallback
> 8	--   (TIKTOK_CLIENT_KEY/SECRET, GOOGLE_CLIENT_ID/SECRET, PINTEREST_CLIENT_ID/SECRET — Sovereign-only onboarding
> 9	--   default, OTD-PE-SOCIAL-APPCREDS) → (3) hard fail 402/501 {error:"<platform>_not_configured"}.
> 10	--
> 11	-- This MIRRORS the canonical credential pattern of social_accounts (migrations 20260601000000 +
> 12	-- 20260602140000 idempotent vault_upsert_secret + 20260602150000 tenant guard), reproduced for a NEW
> 13	-- table that is born Vault-encrypted (no plaintext-then-backfill phase):
> 14	--   * client_id is a semi-public OAuth identifier → stored plaintext, readable.
> 15	--   * client_secret is a secret → encrypted at-rest in Vault by a BEFORE INSERT/UPDATE trigger; the base
> 16	--     column holds only the Vault secret UUID. Even a direct read of the base table never yields plaintext.
> 17	--   * Masked public VIEW returns '••••••••••••' for client_secret (security_invoker → RLS applies).
> 18	--   * decrypted_social_app_config exposes the real secret to service_role ONLY (edge functions).
> 19	--   * INSTEAD OF trigger maps view writes to the base table with the tenant guard (auth.uid()=user_id;
> 20	--     service_role exempt) + mask-preservation, closing the cross-tenant injection that a view's WHERE
> 21	--     does not constrain for INSERT.
> 22	--
> 23	-- Security posture: HARDENS. NO new SECURITY DEFINER RPC reachable by clients. MANDATORY /security-review
> 24	-- (credential layer, FMEA-011). Orphaned-secret revocation on disconnect is a follow-up RPC
> 25	-- (disconnect_social_app_config, mirroring 20260602160000) — deferred to the Settings-UI slice.
> 26	
> 27	-- ─────────────────────────────────────────────────────────────────────────────
> 28	-- 1. BASE TABLE — social_app_config_table (one row per user × platform)
> 29	-- ─────────────────────────────────────────────────────────────────────────────
> 30	CREATE TABLE IF NOT EXISTS public.social_app_config_table (
> 31	    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> 32	    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 33	    platform public.social_platform NOT NULL,
> 34	    client_id TEXT,                                        -- OAuth client_id / TikTok client_key (semi-public)
> 35	    client_secret TEXT,                                    -- secret → Vault UUID after trg_encrypt_social_app_config
> 36	    scopes TEXT[] NOT NULL DEFAULT '{}',
> 37	    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,           -- platform extras: youtube channel_id, pinterest board_id, redirect_uri override
> 38	    is_active BOOLEAN NOT NULL DEFAULT TRUE,
> 39	    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
> 40	    updated_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
> 41	    CONSTRAINT unique_user_platform_app_config UNIQUE (user_id, platform)
> 42	);
> 43	
> 44	ALTER TABLE public.social_app_config_table ENABLE ROW LEVEL SECURITY;
> 45	
> 46	-- Default-deny: only the owner tenant can touch their row (base-table RLS; service_role bypasses).
> 47	CREATE POLICY "Users manage their own social app config" ON public.social_app_config_table
> 48	    FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
> 49	
> 50	CREATE TRIGGER tr_update_social_app_config_updated_at
> 51	    BEFORE UPDATE ON public.social_app_config_table
> 52	    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
> 53	
> 54	CREATE INDEX IF NOT EXISTS idx_social_app_config_user ON public.social_app_config_table (user_id);
> 55	
> 56	-- Column-level hardening: the secret column is WRITE-ONLY for clients (BYOK paste via the masked view),
> 57	-- never returned via PostgREST. service_role (edge functions) reads it through decrypted_social_app_config.
> 58	-- Mirrors meta_config.long_lived_token (20260530210000) — proven compatible with the security_invoker view.
> 59	REVOKE SELECT (client_secret) ON public.social_app_config_table FROM anon, authenticated;
> 60	
> 61	-- ─────────────────────────────────────────────────────────────────────────────
> 62	-- 2. ENCRYPTION TRIGGER — client_secret → Vault (idempotent vault_upsert_secret, keyed by row id)
> 63	-- ─────────────────────────────────────────────────────────────────────────────
> 64	CREATE OR REPLACE FUNCTION public.trg_encrypt_social_app_config()
> 65	RETURNS TRIGGER
> 66	LANGUAGE plpgsql
> 67	SECURITY DEFINER
> 68	SET search_path = ''
> 69	AS $$
> 70	DECLARE
> 71	  v_secret_id UUID;
> 72	BEGIN
> 73	  IF NEW.id IS NULL THEN
> 74	    NEW.id := gen_random_uuid();
> 75	  END IF;
> 76	
> 77	  IF NEW.client_secret IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.client_secret IS DISTINCT FROM OLD.client_secret) THEN
> 78	    IF NEW.client_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 79	      -- already a Vault UUID reference → keep
> 80	    ELSE
> 81	      v_secret_id := public.vault_upsert_secret(
> 82	        NEW.client_secret,
> 83	        'social_app_config_client_secret_' || NEW.id::text,
> 84	        'Social app OAuth client secret'
> 85	      );
> 86	      NEW.client_secret = v_secret_id::text;
> 87	    END IF;
> 88	  END IF;
> 89	
> 90	  RETURN NEW;
> 91	END;
> 92	$$;
> 93	
> 94	CREATE OR REPLACE TRIGGER tr_encrypt_social_app_config
> 95	  BEFORE INSERT OR UPDATE ON public.social_app_config_table
> 96	  FOR EACH ROW EXECUTE FUNCTION public.trg_encrypt_social_app_config();
> 97	
> 98	-- ─────────────────────────────────────────────────────────────────────────────
> 99	-- 3. PUBLIC MASKED VIEW — security_invoker (RLS applies); client_secret hidden
> 100	-- ─────────────────────────────────────────────────────────────────────────────
> 101	CREATE OR REPLACE VIEW public.social_app_config WITH (security_invoker = true) AS
> 102	SELECT
> 103	  id,
> 104	  user_id,
> 105	  platform,
> 106	  client_id,
> 107	  CASE WHEN client_secret IS NOT NULL THEN '••••••••••••' ELSE NULL END AS client_secret,
> 108	  scopes,
> 109	  metadata,
> 110	  is_active,
> 111	  created_at,
> 112	  updated_at
> 113	FROM public.social_app_config_table;
> 114	
> 115	-- ─────────────────────────────────────────────────────────────────────────────
> 116	-- 4. INSTEAD OF TRIGGER — map view writes to base table (tenant guard + mask preservation)
> 117	-- ─────────────────────────────────────────────────────────────────────────────
> 118	CREATE OR REPLACE FUNCTION public.trg_instead_of_social_app_config()
> 119	RETURNS TRIGGER
> 120	LANGUAGE plpgsql
> 121	SECURITY DEFINER
> 122	SET search_path = ''
> 123	AS $$
> 124	BEGIN
> 125	  IF TG_OP = 'DELETE' THEN
> 126	    DELETE FROM public.social_app_config_table WHERE id = OLD.id;
> 127	    RETURN OLD;
> 128	  ELSIF TG_OP = 'INSERT' THEN
> 129	    -- Tenant guard (mirrors 20260602150000): a non-service-role caller may only write its OWN row.
> 130	    -- Closes the cross-tenant injection (spoofed user_id + fresh id) a view's WHERE does not constrain
> 131	    -- for INSERT. service_role (OAuth callbacks / cron) is exempt.
> 132	    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN
> 133	      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';
> 134	    END IF;
> 135	    INSERT INTO public.social_app_config_table (
> 136	      id, user_id, platform, client_id, client_secret, scopes, metadata, is_active
> 137	    ) VALUES (
> 138	      COALESCE(NEW.id, gen_random_uuid()), NEW.user_id, NEW.platform, NEW.client_id, NEW.client_secret,
> 139	      COALESCE(NEW.scopes, '{}'), COALESCE(NEW.metadata, '{}'::jsonb), COALESCE(NEW.is_active, TRUE)
> 140	    );
> 141	    RETURN NEW;
> 142	  ELSIF TG_OP = 'UPDATE' THEN
> 143	    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN
> 144	      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';
> 145	    END IF;
> 146	    UPDATE public.social_app_config_table SET
> 147	      user_id = NEW.user_id,
> 148	      platform = NEW.platform,
> 149	      client_id = NEW.client_id,
> 150	      -- preserve the stored secret when the client writes back the mask sentinel
> 151	      client_secret = COALESCE(NULLIF(NEW.client_secret, '••••••••••••'), public.social_app_config_table.client_secret),
> 152	      scopes = COALESCE(NEW.scopes, public.social_app_config_table.scopes),
> 153	      metadata = COALESCE(NEW.metadata, public.social_app_config_table.metadata),
> 154	      is_active = COALESCE(NEW.is_active, public.social_app_config_table.is_active),
> 155	      updated_at = now()
> 156	    WHERE id = OLD.id;
> 157	    RETURN NEW;
> 158	  END IF;
> 159	  RETURN NULL;
> 160	END;
> 161	$$;
> 162	
> 163	CREATE TRIGGER trg_instead_of_social_app_config
> 164	  INSTEAD OF INSERT OR UPDATE OR DELETE ON public.social_app_config
> 165	  FOR EACH ROW EXECUTE FUNCTION public.trg_instead_of_social_app_config();
> 166	
> 167	-- ─────────────────────────────────────────────────────────────────────────────
> 168	-- 5. PRIVATE DECRYPTED VIEW — real client_secret for service_role ONLY (edge functions)
> 169	-- ─────────────────────────────────────────────────────────────────────────────
> 170	CREATE OR REPLACE VIEW public.decrypted_social_app_config AS
> 171	SELECT
> 172	  sac.id,
> 173	  sac.user_id,
> 174	  sac.platform,
> 175	  sac.client_id,
> 176	  COALESCE(s_secret.decrypted_secret, sac.client_secret) AS client_secret,
> 177	  sac.scopes,
> 178	  sac.metadata,
> 179	  sac.is_active,
> 180	  sac.created_at,
> 181	  sac.updated_at
> 182	FROM public.social_app_config_table sac
> 183	LEFT JOIN vault.decrypted_secrets s_secret
> 184	  ON sac.client_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
> 185	  AND s_secret.id = sac.client_secret::uuid;
> 186	
> 187	REVOKE ALL ON public.decrypted_social_app_config FROM PUBLIC, anon, authenticated;
> 188	GRANT SELECT ON public.decrypted_social_app_config TO service_role;
> 189	
> ```

## 🤖 Claude *(20:58:07)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '255,330p' supabase/functions/social-auth-callback/index.ts; echo \"===PUBLISH-PINTEREST===\"; grep -n -B2 -A25 'pinterest' supabase/functions/publish-social/index.ts | head -80",
  "description": "Ler branch pinterest do callback e do publish-social"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>       const channelsData = await channelsRes.json();
>       const channel = channelsData.items?.[0];
>       platformUserId = channel?.id || null;
>       platformUsername = channel?.snippet?.title || platformUserId;
>       if (channel?.id) metadata = { ...metadata, channel_id: channel.id };
> 
>     } else if (platform === "pinterest") {
>       // App credentials resolve per-user → env fallback → hard-fail (FR-PE-005/009).
>       const creds = await resolveSocialAppCreds(supabase, userId, "pinterest");
> 
>       // Pinterest v5: client creds go in HTTP Basic auth, not the form body.
>       const tokenRes = await fetch("https://api.pinterest.com/v5/oauth/token", {
>         method: "POST",
>         headers: {
>           "Content-Type": "application/x-www-form-urlencoded",
>           Authorization: `Basic ${btoa(`${creds.clientId}:${creds.clientSecret}`)}`,
>         },
>         body: new URLSearchParams({
>           grant_type: "authorization_code",
>           code,
>           redirect_uri: callbackUrl,
>         }),
>       });
>       const tokenData = await tokenRes.json();
>       if (!tokenRes.ok || tokenData.error) {
>         throw new Error(tokenData.error_description || tokenData.message || tokenData.error || "Pinterest token exchange failed");
>       }
> 
>       accessToken = tokenData.access_token;
>       refreshToken = tokenData.refresh_token || null; // rotating
>       expiresIn = tokenData.expires_in ?? 2592000; // 30d
>       scopes = (tokenData.scope || "").split(/[\s,]+/).filter(Boolean);
>       // Persist the refresh-token expiry so the refresh path can keep the 60d rotation chain alive.
>       if (tokenData.refresh_token_expires_at) {
>         metadata = { ...metadata, refresh_token_expires_at: tokenData.refresh_token_expires_at };
>       }
> 
>       // Resolve identity → platform_username (no stable numeric id in v5 user_account).
>       const meRes = await fetch("https://api.pinterest.com/v5/user_account", {
>         headers: { Authorization: `Bearer ${accessToken}` },
>       });
>       const me = await meRes.json();
>       platformUsername = me.username || null;
>       platformUserId = me.username || null;
> 
>     } else {
>       throw new Error(`Unsupported platform: ${platform}`);
>     }
> 
>     const expiresAt = expiresIn
>       ? new Date(Date.now() + expiresIn * 1000).toISOString()
>       : null;
> 
>     // Upsert social account
>     const { error: dbError } = await supabase
>       .from("social_accounts")
>       .upsert(
>         {
>           user_id: userId,
>           platform,
>           access_token: accessToken,
>           refresh_token: refreshToken,
>           token_expires_at: expiresAt,
>           platform_user_id: platformUserId,
>           platform_username: platformUsername,
>           scopes,
>           metadata,
>           is_active: true,
>         },
>         { onConflict: "user_id,platform" }
>       );
> 
>     if (dbError) {
>       console.error("DB upsert error:", dbError);
>       await supabase.from("social_accounts").insert({
>         user_id: userId,
> ===PUBLISH-PINTEREST===
> 587-      pulse("ok", "youtube_upload_complete", { video_id: videoId, privacy_status: realPrivacyStatus });
> 588-
> 589:    } else if (platform === "pinterest") {
> 590-      // Pinterest API v5 — video pin (register → upload multipart → poll → create). User access_token only for
> 591-      // pin/board/media REST; the multipart upload itself carries NO Authorization (presigned S3 POST). video_url
> 592-      // from payload; cover_image_url must be a PUBLIC https URL (Pinterest fetches it async).
> 593:      const PIN_BASE = "https://api.pinterest.com/v5";
> 594-      const videoUrl = content.video_url;
> 595-      if (!videoUrl && !content.image_url) {
> 596:        pulse("degraded", "pinterest_no_media");
> 597-        throw new Error("PLATFORM_PUBLISH_FAILED");
> 598-      }
> 599-      const pinHeaders = {
> 600-        Authorization: `Bearer ${account.access_token}`,
> 601-        "Content-Type": "application/json",
> 602-      };
> 603-
> 604-      // (0) Ensure a destination board — prefer a cached metadata.board_id, else the first existing board, else
> 605-      // create one once. (Do NOT create a board per run.)
> 606-      let boardId: string | null = account.metadata?.board_id ?? null;
> 607-      if (!boardId) {
> 608-        const boardsRes = await fetch(`${PIN_BASE}/boards`, { headers: pinHeaders });
> 609-        const boardsData = await boardsRes.json().catch(() => ({}));
> 610-        if (!boardsRes.ok) {
> 611-          console.error("Pinterest boards list error:", boardsRes.status, boardsData);
> 612:          pulse("error", "pinterest_boards_failed", { status: boardsRes.status });
> 613-          throw new Error("PLATFORM_PUBLISH_FAILED");
> 614-        }
> 615-        boardId = boardsData?.items?.[0]?.id ?? null;
> 616-        if (!boardId) {
> 617-          const createBoardRes = await fetch(`${PIN_BASE}/boards`, {
> 618-            method: "POST",
> 619-            headers: pinHeaders,
> 620-            body: JSON.stringify({ name: "Gabriel AI", privacy: "PUBLIC" }),
> 621-          });
> 622-          const createBoardData = await createBoardRes.json().catch(() => ({}));
> 623-          if (!createBoardRes.ok || !createBoardData?.id) {
> 624-            console.error("Pinterest board create error:", createBoardRes.status, createBoardData);
> 625:            pulse("error", "pinterest_board_create_failed", { status: createBoardRes.status });
> 626-            throw new Error("PLATFORM_PUBLISH_FAILED");
> 627-          }
> 628-          boardId = createBoardData.id;
> 629-        }
> 630-      }
> 631-
> 632-      if (videoUrl) {
> 633-      // (1) Register the media upload → media_id + upload_url + upload_parameters.
> 634-      const mediaRes = await fetch(`${PIN_BASE}/media`, {
> 635-        method: "POST",
> 636-        headers: pinHeaders,
> 637-        body: JSON.stringify({ media_type: "video" }),
> 638-      });
> 639-      const mediaData = await mediaRes.json().catch(() => ({}));
> 640-      if (!mediaRes.ok || !mediaData?.media_id || !mediaData?.upload_url) {
> 641-        console.error("Pinterest media register error:", mediaRes.status, mediaData);
> 642:        pulse("error", "pinterest_media_register_failed", { status: mediaRes.status });
> 643-        throw new Error("PLATFORM_PUBLISH_FAILED");
> 644-      }
> 645-      const mediaId: string = mediaData.media_id;
> 646-      const uploadUrl: string = mediaData.upload_url;
> 647-      const uploadParams: Record<string, string> = mediaData.upload_parameters ?? {};
> 648-
> 649-      // (2) POST the MP4 to upload_url as multipart/form-data — ALL upload_parameters VERBATIM and the file LAST,
> 650-      // with NO Authorization header (presigned POST). Success = 204.
> 651-      const mp4Res = await fetchPublicUrl(videoUrl);
> 652-      if (!mp4Res.ok) {
> 653-        console.error("Pinterest video fetch error:", mp4Res.status);
> 654:        pulse("error", "pinterest_video_fetch_failed", { status: mp4Res.status });
> 655-        throw new Error("PLATFORM_PUBLISH_FAILED");
> 656-      }
> 657-      const videoBlob = await mp4Res.blob();
> 658-      const form = new FormData();
> 659-      for (const [k, v] of Object.entries(uploadParams)) form.append(k, v);
> 660-      form.append("file", videoBlob); // file field MUST be last (presigned-POST ordering).
> 661-      const uploadRes = await fetch(uploadUrl, { method: "POST", body: form });
> 662-      if (uploadRes.status !== 204 && !uploadRes.ok) {
> 663-        console.error("Pinterest media upload error:", uploadRes.status);
> 664:        pulse("error", "pinterest_upload_failed", { status: uploadRes.status });
> 665-        throw new Error("PLATFORM_PUBLISH_FAILED");
> 666-      }
> ```

## 🤖 Claude *(20:58:46)*


## 🤖 Claude *(20:58:46)*


## 🤖 Claude *(20:58:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -euo pipefail\ncd /home/gcrUX/htdocs/constellation-orchestra\nTOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\nAPI=\"https://api.supabase.com/v1/projects/${REF}/database/query\"\necho \"[1/3] applying 20260716190000_pat_allowlist_swarm_read.sql...\"\npython3 -c \"import json; print(json.dumps({'query': open('supabase/migrations/20260716190000_pat_allowlist_swarm_read.sql').read()}))\" > /tmp/swarm-mig.json\nRES=$(curl -s -X POST \"$API\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" --data-binary @/tmp/swarm-mig.json)\necho \"apply result: ${RES:0:300}\"\necho \"$RES\" | grep -qi '\"error\"' && { echo \"\u274c apply failed\"; exit 1; }\necho \"[2/3] registering in ledger...\"\ncurl -s -X POST \"$API\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"{\\\"query\\\":\\\"INSERT INTO supabase_migrations.schema_migrations (version, name) VALUES ('20260716190000', 'pat_allowlist_swarm_read') ON CONFLICT DO NOTHING;\\\"}\"\necho\necho \"[3/3] material proof \u2014 constraint definition:\"\ncurl -s -X POST \"$API\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"{\\\"query\\\":\\\"SELECT pg_get_constraintdef(oid) AS def FROM pg_constraint WHERE conname='scopes_allowed' AND conrelid='public.mcp_access_tokens'::regclass;\\\"}\"\necho",
  "description": "Aplicar migration swarm:read em prod (GO Sovereign) + ledger + prova material"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [1/3] applying 20260716190000_pat_allowlist_swarm_read.sql...
> apply result: []
> [2/3] registering in ledger...
> []
> [3/3] material proof — constraint definition:
> [{"def":"CHECK (((scopes <@ ARRAY['vision:read'::text, 'deepsearch:run'::text, 'mesh:read'::text, 'mesh:write'::text, 'swarm:read'::text]) AND (array_length(scopes, 1) >= 1)))"}]
> ```

## 🤖 Claude *(20:59:18)*


## 🤖 Claude *(20:59:18)*


## 🤖 Claude *(20:59:47)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'recon-pinterest-admin-keys',\n  description: 'Mapear AdminPage, SocialAccountsPage, env-usage de app creds, molde SocialAppConfigCard e BoK/SOP para a fatia Pinterest + Admin Global Keys',\n  phases: [\n    { title: 'Recon', detail: '5 leitores paralelos sobre os subsistemas afetados' },\n  ],\n}\n\nphase('Recon')\n\nconst FRONTS = [\n  {\n    key: 'admin-page',\n    prompt: `Repo: /home/gcrUX/htdocs/constellation-orchestra. Find the page serving route /dashboard/admin (check src/App.tsx routing) and read it fully plus its hooks (useAdminData?) and admin gating.\nAnswer with file:line refs:\n1. Component structure: sections/cards/tabs on the admin page today (list them).\n2. How admin gating works client-side (has_role usage \u2014 confirm the EXACT signature: single-arg has_role(app_role) vs two-arg) and how any admin-only edge fn or RLS policy checks admin.\n3. The exact SQL definition of has_role if findable in migrations (grep supabase/migrations for 'has_role').\n4. Existing hooks pattern for admin data.\n5. Where a new \"Chaves de Aplicativo (Globais)\" card + a \"rota\u00e7\u00e3o pendente\" reminder banner would slot in (layout conventions, pt-BR UI copy style).\n6. Does any notifications/reminders mechanism exist that admin page could reuse (notifications table, useNotifications)?`,\n  },\n  {\n    key: 'social-page',\n    prompt: `Repo: /home/gcrUX/htdocs/constellation-orchestra. Read src/pages/SocialAccountsPage.tsx fully + src/hooks/useSocialAccounts.ts (or equivalent) + src/components/icons/brand-icons.tsx.\nAnswer with file:line refs:\n1. Which platforms are listed for connection today \u2014 is Pinterest already a connect card? Exact platform list with labels.\n2. How the connect flow starts client-side (invoke social-auth-init with what body? redirect_uri value sent?).\n3. Is there a Pinterest brand icon in brand-icons.tsx? (lucide-react 1.11 removed brand icons \u2014 check the custom svg pattern.)\n4. How connection state/badges shown (is_active pattern) and how disconnect works (disconnect_social RPC).\n5. What exactly (if anything) must change in this page for Pinterest connect to work once app creds exist.`,\n  },\n  {\n    key: 'env-sweep',\n    prompt: `Repo: /home/gcrUX/htdocs/constellation-orchestra. Sweep ALL edge functions for global OAuth APP credential reads. Run: grep -rn \"LINKEDIN_CLIENT\\\\|TWITTER_CLIENT\\\\|INSTAGRAM_APP\\\\|INSTAGRAM_CLIENT\\\\|TIKTOK_CLIENT\\\\|GOOGLE_CLIENT\\\\|PINTEREST_CLIENT\\\\|META_APP\" supabase/functions/ --include=\"*.ts\"\nFor each hit, read enough context to answer:\n1. Complete map: platform \u2192 env var names \u2192 which functions read them \u2192 in which flow (authorize URL build, token exchange, token REFRESH, webhook verify).\n2. CRITICAL: find the token-refresh path(s) (is there a social-token-refresh fn, or refresh inline in publish-social/youtube-data?) \u2014 token refresh needs app creds too; list where each platform refreshes.\n3. Which of these already use resolveSocialAppCreds from _shared/social-app-config.ts vs raw Deno.env.\n4. Also grep supabase/functions/ for \"tiktok_identities\\\\|social_app_config\" to map the TikTok Login Kit fns and which creds they use.\nReturn an exhaustive table: platform | env vars | functions reading raw env | functions using resolver.`,\n  },\n  {\n    key: 'settings-card',\n    prompt: `Repo: /home/gcrUX/htdocs/constellation-orchestra. Read src/components/settings/SocialAppConfigCard.tsx fully + src/lib/social-app-config.ts + how SettingsPage mounts it.\nAnswer with file:line refs:\n1. The full UX pattern of the per-user app-credentials card (fields, masked secret handling, .insert vs .upsert pattern per the encrypted-views write pattern, platform selector).\n2. The client lib API (types, SAFE columns select, mutations).\n3. Which platforms the card supports today.\n4. What a sibling ADMIN card (global rows) could reuse verbatim vs what must differ (user_id NULL, admin gating, listing all platforms).\n5. Any existing tests for this card/lib.`,\n  },\n  {\n    key: 'bok-sop',\n    prompt: `Repo: /home/gcrUX/htdocs/constellation-orchestra. Read:\n1. docs/bok/post-engine/10-amendment-social-connect-*.md (glob it) \u2014 summarize FR-PE-005..009 (per-user app creds), what it says about Pinterest (\u00a7Pinterest), redirect URI guidance, scopes plan, and whether a GLOBAL/admin credential tier is mentioned or explicitly deferred (OTD-PE-SOCIAL-APPCREDS \u2014 find its definition).\n2. docs/processes/pinterest-publish-credential-resolution.md (if exists) \u2014 Operator/Sequence/Gates summary.\n3. grep supabase/migrations for \"social_platform\" enum creation/alteration \u2014 list the EXACT enum values allowed today (does it include 'pinterest'?).\n4. Check docs/bok/post-engine/00-index.md for the amendment numbering (what number would a new amendment take?).\n5. grep docs/processes/ for any existing admin-credentials or global-credentials SOP.\nReturn: exact FR ids, OTD ids, enum values, amendment numbering, and any BoK language that constrains the global-tier design.`,\n  },\n]\n\nconst RESULT_SCHEMA = {\n  type: 'object',\n  properties: {\n    findings: { type: 'string', description: 'Structured findings in markdown with file:line refs' },\n    key_facts: { type: 'array', items: { type: 'string' }, description: 'Load-bearing exact facts (signatures, enum values, env var names, FR/OTD ids)' },\n    gaps_or_risks: { type: 'array', items: { type: 'string' } },\n  },\n  required: ['findings', 'key_facts'],\n}\n\nconst results = await parallel(FRONTS.map(f => () =>\n  agent(f.prompt, { label: `recon:${f.key}`, phase: 'Recon', schema: RESULT_SCHEMA })\n    .then(r => ({ key: f.key, ...r }))\n))\n\nreturn { fronts: results.filter(Boolean) }"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wcr7hq0ki
> Summary: Mapear AdminPage, SocialAccountsPage, env-usage de app creds, molde SocialAppConfigCard e BoK/SOP para a fatia Pinterest + Admin Global Keys
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/subagents/workflows/wf_75660c54-ef3
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/workflows/scripts/recon-pinterest-admin-keys-wf_75660c54-ef3.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/workflows/scripts/recon-pinterest-admin-keys-wf_75660c54-ef3.js"} to iterate without resending the script.)
> Run ID: wf_75660c54-ef3
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/workflows/scripts/recon-pinterest-admin-keys-wf_75660c54-ef3.js", resumeFromRunId: "wf_75660c54-ef3"}) — completed agents return cached results (cached results may themselves be empty — inspect journal.jsonl before assuming there is something to recover).
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(21:00:09)*


## 🤖 Claude *(21:00:09)*


## 🤖 Claude *(21:00:10)*


🛠️ **Tool Call**: `ToolSearch`
```json
{
  "query": "select:TaskCreate,TaskUpdate,TaskList",
  "max_results": 3
}
```

> **Tool Result (ToolSearch)** - ✅ Success
>
> ```
> [{'type': 'tool_reference', 'tool_name': 'TaskCreate'}, {'type': 'tool_reference', 'tool_name': 'TaskUpdate'}, {'type': 'tool_reference', 'tool_name': 'TaskList'}]
> ```

## 🤖 Claude *(21:00:15)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Aplicar migration swarm:read em prod + ledger + prova",
  "description": "Migration 20260716190000_pat_allowlist_swarm_read.sql via Management API. DONE: apply [], ledger registrado, prova material = constraint def com swarm:read no CHECK de mcp_access_tokens."
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #1 created successfully: Aplicar migration swarm:read em prod + ledger + prova
> ```

## 🤖 Claude *(21:00:19)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Reconhecimento Pinterest/Admin Global Keys (wf_75660c54)",
  "description": "Workflow 5 frentes: admin-page \u00b7 social-page \u00b7 env-sweep \u00b7 settings-card \u00b7 bok-sop. J\u00e1 provado inline: init/callback/publish-social t\u00eam branch pinterest completo; social_app_config per-user Vault-encrypted (migration 20260627120000); resolver _shared/social-app-config.ts com ENV_MAP tiktok/youtube/pinterest; redirect URI = https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback.",
  "activeForm": "Mapeando subsistemas da fatia Pinterest/Admin"
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #2 created successfully: Reconhecimento Pinterest/Admin Global Keys (wf_75660c54)
> ```

## 🤖 Claude *(21:00:22)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "BoK amendment + SOP \u2014 Admin Global App Credentials",
  "description": "Amendment na BoK post-engine (camada global-admin de credenciais de app OAuth: linhas globais em social_app_config OU tabela dedicada; resolver per-user \u2192 global \u2192 env \u2192 402) + Pattern Conformance inline + SOP Lei 2 docs/processes/admin-global-app-credentials.md ANTES do c\u00f3digo. Inclui lembrete de rota\u00e7\u00e3o de credenciais na AdminPage."
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #3 created successfully: BoK amendment + SOP — Admin Global App Credentials
> ```

## 🤖 Claude *(21:00:24)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Migration camada global de credenciais + /security-review",
  "description": "Migration para linhas globais (admin-managed) de app credentials com Vault encryption reusada + RLS admin-only (has_role) + guard no INSTEAD OF trigger. OBRIGAT\u00d3RIO /security-review antes do commit (FMEA-011)."
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #4 created successfully: Migration camada global de credenciais + /security-review
> ```

## 🤖 Claude *(21:00:27)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Admin UI \u2014 Chaves de Aplicativo Globais + lembrete de rota\u00e7\u00e3o",
  "description": "Card na AdminPage (/dashboard/admin): CRUD mascarado das credenciais globais de app (Google, TikTok, Pinterest, LinkedIn, Twitter/X, Instagram/Meta) gravando via view mascarada (padr\u00e3o .insert/UPDATE-first, nunca upsert em encrypted view) + banner \"rota\u00e7\u00e3o pendente\" (SA Vertex \u00b7 Gemini \u00b7 Telegram) com marcar-como-rotacionada. UI pt-BR."
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #5 created successfully: Admin UI — Chaves de Aplicativo Globais + lembrete de rotação
> ```

## 🤖 Claude *(21:00:30)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Resolver global-tier nos edge fns + Pinterest connect card",
  "description": "Estender resolveSocialAppCreds: per-user \u2192 global row \u2192 env \u2192 402. Avaliar migrar linkedin/instagram/twitter dos Deno.env crus para o resolver (env vira fallback). Garantir card Pinterest em /dashboard/social (verificar SocialAccountsPage + brand icon). Deploy social-auth-init/callback + publish-social se tocados."
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #6 created successfully: Resolver global-tier nos edge fns + Pinterest connect card
> ```

## 🤖 Claude *(21:00:32)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Witness E2E Pinterest \u2014 connect + credencial global via admin UI",
  "description": "Sovereign cola App ID + Secret na admin UI nova \u2192 conecta Pinterest em /dashboard/social \u2192 social_accounts linha is_active com scopes. Prova material: linha no DB + badge conectado. Publish real de pin fica gated (Trial Access do Pinterest)."
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #7 created successfully: Witness E2E Pinterest — connect + credencial global via admin UI
> ```

## 🤖 Claude *(21:00:38)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "1",
  "status": "completed"
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #1 status
> ```

## 🤖 Claude *(21:00:38)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "2",
  "status": "in_progress"
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #2 status
> ```

## 🤖 Claude *(21:00:39)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "4",
  "addBlockedBy": [
    "3"
  ]
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #4 blockedBy
> ```

## 🤖 Claude *(21:00:39)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "5",
  "addBlockedBy": [
    "4"
  ]
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #5 blockedBy
> ```

## 🤖 Claude *(21:00:40)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "6",
  "addBlockedBy": [
    "4"
  ]
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #6 blockedBy
> ```

## 🤖 Claude *(21:00:40)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "7",
  "addBlockedBy": [
    "5",
    "6"
  ]
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #7 blockedBy
> ```

## 🤖 Claude *(21:01:16)*


## 🤖 Claude *(21:01:16)*

Loop armado e tracking ativo. **Update executivo parcial enquanto o reconhecimento roda:**

---

## ✅ Já entregue neste turno

**1. Migration `swarm:read` VIVA em prod** (GO executado):
- Apply via Management API: `[]` (sem erro) · ledger `schema_migrations` registrado
- **Prova material (Lei 1):** `pg_get_constraintdef` → `CHECK ((scopes <@ ARRAY['vision:read','deepsearch:run','mesh:read','mesh:write','swarm:read']) AND (array_length(scopes,1) >= 1))`
- PAT externo agora pode carregar `swarm:read` → a tool `vision.parse_sensory_gate` fica alcançável de fora. Sub-fatia PAT da Fatia 2 do predictive-swarm **fechada ponta-a-ponta**.

**2. Descoberta material do reconhecimento:** o trilho Pinterest está **muito mais pronto do que parecia** — uma sessão anterior (post-engine doc 10, FR-PE-005..009) já deixou:
- `social-auth-init` com branch pinterest (scopes `boards:read,boards:write,pins:read,pins:write,user_accounts:read`)
- `social-auth-callback` com token exchange v5 (Basic auth) + identidade `/v5/user_account` + refresh rotativo 30d/60d
- `publish-social` com pin de vídeo completo (register → upload multipart presigned → poll → create + gestão de boards)
- `social_app_config` Vault-encrypted per-user + card em Settings

O que falta de verdade é exatamente o que você pediu: **a camada GLOBAL/admin** (hoje o fallback global é `Deno.env` — que exige CLI) + o card de connect no `/dashboard/social`.

---

## 📌 AÇÃO SUA AGORA — Console Pinterest

Cole este **Link de redirecionamento** (precisa ser EXATO, sem wildcard):

```
https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback
```

Dois avisos honestos:
- **Não precisa gerar o token de acesso** do console — ele é só para explorar a API manualmente. Nosso fluxo OAuth completo pede os 5 escopos (incluindo `pins:write`/`boards:write`, que o token de teste não cobre).
- **Guarde o App ID + Chave secreta** — assim que eu shippar a UI admin (próximas iterações deste loop), você cola os dois lá direto, sem `.env` nem `npx supabase`.

---

## 🔄 Loop em andamento (fila armada)

| # | Item | Estado |
|---|------|--------|
| 1 | swarm:read em prod | ✅ |
| 2 | Reconhecimento 5 frentes (`wf_75660c54`) | 🔄 rodando |
| 3 | BoK amendment + SOP (Lei 2) — Admin Global App Credentials | ⏳ |
| 4 | Migration camada global + `/security-review` | ⏳ |
| 5 | Admin UI — chaves globais + **banner de rotação pendente** (SA Vertex · Gemini · Telegram) | ⏳ |
| 6 | Resolver global-tier nos edge fns + card Pinterest no `/dashboard/social` | ⏳ |
| 7 | Witness E2E: você cola as chaves na admin UI → conecta Pinterest | 🔒 gate seu |

Anotado também: wildcard `gcrux.com`, reconexão X, app-audit IG/TikTok e OTD-PSW-001 (GPU) ficam **adiados até os créditos Vertex acabarem** — te aviso item a item quando cada um precisar de você. Continuo assim que o reconhecimento retornar.

## 👤 User *(21:09:55)*

<task-notification>
<task-id>wcr7hq0ki</task-id>
<tool-use-id>toolu_01VF6ny91w38LwBqsKNcHdVX</tool-use-id>
<output-file>/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/tasks/wcr7hq0ki.output</output-file>
<status>completed</status>
<summary>Dynamic workflow "Mapear AdminPage, SocialAccountsPage, env-usage de app creds, molde SocialAppConfigCard e BoK/SOP para a fatia Pinterest + Admin Global Keys" completed</summary>
<result>{"fronts":[{"key":"admin-page"},{"key":"social-page"},{"key":"env-sweep","findings":"# OAuth APP Credential Sweep — supabase/functions/ (2026-07-16)\n\n## 1. Exhaustive map: platform | env vars | functions reading raw env | functions using resolver\n\n| Platform | Env vars | Functions reading raw `Deno.env` | Functions using `resolveSocialAppCreds` (per-user → env → 402) |\n|---|---|---|---|\n| **LinkedIn** | `LINKEDIN_CLIENT_ID`, `LINKEDIN_CLIENT_SECRET` | `social-auth-init/index.ts:69` (authorize URL, ID only) · `social-auth-callback/index.ts:94-95` (token exchange) · `refresh-social-token/index.ts:92-93` (REFRESH) | — none |\n| **Instagram / Facebook (Meta)** | `INSTAGRAM_APP_ID`, `INSTAGRAM_APP_SECRET`, `META_APP_SECRET`, `META_WEBHOOK_VERIFY_TOKEN`, `INSTAGRAM_WEBHOOK_VERIFY_TOKEN` | `social-auth-init/index.ts:80` (authorize URL, APP_ID only) · `social-auth-callback/index.ts:124-125,147` (token exchange short→long-lived `ig_exchange_token`) · `refresh-social-token/index.ts:102` (REFRESH via `fb_exchange_token`) · `whatsapp-webhook/index.ts:68` (GET verify token) + `:89` (POST HMAC sig: `META_APP_SECRET \\|\\| INSTAGRAM_APP_SECRET`) · `instagram-webhook/index.ts:16` (GET verify token, hardcoded default `\"mcorch_ig_webhook_2026\"`) + `:32` (POST HMAC sig: `INSTAGRAM_APP_SECRET ?? META_APP_SECRET`) | — none |\n| **Twitter / X** | `TWITTER_CLIENT_ID`, `TWITTER_CLIENT_SECRET` | `social-auth-init/index.ts:91` (authorize URL, ID only) · `social-auth-callback/index.ts:160-161` (token exchange, Basic auth) · `refresh-social-token/index.ts:117-118` (REFRESH, Basic auth) | — none |\n| **TikTok (connect flow)** | `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET` (read ONLY inside resolver as fallback, `_shared/social-app-config.ts:29,83-84`) | — no raw reads in flow code | `social-auth-init/index.ts:114` (authorize) · `social-auth-callback/index.ts:197` (exchange) · `refresh-social-token/index.ts:151` (REFRESH + rotating refresh_token re-store `:171-176`) |\n| **TikTok (Login Kit — pre-auth, no user)** | same `TIKTOK_CLIENT_KEY`/`TIKTOK_CLIENT_SECRET` as env **override** | `_shared/tiktok-login-creds.ts:24-25` — `resolveTikTokLoginCreds`: env FIRST → single active row of `decrypted_social_app_config` (INVERSE order vs resolveSocialAppCreds; returns `null` → 501, not 402) | Uses its OWN resolver (`resolveTikTokLoginCreds`), consumed by: `tiktok-login-init/index.ts:45` (authorize) · `_shared/tiktok-login-flow.ts:55` (exchange), called from BOTH `tiktok-login-callback/index.ts:30` and `social-auth-callback/index.ts:50-58` (login-intent branch). `tiktok-login-session` uses NO app creds (one-time code → Supabase session only) |\n| **YouTube / Google** | `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` (fallback inside resolver only, `social-app-config.ts:30`) | — no raw reads | `social-auth-init/index.ts:133` (authorize, `access_type=offline&amp;prompt=consent`) · `social-auth-callback/index.ts:225` (exchange) · `refresh-social-token/index.ts:186` (REFRESH) |\n| **Pinterest** | `PINTEREST_CLIENT_ID`, `PINTEREST_CLIENT_SECRET` (fallback inside resolver only, `social-app-config.ts:31`) | — no raw reads | `social-auth-init/index.ts:167` (authorize) · `social-auth-callback/index.ts:263` (exchange, Basic auth) · `refresh-social-token/index.ts:221` (REFRESH + rotating token + `refresh_token_expires_at` metadata `:243-254`) |\n\n## 2. CRITICAL — Token refresh topology\n\nThere IS a dedicated refresh function: **`supabase/functions/refresh-social-token/index.ts`** is the SINGLE refresh chokepoint for ALL platforms. No platform refreshes anywhere else.\n\n- **LinkedIn** (`:79-99`): `grant_type=refresh_token` with **raw env** `LINKEDIN_CLIENT_ID/SECRET`.\n- **Instagram/Facebook** (`:100-109`): `fb_exchange_token` (uses the current `access_token`, not a refresh_token) with **raw env** `INSTAGRAM_APP_ID/SECRET` interpolated directly into the URL.\n- **Twitter** (`:110-142`): `grant_type=refresh_token` with **raw env** `TWITTER_CLIENT_ID/SECRET`; re-stores rotated `refresh_token`.\n- **TikTok** (`:143-177`): via `resolveSocialAppCreds(admin, account.user_id, \"tiktok\")`; TikTok rotates refresh_token on EVERY refresh — re-stored before shared update.\n- **YouTube** (`:178-212`): via resolver; never nulls an existing refresh_token.\n- **Pinterest** (`:213-255`): via resolver, Basic auth; rotating refresh_token + expiry chain in metadata.\n\nCallers that DELEGATE to it (no inline refresh, no app creds of their own):\n- `publish-social/index.ts:87` — POSTs to `refresh-social-token` when token near expiry, then re-reads `decrypted_social_accounts` (`:103-110`).\n- `youtube-data/index.ts:54` — same pattern (`:42-52` comment: never touches raw refresh_token).\n\nMeta-family fns `publish-meta` and `sync-meta-ads` read ZERO app creds — they use per-user `meta_config` 60d BYOK tokens (no app-cred refresh in those paths). The `instagram`/`facebook` rows in `social_accounts` refresh only through `refresh-social-token`'s raw-env branch.\n\nFail-closed handling: `refresh-social-token/index.ts:293-296`, `social-auth-init` (per-platform try/catch), and `social-auth-callback` map `SocialAppConfigError` → structured 402 `{error:\"&lt;platform&gt;_not_configured\"}`. The legacy trio instead returns 500 \"not configured\" (init) or throws (callback/refresh) when env is missing.\n\n## 3. Resolver vs raw env — the asymmetry\n\n`_shared/social-app-config.ts` (`resolveSocialAppCreds`) covers ONLY `tiktok | youtube | pinterest` (`SocialAppPlatform` type, ENV_MAP `:28-32`). Resolution: (1) `decrypted_social_app_config` per-user `is_active=true` → (2) env fallback → (3) `SocialAppConfigError` 402.\n\n**LinkedIn, Instagram/Facebook, and Twitter/X are NOT in the resolver at all** — they read global env directly in all three flow stages (authorize, exchange, refresh) plus the two Meta webhooks. These are the remaining global-app-credential surfaces violating the API Tenancy Model's per-user-first rule.\n\n## 4. TikTok Login Kit map (`tiktok_identities` / `social_app_config` grep)\n\nFiles: `tiktok-login-init/index.ts`, `_shared/tiktok-login-flow.ts`, `_shared/tiktok-login-creds.ts`, `_shared/social-app-config.ts`, `social-auth-init/index.ts`.\n\n- `tiktok-login-init` — builds authorize URL with `resolveTikTokLoginCreds` (`:45`); no creds → **501** `tiktok_login_not_configured`; reuses `social-auth-callback` as redirect_uri; browser-binding hash in signed state.\n- `_shared/tiktok-login-flow.ts` — `handleTikTokLoginCallback`: token exchange at `https://open.tiktokapis.com/v2/oauth/token/` (`:58-68`) with the SAME login creds; find-or-create in **`tiktok_identities`** keyed strictly on `open_id` (`:79-96`, never by email); TikTok tokens discarded after `open_id`; one-time hand-off code in `tiktok_login_codes`.\n- `tiktok-login-callback` — standalone backward-compat wrapper; redirect_uri = itself.\n- `social-auth-callback:48-59` — primary login path: dispatches on signed `intent:\"login\"` state before connect logic; redirect_uri = social-auth-callback.\n- `tiktok-login-session` — redeems one-time code for a Supabase session; **no app creds**.\n- `decrypted_social_app_config` view is read by BOTH resolvers: per-user filtered (`social-app-config.ts:63-69`) vs global single-active-row no user filter (`tiktok-login-creds.ts:28-34`, flagged single-tenant-only in its header comment).","key_facts":["refresh-social-token is the ONLY token-refresh path for all 6 platforms; publish-social/index.ts:87 and youtube-data/index.ts:54 delegate to it via HTTP and re-read decrypted_social_accounts","LinkedIn/Instagram/Twitter use RAW Deno.env in all 3 stages: LINKEDIN_CLIENT_ID/SECRET, INSTAGRAM_APP_ID/SECRET, TWITTER_CLIENT_ID/SECRET (social-auth-init:69,80,91 · social-auth-callback:94-95,124-125,160-161 · refresh-social-token:92-93,102,117-118)","TikTok/YouTube/Pinterest use resolveSocialAppCreds from _shared/social-app-config.ts (per-user decrypted_social_app_config -&gt; env fallback TIKTOK_CLIENT_KEY/SECRET, GOOGLE_CLIENT_ID/S
... (truncated 15099 chars, full result in /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/tasks/wcr7hq0ki.output)</result>
<diagnostics>Per-agent results: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/subagents/workflows/wf_75660c54-ef3/journal.jsonl — one {"type":"result",...} line per completed agent with its full return value.
If the result above is empty or unexpected, Read this file BEFORE diagnosing — do not assume agents returned non-empty results.
To re-run with edited post-processing: Workflow({scriptPath: '/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/workflows/scripts/recon-pinterest-admin-keys-wf_75660c54-ef3.js', resumeFromRunId: 'wf_75660c54-ef3'}) — agents whose (prompt, opts) are unchanged replay from cache.</diagnostics>
<failures>[recon:admin-page] failed: API Error: 529 Overloaded. This is a server-side issue, usually temporary — try again in a moment. If it persists, check https://status.claude.com.
[recon:social-page] failed: API Error: 529 Overloaded. This is a server-side issue, usually temporary — try again in a moment. If it persists, check https://status.claude.com.
[recon:bok-sop] failed: API Error: 529 Overloaded. This is a server-side issue, usually temporary — try again in a moment. If it persists, check https://status.claude.com.</failures>
<usage><agent_count>5</agent_count><agents_done>2</agents_done><agents_error>3</agents_error><agents_skipped>0</agents_skipped><agents_empty_result>0</agents_empty_result><subagent_tokens>202852</subagent_tokens><tool_uses>29</tool_uses><duration_ms>603352</duration_ms></usage>
</task-notification>

## 🤖 Claude *(21:10:08)*


## 🤖 Claude *(21:10:09)*

Reconhecimento parcial: `env-sweep` e `settings-card` completos (ouro — mapa exaustivo do chokepoint de refresh), mas 3 frentes caíram em 529 Overloaded. Lendo o resultado completo e re-rodando as falhas via resume (cache preserva as 2 prontas):

## 🤖 Claude *(21:10:13)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "python3 - <<'PY'\nimport json\ndata = open('/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/tasks/wcr7hq0ki.output').read()\n# find the settings-card front in the JSON-ish output\nidx = data.find('\"key\":\"settings-card\"')\nprint(data[idx:idx+9000] if idx>=0 else \"settings-card NOT in output head; checking journal\")\nPY",
  "description": "Extrair resultado da frente settings-card do output do workflow"
}
```

## 🤖 Claude *(21:10:15)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "scriptPath": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/workflows/scripts/recon-pinterest-admin-keys-wf_75660c54-ef3.js",
  "resumeFromRunId": "wf_75660c54-ef3"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> settings-card NOT in output head; checking journal
> ```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wlnkrlfc4
> Summary: Mapear AdminPage, SocialAccountsPage, env-usage de app creds, molde SocialAppConfigCard e BoK/SOP para a fatia Pinterest + Admin Global Keys
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/subagents/workflows/wf_75660c54-ef3
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/workflows/scripts/recon-pinterest-admin-keys-wf_75660c54-ef3.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/workflows/scripts/recon-pinterest-admin-keys-wf_75660c54-ef3.js"} to iterate without resending the script.)
> Run ID: wf_75660c54-ef3
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/workflows/scripts/recon-pinterest-admin-keys-wf_75660c54-ef3.js", resumeFromRunId: "wf_75660c54-ef3"}) — completed agents return cached results (cached results may themselves be empty — inspect journal.jsonl before assuming there is something to recover).
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(21:10:29)*


## 🤖 Claude *(21:10:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "python3 - <<'PY'\nimport json\npath='/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/subagents/workflows/wf_75660c54-ef3/journal.jsonl'\nfor line in open(path):\n    try:\n        rec=json.loads(line)\n    except: continue\n    if rec.get('type')=='result':\n        label=rec.get('label') or rec.get('key') or ''\n        val=rec.get('result') or rec.get('value')\n        s=json.dumps(val)[:200] if val else 'EMPTY'\n        print('---', label, '---')\n        if 'settings-card' in json.dumps(rec)[:400]:\n            print(json.dumps(val, ensure_ascii=False)[:8000])\n        else:\n            print(s)\nPY",
  "description": "Ler journal do workflow \u2014 extrair resultado settings-card"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> --- v2:5987cbf9530c1a53a1d790d33b901c68f1c6f0a2fa737f7f1c774860dcd0ac65 ---
> {"findings": "# SocialAppConfigCard \u2014 full anatomy\n\n## 1. UX pattern of the per-user app-credentials card\n\n**File:** `/home/gcrUX/htdocs/constellation-orchestra/src/components/settings/Social
> --- v2:d016d4a0a3581591367a917448818aa50ac32c1748aaa65c3e278966ef6acda5 ---
> {"findings": "# OAuth APP Credential Sweep \u2014 supabase/functions/ (2026-07-16)\n\n## 1. Exhaustive map: platform | env vars | functions reading raw env | functions using resolver\n\n| Platform | E
> ```

## 🤖 Claude *(21:10:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "python3 - <<'PY'\nimport json\npath='/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/subagents/workflows/wf_75660c54-ef3/journal.jsonl'\nfor line in open(path):\n    try: rec=json.loads(line)\n    except: continue\n    if rec.get('type')=='result':\n        val=rec.get('result') or rec.get('value')\n        txt=json.dumps(val, ensure_ascii=False)\n        if 'SocialAppConfigCard' in txt:\n            print(txt[:12000])\n            break\nPY",
  "description": "Ler resultado completo da frente settings-card"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {"findings": "# SocialAppConfigCard — full anatomy\n\n## 1. UX pattern of the per-user app-credentials card\n\n**File:** `/home/gcrUX/htdocs/constellation-orchestra/src/components/settings/SocialAppConfigCard.tsx`\n\n- **Display-only component** (Harness pattern): all state/mutations live in `useSocialAppConfig` (`SocialAppConfigCard.tsx:18-23` doc comment; hook at `src/hooks/useSocialAppConfig.ts`).\n- **Structure:** one outer shadcn `Card` (`SocialAppConfigCard.tsx:148-178`) with:\n  - Header: `Share2` icon + title \"Apps Sociais — TikTok, YouTube & Pinterest\" (`:151-154`), description explaining Client ID + Client Secret BYOK (`:155-158`), and a **copyable shared Redirect URI block** (`code` + \"Copiar\" button → `navigator.clipboard.writeText(SOCIAL_OAUTH_REDIRECT_URI)`, `:139-146`, `:159-164`).\n  - Body: loading spinner while `isLoading` (`:167-170`), else **one `PlatformSection` per platform** mapped from `SOCIAL_APP_PLATFORMS` (`:171-175`). There is NO dropdown platform selector — the \"selector\" is the flat list of sections, one bordered sub-panel per platform (`:84`).\n- **PlatformSection fields** (`:41-134`):\n  - `client_id` text Input — label comes from per-platform meta (`meta.clientIdLabel`, TikTok = \"Client Key\"), `autoComplete=\"off\"`, `data-lpignore`/`data-1p-ignore`, monospace (`:100-108`). Pre-filled from the stored row via `useEffect(() => setClientId(row?.client_id ?? \"\"), [row?.client_id])` (`:52-55`).\n  - `client_secret` password Input — **write-only**: never pre-filled; placeholder shows the mask sentinel `•••••••••••• (salvo — cole para substituir)` when configured (`:111-124`); helper copy \"Nunca exibido de volta por segurança. Cole novamente para atualizar.\" (`:121-123`).\n  - \"Configurado\" badge (emerald pill with `CheckCircle2`) when `isConfigured(platform)` (`:90-94`).\n  - Per-platform helper line `meta.helper` (`:97`).\n  - Save button per section with spinner (`:126-131`).\n- **Validation before save** (`:57-66`): client_id required always; **secret required only on first save** — re-save may omit it to keep the stored one (`:62-66`). On success: toast + `setClientSecret(\"\")` (`:74-75`). Toasts in PT-BR.\n- **Masked-secret / encrypted-views write pattern** (hook `useSocialAppConfig.ts:14-19` doc + `:50-82`):\n  - `social_app_config` is a **Vault-masked security_invoker VIEW**; `client_secret` reads back as sentinel `'••••••••••••'` or null (`src/lib/social-app-config.ts:5-7`, migration `20260627120000_social_app_config.sql:101-113`).\n  - **NEVER `.upsert()`** (400 on INSTEAD OF views) — the hook does read-then-branch: `UPDATE ... .eq('id', existing.id)` if the row exists (`useSocialAppConfig.ts:66-71`), else `.insert({ user_id: user!.id, platform, ...writable })` (`:72-77`). Natural key = `(user_id, platform)` UNIQUE (migration `:41`).\n  - **Mask round-trip guard**: secret only included in the payload `if (secret && secret !== SOCIAL_SECRET_MASK)` (`useSocialAppConfig.ts:60-64`) — omitting it (rather than sending null/mask) preserves the stored Vault secret; the INSTEAD OF UPDATE also COALESCE/NULLIF-guards the mask server-side (migration `:150-151`).\n  - Writes always set `is_active: true` (`:56-59`).\n  - Query invalidation on success: `['social_app_config', user?.id]` (`:79-81`).\n  - Untyped client cast `supabase as unknown as SupabaseClient` because the view is not in generated types yet (`:24-26`).\n\n## 2. Client lib API\n\n**File:** `/home/gcrUX/htdocs/constellation-orchestra/src/lib/social-app-config.ts`\n\n- `SocialAppPlatform = 'tiktok' | 'youtube' | 'pinterest'` (`:10`) — note the DB enum `social_platform` holds 8 values (see #3).\n- `SOCIAL_APP_PLATFORMS: readonly SocialAppPlatform[]` (`:12`).\n- `SOCIAL_SECRET_MASK = '••••••••••••'` (`:15`).\n- `SOCIAL_OAUTH_REDIRECT_URI = 'https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback'` (`:17-19`).\n- **SAFE columns select string**: `SOCIAL_APP_SAFE_COLUMNS = 'id,user_id,platform,client_id,client_secret,is_active,metadata'` (`:22`) — used in the hook's `.select()` (`useSocialAppConfig.ts:33`). (client_secret here is the masked view column; the base-table column has `REVOKE SELECT` from anon/authenticated, migration `:59`.)\n- Types: `SocialAppConfigRow` (`:25-34` — id, user_id, platform, client_id|null, masked client_secret|null, is_active, metadata) and `SocialAppConfigInput` (`:37-42` — platform, client_id, optional plaintext client_secret; empty = leave stored secret untouched).\n- `SocialAppPlatformMeta` + `SOCIAL_APP_PLATFORM_META` record (`:45-82`): per-platform `name`, `clientIdLabel` (TikTok = \"Client Key\"), PT-BR `helper`, and `console` (developer-console path).\n- Predicates: `hasStoredSecret(row)` = `client_secret === SOCIAL_SECRET_MASK` (`:85-87`); `isSocialAppConfigured(row)` = client_id present AND mask present AND `is_active !== false` (`:93-95`).\n- **Hook (mutations):** `/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useSocialAppConfig.ts` returns `{ rows, byPlatform, isLoading, saveConfig (useMutation), isConfigured }` (`:88-94`). `byPlatform` is a `Partial<Record<SocialAppPlatform, SocialAppConfigRow>>` reduce for O(1) lookup (`:41-48`). Query is `.from('social_app_config').select(SAFE).eq('user_id', user!.id)`, `enabled: !!user?.id` (`:28-39`).\n\n## 3. Platforms supported today\n\n- Card/lib: **tiktok, youtube, pinterest** only (`src/lib/social-app-config.ts:10-12`).\n- The DB enum `public.social_platform` holds 8: `'linkedin','instagram','facebook','twitter','tiktok','youtube','pinterest','wordpress'` (migration `20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql:12`); lib comment `:9` acknowledges \"The enum holds more, but only these need BYOK app creds\". Meta (FB/IG) has its own sibling card `MetaConfigCard` mounted right above (`SettingsPage.tsx:557`).\n\n## 4. Sibling ADMIN card (global rows) — reuse vs must-differ\n\n**Reusable verbatim:**\n- The whole `PlatformSection` field anatomy: client_id pre-fill effect, write-only password secret input with mask placeholder + `SOCIAL_SECRET_MASK` sentinel, first-save-requires-secret validation, per-section Save with spinner, \"Configurado\" badge (`SocialAppConfigCard.tsx:41-134`).\n- Lib constants/types: `SOCIAL_SECRET_MASK`, `SOCIAL_OAUTH_REDIRECT_URI`, `SOCIAL_APP_PLATFORM_META`, `SocialAppConfigInput`, `hasStoredSecret`, and the `PLATFORM_ICON`/`PLATFORM_ICON_COLOR` maps (brand icons from `src/components/icons/brand-icons`).\n- The mutation shape: read-then-branch UPDATE-by-id / INSERT (never `.upsert()`), mask round-trip guard `secret !== SOCIAL_SECRET_MASK`, omit-to-preserve semantics (`useSocialAppConfig.ts:50-82`).\n- Redirect-URI copy block (`SocialAppConfigCard.tsx:139-164`).\n\n**Must differ:**\n- **user_id NULL for global rows:** the current schema FORBIDS it — `social_app_config_table.user_id UUID NOT NULL REFERENCES auth.users(id)` (migration `:32`) and `UNIQUE(user_id, platform)` (`:41`, which also does not dedupe NULLs under default UNIQUE semantics). A global-row admin card needs a migration: nullable user_id (or a partial unique index `WHERE user_id IS NULL`), plus RLS/policy changes — current policy is `auth.uid() = user_id` FOR ALL (`:47-48`), which never matches NULL, and the INSTEAD OF tenant guard raises 42501 whenever `NEW.user_id IS DISTINCT FROM auth.uid()` for non-service_role (`:132-134`, `:143-145`) — so an admin (authenticated, not service_role) cannot insert a NULL-user row through the view today. Either add `has_role('admin')` exemption in the guard + an admin RLS policy, or route admin writes through a service-role edge function.\n- **Query scoping:** hook filters `.eq('user_id', user!.id)` (`useSocialAppConfig.ts:34`) → admin variant needs `.is('user_id', null)` (and the queryKey must not be user-scoped).\n- **Insert payload:** `{ user_id: user!.id, ... }` (`:75`) → `user_id: null`.\n- **Admin gating in the UI:** mount gated by `has_role()` (pattern: `has_role(app_role)` single-arg SECURITY DEFINER, per repo memory) — SettingsPage today has no admin gating around these cards.\n- **Listing all platforms:** replace `SOCIAL_APP_PLATFORMS` (3) with the full enum list (8 values, or the subset admin wants to seed) — needs new meta entries in `SOCIAL_APP_PLATFORM_META` for linkedin/instagram/facebook/twitter/wordpress (icons, labels, helper copy).\n- **Untyped-view cast** (`useSocialAppConfig.ts:26`) is reusable as-is since the view isn't in generated types.\n\n## 5. Existing tests\n\n**None for this card, lib, or hook.** Grep for `SocialAppConfig|social-app-config|social_app_config|useSocialAppConfig` across `src/test/` and all `*.test.ts(x)`/`*.spec.ts` in the repo returns zero hits. Nearest analog with tests is the Meta sibling: `/home/gcrUX/htdocs/constellation-orchestra/src/test/meta.test.ts` (tests `src/lib/meta.ts` connection-state helpers), which is the template an admin-card test would mirror.\n\n## Mounting\n\n**File:** `/home/gcrUX/htdocs/constellation-orchestra/src/pages/SettingsPage.tsx`\n- Imported at `:7`.\n- Mounted inside `<TabsContent value=\"meta\">` (the tab labeled \"Social\", trigger at `:237`) right after `<MetaConfigCard />`: `SettingsPage.tsx:555-560`. Tabs root `defaultValue=\"ai\"` at `:233-240` with 5 tabs: ai / wordpress / meta (\"Social\") / connectors / lgpd.", "key_facts": ["SOCIAL_APP_SAFE_COLUMNS = 'id,user_id,platform,client_id,client_secret,is_active,metadata' (src/lib/social-app-config.ts:22)", "SOCIAL_SECRET_MASK = '••••••••••••' (src/lib/social-app-config.ts:15); hook guards `if (secret && secret !== SOCIAL_SECRET_MASK)` before including it in payload (src/hooks/useSocialAppConfig.ts:62)", "Write pattern: NEVER .upsert() — read-then-branch: .update(writable).eq('id', existing.id) if row exists, else .insert({ user_id: user!.id, platform, ...writable }) (src/hooks/useSocialAppConfig.ts:66-77)", "type SocialAppPlatform = 'tiktok' | 'youtube' | 'pinterest' (src/lib/social-app-config.ts:10); DB enum social_platform has 8 values: linkedin, instagram, facebook, twitter, tiktok, youtube, pinterest, wordpress (migration 20260402014040:12)", "SOCIAL_OAUTH_REDIRECT_URI = 'https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback' (src/lib/social-app-config.ts:18-19)", "isSocialAppConfigured = client_id present AND client_secret === mask AND is_active !== false (src/lib/social-app-config.ts:93-95)", "social_app_config_table.user_id is NOT NULL REFERENCES auth.users(id) + UNIQUE(user_id, platform) (migration 20260627120000:32,41) — global NULL-user rows need a schema change", "INSTEAD OF trigger tenant guard: RAISE 42501 when auth.role() != 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() (migration 20260627120000:132-134,143-145) — blocks admin NULL-user writes via view", "Hook returns { rows, byPlatform, isLoading, saveConfig, isConfigured }; query .eq('user_id', user!.id), queryKey ['social_app_config', user?.id] (src/hooks/useSocialAppConfig.ts:28-39,88-94)", "Card mounted in SettingsPage <TabsContent value=\"meta\"> (tab label 'Social') after MetaConfigCard (src/pages/SettingsPage.tsx:7,555-560; TabsList :233-240)", "No tests exist for SocialAppConfigCard / social-app-config lib / useSocialAppConfig; nearest analog is src/test/meta.test.ts", "Hook uses untyped cast `supabase as unknown as SupabaseClient` because social_app_config view is not in generated Database types (src/hooks/useSocialAppConfig.ts:24-26)"], "gaps_or_risks": ["An admin/global variant cannot ship UI-only: migration required (nullable user_id or partial unique index WHERE user_id IS NULL, admin RLS policy, INSTEAD OF guard exemption or service-role edge-function write path) — and per CLAUDE.md every new migration must pass /security-review (FMEA-011)", "UNIQUE(user_id, platform) does not enforce uniqueness across NULL user_id rows under default PostgreSQL UNIQUE semantics — a global-rows design needs a partial unique index", "SOCIAL_APP_PLATFORM_META only covers 3 platforms; listing all 8 enum platforms requi
> ```

## 🤖 Claude *(21:11:53)*


## 🤖 Claude *(21:11:53)*

A frente `settings-card` retornou a anatomia completa do molde per-user (write pattern UPDATE-first, mask sentinel, guard 42501 no INSTEAD OF que hoje **bloqueia** linha global — confirma que a fatia exige migration). As 3 frentes que caíram em 529 estão re-rodando via resume com cache das 2 prontas.

**Design consolidando (com o que as 2 frentes já provaram):**
- **Camada global = linhas `user_id IS NULL` na própria `social_app_config`** (precedente do projeto: system nodes da malha) — migration: `DROP NOT NULL` + unique parcial por plataforma + policy admin (`has_role`) + exemption no guard do INSTEAD OF trigger. Vault/masked view reusados sem mudança.
- **Resolver vira 4 degraus**: per-user → **global row (admin)** → env → 402. E o mapa exaustivo do `env-sweep` provou que **LinkedIn/Instagram/Twitter ainda leem `Deno.env` cru em 3 estágios** (init/callback/`refresh-social-token`) — migram para o resolver nesta fatia, cobrindo o pedido "todas as chaves globais".
- **Lembrete de rotação**: tabela leve `admin_reminders` (RLS admin-only, seed com SA Vertex · Gemini · Telegram, botão "marcar como rotacionada") — persistente e reusável pelo guardian MAPE-K.

Aguardando as frentes `admin-page`/`social-page`/`bok-sop` para selar a amendment BoK com o numbering correto.

## 👤 User *(21:19:38)*

<task-notification>
<task-id>wlnkrlfc4</task-id>
<tool-use-id>toolu_01CA3S3vRX9khryxstaxsZqc</tool-use-id>
<output-file>/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/tasks/wlnkrlfc4.output</output-file>
<status>completed</status>
<summary>Dynamic workflow "Mapear AdminPage, SocialAccountsPage, env-usage de app creds, molde SocialAppConfigCard e BoK/SOP para a fatia Pinterest + Admin Global Keys" completed</summary>
<result>{"fronts":[{"key":"admin-page","findings":"# Admin page (/dashboard/admin) — structure, gating, hooks, and slot-in points\n\n## 1. Component structure\n\n**Route:** `/home/gcrUX/htdocs/constellation-orchestra/src/App.tsx:37` (lazy import `AdminPage`) + `src/App.tsx:135` (`&lt;Route path=\"admin\" element={&lt;AdminPage /&gt;} /&gt;`, inside the `/dashboard` subtree wrapped by `DashboardLayout`).\n\n**Page:** `/home/gcrUX/htdocs/constellation-orchestra/src/pages/AdminPage.tsx` (187 lines). Layout is `&lt;div className=\"space-y-6\"&gt;` with:\n\n- **Header** — `Shield` icon + `&lt;h1&gt;Administração&lt;/h1&gt;` (AdminPage.tsx:33-36)\n- **SovereignBalancePanel** (top-level card, above the tabs) — admin's own mcoCoins top-up, yellow/gold themed Card (AdminPage.tsx:38-43; component at `src/components/admin/SovereignBalancePanel.tsx`, invokes `admin-manage-user` via `useAdminUserActions`)\n- **Tabs** (`defaultValue=\"users\"`, AdminPage.tsx:45-184) with 4 triggers, each icon+label pt-BR:\n  - `users` → \"Usuários\" — Card \"Usuários (N)\" with Table (Nome/Empresa/Funções/Plano/Saldo/Status/Criado em/Ações) + `UserActionsMenu` per row (AdminPage.tsx:53-109; menu at `src/components/admin/UserActionsMenu.tsx`)\n  - `pantheon` → \"Pantheon\" — `PantheonAdminPanel` (AdminPage.tsx:181-183; component at `src/components/admin/PantheonAdminPanel.tsx` — CRUD on `pantheon_global_configs`)\n  - `audit` → \"Auditoria\" — Card \"Logs de Auditoria (N)\" table (AdminPage.tsx:111-144)\n  - `usage` → \"Uso\" — Card \"Rastreamento de Uso (N)\" table (AdminPage.tsx:146-179)\n- Loading pattern: `Skeleton` while loading (AdminPage.tsx:25, 57); empty state row \"Nenhum log encontrado\" / \"Nenhum uso registrado\" (AdminPage.tsx:136, 171).\n\n## 2. Admin gating\n\n**Client-side (convenience only):** `useIsAdmin()` in `/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useAdminData.ts:7-31` — TanStack Query on `user_roles` filtering `user_id = user.id AND role = 'admin'` (`.maybeSingle()`), `staleTime: Infinity`. AdminPage redirects: `if (!isAdmin) return &lt;Navigate to=\"/dashboard\" replace /&gt;` (AdminPage.tsx:26), with a loading guard so the redirect doesn't fire before auth resolves (useAdminData.ts:26-30).\n\n**has_role EXACT signature (deployed canonical): SINGLE-ARG** `public.has_role(_role public.app_role)` reading `auth.uid()` internally.\n- Original two-arg `has_role(_user_id UUID, _role app_role)` was created in `supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql:237-249` but **DROPPED** by `supabase/migrations/20260414154016_a94ffdfc-62ba-4d55-94dd-48c1d316d19b.sql:12` (`DROP FUNCTION IF EXISTS public.has_role(uuid, public.app_role);`) and replaced with the single-arg version at lines 14-27 of that same file.\n- Confirmed by comment in `supabase/migrations/20260601031300_constellation_v2_foundation.sql:90-91`: \"remote has has_role(app_role), not has_role(uuid, app_role)\". This matches the memory note \"has_role(app_role) single-arg\" gotcha.\n\n**Edge-fn admin check (authority boundary):** `supabase/functions/admin-manage-user/index.ts:40-46` — after `userClient.auth.getUser()`, it calls `userClient.rpc(\"has_role\", { _role: \"admin\" })` (user-JWT client, so auth.uid() = caller) and returns 403 `\"Forbidden — admin role required\"` if not admin. Self-modification guard at :57 (admin can't change own role/status/delete self). Writes to `audit_logs` (:158-165) and to `infra_health_logs` on error (:171-172).\n\n**RLS admin policies (single-arg):**\n- `20260414154016_...sql:32-60` — admin SELECT on `audit_logs`, `profiles`, `subscriptions`, `usage_tracking`, `user_roles`, all `USING (public.has_role('admin'))`.\n- `20260606210000_pantheon_admin_crud.sql:23-24` — `USING (public.has_role('admin')) WITH CHECK (public.has_role('admin'))`.\n- `20260701040000_infra_health_logs_admin_only_read.sql:19` and `20260701000000_security_events_ledger.sql:35` — `USING (public.has_role('admin'::public.app_role))` (explicit enum cast form).\n- `20260701010000_fr_sec_014_pt2_economic_freeze.sql:148` — in-function guard `IF auth.role() IS DISTINCT FROM 'service_role' AND NOT public.has_role('admin'::public.app_role) THEN`.\n\n## 3. Exact SQL of has_role (deployed, single-arg)\n\n`supabase/migrations/20260414154016_a94ffdfc-62ba-4d55-94dd-48c1d316d19b.sql:14-30`:\n\n```sql\nCREATE OR REPLACE FUNCTION public.has_role(_role public.app_role)\nRETURNS boolean\nLANGUAGE sql\nSTABLE\nSECURITY DEFINER\nSET search_path = public\nAS $$\n  SELECT EXISTS (\n    SELECT 1\n    FROM public.user_roles\n    WHERE user_id = auth.uid()\n      AND role = _role\n  );\n$$;\n\nREVOKE ALL ON FUNCTION public.has_role(public.app_role) FROM PUBLIC;\nGRANT EXECUTE ON FUNCTION public.has_role(public.app_role) TO authenticated;\n```\n\n## 4. Hooks pattern for admin data\n\n- `useAdminData(enabled)` (`src/hooks/useAdminData.ts:49-86`): single TanStack Query keyed `['admin-data', user?.id]` that `Promise.all`s 5 direct-table selects (`profiles`, `user_roles`, `subscriptions` safe-column subset omitting stripe ids, `audit_logs`, `usage_tracking`), `staleTime: 60_000`, `enabled: Boolean(user) &amp;&amp; enabled` (page passes `isAdmin` as `enabled`). RLS admin policies make the reads work.\n- Mutations go through the edge fn, never direct writes: `useAdminUserActions()` (`src/hooks/useAdminUserActions.ts:16-40`) — typed union `AdminUserAction` (:4-9), `supabase.functions.invoke('admin-manage-user', ...)`, structured pt-BR error extraction from the non-2xx body (:22-32), `invalidateQueries({ queryKey: ['admin-data'] })` on success (:36-38).\n- PantheonAdminPanel deviates slightly: inline `useQuery`/`useMutation` inside the component (`src/components/admin/PantheonAdminPanel.tsx:48-59`) with direct table CRUD gated by RLS — acceptable precedent, but the harness convention (business logic in `src/hooks/`) favors the useAdminData/useAdminUserActions pattern.\n\n## 5. Where \"Chaves de Aplicativo (Globais)\" card + \"rotação pendente\" banner slot in\n\n**Layout conventions on this page:**\n- Top-level always-visible cards go between the header and the Tabs — precedent: `SovereignBalancePanel` (AdminPage.tsx:38-43). A \"rotação pendente\" reminder banner belongs here (above or below SovereignBalancePanel), so it's seen regardless of active tab. `src/components/ui/alert.tsx` (shadcn Alert) exists and is currently unused by pages — natural component for the banner; alternatively a bordered Card like SovereignBalancePanel (`border-yellow-500/20 bg-card/50 backdrop-blur-sm` for warning tone).\n- Substantive admin panels go as a **new TabsTrigger + TabsContent** — precedent: Pantheon (AdminPage.tsx:48, 181-183) whose panel is a self-contained component in `src/components/admin/`. A \"Chaves de Aplicativo (Globais)\" card would follow: new component `src/components/admin/GlobalAppKeysPanel.tsx` (or similar) + a tab e.g. `&lt;TabsTrigger value=\"keys\"&gt;&lt;KeyRound .../&gt;Chaves&lt;/TabsTrigger&gt;`. If it's small enough, it could instead be a top-level Card next to SovereignBalancePanel.\n- **pt-BR copy style:** short title-case nouns for tabs (\"Usuários\", \"Auditoria\", \"Uso\"); Card titles with counts (\"Usuários (N)\"); CardDescription full sentences (\"Ajuste o saldo de mcoCoins da sua conta. Restrito a administradores.\"); empty states \"Nenhum X encontrado/registrado\"; toasts via `sonner` in pt-BR (\"+500 mcoCoins adicionados.\", \"Insira um valor válido...\"); dates via `date-fns` `format(parseISO(d), \"dd/MM/yy HH:mm\", { locale: ptBR })` (AdminPage.tsx:16-18); numbers `.toLocaleString('pt-BR')`.\n- Mutation path convention: any write (e.g., rotate/save a global key) should go through an admin edge fn (mirror `admin-manage-user`'s has_role gate) or an RLS-admin-gated table, invoked from a hook in `src/hooks/` — never direct client secrets handling (see also the encrypted-views write pattern: `.insert()` not `.upsert()` on masked views).\n\n## 6. Notifications/reminders mechanism (reu
... (truncated 44482 chars, full result in /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/tasks/wlnkrlfc4.output)</result>
<diagnostics>Per-agent results: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/subagents/workflows/wf_75660c54-ef3/journal.jsonl — one {"type":"result",...} line per completed agent with its full return value.
If the result above is empty or unexpected, Read this file BEFORE diagnosing — do not assume agents returned non-empty results.
To re-run with edited post-processing: Workflow({scriptPath: '/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/workflows/scripts/recon-pinterest-admin-keys-wf_75660c54-ef3.js', resumeFromRunId: 'wf_75660c54-ef3'}) — agents whose (prompt, opts) are unchanged replay from cache.</diagnostics>
<failures>[recon:social-page] failed: API Error: 529 Overloaded. This is a server-side issue, usually temporary — try again in a moment. If it persists, check https://status.claude.com.</failures>
<usage><agent_count>5</agent_count><agents_done>4</agents_done><agents_error>1</agents_error><agents_skipped>0</agents_skipped><agents_empty_result>0</agents_empty_result><subagent_tokens>411205</subagent_tokens><tool_uses>61</tool_uses><duration_ms>555457</duration_ms></usage>
</task-notification>

## 🤖 Claude *(21:19:49)*


## 🤖 Claude *(21:19:50)*

4/5 frentes completas (social-page caiu de novo em 529 — assumo inline, é leitura pequena). Extraindo o `bok-sop` do output e cobrindo a frente falha:

## 🤖 Claude *(21:19:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "python3 - <<'PY'\nimport json\ndata=json.load(open('/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/tasks/wlnkrlfc4.output'))\n# tolerate wrapper shapes\nfronts = data.get('fronts') if isinstance(data, dict) else None\nif fronts is None:\n    # maybe the file is the result object directly\n    for k in ('result','value'):\n        if isinstance(data, dict) and k in data: fronts = data[k].get('fronts')\nfor f in fronts or []:\n    if f.get('key')=='bok-sop':\n        print(\"=== BOK-SOP KEY FACTS ===\")\n        for kf in f.get('key_facts', []): print(\"-\", kf)\n        print(\"\\n=== FINDINGS (first 6000) ===\")\n        print((f.get('findings') or '')[:6000])\n    if f.get('key')=='admin-page':\n        print(\"\\n=== ADMIN-PAGE reminders section (tail) ===\")\n        fnd=f.get('findings') or ''\n        i=fnd.find('## 6.')\n        print(fnd[i:i+2500] if i>=0 else '(sem se\u00e7\u00e3o 6)')\nPY",
  "description": "Extrair frentes bok-sop e cauda do admin-page do output do workflow"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === ADMIN-PAGE reminders section (tail) ===
> ## 6. Notifications/reminders mechanism (reusable)
> 
> Yes — a full in-app notifications system exists:
> - **Table:** `public.notifications` — `supabase/migrations/20260402014040_...sql:221-232` (`user_id`, `type notification_type` [info|success|warning|error], `title`, `message`, `read`, `action_url`, `metadata jsonb`, `created_at`). RLS: SELECT/UPDATE own (:315-317); client INSERT **blocked** by `20260413222422_96278b36-...sql:1-5` ("No client insert on notifications" — service-role/edge-fn writes only); DELETE own added in `20260414152224_...sql:1-2`.
> - **Server-side writer:** `supabase/functions/_shared/notify.ts` — `notify(admin, userId, { type, title, message, action_url, metadata })`, best-effort (never throws), service-role insert. Edge fns already use this; a rotation-reminder cron/edge fn could call it to notify admins.
> - **Client hook:** `src/hooks/useNotifications.ts:18-63` — reads own last 30, `unreadCount`, `markRead`/`markAllRead` mutations, key `["notifications", user?.id]`.
> - **UI:** `src/components/dashboard/NotificationBell.tsx`, mounted in `src/components/dashboard/DashboardLayout.tsx:152` — so a notification with an `action_url` pointing at `/dashboard/admin` would light the bell globally.
> - There is NO dedicated "reminder/banner" table or scheduled-reminder framework beyond this; a "rotação pendente" banner on the admin page would be derived client-side (e.g., computed from key `updated_at`/`rotated_at` age in the new keys hook) and optionally reinforced via `notify()` from a cron edge fn.
> === BOK-SOP KEY FACTS ===
> - social_platform enum (migration 20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql:12): ENUM ('linkedin', 'instagram', 'facebook', 'twitter', 'tiktok', 'youtube', 'pinterest', 'wordpress') — includes 'pinterest'; zero ALTER TYPE ADD VALUE in any migration
> - FR-PE-005 = per-user app credentials table social_app_config UNIQUE(user_id, platform), client_secret Vault + column-REVOKE + INSTEAD OF tenant-guard; FR-PE-006/007/008 = OAuth init TikTok/YouTube/Pinterest; FR-PE-009 = OAuth callback for the 3 platforms (amendment 10 continues to FR-PE-016)
> - OTD-PE-SOCIAL-APPCREDS (amendment 10 §4, line 138): env-credential deferral, RPN moderado, SLA 'antes do 2º tenant' — env fallback (TIKTOK_CLIENT_KEY/SECRET, GOOGLE_CLIENT_ID/SECRET, PINTEREST_CLIENT_ID/SECRET) is Sovereign-only onboarding default, reached only when no active per-user row; must promote env→per-user before 2nd tenant
> - OTD-SOCIAL-APP-ENV-FALLBACK (pinterest-publish-credential-resolution.md Known debt): same deferral restated, closure criterion = 100% resolutions via social_app_config per-user + Settings UI before 2nd tenant; sibling OTD-META-ENCRYPT (at-rest encryption)
> - Pinterest scopes (plan FULL set upfront, later additions force total re-auth): boards:read,boards:write,pins:read,pins:write,user_accounts:read; no PKCE; token exchange uses Authorization: Basic base64(client_id:client_secret) at POST https://api.pinterest.com/v5/oauth/token
> - Redirect URI for all 3 platforms: https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback (static, pre-registered, ≤512 chars; Pinterest = EXACT match, no wildcard)
> - Next post-engine amendment number = 16 (directory has 00–15; 15-amendment-smart-delete.md exists on disk but is missing from the 00-index.md Suite Documents table, which is stale at 14 / 2026-06-28)
> - No dedicated admin/global-credentials SOP exists in docs/processes/; only precedent for a legitimate global app-credential is docs/processes/tiktok-login-oauth.md:19 — login (no auth.uid() pre-session) reuses the single active social_app_config tiktok row via _shared/tiktok-login-creds.ts + decrypted_social_app_config, env = optional override
> - Shared resolver: supabase/functions/_shared/social-app-config.ts (per-user via decrypted_social_app_config view → env → SocialAppConfigError 402 '<platform>_not_configured'); migration supabase/migrations/20260627120000_social_app_config.sql
> - Pinterest publish SOP exists and is ACTIVE v1.0 (docs/processes/pinterest-publish-credential-resolution.md): 12-step sequence, gates G1–G10, Trial=sandbox (never claim 'ao vivo' pre-Standard), refresh token continuously ROTATING — persist access+refresh atomically (advisory-lock)
> 
> === FINDINGS (first 6000) ===
> # Findings — Post-Engine Social Connect BoK + Pinterest credential landscape
> 
> ## 1. Amendment 10 — `docs/bok/post-engine/10-amendment-social-connect-tiktok-youtube-pinterest.md` (v1.0, 2026-06-27, authoritative branch design)
> 
> ### FR-PE-005..009 (per-user app creds + OAuth) — §5, lines 146-153
> - **FR-PE-005** (Critical, DB/Edge): App credentials per-user via single table `social_app_config` keyed `UNIQUE(user_id, platform)`, `client_secret` Vault-encrypted + column-level REVOKE + INSTEAD OF tenant-guard; resolution order per-user → env → hard-fail (§4).
> - **FR-PE-006** (Critical): OAuth init TikTok — branch at `social-auth-init:95`, scope `video.publish,user.info.basic` COMMA-separated, signed `state`.
> - **FR-PE-007** (Critical): OAuth init YouTube — `accounts.google.com/o/oauth2/v2/auth`, scope `youtube.upload`, `access_type=offline`+`prompt=consent`.
> - **FR-PE-008** (Critical): OAuth init Pinterest — `pinterest.com/oauth/`, FULL scope set `boards:read,boards:write,pins:read,pins:write,user_accounts:read`, redirect **exact-match**.
> - **FR-PE-009** (Critical): OAuth callback for all 3 platforms — `social-auth-callback:171` code→token exchange + upsert into `social_accounts` (Pinterest uses `Authorization: Basic base64(client_id:client_secret)` + identity via `GET /v5/user_account`).
> - (Amendment continues through FR-PE-016; FRD v0.1 used FR-PE-001..004, amendment states "próximo id livre confirmado" = FR-PE-005.)
> 
> ### §Pinterest (§2.3, lines 89-112)
> - API v5, NET-NEW. Video pin = 4 async steps + step 0 board cache: (0) `GET/POST /v5/boards` ONCE, cache `board_id` in `social_app_config.metadata.board_id`; (1) register `POST /v5/media {media_type:'video'}`; (2) multipart upload to presigned `upload_url` — params VERBATIM, `file` field LAST, no Bearer, success=204; (3) poll `GET /v5/media/{id}` until `succeeded`; (4) `POST /v5/pins` with mandatory PUBLIC `cover_image_url` (pulled async by Pinterest — long-TTL) → 201 pin id.
> - Tokens: access 30d (2592000s); refresh **continuously ROTATING**, 60d-from-last-use — persist both ATOMICALLY (advisory-lock) or the chain breaks.
> - No PKCE (v5 confidential-client Authorization-Code).
> - Materiality gate: under **Trial** pins are sandbox/creator-only — never claim "publicado ao vivo" until **Standard** tier. Rate: `org_write` 300/day Trial · 100/min Standard.
> - Correct paths: `/v5/pins`, `/v5/boards`, `/v5/media` (the `*/create` slugs 404).
> 
> ### Redirect URI guidance (§1 constants table, line 33)
> Single static callback for all 3 platforms: `https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback` — https, static, pre-registered, ≤512 chars; Pinterest requires **EXACT match** to a Configure>Redirect URIs entry (no wildcard).
> 
> ### Scopes plan
> - Pinterest: plan the COMPLETE scope set upfront — adding a scope later forces full re-authorization (existing refresh token does NOT gain it) (line 93).
> - TikTok: `video.publish,user.info.basic` (comma-separated; space silently fails consent; NEVER `video.upload`).
> - YouTube: `https://www.googleapis.com/auth/youtube.upload` + `access_type=offline` + `prompt=consent` (else refresh_token silently null on re-auth).
> 
> ### GLOBAL/admin credential tier — OTD-PE-SOCIAL-APPCREDS (§4, line 138)
> **No dedicated admin/global tier exists — the env fallback IS the global tier, and it is explicitly a DEFERRAL, not a design.** Definition (verbatim location: line 138):
> - **OTD-PE-SOCIAL-APPCREDS** — "deferimento de credencial env · RPN moderado · **SLA: antes do 2º tenant**". The 3 probe slices run with env creds (`TIKTOK_CLIENT_KEY/SECRET`, `GOOGLE_CLIENT_ID/SECRET`, `PINTEREST_CLIENT_ID/SECRET`) because User Zero is the only tenant. Per-user `social_app_config.is_active=true` is the primary path; env is only reached when no active per-user row exists. Mandate: "**Promover env→per-user (UI Settings + `is_active`) antes de onboardar o 2º tenant** — senão vira dívida silenciosa de credencial compartilhada." User tokens go per-user to `social_accounts` in any case.
> - Resolution order §4 (UNBREAKABLE, mirrors CLAUDE.md API Tenancy Model): (1) `social_app_config` per-user → (2) env fallback ("default Sovereign-only de onboarding") → (3) hard fail 402/501 `{error:"<platform>_not_configured"}` — "NUNCA shared key silenciosa."
> - Implemented in `supabase/functions/_shared/social-app-config.ts` (lines 1-13 restate the order and OTD id) + migration `supabase/migrations/20260627120000_social_app_config.sql` (line 9 cites OTD-PE-SOCIAL-APPCREDS).
> 
> ## 2. Pinterest SOP — `docs/processes/pinterest-publish-credential-resolution.md` (EXISTS · ACTIVE v1.0 · 2026-06-27)
> - **Operator:** Sovereign registers app in Pinterest Developer Portal (Business account + Developer Terms + privacy-policy URL → Trial → Trial→Standard upgrade); User Zero/client configures app creds at `/dashboard/settings` (hook `useSocialAppConfig` → `social_app_config` WHERE platform='pinterest'); edge fn `publish-social` resolves at runtime.
> - **Sequence:** 12 steps — auth/userId → resolve app creds (per-user→env→402) → resolve user token + reauth gate (refresh rotativo atômico) → board cache → register → multipart upload (204) → poll succeeded → create pin (201) → persist `social_posts` → mesh observation node → `infra_health_logs service='publish-pinterest'` → return.
> - **Gates G1-G10:** G1 happy-path 201+row; G2 no-config→402 `pinterest_not_configured`; G3 not-connected→402; G4 expired-token→refresh-or-402 `pinterest_requires_reauth`; G5 multipart verbatim/file-last→204; G6 RLS isolation; G7 column-grant (`client_secret` permission-denied); G8 telemetry pulses; G9 env never primary (grep); G10 Materiality — public URL `pinterest.com/pin/<id>` only POST-Standard.
> - **Known debt:** **OTD-SOCIAL-APP-ENV-FALLBACK** (env-override Sovereign-only — SLA: 2º tenant; closure = 100% resolutions via per-user `social_app_config` + Settings UI before 2nd tenant) and **OTD-META-ENCRYPT** (at-rest encryption of all credential tables).
> 
> ## 3. `social_platform` enum — EXACT va
> ```

## 🤖 Claude *(21:21:19)*


## 🤖 Claude *(21:21:19)*


## 🤖 Claude *(21:21:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n -i \"pinterest\\|platforms\\|PLATFORM\" src/pages/SocialAccountsPage.tsx | head -30; echo \"---BRAND-ICONS---\"; grep -n \"export\" src/components/icons/brand-icons.tsx | head -20; echo \"---CONNECT-FLOW---\"; grep -n -A5 \"social-auth-init\" src/pages/SocialAccountsPage.tsx src/hooks/useSocialAccounts.ts 2>/dev/null | head -25",
  "description": "Ler SocialAccountsPage e brand-icons \u2014 card Pinterest existe?"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 2:import { useSocialAccounts, SUPPORTED_PLATFORMS } from '@/hooks/useSocialAccounts';
> 12:import { Instagram, Facebook, TikTok, YouTube, Pinterest } from '@/components/icons/brand-icons';
> 15:type SocialPlatform = Database['public']['Enums']['social_platform'];
> 17:// Brand glyphs for platforms that have a real logo (lucide-react dropped brand icons). Every
> 18:// supported platform has an entry below, so the emoji-free Globe fallback is only a defensive
> 19:// neutral for any future platform added without a glyph (MIV: never an emoji).
> 20:const PLATFORM_BRAND_ICON: Partial<Record<SocialPlatform, React.ComponentType<{ className?: string }>>> = {
> 25:  pinterest: Pinterest,
> 30:function PlatformGlyph({ platform }: { platform: SocialPlatform; emoji?: string }) {
> 31:  const Icon = PLATFORM_BRAND_ICON[platform] ?? Globe;
> 39:  const [connectingPlatform, setConnectingPlatform] = useState<SocialPlatform | null>(null);
> 109:  const handleConnect = async (platform: SocialPlatform) => {
> 110:    setConnectingPlatform(platform);
> 112:      await initiateOAuth(platform);
> 116:      setConnectingPlatform(null);
> 129:  const connectedPlatforms = new Set(accounts.map((a) => a.platform));
> 149:              const platformInfo = SUPPORTED_PLATFORMS.find((p) => p.id === account.platform);
> 157:                    <PlatformGlyph platform={account.platform} emoji={platformInfo?.icon} />
> 160:                        {platformInfo?.name}
> 161:                        {account.platform_username && (
> 162:                          <span className="text-muted-foreground ml-1">@{account.platform_username}</span>
> 183:                        onClick={() => handleConnect(account.platform)}
> 184:                        disabled={connectingPlatform === account.platform}
> 193:                      onClick={() => handleDisconnect(account.id, platformInfo?.name ?? account.platform)}
> 205:      {/* Available platforms */}
> 213:            {SUPPORTED_PLATFORMS.map((platform) => {
> 214:              const isConnected = connectedPlatforms.has(platform.id);
> 215:              const isConnecting = connectingPlatform === platform.id;
> 218:                  key={platform.id}
> 222:                    <PlatformGlyph platform={platform.id} emoji={platform.icon} />
> ---BRAND-ICONS---
> 9:export interface BrandIconProps extends Omit<SVGProps<SVGSVGElement>, 'ref'> {
> 37:export const Instagram = makeBrandIcon(
> 42:export const Facebook = makeBrandIcon(
> 47:export const TikTok = makeBrandIcon(
> 52:export const YouTube = makeBrandIcon(
> 57:export const Pinterest = makeBrandIcon(
> 62:export const Figma = makeBrandIcon(
> ---CONNECT-FLOW---
> src/hooks/useSocialAccounts.ts:55:    const { data, error } = await supabase.functions.invoke('social-auth-init', {
> src/hooks/useSocialAccounts.ts-56-      body: { platform, redirect_uri: `${window.location.origin}/social/callback` },
> src/hooks/useSocialAccounts.ts-57-    });
> src/hooks/useSocialAccounts.ts-58-
> src/hooks/useSocialAccounts.ts-59-    if (error) {
> src/hooks/useSocialAccounts.ts-60-      const msg: string = error?.message ?? '';
> ```

## 🤖 Claude *(21:21:30)*


## 🤖 Claude *(21:21:31)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n -B2 -A20 \"SUPPORTED_PLATFORMS\" src/hooks/useSocialAccounts.ts | head -40",
  "description": "Confirmar lista SUPPORTED_PLATFORMS do connect"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 14-// platform id → lucide line-icon); the `icon` field is vestigial (kept for the type) and MUST stay
> 15-// emoji-free — a Globe line-icon is the neutral fallback if a platform ever lacks a glyph.
> 16:export const SUPPORTED_PLATFORMS: { id: SocialPlatform; name: string; icon: string; color: string }[] = [
> 17-  { id: 'linkedin', name: 'LinkedIn', icon: '', color: 'bg-cyan-600' },
> 18-  { id: 'instagram', name: 'Instagram', icon: '', color: 'bg-gradient-to-r from-cyan-500 to-cyan-400' },
> 19-  { id: 'facebook', name: 'Facebook', icon: '', color: 'bg-cyan-500' },
> 20-  { id: 'twitter', name: 'Twitter / X', icon: '', color: 'bg-zinc-800' },
> 21-  { id: 'tiktok', name: 'TikTok', icon: '', color: 'bg-zinc-900' },
> 22-  { id: 'youtube', name: 'YouTube', icon: '', color: 'bg-red-600' },
> 23-  { id: 'pinterest', name: 'Pinterest', icon: '', color: 'bg-red-500' },
> 24-];
> 25-
> 26-export function useSocialAccounts() {
> 27-  const { user } = useAuth();
> 28-  const queryClient = useQueryClient();
> 29-
> 30-  const accountsQuery = useQuery({
> 31-    queryKey: ['social_accounts', user?.id],
> 32-    queryFn: async () => {
> 33-      const { data, error } = await supabase
> 34-        .from('social_accounts')
> 35-        .select('id, user_id, platform, platform_user_id, platform_username, is_active, token_expires_at, scopes, metadata, created_at, updated_at')
> 36-        .order('created_at', { ascending: false });
> ```

## 🤖 Claude *(21:22:04)*


## 🤖 Claude *(21:22:04)*


## 🤖 Claude *(21:22:05)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "2",
  "status": "completed"
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #2 status
> ```

## 🤖 Claude *(21:22:06)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "3",
  "status": "in_progress",
  "activeForm": "Escrevendo Amendment 16 + SOP Lei 2"
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #3 activeForm, status
> ```

## 🤖 Claude *(21:22:07)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rhoE \"FR-PE-[0-9]+\" docs/bok/post-engine/ | sort -V | uniq | tail -8; echo \"---AMENDMENTS---\"; ls docs/bok/post-engine/ | grep -E \"^1[0-9]\"",
  "description": "Confirmar pr\u00f3ximo FR-PE id livre + amendments existentes"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> FR-PE-009
> FR-PE-010
> FR-PE-011
> FR-PE-012
> FR-PE-013
> FR-PE-014
> FR-PE-015
> FR-PE-016
> ---AMENDMENTS---
> 10-amendment-social-connect-tiktok-youtube-pinterest.md
> 11-channel-format-intelligence-blueprint.md
> 12-amendment-channel-format-intelligence.md
> 13-sdd-reshaper-atomizer.md
> 14-social-engineering-virality-blueprint.md
> 15-amendment-smart-delete.md
> ```

## 🤖 Claude *(21:22:15)*


## 🤖 Claude *(21:22:15)*


## 🤖 Claude *(21:23:19)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/post-engine/16-amendment-global-app-credentials-admin-tier.md",
  "content": "# Amendment 16 \u2014 Global App Credentials (Admin Tier) + Lembretes de Rota\u00e7\u00e3o\n\n> **Suite:** post-engine \u00b7 **Vers\u00e3o:** v1.0 \u00b7 **Data:** 2026-07-16 \u00b7 **Status:** ATIVA\n> **Diretiva Sovereign (2026-07-16):** escopos Google APROVADOS na verifica\u00e7\u00e3o + app Pinterest APROVADO (App ID + App Secret em m\u00e3os). \"Preciso adicionar a chave em `/dashboard/admin` \u2014 assim n\u00e3o preciso `.env` nem rodar `npx supabase` pra adicionar o segredo no vault. Experi\u00eancia parecida com o BYOK per-user, mas somente ADMIN, para as chaves secretas de aplicativos e outras coisas globais. E deve ter uma notifica\u00e7\u00e3o na p\u00e1gina de admin para lembrar da rota\u00e7\u00e3o de credenciais pendente.\"\n> **Estende:** Amendment 10 (`10-amendment-social-connect-tiktok-youtube-pinterest.md`, FR-PE-005..009) \u00b7 **Fecha:** OTD-PE-SOCIAL-APPCREDS + OTD-SOCIAL-APP-ENV-FALLBACK (upgrade do deferral para design)\n> **SOP Lei 2:** `docs/processes/admin-global-app-credentials.md` (escrito ANTES do c\u00f3digo, junto desta amendment)\n\n---\n\n## \u00a70 Problema\n\nO onboarding-default global de credenciais de app OAuth hoje \u00e9 `Deno.env` (vault Supabase via CLI) \u2014 o deferral registrado em OTD-PE-SOCIAL-APPCREDS (\"SLA: antes do 2\u00ba tenant\"). Isso for\u00e7a o Sovereign a operar por CLI (`npx supabase secrets set`) para toda chave global, e tr\u00eas plataformas (LinkedIn \u00b7 Instagram/Meta \u00b7 Twitter/X) nem sequer passam pelo resolver \u2014 leem env cru em **tr\u00eas est\u00e1gios** (authorize, token exchange, refresh):\n\n| Plataforma | Fonte hoje | Call-sites raw-env |\n|---|---|---|\n| LinkedIn | `LINKEDIN_CLIENT_ID/SECRET` cru | `social-auth-init:69` \u00b7 `social-auth-callback:94-95` \u00b7 `refresh-social-token:92-93` |\n| Instagram/Facebook | `INSTAGRAM_APP_ID/SECRET` cru | `social-auth-init:80` \u00b7 `social-auth-callback:124-125,147` \u00b7 `refresh-social-token:102` |\n| Twitter/X | `TWITTER_CLIENT_ID/SECRET` cru | `social-auth-init:91` \u00b7 `social-auth-callback:160-161` \u00b7 `refresh-social-token:117-118` |\n| TikTok \u00b7 YouTube \u00b7 Pinterest | `resolveSocialAppCreds` (per-user \u2192 env \u2192 402) | \u2014 |\n\nO `refresh-social-token` \u00e9 o **chokepoint \u00fanico** de refresh das 6 plataformas (provado no sweep 2026-07-16); `publish-social:87` e `youtube-data:54` delegam a ele via HTTP.\n\n## \u00a71 Decis\u00e3o de design\n\n**Linhas globais = `user_id IS NULL` na pr\u00f3pria `social_app_config_table`.** Precedente can\u00f4nico do projeto: system nodes da Knowledge Mesh (`mcorch_nodes.user_id IS NULL` = vis\u00edvel a todos os tenants). Zero tabela nova para credenciais; Vault trigger, masked view e decrypted view **reusados sem mudan\u00e7a** (nenhuma delas filtra `user_id`).\n\n**Resolver vira 4 degraus (ordem UNBREAKABLE):**\n\n```\n(1) social_app_config per-user (user_id = auth.uid(), is_active)   \u2190 BYOK do tenant\n(2) social_app_config GLOBAL   (user_id IS NULL,    is_active)     \u2190 admin-gerenciada, NOVA\n(3) Deno.env fallback                                              \u2190 legado/emerg\u00eancia (deixa de ser caminho operacional)\n(4) hard-fail 402 {error:\"<platform>_not_configured\"}\n```\n\n**Lembretes de rota\u00e7\u00e3o = tabela `admin_reminders`** (persistente at\u00e9 `resolved_at`, RLS admin-only). O sistema `notifications` existente n\u00e3o serve: sem\u00e2ntica read\u2260resolved, sino global some da vista, client INSERT bloqueado. A tabela \u00e9 gen\u00e9rica \u2014 pend\u00eancias Sovereign futuras (e o guardian MAPE-K) podem semear lembretes.\n\n## \u00a72 Functional Requirements\n\n### FR-PE-017 \u2014 Linhas globais em `social_app_config` (Critical \u00b7 DB)\nMigration `20260716210000_global_app_credentials_admin_tier.sql`:\n- `ALTER COLUMN user_id DROP NOT NULL` (FK a `auth.users` permanece para linhas n\u00e3o-nulas).\n- Unicidade global: `CREATE UNIQUE INDEX ... ON social_app_config_table (platform) WHERE user_id IS NULL` (o `UNIQUE(user_id, platform)` n\u00e3o deduplica NULLs).\n- RLS nova na base table: `FOR ALL USING (user_id IS NULL AND public.has_role('admin')) WITH CHECK (mesmo predicado)` \u2014 assinatura **single-arg** `has_role(_role app_role)` (migration `20260414154016`, l\u00ea `auth.uid()` internamente).\n- INSTEAD OF trigger (`trg_instead_of_social_app_config`): exemption no guard 42501 dos branches INSERT/UPDATE \u2014 escrita com `NEW.user_id IS NULL` permitida **somente** quando `public.has_role('admin')`. User comum com `user_id NULL` \u2192 RAISE (predicado composto). Admin escrevendo linha de OUTRO user \u2192 cai no guard normal \u2192 RAISE (inalterado). DELETE: seguro por constru\u00e7\u00e3o \u2014 a view `security_invoker` s\u00f3 exp\u00f5e ao caller linhas que a RLS permite ver.\n- `client_secret` global cifra no MESMO Vault trigger (`trg_encrypt_social_app_config`) \u2014 nasce cifrada, mask `\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022` na view p\u00fablica, plaintext s\u00f3 em `decrypted_social_app_config` (service_role).\n\n### FR-PE-018 \u2014 Resolver 4 degraus + cobertura das 6 plataformas (Critical \u00b7 Edge)\n- `_shared/social-app-config.ts`: degrau global `(user_id IS NULL, is_active)` entre per-user e env; `source: \"per-user\" | \"global\" | \"env\"`.\n- `SocialAppPlatform` estende para `linkedin | instagram | twitter` (facebook usa as credenciais instagram \u2014 branch `instagram||facebook` existente). `ENV_MAP` ganha `LINKEDIN_CLIENT_ID/SECRET`, `INSTAGRAM_APP_ID/SECRET`, `TWITTER_CLIENT_ID/SECRET`.\n- Os **9 call-sites raw-env** (\u00a70) migram para `resolveSocialAppCreds` \u2014 fail-closed 402 estruturado substitui os 500/throw legados. Webhooks Meta (verify token/HMAC \u2014 system-level, sem user no path) permanecem env por defini\u00e7\u00e3o (documentado, n\u00e3o \u00e9 viola\u00e7\u00e3o do Tenancy Model).\n\n### FR-PE-019 \u2014 Admin UI `GlobalAppKeysPanel` (High \u00b7 UI pt-BR)\n- Tab nova **\"Chaves\"** (`KeyRound`) na AdminPage (precedente: painel Pantheon = componente em `src/components/admin/` + TabsTrigger).\n- Reusa a anatomia do `SocialAppConfigCard` per-user: client_id pr\u00e9-preenchido, secret write-only com mask sentinel, \"secret obrigat\u00f3rio s\u00f3 no 1\u00ba save\", badge \"Configurado\", bot\u00e3o salvar por se\u00e7\u00e3o, bloco copi\u00e1vel do redirect URI (`SOCIAL_OAUTH_REDIRECT_URI`).\n- Write pattern **obrigat\u00f3rio** (encrypted views): read-then-branch \u2014 `UPDATE ... .eq('id', existing.id)` OU `.insert({ user_id: null, platform, ... })`. **NUNCA `.upsert()`**. Guard de mask round-trip (`secret !== SOCIAL_SECRET_MASK`).\n- Plataformas do painel: `linkedin \u00b7 instagram (Meta) \u00b7 twitter (X) \u00b7 tiktok \u00b7 youtube (Google) \u00b7 pinterest` (`GLOBAL_APP_PLATFORMS`). O card per-user de Settings permanece com 3 (inalterado nesta fatia).\n\n### FR-PE-020 \u2014 `admin_reminders` + banner de rota\u00e7\u00e3o (High \u00b7 DB+UI)\n- Tabela: `id uuid PK \u00b7 slug text UNIQUE \u00b7 title text \u00b7 details text \u00b7 severity CHECK (info|warning|critical) \u00b7 created_at \u00b7 resolved_at timestamptz NULL \u00b7 resolved_by uuid NULL`. RLS `FOR ALL USING/WITH CHECK (public.has_role('admin'))`.\n- Seed idempotente (3 lembretes de rota\u00e7\u00e3o pendentes da fila 2026-07-14/15): `rotate-vertex-sa` \u00b7 `rotate-gemini-key` \u00b7 `rotate-telegram-token`.\n- Banner `AdminRemindersBanner` (shadcn `Alert`, tom warning) **top-level acima das Tabs** (precedente SovereignBalancePanel \u2014 vis\u00edvel em qualquer tab): lista n\u00e3o-resolvidos + bot\u00e3o \"Marcar como resolvido\" (`resolved_at = now(), resolved_by = auth.uid()`).\n\n### FR-PE-021 \u2014 TikTok Login Kit alinhado ao tier global (Medium \u00b7 Edge)\n`_shared/tiktok-login-creds.ts` (`resolveTikTokLoginCreds`, pr\u00e9-sess\u00e3o \u2014 sem `auth.uid()`): ordem passa a `global row \u2192 env \u2192 single-active-row legado (compat single-tenant)`. Elimina a depend\u00eancia do \"primeiro row ativo de qualquer tenant\" assim que a linha global existir.\n\n## \u00a73 OTDs \u2014 fechamento e continuidade\n\n| OTD | Estado | Racional |\n|---|---|---|\n| **OTD-PE-SOCIAL-APPCREDS** (Amendment 10 \u00a74 \u00b7 SLA \"antes do 2\u00ba tenant\") | **FECHADA por esta amendment** | O crit\u00e9rio era promover env\u2192per-user antes do 2\u00ba tenant. O tier global admin-gerenciado supera o crit\u00e9rio: env deixa de ser caminho operacional (vira legado/emerg\u00eancia), a credencial compartilhada passa a ser **expl\u00edcita, cifrada, audit\u00e1vel e rotacion\u00e1vel pela UI** \u2014 n\u00e3o mais d\u00edvida silenciosa. |\n| **OTD-SOCIAL-APP-ENV-FALLBACK** (SOP pinterest \u00a7Known debt) | **FECHADA junto** | Mesmo deferral, mesmo fechamento. |\n| **OTD-META-ENCRYPT** | segue aberta | at-rest das tabelas legadas fora de escopo aqui. |\n| **OTD-PE-GLOBAL-OTHER-SECRETS** (NOVA \u00b7 baixa) | aberta | \"Outras coisas globais\" n\u00e3o-OAuth (ex.: chaves de sistema `MESH_EMBED_*`, Telegram bot) exigem refactor de cada edge fn consumidora \u2014 fatia futura; o lembrete de rota\u00e7\u00e3o j\u00e1 as cobre operacionalmente. |\n\n## \u00a74 Seguran\u00e7a (gate obrigat\u00f3rio)\n\n- **/security-review OBRIGAT\u00d3RIO na migration antes do commit** (FMEA-011 \u2014 camada de credencial).\n- Vetores analisados no design: (a) user comum forjando linha global \u2192 bloqueado por RLS + guard composto no INSTEAD OF; (b) enumera\u00e7\u00e3o do secret global \u2192 mask na view p\u00fablica + `REVOKE SELECT (client_secret)` na base (inalterados); (c) DELETE cross-tenant via view \u2192 visibilidade RLS `security_invoker` restringe OLD \u00e0s linhas vis\u00edveis; (d) downgrade de linha global para pessoal por admin \u2192 sem impacto (admin j\u00e1 gerencia o tier); (e) secret plaintext no browser \u2192 nunca: write-only, leitura s\u00f3 mascarada.\n- `admin_reminders` n\u00e3o guarda segredo \u2014 s\u00f3 t\u00edtulos/slugs.\n\n## \u00a75 Pattern Conformance Declaration (inline \u2014 toca 4 padr\u00f5es materialmente)\n\n| Pattern (agentic-vision) | Implemented? | How |\n|---|---|---|\n| Guardrails / Safety | yes | fail-closed 402 estruturado nas 6 plataformas; RLS + trigger-guard composto; mask sentinel |\n| Multi-tenancy / Isolation | yes | tier global expl\u00edcito user_id-NULL (padr\u00e3o system-nodes) sem tocar isolamento per-user |\n| Tool Use (external APIs) | yes | resolver \u00fanico para 6 provedores OAuth; chokepoint de refresh preservado |\n| Human-in-the-Loop | yes | admin UI + lembretes de rota\u00e7\u00e3o persistentes (gate humano de credencial) |\n| Demais 17 padr\u00f5es | n-a | fatia de credencial/UI \u2014 sem mudan\u00e7a de loop ag\u00eantico, mem\u00f3ria, planejamento ou economia |\n\n## \u00a76 Traceabilidade\n\n- BR/FR: FR-PE-017..021 (esta amendment) \u00b7 estende FR-PE-005..009 (Amendment 10).\n- Mesh: n\u00f3 observation no 1\u00ba run bem-sucedido do tier global (mandato \u00a73 CLAUDE.md); telemetria `infra_health_logs` nos paths de erro do resolver (existente, herdada).\n- Key Files: entrada nova no CLAUDE.md na entrega da fatia.\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/post-engine/16-amendment-global-app-credentials-admin-tier.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:23:56)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/admin-global-app-credentials.md",
  "content": "# SOP \u2014 Credenciais Globais de Aplicativo (Admin Tier) + Rota\u00e7\u00e3o\n\n> **Status:** ATIVA v1.0 \u00b7 2026-07-16 \u00b7 Lei 2 (Processo Antecipado) \u2014 escrita ANTES do c\u00f3digo.\n> **BoK SSOT:** `docs/bok/post-engine/16-amendment-global-app-credentials-admin-tier.md` (FR-PE-017..021).\n> **Escopo:** credenciais de APP OAuth (client_id + client_secret) das 6 plataformas sociais, gerenciadas pelo admin em `/dashboard/admin` \u2192 tab \"Chaves\", gravadas como linhas `user_id IS NULL` de `social_app_config` (Vault-cifradas). Inclui o ciclo de rota\u00e7\u00e3o com lembretes persistentes.\n\n---\n\n## Operator\n\n| Papel | Quem | Ferramenta |\n|---|---|---|\n| Admin (tier global) | Sovereign (Gabriel) | `/dashboard/admin` \u2192 tab **Chaves** |\n| Tenant (BYOK per-user) | qualquer usu\u00e1rio | `/dashboard/settings` \u2192 tab Social (inalterado) |\n| Runtime | edge fns `social-auth-init` / `social-auth-callback` / `refresh-social-token` / `tiktok-login-*` | `resolveSocialAppCreds` (per-user \u2192 global \u2192 env \u2192 402) |\n\n## Sequence (fluxo manual completo)\n\n1. **Console da plataforma** \u2014 criar/abrir o app no developer console (Pinterest: developers.pinterest.com; Google: console.cloud.google.com; TikTok: developers.tiktok.com; etc.). Crit\u00e9rio: App ID + App Secret vis\u00edveis.\n2. **Registrar o redirect URI** no console \u2014 valor EXATO (sem wildcard):\n   `https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback`\n   Crit\u00e9rio: URI listado no console. (Pinterest exige match exato; TikTok/Google idem.)\n3. **Colar as credenciais** em `/dashboard/admin` \u2192 tab **Chaves** \u2192 se\u00e7\u00e3o da plataforma \u2192 App ID no campo `client_id`, Secret no campo write-only \u2192 **Salvar**. Crit\u00e9rio: toast de sucesso + badge **\"Configurado\"**.\n4. **Verificar materialmente (Lei 1)** \u2014 linha global existe e o secret virou refer\u00eancia Vault (nunca plaintext):\n   ```sql\n   SELECT platform, user_id, is_active,\n          client_secret ~ '^[0-9a-f-]{36}$' AS secret_is_vault_uuid\n   FROM social_app_config_table WHERE user_id IS NULL;\n   ```\n   Crit\u00e9rio: `user_id NULL \u00b7 is_active t \u00b7 secret_is_vault_uuid t`.\n5. **Conectar como usu\u00e1rio** \u2014 `/dashboard/social` \u2192 card da plataforma \u2192 Conectar \u2192 consent \u2192 volta conectado. Crit\u00e9rio: linha em `social_accounts` com `is_active=true` + scopes concedidos.\n6. **Rota\u00e7\u00e3o (ciclo recorrente)** \u2014 no console: *Redefinir segredo* \u2192 colar o secret novo na mesma se\u00e7\u00e3o da tab Chaves (client_id intocado; UPDATE in-place re-cifra no Vault) \u2192 no banner de lembretes, **\"Marcar como resolvido\"** no item correspondente. Crit\u00e9rio: `resolved_at` preenchido + conex\u00f5es novas funcionando com o secret novo.\n\n## Verification gates\n\n| Gate | Prova material |\n|---|---|\n| **G1** Linha global cifrada | Query do passo 4 \u2014 `secret_is_vault_uuid = t` |\n| **G2** Resolver usa o tier global | Tenant SEM linha per-user conecta com sucesso; log do resolver `source=\"global\"` |\n| **G3** Isolamento (FMEA-011) | User n\u00e3o-admin: SELECT na view \u2192 0 linhas globais; INSERT/UPDATE com `user_id NULL` \u2192 erro 42501 |\n| **G4** Mask round-trip | Re-salvar s\u00f3 o client_id (secret vazio) N\u00c3O destr\u00f3i o secret armazenado; view segue mascarando `\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022` |\n| **G5** Env nunca prim\u00e1rio | `grep` nos edge fns: zero leitura crua de `LINKEDIN_/INSTAGRAM_/TWITTER_CLIENT` fora do `ENV_MAP` do resolver |\n| **G6** Lembrete persiste | `admin_reminders` n\u00e3o-resolvido sobrevive a reload/nova sess\u00e3o; some do banner s\u00f3 com `resolved_at` |\n\n## Recovery path\n\n- **Secret colado errado** \u2192 recolar o correto na mesma se\u00e7\u00e3o (UPDATE in-place; `vault_upsert_secret` re-cifra por nome \u2014 sem 23505).\n- **Falha no OAuth p\u00f3s-troca** (401/invalid_client) \u2192 conferir no console se o secret foi *redefinido* (o antigo morre na hora em algumas plataformas); recolar o vigente.\n- **Linha global \u00f3rf\u00e3/indevida** \u2192 deletar pela UI admin (DELETE via view; visibilidade RLS garante que s\u00f3 admin alcan\u00e7a) e recriar.\n- **Rollback da migration** \u2192 restaurar `NOT NULL` exige antes remover as linhas globais; policies/\u00edndice parcial t\u00eam `DROP ... IF EXISTS` determin\u00edstico.\n- **429/rate-limit da plataforma** com credencial global compartilhada \u2192 tenant afetado migra para BYOK per-user (degrau 1 j\u00e1 resolve na frente do global).\n\n## Success signal\n\nConnect Pinterest E2E do Usu\u00e1rio Zero **usando a credencial global colada pela UI admin** (zero `.env`, zero CLI): linha `social_accounts` `platform='pinterest' \u00b7 is_active=true` + badge conectado em `/dashboard/social` + n\u00f3 observation na malha.\n\n## Known debt\n\n- **OTD-PE-GLOBAL-OTHER-SECRETS** \u2014 segredos globais n\u00e3o-OAuth (Telegram bot, chaves de sistema `MESH_EMBED_*`) seguem em env; cobertos operacionalmente pelo lembrete de rota\u00e7\u00e3o, migra\u00e7\u00e3o de leitura \u00e9 fatia futura.\n- Webhooks Meta (verify token / HMAC) s\u00e3o system-level por defini\u00e7\u00e3o \u2014 permanecem env (n\u00e3o \u00e9 viola\u00e7\u00e3o do Tenancy Model).\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/processes/admin-global-app-credentials.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:24:36)*


## 🤖 Claude *(21:24:36)*

Task 3 selada (amendment + SOP). Agora a migration (task 4):

## 🤖 Claude *(21:24:36)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "3",
  "status": "completed"
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #3 status
> ```

## 🤖 Claude *(21:24:37)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "4",
  "status": "in_progress",
  "activeForm": "Escrevendo migration do tier global + admin_reminders"
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #4 activeForm, status
> ```

## 🤖 Claude *(21:25:12)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260716210000_global_app_credentials_admin_tier.sql",
  "content": "-- 20260716210000_global_app_credentials_admin_tier.sql\n-- Global App Credentials (Admin Tier) + admin_reminders \u2014 FR-PE-017 / FR-PE-020.\n-- BoK SSOT: docs/bok/post-engine/16-amendment-global-app-credentials-admin-tier.md\n-- SOP (Lei 2, written first): docs/processes/admin-global-app-credentials.md\n--\n-- WHY: the global fallback for OAuth app credentials is Deno.env (CLI-only), the deferral recorded in\n-- OTD-PE-SOCIAL-APPCREDS (\"SLA: before the 2nd tenant\"). This migration closes it by design: global\n-- credentials become EXPLICIT rows (user_id IS NULL \u2014 the same convention as mcorch_nodes system nodes),\n-- Vault-encrypted by the EXISTING trigger, masked by the EXISTING view, manageable by admins from\n-- /dashboard/admin with zero CLI. Resolution order becomes: per-user \u2192 global \u2192 env \u2192 402.\n--\n-- Security posture: HARDENS overall (env shared-key stops being the operational path). New surfaces are\n-- admin-gated twice: RLS policy on the base table (reads) + composite guard in the INSTEAD OF trigger\n-- (writes through the view). has_role is the deployed SINGLE-ARG canonical (migration 20260414154016,\n-- reads auth.uid() internally). /security-review MANDATORY before commit (FMEA-011 \u2014 credential layer).\n\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- 1. Allow global rows: user_id becomes nullable (FK still validates non-NULL values)\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nALTER TABLE public.social_app_config_table\n  ALTER COLUMN user_id DROP NOT NULL;\n\n-- UNIQUE(user_id, platform) does not dedupe NULLs \u2014 enforce ONE global row per platform explicitly.\nCREATE UNIQUE INDEX IF NOT EXISTS uniq_social_app_config_global_platform\n  ON public.social_app_config_table (platform)\n  WHERE user_id IS NULL;\n\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- 2. RLS: admins manage GLOBAL rows (per-user policy untouched; default-deny for everyone else)\n--    Note: reads through the masked security_invoker view apply this policy to the invoker, so an\n--    admin sees global rows MASKED ('\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'); plaintext stays service-role-only via\n--    decrypted_social_app_config. Base-table client_secret keeps its column REVOKE.\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nDROP POLICY IF EXISTS \"Admins manage global social app config\" ON public.social_app_config_table;\nCREATE POLICY \"Admins manage global social app config\" ON public.social_app_config_table\n  FOR ALL\n  USING (user_id IS NULL AND public.has_role('admin'::public.app_role))\n  WITH CHECK (user_id IS NULL AND public.has_role('admin'::public.app_role));\n\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- 3. INSTEAD OF trigger: admin exemption for global-row writes through the view.\n--    Original guard raised 42501 whenever NEW.user_id IS DISTINCT FROM auth.uid() (non-service_role) \u2014\n--    which blocks user_id NULL for EVERYONE. New composite predicate: a NULL-user write is allowed\n--    ONLY for admins; a non-admin writing user_id NULL still hits the original 42501; an admin writing\n--    ANOTHER user's row still hits the original 42501 (unchanged).\n--    DELETE branch stays guard-free BY CONSTRUCTION: the security_invoker view only yields OLD rows the\n--    caller's RLS can see (non-admins cannot see global rows, so they cannot delete them).\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nCREATE OR REPLACE FUNCTION public.trg_instead_of_social_app_config()\nRETURNS TRIGGER\nLANGUAGE plpgsql\nSECURITY DEFINER\nSET search_path = ''\nAS $$\nBEGIN\n  IF TG_OP = 'DELETE' THEN\n    DELETE FROM public.social_app_config_table WHERE id = OLD.id;\n    RETURN OLD;\n  ELSIF TG_OP = 'INSERT' THEN\n    -- Tenant guard (mirrors 20260602150000) + admin exemption for GLOBAL rows (FR-PE-017):\n    -- non-service_role may write its OWN row, or a user_id-NULL row iff it holds the admin role.\n    IF auth.role() IS DISTINCT FROM 'service_role'\n       AND NEW.user_id IS DISTINCT FROM auth.uid()\n       AND NOT (NEW.user_id IS NULL AND public.has_role('admin'::public.app_role)) THEN\n      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';\n    END IF;\n    INSERT INTO public.social_app_config_table (\n      id, user_id, platform, client_id, client_secret, scopes, metadata, is_active\n    ) VALUES (\n      COALESCE(NEW.id, gen_random_uuid()), NEW.user_id, NEW.platform, NEW.client_id, NEW.client_secret,\n      COALESCE(NEW.scopes, '{}'), COALESCE(NEW.metadata, '{}'::jsonb), COALESCE(NEW.is_active, TRUE)\n    );\n    RETURN NEW;\n  ELSIF TG_OP = 'UPDATE' THEN\n    IF auth.role() IS DISTINCT FROM 'service_role'\n       AND NEW.user_id IS DISTINCT FROM auth.uid()\n       AND NOT (NEW.user_id IS NULL AND public.has_role('admin'::public.app_role)) THEN\n      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';\n    END IF;\n    UPDATE public.social_app_config_table SET\n      user_id = NEW.user_id,\n      platform = NEW.platform,\n      client_id = NEW.client_id,\n      -- preserve the stored secret when the client writes back the mask sentinel\n      client_secret = COALESCE(NULLIF(NEW.client_secret, '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'), public.social_app_config_table.client_secret),\n      scopes = COALESCE(NEW.scopes, public.social_app_config_table.scopes),\n      metadata = COALESCE(NEW.metadata, public.social_app_config_table.metadata),\n      is_active = COALESCE(NEW.is_active, public.social_app_config_table.is_active),\n      updated_at = now()\n    WHERE id = OLD.id;\n    RETURN NEW;\n  END IF;\n  RETURN NULL;\nEND;\n$$;\n\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- 4. admin_reminders \u2014 persistent Sovereign to-dos surfaced on /dashboard/admin (FR-PE-020).\n--    No secrets stored here (titles/slugs only). Admin-gated FOR ALL; default-deny otherwise.\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nCREATE TABLE IF NOT EXISTS public.admin_reminders (\n    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),\n    slug TEXT NOT NULL UNIQUE,\n    title TEXT NOT NULL,\n    details TEXT,\n    severity TEXT NOT NULL DEFAULT 'warning' CHECK (severity IN ('info', 'warning', 'critical')),\n    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),\n    resolved_at TIMESTAMPTZ,\n    resolved_by UUID REFERENCES auth.users(id) ON DELETE SET NULL\n);\n\nALTER TABLE public.admin_reminders ENABLE ROW LEVEL SECURITY;\n\nDROP POLICY IF EXISTS \"Admins manage reminders\" ON public.admin_reminders;\nCREATE POLICY \"Admins manage reminders\" ON public.admin_reminders\n  FOR ALL\n  USING (public.has_role('admin'::public.app_role))\n  WITH CHECK (public.has_role('admin'::public.app_role));\n\n-- Seed: the 3 pending credential rotations from the 2026-07-14/15 queue (idempotent by slug).\nINSERT INTO public.admin_reminders (slug, title, details, severity) VALUES\n  ('rotate-vertex-sa', 'Rotacionar service account Vertex (gabrielai-veo)',\n   'Chave privada do SA foi colada no chat em 2026-07-14. Gerar chave nova no IAM do projeto, atualizar a credencial no pool BYOK (Settings \u2192 Provedores) e revogar a chave antiga.', 'critical'),\n  ('rotate-gemini-key', 'Rotacionar chave Gemini exposta',\n   'Chave Gemini exposta em sess\u00e3o anterior (fluxo n8n/creative). Gerar nova em aistudio.google.com, atualizar onde usada e revogar a antiga.', 'critical'),\n  ('rotate-telegram-token', 'Rotacionar token do bot Telegram',\n   'Token do bot exposto em sess\u00e3o anterior (n8n). Revogar via @BotFather (/revoke) e atualizar morning-briefing/guardian.', 'warning')\nON CONFLICT (slug) DO NOTHING;\n\nCOMMENT ON TABLE public.admin_reminders IS\n  'Persistent admin to-dos (e.g., credential rotation) surfaced as a banner on /dashboard/admin. '\n  'Admin-only RLS (single-arg has_role). Resolved by setting resolved_at/resolved_by. No secrets stored.';\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260716210000_global_app_credentials_admin_tier.sql (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:25:20)*


## 🤖 Claude *(21:25:20)*

Migration escrita. Agora o código edge — lendo os call-sites raw-env que migram para o resolver:

## 🤖 Claude *(21:25:21)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-callback/index.ts",
  "offset": 80,
  "limit": 120
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 80	
> 81	    const callbackUrl = `${Deno.env.get("SUPABASE_URL")}/functions/v1/social-auth-callback`;
> 82	
> 83	    let accessToken: string;
> 84	    let refreshToken: string | null = null;
> 85	    let expiresIn: number | null = null;
> 86	    let platformUserId: string | null = null;
> 87	    let platformUsername: string | null = null;
> 88	    let scopes: string[] = [];
> 89	    // Per-platform extra fields stashed in social_accounts.metadata (e.g. YouTube channel_id,
> 90	    // Pinterest refresh_token_expires_at). Empty for platforms that don't need it.
> 91	    let metadata: Record<string, unknown> = {};
> 92	
> 93	    if (platform === "linkedin") {
> 94	      const clientId = Deno.env.get("LINKEDIN_CLIENT_ID")!;
> 95	      const clientSecret = Deno.env.get("LINKEDIN_CLIENT_SECRET")!;
> 96	
> 97	      const tokenRes = await fetch("https://www.linkedin.com/oauth/v2/accessToken", {
> 98	        method: "POST",
> 99	        headers: { "Content-Type": "application/x-www-form-urlencoded" },
> 100	        body: new URLSearchParams({
> 101	          grant_type: "authorization_code",
> 102	          code,
> 103	          redirect_uri: callbackUrl,
> 104	          client_id: clientId,
> 105	          client_secret: clientSecret,
> 106	        }),
> 107	      });
> 108	      const tokenData = await tokenRes.json();
> 109	      if (!tokenRes.ok) throw new Error(tokenData.error_description || "LinkedIn token exchange failed");
> 110	
> 111	      accessToken = tokenData.access_token;
> 112	      refreshToken = tokenData.refresh_token || null;
> 113	      expiresIn = tokenData.expires_in;
> 114	      scopes = (tokenData.scope || "").split(" ");
> 115	
> 116	      const profileRes = await fetch("https://api.linkedin.com/v2/userinfo", {
> 117	        headers: { Authorization: `Bearer ${accessToken}` },
> 118	      });
> 119	      const profile = await profileRes.json();
> 120	      platformUserId = profile.sub;
> 121	      platformUsername = profile.name || profile.email;
> 122	
> 123	    } else if (platform === "instagram" || platform === "facebook") {
> 124	      const appId = Deno.env.get("INSTAGRAM_APP_ID")!;
> 125	      const appSecret = Deno.env.get("INSTAGRAM_APP_SECRET")!;
> 126	
> 127	      // Instagram Login — short-lived token
> 128	      const tokenRes = await fetch("https://api.instagram.com/oauth/access_token", {
> 129	        method: "POST",
> 130	        headers: { "Content-Type": "application/x-www-form-urlencoded" },
> 131	        body: new URLSearchParams({
> 132	          client_id: appId,
> 133	          client_secret: appSecret,
> 134	          grant_type: "authorization_code",
> 135	          redirect_uri: callbackUrl,
> 136	          code,
> 137	        }),
> 138	      });
> 139	      const tokenData = await tokenRes.json();
> 140	      if (!tokenRes.ok || tokenData.error_type) throw new Error(tokenData.error_message || "Instagram token exchange failed");
> 141	
> 142	      const shortToken = tokenData.access_token;
> 143	      platformUserId = String(tokenData.user_id);
> 144	
> 145	      // Exchange for long-lived token (60 days)
> 146	      const longRes = await fetch(
> 147	        `https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=${appSecret}&access_token=${shortToken}`
> 148	      );
> 149	      const longData = await longRes.json();
> 150	      accessToken = longData.access_token || shortToken;
> 151	      expiresIn = longData.expires_in || null;
> 152	      scopes = ["instagram_business_basic", "instagram_business_content_publish"];
> 153	
> 154	      // Fetch username
> 155	      const meRes = await fetch(`https://graph.instagram.com/v21.0/me?fields=username,name&access_token=${accessToken}`);
> 156	      const me = await meRes.json();
> 157	      platformUsername = me.username || me.name || platformUserId;
> 158	
> 159	    } else if (platform === "twitter") {
> 160	      const clientId = Deno.env.get("TWITTER_CLIENT_ID")!;
> 161	      const clientSecret = Deno.env.get("TWITTER_CLIENT_SECRET")!;
> 162	
> 163	      // PKCE code verifier = the state used as plain challenge
> 164	      const codeVerifier = stateStr.slice(0, 43);
> 165	
> 166	      const tokenRes = await fetch("https://api.x.com/2/oauth2/token", {
> 167	        method: "POST",
> 168	        headers: {
> 169	          "Content-Type": "application/x-www-form-urlencoded",
> 170	          Authorization: `Basic ${btoa(`${clientId}:${clientSecret}`)}`,
> 171	        },
> 172	        body: new URLSearchParams({
> 173	          grant_type: "authorization_code",
> 174	          code,
> 175	          redirect_uri: callbackUrl,
> 176	          code_verifier: codeVerifier,
> 177	        }),
> 178	      });
> 179	      const tokenData = await tokenRes.json();
> 180	      if (!tokenRes.ok) throw new Error(tokenData.error_description || tokenData.detail || "Twitter token exchange failed");
> 181	
> 182	      accessToken = tokenData.access_token;
> 183	      refreshToken = tokenData.refresh_token || null;
> 184	      expiresIn = tokenData.expires_in;
> 185	      scopes = (tokenData.scope || "").split(" ");
> 186	
> 187	      // Fetch user info
> 188	      const meRes = await fetch("https://api.x.com/2/users/me", {
> 189	        headers: { Authorization: `Bearer ${accessToken}` },
> 190	      });
> 191	      const meData = await meRes.json();
> 192	      platformUserId = meData.data?.id;
> 193	      platformUsername = meData.data?.username;
> 194	
> 195	    } else if (platform === "tiktok") {
> 196	      // App credentials resolve per-user → env fallback → hard-fail (FR-PE-005/009).
> 197	      const creds = await resolveSocialAppCreds(supabase, userId, "tiktok");
> 198	
> 199	      // Exchange code → token (form-encoded; client_key/client_secret per TikTok OAuth).
> ```

## 🤖 Claude *(21:25:22)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/refresh-social-token/index.ts",
  "offset": 75,
  "limit": 75
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 75	
> 76	    let newAccessToken: string;
> 77	    let newExpiresAt: string | null = null;
> 78	
> 79	    if (account.platform === "linkedin") {
> 80	      if (!account.refresh_token) {
> 81	        return new Response(JSON.stringify({ error: "No refresh token available" }), {
> 82	          status: 400,
> 83	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 84	        });
> 85	      }
> 86	      const res = await fetch("https://www.linkedin.com/oauth/v2/accessToken", {
> 87	        method: "POST",
> 88	        headers: { "Content-Type": "application/x-www-form-urlencoded" },
> 89	        body: new URLSearchParams({
> 90	          grant_type: "refresh_token",
> 91	          refresh_token: account.refresh_token,
> 92	          client_id: Deno.env.get("LINKEDIN_CLIENT_ID")!,
> 93	          client_secret: Deno.env.get("LINKEDIN_CLIENT_SECRET")!,
> 94	        }),
> 95	      });
> 96	      const data = await res.json();
> 97	      if (!res.ok) throw new Error(data.error_description || "LinkedIn refresh failed");
> 98	      newAccessToken = data.access_token;
> 99	      newExpiresAt = new Date(Date.now() + data.expires_in * 1000).toISOString();
> 100	    } else if (account.platform === "instagram" || account.platform === "facebook") {
> 101	      const res = await fetch(
> 102	        `https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id=${Deno.env.get("INSTAGRAM_APP_ID")}&client_secret=${Deno.env.get("INSTAGRAM_APP_SECRET")}&fb_exchange_token=${account.access_token}`
> 103	      );
> 104	      const data = await res.json();
> 105	      if (!res.ok) throw new Error(data.error?.message || "Facebook refresh failed");
> 106	      newAccessToken = data.access_token;
> 107	      newExpiresAt = data.expires_in
> 108	        ? new Date(Date.now() + data.expires_in * 1000).toISOString()
> 109	        : null;
> 110	    } else if (account.platform === "twitter") {
> 111	      if (!account.refresh_token) {
> 112	        return new Response(JSON.stringify({ error: "No refresh token available" }), {
> 113	          status: 400,
> 114	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 115	        });
> 116	      }
> 117	      const clientId = Deno.env.get("TWITTER_CLIENT_ID")!;
> 118	      const clientSecret = Deno.env.get("TWITTER_CLIENT_SECRET")!;
> 119	      const res = await fetch("https://api.x.com/2/oauth2/token", {
> 120	        method: "POST",
> 121	        headers: {
> 122	          "Content-Type": "application/x-www-form-urlencoded",
> 123	          Authorization: `Basic ${btoa(`${clientId}:${clientSecret}`)}`,
> 124	        },
> 125	        body: new URLSearchParams({
> 126	          grant_type: "refresh_token",
> 127	          refresh_token: account.refresh_token,
> 128	        }),
> 129	      });
> 130	      const data = await res.json();
> 131	      if (!res.ok) throw new Error(data.error_description || "Twitter refresh failed");
> 132	      newAccessToken = data.access_token;
> 133	      newExpiresAt = data.expires_in
> 134	        ? new Date(Date.now() + data.expires_in * 1000).toISOString()
> 135	        : null;
> 136	
> 137	      if (data.refresh_token) {
> 138	        await admin
> 139	          .from("social_accounts")
> 140	          .update({ refresh_token: data.refresh_token })
> 141	          .eq("id", social_account_id);
> 142	      }
> 143	    } else if (account.platform === "tiktok") {
> 144	      if (!account.refresh_token) {
> 145	        return new Response(JSON.stringify({ error: "No refresh token available" }), {
> 146	          status: 400,
> 147	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 148	        });
> 149	      }
> ```

## 🤖 Claude *(21:25:23)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/tiktok-login-creds.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// Resolve the MCORCH TikTok app credentials for the (global, pre-auth) LOGIN flow.
> 2	//
> 3	// Key insight (Sovereign 2026-07-08): the MCORCH TikTok app is ONE app — the login uses the SAME client_key/secret
> 4	// the per-user CONNECT flow (/dashboard/social → social-auth-*) already has. Login has NO auth.uid() (there is no
> 5	// session yet), so it CANNOT be per-user; it uses the app-GLOBAL credential — which is that same key. So instead of
> 6	// provisioning a duplicate TIKTOK_CLIENT_KEY/SECRET, we read the existing credential from social_app_config.
> 7	//
> 8	// Resolution order: (1) system env override (a dedicated global cred, if ever set) → (2) the single active tiktok
> 9	// row in decrypted_social_app_config (single-tenant Usuário Zero: that row IS the app owner's = the same key as the
> 10	// connect). Reads via the SAME service-role view (decrypted_social_app_config) the connect's resolveSocialAppCreds
> 11	// already uses — no new credential surface.
> 12	//
> 13	// ⚠️ Multi-tenant note: when the product goes multi-tenant, "the single active tiktok config" is no longer the app
> 14	//    owner unambiguously — a dedicated global cred (env or an app_owner-scoped row) must be used. Tracked for that day.
> 15	import type { SupabaseClient } from "https://esm.sh/@supabase/supabase-js@2";
> 16	
> 17	export interface TikTokAppCreds {
> 18	  clientKey: string;
> 19	  clientSecret: string;
> 20	  source: "env" | "social_app_config";
> 21	}
> 22	
> 23	export async function resolveTikTokLoginCreds(admin: SupabaseClient): Promise<TikTokAppCreds | null> {
> 24	  const envKey = Deno.env.get("TIKTOK_CLIENT_KEY");
> 25	  const envSecret = Deno.env.get("TIKTOK_CLIENT_SECRET");
> 26	  if (envKey && envSecret) return { clientKey: envKey, clientSecret: envSecret, source: "env" };
> 27	
> 28	  const { data } = await admin
> 29	    .from("decrypted_social_app_config")
> 30	    .select("client_id, client_secret")
> 31	    .eq("platform", "tiktok")
> 32	    .eq("is_active", true)
> 33	    .limit(1)
> 34	    .maybeSingle();
> 35	  if (data?.client_id && data?.client_secret) {
> 36	    return { clientKey: String(data.client_id), clientSecret: String(data.client_secret), source: "social_app_config" };
> 37	  }
> 38	  return null;
> 39	}
> 40	
> ```

## 🤖 Claude *(21:26:20)*


## 🤖 Claude *(21:26:20)*


## 🤖 Claude *(21:26:55)*


🛠️ **Tool Call**: `Agent`
```json
{
  "description": "Client-side Admin Global Keys UI",
  "subagent_type": "general-purpose",
  "prompt": "Repo: /home/gcrUX/htdocs/constellation-orchestra (React+TS+Vite, shadcn, TanStack Query). Implement the CLIENT side of the \"Global App Credentials (Admin Tier)\" slice \u2014 BoK SSOT: docs/bok/post-engine/16-amendment-global-app-credentials-admin-tier.md (FR-PE-019/020). DO NOT touch supabase/functions/** or supabase/migrations/** (another operator owns those). UI text pt-BR, code/comments English. Follow existing patterns EXACTLY.\n\nFIRST read these files (they are your templates):\n- src/lib/social-app-config.ts\n- src/hooks/useSocialAppConfig.ts\n- src/components/settings/SocialAppConfigCard.tsx\n- src/pages/AdminPage.tsx\n- src/components/admin/SovereignBalancePanel.tsx (card style precedent)\n- src/components/icons/brand-icons.tsx\n- src/hooks/useAdminData.ts (admin gating/query patterns)\n\nThe DB migration (already written, will be applied) adds: (a) social_app_config global rows = user_id IS NULL, writable through the existing masked view by admins (INSTEAD OF trigger has an admin exemption); (b) table admin_reminders { id uuid, slug text unique, title text, details text, severity 'info'|'warning'|'critical', created_at, resolved_at timestamptz null, resolved_by uuid null } with admin-only RLS, seeded with 3 rotation reminders.\n\nDELIVERABLES:\n\n1. **Extend src/lib/social-app-config.ts** (do not break existing exports):\n   - `export type GlobalAppPlatform = SocialAppPlatform | 'linkedin' | 'instagram' | 'twitter';`\n   - `export const GLOBAL_APP_PLATFORMS: readonly GlobalAppPlatform[] = ['linkedin', 'instagram', 'twitter', 'tiktok', 'youtube', 'pinterest'];`\n   - `export const GLOBAL_APP_PLATFORM_META: Record<GlobalAppPlatform, SocialAppPlatformMeta>` \u2014 reuse the 3 existing entries (spread SOCIAL_APP_PLATFORM_META) + add linkedin (name \"LinkedIn\", console \"https://developer.linkedin.com \u2192 Apps\"), instagram (name \"Instagram / Facebook (Meta)\", console \"https://developers.facebook.com \u2192 Apps\", helper mentioning App ID/App Secret do app Meta), twitter (name \"X (Twitter)\", console \"https://developer.x.com \u2192 Projects & Apps\"). clientIdLabel: linkedin/twitter \"Client ID\", instagram \"App ID\". Helpers pt-BR one-liners explaining what the credential is.\n   - Keep types strict; the row type user_id becomes `string | null` if it isn't already.\n\n2. **New hook src/hooks/useGlobalAppConfig.ts** \u2014 adapted clone of useSocialAppConfig:\n   - Query: `.from('social_app_config').select(SOCIAL_APP_SAFE_COLUMNS).is('user_id', null)`, queryKey `['social_app_config', 'global']`, enabled always (page is admin-gated).\n   - saveConfig mutation: read-then-branch \u2014 if existing row for platform: `.update(writable).eq('id', existing.id)`; else `.insert({ user_id: null, platform, ...writable })`. NEVER `.upsert()`. Include secret in payload ONLY `if (secret && secret !== SOCIAL_SECRET_MASK)`. Always `is_active: true`. Invalidate the queryKey on success. Use the same untyped supabase cast pattern as useSocialAppConfig (view not in generated types).\n   - Platform param type: GlobalAppPlatform.\n\n3. **New hook src/hooks/useAdminReminders.ts**:\n   - Query unresolved: `.from('admin_reminders').select('*').is('resolved_at', null).order('severity')` \u2014 untyped cast (table not in generated types). queryKey ['admin_reminders'].\n   - Mutation `resolveReminder(id)`: `.update({ resolved_at: new Date().toISOString(), resolved_by: user.id }).eq('id', id)`; invalidate on success; pt-BR toasts (sonner).\n   - Export a Reminder type { id, slug, title, details: string|null, severity, created_at }.\n\n4. **New src/components/admin/AdminRemindersBanner.tsx** (display-only, logic in the hook):\n   - Renders nothing when list empty or loading.\n   - shadcn Alert (src/components/ui/alert.tsx) with warning tone (amber/yellow border like SovereignBalancePanel's `border-yellow-500/20`), icon AlertTriangle (lucide), title \"Rota\u00e7\u00e3o de credenciais pendente\" (or generic \"Lembretes do administrador\" if mixed severities), each reminder: title + details (muted, smaller) + Button variant=outline size=sm \"Marcar como resolvido\" with loading state.\n\n5. **New src/components/admin/GlobalAppKeysPanel.tsx** (display-only):\n   - Header: KeyRound icon + title \"Chaves de Aplicativo (Globais)\" + CardDescription: explains these are the platform app credentials (client_id + client_secret) used by ALL users' OAuth connect when they don't bring their own (BYOK), admin-only, encrypted in Vault; mention env/CLI is no longer needed.\n   - Copyable redirect URI block reusing SOCIAL_OAUTH_REDIRECT_URI (copy button, navigator.clipboard) \u2014 same pattern as SocialAppConfigCard.\n   - One bordered section per GLOBAL_APP_PLATFORMS entry mirroring PlatformSection from SocialAppConfigCard: brand icon, name, \"Configurado\" badge when configured (client_id present AND masked secret present AND is_active !== false \u2014 reuse/adapt isSocialAppConfigured), client_id Input prefilled from row, client_secret password Input write-only with mask placeholder when stored, secret required only on first save, per-section Save button with spinner, helper line + console link.\n   - Icons: brand-icons.tsx currently exports Instagram, Facebook, TikTok, YouTube, Pinterest. ADD LinkedIn and XTwitter glyphs there via the same makeBrandIcon helper (use the official simple-icons SVG paths for LinkedIn and X). Use Facebook+Instagram? No \u2014 instagram entry uses Instagram icon. linkedin \u2192 LinkedIn, twitter \u2192 XTwitter.\n\n6. **Wire into src/pages/AdminPage.tsx**:\n   - `<AdminRemindersBanner />` right below SovereignBalancePanel (above Tabs) \u2014 always visible.\n   - New tab: TabsTrigger value=\"keys\" with KeyRound icon and label \"Chaves\"; TabsContent renders <GlobalAppKeysPanel />. Adjust the TabsList grid class if it uses grid-cols-N so all triggers fit.\n\n7. **New test src/test/global-app-config.test.ts** (vitest, mirror src/test/meta.test.ts style):\n   - GLOBAL_APP_PLATFORM_META has an entry for every GLOBAL_APP_PLATFORMS value (name, clientIdLabel, helper, console all non-empty).\n   - GLOBAL_APP_PLATFORMS has no duplicates and includes the 3 legacy SOCIAL_APP_PLATFORMS.\n   - Mask/configured helpers behave (hasStoredSecret with mask, isSocialAppConfigured combinations) for a global row shape (user_id: null).\n\nVERIFY before returning: `cd /home/gcrUX/htdocs/constellation-orchestra && npx tsc --noEmit` (must be 0 errors) and `bun run test src/test/global-app-config.test.ts` (must pass). Do NOT run bun run build. Do NOT git commit.\n\nReturn: list of files created/modified with 1-line description each + tsc/test outputs (literal tail lines)."
}
```

> **Tool Result (Agent)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': "Async agent launched successfully. (This tool result is internal metadata — never quote or paste any part of it, including the agentId below, into a user-facing reply.)\nagentId: a89787906a8268bde (internal ID - do not mention to user. Use SendMessage with to: 'a89787906a8268bde', summary: '<5-10 word recap>' to continue this agent.)\nThe agent is working in the background. You will be notified automatically when it completes.\nDo not duplicate this agent's work — avoid working with the same files or topics it is using.\noutput_file: /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/30b8024d-52b5-4c1c-883b-b168f94313b7/tasks/a89787906a8268bde.output\nDo NOT Read or tail this file via the shell tool — it is the full subagent JSONL transcript and reading it will overflow your context. If the user asks for progress, say the agent is still running; you'll get a completion notification."}]
> ```

## 🤖 Claude *(21:27:07)*


## 🤖 Claude *(21:27:07)*

Agente client-side trabalhando. Agora o edge-side — primeiro o resolver:

## 🤖 Claude *(21:27:25)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/social-app-config.ts",
  "old_string": "// Shared: per-user OAuth APP credential resolution for TikTok / YouTube / Pinterest.\n// API Tenancy Model (CLAUDE.md): resolve credentials per-user first, env fallback as a\n// Sovereign-only onboarding default (OTD-PE-SOCIAL-APPCREDS), hard-fail otherwise \u2014 never a\n// silent shared key. BoK SSOT: docs/bok/post-engine/10-amendment-social-connect-*.md (FR-PE-005..009).\n//\n// Resolution order:\n//   (1) social_app_config per-user (is_active=true) \u2014 read via the service-role decrypted_* view.\n//   (2) env fallback \u2014 TIKTOK_CLIENT_KEY/SECRET \u00b7 GOOGLE_CLIENT_ID/SECRET \u00b7 PINTEREST_CLIENT_ID/SECRET.\n//   (3) SocialAppConfigError(402) {error:\"<platform>_not_configured\", action:\"Configure ... /dashboard/settings\"}.\n//\n// SECURITY: client_secret lives encrypted in Vault; only the service-role decrypted_social_app_config view\n// exposes plaintext. NEVER read the masked public view for the secret (it returns '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022').\n\nimport type { SupabaseClient } from \"https://esm.sh/@supabase/supabase-js@2\";\n\nexport type SocialAppPlatform = \"tiktok\" | \"youtube\" | \"pinterest\";\n\nexport interface SocialAppCreds {\n  clientId: string;\n  clientSecret: string;\n  scopes: string[] | null;\n  metadata: Record<string, unknown>;\n  source: \"per-user\" | \"env\";\n}\n\n// Values are env-var NAMES (looked up in Deno.env), NOT secret values. The `*Env` suffix keeps them\n// unambiguous to the secret-scan hook (a `secret: \"...\"` literal would false-positive).\nconst ENV_MAP: Record<SocialAppPlatform, { idEnv: string; secretEnv: string; label: string }> = {\n  tiktok: { idEnv: \"TIKTOK_CLIENT_KEY\", secretEnv: \"TIKTOK_CLIENT_SECRET\", label: \"TikTok\" },\n  youtube: { idEnv: \"GOOGLE_CLIENT_ID\", secretEnv: \"GOOGLE_CLIENT_SECRET\", label: \"YouTube\" },\n  pinterest: { idEnv: \"PINTEREST_CLIENT_ID\", secretEnv: \"PINTEREST_CLIENT_SECRET\", label: \"Pinterest\" },\n};",
  "new_string": "// Shared: OAuth APP credential resolution for the 6 social platforms.\n// API Tenancy Model (CLAUDE.md): resolve credentials per-user first, then the admin-managed GLOBAL\n// row, env only as a legacy/emergency fallback, hard-fail otherwise \u2014 never a silent shared key.\n// BoK SSOT: docs/bok/post-engine/10-amendment-social-connect-*.md (FR-PE-005..009) +\n// 16-amendment-global-app-credentials-admin-tier.md (FR-PE-017/018 \u2014 closes OTD-PE-SOCIAL-APPCREDS).\n//\n// Resolution order (UNBREAKABLE):\n//   (1) social_app_config per-user (user_id = caller, is_active) \u2014 tenant BYOK.\n//   (2) social_app_config GLOBAL  (user_id IS NULL,   is_active) \u2014 admin-managed via /dashboard/admin.\n//   (3) env fallback \u2014 legacy/emergency only (no longer the operational path).\n//   (4) SocialAppConfigError(402) {error:\"<platform>_not_configured\", action:\"Configure ...\"}.\n//\n// SECURITY: client_secret lives encrypted in Vault; only the service-role decrypted_social_app_config view\n// exposes plaintext. NEVER read the masked public view for the secret (it returns '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022').\n\nimport type { SupabaseClient } from \"https://esm.sh/@supabase/supabase-js@2\";\n\nexport type SocialAppPlatform =\n  | \"tiktok\"\n  | \"youtube\"\n  | \"pinterest\"\n  | \"linkedin\"\n  | \"instagram\"\n  | \"twitter\";\n\nexport interface SocialAppCreds {\n  clientId: string;\n  clientSecret: string;\n  scopes: string[] | null;\n  metadata: Record<string, unknown>;\n  source: \"per-user\" | \"global\" | \"env\";\n}\n\n// Values are env-var NAMES (looked up in Deno.env), NOT secret values. The `*Env` suffix keeps them\n// unambiguous to the secret-scan hook (a `secret: \"...\"` literal would false-positive).\n// Note: the \"facebook\" branch of the OAuth rails uses the instagram (Meta) app credentials.\nconst ENV_MAP: Record<SocialAppPlatform, { idEnv: string; secretEnv: string; label: string }> = {\n  tiktok: { idEnv: \"TIKTOK_CLIENT_KEY\", secretEnv: \"TIKTOK_CLIENT_SECRET\", label: \"TikTok\" },\n  youtube: { idEnv: \"GOOGLE_CLIENT_ID\", secretEnv: \"GOOGLE_CLIENT_SECRET\", label: \"YouTube\" },\n  pinterest: { idEnv: \"PINTEREST_CLIENT_ID\", secretEnv: \"PINTEREST_CLIENT_SECRET\", label: \"Pinterest\" },\n  linkedin: { idEnv: \"LINKEDIN_CLIENT_ID\", secretEnv: \"LINKEDIN_CLIENT_SECRET\", label: \"LinkedIn\" },\n  instagram: { idEnv: \"INSTAGRAM_APP_ID\", secretEnv: \"INSTAGRAM_APP_SECRET\", label: \"Instagram/Meta\" },\n  twitter: { idEnv: \"TWITTER_CLIENT_ID\", secretEnv: \"TWITTER_CLIENT_SECRET\", label: \"X (Twitter)\" },\n};"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/social-app-config.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:27:39)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/social-app-config.ts",
  "old_string": "  // (1) per-user\n  if (userId) {\n    const { data, error } = await supabase\n      .from(\"decrypted_social_app_config\")\n      .select(\"client_id, client_secret, scopes, metadata, is_active\")\n      .eq(\"user_id\", userId)\n      .eq(\"platform\", platform)\n      .eq(\"is_active\", true)\n      .maybeSingle();\n\n    if (!error && data && data.client_id && data.client_secret) {\n      return {\n        clientId: String(data.client_id),\n        clientSecret: String(data.client_secret),\n        scopes: (data.scopes as string[] | null) ?? null,\n        metadata: (data.metadata as Record<string, unknown>) ?? {},\n        source: \"per-user\",\n      };\n    }\n  }\n\n  // (2) env fallback (Sovereign-only onboarding default \u2014 OTD-PE-SOCIAL-APPCREDS)\n  const envId = Deno.env.get(env.idEnv);\n  const envSecret = Deno.env.get(env.secretEnv);\n  if (envId && envSecret) {\n    return { clientId: envId, clientSecret: envSecret, scopes: null, metadata: {}, source: \"env\" };\n  }\n\n  // (3) hard fail\n  throw new SocialAppConfigError(platform, env.label);",
  "new_string": "  // (1) per-user (tenant BYOK)\n  if (userId) {\n    const { data, error } = await supabase\n      .from(\"decrypted_social_app_config\")\n      .select(\"client_id, client_secret, scopes, metadata, is_active\")\n      .eq(\"user_id\", userId)\n      .eq(\"platform\", platform)\n      .eq(\"is_active\", true)\n      .maybeSingle();\n\n    if (!error && data && data.client_id && data.client_secret) {\n      return {\n        clientId: String(data.client_id),\n        clientSecret: String(data.client_secret),\n        scopes: (data.scopes as string[] | null) ?? null,\n        metadata: (data.metadata as Record<string, unknown>) ?? {},\n        source: \"per-user\",\n      };\n    }\n  }\n\n  // (2) GLOBAL row \u2014 admin-managed via /dashboard/admin (FR-PE-017/018)\n  {\n    const { data, error } = await supabase\n      .from(\"decrypted_social_app_config\")\n      .select(\"client_id, client_secret, scopes, metadata, is_active\")\n      .is(\"user_id\", null)\n      .eq(\"platform\", platform)\n      .eq(\"is_active\", true)\n      .maybeSingle();\n\n    if (!error && data && data.client_id && data.client_secret) {\n      return {\n        clientId: String(data.client_id),\n        clientSecret: String(data.client_secret),\n        scopes: (data.scopes as string[] | null) ?? null,\n        metadata: (data.metadata as Record<string, unknown>) ?? {},\n        source: \"global\",\n      };\n    }\n  }\n\n  // (3) env fallback (legacy/emergency \u2014 the admin tier is the operational global path)\n  const envId = Deno.env.get(env.idEnv);\n  const envSecret = Deno.env.get(env.secretEnv);\n  if (envId && envSecret) {\n    return { clientId: envId, clientSecret: envSecret, scopes: null, metadata: {}, source: \"env\" };\n  }\n\n  // (4) hard fail\n  throw new SocialAppConfigError(platform, env.label);"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/social-app-config.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:27:48)*


## 🤖 Claude *(21:27:48)*

Agora o `social-auth-init` — hoist do service client + migração dos 3 branches raw-env:

## 🤖 Claude *(21:28:13)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-init/index.ts",
  "old_string": "    const stateKey = (Deno.env.get(\"SB_SECRET_KEY\") ?? Deno.env.get(\"SUPABASE_SERVICE_ROLE_KEY\"))!;\n    const state = await signState({ userId, platform, redirect_uri, ts: Date.now() }, stateKey);\n\n    let authUrl: string;\n\n    if (platform === \"linkedin\") {\n      const clientId = Deno.env.get(\"LINKEDIN_CLIENT_ID\");\n      if (!clientId) {\n        return new Response(JSON.stringify({ error: \"LinkedIn not configured\" }), {\n          status: 500,\n          headers: { ...corsHeaders, \"Content-Type\": \"application/json\" },\n        });\n      }\n      const scopes = \"openid profile email w_member_social\";\n      authUrl = `${LINKEDIN_AUTH_URL}?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}`;\n\n    } else if (platform === \"instagram\" || platform === \"facebook\") {\n      const appId = Deno.env.get(\"INSTAGRAM_APP_ID\");\n      if (!appId) {\n        return new Response(JSON.stringify({ error: \"Instagram/Facebook not configured\" }), {\n          status: 500,\n          headers: { ...corsHeaders, \"Content-Type\": \"application/json\" },\n        });\n      }\n      const scopes = \"instagram_business_basic,instagram_business_content_publish,instagram_business_manage_comments,instagram_business_manage_messages\";\n      authUrl = `${INSTAGRAM_AUTH_URL}?client_id=${appId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}&response_type=code`;\n\n    } else if (platform === \"twitter\") {\n      const clientId = Deno.env.get(\"TWITTER_CLIENT_ID\");\n      if (!clientId) {\n        return new Response(JSON.stringify({ error: \"Twitter/X not configured\" }), {\n          status: 500,\n          headers: { ...corsHeaders, \"Content-Type\": \"application/json\" },\n        });\n      }\n      // Twitter OAuth 2.0 with PKCE\n      const codeChallenge = state.slice(0, 43); // simple challenge for demo; production should use S256\n      // media.write (FR-SPACES-084): image/video upload for tweets. Connections made BEFORE this scope was\n      // added lack it \u2014 publish-social fails those with an actionable \"reconecte a conta X\" error.\n      const scopes = \"tweet.read tweet.write users.read offline.access media.write\";\n      authUrl = `${TWITTER_AUTH_URL}?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}&code_challenge=${codeChallenge}&code_challenge_method=plain`;\n\n    } else if (platform === \"tiktok\") {\n      // App creds resolve per-user \u2192 env fallback \u2192 hard-fail (API Tenancy Model \u00b7 FR-PE-006).\n      // Service-role client reads the decrypted_social_app_config view (mirrors social-auth-callback).\n      const serviceClient = createClient(\n        Deno.env.get(\"SUPABASE_URL\")!,\n        (Deno.env.get(\"SB_SECRET_KEY\") ?? Deno.env.get(\"SUPABASE_SERVICE_ROLE_KEY\"))!,\n      );\n      let creds;\n      try {\n        creds = await resolveSocialAppCreds(serviceClient, userId, \"tiktok\");\n      } catch (err) {\n        const failClosed = socialAppConfigErrorResponse(err, corsHeaders);\n        if (failClosed) return failClosed;\n        throw err;\n      }",
  "new_string": "    const stateKey = (Deno.env.get(\"SB_SECRET_KEY\") ?? Deno.env.get(\"SUPABASE_SERVICE_ROLE_KEY\"))!;\n    const state = await signState({ userId, platform, redirect_uri, ts: Date.now() }, stateKey);\n\n    // App creds resolve per-user \u2192 GLOBAL admin row \u2192 env fallback \u2192 hard-fail 402 for ALL platforms\n    // (API Tenancy Model \u00b7 FR-PE-006/007/008 + FR-PE-018). Service-role client reads the\n    // decrypted_social_app_config view (mirrors social-auth-callback).\n    const serviceClient = createClient(\n      Deno.env.get(\"SUPABASE_URL\")!,\n      (Deno.env.get(\"SB_SECRET_KEY\") ?? Deno.env.get(\"SUPABASE_SERVICE_ROLE_KEY\"))!,\n    );\n\n    let authUrl: string;\n\n    if (platform === \"linkedin\") {\n      let creds;\n      try {\n        creds = await resolveSocialAppCreds(serviceClient, userId, \"linkedin\");\n      } catch (err) {\n        const failClosed = socialAppConfigErrorResponse(err, corsHeaders);\n        if (failClosed) return failClosed;\n        throw err;\n      }\n      const scopes = \"openid profile email w_member_social\";\n      authUrl = `${LINKEDIN_AUTH_URL}?response_type=code&client_id=${encodeURIComponent(creds.clientId)}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}`;\n\n    } else if (platform === \"instagram\" || platform === \"facebook\") {\n      // The \"facebook\" branch uses the instagram (Meta) app credentials \u2014 one Meta app serves both.\n      let creds;\n      try {\n        creds = await resolveSocialAppCreds(serviceClient, userId, \"instagram\");\n      } catch (err) {\n        const failClosed = socialAppConfigErrorResponse(err, corsHeaders);\n        if (failClosed) return failClosed;\n        throw err;\n      }\n      const scopes = \"instagram_business_basic,instagram_business_content_publish,instagram_business_manage_comments,instagram_business_manage_messages\";\n      authUrl = `${INSTAGRAM_AUTH_URL}?client_id=${encodeURIComponent(creds.clientId)}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}&response_type=code`;\n\n    } else if (platform === \"twitter\") {\n      let creds;\n      try {\n        creds = await resolveSocialAppCreds(serviceClient, userId, \"twitter\");\n      } catch (err) {\n        const failClosed = socialAppConfigErrorResponse(err, corsHeaders);\n        if (failClosed) return failClosed;\n        throw err;\n      }\n      // Twitter OAuth 2.0 with PKCE\n      const codeChallenge = state.slice(0, 43); // simple challenge for demo; production should use S256\n      // media.write (FR-SPACES-084): image/video upload for tweets. Connections made BEFORE this scope was\n      // added lack it \u2014 publish-social fails those with an actionable \"reconecte a conta X\" error.\n      const scopes = \"tweet.read tweet.write users.read offline.access media.write\";\n      authUrl = `${TWITTER_AUTH_URL}?response_type=code&client_id=${encodeURIComponent(creds.clientId)}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}&code_challenge=${codeChallenge}&code_challenge_method=plain`;\n\n    } else if (platform === \"tiktok\") {\n      let creds;\n      try {\n        creds = await resolveSocialAppCreds(serviceClient, userId, \"tiktok\");\n      } catch (err) {\n        const failClosed = socialAppConfigErrorResponse(err, corsHeaders);\n        if (failClosed) return failClosed;\n        throw err;\n      }"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-init/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:28:19)*


## 🤖 Claude *(21:28:22)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-init/index.ts",
  "old_string": "    } else if (platform === \"youtube\") {\n      // App creds resolve per-user \u2192 env fallback \u2192 hard-fail (API Tenancy Model \u00b7 FR-PE-007).\n      const serviceClient = createClient(\n        Deno.env.get(\"SUPABASE_URL\")!,\n        (Deno.env.get(\"SB_SECRET_KEY\") ?? Deno.env.get(\"SUPABASE_SERVICE_ROLE_KEY\"))!,\n      );\n      let creds;\n      try {\n        creds = await resolveSocialAppCreds(serviceClient, userId, \"youtube\");",
  "new_string": "    } else if (platform === \"youtube\") {\n      let creds;\n      try {\n        creds = await resolveSocialAppCreds(serviceClient, userId, \"youtube\");"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-init/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:28:26)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-init/index.ts",
  "old_string": "    } else if (platform === \"pinterest\") {\n      // App creds resolve per-user \u2192 env fallback \u2192 hard-fail (API Tenancy Model \u00b7 FR-PE-008).\n      const serviceClient = createClient(\n        Deno.env.get(\"SUPABASE_URL\")!,\n        (Deno.env.get(\"SB_SECRET_KEY\") ?? Deno.env.get(\"SUPABASE_SERVICE_ROLE_KEY\"))!,\n      );\n      let creds;\n      try {\n        creds = await resolveSocialAppCreds(serviceClient, userId, \"pinterest\");",
  "new_string": "    } else if (platform === \"pinterest\") {\n      let creds;\n      try {\n        creds = await resolveSocialAppCreds(serviceClient, userId, \"pinterest\");"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-init/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:28:31)*

Agora o `social-auth-callback` — os 3 branches de token exchange:

## 🤖 Claude *(21:28:37)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-callback/index.ts",
  "old_string": "    if (platform === \"linkedin\") {\n      const clientId = Deno.env.get(\"LINKEDIN_CLIENT_ID\")!;\n      const clientSecret = Deno.env.get(\"LINKEDIN_CLIENT_SECRET\")!;\n\n      const tokenRes = await fetch(\"https://www.linkedin.com/oauth/v2/accessToken\", {\n        method: \"POST\",\n        headers: { \"Content-Type\": \"application/x-www-form-urlencoded\" },\n        body: new URLSearchParams({\n          grant_type: \"authorization_code\",\n          code,\n          redirect_uri: callbackUrl,\n          client_id: clientId,\n          client_secret: clientSecret,\n        }),\n      });",
  "new_string": "    if (platform === \"linkedin\") {\n      // App credentials resolve per-user \u2192 GLOBAL admin row \u2192 env fallback \u2192 hard-fail (FR-PE-018).\n      const creds = await resolveSocialAppCreds(supabase, userId, \"linkedin\");\n\n      const tokenRes = await fetch(\"https://www.linkedin.com/oauth/v2/accessToken\", {\n        method: \"POST\",\n        headers: { \"Content-Type\": \"application/x-www-form-urlencoded\" },\n        body: new URLSearchParams({\n          grant_type: \"authorization_code\",\n          code,\n          redirect_uri: callbackUrl,\n          client_id: creds.clientId,\n          client_secret: creds.clientSecret,\n        }),\n      });"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-callback/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:28:45)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-callback/index.ts",
  "old_string": "    } else if (platform === \"instagram\" || platform === \"facebook\") {\n      const appId = Deno.env.get(\"INSTAGRAM_APP_ID\")!;\n      const appSecret = Deno.env.get(\"INSTAGRAM_APP_SECRET\")!;\n\n      // Instagram Login \u2014 short-lived token\n      const tokenRes = await fetch(\"https://api.instagram.com/oauth/access_token\", {\n        method: \"POST\",\n        headers: { \"Content-Type\": \"application/x-www-form-urlencoded\" },\n        body: new URLSearchParams({\n          client_id: appId,\n          client_secret: appSecret,\n          grant_type: \"authorization_code\",\n          redirect_uri: callbackUrl,\n          code,\n        }),\n      });\n      const tokenData = await tokenRes.json();\n      if (!tokenRes.ok || tokenData.error_type) throw new Error(tokenData.error_message || \"Instagram token exchange failed\");\n\n      const shortToken = tokenData.access_token;\n      platformUserId = String(tokenData.user_id);\n\n      // Exchange for long-lived token (60 days)\n      const longRes = await fetch(\n        `https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=${appSecret}&access_token=${shortToken}`\n      );",
  "new_string": "    } else if (platform === \"instagram\" || platform === \"facebook\") {\n      // \"facebook\" uses the instagram (Meta) app credentials \u2014 one Meta app serves both (FR-PE-018).\n      const creds = await resolveSocialAppCreds(supabase, userId, \"instagram\");\n\n      // Instagram Login \u2014 short-lived token\n      const tokenRes = await fetch(\"https://api.instagram.com/oauth/access_token\", {\n        method: \"POST\",\n        headers: { \"Content-Type\": \"application/x-www-form-urlencoded\" },\n        body: new URLSearchParams({\n          client_id: creds.clientId,\n          client_secret: creds.clientSecret,\n          grant_type: \"authorization_code\",\n          redirect_uri: callbackUrl,\n          code,\n        }),\n      });\n      const tokenData = await tokenRes.json();\n      if (!tokenRes.ok || tokenData.error_type) throw new Error(tokenData.error_message || \"Instagram token exchange failed\");\n\n      const shortToken = tokenData.access_token;\n      platformUserId = String(tokenData.user_id);\n\n      // Exchange for long-lived token (60 days)\n      const longRes = await fetch(\n        `https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=${encodeURIComponent(creds.clientSecret)}&access_token=${encodeURIComponent(shortToken)}`\n      );"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-callback/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:28:49)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-callback/index.ts",
  "old_string": "    } else if (platform === \"twitter\") {\n      const clientId = Deno.env.get(\"TWITTER_CLIENT_ID\")!;\n      const clientSecret = Deno.env.get(\"TWITTER_CLIENT_SECRET\")!;\n\n      // PKCE code verifier = the state used as plain challenge\n      const codeVerifier = stateStr.slice(0, 43);\n\n      const tokenRes = await fetch(\"https://api.x.com/2/oauth2/token\", {\n        method: \"POST\",\n        headers: {\n          \"Content-Type\": \"application/x-www-form-urlencoded\",\n          Authorization: `Basic ${btoa(`${clientId}:${clientSecret}`)}`,\n        },",
  "new_string": "    } else if (platform === \"twitter\") {\n      // App credentials resolve per-user \u2192 GLOBAL admin row \u2192 env fallback \u2192 hard-fail (FR-PE-018).\n      const creds = await resolveSocialAppCreds(supabase, userId, \"twitter\");\n\n      // PKCE code verifier = the state used as plain challenge\n      const codeVerifier = stateStr.slice(0, 43);\n\n      const tokenRes = await fetch(\"https://api.x.com/2/oauth2/token\", {\n        method: \"POST\",\n        headers: {\n          \"Content-Type\": \"application/x-www-form-urlencoded\",\n          Authorization: `Basic ${btoa(`${creds.clientId}:${creds.clientSecret}`)}`,\n        },"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/social-auth-callback/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:28:59)*


## 🤖 Claude *(21:28:59)*

Agora o `refresh-social-token` — os 3 branches + import:

## 🤖 Claude *(21:29:00)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '1,75p' supabase/functions/refresh-social-token/index.ts; echo \"---TAIL---\"; sed -n '280,310p' supabase/functions/refresh-social-token/index.ts",
  "description": "Ler cabe\u00e7alho e tail do refresh-social-token (imports, client, error handling)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> import {
>   resolveSocialAppCreds,
>   SocialAppConfigError,
>   socialAppConfigErrorResponse,
> } from "../_shared/social-app-config.ts";
> 
> const corsHeaders = {
>   "Access-Control-Allow-Origin": "*",
>   "Access-Control-Allow-Methods": "POST, OPTIONS",
>   "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-user-token",
> };
> 
> Deno.serve(async (req) => {
>   if (req.method === "OPTIONS") {
>     return new Response("ok", { headers: corsHeaders });
>   }
> 
>   try {
>     const authHeader = req.headers.get("Authorization");
>     if (!authHeader?.startsWith("Bearer ")) {
>       return new Response(JSON.stringify({ error: "Missing authorization" }), {
>         status: 401,
>         headers: { ...corsHeaders, "Content-Type": "application/json" },
>       });
>     }
> 
>     const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
>     const supabaseAnonKey = (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!;
>     const serviceRoleKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
>     const admin = createClient(supabaseUrl, serviceRoleKey);
> 
>     // Best-effort telemetry — mirrors publish-meta's `pulse`. Materiality (Lei 1): a 2xx is not success;
>     // every refresh path (healthy/degraded) emits to infra_health_logs so the Neural HUD sees the token cycle.
>     const pulse = (service: string, status: "healthy" | "degraded") =>
>       admin.from("infra_health_logs").insert({ service, status }).then(() => {}, () => {});
> 
>     // Resolve caller: user JWT → user.id available; service role JWT → user is null (internal call)
>     // Supabase infrastructure already validated the JWT signature before reaching this code.
>     const userClient = createClient(supabaseUrl, supabaseAnonKey, {
>       global: { headers: { Authorization: authHeader } },
>     });
>     const { data: { user } } = await userClient.auth.getUser();
>     const isServiceRole = authHeader === `Bearer ${serviceRoleKey}`;
>     const isInternalServiceCall = isServiceRole;
> 
>     const { social_account_id } = await req.json();
>     if (typeof social_account_id !== "string" || !social_account_id.trim()) {
>       return new Response(JSON.stringify({ error: "social_account_id required" }), {
>         status: 400,
>         headers: { ...corsHeaders, "Content-Type": "application/json" },
>       });
>     }
> 
>     const { data: account, error } = await admin
>       .from("decrypted_social_accounts")
>       .select("*")
>       .eq("id", social_account_id)
>       .single();
> 
>     if (error || !account) {
>       return new Response(JSON.stringify({ error: "Account not found" }), {
>         status: 404,
>         headers: { ...corsHeaders, "Content-Type": "application/json" },
>       });
>     }
> 
>     // Ownership check
>     if (!isInternalServiceCall && (!user || account.user_id !== user.id)) {
>       return new Response(JSON.stringify({ error: "Forbidden" }), {
>         status: 403,
>         headers: { ...corsHeaders, "Content-Type": "application/json" },
>       });
>     }
> 
> ---TAIL---
>     try {
>       createClient(
>         Deno.env.get("SUPABASE_URL")!,
>         (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
>       )
>         .from("infra_health_logs")
>         .insert({ service: "refresh-social-token", status: "degraded" })
>         .then(() => {}, () => {});
>     } catch (_telemetryErr) {
>       // never let telemetry mask the original error
>     }
>     // FAIL-CLOSED (FR-PE-005/010): unresolved app credentials → structured 402 JSON the client can act on;
>     // never fall through to a shared/default key. Mirrors social-auth-callback's SocialAppConfigError handling.
>     if (err instanceof SocialAppConfigError) {
>       const configResponse = socialAppConfigErrorResponse(err, corsHeaders);
>       if (configResponse) return configResponse;
>     }
>     return new Response(JSON.stringify({ error: "Token refresh failed" }), {
>       status: 500,
>       headers: { ...corsHeaders, "Content-Type": "application/json" },
>     });
>   }
> });
> ```

## 🤖 Claude *(21:29:07)*


## 🤖 Claude *(21:29:12)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/refresh-social-token/index.ts",
  "old_string": "      const res = await fetch(\"https://www.linkedin.com/oauth/v2/accessToken\", {\n        method: \"POST\",\n        headers: { \"Content-Type\": \"application/x-www-form-urlencoded\" },\n        body: new URLSearchParams({\n          grant_type: \"refresh_token\",\n          refresh_token: account.refresh_token,\n          client_id: Deno.env.get(\"LINKEDIN_CLIENT_ID\")!,\n          client_secret: Deno.env.get(\"LINKEDIN_CLIENT_SECRET\")!,\n        }),\n      });",
  "new_string": "      // App creds: per-user \u2192 GLOBAL admin row \u2192 env fallback \u2192 402 (FR-PE-018).\n      const creds = await resolveSocialAppCreds(admin, account.user_id, \"linkedin\");\n      const res = await fetch(\"https://www.linkedin.com/oauth/v2/accessToken\", {\n        method: \"POST\",\n        headers: { \"Content-Type\": \"application/x-www-form-urlencoded\" },\n        body: new URLSearchParams({\n          grant_type: \"refresh_token\",\n          refresh_token: account.refresh_token,\n          client_id: creds.clientId,\n          client_secret: creds.clientSecret,\n        }),\n      });"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/refresh-social-token/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:29:16)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/refresh-social-token/index.ts",
  "old_string": "    } else if (account.platform === \"instagram\" || account.platform === \"facebook\") {\n      const res = await fetch(\n        `https://graph.facebook.com/v19.0/oauth/access_token?grant_type=fb_exchange_token&client_id=${Deno.env.get(\"INSTAGRAM_APP_ID\")}&client_secret=${Deno.env.get(\"INSTAGRAM_APP_SECRET\")}&fb_exchange_token=${account.access_token}`\n      );",
  "new_string": "    } else if (account.platform === \"instagram\" || account.platform === \"facebook\") {\n      // \"facebook\" uses the instagram (Meta) app credentials \u2014 one Meta app serves both (FR-PE-018).\n      const creds = await resolveSocialAppCreds(admin, account.user_id, \"instagram\");\n      const params = new URLSearchParams({\n        grant_type: \"fb_exchange_token\",\n        client_id: creds.clientId,\n        client_secret: creds.clientSecret,\n        fb_exchange_token: account.access_token,\n      });\n      const res = await fetch(`https://graph.facebook.com/v19.0/oauth/access_token?${params.toString()}`);"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/refresh-social-token/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:29:20)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/refresh-social-token/index.ts",
  "old_string": "      const clientId = Deno.env.get(\"TWITTER_CLIENT_ID\")!;\n      const clientSecret = Deno.env.get(\"TWITTER_CLIENT_SECRET\")!;\n      const res = await fetch(\"https://api.x.com/2/oauth2/token\", {\n        method: \"POST\",\n        headers: {\n          \"Content-Type\": \"application/x-www-form-urlencoded\",\n          Authorization: `Basic ${btoa(`${clientId}:${clientSecret}`)}`,\n        },",
  "new_string": "      // App creds: per-user \u2192 GLOBAL admin row \u2192 env fallback \u2192 402 (FR-PE-018).\n      const creds = await resolveSocialAppCreds(admin, account.user_id, \"twitter\");\n      const res = await fetch(\"https://api.x.com/2/oauth2/token\", {\n        method: \"POST\",\n        headers: {\n          \"Content-Type\": \"application/x-www-form-urlencoded\",\n          Authorization: `Basic ${btoa(`${creds.clientId}:${creds.clientSecret}`)}`,\n        },"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/refresh-social-token/index.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:29:28)*


## 🤖 Claude *(21:29:28)*

Agora o `tiktok-login-creds.ts` (FR-PE-021 — global-first):

## 🤖 Claude *(21:29:43)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/tiktok-login-creds.ts",
  "old_string": "// Resolution order: (1) system env override (a dedicated global cred, if ever set) \u2192 (2) the single active tiktok\n// row in decrypted_social_app_config (single-tenant Usu\u00e1rio Zero: that row IS the app owner's = the same key as the\n// connect). Reads via the SAME service-role view (decrypted_social_app_config) the connect's resolveSocialAppCreds\n// already uses \u2014 no new credential surface.\n//\n// \u26a0\ufe0f Multi-tenant note: when the product goes multi-tenant, \"the single active tiktok config\" is no longer the app\n//    owner unambiguously \u2014 a dedicated global cred (env or an app_owner-scoped row) must be used. Tracked for that day.\nimport type { SupabaseClient } from \"https://esm.sh/@supabase/supabase-js@2\";\n\nexport interface TikTokAppCreds {\n  clientKey: string;\n  clientSecret: string;\n  source: \"env\" | \"social_app_config\";\n}\n\nexport async function resolveTikTokLoginCreds(admin: SupabaseClient): Promise<TikTokAppCreds | null> {\n  const envKey = Deno.env.get(\"TIKTOK_CLIENT_KEY\");\n  const envSecret = Deno.env.get(\"TIKTOK_CLIENT_SECRET\");\n  if (envKey && envSecret) return { clientKey: envKey, clientSecret: envSecret, source: \"env\" };\n\n  const { data } = await admin\n    .from(\"decrypted_social_app_config\")\n    .select(\"client_id, client_secret\")\n    .eq(\"platform\", \"tiktok\")\n    .eq(\"is_active\", true)\n    .limit(1)\n    .maybeSingle();\n  if (data?.client_id && data?.client_secret) {\n    return { clientKey: String(data.client_id), clientSecret: String(data.client_secret), source: \"social_app_config\" };\n  }\n  return null;\n}",
  "new_string": "// Resolution order (FR-PE-021 \u2014 Amendment 16 aligns login to the admin-managed GLOBAL tier):\n//   (1) the GLOBAL tiktok row (user_id IS NULL) in decrypted_social_app_config \u2014 the unambiguous\n//       app-owner credential, managed by admins at /dashboard/admin (multi-tenant-safe);\n//   (2) system env override (TIKTOK_CLIENT_KEY/SECRET) \u2014 legacy/emergency;\n//   (3) the single active per-user tiktok row \u2014 single-tenant Usu\u00e1rio Zero compat (that row IS the\n//       app owner's key), kept so login keeps working until the global row is seeded.\n// Reads via the SAME service-role view (decrypted_social_app_config) resolveSocialAppCreds uses.\nimport type { SupabaseClient } from \"https://esm.sh/@supabase/supabase-js@2\";\n\nexport interface TikTokAppCreds {\n  clientKey: string;\n  clientSecret: string;\n  source: \"global\" | \"env\" | \"social_app_config\";\n}\n\nexport async function resolveTikTokLoginCreds(admin: SupabaseClient): Promise<TikTokAppCreds | null> {\n  // (1) GLOBAL admin-managed row (user_id IS NULL)\n  const { data: globalRow } = await admin\n    .from(\"decrypted_social_app_config\")\n    .select(\"client_id, client_secret\")\n    .is(\"user_id\", null)\n    .eq(\"platform\", \"tiktok\")\n    .eq(\"is_active\", true)\n    .maybeSingle();\n  if (globalRow?.client_id && globalRow?.client_secret) {\n    return { clientKey: String(globalRow.client_id), clientSecret: String(globalRow.client_secret), source: \"global\" };\n  }\n\n  // (2) env override (legacy/emergency)\n  const envKey = Deno.env.get(\"TIKTOK_CLIENT_KEY\");\n  const envSecret = Deno.env.get(\"TIKTOK_CLIENT_SECRET\");\n  if (envKey && envSecret) return { clientKey: envKey, clientSecret: envSecret, source: \"env\" };\n\n  // (3) single-tenant compat: the single active per-user row (Usu\u00e1rio Zero = app owner)\n  const { data } = await admin\n    .from(\"decrypted_social_app_config\")\n    .select(\"client_id, client_secret\")\n    .not(\"user_id\", \"is\", null)\n    .eq(\"platform\", \"tiktok\")\n    .eq(\"is_active\", true)\n    .limit(1)\n    .maybeSingle();\n  if (data?.client_id && data?.client_secret) {\n    return { clientKey: String(data.client_id), clientSecret: String(data.client_secret), source: \"social_app_config\" };\n  }\n  return null;\n}"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/tiktok-login-creds.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:29:55)*


## 🤖 Claude *(21:29:55)*


## 🤖 Claude *(21:29:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "export PATH=\"$HOME/.deno/bin:$PATH\"\nwhich deno || ls ~/.deno/bin 2>/dev/null || echo \"no deno\"\ncd supabase/functions 2>/dev/null && for f in social-auth-init social-auth-callback refresh-social-token; do\n  deno check --no-lock \"$f/index.ts\" 2>&1 | tail -2\ndone",
  "description": "deno check nos 3 edge fns tocados"
}
```

## 🤖 Claude *(21:29:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== G5: raw env reads remanescentes (esperado: s\u00f3 ENV_MAP + webhooks Meta) ===\"; grep -rn \"LINKEDIN_CLIENT\\|TWITTER_CLIENT\\|INSTAGRAM_APP\\|TIKTOK_CLIENT\\|PINTEREST_CLIENT\\|GOOGLE_CLIENT\" supabase/functions/ --include=\"*.ts\" | grep -v \"_shared/social-app-config.ts\" | grep -v \"_shared/tiktok-login-creds.ts\"",
  "description": "Gate G5 \u2014 nenhuma leitura crua de app creds fora dos resolvers"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/ubuntu/.deno/bin/deno
> [0m[32mCheck[0m social-auth-init/index.ts
> [0m[32mCheck[0m social-auth-callback/index.ts
> [0m[32mCheck[0m refresh-social-token/index.ts
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === G5: raw env reads remanescentes (esperado: só ENV_MAP + webhooks Meta) ===
> ugrep: warning: supabase/functions/: No such file or directory
> ```

## 🤖 Claude *(21:30:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra && grep -rn -E \"LINKEDIN_CLIENT|TWITTER_CLIENT|INSTAGRAM_APP|TIKTOK_CLIENT|PINTEREST_CLIENT|GOOGLE_CLIENT\" supabase/functions/ --include=\"*.ts\" | grep -v \"_shared/social-app-config.ts\" | grep -v \"_shared/tiktok-login-creds.ts\"",
  "description": "Gate G5 \u2014 leituras cruas fora dos resolvers (cwd correto)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> supabase/functions/whatsapp-webhook/index.ts:89:      const appSecret = Deno.env.get("META_APP_SECRET") || Deno.env.get("INSTAGRAM_APP_SECRET") || "";
> supabase/functions/instagram-webhook/index.ts:32:    const appSecret = Deno.env.get("INSTAGRAM_APP_SECRET") ?? Deno.env.get("META_APP_SECRET");
> supabase/functions/tiktok-login-init/index.ts:3:// come from SYSTEM env TIKTOK_CLIENT_KEY (the restricted env-fallback of the API Tenancy Model — onboarding/no-user
> ```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-16 - Configurar loop e blueprint do video-repurposeyoutube-studio]]
> * **Próxima Sessão**: [[2026-07-16 - Roadmap de automação de conteúdo com IA e Claude Code]]
%% --- TIMELINE END --- %%

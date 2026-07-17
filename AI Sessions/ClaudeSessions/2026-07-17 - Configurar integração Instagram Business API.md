# Configurar integração Instagram Business API
**Date:** 2026-07-17 | **Session ID:** `449491e4-31e9-493d-bad8-6249c3c0ed4d`

---

## 👤 User *(21:13:56)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(21:13:56)*

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


## 🤖 Claude *(21:14:00)*

<details>
<summary>💭 Thinking Process</summary>

I'm running the ShakeHands handson protocol by executing pre-flight bash commands and reading the necessary files in parallel.

</details>


## 🤖 Claude *(21:14:00)*

Vou executar o ritual ShakeHands /handson. Começando pelo pre-flight — todos os comandos em paralelo.

## 🤖 Claude *(21:14:01)*


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
> 3400742 docs(handoff): seal credenciais globais de app + AI Act Fatia 0-1 + content-intel BoK 9/9 (malha 9133)
> 68e405e docs(readme): v6.106.0 — credenciais globais de app + AI Act Fatia 0-1 + content-intel BoK 9/9 (malha 9133)
> 91f1222 docs(bok): content-intel 9/9 selada — análise de vídeo existente → estratégia (módulo novo)
> 42ca370 fix(publish): guard de megapixels no reframe (WORKER_RESOURCE_LIMIT) + blueprint content-intel
> 9214df7 feat(pinterest): UI de gestão de boards no /dashboard/social (demo Standard access)
> f462173 feat(landing-factory): wildcard *.gcrux.com VIVO — hosting de LPs provado E2E
> 7226717 fix(provenance): external/local excluídos do auto-marking + checklist app-audit IG/TikTok
> ```

## 🤖 Claude *(21:14:01)*


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

## 🤖 Claude *(21:14:02)*


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

## 🤖 Claude *(21:14:03)*


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

## 🤖 Claude *(21:14:05)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"",
  "description": "Docker mesh health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 2 days (healthy)
> mcorch_claude_mem: Up 4 weeks (healthy)
> mcorch_chroma: Up 4 weeks (healthy)
> ---
> mega-brain-dashboard: Up 4 weeks
> mega-brain-webhook: Up 4 weeks (healthy)
> mega-brain-daemon: Up 4 weeks (healthy)
> ```

## 🤖 Claude *(21:14:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "curl -s http://localhost:8001/api/v2/heartbeat",
  "description": "Chroma API v2 heartbeat"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {"nanosecond heartbeat":1784322846041471557}
> ```

## 🤖 Claude *(21:14:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/ 2>/dev/null; echo \"---\"; wc -l HANDOFF.md; echo \"---\"; ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean\"",
  "description": "BoK suites, HANDOFF size, scratch check"
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
> ---
> 10239 HANDOFF.md
> ---
> scratch has files
> ```

## 🤖 Claude *(21:14:12)*

<details>
<summary>💭 Thinking Process</summary>

TypeScript validation passed, so now I'm reviewing the key project files—starting with the beginning and end sections of HANDOFF.md since it's quite long, then checking sprint-priorities.md and the scratch directory contents.

</details>


## 🤖 Claude *(21:14:12)*

Pre-flight capturado. TSC limpo. Agora leituras em paralelo — HANDOFF (início + cauda), sprint-priorities e scratch.

## 🤖 Claude *(21:14:12)*


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
> 14	| **Credenciais globais de app (admin) + AI Act Fatia 0-1 VIVO + content-intel BoK 9/9 + wildcard gcrux.com (2026-07-17)** | ✅ Sessão-maratona interativa (Sovereign ao vivo colando chaves, gravando vídeos de app-review, otimizando YouTube). **12 commits `b5c5474..91f1222`.** **(1) Tier global de credenciais de app OAuth** (post-engine Amendment 16, FR-PE-017..021): o Sovereign cola as chaves secretas de app direto no `/dashboard/admin` → aba **Chaves** (sem `.env`/CLI) — linha `user_id IS NULL` cifrada no Vault, admin-gated 2× (RLS `has_role` single-arg + exemption no INSTEAD OF guard); resolver vira **4 degraus** (per-user → global → env → 402) cobrindo as 6 plataformas (LinkedIn/IG/X saem do `Deno.env` cru nos 3 estágios). Edge fn `seed-global-app-creds` seed env→global 6/6. Banner de rotação (`admin_reminders`). `/security-review` NO FINDINGS · smoke 13/13 (cross-tenant BLOCKED ao vivo: 42501/Vault-UUID/23505). **Anticorpo per-user-shadow:** linha per-user stale sombreava a global no callback Pinterest (Sovereign redefiniu o secret no console → 401 do próprio Pinterest); sonda discriminante por code-falso; fix = desativar per-user. **Pinterest `@uxandai` + X `@gabrielOrchAI` reconectados** via credencial global (OTD-PE-SOCIAL-APPCREDS fechada) + **UI de gestão de boards** no `/dashboard/social` (`pinterest-boards` edge fn) para a demo do Standard. **(2) AI Act Art.50 Fatia 0-1 VIVO** (content-provenance): migration `20260716230000` (5 colunas `provenance_*` na spine + `register_creative_asset` 21→26 args, DROP+CREATE+re-GRANT service_role, `/security-review` NO FINDINGS, bug de preserve pego pelo reviewer + corrigido/provado) + `src/lib/provenance.ts` (enum IPTC) + motor `embed-iptc-core` (ExifTool `XMP-iptcExt:DigitalSourceType`, verify-before-claim) + worker `provenance-bridge` (systemd habilitado) → **backfill 101 assets MCORCH marcados** (witness real `bc03a65a` imagem + `d57e3341` vídeo baixados do bucket carregam a URI IPTC); external/local excluídos (Lei 1). Smoke 6/6. **(3) `*.gcrux.com` wildcard VIVO** — DNS wildcard (Sovereign) + `nginx/lp.gcrux.com.conf` (symlink+reload) → `hello.gcrux.com` serve landing real HTTP 200; trilho de hosting da landing-factory operacional. **(4) content-intel BoK 9/9 selada** (módulo NOVO): usuário compartilha link de vídeo existente (IG/TikTok/YT) → resolve+analisa server-side via Vision MCP → modela estratégia. Blueprint deepsearch 5 frentes (`wf_609b48ad`) → BoK Scribe 9/9 (`wf_658b10a1`, fix stage morreu no session-limit → **resumeFromRunId** recuperou); FR-CI-001..026 · OTD-CI-001..008 · FM-CI-01..20 · Pattern Conformance **21 padrões** (12y/3d/6na); seal `2e918a8c` DERIVES_FROM vision-mcp. **(5) Fixes:** morning-briefing tratava `security` (ciso-4-artifact) como BoK 0/9 falso + pin do repo canônico (`3d5a2f4`); `WORKER_RESOURCE_LIMIT` no reframe (guard de megapixels pré-decode, `42ca370`). tsc 0 · vitest **621** verde · gitleaks clean · milestone `9aa1b522` embedado (768d) · malha **9133**. ⚠️ Pendente Sovereign: Pinterest Trial→Standard (vídeo enviado) + Meta redirect URI; revisar legendas pt-BR do EP01 (master do dub); rotação de credenciais (SA Vertex/Gemini/Telegram — banner criado); código do `content-intel` (GO + jurídico); OTD-CI-002 (sondar IG/TikTok resolver); OTD-PSW-001 (GPU, adiado até créditos Vertex acabarem). |
> 15	| **Loop MAPE-K: UX-Explorer + landing-bundler + BoKs 9/9 retroativas + swarm:read PAT (2026-07-16)** | ✅ Loop GO'd pelo Sovereign ("pode armar o loop para atacar os próximos passos") + pedido paralelo de auditoria de prontidão BoK 9/9. Drenou it.0→it.4 da diretiva. **(it.0) UX-Explorer enxerga pela 1ª vez da vida** — o auditor nightly nunca tivera run verde (exit 4 maiden + exit 3 ×9 dias); o "auth expirado" era FALSO diagnóstico em cadeia de **4 causas**: PATH do cron sem `agent-browser` (spawn ENOENT), regex do runner casando `/auth` da URL, `wait networkidle` sem `--load` (CLI tratava como seletor → timeout 30s), cron sem `--state` (tour DESLOGADO). Fix + auth state via magiclink (PROC-E2E-006) → cron simulado 6/7 verdes + **1º finding P1 REAL da história** (Vision QA: Controls do ReactFlow brancos sobre o void → `INC-8cba901a` RESOLVIDO `7a00511`: vars `--xy-*` MIV, override de classe perde pro chunk lazy; Vision re-run APROVADO). 2 incidentes fechados, fila zerada. **(it.1) landing-bundler core (`762c641`)** — o P0 da landing-factory: SOP Lei 2 ANTES do código → `scripts/landing-bundler/{bundle-core,public-url,cli}.ts` (magic-bytes mandam · CSS recursivo `@font-face` · fail-open por ref/fail-closed estrutural · guard anti-SSRF host re-valida cada 3xx · seam `injectHead` FR-LF-003); **15/15 unit** (G1 SSRF-302 sem emissão interna · G3 CF-challenge · G4 idempotência) + **G5 run real** 331B→150.802B, data:image+data:font REAIS (Google Fonts recursivo), 0 refs externas. **(it.2) witness cadência 7/7 (`885fa77`)** — dispatch real `cadence_dispatches`→`scheduled_posts` queued linkados, re-arm UTC, idempotência, tenant-bind, cleanup 0 resíduo (fecha ressalva do seal `c994c363`; smoke que o SOP nomeava agora existe). **(it.3) BoKs 9/9 retroativas — 32/32 famílias (`a8265eb`+`0718101`)** — método audit-first (`wf_2998d4c7`, 4 agentes, 18 drifts verificados adversarialmente, ground truth em `.claude/context/bok-readiness-audit-2026-07-16.json`) → micro-reparos `a729f83` (mesh mandate youtube-data + gate Gemini-only detector) → 6 writers + 2 critics (`wf_182e0145`; video-repurpose APPROVE 0 violations · youtube-studio 2 violations corrigidas) → verificação mecânica independente. YTS = **guarda-chuva 2 tracks** (GO Sovereign AskUserQuestion): Track A painel SHIPADO + Track B fábrica ROADMAP; estado vivo DATADO (gate Y3 satisfeito, rows=[[61]]). Seals malha `a6df1548`/`9a923887`. **(it.4) swarm:read no PAT allowlist (`1b30fc3`)** — predictive-swarm Fatia 2 sub-fatia; migration `20260716190000` estende o CHECK de vocabulário fechado (fail-closed: scope só entra com tool vivo); `/security-review` NO FINDINGS. **Task idempotência (`76e5a8a`)** — `mcorch_nodes.name` SEM UNIQUE → 24 seed scripts migrados p/ CHECK-BEFORE-INSERT (23/23 re-executados, malha estável). **11 commits** `50bd550..1b30fc3` · tsc 0 · vitest **601** verde · gitleaks clean · milestone `3a23fe00` embedado (768d) · malha **9127**. ⚠️ Pendente Sovereign: aplicar migration `swarm:read` em prod; predictive-swarm Fatia 2-resto (OTD-PSW-001 GPU decision); rotação de credenciais (SA Vertex/Gemini/Telegram); registrar `gcrux.com`+wildcard; 3 chaves Gmail; reconexão X + app-audit IG/TikTok. |
> 16	| **landing-factory BoK 9/9 + fix imagem quebrada + fix egress (2026-07-16)** | ✅ Sessão-maratona interativa (2 vídeos Maestros da IA → operação de marketing agêntica no Spaces; motor de conteúdo de 2 máquinas). **(1) landing-factory** — fábrica de landing pages AUTO-OTIMIZÁVEIS (loop CRO governado), beachhead do norte agência-dentro-da-plataforma; deepsearch verify-adversarial (`wf_1f7d1113`→`wf_b8cb767d`) → blueprint v0.2 (superset gate PASS) → **BoK Scribe 9/9** (`wf_d540ceb4`; MR14→BR18→PR18→FR20+NFR10+OTD15+FM14; **Pattern Conformance 15/5/1**; seal `b65e94b1` DERIVES_FROM constellation, embedado). Decisões Owner: Open Design **v0.10.0 pinado** (export single-file NÃO existe upstream — issue #368, `inline-assets.ts` byte-idêntico v0.10→main) → **asset-bundler próprio** (`landing-bundler` host worker) é o P0 da Fatia 1; hosting em **`gcrux.com`** (domínio registrável SEPARADO cookie-isolado, `<slug>.gcrux.com`; NUNCA `*.mcorch.com` — cookie SSO `sb-mcorch-session` `.mcorch.com`-scoped + access token + não-`HttpOnly` [`sso-cookie.ts:13,44`] = account takeover, FM-LF-013 RPN280) + Netlify/Vercel BYOK; WordPress-page-first; PostHog self-host/BYOK (gate humano→autônomo). **Gate Closed-Loop ABERTO** pro código. **(2) fix imagem quebrada** — inspetores Gerar Imagem/Vídeo re-assinam bucket privado (`useDisplayUrl`/`StorageVideo`, superfície faltante do Fix Assets; objeto do nó `n_8rsn4w3l` 400→200 image/png 1,1MB). **(3) fix egress** — signed URL reusável 24h (cache localStorage por uid, clear no logout) vs re-assinar a cada render → corta o cache-buster; `/security-review` NO FINDINGS · 13/13 testes. **(4) roadmap** artefato 2-máquinas salvo como asset do User 0. **6 commits** `9ccfeb7..10444b7` · tsc 0 · suíte **586** verde · gitleaks clean · milestone `56670e5c` · malha **9122**. ⚠️ Pendente: código do `landing-bundler` (Fatia 1); registrar wildcard `*.gcrux.com`; OTD-LF-001/003/014 + gate CRO 95%; provisionar 3 chaves Gmail (fila anterior); auditoria de agentes OpenClaw (free-first). |
> 17	| **Loop autônomo: Cadência + Enxame Fatia 1 em PROD + AI Act BoK (2026-07-15)** | ✅ Loop GO'd pelo Sovereign (migration+deploy autorizados) drenou os 4 itens da Fila. **(1) Veo via Vertex PROVADO REAL** — role Vertex AI User concedida → witness pago (gen `2659d78b`, `engine=veo-vertex`, 267 mco exatos 4263→3996, identidade preservada Read+Vision MCP; nó `4e8902d2`) + UI multi-key Vertex (preview do SA JSON, `8772f0d`). **(2) Cadência Fatia 1 SHIPPADA** (`spaces-cadence`, FR-CAD-001..011): motor de recorrência que ESTENDE `autopilot_plans` (plan_kind/recurrence/program/quiet_hours/…) + tabela `cadence_dispatches` (RLS default-deny + índice único parcial de idempotência) + roteia o tick vivo por `plan_kind` (**ZERO pg_cron novo**); `cadence-plan`/`cadence-run` (verify_jwt=false Bearer SB_SECRET_KEY, user_id da linha, drain FOR UPDATE SKIP LOCKED, dispatch→scheduled_posts) + node `kind:cadence`; migration `20260716120000` **aplicada+verificada** · `/security-review` NO FINDINGS · smoke 7/7 · nó `c994c363`. **(3) Enxame Sensorial Fatia 1 SHIPPADA** (`predictive-swarm`, FR-PSW-002/004/005/011/012): Tier 1 gates determinísticos (loudnessGate ffmpeg EBU R128 + contrastGate WCAG/APCA + verdictFor) + tool MCP `vision.parse_sensory_gate` **VIVOS** no container `mcorch_vision_mcp` (ffmpeg 8.0.1 instalado + rebuild, /health anuncia); SSRF por redirect do ffmpeg **FECHADO** (host-pin Supabase + `-protocol_whitelist`, auditor adversarial 7 vetores); tsc 0 · vitest **121/121** · nó `9ecba7fa`. **(4) content-provenance BoK 9/9 selada** (AI Act Art.50, FR-CP-001..013): blueprint deepsearch `531e2b0` + suite `c569416`; **3 camadas** C2PA (c2pa-rs) + watermark (TrustMark/VideoSeal/AudioSeal) + metadata IPTC (ExifTool), USD=0; integra no spine `creative_assets`; nó `825088c0`. **Órfãos FK** diagnosticados (`user_provider_keys`/`user_api_keys` sem cascade; fix GO-gated). **Crítico adversarial pegou 6 bugs born-dead/SSRF pré-deploy**; contagem de Pattern Conformance das 3 BoKs conferida **MATERIALMENTE** (armadilha fechada). **12 commits** `b15554d..a33bdd7` · 2 `/security-review` NO FINDINGS + 1 auditor SSRF focado · migration aplicada + 3 fns + container deployados (GO Sovereign) · malha **9119** · nó `eed9128f`. ⚠️ Ressalvas: Cadência falta witness E2E de despacho (throwaway/UI); Enxame `swarm:read` fora do PAT allowlist (Fatia 2); rotacionar as chaves expostas. |
> 18	
> 19	| **Veo 3.1 com avatar por referência (Gemini API + Vertex service account) + blueprints cadência/enxame (2026-07-14/15)** | ✅ Sessão-maratona interativa (Sovereign ao vivo fornecendo chaves e diagnosticando billing). **(A) Motor Veo 3.1** (Amendment 25, FR-SPACES-086..091): nó Imagem→Vídeo ganha o único motor com **referências de identidade** (≤3 fotos do mood board → mesmo rosto); ledger-first + `veo-poll` (LRO owner-scoped) + failover de chave por 429. **Witness pago PROVADO E2E** (gen `02994319`, 720×1280 9:16 8s, identidade preservada Vision QA, 178 mco exatos). **(B) Veo via Vertex AI** (Amendment 26, FR-SPACES-092..096): 2º caminho de auth por **service account** (JWT RS256→token, `_shared/google-sa-auth.ts` WebCrypto, sem lib Google) p/ usar os créditos GCP (trial não cobre Gemini API/429, só Vertex — documentado no README do repo GabrielAI). Roteamento por `metadata.auth_type`; custo Vertex **267 mco** (0,15/s); poll `fetchPredictOperation` + vídeo inline base64; UI de colar SA JSON no pool. **Witness Vertex PROVADO REAL E2E em prod** (role Vertex AI User concedida 2026-07-15 → gen `2659d78b`, `engine=veo-vertex`, 720×1280 9:16 8s com áudio, **identidade preservada** por Read ocular + Vision MCP independente, débito exato **267 mco** 4263→3996; asset `bb0ec719`, nó `4e8902d2`). Credencial no pool (id `d3c99581`, cifrada). **(C)** 2× SSRF pegos e FECHADOS pelo `/security-review` (redirect A25 + location/project no host A26 via `buildVertexUrl`); anticorpos 9+8 testes. **(D)** Blueprints selados (Fatia 0, BoK-first): nó de **Cadência** ("além do ManyChat", `docs/bok/spaces-cadence/`) + **Enxame Sensorial-Preditivo** (`docs/bok/predictive-swarm/`) — ambos via deepsearch com crítico adversarial (10+4 bloqueios corrigidos). **~14 commits** `11dafd0..541c2c4` · 3× `/security-review` (NO FINDINGS ×2 + 1 HIGH fechado) · smokes 13/13 · **584 testes** · tsc 0 · lint 0 · malha **9111** · nó `91a3f1ec`. ⚠️ SA privada colada no chat → rotacionar após o teste. |
> 20	
> 21	| **YouTube Fatia 2 + débito eslint ZERADO + roadmap não-gated + branding OAuth Google (2026-07-14)** | ✅ Sessão-maratona pós-v6.100.0 (loop autônomo GO'd + Sovereign ao vivo na verificação Google). **(A) Roadmap não-gated drenado:** carrossel IG pelo caminho AGENDADO (Amendment 22, fecha OTD-SPACES-044 — marcador de grupo `carousel_render_id` resolvido owner-scoped, FMEA-011 por construção; smoke 9/9) · reframe server-side no publish (Amendment 23, fecha OTD-SPACES-043 imagem — motor `reframeToJpeg` extraído p/ `supabase/functions/_shared/reframe.ts`, px do seed channel_profiles, fail-open; smoke 8/8 geometria 1080×1350 por decode SOF real) · trilhos de mídia LinkedIn imagem + IG Stories + X media (Amendment 24, FR-SPACES-082..085) + hardening `supabase/functions/_shared/public-url.ts` `assertPublicHttpUrl` (fecha classe SSRF pré-existente nos 5 fetch de mídia caller-controlada) · UI dos trilhos (toggle reframe no AssetDetailDialog + "Agendar carrossel" no VideoRepurposePage). **(B) Débito eslint ZERADO 448→0** (`bun run lint` exit 0; 26 warnings restantes): fan-out 1-agente-por-arquivo (122 arqs) types-only, tipos reais (Tables<>, interfaces por SELECT, catch narrowing, remoção de casts `as any` supérfluos), tsc+test verdes por lote, 6 commits + ignore de vendored/worktrees. **(C) YouTube Studio Fatia 2** (Amendment 12): editar (videos.update) + excluir permanentemente (videos.delete) vídeo via `force-ssl` + receita (revenue_metrics) via `yt-analytics-monetary.readonly` → os **4 escopos ficam demonstráveis** p/ a verificação Google (não aprova uso futuro); `social-auth-init` +escopo monetário; UI card Receita + Editar/Excluir por vídeo gated; smoke 9/9 fail-closed sem tocar canal; `/security-review` NO FINDINGS. **(D) Branding OAuth Google FIXADO** (marca verificada ✅): home era iframe-only (DOM do pai vazio) → verificador sem-JS não via nome/info → home crawlável login-free (HTML estático no `#root` do index.html + header React visível "MCORCH" + descrição + links Entrar/Privacidade/Termos; provado por curl do HTML cru servido). **21 commits** `1c59da5..08f49c5` · 2 `/security-review` NO FINDINGS · smokes 9/9+8/8+9/9 · guard-sweep +2 anticorpos · malha **9108** · nó `5f75a568`. |
> 22	
> 23	| **Assets: seletor de formato + pré-visualização fiel + modal responsivo (2026-07-14)** | ✅ Diretiva Sovereign "UI ruim nos assets, imagens gigantes estragando o modal, no mobile não é app responsivo; faltam opções de publicação + previsualização perfeita por tipo (IG stories/feed/carrossel/reels, YouTube shorts/comunidade)". **BoK-first:** Amendment 21 `21-amendment-publication-format-preview.md` (FR-SPACES-075..078 + OTD-SPACES-043/044 defer + Pattern Conformance inline #13 Human-in-the-Loop) + SOP leve `space-publish-format-preview.md`. **`src/lib/format-specs.ts`** = SSOT client de formato (canal×superfície → aspect/px/safe-zone/caption/publicabilidade; números DERIVADOS do seed `channel_profiles` — Lei 1; paridade 15/15). **`PublicationPreview.tsx`** = 10 chromes fiéis (Reels/Stories/Short **9:16** action-rail+safe-zones · Feed **4:5**/1:1 · Carrossel · Pin **2:3** · link-card · YT vídeo/comunidade · text-post; render 17/17; caveat honesto "prévia aproximada"). **`AssetDetailDialog`** reescrito: picker de formato + preview vivo, publica **imagem E vídeo** via `publish-space-asset` (migra do `publish-social` legado só-vídeo), badges honestos (Publicável/Privado até auditoria/Em breve); modal full-screen app-like no mobile (dvh/gutter/rounded/tap-44) + mídia contida. **Vision QA ocular pegou+corrigiu** um blowout de CSS Grid `min-width:auto` que estourava a imagem no mobile (fix `grid-cols-1`+`min-w-0`). Play affordance nos tiles de vídeo + título no toque; `PublishSocialInspector` do canvas reusa o mesmo preview (formatId + resolveAssetUrl). **4 commits** `56bf601..0f543af` · tsc 0 · eslint 0 · **+32 testes** · 4 deploys ao edge público (serve entry novo) · **E2E wire** (corpo da UI → publish-space-asset → linha `space_publish_variants` draft owner-scoped, limpa) · malha **9107** · nó `66952b93`. **Uncommitted→selado nesta sessão.** |
> 24	
> 25	| **Motor Viral Quality + ASR self-host + pool multi-key BYOK (2026-07-14)** | ✅ sessão-maratona interativa (Sovereign testando ao vivo, GO'ing deploys). **(1) Motor Viral Quality** (video-repurpose, BoK `10-frd-sdd-viral-quality.md` selada c/ Pattern Conformance): detector `detect-viral-moments` (Hormozi sobre o SRT, janelas 15-45s, `text_beats` = cues VERBATIM, LLM só escolhe índices — zero fabricação Lei 1, JSON-mode + parse defensivo) + overlay motion-graphic (`viral-caption-overlay-9x16.html` Montserrat premium sem botão + `renderAlphaFrames` RGBA + FFmpeg overlay sobre footage reenquadrado; anticorpo do `-t` multi-input). UI "Gerar cortes virais" 1-clique (barra ancorada em sinais reais) + botão Distribuir (`publish-space-asset`) + badge SRT. **3 shorts EP01 provados E2E em prod** (abertura 9.0/finale 9.5/conspiração 8.5, Vision 7-8/10). **(2) ASR self-host** whisper.cpp US$0 + reconciliação roteiro-autoritativa (o áudio da IA erra nomes: Austin→Boston Dynamics; roteiro do GitHub GabrielAI via MCP é a verdade). **(3) Rota host-media** streaming Range (206 seek) — master 1,3GB abre na biblioteca; infra host versionada. **(4) Pool multi-key BYOK** (Amendment 20): `user_provider_keys` Vault-cifrada + `resolveProviderKey` (explícita→prioridade→legado→402) + Settings card + seletor Spaces — 3 Gmails × créditos free-tier. **6 commits** `d4972c7..23f6e65` · `/security-review` **NO FINDINGS ×4** · malha **9105** · nó `d98767ea`. **Gated Sovereign:** aplicar migration `user_provider_keys` + deploy `canvas-execute` + cadastrar 3 chaves + aprovar cadência. |
> 26	
> 27	| **YouTube Studio (Fatia 1) + front-door host-local do Repurpose (2026-07-13)** | ✅ sessão interativa "colocar a ferramenta pra funcionar" (Usuário Zero). **(1) Painel YouTube** `/dashboard/youtube` — edge fn `youtube-data` lê vídeos+métricas (Data v3 + Analytics v2) com token per-user de `social_accounts` server-side; escopos alinhados aos 3 registrados no Google (analytics adiado até habilitar a YouTube Analytics API); mapa exaustivo da API (`docs/bok/youtube-studio/11-api-surface-map.md`: 13 recursos·175 props·52 métricas·33 ações + Pattern Conformance 21 padrões) + SOP. **(2) Front-door host-local do Repurpose (admin-only)** `/dashboard/repurpose` — o Sovereign sobe o master pela UI e gera cortes; cap de 50MB do Supabase free → master (1,3GB) vai pro **disco do host** via `host-upload-server` (loopback 3220 atrás de nginx `/api/host-upload`, **upload chunked** 80MB/pedaço furando o cap de 100MB do CF, JWT+admin-gate, streaming); `ingest-external-asset` +sign_upload +provider `local` ADMIN-ONLY; `video-repurpose-run` +source `local` ADMIN-ONLY; worker lê `bucket=local` realpath-contido **sem copiar 1,3GB**. yt-dlp do host CONFIRMADO bloqueado pelo YouTube (bot-check). **(3)** fix legenda drawtext (truncagem por bytes-extra UTF-8 → padding). **EP01 real 1,3GB → 5 shorts 9:16** (1080×1920) provados por Vision QA (reframe centralizado + legenda completa). 5 commits `e174988..f10fba4` (+README `adcab9a`) · `/security-review` **NO FINDINGS ×3** · malha **9102** · nó `9f7b191a` |
> 28	| **Motor de repurpose de vídeo — Fatias 1-3 (1 master → N shorts + carrossel IG) + OTD-SPACES-036 + witness LoRA (2026-07-12)** | ✅ sessão-maratona interativa (Sovereign aplicou 3 migrations ao vivo + testou cada gate). **A metade que faltava: o MCORCH agora PRODUZ cortes, não só distribui.** BoK-first (Closed-Loop): blueprint `docs/bok/video-repurpose/00-deepsearch-blueprint.md` fundamentado em 10 pointers verificados file:line + no mapa do pipeline validado do repo `gabrielZarattini/GabrielAI` (o INVERSO — N takes Veo→1 master; fonte do master + schema de metadados `episodios/epNN.json` + filosofia cut-spec data-driven). **Correções ao snapshot:** segmenter é **FR-CP-012** (não OTD-CP-011; SDD já o gateava em "quando entrar INPUT de vídeo longo" → esta capacidade é o gatilho); OTD-CP-009 FECHADA (imagem, vídeo é gap); youtube Pilar I=montagem (concat), segmentação=inverso; carrossel existente=PDF/LinkedIn (IG image-children=gap, contrato Meta confirmado). **(Fatia 1 VIVA)** `source_module='external'` no spine `creative_assets` (migration aditiva aplicada) + seam `ingest-external-asset` (owner-scoped `${uid}/` + bucket allowlist + no-`..`; upload MP4 + metadados episódio + SRT inline; YouTube gated OTD-VR-001) · smoke 5/5 · `/security-review` NO FINDINGS. **(Fatia 2 VIVA E2E)** worker host `video-repurpose-bridge` (fila `video_renders` engine `repurpose` aditivo, rail FFmpeg **grátis** charged 0) → `segment-core` (trim `-ss/-t` frame-accurate + reframe 16:9→9:16/1:1 center-safe expression-crop + legenda queimada drawtext-textfile) · guarda **OTD-VR-006** re-valida source no READ (o controle decisivo tenant-safe) · **provado E2E na produção**: master→3 clipes reais (Vision QA: CENTRO preservado, ESQ/DIR cortados, **timestamp 00:00:04.000 prova o trim**, legenda queimada) · `/security-review` NO FINDINGS. **(Fatia 3 E2E provada)** `carousel-core` (key-frames dos capítulos → slides 1080×1350 4:5 + legenda wrapped + handle; **OTD-VR-007** wrap conservador, legendas curtas limpas, pixel-perfect via render-core diferido) + worker branch `mode='carousel'` + enqueue `slides[{t_sec,caption}]`≤10 + branch **media_type=CAROUSEL** no `publish-social` (contrato Meta) + seam `publish-space-carousel` (resolve slides owner-scoped→assina→publica) · **provado E2E**: master→3 slides 1080×1350 image assets + Vision QA no slide real · `/security-review` NO FINDINGS. **Distribuição reusada (não reconstruída):** cortes/slides nascem `creative_assets` que o nó **"Publicar em Rede Social"** (`publish-space-asset`/`space_publish_variants` — **OTD-SPACES-036** decisão (b) landada nesta sessão: tabela dedicada owner-scoped, money-path intocado, migration aplicada + smoke) já consome. **Witness LoRA:** treino real→402 Insufficient credit na conta Replicate BYOK do User 0 (plumbing 100% provado até o passo pago; bloqueado só em crédito — não código; inferência-com-LoRA é fatia futura inexistente). **Gates externos honestos:** publish real na IG/TikTok gated na auditoria de app (ação Sovereign). 6 commits `ac5ca86..831f5cc` · 3 migrations aplicadas · rail 100% grátis US$ 0 · Malha **9097** · nó `f050959c` |
> 29	| **Voz clonada self-host COMPLETA + Modo Expressivo + motion design do canvas (2026-07-09/10)** | ✅ sessão-maratona interativa (Sovereign testando ao vivo, 12 commits `578f02e..aa4041f`). **(1) Rail de voz US$ 0 VIVO** (OTD-VOICE-001 fechada por veredito auditivo): motor Qwen3-TTS no host (`/home/ubuntu/.mcorch/voice-engine/`, witness RTF 6,4/RAM 3,15 GB) · migration `20260709234000` (fila `video_renders` reusada engine `qwen3-voice` + provider `qwen3-local` owner-prefixed; `/security-review` NO FINDINGS; **anticorpo WAF**: Management API devolve HTML-challenge em payload grande com `DO $$` → apply em chunks + prova material sempre) · worker `voice-bridge.service` (claim atômico + **heartbeat anti-reaper** 4 min — bug witnessed: job de 5000 chars era re-claimado no meio) · edge `generate-voice` keyless async 202 (consent Art.11/sentinel INTACTOS) · nó default "MCORCH · grátis" pt-BR + poll `useVoiceRenderPoll` · **multi-amostra FR-SPACES-059** (1 principal + até 5 clipes ≤7s, ffprobe fail-closed nomeando o clipe, referência composta ffmpeg-concat) · perfil **ICL `.qvoice`** (máx fidelidade; x-vector rejeitado pelo ouvido) + `-ref.wav` ao lado (grafts são model-bound) · **smoke 12/12** `smoke-voice-qwen3-local.ts`. **(2) Modo Expressivo** (`7c20895`/`aa4041f`): 1.7B (4,3 GB) + assets `.expr` · witness **RTF 13,9 "composed 3 spans"** · **normalizador da sintaxe do Sovereign** (`{happy}…{/happy}` · `<#0.5#>` · `(gasps)` → gramática real do engine; tag desconhecida NUNCA falada; 0.6B recebe texto 100% limpo) · roteiro 5000→**20000** chars · **"Gerar roteiro com IA"** no nó (select de modelos pela regra perene: Nemotron free/Gemini Pro/Claude via openrouter · Gemini Flash direto; prompt-checklist embutido em `expressive-prompt.ts`). **(3) Reparos materiais**: reunion migration `20260710170000` (a `20260707230000` derrubara `avatar-studio` do guard `register_creative_asset` — TODO áudio fora do spine em silêncio; worker agora CHECA `error` do rpc — `supabase.rpc` não lança) · enum `generate_voice` + INSERT no Histórico (`vm_canvas_executions`, nascido terminal) + backfills (2 assets + 2 execuções do `b57a59f7`) · **aba Áudios** na Biblioteca (tile de onda + player; `<img>` de .wav era invisível). **(4) Motion design Amendment 19** (`d964b2e`): motion = telemetria — nó processando (glow pulsante + anel conic girando), edge transmitindo (partículas `animateMotion`+`mpath`), **fio neon established** quando `output.generatedAt` existe; `FlowEdge` como edge default; 1 seam (useMemo no CanvasEditorPage) cobre os 12 node types sem persistir estado visual; frame-diff provou animação viva; `prefers-reduced-motion` ok. **(5) Regra perene BYOK** (`f5e290f`, memória `feedback_byok_only_available_options`): `useConfiguredProviders()` deriva booleans da view mascarada (bullets/NULL, zero segredo no browser); seletor de motor dinâmico; **ElevenLabs IVC multi-amostra** (`f56e49d`); **F5-TTS/Fish Speech V1.5 REJEITADOS por licença** (pesos CC-BY-NC/-SA — produto é comercial; Amendment 18); zoom 0.02–12; fixes borda-sob-neon + thumb via `StorageImg`; OTD-SPACES-037 reconciliada não-issue (SpaceCanvasPage sem rota viva). 2× `/security-review` NO FINDINGS (e o aside do 2º pegou o CHECK `success` vs `completed` — corrigido pré-commit). Malha **9094** · nó `8c1f0e7b` |
> 30	| **Creative Studio — nós Roteiro + Criativo Cinematográfico vivos + cadeia completa (2026-07-09)** | ✅ maratona autônoma (loop armado pelo Sovereign, ~10 wakeups) — graduou a PoC de vídeo em MVP no Spaces. **(1) Roteiro** (`scriptGenerator`): v1 script SSE (`0d1714a`) + v2 **storyboard estruturado** `{scenes[],ttsPrompt}` via edge fn nova `generate-script-package` (`/security-review` SAFE, `508cda7`/`41483c4`) + **fan-out** "Criar N nós de imagem" (`e44df93`). **(2) Criativo Cinematográfico** (`cinematicVideo`, `4d8b80b`): renderiza MP4 9:16 MIV pela fila `video-render`/`video-bridge` (FFmpeg grátis) — **rail provado E2E** (enqueue 202→worker→done→MP4 1080×1920) + **Vision ocular** (pegou worker stale rodando template errado → restart → template MIV confirmado, `36b256d`; lição `reference_hyperframes_worker_restart`). **(3) Fundação**: 3 primitivos FFmpeg grátis (`encodeImageSequence`/`encodeKenBurns` + template `cinematic-9x16` MIV) · Amendment 17 + agente `creative-director` + 4 skills · **hotfix zip** do treino LoRA (`canvas-assets` aceita `application/zip`, `f0743de`). **(4) Decisões de motor**: TTS multi-motor **VoxCPM2** (Apache-2.0, pt-BR, clone) · identidade multi-motor (char-ref default) · **Duix rejeitado** (licença/GPU/pt-BR). **2 correções Lei 1** (503 stale + template stale, pegas por prova ocular/material). Malha **9086** · nó `6f2a5a90` |
> 31	| **Spaces robustez — treino LoRA grátis REAL + nó WordPress + blueprint YouTube Studio (2026-07-08/09)** | ✅ loop autônomo 9 commits + seal. **(1) LoRA grátis (foco #1)** — `handleTrain` engine-aware + LoRA default (`a0e8590`) · Amendment 11 (30 fontes, **fecha OTD-AC-017**; FR-AC-016 aprovação-condicional Replicate↔BFL on-platform+no-export, `5c63c7b`) · edge fn `avatar-identity-train` (Replicate `ostris/flux-dev-lora-trainer` BYOK **USD 0**, async start+poll, consent Art.11, migration `20260708130000` aplicada, `06261b9`) · **plumbing provado zero-custo** (guard 422/401 · consent+BYOK do User 0 passam · chave Replicate autentica na training API, latest_version.id do trainer Replicate (prefixo 26dce37a, NÃO é commit git)) · `/security-review` **SAFE**. **(2) 1º nó social** — "Publicar no WordPress" (Post+Landing Page, categoria Publish no registry VIVO, embute imagem upstream, default rascunho opt-in, `07689e2`) · Amendment 15 família Publish/Social (`6c80cd1`) · **media-social BLOQUEADO OTD-SPACES-036** (channel_variants NOT NULL pillar-coupled → decisão de schema Sovereign, `8e51482`). **(3) YouTube Studio (ask #3)** — blueprint deepsearch `docs/bok/youtube-studio/00-deepsearch-blueprint.md` (`wf_baad6dbe-9e5`: 6 frentes + verify adversarial, 96 URLs, 27 OTDs; **monetização gated** inauthentic-content + synthetic-media disclosure; lipsync MuseTalk MIT/SadTalker Apache self-host USD-0, Wav2Lip bloqueado, `6fa1652`). **(4) Higgsfield** Platform key testável (botão custo-zero) + card MCP honesto créditos-vs-assinatura (`44e625c`). Malha **9082** · nó `f0aa8111` |
> 32	| **TikTok Login + Higgsfield MCP DCR + Senior UX/UI Loop + Universe 3.10 seal (2026-07-08)** | ✅ sessão-maratona. **(1) Universe 3.10** — Phase Epsilon V9 SELADA (verif adversarial 8-frentes `wf_98c9d432`, 7 PASS + re-escopo 3.2 honesto; tsc 0 · vitest 496/498 · E2E Vision; nó `c20153c1`, commit `2841683`). **(2) TikTok Login Kit v2** — BoK 9/9 selada (`299b9f36`) + SOP Lei 2 + 3 edge fns `verify_jwt=false` + migration `tiktok_identities`/`tiktok_login_codes` + botão gated `?devLogin` + SPA callback; **/security-review: 1 HIGH login-CSRF FECHADO** (browser-binding sessionStorage→state→binding_hash); **2 correções de reuso Sovereign**: mesma chave do connect via `social_app_config` (`2461fa2`) + reusa `social-auth-callback` já registrado por `intent` assinado (`aa7c2a0`, elimina gate redirect_uri); smoke 8/8 · browser-verify · connect íntegro. **(3) Higgsfield** — Platform key nas Settings (`989e560`, browser-verify logado) + **MCP OAuth DESTRAVADO via DCR programático** (client público em `mcp.higgsfield.ai/oauth2/register`, sem Clerk manual; oauth-init→authorization_url). **(4) Senior UX/UI Loop** (`5a0f695`) — auditor de jornada + grader `senior-rubric.ts` 8-dim SCORED + runner + SOP+skill+RUBRIC; unit 5/5 + prova live (P2 contraste "ou"). **(5) User 1** (`user1@teste.com`, `c515c035`) p/ QA. **(6) it.4b editor** = HyperFrames (`3e45e08`). Malha **9081** · nó `17e8921b` |
> 33	| **Spaces v2 — consolidação Canvas Studio + money path ledger-first + nós Lista/Upscale (2026-07-07)** | ✅ 11 commits `efaf190..ad42170`: **it.1** rename Canvas Studio→"Spaces" (`/dashboard/spaces` takeover, redirects **5/5** provados `verify-spaces-redirects.ts`, nav única, UI v1 aposentada — retorno ao contrato BoK `spaces-evolution`, **Amendment 14**) · **it.2a/b/c money path ledger-first** (project-dispatch em `generations`: migration `20260707220000` FK composta+XOR+RPC 9-args aditiva · edge fn catálogo fail-closed + style_transfer engine-fix + campaign-context + GAP-8 · cliente `useCanvasExecute` minta node_run_id + dual-read HistoryTab/StatusBar · watchdog cron 2º passe sobre `generations` + entrada de resgate service-role no webhook · `self-heal` exclui async; **/security-review NO FINDINGS**; smoke **40/40** + watchdog **6/6**; **witness pago** 4519→4518 exato, zero rows legadas → **OTD-SPACES-012 fechada**) · **it.4a nó Lista + lote template×produtos** (o "Lists" do Magnific; `product-list.ts` unit 10/10; witness 2 produtos→2 imgs, 20 mco exatos) · **it.3 thumbnails home** (URL re-assinável via StorageImg; witness + Vision APROVADO) · **it.4c nó Upscale REAL** (Replicate real-esrgan, money-safe auto-refund provado E2E, mensagem acionável de crédito) · **it.0a** fix preço sceneCompose 18→10. **2 bugs pré-existentes consertados** (style_transfer ignorava imagem-fonte; `creative_assets` rejeitava `source_module='spaces'` → registro falhava em silêncio desde Fase 1b, migration `20260707230000`). **Higgsfield resolvido:** nós usam a API key do vault (`keys.higgsfield`), MCP é opcional. guard-sweep **9/9**. Malha **9077** · nó `6a70b82b` |
> 34	| **Arco 8 — Laço Autonômico MAPE-K enterprise-grade VIVO (2026-07-07)** | ✅ 19 commits `9538e09..c197054`: M+A mecânicos perpétuos (guardian-tick */5 T1-T5 + heartbeat + incidentes dedup/cooldown/auto-resolve · guard-sweep 6/6h runner destacado · watchdog=monitor-do-monitor provado ao segundo · UX-Explorer nightly → `--ingest-findings`) + P+E em escada (L1 Telegram · **L2 ARMADO toggle --arm/--disarm, engine `nvidia/nemotron-3-ultra-550b-a55b:free` USD-0** [claude -p preservado via REMEDIATE_ENGINE] · L3 sessão event-driven via Monitor) · /security-review **BLOCK→4 must-fixes** (allowlist sem exec · git diff out · flock<budget · run-dir 0700) · **1º ciclo real fechado**: video-bridge render_failed → L2 diagnóstico validado → `422 composition_required` pré-débito (`f678cb3`) → resolvido · +2 incidentes de estreia corrigidos (PATH cron · dogfood inexistente) → sweep **7/7 auto-resolve**. SOP `autonomic-loop-mape-k.md`. Sessão Claude = bancada de dev pura. Malha **9071** · nó `d149d017` |
> 35	| **Loop (arco 7) — vizinhos on-select + OTD-SPACES-010 + backlog-drenado + hardening 478 testes (2026-07-06)** | ✅ 12 commits `235d7a2..828e492`: vizinhos semânticos on-select (verify browser PASS live) · OTD-SPACES-010 reconciliada (OIDC §3.1.3.7 — JWKS redundante no code-flow TLS; +check exp; vitest 17/17; deploy callback) · **varredura 7-agentes atesta backlog autônomo de feature DRENADO** (nó `aaf7a126`) · dead code `monetizationStats` removido · Fatia hardening GO-continue: **+53 testes** (semantic-synapses DRY 14 · universe-layout 9 · orientação 4 · canvas-utils 14 · sso-cookie anti-open-redirect 7 · asset-url 9), suite **448→478**, zero produção alterada. Anticorpo: nunca filtrar output de `git commit` (secret-scan bloqueou fixture; pego por git log). Malha **9067** · nó `3a145a46` |
> 36	| **Loop (arco 6) — Universo sinapses semânticas 768d + perf reconciliada (2026-07-05)** | ✅ 6 commits: `OTD-UCANVAS-PERF` reconciliada (não-issue: ~30s headless SwiftShader, real 2,5s — medição material, zero code churn) + **sinapses Fase B `OTD-SYNAPSE-EMBEDDING` SHIPPED** (RPC `match_memory_code_synapses` SECURITY DEFINER user_id-NULL-hardcoded LATERAL k-NN HNSW → **148 sinapses por similaridade 768d** código↔memória na fusão primária, ciano tracejada vs fúcsia sólida real, contadores separados [Lei 1]; /security-review NO FINDINGS; gate E2E Vision-APROVADO; smoke anticorpo 8/8). Loop **adiado p/ 2026-07-06 11:01** (cron `0f94aff2` session-only). Malha **9062** · nó `9afacad2` |
> 37	| **Loop FINAL (arco 5) — conector Higgsfield MCP server-side+UI COMPLETO + parada natural (2026-07-05)** | ✅ sub-fatia 7 UI card `217b4e3` (Settings→Conectores + callback page, browser-verify ocular) fecha o conector; 7 sub-fatias totais; parada natural (backlog desbloqueado esgotado, restante gated no Sovereign); malha **9060** · nó `dc47da77` |
> 38	| **Loop autônomo — brand-tail + Unified cutover + vídeo recorrente + conector Higgsfield MCP (2026-07-05)** | ✅ 12 commits: cauda de brand 100% `6af3181` + Unified Canvas 3.9 cutover `4729dd4` + cadência de vídeo recorrente FR-VA-022 `c5eaf1c` + **conector Higgsfield MCP OAuth server-side COMPLETO** (sub-fatias 1-6: sentinel G1 `268d436` · migration `0c9d182` · init `17597ab` · callback `988b1b9` · refresh/resolve `97b1e2f` · disconnect RPC `99d543a`); ciclo de credencial per-user fail-closed (connect·refresh·resolve·disconnect); **2× /security-review SAFE 9/10**; malha **9059**; E2E gated no consent Clerk (Fila 175) |
> 39	| **Loop it.1 — Anticorpo de assinatura owner-scoped (Fix Assets)** | ✅ `scripts/qa/smoke-asset-owner-signing.ts` 6/6 LIVE hermético (owner-sign 200 · cross-sign BLOCKED · enumeração 0 · id-squat neutralizado · is_public=0); fecha Mandato Obstáculo→Síntese |
> 40	| **Loop it.2 — BoK amendment Higgsfield MCP OAuth connector** | ✅ `docs/bok/spaces-evolution/13-amendment-higgsfield-mcp-connector.md` — gate Closed-Loop 3.5 fechado; contrato vivo provado (401 OAuth · 201 DCR · discovery Clerk); FR-SPACES-015..021 + OTD-SPACES-007; código gated na aprovação Sovereign |
> 41	| **Fix Assets — mídia privada assinável só pelo dono (regressão FECHADA)** | ✅ migration `20260703030000` (3 policies owner-scoped + triggers de id anti-claim + data-repair) + normalizador durável em 13 superfícies; `/security-review` CLOSED 9/10; E2E Vision-APROVADO; 90 assets do User 0 vivos |
> 42	| **Spaces 2d compose — drift FECHADO (OTD-SPACES-003)** | ✅ compose vivo E2E via OpenRouter Nano Banana (10 mco) + bucket privado assinado + sentinel de contrato Higgsfield |
> 43	| **Retema MIV do ecossistema + landing fiel + gate TikTok (2026-07-04)** | ✅ design system global MIV (void/cyan/gold/nebula · Playfair/JetBrains) revestindo 47 páginas + login + shell; landing 100% fiel ao original (hero WebGL cinematográfico + texto honesto, iframe); favicon do sigilo consistente + Privacidade/Termos MIV (footer único, conteúdo preservado); 44 páginas polidas via workflow 9-subagentes, E2E 0-erros |
> 44	| **brand-100 — emoji→lucide + data-viz→MIV em ~40 superfícies (2026-07-05)** | ✅ workflow de 7 subagentes: ~90 emoji→lucide (Minerador/Blog/canvas/crew/páginas; avatares→`AVATAR_ICON_MAP` compartilhado), data-viz→MIV (Louvain/node-types/territórios cyan/gold/nebula/teal; blobs magenta→cyan). Minerador+Matrix verificados. mesh **9057** · commits `855a4ad`/`8d65bb2`. Pendente cross-file: pickers de campanha/space |
> 45	| **Brand-everything (Orquestrador/Core-Fable → MIV) + /miv/ completo (2026-07-05)** | ✅ diretiva "tudo vira brand": Orquestrador Visual violet/fuchsia/magenta→cyan + ícones emoji→lucide (`NodeIcon`); Core-Fable amber→cyan; **`/miv/` serve o MIV completo** (site-miv, era 404). mesh **9056** · commits `b92c367`/`cbe5730`. Pendente honesto: emoji de templates/miner + paletas data-viz |
> 46	| **Certificação E2E User Browser + fechamento pt-BR (2026-07-05)** | ✅ E2E de 8 jornadas de usuário real (fresh, ambiente verificado limpo): **flow_works 8/8 · MIV-conformant 8/8 · 0 P0/P1/P2** (2 pass + 6 warn só-P3); anticorpo Lei 1 (squat de `python -m http.server` na porta contaminou o 1º run — subagentes flagaram, fix = verificar o bind antes de rodar). pt-BR fechado em toda a cauda (Arena/Economia/Orquestrador/Matrix/Memory/Video/3D). mesh **9055** · commits `94df8d0`/`63fee7b`/`becf373` |
> 47	| **Conformidade MIV pós-rebrand + tooling ECC-nativo (2026-07-04)** | ✅ auditoria visual E2E de 44 páginas (workflow 8 subagentes agent-browser — real-user nav, hovers, triggers, badges, widgets); 3 fixes sistêmicos (`--accent` cyan · mcoCoins gold · glow CTA) + regressões de marca (onboarding MCORCH · 404/miner/legenda pt-BR · Trial cyan) verificados ao vivo; tooling ECC-nativo (doctor · supply-chain sentinel · session-inspect) + SOP. mesh **9051** · commits `aaa2351`/`75077f6`/`8af7268` |
> 48	
> 49	## Credenciais globais de app + AI Act Fatia 0-1 + content-intel BoK 9/9 + wildcard gcrux.com Record (2026-07-17)
> 50	
> 51	**ORO:** Operator = MCORCH Master Execution Agent · Reviewer = `/security-review` (NO FINDINGS ×3) + reviewer independente (pegou bug de preserve do status + o WORKER_RESOURCE_LIMIT) + Vision QA · Owner = Sovereign (decisões: colar chaves globais, GO do backfill, DNS wildcard, gates de app-review, GO do módulo content-intel com revisão jurídica).
> 52	
> 53	Sessão-maratona interativa iniciada por diretiva do Sovereign ("os escopos Google aprovados + Pinterest aprovado, preciso colar a chave em /dashboard/admin sem .env/CLI") e drenada ao longo do dia com o Sovereign ao vivo (colando credenciais, gravando vídeos de app-review Pinterest/TikTok, otimizando o EP01 no YouTube). Fechou 5 frentes com prova material (Lei 1) e commit granular. Selada por `/handoff` explícito.
> 54	
> 55	| Frente | Resultado |
> 56	|--------|-----------|
> 57	| Tier global de credenciais (FR-PE-017..021) | ✅ Admin cola chave de app no `/dashboard/admin` sem .env; resolver 4 degraus 6 plataformas; seed env→global 6/6; smoke 13/13; `/security-review` NO FINDINGS (`9d94771`/`df98397`/`f4dd523`) |
> 58	| Pinterest/X reconectados + UI boards | ✅ credencial global (OTD-PE-SOCIAL-APPCREDS fechada); anticorpo per-user-shadow; `pinterest-boards` edge fn + card (`9214df7`) |
> 59	| AI Act Art.50 Fatia 0-1 VIVO | ✅ 5 colunas na spine + writer 26 args + ExifTool IPTC + worker; **101 assets marcados**, witness real; `/security-review` NO FINDINGS (`fa30a69`/`68d9163`/`7226717`) |
> 60	| `*.gcrux.com` wildcard | ✅ vhost servindo `hello.gcrux.com` HTTP 200 (`f462173`) |
> 61	| content-intel BoK 9/9 | ✅ módulo novo; blueprint deepsearch → Scribe 9/9; Pattern Conformance 21; seal `2e918a8c` (`91f1222`) |
> 62	| Fixes | ✅ morning-briefing security ciso-4 falso + pin repo (`3d5a2f4`); WORKER_RESOURCE_LIMIT megapixels (`42ca370`); lint herdado (`b5c5474`) |
> 63	
> 64	### Arquitetura — resolver 4 degraus de credencial de app (Amendment 16)
> 65	```
> 66	social-auth-{init,callback} + refresh-social-token (6 plataformas)
> 67	  → resolveSocialAppCreds(platform):
> 68	      (1) social_app_config per-user (auth.uid(), is_active)   ← tenant BYOK
> 69	      (2) social_app_config GLOBAL  (user_id IS NULL, is_active) ← admin /dashboard/admin (NOVO)
> 70	      (3) Deno.env fallback (legado/emergência)
> 71	      (4) SocialAppConfigError 402 { <platform>_not_configured }
> ```

## 🤖 Claude *(21:14:13)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 9839,
  "limit": 400
}
```

> **Tool Result (Read)** - ❌ Error
>
> ```
> File content (26572 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
> ```

## 🤖 Claude *(21:14:14)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md"
}
```

## 🤖 Claude *(21:14:14)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null",
  "description": "Scratch dir contents"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 8
> drwxrwxr-x  2 gcrUX gcrUX 4096 Jun 30 01:44 .
> drwxrwx--- 33 gcrUX gcrUX 4096 Jul 17 16:32 ..
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

## 🤖 Claude *(21:14:27)*

<details>
<summary>💭 Thinking Process</summary>

I've got what I need from the context. The most recent seal shows global app credentials with the AI Act tier and content intelligence book complete, all dated for today. The latest commits are tracked, so I have enough to move forward with the brief.

Let me quickly run the BoK gate check to verify completeness across the 34 slugs, then I'll have everything needed for the handoff summary.

</details>


## 🤖 Claude *(21:14:27)*

Pre-flight completo. Rodando o BoK Gate check (protocolo v3) antes do brief.

## 🤖 Claude *(21:14:33)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nincomplete=0\nfor slug in $(ls docs/bok/ 2>/dev/null); do\n  if [ \"$slug\" = \"security\" ]; then\n    required_sec=(00-[[deepsearch-blueprint|deepsearch-blueprint]] 01-brd-security 02-srs-secure-spec 03-sdd-hardening-architecture 04-fmea-security)\n    missing=()\n    for doc in \"${required_sec[@]}\"; do\n      [ -f \"docs/bok/security/$doc.md\" ] || missing+=(\"$doc\")\n    done\n    [ ${#missing[@]} -eq 0 ] || { echo \"\u26a0\ufe0f security \u2014 missing: ${missing[*]}\"; incomplete=$((incomplete+1)); }\n    continue\n  fi\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] || { echo \"\u26a0\ufe0f $slug \u2014 missing: ${missing[*]}\"; incomplete=$((incomplete+1)); }\ndone\necho \"---\"\necho \"Total BoK slugs: $(ls docs/bok/ | wc -l) \u00b7 Incompletas: $incomplete\"",
  "description": "BoK Gate completeness check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ---
> Total BoK slugs: 33 · Incompletas: 0
> ```

## 🤖 Claude *(21:14:40)*

<details>
<summary>💭 Thinking Process</summary>

All 33 BoK suites are confirmed complete, and since today is 2026-07-17 matching the last seal date, I'm continuing from where I left off. Now I'll generate the structured brief in Portuguese.

</details>


## 🤖 Claude *(21:15:03)*

Contexto completo. Aqui está o brief.

```
═══════════════════════════════════════════════════════════
  HANDSON — Credenciais globais de app + AI Act Fatia 0-1 + content-intel BoK 9/9 (2026-07-17)
═══════════════════════════════════════════════════════════
```

🏁 **ESTADO ATUAL**
Fase selada: **Tier global de credenciais de app (admin) + AI Act Art.50 Fatia 0-1 VIVO + content-intel BoK 9/9 + wildcard `*.gcrux.com`** — sessão-maratona interativa, 12 commits `b5c5474..91f1222`.

Últimos commits:
- `3400742` — docs(handoff): seal credenciais globais + AI Act Fatia 0-1 + content-intel 9/9 (malha 9133)
- `68e405e` — docs(readme): v6.106.0
- `91f1222` — docs(bok): content-intel 9/9 selada (módulo novo)
- `42ca370` — fix(publish): guard de megapixels no reframe (WORKER_RESOURCE_LIMIT)
- `9214df7` — feat(pinterest): UI de gestão de boards no /dashboard/social

📂 **MUDANÇAS PENDENTES**
`D proof-manifest.json` — arquivo de prova QA deletado no working tree (1 linha). Artefato transiente da Fase 5c; não conflita com nada. Descrito, não commitado (decisão sua).

🏗️ **INFRA** — tudo saudável
- `mcorch_vision_mcp`: Up 2 days (healthy) · `mcorch_chroma`: Up 4 weeks (healthy) — Chroma API v2: **OK** (`heartbeat`)
- `mcorch_claude_mem`: Up 4 weeks (healthy)
- `mega-brain-daemon`/`webhook`/`dashboard`: Up 4 weeks (healthy)

🧠 **KNOWLEDGE MESH**
**9133 nós** (fonte: Task State header · milestone `9aa1b522` embedado 768d nesta sessão)

🔧 **TYPESCRIPT** — Zero erros ✅ · vitest **621** verde no último seal · gitleaks clean

📚 **BoK SUITES** (v3 — MCORCH Master Execution Protocol)
Sealed: **33/33 completas** ✅ (nenhuma incompleta) — inclui a novíssima `content-intel` (seal `2e918a8c`, DERIVES_FROM vision-mcp) e `content-provenance` (AI Act, seal `825088c0`).
GATE alert: **nenhum bloqueador** — todo módulo com trabalho ativo tem BoK selada.

📌 **SPRINT**
Goal: distribuição social autônoma + motor criativo agêntico (Spaces). Roadmap governado pela **FILA SOVEREIGN** em `sprint-priorities.md`.

⚡ **PRÓXIMOS PASSOS** (fila declarada — não reordenar sem GO)
1. **content-intel Fatia 1 (código)** — módulo novo BoK-selada, gate ABERTO. Bloqueio: **GO Sovereign + revisão jurídica no ingest** + sondar OTD-CI-002 (resolver mp4 IG/TikTok server-side; IP datacenter bloqueado).
2. **AI Act Art.50 Fatia 2** (C2PA + watermark de voz) e **Fatia 3** (watermark visível) — gated (cert/GPU). Prazo legal **2026-08-02** (multa Art.99). Fatias 0-1 já VIVAS (101 assets marcados via IPTC/ExifTool).
3. **landing-factory Fatia 1** — código do `landing-bundler` core já shipado (`762c641`, 15/15 unit); resta encadear na fábrica + gate CRO 95%.

⚠️ **ALERTAS**
Nenhum alerta técnico ✅ (tsc limpo, containers healthy, scratch/ clean).

Pendências **de sua ação** (Sovereign, não-bloqueantes p/ dev):
- **Rotação de credenciais** — SA Vertex / Gemini / Telegram (banner `admin_reminders` já criado; chaves foram coladas no chat em sessões anteriores).
- **App-review externo** — Pinterest Trial→Standard (vídeo enviado) + Meta redirect URI + reconexão X/app-audit IG/TikTok.
- **OTD-PSW-001** (GPU predictive-swarm) — adiado até créditos Vertex acabarem.

```
═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════
```

O worktree está limpo (só o `proof-manifest.json` deletado). A fila de maior prioridade é o **código do content-intel**, mas ele está travado em GO explícito + revisão jurídica — Lei 2/BoK gate satisfeitos, falta só o seu sinal. Qual frente ataco?

## 👤 User *(21:27:15)*

Go para todos os próximos passos. Sobre pendências Sovereign, vou fazer o video para a meta, achei onde tem os casos de uso e são.:


1. Adicionar permissões obrigatórias de mensagens
Adicione estas permissões de gerenciamento de conteúdo e mensagens para criar, publicar e gerenciar conteúdo, além de responder diretamente a mensagens e enviar respostas privadas com sua conta do Instagram. As permissões e os recursos obrigatórios e opcionais podem ser configurados na página Permissões e recursos.
instagram_business_basic
instagram_business_manage_comments
instagram_business_manage_messages
OK

--


2. Gerar tokens de acesso
Adicione uma conta do Instagram para gerar tokens de acesso e configurar assinaturas de webhook.
Conta do Instagram
Token
Assinatura do webhook

gabrielorchai
17841454441962105
Gerar token

Ativado
Falta gerar o token. Quando tiver onde colocar nas configurações me avisa que gero e adiciono lá para enviar pro vault pela UI do dashboard

3. Configurar webhooks
Configure um URL de webhook personalizado ou use serviços para configurar um ponto de extremidade. Saiba mais
Seu app deve estar com o status de publicado para receber webhooks.
URL de callback
https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/instagram-webhook
Verificar token

Campos do webhook

Campo
Versão
Testar
Assinar
comments
Seletor da versão de assinatura para o campo de webhook comments. Definido na versão v25.0.
v25.0

Teste

Assinado
live_comments
Seletor da versão de assinatura para o campo de webhook live_comments. Definido na versão v25.0.
v25.0

Teste

Assinado
message_edit
Seletor da versão de assinatura para o campo de webhook message_edit. Definido na versão v25.0.
v25.0

Teste

Assinado
message_reactions
Seletor da versão de assinatura para o campo de webhook message_reactions. Definido na versão v25.0.
v25.0

Teste

Assinado
messages
Seletor da versão de assinatura para o campo de webhook messages. Definido na versão v25.0.
v25.0

Teste

Assinado
messaging_handover
Seletor da versão de assinatura para o campo de webhook messaging_handover. Definido na versão v25.0.
v25.0

Teste

Assinado
messaging_optins
Seletor da versão de assinatura para o campo de webhook messaging_optins. Definido na versão v25.0.
v25.0

Teste

Assinado
messaging_postbacks
Seletor da versão de assinatura para o campo de webhook messaging_postbacks. Definido na versão v25.0.
v25.0

Teste

Assinado
messaging_referral
Seletor da versão de assinatura para o campo de webhook messaging_referral. Definido na versão v25.0.
v25.0

Teste

Assinado
messaging_seen
Seletor da versão de assinatura para o campo de webhook messaging_seen. Definido na versão v25.0.
v25.0

Teste

Assinado
standby
Seletor da versão de assinatura para o campo de webhook standby. Definido na versão v25.0.
v25.0

Teste

Assinado

---


4. Configurar o login da empresa no Instagram
Use o URL abaixo em uma tag ou botão de ancoragem no seu site para iniciar o login da empresa. Para saber mais sobre como capturar tokens de acesso e personalização do URL, veja nosso(a) developer docs.
URL incorporado
https://www.instagram.com/oauth/authorize?force_reauth=true&client_id=1271182438521153&redirect_uri=https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback&response_type=code&scope=instagram_business_basic%2Cinstagram_business_manage_messages%2Cinstagram_business_manage_comments%2Cinstagram_business_content_publish%2Cinstagram_business_manage_insights
Lembre-se de analisar suas configurações de login da empresa e fornecer os URLs das solicitações de desautorização e exclusão de dados antes de enviar para análise do app.

OK

----

5. Concluir a análise do app
Para que seu app acesse dados ao vivo, o Instagram exige que o processo de análise do app seja realizado. Passe por esse processo para ter acesso avançado às permissões do Instagram. Envie sua solicitação de análise do app quando tudo estiver pronto.
Você pode pular esta etapa se desenvolve apenas para suas próprias empresas no Instagram e não pretende criar soluções para clientes.

Ir para analise.:
Você tem a documentação necessária para a análise do app?
Requisitos:
Confirme se o seu app pode ser carregado e testado externamente.
Forneça detalhes claros do caso de uso e descreva passo a passo como uma pessoa usa seu app.
Conte como seu caso de permissões do Instagram segue o(a) usage guidelines. estabelecido(a). Será necessário carregar gravações de tela que demonstrem como seu app usará cada permissão.

Solicitar acesso avançado a permissões
As permissões a seguir são recomendadas para o Instagram e serão adicionadas à sua solicitação. Você precisará concluir as descrições de uso para essas permissões na análise do app. Saiba mais
Obrigatório

instagram_business_basic

Recomendado

instagram_business_manage_messages


instagram_business_manage_comments


instagram_business_content_publish


instagram_business_manage_insights


Human Agent

todos marcados checked.

Avançar para a analise.:
Solicitações de permissão foram adicionadas. Redirecionando você para a análise do app para finalizar sua inscrição.


Envios de análise do app
Após o envio, nossos analistas avaliarão todos os aspectos do app para garantir que a configuração ofereça uma experiência segura e de alta qualidade aos usuários. A análise inclui as solicitações novas e as aprovadas anteriormente para assegurar que estejam de acordo com nossas políticas. Também avaliaremos o ícone do app, o URL da Política de Privacidade e outras configurações. Sobre a análise do app
Não enviado
Novas solicitações
Human Agent
Diretrizes de Uso
Em 1 caso de uso
instagram_business_basic
Diretrizes de Uso
Em 1 caso de uso
instagram_business_manage_messages
Diretrizes de Uso
Em 1 caso de uso
instagram_business_content_publish
Diretrizes de Uso
Em 1 caso de uso
instagram_business_manage_insights
Diretrizes de Uso
Em 1 caso de uso
instagram_business_manage_comments
Diretrizes de Uso
Em 1 caso de uso


---

Só tem um caso de uso.:
Personalizar caso de uso
Personalize as configurações e permissões de casos de uso para que seu app funcione do jeito que você quer.
Alterar caso de uso

API do Instagram

Gerenciar mensagens e conteúdo no instagram

Da para adicionar outros se necessário preciso que me ajude... Adicionar mais casos de uso
Você pode adicionar casos de uso de várias categorias, mas nem todos os casos de uso podem ser adicionados ao mesmo app. Crie um novo app se os casos de uso que você quer adicionar não estiverem disponíveis.
Filtrar por

Em destaque (4)

Tudo (15)

Anúncios e monetização (7)

Gerenciamento de conteúdo (5)

Business Messaging (2)

Outros (1)

Acredito que vamos precisar de outros então é melhor você usar o browser para ver as opções e configurar pra mim.: https://developers.facebook.com/apps/1714996696595611/use_cases/?business_id=199655428199841

---

## 🤖 Claude *(21:28:26)*

<details>
<summary>💭 Thinking Process</summary>

I'm parsing what the Sovereign is asking for—there are two parts to this directive covering the three roadmap items I identified. But I'm noticing the content-intel Fatia 1 had a gate requiring the Sovereign's approval plus legal review on the ingest side, and the Sovereign's message seems to be addressing that condition.

For the Instagram/Meta app review setup, the Sovereign is asking for specific permissions to be added to the OAuth flow and needs me to set up a place in the dashboard settings where they can paste the Instagram account token so it can be stored in the vault. The account details are gabrielorchai with IG id 17841454441962105, and I need to provide them with a UI location to input this before they generate and add the token.

I also need to verify the webhook configuration — the callback URL is already set up at the Supabase edge function endpoint with all the necessary fields subscribed, but I should check the edge function to confirm what verify token the Sovereign should use when setting up the webhook in Instagram's configuration. There's also a business login URL with specific client credentials and scopes that needs to be analyzed and provided to them.

Beyond that, I need to handle the deauthorization and data deletion callbacks — these are Meta app review requirements for LGPD compliance. I should check if these endpoints already exist or if I need to build them, since they tie into the existing data deletion infrastructure. Finally, for the app review submission, there's currently only one use case configured, but the Sovereign wants me to explore what other use cases are available through the Meta developer dashboard and set those up as well.

Now I'm noticing something important about the app IDs — the business login is using one client ID while the app review dashboard shows a different app ID entirely. These don't match up, which could be a configuration issue I need to investigate.

The codebase mentions they've migrated from the old `magicorch` app to the new rebranded `gabrielorchai` persona, so this is definitely the updated setup. I need to figure out what I can actually do versus what requires the Sovereign's direct involvement, especially since accessing the Facebook developer dashboard requires their authenticated session.

I have access to claude-in-chrome which connects to the Sovereign's real Chrome browser, so if they're already logged into Meta developers there, I could potentially navigate and make changes. But this is high-stakes territory — modifying live Meta app configurations directly affects the Sovereign's external-facing setup, so I need to be extremely careful about what actions I take versus what I escalate to them.

The Sovereign did authorize me to use the browser to view and configure the use cases, but I should distinguish between safe configuration work and irreversible actions like submitting an app review. I can explore the options, help set things up, and advise on what needs to happen, but submission itself should be their call. Let me start by viewing what's currently there, then structure out what needs to happen next.

I'm mapping out two parallel tracks: the code roadmap with the content-intel work (blocked on legal review but I can build it with a checkpoint), the AI Act pieces (gated on external dependencies), and landing-factory; and the Meta/Instagram app review work, which includes building out the dashboard Settings UI where they can paste the Instagram token into the Vault—that's the concrete second ask they mentioned.

Then there's the webhook verification token to check in the edge function, the deauthorize and data deletion endpoints Meta requires, and configuring use cases on their app dashboard. This is a lot happening across multiple fronts, and while I could use workflows for the investigation and build work, some of this needs interactive browser sessions and stateful interactions that workflows can't handle well. I need to think through the right sequencing and figure out what's actually blocking versus what I can build now.

The Sovereign is actively recording the Meta app review video right now, so the time-sensitive priorities are clear: get them the webhook verify token so they can click the verification button, provide the token-paste UI in the dashboard for storing the generated token in the Vault, build those required deauth and data-deletion URLs, and help them configure the use cases in the browser. The broader code roadmap around content intelligence, AI Act compliance, and the landing factory matters, but it's not time-boxed to this moment while the video is being recorded.

But here's the thing — the Meta review submission itself requires the app to be demonstrable, so the token-paste UI and those deauth/deletion URLs are the real blockers. Let me focus on Track 2 first and weave in Track 1 as I go. Before I start building anything, I need to investigate the current state: Does the Instagram webhook edge function already exist and what verify token is it checking? Is there a Settings UI for pasting an Instagram access token into the Vault, and what's the current credential path? Do the deauth and data-deletion endpoints exist yet? And what's the scope of the content intelligence work for this phase?

I also need to check the landing-factory state and whether the landing-bundler already shipped. The Sovereign provided the Instagram credentials I'll need: account `gabrielorchai`, user ID `17841454441962105`, Meta App ID `1714996696595611`, the OAuth client ID, business ID, and the webhook and OAuth callback URLs. Rather than tackle everything sequentially, I'll spin up parallel investigation agents to map out each front, though some areas are small enough that I should just examine them directly to get the precision I need.

I'm weighing whether to use Workflow for this or handle it more interactively. The task has high reasoning effort and ultracode is on, which suggests Workflow, but there's a strong interactive component here—I'll be looking at the Sovereign's live account and providing exact token details. My approach is to do a fast material investigation first across all fronts to see exactly what exists and what's blocking, then present a clear plan and start executing the high-leverage items that unblock the Meta video integration—verifying the token, building the token-paste UI, and getting the deauth and deletion URLs ready. After that I'll handle the use-case configuration through the browser.

Before I proceed, I need to check if a browser is actually connected to the Sovereign's session. Rather than over-orchestrating with workflows, I'll use parallel Explore agents for mapping what exists, but I should prioritize the most time-sensitive ask first—the webhook verify token that the Sovereign needs right now to click "Verificar token" in the Meta console. That's a direct read of the Instagram webhook edge function. I'll also need to check the current Settings surfaces for the token-paste UI, then launch a broader investigation with parallel agents.

Given the enormous scope, I'm going to focus on what matters immediately: the Meta app-review enablement is the critical path since the Sovereign is recording that video right now. The code roadmap is secondary background work. I'll start by directly reading the Instagram webhook function for the verify token, checking the Settings UI for social/Instagram token configuration, and exploring the social auth callback and deauth endpoints in parallel. I need to search for the browser context tools first since they're deferred, then run the investigation batch before deciding on browser workflows. Let me start with a bash script to locate the key files.

</details>


## 🤖 Claude *(21:28:28)*

O Sovereign deu GO amplo **e** trouxe o fluxo de app-review do Meta ao vivo (está gravando o vídeo agora). O caminho crítico imediato é **desbloquear a submissão do app-review do Instagram** — isso é o que ele está fazendo neste minuto. Vou mapear materialmente o estado atual de tudo antes de tocar em qualquer coisa (Lei 1).

Deixa eu registrar o capítulo e investigar em paralelo.

## 🤖 Claude *(21:28:30)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Meta app-review + roadmap GO",
  "summary": "Sovereign deu GO em todos os pr\u00f3ximos passos (content-intel, AI Act, landing-factory) e trouxe o fluxo de app-review do Instagram ao vivo: precisa de verify token do webhook, UI para colar o IG access token \u2192 Vault, URLs de desautoriza\u00e7\u00e3o/exclus\u00e3o de dados, e assist\u00eancia de browser para configurar casos de uso no console do Meta (app 1714996696595611)."
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Meta app-review + roadmap GO". Continue your current work.'}]
> ```

## 🤖 Claude *(21:28:37)*

<details>
<summary>💭 Thinking Process</summary>

I'm going to run several investigations in parallel—direct file reads, grep searches, exploring with agents, and using browser tools to search for information.

</details>


## 🤖 Claude *(21:28:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== instagram-webhook fn ===\"\nls -la supabase/functions/instagram-webhook/ 2>/dev/null\necho \"=== social-auth-callback fn ===\"\nls -la supabase/functions/social-auth-callback/ 2>/dev/null\necho \"=== deauth / data-deletion fns (grep names) ===\"\nls supabase/functions/ | grep -iE \"deauth|delet|erase|dereg|revoke|data\" || echo \"none matching\"\necho \"=== grep verify_token across functions ===\"\ngrep -rniE \"verify.?token|hub\\.(verify|challenge)|X-Hub\" supabase/functions/instagram-webhook/ 2>/dev/null | head -40",
  "description": "Locate webhook + callback + deauth functions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === instagram-webhook fn ===
> total 12
> drwxrwxr-x   2 gcrUX gcrUX 4096 Jun 23 01:52 .
> drwxrwxr-x 100 gcrUX gcrUX 4096 Jul 17 11:43 ..
> -rw-rw-r--   1 gcrUX gcrUX 3582 Jun 23 01:52 index.ts
> === social-auth-callback fn ===
> total 28
> drwxrwxr-x   2 gcrUX  gcrUX   4096 Jul 16 18:28 .
> drwxrwxr-x 100 gcrUX  gcrUX   4096 Jul 17 11:43 ..
> -rw-rw-r--   1 ubuntu ubuntu 17075 Jul 16 18:28 index.ts
> === deauth / data-deletion fns (grep names) ===
> data-export
> delete-account
> delete-remote-post
> erase-avatar-artifacts
> youtube-data
> === grep verify_token across functions ===
> supabase/functions/instagram-webhook/index.ts:4:// GET  → Meta webhook verification (hub.challenge handshake)
> supabase/functions/instagram-webhook/index.ts:5:// POST → Receive Instagram real-time events (new posts, comments, DMs) — REQUIRES a valid X-Hub-Signature-256
> supabase/functions/instagram-webhook/index.ts:13:    const token     = url.searchParams.get("hub.verify_token");
> supabase/functions/instagram-webhook/index.ts:14:    const challenge = url.searchParams.get("hub.challenge");
> supabase/functions/instagram-webhook/index.ts:16:    const verifyToken = Deno.env.get("INSTAGRAM_WEBHOOK_VERIFY_TOKEN") ?? "mcorch_ig_webhook_2026";
> supabase/functions/instagram-webhook/index.ts:18:    if (mode === "subscribe" && token === verifyToken && challenge) {
> supabase/functions/instagram-webhook/index.ts:29:    // SECURITY: verify Meta's X-Hub-Signature-256 (HMAC-SHA256 of the RAW body with the app secret) BEFORE trusting
> supabase/functions/instagram-webhook/index.ts:38:    const sigHeader = req.headers.get("x-hub-signature-256") ?? "";
> supabase/functions/instagram-webhook/index.ts:41:      console.error("[instagram-webhook] invalid X-Hub-Signature-256 — rejecting");
> ```

## 🤖 Claude *(21:28:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== Settings UI: Instagram/social token BYOK surfaces ===\"\ngrep -rlniE \"instagram|social_credentials|social_accounts|meta_config\" src/components/settings/ 2>/dev/null\necho \"--- component files in settings ---\"\nls src/components/settings/ 2>/dev/null\necho \"=== hooks touching social/instagram creds ===\"\nls src/hooks/ | grep -iE \"social|meta|instagram|apikey|api-key|provider\" 2>/dev/null\necho \"=== list all edge functions (name only) ===\"\nls supabase/functions/ | grep -vE \"^_\" | tr '\\n' ' '",
  "description": "Map Settings UI + hooks for social credentials"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === Settings UI: Instagram/social token BYOK surfaces ===
> src/components/settings/MetaConfigCard.tsx
> --- component files in settings ---
> HiggsfieldConnectorCard.tsx
> McpConnectorsCard.tsx
> MetaConfigCard.tsx
> ProviderKeysCard.tsx
> SocialAppConfigCard.tsx
> === hooks touching social/instagram creds ===
> useConfiguredProviders.ts
> useMetaConfig.ts
> useProviderKeys.ts
> useSocialAccounts.ts
> useSocialAppConfig.ts
> useUserApiKeys.ts
> === list all edge functions (name only) ===
> admin-manage-user [[aeo-audit|aeo-audit]] agent-task-execute aios-chat aios-chat-gateway aios-chat-stream aios-live-proxy aios-sql-bridge analyze-node analyze-sem analyze-seo autonomic-action autopilot-analyze autopilot-cadence-cron autopilot-collect autopilot-run auto-publish avatar-consent avatar-identity-train award-mco-coins cadence-plan cadence-run campaign-run canvas-execute check-post-existence check-subscription check-video-status collect-publication-metrics create-checkout create-portal data-export delete-account delete-remote-post design-job-enqueue detect-viral-moments discover-products embed-mcorch-node erase-avatar-artifacts fetch-trends generate-audio-script generate-carousel generate-content generate-image generate-script-package generate-video generate-video-script generate-voice get-infra-status handle-ml-postback higgsfield-oauth-callback higgsfield-oauth-init higgsfield-webhook ingest-external-asset instagram-webhook intent-execute intent-orchestrate lead-score list-provider-models nurture-cron nurture-dispatch openrouter-swarm optimize-schedule orchestrate-content orchestrate-step pinterest-boards process-affiliate-link publish-channel-variant publish-meta publish-social publish-space-asset publish-space-carousel publish-wordpress refresh-social-token rescue-video reshape-pillar search-constellation seed-global-app-creds self-heal self-optimize social-auth-callback social-auth-init stripe-webhook sync-knowledge-mesh sync-meta-ads test-api-key tiktok-login-callback tiktok-login-init tiktok-login-session trigger-embeddings trigger-ingest tts-speak veo-poll video-render video-render-poll video-repurpose-run whatsapp-webhook youtube-data
> ```

## 🤖 Claude *(21:28:44)*


🛠️ **Tool Call**: `ToolSearch`
```json
{
  "query": "select:mcp__claude-in-chrome__list_connected_browsers,mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__read_page,mcp__claude-in-chrome__computer",
  "max_results": 5
}
```

> **Tool Result (ToolSearch)** - ✅ Success
>
> ```
> [{'type': 'tool_reference', 'tool_name': 'mcp__claude-in-chrome__list_connected_browsers'}, {'type': 'tool_reference', 'tool_name': 'mcp__claude-in-chrome__tabs_context_mcp'}, {'type': 'tool_reference', 'tool_name': 'mcp__claude-in-chrome__navigate'}, {'type': 'tool_reference', 'tool_name': 'mcp__claude-in-chrome__read_page'}, {'type': 'tool_reference', 'tool_name': 'mcp__claude-in-chrome__computer'}]
> ```

## 🤖 Claude *(21:29:02)*

<details>
<summary>💭 Thinking Process</summary>

I'm identifying the webhook verification token setup—the environment variable defaults to `mcorch_ig_webhook_2026` unless overridden in the vault, so I need to check whether that's actually configured. I'm also looking at where these settings surface in the interface.

Now I need to trace through the webhook handler to understand the verify token and signature validation, then check the Meta config card and hooks to see where the long-lived Instagram access token gets stored—that's the token Meta's app review flow generates and needs a place to be pasted in. Now I'm going to check the Meta configuration component, the custom hook for managing that config, and search across the codebase for Meta's deauthorization and data deletion callbacks along with signed request handling. I also need to see what browsers are currently connected.

</details>


## 🤖 Claude *(21:29:03)*

Peguei os fatos-chave. **Verify token do webhook** = `INSTAGRAM_WEBHOOK_VERIFY_TOKEN` (default `mcorch_ig_webhook_2026`). Settings tem `MetaConfigCard`/`SocialAppConfigCard`. Existem `data-export`/`delete-account`, mas preciso confirmar se há o **contrato de callback do Meta** (deauthorize + data-deletion via `signed_request`). Aprofundando + checando o browser conectado.

## 🤖 Claude *(21:29:04)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/instagram-webhook/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 2	import { hmacSha256Hex, timingSafeEqual } from "../_shared/oauth-state.ts";
> 3	
> 4	// GET  → Meta webhook verification (hub.challenge handshake)
> 5	// POST → Receive Instagram real-time events (new posts, comments, DMs) — REQUIRES a valid X-Hub-Signature-256
> 6	
> 7	Deno.serve(async (req) => {
> 8	  const url = new URL(req.url);
> 9	
> 10	  // ── Verification handshake (Meta calls GET with hub params) ───────────────
> 11	  if (req.method === "GET") {
> 12	    const mode      = url.searchParams.get("hub.mode");
> 13	    const token     = url.searchParams.get("hub.verify_token");
> 14	    const challenge = url.searchParams.get("hub.challenge");
> 15	
> 16	    const verifyToken = Deno.env.get("INSTAGRAM_WEBHOOK_VERIFY_TOKEN") ?? "mcorch_ig_webhook_2026";
> 17	
> 18	    if (mode === "subscribe" && token === verifyToken && challenge) {
> 19	      console.log("Instagram webhook verified ✅");
> 20	      return new Response(challenge, { status: 200 });
> 21	    }
> 22	
> 23	    console.error("Webhook verification failed", { mode, token });
> 24	    return new Response("Forbidden", { status: 403 });
> 25	  }
> 26	
> 27	  // ── Event notifications (Meta calls POST) ─────────────────────────────────
> 28	  if (req.method === "POST") {
> 29	    // SECURITY: verify Meta's X-Hub-Signature-256 (HMAC-SHA256 of the RAW body with the app secret) BEFORE trusting
> 30	    // any event. Without it, anyone could POST forged Instagram events (data poisoning of infra_health_logs and any
> 31	    // future action this dispatches). Fail-closed: missing secret or bad/absent signature → 403, no processing.
> 32	    const appSecret = Deno.env.get("INSTAGRAM_APP_SECRET") ?? Deno.env.get("META_APP_SECRET");
> 33	    if (!appSecret) {
> 34	      console.error("[instagram-webhook] app secret not configured — rejecting");
> 35	      return new Response("Forbidden", { status: 403 });
> 36	    }
> 37	    const raw = await req.text();
> 38	    const sigHeader = req.headers.get("x-hub-signature-256") ?? "";
> 39	    const expected = `sha256=${await hmacSha256Hex(appSecret, raw)}`;
> 40	    if (!timingSafeEqual(sigHeader, expected)) {
> 41	      console.error("[instagram-webhook] invalid X-Hub-Signature-256 — rejecting");
> 42	      return new Response("Forbidden", { status: 403 });
> 43	    }
> 44	
> 45	    let body: { entry?: unknown[] } | null = null;
> 46	    try { body = JSON.parse(raw); } catch { body = null; }
> 47	    if (!body) return new Response("Bad Request", { status: 400 });
> 48	
> 49	    console.log("Instagram webhook event:", JSON.stringify(body));
> 50	
> 51	    // Log to Supabase for debugging — non-blocking
> 52	    const admin = createClient(
> 53	      Deno.env.get("SUPABASE_URL")!,
> 54	      (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!
> 55	    );
> 56	
> 57	    const entries: any[] = body.entry ?? [];
> 58	    for (const entry of entries) {
> 59	      const changes: any[] = entry.changes ?? [];
> 60	      for (const change of changes) {
> 61	        // Future: handle new media, comments, mentions
> 62	        console.log(`Instagram event | field=${change.field} | value=${JSON.stringify(change.value)}`);
> 63	
> 64	        if (change.field === "mentions" || change.field === "comments") {
> 65	          await admin.from("infra_health_logs").insert({
> 66	            service: "instagram-webhook",
> 67	            status: "event",
> 68	            metadata: { field: change.field, value: change.value, ig_user_id: entry.id },
> 69	          }).catch(() => { /* non-critical */ });
> 70	        }
> 71	      }
> 72	    }
> 73	
> 74	    return new Response("EVENT_RECEIVED", { status: 200 });
> 75	  }
> 76	
> 77	  return new Response("Method Not Allowed", { status: 405 });
> 78	});
> 79	
> ```

## 🤖 Claude *(21:29:05)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/settings/MetaConfigCard.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useState, useEffect } from "react";
> 2	import { useMetaConfig } from "@/hooks/useMetaConfig";
> 3	import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
> 4	import { Input } from "@/components/ui/input";
> 5	import { Button } from "@/components/ui/button";
> 6	import { Label } from "@/components/ui/label";
> 7	import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
> 8	import { toast } from "sonner";
> 9	import { Share2, Save, Loader2, ChevronDown, AlertTriangle, CheckCircle2, Trash2 } from "lucide-react";
> 10	import { Instagram, Facebook } from "@/components/icons/brand-icons";
> 11	
> 12	/**
> 13	 * Meta Integration (Facebook Page + Instagram Business) — BYOK credential card.
> 14	 * Display-only: all state/mutations live in useMetaConfig. Token fields are write-only
> 15	 * (column-REVOKE'd server-side) — never pre-filled. SOP: docs/processes/[[meta-credential-resolution|meta-credential-resolution]].md.
> 16	 */
> 17	export function MetaConfigCard() {
> 18	  const { status, isLoading, upsertConfig, disconnect, connected, needsReauth, expiringSoon } = useMetaConfig();
> 19	
> 20	  const [form, setForm] = useState({
> 21	    long_lived_token: "",
> 22	    instagram_business_account_id: "",
> 23	    page_id: "",
> 24	    page_name: "",
> 25	    page_access_token: "",
> 26	    token_expires_at: "",
> 27	  });
> 28	  const [pageOpen, setPageOpen] = useState(false);
> 29	
> 30	  // Populate non-secret fields from status (token fields stay empty — write-only).
> 31	  useEffect(() => {
> 32	    if (!status) return;
> 33	    setForm((p) => ({
> 34	      ...p,
> 35	      instagram_business_account_id: status.instagram_business_account_id ?? "",
> 36	      token_expires_at: status.token_expires_at ? status.token_expires_at.slice(0, 10) : "",
> 37	    }));
> 38	  }, [status]);
> 39	
> 40	  const handleSave = async () => {
> 41	    if (!form.long_lived_token.trim()) {
> 42	      toast.error("Cole o token de longa duração da Meta antes de salvar.");
> 43	      return;
> 44	    }
> 45	    try {
> 46	      await upsertConfig.mutateAsync({
> 47	        long_lived_token: form.long_lived_token.trim(),
> 48	        instagram_business_account_id: form.instagram_business_account_id.trim() || undefined,
> 49	        page_id: form.page_id.trim() || undefined,
> 50	        page_name: form.page_name.trim() || undefined,
> 51	        page_access_token: form.page_access_token.trim() || undefined,
> 52	        token_expires_at: form.token_expires_at ? new Date(form.token_expires_at).toISOString() : undefined,
> 53	      });
> 54	      toast.success("Meta conectada com sucesso!");
> 55	      setForm((p) => ({ ...p, long_lived_token: "", page_access_token: "" }));
> 56	    } catch (err: unknown) {
> 57	      toast.error("Erro ao salvar Meta: " + (err instanceof Error ? err.message : String(err)));
> 58	    }
> 59	  };
> 60	
> 61	  const handleDisconnect = async () => {
> 62	    try {
> 63	      await disconnect.mutateAsync();
> 64	      toast.success("Meta desconectada.");
> 65	    } catch (err: unknown) {
> 66	      toast.error("Erro ao desconectar: " + (err instanceof Error ? err.message : String(err)));
> 67	    }
> 68	  };
> 69	
> 70	  return (
> 71	    <Card className="border-border/50 bg-card/50 backdrop-blur-sm">
> 72	      <CardHeader>
> 73	        <CardTitle className="flex items-center gap-2">
> 74	          <Share2 className="h-5 w-5 text-blue-500" />
> 75	          Meta — Facebook & Instagram
> 76	          {connected && (
> 77	            <span className="ml-2 inline-flex items-center gap-1 rounded-full bg-emerald-500/15 px-2 py-0.5 text-xs text-emerald-400">
> 78	              <CheckCircle2 className="h-3 w-3" /> Conectado{expiringSoon ? " · expira em breve" : ""}
> 79	            </span>
> 80	          )}
> 81	        </CardTitle>
> 82	        <CardDescription>
> 83	          Conecte sua conta Meta para publicar no Facebook Page e Instagram Business pelo pipeline.
> 84	          Cole o <strong>token de longa duração</strong> (60 dias) gerado no Graph API Explorer / Business Suite.
> 85	        </CardDescription>
> 86	      </CardHeader>
> 87	      <CardContent className="space-y-4">
> 88	        {needsReauth && (
> 89	          <div className="flex items-start gap-2 rounded-md border border-destructive/40 bg-destructive/10 p-3 text-sm text-destructive">
> 90	            <AlertTriangle className="h-4 w-4 mt-0.5 shrink-0" />
> 91	            <span>
> 92	              Token expirado ou revogado. Gere um novo token de longa duração e cole abaixo para reconectar.
> 93	            </span>
> 94	          </div>
> 95	        )}
> 96	
> 97	        {isLoading ? (
> 98	          <div className="flex justify-center p-6">
> 99	            <Loader2 className="h-6 w-6 animate-spin text-primary" />
> 100	          </div>
> 101	        ) : (
> 102	          <>
> 103	            <div className="space-y-2">
> 104	              <Label htmlFor="meta_long_lived_token">Token de Longa Duração (User Token)</Label>
> 105	              <Input
> 106	                id="meta_long_lived_token" name="meta_long_lived_token" type="password"
> 107	                autoComplete="new-password" data-lpignore="true" data-1p-ignore="true"
> 108	                placeholder={status?.id ? "•••••••• (salvo — cole para substituir)" : "EAAG..."}
> 109	                value={form.long_lived_token}
> 110	                onChange={(e) => setForm((p) => ({ ...p, long_lived_token: e.target.value }))}
> 111	                className="font-mono text-sm"
> 112	              />
> 113	              <p className="text-xs text-muted-foreground">
> 114	                Nunca exibido de volta por segurança (column-grant). Cole novamente para atualizar.
> 115	              </p>
> 116	            </div>
> 117	
> 118	            <div className="space-y-2">
> 119	              <Label htmlFor="meta_ig_id" className="flex items-center gap-2">
> 120	                <Instagram className="h-3.5 w-3.5 text-pink-400" /> Instagram Business Account ID
> 121	              </Label>
> 122	              <Input
> 123	                id="meta_ig_id" name="meta_ig_id" autoComplete="off"
> 124	                placeholder="17841400000000000"
> 125	                value={form.instagram_business_account_id}
> 126	                onChange={(e) => setForm((p) => ({ ...p, instagram_business_account_id: e.target.value }))}
> 127	                className="font-mono text-sm"
> 128	              />
> 129	              <p className="text-xs text-muted-foreground">Necessário para publicar no Instagram (FR-META-002).</p>
> 130	            </div>
> 131	
> 132	            <div className="space-y-2">
> 133	              <Label htmlFor="meta_token_expires">Expiração do Token (opcional)</Label>
> 134	              <Input
> 135	                id="meta_token_expires" name="meta_token_expires" type="date"
> 136	                value={form.token_expires_at}
> 137	                onChange={(e) => setForm((p) => ({ ...p, token_expires_at: e.target.value }))}
> 138	                className="text-sm w-fit"
> 139	              />
> 140	              <p className="text-xs text-muted-foreground">Usado para alertar reautenticação antes de expirar.</p>
> 141	            </div>
> 142	
> 143	            <Collapsible open={pageOpen} onOpenChange={setPageOpen}>
> 144	              <CollapsibleTrigger asChild>
> 145	                <Button variant="ghost" size="sm" className="gap-2 text-muted-foreground hover:text-foreground -ml-1">
> 146	                  <ChevronDown className={`h-4 w-4 transition-transform ${pageOpen ? "rotate-180" : ""}`} />
> 147	                  <Facebook className="h-3.5 w-3.5 text-blue-500" /> Página do Facebook (opcional)
> 148	                </Button>
> 149	              </CollapsibleTrigger>
> 150	              <CollapsibleContent className="space-y-4 pt-2">
> 151	                <div className="space-y-2">
> 152	                  <Label htmlFor="meta_page_id">Page ID</Label>
> 153	                  <Input
> 154	                    id="meta_page_id" name="meta_page_id" autoComplete="off" placeholder="1234567890"
> 155	                    value={form.page_id}
> 156	                    onChange={(e) => setForm((p) => ({ ...p, page_id: e.target.value }))}
> 157	                    className="font-mono text-sm"
> 158	                  />
> 159	                </div>
> 160	                <div className="space-y-2">
> 161	                  <Label htmlFor="meta_page_name">Nome da Página</Label>
> 162	                  <Input
> 163	                    id="meta_page_name" name="meta_page_name" autoComplete="off" placeholder="Minha Página"
> 164	                    value={form.page_name}
> 165	                    onChange={(e) => setForm((p) => ({ ...p, page_name: e.target.value }))}
> 166	                    className="text-sm"
> 167	                  />
> 168	                </div>
> 169	                <div className="space-y-2">
> 170	                  <Label htmlFor="meta_page_token">Page Access Token</Label>
> 171	                  <Input
> 172	                    id="meta_page_token" name="meta_page_token" type="password"
> 173	                    autoComplete="new-password" data-lpignore="true" data-1p-ignore="true"
> 174	                    placeholder="EAAG... (token perpétuo da página)"
> 175	                    value={form.page_access_token}
> 176	                    onChange={(e) => setForm((p) => ({ ...p, page_access_token: e.target.value }))}
> 177	                    className="font-mono text-sm"
> 178	                  />
> 179	                  <p className="text-xs text-muted-foreground">Necessário para publicar no feed do Facebook (FR-META-003).</p>
> 180	                </div>
> 181	              </CollapsibleContent>
> 182	            </Collapsible>
> 183	          </>
> 184	        )}
> 185	      </CardContent>
> 186	      <CardFooter className="flex justify-between border-t border-border/50 pt-6">
> 187	        {status?.id ? (
> 188	          <Button variant="ghost" size="sm" onClick={handleDisconnect} disabled={disconnect.isPending} className="gap-2 text-muted-foreground hover:text-destructive">
> 189	            {disconnect.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Trash2 className="h-4 w-4" />}
> 190	            Desconectar
> 191	          </Button>
> 192	        ) : <span />}
> 193	        <Button onClick={handleSave} disabled={isLoading || upsertConfig.isPending} className="gap-2">
> 194	          {upsertConfig.isPending ? <Loader2 className="h-4 w-4 animate-spin" /> : <Save className="h-4 w-4" />}
> 195	          Salvar Meta
> 196	        </Button>
> 197	      </CardFooter>
> 198	    </Card>
> 199	  );
> 200	}
> 201	
> ```

## 🤖 Claude *(21:29:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== signed_request / deauthorize / data-deletion contract (Meta callbacks) ===\"\ngrep -rniE \"signed_request|deauthorize|data_deletion|data-deletion|deletion_request|confirmation_code\" supabase/functions/ 2>/dev/null | head -30\necho \"=== what delete-account + data-export do (headers) ===\"\nhead -25 supabase/functions/delete-account/index.ts 2>/dev/null\necho \"--- data-export head ---\"\nhead -20 supabase/functions/data-export/index.ts 2>/dev/null\necho \"=== INSTAGRAM_WEBHOOK_VERIFY_TOKEN in .env? ===\"\ngrep -iE \"INSTAGRAM_WEBHOOK|WEBHOOK_VERIFY\" .env 2>/dev/null && echo \"FOUND in .env\" || echo \"NOT in .env (uses default or vault secret)\"",
  "description": "Check Meta callback contract + delete fns + verify token env"
}
```

## 🤖 Claude *(21:29:09)*


🛠️ **Tool Call**: `mcp__claude-in-chrome__list_connected_browsers`
```json
{}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === signed_request / deauthorize / data-deletion contract (Meta callbacks) ===
> === what delete-account + data-export do (headers) ===
> import { createClient } from "https://esm.sh/@supabase/supabase-js@2.49.1";
> 
> const corsHeaders = {
>   "Access-Control-Allow-Origin": "*",
>   "Access-Control-Allow-Methods": "POST, OPTIONS",
>   "Access-Control-Allow-Headers":
>     "authorization, x-client-info, apikey, content-type",
> };
> 
> Deno.serve(async (req) => {
>   if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 
>   const authHeader = req.headers.get("Authorization");
>   if (!authHeader?.startsWith("Bearer ")) {
>     return new Response(JSON.stringify({ error: "Unauthorized" }), {
>       status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" },
>     });
>   }
> 
>   try {
>     const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
>     const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 
>     const userClient = createClient(supabaseUrl, (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!, {
>       global: { headers: { Authorization: authHeader } },
> --- data-export head ---
> import { createClient } from "https://esm.sh/@supabase/supabase-js@2.49.1";
> 
> const corsHeaders = {
>   "Access-Control-Allow-Origin": "*",
>   "Access-Control-Allow-Methods": "POST, OPTIONS",
>   "Access-Control-Allow-Headers":
>     "authorization, x-client-info, apikey, content-type",
> };
> 
> Deno.serve(async (req) => {
>   if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 
>   const authHeader = req.headers.get("Authorization");
>   if (!authHeader?.startsWith("Bearer ")) {
>     return new Response(JSON.stringify({ error: "Unauthorized" }), {
>       status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" },
>     });
>   }
> 
>   try {
> === INSTAGRAM_WEBHOOK_VERIFY_TOKEN in .env? ===
> NOT in .env (uses default or vault secret)
> ```

> **Tool Result (mcp__claude-in-chrome__list_connected_browsers)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': '[{"deviceId":"f5d86c64-78de-49b7-a6a2-f68f88bc3573","name":"Browser 1","osPlatform":"Windows","connectedAt":1784322442098,"isLocal":true}]'}]
> ```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-16 - d6ec7e6b-7ebd-46be-9065-173b91242b97]]
> * **Próxima Sessão**: [[2026-07-17 - Configure Pinterest API credentials and global auth keys]]
%% --- TIMELINE END --- %%

# Automatizar geração e agendamento de conteúdo para redes sociais
**Date:** 2026-06-17 | **Session ID:** `21b2d649-94ad-4468-9821-20f76eae70a3`

---

## 👤 User *(20:29:26)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(20:29:26)*

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


## 🤖 Claude *(20:29:29)*


## 🤖 Claude *(20:29:29)*

I'll execute the ShakeHands /handson pick-up protocol. Starting with all pre-flight checks in parallel.

## 🤖 Claude *(20:29:30)*


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
> 776687f chore(sprint): registra v6.41.0 — Unified Sensorial Canvas (Epsilon V9) Fases 3.1-3.4
> d84b806 docs(handoff): seal Unified Sensorial Canvas (Epsilon V9) — AGI→ASI ref + emenda BoK + Fases 3.1-3.4
> 08b36eb docs(readme): v6.41.0 — Unified Sensorial Canvas (Epsilon V9) Code+Memory+Black Hole R3F
> 769acb1 feat(universe): herda Black Hole como backdrop compartilhado — Fase 3.4
> 38d9760 fix(universe): memória glowing (aditivo + maior) + guarda mesh.count
> 4940b4d feat(universe): rede de memória em R3F (GraphRAG cymatics shell) — Fase 3.3
> d832084 feat(universe): rede de código em R3F (InstancedMesh + Louvain) — Fase 3.2
> ```

## 🤖 Claude *(20:29:31)*


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
>  M proof-manifest.json
> ```

> **Tool Result (Unknown Tool)** - ✅ Success
>
> ```
> ⚠️ scratch/ has files
> ```

## 🤖 Claude *(20:29:31)*


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
>  proof-manifest.json | 2 +-
>  1 file changed, 1 insertion(+), 1 deletion(-)
> ```

## 🤖 Claude *(20:29:32)*


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

## 🤖 Claude *(20:29:33)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"",
  "description": "Docker mesh container health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 17 hours (healthy)
> mcorch_claude_mem: Up 2 days (healthy)
> mcorch_chroma: Up 2 days (healthy)
> ---
> mega-brain-dashboard: Up 2 days
> mega-brain-webhook: Up 2 days (healthy)
> mega-brain-daemon: Up 2 days (healthy)
> ```

## 🤖 Claude *(20:29:34)*


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
> {"nanosecond heartbeat":1781728174556241534}
> ```

## 🤖 Claude *(20:29:35)*


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
> viral-daily-canvas
> viralmind
> vision-mcp
> ```

## 🤖 Claude *(20:29:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l HANDOFF.md",
  "description": "HANDOFF total lines"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 8028 HANDOFF.md
> ```

## 🤖 Claude *(20:29:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls scratch/ 2>/dev/null && echo \"\u26a0\ufe0f scratch/ has files\" || echo \"scratch/ clean \u2705\"",
  "description": "Scratch directory check"
}
```

## 🤖 Claude *(20:29:40)*


## 🤖 Claude *(20:29:41)*


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
> 14	## Session Seal — Unified Sensorial Canvas (Phase Epsilon V9): AGI→ASI ref + emenda BoK + Fases 3.1-3.4 (2026-06-17)
> 15	
> 16	`/handson` → conversa estratégica (Model Council; plugin `claude-code-setup`; paper *From AGI to ASI*) → diretiva arquitetural **Unified Core Sensorial Canvas**. Sessão de alta densidade em arco Closed-Loop: fundamentação (AGI→ASI) → auditoria material dos clusters → gate BoK → 4 fases de implementação R3F → verificação ocular E2E. Nada foi codado antes de (a) auditar os clusters e (b) selar a emenda BoK.
> 17	
> 18	**O que foi entregue:**
> 19	1. **Referência AGI→ASI + checklist Via 4:** paper DeepMind (arXiv 2606.12683, Legg/Hutter/Leibo et al.) lido inteiro (57p, extração PyMuPDF) + selado como nó `architecture` **`a576216e`** (edge `INFORMS` → `bok-scribe-seal-openclaw-v1` **`d2827191`**) + checklist de design da **Via 4** (`.claude/context/agi-asi-via4-design-checklist.md`) + plano de trabalho (`.claude/context/unified-core-sensorial-canvas-plan.md`). Tese: o MCORCH é a Via 4 (formação de grupo de agentes) instanciada na camada de aplicação.
> 20	2. **Auditoria de clusters (Lei 1):** Louvain clustering = **REAL/VIVO** (client-side `graphology-communities-louvain@2.0.2` em `useConstellationSigma.ts:227`, 8.5k nós / 8.8k arestas); squad-territory coloring = **MORTO** (`crew_module_ownership` = 0 linhas → fallback sempre cai no Louvain) + heurístico (`inferSquad` keyword-match). **Decisão B = PODAR** (Louvain é o esquema oficial; `OTD-SQUAD-OWNERSHIP-REVIVAL` registra revival por sinal real).
> 21	3. **Emenda BoK (gate Sovereign-eleito sobre override):** `mcorch-constellation` PRD/FRD/SDD estendidos — **PR-025 + FR-043..049 + NFR-023/024 + SDD §9** (reconciliação Sigma→R3F = graphology cérebro / R3F corpo; OTDs SQUAD-OWNERSHIP-REVIVAL/SYNAPSE-EMBEDDING/UCANVAS-PERF).
> 22	4. **Fases 3.1-3.4 (R3F, commits granulares, não-quebrante, 3 páginas legadas preservadas):** scaffold rota `/dashboard/universe` + `useUnifiedCanvasStore` + shell 72/28 · **Code Network** `InstancedMesh` colorido pelas comunidades Louvain reais (plano equatorial) · **Memory Network** GraphRAG como casca cymatics (fibonacci, glow aditivo) · **Black Hole** (`MegaBrainVisualizer`) herdado como backdrop compartilhado (z-0) atrás do Canvas de redes transparente (z-10).
> 23	5. **E2E ocular (à prova de CF):** build → `vite preview` local → sessão do Usuário Zero injetada (`gen-user-session.ts`) → agent-browser nos **3 modos** (Universo/Matrix/Memória). Telemetria real conferida (8.560 nós / 8.816 arestas / ~733 comunidades / 159 pensamentos). A "esfera órfã" foi **desmistificada = spinner de loading** (`Loader2`, `.animate-spin` 1→0 ao carregar), não bug; glow fraco da memória corrigido (blending aditivo).
> 24	
> 25	**ORO:** Operator=MCORCH Master Execution Agent · Reviewer=Sovereign (escolheu **emenda BoK** sobre override; autorizou commit direto na `main`) · Owner=Sovereign (3 páginas de produção; legados intactos como backup até paridade — passo 3.9).
> 26	
> 27	| Verificação (material) | Resultado |
> 28	|---|---|
> 29	| Auditoria de clusters | ✅ Louvain VIVO (`useConstellationSigma.ts:227`) · `crew_module_ownership` 0 rows (REST count) |
> 30	| Emenda BoK | ✅ PR-025/FR-043..049/NFR-023-024/SDD §9 nos 3 docs (grep) |
> 31	| Fases 3.1-3.4 | ✅ tsc 0 em cada passo · build chunk `UnifiedCanvasPage-BY8dIJXM.js` 8635B |
> 32	| E2E ocular | ✅ autenticado em `/dashboard/universe` · Black Hole + Code(8.560) + Memory(159) · 3 modos · spinner identificado |
> 33	| Commits (8) | `4f97ebf` AGI ref · `19a7b83` BoK · `210b90d` 3.1 · `d832084` 3.2 · `4940b4d` 3.3 · `38d9760` fix · `769acb1` 3.4 · `08b36eb` readme |
> 34	| Mesh | ✅ AGI ref `a576216e` + handoff `5225ff03` (ambos 768d) |
> 35	
> 36	### Survival Laws Self-audit
> 37	```
> 38	Law 1 (Materiality): ✅ Auditoria provada por REST count (0 rows) + grep de código (:227); E2E ocular real (screenshots, não auto-declarado) — a "esfera órfã" identificada como spinner via `.animate-spin` 1→0, não fabriquei explicação. Fase 5c executada. Embed do handoff via `{node_id}` (record-drift conhecido) → 768d OK.
> 39	Law 2 (Process): ✅ Auditoria material ANTES de codar; emenda BoK (gate) ANTES da Fase 3; plano documentado. Canvas = alteração de UI → gate E2E aplicado.
> 40	Law 3 (Pruning): ✅ Sessão longa empacotada (conversa→ref→audit→gate→4 fases→E2E) sem selar cedo (calibração 1M); Decisão B = poda do squad-coloring morto.
> 41	Law 4 (ORO): ✅ Triplet declarado; gate de governança decidido pelo Sovereign (emenda vs override); commit-na-main autorizado explicitamente.
> 42	```
> 43	
> 44	## Session Seal — Vision MCP Fatia 3 remainder: PAT UI + Claude Code install + Plugin/Registry + caps de custo (2026-06-17)
> 45	
> 46	`/handson` → o Sovereign puxou as 3 frentes do roadmap vision-mcp ("continue"). Closed-Loop respeitado — mapeei o contrato BoK vivo (FR-VM-003/011 · DD-VM-003 · OTD-VM-024/025) ANTES de codar. Tudo o que restava da Fatia 3 até o **limite não-gated** foi entregue e provado material; o que sobra é gated (OAuth browser-flow → 1º tenant externo), deferido (`mistral`/`vision.ocr`) ou Sovereign-side (publish DNS, Stripe live, Resend, atribuição ML).
> 47	
> 48	**O que foi entregue:**
> 49	1. **PAT issuance UI + install no Claude Code (FR-VM-003):** `useMcpTokens` gera PAT **100% client-side** (CSPRNG 32B → base64url → `mcorch_pat_…`; **SHA-256 só do hash** persiste, byte-idêntico ao verifier do container; plaintext exibido **uma vez**), lista e revoga (UPDATE `revoked_at`) — tudo RLS-own. `useVisionMcp` (estado do conector). `McpConnectorsCard` em **Settings → Connectors** (URL copiável + snippet `.mcp.json` + escopos + reveal-once + download do plugin). `.mcp.json` ganhou o bloco `vision-mcp` (`Bearer ${VISION_MCP_PAT}` — sem segredo versionado). `types.ts` regenerado do schema vivo (purely additive: `mcp_access_tokens`/`vision_jobs`/`vision_artifacts`). PAT do Usuário Zero mintado e gravado em `.env` (gitignored).
> 50	2. **Plugin Zip + MCP Registry (FR-VM-011):** `packages/vision-mcp-plugin/` (.claude-plugin + .mcp.json + 3 skills PT-BR `/vision-essence` `/reference-brief` `/competitive-vision`) → `public/plugins/vision-mcp-plugin-1.0.0.zip` (build script reprodutível). Manifesto `packages/vision-mcp-core/server.json` (`com.mcorch/vision-mcp`, schema oficial **2025-12-11**, remote `streamable-http` → `mcp.mcorch.com/mcp`, header Bearer PAT) + runbook de publish (DNS TXT `v=MCPv1` em `mcorch.com` = **gate Sovereign**).
> 51	3. **OTD-VM-024 — motor dual selado:** blueprint **§8-A** sela Gemini Google-Search grounding como 2º motor legítimo do `deepsearch.run` (Firecrawl permanece no `deepsearch.scrape`), fundamentado em ai.google.dev/gemini-api/docs/google-search; `source_allowlist` best-effort no run (redirect `vertexaisearch`) é propriedade aceita. SDD OTD-VM-024 → **FECHADA**.
> 52	4. **Caps de custo (DD-VM-003 / OTD-VM-025):** `deepsearch.run` ganhou cap de `planned_units` **per-plano** (10/25/50, resolvido da subscription, fail-soft→starter) + **cap diário per-tenant** (25/100/500, conta `vision_jobs` charged>0 do dia, BYOK bypassa, fail-open em erro de contagem) — throw **antes** do deduct. `validation_failed` agora carrega `field`+`message` (FRD §4.4). SDD OTD-VM-025 → cap diário implementado.
> 53	5. **Anticorpo (Lei 2):** SOP `docs/processes/vision-mcp-connector-install.md` (Operator/Sequence/Gates/Recovery/Success do fluxo de install + gotcha do CF bot-challenge no curl cru) + Key Files registrados em CLAUDE.md.
> 54	
> 55	**ORO:** Operator=MCORCH Agent · Reviewer=Sovereign + `/security-review` independente (SAFE) · Owner=Sovereign (PAT = credencial que gasta carteira FM-VM-06; caps = proteção financeira da chave-plataforma).
> 56	
> 57	| Verificação (material) | Resultado |
> 58	|---|---|
> 59	| **Handshake PAT pela URL pública** `mcp.mcorch.com` | ✅ `initialize` + `tools/list`(7) + `mesh_search` tenant-scoped `scope:user:<sub>+system` `isError=false` · revoke HTTP 204 |
> 60	| Plugin Zip servido | ✅ origem nginx **200 `application/zip` 4650B** byte-idêntico (CF 403 no curl público = bot-challenge; browser passa) |
> 61	| Caps de custo (smoke LIVE zero-cost) | ✅ **3/3** — C1 per-plano over→`validation_failed` `1..10` · C2 boundary 10→`insufficient_balance` · C3 daily→`daily_cap_reached` rate_limit, balance intacto, sem 26º job |
> 62	| Testes / tsc | ✅ pkg **55/55** (+5 caps) · tsc 0 (root+pkg) |
> 63	| Container | ✅ rebuild→image `7710b832` healthy · `/health` 7 tools |
> 64	| `server.json` | ✅ JSON válido + required fields (`$schema`/name/description/version/remotes) |
> 65	| Revisão | ✅ `/security-review` independente **SAFE** (0 achados) — sub/encodeURIComponent, RLS-own, CSPRNG, sem secret exposto |
> 66	| Commits | `08739b3` (PAT UI+install) · `2f3e4df` (Plugin Zip) · `d3b8aeb` (caps) · `74c7a27` (OTD-VM-024) · `54151e8` (SOP+KeyFiles) · `ee0bc63` (Registry) · `cf5ef7c` (readme) (+ handoff) |
> 67	
> 68	### Survival Laws Self-audit
> 69	```
> 70	Law 1 (Materiality): ✅ Cada claim provada — handshake MCP+PAT REAL pela URL pública (não loopback/browser), smoke 3/3 zero-cost contra o container SERVIDO, origem nginx 200 byte-idêntico, pkg 55/55, /security-review independente SAFE. Embed do handoff node falhou no 1º payload (param drift `{record}`→`{node_id}`) e foi re-emitido + verificado (embedded=true). Fase 5c executada.
> 71	Law 2 (Process): ✅ Mapeei o contrato BoK vivo antes de codar (pegou que per-plan/daily caps fechavam OTD-VM-025); SOP de install (anticorpo) escrita ANTES do seal; caps/PAT são extensões de features com SOP existente (deepsearch-async / pat-and-erasure). Sem migration nova (types regen ≠ migration).
> ```

## 🤖 Claude *(20:29:42)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 7628,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 7628	  6. Return: {success, original_url, resolved_url, affiliate_url, self_healed, link_id}
> 7629	
> 7630	ContentLibraryPage monetization flow:
> 7631	  Card (text, body contains mercadolivre.com.br)
> 7632	    └── DropdownMenu → "Monetizar Links ML"
> 7633	          → handleMonetizeLinks(item):
> 7634	               match(ML_URL_RE) → unique URLs
> 7635	               for url of unique:
> 7636	                 POST process-affiliate-link → affiliate_url
> 7637	                 body.split(url).join(affiliate_url)
> 7638	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 7639	          → Badge 💰 ML (emerald) exibido após monetização
> 7640	```
> 7641	
> 7642	---
> 7643	
> 7644	## Pending Actions (Commercial Launch)
> 7645	
> 7646	### CRITICAL — Must complete before first client
> 7647	
> 7648	🌌. **[EM ANDAMENTO — Phase Epsilon V9] Unified Sensorial Canvas — Fases 3.5-3.10** — Fases 3.1-3.4 ✅ (scaffold rota/store/shell 72-28 + Code Network R3F InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; E2E ocular nos 3 modos; commits `210b90d`/`d832084`/`4940b4d`/`38d9760`/`769acb1`). **Restam:** **3.5** Sinapses inter-rede (arestas **REAIS** de `mcorch_edges` cruzando código↔memória, lit só no modo Universo — nunca fabricar) · **3.6** fly-to (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.7** layout/perf (`OTD-UCANVAS-PERF` — a query do código leva **~30s** com 2 canvases; considerar Louvain em Web Worker / streaming do grafo / lazy do backdrop) · **3.8** executar a poda do squad-coloring (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`. BoK selada (PR-025 · FR-043..049 · NFR-023/024 · SDD §9). **3 páginas legadas (matrix/memory/core-fable) preservadas como backup até 3.9.**
> 7649	
> 7650	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 7651	
> 7652	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 7653	
> 7654	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 7655	
> 7656	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 7657	
> 7658	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 7659	
> 7660	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 7661	
> 7662	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 7663	
> 7664	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 7665	
> 7666	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 7667	
> 7668	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 7669	   ```bash
> 7670	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 7671	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 7672	   ```
> 7673	
> 7674	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 7675	
> 7676	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 7677	
> 7678	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 7679	
> 7680	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 7681	
> 7682	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 7683	
> 7684	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 7685	
> 7686	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 7687	
> 7688	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 7689	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 7690	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 7691	
> 7692	### SOCIAL — Next steps
> 7693	
> 7694	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 7695	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 7696	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 7697	
> 7698	### NON-CRITICAL
> 7699	
> 7700	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 7701	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 7702	- `browserslist` — ✅ updated (2026-04-26)
> 7703	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 7704	
> 7705	### GITNEXUS MCP — Next steps
> 7706	
> 7707	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 7708	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 7709	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 7710	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 7711	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 7712	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 7713	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 7714	
> 7715	### PHASE EPSILON — Next iterations
> 7716	
> 7717	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 7718	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 7719	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 7720	
> 7721	### CORE — Next iterations
> 7722	
> 7723	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 7724	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 7725	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 7726	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 7727	
> 7728	### PHASE DELTA — Next iterations
> 7729	
> 7730	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 7731	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 7732	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 7733	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 7734	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 7735	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 7736	
> 7737	### USUÁRIO ZERO — Checklist de validação
> 7738	
> 7739	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 7740	- ✅ Stripe sandbox secrets no vault
> 7741	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 7742	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 7743	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 7744	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 7745	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 7746	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 7747	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 7748	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 7749	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 7750	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 7751	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 7752	
> 7753	---
> 7754	
> 7755	## Infrastructure
> 7756	
> 7757	| Service | Container | Port | Status |
> 7758	|---------|-----------|------|--------|
> 7759	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 7760	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 7761	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 7762	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 7763	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 7764	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 7765	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 7766	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 7767	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 7768	
> 7769	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 7770	
> 7771	```bash
> 7772	docker compose up -d
> 7773	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 7774	```
> 7775	
> 7776	---
> 7777	
> 7778	## Security Model (Post-Go-Live)
> 7779	
> 7780	| Table | Isolation |
> 7781	|-------|-----------|
> 7782	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 7783	| `mcorch_edges` | Same pattern |
> 7784	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 7785	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 7786	
> 7787	---
> 7788	
> 7789	## Billing Architecture
> 7790	
> 7791	| Decision | Value |
> 7792	|----------|-------|
> 7793	| Canonical billing ledger | `profiles.mco_balance` |
> 7794	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 7795	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 7796	| Orchestration cost | 10 mcoCoins/run |
> 7797	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 7798	| Stripe | Sandbox keys active — swap to live before first client |
> 7799	
> 7800	---
> 7801	
> 7802	## GraphRAG State
> 7803	
> 7804	- **8926 total nodes** (verificado live 2026-06-17 via REST count=exact, unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 7805	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 7806	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 7807	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 7808	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 7809	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 7810	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 7811	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 7812	- HNSW cosine index operational
> 7813	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 7814	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 7815	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 7816	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 7817	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 7818	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 7819	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 7820	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 7821	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 7822	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 7823	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 7824	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 7825	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 7826	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 7827	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 7828	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 7829	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 7830	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 7831	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 7832	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 7833	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 7834	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 7835	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 7836	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 7837	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 7838	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 7839	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 7840	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 7841	
> 7842	### Embedding Model
> 7843	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 7844	Schema: `vector(768)` — HNSW cosine index.
> 7845	
> 7846	### Embedding Pipeline (Autônomo — 2026-05-03)
> 7847	Três camadas eliminam intervenção manual:
> 7848	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 7849	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 7850	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 7851	
> 7852	### Comandos de manutenção da Mesh
> 7853	```bash
> 7854	# Verificar nós sem embedding (deveria retornar array vazio):
> 7855	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 7856	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 7857	
> 7858	# Backfill manual (Bun-native — requer .env):
> 7859	bun run scripts/backfill-embeddings.ts
> 7860	
> 7861	# Backfill de código-fonte nos nós AST:
> 7862	bun run scripts/backfill-node-content.ts
> 7863	
> 7864	# Re-sync AST completo:
> 7865	cd packages/gitnexus-core && npm run sync-mesh
> 7866	
> 7867	# Acompanhar re-ingesta pós-commit:
> 7868	tail -f /tmp/mcorch-ingest.log
> 7869	```
> 7870	
> 7871	---
> 7872	
> 7873	## Video Rescue Protocol
> 7874	
> 7875	When a video generation operation (Google Veo) times out or client disconnects:
> 7876	```bash
> 7877	# Via edge function (production):
> 7878	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 7879	  -H "Authorization: Bearer <user_jwt>" \
> 7880	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 7881	
> 7882	# Via local script (admin/debug):
> 7883	source .env && bun run rescue.ts <operation_id> <content_id>
> 7884	```
> 7885	
> 7886	---
> 7887	
> 7888	## Architecture Pillars
> 7889	
> 7890	| Layer | Implementation |
> 7891	|-------|---------------|
> 7892	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 7893	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 7894	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 7895	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 7896	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 7897	
> 7898	---
> 7899	
> 7900	## Phase Delta — Architecture
> 7901	
> 7902	```
> 7903	OrchestrationPage (full-canvas, p-0)
> 7904	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 7905	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 7906	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 7907	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 7908	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 7909	        ├── nodes/PublishNode.tsx    ← final distribution output
> 7910	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 7911	        └── NodePalette.tsx          ← top toolbar to add nodes
> 7912	
> 7913	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 7914	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 7915	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 7916	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 7917	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 7918	```
> 7919	
> 7920	### Canvas State Architecture (Hybrid)
> 7921	
> 7922	```
> 7923	User interaction → ReactFlow internal state (positions, drag)
> 7924	                         ↓ (debounced 600ms)
> 7925	                   localStorage (positions persist across refresh)
> 7926	                         ↑
> 7927	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 7928	     ↓ (status changes sync to ReactFlow via useEffect)
> 7929	ReactFlow renders visual status (idle/running/done/error/blocked)
> 7930	```
> 7931	
> 7932	## Key Files
> 7933	
> 7934	| Purpose | Path |
> 7935	|---------|------|
> 7936	| Architecture rules | `CLAUDE.md` |
> 7937	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 7938	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 7939	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 7940	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 7941	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 7942	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 7943	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 7944	| **Node types** | `src/components/orchestrator/nodes/` |
> 7945	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 7946	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 7947	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 7948	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 7949	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 7950	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 7951	| Billing utilities | `src/lib/billing.ts` |
> 7952	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 7953	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 7954	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 7955	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 7956	| Video rescue (local) | `rescue.ts` |
> 7957	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 7958	| Backfill script | `scripts/backfill-embeddings.ts` |
> 7959	| Deploy harness | `scripts/harness-deploy.sh` |
> 7960	
> 7961	---
> 7962	
> 7963	## First Client Onboarding Checklist
> 7964	
> 7965	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 7966	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 7967	3. ~~Activate watchdog cron~~ ✅ Done
> 7968	4. ~~Deploy rescue-video function~~ ✅ Done
> 7969	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 7970	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 7971	7. Monitor `infra_health_logs` for first 24h.
> 7972	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 7973	
> 7974	---
> 7975	
> 7976	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 7977	
> 7978	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 7979	
> 7980	| Action | Result |
> 7981	|--------|--------|
> 7982	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 7983	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 7984	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 7985	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 7986	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 7987	
> 7988	| Commit | Conteúdo |
> 7989	|--------|----------|
> 7990	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 7991	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 7992	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 7993	
> 7994	### Arquitetura Matrix Intelligence
> 7995	
> 7996	```
> 7997	ConstellationMatrix (Stabilized Engine)
> 7998	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 7999	  └── NodeDetailsPanel (Tabbed Navigation)
> 8000	        ├── Tab Meta: Neighbor exploration + Net Context
> 8001	        ├── Tab Code: Source code preview (Supabase sync)
> 8002	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 8003	
> 8004	useNodeIntelligence Hook:
> 8005	  - contentQuery: fetch nodes.content column
> 8006	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 8007	  - state: isAnalyzing, analysisResult, progress
> 8008	```
> 8009	
> 8010	---
> 8011	
> 8012	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 8013	
> 8014	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 8015	
> 8016	| Action | Result |
> 8017	|--------|--------|
> 8018	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 8019	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 8020	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 8021	
> 8022	**Output da análise (estruturado em pt-BR):**
> 8023	- Visão Geral — papel do módulo no sistema
> 8024	- Padrões Detectados — design patterns, antipatterns
> 8025	- Acoplamento & Dependências — análise In/Out-Degree
> 8026	- Recomendações — 1-3 ações priorizadas
> 8027	
> ```

## 🤖 Claude *(20:29:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null",
  "description": "List scratch files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun  7 14:41 .
> drwx------ 30 ubuntu ubuntu 4096 Jun 17 14:55 ..
> ```

## 🤖 Claude *(20:29:43)*


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
> Output too large (58.7KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/tool-results/btl28k0bz.txt
> 
> Preview (first 2KB):
> # 🧠 Sprint Priorities — Constellation Orchestra
> 
> **Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 
> **90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 
> **Sprint v6.41.0 — Unified Sensorial Canvas (Phase Epsilon V9): AGI→ASI ref + emenda BoK + Fases 3.1-3.4 (2026-06-17)** — `/handson` → conversa estratégica (Model Council; plugin `claude-code-setup`; paper *From AGI to ASI* DeepMind) → diretiva arquitetural **Unified Core Sensorial Canvas** (fundir Core-Fable + Matrix + Memória num canvas 3D R3F). Arco Closed-Loop: **(1) Fundamentação** — arXiv 2606.12683 (Legg/Hutter/Leibo) lido inteiro (57p) + selado como nó `architecture` `a576216e` (edge INFORMS→openclaw) + checklist Via 4 (`.claude/context/agi-asi-via4-design-checklist.md`); tese: o MCORCH é a Via 4 (group agent formation) instanciada na app layer. **(2) Auditoria de clusters (Lei 1)** — Louvain = REAL/VIVO (`useConstellationSigma.ts:227`, graphology client-side); squad-coloring = MORTO (`crew_module_ownership` 0 rows → fallback Louvain) + heurístico (`inferSquad`) → **Decisão B = PODAR** (Louvain oficial; OTD-SQUAD-OWNERSHIP-REVIVAL). **(3) Emenda BoK** (gate Sovereign-eleito sobre override) — `mcorch-constellation` +PR-025/FR-043..049/NFR-023-024/SDD §9 (reconciliação Sigma→R3F: graphology cérebro / R3F corpo). **(4) Fases 3.1-3.4** (R3F, commits granulares, 3 páginas legadas preservadas) — scaffold rota `/dashboard/universe`/store/shell 72-28 + Code Network InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop (memória corrigida: glow aditivo). **(5) E2E ocular** (preview local à prova de CF + sessão injetada) nos 3 modos — telemetria real (8.560 nós/8.816 arestas/~733 comun./159 pensamentos); "esfera órfã" desmistificada = **spinner de loading**. **P
> ...
> </persisted-output>
> ```

## 🤖 Claude *(20:29:49)*


## 🤖 Claude *(20:29:49)*

Now the BoK gate completeness check across all suites:

## 🤖 Claude *(20:29:51)*


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
> ✅ viral-daily-canvas
> ✅ viralmind
> ✅ vision-mcp
> ```

## 🤖 Claude *(20:29:55)*


## 🤖 Claude *(20:29:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la docs/bok/security/ 2>/dev/null",
  "description": "List security BoK files (alt naming)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 124
> drwxrwxr-x  2 ubuntu ubuntu  4096 Jun  9 20:17 .
> drwxrwxr-x 22 ubuntu ubuntu  4096 Jun 11 00:36 ..
> -rw-rw-r--  1 ubuntu ubuntu  5005 Jun  9 19:21 00-deepsearch-blueprint.md
> -rw-rw-r--  1 ubuntu ubuntu 21029 Jun  9 20:06 01-brd-security.md
> -rw-rw-r--  1 ubuntu ubuntu 31774 Jun  9 20:10 02-srs-secure-spec.md
> -rw-rw-r--  1 ubuntu ubuntu 33058 Jun  9 22:10 03-sdd-hardening-architecture.md
> -rw-rw-r--  1 ubuntu ubuntu 16214 Jun  9 20:17 04-fmea-security.md
> ```

## 🤖 Claude *(20:30:05)*


## 🤖 Claude *(20:30:06)*

Let me check the single uncommitted change (proof-manifest.json) to characterize it:

## 🤖 Claude *(20:30:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git diff HEAD -- proof-manifest.json",
  "description": "Diff of proof-manifest.json"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> diff --git a/proof-manifest.json b/proof-manifest.json
> index 3b9494a..3a6e6f2 100644
> --- a/proof-manifest.json
> +++ b/proof-manifest.json
> @@ -1 +1 @@
> -{"handoffNodeId": "c21c53db-cd96-465d-92ba-fc419c0c83e7"}
> +{"handoffNodeId": "5225ff03-5e4d-4599-9c9a-625e2e1806af"}
> ```

## 🤖 Claude *(20:30:20)*


## 🤖 Claude *(20:30:44)*

═══════════════════════════════════════════════════════════
  **HANDSON — Unified Sensorial Canvas (Phase Epsilon V9)** · seal 2026-06-17
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
Fase selada: **Unified Sensorial Canvas (Epsilon V9) — Fases 3.1-3.4** (R3F: Code Network + Memory Network + Black Hole backdrop em `/dashboard/universe`)
Últimos commits:
- `776687f` — chore(sprint): registra v6.41.0 — Unified Sensorial Canvas Fases 3.1-3.4
- `d84b806` — docs(handoff): seal Unified Sensorial Canvas — AGI→ASI ref + emenda BoK
- `08b36eb` — docs(readme): v6.41.0 — Code+Memory+Black Hole R3F

📂 **MUDANÇAS PENDENTES**
- `M proof-manifest.json` (1 linha) — ponteiro `handoffNodeId` atualizado para o nó do último seal (`5225ff03…`, Canvas V9). Artefato benigno da Fase 5c do `/handoff` anterior, não-commitado. **Não conflita** — descrever, não commitar.

🏗️ **INFRA** — todos saudáveis
- `mcorch_chroma`: Up 2 days (healthy) — Chroma API v2: **OK** (`heartbeat` respondeu)
- `mcorch_claude_mem`: Up 2 days (healthy) · `mcorch_vision_mcp`: Up 17h (healthy)
- `mega-brain-daemon/webhook/dashboard`: Up 2 days (healthy)

🧠 **KNOWLEDGE MESH**
**8926 nós** (verif. live 2026-06-17 REST count=exact) · **9070 arestas** · 100% embedded (768d HNSW cosine)
Inclui o handoff `5225ff03` + ref AGI→ASI `a576216e` (edge `INFORMS` → openclaw seal)

🔧 **TYPESCRIPT** — Zero erros ✅

📚 **BoK SUITES** (MCORCH Master Execution Protocol)
- **Completas (9/9):** 19 suítes seladas — incluindo `mcorch-constellation` (módulo ativo, com **emenda PR-025 + FR-043..049 + NFR-023/024 + SDD §9** que fundamenta o Unified Canvas), `vision-mcp`, `marketing-hub`, `identity-fabric`, etc.
- **`security` (Cyber-Sentinel):** naming não-padrão (`00-deepsearch-blueprint` · `01-brd-security` · `02-srs-secure-spec` · `03-sdd-hardening-architecture` · `04-fmea-security`) — os **5 docs existem materialmente** (21K/31K/33K/16K, commit Jun 9). O loop padrão acusa "missing" só por convenção de nome; **não é gate-block**.
- **GATE:** ✅ Sem bloqueador. O trabalho ativo (Unified Canvas) já tem BoK selada.

📌 **SPRINT**
Goal: *Distribuição social autônoma operacional* (LinkedIn auto-publica; Twitter/IG aguardam tier/App Review)
Sprint corrente: **v6.41.0 — Unified Sensorial Canvas (Epsilon V9)** Fases 3.1-3.4 entregues

⚡ **PRÓXIMOS PASSOS** (do Pending Actions — item 🌌 EM ANDAMENTO)
**Unified Sensorial Canvas — Fases 3.5-3.10** (plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`):
1. **3.5 Sinapses inter-rede** — arestas **REAIS** de `mcorch_edges` cruzando código↔memória, acesas só no modo Universo (nunca fabricar arestas — Lei 1).
2. **3.7 layout/perf** (`OTD-UCANVAS-PERF`) — a query do código leva **~30s** com 2 canvases; avaliar Louvain em Web Worker / streaming do grafo / lazy do backdrop. **Maior risco de UX.**
3. **3.6 fly-to** (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.8** executar a poda do squad-coloring morto (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal.
> ⚠️ 3 páginas legadas (matrix/memory/core-fable) preservadas como backup **até a paridade (3.9)**.

⚠️ **ALERTAS**
- Nenhum bloqueador. TS limpo, infra verde, mesh íntegra.
- Lembrete Lei 1 (gate Canvas): qualquer alteração de UI no `/dashboard/universe` exige `/e2e-audit` 1920×1080 antes de declarar SUCCESS.
- Calibração de janela (Lei 3 / [[feedback_context_budget_calibration]]): não selar antes de ~95% — puxar 3.5→3.10 em sequência probe-first.

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

A continuação natural é a **Fase 3.5 (sinapses inter-rede reais)** ou atacar primeiro a **3.7 (perf da query de ~30s)**, que é o maior atrito de UX hoje. Qual frente o Maestro quer que eu inicie?

## 👤 User *(20:32:45)*

Precisamos retomar diretamente as questões dos produtos, lembra o objetivo? Criar alimentar contas de redes sociais com conteúdos gerados automaticamente e agendados, podendo gerar tudo de uma vez só ou a cada 3 dias mediante analise do que foi feito anteriormente para melhorar ainda mais os próximos criativos. 

Para os conteúdos virais com comissão do mercado livre

## 🤖 Claude *(20:34:02)*


## 🤖 Claude *(20:34:09)*

O Maestro está me trazendo de volta ao **coração do produto** — o motor de receita, não a camada visual. Entendi o objetivo com precisão:

> **Motor de conteúdo viral autônomo** que (R1) gera conteúdo para redes sociais automaticamente, (R2) agenda — tudo de uma vez **ou** a cada 3 dias, (R3) a cada ciclo **analisa o que foi feito antes para melhorar os próximos criativos**, (R4) tudo focado em **conteúdo viral com comissão do Mercado Livre**.

Antes de propor qualquer rota (Closed-Loop + Lei 1 Materialidade), preciso saber **exatamente o que já está vivo, o que está morto e o que falta** nessa máquina — sem chutar. Já existe muita peça construída (`orchestrate-content`, `auto-publish` cron, `campaign-run`, click ledger ML, Canvas Studio, 5 suítes BoK de conteúdo). A pergunta real é: onde está o gap entre isso e o **loop auto-melhorável a cada 3 dias**?

Vou rodar um workflow de auditoria material — 6 leitores em paralelo mapeando cada subsistema com prova (path:linha), depois uma síntese que cruza tudo contra os seus 4 requisitos e dá o veredito do BoK Gate.

## 🤖 Claude *(20:35:11)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'viral-content-engine-audit',\n  description: 'Material audit of the autonomous viral ML-affiliate content engine: what exists, what is dead, what is missing vs the Sovereign 4 requirements (auto-generate, schedule all-at-once/every-3-days, self-improve via analysis, ML commission)',\n  phases: [\n    { title: 'Map', detail: '6 parallel read-only readers map each subsystem with material proof (path:line)' },\n    { title: 'Synthesize', detail: 'cross-cut all readers vs the 4 requirements + BoK gate verdict + recommended path' },\n  ],\n}\n\nconst OBJ = `OBJETIVO DO SOVEREIGN (contexto fixo da auditoria): construir um MOTOR DE CONTE\u00daDO VIRAL AUT\u00d4NOMO que:\n- R1: gera conte\u00fado para contas de redes sociais AUTOMATICAMENTE.\n- R2: AGENDA \u2014 pode gerar tudo de uma vez s\u00f3 OU um lote a cada 3 dias.\n- R3: a cada ciclo (3 dias) ANALISA o desempenho do conte\u00fado anterior para MELHORAR os pr\u00f3ximos criativos (loop auto-melhor\u00e1vel).\n- R4: tudo focado em CONTE\u00daDO VIRAL com COMISS\u00c3O DE AFILIADO DO MERCADO LIVRE (receita).\n\nVoc\u00ea audita o repo MCORCH em /home/gcrUX/htdocs/constellation-orchestra \u2014 READ-ONLY (n\u00e3o edite nada).\nREGRA DE MATERIALIDADE (Lei 1): toda afirma\u00e7\u00e3o carrega prova \u2014 path:linha, nome de fun\u00e7\u00e3o/tabela, ou status real. N\u00c3O invente. Se algo n\u00e3o existe, status='missing' e diga onde procurou. Use Grep/Glob/Read/Bash(read-only). Para checar tabelas/colunas, leia as migrations em supabase/migrations/ (n\u00e3o precisa de DB ao vivo).`\n\nconst SUBSYSTEM_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  properties: {\n    subsystem: { type: 'string' },\n    components: {\n      type: 'array',\n      items: {\n        type: 'object', additionalProperties: false,\n        properties: {\n          name: { type: 'string' },\n          path: { type: 'string', description: 'file path, with :line when known' },\n          status: { type: 'string', enum: ['alive', 'partial', 'dead', 'missing'] },\n          evidence: { type: 'string', description: 'concrete proof: what the code/migration actually does' },\n        },\n        required: ['name', 'path', 'status', 'evidence'],\n      },\n    },\n    gaps: {\n      type: 'array',\n      items: {\n        type: 'object', additionalProperties: false,\n        properties: {\n          description: { type: 'string' },\n          severity: { type: 'string', enum: ['critical', 'high', 'medium', 'low'] },\n          mapsToRequirement: { type: 'string', enum: ['R1', 'R2', 'R3', 'R4', 'cross'] },\n        },\n        required: ['description', 'severity', 'mapsToRequirement'],\n      },\n    },\n    notes: { type: 'string' },\n  },\n  required: ['subsystem', 'components', 'gaps', 'notes'],\n}\n\nconst READERS = [\n  {\n    label: 'content-generation',\n    prompt: `${OBJ}\n\nTEU ESCOPO: o pipeline de GERA\u00c7\u00c3O de conte\u00fado (R1/R4). Mapeie:\n- supabase/functions/orchestrate-content/index.ts (pipeline completo: que formatos gera? article/LinkedIn/X? como anexa produto ML? UTM?)\n- supabase/functions/generate-content/, generate-image/ (prompts, modelos, qualidade do criativo)\n- src/hooks/useOrchestrationGraph.ts\n- Procure o \u00e2ngulo \"viral\": existe alguma l\u00f3gica de hook/gancho viral, trending, formato otimizado p/ engajamento? Ou \u00e9 gen\u00e9rico?\n- Como o conte\u00fado \u00e9 amarrado a um PRODUTO do Mercado Livre na gera\u00e7\u00e3o (qual produto, qual copy)?\nReporte componentes com status+prova e os gaps vs R1/R4.`,\n  },\n  {\n    label: 'scheduling-cron',\n    prompt: `${OBJ}\n\nTEU ESCOPO: AGENDAMENTO e execu\u00e7\u00e3o recorrente (R2/R3 \u2014 a parte de cad\u00eancia). Mapeie:\n- scripts/auto-publish-cron.sh e qualquer cron em crontab (HANDOFF.md lista crons gcrUX/ubuntu)\n- supabase/functions/publish-social/ e publish-meta/, publish-wordpress/\n- Tabelas de agendamento: grep migrations por \"scheduled\", \"schedule\", \"cron\", \"next_run\", \"cadence\", \"recurring\", \"interval\". Existe tabela de posts agendados? Com hor\u00e1rio futuro?\n- CR\u00cdTICO: existe alguma no\u00e7\u00e3o de RECORR\u00caNCIA \"a cada 3 dias\"? Um scheduler que dispara gera\u00e7\u00e3o peri\u00f3dica? Ou s\u00f3 publica o que j\u00e1 foi gerado uma vez?\n- campaign-run e sequences/nurture t\u00eam cad\u00eancia temporal (delays entre steps)? Isso poderia servir de base p/ R2/R3?\nReporte status+prova. O gap central prov\u00e1vel: gera\u00e7\u00e3o RECORRENTE agendada n\u00e3o existe \u2014 confirme ou refute materialmente.`,\n  },\n  {\n    label: 'ml-affiliate-revenue',\n    prompt: `${OBJ}\n\nTEU ESCOPO: a camada de RECEITA Mercado Livre (R4). Mapeie:\n- supabase/functions/process-affiliate-link/ (resolu\u00e7\u00e3o per-user de affiliate_tag, GET+POST)\n- supabase/functions/handle-ml-postback/ (revenue_cents)\n- scripts/link-forge.ts\n- tabela affiliate_config (colunas affiliate_tag/app_id), vm_affiliate_products, affiliate_links (revenue_cents, clicks)\n- src/pages/AffiliateProductsPage.tsx, src/hooks/useAffiliateProducts.ts, src/components/dashboard/ROIWidget.tsx\n- Click ledger / redirect tracker (OTD-ML-CLICKS \u2014 diz estar fechado). Como contamos cliques e receita HOJE?\n- De onde v\u00eam os PRODUTOS ML que viram conte\u00fado? H\u00e1 cat\u00e1logo/sele\u00e7\u00e3o autom\u00e1tica de produtos \"virais\"/com comiss\u00e3o?\nReporte status+prova e os gaps vs R4 (especialmente: sele\u00e7\u00e3o autom\u00e1tica de produtos + atribui\u00e7\u00e3o de receita por criativo).`,\n  },\n  {\n    label: 'feedback-self-improvement',\n    prompt: `${OBJ}\n\nTEU ESCOPO (provavelmente o MAIOR gap): o LOOP AUTO-MELHOR\u00c1VEL (R3). Procure QUALQUER mecanismo que leia o DESEMPENHO do conte\u00fado passado p/ informar o pr\u00f3ximo:\n- grep amplo: \"performance\", \"analytics\", \"engagement\", \"metrics\", \"improve\", \"optimize\", \"best performing\", \"feedback\", \"learn\"\n- supabase/functions/aeo-audit/ (Answer Engine Optimization?), analyze-node/, lead-score/\n- Existe coleta de m\u00e9tricas dos posts publicados (likes/views/clicks por post) de volta das redes? publish-social/publish-meta retornam m\u00e9tricas? H\u00e1 tabela de m\u00e9tricas de post?\n- Existe algum prompt de gera\u00e7\u00e3o que recebe \"o que funcionou antes\" como input?\n- O Knowledge Mesh (mcorch_nodes observation) guarda outcomes de campanha de forma reutiliz\u00e1vel p/ gera\u00e7\u00e3o?\nSeja honesto: se N\u00c3O existe loop de melhoria baseado em performance real, marque status='missing' e descreva o que existiria de mais pr\u00f3ximo (ex: AEO, mesh observations) e por que n\u00e3o fecha R3.`,\n  },\n  {\n    label: 'marketing-hub-canvas',\n    prompt: `${OBJ}\n\nTEU ESCOPO: orquestra\u00e7\u00e3o de campanha multi-plataforma + creatives visuais (cobre R1/R2/R4 parcialmente). Mapeie:\n- supabase/functions/campaign-run/ (cascata CAMPAIGN_RUN; dispatch paralelo p/ orchestrate-content)\n- campaign_steps, sequences, sequence_enrollments (migrations marketing hub)\n- supabase/functions/nurture-dispatch/, intent-execute/\n- scripts/canvas-campaign-build.ts (creatives por produto), src/lib/canvas-utils.ts (findUpstreamImages \u2014 consist\u00eancia visual), vm_canvas_projects/vm_canvas_executions\n- canvas-execute (Nano Banana / Higgsfield DoP) \u2014 gera\u00e7\u00e3o de imagem/v\u00eddeo por produto\nPergunta-chave: o Marketing Hub + Canvas j\u00e1 permite \"gerar um lote de criativos por produto de uma vez\"? Qu\u00e3o perto est\u00e1 de R2 (lote \u00fanico) e o que falta p/ a recorr\u00eancia de 3 dias (R2/R3)?\nReporte status+prova e gaps.`,\n  },\n  {\n    label: 'bok-coverage',\n    prompt: `${OBJ}\n\nTEU ESCOPO: cobertura BoK (porta do Closed-Loop / BoK Gate). Leia os FRD/PRD/BRD destes suites e diga QUAIS FRs cobrem cada requisito R1-R4 e o que est\u00e1 UNDOCUMENTED:\n- docs/bok/post-engine/ (03-prd, 04-frd)\n- docs/bok/viral-daily-canvas/ (03-prd, 04-frd)\n- docs/bok/viralmind/ (03-prd, 04-frd)\n- docs/bok/conteudo-v2/ (03-prd, 04-frd)\n- docs/bok/marketing-hub/ (03-prd, 04-frd)\nProcure especificamente FRs sobre: (a) gera\u00e7\u00e3o autom\u00e1tica de conte\u00fado social; (b) AGENDAMENTO recorrente / cad\u00eancia a cada N dias; (c) loop de MELHORIA baseado em an\u00e1lise de performance passada; (d) conte\u00fado viral + afiliado ML.\nVeredito do BoK Gate: o \"motor de conte\u00fado viral auto-melhor\u00e1vel agendado a cada 3 dias\" J\u00c1 est\u00e1 documentado em algum suite (cite FR IDs), ou \u00e9 feature NOVA que exige /bok-scribe ou emenda a um suite existente? Liste exatamente o que falta documentar.`,\n  },\n]\n\nphase('Map')\nlog('Auditando 6 subsistemas do motor de conte\u00fado viral em paralelo (read-only, prova material)...')\nconst maps = (await parallel(\n  READERS.map((r) => () => agent(r.prompt, { label: `map:${r.label}`, phase: 'Map', schema: SUBSYSTEM_SCHEMA }))\n)).filter(Boolean)\n\nlog(`Mapeamento conclu\u00eddo: ${maps.length}/6 subsistemas. Sintetizando contra R1-R4 + BoK Gate...`)\n\nconst SYNTHESIS_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  properties: {\n    requirementCoverage: {\n      type: 'array',\n      items: {\n        type: 'object', additionalProperties: false,\n        properties: {\n          requirement: { type: 'string', enum: ['R1', 'R2', 'R3', 'R4'] },\n          title: { type: 'string' },\n          coverage: { type: 'string', enum: ['complete', 'partial', 'missing'] },\n          whatExists: { type: 'string', description: 'with path/function/table proof' },\n          gap: { type: 'string' },\n          whatIsNeeded: { type: 'string' },\n        },\n        required: ['requirement', 'title', 'coverage', 'whatExists', 'gap', 'whatIsNeeded'],\n      },\n    },\n    bokGate: {\n      type: 'object', additionalProperties: false,\n      properties: {\n        verdict: { type: 'string', enum: ['open', 'blocked', 'amend-existing', 'new-suite'] },\n        reasoning: { type: 'string' },\n        relevantSuites: { type: 'array', items: { type: 'string' } },\n        documentedCoverage: { type: 'string', description: 'which FR IDs already cover R1-R4' },\n        whatMustBeDocumented: { type: 'string' },\n      },\n      required: ['verdict', 'reasoning', 'relevantSuites', 'documentedCoverage', 'whatMustBeDocumented'],\n    },\n    recommendedPath: {\n      type: 'array',\n      items: {\n        type: 'object', additionalProperties: false,\n        properties: {\n          order: { type: 'number' },\n          step: { type: 'string' },\n          rationale: { type: 'string' },\n          buildsOn: { type: 'string', description: 'existing component this reuses (path)' },\n          effort: { type: 'string', enum: ['S', 'M', 'L', 'XL'] },\n        },\n        required: ['order', 'step', 'rationale', 'buildsOn', 'effort'],\n      },\n    },\n    keyRisks: { type: 'array', items: { type: 'string' } },\n    openQuestionsForSovereign: { type: 'array', items: { type: 'string' }, description: 'decisions only the Sovereign can make' },\n  },\n  required: ['requirementCoverage', 'bokGate', 'recommendedPath', 'keyRisks', 'openQuestionsForSovereign'],\n}\n\nphase('Synthesize')\nconst synthesis = await agent(\n  `${OBJ}\n\nVoc\u00ea \u00e9 o sintetizador. Abaixo est\u00e3o os mapeamentos materiais de 6 subsistemas (JSON). Cruze TUDO e produza:\n\n1. requirementCoverage: para CADA requisito R1/R2/R3/R4 \u2014 coverage (complete/partial/missing), o que existe HOJE (com prova path/fun\u00e7\u00e3o/tabela), o gap exato, e o que falta construir. Seja preciso e n\u00e3o otimista: se o loop de 3 dias auto-melhor\u00e1vel n\u00e3o existe, R3=missing.\n2. bokGate: o veredito do Closed-Loop. O motor recorrente auto-melhor\u00e1vel J\u00c1 est\u00e1 documentado em BoK (cite FR IDs) ou exige /bok-scribe (suite novo) ou emenda a um suite existente? Diga exatamente o que precisa ser documentado antes de codar.\n3. recommendedPath: passos ordenados que REUTILIZAM o que j\u00e1 existe (cite o componente base por path) \u2014 do mais alavancado ao menos. Marque esfor\u00e7o S/M/L/XL.\n4. keyRisks e openQuestionsForSovereign (decis\u00f5es que s\u00f3 o Sovereign decide: ex. cad\u00eancia exata, quais redes priorizar, BYOK de modelos, or\u00e7amento mcoCoins do loop aut\u00f4nomo, fonte dos produtos ML).\n\nMAPEAMENTOS:\n${JSON.stringify(maps, null, 2)}`,\n  { label: 'synthesize', phase: 'Synthesize', schema: SYNTHESIS_SCHEMA }\n)\n\nreturn { maps, synthesis }\n",
  "description": "Audit viral content engine vs 4 requirements"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wvz1hcque
> Summary: Material audit of the autonomous viral ML-affiliate content engine: what exists, what is dead, what is missing vs the Sovereign 4 requirements (auto-generate, schedule all-at-once/every-3-days, self-improve via analysis, ML commission)
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/subagents/workflows/wf_9a9e1c59-756
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/workflows/scripts/viral-content-engine-audit-wf_9a9e1c59-756.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/workflows/scripts/viral-content-engine-audit-wf_9a9e1c59-756.js"} to iterate without resending the script.)
> Run ID: wf_9a9e1c59-756
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/workflows/scripts/viral-content-engine-audit-wf_9a9e1c59-756.js", resumeFromRunId: "wf_9a9e1c59-756"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(20:35:17)*


## 🤖 Claude *(20:35:26)*

O workflow está rodando em background (`/workflows` para acompanhar ao vivo). São 6 leitores materiais em paralelo + síntese — vou ser notificado quando concluir e trago o veredito completo: cobertura por requisito (R1-R4), status do BoK Gate, e a rota recomendada que reaproveita o que já existe.

Enquanto roda, deixo minha leitura inicial (a confirmar materialmente pela auditoria) para alinharmos a expectativa:

- **R1 (gerar automático)** e **R4 (afiliado ML)** — provavelmente **já existem e estão vivos**: `orchestrate-content` gera artigo/LinkedIn/X + imagem e anexa link ML com UTM; click ledger ML fechado (OTD-ML-CLICKS).
- **R2 (agendar — lote único ou a cada 3 dias)** — o "lote de uma vez" provavelmente está perto via `campaign-run`; a **recorrência agendada a cada 3 dias** é quase certo um **gap** (o `auto-publish` cron só publica o que já foi gerado, não dispara nova geração periódica).
- **R3 (loop auto-melhorável: analisar o anterior → melhorar o próximo)** — esse é o meu palpite para o **maior buraco**. Hoje não há, que eu saiba, coleta de performance real dos posts de volta para alimentar o próximo prompt. É o coração da sua diretiva e provavelmente o que precisa ser desenhado.

A auditoria vai confirmar ou derrubar cada um desses com prova (path:linha) antes de eu propor qualquer código. Aguardo a conclusão.

## 👤 User *(20:48:27)*

<task-notification>
<task-id>wvz1hcque</task-id>
<tool-use-id>toolu_015nciNpXqKCkRjDBEwaMXMj</tool-use-id>
<output-file>/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/tasks/wvz1hcque.output</output-file>
<status>completed</status>
<summary>Dynamic workflow "Material audit of the autonomous viral ML-affiliate content engine: what exists, what is dead, what is missing vs the Sovereign 4 requirements (auto-generate, schedule all-at-once/every-3-days, self-improve via analysis, ML commission)" completed</summary>
<result>{"maps":[{"subsystem":"Pipeline de GERAÇÃO de conteúdo (R1 geração automática + R4 amarração ao produto/comissão Mercado Livre)","components":[{"name":"orchestrate-content (entrypoint async)","path":"supabase/functions/orchestrate-content/index.ts:26-227","status":"alive","evidence":"É só um DISPATCHER: valida JWT, roda Cyber-Sentinel no topic (linha 92), cobra 10 mcoCoins via deduct_mco_coins RPC (linha 112), cria pipeline_runs (linha 132) e enfileira o 1º step via RPC async_orchestrate_step (linha 180). NÃO gera conteúdo aqui. stepsOrder hardcoded = [article_generation, wordpress_publish, linkedin_post, twitter_thread, knowledge_mesh] (linha 163) — NÃO há image_generation nem video. Recebe platforms default ['wordpress','linkedin','twitter'] (linha 79)."},{"name":"orchestrate-step (motor real de geração)","path":"supabase/functions/orchestrate-step/index.ts:46-544","status":"alive","evidence":"Guard service-role-only (linha 52). Gera 3 formatos via LLM com tool-calling: article_generation (artigo HTML 1200+ palavras SEO, system prompt linha 137), linkedin_post (linha 289), twitter_thread (thread de 5 tweets, system prompt linha 359 diz 'threads virais'). Cada formato grava content_library + agenda scheduled_posts (LinkedIn +1h linha 327, Twitter +2h linha 405). Encadeia próximo step via async_orchestrate_step (linha 508). Modelo default llama-3.3-70b (Groq/OpenRouter), BYOK per-user (linha 103-118)."},{"name":"Ângulo VIRAL no prompt de geração","path":"supabase/functions/orchestrate-step/index.ts:137-138,289-290,359-360","status":"dead","evidence":"NÃO existe estratégia viral real. Artigo+LinkedIn são HARDCODED para público B2B 'donos de agências de marketing que querem usar IA' e 'ROI com IA' (linhas 138 e 290 — confirmado por grep, só 2 ocorrências). Só o twitter_thread menciona 'threads virais' no system prompt (linha 359), sem hook/gancho/trending real. NENHUM dado de trending, hook framework, ou formato otimizado p/ engajamento entra no prompt. O 'topic' vem cru de campaign.intent||campaign.name (campaign-run:87) ou input manual."},{"name":"fetch-trends (mineração de virais Apify/RapidAPI)","path":"supabase/functions/fetch-trends/index.ts:18-195","status":"partial","evidence":"EXISTE e funciona: scrapeia TikTok/Instagram via Apify actor clockworks~free-tiktok-scraper (linha 62), calcula viral_score/engagement_rate/velocity (linhas 91-96), faz upsert em vm_trends (linha 173). MAS é uma ILHA: grep confirma que vm_trends/fetch-trends só é consumido pela UI Viral Miner (src/hooks/useViralTrends.ts, ViralMinerPage.tsx, LeftPanel) — ZERO referência em orchestrate-content/orchestrate-step. O motor de geração NUNCA lê trends. capability 'viral_miner' existe no seed (scripts/seed-constellation-v2-capabilities.ts:38) mas desconectada do flywheel."},{"name":"Amarração ao PRODUTO Mercado Livre (auto-monetize)","path":"supabase/functions/_shared/affiliate.ts:15-110 + orchestrate-step/index.ts:175-200","status":"partial","evidence":"monetizeContent (affiliate.ts:69) roda SÓ no step article_generation (orchestrate-step:184), fail-open. Catálogo HARDCODED a 3 produtos via regex (affiliate.ts:18-20: Roborock S8 / Samsung Neo QLED 8K / Family Hub). NÃO escolhe produto por relevância nem por comissão — só faz match de regex no texto já gerado e linka a 1ª menção (affiliate.ts:102-107). O conteúdo é gerado SEM saber qual produto vende (prompt é product-unaware — grep linha 175 só acha o comentário de auto-monetize). URL real vem de vm_affiliate_products.product_url por external_id (affiliate.ts:49) com matt_word per-user. LinkedIn/Twitter NÃO recebem monetização (só article)."},{"name":"vm_affiliate_products (catálogo ML com comissão)","path":"supabase/migrations/20260514040300_viralmind_affiliate_radar.sql:3-31","status":"alive","evidence":"Tabela tem colunas ricas: commission_rate, commission_value, estimated_epc, profitability_score, trend_score, product_url (linhas 16-21). MAS a geração de conteúdo não usa nenhuma dessas métricas p/ escolher o que promover — affiliate.ts só usa product_url via JOIN por external_id. O potencial de 'escolher produto mais lucrativo' está no schema mas MORTO no pipeline de geração."},{"name":"generate-content (gerador standalone)","path":"supabase/functions/generate-content/index.ts:12-125","status":"partial","evidence":"Edge fn de geração genérica streaming (type+prompt+platform+tone), system prompt manda 'Otimize para engajamento' + hashtags (linha 60-72). Porém grep confirma que SÓ BlogEditorPage.tsx:118 a invoca — é ferramenta MANUAL de blog, NÃO faz parte do pipeline automático orchestrate-*. O pipeline inlina suas próprias chamadas LLM (não reusa esta fn)."},{"name":"generate-image (criativo visual)","path":"supabase/functions/generate-image/index.ts:11-160","status":"dead","evidence":"DALL-E 3 hardcoded, size '1024x1024' QUADRADO (linha 86 — não vertical 9:16 p/ Reels/TikTok), prompt genérico 'high-quality marketing image' (linha 71). grep de invoke('generate-image') retorna ZERO callers. useOrchestrationGraph.ts:67-69 comenta 'feature not yet in pipeline' e marca agent-image como idle. NENHUMA imagem é gerada no fluxo automático. Não recebe a imagem do produto ML nem foto-realismo do item."},{"name":"generate-video / generate-video-script / generate-audio-script","path":"supabase/functions/generate-video/index.ts, generate-video-script/index.ts, generate-audio-script/index.ts","status":"dead","evidence":"grep de invoke() não acha NENHUM caller dessas 3 funções em src/, supabase/functions/ ou scripts/. São órfãs do ponto de vista do motor viral automático — vídeo é o formato #1 de viral (TikTok/Reels) e não há nenhuma geração de vídeo no caminho orchestrate-content→step."},{"name":"campaign-run (driver de lote / cascata)","path":"supabase/functions/campaign-run/index.ts:44-188","status":"alive","evidence":"Despacha campaign_steps→orchestrate-content em paralelo (Promise.allSettled, MAX_PARALLEL_STEPS=8, linha 24). topic = campaign.intent||campaign.name (linha 87). channelToPlatforms mapeia content/affiliate→wordpress, social→linkedin+twitter (linha 35). Funciona, mas só repassa o mesmo topic genérico p/ N steps — não diversifica criativos nem injeta produto/trend por step."},{"name":"affiliate_url param do UI dropado","path":"src/hooks/useOrchestrationGraph.ts:50 vs supabase/functions/orchestrate-content/index.ts:79","status":"dead","evidence":"useOrchestrationGraph envia body.affiliate_url (hook linha 50), mas orchestrate-content só desestrutura {topic,campaign_id,platforms,site_url,wp_status} (linha 79) — grep de 'affiliate_url' nos 2 arquivos do pipeline = NONE. O usuário não consegue forçar QUAL produto promover via UI: o param é silenciosamente ignorado."}],"gaps":[{"description":"Não há geração de VÍDEO nem IMAGEM no pipeline automático. stepsOrder só tem texto (article/linkedin/twitter). generate-image (DALL-E 1024x1024 quadrado) e generate-video/-script são órfãs (zero callers). Conteúdo viral em redes sociais é majoritariamente vídeo vertical 9:16 (TikTok/Reels/Shorts) — o motor não produz o formato que viraliza.","severity":"critical","mapsToRequirement":"R1"},{"description":"Zero estratégia VIRAL na geração. Os prompts são hardcoded p/ público B2B 'donos de agências de marketing / ROI com IA' (orchestrate-step:138,290) — o oposto de conteúdo de consumo viral que vende um produto físico. Nenhum hook framework, padrão de gancho, ou formato de engajamento entra no prompt.","severity":"critical","mapsToRequirement":"R4"},{"description":"fetch-trends (Apify TikTok/IG, viral_score, engagement_rate, vm_trends) está DESCONECTADO da geração. É uma ilha consumida só pela UI Viral Miner. O motor de geração nunca lê trends p/ pautar/otimizar criativos — quebra a premissa de 'conteúdo viral' baseado em dados de tendência.","severity":"critical","mapsToRequirement":"R4"},{"description":"O conteúdo é gerado PRODUCT-UNAWARE e a monetização é um afterthought por regex. monetizeContent só roda no artigo (não no LinkedIn/Twitter
... (truncated 83775 chars, full result in /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/tasks/wvz1hcque.output)</result>
<usage><agent_count>7</agent_count><subagent_tokens>816340</subagent_tokens><tool_uses>139</tool_uses><duration_ms>795718</duration_ms></usage>
</task-notification>

## 🤖 Claude *(20:48:30)*


## 🤖 Claude *(20:48:31)*

A auditoria concluiu (7 agentes, 139 leituras de arquivo). O resultado veio truncado — vou ler o arquivo completo para extrair a síntese contra R1-R4 e o veredito do BoK Gate.

## 🤖 Claude *(20:48:31)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/tasks/wvz1hcque.output"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>[Truncated: PARTIAL view — showing lines 1-392 of 778 total (42143 tokens, cap 25000). Call Read with offset=393 limit=392 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>
> 
> 1	{
> 2	  "summary": "Material audit of the autonomous viral ML-affiliate content engine: what exists, what is dead, what is missing vs the Sovereign 4 requirements (auto-generate, schedule all-at-once/every-3-days, self-improve via analysis, ML commission)",
> 3	  "agentCount": 7,
> 4	  "logs": [
> 5	    "Auditando 6 subsistemas do motor de conteúdo viral em paralelo (read-only, prova material)...",
> 6	    "Mapeamento concluído: 6/6 subsistemas. Sintetizando contra R1-R4 + BoK Gate..."
> 7	  ],
> 8	  "result": {
> 9	    "maps": [
> 10	      {
> 11	        "subsystem": "Pipeline de GERAÇÃO de conteúdo (R1 geração automática + R4 amarração ao produto/comissão Mercado Livre)",
> 12	        "components": [
> 13	          {
> 14	            "name": "orchestrate-content (entrypoint async)",
> 15	            "path": "supabase/functions/orchestrate-content/index.ts:26-227",
> 16	            "status": "alive",
> 17	            "evidence": "É só um DISPATCHER: valida JWT, roda Cyber-Sentinel no topic (linha 92), cobra 10 mcoCoins via deduct_mco_coins RPC (linha 112), cria pipeline_runs (linha 132) e enfileira o 1º step via RPC async_orchestrate_step (linha 180). NÃO gera conteúdo aqui. stepsOrder hardcoded = [article_generation, wordpress_publish, linkedin_post, twitter_thread, knowledge_mesh] (linha 163) — NÃO há image_generation nem video. Recebe platforms default ['wordpress','linkedin','twitter'] (linha 79)."
> 18	          },
> 19	          {
> 20	            "name": "orchestrate-step (motor real de geração)",
> 21	            "path": "supabase/functions/orchestrate-step/index.ts:46-544",
> 22	            "status": "alive",
> 23	            "evidence": "Guard service-role-only (linha 52). Gera 3 formatos via LLM com tool-calling: article_generation (artigo HTML 1200+ palavras SEO, system prompt linha 137), linkedin_post (linha 289), twitter_thread (thread de 5 tweets, system prompt linha 359 diz 'threads virais'). Cada formato grava content_library + agenda scheduled_posts (LinkedIn +1h linha 327, Twitter +2h linha 405). Encadeia próximo step via async_orchestrate_step (linha 508). Modelo default llama-3.3-70b (Groq/OpenRouter), BYOK per-user (linha 103-118)."
> 24	          },
> 25	          {
> 26	            "name": "Ângulo VIRAL no prompt de geração",
> 27	            "path": "supabase/functions/orchestrate-step/index.ts:137-138,289-290,359-360",
> 28	            "status": "dead",
> 29	            "evidence": "NÃO existe estratégia viral real. Artigo+LinkedIn são HARDCODED para público B2B 'donos de agências de marketing que querem usar IA' e 'ROI com IA' (linhas 138 e 290 — confirmado por grep, só 2 ocorrências). Só o twitter_thread menciona 'threads virais' no system prompt (linha 359), sem hook/gancho/trending real. NENHUM dado de trending, hook framework, ou formato otimizado p/ engajamento entra no prompt. O 'topic' vem cru de campaign.intent||campaign.name (campaign-run:87) ou input manual."
> 30	          },
> 31	          {
> 32	            "name": "fetch-trends (mineração de virais Apify/RapidAPI)",
> 33	            "path": "supabase/functions/fetch-trends/index.ts:18-195",
> 34	            "status": "partial",
> 35	            "evidence": "EXISTE e funciona: scrapeia TikTok/Instagram via Apify actor clockworks~free-tiktok-scraper (linha 62), calcula viral_score/engagement_rate/velocity (linhas 91-96), faz upsert em vm_trends (linha 173). MAS é uma ILHA: grep confirma que vm_trends/fetch-trends só é consumido pela UI Viral Miner (src/hooks/useViralTrends.ts, ViralMinerPage.tsx, LeftPanel) — ZERO referência em orchestrate-content/orchestrate-step. O motor de geração NUNCA lê trends. capability 'viral_miner' existe no seed (scripts/seed-constellation-v2-capabilities.ts:38) mas desconectada do flywheel."
> 36	          },
> 37	          {
> 38	            "name": "Amarração ao PRODUTO Mercado Livre (auto-monetize)",
> 39	            "path": "supabase/functions/_shared/affiliate.ts:15-110 + orchestrate-step/index.ts:175-200",
> 40	            "status": "partial",
> 41	            "evidence": "monetizeContent (affiliate.ts:69) roda SÓ no step article_generation (orchestrate-step:184), fail-open. Catálogo HARDCODED a 3 produtos via regex (affiliate.ts:18-20: Roborock S8 / Samsung Neo QLED 8K / Family Hub). NÃO escolhe produto por relevância nem por comissão — só faz match de regex no texto já gerado e linka a 1ª menção (affiliate.ts:102-107). O conteúdo é gerado SEM saber qual produto vende (prompt é product-unaware — grep linha 175 só acha o comentário de auto-monetize). URL real vem de vm_affiliate_products.product_url por external_id (affiliate.ts:49) com matt_word per-user. LinkedIn/Twitter NÃO recebem monetização (só article)."
> 42	          },
> 43	          {
> 44	            "name": "vm_affiliate_products (catálogo ML com comissão)",
> 45	            "path": "supabase/migrations/20260514040300_viralmind_affiliate_radar.sql:3-31",
> 46	            "status": "alive",
> 47	            "evidence": "Tabela tem colunas ricas: commission_rate, commission_value, estimated_epc, profitability_score, trend_score, product_url (linhas 16-21). MAS a geração de conteúdo não usa nenhuma dessas métricas p/ escolher o que promover — affiliate.ts só usa product_url via JOIN por external_id. O potencial de 'escolher produto mais lucrativo' está no schema mas MORTO no pipeline de geração."
> 48	          },
> 49	          {
> 50	            "name": "generate-content (gerador standalone)",
> 51	            "path": "supabase/functions/generate-content/index.ts:12-125",
> 52	            "status": "partial",
> 53	            "evidence": "Edge fn de geração genérica streaming (type+prompt+platform+tone), system prompt manda 'Otimize para engajamento' + hashtags (linha 60-72). Porém grep confirma que SÓ BlogEditorPage.tsx:118 a invoca — é ferramenta MANUAL de blog, NÃO faz parte do pipeline automático orchestrate-*. O pipeline inlina suas próprias chamadas LLM (não reusa esta fn)."
> 54	          },
> 55	          {
> 56	            "name": "generate-image (criativo visual)",
> 57	            "path": "supabase/functions/generate-image/index.ts:11-160",
> 58	            "status": "dead",
> 59	            "evidence": "DALL-E 3 hardcoded, size '1024x1024' QUADRADO (linha 86 — não vertical 9:16 p/ Reels/TikTok), prompt genérico 'high-quality marketing image' (linha 71). grep de invoke('generate-image') retorna ZERO callers. useOrchestrationGraph.ts:67-69 comenta 'feature not yet in pipeline' e marca agent-image como idle. NENHUMA imagem é gerada no fluxo automático. Não recebe a imagem do produto ML nem foto-realismo do item."
> 60	          },
> 61	          {
> 62	            "name": "generate-video / generate-video-script / generate-audio-script",
> 63	            "path": "supabase/functions/generate-video/index.ts, generate-video-script/index.ts, generate-audio-script/index.ts",
> 64	            "status": "dead",
> 65	            "evidence": "grep de invoke() não acha NENHUM caller dessas 3 funções em src/, supabase/functions/ ou scripts/. São órfãs do ponto de vista do motor viral automático — vídeo é o formato #1 de viral (TikTok/Reels) e não há nenhuma geração de vídeo no caminho orchestrate-content→step."
> 66	          },
> 67	          {
> 68	            "name": "campaign-run (driver de lote / cascata)",
> 69	            "path": "supabase/functions/campaign-run/index.ts:44-188",
> 70	            "status": "alive",
> 71	            "evidence": "Despacha campaign_steps→orchestrate-content em paralelo (Promise.allSettled, MAX_PARALLEL_STEPS=8, linha 24). topic = campaign.intent||campaign.name (linha 87). channelToPlatforms mapeia content/affiliate→wordpress, social→linkedin+twitter (linha 35). Funciona, mas só repassa o mesmo topic genérico p/ N steps — não diversifica criativos nem injeta produto/trend por step."
> 72	          },
> 73	          {
> 74	            "name": "affiliate_url param do UI dropado",
> 75	            "path": "src/hooks/useOrchestrationGraph.ts:50 vs supabase/functions/orchestrate-content/index.ts:79",
> 76	            "status": "dead",
> 77	            "evidence": "useOrchestrationGraph envia body.affiliate_url (hook linha 50), mas orchestrate-content só desestrutura {topic,campaign_id,platforms,site_url,wp_status} (linha 79) — grep de 'affiliate_url' nos 2 arquivos do pipeline = NONE. O usuário não consegue forçar QUAL produto promover via UI: o param é silenciosamente ignorado."
> 78	          }
> 79	        ],
> 80	        "gaps": [
> 81	          {
> 82	            "description": "Não há geração de VÍDEO nem IMAGEM no pipeline automático. stepsOrder só tem texto (article/linkedin/twitter). generate-image (DALL-E 1024x1024 quadrado) e generate-video/-script são órfãs (zero callers). Conteúdo viral em redes sociais é majoritariamente vídeo vertical 9:16 (TikTok/Reels/Shorts) — o motor não produz o formato que viraliza.",
> 83	            "severity": "critical",
> 84	            "mapsToRequirement": "R1"
> 85	          },
> 86	          {
> 87	            "description": "Zero estratégia VIRAL na geração. Os prompts são hardcoded p/ público B2B 'donos de agências de marketing / ROI com IA' (orchestrate-step:138,290) — o oposto de conteúdo de consumo viral que vende um produto físico. Nenhum hook framework, padrão de gancho, ou formato de engajamento entra no prompt.",
> 88	            "severity": "critical",
> 89	            "mapsToRequirement": "R4"
> 90	          },
> 91	          {
> 92	            "description": "fetch-trends (Apify TikTok/IG, viral_score, engagement_rate, vm_trends) está DESCONECTADO da geração. É uma ilha consumida só pela UI Viral Miner. O motor de geração nunca lê trends p/ pautar/otimizar criativos — quebra a premissa de 'conteúdo viral' baseado em dados de tendência.",
> 93	            "severity": "critical",
> 94	            "mapsToRequirement": "R4"
> 95	          },
> 96	          {
> 97	            "description": "O conteúdo é gerado PRODUCT-UNAWARE e a monetização é um afterthought por regex. monetizeContent só roda no artigo (não no LinkedIn/Twitter), com catálogo hardcoded a 3 produtos (Roborock/Samsung TV/geladeira), linkando a 1ª menção que por acaso apareça no texto. A IA não sabe qual produto está vendendo ao escrever; vm_affiliate_products.commission_value/profitability_score/trend_score existem no schema mas NÃO orientam a escolha do produto. Não há copy de venda construída em torno de um produto específico.",
> 98	            "severity": "critical",
> 99	            "mapsToRequirement": "R4"
> 100	          },
> 101	          {
> 102	            "description": "Usuário não consegue escolher o produto-alvo: o param affiliate_url enviado por useOrchestrationGraph é silenciosamente ignorado por orchestrate-content (nunca desestruturado). A amarração produto↔conteúdo é puramente reativa por regex, não intencional.",
> 103	            "severity": "high",
> 104	            "mapsToRequirement": "R4"
> 105	          },
> 106	          {
> 107	            "description": "As redes 'virais' por excelência (TikTok, Instagram, YouTube) NÃO são destinos de geração — platforms suportadas são só wordpress/linkedin/twitter. fetch-trends scrapeia TikTok/IG mas o pipeline não publica neles. Há publish-meta (IG/FB) no repo mas não está no stepsOrder do orchestrate.",
> 108	            "severity": "high",
> 109	            "mapsToRequirement": "R1"
> 110	          },
> 111	          {
> 112	            "description": "Geração de texto sem etapa de qualidade/viral-scoring do próprio criativo. validateContent só checa tamanho mínimo (article 500/linkedin 50/twitter 30 chars, orchestrate-step:13) — não há avaliação de potencial de engajamento, gancho, ou A/B do criativo antes de publicar.",
> 113	            "severity": "medium",
> 114	            "mapsToRequirement": "R1"
> 115	          },
> 116	          {
> 117	            "description": "generate-image produz só 1024x1024 quadrado com prompt genérico, sem usar a image_url do produto ML (vm_affiliate_products.image_url existe) nem formatos por plataforma. Mesmo se fosse plugada, não geraria criativo de produto consistente.",
> 118	            "severity": "medium",
> 119	            "mapsToRequirement": "R4"
> 120	          }
> 121	        ],
> 122	        "notes": "VEREDITO R1/R4: o pipeline de geração ESTÁ VIVO e materialmente funcional, mas é um gerador de conteúdo B2B-de-blog/social genérico, NÃO um motor de conteúdo VIRAL amarrado a produto ML. Fluxo real: orchestrate-content (dispatcher, cobra 10 mco) → async_orchestrate_step (pg_net) → orchestrate-step executa em cascata article→wordpress→linkedin→twitter→knowledge_mesh, cada formato via LLM tool-calling (llama-3.3-70b por padrão, BYOK per-user), gravando content_library + agendando scheduled_posts. UTM padronizado via utmTag() (orchestrate-step:22). Monetização ML é fail-open e só no artigo.\\n\\nDESCASAMENTO CENTRAL com o objetivo Sovereign (vender Roborock/Samsung via conteúdo viral): (1) os prompts vendem 'IA p/ agências de marketing', não os produtos físicos; (2) a IA escreve sem saber qual produto monetizar — o link é colado depois por regex se a menção casar; (3) o sinal viral real (fetch-trends/vm_trends) existe mas está desconectado; (4) não há vídeo (formato viral nº1) nem publicação em TikTok/IG/YouTube. Componentes-prova: orchestrate-step/index.ts:122-501 (geração), _shared/affiliate.ts:15-110 (monetize regex 3 produtos), fetch-trends/index.ts (trends órfãos), migration 20260514040300 (schema rico de comissão não usado pela geração). R2 (agendamento/lote a cada 3 dias) e R3 (loop de melhoria por desempenho) estão FORA do meu escopo — outro auditor cobre. NÃO editei nada (read-only)."
> 123	      },
> 124	      {
> 125	        "subsystem": "Scheduling & Recurring Execution (R2/R3 cadence) — viral content engine",
> 126	        "components": [
> 127	          {
> 128	            "name": "scheduled_posts queue + auto-publish cron",
> 129	            "path": "supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql:158 · scripts/auto-publish-cron.sh · supabase/functions/auto-publish/index.ts:20",
> 130	            "status": "alive",
> 131	            "evidence": "Table scheduled_posts(scheduled_at TIMESTAMPTZ, status post_status DEFAULT 'queued', retry_count) exists and is drained every 5 min by crontab (gcrUX+ubuntu): `*/5 * * * * .../auto-publish-cron.sh` → POST /functions/v1/auto-publish, which SELECTs status='queued' AND scheduled_at<=now() limit 50, marks 'publishing', publishes. This is a one-shot scheduled PUBLISHER of already-generated posts — there is no recurrence column (no next_run, interval, frequency, cron, cadence on this table). It only drains; it never re-fills."
> 132	          },
> 133	          {
> 134	            "name": "orchestrate-step — writer of scheduled_at (the only generation→schedule link)",
> 135	            "path": "supabase/functions/orchestrate-step/index.ts:324 (linkedin) · :402 (twitter)",
> 136	            "status": "partial",
> 137	            "evidence": "After generating content, it inserts scheduled_posts with HARDCODED single offsets: LinkedIn `new Date(Date.now()+3600000)` (now+1h), Twitter `now+7200000` (now+2h). So a generation run schedules exactly ONE future post per platform, ~1-2h out. No multi-day spread, no batch of future dates, no '3 day' notion. R2's 'generate everything at once' is NOT supported (each run = 1 post/platform); R2's 'a batch every 3 days' has no mechanism at all."
> 138	          },
> 139	          {
> 140	            "name": "optimize-schedule edge fn",
> 141	            "path": "supabase/functions/optimize-schedule/index.ts",
> 142	            "status": "partial",
> 143	            "evidence": "JWT-guarded LLM call that RETURNS 5 suggested posting datetimes within the next 7 days (score+reason JSON). It is advisory only — it does NOT write to scheduled_posts, has no recurrence, and the offsets actually used by orchestrate-step (+1h/+2h) ignore it. Pure suggestion surface, not a scheduler."
> 144	          },
> 145	          {
> 146	            "name": "sequences + sequence_enrollments (nurturing drip — generic cadence primitive)",
> 147	            "path": "supabase/migrations/20260603050000_marketing_hub_nurturing.sql:13 · :35",
> 148	            "status": "alive",
> 149	            "evidence": "sequence_enrollments has current_step smallint + next_run_at timestamptz + status('active'|'paused'|'completed'|'opted_out') + idx_enroll_due partial index. sequences.steps jsonb = [{channel,wait_hours,prompt}]. This is a REAL time-spaced cadence engine — the closest existing base for R2/R3 — but it is a FINITE drip over a pre-authored step list, NOT a self-perpetuating loop, and it targets LEAD nurturing (email/social touches per consent), not viral social post generation."
> 150	          },
> 151	          {
> 152	            "name": "nurture-cron + nurture-dispatch (the only recurring generation that exists)",
> 153	            "path": "supabase/migrations/20260603230000_nurture_advance_cron.sql:20 · supabase/functions/nurture-cron/index.ts · supabase/functions/nurture-dispatch/index.ts",
> 154	            "status": "alive",
> 155	            "evidence": "pg_cron job 'nurture-advance' `*/15 * * * *` POSTs nurture-cron (service-role, Vault key), which finds DUE enrollments (status='active' AND next_run_at<=now()) and fans out (concurrency 8, cap 200) to nurture-dispatch. nurture-dispatch (CONSENT-GATED, debits 2 mco) advances: `current_step+1`, `next_run_at = now + (steps[next].wait_hours ?? 24)*3600000`, status='completed' when current_step>=steps.length. So recurrence = arbitrary wait_hours between FINITE steps. CRITICAL: it stops at the end of the step list — it never regenerates a new batch, never re-enters. Could be a foundation for a 3-day generation loop, but as built it does not generate viral social content nor self-refill."
> 156	          },
> 157	          {
> 158	            "name": "campaign-run (campaign fan-out)",
> 159	            "path": "supabase/functions/campaign-run/index.ts",
> 160	            "status": "partial",
> 161	            "evidence": "JWT-guarded, MANUALLY triggered (no cron targets it — only nurture-cron and memory-decay exist in pg_cron). Debits 10 mco, then dispatches ALL ordered campaign_steps to orchestrate-content IN PARALLEL (Promise.allSettled, EdgeRuntime.waitUntil for >8) — i.e. all NOW, no time spacing, no per-step delay, no 'every 3 days'. Header comment OTD-CAMPAIGN-RUN-ASYNC notes synchronous fan-out is an MVP simplification. No recurrence and no analysis of prior performance."
> 162	          },
> 163	          {
> 164	            "name": "self-optimize (R3 feedback-loop candidate)",
> 165	            "path": "supabase/functions/self-optimize/index.ts:60,176 · src/pages/DashboardHome.tsx:317",
> 166	            "status": "partial",
> 167	            "evidence": "Reads campaign_metrics + scheduled_posts + content_library, asks an LLM for recommendations, and INSERTs them into optimization_policy(action_type, action_details, reward). BUT: (1) it is invoked ONLY by a UI button (DashboardHome.tsx:317) — `grep self-optimize scripts/` and crontab are EMPTY, so it is never scheduled/automatic; (2) its output (optimization_policy) is read back ONLY by DashboardHome.tsx:293 for DISPLAY — no generation function (orchestrate-content/orchestrate-step/campaign-run) ever reads optimization_policy. The loop is open: advice is shown to a human, never auto-applied to the next creatives."
> 168	          },
> 169	          {
> 170	            "name": "campaign_metrics (the performance-data source R3 must analyze)",
> 171	            "path": "supabase/migrations/20260402014040_...sql:288 · grep across repo",
> 172	            "status": "dead",
> 173	            "evidence": "Table + RLS INSERT policy exist, but NO application code writes it: repo-wide grep for campaign_metrics with insert/upsert returns only the README doc row and the migration's RLS policy line — zero writer in supabase/functions/, src/hooks/, or scripts/. So real platform engagement (impressions/clicks/ctr/conversions) is never ingested. The R3 'analyze prior performance' loop has no real data to analyze — self-optimize would feed the LLM an empty/near-empty metrics array (it even prompts 'Se não houver dados suficientes, forneça recomendações genéricas')."
> 174	          },
> 175	          {
> 176	            "name": "Recurring GENERATION scheduler ('a batch every 3 days')",
> 177	            "path": "searched: supabase/migrations/, supabase/functions/, src/, scripts/, crontab -l (gcrUX+ubuntu)",
> 178	            "status": "missing",
> 179	            "evidence": "No table column or job expresses recurrence of content GENERATION. grep over migrations for scheduled|next_run|cadence|recurring|interval|recurrence|every_n_days found only: scheduled_posts (publish queue), sequence_enrollments.next_run_at (finite drip), vm_affiliate_products.is_recurring (a COMMISSION attribute, types.ts:2878 — unrelated to time). Only 2 pg_cron jobs exist (memory_decay_fsrs, nurture-advance) and only the OS crontab triggers generation-adjacent work — none of which RE-GENERATES content on a period. 'a cada 3 dias' / '3-day' / 're-generate' / 'lote' appear NOWHERE in functions/src except a BoK queue-overflow projection (docs/bok/mcorch-constellation/bok-agents-system...:309) describing this as a FUTURE concern, not built."
> 180	          }
> 181	        ],
> 182	        "gaps": [
> 183	          {
> 184	            "description": "R2 'a batch every 3 days' (recurring GENERATION cadence) does not exist. There is no scheduler that periodically invokes orchestrate-content/orchestrate-step to PRODUCE new content. The only periodic generation is nurture-cron (every 15 min), which advances a FINITE drip of lead-nurturing messages and stops at the end of the step list — it neither targets viral social posts nor self-refills a new batch. The OS crontab and the 2 pg_cron jobs contain no content-generation recurrence. Confirmed materially: grep of all migrations/functions/src for recurrence vocabulary yields only the publish queue, a finite drip's next_run_at, and an unrelated commission flag.",
> 185	            "severity": "critical",
> 186	            "mapsToRequirement": "R2"
> 187	          },
> 188	          {
> 189	            "description": "R2 'generate everything at once' is also unmet at the scheduling layer: a single orchestrate-step run schedules exactly ONE post per platform at fixed +1h/+2h offsets (orchestrate-step/index.ts:327,406). There is no path that lays down a multi-post calendar of future-dated scheduled_posts in one shot; optimize-schedule suggests times but writes nothing.",
> 190	            "severity": "high",
> 191	            "mapsToRequirement": "R2"
> 192	          },
> 193	          {
> 194	            "description": "R3 self-improvement loop is OPEN, not closed. self-optimize writes advice to optimization_policy, but (a) it is manual-only (no cron — verified empty), so it never runs 'each 3-day cycle'; and (b) NO generation function reads optimization_policy back, so prior-performance insight is never fed into the next creatives. The advice terminates at a dashboard display (DashboardHome.tsx:293).",
> 195	            "severity": "critical",
> 196	            "mapsToRequirement": "R3"
> 197	          },
> 198	          {
> 199	            "description": "R3 has no real performance data to analyze: campaign_metrics has zero application writer across the entire repo (only an RLS INSERT policy + README doc). Platform engagement (impressions/clicks/ctr/conversions) is never ingested, so even if the loop were wired and scheduled, the analysis step would operate on empty data and fall back to 'generic best-practice' recommendations (the function's own prompt admits this).",
> 200	            "severity": "critical",
> 201	            "mapsToRequirement": "R3"
> 202	          },
> 203	          {
> 204	            "description": "A reusable cadence primitive DOES exist and is the natural foundation to build R2/R3 on: sequence_enrollments(next_run_at, current_step, status) + the nurture-advance pg_cron (*/15) + the service-role fan-out pattern in nurture-cron. Building R2/R3 would mean (a) generalizing this from finite lead-drip to a self-refilling content cadence keyed on a 3-day interval, (b) wiring a metrics ingest writer for campaign_metrics, and (c) having the generator read optimization_policy. None of these three bridges exist today.",
> 205	            "severity": "medium",
> 206	            "mapsToRequirement": "cross"
> 207	          }
> 208	        ],
> 209	        "notes": "Bottom line: the gap the directive predicted is CONFIRMED materially. The system has a robust scheduled PUBLISHER (scheduled_posts drained every 5 min by auto-publish) and a real but FINITE time-spaced drip engine for lead nurturing (sequence_enrollments.next_run_at advanced by nurture-cron every 15 min). It has NO recurring GENERATION scheduler — nothing periodically re-invokes content generation, and there is no '3-day cycle' concept anywhere (the only is_recurring in the schema is a Mercado Livre commission attribute on vm_affiliate_products, types.ts:2878). R3's self-improvement loop is structurally open on three independent breaks: self-optimize is manual-only (not scheduled), its output (optimization_policy) is never read by any generator, and the metrics it would analyze (campaign_metrics) have no writer at all. campaign-run dispatches all steps in parallel NOW (no spacing, no recurrence, no prior-performance analysis). The cleanest path to R2/R3 is to generalize the existing nurture cadence primitive (next_run_at + pg_cron fan-out) into a self-refilling 3-day content loop, plus add a campaign_metrics ingest writer and make the generator consume optimization_policy. Evidence anchors: crontab -l (gcrUX & ubuntu) listed; pg_cron schedules = only memory_decay_fsrs (20260425190000) + nurture-advance (20260603230000); recurrence grep over migrations returned no GENERATION scheduler."
> 210	      },
> 211	      {
> 212	        "subsystem": "Mercado Livre Revenue Layer (R4) — afiliados: catálogo de produtos, resolução de link per-user, ledger de cliques e atribuição de receita por postback",
> 213	        "components": [
> 214	          {
> 215	            "name": "process-affiliate-link (POST monetize)",
> 216	            "path": "supabase/functions/process-affiliate-link/index.ts:292-466",
> 217	            "status": "alive",
> 218	            "evidence": "POST autenticado (auth.getUser via userClient). Resolve affiliate_config per-user (affiliate_tag/matt_tool/metadata) por user.id+platform='mercadolivre'+is_active (linhas 336-342). Fail-closed: HTTP 402 mercadolivre_not_configured quando sem affiliate_tag E sem shortlink override (352-365). Constroi matt_word URL (buildMattWordUrl 84-114) ou usa meli.la override; HEAD-probe + self-heal via ML search (371-393); insere affiliate_links e retorna trackedUrl com ?link_id= (407-446). SEM fallback de token global — confirma fechamento OTD-OE661-PER-USER."
> 219	          },
> 220	          {
> 221	            "name": "process-affiliate-link (GET redirect / click tracker)",
> 222	            "path": "supabase/functions/process-affiliate-link/index.ts:162-270",
> 223	            "status": "alive",
> 224	            "evidence": "verify_jwt=false (config.toml:60-61). Dois caminhos: (a) ?link_id= → SELECT affiliate_links.short_url, guarda open-redirect (isMlShortLink || mercadolivre.com regex, 174-175), record_affiliate_click_by_link RPC, 302 (168-183); (b) ?product_id=&content_variant_id= → resolve owner via mcorch_nodes.user_id → affiliate_config per-user → shortlink override OU matt_word, record_affiliate_click RPC, 302 (185-261). Fail-closed para /dashboard/settings?no_config=1 (263-269)."
> 225	          },
> 226	          {
> 227	            "name": "handle-ml-postback (revenue_cents)",
> 228	            "path": "supabase/functions/handle-ml-postback/index.ts:80-366",
> 229	            "status": "partial",
> 230	            "evidence": "Função completa e bem feita: gate HMAC x-signature fail-closed (verifyMpSignature 32-78), 501 se MP_WEBHOOK_SECRET ausente (101-110), idempotência por order_id (226-242), UPDATE affiliate_links.revenue_cents (245-258), INSERT marketing_attribution (266-285), sync mcorch_nodes.revenue_impact + edge ATTRIBUTES_REVENUE_TO (310-344). PARTIAL porque depende de um postback REAL do Mercado Pago/ML que nunca foi provado chegar: o secret é global ('Usuário Zero pilot', OTD-ML-MP-PER-USER aberta, 96-97) e nenhum run E2E com conversão real existe. É infra pronta sem fonte de dados confirmada."
> 231	          },
> 232	          {
> 233	            "name": "link-forge.ts (injeta links de afiliado no conteúdo)",
> 234	            "path": "scripts/link-forge.ts:55-291",
> 235	            "status": "partial",
> 236	            "evidence": "Script Bun CLI manual (uso: bun run scripts/link-forge.ts). Varre mcorch_nodes node_type='content_mesh_asset' project_id='mcorch-affiliate', casa 3 produtos HARDCODED por regex (PRODUCTS[] 56-75: Roborock S8 MLB27834876, Samsung Neo QLED 8K, Family Hub), substitui menções por markdown link ?product_id=&content_variant_id= e cria edges CONTAINS_LINK_FOR. PARTIAL: catálogo de produtos é fixo/hardcoded no script (não lê vm_affiliate_products), e NÃO está em nenhum cron (crontab -l não tem link-forge — confirmado). Roda só por mão humana."
> 237	          },
> 238	          {
> 239	            "name": "affiliate_config (affiliate_tag/app_id/matt_tool)",
> 240	            "path": "supabase/migrations/20260530183000_affiliate_tag_per_user.sql + 20260604150000_affiliate_matt_tool.sql",
> 241	            "status": "alive",
> 242	            "evidence": "ALTER TABLE affiliate_config ADD COLUMN affiliate_tag text (matt_word, per-user, RLS auth.uid()=user_id herdada). matt_tool adicionado em 20260604150000. app_id usado para OAuth (não é o id de afiliado — comentário explícito linhas 5-8). Tabela é base RLS-protegida; resolvida per-user em ambas as funções edge."
> 243	          },
> 244	          {
> 245	            "name": "vm_affiliate_products (catálogo)",
> 246	            "path": "supabase/migrations/20260514040300_viralmind_affiliate_radar.sql:3-31",
> 247	            "status": "alive",
> 248	            "evidence": "Tabela existe com colunas relevantes: external_id, name, price, commission_rate, commission_value, profitability_score (CHECK 0-100), trend_score, product_url, affiliate_template_url, niches[], metadata jsonb, is_active. RLS: 'Authenticated read affiliate products' USING(true) (catálogo compartilhado), service_role gerencia writes (82-85). Lido por useAffiliateProducts e (no GET) por process-affiliate-link para product_url verificado."
> 249	          },
> 250	          {
> 251	            "name": "affiliate_links (revenue_cents, clicks, conversions)",
> 252	            "path": "supabase/migrations/20260415201855_*.sql:48-90",
> 253	            "status": "alive",
> 254	            "evidence": "Colunas: clicks/conversions/revenue_cents INTEGER DEFAULT 0, product_id text, content_id uuid, campaign_id uuid, metadata jsonb. RLS: SELECT own (auth.uid()=user_id), INSERT own, UPDATE/DELETE bloqueados para authenticated (USING false) — só service_role escreve clicks/revenue. Índices em user_id/product_id/campaign_id."
> 255	          },
> 256	          {
> 257	            "name": "record_affiliate_click / _by_link RPC (click ledger OTD-ML-CLICKS)",
> 258	            "path": "supabase/migrations/20260604130000_fix_affiliate_click_content_uuid.sql + 20260604140000_affiliate_click_by_link.sql",
> 259	            "status": "alive",
> 260	            "evidence": "record_affiliate_click(uuid,text,uuid,text): UPDATE-first atomic clicks+1 keyed por owner+product+content (is not distinct from no content_id uuid — corrige bug 22P02 da v1), INSERT se row_count=0. record_affiliate_click_by_link(uuid): clicks+1 por id. Ambas SECURITY DEFINER, search_path='', EXECUTE só service_role (revoke public/anon/authenticated). Chamadas pelo GET redirect. Provam que HOJE contamos cada clique que passa pelo nosso redirect — não cliques no painel ML (ML sem API)."
> 261	          },
> 262	          {
> 263	            "name": "useAffiliateProducts.ts",
> 264	            "path": "src/hooks/useAffiliateProducts.ts:39-71",
> 265	            "status": "alive",
> 266	            "evidence": "Hook display-only TanStack Query lê vm_affiliate_products is_active=true ordenado por profitability_score. isListableProduct gate (39-42): só lista is_active && price!=null && metadata.availability==='available'. hiddenCount expõe quantos foram ocultados (verificação SOP affiliate-catalog-enrichment)."
> 267	          },
> 268	          {
> 269	            "name": "AffiliateProductsPage.tsx",
> 270	            "path": "src/pages/AffiliateProductsPage.tsx",
> 271	            "status": "alive",
> 272	            "evidence": "Painel de catálogo: lista produtos verificados, resolve link via resolveAffiliateLink (shortlink meli.la / matt_word / needs_config), botão Copiar link, dialog para salvar meli.la cravado per-produto (setProductShortlink em metadata.shortlinks). Tudo MANUAL (copy/paste pelo usuário), não alimenta geração de conteúdo."
> 273	          },
> 274	          {
> 275	            "name": "ROIWidget.tsx",
> 276	            "path": "src/components/dashboard/ROIWidget.tsx:22-104",
> 277	            "status": "alive",
> 278	            "evidence": "Lê affiliate_links (revenue_cents, clicks, conversions) por user.id + campaign_metrics + usage_tracking. totalClicks soma metrics+affiliate.clicks (44-45); affiliateRevenueBRL = sum(revenue_cents)/100 (51); ROI = (receita-custo)/custo (58-60). Reflete o click ledger e a receita do postback. Real, per-user."
> 279	          },
> 280	          {
> 281	            "name": "discover-affiliate-products.ts (mineração de produtos)",
> 282	            "path": "scripts/discover-affiliate-products.ts",
> 283	            "status": "partial",
> 284	            "evidence": "Script Bun manual: roda Apify actor karamelo~mercadolivre-scraper por keyword PASSADA À MÃO (argv), filtra MLB+price>=min-price+image+não-usado, com --commit insere em vm_affiliate_products. profitability_score = min(90, 40+log10(price)*10) (89) — heurística baseada SÓ em preço, NÃO em virtualidade/trend/comissão real. SEM cron (crontab só tem affiliate-enrich-cron de 6/6h que re-checa disponibilidade, não descobre novos). Sem seleção automática de produtos 'virais'."
> 285	          },
> 286	          {
> 287	            "name": "orchestrate-content (pipeline de campanha — wiring R4)",
> 288	            "path": "supabase/functions/orchestrate-content/index.ts",
> 289	            "status": "missing",
> 290	            "evidence": "grep por 'affiliate|mercado|matt_word|product|vm_affiliate' no arquivo retorna ZERO ocorrências de wiring de afiliado (só 'utm' e 'link' genéricos). stepsOrder = article_generation, wordpress_publish, linkedin_post, twitter_thread, knowledge_mesh (163) — NÃO há passo de seleção de produto nem de inserção de link de afiliado. O CLAUDE.md afirma 'step 5 = anexar links ML afiliado' mas isso NÃO existe no código atual. O flywheel gera conteúdo que não contém produtos/links monetizáveis."
> 291	          }
> 292	        ],
> 293	        "gaps": [
> 294	          {
> 295	            "description": "SELEÇÃO AUTOMÁTICA DE PRODUTOS 'VIRAIS'/COM COMISSÃO É INEXISTENTE. A descoberta de produtos (discover-affiliate-products.ts) é um CLI manual onde o humano digita a keyword; o único score ('profitability_score') é uma função de log10(preço) — não usa comissão real, trend_score, nem sinal de viralidade. O cron existente (affiliate-enrich-cron.sh, 6/6h) apenas RE-VERIFICA disponibilidade de produtos já no catálogo, não descobre/seleciona novos. Nada escolhe automaticamente produtos com alta comissão ou alto potencial viral para virar conteúdo.",
> 296	            "severity": "critical",
> 297	            "mapsToRequirement": "R4"
> 298	          },
> 299	          {
> 300	            "description": "O CONTEÚDO GERADO NÃO É MONETIZADO AUTOMATICAMENTE. orchestrate-content/index.ts não tem nenhum passo de afiliado (grep: 0 refs a affiliate/product/matt_word) — contrariando o CLAUDE.md que documenta 'step 5: anexar links ML afiliado'. A única monetização é manual: o botão 'Monetizar Links ML' (ContentLibraryPage.tsx:746 handleMonetizeLinks, 1 clique humano por item) que só substitui URLs ML que JÁ ESTEJAM no corpo (ML_URL_RE :744) — e o pipeline nunca insere essas URLs. link-forge.ts (que injetaria links) é CLI manual e não está em nenhum cron. Resultado: a receita R4 depende inteiramente de ação humana; o flywheel autônomo não fecha o loop de monetização.",
> 301	            "severity": "critical",
> 302	            "mapsToRequirement": "R4"
> 303	          },
> 304	          {
> 305	            "description": "ATRIBUIÇÃO DE RECEITA POR CRIATIVO É FRÁGIL/NÃO PROVADA. handle-ml-postback liga revenue a affiliate_links.id via click_id e a um content_mesh_asset via content_id/metadata (OR-filter 290), mas: (a) depende de um postback REAL do Mercado Pago que nunca foi materialmente provado chegar (secret global, OTD-ML-MP-PER-USER aberta); (b) a atribuição ao criativo específico só funciona se o link embutido carregar o content_variant_id correto — o que só o caminho link-forge manual faz. ML não expõe API de cliques (OTD-ML-001), então a única fonte de receita é o postback do Mercado Pago, cuja entrega/configuração no painel não está verificada no repo. Sem o postback funcionando, ROIWidget mostra receita=0 mesmo com vendas reais.",
> 306	            "severity": "critical",
> 307	            "mapsToRequirement": "R4"
> 308	          },
> 309	          {
> 310	            "description": "PRODUTOS HARDCODED EM link-forge.ts (3 SKUs fixos no array PRODUCTS, scripts/link-forge.ts:56-75) DESACOPLADOS do catálogo vm_affiliate_products. O caminho de injeção automática de links usa um catálogo morto/fixo, enquanto o catálogo real minerado (vm_affiliate_products) só é consumido pelo painel manual e pelo GET redirect. As duas metades (catálogo dinâmico ↔ injeção de link) não se falam.",
> 311	            "severity": "high",
> 312	            "mapsToRequirement": "R4"
> 313	          },
> 314	          {
> 315	            "description": "matt_tool/atribuição definitiva não verificável e meli.la cravado é 100% manual. A atribuição 'cravada' (meli.la) exige o usuário colar manualmente o short link gerado no painel ML por produto (AffiliateProductsPage dialog → metadata.shortlinks). Sem isso, usa-se matt_word, cujo efeito sobre a comissão real é admitidamente não-verificável de fora do ML (migration 20260604150000 comentário linhas 5-6). Risco de receita atribuída incorretamente / não-creditada.",
> 316	            "severity": "medium",
> 317	            "mapsToRequirement": "R4"
> 318	          }
> 319	        ],
> 320	        "notes": "VEREDITO R4 (receita ML): a INFRAESTRUTURA de receita está madura e per-user (resolução fail-closed, click ledger atômico, postback HMAC-gated, ROI widget real) — OTD-OE661-PER-USER e OTD-ML-CLICKS realmente fechadas, com prova nos arquivos. PORÉM o LOOP AUTÔNOMO de receita está QUEBRADO em três pontos que impedem R4 'autônomo': (1) não há seleção automática de produtos virais/com comissão (mineração é CLI manual + score só por preço); (2) orchestrate-content NÃO monetiza o conteúdo que gera (zero refs a afiliado; monetização só por botão manual + link-forge CLI fora de cron); (3) a atribuição por criativo depende de um postback Mercado Pago real nunca provado em produção (secret global, sem run E2E com conversão). Onde procurei e NÃO achei: cron de link-forge ou de discover-affiliate-products (crontab -l só tem affiliate-enrich-cron de re-check de disponibilidade); qualquer chamada automática a process-affiliate-link (único caller em src é ContentLibraryPage.tsx:763, manual); qualquer passo de produto/afiliado em orchestrate-content stepsOrder (:163). Pré-requisito para R4 fechar: (a) cron/serviço que selecione produtos do catálogo por comissão+trend e os injete no pipeline; (b) wire de link-forge (ou equivalente) dentro do orchestrate-content para que TODO conteúdo gerado já saia monetizado com content_variant_id; (c) provar materialmente um postback de conversão real chegando e creditando revenue_cents. NB: este escopo é R4; o agendamento por ciclos de 3 dias (R2) e o loop de auto-melhoria por desempenho (R3) ficam fora — mas observo que a ausência de monetização automática no pipeline também os afeta, pois sem link por-criativo o R3 não tem sinal de receita por criativo para otimizar."
> 321	      },
> 322	      {
> 323	        "subsystem": "Loop Auto-Melhorável baseado em desempenho real (R3) — e dependências em R1/R2 que o R3 exigiria",
> 324	        "components": [
> 325	          {
> 326	            "name": "self-optimize (edge fn)",
> 327	            "path": "supabase/functions/self-optimize/index.ts:58-187",
> 328	            "status": "partial",
> 329	            "evidence": "É o único componente que SE PARECE com R3. Lê campaign_metrics (impressions/clicks/engagements/ctr/conversions), scheduled_posts e content_library do usuário (linhas 58-62), manda pra um LLM (llama-3.3-70b) e grava recomendações em optimization_policy (linhas 177-185). MAS: (a) a fonte campaign_metrics é uma tabela SEM nenhum writer de produção (ver abaixo) → roda quase sempre vazia, e o próprio prompt instrui 'Se não houver dados suficientes, forneça recomendações genéricas baseadas em melhores práticas' (linha 76); (b) o output (optimization_policy) NÃO é lido por nenhuma função de geração; (c) é invocado SÓ pelo botão da UI em DashboardHome (src/pages/DashboardHome.tsx:317) — não há cron/script chamando, logo não é autônomo nem a cada 3 dias. Não fecha R3: não há leitura de desempenho real nem reinjeção no próximo criativo."
> 330	          },
> 331	          {
> 332	            "name": "campaign_metrics (tabela de desempenho)",
> 333	            "path": "supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql:119-133",
> 334	            "status": "dead",
> 335	            "evidence": "Tabela existe com colunas de performance (impressions/clicks/engagements/ctr/conversions/spend_cents) e RLS (SELECT/INSERT own). Grep em supabase/functions/, src/ e scripts/ por escrita: ZERO writers. Só leitores: self-optimize:59, src/pages/AnalyticsPage.tsx:95, src/components/dashboard/ROIWidget.tsx:31, src/hooks/useDashboardData.ts:36. AnalyticsPage assume vazio ('Sem dados de métricas para este período', linha 241). É a tabela onde o desempenho real DEVERIA entrar — está morta na ausência de ingestão."
> 336	          },
> 337	          {
> 338	            "name": "optimization_policy (recomendações)",
> 339	            "path": "supabase/functions/self-optimize/index.ts:177-185 + supabase/migrations/20260414150946_850633b4-d676-428c-b2c1-8d0aa8fca4d0.sql",
> 340	            "status": "dead",
> 341	            "evidence": "Gravada por self-optimize com campos action_type/action_details/reward. Único leitor é a UI src/pages/DashboardHome.tsx:289-300 ('Fetch optimization history' — apenas exibe histórico). NENHUMA função de geração (generate-content, orchestrate-content, campaign-run, intent-orchestrate) lê esta tabela. O 'policy' nunca fecha o loop de volta na criação do conteúdo."
> 342	          },
> 343	          {
> 344	            "name": "sync-meta-ads (ingestão de métricas)",
> 345	            "path": "supabase/functions/sync-meta-ads/index.ts:139-176",
> 346	            "status": "partial",
> 347	            "evidence": "Único componente que traz métricas REAIS de fora: chama Graph API /insights (spend/clicks/impressions, últimos 7 dias) e faz upsert em meta_ads_metrics (linha 159). PORÉM: (a) são métricas de ANÚNCIOS PAGOS do Meta Ads, não de posts orgânicos virais publicados pelo motor; (b) grava em meta_ads_metrics, tabela DIFERENTE da campaign_metrics que o self-optimize lê — não há ponte; (c) meta_ads_metrics não é lida por nenhuma função de geração. Não alimenta R3."
> 348	          },
> 349	          {
> 350	            "name": "publish-social / publish-meta (coleta pós-publicação)",
> 351	            "path": "supabase/functions/publish-social/index.ts:214-231 ; supabase/functions/publish-meta/index.ts",
> 352	            "status": "missing",
> 353	            "evidence": "Após publicar, publish-social só seta status:'published' (linha 224) e retorna {success,result}. Grep por metric|insight|like|view|impression|engagement|reach em ambos: ZERO. Não há coleta de likes/views/clicks por post de volta das redes. Sem isso, não existe 'desempenho do conteúdo anterior' real para o R3 analisar."
> 354	          },
> 355	          {
> 356	            "name": "aeo-audit (Answer Engine Optimization)",
> 357	            "path": "supabase/functions/aeo-audit/index.ts:1-70",
> 358	            "status": "partial",
> 359	            "evidence": "Não é performance real: o cabeçalho declara modo 'degraded' (OTD-MH-003) — PERGUNTA AO LLM se a marca seria citada, sem scrape de SERP real (linhas 5-7). Grava snapshot append-only em aeo_audits. Não lê desempenho de posts publicados e não é reinjetado na geração. É visibilidade especulativa, não loop de melhoria."
> 360	          },
> 361	          {
> 362	            "name": "Knowledge Mesh observation nodes (outcome reuse)",
> 363	            "path": "supabase/functions/campaign-run/index.ts:141 ; supabase/functions/intent-orchestrate/index.ts:113",
> 364	            "status": "partial",
> 365	            "evidence": "campaign-run e intent-orchestrate inserem nós node_type:'observation' no mcorch_nodes, mas registram O QUE FOI PLANEJADO/EXECUTADO (intent-plan, run record), não O QUE PERFORMOU. Nenhuma função de geração faz match_mcorch_nodes/select de observations de outcome para informar o próximo criativo (grep em generate-content/orchestrate-content/campaign-run/intent-orchestrate: nenhuma leitura de observation como input). O mesh guarda histórico, não fecha o loop de performance→geração."
> 366	          },
> 367	          {
> 368	            "name": "fetch-trends (descoberta de tendências)",
> 369	            "path": "supabase/functions/fetch-trends/index.ts:11-25",
> 370	            "status": "partial",
> 371	            "evidence": "Puxa tendências externas (apify/rapidapi/mock) — input-side de descoberta de tópicos, NÃO desempenho dos posts próprios do usuário. Útil para R1/R4 (achar tema viral) mas não é o loop auto-melhorável: não mede o que funcionou antes."
> 372	          },
> 373	          {
> 374	            "name": "campaign-run / intent-orchestrate (geração de lote)",
> 375	            "path": "supabase/functions/campaign-run/index.ts ; supabase/functions/intent-orchestrate/index.ts",
> 376	            "status": "partial",
> 377	            "evidence": "Geram conteúdo/cascata (relevante a R1), mas grep por metric|performance|prior|previous|improve|best|engagement|optimization_policy: ZERO leitura. Geram do zero a cada vez, sem condicionar o prompt no desempenho do ciclo anterior. Confirma que R3 não está plugado na geração."
> 378	          },
> 379	          {
> 380	            "name": "Cadência de 3 dias / gerador recorrente autônomo (R2 que R3 depende)",
> 381	            "path": "supabase/functions/auto-publish/index.ts:20-26 ; supabase/migrations/ (cron.schedule)",
> 382	            "status": "missing",
> 383	            "evidence": "Grep por '3 day|72 hour|every 3|cadence|cycle|recurr' em todo o código: nenhuma cadência de 3 dias. Os únicos cron.schedule em migrations são memory_decay_fsrs (FSRS) e nurture_advance (drip de e-mail de leads, a cada 15min). auto-publish apenas publica posts já enfileirados (scheduled_at<=now), não GERA. Não existe cron que GERE conteúdo viral periodicamente — logo o ciclo de 3 dias que dispararia o R3 (analisar→melhorar→gerar próximo lote) não existe."
> 384	          }
> 385	        ],
> 386	        "gaps": [
> 387	          {
> 388	            "description": "R3 NÃO EXISTE como loop fechado. Não há (a) coleta de desempenho real dos posts orgânicos publicados (likes/views/clicks/comentários por post das redes), (b) tabela populada com esse desempenho — campaign_metrics está morta/sem writer, e (c) reinjeção desse desempenho na geração do próximo criativo. self-optimize é o esqueleto mais próximo, mas lê uma tabela vazia, é manual (não tem cron) e seu output (optimization_policy) nunca volta para a geração.",
> 389	            "severity": "critical",
> 390	            "mapsToRequirement": "R3"
> 391	          },
> 392	          {
> ```

## 🤖 Claude *(20:48:35)*


## 🤖 Claude *(20:48:37)*

Excelente — confirmação material rica. Vou ler o restante (cobertura BoK + a síntese final com veredito por requisito + BoK Gate + rota recomendada):

## 🤖 Claude *(20:48:39)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/tasks/wvz1hcque.output",
  "offset": 393,
  "limit": 386
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 393	            "description": "Falta o pré-requisito de R3: ingestão de métricas de POSTS ORGÂNICOS publicados. publish-social/publish-meta marcam 'published' e nunca buscam de volta as estatísticas (Graph API insights de post, IG/FB media insights, etc.). O único sync de métricas (sync-meta-ads) é de Meta Ads PAGO e grava em meta_ads_metrics, tabela desconectada do otimizador. Sem coleta de outcome real, R3 não tem matéria-prima.",
> 394	            "severity": "critical",
> 395	            "mapsToRequirement": "R3"
> 396	          },
> 397	          {
> 398	            "description": "Desconexão de tabelas: o otimizador (self-optimize) lê campaign_metrics; a única ingestão real (sync-meta-ads) escreve meta_ads_metrics. Não há ETL/trigger ligando uma à outra, nem agregação por post→campanha. Mesmo que a coleta existisse, os dados não chegariam ao analisador.",
> 399	            "severity": "high",
> 400	            "mapsToRequirement": "R3"
> 401	          },
> 402	          {
> 403	            "description": "Nenhum prompt de geração recebe 'o que funcionou antes' como input. generate-content/orchestrate-content/campaign-run/intent-orchestrate geram sempre do zero (ou de tendências externas via fetch-trends), sem condicionar nos criativos de melhor desempenho do usuário. Falta o canal performance→prompt que define o caráter 'auto-melhorável'.",
> 404	            "severity": "high",
> 405	            "mapsToRequirement": "R3"
> 406	          },
> 407	          {
> 408	            "description": "Ausência de cadência autônoma de 3 dias (R2) que dispararia o ciclo de melhoria. Não há cron de GERAÇÃO recorrente; auto-publish só drena fila. Sem o gatilho periódico, mesmo que R3 fosse implementado não rodaria sozinho 'a cada 3 dias analisando o ciclo anterior'.",
> 409	            "severity": "high",
> 410	            "mapsToRequirement": "R2"
> 411	          },
> 412	          {
> 413	            "description": "O Knowledge Mesh guarda observation nodes de planos/execuções (campaign-run, intent-orchestrate) mas não de OUTCOMES de performance, e nenhuma geração os relê. A infra de mesh+embeddings poderia servir de memória de 'campanhas vencedoras', mas hoje é write-only para esse fim — não fecha o loop.",
> 414	            "severity": "medium",
> 415	            "mapsToRequirement": "cross"
> 416	          },
> 417	          {
> 418	            "description": "aeo-audit roda em modo 'degraded' (LLM adivinha citação, sem SERP real). Se for considerado proxy de desempenho para R3, é especulativo e não-acionável; precisaria de sinal real para alimentar melhoria de criativo.",
> 419	            "severity": "low",
> 420	            "mapsToRequirement": "R3"
> 421	          }
> 422	        ],
> 423	        "notes": "VEREDITO R3 (loop auto-melhorável por desempenho real): MISSING/PARTIAL — o gap é exatamente o que o Sovereign suspeitava. Existe um esqueleto (self-optimize) que dá a APARÊNCIA de R3, mas é um loop ABERTO em três pontos: (1) entrada sem dados — campaign_metrics não tem nenhum writer de produção (zero .insert/.upsert em functions/src/scripts; só RLS e leitores), então o analisador roda com 'recomendações genéricas' (self-optimize/index.ts:76); (2) saída sem consumo — optimization_policy só é exibida em DashboardHome:289, nunca lida por geração; (3) sem autonomia — self-optimize não tem cron, só botão de UI (DashboardHome:317). O loop ideal seria: publicar→COLETAR métricas reais do post→agregar em campaign_metrics→analisar (self-optimize)→GRAVAR policy→a próxima geração LER a policy/criativos vencedores e ajustar o prompt. Hoje só os passos 'publicar' e 'analisar-vazio' existem; faltam coleta, agregação e reinjeção. O mais próximo de funcional é sync-meta-ads (métricas REAIS, mas de ANÚNCIO PAGO Meta, em tabela desconectada meta_ads_metrics, e não reinjetadas). Recomendação de menor caminho para fechar R3: (a) implementar coletor de insights por post (publish-meta/publish-social retornam post_id → fn agendada busca insights e escreve campaign_metrics); (b) cron de 3 dias (R2) que chama self-optimize por usuário e persiste policy; (c) fazer generate-content/campaign-run lerem optimization_policy + top criativos e injetarem no system prompt. Prova de materialidade: todos os greps de writer/reader citados acima retornaram exatamente os arquivos:linha listados; campaign_metrics CREATE TABLE em 20260402014040...sql:119; nenhum cron.schedule de geração de conteúdo nas 119 migrations."
> 424	      },
> 425	      {
> 426	        "subsystem": "Campaign Orchestration (multi-platform) + Visual Creatives (Canvas Studio) — covers R1/R4 well, R2 partially, R3 only as advisory (no closed loop)",
> 427	        "components": [
> 428	          {
> 429	            "name": "campaign-run edge fn (cascade fan-out)",
> 430	            "path": "supabase/functions/campaign-run/index.ts:44-188",
> 431	            "status": "alive",
> 432	            "evidence": "JWT-guarded; ownership-checks campaigns by user_id (l.66-70); reads ordered campaign_steps (l.73-78); atomic fee deduct_mco_coins=10 (l.83); parallel Promise.allSettled fan-out to orchestrate-content forwarding the JWT so each step self-bills (dispatchStep l.102-123, runBatches l.127-134); async EdgeRuntime.waitUntil path for >8 steps (l.164-172); mesh observation node + infra_health_logs pulse (l.137-159,169). This IS 'fire one campaign → many platform steps at once' = the R2 'gerar tudo de uma vez' primitive."
> 433	          },
> 434	          {
> 435	            "name": "channelToPlatforms mapping",
> 436	            "path": "supabase/functions/campaign-run/index.ts:35-42",
> 437	            "status": "alive",
> 438	            "evidence": "content/affiliate→[wordpress], social→[linkedin,twitter]; email/unknown→[] (blocked up-front l.93-97, never charged). So a single campaign run already dispatches WP article + LinkedIn + X with affiliate links per servable step."
> 439	          },
> 440	          {
> 441	            "name": "campaign_steps / campaigns(ALTER) / marketing_attribution",
> 442	            "path": "supabase/migrations/20260603025256_marketing_hub_campaign_core.sql:16-112",
> 443	            "status": "alive",
> 444	            "evidence": "campaigns ALTERed +intent/+channels/+mesh_node_id (l.16-19); campaign_steps with position/channel/action(generate_content|publish|affiliate_attach)/status, composite tenant FK CASCADE (l.39-53); marketing_attribution links revenue→campaign/lead (l.73-83). NOTE: action CHECK has NO 'analyze' or 'schedule' action — the schema cannot express R3 (analyze prior) nor R2 (3-day stagger) as a step type."
> 445	          },
> 446	          {
> 447	            "name": "orchestrate-step (real content+publish+monetize)",
> 448	            "path": "supabase/functions/orchestrate-step/index.ts:175-418",
> 449	            "status": "alive",
> 450	            "evidence": "Generates WP article + LinkedIn post + X thread via LLM; AUTO-MONETIZE embeds per-owner ML affiliate links via monetizeContent + affiliate_config(affiliate_tag,matt_tool) per user (l.175-199) — solid R4. Inserts scheduled_posts for social (l.324-330,402-409)."
> 451	          },
> 452	          {
> 453	            "name": "Affiliate monetization (R4)",
> 454	            "path": "supabase/functions/orchestrate-step/index.ts:10,181-184 + supabase/functions/_shared/affiliate.ts",
> 455	            "status": "alive",
> 456	            "evidence": "monetizeContent resolves affiliate_config per user_id+platform='mercadolivre'+is_active, fail-open if no affiliate_tag; UTM tags on every link (utmTag l.23). handle-ml-postback writes real revenue into affiliate_links (l.207-211) idempotently. R4 is the most complete requirement."
> 457	          },
> 458	          {
> 459	            "name": "canvas-execute (per-product creatives engine)",
> 460	            "path": "supabase/functions/canvas-execute/index.ts:78,122-123,280",
> 461	            "status": "alive",
> 462	            "evidence": "Generates ONE node per call (requires project_id+node_id+prompt l.122); supports reference_image_urls for visual consistency (refUrls l.758). 'batch' param (l.72) is Higgsfield Soul image-count per single node, NOT multi-product batching."
> 463	          },
> 464	          {
> 465	            "name": "canvas-campaign-build.ts (per-product creative batch)",
> 466	            "path": "scripts/canvas-campaign-build.ts:40-71,188-302",
> 467	            "status": "partial",
> 468	            "evidence": "Manual CLI: 'bun run scripts/canvas-campaign-build.ts <productKey>' — generates base→consistent variation (→opt-in video) for ONE hardcoded product per invocation (PRODUCTS map l.40-71, only 3 products). Idempotent reuse of assets (findExistingAsset l.76-87). This is the closest thing to 'lote de criativos por produto', but it is one-product-per-run, Sovereign-only (magiclink as gabrielcall@gmail.com l.30,200-211), not a UI/scheduled flow, and not driven from the affiliate catalog."
> 469	          },
> 470	          {
> 471	            "name": "findUpstreamImages (visual consistency threading)",
> 472	            "path": "src/lib/canvas-utils.ts:52-65",
> 473	            "status": "alive",
> 474	            "evidence": "Collects up to 4 deduped upstream image URLs from incoming edges → passed as reference_image_urls so model preserves product identity across creatives. Real R1-quality consistency primitive for the Canvas."
> 475	          },
> 476	          {
> 477	            "name": "useCanvasPipeline 'Run All' (DAG batch within a project)",
> 478	            "path": "src/hooks/useCanvasPipeline.ts:50-238",
> 479	            "status": "alive",
> 480	            "evidence": "Topological-layer execution: getTopologicalLayers (l.61,181), Promise.all per layer + waitForNodesToComplete (l.217-221). Generates ALL runnable nodes of ONE canvas at once — batch is per-project, NOT per-product-catalog."
> 481	          },
> 482	          {
> 483	            "name": "optimize-schedule edge fn",
> 484	            "path": "supabase/functions/optimize-schedule/index.ts:42-157",
> 485	            "status": "partial",
> 486	            "evidence": "LLM suggests 5 best posting times in next 7 days per platform/audience (systemPrompt l.68-84) and RETURNS them to the caller (l.155). Advisory only: output is not persisted and NOT consumed by campaign-run/orchestrate-step scheduling. The relevant R2 'when to post' brain exists but is disconnected from the post-scheduling path."
> 487	          },
> 488	          {
> 489	            "name": "self-optimize edge fn (performance analysis → recommendations)",
> 490	            "path": "supabase/functions/self-optimize/index.ts:60-66,end-insert-loop",
> 491	            "status": "partial",
> 492	            "evidence": "Reads campaign_metrics+scheduled_posts+content_library (l.60-66), produces a scored optimization_report and WRITES top-5 recs to optimization_policy (insert loop near end). This is the R3 'analyze performance' brain — BUT it reads campaign_metrics (see gap: never populated) and its output is read only by self-optimize itself + DashboardHome display, never fed back into orchestrate-content/campaign-run to improve the NEXT creatives. Loop is open, not closed."
> 493	          },
> 494	          {
> 495	            "name": "nurture sequences + nurture-advance cron (closest recurrence primitive)",
> 496	            "path": "supabase/migrations/20260603050000_marketing_hub_nurturing.sql:11-62 + 20260603230000_nurture_advance_cron.sql:20-33",
> 497	            "status": "partial",
> 498	            "evidence": "sequences.steps jsonb supports [{channel,wait_hours,prompt}] (l.16) and sequence_enrollments.next_run_at drives a */15 cron→nurture-cron→nurture-dispatch. wait_hours COULD express 72h cadence, but: (a) it is LEAD-scoped + CONSENT-GATED (nurture-dispatch l.71-82), (b) external delivery is email-via-Resend only (l.142-152, social/whatsapp gated='gated'), (c) it does NOT generate creatives nor post to social accounts. Not a viral-content batch scheduler."
> 499	          },
> 500	          {
> 501	            "name": "auto-publish (shell-cron worker for due posts)",
> 502	            "path": "supabase/functions/auto-publish/index.ts:22-30 + scripts/auto-publish-cron.sh",
> 503	            "status": "alive",
> 504	            "evidence": "Picks scheduled_posts where status='queued' AND scheduled_at<=now (l.22-30), marks publishing, dispatches to publish-social. Cron is a shell script not pg_cron. Executes the schedule — but the schedule itself is fixed +1h/+2h offsets (see gap), not a 3-day stagger and not recurring."
> 505	          },
> 506	          {
> 507	            "name": "intent-orchestrate / intent-execute (NL→plan→HITL)",
> 508	            "path": "supabase/functions/intent-orchestrate/index.ts:1-7 + supabase/functions/intent-execute/index.ts",
> 509	            "status": "alive",
> 510	            "evidence": "Translates NL marketing intent into a task plan, policy-engine HITL gate for high-impact actions, persists to intent_plans; sub-steps self-bill. Cost 0 orchestrator. Could be the human entrypoint for 'gere uma campanha viral', but it does not itself implement 3-day recurrence or performance feedback."
> 511	          },
> 512	          {
> 513	            "name": "sync-meta-ads (real ad metrics ingestion)",
> 514	            "path": "supabase/functions/sync-meta-ads/index.ts:139-178",
> 515	            "status": "alive",
> 516	            "evidence": "Pulls Meta insights (spend/clicks/impressions) per user and UPSERTs into meta_ads_metrics (l.159-174). Real performance data EXISTS — but lands in meta_ads_metrics, which self-optimize does NOT read (it reads campaign_metrics). Metrics-table mismatch breaks the R3 data path."
> 517	          },
> 518	          {
> 519	            "name": "campaign_metrics table (R3 input self-optimize reads)",
> 520	            "path": "supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql:288",
> 521	            "status": "dead",
> 522	            "evidence": "grep across supabase/ src/ scripts/ for insert/upsert into campaign_metrics returns ONLY the RLS policy line (l.288) — ZERO code writers. self-optimize reads it (R3 analysis), but it is never populated by any publish/postback/sync path. Real signals live in affiliate_links (revenue) and meta_ads_metrics (ads), neither wired to self-optimize."
> 523	          }
> 524	        ],
> 525	        "gaps": [
> 526	          {
> 527	            "description": "NO 3-day recurrence for content batches. Only two pg_cron jobs exist in migrations: mcorch-stability-decay (memory FSRS, 20260425190000) and nurture-advance (lead drip */15, 20260603230000). There is no cron, schedule table, or 'next_batch_at' that re-fires campaign-run / a creative batch every 72h. A user can 'gerar tudo de uma vez' (one campaign-run) but cannot say 'um lote a cada 3 dias' — that loop does not exist anywhere.",
> 528	            "severity": "critical",
> 529	            "mapsToRequirement": "R2"
> 530	          },
> 531	          {
> 532	            "description": "R3 self-improvement loop is OPEN, not closed. self-optimize analyzes performance and writes recs to optimization_policy, but those recs are consumed ONLY by self-optimize itself + DashboardHome.tsx (display). orchestrate-content/orchestrate-step/campaign-run contain ZERO references to campaign_metrics, optimization_policy, prior/previous/performance/improve (verified by grep). So the NEXT batch of creatives is NOT influenced by the previous batch's results. The analysis exists; the feedback wire into generation does not.",
> 533	            "severity": "critical",
> 534	            "mapsToRequirement": "R3"
> 535	          },
> 536	          {
> 537	            "description": "R3 has no live data source: campaign_metrics (the table self-optimize reads) is never written by any code (only the RLS INSERT policy exists). Real metrics are split across meta_ads_metrics (sync-meta-ads) and affiliate_links revenue (handle-ml-postback), neither of which self-optimize reads. Per-post organic engagement (likes/shares/views) from LinkedIn/Twitter/Meta is not ingested at all. Even the advisory R3 brain runs on an empty/wrong table.",
> 538	            "severity": "high",
> 539	            "mapsToRequirement": "R3"
> 540	          },
> 541	          {
> 542	            "description": "R2 scheduling is hardcoded fixed offsets, not a real schedule. orchestrate-step inserts scheduled_posts with scheduled_at = now+1h (LinkedIn, l.327) and now+2h (Twitter, l.405). It does not stagger across days, does not call optimize-schedule, and accepts no schedule/cadence parameter. campaign-run dispatches everything immediately (or background) — there is no 'spread this batch over the next 3 days' capability.",
> 543	            "severity": "high",
> 544	            "mapsToRequirement": "R2"
> 545	          },
> 546	          {
> 547	            "description": "Per-product creative batching is manual/CLI-only and not catalog-driven. scripts/canvas-campaign-build.ts generates creatives for ONE of 3 hardcoded products per invocation, as the Sovereign via magiclink. There is no UI/edge-function flow that loops over the affiliate catalog (vm_affiliate_products / useAffiliateProducts) to 'gerar um lote de criativos por produto de uma vez'. canvas-execute is single-node; useCanvasPipeline 'Run All' is single-canvas. The R2 'batch of creatives per product at once' is ~30% there (engine + consistency wiring proven) but lacks the orchestration that fans out over products.",
> 548	            "severity": "high",
> 549	            "mapsToRequirement": "R2"
> 550	          },
> 551	          {
> 552	            "description": "Canvas creatives (images/videos) are NOT wired into the social publishing path. orchestrate-step schedules text posts (LinkedIn/Twitter) + WP article; it never attaches vm_canvas_assets media to scheduled_posts. So the visual creatives generated by the Canvas do not flow into the auto-publish→publish-social pipeline. R1 (auto content for social) currently means text-only via orchestration; the cinematic creatives live in a parallel, manually-driven subsystem.",
> 553	            "severity": "medium",
> 554	            "mapsToRequirement": "R1"
> 555	          },
> 556	          {
> 557	            "description": "campaign_steps.action CHECK is limited to generate_content|publish|affiliate_attach (migration l.46). The data model cannot represent an 'analyze previous performance' step or a 'schedule/delay' step, so R2 cadence and R3 feedback cannot be expressed as campaign steps without a schema migration.",
> 558	            "severity": "medium",
> 559	            "mapsToRequirement": "cross"
> 560	          }
> 561	        ],
> 562	        "notes": "READ-ONLY audit; no DB live — schema claims read from supabase/migrations/. Scope = campaign orchestration + visual creatives (R1/R2/R4 partial). VERDICT vs the 4 reqs: R1 (auto content for social) = LARGELY ALIVE for text (campaign-run→orchestrate-step generates WP+LinkedIn+X, auto-monetized) but visual creatives are a separate manual subsystem not wired into publishing. R4 (ML affiliate revenue) = STRONGEST: per-user affiliate_config + monetizeContent + UTM + handle-ml-postback idempotent revenue, all proven. R2 (gerar tudo de uma vez OU lote a cada 3 dias) = HALF: 'tudo de uma vez' EXISTS (one campaign-run fans out all steps); '3-day recurring batch' DOES NOT EXIST (no cron/schedule beyond the 15-min lead-drip nurture-advance; scheduling is fixed +1h/+2h offsets). R3 (analyze prior → improve next) = WEAKEST/ABSENT as a closed loop: self-optimize + optimize-schedule produce advisory recommendations into optimization_policy, but NOTHING in the generation path reads them back, AND the metric source (campaign_metrics) is an unpopulated table while real signals (meta_ads_metrics, affiliate_links) are not fed to the analyzer. Closest reusable recurrence primitive = sequences.steps[].wait_hours + sequence_enrollments.next_run_at + the */15 cron (could be generalized to a 72h content batch), but today it is lead-scoped, consent-gated, email-only and generates no creatives. Bottom line for the viral autonomous engine: R1/R4 solid for text+affiliate; R2 needs a scheduler/cron with a 3-day cadence + a catalog-driven per-product creative fan-out (canvas-campaign-build.ts must become an edge fn that loops the catalog); R3 needs (a) a real per-post engagement ingestion into a single metrics table, and (b) a wire from optimization_policy/metrics back into orchestrate-content's prompt/timing so each cycle improves the next."
> 563	      },
> 564	      {
> 565	        "subsystem": "BoK Coverage Audit — Autonomous Viral Content Engine (R1 auto-gen social · R2 scheduling all-at-once OR batch every 3 days · R3 self-improving loop from past performance · R4 viral + Mercado Livre affiliate) across docs/bok/{post-engine,viral-daily-canvas,viralmind,conteudo-v2,marketing-hub}",
> 566	        "components": [
> 567	          {
> 568	            "name": "viral-daily-canvas — DAILY autonomous social-creative generation (closest to R1)",
> 569	            "path": "docs/bok/viral-daily-canvas/04-frd.md:20 (FR-VDC-001..004); 03-prd.md:38-46 (PR-VDC-001..006)",
> 570	            "status": "partial",
> 571	            "evidence": "FR-VDC-001 'Web Search Scanner' (consultas DIÁRIAS por tendências), FR-VDC-002 'Script Composer' (hook/core/CTA), FR-VDC-003 'Audio Synth TTS', FR-VDC-004 'Video Compositor' (MP4). PR-VDC-001 = 'Rotina diária cron de pesquisa de tendências'. Cobre R1 (geração automática de criativo social) e parte de R2 — mas SÓ na cadência DIÁRIA fixa (04:00 UTC, Gherkin 03-prd.md:58-65). NÃO publica nas redes (entrega à content_library 'pronto para publicação pelo Post Engine' — 03-prd.md:31). Visão diz 'auto-otimiza com base nas tendências do dia' (03-prd.md:11) = otimização por TREND, não por desempenho passado (R3)."
> 572	          },
> 573	          {
> 574	            "name": "post-engine — auto-publish scheduler + analytics collection (R1 distribution + R2 one-shot scheduling)",
> 575	            "path": "docs/bok/post-engine/04-frd.md:20-23 (FR-PE-001..004); 03-prd.md:38-46 (PR-PE-001..006)",
> 576	            "status": "partial",
> 577	            "evidence": "FR-PE-002 'Scheduler Daemon' (varredura periódica de agendamentos → dispara envios em background) + FR-PE-001 OAuth + FR-PE-003 'Publicação de Vídeos' cobrem publicação automática agendada (R1+parte de R2). MAS o agendamento documentado é PONTUAL: usuário escolhe data/hora de um post (03-prd.md:29 'Escolhe a data e hora'; Gherkin 03-prd.md:60 'scheduled para 14:00'). FR-PE-004 'Coletor de Analytics' grava engagement_score — mede desempenho mas NÃO o realimenta na geração. PR-PE-005 (hashtags por trend) é Should-have SEM FR. Nenhuma FR cobre 'gerar tudo de uma vez OU lote a cada 3 dias' nem o loop de melhoria de criativos."
> 578	          },
> 579	          {
> 580	            "name": "R2 — Cadência recorrente configurável (all-at-once OU lote a cada 3 dias)",
> 581	            "path": "grep 'a cada N dias|3 dias|lote|batch|recorrente cadence' em todas as 5 suítes (01-04)",
> 582	            "status": "missing",
> 583	            "evidence": "ZERO FRs descrevem cadência recorrente CONFIGURÁVEL. viral-daily-canvas codifica cadência FIXA diária (cron 04:00 UTC), não 'gerar tudo de uma vez OU a cada 3 dias'. viralmind PRD tem 'Bulk operations: select multiple products → generate links in batch' (03-prd.md:567) e 'Schedule or Publish Now' (03-prd.md:264) — batch é de LINKS de afiliado e schedule é publicação pontual, não agendamento recorrente de geração de conteúdo. marketing-hub campaign-run (FR-MH-004) é disparo one-shot. Nenhuma FR para escolher 'tudo de uma vez' vs 'lote a cada 3 dias'."
> 584	          },
> 585	          {
> 586	            "name": "R3 — Loop de melhoria: analisar desempenho do ciclo anterior para melhorar próximos criativos",
> 587	            "path": "docs/bok/post-engine/01-mrd.md:48,55; viralmind/03-prd.md:31,266-270; marketing-hub/03-prd.md:52 + 01-mrd.md:39,87,96",
> 588	            "status": "missing",
> 589	            "evidence": "Existe forte sinal de VISÃO mas NENHUMA FR concreta fecha o loop. post-engine MRD:55 nomeia 'otimização de hashtags baseada em desempenho recente' como vantagem competitiva e MRD:48 'Feedback de métricas integrado ao GraphRAG' — mas o FRD só entrega FR-PE-004 (coletor de métricas), sem FR que use métricas para gerar/ajustar criativos futuros. viralmind PRD:31 'system that learns and self-optimizes' e o flow 03-prd.md:266-270 termina em 'Performance Dashboard Updates' (dashboard, NÃO re-alimenta geração); FR-022..028 são roadmap. marketing-hub: MR-MH-011 'auto-otimização' (01-mrd.md:96, Medium) + PR-MH-021 'Self-Healing marketing ops' (Could-Have) + 'Self-optimization insight card / Loop de aprendizado' (03-prd.md:52) — NENHUM tem FR no 04-frd.md (FR-MH-001..012 não incluem auto-otimização/aprendizado). O loop auto-melhorável por desempenho passado é o requisito MENOS documentado."
> 590	          },
> 591	          {
> 592	            "name": "R4 — Conteúdo viral + comissão de afiliado (genérico)",
> 593	            "path": "docs/bok/viralmind/04-frd.md:79-81 (FR-024..026); 02-brd.md:55 (BR-007), :62 (BR-014)",
> 594	            "status": "partial",
> 595	            "evidence": "viralmind FR-024 'Affiliate product catalog' (vm_affiliate_products, EPC, profitability_score), FR-025 'Affiliate link generation' (UTM, short_code), FR-026 'Click tracking' (vm_affiliate_clicks → atribuição de receita). BR-014 'todo output carrega vetor de monetização (link de afiliado)'. Cobre R4 conceitualmente. PORÉM FR-024 é schema-only shipped e FR-025/026 são ROADMAP (04-frd.md:75 'Affiliate Radar — partial: schema shipped, UI/Edge roadmap'; BRD:217). Vínculo viral↔afiliado existe na visão mas não numa FR única e construída."
> 596	          },
> 597	          {
> 598	            "name": "R4 — Mercado Livre ESPECIFICAMENTE como rede de afiliado",
> 599	            "path": "docs/bok/viralmind/06-data-model.md:58 (enum vm_affiliate_network inclui 'mercadolivre'); 01-mrd.md:81,132; 02-brd.md:39 (SH-008)",
> 600	            "status": "partial",
> 601	            "evidence": "Mercado Livre aparece SÓ no viralmind, e como item de enum/stakeholder genérico: vm_affiliate_network enum lista 'mercadolivre' entre 12 redes (data-model:58); MRD:81/132 cita ML como rede de afiliado BR; BRD:39 SH-008 lista ML como stakeholder externo. NÃO há FR que trate a integração ML especificamente (catálogo de produtos ML, geração de link com matt_word/matt_tool, atribuição de comissão ML). post-engine/viral-daily-canvas/conteudo-v2/marketing-hub: ZERO menção a Mercado Livre. A especificidade-ML do objetivo Sovereign está apenas como valor de enum, não como requisito funcional."
> 602	          },
> 603	          {
> 604	            "name": "marketing-hub — campaign orchestration (executor reutilizável, não engine viral)",
> 605	            "path": "docs/bok/marketing-hub/04-frd.md:30-34 (FR-MH-004..008)",
> 606	            "status": "partial",
> 607	            "evidence": "FR-MH-004 'campaign-run' (orquestra orchestrate-content por passo), FR-MH-007 'Campaign Attribution' (liga receita a campaign_id), FR-MH-008 'Nurturing Sequences' (cron AVANÇA passos de drip). O cron de FR-MH-008 avança passos de uma sequência de nurturing — NÃO é uma cadência recorrente de GERAÇÃO de conteúdo viral. Atribuição é por campanha/lead, genérica (não ML). Útil como executor (R1 parcial via orchestrate-content) mas não documenta R2 recorrente nem R3 loop nem R4 ML."
> 608	          },
> 609	          {
> 610	            "name": "conteudo-v2 — canvas criativo multimodal (produção, não automação agendada)",
> 611	            "path": "docs/bok/conteudo-v2/04-frd.md:38-104 (FR-001..030)",
> 612	            "status": "alive",
> 613	            "evidence": "Suíte completa e madura para PRODUÇÃO manual no canvas (ImageGenerator, TTS, Video, Recipes, MCP). Mas é geração SOB DEMANDA pelo usuário no canvas — nenhuma FR cobre geração automática agendada (R1/R2), análise de desempenho (R3) ou afiliado/ML (R4). Único hit de 'a cada' é narrativo no MRD:20. Fora do escopo do motor viral autônomo, exceto como fornecedor de Edge Functions de geração (generate-image/video) reutilizáveis."
> 614	          }
> 615	        ],
> 616	        "gaps": [
> 617	          {
> 618	            "description": "VEREDITO BoK GATE: o 'motor de conteúdo viral auto-melhorável, agendado a cada 3 dias' NÃO está documentado de ponta a ponta em nenhum suite. As 4 partes estão FRAGMENTADAS e PARCIAIS: R1 (geração auto) ≈ viral-daily-canvas FR-VDC-001..004 + post-engine FR-PE-001..003 (publicação); R4 (afiliado) ≈ viralmind FR-024..026 (mas FR-025/026 roadmap). R2 (cadência configurável tudo-de-uma-vez OU a cada 3 dias) e R3 (loop de melhoria por desempenho passado) NÃO têm FR em suite algum. Conclusão: é feature NOVA que exige emenda BoK — NÃO basta o existente.",
> 619	            "severity": "critical",
> 620	            "mapsToRequirement": "cross"
> 621	          },
> 622	          {
> 623	            "description": "R2 sem documentação: nenhuma FR descreve agendamento RECORRENTE CONFIGURÁVEL ('gerar tudo de uma vez OU lote a cada 3 dias'). viral-daily-canvas só tem cron DIÁRIO FIXO (FR-VDC-001, 04:00 UTC); post-engine FR-PE-002 agenda posts PONTUAIS por data/hora. Falta documentar: (a) escolha de modo all-at-once vs batch-cadence; (b) intervalo configurável (N dias, default 3); (c) entidade de 'plano de cadência'/'schedule recorrente' persistida; (d) cron que dispara o ciclo a cada N dias por tenant.",
> 624	            "severity": "critical",
> 625	            "mapsToRequirement": "R2"
> 626	          },
> 627	          {
> 628	            "description": "R3 sem documentação (o requisito mais crítico e mais ausente): nenhum FR fecha o loop 'analisa desempenho do ciclo anterior → melhora próximos criativos'. Sinais de VISÃO sem FR: post-engine MRD:55 (otimização por desempenho recente) e MRD:48 (feedback de métricas no GraphRAG) — mas FRD só entrega coleta (FR-PE-004), não a realimentação; viralmind PRD:31 'learns and self-optimizes' e flow termina em dashboard, não re-geração; marketing-hub MR-MH-011/PR-MH-021/'Self-optimization insight card' sem qualquer FR no 04-frd.md. Falta documentar: ingestão de métricas por criativo, feature de 'análise de desempenho do lote anterior', e o mecanismo de injeção desses aprendizados no prompt/seleção de trend/template do próximo ciclo.",
> 629	            "severity": "critical",
> 630	            "mapsToRequirement": "R3"
> 631	          },
> 632	          {
> 633	            "description": "R4 sem especificidade Mercado Livre: ML aparece SÓ no viralmind e apenas como valor de enum (vm_affiliate_network 'mercadolivre', 06-data-model:58) e stakeholder genérico (BRD:39, MRD:81/132). Nenhuma FR documenta a integração ML real (catálogo de produtos ML, geração de link com tag de afiliado matt_word/matt_tool, atribuição de comissão ML por clique/compra). Os outros 4 suites não citam ML. Falta documentar a ponte 'criativo viral → produto ML → link rastreável → comissão atribuída' como FR.",
> 634	            "severity": "high",
> 635	            "mapsToRequirement": "R4"
> 636	          },
> 637	          {
> 638	            "description": "R1 fragmentado entre dois suites sem orquestração documentada: viral-daily-canvas GERA o criativo (mas entrega à content_library, não publica) e post-engine PUBLICA (mas espera um criativo já pronto). Nenhuma FR documenta a costura geração→publicação automática numa única passada autônoma, nem qual suite é dono do orquestrador do ciclo. Risco de gap de integração (criativo gerado mas nunca publicado, ou publicação sem o passo de geração).",
> 639	            "severity": "high",
> 640	            "mapsToRequirement": "R1"
> 641	          },
> 642	          {
> 643	            "description": "Affiliate Radar (R4) está majoritariamente em estado ROADMAP no viralmind: FR-024 schema-only shipped; FR-025 (geração de link) e FR-026 (click tracking/atribuição) marcados roadmap (04-frd.md:75; BRD:217 'sem UI nem Edge Functions'). Construir R4 sobre estas FRs exige primeiro promovê-las de roadmap a construído — débito BoK + implementação.",
> 644	            "severity": "medium",
> 645	            "mapsToRequirement": "R4"
> 646	          }
> 647	        ],
> 648	        "notes": "RECOMENDAÇÃO DO BoK GATE (Closed-Loop / Lei 2): o objetivo Sovereign é uma feature NOVA que cruza 5 suites parciais — NÃO está documentado de ponta a ponta. Caminho mais limpo: rodar /bok-scribe para um suite-mãe novo (ex.: 'viral-autopilot' ou 'viral-engine') que UNIFIQUE R1-R4, OU emendar formalmente os suites existentes assim: (1) R1 — costurar viral-daily-canvas (geração) ↔ post-engine (publicação) com uma FR de orquestração do ciclo; (2) R2 — nova FR de cadência recorrente CONFIGURÁVEL (all-at-once vs lote-a-cada-N-dias, default 3) + entidade de schedule + cron por-tenant (hoje só existe cron diário fixo em viral-daily-canvas e agendamento pontual em post-engine); (3) R3 — nova FR do loop de melhoria que INGERE desempenho (engagement_score já coletado por FR-PE-004) e o REALIMENTA na geração do próximo ciclo (hoje só há visão em MRDs/PRDs, zero FR — é o maior buraco); (4) R4 — promover viralmind FR-025/FR-026 de roadmap→construído e adicionar FR específica de Mercado Livre (link com tag matt_word/matt_tool + atribuição), já que ML hoje é só valor de enum. Materialidade: todas as citações são path:linha de arquivos lidos nesta sessão; FR IDs verificados por leitura direta dos 04-frd.md e por ripgrep (o grep-shim do tool no-opou com -i multi-flag, então usei rg 14.1.1). Suites como conteudo-v2 e marketing-hub são fornecedores de capability (geração/orquestração) reutilizáveis, mas não documentam o motor viral autônomo agendado em si."
> 649	      }
> 650	    ],
> 651	    "synthesis": {
> 652	      "requirementCoverage": [
> 653	        {
> 654	          "requirement": "R1",
> 655	          "title": "Geração automática de conteúdo para redes sociais",
> 656	          "coverage": "partial",
> 657	          "whatExists": "Pipeline de geração VIVO e funcional para TEXTO: orchestrate-content (dispatcher, cobra 10 mco via deduct_mco_coins, supabase/functions/orchestrate-content/index.ts:79,112) → async_orchestrate_step (pg_net) → orchestrate-step executa cascata article_generation→wordpress_publish→linkedin_post→twitter_thread→knowledge_mesh (orchestrate-step/index.ts:28,122-499), cada formato via LLM tool-calling (llama-3.3-70b, BYOK per-user), gravando content_library + agendando scheduled_posts. campaign-run (campaign-run/index.ts:44-188) faz fan-out de campaign_steps→orchestrate-content. Edge fns de mídia EXISTEM (generate-image, generate-video, generate-video-script, generate-audio-script) e os BoK viral-daily-canvas (FR-VDC-001..004: scanner+script+TTS+video) e post-engine (FR-PE-001..003: OAuth+scheduler+publicação vídeo) documentam o ciclo.",
> 658	          "gap": "(1) ZERO geração de VÍDEO/IMAGEM no pipeline automático — stepsOrder só tem texto; generate-image (DALL-E 1024x1024 quadrado) e generate-video/-script são ÓRFÃS (zero callers, verificado por grep). Vídeo vertical 9:16 é o formato viral nº1 e não é produzido. (2) Destinos são só wordpress/linkedin/twitter — TikTok/Instagram/YouTube (as redes virais) NÃO são alvos de publicação, embora fetch-trends scrapeie TikTok/IG. (3) Os criativos visuais do Canvas Studio (vm_canvas_assets) NÃO são anexados a scheduled_posts — vivem num subsistema paralelo manual.",
> 659	          "whatIsNeeded": "Adicionar steps de mídia (imagem 9:16 + vídeo) ao stepsOrder, plugar generate-image/generate-video no pipeline, costurar geração(viral-daily-canvas)→publicação(post-engine) numa passada autônoma, e wirear vm_canvas_assets em scheduled_posts. Adicionar IG/TikTok/YT como plataformas de publicação."
> 660	        },
> 661	        {
> 662	          "requirement": "R2",
> 663	          "title": "Agendamento: gerar tudo de uma vez OU lote a cada 3 dias",
> 664	          "coverage": "partial",
> 665	          "whatExists": "'Tudo de uma vez' EXISTE: um campaign-run dispara TODOS os campaign_steps em paralelo (Promise.allSettled, MAX_PARALLEL_STEPS=8, campaign-run/index.ts). Há um PUBLICADOR agendado robusto: scheduled_posts drenado a cada 5min por auto-publish (crontab gcrUX verificado: `*/5 ... auto-publish-cron.sh`). Existe primitiva de cadência REUTILIZÁVEL: sequence_enrollments.next_run_at + pg_cron 'nurture-advance' */15 (migration 20260603230000) + fan-out service-role (nurture-cron→nurture-dispatch), onde steps[].wait_hours PODERIA expressar 72h. post-engine FR-PE-002 documenta um Scheduler Daemon.",
> 666	          "gap": "O 'lote a cada 3 dias' (cadência RECORRENTE de GERAÇÃO) NÃO EXISTE em lugar nenhum. Verificado: só 2 pg_cron jobs (memory_decay_fsrs 20260425190000 + nurture-advance 20260603230000) e 12 jobs no crontab OS — NENHUM re-invoca geração de conteúdo periodicamente. Não há coluna/tabela de recorrência de geração (o único is_recurring no schema é atributo de COMISSÃO em vm_affiliate_products). O agendamento de posts é hardcoded a offsets fixos +1h (linkedin, orchestrate-step:324) / +2h (twitter, :402); optimize-schedule sugere horários mas NÃO persiste nada. A primitiva nurture é finita (para no fim da lista de steps), lead-scoped, consent-gated, email-only — não se auto-realimenta nem gera criativo viral. NENHUMA FR documenta cadência configurável.",
> 667	          "whatIsNeeded": "Generalizar a primitiva nurture (next_run_at + pg_cron fan-out) num loop de conteúdo AUTO-REFILL keyed em intervalo de 3 dias por tenant: entidade de 'plano de cadência' persistida (modo all-at-once vs batch-N-dias, default 3), cron por-tenant que dispara campaign-run a cada N dias, e um layer de calendário que deita múltiplos scheduled_posts futuros numa passada (consumindo optimize-schedule). Schema campaign_steps.action (CHECK só generate_content|publish|affiliate_attach) precisa de tipo 'schedule'/'delay'."
> 668	        },
> 669	        {
> 670	          "requirement": "R3",
> 671	          "title": "Loop auto-melhorável: analisar desempenho do ciclo anterior para melhorar próximos criativos",
> 672	          "coverage": "missing",
> 673	          "whatExists": "Apenas um ESQUELETO aberto: self-optimize (supabase/functions/self-optimize/index.ts:60) lê campaign_metrics+scheduled_posts+content_library, pede recomendações ao LLM e grava em optimization_policy (:177). Há ingestão REAL de métricas em UM ponto: sync-meta-ads (sync-meta-ads/index.ts:159) traz insights do Meta Ads (PAGO) → meta_ads_metrics. post-engine FR-PE-004 documenta um 'Coletor de Analytics' (engagement_score).",
> 674	          "gap": "O loop é ABERTO em TRÊS quebras independentes, todas verificadas materialmente: (1) ENTRADA SEM DADOS — campaign_metrics (a tabela que self-optimize lê) tem ZERO writers em todo o repo (grep insert/upsert retornou só RLS policy + types.ts); o próprio prompt admite 'recomendações genéricas se não houver dados'. (2) SAÍDA SEM CONSUMO — optimization_policy só é lida por self-optimize e DashboardHome.tsx (DISPLAY); NENHUMA função de geração (orchestrate-content/orchestrate-step/campaign-run/generate-content/intent-orchestrate) lê optimization_policy (grep confirmou zero refs). (3) SEM AUTONOMIA — self-optimize só é chamada pelo botão da UI (DashboardHome.tsx:317); não há cron (o 2º caller, agent-task-execute, lista 'self-optimize' apenas num allowlist de capability e só roda por smoke/seed QA). Métricas reais de POSTS ORGÂNICOS (likes/views/shares por post de LinkedIn/Twitter/Meta) NÃO são coletadas (publish-social só seta status='published', zero coleta). sync-meta-ads escreve em meta_ads_metrics, tabela DESCONECTADA da campaign_metrics que o analisador lê. NENHUMA FR em suite algum documenta o loop de melhoria por desempenho passado — é o requisito MENOS coberto (só visão em MRD/PRD).",
> 675	          "whatIsNeeded": "Construir o loop fechado: (a) coletor de insights por post (post-engine FR-PE-004 como base doc) que, dado post_id retornado por publish-social/publish-meta, busca engagement real e ESCREVE em campaign_metrics (unificar com meta_ads_metrics); (b) cron de 3 dias (R2) que chama self-optimize por tenant e persiste optimization_policy + identifica criativos vencedores; (c) fazer orchestrate-step/campaign-run LEREM optimization_policy + top criativos e injetarem no system prompt do próximo ciclo. Precisa de /bok-scribe — não há FR."
> 676	        },
> 677	        {
> 678	          "requirement": "R4",
> 679	          "title": "Conteúdo viral monetizado com comissão de afiliado do Mercado Livre",
> 680	          "coverage": "partial",
> 681	          "whatExists": "INFRAESTRUTURA de receita ML MADURA e per-user: affiliate_config (affiliate_tag/matt_tool, RLS auth.uid(), migrations 20260530183000/20260604150000); resolução fail-closed em process-affiliate-link POST (HTTP 402 mercadolivre_not_configured) e GET redirect (verify_jwt=false, click tracker via record_affiliate_click/_by_link RPC service-role-only); handle-ml-postback com HMAC gate idempotente que grava affiliate_links.revenue_cents + edge ATTRIBUTES_REVENUE_TO; ROIWidget real per-user. monetizeContent (orchestrate-step:184) embute link ML no ARTIGO. Catálogo vm_affiliate_products tem commission_value/profitability_score/trend_score (migration 20260514040300). BoK FORTE: suite mercado-livre-api/04-frd.md (FR-ML-001..012 documenta resolver item real, gerar short link meli.la, credencial per-user, postback de receita, remover placeholders) + mcorch-constellation/revenue-flywheel.md (topologia content_mesh_asset→revenue_conversion_event→ATTRIBUTES_REVENUE_TO).",
> 682	          "gap": "O LOOP AUTÔNOMO de receita está QUEBRADO em 3 pontos: (1) SELEÇÃO de produto viral/lucrativo INEXISTENTE — discover-affiliate-products.ts é CLI manual (keyword digitada à mão), profitability_score = log10(preço) só, sem usar comissão/trend/viralidade; o cron existente (affiliate-enrich-cron.sh 6/6h) só RE-VERIFICA disponibilidade, não descobre/seleciona. (2) CONTEÚDO É PRODUCT-UNAWARE — orchestrate-content tem ZERO refs a afiliado (grep), contrariando o CLAUDE.md que afirma 'step 5: anexar links ML'; monetizeContent roda SÓ no artigo (não LinkedIn/Twitter), com catálogo HARDCODED a 3 SKUs por regex em _shared/affiliate.ts, colando link na 1ª menção que por acaso casar — a IA escreve sem saber qual produto vende. Os prompts são B2B 'IA para agências de marketing' (orchestrate-step:138,290), não copy de venda de produto físico. (3) O param affiliate_url enviado pela UI (useOrchestrationGraph:50) é SILENCIOSAMENTE IGNORADO (não desestruturado em orchestrate-content:79). (4) Sinal viral (fetch-trends/vm_trends) está DESCONECTADO da geração — é ilha consumida só pela UI Viral Miner. (5) Atribuição depende de postback Mercado Pago real NUNCA provado em produção (secret global, OTD-ML-MP-PER-USER aberta). No BoK, FR-ML-002/005/006/007-009 estão majoritariamente roadmap.",
> 683	          "whatIsNeeded": "(a) Cron/serviço que selecione produtos do catálogo por comissão+trend e os injete no pipeline; (b) tornar a geração PRODUCT-AWARE — passar produto-alvo (id+nome+imagem) ao prompt e construir copy de venda; wirear link-forge/monetizeContent em TODO formato com content_variant_id; (c) reconectar fetch-trends à pauta de geração; (d) honrar affiliate_url da UI; (e) provar materialmente um postback de conversão real creditando revenue_cents. No BoK: promover FR-ML-002/005..009 de roadmap→construído."
> 684	        }
> 685	      ],
> 686	      "bokGate": {
> 687	        "verdict": "new-suite",
> 688	        "reasoning": "O 'motor de conteúdo viral autônomo, agendado a cada 3 dias, auto-melhorável' NÃO está documentado de ponta a ponta em nenhum suite — as 4 partes estão FRAGMENTADAS entre 5+ suites parciais, e os DOIS requisitos que dão caráter ao motor (R2 cadência recorrente configurável + R3 loop de melhoria por desempenho) NÃO têm FR em suite ALGUM (verificado por grep sobre todos os 04-frd.md: a vocabulária de recorrência/auto-melhoria só aparece em FRs não-relacionadas — openclaw audit cadence, vision-mcp batch). Pelo Closed-Loop Protocol (CLAUDE.md) e Lei 2 Survival, isto é feature NOVA cross-cutting que exige /bok-scribe para um suite-mãe (ex.: 'viral-autopilot') que UNIFIQUE R1-R4 e seja dono explícito do orquestrador do ciclo — OU, alternativamente, emendas formais coordenadas aos suites existentes. Recomendo suite novo porque o gap central (R2+R3) não pertence a nenhum suite atual e a costura geração→publicação→análise→re-geração não tem dono documentado, criando risco de gap de integração. R1 e R4 podem ser referenciados/promovidos dos suites existentes em vez de re-documentados.",
> 689	        "relevantSuites": [
> 690	          "docs/bok/viral-daily-canvas/ (R1 geração de criativo diário: FR-VDC-001..004 scanner+script+TTS+video — cadência DIÁRIA fixa 04:00 UTC, NÃO publica)",
> 691	          "docs/bok/post-engine/ (R1 distribuição + R2 parcial: FR-PE-001 OAuth, FR-PE-002 Scheduler Daemon, FR-PE-003 publicação vídeo, FR-PE-004 Coletor de Analytics — base doc para ingestão R3 mas sem realimentação)",
> 692	          "docs/bok/mercado-livre-api/ (R4 plumbing completo: FR-ML-001..012 — item real, short link meli.la, credencial per-user, postback receita; FR-ML-002/005..009 majoritariamente roadmap)",
> 693	          "docs/bok/mcorch-constellation/ (revenue-flywheel.md: topologia de atribuição ATTRIBUTES_REVENUE_TO; roadmap-v1.md 'Flywheel da Riqueza' Dias 24-30 — intenção sem FR)",
> 694	          "docs/bok/viralmind/ (R4 conceitual: FR-024..026 catálogo/link/click — FR-025/026 roadmap; vm_affiliate_network enum inclui 'mercadolivre')",
> 695	          "docs/bok/marketing-hub/ (executor reutilizável: FR-MH-004 campaign-run, FR-MH-007 atribuição, FR-MH-008 nurturing cron — não documenta R2 recorrente nem R3 loop)"
> 696	        ],
> 697	        "documentedCoverage": "R1 PARCIAL por FR-VDC-001..004 (geração) + FR-PE-001..003 (publicação), sem FR de orquestração que costure os dois. R4 documentado por FR-ML-001..012 (mercado-livre-api) + revenue-flywheel.md, com FR-ML-002/005..009 e viralmind FR-025/026 em estado roadmap. R2: NENHUMA FR (só cadência DIÁRIA fixa em viral-daily-canvas, sem 'a cada 3 dias' configurável). R3: NENHUMA FR — só visão em post-engine MRD:48/55, viralmind PRD:31, marketing-hub MR-MH-011/PR-MH-021; é o maior buraco documental.",
> 698	        "whatMustBeDocumented": "Antes de codar, documentar: (1) R1 — FR de orquestração do ciclo costurando viral-daily-canvas(geração)↔post-engine(publicação) numa passada autônoma, com dono explícito; incluir mídia 9:16 e destinos IG/TikTok/YT. (2) R2 — FR de cadência RECORRENTE CONFIGURÁVEL (modo all-at-once vs lote-a-cada-N-dias default 3) + entidade de schedule/plano persistida + cron por-tenant. (3) R3 — FR do loop fechado: ingestão de engagement por criativo (campaign_metrics unificada), análise do lote anterior, e mecanismo de REALIMENTAÇÃO dos aprendizados no prompt/seleção de trend/template do próximo ciclo (hoje optimization_policy é write-only para display). (4) R4 — FR que torne a geração PRODUCT-AWARE (selecionar produto ML por comissão+trend, construir copy em torno dele, embutir link com content_variant_id em TODO formato) + promover FR-ML-002/005..009 de roadmap→construído + provar postback real. Definir orçamento mcoCoins do loop autônomo e ORO triplet."
> 699	      },
> 700	      "recommendedPath": [
> 701	        {
> 702	          "order": 1,
> 703	          "step": "BoK gate primeiro: rodar /bok-scribe para suite-mãe novo 'viral-autopilot' unificando R1-R4 (ou emendas coordenadas), referenciando os suites existentes (mercado-livre-api FR-ML-*, post-engine FR-PE-*, viral-daily-canvas FR-VDC-*). Documentar especialmente R2 (cadência configurável) e R3 (loop fechado) que hoje têm ZERO FR.",
> 704	          "rationale": "Closed-Loop Protocol + Lei 2: feature nova cross-cutting não pode ganhar código antes de MRD/BRD/PRD/FRD/SDD. R2 e R3 são inéditos no BoK — sem isso, improviso vira dívida exponencial.",
> 705	          "buildsOn": "docs/bok/mercado-livre-api/04-frd.md + docs/bok/post-engine/04-frd.md + docs/bok/viral-daily-canvas/04-frd.md",
> 706	          "effort": "M"
> 707	        },
> 708	        {
> 709	          "order": 2,
> 710	          "step": "Tornar a geração PRODUCT-AWARE e monetizar TODO formato (R4): honrar o param product/affiliate_url em orchestrate-content (hoje dropado em :79), passar produto-alvo (id+nome+imagem ML) ao prompt do orchestrate-step e construir copy de venda; estender monetizeContent do artigo para linkedin_post+twitter_thread com content_variant_id por criativo.",
> 711	          "rationale": "Maior alavancagem com menor risco: pipeline já vivo, affiliate_config per-user + monetizeContent + handle-ml-postback já existem. Resolve o descasamento central (conteúdo B2B genérico vs venda de produto ML) e habilita atribuição por criativo que R3 exige.",
> 712	          "buildsOn": "supabase/functions/orchestrate-step/index.ts:184 + supabase/functions/_shared/affiliate.ts",
> 713	          "effort": "M"
> 714	        },
> 715	        {
> 716	          "order": 3,
> 717	          "step": "Reconectar o sinal viral à pauta (R4/R1): fazer orchestrate-content/orchestrate-step lerem vm_trends (fetch-trends) e vm_affiliate_products (por commission_value+trend_score) para SELECIONAR produto e ângulo viral, em vez de topic cru. Substituir os prompts B2B hardcoded por framework de gancho viral de consumo.",
> 718	          "rationale": "fetch-trends/vm_trends já scrapeiam TikTok/IG e calculam viral_score, mas são ilha (só UI Viral Miner). Liga o dado viral existente ao motor sem reconstruir.",
> 719	          "buildsOn": "supabase/functions/fetch-trends/index.ts + supabase/migrations/20260514040300_viralmind_affiliate_radar.sql",
> 720	          "effort": "M"
> 721	        },
> 722	        {
> 723	          "order": 4,
> 724	          "step": "Construir a cadência de 3 dias (R2) generalizando a primitiva nurture: entidade de 'content cadence plan' (modo all-at-once vs N-dias default 3) + pg_cron por-tenant que re-invoca campaign-run a cada N dias (auto-refill, ao contrário do drip finito). Adicionar tipo 'schedule' ao CHECK de campaign_steps.action.",
> 725	          "rationale": "sequence_enrollments.next_run_at + pg_cron nurture-advance */15 + fan-out service-role são o molde exato; só falta auto-refill e desacoplar de lead/consent/email.",
> 726	          "buildsOn": "supabase/migrations/20260603230000_nurture_advance_cron.sql + supabase/functions/nurture-cron/index.ts + supabase/functions/campaign-run/index.ts",
> 727	          "effort": "L"
> 728	        },
> 729	        {
> 730	          "order": 5,
> 731	          "step": "Coletor de engagement por post (R3 ingestão): após publish-social/publish-meta retornarem post_id, fn agendada busca insights reais (likes/views/clicks) e ESCREVE em campaign_metrics (unificar com meta_ads_metrics). Hoje campaign_metrics tem ZERO writers.",
> 732	          "rationale": "Pré-requisito material de R3 documentado em post-engine FR-PE-004; sem dado real o self-optimize roda vazio ('recomendações genéricas').",
> 733	          "buildsOn": "supabase/functions/publish-social/index.ts + supabase/functions/sync-meta-ads/index.ts (padrão de upsert de insights)",
> 734	          "effort": "L"
> 735	        },
> 736	        {
> 737	          "order": 6,
> 738	          "step": "Fechar o loop R3: agendar self-optimize por tenant no cron de 3 dias e fazer orchestrate-step/campaign-run LEREM optimization_policy + top criativos para injetar no system prompt do próximo ciclo. Hoje optimization_policy é write-only para display (DashboardHome).",
> 739	          "rationale": "Transforma o esqueleto self-optimize (já existe, lê metrics, grava policy) de loop aberto em fechado — o caráter 'auto-melhorável'.",
> 740	          "buildsOn": "supabase/functions/self-optimize/index.ts:177 + supabase/functions/orchestrate-step/index.ts",
> 741	          "effort": "M"
> 742	        },
> 743	        {
> 744	          "order": 7,
> 745	          "step": "Adicionar geração de mídia viral (R1): plugar generate-image (refatorar p/ 9:16) e generate-video ao stepsOrder, usar image_url do produto ML como referência, e wirear vm_canvas_assets em scheduled_posts. Adicionar IG/TikTok/YT como destinos de publicação.",
> 746	          "rationale": "Vídeo vertical é o formato viral nº1 e hoje as fns são órfãs (zero callers); canvas-execute + findUpstreamImages já provam consistência visual. Maior esforço/risco, por último.",
> 747	          "buildsOn": "supabase/functions/generate-image/index.ts + supabase/functions/canvas-execute/index.ts + src/lib/canvas-utils.ts (findUpstreamImages)",
> 748	          "effort": "XL"
> 749	        },
> 750	        {
> 751	          "order": 8,
> 752	          "step": "Provar materialmente um postback de conversão ML real (R4): fechar OTD-ML-MP-PER-USER (secret per-user), configurar webhook no painel Mercado Pago e validar revenue_cents creditado no tenant correto via SELECT real.",
> 753	          "rationale": "handle-ml-postback é infra pronta mas sem fonte de dados confirmada; sem postback real o ROI/feedback de receita por criativo (entrada de R3) é zero.",
> 754	          "buildsOn": "supabase/functions/handle-ml-postback/index.ts",
> 755	          "effort": "M"
> 756	        }
> 757	      ],
> 758	      "keyRisks": [
> 759	        "R3 (loop auto-melhorável) é o requisito que o Sovereign mais valoriza e o MENOS pronto: está quebrado em 3 quebras independentes (campaign_metrics sem writer, optimization_policy nunca lida por geradores, self-optimize sem cron). Mesmo construindo R2, sem o coletor de engagement por post o loop roda vazio e o LLM cai em 'recomendações genéricas' — risco de auto-melhoria teatral, não real.",
> 760	        "Custo descontrolado do loop autônomo: cada orchestrate-content cobra 10 mco + sub-steps. Um cron de 3 dias multiplicado por N produtos/plataformas pode drenar saldo silenciosamente. Sem orçamento/kill-switch por ciclo, o motor autônomo vira buraco de mcoCoins.",
> 761	        "Atribuição de receita ML não comprovada em produção: handle-ml-postback depende de postback Mercado Pago real (secret global, OTD-ML-MP-PER-USER aberta) nunca provado. Se não chega, ROIWidget mostra receita=0 mesmo com vendas — e R3 fica sem o sinal de receita-por-criativo para otimizar.",
> 762	        "Conteúdo gerado hoje é B2B 'IA para agências' e product-unaware — o oposto de conteúdo viral de consumo que vende Roborock/Samsung. Risco de o motor escalar volume de conteúdo que NÃO converte (custo sobe, comissão não vem).",
> 763	        "Vídeo (formato viral nº1) e as redes virais (TikTok/IG/YT) estão completamente fora do pipeline; as fns generate-video são órfãs. Risco de o 'motor viral' publicar só texto em WordPress/LinkedIn/X — onde a viralização orgânica é marginal.",
> 764	        "Gap de integração geração→publicação: viral-daily-canvas GERA mas entrega à content_library (não publica) e post-engine PUBLICA mas espera criativo pronto — sem FR de orquestração, risco de criativo gerado nunca publicado (ou publicação sem geração).",
> 765	        "Lei 2 (Processo Antecipado): codar R2/R3 sem SOP/FR documentado reproduz o anti-pattern de 'automatizar bagunça' — a ausência de FR para o loop é o maior débito antes de qualquer linha de código."
> 766	      ],
> 767	      "openQuestionsForSovereign": [
> 768	        "Cadência exata (R2): default a cada 3 dias está correto, ou deve ser configurável por tenant/campanha (ex.: diário, 2/2 dias)? E o modo 'tudo de uma vez' gera quantos criativos por produto/plataforma por disparo?",
> 769	        "Quais redes priorizar (R1): manter WordPress/LinkedIn/Twitter ou priorizar as virais (TikTok/Instagram Reels/YouTube Shorts)? Isso decide se vídeo 9:16 entra no MVP ou fica para fase 2 (impacta esforço XL do passo 7).",
> 770	        "Orçamento mcoCoins do loop autônomo: qual o teto de gasto por ciclo de 3 dias por tenant, e qual o kill-switch quando o saldo cair abaixo de X? Sem isso o cron autônomo pode drenar o saldo.",
> 771	        "Fonte dos produtos ML: seleção automática por comissão+trend a partir de vm_affiliate_products, OU o Sovereign cura uma shortlist de produtos-alvo? E os 3 SKUs hardcoded (Roborock/Samsung TV/Family Hub) são o foco fixo ou só sementes?",
> 772	        "BYOK de modelos no loop: o motor autônomo deve usar a chave per-user do tenant (gasto do tenant) ou uma chave de sistema com rateio? Afeta atribuição de custo no cálculo de ROI por asset (revenue-flywheel.md).",
> 773	        "Definição de 'desempenho' para R3: que sinal alimenta a melhoria — engagement orgânico por post (likes/views/shares), cliques no link de afiliado (já temos click ledger), receita confirmada por postback, ou combinação? Isso define o coletor do passo 5.",
> 774	        "BoK gate: autoriza /bok-scribe para suite-mãe novo 'viral-autopilot' (recomendado), ou prefere emendas formais aos suites existentes (mercado-livre-api + post-engine + viral-daily-canvas)? E quem é o ORO triplet (Owner do blast radius do conteúdo autônomo publicado)?"
> 775	      ]
> 776	    }
> 777	  }
> 778	}
> ```

## 🤖 Claude *(20:49:21)*


## 🤖 Claude *(20:49:44)*

A auditoria voltou completa e materialmente ancorada (cada achado com `path:linha`). O quadro é nítido — e confirma sua intuição: **a infraestrutura de geração e de receita ML existe e está madura, mas o que dá o caráter de "motor viral autônomo" — a cadência recorrente e o loop auto-melhorável — simplesmente não existe.**

## Placar por requisito (prova material)

| Req | Cobertura | Vivo hoje | O buraco real |
|---|---|---|---|
| **R1** — gerar automático p/ redes | 🟡 **parcial** | Pipeline de **texto** vivo: `orchestrate-content` → `orchestrate-step` gera artigo+LinkedIn+X (LLM tool-calling, BYOK) e agenda em `scheduled_posts` | **Zero vídeo/imagem** no fluxo — `generate-image`/`generate-video` são **órfãs** (zero callers). Só publica WP/LinkedIn/X — **TikTok/IG/YT ficam de fora**. Criativos do Canvas **não** entram no publish |
| **R2** — tudo de uma vez **ou** a cada 3 dias | 🟡 **parcial** | "Tudo de uma vez" **existe** (`campaign-run` faz fan-out paralelo). Publicador agendado robusto (`auto-publish` cron 5/5min) | **A recorrência "a cada 3 dias" não existe em lugar nenhum.** Só 2 pg_cron (memory-decay + nurture-drip 15min) — **nenhum re-gera conteúdo**. Agendamento é offset fixo +1h/+2h hardcoded |
| **R3** — analisar o anterior → melhorar o próximo | 🔴 **ausente** | Só um **esqueleto** (`self-optimize` lê métricas → grava `optimization_policy`) | Loop **aberto em 3 quebras**: `campaign_metrics` tem **zero writers** (roda vazio); `optimization_policy` **nunca é lida por nenhum gerador**; `self-optimize` **não tem cron** (só botão de UI). Engajamento orgânico por post **nunca é coletado** |
| **R4** — viral + comissão ML | 🟡 **parcial** | Receita ML **madura**: `affiliate_config` per-user, click ledger atômico, `handle-ml-postback` HMAC idempotente, ROIWidget real | Conteúdo é **product-unaware**: monetiza **só o artigo**, catálogo **hardcoded a 3 SKUs** por regex, cola link na 1ª menção. `affiliate_url` da UI é **silenciosamente ignorado**. Sinal viral (`fetch-trends`) está **desconectado**. Prompts são **B2B "IA p/ agências"**, não venda de produto físico |

## A leitura estratégica

O sistema hoje é um **gerador de blog/social B2B genérico com plumbing de afiliado ML maduro** — não um motor de conteúdo **viral** amarrado a produto. Os três descasamentos que matam o objetivo:

1. **A IA escreve sem saber qual produto vende.** O link ML é colado *depois*, por regex, e só no artigo. As métricas ricas do catálogo (`commission_value`, `trend_score`, `profitability_score`) existem no schema mas **não orientam nada**.
2. **Não há gatilho recorrente.** Ninguém re-dispara geração a cada 3 dias. O molde existe (a cadência do nurturing: `next_run_at` + pg_cron + fan-out service-role), mas é finito, lead-scoped e só e-mail.
3. **O loop não fecha.** `self-optimize` é teatro: analisa uma tabela vazia e a recomendação morre num display. Nada do desempenho passado volta para o prompt do próximo criativo.

## 🚦 BoK Gate (Closed-Loop / Lei 2)

**Veredito: feature NOVA cross-cutting.** Os dois requisitos que definem o motor — **R2 (cadência configurável) e R3 (loop de melhoria) não têm UMA ÚNICA FR em suite algum** (verificado por grep em todos os `04-frd.md`; só visão solta em MRDs/PRDs). R1 e R4 estão fragmentados e parciais entre 5 suites (`viral-daily-canvas`, `post-engine`, `mercado-livre-api`, `viralmind`, `marketing-hub`).

Pelo Protocolo Mestre, **não posso codar isto antes de selar a Fonte da Verdade.** A rota recomendada de 8 passos já está mapeada (do maior alavancagem ao menor risco: gate → geração product-aware → reconectar trends → cadência 3 dias → coletor de engajamento → fechar loop R3 → mídia viral → provar postback).

Antes de eu acionar o `/bok-scribe`, preciso de 4 decisões suas que parametrizam a Fonte da Verdade inteira:

## 🤖 Claude *(20:50:02)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "Como destravar o BoK Gate para o motor viral aut\u00f4nomo? (R2 cad\u00eancia + R3 loop n\u00e3o t\u00eam FR em nenhum suite \u2014 \u00e9 feature nova cross-cutting)",
      "header": "BoK Gate",
      "multiSelect": false,
      "options": [
        {
          "label": "/bok-scribe suite novo 'viral-autopilot'",
          "description": "Suite-m\u00e3e novo que UNIFICA R1-R4 e \u00e9 dono expl\u00edcito do orquestrador do ciclo, referenciando os suites existentes (mercado-livre-api, post-engine, viral-daily-canvas). Recomendado \u2014 o gap central (R2+R3) n\u00e3o pertence a nenhum suite atual."
        },
        {
          "label": "Emendas aos suites existentes",
          "description": "Emendar formalmente post-engine + mercado-livre-api + viral-daily-canvas em vez de criar suite novo. Mais espalhado, risco de gap de integra\u00e7\u00e3o sem dono \u00fanico do ciclo."
        },
        {
          "label": "Override consciente + d\u00e9bito BoK",
          "description": "Pular o gate (precedente: viralmind Sprint 4) e come\u00e7ar j\u00e1 a costura m\u00ednima de R4 (gera\u00e7\u00e3o product-aware), selando o d\u00e9bito BoK no /handoff. Mais r\u00e1pido, menos fundamentado."
        }
      ]
    },
    {
      "question": "Qual o escopo do MVP \u2014 quais formatos e redes entram na primeira fatia?",
      "header": "Escopo MVP",
      "multiSelect": false,
      "options": [
        {
          "label": "Texto+imagem nas redes atuais primeiro",
          "description": "WP/LinkedIn/X com texto monetizado product-aware + imagem; v\u00eddeo 9:16 e TikTok/IG/YT como fase 2. Menor risco \u2014 pipeline j\u00e1 vivo, valida o loop econ\u00f4mico r\u00e1pido. Recomendado."
        },
        {
          "label": "Incluir v\u00eddeo 9:16 + TikTok/IG/YT no MVP",
          "description": "J\u00e1 no MVP: v\u00eddeo vertical (formato viral n\u00ba1) + redes virais. Esfor\u00e7o XL \u2014 generate-video est\u00e1 \u00f3rf\u00e3, exige plugar m\u00eddia + OAuth de novas redes + publish."
        },
        {
          "label": "S\u00f3 texto monetizado + cad\u00eancia (adiar m\u00eddia)",
          "description": "Foco cir\u00fargico em R2+R4+R3 com texto; nenhuma m\u00eddia visual nesta fatia. Mais enxuto, mas conte\u00fado de texto viraliza menos organicamente."
        }
      ]
    },
    {
      "question": "Qual sinal de desempenho deve alimentar o loop auto-melhor\u00e1vel (R3)? (define o coletor a construir)",
      "header": "Sinal R3",
      "multiSelect": true,
      "options": [
        {
          "label": "Cliques no link de afiliado",
          "description": "J\u00e1 temos o click ledger at\u00f4mico (record_affiliate_click). Sinal dispon\u00edvel HOJE, zero coleta nova \u2014 o mais barato para fechar o loop primeiro."
        },
        {
          "label": "Engajamento org\u00e2nico por post",
          "description": "Likes/views/shares por post das redes. Exige coletor novo (publish-* retorna post_id \u2192 fn agendada busca insights \u2192 campaign_metrics). Sinal mais rico de 'viralidade'."
        },
        {
          "label": "Receita confirmada por postback ML",
          "description": "Convers\u00e3o real creditada por handle-ml-postback. Sinal definitivo de ROI, mas depende de provar o postback Mercado Pago em produ\u00e7\u00e3o (OTD-ML-MP-PER-USER aberta)."
        }
      ]
    },
    {
      "question": "De onde v\u00eam os produtos ML que viram conte\u00fado?",
      "header": "Produtos ML",
      "multiSelect": false,
      "options": [
        {
          "label": "Sele\u00e7\u00e3o autom\u00e1tica por comiss\u00e3o+trend",
          "description": "Motor escolhe de vm_affiliate_products rankeando por commission_value + trend_score + profitability_score. Mais aut\u00f4nomo \u2014 fecha o flywheel sem m\u00e3o humana. Recomendado."
        },
        {
          "label": "Sovereign cura uma shortlist",
          "description": "Voc\u00ea define os produtos-alvo; o motor gera em torno deles. Mais controle de marca/foco, menos aut\u00f4nomo."
        },
        {
          "label": "Manter os 3 SKUs semente por ora",
          "description": "Roborock S8 / Samsung Neo QLED / Family Hub como foco fixo inicial, expandir depois. Mais simples para validar o loop antes de escalar cat\u00e1logo."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "Como destravar o BoK Gate para o motor viral autônomo? (R2 cadência + R3 loop não têm FR em nenhum suite — é feature nova cross-cutting)"="/bok-scribe suite novo 'viral-autopilot'", "Qual o escopo do MVP — quais formatos e redes entram na primeira fatia?"="Texto+imagem nas redes atuais primeiro", "Qual sinal de desempenho deve alimentar o loop auto-melhorável (R3)? (define o coletor a construir)"="Cliques no link de afiliado,Engajamento orgânico por post,Receita confirmada por postback ML", "De onde vêm os produtos ML que viram conteúdo?"="Manter os 3 SKUs semente por ora". You can now continue with these answers in mind.
> ```

## 🤖 Claude *(20:54:06)*


## 🤖 Claude *(20:54:10)*

Decisões registradas. O caminho está selado:

- **BoK Gate** → `/bok-scribe` suite-mãe novo **`viral-autopilot`** unificando R1-R4 ✅
- **MVP** → texto + imagem nas redes atuais (WP/LinkedIn/X); vídeo 9:16 + TikTok/IG/YT em fase 2
- **Sinal R3** → **combo completo**: cliques de afiliado (já temos) + engajamento orgânico (coletor novo) + receita por postback ML
- **Produtos** → 3 SKUs semente (Roborock S8 / Samsung Neo QLED / Family Hub) para validar o loop antes de escalar catálogo

Pelo Protocolo Mestre, o próximo passo obrigatório é **selar a Fonte da Verdade antes de qualquer linha de código**. Vou gravar a diretiva na memória de projeto e acionar o `/bok-scribe` parametrizado por essas 4 decisões + os achados materiais da auditoria.

## 🤖 Claude *(20:54:31)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_viral_autopilot.md",
  "content": "---\nname: project_viral_autopilot\ndescription: Motor de conte\u00fado viral aut\u00f4nomo monetizado (afiliado ML) \u2014 auditoria material + 4 decis\u00f5es Sovereign + BoK gate (suite novo viral-autopilot)\nmetadata:\n  type: project\n---\n\nDiretiva Sovereign 2026-06-17: construir o **motor de conte\u00fado viral aut\u00f4nomo** \u2014 o cora\u00e7\u00e3o de receita do MCORCH. Quatro requisitos:\n- **R1** gerar conte\u00fado p/ redes sociais automaticamente \u00b7 **R2** agendar (tudo de uma vez OU lote a cada 3 dias) \u00b7 **R3** a cada ciclo analisar o desempenho anterior p/ melhorar os pr\u00f3ximos criativos (loop auto-melhor\u00e1vel) \u00b7 **R4** conte\u00fado viral com comiss\u00e3o de afiliado do Mercado Livre.\n\n**Auditoria material (workflow 7-agentes, 2026-06-17 \u2014 cada achado com path:linha):**\n- **R1 parcial:** pipeline de TEXTO vivo (`orchestrate-content`\u2192`orchestrate-step` gera artigo+LinkedIn+X). `generate-image`/`generate-video` s\u00e3o \u00d3RF\u00c3S (zero callers); s\u00f3 publica WP/LinkedIn/X; Canvas assets n\u00e3o entram no publish.\n- **R2 parcial:** \"tudo de uma vez\" existe (`campaign-run` fan-out). **A recorr\u00eancia \"a cada 3 dias\" N\u00c3O existe** \u2014 s\u00f3 2 pg_cron (memory-decay + nurture-drip), nenhum re-gera. Agendamento \u00e9 offset fixo +1h/+2h hardcoded.\n- **R3 ausente:** loop aberto em 3 quebras \u2014 `campaign_metrics` tem ZERO writers (roda vazio); `optimization_policy` nunca lida por gerador; `self-optimize` sem cron (s\u00f3 bot\u00e3o UI). Engajamento org\u00e2nico por post nunca coletado.\n- **R4 parcial:** receita ML madura (`affiliate_config` per-user, click ledger, `handle-ml-postback` HMAC). MAS conte\u00fado \u00e9 product-unaware \u2014 monetiza s\u00f3 o artigo, cat\u00e1logo hardcoded 3 SKUs por regex; `affiliate_url` da UI ignorado; `fetch-trends`/`vm_trends` desconectados; prompts s\u00e3o B2B \"IA p/ ag\u00eancias\", n\u00e3o venda de produto f\u00edsico.\n\n**3 descasamentos centrais:** (1) a IA escreve sem saber qual produto vende; (2) n\u00e3o h\u00e1 gatilho recorrente (molde = cad\u00eancia nurturing `next_run_at`+pg_cron, mas finita/lead/email); (3) o loop n\u00e3o fecha \u2014 desempenho passado nunca volta ao prompt.\n\n**4 decis\u00f5es Sovereign (parametrizam o BoK):**\n1. **BoK Gate** = `/bok-scribe` suite-m\u00e3e NOVO `viral-autopilot` unificando R1-R4 (R2 cad\u00eancia + R3 loop n\u00e3o t\u00eam FR em suite algum).\n2. **MVP** = texto+imagem nas redes ATUAIS (WP/LinkedIn/X) primeiro; v\u00eddeo 9:16 + TikTok/IG/YT = fase 2.\n3. **Sinal R3** = combo completo (cliques afiliado [j\u00e1 temos] + engajamento org\u00e2nico [coletor novo] + receita postback ML).\n4. **Produtos** = 3 SKUs semente (Roborock S8 / Samsung Neo QLED 8K / Family Hub) por ora, escalar cat\u00e1logo depois.\n\n**Rota recomendada (8 passos, do maior alavancagem):** 1 BoK gate \u2192 2 gera\u00e7\u00e3o product-aware (honrar param produto, monetizar TODO formato c/ content_variant_id) \u2192 3 reconectar `fetch-trends`/`vm_affiliate_products` \u00e0 pauta \u2192 4 cad\u00eancia 3 dias (generalizar primitiva nurture, auto-refill) \u2192 5 coletor de engajamento por post \u2192 6 fechar loop R3 (gerador l\u00ea `optimization_policy`) \u2192 7 m\u00eddia viral 9:16 (fase 2) \u2192 8 provar postback ML real (OTD-ML-MP-PER-USER).\n\n**Riscos:** custo descontrolado do cron aut\u00f4nomo (precisa teto mcoCoins + kill-switch por ciclo); R3 pode virar \"auto-melhoria teatral\" se rodar sem dado real; postback ML nunca provado em prod.\n\nSuites a referenciar/promover: [[project_marketing_hub_v2]] (campaign-run executor), mercado-livre-api FR-ML-*, post-engine FR-PE-*, viral-daily-canvas FR-VDC-*. Relacionado: [[project_orchestrate_pipeline_repair]] (pipeline async), [[project_authenticated_browser_operator]] (atribui\u00e7\u00e3o ML), [[project_mcoin_calibration]] (custo por run).\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_viral_autopilot.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(20:54:34)*

Agora o pointer no índice de memória e o disparo do `/bok-scribe`:

## 🤖 Claude *(20:54:39)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md",
  "old_string": "# Memory Index\n\n- [Unified Sensorial Canvas \u2014 Phase Epsilon V9",
  "new_string": "# Memory Index\n\n- [Motor de conte\u00fado viral aut\u00f4nomo (viral-autopilot) \u2014 auditoria + 4 decis\u00f5es + BoK gate](project_viral_autopilot.md) \u2014 Diretiva Sovereign 2026-06-17: alimentar redes com conte\u00fado viral auto-gerado/agendado (R1-R4), monetizado c/ afiliado ML. Auditoria 7-agentes provou: R1/R4 parciais (texto vivo + receita ML madura), **R2 recorr\u00eancia 3-dias N\u00c3O existe**, **R3 loop auto-melhor\u00e1vel ausente** (campaign_metrics sem writer \u00b7 optimization_policy nunca lida \u00b7 self-optimize sem cron). Decis\u00f5es: BoK suite NOVO viral-autopilot \u00b7 MVP texto+imagem WP/LinkedIn/X (v\u00eddeo/TikTok fase 2) \u00b7 sinal R3 combo \u00b7 3 SKUs semente. Rota 8 passos.\n- [Unified Sensorial Canvas \u2014 Phase Epsilon V9"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(20:54:42)*


## 🤖 Claude *(20:54:43)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md",
  "limit": 5
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Memory Index
> 2	
> 3	- [Unified Sensorial Canvas — Phase Epsilon V9 (Code+Memory+Black Hole numa cena R3F)](project_unified_sensorial_canvas.md) — v6.41.0 2026-06-17: funde Core-Fable+Matrix+Memória em `/dashboard/universe`, ancorado no paper *From AGI to ASI* (Via 4; nó `a576216e`). **3.1-3.4 LIVE** (scaffold + Code Network InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; graphology=cérebro/R3F=corpo). **3.5-3.10 pendentes** (sinapses reais · fly-to · perf · poda · paridade+gate E2E · seal). Emenda BoK mcorch-constellation (PR-025/FR-043..049/SDD §9). **Gotchas:** "esfera órfã"=spinner `Loader2` (não bug); query do código ~30s c/ 2 canvases (OTD-UCANVAS-PERF); squad-coloring MORTO (0 rows)→podado, Louvain oficial (Decisão B); 3 páginas legadas preservadas até paridade.
> 4	- [Vision MCP — Fatia 1+2 + deepsearch async + Fatia 3 CORE + remainder (PAT UI/Plugin/Registry/caps)](project_vision_mcp.md) — v6.40.0 2026-06-17: MCP nativo vision×deepsearch, container Sovereign Mesh `127.0.0.1:3200` por trás de `mcp.mcorch.com` (CF), 0 edge fns. BoK 9/9 selada. Fatia 1 (ES256 JWKS+sentinel+mesh.search) + Fatia 2 (4 tools billable) + **deepsearch.run/poll async** + **Fatia 3 CORE v6.39.0** (PAT external auth `mcp_access_tokens` SHA-256+scopes-allowlist+365d · LGPD erase `vision_artifacts`/`erase_vision_artifacts` · ⚠️ OTD-VM-026 storage via Storage API não SQL) + **mcp.mcorch.com LIVE pelo CF v6.39.1** (proxy laranja esconde IP `137.131.243.179` + SSL Full + cert self-signed origem + **WAF Skip rule obrigatória** senão CF challenge bloqueia clientes não-browser) + **Fatia 3 remainder v6.40.0** (handoff `c21c53db`, mesh 8922): **PAT UI client-side** (`useMcpTokens` CSPRNG→SHA-256 byte-idêntico ao container, plaintext once, RLS-own + `McpConnectorsCard` Settings→Connectors) + **install Claude Code provado por handshake MCP+PAT REAL da URL pública** (`.mcp.json` `Bearer ${VISION_MCP_PAT}`; PAT do Usuário Zero em `.env`, `export`+reload p/ acender) + **Plugin Zip** (`packages/vision-mcp-plugin/`→`public/plugins/`) + **MCP Registry manifest** `com.mcorch/vision-mcp` (`server.json` schema 2025-12-11; publish gated no DNS TXT) + **OTD-VM-024 FECHADA** (blueprint §8-A: motor dual Firecrawl-scrape + Gemini-grounding-run) + **caps custo** (`deepsearch.run` per-plano 10/25/50 + diário 25/100/500, BYOK bypassa, smoke 3/3 zero-cost). Lições: SHA-256 client (Web Crypto) tem que casar byte-a-byte com node:crypto do container; "funciona no Claude Code" prova-se pelo handshake da URL pública (não loopback/browser); **CF bot-challenge volta 403 text/html no curl cru de asset estático** — confirmar deploy pela origem `--resolve` ou handshake; `supabase gen types --linked` usa PAT em `~/.supabase/access-token` (diff additive antes de aplicar). Falta (gated): OAuth browser-flow (1º tenant externo) · `mistral`/`vision.ocr` (deferidos) · publish DNS no Registry.
> 5	- [Core-Fable — rota, Fable 5 flagship, seletor desacoplado, shader Interstellar](project_core_fable.md) — ex-Core-v2; regras do shader (capturado=preto, sem glow artificial) e do billing (chat localStorage ≠ pref pipeline)
> ```

## 🤖 Claude *(20:54:50)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md",
  "old_string": "# Memory Index\n\n- [Unified Sensorial Canvas \u2014 Phase Epsilon V9 (Code+Memory+Black Hole numa cena R3F)](project_unified_sensorial_canvas.md)",
  "new_string": "# Memory Index\n\n- [Motor de conte\u00fado viral aut\u00f4nomo (viral-autopilot) \u2014 auditoria + 4 decis\u00f5es + BoK gate](project_viral_autopilot.md) \u2014 Diretiva Sovereign 2026-06-17: alimentar redes com conte\u00fado viral auto-gerado/agendado (R1-R4), monetizado c/ afiliado ML. Auditoria 7-agentes provou: R1/R4 parciais (texto vivo + receita ML madura), **R2 recorr\u00eancia 3-dias N\u00c3O existe**, **R3 loop auto-melhor\u00e1vel ausente** (campaign_metrics sem writer \u00b7 optimization_policy nunca lida \u00b7 self-optimize sem cron). Decis\u00f5es: BoK suite NOVO viral-autopilot \u00b7 MVP texto+imagem WP/LinkedIn/X (v\u00eddeo/TikTok fase 2) \u00b7 sinal R3 combo \u00b7 3 SKUs semente. Rota 8 passos.\n- [Unified Sensorial Canvas \u2014 Phase Epsilon V9 (Code+Memory+Black Hole numa cena R3F)](project_unified_sensorial_canvas.md)"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(20:54:53)*

Agora aciono o `/bok-scribe` para selar a Fonte da Verdade do `viral-autopilot`, parametrizado pelas suas 4 decisões e ancorado nos achados materiais da auditoria:

## 🤖 Claude *(20:55:21)*


🛠️ **Tool Call**: `Skill`
```json
{
  "skill": "bok-scribe",
  "args": "viral-autopilot \u2014 Motor de conte\u00fado viral aut\u00f4nomo monetizado com afiliado do Mercado Livre. O cora\u00e7\u00e3o de receita do MCORCH: alimentar contas de redes sociais com conte\u00fado viral gerado automaticamente e agendado, podendo gerar tudo de uma vez OU um lote a cada 3 dias, e a cada ciclo analisar o desempenho do conte\u00fado anterior para melhorar os pr\u00f3ximos criativos.\n\nREQUISITOS-N\u00daCLEO (a documentar de ponta a ponta \u2014 R2 e R3 N\u00c3O t\u00eam FR em nenhum suite existente):\n- R1: gera\u00e7\u00e3o autom\u00e1tica de conte\u00fado para redes sociais.\n- R2: agendamento \u2014 modo \"tudo de uma vez\" OU \"lote a cada N dias\" (default 3), configur\u00e1vel por tenant/campanha.\n- R3: loop AUTO-MELHOR\u00c1VEL \u2014 ingerir o desempenho do ciclo anterior e REALIMENTAR no prompt/sele\u00e7\u00e3o do pr\u00f3ximo criativo (hoje optimization_policy \u00e9 write-only para display; campaign_metrics n\u00e3o tem writer; self-optimize n\u00e3o tem cron).\n- R4: conte\u00fado viral amarrado a produto do Mercado Livre, com link de afiliado per-user e atribui\u00e7\u00e3o de comiss\u00e3o.\n\nDECIS\u00d5ES SOBERANAS (par\u00e2metros fixos da Fonte da Verdade):\n1. Suite-m\u00e3e NOVO 'viral-autopilot' que UNIFICA R1-R4 e \u00e9 dono expl\u00edcito do orquestrador do ciclo (gera\u00e7\u00e3o\u2192publica\u00e7\u00e3o\u2192an\u00e1lise\u2192re-gera\u00e7\u00e3o). Referenciar/promover, sem re-documentar: mercado-livre-api (FR-ML-001..012), post-engine (FR-PE-001..004), viral-daily-canvas (FR-VDC-001..004), viralmind (FR-024..026 afiliado), marketing-hub (FR-MH-004 campaign-run executor).\n2. MVP = TEXTO + IMAGEM nas redes ATUAIS (WordPress/LinkedIn/Twitter-X). V\u00eddeo vertical 9:16 + TikTok/Instagram/YouTube = FASE 2 expl\u00edcita (n\u00e3o MVP).\n3. Sinal de desempenho de R3 = COMBO completo: (a) cliques no link de afiliado (j\u00e1 existe click ledger record_affiliate_click), (b) engajamento org\u00e2nico por post (coletor NOVO: publish-* retorna post_id \u2192 fn agendada busca insights \u2192 grava campaign_metrics), (c) receita confirmada por postback ML (handle-ml-postback).\n4. Produtos ML = 3 SKUs semente por ora (Roborock S8, Samsung Neo QLED 8K, Family Hub), com caminho de expans\u00e3o de cat\u00e1logo (vm_affiliate_products) documentado para depois.\n\nCONTEXTO DE ARQUITETURA EXISTENTE (reusar, n\u00e3o reinventar \u2014 prova material da auditoria 2026-06-17):\n- Gera\u00e7\u00e3o viva: orchestrate-content (dispatcher, cobra 10 mco) \u2192 async_orchestrate_step (pg_net) \u2192 orchestrate-step (article/linkedin/twitter, LLM tool-calling, BYOK per-user). campaign-run faz fan-out de campaign_steps.\n- Receita ML madura per-user: affiliate_config (affiliate_tag/matt_tool), process-affiliate-link (POST monetize fail-closed + GET redirect/click tracker), handle-ml-postback (HMAC idempotente \u2192 affiliate_links.revenue_cents + edge ATTRIBUTES_REVENUE_TO), ROIWidget.\n- Primitiva de cad\u00eancia reutiliz\u00e1vel p/ R2: sequence_enrollments.next_run_at + pg_cron 'nurture-advance' (*/15) + fan-out service-role (nurture-cron\u2192nurture-dispatch) \u2014 HOJE finita/lead-scoped/consent-gated/email; precisa virar auto-refill de conte\u00fado a cada N dias.\n- Esqueleto de R3 (loop aberto): self-optimize l\u00ea campaign_metrics \u2192 grava optimization_policy. Quebras: campaign_metrics SEM writer; optimization_policy nunca lida por gerador; self-optimize SEM cron.\n- Sinal viral existente mas DESCONECTADO: fetch-trends (Apify TikTok/IG \u2192 vm_trends, viral_score). Cat\u00e1logo vm_affiliate_products tem commission_value/trend_score/profitability_score (n\u00e3o usados pela gera\u00e7\u00e3o).\n- Monetiza\u00e7\u00e3o atual \u00e9 afterthought: monetizeContent s\u00f3 no artigo, cat\u00e1logo hardcoded 3 SKUs por regex em _shared/affiliate.ts; param affiliate_url da UI \u00e9 ignorado em orchestrate-content.\n\nRESTRI\u00c7\u00d5ES (Survival Laws + CLAUDE.md):\n- API Tenancy per-user obrigat\u00f3ria (auth.uid()) para toda credencial externa.\n- Custo: cada orchestrate-content cobra 10 mcoCoins + sub-steps; o loop aut\u00f4nomo recorrente PRECISA de teto de gasto por ciclo + kill-switch quando saldo < X (documentar como FR/NFR + FMEA RPN alto).\n- Toda nova migration passa /security-review; multi-tenant user_id+project_id.\n- ORO: Operator=MCORCH Agent; Reviewer=Sovereign; Owner=Sovereign (blast radius = conte\u00fado aut\u00f4nomo publicado em redes reais + gasto de carteira).\n\nGerar a fam\u00edlia BoK completa (00-index, 01-mrd, 02-brd, 03-prd, 04-frd, 05-sdd, 06-data-model, 07-process-flow, 08-quality-metrics) em docs/bok/viral-autopilot/, production-ready, sem placeholders, com FRs expl\u00edcitas para R2 (cad\u00eancia configur\u00e1vel) e R3 (loop fechado de melhoria) que hoje n\u00e3o existem em suite algum."
}
```

> **Tool Result (Skill)** - ✅ Success
>
> ```
> Launching skill: bok-scribe
> ```

## 👤 User *(20:55:21)*

# MCORCH BoK Scribe Agent

You are the **MCORCH BoK Scribe Agent** — the Requirements Engineering layer of the MCORCH
Sovereign Ecosystem. Your role is to act as the translation layer between the
Sovereign/Maestro (the human architect) and the Execution Agents (Claude/Antigravity).

When given a raw business idea in `viral-autopilot — Motor de conteúdo viral autônomo monetizado com afiliado do Mercado Livre. O coração de receita do MCORCH: alimentar contas de redes sociais com conteúdo viral gerado automaticamente e agendado, podendo gerar tudo de uma vez OU um lote a cada 3 dias, e a cada ciclo analisar o desempenho do conteúdo anterior para melhorar os próximos criativos.

REQUISITOS-NÚCLEO (a documentar de ponta a ponta — R2 e R3 NÃO têm FR em nenhum suite existente):
- R1: geração automática de conteúdo para redes sociais.
- R2: agendamento — modo "tudo de uma vez" OU "lote a cada N dias" (default 3), configurável por tenant/campanha.
- R3: loop AUTO-MELHORÁVEL — ingerir o desempenho do ciclo anterior e REALIMENTAR no prompt/seleção do próximo criativo (hoje optimization_policy é write-only para display; campaign_metrics não tem writer; self-optimize não tem cron).
- R4: conteúdo viral amarrado a produto do Mercado Livre, com link de afiliado per-user e atribuição de comissão.

DECISÕES SOBERANAS (parâmetros fixos da Fonte da Verdade):
1. Suite-mãe NOVO 'viral-autopilot' que UNIFICA R1-R4 e é dono explícito do orquestrador do ciclo (geração→publicação→análise→re-geração). Referenciar/promover, sem re-documentar: mercado-livre-api (FR-ML-001..012), post-engine (FR-PE-001..004), viral-daily-canvas (FR-VDC-001..004), viralmind (FR-024..026 afiliado), marketing-hub (FR-MH-004 campaign-run executor).
2. MVP = TEXTO + IMAGEM nas redes ATUAIS (WordPress/LinkedIn/Twitter-X). Vídeo vertical 9:16 + TikTok/Instagram/YouTube = FASE 2 explícita (não MVP).
3. Sinal de desempenho de R3 = COMBO completo: (a) cliques no link de afiliado (já existe click ledger record_affiliate_click), (b) engajamento orgânico por post (coletor NOVO: publish-* retorna post_id → fn agendada busca insights → grava campaign_metrics), (c) receita confirmada por postback ML (handle-ml-postback).
4. Produtos ML = 3 SKUs semente por ora (Roborock S8, Samsung Neo QLED 8K, Family Hub), com caminho de expansão de catálogo (vm_affiliate_products) documentado para depois.

CONTEXTO DE ARQUITETURA EXISTENTE (reusar, não reinventar — prova material da auditoria 2026-06-17):
- Geração viva: orchestrate-content (dispatcher, cobra 10 mco) → async_orchestrate_step (pg_net) → orchestrate-step (article/linkedin/twitter, LLM tool-calling, BYOK per-user). campaign-run faz fan-out de campaign_steps.
- Receita ML madura per-user: affiliate_config (affiliate_tag/matt_tool), process-affiliate-link (POST monetize fail-closed + GET redirect/click tracker), handle-ml-postback (HMAC idempotente → affiliate_links.revenue_cents + edge ATTRIBUTES_REVENUE_TO), ROIWidget.
- Primitiva de cadência reutilizável p/ R2: sequence_enrollments.next_run_at + pg_cron 'nurture-advance' (*/15) + fan-out service-role (nurture-cron→nurture-dispatch) — HOJE finita/lead-scoped/consent-gated/email; precisa virar auto-refill de conteúdo a cada N dias.
- Esqueleto de R3 (loop aberto): self-optimize lê campaign_metrics → grava optimization_policy. Quebras: campaign_metrics SEM writer; optimization_policy nunca lida por gerador; self-optimize SEM cron.
- Sinal viral existente mas DESCONECTADO: fetch-trends (Apify TikTok/IG → vm_trends, viral_score). Catálogo vm_affiliate_products tem commission_value/trend_score/profitability_score (não usados pela geração).
- Monetização atual é afterthought: monetizeContent só no artigo, catálogo hardcoded 3 SKUs por regex em _shared/affiliate.ts; param affiliate_url da UI é ignorado em orchestrate-content.

RESTRIÇÕES (Survival Laws + CLAUDE.md):
- API Tenancy per-user obrigatória (auth.uid()) para toda credencial externa.
- Custo: cada orchestrate-content cobra 10 mcoCoins + sub-steps; o loop autônomo recorrente PRECISA de teto de gasto por ciclo + kill-switch quando saldo < X (documentar como FR/NFR + FMEA RPN alto).
- Toda nova migration passa /security-review; multi-tenant user_id+project_id.
- ORO: Operator=MCORCH Agent; Reviewer=Sovereign; Owner=Sovereign (blast radius = conteúdo autônomo publicado em redes reais + gasto de carteira).

Gerar a família BoK completa (00-index, 01-mrd, 02-brd, 03-prd, 04-frd, 05-sdd, 06-data-model, 07-process-flow, 08-quality-metrics) em docs/bok/viral-autopilot/, production-ready, sem placeholders, com FRs explícitas para R2 (cadência configurável) e R3 (loop fechado de melhoria) que hoje não existem em suite algum.`, you autonomously produce the complete
documentation family using the phased workflow below. All documents are saved as markdown
files under `docs/bok/<project-slug>/`.

---

## Identity

```
Role:       Scientist / Architect Layer
Position:   Between Sovereign vision and Execution implementation
Mandate:    Zero-ambiguity documentation; every output feeds directly into
            Supabase schema, Edge Functions, or n8n process flows
Standards:  BABOK v3 · ProdBOK · CXBOK · SWEBOK v4 · CISSP CBK 2024
            DMBOK v2 · BPM CBOK v4 · CMQ/OE BOK
Output dir: docs/bok/<project-slug>/
```

---

## Phase 0 — Project Bootstrapping

Load the agent definition from `.claude/agents/bok-scribe-agent.md` and execute the
full 7-phase workflow described there.

**Input capture (ask if not provided in viral-autopilot — Motor de conteúdo viral autônomo monetizado com afiliado do Mercado Livre. O coração de receita do MCORCH: alimentar contas de redes sociais com conteúdo viral gerado automaticamente e agendado, podendo gerar tudo de uma vez OU um lote a cada 3 dias, e a cada ciclo analisar o desempenho do conteúdo anterior para melhorar os próximos criativos.

REQUISITOS-NÚCLEO (a documentar de ponta a ponta — R2 e R3 NÃO têm FR em nenhum suite existente):
- R1: geração automática de conteúdo para redes sociais.
- R2: agendamento — modo "tudo de uma vez" OU "lote a cada N dias" (default 3), configurável por tenant/campanha.
- R3: loop AUTO-MELHORÁVEL — ingerir o desempenho do ciclo anterior e REALIMENTAR no prompt/seleção do próximo criativo (hoje optimization_policy é write-only para display; campaign_metrics não tem writer; self-optimize não tem cron).
- R4: conteúdo viral amarrado a produto do Mercado Livre, com link de afiliado per-user e atribuição de comissão.

DECISÕES SOBERANAS (parâmetros fixos da Fonte da Verdade):
1. Suite-mãe NOVO 'viral-autopilot' que UNIFICA R1-R4 e é dono explícito do orquestrador do ciclo (geração→publicação→análise→re-geração). Referenciar/promover, sem re-documentar: mercado-livre-api (FR-ML-001..012), post-engine (FR-PE-001..004), viral-daily-canvas (FR-VDC-001..004), viralmind (FR-024..026 afiliado), marketing-hub (FR-MH-004 campaign-run executor).
2. MVP = TEXTO + IMAGEM nas redes ATUAIS (WordPress/LinkedIn/Twitter-X). Vídeo vertical 9:16 + TikTok/Instagram/YouTube = FASE 2 explícita (não MVP).
3. Sinal de desempenho de R3 = COMBO completo: (a) cliques no link de afiliado (já existe click ledger record_affiliate_click), (b) engajamento orgânico por post (coletor NOVO: publish-* retorna post_id → fn agendada busca insights → grava campaign_metrics), (c) receita confirmada por postback ML (handle-ml-postback).
4. Produtos ML = 3 SKUs semente por ora (Roborock S8, Samsung Neo QLED 8K, Family Hub), com caminho de expansão de catálogo (vm_affiliate_products) documentado para depois.

CONTEXTO DE ARQUITETURA EXISTENTE (reusar, não reinventar — prova material da auditoria 2026-06-17):
- Geração viva: orchestrate-content (dispatcher, cobra 10 mco) → async_orchestrate_step (pg_net) → orchestrate-step (article/linkedin/twitter, LLM tool-calling, BYOK per-user). campaign-run faz fan-out de campaign_steps.
- Receita ML madura per-user: affiliate_config (affiliate_tag/matt_tool), process-affiliate-link (POST monetize fail-closed + GET redirect/click tracker), handle-ml-postback (HMAC idempotente → affiliate_links.revenue_cents + edge ATTRIBUTES_REVENUE_TO), ROIWidget.
- Primitiva de cadência reutilizável p/ R2: sequence_enrollments.next_run_at + pg_cron 'nurture-advance' (*/15) + fan-out service-role (nurture-cron→nurture-dispatch) — HOJE finita/lead-scoped/consent-gated/email; precisa virar auto-refill de conteúdo a cada N dias.
- Esqueleto de R3 (loop aberto): self-optimize lê campaign_metrics → grava optimization_policy. Quebras: campaign_metrics SEM writer; optimization_policy nunca lida por gerador; self-optimize SEM cron.
- Sinal viral existente mas DESCONECTADO: fetch-trends (Apify TikTok/IG → vm_trends, viral_score). Catálogo vm_affiliate_products tem commission_value/trend_score/profitability_score (não usados pela geração).
- Monetização atual é afterthought: monetizeContent só no artigo, catálogo hardcoded 3 SKUs por regex em _shared/affiliate.ts; param affiliate_url da UI é ignorado em orchestrate-content.

RESTRIÇÕES (Survival Laws + CLAUDE.md):
- API Tenancy per-user obrigatória (auth.uid()) para toda credencial externa.
- Custo: cada orchestrate-content cobra 10 mcoCoins + sub-steps; o loop autônomo recorrente PRECISA de teto de gasto por ciclo + kill-switch quando saldo < X (documentar como FR/NFR + FMEA RPN alto).
- Toda nova migration passa /security-review; multi-tenant user_id+project_id.
- ORO: Operator=MCORCH Agent; Reviewer=Sovereign; Owner=Sovereign (blast radius = conteúdo autônomo publicado em redes reais + gasto de carteira).

Gerar a família BoK completa (00-index, 01-mrd, 02-brd, 03-prd, 04-frd, 05-sdd, 06-data-model, 07-process-flow, 08-quality-metrics) em docs/bok/viral-autopilot/, production-ready, sem placeholders, com FRs explícitas para R2 (cadência configurável) e R3 (loop fechado de melhoria) que hoje não existem em suite algum.):**
1. Business idea (free text — what problem does it solve?)
2. Target market segment (B2B / B2C / B2B2C)
3. Monetization model (subscription / transaction / hybrid)
4. Regulatory sensitivity (LGPD / GDPR / financial / healthcare / none)
5. Integration surface (standalone / extends existing MCORCH feature)

Derive `<project-slug>` from the business idea (kebab-case, max 32 chars).
Create `docs/bok/<project-slug>/` if it does not exist.

---

## Execution

After collecting inputs, execute ALL phases in strict sequence. Do NOT skip phases.
Each phase reads the output of the previous phase.

Load full workflow from: `.claude/agents/bok-scribe-agent.md`
Load all document templates from: `.claude/agents/bok-scribe/templates/`

After all phases complete:
1. Print a summary table listing every file created with its purpose.
2. Insert a Knowledge Mesh node (see Phase 7 in agent definition).
3. Confirm: "BoK documentation suite complete for `<project-slug>`."


## 🤖 Claude *(20:55:32)*


## 🤖 Claude *(20:55:33)*

A skill carregou. Vou ler a definição completa do workflow do agente + os templates antes de gerar qualquer documento.

## 🤖 Claude *(20:55:34)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe-agent.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# MCORCH BoK Scribe Agent — Operational Framework
> 2	
> 3	**Version:** 1.0.0  
> 4	**Date:** 2026-05-06  
> 5	**Invocation:** `/bok-scribe <business-idea>`  
> 6	**Output root:** `docs/bok/<project-slug>/`
> 7	
> 8	---
> 9	
> 10	## Agent Identity Contract
> 11	
> 12	```
> 13	Name:         MCORCH BoK Scribe Agent
> 14	Archetype:    Scientist / Architect Layer
> 15	Layer:        Requirements Engineering (between Sovereign and Execution)
> 16	Authority:    Reads from all BoKs; writes only to docs/bok/ and mcorch_nodes
> 17	Restrictions: NEVER writes code. NEVER modifies src/. NEVER touches supabase/functions/.
> 18	              NEVER deducts mcoCoins. Documentation only.
> 19	Language:     Thinking = English. Headings & labels = English.
> 20	              Narrative explanations to Sovereign = Português (Brasil).
> 21	```
> 22	
> 23	---
> 24	
> 25	## Input Schema
> 26	
> 27	```typescript
> 28	interface BokScribeInput {
> 29	  businessIdea:       string   // raw free-text description
> 30	  marketSegment:      'B2B' | 'B2C' | 'B2B2C'
> 31	  monetizationModel:  'subscription' | 'transaction' | 'hybrid'
> 32	  regulatoryProfile:  'LGPD' | 'GDPR' | 'financial' | 'healthcare' | 'none'
> 33	  integrationSurface: 'standalone' | 'extends-mcorch'
> 34	  projectSlug:        string   // derived: kebab-case, max 32 chars
> 35	}
> 36	```
> 37	
> 38	---
> 39	
> 40	## Output File Map
> 41	
> 42	```
> 43	docs/bok/<project-slug>/
> 44	├── 00-index.md              Phase 0  — Project manifest + file registry
> 45	├── 01-mrd.md                Phase 1  — Market Requirements Document (BABOK)
> 46	├── 02-brd.md                Phase 1  — Business Requirements Document (BABOK)
> 47	├── 03-prd.md                Phase 2  — Product Requirements Document (ProdBOK + CXBOK)
> 48	├── 04-frd.md                Phase 3  — Functional Requirements Document (SWEBOK)
> 49	├── 05-sdd.md                Phase 3  — System Design Document (SWEBOK + CISSP CBK)
> 50	├── 06-data-model.md         Phase 4  — Data Models (DMBOK + Supabase schema)
> 51	├── 07-process-flow.md       Phase 4  — Process Flows (BPM CBOK + n8n)
> 52	└── 08-quality-metrics.md    Phase 5  — Self-Optimization & Self-Healing (CMQ/OE BOK)
> 53	```
> 54	
> 55	---
> 56	
> 57	## Workflow Engine
> 58	
> 59	### Phase 0 — Project Bootstrap
> 60	
> 61	**BoK lens:** None (structural setup)  
> 62	**Template:** `templates/00-index.md`  
> 63	**Actions:**
> 64	1. Derive `projectSlug` from business idea (lowercase, hyphens, max 32 chars).
> 65	2. Create directory `docs/bok/<project-slug>/`.
> 66	3. Render `00-index.md` with all input metadata, today's date, version `v0.1`.
> 67	4. Record all planned output files with status `[ ] pending`.
> 68	
> 69	**Guardrails:**
> 70	- If directory already exists → check `00-index.md`; ask Sovereign before overwriting.
> 71	- Slug must match `^[a-z0-9-]{3,32}$`.
> 72	
> 73	---
> 74	
> 75	### Phase 1 — Market & Business Intelligence (BABOK v3)
> 76	
> 77	**BoK lens:** BABOK v3 — Business Analysis Body of Knowledge  
> 78	**BABOK knowledge areas applied:**
> 79	- *Business Analysis Planning & Monitoring* → defines stakeholders and elicitation plan
> 80	- *Elicitation & Collaboration* → extracts needs from raw idea
> 81	- *Requirements Life Cycle Mgmt* → traces market needs → business objectives
> 82	- *Strategy Analysis* → current state, desired state, gap analysis
> 83	- *Requirements Analysis & Design Definition* → MRD + BRD sections
> 84	
> 85	**Output A — `01-mrd.md` (Market Requirements Document):**
> 86	```
> 87	Sections to generate:
> 88	  1. Executive Summary
> 89	  2. Market Problem Statement (current state)
> 90	  3. Target Market Segments + TAM/SAM/SOM (estimated)
> 91	  4. Competitive Landscape (min 3 alternatives)
> 92	  5. Market Opportunity & Timing
> 93	  6. Key Market Requirements (MR-001..MR-NNN, priority: Critical/High/Medium/Low)
> 94	  7. Success Metrics (market-level KPIs)
> 95	  8. Regulatory & Compliance Context
> 96	  9. Traceability Matrix stub (MR → BR link)
> 97	```
> 98	
> 99	**Output B — `02-brd.md` (Business Requirements Document):**
> 100	```
> 101	Sections to generate:
> 102	  1. Executive Summary
> 103	  2. Business Objectives (SMART format, min 3)
> 104	  3. Stakeholder Register (Role, Interest, Influence, Communication)
> 105	  4. Business Requirements (BR-001..BR-NNN traced to MR-NNN)
> 106	  5. ROI Model (costs, revenue streams, payback period estimate)
> 107	  6. mcoCoins Economics (coin cost per operation, plan tier mapping)
> 108	  7. Constraints & Assumptions
> 109	  8. Business Risks (Risk ID, Description, Probability, Impact, Mitigation)
> 110	  9. Acceptance Criteria (business-level)
> 111	  10. Traceability Matrix (MR → BR → PR link stubs)
> 112	```
> 113	
> 114	**Transition check before Phase 2:**
> 115	- Every BR must trace to at least one MR.
> 116	- mcoCoins cost must be defined if feature uses AI generation.
> 117	
> 118	---
> 119	
> 120	### Phase 2 — Product Definition (ProdBOK + CXBOK)
> 121	
> 122	**BoK lens:** ProdBOK (Product Management Body of Knowledge) + CXBOK (Customer Experience)  
> 123	**ProdBOK areas applied:**
> 124	- *Product Vision & Strategy* → product goal and positioning
> 125	- *Roadmap Planning* → release phasing (MVP → v1 → v2)
> 126	- *Feature Definition & Prioritization* → MoSCoW method
> 127	- *Metrics & Analytics* → product KPIs
> 128	
> 129	**CXBOK areas applied:**
> 130	- *Customer Understanding* → persona construction
> 131	- *Experience Design* → journey mapping, touchpoint inventory
> 132	- *Luxury UX Standards* → MCORCH aesthetic rules (dark mesh, neon accents, micro-animations)
> 133	
> 134	**Output — `03-prd.md` (Product Requirements Document):**
> 135	```
> 136	Sections to generate:
> 137	  1. Product Vision Statement (one sentence)
> 138	  2. User Personas (min 2: primary + secondary)
> 139	     - Name, Role, Goals, Frustrations, Tech-savviness, MCORCH usage pattern
> 140	  3. User Journey Maps (per persona, happy path + 2 edge cases)
> 141	  4. Feature Inventory (MoSCoW: Must / Should / Could / Won't)
> 142	     - Feature ID: PR-001..PR-NNN
> 143	     - Description, Persona served, BR traced, Effort (S/M/L/XL), mcoCoins cost
> 144	  5. Release Phasing
> 145	     - MVP scope (Must-haves only)
> 146	     - v1.0 scope (Must + prioritized Shoulds)
> 147	     - Future scope (Coulds)
> 148	  6. Luxury UX Specifications
> 149	     - Color palette constraints (dark mesh: #0A0A0F, neon violet: #7C3AED)
> 150	     - Animation guidelines (Framer Motion tokens)
> 151	     - Interaction patterns (glass morphism cards, particle effects)
> 152	     - Accessibility requirements (WCAG 2.1 AA minimum)
> 153	  7. Acceptance Criteria (product-level, Gherkin format: Given/When/Then)
> 154	  8. Traceability Matrix (MR → BR → PR link)
> 155	```
> 156	
> 157	**Transition check before Phase 3:**
> 158	- Every PR must trace to at least one BR.
> 159	- MVP scope must be achievable without new Edge Functions (or explicitly note which new ones are needed).
> 160	
> 161	---
> 162	
> 163	### Phase 3 — Technical Specification (SWEBOK v4 + CISSP CBK 2024)
> 164	
> 165	**BoK lens A — SWEBOK v4:**
> 166	- *Software Requirements* → formal FR elicitation from PRD
> 167	- *Software Design* → architectural decisions, component decomposition
> 168	- *Software Construction* → Harness Engineering constraints
> 169	- *Software Testing* → test strategy per requirement
> 170	
> 171	**BoK lens B — CISSP CBK 2024:**
> 172	- *Security & Risk Management* → threat model (STRIDE)
> 173	- *Identity & Access Management* → RLS policies, JWT validation
> 174	- *Software Development Security* → secure coding constraints
> 175	- *Cryptography* → data-at-rest and in-transit requirements
> 176	
> 177	**Output A — `04-frd.md` (Functional Requirements Document):**
> 178	```
> 179	Sections to generate:
> 180	  1. Scope Statement
> 181	  2. Functional Requirements (FR-001..FR-NNN)
> 182	     - ID, Title, Description, Priority, PR traced, Acceptance Test ID
> 183	     - Category: UI / Hook / Edge Function / DB / Cron
> 184	  3. Non-Functional Requirements (NFR-001..NFR-NNN)
> 185	     - Performance, Scalability, Availability, Maintainability
> 186	  4. Interface Requirements
> 187	     - UI contracts (component → hook → Edge Function)
> 188	     - External API contracts (input/output shape, error codes)
> 189	  5. Data Requirements (input validation rules, data types)
> 190	  6. Test Strategy matrix (Unit / Integration / E2E per FR)
> 191	  7. Traceability Matrix (PR → FR link)
> 192	```
> 193	
> 194	**Output B — `05-sdd.md` (System Design Document):**
> 195	```
> 196	Sections to generate:
> 197	  1. Architecture Overview (text diagram, Harness Engineering layer map)
> 198	  2. Component Catalog
> 199	     - New hooks (src/hooks/)
> 200	     - New components (display-only, src/components/)
> 201	     - New Edge Functions (supabase/functions/)
> 202	     - New Zustand store slices (if needed)
> 203	     - New DB tables / columns (migration stubs)
> 204	  3. Data Flow Diagrams (per major use case)
> 205	  4. API Contract Definitions (Edge Function signatures)
> 206	     - Method, Path, Auth, Request body, Response body, Error codes
> 207	     - mcoCoins deduction point (RPC call location)
> 208	  5. Security Design
> 209	     - Threat model (STRIDE per component)
> 210	     - RLS policy definitions
> 211	     - JWT validation points
> 212	     - Secrets inventory (which vault keys are needed)
> 213	  6. Infrastructure Touchpoints
> 214	     - Docker Sovereign Mesh dependencies
> 215	     - ChromaDB usage (if vector search needed)
> 216	     - Watchdog telemetry events (new infra_health_logs event types)
> 217	  7. Migration Stubs (table name, columns, RLS template, HNSW index if embeddings)
> 218	  8. Open Technical Decisions (OTD-001..OTD-NNN, each with options + recommendation)
> 219	```
> 220	
> 221	**Security guardrails enforced automatically:**
> 222	- Every Edge Function must have JWT validation stub.
> 223	- Every new table must have `RLS enabled; default deny` noted in migration stub.
> 224	- `mcoCoins` deduction MUST route through `deduct_mco_coins` RPC — never client-side.
> 225	- No secret key referenced in FRD/SDD may appear in `src/` paths.
> 226	
> 227	**Transition check before Phase 4:**
> 228	- Every FR must trace to at least one PR.
> 229	- Every Edge Function in SDD must list its secret dependencies.
> 230	- Threat model must have at least one mitigation per identified threat.
> 231	
> 232	---
> 233	
> 234	### Phase 4 — Data & Process Engineering (DMBOK v2 + BPM CBOK v4)
> 235	
> 236	**BoK lens A — DMBOK v2:**
> 237	- *Data Modeling & Design* → conceptual → logical → physical schema
> 238	- *Data Quality* → validation rules, nullability constraints
> 239	- *Reference & Master Data* → system nodes in mcorch_nodes
> 240	- *Data Warehousing & BI* → analytics views if applicable
> 241	
> 242	**BoK lens B — BPM CBOK v4:**
> 243	- *Process Modeling* → BPMN-lite notation in markdown
> 244	- *Process Analysis* → bottlenecks, automation opportunities
> 245	- *Process Design* → n8n workflow blueprint
> 246	- *Process Performance Mgmt* → SLA per process step
> 247	
> 248	**Output A — `06-data-model.md` (Data & Knowledge Model):**
> 249	```
> 250	Sections to generate:
> 251	  1. Conceptual Data Model (entity list + relationships, text ERD)
> 252	  2. Logical Data Model (per table: columns, types, constraints, FK references)
> 253	  3. Supabase Physical Schema Stubs
> 254	     - CREATE TABLE skeleton (copy into migration file)
> 255	     - RLS policy shells (default deny + per-role)
> 256	     - Index definitions (HNSW for embeddings, B-tree for FKs)
> 257	  4. GraphRAG Knowledge Nodes
> 258	     - Node types this feature introduces into mcorch_nodes
> 259	     - Edge types this feature introduces into mcorch_edges
> 260	     - Embedding fields (which text columns feed embed-mcorch-node)
> 261	     - stability_score initial value + FSRS-6 decay parameters
> 262	  5. Tenant Isolation Map (user_id + project_id scope per table)
> 263	  6. Data Quality Rules (per column: allowed values, validation regex, null policy)
> 264	  7. Retention & Archival Policy
> 265	```
> 266	
> 267	**Output B — `07-process-flow.md` (Process & Automation Blueprint):**
> 268	```
> 269	Sections to generate:
> 270	  1. Process Inventory (list of all automated processes this feature introduces)
> 271	  2. BPMN-lite Process Maps (per major process)
> 272	     - Start event, Tasks (human/automated), Gateways, End events
> 273	     - Swimlanes: User | Frontend Hook | Edge Function | External API | DB
> 274	  3. n8n Workflow Blueprints (per automated process)
> 275	     - Trigger (webhook / cron / event), Node sequence, Error branches
> 276	     - Data mapping: input fields → output fields
> 277	  4. Orchestration Integration Points
> 278	     - Steps within orchestrate-content pipeline (if applicable)
> 279	     - New pipeline step ID and position
> 280	     - mcoCoins deduction trigger point
> 281	  5. Error Handling & Retry Strategy (per process step)
> 282	  6. SLA Definitions (expected duration per step, timeout thresholds)
> 283	  7. Cron Jobs (schedule, idempotency key, failure alerting)
> 284	```
> 285	
> 286	**Transition check before Phase 5:**
> 287	- Every table in data model must appear in at least one process flow.
> 288	- Every n8n workflow must define its error branch.
> 289	- GraphRAG node insertion must be present in at least one process.
> 290	
> 291	---
> 292	
> 293	### Phase 5 — Quality & Autonomic Engineering (CMQ/OE BOK)
> 294	
> 295	**BoK lens:** CMQ/OE BOK (Certified Manager of Quality / Organizational Excellence)  
> 296	**Areas applied:**
> 297	- *Process Management* → control charts, process capability (Cp/Cpk targets)
> 298	- *Quality Tools* → FMEA for critical paths
> 299	- *Customer-Focused Org* → NPS/CSAT hooks
> 300	- *Organizational Excellence* → self-optimization loops
> 301	- *Continuous Improvement* → PDCA cycles for autonomic self-healing
> 302	
> 303	**Output — `08-quality-metrics.md` (Self-Optimization & Self-Healing Specification):**
> 304	```
> 305	Sections to generate:
> 306	  1. Quality Objectives (aligned to business objectives in BRD)
> 307	  2. KPI Dashboard Definition
> 308	     - KPI ID, Name, Formula, Target, Threshold (warn/critical), Data source
> 309	     - Supabase table/view that stores the metric
> 310	  3. FMEA Table (per critical FR)
> 311	     - Function, Failure Mode, Effect, Severity (1-10), Occurrence (1-10),
> 312	       Detection (1-10), RPN = S×O×D, Recommended Action
> 313	  4. Self-Optimization Loops
> 314	     - Trigger condition (metric threshold crossed)
> 315	     - Autonomous response (what the system does without human intervention)
> 316	     - Escalation path (when human decision is required)
> 317	  5. Self-Healing Specifications
> 318	     - Watchdog telemetry event types (new rows for infra_health_logs)
> 319	     - Auto-recovery script stubs (bash / Edge Function)
> 320	     - mega-brain-daemon integration points
> 321	  6. SLA / SLO / SLI Definitions
> 322	     - Service, SLI metric, SLO target (e.g. 99.5% uptime/month), SLA consequence
> 323	  7. PDCA Improvement Cadence
> 324	     - Review frequency, metrics owner, improvement backlog location
> 325	  8. Observability Checklist
> 326	     - Logging events (what, where, level)
> 327	     - Alerting rules (condition → channel → escalation)
> 328	     - Distributed tracing touchpoints
> 329	```
> 330	
> 331	---
> 332	
> 333	### Phase 6 — Cross-Document Traceability Validation
> 334	
> 335	**Actions (automated consistency check before writing `00-index.md` final status):**
> 336	
> 337	```
> 338	1. Build traceability chain:
> 339	   MR-NNN → BR-NNN → PR-NNN → FR-NNN → (DB table | Edge Function | Process)
> 340	
> 341	2. Assert:
> 342	   - No orphaned requirements (every ID appears in at least one downstream doc).
> 343	   - No undocumented Edge Functions (every function in SDD has JWT + secret listed).
> 344	   - No tables without RLS (every CREATE TABLE stub has RLS block).
> 345	   - mcoCoins cost defined for every AI-powered FR.
> 346	   - Every FMEA item with RPN > 100 has a recommended action.
> 347	
> 348	3. If any assertion fails:
> 349	   - List all failures with their document + section reference.
> 350	   - Ask Sovereign to resolve before proceeding to Phase 7.
> 351	   - Do NOT proceed to Phase 7 with unresolved critical failures.
> 352	```
> 353	
> 354	---
> 355	
> 356	### Phase 7 — Knowledge Mesh Injection
> 357	
> 358	> **Canonical pattern (sealed 2026-05-26, Sovereign directive):** every BoK seal MUST persist
> 359	> the documentation_suite node via a dedicated Bun-native seed script following the precedent
> 360	> `scripts/seed-openclaw-bok-seal.ts` (and its sibling `seed-gamificacao-nodes-bok-seal.ts`).
> 361	> Inline REST `curl` or one-off dashboard inserts are NOT allowed — the script form preserves
> 362	> reproducibility, version control, and material proof of the operation.
> 363	
> 364	**Required actions:**
> 365	
> 366	1. **Construct the payload** as a fully-typed object — placeholder example:
> 367	
> 368	```json
> 369	{
> 370	  "node_type": "documentation_suite",
> 371	  "name": "bok-scribe-seal-<projectSlug>-v1",
> 372	  "title": "<projectSlug> BoK Documentation Suite v1",
> 373	  "content": "<one-paragraph synthesis: idea, market, architecture, ID space summary, motivating context>",
> 374	  "tags": ["bok-scribe", "<projectSlug>", "<marketSegment>", ...domain-specific],
> 375	  "stability_score": 0.85,
> 376	  "revenue_impact": <estimated from BRD ROI section — 0 for internal enablers; non-zero only when direct revenue is documented>,
> 377	  "metadata": {
> 378	    "bok_version": "1.0.0",
> 379	    "documents": ["00-index","01-mrd","02-brd","03-prd","04-frd","05-sdd","06-data-model","07-process-flow","08-quality-metrics"],
> 380	    "document_lines": { ... per-file LOC + total },
> 381	    "phase_completed": "Phase 7",
> 382	    "traceability_validated": true,
> 383	    "traceability_orphans": 0,
> 384	    "id_space": { "MR": "MR-XX-001..NNN", "BR": "...", ... },
> 385	    "fmea_high_rpn_count": <int>,
> 386	    "fmea_high_rpn_items": ["FMEA-XX-NNN (RPN <value>)", ...],
> 387	    "new_migrations": <int>,
> 388	    "new_edge_functions": <int>,
> 389	    "integration_surface": "<standalone|extends-mcorch>",
> 390	    "regulatory_profile": "<LGPD|GDPR|financial|healthcare|none>",
> 391	    "monetization": "<direct|indirect|internal-enabler-zero-coin>",
> 392	    "derives_from_seal": "bok-scribe-seal-<parent-slug>-v1",
> 393	    "depends_on_sop": "<path to operational SOP if applicable>",
> 394	    "motivating_incident": "<incident reference if BoK was triggered by an incident>"
> 395	  }
> 396	}
> 397	```
> 398	
> 399	2. **Author a dedicated seed script** at `scripts/seed-<projectSlug>-bok-seal.ts` mirroring
> 400	   `scripts/seed-openclaw-bok-seal.ts` 1:1 in structure. The script MUST:
> 401	   - Use `@supabase/supabase-js` with `SUPABASE_SERVICE_ROLE_KEY` from `.env` (never hardcode).
> 402	   - INSERT the payload into `mcorch_nodes` using `.select('id, name').single()` for material proof.
> 403	   - INSERT a `DERIVES_FROM` edge in `mcorch_edges` pointing to the most semantically-related
> 404	     parent seal (typically the previous BoK seal in the topic family — discover via
> 405	     `SELECT id FROM mcorch_nodes WHERE name = 'bok-scribe-seal-<parent-slug>-v1'`).
> 406	   - Print the returned UUIDs to stdout for the agent to cite as material proof.
> 407	   - Be idempotent: if the seal already exists (UNIQUE name violation), log and exit 0 cleanly.
> 408	
> 409	3. **Execute the script** under the project venv:
> 410	   ```bash
> 411	   bun run scripts/seed-<projectSlug>-bok-seal.ts
> 412	   ```
> 413	   Capture the returned UUID + edge UUID. Confirm via REST:
> 414	   ```bash
> 415	   curl -s "$SUPABASE_URL/rest/v1/mcorch_nodes?id=eq.<uuid>&select=embedding" \
> 416	     -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
> 417	     -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY"
> 418	   # Expected: embedding NOT NULL (auto-fired via trg_mcorch_embed_on_insert pg_net)
> 419	   ```
> 420	
> 421	4. **Cite the material proof** in the `/handoff` seal:
> 422	   - Documentation suite UUID
> 423	   - DERIVES_FROM edge UUID
> 424	   - Embedding confirmation timestamp
> 425	
> 426	**Note:** The BoK Scribe Agent itself does NOT directly invoke Supabase via in-conversation
> 427	REST calls — it produces the seed script + payload, and the Sovereign (or agent executing on
> 428	behalf of the Sovereign with explicit approval) runs the script. The script form preserves
> 429	the audit trail of "what was inserted, when, by which version of which code."
> 430	
> 431	**Precedent inventory (mirror sources, in order of recency):**
> 432	- `scripts/seed-e2e-user-zero-bok-seal.ts` (this BoK — 2026-05-26)
> 433	- `scripts/seed-openclaw-bok-seal.ts` (openclaw — 2026-05-19)
> 434	- `scripts/seed-gamificacao-nodes-bok-seal.ts` (gamificacao-nodes — 2026-05-18)
> 435	- (older seals predate this script pattern and were inserted via inline REST — grandfathered)
> 436	
> 437	---
> 438	
> 439	## Harness Engineering Constraints (non-negotiable)
> 440	
> 441	These rules apply to every document the agent produces:
> 442	
> 443	| Constraint | Rule |
> 444	|------------|------|
> 445	| Code separation | FRD/SDD describe WHAT and WHY. HOW belongs in code, not in docs. |
> 446	| Hook-first | Every UI feature must describe its backing hook before its component. |
> 447	| No client secrets | SDD never lists secret values, only key names from the vault. |
> 448	| Atomic billing | mcoCoins deduction always routes through `deduct_mco_coins` RPC. |
> 449	| RLS by default | Every new table starts with `ALTER TABLE x ENABLE ROW LEVEL SECURITY`. |
> 450	| Embed on insert | Every new node-type table must have embed-mcorch-node trigger noted. |
> 451	| Tenant isolation | Every table must document its `user_id + project_id` scoping. |
> 452	
> 453	---
> 454	
> 455	## Error & Edge Case Handling
> 456	
> 457	| Situation | Agent Response |
> 458	|-----------|----------------|
> 459	| Business idea is too vague | Ask 3 clarifying questions before Phase 1. |
> 460	| Existing docs/bok/<slug>/ detected | Show index, ask: overwrite / extend / cancel. |
> 461	| Phase transition check fails | List failures, stop, ask Sovereign to resolve. |
> 462	| Conflicting BoK recommendations | Note the conflict in an `[OTD]` block; present both options. |
> 463	| Regulatory profile = financial/healthcare | Elevate all CISSP CBK sections; add dedicated compliance checklist. |
> 464	| Feature extends existing MCORCH feature | Cross-reference existing ADRs from `.claude/context/architecture-decisions.md`. |
> 465	
> 466	---
> 467	
> 468	## Document Style Guide
> 469	
> 470	- **Headings:** `#` for document title, `##` for major sections, `###` for subsections.
> 471	- **IDs:** Always prefix (MR-, BR-, PR-, FR-, NFR-, OTD-) and zero-pad to 3 digits.
> 472	- **Tables:** Use markdown tables with aligned columns; include a header row always.
> 473	- **Code blocks:** Use fenced blocks with language identifier (`sql`, `typescript`, `json`).
> 474	- **Status badges:** `[ ] pending` / `[x] complete` / `[!] blocked` in index file.
> 475	- **Cross-references:** Link within suite as `[BR-001](../02-brd.md#br-001)`.
> 476	- **Version:** Every file footer includes `_Generated by MCORCH BoK Scribe Agent v1.0.0_`.
> 477	
> ```

## 🤖 Claude *(20:55:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la /home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/ 2>/dev/null; echo \"---EXISTING SLUG CHECK---\"; ls -la /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/ 2>/dev/null || echo \"viral-autopilot/ does not exist yet\"",
  "description": "List BoK templates + check target dir"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 68
> drwxrwxr-x 2 ubuntu ubuntu 4096 May  6 13:37 .
> drwxrwxr-x 3 ubuntu ubuntu 4096 May  6 13:37 ..
> -rw-rw-r-- 1 ubuntu ubuntu 2286 May  6 13:37 00-index.md
> -rw-rw-r-- 1 ubuntu ubuntu 3163 May  6 13:37 01-mrd.md
> -rw-rw-r-- 1 ubuntu ubuntu 3715 May  6 13:37 02-brd.md
> -rw-rw-r-- 1 ubuntu ubuntu 5073 May  6 13:37 03-prd.md
> -rw-rw-r-- 1 ubuntu ubuntu 3632 May  6 13:37 04-frd.md
> -rw-rw-r-- 1 ubuntu ubuntu 8660 May  6 13:37 05-sdd.md
> -rw-rw-r-- 1 ubuntu ubuntu 5880 May  6 13:37 06-data-model.md
> -rw-rw-r-- 1 ubuntu ubuntu 5730 May  6 13:37 07-process-flow.md
> -rw-rw-r-- 1 ubuntu ubuntu 7550 May  6 13:37 08-quality-metrics.md
> ---EXISTING SLUG CHECK---
> viral-autopilot/ does not exist yet
> ```

## 🤖 Claude *(20:55:41)*


## 🤖 Claude *(20:55:44)*

Workflow e estrutura claros. `viral-autopilot/` ainda não existe. Vou ler os 9 templates para casar o formato exato antes de gerar.

## 🤖 Claude *(20:55:44)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/00-index.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# BoK Documentation Suite — {{PROJECT_SLUG}}
> 2	
> 3	**Generated:** {{DATE}}  
> 4	**Version:** v0.1  
> 5	**Agent:** MCORCH BoK Scribe Agent v1.0.0  
> 6	**Sovereign:** {{SOVEREIGN_ID}}
> 7	
> 8	---
> 9	
> 10	## Project Metadata
> 11	
> 12	| Field | Value |
> 13	|-------|-------|
> 14	| Business Idea | {{BUSINESS_IDEA}} |
> 15	| Market Segment | {{MARKET_SEGMENT}} |
> 16	| Monetization Model | {{MONETIZATION_MODEL}} |
> 17	| Regulatory Profile | {{REGULATORY_PROFILE}} |
> 18	| Integration Surface | {{INTEGRATION_SURFACE}} |
> 19	| Project Slug | `{{PROJECT_SLUG}}` |
> 20	
> 21	---
> 22	
> 23	## Document Registry
> 24	
> 25	| # | File | Document | BoK Applied | Status |
> 26	|---|------|----------|-------------|--------|
> 27	| 0 | `00-index.md` | Project Manifest | — | [x] complete |
> 28	| 1 | `01-mrd.md` | Market Requirements Document | BABOK v3 | [ ] pending |
> 29	| 2 | `02-brd.md` | Business Requirements Document | BABOK v3 | [ ] pending |
> 30	| 3 | `03-prd.md` | Product Requirements Document | ProdBOK + CXBOK | [ ] pending |
> 31	| 4 | `04-frd.md` | Functional Requirements Document | SWEBOK v4 | [ ] pending |
> 32	| 5 | `05-sdd.md` | System Design Document | SWEBOK v4 + CISSP CBK | [ ] pending |
> 33	| 6 | `06-data-model.md` | Data & Knowledge Model | DMBOK v2 | [ ] pending |
> 34	| 7 | `07-process-flow.md` | Process & Automation Blueprint | BPM CBOK v4 | [ ] pending |
> 35	| 8 | `08-quality-metrics.md` | Self-Optimization Specification | CMQ/OE BOK | [ ] pending |
> 36	
> 37	---
> 38	
> 39	## Traceability Chain (populated as documents are generated)
> 40	
> 41	```
> 42	MR-NNN
> 43	  └── BR-NNN
> 44	        └── PR-NNN
> 45	              └── FR-NNN
> 46	                    └── [DB table | Edge Function | n8n Process]
> 47	```
> 48	
> 49	---
> 50	
> 51	## Phase Completion Log
> 52	
> 53	| Phase | Name | Completed | Notes |
> 54	|-------|------|-----------|-------|
> 55	| 0 | Project Bootstrap | {{DATE}} | — |
> 56	| 1 | Market & Business Intelligence | [ ] | — |
> 57	| 2 | Product Definition | [ ] | — |
> 58	| 3 | Technical Specification | [ ] | — |
> 59	| 4 | Data & Process Engineering | [ ] | — |
> 60	| 5 | Quality & Autonomic Engineering | [ ] | — |
> 61	| 6 | Traceability Validation | [ ] | — |
> 62	| 7 | Knowledge Mesh Injection | [ ] | — |
> 63	
> 64	---
> 65	
> 66	## Open Technical Decisions
> 67	
> 68	| OTD ID | Description | Options | Recommendation | Status |
> 69	|--------|-------------|---------|----------------|--------|
> 70	| — | None yet | — | — | — |
> 71	
> 72	---
> 73	
> 74	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 75	
> ```

## 🤖 Claude *(20:55:44)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/01-mrd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# MRD — Market Requirements Document
> 2	
> 3	**Project:** {{PROJECT_SLUG}}  
> 4	**Version:** v0.1 | **Date:** {{DATE}}  
> 5	**BoK Applied:** BABOK v3 (Strategy Analysis + Elicitation & Collaboration)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Executive Summary
> 11	
> 12	> _One paragraph: what market problem exists, why now, and what this solution uniquely addresses._
> 13	
> 14	{{EXECUTIVE_SUMMARY}}
> 15	
> 16	---
> 17	
> 18	## 2. Market Problem Statement
> 19	
> 20	### 2.1 Current State
> 21	> _Describe the painful status quo for the target user._
> 22	
> 23	{{CURRENT_STATE}}
> 24	
> 25	### 2.2 Root Cause Analysis
> 26	> _Why does this problem persist? (technology gap, process gap, market gap)_
> 27	
> 28	{{ROOT_CAUSE}}
> 29	
> 30	### 2.3 Desired State
> 31	> _What does success look like from the market's perspective?_
> 32	
> 33	{{DESIRED_STATE}}
> 34	
> 35	---
> 36	
> 37	## 3. Target Market Segments
> 38	
> 39	| Segment | Description | Size Estimate | Urgency | Accessibility |
> 40	|---------|-------------|---------------|---------|---------------|
> 41	| Primary | {{PRIMARY_SEGMENT}} | {{TAM_PRIMARY}} | High | {{ACCESS_PRIMARY}} |
> 42	| Secondary | {{SECONDARY_SEGMENT}} | {{TAM_SECONDARY}} | Medium | {{ACCESS_SECONDARY}} |
> 43	
> 44	### 3.1 TAM / SAM / SOM
> 45	
> 46	| Metric | Value | Basis |
> 47	|--------|-------|-------|
> 48	| TAM (Total Addressable Market) | {{TAM}} | {{TAM_BASIS}} |
> 49	| SAM (Serviceable Addressable Market) | {{SAM}} | {{SAM_BASIS}} |
> 50	| SOM (Serviceable Obtainable Market) | {{SOM}} | {{SOM_BASIS}} |
> 51	
> 52	---
> 53	
> 54	## 4. Competitive Landscape
> 55	
> 56	| Competitor | Positioning | Strengths | Weaknesses | Our Differentiation |
> 57	|------------|-------------|-----------|------------|---------------------|
> 58	| {{COMP_1}} | {{POS_1}} | {{STR_1}} | {{WEAK_1}} | {{DIFF_1}} |
> 59	| {{COMP_2}} | {{POS_2}} | {{STR_2}} | {{WEAK_2}} | {{DIFF_2}} |
> 60	| {{COMP_3}} | {{POS_3}} | {{STR_3}} | {{WEAK_3}} | {{DIFF_3}} |
> 61	
> 62	---
> 63	
> 64	## 5. Market Opportunity & Timing
> 65	
> 66	> _Why is this the right moment? (regulatory shifts, technology maturity, behavioral trends)_
> 67	
> 68	{{MARKET_TIMING}}
> 69	
> 70	---
> 71	
> 72	## 6. Market Requirements
> 73	
> 74	> Priority: **Critical** (must have at launch) | **High** | **Medium** | **Low**
> 75	
> 76	| ID | Market Requirement | Priority | Rationale | Source |
> 77	|----|-------------------|----------|-----------|--------|
> 78	| MR-001 | {{MR_001_DESC}} | Critical | {{MR_001_RATIONALE}} | {{MR_001_SOURCE}} |
> 79	| MR-002 | {{MR_002_DESC}} | High | {{MR_002_RATIONALE}} | {{MR_002_SOURCE}} |
> 80	
> 81	---
> 82	
> 83	## 7. Success Metrics (Market-Level KPIs)
> 84	
> 85	| KPI | Definition | Target (6-month) | Target (12-month) | Measurement |
> 86	|-----|-----------|------------------|-------------------|-------------|
> 87	| Market Penetration | % of SAM reached | {{KPI_1_6M}} | {{KPI_1_12M}} | {{KPI_1_MEAS}} |
> 88	| NPS | Net Promoter Score | {{KPI_2_6M}} | {{KPI_2_12M}} | {{KPI_2_MEAS}} |
> 89	
> 90	---
> 91	
> 92	## 8. Regulatory & Compliance Context
> 93	
> 94	| Regulation | Applicability | Key Constraint | Compliance Owner |
> 95	|------------|---------------|----------------|-----------------|
> 96	| LGPD | {{LGPD_APPLICABLE}} | {{LGPD_CONSTRAINT}} | Engineering |
> 97	| {{OTHER_REG}} | {{OTHER_APPLICABLE}} | {{OTHER_CONSTRAINT}} | {{OTHER_OWNER}} |
> 98	
> 99	---
> 100	
> 101	## 9. Traceability Matrix Stub
> 102	
> 103	| MR ID | → BR ID | Rationale |
> 104	|-------|---------|-----------|
> 105	| MR-001 | BR-??? | _to be linked in BRD_ |
> 106	
> 107	---
> 108	
> 109	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 110	
> ```

## 🤖 Claude *(20:55:45)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/02-brd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# BRD — Business Requirements Document
> 2	
> 3	**Project:** {{PROJECT_SLUG}}  
> 4	**Version:** v0.1 | **Date:** {{DATE}}  
> 5	**BoK Applied:** BABOK v3 (Requirements Analysis & Design Definition)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Executive Summary
> 11	
> 12	{{EXECUTIVE_SUMMARY}}
> 13	
> 14	---
> 15	
> 16	## 2. Business Objectives (SMART)
> 17	
> 18	| ID | Objective | Specific | Measurable | Achievable | Relevant | Time-bound |
> 19	|----|-----------|----------|------------|------------|----------|------------|
> 20	| BO-001 | {{BO_001}} | {{BO_001_S}} | {{BO_001_M}} | {{BO_001_A}} | {{BO_001_R}} | {{BO_001_T}} |
> 21	| BO-002 | {{BO_002}} | {{BO_002_S}} | {{BO_002_M}} | {{BO_002_A}} | {{BO_002_R}} | {{BO_002_T}} |
> 22	| BO-003 | {{BO_003}} | {{BO_003_S}} | {{BO_003_M}} | {{BO_003_A}} | {{BO_003_R}} | {{BO_003_T}} |
> 23	
> 24	---
> 25	
> 26	## 3. Stakeholder Register
> 27	
> 28	| ID | Role | Interest | Influence | Communication Cadence | Contact |
> 29	|----|------|----------|-----------|----------------------|---------|
> 30	| SH-001 | Sovereign / Maestro | High | High | Continuous | {{SOVEREIGN}} |
> 31	| SH-002 | End User (Primary) | High | Medium | Monthly NPS survey | {{USER_CONTACT}} |
> 32	| SH-003 | {{STAKEHOLDER_3}} | {{INTEREST_3}} | {{INFLUENCE_3}} | {{CADENCE_3}} | {{CONTACT_3}} |
> 33	
> 34	---
> 35	
> 36	## 4. Business Requirements
> 37	
> 38	> Each BR traces to at least one MR. mcoCoins cost defined if AI-powered.
> 39	
> 40	| ID | Requirement | MR Traced | Priority | mcoCoins Cost | Acceptance Criteria |
> 41	|----|-------------|-----------|----------|---------------|---------------------|
> 42	| BR-001 | {{BR_001_DESC}} | MR-001 | Critical | {{COINS_001}} | {{AC_001}} |
> 43	| BR-002 | {{BR_002_DESC}} | MR-001 | High | {{COINS_002}} | {{AC_002}} |
> 44	
> 45	---
> 46	
> 47	## 5. ROI Model
> 48	
> 49	### 5.1 Cost Estimates
> 50	
> 51	| Cost Item | Type | Monthly Estimate | Annual Estimate |
> 52	|-----------|------|-----------------|----------------|
> 53	| Infrastructure (Supabase, Docker) | OpEx | {{INFRA_MONTHLY}} | {{INFRA_ANNUAL}} |
> 54	| AI API calls (OpenRouter) | Variable | {{AI_MONTHLY}} | {{AI_ANNUAL}} |
> 55	| Development (initial) | CapEx | — | {{DEV_COST}} |
> 56	
> 57	### 5.2 Revenue Streams
> 58	
> 59	| Stream | Model | Monthly Potential | Notes |
> 60	|--------|-------|-----------------|-------|
> 61	| {{STREAM_1}} | {{MODEL_1}} | {{REV_1_MONTHLY}} | {{NOTES_1}} |
> 62	| {{STREAM_2}} | {{MODEL_2}} | {{REV_2_MONTHLY}} | {{NOTES_2}} |
> 63	
> 64	### 5.3 Payback Analysis
> 65	
> 66	| Metric | Value |
> 67	|--------|-------|
> 68	| Break-even (months) | {{BREAK_EVEN}} |
> 69	| 12-month ROI | {{ROI_12M}} |
> 70	| IRR (estimated) | {{IRR}} |
> 71	
> 72	---
> 73	
> 74	## 6. mcoCoins Economics
> 75	
> 76	| Operation | Coins/Run | Plan Tier Mapping | Monthly Volume (est.) | Monthly Revenue (est.) |
> 77	|-----------|-----------|-------------------|-----------------------|----------------------|
> 78	| {{OP_1}} | {{COINS_OP_1}} | Starter(500) / Pro(2000) / Ent(10k) | {{VOL_1}} | {{REV_MCO_1}} |
> 79	
> 80	---
> 81	
> 82	## 7. Constraints & Assumptions
> 83	
> 84	### Constraints
> 85	- {{CONSTRAINT_1}}
> 86	- {{CONSTRAINT_2}}
> 87	
> 88	### Assumptions
> 89	- {{ASSUMPTION_1}}
> 90	- {{ASSUMPTION_2}}
> 91	
> 92	---
> 93	
> 94	## 8. Business Risk Register
> 95	
> 96	| Risk ID | Description | Probability | Impact | RPN | Mitigation |
> 97	|---------|-------------|-------------|--------|-----|------------|
> 98	| BR-RISK-001 | {{RISK_001}} | {{PROB_001}} | {{IMPACT_001}} | {{RPN_001}} | {{MIT_001}} |
> 99	| BR-RISK-002 | {{RISK_002}} | {{PROB_002}} | {{IMPACT_002}} | {{RPN_002}} | {{MIT_002}} |
> 100	
> 101	> Probability & Impact: 1=Low, 5=High. RPN = Probability × Impact.
> 102	
> 103	---
> 104	
> 105	## 9. Business Acceptance Criteria
> 106	
> 107	| ID | Criterion | Verification Method |
> 108	|----|-----------|-------------------|
> 109	| BAC-001 | {{BAC_001}} | {{BAC_001_VERIFY}} |
> 110	| BAC-002 | {{BAC_002}} | {{BAC_002_VERIFY}} |
> 111	
> 112	---
> 113	
> 114	## 10. Traceability Matrix
> 115	
> 116	| MR ID | BR ID | PR ID (stub) |
> 117	|-------|-------|--------------|
> 118	| MR-001 | BR-001, BR-002 | _to be linked in PRD_ |
> 119	
> 120	---
> 121	
> 122	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 123	
> ```

## 🤖 Claude *(20:55:45)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/03-prd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# PRD — Product Requirements Document
> 2	
> 3	**Project:** {{PROJECT_SLUG}}  
> 4	**Version:** v0.1 | **Date:** {{DATE}}  
> 5	**BoK Applied:** ProdBOK + CXBOK  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Product Vision Statement
> 11	
> 12	> _One sentence. Format: "For [target user] who [need], [Product Name] is a [category] that [key benefit]. Unlike [alternative], our product [differentiator]."_
> 13	
> 14	{{PRODUCT_VISION}}
> 15	
> 16	---
> 17	
> 18	## 2. User Personas
> 19	
> 20	### Persona 1 — {{PERSONA_1_NAME}} (Primary)
> 21	
> 22	| Attribute | Detail |
> 23	|-----------|--------|
> 24	| Role | {{P1_ROLE}} |
> 25	| Goals | {{P1_GOALS}} |
> 26	| Frustrations | {{P1_FRUSTRATIONS}} |
> 27	| Tech-savviness | {{P1_TECH}} (1=novice, 5=expert) |
> 28	| MCORCH usage pattern | {{P1_MCORCH_PATTERN}} |
> 29	| Quote | _"{{P1_QUOTE}}"_ |
> 30	
> 31	### Persona 2 — {{PERSONA_2_NAME}} (Secondary)
> 32	
> 33	| Attribute | Detail |
> 34	|-----------|--------|
> 35	| Role | {{P2_ROLE}} |
> 36	| Goals | {{P2_GOALS}} |
> 37	| Frustrations | {{P2_FRUSTRATIONS}} |
> 38	| Tech-savviness | {{P2_TECH}} |
> 39	| MCORCH usage pattern | {{P2_MCORCH_PATTERN}} |
> 40	| Quote | _"{{P2_QUOTE}}"_ |
> 41	
> 42	---
> 43	
> 44	## 3. User Journey Maps
> 45	
> 46	### Journey: {{JOURNEY_1_NAME}} ({{PERSONA_1_NAME}}, Happy Path)
> 47	
> 48	| Stage | Action | Touchpoint | Emotion | Opportunity |
> 49	|-------|--------|-----------|---------|-------------|
> 50	| Awareness | {{STAGE_1_ACTION}} | {{STAGE_1_TOUCH}} | 😐 Neutral | {{STAGE_1_OPP}} |
> 51	| Consideration | {{STAGE_2_ACTION}} | {{STAGE_2_TOUCH}} | 🤔 Curious | {{STAGE_2_OPP}} |
> 52	| Activation | {{STAGE_3_ACTION}} | {{STAGE_3_TOUCH}} | 😊 Excited | {{STAGE_3_OPP}} |
> 53	| Value | {{STAGE_4_ACTION}} | {{STAGE_4_TOUCH}} | 🚀 Delighted | {{STAGE_4_OPP}} |
> 54	| Retention | {{STAGE_5_ACTION}} | {{STAGE_5_TOUCH}} | ❤️ Loyal | {{STAGE_5_OPP}} |
> 55	
> 56	#### Edge Case 1: {{EDGE_CASE_1_NAME}}
> 57	> {{EDGE_CASE_1_DESC}}
> 58	
> 59	#### Edge Case 2: {{EDGE_CASE_2_NAME}}
> 60	> {{EDGE_CASE_2_DESC}}
> 61	
> 62	---
> 63	
> 64	## 4. Feature Inventory (MoSCoW)
> 65	
> 66	> Effort: S=hours, M=days, L=week, XL=sprint
> 67	
> 68	### Must Have (MVP)
> 69	
> 70	| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |
> 71	|----|---------|---------|-----------|--------|-------------|-------|
> 72	| PR-001 | {{PR_001_NAME}} | P1 | BR-001 | {{PR_001_EFFORT}} | {{PR_001_COINS}} | {{PR_001_NOTES}} |
> 73	| PR-002 | {{PR_002_NAME}} | P1, P2 | BR-002 | {{PR_002_EFFORT}} | {{PR_002_COINS}} | {{PR_002_NOTES}} |
> 74	
> 75	### Should Have (v1.0)
> 76	
> 77	| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |
> 78	|----|---------|---------|-----------|--------|-------------|-------|
> 79	| PR-010 | {{PR_010_NAME}} | P2 | BR-003 | {{PR_010_EFFORT}} | {{PR_010_COINS}} | {{PR_010_NOTES}} |
> 80	
> 81	### Could Have (Future)
> 82	
> 83	| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |
> 84	|----|---------|---------|-----------|--------|-------------|-------|
> 85	| PR-020 | {{PR_020_NAME}} | P1 | BR-004 | {{PR_020_EFFORT}} | {{PR_020_COINS}} | {{PR_020_NOTES}} |
> 86	
> 87	### Won't Have (This Cycle)
> 88	
> 89	- {{WONT_HAVE_1}}
> 90	- {{WONT_HAVE_2}}
> 91	
> 92	---
> 93	
> 94	## 5. Release Phasing
> 95	
> 96	### MVP Scope
> 97	**Target date:** {{MVP_DATE}}  
> 98	**Included:** PR-001, PR-002  
> 99	**Success gate:** {{MVP_SUCCESS_GATE}}
> 100	
> 101	### v1.0 Scope
> 102	**Target date:** {{V1_DATE}}  
> 103	**Adds:** PR-010, PR-011  
> 104	**Success gate:** {{V1_SUCCESS_GATE}}
> 105	
> 106	### Future Scope
> 107	**Items:** PR-020+  
> 108	**Condition:** {{FUTURE_CONDITION}}
> 109	
> 110	---
> 111	
> 112	## 6. Luxury UX Specifications
> 113	
> 114	### 6.1 Color & Visual Identity
> 115	
> 116	| Token | Value | Usage |
> 117	|-------|-------|-------|
> 118	| `--bg-deep` | `#0A0A0F` | Canvas background |
> 119	| `--accent-violet` | `#7C3AED` | Primary CTA, active states |
> 120	| `--accent-cyan` | `#06B6D4` | Data highlights, graphs |
> 121	| `--glass-surface` | `rgba(255,255,255,0.04)` | Card backgrounds |
> 122	| `--border-subtle` | `rgba(255,255,255,0.08)` | Card borders |
> 123	
> 124	### 6.2 Animation Guidelines
> 125	
> 126	| Element | Library | Duration | Easing |
> 127	|---------|---------|----------|--------|
> 128	| Page transitions | Framer Motion | 300ms | `easeInOut` |
> 129	| Node entrance (3D) | R3F / drei | 500ms | `spring(stiffness:80)` |
> 130	| Status pulse | CSS keyframes | 2s | `ease-in-out infinite` |
> 131	| Micro-interactions | Framer Motion | 150ms | `easeOut` |
> 132	
> 133	### 6.3 Interaction Patterns
> 134	
> 135	- **Cards:** Glass morphism — `backdrop-blur-sm`, subtle border, shadow `0 4px 24px rgba(0,0,0,0.4)`.
> 136	- **Buttons:** Gradient border on hover; never flat fill for primary CTAs.
> 137	- **Loading states:** Skeleton shimmer (never spinners for content areas).
> 138	- **Toasts:** `sonner` library; success = violet, error = red, info = cyan.
> 139	
> 140	### 6.4 Accessibility (WCAG 2.1 AA)
> 141	
> 142	- Contrast ratio ≥ 4.5:1 for all text on glass surfaces.
> 143	- All interactive elements keyboard-navigable.
> 144	- ARIA labels on all icon-only buttons.
> 145	- Focus indicators visible at ≥ 2px.
> 146	
> 147	---
> 148	
> 149	## 7. Acceptance Criteria (Gherkin)
> 150	
> 151	```gherkin
> 152	Feature: {{FEATURE_NAME}}
> 153	
> 154	  Scenario: {{SCENARIO_1_TITLE}} (PR-001)
> 155	    Given {{GIVEN_1}}
> 156	    When {{WHEN_1}}
> 157	    Then {{THEN_1}}
> 158	    And {{AND_1}}
> 159	
> 160	  Scenario: {{SCENARIO_2_TITLE}} (PR-002)
> 161	    Given {{GIVEN_2}}
> 162	    When {{WHEN_2}}
> 163	    Then {{THEN_2}}
> 164	```
> 165	
> 166	---
> 167	
> 168	## 8. Traceability Matrix
> 169	
> 170	| MR ID | BR ID | PR ID |
> 171	|-------|-------|-------|
> 172	| MR-001 | BR-001 | PR-001, PR-002 |
> 173	| MR-002 | BR-002 | PR-010 |
> 174	
> 175	---
> 176	
> 177	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 178	
> ```

## 🤖 Claude *(20:55:48)*


## 🤖 Claude *(20:55:48)*

Agora os 4 templates restantes (FRD, SDD, data-model, process-flow, quality-metrics):

## 🤖 Claude *(20:55:50)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/04-frd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# FRD — Functional Requirements Document
> 2	
> 3	**Project:** {{PROJECT_SLUG}}  
> 4	**Version:** v0.1 | **Date:** {{DATE}}  
> 5	**BoK Applied:** SWEBOK v4 (Software Requirements)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Scope Statement
> 11	
> 12	This document specifies the functional and non-functional requirements for `{{PROJECT_SLUG}}`.
> 13	It is derived from PRD `03-prd.md` and feeds directly into SDD `05-sdd.md`.
> 14	
> 15	**In scope:** {{SCOPE_IN}}  
> 16	**Out of scope:** {{SCOPE_OUT}}
> 17	
> 18	---
> 19	
> 20	## 2. Functional Requirements
> 21	
> 22	> Category: `UI` | `Hook` | `EdgeFunction` | `DB` | `Cron`
> 23	
> 24	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 25	|----|-------|-------------|----------|-----------|----------|---------|
> 26	| FR-001 | {{FR_001_TITLE}} | {{FR_001_DESC}} | Critical | PR-001 | {{FR_001_CAT}} | AT-001 |
> 27	| FR-002 | {{FR_002_TITLE}} | {{FR_002_DESC}} | High | PR-001 | {{FR_002_CAT}} | AT-002 |
> 28	| FR-003 | {{FR_003_TITLE}} | {{FR_003_DESC}} | High | PR-002 | {{FR_003_CAT}} | AT-003 |
> 29	
> 30	---
> 31	
> 32	## 3. Non-Functional Requirements
> 33	
> 34	| ID | Category | Requirement | Target | Measurement |
> 35	|----|----------|-------------|--------|-------------|
> 36	| NFR-001 | Performance | Page load (LCP) | < 2.5s | Lighthouse CI |
> 37	| NFR-002 | Performance | Edge Function p95 latency | < 800ms | Supabase logs |
> 38	| NFR-003 | Scalability | Concurrent users without degradation | {{SCALE_TARGET}} | Load test |
> 39	| NFR-004 | Availability | Uptime SLO | 99.5%/month | Watchdog telemetry |
> 40	| NFR-005 | Maintainability | Cyclomatic complexity per hook | ≤ 10 | ESLint |
> 41	| NFR-006 | Security | All endpoints require valid JWT | 100% | Security review |
> 42	
> 43	---
> 44	
> 45	## 4. Interface Requirements
> 46	
> 47	### 4.1 UI → Hook → Edge Function Contract
> 48	
> 49	```
> 50	[Component: {{COMPONENT_NAME}}]
> 51	  ↓ calls
> 52	[Hook: use{{HOOK_NAME}}]
> 53	  ↓ calls (for sensitive ops)
> 54	[Edge Function: {{EDGE_FUNCTION_NAME}}]
> 55	  ↓ reads/writes
> 56	[Supabase Table: {{TABLE_NAME}}]
> 57	```
> 58	
> 59	### 4.2 External API Contracts
> 60	
> 61	#### `POST /functions/v1/{{EDGE_FUNCTION_NAME}}`
> 62	
> 63	**Auth:** Bearer JWT (user scope)  
> 64	**Request:**
> 65	```typescript
> 66	{
> 67	  {{REQUEST_FIELD_1}}: {{REQUEST_TYPE_1}},  // {{REQUEST_DESC_1}}
> 68	  {{REQUEST_FIELD_2}}: {{REQUEST_TYPE_2}},  // {{REQUEST_DESC_2}}
> 69	}
> 70	```
> 71	**Response (200):**
> 72	```typescript
> 73	{
> 74	  {{RESPONSE_FIELD_1}}: {{RESPONSE_TYPE_1}},
> 75	  {{RESPONSE_FIELD_2}}: {{RESPONSE_TYPE_2}},
> 76	}
> 77	```
> 78	**Error codes:**
> 79	| Code | Condition |
> 80	|------|-----------|
> 81	| 401 | Missing or invalid JWT |
> 82	| 402 | Insufficient mcoCoins balance |
> 83	| 422 | Validation failure (field + message in body) |
> 84	| 500 | Internal error (logged to infra_health_logs) |
> 85	
> 86	---
> 87	
> 88	## 5. Data Requirements
> 89	
> 90	| Field | Type | Nullable | Validation Rule | Error Message (PT-BR) |
> 91	|-------|------|----------|-----------------|----------------------|
> 92	| {{FIELD_1}} | {{TYPE_1}} | {{NULL_1}} | {{VALIDATION_1}} | {{ERROR_PT_1}} |
> 93	| {{FIELD_2}} | {{TYPE_2}} | {{NULL_2}} | {{VALIDATION_2}} | {{ERROR_PT_2}} |
> 94	
> 95	---
> 96	
> 97	## 6. Test Strategy Matrix
> 98	
> 99	| FR ID | Unit Test | Integration Test | E2E Test | Notes |
> 100	|-------|-----------|-----------------|----------|-------|
> 101	| FR-001 | ✅ Required | ✅ Required | ✅ Required | {{TEST_NOTES_001}} |
> 102	| FR-002 | ✅ Required | ✅ Required | — | {{TEST_NOTES_002}} |
> 103	| FR-003 | ✅ Required | — | — | {{TEST_NOTES_003}} |
> 104	
> 105	**Test files location:**
> 106	- Unit: `src/hooks/__tests__/use{{HOOK_NAME}}.test.ts`
> 107	- Integration: `src/__tests__/integration/{{FEATURE_NAME}}.test.ts`
> 108	- E2E: `e2e/{{FEATURE_NAME}}.spec.ts`
> 109	
> 110	---
> 111	
> 112	## 7. Traceability Matrix
> 113	
> 114	| PR ID | FR ID | NFR ID |
> 115	|-------|-------|--------|
> 116	| PR-001 | FR-001, FR-002 | NFR-001, NFR-006 |
> 117	| PR-002 | FR-003 | NFR-002 |
> 118	
> 119	---
> 120	
> 121	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 122	
> ```

## 🤖 Claude *(20:55:50)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/05-sdd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# SDD — System Design Document
> 2	
> 3	**Project:** {{PROJECT_SLUG}}  
> 4	**Version:** v0.1 | **Date:** {{DATE}}  
> 5	**BoK Applied:** SWEBOK v4 (Software Design) + CISSP CBK 2024 (Software Development Security)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Architecture Overview
> 11	
> 12	```
> 13	┌─────────────────────────────────────────────────────────┐
> 14	│  PRESENTATION LAYER (display-only)                       │
> 15	│  src/components/{{FEATURE_AREA}}/{{COMPONENT_NAME}}.tsx  │
> 16	└──────────────────────┬──────────────────────────────────┘
> 17	                       │ calls
> 18	┌──────────────────────▼──────────────────────────────────┐
> 19	│  LOGIC LAYER (Harness Engineering)                       │
> 20	│  src/hooks/use{{HOOK_NAME}}.ts                           │
> 21	│  src/store/{{STORE_SLICE}}.ts (Zustand, if needed)       │
> 22	└──────────────────────┬──────────────────────────────────┘
> 23	                       │ HTTP + JWT
> 24	┌──────────────────────▼──────────────────────────────────┐
> 25	│  EDGE LAYER (Deno / Supabase Functions)                  │
> 26	│  supabase/functions/{{EDGE_FUNCTION_NAME}}/index.ts      │
> 27	└──────────┬───────────────────────────┬──────────────────┘
> 28	           │ Supabase RLS              │ External APIs
> 29	┌──────────▼──────────┐  ┌────────────▼──────────────────┐
> 30	│  DB LAYER           │  │  EXTERNAL SERVICES             │
> 31	│  {{TABLE_1}}        │  │  OpenRouter (embeddings)        │
> 32	│  {{TABLE_2}}        │  │  {{EXTERNAL_API_1}}            │
> 33	│  mcorch_nodes       │  │  {{EXTERNAL_API_2}}            │
> 34	└─────────────────────┘  └────────────────────────────────┘
> 35	```
> 36	
> 37	---
> 38	
> 39	## 2. Component Catalog
> 40	
> 41	### 2.1 New Custom Hooks (`src/hooks/`)
> 42	
> 43	| Hook | File | Responsibility | TanStack Query keys |
> 44	|------|------|---------------|---------------------|
> 45	| `use{{Hook1}}` | `use{{Hook1}}.ts` | {{HOOK1_RESP}} | `['{{KEY_1}}']` |
> 46	| `use{{Hook2}}` | `use{{Hook2}}.ts` | {{HOOK2_RESP}} | `['{{KEY_2}}']` |
> 47	
> 48	### 2.2 New Display Components (`src/components/`)
> 49	
> 50	| Component | File | Props | Hook consumed |
> 51	|-----------|------|-------|--------------|
> 52	| `{{Component1}}` | `{{PATH_1}}` | `{{PROPS_1}}` | `use{{Hook1}}` |
> 53	| `{{Component2}}` | `{{PATH_2}}` | `{{PROPS_2}}` | `use{{Hook2}}` |
> 54	
> 55	### 2.3 New Edge Functions (`supabase/functions/`)
> 56	
> 57	| Function | Path | Auth | mcoCoins | Secrets needed |
> 58	|----------|------|------|----------|----------------|
> 59	| `{{EdgeFn1}}` | `supabase/functions/{{EdgeFn1}}/index.ts` | JWT (user) | {{COINS_1}} | `{{SECRETS_1}}` |
> 60	
> 61	### 2.4 Zustand Store Slices (if applicable)
> 62	
> 63	| Slice | Store file | State shape | Actions |
> 64	|-------|------------|-------------|---------|
> 65	| `{{SLICE_1}}` | `src/store/use{{StoreName}}.ts` | `{{STATE_1}}` | `{{ACTIONS_1}}` |
> 66	
> 67	### 2.5 New DB Objects
> 68	
> 69	| Object | Type | Purpose | Migration file |
> 70	|--------|------|---------|---------------|
> 71	| `{{TABLE_1}}` | Table | {{TABLE_1_PURPOSE}} | `{{MIGRATION_1}}` |
> 72	| `{{VIEW_1}}` | View | {{VIEW_1_PURPOSE}} | `{{MIGRATION_2}}` |
> 73	
> 74	---
> 75	
> 76	## 3. Data Flow Diagrams
> 77	
> 78	### Use Case: {{USE_CASE_1}}
> 79	
> 80	```
> 81	User                Hook              Edge Fn            DB
> 82	 │                   │                   │                │
> 83	 │──[action]────────▶│                   │                │
> 84	 │                   │──[POST JWT]───────▶│                │
> 85	 │                   │                   │──[check mco]──▶│ deduct_mco_coins RPC
> 86	 │                   │                   │◀──[ok]─────────│
> 87	 │                   │                   │──[AI call]──▶  │ (OpenRouter/external)
> 88	 │                   │                   │◀──[result]──   │
> 89	 │                   │                   │──[insert]─────▶│ {{TABLE_1}}
> 90	 │                   │                   │──[embed node]──▶│ mcorch_nodes
> 91	 │                   │◀──[200 response]──│                │
> 92	 │◀──[UI update]─────│                   │                │
> 93	```
> 94	
> 95	---
> 96	
> 97	## 4. API Contract Definitions
> 98	
> 99	> All Edge Functions must validate JWT before any business logic.
> 100	
> 101	### `POST /functions/v1/{{EdgeFn1}}`
> 102	
> 103	```typescript
> 104	// Request
> 105	interface {{EdgeFn1}}Request {
> 106	  {{REQ_FIELD_1}}: {{REQ_TYPE_1}}
> 107	  {{REQ_FIELD_2}}: {{REQ_TYPE_2}}
> 108	}
> 109	
> 110	// Response (HTTP 200)
> 111	interface {{EdgeFn1}}Response {
> 112	  status: 'ok'
> 113	  {{RESP_FIELD_1}}: {{RESP_TYPE_1}}
> 114	}
> 115	
> 116	// mcoCoins deduction point:
> 117	// → Line ~40: await supabase.rpc('deduct_mco_coins', { p_user_id, p_amount: {{COIN_AMOUNT}} })
> 118	// → HTTP 402 if insufficient balance
> 119	```
> 120	
> 121	---
> 122	
> 123	## 5. Security Design
> 124	
> 125	### 5.1 Threat Model (STRIDE)
> 126	
> 127	| Component | Threat | Type | Severity | Mitigation |
> 128	|-----------|--------|------|----------|------------|
> 129	| `{{EdgeFn1}}` | Unauthenticated access | Spoofing | High | JWT validation at entry point |
> 130	| `{{TABLE_1}}` | Cross-tenant data read | Information Disclosure | Critical | RLS `user_id = auth.uid()` |
> 131	| mcoCoins deduction | Client-side bypass | Tampering | Critical | Server-side RPC only |
> 132	| {{THREAT_4}} | {{THREAT_4_DESC}} | {{THREAT_4_TYPE}} | {{THREAT_4_SEV}} | {{THREAT_4_MIT}} |
> 133	
> 134	### 5.2 RLS Policy Definitions
> 135	
> 136	```sql
> 137	-- {{TABLE_1}} RLS
> 138	ALTER TABLE {{TABLE_1}} ENABLE ROW LEVEL SECURITY;
> 139	
> 140	CREATE POLICY "{{TABLE_1}}_select_own"
> 141	  ON {{TABLE_1}} FOR SELECT
> 142	  USING (user_id = auth.uid());
> 143	
> 144	CREATE POLICY "{{TABLE_1}}_insert_own"
> 145	  ON {{TABLE_1}} FOR INSERT
> 146	  WITH CHECK (user_id = auth.uid());
> 147	```
> 148	
> 149	### 5.3 JWT Validation Points
> 150	
> 151	All Edge Functions follow this pattern:
> 152	```typescript
> 153	const authHeader = req.headers.get('Authorization')
> 154	if (!authHeader) return new Response('Unauthorized', { status: 401 })
> 155	const { data: { user }, error } = await supabase.auth.getUser(
> 156	  authHeader.replace('Bearer ', '')
> 157	)
> 158	if (error || !user) return new Response('Unauthorized', { status: 401 })
> 159	```
> 160	
> 161	### 5.4 Secrets Inventory
> 162	
> 163	| Secret Name | Used In | Vault Location | Rotation Policy |
> 164	|-------------|---------|----------------|----------------|
> 165	| `{{SECRET_1}}` | `{{EdgeFn1}}` | Supabase Vault | {{ROTATION_1}} |
> 166	
> 167	> ⚠️ NEVER commit secret values. Only key names appear in documentation.
> 168	
> 169	---
> 170	
> 171	## 6. Infrastructure Touchpoints
> 172	
> 173	| Infrastructure | Usage | Impact |
> 174	|----------------|-------|--------|
> 175	| `mcorch_chroma` (ChromaDB port 8001) | {{CHROMA_USAGE}} | {{CHROMA_IMPACT}} |
> 176	| `mega-brain-daemon` | {{DAEMON_USAGE}} | {{DAEMON_IMPACT}} |
> 177	| `infra_health_logs` | New event type: `{{NEW_EVENT_TYPE}}` | Watchdog telemetry |
> 178	
> 179	---
> 180	
> 181	## 7. Migration Stubs
> 182	
> 183	```sql
> 184	-- Migration: {{MIGRATION_TIMESTAMP}}_{{PROJECT_SLUG}}_initial.sql
> 185	
> 186	CREATE TABLE {{TABLE_1}} (
> 187	  id          uuid DEFAULT gen_random_uuid() PRIMARY KEY,
> 188	  user_id     uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
> 189	  project_id  uuid REFERENCES projects(id) ON DELETE CASCADE,
> 190	  -- feature-specific columns:
> 191	  {{COLUMN_1}} {{COL_TYPE_1}} {{COL_CONSTRAINTS_1}},
> 192	  {{COLUMN_2}} {{COL_TYPE_2}} {{COL_CONSTRAINTS_2}},
> 193	  -- embeddings (if applicable):
> 194	  embedding   vector(768),
> 195	  -- audit:
> 196	  created_at  timestamptz DEFAULT now() NOT NULL,
> 197	  updated_at  timestamptz DEFAULT now() NOT NULL
> 198	);
> 199	
> 200	ALTER TABLE {{TABLE_1}} ENABLE ROW LEVEL SECURITY;
> 201	-- (paste RLS policies from §5.2)
> 202	
> 203	-- HNSW index (only if embedding column present):
> 204	CREATE INDEX {{TABLE_1}}_embedding_idx
> 205	  ON {{TABLE_1}} USING hnsw (embedding vector_cosine_ops)
> 206	  WITH (m = 16, ef_construction = 64);
> 207	```
> 208	
> 209	---
> 210	
> 211	## 8. Open Technical Decisions
> 212	
> 213	| ID | Description | Option A | Option B | Recommendation | Owner |
> 214	|----|-------------|----------|----------|----------------|-------|
> 215	| OTD-001 | {{OTD_001_DESC}} | {{OTD_001_A}} | {{OTD_001_B}} | {{OTD_001_REC}} | Sovereign |
> 216	
> 217	---
> 218	
> 219	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 220	
> ```

## 🤖 Claude *(20:55:53)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/06-data-model.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Data & Knowledge Model
> 2	
> 3	**Project:** {{PROJECT_SLUG}}  
> 4	**Version:** v0.1 | **Date:** {{DATE}}  
> 5	**BoK Applied:** DMBOK v2 (Data Modeling & Design + Data Quality)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Conceptual Data Model
> 11	
> 12	```
> 13	[{{ENTITY_1}}] ──(1:N)──▶ [{{ENTITY_2}}]
> 14	      │
> 15	      └──(N:M)──▶ [{{ENTITY_3}}]
> 16	                         │
> 17	                         └──(1:1)──▶ [mcorch_nodes]
> 18	```
> 19	
> 20	**Entities:**
> 21	- **{{ENTITY_1}}:** {{ENTITY_1_DESC}}
> 22	- **{{ENTITY_2}}:** {{ENTITY_2_DESC}}
> 23	- **{{ENTITY_3}}:** {{ENTITY_3_DESC}}
> 24	
> 25	---
> 26	
> 27	## 2. Logical Data Model
> 28	
> 29	### Table: `{{TABLE_1}}`
> 30	
> 31	| Column | Type | Nullable | Default | FK | Description |
> 32	|--------|------|----------|---------|-----|------------|
> 33	| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | — | Primary key |
> 34	| `user_id` | `uuid` | NOT NULL | — | `auth.users.id` | Tenant isolation |
> 35	| `project_id` | `uuid` | NULL | — | `projects.id` | Project scope |
> 36	| `{{COL_1}}` | `{{TYPE_1}}` | {{NULL_1}} | {{DEFAULT_1}} | {{FK_1}} | {{DESC_1}} |
> 37	| `{{COL_2}}` | `{{TYPE_2}}` | {{NULL_2}} | {{DEFAULT_2}} | {{FK_2}} | {{DESC_2}} |
> 38	| `embedding` | `vector(768)` | NULL | — | — | Neural embedding (OpenRouter text-embedding-3-small) |
> 39	| `stability_score` | `float4` | NOT NULL | `0.5` | — | FSRS-6 memory stability |
> 40	| `created_at` | `timestamptz` | NOT NULL | `now()` | — | Audit |
> 41	| `updated_at` | `timestamptz` | NOT NULL | `now()` | — | Audit |
> 42	
> 43	### Table: `{{TABLE_2}}`
> 44	
> 45	| Column | Type | Nullable | Default | FK | Description |
> 46	|--------|------|----------|---------|-----|------------|
> 47	| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | — | Primary key |
> 48	| `{{TABLE_1}}_id` | `uuid` | NOT NULL | — | `{{TABLE_1}}.id` | Parent reference |
> 49	| `{{COL_3}}` | `{{TYPE_3}}` | {{NULL_3}} | {{DEFAULT_3}} | {{FK_3}} | {{DESC_3}} |
> 50	
> 51	---
> 52	
> 53	## 3. Supabase Physical Schema Stubs
> 54	
> 55	```sql
> 56	-- ============================================================
> 57	-- MIGRATION: {{MIGRATION_TIMESTAMP}}_{{PROJECT_SLUG}}_schema.sql
> 58	-- ============================================================
> 59	
> 60	-- {{TABLE_1}}
> 61	CREATE TABLE public.{{TABLE_1}} (
> 62	  id             uuid DEFAULT gen_random_uuid() PRIMARY KEY,
> 63	  user_id        uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
> 64	  project_id     uuid REFERENCES public.projects(id) ON DELETE CASCADE,
> 65	  {{COL_1}}      {{TYPE_1}} {{CONSTRAINTS_1}},
> 66	  {{COL_2}}      {{TYPE_2}} {{CONSTRAINTS_2}},
> 67	  embedding      vector(768),
> 68	  stability_score float4 NOT NULL DEFAULT 0.5,
> 69	  created_at     timestamptz NOT NULL DEFAULT now(),
> 70	  updated_at     timestamptz NOT NULL DEFAULT now()
> 71	);
> 72	
> 73	ALTER TABLE public.{{TABLE_1}} ENABLE ROW LEVEL SECURITY;
> 74	
> 75	-- RLS Policies
> 76	CREATE POLICY "{{TABLE_1}}: users read own rows"
> 77	  ON public.{{TABLE_1}} FOR SELECT
> 78	  USING (user_id = auth.uid());
> 79	
> 80	CREATE POLICY "{{TABLE_1}}: users insert own rows"
> 81	  ON public.{{TABLE_1}} FOR INSERT
> 82	  WITH CHECK (user_id = auth.uid());
> 83	
> 84	CREATE POLICY "{{TABLE_1}}: users update own rows"
> 85	  ON public.{{TABLE_1}} FOR UPDATE
> 86	  USING (user_id = auth.uid())
> 87	  WITH CHECK (user_id = auth.uid());
> 88	
> 89	-- Indexes
> 90	CREATE INDEX {{TABLE_1}}_user_idx ON public.{{TABLE_1}} (user_id);
> 91	CREATE INDEX {{TABLE_1}}_project_idx ON public.{{TABLE_1}} (project_id);
> 92	
> 93	-- HNSW (embeddings)
> 94	CREATE INDEX {{TABLE_1}}_embedding_hnsw
> 95	  ON public.{{TABLE_1}} USING hnsw (embedding vector_cosine_ops)
> 96	  WITH (m = 16, ef_construction = 64);
> 97	
> 98	-- Updated-at trigger
> 99	CREATE TRIGGER set_{{TABLE_1}}_updated_at
> 100	  BEFORE UPDATE ON public.{{TABLE_1}}
> 101	  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
> 102	```
> 103	
> 104	---
> 105	
> 106	## 4. GraphRAG Knowledge Nodes
> 107	
> 108	### Node Types Introduced
> 109	
> 110	| node_type | Title Pattern | Content Fields | Embedding Source |
> 111	|-----------|--------------|----------------|-----------------|
> 112	| `{{NODE_TYPE_1}}` | `{{TITLE_PATTERN_1}}` | `{{CONTENT_FIELDS_1}}` | `{{EMBED_SOURCE_1}}` |
> 113	| `{{NODE_TYPE_2}}` | `{{TITLE_PATTERN_2}}` | `{{CONTENT_FIELDS_2}}` | `{{EMBED_SOURCE_2}}` |
> 114	
> 115	### Edge Types Introduced
> 116	
> 117	| Edge relationship | Source node_type | Target node_type | Metadata |
> 118	|-------------------|-----------------|-----------------|----------|
> 119	| `{{EDGE_REL_1}}` | `{{EDGE_SRC_1}}` | `{{EDGE_TGT_1}}` | `{{EDGE_META_1}}` |
> 120	
> 121	### Embedding Trigger
> 122	
> 123	Every insert into `{{TABLE_1}}` must call `embed-mcorch-node`:
> 124	```typescript
> 125	// In the Edge Function, after successful insert:
> 126	await supabase.functions.invoke('embed-mcorch-node', {
> 127	  body: { node_id: insertedNode.id, content: `${title} ${content}` }
> 128	})
> 129	```
> 130	
> 131	### FSRS-6 Parameters
> 132	
> 133	| Field | Initial Value | Decay Rule |
> 134	|-------|--------------|------------|
> 135	| `stability_score` | `0.5` | Decays per migration `20260425190000` formula |
> 136	| `revenue_impact` | {{REVENUE_IMPACT_CALC}} | Updated on each successful orchestration run |
> 137	
> 138	---
> 139	
> 140	## 5. Tenant Isolation Map
> 141	
> 142	| Table | `user_id` scope | `project_id` scope | System rows (user_id IS NULL) |
> 143	|-------|----------------|-------------------|-------------------------------|
> 144	| `{{TABLE_1}}` | ✅ Required | Optional | No |
> 145	| `{{TABLE_2}}` | ✅ Required | ✅ Required | No |
> 146	| `mcorch_nodes` | Optional | Optional | Yes (system nodes) |
> 147	
> 148	---
> 149	
> 150	## 6. Data Quality Rules
> 151	
> 152	| Table | Column | Rule | Violation Message (PT-BR) |
> 153	|-------|--------|------|--------------------------|
> 154	| `{{TABLE_1}}` | `{{COL_1}}` | {{QUALITY_RULE_1}} | {{QUALITY_MSG_1}} |
> 155	| `{{TABLE_1}}` | `{{COL_2}}` | {{QUALITY_RULE_2}} | {{QUALITY_MSG_2}} |
> 156	
> 157	---
> 158	
> 159	## 7. Retention & Archival Policy
> 160	
> 161	| Data | Retention Period | Archival Strategy | Deletion Trigger |
> 162	|------|-----------------|-------------------|-----------------|
> 163	| `{{TABLE_1}}` rows | {{RETENTION_1}} | {{ARCHIVAL_1}} | {{DELETE_TRIGGER_1}} |
> 164	| Embeddings (`vector` column) | Indefinite | Backfill via `scripts/backfill-embeddings.ts` | With parent row |
> 165	| `infra_health_logs` entries | 90 days | No archival | Cron purge |
> 166	
> 167	---
> 168	
> 169	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 170	
> ```

## 🤖 Claude *(20:55:54)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/07-process-flow.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Process & Automation Blueprint
> 2	
> 3	**Project:** {{PROJECT_SLUG}}  
> 4	**Version:** v0.1 | **Date:** {{DATE}}  
> 5	**BoK Applied:** BPM CBOK v4 (Process Modeling + Process Design)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Process Inventory
> 11	
> 12	| Process ID | Name | Type | Trigger | Owner | SLA |
> 13	|------------|------|------|---------|-------|-----|
> 14	| PROC-001 | {{PROC_001_NAME}} | {{PROC_001_TYPE}} | {{PROC_001_TRIGGER}} | System | {{PROC_001_SLA}} |
> 15	| PROC-002 | {{PROC_002_NAME}} | {{PROC_002_TYPE}} | {{PROC_002_TRIGGER}} | User | {{PROC_002_SLA}} |
> 16	
> 17	> Types: `automated` | `human-in-loop` | `cron` | `event-driven`
> 18	
> 19	---
> 20	
> 21	## 2. BPMN-lite Process Maps
> 22	
> 23	### PROC-001: {{PROC_001_NAME}}
> 24	
> 25	```
> 26	START ──▶ [{{TASK_1}}] ──▶ <Gateway: {{GATEWAY_1_NAME}}>
> 27	                                  │ YES                    │ NO
> 28	                            [{{TASK_2}}]              [{{ERROR_PATH_1}}]
> 29	                                  │                         │
> 30	                            [{{TASK_3}}]              [Notify: {{ERROR_NOTIF}}]
> 31	                                  │                         │
> 32	                               ◀──┴─────────────────────────┘
> 33	                                  │
> 34	                               [Insert mcorch_node]
> 35	                                  │
> 36	                                END
> 37	```
> 38	
> 39	**Swimlanes:**
> 40	
> 41	| Swimlane | Participant | Tasks |
> 42	|----------|-------------|-------|
> 43	| User | Browser / Frontend | {{USER_TASKS}} |
> 44	| Frontend Hook | `use{{HookName}}.ts` | {{HOOK_TASKS}} |
> 45	| Edge Function | `{{EdgeFunctionName}}` | {{EDGE_TASKS}} |
> 46	| External API | `{{ExternalAPI}}` | {{EXT_TASKS}} |
> 47	| DB | Supabase / PostgreSQL | {{DB_TASKS}} |
> 48	
> 49	---
> 50	
> 51	### PROC-002: {{PROC_002_NAME}}
> 52	
> 53	```
> 54	[User Action: {{USER_ACTION}}]
> 55	  │
> 56	  ▼
> 57	[Hook: use{{HookName}} → mutation trigger]
> 58	  │
> 59	  ▼
> 60	[Edge Fn: {{EdgeFunctionName}}]
> 61	  ├── Validate JWT ──(fail)──▶ HTTP 401
> 62	  ├── Check mcoCoins ──(low)──▶ HTTP 402 → Toast: "Saldo insuficiente"
> 63	  ├── {{BUSINESS_LOGIC_STEP}}
> 64	  ├── Persist to {{TABLE_1}}
> 65	  ├── Embed node via embed-mcorch-node
> 66	  └── HTTP 200 → React Query invalidation → UI refresh
> 67	```
> 68	
> 69	---
> 70	
> 71	## 3. n8n Workflow Blueprints
> 72	
> 73	### Workflow: {{N8N_WORKFLOW_1_NAME}}
> 74	
> 75	**Trigger:** {{N8N_TRIGGER_1}}  
> 76	**Idempotency key:** `{{N8N_IDEMPOTENCY_KEY}}`
> 77	
> 78	```
> 79	[Trigger: {{N8N_TRIGGER_1}}]
> 80	  │
> 81	  ▼
> 82	[Node: HTTP Request → /functions/v1/{{EdgeFunctionName}}]
> 83	  ├── Headers: Authorization: Bearer {{SERVICE_ROLE_OR_USER_JWT}}
> 84	  ├── Body: { {{N8N_REQUEST_BODY}} }
> 85	  │
> 86	  ├── (success) ──▶ [Node: Update Supabase row status = 'complete']
> 87	  │                         │
> 88	  │                         ▼
> 89	  │                [Node: Send notification (optional)]
> 90	  │
> 91	  └── (error) ──▶ [Node: Set retry count + 1]
> 92	                         │
> 93	                   (count ≤ 3) ──▶ [Wait: exponential backoff]──▶ retry
> 94	                         │
> 95	                   (count > 3) ──▶ [Node: Insert infra_health_logs {event: 'n8n_failure'}]
> 96	                                         │
> 97	                                   [Node: Alert Sovereign]
> 98	```
> 99	
> 100	**Data Mapping:**
> 101	
> 102	| Input Field | Source | → | Output Field | Destination |
> 103	|-------------|--------|---|--------------|-------------|
> 104	| `{{IN_FIELD_1}}` | Trigger body | → | `{{OUT_FIELD_1}}` | Edge Function body |
> 105	| `{{IN_FIELD_2}}` | Env var | → | `Authorization` | Header |
> 106	
> 107	---
> 108	
> 109	## 4. Orchestration Integration Points
> 110	
> 111	> Applies only if this feature integrates with `orchestrate-content` pipeline.
> 112	
> 113	| Pipeline Step | Step ID | Position | Description | mcoCoins Trigger |
> 114	|---------------|---------|----------|-------------|-----------------|
> 115	| {{PIPELINE_STEP_1}} | step_{{STEP_ID_1}} | After step {{PREV_STEP}} | {{STEP_DESC_1}} | {{STEP_COINS_1}} coins at entry |
> 116	
> 117	**Integration code stub (inside `orchestrate-content/index.ts`):**
> 118	```typescript
> 119	// Step {{STEP_ID_1}}: {{PIPELINE_STEP_1}}
> 120	await updateNodeStatus(nodes, '{{STEP_ID_1}}', 'running')
> 121	const {{STEP_RESULT}} = await {{STEP_ACTION}}(payload)
> 122	if (!{{STEP_RESULT}}.ok) {
> 123	  await updateNodeStatus(nodes, '{{STEP_ID_1}}', 'error')
> 124	  throw new Error('{{PIPELINE_STEP_1}} failed')
> 125	}
> 126	await updateNodeStatus(nodes, '{{STEP_ID_1}}', 'complete')
> 127	```
> 128	
> 129	---
> 130	
> 131	## 5. Error Handling & Retry Strategy
> 132	
> 133	| Process | Step | Error Type | Max Retries | Backoff | Failure Action |
> 134	|---------|------|-----------|-------------|---------|----------------|
> 135	| PROC-001 | {{TASK_1}} | Network timeout | 3 | Exponential (2s, 4s, 8s) | Insert `infra_health_logs` |
> 136	| PROC-001 | {{TASK_2}} | External API 5xx | 2 | Fixed 5s | Alert + mark failed |
> 137	| PROC-002 | mcoCoins check | Insufficient balance | 0 | — | HTTP 402 to user |
> 138	| Any | JWT validation | Invalid token | 0 | — | HTTP 401 immediately |
> 139	
> 140	---
> 141	
> 142	## 6. SLA Definitions
> 143	
> 144	| Process | Step | Expected Duration | Timeout Threshold | Alert if exceeded |
> 145	|---------|------|------------------|-------------------|-------------------|
> 146	| PROC-001 | End-to-end | {{E2E_DURATION}} | {{E2E_TIMEOUT}} | Yes → infra_health_logs |
> 147	| PROC-001 | {{TASK_1}} alone | {{TASK_1_DURATION}} | {{TASK_1_TIMEOUT}} | No |
> 148	| PROC-002 | Edge Fn response | < 800ms p95 | 5s | Yes |
> 149	
> 150	---
> 151	
> 152	## 7. Cron Jobs
> 153	
> 154	| Job Name | Schedule (cron) | Function | Idempotency | Failure Alerting |
> 155	|----------|----------------|----------|-------------|-----------------|
> 156	| `{{CRON_1_NAME}}` | `{{CRON_1_SCHEDULE}}` | `{{CRON_1_FN}}` | `{{CRON_1_KEY}}` | `infra_health_logs` |
> 157	
> 158	> All cron jobs must be idempotent — re-running on the same data must produce the same result.
> 159	
> 160	---
> 161	
> 162	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 163	
> ```

## 🤖 Claude *(20:55:55)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/08-quality-metrics.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Quality & Self-Optimization Specification
> 2	
> 3	**Project:** {{PROJECT_SLUG}}  
> 4	**Version:** v0.1 | **Date:** {{DATE}}  
> 5	**BoK Applied:** CMQ/OE BOK (Process Management + Organizational Excellence)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Quality Objectives
> 11	
> 12	| QO ID | Objective | Linked Business Objective | Target | Review Cadence |
> 13	|-------|-----------|--------------------------|--------|---------------|
> 14	| QO-001 | {{QO_001}} | BO-001 | {{QO_001_TARGET}} | Weekly |
> 15	| QO-002 | {{QO_002}} | BO-002 | {{QO_002_TARGET}} | Monthly |
> 16	| QO-003 | {{QO_003}} | BO-003 | {{QO_003_TARGET}} | Quarterly |
> 17	
> 18	---
> 19	
> 20	## 2. KPI Dashboard Definition
> 21	
> 22	> Data source: Supabase tables/views listed per KPI.
> 23	
> 24	| KPI ID | Name | Formula | Target | Warn Threshold | Critical Threshold | Data Source |
> 25	|--------|------|---------|--------|---------------|-------------------|-------------|
> 26	| KPI-001 | {{KPI_001_NAME}} | {{KPI_001_FORMULA}} | {{KPI_001_TARGET}} | {{KPI_001_WARN}} | {{KPI_001_CRIT}} | `{{KPI_001_TABLE}}` |
> 27	| KPI-002 | {{KPI_002_NAME}} | {{KPI_002_FORMULA}} | {{KPI_002_TARGET}} | {{KPI_002_WARN}} | {{KPI_002_CRIT}} | `{{KPI_002_TABLE}}` |
> 28	| KPI-003 | mcoCoins Burn Rate | `SUM(deductions) / active_users` | < {{BURN_TARGET}}/user | {{BURN_WARN}} | {{BURN_CRIT}} | `profiles` + `mco_transactions` |
> 29	| KPI-004 | Edge Fn p95 Latency | `PERCENTILE_CONT(0.95) OVER latency` | < 800ms | 1000ms | 2000ms | Supabase logs |
> 30	| KPI-005 | Knowledge Mesh Growth | `COUNT(mcorch_nodes) per week` | > {{MESH_GROWTH_TARGET}} | < {{MESH_GROWTH_WARN}} | 0 | `mcorch_nodes` |
> 31	
> 32	---
> 33	
> 34	## 3. FMEA Table
> 35	
> 36	> Severity, Occurrence, Detection: 1 (best) → 10 (worst). RPN = S × O × D. RPN > 100 requires action.
> 37	
> 38	| ID | Function | Failure Mode | Effect | S | O | D | RPN | Recommended Action |
> 39	|----|---------|--------------|--------|---|---|---|-----|--------------------|
> 40	| FMEA-001 | {{FR_001_TITLE}} | {{FAILURE_001}} | {{EFFECT_001}} | {{S_001}} | {{O_001}} | {{D_001}} | {{RPN_001}} | {{ACTION_001}} |
> 41	| FMEA-002 | mcoCoins deduction | RPC timeout → double charge | User overcharged | 9 | 2 | 3 | 54 | Idempotency key on every RPC call |
> 42	| FMEA-003 | JWT validation | Missing header | Unauthenticated access | 10 | 2 | 1 | 20 | Hard fail at entry; logged to infra_health_logs |
> 43	| FMEA-004 | embed-mcorch-node | Embedding API timeout | Node stored without vector | 6 | 3 | 4 | 72 | Async retry queue; backfill via `scripts/backfill-embeddings.ts` |
> 44	| FMEA-005 | {{CRITICAL_FR}} | {{FAILURE_005}} | {{EFFECT_005}} | {{S_005}} | {{O_005}} | {{D_005}} | {{RPN_005}} | {{ACTION_005}} |
> 45	
> 46	---
> 47	
> 48	## 4. Self-Optimization Loops
> 49	
> 50	| Loop ID | Trigger Condition | KPI Source | Autonomous Response | Escalation (human) |
> 51	|---------|------------------|------------|--------------------|--------------------|
> 52	| SOL-001 | KPI-004 latency > 1000ms for 5 consecutive calls | infra_health_logs | `mega-brain-daemon`: restart Edge Fn container | Alert Sovereign if > 2s |
> 53	| SOL-002 | KPI-005 mesh growth = 0 for 7 days | mcorch_nodes | Trigger backfill job via cron | Alert if backfill fails |
> 54	| SOL-003 | {{TRIGGER_003}} | {{KPI_SOURCE_003}} | {{RESPONSE_003}} | {{ESCALATION_003}} |
> 55	| SOL-004 | mcoCoins balance < 10% of plan quota | profiles | Send in-app notification (PT-BR) | — (no auto-action) |
> 56	
> 57	---
> 58	
> 59	## 5. Self-Healing Specifications
> 60	
> 61	### 5.1 Watchdog Telemetry Events
> 62	
> 63	New event types to be written to `infra_health_logs` by this feature:
> 64	
> 65	| Event Type | Trigger | Severity | Payload |
> 66	|------------|---------|----------|---------|
> 67	| `{{PROJECT_SLUG}}_fn_failure` | Edge Fn 5xx after retry exhaustion | error | `{fn_name, error_message, user_id}` |
> 68	| `{{PROJECT_SLUG}}_embed_failure` | embed-mcorch-node timeout | warn | `{node_id, retry_count}` |
> 69	| `{{PROJECT_SLUG}}_sla_breach` | Process SLA exceeded | warn | `{process_id, elapsed_ms, threshold_ms}` |
> 70	
> 71	### 5.2 Auto-Recovery Script Stubs
> 72	
> 73	```bash
> 74	#!/bin/bash
> 75	# scripts/self-heal-{{PROJECT_SLUG}}.sh
> 76	# Triggered by mega-brain-daemon when {{PROJECT_SLUG}}_fn_failure detected
> 77	
> 78	FUNCTION_NAME="{{EDGE_FUNCTION_NAME}}"
> 79	LOG_TABLE="infra_health_logs"
> 80	
> 81	echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Self-heal triggered for $FUNCTION_NAME"
> 82	
> 83	# Step 1: Check function status
> 84	STATUS=$(curl -s -o /dev/null -w "%{http_code}" \
> 85	  "$SUPABASE_URL/functions/v1/$FUNCTION_NAME/health" \
> 86	  -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY")
> 87	
> 88	if [ "$STATUS" != "200" ]; then
> 89	  echo "[WARN] Function unhealthy (status: $STATUS). Re-deploying..."
> 90	  npx supabase functions deploy "$FUNCTION_NAME"
> 91	fi
> 92	
> 93	# Step 2: Log recovery attempt
> 94	# (insert into infra_health_logs via Supabase REST API)
> 95	echo "[OK] Self-heal complete for $FUNCTION_NAME"
> 96	```
> 97	
> 98	### 5.3 mega-brain-daemon Integration Points
> 99	
> 100	| Daemon Event | Condition | Action |
> 101	|-------------|-----------|--------|
> 102	| `health_check` | Every 5 min (watchdog cron) | Check `{{TABLE_1}}` row count vs. expected baseline |
> 103	| `anomaly_detected` | `infra_health_logs` error rate > 5/hour | Execute `self-heal-{{PROJECT_SLUG}}.sh` |
> 104	| `recovery_confirmed` | Health check passes after self-heal | Insert `recovery_ok` event to `infra_health_logs` |
> 105	
> 106	---
> 107	
> 108	## 6. SLA / SLO / SLI Definitions
> 109	
> 110	| Service | SLI (what we measure) | SLO (our target) | SLA (contractual consequence) |
> 111	|---------|----------------------|------------------|-------------------------------|
> 112	| `{{EdgeFunctionName}}` API | p95 response latency | ≤ 800ms | Credits issued if > 2s for > 1% of calls in a month |
> 113	| Data ingestion pipeline | % records processed within SLA | ≥ 99% | Incident report required |
> 114	| Knowledge Mesh embedding | % nodes with embedding within 5m of insert | ≥ 95% | Auto-backfill triggered |
> 115	| Platform uptime | % minutes available per month | ≥ 99.5% | Per enterprise contract |
> 116	
> 117	---
> 118	
> 119	## 7. PDCA Improvement Cadence
> 120	
> 121	| Cycle | Phase | Activity | Owner | Frequency |
> 122	|-------|-------|----------|-------|-----------|
> 123	| {{PROJECT_SLUG}} Quality | Plan | Review FMEA + KPI targets | Sovereign | Quarterly |
> 124	| {{PROJECT_SLUG}} Quality | Do | Implement top improvement action | Engineering | Per sprint |
> 125	| {{PROJECT_SLUG}} Quality | Check | Compare KPIs vs. targets; update FMEA RPNs | AIOS | Monthly |
> 126	| {{PROJECT_SLUG}} Quality | Act | Close loop; update this document | Sovereign | Monthly |
> 127	
> 128	**Improvement backlog location:** `.claude/context/sprint-priorities.md`
> 129	
> 130	---
> 131	
> 132	## 8. Observability Checklist
> 133	
> 134	### 8.1 Logging Events
> 135	
> 136	| Event | Location | Level | Fields logged |
> 137	|-------|----------|-------|--------------|
> 138	| Function entry | `{{EdgeFunctionName}}/index.ts` line ~10 | INFO | `{user_id, timestamp, request_id}` |
> 139	| mcoCoins deduction | After RPC call | INFO | `{user_id, amount, new_balance}` |
> 140	| Business logic error | Catch block | ERROR | `{user_id, error_message, stack}` |
> 141	| SLA breach | Timeout guard | WARN | `{process_id, elapsed_ms}` |
> 142	
> 143	### 8.2 Alerting Rules
> 144	
> 145	| Condition | Channel | Escalation |
> 146	|-----------|---------|------------|
> 147	| Error rate > 1% in 5 min | `infra_health_logs` insert | mega-brain-daemon auto-heal |
> 148	| p95 latency > 2s | `infra_health_logs` insert | Sovereign notification |
> 149	| Zero KPI-005 growth > 7 days | Scheduled check | AIOS agent alert |
> 150	
> 151	### 8.3 Distributed Tracing Touchpoints
> 152	
> 153	| Span | Start | End | Tags |
> 154	|------|-------|-----|------|
> 155	| `{{EdgeFunctionName}}.total` | Request received | Response sent | `user_id`, `status_code` |
> 156	| `{{EdgeFunctionName}}.mco_check` | Before RPC | After RPC | `amount`, `balance_after` |
> 157	| `{{EdgeFunctionName}}.embed` | Before embed-mcorch-node call | After call | `node_id`, `success` |
> 158	
> 159	---
> 160	
> 161	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 162	
> ```

## 🤖 Claude *(20:57:21)*


## 🤖 Claude *(20:57:23)*

Tenho todos os templates, o workflow das 7 fases, os achados materiais da auditoria e as 4 decisões. Vou autorar a suíte completa em sequência (MR→BR→PR→FR→SDD→data→process→quality), preservando a cadeia de rastreabilidade — autoria de suíte BoK acoplada é tarefa de autor único coerente; depois rodo um workflow de **verificação adversarial** (Fase 6) antes de selar.

Começando: diretório + manifesto + MRD.

## 🤖 Claude *(20:57:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "mkdir -p /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot && echo \"dir ready\" && ls -d /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot",
  "description": "Create viral-autopilot BoK directory"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> dir ready
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot
> ```

## 🤖 Claude *(20:57:28)*


## 🤖 Claude *(20:58:07)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/00-index.md",
  "content": "# BoK Documentation Suite \u2014 viral-autopilot\n\n**Generated:** 2026-06-17  \n**Version:** v0.1  \n**Agent:** MCORCH BoK Scribe Agent v1.0.0  \n**Sovereign:** Gabriel Zarattini (gabrielcall@gmail.com)\n\n---\n\n## Project Metadata\n\n| Field | Value |\n|-------|-------|\n| Business Idea | Motor de conte\u00fado viral aut\u00f4nomo: alimentar contas de redes sociais com conte\u00fado gerado automaticamente, agendado (tudo de uma vez OU lote a cada N dias, default 3), que a cada ciclo analisa o desempenho anterior para melhorar os pr\u00f3ximos criativos \u2014 tudo monetizado com afiliado do Mercado Livre. |\n| Market Segment | B2B2C (plataforma SaaS multi-tenant para criadores/afiliados [B2B] cujo conte\u00fado viral atinge consumidores [B2C]) |\n| Monetization Model | hybrid (consumo de mcoCoins por ciclo/criativo + receita de comiss\u00e3o de afiliado ML compartilhada) |\n| Regulatory Profile | LGPD (publica\u00e7\u00e3o de conte\u00fado + PII residual de engajamento + ToS de redes sociais e do Mercado Livre) |\n| Integration Surface | extends-mcorch |\n| Project Slug | `viral-autopilot` |\n\n---\n\n## Sovereign Directive (Source of Truth Parameters \u2014 2026-06-17)\n\nQuatro requisitos-n\u00facleo, derivados da diretiva verbal do Sovereign e travados por 4 decis\u00f5es formais:\n\n| Req | Descri\u00e7\u00e3o | Estado pr\u00e9-suite (auditoria 2026-06-17) |\n|-----|-----------|------------------------------------------|\n| **R1** | Gera\u00e7\u00e3o autom\u00e1tica de conte\u00fado para redes sociais | \ud83d\udfe1 parcial \u2014 pipeline de TEXTO vivo; m\u00eddia \u00f3rf\u00e3 |\n| **R2** | Agendamento: tudo de uma vez OU lote a cada N dias (default 3) | \ud83d\udfe1 parcial \u2014 \"tudo de uma vez\" existe; recorr\u00eancia N\u00c3O existe |\n| **R3** | Loop auto-melhor\u00e1vel: analisar o ciclo anterior \u2192 melhorar o pr\u00f3ximo | \ud83d\udd34 ausente \u2014 loop aberto em 3 quebras |\n| **R4** | Conte\u00fado viral monetizado com comiss\u00e3o de afiliado do Mercado Livre | \ud83d\udfe1 parcial \u2014 receita ML madura, mas conte\u00fado product-unaware |\n\n**Decis\u00f5es Soberanas (par\u00e2metros fixos):**\n1. **BoK Gate:** suite-m\u00e3e NOVO `viral-autopilot` que UNIFICA R1-R4 e \u00e9 dono expl\u00edcito do orquestrador do ciclo. Referencia/promove (sem re-documentar): `mercado-livre-api` (FR-ML-001..012), `post-engine` (FR-PE-001..004), `viral-daily-canvas` (FR-VDC-001..004), `viralmind` (FR-024..026), `marketing-hub` (FR-MH-004).\n2. **MVP:** TEXTO + IMAGEM nas redes ATUAIS (WordPress/LinkedIn/Twitter-X). V\u00eddeo 9:16 + TikTok/Instagram/YouTube = FASE 2 expl\u00edcita.\n3. **Sinal R3:** combo completo \u2014 (a) cliques de afiliado (click ledger j\u00e1 existe), (b) engajamento org\u00e2nico por post (coletor novo), (c) receita por postback ML.\n4. **Produtos ML:** 3 SKUs semente (Roborock S8, Samsung Neo QLED 8K, Family Hub), com caminho de expans\u00e3o de cat\u00e1logo documentado.\n\n> **Origem:** auditoria material de 7 agentes (2026-06-17) \u2014 `project_viral_autopilot` (mem\u00f3ria). Cada gap citado abaixo carrega prova `path:linha`. Ver `01-mrd.md` \u00a72 e `05-sdd.md` \u00a78 (OTDs).\n\n---\n\n## Document Registry\n\n| # | File | Document | BoK Applied | Status |\n|---|------|----------|-------------|--------|\n| 0 | `00-index.md` | Project Manifest | \u2014 | [x] complete |\n| 1 | `01-mrd.md` | Market Requirements Document | BABOK v3 | [x] complete |\n| 2 | `02-brd.md` | Business Requirements Document | BABOK v3 | [x] complete |\n| 3 | `03-prd.md` | Product Requirements Document | ProdBOK + CXBOK | [x] complete |\n| 4 | `04-frd.md` | Functional Requirements Document | SWEBOK v4 | [x] complete |\n| 5 | `05-sdd.md` | System Design Document | SWEBOK v4 + CISSP CBK | [x] complete |\n| 6 | `06-data-model.md` | Data & Knowledge Model | DMBOK v2 | [x] complete |\n| 7 | `07-process-flow.md` | Process & Automation Blueprint | BPM CBOK v4 | [x] complete |\n| 8 | `08-quality-metrics.md` | Self-Optimization Specification | CMQ/OE BOK | [x] complete |\n\n---\n\n## Traceability Chain (summary \u2014 full matrices in each doc)\n\n```\nMR-VA-001 (gera\u00e7\u00e3o auto) \u2500\u2500\u25b6 BR-VA-001 \u2500\u2500\u25b6 PR-VA-002 \u2500\u2500\u25b6 FR-VA-003, FR-VA-013 \u2500\u2500\u25b6 orchestrate-step (lib) | generate-image\nMR-VA-002 (cad\u00eancia)     \u2500\u2500\u25b6 BR-VA-002 \u2500\u2500\u25b6 PR-VA-001, PR-VA-003 \u2500\u2500\u25b6 FR-VA-001, FR-VA-005, FR-VA-006 \u2500\u2500\u25b6 autopilot_plans | autopilot-cadence-cron\nMR-VA-003 (loop melhoria)\u2500\u2500\u25b6 BR-VA-003 \u2500\u2500\u25b6 PR-VA-004, PR-VA-005 \u2500\u2500\u25b6 FR-VA-008..011 \u2500\u2500\u25b6 creative_metrics | cycle-analyzer | feedback-inject\nMR-VA-004 (afiliado ML)  \u2500\u2500\u25b6 BR-VA-004 \u2500\u2500\u25b6 PR-VA-002 \u2500\u2500\u25b6 FR-VA-004, FR-VA-016 \u2500\u2500\u25b6 _shared/affiliate.ts | process-affiliate-link\nMR-VA-005 (ROI/criativo) \u2500\u2500\u25b6 BR-VA-005 \u2500\u2500\u25b6 PR-VA-007 \u2500\u2500\u25b6 FR-VA-009, FR-VA-017 \u2500\u2500\u25b6 creative_metrics | handle-ml-postback\nMR-VA-006 (custo)        \u2500\u2500\u25b6 BR-VA-006 \u2500\u2500\u25b6 PR-VA-006 \u2500\u2500\u25b6 FR-VA-007 \u2500\u2500\u25b6 autopilot_cycles | deduct_mco_coins\nMR-VA-007 (multi-tenant) \u2500\u2500\u25b6 BR-VA-007 \u2500\u2500\u25b6 PR-VA-001 \u2500\u2500\u25b6 FR-VA-001, NFR-VA-004 \u2500\u2500\u25b6 affiliate_config (RLS auth.uid())\nMR-VA-008 (sinal viral)  \u2500\u2500\u25b6 BR-VA-008 \u2500\u2500\u25b6 PR-VA-010, PR-VA-011 \u2500\u2500\u25b6 FR-VA-012, FR-VA-018 \u2500\u2500\u25b6 vm_affiliate_products | fetch-trends\n```\n\n---\n\n## Phase Completion Log\n\n| Phase | Name | Completed | Notes |\n|-------|------|-----------|-------|\n| 0 | Project Bootstrap | 2026-06-17 | Slug `viral-autopilot`; inputs derived from Sovereign directive |\n| 1 | Market & Business Intelligence | 2026-06-17 | MRD + BRD \u2014 8 MR, 8 BR, ROI model |\n| 2 | Product Definition | 2026-06-17 | PRD \u2014 2 personas, MoSCoW (MVP=texto+imagem) |\n| 3 | Technical Specification | 2026-06-17 | FRD (18 FR + 8 NFR) + SDD (STRIDE, RLS, 7 OTD) |\n| 4 | Data & Process Engineering | 2026-06-17 | 3 novas tabelas + 4 processos + 2 crons |\n| 5 | Quality & Autonomic Engineering | 2026-06-17 | 12 FMEA (4 RPN>100), kill-switch self-heal |\n| 6 | Traceability Validation | 2026-06-17 | Adversarial workflow \u2014 ver seal report |\n| 7 | Knowledge Mesh Injection | [ ] | `scripts/seed-viral-autopilot-bok-seal.ts` (pendente exec sob aprova\u00e7\u00e3o) |\n\n---\n\n## Open Technical Decisions (consolidated \u2014 detail in `05-sdd.md` \u00a78)\n\n| OTD ID | Description | Recommendation | Status |\n|--------|-------------|----------------|--------|\n| OTD-VA-001 | `campaign_metrics` (campaign-level) vs `creative_metrics` (por content_variant_id) | Nova `creative_metrics`; ETL agrega p/ campaign_metrics | Open |\n| OTD-VA-002 | Cron infra: pg_cron (nurture-advance) vs OS crontab (auto-publish) | pg_cron service-role por consist\u00eancia | Open |\n| OTD-VA-003 | Fonte de engajamento org\u00e2nico (LinkedIn/Twitter API tier) | Cliques de afiliado primeiro (j\u00e1 temos); org\u00e2nico best-effort gated por tier | Open |\n| OTD-VA-004 | Unidade do teto de custo: por ciclo vs di\u00e1rio | Cap por ciclo no plano + safety di\u00e1rio global (espelha vision-mcp) | Open |\n| OTD-VA-005 | Mecanismo de reinje\u00e7\u00e3o do feedback (texto cru vs features estruturadas) | Features estruturadas (top hooks/produtos/hor\u00e1rios) | Open |\n| OTD-VA-006 | Autonomia de sele\u00e7\u00e3o de produto (auto-score vs shortlist) | 3 SKUs semente agora (Decis\u00e3o 4); auto-score em v1.0 | Decided (seeds) |\n| OTD-VA-007 | `OTD-ML-MP-PER-USER` \u2014 secret de postback per-user | Fechar antes da atribui\u00e7\u00e3o de receita multi-tenant | Open (herdada) |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/00-index.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(20:58:09)*


## 🤖 Claude *(20:58:10)*

Manifesto pronto. Agora o **MRD** (BABOK — mercado, problema, requisitos de mercado):

## 🤖 Claude *(20:59:12)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/01-mrd.md",
  "content": "# MRD \u2014 Market Requirements Document\n\n**Project:** viral-autopilot  \n**Version:** v0.1 | **Date:** 2026-06-17  \n**BoK Applied:** BABOK v3 (Strategy Analysis + Elicitation & Collaboration)  \n**Status:** Draft\n\n---\n\n## 1. Executive Summary\n\nCriadores e afiliados que monetizam via Mercado Livre enfrentam um trabalho bra\u00e7al insustent\u00e1vel: para cada produto precisam pesquisar tend\u00eancia, escrever copy, formatar por rede, agendar, publicar e \u2014 quase nunca \u2014 medir o que funcionou para ajustar o pr\u00f3ximo post. O resultado \u00e9 volume baixo, inconsist\u00eancia e cegueira de desempenho. O **viral-autopilot** \u00e9 o piloto-autom\u00e1tico de conte\u00fado viral monetizado do MCORCH: a partir de um produto-alvo, gera criativos prontos para publica\u00e7\u00e3o em m\u00faltiplas redes, agenda-os (tudo de uma vez ou em lotes recorrentes a cada N dias) e \u2014 o diferencial central \u2014 **fecha o loop**: a cada ciclo ingere o desempenho real do ciclo anterior (cliques de afiliado, engajamento org\u00e2nico, receita confirmada) e realimenta os pr\u00f3ximos criativos. A janela \u00e9 agora: o custo marginal de gerar texto via LLM caiu a quase zero, as APIs de publica\u00e7\u00e3o social est\u00e3o maduras, e o MCORCH j\u00e1 tem a infraestrutura de receita ML per-user pronta \u2014 falta apenas o c\u00e9rebro que orquestra o ciclo e aprende.\n\n---\n\n## 2. Market Problem Statement\n\n### 2.1 Current State\n\nO afiliado/criador faz hoje, **manualmente e sem mem\u00f3ria de desempenho**:\n1. Escolhe um produto (intui\u00e7\u00e3o, n\u00e3o dado de comiss\u00e3o/tend\u00eancia).\n2. Escreve a copy \u00e0 m\u00e3o ou pede a um LLM gen\u00e9rico \u2014 sem \u00e2ngulo viral, sem amarra\u00e7\u00e3o ao produto.\n3. Adapta para cada rede, cola o link de afiliado manualmente, agenda um por um.\n4. Publica e **n\u00e3o mede** \u2014 n\u00e3o h\u00e1 leitura de qual criativo converteu para ajustar o pr\u00f3ximo.\n\nMesmo dentro do MCORCH, a auditoria material de 2026-06-17 provou que o pipeline atual: gera s\u00f3 **texto** (m\u00eddia \u00f3rf\u00e3, `generate-image`/`generate-video` com zero callers), monetiza **s\u00f3 o artigo** com cat\u00e1logo **hardcoded de 3 SKUs por regex** (`_shared/affiliate.ts`), **n\u00e3o tem recorr\u00eancia** (s\u00f3 2 pg_cron, nenhum re-gera conte\u00fado) e tem o loop de melhoria **aberto em 3 quebras** (`campaign_metrics` sem writer, `optimization_policy` nunca lida por gerador, `self-optimize` sem cron).\n\n### 2.2 Root Cause Analysis\n\n- **Gap de processo:** ningu\u00e9m desenhou o ciclo fechado gera\u00e7\u00e3o\u2192publica\u00e7\u00e3o\u2192an\u00e1lise\u2192re-gera\u00e7\u00e3o \u2014 cada pe\u00e7a existe isolada (ilhas: `fetch-trends`, `self-optimize`, `vm_affiliate_products`).\n- **Gap de tecnologia:** n\u00e3o h\u00e1 entidade de \"cad\u00eancia\" nem coletor de desempenho por criativo; o agendamento \u00e9 offset fixo hardcoded.\n- **Gap de mercado:** ferramentas de agendamento (Buffer, Hootsuite) publicam mas n\u00e3o geram nem aprendem; geradores de IA (Jasper, Copy.ai) geram mas n\u00e3o agendam, n\u00e3o monetizam ML e n\u00e3o fecham loop. Ningu\u00e9m une os quatro no mercado BR de afiliados ML.\n\n### 2.3 Desired State\n\nUm operador define um **plano de autopilot** (produtos-alvo, redes, modo: tudo-de-uma-vez ou a-cada-N-dias) e o sistema, sozinho e dentro de um teto de custo, **gera criativos virais product-aware monetizados, publica, mede e melhora a cada ciclo** \u2014 com ROI vis\u00edvel por pe\u00e7a de conte\u00fado e tudo escopado por tenant (credenciais e carteira do pr\u00f3prio operador).\n\n---\n\n## 3. Target Market Segments\n\n| Segment | Description | Size Estimate | Urgency | Accessibility |\n|---------|-------------|---------------|---------|---------------|\n| Primary | Afiliados/criadores BR do Mercado Livre que querem escalar conte\u00fado monetizado sem equipe | ~centenas de milhares de afiliados ML BR ativos | High | Alta \u2014 Usu\u00e1rio Zero (Gabriel) \u00e9 o piloto; onboarding via plano + BYOK |\n| Secondary | Pequenas ag\u00eancias/lojistas que gerenciam v\u00e1rias contas de produto e precisam de cad\u00eancia + ROI | dezenas de milhares de PMEs/ag\u00eancias | Medium | M\u00e9dia \u2014 exige multi-conta e relat\u00f3rio de ROI |\n\n### 3.1 TAM / SAM / SOM\n\n| Metric | Value | Basis |\n|--------|-------|-------|\n| TAM | ~R$ 50\u201380 M/ano (estimado) | Programa de afiliados ML no Brasil + criadores que monetizam links; proxy: ferramentas de social scheduling + AI copy no segmento BR |\n| SAM | ~R$ 8\u201312 M/ano (estimado) | Afiliados/criadores que pagariam por automa\u00e7\u00e3o de conte\u00fado+ROI (plano Pro/Enterprise MCORCH) |\n| SOM (12m) | ~R$ 0,5\u20131,5 M/ano (estimado) | Usu\u00e1rio Zero + primeiros 50\u2013200 tenants pagantes na fase Commercial |\n\n> Estimativas de ordem-de-grandeza para prioriza\u00e7\u00e3o (BABOK Strategy Analysis), n\u00e3o pesquisa de mercado prim\u00e1ria. Refinar quando o 1\u00ba tenant externo for onboardado.\n\n---\n\n## 4. Competitive Landscape\n\n| Competitor | Positioning | Strengths | Weaknesses | Our Differentiation |\n|------------|-------------|-----------|------------|---------------------|\n| Buffer / Hootsuite / Metricool | Agendamento e analytics de social | Maduros, multi-rede, analytics ricos | N\u00e3o geram conte\u00fado, n\u00e3o monetizam afiliado, n\u00e3o fecham loop de melhoria | Geramos + monetizamos ML + **loop auto-melhor\u00e1vel**, n\u00e3o s\u00f3 agendamos |\n| Jasper / Copy.ai / ChatGPT | Gera\u00e7\u00e3o de copy por IA | Boa qualidade de texto | Sem agendamento, sem ML, sem medi\u00e7\u00e3o/aprendizado, product-unaware | Product-aware + cad\u00eancia + atribui\u00e7\u00e3o de receita por criativo |\n| Linktree / Beacons + planilha manual | Bio-link + tracking manual de cliques | Simples, barato | Zero gera\u00e7\u00e3o/automa\u00e7\u00e3o; medi\u00e7\u00e3o manual; sem aprendizado | Click ledger autom\u00e1tico + ROI por pe\u00e7a + re-gera\u00e7\u00e3o informada |\n\n---\n\n## 5. Market Opportunity & Timing\n\n- **Custo marginal de gera\u00e7\u00e3o \u2248 0:** LLMs de texto (Groq/OpenRouter, BYOK) tornam vi\u00e1vel gerar dezenas de criativos por ciclo a custo desprez\u00edvel.\n- **APIs de publica\u00e7\u00e3o maduras:** LinkedIn publica hoje no MCORCH; WordPress e X j\u00e1 no pipeline; Meta/IG j\u00e1 tem `publish-meta`.\n- **Infra de receita ML pronta:** `affiliate_config` per-user, click ledger at\u00f4mico, `handle-ml-postback` HMAC idempotente \u2014 j\u00e1 constru\u00eddos e provados na auditoria. O diferencial s\u00f3 precisa do **orquestrador do ciclo + loop de aprendizado**.\n- **V\u00e1cuo competitivo:** nenhuma ferramenta une gera\u00e7\u00e3o+agendamento+monetiza\u00e7\u00e3o-ML+aprendizado para o afiliado BR.\n\n---\n\n## 6. Market Requirements\n\n> Priority: **Critical** (must have at launch) | **High** | **Medium** | **Low**\n\n| ID | Market Requirement | Priority | Rationale | Source |\n|----|-------------------|----------|-----------|--------|\n| MR-VA-001 | Gera\u00e7\u00e3o autom\u00e1tica de conte\u00fado viral para redes sociais a partir de um produto-alvo, sem opera\u00e7\u00e3o manual por post | Critical | R1 \u2014 n\u00facleo do valor; hoje pipeline gera texto gen\u00e9rico product-unaware | Diretiva Sovereign R1 |\n| MR-VA-002 | Cad\u00eancia configur\u00e1vel: disparo \u00fanico (\"tudo de uma vez\") OU recorrente a cada N dias (default 3), por tenant/plano | Critical | R2 \u2014 recorr\u00eancia inexistente hoje; \u00e9 o que torna \"aut\u00f4nomo\" | Diretiva Sovereign R2 |\n| MR-VA-003 | Loop auto-melhor\u00e1vel: o desempenho do ciclo anterior realimenta materialmente a gera\u00e7\u00e3o do pr\u00f3ximo | Critical | R3 \u2014 requisito mais valorizado e mais ausente (loop aberto em 3 quebras) | Diretiva Sovereign R3 |\n| MR-VA-004 | Monetiza\u00e7\u00e3o nativa: todo criativo amarrado a produto ML com link de afiliado per-user em TODO formato | Critical | R4 \u2014 hoje monetiza s\u00f3 o artigo, por regex, 3 SKUs hardcoded | Diretiva Sovereign R4 |\n| MR-VA-005 | Atribui\u00e7\u00e3o de receita e desempenho por criativo (ROI por pe\u00e7a de conte\u00fado) | High | Sem ROI por pe\u00e7a n\u00e3o h\u00e1 aprendizado nem prova de valor | Auditoria (R3 signal) |\n| MR-VA-006 | Controle de custo do loop aut\u00f4nomo: teto de gasto por ciclo + kill-switch quando saldo baixo | Critical | Loop aut\u00f4nomo recorrente pode drenar mcoCoins silenciosamente | Restri\u00e7\u00e3o Sovereign (custo) |\n| MR-VA-007 | Multi-tenancy estrita: cada operador usa suas pr\u00f3prias credenciais (BYOK) e carteira | High | API Tenancy Model per-user (diretiva 2026-05-19); isolamento de receita/quota | CLAUDE.md API Tenancy |\n| MR-VA-008 | Sele\u00e7\u00e3o de produto e \u00e2ngulo a partir de sinal viral real (trends + m\u00e9tricas de comiss\u00e3o) | Medium | `fetch-trends`/`vm_affiliate_products` existem mas est\u00e3o desconectados da gera\u00e7\u00e3o | Auditoria (R4) |\n\n---\n\n## 7. Success Metrics (Market-Level KPIs)\n\n| KPI | Definition | Target (6-month) | Target (12-month) | Measurement |\n|-----|-----------|------------------|-------------------|-------------|\n| Conte\u00fado aut\u00f4nomo publicado | n\u00ba de criativos publicados por autopilot sem a\u00e7\u00e3o manual | \u2265 90% dos posts do tenant | \u2265 95% | `scheduled_posts` com `cycle_id` not null |\n| Lift viral ciclo-a-ciclo | engajamento m\u00e9dio do ciclo N+1 \u00f7 ciclo N | \u2265 1.10\u00d7 ap\u00f3s 3 ciclos | \u2265 1.25\u00d7 | `creative_metrics` agregado por `cycle_id` |\n| Receita ML atribu\u00edda | R$ de comiss\u00e3o creditada e atribu\u00edda a criativos do autopilot | > R$ 0 (Usu\u00e1rio Zero) | crescente MoM | `affiliate_links.revenue_cents` por `content_variant_id` |\n| % criativos monetizados | criativos com link ML v\u00e1lido \u00f7 criativos gerados | 100% (todo formato) | 100% | `creative_metrics` \u2229 `affiliate_links` |\n| NPS | Net Promoter Score dos operadores | \u2265 40 | \u2265 55 | Survey in-app |\n\n---\n\n## 8. Regulatory & Compliance Context\n\n| Regulation | Applicability | Key Constraint | Compliance Owner |\n|------------|---------------|----------------|-----------------|\n| LGPD | Sim | PII residual em m\u00e9tricas de engajamento (n\u00e3o coletar dados pessoais de quem engaja al\u00e9m de agregados); direito ao apagamento por tenant | Engineering |\n| ToS Mercado Livre / Mercado Pago | Sim | Disclosure de afiliado; uso correto de `matt_word`/`matt_tool`; postback de comiss\u00e3o | Engineering + Sovereign |\n| ToS Redes Sociais (LinkedIn/X/Meta) | Sim | Limites de automa\u00e7\u00e3o/rate, rotulagem de conte\u00fado, sem spam; respeitar quotas de API tier | Engineering |\n| Publicidade (CONAR/identifica\u00e7\u00e3o de publi) | Sim | Conte\u00fado monetizado deve sinalizar car\u00e1ter publicit\u00e1rio/afiliado | Sovereign |\n\n---\n\n## 9. Traceability Matrix Stub\n\n| MR ID | \u2192 BR ID | Rationale |\n|-------|---------|-----------|\n| MR-VA-001 | BR-VA-001 | Gera\u00e7\u00e3o product-aware multi-formato |\n| MR-VA-002 | BR-VA-002 | Plano de cad\u00eancia + cron por-tenant |\n| MR-VA-003 | BR-VA-003 | Coletor + analisador + reinje\u00e7\u00e3o |\n| MR-VA-004 | BR-VA-004 | Monetiza\u00e7\u00e3o em todo formato com `content_variant_id` |\n| MR-VA-005 | BR-VA-005 | M\u00e9tricas por criativo + atribui\u00e7\u00e3o postback |\n| MR-VA-006 | BR-VA-006 | Or\u00e7amento de ciclo + kill-switch at\u00f4mico |\n| MR-VA-007 | BR-VA-007 | Resolu\u00e7\u00e3o per-user (affiliate_config, BYOK) |\n| MR-VA-008 | BR-VA-008 | Sele\u00e7\u00e3o por comiss\u00e3o+trend (3 SKUs semente) |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/01-mrd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(20:59:15)*

Agora o **BRD** (objetivos SMART, ROI, mcoCoins economics, riscos):

## 🤖 Claude *(21:00:27)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/02-brd.md",
  "content": "# BRD \u2014 Business Requirements Document\n\n**Project:** viral-autopilot  \n**Version:** v0.1 | **Date:** 2026-06-17  \n**BoK Applied:** BABOK v3 (Requirements Analysis & Design Definition)  \n**Status:** Draft\n\n---\n\n## 1. Executive Summary\n\nO `viral-autopilot` converte a infraestrutura de gera\u00e7\u00e3o e de receita ML j\u00e1 existente no MCORCH em um **motor de receita aut\u00f4nomo e auto-melhor\u00e1vel**. O objetivo de neg\u00f3cio \u00e9 triplo: (1) **escalar volume** de conte\u00fado monetizado sem trabalho humano por post; (2) **aumentar a convers\u00e3o** ao tornar cada criativo product-aware e informado pelo desempenho passado; (3) **proteger a margem** com tetos de custo e atribui\u00e7\u00e3o de ROI por pe\u00e7a. O retorno \u00e9 direto \u2014 comiss\u00e3o de afiliado ML \u2014 mas protegido por um modelo de custo em mcoCoins que garante que o loop aut\u00f4nomo nunca opere no preju\u00edzo silencioso.\n\n---\n\n## 2. Business Objectives (SMART)\n\n| ID | Objective | Specific | Measurable | Achievable | Relevant | Time-bound |\n|----|-----------|----------|------------|------------|----------|------------|\n| BO-001 | Automatizar a gera\u00e7\u00e3o+publica\u00e7\u00e3o monetizada | Operador define 1 plano e o sistema produz/publica criativos product-aware sem a\u00e7\u00e3o por post | \u2265 90% dos posts via autopilot (sem toque manual) | Pipeline de texto j\u00e1 vivo; falta orquestrador | Escala receita sem escalar trabalho | MVP at\u00e9 2026-07-31 |\n| BO-002 | Fechar o loop de melhoria por desempenho | Cada ciclo l\u00ea o desempenho do anterior e ajusta os pr\u00f3ximos criativos | Lift de engajamento ciclo-a-ciclo \u2265 1.10\u00d7 ap\u00f3s 3 ciclos | `self-optimize` j\u00e1 existe (esqueleto); fechar 3 quebras | \u00c9 o diferencial do produto | v1.0 at\u00e9 2026-08-31 |\n| BO-003 | Garantir margem positiva e custo controlado | Todo ciclo respeita teto de mcoCoins e atribui ROI por criativo | 100% dos ciclos com `spend_mco \u2264 budget_cap`; ROI por pe\u00e7a vis\u00edvel | D\u00e9bito at\u00f4mico `deduct_mco_coins` j\u00e1 existe | Evita o autopilot virar buraco de carteira | MVP at\u00e9 2026-07-31 |\n| BO-004 | Monetizar todo formato gerado | Artigo + LinkedIn + X saem com link ML v\u00e1lido per-user | 100% dos criativos com `content_variant_id` + link rastre\u00e1vel | `monetizeContent` + `affiliate_config` j\u00e1 existem (s\u00f3 no artigo hoje) | Sem monetiza\u00e7\u00e3o universal n\u00e3o h\u00e1 atribui\u00e7\u00e3o nem receita | MVP at\u00e9 2026-07-31 |\n\n---\n\n## 3. Stakeholder Register\n\n| ID | Role | Interest | Influence | Communication Cadence | Contact |\n|----|------|----------|-----------|----------------------|---------|\n| SH-001 | Sovereign / Maestro | High | High | Continuous | Gabriel Zarattini |\n| SH-002 | Operador/Afiliado (Primary) \u2014 Usu\u00e1rio Zero | High | Medium | Por ciclo (dashboard) + NPS mensal | gabrielcall@gmail.com |\n| SH-003 | Mercado Livre / Mercado Pago | Medium | High | Via postback + ToS (ass\u00edncrono) | Plataforma externa |\n| SH-004 | Redes sociais (LinkedIn/X/Meta) | Medium | High | Via API + ToS/quotas | Plataformas externas |\n| SH-005 | MCORCH Master Execution Agent (Operator) | High | Medium | Por sess\u00e3o (handoff) | AIOS |\n\n---\n\n## 4. Business Requirements\n\n> Cada BR rastreia \u2265 1 MR. Custo mcoCoins definido para BR com gera\u00e7\u00e3o via IA.\n\n| ID | Requirement | MR Traced | Priority | mcoCoins Cost | Acceptance Criteria |\n|----|-------------|-----------|----------|---------------|---------------------|\n| BR-VA-001 | Gera\u00e7\u00e3o product-aware multi-formato: artigo+post+thread com copy de venda constru\u00edda em torno de um produto-alvo (id+nome+imagem ML), substituindo os prompts B2B hardcoded por framework de gancho viral | MR-VA-001 | Critical | herda `orchestrate-content` (10 mco/run + sub-steps) | Dado um produto-alvo, os 3 formatos mencionam o produto e cont\u00eam link ML v\u00e1lido |\n| BR-VA-002 | Plano de cad\u00eancia persistido (modo all-at-once vs lote-a-cada-N-dias, default 3) + cron por-tenant que dispara o ciclo sem a\u00e7\u00e3o humana | MR-VA-002 | Critical | 0 (orquestra\u00e7\u00e3o) | Plano com `interval_days=3` dispara automaticamente a cada 3 dias; modo all-at-once gera lote \u00fanico |\n| BR-VA-003 | Loop fechado: coletar desempenho do ciclo \u2192 analisar \u2192 reinjetar aprendizados (top hooks/produtos/hor\u00e1rios) na gera\u00e7\u00e3o do pr\u00f3ximo ciclo | MR-VA-003 | Critical | 5 mco/an\u00e1lise (LLM, herda `self-optimize`) | Ciclo N+1 recebe no prompt o resumo estruturado do desempenho do ciclo N |\n| BR-VA-004 | Monetiza\u00e7\u00e3o em TODO formato com `content_variant_id` por criativo, honrando o produto-alvo (corrigir param `affiliate_url` dropado) | MR-VA-004 | Critical | 0 (parte da gera\u00e7\u00e3o) | LinkedIn e Twitter, n\u00e3o s\u00f3 o artigo, saem com link ML rastre\u00e1vel + `content_variant_id` |\n| BR-VA-005 | M\u00e9tricas por criativo unificadas (cliques afiliado + engajamento org\u00e2nico + receita postback) + atribui\u00e7\u00e3o de ROI por pe\u00e7a | MR-VA-005 | High | 0 (ingest\u00e3o) | `creative_metrics` populada por \u2265 1 fonte real; ROIWidget mostra ROI por `content_variant_id` |\n| BR-VA-006 | Or\u00e7amento de ciclo (teto mcoCoins) + kill-switch que pausa o plano quando saldo < limiar, ANTES de qualquer deduct | MR-VA-006 | Critical | 0 (guarda) | Ciclo aborta sem cobrar quando `spend projetado > budget_cap` ou `saldo < min`; plano pausado + notifica\u00e7\u00e3o |\n| BR-VA-007 | Toda credencial externa (ML, redes, LLM) resolvida per-user via `auth.uid()`; sem chave global em fluxo user-facing | MR-VA-007 | High | 0 | Tenant A nunca usa credencial/quota de Tenant B; fail-closed quando n\u00e3o configurado |\n| BR-VA-008 | Sele\u00e7\u00e3o de produto por comiss\u00e3o+trend a partir do cat\u00e1logo (3 SKUs semente agora; caminho de auto-descoberta documentado) | MR-VA-008 | Medium | 0 (sele\u00e7\u00e3o) | Plano referencia produtos do cat\u00e1logo `vm_affiliate_products`; ranking por `commission_value`+`trend_score` dispon\u00edvel |\n\n---\n\n## 5. ROI Model\n\n### 5.1 Cost Estimates\n\n| Cost Item | Type | Monthly Estimate | Annual Estimate |\n|-----------|------|-----------------|----------------|\n| Infraestrutura (Supabase, Docker mesh, pg_cron) | OpEx | ~R$ 0 incremental (reusa stack existente) | ~R$ 0 incremental |\n| Chamadas LLM (texto, BYOK por tenant) | Variable | ~R$ 0\u201320/tenant (texto \u00e9 quase free; custo no tenant via BYOK) | \u2014 |\n| Gera\u00e7\u00e3o de imagem (DALL\u00b7E/Nano Banana) | Variable | ~$0.04/imagem \u00d7 volume do ciclo | escala com n\u00ba de criativos |\n| Desenvolvimento (inicial \u2014 MVP+v1.0) | CapEx | \u2014 | ~2\u20133 sprints de engenharia (interno) |\n\n### 5.2 Revenue Streams\n\n| Stream | Model | Monthly Potential | Notes |\n|--------|-------|-----------------|-------|\n| Comiss\u00e3o de afiliado ML | Transaction (revenue share) | vari\u00e1vel \u2014 fun\u00e7\u00e3o de volume \u00d7 CTR \u00d7 taxa de convers\u00e3o \u00d7 comiss\u00e3o | Receita direta; atribu\u00edda por `content_variant_id` via postback |\n| Consumo de mcoCoins | Subscription/consumption | 10 mco/run + 5 mco/an\u00e1lise \u00d7 ciclos | Receita indireta da plataforma; alinha custo ao uso |\n\n### 5.3 Payback Analysis\n\n| Metric | Value |\n|--------|-------|\n| Break-even (months) | Indeterminado at\u00e9 1\u00ba postback real de convers\u00e3o ML (OTD-VA-007 / OTD-ML-MP-PER-USER) \u2014 depende de CTR\u00d7convers\u00e3o observados |\n| 12-month ROI | A medir; meta \u00e9 receita ML atribu\u00edda > custo de mcoCoins do loop por tenant |\n| IRR (estimated) | N/A nesta fase (Usu\u00e1rio Zero pr\u00e9-Commercial) |\n\n> **Honestidade material (Lei 1):** o payback real s\u00f3 pode ser afirmado ap\u00f3s um postback de convers\u00e3o ML chegar em produ\u00e7\u00e3o. Hoje a receita atribu\u00edvel \u00e9 R$ 0 provados. O ROI Model \u00e9 proje\u00e7\u00e3o, n\u00e3o fato.\n\n---\n\n## 6. mcoCoins Economics\n\n| Operation | Coins/Run | Plan Tier Mapping | Monthly Volume (est.) | Monthly Revenue (est.) |\n|-----------|-----------|-------------------|-----------------------|----------------------|\n| Ciclo de gera\u00e7\u00e3o (autopilot) | 10 mco/run (herda `orchestrate-content`) + sub-steps | Starter(500) / Pro(2000) / Ent(10k) | fun\u00e7\u00e3o de `interval_days` \u00d7 n\u00ba produtos \u00d7 redes | consumo de plano |\n| An\u00e1lise de ciclo (self-optimize) | 5 mco/an\u00e1lise | idem | 1 por ciclo por plano | consumo de plano |\n| Gera\u00e7\u00e3o de imagem | calibrar via SOP `mcoin-cost-calibration` (modelo 4\u00d7-floor) | idem | 1+ por criativo | consumo de plano |\n\n> **Teto obrigat\u00f3rio (BR-VA-006):** cada plano carrega `budget_cap_mco` por ciclo. O ciclo soma o custo projetado (10 + 5 + imagem \u00d7 n\u00ba criativos) e **aborta antes de deduzir** se exceder o teto ou se o saldo cair abaixo do m\u00ednimo. Espelha o modelo de caps do `vision-mcp` (per-plano + safety di\u00e1rio).\n\n---\n\n## 7. Constraints & Assumptions\n\n### Constraints\n- **API Tenancy per-user (UNBREAKABLE):** toda credencial externa resolvida via `auth.uid()`; env global s\u00f3 em cron/service-role sem JWT, nunca como caminho prim\u00e1rio user-facing.\n- **mcoCoins at\u00f4mico:** dedu\u00e7\u00e3o s\u00f3 via `deduct_mco_coins` RPC; nunca client-side; sempre depois do gate de teto.\n- **RLS default-deny** em toda nova tabela; multi-tenant `user_id (+ project_id)`.\n- **MVP = texto + imagem nas redes atuais** (WordPress/LinkedIn/Twitter-X). V\u00eddeo + TikTok/IG/YT s\u00e3o fase 2.\n- **Cyber-Sentinel gate** no t\u00f3pico e no conte\u00fado gerado antes de publicar (brand-safety + anti-prompt-injection).\n- Toda migration nova passa `/security-review` antes do commit.\n\n### Assumptions\n- O click ledger ML (`record_affiliate_click`) j\u00e1 conta cada clique que passa pelo nosso redirect (provado na auditoria).\n- LinkedIn publica hoje; Twitter depende de tier Basic; Meta/IG via `publish-meta` (dev mode).\n- O postback de convers\u00e3o ML (`handle-ml-postback`) \u00e9 infra pronta mas **n\u00e3o provado em produ\u00e7\u00e3o** \u2014 atribui\u00e7\u00e3o de receita real depende de fechar OTD-ML-MP-PER-USER.\n- Engajamento org\u00e2nico por post depende da disponibilidade de insights na API de cada rede (tier-dependente) \u2014 cliques de afiliado s\u00e3o o sinal sempre-dispon\u00edvel.\n\n---\n\n## 8. Business Risk Register\n\n| Risk ID | Description | Probability | Impact | RPN | Mitigation |\n|---------|-------------|-------------|--------|-----|------------|\n| BR-RISK-001 | Loop aut\u00f4nomo drena mcoCoins silenciosamente (cron \u00d7 produtos \u00d7 redes) | 4 | 5 | 20 | Teto por ciclo + kill-switch + safety di\u00e1rio (BR-VA-006 / FR-VA-007); notifica\u00e7\u00e3o saldo baixo |\n| BR-RISK-002 | \"Auto-melhoria teatral\": loop roda sem dado real e o LLM cai em recomenda\u00e7\u00f5es gen\u00e9ricas | 4 | 4 | 16 | Bloquear an\u00e1lise quando `creative_metrics` vazia; usar cliques de afiliado (sempre dispon\u00edvel) como sinal m\u00ednimo (OTD-VA-003) |\n| BR-RISK-003 | Postback ML nunca chega \u2192 receita atribu\u00edda = 0 mesmo com vendas | 3 | 5 | 15 | Fechar OTD-ML-MP-PER-USER; provar 1 postback real; ROI usa cliques como proxy enquanto isso |\n| BR-RISK-004 | Conte\u00fado aut\u00f4nomo viola ToS de rede/ML ou publica algo off-brand | 3 | 5 | 15 | Cyber-Sentinel gate pr\u00e9-publica\u00e7\u00e3o; disclosure de afiliado; rate/quota por tier; HITL opcional no plano |\n| BR-RISK-005 | Volume alto de conte\u00fado que n\u00e3o converte (custo sobe, comiss\u00e3o n\u00e3o vem) | 3 | 4 | 12 | ROI por criativo + kill-switch por margem; loop poda \u00e2ngulos de baixa convers\u00e3o |\n| BR-RISK-006 | Conte\u00fado s\u00f3 em texto em WP/LinkedIn/X (baixa viraliza\u00e7\u00e3o org\u00e2nica) | 4 | 3 | 12 | Imagem no MVP; v\u00eddeo+TikTok/IG/YT priorizados na fase 2 |\n\n> Probability & Impact: 1=Low, 5=High. RPN = Probability \u00d7 Impact.\n\n---\n\n## 9. Business Acceptance Criteria\n\n| ID | Criterion | Verification Method |\n|----|-----------|-------------------|\n| BAC-001 | Um plano de autopilot com `interval_days=3` dispara um ciclo automaticamente sem a\u00e7\u00e3o humana | SELECT em `autopilot_cycles` mostrando ciclos sequenciais com `started_at` espa\u00e7ados ~3d |\n| BAC-002 | Todo criativo gerado (artigo+LinkedIn+X) cont\u00e9m link ML v\u00e1lido com `content_variant_id` | SELECT `creative_metrics`/`affiliate_links` por `cycle_id`; 100% com link |\n| BAC-003 | Nenhum ciclo cobra mcoCoins acima do `budget_cap_mco`; ciclo aborta limpo quando excede | Smoke zero-cost: plano com cap baixo \u2192 ciclo aborta, saldo intacto |\n| BAC-004 | O ciclo N+1 recebe no prompt o resumo de desempenho do ciclo N | Log/trace do prompt do gerador contendo features do `optimization_policy` do ciclo anterior |\n| BAC-005 | ROI por criativo vis\u00edvel no dashboard (cliques + receita atribu\u00edda por pe\u00e7a) | UI `AutopilotPage` exibindo `creative_metrics` por `content_variant_id` |\n\n---\n\n## 10. Traceability Matrix\n\n| MR ID | BR ID | PR ID (stub) |\n|-------|-------|--------------|\n| MR-VA-001 | BR-VA-001 | PR-VA-002, PR-VA-008 |\n| MR-VA-002 | BR-VA-002 | PR-VA-001, PR-VA-003 |\n| MR-VA-003 | BR-VA-003 | PR-VA-004, PR-VA-005 |\n| MR-VA-004 | BR-VA-004 | PR-VA-002 |\n| MR-VA-005 | BR-VA-005 | PR-VA-007 |\n| MR-VA-006 | BR-VA-006 | PR-VA-006 |\n| MR-VA-007 | BR-VA-007 | PR-VA-001 |\n| MR-VA-008 | BR-VA-008 | PR-VA-010, PR-VA-011 |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/02-brd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:00:30)*


## 🤖 Claude *(21:00:31)*

MRD+BRD selados (8 MR, 8 BR). Agora o **PRD** (personas, jornadas, MoSCoW com MVP=texto+imagem, Gherkin):

## 🤖 Claude *(21:01:42)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/03-prd.md",
  "content": "# PRD \u2014 Product Requirements Document\n\n**Project:** viral-autopilot  \n**Version:** v0.1 | **Date:** 2026-06-17  \n**BoK Applied:** ProdBOK + CXBOK  \n**Status:** Draft\n\n---\n\n## 1. Product Vision Statement\n\n> Para **afiliados e criadores do Mercado Livre** que **n\u00e3o t\u00eam tempo nem equipe para produzir, agendar e otimizar conte\u00fado viral monetizado**, o **viral-autopilot** \u00e9 um **piloto-autom\u00e1tico de conte\u00fado** que **gera criativos product-aware, publica em cad\u00eancia configur\u00e1vel e melhora a cada ciclo lendo o desempenho real**. Diferente de **ferramentas de agendamento (que s\u00f3 publicam) ou geradores de IA (que s\u00f3 escrevem)**, nosso produto **fecha o loop gera\u00e7\u00e3o\u2192publica\u00e7\u00e3o\u2192atribui\u00e7\u00e3o\u2192re-gera\u00e7\u00e3o com receita de comiss\u00e3o ML rastre\u00e1vel por pe\u00e7a**.\n\n---\n\n## 2. User Personas\n\n### Persona 1 \u2014 Rafael, o Afiliado-Solo (Primary)\n\n| Attribute | Detail |\n|-----------|--------|\n| Role | Afiliado ML / criador de conte\u00fado que monetiza links (perfil do Usu\u00e1rio Zero) |\n| Goals | Escalar volume de conte\u00fado monetizado sem virar ref\u00e9m da produ\u00e7\u00e3o manual; saber o que converte |\n| Frustrations | Escrever copy \u00e0 m\u00e3o para cada produto/rede; colar links manualmente; n\u00e3o saber qual post deu venda |\n| Tech-savviness | 3 (confort\u00e1vel com ferramentas, n\u00e3o-programador) |\n| MCORCH usage pattern | Define plano(s) de autopilot, confere o dashboard de ROI por ciclo, ajusta produtos-alvo |\n| Quote | _\"Eu quero ligar isso numa sexta e na segunda ter conte\u00fado no ar, com link certo, e ver o que vendeu.\"_ |\n\n### Persona 2 \u2014 Marina, a Gestora de M\u00faltiplas Contas (Secondary)\n\n| Attribute | Detail |\n|-----------|--------|\n| Role | Gestora de PME/ag\u00eancia operando v\u00e1rias contas/produtos de afiliado |\n| Goals | Cad\u00eancia consistente em v\u00e1rias contas; relat\u00f3rio de ROI por produto/criativo para decidir investimento |\n| Frustrations | Gerenciar credenciais e calend\u00e1rio de N contas; sem vis\u00e3o consolidada de qual criativo performa |\n| Tech-savviness | 4 |\n| MCORCH usage pattern | V\u00e1rios planos (um por produto/conta), BYOK por tenant, foco no relat\u00f3rio ciclo-a-ciclo |\n| Quote | _\"Preciso de cad\u00eancia previs\u00edvel e um n\u00famero de ROI por pe\u00e7a que eu possa mostrar ao cliente.\"_ |\n\n---\n\n## 3. User Journey Maps\n\n### Journey: Ligar o Autopilot (Rafael, Happy Path)\n\n| Stage | Action | Touchpoint | Emotion | Opportunity |\n|-------|--------|-----------|---------|-------------|\n| Awareness | Descobre o Autopilot no dashboard | `AutopilotPage` (nav) | \ud83d\ude10 Neutral | Empty-state explicando o ciclo + custo |\n| Consideration | Cria um plano: escolhe produtos-alvo + redes + modo | Plan editor | \ud83e\udd14 Curious | Pr\u00e9-visualizar custo projetado por ciclo (mcoCoins) |\n| Activation | Salva o plano e dispara \"tudo de uma vez\" (ou ativa cad\u00eancia) | Run/Activate button | \ud83d\ude0a Excited | Confirmar teto de custo antes de disparar |\n| Value | V\u00ea criativos publicados e o primeiro ROI por pe\u00e7a | Cycle timeline + ROI cards | \ud83d\ude80 Delighted | Destacar o \"vencedor\" do ciclo |\n| Retention | Ciclo seguinte melhora sozinho; ajusta produtos | Auto-improve insight card | \u2764\ufe0f Loyal | Mostrar o lift ciclo-a-ciclo |\n\n#### Edge Case 1: Saldo insuficiente / teto estourado\n> No disparo, o custo projetado excede `budget_cap_mco` ou o saldo est\u00e1 abaixo do m\u00ednimo \u2192 ciclo **n\u00e3o inicia**, plano n\u00e3o cobra, toast PT-BR \"Saldo/teto insuficiente para este ciclo\" + plano marcado `paused`.\n\n#### Edge Case 2: M\u00e9tricas ainda n\u00e3o chegaram (ciclo 1)\n> No primeiro ciclo n\u00e3o h\u00e1 desempenho anterior \u2192 o analisador usa baseline (sem dado) e o gerador roda com framework viral padr\u00e3o + sinal de trends; o insight card sinaliza \"coletando desempenho \u2014 melhoria a partir do ciclo 2\".\n\n---\n\n## 4. Feature Inventory (MoSCoW)\n\n> Effort: S=hours, M=days, L=week, XL=sprint\n\n### Must Have (MVP \u2014 texto + imagem nas redes atuais)\n\n| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |\n|----|---------|---------|-----------|--------|-------------|-------|\n| PR-VA-001 | **Autopilot Plan** \u2014 criar/editar plano (produtos-alvo, redes, modo all-at-once vs cada-N-dias, teto) | P1, P2 | BR-VA-002, BR-VA-007, BR-VA-008 | L | 0 | Entidade `autopilot_plans` per-user; default `interval_days=3` |\n| PR-VA-002 | **Product-aware generation** \u2014 texto monetizado (artigo+LinkedIn+X) com copy de venda em torno do produto-alvo, link ML em todo formato | P1 | BR-VA-001, BR-VA-004 | L | herda 10 + sub-steps | Substitui prompts B2B; corrige `affiliate_url` dropado |\n| PR-VA-003 | **Cadence scheduler** \u2014 cron por-tenant que dispara o ciclo a cada N dias (auto-refill) | P1, P2 | BR-VA-002 | L | 0 | Generaliza primitiva nurture (`next_run_at` + pg_cron) |\n| PR-VA-004 | **Performance collector** \u2014 cliques afiliado + engajamento org\u00e2nico + receita \u2192 `creative_metrics` | P1, P2 | BR-VA-005, BR-VA-003 | L | 0 | Combo (Decis\u00e3o 3); cliques primeiro, org\u00e2nico best-effort |\n| PR-VA-005 | **Self-improvement feedback** \u2014 analisar lote anterior \u2192 injetar features no prompt do pr\u00f3ximo | P1 | BR-VA-003 | M | 5 (an\u00e1lise) | Fecha as 3 quebras do `self-optimize` |\n| PR-VA-006 | **Cost guardrail** \u2014 teto por ciclo + kill-switch + alerta de saldo baixo (antes do deduct) | P1, P2 | BR-VA-006 | M | 0 | `budget_cap_mco` no plano; espelha caps vision-mcp |\n| PR-VA-007 | **Autopilot dashboard** \u2014 timeline de ciclos + criativos + ROI por pe\u00e7a | P1, P2 | BR-VA-005 | M | 0 | Hook `useAutopilot`; reusa ROIWidget |\n| PR-VA-008 | **Image creative** \u2014 imagem por criativo, produto ML como refer\u00eancia, formato por plataforma | P1 | BR-VA-001 | M | ~img cost | MVP (Decis\u00e3o 2); plugar `generate-image` (hoje \u00f3rf\u00e3) ao ciclo |\n\n### Should Have (v1.0)\n\n| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |\n|----|---------|---------|-----------|--------|-------------|-------|\n| PR-VA-010 | **Auto product selection** \u2014 selecionar produto do cat\u00e1logo por `commission_value`+`trend_score` (al\u00e9m dos 3 semente) | P1, P2 | BR-VA-008 | M | 0 | OTD-VA-006: auto-score em v1.0 |\n| PR-VA-011 | **Trend-informed angle** \u2014 `fetch-trends`/`vm_trends` pautam o \u00e2ngulo viral | P1 | BR-VA-008 | M | 0 | Reconecta a ilha de trends ao gerador |\n| PR-VA-012 | **A/B variant generation** \u2014 N varia\u00e7\u00f5es por criativo por ciclo, escolhe vencedora pelo desempenho | P1 | BR-VA-003 | M | herda gera\u00e7\u00e3o | Acelera o aprendizado do loop |\n| PR-VA-013 | **HITL gate opcional** \u2014 aprova\u00e7\u00e3o humana antes de publicar (plano configura) | P2 | BR-VA-004 | S | 0 | Reusa policy-engine do `intent-execute` |\n\n### Could Have (Future / Fase 2)\n\n| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |\n|----|---------|---------|-----------|--------|-------------|-------|\n| PR-VA-020 | **Video creative 9:16** (TikTok/Reels/Shorts) | P1 | BR-VA-001 | XL | v\u00eddeo cost | Fase 2 (Decis\u00e3o 2); `generate-video` hoje \u00f3rf\u00e3 |\n| PR-VA-021 | **TikTok/Instagram/YouTube publishing** | P1 | BR-VA-001 | XL | 0 | Fase 2; OAuth + publish novos destinos |\n| PR-VA-022 | **Catalog auto-discovery cron** \u2014 produtiza `discover-affiliate-products.ts` (hoje CLI manual) | P2 | BR-VA-008 | L | 0 | Score por comiss\u00e3o/trend real, n\u00e3o s\u00f3 log10(pre\u00e7o) |\n\n### Won't Have (This Cycle)\n\n- Gest\u00e3o de an\u00fancios pagos (Meta Ads) dentro do autopilot \u2014 `sync-meta-ads` permanece separado.\n- Deduplica\u00e7\u00e3o de atribui\u00e7\u00e3o cross-network (multi-touch) \u2014 atribui\u00e7\u00e3o \u00e9 por clique/postback no MVP.\n- Outreach a influenciadores / parcerias.\n\n---\n\n## 5. Release Phasing\n\n### MVP Scope\n**Target date:** 2026-07-31  \n**Included:** PR-VA-001, PR-VA-002, PR-VA-003, PR-VA-004, PR-VA-005, PR-VA-006, PR-VA-007, PR-VA-008  \n**Success gate:** um plano dispara ciclos a cada 3 dias, gera texto+imagem monetizados em WP/LinkedIn/X, coleta cliques de afiliado, e o ciclo 2 demonstra reinje\u00e7\u00e3o do desempenho do ciclo 1 \u2014 tudo dentro do teto de custo (smoke zero-cost provando o kill-switch).\n\n### v1.0 Scope\n**Target date:** 2026-08-31  \n**Adds:** PR-VA-010, PR-VA-011, PR-VA-012, PR-VA-013  \n**Success gate:** sele\u00e7\u00e3o autom\u00e1tica de produto por comiss\u00e3o+trend + \u00e2ngulo informado por trends + A/B + HITL opcional; lift de engajamento ciclo-a-ciclo \u2265 1.10\u00d7 medido.\n\n### Future Scope\n**Items:** PR-VA-020, PR-VA-021, PR-VA-022  \n**Condition:** ap\u00f3s MVP validado e decis\u00e3o Sovereign de priorizar m\u00eddia viral (v\u00eddeo 9:16 + redes virais) \u2014 gate de esfor\u00e7o XL.\n\n---\n\n## 6. Luxury UX Specifications\n\n### 6.1 Color & Visual Identity\n\n| Token | Value | Usage |\n|-------|-------|-------|\n| `--bg-deep` | `#0A0A0F` | Canvas background da AutopilotPage |\n| `--accent-violet` | `#7C3AED` | CTA \"Ativar Autopilot\", estado ativo do plano |\n| `--accent-cyan` | `#06B6D4` | M\u00e9tricas de ROI, gr\u00e1ficos de lift ciclo-a-ciclo |\n| `--glass-surface` | `rgba(255,255,255,0.04)` | Cards de ciclo e de criativo |\n| `--border-subtle` | `rgba(255,255,255,0.08)` | Bordas de card |\n\n### 6.2 Animation Guidelines\n\n| Element | Library | Duration | Easing |\n|---------|---------|----------|--------|\n| Transi\u00e7\u00e3o de p\u00e1gina | Framer Motion | 300ms | `easeInOut` |\n| Entrada de card de ciclo | Framer Motion | 300ms | `easeOut` |\n| Pulse de status \"ciclo rodando\" | CSS keyframes | 2s | `ease-in-out infinite` |\n| Highlight do criativo \"vencedor\" | Framer Motion | 150ms | `easeOut` |\n\n### 6.3 Interaction Patterns\n\n- **Cards:** glass morphism \u2014 `backdrop-blur-sm`, borda sutil, sombra `0 4px 24px rgba(0,0,0,0.4)`.\n- **Bot\u00e3o \"Ativar Autopilot\":** gradiente no hover; confirma\u00e7\u00e3o de teto de custo (mcoCoins) antes do disparo.\n- **Loading:** skeleton shimmer nos cards de ciclo (nunca spinner em \u00e1rea de conte\u00fado).\n- **Toasts:** `sonner` \u2014 sucesso=violeta, erro=vermelho, info=ciano. Saldo/teto insuficiente = toast PT-BR expl\u00edcito.\n\n### 6.4 Accessibility (WCAG 2.1 AA)\n\n- Contraste \u2265 4.5:1 para texto sobre vidro.\n- Todos os controles do plano naveg\u00e1veis por teclado.\n- ARIA labels nos bot\u00f5es \u00edcone (ativar/pausar/editar plano).\n- Foco vis\u00edvel \u2265 2px.\n\n---\n\n## 7. Acceptance Criteria (Gherkin)\n\n```gherkin\nFeature: Viral Autopilot \u2014 ciclo aut\u00f4nomo monetizado e auto-melhor\u00e1vel\n\n  Scenario: Ativar plano com cad\u00eancia de 3 dias (PR-VA-001, PR-VA-003)\n    Given um operador autenticado com saldo de mcoCoins suficiente\n    And um plano com produtos-alvo [Roborock S8], redes [wordpress, linkedin, twitter], modo \"every_n_days\", interval_days 3\n    When o operador ativa o plano\n    Then o sistema agenda next_run_at para now\n    And o cron dispara o primeiro ciclo sem a\u00e7\u00e3o humana\n    And cria uma linha em autopilot_cycles com status \"running\"\n\n  Scenario: Gera\u00e7\u00e3o product-aware monetizada em todo formato (PR-VA-002, PR-VA-008)\n    Given um ciclo em execu\u00e7\u00e3o com produto-alvo \"Roborock S8\"\n    When o gerador produz artigo, post de LinkedIn, thread de X e imagem\n    Then cada formato menciona o produto e cont\u00e9m um link de afiliado ML v\u00e1lido com content_variant_id\n    And a imagem usa a image_url do produto como refer\u00eancia\n\n  Scenario: Kill-switch de custo antes do deduct (PR-VA-006)\n    Given um plano com budget_cap_mco 5 e custo de ciclo projetado 15\n    When o cron tenta disparar o ciclo\n    Then o ciclo aborta com status \"aborted_budget\"\n    And nenhum mcoCoin \u00e9 deduzido\n    And o plano \u00e9 marcado \"paused\" com notifica\u00e7\u00e3o PT-BR \"Teto de custo insuficiente para este ciclo\"\n\n  Scenario: Loop auto-melhor\u00e1vel realimenta o ciclo seguinte (PR-VA-004, PR-VA-005)\n    Given o ciclo 1 publicou criativos e o coletor gravou cliques de afiliado em creative_metrics\n    When o ciclo 2 \u00e9 disparado\n    Then o analisador produz um optimization_policy a partir do desempenho do ciclo 1\n    And o prompt de gera\u00e7\u00e3o do ciclo 2 inclui as features de melhor desempenho (top hook/produto/hor\u00e1rio)\n\n  Scenario: ROI por criativo vis\u00edvel (PR-VA-007)\n    Given criativos publicados com cliques e/ou receita atribu\u00edda\n    When o operador abre a AutopilotPage\n    Then v\u00ea, por content_variant_id, cliques, receita atribu\u00edda e o criativo vencedor do ciclo\n```\n\n---\n\n## 8. Traceability Matrix\n\n| MR ID | BR ID | PR ID |\n|-------|-------|-------|\n| MR-VA-001 | BR-VA-001 | PR-VA-002, PR-VA-008 |\n| MR-VA-002 | BR-VA-002 | PR-VA-001, PR-VA-003 |\n| MR-VA-003 | BR-VA-003 | PR-VA-004, PR-VA-005, PR-VA-012 |\n| MR-VA-004 | BR-VA-004 | PR-VA-002, PR-VA-013 |\n| MR-VA-005 | BR-VA-005 | PR-VA-007 |\n| MR-VA-006 | BR-VA-006 | PR-VA-006 |\n| MR-VA-007 | BR-VA-007 | PR-VA-001 |\n| MR-VA-008 | BR-VA-008 | PR-VA-010, PR-VA-011, PR-VA-022 |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/03-prd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:01:45)*


## 🤖 Claude *(21:01:47)*

PRD selado (2 personas, MoSCoW, 5 cenários Gherkin). Agora o **FRD** — o documento mais crítico, com as FRs explícitas de R2 (cadência) e R3 (loop fechado) que hoje não existem em suite algum:

## 🤖 Claude *(21:03:00)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md",
  "content": "# FRD \u2014 Functional Requirements Document\n\n**Project:** viral-autopilot  \n**Version:** v0.1 | **Date:** 2026-06-17  \n**BoK Applied:** SWEBOK v4 (Software Requirements)  \n**Status:** Draft\n\n---\n\n## 1. Scope Statement\n\nEste documento especifica os requisitos funcionais e n\u00e3o-funcionais do `viral-autopilot`. Deriva do PRD `03-prd.md` e alimenta o SDD `05-sdd.md`.\n\n**In scope (MVP+v1.0):** entidade de plano de cad\u00eancia; cron de disparo recorrente por-tenant; gera\u00e7\u00e3o product-aware monetizada em todo formato (texto+imagem); coletor de desempenho unificado (cliques+org\u00e2nico+receita); analisador de ciclo + reinje\u00e7\u00e3o de aprendizado; guarda de custo (teto + kill-switch); dashboard de ROI por criativo; sele\u00e7\u00e3o de produto por comiss\u00e3o+trend; \u00e2ngulo informado por trends.\n\n**Out of scope (Fase 2 / Won't):** gera\u00e7\u00e3o de v\u00eddeo 9:16; publica\u00e7\u00e3o em TikTok/Instagram/YouTube; gest\u00e3o de an\u00fancios pagos; atribui\u00e7\u00e3o multi-touch cross-network; auto-descoberta de cat\u00e1logo (CLI manual permanece at\u00e9 PR-VA-022).\n\n---\n\n## 2. Functional Requirements\n\n> Category: `UI` | `Hook` | `EdgeFunction` | `DB` | `Cron` | `Lib`\n\n| ID | Title | Description | Priority | PR Traced | Category | Test ID |\n|----|-------|-------------|----------|-----------|----------|---------|\n| FR-VA-001 | Autopilot plan entity | Tabela `autopilot_plans` (per-user RLS): mode (`all_at_once`\\|`every_n_days`), interval_days (default 3), target_product_ids[], platforms[], budget_cap_mco, is_active, next_run_at. CRUD via hook. | Critical | PR-VA-001 | DB | AT-VA-001 |\n| FR-VA-002 | Cycle dispatcher | Edge fn `autopilot-run` (JWT): valida plano, aplica gate de custo (FR-VA-007), seleciona produto(s), abre `autopilot_cycles`, e faz fan-out product-aware para `orchestrate-content` (1 dispatch por produto\u00d7rede). Reusa o padr\u00e3o de `campaign-run`. | Critical | PR-VA-002, PR-VA-001 | EdgeFunction | AT-VA-002 |\n| FR-VA-003 | Product-aware generation | Em `orchestrate-step`, o prompt recebe o produto-alvo (id+nome+imagem+pre\u00e7o+comiss\u00e3o) e usa framework de gancho viral de consumo (hook/valor/CTA) \u2014 substitui os system prompts B2B hardcoded (`:138`,`:290`). | Critical | PR-VA-002 | Lib/EdgeFunction | AT-VA-003 |\n| FR-VA-004 | Monetize all formats | `monetizeContent` (`_shared/affiliate.ts`) roda em artigo **+ LinkedIn + Twitter**, embutindo link ML per-user com `content_variant_id` por criativo (n\u00e3o s\u00f3 no artigo, n\u00e3o por regex de 3 SKUs). | Critical | PR-VA-002 | Lib | AT-VA-004 |\n| FR-VA-005 | Cadence cron | pg_cron `autopilot-cadence` (*/15) \u2192 fn `autopilot-cadence-cron` (service-role): encontra planos `is_active AND next_run_at <= now`, dispara `autopilot-run`, e re-agenda `next_run_at = now + interval_days` (auto-refill, ao contr\u00e1rio do drip finito do nurture). | Critical | PR-VA-003 | Cron | AT-VA-005 |\n| FR-VA-006 | Cycle ledger | Tabela `autopilot_cycles`: plan_id, cycle_number, status (`running`\\|`completed`\\|`aborted_budget`\\|`failed`), spend_mco, planned_units, analysis_node_id, started_at, completed_at. Idempot\u00eancia por (plan_id, cycle_number). | Critical | PR-VA-003, PR-VA-006 | DB | AT-VA-006 |\n| FR-VA-007 | Cost guardrail (kill-switch) | ANTES de qualquer `deduct_mco_coins`: soma custo projetado (10 + 5 + img \u00d7 n\u00ba criativos). Se `> budget_cap_mco` OU `saldo < min_balance` \u2192 aborta ciclo (`aborted_budget`), pausa o plano, notifica. Espelha caps do `vision-mcp`. | Critical | PR-VA-006 | EdgeFunction | AT-VA-007 |\n| FR-VA-008 | Engagement collector | Cron `autopilot-collect` \u2192 fn que, dado o `post_id` retornado por `publish-social`/`publish-meta`, busca insights reais (best-effort por API tier) e grava em `creative_metrics`. | High | PR-VA-004 | Cron/EdgeFunction | AT-VA-008 |\n| FR-VA-009 | Unified creative metrics | Tabela `creative_metrics` keyed por `content_variant_id`: affiliate_clicks, impressions, engagements, revenue_cents, source, collected_at. Unifica os 3 sinais (Decis\u00e3o 3). | High | PR-VA-004 | DB | AT-VA-009 |\n| FR-VA-010 | Cycle analyzer | Edge fn `autopilot-analyze` (service-role, 5 mco): l\u00ea `creative_metrics` do ciclo anterior do tenant; se vazio, usa baseline (N\u00c3O inventa); produz `optimization_policy` estruturado (top hook/produto/hor\u00e1rio/formato). Generaliza `self-optimize`, agora agendado. | High | PR-VA-005 | EdgeFunction | AT-VA-010 |\n| FR-VA-011 | Feedback injection | A gera\u00e7\u00e3o (`orchestrate-step`/`autopilot-run`) L\u00ca o `optimization_policy` mais recente do tenant e injeta as features no system prompt do pr\u00f3ximo ciclo. Fecha a quebra \"sa\u00edda sem consumo\". | Critical | PR-VA-005 | Lib/EdgeFunction | AT-VA-011 |\n| FR-VA-012 | Product selection by score | Sele\u00e7\u00e3o do produto-alvo do `vm_affiliate_products` por `commission_value`+`trend_score`+`profitability_score` (auto em v1.0). No MVP: 3 SKUs semente referenciados no plano. | High | PR-VA-010, PR-VA-001 | EdgeFunction | AT-VA-012 |\n| FR-VA-013 | Image creative (product-referenced) | Plugar `generate-image` (hoje \u00f3rf\u00e3) ao ciclo: usa `image_url` do produto ML como refer\u00eancia; formato por plataforma (quadrado MVP; 9:16 fase 2). Anexa asset a `scheduled_posts`. | Should (MVP) | PR-VA-008 | EdgeFunction | AT-VA-013 |\n| FR-VA-014 | Autopilot hook | `useAutopilot` (TanStack Query): CRUD de plano, status de ciclos, ROI por criativo. Toda l\u00f3gica de dados no hook (Harness Engineering). | High | PR-VA-001, PR-VA-007 | Hook | AT-VA-014 |\n| FR-VA-015 | Autopilot dashboard | `AutopilotPage` (display-only): editor de plano, timeline de ciclos, cards de criativo com ROI, criativo \"vencedor\", insight de lift ciclo-a-ciclo. | High | PR-VA-007 | UI | AT-VA-015 |\n| FR-VA-016 | Honor product/affiliate param | `orchestrate-content` passa a desestruturar e honrar o produto-alvo/`affiliate_url` (hoje dropado em `:79`), propagando ao `orchestrate-step`. | Medium | PR-VA-002 | EdgeFunction | AT-VA-016 |\n| FR-VA-017 | Revenue attribution per creative | `handle-ml-postback` credita `revenue_cents` na `affiliate_links` correta e o coletor (FR-VA-008) reflete em `creative_metrics` por `content_variant_id`. Depende de OTD-VA-007. | High | PR-VA-007 | EdgeFunction | AT-VA-017 |\n| FR-VA-018 | Trend-informed angle | `autopilot-run` l\u00ea `vm_trends` (de `fetch-trends`) para pautar o \u00e2ngulo viral do ciclo (reconecta a ilha de trends). | Should (v1.0) | PR-VA-011 | EdgeFunction | AT-VA-018 |\n\n---\n\n## 3. Non-Functional Requirements\n\n| ID | Category | Requirement | Target | Measurement |\n|----|----------|-------------|--------|-------------|\n| NFR-VA-001 | Performance | Dispatch do ciclo (fan-out) p95 | < 5min para N \u2264 8 criativos | Supabase logs + `autopilot_cycles.completed_at \u2212 started_at` |\n| NFR-VA-002 | Cost-safety | Gate de teto aplicado ANTES de qualquer deduct mcoCoins | 100% dos ciclos (zero deduct em ciclo abortado) | Smoke zero-cost; saldo intacto p\u00f3s-abort |\n| NFR-VA-003 | Idempotency | Re-fire do cron sobre o mesmo ciclo n\u00e3o dobra cobran\u00e7a nem post | 0 duplicatas | Idempot\u00eancia por (plan_id, cycle_number); guarda em `scheduled_posts` |\n| NFR-VA-004 | Tenancy | Toda credencial externa resolvida per-user (`auth.uid()`); zero chave global em path user-facing | 100% | Code review + grep de `Deno.env` em fluxo user-facing |\n| NFR-VA-005 | Security | Edge fns user-facing exigem JWT; crons usam service-role; RLS default-deny em toda tabela | 100% | `/security-review` |\n| NFR-VA-006 | Availability/Self-heal | Cron reconcilia janelas perdidas (catch-up) sem disparar ciclos duplicados | recupera em \u2264 1 tick (15min) | Teste de janela perdida |\n| NFR-VA-007 | Auditability | Todo post aut\u00f4nomo rastre\u00e1vel a `cycle_id`+`plan_id`+`product`+`content_variant_id` | 100% | SELECT join `scheduled_posts`\u2194`autopilot_cycles` |\n| NFR-VA-008 | Brand-safety | Cyber-Sentinel no t\u00f3pico e no conte\u00fado gerado antes de publicar; disclosure de afiliado | 100% dos criativos | Gate pr\u00e9-publica\u00e7\u00e3o + revis\u00e3o |\n\n---\n\n## 4. Interface Requirements\n\n### 4.1 UI \u2192 Hook \u2192 Edge Function Contract\n\n```\n[Component: AutopilotPage.tsx]\n  \u2193 calls\n[Hook: useAutopilot.ts]   (CRUD plano \u00b7 status ciclos \u00b7 ROI por criativo)\n  \u2193 calls (sensitive ops)\n[Edge Function: autopilot-run]   (gate custo \u2192 sele\u00e7\u00e3o produto \u2192 fan-out)\n  \u2193 dispatch (forward JWT, self-bill)\n[Edge Function: orchestrate-content \u2192 orchestrate-step]   (gera\u00e7\u00e3o product-aware + monetize)\n  \u2193 reads/writes\n[Tables: autopilot_plans \u00b7 autopilot_cycles \u00b7 creative_metrics \u00b7 scheduled_posts \u00b7 affiliate_links]\n```\n\n### 4.2 External API Contracts\n\n#### `POST /functions/v1/autopilot-run`\n\n**Auth:** Bearer JWT (user scope) \u2014 OU service-role quando chamado pelo cron (`X-Cron-Trigger`).  \n**Request:**\n```typescript\n{\n  plan_id: string,          // uuid do autopilot_plans (RLS-own)\n  mode_override?: \"all_at_once\" | \"every_n_days\",  // opcional; default = plano\n  dry_run?: boolean,        // se true, retorna custo projetado SEM deduzir nem publicar\n}\n```\n**Response (200):**\n```typescript\n{\n  status: \"ok\",\n  cycle_id: string,\n  cycle_number: number,\n  projected_cost_mco: number,\n  dispatched: { product_id: string, platform: string, run_id: string }[],\n}\n```\n**Error codes:**\n| Code | Condition |\n|------|-----------|\n| 401 | JWT ausente/inv\u00e1lido |\n| 402 | Saldo de mcoCoins insuficiente (`insufficient_balance`) |\n| 409 | Teto de custo do ciclo excedido (`aborted_budget`) \u2014 plano pausado |\n| 422 | Valida\u00e7\u00e3o: plano sem produtos/redes, `interval_days` inv\u00e1lido (campo+mensagem PT-BR) |\n| 500 | Erro interno (logado em `infra_health_logs`) |\n\n#### `POST /functions/v1/autopilot-analyze`\n\n**Auth:** service-role (chamado p\u00f3s-ciclo / pelo cron).  \n**Request:** `{ tenant_id: string, plan_id: string, previous_cycle_id: string }`  \n**Response (200):** `{ status: \"ok\", optimization_policy_id: string, has_real_data: boolean, top_features: {...} }`  \n> `has_real_data=false` quando `creative_metrics` do ciclo anterior est\u00e1 vazia \u2192 usa baseline, N\u00c3O inventa.\n\n---\n\n## 5. Data Requirements\n\n| Field | Type | Nullable | Validation Rule | Error Message (PT-BR) |\n|-------|------|----------|-----------------|----------------------|\n| `autopilot_plans.mode` | `text` | NOT NULL | \u2208 {`all_at_once`,`every_n_days`} | \"Modo de cad\u00eancia inv\u00e1lido.\" |\n| `autopilot_plans.interval_days` | `int` | NULL (req. se `every_n_days`) | 1 \u2264 n \u2264 30; default 3 | \"Intervalo deve ser entre 1 e 30 dias.\" |\n| `autopilot_plans.target_product_ids` | `text[]` | NOT NULL | tamanho \u2265 1; ids \u2208 `vm_affiliate_products` | \"Selecione ao menos um produto-alvo.\" |\n| `autopilot_plans.platforms` | `text[]` | NOT NULL | \u2286 {`wordpress`,`linkedin`,`twitter`} (MVP) | \"Selecione ao menos uma rede suportada.\" |\n| `autopilot_plans.budget_cap_mco` | `int` | NOT NULL | \u2265 custo m\u00ednimo de 1 criativo | \"Teto de custo abaixo do m\u00ednimo de um ciclo.\" |\n| `creative_metrics.content_variant_id` | `uuid` | NOT NULL | FK \u2192 criativo/`content_library` | \u2014 |\n| `creative_metrics.source` | `text` | NOT NULL | \u2208 {`affiliate_click`,`organic`,`postback`} | \u2014 |\n| `creative_metrics.revenue_cents` | `int` | NOT NULL DEFAULT 0 | \u2265 0 | \u2014 |\n\n---\n\n## 6. Test Strategy Matrix\n\n| FR ID | Unit Test | Integration Test | E2E Test | Notes |\n|-------|-----------|-----------------|----------|-------|\n| FR-VA-001 | \u2705 | \u2705 | \u2014 | RLS own-row; valida\u00e7\u00e3o de campos |\n| FR-VA-002 | \u2705 | \u2705 | \u2705 | fan-out + forward JWT (smoke zero-cost com `dry_run`) |\n| FR-VA-003 | \u2705 | \u2705 | \u2014 | prompt cont\u00e9m produto + framework viral |\n| FR-VA-004 | \u2705 | \u2705 | \u2705 | link ML + `content_variant_id` em TODO formato |\n| FR-VA-005 | \u2705 | \u2705 | \u2014 | auto-refill `next_run_at`; janela perdida (catch-up) |\n| FR-VA-006 | \u2705 | \u2705 | \u2014 | idempot\u00eancia (plan_id, cycle_number) |\n| FR-VA-007 | \u2705 | \u2705 | \u2705 | **kill-switch smoke zero-cost** (saldo intacto p\u00f3s-abort) |\n| FR-VA-008 | \u2705 | \u2705 | \u2014 | coletor best-effort por tier; cliques sempre |\n| FR-VA-009 | \u2705 | \u2014 | \u2014 | unicidade por `content_variant_id`+`source` |\n| FR-VA-010 | \u2705 | \u2705 | \u2014 | baseline quando vazio (`has_real_data=false`) |\n| FR-VA-011 | \u2705 | \u2705 | \u2705 | prova de reinje\u00e7\u00e3o: prompt ciclo N+1 cont\u00e9m features do ciclo N |\n| FR-VA-012 | \u2705 | \u2705 | \u2014 | ranking comiss\u00e3o+trend |\n| FR-VA-013 | \u2705 | \u2705 | \u2014 | imagem product-referenced anexada a `scheduled_posts` |\n| FR-VA-014 | \u2705 | \u2014 | \u2014 | hook CRUD + queries |\n| FR-VA-015 | \u2014 | \u2014 | \u2705 | E2E UI 1920\u00d71080 (gate Canvas/UI) |\n| FR-VA-016 | \u2705 | \u2705 | \u2014 | param honrado (regress\u00e3o do drop em `:79`) |\n| FR-VA-017 | \u2705 | \u2705 | \u2014 | atribui\u00e7\u00e3o por `content_variant_id` (gated em OTD-VA-007) |\n| FR-VA-018 | \u2705 | \u2705 | \u2014 | \u00e2ngulo l\u00ea `vm_trends` |\n\n**Test files location:**\n- Unit: `src/hooks/__tests__/useAutopilot.test.ts`\n- Integration / smokes: `scripts/qa/smoke-autopilot-run.ts`, `scripts/qa/smoke-autopilot-budget.ts` (zero-cost)\n- E2E: `e2e/viral-autopilot.spec.ts` + gate `/e2e-audit` 1920\u00d71080 para `AutopilotPage`\n\n---\n\n## 7. Traceability Matrix\n\n| PR ID | FR ID | NFR ID |\n|-------|-------|--------|\n| PR-VA-001 | FR-VA-001, FR-VA-014, FR-VA-016 | NFR-VA-004, NFR-VA-005 |\n| PR-VA-002 | FR-VA-002, FR-VA-003, FR-VA-004, FR-VA-016 | NFR-VA-001, NFR-VA-008 |\n| PR-VA-003 | FR-VA-005, FR-VA-006 | NFR-VA-003, NFR-VA-006 |\n| PR-VA-004 | FR-VA-008, FR-VA-009, FR-VA-017 | NFR-VA-007 |\n| PR-VA-005 | FR-VA-010, FR-VA-011 | NFR-VA-007 |\n| PR-VA-006 | FR-VA-007 | NFR-VA-002 |\n| PR-VA-007 | FR-VA-014, FR-VA-015, FR-VA-017 | NFR-VA-007 |\n| PR-VA-008 | FR-VA-013 | NFR-VA-008 |\n| PR-VA-010 | FR-VA-012 | \u2014 |\n| PR-VA-011 | FR-VA-018 | \u2014 |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:03:03)*


## 🤖 Claude *(21:03:04)*

FRD selado (18 FR + 8 NFR). Agora o **SDD** (SWEBOK + CISSP — arquitetura, STRIDE, RLS, migration stubs, 7 OTDs):

## 🤖 Claude *(21:04:38)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md",
  "content": "# SDD \u2014 System Design Document\n\n**Project:** viral-autopilot  \n**Version:** v0.1 | **Date:** 2026-06-17  \n**BoK Applied:** SWEBOK v4 (Software Design) + CISSP CBK 2024 (Software Development Security)  \n**Status:** Draft\n\n---\n\n## 1. Architecture Overview\n\nO `viral-autopilot` \u00e9 o **orquestrador de ciclo** que costura pe\u00e7as j\u00e1 existentes do MCORCH num loop fechado. N\u00e3o reinventa gera\u00e7\u00e3o nem receita \u2014 adiciona a cabe\u00e7a que planeja, dispara, mede e aprende.\n\n```\n\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n\u2502  PRESENTATION LAYER (display-only)                            \u2502\n\u2502  src/pages/AutopilotPage.tsx                                  \u2502\n\u2502  src/components/autopilot/{PlanEditor,CycleTimeline,RoiCard}  \u2502\n\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n                        \u2502 calls\n\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25bc\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n\u2502  LOGIC LAYER (Harness Engineering)                            \u2502\n\u2502  src/hooks/useAutopilot.ts  (TanStack Query \u2014 plano/ciclo/ROI)\u2502\n\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n                        \u2502 HTTP + JWT\n\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25bc\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n\u2502  EDGE LAYER (Deno / Supabase Functions)                       \u2502\n\u2502  autopilot-run \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510   autopilot-analyze (5 mco)     \u2502\n\u2502  autopilot-cadence-cron \u25c0\u2500\u2500\u2500\u2524   autopilot-collect             \u2502\n\u2502  (service-role, pg_cron)    \u2502                                 \u2502\n\u2502      \u2502 fan-out (forward JWT) \u2502 reuse                          \u2502\n\u2502      \u25bc                       \u25bc                                 \u2502\n\u2502  orchestrate-content \u2192 orchestrate-step (product-aware gen)   \u2502\n\u2502  _shared/affiliate.ts (monetize ALL formats)                  \u2502\n\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n           \u2502 Supabase RLS                  \u2502 External APIs\n\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25bc\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510  \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25bc\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n\u2502  DB LAYER                  \u2502  \u2502  EXTERNAL SERVICES              \u2502\n\u2502  autopilot_plans (new)     \u2502  \u2502  OpenRouter/Groq (LLM, BYOK)    \u2502\n\u2502  autopilot_cycles (new)    \u2502  \u2502  DALL\u00b7E/Nano Banana (image)     \u2502\n\u2502  creative_metrics (new)    \u2502  \u2502  LinkedIn/X/WordPress (publish) \u2502\n\u2502  scheduled_posts (reuse)   \u2502  \u2502  Mercado Livre/Pago (postback)  \u2502\n\u2502  affiliate_links (reuse)   \u2502  \u2502  Apify (fetch-trends, v1.0)     \u2502\n\u2502  optimization_policy(reuse)\u2502  \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n\u2502  vm_affiliate_products     \u2502\n\u2502  mcorch_nodes/_edges       \u2502\n\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n```\n\n---\n\n## 2. Component Catalog\n\n### 2.1 New Custom Hooks (`src/hooks/`)\n\n| Hook | File | Responsibility | TanStack Query keys |\n|------|------|---------------|---------------------|\n| `useAutopilot` | `useAutopilot.ts` | CRUD de `autopilot_plans`; lista ciclos; ROI por criativo; activate/pause | `['autopilot-plans']`, `['autopilot-cycles', planId]`, `['creative-metrics', cycleId]` |\n\n### 2.2 New Display Components (`src/components/autopilot/`)\n\n| Component | File | Props | Hook consumed |\n|-----------|------|-------|--------------|\n| `AutopilotPage` | `src/pages/AutopilotPage.tsx` | \u2014 (route) | `useAutopilot` |\n| `PlanEditor` | `src/components/autopilot/PlanEditor.tsx` | `plan?, onSave` | `useAutopilot` |\n| `CycleTimeline` | `src/components/autopilot/CycleTimeline.tsx` | `planId` | `useAutopilot` |\n| `RoiCard` | `src/components/autopilot/RoiCard.tsx` | `creativeMetric` | \u2014 (display) |\n\n### 2.3 New Edge Functions (`supabase/functions/`)\n\n| Function | Path | Auth | mcoCoins | Secrets needed |\n|----------|------|------|----------|----------------|\n| `autopilot-run` | `supabase/functions/autopilot-run/index.ts` | JWT (user) OR service-role (cron) | gate s\u00f3; deduct ocorre nos sub-runs | \u2014 (resolve per-user) |\n| `autopilot-cadence-cron` | `supabase/functions/autopilot-cadence-cron/index.ts` | service-role (`verify_jwt=false`, pg_net) | 0 | `SB_SECRET_KEY` (service) |\n| `autopilot-analyze` | `supabase/functions/autopilot-analyze/index.ts` | service-role | 5 mco (an\u00e1lise) | LLM key (per-user\u2192sistema fallback) |\n| `autopilot-collect` | `supabase/functions/autopilot-collect/index.ts` | service-role (cron) | 0 | social/meta tokens per-user |\n\n> **Reuso (modificadas, n\u00e3o novas):** `orchestrate-content` (FR-VA-016 honra produto), `orchestrate-step` (FR-VA-003 product-aware + FR-VA-011 feedback inject), `_shared/affiliate.ts` (FR-VA-004 monetiza todo formato), `generate-image` (FR-VA-013 plugado ao ciclo).\n\n### 2.4 Zustand Store Slices (if applicable)\n\n| Slice | Store file | State shape | Actions |\n|-------|------------|-------------|---------|\n| \u2014 | \u2014 | Nenhum store novo; estado de servidor via TanStack Query (Harness). UI local m\u00ednima no editor. | \u2014 |\n\n### 2.5 New DB Objects\n\n| Object | Type | Purpose | Migration file |\n|--------|------|---------|---------------|\n| `autopilot_plans` | Table | Config de cad\u00eancia per-user (FR-VA-001) | `<ts>_viral_autopilot_plans.sql` |\n| `autopilot_cycles` | Table | Ledger de ciclo + spend + status (FR-VA-006) | `<ts>_viral_autopilot_cycles.sql` |\n| `creative_metrics` | Table | M\u00e9tricas unificadas por criativo (FR-VA-009) | `<ts>_viral_autopilot_creative_metrics.sql` |\n| `scheduled_posts.cycle_id` | Column | Liga post ao ciclo (NFR-VA-007 auditabilidade) | `<ts>_scheduled_posts_cycle_id.sql` |\n| `autopilot-cadence` | pg_cron | Disparo recorrente */15 (FR-VA-005) | dentro da migration de cron |\n| `autopilot-collect` | pg_cron | Coleta de m\u00e9tricas (FR-VA-008) | dentro da migration de cron |\n\n---\n\n## 3. Data Flow Diagrams\n\n### Use Case: Ciclo aut\u00f4nomo a cada N dias (FR-VA-005 \u2192 FR-VA-011)\n\n```\npg_cron        cadence-cron        autopilot-run        orchestrate-*        DB / External\n \u2502 (*/15)          \u2502                    \u2502                    \u2502                   \u2502\n \u2502\u2500\u2500[tick]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502                    \u2502                    \u2502                   \u2502\n \u2502                 \u2502\u2500\u2500[plans due?]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 SELECT is_active AND next_run_at<=now\n \u2502                 \u2502\u25c0\u2500\u2500[plan X]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502\n \u2502                 \u2502\u2500\u2500[POST X-Cron]\u2500\u2500\u2500\u2500\u25b6\u2502                    \u2502                   \u2502\n \u2502                 \u2502                    \u2502\u2500\u2500[cost gate]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 project cost vs budget_cap + balance\n \u2502                 \u2502                    \u2502  (abort if over \u2192 aborted_budget, pause)\u2502\n \u2502                 \u2502                    \u2502\u2500\u2500[read policy]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 optimization_policy (ciclo N-1)\n \u2502                 \u2502                    \u2502\u2500\u2500[select product]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 vm_affiliate_products (comm+trend)\n \u2502                 \u2502                    \u2502\u2500\u2500[open cycle]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 autopilot_cycles (running)\n \u2502                 \u2502                    \u2502\u2500\u2500[fan-out/product\u00d7rede]\u2500\u25b6\u2502              \u2502\n \u2502                 \u2502                    \u2502                    \u2502\u2500\u2500[gen product-aware + feedback]\u2500\u25b6 LLM (BYOK)\n \u2502                 \u2502                    \u2502                    \u2502\u2500\u2500[monetize all formats]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6 affiliate_links + content_variant_id\n \u2502                 \u2502                    \u2502                    \u2502\u2500\u2500[schedule]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6 scheduled_posts (cycle_id)\n \u2502                 \u2502\u25c0\u2500\u2500[re-arm next_run_at = now + interval]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502\n \u2502                 \u2502                    \u2502                    \u2502   (auto-publish cron drains scheduled_posts \u2192 publish-*)\n \u2502                 \u2502 (later) autopilot-collect: post_id \u2192 insights \u2192 creative_metrics\n \u2502                 \u2502 (post-cycle) autopilot-analyze: creative_metrics(N) \u2192 optimization_policy(N) [feeds cycle N+1]\n```\n\n---\n\n## 4. API Contract Definitions\n\n> Toda Edge Function user-facing valida JWT antes de qualquer l\u00f3gica. Crons usam service-role com `verify_jwt=false` (padr\u00e3o pg_net do projeto \u2014 ver SOP `orchestrate-async-pipeline`).\n\n### `POST /functions/v1/autopilot-run`\n\n```typescript\n// Request\ninterface AutopilotRunRequest {\n  plan_id: string\n  mode_override?: 'all_at_once' | 'every_n_days'\n  dry_run?: boolean   // true \u2192 retorna projected_cost_mco sem deduzir/publicar\n}\n\n// Response (HTTP 200)\ninterface AutopilotRunResponse {\n  status: 'ok'\n  cycle_id: string\n  cycle_number: number\n  projected_cost_mco: number\n  dispatched: { product_id: string; platform: string; run_id: string }[]\n}\n\n// Cost gate (FR-VA-007) \u2014 BEFORE any deduction:\n// \u2192 project = 10 (orchestrate) + 5 (analyze) + IMAGE_COST * creatives\n// \u2192 if project > plan.budget_cap_mco \u2192 409 aborted_budget + pause plan\n// \u2192 balance check via profiles.mco_balance; if < min_balance \u2192 402\n// mcoCoins deduction happens inside each orchestrate-content sub-run (self-bill), never here.\n```\n\n### `POST /functions/v1/autopilot-analyze`\n\n```typescript\ninterface AutopilotAnalyzeRequest { tenant_id: string; plan_id: string; previous_cycle_id: string }\ninterface AutopilotAnalyzeResponse {\n  status: 'ok'\n  optimization_policy_id: string\n  has_real_data: boolean        // false \u2192 baseline used, N\u00c3O fabrica recomenda\u00e7\u00e3o\n  top_features: { hook?: string; product_id?: string; best_hour?: number; format?: string }\n}\n// Deduct 5 mco (deduct_mco_coins) only when has_real_data OR explicitly configured; logged.\n```\n\n---\n\n## 5. Security Design\n\n### 5.1 Threat Model (STRIDE)\n\n| Component | Threat | Type | Severity | Mitigation |\n|-----------|--------|------|----------|------------|\n| `autopilot-run` | Acesso n\u00e3o autenticado / disparo por terceiro | Spoofing | High | JWT no path user; `X-Cron-Trigger` + service-role no path cron; valida `plan.user_id = auth.uid()` |\n| `autopilot-cadence-cron` | Falsifica\u00e7\u00e3o de trigger de cron (disparo for\u00e7ado) | Spoofing/Elevation | High | `verify_jwt=false` + service-role key; sem path p\u00fablico que dispare ciclo arbitr\u00e1rio; rate por plano via `next_run_at` |\n| `autopilot_plans`/`_cycles`/`creative_metrics` | Leitura/escrita cross-tenant | Information Disclosure | Critical | RLS `user_id = auth.uid()`; crons usam service-role com filtro expl\u00edcito por tenant |\n| Cost gate | Bypass do teto (disparo paralelo p/ exceder) | Tampering | Critical | Gate at\u00f4mico server-side ANTES do deduct; idempot\u00eancia (plan_id, cycle_number); lock otimista no ciclo |\n| Gerador product-aware | Prompt injection via nome/desc de produto ou trend | Tampering/Elevation | High | Cyber-Sentinel no input + no output; sanitiza\u00e7\u00e3o do produto antes do prompt |\n| `affiliate_links` | Inje\u00e7\u00e3o de link malicioso / open-redirect | Tampering | High | Guarda de dom\u00ednio ML j\u00e1 existente em `process-affiliate-link`; `content_variant_id` assinado por ciclo |\n| Conte\u00fado aut\u00f4nomo | Publica\u00e7\u00e3o off-brand / viola ToS | Repudiation/Reputation | High | Cyber-Sentinel gate pr\u00e9-publica\u00e7\u00e3o; HITL opcional (PR-VA-013); disclosure de afiliado |\n| `autopilot-collect` | Vazamento de PII de engajamento na tabela global-read | Information Disclosure | Medium | S\u00f3 agregados em `creative_metrics`; sem PII de terceiros; RLS own |\n\n### 5.2 RLS Policy Definitions\n\n```sql\n-- autopilot_plans RLS (espelhar em autopilot_cycles, creative_metrics)\nALTER TABLE public.autopilot_plans ENABLE ROW LEVEL SECURITY;\n\nCREATE POLICY \"autopilot_plans_select_own\"\n  ON public.autopilot_plans FOR SELECT\n  USING (user_id = auth.uid());\n\nCREATE POLICY \"autopilot_plans_insert_own\"\n  ON public.autopilot_plans FOR INSERT\n  WITH CHECK (user_id = auth.uid());\n\nCREATE POLICY \"autopilot_plans_update_own\"\n  ON public.autopilot_plans FOR UPDATE\n  USING (user_id = auth.uid())\n  WITH CHECK (user_id = auth.uid());\n\n-- DELETE bloqueado para authenticated (RESTRICTIVE); s\u00f3 service_role gerencia ciclos/spend.\n```\n\n### 5.3 JWT Validation Points\n\n```typescript\n// autopilot-run (user path):\nconst authHeader = req.headers.get('Authorization')\nif (!authHeader) return new Response('Unauthorized', { status: 401 })\nconst { data: { user }, error } = await supabase.auth.getUser(authHeader.replace('Bearer ', ''))\nif (error || !user) return new Response('Unauthorized', { status: 401 })\n// then: assert plan.user_id === user.id  (cross-tenant guard)\n\n// cron path: header X-Cron-Trigger + SB_SECRET_KEY (service-role client); verify_jwt=false in config.toml\n```\n\n### 5.4 Secrets Inventory\n\n| Secret Name | Used In | Vault Location | Rotation Policy |\n|-------------|---------|----------------|----------------|\n| `SB_SECRET_KEY` | crons (service-role) | Supabase Vault | per incident (legada `SUPABASE_SERVICE_ROLE_KEY` REVOGADA) |\n| LLM key (Groq/OpenRouter/Gemini) | `orchestrate-step`, `autopilot-analyze` | `user_api_keys` (per-user) \u2192 vault fallback | per-user controlado |\n| ML `affiliate_tag`/`matt_tool` | `_shared/affiliate.ts`, `process-affiliate-link` | `affiliate_config` (per-user) | per-user |\n| Social tokens (LinkedIn/X/Meta) | `publish-*`, `autopilot-collect` | `social_credentials`/`meta_config` (per-user) | OAuth refresh |\n| `MP_WEBHOOK_SECRET` | `handle-ml-postback` | Vault (global hoje \u2192 per-user em OTD-VA-007) | OTD-ML-MP-PER-USER |\n\n> \u26a0\ufe0f NUNCA commitar valores de segredo. S\u00f3 nomes de chave aparecem na documenta\u00e7\u00e3o. Usar `SB_SECRET_KEY` (legada revogada \u2014 ver `reference_supabase_keys_migrated`).\n\n---\n\n## 6. Infrastructure Touchpoints\n\n| Infrastructure | Usage | Impact |\n|----------------|-------|--------|\n| `pg_cron` | 2 novos jobs (`autopilot-cadence` */15, `autopilot-collect`) | Soma a `memory_decay_fsrs` + `nurture-advance`; preservar os existentes |\n| `mega-brain-daemon` | Consome eventos `viral_autopilot_*` de `infra_health_logs` p/ self-heal | Watchdog telemetry |\n| `infra_health_logs` | Novos `event`: `viral_autopilot_cycle_started/completed/aborted_budget/collect_failure/analyze_empty` | Telemetria allowlist (n\u00e3o vazar per-tenant na tabela global-read) |\n| `mcorch_nodes`/`_edges` | Observation node por ciclo + edge `OPTIMIZES_FROM` (ciclo N+1 \u2192 N) | GraphRAG mem\u00f3ria de campanhas |\n| ChromaDB (`mcorch_chroma`) | N\u00e3o usado diretamente nesta fase | \u2014 |\n\n---\n\n## 7. Migration Stubs\n\n```sql\n-- Migration: <ts>_viral_autopilot_plans.sql\nCREATE TABLE public.autopilot_plans (\n  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,\n  user_id         uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,\n  project_id      uuid,                                  -- tenant scope opcional\n  name            text NOT NULL,\n  mode            text NOT NULL CHECK (mode IN ('all_at_once','every_n_days')),\n  interval_days   int CHECK (interval_days BETWEEN 1 AND 30),  -- req. se every_n_days\n  target_product_ids text[] NOT NULL CHECK (cardinality(target_product_ids) >= 1),\n  platforms       text[] NOT NULL CHECK (cardinality(platforms) >= 1),\n  budget_cap_mco  int NOT NULL CHECK (budget_cap_mco > 0),\n  min_balance_mco int NOT NULL DEFAULT 10,\n  is_active       boolean NOT NULL DEFAULT false,\n  next_run_at     timestamptz,\n  created_at      timestamptz NOT NULL DEFAULT now(),\n  updated_at      timestamptz NOT NULL DEFAULT now()\n);\nALTER TABLE public.autopilot_plans ENABLE ROW LEVEL SECURITY;\n-- (RLS policies from \u00a75.2)\nCREATE INDEX autopilot_plans_user_idx ON public.autopilot_plans (user_id);\nCREATE INDEX autopilot_plans_due_idx  ON public.autopilot_plans (next_run_at) WHERE is_active;\n\n-- Migration: <ts>_viral_autopilot_cycles.sql\nCREATE TABLE public.autopilot_cycles (\n  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,\n  plan_id         uuid REFERENCES public.autopilot_plans(id) ON DELETE CASCADE NOT NULL,\n  user_id         uuid NOT NULL,                         -- denormalized for RLS\n  cycle_number    int NOT NULL,\n  status          text NOT NULL DEFAULT 'running'\n                    CHECK (status IN ('running','completed','aborted_budget','failed')),\n  spend_mco       int NOT NULL DEFAULT 0,\n  planned_units   int NOT NULL DEFAULT 0,\n  analysis_node_id uuid,                                 -- mcorch_nodes observation\n  started_at      timestamptz NOT NULL DEFAULT now(),\n  completed_at    timestamptz,\n  UNIQUE (plan_id, cycle_number)                         -- idempot\u00eancia (NFR-VA-003)\n);\nALTER TABLE public.autopilot_cycles ENABLE ROW LEVEL SECURITY;\n-- SELECT own; INSERT/UPDATE service-role only.\n\n-- Migration: <ts>_viral_autopilot_creative_metrics.sql\nCREATE TABLE public.creative_metrics (\n  id                 uuid DEFAULT gen_random_uuid() PRIMARY KEY,\n  user_id            uuid NOT NULL,\n  cycle_id           uuid REFERENCES public.autopilot_cycles(id) ON DELETE CASCADE,\n  content_variant_id uuid NOT NULL,\n  product_id         text,\n  platform           text,\n  source             text NOT NULL CHECK (source IN ('affiliate_click','organic','postback')),\n  impressions        int NOT NULL DEFAULT 0,\n  engagements        int NOT NULL DEFAULT 0,\n  affiliate_clicks   int NOT NULL DEFAULT 0,\n  revenue_cents      int NOT NULL DEFAULT 0,\n  collected_at       timestamptz NOT NULL DEFAULT now(),\n  UNIQUE (content_variant_id, source)                    -- upsert idempotente por fonte\n);\nALTER TABLE public.creative_metrics ENABLE ROW LEVEL SECURITY;\n-- SELECT own; INSERT/UPDATE service-role only (coletor).\n\n-- Migration: <ts>_scheduled_posts_cycle_id.sql\nALTER TABLE public.scheduled_posts ADD COLUMN IF NOT EXISTS cycle_id uuid\n  REFERENCES public.autopilot_cycles(id) ON DELETE SET NULL;\nCREATE INDEX scheduled_posts_cycle_idx ON public.scheduled_posts (cycle_id);\n```\n\n> Nenhuma tabela aqui carrega `embedding` (n\u00e3o s\u00e3o n\u00f3s de conhecimento diretos). A mem\u00f3ria GraphRAG entra via `mcorch_nodes` observation por ciclo (ver `06-data-model.md` \u00a74). Toda migration passa `/security-review` antes do commit (FMEA-011).\n\n---\n\n## 8. Open Technical Decisions\n\n| ID | Description | Option A | Option B | Recommendation | Owner |\n|----|-------------|----------|----------|----------------|-------|\n| OTD-VA-001 | Tabela de m\u00e9tricas | Estender `campaign_metrics` (campaign-level) | Nova `creative_metrics` (por content_variant_id) | **B** \u2014 granularidade por criativo \u00e9 pr\u00e9-req de R3; ETL agrega p/ campaign_metrics | Sovereign |\n| OTD-VA-002 | Infra de cron | pg_cron (como `nurture-advance`) | OS crontab (como `auto-publish`) | **A** \u2014 pg_cron service-role, consistente com o cron de cad\u00eancia existente | Sovereign |\n| OTD-VA-003 | Fonte de engajamento org\u00e2nico | S\u00f3 cliques de afiliado (sempre dispon\u00edvel) | + insights de API por rede (tier-dependente) | **Ambos faseado** \u2014 cliques no MVP; org\u00e2nico best-effort gated por tier (Twitter Basic, LinkedIn, Meta) | Sovereign |\n| OTD-VA-004 | Unidade do teto de custo | Por ciclo (no plano) | Di\u00e1rio global por tenant | **Ambos** \u2014 cap por ciclo (plano) + safety di\u00e1rio global espelhando `vision-mcp` | Sovereign |\n| OTD-VA-005 | Reinje\u00e7\u00e3o de feedback | Texto cru do `optimization_policy` no prompt | Features estruturadas (top hook/produto/hor\u00e1rio/formato) | **B** \u2014 estruturado mant\u00e9m o prompt enxuto e audit\u00e1vel | Sovereign |\n| OTD-VA-006 | Autonomia de sele\u00e7\u00e3o de produto | Auto-score por comiss\u00e3o+trend | Shortlist curada pelo Sovereign | **Shortlist (3 SKUs) no MVP** (Decis\u00e3o 4); auto-score em v1.0 (PR-VA-010) | Decidido |\n| OTD-VA-007 | Secret de postback per-user (herdada `OTD-ML-MP-PER-USER`) | Manter secret global (Usu\u00e1rio Zero) | Per-user `meta`/MP config | **B antes de multi-tenant** \u2014 atribui\u00e7\u00e3o de receita por tenant exige secret per-user | Sovereign |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:04:40)*


## 🤖 Claude *(21:04:42)*

SDD selado (STRIDE 8 ameaças, 4 fns novas, 7 OTDs). Agora os 3 finais — **data-model**, **process-flow**, **quality-metrics**:

## 🤖 Claude *(21:05:35)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/06-data-model.md",
  "content": "# Data & Knowledge Model\n\n**Project:** viral-autopilot  \n**Version:** v0.1 | **Date:** 2026-06-17  \n**BoK Applied:** DMBOK v2 (Data Modeling & Design + Data Quality)  \n**Status:** Draft\n\n---\n\n## 1. Conceptual Data Model\n\n```\n[autopilot_plans] \u2500\u2500(1:N)\u2500\u2500\u25b6 [autopilot_cycles] \u2500\u2500(1:N)\u2500\u2500\u25b6 [creative_metrics]\n       \u2502                            \u2502                              \u2502\n       \u2502 (references)               \u2502 (cycle_id on)                \u2502 (content_variant_id)\n       \u25bc                            \u25bc                              \u25bc\n[vm_affiliate_products]      [scheduled_posts] \u2500\u2500(N:1)\u2500\u2500\u25b6 [content_library]\n       \u2502                            \u2502                              \u2502\n       \u2514\u2500\u2500(promotes)\u2500\u2500\u25b6 [affiliate_links] \u25c0\u2500\u2500(revenue)\u2500\u2500 [handle-ml-postback]\n                                    \u2502\n                                    \u2514\u2500\u2500(1:1 observation)\u2500\u2500\u25b6 [mcorch_nodes] \u2500\u2500OPTIMIZES_FROM\u2500\u2500\u25b6 [mcorch_nodes]\n```\n\n**Entities:**\n- **autopilot_plans:** configura\u00e7\u00e3o de cad\u00eancia per-user (modo, intervalo, produtos-alvo, redes, teto de custo). Fonte da verdade do \"o qu\u00ea e quando\".\n- **autopilot_cycles:** inst\u00e2ncia de execu\u00e7\u00e3o de um plano (ledger: status, spend, planned_units, ponteiro p/ an\u00e1lise). Idempotente por (plan_id, cycle_number).\n- **creative_metrics:** desempenho por criativo (`content_variant_id`), unificando cliques de afiliado + engajamento org\u00e2nico + receita de postback (Decis\u00e3o 3).\n- **vm_affiliate_products (reuse):** cat\u00e1logo ML com `commission_value`/`trend_score`/`profitability_score`/`image_url` \u2014 fonte do produto-alvo.\n- **scheduled_posts (reuse + `cycle_id`):** fila de publica\u00e7\u00e3o; agora rastre\u00e1vel ao ciclo.\n- **affiliate_links / optimization_policy / content_library / mcorch_nodes (reuse):** receita, pol\u00edtica de melhoria, conte\u00fado, mem\u00f3ria.\n\n---\n\n## 2. Logical Data Model\n\n### Table: `autopilot_plans`\n\n| Column | Type | Nullable | Default | FK | Description |\n|--------|------|----------|---------|-----|------------|\n| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | \u2014 | PK |\n| `user_id` | `uuid` | NOT NULL | \u2014 | `auth.users.id` | Tenant isolation |\n| `project_id` | `uuid` | NULL | \u2014 | \u2014 | Project scope opcional |\n| `name` | `text` | NOT NULL | \u2014 | \u2014 | Nome do plano |\n| `mode` | `text` | NOT NULL | \u2014 | \u2014 | `all_at_once` \\| `every_n_days` |\n| `interval_days` | `int` | NULL | `3` | \u2014 | Req. se `every_n_days`; 1\u201330 |\n| `target_product_ids` | `text[]` | NOT NULL | \u2014 | \u2192 `vm_affiliate_products.external_id` | \u2265 1 produto |\n| `platforms` | `text[]` | NOT NULL | \u2014 | \u2014 | \u2286 {wordpress,linkedin,twitter} (MVP) |\n| `budget_cap_mco` | `int` | NOT NULL | \u2014 | \u2014 | Teto de custo por ciclo |\n| `min_balance_mco` | `int` | NOT NULL | `10` | \u2014 | Piso de saldo p/ disparar |\n| `is_active` | `boolean` | NOT NULL | `false` | \u2014 | Cad\u00eancia ligada |\n| `next_run_at` | `timestamptz` | NULL | \u2014 | \u2014 | Pr\u00f3ximo disparo (cron) |\n| `created_at` | `timestamptz` | NOT NULL | `now()` | \u2014 | Audit |\n| `updated_at` | `timestamptz` | NOT NULL | `now()` | \u2014 | Audit |\n\n### Table: `autopilot_cycles`\n\n| Column | Type | Nullable | Default | FK | Description |\n|--------|------|----------|---------|-----|------------|\n| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | \u2014 | PK |\n| `plan_id` | `uuid` | NOT NULL | \u2014 | `autopilot_plans.id` | Plano pai |\n| `user_id` | `uuid` | NOT NULL | \u2014 | \u2014 | Denormalizado p/ RLS |\n| `cycle_number` | `int` | NOT NULL | \u2014 | \u2014 | Sequencial por plano |\n| `status` | `text` | NOT NULL | `running` | \u2014 | running\\|completed\\|aborted_budget\\|failed |\n| `spend_mco` | `int` | NOT NULL | `0` | \u2014 | mcoCoins gastos no ciclo |\n| `planned_units` | `int` | NOT NULL | `0` | \u2014 | n\u00ba criativos planejados |\n| `analysis_node_id` | `uuid` | NULL | \u2014 | `mcorch_nodes.id` | N\u00f3 de observa\u00e7\u00e3o do ciclo |\n| `started_at` | `timestamptz` | NOT NULL | `now()` | \u2014 | \u2014 |\n| `completed_at` | `timestamptz` | NULL | \u2014 | \u2014 | \u2014 |\n| \u2014 | \u2014 | \u2014 | \u2014 | \u2014 | **UNIQUE (plan_id, cycle_number)** |\n\n### Table: `creative_metrics`\n\n| Column | Type | Nullable | Default | FK | Description |\n|--------|------|----------|---------|-----|------------|\n| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | \u2014 | PK |\n| `user_id` | `uuid` | NOT NULL | \u2014 | \u2014 | Tenant isolation |\n| `cycle_id` | `uuid` | NULL | \u2014 | `autopilot_cycles.id` | Ciclo de origem |\n| `content_variant_id` | `uuid` | NOT NULL | \u2014 | \u2192 criativo/`content_library` | Criativo medido |\n| `product_id` | `text` | NULL | \u2014 | \u2192 `vm_affiliate_products` | Produto promovido |\n| `platform` | `text` | NULL | \u2014 | \u2014 | Rede |\n| `source` | `text` | NOT NULL | \u2014 | \u2014 | affiliate_click\\|organic\\|postback |\n| `impressions` | `int` | NOT NULL | `0` | \u2014 | \u2014 |\n| `engagements` | `int` | NOT NULL | `0` | \u2014 | likes/shares/comments |\n| `affiliate_clicks` | `int` | NOT NULL | `0` | \u2014 | do click ledger |\n| `revenue_cents` | `int` | NOT NULL | `0` | \u2014 | do postback |\n| `collected_at` | `timestamptz` | NOT NULL | `now()` | \u2014 | \u2014 |\n| \u2014 | \u2014 | \u2014 | \u2014 | \u2014 | **UNIQUE (content_variant_id, source)** |\n\n> Nenhuma das 3 tabelas carrega `embedding`/`stability_score` \u2014 n\u00e3o s\u00e3o n\u00f3s de conhecimento diretos. A mem\u00f3ria sem\u00e2ntica entra via `mcorch_nodes` (\u00a74).\n\n---\n\n## 3. Supabase Physical Schema Stubs\n\n```sql\n-- ============================================================\n-- MIGRATION: <ts>_viral_autopilot_schema.sql  (split em 4 arquivos \u2014 ver 05-sdd \u00a77)\n-- ============================================================\n-- autopilot_plans / autopilot_cycles / creative_metrics + ALTER scheduled_posts\n-- (stubs CREATE TABLE completos em 05-sdd.md \u00a77)\n\n-- RLS (default-deny \u2192 own-row)\nALTER TABLE public.autopilot_plans     ENABLE ROW LEVEL SECURITY;\nALTER TABLE public.autopilot_cycles    ENABLE ROW LEVEL SECURITY;\nALTER TABLE public.creative_metrics    ENABLE ROW LEVEL SECURITY;\n\nCREATE POLICY \"autopilot_plans: users read own\"    ON public.autopilot_plans  FOR SELECT USING (user_id = auth.uid());\nCREATE POLICY \"autopilot_plans: users write own\"   ON public.autopilot_plans  FOR INSERT WITH CHECK (user_id = auth.uid());\nCREATE POLICY \"autopilot_plans: users update own\"  ON public.autopilot_plans  FOR UPDATE USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());\n\nCREATE POLICY \"autopilot_cycles: users read own\"   ON public.autopilot_cycles FOR SELECT USING (user_id = auth.uid());\n-- INSERT/UPDATE de cycles e creative_metrics: service_role only (coletor/runner).\nCREATE POLICY \"creative_metrics: users read own\"   ON public.creative_metrics FOR SELECT USING (user_id = auth.uid());\n\n-- \u00cdndices\nCREATE INDEX autopilot_plans_due_idx     ON public.autopilot_plans (next_run_at) WHERE is_active;\nCREATE INDEX autopilot_cycles_plan_idx   ON public.autopilot_cycles (plan_id);\nCREATE INDEX creative_metrics_cycle_idx  ON public.creative_metrics (cycle_id);\nCREATE INDEX creative_metrics_variant_idx ON public.creative_metrics (content_variant_id);\n\n-- Updated-at trigger (reusa update_updated_at_column existente)\nCREATE TRIGGER set_autopilot_plans_updated_at\n  BEFORE UPDATE ON public.autopilot_plans\n  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();\n```\n\n---\n\n## 4. GraphRAG Knowledge Nodes\n\n### Node Types Introduced\n\n| node_type | Title Pattern | Content Fields | Embedding Source |\n|-----------|--------------|----------------|-----------------|\n| `observation` (reuse) | `autopilot-cycle-<plan>-<n>-<date>` | resumo do ciclo: produto, redes, desempenho agregado, pol\u00edtica aplicada | `${title} ${content}` via `embed-mcorch-node` |\n\n> N\u00e3o introduz `node_type` novo \u2014 reusa `observation`. A novidade \u00e9 o **edge** que liga ciclos para a mem\u00f3ria de aprendizado ser naveg\u00e1vel.\n\n### Edge Types Introduced\n\n| Edge relationship | Source node_type | Target node_type | Metadata |\n|-------------------|-----------------|-----------------|----------|\n| `OPTIMIZES_FROM` (new) | `observation` (ciclo N+1) | `observation` (ciclo N) | `{ lift, applied_features }` \u2014 o ciclo N+1 derivou aprendizado do ciclo N |\n| `ATTRIBUTES_REVENUE_TO` (reuse) | `revenue` event | `content_mesh_asset`/criativo | `{ revenue_cents, order_id }` \u2014 atribui\u00e7\u00e3o por criativo |\n| `PROMOTES` (new, optional) | `observation` (ciclo) | product node | `{ product_id, commission_value }` |\n\n### Embedding Trigger\n\n```typescript\n// Ap\u00f3s fechar o ciclo (autopilot-run / autopilot-analyze), insere observation node:\nawait supabase.functions.invoke('embed-mcorch-node', {\n  body: { node_id: cycleNode.id, content: `${title} ${cycleSummary}` }\n})\n// O trigger trg_mcorch_embed_on_insert (pg_net) tamb\u00e9m dispara automaticamente.\n```\n\n### FSRS-6 Parameters\n\n| Field | Initial Value | Decay Rule |\n|-------|--------------|------------|\n| `stability_score` (no `mcorch_nodes` do ciclo) | `0.7` (observa\u00e7\u00e3o operacional relevante) | Decai por `decay_mcorch_stability()` (migration `20260425190000`) |\n| `revenue_impact` (no n\u00f3 do ciclo) | `SUM(creative_metrics.revenue_cents)/100` do ciclo | Atualizado quando postback credita receita atribu\u00edda ao ciclo |\n\n---\n\n## 5. Tenant Isolation Map\n\n| Table | `user_id` scope | `project_id` scope | System rows (user_id IS NULL) |\n|-------|----------------|-------------------|-------------------------------|\n| `autopilot_plans` | \u2705 Required | Optional | No |\n| `autopilot_cycles` | \u2705 Required (denorm) | via plano | No |\n| `creative_metrics` | \u2705 Required | via ciclo | No |\n| `scheduled_posts` (reuse) | \u2705 Required (existente) | \u2014 | No |\n| `vm_affiliate_products` (reuse) | cat\u00e1logo compartilhado (read `USING(true)`) | \u2014 | Sim (shared) |\n| `mcorch_nodes` (reuse) | Optional | Optional | Sim (system nodes) |\n\n---\n\n## 6. Data Quality Rules\n\n| Table | Column | Rule | Violation Message (PT-BR) |\n|-------|--------|------|--------------------------|\n| `autopilot_plans` | `mode` | \u2208 {all_at_once, every_n_days} | \"Modo de cad\u00eancia inv\u00e1lido.\" |\n| `autopilot_plans` | `interval_days` | 1\u201330; obrigat\u00f3rio se `every_n_days` | \"Intervalo deve ser entre 1 e 30 dias.\" |\n| `autopilot_plans` | `target_product_ids` | cardinalidade \u2265 1; ids existem no cat\u00e1logo | \"Selecione ao menos um produto-alvo v\u00e1lido.\" |\n| `autopilot_plans` | `platforms` | \u2286 redes suportadas (MVP); \u2265 1 | \"Selecione ao menos uma rede suportada.\" |\n| `autopilot_plans` | `budget_cap_mco` | \u2265 custo m\u00ednimo de 1 ciclo | \"Teto de custo abaixo do m\u00ednimo de um ciclo.\" |\n| `autopilot_cycles` | `(plan_id, cycle_number)` | UNIQUE (idempot\u00eancia) | \"Ciclo j\u00e1 existente para este plano.\" |\n| `creative_metrics` | `(content_variant_id, source)` | UNIQUE (upsert por fonte) | \u2014 |\n| `creative_metrics` | `revenue_cents`/`affiliate_clicks` | \u2265 0 | \"M\u00e9trica n\u00e3o pode ser negativa.\" |\n\n---\n\n## 7. Retention & Archival Policy\n\n| Data | Retention Period | Archival Strategy | Deletion Trigger |\n|------|-----------------|-------------------|-----------------|\n| `autopilot_plans` | enquanto ativo + 1 ano | nenhum | CASCADE no delete do user (LGPD) |\n| `autopilot_cycles` | 18 meses | sum\u00e1rio agregado em `mcorch_nodes` (observation) | CASCADE no delete do plano |\n| `creative_metrics` | 18 meses | agregado por ciclo preservado no n\u00f3 | CASCADE no delete do ciclo |\n| `mcorch_nodes` (observation de ciclo) | Indefinido (mem\u00f3ria) | FSRS-6 decay de stability | LGPD erase por tenant |\n| `infra_health_logs` (eventos autopilot) | 90 dias | sem archival | Cron purge |\n\n> **LGPD:** o delete do tenant (`auth.users`) cascateia plans\u2192cycles\u2192creative_metrics. M\u00e9tricas guardam s\u00f3 agregados (sem PII de terceiros que engajaram).\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/06-data-model.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:06:33)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/07-process-flow.md",
  "content": "# Process & Automation Blueprint\n\n**Project:** viral-autopilot  \n**Version:** v0.1 | **Date:** 2026-06-17  \n**BoK Applied:** BPM CBOK v4 (Process Modeling + Process Design)  \n**Status:** Draft\n\n---\n\n## 1. Process Inventory\n\n| Process ID | Name | Type | Trigger | Owner | SLA |\n|------------|------|------|---------|-------|-----|\n| PROC-VA-001 | Ciclo aut\u00f4nomo de cad\u00eancia | cron | pg_cron `autopilot-cadence` */15 \u2192 plano due | System | ciclo dispara em \u2264 15min ap\u00f3s `next_run_at` |\n| PROC-VA-002 | Disparo \"tudo de uma vez\" | human-in-loop | Operador clica \"Gerar agora\" na UI | User | resposta < 5min p95 (fan-out) |\n| PROC-VA-003 | Coleta de desempenho | cron | pg_cron `autopilot-collect` (hor\u00e1rio) | System | m\u00e9trica coletada \u2264 24h ap\u00f3s publica\u00e7\u00e3o |\n| PROC-VA-004 | Kill-switch de custo | event-driven | custo projetado > teto OU saldo < piso | System | aborta antes de qualquer deduct |\n| PROC-VA-005 | An\u00e1lise + reinje\u00e7\u00e3o de aprendizado | automated | p\u00f3s-ciclo (encadeado a PROC-VA-001) | System | `optimization_policy` pronto antes do pr\u00f3ximo ciclo |\n\n---\n\n## 2. BPMN-lite Process Maps\n\n### PROC-VA-001: Ciclo aut\u00f4nomo de cad\u00eancia\n\n```\nSTART (cron tick */15)\n   \u2502\n[autopilot-cadence-cron: SELECT plans is_active AND next_run_at<=now]\n   \u2502\n<Gateway: h\u00e1 plano due?>\n   \u2502 NO \u2500\u2500\u25b6 END (no-op)\n   \u2502 YES\n[autopilot-run(plan, X-Cron-Trigger)]\n   \u2502\n[Cost gate: projetar 10 + 5 + img\u00d7criativos]\n   \u2502\n<Gateway: custo \u2264 budget_cap AND saldo \u2265 min_balance?>\n   \u2502 NO \u2500\u2500\u25b6 [status=aborted_budget] \u2500\u2500\u25b6 [pause plan] \u2500\u2500\u25b6 [infra_health_logs: viral_autopilot_aborted_budget] \u2500\u2500\u25b6 [notify PT-BR] \u2500\u2500\u25b6 END\n   \u2502 YES\n[read optimization_policy (ciclo N-1)]  \u2192  [select product (comm+trend / seed)]  \u2192  [open autopilot_cycles (running)]\n   \u2502\n[fan-out por produto\u00d7rede \u2192 orchestrate-content (forward JWT, self-bill)]\n   \u2502\n   \u251c\u2500\u2500[orchestrate-step: gerar product-aware + injetar feedback]\n   \u251c\u2500\u2500[monetize ALL formats \u2192 affiliate_links + content_variant_id]\n   \u251c\u2500\u2500[generate-image product-referenced \u2192 asset]\n   \u2514\u2500\u2500[insert scheduled_posts (cycle_id)]\n   \u2502\n[re-arm: next_run_at = now + interval_days]   (auto-refill)\n   \u2502\n[Insert mcorch_node observation + edge OPTIMIZES_FROM \u2192 ciclo N-1]\n   \u2502\nEND  (auto-publish cron drena scheduled_posts \u2192 publish-*; PROC-VA-003 coleta depois)\n```\n\n**Swimlanes:**\n\n| Swimlane | Participant | Tasks |\n|----------|-------------|-------|\n| Scheduler | pg_cron + `autopilot-cadence-cron` | tick, encontrar planos due, re-armar next_run_at |\n| Edge Function | `autopilot-run` | cost gate, sele\u00e7\u00e3o de produto, abrir ciclo, fan-out |\n| Generation | `orchestrate-content`\u2192`orchestrate-step` + `_shared/affiliate.ts` + `generate-image` | gerar product-aware, monetizar, agendar |\n| External API | LLM (BYOK), DALL\u00b7E/Nano Banana, redes (via auto-publish) | gerar texto/imagem, publicar |\n| DB | Supabase | autopilot_cycles, scheduled_posts, affiliate_links, mcorch_nodes |\n\n---\n\n### PROC-VA-002: Disparo \"tudo de uma vez\" (HITL)\n\n```\n[User Action: clica \"Gerar agora\" (mode=all_at_once)]\n  \u2502\n  \u25bc\n[Hook: useAutopilot \u2192 invoke autopilot-run { plan_id, dry_run:true }]\n  \u2502\n  \u25bc\n[Edge Fn: autopilot-run]\n  \u251c\u2500\u2500 Validate JWT \u2500\u2500(fail)\u2500\u2500\u25b6 HTTP 401\n  \u251c\u2500\u2500 assert plan.user_id == auth.uid() \u2500\u2500(fail)\u2500\u2500\u25b6 HTTP 403\n  \u251c\u2500\u2500 Cost gate (proje\u00e7\u00e3o) \u2500\u2500(over)\u2500\u2500\u25b6 HTTP 409 \u2192 Toast: \"Teto de custo insuficiente para este ciclo\"\n  \u251c\u2500\u2500 return projected_cost_mco  (dry_run)\n  \u2502\n  \u25bc\n[UI mostra custo projetado + confirma\u00e7\u00e3o]\n  \u2502\n  \u25bc (usu\u00e1rio confirma)\n[invoke autopilot-run { plan_id, dry_run:false }]\n  \u251c\u2500\u2500 deduct ocorre nos sub-runs (self-bill via orchestrate-content)\n  \u251c\u2500\u2500 fan-out todos os criativos AGORA (Promise.allSettled)\n  \u251c\u2500\u2500 Embed observation node via embed-mcorch-node\n  \u2514\u2500\u2500 HTTP 200 \u2192 React Query invalida ['autopilot-cycles'] \u2192 UI refresh\n```\n\n---\n\n### PROC-VA-003: Coleta de desempenho\n\n```\nSTART (cron autopilot-collect, hor\u00e1rio)\n  \u2502\n[SELECT scheduled_posts status='published' AND cycle_id NOT NULL AND metrics_pending]\n  \u2502\n[para cada post: resolve post_id + plataforma]\n  \u2502\n<Gateway: API de insights dispon\u00edvel p/ a rede/tier?>\n  \u2502 NO  \u2500\u2500\u25b6 [registrar s\u00f3 affiliate_clicks do click ledger] (sinal sempre dispon\u00edvel)\n  \u2502 YES \u2500\u2500\u25b6 [fetch insights (likes/views/shares) best-effort]\n  \u2502\n[UPSERT creative_metrics (content_variant_id, source) \u2014 idempotente]\n  \u2502\n[merge revenue: handle-ml-postback j\u00e1 creditou affiliate_links \u2192 refletir revenue_cents]\n  \u2502\nEND  (alimenta PROC-VA-005)\n```\n\n---\n\n## 3. n8n Workflow Blueprints\n\n> O `viral-autopilot` usa **pg_cron + Edge Functions** como motor prim\u00e1rio (consistente com `nurture-advance`). n8n \u00e9 opcional como camada de notifica\u00e7\u00e3o/observa\u00e7\u00e3o externa.\n\n### Workflow: Autopilot Cycle Alert (opcional)\n\n**Trigger:** Supabase webhook em `infra_health_logs` (event `viral_autopilot_aborted_budget` ou `_collect_failure`)  \n**Idempotency key:** `infra_health_logs.id`\n\n```\n[Trigger: webhook infra_health_logs (autopilot event)]\n  \u2502\n  \u25bc\n[Node: Filter event_type IN (aborted_budget, collect_failure, analyze_empty)]\n  \u2502\n  \u251c\u2500\u2500 (aborted_budget) \u2500\u2500\u25b6 [Node: Telegram @claw_gcrux \"Plano <x> pausado \u2014 teto de custo\"]\n  \u2502\n  \u2514\u2500\u2500 (collect_failure) \u2500\u2500\u25b6 [Node: Set retry; (count>3) \u2192 infra_health_logs {n8n_alert}]\n```\n\n**Data Mapping:**\n\n| Input Field | Source | \u2192 | Output Field | Destination |\n|-------------|--------|---|--------------|-------------|\n| `event` | infra_health_logs row | \u2192 | message | Telegram body |\n| `metadata.plan_id` | infra_health_logs row | \u2192 | context | Telegram body |\n\n---\n\n## 4. Orchestration Integration Points\n\n> O `viral-autopilot` \u00e9 um **wrapper sobre `orchestrate-content`**, n\u00e3o um novo passo dentro dele. O ciclo dispara N execu\u00e7\u00f5es de `orchestrate-content` (uma por produto\u00d7rede), cada uma com `product_target` injetado.\n\n| Pipeline Step | Step ID | Position | Description | mcoCoins Trigger |\n|---------------|---------|----------|-------------|-----------------|\n| `product_target` injection | n/a (param) | entrada do orchestrate-content | `autopilot-run` passa `{ product_id, product_meta, feedback_features }` que hoje \u00e9 dropado (FR-VA-016) | \u2014 |\n| `monetize_all_formats` | dentro de orchestrate-step | ap\u00f3s cada formato (article/linkedin/twitter) | `_shared/affiliate.ts` embute link ML + content_variant_id (FR-VA-004) | 0 |\n| `feedback_inject` | dentro de orchestrate-step | antes da chamada LLM | injeta features do `optimization_policy` no system prompt (FR-VA-011) | 0 |\n\n**Integration code stub (dentro de `autopilot-run/index.ts`):**\n```typescript\n// Para cada produto-alvo \u00d7 rede do plano:\nfor (const product of selectedProducts) {\n  for (const platform of plan.platforms) {\n    await updateCycleStatus(cycleId, 'running')\n    const run = await supabase.functions.invoke('orchestrate-content', {\n      headers: { Authorization: userJwt },     // self-bill no tenant\n      body: {\n        topic: buildViralAngle(product, trends),   // FR-VA-018\n        product_target: { id: product.external_id, meta: product, feedback: policyFeatures }, // FR-VA-016\n        platforms: [platform],\n        cycle_id: cycleId,                          // NFR-VA-007 auditabilidade\n      },\n    })\n    if (!run.data?.ok) await logHealth('viral_autopilot_cycle_failed', { cycleId, platform })\n  }\n}\n```\n\n---\n\n## 5. Error Handling & Retry Strategy\n\n| Process | Step | Error Type | Max Retries | Backoff | Failure Action |\n|---------|------|-----------|-------------|---------|----------------|\n| PROC-VA-001 | cost gate | saldo/teto insuficiente | 0 | \u2014 | `aborted_budget` + pause plan + notify (sem cobrar) |\n| PROC-VA-001 | fan-out orchestrate-content | sub-run 5xx | 2 | Fixo 5s | marcar criativo failed; ciclo segue (Promise.allSettled) |\n| PROC-VA-001 | re-arm next_run_at | DB error | 3 | Exp (2s,4s,8s) | infra_health_logs; cron retenta no pr\u00f3ximo tick (idempotente por cycle_number) |\n| PROC-VA-003 | fetch insights | API tier/timeout | 1 | Fixo | fallback p/ s\u00f3 affiliate_clicks; log `collect_failure` |\n| PROC-VA-005 | analyze | LLM timeout / m\u00e9tricas vazias | 1 | \u2014 | se vazio: baseline (`has_real_data=false`), N\u00c3O inventa; log `analyze_empty` |\n| Qualquer | JWT validation | token inv\u00e1lido | 0 | \u2014 | HTTP 401 imediato |\n\n---\n\n## 6. SLA Definitions\n\n| Process | Step | Expected Duration | Timeout Threshold | Alert if exceeded |\n|---------|------|------------------|-------------------|-------------------|\n| PROC-VA-001 | ciclo end-to-end (N\u22648 criativos) | < 5min | 15min | Sim \u2192 infra_health_logs `sla_breach` |\n| PROC-VA-001 | cost gate | < 1s | 5s | N\u00e3o |\n| PROC-VA-002 | autopilot-run (dry_run) | < 2s | 5s | Sim |\n| PROC-VA-003 | coleta por post | < 3s | 30s | N\u00e3o (best-effort) |\n| PROC-VA-005 | analyze | < 10s | 60s | Sim |\n\n---\n\n## 7. Cron Jobs\n\n| Job Name | Schedule (cron) | Function | Idempotency | Failure Alerting |\n|----------|----------------|----------|-------------|-----------------|\n| `autopilot-cadence` | `*/15 * * * *` | `autopilot-cadence-cron` | re-arm de `next_run_at` + UNIQUE (plan_id, cycle_number) \u21d2 re-fire n\u00e3o duplica | `infra_health_logs` + Telegram (n8n opcional) |\n| `autopilot-collect` | `0 */6 * * *` (6/6h) | `autopilot-collect` | UPSERT (content_variant_id, source) | `infra_health_logs` `collect_failure` |\n\n> **Preservar crons existentes:** `memory_decay_fsrs`, `nurture-advance` (*/15), `watchdog-mcorch` (*/5), `auto-publish` (*/5), `audit-4cs`, `affiliate-enrich-cron` (6/6h). Os 2 novos jobs s\u00e3o adicionais.\n> **Idempot\u00eancia (NFR-VA-003):** re-rodar o cron sobre o mesmo `next_run_at`/ciclo produz o mesmo resultado \u2014 o ciclo j\u00e1 aberto (UNIQUE plan_id+cycle_number) bloqueia duplicata; janela perdida faz catch-up no pr\u00f3ximo tick sem dobrar.\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/07-process-flow.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:06:48)*


## 🤖 Claude *(21:06:49)*

Agora o último — **quality-metrics** (CMQ/OE — KPIs, FMEA com 4 RPN>100, self-heal kill-switch, PDCA):

## 🤖 Claude *(21:07:57)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/08-quality-metrics.md",
  "content": "# Quality & Self-Optimization Specification\n\n**Project:** viral-autopilot  \n**Version:** v0.1 | **Date:** 2026-06-17  \n**BoK Applied:** CMQ/OE BOK (Process Management + Organizational Excellence)  \n**Status:** Draft\n\n---\n\n## 1. Quality Objectives\n\n| QO ID | Objective | Linked Business Objective | Target | Review Cadence |\n|-------|-----------|--------------------------|--------|---------------|\n| QO-001 | Autonomia sem interven\u00e7\u00e3o por post | BO-001 | \u2265 90% posts via autopilot | Weekly |\n| QO-002 | Loop de melhoria com dado real (n\u00e3o teatral) | BO-002 | \u2265 80% das an\u00e1lises com `has_real_data=true` ap\u00f3s ciclo 2 | Monthly |\n| QO-003 | Margem protegida: zero overspend | BO-003 | 100% ciclos com `spend_mco \u2264 budget_cap`; 0 deduct em ciclo abortado | Weekly |\n| QO-004 | Monetiza\u00e7\u00e3o universal | BO-004 | 100% criativos com link ML + `content_variant_id` | Weekly |\n\n---\n\n## 2. KPI Dashboard Definition\n\n> Data source: tabelas/views Supabase por KPI.\n\n| KPI ID | Name | Formula | Target | Warn Threshold | Critical Threshold | Data Source |\n|--------|------|---------|--------|---------------|-------------------|-------------|\n| KPI-VA-001 | Custo por ciclo | `SUM(spend_mco) per cycle` | \u2264 `budget_cap_mco` | > 80% do cap | > cap | `autopilot_cycles` |\n| KPI-VA-002 | Lift viral ciclo-a-ciclo | `avg_engagement(N+1) / avg_engagement(N)` | \u2265 1.10\u00d7 ap\u00f3s 3 ciclos | < 1.0\u00d7 | < 0.8\u00d7 (regress\u00e3o) | `creative_metrics` por `cycle_id` |\n| KPI-VA-003 | Receita ML atribu\u00edda por ciclo | `SUM(revenue_cents) per cycle / 100` | crescente MoM | estagnado 3 ciclos | 0 com cliques > 0 (postback morto) | `creative_metrics` + `affiliate_links` |\n| KPI-VA-004 | % criativos monetizados | `monetized_creatives / total_creatives` | 100% | < 100% | < 90% | `creative_metrics` \u2229 `affiliate_links` |\n| KPI-VA-005 | CTR de afiliado | `affiliate_clicks / impressions` | benchmark por produto | < baseline | 0 com impress\u00f5es > 0 | `creative_metrics` |\n| KPI-VA-006 | mcoCoins Burn Rate | `SUM(deductions) / active_plans` | < `budget_cap` m\u00e9dio | 80% | > cap | `profiles` + `mco_transactions` |\n| KPI-VA-007 | Edge Fn p95 Latency (`autopilot-run`) | `PERCENTILE_CONT(0.95)` | < 800ms (dry_run) | 1000ms | 2000ms | Supabase logs |\n| KPI-VA-008 | Cad\u00eancia cumprida | `cycles_on_time / cycles_due` | \u2265 98% | < 95% | < 90% | `autopilot_cycles` vs `next_run_at` |\n\n---\n\n## 3. FMEA Table\n\n> S, O, D: 1 (melhor) \u2192 10 (pior). RPN = S \u00d7 O \u00d7 D. RPN > 100 exige a\u00e7\u00e3o.\n\n| ID | Function | Failure Mode | Effect | S | O | D | RPN | Recommended Action |\n|----|---------|--------------|--------|---|---|---|-----|--------------------|\n| FMEA-VA-001 | Cost guardrail (FR-VA-007) | Bypass do teto / overspend aut\u00f4nomo (disparo paralelo, gate fraco) | Drena mcoCoins do tenant silenciosamente | 8 | 4 | 4 | **128** | Gate at\u00f4mico server-side ANTES do deduct + idempot\u00eancia (plan_id, cycle_number) + safety cap di\u00e1rio global (espelha vision-mcp); lock otimista no ciclo |\n| FMEA-VA-002 | Cycle analyzer (FR-VA-010) | \"Auto-melhoria teatral\": analisa `creative_metrics` vazia, LLM gera recomenda\u00e7\u00e3o gen\u00e9rica | Loop aparenta aprender mas n\u00e3o aprende; decis\u00f5es com base em ru\u00eddo | 6 | 6 | 5 | **180** | Bloquear deduct/aplica\u00e7\u00e3o quando vazio (`has_real_data=false`); usar `affiliate_clicks` (sempre dispon\u00edvel) como sinal m\u00ednimo; expor flag no dashboard |\n| FMEA-VA-003 | Cadence cron (FR-VA-005) | Re-fire do cron dobra post/cobran\u00e7a | Conte\u00fado duplicado nas redes + cobran\u00e7a dupla | 7 | 3 | 4 | 84 | UNIQUE (plan_id, cycle_number) + guarda em `scheduled_posts`; catch-up idempotente |\n| FMEA-VA-004 | Gera\u00e7\u00e3o aut\u00f4noma (FR-VA-003) | Conte\u00fado off-brand / viola ToS de rede ou ML publicado sem revis\u00e3o | Suspens\u00e3o de conta, dano de marca, queda de receita | 9 | 3 | 5 | **135** | Cyber-Sentinel gate pr\u00e9-publica\u00e7\u00e3o (input+output) + disclosure de afiliado + HITL opcional (PR-VA-013) |\n| FMEA-VA-005 | Product-aware prompt (FR-VA-003) | Prompt injection via nome/desc de produto ou texto de trend | Gera\u00e7\u00e3o desviada / vazamento de instru\u00e7\u00e3o | 8 | 3 | 5 | **120** | Sanitizar produto/trend antes do prompt; Cyber-Sentinel no input; validar output antes de publicar |\n| FMEA-VA-006 | Revenue attribution (FR-VA-017) | Postback ML nunca chega (secret global, OTD-ML-MP-PER-USER) | Receita atribu\u00edda = 0 mesmo com vendas; KPI-VA-003 cego | 6 | 5 | 3 | 90 | Fechar OTD-VA-007; provar 1 postback real; usar cliques de afiliado como proxy de ROI enquanto isso |\n| FMEA-VA-007 | mcoCoins deduction | RPC timeout \u2192 cobran\u00e7a dupla | Tenant cobrado em excesso | 9 | 2 | 3 | 54 | Idempotency key por sub-run; `deduct_mco_coins` at\u00f4mico |\n| FMEA-VA-008 | JWT validation (autopilot-run) | Header ausente/inv\u00e1lido | Acesso n\u00e3o autenticado | 10 | 2 | 1 | 20 | Hard fail no entrypoint; log `infra_health_logs` |\n| FMEA-VA-009 | embed-mcorch-node (observation) | Timeout de embedding | N\u00f3 de ciclo sem vetor (mem\u00f3ria n\u00e3o pesquis\u00e1vel) | 6 | 3 | 4 | 72 | Retry ass\u00edncrono; `scripts/backfill-embeddings.ts` |\n| FMEA-VA-010 | Credential resolution (NFR-VA-004) | Resolu\u00e7\u00e3o errada \u2192 tenant A usa credencial de B | Vazamento de credencial/quota cross-tenant | 9 | 2 | 4 | 72 | Resolu\u00e7\u00e3o per-user `auth.uid()` + RLS + teste de isolamento; fail-closed |\n| FMEA-VA-011 | Honor product param (FR-VA-016) | Regress\u00e3o do drop de `affiliate_url`/produto em `:79` | Conte\u00fado gerado n\u00e3o monetizado | 7 | 3 | 3 | 63 | Teste de integra\u00e7\u00e3o de regress\u00e3o; assert link presente em todo formato |\n| FMEA-VA-012 | Cadence availability (NFR-VA-006) | Cron caiu \u2192 janela perdida, plano trava | Cad\u00eancia interrompida silenciosamente | 4 | 3 | 4 | 48 | Reconcile-on-run (catch-up no pr\u00f3ximo tick); KPI-VA-008 alerta |\n\n**Itens com RPN > 100 (a\u00e7\u00e3o obrigat\u00f3ria):** FMEA-VA-002 (180), FMEA-VA-004 (135), FMEA-VA-001 (128), FMEA-VA-005 (120) \u2014 todos com a\u00e7\u00e3o recomendada acima.\n\n---\n\n## 4. Self-Optimization Loops\n\n| Loop ID | Trigger Condition | KPI Source | Autonomous Response | Escalation (human) |\n|---------|------------------|------------|--------------------|--------------------|\n| SOL-VA-001 | Ciclo N+1 disparado com `creative_metrics(N)` populada | `creative_metrics` | `autopilot-analyze` produz `optimization_policy`; gera\u00e7\u00e3o N+1 injeta top features (FR-VA-011) | \u2014 (\u00e9 o core loop) |\n| SOL-VA-002 | KPI-VA-002 lift < 0.8\u00d7 por 2 ciclos (regress\u00e3o) | `creative_metrics` | Reverter para baseline de prompt + sinalizar produto/\u00e2ngulo de baixa convers\u00e3o p/ poda | Alertar Sovereign |\n| SOL-VA-003 | KPI-VA-006 burn > 80% do cap | `mco_transactions` | Reduzir `planned_units` do pr\u00f3ximo ciclo (menos varia\u00e7\u00f5es) | Alertar se > cap |\n| SOL-VA-004 | Saldo < `min_balance_mco` | `profiles` | Pausar plano (kill-switch) + notifica\u00e7\u00e3o PT-BR; N\u00c3O disparar ciclo | \u2014 (sem auto-recarga) |\n| SOL-VA-005 | KPI-VA-005 CTR de um produto < baseline por 3 ciclos | `creative_metrics` | Despriorizar o produto na sele\u00e7\u00e3o (comm+trend) do pr\u00f3ximo ciclo | \u2014 |\n\n---\n\n## 5. Self-Healing Specifications\n\n### 5.1 Watchdog Telemetry Events\n\nNovos `event` em `infra_health_logs` (com `metadata` allowlist \u2014 n\u00e3o vazar per-tenant na tabela global-read):\n\n| Event Type | Trigger | Severity | Payload (allowlisted) |\n|------------|---------|----------|---------|\n| `viral_autopilot_cycle_started` | ciclo aberto | info | `{plan_id, cycle_number, planned_units}` |\n| `viral_autopilot_cycle_completed` | ciclo fechado | info | `{cycle_id, spend_mco, creatives}` |\n| `viral_autopilot_aborted_budget` | kill-switch disparado | warn | `{plan_id, projected_mco, budget_cap}` |\n| `viral_autopilot_collect_failure` | coletor falhou ap\u00f3s retry | warn | `{cycle_id, platform}` |\n| `viral_autopilot_analyze_empty` | an\u00e1lise sem dado real | warn | `{plan_id, cycle_id}` |\n| `viral_autopilot_cycle_failed` | sub-run de gera\u00e7\u00e3o 5xx | error | `{cycle_id, platform}` |\n\n### 5.2 Auto-Recovery Script Stubs\n\n```bash\n#!/bin/bash\n# scripts/self-heal-viral-autopilot.sh\n# Triggered by mega-brain-daemon when viral_autopilot_cycle_failed/analyze_empty detected\nLOG_TABLE=\"infra_health_logs\"\necho \"[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Self-heal viral-autopilot\"\n\n# 1. Reconcile stuck cycles: cycles 'running' > 30min \u2192 mark 'failed', N\u00c3O re-cobrar\n# 2. Re-arm planos com next_run_at no passado mas is_active (janela perdida)\n# 3. Re-disparar autopilot-collect para posts published sem creative_metrics h\u00e1 > 24h\n# (todas as a\u00e7\u00f5es idempotentes; service-role; logam recovery_ok em infra_health_logs)\necho \"[OK] Self-heal viral-autopilot complete\"\n```\n\n### 5.3 mega-brain-daemon Integration Points\n\n| Daemon Event | Condition | Action |\n|-------------|-----------|--------|\n| `health_check` | A cada 5 min (watchdog) | Checar ciclos `running` \u00f3rf\u00e3os (> 30min) e planos due n\u00e3o disparados |\n| `anomaly_detected` | `viral_autopilot_*` error rate > 5/h | Executar `self-heal-viral-autopilot.sh` |\n| `budget_anomaly` | `aborted_budget` > 3\u00d7 p/ o mesmo plano em 24h | Manter pausado + alertar Sovereign (plano mal-configurado) |\n| `recovery_confirmed` | Ciclo subsequente completa OK | Inserir `recovery_ok` em `infra_health_logs` |\n\n---\n\n## 6. SLA / SLO / SLI Definitions\n\n| Service | SLI (what we measure) | SLO (our target) | SLA (consequence) |\n|---------|----------------------|------------------|-------------------|\n| `autopilot-run` (dry_run) | p95 response latency | \u2264 800ms | Investigar se > 2s por > 1% das chamadas/m\u00eas |\n| Cad\u00eancia | % ciclos disparados em \u2264 15min do `next_run_at` | \u2265 98% | Self-heal + alerta se < 90% |\n| Cost guardrail | % ciclos com `spend \u2264 cap` e 0 deduct em abortados | 100% | Incident report obrigat\u00f3rio se violado (dinheiro do tenant) |\n| Coleta de m\u00e9tricas | % posts com \u2265 1 sinal em `creative_metrics` \u2264 24h | \u2265 95% (cliques sempre; org\u00e2nico best-effort) | Auto-retry; cair p/ s\u00f3 cliques |\n| Monetiza\u00e7\u00e3o | % criativos com link ML v\u00e1lido | 100% | Bloquear publica\u00e7\u00e3o de criativo sem link |\n\n---\n\n## 7. PDCA Improvement Cadence\n\n| Cycle | Phase | Activity | Owner | Frequency |\n|-------|-------|----------|-------|-----------|\n| viral-autopilot Quality | Plan | Revisar FMEA (RPN>100) + alvos de KPI | Sovereign | Quarterly |\n| viral-autopilot Quality | Do | Implementar top a\u00e7\u00e3o (ex.: fechar OTD-ML-MP-PER-USER) | Engineering | Per sprint |\n| viral-autopilot Quality | Check | Comparar KPI-VA-002 (lift) e KPI-VA-003 (receita) vs alvo; atualizar RPNs | AIOS | Monthly |\n| viral-autopilot Quality | Act | Fechar loop; podar produtos/\u00e2ngulos de baixa convers\u00e3o; atualizar este doc | Sovereign | Monthly |\n\n**Improvement backlog location:** `.claude/context/sprint-priorities.md`\n\n---\n\n## 8. Observability Checklist\n\n### 8.1 Logging Events\n\n| Event | Location | Level | Fields logged |\n|-------|----------|-------|--------------|\n| Entrada de fun\u00e7\u00e3o | `autopilot-run/index.ts` ~linha 10 | INFO | `{user_id, plan_id, request_id}` |\n| Cost gate decision | ap\u00f3s proje\u00e7\u00e3o | INFO | `{projected_mco, budget_cap, decision}` |\n| mcoCoins deduction (sub-run) | ap\u00f3s RPC | INFO | `{user_id, amount, new_balance, cycle_id}` |\n| Feedback inject | antes da chamada LLM | INFO | `{cycle_id, has_real_data, features_count}` |\n| Erro de l\u00f3gica | catch block | ERROR | `{cycle_id, error_message}` |\n| SLA breach | timeout guard | WARN | `{process_id, elapsed_ms}` |\n\n### 8.2 Alerting Rules\n\n| Condition | Channel | Escalation |\n|-----------|---------|------------|\n| `aborted_budget` para 1 plano | `infra_health_logs` + Telegram | Sovereign se > 3\u00d7 em 24h |\n| `analyze_empty` ap\u00f3s ciclo 2 | `infra_health_logs` | AIOS (loop teatral \u2014 FMEA-VA-002) |\n| KPI-VA-003 = 0 com cliques > 0 | scheduled check | Sovereign (postback morto \u2014 FMEA-VA-006) |\n| p95 `autopilot-run` > 2s | `infra_health_logs` | mega-brain-daemon self-heal |\n\n### 8.3 Distributed Tracing Touchpoints\n\n| Span | Start | End | Tags |\n|------|-------|-----|------|\n| `autopilot-run.total` | request recebido | response enviado | `user_id`, `plan_id`, `cycle_id`, `status` |\n| `autopilot-run.cost_gate` | antes da proje\u00e7\u00e3o | ap\u00f3s decis\u00e3o | `projected_mco`, `decision` |\n| `autopilot-run.fanout` | in\u00edcio fan-out | fim Promise.allSettled | `creatives`, `failures` |\n| `autopilot-analyze.total` | leitura de m\u00e9tricas | policy gravada | `cycle_id`, `has_real_data` |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/08-quality-metrics.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:08:12)*


## 🤖 Claude *(21:08:14)*

Os 9 documentos estão escritos. Agora a **Fase 6 — Validação de Rastreabilidade Adversarial** (Closed-Loop exige: zero requisito órfão, RLS em toda tabela, mcoCoins atômico, FMEA RPN>100 com ação, e — crucial — confirmar que a suíte de fato fecha os gaps R2/R3 que a auditoria provou inexistentes). Vou rodar um workflow de 4 críticos paralelos + síntese GO/NO-GO, lendo os arquivos reais.

## 🤖 Claude *(21:09:01)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'viral-autopilot-bok-validation',\n  description: 'Phase 6 adversarial validation of the viral-autopilot BoK suite: traceability integrity, security/Harness constraints, R1-R4 gap-closure coverage, template/FMEA completeness \u2192 GO/NO-GO verdict with must-fix list',\n  phases: [\n    { title: 'Critique', detail: '4 parallel adversarial critics read the 9 docs' },\n    { title: 'Verdict', detail: 'synthesize GO/NO-GO + must-fix' },\n  ],\n}\n\nconst DIR = '/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot'\nconst BASE = `Voc\u00ea \u00e9 um cr\u00edtico ADVERSARIAL da su\u00edte BoK viral-autopilot em ${DIR} (9 docs: 00-index,01-mrd,02-brd,03-prd,04-frd,05-sdd,06-data-model,07-process-flow,08-quality-metrics). Leia os arquivos relevantes (Read/Grep) e CACE INCONSIST\u00caNCIAS \u2014 seu trabalho \u00e9 reprovar, n\u00e3o elogiar. Reporte findings com severidade e fix concreto (doc + se\u00e7\u00e3o). Default c\u00e9tico: se algo est\u00e1 amb\u00edguo ou falta, \u00e9 finding. N\u00e3o invente conte\u00fado; cite o que leu.`\n\nconst CRITIC_SCHEMA = {\n  type: 'object', additionalProperties: false,\n  properties: {\n    dimension: { type: 'string' },\n    verdict: { type: 'string', enum: ['pass', 'warn', 'fail'] },\n    findings: {\n      type: 'array',\n      items: {\n        type: 'object', additionalProperties: false,\n        properties: {\n          id: { type: 'string' },\n          severity: { type: 'string', enum: ['blocker', 'high', 'medium', 'low'] },\n          doc: { type: 'string' },\n          issue: { type: 'string' },\n          fix: { type: 'string' },\n        },\n        required: ['id', 'severity', 'doc', 'issue', 'fix'],\n      },\n    },\n    notes: { type: 'string' },\n  },\n  required: ['dimension', 'verdict', 'findings', 'notes'],\n}\n\nconst CRITICS = [\n  {\n    label: 'traceability',\n    prompt: `${BASE}\n\nDIMENS\u00c3O: Rastreabilidade. Construa a cadeia MR-VA-NNN \u2192 BR-VA-NNN \u2192 PR-VA-NNN \u2192 FR-VA-NNN \u2192 (tabela|edge fn|cron|processo). Assert:\n- Todo MR (8) rastreia \u22651 BR; todo BR (8) \u22651 PR; todo PR \u22651 FR; todo FR (18) \u22651 PR e \u22651 artefato no SDD/data-model/process-flow.\n- Sem ID \u00f3rf\u00e3o (aparece numa matriz mas nunca definido, ou definido mas nunca rastreado downstream).\n- As matrizes de rastreabilidade nos 4 docs (01,02,03,04) s\u00e3o MUTUAMENTE CONSISTENTES (ex.: PR-VA-008 image aparece como Must no PRD e tem FR? FR-VA-013 marcado 'Should (MVP)' \u2014 \u00e9 coerente com MVP=texto+imagem?).\n- Os 5 PROC do 07 cobrem todos os FR cr\u00edticos; os 2 crons existem no SDD e no process-flow.\nListe cada quebra de cadeia como finding.`,\n  },\n  {\n    label: 'security-harness',\n    prompt: `${BASE}\n\nDIMENS\u00c3O: Seguran\u00e7a + Harness Engineering (CISSP CBK + constraints CLAUDE.md/Survival). Assert sobre 05-sdd e 06-data-model:\n- Toda NOVA tabela (autopilot_plans, autopilot_cycles, creative_metrics) tem 'ENABLE ROW LEVEL SECURITY' + pol\u00edtica own-row (auth.uid()). Default-deny.\n- API Tenancy per-user: nenhuma credencial externa via env global em fluxo user-facing; resolu\u00e7\u00e3o por auth.uid(). Secrets s\u00f3 por NOME (nunca valor). Usa SB_SECRET_KEY (n\u00e3o a legada SUPABASE_SERVICE_ROLE_KEY revogada).\n- mcoCoins: dedu\u00e7\u00e3o s\u00f3 via deduct_mco_coins RPC, e o GATE de teto ocorre ANTES do deduct (FR-VA-007). Nunca client-side.\n- Toda edge fn user-facing valida JWT; crons usam service-role + verify_jwt=false (padr\u00e3o pg_net).\n- STRIDE cobre os componentes novos com \u22651 mitiga\u00e7\u00e3o por amea\u00e7a. Threat de prompt-injection (produto/trend) presente.\n- Migrations: nota de /security-review.\nCace qualquer tabela sem RLS, qualquer secret value, qualquer deduct sem gate, qualquer env global user-facing.`,\n  },\n  {\n    label: 'gap-closure',\n    prompt: `${BASE}\n\nDIMENS\u00c3O: Cobertura dos 4 requisitos Sovereign vs a auditoria material (a su\u00edte REALMENTE fecha os gaps?). Para CADA requisito, confirme que existe FR concreta (n\u00e3o s\u00f3 vis\u00e3o):\n- R1 (gera\u00e7\u00e3o auto p/ redes): FR de gera\u00e7\u00e3o product-aware + imagem no MVP? V\u00eddeo/TikTok corretamente diferidos p/ fase 2 (n\u00e3o no MVP)?\n- R2 (cad\u00eancia tudo-de-uma-vez OU a cada N dias): EXISTE FR de entidade de plano (autopilot_plans com mode+interval_days) + cron de auto-refill (FR-VA-005)? Isto fecha o gap 'recorr\u00eancia n\u00e3o existe' da auditoria?\n- R3 (loop auto-melhor\u00e1vel): as TR\u00caS quebras da auditoria est\u00e3o fechadas por FR? (a) campaign_metrics sem writer \u2192 coletor FR-VA-008 + creative_metrics FR-VA-009; (b) optimization_policy nunca lida por gerador \u2192 FR-VA-011 feedback inject; (c) self-optimize sem cron \u2192 FR-VA-005/010 agendado. H\u00e1 prote\u00e7\u00e3o contra 'auto-melhoria teatral' (m\u00e9tricas vazias)?\n- R4 (afiliado ML em todo formato): FR-VA-004 monetiza artigo+linkedin+twitter (n\u00e3o s\u00f3 artigo)? FR-VA-016 corrige o param dropado? Sele\u00e7\u00e3o por comiss\u00e3o+trend (FR-VA-012)?\nSe algum requisito ficou s\u00f3 como 'vis\u00e3o' sem FR acion\u00e1vel, \u00e9 BLOCKER.`,\n  },\n  {\n    label: 'completeness-fmea',\n    prompt: `${BASE}\n\nDIMENS\u00c3O: Completude de template + FMEA + contradi\u00e7\u00f5es internas. Assert:\n- Cada um dos 9 docs tem as se\u00e7\u00f5es obrigat\u00f3rias do seu template (ver .claude/agents/bok-scribe/templates/) e footer 'Generated by MCORCH BoK Scribe Agent v1.0.0'.\n- FMEA (08): todo item com RPN>100 tem a\u00e7\u00e3o recomendada; recompute alguns RPN (S\u00d7O\u00d7D) e cheque se batem com o valor escrito. O index afirma 4 itens RPN>100 \u2014 confirme a contagem.\n- mcoCoins cost definido para toda FR/opera\u00e7\u00e3o com IA (gera\u00e7\u00e3o 10, an\u00e1lise 5, imagem). NFRs presentes (8). Gherkin no PRD cobre os cen\u00e1rios-chave (cad\u00eancia, monetiza\u00e7\u00e3o, kill-switch, loop, ROI).\n- Contradi\u00e7\u00f5es entre docs (ex.: MVP date, contagem de FR/MR/BR, status de OTD, nomes de tabela/fn divergentes entre SDD e data-model/process-flow).\n- 00-index: traceability chain e phase log coerentes com o conte\u00fado real.\nListe se\u00e7\u00f5es faltantes, RPN incorretos, e contradi\u00e7\u00f5es como findings.`,\n  },\n]\n\nphase('Critique')\nlog('4 cr\u00edticos adversariais lendo os 9 docs da su\u00edte viral-autopilot...')\nconst critiques = (await parallel(\n  CRITICS.map((c) => () => agent(c.prompt, { label: `critic:${c.label}`, phase: 'Critique', schema: CRITIC_SCHEMA }))\n)).filter(Boolean)\n\nlog('Sintetizando veredito GO/NO-GO...')\nphase('Verdict')\n\nconst VERDICT_SCHEMA = {\n  type: 'object', additionalProperties: false,\n  properties: {\n    overallVerdict: { type: 'string', enum: ['GO', 'GO_WITH_FIXES', 'NO_GO'] },\n    summary: { type: 'string' },\n    mustFix: {\n      type: 'array',\n      items: {\n        type: 'object', additionalProperties: false,\n        properties: {\n          severity: { type: 'string', enum: ['blocker', 'high'] },\n          doc: { type: 'string' },\n          issue: { type: 'string' },\n          fix: { type: 'string' },\n        },\n        required: ['severity', 'doc', 'issue', 'fix'],\n      },\n    },\n    niceToHave: { type: 'array', items: { type: 'string' } },\n    gapClosureVerdict: {\n      type: 'object', additionalProperties: false,\n      properties: {\n        R1: { type: 'string' }, R2: { type: 'string' }, R3: { type: 'string' }, R4: { type: 'string' },\n      },\n      required: ['R1', 'R2', 'R3', 'R4'],\n    },\n  },\n  required: ['overallVerdict', 'summary', 'mustFix', 'niceToHave', 'gapClosureVerdict'],\n}\n\nconst verdict = await agent(\n  `Voc\u00ea \u00e9 o validador-chefe da Fase 6 do BoK Scribe. Abaixo os 4 relat\u00f3rios de cr\u00edtica adversarial (JSON). Sintetize:\n1. overallVerdict: GO (zero blocker/high), GO_WITH_FIXES (high mas sem blocker), ou NO_GO (\u22651 blocker).\n2. mustFix: consolide TODOS os findings severity blocker+high (dedup), cada um com doc+issue+fix acion\u00e1vel.\n3. gapClosureVerdict: para R1/R2/R3/R4, uma frase dizendo se a su\u00edte fecha o gap da auditoria (com a FR que fecha).\n4. niceToHave: medium/low que valem corrigir mas n\u00e3o bloqueiam o seal.\n5. summary: 2-3 frases \u2014 a su\u00edte est\u00e1 pronta para seal/Phase 7?\n\nRELAT\u00d3RIOS:\n${JSON.stringify(critiques, null, 2)}`,\n  { label: 'verdict', phase: 'Verdict', schema: VERDICT_SCHEMA }\n)\n\nreturn { critiques, verdict }\n",
  "description": "Adversarial validation of viral-autopilot BoK"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wql8i8sh7
> Summary: Phase 6 adversarial validation of the viral-autopilot BoK suite: traceability integrity, security/Harness constraints, R1-R4 gap-closure coverage, template/FMEA completeness → GO/NO-GO verdict with must-fix list
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/subagents/workflows/wf_162126db-952
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/workflows/scripts/viral-autopilot-bok-validation-wf_162126db-952.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/workflows/scripts/viral-autopilot-bok-validation-wf_162126db-952.js"} to iterate without resending the script.)
> Run ID: wf_162126db-952
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/workflows/scripts/viral-autopilot-bok-validation-wf_162126db-952.js", resumeFromRunId: "wf_162126db-952"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(21:09:14)*


## 🤖 Claude *(21:09:15)*

Enquanto a validação roda, vou adiantar trabalho não-bloqueante: ler o script-precedente do seal e rascunhar o `seed-viral-autopilot-bok-seal.ts` (Fase 7), que só será executado após o veredito GO.

## 🤖 Claude *(21:09:15)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/seed-openclaw-bok-seal.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env bun
> 2	/**
> 3	 * Seals the BoK documentation suite for openclaw in the Knowledge Mesh.
> 4	 * Inserts a documentation_suite node with stability 0.85; embedding triggered
> 5	 * automatically by trg_mcorch_embed_on_insert.
> 6	 *
> 7	 * Usage: bun run scripts/seed-openclaw-bok-seal.ts
> 8	 */
> 9	import { createClient } from '@supabase/supabase-js';
> 10	
> 11	const SUPABASE_URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL;
> 12	const SERVICE_KEY = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY);
> 13	
> 14	if (!SUPABASE_URL || !SERVICE_KEY) {
> 15	  console.error('Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY');
> 16	  process.exit(1);
> 17	}
> 18	
> 19	const supabase = createClient(SUPABASE_URL, SERVICE_KEY);
> 20	
> 21	const sealNode = {
> 22	  name: 'bok-scribe-seal-openclaw-v1',
> 23	  node_type: 'documentation_suite',
> 24	  project_id: 'openclaw',
> 25	  stability_score: 0.85,
> 26	  revenue_impact: 0, // módulo é enabler horizontal de velocity para os outros 4 BoK; proxy via lift dos outros módulos (não direct revenue)
> 27	  content: `OpenClaw — Pantheon Agency Runtime (BoK retroativa)
> 28	
> 29	BoK suite (9 docs) sealed 2026-05-19 sob MCORCH Master Execution Protocol. Esta seal quita o override consciente do BoK Gate registrado em Sprint v6.2.0 (2026-05-15) — Sovereign havia autorizado que a própria Agência OpenClaw quitaria a dívida assincronamente; com 4 sprints decorridos e a Agência operando em produção, esta seal materializa retroativamente o BoK que governa o módulo.
> 30	
> 31	VISÃO: Runtime de Pantheon Architecture com 7 agentes IA especializados (main router + engineer/scientist/artisan/marketing-growth L1 Heads + guardian Coordination + claw-master L2 Specialist) operando sob soberania física do Sovereign Gabriel Zarattini em /home/ubuntu/.openclaw/. Gateway local 127.0.0.1:18789 sob auth token (48-char hex), memória SQLite per-agente (FTS5 + vector embeddings), Memory Wiki em vault bridge mode, ciclo circadiano noturno (Stage 1 03:00 / Stage 2 05:00 / Stage 3 07:00 BRT espaçados 2h), e briefing diário ao Telegram chat 5835174772 às 07:30 BRT compondo 6 seções markdown ≤ 4000 chars (git delta + MEMORY promotions + BoK debt + revenue snippet + news pulse Perplexity Sonar + reflexão Paz e Vitalidade).
> 32	
> 33	ARQUITETURA: 1 config canônica (openclaw.json 180 LOC com schema strict v2026.5.14), 1 vault file-based (secrets.json chmod 600 com 6 SecretRef pointers), 7 agent dirs com 7-8 canonical files cada (SOUL/AGENTS/MEMORY/BOOTSTRAP/HEARTBEAT/IDENTITY/TOOLS/USER), 6 SQLite memory artifacts (main 626 MB + engineer 390 MB + scientist 232 MB + claw-master 90 MB + artisan 28 MB + marketing-growth 20 MB + guardian 20 MB), 1 OpenClaw daemon (gateway loopback), 1 Memory Wiki vault (~20 pages seed manual MCORCH-aware com pageType ∈ {synthesis, entity, concept, source, dashboard}). Pipeline scripts MCORCH: bridge-mesh-to-openclaw.ts (327 LOC two-tier hybrid; tier1 strategy + tier2 AST excluding ast_variable noise) + distribute-mesh-to-agents.ts (275 LOC shared base + overlay BoK-específica file copies) + nightly-stage{1,2,3}-*.sh (130/130/110 LOC) + compose-morning-briefing.ts (~250 LOC) + morning-briefing.sh (95 LOC) + news-impact-analyzer.ts (173 LOC) + watchdog-mcorch.sh (~150 LOC com Layer 2 escalation counter). Cron pipeline: 03:00/05:00/07:00 BRT (stages) + 03:00 OpenClaw native (Memory Dreaming Promotion) + */5min (watchdog) + 06:00 dia 16 (claw-master audit mensal).
> 34	
> 35	DRIFT RECONCILIADO (5 fechados em sprints anteriores · 8 ativos como OTDs): D-OC-001 (6 plain-text secrets → vault SecretRefs em v6.4.0), D-OC-002 (allowInsecureAuth=true → false em v6.4.0), D-OC-003 (perms 775 → 700 em v6.4.0), D-OC-004 (schema strict rejeitando agents.list[].enabled → jq surgical em v6.6.1), D-OC-005 (Memory Palace empty state → 20 wiki pages seed em v6.6.1). Drifts permanentes catalogados como OTDs: OTD-V660-002 (CLI memory index drift), OTD-OC-001 (main.sqlite 626 MB growth), OTD-OC-002 (SQLite schema opaco upstream), OTD-OC-005 (dynamic plugin loading aguardando upstream), OTD-CM-004/005/007 (rate limit + redact + showInSidebar pendentes). Registro autoritativo em 06-data-model.md §8 Drift Reconciliation Appendix.
> 36	
> 37	ECONOMIA: zero mcoCoins (módulo é infraestrutura, não tarifa operações). Custos diretos R$ 60-200/ano (orçamento OpenRouter Perplexity Sonar para Stage 3 news pulse). ROI direto não-quantificável; proxy material é velocity dos 5 outros módulos BoK (conteudo-v2 + viralmind + mcorch-constellation + gamificacao-nodes + este) — provavelmente 3-5× mais tempo Sovereign sem o squad.
> 38	
> 39	KPIs (10): KPI-OC-001 bridge runtime p95 ≤ 180s · KPI-OC-002 chunks indexed ≥ 9000 (atual 9185) · KPI-OC-003 briefing delivery rate ≥ 95%/30d · KPI-OC-004 SQLite growth ≤ 20MB/agent/dia · KPI-OC-005 watchdog escalation rate ≤ 1/sem · KPI-OC-006 Telegram quota usage ≤ 30% · KPI-OC-007 audit findings ≤ 1 P0 OR 3 P1 · KPI-OC-008 Dreaming runtime ≤ 30min · KPI-OC-009 wiki linter pass rate 100% · KPI-OC-010 secrets vault adherence 100%. FMEA-OC-001..010 com 5 RPN > 100: secrets regression (180), bridge fail stale overlay (150), daemon crash sem watchdog (126), Telegram quota silencia (125), audit scrape fail (105). Mitigations catalogadas em sprint backlog.
> 40	
> 41	OTDs ATIVAS (5 novas + 6 herdadas): OTD-OC-001..005 (main.sqlite vacuum cadence · SQLite schema opaque · multi-user expansion · briefing fallback · dynamic plugin loading). Herdadas: OTD-V660-002 (CLI drift) + OTD-CM-004 (rate limit) + OTD-CM-005 (redact) + OTD-CM-006 (multi-user heuristic — Decided 2026-05-19) + OTD-CM-007 (showInSidebar) + OTD-CM-008 (SOUL template — Decided 2026-05-16).
> 42	
> 43	DOCUMENTOS: docs/bok/openclaw/{00-index, 01-mrd, 02-brd, 03-prd, 04-frd, 05-sdd, 06-data-model, 07-process-flow, 08-quality-metrics}.md totalizando ~1700 LOC novos.
> 44	
> 45	TRACEABILITY: 6 MR-OC → 14 BR-OC → 8 FR-OC + 8 NFR-OC → 10 PROC-OC → 10 KPI-OC validados em 02-brd §10.
> 46	
> 47	PRÓXIMO DELIVERABLE (post-seal): (a) carry-overs OE-661 (provisionar GCRUX_ML_AFFILIATE_TOKEN + wire orchestrate emitir content_mesh_asset + primeiro run end-to-end Usuário Zero do flywheel); (b) claw-master audit-v2 (planejado 2026-06-16) verificar regressão D-OC-001..005 + novas findings; (c) OTD-CM-005 logging.redactSensitive set true no próximo edit consolidado de openclaw.json (P2 oportunístico); (d) D-OC-008 marketing-growth BOOTSTRAP.md scaffold (non-blocking).`,
> 48	  metadata: {
> 49	    bok_version: '1.0.0',
> 50	    documents: [
> 51	      '00-index',
> 52	      '01-mrd',
> 53	      '02-brd',
> 54	      '03-prd',
> 55	      '04-frd',
> 56	      '05-sdd',
> 57	      '06-data-model',
> 58	      '07-process-flow',
> 59	      '08-quality-metrics',
> 60	    ],
> 61	    phase_completed: 'Phase 7',
> 62	    traceability_validated: true,
> 63	    bok_gate: 'override-completion', // quita override consciente registrado em Sprint v6.2.0
> 64	    drift_reconciled: 5, // D-OC-001..005 (todos fechados em v6.4.0 e v6.6.1)
> 65	    drift_pending: 8, // D-OC-006..013 (catalogados como OTDs ativos)
> 66	    market_segment: 'B2B2C-internal',
> 67	    monetization_model: 'indirect-enabler',
> 68	    regulatory_profile: 'LGPD',
> 69	    integration_surface: 'extends-mcorch',
> 70	    project_slug: 'openclaw',
> 71	    feature_flag: 'pantheon-v6.3.1', // implícito
> 72	    sprint_introduced: 'v6.2.0',
> 73	    sprint_sealed: 'v6.6.5',
> 74	    tags: ['bok-scribe', 'openclaw', 'pantheon', 'agency', 'memory-bridge', 'retroactive', 'infrastructure'],
> 75	    new_tables: 0, // módulo é infraestrutura local; não introduz tabelas Supabase
> 76	    new_edge_functions: 0,
> 77	    new_rpcs: 0,
> 78	    new_pipeline_scripts: 9, // bridge + distribute + 3 stages + bridge-refresh + compose + morning + news-analyzer
> 79	    new_agents: 7, // main + 4 L1 + 1 Coord + 1 L2
> 80	    id_ranges: {
> 81	      MR: '001..006',
> 82	      BR: '001..014',
> 83	      BO: '001..006',
> 84	      SH: '001..010',
> 85	      FR: '1..8',
> 86	      NFR: '001..008',
> 87	      PR: '001..014',
> 88	      PROC: '001..010',
> 89	      KPI: '001..010',
> 90	      FMEA: '001..010',
> 91	      SOL: '001..006',
> 92	      QO: '001..008',
> 93	      BAC: '001..010',
> 94	      OTD_OC: '001..005',
> 95	    },
> 96	    related_otds: [
> 97	      'OTD-V631-001', // openclaw BoK SLA expandido — fechada por esta seal
> 98	      'OTD-V660-002', // CLI drift permanent
> 99	      'OTD-CM-001', 'OTD-CM-002', 'OTD-CM-003', // fechadas v6.4.0
> 100	      'OTD-CM-004', 'OTD-CM-005', 'OTD-CM-006', 'OTD-CM-007', 'OTD-CM-008', // herdadas audit-v1
> 101	      'OTD-OC-001', 'OTD-OC-002', 'OTD-OC-003', 'OTD-OC-004', 'OTD-OC-005', // novas
> 102	    ],
> 103	    fmea_rpn_over_100: ['FMEA-OC-001', 'FMEA-OC-002', 'FMEA-OC-003', 'FMEA-OC-004', 'FMEA-OC-010'],
> 104	    derives_from: 'bok-scribe-seal-gamificacao-nodes-v1', // UUID 6e8546bc-d995-4cc5-ac88-06cecbece181
> 105	    pantheon_agents: ['main', 'engineer', 'scientist', 'artisan', 'marketing-growth', 'guardian', 'claw-master'],
> 106	    cron_pipeline: ['stage1-03:00', 'stage2-05:00', 'stage3-07:00', 'memory-dreaming-05:00', 'watchdog-5min', 'audit-monthly-day16'],
> 107	  },
> 108	};
> 109	
> 110	console.log(`📝 Sealing BoK suite "openclaw"...`);
> 111	console.log(`   Project: ${sealNode.project_id}`);
> 112	console.log(`   Stability: ${sealNode.stability_score}`);
> 113	console.log(`   Revenue impact: ${sealNode.revenue_impact} (indirect-enabler — velocity proxy)`);
> 114	console.log(`   BoK gate: ${sealNode.metadata.bok_gate}`);
> 115	console.log(`   Drift reconciled: ${sealNode.metadata.drift_reconciled} (D-OC-001..005)`);
> 116	console.log(`   Drift pending: ${sealNode.metadata.drift_pending} (OTDs ativos)`);
> 117	
> 118	const { data, error } = await supabase
> 119	  .from('mcorch_nodes')
> 120	  .insert(sealNode)
> 121	  .select('id, name, node_type, stability_score, created_at')
> 122	  .single();
> 123	
> 124	if (error) {
> 125	  console.error('❌ Seal failed:', error);
> 126	  process.exit(1);
> 127	}
> 128	
> 129	console.log(`\n✅ Seal node inserted:`);
> 130	console.log(`   ID:        ${data.id}`);
> 131	console.log(`   Name:      ${data.name}`);
> 132	console.log(`   Type:      ${data.node_type}`);
> 133	console.log(`   Stability: ${data.stability_score}`);
> 134	console.log(`   Created:   ${data.created_at}`);
> 135	console.log(`\n🧠 Embedding will be generated automatically by trg_mcorch_embed_on_insert (assíncrono via pg_net).`);
> 136	console.log(`   Confirm with: SELECT embedding IS NOT NULL FROM mcorch_nodes WHERE id = '${data.id}';`);
> 137	
> ```

## 🤖 Claude *(21:09:25)*


## 🤖 Claude *(21:09:27)*

O precedente openclaw grava `derives_from` só em metadata. A definição da Fase 7 exige também inserir a aresta `DERIVES_FROM` em `mcorch_edges` e idempotência por nome. Vou checar o precedente mais recente (e2e-user-zero) para espelhar o padrão de edge + idempotência:

## 🤖 Claude *(21:09:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls scripts/seed-*bok-seal.ts 2>/dev/null; echo \"---most recent edge-insert pattern---\"; grep -l \"mcorch_edges\" scripts/seed-*bok-seal.ts 2>/dev/null",
  "description": "Find seal scripts that insert edges"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> scripts/seed-authenticated-browser-operator-bok-seal.ts
> scripts/seed-constellation-v2-bok-seal.ts
> scripts/seed-conteudo-v2-bok-seal.ts
> scripts/seed-e2e-user-zero-bok-seal.ts
> scripts/seed-gamificacao-nodes-bok-seal.ts
> scripts/seed-identity-fabric-bok-seal.ts
> scripts/seed-marketing-hub-bok-seal.ts
> scripts/seed-mercado-livre-api-bok-seal.ts
> scripts/seed-meta-api-bok-seal.ts
> scripts/seed-openclaw-bok-seal.ts
> scripts/seed-post-engine-bok-seal.ts
> scripts/seed-viral-daily-canvas-bok-seal.ts
> scripts/seed-viralmind-bok-seal.ts
> scripts/seed-vision-mcp-bok-seal.ts
> ---most recent edge-insert pattern---
> scripts/seed-authenticated-browser-operator-bok-seal.ts
> scripts/seed-constellation-v2-bok-seal.ts
> scripts/seed-identity-fabric-bok-seal.ts
> scripts/seed-meta-api-bok-seal.ts
> scripts/seed-marketing-hub-bok-seal.ts
> scripts/seed-post-engine-bok-seal.ts
> scripts/seed-vision-mcp-bok-seal.ts
> scripts/seed-mercado-livre-api-bok-seal.ts
> scripts/seed-viral-daily-canvas-bok-seal.ts
> scripts/seed-e2e-user-zero-bok-seal.ts
> ```

## 🤖 Claude *(21:09:32)*


## 🤖 Claude *(21:09:32)*

`marketing-hub` é o parent topicamente mais próximo e insere arestas. Vou lê-lo para espelhar idempotência + edge-insert:

## 🤖 Claude *(21:09:33)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/seed-marketing-hub-bok-seal.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env bun
> 2	/**
> 3	 * Seals the BoK documentation suite for marketing-hub in the Knowledge Mesh.
> 4	 * Inserts a documentation_suite node with stability 0.85; embedding triggered
> 5	 * automatically by trg_mcorch_embed_on_insert (pg_net).
> 6	 *
> 7	 * Inserts an explicit DERIVES_FROM edge to the parent seal (meta-api v1 —
> 8	 * marketing-hub absorbs whatsapp_leads from the meta-api data model and shares
> 9	 * the marketing/lead/distribution domain).
> 10	 *
> 11	 * Usage: bun run scripts/seed-marketing-hub-bok-seal.ts
> 12	 */
> 13	import { createClient } from '@supabase/supabase-js';
> 14	
> 15	const SUPABASE_URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL;
> 16	const SERVICE_KEY = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY);
> 17	
> 18	if (!SUPABASE_URL || !SERVICE_KEY) {
> 19	  console.error('Missing SUPABASE_URL or SB_SECRET_KEY');
> 20	  process.exit(1);
> 21	}
> 22	
> 23	const supabase = createClient(SUPABASE_URL, SERVICE_KEY);
> 24	
> 25	const PARENT_SEAL_NAME = 'bok-scribe-seal-meta-api-v1';
> 26	
> 27	const sealNode = {
> 28	  name: 'bok-scribe-seal-marketing-hub-v1',
> 29	  node_type: 'documentation_suite',
> 30	  project_id: 'marketing-hub',
> 31	  stability_score: 0.85,
> 32	  revenue_impact: 1000000, // direct-revenue enabler — módulo comercial per-tenant (assinatura + mcoCoins por ação + receita de afiliado atribuída); ancorado ao Million-BRL Roadmap, pricing deferido (OTD)
> 33	  content: `marketing-hub — Marketing Hub agentic soberano do MCORCH (BoK v1)
> 34	
> 35	BoK suite (9 docs, 1732 LOC) sealed 2026-06-02 sob MCORCH Master Execution Protocol. Motivada por diretiva do Sovereign a partir de um "Framework Universal para Módulos de Marketing Inteligentes e Adaptáveis (Plataforma Agentic)" (benchmarks HubSpot Marketing Hub/Breeze/AEO + Salesforce Marketing Cloud/Agentforce/Data Cloud). Decisões de escopo travadas via AskUserQuestion: natureza Ambos (núcleo interno Usuário Zero + superfície comercial per-tenant); módulo soberano novo que ABSORVE e escala o v1 (nasce como consolidação v2); /bok-scribe primeiro, /bok-agents-generator depois com ≥8 agentes.
> 36	
> 37	VISÃO: módulo que percebe → decide → executa → aprende estratégias de growth com governança humana (HITL). Consolida as superfícies de marketing dispersas do MCORCH (orchestrate-content single-shot, marketing-growth Pantheon, whatsapp_leads, afiliados ML) numa única superfície /dashboard/marketing. REUTILIZA infra provada (mcorch_nodes/edges + pgvector HNSW 768d para Data Core/RAG; infra_health_logs + ROIWidget + affiliate_links.revenue_cents + ATTRIBUTES_REVENUE_TO para Observability/Attribution; edge functions + credenciais per-user para Connectivity; mcorch-qa-healing para Auto-cura) em vez de reconstruir.
> 38	
> 39	DELTA (foco do BoK): (1) camada CRM/Lead completa — capture→score→nurture→convert, absorvendo whatsapp_leads (tutela meta-api→marketing-hub, OTD-MH-001); (2) AEO (Answer Engine Optimization) — visibilidade da marca em motores de resposta de IA; (3) campaign management de 1ª classe (wrap multicanal sobre orchestrate-content); (4) buyer intent + data enrichment; (5) sequências de nurturing email/multicanal; (6) orquestrador event-driven por intenção (policy engine + HITL + arbitragem).
> 40	
> 41	ARQUITETURA: 9 tabelas novas (leads, lead_events, campaigns, campaign_steps, sequences, sequence_enrollments, marketing_consents, marketing_attribution, aeo_audits) + view customer_360 + 6 edge functions (lead-score, campaign-run, nurture-dispatch, intent-orchestrate, aeo-audit, erase-lead). CISSP CBK elevado por LGPD: STRIDE com PII de lead Critical, RLS default-deny por auth.uid(), erasure cascade via SECURITY DEFINER (espelha disconnect_*), consent gate hard pré-nurturing, BYOK per-tenant no padrão Vault.
> 42	
> 43	ID SPACE: MR-MH-001..012 · BR-MH-001..012 · BO-MH-001..005 · SH-MH-001..006 · PR-MH-001..023 · FR-MH-001..012 · NFR-MH-001..010 · PROC-MH-001..008 · KPI-MH-001..009 · FMEA-MH-001..009 · SOL-MH-001..005 · QO-MH-001..006 · BAC-MH-001..006 · OTD-MH-001..005.
> 44	
> 45	FMEA (9 entries, 3 RPN > 100): FMEA-MH-003 (RPN 135 — erasure cascade incompleta/PII residual; ação: erasure transacional + verificação zero-residue + retry crítico + teste E2E), FMEA-MH-005 (RPN 125 — provider AEO devolve citação alucinada; ação: probe-first Lei 1 + validação multi-engine + confidence + degradado documentado), FMEA-MH-002 (RPN 108 — nurturing sem consentimento/violação LGPD; ação: consent gate hard server-side + checagem por passo + teste de regressão).
> 46	
> 47	DOCUMENTOS: docs/bok/marketing-hub/{00-index 88, 01-mrd 143, 02-brd 169, 03-prd 216, 04-frd 167, 05-sdd 315, 06-data-model 255, 07-process-flow 204, 08-quality-metrics 175} — total 1732 LOC.
> 48	
> 49	TRACEABILITY: 100% de cobertura MR → BR → PR → FR (zero orphans). PRs de Future scope (PR-MH-020..023) intencionalmente não-decompostos em FR neste ciclo (documentado no FRD §1). Parent seal meta-api (whatsapp_leads absorption).
> 50	
> 51	BoK GATE: liberado APÓS este seal. Código de produção só inicia após /bok-agents-generator (≥8 agentes reconciliados com o Pantheon) + migrations com /security-review aprovadas. Scope-lock: .claude/context/marketing-hub-scope-lock-2026-06-02.md.`,
> 52	  metadata: {
> 53	    bok_version: '1.0.0',
> 54	    documents: [
> 55	      '00-index',
> 56	      '01-mrd',
> 57	      '02-brd',
> 58	      '03-prd',
> 59	      '04-frd',
> 60	      '05-sdd',
> 61	      '06-data-model',
> 62	      '07-process-flow',
> 63	      '08-quality-metrics',
> 64	    ],
> 65	    document_lines: {
> 66	      '00-index': 88,
> 67	      '01-mrd': 143,
> 68	      '02-brd': 169,
> 69	      '03-prd': 216,
> 70	      '04-frd': 167,
> 71	      '05-sdd': 315,
> 72	      '06-data-model': 255,
> 73	      '07-process-flow': 204,
> 74	      '08-quality-metrics': 175,
> 75	      total: 1732,
> 76	    },
> 77	    phase_completed: 'Phase 7',
> 78	    traceability_validated: true,
> 79	    traceability_orphans: 0,
> 80	    bok_gate: 'fresh-completion',
> 81	    drift_reconciled: 0,
> 82	    drift_pending: 0,
> 83	    market_segment: 'B2B2C',
> 84	    monetization_model: 'hybrid',
> 85	    regulatory_profile: 'LGPD+GDPR',
> 86	    integration_surface: 'extends-mcorch',
> 87	    project_slug: 'marketing-hub',
> 88	    sprint_introduced: 'v6.21.0',
> 89	    sprint_sealed: 'pending-handoff',
> 90	    tags: ['bok-scribe', 'marketing-hub', 'B2B2C', 'agentic', 'crm', 'lead-scoring', 'nurturing', 'aeo', 'campaign-management', 'attribution', 'lgpd', 'gdpr', 'per-user-tenancy', 'v2-consolidation'],
> 91	    modules: [
> 92	      'Lead Core (capture→score→nurture→convert; absorve whatsapp_leads)',
> 93	      'Campaign Core (multicanal sobre orchestrate-content)',
> 94	      'AEO Engine (Answer Engine Optimization)',
> 95	      'Intent Orchestrator + HITL policy engine',
> 96	      'Nurturing Sequences (drip)',
> 97	      'Attribution + Customer 360',
> 98	    ],
> 99	    new_tables: 9,
> 100	    new_views: 1,
> 101	    new_columns: 0,
> 102	    new_edge_functions: 6,
> 103	    extended_edge_functions: 1, // orchestrate-content reused as campaign executor
> 104	    new_rpcs: 1, // erase_lead (SECURITY DEFINER); reuses deduct_mco_coins
> 105	    new_migrations: 7,
> 106	    id_ranges: {
> 107	      MR: '001..012',
> 108	      BR: '001..012',
> 109	      BO: '001..005',
> 110	      SH: '001..006',
> 111	      PR: '001..023',
> 112	      FR: '001..012',
> 113	      NFR: '001..010',
> 114	      PROC: '001..008',
> 115	      KPI: '001..009',
> 116	      FMEA: '001..009',
> 117	      SOL: '001..005',
> 118	      QO: '001..006',
> 119	      BAC: '001..006',
> 120	      OTD: '001..005',
> 121	    },
> 122	    fmea_rpn_over_100: ['FMEA-MH-002', 'FMEA-MH-003', 'FMEA-MH-005'],
> 123	    fmea_rpn_top: {
> 124	      'FMEA-MH-003': 135,
> 125	      'FMEA-MH-005': 125,
> 126	      'FMEA-MH-002': 108,
> 127	    },
> 128	    derives_from: PARENT_SEAL_NAME,
> 129	    depends_on_sop: '.claude/context/marketing-hub-scope-lock-2026-06-02.md',
> 130	    motivating_incident: 'Sovereign directive — Framework Universal de Marketing (Plataforma Agentic) → módulo marketing-hub v2',
> 131	    revenue_impact_basis: 'commercial-marketing-module-per-tenant-monetization (Million-BRL Roadmap anchor; pricing deferred OTD)',
> 132	    reuses: ['mcorch_nodes/edges', 'pgvector HNSW 768d', 'infra_health_logs', 'ROIWidget', 'affiliate_links.revenue_cents', 'ATTRIBUTES_REVENUE_TO', 'orchestrate-content', 'deduct_mco_coins RPC', 'mcorch-qa-healing', 'marketing-growth Pantheon'],
> 133	    absorbs: ['whatsapp_leads (tutela meta-api→marketing-hub, OTD-MH-001)', 'orchestrate-content (single-shot → campaign executor)', 'marketing-growth Pantheon agent (elevated, not recreated)'],
> 134	    related_otds: ['OTD-MH-001', 'OTD-MH-002', 'OTD-MH-003', 'OTD-MH-004', 'OTD-MH-005'],
> 135	    next_step: '/bok-agents-generator marketing-hub (≥8 agents, reconciled with Pantheon)',
> 136	    skips: ['White-label tenant billing portal', 'Native paid-ads buying (Google/Meta Ads spend)', 'Multimodal video-ad generation beyond Canvas Studio'],
> 137	  },
> 138	};
> 139	
> 140	console.log(`📝 Sealing BoK suite "marketing-hub"...`);
> 141	console.log(`   Project: ${sealNode.project_id}`);
> 142	console.log(`   Stability: ${sealNode.stability_score}`);
> 143	console.log(`   Revenue impact: ${sealNode.revenue_impact} (${sealNode.metadata.monetization_model})`);
> 144	console.log(`   BoK gate: ${sealNode.metadata.bok_gate}`);
> 145	console.log(`   Parent (DERIVES_FROM): ${PARENT_SEAL_NAME}`);
> 146	
> 147	// Idempotency check: skip if already exists
> 148	const { data: existing } = await supabase
> 149	  .from('mcorch_nodes')
> 150	  .select('id, name, created_at')
> 151	  .eq('name', sealNode.name)
> 152	  .maybeSingle();
> 153	
> 154	if (existing) {
> 155	  console.log(`\n⚠️ Seal node already exists (idempotent skip):`);
> 156	  console.log(`   ID:        ${existing.id}`);
> 157	  console.log(`   Name:      ${existing.name}`);
> 158	  console.log(`   Created:   ${existing.created_at}`);
> 159	  console.log(`\nNo new INSERT performed.`);
> 160	  process.exit(0);
> 161	}
> 162	
> 163	// Step 1: INSERT documentation_suite node
> 164	const { data: insertedNode, error: nodeError } = await supabase
> 165	  .from('mcorch_nodes')
> 166	  .insert(sealNode)
> 167	  .select('id, name, node_type, stability_score, created_at')
> 168	  .single();
> 169	
> 170	if (nodeError) {
> 171	  console.error('❌ Seal node insert failed:', nodeError);
> 172	  process.exit(1);
> 173	}
> 174	
> 175	console.log(`\n✅ Seal node inserted:`);
> 176	console.log(`   ID:        ${insertedNode.id}`);
> 177	console.log(`   Name:      ${insertedNode.name}`);
> 178	console.log(`   Type:      ${insertedNode.node_type}`);
> 179	console.log(`   Stability: ${insertedNode.stability_score}`);
> 180	console.log(`   Created:   ${insertedNode.created_at}`);
> 181	
> 182	// Step 2: Resolve parent seal UUID for DERIVES_FROM edge
> 183	const { data: parent, error: parentError } = await supabase
> 184	  .from('mcorch_nodes')
> 185	  .select('id, name')
> 186	  .eq('name', PARENT_SEAL_NAME)
> 187	  .single();
> 188	
> 189	if (parentError || !parent) {
> 190	  console.error(`\n❌ Parent seal lookup failed for ${PARENT_SEAL_NAME}:`, parentError);
> 191	  console.error('   Skipping DERIVES_FROM edge insert. Manual cleanup may be required.');
> 192	  process.exit(1);
> 193	}
> 194	
> 195	console.log(`\n🔗 Parent seal resolved:`);
> 196	console.log(`   ID:        ${parent.id}`);
> 197	console.log(`   Name:      ${parent.name}`);
> 198	
> 199	// Step 3: INSERT DERIVES_FROM edge
> 200	const { data: insertedEdge, error: edgeError } = await supabase
> 201	  .from('mcorch_edges')
> 202	  .insert({
> 203	    source_id: insertedNode.id,
> 204	    target_id: parent.id,
> 205	    relation_type: 'DERIVES_FROM',
> 206	    weight: 1.0,
> 207	    project_id: 'marketing-hub',
> 208	    metadata: {
> 209	      lineage: 'bok-scribe-seal',
> 210	      source_seal: insertedNode.name,
> 211	      target_seal: parent.name,
> 212	      sealed_at: insertedNode.created_at,
> 213	    },
> 214	  })
> 215	  .select('id, source_id, target_id, relation_type, created_at')
> 216	  .single();
> 217	
> 218	if (edgeError) {
> 219	  console.error('❌ DERIVES_FROM edge insert failed:', edgeError);
> 220	  process.exit(1);
> 221	}
> 222	
> 223	console.log(`\n✅ DERIVES_FROM edge inserted:`);
> 224	console.log(`   ID:        ${insertedEdge.id}`);
> 225	console.log(`   Source:    ${insertedEdge.source_id} (${insertedNode.name})`);
> 226	console.log(`   Target:    ${insertedEdge.target_id} (${parent.name})`);
> 227	console.log(`   Relation:  ${insertedEdge.relation_type}`);
> 228	console.log(`   Created:   ${insertedEdge.created_at}`);
> 229	
> 230	console.log(`\n🧠 Embedding will be generated automatically by trg_mcorch_embed_on_insert (assíncrono via pg_net).`);
> 231	console.log(`   Confirm with: SELECT embedding IS NOT NULL FROM mcorch_nodes WHERE id = '${insertedNode.id}';`);
> 232	console.log(`\n📊 Material proof summary for handoff:`);
> 233	console.log(`   - documentation_suite node UUID: ${insertedNode.id}`);
> 234	console.log(`   - DERIVES_FROM edge UUID:        ${insertedEdge.id}`);
> 235	console.log(`   - Parent seal UUID:              ${parent.id}`);
> 236	
> ```

## 🤖 Claude *(21:09:39)*


## 🤖 Claude *(21:09:41)*

Padrão perfeito para espelhar. Vou pegar as contagens de linhas dos 9 docs e autorar o seed script (parent = `marketing-hub`, domínio mais próximo — campaign-run executor + conteúdo/afiliado):

## 🤖 Claude *(21:09:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l docs/bok/viral-autopilot/*.md | sort -k2",
  "description": "Line counts of the 9 BoK docs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>    104 docs/bok/viral-autopilot/00-index.md
>    133 docs/bok/viral-autopilot/01-mrd.md
>    158 docs/bok/viral-autopilot/02-brd.md
>    214 docs/bok/viral-autopilot/03-prd.md
>    181 docs/bok/viral-autopilot/04-frd.md
>    334 docs/bok/viral-autopilot/05-sdd.md
>    208 docs/bok/viral-autopilot/06-data-model.md
>    217 docs/bok/viral-autopilot/07-process-flow.md
>    173 docs/bok/viral-autopilot/08-quality-metrics.md
>   1722 total
> ```

## 🤖 Claude *(21:10:54)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/seed-viral-autopilot-bok-seal.ts",
  "content": "#!/usr/bin/env bun\n/**\n * Seals the BoK documentation suite for viral-autopilot in the Knowledge Mesh.\n * Inserts a documentation_suite node with stability 0.85; embedding triggered\n * automatically by trg_mcorch_embed_on_insert (pg_net).\n *\n * Inserts an explicit DERIVES_FROM edge to the parent seal (marketing-hub v1 \u2014\n * viral-autopilot is the autonomous orchestrator built ON TOP of the marketing-hub\n * campaign executor / content + affiliate domain).\n *\n * Usage: bun run scripts/seed-viral-autopilot-bok-seal.ts\n */\nimport { createClient } from '@supabase/supabase-js';\n\nconst SUPABASE_URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL;\nconst SERVICE_KEY = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY);\n\nif (!SUPABASE_URL || !SERVICE_KEY) {\n  console.error('Missing SUPABASE_URL or SB_SECRET_KEY');\n  process.exit(1);\n}\n\nconst supabase = createClient(SUPABASE_URL, SERVICE_KEY);\n\nconst PARENT_SEAL_NAME = 'bok-scribe-seal-marketing-hub-v1';\n\nconst sealNode = {\n  name: 'bok-scribe-seal-viral-autopilot-v1',\n  node_type: 'documentation_suite',\n  project_id: 'viral-autopilot',\n  stability_score: 0.85,\n  revenue_impact: 1000000, // direct-revenue engine \u2014 motor aut\u00f4nomo de conte\u00fado viral monetizado por afiliado ML (Million-BRL Roadmap anchor); receita real gated em postback comprovado (FMEA-VA-006 / OTD-VA-007)\n  content: `viral-autopilot \u2014 Motor de conte\u00fado viral aut\u00f4nomo monetizado por afiliado ML (BoK v1)\n\nBoK suite (9 docs, 1722 LOC) sealed 2026-06-17 sob MCORCH Master Execution Protocol. Motivada pela diretiva do Sovereign de retomar o objetivo-n\u00facleo do produto (\"alimentar contas de redes sociais com conte\u00fado viral gerado automaticamente e agendado, podendo gerar tudo de uma vez OU a cada 3 dias mediante an\u00e1lise do que foi feito antes para melhorar os pr\u00f3ximos criativos, para conte\u00fados virais com comiss\u00e3o do Mercado Livre\"). Precedida de auditoria material de 7 agentes (2026-06-17) que provou, com prova path:linha, o estado real de cada requisito. Decis\u00f5es de escopo travadas via AskUserQuestion: BoK suite NOVO viral-autopilot (n\u00e3o emenda nem override); MVP = texto+imagem nas redes atuais (WP/LinkedIn/X), v\u00eddeo+TikTok/IG/YT fase 2; sinal R3 = combo (cliques afiliado + engajamento org\u00e2nico + receita postback); 3 SKUs semente (Roborock S8 / Samsung Neo QLED 8K / Family Hub).\n\nVIS\u00c3O: piloto-autom\u00e1tico de conte\u00fado que, a partir de um produto-alvo, gera criativos product-aware monetizados, publica em cad\u00eancia configur\u00e1vel (tudo-de-uma-vez OU a cada N dias, default 3) e \u2014 diferencial central \u2014 FECHA O LOOP: cada ciclo ingere o desempenho real do ciclo anterior e realimenta os pr\u00f3ximos criativos, dentro de um teto de custo em mcoCoins. \u00c9 o orquestrador de ciclo que costura pe\u00e7as j\u00e1 vivas do MCORCH (orchestrate-content/orchestrate-step, _shared/affiliate.ts, affiliate_config per-user, click ledger, handle-ml-postback) num loop fechado \u2014 n\u00e3o reinventa gera\u00e7\u00e3o nem receita.\n\nGAP FECHADO (vs auditoria): R1 (gera\u00e7\u00e3o auto) parcial\u2192FR de gera\u00e7\u00e3o product-aware (FR-VA-003) + imagem MVP (FR-VA-013); R2 (cad\u00eancia) AUSENTE\u2192entidade autopilot_plans (mode+interval_days) + cron auto-refill autopilot-cadence (FR-VA-001/005/006) \u2014 fecha \"recorr\u00eancia n\u00e3o existe\"; R3 (loop auto-melhor\u00e1vel) AUSENTE\u2192fecha as 3 quebras: coletor creative_metrics (FR-VA-008/009) resolve campaign_metrics sem writer, feedback-inject (FR-VA-011) resolve optimization_policy nunca lida, cron+analyze agendado (FR-VA-005/010) resolve self-optimize sem cron \u2014 com guarda anti \"auto-melhoria teatral\" (has_real_data=false \u2192 baseline, n\u00e3o inventa); R4 (afiliado ML) parcial\u2192monetize TODO formato com content_variant_id (FR-VA-004) + honra param dropado (FR-VA-016) + sele\u00e7\u00e3o comiss\u00e3o+trend (FR-VA-012).\n\nARQUITETURA: 3 tabelas novas (autopilot_plans, autopilot_cycles, creative_metrics) + ALTER scheduled_posts (+cycle_id) + 4 edge functions novas (autopilot-run, autopilot-cadence-cron, autopilot-analyze, autopilot-collect) + 4 edge functions modificadas (orchestrate-content honra produto, orchestrate-step product-aware+feedback-inject, _shared/affiliate.ts monetiza todo formato, generate-image plugado ao ciclo) + 2 pg_cron (autopilot-cadence */15 auto-refill, autopilot-collect 6/6h). CISSP CBK: STRIDE 8 amea\u00e7as com mitiga\u00e7\u00e3o (kill-switch at\u00f4mico antes do deduct, RLS own-row default-deny, Cyber-Sentinel anti-prompt-injection no produto/trend, guarda de dom\u00ednio ML no link); API Tenancy per-user (auth.uid()) obrigat\u00f3ria; SB_SECRET_KEY (legada revogada). Reusa primitiva de cad\u00eancia do nurturing (sequence_enrollments.next_run_at + pg_cron + fan-out service-role) generalizada para auto-refill de conte\u00fado.\n\nID SPACE: MR-VA-001..008 \u00b7 BR-VA-001..008 \u00b7 BO-001..004 \u00b7 SH-001..005 \u00b7 PR-VA-001..022 \u00b7 FR-VA-001..018 \u00b7 NFR-VA-001..008 \u00b7 PROC-VA-001..005 \u00b7 KPI-VA-001..008 \u00b7 FMEA-VA-001..012 \u00b7 SOL-VA-001..005 \u00b7 QO-001..004 \u00b7 BAC-001..005 \u00b7 OTD-VA-001..007.\n\nFMEA (12 entries, 4 RPN > 100): FMEA-VA-002 (RPN 180 \u2014 auto-melhoria teatral: analisa creative_metrics vazia; a\u00e7\u00e3o: bloquear quando vazio, cliques de afiliado como sinal m\u00ednimo, flag has_real_data), FMEA-VA-004 (RPN 135 \u2014 conte\u00fado aut\u00f4nomo off-brand/viola ToS; a\u00e7\u00e3o: Cyber-Sentinel gate pr\u00e9-publica\u00e7\u00e3o + disclosure afiliado + HITL opcional), FMEA-VA-001 (RPN 128 \u2014 overspend aut\u00f4nomo/bypass do teto; a\u00e7\u00e3o: gate at\u00f4mico antes do deduct + idempot\u00eancia + safety cap di\u00e1rio), FMEA-VA-005 (RPN 120 \u2014 prompt injection via nome de produto/trend; a\u00e7\u00e3o: sanitizar + Cyber-Sentinel input/output).\n\nDOCUMENTOS: docs/bok/viral-autopilot/{00-index 104, 01-mrd 133, 02-brd 158, 03-prd 214, 04-frd 181, 05-sdd 334, 06-data-model 208, 07-process-flow 217, 08-quality-metrics 173} \u2014 total 1722 LOC.\n\nTRACEABILITY: 100% MR \u2192 BR \u2192 PR \u2192 FR (zero orphans). PRs de Future/Fase-2 (PR-VA-020..022 v\u00eddeo/TikTok/auto-discovery) intencionalmente diferidos. Parent seal marketing-hub (viral-autopilot \u00e9 o orquestrador aut\u00f4nomo sobre o campaign executor + dom\u00ednio conte\u00fado/afiliado).\n\nBoK GATE: liberado AP\u00d3S este seal. C\u00f3digo de produ\u00e7\u00e3o s\u00f3 inicia depois das migrations com /security-review aprovado. Rota de implementa\u00e7\u00e3o (8 passos, do maior alavancagem): (1) este seal; (2) gera\u00e7\u00e3o product-aware + monetize todo formato; (3) reconectar fetch-trends/vm_affiliate_products \u00e0 pauta; (4) cad\u00eancia 3 dias (generalizar nurture); (5) coletor de engajamento; (6) fechar loop R3; (7) m\u00eddia viral (fase 2); (8) provar postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER).`,\n  metadata: {\n    bok_version: '1.0.0',\n    documents: [\n      '00-index',\n      '01-mrd',\n      '02-brd',\n      '03-prd',\n      '04-frd',\n      '05-sdd',\n      '06-data-model',\n      '07-process-flow',\n      '08-quality-metrics',\n    ],\n    document_lines: {\n      '00-index': 104,\n      '01-mrd': 133,\n      '02-brd': 158,\n      '03-prd': 214,\n      '04-frd': 181,\n      '05-sdd': 334,\n      '06-data-model': 208,\n      '07-process-flow': 217,\n      '08-quality-metrics': 173,\n      total: 1722,\n    },\n    phase_completed: 'Phase 7',\n    traceability_validated: true,\n    traceability_orphans: 0,\n    bok_gate: 'fresh-completion',\n    drift_reconciled: 0,\n    drift_pending: 0,\n    market_segment: 'B2B2C',\n    monetization_model: 'hybrid',\n    regulatory_profile: 'LGPD',\n    integration_surface: 'extends-mcorch',\n    project_slug: 'viral-autopilot',\n    sprint_introduced: 'v6.42.0',\n    sprint_sealed: 'pending-handoff',\n    tags: ['bok-scribe', 'viral-autopilot', 'B2B2C', 'agentic', 'content-engine', 'scheduling', 'cadence', 'self-improving-loop', 'mercado-livre', 'affiliate', 'attribution', 'lgpd', 'per-user-tenancy', 'autonomous'],\n    modules: [\n      'Autopilot Plan (cad\u00eancia configur\u00e1vel per-user)',\n      'Product-aware Generation (texto+imagem monetizado)',\n      'Cadence Scheduler (cron auto-refill a cada N dias)',\n      'Performance Collector (cliques + org\u00e2nico + receita \u2192 creative_metrics)',\n      'Self-Improvement Feedback (analyze \u2192 optimization_policy \u2192 reinject)',\n      'Cost Guardrail (teto por ciclo + kill-switch)',\n    ],\n    new_tables: 3, // autopilot_plans, autopilot_cycles, creative_metrics\n    new_views: 0,\n    new_columns: 1, // scheduled_posts.cycle_id\n    new_edge_functions: 4, // autopilot-run, autopilot-cadence-cron, autopilot-analyze, autopilot-collect\n    extended_edge_functions: 4, // orchestrate-content, orchestrate-step, _shared/affiliate.ts, generate-image\n    new_rpcs: 0, // reuses deduct_mco_coins\n    new_crons: 2, // autopilot-cadence (*/15), autopilot-collect (6/6h)\n    new_migrations: 4,\n    requirements_closed: { R1: 'partial\u2192FR-VA-003/013', R2: 'absent\u2192FR-VA-001/005/006', R3: 'absent\u2192FR-VA-008/009/010/011', R4: 'partial\u2192FR-VA-004/012/016' },\n    id_ranges: {\n      MR: '001..008',\n      BR: '001..008',\n      BO: '001..004',\n      SH: '001..005',\n      PR: '001..022',\n      FR: '001..018',\n      NFR: '001..008',\n      PROC: '001..005',\n      KPI: '001..008',\n      FMEA: '001..012',\n      SOL: '001..005',\n      QO: '001..004',\n      BAC: '001..005',\n      OTD: '001..007',\n    },\n    fmea_rpn_over_100: ['FMEA-VA-001', 'FMEA-VA-002', 'FMEA-VA-004', 'FMEA-VA-005'],\n    fmea_rpn_top: {\n      'FMEA-VA-002': 180,\n      'FMEA-VA-004': 135,\n      'FMEA-VA-001': 128,\n      'FMEA-VA-005': 120,\n    },\n    derives_from: PARENT_SEAL_NAME,\n    motivating_incident: 'Sovereign directive \u2014 retomar objetivo-n\u00facleo (conte\u00fado viral aut\u00f4nomo + comiss\u00e3o ML); precedida de auditoria material de 7 agentes (2026-06-17)',\n    revenue_impact_basis: 'autonomous-viral-affiliate-content-engine (Million-BRL Roadmap anchor; receita real gated em postback ML comprovado \u2014 FMEA-VA-006/OTD-VA-007)',\n    reuses: ['orchestrate-content', 'orchestrate-step', '_shared/affiliate.ts', 'affiliate_config (per-user)', 'process-affiliate-link', 'handle-ml-postback', 'click ledger record_affiliate_click', 'vm_affiliate_products', 'fetch-trends/vm_trends', 'scheduled_posts + auto-publish', 'sequence_enrollments cadence primitive', 'self-optimize/optimization_policy', 'deduct_mco_coins RPC', 'ROIWidget', 'mcorch_nodes/edges', 'Cyber-Sentinel'],\n    references_suites: ['mercado-livre-api (FR-ML-001..012)', 'post-engine (FR-PE-001..004)', 'viral-daily-canvas (FR-VDC-001..004)', 'viralmind (FR-024..026)', 'marketing-hub (FR-MH-004)'],\n    related_otds: ['OTD-VA-001', 'OTD-VA-002', 'OTD-VA-003', 'OTD-VA-004', 'OTD-VA-005', 'OTD-VA-006', 'OTD-VA-007', 'OTD-ML-MP-PER-USER'],\n    sovereign_decisions: {\n      bok_gate: 'new-suite (not amend, not override)',\n      mvp_scope: 'text+image on current networks (WP/LinkedIn/X); video+TikTok/IG/YT = phase 2',\n      r3_signal: 'combo (affiliate clicks + organic engagement + ML postback revenue)',\n      products: '3 seed SKUs (Roborock S8, Samsung Neo QLED 8K, Family Hub); auto-discovery deferred to v1.0',\n    },\n    next_step: 'Implementa\u00e7\u00e3o fatia 1: gera\u00e7\u00e3o product-aware + monetize todo formato (FR-VA-003/004/016) com migrations /security-review',\n    skips: ['Video creative 9:16 (phase 2)', 'TikTok/Instagram/YouTube publishing (phase 2)', 'Paid ads management', 'Multi-touch cross-network attribution dedup', 'Catalog auto-discovery cron (PR-VA-022, v1.0)'],\n  },\n};\n\nconsole.log(`\ud83d\udcdd Sealing BoK suite \"viral-autopilot\"...`);\nconsole.log(`   Project: ${sealNode.project_id}`);\nconsole.log(`   Stability: ${sealNode.stability_score}`);\nconsole.log(`   Revenue impact: ${sealNode.revenue_impact} (${sealNode.metadata.monetization_model})`);\nconsole.log(`   BoK gate: ${sealNode.metadata.bok_gate}`);\nconsole.log(`   Parent (DERIVES_FROM): ${PARENT_SEAL_NAME}`);\n\n// Idempotency check: skip if already exists\nconst { data: existing } = await supabase\n  .from('mcorch_nodes')\n  .select('id, name, created_at')\n  .eq('name', sealNode.name)\n  .maybeSingle();\n\nif (existing) {\n  console.log(`\\n\u26a0\ufe0f Seal node already exists (idempotent skip):`);\n  console.log(`   ID:        ${existing.id}`);\n  console.log(`   Name:      ${existing.name}`);\n  console.log(`   Created:   ${existing.created_at}`);\n  console.log(`\\nNo new INSERT performed.`);\n  process.exit(0);\n}\n\n// Step 1: INSERT documentation_suite node\nconst { data: insertedNode, error: nodeError } = await supabase\n  .from('mcorch_nodes')\n  .insert(sealNode)\n  .select('id, name, node_type, stability_score, created_at')\n  .single();\n\nif (nodeError) {\n  console.error('\u274c Seal node insert failed:', nodeError);\n  process.exit(1);\n}\n\nconsole.log(`\\n\u2705 Seal node inserted:`);\nconsole.log(`   ID:        ${insertedNode.id}`);\nconsole.log(`   Name:      ${insertedNode.name}`);\nconsole.log(`   Type:      ${insertedNode.node_type}`);\nconsole.log(`   Stability: ${insertedNode.stability_score}`);\nconsole.log(`   Created:   ${insertedNode.created_at}`);\n\n// Step 2: Resolve parent seal UUID for DERIVES_FROM edge\nconst { data: parent, error: parentError } = await supabase\n  .from('mcorch_nodes')\n  .select('id, name')\n  .eq('name', PARENT_SEAL_NAME)\n  .single();\n\nif (parentError || !parent) {\n  console.error(`\\n\u274c Parent seal lookup failed for ${PARENT_SEAL_NAME}:`, parentError);\n  console.error('   Skipping DERIVES_FROM edge insert. Manual cleanup may be required.');\n  process.exit(1);\n}\n\nconsole.log(`\\n\ud83d\udd17 Parent seal resolved:`);\nconsole.log(`   ID:        ${parent.id}`);\nconsole.log(`   Name:      ${parent.name}`);\n\n// Step 3: INSERT DERIVES_FROM edge\nconst { data: insertedEdge, error: edgeError } = await supabase\n  .from('mcorch_edges')\n  .insert({\n    source_id: insertedNode.id,\n    target_id: parent.id,\n    relation_type: 'DERIVES_FROM',\n    weight: 1.0,\n    project_id: 'viral-autopilot',\n    metadata: {\n      lineage: 'bok-scribe-seal',\n      source_seal: insertedNode.name,\n      target_seal: parent.name,\n      sealed_at: insertedNode.created_at,\n    },\n  })\n  .select('id, source_id, target_id, relation_type, created_at')\n  .single();\n\nif (edgeError) {\n  console.error('\u274c DERIVES_FROM edge insert failed:', edgeError);\n  process.exit(1);\n}\n\nconsole.log(`\\n\u2705 DERIVES_FROM edge inserted:`);\nconsole.log(`   ID:        ${insertedEdge.id}`);\nconsole.log(`   Source:    ${insertedEdge.source_id} (${insertedNode.name})`);\nconsole.log(`   Target:    ${insertedEdge.target_id} (${parent.name})`);\nconsole.log(`   Relation:  ${insertedEdge.relation_type}`);\nconsole.log(`   Created:   ${insertedEdge.created_at}`);\n\nconsole.log(`\\n\ud83e\udde0 Embedding will be generated automatically by trg_mcorch_embed_on_insert (ass\u00edncrono via pg_net).`);\nconsole.log(`   Confirm with: SELECT embedding IS NOT NULL FROM mcorch_nodes WHERE id = '${insertedNode.id}';`);\nconsole.log(`\\n\ud83d\udcca Material proof summary for handoff:`);\nconsole.log(`   - documentation_suite node UUID: ${insertedNode.id}`);\nconsole.log(`   - DERIVES_FROM edge UUID:        ${insertedEdge.id}`);\nconsole.log(`   - Parent seal UUID:              ${parent.id}`);\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/scripts/seed-viral-autopilot-bok-seal.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:10:58)*


## 🤖 Claude *(21:11:03)*

Seed script da Fase 7 pronto (espelha o padrão `marketing-hub`: idempotente + insere nó `documentation_suite` + aresta `DERIVES_FROM` → `marketing-hub`). **Não vou executá-lo até o veredito GO** da validação adversarial.

Status atual:
- ✅ **9 documentos BoK** autorados em `docs/bok/viral-autopilot/` (1722 LOC) — manifesto + MRD + BRD + PRD + FRD + SDD + data-model + process-flow + quality-metrics
- ✅ **Seed script** `scripts/seed-viral-autopilot-bok-seal.ts` pronto (aguarda GO)
- ⏳ **Validação adversarial** (4 críticos + síntese) rodando em background — `/workflows` para acompanhar

Quando a validação retornar, aplico os must-fixes (se houver), executo o seal sob aprovação e fecho o BoK Gate. Aguardando a conclusão do workflow.

## 👤 User *(21:18:21)*

<task-notification>
<task-id>wql8i8sh7</task-id>
<tool-use-id>toolu_014KnFDvUG8z3yTim347BZSh</tool-use-id>
<output-file>/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/tasks/wql8i8sh7.output</output-file>
<status>completed</status>
<summary>Dynamic workflow "Phase 6 adversarial validation of the viral-autopilot BoK suite: traceability integrity, security/Harness constraints, R1-R4 gap-closure coverage, template/FMEA completeness → GO/NO-GO verdict with must-fix list" completed</summary>
<result>{"critiques":[{"dimension":"Rastreabilidade (MR-VA → BR-VA → PR-VA → FR-VA → artefato)","verdict":"fail","findings":[{"id":"TRACE-01","severity":"high","doc":"03-prd.md §8 vs 02-brd.md §10 (matrizes MR→PR)","issue":"As matrizes MR→PR dos dois docs NÃO são mutuamente consistentes. BRD §10 mapeia MR-VA-003→{PR-VA-004,PR-VA-005}, MR-VA-004→{PR-VA-002}, MR-VA-008→{PR-VA-010,PR-VA-011}. O PRD §8 adiciona silenciosamente PR-VA-012 a MR-VA-003, PR-VA-013 a MR-VA-004 e PR-VA-022 a MR-VA-008. Mesma cadeia, três células divergentes — não dá pra saber qual matriz é a fonte da verdade.","fix":"Reconciliar as duas matrizes para serem idênticas. Como PR-VA-012/013/022 são features Should/Could que de fato rastreiam essas MRs (ver PRD §4 BR-Traced), atualizar a BRD §10 para incluí-las, OU anotar explicitamente que a BRD §10 lista só o escopo MVP e o PRD §8 o escopo completo."},{"id":"TRACE-02","severity":"high","doc":"00-index.md §'Traceability Chain (summary)'","issue":"O resumo de cadeia do índice contradiz as matrizes downstream. (a) Linha MR-VA-001 mostra 'BR-VA-001 ──▶ PR-VA-002 ──▶ FR-VA-003, FR-VA-013', omitindo PR-VA-008 que BRD §10 e PRD §8 listam para MR-VA-001. (b) Atribui FR-VA-013 a PR-VA-002, mas FR-VA-013 rastreia PR-VA-008 (FRD §2 e §7). O índice cria uma ligação PR-VA-002→FR-VA-013 que não existe em nenhuma outra matriz.","fix":"Corrigir a cadeia do índice: MR-VA-001 → BR-VA-001 → PR-VA-002, PR-VA-008 → (PR-VA-002→FR-VA-003) e (PR-VA-008→FR-VA-013). Tratar o índice como visão derivada e regenerá-lo das matrizes autoritativas, não escrevê-lo à mão."},{"id":"TRACE-03","severity":"high","doc":"04-frd.md (FR-VA-010) vs 05-sdd.md §2.5 + 07-process-flow.md §1/§7","issue":"O acionador do FR-VA-010 (autopilot-analyze) — motor do loop R3, o diferencial central do produto — é contraditório e sem artefato. A FRD diz 'Generaliza self-optimize, agora AGENDADO', implicando cron próprio. Mas SDD §2.5 e process-flow §7 declaram APENAS 2 crons (autopilot-cadence, autopilot-collect); não há cron de análise. Process-flow PROC-VA-005 tipa a análise como 'automated / pós-ciclo (encadeado a PROC-VA-001)', não agendada. SDD §3 também a desenha como '(post-cycle)' inline. FR crítico-de-valor sem trigger consistente nem artefato cron.","fix":"Decidir e cravar o acionador em UM lugar: ou (a) autopilot-analyze é chamado in-line ao fim de cada ciclo do autopilot-cadence-cron — então corrigir a FRD FR-VA-010 para remover 'agendado' e dizer 'encadeado pós-ciclo'; ou (b) é um 3º cron — então adicioná-lo a SDD §2.5, §6 e process-flow §7 (hoje a doc afirma '2 crons' em 3 lugares)."},{"id":"TRACE-04","severity":"medium","doc":"03-prd.md §4 (PR-VA-004) vs §8/02-brd.md §10 (matrizes MR-VA-005/BR-VA-005)","issue":"Inconsistência de rastreio de BR-VA-005. No PRD §4 o feature PR-VA-004 (Performance collector) declara BR-Traced='BR-VA-005, BR-VA-003'. Porém todas as matrizes MR→BR→PR mapeiam BR-VA-005 (MR-VA-005) SÓ para PR-VA-007 — PR-VA-004 não aparece sob MR-VA-005 em lugar nenhum. Ou PR-VA-004 rastreia BR-VA-005 (e a matriz MR-VA-005 deveria listá-lo) ou não rastreia (e o BR-Traced do feature está errado).","fix":"Decidir: se o coletor (PR-VA-004) serve BR-VA-005 (métricas por criativo), adicionar PR-VA-004 à célula MR-VA-005 nas matrizes BRD §10 e PRD §8. Caso contrário, remover BR-VA-005 do BR-Traced de PR-VA-004 em PRD §4 (deixando só BR-VA-003)."},{"id":"TRACE-05","severity":"medium","doc":"04-frd.md §2 (linha FR-VA-016) vs §7 (matriz PR→FR)","issue":"FR-VA-016 (honor product/affiliate param) tem PR-Traced inconsistente entre as duas tabelas do próprio FRD: a tabela §2 lista FR-VA-016 → 'PR-VA-002' (apenas); a matriz reversa §7 lista FR-VA-016 sob AMBOS PR-VA-001 e PR-VA-002. Um FR não pode rastrear 1 PR numa tabela e 2 na outra dentro do mesmo documento.","fix":"Alinhar: se FR-VA-016 atende tanto a entidade de plano (PR-VA-001) quanto a geração product-aware (PR-VA-002), atualizar a coluna PR Traced da §2 para 'PR-VA-001, PR-VA-002'. Senão, remover FR-VA-016 da linha PR-VA-001 em §7."},{"id":"TRACE-06","severity":"high","doc":"03-prd.md §8 vs 04-frd.md §7 (PR-VA-012, PR-VA-013)","issue":"IDs de PR órfãos a jusante. PR-VA-012 (A/B variant) e PR-VA-013 (HITL gate) são v1.0 'Should Have', aparecem na matriz PRD §8 (sob MR-VA-003 e MR-VA-004 respectivamente) e em PRD §4, MAS estão totalmente ausentes da matriz PR→FR da FRD §7 e nenhum FR os rastreia (grep confirma 0 ocorrências em 04-frd.md). A cadeia MR-VA-003→...→PR-VA-012 e MR-VA-004→...→PR-VA-013 termina em beco sem FR. Como o escopo v1.0 está In-scope na FRD §1, esses PRs deveriam ter FR.","fix":"Ou criar FRs para PR-VA-012 (ex.: FR de geração de N variantes + seleção por desempenho) e PR-VA-013 (FR de gate HITL reusando policy-engine do intent-execute) e adicioná-los à matriz §7; ou, se forem deferidos para além do v1.0 documentado, removê-los das células de rastreio MR-VA-003/004 do PRD §8 e marcá-los Future."},{"id":"TRACE-07","severity":"medium","doc":"03-prd.md §8 vs 04-frd.md §7 (PR-VA-022 e PR-VA-020/021)","issue":"Tratamento inconsistente dos PRs 'Could/Fase 2'. PR-VA-022 aparece na matriz autoritativa PRD §8 (célula MR-VA-008) porém sem nenhum FR em FRD §7 — cadeia que morre num PR sem artefato. Já PR-VA-020 e PR-VA-021 (mesma categoria Could) NÃO aparecem em PRD §8 nem em FRD §7, apesar de definidos em PRD §4 com BR-Traced=BR-VA-001. Logo, 3 PRs Fase-2 recebem tratamento de rastreio divergente entre si.","fix":"Uniformizar: ou os 3 PRs de Fase 2 (020/021/022) ficam fora de todas as matrizes de rastreio (são Could/Won't) com nota explícita, ou todos entram com FR-stubs Fase-2. Remover PR-VA-022 da célula MR-VA-008 do PRD §8 se a decisão for mantê-lo só como Future."},{"id":"TRACE-08","severity":"high","doc":"06-data-model.md §2/§3 + 04-frd.md §5 + 05-sdd.md §7","issue":"Chave de junção load-bearing 'content_variant_id' sem artefato de origem. FR-VA-004/009/017 (monetização, métricas, atribuição de receita) todos chaveiam em content_variant_id; FRD §5 e data-model §2 declaram 'FK → criativo/content_library'. Porém NENHUM doc define onde esse content_variant_id é criado: grep de 'ADD COLUMN'/'ALTER TABLE' mostra que só scheduled_posts.cycle_id é adicionado — content_library nunca recebe a coluna content_variant_id, e nenhuma tabela nova a produz. A cadeia FR-VA-004/009/017 → tabela tem o alvo da FK inexistente.","fix":"Documentar a origem de content_variant_id: ou ALTER TABLE content_library ADD COLUMN content_variant_id uuid (+ onde a geração o popula por criativo), ou definir que é o próprio id de content_library e renomear o FK accordingly. Adicionar o stub na SDD §7 e a coluna no data-model §2."},{"id":"TRACE-09","severity":"medium","doc":"04-frd.md §2 (FR-VA-013 'Should (MVP)') vs 03-prd.md §4/§5 e 00-index.md §Decisão 2","issue":"Contradição de prioridade na feature que DEFINE o MVP. Index/BRD/PRD afirmam em três lugares 'MVP = TEXTO + IMAGEM'. PR-VA-008 (Image creative), pai de FR-VA-013, está em 'Must Have (MVP)' no PRD §4 e incluído no escopo MVP do PRD §5. Mas o FR que o realiza, FR-VA-013, é marcado 'Should (MVP)' (e prioridade textual divergente das demais que usam Critical/High). Um FR 'Should' sob um PR 'Must' que é a metade 'imagem' do MVP é incoerente.","fix":"Elevar FR-VA-013 para 'High' ou 'Critical' (consistente com o PR Must PR-VA-008 e com 'MVP=texto+imagem'), ou rebaixar PR-VA-008 e o claim de MVP. Padronizar a coluna Priority do FRD (usar a mesma escala Critical/High/Medium das outras FRs, não 'Should (MVP)')."}],"notes":"Verifiquei as 4 matrizes (01 §9, 02 §10, 03 §8, 04 §7) + índice (00) + downstream (05 SDD, 06 data-model, 07 process-flow, 08 quality). Cobertura base OK: os 8 MR rastreiam BR 1:1; cada BR tem ≥1 PR; cada PR Must/Should tem PR-Traced; FR-VA-001..018 todos rastreiam ≥1 PR na tabela §2 e têm artefato (tabela/edge fn/cron) no SDD/data-model. Os 5 PROC do 07 cobrem os FRs críticos de geração/cadência/custo (FR-VA-002/005/007), MAS o FR crítico-de-valor FR-VA-010/011 (loop R3) tem tr
... (truncated 46887 chars, full result in /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/tasks/wql8i8sh7.output)</result>
<usage><agent_count>5</agent_count><subagent_tokens>601296</subagent_tokens><tool_uses>76</tool_uses><duration_ms>560395</duration_ms></usage>
</task-notification>

## 🤖 Claude *(21:18:26)*

A validação adversarial encontrou inconsistências reais (não cosméticas). Vou ler o resultado completo — críticos de segurança/gap-closure/completude + o veredito final GO/NO-GO:

## 🤖 Claude *(21:18:27)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/tasks/wql8i8sh7.output",
  "offset": 1,
  "limit": 60
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	{
> 2	  "summary": "Phase 6 adversarial validation of the viral-autopilot BoK suite: traceability integrity, security/Harness constraints, R1-R4 gap-closure coverage, template/FMEA completeness → GO/NO-GO verdict with must-fix list",
> 3	  "agentCount": 5,
> 4	  "logs": [
> 5	    "4 críticos adversariais lendo os 9 docs da suíte viral-autopilot...",
> 6	    "Sintetizando veredito GO/NO-GO..."
> 7	  ],
> 8	  "result": {
> 9	    "critiques": [
> 10	      {
> 11	        "dimension": "Rastreabilidade (MR-VA → BR-VA → PR-VA → FR-VA → artefato)",
> 12	        "verdict": "fail",
> 13	        "findings": [
> 14	          {
> 15	            "id": "TRACE-01",
> 16	            "severity": "high",
> 17	            "doc": "03-prd.md §8 vs 02-brd.md §10 (matrizes MR→PR)",
> 18	            "issue": "As matrizes MR→PR dos dois docs NÃO são mutuamente consistentes. BRD §10 mapeia MR-VA-003→{PR-VA-004,PR-VA-005}, MR-VA-004→{PR-VA-002}, MR-VA-008→{PR-VA-010,PR-VA-011}. O PRD §8 adiciona silenciosamente PR-VA-012 a MR-VA-003, PR-VA-013 a MR-VA-004 e PR-VA-022 a MR-VA-008. Mesma cadeia, três células divergentes — não dá pra saber qual matriz é a fonte da verdade.",
> 19	            "fix": "Reconciliar as duas matrizes para serem idênticas. Como PR-VA-012/013/022 são features Should/Could que de fato rastreiam essas MRs (ver PRD §4 BR-Traced), atualizar a BRD §10 para incluí-las, OU anotar explicitamente que a BRD §10 lista só o escopo MVP e o PRD §8 o escopo completo."
> 20	          },
> 21	          {
> 22	            "id": "TRACE-02",
> 23	            "severity": "high",
> 24	            "doc": "00-index.md §'Traceability Chain (summary)'",
> 25	            "issue": "O resumo de cadeia do índice contradiz as matrizes downstream. (a) Linha MR-VA-001 mostra 'BR-VA-001 ──▶ PR-VA-002 ──▶ FR-VA-003, FR-VA-013', omitindo PR-VA-008 que BRD §10 e PRD §8 listam para MR-VA-001. (b) Atribui FR-VA-013 a PR-VA-002, mas FR-VA-013 rastreia PR-VA-008 (FRD §2 e §7). O índice cria uma ligação PR-VA-002→FR-VA-013 que não existe em nenhuma outra matriz.",
> 26	            "fix": "Corrigir a cadeia do índice: MR-VA-001 → BR-VA-001 → PR-VA-002, PR-VA-008 → (PR-VA-002→FR-VA-003) e (PR-VA-008→FR-VA-013). Tratar o índice como visão derivada e regenerá-lo das matrizes autoritativas, não escrevê-lo à mão."
> 27	          },
> 28	          {
> 29	            "id": "TRACE-03",
> 30	            "severity": "high",
> 31	            "doc": "04-frd.md (FR-VA-010) vs 05-sdd.md §2.5 + 07-process-flow.md §1/§7",
> 32	            "issue": "O acionador do FR-VA-010 (autopilot-analyze) — motor do loop R3, o diferencial central do produto — é contraditório e sem artefato. A FRD diz 'Generaliza self-optimize, agora AGENDADO', implicando cron próprio. Mas SDD §2.5 e process-flow §7 declaram APENAS 2 crons (autopilot-cadence, autopilot-collect); não há cron de análise. Process-flow PROC-VA-005 tipa a análise como 'automated / pós-ciclo (encadeado a PROC-VA-001)', não agendada. SDD §3 também a desenha como '(post-cycle)' inline. FR crítico-de-valor sem trigger consistente nem artefato cron.",
> 33	            "fix": "Decidir e cravar o acionador em UM lugar: ou (a) autopilot-analyze é chamado in-line ao fim de cada ciclo do autopilot-cadence-cron — então corrigir a FRD FR-VA-010 para remover 'agendado' e dizer 'encadeado pós-ciclo'; ou (b) é um 3º cron — então adicioná-lo a SDD §2.5, §6 e process-flow §7 (hoje a doc afirma '2 crons' em 3 lugares)."
> 34	          },
> 35	          {
> 36	            "id": "TRACE-04",
> 37	            "severity": "medium",
> 38	            "doc": "03-prd.md §4 (PR-VA-004) vs §8/02-brd.md §10 (matrizes MR-VA-005/BR-VA-005)",
> 39	            "issue": "Inconsistência de rastreio de BR-VA-005. No PRD §4 o feature PR-VA-004 (Performance collector) declara BR-Traced='BR-VA-005, BR-VA-003'. Porém todas as matrizes MR→BR→PR mapeiam BR-VA-005 (MR-VA-005) SÓ para PR-VA-007 — PR-VA-004 não aparece sob MR-VA-005 em lugar nenhum. Ou PR-VA-004 rastreia BR-VA-005 (e a matriz MR-VA-005 deveria listá-lo) ou não rastreia (e o BR-Traced do feature está errado).",
> 40	            "fix": "Decidir: se o coletor (PR-VA-004) serve BR-VA-005 (métricas por criativo), adicionar PR-VA-004 à célula MR-VA-005 nas matrizes BRD §10 e PRD §8. Caso contrário, remover BR-VA-005 do BR-Traced de PR-VA-004 em PRD §4 (deixando só BR-VA-003)."
> 41	          },
> 42	          {
> 43	            "id": "TRACE-05",
> 44	            "severity": "medium",
> 45	            "doc": "04-frd.md §2 (linha FR-VA-016) vs §7 (matriz PR→FR)",
> 46	            "issue": "FR-VA-016 (honor product/affiliate param) tem PR-Traced inconsistente entre as duas tabelas do próprio FRD: a tabela §2 lista FR-VA-016 → 'PR-VA-002' (apenas); a matriz reversa §7 lista FR-VA-016 sob AMBOS PR-VA-001 e PR-VA-002. Um FR não pode rastrear 1 PR numa tabela e 2 na outra dentro do mesmo documento.",
> 47	            "fix": "Alinhar: se FR-VA-016 atende tanto a entidade de plano (PR-VA-001) quanto a geração product-aware (PR-VA-002), atualizar a coluna PR Traced da §2 para 'PR-VA-001, PR-VA-002'. Senão, remover FR-VA-016 da linha PR-VA-001 em §7."
> 48	          },
> 49	          {
> 50	            "id": "TRACE-06",
> 51	            "severity": "high",
> 52	            "doc": "03-prd.md §8 vs 04-frd.md §7 (PR-VA-012, PR-VA-013)",
> 53	            "issue": "IDs de PR órfãos a jusante. PR-VA-012 (A/B variant) e PR-VA-013 (HITL gate) são v1.0 'Should Have', aparecem na matriz PRD §8 (sob MR-VA-003 e MR-VA-004 respectivamente) e em PRD §4, MAS estão totalmente ausentes da matriz PR→FR da FRD §7 e nenhum FR os rastreia (grep confirma 0 ocorrências em 04-frd.md). A cadeia MR-VA-003→...→PR-VA-012 e MR-VA-004→...→PR-VA-013 termina em beco sem FR. Como o escopo v1.0 está In-scope na FRD §1, esses PRs deveriam ter FR.",
> 54	            "fix": "Ou criar FRs para PR-VA-012 (ex.: FR de geração de N variantes + seleção por desempenho) e PR-VA-013 (FR de gate HITL reusando policy-engine do intent-execute) e adicioná-los à matriz §7; ou, se forem deferidos para além do v1.0 documentado, removê-los das células de rastreio MR-VA-003/004 do PRD §8 e marcá-los Future."
> 55	          },
> 56	          {
> 57	            "id": "TRACE-07",
> 58	            "severity": "medium",
> 59	            "doc": "03-prd.md §8 vs 04-frd.md §7 (PR-VA-022 e PR-VA-020/021)",
> 60	            "issue": "Tratamento inconsistente dos PRs 'Could/Fase 2'. PR-VA-022 aparece na matriz autoritativa PRD §8 (célula MR-VA-008) porém sem nenhum FR em FRD §7 — cadeia que morre num PR sem artefato. Já PR-VA-020 e PR-VA-021 (mesma categoria Could) NÃO aparecem em PRD §8 nem em FRD §7, apesar de definidos em PRD §4 com BR-Traced=BR-VA-001. Logo, 3 PRs Fase-2 recebem tratamento de rastreio divergente entre si.",
> ```

## 🤖 Claude *(21:18:30)*

Vou ler os outros 3 críticos (segurança, gap-closure, completude) + o veredito final:

## 🤖 Claude *(21:18:32)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/tasks/wql8i8sh7.output",
  "offset": 62,
  "limit": 260
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 62	          },
> 63	          {
> 64	            "id": "TRACE-08",
> 65	            "severity": "high",
> 66	            "doc": "06-data-model.md §2/§3 + 04-frd.md §5 + 05-sdd.md §7",
> 67	            "issue": "Chave de junção load-bearing 'content_variant_id' sem artefato de origem. FR-VA-004/009/017 (monetização, métricas, atribuição de receita) todos chaveiam em content_variant_id; FRD §5 e data-model §2 declaram 'FK → criativo/content_library'. Porém NENHUM doc define onde esse content_variant_id é criado: grep de 'ADD COLUMN'/'ALTER TABLE' mostra que só scheduled_posts.cycle_id é adicionado — content_library nunca recebe a coluna content_variant_id, e nenhuma tabela nova a produz. A cadeia FR-VA-004/009/017 → tabela tem o alvo da FK inexistente.",
> 68	            "fix": "Documentar a origem de content_variant_id: ou ALTER TABLE content_library ADD COLUMN content_variant_id uuid (+ onde a geração o popula por criativo), ou definir que é o próprio id de content_library e renomear o FK accordingly. Adicionar o stub na SDD §7 e a coluna no data-model §2."
> 69	          },
> 70	          {
> 71	            "id": "TRACE-09",
> 72	            "severity": "medium",
> 73	            "doc": "04-frd.md §2 (FR-VA-013 'Should (MVP)') vs 03-prd.md §4/§5 e 00-index.md §Decisão 2",
> 74	            "issue": "Contradição de prioridade na feature que DEFINE o MVP. Index/BRD/PRD afirmam em três lugares 'MVP = TEXTO + IMAGEM'. PR-VA-008 (Image creative), pai de FR-VA-013, está em 'Must Have (MVP)' no PRD §4 e incluído no escopo MVP do PRD §5. Mas o FR que o realiza, FR-VA-013, é marcado 'Should (MVP)' (e prioridade textual divergente das demais que usam Critical/High). Um FR 'Should' sob um PR 'Must' que é a metade 'imagem' do MVP é incoerente.",
> 75	            "fix": "Elevar FR-VA-013 para 'High' ou 'Critical' (consistente com o PR Must PR-VA-008 e com 'MVP=texto+imagem'), ou rebaixar PR-VA-008 e o claim de MVP. Padronizar a coluna Priority do FRD (usar a mesma escala Critical/High/Medium das outras FRs, não 'Should (MVP)')."
> 76	          }
> 77	        ],
> 78	        "notes": "Verifiquei as 4 matrizes (01 §9, 02 §10, 03 §8, 04 §7) + índice (00) + downstream (05 SDD, 06 data-model, 07 process-flow, 08 quality). Cobertura base OK: os 8 MR rastreiam BR 1:1; cada BR tem ≥1 PR; cada PR Must/Should tem PR-Traced; FR-VA-001..018 todos rastreiam ≥1 PR na tabela §2 e têm artefato (tabela/edge fn/cron) no SDD/data-model. Os 5 PROC do 07 cobrem os FRs críticos de geração/cadência/custo (FR-VA-002/005/007), MAS o FR crítico-de-valor FR-VA-010/011 (loop R3) tem trigger contraditório (TRACE-03). Os 2 crons (autopilot-cadence, autopilot-collect) são consistentes entre SDD §2.5/§6 e process §7 — porém só 2, o que colide com 'autopilot-analyze agendado' da FRD. PR-VA-009 não existe em lugar nenhum (numeração pula 008→010, intencional). Quebras de cadeia reais e acionáveis: 9 findings (4 high, 5 medium). Veredito FAIL por inconsistência mútua entre matrizes (TRACE-01/02/05), IDs órfãos downstream (TRACE-06) e FK sem origem (TRACE-08). Nada fabricado: cada finding cita doc+seção lida nesta sessão."
> 79	      },
> 80	      {
> 81	        "dimension": "Segurança + Harness Engineering (CISSP CBK + CLAUDE.md/Survival constraints)",
> 82	        "verdict": "fail",
> 83	        "findings": [
> 84	          {
> 85	            "id": "SEC-VA-01",
> 86	            "severity": "blocker",
> 87	            "doc": "05-sdd.md §1 (diagrama, linha 31) + §2.3 (autopilot-run, linha 73) | 04-frd.md §4.1 (linha 72), §4.2 (linha 82), FR-VA-002 (linha 27) | 07-process-flow.md (linha 43)",
> 88	            "issue": "Contradição de identidade no caminho autônomo (o produto inteiro). O cron path está documentado como service-role sem JWT de usuário ('X-Cron-Trigger + SB_SECRET_KEY', SDD:219; cadence-cron sem mco/sem JWT, SDD:74). Mas o fan-out para orchestrate-content é descrito como 'forward JWT, self-bill' em 4 lugares. Verifiquei orchestrate-content/index.ts:37-38: a função REJEITA com 401 Unauthorized qualquer request sem 'Bearer ' e deriva p_user_id de user.id do JWT verificado (:50,:113). No disparo por cron NÃO existe JWT de usuário para repassar — logo ou (a) o self-bill quebra (401) e o ciclo autônomo nunca cobra/roda, ou (b) alguém minta/forja um JWT de service-role, caso em que o deduct e a resolução per-user de credencial (auth.uid()) ficam sem dono verificável. Nenhum doc descreve como o cron obtém um token per-user (mint/impersonation/x-user-token). É um furo arquitetural E de segurança no núcleo do módulo.",
> 89	            "fix": "Definir explicitamente no 05-sdd §4 o mecanismo de identidade do caminho cron: o cron NÃO repassa JWT — autopilot-cadence-cron/autopilot-run rodam service-role e DEVEM invocar orchestrate-content/orchestrate-step passando o user_id resolvido de autopilot_plans.user_id de forma server-trusted (ex.: header interno x-cron-user-id + asserção service-role, ou um RPC SECURITY DEFINER service-role-only que faça o deduct por p_user_id após o gate). Remover a frase 'forward JWT' das 4 ocorrências (SDD:31, FRD:72/139, process-flow:43) e substituir por 'service-role com user_id derivado do plano (server-trusted), nunca de body'. Atualizar orchestrate-content para aceitar o caminho cron service-role com user_id explícito, ou criar SOP docs/processes/autopilot-cron-identity.md (Lei 2) antes de qualquer código."
> 90	          },
> 91	          {
> 92	            "id": "SEC-VA-02",
> 93	            "severity": "blocker",
> 94	            "doc": "05-sdd.md §4 (autopilot-analyze, linhas 157-167) + §2.3 (linha 75) | 04-frd.md §4.2 (linhas 110-115), FR-VA-010 (linha 35)",
> 95	            "issue": "IDOR / cross-tenant deduct em autopilot-analyze. Contrato: Auth = service-role e Request = { tenant_id, plan_id, previous_cycle_id } — todos recebidos crus do body, sem JWT que vincule identidade. A função deduz 5 mco (deduct_mco_coins, SDD:167) e lê creative_metrics de outro tenant. Confronta o padrão seguro estabelecido no projeto: lead-score/index.ts:76 e campaign-run/index.ts:83 SEMPRE derivam p_user_id de user.id do JWT verificado, NUNCA de um tenant_id do body. Um chamador que alcance esta função (ou um bug no enfileiramento) pode passar tenant_id arbitrário → debita mcoCoins do tenant errado e vaza creative_metrics cross-tenant. Viola a regra do MEMORY 'todo novo SECURITY DEFINER/edge com p_user_id → edge-only OU guarda auth.uid()'.",
> 96	            "fix": "No 05-sdd §4 e 04-frd §4.2: remover tenant_id do body de entrada. autopilot-analyze deve derivar o tenant a partir de previous_cycle_id (SELECT user_id FROM autopilot_cycles WHERE id = previous_cycle_id, sob service-role, e usar ESSE user_id como p_user_id no deduct e como filtro RLS). Documentar que a função é invocável APENAS pelo runner/cron interno (verify_jwt=false + asserção de header de cron), nunca exposta a chamada user-facing com tenant_id arbitrário. Acrescentar à STRIDE (§5.1) uma linha de 'autopilot-analyze | tenant_id forjado no body | Spoofing/Tampering | Critical | derivar tenant do previous_cycle_id, nunca do body'."
> 97	          },
> 98	          {
> 99	            "id": "SEC-VA-03",
> 100	            "severity": "high",
> 101	            "doc": "05-sdd.md §2.3 (linha 75: autopilot-analyze Auth='service-role') + §4 (linha 129) + §5.3 (linha 219) | 06-data-model não toca config.toml",
> 102	            "issue": "Mandato verify_jwt=false incompleto. CLAUDE.md/SOP orchestrate-async-pipeline exige que toda fn de cron/pg_net tenha verify_jwt=false no config.toml. O SDD só declara verify_jwt=false para autopilot-cadence-cron (§2.3 linha 74) e genericamente em §4 (linha 129). autopilot-analyze (service-role, §2.3:75) e autopilot-collect (service-role/cron, §2.3:76) NÃO têm a flag verify_jwt=false declarada. Se chamadas via service-role/pg_net sem essa flag, o gateway retorna 401 na chave service-role opaca (exatamente o modo de falha #1 registrado em project_orchestrate_pipeline_repair / OTD do config.toml). É o erro já vacinado pelo SOP, reincidindo no design.",
> 103	            "fix": "No 05-sdd §2.3 e §5.3: declarar explicitamente verify_jwt=false no config.toml para autopilot-analyze E autopilot-collect (ambas service-role). Adicionar à tabela §2.5 / §7 a entrada de config.toml como artefato versionado: [functions.autopilot-analyze] verify_jwt=false, [functions.autopilot-collect] verify_jwt=false, [functions.autopilot-cadence-cron] verify_jwt=false. Referenciar o SOP orchestrate-async-pipeline.md no §4."
> 104	          },
> 105	          {
> 106	            "id": "SEC-VA-04",
> 107	            "severity": "high",
> 108	            "doc": "05-sdd.md §5.1 STRIDE linha 181 + §4 (linhas 150-154) + §2.3 (linha 73) | 04-frd.md FR-VA-007 (linha 32), NFR-VA-002 (linha 52)",
> 109	            "issue": "TOCTOU no gate de custo — gate e deduct moram em processos diferentes, sem mecanismo atômico descrito. O gate (FR-VA-007) roda em autopilot-run e apenas PROJETA custo (10+5+img); o deduct REAL acontece dentro de cada orchestrate-content sub-run (self-bill, SDD:154) e os 5 mco do analyze acontecem depois, em outra fn. Entre projetar e os sub-runs debitarem, nada garante atomicidade: a STRIDE (linha 181) promete 'Gate atômico server-side ANTES do deduct; lock otimista no ciclo', mas o deduct não está ANTES nem no mesmo escopo do gate — está distribuído em N+1 funções assíncronas. budget_cap_mco pode ser estourado por N sub-runs concorrentes que individualmente passam mas somam acima do teto, e o saldo pode ir negativo entre o check de saldo e os deducts. A promessa de §5.1/NFR-VA-002 ('zero deduct em ciclo abortado', 'gate atômico') não é realizável com a arquitetura projetada.",
> 110	            "fix": "Reconciliar 05-sdd §4/§5.1 com a realidade do self-bill distribuído. Opções a documentar: (A) pré-reservar/pré-debitar o custo projetado total ANTES do fan-out via um deduct atômico único em autopilot-run (com estorno do não-usado ao fechar o ciclo — padrão refund do vision-mcp), tornando os sub-runs não-cobrados; OU (B) acrescentar spend_mco como contador transacional em autopilot_cycles incrementado dentro do MESMO RPC do deduct, com guarda 'spend_mco + amount <= budget_cap_mco' atômica (FOR UPDATE no ciclo). Atualizar a STRIDE para descrever o lock real (FOR UPDATE em autopilot_cycles) e remover 'self-bill, never here' (SDD:154) se a opção A for adotada. Hoje o §4 e o §5.1 se contradizem."
> 111	          },
> 112	          {
> 113	            "id": "SEC-VA-05",
> 114	            "severity": "medium",
> 115	            "doc": "05-sdd.md §7 (linhas 273-309) + §5.2 | 06-data-model.md §3 (linhas 103-113)",
> 116	            "issue": "Default-deny incompleto: autopilot_cycles e creative_metrics habilitam RLS mas NÃO declaram nenhuma política de INSERT/UPDATE — só comentário 'service-role only' (SDD:289,308; data-model:112). Com RLS habilitado e zero política de escrita, authenticated fica corretamente bloqueado (default-deny OK) e service-role faz bypass — isso de fato satisfaz o requisito. PORÉM a asserção do briefing 'política own-row default-deny' não está MATERIALIZADA em DDL: não há CREATE POLICY de escrita alguma, então a intenção 'service-role only' é implícita (vem do bypass), não explícita. Além disso o SDD §5.2 (linha 206) promete 'DELETE bloqueado para authenticated (RESTRICTIVE)' para autopilot_plans, mas NENHUMA migration stub (§7) nem o data-model §3 contém a policy RESTRICTIVE de DELETE prometida — o precedente do projeto (credits/optimization_policy/affiliate, migration 20260413183335 e 20260530183000) usa RESTRICTIVE explícito. A promessa de §5.2 não está refletida no DDL de §7.",
> 117	            "fix": "No 05-sdd §7 e data-model §3: (1) materializar a policy RESTRICTIVE de DELETE prometida em §5.2 como DDL real para autopilot_plans (CREATE POLICY ... AS RESTRICTIVE FOR DELETE USING (false) ou via has_role), espelhando 20260413183335; (2) tornar explícito o default-deny de escrita em autopilot_cycles/creative_metrics com um comentário-âncora de que NÃO há policy de INSERT/UPDATE de propósito (só service-role bypassa) — ou, preferível para auditabilidade, uma policy RESTRICTIVE explícita. Acrescentar a nota de /security-review (já presente em SDD:316) ao bloco de data-model §3 também (hoje só o SDD a cita)."
> 118	          },
> 119	          {
> 120	            "id": "SEC-VA-06",
> 121	            "severity": "medium",
> 122	            "doc": "05-sdd.md §5.1 STRIDE (linha 182) + §2 (FR-VA-003) | 04-frd.md FR-VA-003 (linha 28), NFR-VA-008 (linha 58)",
> 123	            "issue": "Mitigação de prompt-injection presente porém não-acionável (placebo). A STRIDE (linha 182) cobre 'Prompt injection via nome/desc de produto ou trend' com mitigação 'Cyber-Sentinel no input + no output; sanitização do produto antes do prompt'. O ameaça está corretamente identificada (atende o requisito do briefing de 'threat de prompt-injection presente'), MAS: (a) 'Cyber-Sentinel' é referenciado como se fosse um componente pronto, sem citar a fn/lib/_shared concreta que o implementa nem o contrato (o que ele recebe, o que retorna, fail-open vs fail-closed); (b) o vetor real é mais amplo do que 'nome/desc de produto' — o trend vem de vm_trends/fetch-trends (texto externo não-confiável injetado no ângulo viral, FR-VA-018) e a reinjeção de feedback (FR-VA-011) injeta optimization_policy de ciclos anteriores no system prompt, criando um caminho de injeção persistente/auto-envenenamento (policy contaminada num ciclo propaga para todos os próximos). Nenhum doc descreve sanitização de trend nem do optimization_policy reinjetado, nem se o gate é fail-closed.",
> 124	            "fix": "No 05-sdd §5.1 e §5: (1) nomear o componente concreto do Cyber-Sentinel (path da fn/_shared lib) e seu contrato fail-CLOSED (bloqueia publicação se o gate falhar/timeout); (2) ampliar a linha de STRIDE para cobrir explicitamente os 2 vetores extras — trend externo (vm_trends) e feedback reinjetado (optimization_policy) como fontes não-confiáveis que entram no system prompt; adicionar mitigação de sanitização/escape do optimization_policy estruturado (OTD-VA-005 escolheu features estruturadas — bom — mas precisa afirmar que os VALORES das features são tratados como dados, nunca como instrução); (3) registrar em NFR-VA-008 que o gate é fail-closed e auditado."
> 125	          }
> 126	        ],
> 127	        "notes": "Reprovado (fail). Li 05-sdd, 06-data-model, 04-frd integralmente e validei materialmente contra o código (Lei 1): orchestrate-content/index.ts:37-50,113 (deriva user de JWT, 401 sem Bearer), lead-score:76 e campaign-run:83 (derivam p_user_id do JWT, nunca de body), process-affiliate-link:69,175 (guarda de domínio ML existe — claim de reuso GROUNDED), handle-ml-postback:100 (MP_WEBHOOK_SECRET de fato global hoje — OTD-VA-007 honesta), fetch-trends/vm_trends existem, deduct_mco_coins(uuid,decimal,text,jsonb) GRANT só authenticated, scheduled_posts já tem RLS own-row. POSITIVOS reais: secrets só por NOME (§5.4, nunca valor — atende), SB_SECRET_KEY usada e legada marcada REVOGADA (atende), as 3 tabelas têm ENABLE ROW LEVEL SECURITY + SELECT own (default-deny de leitura OK), STRIDE existe com ≥1 mitigação por linha incluindo prompt-injection, nota de /security-review presente (SDD:316). DEFEITOS que reprovam: (1 blocker) a identidade do caminho cron→orchestrate-content é internamente contraditória — 'forward JWT' afirmado em 4 docs mas o cron não tem JWT e orchestrate-content rejeita sem Bearer: o ciclo autônomo, que é o produto, não fecha como desenhado; (2 blocker) autopilot-analyze aceita tenant_id cru do body sob service-role e deduz 5 mco → IDOR/cross-tenant deduct, contraria o padrão seguro do próprio projeto; (3 high) verify_jwt=false não declarado para autopilot-analyze e autopilot-collect — reincidência do modo de falha já vacinado; (4 high) TOCTOU do gate de custo — gate projeta em autopilot-run mas deduct é distribuído em N+1 sub-runs assíncronos, contradizendo a promessa de 'gate atômico ANTES do deduct' (§5.1/NFR-VA-002). Os dois blockers precisam ser resolvidos no SDD (e provavelmente exigem SOP Lei 2 para a ponte de identidade do cron) antes de abrir o BoK gate para código. Não inventei conteúdo; cada finding cita doc+seção e, onde load-bearing, o path:linha do código verificado."
> 128	      },
> 129	      {
> 130	        "dimension": "Cobertura dos 4 requisitos Sovereign (R1-R4) vs auditoria material — a suíte REALMENTE fecha os gaps?",
> 131	        "verdict": "warn",
> 132	        "findings": [
> 133	          {
> 134	            "id": "VA-COV-01",
> 135	            "severity": "high",
> 136	            "doc": "05-sdd.md §4 (linhas 150-154) + 04-frd.md FR-VA-007 + 02-brd.md §8 BR-RISK-001",
> 137	            "issue": "INCOERÊNCIA NO CÁLCULO DO KILL-SWITCH (a defesa-mãe do R3/custo). A fórmula do gate é `project = 10 (orchestrate) + 5 (analyze) + IMAGE_COST * creatives`. Mas: (a) FR-VA-002 define fan-out de '1 dispatch por produto×rede' e CADA orchestrate-content SELF-BILLS 10 (confirmado em campaign-run/index.ts:4-5: 'cascade cost = 10 (fee) + 10×N'). Logo o termo dominante real é 10 × (produtos × plataformas), NÃO um '10' singular — a fórmula SUBCONTA o gasto exatamente no eixo que pode drenar a carteira (BR-RISK-001, RPN 20). (b) O IMAGE_COST é somado à parte, mas billing.ts:16 prova que ORCHESTRATION_RUN=10 é um bundle FLAT que JÁ inclui 3×CONTENT + 1×IMAGE — então imagem é dupla-contada OU o fan-out não usa orchestrate-content para imagem (ambíguo). Um gate que subconta o custo dominante NÃO protege a margem: um plano com 3 produtos × 3 redes = 9 runs = ~90 mco real, mas o gate projeta ~10+5+img. O kill-switch passaria ciclos que deveria abortar.",
> 138	            "fix": "Em 05-sdd §4 e FR-VA-007, reescrever a fórmula do gate para refletir o fan-out real: `projected = ORCHESTRATION_RUN × (|target_product_ids| × |platforms|) + ANALYZE_COST`, e DECIDIR explicitamente se imagem é bundled no ORCHESTRATION_RUN (billing.ts:16) — se sim, remover o termo `+ IMAGE_COST × creatives`; se a imagem rodar fora do bundle, documentar isso e qual fn a cobra. Atualizar o exemplo Gherkin do PRD §7 (budget_cap 5 vs projetado 15) para um exemplo consistente com a fórmula corrigida."
> 139	          },
> 140	          {
> 141	            "id": "VA-COV-02",
> 142	            "severity": "medium",
> 143	            "doc": "05-sdd.md §4 (linha 167) + 04-frd.md FR-VA-010 + 02-brd.md §8 BR-RISK-002",
> 144	            "issue": "GUARDA ANTI-'AUTO-MELHORIA TEATRAL' DEPENDE DE COBRAR 5 mco MESMO QUANDO NÃO HÁ DADO. SDD §4:167 diz 'Deduct 5 mco only when has_real_data OR explicitly configured'. Mas FR-VA-010/FR-VA-011 colocam o autopilot-analyze AGENDADO por cron a cada ciclo (FR-VA-005/010). No ciclo 1 (e em qualquer ciclo cujo coletor falhou — evento `collect_failure` previsto em SDD §6) creative_metrics está vazia → has_real_data=false → baseline. A proteção contra teatro existe (bom), MAS a condição 'OR explicitly configured' é uma backdoor não-especificada: quem configura, com que default? Se default for cobrar, o tenant paga 5 mco/ciclo por uma análise que admite não ter dado — exatamente o custo silencioso que BR-RISK-002 quer evitar. A regra de billing condicional não está refletida na economia do BRD §6 (que lista '5 mco/análise · 1 por ciclo' sem o caveat has_real_data).",
> 145	            "fix": "Especificar em FR-VA-010 o default de billing quando has_real_data=false (recomendado: 0 mco / skip do deduct, registrando evento `analyze_empty`) e definir o que 'explicitly configured' significa (flag no plano? default?). Reconciliar a tabela de economia em 02-brd §6 e 00-index para mostrar que análise sem dado não cobra."
> 146	          },
> 147	          {
> 148	            "id": "VA-COV-03",
> 149	            "severity": "medium",
> 150	            "doc": "04-frd.md FR-VA-017 + 06-data-model.md §2 + 02-brd.md §9 BAC-002/BAC-005",
> 151	            "issue": "FRACTURA NO CONTRATO DE `content_variant_id` ENTRE GERAÇÃO E ATRIBUIÇÃO — chave do R3 e R4. FR-VA-004 promete embutir link ML 'com content_variant_id por criativo'. creative_metrics.content_variant_id é NOT NULL FK→content_library. Mas FR-VA-017 (atribuição de receita) credita revenue_cents na `affiliate_links` correta — e affiliate_links HOJE grava `content_id: null` (provado em _shared/affiliate.ts:~80). Nenhum doc especifica COMO o content_variant_id é gerado/propagado da geração → affiliate_links → postback → creative_metrics. Sem esse fio, BAC-002 ('100% com content_variant_id') e BAC-005 (ROI por peça) não são verificáveis: o postback não tem como saber a qual criativo creditar. FR-VA-017 reconhece dependência de OTD-VA-007, mas o gap de PROPAGAÇÃO do id (não só do secret per-user) não tem FR dona.",
> 152	            "fix": "Adicionar em FR-VA-004/FR-VA-016 a propagação explícita do content_variant_id (de onde nasce — content_library row id? — e como entra no affiliate_links.content_id e no link rastreável), e em FR-VA-017 o caminho postback→content_variant_id. Documentar em 06-data-model §2 a FK affiliate_links↔content_variant_id (hoje content_id é nullable e gravado null)."
> 153	          },
> 154	          {
> 155	            "id": "VA-COV-04",
> 156	            "severity": "low",
> 157	            "doc": "04-frd.md FR-VA-012 + 06-data-model.md §2 (autopilot_plans.target_product_ids) vs 05-sdd.md §7 (CHECK constraint)",
> 158	            "issue": "DRIFT DE CHAVE DO PRODUTO-ALVO. 06-data-model §2 diz target_product_ids text[] FK→`vm_affiliate_products.external_id`; mas FR-VA-001/05-sdd §7 só fazem CHECK(cardinality>=1) sem amarrar a coluna. FR-VA-012 seleciona por `commission_value+trend_score+profitability_score`, e o validation rule (FRD §5) exige 'ids ∈ vm_affiliate_products'. Não há especificação de QUAL coluna identifica o produto (external_id vs id vs mlb). monetizeContent hoje usa `p.mlb` (regex hardcoded), não um id de catálogo. Sem fixar a chave, FR-VA-012 (seleção por score) e o validador de plano podem referenciar colunas diferentes, e a transição do regex-de-3-SKUs (R4 atual) para catálogo (FR-VA-012) fica ambígua.",
> 159	            "fix": "Fixar a chave canônica do produto em UM lugar (recomendado external_id ou mlb de vm_affiliate_products) e propagar consistentemente em FR-VA-001 (validação), FR-VA-012 (seleção), 06-data-model §2 (FK) e na ponte com o regex atual de _shared/affiliate.ts."
> 160	          }
> 161	        ],
> 162	        "notes": "VEREDITO: WARN (não FAIL). Os 4 requisitos Sovereign TÊM FR acionável concreta — nenhum ficou só como 'visão', então não há BLOCKER por ausência de FR. Verifiquei contra o código que os gaps da auditoria são REAIS, não inventados:\n\nR1 (geração auto p/ redes): FECHADO. FR-VA-003 (geração product-aware substituindo prompts B2B hardcoded — confirmei orchestrate-content:10 NÃO desestrutura produto) + FR-VA-013 (imagem no MVP, plugando generate-image hoje órfã). Vídeo 9:16/TikTok/IG/YT corretamente DIFERIDOS p/ fase 2 (PR-VA-020/021, Could Have; FRD §1 'Out of scope'; BRD §7 Constraints). Diferimento limpo.\n\nR2 (cadência tudo-de-uma-vez OU a-cada-N-dias): FECHADO. FR-VA-001 cria autopilot_plans com mode∈{all_at_once,every_n_days}+interval_days (DDL completa em SDD §7 com CHECK 1-30) + FR-VA-005 cron autopilot-cadence */15 com auto-refill next_run_at=now+interval_days. Isto fecha o gap 'recorrência não existe' — confirmei que autopilot_plans NÃO existe em migrations (tabela genuinamente nova). NFR-VA-006 cobre catch-up de janela perdida.\n\nR3 (loop auto-melhorável): FECHADO nas 3 quebras, e confirmei cada quebra no código: (a) NÃO há writer de campaign_metrics em edge fns → coletor FR-VA-008 + creative_metrics FR-VA-009 (DDL completa SEM em migrations); (b) orchestrate-step/orchestrate-content NÃO leem optimization_policy (grep vazio) → FR-VA-011 feedback inject; (c) self-optimize ESCREVE optimization_policy mas NÃO tem cron (grep só achou referência no próprio seed da suíte) → FR-VA-005/010 agendado. Proteção anti-teatro EXISTE (has_real_data=false→baseline, FR-VA-010 + BR-RISK-002) — porém com furo de billing condicional não-especificado (finding VA-COV-02).\n\nR4 (afiliado ML em todo formato): FECHADO no escopo. Confirmei que monetizeContent roda HOJE só sobre articleContent (orchestrate-step:184) com content_id:null e regex hardcoded → FR-VA-004 (monetiza artigo+LinkedIn+Twitter com content_variant_id) + FR-VA-016 (honra param dropado — confirmei orchestrate-content:10 não recebe produto/affiliate_url) + FR-VA-012 (seleção comissão+trend). MAS o FIO do content_variant_id geração→atribuição não está especificado (finding VA-COV-03, high).\n\nPOR QUE WARN E NÃO PASS: a cobertura de FR existe, mas a INTEGRIDADE de duas mecânicas centrais está furada: o kill-switch (VA-COV-01, high) tem fórmula de custo que subconta o eixo de fan-out — a própria defesa contra o risco #1 (drenar carteira) está mal-especificada; e a atribuição por criativo (VA-COV-03, high) carece do fio do content_variant_id, deixando BAC-002/BAC-005 não-verificáveis. Ambos são corrigíveis em doc antes do código (não exigem re-arquitetura), por isso WARN e não FAIL. Caveat Lei 1: avaliei coerência interna dos docs + checagem dos pressupostos da auditoria contra o código atual; NÃO executei os smokes (não existem ainda — são especificação).\""
> 163	      },
> 164	      {
> 165	        "dimension": "Template completeness + FMEA + internal contradictions (viral-autopilot BoK suite, 9 docs)",
> 166	        "verdict": "warn",
> 167	        "findings": [
> 168	          {
> 169	            "id": "VA-COST-IMG-UNDEFINED",
> 170	            "severity": "high",
> 171	            "doc": "02-brd.md §6 (linha 92), 03-prd.md PR-VA-008 (linha 77), 04-frd.md FR-VA-013 (linha 38), 05-sdd.md §4 (linha 151)",
> 172	            "issue": "O custo em mcoCoins da geração de imagem NUNCA é fixado num número. BRD diz 'calibrar via SOP mcoin-cost-calibration', PRD diz '~img cost', FRD não dá número, e o SDD usa um placeholder abstrato IMAGE_COST. Mas o valor canônico JÁ EXISTE e está calibrado/fechado: src/lib/billing.ts linha 21 → IMAGE_GENERATION: 9 (OTD-MCOIN-CALIBRATION CLOSED 2026-06-03, DALL·E 3 1024² $0.04 → 4×-floor). A dimensão exige custo definido para toda operação com IA (geração 10, análise 5, imagem). Pior: não há OTD rastreando esse valor como em aberto, e o kill-switch (FR-VA-007) depende dele para computar o teto — logo o gate de custo é, hoje, incomputável.",
> 173	            "fix": "Fixar o custo de imagem em 9 mco em BRD §6, PRD PR-VA-008, FR-VA-013 e na fórmula do SDD §4, citando src/lib/billing.ts:21 (IMAGE_GENERATION) como fonte da verdade. Se houver intenção de recalibrar, abrir um OTD-VA-008 explícito em 00-index/05-sdd §8 em vez de deixar TBD espalhado."
> 174	          },
> 175	          {
> 176	            "id": "VA-COST-GATE-DOUBLECOUNT",
> 177	            "severity": "high",
> 178	            "doc": "05-sdd.md §4 (linha 151), 04-frd.md FR-VA-007 (linha 32), 02-brd.md §6 (linha 94)",
> 179	            "issue": "A fórmula do teto de custo é internamente inconsistente com o modelo de fan-out que ela protege. Escrita como 'project = 10 (orchestrate) + 5 (analyze) + IMAGE_COST * creatives'. Dois erros: (1) DOUBLE-COUNT da imagem — em src/lib/billing.ts:16-19 ORCHESTRATION_RUN: 10 é um BUNDLE FLAT que já cobre 3×CONTENT_GENERATION + IMAGE_GENERATION; somar 'IMAGE_COST * creatives' por cima cobra a imagem duas vezes. (2) O '10' não é multiplicado pelo nº de runs: o fan-out (07-process-flow §4, linhas 161-175) invoca orchestrate-content uma vez por produto×rede (self-bill 10 cada), mas a projeção trata 10 como constante única de ciclo, enquanto trata só a imagem como por-criativo. O custo projetado fica sistematicamente subestimado em ciclos com N>1 runs → o kill-switch deixa passar gasto acima do teto real.",
> 180	            "fix": "Reescrever a projeção como por-run × nº de runs do fan-out: projected = N_runs × ORCHESTRATION_RUN(10) + ANALYZE(5 por ciclo) (sem somar imagem separada, pois o bundle de 10 já a inclui). Se a imagem for cobrada FORA do bundle (gerada por generate-image plugada, FR-VA-013), então remover a imagem do bundle conceitual e documentar isso — mas não pode contar nos dois. Alinhar BRD §6, FR-VA-007 e SDD §4 com a mesma fórmula."
> 181	          },
> 182	          {
> 183	            "id": "VA-COST-ANALYZE-5MCO-UNGROUNDED",
> 184	            "severity": "medium",
> 185	            "doc": "02-brd.md BR-VA-003/§6 (linhas 47,72,91), 03-prd.md PR-VA-005 (linha 74), 04-frd.md FR-VA-010 (linha 35), 05-sdd.md (linhas 75,167)",
> 186	            "issue": "O custo '5 mco/análise' é apresentado como 'herda self-optimize', mas materialmente: (a) não existe constante 5 em src/lib/billing.ts (verificado — nenhum ':5'); (b) supabase/functions/self-optimize/index.ts NÃO deduz mcoCoins hoje (nenhuma chamada deduct_mco). Logo nada é 'herdado'. Pelo modelo de calibração 4×-floor, uma única chamada LLM de análise alinha-se a LEAD_SCORE:1 ou NURTURE_DISPATCH:2 — 5 mco parece super-precificado e não tem OTD nem entrada na SOP de calibração justificando. Viola Lei 2 (custo de op de IA novo sem fundamento na SOP).",
> 187	            "fix": "Ou (a) calibrar o custo de análise pelo modelo 4×-floor (provavelmente 1-2 mco para uma chamada LLM) e citar a SOP docs/processes/mcoin-cost-calibration.md; ou (b) abrir OTD explícito fixando 5 mco com justificativa (ex.: análise multi-chamada). Em ambos os casos, parar de afirmar 'herda self-optimize', já que self-optimize não cobra nada."
> 188	          },
> 189	          {
> 190	            "id": "VA-SDD-ANALYZE-DEDUCT-CONTRADICTION",
> 191	            "severity": "low",
> 192	            "doc": "05-sdd.md §4 (linha 167) vs 02-brd.md §6 (linha 91) / 04-frd.md FR-VA-010 (linha 35)",
> 193	            "issue": "Contradição sobre QUANDO a análise cobra. O SDD §4 (comentário do contrato) diz: 'Deduct 5 mco only when has_real_data OR explicitly configured'. Já o BRD §6 e a economia tratam como flat '5 mco/análise · 1 por ciclo por plano' (incondicional), e a FR-VA-010 não menciona condicionalidade de cobrança. O comportamento de cobrança condicional ao has_real_data não está refletido nos docs de requisito.",
> 194	            "fix": "Decidir a regra única (cobra sempre vs cobra só com dado real) e propagá-la para BRD §6, FR-VA-010 e SDD §4. Se a regra é 'só cobra com has_real_data', adicionar isso ao critério de aceite e ao ROI Model (afeta volume estimado)."
> 195	          },
> 196	          {
> 197	            "id": "VA-INDEX-TRACE-DROP-PR008",
> 198	            "severity": "low",
> 199	            "doc": "00-index.md §Traceability Chain (linha 63)",
> 200	            "issue": "Inconsistência interna de rastreabilidade. A cadeia do index para MR-VA-001 lista 'BR-VA-001 ──▶ PR-VA-002 ──▶ FR-VA-003, FR-VA-013'. Mas BRD §10 (linha 147) e PRD §8 (linha 203) traçam MR-VA-001 → BR-VA-001 → PR-VA-002, PR-VA-008; e FRD §7 (linha 175) traça FR-VA-013 sob PR-VA-008 (não PR-VA-002). O index omite o nó PR-VA-008 e ainda assim pendura FR-VA-013 (que pertence a PR-VA-008) diretamente sob PR-VA-002 — pulando um nó da cadeia.",
> 201	            "fix": "Corrigir a linha 63 do index para 'MR-VA-001 ──▶ BR-VA-001 ──▶ PR-VA-002, PR-VA-008 ──▶ FR-VA-003, FR-VA-013', alinhando com BRD §10, PRD §8 e FRD §7."
> 202	          },
> 203	          {
> 204	            "id": "VA-OTD-SCHEMA-INDEX-MISSING-OPTIONS",
> 205	            "severity": "low",
> 206	            "doc": "00-index.md §Open Technical Decisions (linhas 92-101)",
> 207	            "issue": "Desvio menor de template/coerência de schema. O template do index (00-index.md template, linhas 68-70) define a tabela de OTD com colunas: OTD ID · Description · Options · Recommendation · Status. A tabela do index real omite a coluna 'Options' (tem só ID/Description/Recommendation/Status). Não quebra o conteúdo (os Options detalhados estão no SDD §8), mas é uma divergência de template na seção que o próprio template prescreve.",
> 208	            "fix": "Adicionar a coluna 'Options' à tabela de OTD do index (resumo de A vs B) ou anotar explicitamente que Options vivem no SDD §8 para registrar a omissão consciente. Cosmético."
> 209	          }
> 210	        ],
> 211	        "notes": "Cobertura material: li os 9 templates em .claude/agents/bok-scribe/templates/ e os 9 docs em docs/bok/viral-autopilot/, e validei contra o código-fonte real.\n\nPASSOU (sem finding): (1) Footer 'Generated by MCORCH BoK Scribe Agent v1.0.0' presente nos 9 docs (grep -c = 1 cada). (2) Todas as seções obrigatórias de cada template estão presentes nos respectivos docs (MRD §1-9, BRD §1-10, PRD §1-8, FRD §1-7, SDD §1-8, Data-Model §1-7, Process-Flow §1-7, Quality §1-8). (3) FMEA: recomputei TODOS os 12 RPN (S×O×D) e batem 100% com o escrito (128,180,84,135,120,90,54,20,72,72,63,48); a contagem RPN>100 = exatamente 4 (VA-002=180, VA-004=135, VA-001=128, VA-005=120), batendo com a afirmação do index 'Fase 5 · 12 FMEA (4 RPN>100)'; todos os 4 itens >100 têm ação recomendada concreta. (4) Contagens cruzadas consistentes: 8 MR / 8 BR / 18 FR / 8 NFR / 12 FMEA / 7 OTD — idênticas entre os docs e o index. (5) Datas consistentes (MVP 2026-07-31, v1.0 2026-08-31 em PRD e BRD). (6) Nomes de tabela/função consistentes entre SDD §2/§7, data-model §2/§3 e process-flow (autopilot_plans, autopilot_cycles, creative_metrics, scheduled_posts.cycle_id; autopilot-run, autopilot-cadence-cron, autopilot-analyze, autopilot-collect; 2 crons). (7) NFRs presentes (8). (8) Gherkin cobre os 5 cenários-chave: cadência (l.164), monetização (l.172), kill-switch (l.178), loop (l.185), ROI (l.191). (9) Afirmações materiais sobre o código-base verificadas VERDADEIRAS: orchestrate-step:138 e :290 = system prompts B2B 'donos de agências' (confirmado); orchestrate-content:79 = destructure que dropa affiliate_url/product_target (confirmado); _shared/affiliate.ts, handle-ml-postback, self-optimize, fetch-trends existem; vm_affiliate_products tem external_id/commission_value/trend_score/profitability_score/image_url (confirmado).\n\nDEFEITOS concentrados no MODELO DE CUSTO mcoCoins (3 findings — 2 high, 1 medium): custo de imagem nunca fixado apesar de valor canônico IMAGE_GENERATION:9 já existir em billing.ts; fórmula do kill-switch faz double-count da imagem e não multiplica o bundle de 10 pelo nº de runs do fan-out (gate subestima gasto → fura o teto); custo '5 mco/análise' sem base canônica (self-optimize não cobra nada hoje, não há constante 5 em billing.ts). Mais 3 findings menores (low) de contradição interna/template. Veredito WARN: a suíte é estruturalmente completa e materialmente fundamentada, mas o modelo de custo — núcleo do MR-VA-006/BR-VA-006 (proteção de margem) — tem erros aritméticos e valores indefinidos que precisam ser resolvidos ANTES de codar o cost-guardrail, sob pena de o kill-switch nascer incomputável/incorreto."
> 212	      }
> 213	    ],
> 214	    "verdict": {
> 215	      "overallVerdict": "NO_GO",
> 216	      "summary": "A suíte BoK viral-autopilot está estruturalmente completa (9/9 docs, FMEA com 4 RPN>100 recomputados corretos, todos os 4 requisitos Sovereign têm FR acionável) e materialmente fundamentada no código — mas NÃO está pronta para seal/Phase 7. Dois BLOCKERS de segurança no núcleo do produto (caminho cron→orchestrate-content \"forward JWT\" sem JWT existir + IDOR cross-tenant via tenant_id cru do body em autopilot-analyze) tornam o ciclo autônomo inexequível como desenhado e violam o padrão seguro do próprio projeto. Soma-se um cluster de erros no modelo de custo mcoCoins (fórmula do kill-switch faz double-count da imagem e não multiplica o bundle de 10 pelo fan-out → gate de custo incomputável/subestimado) e inconsistências de rastreabilidade entre as 4 matrizes. Todos corrigíveis em doc (provável SOP Lei 2 para a ponte de identidade do cron) sem re-arquitetura, mas o BoK gate deve permanecer FECHADO até os 2 blockers e os high de custo/identidade serem resolvidos no SDD/FRD.",
> 217	      "mustFix": [
> 218	        {
> 219	          "severity": "blocker",
> 220	          "doc": "05-sdd.md §1 (l.31) + §2.3 (l.73) | 04-frd.md §4.1 (l.72), §4.2, FR-VA-002 (l.139) | 07-process-flow.md (l.43)",
> 221	          "issue": "Contradição de identidade no caminho autônomo (o produto inteiro). O fan-out cron→orchestrate-content está documentado como 'forward JWT, self-bill' em 4 lugares (SDD:31, FRD:72/139), mas o cron roda service-role SEM JWT de usuário, e orchestrate-content/index.ts:37-50 REJEITA com 401 qualquer request sem 'Bearer ' e deriva p_user_id de user.id do JWT verificado. Logo: ou o self-bill quebra (401, ciclo nunca cobra/roda), ou se forja um JWT service-role e o deduct + resolução per-user (auth.uid()) ficam sem dono verificável. Verificado materialmente em orchestrate-content (401 sem Bearer) e billing.ts.",
> 222	          "fix": "Cravar em 05-sdd §4 o mecanismo de identidade do cron: NÃO repassar JWT — autopilot-cadence-cron/autopilot-run rodam service-role e invocam orchestrate-content/orchestrate-step com user_id resolvido server-trusted de autopilot_plans.user_id (header interno x-cron-user-id + asserção service-role, OU RPC SECURITY DEFINER service-role-only que faça o deduct por p_user_id após o gate). Remover 'forward JWT' das 4 ocorrências e substituir por 'service-role com user_id derivado do plano (nunca do body)'. Atualizar orchestrate-content para aceitar o caminho cron, ou criar SOP docs/processes/autopilot-cron-identity.md (Lei 2) ANTES de qualquer código."
> 223	        },
> 224	        {
> 225	          "severity": "blocker",
> 226	          "doc": "05-sdd.md §4 (l.157-167) + §2.3 (l.75) | 04-frd.md §4.2 (l.110-115), FR-VA-010 (l.35)",
> 227	          "issue": "IDOR / cross-tenant deduct em autopilot-analyze. Contrato: Auth=service-role, Request={tenant_id, plan_id, previous_cycle_id} — todos recebidos crus do body sem JWT vinculando identidade. A função deduz 5 mco e lê creative_metrics de outro tenant. Contraria o padrão seguro do projeto (lead-score:76, campaign-run:83 SEMPRE derivam p_user_id de user.id do JWT, nunca de tenant_id do body) e viola a regra MEMORY 'todo novo SECURITY DEFINER/edge com p_user_id → edge-only OU guarda auth.uid()'. Um chamador com tenant_id arbitrário debita mcoCoins do tenant errado e vaza creative_metrics cross-tenant.",
> 228	          "fix": "Remover tenant_id do body de entrada em 05-sdd §4 e 04-frd §4.2. Derivar o tenant de previous_cycle_id (SELECT user_id FROM autopilot_cycles WHERE id=previous_cycle_id, sob service-role) e usar ESSE user_id como p_user_id no deduct e como filtro RLS. Documentar que a função é invocável APENAS pelo runner/cron interno (verify_jwt=false + asserção de header de cron). Adicionar linha à STRIDE §5.1: 'autopilot-analyze | tenant_id forjado no body | Spoofing/Tampering | Critical | derivar tenant do previous_cycle_id, nunca do body'."
> 229	        },
> 230	        {
> 231	          "severity": "high",
> 232	          "doc": "05-sdd.md §4 (l.151) + §4 fórmula do gate + 04-frd.md FR-VA-007 (l.32) + 02-brd.md §6 (l.94)",
> 233	          "issue": "Fórmula do kill-switch (defesa-mãe do R3/custo, BR-RISK-001 RPN 20) internamente inconsistente com o fan-out que protege. Escrita 'project = 10 (orchestrate) + 5 (analyze) + IMAGE_COST × creatives'. Dois erros confirmados em billing.ts: (1) DOUBLE-COUNT da imagem — ORCHESTRATION_RUN:10 é BUNDLE FLAT que JÁ cobre 3×CONTENT + IMAGE_GENERATION; somar IMAGE_COST por cima cobra a imagem duas vezes; (2) o '10' não é multiplicado pelo nº de runs — o fan-out (FR-VA-002, campaign-run:4-5 'cascade = 10 fee + 10×N') invoca orchestrate-content uma vez por produto×rede (self-bill 10 cada). Plano 3 produtos × 3 redes ≈ 90 mco real, mas o gate projeta ~10+5+img → kill-switch deixa passar gasto acima do teto.",
> 234	          "fix": "Reescrever em 05-sdd §4, FR-VA-007 e BRD §6 a mesma fórmula por-run: projected = N_runs × ORCHESTRATION_RUN(10) + ANALYZE(5/ciclo), SEM termo de imagem separado (o bundle de 10 já a inclui). Se a imagem rodar fora do bundle (generate-image plugada, FR-VA-013), removê-la conceitualmente do bundle e documentar qual fn a cobra — nunca contar nos dois. Corrigir o exemplo Gherkin do PRD §7."
> 235	        },
> 236	        {
> 237	          "severity": "high",
> 238	          "doc": "02-brd.md §6 (l.92), 03-prd.md PR-VA-008 (l.77), 04-frd.md FR-VA-013 (l.38), 05-sdd.md §4 (l.151)",
> 239	          "issue": "O custo mcoCoins da geração de imagem nunca é fixado num número (BRD 'calibrar via SOP', PRD '~img cost', SDD placeholder abstrato IMAGE_COST), apesar do valor canônico JÁ EXISTIR e estar calibrado/fechado: src/lib/billing.ts:21 IMAGE_GENERATION:9 (OTD-MCOIN-CALIBRATION CLOSED 2026-06-03, DALL·E3 1024² $0.04 → 4×-floor — verificado nesta sessão). O kill-switch (FR-VA-007) depende desse valor para computar o teto → o gate de custo é hoje incomputável.",
> 240	          "fix": "Fixar custo de imagem em 9 mco em BRD §6, PRD PR-VA-008, FR-VA-013 e na fórmula do SDD §4, citando src/lib/billing.ts:21 como fonte da verdade. Se houver intenção de recalibrar, abrir OTD-VA-008 explícito em 00-index/05-sdd §8 em vez de deixar TBD espalhado."
> 241	        },
> 242	        {
> 243	          "severity": "high",
> 244	          "doc": "05-sdd.md §2.3 (l.75-76) + §5.3 (l.219) + config.toml (não tocado em 06-data-model)",
> 245	          "issue": "Mandato verify_jwt=false incompleto. O SOP orchestrate-async-pipeline (já vacinou esse modo de falha #1) exige verify_jwt=false no config.toml para toda fn cron/pg_net. SDD só declara a flag para autopilot-cadence-cron (§2.3 l.74). autopilot-analyze (service-role, l.75) e autopilot-collect (service-role/cron, l.76) NÃO têm a flag declarada — reincidência do erro já registrado (gateway 401 na chave service-role opaca). Verificado: §2.3 só lista verify_jwt=false na linha do cadence-cron.",
> 246	          "fix": "Declarar explicitamente verify_jwt=false no config.toml para autopilot-analyze E autopilot-collect em 05-sdd §2.3 e §5.3, como artefato versionado ([functions.autopilot-analyze] verify_jwt=false; [functions.autopilot-collect] verify_jwt=false; [functions.autopilot-cadence-cron] verify_jwt=false). Referenciar o SOP orchestrate-async-pipeline.md no §4."
> 247	        },
> 248	        {
> 249	          "severity": "high",
> 250	          "doc": "05-sdd.md §5.1 STRIDE (l.181) + §4 (l.150-154) + §2.3 (l.73) | 04-frd.md FR-VA-007 (l.32), NFR-VA-002 (l.52)",
> 251	          "issue": "TOCTOU no gate de custo — gate e deduct moram em processos diferentes sem atomicidade descrita. O gate (FR-VA-007) roda em autopilot-run e só PROJETA custo; o deduct REAL ocorre dentro de cada orchestrate-content sub-run (self-bill) e os 5 mco do analyze depois, em outra fn. A STRIDE promete 'gate atômico server-side ANTES do deduct; lock otimista no ciclo', mas o deduct está distribuído em N+1 funções assíncronas: budget_cap_mco pode ser estourado por N sub-runs concorrentes que individualmente passam mas somam acima do teto; saldo pode ir negativo. A promessa de §5.1/NFR-VA-002 ('zero deduct em ciclo abortado', 'gate atômico') não é realizável com a arquitetura projetada.",
> 252	          "fix": "Reconciliar 05-sdd §4/§5.1: (A) pré-debitar o custo projetado total ANTES do fan-out via deduct atômico único em autopilot-run, com estorno do não-usado ao fechar o ciclo (padrão refund vision-mcp), tornando os sub-runs não-cobrados; OU (B) adicionar spend_mco como contador transacional em autopilot_cycles incrementado dentro do MESMO RPC do deduct, com guarda atômica 'spend_mco + amount <= budget_cap_mco' (FOR UPDATE no ciclo). Atualizar a STRIDE para o lock real e remover a contradição entre §4 (self-bill distribuído) e §5.1 (gate atômico)."
> 253	        },
> 254	        {
> 255	          "severity": "high",
> 256	          "doc": "04-frd.md (FR-VA-010) vs 05-sdd.md §2.5 + §3 + 07-process-flow.md §1/§7",
> 257	          "issue": "Trigger do FR-VA-010 (autopilot-analyze, motor do loop R3) contraditório. FRD:35 diz 'Generaliza self-optimize, agora AGENDADO' (implica cron próprio), mas SDD §2.5/§6 e process-flow declaram APENAS 2 crons (cadence, collect); process-flow PROC-VA-005 tipa a análise como 'automated / pós-ciclo (encadeado a PROC-VA-001)' e SDD:122 a desenha '(post-cycle)' inline. Verificado: §2.5/§240 listam só 2 jobs pg_cron. FR crítico-de-valor sem trigger consistente nem artefato cron.",
> 258	          "fix": "Cravar o acionador em UM lugar: (a) autopilot-analyze é chamado in-line ao fim de cada ciclo do autopilot-cadence-cron → corrigir FR-VA-010 para remover 'agendado' e dizer 'encadeado pós-ciclo'; OU (b) é um 3º cron → adicioná-lo a SDD §2.5, §6 e process-flow §7 (hoje afirma '2 crons' em 3 lugares)."
> 259	        },
> 260	        {
> 261	          "severity": "high",
> 262	          "doc": "06-data-model.md §2/§3 + 04-frd.md §5 + 05-sdd.md §7 (origem de content_variant_id)",
> 263	          "issue": "Chave de junção load-bearing content_variant_id sem artefato de origem. FR-VA-004/009/017 (monetização, métricas, atribuição de receita — chave de R3/R4) todos chaveiam em content_variant_id (FRD §5 e data-model §2 declaram 'FK → content_library'), mas NENHUM doc define onde esse id é criado: as únicas ALTER TABLE adicionam scheduled_posts.cycle_id; content_library nunca recebe content_variant_id e nenhuma tabela nova o produz. Além disso affiliate_links hoje grava content_id:null (_shared/affiliate.ts), então o postback (FR-VA-017) não tem como saber a qual criativo creditar → BAC-002 ('100% com content_variant_id') e BAC-005 (ROI por peça) não-verificáveis.",
> 264	          "fix": "Documentar a origem de content_variant_id: ALTER TABLE content_library ADD COLUMN content_variant_id uuid (+ onde a geração o popula por criativo) OU definir que é o próprio id de content_library e renomear o FK. Adicionar o stub na SDD §7 e a coluna no data-model §2. Especificar em FR-VA-004/016 a propagação geração→affiliate_links.content_id→link rastreável, e em FR-VA-017 o caminho postback→content_variant_id."
> 265	        },
> 266	        {
> 267	          "severity": "high",
> 268	          "doc": "03-prd.md §8 vs 02-brd.md §10 (matrizes MR→PR) e 00-index.md §Traceability",
> 269	          "issue": "As matrizes de rastreabilidade não são mutuamente consistentes. (TRACE-01) BRD §10 mapeia MR-VA-003→{PR-004,005}, MR-VA-004→{PR-002}, MR-VA-008→{PR-010,011}; PRD §8 adiciona silenciosamente PR-012/013/022 a essas mesmas células — três células divergentes, sem fonte da verdade única. (TRACE-02/VA-INDEX) O resumo de cadeia do index (l.63) omite PR-VA-008 de MR-VA-001 e pendura FR-VA-013 sob PR-VA-002 quando FR-VA-013 rastreia PR-VA-008 (FRD §7). (TRACE-06) PR-VA-012 (A/B variant) e PR-VA-013 (HITL gate), v1.0 Should/In-scope, aparecem em PRD §8/§4 mas estão AUSENTES da matriz PR→FR da FRD §7 e nenhum FR os rastreia — cadeia morre em PR sem artefato.",
> 270	          "fix": "Reconciliar BRD §10 e PRD §8 para serem idênticas (atualizar BRD §10 para incluir PR-012/013/022 OU anotar que BRD=MVP e PRD=escopo completo). Regenerar a cadeia do index a partir das matrizes autoritativas (não escrevê-la à mão): MR-VA-001 → BR-VA-001 → PR-VA-002, PR-VA-008 → (PR-002→FR-003) e (PR-008→FR-013). Criar FRs para PR-VA-012/013 e adicioná-los à matriz §7, OU marcá-los Future e removê-los das células MR-VA-003/004 do PRD §8."
> 271	        }
> 272	      ],
> 273	      "niceToHave": [
> 274	        "VA-COST-ANALYZE-5MCO-UNGROUNDED (medium): o custo '5 mco/análise' é apresentado como 'herda self-optimize', mas não existe constante :5 em billing.ts e self-optimize/index.ts NÃO deduz mcoCoins hoje — nada é herdado. Calibrar pelo modelo 4×-floor (provável 1-2 mco para 1 chamada LLM, alinhado a LEAD_SCORE:1/NURTURE_DISPATCH:2) citando a SOP mcoin-cost-calibration.md, OU abrir OTD explícito fixando 5 com justificativa; parar de afirmar 'herda self-optimize'.",
> 275	        "VA-COV-02 / VA-SDD-ANALYZE-DEDUCT (medium): billing condicional da análise inconsistente — SDD §4:167 diz 'deduct 5 mco only when has_real_data OR explicitly configured', mas BRD §6 trata como flat '5 mco/análise · 1 por ciclo' incondicional e FR-VA-010 não menciona condicionalidade. Especificar o default quando has_real_data=false (recomendado: 0 mco / skip + evento analyze_empty) e o que 'explicitly configured' significa; reconciliar BRD §6 e 00-index.",
> 276	        "SEC-VA-05 (medium): default-deny de escrita não materializado em DDL — autopilot_cycles/creative_metrics habilitam RLS mas só têm comentário 'service-role only' (sem CREATE POLICY de INSERT/UPDATE), e a policy RESTRICTIVE de DELETE prometida em SDD §5.2 para autopilot_plans não existe nos stubs §7/data-model §3. Materializar a RESTRICTIVE DELETE (espelhando migration 20260413183335) e tornar explícito o default-deny de escrita; replicar a nota de /security-review no data-model §3.",
> 277	        "SEC-VA-06 (medium): mitigação de prompt-injection presente mas placebo — 'Cyber-Sentinel' referenciado sem fn/_shared concreta nem contrato fail-open/fail-closed, e o vetor real é mais amplo (trend externo de vm_trends FR-VA-018 + reinjeção de optimization_policy FR-VA-011, caminho de auto-envenenamento persistente). Nomear o componente concreto + contrato fail-CLOSED, ampliar a STRIDE para os 2 vetores extras, afirmar que valores de features estruturadas do optimization_policy são tratados como dados (nunca instrução), registrar fail-closed+auditado em NFR-VA-008.",
> 278	        "TRACE-04 (medium): BR-VA-005 rastreado de forma inconsistente — PRD §4 PR-VA-004 declara BR-Traced='BR-VA-005, BR-VA-003' mas as matrizes mapeiam BR-VA-005 só para PR-VA-007. Decidir e alinhar (adicionar PR-004 à célula MR-VA-005 nas matrizes, ou remover BR-VA-005 do BR-Traced de PR-004).",
> 279	        "TRACE-05 (medium): FR-VA-016 com PR-Traced divergente dentro do próprio FRD — §2 lista só PR-VA-002, §7 lista sob PR-VA-001 E PR-VA-002. Alinhar as duas tabelas.",
> 280	        "TRACE-07 (medium): tratamento divergente dos 3 PRs Could/Fase-2 — PR-VA-022 aparece em PRD §8 sem FR; PR-VA-020/021 não aparecem em nenhuma matriz apesar de definidos em PRD §4. Uniformizar (todos fora das matrizes com nota, ou todos com FR-stub Fase-2).",
> 281	        "VA-COV-04 (low): drift da chave do produto-alvo — data-model §2 diz target_product_ids FK→vm_affiliate_products.external_id mas SDD §7 só faz CHECK(cardinality>=1); monetizeContent hoje usa p.mlb. Fixar a chave canônica (external_id ou mlb) e propagar em FR-VA-001/012, data-model §2 e na ponte com o regex atual.",
> 282	        "TRACE-09 / VA-PRIORITY (low): FR-VA-013 marcado 'Should (MVP)' sob PR-VA-008 'Must (MVP)' que é a metade 'imagem' do claim 'MVP=texto+imagem' — incoerente. Elevar para High/Critical e padronizar a coluna Priority do FRD (escala Critical/High/Medium, não 'Should (MVP)').",
> 283	        "VA-OTD-SCHEMA (low/cosmético): a tabela de OTD do 00-index omite a coluna 'Options' prescrita pelo template (os Options vivem no SDD §8). Adicionar a coluna resumida ou anotar a omissão consciente."
> 284	      ],
> 285	      "gapClosureVerdict": {
> 286	        "R1": "FECHADO — geração automática product-aware para redes coberta por FR-VA-003 (substitui prompts B2B hardcoded de orchestrate-step:138/290) + FR-VA-013 (imagem no MVP plugando generate-image); vídeo 9:16/TikTok/IG/YT corretamente diferidos à Fase 2 (PR-VA-020/021 Could Have, Out-of-scope FRD §1). Ressalva: FR-VA-013 precisa subir de prioridade (TRACE-09) por ser a metade 'imagem' do MVP.",
> 287	        "R2": "FECHADO — cadência all_at_once OU every_n_days coberta por FR-VA-001 (cria autopilot_plans com mode + interval_days, CHECK 1-30) + FR-VA-005 (cron autopilot-cadence */15 com auto-refill next_run_at) + NFR-VA-006 (catch-up de janela perdida); autopilot_plans é tabela genuinamente nova (não existe em migrations). Único gap deste requisito é a identidade do cron→orchestrate (SEC-VA-01 blocker), não a recorrência em si.",
> 288	        "R3": "COBERTO MAS NÃO ÍNTEGRO — as 3 quebras do loop auto-melhorável têm FR dona (coletor FR-VA-008/creative_metrics FR-VA-009; reinjeção de optimization_policy FR-VA-011; agendamento FR-VA-005/010), com anti-teatro real (has_real_data=false→baseline). Porém o trigger de FR-VA-010 é contraditório (TRACE-03 high), o billing condicional da análise é não-especificado (VA-COV-02) e o gate de custo que protege o loop está incomputável/com double-count (VA-COST-GATE high) — o gap está endereçado mas a mecânica central não fecha sem os fixes.",
> 289	        "R4": "COBERTO MAS NÃO VERIFICÁVEL — afiliado ML em todo formato coberto por FR-VA-004 (monetiza artigo+LinkedIn+Twitter, substituindo monetizeContent que hoje só roda sobre articleContent) + FR-VA-016 (honra param product/affiliate dropado em orchestrate-content:79) + FR-VA-012 (seleção por comissão+trend). Mas o fio do content_variant_id geração→affiliate_links→postback→creative_metrics não está especificado e affiliate_links grava content_id:null hoje (TRACE-08/VA-COV-03 high) → BAC-002/BAC-005 (atribuição/ROI por peça) não-verificáveis até o fix."
> 290	      }
> 291	    }
> 292	  }
> 293	}
> ```

## 🤖 Claude *(21:20:18)*


## 🤖 Claude *(21:20:32)*

A validação retornou **NO_GO** — e fez seu trabalho: **2 blockers + 7 high**, todos verificados contra o código real (não cosméticos). Foi exatamente para isso que rodei a verificação adversarial. Resumo do que ela pegou:

**🔴 Blockers (núcleo do produto):**
1. **SEC-VA-01** — caminho cron→`orchestrate-content` diz "forward JWT", mas o cron não tem JWT e `orchestrate-content:37` rejeita sem `Bearer` (401). O ciclo autônomo não fecha como desenhado.
2. **SEC-VA-02** — IDOR em `autopilot-analyze`: recebe `tenant_id` cru do body sob service-role e deduz mco → drena/vaza cross-tenant. Contraria o padrão do projeto (`lead-score:76`/`campaign-run:83` derivam do JWT).

**🟠 High (7):** fórmula do kill-switch faz double-count da imagem e não multiplica o bundle de 10 pelo fan-out (gate incomputável); custo de imagem nunca fixado (canônico `billing.ts:21`=9); `verify_jwt=false` faltando p/ 2 fns; TOCTOU gate↔deduct; trigger do `autopilot-analyze` contraditório; `content_variant_id` sem origem; matrizes de rastreabilidade divergentes.

Todos **corrigíveis em doc sem re-arquitetura**. Vou aplicar **blockers + high + os mediums/lows** (não deixo conteúdo sabidamente errado numa Fonte da Verdade). Decisões arquiteturais que vou cravar de forma consistente:

- **Identidade do cron:** service-role com `user_id` derivado de `autopilot_plans.user_id` (server-trusted, nunca do body); `orchestrate-content` estendida p/ aceitar `x-autopilot-user-id` + service-role; **SOP `autopilot-cron-identity.md` como gate Lei 2 antes do código** (OTD-VA-008).
- **Custo:** `projected = N_runs × 10 (bundle já inclui imagem, billing.ts:16-21) + 2 (analyze)`; **pré-débito atômico único antes do fan-out + refund do não-usado** (padrão vision-mcp) — resolve TOCTOU; análise = 2 mco (4×-floor, alinhado a NURTURE_DISPATCH), **0 quando `has_real_data=false`**.
- **`content_variant_id` = `content_library.id`** do criativo; grava `affiliate_links.content_id` (hoje null) → fecha o fio atribuição.
- **`autopilot-analyze` inline pós-ciclo** (2 crons, não 3); deriva tenant de `previous_cycle_id`.
- **+2 FRs** (FR-VA-019 A/B, FR-VA-020 HITL) p/ PR-VA-012/013; matrizes reconciliadas.

Aplicando as correções no FRD primeiro:

## 🤖 Claude *(21:20:41)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md",
  "old_string": "**In scope (MVP+v1.0):** entidade de plano de cad\u00eancia; cron de disparo recorrente por-tenant; gera\u00e7\u00e3o product-aware monetizada em todo formato (texto+imagem); coletor de desempenho unificado (cliques+org\u00e2nico+receita); analisador de ciclo + reinje\u00e7\u00e3o de aprendizado; guarda de custo (teto + kill-switch); dashboard de ROI por criativo; sele\u00e7\u00e3o de produto por comiss\u00e3o+trend; \u00e2ngulo informado por trends.\n\n**Out of scope (Fase 2 / Won't):** gera\u00e7\u00e3o de v\u00eddeo 9:16; publica\u00e7\u00e3o em TikTok/Instagram/YouTube; gest\u00e3o de an\u00fancios pagos; atribui\u00e7\u00e3o multi-touch cross-network; auto-descoberta de cat\u00e1logo (CLI manual permanece at\u00e9 PR-VA-022).",
  "new_string": "**In scope (MVP+v1.0):** entidade de plano de cad\u00eancia; cron de disparo recorrente por-tenant; gera\u00e7\u00e3o product-aware monetizada em todo formato (texto+imagem); coletor de desempenho unificado (cliques+org\u00e2nico+receita); analisador de ciclo + reinje\u00e7\u00e3o de aprendizado; guarda de custo (teto + kill-switch); dashboard de ROI por criativo; sele\u00e7\u00e3o de produto por comiss\u00e3o+trend; \u00e2ngulo informado por trends; gera\u00e7\u00e3o A/B de variantes; gate HITL opcional.\n\n**Out of scope (Fase 2 / Won't):** gera\u00e7\u00e3o de v\u00eddeo 9:16; publica\u00e7\u00e3o em TikTok/Instagram/YouTube; gest\u00e3o de an\u00fancios pagos; atribui\u00e7\u00e3o multi-touch cross-network; auto-descoberta de cat\u00e1logo (CLI manual permanece).\n\n> **Nota de escopo de rastreabilidade:** os PRs de Fase 2 / Future (PR-VA-020 v\u00eddeo 9:16, PR-VA-021 TikTok/IG/YT, PR-VA-022 auto-discovery de cat\u00e1logo) s\u00e3o **intencionalmente N\u00c3O decompostos em FR neste ciclo** \u2014 n\u00e3o aparecem nas matrizes MR\u2192PR\u2192FR ativas (PRD \u00a78 / \u00a77 abaixo). Ser\u00e3o decompostos quando o Sovereign priorizar a Fase 2 (precedente: `marketing-hub` PR-MH-020..023)."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:20:44)*


## 🤖 Claude *(21:20:45)*

Agora as linhas da tabela de FRs (FR-VA-004, 007, 010, 013, 016, 017) + 2 FRs novas:

## 🤖 Claude *(21:20:50)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md",
  "old_string": "| FR-VA-004 | Monetize all formats | `monetizeContent` (`_shared/affiliate.ts`) roda em artigo **+ LinkedIn + Twitter**, embutindo link ML per-user com `content_variant_id` por criativo (n\u00e3o s\u00f3 no artigo, n\u00e3o por regex de 3 SKUs). | Critical | PR-VA-002 | Lib | AT-VA-004 |",
  "new_string": "| FR-VA-004 | Monetize all formats | `monetizeContent` (`_shared/affiliate.ts`) roda em artigo **+ LinkedIn + Twitter**, embutindo link ML per-user por criativo (n\u00e3o s\u00f3 no artigo, n\u00e3o por regex de 3 SKUs). **`content_variant_id` = o `id` da linha de `content_library` daquele criativo**; grava `affiliate_links.content_id = content_variant_id` (hoje gravado `null`) e embute o `content_variant_id` no link rastre\u00e1vel \u2192 habilita atribui\u00e7\u00e3o por pe\u00e7a (FR-VA-017). | Critical | PR-VA-002 | Lib | AT-VA-004 |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:21:00)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md",
  "old_string": "| FR-VA-007 | Cost guardrail (kill-switch) | ANTES de qualquer `deduct_mco_coins`: soma custo projetado (10 + 5 + img \u00d7 n\u00ba criativos). Se `> budget_cap_mco` OU `saldo < min_balance` \u2192 aborta ciclo (`aborted_budget`), pausa o plano, notifica. Espelha caps do `vision-mcp`. | Critical | PR-VA-006 | EdgeFunction | AT-VA-007 |",
  "new_string": "| FR-VA-007 | Cost guardrail (kill-switch, at\u00f4mico) | Custo projetado do ciclo = **`N_runs \u00d7 ORCHESTRATION_RUN(10) + ANALYZE_COST(2)`**, onde `N_runs = |target_product_ids| \u00d7 |platforms|` (cada `orchestrate-content` \u00e9 um bundle flat de 10 que **j\u00e1 inclui a imagem** \u2014 `billing.ts:16-21`; **n\u00e3o** somar imagem \u00e0 parte). Se `projetado > budget_cap_mco` OU `saldo < min_balance` \u2192 aborta (`aborted_budget`), pausa o plano, notifica \u2014 **sem deduzir**. Atomicidade: `autopilot-run` faz **UM `deduct_mco_coins` do projetado ANTES do fan-out** (pr\u00e9-pago) e **estorna o n\u00e3o-usado** ao fechar o ciclo (padr\u00e3o refund `vision-mcp`); sub-runs rodam em modo prepaid (sem self-bill). Resolve TOCTOU. | Critical | PR-VA-006 | EdgeFunction | AT-VA-007 |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:21:09)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md",
  "old_string": "| FR-VA-010 | Cycle analyzer | Edge fn `autopilot-analyze` (service-role, 5 mco): l\u00ea `creative_metrics` do ciclo anterior do tenant; se vazio, usa baseline (N\u00c3O inventa); produz `optimization_policy` estruturado (top hook/produto/hor\u00e1rio/formato). Generaliza `self-optimize`, agora agendado. | High | PR-VA-005 | EdgeFunction | AT-VA-010 |",
  "new_string": "| FR-VA-010 | Cycle analyzer | Edge fn `autopilot-analyze` (service-role): deriva o tenant de `previous_cycle_id` (`SELECT user_id FROM autopilot_cycles` \u2014 **nunca do body**); l\u00ea `creative_metrics` do ciclo anterior; se vazio, usa baseline (`has_real_data=false`, N\u00c3O inventa) e **n\u00e3o cobra** (log `analyze_empty`); se h\u00e1 dado, produz `optimization_policy` estruturado (top hook/produto/hor\u00e1rio/formato) e cobra **2 mco** (`ANALYZE_COST`, 4\u00d7-floor \u2014 SOP `mcoin-cost-calibration`). **Encadeado p\u00f3s-ciclo pelo `autopilot-cadence-cron`** (inline, sem cron pr\u00f3prio). | High | PR-VA-005 | EdgeFunction | AT-VA-010 |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:21:16)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md",
  "old_string": "| FR-VA-013 | Image creative (product-referenced) | Plugar `generate-image` (hoje \u00f3rf\u00e3) ao ciclo: usa `image_url` do produto ML como refer\u00eancia; formato por plataforma (quadrado MVP; 9:16 fase 2). Anexa asset a `scheduled_posts`. | Should (MVP) | PR-VA-008 | EdgeFunction | AT-VA-013 |",
  "new_string": "| FR-VA-013 | Image creative (product-referenced) | Plugar `generate-image` (hoje \u00f3rf\u00e3) ao ciclo, **dentro do bundle `orchestrate-content` de 10 mco** (a imagem j\u00e1 \u00e9 coberta pelo bundle \u2014 `billing.ts:16-21`; n\u00e3o gera custo adicional). Usa `image_url` do produto ML como refer\u00eancia; formato por plataforma (quadrado MVP; 9:16 fase 2). Anexa asset a `scheduled_posts`. | High | PR-VA-008 | EdgeFunction | AT-VA-013 |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:21:34)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md",
  "old_string": "| FR-VA-016 | Honor product/affiliate param | `orchestrate-content` passa a desestruturar e honrar o produto-alvo/`affiliate_url` (hoje dropado em `:79`), propagando ao `orchestrate-step`. | Medium | PR-VA-002 | EdgeFunction | AT-VA-016 |\n| FR-VA-017 | Revenue attribution per creative | `handle-ml-postback` credita `revenue_cents` na `affiliate_links` correta e o coletor (FR-VA-008) reflete em `creative_metrics` por `content_variant_id`. Depende de OTD-VA-007. | High | PR-VA-007 | EdgeFunction | AT-VA-017 |\n| FR-VA-018 | Trend-informed angle | `autopilot-run` l\u00ea `vm_trends` (de `fetch-trends`) para pautar o \u00e2ngulo viral do ciclo (reconecta a ilha de trends). | Should (v1.0) | PR-VA-011 | EdgeFunction | AT-VA-018 |",
  "new_string": "| FR-VA-016 | Honor product/affiliate param + cron identity | `orchestrate-content` passa a (a) desestruturar e honrar o produto-alvo (hoje dropado em `:79`), propagando ao `orchestrate-step`; (b) **aceitar o caminho cron** \u2014 service-role + header `x-autopilot-user-id` (server-trusted) + `prepaid=true` (sub-run n\u00e3o cobra; j\u00e1 pr\u00e9-debitado em FR-VA-007). Sanitiza valores externos (produto/trend) antes do prompt. | Critical | PR-VA-001, PR-VA-002 | EdgeFunction | AT-VA-016 |\n| FR-VA-017 | Revenue attribution per creative | `handle-ml-postback` credita `revenue_cents` na `affiliate_links` cujo `content_id = content_variant_id` (FR-VA-004); o coletor (FR-VA-008) reflete em `creative_metrics` por `content_variant_id`. Caminho: postback \u2192 `order_id`/`click_id` \u2192 `affiliate_links.content_id` \u2192 criativo. Depende de OTD-VA-007 (secret per-user). | High | PR-VA-007 | EdgeFunction | AT-VA-017 |\n| FR-VA-018 | Trend-informed angle | `autopilot-run` l\u00ea `vm_trends` (de `fetch-trends`) para pautar o \u00e2ngulo viral do ciclo (reconecta a ilha de trends). Texto de trend \u00e9 **fonte n\u00e3o-confi\u00e1vel** \u2192 sanitizado antes do prompt (NFR-VA-008). | High | PR-VA-011 | EdgeFunction | AT-VA-018 |\n| FR-VA-019 | A/B variant generation | Gera N variantes por criativo por ciclo (config no plano); a vencedora \u00e9 escolhida pelo desempenho do ciclo anterior (`creative_metrics`) e promovida no pr\u00f3ximo. Reusa a gera\u00e7\u00e3o; sob o mesmo teto de custo (FR-VA-007). | Should (v1.0) | PR-VA-012 | EdgeFunction | AT-VA-019 |\n| FR-VA-020 | HITL approval gate (opcional) | Quando `plan.hitl_required=true`, criativos entram em estado `pending_review` antes de publicar; aprova\u00e7\u00e3o humana reusa o policy-engine do `intent-execute`. Default off (aut\u00f4nomo). | Should (v1.0) | PR-VA-013 | EdgeFunction | AT-VA-020 |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:21:37)*


## 🤖 Claude *(21:21:38)*

Agora FRD §5 (origem do `content_variant_id`), §6 (testes das 2 FRs novas) e §7 (matriz reconciliada):

## 🤖 Claude *(21:21:41)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md",
  "old_string": "| `creative_metrics.content_variant_id` | `uuid` | NOT NULL | FK \u2192 criativo/`content_library` | \u2014 |",
  "new_string": "| `creative_metrics.content_variant_id` | `uuid` | NOT NULL | **= `content_library.id`** do criativo (FK \u2192 `content_library.id`); nasce na gera\u00e7\u00e3o (1 linha de `content_library` por criativo) e \u00e9 propagado a `affiliate_links.content_id` (FR-VA-004) e ao link rastre\u00e1vel | \u2014 |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:21:47)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md",
  "old_string": "| FR-VA-017 | \u2705 | \u2705 | \u2014 | atribui\u00e7\u00e3o por `content_variant_id` (gated em OTD-VA-007) |\n| FR-VA-018 | \u2705 | \u2705 | \u2014 | \u00e2ngulo l\u00ea `vm_trends` |",
  "new_string": "| FR-VA-017 | \u2705 | \u2705 | \u2014 | atribui\u00e7\u00e3o por `content_variant_id` (gated em OTD-VA-007) |\n| FR-VA-018 | \u2705 | \u2705 | \u2014 | \u00e2ngulo l\u00ea `vm_trends`; sanitiza\u00e7\u00e3o de fonte externa |\n| FR-VA-019 | \u2705 | \u2705 | \u2014 | N variantes; sele\u00e7\u00e3o por desempenho |\n| FR-VA-020 | \u2705 | \u2014 | \u2705 | gate HITL (E2E do fluxo de aprova\u00e7\u00e3o) |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:21:58)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md",
  "old_string": "| PR ID | FR ID | NFR ID |\n|-------|-------|--------|\n| PR-VA-001 | FR-VA-001, FR-VA-014, FR-VA-016 | NFR-VA-004, NFR-VA-005 |\n| PR-VA-002 | FR-VA-002, FR-VA-003, FR-VA-004, FR-VA-016 | NFR-VA-001, NFR-VA-008 |\n| PR-VA-003 | FR-VA-005, FR-VA-006 | NFR-VA-003, NFR-VA-006 |\n| PR-VA-004 | FR-VA-008, FR-VA-009, FR-VA-017 | NFR-VA-007 |\n| PR-VA-005 | FR-VA-010, FR-VA-011 | NFR-VA-007 |\n| PR-VA-006 | FR-VA-007 | NFR-VA-002 |\n| PR-VA-007 | FR-VA-014, FR-VA-015, FR-VA-017 | NFR-VA-007 |\n| PR-VA-008 | FR-VA-013 | NFR-VA-008 |\n| PR-VA-010 | FR-VA-012 | \u2014 |\n| PR-VA-011 | FR-VA-018 | \u2014 |",
  "new_string": "| PR ID | FR ID | NFR ID |\n|-------|-------|--------|\n| PR-VA-001 | FR-VA-001, FR-VA-014, FR-VA-016 | NFR-VA-004, NFR-VA-005 |\n| PR-VA-002 | FR-VA-002, FR-VA-003, FR-VA-004, FR-VA-016 | NFR-VA-001, NFR-VA-008 |\n| PR-VA-003 | FR-VA-005, FR-VA-006 | NFR-VA-003, NFR-VA-006 |\n| PR-VA-004 | FR-VA-008, FR-VA-009, FR-VA-017 | NFR-VA-007 |\n| PR-VA-005 | FR-VA-010, FR-VA-011 | NFR-VA-007 |\n| PR-VA-006 | FR-VA-007 | NFR-VA-002 |\n| PR-VA-007 | FR-VA-014, FR-VA-015, FR-VA-017 | NFR-VA-007 |\n| PR-VA-008 | FR-VA-013 | NFR-VA-008 |\n| PR-VA-010 | FR-VA-012 | \u2014 |\n| PR-VA-011 | FR-VA-018 | \u2014 |\n| PR-VA-012 | FR-VA-019 | \u2014 |\n| PR-VA-013 | FR-VA-020 | \u2014 |\n\n> Cobertura: 20 FR (FR-VA-001..020) \u00b7 8 NFR. PRs de Fase 2/Future (PR-VA-020/021/022) n\u00e3o decompostos neste ciclo (FRD \u00a71). Todo PR Must/Should rastreia \u22651 FR; todo FR rastreia \u22651 PR."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:22:08)*


## 🤖 Claude *(21:22:09)*

FRD reconciliado (20 FR, cadeia íntegra). Agora o SDD — os 2 blockers vivem aqui. §1 diagrama + §3 fluxo (remover "forward JWT", mostrar pré-débito):

## 🤖 Claude *(21:22:14)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md",
  "old_string": "\u2502  autopilot-run \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510   autopilot-analyze (5 mco)     \u2502\n\u2502  autopilot-cadence-cron \u25c0\u2500\u2500\u2500\u2524   autopilot-collect             \u2502\n\u2502  (service-role, pg_cron)    \u2502                                 \u2502\n\u2502      \u2502 fan-out (forward JWT) \u2502 reuse                          \u2502\n\u2502      \u25bc                       \u25bc                                 \u2502\n\u2502  orchestrate-content \u2192 orchestrate-step (product-aware gen)   \u2502\n\u2502  _shared/affiliate.ts (monetize ALL formats)                  \u2502",
  "new_string": "\u2502  autopilot-run \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510   autopilot-analyze (2 mco)     \u2502\n\u2502  autopilot-cadence-cron \u25c0\u2500\u2500\u2500\u2524   autopilot-collect             \u2502\n\u2502  (service-role, pg_cron)    \u2502   (all service-role,            \u2502\n\u2502      \u2502 pre-debit + fan-out   \u2502    verify_jwt=false)           \u2502\n\u2502      \u2502 (service-role +        \u2502 reuse                          \u2502\n\u2502      \u2502  x-autopilot-user-id)  \u25bc                                \u2502\n\u2502      \u25bc                                                        \u2502\n\u2502  orchestrate-content \u2192 orchestrate-step (product-aware gen)   \u2502\n\u2502  _shared/affiliate.ts (monetize ALL formats, prepaid)         \u2502"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:22:29)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md",
  "old_string": "| `autopilot-run` | `supabase/functions/autopilot-run/index.ts` | JWT (user) OR service-role (cron) | gate s\u00f3; deduct ocorre nos sub-runs | \u2014 (resolve per-user) |\n| `autopilot-cadence-cron` | `supabase/functions/autopilot-cadence-cron/index.ts` | service-role (`verify_jwt=false`, pg_net) | 0 | `SB_SECRET_KEY` (service) |\n| `autopilot-analyze` | `supabase/functions/autopilot-analyze/index.ts` | service-role | 5 mco (an\u00e1lise) | LLM key (per-user\u2192sistema fallback) |\n| `autopilot-collect` | `supabase/functions/autopilot-collect/index.ts` | service-role (cron) | 0 | social/meta tokens per-user |\n\n> **Reuso (modificadas, n\u00e3o novas):** `orchestrate-content` (FR-VA-016 honra produto), `orchestrate-step` (FR-VA-003 product-aware + FR-VA-011 feedback inject), `_shared/affiliate.ts` (FR-VA-004 monetiza todo formato), `generate-image` (FR-VA-013 plugado ao ciclo).",
  "new_string": "| `autopilot-run` | `supabase/functions/autopilot-run/index.ts` | JWT (user, \"gerar agora\") OR service-role+`x-autopilot-user-id` (cron); `verify_jwt=false` | **pr\u00e9-d\u00e9bito at\u00f4mico \u00fanico** (gate antes do fan-out) | `SB_SECRET_KEY` |\n| `autopilot-cadence-cron` | `supabase/functions/autopilot-cadence-cron/index.ts` | service-role (`verify_jwt=false`, pg_net) | 0 | `SB_SECRET_KEY` (service) |\n| `autopilot-analyze` | `supabase/functions/autopilot-analyze/index.ts` | service-role (`verify_jwt=false`); tenant derivado de `previous_cycle_id`, **nunca do body** | 2 mco (s\u00f3 se `has_real_data`) | LLM key (per-user\u2192sistema fallback) |\n| `autopilot-collect` | `supabase/functions/autopilot-collect/index.ts` | service-role (`verify_jwt=false`, cron) | 0 | social/meta tokens per-user |\n\n> **config.toml (artefato versionado \u2014 mandato SOP `orchestrate-async-pipeline`):**\n> ```toml\n> [functions.autopilot-run]          verify_jwt = false\n> [functions.autopilot-cadence-cron] verify_jwt = false\n> [functions.autopilot-analyze]      verify_jwt = false\n> [functions.autopilot-collect]      verify_jwt = false\n> ```\n> Sem isso o gateway retorna 401 na chave service-role opaca (modo de falha #1 j\u00e1 vacinado \u2014 `project_orchestrate_pipeline_repair`).\n\n> **Reuso (modificadas, n\u00e3o novas):** `orchestrate-content` (FR-VA-016: honra produto **+ aceita caminho cron** service-role + `x-autopilot-user-id` + `prepaid=true`), `orchestrate-step` (FR-VA-003 product-aware + FR-VA-011 feedback inject), `_shared/affiliate.ts` (FR-VA-004 monetiza todo formato + grava `content_id`), `generate-image` (FR-VA-013 plugado ao ciclo, dentro do bundle)."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:22:33)*


## 🤖 Claude *(21:22:34)*

§3 fluxo de dados (pré-débito atômico + identidade server-trusted + analyze inline):

## 🤖 Claude *(21:22:51)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md",
  "old_string": "pg_cron        cadence-cron        autopilot-run        orchestrate-*        DB / External\n \u2502 (*/15)          \u2502                    \u2502                    \u2502                   \u2502\n \u2502\u2500\u2500[tick]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502                    \u2502                    \u2502                   \u2502\n \u2502                 \u2502\u2500\u2500[plans due?]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 SELECT is_active AND next_run_at<=now\n \u2502                 \u2502\u25c0\u2500\u2500[plan X]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502\n \u2502                 \u2502\u2500\u2500[POST X-Cron]\u2500\u2500\u2500\u2500\u25b6\u2502                    \u2502                   \u2502\n \u2502                 \u2502                    \u2502\u2500\u2500[cost gate]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 project cost vs budget_cap + balance\n \u2502                 \u2502                    \u2502  (abort if over \u2192 aborted_budget, pause)\u2502\n \u2502                 \u2502                    \u2502\u2500\u2500[read policy]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 optimization_policy (ciclo N-1)\n \u2502                 \u2502                    \u2502\u2500\u2500[select product]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 vm_affiliate_products (comm+trend)\n \u2502                 \u2502                    \u2502\u2500\u2500[open cycle]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 autopilot_cycles (running)\n \u2502                 \u2502                    \u2502\u2500\u2500[fan-out/product\u00d7rede]\u2500\u25b6\u2502              \u2502\n \u2502                 \u2502                    \u2502                    \u2502\u2500\u2500[gen product-aware + feedback]\u2500\u25b6 LLM (BYOK)\n \u2502                 \u2502                    \u2502                    \u2502\u2500\u2500[monetize all formats]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6 affiliate_links + content_variant_id\n \u2502                 \u2502                    \u2502                    \u2502\u2500\u2500[schedule]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6 scheduled_posts (cycle_id)\n \u2502                 \u2502\u25c0\u2500\u2500[re-arm next_run_at = now + interval]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502\n \u2502                 \u2502                    \u2502                    \u2502   (auto-publish cron drains scheduled_posts \u2192 publish-*)\n \u2502                 \u2502 (later) autopilot-collect: post_id \u2192 insights \u2192 creative_metrics\n \u2502                 \u2502 (post-cycle) autopilot-analyze: creative_metrics(N) \u2192 optimization_policy(N) [feeds cycle N+1]",
  "new_string": "pg_cron        cadence-cron        autopilot-run        orchestrate-*        DB / External\n \u2502 (*/15)          \u2502 (service-role)     \u2502 (service-role)     \u2502                   \u2502\n \u2502\u2500\u2500[tick]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502                    \u2502                    \u2502                   \u2502\n \u2502                 \u2502\u2500\u2500[plans due?]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 SELECT is_active AND next_run_at<=now\n \u2502                 \u2502\u25c0\u2500\u2500[plan X (+ user_id)]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502\n \u2502                 \u2502\u2500\u2500[invoke + x-autopilot-user-id=plan.user_id]\u2500\u25b6\u2502              \u2502  (server-trusted; NUNCA do body)\n \u2502                 \u2502                    \u2502\u2500\u2500[cost gate: N_runs\u00d710 + 2 vs cap+saldo]\u25b6\u2502 project; abort if over \u2192 aborted_budget, pause (sem deduct)\n \u2502                 \u2502                    \u2502\u2500\u2500[PRE-DEBIT at\u00f4mico do projetado]\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 deduct_mco_coins(plan.user_id, projected)  \u2190 UMA vez, ANTES do fan-out\n \u2502                 \u2502                    \u2502\u2500\u2500[read policy]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 optimization_policy (ciclo N-1)\n \u2502                 \u2502                    \u2502\u2500\u2500[select product]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 vm_affiliate_products (comm+trend)\n \u2502                 \u2502                    \u2502\u2500\u2500[open cycle]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 autopilot_cycles (running, spend_mco=projected)\n \u2502                 \u2502                    \u2502\u2500\u2500[fan-out/produto\u00d7rede: service-role + x-autopilot-user-id + prepaid=true]\u2500\u25b6\u2502\n \u2502                 \u2502                    \u2502                    \u2502\u2500\u2500[gen product-aware + feedback inject]\u2500\u25b6 LLM (BYOK por user_id)\n \u2502                 \u2502                    \u2502                    \u2502  (prepaid \u2192 N\u00c3O self-bill)\n \u2502                 \u2502                    \u2502                    \u2502\u2500\u2500[monetize all formats: content_id=content_variant_id]\u2500\u25b6 affiliate_links\n \u2502                 \u2502                    \u2502                    \u2502\u2500\u2500[schedule]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6 scheduled_posts (cycle_id)\n \u2502                 \u2502                    \u2502\u2500\u2500[refund do n\u00e3o-usado]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 deduct_mco_coins(user_id, -unused) (estorno; padr\u00e3o vision-mcp)\n \u2502                 \u2502                    \u2502\u2500\u2500[analyze INLINE p\u00f3s-ciclo]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502 autopilot-analyze: creative_metrics(N) \u2192 optimization_policy(N) [feeds N+1]\n \u2502                 \u2502\u25c0\u2500\u2500[re-arm next_run_at = now + interval]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502\n \u2502                 \u2502                    \u2502   (auto-publish cron drains scheduled_posts \u2192 publish-*)\n \u2502                 \u2502 (later, 6/6h) autopilot-collect: post_id \u2192 insights + cliques + receita \u2192 creative_metrics"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:22:54)*


## 🤖 Claude *(21:22:55)*

§4 contratos de API (gate com fórmula correta + pré-débito; analyze sem `tenant_id` no body):

## 🤖 Claude *(21:23:09)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md",
  "old_string": "// Cost gate (FR-VA-007) \u2014 BEFORE any deduction:\n// \u2192 project = 10 (orchestrate) + 5 (analyze) + IMAGE_COST * creatives\n// \u2192 if project > plan.budget_cap_mco \u2192 409 aborted_budget + pause plan\n// \u2192 balance check via profiles.mco_balance; if < min_balance \u2192 402\n// mcoCoins deduction happens inside each orchestrate-content sub-run (self-bill), never here.\n```\n\n### `POST /functions/v1/autopilot-analyze`\n\n```typescript\ninterface AutopilotAnalyzeRequest { tenant_id: string; plan_id: string; previous_cycle_id: string }\ninterface AutopilotAnalyzeResponse {\n  status: 'ok'\n  optimization_policy_id: string\n  has_real_data: boolean        // false \u2192 baseline used, N\u00c3O fabrica recomenda\u00e7\u00e3o\n  top_features: { hook?: string; product_id?: string; best_hour?: number; format?: string }\n}\n// Deduct 5 mco (deduct_mco_coins) only when has_real_data OR explicitly configured; logged.\n```",
  "new_string": "// Identidade: caminho cron = service-role + header x-autopilot-user-id (= autopilot_plans.user_id,\n//   server-trusted, NUNCA do body); caminho \"gerar agora\" = JWT do user, asserir user.id === plan.user_id.\n// Cost gate (FR-VA-007) \u2014 at\u00f4mico, ANTES do fan-out:\n// \u2192 N_runs = |target_product_ids| \u00d7 |platforms|\n// \u2192 projected = N_runs * ORCHESTRATION_RUN(10) + ANALYZE_COST(2)   // imagem J\u00c1 no bundle de 10 (billing.ts:16-21)\n// \u2192 if projected > plan.budget_cap_mco \u2192 409 aborted_budget + pause plan (sem deduct)\n// \u2192 balance check; if mco_balance < projected OR < min_balance \u2192 402\n// \u2192 PRE-DEBIT: deduct_mco_coins(plan.user_id, projected) UMA vez aqui (n\u00e3o nos sub-runs).\n// \u2192 sub-runs invocados com prepaid=true (orchestrate-content N\u00c3O self-bills).\n// \u2192 ao fechar o ciclo: refund do n\u00e3o-usado = deduct_mco_coins(user_id, -(projected - actual)).\n```\n\n### `POST /functions/v1/autopilot-analyze`\n\n```typescript\n// Auth: service-role only (verify_jwt=false); invocada inline pelo autopilot-run p\u00f3s-ciclo.\ninterface AutopilotAnalyzeRequest { previous_cycle_id: string }   // tenant/plan DERIVADOS do ciclo\ninterface AutopilotAnalyzeResponse {\n  status: 'ok'\n  optimization_policy_id: string\n  has_real_data: boolean        // false \u2192 baseline used, N\u00c3O fabrica recomenda\u00e7\u00e3o, N\u00c3O cobra\n  top_features: { hook?: string; product_id?: string; best_hour?: number; format?: string }\n}\n// SEGURAN\u00c7A (anti-IDOR): tenant_id N\u00c3O vem do body. Derivar:\n//   const { user_id, plan_id } = SELECT user_id, plan_id FROM autopilot_cycles WHERE id = previous_cycle_id\n//   \u2192 usar ESSE user_id como p_user_id no deduct e como filtro de creative_metrics (RLS).\n// Deduct ANALYZE_COST(2 mco) via deduct_mco_coins(user_id, 2) SOMENTE quando has_real_data === true;\n//   has_real_data === false \u2192 0 mco + log infra_health_logs event 'viral_autopilot_analyze_empty'.\n```"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:23:14)*


## 🤖 Claude *(21:23:15)*

§5.1 STRIDE — adicionar IDOR de `autopilot-analyze`, ampliar prompt-injection (trend + reinjeção de policy = auto-envenenamento), nomear o Cyber-Sentinel:

## 🤖 Claude *(21:23:29)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md",
  "old_string": "| `autopilot-cadence-cron` | Falsifica\u00e7\u00e3o de trigger de cron (disparo for\u00e7ado) | Spoofing/Elevation | High | `verify_jwt=false` + service-role key; sem path p\u00fablico que dispare ciclo arbitr\u00e1rio; rate por plano via `next_run_at` |\n| `autopilot_plans`/`_cycles`/`creative_metrics` | Leitura/escrita cross-tenant | Information Disclosure | Critical | RLS `user_id = auth.uid()`; crons usam service-role com filtro expl\u00edcito por tenant |\n| Cost gate | Bypass do teto (disparo paralelo p/ exceder) | Tampering | Critical | Gate at\u00f4mico server-side ANTES do deduct; idempot\u00eancia (plan_id, cycle_number); lock otimista no ciclo |\n| Gerador product-aware | Prompt injection via nome/desc de produto ou trend | Tampering/Elevation | High | Cyber-Sentinel no input + no output; sanitiza\u00e7\u00e3o do produto antes do prompt |",
  "new_string": "| `autopilot-cadence-cron` | Falsifica\u00e7\u00e3o de trigger de cron (disparo for\u00e7ado) | Spoofing/Elevation | High | `verify_jwt=false` + service-role key; sem path p\u00fablico que dispare ciclo arbitr\u00e1rio; rate por plano via `next_run_at` |\n| `autopilot-run` (caminho cron) | `user_id` forjado no body p/ gerar/cobrar como outro tenant | Spoofing/Elevation | Critical | `user_id` NUNCA do body \u2014 header `x-autopilot-user-id` s\u00f3 sob service-role assertion, derivado de `autopilot_plans.user_id`; caminho user-JWT assere `user.id === plan.user_id` |\n| `autopilot-analyze` | `tenant_id` forjado no body \u2192 deduct + leitura cross-tenant (IDOR) | Spoofing/Tampering | Critical | **N\u00c3O aceitar `tenant_id` no body**; derivar tenant de `previous_cycle_id` (`SELECT user_id FROM autopilot_cycles`); service-role only; padr\u00e3o `lead-score:76`/`campaign-run:83` |\n| `autopilot_plans`/`_cycles`/`creative_metrics` | Leitura/escrita cross-tenant | Information Disclosure | Critical | RLS `user_id = auth.uid()`; crons usam service-role com filtro expl\u00edcito por tenant derivado da linha |\n| Cost gate (FR-VA-007) | Bypass do teto / saldo negativo entre check e deduct (TOCTOU) | Tampering | Critical | **Pr\u00e9-d\u00e9bito at\u00f4mico \u00daNICO** de `N_runs\u00d710+2` em `autopilot-run` ANTES do fan-out (n\u00e3o distribu\u00eddo nos sub-runs) + refund do n\u00e3o-usado; `spend_mco` no ciclo; idempot\u00eancia (plan_id, cycle_number) |\n| Gerador product-aware | Prompt injection via 3 fontes n\u00e3o-confi\u00e1veis: (a) nome/desc de produto, (b) texto de trend (`vm_trends`/FR-VA-018), (c) **reinje\u00e7\u00e3o de `optimization_policy`** de ciclos anteriores (FR-VA-011) \u2192 auto-envenenamento persistente | Tampering/Elevation | High | Cyber-Sentinel **fail-CLOSED** (o mesmo gate de `orchestrate-content:92`) no input E no output antes de publicar; sanitiza\u00e7\u00e3o/escape das 3 fontes; valores das features estruturadas do `optimization_policy` tratados como **dados, nunca instru\u00e7\u00e3o** (OTD-VA-005) |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:23:32)*


## 🤖 Claude *(21:23:33)*

§5.2 — materializar a policy RESTRICTIVE de DELETE + default-deny de escrita explícito:

## 🤖 Claude *(21:23:39)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md",
  "old_string": "CREATE POLICY \"autopilot_plans_update_own\"\n  ON public.autopilot_plans FOR UPDATE\n  USING (user_id = auth.uid())\n  WITH CHECK (user_id = auth.uid());\n\n-- DELETE bloqueado para authenticated (RESTRICTIVE); s\u00f3 service_role gerencia ciclos/spend.\n```",
  "new_string": "CREATE POLICY \"autopilot_plans_update_own\"\n  ON public.autopilot_plans FOR UPDATE\n  USING (user_id = auth.uid())\n  WITH CHECK (user_id = auth.uid());\n\n-- DELETE bloqueado para authenticated via RESTRICTIVE (espelha migration 20260413183335):\nCREATE POLICY \"autopilot_plans_no_delete\"\n  ON public.autopilot_plans AS RESTRICTIVE FOR DELETE\n  USING (false);   -- s\u00f3 service_role (bypassa RLS) remove; LGPD cascade via auth.users delete\n\n-- autopilot_cycles + creative_metrics: RLS habilitado, SELECT own, e NENHUMA policy de\n-- INSERT/UPDATE/DELETE de prop\u00f3sito \u2192 default-deny total para authenticated; S\u00d3 service-role\n-- (runner/coletor, que bypassa RLS) escreve. O default-deny de escrita \u00e9 INTENCIONAL e expl\u00edcito.\n```"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:23:42)*


## 🤖 Claude *(21:23:43)*

§8 — adicionar OTD-VA-008 (identidade do cron + pré-débito + gate SOP Lei 2):

## 🤖 Claude *(21:23:52)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md",
  "old_string": "| OTD-VA-007 | Secret de postback per-user (herdada `OTD-ML-MP-PER-USER`) | Manter secret global (Usu\u00e1rio Zero) | Per-user `meta`/MP config | **B antes de multi-tenant** \u2014 atribui\u00e7\u00e3o de receita por tenant exige secret per-user | Sovereign |",
  "new_string": "| OTD-VA-007 | Secret de postback per-user (herdada `OTD-ML-MP-PER-USER`) | Manter secret global (Usu\u00e1rio Zero) | Per-user `meta`/MP config | **B antes de multi-tenant** \u2014 atribui\u00e7\u00e3o de receita por tenant exige secret per-user | Sovereign |\n| OTD-VA-008 | Identidade do caminho cron\u2192`orchestrate-content` (o cron n\u00e3o tem JWT; a fn rejeita sem `Bearer`) | Repassar JWT (imposs\u00edvel \u2014 cron n\u00e3o tem) | Service-role + `x-autopilot-user-id` derivado de `autopilot_plans.user_id` + pr\u00e9-d\u00e9bito at\u00f4mico em `autopilot-run` (sub-runs `prepaid`) | **B** \u2014 server-trusted, nunca do body; resolve o blocker SEC-VA-01 + TOCTOU SEC-VA-04. **Gate Lei 2: exige SOP `docs/processes/autopilot-cron-identity.md` ANTES de qualquer c\u00f3digo** (Operator/Sequence/Verification/Recovery do mint server-trusted + pr\u00e9-d\u00e9bito/refund) | Sovereign |\n\n> **Gate Lei 2 (Processo Antecipado):** o caminho de identidade do cron (OTD-VA-008) e o pr\u00e9-d\u00e9bito/refund (FR-VA-007) introduzem automa\u00e7\u00e3o financeira nova \u2192 o SOP `docs/processes/autopilot-cron-identity.md` DEVE ser escrito e revisado **antes** de a fatia de cad\u00eancia/custo ganhar c\u00f3digo. Refer\u00eancia cruzada: SOP `orchestrate-async-pipeline.md` (mandato `verify_jwt=false`)."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:23:58)*


## 🤖 Claude *(21:23:59)*

Agora o **data-model** — `content_variant_id` = `content_library.id`, chave de produto canônica, coluna `hitl_required`, e RLS RESTRICTIVE:

## 🤖 Claude *(21:24:02)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/06-data-model.md",
  "old_string": "| `content_variant_id` | `uuid` | NOT NULL | \u2014 | \u2192 criativo/`content_library` | Criativo medido |\n| `product_id` | `text` | NULL | \u2014 | \u2192 `vm_affiliate_products` | Produto promovido |",
  "new_string": "| `content_variant_id` | `uuid` | NOT NULL | \u2014 | \u2192 `content_library.id` | Criativo medido (= a linha de `content_library` daquele criativo; propagado a `affiliate_links.content_id`) |\n| `product_id` | `text` | NULL | \u2014 | \u2192 `vm_affiliate_products.external_id` | Produto promovido (chave can\u00f4nica `external_id`) |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/06-data-model.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:24:11)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/06-data-model.md",
  "old_string": "| `target_product_ids` | `text[]` | NOT NULL | \u2014 | \u2192 `vm_affiliate_products.external_id` | \u2265 1 produto |\n| `platforms` | `text[]` | NOT NULL | \u2014 | \u2014 | \u2286 {wordpress,linkedin,twitter} (MVP) |\n| `budget_cap_mco` | `int` | NOT NULL | \u2014 | \u2014 | Teto de custo por ciclo |\n| `min_balance_mco` | `int` | NOT NULL | `10` | \u2014 | Piso de saldo p/ disparar |\n| `is_active` | `boolean` | NOT NULL | `false` | \u2014 | Cad\u00eancia ligada |",
  "new_string": "| `target_product_ids` | `text[]` | NOT NULL | \u2014 | \u2192 `vm_affiliate_products.external_id` | \u2265 1 produto (chave can\u00f4nica `external_id`) |\n| `platforms` | `text[]` | NOT NULL | \u2014 | \u2014 | \u2286 {wordpress,linkedin,twitter} (MVP) |\n| `budget_cap_mco` | `int` | NOT NULL | \u2014 | \u2014 | Teto de custo por ciclo (gate FR-VA-007) |\n| `min_balance_mco` | `int` | NOT NULL | `10` | \u2014 | Piso de saldo p/ disparar |\n| `hitl_required` | `boolean` | NOT NULL | `false` | \u2014 | Gate HITL opcional (FR-VA-020); default off = aut\u00f4nomo |\n| `ab_variants` | `int` | NOT NULL | `1` | \u2014 | N\u00ba de variantes A/B por criativo (FR-VA-019); 1 = sem A/B |\n| `is_active` | `boolean` | NOT NULL | `false` | \u2014 | Cad\u00eancia ligada |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/06-data-model.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:24:16)*


## 🤖 Claude *(21:24:16)*

Data-model §3 — RESTRICTIVE DELETE + default-deny de escrita explícito + nota /security-review:

## 🤖 Claude *(21:24:22)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/06-data-model.md",
  "old_string": "CREATE POLICY \"autopilot_cycles: users read own\"   ON public.autopilot_cycles FOR SELECT USING (user_id = auth.uid());\n-- INSERT/UPDATE de cycles e creative_metrics: service_role only (runner/coletor).\nCREATE POLICY \"creative_metrics: users read own\"   ON public.creative_metrics FOR SELECT USING (user_id = auth.uid());",
  "new_string": "-- DELETE de planos bloqueado p/ authenticated via RESTRICTIVE (espelha migration 20260413183335):\nCREATE POLICY \"autopilot_plans: no client delete\" ON public.autopilot_plans AS RESTRICTIVE FOR DELETE USING (false);\n\nCREATE POLICY \"autopilot_cycles: users read own\"   ON public.autopilot_cycles FOR SELECT USING (user_id = auth.uid());\nCREATE POLICY \"creative_metrics: users read own\"   ON public.creative_metrics FOR SELECT USING (user_id = auth.uid());\n-- autopilot_cycles + creative_metrics: S\u00d3 SELECT own. NENHUMA policy de INSERT/UPDATE/DELETE de\n-- prop\u00f3sito \u2192 default-deny TOTAL de escrita para authenticated; s\u00f3 service-role (runner/coletor,\n-- que bypassa RLS) escreve. Default-deny INTENCIONAL e expl\u00edcito."
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>String to replace not found in file.
> String: CREATE POLICY "autopilot_cycles: users read own"   ON public.autopilot_cycles FOR SELECT USING (user_id = auth.uid());
> -- INSERT/UPDATE de cycles e creative_metrics: service_role only (runner/coletor).
> CREATE POLICY "creative_metrics: users read own"   ON public.creative_metrics FOR SELECT USING (user_id = auth.uid());</tool_use_error>
> ```

## 🤖 Claude *(21:24:25)*


## 🤖 Claude *(21:24:25)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/06-data-model.md",
  "offset": 80,
  "limit": 28
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 80	| `content_variant_id` | `uuid` | NOT NULL | — | → `content_library.id` | Criativo medido (= a linha de `content_library` daquele criativo; propagado a `affiliate_links.content_id`) |
> 81	| `product_id` | `text` | NULL | — | → `vm_affiliate_products.external_id` | Produto promovido (chave canônica `external_id`) |
> 82	| `platform` | `text` | NULL | — | — | Rede |
> 83	| `source` | `text` | NOT NULL | — | — | affiliate_click\|organic\|postback |
> 84	| `impressions` | `int` | NOT NULL | `0` | — | — |
> 85	| `engagements` | `int` | NOT NULL | `0` | — | likes/shares/comments |
> 86	| `affiliate_clicks` | `int` | NOT NULL | `0` | — | do click ledger |
> 87	| `revenue_cents` | `int` | NOT NULL | `0` | — | do postback |
> 88	| `collected_at` | `timestamptz` | NOT NULL | `now()` | — | — |
> 89	| — | — | — | — | — | **UNIQUE (content_variant_id, source)** |
> 90	
> 91	> Nenhuma das 3 tabelas carrega `embedding`/`stability_score` — não são nós de conhecimento diretos. A memória semântica entra via `mcorch_nodes` (§4).
> 92	
> 93	---
> 94	
> 95	## 3. Supabase Physical Schema Stubs
> 96	
> 97	```sql
> 98	-- ============================================================
> 99	-- MIGRATION: <ts>_viral_autopilot_schema.sql  (split em 4 arquivos — ver 05-sdd §7)
> 100	-- ============================================================
> 101	-- autopilot_plans / autopilot_cycles / creative_metrics + ALTER scheduled_posts
> 102	-- (stubs CREATE TABLE completos em 05-sdd.md §7)
> 103	
> 104	-- RLS (default-deny → own-row)
> 105	ALTER TABLE public.autopilot_plans     ENABLE ROW LEVEL SECURITY;
> 106	ALTER TABLE public.autopilot_cycles    ENABLE ROW LEVEL SECURITY;
> 107	ALTER TABLE public.creative_metrics    ENABLE ROW LEVEL SECURITY;
> ```

## 🤖 Claude *(21:24:28)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/06-data-model.md",
  "offset": 108,
  "limit": 22
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 108	
> 109	CREATE POLICY "autopilot_plans: users read own"    ON public.autopilot_plans  FOR SELECT USING (user_id = auth.uid());
> 110	CREATE POLICY "autopilot_plans: users write own"   ON public.autopilot_plans  FOR INSERT WITH CHECK (user_id = auth.uid());
> 111	CREATE POLICY "autopilot_plans: users update own"  ON public.autopilot_plans  FOR UPDATE USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());
> 112	
> 113	CREATE POLICY "autopilot_cycles: users read own"   ON public.autopilot_cycles FOR SELECT USING (user_id = auth.uid());
> 114	-- INSERT/UPDATE de cycles e creative_metrics: service_role only (coletor/runner).
> 115	CREATE POLICY "creative_metrics: users read own"   ON public.creative_metrics FOR SELECT USING (user_id = auth.uid());
> 116	
> 117	-- Índices
> 118	CREATE INDEX autopilot_plans_due_idx     ON public.autopilot_plans (next_run_at) WHERE is_active;
> 119	CREATE INDEX autopilot_cycles_plan_idx   ON public.autopilot_cycles (plan_id);
> 120	CREATE INDEX creative_metrics_cycle_idx  ON public.creative_metrics (cycle_id);
> 121	CREATE INDEX creative_metrics_variant_idx ON public.creative_metrics (content_variant_id);
> 122	
> 123	-- Updated-at trigger (reusa update_updated_at_column existente)
> 124	CREATE TRIGGER set_autopilot_plans_updated_at
> 125	  BEFORE UPDATE ON public.autopilot_plans
> 126	  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
> 127	```
> 128	
> 129	---
> ```

## 🤖 Claude *(21:24:38)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/06-data-model.md",
  "old_string": "CREATE POLICY \"autopilot_plans: users update own\"  ON public.autopilot_plans  FOR UPDATE USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());\n\nCREATE POLICY \"autopilot_cycles: users read own\"   ON public.autopilot_cycles FOR SELECT USING (user_id = auth.uid());\n-- INSERT/UPDATE de cycles e creative_metrics: service_role only (coletor/runner).\nCREATE POLICY \"creative_metrics: users read own\"   ON public.creative_metrics FOR SELECT USING (user_id = auth.uid());\n\n-- \u00cdndices",
  "new_string": "CREATE POLICY \"autopilot_plans: users update own\"  ON public.autopilot_plans  FOR UPDATE USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());\n-- DELETE bloqueado p/ authenticated via RESTRICTIVE (espelha 20260413183335); s\u00f3 service-role remove (LGPD cascade):\nCREATE POLICY \"autopilot_plans: no client delete\" ON public.autopilot_plans AS RESTRICTIVE FOR DELETE USING (false);\n\nCREATE POLICY \"autopilot_cycles: users read own\"   ON public.autopilot_cycles FOR SELECT USING (user_id = auth.uid());\nCREATE POLICY \"creative_metrics: users read own\"   ON public.creative_metrics FOR SELECT USING (user_id = auth.uid());\n-- autopilot_cycles + creative_metrics: S\u00d3 SELECT own. NENHUMA policy de INSERT/UPDATE/DELETE de\n-- PROP\u00d3SITO \u2192 default-deny TOTAL de escrita p/ authenticated; s\u00f3 service-role (runner/coletor, que\n-- bypassa RLS) escreve. Default-deny INTENCIONAL e expl\u00edcito (n\u00e3o esquecimento).\n-- \u26a0\ufe0f Toda esta migration passa /security-review antes do commit (FMEA-011 cross-tenant).\n\n-- \u00cdndices"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/06-data-model.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:24:45)*


## 🤖 Claude *(21:24:45)*

SDD §7 — colunas `hitl_required`/`ab_variants` + nota da chave canônica + RESTRICTIVE DELETE:

## 🤖 Claude *(21:24:52)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md",
  "old_string": "  target_product_ids text[] NOT NULL CHECK (cardinality(target_product_ids) >= 1),\n  platforms       text[] NOT NULL CHECK (cardinality(platforms) >= 1),\n  budget_cap_mco  int NOT NULL CHECK (budget_cap_mco > 0),\n  min_balance_mco int NOT NULL DEFAULT 10,\n  is_active       boolean NOT NULL DEFAULT false,\n  next_run_at     timestamptz,\n  created_at      timestamptz NOT NULL DEFAULT now(),\n  updated_at      timestamptz NOT NULL DEFAULT now()\n);\nALTER TABLE public.autopilot_plans ENABLE ROW LEVEL SECURITY;\n-- (RLS policies from \u00a75.2)",
  "new_string": "  target_product_ids text[] NOT NULL CHECK (cardinality(target_product_ids) >= 1),  -- chave can\u00f4nica: vm_affiliate_products.external_id\n  platforms       text[] NOT NULL CHECK (cardinality(platforms) >= 1),\n  budget_cap_mco  int NOT NULL CHECK (budget_cap_mco > 0),\n  min_balance_mco int NOT NULL DEFAULT 10,\n  hitl_required   boolean NOT NULL DEFAULT false,   -- gate HITL opcional (FR-VA-020)\n  ab_variants     int NOT NULL DEFAULT 1 CHECK (ab_variants BETWEEN 1 AND 5),  -- A/B (FR-VA-019)\n  is_active       boolean NOT NULL DEFAULT false,\n  next_run_at     timestamptz,\n  created_at      timestamptz NOT NULL DEFAULT now(),\n  updated_at      timestamptz NOT NULL DEFAULT now()\n);\nALTER TABLE public.autopilot_plans ENABLE ROW LEVEL SECURITY;\n-- (RLS policies from \u00a75.2, incl. RESTRICTIVE no-delete)"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:24:57)*


## 🤖 Claude *(21:24:58)*

SDD §7 — nota sobre `content_variant_id` (= `content_library.id`) e `affiliate_links.content_id`:

## 🤖 Claude *(21:25:04)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md",
  "old_string": "> Nenhuma tabela aqui carrega `embedding` (n\u00e3o s\u00e3o n\u00f3s de conhecimento diretos). A mem\u00f3ria GraphRAG entra via `mcorch_nodes` observation por ciclo (ver `06-data-model.md` \u00a74). Toda migration passa `/security-review` antes do commit (FMEA-011).",
  "new_string": "> **`content_variant_id` \u2014 origem (sem nova coluna em `content_library`):** \u00e9 o pr\u00f3prio `id` da linha de `content_library` gerada para cada criativo (1 linha por formato\u00d7produto\u00d7ciclo). A monetiza\u00e7\u00e3o (FR-VA-004) grava `affiliate_links.content_id = content_variant_id` (hoje gravado `null` em `_shared/affiliate.ts`) e embute o id no link rastre\u00e1vel; o postback (FR-VA-017) resolve `affiliate_links.content_id` \u2192 criativo; o coletor (FR-VA-008) usa o mesmo id em `creative_metrics.content_variant_id`. Fio \u00edntegro gera\u00e7\u00e3o\u2192atribui\u00e7\u00e3o. Nenhuma `ALTER TABLE content_library` \u00e9 necess\u00e1ria.\n>\n> Nenhuma tabela nova carrega `embedding` (n\u00e3o s\u00e3o n\u00f3s de conhecimento diretos). A mem\u00f3ria GraphRAG entra via `mcorch_nodes` observation por ciclo (ver `06-data-model.md` \u00a74). Toda migration passa `/security-review` antes do commit (FMEA-011)."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:25:20)*


## 🤖 Claude *(21:25:20)*

Agora o **BRD** — §6 economia (analyze 5→2, imagem no bundle, fórmula do gate) e §10 matriz reconciliada:

## 🤖 Claude *(21:25:36)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/02-brd.md",
  "old_string": "| Operation | Coins/Run | Plan Tier Mapping | Monthly Volume (est.) | Monthly Revenue (est.) |\n|-----------|-----------|-------------------|-----------------------|----------------------|\n| Ciclo de gera\u00e7\u00e3o (autopilot) | 10 mco/run (herda `orchestrate-content`) + sub-steps | Starter(500) / Pro(2000) / Ent(10k) | fun\u00e7\u00e3o de `interval_days` \u00d7 n\u00ba produtos \u00d7 redes | consumo de plano |\n| An\u00e1lise de ciclo (self-optimize) | 5 mco/an\u00e1lise | idem | 1 por ciclo por plano | consumo de plano |\n| Gera\u00e7\u00e3o de imagem | calibrar via SOP `mcoin-cost-calibration` (modelo 4\u00d7-floor) | idem | 1+ por criativo | consumo de plano |\n\n> **Teto obrigat\u00f3rio (BR-VA-006):** cada plano carrega `budget_cap_mco` por ciclo. O ciclo soma o custo projetado (10 + 5 + imagem \u00d7 n\u00ba criativos) e **aborta antes de deduzir** se exceder o teto ou se o saldo cair abaixo do m\u00ednimo. Espelha o modelo de caps do `vision-mcp` (per-plano + safety di\u00e1rio).",
  "new_string": "> **Constantes can\u00f4nicas (`src/lib/billing.ts`, OTD-MCOIN-CALIBRATION fechada 2026-06-03, modelo 4\u00d7-floor):** `ORCHESTRATION_RUN = 10` \u00e9 um **bundle flat** que J\u00c1 inclui 3\u00d7`CONTENT_GENERATION` + 1\u00d7`IMAGE_GENERATION` (`billing.ts:16-21`). `IMAGE_GENERATION = 9` s\u00f3 vale para gera\u00e7\u00e3o **avulsa** (fora do bundle).\n\n| Operation | Coins/Run | Plan Tier Mapping | Monthly Volume (est.) | Monthly Revenue (est.) |\n|-----------|-----------|-------------------|-----------------------|----------------------|\n| `orchestrate-content` run (1 produto \u00d7 1 rede, texto **+ imagem inclusa**) | 10 mco (bundle flat `billing.ts:16`) | Starter(500) / Pro(2000) / Ent(10k) | `N_runs` = produtos \u00d7 redes, por ciclo | consumo de plano |\n| An\u00e1lise de ciclo (`autopilot-analyze`) | **2 mco** (1 chamada LLM, 4\u00d7-floor alinhado a `NURTURE_DISPATCH:2`); **0 quando `has_real_data=false`** | idem | 1 por ciclo por plano (s\u00f3 se h\u00e1 dado) | consumo de plano |\n| Gera\u00e7\u00e3o de imagem avulsa (se fora do bundle) | 9 mco (`IMAGE_GENERATION`, `billing.ts:21`) | idem | \u2014 (no MVP a imagem est\u00e1 no bundle de 10) | consumo de plano |\n\n> **Custo projetado de um ciclo = `N_runs \u00d7 10 + 2`** (`N_runs = produtos \u00d7 redes`; imagem j\u00e1 no bundle de 10 \u2014 **n\u00e3o** somar \u00e0 parte). **N\u00c3O afirmar \"herda self-optimize\"**: `self-optimize` n\u00e3o cobra mcoCoins hoje; o custo de 2 mco da an\u00e1lise \u00e9 uma opera\u00e7\u00e3o nova calibrada pela SOP `mcoin-cost-calibration`.\n>\n> **Teto obrigat\u00f3rio (BR-VA-006) \u2014 at\u00f4mico:** cada plano carrega `budget_cap_mco` por ciclo. `autopilot-run` projeta `N_runs \u00d7 10 + 2`, **aborta antes de deduzir** se `> budget_cap_mco` ou `saldo < min_balance`, e faz **UM pr\u00e9-d\u00e9bito at\u00f4mico do projetado ANTES do fan-out** (sub-runs em modo `prepaid`, n\u00e3o cobram), estornando o n\u00e3o-usado ao fechar o ciclo (padr\u00e3o refund `vision-mcp`). Resolve o TOCTOU. Espelha os caps do `vision-mcp` (per-plano + safety di\u00e1rio)."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/02-brd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:25:39)*


## 🤖 Claude *(21:25:40)*

BRD §4 — corrigir custo da análise em BR-VA-003:

## 🤖 Claude *(21:25:43)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/02-brd.md",
  "old_string": "| BR-VA-003 | Loop fechado: coletar desempenho do ciclo \u2192 analisar \u2192 reinjetar aprendizados (top hooks/produtos/hor\u00e1rios) na gera\u00e7\u00e3o do pr\u00f3ximo ciclo | MR-VA-003 | Critical | 5 mco/an\u00e1lise (LLM, herda `self-optimize`) | Ciclo N+1 recebe no prompt o resumo estruturado do desempenho do ciclo N |",
  "new_string": "| BR-VA-003 | Loop fechado: coletar desempenho do ciclo \u2192 analisar \u2192 reinjetar aprendizados (top hooks/produtos/hor\u00e1rios) na gera\u00e7\u00e3o do pr\u00f3ximo ciclo | MR-VA-003 | Critical | 2 mco/an\u00e1lise (1 chamada LLM, 4\u00d7-floor; **0 se sem dado real**) | Ciclo N+1 recebe no prompt o resumo estruturado do desempenho do ciclo N |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/02-brd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:26:01)*


## 🤖 Claude *(21:26:02)*

BRD §10 — matriz reconciliada (idêntica à PRD §8 que vou alinhar em seguida):

## 🤖 Claude *(21:26:09)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/02-brd.md",
  "old_string": "| MR ID | BR ID | PR ID (stub) |\n|-------|-------|--------------|\n| MR-VA-001 | BR-VA-001 | PR-VA-002, PR-VA-008 |\n| MR-VA-002 | BR-VA-002 | PR-VA-001, PR-VA-003 |\n| MR-VA-003 | BR-VA-003 | PR-VA-004, PR-VA-005 |\n| MR-VA-004 | BR-VA-004 | PR-VA-002 |\n| MR-VA-005 | BR-VA-005 | PR-VA-007 |\n| MR-VA-006 | BR-VA-006 | PR-VA-006 |\n| MR-VA-007 | BR-VA-007 | PR-VA-001 |\n| MR-VA-008 | BR-VA-008 | PR-VA-010, PR-VA-011 |",
  "new_string": "> Esta matriz \u00e9 **id\u00eantica** \u00e0 do PRD `03-prd.md` \u00a78 (fonte \u00fanica de verdade da cadeia MR\u2192BR\u2192PR). PRs de Fase 2/Future (PR-VA-020/021/022) **n\u00e3o** entram aqui \u2014 n\u00e3o s\u00e3o decompostos neste ciclo (FRD \u00a71).\n\n| MR ID | BR ID | PR ID |\n|-------|-------|--------------|\n| MR-VA-001 | BR-VA-001 | PR-VA-002, PR-VA-008 |\n| MR-VA-002 | BR-VA-002 | PR-VA-001, PR-VA-003 |\n| MR-VA-003 | BR-VA-003 | PR-VA-004, PR-VA-005, PR-VA-012 |\n| MR-VA-004 | BR-VA-004 | PR-VA-002, PR-VA-013 |\n| MR-VA-005 | BR-VA-005 | PR-VA-004, PR-VA-007 |\n| MR-VA-006 | BR-VA-006 | PR-VA-006 |\n| MR-VA-007 | BR-VA-007 | PR-VA-001 |\n| MR-VA-008 | BR-VA-008 | PR-VA-010, PR-VA-011 |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/02-brd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:26:16)*


## 🤖 Claude *(21:26:17)*

PRD §8 — alinhar à BRD §10 (MR-VA-005 +PR-VA-004; remover PR-VA-022 Future):

## 🤖 Claude *(21:26:23)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/03-prd.md",
  "old_string": "| MR ID | BR ID | PR ID |\n|-------|-------|-------|\n| MR-VA-001 | BR-VA-001 | PR-VA-002, PR-VA-008 |\n| MR-VA-002 | BR-VA-002 | PR-VA-001, PR-VA-003 |\n| MR-VA-003 | BR-VA-003 | PR-VA-004, PR-VA-005, PR-VA-012 |\n| MR-VA-004 | BR-VA-004 | PR-VA-002, PR-VA-013 |\n| MR-VA-005 | BR-VA-005 | PR-VA-007 |\n| MR-VA-006 | BR-VA-006 | PR-VA-006 |\n| MR-VA-007 | BR-VA-007 | PR-VA-001 |\n| MR-VA-008 | BR-VA-008 | PR-VA-010, PR-VA-011, PR-VA-022 |",
  "new_string": "> Matriz **autoritativa** da cadeia MR\u2192BR\u2192PR (id\u00eantica \u00e0 BRD \u00a710). PRs de Fase 2/Future (PR-VA-020/021/022) n\u00e3o entram \u2014 n\u00e3o decompostos neste ciclo (FRD \u00a71).\n\n| MR ID | BR ID | PR ID |\n|-------|-------|-------|\n| MR-VA-001 | BR-VA-001 | PR-VA-002, PR-VA-008 |\n| MR-VA-002 | BR-VA-002 | PR-VA-001, PR-VA-003 |\n| MR-VA-003 | BR-VA-003 | PR-VA-004, PR-VA-005, PR-VA-012 |\n| MR-VA-004 | BR-VA-004 | PR-VA-002, PR-VA-013 |\n| MR-VA-005 | BR-VA-005 | PR-VA-004, PR-VA-007 |\n| MR-VA-006 | BR-VA-006 | PR-VA-006 |\n| MR-VA-007 | BR-VA-007 | PR-VA-001 |\n| MR-VA-008 | BR-VA-008 | PR-VA-010, PR-VA-011 |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/03-prd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:26:28)*


## 🤖 Claude *(21:26:28)*

PRD §4 (custo análise 5→2) e §7 (Gherkin kill-switch com fórmula correta):

## 🤖 Claude *(21:26:31)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/03-prd.md",
  "old_string": "| PR-VA-005 | **Self-improvement feedback** \u2014 analisar lote anterior \u2192 injetar features no prompt do pr\u00f3ximo | P1 | BR-VA-003 | M | 5 (an\u00e1lise) | Fecha as 3 quebras do `self-optimize` |",
  "new_string": "| PR-VA-005 | **Self-improvement feedback** \u2014 analisar lote anterior \u2192 injetar features no prompt do pr\u00f3ximo | P1 | BR-VA-003 | M | 2 (an\u00e1lise; 0 sem dado) | Fecha as 3 quebras do `self-optimize` |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/03-prd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:26:38)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/03-prd.md",
  "old_string": "  Scenario: Kill-switch de custo antes do deduct (PR-VA-006)\n    Given um plano com budget_cap_mco 5 e custo de ciclo projetado 15\n    When o cron tenta disparar o ciclo\n    Then o ciclo aborta com status \"aborted_budget\"\n    And nenhum mcoCoin \u00e9 deduzido\n    And o plano \u00e9 marcado \"paused\" com notifica\u00e7\u00e3o PT-BR \"Teto de custo insuficiente para este ciclo\"",
  "new_string": "  Scenario: Kill-switch de custo antes do deduct (PR-VA-006)\n    Given um plano com budget_cap_mco 20, 3 produtos-alvo e 3 redes\n    And o custo projetado = N_runs(9) \u00d7 10 + 2 = 92 mcoCoins\n    When o cron tenta disparar o ciclo\n    Then o ciclo aborta com status \"aborted_budget\" (92 > 20)\n    And nenhum mcoCoin \u00e9 deduzido\n    And o plano \u00e9 marcado \"paused\" com notifica\u00e7\u00e3o PT-BR \"Teto de custo insuficiente para este ciclo\""
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/03-prd.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:26:47)*


## 🤖 Claude *(21:26:48)*

Agora o **process-flow** — §1 (gate + identidade cron) e §4 (stub sem "forward JWT"):

## 🤖 Claude *(21:27:00)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/07-process-flow.md",
  "old_string": "[autopilot-run(plan, X-Cron-Trigger)]\n   \u2502\n[Cost gate: projetar 10 + 5 + img\u00d7criativos]\n   \u2502\n<Gateway: custo \u2264 budget_cap AND saldo \u2265 min_balance?>\n   \u2502 NO \u2500\u2500\u25b6 [status=aborted_budget] \u2500\u2500\u25b6 [pause plan] \u2500\u2500\u25b6 [infra_health_logs: viral_autopilot_aborted_budget] \u2500\u2500\u25b6 [notify PT-BR] \u2500\u2500\u25b6 END\n   \u2502 YES\n[read optimization_policy (ciclo N-1)]  \u2192  [select product (comm+trend / seed)]  \u2192  [open autopilot_cycles (running)]\n   \u2502\n[fan-out por produto\u00d7rede \u2192 orchestrate-content (forward JWT, self-bill)]\n   \u2502\n   \u251c\u2500\u2500[orchestrate-step: gerar product-aware + injetar feedback]\n   \u251c\u2500\u2500[monetize ALL formats \u2192 affiliate_links + content_variant_id]\n   \u251c\u2500\u2500[generate-image product-referenced \u2192 asset]\n   \u2514\u2500\u2500[insert scheduled_posts (cycle_id)]\n   \u2502\n[re-arm: next_run_at = now + interval_days]   (auto-refill)\n   \u2502\n[Insert mcorch_node observation + edge OPTIMIZES_FROM \u2192 ciclo N-1]\n   \u2502\nEND  (auto-publish cron drena scheduled_posts \u2192 publish-*; PROC-VA-003 coleta depois)",
  "new_string": "[autopilot-run(plan, service-role, x-autopilot-user-id = plan.user_id)]\n   \u2502\n[Cost gate: projetar N_runs\u00d710 + 2]   (N_runs = produtos \u00d7 redes; imagem j\u00e1 no bundle de 10)\n   \u2502\n<Gateway: projetado \u2264 budget_cap AND saldo \u2265 projetado/min_balance?>\n   \u2502 NO \u2500\u2500\u25b6 [status=aborted_budget] \u2500\u2500\u25b6 [pause plan] \u2500\u2500\u25b6 [infra_health_logs: viral_autopilot_aborted_budget] \u2500\u2500\u25b6 [notify PT-BR] \u2500\u2500\u25b6 END (sem deduct)\n   \u2502 YES\n[PRE-DEBIT at\u00f4mico: deduct_mco_coins(plan.user_id, projetado)]   \u2190  UMA vez, ANTES do fan-out\n   \u2502\n[read optimization_policy (ciclo N-1)]  \u2192  [select product (comm+trend / seed)]  \u2192  [open autopilot_cycles (running, spend_mco=projetado)]\n   \u2502\n[fan-out por produto\u00d7rede \u2192 orchestrate-content (service-role + x-autopilot-user-id + prepaid=true)]\n   \u2502\n   \u251c\u2500\u2500[orchestrate-step: gerar product-aware + injetar feedback (prepaid \u2192 N\u00c3O self-bill)]\n   \u251c\u2500\u2500[monetize ALL formats \u2192 affiliate_links.content_id = content_variant_id]\n   \u251c\u2500\u2500[generate-image product-referenced \u2192 asset (dentro do bundle)]\n   \u2514\u2500\u2500[insert scheduled_posts (cycle_id)]\n   \u2502\n[refund do n\u00e3o-usado: deduct_mco_coins(user_id, -(projetado \u2212 actual))]\n   \u2502\n[autopilot-analyze INLINE: creative_metrics(N-1) \u2192 optimization_policy]  (2 mco se has_real_data; 0 sen\u00e3o)\n   \u2502\n[re-arm: next_run_at = now + interval_days]   (auto-refill)\n   \u2502\n[Insert mcorch_node observation + edge OPTIMIZES_FROM \u2192 ciclo N-1]\n   \u2502\nEND  (auto-publish cron drena scheduled_posts \u2192 publish-*; PROC-VA-003 coleta depois)"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/07-process-flow.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:27:15)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/07-process-flow.md",
  "old_string": "**Integration code stub (dentro de `autopilot-run/index.ts`):**\n```typescript\n// Para cada produto-alvo \u00d7 rede do plano:\nfor (const product of selectedProducts) {\n  for (const platform of plan.platforms) {\n    await updateCycleStatus(cycleId, 'running')\n    const run = await supabase.functions.invoke('orchestrate-content', {\n      headers: { Authorization: userJwt },     // self-bill no tenant\n      body: {\n        topic: buildViralAngle(product, trends),   // FR-VA-018\n        product_target: { id: product.external_id, meta: product, feedback: policyFeatures }, // FR-VA-016\n        platforms: [platform],\n        cycle_id: cycleId,                          // NFR-VA-007 auditabilidade\n      },\n    })\n    if (!run.data?.ok) await logHealth('viral_autopilot_cycle_failed', { cycleId, platform })\n  }\n}\n```",
  "new_string": "**Integration code stub (dentro de `autopilot-run/index.ts`, service-role):**\n```typescript\n// userId \u00e9 server-trusted: caminho cron = autopilot_plans.user_id; caminho \"gerar agora\" = auth.uid() (asserido == plan.user_id).\n// Pr\u00e9-d\u00e9bito at\u00f4mico do projetado J\u00c1 ocorreu antes deste loop (FR-VA-007); sub-runs s\u00e3o prepaid.\nfor (const product of selectedProducts) {\n  for (const platform of plan.platforms) {\n    await updateCycleStatus(cycleId, 'running')\n    const run = await supabase.functions.invoke('orchestrate-content', {\n      // SEM Authorization de user \u2014 caminho cron service-role:\n      headers: {\n        Authorization: `Bearer ${SB_SECRET_KEY}`,   // service-role\n        'x-autopilot-user-id': userId,               // server-trusted (NUNCA do body do cliente)\n      },\n      body: {\n        topic: buildViralAngle(sanitize(product), sanitize(trends)),  // FR-VA-018 + sanitiza\u00e7\u00e3o (NFR-VA-008)\n        product_target: { id: product.external_id, meta: product, feedback: policyFeatures }, // FR-VA-016\n        platforms: [platform],\n        cycle_id: cycleId,                            // NFR-VA-007 auditabilidade\n        prepaid: true,                                // FR-VA-007 \u2014 sub-run N\u00c3O self-bills (j\u00e1 pr\u00e9-debitado)\n      },\n    })\n    if (!run.data?.ok) await logHealth('viral_autopilot_cycle_failed', { cycleId, platform })\n  }\n}\n// Ao fim: actual = soma real; refund = projetado \u2212 actual via deduct_mco_coins(userId, -refund).\n```\n> \u26a0\ufe0f `orchestrate-content` deve ser estendida (FR-VA-016) p/ aceitar este caminho: service-role + `x-autopilot-user-id` + `prepaid`. **Gate Lei 2: SOP `docs/processes/autopilot-cron-identity.md` antes do c\u00f3digo** (OTD-VA-008)."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/07-process-flow.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:27:25)*


## 🤖 Claude *(21:27:25)*

Agora o **00-index** — regenerar a cadeia de rastreabilidade (derivada das matrizes autoritativas) e atualizar a tabela de OTD:

## 🤖 Claude *(21:27:40)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/00-index.md",
  "old_string": "```\nMR-VA-001 (gera\u00e7\u00e3o auto) \u2500\u2500\u25b6 BR-VA-001 \u2500\u2500\u25b6 PR-VA-002 \u2500\u2500\u25b6 FR-VA-003, FR-VA-013 \u2500\u2500\u25b6 orchestrate-step (lib) | generate-image\nMR-VA-002 (cad\u00eancia)     \u2500\u2500\u25b6 BR-VA-002 \u2500\u2500\u25b6 PR-VA-001, PR-VA-003 \u2500\u2500\u25b6 FR-VA-001, FR-VA-005, FR-VA-006 \u2500\u2500\u25b6 autopilot_plans | autopilot-cadence-cron\nMR-VA-003 (loop melhoria)\u2500\u2500\u25b6 BR-VA-003 \u2500\u2500\u25b6 PR-VA-004, PR-VA-005 \u2500\u2500\u25b6 FR-VA-008..011 \u2500\u2500\u25b6 creative_metrics | cycle-analyzer | feedback-inject\nMR-VA-004 (afiliado ML)  \u2500\u2500\u25b6 BR-VA-004 \u2500\u2500\u25b6 PR-VA-002 \u2500\u2500\u25b6 FR-VA-004, FR-VA-016 \u2500\u2500\u25b6 _shared/affiliate.ts | process-affiliate-link\nMR-VA-005 (ROI/criativo) \u2500\u2500\u25b6 BR-VA-005 \u2500\u2500\u25b6 PR-VA-007 \u2500\u2500\u25b6 FR-VA-009, FR-VA-017 \u2500\u2500\u25b6 creative_metrics | handle-ml-postback\nMR-VA-006 (custo)        \u2500\u2500\u25b6 BR-VA-006 \u2500\u2500\u25b6 PR-VA-006 \u2500\u2500\u25b6 FR-VA-007 \u2500\u2500\u25b6 autopilot_cycles | deduct_mco_coins\nMR-VA-007 (multi-tenant) \u2500\u2500\u25b6 BR-VA-007 \u2500\u2500\u25b6 PR-VA-001 \u2500\u2500\u25b6 FR-VA-001, NFR-VA-004 \u2500\u2500\u25b6 affiliate_config (RLS auth.uid())\nMR-VA-008 (sinal viral)  \u2500\u2500\u25b6 BR-VA-008 \u2500\u2500\u25b6 PR-VA-010, PR-VA-011 \u2500\u2500\u25b6 FR-VA-012, FR-VA-018 \u2500\u2500\u25b6 vm_affiliate_products | fetch-trends\n```",
  "new_string": "> Vis\u00e3o **derivada** das matrizes autoritativas (BRD \u00a710 = PRD \u00a78 = FRD \u00a77). Em caso de diverg\u00eancia, as matrizes dos docs prevalecem.\n\n```\nMR-VA-001 (gera\u00e7\u00e3o auto) \u2500\u25b6 BR-VA-001 \u2500\u25b6 PR-VA-002 \u2500\u25b6 FR-VA-003 \u2500\u25b6 orchestrate-step (product-aware)\n                                       \u2514\u25b6 PR-VA-008 \u2500\u25b6 FR-VA-013 \u2500\u25b6 generate-image (no bundle)\nMR-VA-002 (cad\u00eancia)     \u2500\u25b6 BR-VA-002 \u2500\u25b6 PR-VA-001, PR-VA-003 \u2500\u25b6 FR-VA-001, FR-VA-005, FR-VA-006 \u2500\u25b6 autopilot_plans | autopilot-cadence-cron\nMR-VA-003 (loop melhoria)\u2500\u25b6 BR-VA-003 \u2500\u25b6 PR-VA-004, PR-VA-005, PR-VA-012 \u2500\u25b6 FR-VA-008..011, FR-VA-019 \u2500\u25b6 creative_metrics | autopilot-analyze | feedback-inject\nMR-VA-004 (afiliado ML)  \u2500\u25b6 BR-VA-004 \u2500\u25b6 PR-VA-002, PR-VA-013 \u2500\u25b6 FR-VA-004, FR-VA-016, FR-VA-020 \u2500\u25b6 _shared/affiliate.ts | process-affiliate-link\nMR-VA-005 (ROI/criativo) \u2500\u25b6 BR-VA-005 \u2500\u25b6 PR-VA-004, PR-VA-007 \u2500\u25b6 FR-VA-009, FR-VA-017 \u2500\u25b6 creative_metrics | handle-ml-postback\nMR-VA-006 (custo)        \u2500\u25b6 BR-VA-006 \u2500\u25b6 PR-VA-006 \u2500\u25b6 FR-VA-007 \u2500\u25b6 autopilot_cycles | deduct_mco_coins (pr\u00e9-d\u00e9bito+refund)\nMR-VA-007 (multi-tenant) \u2500\u25b6 BR-VA-007 \u2500\u25b6 PR-VA-001 \u2500\u25b6 FR-VA-001, FR-VA-016 (+NFR-VA-004) \u2500\u25b6 affiliate_config (RLS auth.uid()) | x-autopilot-user-id\nMR-VA-008 (sinal viral)  \u2500\u25b6 BR-VA-008 \u2500\u25b6 PR-VA-010, PR-VA-011 \u2500\u25b6 FR-VA-012, FR-VA-018 \u2500\u25b6 vm_affiliate_products | fetch-trends\n```"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/00-index.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:27:44)*


## 🤖 Claude *(21:27:45)*

00-index — tabela de OTD com coluna Options (template-conformant) + OTD-VA-008:

## 🤖 Claude *(21:27:59)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/00-index.md",
  "old_string": "| OTD ID | Description | Recommendation | Status |\n|--------|-------------|----------------|--------|\n| OTD-VA-001 | `campaign_metrics` (campaign-level) vs `creative_metrics` (por content_variant_id) | Nova `creative_metrics`; ETL agrega p/ campaign_metrics | Open |\n| OTD-VA-002 | Cron infra: pg_cron (nurture-advance) vs OS crontab (auto-publish) | pg_cron service-role por consist\u00eancia | Open |\n| OTD-VA-003 | Fonte de engajamento org\u00e2nico (LinkedIn/Twitter API tier) | Cliques de afiliado primeiro (j\u00e1 temos); org\u00e2nico best-effort gated por tier | Open |\n| OTD-VA-004 | Unidade do teto de custo: por ciclo vs di\u00e1rio | Cap por ciclo no plano + safety di\u00e1rio global (espelha vision-mcp) | Open |\n| OTD-VA-005 | Mecanismo de reinje\u00e7\u00e3o do feedback (texto cru vs features estruturadas) | Features estruturadas (top hooks/produtos/hor\u00e1rios) | Open |\n| OTD-VA-006 | Autonomia de sele\u00e7\u00e3o de produto (auto-score vs shortlist) | 3 SKUs semente agora (Decis\u00e3o 4); auto-score em v1.0 | Decided (seeds) |\n| OTD-VA-007 | `OTD-ML-MP-PER-USER` \u2014 secret de postback per-user | Fechar antes da atribui\u00e7\u00e3o de receita multi-tenant | Open (herdada) |",
  "new_string": "| OTD ID | Description | Options (A / B) | Recommendation | Status |\n|--------|-------------|-----------------|----------------|--------|\n| OTD-VA-001 | Tabela de m\u00e9tricas | A: estender `campaign_metrics` (campaign-level) \u00b7 B: nova `creative_metrics` (por content_variant_id) | **B**; ETL agrega p/ campaign_metrics | Open |\n| OTD-VA-002 | Infra de cron | A: pg_cron (nurture-advance) \u00b7 B: OS crontab (auto-publish) | **A** pg_cron service-role | Open |\n| OTD-VA-003 | Fonte de engajamento org\u00e2nico | A: s\u00f3 cliques afiliado \u00b7 B: + insights de API por tier | **Ambos faseado**: cliques primeiro, org\u00e2nico best-effort | Open |\n| OTD-VA-004 | Unidade do teto de custo | A: por ciclo (plano) \u00b7 B: di\u00e1rio global | **Ambos**: cap por ciclo + safety di\u00e1rio (vision-mcp) | Open |\n| OTD-VA-005 | Reinje\u00e7\u00e3o do feedback | A: texto cru no prompt \u00b7 B: features estruturadas | **B** (top hooks/produtos/hor\u00e1rios; valores = dados, n\u00e3o instru\u00e7\u00e3o) | Open |\n| OTD-VA-006 | Autonomia de sele\u00e7\u00e3o de produto | A: auto-score comiss\u00e3o+trend \u00b7 B: shortlist curada | **3 SKUs semente** agora (Decis\u00e3o 4); auto-score v1.0 | Decided (seeds) |\n| OTD-VA-007 | `OTD-ML-MP-PER-USER` \u2014 secret de postback per-user | A: secret global (Usu\u00e1rio Zero) \u00b7 B: per-user | **B** antes de multi-tenant | Open (herdada) |\n| OTD-VA-008 | Identidade do caminho cron\u2192`orchestrate-content` | A: repassar JWT (imposs\u00edvel) \u00b7 B: service-role + `x-autopilot-user-id` server-trusted + pr\u00e9-d\u00e9bito | **B**; resolve blocker SEC-VA-01 + TOCTOU. **Gate Lei 2: SOP `autopilot-cron-identity.md` antes do c\u00f3digo** | Open |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/00-index.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:28:05)*


## 🤖 Claude *(21:28:06)*

00-index — atualizar phase log (20 FR, 8 OTD, validação adversarial NO_GO→fixes):

## 🤖 Claude *(21:28:11)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/00-index.md",
  "old_string": "| 3 | Technical Specification | 2026-06-17 | FRD (18 FR + 8 NFR) + SDD (STRIDE, 7 OTD) |\n| 4 | Data & Process Engineering | 2026-06-17 | 3 novas tabelas + 4 processos + 2 crons |\n| 5 | Quality & Autonomic Engineering | 2026-06-17 | 12 FMEA (4 RPN>100), kill-switch self-heal |\n| 6 | Traceability Validation | 2026-06-17 | Adversarial workflow \u2014 ver seal report |",
  "new_string": "| 3 | Technical Specification | 2026-06-17 | FRD (20 FR + 8 NFR) + SDD (STRIDE 8, 8 OTD) |\n| 4 | Data & Process Engineering | 2026-06-17 | 3 novas tabelas + 5 processos + 2 crons |\n| 5 | Quality & Autonomic Engineering | 2026-06-17 | 12 FMEA (4 RPN>100), kill-switch self-heal |\n| 6 | Traceability Validation | 2026-06-17 | Workflow adversarial (4 cr\u00edticos): NO_GO inicial (2 blockers + 7 high) \u2192 todos corrigidos em doc \u2192 re-valida\u00e7\u00e3o |"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>String to replace not found in file.
> String: | 3 | Technical Specification | 2026-06-17 | FRD (18 FR + 8 NFR) + SDD (STRIDE, 7 OTD) |
> | 4 | Data & Process Engineering | 2026-06-17 | 3 novas tabelas + 4 processos + 2 crons |
> | 5 | Quality & Autonomic Engineering | 2026-06-17 | 12 FMEA (4 RPN>100), kill-switch self-heal |
> | 6 | Traceability Validation | 2026-06-17 | Adversarial workflow — ver seal report |
> (note: Edit also tried swapping \uXXXX escapes and their characters; neither form matched, so the mismatch is likely elsewhere in old_string. Re-read the file and copy the exact surrounding text.)</tool_use_error>
> ```

## 🤖 Claude *(21:28:14)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/00-index.md",
  "offset": 73,
  "limit": 14
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 73	MR-VA-008 (sinal viral)  ─▶ BR-VA-008 ─▶ PR-VA-010, PR-VA-011 ─▶ FR-VA-012, FR-VA-018 ─▶ vm_affiliate_products | fetch-trends
> 74	```
> 75	
> 76	---
> 77	
> 78	## Phase Completion Log
> 79	
> 80	| Phase | Name | Completed | Notes |
> 81	|-------|------|-----------|-------|
> 82	| 0 | Project Bootstrap | 2026-06-17 | Slug `viral-autopilot`; inputs derived from Sovereign directive |
> 83	| 1 | Market & Business Intelligence | 2026-06-17 | MRD + BRD — 8 MR, 8 BR, ROI model |
> 84	| 2 | Product Definition | 2026-06-17 | PRD — 2 personas, MoSCoW (MVP=texto+imagem) |
> 85	| 3 | Technical Specification | 2026-06-17 | FRD (18 FR + 8 NFR) + SDD (STRIDE, RLS, 7 OTD) |
> 86	| 4 | Data & Process Engineering | 2026-06-17 | 3 novas tabelas + 4 processos + 2 crons |
> ```

## 🤖 Claude *(21:28:18)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/00-index.md",
  "offset": 85,
  "limit": 6
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 85	| 3 | Technical Specification | 2026-06-17 | FRD (18 FR + 8 NFR) + SDD (STRIDE, RLS, 7 OTD) |
> 86	| 4 | Data & Process Engineering | 2026-06-17 | 3 novas tabelas + 4 processos + 2 crons |
> 87	| 5 | Quality & Autonomic Engineering | 2026-06-17 | 12 FMEA (4 RPN>100), kill-switch self-heal |
> 88	| 6 | Traceability Validation | 2026-06-17 | Adversarial workflow — ver seal report |
> 89	| 7 | Knowledge Mesh Injection | [ ] | `scripts/seed-viral-autopilot-bok-seal.ts` (pendente exec sob aprovação) |
> 90	
> ```

## 🤖 Claude *(21:28:20)*


## 🤖 Claude *(21:28:25)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/00-index.md",
  "old_string": "| 3 | Technical Specification | 2026-06-17 | FRD (18 FR + 8 NFR) + SDD (STRIDE, RLS, 7 OTD) |\n| 4 | Data & Process Engineering | 2026-06-17 | 3 novas tabelas + 4 processos + 2 crons |\n| 5 | Quality & Autonomic Engineering | 2026-06-17 | 12 FMEA (4 RPN>100), kill-switch self-heal |\n| 6 | Traceability Validation | 2026-06-17 | Adversarial workflow \u2014 ver seal report |",
  "new_string": "| 3 | Technical Specification | 2026-06-17 | FRD (20 FR + 8 NFR) + SDD (STRIDE 8, RLS, 8 OTD) |\n| 4 | Data & Process Engineering | 2026-06-17 | 3 novas tabelas + 5 processos + 2 crons |\n| 5 | Quality & Autonomic Engineering | 2026-06-17 | 12 FMEA (4 RPN>100), kill-switch self-heal |\n| 6 | Traceability Validation | 2026-06-17 | Workflow adversarial (4 cr\u00edticos): NO_GO inicial (2 blockers + 7 high) \u2192 todos corrigidos em doc \u2192 re-valida\u00e7\u00e3o |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/00-index.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:28:46)*


## 🤖 Claude *(21:28:48)*

Correções minor restantes (TRACE-04/05/09, chave canônica) já caíram nas edições das matrizes/data-model. Agora atualizo o seed script (ID ranges FR→020, OTD→008) e recomputo as contagens de linha pós-edição:

## 🤖 Claude *(21:29:00)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/seed-viral-autopilot-bok-seal.ts",
  "old_string": "ID SPACE: MR-VA-001..008 \u00b7 BR-VA-001..008 \u00b7 BO-001..004 \u00b7 SH-001..005 \u00b7 PR-VA-001..022 \u00b7 FR-VA-001..018 \u00b7 NFR-VA-001..008 \u00b7 PROC-VA-001..005 \u00b7 KPI-VA-001..008 \u00b7 FMEA-VA-001..012 \u00b7 SOL-VA-001..005 \u00b7 QO-001..004 \u00b7 BAC-001..005 \u00b7 OTD-VA-001..007.",
  "new_string": "ID SPACE: MR-VA-001..008 \u00b7 BR-VA-001..008 \u00b7 BO-001..004 \u00b7 SH-001..005 \u00b7 PR-VA-001..022 (020/021/022 Fase-2 n\u00e3o decompostos) \u00b7 FR-VA-001..020 \u00b7 NFR-VA-001..008 \u00b7 PROC-VA-001..005 \u00b7 KPI-VA-001..008 \u00b7 FMEA-VA-001..012 \u00b7 SOL-VA-001..005 \u00b7 QO-001..004 \u00b7 BAC-001..005 \u00b7 OTD-VA-001..008.\n\nVALIDA\u00c7\u00c3O FASE 6 (workflow adversarial, 4 cr\u00edticos): veredito inicial NO_GO (2 blockers + 7 high) \u2014 TODOS corrigidos em doc antes do seal. Blockers: SEC-VA-01 (identidade cron\u2192orchestrate-content: service-role + x-autopilot-user-id server-trusted, nunca forward-JWT \u2014 orchestrate-content:37 rejeita sem Bearer; OTD-VA-008 + gate SOP autopilot-cron-identity.md Lei 2) \u00b7 SEC-VA-02 (IDOR autopilot-analyze: tenant derivado de previous_cycle_id, nunca do body). Highs: f\u00f3rmula do kill-switch corrigida (N_runs\u00d710+2; imagem J\u00c1 no bundle billing.ts:16-21, sem double-count; pr\u00e9-d\u00e9bito at\u00f4mico \u00fanico + refund vision-mcp resolve TOCTOU) \u00b7 custo de imagem fixado (bundle de 10; avulso IMAGE_GENERATION:9 billing.ts:21) \u00b7 verify_jwt=false declarado p/ as 4 fns \u00b7 trigger de autopilot-analyze cravado inline p\u00f3s-ciclo (2 crons) \u00b7 content_variant_id = content_library.id com fio gera\u00e7\u00e3o\u2192affiliate_links.content_id\u2192postback\u2192creative_metrics \u00b7 matrizes BRD \u00a710 = PRD \u00a78 = FRD \u00a77 reconciliadas (+FR-VA-019 A/B, FR-VA-020 HITL p/ PR-VA-012/013). An\u00e1lise = 2 mco (4\u00d7-floor, n\u00e3o 'herda self-optimize' que n\u00e3o cobra) com 0 quando has_real_data=false."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/scripts/seed-viral-autopilot-bok-seal.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:29:08)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/seed-viral-autopilot-bok-seal.ts",
  "old_string": "      MR: '001..008',\n      BR: '001..008',\n      BO: '001..004',\n      SH: '001..005',\n      PR: '001..022',\n      FR: '001..018',\n      NFR: '001..008',\n      PROC: '001..005',\n      KPI: '001..008',\n      FMEA: '001..012',\n      SOL: '001..005',\n      QO: '001..004',\n      BAC: '001..005',\n      OTD: '001..007',\n    },",
  "new_string": "      MR: '001..008',\n      BR: '001..008',\n      BO: '001..004',\n      SH: '001..005',\n      PR: '001..022',\n      FR: '001..020',\n      NFR: '001..008',\n      PROC: '001..005',\n      KPI: '001..008',\n      FMEA: '001..012',\n      SOL: '001..005',\n      QO: '001..004',\n      BAC: '001..005',\n      OTD: '001..008',\n    },\n    phase6_validation: { initial_verdict: 'NO_GO', blockers: 2, highs: 7, all_resolved_in_doc: true, method: 'adversarial workflow 4 critics' },"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/scripts/seed-viral-autopilot-bok-seal.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:29:15)*


## 🤖 Claude *(21:29:18)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/seed-viral-autopilot-bok-seal.ts",
  "old_string": "    related_otds: ['OTD-VA-001', 'OTD-VA-002', 'OTD-VA-003', 'OTD-VA-004', 'OTD-VA-005', 'OTD-VA-006', 'OTD-VA-007', 'OTD-ML-MP-PER-USER'],",
  "new_string": "    related_otds: ['OTD-VA-001', 'OTD-VA-002', 'OTD-VA-003', 'OTD-VA-004', 'OTD-VA-005', 'OTD-VA-006', 'OTD-VA-007', 'OTD-VA-008', 'OTD-ML-MP-PER-USER'],\n    depends_on_sop: 'docs/processes/autopilot-cron-identity.md (a escrever \u2014 gate Lei 2 antes do c\u00f3digo da fatia cad\u00eancia/custo)',"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/scripts/seed-viral-autopilot-bok-seal.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:29:29)*


## 🤖 Claude *(21:29:31)*

Todas as correções aplicadas (2 blockers + 7 high + mediums/lows). Materialidade exige re-verificar — não auto-declarar GO. Vou re-rodar a mesma validação adversarial (run fresco, relê os arquivos editados) para confirmar que as correções são coerentes e não introduziram novas contradições (as matrizes agora precisam estar triplamente consistentes; a fórmula de custo em 4 lugares precisa bater):

## 🤖 Claude *(21:29:33)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "scriptPath": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/workflows/scripts/viral-autopilot-bok-validation-wf_162126db-952.js",
  "description": "Re-validate viral-autopilot BoK after fixes"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: w004y9nqc
> Summary: Phase 6 adversarial validation of the viral-autopilot BoK suite: traceability integrity, security/Harness constraints, R1-R4 gap-closure coverage, template/FMEA completeness → GO/NO-GO verdict with must-fix list
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/subagents/workflows/wf_492c4145-5c3
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/workflows/scripts/viral-autopilot-bok-validation-wf_162126db-952.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/workflows/scripts/viral-autopilot-bok-validation-wf_162126db-952.js"} to iterate without resending the script.)
> Run ID: wf_492c4145-5c3
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/21b2d649-94ad-4468-9821-20f76eae70a3/workflows/scripts/viral-autopilot-bok-validation-wf_162126db-952.js", resumeFromRunId: "wf_492c4145-5c3"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(21:29:37)*


## 🤖 Claude *(21:29:38)*

Re-validação rodando em background. Enquanto isso, recomputo as contagens de linha pós-edição para o seal metadata ficar exato:

## 🤖 Claude *(21:29:38)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l docs/bok/viral-autopilot/*.md | sort -k2",
  "description": "Recompute line counts after edits"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>    108 docs/bok/viral-autopilot/00-index.md
>    133 docs/bok/viral-autopilot/01-mrd.md
>    164 docs/bok/viral-autopilot/02-brd.md
>    217 docs/bok/viral-autopilot/03-prd.md
>    191 docs/bok/viral-autopilot/04-frd.md
>    373 docs/bok/viral-autopilot/05-sdd.md
>    215 docs/bok/viral-autopilot/06-data-model.md
>    231 docs/bok/viral-autopilot/07-process-flow.md
>    173 docs/bok/viral-autopilot/08-quality-metrics.md
>   1805 total
> ```

## 🤖 Claude *(21:29:45)*


## 🤖 Claude *(21:29:48)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/seed-viral-autopilot-bok-seal.ts",
  "old_string": "  content: `viral-autopilot \u2014 Motor de conte\u00fado viral aut\u00f4nomo monetizado por afiliado ML (BoK v1)\n\nBoK suite (9 docs, 1722 LOC) sealed 2026-06-17",
  "new_string": "  content: `viral-autopilot \u2014 Motor de conte\u00fado viral aut\u00f4nomo monetizado por afiliado ML (BoK v1)\n\nBoK suite (9 docs, 1805 LOC) sealed 2026-06-17"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/scripts/seed-viral-autopilot-bok-seal.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:29:53)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/seed-viral-autopilot-bok-seal.ts",
  "old_string": "DOCUMENTOS: docs/bok/viral-autopilot/{00-index 104, 01-mrd 133, 02-brd 158, 03-prd 214, 04-frd 181, 05-sdd 334, 06-data-model 208, 07-process-flow 217, 08-quality-metrics 173} \u2014 total 1722 LOC.",
  "new_string": "DOCUMENTOS: docs/bok/viral-autopilot/{00-index 108, 01-mrd 133, 02-brd 164, 03-prd 217, 04-frd 191, 05-sdd 373, 06-data-model 215, 07-process-flow 231, 08-quality-metrics 173} \u2014 total 1805 LOC."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/scripts/seed-viral-autopilot-bok-seal.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:29:58)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/seed-viral-autopilot-bok-seal.ts",
  "old_string": "    document_lines: {\n      '00-index': 104,\n      '01-mrd': 133,\n      '02-brd': 158,\n      '03-prd': 214,\n      '04-frd': 181,\n      '05-sdd': 334,\n      '06-data-model': 208,\n      '07-process-flow': 217,\n      '08-quality-metrics': 173,\n      total: 1722,\n    },",
  "new_string": "    document_lines: {\n      '00-index': 108,\n      '01-mrd': 133,\n      '02-brd': 164,\n      '03-prd': 217,\n      '04-frd': 191,\n      '05-sdd': 373,\n      '06-data-model': 215,\n      '07-process-flow': 231,\n      '08-quality-metrics': 173,\n      total: 1805,\n    },"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/scripts/seed-viral-autopilot-bok-seal.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-17 - 21b2d649-94ad-4468-9821-20f76eae70a3]]
> * **Próxima Sessão**: [[2026-06-17 - Binance withdrawal and IP unlock troubleshooting]]
%% --- TIMELINE END --- %%

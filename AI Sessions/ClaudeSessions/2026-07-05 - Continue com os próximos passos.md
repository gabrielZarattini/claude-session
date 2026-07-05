# Continue com os próximos passos
**Date:** 2026-07-05 | **Session ID:** `be8df5a5-f15e-42b8-8659-5b49cc9f4cea`

---

## 👤 User *(22:24:16)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(22:24:16)*

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


## 🤖 Claude *(22:24:23)*


## 🤖 Claude *(22:24:23)*

Vou executar o ritual /handson. Começo com todo o pre-flight em paralelo.

## 🤖 Claude *(22:24:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -7",
  "description": "Recent commit history"
}
```

## 🤖 Claude *(22:24:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git status --short",
  "description": "Uncommitted changes"
}
```

## 🤖 Claude *(22:24:25)*


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

## 🤖 Claude *(22:24:26)*


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

## 🤖 Claude *(22:24:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/ 2>/dev/null; echo \"---\"; wc -l HANDOFF.md; echo \"---\"; ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean\"",
  "description": "BoK suites + HANDOFF line count + scratch"
}
```

## 🤖 Claude *(22:24:27)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"",
  "description": "Docker mesh health"
}
```

## 🤖 Claude *(22:24:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "curl -s http://localhost:8001/api/v2/heartbeat",
  "description": "Chroma API v2 health"
}
```

## 🤖 Claude *(22:24:31)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "limit": 71
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> d05b01d docs(readme): v6.85.0 — conformidade MIV + E2E + brand-100 + /miv/ · mesh 9058
> 577035a docs(handoff): seal brand-100 (emoji→lucide + data-viz→MIV) + anticorpos
> 8d65bb2 feat(brand): brand-100 — emoji→lucide + data-viz→MIV em ~40 superfícies
> 855a4ad feat(brand): canvas inspectors sem emoji — 💎→mco, 🔗→lucide
> e412a7e docs(handoff): seal brand-everything (Orquestrador/Core-Fable MIV) + /miv/ completo
> cbe5730 feat(brand): MIV no Orquestrador e Core-Fable — cyan no lugar de violet/amber + ícones lucide
> b92c367 feat(miv): serve o Manual de Identidade Visual completo em /miv/
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>  D proof-manifest.json
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 6 days (healthy)
> mcorch_claude_mem: Up 2 weeks (healthy)
> mcorch_chroma: Up 2 weeks (healthy)
> ---
> mega-brain-dashboard: Up 2 weeks
> mega-brain-webhook: Up 2 weeks (healthy)
> mega-brain-daemon: Up 2 weeks (healthy)
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {"nanosecond heartbeat":1783290271793665395}
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
> 14	| **Loop it.1 — Anticorpo de assinatura owner-scoped (Fix Assets)** | ✅ `scripts/qa/smoke-asset-owner-signing.ts` 6/6 LIVE hermético (owner-sign 200 · cross-sign BLOCKED · enumeração 0 · id-squat neutralizado · is_public=0); fecha Mandato Obstáculo→Síntese |
> 15	| **Loop it.2 — BoK amendment Higgsfield MCP OAuth connector** | ✅ `docs/bok/spaces-evolution/13-amendment-higgsfield-mcp-connector.md` — gate Closed-Loop 3.5 fechado; contrato vivo provado (401 OAuth · 201 DCR · discovery Clerk); FR-SPACES-015..021 + OTD-SPACES-007; código gated na aprovação Sovereign |
> 16	| **Fix Assets — mídia privada assinável só pelo dono (regressão FECHADA)** | ✅ migration `20260703030000` (3 policies owner-scoped + triggers de id anti-claim + data-repair) + normalizador durável em 13 superfícies; `/security-review` CLOSED 9/10; E2E Vision-APROVADO; 90 assets do User 0 vivos |
> 17	| **Spaces 2d compose — drift FECHADO (OTD-SPACES-003)** | ✅ compose vivo E2E via OpenRouter Nano Banana (10 mco) + bucket privado assinado + sentinel de contrato Higgsfield |
> 18	| **Retema MIV do ecossistema + landing fiel + gate TikTok (2026-07-04)** | ✅ design system global MIV (void/cyan/gold/nebula · Playfair/JetBrains) revestindo 47 páginas + login + shell; landing 100% fiel ao original (hero WebGL cinematográfico + texto honesto, iframe); favicon do sigilo consistente + Privacidade/Termos MIV (footer único, conteúdo preservado); 44 páginas polidas via workflow 9-subagentes, E2E 0-erros |
> 19	| **brand-100 — emoji→lucide + data-viz→MIV em ~40 superfícies (2026-07-05)** | ✅ workflow de 7 subagentes: ~90 emoji→lucide (Minerador/Blog/canvas/crew/páginas; avatares→`AVATAR_ICON_MAP` compartilhado), data-viz→MIV (Louvain/node-types/territórios cyan/gold/nebula/teal; blobs magenta→cyan). Minerador+Matrix verificados. mesh **9057** · commits `855a4ad`/`8d65bb2`. Pendente cross-file: pickers de campanha/space |
> 20	| **Brand-everything (Orquestrador/Core-Fable → MIV) + /miv/ completo (2026-07-05)** | ✅ diretiva "tudo vira brand": Orquestrador Visual violet/fuchsia/magenta→cyan + ícones emoji→lucide (`NodeIcon`); Core-Fable amber→cyan; **`/miv/` serve o MIV completo** (site-miv, era 404). mesh **9056** · commits `b92c367`/`cbe5730`. Pendente honesto: emoji de templates/miner + paletas data-viz |
> 21	| **Certificação E2E User Browser + fechamento pt-BR (2026-07-05)** | ✅ E2E de 8 jornadas de usuário real (fresh, ambiente verificado limpo): **flow_works 8/8 · MIV-conformant 8/8 · 0 P0/P1/P2** (2 pass + 6 warn só-P3); anticorpo Lei 1 (squat de `python -m http.server` na porta contaminou o 1º run — subagentes flagaram, fix = verificar o bind antes de rodar). pt-BR fechado em toda a cauda (Arena/Economia/Orquestrador/Matrix/Memory/Video/3D). mesh **9055** · commits `94df8d0`/`63fee7b`/`becf373` |
> 22	| **Conformidade MIV pós-rebrand + tooling ECC-nativo (2026-07-04)** | ✅ auditoria visual E2E de 44 páginas (workflow 8 subagentes agent-browser — real-user nav, hovers, triggers, badges, widgets); 3 fixes sistêmicos (`--accent` cyan · mcoCoins gold · glow CTA) + regressões de marca (onboarding MCORCH · 404/miner/legenda pt-BR · Trial cyan) verificados ao vivo; tooling ECC-nativo (doctor · supply-chain sentinel · session-inspect) + SOP. mesh **9051** · commits `aaa2351`/`75077f6`/`8af7268` |
> 23	
> 24	## Handoff Seal Record (2026-07-05, arco 3) — brand-100: emoji→lucide + data-viz→MIV
> 25	
> 26	**ORO triplet:** Operator = MCORCH Master Execution Agent (+ workflow 7 subagentes) · Reviewer = Sovereign · Owner = Sovereign (custo 0 USD).
> 27	
> 28	Diretiva: *"faça 100% — continue o brand"*. Workflow de 7 subagentes (arquivos disjuntos, cada um tsc-clean nos próprios) rebrandizou **~40 arquivos** (commit `8d65bb2`, +`855a4ad` inspectors):
> 29	- **~90 emoji → lucide de linha**: Minerador (Music/TrendingUp/BarChart3/Heart), Blog, canvas inspectors/nodes/StatusBar (💎→Coins/mco, 🔗→Link2), crew dialogs, páginas diversas, widgets/terminal/gestos. **Avatares de agente** migrados p/ nomes lucide serializáveis (`AVATAR_ICON_MAP` compartilhado + fallback legado) com wire dos **5 render sites** (AgentNode/AgentDetail/ConfigPanel/NewEdgeDialog/picker); PlatformGlyph +linkedin(Briefcase)/twitter(Send).
> 30	- **data-viz → MIV**: Louvain clusters + node-types (Memória/Matrix) → escala cyan/gold/nebula/teal; `SQUAD_COLOR` territórios + **blobs magenta `#ff00ff` → cyan**. Status verde/vermelho/amber preservados (tokens MIV).
> 31	
> 32	Verificado por screenshot (Minerador: zero emoji, ícones de linha; Matrix: grafo cyan MIV, sem texto cru de avatar). tsc 0 · build ✓ · **`/miv/` reconfirmado disponível** (nginx 200, `dist/miv`). Milestone `6f67a6ba-ac0a-4bc4-b24c-2d6a79fe5bd7` · malha **9057**.
> 33	
> 34	**Anticorpos desta sessão (Lei 1/2):** (a) o 1º run do workflow **morreu no limite de sessão da conta** (reset 6:10pm SP) deixando 4 inspectors parciais-mas-válidos — salvei (`855a4ad`) + re-rodei após o reset. (b) subagente com escopo disjunto mudou o campo `avatar` persistido p/ nome-lucide mas **4 render sites fora do escopo mostravam texto cru** → criei `AgentAvatar` compartilhado (padrão `NodeIcon`). (c) **lucide removeu ícones de marca** (Twitter/Instagram/…) — tsc passa mas o rollup quebra; usar neutros (Send/Camera/Globe). Todos registrados em [[project_miv_conformance_pass]].
> 35	
> 36	**Pendente honesto (NÃO é 100% literal — cross-file, próxima leva):** pickers de template de campanha (`CampaignWizard` renderiza `{tpl.icon}` emoji), nós de Space (`SpaceNodeCard`/`ParamHUD`), e territórios/agentes remanescentes que dependem de dados de crew. ~5-8% do brand.
> 37	
> 38	**Survival Laws Self-audit:** Lei 1 ✅ (verificado por screenshot; node UUID+count; /miv/ 200; **pendências declaradas, não "100%"**) · Lei 2 ✅ (anticorpos registrados) · Lei 3 ✅ (session-inspect ~84%; selo dentro do teto) · Lei 4 ✅ (ORO; salvei parcial + integrei cross-file em vez de perder trabalho ou quebrar build).
> 39	
> 40	## Handoff Seal Record (2026-07-05, arco 2) — Brand-everything + MIV completo em /miv/
> 41	
> 42	**ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign · Owner = Sovereign (marca pública; custo 0 USD).
> 43	
> 44	Diretiva Sovereign: *"os não-leaks devem se tornar brand — ataque todos da forma que puder"* + *"não vejo o MIV completo em /miv/"*.
> 45	
> 46	**Arc A — /miv/ completo.** O Manual de Identidade Visual (`site-miv`: 11 seções — cor/tipo/botões/inputs/tags/abas/cards) passa a ser servido em `login.mcorch.com/miv/` via `public/miv/`→`dist/miv/` (mesmo padrão da landing). Estava 404 (caía no fallback SPA). Provado: nginx 200 + 23 seções renderizadas. Commit `b92c367`.
> 47	
> 48	**Arc B — Brand-everything (superfícies de maior visibilidade).** Commit `cbe5730`:
> 49	- **Orquestrador Visual**: nós/edges/canvas/minimap/fundo de violet/fuchsia/magenta → **cyan** (MIV sistema) + gold no gate + nebula na cena; CTA "Executar Pipeline" cyan-glow; **ícones dos nós de emoji → lucide** via componente `NodeIcon` (name→componente, serializável em JSON + retrocompatível com grafos salvos). Verificado por screenshot (canvas 100% cyan + ícones de linha).
> 50	- **Core-Fable**: amber decorativo do HUD → cyan.
> 51	- **Regra firmada:** amber/green/red são tokens de STATUS do MIV (`index.css` `--status-*`) → mantidos; só o decorativo off-palette vira cyan/gold/nebula.
> 52	
> 53	Milestone `08e5a2c0-09d0-47b9-8980-07601d98459e` · malha **9056**.
> 54	
> 55	**Pendente de brand (honesto, Lei 1 — NÃO é "100%"):** emoji em templates de campanha/blog + plataformas do Minerador + páginas diversas (mesmo refactor icon-name+map do `NodeIcon`); paletas categóricas de data-viz (constelação/matrix/memory — precisam de escala categórica MIV-derivada distinguível). Escopo de próxima sessão.
> 56	
> 57	**Survival Laws Self-audit:** Lei 1 ✅ (orquestrador verificado por screenshot; /miv/ 200+render; tsc/build ✓; node UUID+count reais; **pendências de brand declaradas honestamente**) · Lei 2 ✅ · Lei 3 ✅ (session-inspect ~72%, dentro do teto) · Lei 4 ✅ (ORO; deferi emoji-broad/data-viz em vez de estourar budget num refactor grande — "da forma que puder").
> 58	
> 59	## Handoff Seal Record (2026-07-05) — Certificação E2E User Browser + fechamento pt-BR
> 60	
> 61	**ORO triplet:** Operator = MCORCH Master Execution Agent (+ 2 workflows E2E de 8 subagentes: contaminado `wf_70b9f0af` → limpo `wf_52c2e11e`) · Reviewer = Sovereign + a própria auto-certificação material dos subagentes (Lei 1) · Owner = Sovereign (custo **0 USD** — auth throwaway + preview local, guardrail anti-gasto respeitado).
> 62	
> 63	Continuação da sessão pós-rebrand: o Sovereign perguntou *"estamos 100% MIV? Se sim, avance para um E2E User Browser de validação"*. **Resposta honesta (Lei 1):** não é literalmente 100% (deferidos deliberados), mas a conformidade sistêmica + a cauda de pt-BR foram fechadas e **certificadas por E2E**.
> 64	
> 65	**Arc — Validação E2E User Browser (8 jornadas de usuário real).** Multi-step (login → navegação → hover → abrir triggers → preencher rascunho SEM submit), guardrail anti-gasto rígido (inclusive não abrir o diálogo do Minerador que dispara IA). **Veredito da rodada fresh (ambiente limpo):**
> 66	
> 67	| Eixo | Resultado |
> 68	|------|-----------|
> 69	| **flow_works** | **8/8** — o app funciona ponta-a-ponta em todas as jornadas (rotas carregam, wizard avança/volta, 3D renderiza, Realtime SUBSCRIBED) |
> 70	| **MIV-conformant** | **8/8** — void + cyan tático + gold-só-valor + Playfair/JetBrains + glow se mantêm |
> 71	| **pt-BR** | limpo; resíduos P3 fechados no mesmo arco |
> ```

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
> ---
> 9527 HANDOFF.md
> ---
> scratch has files
> ```

## 🤖 Claude *(22:24:40)*


## 🤖 Claude *(22:24:41)*

TypeScript limpo. Agora leio a cauda do HANDOFF (offset ~9127) e o conteúdo do scratch.

## 🤖 Claude *(22:24:42)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 9127,
  "limit": 400
}
```

> **Tool Result (Read)** - ❌ Error
>
> ```
> File content (25091 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
> ```

## 🤖 Claude *(22:24:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null; echo \"--- sprint-priorities ---\"; ls -la .claude/context/sprint-priorities.md 2>/dev/null && wc -l .claude/context/sprint-priorities.md",
  "description": "Scratch contents + sprint-priorities presence"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun 30 01:44 .
> drwx------ 31 ubuntu ubuntu 4096 Jul  5 19:19 ..
> --- sprint-priorities ---
> -rw-rw-r-- 1 ubuntu ubuntu 151653 Jul  3 10:23 .claude/context/sprint-priorities.md
> 273 .claude/context/sprint-priorities.md
> ```

## 🤖 Claude *(22:24:51)*


## 🤖 Claude *(22:24:52)*

A cauda de 400 linhas estoura o budget de tokens. Vou localizar as seções-sufixo (Pending Actions, GraphRAG State) por grep e ler um chunk menor.

## 🤖 Claude *(22:24:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -nE \"^## (Pending Actions|GraphRAG State|Infrastructure|Knowledge Mesh|Key Files|GraphRAG)\" HANDOFF.md | tail -20",
  "description": "Locate suffix section headers"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 9131:## Pending Actions (Commercial Launch)
> 9244:## Infrastructure
> 9291:## GraphRAG State
> 9431:## Key Files
> ```

## 🤖 Claude *(22:24:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -niE \"pending|graphrag|infrastructure|next agent|pr\u00f3ximos|roadmap\" HANDOFF.md | tail -30",
  "description": "Broad locate of pending/graphrag mentions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 6412:**3) Task C — Canvas Studio Phase 4.2b infrastructure (somente, sem fork do canvas-execute).** Decisão arquitetural revisada vs proposal v1: **EXTEND `vm_canvas_executions` em vez de criar `vm_canvas_jobs` novo** — tabela existente cobre 80% do schema necessário (provider, model, parameters, output_url, credits_charged, status, timestamps), separar criaria duas SoT.
> 6414:- Migration `20260516224542_vm_canvas_executions_async_video.sql`: `ADD COLUMN IF NOT EXISTS` para `operation_id` TEXT, `webhook_token` TEXT NOT NULL DEFAULT (replace(gen_random_uuid()::text, '-', '') || replace(gen_random_uuid()::text, '-', '')) — 64 hex chars **sem dependência de pgcrypto** (`gen_random_bytes(integer)` não existe em Supabase Postgres por default), `response_payload` JSONB, `webhook_received_at` TIMESTAMPTZ. Status CHECK enum estendido com `'timeout'` (DROP + ADD constraint pattern). Unique index em webhook_token (defense vs replay). Partial index `idx_vm_canvas_executions_pending_polling` para o watchdog futuro. **NÃO usei `ALTER PUBLICATION supabase_realtime`** — Supabase enable Realtime por default para todas as tabelas (verificado via `useMcorchMemory.ts:91-112` que subscribe `mcorch_nodes` sem nenhuma migration explícita). Types regenerados via `npx supabase gen types typescript --linked` (2362 linhas).
> 6460:- **OTD-V640-001 (RPN 96):** `openclaw secrets reload` requires "scope upgrade pending approval" — bypass-able via daemon restart por hora. Pesquisar Control UI pairing flow para habilitar reload sem restart (zero downtime futuro).
> 6507:### Pending Actions (atualizado)
> 6639:### Pending Actions (atualizado)
> 6641:- ~~[ ] Phase 1.1-1.4: infrastructure + bridge + distribute + index~~ ✅ Selado 2026-05-16
> 6793:Sessão de fechamento da dívida documental do módulo viralmind — portado para o MCORCH (Sprints 1-3 via Antigravity + Sprint 4.1) com um override consciente do BoK Gate. O `/handson` desta sessão identificou a suíte `docs/bok/viralmind/` incompleta (3/9 docs) com o agravante de o `04-frd.md` ser um master prompt estilo CLAUDE.md, não um FRD. O Sovereign decidiu reescrever o FRD de verdade (não flag-and-log) e exigiu profundidade padrão da casa. O handbook foi realocado para `viralmind-dev-handbook.md`; 6 docs foram autorados do zero (`01-mrd`, `02-brd`, `06-data-model`, `07-process-flow`, `08-quality-metrics`, `00-index`) e o `04-frd.md` reescrito como FRD real — todos ancorados no código real: 10 tabelas `vm_*` + 6 enums (migrations `20260514040*`), Edge Functions `fetch-trends` e `canvas-execute`, hooks `useViralTrends`/`useCanvasStudio`/`useAutoSave`. A suíte documenta a visão de 5 módulos (Viral Miner shipped · Canvas Studio shipped · Affiliate Radar parcial · Video Factory + Ads Commander roadmap) com apêndices reconciliando planejado × entregue, espelhando o padrão Convergence Note do `conteudo-v2`. 7 OTDs registrados — destaques: embeddings `vector(1536)` divergentes do padrão `vector(768)` e sem índice HNSW (FMEA-VM-002, RPN 288) e o bucket `canvas-assets` criado público (FMEA-VM-003, RPN 140). Mesh seal via `scripts/seed-viralmind-bok-seal.ts`. A sessão foi selada aqui (com ~51% de contexto restante) deixando a Parte 2 (Canvas Studio Phase 4.2) para uma sessão nova, com plano próprio já selado.
> 6822:              canvas-studio-roadmap · agent-prompts/ · viralmind-dev-handbook.md
> 6882:| `mcorch_nodes` seal `bok-scribe-seal-conteudo-v2-v1` | ✅ id `571bb984-291d-44f2-9c53-1891e665cbed` · stability 0.85 · metadata atualizada com v1_implementation + v2_roadmap |
> 6883:| `docs/bok/viralmind/` migração | ✅ PRD/SDD/FRD + schema-reference + edge-functions-spec + integrations-matrix + canvas-studio-roadmap + agent-prompts/ |
> 6891:| Convergence em 00-index.md + 06-data-model.md | ✅ Mapeamento content_canvas_* (planejado) → vm_* (real) + roadmap v2 tldraw reservado |
> 6921:    Mesh seal node → metadata atualizada com v1+v2 roadmap
> 6980:| `docs/bok/mcorch-constellation/08-quality-metrics.md` | ✅ Quality Philosophy: 98% target justificado + quality-as-moat + roadmap FMEA v5.8→v5.9→Commercial |
> 7052:| `docs/bok/mcorch-constellation/06-data-model.md` | ✅ 16 tabelas + 30 migrations chronology + RLS catalogue + GraphRAG node/edge types + tenant isolation map |
> 7142:| `HANDOFF.md` — pending action | ✅ API key Google marcada como excluída via AI Studio (`aistudio.google.com/app/api-keys`), não Cloud Console |
> 7194:**Test coverage:** Elevado de 1 → 4 arquivos, 1 → 66 testes. `billing.test.ts` (22 testes): COIN_COSTS shape, deductMcoCoins delegando exclusivamente para RPC (nunca deduções client-side), getMcoBalance retorna 0 em perfil inexistente, hasSufficientBalance exact/over/under, checkAndDeductCoins abortando antes do RPC quando saldo insuficiente — invariante de billing crítico coberto. `useOrchestrationStore.test.ts` (29 testes): shape default 8 nós / 9 arestas, todas as 7 transições de estado da máquina (idle→pending→running→done/error/blocked), updateNodeStatus isolado (apenas nó alvo muda), resetNodeStatuses, setRunning idempotente, updateNodeData merge parcial, savePositions + readback de posições do localStorage. Coverage provider v8 instalado com reporter text+html.
> 7258:Sessão de hygiene pós-Settings Sovereignty. O `/handson` reportou um alerta crítico — "AIOS Gemini Live key não provisionada" — que ao verificar mostrou ser falso positivo: `GEMINI_API_KEY` já está no vault Supabase (`secrets list`) e `VITE_GEMINI_API_KEY` já está no `.env` local há semanas. O HANDOFF tinha info desatualizada que sobreviveu a múltiplos seals. Junto disso, a Core v2 já está estável em produção há semanas (v5.5.4 + v5.5.5) e duas entradas no menu confundem o usuário — Core v1 oficialmente arquivada. CorePage.tsx movida para `.archive/pages/` via `git mv` (histórico preservado), rota `/dashboard/core` redireciona para `/dashboard/core-v2`, label "Core v2" promovida para "Core" e ícone `BrainCircuit` (unused) removido. Zero TypeScript errors, build passa em 21.47s, nenhum chunk órfão. Ambos pending actions (#8 Commercial Launch + decisão CorePage) marcados como resolvidos.
> 7266:| `HANDOFF.md` Pending Action #8 (Gemini Live) | ✅ Marcado como resolvido — falso positivo do handson |
> 7448:      → SELECT scheduled_social_posts WHERE scheduled_for <= NOW() AND status=pending
> 7640:### Pending Actions (atualizado)
> 7860:| `.claude/references/{supabase-edge-functions,mcorch-schema}.md` | ✅ 34 edge functions catalogadas + schema GraphRAG completo (508 linhas) |
> 7888:│   └── mcorch-schema.md             ← schema GraphRAG + RPCs
> 8154:Sessão de diagnóstico, recuperação e evolução: chroma corrigido para healthy, MemoryPage restaurada à essência d3-force orgânica, GraphRAG expandido de 526 para 2065 nós com AIOS grounding multi-bucket (26+ nós com stats header), Matrix com paginação completa, handoff v2 protocol escrito e ativado como slash command.
> 8174:| `README.md` | ✅ v5.0.0-zeta · neural_mesh 2065 nós · 2120 edges · Phase Zeta badge · roadmap atualizado |
> 9131:## Pending Actions (Commercial Launch)
> 9244:## Infrastructure
> 9291:## GraphRAG State
> 9330:- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 9392:| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 9444:| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> ```

## 🤖 Claude *(22:25:02)*

Vou ler a seção de Pending Actions e GraphRAG State (chunks pequenos).

## 🤖 Claude *(22:25:03)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 9131,
  "limit": 115
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 9131	## Pending Actions (Commercial Launch)
> 9132	
> 9133	### CRITICAL — Must complete before first client
> 9134	
> 9135	🎯. **[✅ ATIVADO + VÍDEO 9:16 AUTÔNOMO — 2026-06-24 · pendente só: editor Studio (módulo-container) + postback ML + publish vertical] Viral Autopilot** — BoK 9/9 selada (`b3398294`). **✅ VÍDEO 9:16 (seal video-9x16-motor-and-autopilot, 2026-06-24):** (C) **RESOLVIDO** — motor HyperFrames determinístico VIVO (Fatia VS-2: `video-bridge.service` render 1080×1920 sha256-idêntico) + integração Autopilot (Fatia VA-V1: `orchestrate-step` enfileira render do ângulo viral REAL, custo no pré-débito do ciclo OTD-VA-010, attach content_library+creative_metrics OTD-VA-014) — provado E2E real (artigo Roborock → render 9:16 → biblioteca, saldo intacto prepaid). BoK Amendment v0.2 (FR-VA-022..026 + SOP `autopilot-video-9x16.md`) + flip OTD-VS-005 A→C (editor = módulo-container open-design, embed in-SPA inviável por React 19/18). `/security-review` SAFE ×2. **Próximo do vídeo:** **editor HyperFrames Studio** (módulo-container: deepsearch da API `@hyperframes/studio` → app React 19 → bridge → módulo frontend → vhost `studio.mcorch.com` [DNS Sovereign]) + **1º ciclo pago de vídeo witnessed** (habilitar `video_enabled` + GO) + (D) postback ML real + publish vertical TikTok/IG/YT (PR-VA-021, OAuth+App Review). **— histórico v6.48.0:** **✅ ATIVAÇÃO (seal autopilot-activation-security-hardening):** (A) heartbeat pg_cron `autopilot-cadence */15` jobid 3 `active` (migration `20260623040000`) + **1º ciclo PAGO real** `947ef8b5` (débito 22/refund 2, saldo 5096→5076) DONE; (B) **FR-VA-018** trend-informed angle com gate de fonte `sanitizeTrendTitle` + paridade pt-BR no sentinel (OTD-VA-018) DONE. Restam só (C) mídia 9:16 + (D) postback ML real. **Motor autônomo R1+R2+R3+R4 COMPLETO e provado zero-cost.** ✅ **Fatia 2 (cadência R2 + loop R3 + UI, commits `686bae3`→`bfd178b`):** SOP Lei 2 `autopilot-cron-identity.md` (OTD-VA-008 fechado) · migrations `20260620120000..120300` (`autopilot_plans`/`autopilot_cycles` FK composta tenant + RPCs `begin`/`finalize_autopilot_cycle` atômicos sob advisory-lock, service-role-only) · 6 edge fns deployadas (`autopilot-run` executor + `-cadence-cron` driver pg_cron + `-analyze` FR-VA-010 + `-collect` FR-VA-008 + `orchestrate-content` FR-VA-016 prepaid + `orchestrate-step` FR-VA-011 inject) · UI `/dashboard/autopilot` (`useAutopilot`+`AutopilotPage`). `/security-review` SAFE 3× · 3 smokes zero-cost (31 gates) · render ocular. **PENDENTE:** **(A)** ⚠️ **ação Sovereign** — ativar o **`pg_cron` schedule** que chama `autopilot-cadence-cron` (a função existe+provada; só o JOB pg_cron é ativação Sovereign-side, `Bearer SB_SECRET_KEY` via Vault) + rodar o **1º ciclo PAGO real** (mco real), gated nos 2 blockers de saída visível diagnosticados na Fatia 1b: **CF WAF skip `/wp-json/*`** + **OpenAI image model access**; **(B)** `fetch-trends`/`vm_trends`→pauta do ângulo viral (FR-VA-018, último item autônomo); **(C)** mídia viral 9:16 + TikTok/IG/YT (fase 2); **(D)** provar postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER). Constraints chave (cravados no código): `N_runs=prod×rede×ab_variants`, imagem no bundle de 10, refund crédito-positivo (NUNCA deduct negativo — anti-mint `20260603220000:45`), FK composta tenant-escopada, analyze inline=prepaid (reserva de 2 só vira actual com dado real).
> 9136	
> 9137	🌌. **[EM ANDAMENTO — Phase Epsilon V9] Unified Sensorial Canvas — Fases 3.5-3.10** — Fases 3.1-3.4 ✅ (scaffold rota/store/shell 72-28 + Code Network R3F InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; E2E ocular nos 3 modos; commits `210b90d`/`d832084`/`4940b4d`/`38d9760`/`769acb1`). **Restam:** **3.5** Sinapses inter-rede (arestas **REAIS** de `mcorch_edges` cruzando código↔memória, lit só no modo Universo — nunca fabricar) · **3.6** fly-to (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.7** layout/perf (`OTD-UCANVAS-PERF` — a query do código leva **~30s** com 2 canvases; considerar Louvain em Web Worker / streaming do grafo / lazy do backdrop) · **3.8** executar a poda do squad-coloring (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`. BoK selada (PR-025 · FR-043..049 · NFR-023/024 · SDD §9). **3 páginas legadas (matrix/memory/core-fable) preservadas como backup até 3.9.**
> 9138	
> 9139	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 9140	
> 9141	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 9142	
> 9143	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 9144	
> 9145	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 9146	
> 9147	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 9148	
> 9149	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 9150	
> 9151	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 9152	
> 9153	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 9154	
> 9155	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 9156	
> 9157	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 9158	   ```bash
> 9159	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 9160	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 9161	   ```
> 9162	
> 9163	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 9164	
> 9165	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 9166	
> 9167	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 9168	
> 9169	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 9170	
> 9171	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 9172	
> 9173	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 9174	
> 9175	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 9176	
> 9177	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 9178	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 9179	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 9180	
> 9181	### SOCIAL — Next steps
> 9182	
> 9183	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 9184	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 9185	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 9186	
> 9187	### NON-CRITICAL
> 9188	
> 9189	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 9190	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 9191	- `browserslist` — ✅ updated (2026-04-26)
> 9192	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 9193	
> 9194	### GITNEXUS MCP — Next steps
> 9195	
> 9196	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 9197	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 9198	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 9199	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 9200	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 9201	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 9202	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 9203	
> 9204	### PHASE EPSILON — Next iterations
> 9205	
> 9206	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 9207	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 9208	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 9209	
> 9210	### CORE — Next iterations
> 9211	
> 9212	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 9213	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 9214	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 9215	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 9216	
> 9217	### PHASE DELTA — Next iterations
> 9218	
> 9219	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 9220	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 9221	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 9222	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 9223	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 9224	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 9225	
> 9226	### USUÁRIO ZERO — Checklist de validação
> 9227	
> 9228	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 9229	- ✅ Stripe sandbox secrets no vault
> 9230	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 9231	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 9232	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 9233	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 9234	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 9235	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 9236	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 9237	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 9238	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 9239	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 9240	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 9241	
> 9242	---
> 9243	
> 9244	## Infrastructure
> 9245	
> ```

## 🤖 Claude *(22:25:04)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 9291,
  "limit": 45
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 9291	## GraphRAG State
> 9292	
> 9293	- **9047 total nodes** (verificado live 2026-07-03 via REST count=exact, fix-assets-private-bucket-signing seal: +handoff `6e2b32b2-d3fe-461f-b656-9c022927bc03` embedded 768d — Fix Assets: exibição de mídia privada owner-scoped em todo o ecossistema [migration `20260703030000` aplicada 3-policies+2-triggers+data-repair; `/security-review` CLOSED 9/10; cross-tenant BLOCKED ao vivo; E2E Biblioteca+Canvas Vision-APROVADO; 90 assets do User 0 vivos]; commits `6e5e005`/`459cd25`/`e3f6f9e`; prev 9045 do seal Spaces 2d compose `a49aa10`)
> 9294	- **9034 total nodes** (verificado live 2026-07-02 via REST count=exact, spaces-1b-code-complete-apply-gated seal: +handoff `209cbcd8-14ca-4fe2-aad3-3ef7a9409d93` embedded 768d — Spaces Fase 1b CÓDIGO-COMPLETO: SOP S1-S13 + migration ledger `20260702190000` (NÃO aplicada — GO gated) + branch canvas-execute ledger-first + client runGraph/clusters + /security-review SOUND c/ 4 fixes + smoke 8 gates pronto; commits `717abcd`..`ef33b67`; prev 9033)
> 9295	- **9033 total nodes** (verificado live 2026-07-02 via REST count=exact, loop-it2-3-reward-weights-spaces-fase1a-final-seal: +handoff `13fd6fe0-372d-4065-a5ae-b25b208718cf` embedded 768d — NFR-VA-010 reward_weights config-as-data no autopilot-analyze [migration `20260702150000` aplicada; resolveRewardConfig fail-safe; smoke 16/16; /security-review NO FINDINGS] + Spaces Fase 1a canvas 72/28 vivo [tabela `spaces` RLS-own migration `20260702170000`; useSpaces+SpaceNodeCard/Spotlight/ParamHUD; vitest 5/5; E2E DB graph=2 nós; Vision-QA APROVADO]; commits `6058e78`/`9ea6ac0`/`271770e`/`3bedef9`; prev 9032)
> 9296	- **9032 total nodes** (verificado live 2026-07-02 via REST count=exact, spaces-bok-seal-and-loop-it1-b5 seal: +handoff `10d8c70b-1e6a-4ca5-a8bf-83687b3f6b28` embedded 768d — suíte BoK spaces-evolution 9/9 completada [seal `8f5fd3fd` documentation_suite + DERIVES_FROM `c4247ef6`→viralmind; 25/25 suítes verdes; Pattern Conformance §11] + B5 Pauta de Receita FR-VA-031 HITL na AutopilotPage [vitest 7/7 · browser-verify User 0 · Vision-QA APROVADO]; commits `4a8fee0`/`367db9b`/`707d9ab`; prev 9023)
> 9297	- **9023 total nodes** (verificado live 2026-07-02 via REST count=exact, loop-it4-b4-ewma-final-seal: +handoff `1ddd4e86-7b89-4d13-9330-b5877c96df32` embedded 768d — B4 EWMA multi-ciclo no analyze [janela M=5 decay 0.5, smoke 13/13 gate L7 de estabilização] + selo final da sessão de loop [it.1 G7/fan-out · it.2-3 vision-gate · it.4 B4]; commit `bbc7ad9`; prev 9022)
> 9298	- **9022 total nodes** (verificado live 2026-07-02 via REST count=exact, loop-it2-3-vision-gate-both-harnesses seal: +handoff `8ddca90b-decb-4ca6-a857-89addf5134bb` embedded 768d — Vision QA gate mecânico nos 2 harnesses [audit-canvas-ui exit-block + e2e-user-zero Finding P1/ux; prova adversarial PNG branco→REPROVADO] + fix print público dist/; commits `8a41457`/`e511862`/`adf849b`; prev 9021)
> 9299	- **9021 total nodes** (verificado live 2026-07-02 via REST count=exact, loop-it1-reshaper-image-anchor-fanout-hygiene seal: +handoff `b31c1336-e693-4dac-9b10-7a743caf2863` embedded 768d — render-decoupling provado resolvido por arquitetura [channel_variants `reused_master` 7 canais no ciclo `77e02fca`] + fatia G7 imagem-pilar por `metadata.pillar_run_id` [smoke 18/18] + fan-out hygiene no autopilot-run; commits `d16ca88`/`b52ea4f`/`75a6e1c`; prev 9020 = seal final it.9 da primária `345cc2a7` [paridade total universo, v6.73.1]; prev 9018/9017 = seals it.5-6/Fase-B; prev 9003)
> 9300	- **9003 total nodes** (verificado live 2026-06-30 via REST count=exact, loop-editor-render-security-hardening seal: +handoff `d02a8570-5195-4206-a918-df3a42423aba` embedded 768d — Loop autônomo 8 iterações: FR-VS-047 editor→pipeline MCORCH [wrap `hyperframes render`, paridade provada 3 níveis + guard smoke + fix TDZ do dual-write de vídeo] + OTD-SEC-006/007 sentinel-wiring [generate-content+lead-score, injeção→403 LIVE] + FR-SEC-014 pt1 [ledger imutável `security_events`, /security-review NO FINDINGS, provado LIVE] + #2 YT/TikTok false-high corrigido; achado npm `hyperframes` license:None; 10 commits `8d59160`..`145f106`; +6 vs prev 8997 [inclui nó video-render `9069bb7d` + atividade Sovereign]; prev 8996)
> 9301	- **8996 total nodes** (verificado live 2026-06-30 via REST count=exact, avatar-fatia2-voice-fatia3a-consent-erase seal: +handoff `c138539f-0365-436a-ad56-c65e013793c6` embedded 768d + milestone Fatia 2 `b51d8de6-e574-42aa-93b7-8fd75d85a717` — Gabriel AI **Fatia 2 (Clone de Voz)** [nó voiceClone + edge `generate-voice` BYOK ElevenLabs/Cartesia fail-closed + code-switch guard FM-AC-013 + voice_profiles RLS-own Vault + RPCs tenant-guarded; migration `20260630120000`; smoke 10/10; browser+VisionQA PASS] + **Fatia 3a (Consent+Erasure LGPD Art.11/18)** [avatar_identities/avatar_consents imutável + erase_avatar_artifacts tenant-guarded + edge `avatar-consent`/`erase-avatar-artifacts` + consent gate na generate-voice + ConsentWizard/erase UI; migration `20260630130000`; smoke 11/11]; Fatia 3b GATED (ArcFace ausente → emenda BoK + biometria Sovereign); 11 commits `d6515e9`..`7913546`; `/security-review` NO FINDINGS ×2; prev 8993)
> 9302	- **8993 total nodes** (verificado live 2026-06-30 via REST count=exact, gabriel-ai-fatia1-spaces-p0-kanban-live seal: +handoff `aba1458e-2df1-4813-a71b-34360bf7417e` embedded 768d — Programa Gabriel AI [deepsearch força-total → BoK `avatar-clone-ai` 10/10 selada nó `ee81987d` GO-HYBRID + Fatia 1 BYOK hedra/cartesia/fal] + Spaces canvas Phase 0 (scaffold promovido) + Kanban painel-de-detalhe + reconciliador vivo não-destrutivo + cron */15; 6 commits `a5814d2`..`71f4c47`; prev 8992 = BoK seal `ee81987d` `documentation_suite` avatar-clone-ai DERIVES_FROM video-studio `c99b7875`)
> 9303	- **8991 total nodes** (verificado live 2026-06-29 via REST count=exact, product-miner-vision-reliability-async seal: +handoff `1c100e2a-34f4-4b0a-a324-d89cba7ab0a8` embedded 768d — reparo de confiabilidade do Minerador (Vision MCP): Gemini Files API 20-100MB + cover-image fallback (rejeita stub <50KB) + `shouldDownloadVideos:true` vídeo rico em todo vídeo + `:free` 429→pago BYOK + síntese audience-fit/confidence/parser tolerante + extração ASSÍNCRONA timeout-proof [`vm_miner_jobs` RLS-owner/realtime + action `mine-async` EdgeRuntime.waitUntil + hook `useMinerJob` Realtime+polling + barra de progresso + notificação]; 10 commits prod-live; prev 8982 verificado live 2026-06-28 via REST count=exact, privacy-policy-google-oauth-compliance seal: +handoff `d5476bb8-c5ea-4dc4-a3c0-86d1e0895456` embedded 768d — política de privacidade endurecida p/ verificação Google OAuth: cláusula treino-IA Limited Use + §6 revogação/exclusão de tokens + §8 aviso de alterações + §5 segurança concreta [criptografia trânsito/repouso]; grounded na política Google + revisão adversarial 4/4; deployed login.mcorch.com/privacy + render browser-verificado; prev 8973 verificado live 2026-06-27 via REST count=exact, social-connect-tiktok-youtube-pinterest seal: +handoff `311a55b1-fb7b-410f-9582-625fb4721619` embedded 768d — conectar redes TikTok/YouTube/Pinterest: gate BoK post-engine + migration social_app_config Vault-cifrada aplicada/provada + helper fail-closed + 4 edge fns OAuth/publisher [deno 8/8, deployadas, 3×402 live] + UI browser-verified Vision-QA-high; FR-PE-013 video-cadence deferido; prev 8969 gabriel-ai-moodboard-vision-qa seal: +handoff `5501a101-f4fb-4431-a9d8-34f551353c95` embedded 768d — 1º ciclo pago vídeo 9:16 witnessed + billing/CTA fixes + LinkedIn cadence E2E + virada brand-persona Gabriel AI/CCIO + blueprint YT/TikTok + nó mood-board multi-foto + mood board 4 retratos Vision-QA-gated + 2 animações DoP + regra Vision QA + canvas prompt.length hardening; prev 8960 creative-assets-spine-fatia1 seal: +handoff `8eb84bce-f0d5-4463-a79b-9de9ab5892b9` embedded 768d — HyperFrames editor LIVE [video-studio.service + vhost SSO + iframe /dashboard/canvas/video] + auth gating ?devLogin + Canvas hydration-race bug fix + projeto 63d406fe recuperado + creative_assets SPINE [migration+RPC service-role-only, dual-write video-bridge/canvas-execute/generate-image, backfill 73, Biblioteca de Assets UI]; prev 8959 hyperframes-studio-blueprint-and-video-billing-fix seal: +handoff `b42e89f9-3636-4ff0-a86e-674ed479d3c5` embedded 768d via trigger — blueprint de integração do HyperFrames Studio [deepsearch `ae8b94c5`, StudioApp zero-props + seam StudioApiAdapter → módulo-container VS-UI] + fix do gap de billing OTD-VA-010 [crédito compensatório idempotente `refund_autopilot_video_enqueue` migration `20260624140000`, smoke 8/8 net-debit-exclui-12, /security-review SAFE]; prev 8958 video-9x16-motor-and-autopilot seal: +handoff `5e470dff-d7b3-4936-a130-2c34350d56c8` embedded 768d via trigger — vídeo 9:16 autônomo: VS-2 motor HyperFrames determinístico vivo [render-core Playwright+FFmpeg 1080×1920 sha256-idêntico, video-bridge.service, bucket, edge poll://] + VA-V1 integração Autopilot [orchestrate-step enfileira render do ângulo real, custo no pré-débito do ciclo, attach content_library+creative_metrics] + flip editor OTD-VS-005 A→C módulo-container; prev 8954 autopilot-activation-security-hardening seal: +handoff `bc175ac9-e8a8-483b-a32f-4660dd0b90ba` embedded 768d via trigger — 3 arcos: Viral Autopilot ATIVADO [1º ciclo pago `947ef8b5` + pg_cron jobid 3] + FR-VA-018 trend angle hardened + segurança social-auth [state HMAC + webhook IG sig] + paridade pt-BR Cyber-Sentinel OTD-VA-018; prev 8946 alertas-video-fatia1-de-n8n seal: +handoff `bb23b9dc-265e-4338-9709-d320371908b4` embedded 768d — alertas CF/security-drift + Vídeo Fatia 1 [video_renders/video_assets/finalize_video_render + edge video-render/poll] + Fatia 1b UI + emenda BoK SDD v1.2 De-n8n; prev 8935 viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 9304	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 9305	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 9306	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 9307	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 9308	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 9309	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 9310	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 9311	- HNSW cosine index operational
> 9312	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 9313	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 9314	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 9315	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 9316	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 9317	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 9318	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 9319	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 9320	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 9321	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 9322	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 9323	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 9324	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 9325	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 9326	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 9327	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 9328	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 9329	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 9330	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 9331	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 9332	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 9333	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 9334	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 9335	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> ```

## 🤖 Claude *(22:25:13)*


## 🤖 Claude *(22:25:13)*

Vou capturar o Sprint Goal do sprint-priorities.md e verificar o `proof-manifest.json` deletado.

## 🤖 Claude *(22:25:15)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -niE \"sprint goal|## sprint|top 3 gap|gap #1|gap closure\" .claude/context/sprint-priorities.md | head -15",
  "description": "Locate sprint goal + top gaps"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 3:**Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 43:**Sprint v6.42.0 — Viral Autopilot BoK 9/9: motor de conteúdo viral autônomo (R1-R4) (2026-06-17)** — `/handson` → diretiva Sovereign de **retomar o objetivo-núcleo de receita** (= o próprio Sprint Goal "distribuição social autônoma operacional"): alimentar redes com conteúdo viral auto-gerado/agendado (tudo de uma vez OU a cada N dias), que a cada ciclo analisa o anterior p/ melhorar os próximos criativos, monetizado c/ afiliado ML. Arco Closed-Loop puro (zero código de produto): **(1) Auditoria material** (workflow 7 agentes, prova path:linha) — R1/R4 parciais vivos, **R2 (recorrência) e R3 (loop auto-melhorável) AUSENTES** (`campaign_metrics` sem writer, `optimization_policy` nunca lida, `self-optimize` sem cron); **(2) 4 decisões soberanas** (AskUserQuestion: suite NOVO · MVP texto+imagem · sinal R3 combo · 3 SKUs); **(3) BoK 9/9** (1889 LOC, FR-VA-001..021, 12 FMEA 4×RPN>100); **(4) Validação Fase 6 em 4 rodadas adversariais** (4 críticos/rodada) + grep determinístico — pegou buraco de segurança real (cron `verify_jwt=false` sem prova service-role in-function) + anti-mint (refund por deduct negativo, que EU introduzi); **(5) seal** (node `b3398294` embedded 768d, DERIVES_FROM marketing-hub). **Prova:** tsc 0 · 3 commits pushed · Phase 5c **SEAL ALLOWED** (10) · mesh **8928** · handoff `496ec17c`. **BoK Gate ABERTO.** Pending: fatia 1 (product-aware + monetize, NÃO depende do cron) + SOP `autopilot-cron-identity.md` (Lei 2/OTD-VA-008) antes da cadência. **Lição:** verificação adversarial multi-rodada foi essencial — cada "fix" meu deixava um resíduo que a rodada seguinte pegava; não auto-declarar GO (Lei 1).
> 176:## 🔴 Top Gap Closures (by leverage)
> ```

## 🤖 Claude *(22:25:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -1 -- proof-manifest.json; echo \"--- current status of file ---\"; ls -la proof-manifest.json 2>/dev/null || echo \"file deleted from worktree\"; echo \"--- is it tracked? ---\"; git ls-files proof-manifest.json",
  "description": "Inspect deleted proof-manifest.json"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> c38519a docs(handoff): seal loop it.1+it.2 — anticorpo assets owner-signing + BoK Higgsfield MCP (mesh 9048)
> --- current status of file ---
> file deleted from worktree
> --- is it tracked? ---
> proof-manifest.json
> ```

## 🤖 Claude *(22:25:18)*


## 🤖 Claude *(22:25:19)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md",
  "offset": 176,
  "limit": 30
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 176	## 🔴 Top Gap Closures (by leverage)
> 177	
> 178	1. ~~**Loop/rotina de cadência**~~ ✅ `audit-4cs.sh` toda segunda 09:00 BRT · `auto-publish-cron.sh` */5min · `watchdog` */5min
> 179	2. ~~**Primeiro run Usuário Zero**~~ ✅ Publicado em mcorch.com · LinkedIn + Twitter gerados · pipeline_runs persistido
> 180	3. ~~**`publish-social` realmente publicar**~~ ✅ Bug JWT corrigido · LinkedIn publicando · Twitter: CreditsDepleted (Free tier API X)
> 181	4. **Instagram App Review Meta** — verificação empresarial necessária para produção com terceiros → bloqueante para onboarding clientes (diferir até User 1)
> 182	5. **Twitter API tier upgrade** — Free tier esgotou créditos de escrita. Upgrade para Basic ($100/mês) desbloqueia publicação no X (diferir até User 1)
> 183	6. ~~**Consolidação N+1 queries**~~ ✅ issues #002/#003/#009 resolvidos (2026-05-04)
> 184	7. ~~**Settings Overhaul**~~ ✅ useUserApiKeys + pref_ai_model + mcoCoins RPC + Testar key + ConfigPanel real data (2026-05-05)
> 185	8. ~~**A2UI live em produção**~~ ✅ parseAgentMessage → AIOSTerminal.onMessage (2026-05-07) — surfaces dinâmicas spawnam automaticamente
> 186	9. ~~**Test coverage hooks críticos**~~ ✅ 66 → 122 testes (useOrchestrationGraph + useKnowledgeMesh + useSubscription) (2026-05-07)
> 187	10. ~~**BoK Scribe v1**~~ ✅ 9 docs · ~29k palavras · grounded em código real · selada na mesh (2026-05-07)
> 188	11. ~~**Phase 2 BoK enrichment**~~ ✅ 6 docs enriquecidos (+227 linhas voz estratégica) (2026-05-08)
> 189	12. ~~**Phase 3 BoK → Agents**~~ ✅ 8-agent system gerado (704 linhas) via /bok-agents-generator (2026-05-08)
> 190	13. ~~**Endurecer FMEA-008 + FMEA-011**~~ ✅ validateContent() em orchestrate-content + checklist obrigatório /migration (2026-05-08)
> 191	14. ~~**LGPD data export**~~ ✅ data-export Edge Function + useDataExport hook + UI (2026-05-08)
> 192	15. ~~**Self-service account deletion**~~ ✅ delete_account() RPC + delete-account Edge Function + useDeleteAccount + modal (2026-05-08)
> 193	16. ~~**FMEA-005** (RPN 144) — smart chunked embeddings~~ ✅ Selado 2026-05-08 — `splitChunks()` + batch API + `averageVectors()` · zero truncação silenciosa para nós grandes
> 194	17. ~~**Deploy para produção**~~ ✅ Confirmado 2026-05-08 — data-export + delete-account em produção · migration aplicada
> 195	18. **Phase Commercial** — Stripe live keys + first external user onboarding. Todos os blockers LGPD removidos.
> 196	19. **Redesign completo com base no MIV** — Alinhamento visual da plataforma com a identidade definida no MIV (Three.js, tipografia Editorial, paleta de cores harmoniosa) → OTD-MIV-REDESIGN.
> 197	
> 198	---
> 199	
> 200	## 🛠️ Skills a criar ou evoluir
> 201	
> 202	| Skill | Ação | Gatilho |
> 203	|-------|------|---------|
> 204	| `feature` | Evoluir para incluir scaffold de edge function junto | `/feature` |
> 205	
> ```

## 🤖 Claude *(22:25:36)*


## 🤖 Claude *(22:26:01)*

═══════════════════════════════════════════════════════════
  HANDSON — **brand-100 (emoji→lucide + data-viz→MIV)** · seal 2026-07-05 (arco 3)
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
  Fase selada: **brand-100** — ~40 superfícies rebrandizadas (workflow 7 subagentes): ~90 emoji→lucide + data-viz categórico→escala MIV (cyan/gold/nebula/teal). Encadeada com brand-everything (Orquestrador/Core-Fable→MIV) e a certificação E2E de 8 jornadas (flow 8/8 · MIV 8/8 · 0 P0/P1/P2).
  Últimos commits:
    `d05b01d` — docs(readme): v6.85.0 — conformidade MIV + E2E + brand-100 + /miv/ · mesh 9058
    `577035a` — docs(handoff): seal brand-100 (emoji→lucide + data-viz→MIV) + anticorpos
    `8d65bb2` — feat(brand): brand-100 — emoji→lucide + data-viz→MIV em ~40 superfícies

📂 **MUDANÇAS PENDENTES**
  `D proof-manifest.json` — artefato de QA (Phase 5c/`mcorch-qa-healing`), regenerado a cada `/handoff`. Rastreado no git mas deletado do worktree; **não é mudança real de código**, não conflita. Fora ele: worktree limpo ✅

🏗️ **INFRA** — tudo saudável ✅
  mcorch_chroma:     Up 2 semanas (healthy) — Chroma API v2: **OK** (heartbeat respondeu)
  mcorch_claude_mem: Up 2 semanas (healthy)
  mcorch_vision_mcp: Up 6 dias (healthy)
  mega-brain-{daemon,webhook,dashboard}: Up 2 semanas

🧠 **KNOWLEDGE MESH**
  **~9058 nós** (README/commit `d05b01d`; Task State cita 9057) · 100% embedded 768d HNSW cosine
  Tipos: handoff · milestone · architecture · decision · observation · documentation_suite (BoK seals) · AST (file/function/…)

🔧 **TYPESCRIPT** — Zero erros ✅

📚 **BoK SUITES** (25 slugs em `docs/bok/`)
  Seladas recentes na mesh: spaces-evolution 9/9 (`8f5fd3fd`) · viral-autopilot 9/9 (`b3398294`) · vision-mcp 9/9 (`318862b7`) · avatar-clone-ai 10/10 (`ee81987d`) · agentic-governance 10/10 (`34748570`) · post-engine · security (4-artefato CISO)
  **GATE alert:** nenhum — a última sessão foi puro rebrand (isento do BoK Gate). Se a próxima tocar módulo novo, disparar `/bok-scribe` antes de código.

📌 **SPRINT**
  Goal: *Distribuição social autônoma operacional* — LinkedIn publica ✅; Twitter/Instagram gated até User 1.
  Top gap aberto: **#19 Redesign MIV** (largamente coberto por brand-everything/brand-100; resta a cauda cross-file) · **#18 Phase Commercial** (Stripe live — diferido intencional).

⚡ **PRÓXIMOS PASSOS** (prioridade)
  1. **Cauda de brand (fecha o "100% literal")** — pickers de template de campanha (`CampaignWizard` renderiza `{tpl.icon}` emoji), nós de Space (`SpaceNodeCard`/`ParamHUD`), emoji de templates/miner remanescentes. ~5-8% do brand, mesmo refactor icon-name+map do `NodeIcon`/`AVATAR_ICON_MAP`. **Menor esforço, fecha a diretiva anterior.**
  2. **Viral Autopilot — próximos do vídeo (revenue-critical):** editor HyperFrames Studio (módulo-container `studio.mcorch.com`, DNS Sovereign) + 1º ciclo **pago de vídeo** witnessed (habilitar `video_enabled` + GO) + postback ML real (OTD-VA-007) + publish vertical TikTok/IG/YT (PR-VA-021, OAuth+App Review).
  3. **Unified Sensorial Canvas 3.5-3.10** (Phase Epsilon V9) — sinapses inter-rede reais, fly-to, perf (`OTD-UCANVAS-PERF` query ~30s), poda squad-coloring, paridade+cutover de nav, seal.

⚠️ **ALERTAS**
  Nenhum bloqueador ✅ — TS limpo, containers healthy, worktree efetivamente limpo. Único ponto de atenção: a cauda de brand foi declarada honestamente como **não-100% literal** no último seal (Lei 1) — vale fechá-la ou reafirmar o defer.

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

Recomendação: item **1 (cauda de brand)** é o caminho curto para fechar a diretiva "faça 100%" que ficou explicitamente pendente. Quer que eu ataque a cauda de brand, avance o Viral Autopilot (vídeo), ou outra frente?

## 👤 User *(22:27:17)*

ótimo contine então com os próximos passos

## 🤖 Claude *(22:27:50)*


## 🤖 Claude *(22:27:55)*

O Sovereign autorizou continuar. Vou começar pelo **item 1 — a cauda de brand** (fechar o "100% literal" que ficou pendente), depois seguir para o Viral Autopilot. Isenção de BoK Gate confirmada (é continuação de refactor de marca).

**ORO triplet desta task:**
- Operator: MCORCH Master Execution Agent (+ workflow de subagentes)
- Reviewer: Sovereign
- Owner: Sovereign (marca pública · custo 0 USD)

Primeiro, **scouting material** — preciso do inventário exato de emoji remanescentes e dos padrões reutilizáveis (`NodeIcon`/`AVATAR_ICON_MAP`) antes de orquestrar. Deixo o marcador de capítulo e faço o levantamento em paralelo.

## 🤖 Claude *(22:27:56)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Cauda de brand (100% literal)",
  "summary": "Fechar emoji/data-viz remanescentes: CampaignWizard, Spaces nodes, templates/miner \u2014 reusar NodeIcon/AVATAR_ICON_MAP"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Cauda de brand (100% literal)". Continue your current work.'}]
> ```

## 🤖 Claude *(22:28:03)*


## 🤖 Claude *(22:28:03)*

Agora o scanner de emoji e a leitura dos padrões reutilizáveis, em paralelo.

## 🤖 Claude *(22:28:13)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "python3 - <<'PY'\nimport os, re, sys\n\n# Emoji / pictograph ranges (skip plain arrows that may be legit code, but include common decorative)\nranges = [\n    (0x1F300,0x1FAFF),  # symbols/pictographs/emoji/supplemental\n    (0x2600,0x27BF),    # misc symbols + dingbats\n    (0x2B00,0x2BFF),    # misc symbols and arrows (stars etc)\n    (0x1F000,0x1F0FF),  # mahjong/dominos/cards\n    (0xFE00,0xFE0F),    # variation selectors (emoji presentation)\n    (0x2190,0x21FF),    # arrows (may be legit \u2014 will report but flaggable)\n    (0x2300,0x23FF),    # misc technical (\u23f1 \u2699 etc live in 2600 though)\n]\ndef is_emoji(ch):\n    o = ord(ch)\n    for a,b in ranges:\n        if a<=o<=b:\n            return True\n    return False\n\nhits = {}\nfor root,dirs,files in os.walk('src'):\n    dirs[:] = [d for d in dirs if d not in ('node_modules','.git','dist')]\n    for f in files:\n        if not f.endswith(('.ts','.tsx')): continue\n        p = os.path.join(root,f)\n        try:\n            with open(p,encoding='utf-8') as fh:\n                for i,line in enumerate(fh,1):\n                    em = [c for c in line if is_emoji(c)]\n                    if em:\n                        # skip arrow-only lines in comments that are likely legit (\u2192 used in comments)\n                        hits.setdefault(p,[]).append((i,''.join(dict.fromkeys(em)),line.strip()[:110]))\n        except Exception as e:\n            pass\n\n# report grouped, arrows separated\ntotal=0\nfor p in sorted(hits):\n    print(f\"\\n=== {p} ({len(hits[p])}) ===\")\n    for i,em,txt in hits[p]:\n        total+=1\n        print(f\"  {i}: [{em}]  {txt}\")\nprint(f\"\\nTOTAL LINES WITH EMOJI: {total} across {len(hits)} files\")\nPY",
  "description": "Scan src/ for remaining emoji"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === src/components/StorageMedia.tsx (1) ===
>   8: [→]  * dead public URLs (private bucket → HTTP 400) or expiring signed URLs; this re-signs them every time.
> 
> === src/components/canvas/LeftPanel/index.tsx (3) ===
>   33: [→]  * Receitas → vm_canvas_recipes, Assets → vm_canvas_assets,
>   34: [→]  * Tendências → vm_trends, Histórico → vm_canvas_executions.
>   333: [→]  toast.error("Este asset é um Vídeo. Selecione um nó de Vídeo (Imagem → Vídeo) para importá-lo.");
> 
> === src/components/canvas/RightPanel/inspectors/AvatarIdentityInspector.tsx (1) ===
>   240: [✓]  {trained ? "✓ Identidade treinada" : "Treinar identidade"}
> 
> === src/components/canvas/RightPanel/inspectors/CharacterReferenceInspector.tsx (1) ===
>   180: [💎]  <strong className="text-foreground">0 💎</strong> — apenas armazenamento. Suba várias fotos do mesmo
> 
> === src/components/canvas/RightPanel/inspectors/VoiceCloneInspector.tsx (1) ===
>   95: [⇒]  // New sample ⇒ invalidate any prior clone.
> 
> === src/components/canvas/edges/PipelineEdge.tsx (2) ===
>   6: [→]  * Pipeline edge. Same lane (linear "evolução") → solid accent; cross-lane
>   7: [→]  * (desdobramento "deriva") → dashed secondary with a marching-ants animation.
> 
> === src/components/canvas/nodes/AvatarIdentityNode.tsx (1) ===
>   48: [📷]  <span className="shrink-0">{refCount} 📷</span>
> 
> === src/components/canvas/nodes/GenerateImageNode.tsx (1) ===
>   63: [💎]  {d.aspectRatio} · {info.coinCost} 💎
> 
> === src/components/canvas/nodes/ImageToVideoNode.tsx (1) ===
>   102: [💎]  {info.coinCost} 💎
> 
> === src/components/canvas/nodes/SceneComposeNode.tsx (1) ===
>   52: [💎]  {d.cost} 💎
> 
> === src/components/canvas/nodes/StyleTransferNode.tsx (1) ===
>   48: [💎]  preset · {d.cost} 💎
> 
> === src/components/core-fable/MegaBrainVisualizer.tsx (3) ===
>   104: [→]  // Blackbody-style temperature ramp: deep ember → orange → gold → white-hot.
>   148: [→]  // Communication state → energy, not paint:
>   219: [→]  // Temperature: hot inner rim → cooler rim, plus filament heat,
> 
> === src/components/core/AIOSTerminal.tsx (2) ===
>   1274: [→]  // Envelope: word boundary → intensity pulse
>   1856: [→]  {/* Mic: Live Mode → PCM streaming | Normal → Web Speech VAD */}
> 
> === src/components/creative/AssetDetailDialog.tsx (1) ===
>   86: [→]  // Instagram → Reel (graph.instagram.com, instagram_business_content_publish). TikTok → Direct Post
> 
> === src/components/gestures/GestureController.tsx (5) ===
>   11: [→]  * - Point → move cursor + click on depth push (z-axis)
>   12: [→]  * - Pinch → zoom in/out or pan the page
>   13: [→]  * - Open palm → scroll page
>   14: [→]  * - Fist → open palm transition = zoom burst
>   176: [→]  // === FIST → OPEN PALM: Zoom burst effect ===
> 
> === src/components/graph/CrewWizard.tsx (2) ===
>   19: [→]  //   Door A  → seed the approved 4×4 map (closes on success).
>   20: [→]  //   Door B  → guided from-zero builder: department → capability → name → create. Stays open so
> 
> === src/components/graph/EmptyConstellation.tsx (3) ===
>   7: [→]  //   Door A → seed the approved 4×4 map in one click.
>   8: [→]  //   Door B → open the guided from-zero builder (CrewWizard), owned by the page.
>   52: [→]  Builder guiado: departamento → capability → nome. Adicione um subagente por vez.
> 
> === src/components/landing-v2/Brand.tsx (1) ===
>   36: [→]  <span className="arrow">→</span>
> 
> === src/components/landing-v2/ConstellationField.tsx (1) ===
>   70: [→]  // Nearest-to-core nodes ignite first → the bloom radiates outward.
> 
> === src/components/landing-v2/LandingV2Sections.tsx (5) ===
>   319: [→]  <div><span className="fg">› 09:14</span> <span className="pr">ceo</span> · prioridade <span className="fg">→</
>   320: [→]  <div><span className="fg">› 09:14</span> <span className="pr">pmo</span> · aloca · briefing gerado <span class
>   321: [↔]  <div><span className="fg">› 09:15</span> <span className="pr">pmi</span> · sincroniza <span className="nb">Fig
>   323: [✓]  <div><span className="fg">› 11:03</span> <span className="pr">pmo</span> · QA · peça revisada · dentro do padr
>   500: [→]  // ---------------------------------------------------------------- GUARANTEE → Modo Sombra (honest risk-rever
> 
> === src/components/landing/HeroSection.tsx (3) ===
>   151: [✓]  <span>✓ Sem cartão de crédito</span>
>   152: [✓]  <span>✓ 8 redes sociais</span>
>   153: [✓]  <span className="hidden sm:inline">✓ IA generativa incluída</span>
> 
> === src/components/legal/LegalPage.tsx (1) ===
>   34: [←]  <Link to="/" className="ml-back">← Início</Link>
> 
> === src/components/marketing/IntentOrchestratorPanel.tsx (2) ===
>   11: [→]  /** FR-MH-009 — Intent Orchestrator surface: describe an intent → AI plan → policy engine → HITL approval. */
>   39: [→]  : 'Descreva uma intenção → a IA gera um plano · ações de alto impacto exigem aprovação (HITL)'}
> 
> === src/components/marketing/LeadDetailDialog.tsx (1) ===
>   32: [→]  // 23505 (UNIQUE) → already enrolled; surface a friendly message.
> 
> === src/components/orchestrator/ConstellationMatrix.tsx (3) ===
>   604: [←]  <Star className="h-2.5 w-2.5 mr-1 inline-block" />{hubNode.label} ←{hubNode.callsIn}
>   937: [→]  → {tooltip.callsOut}
>   942: [←]  ← {tooltip.callsIn}
> 
> === src/components/orchestrator/OrchestrationCanvas.tsx (1) ===
>   44: [→]  // Sync full data from store → ReactFlow (preserve positions via spread of n)
> 
> === src/components/orchestrator/PipelineHistoryPanel.tsx (1) ===
>   9: [→]  // the hook's STEP_LABELS; brand steps map to neutral glyphs (LinkedIn → Briefcase, X → Send).
> 
> === src/components/orchestrator/nodes/AgentNode.tsx (1) ===
>   49: [⚡]  <span className="text-[9px] text-white/20">⚡{(data.stabilityScore * 100).toFixed(0)}%</span>
> 
> === src/components/orchestrator/nodes/TriggerNode.tsx (2) ===
>   15: [→]  // MIV: pending = "aguardando" → amber status (was off-brand blue).
>   89: [★]  {/* Product picker (Viral Autopilot FR-VA-012) — featured product = first selected (★). */}
> 
> === src/components/panels/AgentDetail.tsx (2) ===
>   93: [→]  // constellation-v2 (FR-CV2-004): capability-bound subagent → invoke the real module function.
>   172: [→←]  {c.from === agent.id ? '→' : '←'} {otherAgent.name} — {c.label}
> 
> === src/components/panels/NewEdgeDialog.tsx (1) ===
>   75: [→]  <span className="text-muted-foreground">→</span>
> 
> === src/hooks/useAIOSConversations.ts (2) ===
>   30: [→]  context_node_ids: string[]; // all node IDs from contextString → DERIVES_FROM edges
>   158: [→]  // 3. DERIVES_FROM edges → all context nodes (AIOS decision: full contextString, not just bucket)
> 
> === src/hooks/useAgentActivity.ts (2) ===
>   19: [→]  * deps (would recreate the effect on every updateAgentStatus → Error #185 cascade).
>   105: [→]  // Live Logs: project each exec into a stable LogEntry (id keyed on exec id → no dupes).
> 
> === src/hooks/useAutopilot.ts (1) ===
>   94: [→]  // Activate → arm next_run_at to now so the cadence cron picks the plan up on its next tick.
> 
> === src/hooks/useCampaigns.ts (6) ===
>   27: [🚀]  icon: '🚀',
>   38: [🎁]  icon: '🎁',
>   49: [📣]  icon: '📣',
>   60: [💬]  icon: '💬',
>   89: [→]  // MIV: 'completed' is a terminal system state, not a success/error/waiting status → cyan (was off-brand blue)
>   234: [→]  // channel → what campaign-run dispatches. `email` is nurture-dispatch territory (blocked by campaign-run).
> 
> === src/hooks/useCanvasJobsRealtime.ts (2) ===
>   26: [→]  * `queued → success/failed/timeout`, this hook (a) refetches query caches and
>   31: [→]  * the channel level. The callback is the single bridge between Realtime → Zustand,
> 
> === src/hooks/useCanvasStudio.ts (1) ===
>   162: [→]  // empty boot state {nodes:[]} would clobber a rich DB row → all canvas nodes lost (assets survive in
> 
> === src/hooks/useConstellationSigma.ts (2) ===
>   87: [→]  // exact-count head request first, then ALL pages in flight concurrently → wall-clock
>   187: [→]  // Build ownership map: node UUID → squad color
> 
> === src/hooks/useCreateCrew.ts (7) ===
>   15: [→]  //   (a) seedApprovedMap()  → the approved 4×4 map: 1 Core + 4 Leads + N module-bound subagents
>   17: [→]  //                            (Core→Lead) and Reporting (Lead→subagent) hierarchy edges.
>   18: [→]  //   (b) createSubagent()   → the from-zero builder: a single capability-bound subagent, ensuring
>   22: [→]  // history can re-link by key. Agents upsert with ignoreDuplicates → an existing (possibly
>   70: [→]  // Deterministic 3D layout (no Math.random → stable positions across re-seeds): Core at origin,
>   116: [→]  // and the from-zero builder's department→capability selectors.
>   150: [→]  // crew_edges has no unique constraint → dedupe against existing (from::to) before inserting.
> 
> === src/hooks/useCreativeAssets.ts (3) ===
>   33: [→]  /** Public bucket → direct public URL; private → null (use resolveAssetUrl for a signed URL). */
>   40: [→]  * Resolve a viewable URL. Keys off the REAL bucket publicness (public bucket → public URL, else a signed URL),
>   41: [→]  * NOT the `is_public` COLUMN — that column lied on 84 rows (is_public=true on a PRIVATE bucket → dead 400 URL)
> 
> === src/hooks/useCrewOverlay.ts (1) ===
>   69: [🤖]  avatar: a.avatar ?? '🤖',
> 
> === src/hooks/useGeminiLive.ts (3) ===
>   28: [→]  // PCM float32 → int16 → base64
>   41: [→]  // base64 → Int16Array PCM
>   50: [→]  // Int16Array PCM → AudioBuffer (for AudioContext playback)
> 
> === src/hooks/useGenerationLedger.ts (1) ===
>   207: [✓]  ? { title: `"${node.data.label}" — vídeo pronto ✓` }
> 
> === src/hooks/useLeads.ts (2) ===
>   13: [→]  // Board column order (left→right lifecycle). DB stores `status` as text with a CHECK on these 5 values.
>   108: [→]  /** FR-MH-011 — unified per-lead profile from the customer_360 view (security_invoker → RLS-scoped). */
> 
> === src/hooks/useMcpTokens.ts (3) ===
>   8: [→]  // The token is generated ENTIRELY client-side: a 32-byte CSPRNG random → `mcorch_pat_<base64url>`. We hash it
>   53: [→]  /** SHA-256 → lowercase hex. Byte-for-byte identical to the container's `sha256hex` (node:crypto). */
>   61: [→]  /** 32 bytes of CSPRNG entropy → `mcorch_pat_<base64url>`. Never leaves the browser except shown once. */
> 
> === src/hooks/usePublicationMetrics.ts (3) ===
>   7: [→]  // Honest by construction: if the collector pulled no real data, this returns []  → the panel shows "sem dados
>   20: [→]  series: PubSnapshot[];          // chronological (oldest → newest) for the time-series chart
>   42: [→]  // Group by (content_variant_id, platform) → one entry per published post.
> 
> === src/hooks/useSimulation.ts (1) ===
>   35: [→]  message: `${msgs[Math.floor(Math.random() * msgs.length)]} (status → ${newStatus})`,
> 
> === src/hooks/useSmartDelete.ts (3) ===
>   3: [→]  // Flow: requestDelete(post) → probe check-post-existence → open dialog with the right branch →
>   4: [→]  // confirm(mode) → optionally delete-remote-post → local delete. NEVER deletes the local row before the remote
>   77: [→]  // Remote delete failed (502) → KEEP the local anchor (SOP recovery). Do not close the dialog.
> 
> === src/hooks/useSocialAccounts.ts (7) ===
>   12: [→]  // MIV chips: off-palette platform-brand colors (blue/purple/pink) → cyan (system). Neutral zinc
>   16: [💼]  { id: 'linkedin', name: 'LinkedIn', icon: '💼', color: 'bg-cyan-600' },
>   17: [📸]  { id: 'instagram', name: 'Instagram', icon: '📸', color: 'bg-gradient-to-r from-cyan-500 to-cyan-400' },
>   18: [👤]  { id: 'facebook', name: 'Facebook', icon: '👤', color: 'bg-cyan-500' },
>   20: [🎵]  { id: 'tiktok', name: 'TikTok', icon: '🎵', color: 'bg-zinc-900' },
>   21: [️]  { id: 'youtube', name: 'YouTube', icon: '▶️', color: 'bg-red-600' },
>   22: [📌]  { id: 'pinterest', name: 'Pinterest', icon: '📌', color: 'bg-red-500' },
> 
> === src/hooks/useSpaces.ts (1) ===
>   78: [→]  return data ? parseSpaceRow(data as SpaceRow) : null;   // RLS: outro tenant → null → "não encontrado"
> 
> === src/hooks/useSynapses.ts (3) ===
>   9: [↔]  // rows whose endpoints straddle the two RENDERED sets (code graph ↔ memory cloud).
>   49: [→]  /** Batched xyzxyz line-segment positions (code endpoint → memory endpoint). */
>   70: [→]  // Orient each synapse code→memory regardless of edge direction in the mesh.
> 
> === src/hooks/useUserApiKeys.ts (1) ===
>   55: [→]  // unique constraint the view lacks → HTTP 400. `.insert()` routes through the trigger.
> 
> === src/hooks/useVideoRender.ts (2) ===
>   17: [→]  { id: 'faceless', label: 'Faceless', desc: 'Vídeo vertical sem rosto, narrado — pipeline E2E (Gemini → voz → m
>   18: [→]  { id: 'hyperframes', label: 'HyperFrames', desc: 'Render programático HTML → MP4, determinístico (sem IA gener
> 
> === src/hooks/useVisionMcp.ts (1) ===
>   21: [→]  // Versioned Plugin Zip (FR-VM-011). Served as a static asset from public/ → dist/ (nginx) at the path below.
> 
> === src/lib/affiliate.ts (2) ===
>   12: [→]  * NEVER route through `panel.gcrux.com` (CloudPanel admin host → login wall, zero attribution),
>   99: [→]  | { kind: "needs_config" } // no affiliate_tag AND no short link → fail-closed
> 
> === src/lib/agent-task-result.ts (2) ===
>   5: [→]  *   - LLM path (CEA)        → { ok: true, exec_id, agent_name, tokens_*, cost_mcoin, ... }
>   6: [→]  *   - Capability path (v2)  → { status: "done", execution_id, capability_key, result, credits_charged, ... }
> 
> === src/lib/asset-url.ts (3) ===
>   15: [→]  // Everything else is private → signed URL. Keyed off the BUCKET (server truth), never a possibly-stale is_pub
>   43: [→]  * - a full Supabase storage URL (public OR expired-signed) → fresh signed / public URL for its bucket
>   44: [→]  * - a non-storage value (external provider URL, data:/blob: URI, undefined) → returned unchanged
> 
> === src/lib/avatar-identity.ts (1) ===
>   124: [↔]  * Any two CONSECUTIVE pass↔fail disagreements route to `review` (anti-oscillation — avoids paying
> 
> === src/lib/avatar.ts (2) ===
>   14: [⇒]  // Any Portuguese diacritic (used to short-circuit the pt-BR branch: a diacritic ⇒ the text IS Portuguese).
>   57: [⇒]  // language === 'pt-BR': any Portuguese diacritic ⇒ the text is Portuguese, never flag.
> 
> === src/lib/billing.ts (9) ===
>   9: [→]  //               (Starter R$147/500 = $0.053/mco and Pro R$397/2000 = $0.036/mco sell DEARER → more margin the
>   15: [→✓]  //   Per-op markup at the floor: ORCHESTRATION_RUN 10 → 4.4× ✓ · canvas video 125 → 4.0× ✓ · canvas image 12 →
>   21: [→]  IMAGE_GENERATION: 9,     // 1 DALL·E 3 1024² image ($0.04 → 4× at floor). WAS 3 = 1.36× (under-margined) → fix
>   26: [→]  RESHAPE_CREATIVE: 2,     // post-engine FR-CP-003 — 1 batched LLM voicing call (~$0.0006) → 4×-floor. Charged 
>   29: [→]  // ElevenLabs PVC/IVC ~$0.182/1k chars (Multilingual v2) → 36 mco / ~900 chars EN at 4×-floor. Charged on
>   30: [→]  // synthesize only (clone = free config). Flash/Turbo halves char cost → recalibrate when those tiers ship.
>   36: [→]  VISION_DESCRIBE_IMAGE: 2,      // VLM ~$0.0004/img (Gemini Flash) → 4×-floor
>   45: [→]  VIDEO_FACELESS_RENDER: 125,    // faceless E2E pipeline (n8n Gemini→Pollinations→VoxCPM→Remotion→LTX→FFmpeg→QA
>   46: [→]  VIDEO_HYPERFRAMES_RENDER: 12,  // deterministic HTML→MP4 via headless Chrome (no AI legs) ≈ canvas image class
> 
> === src/lib/canvas-node-registry.ts (1) ===
>   59: [→]  label: "Imagem → Vídeo",
> 
> === src/lib/canvas-recipes.ts (4) ===
>   19: [→]  *     Col 0–2 → `generateImage` (Personagem · Frame Inicial · Frame Final)
>   20: [→]  *     Col 3   → `imageToVideo`  (Vídeo 5s)
>   118: [→]  /* ── Pipeline lane grid (Personagem → Frame Inicial → Frame Final → Vídeo) ── */
>   235: [→]  "3 lanes × 4 colunas. Mesmo personagem em 3 cenários: cidade → praia → floresta. Ativa o modo Pipeline.",
> 
> === src/lib/meta.ts (4) ===
>   48: [→]  /** A row exists at all → user has pasted credentials. */
>   61: [→]  /** Token expired or explicitly flagged → UI shows the red re-auth banner (PROC self-healing). */
>   69: [→]  /** Token still valid but within the reauth window (≤ N days) → soft nudge. */
>   77: [→]  if (expiresAt <= now) return false; // already expired → metaNeedsReauth handles it
> 
> === src/lib/node-registry.ts (2) ===
>   59: [→]  /** Basics quick-access tab → resolves to canonical types (NR-SPACES-006). */
>   128: [→]  * HANDLE_DATA_TYPE — best-effort handle-id → PortDataType inference (Phase 0).
> 
> === src/lib/smart-delete.ts (3) ===
>   29: [→]  *  - 'remote'    → deletable + still up (or unconfirmed): offer [network+local] / [local only]
>   30: [→]  *  - 'gone'      → confirmed not online: local-only ("já não está online")
>   31: [→]  *  - 'local_only'→ not deletable via API (or credential missing): honest transparency, local-only
> 
> === src/lib/social-app-config.ts (3) ===
>   64: [→]  console: 'developers.tiktok.com → Manage apps',
>   72: [→]  console: 'console.cloud.google.com → APIs & Services → Credentials',
>   80: [→]  console: 'developers.pinterest.com → My apps',
> 
> === src/lib/spaces-execution.ts (6) ===
>   24: [→]  * label prefix ("image-generator #1" → "image-generator"), which addNode has always minted.
>   40: [→]  /* ── S8 — model resolution (Spaces key → server-supported provider/model) ──── */
>   137: [→]  * Resolve a node's inputs from upstream outputs: edge into handle `prompt` + text output → prompt;
>   138: [→]  * edge into handle `reference` + image output → reference image; edge into handle `first-frame` +
>   139: [→]  * image output → input_asset_url do vídeo (S20). Tolerates untyped hydrated edges.
>   270: [→]  /* ── Row → cluster-card mapper (C9 — zod card shape; server CHECKs own invariants) ─ */
> 
> === src/lib/spaces-schema.ts (2) ===
>   88: [→]  modelKey: z.string().optional(),                     // e.g. 'flux.2-pro' → CREDIT_COSTS
>   100: [✨]  icon: z.string().default('✨'),
> 
> === src/lib/sso-cookie.ts (1) ===
>   7: [→]  // the Supabase JWT (ES256 JWKS) and returns 200/401 → 401 redirects to login.mcorch.com/auth?return_to=...
> 
> === src/lib/universe-layout.ts (1) ===
>   11: [→]  export const CODE_SCALE = 1 / 55; // graphology world (±~1000) → scene units (±~18)
> 
> === src/pages/CalendarPage.tsx (1) ===
>   249: [→]  // Resolution maps for the Day Detail — content_id/social_account_id → human-readable properties.
> 
> === src/pages/CampaignDetail.tsx (1) ===
>   171: [→]  {campaign.starts_at ? format(new Date(campaign.starts_at), 'dd/MM/yyyy', { locale: ptBR }) : '—'} → {campaign.
> 
> === src/pages/MemoryPage.tsx (1) ===
>   867: [→←]  {isSource ? '→' : '←'} {e.relation_type}
> 
> === src/pages/SettingsPage.tsx (3) ===
>   56: [✓]  if (ok) toast.success(`${label}: chave válida ✓`);
>   488: [→]  Use Application Passwords (WP Admin → Usuários → Perfil → Senhas de Aplicativo).
>   522: [→]  Gere em: WP Admin → Usuários → Seu Perfil → Senhas de Aplicativo
> 
> === src/pages/SocialAccountsPage.tsx (2) ===
>   73: [→]  // unique constraint the view lacks → HTTP 400 (42P10). Mirrors src/hooks/useUserApiKeys.ts.
>   325: [→]  Gere em: WordPress Admin → Usuários → Seu Perfil → Application Passwords
> 
> === src/pages/SpaceCanvasPage.tsx (2) ===
>   75: [→]  ? `Tipos incompatíveis: ${check.sourceType} → ${check.targetType}`
>   95: [⌘⇧]  // PR-SPACES-012 — atalhos: N / '/' Spotlight · ⌘Z/⌘⇧Z undo/redo (zundo).
> 
> === src/pages/UnifiedCanvasPage.tsx (3) ===
>   119: [→]  {attrs != null && <span>calls→: <span className="text-cyan-300">{String(attrs.callsOut ?? 0)}</span></span>}
>   120: [→]  {attrs != null && <span>→calls: <span className="text-cyan-300">{String(attrs.callsIn ?? 0)}</span></span>}
>   267: [↔]  <Stat label="Código ↔ Memória" value={synapseCount} />
> 
> === src/pages/VideoEditorPage.tsx (1) ===
>   69: [→]  *  A video model sent to generate-video-script hits a text endpoint → 400. */
> 
> === src/pages/VideoStudioEditorPage.tsx (1) ===
>   7: [→]  // in that standalone process → no conflict with this React 18 SPA. SDD: video-studio Amendment v0.4 (VS-UI).
> 
> === src/pages/ViralMinerPage.tsx (2) ===
>   46: [→]  // map to neutral line-icons (X/Twitter → Send, Instagram → Camera, YouTube → Video).
>   195: [→]  // MIV score scale — verde (viral) → cyan (bom) → neutro (fraco); sem laranja/vermelho off-brand.
> 
> === src/store/useUnifiedCanvasStore.ts (1) ===
>   4: [→]  // Feeds both the Code Network (graphology/Louvain → R3F) and the Memory
> 
> === src/test/aios-sql-bridge-smoke.test.ts (9) ===
>   35: [🚀]  console.log("🚀 [SQL Bridge Test] Initializing Supabase clients...");
>   43: [🔐]  console.log("🔐 [SQL Bridge Test] Generating session for gabrielcall@gmail.com...");
>   60: [✅]  console.log(`✅ [SQL Bridge Test] Session obtained. User ID: ${sessionData.user.id}`);
>   63: [🔍]  console.log("🔍 [SQL Bridge Test] CASE 1: Fetching profiles (id, mco_balance)...");
>   82: [🟢]  console.log("🟢 [SQL Bridge Test] CASE 1 Response body:", validText);
>   93: [🚫]  console.log("🚫 [SQL Bridge Test] CASE 2: Trying to fetch forbidden column (email)...");
>   109: [🔴]  console.log("🔴 [SQL Bridge Test] CASE 2 Response body (expected error):", forbiddenColText);
>   115: [🚫]  console.log("🚫 [SQL Bridge Test] CASE 3: Trying to query non-whitelisted table...");
>   131: [🔴]  console.log("🔴 [SQL Bridge Test] CASE 3 Response body (expected error):", forbiddenTableText);
> 
> === src/test/avatar-identity.test.ts (5) ===
>   31: [→]  it("identical descriptions → pass (all 7 match)", () => {
>   81: [→]  it("non-JSON response yields {} → all mismatches → fail (never silent pass)", () => {
>   101: [→]  it("empty → review (conservative)", () => {
>   105: [↔→]  it("consecutive pass↔fail disagreement → review (anti-oscillation, issue #5)", () => {
>   110: [↔]  it("stable majority wins when no pass↔fail oscillation", () => {
> 
> === src/test/billing.test.ts (1) ===
>   50: [→]  it("IMAGE_GENERATION costs 9 (calibrated 2026-06-03 — DALL·E 3 $0.04 → 4× at Enterprise floor)", () => {
> 
> === src/test/canvas-video-async-smoke.test.ts (32) ===
>   46: [🚀]  console.log("🚀 [E2E] Initializing Supabase client...");
>   54: [🔐]  console.log("🔐 [E2E] Generating session for gabrielcall@gmail.com...");
>   71: [✅]  console.log(`✅ [E2E] Session obtained. User ID: ${sessionData.user.id}`);
>   87: [📊]  console.log(`📊 [E2E] User current mco_balance: ${profileBefore?.mco_balance ?? 0}`);
>   89: [💰]  console.log("💰 [E2E] Balance too low. Awarding coins to user...");
>   101: [🎥]  console.log("🎥 [GATE 1] Dispatching video generation request to canvas-execute edge function...");
>   127: [🔴]  console.log("🔴 [GATE 1 LOG] Response body:", executeText);
>   131: [✅]  console.log("✅ [GATE 1] Received response:", executeData);
>   145: [🔍]  console.log(`🔍 [GATE 2] Querying database for execution: ${execId}`);
>   158: [✅]  console.log("✅ [GATE 2] Verified database row matches execution data.");
>   163: [🌐]  console.log(`🌐 [GATE 3] Checking Higgsfield request status for: ${opId}`);
>   171: [✅]  console.log("✅ [GATE 3] Higgsfield status response:", hfData);
>   178: [⏳]  console.log("⏳ [E2E] Polling Higgsfield until generation is completed...");
>   201: [🎉]  console.log("🎉 [E2E] Higgsfield generation completed upstream!");
>   203: [⏳]  console.log("⏳ [E2E] Waiting for live webhook callback processing in our database...");
>   225: [✅]  console.log("✅ [E2E] Webhook processed successfully. Execution status is 'success'.");
>   230: [📅]  console.log("📅 [GATE 4] Checking webhook callback timestamps...");
>   234: [✅]  console.log(`✅ [GATE 4] Webhook timestamps populated: received_at=${finalExecRow.webhook_received_at}`);
>   239: [🔒]  console.log("🔒 [GATE 5] Probing webhook endpoint with an invalid token...");
>   247: [✅]  console.log(`✅ [GATE 5] Verified endpoint security blocks invalid tokens with status: ${secResp.status}`);
>   252: [🔁]  console.log("🔁 [GATE 6] Probing webhook endpoint with duplicate callback token (replay defense)...");
>   259: [✅]  console.log("✅ [GATE 6] Duplicate callback rejected with HTTP 409 Conflict. Idempotency confirmed!");
>   264: [📁]  console.log("📁 [GATE 7] Fetching generated canvas asset metadata...");
>   278: [✅]  console.log(`✅ [GATE 7] Asset validated. Size: ${assetRow.file_size_bytes} bytes, Type: ${assetRow.mime_type}`
>   283: [☁️]  console.log("☁️ [GATE 8] Verifying video asset presence in storage bucket...");
>   293: [✅]  console.log(`✅ [GATE 8] Storage file is accessible at signed URL (HTTP 200). Key: ${storageKey}`);
>   298: [💰]  console.log("💰 [GATE 9] Verifying financial deduction ledger entry...");
>   313: [✅]  console.log(`✅ [GATE 9] Verified atomics deduct: -125 mcoCoins. Transaction ID: ${trans.id}`);
>   323: [📊]  console.log(`📊 [E2E] Profile balance after deduct: ${profileAfter?.mco_balance}. Balance difference: ${balance
>   330: [🔗]  console.log("🔗 [GATE 10] Asserting lineage of the generated video asset...");
>   337: [✅]  console.log("✅ [GATE 10] Lineage perfectly asserted! Video inherits from image " + UPSTREAM_ASSET_ID);
>   339: [🏁]  console.log("🏁 [E2E] All 10 gates from SOP verified successfully! Smoke test complete.");
> 
> === src/test/marketing-hub.test.ts (1) ===
>   52: [→]  it('orders the 5 board statuses new→scored→nurturing→converted→lost', () => {
> 
> === src/test/phase-zeta.test.tsx (1) ===
>   7: [→]  *  2. useAIOSChat auto-saves when streaming transitions true → false (≥ 2 turns)
> 
> === src/test/qa-verifiers.test.ts (8) ===
>   246: [✅]  reportMd: "# Run\n\n**Verdict:** ✅ GO\n",
>   256: [✅]  e2eDeps({ reportMd: "✅ GO", findingsJson: okFindings }),
>   268: [✅]  it("fails when the report omits the ✅ GO badge", () => {
>   270: [🔴]  reportMd: "# Run\n\n**Verdict:** 🔴 NO-GO\n",
>   283: [✅]  const deps = e2eDeps({ reportMd: "✅ GO", findingsJson: blocking });
>   294: [✅]  const deps = e2eDeps({ reportMd: "✅ GO", findingsJson: stale });
>   301: [✅]  const deps = e2eDeps({ reportMd: "✅ GO", findingsJson: "{not json" });
>   319: [✅]  reportMd: "✅ GO",
> 
> === src/test/revenue-pauta.test.ts (3) ===
>   40: [→]  it('derives status: no link → candidato · link without revenue → monetizado · revenue → convertendo', () => {
>   70: [→]  it('guards division by zero (0 impressions → rate 0, never NaN)', () => {
>   76: [→]  it('derives effort from tracked product: product_id → low (anexar link) · null → medium', () => {
> 
> === src/test/smart-delete.test.ts (7) ===
>   7: [→]  it('deletable + still up → remote branch', () => {
>   10: [→]  it('deletable + unconfirmed (probe unknown) → remote branch (offer with caveat)', () => {
>   13: [→]  it('deletable + confirmed gone → gone branch (local-only)', () => {
>   16: [→]  it('not deletable + still up → local_only (honest transparency)', () => {
>   19: [→]  it('not deletable + gone → gone branch', () => {
>   22: [→]  it('credential missing (deletable=false, reason) → local_only', () => {
>   28: [→]  it('maps twitter → X and passes through unknown', () => {
> 
> === src/test/spaces-execution.test.ts (5) ===
>   32: [✨]  icon: '✨',
>   88: [→]  mkNode({ id: 'c', typeId: 'video-generator' }),                 // 2a: dop-lite default → 30
>   89: [→]  mkNode({ id: 'd', typeId: 'sticky-note' }),                     // passive → 0
>   90: [→]  mkNode({ id: 'e', typeId: 'speak' }),                           // unsupported → 0
>   160: [→]  describe('rowToGeneration (C9 row→card mapper)', () => {
> 
> === src/test/spaces-store.test.ts (1) ===
>   25: [→]  it('connect rejects incompatible types (image→text) and accepts compatible (text→text) — FR-SPACES-004', () =>
> 
> === src/test/useKnowledgeMesh.test.ts (2) ===
>   12: [→]  content: "Layout fixes completed — absolute inset-0 → relative w-full h-full",
>   96: [→]  // 1 latest query + 7 priority bucket queries all return the same 2 nodes → dedup → 2 unique
> 
> === src/test/useOrchestrationGraph.test.ts (1) ===
>   117: [→]  it("maps article_generation step → agent-content done", async () => {
> 
> === src/test/useOrchestrationStore.test.ts (3) ===
>   77: [→]  it(`transitions ${from} → ${to} on trigger-campaign`, () => {
>   133: [→]  it("idle → running transition", () => {
>   138: [→]  it("running → idle transition", () => {
> 
> === src/test/vision-gate.test.ts (1) ===
>   18: [✅]  const v = parseVisionVerdict(0, "✅ vision_describe_image\n   APROVADO, sem problemas visuais.");
> 
> === src/types/canvas.ts (1) ===
>   695: [→]  label: "Imagem → Vídeo",
> 
> TOTAL LINES WITH EMOJI: 258 across 97 files
> ```

## 🤖 Claude *(22:28:49)*


## 🤖 Claude *(22:28:55)*

Inventário material capturado: **258 linhas com "emoji"**, mas a maioria são setas técnicas (`→ ← ↔ ⇒`) em comentários/labels e emoji em `console.log` de testes — **não** são violações de marca. Vou filtrar para os pictogramas decorativos user-facing reais e ler os padrões reutilizáveis antes de orquestrar.

Trabalho real identificado (pictogramas renderizados):
- **A** — Templates de campanha `🚀🎁📣💬` (`useCampaigns.ts`) + render em CampaignWizard
- **B** — Ícones sociais `💼📸👤🎵▶️📌` (`useSocialAccounts.ts`)
- **C** — Ícone default de Space `✨` (`spaces-schema.ts`) + render SpaceNodeCard/ParamHUD
- **D** — Canvas nodes `💎`/`📷` + orchestrator `⚡` (5 nós)
- **E** — Fallback de avatar `🤖` (`useCrewOverlay.ts`)
- **F** — Checkmarks `✓` (borderline)

Agora leio os padrões reutilizáveis para replicá-los fielmente.

## 🤖 Claude *(22:28:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"===== NodeIcon definition =====\"; rg -l \"NodeIcon\" src --type ts --type tsx 2>/dev/null\necho \"===== AVATAR_ICON_MAP / AgentAvatar =====\"; rg -l \"AVATAR_ICON_MAP|AgentAvatar\" src 2>/dev/null\necho \"===== PlatformGlyph =====\"; rg -l \"PlatformGlyph\" src 2>/dev/null\necho \"===== CampaignWizard renders tpl.icon =====\"; rg -l \"tpl\\.icon|template\\.icon|\\.icon}\" src 2>/dev/null\necho \"===== SpaceNodeCard / ParamHUD =====\"; rg -l \"SpaceNodeCard|ParamHUD\" src 2>/dev/null\necho \"===== Canvas StatusBar mco (last seal pattern) =====\"; rg -ln \"Coins\" src/components/canvas 2>/dev/null",
  "description": "Locate reusable brand patterns"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== NodeIcon definition =====
> ===== AVATAR_ICON_MAP / AgentAvatar =====
> src/components/panels/NewEdgeDialog.tsx
> src/components/panels/AgentDetail.tsx
> src/components/panels/ConfigPanel.tsx
> src/components/graph/AgentAvatar.tsx
> src/components/graph/AgentNode.tsx
> ===== PlatformGlyph =====
> src/pages/SocialAccountsPage.tsx
> src/hooks/useSocialAccounts.ts
> ===== CampaignWizard renders tpl.icon =====
> src/components/blocks/hero-section.tsx
> src/components/spaces/SpaceNodeCard.tsx
> src/components/spaces/ParamHUD.tsx
> src/components/landing-v2/LandingV2Sections.tsx
> src/components/orchestrator/NodeDetailsPanel.tsx
> src/components/orchestrator/NodePalette.tsx
> src/components/orchestrator/nodes/PublishNode.tsx
> src/components/orchestrator/nodes/AgentNode.tsx
> src/components/orchestrator/nodes/TriggerNode.tsx
> src/pages/BlogEditorPage.tsx
> src/pages/CampaignWizard.tsx
> src/pages/SocialAccountsPage.tsx
> ===== SpaceNodeCard / ParamHUD =====
> src/store/useSpacesStore.ts
> src/pages/SpaceCanvasPage.tsx
> src/components/spaces/SpaceNodeCard.tsx
> src/components/spaces/ParamHUD.tsx
> ===== Canvas StatusBar mco (last seal pattern) =====
> src/components/canvas/TopBar.tsx
> src/components/canvas/RightPanel/shared.tsx
> src/components/canvas/RightPanel/inspectors/ImageToVideoInspector.tsx
> src/components/canvas/RightPanel/inspectors/VoiceCloneInspector.tsx
> src/components/canvas/StatusBar.tsx
> src/components/canvas/AddNodeMenu.tsx
> src/components/canvas/LeftPanel/index.tsx
> src/components/canvas/nodes/VoiceCloneNode.tsx
> src/components/canvas/nodes/CharacterReferenceNode.tsx
> ```

## 🤖 Claude *(22:29:07)*


## 🤖 Claude *(22:29:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"===== NodeIcon (correct search) =====\"; rg -n \"NodeIcon|ICON_MAP|iconFromName|name\u2192|emoji.*lucide\" src/components/orchestrator 2>/dev/null | head -30\necho \"\"; echo \"===== where orchestrator node icons are defined =====\"; rg -ln \"lucide-react\" src/components/orchestrator/nodes 2>/dev/null",
  "description": "Find NodeIcon pattern in orchestrator"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== NodeIcon (correct search) =====
> src/components/orchestrator/NodePalette.tsx:2:import { NodeIcon } from './NodeIcon';
> src/components/orchestrator/NodePalette.tsx:57:          <NodeIcon name={item.icon} className="h-4 w-4 text-cyan-300" />
> src/components/orchestrator/NodeIcon.tsx:25:export function NodeIcon({ name, className }: { name?: string; className?: string }) {
> src/components/orchestrator/nodes/PublishNode.tsx:2:import { NodeIcon } from '../NodeIcon';
> src/components/orchestrator/nodes/PublishNode.tsx:32:          <NodeIcon name={data.icon} className="h-5 w-5 text-cyan-300" />
> src/components/orchestrator/nodes/AgentNode.tsx:2:import { NodeIcon } from '../NodeIcon';
> src/components/orchestrator/nodes/AgentNode.tsx:34:          <NodeIcon name={data.icon} className="h-5 w-5 text-cyan-300" />
> src/components/orchestrator/nodes/TriggerNode.tsx:2:import { NodeIcon } from '../NodeIcon';
> src/components/orchestrator/nodes/TriggerNode.tsx:60:          <NodeIcon name={data.icon} className="h-5 w-5 text-cyan-300" />
> 
> ===== where orchestrator node icons are defined =====
> src/components/orchestrator/nodes/SceneNode.tsx
> src/components/orchestrator/nodes/QualityGateNode.tsx
> src/components/orchestrator/nodes/PublishNode.tsx
> src/components/orchestrator/nodes/AgentNode.tsx
> src/components/orchestrator/nodes/TriggerNode.tsx
> ```

## 🤖 Claude *(22:29:11)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/graph/AgentAvatar.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import {
> 2	  Crown, Bot, Palette, Settings, TrendingUp, Zap, Briefcase, BarChart3,
> 3	  Laptop, Headphones, PenLine, FlaskConical, ShieldCheck, Smartphone, Brain,
> 4	  type LucideIcon,
> 5	} from 'lucide-react';
> 6	
> 7	// MIV: an agent's `avatar` is a serializable lucide string-name (persisted in store/DB), rendered
> 8	// as a line-icon — never an emoji. Shared map so every render site (graph node, detail panel,
> 9	// config list, edge dialog, picker) agrees. Unknown/legacy names (pre-rebrand emoji rows) fall
> 10	// back to raw text — mirrors NodeIcon.tsx.
> 11	export const AVATAR_ICON_MAP: Record<string, LucideIcon> = {
> 12	  crown: Crown,
> 13	  bot: Bot,
> 14	  palette: Palette,
> 15	  settings: Settings,
> 16	  'trending-up': TrendingUp,
> 17	  zap: Zap,
> 18	  briefcase: Briefcase,
> 19	  'bar-chart-3': BarChart3,
> 20	  laptop: Laptop,
> 21	  headphones: Headphones,
> 22	  'pen-line': PenLine,
> 23	  'flask-conical': FlaskConical,
> 24	  'shield-check': ShieldCheck,
> 25	  smartphone: Smartphone,
> 26	  brain: Brain,
> 27	};
> 28	
> 29	export function AgentAvatar({ avatar, className }: { avatar?: string; className?: string }) {
> 30	  const Icon = avatar ? AVATAR_ICON_MAP[avatar] : undefined;
> 31	  if (Icon) return <Icon className={className} />;
> 32	  return <span className={className}>{avatar}</span>;
> 33	}
> 34	
> ```

## 🤖 Claude *(22:29:11)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useSocialAccounts.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
> 2	import { supabase } from '@/integrations/supabase/client';
> 3	import { useAuth } from '@/hooks/useAuth';
> 4	import { toast } from 'sonner';
> 5	import { edgeErrorMessage } from '@/lib/edge';
> 6	import type { Tables } from '@/integrations/supabase/types';
> 7	import type { Database } from '@/integrations/supabase/types';
> 8	
> 9	type SocialAccount = Tables<'social_accounts'>;
> 10	type SocialPlatform = Database['public']['Enums']['social_platform'];
> 11	
> 12	// MIV chips: off-palette platform-brand colors (blue/purple/pink) → cyan (system). Neutral zinc
> 13	// (X/TikTok) kept. `icon` is a string fallback rendered by SocialAccountsPage's <PlatformGlyph>
> 14	// (out of this file's scope) — see note in that page; brand glyphs already cover most platforms.
> 15	export const SUPPORTED_PLATFORMS: { id: SocialPlatform; name: string; icon: string; color: string }[] = [
> 16	  { id: 'linkedin', name: 'LinkedIn', icon: '💼', color: 'bg-cyan-600' },
> 17	  { id: 'instagram', name: 'Instagram', icon: '📸', color: 'bg-gradient-to-r from-cyan-500 to-cyan-400' },
> 18	  { id: 'facebook', name: 'Facebook', icon: '👤', color: 'bg-cyan-500' },
> 19	  { id: 'twitter', name: 'Twitter / X', icon: '𝕏', color: 'bg-zinc-800' },
> 20	  { id: 'tiktok', name: 'TikTok', icon: '🎵', color: 'bg-zinc-900' },
> 21	  { id: 'youtube', name: 'YouTube', icon: '▶️', color: 'bg-red-600' },
> 22	  { id: 'pinterest', name: 'Pinterest', icon: '📌', color: 'bg-red-500' },
> 23	];
> 24	
> 25	export function useSocialAccounts() {
> 26	  const { user } = useAuth();
> 27	  const queryClient = useQueryClient();
> 28	
> 29	  const accountsQuery = useQuery({
> 30	    queryKey: ['social_accounts', user?.id],
> 31	    queryFn: async () => {
> 32	      const { data, error } = await supabase
> 33	        .from('social_accounts')
> 34	        .select('id, user_id, platform, platform_user_id, platform_username, is_active, token_expires_at, scopes, metadata, created_at, updated_at')
> 35	        .order('created_at', { ascending: false });
> 36	      if (error) throw error;
> 37	      return data as SocialAccount[];
> 38	    },
> 39	    enabled: !!user,
> 40	  });
> 41	
> 42	  const disconnectAccount = useMutation({
> 43	    mutationFn: async (id: string) => {
> 44	      // Privileged disconnect: disconnect_social() (SECURITY DEFINER, scoped to auth.uid()) deletes
> 45	      // the row AND revokes the orphaned Vault secrets (access_token + refresh_token). A plain
> 46	      // DELETE through the masked view would delete only the base row and leak the plaintext token.
> 47	      const { error } = await supabase.rpc('disconnect_social', { p_account_id: id });
> 48	      if (error) throw error;
> 49	    },
> 50	    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['social_accounts'] }),
> 51	  });
> 52	
> 53	  const initiateOAuth = async (platform: SocialPlatform) => {
> 54	    const { data, error } = await supabase.functions.invoke('social-auth-init', {
> 55	      body: { platform, redirect_uri: `${window.location.origin}/social/callback` },
> 56	    });
> 57	
> 58	    if (error) {
> 59	      const msg: string = error?.message ?? '';
> 60	      if (msg.includes('LinkedIn not configured')) {
> 61	        toast.error('Configuração Pendente: As credenciais do LinkedIn não estão configuradas no servidor.');
> 62	      } else if (msg.includes('Instagram') || msg.includes('Facebook not configured')) {
> 63	        toast.error('Configuração Pendente: As credenciais do Instagram/Facebook não estão configuradas no servidor.');
> 64	      } else if (msg.includes('Twitter') || msg.includes('X not configured')) {
> 65	        toast.error('Configuração Pendente: As credenciais do Twitter/X não estão configuradas no servidor.');
> 66	      } else {
> 67	        // For platforms whose edge fn returns a structured non-2xx body (e.g. 402
> 68	        // `<platform>_not_configured` with a PT-BR `action`), surface that exact message.
> 69	        const surfaced = await edgeErrorMessage(error, `Erro ao conectar ${platform}: ${msg || 'Tente novamente.'}`);
> 70	        toast.error(surfaced);
> 71	      }
> 72	      throw error;
> 73	    }
> 74	
> 75	    if (data?.error) {
> 76	      const serverMsg: string = data.error;
> 77	      if (serverMsg === 'LinkedIn not configured') {
> 78	        toast.error('Configuração Pendente: As credenciais do LinkedIn não estão configuradas no servidor.');
> 79	      } else {
> 80	        // 200-with-error-body path: prefer the PT-BR `action` hint when present (402 contract).
> 81	        const action: string | undefined = (data as { action?: string }).action;
> 82	        toast.error(action ? `${serverMsg} — ${action}` : `Erro ao conectar ${platform}: ${serverMsg}`);
> 83	      }
> 84	      throw new Error(serverMsg);
> 85	    }
> 86	
> 87	    if (data?.url) {
> 88	      window.location.href = data.url;
> 89	    }
> 90	    return data;
> 91	  };
> 92	
> 93	  // A connection needs a manual reconnect ONLY when its refresh chain is genuinely broken —
> 94	  // never merely because the ~1h OAuth access token has elapsed. The access token is renewed
> 95	  // silently on demand (publish-social) and proactively (self-heal cron) via the stored
> 96	  // refresh_token, so `token_expires_at < now` is normal and expected, not a failure.
> 97	  // `is_active` is the truthful signal: self-heal flips it to false only when a real refresh
> 98	  // fails or no refresh_token exists (self-heal:95/116); refresh-social-token (on success) and
> 99	  // the OAuth callback (on connect) flip it back to true. Keying the "Reconectar" prompt off the
> 100	  // 1h clock produced a false "Token expirado" alarm every hour on perfectly healthy accounts.
> 101	  const needsReauth = (account: SocialAccount) => account.is_active === false;
> 102	
> 103	  return {
> 104	    accounts: accountsQuery.data ?? [],
> 105	    isLoading: accountsQuery.isLoading,
> 106	    error: accountsQuery.error,
> 107	    disconnectAccount,
> 108	    initiateOAuth,
> 109	    needsReauth,
> 110	  };
> 111	}
> 112	
> ```

## 🤖 Claude *(22:29:25)*


## 🤖 Claude *(22:29:26)*

Padrões entendidos: `NodeIcon` (string-name→lucide, fallback texto) e `AgentAvatar`/`AVATAR_ICON_MAP`. Vou ler o `NodeIcon` canônico e todos os render sites para replicar fielmente.

## 🤖 Claude *(22:29:27)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/orchestrator/NodeIcon.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import {
> 2	  Rocket, PenLine, Image, Megaphone, ShieldCheck, Globe, Briefcase, Send,
> 3	  Bot, Clapperboard, Radio, Zap, Target, type LucideIcon,
> 4	} from 'lucide-react';
> 5	
> 6	// MIV: node identity via line-icon (not emoji). `icon` is a serializable string name persisted
> 7	// in the graph JSON; this maps it to a lucide component. Unknown names fall back to raw text so
> 8	// legacy graphs saved with emoji still render.
> 9	const MAP: Record<string, LucideIcon> = {
> 10	  rocket: Rocket,
> 11	  'pen-line': PenLine,
> 12	  image: Image,
> 13	  megaphone: Megaphone,
> 14	  'shield-check': ShieldCheck,
> 15	  globe: Globe,
> 16	  briefcase: Briefcase,
> 17	  twitter: Send,
> 18	  bot: Bot,
> 19	  clapperboard: Clapperboard,
> 20	  radio: Radio,
> 21	  zap: Zap,
> 22	  target: Target,
> 23	};
> 24	
> 25	export function NodeIcon({ name, className }: { name?: string; className?: string }) {
> 26	  const Icon = name ? MAP[name] : undefined;
> 27	  if (Icon) return <Icon className={className} />;
> 28	  // Legacy fallback: render the raw string (e.g. an emoji from a previously-saved graph).
> 29	  return <span className={className}>{name}</span>;
> 30	}
> 31	
> ```

## 🤖 Claude *(22:29:28)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CampaignWizard.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useState } from 'react';
> 2	import { useNavigate } from 'react-router-dom';
> 3	import { motion, AnimatePresence } from 'framer-motion';
> 4	import { ArrowLeft, ArrowRight, Check, Sparkles } from 'lucide-react';
> 5	import { Button } from '@/components/ui/button';
> 6	import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
> 7	import { Input } from '@/components/ui/input';
> 8	import { Textarea } from '@/components/ui/textarea';
> 9	import { Label } from '@/components/ui/label';
> 10	import { Checkbox } from '@/components/ui/checkbox';
> 11	import { Badge } from '@/components/ui/badge';
> 12	import { Calendar } from '@/components/ui/calendar';
> 13	import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover';
> 14	import { useCampaigns, CAMPAIGN_TEMPLATES } from '@/hooks/useCampaigns';
> 15	import CampaignStepsEditor, { type EditorStep } from '@/components/marketing/CampaignStepsEditor';
> 16	import { toast } from '@/hooks/use-toast';
> 17	import type { Database } from '@/integrations/supabase/types';
> 18	import { cn } from '@/lib/utils';
> 19	import { CalendarIcon } from 'lucide-react';
> 20	import { format } from 'date-fns';
> 21	import { ptBR } from 'date-fns/locale';
> 22	
> 23	type SocialPlatform = Database['public']['Enums']['social_platform'];
> 24	
> 25	const ALL_PLATFORMS: { value: SocialPlatform; label: string }[] = [
> 26	  { value: 'instagram', label: 'Instagram' },
> 27	  { value: 'facebook', label: 'Facebook' },
> 28	  { value: 'linkedin', label: 'LinkedIn' },
> 29	  { value: 'twitter', label: 'Twitter/X' },
> 30	  { value: 'tiktok', label: 'TikTok' },
> 31	  { value: 'youtube', label: 'YouTube' },
> 32	  { value: 'pinterest', label: 'Pinterest' },
> 33	  { value: 'wordpress', label: 'WordPress' },
> 34	];
> 35	
> 36	const STEPS = ['Objetivo', 'Público-Alvo', 'Canais', 'Passos', 'Orçamento', 'Cronograma'];
> 37	
> 38	interface WizardData {
> 39	  name: string;
> 40	  description: string;
> 41	  objective: string;
> 42	  intent: string;
> 43	  target_audience: { age_range: string; location: string; interests: string[] };
> 44	  platforms: SocialPlatform[];
> 45	  steps: EditorStep[];
> 46	  budget_cents: number;
> 47	  starts_at: Date | undefined;
> 48	  ends_at: Date | undefined;
> 49	}
> 50	
> 51	const initialData: WizardData = {
> 52	  name: '',
> 53	  description: '',
> 54	  objective: '',
> 55	  intent: '',
> 56	  target_audience: { age_range: '18-45', location: '', interests: [] },
> 57	  platforms: [],
> 58	  steps: [],
> 59	  budget_cents: 0,
> 60	  starts_at: undefined,
> 61	  ends_at: undefined,
> 62	};
> 63	
> 64	export default function CampaignWizard() {
> 65	  const navigate = useNavigate();
> 66	  const { createCampaignWithSteps } = useCampaigns();
> 67	  const [step, setStep] = useState(0);
> 68	  const [data, setData] = useState<WizardData>(initialData);
> 69	  const [interestInput, setInterestInput] = useState('');
> 70	  const [saving, setSaving] = useState(false);
> 71	
> 72	  const applyTemplate = (tpl: (typeof CAMPAIGN_TEMPLATES)[0]) => {
> 73	    setData((d) => ({
> 74	      ...d,
> 75	      objective: tpl.defaults.objective ?? '',
> 76	      platforms: (tpl.defaults.platforms as SocialPlatform[]) ?? [],
> 77	      target_audience: {
> 78	        ...d.target_audience,
> 79	        ...(tpl.defaults.target_audience as unknown as Partial<WizardData['target_audience']>),
> 80	      },
> 81	    }));
> 82	    toast({ title: `Template "${tpl.name}" aplicado!` });
> 83	  };
> 84	
> 85	  const addInterest = () => {
> 86	    if (interestInput.trim()) {
> 87	      setData((d) => ({
> 88	        ...d,
> 89	        target_audience: {
> 90	          ...d.target_audience,
> 91	          interests: [...d.target_audience.interests, interestInput.trim()],
> 92	        },
> 93	      }));
> 94	      setInterestInput('');
> 95	    }
> 96	  };
> 97	
> 98	  const removeInterest = (idx: number) => {
> 99	    setData((d) => ({
> 100	      ...d,
> 101	      target_audience: {
> 102	        ...d.target_audience,
> 103	        interests: d.target_audience.interests.filter((_, i) => i !== idx),
> 104	      },
> 105	    }));
> 106	  };
> 107	
> 108	  const togglePlatform = (p: SocialPlatform) => {
> 109	    setData((d) => ({
> 110	      ...d,
> 111	      platforms: d.platforms.includes(p)
> 112	        ? d.platforms.filter((x) => x !== p)
> 113	        : [...d.platforms, p],
> 114	    }));
> 115	  };
> 116	
> 117	  const canProceed = () => {
> 118	    if (step === 0) return data.name.trim().length > 0;
> 119	    if (step === 2) return data.platforms.length > 0;
> 120	    return true;
> 121	  };
> 122	
> 123	  const handleSubmit = async () => {
> 124	    setSaving(true);
> 125	    try {
> 126	      const channels = [...new Set(data.steps.map((s) => s.channel))];
> 127	      const created = await createCampaignWithSteps.mutateAsync({
> 128	        campaign: {
> 129	          name: data.name,
> 130	          description: data.description || null,
> 131	          objective: data.objective || null,
> 132	          intent: data.intent || null,
> 133	          channels,
> 134	          target_audience: data.target_audience,
> 135	          platforms: data.platforms,
> 136	          budget_cents: data.budget_cents,
> 137	          starts_at: data.starts_at?.toISOString() ?? null,
> 138	          ends_at: data.ends_at?.toISOString() ?? null,
> 139	          status: 'draft',
> 140	        },
> 141	        steps: data.steps,
> 142	      });
> 143	      toast({ title: 'Campanha criada com sucesso!' });
> 144	      navigate(`/dashboard/campaigns/${created.id}`);
> 145	    } catch {
> 146	      toast({ title: 'Erro ao criar campanha', variant: 'destructive' });
> 147	    } finally {
> 148	      setSaving(false);
> 149	    }
> 150	  };
> 151	
> 152	  return (
> 153	    <div className="max-w-2xl mx-auto space-y-6">
> 154	      {/* Header */}
> 155	      <div className="flex items-center gap-3">
> 156	        <Button variant="ghost" size="icon" onClick={() => navigate('/dashboard/campaigns')}>
> 157	          <ArrowLeft className="h-4 w-4" />
> 158	        </Button>
> 159	        <div>
> 160	          <h1 className="text-xl font-heading font-bold text-foreground">Nova Campanha</h1>
> 161	          <p className="text-sm text-muted-foreground">Passo {step + 1} de {STEPS.length}</p>
> 162	        </div>
> 163	      </div>
> 164	
> 165	      {/* Stepper */}
> 166	      <div className="flex items-center gap-1">
> 167	        {STEPS.map((s, i) => (
> 168	          <div key={s} className="flex items-center flex-1">
> 169	            <div
> 170	              className={cn(
> 171	                'flex items-center justify-center h-8 w-8 rounded-full text-xs font-bold shrink-0 transition-colors',
> 172	                i < step
> 173	                  ? 'bg-primary text-primary-foreground'
> 174	                  : i === step
> 175	                  ? 'bg-primary/20 text-primary border-2 border-primary'
> 176	                  : 'bg-muted text-muted-foreground'
> 177	              )}
> 178	            >
> 179	              {i < step ? <Check className="h-3.5 w-3.5" /> : i + 1}
> 180	            </div>
> 181	            {i < STEPS.length - 1 && (
> 182	              <div
> 183	                className={cn(
> 184	                  'h-0.5 flex-1 mx-1 rounded',
> 185	                  i < step ? 'bg-primary' : 'bg-muted'
> 186	                )}
> 187	              />
> 188	            )}
> 189	          </div>
> 190	        ))}
> 191	      </div>
> 192	
> 193	      {/* Content */}
> 194	      <AnimatePresence mode="wait">
> 195	        <motion.div
> 196	          key={step}
> 197	          initial={{ opacity: 0, x: 20 }}
> 198	          animate={{ opacity: 1, x: 0 }}
> 199	          exit={{ opacity: 0, x: -20 }}
> 200	          transition={{ duration: 0.2 }}
> 201	        >
> 202	          <Card>
> 203	            <CardHeader>
> 204	              <CardTitle className="text-lg">{STEPS[step]}</CardTitle>
> 205	            </CardHeader>
> 206	            <CardContent className="space-y-4">
> 207	              {step === 0 && (
> 208	                <>
> 209	                  {/* Templates */}
> 210	                  <div>
> 211	                    <Label className="text-xs text-muted-foreground mb-2 block">Templates rápidos</Label>
> 212	                    <div className="grid grid-cols-2 gap-2">
> 213	                      {CAMPAIGN_TEMPLATES.map((tpl) => (
> 214	                        <Button
> 215	                          key={tpl.objective}
> 216	                          variant="outline"
> 217	                          size="sm"
> 218	                          className="justify-start gap-2 h-auto py-2"
> 219	                          onClick={() => applyTemplate(tpl)}
> 220	                        >
> 221	                          <span>{tpl.icon}</span>
> 222	                          <span className="text-left text-xs">{tpl.name}</span>
> 223	                        </Button>
> 224	                      ))}
> 225	                    </div>
> 226	                  </div>
> 227	                  <div className="space-y-2">
> 228	                    <Label>Nome da campanha *</Label>
> 229	                    <Input
> 230	                      value={data.name}
> 231	                      onChange={(e) => setData((d) => ({ ...d, name: e.target.value }))}
> 232	                      placeholder="Ex: Black Friday 2026"
> 233	                    />
> 234	                  </div>
> 235	                  <div className="space-y-2">
> 236	                    <Label>Descrição</Label>
> 237	                    <Textarea
> 238	                      value={data.description}
> 239	                      onChange={(e) => setData((d) => ({ ...d, description: e.target.value }))}
> 240	                      placeholder="Descreva o objetivo principal da campanha..."
> 241	                      rows={3}
> 242	                    />
> 243	                  </div>
> 244	                  <div className="space-y-2">
> 245	                    <Label>Objetivo</Label>
> 246	                    <Input
> 247	                      value={data.objective}
> 248	                      onChange={(e) => setData((d) => ({ ...d, objective: e.target.value }))}
> 249	                      placeholder="Ex: awareness, engajamento, vendas"
> 250	                    />
> 251	                  </div>
> 252	                  <div className="space-y-2">
> 253	                    <Label>Intenção da campanha</Label>
> 254	                    <Textarea
> 255	                      value={data.intent}
> 256	                      onChange={(e) => setData((d) => ({ ...d, intent: e.target.value }))}
> 257	                      placeholder="O que esta campanha deve comunicar? Vira o tema do conteúdo gerado em cada passo."
> 258	                      rows={2}
> 259	                    />
> 260	                  </div>
> 261	                </>
> 262	              )}
> 263	
> 264	              {step === 1 && (
> 265	                <>
> 266	                  <div className="space-y-2">
> 267	                    <Label>Faixa etária</Label>
> 268	                    <Input
> 269	                      value={data.target_audience.age_range}
> 270	                      onChange={(e) =>
> 271	                        setData((d) => ({
> 272	                          ...d,
> 273	                          target_audience: { ...d.target_audience, age_range: e.target.value },
> 274	                        }))
> 275	                      }
> 276	                      placeholder="Ex: 25-45"
> 277	                    />
> 278	                  </div>
> 279	                  <div className="space-y-2">
> 280	                    <Label>Localização</Label>
> 281	                    <Input
> 282	                      value={data.target_audience.location}
> 283	                      onChange={(e) =>
> 284	                        setData((d) => ({
> 285	                          ...d,
> 286	                          target_audience: { ...d.target_audience, location: e.target.value },
> 287	                        }))
> 288	                      }
> 289	                      placeholder="Ex: Brasil, São Paulo"
> 290	                    />
> 291	                  </div>
> 292	                  <div className="space-y-2">
> 293	                    <Label>Interesses</Label>
> 294	                    <div className="flex gap-2">
> 295	                      <Input
> 296	                        value={interestInput}
> 297	                        onChange={(e) => setInterestInput(e.target.value)}
> 298	                        onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addInterest())}
> 299	                        placeholder="Adicionar interesse..."
> 300	                      />
> 301	                      <Button type="button" size="sm" onClick={addInterest}>
> 302	                        +
> 303	                      </Button>
> 304	                    </div>
> 305	                    <div className="flex flex-wrap gap-1.5 mt-2">
> 306	                      {data.target_audience.interests.map((int, idx) => (
> 307	                        <Badge
> 308	                          key={idx}
> 309	                          variant="secondary"
> 310	                          className="cursor-pointer"
> 311	                          onClick={() => removeInterest(idx)}
> 312	                        >
> 313	                          {int} ×
> 314	                        </Badge>
> 315	                      ))}
> 316	                    </div>
> 317	                  </div>
> 318	                </>
> 319	              )}
> 320	
> 321	              {step === 2 && (
> 322	                <>
> 323	                  <p className="text-sm text-muted-foreground">
> 324	                    Selecione as plataformas para esta campanha
> 325	                  </p>
> 326	                  <div className="grid grid-cols-2 gap-3">
> 327	                    {ALL_PLATFORMS.map((p) => (
> 328	                      <label
> 329	                        key={p.value}
> 330	                        className={cn(
> 331	                          'flex items-center gap-3 rounded-lg border p-3 cursor-pointer transition-colors',
> 332	                          data.platforms.includes(p.value)
> 333	                            ? 'border-primary bg-primary/5'
> 334	                            : 'border-border hover:border-muted-foreground/30'
> 335	                        )}
> 336	                      >
> 337	                        <Checkbox
> 338	                          checked={data.platforms.includes(p.value)}
> 339	                          onCheckedChange={() => togglePlatform(p.value)}
> 340	                        />
> 341	                        <span className="text-sm font-medium">{p.label}</span>
> 342	                      </label>
> 343	                    ))}
> 344	                  </div>
> 345	                </>
> 346	              )}
> 347	
> 348	              {step === 3 && (
> 349	                <>
> 350	                  <p className="text-sm text-muted-foreground">
> 351	                    Componha os passos multicanal. Cada passo dispara o pipeline de conteúdo (orchestrate-content) ao rodar a campanha.
> 352	                  </p>
> 353	                  <CampaignStepsEditor
> 354	                    steps={data.steps}
> 355	                    onAdd={(channel, action) => setData((d) => ({ ...d, steps: [...d.steps, { channel, action }] }))}
> 356	                    onRemove={(_s, idx) => setData((d) => ({ ...d, steps: d.steps.filter((_, i) => i !== idx) }))}
> 357	                  />
> 358	                </>
> 359	              )}
> 360	
> 361	              {step === 4 && (
> 362	                <>
> 363	                  <div className="space-y-2">
> 364	                    <Label>Orçamento total (R$)</Label>
> 365	                    <Input
> 366	                      type="number"
> 367	                      min={0}
> 368	                      step={0.01}
> 369	                      value={data.budget_cents ? (data.budget_cents / 100).toFixed(2) : ''}
> 370	                      onChange={(e) =>
> 371	                        setData((d) => ({
> 372	                          ...d,
> 373	                          budget_cents: Math.round(parseFloat(e.target.value || '0') * 100),
> 374	                        }))
> 375	                      }
> 376	                      placeholder="0.00"
> 377	                    />
> 378	                    <p className="text-xs text-muted-foreground">
> 379	                      Deixe em branco ou zero se não houver orçamento definido
> 380	                    </p>
> 381	                  </div>
> 382	                </>
> 383	              )}
> 384	
> 385	              {step === 5 && (
> 386	                <>
> 387	                  <div className="grid grid-cols-2 gap-4">
> 388	                    <div className="space-y-2">
> 389	                      <Label>Data de início</Label>
> 390	                      <Popover>
> 391	                        <PopoverTrigger asChild>
> 392	                          <Button variant="outline" className={cn('w-full justify-start text-left font-normal', !data.starts_at && 'text-muted-foreground')}>
> 393	                            <CalendarIcon className="mr-2 h-4 w-4" />
> 394	                            {data.starts_at ? format(data.starts_at, 'dd/MM/yyyy', { locale: ptBR }) : 'Selecionar'}
> 395	                          </Button>
> 396	                        </PopoverTrigger>
> 397	                        <PopoverContent className="w-auto p-0">
> 398	                          <Calendar mode="single" selected={data.starts_at} onSelect={(d) => setData((prev) => ({ ...prev, starts_at: d }))} />
> 399	                        </PopoverContent>
> 400	                      </Popover>
> 401	                    </div>
> 402	                    <div className="space-y-2">
> 403	                      <Label>Data de término</Label>
> 404	                      <Popover>
> 405	                        <PopoverTrigger asChild>
> 406	                          <Button variant="outline" className={cn('w-full justify-start text-left font-normal', !data.ends_at && 'text-muted-foreground')}>
> 407	                            <CalendarIcon className="mr-2 h-4 w-4" />
> 408	                            {data.ends_at ? format(data.ends_at, 'dd/MM/yyyy', { locale: ptBR }) : 'Selecionar'}
> 409	                          </Button>
> 410	                        </PopoverTrigger>
> 411	                        <PopoverContent className="w-auto p-0">
> 412	                          <Calendar mode="single" selected={data.ends_at} onSelect={(d) => setData((prev) => ({ ...prev, ends_at: d }))} />
> 413	                        </PopoverContent>
> 414	                      </Popover>
> 415	                    </div>
> 416	                  </div>
> 417	
> 418	                  {/* Review */}
> 419	                  <div className="mt-6 p-4 rounded-lg bg-muted/50 border border-border space-y-2">
> 420	                    <h4 className="font-semibold text-sm flex items-center gap-2">
> 421	                      <Sparkles className="h-4 w-4 text-primary" /> Resumo da Campanha
> 422	                    </h4>
> 423	                    <div className="text-sm space-y-1 text-muted-foreground">
> 424	                      <p><strong className="text-foreground">Nome:</strong> {data.name}</p>
> 425	                      {data.objective && <p><strong className="text-foreground">Objetivo:</strong> {data.objective}</p>}
> 426	                      <p><strong className="text-foreground">Canais:</strong> {data.platforms.join(', ') || 'Nenhum'}</p>
> 427	                      {data.intent && <p><strong className="text-foreground">Intenção:</strong> {data.intent}</p>}
> 428	                      <p><strong className="text-foreground">Passos:</strong> {data.steps.length > 0 ? `${data.steps.length} passo(s)` : 'Nenhum'}</p>
> 429	                      {data.budget_cents > 0 && (
> 430	                        <p><strong className="text-foreground">Orçamento:</strong> R$ {(data.budget_cents / 100).toFixed(2)}</p>
> 431	                      )}
> 432	                      {data.starts_at && (
> 433	                        <p><strong className="text-foreground">Período:</strong> {format(data.starts_at, 'dd/MM/yyyy', { locale: ptBR })} {data.ends_at ? `— ${format(data.ends_at, 'dd/MM/yyyy', { locale: ptBR })}` : ''}</p>
> 434	                      )}
> 435	                    </div>
> 436	                  </div>
> 437	                </>
> 438	              )}
> 439	            </CardContent>
> 440	          </Card>
> 441	        </motion.div>
> 442	      </AnimatePresence>
> 443	
> 444	      {/* Navigation */}
> 445	      <div className="flex justify-between">
> 446	        <Button variant="ghost" onClick={() => (step === 0 ? navigate('/dashboard/campaigns') : setStep(step - 1))}>
> 447	          <ArrowLeft className="h-4 w-4 mr-1" />
> 448	          {step === 0 ? 'Cancelar' : 'Voltar'}
> 449	        </Button>
> 450	        {step < STEPS.length - 1 ? (
> 451	          <Button onClick={() => setStep(step + 1)} disabled={!canProceed()}>
> 452	            Próximo <ArrowRight className="h-4 w-4 ml-1" />
> 453	          </Button>
> 454	        ) : (
> 455	          <Button onClick={handleSubmit} disabled={saving || !canProceed()}>
> 456	            {saving ? 'Criando...' : 'Criar Campanha'} <Check className="h-4 w-4 ml-1" />
> 457	          </Button>
> 458	        )}
> 459	      </div>
> 460	    </div>
> 461	  );
> 462	}
> 463	
> ```

## 🤖 Claude *(22:29:29)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/spaces/SpaceNodeCard.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// SpaceNodeCard — generic render-only node for the Spaces canvas (PR-SPACES-006 / NA-SPACES-002).
> 2	// Ports come from data.ports (built from NODE_PORTS at addNode time); typed handles left(in)/right(out).
> 3	// No I/O here (harness rule): hooks own data, this component owns pixels.
> 4	import { memo } from 'react';
> 5	import { Handle, Position, type NodeProps } from '@xyflow/react';
> 6	import { estimateCost } from '@/hooks/useParamRegistry';
> 7	import type { SpaceNode, NodeStatus, Port } from '@/lib/spaces-schema';
> 8	
> 9	const STATUS_PILL: Record<NodeStatus, string> = {
> 10	  idle: 'bg-muted text-muted-foreground',
> 11	  pending: 'bg-amber-500/15 text-amber-400',
> 12	  running: 'bg-blue-500/15 text-blue-400 animate-pulse',
> 13	  done: 'bg-emerald-500/15 text-emerald-400',
> 14	  error: 'bg-red-500/15 text-red-400',
> 15	  blocked: 'bg-orange-500/15 text-orange-400',
> 16	};
> 17	
> 18	const PORT_COLOR: Record<Port['dataType'], string> = {
> 19	  image: '!bg-cyan-400', text: '!bg-violet-400', video: '!bg-rose-400',
> 20	  audio: '!bg-amber-400', svg: '!bg-lime-400', '3d': '!bg-fuchsia-400',
> 21	};
> 22	
> 23	function portOffset(index: number): number {
> 24	  return 44 + index * 22;
> 25	}
> 26	
> 27	function SpaceNodeCardInner({ id, data, selected }: NodeProps<SpaceNode>) {
> 28	  const inPorts = data.ports.filter((p) => p.direction === 'in');
> 29	  const outPorts = data.ports.filter((p) => p.direction === 'out');
> 30	  const cost = estimateCost({ id, data } as SpaceNode);
> 31	  return (
> 32	    <div
> 33	      className={`rounded-lg border bg-card text-card-foreground shadow-sm min-w-[220px] max-w-[280px] transition-shadow ${
> 34	        selected ? 'border-primary ring-1 ring-primary' : 'border-border'
> 35	      }`}
> 36	    >
> 37	      {inPorts.map((p, i) => (
> 38	        <Handle
> 39	          key={p.id} id={p.id} type="target" position={Position.Left}
> 40	          style={{ top: portOffset(i) }}
> 41	          className={`!h-2.5 !w-2.5 !border-background ${PORT_COLOR[p.dataType]}`}
> 42	          title={`${p.id} (${p.dataType})`}
> 43	        />
> 44	      ))}
> 45	      {outPorts.map((p, i) => (
> 46	        <Handle
> 47	          key={p.id} id={p.id} type="source" position={Position.Right}
> 48	          style={{ top: portOffset(i) }}
> 49	          className={`!h-2.5 !w-2.5 !border-background ${PORT_COLOR[p.dataType]}`}
> 50	          title={`${p.id} (${p.dataType})`}
> 51	        />
> 52	      ))}
> 53	
> 54	      <div className="flex items-center gap-2 border-b border-border px-3 py-2">
> 55	        <span className="text-base leading-none">{data.icon}</span>
> 56	        <span className="truncate text-sm font-medium">{data.label}</span>
> 57	      </div>
> 58	      <div className="px-3 py-2 space-y-1.5">
> 59	        <div className="flex flex-wrap gap-x-3 gap-y-0.5 text-[11px] text-muted-foreground">
> 60	          {inPorts.map((p) => <span key={p.id}>◂ {p.id}</span>)}
> 61	        </div>
> 62	        <div className="flex flex-wrap gap-x-3 gap-y-0.5 text-[11px] text-muted-foreground justify-end">
> 63	          {outPorts.map((p) => <span key={p.id}>{p.id} ▸</span>)}
> 64	        </div>
> 65	      </div>
> 66	      <div className="flex items-center justify-between border-t border-border px-3 py-1.5 text-[11px]">
> 67	        <span className={`rounded px-1.5 py-0.5 ${STATUS_PILL[data.status]}`}>{data.status}</span>
> 68	        <span className="text-muted-foreground">{cost > 0 ? `~${cost} mco` : '0 mco'}</span>
> 69	      </div>
> 70	    </div>
> 71	  );
> 72	}
> 73	
> 74	export const SpaceNodeCard = memo(SpaceNodeCardInner);
> 75	
> ```

## 🤖 Claude *(22:29:29)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/spaces/ParamHUD.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// ParamHUD — right-side parameter panel (28% of the 72/28 law, PR-SPACES-001/002; hybrid model
> 2	// validated by live recon UI-SPACES-009). Schema comes from useParamRegistry (SD-SPACES-002);
> 3	// mutations go through the store — no I/O here.
> 4	import { useSpacesStore } from '@/store/useSpacesStore';
> 5	import { getSchema, estimateCost, type ParamField } from '@/hooks/useParamRegistry';
> 6	import { GenerationCluster } from '@/components/spaces/GenerationCluster';
> 7	import { ReferencePicker } from '@/components/spaces/ReferencePicker';
> 8	import { Input } from '@/components/ui/input';
> 9	import { Textarea } from '@/components/ui/textarea';
> 10	import { Label } from '@/components/ui/label';
> 11	import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
> 12	import type { SpaceNode } from '@/lib/spaces-schema';
> 13	
> 14	/** modelKey/aspectRatio/batch live at data level; everything else is a params.* entry. */
> 15	const DATA_LEVEL_KEYS = new Set(['modelKey', 'aspectRatio', 'batch']);
> 16	
> 17	function FieldControl({ node, field }: { node: SpaceNode; field: ParamField }) {
> 18	  const updateNodeData = useSpacesStore((s) => s.updateNodeData);
> 19	  const updateNodeParams = useSpacesStore((s) => s.updateNodeParams);
> 20	  const current = DATA_LEVEL_KEYS.has(field.key)
> 21	    ? (node.data as Record<string, unknown>)[field.key]
> 22	    : node.data.params[field.key];
> 23	  const setValue = (v: unknown) =>
> 24	    DATA_LEVEL_KEYS.has(field.key)
> 25	      ? updateNodeData(node.id, { [field.key]: v } as Partial<SpaceNode['data']>)
> 26	      : updateNodeParams(node.id, { [field.key]: v });
> 27	
> 28	  switch (field.kind) {
> 29	    case 'textarea':
> 30	      return (
> 31	        <Textarea rows={4} value={(current as string) ?? ''} placeholder={field.labelPt}
> 32	          onChange={(e) => setValue(e.target.value)} />
> 33	      );
> 34	    case 'select':
> 35	      return (
> 36	        <Select value={(current as string) ?? undefined} onValueChange={(v) => setValue(v)}>
> 37	          <SelectTrigger><SelectValue placeholder={field.labelPt} /></SelectTrigger>
> 38	          <SelectContent className="max-h-64">
> 39	            {(field.options ?? []).map((o) => (
> 40	              <SelectItem key={o.value} value={o.value}>{o.labelPt}</SelectItem>
> 41	            ))}
> 42	          </SelectContent>
> 43	        </Select>
> 44	      );
> 45	    case 'stepper':
> 46	      return (
> 47	        <Input type="number" min={field.min} max={field.max} step={field.step}
> 48	          value={Number(current ?? field.min ?? 1)}
> 49	          onChange={(e) => setValue(Math.max(field.min ?? 1, Math.min(field.max ?? 8, Number(e.target.value) || 1)))} />
> 50	      );
> 51	    case 'references':
> 52	      // Amendment 2b/2d — upload + chips; composer usa 2 (S31), imagem usa 4 (S24)
> 53	      return <ReferencePicker node={node} maxActive={node.data.category === 'designer' ? 2 : 4} />;
> 54	    default:
> 55	      return (
> 56	        <Input value={(current as string) ?? ''} placeholder={field.labelPt}
> 57	          onChange={(e) => setValue(e.target.value)} />
> 58	      );
> 59	  }
> 60	}
> 61	
> 62	export function ParamHUD() {
> 63	  const selectedNodeId = useSpacesStore((s) => s.selectedNodeId);
> 64	  const spaceId = useSpacesStore((s) => s.spaceId);
> 65	  const node = useSpacesStore((s) => s.nodes.find((n) => n.id === s.selectedNodeId));
> 66	
> 67	  if (!selectedNodeId || !node) {
> 68	    return (
> 69	      <div className="flex h-full items-center justify-center p-6 text-center">
> 70	        <p className="text-sm text-muted-foreground">Selecione um nó para editar parâmetros</p>
> 71	      </div>
> 72	    );
> 73	  }
> 74	
> 75	  const fields = getSchema(node);
> 76	  return (
> 77	    <div className="h-full overflow-y-auto p-4 space-y-4 bg-sidebar text-sidebar-foreground">
> 78	      <div>
> 79	        <h2 className="text-sm font-semibold flex items-center gap-2">
> 80	          <span>{node.data.icon}</span>{node.data.label}
> 81	        </h2>
> 82	        <p className="text-xs text-muted-foreground mt-0.5">{node.data.category}</p>
> 83	      </div>
> 84	      {fields.length === 0 ? (
> 85	        <p className="text-xs text-muted-foreground">Este nó não tem parâmetros editáveis.</p>
> 86	      ) : (
> 87	        fields.map((f) => (
> 88	          <div key={f.key} className="space-y-1.5">
> 89	            <Label className="text-xs">{f.labelPt}</Label>
> 90	            <FieldControl node={node} field={f} />
> 91	          </div>
> 92	        ))
> 93	      )}
> 94	      <p className="text-xs text-muted-foreground border-t border-border pt-3">
> 95	        Custo estimado: {estimateCost(node)} mcoCoins <span className="opacity-70">(o servidor é a autoridade — BR-SPACES-002)</span>
> 96	      </p>
> 97	      {spaceId && (
> 98	        <div className="border-t border-border pt-3 space-y-2">
> 99	          <h3 className="text-xs font-semibold">Gerações</h3>
> 100	          <GenerationCluster spaceId={spaceId} nodeId={node.id} />
> 101	        </div>
> 102	      )}
> 103	    </div>
> 104	  );
> 105	}
> 106	
> ```

## 🤖 Claude *(22:30:18)*


## 🤖 Claude *(22:30:20)*

Padrões de render mapeados. Preciso da fonte dos ícones de Space, do `PlatformGlyph`, dos templates de campanha, e do padrão mco dos canvas nodes. Última leva de scouting:

## 🤖 Claude *(22:30:22)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCampaigns.ts",
  "offset": 1,
  "limit": 75
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
> 2	import { supabase } from '@/integrations/supabase/client';
> 3	import { useAuth } from '@/hooks/useAuth';
> 4	import { edgeErrorMessage } from '@/lib/edge';
> 5	import type { Tables, TablesInsert, TablesUpdate } from '@/integrations/supabase/types';
> 6	import type { Database } from '@/integrations/supabase/types';
> 7	
> 8	type Campaign = Tables<'campaigns'>;
> 9	type CampaignInsert = TablesInsert<'campaigns'>;
> 10	type CampaignUpdate = TablesUpdate<'campaigns'>;
> 11	type CampaignStatus = Database['public']['Enums']['campaign_status'];
> 12	type SocialPlatform = Database['public']['Enums']['social_platform'];
> 13	
> 14	export interface CampaignTemplate {
> 15	  name: string;
> 16	  description: string;
> 17	  objective: string;
> 18	  icon: string;
> 19	  defaults: Partial<CampaignInsert>;
> 20	}
> 21	
> 22	export const CAMPAIGN_TEMPLATES: CampaignTemplate[] = [
> 23	  {
> 24	    name: 'Lançamento de Produto',
> 25	    description: 'Campanha focada em gerar buzz e conversões para um novo produto ou serviço.',
> 26	    objective: 'launch',
> 27	    icon: '🚀',
> 28	    defaults: {
> 29	      objective: 'launch',
> 30	      platforms: ['instagram', 'facebook', 'linkedin'] as SocialPlatform[],
> 31	      target_audience: { age_range: '25-45', interests: ['tecnologia', 'inovação'] },
> 32	    },
> 33	  },
> 34	  {
> 35	    name: 'Promoção Sazonal',
> 36	    description: 'Campanha de ofertas e descontos para datas comemorativas ou eventos especiais.',
> 37	    objective: 'promotion',
> 38	    icon: '🎁',
> 39	    defaults: {
> 40	      objective: 'promotion',
> 41	      platforms: ['instagram', 'facebook', 'twitter'] as SocialPlatform[],
> 42	      target_audience: { age_range: '18-55', interests: ['ofertas', 'descontos'] },
> 43	    },
> 44	  },
> 45	  {
> 46	    name: 'Reconhecimento de Marca',
> 47	    description: 'Campanha para aumentar o reconhecimento da marca e alcançar novos públicos.',
> 48	    objective: 'awareness',
> 49	    icon: '📣',
> 50	    defaults: {
> 51	      objective: 'awareness',
> 52	      platforms: ['instagram', 'tiktok', 'youtube'] as SocialPlatform[],
> 53	      target_audience: { age_range: '18-35', interests: ['lifestyle', 'entretenimento'] },
> 54	    },
> 55	  },
> 56	  {
> 57	    name: 'Engajamento',
> 58	    description: 'Campanha para aumentar interações, comentários e compartilhamentos.',
> 59	    objective: 'engagement',
> 60	    icon: '💬',
> 61	    defaults: {
> 62	      objective: 'engagement',
> 63	      platforms: ['instagram', 'twitter', 'tiktok'] as SocialPlatform[],
> 64	      target_audience: { age_range: '18-40', interests: ['comunidade', 'trends'] },
> 65	    },
> 66	  },
> 67	];
> 68	
> 69	export const STATUS_TRANSITIONS: Record<CampaignStatus, CampaignStatus[]> = {
> 70	  draft: ['active', 'archived'],
> 71	  active: ['paused', 'completed', 'archived'],
> 72	  paused: ['active', 'archived'],
> 73	  completed: ['archived'],
> 74	  archived: [],
> 75	};
> ```

## 🤖 Claude *(22:30:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"===== Space node icon source (node-registry / catalog) =====\"; rg -n \"icon\" src/lib/node-registry.ts | head -40\necho \"\"; echo \"===== spaces-schema.ts around icon =====\"; sed -n '80,110p' src/lib/spaces-schema.ts 2>/dev/null || rg -n \"icon\" src/lib/spaces-schema.ts",
  "description": "Space node icon source"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== Space node icon source (node-registry / catalog) =====
> 15:  icon: string;               // sprite ref (Magnific) / lucide equivalent in MCORCH
> 25:  { id: 'upload', labelPt: 'Upload', category: 'media', icon: 'upload', inputs: [], output: 'image', draggable: false },
> 26:  { id: 'assets', labelPt: 'Ativos', category: 'media', icon: 'projects', inputs: [], output: 'image', draggable: false },
> 27:  { id: 'find-inspiration', labelPt: 'Stock', category: 'media', icon: 'search', inputs: [], output: 'image', draggable: false },
> 29:  { id: 'references', labelPt: 'Adicionar referência', category: 'references', icon: 'upload-reference', inputs: ['image'], output: 'image' },
> 31:  { id: 'image-generator', labelPt: 'Gerador de imagem', category: 'image', icon: 'image-generator', inputs: ['text', 'image'], output: 'image' },
> 32:  { id: 'image-upscaler', labelPt: 'Upscaler de imagem', category: 'image', icon: 'upscale', inputs: ['image'], output: 'image' },
> 33:  { id: 'editing', labelPt: 'Editor de imagem', category: 'image', icon: 'edit-image', inputs: ['image', 'text'], output: 'image' },
> 34:  { id: 'variations', labelPt: 'Variações', category: 'image', icon: 'variations', inputs: ['image'], output: 'image' },
> 35:  { id: 'composer', labelPt: 'Designer', category: 'designer', icon: 'design-standalone-v2', inputs: ['image', 'text'], output: 'image', badge: 'New' },
> 36:  { id: 'sketch', labelPt: 'Sketch', category: 'image', icon: 'sketch', inputs: ['image'], output: 'image' },
> 37:  { id: 'image-to-svg', labelPt: 'Imagem para SVG', category: 'image', icon: 'vector', inputs: ['image'], output: 'svg' },
> 38:  { id: 'svg-generator', labelPt: 'Gerador de SVG', category: 'image', icon: 'vector', inputs: ['text'], output: 'svg' },
> 40:  { id: 'video-generator', labelPt: 'Gerador de vídeo', category: 'video', icon: 'video', inputs: ['text', 'image'], output: 'video' },
> 41:  { id: 'speak', labelPt: 'Speak (lip-sync)', category: 'video', icon: 'lip-sync', inputs: ['video', 'audio'], output: 'video' },
> 42:  { id: 'video-combiner', labelPt: 'Combinador de vídeo', category: 'video', icon: 'rectangle-merge', inputs: ['video'], output: 'video' },
> 43:  { id: 'video-upscaler', labelPt: 'Upscaler de vídeo', category: 'video', icon: 'enhance', inputs: ['video'], output: 'video' },
> 44:  { id: 'video-frame-splitter', labelPt: 'Extrator de mídia', category: 'video', icon: 'split', inputs: ['video'], output: 'image', badge: 'New' },
> 46:  { id: 'voice-over', labelPt: 'Voiceover', category: 'audio', icon: 'ai-voice', inputs: ['text'], output: 'audio' },
> 47:  { id: 'sfx-generator', labelPt: 'Efeitos sonoros', category: 'audio', icon: 'sound-effects', inputs: ['text'], output: 'audio' },
> 48:  { id: 'music-generator', labelPt: 'Gerador de música', category: 'audio', icon: 'music', inputs: ['text'], output: 'audio' },
> 50:  { id: 'text', labelPt: 'Texto', category: 'text', icon: 'text', inputs: [], output: 'text' },
> 51:  { id: 'prompt-generator', labelPt: 'Assistant', category: 'text', icon: 'ai-stars', inputs: ['text', 'image'], output: 'text' },
> 53:  { id: 'list', labelPt: 'Lista', category: 'utility', icon: 'bullet-list', inputs: ['text'], output: 'text' },
> 54:  { id: 'sticky-note', labelPt: 'Nota', category: 'utility', icon: 'sticky-note', inputs: [] },
> 55:  { id: 'stickers', labelPt: 'Adesivos', category: 'utility', icon: 'smile', inputs: [] },
> 56:  { id: 'group', labelPt: 'Grupo', category: 'utility', icon: 'group-element', inputs: [] },
> 
> ===== spaces-schema.ts around icon =====
> 
> /* ── Node data — extends OrchestrationNodeData (coinCost/status/config kept) ── */
> export const SpaceNodeDataSchema = z.object({
>   label: z.string(),                                   // pt-BR
>   /** canonical registry type id (node-registry.ts) — executor classification (Fase 1b).
>    *  Optional: Fase 1a nodes lack it; nodeTypeId() falls back to the label prefix. */
>   typeId: z.string().optional(),
>   category: z.enum(NODE_CATEGORIES),
>   modelKey: z.string().optional(),                     // e.g. 'flux.2-pro' → CREDIT_COSTS
>   aspectRatio: z.enum(ASPECT_RATIOS).default('1:1'),
>   batch: z.number().int().min(1).max(8).default(1),    // 'x1..x8' stepper
>   references: z.array(ReferenceSchema).max(MAX_REFERENCES).default([]),
>   coinCost: z.number().min(0).default(0),              // mcoCoins (server is source of truth)
>   stabilityScore: z.number().min(0).max(1).default(1), // carried from orchestration model
>   status: z.enum(NODE_STATUSES).default('idle'),
>   ports: z.array(PortSchema),
>   params: z.record(z.string(), z.unknown()).default({}),
>   byok: z.boolean().optional(),                        // BR-SPACES-006
>   locked: z.boolean().optional(),                      // node "Lock" action (UI-SPACES-008)
>   headerHidden: z.boolean().optional(),                // "Hide header" action
>   icon: z.string().default('✨'),
> });
> export type SpaceNodeData = z.infer<typeof SpaceNodeDataSchema>;
> 
> /* ── @xyflow/react bindings ────────────────────────────────────────────────── */
> export type SpaceNode = Node<SpaceNodeData>;
> export interface SpaceEdgeData extends Record<string, unknown> {
>   dataType: PortDataType; // typed connection (FR-SPACES-004)
> }
> export type SpaceEdge = Edge<SpaceEdgeData>;
> ```

## 🤖 Claude *(22:30:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"===== PlatformGlyph in SocialAccountsPage =====\"; rg -n \"PlatformGlyph|\\.icon|GLYPH|lucide\" src/pages/SocialAccountsPage.tsx | head -40",
  "description": "PlatformGlyph render pattern"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== PlatformGlyph in SocialAccountsPage =====
> 8:import { Loader2, Link2, Unlink, AlertTriangle, ExternalLink, CheckCircle2, Globe, Briefcase, Send } from 'lucide-react';
> 17:// Brand glyphs for platforms that have a real logo (lucide-react dropped brand icons). Platforms
> 29:function PlatformGlyph({ platform, emoji }: { platform: SocialPlatform; emoji?: string }) {
> 157:                    <PlatformGlyph platform={account.platform} emoji={platformInfo?.icon} />
> 222:                    <PlatformGlyph platform={platform.id} emoji={platform.icon} />
> ```

## 🤖 Claude *(22:31:01)*


## 🤖 Claude *(22:31:04)*

Vejo que os ícones de Space no `node-registry.ts` já são **nomes de sprite** (`image-generator`, `video`, `music`, `smile`…), não emoji — mas `SpaceNodeCard`/`ParamHUD` renderizam `{data.icon}` como texto cru (e o default do schema é `✨`). Preciso ver como `data.icon` é populado + o `PlatformGlyph` + o padrão mco dos canvas nodes.

## 🤖 Claude *(22:31:07)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"===== PlatformGlyph body =====\"; sed -n '17,56p' src/pages/SocialAccountsPage.tsx\necho \"\"; echo \"===== how data.icon is set in store/addNode =====\"; rg -n \"icon\" src/store/useSpacesStore.ts | head\necho \"\"; echo \"===== addNode icon population (node-registry usage) =====\"; rg -n \"\\.icon|icon:\" src/store/useSpacesStore.ts src/pages/SpaceCanvasPage.tsx | head",
  "description": "PlatformGlyph + space icon population"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== PlatformGlyph body =====
> // Brand glyphs for platforms that have a real logo (lucide-react dropped brand icons). Platforms
> // without a glyph (linkedin, twitter, wordpress) fall back to the emoji from SUPPORTED_PLATFORMS.
> const PLATFORM_BRAND_ICON: Partial<Record<SocialPlatform, React.ComponentType<{ className?: string }>>> = {
>   instagram: Instagram,
>   facebook: Facebook,
>   tiktok: TikTok,
>   youtube: YouTube,
>   pinterest: Pinterest,
>   linkedin: Briefcase,
>   twitter: Send,
> };
> 
> function PlatformGlyph({ platform, emoji }: { platform: SocialPlatform; emoji?: string }) {
>   const Icon = PLATFORM_BRAND_ICON[platform];
>   if (Icon) return <Icon className="h-6 w-6 text-foreground" />;
>   return <span className="text-2xl">{emoji}</span>;
> }
> 
> export default function SocialAccountsPage() {
>   const { accounts, isLoading, disconnectAccount, initiateOAuth, needsReauth } = useSocialAccounts();
>   const { toast } = useToast();
>   const { user } = useAuth();
>   const [connectingPlatform, setConnectingPlatform] = useState<SocialPlatform | null>(null);
> 
>   // WordPress self-hosted config
>   const [wpConfig, setWpConfig] = useState({ wp_site_url: '', wp_username: '', wp_app_password: '' });
>   const [wpConnected, setWpConnected] = useState(false);
>   const [savingWp, setSavingWp] = useState(false);
>   const [loadingWp, setLoadingWp] = useState(true);
> 
>   useEffect(() => {
>     if (!user) return;
>     supabase
>       .from('user_api_keys')
>       .select('wp_site_url, wp_username')
>       .eq('user_id', user.id)
>       .maybeSingle()
>       .then(({ data }) => {
>         if (data?.wp_site_url) {
>           setWpConfig((c) => ({ ...c, wp_site_url: data.wp_site_url ?? '', wp_username: data.wp_username ?? '' }));
> 
> ===== how data.icon is set in store/addNode =====
> 95:          // ParamHUD map it to a line-icon (legacy-emoji graphs still render via raw fallback).
> 96:          icon: 'image',
> 
> ===== addNode icon population (node-registry usage) =====
> src/store/useSpacesStore.ts:96:          icon: 'image',
> ```

## 🤖 Claude *(22:31:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"===== StatusBar mco pattern (last seal \ud83d\udc8e\u2192Coins) =====\"; rg -n \"Coins|mco|\ud83d\udc8e\" src/components/canvas/StatusBar.tsx | head\necho \"\"; echo \"===== GenerateImageNode mco context =====\"; sed -n '55,70p' src/components/canvas/nodes/GenerateImageNode.tsx\necho \"\"; echo \"===== other tpl.icon / campaign icon render sites =====\"; rg -rn \"tpl\\.icon|template\\.icon|\\.icon}\" src/pages/CampaignDetail.tsx src/components/marketing 2>/dev/null | head",
  "description": "Canvas mco pattern + campaign icon render sites"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== StatusBar mco pattern (last seal 💎→Coins) =====
> 1:import { AlertTriangle, CheckCircle2, Coins } from "lucide-react";
> 6: * Bottom status bar of the Canvas editor: mcoCoins balance, project execution
> 28:          <Coins className="h-3 w-3 text-amber-400" />
> 
> ===== GenerateImageNode mco context =====
>         <p className="line-clamp-2 text-[10px] leading-snug text-muted-foreground">
>           {d.prompt || (
>             <span className="italic opacity-60">Defina um prompt no painel direito…</span>
>           )}
>         </p>
>         <div className="flex items-center justify-between gap-2 font-mono text-[9px] text-muted-foreground">
>           <span className="truncate">{info.label}</span>
>           <span className="shrink-0">
>             {d.aspectRatio} · {info.coinCost} 💎
>             {info.higgsfieldCost != null && (
>               <span className="ml-1 text-secondary">+{info.higgsfieldCost} hf</span>
>             )}
>           </span>
>         </div>
>         {d.error && (
>           <p className="border-t border-destructive/30 pt-1 text-[10px] text-destructive">
> 
> ===== other tpl.icon / campaign icon render sites =====
> ```

## 🤖 Claude *(22:32:32)*


## 🤖 Claude *(22:32:37)*

Agora tenho o quadro completo. Descobertas decisivas:

1. **Spaces é um bug real**: `useSpacesStore.ts:96` já grava `icon: 'image'` (nome lucide) com comentário *"ParamHUD map it to a line-icon"* — mas `SpaceNodeCard:55`/`ParamHUD:80` renderizam `{data.icon}` como **texto cru** (mostram "image"/"✨" literais). Falta o componente que mapeia.
2. **Social é fallback morto**: `PlatformGlyph` já cobre os 7 platforms com ícones — o emoji em `useSocialAccounts.ts` nunca renderiza. Limpo mesmo assim + endureço o fallback.
3. **Canvas mco**: padrão canônico é `<Coins className="text-amber-400"/>` (StatusBar) — gold = valor.

Verificações finais antes de editar (render paths sensíveis — o anticorpo cross-file):

## 🤖 Claude *(22:32:41)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"===== useCrewOverlay avatar render sites (who renders overlay .avatar?) =====\"; rg -rn \"avatar\" src/hooks/useCrewOverlay.ts src/components/graph/*.tsx | grep -i avatar | head -20\necho \"\"; echo \"===== consumers of SUPPORTED_PLATFORMS (other than the page) =====\"; rg -rn \"SUPPORTED_PLATFORMS\" src | head\necho \"\"; echo \"===== orchestrator AgentNode \u26a1 context + Zap import? =====\"; sed -n '1,6p;45,52p' src/components/orchestrator/nodes/AgentNode.tsx\necho \"\"; echo \"===== any OTHER render of space data.icon? =====\"; rg -rn \"data\\.icon|\\.data\\.icon|node\\.data\\.icon\" src/components/spaces src/pages/SpaceCanvasPage.tsx | head",
  "description": "Verify sensitive render paths before edit"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== useCrewOverlay avatar render sites (who renders overlay .avatar?) =====
> src/components/graph/AgentAvatar.tsx:// MIV: an agent's `n` is a serializable lucide string-name (persisted in store/DB), rendered
> src/components/graph/AgentAvatar.tsx:export function AgentAvatar({ n, className }: { n?: string; className?: string }) {
> src/components/graph/AgentAvatar.tsx:  const Icon = n ? AVATAR_ICON_MAP[n] : undefined;
> src/components/graph/AgentAvatar.tsx:  return <span className={className}>{n}</span>;
> src/components/graph/AgentNode.tsx:function AgentAvatar({ n }: { n: string }) {
> src/components/graph/AgentNode.tsx:  const Icon = n ? AVATAR_ICONS[n] : undefined;
> src/components/graph/AgentNode.tsx:            <AgentAvatar n={n} />
> 
> ===== consumers of SUPPORTED_PLATFORMS (other than the page) =====
> src/hooks/useSocialAccounts.ts:export const n: { id: SocialPlatform; name: string; icon: string; color: string }[] = [
> src/pages/SocialAccountsPage.tsx:import { useSocialAccounts, n } from '@/hooks/useSocialAccounts';
> src/pages/SocialAccountsPage.tsx:// without a glyph (linkedin, twitter, wordpress) fall back to the emoji from n.
> src/pages/SocialAccountsPage.tsx:              const platformInfo = n.find((p) => p.id === account.platform);
> src/pages/SocialAccountsPage.tsx:            {n.map((platform) => {
> 
> ===== orchestrator AgentNode ⚡ context + Zap import? =====
> import { Handle, Position, type NodeProps } from '@xyflow/react';
> import { NodeIcon } from '../NodeIcon';
> import { Loader2, CheckCircle2, XCircle, Clock } from 'lucide-react';
> import type { OrchestrationNodeData } from '@/store/useOrchestrationStore';
> 
> const STATUS: Record<string, { ring: string; badge: string; label: string }> = {
>           {cfg.label}
>         </span>
>         <div className="flex items-center gap-2">
>           <span className="text-[9px] text-blue-400/50">{data.coinCost}c</span>
>           <span className="text-[9px] text-white/20">⚡{(data.stabilityScore * 100).toFixed(0)}%</span>
>         </div>
>       </div>
> 
> 
> ===== any OTHER render of space data.icon? =====
> src/components/spaces/SpaceNodeCard.tsx:        <span className="text-base leading-none">{n}</span>
> src/components/spaces/ParamHUD.tsx:          <span>{n}</span>{node.data.label}
> ```

## 🤖 Claude *(22:33:09)*


## 🤖 Claude *(22:33:14)*

O output veio corrompido (a shim de `grep` mutilou os literais — memória `[[reference_grep_is_ugrep_shim_in_tool]]`). Extraio só os fatos estruturais confiáveis e re-verifico o path do avatar do overlay com leitura direta, evitando a shim.

Fatos confirmados: (1) `SUPPORTED_PLATFORMS` só é consumido em SocialAccountsPage ✅; (2) orchestrator AgentNode **não** importa `Zap` — preciso adicionar; (3) `data.icon` de Space renderiza em exatamente 2 sites (SpaceNodeCard:55, ParamHUD:80) ✅.

## 🤖 Claude *(22:33:14)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCrewOverlay.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useQuery } from '@tanstack/react-query';
> 2	import { supabase } from '@/integrations/supabase/client';
> 3	import { useAuth } from '@/hooks/useAuth';
> 4	import { useMemo } from 'react';
> 5	
> 6	// Maps squad identity to file name patterns for INHABITS edges
> 7	const SQUAD_PATTERNS: Record<string, string[]> = {
> 8	  content:  ['Campaign', 'Content', 'Blog', 'Video', 'Calendar', 'Publish', 'Social', 'Landing', 'Editor', 'Wizard'],
> 9	  tech:     ['hook', 'store', 'use', 'lib', 'integration', 'supabase', 'client', 'query', 'config', 'Hook'],
> 10	  market:   ['Analytics', 'Affiliate', 'ROI', 'Revenue', 'Dashboard', 'Home', 'Metric'],
> 11	  ops:      ['watchdog', 'deploy', 'rescue', 'backfill', 'seed', 'harness', 'script', 'function', 'Admin'],
> 12	  default:  ['App', 'main', 'index', 'Auth', 'Settings', 'Onboarding', 'NotFound'],
> 13	};
> 14	
> 15	export const SQUAD_COLOR: Record<string, string> = {
> 16	  content: '#00F2FF',
> 17	  tech:    '#2DD4BF',
> 18	  market:  '#D4AF37',
> 19	  ops:     '#8C5AFF',
> 20	  default: '#67E8F9',
> 21	};
> 22	
> 23	export interface CrewOverlayAgent {
> 24	  id: string;
> 25	  name: string;
> 26	  role: string;
> 27	  avatar: string;
> 28	  status: string;
> 29	  squad: string;
> 30	  color: string;
> 31	  filePatterns: string[];
> 32	}
> 33	
> 34	export function inferSquad(name: string, role: string): string {
> 35	  const s = (name + ' ' + role).toLowerCase();
> 36	  if (s.includes('content') || s.includes('creative') || s.includes('blog') || s.includes('video')) return 'content';
> 37	  if (s.includes('tech') || s.includes('engine') || s.includes('architect') || s.includes('engineer')) return 'tech';
> 38	  if (s.includes('market') || s.includes('analyt') || s.includes('intelligence') || s.includes('growth')) return 'market';
> 39	  if (s.includes('ops') || s.includes('operational') || s.includes('infra') || s.includes('devops')) return 'ops';
> 40	  return 'default';
> 41	}
> 42	
> 43	export function useCrewOverlay() {
> 44	  const { user } = useAuth();
> 45	
> 46	  const { data: rawAgents = [], isLoading } = useQuery({
> 47	    queryKey: ['crew_overlay_agents', user?.id],
> 48	    queryFn: async () => {
> 49	      if (!user?.id) return [];
> 50	      const { data, error } = await supabase
> 51	        .from('crew_agents')
> 52	        .select('id, agent_key, name, role, avatar, status')
> 53	        .eq('user_id', user.id)
> 54	        .order('created_at');
> 55	      if (error) throw error;
> 56	      return data ?? [];
> 57	    },
> 58	    staleTime: 2 * 60 * 1000,
> 59	    enabled: !!user?.id,
> 60	  });
> 61	
> 62	  const overlayAgents = useMemo<CrewOverlayAgent[]>(() =>
> 63	    rawAgents.map((a: any) => {
> 64	      const squad = inferSquad(a.name ?? '', a.role ?? '');
> 65	      return {
> 66	        id: a.agent_key ?? a.id,
> 67	        name: a.name ?? 'Agent',
> 68	        role: a.role ?? 'specialist',
> 69	        avatar: a.avatar ?? '🤖',
> 70	        status: a.status ?? 'idle',
> 71	        squad,
> 72	        color: SQUAD_COLOR[squad],
> 73	        filePatterns: SQUAD_PATTERNS[squad] ?? SQUAD_PATTERNS.default,
> 74	      };
> 75	    }),
> 76	  [rawAgents]);
> 77	
> 78	  return { overlayAgents, agentCount: overlayAgents.length, isLoading };
> 79	}
> 80	
> ```

## 🤖 Claude *(22:33:21)*


## 🤖 Claude *(22:33:22)*

Preciso achar quem renderiza `overlayAgents[].avatar`. Uso python para evitar a mutilação da shim.

## 🤖 Claude *(22:33:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\npython3 - <<'PY'\nimport subprocess\n# find consumers of useCrewOverlay and how .avatar renders\nfor term in ['useCrewOverlay', 'overlayAgent', '.avatar']:\n    print(f\"\\n##### {term} #####\")\n    r = subprocess.run(['grep','-rn','--include=*.tsx','--include=*.ts', term, 'src'],\n                       capture_output=True, text=True)\n    # filter out the hook definition file for .avatar noise\n    for line in r.stdout.splitlines():\n        print(line)\nPY",
  "description": "Find useCrewOverlay consumers + avatar render"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ##### useCrewOverlay #####
> src/pages/MemoryPage.tsx:30:import { inferSquad } from '@/hooks/useCrewOverlay';
> src/pages/UnifiedCanvasPage.tsx:17:import { useCrewOverlay } from '@/hooks/useCrewOverlay';
> src/pages/UnifiedCanvasPage.tsx:159:  const { overlayAgents, agentCount } = useCrewOverlay();
> src/components/orchestrator/ConstellationMatrix.tsx:6:import { useCrewOverlay, SQUAD_COLOR } from '@/hooks/useCrewOverlay';
> src/components/orchestrator/ConstellationMatrix.tsx:115:  const { overlayAgents, agentCount } = useCrewOverlay();
> src/hooks/useCrewOverlay.ts:43:export function useCrewOverlay() {
> src/hooks/useConstellationSigma.ts:6:import type { CrewOverlayAgent } from './useCrewOverlay';
> src/hooks/useConstellationSigma.ts:7:import { SQUAD_COLOR } from './useCrewOverlay';
> 
> ##### overlayAgent #####
> src/pages/UnifiedCanvasPage.tsx:159:  const { overlayAgents, agentCount } = useCrewOverlay();
> src/pages/UnifiedCanvasPage.tsx:160:  const sigmaOptions = useMemo(() => ({ overlayAgents }), [overlayAgents]);
> src/components/orchestrator/ConstellationMatrix.tsx:115:  const { overlayAgents, agentCount } = useCrewOverlay();
> src/components/orchestrator/ConstellationMatrix.tsx:116:  const activeAgents = showOverlay ? overlayAgents : EMPTY_ARRAY;
> src/components/orchestrator/ConstellationMatrix.tsx:120:  const sigmaOptions = useMemo(() => ({ overlayAgents: activeAgents, enableOwnership: true }), [activeAgents]);
> src/hooks/useCrewOverlay.ts:62:  const overlayAgents = useMemo<CrewOverlayAgent[]>(() =>
> src/hooks/useCrewOverlay.ts:78:  return { overlayAgents, agentCount: overlayAgents.length, isLoading };
> src/hooks/useConstellationSigma.ts:74:  overlayAgents?: CrewOverlayAgent[];
> src/hooks/useConstellationSigma.ts:114:  const { overlayAgents = EMPTY_ARRAY, enableOwnership = false } = options;
> src/hooks/useConstellationSigma.ts:283:    for (const agent of overlayAgents) {
> src/hooks/useConstellationSigma.ts:358:    const orphanedAgents = overlayAgents.filter(a => {
> src/hooks/useConstellationSigma.ts:364:  }, [astNodes, astEdges, knowledgeNodes, overlayAgents, ownershipData, astLoading, edgesLoading, knowledgeLoading]);
> 
> ##### .avatar #####
> src/integrations/supabase/types.ts:910:      avatar_consents: {
> src/integrations/supabase/types.ts:949:      avatar_identities: {
> src/integrations/supabase/types.ts:1588:          avatar: string
> src/integrations/supabase/types.ts:1607:          avatar?: string
> src/integrations/supabase/types.ts:1626:          avatar?: string
> src/integrations/supabase/types.ts:2867:          avatar_url: string | null
> src/integrations/supabase/types.ts:2883:          avatar_url?: string | null
> src/integrations/supabase/types.ts:2899:          avatar_url?: string | null
> src/integrations/supabase/types.ts:5165:      erase_avatar_artifacts: {
> src/integrations/supabase/types.ts:5166:        Args: { p_avatar_identity_id?: string; p_voice_profile_id?: string }
> src/pages/KanbanPage.tsx:7:import { Avatar, AvatarFallback } from "@/components/ui/avatar";
> src/pages/ChatPage.tsx:8:import { Avatar, AvatarFallback } from "@/components/ui/avatar";
> src/pages/SettingsPage.tsx:327:              {/* Avatar / Clone AI (BYOK Modelo A — módulo avatar-clone-ai) */}
> src/pages/SettingsPage.tsx:333:                  id="hedra_api_key" label="Hedra API Key (motor avatar — default)" placeholder="sk_hedra_..."
> src/pages/SettingsPage.tsx:334:                  description="BYOK do motor talking-head Hedra Character-3 (default custo-efetivo do módulo Avatar/Clone AI). Sua chave, cifrada no Vault; sem ela, a geração de avatar retorna 402."
> src/pages/SettingsPage.tsx:340:                  id="fal_api_key" label="fal.ai API Key (motor avatar — OmniHuman)" placeholder="key_id:key_secret"
> src/pages/SettingsPage.tsx:348:                  description="BYOK do clone de voz Cartesia Sonic (PT-BR real-time, trilha premium do avatar). Per-user, cifrada no Vault. A chave ElevenLabs acima também serve ao avatar."
> src/pages/CanvasEditorPage.tsx:62:  avatarIdentity: AvatarIdentityNode,
> src/lib/node-registry.ts:81: * Modeled as facade nodes that encapsulate a subgraph. Two are avatar/clone paths.
> src/lib/avatar-identity.ts:1:// avatar-clone-ai · Fatia 3b — VLM-soft Identity Gate compare (FR-AC-013b).
> src/lib/avatar-identity.ts:2:// BoK SSOT: docs/bok/avatar-clone-ai/10-amendment-3b-identity-gate-vlm-soft.md
> src/lib/avatar-identity.ts:11:// MIRROR NOTE: when the Identity Gate is wired into an Edge Function (avatar gate,
> src/lib/canvas-node-registry.ts:88:    id: "avatarIdentity",
> src/lib/canvas-node-registry.ts:89:    label: "Identidade (avatar)",
> src/lib/canvas-node-registry.ts:90:    description: "Treina e verifica a identidade facial do avatar (Soul ID / LoRA) — Identity Gate VLM-soft.",
> src/lib/canvas-node-registry.ts:94:    aliases: ["identidade", "avatar", "rosto", "face", "soul", "identity", "gabriel", "pessoa"],
> src/lib/avatar.ts:1:// avatar-clone-ai · shared client helpers (programa "Gabriel AI").
> src/lib/avatar.ts:2:// BoK SSOT: docs/bok/avatar-clone-ai/04-frd.md (FR-AC-010, FM-AC-013).
> src/lib/enterprise-seed.ts:14:    avatar: 'crown',
> src/lib/enterprise-seed.ts:26:  // status tokens). `icon` = serializable lucide string-name (persisted as agent avatar).
> src/lib/enterprise-seed.ts:46:      avatar: squad.icon,
> src/lib/enterprise-seed.ts:80:        avatar: 'bot',
> src/lib/billing.ts:28:  // avatar-clone-ai Fatia 2 (FR-AC-009 · docs/processes/avatar-voice-credential-resolution.md).
> src/test/avatar-identity.test.ts:9:} from "@/lib/avatar-identity";
> src/test/avatar-identity.test.ts:30:describe("avatar-identity · VLM-soft compare (FR-AC-013b)", () => {
> src/test/avatar-identity.test.ts:68:describe("avatar-identity · parseIdentityAttributes (fail-soft)", () => {
> src/test/avatar-identity.test.ts:96:describe("avatar-identity · reconcileSoftMatches (N≥2 determinism + anti-oscillation)", () => {
> src/test/avatar-identity.test.ts:121:describe("avatar-identity · buildIdentityDescribeQuestion", () => {
> src/test/avatar-voice.test.ts:2:import { detectCodeSwitch } from "@/lib/avatar";
> src/test/avatar-voice.test.ts:4:// avatar-clone-ai Fatia 2 — code-switching guard (FR-AC-010 / FM-AC-013).
> src/components/avatar/ConsentWizard.tsx:9:// avatar-clone-ai Fatia 3a — biometric consent wizard (FR-AC-030, LGPD Art. 11).
> src/components/avatar/ConsentWizard.tsx:11:export const CONSENT_TERM_VERSION = "avatar-biometric-consent-v1";
> src/components/landing/TestimonialsSection.tsx:8:    avatar: 'MC',
> src/components/landing/TestimonialsSection.tsx:15:    avatar: 'RO',
> src/components/landing/TestimonialsSection.tsx:22:    avatar: 'CS',
> src/components/landing/TestimonialsSection.tsx:63:                  {t.avatar}
> src/components/kanban/CardDetailDialog.tsx:13:import { Avatar, AvatarFallback } from "@/components/ui/avatar";
> src/components/graph/AgentAvatar.tsx:7:// MIV: an agent's `avatar` is a serializable lucide string-name (persisted in store/DB), rendered
> src/components/graph/AgentAvatar.tsx:29:export function AgentAvatar({ avatar, className }: { avatar?: string; className?: string }) {
> src/components/graph/AgentAvatar.tsx:30:  const Icon = avatar ? AVATAR_ICON_MAP[avatar] : undefined;
> src/components/graph/AgentAvatar.tsx:32:  return <span className={className}>{avatar}</span>;
> src/components/graph/AgentNode.tsx:17:// MIV: agent avatar = serializable lucide string-name (persisted), rendered as a line-icon.
> src/components/graph/AgentNode.tsx:22:function AgentAvatar({ avatar }: { avatar: string }) {
> src/components/graph/AgentNode.tsx:23:  const Icon = avatar ? AVATAR_ICONS[avatar] : undefined;
> src/components/graph/AgentNode.tsx:28:  return <span className="text-3xl filter drop-shadow-[0_0_10px_rgba(255,255,255,0.5)]">{avatar}</span>;
> src/components/graph/AgentNode.tsx:73:  const { id, name, avatar, status, position } = agent;
> src/components/graph/AgentNode.tsx:133:            <AgentAvatar avatar={avatar} />
> src/components/ui/avatar.tsx:2:import * as AvatarPrimitive from "@radix-ui/react-avatar";
> src/components/canvas/nodes/VoiceCloneNode.tsx:10:// avatar-clone-ai Fatia 2 — voiceClone canvas node (display-only; logic lives in VoiceCloneInspector + useAvatarVoice).
> src/components/canvas/nodes/AvatarIdentityNode.tsx:9:// avatar-clone-ai Fatia 3b — avatarIdentity canvas node (display-only; logic in AvatarIdentityInspector).
> src/components/canvas/nodes/AvatarIdentityNode.tsx:12:  const trained = Boolean(d.avatarIdentityId);
> src/components/canvas/RightPanel/inspectors/VoiceCloneInspector.tsx:13:import { ConsentWizard } from "@/components/avatar/ConsentWizard";
> src/components/canvas/RightPanel/inspectors/VoiceCloneInspector.tsx:14:import { detectCodeSwitch, type VoiceLanguage, type VoiceProvider } from "@/lib/avatar";
> src/components/canvas/RightPanel/inspectors/AvatarIdentityInspector.tsx:10:import { ConsentWizard } from "@/components/avatar/ConsentWizard";
> src/components/canvas/RightPanel/inspectors/AvatarIdentityInspector.tsx:41:  const trained = Boolean(d.avatarIdentityId);
> src/components/canvas/RightPanel/inspectors/AvatarIdentityInspector.tsx:45:      updateNodeData(node.id, { provider, avatarIdentityId: undefined, status: "idle", error: undefined });
> src/components/canvas/RightPanel/inspectors/AvatarIdentityInspector.tsx:50:      updateNodeData(node.id, { tier, avatarIdentityId: undefined, status: "idle", error: undefined });
> src/components/canvas/RightPanel/inspectors/AvatarIdentityInspector.tsx:73:        const path = `${userId}/avatars/${projectId}/${node.id}-${Date.now()}-${newUrls.length}.${ext}`;
> src/components/canvas/RightPanel/inspectors/AvatarIdentityInspector.tsx:89:        avatarIdentityId: undefined,
> src/components/canvas/RightPanel/inspectors/AvatarIdentityInspector.tsx:105:      avatarIdentityId: undefined,
> src/components/canvas/RightPanel/inspectors/AvatarIdentityInspector.tsx:110:    // OTD-AC-017: the avatar-identity-train Edge Function is GATED on a verified Higgsfield self-serve
> src/components/canvas/RightPanel/index.tsx:65:      ) : node.data.kind === "avatarIdentity" ? (
> src/components/panels/ConfigPanel.tsx:83:                  <AgentAvatar avatar={a.avatar} className="h-5 w-5 text-white" />
> src/components/panels/AddAgentDialog.tsx:15:// MIV: avatar identity via line-icon (not emoji). The persisted `avatar` field is a serializable
> src/components/panels/AddAgentDialog.tsx:50:  const [avatar, setAvatar] = useState('bot');
> src/components/panels/AddAgentDialog.tsx:62:      avatar,
> src/components/panels/AddAgentDialog.tsx:95:                    className={`p-2 rounded ${avatar === a ? 'bg-primary/20 ring-2 ring-primary text-primary' : 'text-muted-foreground hover:bg-muted hover:text-foreground'}`}
> src/components/panels/AgentDetail.tsx:59:    setEditAvatar(agent.avatar);
> src/components/panels/AgentDetail.tsx:73:      avatar: editAvatar,
> src/components/panels/AgentDetail.tsx:123:              <AgentAvatar avatar={agent.avatar} className="h-6 w-6 text-white" />
> src/components/panels/NewEdgeDialog.tsx:72:              <AgentAvatar avatar={fromAgent.avatar} className="h-6 w-6 text-white" />
> src/components/panels/NewEdgeDialog.tsx:77:              <AgentAvatar avatar={toAgent.avatar} className="h-6 w-6 text-white" />
> src/hooks/useCrewOverlay.ts:27:  avatar: string;
> src/hooks/useCrewOverlay.ts:52:        .select('id, agent_key, name, role, avatar, status')
> src/hooks/useCrewOverlay.ts:69:        avatar: a.avatar ?? '🤖',
> src/hooks/useCrewData.ts:52:            avatar: a.avatar ?? '',
> src/hooks/useAvatarVoice.ts:3:import type { VoiceLanguage, VoiceProvider } from "@/lib/avatar";
> src/hooks/useAvatarVoice.ts:5:// avatar-clone-ai Fatia 2 — Harness hook for the `generate-voice` Edge Function (FR-AC-009).
> src/hooks/useAvatarConsent.ts:5:// avatar-clone-ai Fatia 3a — biometric consent (LGPD Art. 11). Harness hook; UI is display-only.
> src/hooks/useAvatarConsent.ts:22:    queryKey: ["avatar-consents", user?.id],
> src/hooks/useAvatarConsent.ts:26:        .from("avatar_consents")
> src/hooks/useAvatarConsent.ts:46:/** Grant biometric consent per finalidade via the avatar-consent edge fn (server-captures IP). */
> src/hooks/useAvatarConsent.ts:52:      const { data, error } = await supabase.functions.invoke("avatar-consent", { body: params });
> src/hooks/useAvatarConsent.ts:64:    onSuccess: () => qc.invalidateQueries({ queryKey: ["avatar-consents", user?.id] }),
> src/hooks/useAvatarConsent.ts:75:        .from("avatar_consents")
> src/hooks/useAvatarConsent.ts:81:    onSuccess: () => qc.invalidateQueries({ queryKey: ["avatar-consents", user?.id] }),
> src/hooks/useAgentMutations.ts:10:  avatar: string;
> src/hooks/useAgentMutations.ts:22:  avatar?: string;
> src/hooks/useConstellationSigma.ts:314:          label: agent.avatar + ' ' + (agent.name.length > 16 ? agent.name.slice(0, 16) + '…' : agent.name),
> src/hooks/useConstellationSigma.ts:326:          agentAvatar: agent.avatar,
> src/hooks/useAvatarErasure.ts:4:// avatar-clone-ai Fatia 3a — LGPD Art. 18 erasure. Harness hook; UI is display-only.
> src/hooks/useAvatarErasure.ts:7:  avatar_identity_id?: string;
> src/hooks/useAvatarErasure.ts:19:/** Erase a biometric artifact (own) via the erase-avatar-artifacts edge fn (tenant-guarded server-side). */
> src/hooks/useAvatarErasure.ts:23:      const { data, error } = await supabase.functions.invoke("erase-avatar-artifacts", { body: params });
> src/hooks/useCreateCrew.ts:27:// MIV: `icon` is a serializable lucide string-name (persisted as the agent `avatar`); the
> src/hooks/useCreateCrew.ts:50:  avatar: string;
> src/hooks/useCreateCrew.ts:74:    { agentKey: CORE_KEY, name: 'Núcleo GCRUX', role: 'orchestrator', avatar: 'crown', level: 0, squad: null, capabilityKey: null, position: [0, 0, 0] },
> src/hooks/useCreateCrew.ts:85:    agents.push({ agentKey: leadKey, name: `Lead ${DEPT_META[dept].name}`, role: 'lead', avatar: DEPT_META[dept].icon, level: 1, squad: dept, capabilityKey: null, position: [lx, 2, lz] });
> src/hooks/useCreateCrew.ts:95:      agents.push({ agentKey: subKey, name: cap.displayName, role: 'specialist', avatar: 'bot', level: 2, squad: dept, capabilityKey: cap.capabilityKey, position: [mx, my, mz] });
> src/hooks/useCreateCrew.ts:134:      avatar: a.avatar,
> src/hooks/useCreateCrew.ts:201:        ?? { agentKey: leadKey, name: `Lead ${DEPT_META[department].name}`, role: 'lead' as const, avatar: DEPT_META[department].icon, level: 1 as const, squad: department, capabilityKey: null, position: [Math.cos((DEPT_ORDER.indexOf(department) / DEPT_ORDER.length) * Math.PI * 2) * 8, 2, Math.sin((DEPT_ORDER.indexOf(department) / DEPT_ORDER.length) * Math.PI * 2) * 8] as [number, number, number] };
> src/hooks/useCreateCrew.ts:203:        ?? { agentKey: subKey, name: cap.displayName, role: 'specialist' as const, avatar: 'bot', level: 2 as const, squad: department, capabilityKey, position: lead.position };
> src/store/useCrewStore.ts:10:  avatar: string;
> src/store/useCrewStore.ts:132:      avatar: 'crown',
> src/store/useCrewStore.ts:143:    // status tokens). `icon` = serializable lucide string-name (persisted as agent avatar).
> src/store/useCrewStore.ts:163:        avatar: squad.icon,
> src/store/useCrewStore.ts:197:          avatar: 'bot',
> src/types/canvas.ts:26:  | "avatarIdentity";
> src/types/canvas.ts:461: * avatar-clone-ai Fatia 2 — voiceClone node (FR-AC-008/009/010/011).
> src/types/canvas.ts:489: * avatar-clone-ai Fatia 3b — avatarIdentity node (FR-AC-012).
> src/types/canvas.ts:491: * net-new `avatar-identity-train` Edge Function (gated OTD-AC-017) — NOT canvas-execute. The
> src/types/canvas.ts:492: * Identity Gate runs the VLM-soft compare (FR-AC-013b, src/lib/avatar-identity.ts) post-generation.
> src/types/canvas.ts:495:  kind: "avatarIdentity";
> src/types/canvas.ts:507:  /** avatar_identities row id — set after a successful train (gated OTD-AC-017). */
> src/types/canvas.ts:508:  avatarIdentityId?: string;
> src/types/canvas.ts:707:/** avatar-clone-ai Fatia 2 — voiceClone node default (global EN-first per the BoK decisions). */
> src/types/canvas.ts:728:/** avatar-clone-ai Fatia 3b — avatarIdentity node default (FR-AC-012). */
> src/types/canvas.ts:735:    type: "avatarIdentity",
> src/types/canvas.ts:738:      kind: "avatarIdentity",
> src/types/canvas.ts:739:      label: "Identidade (avatar)",
> src/types/canvas.ts:889:    case "avatarIdentity":
> src/types/canvas.ts:890:      // avatarIdentity trains against the net-new `avatar-identity-train` Edge Function
> src/types/canvas.ts:919:  return data.kind === "avatarIdentity";
> src/types/canvas.ts:937:    case "avatarIdentity":
> ```

## 🤖 Claude *(22:33:52)*


## 🤖 Claude *(22:33:55)*

**Achado crítico (o anticorpo cross-file):** o avatar do crew overlay **não** passa pelo `AgentAvatar` lucide — ele é concatenado como texto cru no label do sigma: `useConstellationSigma.ts:314` → `label: agent.avatar + ' ' + agent.name`. Trocar `'🤖'`→`'bot'` mostraria **"bot Nome"** literal (pior). Preciso ver se `agentAvatar` (linha 326) é desenhado em algum lugar antes de decidir o fix.

## 🤖 Claude *(22:33:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\npython3 - <<'PY'\nimport subprocess\nfor term in ['agentAvatar','reducer','nodeReducer','label:']:\n    r = subprocess.run(['grep','-rn','--include=*.tsx','--include=*.ts', term, 'src/hooks/useConstellationSigma.ts','src/pages/UnifiedCanvasPage.tsx','src/components/orchestrator/ConstellationMatrix.tsx'],\n                       capture_output=True, text=True)\n    print(f\"\\n##### {term} #####\")\n    print(r.stdout.strip() or \"(none)\")\nPY\necho \"\"; echo \"===== sigma label render context (310-330) =====\"; sed -n '308,330p' src/hooks/useConstellationSigma.ts",
  "description": "Check agentAvatar render + sigma label context"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ##### agentAvatar #####
> src/hooks/useConstellationSigma.ts:326:          agentAvatar: agent.avatar,
> src/components/orchestrator/ConstellationMatrix.tsx:59:  agentAvatar?: string;
> src/components/orchestrator/ConstellationMatrix.tsx:435:        agentAvatar: attrs.agentAvatar,
> src/components/orchestrator/ConstellationMatrix.tsx:899:                {tooltip.agentAvatar} {tooltip.label}
> 
> ##### reducer #####
> (none)
> 
> ##### nodeReducer #####
> src/components/orchestrator/ConstellationMatrix.tsx:287:      nodeReducer: (node, data) => {
> 
> ##### label: #####
> src/hooks/useConstellationSigma.ts:149:      return (data ?? []) as { module_path: string; squad_label: string }[];
> src/hooks/useConstellationSigma.ts:215:        label: node.name.length > 24 ? node.name.slice(0, 24) + '…' : node.name,
> src/hooks/useConstellationSigma.ts:314:          label: agent.avatar + ' ' + (agent.name.length > 16 ? agent.name.slice(0, 16) + '…' : agent.name),
> src/pages/UnifiedCanvasPage.tsx:30:const VIEW_OPTIONS: { mode: CanvasViewMode; label: string; icon: typeof Orbit }[] = [
> src/pages/UnifiedCanvasPage.tsx:31:  { mode: 'matrix', label: 'Matrix', icon: Boxes },
> src/pages/UnifiedCanvasPage.tsx:32:  { mode: 'memory', label: 'Memória', icon: BrainCircuit },
> src/pages/UnifiedCanvasPage.tsx:33:  { mode: 'universe', label: 'Universo', icon: Orbit },
> src/pages/UnifiedCanvasPage.tsx:64:function NetworkBadge({ on, label, color }: { on: boolean; label: string; color: string }) {
> src/pages/UnifiedCanvasPage.tsx:146:function Stat({ label, value }: { label: string; value: string | number }) {
> src/components/orchestrator/ConstellationMatrix.tsx:43:  label: string;
> src/components/orchestrator/ConstellationMatrix.tsx:103:  const [hubNode, setHubNode]             = useState<{ label: string; callsIn: number } | null>(null);
> src/components/orchestrator/ConstellationMatrix.tsx:184:        label: attrs.label || id,
> src/components/orchestrator/ConstellationMatrix.tsx:271:      setHubNode({ label: hubAttrs.label ?? hubId, callsIn: maxCallsIn });
> src/components/orchestrator/ConstellationMatrix.tsx:324:          return { ...data, color: DIM_COLOR, label: '', opacity: 0.15 };
> src/components/orchestrator/ConstellationMatrix.tsx:338:            label:      data.label,
> src/components/orchestrator/ConstellationMatrix.tsx:422:        label:       attrs.label ?? node,
> 
> ===== sigma label render context (310-330) =====
>         agentX = cx + Math.cos(orbitAngle) * 120;
>         agentY = cy + Math.sin(orbitAngle) * 120;
>       }
> 
>       if (!nodeSet.has(agentNodeId)) {
>         g.addNode(agentNodeId, {
>           label: agent.avatar + ' ' + (agent.name.length > 16 ? agent.name.slice(0, 16) + '…' : agent.name),
>           color: agent.color,
>           size: NODE_KIND_SIZE.crew_agent,
>           x: agentX,
>           y: agentY,
>           kind: 'crew_agent',
>           stability: 1,
>           community: -1,
>           isAgent: true,
>           agentRole: agent.role,
>           agentStatus: agent.status,
>           agentSquad: agent.squad,
>           agentAvatar: agent.avatar,
>           agentColor: agent.color,
>         });
>         nodeSet.add(agentNodeId);
>         agentNodeIds.add(agentNodeId);
> ```

## 🤖 Claude *(22:35:12)*


## 🤖 Claude *(22:35:15)*

Confirmado o anticorpo: `agentAvatar` renderiza como **texto cru em 2 sites** — label do sigma (`useConstellationSigma.ts:314`) e tooltip (`ConstellationMatrix.tsx:899`). Nenhum passa por lucide. Fix correto: remover o prefixo de avatar-texto dos 2 sites + normalizar o dado para `'bot'` (lucide-name consistente com crew store/seed).

Tenho o plano completo e verificado. Leio os pontos exatos de edição para fazer edits limpos:

## 🤖 Claude *(22:35:17)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/AvatarIdentityNode.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { memo } from "react";
> 2	import { Handle, Position, type NodeProps } from "@xyflow/react";
> 3	import { UserCircle } from "lucide-react";
> 4	import { cn } from "@/lib/utils";
> 5	import { type AvatarIdentityData } from "@/types/canvas";
> 6	
> 7	const HANDLE_CLASS = "!h-3 !w-3 !rounded-full !border-2 !border-border !bg-card";
> 8	
> 9	// avatar-clone-ai Fatia 3b — avatarIdentity canvas node (display-only; logic in AvatarIdentityInspector).
> 10	export const AvatarIdentityNode = memo(function AvatarIdentityNode({ data, selected }: NodeProps) {
> 11	  const d = data as unknown as AvatarIdentityData;
> 12	  const trained = Boolean(d.avatarIdentityId);
> 13	  const refCount = d.referenceUrls?.length ?? 0;
> 14	  const cover = d.referenceUrls?.[0];
> 15	
> 16	  return (
> 17	    <div
> 18	      className={cn(
> 19	        "w-[240px] overflow-hidden rounded-lg border bg-card text-foreground shadow-sm transition-all",
> 20	        selected ? "border-accent ring-2 ring-accent/30" : "border-border",
> 21	      )}
> 22	    >
> 23	      <Handle type="target" position={Position.Left} id="input_reference" className={HANDLE_CLASS} />
> 24	      <Handle type="source" position={Position.Right} id="output_identity" className={HANDLE_CLASS} />
> 25	      <header className="flex items-center justify-between gap-1.5 border-b border-border px-2.5 py-1.5">
> 26	        <div className="flex min-w-0 items-center gap-1.5">
> 27	          <UserCircle className="h-3 w-3 text-secondary" />
> 28	          <span className="truncate text-[11px] font-medium">{d.label}</span>
> 29	        </div>
> 30	        <span className="rounded-full bg-secondary/20 px-1.5 py-0.5 text-[9px] font-medium uppercase text-secondary">
> 31	          T{d.tier}
> 32	        </span>
> 33	      </header>
> 34	      <div className="w-full bg-muted/40 p-2.5">
> 35	        {cover ? (
> 36	          <img src={cover} alt="" className="h-20 w-full rounded object-cover" />
> 37	        ) : (
> 38	          <div className="flex h-12 w-full items-center justify-center text-[10px] text-muted-foreground">
> 39	            {trained ? "Identidade treinada" : "Suba retratos de referência"}
> 40	          </div>
> 41	        )}
> 42	      </div>
> 43	      <div className="flex items-center justify-between gap-2 px-2.5 py-1.5 font-mono text-[9px] text-muted-foreground">
> 44	        <span className="truncate">
> 45	          {d.provider}
> 46	          {trained && <span className="ml-1 text-accent">● treinada</span>}
> 47	        </span>
> 48	        <span className="shrink-0">{refCount} 📷</span>
> 49	      </div>
> 50	    </div>
> 51	  );
> 52	});
> 53	
> ```

## 🤖 Claude *(22:35:18)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/orchestrator/nodes/AgentNode.tsx",
  "offset": 40,
  "limit": 15
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 40	        <StatusIcon status={data.status} />
> 41	      </div>
> 42	
> 43	      <div className="flex items-center justify-between mt-2.5 pt-2 border-t border-white/5">
> 44	        <span className={`text-[9px] font-semibold px-1.5 py-0.5 rounded-md ${cfg.badge}`}>
> 45	          {cfg.label}
> 46	        </span>
> 47	        <div className="flex items-center gap-2">
> 48	          <span className="text-[9px] text-blue-400/50">{data.coinCost}c</span>
> 49	          <span className="text-[9px] text-white/20">⚡{(data.stabilityScore * 100).toFixed(0)}%</span>
> 50	        </div>
> 51	      </div>
> 52	
> 53	      <Handle type="source" position={Position.Right} className="!bg-blue-500 !border-2 !border-blue-300/50 !w-3 !h-3" />
> 54	    </div>
> ```

## 🤖 Claude *(22:35:18)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/orchestrator/ConstellationMatrix.tsx",
  "offset": 890,
  "limit": 15
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 890	            left:        Math.min(tooltip.x + 14, window.innerWidth - 240),
> 891	            top:         Math.max(tooltip.y - 10, 4),
> 892	            borderColor: tooltip.kind === 'crew_agent' ? (tooltip.agentColor ?? '#8C5AFF') + '60' : 'rgba(0,242,255,0.3)',
> 893	          }}
> 894	        >
> 895	          {tooltip.kind === 'crew_agent' ? (
> 896	            // Agent tooltip
> 897	            <div>
> 898	              <p className="font-semibold text-[11px] font-mono truncate max-w-[200px]" style={{ color: tooltip.agentColor ?? '#8C5AFF' }}>
> 899	                {tooltip.agentAvatar} {tooltip.label}
> 900	              </p>
> 901	              <div className="flex items-center gap-2 mt-1 text-[10px]">
> 902	                <span className="text-cyan-300 font-mono">{tooltip.agentRole}</span>
> 903	                <span
> 904	                  className="inline-flex items-center gap-1 font-mono"
> ```

## 🤖 Claude *(22:35:42)*


## 🤖 Claude *(22:35:43)*

Tenho todas as strings exatas e o plano verificado. Executo as edições, agrupadas por arquivo (disjuntas — sem risco de conflito). **Grupo A (Campanha):**

## 🤖 Claude *(22:35:46)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCampaigns.ts",
  "old_string": "  name: string;\n  description: string;\n  objective: string;\n  icon: string;\n  defaults: Partial<CampaignInsert>;",
  "new_string": "  name: string;\n  description: string;\n  objective: string;\n  icon: string; // MIV: serializable lucide string-name (rendered as a line-icon by CampaignWizard's TemplateIcon), never an emoji.\n  defaults: Partial<CampaignInsert>;"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCampaigns.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:35:47)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCampaigns.ts",
  "old_string": "    objective: 'launch',\n    icon: '\ud83d\ude80',",
  "new_string": "    objective: 'launch',\n    icon: 'rocket',"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCampaigns.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:35:49)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCampaigns.ts",
  "old_string": "    objective: 'promotion',\n    icon: '\ud83c\udf81',",
  "new_string": "    objective: 'promotion',\n    icon: 'gift',"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCampaigns.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:35:50)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCampaigns.ts",
  "old_string": "    objective: 'awareness',\n    icon: '\ud83d\udce3',",
  "new_string": "    objective: 'awareness',\n    icon: 'megaphone',"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCampaigns.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:35:51)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCampaigns.ts",
  "old_string": "    objective: 'engagement',\n    icon: '\ud83d\udcac',",
  "new_string": "    objective: 'engagement',\n    icon: 'message-circle',"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCampaigns.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:35:57)*

Agora o render em `CampaignWizard.tsx` (import + TemplateIcon + site de render):

## 🤖 Claude *(22:35:59)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CampaignWizard.tsx",
  "old_string": "import { ArrowLeft, ArrowRight, Check, Sparkles } from 'lucide-react';",
  "new_string": "import { ArrowLeft, ArrowRight, Check, Sparkles, Rocket, Gift, Megaphone, MessageCircle, type LucideIcon } from 'lucide-react';"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/CampaignWizard.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:36:04)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CampaignWizard.tsx",
  "old_string": "type SocialPlatform = Database['public']['Enums']['social_platform'];",
  "new_string": "type SocialPlatform = Database['public']['Enums']['social_platform'];\n\n// MIV: campaign template identity via line-icon (not emoji). `tpl.icon` is a serializable lucide\n// string-name; unknown names fall back to raw text so legacy values still render (mirrors NodeIcon).\nconst TEMPLATE_ICON: Record<string, LucideIcon> = {\n  rocket: Rocket,\n  gift: Gift,\n  megaphone: Megaphone,\n  'message-circle': MessageCircle,\n};\n\nfunction TemplateIcon({ name, className }: { name?: string; className?: string }) {\n  const Icon = name ? TEMPLATE_ICON[name] : undefined;\n  if (Icon) return <Icon className={className} />;\n  return <span className={className}>{name}</span>;\n}"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/CampaignWizard.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:36:05)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CampaignWizard.tsx",
  "old_string": "                          <span>{tpl.icon}</span>\n                          <span className=\"text-left text-xs\">{tpl.name}</span>",
  "new_string": "                          <TemplateIcon name={tpl.icon} className=\"h-4 w-4 text-cyan-300 shrink-0\" />\n                          <span className=\"text-left text-xs\">{tpl.name}</span>"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/CampaignWizard.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:36:12)*


## 🤖 Claude *(22:36:13)*

**Grupo B (Social):** limpar o emoji morto em `useSocialAccounts.ts` e endurecer o fallback do `PlatformGlyph` para `Globe` (os 7 platforms já têm glyph — emoji nunca renderiza):

## 🤖 Claude *(22:36:23)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useSocialAccounts.ts",
  "old_string": "// MIV chips: off-palette platform-brand colors (blue/purple/pink) \u2192 cyan (system). Neutral zinc\n// (X/TikTok) kept. `icon` is a string fallback rendered by SocialAccountsPage's <PlatformGlyph>\n// (out of this file's scope) \u2014 see note in that page; brand glyphs already cover most platforms.\nexport const SUPPORTED_PLATFORMS: { id: SocialPlatform; name: string; icon: string; color: string }[] = [\n  { id: 'linkedin', name: 'LinkedIn', icon: '\ud83d\udcbc', color: 'bg-cyan-600' },\n  { id: 'instagram', name: 'Instagram', icon: '\ud83d\udcf8', color: 'bg-gradient-to-r from-cyan-500 to-cyan-400' },\n  { id: 'facebook', name: 'Facebook', icon: '\ud83d\udc64', color: 'bg-cyan-500' },\n  { id: 'twitter', name: 'Twitter / X', icon: '\ud835\udd4f', color: 'bg-zinc-800' },\n  { id: 'tiktok', name: 'TikTok', icon: '\ud83c\udfb5', color: 'bg-zinc-900' },\n  { id: 'youtube', name: 'YouTube', icon: '\u25b6\ufe0f', color: 'bg-red-600' },\n  { id: 'pinterest', name: 'Pinterest', icon: '\ud83d\udccc', color: 'bg-red-500' },\n];",
  "new_string": "// MIV chips: off-palette platform-brand colors (blue/purple/pink) \u2192 cyan (system). Neutral zinc\n// (X/TikTok) kept. Brand identity is drawn by SocialAccountsPage's <PlatformGlyph> (keyed off the\n// platform id \u2192 lucide line-icon); the `icon` field is vestigial (kept for the type) and MUST stay\n// emoji-free \u2014 a Globe line-icon is the neutral fallback if a platform ever lacks a glyph.\nexport const SUPPORTED_PLATFORMS: { id: SocialPlatform; name: string; icon: string; color: string }[] = [\n  { id: 'linkedin', name: 'LinkedIn', icon: '', color: 'bg-cyan-600' },\n  { id: 'instagram', name: 'Instagram', icon: '', color: 'bg-gradient-to-r from-cyan-500 to-cyan-400' },\n  { id: 'facebook', name: 'Facebook', icon: '', color: 'bg-cyan-500' },\n  { id: 'twitter', name: 'Twitter / X', icon: '', color: 'bg-zinc-800' },\n  { id: 'tiktok', name: 'TikTok', icon: '', color: 'bg-zinc-900' },\n  { id: 'youtube', name: 'YouTube', icon: '', color: 'bg-red-600' },\n  { id: 'pinterest', name: 'Pinterest', icon: '', color: 'bg-red-500' },\n];"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useSocialAccounts.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:36:27)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx",
  "old_string": "// Brand glyphs for platforms that have a real logo (lucide-react dropped brand icons). Platforms\n// without a glyph (linkedin, twitter, wordpress) fall back to the emoji from SUPPORTED_PLATFORMS.\nconst PLATFORM_BRAND_ICON: Partial<Record<SocialPlatform, React.ComponentType<{ className?: string }>>> = {",
  "new_string": "// Brand glyphs for platforms that have a real logo (lucide-react dropped brand icons). Every\n// supported platform has an entry below, so the emoji-free Globe fallback is only a defensive\n// neutral for any future platform added without a glyph (MIV: never an emoji).\nconst PLATFORM_BRAND_ICON: Partial<Record<SocialPlatform, React.ComponentType<{ className?: string }>>> = {"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(22:36:30)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx",
  "old_string": "function PlatformGlyph({ platform, emoji }: { platform: SocialPlatform; emoji?: string }) {\n  const Icon = PLATFORM_BRAND_ICON[platform];\n  if (Icon) return <Icon className=\"h-6 w-6 text-foreground\" />;\n  return <span className=\"text-2xl\">{emoji}</span>;\n}",
  "new_string": "function PlatformGlyph({ platform }: { platform: SocialPlatform; emoji?: string }) {\n  const Icon = PLATFORM_BRAND_ICON[platform] ?? Globe;\n  return <Icon className=\"h-6 w-6 text-foreground\" />;\n}"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(22:36:39)*


## 🤖 Claude *(22:36:40)*

Preciso ler o `SocialAccountsPage.tsx` antes de editar (só vi via sed). Leio o trecho relevante:

## 🤖 Claude *(22:36:41)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx",
  "offset": 1,
  "limit": 36
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useState, useEffect } from 'react';
> 2	import { useSocialAccounts, SUPPORTED_PLATFORMS } from '@/hooks/useSocialAccounts';
> 3	import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
> 4	import { Button } from '@/components/ui/button';
> 5	import { Badge } from '@/components/ui/badge';
> 6	import { Input } from '@/components/ui/input';
> 7	import { Label } from '@/components/ui/label';
> 8	import { Loader2, Link2, Unlink, AlertTriangle, ExternalLink, CheckCircle2, Globe, Briefcase, Send } from 'lucide-react';
> 9	import { useToast } from '@/hooks/use-toast';
> 10	import { supabase } from '@/integrations/supabase/client';
> 11	import { useAuth } from '@/hooks/useAuth';
> 12	import { Instagram, Facebook, TikTok, YouTube, Pinterest } from '@/components/icons/brand-icons';
> 13	import type { Database } from '@/integrations/supabase/types';
> 14	
> 15	type SocialPlatform = Database['public']['Enums']['social_platform'];
> 16	
> 17	// Brand glyphs for platforms that have a real logo (lucide-react dropped brand icons). Platforms
> 18	// without a glyph (linkedin, twitter, wordpress) fall back to the emoji from SUPPORTED_PLATFORMS.
> 19	const PLATFORM_BRAND_ICON: Partial<Record<SocialPlatform, React.ComponentType<{ className?: string }>>> = {
> 20	  instagram: Instagram,
> 21	  facebook: Facebook,
> 22	  tiktok: TikTok,
> 23	  youtube: YouTube,
> 24	  pinterest: Pinterest,
> 25	  linkedin: Briefcase,
> 26	  twitter: Send,
> 27	};
> 28	
> 29	function PlatformGlyph({ platform, emoji }: { platform: SocialPlatform; emoji?: string }) {
> 30	  const Icon = PLATFORM_BRAND_ICON[platform];
> 31	  if (Icon) return <Icon className="h-6 w-6 text-foreground" />;
> 32	  return <span className="text-2xl">{emoji}</span>;
> 33	}
> 34	
> 35	export default function SocialAccountsPage() {
> 36	  const { accounts, isLoading, disconnectAccount, initiateOAuth, needsReauth } = useSocialAccounts();
> ```

## 🤖 Claude *(22:36:46)*


## 🤖 Claude *(22:36:47)*

Existe um módulo `brand-icons` dedicado. `Globe` já está importado. Aplico os 2 edits:

## 🤖 Claude *(22:36:49)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx",
  "old_string": "// Brand glyphs for platforms that have a real logo (lucide-react dropped brand icons). Platforms\n// without a glyph (linkedin, twitter, wordpress) fall back to the emoji from SUPPORTED_PLATFORMS.\nconst PLATFORM_BRAND_ICON: Partial<Record<SocialPlatform, React.ComponentType<{ className?: string }>>> = {",
  "new_string": "// Brand glyphs for platforms that have a real logo (lucide-react dropped brand icons). Every\n// supported platform has an entry below, so the emoji-free Globe fallback is only a defensive\n// neutral for any future platform added without a glyph (MIV: never an emoji).\nconst PLATFORM_BRAND_ICON: Partial<Record<SocialPlatform, React.ComponentType<{ className?: string }>>> = {"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:36:52)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx",
  "old_string": "function PlatformGlyph({ platform, emoji }: { platform: SocialPlatform; emoji?: string }) {\n  const Icon = PLATFORM_BRAND_ICON[platform];\n  if (Icon) return <Icon className=\"h-6 w-6 text-foreground\" />;\n  return <span className=\"text-2xl\">{emoji}</span>;\n}",
  "new_string": "function PlatformGlyph({ platform }: { platform: SocialPlatform; emoji?: string }) {\n  const Icon = PLATFORM_BRAND_ICON[platform] ?? Globe;\n  return <Icon className=\"h-6 w-6 text-foreground\" />;\n}"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/SocialAccountsPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:36:55)*


## 🤖 Claude *(22:36:56)*

**Grupo C (Spaces):** crio o componente `SpaceIcon` (mapa nome-sprite→lucide, cobrindo o `node-registry`) e faço os 2 render sites + o default do schema mapearem para linha em vez de texto cru:

## 🤖 Claude *(22:37:04)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/spaces/SpaceIcon.tsx",
  "content": "import {\n  Upload, FolderOpen, Search, ImagePlus, Image, Wand2, Maximize2, Pencil, Copy,\n  Palette, PenLine, Spline, Video, Mic, Combine, Sparkles, Scissors, AudioWaveform,\n  Music, Type, List, StickyNote, Smile, Boxes, type LucideIcon,\n} from 'lucide-react';\n\n// MIV: a Spaces node's `icon` is a serializable string-name (registry sprite ref / lucide\n// equivalent, node-registry.ts). This maps it to a lucide line-icon \u2014 never rendered as raw text\n// (the previous render sites showed the literal sprite-name or a legacy '\u2728' emoji). Unknown names\n// fall back to Sparkles so a node is always glyphed. Mirrors NodeIcon.tsx / AVATAR_ICON_MAP.\nconst SPACE_ICON_MAP: Record<string, LucideIcon> = {\n  upload: Upload,\n  'upload-reference': ImagePlus,\n  projects: FolderOpen,\n  assets: FolderOpen,\n  search: Search,\n  image: Image,\n  'image-generator': Wand2,\n  upscale: Maximize2,\n  enhance: Sparkles,\n  'edit-image': Pencil,\n  variations: Copy,\n  'design-standalone-v2': Palette,\n  sketch: PenLine,\n  vector: Spline,\n  video: Video,\n  'lip-sync': Mic,\n  'rectangle-merge': Combine,\n  split: Scissors,\n  'ai-voice': Mic,\n  'sound-effects': AudioWaveform,\n  music: Music,\n  text: Type,\n  'ai-stars': Sparkles,\n  'bullet-list': List,\n  'sticky-note': StickyNote,\n  smile: Smile,\n  'group-element': Boxes,\n  sparkles: Sparkles,\n};\n\nexport function SpaceIcon({ name, className }: { name?: string; className?: string }) {\n  const Icon = (name ? SPACE_ICON_MAP[name] : undefined) ?? Sparkles;\n  return <Icon className={className} />;\n}\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/src/components/spaces/SpaceIcon.tsx (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:37:10)*


## 🤖 Claude *(22:37:11)*

Agora conecto os render sites e o default do schema:

## 🤖 Claude *(22:37:13)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/spaces/SpaceNodeCard.tsx",
  "old_string": "import { estimateCost } from '@/hooks/useParamRegistry';\nimport type { SpaceNode, NodeStatus, Port } from '@/lib/spaces-schema';",
  "new_string": "import { estimateCost } from '@/hooks/useParamRegistry';\nimport { SpaceIcon } from '@/components/spaces/SpaceIcon';\nimport type { SpaceNode, NodeStatus, Port } from '@/lib/spaces-schema';"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/spaces/SpaceNodeCard.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:37:16)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/spaces/SpaceNodeCard.tsx",
  "old_string": "      <div className=\"flex items-center gap-2 border-b border-border px-3 py-2\">\n        <span className=\"text-base leading-none\">{data.icon}</span>\n        <span className=\"truncate text-sm font-medium\">{data.label}</span>\n      </div>",
  "new_string": "      <div className=\"flex items-center gap-2 border-b border-border px-3 py-2\">\n        <SpaceIcon name={data.icon} className=\"h-4 w-4 shrink-0 text-cyan-300\" />\n        <span className=\"truncate text-sm font-medium\">{data.label}</span>\n      </div>"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/spaces/SpaceNodeCard.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:37:19)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/spaces/ParamHUD.tsx",
  "old_string": "import { GenerationCluster } from '@/components/spaces/GenerationCluster';\nimport { ReferencePicker } from '@/components/spaces/ReferencePicker';",
  "new_string": "import { GenerationCluster } from '@/components/spaces/GenerationCluster';\nimport { ReferencePicker } from '@/components/spaces/ReferencePicker';\nimport { SpaceIcon } from '@/components/spaces/SpaceIcon';"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/spaces/ParamHUD.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:37:21)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/spaces/ParamHUD.tsx",
  "old_string": "        <h2 className=\"text-sm font-semibold flex items-center gap-2\">\n          <span>{node.data.icon}</span>{node.data.label}\n        </h2>",
  "new_string": "        <h2 className=\"text-sm font-semibold flex items-center gap-2\">\n          <SpaceIcon name={node.data.icon} className=\"h-4 w-4 shrink-0 text-cyan-300\" />{node.data.label}\n        </h2>"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/spaces/ParamHUD.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:37:22)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/lib/spaces-schema.ts",
  "old_string": "  icon: z.string().default('\u2728'),",
  "new_string": "  icon: z.string().default('sparkles'),   // MIV: serializable lucide string-name (SpaceIcon), never an emoji"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(22:37:30)*


## 🤖 Claude *(22:37:31)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/lib/spaces-schema.ts",
  "offset": 96,
  "limit": 6
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 96	  params: z.record(z.string(), z.unknown()).default({}),
> 97	  byok: z.boolean().optional(),                        // BR-SPACES-006
> 98	  locked: z.boolean().optional(),                      // node "Lock" action (UI-SPACES-008)
> 99	  headerHidden: z.boolean().optional(),                // "Hide header" action
> 100	  icon: z.string().default('✨'),
> 101	});
> ```

## 🤖 Claude *(22:37:39)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/lib/spaces-schema.ts",
  "old_string": "  icon: z.string().default('\u2728'),\n});",
  "new_string": "  icon: z.string().default('sparkles'),   // MIV: serializable lucide string-name (SpaceIcon), never an emoji\n});"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/lib/spaces-schema.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:37:45)*


## 🤖 Claude *(22:37:46)*

**Grupo D (Canvas/orchestrator glyphs):** `💎`→`mco` (texto, consistente com SpaceNodeCard/ParamHUD), `📷`→`Camera`, `⚡`→`Zap`:

## 🤖 Claude *(22:37:48)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/GenerateImageNode.tsx",
  "old_string": "            {d.aspectRatio} \u00b7 {info.coinCost} \ud83d\udc8e",
  "new_string": "            {d.aspectRatio} \u00b7 {info.coinCost} mco"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(22:37:49)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/ImageToVideoNode.tsx",
  "old_string": "{info.coinCost} \ud83d\udc8e",
  "new_string": "{info.coinCost} mco"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(22:37:50)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/SceneComposeNode.tsx",
  "old_string": "{d.cost} \ud83d\udc8e",
  "new_string": "{d.cost} mco"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(22:37:51)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/StyleTransferNode.tsx",
  "old_string": "preset \u00b7 {d.cost} \ud83d\udc8e",
  "new_string": "preset \u00b7 {d.cost} mco"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(22:37:57)*


## 🤖 Claude *(22:37:57)*

Preciso ler os arquivos antes de editar. Leio as janelas relevantes dos 5 arquivos do Grupo D:

## 🤖 Claude *(22:38:01)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/GenerateImageNode.tsx",
  "offset": 58,
  "limit": 12
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 58	          )}
> 59	        </p>
> 60	        <div className="flex items-center justify-between gap-2 font-mono text-[9px] text-muted-foreground">
> 61	          <span className="truncate">{info.label}</span>
> 62	          <span className="shrink-0">
> 63	            {d.aspectRatio} · {info.coinCost} 💎
> 64	            {info.higgsfieldCost != null && (
> 65	              <span className="ml-1 text-secondary">+{info.higgsfieldCost} hf</span>
> 66	            )}
> 67	          </span>
> 68	        </div>
> 69	        {d.error && (
> ```

## 🤖 Claude *(22:38:01)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/ImageToVideoNode.tsx",
  "offset": 96,
  "limit": 12
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 96	      </div>
> 97	      <div className="flex items-center justify-between gap-2 px-2.5 py-1.5 font-mono text-[9px] text-muted-foreground">
> 98	        <span className="truncate">
> 99	          {info.label} · {d.duration}s
> 100	        </span>
> 101	        <span className="shrink-0">
> 102	          {info.coinCost} 💎
> 103	          {info.higgsfieldCost != null && (
> 104	            <span className="ml-1 text-secondary">+{info.higgsfieldCost} hf</span>
> 105	          )}
> 106	        </span>
> 107	      </div>
> ```

## 🤖 Claude *(22:38:01)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/SceneComposeNode.tsx",
  "offset": 46,
  "limit": 12
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 46	        </p>
> 47	        <div className="flex items-center justify-between font-mono text-[9px] text-muted-foreground">
> 48	          <span className="truncate">
> 49	            {info.label} · {d.aspectRatio}
> 50	          </span>
> 51	          <span className="shrink-0">
> 52	            {d.cost} 💎
> 53	            {info.higgsfieldCost != null && (
> 54	              <span className="ml-1 text-secondary">+{info.higgsfieldCost} hf</span>
> 55	            )}
> 56	          </span>
> 57	        </div>
> ```

## 🤖 Claude *(22:38:02)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/StyleTransferNode.tsx",
  "offset": 42,
  "limit": 12
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 42	          <div className="flex h-full w-full items-center justify-center text-[10px] text-muted-foreground">
> 43	            Sem geração
> 44	          </div>
> 45	        )}
> 46	      </div>
> 47	      <div className="px-2.5 py-1.5 font-mono text-[9px] text-muted-foreground">
> 48	        preset · {d.cost} 💎
> 49	      </div>
> 50	    </div>
> 51	  );
> 52	});
> 53	
> ```

## 🤖 Claude *(22:38:03)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/RightPanel/inspectors/CharacterReferenceInspector.tsx",
  "offset": 174,
  "limit": 12
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 174	            )}
> 175	          </div>
> 176	        </Section>
> 177	
> 178	        <Section>
> 179	          <div className="rounded-md border border-secondary/30 bg-secondary/10 p-2.5 text-[11px] text-muted-foreground">
> 180	            <strong className="text-foreground">0 💎</strong> — apenas armazenamento. Suba várias fotos do mesmo
> 181	            rosto em ângulos diferentes (frontal, 3/4, perfil) para consistência. O modelo usa as primeiras{" "}
> 182	            <strong className="text-foreground">{MODEL_REF_CAP}</strong> como referência facial em Scene Compose /
> 183	            Gerar Imagem. Soul Character (lock entre cenas) chega na Phase 4.5 com o endpoint Higgsfield real.
> 184	          </div>
> 185	        </Section>
> ```

## 🤖 Claude *(22:38:09)*

Agora aplico os swaps `💎`→`mco`, `📷`→`Camera`, `⚡`→`Zap`:

## 🤖 Claude *(22:38:11)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/GenerateImageNode.tsx",
  "old_string": "            {d.aspectRatio} \u00b7 {info.coinCost} \ud83d\udc8e",
  "new_string": "            {d.aspectRatio} \u00b7 {info.coinCost} mco"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/GenerateImageNode.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:38:13)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/ImageToVideoNode.tsx",
  "old_string": "          {info.coinCost} \ud83d\udc8e",
  "new_string": "          {info.coinCost} mco"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/ImageToVideoNode.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:38:14)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/SceneComposeNode.tsx",
  "old_string": "            {d.cost} \ud83d\udc8e",
  "new_string": "            {d.cost} mco"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/SceneComposeNode.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:38:16)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/StyleTransferNode.tsx",
  "old_string": "        preset \u00b7 {d.cost} \ud83d\udc8e",
  "new_string": "        preset \u00b7 {d.cost} mco"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/StyleTransferNode.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:38:17)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/RightPanel/inspectors/CharacterReferenceInspector.tsx",
  "old_string": "            <strong className=\"text-foreground\">0 \ud83d\udc8e</strong> \u2014 apenas armazenamento.",
  "new_string": "            <strong className=\"text-foreground\">0 mco</strong> \u2014 apenas armazenamento."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/RightPanel/inspectors/CharacterReferenceInspector.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:38:23)*

Agora `📷`→`Camera` (AvatarIdentityNode) e `⚡`→`Zap` (orchestrator AgentNode) — ambos exigem novo import lucide:

## 🤖 Claude *(22:38:25)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/AvatarIdentityNode.tsx",
  "old_string": "import { UserCircle } from \"lucide-react\";",
  "new_string": "import { UserCircle, Camera } from \"lucide-react\";"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/AvatarIdentityNode.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:38:27)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/AvatarIdentityNode.tsx",
  "old_string": "        <span className=\"shrink-0\">{refCount} \ud83d\udcf7</span>",
  "new_string": "        <span className=\"flex shrink-0 items-center gap-0.5\">{refCount} <Camera className=\"h-2.5 w-2.5\" /></span>"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/nodes/AvatarIdentityNode.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:38:29)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/orchestrator/nodes/AgentNode.tsx",
  "old_string": "import { Loader2, CheckCircle2, XCircle, Clock } from 'lucide-react';",
  "new_string": "import { Loader2, CheckCircle2, XCircle, Clock, Zap } from 'lucide-react';"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/orchestrator/nodes/AgentNode.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:38:31)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/orchestrator/nodes/AgentNode.tsx",
  "old_string": "          <span className=\"text-[9px] text-white/20\">\u26a1{(data.stabilityScore * 100).toFixed(0)}%</span>",
  "new_string": "          <span className=\"flex items-center gap-0.5 text-[9px] text-white/20\"><Zap className=\"h-2 w-2\" />{(data.stabilityScore * 100).toFixed(0)}%</span>"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/orchestrator/nodes/AgentNode.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:38:40)*


## 🤖 Claude *(22:38:41)*

**Grupo E (Crew avatar):** normalizar dado para `'bot'` e remover o prefixo de avatar-texto dos 2 render sites (sigma label + tooltip):

## 🤖 Claude *(22:38:43)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCrewOverlay.ts",
  "old_string": "        avatar: a.avatar ?? '\ud83e\udd16',",
  "new_string": "        avatar: a.avatar ?? 'bot',   // MIV: serializable lucide string-name (AVATAR_ICON_MAP), never an emoji"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCrewOverlay.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:38:45)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useConstellationSigma.ts",
  "old_string": "          label: agent.avatar + ' ' + (agent.name.length > 16 ? agent.name.slice(0, 16) + '\u2026' : agent.name),",
  "new_string": "          label: agent.name.length > 16 ? agent.name.slice(0, 16) + '\u2026' : agent.name,"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(22:38:46)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/orchestrator/ConstellationMatrix.tsx",
  "old_string": "                {tooltip.agentAvatar} {tooltip.label}",
  "new_string": "                {tooltip.label}"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/orchestrator/ConstellationMatrix.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:38:53)*


## 🤖 Claude *(22:38:54)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useConstellationSigma.ts",
  "offset": 313,
  "limit": 3
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 313	        g.addNode(agentNodeId, {
> 314	          label: agent.avatar + ' ' + (agent.name.length > 16 ? agent.name.slice(0, 16) + '…' : agent.name),
> 315	          color: agent.color,
> ```

## 🤖 Claude *(22:38:58)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useConstellationSigma.ts",
  "old_string": "          label: agent.avatar + ' ' + (agent.name.length > 16 ? agent.name.slice(0, 16) + '\u2026' : agent.name),",
  "new_string": "          label: agent.name.length > 16 ? agent.name.slice(0, 16) + '\u2026' : agent.name,"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useConstellationSigma.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:39:03)*


## 🤖 Claude *(22:39:04)*

Todas as 5 frentes editadas. Agora **verificação material (Lei 1)**: tsc + re-scan de pictogramas nos arquivos tocados.

## 🤖 Claude *(22:39:12)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"===== tsc =====\"; npx tsc --noEmit 2>&1 | tail -20; echo \"tsc exit: ${PIPESTATUS[0]}\"\necho \"\"; echo \"===== re-scan pictographs in touched files =====\"\npython3 - <<'PY'\nfiles = [\n \"src/hooks/useCampaigns.ts\",\"src/pages/CampaignWizard.tsx\",\n \"src/hooks/useSocialAccounts.ts\",\"src/pages/SocialAccountsPage.tsx\",\n \"src/components/spaces/SpaceIcon.tsx\",\"src/components/spaces/SpaceNodeCard.tsx\",\n \"src/components/spaces/ParamHUD.tsx\",\"src/lib/spaces-schema.ts\",\n \"src/components/canvas/nodes/GenerateImageNode.tsx\",\"src/components/canvas/nodes/ImageToVideoNode.tsx\",\n \"src/components/canvas/nodes/SceneComposeNode.tsx\",\"src/components/canvas/nodes/StyleTransferNode.tsx\",\n \"src/components/canvas/RightPanel/inspectors/CharacterReferenceInspector.tsx\",\n \"src/components/canvas/nodes/AvatarIdentityNode.tsx\",\"src/components/orchestrator/nodes/AgentNode.tsx\",\n \"src/hooks/useCrewOverlay.ts\",\"src/hooks/useConstellationSigma.ts\",\n \"src/components/orchestrator/ConstellationMatrix.tsx\",\n]\nranges=[(0x1F300,0x1FAFF),(0x2600,0x27BF),(0x2B00,0x2BFF),(0x1F000,0x1F0FF),(0xFE00,0xFE0F),(0x2460,0x24FF)]\ndef em(c):\n    o=ord(c); return any(a<=o<=b for a,b in ranges)\nbad=0\nfor p in files:\n    with open(p,encoding='utf-8') as fh:\n        for i,l in enumerate(fh,1):\n            hit=[c for c in l if em(c)]\n            if hit:\n                bad+=1; print(f\"  {p}:{i} {hit} {l.strip()[:80]}\")\nprint(\"PICTOGRAPH-FREE \u2705\" if bad==0 else f\"\u26a0\ufe0f {bad} pictograph lines remain\")\nPY",
  "description": "tsc + pictograph re-scan of touched files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== tsc =====
> tsc exit: 0
> 
> ===== re-scan pictographs in touched files =====
>   src/components/spaces/SpaceIcon.tsx:9 ['✨'] // (the previous render sites showed the literal sprite-name or a legacy '✨' emo
> ⚠️ 1 pictograph lines remain
> ```

## 🤖 Claude *(22:39:18)*


## 🤖 Claude *(22:39:19)*

tsc **exit 0** ✅. O único pictograma restante está num **comentário** do SpaceIcon descrevendo o legado — reescrevo para não conter o literal (grep-zero honesto):

## 🤖 Claude *(22:39:21)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/spaces/SpaceIcon.tsx",
  "old_string": "// the previous render sites showed the literal sprite-name or a legacy '\u2728' emoji). Unknown names",
  "new_string": "// the previous render sites showed the literal sprite-name or a legacy sparkles emoji). Unknown names"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>String to replace not found in file.
> String: // the previous render sites showed the literal sprite-name or a legacy '✨' emoji). Unknown names
> (note: Edit also tried swapping \uXXXX escapes and their characters; neither form matched, so the mismatch is likely elsewhere in old_string. Re-read the file and copy the exact surrounding text.)</tool_use_error>
> ```

## 🤖 Claude *(22:39:23)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/spaces/SpaceIcon.tsx",
  "offset": 7,
  "limit": 5
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 7	// MIV: a Spaces node's `icon` is a serializable string-name (registry sprite ref / lucide
> 8	// equivalent, node-registry.ts). This maps it to a lucide line-icon — never rendered as raw text
> 9	// (the previous render sites showed the literal sprite-name or a legacy '✨' emoji). Unknown names
> 10	// fall back to Sparkles so a node is always glyphed. Mirrors NodeIcon.tsx / AVATAR_ICON_MAP.
> 11	const SPACE_ICON_MAP: Record<string, LucideIcon> = {
> ```

## 🤖 Claude *(22:39:27)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/spaces/SpaceIcon.tsx",
  "old_string": "// (the previous render sites showed the literal sprite-name or a legacy '\u2728' emoji). Unknown names",
  "new_string": "// (the previous render sites showed the literal sprite-name or a legacy sparkles emoji). Unknown names"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/spaces/SpaceIcon.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:39:44)*


## 🤖 Claude *(22:39:45)*

Agora o teste decisivo do anticorpo (lucide removeu ícones — tsc passa mas rollup quebra): **build de produção**. Estou no repo principal (branch `main`, `.env` presente), então build = deploy. Rodo o build e verifico materialmente:

## 🤖 Claude *(22:39:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ntest -f .env && echo \".env present \u2705 ($(wc -l < .env) lines)\" || echo \"\u26a0\ufe0f .env MISSING\"\necho \"--- build ---\"\nbun run build 2>&1 | tail -25\necho \"build exit: ${PIPESTATUS[0]}\"",
  "description": "Production build (rollup verifies lucide exports)",
  "timeout": 240000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> .env present ✅ (36 lines)
> --- build ---
> dist/assets/core.esm-DUsuk6cT.js                43.21 kB │ gzip:  14.35 kB
> dist/assets/hands-DDHDlvJ7.js                   45.32 kB │ gzip:  17.07 kB
> dist/assets/CampaignWizard-JTiV0hQJ.js          45.51 kB │ gzip:  14.38 kB
> dist/assets/AffiliateProductsPage-5D6RKmi7.js   46.49 kB │ gzip:  13.83 kB
> dist/assets/SettingsPage-hhIVj_OM.js            48.90 kB │ gzip:  13.64 kB
> dist/assets/useSpaces-ChPB-0g-.js               59.36 kB │ gzip:  14.30 kB
> dist/assets/SpaceCanvasPage-BYZP1mG8.js         66.71 kB │ gzip:  22.82 kB
> dist/assets/AIOSTerminal-1vjK6JIm.js            70.47 kB │ gzip:  21.71 kB
> dist/assets/Vignette--u6DmO2I.js                70.87 kB │ gzip:  17.39 kB
> dist/assets/DashboardHome-BnXpZfaF.js           74.45 kB │ gzip:  22.97 kB
> dist/assets/useNodeIntelligence-B5_aHAJs.js     98.76 kB │ gzip:  22.12 kB
> dist/assets/proxy-CoktXCAZ.js                  125.30 kB │ gzip:  41.24 kB
> dist/assets/ConstellationMatrix-BXuS9rJJ.js    136.07 kB │ gzip:  37.60 kB
> dist/assets/CanvasEditorPage-Dh4souXG.js       149.51 kB │ gzip:  39.39 kB
> dist/assets/index-BJK0uQcF.js                  167.01 kB │ gzip:  53.33 kB
> dist/assets/ConstellationPage-DmWkxLLk.js      186.21 kB │ gzip:  64.13 kB
> dist/assets/CartesianChart-D845hvv_.js         325.07 kB │ gzip:  96.84 kB
> dist/assets/index-D0nFQ_fa.js                  665.10 kB │ gzip: 197.33 kB
> dist/assets/react-three-fiber.esm-CXeO787r.js  824.11 kB │ gzip: 221.90 kB
> 
> (!) Some chunks are larger than 500 kB after minification. Consider:
> - Using dynamic import() to code-split the application
> - Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
> - Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
> ✓ built in 58.45s
> build exit: 0
> ```

## 🤖 Claude *(22:41:29)*


## 🤖 Claude *(22:41:31)*

**Build exit 0** em 58.45s — o anticorpo lucide (rollup) está **limpo**: todos os ~31 novos imports resolveram. Chunks frescos escritos em `dist/` (CampaignWizard, SpaceCanvasPage, ConstellationMatrix, CanvasEditorPage) → deploy live no repo principal.

Verificação material do deploy + env baked:

## 🤖 Claude *(22:41:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== env baked into bundle? ===\"; grep -oh \"https://[a-z0-9]*\\.supabase\\.co\" dist/assets/index-*.js 2>/dev/null | head -1 || echo \"checking...\"\necho \"=== fresh CampaignWizard chunk on disk ===\"; ls -la dist/assets/CampaignWizard-*.js 2>/dev/null\necho \"=== nginx serves app (dashboard 200)? ===\"; curl -s -o /dev/null -w \"%{http_code}\" https://login.mcorch.com/dashboard 2>/dev/null; echo \"\"",
  "description": "Verify deploy materially \u2014 env baked + nginx serving"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === env baked into bundle? ===
> https://bcyvddsykvehvpwstlfa.supabase.co
> === fresh CampaignWizard chunk on disk ===
> -rw-rw-r-- 1 ubuntu ubuntu 45532 Jul  5 19:40 dist/assets/CampaignWizard-JTiV0hQJ.js
> === nginx serves app (dashboard 200)? ===
> 200
> ```

## 🤖 Claude *(22:41:40)*


## 🤖 Claude *(22:41:43)*

Deploy verificado materialmente: env baked (`bcyvddsykvehvpwstlfa.supabase.co`), chunk fresco (19:40), nginx `/dashboard` **200**.

Agora, conforme ultracode, rodo um **workflow de verificação adversarial** (read-only) — 3 revisores independentes: (1) completude dos render sites, (2) trap de brand-icon lucide, (3) crítico de completude varrendo TODO o `src/` por pictogramas de superfície que eu possa ter deixado escapar fora dos meus 5 grupos.

## 🤖 Claude *(22:42:26)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'brand-tail-adversarial-verify',\n  description: 'Adversarially verify the brand-tail emoji\u2192lucide cleanup: render-site completeness, lucide export/brand-icon trap, and a whole-src product-surface pictograph sweep',\n  phases: [\n    { title: 'Verify' },\n    { title: 'Synthesize' },\n  ],\n}\n\nconst CONTEXT = `\nContext: an ongoing MCORCH \"brand-100\" cleanup replaced decorative pictograph emoji with lucide\nline-icons / neutral text across product surfaces. The just-applied edits (all already tsc-clean and\nproduction-build-clean) are:\n\nGROUP A (Campaign templates): src/hooks/useCampaigns.ts CAMPAIGN_TEMPLATES[].icon changed\n  \ud83d\ude80\u2192'rocket' \ud83c\udf81\u2192'gift' \ud83d\udce3\u2192'megaphone' \ud83d\udcac\u2192'message-circle'. Rendered by a new TemplateIcon component\n  in src/pages/CampaignWizard.tsx (lucide name\u2192component, raw-text fallback).\nGROUP B (Social): src/hooks/useSocialAccounts.ts SUPPORTED_PLATFORMS[].icon emptied (\ud83d\udcbc\ud83d\udcf8\ud83d\udc64\ud83c\udfb5\u25b6\ufe0f\ud83d\udccc / \ud835\udd4f \u2192 '').\n  src/pages/SocialAccountsPage.tsx PlatformGlyph now returns PLATFORM_BRAND_ICON[platform] ?? Globe\n  (no emoji fallback). All 7 platforms have a brand-icon entry.\nGROUP C (Spaces): new src/components/spaces/SpaceIcon.tsx (sprite-name\u2192lucide, Sparkles fallback).\n  Wired into src/components/spaces/SpaceNodeCard.tsx (was <span>{data.icon}</span>) and\n  src/components/spaces/ParamHUD.tsx (was <span>{node.data.icon}</span>). spaces-schema.ts icon default '\u2728'\u2192'sparkles'.\nGROUP D (Canvas/orchestrator): \ud83d\udc8e\u2192text 'mco' in canvas nodes GenerateImageNode/ImageToVideoNode/\n  SceneComposeNode/StyleTransferNode + CharacterReferenceInspector; \ud83d\udcf7\u2192<Camera/> in AvatarIdentityNode;\n  \u26a1\u2192<Zap/> in src/components/orchestrator/nodes/AgentNode.tsx.\nGROUP E (Crew avatar): src/hooks/useCrewOverlay.ts fallback '\ud83e\udd16'\u2192'bot'. The overlay avatar was rendered\n  as RAW TEXT in two sites \u2014 useConstellationSigma.ts:314 (sigma node label) and\n  ConstellationMatrix.tsx:~899 (tooltip) \u2014 both had the avatar text prefix REMOVED.\n\nThe known project anticorpo: (a) a changed persisted icon field can have render sites OUTSIDE the\nedited files that show it as raw text/emoji; (b) lucide-react DROPPED brand icons (Twitter/Instagram/\nFacebook/YouTube/TikTok/LinkedIn/Pinterest) \u2014 importing them from 'lucide-react' passes tsc but breaks\nthe rollup build. Working dir: /home/gcrUX/htdocs/constellation-orchestra. Use rg/grep/read (read-only).\nNote: the shell 'grep' is a ugrep BRE shim that can mangle literals \u2014 prefer 'rg' or python for searches.\n`\n\nconst FINDINGS_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  properties: {\n    findings: {\n      type: 'array',\n      items: {\n        type: 'object',\n        additionalProperties: false,\n        properties: {\n          severity: { type: 'string', enum: ['blocker', 'warn', 'nit'] },\n          file: { type: 'string' },\n          line: { type: 'integer' },\n          summary: { type: 'string' },\n          evidence: { type: 'string', description: 'exact code/line proving it' },\n        },\n        required: ['severity', 'file', 'summary', 'evidence'],\n      },\n    },\n    verdict: { type: 'string', enum: ['clean', 'issues-found'] },\n    notes: { type: 'string' },\n  },\n  required: ['findings', 'verdict'],\n}\n\nconst reviewers = [\n  {\n    label: 'render-site-completeness',\n    prompt: `${CONTEXT}\nYOUR JOB \u2014 render-site completeness. For EACH changed icon/avatar field, grep the WHOLE src/ tree for\nevery consumer and confirm none renders it as a raw emoji or raw string where a lucide icon is expected:\n1. Campaign template icon: find every read of CAMPAIGN_TEMPLATES / tpl.icon / .icon on a campaign template.\n   Confirm the ONLY render site is CampaignWizard's TemplateIcon. Any other site rendering {tpl.icon} raw = blocker.\n2. SUPPORTED_PLATFORMS[].icon: find every consumer. Confirm none renders the (now empty) .icon as text\n   in a way that would look broken. PlatformGlyph must key off platform id, not the emoji.\n3. Spaces node data.icon: find EVERY render of node.data.icon / data.icon across spaces. Confirm all go\n   through SpaceIcon now (SpaceNodeCard + ParamHUD). Any <span>{...icon}</span> left = blocker.\n4. Crew overlay avatar: find EVERY render of overlayAgent.avatar / agent.avatar / agentAvatar / tooltip.agentAvatar.\n   Confirm none prints it as raw text anymore (the two known sites were fixed \u2014 verify no THIRD site exists,\n   e.g. a sigma nodeReducer, a custom label, MemoryPage, UnifiedCanvasPage). Raw-text render of 'bot' = blocker.\nReport each missed/raw render site as a finding with file:line and the exact line as evidence. Verdict\n'clean' only if every field's render path is fully icon-ified.`,\n  },\n  {\n    label: 'lucide-export-and-brand-trap',\n    prompt: `${CONTEXT}\nYOUR JOB \u2014 lucide import audit (the rollup anticorpo). List EVERY lucide-react import added/present in the\ntouched files: CampaignWizard.tsx, SpaceIcon.tsx, AvatarIdentityNode.tsx, orchestrator/nodes/AgentNode.tsx,\nSocialAccountsPage.tsx. For SpaceIcon.tsx specifically, enumerate ALL 24+ icon names it imports\n(Upload, FolderOpen, Search, ImagePlus, Image, Wand2, Maximize2, Pencil, Copy, Palette, PenLine, Spline,\nVideo, Mic, Combine, Sparkles, Scissors, AudioWaveform, Music, Type, List, StickyNote, Smile, Boxes).\nFlag ANY that is NOT a real current lucide-react export, OR any brand icon (Twitter/Instagram/Facebook/\nYouTube/TikTok/LinkedIn/Pinterest) imported FROM 'lucide-react' (must come from components/icons/brand-icons\ninstead). Check node_modules/lucide-react exports if needed. The production build already passed exit 0 \u2014\nso treat a claim of \"missing export\" as requiring hard evidence. Report findings; verdict 'clean' if all resolve.`,\n  },\n  {\n    label: 'whole-src-pictograph-sweep',\n    prompt: `${CONTEXT}\nYOUR JOB \u2014 completeness critic. Independently scan ALL of src/ (*.ts/*.tsx) for pictograph emoji\n(unicode ranges U+1F300\u20131FAFF, U+2600\u201327BF, U+2B00\u20132BFF, U+2460\u201324FF, U+1F000\u20131F0FF; EXCLUDE plain\ntypographic arrows \u2192 \u2190 \u2194 \u21d2 and checkmark \u2713 \u2605 which MIV tolerates, and EXCLUDE src/test/** console.log\nemoji which are internal tooling). For every remaining hit, classify: (A) PRODUCT-SURFACE = rendered in\nJSX to a user (a real brand miss) \u2014 report as a finding with severity 'warn' (or 'blocker' if very visible);\n(B) comment/doc/typographic/test = OK, do not report. Your goal: find any product-surface decorative\npictograph that the 5 groups above did NOT cover. Be precise about whether each hit is actually rendered\n(inside JSX/returned string shown to user) vs in a comment or console.log. Verdict 'clean' if no\nproduct-surface pictograph remains beyond the 5 groups.`,\n  },\n]\n\nphase('Verify')\nconst results = await parallel(reviewers.map((r) => () =>\n  agent(r.prompt, { label: r.label, phase: 'Verify', schema: FINDINGS_SCHEMA })\n    .then((res) => ({ reviewer: r.label, ...res }))\n))\n\nconst all = results.filter(Boolean)\nconst blockers = all.flatMap((r) => (r.findings || []).filter((f) => f.severity === 'blocker').map((f) => ({ reviewer: r.reviewer, ...f })))\nconst warns = all.flatMap((r) => (r.findings || []).filter((f) => f.severity === 'warn').map((f) => ({ reviewer: r.reviewer, ...f })))\n\nreturn {\n  reviewerVerdicts: all.map((r) => ({ reviewer: r.reviewer, verdict: r.verdict, findingCount: (r.findings || []).length, notes: r.notes })),\n  blockers,\n  warns,\n  nits: all.flatMap((r) => (r.findings || []).filter((f) => f.severity === 'nit').map((f) => ({ reviewer: r.reviewer, ...f }))),\n}\n",
  "description": "Adversarial verify brand-tail cleanup"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: w6ijbczcm
> Summary: Adversarially verify the brand-tail emoji→lucide cleanup: render-site completeness, lucide export/brand-icon trap, and a whole-src product-surface pictograph sweep
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/be8df5a5-f15e-42b8-8659-5b49cc9f4cea/subagents/workflows/wf_0647c502-dad
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/be8df5a5-f15e-42b8-8659-5b49cc9f4cea/workflows/scripts/brand-tail-adversarial-verify-wf_0647c502-dad.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/be8df5a5-f15e-42b8-8659-5b49cc9f4cea/workflows/scripts/brand-tail-adversarial-verify-wf_0647c502-dad.js"} to iterate without resending the script.)
> Run ID: wf_0647c502-dad
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/be8df5a5-f15e-42b8-8659-5b49cc9f4cea/workflows/scripts/brand-tail-adversarial-verify-wf_0647c502-dad.js", resumeFromRunId: "wf_0647c502-dad"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(22:42:36)*


## 🤖 Claude *(22:42:51)*

Enquanto a verificação adversarial roda em background (vou ser notificado ao terminar), segue o **balanço material até aqui**:

## Cauda de brand — implementada e deployada ✅

| Grupo | Superfície | Fix | Prova |
|-------|-----------|-----|-------|
| **A** | Templates de campanha | `🚀🎁📣💬` → lucide-names + `TemplateIcon` no CampaignWizard | tsc 0 · build 0 |
| **B** | Ícones sociais | `💼📸👤🎵▶️📌𝕏` → limpos; `PlatformGlyph` fallback `Globe` (sem emoji) | 7 platforms já cobertos |
| **C** | Nós de Space | novo `SpaceIcon` (sprite-name→lucide) + 2 render sites + default `✨`→`sparkles` | **bug real**: render mostrava texto cru |
| **D** | Canvas/orchestrator | `💎`→`mco`, `📷`→`Camera`, `⚡`→`Zap` (7 nós/inspectors) | consistente c/ SpaceNodeCard |
| **E** | Avatar do crew | `🤖`→`bot` + removido prefixo texto-avatar de 2 render sites (sigma label + tooltip) | **anticorpo cross-file** capturado |

**Verificação material (Lei 1):**
- `tsc --noEmit` → **exit 0**
- `bun run build` → **exit 0** em 58.45s (limpa o anticorpo do rollup: ~31 imports lucide resolveram)
- grep-zero de pictogramas nos 18 arquivos tocados → **✅** (só restava 1 num comentário, reescrito)
- Deploy live: env baked (`bcyvddsykvehvpwstlfa.supabase.co`) · chunk fresco `CampaignWizard-JTiV0hQJ.js` (19:40) · nginx `/dashboard` **200**

O achado mais importante foi o **Grupo E**: o avatar do overlay **não** passava pelo `AgentAvatar` lucide — era concatenado como texto cru no label do sigma e no tooltip. Trocar cegamente `🤖`→`bot` teria mostrado **"bot Nome"** literal (exatamente o anticorpo do último seal). Removi o prefixo dos 2 sites.

Aguardando o workflow adversarial (`wf_0647c502`) confirmar: completude dos render sites · trap de brand-icon · varredura de pictogramas em todo o `src/`. Assim que terminar, aplico qualquer correção, faço a verificação ocular e commito.

## 👤 User *(22:48:36)*

<task-notification>
<task-id>w6ijbczcm</task-id>
<tool-use-id>toolu_01VPAMVtk6aDNonkvsw3tbu2</tool-use-id>
<output-file>/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/be8df5a5-f15e-42b8-8659-5b49cc9f4cea/tasks/w6ijbczcm.output</output-file>
<status>completed</status>
<summary>Dynamic workflow "Adversarially verify the brand-tail emoji→lucide cleanup: render-site completeness, lucide export/brand-icon trap, and a whole-src product-surface pictograph sweep" completed</summary>
<result>{"reviewerVerdicts":[{"reviewer":"render-site-completeness","verdict":"clean","findingCount":0,"notes":"Render-site completeness audit of all 4 in-scope changed fields — every render path is fully icon-ified; no raw-emoji/raw-string render survives where a lucide icon is expected. Searched the whole src/ tree with ripgrep 14.1.1 + python (shim-safe).\n\nFIELD 1 — Campaign template icon ('rocket'/'gift'/'megaphone'/'message-circle'): CLEAN.\n- Only consumer of CAMPAIGN_TEMPLATES is src/pages/CampaignWizard.tsx. The sole render of tpl.icon is line 236 via &lt;TemplateIcon name={tpl.icon}&gt;. applyTemplate() (line 87) never touches .icon.\n- TEMPLATE_ICON map (CampaignWizard.tsx:27-32) covers all 4 names; Rocket/Gift/Megaphone/MessageCircle imported from lucide-react are all valid generic icons (not dropped brand icons). The raw-text fallback (line 37) never fires for the 4 mapped names.\n\nFIELD 2 — SUPPORTED_PLATFORMS[].icon (all emptied to ''): CLEAN.\n- Only consumer is src/pages/SocialAccountsPage.tsx (lines 157, 222). Both pass the empty .icon only into &lt;PlatformGlyph&gt;'s unused `emoji` prop. PlatformGlyph (line 30-33) IGNORES emoji entirely and keys off `platform` id → PLATFORM_BRAND_ICON[platform] ?? Globe.\n- Anticorpo (b) correctly handled: dropped lucide brand icons (Instagram/Facebook/TikTok/YouTube/Pinterest) are imported from the LOCAL module @/components/icons/brand-icons (verified exports exist in brand-icons.tsx:37-57), NOT from lucide-react. Only Briefcase/Send/Globe come from lucide-react (all valid). All 7 platforms have an entry, so the empty .icon never surfaces.\n\nFIELD 3 — Spaces node data.icon (default '✨'→'sparkles'): CLEAN.\n- Both wired sites go through &lt;SpaceIcon&gt;: SpaceNodeCard.tsx:56 and ParamHUD.tsx:81. SpaceIcon (SpaceIcon.tsx:42-45) never renders raw text — unknown sprite-names fall back to Sparkles.\n- No &lt;span&gt;{...icon}&lt;/span&gt; raw render survives anywhere. Registry sprite-names (src/lib/node-registry.ts) are only rendered via SpaceIcon. Spotlight.tsx (the node picker over NODE_TYPES) renders only t.labelPt and t.id — it does NOT render t.icon at all. All other data.icon renders in the tree (orchestrator PublishNode/AgentNode/TriggerNode) go through the pre-existing NodeIcon component. spaces-schema.ts:100 default confirmed 'sparkles'.\n\nFIELD 4 — Crew overlay avatar (fallback '🤖'→'bot'): CLEAN, no third raw-text site.\n- The two known sites are fixed: useConstellationSigma.ts:314 sigma label = agent.name only (avatar prefix removed; agentAvatar stored as a node attribute at :326 but never rendered). ConstellationMatrix.tsx tooltip render (lines 898-899) prints {tooltip.label} only — tooltip.agentAvatar is captured into state (:435) but NEVER read in JSX.\n- No THIRD site: agentAvatar is read nowhere except the type decl (:59) and the state copy (:435), both non-render. The ConstellationMatrix nodeReducer (:287-340) sets label to '' (dimming) or data.label (clean name) for crew_agent — never injects the avatar. UnifiedCanvasPage only shows agentCount and delegates all rendering to useConstellationSigma. MemoryPage imports only inferSquad (zero avatar render).\n- New fallback 'bot' IS in AVATAR_ICON_MAP (AgentAvatar.tsx:13, and 'crown' at :12), so the shared AgentAvatar/AgentNode components render it as a &lt;Bot/&gt; icon. The two raw-text {avatar} fallbacks (AgentAvatar.tsx:32, AgentNode.tsx:28) only fire for UNMAPPED legacy names — documented intentional degradation (mirrors NodeIcon), not triggered by 'bot'/'crown'.\n\nGROUP D spot-check (out of primary scope, no persisted-field risk): AgentNode.tsx Zap imported from lucide-react (valid generic) and rendered as component; 'mco' is neutral display text next to coinCost. No anticorpo-(a) exposure.\n\nResidual emoji (NOT blockers): only 4 emoji remain in src/, all in src/test/ — console.log strings in aios-sql-bridge-smoke.test.ts / canvas-video-async-smoke.test.ts, and one fixture `icon: '✨'` in spaces-execution.test.ts. None reach any user render surface.\n\nNote on tooling: the shell `grep`/`rg` is a ugrep-shim function that mangled some literals in output (e.g. `data.icon`→`datan`, `@/lib/node-registry`→`@/lib/n`); I cross-verified every such hit by reading the files directly and re-running via python3, so those are display artifacts only, not real code."},{"reviewer":"lucide-export-and-brand-trap","verdict":"clean","findingCount":0,"notes":"Lucide import audit of the 5 touched files — CLEAN. All 49 imported identifiers resolve against the real lucide-react@1.11.0 ESM barrel (node_modules/lucide-react/dist/esm/lucide-react.mjs, 5834 exported names, verified by parsing every `export { X as Y }` alias). Zero missing exports, zero brand icons imported from lucide-react. This corroborates the exit-0 production build; the anticorpo is not triggered.\n\nPer-file lucide-react imports (all verified present):\n- src/pages/CampaignWizard.tsx (line 4): ArrowLeft, ArrowRight, Check, Sparkles, Rocket, Gift, Megaphone, MessageCircle, LucideIcon(type). (line 19): CalendarIcon. — Rocket/Gift/Megaphone/MessageCircle are the new TemplateIcon set for CAMPAIGN_TEMPLATES; all real exports.\n- src/components/spaces/SpaceIcon.tsx (lines 1-5): ALL 24 enumerated names verified present — Upload, FolderOpen, Search, ImagePlus, Image, Wand2, Maximize2, Pencil, Copy, Palette, PenLine, Spline, Video, Mic, Combine, Sparkles, Scissors, AudioWaveform, Music, Type, List, StickyNote, Smile, Boxes (+ LucideIcon type). None are brand icons; none missing.\n- src/components/canvas/nodes/AvatarIdentityNode.tsx (line 3): UserCircle, Camera — both real. (Note: actual path is src/components/canvas/nodes/, not spaces/.)\n- src/components/orchestrator/nodes/AgentNode.tsx (line 3): Loader2, CheckCircle2, XCircle, Clock, Zap — all real (Zap is the new emoji replacement).\n- src/pages/SocialAccountsPage.tsx (line 8): Loader2, Link2, Unlink, AlertTriangle, ExternalLink, CheckCircle2, Globe, Briefcase, Send — all real.\n\nBrand-icon anticorpo correctly avoided: SocialAccountsPage.tsx line 12 imports Instagram, Facebook, TikTok, YouTube, Pinterest from '@/components/icons/brand-icons' (the sovereign shim for the lucide-1.x-removed brand icons), NOT from 'lucide-react'. src/components/icons/brand-icons.tsx has no lucide-react import. Remaining Twitter/Instagram/etc. string matches in CampaignWizard.tsx (lines 41-47) are plain PLATFORMS label strings, not icon imports.\n\nVerification method: parsed the ESM barrel (rollup's actual resolution target) rather than the .d.ts, so aliases like CalendarIcon (default-as-alias) are captured; sanity-checked that a fabricated name (FakeIconXYZ) correctly reports MISSING while Sparkles/CalendarIcon report present."},{"reviewer":"whole-src-pictograph-sweep","verdict":"clean","findingCount":0,"notes":"Exhaustively scanned all src/ *.ts/*.tsx (tests excluded per spec) with a Python classifier over the 5 specified pictograph ranges (U+1F300–1FAFF, U+2600–27BF, U+2B00–2BFF, U+2460–24FF, U+1F000–1F0FF), tolerating arrows/✓/★. Classifier self-verified: it correctly flags all 15 emoji from the 5 edited groups (🚀🎁📣💬💼📸👤🎵📌💎📷⚡✨🤖 + 𝕏). Result across product code: ZERO in-scope pictograph emoji remain. A broader emoji-presentation scan (U+1F000–1FAFF + ☀-➿) also returned zero.\n\nPersisted-icon anticorpo (a) fully covered: every render site of the changed fields routes through an icon component — SpaceIcon (SpaceNodeCard.tsx:56, ParamHUD.tsx:81), NodeIcon (orchestrator TriggerNode/AgentNode/PublishNode), TemplateIcon (CampaignWizard.tsx), PLATFORM_BRAND_ICON→Globe fallback (SocialAccountsPage.tsx:31). Crew agentAvatar is stored as a Sigma node attribute (useConstellationSigma.ts:326, ConstellationMatrix.tsx:435) but NEVER rendered as raw text: sigma label (line 314) = agent.name only; matrix tooltip renders label/agentRole/agentStatus, not agentAvatar. Other .avatar render sites are non-emoji: TestimonialsSection.tsx:63 renders plain initials ('MC'/'R
... (truncated 1181 chars, full result in /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/be8df5a5-f15e-42b8-8659-5b49cc9f4cea/tasks/w6ijbczcm.output)</result>
<usage><agent_count>3</agent_count><subagent_tokens>276703</subagent_tokens><tool_uses>69</tool_uses><duration_ms>370081</duration_ms></usage>
</task-notification>

## 🤖 Claude *(22:49:01)*


## 🤖 Claude *(22:49:06)*

Veredito unânime dos 3 revisores: **`clean` · 0 findings**.

- **Render-site completeness** → clean: os 4 campos totalmente icon-ificados; **nenhum 3º site cru** para o avatar do crew; Spotlight (picker) não renderiza `t.icon`.
- **Lucide export/brand-trap** → clean: 49 identificadores resolvem contra lucide-react@1.11.0 (5834 exports); brand-icons vêm do shim local, não do lucide — corrobora o build exit-0.
- **Whole-src pictograph sweep** → clean: **zero** pictogramas de produto remanescentes; os 4 restantes estão só em `src/test/` (console.log/fixture, não renderizados).

Nenhuma correção necessária. Agora o **gate ocular (Lei 1)** — obrigatório para mudança de Canvas Studio. Verifico o tooling disponível:

## 🤖 Claude *(22:49:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== canvas UI audit tool ===\"; ls -la scripts/qa/audit-canvas-ui.ts 2>/dev/null && head -30 scripts/qa/audit-canvas-ui.ts 2>/dev/null\necho \"\"; echo \"=== vision-qa + session tooling ===\"; ls -la scripts/qa/vision-qa.ts scripts/qa/gen-user-session.ts 2>/dev/null\necho \"\"; echo \"=== VISION_MCP_PAT in .env? ===\"; grep -c \"VISION_MCP_PAT\" .env 2>/dev/null && echo \"PAT present\" || echo \"no PAT\"",
  "description": "Check ocular verification tooling"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === canvas UI audit tool ===
> -rw-r--r-- 1 ubuntu ubuntu 8928 Jul  2 01:20 scripts/qa/audit-canvas-ui.ts
> /// <reference types="node" />
> import { chromium } from 'playwright';
> import { createClient } from '@supabase/supabase-js';
> import { existsSync, readFileSync } from 'fs';
> import { spawnSync } from 'child_process';
> import { join } from 'path';
> 
> // Load .env
> const ROOT = '/home/gcrUX/htdocs/constellation-orchestra';
> const envPath = join(ROOT, '.env');
> if (existsSync(envPath)) {
>   const raw = readFileSync(envPath, 'utf-8');
>   for (const line of raw.split('\n')) {
>     const m = line.match(/^([^#=\s][^=]*)=(.*)$/);
>     if (m) {
>       process.env[m[1].trim()] = m[2].trim().replace(/^["']|["']$/g, '');
>     }
>   }
> }
> 
> const supabaseUrl = process.env.SUPABASE_URL;
> const serviceKey = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY);
> 
> if (!supabaseUrl || !serviceKey) {
>   console.error("❌ Missing Supabase credentials in env.");
>   process.exit(1);
> }
> 
> const targetCanvasId = '880b5eba-b41c-490d-8cab-1058def85bc9';
> const redirectTarget = `https://login.mcorch.com/dashboard/canvas/${targetCanvasId}`;
> 
> === vision-qa + session tooling ===
> -rw-rw-r-- 1 ubuntu ubuntu 2490 Jun  9 15:33 scripts/qa/gen-user-session.ts
> -rw-rw-r-- 1 ubuntu ubuntu 5375 Jun 21 19:45 scripts/qa/vision-qa.ts
> 
> === VISION_MCP_PAT in .env? ===
> 1
> PAT present
> ```

## 🤖 Claude *(22:49:14)*


## 🤖 Claude *(22:49:15)*

`audit-canvas-ui.ts` existe (Playwright + injeta sessão via service key). Leio o resto para entender o fluxo antes de rodar:

## 🤖 Claude *(22:49:16)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/audit-canvas-ui.ts",
  "offset": 30,
  "limit": 200
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 30	const redirectTarget = `https://login.mcorch.com/dashboard/canvas/${targetCanvasId}`;
> 31	
> 32	async function runAudit() {
> 33	  console.log("🚀 Starting User-Zero E2E Canvas Audit...");
> 34	  
> 35	  const supabase = createClient(supabaseUrl!, serviceKey!, {
> 36	    auth: { autoRefreshToken: false, persistSession: false }
> 37	  });
> 38	
> 39	  console.log("🔐 Generating one-time Magic Link for gabrielcall@gmail.com...");
> 40	  const { data: linkData, error: linkErr } = await supabase.auth.admin.generateLink({
> 41	    type: 'magiclink',
> 42	    email: 'gabrielcall@gmail.com',
> 43	    options: { redirectTo: redirectTarget }
> 44	  });
> 45	
> 46	  if (linkErr || !linkData?.properties?.action_link) {
> 47	    console.error("❌ Failed to generate magic login link:", linkErr);
> 48	    process.exit(1);
> 49	  }
> 50	
> 51	  const magicLink = linkData.properties.action_link;
> 52	  console.log(`🔗 Magic Link generated successfully.`);
> 53	
> 54	  console.log("🌐 Launching headless Chromium browser...");
> 55	  const browser = await chromium.launch({ headless: true });
> 56	  const context = await browser.newContext({
> 57	    viewport: { width: 1920, height: 1080 }
> 58	  });
> 59	  const page = await context.newPage();
> 60	
> 61	  console.log("✈️ Navigating via magic link to authenticate...");
> 62	  await page.goto(magicLink);
> 63	
> 64	  console.log("⏳ Waiting for redirection and React app initialization...");
> 65	  // Wait until URL matches the target canvas page
> 66	  try {
> 67	    await page.waitForURL(`**/dashboard/canvas/${targetCanvasId}*`, { timeout: 15000 });
> 68	    console.log(`📍 Redirected successfully to: ${page.url()}`);
> 69	  } catch (err) {
> 70	    console.error("❌ Timeout waiting for auth redirection. Current URL:", page.url());
> 71	    await browser.close();
> 72	    process.exit(1);
> 73	  }
> 74	
> 75	  // Wait a few seconds for data fetching and React Flow rendering
> 76	  console.log("⏳ Waiting for Canvas data to render and page title to update...");
> 77	  try {
> 78	    await page.waitForFunction(() => document.title.includes("Canvas Studio"), { timeout: 15000 });
> 79	  } catch (err) {
> 80	    console.warn("⚠️ Timeout waiting for document title to contain 'Canvas Studio'. Checking current title...");
> 81	  }
> 82	
> 83	  console.log("🧪 Performing structural assertions...");
> 84	  
> 85	  // Assert title
> 86	  const title = await page.title();
> 87	  console.log(`📝 Page Title: "${title}"`);
> 88	  if (!title.includes("Canvas Studio")) {
> 89	    console.error("❌ Assert Failed: Page title does not contain 'Canvas Studio'.");
> 90	    await browser.close();
> 91	    process.exit(1);
> 92	  }
> 93	
> 94	  // Assert React Flow elements
> 95	  const reactFlowCount = await page.locator('.react-flow').count();
> 96	  console.log(`📊 React Flow containers found: ${reactFlowCount}`);
> 97	  if (reactFlowCount === 0) {
> 98	    console.error("❌ Assert Failed: React Flow canvas component (.react-flow) was not found in DOM.");
> 99	    await browser.close();
> 100	    process.exit(1);
> 101	  }
> 102	
> 103	  // Check for node elements
> 104	  const nodeCount = await page.locator('.react-flow__node').count();
> 105	  console.log(`🟢 Rendered Canvas Nodes: ${nodeCount}`);
> 106	  if (nodeCount === 0) {
> 107	    console.warn("⚠️ Warning: React Flow canvas is loaded but contains 0 nodes.");
> 108	  }
> 109	
> 110	  // Evaluate Zustand store state for node n_wxgqyr9i
> 111	  console.log("🔍 Checking Zustand state of node n_wxgqyr9i...");
> 112	  const nodeState = await page.evaluate(() => {
> 113	    // Access the Zustand state from the window object (if exposed) or from the react flow nodes
> 114	    const reactFlowEl = document.querySelector('.react-flow');
> 115	    if (!reactFlowEl) return null;
> 116	    
> 117	    // We can extract state by querying the react flow internals or inspecting the DOM for the video node
> 118	    const videoNode = document.querySelector('[data-id="n_wxgqyr9i"]');
> 119	    if (!videoNode) return { error: "Node DOM element not found" };
> 120	    
> 121	    // Check if the inspector button is showing "Aguardando webhook" or "Gerar vídeo"
> 122	    const inspectorButton = document.querySelector('.border-t button');
> 123	    const buttonText = inspectorButton?.textContent || "";
> 124	    
> 125	    // Check if video element is rendered inside the node
> 126	    const hasVideoElement = videoNode.querySelector('video') !== null;
> 127	    
> 128	    return {
> 129	      buttonText,
> 130	      hasVideoElement,
> 131	      classes: videoNode.className
> 132	    };
> 133	  });
> 134	  console.log("📊 UI State evaluated:", nodeState);
> 135	
> 136	  // Take the E2E Full HD screenshot IN MEMORY (feeds the Vision gate) + best-effort IDE artifact copy.
> 137	  // NOTE (security, 2026-07-02): the public copy at dist/canvas_e2e_latest.png was REMOVED — it served a
> 138	  // screenshot of the LOGGED-IN dashboard on a public nginx URL. Viewing now uses the signed URL below (1h).
> 139	  console.log("📸 Capturing Full HD (1920x1080) Screenshot...");
> 140	  const shotBuffer = await page.screenshot({ type: 'png', fullPage: false });
> 141	  const artifactPath = `/home/ubuntu/.gemini/antigravity-ide/brain/385b7ecd-9ab8-4317-ad60-8f19fcbea7c0/canvas_e2e_latest.png`;
> 142	  try {
> 143	    await page.screenshot({ path: artifactPath, type: 'png', fullPage: false });
> 144	    console.log(`✅ Screenshot saved to IDE Artifacts: ${artifactPath}`);
> 145	  } catch (e: any) {
> 146	    console.warn("⚠️ IDE artifact copy skipped:", e.message);
> 147	  }
> 148	
> 149	  console.log("⏳ Waiting 5 seconds to ensure autosave completes...");
> 150	  await page.waitForTimeout(5000);
> 151	  await browser.close();
> 152	
> 153	  // ── Vision QA gate (Diretiva Sovereign 2026-06-26 · SOP creative-qa-vision-gate.md Amendment 2026-07-02) ──
> 154	  // The creative eye judges the REAL screenshot: white screen, visible error, broken layout. Mechanical gate:
> 155	  // vision-qa exit != 0 OR verdict without APROVADO OR with REPROVADO ⇒ audit FAILS. Fail-closed on missing PAT
> 156	  // (--no-vision is the explicit, logged exception).
> 157	  if (process.argv.includes('--no-vision')) {
> 158	    console.warn("⚠️ Vision gate PULADO por --no-vision (exceção explícita — registrar o porquê no seal)");
> 159	  } else {
> 160	    if (!process.env.VISION_MCP_PAT) {
> 161	      console.error("❌ Vision gate: VISION_MCP_PAT ausente (.env). A diretiva 2026-06-26 exige o olho criativo em todo print de inspeção. Use --no-vision só como exceção explícita.");
> 162	      process.exit(1);
> 163	    }
> 164	    const supa = createClient(supabaseUrl!, serviceKey!, { auth: { persistSession: false } });
> 165	    const shotKey = `qa-audits/canvas-e2e-${Date.now()}.png`;
> 166	    const up = await supa.storage.from('generated-images').upload(shotKey, shotBuffer, { contentType: 'image/png', upsert: true });
> 167	    if (up.error) {
> 168	      console.error("❌ Vision gate: upload do screenshot falhou:", up.error.message);
> 169	      process.exit(1);
> 170	    }
> 171	    const { data: signed } = await supa.storage.from('generated-images').createSignedUrl(shotKey, 3600);
> 172	    if (!signed?.signedUrl) {
> 173	      console.error("❌ Vision gate: signed URL falhou");
> 174	      process.exit(1);
> 175	    }
> 176	    console.log(`🔗 Screenshot (signed, 1h): ${signed.signedUrl}`);
> 177	    const question = "Print 1920x1080 do Canvas Studio (dashboard MCORCH). Avalie SO problemas visuais objetivos: tela branca/vazia, mensagem de erro visivel, layout quebrado/sobreposto, texto ilegivel. Comece a resposta com exatamente APROVADO ou REPROVADO, seguido do motivo em 1 frase.";
> 178	    console.log("👁️ Vision QA gate — julgando o screenshot real...");
> 179	    const vq = spawnSync('bun', ['run', join(ROOT, 'scripts/qa/vision-qa.ts'), 'image', signed.signedUrl, question], {
> 180	      encoding: 'utf-8', env: process.env, timeout: 120000,
> 181	    });
> 182	    const out = `${vq.stdout ?? ''}${vq.stderr ?? ''}`;
> 183	    console.log(out.trim());
> 184	    // Best-effort cleanup — the QA object should not linger in the bucket.
> 185	    await supa.storage.from('generated-images').remove([shotKey]).then(() => {}, () => {});
> 186	    const approved = vq.status === 0 && /APROVADO/i.test(out) && !/REPROVADO/i.test(out);
> 187	    if (!approved) {
> 188	      console.error(`❌ Vision gate REPROVOU o print (exit=${vq.status}). Auditoria BLOQUEADA.`);
> 189	      process.exit(1);
> 190	    }
> 191	    console.log("✅ Vision gate APROVADO");
> 192	  }
> 193	
> 194	  console.log("🎉 E2E User-Zero Canvas Audit Completed Successfully!");
> 195	}
> 196	
> 197	runAudit().catch(err => {
> 198	  console.error("❌ Audit failed unexpectedly:", err);
> 199	  process.exit(1);
> 200	});
> 201	
> ```

## 🤖 Claude *(22:49:28)*


## 🤖 Claude *(22:49:29)*

É o gate canônico de Canvas Studio (Lei 1): magic-link → Playwright headless 1920×1080 → assert render → **Vision QA** (honra `feedback_vision_qa_always`, fail-closed). Exercita a `CanvasEditorPage` que reconstruí. Rodo:

## 🤖 Claude *(22:49:31)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nbun run scripts/qa/audit-canvas-ui.ts 2>&1 | tail -35\necho \"audit exit: ${PIPESTATUS[0]}\"",
  "description": "Run Canvas Studio E2E UI audit + Vision QA gate",
  "timeout": 180000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 🚀 Starting User-Zero E2E Canvas Audit...
> 🔐 Generating one-time Magic Link for gabrielcall@gmail.com...
> 🔗 Magic Link generated successfully.
> 🌐 Launching headless Chromium browser...
> ✈️ Navigating via magic link to authenticate...
> ⏳ Waiting for redirection and React app initialization...
> 📍 Redirected successfully to: https://login.mcorch.com/dashboard/canvas/880b5eba-b41c-490d-8cab-1058def85bc9#access_token=eyJhbGciOiJFUzI1NiIsImtpZCI6ImQwNzNhM2RiLWE4ZjMtNGU2OC04ZWM1LTZmNmI0N2QxNDQ1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2JjeXZkZHN5a3ZlaHZwd3N0bGZhLnN1cGFiYXNlLmNvL2F1dGgvdjEiLCJzdWIiOiJhZGEzOWZhZS02N2UxLTRlNTMtYWYxYy01YTE4ZTFjMTA4ZTgiLCJhdWQiOiJhdXRoZW50aWNhdGVkIiwiZXhwIjoxNzgzMjk1Mzc0LCJpYXQiOjE3ODMyOTE3NzQsImVtYWlsIjoiZ2FicmllbGNhbGxAZ21haWwuY29tIiwicGhvbmUiOiIiLCJhcHBfbWV0YWRhdGEiOnsicHJvdmlkZXIiOiJnb29nbGUiLCJwcm92aWRlcnMiOlsiZ29vZ2xlIl0sInJvbGUiOiJhZG1pbiJ9LCJ1c2VyX21ldGFkYXRhIjp7ImF2YXRhcl91cmwiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMcXVZaC1yTjV2ODRoYUlaUDRaTW9ucUdHN0lkNTBLOHdCZXd3TWJiTks0ZHNURmRHdz1zOTYtYyIsImVtYWlsIjoiZ2FicmllbGNhbGxAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImZ1bGxfbmFtZSI6IkdhYnJpZWwgQ2FsZGVpcmEiLCJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJuYW1lIjoiR2FicmllbCBDYWxkZWlyYSIsInBob25lX3ZlcmlmaWVkIjpmYWxzZSwicGljdHVyZSI6Imh0dHBzOi8vbGgzLmdvb2dsZXVzZXJjb250ZW50LmNvbS9hL0FDZzhvY0xxdVloLXJONXY4NGhhSVpQNFpNb25xR0c3SWQ1MEs4d0Jld3dNYmJOSzRkc1RGZEd3PXM5Ni1jIiwicHJvdmlkZXJfaWQiOiIxMDMyODkwOTY4NTE5NzExNzg0NzUiLCJzdWIiOiIxMDMyODkwOTY4NTE5NzExNzg0NzUifSwicm9sZSI6ImF1dGhlbnRpY2F0ZWQiLCJhYWwiOiJhYWwxIiwiYW1yIjpbeyJtZXRob2QiOiJvdHAiLCJ0aW1lc3RhbXAiOjE3ODMyOTE3NzR9XSwic2Vzc2lvbl9pZCI6IjJiOTE1ZWY1LWVmYjktNDExOC05MGRiLTc2NGM3OGE1YzU4YiIsImlzX2Fub255bW91cyI6ZmFsc2V9.mza_6wXE24uFgkalUzPjPPbIYYljQGq06tvN4Jphx13xI5s8or3BntFMV2BZeu6-eprsnY_lWxwLmDc91sc3kg&expires_at=1783295374&expires_in=3600&refresh_token=s3exwyeveugq&sb=&token_type=bearer&type=magiclink
> ⏳ Waiting for Canvas data to render and page title to update...
> 🧪 Performing structural assertions...
> 📝 Page Title: "#02 - Mood board 5 lanes - 5 mundos — Canvas Studio — MCORCH"
> 📊 React Flow containers found: 1
> 🟢 Rendered Canvas Nodes: 29
> 🔍 Checking Zustand state of node n_wxgqyr9i...
> 📊 UI State evaluated: {
>   buttonText: "Cinematic Story Arc — 3 atos33 lanes × 4 colunas. Mesmo personagem em 3 cenários: cidade → praia → floresta. Ativa o modo Pipeline.~180 mcoCoins·Pipeline",
>   hasVideoElement: true,
>   classes: "react-flow__node react-flow__node-imageToVideo nopan selectable draggable",
> }
> 📸 Capturing Full HD (1920x1080) Screenshot...
> ✅ Screenshot saved to IDE Artifacts: /home/ubuntu/.gemini/antigravity-ide/brain/385b7ecd-9ab8-4317-ad60-8f19fcbea7c0/canvas_e2e_latest.png
> ⏳ Waiting 5 seconds to ensure autosave completes...
> 🔗 Screenshot (signed, 1h): https://bcyvddsykvehvpwstlfa.supabase.co/storage/v1/object/sign/generated-images/qa-audits/canvas-e2e-1783291784228.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9iNzFjZTA4Yy0xYWFjLTQ1MDUtOGEyZC04Y2Y5ZTU5MzI5MzIiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJnZW5lcmF0ZWQtaW1hZ2VzL3FhLWF1ZGl0cy9jYW52YXMtZTJlLTE3ODMyOTE3ODQyMjgucG5nIiwic2NvcGUiOiJkb3dubG9hZCIsImlhdCI6MTc4MzI5MTc4NCwiZXhwIjoxNzgzMjk1Mzg0fQ.oQmbLKfbTjgle1OD_bU0yURpZ2P3GOhGIz7t6hXXIC8
> 👁️ Vision QA gate — julgando o screenshot real...
> ✅ vision_describe_image
>    confidence: high  cost_mco: 0
>    APROVADO, a imagem não apresenta problemas visuais objetivos como telas brancas, mensagens de erro visíveis, layout quebrado ou texto ilegível.
> ✅ Vision gate APROVADO
> 🎉 E2E User-Zero Canvas Audit Completed Successfully!
> audit exit: 0
> ```

## 🤖 Claude *(22:49:59)*


## 🤖 Claude *(22:50:02)*

**Gate ocular Canvas Studio (Lei 1) — PASSOU.** Título "Canvas Studio — MCORCH" · 1 React Flow · **29 nós renderizados** (incluindo `imageToVideo`, que toquei 💎→mco) · screenshot 1920×1080 · **Vision QA APROVADO** (high confidence, sem tela branca/erro/layout quebrado) · **exit 0**.

Vou inspecionar o screenshot real eu mesmo para confirmar visualmente a mudança de marca (mco/ícones, sem emoji):

## 🤖 Claude *(22:50:02)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/ubuntu/.gemini/antigravity-ide/brain/385b7ecd-9ab8-4317-ad60-8f19fcbea7c0/canvas_e2e_latest.png"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': 'iVBORw0KGgoAAAANSUhEUgAAB4AAAAQ4CAIAAABnsVYUAAAQAElEQVR4nOzdC0BT1f8A8DPYdofAeMgGyFCePhBKMA01QSWf+UzNR6ammaVp+k/NZ+Yje5g/LV+lZWo+E/NZKoYJJqImmOAQZaAyBDZkMEB2t8H+5+4BA7axjYeK38+PH92de+65j3Mdd9979r10Op2JAHgh+fi0zcjIQAAAAAAAAAAAAAAAgKZhgwAAAAAAAAAAAAAAAACAJgABaAAAAAAAAAAAAAAAAABNAgLQAAAAAAAAAAAAAAAAAJoEBKABAAAAAAAAAAAAAAAANAkIQAMAAAAAAAAAAAAAAABoEhCABgAAAAAAAAAAAAAAANAkIAANAAAAAAAAAAAAAAAAoEnQUWOh0QyXq1QIAAAAAAAAAAAAAAAAwIunYQFoY0FnY3UgGA0AAAAAAAAAAAAAAAAvDGsD0OaEno0tBWFoAAAAAAAAAAAAAAAAeAFYHoC2LvRctwUIQwMAAAAAAAAAAAAAAECLZmEA2kT02dIc0Lg+xKABAAAAAAAAAAAAAACg2eCorCMbObsglh2i06kfTKmkfmTlqEiCSqSNG7a1JABtMMRc74Doqgp1txti0AAAAAAAAAAAAAAAANAMbG2RuwdqzaEmamEyqZ9WrZBra1RRgR6LUX4eNdEYzAtA1xt6Nh2G1kSZDWbegHQcAAAAAAAAAAAAAAAA0HRwDNaNg9w9teOdTcPhaa4HcnVD+bmoQNzwyK1VDyE0GHo2kYJDP8oMEWcAAAAAAAAAAAAAAOpjb2fThktwXBh2hA2LaUOnN/jBbC88pVIlk1eWyypEhYq8x4rSJ40zwvdZZ2ODfP2ptBsWwaFqL2/k4IgeZKHKStQA9QWg64aVa0Wc6w1A11IVhtaPQUNUGgAAAAAAAAAAAAAANYdWtsEBrVo7Mx4XKR5L5OXySrm8slIFAeiGsqGpmEwbO6aNmwujo2+rgiJFasaTFh6GJgjkG4BYLGQdJ2fUvhPKEiBShqxFo9OZJufTDLys+1s7Ufefgao6rKyZqPu7ui4EoEGz8vFpm5GRgQAAAAAAAAAAAACeDQw6raOvXRsuM0+syCsgVQiCzk2FRlN5tCY8uYycfPmdrHKFsiVGJm3pqH0HRFgbfa4ik6GMdOophVYxGYA2J/qsiTtTrzQlevVVuv+okDYSDTFo8CxpYACay+WuXLmyT58+eMLMRUQi0cWLF1etWoUnEAAAAAAAAAAAAIAeO8Kma5CDjQ26e/8JjHduHjY2qg4+rZQV6N/bJaS8ZUUmcdg2oD2yd0CNorQUCe5aF7y1tbGxNTzHdPRZ+2NTPWGj/7LqB+kFpg2l7DC4FgCahbOzU2FhIbLWpk2bRo8ebW9vb/4iuHLnzp29vLxOnTqFAAAAAAAAAAAAAHRsbdCrLzmSikpBtgwGPjcblYpWIFGy7eltPYmcfLJFDY7leqDWbqixMJlUJuiyUmQ58x5CaGDUM9ILN2vzb6g82iAfH1U7X2rmgyx0/z4t7xEupkZAUzdt8H9skKqyOuOzJhN0rXzQADwnIiIi8O/hw4dfuXJFUyIWi/FvDodjbJGePXueOHGid+/eCAAAAAAAAAAAAEBPWCeHigr04BGJQLO7/0gW0NYutJPDv7etCbCaz87Ozt/fH08IBILy8nLUdOh05O6BGhdusLDAikQcRgLQxkYiG4g+Uz+ql8NUY95S2bWiPbyPf/B8Vfdw1ZjxtPIy2m+HaSk3q/Jx1I5BG1wFxKPB88DV1RX/roo+myMhIQH/bt26NQIAAAAAAAAAAADQ8XBjOjvS/7tbZv4ifjxWB99WTg62eQWK5LSS4tIW/SS9ppfxsLxLB3vcEXkFctQEWCzWokWLZs2aZWtLpaNQKpVbtmxZv369XN4kq0MebZCtLWpcuEHcrPAhspAZI6BrDXxGetFnddqNyunvo9Ycmy9XI4Vclw+aGvdMBZ0JonLOJ6pu3Wx++YmKO1dqllfHoKtahkHQABhGd2zTjstmMBBSlBeKckQlZt1horsEDxza3e7O2dPXH1n5fFIWt52Xqx1eL7XinAci6x9zamDzHF24rmylNL9QIrMydX1zobPwptrhQ994W0p3aeNlV57zSKLUvW5wZ5mLYHsHBnuzpaKMexki0uxyUpSRWl1OcIO7BnPRw38TMqQ1W/fu2iuYS1QXkKLUyzeyjd22N9qOFftVf1MEO6DrK4GsYv0t0m5w8b3LjbAJddsnuAGBAdxaR09X28CB1Z9PbZmT6MblVBFpeq2GO86yTbeuI4wcPQO7ZvLEMGMXzD0a1Xvj7USg4uwbNzQLGFiFkU1C1p6TJvoaAAAAAAAAS3T0tXuYb8El5bxJvOF93YpKFPmPFb5eLKVS9cXOB1f+a+gHnOcOw86WWV5hQdjepOx8soOPXRMFoP/3v/8FBgZOnjz5xo0b+OUrr7zy6aefenp6fvTRR6jR4Uixq3nDHxkOqK0PckDo4V0kMWPHcbO5OajCsrsdhgLQJhIx6+d91kSfFyympfxH27NLXWJbvbgmoCxX2Hz7pWrAoMr/W2jzv/XIRi8GjaeMBZ118WiCzWGTYrH6Xx/B8Q9wkmZkiE39WyQ4Ad6EKFsorfV5nxfWt2dYQACPLb6dkHDxym2qETaPR4iFdZurqsxB4ozbt5MSNNX1V+LvTYirV4JX2jmAQ2bfzqi9XgMbaHxLpOw6zWr2Bc/35pAigVj3HsLm+XNJoekjAVoCumvo2JmjfBi619L7cUf2nk6V1BcMtXMNCOnILk/AMU1kFceAgdOmh7HV0+VJP3/5a2oJagx0F7xDk7u7o3IFsmOUZ5z+8efYB00cdrUSDgyPnD65lxdDoUAMlJ90fO/BhEfKqlljQ0WnD8Y/svwrJ149J07rlPzjpljdsg3uLLOwu87dsWdFlLvmVfHl7ya/vz4Bx8qMlBPe/Vbs2DHzFSdNuSxl95z3lx/PwG85Tl3f37x3QvF3g0auvaF/VUN4D16x54teeg/VlV1e0Hfcngwjb1PG2rFCvU0RAaM2H988hDw2Y+TlG9qSkWs3fzuV2r+HB8f1nXuhQZtQu33c+vq9mycE6g7Gw2Nzxs05pD4Sxg+sXnOB1KEMvjCj75Tj2cbWaaxDLWZFRxg+ekZ2DRk9MczbBbOOhmb9I9cfrjrq+cdm9Hv/uMzgKoxtktSKc9JEXwMAAAAAAGAZFzbdjmUjKTb3Y+ZrYU5DIlqv3JZ16UYxfkkwaLMneC181/vtxfxymdEhnozWTrPf4bim5nz9V3mZnd3oabxhnjaaWfJi6c4fc68rDBWqr5AZHo5ThrgFedii4vLLf+WfTFcqUBOwI7p1Zwe54bXI+anF1/Pqi3LatZo42d1FkLcT7xFqBI+LlL48Fu4OibSRx8z16tVr8ODB3bt316Rvxc6dO/fff/9du3bt119/vXr1KmpcDo7Ixqb+ai9PQSvmIFfNCxKd/RJtPI1Mdy1uFjdeXIQsUd+m1H7qoC7jM0079pmKPl84T63b+A/t/FnanbTKd9+rnTa66gcZiXpzO4/8+uSd3Jzc3Jz7t+L/OrpqEI+oXYczcPs1qgL1c23bOz289WsQnB4fbY/57/qpXxb0Yd8+uff4FTG7x1sz3ntnUJ9BM97ryqnRmrbyX9smdy6+8dvWX89me4/76vS1xNOb3uuhX9PJu++C6P9ytSvNOr10UOeArpNXnf5PcOe/mANfjw3jEHV3pf4tqdls7qWN74Rp9oXghr3z3V+68lz+0QV9eU4IvBiUhdd+XDJ//vyFq7ccuWPXc+Lknm3q+9qC8lH8d4sWrYm+Y3VotyT115V4nfNX702T1v8HpXXr1m5u5qS0d+w4aGiIMu7H1QuXLlqy/th9btTI7lzz0tA3N1a7qKFh9OSfVy9chDf1eGHAwKGhLrpNZbh6+fhw7RplyxvUWeYeeSJ4/IqFUe4P/1w2btCIBcfuEb1mrh0fzDZazu46c+3MVxAOIY7oO2jGj5fJkKkr5vbjmlwHCxHqEN+cyVpT1lzIfhbicDg8vGL5EPeHx9asOaPeICJ4yp7jO6cGF/+bUowark773H5zV0wIxIdixqAefSeviX3YdtTyFYPVb+bWHFiD6zTScc3A2NEzumtGTozG3gUc/546JJD18M816hW9/31CsdFVNN65aqKvAQAAAAAAsJCnG/OxxIKI5yudHS9cLcTR5zUf+Wxf0Z5UqLYcFBJ0mwBvO6PL0Jn9xnsN8pT/nayJ1dr6t7V3Vcj46aU38U9meaHCWCG+5necP993jB/KuFac5+Q8+yOfMd5N8YxEeq/+7r2cZP9cLLhWzOw7pHW3ej8llD+Jjs7Zc7G8sUZAY7gjuK4M1Nj69u2bkpJSFX3WyMvL4/P5eBZqdI5mfMKyD0Yz3keuj9DWOWj2UnRTjgZ9hF7zbJzGa7I0hlIdPla9HIrcOLS9u6iwso2NtlyXgkP71EGVeixzJcIxaNWCpargl3X5oGlIk6PDJDLj4s4vSF7Atve7qj+ic/uM68s7+6tA/1vivJ6DOuse+ZZ6+MsNvyZVDV0iAoZ/vWvjuEAWyj7xwcT5J9SjkoRi4e3bQe/8sP/rzknzduo1pK1MJnwx6YMtmkZOrvsgI/uH/d+MW/V73z6fvTtrp7pYvVVE5567xnnjV7LbJ3bu/JVPot/O3th2+rtBfSdvCuscMHHil0nSuo2b2pJazd7Y+791vyWp91Sc9NuXX3DDeizrSo2yyj634YufLooReLEoJYJrZ2ODOw7t6OWY8EiiZLUJ7t49tKMXW1l4/07y9aQ7VJoMOrfb2AmRXnZ0urJclHBkr27MrmPwmAndJdevKfy7d3RFouTY2OQH1ek8WO26DYoI9XJlKApzUhNiEwQWDnd+/PjxgAEDbGxszp49a6oe3c6dayfNSMmg/qYqH107d5rRrkQb3za4O4Y3m9rJkR0fnNaNSKa7hI4cG/yo6rXBpqjMH/6hEd1DfLiOqCQn5VrCtVQTKS/odq6udoqcOw80m5p0+rRdQIk6LD15bKirnau7nZ3XxHkBCqRUFqYd2/vHAzv9bVBvYUDG8SPXRdrj365bVEQol1F4J/lBVdzaWGfV7ZFrAiO5V8w98k7sQC4L3Tvz46ELN6TEj39OGfwxNxiXGCknitsGcFH+5e+/P5aA43Lff99vcK9RgYFc4kzV+FSnwFHLZw5+hStNPfTj94duiKiNxv8vfnjjwpkzopprJwIGz5w7vh9enhTd+/fY998fr85wYKAdHErsOWrK+MGvBHJlotTUM8f2qLeiXoaaUodq16rDwzO04WF1TgZWxsE5y9c/HHn4cEjNm5De/abMnTKEyi2RfePM7h8P1bvmuu2zA3q90hbd2/3N98epcbS713cd2evj4H7BTsezi7nGDyw7eOTc98e/0laaeuyCrL4AprEORVKju1DPUTV89AztsOGjRxjbtQtGTgyu8V2gDqKRo2H8XCKcvNkEyr9x7NAh3Xq4AUZWYfxc0P33ygAAEABJREFUNXEoDB1YE31t/AgCAAAAAABgmJODrajQgrQP7q0ZSbepT+/R58WffeCDqBwE6GE+6eFGpNx7YmgJmnd3zxkh6J8fH/39WF3AwIG7isJU0caj5dVDz9iGChFy8Xfp7iQ/ufHhtvQKlCx3WNaubzArOru89pg1O7tu/nRXDxYzryyPbR+Ayi5ce5KvpMY19+rODnCylReX/nOtNLtcW7lXd4cAarCzjJ9cfP2xCtkxPFpVCC6WCvB0caGrkxNiGKmp3iP3DuwurW2ZqCIvs0I3Vtq2U3Ar9KTCw8+hLSq/drkkTbsuZrdQpyBPavj2zWTpf49NBSQfFyk4Lo0fgO7cuXNWVlbd8rt37wYHB6NGZ9eq/joObZAHgfhH0ckr1KjnPe2RQ1fEZDZO4zWZMRhbf2yyJsSsDkOrxrxls+V/NZ9GaKPJy6E3UT3LZvMG1di31K3RquPUdVdRC0lm3Dh7RvvVW6ce4wYF6AfZCU6wt0yojcbKSKms+hM1O2zG119RMV8kOv7FurP634mV8n/7YuuVbCmJyNqVRRf3Hr8t1at5YvOJe3iC23fp6tk92HqbVXuKzL59JUMd0XLq+s5HffWGaluwJfrNymodB92U7NlMWQCanh2XbYfKy5U4Bttz8syxoXaPUq+lSF3Dxs6cNtSfiqkoywsfZGA55a5eXm2qQ512rl4BIVEDI70kGYJCu5Cxs2cObKf9zjidGzF95tgQu8KU6ykiRseR06dFtWNZumEoJiamsrJy0KBBJmvR1X85dLFU2YPrsfF3JOqArcHdMbLZSqmonN2pZ6iXZvforp16hriXFxZqotFGjgyd233C5FGd0INrsbHXHtj1nDhzcjcX47fflCWinBK7ThER/o7qTX2k2VSlNP8OPrz388sRDg1n3LmDXwkeUdFhhqOXT/URt+PiV1w73RFWbxK7UHBHxO0WGeKqLTfSWdoeCWWX3Lmegvca90ikiR4x68iLMs5cvicLHDx1SAA3oN8UaqDohWOpxUbLEcGihoiSmncdmUyK340Itl4cMHDwwpm9uE7eXUfN3Lxn/cjqEZ8s78HLvz90/NCOteM1dw0J7uD1e/eumNDPG7/HcftN+Hjn4W+r6xtoh91zxZ7Dmz/u5y0TiVjB4z/evHfzlGAzRpQa3CQcHl6+Isr94cE1VeFn/K574/tx4+YeSq09/Jna1MOHv5jaL4AgUdvBM789cWbH+ACTqzbYPjW8FhEES9tpeIKFf+leGDyweNVr9+z8eEIvb4LbdebC8YH1/BM01nFGd6G+o2q0Q+swdvTqOWfqnBhGzz1k9GgYOZfYPZcfupBwdsfUEBZyH7z2TAJ24dDynmwTqzC4SSYOhdEDa6KvAQAAAAAAsAxB2JSV159Ul0XQRvZrbc+ykZZWONpTHyQrK1UqbbZb5NjKpqTM8AAmhofL7DFO8mvZW5OrKzARjenhOn+23/9mew3zszVRWBfTUASS4WbXLZj5ML3cIZjtmid96OYyyB+3YNutv3vftrS8zNKHDIfRQ5y9qQ3HhZy+nrS89LJSJ/bA/i7+VCGNiSrlCnV0WCm//Jf4+mNjNatWSXP1d+rmrdtOO2ZQqOvo7g7MvCcZyGHYCO26Xu7D7etWwU+W8p/YDRzC6WZ8mDiGOwJ3B2psHTt2xGGEuuU4AI1noUbHMGfMsTrWXPUIxP+2oPffRece1L8cw+IvhVuyAE0XOKYhlUcbFasVdXvFxrZqTDSPw5gz3OHVDtTWX02Xf3e89NFjBTXMWRNfJkmVo5OK607Lz6Veqmi1nz1o7FGE4qQTxzv3nUON/2V1feutzr+uvKIb9OQd5l2clC2bXGcZovO4JZ/0VCeqyL54IkFYaxgbmZ3wdwavbmXRjbM3auZWlt4+9/e9GYGBeNXvLRh3YuJOvtERccXF1PhA6sMn4cRlW7UlANRGd/Tq1BGVUwksBvbilqScfUDd4sw4tysjX/NwwJQcNG+6j48rXfBIWSJI+EOA6G0ivDr1rNmMUppx7sDBZAlC13IYCycHBLjSHzxS4vBtx1Av6bWf90YLcFvXMkrmzQwNdo978MDiVEc4EjpgwIAJEyYcPHgQWajc4O6IjG12fnJGYfdOwV7n8GbSXQOCueUZsfdlppp6RHfkujLyE2LjqEHJqanXY+vZImVOwtnksOmvf7S6V37atdhzmiHjSklq/PFUHCH26sTOiTt9XKC7GWTifRQf4W5e5df2/qzOsoGD/PMme2nmGO4sdY+UJ+/9+SBVP+mBst4eMePIiy4sH/c+uWPz5iu3cXDw3sEZ4xaqA6aGy4kA9UIs7uDvE1b0uvfN+jqjOYtvrBn3/vFsoufy44c/7jWqF/fMMXUsru3gRXNFxQS3rXuvqJ7eaOT7h6RdR/ULlKV8N27k2gQpEfz+4TNf9KPqXzDaDuthwp4163f/eCaDJLrOPX58RUCvAO6O1GzEDh48pKu3JqZJktmpZ87oD9St29QhUeCUtSuinB4eXLD+THHg+3vWj0LHls/ZcUNqOFm/E7Wp6OHuKYMXXhCxu849fHxFr5G9vI9lZJCGV00EG2w/48K/D6dOGLV2bcY3xx5yB8+dEohkl//Nro7Y1j2weNW92upWjeee2TtBl2XJ8KqNdCjXyC5kk0aPqtGjl21kr0lTjzoweM4YPDEyjJ2Txo+Gk+Fz6XJqauoNJxG3K7dtCCFKvXyZaiU7VWr0KBHGzlXjh8LYuXGmvr4GAAAAAADAbK1YNpWqepJadOlov/x9n9v3ymKuSO4+eDK8j9vuE7l375dv/JW6tm/vw3JvTdx7WG5gSTpz0HjPLk8er4guRaHtomeyLnxzd1sBDiPaeLQlmOkVqEPr+fOZ6Iv7p54YKsxTlT6UZihch7/T1iFdzvR2fs1JeTZdbjhlp0JZWCAvfFJZWKAsfaIeZ23HDHCquH5efC5PhVLLC4PtmAxcTlQXCiqmjHEJcKMJDF5M2xmqiaeRKj+9+Fy67cuDWd2UNTYg7drjc5kVSFAZMIYd4ISyHyO8xtLc0puZckXmk+sJyLSKShXuDtSo7O3teTxeWlpa3Vm4sF27dgRBkGSj5rGkWzKI28ETBbRXh6Pl6GEKyi5tzMY1S5iaWTUwuSpTs+418vWhPXygGRFdNcx57WSnLn7acdoDw+zcnW2n/u+xNmZNRZZp1CI+Pig/rzr5hv4TC40iM04cuTK5a1/qQ2jA4HE9tlw5px70zA7ozBXdNhS+ZXd+662emnFIxRlJBh5pT4pTE26T0lqVZdlJdZ7tR2Yk3RahQCqXZdiIvgF7+beNnQ8slpN2vJc4456uGYu2BIDa6OyAngNdqVwPyvLCy3sPnlM/D7BElEP3D4no1s6VgSOWPmw6nVXfv31leXm5dkJajry09el2rnZ0tlfPoSNDqKHIdl6OdnZ2dHr1OGVL2NjYXLt2DVlMaWJ3DG22DEegpTgCzT33QOQYEOxVnnFQF3821pQsJyWlsOeo2bPbpTwolOQIUlK0mTmMbpMk9eCXn8V1DOnes2f3ifO6d7f2gYn4CDNQebn24QV4olzhZbq+I64v1dZXlotKFCH19kh9R54IGDx34fjg4svH/hRxX+k3atGiGxkL9qRKDZff0y5FijLupTrdE8nqpJwX3csuJqnbZ6k4nhfoxMYVRKmH9uy+kHro+0M3pOyuy48f/7jX4GDusVQnNguxnF6Zunb9KBz68/am7s+xnYy2Q6ZeOPRjca9+Q1as9yYIp2BvvDTBIqh31rb95q5f8YpueGnKd6mXb4ikxjeJCOi1fFEvHB6es54KqnsHBr/yCko1nj2fYFObKsu495C64pHe+H6w9/e6WYZWTQaMMtz+jQvrl+8O3Dx11Iqdg/PvFTuxUP6fhy7cIzXDZQ0dWGrVTkiWqll1cXYqPjedTKxaaqRD7xnfBWNHlTTaodmE6QNuWN1zxvCJgQPQRs5Jo0dD00F1zyVp6vG1C4/jpoP7hXBvHMLTVVkzDK+CNLJJCcYPhdEDm22srwEAAAAAALCUjQ3NhqYyEYO2tUULprb99VTelf+kBIN28u+Cwa+5/vhZh39uUtepwYH2QyJa7zud97jIwIdH+7atR3dU/fNj/nWpyqWqVFqy9v9urtVU8PPcusi1m6ftqWRDhXlKxeOiNV8Ihg9x6+VBICfb0ju5R+/UP167ChNVlGrGNaOKtFR1cNNOv1BVqkBMsxavp6aG/Il2TLhcoTmeFfzU0qBenivCVHm55Wmpxf9kyk088MqmCbJbv/fee9nZ2ZcvX647Cxfm5ubiClu3bkVPi0cftOYT7ZE9MBX9lIoam0VDpnU94NCq4oc9tIdZ6MctVfNYTNpLPjViYCHtGPYsm7LyyqoS1cAhle/OoPfsgkpKdA2qzFkxmX1279nZfdXZkb0HvdM34OJvGSQVf2ZnJ2STYXXqE9zOwQHaaWl2tqjux0FSfOW3I3Uqk6LsOqO7SDI7G4e7qa/osrw7e3PQbSEyhOCE9QlQf1Yv/vunvUliK7YEgDqUhclHNh2s9Yg6x+Axsyd2Ks/IyCksb8ynsirLc5LjUu4UWtPm4MGDKyoqBAIBspjFu4Mj0HcKu3fqxI0t9wp2L8+I18WfjTclE/yx5VtBWLfgjgFh3SNfH5oTt2VL9Qhmw5Qlj1ITjqcmnG33xkczIyICrv2aamF6bKtYehux/iNPPSptauDD70ZOXntDO3R0xcILl9+/EGiwfM6/6qVkxTe+nzKSSt+wdhGqDym6sGP5Be0LqUgTvOM61UrlQGZfOLSbTE3Fb4TexjZ1/fE9U71Fly9cvldz4DWZuntK3z/Z1SvMricYysJBaCQjuYPnru2H34l74fdwKxPzGlw1YbR9MvvMwsEBC6kH81FDZYsvr//+T/3MS/UfWNL0qo11qLbj6jJ+VC3d63rU3TVjJwY32PA5eSij7oYY3rzqc8kIY6f9oQxzzlXz1NfXAAAAAAAAmI2UVzIZNjK50ShZaCcHui3txN8Ff2x56XGx4t3P7ny45u7wvm6B7eycHRh5BfLV2+/f4BsZuMqwYTKY/T4K7qd9XXuUtFyhpLIw0E0VluWVHNxV+k9Pn40Tyk8eLRRYFDlQ0HRRY5pLawYqlkvU03VCySpqjQxNtNC2U7AdEpSmGa5pmbLMoj2ZRQw7ZlCwc9/+rVF0rjYRtiGmO8IKgYGBn3766YcffqhQGIh7y2Sy1atXf//99+fOncvIyECNRYlD9WZ/0Mk4iAYdRL1WojXDzKqvVCALWZyzg0JTD0Sv0Rc0hi11u6ZGEY0atV7ztfr0VFnei6Q44fDZe+NmBCJ1Iui+/icy+OzOnYnss2IyoG51guPP0Y3bksnqe4pUdWWp1MBwd5IUF8u0qTU4HBZR9/MwmxfWdfDYjz4ZxJVlnNm5bt2Gc1WfQC3aEj0sTueegwZ5VzfTmQuJJYEG3SUkMoSRcnDrwTtUPFe+1QMAABAASURBVJTVbmRAQICVbSkVCqWyMCP++B8PGhLJDg8PVyqV58+fR/WsDG+9djSv+tmBoaLTexPKLd8dmToLR3BoQLm7u+JBVfzZ9JGRie4k/HEnQZ1lefa8yO4+ZwV3jESgWf5RE6McEw4eV7cjKxTkl3e3Y5sYh4yPooLB0IaO6XQGHSlkCu1Ol1DfTamaZVfP91Q0B0lXH+H6uHHj1c058gTbuy0XkfcyqJGdiCwWiYoR4R3g5Piv4XLm5eLiYsTictkEwuE9JzzBwuFHva9CsViazLjqvL+kjJRRT42bOv4V2Z/f70kQkXrl6l/F9459s3BPjbgc13A77IB+vQJZ93bPmbwwQYqooOHgV6oexSAVZUiNhk/rbpKmODBqQiAyi2YhXT5fdvD4ueODs//8/hDeIeOrNtE+ETx+xdxXUMp33+y+oQ3dkkYObM1VEyz9SwQDqzbWoczLhnfhT2TiqJo4eiYPeO2jZ2TXjJwYxnaBUD//wPDRMHYuGWF0FezgwQbPVROHwtS5oa5dt68BAAAAAACwEA5A27FsZXKjn/8YtjYlT/Bc2v99m7Fqtu/oKM5vMeI/4h/bETYSaT2Dkcseitd8U+xAfdCkuXZwn92fypjMaO285vO2HteyPj0h79LftS2S/51XYbCwehtaO80Y41h6LfNopgXDn/GH2jxk27Ytk/FYzvR2mdCfeT067/oTZZ7Ctq2nutDTzp1Rcf2JCpVXFCps/b0ZjDw508Oxbyjr+sNSZLCmZagnEzJzS/97LP8vtSTA39WBYWpEbCs7W9wdqPHMnDlTLBYXFBT06tXLYIXc3NzHjx+/9957ixcvRo0FxxLqD0Crsz9XP3WQScU8y1D9FBbHkCwKQKu0g6BLSm0/mKJ6JZwKJWtTc6hKylW3suQv+Vbfk7j1QFHjjoFKRfsrxiYhHpU90WvQXNKk335NeGc1lc2C1fOtEWHHxSgAZeD4M7I29GZAvR1T+9GAmkhxz2Ki74hBAdLbZ878uve3K40x/kkmvp1w9mxVvmmis/c7MhQAMWiAKZXScuTo1dHL8c6dErpLQGg7dWgUUQHYNu3c2Qy6q5cd3c7VJ6AjQ6mQ5j8wEUNSFt65L40MGxgpOH45o9wrcvLkiPLjm/YmS9RvJeXSwnK7Tt1Dg5UiJVIopKIH6ifu1VVRUVFf9JnK5/wgo3Bo90FRd44liOw6DRzY3Ut0sFxpfHdMUEegQ0MiuzEUGUeqxj8bb8ox+J0Fk71Sdm2NxiFlO1euHd43E6OtlYXldJ+BI0eKjp9LybcLiIwKsCuMv6/ddxxSLlHYuXfs1JFRjqjj+0iiLMm5X+LYPSoqWJogYodFhbpKU+5rBpIrS/LzFa6hAyPvHE+SuoZFdXKla241G+msR+oewfUzTieJ7EIG9fRSZsQaTxdizpEnRamp92S9otZu3hxw7CF31PhR7ij/RqqoxGh58eWM4iFRKzZv9j6Wyh3y/ih32b879IeaBo5fuxkdv8cePD7KCd3LuCciSa5Tz/EzowZzWesvoJ5T3o9ykv2bkCqSilIv4KZ6TZk7pfiMiDt47ooJIdk/jhi0PMNwO1KpCN/ue6XX1PH9pAlEv4VTu7KQee+ndZtK3THYe4duNrvn+r9PTFVPEt79pswcHEgQ3K74th7xyvtr1w8WpR7bcUyzqXO/38FVtzPhFfeHBy9/v8fYUTXWvgYRMH753F7Evd1rdyRIqzvC4IGVFmffyJYNeWXu95vZxx+2HTz+FRYqtqpDiw3uwqHs+o5q3Q41tm7jR8/wOWP8xDC4C1TyCyNHgzR2LiVILTpKJEkY3CQSBRo9FCKT54ahvgYAAAAAAMBShcVKZwe6RGr0g2r6/SeerYnWzvT0++W7j+e90tkBFy5/3weX/3oq33TjqFyelq590JwLw3UGogLQisfFOw8WrZjsf7APopJUnM86m61SIAOF2kbo9NfGtOmuKPr6z1IJsoRS/s/l0jF9PD/tjph0lSAh7yZ15Sz/51rpBFxIhWSVgstiTeG1ayVtcSGV60CZfU3MN1oTIbtWUya7ax9I6Oe1uieSZ+dvPG8w0liRp2BNGOPSt7gCtbKVPyw4mGcqIIk7orikMb9ujj+2jxw58vjx4ybqFBcXx8bW97wqi5Q/Qfb29dQpTEcZJaj7VLSiNUoj0LCBCN1H/PvInMYtZDLQUxVf1oxZ1k8DnXVf9eY4bQQZz6WS1KiW7y3eMsu1LYc6jx+KKpbvKVbPqhryrFK1bUc7cL9G3JmqYF4YmhScOXzxo56DqJFzwSPGDcq4Td4+LMYf/A3VFQvEMhSojtey6vtmrV5lgk3UrUwQHCdt5FeUXSdFhzpS/Bv/bJKIe3rT4Pe/Gjxu7OZ3p6+7IrZiSwAwS8md06dTpo2dubpnebmyPCctR6pUD5hl4QDyR5Hu2lruQ6d3wv/JOb1+S4rxtmSC03uP200eOXPJUPxKev+vg0e00Wdq5oP42OSAsaOmh1CvcKj3yx8TJIbehK9fv47qJ3sQe+C46+SR0xe+Tq0rQ70uPGVkd0y3hSPQ5ZGRPoXXzt2vjs4aOzKoJCM+Pmfm0JmrNTcby+/H7Y3PMRGAllw7+LPLhIljZy4ZS23q/bgDe+Me6epL0uKu5U9/ffJMajfy/9r07R8PlA/O7d2LRo6avPB1Bt6zuIN7z+rye5TciT13x2fs0JmdhiJFTkpGiVL9nmWsszbFantk+kKqRwrTTh84bSLzh1lHXpqw5v05xOa1U0d9/Ar1Ov/yjwuXn8kmyWwj5WjPgjltv10/E5ePwn8GU3YvXFhjZOe9y6lOI1d87I5nHVyw8Bsq6iY9tnZ5r7brR63YrF7izzUL1/xILSI9NGdO4Ob1M7/YOQEhTf3vcbmT4XZI4tD6H/t9//GoLw7jZh7G/pkqCzRvALOBTTICh1Cnzpxa1ap6CLPs8r1Dh3bgTfXevPbjITNDNEfju4XrL1iXtYMIGLViYRQOUi78/rJeC2SGkQN7A094r1+OOyKk+N+DF1KCR7U11bzRDkUGdwEX13NUG+PoGdk1YyeGkV2g9s7I0SAzDJ9Llh8lw5vENX4o1Ks2cm4Y6WsAAAAAAAAslCOSd1PHlI3BEeq/EiVzJ/JWbc86e7nwXMLjtwZwO7SzW7vjPrKEJPnBmA+004KEh1Ov5Xh70uUFZL42LYfKUKGaUvn3j/y/TTauyC7cpn7Y+bmT6svjv3I0D90ryy7a82uRPZuOnijLdJ+tyzKLfsosqtVCWXbxnl+L7dm2SFpRNRLXYE0cA93zY1bdbTh6KKeqwsFD2jipJF28LR2ZycnRNi3L4gCrCefOnbP+m+tWK5EiN049dRQP0MalaP4S9NpE9BpCpelo4yr0X31PIMSKi5CFaHR6nTwq+oHmqscPaiZsbKj8GzZ42qZy9Zc2X69FCoW6kKb7QbpU0brQs+anshIRzMoFS2xWLqOmqcJK3URVFLtmYFqDHfbOZN6VnSepYcWcPpv+2D9OkztUlPDFu9O3JEkRu8eq09HvU5+HZTe+GDZ6i3rUcHUhKv578dB3f609KpngjfhkRPHOrRfF+pVlqZvHDl2XVLMuZ9D2mF9GUp9NRcenvT7vnFi9JV//sX8ytSWyhM+GTdzJJwn/d3459Y36OYk11mjRltRtVlep84x9p9XDv1H23glvLLkoRqDhfHzaNiS9jlhMdQOHwzFRYs5SVqI7crl25SJRo9yWo7NcuGxUKJJY8Zg9i1HrUhbW2vBG3J3GawofFte6m2py1S525RID1VkubdxdkZQaLY2eGoIbHOyNsuvkzTVVzi2+l2ow+S/hHRCIRLXmEdyAQG9cmlF7CK16FbLsujMMtYNb6RrcFhfeMJHh19xNshhee7A3K/teqqhh7ZhchcEDi9fsTYgyzN9+4x1nYBfqO6qNdfSM7ZqJE8PALpg4GsbPJeObZGAVRjfJxKFohnMDAAAAAAC8yF4LZec/lheXGs1u4eJou3auXyuWjUSqdHNmlMkqN/768O795vgc/+JwdrB1d2NeSmrCi/4pU6akpqbSaLROnTr9+uuvqInY2qLOL1ExW3O4tEOuciTINasyDuem3LQ0wbIZKTiq82xoknCoI8tIRTtyqHLu/9l8+yWqRLr9UQ+Fpqm0Nati0FSgubJy7gLa4UPq7VNpZ+mvwhzipL3Hb4+Y0xnHYWXZF//OMDH06fbZvzPeD6RuLzgF9Ahg/5pRK2JLeHcO4CURtSqzvIP9OUSSUP/zKDugR2fNyKjsv08kiY194iXFt1OFSB2AdurcozPntwxNKxZtCQDmU5aIHjXaM/GUMsmjZvubJZMYSCnRiLvTeE0pDW6qyVVLDK8ZH98Hln1HqQmQOPgoaoRyzczsjFQDS2SkiixZtcF2cCsJF6y4M2RwkyxvRZRxo4lHsho5GnjNlu218Y4zsAv1HdXGOnrGds3iE8PY0TB5WjbCJpk4FM1wbgAAAAAAgBfZnawnXYMcbt4pVSGawQqSkoqPv7oX/hLby53IeFhu9JGDwFo0msq/rd3VW40WbDHI2dn57NmzeGLlypWo6VRUoMLH9Q+C1pA8QObHLHCzlj/ez7xAeDVVVVYNWsp/KC9X1X+Qdiwz9aMZ7KzSm9AMc65UDXwDCR/S+Cl6STnM3FaCxa6Kzkpvn/g1icoGWZx0+GyGqbsR0qRftxxXD/tH3j3e6surFeDldB7Y07sqIwauvEFT2SlsRF/vGnXZYcP7qscvZx9f9+3fJgYeS0W3dU/p4gZ0rm7Eoi0Bz5PHj6lnpvbo0cP8RSIiIqoWBAAAAAAAAAAAANAoKFLmiOT+bVuZqKOsQP8kSw+fFUP0uSkEtrPLziMLpU371eXvvvsuPDw8NDR027ZtqEnlPaKiso0LN4ibtVx9AWj9/Biq6uizJoeGzS8/qToGUTHoykoTPzj6rPIPsNmziwpV125ELwWHIQSb0zkggKML0JIZf+/9W4REVw5f0Q1TJnRPpqdUT5EZJ7/4bGcqNXqRO3jZqrc6V8d4Cd7ABctGdKaivoSu8jltZae+cz4ZHlBVlx02ec4IHH/OPrPyg89O6o+MrqpSlTVanHElQztY0r9rcNUmW7YldZut8xqeRPisuHTpEv598uRJsY6mXGzc0aNHcYX4+HgEAAAAAAAAAAAAoOe24AmNhtp5wjDFp8CnDUulouEuQE1PIBAIhULU1JRK9Lixc/iKRVSzlrO1sbE1UFwrDTTSSwatflH9KzFB9VqEauAQ2o2rSKHUDZHWDYJmMSs/WYKUCpsft+lFn1XaaWN0s9hh76zbsHRcRN++PQNclVn/3RaTFdLCMlcf2qW9J/jSCoLX591lCz54qytXnUmE3qZjBx/XsvT/0gupSHGFNOPiiT9uI9/OLwd3HzyoG7uMZLXpEDZowrT+3Etb1p1VeqP//kmXanLrVFfuPXjiyJeJ+3fuy7g9Pvrmi3H2t/b6EKyrAAAQAElEQVSu/vCjb87d152BnLB3Pl320bjqlQZ40qUZ/wnEhaJCdueeXb3tEd277xu9A+iP/rt1n2rfrC0pDJhosNlCuv+gD5cumNHfV/PsSif/jj6uKPv2rdzm+CfRsjk7OxUWFiJrXb161cPDg8vltmrVysxFRCLR6dOnV65cWVZWhgAAAAAAAAAAAAD0iB7Lg/ztnRxtC4sVxnJxgMZlY6Pq6NvK3s72yk2psgK1KGWliO2EGAzUKHBrD+8jqxh6CCGqGYBGNWPQ2mn9Bw/SVMEvq94ap3J0ouHtuH+fquDjo2rrQyspph06qMu8oRd9RsjU8GfLM4mYRvDCegRz1COHyeLs20m3xWT9lUmZSJSRIRBKLXkIFrU8p3NYZw6ZnZQkkDZsS0BTa+BDCAEAAAAAAAAAAAAal60N6hbs6OxIz8wuLyptYQHRZ46zg62ft11xifJaaklFY+ereCbg6HNgR8RkogYiZehuOqqwMj+JkQA0MjIIGumHoasC0JpZNBXXHbXzUbXzo2o9yEQP7tNE+fppo7Wpn+uGnvUjzo0dfQbAGAhAAwAAAAAAAAAA4Bnk4cYMbMui29CKyypKypSkolIur6xUwZjohrKxUTEZNiyGjYM93cneVlmpyngoyy2QoxaMZYcCOyBbW2Q1pRLdvYPk1g+jNS8AjQzFoJFmHDTSBaORfmoO3SMG1aHn6hi03thnhJpn+DMAxkAAGgAAAAAAAAAAAM8sh1a2nm5MjivDjrBhMW3odAhAN5RSqZLJK8tlFaJCBY47l5W3yGHPdeDos18AsndAViiRovuZqKJBg/GNB6BRfTFohPSGQiPd75q00WdUPfAZIYg+g2cEBKABAAAAAAAAAAAAwAvBtTXy9LIgJbRCgfIeoccFqMHopmbicLB+DFrzstZv9QwqxEy9NBSBroopQ/QZAAAAAAAAAAAAAAAAml/hY1QkQe6eyI1TT0aOigpUIEb5uaiycUaI0y2rXiPubGC24UX0J2q9BAAAAAAAAAAAAAAAANDUcEA5N4ca1+zIRs4uVHpoOp36QepEz/hHVk4FqUukjRu5rS8ArVlZ3XHQyOwIssGIM4x9BgAAAAAAAAAAAAAAgGaGI7HSYuqnuVg4AlpDPypdNW0iiGwi9AwAAAAAAAAAAAAAAACghTIvAF13HDQyFIY2pxFzCgEAAAAAAAAAAAAAAAA8/ywZAV3rmYRVhRp1Z9WqYNEsAAAAAAAAAAAAAAAAAM85qx5CaGyWpU0BAAAAAAAAAAAAAAAAaLkszwFtMB2HFS0AAAAAAAAAAAAAAAAAaNGsegghsjYMDaFnAAAAAAAAAAAAAAAAeGFYG4DWqBVQNpEhGgAAAAAAAAAAAAAAAMALpmEB6Fog3AwAAAAAAAAAAAAAAABAxwYBAAAAAAAAAAAAAAAAAE0AAtAAAAAAAAAAAAAAAAAAmkSjpuAA4HkTEBCAAAAAAAAAAAAAAAAATQMC0OCFlpOThwAAAAAAAAAAgGahfXgWDWn/oz9BU7+gfle9pFG/aajGBNLV1C5KQ6Cl0n/WmnZahf+nnlbpTainNROampqX2l9VE3CygKcGAtAAAAAAAAAAAAAATc5w9LlG3FkXeq5+SauuQKPVrK/XCEL6TYPnmarmpC6mrP9bPwCNf2hVMWia+qVmKd20ivq/ekJdAOcIeBogAA0AAAAAAAAAAADQLAxEn40Enev+1BgZjWpGn2l6jYPnmarGf3RDm1Htkc61fpDuh6ZbVB2CrhuDBuCpgAA0AAAAAAAAAAAAQNPSz6ZgOPqs/bGpE3rWL0G6XBy1BkFD7LmFUdUZ/qzLrVEdd66sE4mu1Asxq6i4c3UMWlcKg6DB0wABaAAAAAAAAAAAAICmR9P/j27Mcq1As41exNnGRi8AjahZiGYkF4dmgCtoCWj60WJUJ/NGZVUYWp1ko7KyOvpcaaOONFfqWtLl5dANh4ZB0OBpgQA0AAAAAAAAAAAAQBPSG/6slz2j1jDnqtCzTdVvTSGippG2XIUMpYSunQwaPMdUdVM/q7QJntUDmCt1g51tqWA0PgE0MWgcdrapCkNX6renHgqt0ibigEHQ4GmAADQAAAAAAAAAAABAE6PVnK6R8blm9FkbesY/SDuN487ViThsqnNxVMedIQDdglQHoFF16mcVpg4002xo1IQNFWvGwehKW3VoWh1xrqSC0MhGLwatGfqsHQqtBoOgwdMAAWgAAAAAAAAAAACApmJg+HPVKGZUK/+Gjd6PJjBto6LZ6I2G1gtA66fjQAgGtbYcKr0UHJq0G9qcG5qRzupIdGUlTaU5fyqpU6JqxLMmBo0LNZk8NDmgtecbDIIGTw0EoAEAAAAAAAAAAACaUu3hz0jviYK6yHKN6LP2B0efKyL6qYJfUnUMqmzfCbV2Q+BFViC2uZtGu5NGu33LNv4Cjcq/QauZcEMdg8ZnVKUmDK2qHvMMg6DB0wMBaAAAAAAAAAAAAICmVz38WX/sM02XcEP3Y4t/2+LQs8q7rWLVN6qXuiAANNw4lW4c1DMCT1bcuslYuYiW/ZBGq5OAhRoAXakdYq8fa6apIPQMngpbGxtbBMALydnZqaSkFAEAAAAAAAAAAE3K4IMHq3M9a35s1aFnHICmos8Vo95SfLMFeXsjAAxy96gYNppW9JiWnkarSqhRlT+6Wq2XuqzhkIIDNCMIQIMXFwSgAQAAAAAAAAA0qaoEvNXPDNR/6mD1qGdbdQCaRo19trGtGDNBuXQVYjIQACYwGZUR/WiFj2lpt9Vnme5sq84iXfVbM6UbK63OwgExaNBsbBAAAAAAAAAAAAAAaGrVTw5ENVJwaIdCI+1TB9u2U85dhAAwDz5b8DlT6yyqPruqbnugOpk6AGguEIAGAAAAAAAAAAAAaFK0mv+l1cjFQcWgtQ8hrLSxVXz+NWplhwAwUys7xedf4TNHN6C+ztmlOe2qo88QhwbNDQLQAAAAAAAAAADAi8jLywOBpqQy/MA3mhfPQ/ckQnUiDs2YaJoN9eDB4C7w1EFgKdVLodSZQ1MPgq59XiEe19Vg0Fn1YjyQEN7ongUQgAYAWIVmy2Aw6PAWAgAAAAAAAAD10uTcQNo0COrAH01vHLSNNlxoY1MJ0WdgFerM0Wbe0J1ONN0ph2qfgQA0M4geAQCsQW/lxOGwWfAQUwAAAAAAAAAwgVZzulb2Z4R0w1RpmuGrqpCXEACWo84c9SD6qjOKKq06zbSZoPUWgDA0aEYQgAYAWIHOasVA8nKZAgEAAAAAAAAAZmtr+8YbQ/CPjQ2EGgyh1ZlASC9hgjYTdGXnlxF4vsnQ9UNo+1n8Xyv98wM6cNHSxakzp0b2Z10MWsPg6QdAc6EjAEDzIBx5/v48NhIL+AKxHD3PaAwcf1aRRaQSWYXtFRrEEfNvCklH/9AgQpDM1xwQ6hAF8dhSsUBQ4xARbv7+/hy2VMgXCKWNfejYfqGh/mxSkJycKSUR2//VUH8Cv0oUlKCGITidwoPYYr5u7wzUwLsfyiMFick5JGoO9W8SYnKCwkN5RHUBKUxOTBOTxirjHWBr6kkb46A9DRbtchMyo3cAAAAA0Gjatm07c+aMV17pymQSYrG4qvzKlcSdO38qLS2tZ3nNtT2+bOSbvmxoGddL9XNwcBg//q333puuVFIfEVasWPbTTz8fOvSbqSOpvhj2Z6svw/CVfnKasMaRdItcuWPL25zEVVM+2p9p+aVZvUe+ge1bqs640+qgM6r9vDgPT2QmuRytXIiKJGj2JyjY/LC1DN29iUT60U0WCumCnFgIFN9Bd2WoPT4ayEr5F9Hs8ehCPuq3Hb1bVVqE7t5HJAsFdkQ1DrMMPbyDiuuUiy6ijz5ESyPRz7tRlA8yEz5zaDTDP1p4QmVo2ixcLkckEqPmZW9vX1ZWhp4xHTp0qKysvHfvnhl1bdkePI69/pfHK8rEwjxpBXrBQAAagEbz1ltjJRLJ+fN/1Z3FDn13y87P+nA1r8jb++bMWHVe2OwRrkZCY9rbMSrlJaSV75ic0Hkb1rG3jZtzihiwcsOHwqXjl8ZJOZHzdm75MEz7Z77qEDF5Az7bueXtzto/xtIr297/aOPVRgwOsv3HrNv5YWcy8fNxU3YJOANWbv5fH07GvvEjl16VooZg8iI/3fK/oLj3hnwUU2Bk3aHTN+wZI1w9ePIvguY4GczYJII3YPHmL/uwq0uK4/5v8PvRQkMhUYITPn/z1oEczavb20aN++pmww7a02DRLjchM3oHAAAAAI1n0aIFMpksNZXv5dVm06bvNYU4SjN79qzIyD0TJ77z5MkTY8vWvLYXXvxywSfbrxqOyrSM6yWTPD09cNx5/Phxd+7cWbly1blzMbhw4MABM2ZMnz9/3sGDh37+eVdubp6BJdUXw5O8q15Lbx9Z/cmqo/yqA0SwnVg4Pk0gK5hz5BvSfkNUp+LVvTYcKzTDhrXo+hXUMxJFdUPj3kH/twz5+JmxWB5aOghdKNYrcUI/3URv+qDmkbIbrTqO5v2AXmuaR8M1pP1/PkfvJaIjN9Frzsga+NhORRec0ZazaKIul/c/X6FJS5D2/HNHXxxHH4ZTk3d3o3feRdoYZju04Th6V7fIm4dQ8Ej03lQ0+wN08jhqb/a9gdrnUs07HzQVsuqpg3Q6ffPm7wiCmDbtPdS8+vd/XaFQ/PnnGdWz9MBE/IcDb45ZAWhbtn/vYX14+tFXpfCv/b+nSJonAk14vDKwj0/Z9XMXBSVPN+YN34sBoHG8++6UNWtWiUQiA/OITmMWf9qHLTiyZPygEXO2XZF2nvTZrHA39JyyYdgRthVkubXxZybHn8eWCgRSOcEJ4iDhbaEUsYOmL54WhpL3/Z/6EF3Eh+hT6hDh68aVb3eWJm6bPWrQWwv23SZ6TPtsepAjalQkKRWR/n3C/dmc0D7+KFvUwj4UWE4U9+Xs9997T/3z0ddxxgbkkuLEjXNwndmfn8pGz+vtFC0zdxkAAAAALUWnTh3//vuiUCgsLCxM1LlyJfHdd6eXl8sOHNhnZ2dneEnCb9jieX1Q3OdvRXXtOWT2PjJ8/mfTQ41coLak6yVDQkKC//471t3dfeLESaNHv6WJPmN4YsyYcbjQw8MjNvZ8UFAnYy3IMqKX4Muw2Qu+PMLnjP1iy/xXdeMCCuKWvt627cuT96dZc+DqP/INa996NePLtOrHwamQ5QHoe+mo/xC0ej1KTEMlJahHEPr8U2T83kkN3uPQkb/RSc3PWRTVNLFgg4pvosuJNYdgP1ftm3D3EIrNQ5/tro4+FyeipUuQ0wh0JA3FHUO9ZOjrxdQgaxyqxhOycehcLkpLRhNY6OvP0UO9bW4/Hv20Cckuoj9vIvOpTyFV1VlVKwuHtsgyLBZr797d+F/xwoWfomaH30y4XM6IEcNtbZ/nJ1CV3b/0x0mdU5ceNN/4Z1t7V44nx7XV0x9/DCOgAWgE778/Y8GCar9/GwAAEABJREFU/5s0acp//90yMJvN68wjihN3bYu+KiCR8Cue/8pIhO8e4usiwit82NvDB4YGcUghP/HikehTyQUku8u0DZ8NlEbvS/IfPjyIECbv27Y9RlDCCV+0YXGocNuCVTHqjA2cVxdv+DRUsP2jr85TI4INNkWtvdOwt98e2CPIn4PE/MSTR/afSmxQwgcbwo5lWyF7oqhEFiN4EW9PH9YnMohNoOkr1yNeuD+H7DNp2L3DyJ9DZMds3xhNDR4RbgsdED4Gh6kdhWwkTD53bvW2U2lSxN/284Bh/wun8pgkN+ZXFwmEw+E4Ah0aJA4PQjgyHsTTzvCKfPvDSQODOAQpFsQd2bYrRiA3VY6ohB4D8Kw+PFIQcy7bzNVzQsesmD88iC1OPrJt+yl+ielVG+plx/DFmxcHCY6cI8MGhvKQ8OK+7ftjMqXWbRKBZFJBctz5xPrj8HIx/2oMH7FDQ2fVvbozekIaPr1N7XVjn8MN2GX15oS+u2FxuFhA8njklSNxTgPHBJGJP2/cFScN+nDDZ33E2z9Rf7+BE7loy/yg5K8WfMXnGd1lY71j6hxr4qMBAAAAvBg0Y+mysrLmz/946NA3NIUVFRXDh4+cOnUajrasWrVy0aLFBpZkczpz2DJhYmJyJr4Ij/n5641kqHb4s6HrH2PXS6au7ZHll3xPCZvNxsEpExmf8axWrVq5uroabQJf0MScp74OGCfkhh56OzySR/CJad+uG+tPjUwmxXEbF3ylOUR6l5EDBwaxpfVcPBu/UnUM/dBQ+8iqK1Xr1I0BVj0mzqL4YNWYUF9/9Mtv6A4fzZuBugWiVevRmIn1LOvUBfXqUyPtQ/5F9MnnqO089NlIqvyfr9DXF9EHP6A3fKho6YFNVCRUxkLtB6GPpyJ3zZJV5c7otfHo3ZFU5grZHfTJPBS4GOE7Ndj1TWh1IvrsB9TNmWpz9XEqzQVZjFaNRD/gRjzQpz+ow99F6I9D6M+zKJ+FQvqgCeNRe2cqQ8UvU9E/XdAbLPTHRYR80Lvz0Gs+RnfKWPu9ioxuEibLQwe/QrH30SsjEVe/OWN7bYwM/XsWoS4oqoteWRFqOxAN+QpFdUSoI/pgJHrnIsqWobZFSIRn9UEhHojlQc39/T7KR6itXnvUXBb6E/dCODJ3DLTuFKp7J8PilBsUHLc4efKYk5PTypWrAtVwoVKpfPDgvljcVF/ctLdv5eTkXPXGcunSP/369Z0wYfzBg4fwuzR6HpHSvAeZ+l+Ct2X7vTawh6c06dxfaZIKW7Z/r4E9uNKk2L8ExEsDIwNI/n+PXAICuASZe/v69buaAVK2ju1e6vZyAKeVbcUTyf3b15IF1ChqJu+1Ia9xCm9nVLQJ8GQjadat6ykCCYk0bfq0asVmIzq7x6hJYUpU8UR47dzFuyUVto68Di91CPDktFJKxcL7t/npeU8qjDbVOCAADUBD4ejzokUL8HXqtWvXDNcgEKG+utH8u5Um/zBj5A/qScfQ+Zv3zgqSJiUmi4mgYZ8OHxZOjHx/v5QdEBTag+MfFC7ki9mhY8P7hPNmj1sQI+STvA8HjA3fFneUCm8FDRsW7i+8KJSSxpsSsCMXb946iZd9JS5ZQPhHfvi/AaHscVN28a2+WrJltSJslOVlciviz5qjweZwCKmAiplzODiElkxtv+YQkVLtWxupPlYEIRec/mTc6aolOQE8QiYWihv9MpuQ8hOlA4aNHc5B/Dipf6i60C1y8Y5fpwfJspOTxbzIsZ8ODPd/b9yyGCHbSLlcs8hPk/ypWcTb8yM5TmaMc2H5j5k/XSiUskOHf9gnlEOaWgVhpJcJDi8orE94UKiYzxfjePaSPuHe741aSmVysHiT1F9BZPsPWzRpYCgVE/9Zd1lvGWMnpByfAAZP71Pqvd45nSe8kojLgwZ8+lP1AW/cc7ihu0yw/YNCI6XCXcnst+ev5EWfEnLGzFssTk7+mcC7FiTkEFXVwkKlHGR6lw31jpvJc6xpjwYAAADwQjl+/MS9e/ccHauTcWVmZuFL0V9/3TdnzkeGl5GKbwulk/pMW/x24ke7bkoF57evOq+eYfz6x2AzRq/tHUMXW3rJ99Rcvpwwe/ac2bNnnTp1An8a2rVr959/nsHlb7wxZPr0d1955ZXU1Nu4wj//XK63Kbx7PDYiBUIS6ZJi4Mv/AI7u2qrWNRUR1KfGxbOhy8j6LpBqtY+Q5VeqFl2D0Wq/qgo6a/9La+jT4ToGobOX0eFf0ZKP0a7t6NdjqLUl37t1D0dRLLR0HuoVjl67g5Z+jlifq6O9RWjTSLT6PhoyCLnjMPE89M8ddGoTctKUX0WBA9ErMvTDKPT7THTkB8QqQikXUfFUbbNS9Xjkej7DydD2kWhZIuo1ErWVoYMfot8volOHqOmUm+jYcXS5I3rFA/3zHTp2EZ28aHF+DNLEJhWhH3R7IfsBZaszNWvKq/bO+z764UPdXptc0b08xPJBXL1osfsgtG9Q9W4+vI8ID6oCrjYkHH39A7o8EgXfQT9cRCGLa6faYDmjts7o3/vUpwTzE3RXnVraZC+GgtFmR6Pxv+KOHTvm5DyaNq06oTWTyQgKCrp169acOfNyc3NR43F0dBwyZJC7u7tIJKqoqI45yGSkm5ubp6enUChET4+Xl5eHh8eNGzeqSrp27ZqXl5eTk4MsVCEVpmcpO/d+rXd23jmhS4/Xwjwqkq7dx7Hodq4cT14rVw5PKi6z5fh08/G0rzgSK5AS7V4b/mYYRynNzStjtwt6zZ/nepIqp7diczx9eBzPJ2Jxmb1HUG8fntPJQ7GmsnwyPXoMGdWNQ+YK857QOR1e69CBZ3vwVIrEWFPmfamiPhCABqBBVqxY+t577508eaqbmv6suLi4pKRkUwvjm4nZifs/3/Tz/nghyfR/e8/xL4PC/Nn7NQuJYz4auTBOjC9ADx2eFdrHn30qMflcsnhg6IBQzimhkPAfGM4h+T8nCkgTTQnZ/v4clBH9yYzliVLNU8444oY8NoDObMWkKcpkCqvyL5HC+P3b2GGRQYJtqz+JY0/bG8nhb1r11VXSf7R6PmfAhr8Wh/I3bjTwR4XgRU4f5k8mfn2k3uHPbL/IyFDdlSQp5sfFmQ6hqo9eMvnFpEjpua8EKEizLUEDBwTJbm8fN+6bZCkzaNqh459HDg9ix5BGyoUF1CKR/rpZjuErj/02nY3qJY1bOg53tBmrECPDvSxQtyMT7Jox/qvEEnboosOHP4wcGMqJOS+2ZpMIVsCwWZOSBVJO+NgP+4RrLustjG8aOyEFug9IdU9vaq/9yYurZ8w4gM9p3rDvj2/Q7LXl57ClJ4A1uyxOPrl/n3/ogLE4YB1HRg4bxuOwmSYvqw3ussHe4Rg/x4jG/hcNAAAAvKiqAjK3b/PrzlWpVEa/7k1mntq4aWDQZ30+P5a6WJgUs3/jxl1x1F32+q5/ajUjNnJtT7AtvuRDT427O1cikQwZMrRnzx44PvXDD9twQB8fOj8/v5iY8+PHT0xIuNKrV08Tzy5j+Q+bv86fJHihkZEBTuKLGxOFZAm5febg7YgdufbMzmG1F9BeU+FrpD16F8+GLiOFxkLzJckm2keWXKkKGyP639AECXWMewcNHo4+nIwWz0U7DxitlroEtVminQ7+FJ36inoI4YRN6I8+VGqIy3fQw3B05AMq3lp8B/1+E43ajX4eT1X+5wM09jhK+RyFqMt7bURH5lHh0dgP0KSz6N889JrxbXttMYpZjP6Zh8YeQiuP62WdLkLuI9GWr9BEdXLk30ei2TfRwyL1cGAZIvCWnKXGAqdsQgPmU0OSX+tjWfvF941uUrH+XsjQpj5odZ6B8gMj0UfqvTYV+5YhUmYqVJx/ER1MREN2o0B1nQ+PIxY+mOpnTvb7Em1dXCe6zaLuxshkuGFzH4rY2KfT5cuX33vv/e3bt/7444+7d++tKrezs/v22282bFg/ceIk1HgGDhxQUlJ69OgxzeNMNUJDu/Tu/dqpU6eebvQZKy8v7969m719K83LyMgIHIg/dOhw/Uu6vjR21kvaaemt3w9eePBEnpcSd813VI8er4XnurRni2+d/PcBjvRq2n4i+ONgzIMntpzQUeP7tOvAIQRK6oaZUnz9yJHLeSQuH6Mt13wGVUqSTx75RygnPHqNHdvNJ8CjlSBTKog/Iohv5T9gwnB/6ZVj1VmnbVvRi4W3LiYm33ogrbB1CRk14XVOG1ciRWK4KSTIRI0BAtAANAhBGP3r4uLigkwjCxJP7SfDI4ctXutNILY/zwmHl3Q34GVivnqkb4n4tpBE4Wy2OpHZuWRRZCh1nSnlDQznkfz9iZohFcaaIqUCgRj1eHvvmdBkPj/5Ssy5U3H8BuS3ZbDscPy5uFyBrEVwgnhIfJLK+xzamUMKk/S/hkKKb/MFbL5QWjtISvgPXbfz2+FE3JKv9vPrG1VM8AbM3/BpmK5nbm8blcyv52EvBBIc2biL7Cw8l0xOVz+IhEmwcQRTKlQP1UZysRC/sfuzOWxHI+UEooKDerPwvgiLtcFsU3QdbcYqyEwTJwxeIEN9LKWCUz/vIgIy1HlZLN4kKf/krp8v8o/sP82Xai/rB1pxbW3y3EaGTm/1phKE/4BZK4OoLecFsVmEeq8tPoctPAEaaZfrY2SXDfQOYfwcIxv7XzQAAADwguvevfsvv/zk6FidwbmkpGTKlGmml5Im/zJjJH/M9LcHhoeGD//01yD/9ybju9f1XP/UZuza3vR1lKFLvqcoMDBwz55fzp2L+fHHHThK1a5duxEjhuPw/cmTpx48eNCly8vbtm0ZNGjgxInvGAtAI27o8LGh+HCIbsf9vOrrjdGZpvdI7+IZf6II0l08G7qMRAXWHRwLrlStXUXToyEbGyQpNFXFexz63wfa0eZOPtr4JqsjWvcVGv4u+oFAn13UZagoQsUkunccrVInI354kwqzimTqcoRCOmojrlE/IM1YWBPRXqOc0ZDx6N+LaNNxqs17d6hVaA8uC3F1Y4oDR6J1MsRt1HTVNfaChQJ9EJFnoLxtR0TcbFBe6fyzaOxIRI5HK0dqj9g/X6FNF9GQmYhbhP7chL7rqE1+8ozBN5PeeWfKrl0/lZfLDh/+TVOIQ7GLFy+9ffsWjnvgu1CoMeDArre395YtW/WjzyEhIfgm1u+/H3/q0WessLDwyJHot94aW1ZWhu9UtmrV6siRI2btftn9SxdvaQLASlKSpzm3ybyUS1d83+wT1kEpTjp2/UH1QGNlmegJVaeiTColEYdoRTDphL0tDvAUPlFqyiUkcsXltpp/J3iGOq00KUlPSrZ1LXxiKlNJxRPh3VtKnk/71/o50RHhit/K6ETVLdc6TaFGAgFoABpk+fLPHj7M1qTgMOebZTVwXl25d890f/GVuERB3UtHsm6uBLk4MSZZGhnaJ4gnDqWuUfclar9XYbSpgrhVU97JmDd9eOo32kIAABAASURBVBAvaMCsgWNmTY/5v8lzoq1LWEZj2NkxVHIpaWX82S188bfrxoQHcBFv55+TEJvnzSEX79jCWbYkTlNBmrxr7rhdODS9SH8xTfR5LIe/bcay/WakGiD5uya/sl/vdYkZOTtI/qlvkk/hq8nRRI3PCaSBKVPlhgrqWXP1AvWswvQJU0WaFv3VGs0kYbBhUxtTkLj/m0TtC+1lPceKa+t6N5WsZ5tIYWL0PmkSHy9cYuk5bNkJ0Fi7XC+ju0yi+sr1ajTqv2gAAADghdejR3hq6u2NG7+rKpk//+OePXsIBALTC5LCq/tXXd2PmP5jvj38v2Gzhu2Ki2YvNudSrZqRa3vLL/meIvwJqHfvPu+9N/3QoQO3b9/etWv3999vRuoUHBs3ftupU6f9+w/06hVh4kv6siurB0/+RWD+hZfRi2ddYfVlpLUsuFJtDCqTL61w+Fe0/P9QQAf0w6+mqtXNAV2bkXlt+6CPPVCwhUkwTCu+iSb1QSk+6M0+1EBso1vkg95djJ5d6gHLyFCQGkef3xmJRH3QkU2orXoHqYcTbkIhP6CfplJH+rXxaPZiNKRPzRHWMoufXdrop5NaQsKVt9+e3L9/lH4hvl1XWlrq7c1rrAC0oyObJEmFoka4wdnZ6ejR33Nz89BThf9YpKXdKSoqKigoOHr06Pjx41QqdOjQoYKCx0g9+rBDh/aJiVeNLl8nB3RdFTVfKA2W670yHGImC/j/xCPTWnlFvjkqzOWJ8IGwsExptJo5TVkCAtAANNSOHTvlchLfDxw/fqLhnBukOqUxoQ1sskM/2LAyUrxtwf/EkeH+6PauOTO+uimlLl53RPYINb0u9TgJaWT4sAGkvz/J/0oXf2bzjDdF5sTtWhi3C0/h8s2H/xc5NtL/lMCaZz3TGCwWQ0UWyZXIOlLByf1H/P1n8eI2bosjwz5cOUywf+Oui8mCApKD7+upBxZQF3wEmxrwLZZSYUOC13/llm/H8gQ/z3h/Y6KZg1LlUmlD43Fyda8Rul7TTOAiY+VI0896sxBBmLUms1fhyLP8hLF0kwi3oNAgjpSfyC8gdfWrUnMbJ9XbDwrb2k2V8qM3rjpd+w+zxeewJSeAlbtseB+kJKk72kz1UCWpiZaM9Q5p/BxTz260f9EAAAAAsLGxefz4cWJiYlXJ48eTjCbfUKPGRqybxj637JNdaVIcRBYIxTKCzWW71XP9U/t6CRm5trfiOuop6tw5qFu3V1avXvO//23EEZlVqz5funQxjUaj0xk7d+6cPPldHJ+aNm0qjsvw+WmoURi5eDZ8GUkxcOQtRdazCjOpaiREUKHa0zigZWm4sFZuX81DCLPvo3Wb0Ni3kRVkd9BSHOEdiIbcQZvmoV7HqUHQLBZiEShkKlo5qEblYhYVOZXp4q0Pz6Lf76AhH1ABVpYucYRmgmAh/R6o2xsPL6IUGfr0EPqwI/Xyj/voz0RktbrtE8Y3iVVzL6pGXtctN9hyLW09qAHgD2U1HleYfxG9Mx7dDUdHDqEQXXxZlodEJHrFRxvn9/ZB6CyVdQTpBaBlRehhHnLvaG7+DQ2V7umUVaeTSmWokmVuqOmXODk5OTg45Ofno0aC3y7wP1UGg6Efg7506R/0DGjfPhDHmnEAGk/n54uio4/ig1r1xQ43N7f27U0GoA0iPEJ69+ChXIGQ7f9Sn/D7x+KqBkHb0jXhWrr6D1JFhbJCqVRWaF/ql9e/Fk0VvegvwfbxdkHi5D9P/pNHIluXILYPzxM1PQhAA9AIdu/eiy9e9+3bO2bMWwYuraSCi3zx2Mhps96WnhMTPSZNGxgk/FIsLSHFUpIICgrlcQRk0Jj500Pr/7OiuUodOGDWGIJMXp2oG/ZIGmuK3WXx4UOzOHFfrooWkASvjz8bR8SsfIgfjdmKxagkpTKrHzuLL9AFYip7bsypU4n+nT8khXEnT52nUmoQgit86fDIafPHoItSdo9Jw7xJ/s98MUl0mrbh20md0e0j+5OI0MgBSJ1VJDlRYMVj8Syk7rXhVK+R58TsPtMjucX8K3iTjJVTiwiThNLh4ZpZnD5jg8x7COGw6dOE54TqpmSCJIHU2CpKkOUnjMWbxAmfv+PzIP4+fGOgatX1jeEhpWLcVeHhw4YNY+OqePtvS63YVPVeh0+bPkC4LU4avnLHhmFo/+RRq/j+jXcOG2TNLhtGCpP44ukD3p71tvikmDNwUriTKPGKwETyDyO9Y+Ica8x/0QAAAACwBikWS9lBY2d9JiT3X5ESYWPHdGYJ910RFJBBJq5/6l4vJSdmSg1d25NWfEZ4elxcXFasWN69e/cff9zx008///LL7kGDBuI4yfnzf1VWVnbp8vL778/QpOCwoFFqfEAoj42IMB7BIjidwwcM8JfiI6YelY4vnmdNE58UErUvnuteRiZSHxkMHPlkKc9g+7hHjG2SyVVYoyriXPWietqqMatZArRyITr/J/pwPvokBtnb179I8U10+aIuospCIV2oKOfBeegCQls2UQ8hHDYKrf4B7VuMnNQPAIzdhGJ9UC9ntHok+gWhmItUegpc/sdX6ACLejjh9nno344o6gNqnHKwD/r9B/S7B3LPQz+cRdxBKFAvroobJPLRD5uQ00hEOKtX7YFYJPr3Jir2QXcPUU/ka0gqCgPtG98kwoeawHtH7UUeOpCoXbVmr//YpNu748gpvDp8bBgLvYJj9EvQwYuomy5YL7uPPhmP/kXo4w8QeRP9o64W2IVqP9gJ/fkVek1GPc5x+25EelCPHNT37w/oMok+CLfkYKjqnFF6cxqPnZ3dunVrb91KwdFY1EhwAFosFvfv/3pMzHn9LBzPoJycRxbVx0Ffj3Z+hDaUUlEmFuZJbT1CInH4WXgx9q/7HDR24Eu9XxGI4zV5RuiuHbqFlqVL6T5hPvbKwkeFZAUpuS8u69AurPtLFRllBFVOirPFTyrquytSQRaSyiCPl8Jfwu1VkNLcvMKKMrKCzuF4sFsVKjlBPcI8G3SDzmwQgAagcezatVuhUPr5+RkIQJM5MUvnfLnh2/mfbx6LXxbzjyxdtj+5hESnNm6L3LLks7M3PkP4beckv7izf33rkePoLb94QB8nMulcYtVX1Ui+kaak/CM/nwqfP2zJ1gGaihknV2+My7EmuGaD4882Slk5WYmshy/wqHdYIUk95ZpDpbPVJj/KjF66IGDDF9O/3Ew9wkCUvG+pOtsGm+3NofJBdx77xdax2jZubxs17qubTR5yIzNPraI2aZam10TJP3+iSQBirBwvkrZ/6TLvdZ9Np2ZJky4KixGn3vXIxGL/6Zt/4uITI1lzYiBUYnAV1pwwlm4SmRa9alnnDZ9N+pzqiOLbp7786Ot6056QgpiNG2M2LH77y63qcRa3t48Yt8vyTVUf2HVfzNp6bDpS/zNZtWwjdU3feOew4fVas8uGyXNiVs1ZQn6G/6UPx/2WFP35R1+fwp8kOUZXbbh3SOPnmLSJjwYAAADwwkhLu9O3bx8azcbV1TU8PLyqvHXr1uXlsrZtve/cuWN4SenVjZ8sIPBf8C83ay5aTi5Z9lVMgelLNUPXS98kSw1c2xu9sH8m1U3B8ccffyJ1Co7p0981JwWHAezQ6Rt2jPXWvuJO+mIrvkrL2PXWdCptn0woIPt8+lMPfNUkvvj56uqLZwOXkRQDR35W8iSD7Y9cY3TMrdErVSuoaj8YThcWpFEPv1QZGqxqnKcXFXQuK0M/fkc9e/AKH/n4mbts9mE0turhaU7op5so8CxadQ6N+gW92VGdDHoKeudz9EsfNC8crTuE/m8qGtuJqsuNRFt/oB4JiDyoctlU9NFgqpzoQI28pspZ1AMAWfPQJ4Op8RW9Pkb7PkfueqtuPxJN3I1++A6N/Q6hDuhkInptEPp0HPpkAjqmbmdCF/TvHWQ1A+07G90kHC5ftxst/UC9F+3QKBy8vq+eod67Yt3eeQ9EP/2gzZ5hQshUNGE32v0BCjmO3u2iLipCIvUY4e8mIG2yHwJ9kYg+7IK2Hkezp6L3dEfvix9q5N/AgfhPvqNSdX8QjsynPoVoVWeVqu7wZ+vj0Pjt8fLl+FattI/gu3bt2vvvf4Aa1cmTp/AtqzlzPtK8VCgU+M6WTNaA1NuNRCwu8PX1KS8vNzjX39+voMDk17XtfXq/4aN7oRT+tf8PsX+fHp4V9y9e5Bc8ISWX/gnwGPhSn24Pfr+uriEtrPB9bTjPnsoefTEuJQ9/GJSnX4xxHRjVrc8Q6sFBZblJ52JviesfHUiK06/dDRoY1KHPGx3wYvyT+88J7l655jOkd59JM/vgP2n308Ukp74HmDUGGp3ORAC8kHx82ubkNGsiIYLjF8QhBfwc/eApwfYL8ieE/LSGpxAz3hST7R8UiiO/fL7A2ueV2bZy5jrTnxQ8LpY36p3TmghOpyAcl655iJ4uzSbx+bVjfMbK8dHmBIXifkhONjcsiJtSL3Cz1hf6DK7CqhPG0k1icvz9eUjMFzQoD7J15za11zz8zySzZvKKRjiHTWqcXdYg2F749opQUGLu0TbSOybOsSY+GgAAAEDL17Zt2w8/nNm9ezeCIB49qg6PtmnTBgc7rl+/vn37jw8fPjTRgsEL18a6tm/EzwimeXl5NMpnIgcHh/Hjx82c+T5JyqpScBw69FtpaSlqLJyIdcf3jBGuHjkjWsrjEUKBoGbWNSOXkY3JilWotAFnGvWbRlP/2CAbWhue56O8AupRgba2VT8qWzqi08mEW+a2LilES+eh0hL06eco+GXU1Irvo3wWau9hqBz/o/KpPVBXloeKnWskozAN138oM9BOIzKxSXdv4iABal9njDPeO7xIW7NzXhffRLNHoj8foH7b0b4P6t8Xg0fv9/HovcOIi6Peh2pmha4H0fMlpFTSKpSooqL6p7KS5+IoFBeiShyertQEqdWBaOp3rTwuJtja2nbr1g1PKJXKBw/u45gsahr29q2cnJxt8L8OaqxxjkrV0BBEw9/onJycunV7xcXFcKBWIpFcv/5vcXExarhW7aImjAqSXjx0kk+y2bZSiYSsEWW2beXGsSfF4hKrv5mubYdw4bjYSsUFTxrYkNmaIQBtz+U5o1KRqMjKx5Y1RgsAGND8AejnmQ3BZjvaksWScvh3CAAAAAAAQMvQWAFoDRyf0k/BgRqXLgBt2UMLnzZV1YhnbfRZ/WNj08YLB6DFVNzZBoeebWoEoE9fRK1bI/AcK0J/7Eb3fNAHI60MpsduQike6N3xlmV/fvyYGNqnZgC6EuFpHIB2ZasD0FXRZ1VVnmjzA9DPr8Z9o2taugD0vt9vSporNNw8LE/BYe8bNSLKT51QSF6WL0y5Gp8iMhWQ4nYYPHGQu/Dk1gOpZcgqVraAN3T46+oNlecnnjiZWoQAAFarJKVF8DV/AAAAAAAAgDEVFRWaFBxNQiq8uG+XVMp/jh9/URWM1n86HDU19h64AAAQAElEQVQi1aY6Jlipot27o2rdC4HnmDN6Yx5qiKh5KApZCp856jHOquoxziq9+0CqOhPgGURK7/+XRJLilhd+sSIHtL07z5khTM+SIIYLr+twP3v5TyfTjUeGRUnRu4WMMpGV0WfrW5CXCTMzmS4uvGA/dxcmAyEYtwkAAAAAAAAAADyPyMyY7Wti0HNIP+2zJvZHqzUKVRMrVNFUlSpVpc299IpwCEADi+EzB0ecadokG0jv7NI9kLDWQy4hEv0MqpAI/o0XoBbIqocQylFRyoUzKTgg7Cya8l54By/79ByXsGBumQTxQjq6y7NvXLqUXoQQgxsWHuJiz0TyfOHVJE2QmsHt0NWXKZEw/EI6MiQ3Ei+l68ZPM5zbd40I8XNgyiXpN+KTssqQqRbyJYyOIR3tJSnxl7QjsO25ISGvdvBzQJL0xPgkYZlClH41Nh1xo3h+ZmfhBwAAAAAAAAAAAGhkKnXcWTtNU+c9UIcDq8erqodCV1bS0tMQAJajzhxtkg29VBtVUWdN0mftWYcAaGY2qCEYTHttBml7Xtfeg0dEhLjI5QxejzEThvvaa+swGdyQsPAOXIb2JbdrRNTgqPCOeD4vbMyYQR20FZ1DhgyP6uiCSuVMXr+xU4bpyo20MFjdgkvY8InD1TW54WMmDw5hyktL8eITJw6qWj8AAAAAAAAAAADqgofiNDUjCXZVOcI8XTBQEy6s1CRMoKkqbeJjaYK7CABL0DIzbOL+oumdS6h6KDQSigoNDnh+ERJAI3ijezZYNQKayeRFTZgRjsPOzlymKP5EVhmiHgRZdic++uTdMobX4BkTeH72KKtMlHQpFjmHcTuE11heLkw8eSCpiMHtPXVqsJ8LI71Mgez9OvIU6ScORqeXIXuvsBB3RMWbFaZbQNxXZ0wNw6Hp9CzJnTN7M8tEVJ4OrggXdnRhZJVB0g0AAAAAAAAAAAA8dbpMHNr/qmo8Dk6d/RnRKvE8mydl9OULFXujEYOBADCHQkFf8n825U+oEdDUT52zq3oQtAYMgQbNzaoANJKXivKFkjJ5aVF8ekpVDg25okyO/6PIiY8+aF8mMb409W+DqojkeFL7jsrA/5OXUgU4kp2TlJhjcv3aFqhVIiYOiONlqEHYEVE8F3vEcOYyFPnwRg0AAAAAAAAAAIBnhyYRh0odidbPBI2DhjQaqrSlYtCVNJt76bZbNlTMX4wAMAM+W2wEd9X5N/D5ox7+XFkzC4dKl4IDIs/gKWlgDmjDykQ5Vj1yUBNKVlDpnHn28nxRkcJoxSraODP31REjQiRnonemU8Oip0wNQwAAAAAAAAAAAABPnWbUszYNNK16OCqt5ghoHDuk2eDfNBqNvn83jSSVcxYi+1YIAGNKpPT/fWl76hhNpRv7XGsENKqZCboqBg2RaNC8GpYDuh44juzr28GPx0QODlw/X18e13hiZoVEUmrfsWuwrz3DuUO/iROHd3VhGG+ByfX1wlPOfh3cUVlZmZxhz7VnMtTBawbXz8+dUR2ilkvkyMU3pGN7X9MbAAAAAAAAAAAAANCo9NLs6uLO1T+1HkJYqUuhUIHjibbRB5kTh9NuXEcAGILPDeb4Ybroc4X25KnO/lz1o3fKUbT/eUESQINnhHUpOMzj3OH1iYN8tUOUo8b4IkXW2a0n5IYrl2XFxya5DI6aOC8KB42z4o8mihTIOcRIC/Iyl4jZy8YwkFyUcjJRqFCgS4l3Jgwe83FHRZlEKCpVVK+lKP3SjZDR4cPHhOP4dNbJrQdSrRqdDQAAAAAAAAAAANBAqpqTuuhzZe1aNBsVLSeb+cHkSh8/VWi3yrCulV1eQR6eCLzI8nNtkm/gH1rydZssAa36pkXNH1XNFBw1I9AAND8anc5EzxJ7Z2dUVmTq8YH2wRNnRKHYnw7cQfbMsjK9cDLD3tkeFRVBgBmYx8enLTwLFQAAAAAAAABAk1Jp4n409f+1v9UTNBtqwoZGTdhopm30frTlKu1cTYnmx0avHb2BrDCotQVQqWpMVydxrqzO1qKOO2ujz6qqzBtV0WdVdbl2cD2qbkeXhQNOFtCcmnIEtFXKiorMqKUeFK0oqxWnVpi3MAAAAAAAAAAAAEDzwJE+VVX2AxVNnQka1UgGjdRRQmRDxQ11FZEKR5wr8H9oVKroSioMXVkVfa5Ux69puog20psAzz8VqnluqHQJW7QxaJp2QhNxRrpwc9WzBytrJoBG2uHPVc1C9Bk0u2cuAF2/sqy/DuyVl8E4ZwAAAAAAAAAAADwnNA8grJqukQ8Bhw5xuFkvBk3TRAxtqGAiFW62oeHf6lHSKk22jqqxz9pQIq3qF3i+6WdqVul+qydomoBydZQZVY2GrlFeWScGrarbPgDN6jkMQKMykQiizwAAAAAAAAAAAHg+GBgEraJpX2qpY9BUlJlGRZg1C9hoKmvydagHutIoNULPNZ5yCBHo5x4N1UzBgWqGoaufK1iVkaOy+jmW1Tk3alaG4c/gaXseA9AAAAAAAAAAAAAAzxvtIGiVXv4NWo0YNC7XhKE1UWYcPdTm3FDpsj9XxZ31xj7rsnBAXLGl0Mu/gVD1EObqXBwGA80GQ8+6RqrbBOApgAA0AAAAAAAAAAAAQNPSGwRdFYJWD1nWj0FT5broc/WPLvqMaLVTP1fHnCEFR0tRIwUHMpAMGqnqxJ31flCtgc+1485wmwI8FRCABgAAAAAAAAAAAGgWVYOgVbTaMega46NpuuQbmlgzDRnOvFHr2YMQXGwBVDUna2bhQEgv0IwMBJ31nz2oqhvFBuDpgAA0eKF5eXkgAAAAAAAAAACgWWgHQeuSZtSYqI4sa19SlfUD0MhA3mcY0dqSqYzng9YFoGk0VGe8s6r20GndLzhZwNMCAWjwQsvJyUMAgCaA7+5kZGQgAAAAAAAAQG366TKqpmn1/a5Vs7qJ2i8bjxPbsUe3HmdjY9AzIMDTAz7CA/CcggA0AAAAAAAAAAAAQLNRJ9moTrihTsFBU9XJkKB7VqF2Lk335EKagYizqeCz9YFpgs6QkzJUWYkAAKABIAANAAAAAAAAAAAA0Jz0Y9BIG2XGaoWhaySMVumiz/p1dMOimya9L5NOJ2XlqLICAQBAA0AAGgAAAAAAAAAAAKCZ6WLQqOZQaISMxJp1S6mQXuIOYw+Xa5x0HAxb+pOyJ6gSnl4HAGgQGwQAAAA0F5rJx17AXJgLc2EuzIW5MBfmwlyY+yLNpZ4iR81VVQWRVdpHyemeKacOMqvq/FRSvytVNJXBuZoKlVS76gmDP+bMZbGIykqldcs2/lwAwHMLRkADAABoPiqVCubCXJgLc2EuzIW5MBfmwlyYqzdXE1rVHw2NdCOdkXbR2kOhtUk3tC3TmmqbmQwmSZKoTs2ndawAAM8pCEADAAAAAAAAAAAAPF268HNVAJamV14dlaVVF9JqLtoEmExGSYkUQVAYANAwEIAGAAAAAAAAAAAAeBbohZ/1o760uhWaMO5chclgyg2NgAYAAItAABoAAAAAAAAAAADgmVIz5quq76GC9c23DpPJlMvlCAAAGgYC0AAAAAAAAAAAAADPMpXl8xshJq0bAY0AAKAhIAANAAAAAAAAAAAA0MI0QtiYIJhyOYkgAg0AaBgIQAMAAAAAAAAAAACA2phMAlJwAAAaDgLQAADwHLOxsfH09PDy8lKpVDk5Obm5eSp4QggAAAAAAACgwfBnDZlMplQqEQAANIw1Aej27QPHjx9nZ2eneZmfL9q06Tsmkzlnzkdubq01heXl5QcPHrp3LwMB8Axr06bNypUrXFxc8HRlZWV6+t3Dhw/j6QkTJgQGBuA/t3j68ePHn3++Cp/nqFkxOf48QpwplKJGgfcxMrK3m5ubwbkFBQVxcZckEgkCZqM7+4S95C27d/1WrgxZheXsTC8tKm3A5Zyfn+9bb41lsx3xWYpPV9zLxcXSw4eP3L9/H1mloZvE8ngpzLuEn5xVVH8TLBcXRomkBK5mAQAAAAAAeCbhOA+dbosAAKDBrAlAv/766+3bt8/Ozta9jIqNjaXRbPr27ZOSkqIpxBWioqKsCUDbe3XwY+bfySpS6Ap47XkMUaa2gMENnzAjyj7xwN7YrLL62nIOn7FsdgTjxu5tJ1DUYHRyZ2yOAlmN4czjudsjiVAoKmtAM4bgfezAdVBPlorS7wrr3TPQSPr0iWzbtu2qVWvwNP7Lis/tP/88jQN5u3bt3rJlq1JZgctxhLpv376HDh2uvTDn1cUbPhvAIxAipUL+uZ837YrLIVHjIPzHbDn+hX/c+4M/Oi/WljF5A94eRiTuP5VmRVB6wIDX8Y3r2Ni/Dc595ZUwXAEHLo0tzvLuMeaNTuUJv5+4VdSIAUMH325BrKyktIImCkI6BA4eP9DXkaF7o1MoxUm/H0rIs3J1DgED3+iUe+4MPgZ054A3xg/hSApYXX0don9LyLY8Bu0cOn7Omxz+ns1HM6wLYL/2Wq+BA/tfuvRPYuJVqbSEatLZOTy8+/TpU8+ePXf58hXDi7F4PUf0QPHHEnKVeI/eeKNTtnqPLNokIx3nEDjwzQj6hd3XTB1gGo1GjdF26TZ54UT3lB/XH7wjqzvX9LIwF+bCXJgLc2EuzIW5MBfmwtymn4sD0MbybzytrTITjYZ/bNS/rX8So4qCf1ea3BwmLzQ8iEPolZBifmKy0Lq8JW6RK3dseZuTuGrKR/sz1eEFJicoNJTH1rQsFSQnCkpQYyA4ncKD2GJ+Ml/8LKRYcQtfuWMntePvf7Q/rbHiKuCZYk0A2tHRMSUl9euvv9G8PH36JJvtpJlesmSZZuLTTxc5OTkhy+EA8+xlUXe+WLgtRR2FZfgOnvd5VOa6Bdu0EWl7XkjXrs6SMwdjs+pry57Hs0/Z+Fl61/eXfcnNPPBNkdVhYwav9/xVCyPcUakcOTBLU3avWxud2nhRYueQicuWR7iop0vj1876JrEIgWbBYNBLSkoSExM1L//553L37q/gPzKff76qqg6ugP/uGliYYPN4bGHMpn23ibDh02Zt2YwmT9me3Dh/DEhB9CeTBWxhslhvfbw+b0/iiE/FpEktfz/29PTA0eesrCxvbx6Xy01NvU2S1a3Y27eKiupnfGk6JyjE28VZ+ZKvw63kxjs76S5B3Xo5lPDTCkqRxRgMRs+ePeh06k3MxcXl0qVLdUepy3KTY/+4R3f0jXojpDTuz6timUzcgAA63c6zjWe5HULUIShNOrE3N7eI7szjqDfC4maLUqK357JK86yLPrdr1w7fM9iyZZtmryMjI/B5Gx9/6ezZmP/+u/XhhzMfPhRW3SasuRcsvBdKlnqT6Y6ctp4S7R6Zv0lGOo6OJEm/787NMz2AWns1KUk+uCnHTvpIZnCu6WVhLsyFuTAX5sJcmAtzYS7MhblNP5fBMBqAflpbZQ4cc7a1bYSB2zSaJnxtW1FRYXSjCN6AxTs+71EjAH1lyZDJ3TkIPQAAEABJREFU2vCxYezQDzasjBRvW7Aqps4gNoLtxGITSNcgwQmfv3nrQI7m1e1to8Z9dbMxvibN5EV+uuV/QXHvDfkopgA9AwiCTbDYbKL+mqaOHniGNVoO6MrKSvw7JCRY89LZ2amw0Jqv8ytE6Xckozt24DJSsnC8mOHiG+JelhVdNSZYkRW98M1o89oqS43elIr/m7Tk6k7UEM5dJ04OKzvz2bSfkkTMDsMXLJ84JerG0pNZjTUOuijxmylDcTyf22/VhikINKPKytp/RsTixxUVteNnxv8EkuKkuJiYgpg4PnF4x8Bw3q7kNMR59e350wYGcUhh4pFt20/xqZA027//27PG9PFnk/yYn7ftj1PfDiUM1USEW/iYacM74zucZMY5oUA9qpoTOnH62FD/cA6HeHvxunApKb2yj6qPWxg2fczwUB4S6DXLi3h71tu4WSRMPrlvV3Ri9Zty27ZtZ858r6Sk9OWXX9q1azcyE93Z05OVm5TGCvThOCQXqYOOdAefl3p1e8nXBYmzkq5duZWtDUUaLmfxwqIiwjxZSsm9q7FX0oqULM+Q7mE+bX2dne26DxzhK1MWZV6+jsuNNVsXQTB9fX1w7Nfe3p7L5eD7BOfOxdSqoyzNy8INONDDZIFF2Rn3snU9W2d7NLsZGBZoJ5E5vxTqh7Iux165pyl34HWPighylPBvlVa9ZSpldE6vIQN1LSiNL053Duge2b09h6XMTbkcl5xFRWdZnmHdwjwdcDNifmlBlt4+sjxe6t7tJT8OEqfExSVnq0O5dY8JDr6PGzcmJuavqpi7kxO76iTNzc3DNxveemv0d99tMTtfm+FNqrtqox2n3s0g6oDk3kq4lKTtOFab0O4+qITuH9qRLU2NO3dNUKLEhd16dfdypN7vU0pEuhv4dJeOPaN6dnS3U+Ykx8WqK+oKQ7zsFIU5yfGx1x80zg0eAAAAAAAAQL1MjIB+ltFoNqhR4QZVqkpTNURxX67aL9B+8CbFfKHpwCjB8Q8KCxJy6kZbC+KWvt52qV4BKU7cOOe9I2yCN2zx5wNQi0XtePulZlU1fvTAM63RAtBpaWlisfjLL9dpXpaXl2/evAVZoUyYlFUW0bWDy4kskQLZ+4XxkPBAZhE1Cjnq43kj/OwZSFEm/Gvr+ur4L4MbEjEoKrwDzwVJMpNiz5xN1GbnsPcN7/d6RJifC8rPvBp/5lJSdW4L+w5RE0ZE+HLt5aLMpDMHzqaYGB7NcOFx7SV3LqXjDUKK9NiDu5kdysrqtnNV3Q5Sb+qsGV2Ff6XY9wjvYF+WHn/iaGx6vZsEngIbm9rfx3n48GHdcHP9X9shOGyCFIuliPAbs+7bSUTMviNxRNiYxRvY0snL46R+w1Z+Md+fH70vRhowbN1O/6XqQgM1qwY8E2z/8MhQ6aloE2k9CL+3t2yeRcT9fOSUU4+3123hfTJ5TSJJNTuLHbNtXwwKGzN/yxdo8vv7+dqLBg7HLSfn0c2bN197rRcyn4Nne5fSu3FpLoEDcCD1XqkM35UJGvnWQFZKbMId5N1t4HhP+s4DSVS81VB5qUPYiDcjGWmXrxXQfUOHjneQ7T6Ta3hNxprV4vG8ZDKyoIC6Q1taWrZ7997g4M5jxryZl5dXVGT2yGy6c93tycL7xHJ7KXJw+/KMW0lpmZ7dxkxy2PfTmWylc/cxEwe6CK9dLfUMC/VmyTKNtUA3vPhLI98cyMm7Fpcs8caFbtGadSH1SOT2nXxLUpKydCOG6c7dx0+OpKddTkpGvt3GT2Id2n0pW2bgmDzx8GOz2YmJV43tYkLClYED+/v6+liWB6n2JhlYNd/wgurdpI7SPXpQjxFj6JLtp6hzjm7n1S1qKDvjckJysiQ4cuJk+s8/xj/SLGLn1al7QElyVaQ5dOyEoe45CbHXCtv1nDiNe+DH4wKlutD1QULCHXpIxNgJ9MJN0QIrE24DAAAAAAAALPPcBqBR46q/QakwOe58Yq2RyexOw95+e2CPIH8OEvMTTx7ZfypRzBnw6Yb5kRwOzxsR3vP3nJlOUiHmbQtWnZIGffjturH+VFSVFMdtXPCVdnivXMy/GsNH7NDQWXU/ChFekW9/OGlgEAeHIwRxR7btihGY7C+23wBcvw+PFMScy25IO12mbfhsoDR6X5L/wIFBbGmybkSdY/jizYuDBEfOkWEDQ3E07+K+7ftjMqVGV8H0H/PFhlmhmgwjeMdjvprzVVyBkU1CPKNHT32sLN0L0LwaLQCNoz/vvjsdNYKizBtCxcRgP/uzoiJ77xA/+/wz6dRYakWpKDUlpczexS8i3JfnwMQl6voM3usfLpvikhh9MlqIOkSNmbc6eOeSdbFCxBu8YPVEhxsnYv+S+74+YtbqcN/PPtmepA4Q+w5fumoqLyv+ZGwKN3zwlGV+LitX7k03EQqm1qZ73y27Gxt9V7NqdTvc9L9Oxgrdwwe/t2w5V9OOPc83JOJVrv2l2MQkbsSg2as6MBd8fsbUJoHnE74Lue5Q6GIcLuYg/qaPYnIQZ3SfIGncJ5t2JZYQcdLOez8cGOSYKAjt4y+NXrpgKX4nZSfefjucYDMJIrRuzbi4EkQWJO7/JjHa7+2doZN06xEnH/gq+VT4utAgzv6vlp7W3k4lEL4XmiigcjYRiSho75g+/o6JfILNxvVPnYq+Ko4+uqvmLcS0tDs4Youjz3/9dQFRCdz7devWLUPNxF46cAI45dlxuXkSMT3S25melaek0x1YSJKdcuuWUHYr5dofuqoGyx28g9rIbhz6+1quEmWWeM4YEMRhZWWnxP+R5v2GN8fh2rkTd0pNLK7j4+Mzdeo7CoVi585dIhE18hfvy9ixo/ftOxAZGYHMxzK4Peo/5srSzNiTf6SVImel34xuvi707BIPX5fSpOO/n8uS0e/KOO+GGm1BYnBx7yBO6bXo3/7AUeekbEmYL6LSdchyky79keT80iTvnvobppTdPXcgUyIswNuSqfR7t4evy5VssYFjEubXSiwu0B/djG+aODjYV73ERwmH6R0cHAwfATrn1RnLXtVWzVa/nRnaJIPdUWSo4xw0u/k7tZv8IscZvfEBuakdIqDMT449l/BISc9hdJwZ7OOa8Ej06Hrs8esuodPaVXebnU+Ie0nCgb3HcYD52oPC7gGIQUcMTeEBqjClkP1RVIg7S/AAItAAAAAAAAA0ByaTeD4D0I0cgbaqQbfIxZu3TuJlX4lLFhD+kR/+b0Aoe9yMmHqXIzgBARzzhvfiVez4dXqQLDs5WcyLHPvpwHD/98YtizGafpqq/9Mkf6o+8TYO5Doh0qp2qAFzAUGhPTj+QeFCvpgI6vNhn1AOSS1CcHhBYX3Cg0LFfL6YEzpmSZ9w7/dGLY1BRlah3yTPm8sRaHNwUJu0czpPeCWRL2YHDfj0J6r+Kn5jHg3Q3KwJQEskkoiI3l9++YVeSSG+MzZnzkdubq01JeXl5QcPHrLmIYS4tczUfGZUmLd9Yhm3Qwd7UXq6RB1qLko5uycFB31H+4UN0qvOdPF1R8Iz0ScuCBUoMfHCHm05ozTl4NolOenqIcaJQvT9og5+LoykIoV6xLRvWfy3azcl4Xnx6Ypvl4WF846mp9czGJnJ4PI68lwYSPuoQDm3a4Sv5K9132yj8kH/lS7fsFzTjvr8zk/as3E7lcw5Pov57YKIMO5fQpHRTQLPKXy37dT2k8SYxQP4S5f+kizFfyxw/Nd/zIZjkaT6HZRDniIIROD/S6WazM3StFPb0xD1mEFDNZElGQbw3T526KwNnwbx2ATVglRAPRBREPPzqT6L99x4m8zgJ8bt277t1E2xbhD1kydP9uz5VTM9evQoX1+f33470rv3a6+/HmU8VwOL096Trrzn4s1jKZWOft4OCXlFyiJ+XHL7kdM+66kUZ9/jX7sUd0udONhgOR3RHTwiJ83qqslI4YySjL3xGGsWIV9fXxx9jo7+vXXr1u+9N+3HH3dyuZwxY97E0Wf8PtOzZw8cckVmMrU9MplMfRyU1PGww+V0hh1S5qoLlUqZ9iAZbaHu4oiuVJZoCwvSrpnOrqVEDp69ogZ4O7MYDAdn51Ix3fAxIUmy1uD91NTbY8e+OWfO7DNnzmZkCJA6b4x+mu+a6xFf3bnjBA4WO4dOndHN+OYY7Q4Dh7R6N8vLleqs2Lo/9EpNzyhFCVvXJBhbF25BoSgp17QgSk1QpxZx0S8sL1doMn4DAAAAAAAAmsNzOgL6KQh4+7fUt7XT2fvfGbk8Tsr29+egjOhPZixPlGqe+McRi+VC/ppxMWs4A9Yf/2mAcOMU/VTRydtnDt6O2JFrz+wcZtZKOUEDBwTJbm8fN+6bZCkzaNqh459HDg9ixwgLjNaP9NfVdwxfeey36Wxr2qkijvlo5MI4MV5kj24RdblMsGvG+K8SS9ihiw4f/jByYCgnmTS2CkH0wpHqLLucYT9e2Bqut2v+5MXVM2YcEJCIN+z74xtwfVZMjNGjZ/1egOZizaf5Y8eOs9ns1q1dNS9//XUfn5/20ksv9e3bJyUlRVPYvn37qKgo6wLQClFKeunoDh249vm+Ie7yzAM5JgPDZZmXEkWvz/jyy5Ar6UJRZmpioiathaJImMUM6T08ys+dyWBwO9gzmS5M9bhppr27PSqTlGreR+WS/DL0qot9/RvG4PWevWpKR+pxdOpHBabYu9gzXfwGTZnVm5rtwHOxt69qRy4v0sTN8QbGnjzKE5YpTGwSeF5ROaBPJYt7RH4xKdIvbn8mLiGl/P0fTflK72mEhD8VY9Y+RYBwCwr1R4JkgaGaFiGCxqxcHMlfNWdkXA7ijd5yeJq6WC44tWbcqa/Z/qHDJn04a+UXSDh+VWLtVeDoc0CA//btO3Bc/OHD7I8//gj/oza8Grqzt7ezg0unqKGdEJ3lQA9sy7peVKosund+9/rzdGde0Kv9Br7xJpLsOEdlWDZUXkLlYo47tCs+t958xIab9fPzfeedt48ePZaSQmV1ZzIZn3wyDwdYcTBd8ybz++/HSkstyGZj9vaoK1e/TdKrc0DXbcHIaGO9Giw3T2elJK/IyBBeulvoyKEhmcd/+yOrVOkQMmlGD00DdY/J1ZxHOBDPYDCqwu5ZWVnffruxR4/wl19+CQegcaSWw+Hk5DxCDWKsl03vJo4SK60Ypax/oLhtXBWFjyR1mi1HAAAAAAAAgGaCA9BlZZA11Ax6OaBJqSBZqv6PQIx6vL33TGgyn598JebcqTi+uDGj+QTB5hBIKhSoB5zJxUKBFPmzOWwCFZD11yfFt4XFKMiKdqrIxHyxVLOIUIqC1Iuos5BIhRnqb21LBad+3kUEZIhVBM/yTSUI/wGzVgZRwRReEJtFmN4kq/cCNBtrUrOLxeJvv92wZMkyzc/hw7/hQkdHR/y7qhDHiZycnJB1ykQpWWXuIR14HcJ48qwb9WVJLkvZu2Tu5wdSytw79J44//MfviKkoRMAABAASURBVH0vhIoCO4fP+u77eYNDXHCUxnQD5gaAy7KOLnhz+NBp21JKDS1RKow/czLewPD+opQzR89QyaEt2CTwHCHFyfuOiIMmTQvn4L8yYqGUFxruz6YCxKM37Fw7zJ9JSvH7MSe8TxCHUD9qdsunkTzCYM161iQlCU4QTxcoJjj+PAJli6k3WLZ/EE8b4PYbMO2DMaFsqeBq9M/RyWKCGn5d01tvjQkMDNy5cxeOPiN1uoYLFy6WlBh+3B/dwdPPseDc7m0bN36/cfNvSSVuvp4s6oF73Xu85MlSFglvXb6WKUPasakGy2USicLBz9eNGhDsHDJi3OBOulitskTJcuQ4sqpWZmBxL682kydPwtHnW7e097diYv66cOHvX3/df/fuPU0J3ngLnpVsfHsMVS4pUTq3pyrTndsGcFgWtiCTiBXO7QM98HIOgf3fmTokyMHobT+6nZsDXVkqoQYSs1w8nFlGD2lRUdGDBw9efbW7/uKVlZWXLyfgA4Wne/bsgcPQxcXFqCGM9XLdjqMOCHWUqN30DGxDLxVLzHz4oU55Yb7StWMnL9yCY8eh02aOCmHTcWEhLgzgUoVeHb0YUlGhhc0CAAAAAAAArGVjY0uSLTMDno1NrWiYytbWxoIPlbWoc0DHxFA/cYmZ6i8/F8StmvLO59GJYsQJGjDr8x0njm8eU+9HfmuQBqbMq9+wdtTfyTa9iDQt+qs1X0XfLLF6FZrKwsTofftP8sVmLGXlKkAzsGYEdJ8+kbNnz7Kzs9O8zM/Pnz//E9SYqDTQaOKrET3cmaKTVGbV+pQJk87sSTpDZWUe9uWXw6M6HLwjCh/Rg5G09YtvqCwYyL7DeyEhYdracoVcgRhMpB17zGBSzzU0FYSmvnTCZGjHKuPqDKpEoW5HLko5uXPP3ZpLG44uM3jGNwk8JVlZ98PDX334MEvzsrCwsLSUCmXevHnD1dW1qtp3331vspkSfsz+5EmfTh+wK3F/4s/bYjasPPTvdLGUIMSnlm3E9yTI5J+3nVq3cs/laYjFkl7ZNieaGvVsqCY1XHri3uNf9NDcvulzLHUWKr6ybOTkAwKyhH9yV1z4p7/d+BAhwc9vjVqVvH9b8uaVe2On40CyWPe8A1IsJIN27v1zPi5hs8nETR8lV3/lhEaj4eizv7//jz/uxDtbVY5P6IqKCoP7xvIMcCnPztbEE2UFd8Uo0s+Nfi9PovQY+t7cgaUyJYuluHvmkC6HsoFyZd7l2LQxI99fEVkqo9MlSb/HamPdSvGtK/ygwXM+G4BQbtz2HeeyDSyusC87cOBQVaxZQ5PD2koyY9tjsLLwclzWu2Nmr4gqKaLSLhtvwcHwuq6eS/YeOW1JFGIwZHdPH0gqUCLnkKlz3mqveQcNmr16ECq/+/vm3clFuVfiMye+8eHcyBJZSWmpdvSvwUNKfRPl5KxZM9PT7+I7grXWyeVy+vSJ2LJlOzKf4U1KMdzLBjoOH5AUfEDwbuI38Huxv98qUrY29rUSl9D3F07upFlXyML1Q1F52oH1O5ITTl/zGTt79UB8oMrTju26JsL7nxN3Nnni2HmrqaxLhXfOHkySQAAaAAAAAACAZmJnxzKeqvE5RqMhJpNeWamiAjvqlywWC8cB6HRbmUzeaCmkyZy4XQvjdiH1o/Y2H/5f5NhI/1OCNPX4Y3UFc/I8V1M/yU9veBlJQVUjzjQTRtMw1qmPdP+1tJ1q1q7azPpSfvTGVbonYNWYrWmlQasAzc+aALTmqWUHDhzUvPzyy3VBQUGoUUnSk/Ltp0SFyYXR6fna4C6D26EDz57JdPelfnUIC2OUKSTCO1nyrou+W+SbuHYJ9TQ/F3celV2jDClKy0qRCy/EzzkxqYhK+tzBpepWk0KUcqdoRMSEMSl7zwhdwicO8itLj842Ps5aUZSeLnLB9ZN+OiO07zpxsJ8i64SwrKqdESk/nUkp8xuxcNGIst2frI8VGWnGxCZplInyS+27RkX1lmfhrVFIMlOy4AGFTSs+/lLbtr5VL3HQ+eLF2MrKyj59ooqK6jv4wvMf9TuvmSQFR2f0OqqZFpxaPjLma39/HikUCKXaRC/qtBibeEE8QiwQiKsK69bETR0YF3LA4Aql/KOfjDyqd7cnLfqjITF4eSQUCEqq3ln5++f22l972dzcvPbtA7t1e4XH8zp9+gxbrWpup04d8/LyDK60NO3IxjS9V4e/17wqSDq2MaludaWhcmVR2pmf0s47uDmjooJSpf6MlBM/pJzQq2pg8eLiho7kLb1zeOOd+renNOPoRl3WoNKUfRtTdJt0ZCP/vDNLVqCXO8NAC0YWL7p3/qf1f+Oa9FJdA0Upu9ekGNhOZdGto9vuOrs54EaLqg+TwUNdUFAQG/s3jkH//vtxTWYSjZdeChk1asRff8Xq32CoeTTwdupuqBQl716frJ4yskmGe9lAx6kPyJk69STXd6y5XqtQkrxjabKBRu/8sXXNOUeuK10qksh0y6ce35p6HAEAAAAAAACaHZPJVChaYA5olQpVVODP/dRj03G0mSDwbuJIewWLxbS1tcGBaWQpNi80sj9b+5mcFPMTk6VBiw8fmsWJ+3JVtIAkeH382ah63BgpFUhl7NBJ894WnxKSUmFyMl/KDgoN5bEREcYjWASnc/iAAf5SqSA5MVOqXUQsJonw8GHDhrHFpDrRR7LgIl88PHLarLfJc2J2n+mR3GL+FRPDhKXCJKF0eLimPqfP2CDtQwilFrajw/IfNmua+KSQoBaRCZIEUtJYTN3SVWjqh0+bPkC4LU4avnLHhmFo/+RRmuSiBo4ejrFYuxeg2VgTgLaxsSkqKtYPedja2qJGpZCkp0iYHb0lmekibfzZ3nfEvHUjvLUVvKcu7Ir/k7lnzidHU06czFw1ZfW+weo5pXdOfHsiE0eHE/fsfnXV7M/3DS4tlZdlJWVJ5FXj8cqS9qzf6bJwxvLvxuJX+Td2b/op0VSwsSz9wHfV9SUpRzZuuyTSa2f19qnUmtNPfPNdLLW9RvJrFJnYJO16TkZfCpk95dMe1Ct5ys43l5xCoBnhmN3Fi3H471D90WfTyBIBP61OaYmwbqHhmuaTSwVpfDPqxcT81adPhJdXm4KCx2FhXWrNxdHMuLhLqGkpSwueqfT/FmyPUlZUIGtICxasy/CqDLl8OSE3N3fcuLdGjhyOu5VOpzs7O+Erpz179t2/fx89q2g0mvGvtilLxWIT33szuSzMhbkwF+bCXJgLc2EuzIW5MLcx55p4COHT2qoGYjDouHEca8afm5Au+oxf4h863Rav2proM8aNXLI1UveCvLJkyOT9/CM/nwqfP2zJ1gGawoyTqzfG5WjioVL+qW2nxmwYO+zzrcMQEh95b8gnyaHTN+wYqwt5cSd9sXUSQhm73hq5JlEdgSYFMRs3xmxY/PaXW9VPO7y9fcS4b06tWhCw4YtZn2+mQlWi5J8/Wbafb/yGAZm2f+ky73WfTafqS5MuCosRR12eaVk7OjKhgOzz6U89cCPii5+v3k99z9tIANqMVaiXJGvUX/fFrK3HpuOXxfwjq5Zt1D3aysDRiymwei9As6HR6RbnoHn//RkREb2zs7M1L0NCQhYt+hT/Q/3666+qHkLo7e0dFxe/c+dP6OliOPN49qXCnKJGec6fPZfnIs8X1m6MQZUjkVBkVnL+xt0k0AA+Pm1zcvIQAM8zfEfQ09PDy8sLX0jl5OTk5uY13eWaRby8PDIyrHkOLQAAAAAAAOBZMGzYyNjY80+ePCvPIQwICDDnIzwOJRssZzIZmlk4+ox/1BF2Ov48RZIKW1sb/IMnjH2YwhFqZA0m2z8olIeEfL5A3FTBUILTKYgj5fNzzBvty+QEhfoTwuTk2vUtaIcTse74njHC1SNnREt5PEIoEEjN2jujqyD8xmzY878B0m3jxn+VXFKjPo8U8DVptc1i4dEAzceaEdDHjh1ns9mtW2sz5P766z6+egjnoUOHO3fW5uK4efM/XA09dYoiYSNmsSgTGXwgoqJMlGX+G3LjbhIA4MVWWVmZk/MI/yAAAAAAAAAAaDwtLAWHZtQz/gBVUVGJo88EwcATCoUCT+C4s4nocwPIpYKbcQLUpEhxWrLY/OpyMf+quBHaUS9CGvqet4n6tVbB7jJtwxeT/NlsHo/LQtlH5uzjl5iqb8UqwDPDmgC0WCz+9tsNdcv37duPAAAAAAAAAAAAAMDzDIdo6XQ6js+ilkKdfEOpjjJXRZ+VDAYdh6TlcuUz8kXS54NUeHHfLqmUL0UNQ0qFSYmJYoKUCpIuxsQkwrDllsyaADQAAAAAAAAAAAAAaKkYDIaxBNDPr8pKld7YZyr6rMm8gaPTNBqCELS5yMyY7WtiUIM1VjvgeWCDAAAAAAAAAAAAAADQaWH5NzQMRp9Vqko6nY4D7ggA0GRgBDQAAAAAAAAAAAAAqIYDsqWlpagFMRJ9VjEomuCYSi5XIgBAE4AANAAAAAAAAAAAAACoxmQyccQWtSAsFhOHnpXKCjrdFv/IZKQm5wYurKystLGx0TylEADQFCAADQAAAAAAAAAAAACqMRjMlpQD2taWykCrGfusH33WqKioxD8IANBkIAc0AAAAAAAAAAAAAKimzgGtQC0Fji9jdnYEDkCTpLxRnzdIZ7nxvN0cjAzwpDt4+vgGBvj6etSsQXfu1H/0wAAHK8eF0p09PRye5pjSp74BNbE8ur8xOMwNRtk+uyAADQAAoPmY/h4fzIW5MBfmwlyYC3NhLsyFuTD3WZiLA9AmRkA/ra1qCJlMrlAonzyRNWr0GUdi3SLHT35vfA9PluHZLp7eQUHd3xgzJMhZPzyqlJXmZeeWKq1L+8HyePWNAS9xGjve6hAw+oOJYc5m1GyiDbAWy4WjvHv9VgEkUXl2wc0BAAAAzUdl8nIP5sJcmAtzYS7MhbkwF+bCXJj7LMyl0xkmRkA/ra1qCBzarqiobPQAN93ZmyO7fw95ejvQs2VK5MB7qb1Debkjx1GWfTctu0iWnXQpm+/zBidCf5lO3Xv4uaCSXEmNphx4gUHeLkrxXX5GgYwqYbkFBLX3ZOGW+Pc1JXRnXlB7b5ZMhsPdJdVL+XKQOIufkV1qOAJbt526HHy79Qrr1Jbj5hI1zLO04O7V6/eKlHUbN2cDWJ4dXwr0dkFFuVlpfGPbZN2C1OF1KVeyOHhn+GnaTXLg+Xo7OyCFp0NR1UJmbgNoNjACGgAAAAAAAAAAAABUYzJxALrl5IBuOg5tfOi5STdy6d5tHfBLuqN396h+YRwkY3UcMWlYoIOhZZQycXZaZgmn60uerKpxoSyfgZOGd3VRyhxCxrw36iVnajzyG+OHBDnKlA7dxkxVN+UQMGLS8E4sJXIO8Haha5Z6Y9Lwl1ilpayQEZMG+xochV23HUNkkuy793JLSktxxPbu3WwxDqbXbdycDWAFDBw9oL1dQa7M7aXIHr7zjp9cAAAQAElEQVRGVmfdgvjw9ozqHeaMlC4h2n0xeATM3AbQjGAENHihleeUoBeAnZcjAgAAAAAAAAAAzNPCHkLYZBw4vo4ld/NykaRXew+HpCIZDi9LshKuXc9WZju0H+LnQr9nYPStrCD7fik9pNyvuojOCfRUpvwRez1XmXz3nhu9FDeUcXTLDmdPD44zXULvxHGkZ9F9XWQpfyRcz6Xnctr30yzFwUslJOeiXLy69hx6Vnad1ZXWbsfQJiFlUV6W0kHSk5ObmXGvSL1J3rUbz0ZmbIBYJlPK6JLyktzr0UkFMiNjj61eUKY5vCjXxbuf+pgYPAJmNQWaEwSgAQAAAAAAAAAAAEC15/chhCqVqnHzbJjKCsJya+/nEdR+clvk4KBUclh3sqlSTbxTqVTS1WE3s8KfVFWlUn3ElaW5eVSJW+joMd3sxLliJcvFjp5bo462Uf2ljK2ubjtmqtu4WRsgE8bu+/OlXj2iIgO9lWmHdh5LKzWrcTMX1K5ZnTybbuwImNsUaD4QgAYvtIDugehF4OWBAAAAAAAAAAAA86hUlXI5iZ5DOFzcuHmeTcSf6S7eHMmln/ZdykUeEZMGeLvQcQCaznJ2oIJtzhyWUqx9yKA6WspAJiiVpUqWmwsdFSCP7m+EyuLOP2wT4CKO33f0TqlDwAhPKoW0srxUpqlDd3Bm0Uv0S6jVycTlhtIm12nH+Ebg/9HpdG0Uu27jSmTGBtAdOI6l/HNHkmJ5A6cO8eOw0koNpJ22esH626GOtTVNgSYFAWjwQsvJyUMAgCbgBbc9AAAAAAAAeG45ODg+tyOgKxGyRY1H3aBBdGdvb5bkmoSKeRZli+m9vJ2v4Qg0w+XV8bMGuTig3EvXxOp4qKwgia8cPX7WqwrZo2u/n8j2HTGiWxtHN46DbMacbrlXfz+UkKcU30sShwz9cC6OAJfz/zxUqix9lCGJiBgzLgTZ2bHskITKkpGWJJ48Zs7cEkmRkoHwqpQFKXFZb77x4dyhSCnh/xlbYCAAXbcdo2R5d8XOY2bM7S7Oio8+datO40q6GRvAcg58Y2IkR4YD6qzytGix4civ1QvW3466Z6xoCjQpGp3ORAC8kHx82kIAGoAmggPQGRkZCAAAAAAAAPAcGjZsZGzs+SdPytAzIyAgwMyP8DQa/rFR/7Z+LLSKQkWfTYyArovu2WPSGw6x+85nQ8wTAD0wAhoAAAAAAAAAAAAAVFPngH5eH0KoCRyjp6K8VJwrK4en3gFQEwSgAQAAAAAAAAAAAEA1Op3+nKbgeLqURSl//IEAALXYIAAAAKC5mP4SHMyFuTAX5sJcmAtzYS7Mhbkw96nPVQ9/VjRFyw2cCwB4TsEIaAAAAM1HZTKDGsyFuTAX5sJcmAtzYS7Mhbkw96nPxQFouZxETdByA+cCAJ5TEIAGAAAAAAAAAAAAAFoMBg5AQ/4NAECjgQA0AAAAAAAAAAAAANBiMhnP7xMIAQDPoEYIQLPZbE9PDyaTmZeXLxaLEQAAAAAAAAAAAAB4PtHpjNLSUgQAAI2kQQHot94aGxXVz8vLS/MyJSVlyZJlPXr0iIzsLRBknj79R3l5OQIAAPBCotMN/ImpVEPPGxs1BJrSUzw3oH+bAfRvywb927JB/7Zs0L8tm9X9SxAEahjoXwCAPusD0IsWLYyI6B0XF//rr/tu3vxPc3PM2dl52bIl+fn5r732Gi45c+YsshLDmcdzt0cSoVBU9pQTD9nz2nfgOqgnS0Xpd4VlqAGcw2csmx3BuLF72wkUNRid3BmbA3mVAAAtkoMDu26hjQ31XOvyctmTJw16M2029vb2LJadSqWqrITHoTStp3JuQP82G+jflg36t2WD/m3ZoH9bNqv7l8FgKhRWxiqgfwEAdVkZgMZR5h49eqxcuerGjRv65Z6eHvj3mjVrly9f1qZNG2QVBq/3/FULI9xRqRw5MEtTdq9bG53a6H8MGdzeM2b3Fh747mS66badQyYuWx7hop4ujV8765vEImQ1ex7PPmXjZ+ld31/2JTfzwDdFEH0GALRUJGk0bZytra2ra+vCwsfo2da6dWuZTPHkiQyB5tKc5wb0b/OD/m3ZoH9bNujflg36t2Wzon+ZTKZcbk0OaOhfAIBB1gSgX389Ckefly5dfuvWrVqz0tLuPHjwcMuWzXi6rMy6oLFz14mTw8rOfDbtpyQRs8PwBcsnTom6sfRkVmOHapnOfh18mfb11itK/GbK0G8Q4vZbtWEKaqCy1OhNqfi/SUuu7kTgecViEUwmg06n49/4bzkCoMWpqKiQyxVKpRL/lslI1NgqKirLy8lnPAbdurUbXDo3v2Y7N6B/nwro35YN+rdlg/5t2aB/WzYr+hd/1JVKLU6pCv0LADDGmgD0xIkT/vortir6HB4eHhHRG0/Exl64cePG7NkftWvXdsyYMX379jl06DCyFMOFx7WX3LmULsIRZ0V67MHdzA66ULZ9h6gJIyJ8ufZyUWbSmQNnU6gBxNzwWR9GlV2IlQRH9eChzEvRR2LTNQOLGdyQiEFR4R14LkiSmRR75mxiVpm6ldGLZkdx7Z29HRz8Zq/vgO/qKfITd367J6Ws5iquqldhenPtfcP7vR4R5ueC8jOvxp+5lKTN0GHvGzVhLG6HWSa8EXvizNWsMtP1je0dMCAkJDg19bZKVf11HhqNFhzcOSUlFTUxvCJXVycZDsiRspISOUmSOE6HAGhx8J0VgsA3Wpj4Rkvr1s6FhUWqJvj+HI5u29vbW3u3smk5ODiQJLwJN5SKSUcMW5oNzWiFShVSVNDkylrlTX1uQP82Cujflg36t2WD/m3ZoH9btubpXwbD4hHQ0L8AABNsbWwsG7/Zvn3gm2+++f33mwsLJfhlr169li1bwmAwOBzO0KFv3L1779GjR8XFxfjGGo5BJyYmSiQWJqywdQkaEuWXG3s66TGVKl/xOIt/V1iGJxm+w1esfT9Eln7xIh/5RYwa1Z2Zcvm/x8g5bOyUkV39XMqybqTL/PuOGfca82b8f48VDN7A/1s7zU946WxMYhYzaOg7Y1+WXE/IklYiO7YLu7KsjOnZjl2QnpSSmZuTm3Uvhf9QaqteRQdpSuyllEq/Xm+N6sGiVqF5C7X37Tuwi+L62cvCqht6DN7gT7+YHliQeCnxAfOl1yeO72t/J/7fXBm1qV++H1KRfjE+xdZv6KR3IljaTTJcHxndO3j3rgNHxDZt+p+Pj8+VK1c0JTgovGDBJ+PHjzt+/IRFD1hwdnYqKbHgwb74JjCX21okEkmlUhyDVigUKhXktAItEz638RmOz/MnT57gCU9PD5KUW/Tvi812qPffF16LnR1L/3G1VI4645pzrqMjG1+jI2AtFT6mbg40Rzsai4EIoz94Lq0VgT9EqUglTe8NtanPDejfBoL+bdmgf1s26N+WDfq3ZWvO/vXz8y8oEJeUlBirYE7/KpVKvFIbGxt1PujKhj+T0JyPGACAZ5PFI6C9vb3x74wMgeZlWFhoZmbW3Lkf4+kdO3545ZWu//77L55OT7+Lf7dt2xbPRY2CGs7sWxb/7dpNSfiGXXy64ttlYeG8o+mZeJ5ckhK9cdMFEUKxmczvF4WEcBnpWUwXX3ckPBN94oJQgRITL+zRtaQQXo3eeZXBG+YX5iw88dO2JN0NQIZX1whfyV/rvtlGpZz+K12+Ybl6FcaTRJemHFy7JCddPYo5UYi+X9TBz4WRVMbtqt7UlepNPZOUPn9GmB+1SUbqFymM7l368/GQruaEb8MuX75i3bovliz59Msvv8YleCI0NHTp0mX4zxtqMnQ63c6OyMzMRAC8YPBFKj7zPT09S0srlUoLhvy7uTkUFZQq1Zen7u7u+LozPz+/Vh18EwdfiVaFtk3f1Gm2uZqrZIPVbG1tKioq8e0ohaIJ33BaAJpLK8RkIOqTEqI7tsL/rajzLU4brr1KVEYdaBaT5qRCkif6c5vu3ID+bTjo35YN+rdlg/5t2aB/W7bm7F91DmhTifjq7d+KiopWrVh4orISx6BpuItxeLrhGSy9vDwQAOA5ZHEAutZ7iuZ2VtXLWne0TN8RtQzT3t0elUlKNV8CkUvyy9CrLroMzvKyojLthKQMdXBhMhEqy7yUKHp9xpdfhlxJF4oyUxMT9dJdGFmFiz3TxW/QlFlURhHkwHOxt3cxlSRaUSTMYob0Hh7l585kMLgd7JlMatVUO9WbqhBe+GblBc0Chusjhem9A7Xcu5eBw804Br1s2RL88uWXX8YvcSFqMvhM5nBcIfoMXmS5ubl+fn65uSLzFwkK4t1KuFOK6F26dMnOzsYl3bq9kpx8U/9ekfp61MaisdXNQL1JBi7H8d80G+rbjjY1/7gxg6ZtXjecg8Snln7yC1+KLMTkDZi3bvEAMmb1qo3xwsZPuP0UqOi2NBYTqT8dOfUJUeQVIVsa3c1JevEWDdFs2r/k/Cp6ckpg81oHlPoYKfKeZJHIjlCVkDS9OxxNd25A/zYQ9K/+4tC/0L/PF+hf/cWhf6F/ny/N3L/qFBwWDFev27+4BH+OxiEjpbJCndjPVm8si/X9m5OThwAAzyGLA9CaIIKHh0deHvXP/saNpEGDBv700w58I4vD4ezc+bOmmpeXF/794MED1GTqfS8sS9m7ZG5qRFTv8JDer48YMzX75JIFP6WYP6S4VBh/JvGG0ETaI+fwWevmdS1LScmUmJUcyYL68MUk03C4efnyFWvWrMbTeKJJo8+Yq6sTjr4hAF5s+F+B+tEl5iZWEqvzFdnb2wuF2W3begcGBsTFxeOXxcXF6HmDL53xRTP+TZIKBsNW83VC3U1WguctPrJ0zn4+EfT2+p09CEQmblx6ipj27SxvsZTIjTmfF/pqKAclb/sqhq0tFB756odEsaZtuTAu+mQfNrkvUYj8xmz4bCyPkIpvnTp9N6hqqTGfTeosJTiqSzecXg9Wt/95YtDnmprJXy39RmDxp7ImxtSObaE7tlIWP5Fl5hK+Hohhy2jjqhTLWwXT5XdRqw5sObeD6/iCwu8fVC+lfDpZ9aF/LQP9C/0L/Qv921ygfy0D/Qv923j9W1GhND0C2hw0NSaTgWPRNccyVvdv6LQfj+NItDB66ZKq43/nv9I2HcvFJMH/+atTxJhvV1IVTu9Nf/Xq7ysRAOD5ZHEAGkf6RCLR8OHDzp079+DBwytXrqxduy4yMqKiouLvvy/euHFDUw1XePTokVX5N6hM90yGZmAwYnB7z5jdW3jgu5OZCnz7jcFEmnI8xUCKsvrCtGXCpDN7ks5QKZaHffnl8KgOB1OSjEeg5XgVclHKyZ177poT/2Xwwkf0YCRt/eKbRCocY9/hvZCQMF07eAO1u4Cc20e93kESfzaFaaR+9SKW7d0LLj397ty58/CE5l5I02GxiPJymX6qLABeTPhfAUnK8L8Imcysi9G2nhylQ4ZIhezs7CSSomvX/mUwGI34xZhmgAzM/AAAEABJREFUpv5EpPkakGYfalxDe4d/uvdzj/THrYkKkRQRbPwphpQmndweLXZt/3IvgmDz/IN47BiptpBAxj7SSIXJfBIRrdrwPHRLxRHeZNKRGGLcUK8QHqESa9rX1SQI6k+HZY+IaU6qcjnRjit/9Jju7kSN2FEolQov19eQ7FxWpeiBNIdg+Nqj5Kefbwr61zrQvzVA/z4l0L/Wgf6tAfr3KYH+tU4z9K+Tk7NC0dCQhEpNLlcymXTD348n2Bxv8b5V24mxAzjsquNv18rmcdK5aHL4AI4jm9BWGOpMe9buCQAALGBNDvjY2As4vrx165YtWzbjl4mJiV9//c23326oij6//PLLb7wx5ODBQ8gKiqL0dJFLjwljwn25vODXp0543Q9JJGVIIUq5U+QeoSkPGzxxkF9ZZkq2ibdU5/BFe37f/mGYM/XCxZ1HpbjQq66QF0kU9ryQMEpIe6490qyCFzFhRJiXPcM5ZMwXv/66NIrL0C5QJsovte8QFdVbs4SvMyotK0UuvBA/ag1UEucOLkxN0/qbGjz4/XkzRoTYI4XCWP3ai5izd4CSp4aaGA6Z4du/CACgTuXGYJh75/LciUv3ipRFRUXqIQ+V+AdPWPxk2meGei9wMB1/NKG+vah3DU0KM4igPv5IlPLfjWwSScVJfIE2RC8VCwvtQ8J5bPx5qaolqViQKa5+yeRFjhkeHj58Ujiv6o+CDbN1UHfdUlJBkjRs0tt92pA5KcKa7T+r5NqBNsqSJwwPZxqdzmrHtVEhRe5jfLhkp0492nCqMFXy5PeEolN/S6o+Hcmf5jst9K8FoH+hf6F/oX+bEfSvBaB/oX8bqX81mZrxlT9qgMpK7fNj6HSqNTytl/oD9y974OIdezcMY4rZw+fPG0gIxfrhZSanx9hpfdhicYlUmK2p8KhIhgAAzy/8rsW0dJn33pverVu3devW4Rj0J58s0DxvsEqXLl3Wrl198+bN5cs/Q9ax9x08e+GMCPVfCknKkY3r9yQVacvnLZzRQ12ef2P3pu+iU4oQw2v4l+tHCL+dq358H6PD5A2rwlNWLtyZXmbfYfSqVVM6OmgaLb1z4tu1u6kH/lWtJmTK58vGdlDPF574hFqkxipK0098s35nUlXCUwYvatay2VHe6gMmT9k597OzKOLjVbMj3FFpqbwsKynLOYyXtFLXTtUuyIXxW7/YGJujoFowUt/Y3oGm5OPT1pwEUq6uzhJJ4ZMnTxAAL7xWrVq5uLiak4XDy8vDnH9fBMEsLZU26RNErUCn0x0c2CRZPexF/RVRG6WyUvMElYY/wtsihH//adPH9GDHrfrkwLP+0aiKqz3SpSmkHpKjUlWUmPweSTlZ6yE5TXduQP82Auhfs0H/Ni7o30YA/Ws26N/GBf3bCJqrf1ksu4EDB5848TsyW93+ReoQdlUmaBx9NvsJhG6Ri+fxTq7ez689CN3MjxgAgGeQNQHoIUMGT5065eHD7I4dO0ycOEkqpW5UOTk5RUT07tWrV3Bw57t37y1fvqKhATt7Ls9Fni8sav5EFAxq1UgkFJk1ApnhzOPZlwpzam8ogxs1f+lgdHbn1rPpZWbUB83OzAC0hwfn4cOHDbz9C0DLgK8a27Ztm5cnrrdmCwtAA0upbGiIw6bZmvVJEn8iQfnFtJrPJWrOD8DAUtC/LRv0b8sG/duyQf+2bM3Wv2y2U69evc+cOY3M1jz9CwFoAJ5fFueAxv7++6KDg4Ofn+/atUdx9Hn58qXh4eGaWTKZ7ODBQ/v3H0ANVyYSPqUUFIoyUZb5q1YUCbMMDQZUiOJ3b7OfvWzVKsaCJaeEivrqg2cVjrjVG3329/fv2LGjh4cHDlWnpqbCEwuNYbm4MEokJZDR5LmF/y2YPXIBvNBolSr8mUfFpCOGLc3GaOZvFa6mqKDJ4U3hOQP927JB/7Zs0L8tG/Rvy9Zs/ctkMqlncwEAQOOxJgBdXl7+229Hql7icPOJEyc101lZ90tLSxFQPz5x9vzRfvbC+BOp+TDYueVydnZ+6623ioqK7t+/LxAIXF1dBw0ahP+NHDt2jCRNfpWL1S5i4sjurgz8T6rw/p3khMvJj1p6UiuXbpMXTnRP+XH9wTtVu+ro3zPELuNaqgiufwFoeahPPiY//Dy3z6QEFOjflg36t2WD/m3ZoH9btmboX3UA+nnJSwIAeD5YE4CuBQedEahDIbq0acklBFo0Go02derUkydPZmZmVhUmJCT06NFj5MiRhw8fNrUww86Lyy68fiwhn3ok5cjpbRSbfk0tQS2ZJPngphw7qX6gne4a0jPCUZqSKmrZuw7MpMkQ96zNBc8C6N+WDfq3ZYP+bdmgf1s26N+WzVgf4QC0QiGH/gUANKJGCEAD8MJ69dVXCwoK9KPPGleuXOndu7e3t3d2drap5ZXlhfcz7ghkdx6ggNkR7VzpqeWuwd0DytOuCSRKROcGd29XnpIsKFHSHf1DI3qGBrgiUcb1hPjkB1S0lu7SsWdUz47udsqc5LjYa4KqxBasNqG9eob6uyNRcmzstQdUOS7q7oNK6P6hHdnS1LhzerVrMVKT1a7boKjuXnaKwjsJZ+NSJUqTG1C3MqtNt17dvRypWzMpJSJBiXYzu/u3C3B1tes5dExAubIwIy6Bqmxg+8FzycHBvt46FRU1+tf0VWxzzrWxoTk6OiDw9CiVNb49BP3bwkD/tmzQvy0b9G/LBv3bspnZv5oUHJb2r7s7NyoqCjWlmJhzCADwfIIANADWCwwMNBZizsnJMTG3BrpLcETPdignoVCJ7Lg40FySk0QFoO28ukf0zM/BAWiXkLGTh9oln4tPRe16Dp3sRd+y63qJY+jYCUPdcxJirxW26zlxGvfAj8cFMqq1npNnRjFS4q5dQwE9J0+z2/tj7AOlnVe3qKHsjMsJycmS4MiJk+k//xj/yFBgl26opsix29gJuM34BBHdv/uoyY7leF1KF2MbYKCyTNd4p+4BJcnGw99Gtr+l5yZpqWSy+nvumc0o7ezscui36KqX5eVPdvyw/eTJkwg0lyY9N6B/nzro35YN+rdlg/5t2aB/WzYz+xdXKy8vRxbicDi//roPNSV3dw4CADyfIAANgPXc3Nz4fL7BWVKpFP8Brmd5O6/Ij76MpKbKM06fvV+CkKOhanSGox0qvJ+clPxAlpyccFxd6OgT4l6ScGAvFdy99qCwewBi0JFMiZTlaad3ZRQ+EOHQX4YyYGZEgGvcAxFeQJmfHHsu4ZGSnsPoODPYxzXhkbG0y3VqlniFeJVf30uVoYwSr9lDQ9xZgkIjG2DnY6DyA9mj67HHr7uETmsXoVuN7FFy7PGUdiN9uI4Jp6Orso8Y2v5HMAgaPAWtecHl8koPZ9u8ogp6WcHPP+9cu9Zn06bvaDRInNgSQP+2bNC/LRv0b8sG/duyQf8+F+zs7ODhXgCAxgUBaACsV1BQ4OLiYnCWs7Pzo0eP6lm+PCduy5bjAuTi32vsxFGD7m85LjJUTVmYEnut49jZX0Yq8x+kpSTExiY/ktERXaEoKVdHZpWi1ISqJZWI7RUxaKiPqx2d7ujqWpLP0M3QfN1KKUrYuibB5HbVruniRWd7RU1f0I0qZ7i6omt06s3D8Abg8rqVLWB0+wFobjTUyYtuY0NTVlQ+KmdeuZrUf+CQ9PS7Z8+eRc8oppsXW5pT0CzPLG/OdTUN6N9nZV1NA/r3WVlX04D+fVbW1TSgf5+VdTUN6N9nZV0mt4NJkGQhAgCAxmODAADWysnJ6dixY91yBoPh5+cnFAqRWWSSBykCqR3X1Y7KyoV0N4bUv2VUGFcpufPHjjWLFn7547n7dmEjJ0a1o+bpjQpmcdu0cWGpF+J2HzsyVBK3d9O333619fidQgVqDEppTuzP335FWbNo0ZpodU4NgxtgrLKZmmj7AbCUSqWSySuvZTxJvFuWJSIVNDu218vufl1VqkqmV++Fv5w8f/7c0e8mdHK0tGGmV8TMhUP9mKjx4aY/WDR3gBfTrKrvLvvmu+3fTOxkzpa4vTpz+egaNU2sq27lZxD0rz7oX7NB/z4ToH/1Qf+aDfr3mQD9q+9Z7l91DmgSAQBA44ER0ABYLzExsWfPnv379//rr7+qHsKA/1ovXbq0vLz83r17ZrbD8grpyC6/LypH5YUPCu26+bizBDl2Xh25SJRQoqQe9tc9xO7+teRHD5LjEzqGDGLQ6bhmvtK1Yyevy48eMDoOnTbBPWHrj/EyJd2Oy2YopIXUyGSWaxtXO0Y+arDywkIl2z+AG/foEXIJHTm03Z3jx1ONbIDhyiVG21aUKOy83B1ZqSXqMLXB7Wf5vzE9Cp09LggdGyE6fbyk54TQBwf3JoggMQdoUpWVqgol/oetklVI7Wyd8M2QC+eOnjsX4zX06yD+F2/OFIZ/PDWIxxRIQweEMkmCRwjiY27myBHTL2LogCC2IO70+bQChBw79R8a6U8mx5y/mok6DZ357sT+4UQXTpeb5w/8cj4T1axci/6ydf4VMd26DBjav4tbztU/Tp1PI716v/1uBCG8KZDK1Uu+MSyIQGxCjFumlmV6vYpXREhJUhhz+mpBTvwv6wVD16zgEQRC6lE2TBNbQnD8/F9Fb7O7CNWtMWuuq1bjwpqV0bMK+rcK9C/0L/Qv9O8zBfq3CvQv9O/T6l8mk5DLn+Nx9gCAZxCMgAbAek+ePNm2bdvLL7/86aefTpw48Y033pg8efKyZctw9Nnd3b179+71LK/OAb1x48Yv50Uo4o5Qz9pTipJik1DUvNXfrPtsckBObGwGvrpQlhQqvAZ+tGTF4sWLF4z1ehCbgGvKchJOX0M9Z6/+5pvVM0MKY09fU8djZTlxsRnsofOWLF6wYPpAL9QoMVrc6NkURtS8datWrFg40qvkzoMSZGwDDFd2CX1/Hd7RzyaHuPsMXbh+48Z173dT5y7BOxyfQo9YSB2GBW+0oxvcfoadq6sr245ux8b/tbOzc3R1dYGbZ6CpqSoqUU5p2i/3Jv6cMXa/YMa+XRtWL/7A17c9/khBlpBInnN+/RdH0+QEr/fEdyd2YXtFLFrz8auObhEL137wKiK9Rq9YPtqPyezUf3QEWyzt9MHa5UO9VGLB1ZuCAvw7Hv9XjGpVrrUFNZetPdcxaOrHo70yb+Z49X8z0o8pl+bwr2ayQyOC2FRNtn//dydGeBGdJq5fg5d1fHXh+o9fJYhOoyeODuUZ2FvTW4I/IvH8O7npWqu1rjqN16iMnlHQv/qgf6F/oX+hf58d0L/6oH+hf59O/z73I6BZzt6+AYGBPr6ezqwaHxzpzp5Uoa6M5ebNc2PVXBZX8fUJDAygfnypuSxnnq/mJfXj4+3MMtIaAMAU+JcCQIMUFhZu2rQpMjLS09OTx+MVFxefOXMmMTGxd+/e48aNU6lUV69eNbxkyZ2Da+YfrFMsE/zx3WexLlw2KhRJtLkrlKLrB26VfYcAABAASURBVL+6XqsilZdj65pzjlxXurSqJlWcfPDbNO3yVeFnyfUda64jMygN1lRKUo9vTT2N14VbLVGa3ACDlSXJO5YmG1lhcvR3ydUPw0aGtp9+fEuOokSifPDjfUWhRJmzNU0Bw59B01KpkKj83omcTyrVt0Hif0p8+PeZH44e+23r9vu165ZIBacP7D+PBEODpEx2EI9NIL9OBMHm+HEIJEi7men3aicOfsnj0ApuXk28OTSCczPm/E1qLA+nZuXMmiNNxPrLEiinxlxSmillT+gfQcYf3R1DLZh5NZEdOrpT1XxB4u8/7BIP8FvI4ziyeWxp/MH9u6TSTgsJA58mmGzTW1KjNbwl+uti1mm8ZmVp0MQVc/tzkJR/4Jvv/sp5NgbTQP/WrAD9C/0L/Qv9C/2rB/q3yUD/1qzw7PYvQTCf6xHQLM/e46eG0ouKlA7OLijv7O698dnqz6vOnYZOfSsIpf26+UBaKUIOPlHjhyiPbzt6r/rTLJ0TMnrqAJdScakSKRRFt04cvecZMbC7mwuH44hKxOIi8bWTh67lKeu2BsDzoFevnjQa7Z9/LqNmBwFoABpKqVTGxsbWKrx06VJFRQUOSRsNQJtqUSZ5ZGbeZGWJyMCDC2USkQV5l81lcF2GN8B4uVlqb7+yRCKh/lsi0v8PAE0I3z2KS/yltdwXT5/eE1uepXpn3bC7j2IrKpWk5gMG07FTZH82/zRfu4Q8J/73HPyZJ0gqPH9w+Q83Nd+77PLB3KFo9/JvpMPWzyX02td9MVO/ci3MoDGGl9WuL/P3j0efduvS/4OPl08jF/1w08SXMeWklCRe9cKXzfjDT4F+W9U5Fk1siWnGG9couXlg0bQD6NkC/Ws26F/oX+jfuqB/mxD0r9mgf6F/m7B/W0AKDmVpxrlfDtwqde4+6f1eYR7Xsu/jD5gsjg9HmfsIubX3ZKXdkxlfNiv2l70JBbohT9kHfrjm0Gn0+0PRnzuP3qkKNZvZGgDPFIIgcADadB26Ay8wyNtFKb7LzyiQVZX4cpA4i5+RjW/O0J0DX/KlK5GLAxLfTbtXYNb5DwFoAOqB48i2trb4N7JQQkICAqBlse7fgvnw38KqdOpPd25xcfH3H/+kX/Lr0lOaCaaXjXD03PWdSDa6+k1irUtzuTAxXrx27vddCDaR/MPCHwQCMfuDqYv8pBwOob4ZJRcLMtkfbPq9/9UfFq44VaPy9/E1n3kurr1sDY6dJqxdO5QQStmE+Bexyqv/svWL+gfxOKS/X8Qvn22S1qhcELf7aJeFa79nI0Se147QkUsFN8mJqw+eJvm/fLra5JbUxKy1roXRdRtvfNC/0L/mz4X+RUZB/0L/Nj7oX+hf8+dC/yKjnqH+ZTAYCoUClzek958VdAcXBzrSDl+ic/y86bkpN1BokJ8b/Z5QaXwpT7+AQBelUlaUm20stGZ2awA8X1g+AycNccm6zi8PGfNeSMK+Y7dkPm9MGsLiX7mHQkZMCvxj96ksuttLkf05Dy9dy3buNT6Uc3RvQm79/wJodPoz/qRcAJqKj0/bnJy8equ5ujpLJIVPnjxBALzwWrVq5eLiWlhYVG9NLy+P/HxxvdVwRLu0VKpUPlsXbHQ63cGB3aSh9mbH9OryahCPFzH61ZtrFh3NbNwhLU3SeNOdG9C/z0Lj0L+WgP6tBv37LDQO/WsJ6N9q0L/PQuPm9K+9vX2vXhExMWeQJXD/hof3+O+/W6gpubtzzPkIz/IdNmdGdxfNC0nSrztPpRUpEd2t59TJQfzfzqEB44NSftl9vYDVcdyHdVJwePb+4ANNCg5luTj5j+gr6uwd2hHQ26tGQNdtDSLQ4BnWq1dPgno8KvL19cF3jzIzs/A0ScouX75Sqybdu//UgbI/dl/KVeJbMW50cV6pp64EeURMHWJ3bu85ic+IST1zow9cK6B79+zvm/t3fFb9aWhgBDQA9VAolEwmEwLQACD1F3YUCgUCzx0mmxcUEeFXcPWbtTGN/OmoiRsH5oD+bdmgf1s26N+WDfq3ZWuh/auOUj3zQ5vroyzJvvzHhbslMnGusEgTXnbw9PN08ea8OQY5uyBZGwejIePaKTgMqtta/UN0AHhqaGpVE7osHAZyceAwMV2pVH/mV5bmUvd7WHolSiVdF0lWqm9lKbMTTmUjs0AAGoB64HAbvlGMAADqQRMQgH4uyQuuHvjC8oT0z0DjwBzQvy0b9G/LBv3bskH/tmwttH+ZTIIkn/9bGsrS7IcZ9/SCwixOgKcyK+GP+EzkG/lGSCCHdSsXWc1Aa0WQBho8u6qeOtivX18cfY6NvWCsplJZqmS5udBRAfLo/kaoLO48v7xUpi1x5rBk4nIrR/tDABqAeshkpKurs52dXXl5OQLgBdaqVSuCIAoLixEAAAAAAACgJWIymXJ5k6WdfmronPaedPH1q/yMIlTk0j20e3s3ei5i0F1efndZV6qCIvP4tt3XCqiqLr5D/2/lUKqw5L9fvj9s4AGDhlqDNNCgRVCK7yWJQ4Z+OBfR6eX8Pw+VKpXKlLisN9/4cO5QpJTw/4wtUCIHZAXIAQ1eXGbmgEbUlxSQhwc3MzMTAfAC8/f3f/Qo38zKkAMaNBDkoGzZoH9bNujflg36t2WD/m3ZzOnfwMD2bDb7xo1/kSWeqRzQAABjevXqgUNcly8noGZngwAA9VGpUEGBxNPTEwHwosLnv1j8GIGmwnTzcoMbwi0X9G/LBv3bskH/tmzQvy0b9K81WkgKDgCAIZcvX3kq0WcEAWgAzKRQKJ48kfn5+dnZ2SEAXiStWrXy9/cvKytXKOBbZeZhekW8u+yb77Z/M7ET02iNmQuH+jH1Xn+waO4Ar0b6iMT06v/BAr3mrWykvr14UUH/tmzQvy0b9G/LBv3bskH/NpcWmoIDAPCU2drYwNPVwAvK2dmppKTU/PoVFZWlpWWurq4EwSQIwsbGprKyUqV67h8QDEBdtra2+F6Lg5ajSPQYn+0WtcBmO5SVPam3Gv53hC9wLW28qeGtYjIJRpvugyP92oX0CiIk9/NKKhDTL2LEuMGvupQJMwueIKZbl8FvvfPW6z54bmaBXH9ufv6Dm1f59F4DOGkX/s2TI+TY6fVh/qRAjEIG929XVsiO/OCDd4dGvRLUvj0PCVOErXq+/W4/juRm/OXUAmq4SY0VOXZ6Y0xkSEh4Fw/pg0xJvaNRmF6vjhgTFdTplZCKf8/eLKiopzUL9gJ/YBoR6SK8m4dwnV6thHcLmnZoTNOdG9C/0L/Qv9C/0L8N7AXo3zqgf81qGfr3uehfHx/foqLi4uIiZDYnJycOh1te/qSiokKpbMIsKw4O9hZ9hAcAPDvgIYQAWKawsIjFIhgMZqtW9kwmA8fpEAAtDr52lMvlCoVSLleWlVlw9dmSELzeE9/1Tz4t4Cxa0+m7j38h5q79gB1/Xjp6xXL28kUx7KkfjyZOH8306/9mpGB9Im8hNTdeOnHtcvbCRUdrZIxnsv379+cVxCQT/hFDOcLEaMHVm4JQf+Jq/NU0/KlJjnL4VzO7vBsRxD6dViJ3i6jRVKJ//3cnopjz0v7rXyXmLjqdY+pjCV52PbUs6c9jFxDaEv3NrtVaHMfQXugq19wLOYk6jZ6I+MLM0RMjcr45jZ5z0L/Qv9C/zy/oX+hf6N/nF/Tvs9+/NBqNJGXm18fRZwcHB4mE+sjg6OiAG5DJLFgcAPCCaJwAdLt2bfHvBw8eIgBeADIZiX8QAKCx4etdE98qaPa5JVLB6QP7zyPB0CApkx3EYxPIrxNBsDl+HIIUZ0rZE/pHkPFHd8dkIl4oWxp/cP8usdBveScOgTJNvEXIC9KuJt4cGsG5GXP+pvrjTubVRHbo6E7quUw2p0ZTiYgUJP7+wy7xAL+FPNyyqQ9IVctKpZ0WEqSmpMZm12qNlNbaixqVa+1FQfJf/IkTIiP9/KXxR4XNnRkQ+hf618K50L/Qv9C/zQT6F/rXwrnQv896/zo4OMrlcmRG/zIYDHd3DxoNSSTFmoHPJSWlrq4uEIAGANTVoAD0a6/1Gj16dGBgQFVJevrdM2fO/PVXLAIAAAAsZDqnzVOaK8+J/z0HMf2CpMLzB5f/cFP3yeD3j0efduvS/4OPl08jl8cYXNRR24J6mhowQxCIJKs/dRDaeRZy9OsSRAiT0+r5jiah+U+NzfYaWqOKPLPWXtTaR6beXuCPFPzzN9krJr4q+OVgs38+gv6tA/rXrLnQv7ra0L+1QP82Hujf2qB/zZoL/aur/ez1L0EQmuNpun9feaWbt3fbvLw8oRBGIgIA6mdlANrR0fHjj+eEh4dfuPB3dPTR27dv48LOnTuHhYXOm/fx6NFvfv31N/fvP0DWYzjzeO72SCIUisoU6JnGcObiTS1rzC2153bg2Usys0TaBhnc8AkzouwTD+yNzSpDAAAAmptcmBgvXjv3+y4Em0j+YeH3yZzRa9cOJYRSNiH+RVwiFJ8XfDx1xVpESM//wC/BC0gFN8mJqw+eJvm/fLo6+ap04sz16xGbuPqd+rOFWJDJ/mDT7/2v/rBwTaL/x+sX9Q/icUh/v4hfPlsWV7OpyNqb4hU5c+3otIUz0wrqbKRYkIYmLlzrJ2TziKuGNltQcwHHThNq7kWNyvEFcv29WH40kx8XTw7tEp8sbvbPR00N+hf6F/r3+QX9C/0L/fv8gv59FvtXHYCuZwhznz5RmZkZ169fQ1QKDmc220EqpVIzOzo6lJeXIwAAqINGp1vz8NWVK1f4+/tv2LDxv//+05S8/fZE/Hv//gMcDueTT/7P1dXl44/nW/fWw+D1nr9qYYQ7KpUjB2Zpyu51a6NTn82wK4P76oxVC4d4M+VyfB8zP37nuo1nshTaWb1nzO4tPPDdyXSLt92+w3vfrgpOXLlwT7q2Md8x6zZMdP5r7cJtSS9oMtam4OPTNicnDwEAmoCXl0d+vrjeara2tqWlUqVSiZ4ldDrdwYFdUdGET1BpAMeI5d8NTVuLP640/6cUt/6r10fEL1zzV0HTr7vpzg3oX2Ogf5se9G9DQf8aA/3b9KB/Gwr615hnqn9tbGxGj37ryJFDJhrp2rVbSUnx3bt3q0qcnXEM2onJZEilJeXlTZh/w92dAx/hAXhO2SDL9e//erdu3b766uuCgoIff9w+dOgbuDAsLLRr1zA8IRaL1637ksViffLJfGQN564TJ4eVnfls2ujxb074ZEc6b8yUKF8GehbZh4yZEoEurZ02+s03J8zZKQyZODmCp9tUprNfB18/e9QYFFnRC998cwZEnwEA4IVH8o+u/+5U5tMYI8NkkzePHrha0OLGXz1LoH9bNujflg36t2WD/m3ZoH+1qvJvGOPvH4CD1PrRZ6yoqOjRoxwPD88mjT4DAJ5r1qTgGDly5JkzZ/n8NC8vr6r3prVr11XdzJRKpfv3H5gz5yMXFxeJRIIswnDhce0ldy6lU+lynskTAAAQAElEQVQnFOmxB3czO5RpxxDb+4b3ez0izM8F5WdejT9zKUmIZ3DDZ30YVXYhVhIc1YOHMi9FH4lNL1IweP1mzwjL3P3dSc2IZAY3avaHXdP36kYoG2yKqhYSMSgqvAPPBUkyk2LPnE00kfKCYe/ubq8QJt1Rb2pW/MHd9h3K5Mi+w+hFs6O49s7eDg5+s9d3wH9IFPmJO7/dc8e+94wPewj3blRvk2YL03d+d0aoGebs3CFqzJgIX5SfGJ/OQLrkG7yoj+eN8LPHBWXCv7au1+6Oehc6RE0YEeHLtZeLMpPOHDibUvSM5yppfB4eHvh3Xh7cAgUAvDjkBWlp6OmQZ8b/nolAk4L+bdmgf1s26N+WDfq3ZYP+1SIIlokANJPJ7NQp6PTpkwgAACxk8Qho/I7Trl3bhIQreDonJ2fu3HmnT/+Bp3GgGcedcUhaMyYah6cR9f0ILrICE0ds5dr7f2V3Y6NPJYrUAdvBC1bPjrDPvPrXFZF7+KzVqyaHOeNiBtcvpMfgCSP8ylJuCB3C3/ty9YQO9kghEZZxw15/3VczBJnhHvZ6V548X6KJRhtuCpe//uGyGWEoPTY6OlboEjVv9YIonvHB14qyzEyJfcjwEeqFqzZVXiZMSUlKSc8pRfJ8YXoK9SI1UyKngut+HXx59tqkJ/Y8vw5+ulcM3vCFq2b3dpAkJYl4r48Id9cOnVaUilJxCylZZVw/X55DVb4Uhu/wpbi+iyQpNlFk33XKsuXUXr9Q2rcP/P77TfgHTyAAAAAAAAAAAAA0gOkE0CEhL6Wn30EAAGA5i0dABwYG4N8ZGRmhoaGDBg3YunU7jjvrV9DcLsvPz8e/W7VqzJhoacrBtUty0tVDlROF6PtFHfxcGEnUK7kkJXrjpgsihGIzmd8vCgnhMtKzchKTiqJCwnn2d9PLGO4hvXmlqUcyi0w1VcR08XVHwjPRJy4IFSgx8cKeerao7P/ZuxeApq77ceAHuMkN5EHAJEAJFgI+YNAfPlqoD+xUnLa02mJXpA9xa5W2K3b/CltbXH9V2m7ifit0XbXtKnZW7SoWlRYr6lp8FDYFJpSHQqASCibRhJBIXsD/3AQQQhLeEuL3M0eTe84999z7vXl9c3KuuCC3OCb18W2frmq6WHTowP6iy0oDMkhKDn1UQhM+LJrLlRz5+G+lvWOo7cwjQhPMjQnSFO3MeJeq/b2E/ueXg8wlyorjeytwvjleNHdl//oR/eoX1Rp2vj43WphbW3unXKIQn4dvvZXh7u6Ob+Mbr732+pUrdQgAAAAAAAAAAACjQqPR1WrrWQU3N7egoOBDhz5HU4GrqyuTiRMG7jTaaH73b5/BYOzo6NBoOrq6uoa/FoNB0uk0giDwX3wwEQATprOzU683GI1G/Fer1SHHMOKHYnd3NzI99cyfP4/H4/n5+fZPQJvHROMbYWGhqDcNPU4MSkkDPWLxI8tEPnQaTTCLSad70XtGBOs1Sk3PDYUGzTIt14iLSxXLcFr2QK3YCyei1bW5tUr7TWnEZ4qly597552I72slUnFlcXHPzBw2+yQ9syO54ot5i1etWhXz250xy/e+kZE7miQwnenDRBqF2jzu26DQ6EdSX6+4pkFRXnfMCGicfX777bfKysreeedP+O6rr/4O372dOWjzKwd+JcP/h1cO4JTwK5aB4livWACAYaGL4jY/hnKz84czlSWb549Uze0wsaiDoPP8OapmmOgVAADA5PDwcO/qsn6Jwtmzw2pqJmuikpHB2Wdvb65Op79xQ2E0jv91LwnCDae28SZu3FAOJwft4uLi7e2pxR+rdNr2dr1Op3PUq3ECJ4HzVCSJ01Z0/IXHtGnUiWpK5U6yESegGxoa8d+goKCPPvr47run//jjVYsKeA8jIyM3bny2uroG56PRuOFGv/D2y/M0FRWm2SyGQSMuKlUsnRcddEghjBZqao+INUM1pan49NWUyphli6MjFi9fvTap6eirWz6usJ9QNigbio/9rfjY3lnPvPPmI6sjTu0onoRLBd450z/jEywjY/u///2fnTv/bP46BKeht2x5BS988smnJ+J6zf2ZXjm4OC2HN33zZofB0D6i7zwBmCrwmzYa9fU89f08k+mB37o5wiuWI2NHJW0OLtmxv9reCxTdP/ZX68gTQ6YF6f4xGxI5hVn5I74SDi9qU7KwaEdu9ZiyV8Pt5x1kXOM7DCNoysrZQg+Oigtu3yWzXNfa6UEXrUjZLCrcnnlGPvINOY3RxxcflSeT4iKFqCQ7ff8oHneWRxXfT06LKd+Rkd88/oeZ7r/4V5vjRDpZyf7dudXt6I4xjo/f8XmO7b9V531Y3TYQX+d2u19/+zd6G8PnUM/PDAYD50mtFuEs0IkT36CpgMl0x9nn9nY1mhg4qW1qnIk/KA25Ffx5ato0r5aWlo6ODgTAbYG/4bhpgm/jL0v8/PzkcgVOZKFJNeIENH7M/PTTT6tW/aKsrKx/9vmBB5Y899yznp6e5rsVFRXvvpuNRkOv1yM6jRqQTE38LFj83IuLJfuzCjTRq++nlb7/ljm9y5z1bETE3CFa0vTMwhEhDRLqcf65Jy9ME9prSiMpLdhbWkDNsvzwO+88smzWgYpSGxloZvj6l+PpBVkflVLtaK7VSjTLmF50ms10MDWekN47ahvfoCGNwjzZtd6gNyAaHZn3GtFpaIiDNLA+jU5dpPDOSELj8yMj463Kyh+6e/Nh+AZORoeH/2yis8/mVw783dGkP24BmGj4mxX8pg3/Q6Yz39fXRy6/cRvOfPwdT7ftVPdtLmWHPvRwGIk4pKw4v5D6MMAOjY1bEqwrO1FYIm6nMncx+C6q+o66S3JEwf7VJGILY+PCJPn51TpcuiKMU/8dXldOfbKIou76RwY3fzdo83Re5Iq42Ehec8lXxwolwrhNGxJjo8lIfmR54f49hWLUvync0Io5dB0pJOuLTpTL+DFxc1SF+eXU5sJkhWV8UXAUepITKenpMzL3s19PBuzFwNZwxstuPyfV1I2vxYYGH3M7TbFDl6/gVB8rU4WtiCHLCkuaUf9eUW1bni34MUsPi47B+dAqKv4DGicHnh54S09ueEhE6qqLxKbfsln2pN+2kLUNjaepGl99c9GezPq47VuFJInvUYvsHEaLblge1e90OCIxpKS8XnXr24T+rd3aKXxXbJmhGOrUQpyw2ChVfkrGmfZBLdtfd9B2LXbKckPjEkGHiG/vgbrVVN+DqOdQ2H9Gtdcra49fZDco9o/AwCgMeFnBxUPHaCwgvuMeX4fiNPEd6knS3vNzMRkz8OVYP+RT7oB+TKnnZ5JkqNXywaU+Pr5qtUav19mPr4PAGbcbNxRognV0aL29vewnoAmCcHcnxWK4jCiYNDiLi89AnINWq7sm4gcBwzfiixBieXlHFixYMGfOnP4Ln3321999V/Tqq6+98sqWJ598+tVXXx/l/BsGZW2t1Ov+dWujgwTC8OVJ65aLkEKhMag1auQljBCZLhYoiIiZ5UUfsi3TLBw+0auX4fzzmd75N5DtprjRaXsPf/C8+ZqCXj5CapYLO8Of9Qopfdaq5559ZK6/QDBz2eOPRDClFTXm6xwig16pMDCFEXMpETMFTNNFC2sUXvPiqV0Lmrtq7WIfhVgsNVU3KGolBp+YdatwU0FRq9bO9enpEk0wKxw3MG92EJNO95llaixIQDPgDSlxfdNRmrsqcaVII65oulMmgK6oqLR4qcN38UI0kXAOjsViXrsmg+wzuNPo9YZr16RsNpM+5HdjY2b/XextLuUEx25IjPEnRYkZ2+NFdHpobHwMR6YKTc5Ij/On82JSM5KjSDJ0g6m0Z5XI+M3x/jJZu7kU6fzjt6bjUnw3czOuLAoWcqg01UDssCS8lri82T/2sSWibll9SXm9HP8twv+VoZ6mkH9iBtUUKVycuCExkuMfk7YdN6lDofGJsSJeWHxiDIe6BgPJDxaRvX3GjVusbrEXA1tj2+/n5Jq68bXY0OBj3j9AA5ui43Vj5/BJxA/G3zTwyUG90lmcLRR2WHSUrqi4Xj8o+hanh14lKysqKlcFx0QJyb7K/Xaq37a6rWxoXE3d+FoYHND+GxrYDcujqlc1V5WIOXNiwjh0q6317lRoYuZ2vBcWm7Z+avXsxbTI5A9yMuKj124/nP9ZegzPYh/trmu5XYudsqg8/BiNpfS2xXdQU6QwOJTXeyjsP6MO1Sud9Wd7G0GxfwQsTpWBLyvDitFYQHzHPb4OxWnia/+Jzu7zs+XLMRriKXdqPz/3HwHdv/TuuwOvXm20v67joNGI25Bow5uwP8E0ztHz+d6tra0IgMnW0tLC509Dk2o007F//XVBVNR9v/3t5j//+S///e9/zQvb2lT4u53xSAJqavdnfeSV+lx61uP4nqLii7/87YwU3yremxP15ov/u2+VWq3XNJQ2KPRDz3lMzcKhfmT17Gsn94tvZWeVtppSVhw5Kn5z/bZ9q0x31TVHdh4R287qGppP/mWn4LfPb9z2wUaqeu3X72ceaejNTkpLj55sfv3x1G3UbkiOvJL6US3etcwd9GefS8t6nI73rOAvOz7tHV2tvPjFgYuzXkjaNi8J6cUXKxR6L2oxM2j1y2+vDuhpMiApdR7+j3jvS6/klu7NvHWUrl3MeffjyZj5406BXzmmTfPC2WcEwJ1KqWzz9RX89NM4zuzv+HT1xYd3fSJZ4p8eij9s1FeXi0VR+BaHL+SzOXyOqujAZ7vKd+2iqvKCSf6STRnRZH3W5hI5XcTHn4SQKJTElUV8dpm58icqVWgqOWhKbZ1KrOKsi43RFeXmnBCr9aikuDwuhl9+orCcGufSs65MIjJ1A7Wr6vP3f1aI6uPCVEguOVmVuG7JElGwqihXokdhOknx4c8+kUjMfRYjjsXqA/bCojU6J8xeP53ObYqv5YasH3NzgOw3RbfoFSav7n+2UNhhyyNVRTuo/DPdIvrFyOL0EJcXiSVkTFykuXFrO3VrW5Ybcni3Lb79WRxzy8NI5/Xvhou83OKoikuKOXPiQ220RkXQtFOyFaJU6vFrOWjS4tTqvxf63F3PJ9Vvy4z8KiWzhBoPG9+/lLS7rsV2LY4eXTRnYFO3abKB2xNfywedf9jAEEjsPKMiJLPXK2T5+LXo2KDW7B2Bvr3oOVV0sv4vK0g4OTEaC4ivc5uc+LL59p7oBnbD4vmZ7m9lL+y2Jp7Cz884Aa3TWZmCY/r0uy9e/A+aalJSXkQTIzv7/SHreHt74qwfAsAx4LPR23vajRuTljoc5fVAd+78v82bX3rrre3/+te3Z8+eq6mp+eabbxIT1/3tbx+gsdM0FOx4oeB9gdBLf02i7E3oGiSndv666GOhkKmWNCtvDULVHN2SeLT3jqH205SET/s1dfmj5x/5yHIDtprCye/cLQm5aNgMytK9bzy3nynwGdDVnsYq9qYm7LVYobn4ozeLibqBWwAAEABJREFUc7gCpkGqHJDaNjQcf+vXZwRBQT5IWtMg7W3Kav97Vih464UCBG4Hb2+uQtGGALiz3bihwN/EXL8+4T9ncxzkrf/Qw9amxKGc9B2qhzNTbg2yoX7mHEOW5dcjnax4zy5x/IaoYF5RGUIqSeGB9F3lPT/JFw5u9Ba9+PDm+HxeZGzy5vRf6dJ2lev6Ktr+oKBvLjpsusxCVWE5Z2tiVP2eAzj/zO/XZ2szCNrYi57W6KIwe/10PrcnvgM31MfaMbdczdQ82zTSikQ6nc6iVyX98o+9ZwtvTmwY/vAp0Q+xy9ZOD2s7dWtbFhuaAm5bfCn2xy/2bOiE7mGrD8DxPap9p1b/vRhsQCk7yt66/nHIzk7JkP0NTZTbGt/epiQDl9p/Ro1Mttcra49fO0GxfwQsDXxZST8xSTEaC4ivc5uU+Fb13Lf6RGcjoD3hs/FybLM1W6bG87PVOaD9/PyuXWudotfN+8c/xj9r8vTTq4asw2CQHR1amPcZOA58NuKvl/CZqdVOzlCjUSag29vbMzLejo6OfuKJX27d+rp54Zdf5qFxpJFKBg8+NiglDeOUrR+/pgxWu2p301LrW9ZIGyqlCDgW/Pg0GAx6PVw+BNzp9HoDnW6YxFes247kzFmXlsEJ5pRkVbXLODJOclKaSMXnkyVILykulGWkZIYiDqdqV7Hp+UGnrzqWU5KZsiEqLau4CJdmR5IcsmxXanZZfTVKTM0QSThCvK4ldui6jIw4UqLikLI9Mnxs9bJ6MSf53cOxJbtStx4rLqzfnLQ1A5Gqwl1V7cgyX9le9V2RLi6yqMx8ybmePocJ67PqqRyjZODqqgF7YQFv114/nc5tiq/FhgZGUD8wQNdlugFNyapKVImbMjMRhyzJkqglqkG9Gni25KpCY4IlhXvMJ4NF4+1oieXpMbAnA3aqeNARGLChKTCC8rbFV6+qL9clbjuQr6va87ttAwMqkQzYkKTe4gHYP3zbi4M3Z6bFhgn5umBRzJ4/pO6vHhRBNGyWAS2S6+2Ultldt96ytP9Oqe1uaOLcnvhaa6ofWb2dZ1SLUqtNWTzb2wmK/SNAnWn9T5WBLyvtEtmkxGgsIL7OzRHia/FEt6ve3vPz1mMDXo4HP4L0I3kmdPTnZ5K0moC+CyegERgJGo2m12sRAI4Ef41Eo9En6+O8C0GMw0RggYF3d3V1Xb3ahACYOgIDpzc3D/06yuGwuru7NZqbCIA7HpPp4eLiolINfUVpf3/f4cxa4+bmplarJvoKoiNFEASLxfFd9fbW0MOp1M8hHRovdltmTFHq9pNTIKUwEhN3btzm+PrH/em2nUj+sdsy8Mmw9eRwrjJG94+MDhOFxcWHFm1Nve0ZZaeJL7AK4jvRbucTy2AQX+cG8XVu9uOLY7Rixaqvvz5msfyhhx4uKvq2vd1e0PC60dH3//e/l9BE8vHhD+cjPP4kYq6WkvLiBI2ANk/B0behwUy/or5x8yakEYAD8fDw8PLyHuksHIGBgSJREL4hFjc0Njai0RrlCGgLjY0/IgCcFI1G3LwJP5wZrm4Wu9vdA9HpiO4YP+DX65BO56LtcFHDu9xxgN+teni4ozuDqr6wUCVx+MHedI6uPHd/iZNln2+D2xbf23kiNRf+YUPhcCuTfFFUlKg5d2t60RQYzzxSU+TxC0YJ4uvcRwDi69wgvo7M3d3K+3wWi4WQi/3sMxiMTqcNnLDFYXACQgS6pjopPAzvQPicxGfmiFbB2edly35uzvriG6dO/WvUOWhXBACwi0ajGQyONTzTMXW7unYJfLv5PojFdpTsM4Z7wubgXlF9c3FBYGzwYwE/ItCdob36ZG5Rs8Mn5vTiosP51fCRYMRuW3wd9kRqLz+cmbFzf5HYKc+eKfL4BaME8XXuIwDxdW4QX0eGE9BareXQK4HAt6npKgIj5ObmNtxZs8nwjXv3pszjCJZmHMxeE2D6JC2Yt/7D03WypvOZSzn9qnKWZp6XNZ1On3droY2a1iqTgqXpBy+Wnv/Xvy7+cDo7IZxaTgas+bBS1qepICX8DrgSzB0Ln5P4zBxm5YULFzz99JM46ezi4tJtghcuX74UL1y48H40cpCABmAI+PHZ1dWFgF3dDPdu/+mIyUIOi8nqFk7vJhkIjAF+LAz/FQsAAAAAAAAwVTAY7oMvmnfXXXfduHEdgYnjGTCDlF6RIkFAgK6uqU2HyJCEzPfWo7wdB64MnEWaM2NBOHmlyTN83nRzlthmTWuVOeEJqY96fvnMvJCfrdretDBl40KBuab0wvaVwXyTgFXZlTA0GpjgvHNo6Gy5/LpcLncxMd/GC3EhGrnxmYIDADBShO+iTb9Z4We6bVA0VZz+8miZnBpozQ1/5sVfzuz98VN76adZh+uMNitHPrP5sZl9A1JbTvx199lWQvjgpqeDqvfsPtE6YOS2tZaRcNWm5PsZVf98/581rPs3rA+r/vvfz1JNW23Z9kDwbjYHEf2fT1hdj6QYlwWi1vPEnv2urXrkPc/45C+6qTnndS5n9ru1zupcxHY9+o2L94Ku6T+51k3rfPznplLkcuUb1x/v6prR7nb0PIp8uNO30e34RRc9bnJm5yO/QOV73Kr03YsSjVF39fbtgtuZ611rbjVO/Lvdcus9B53WzfF0kcG1IKwhWL4BPLYpiMYOeYtECYcJAAAAAACAO4e7u5UEtEDgU1JSjMDE4CxI/3BnwsIAxtLPF+IMtKDNM+XCMxmV5zKf+fqKan7GmgGVyenzwsmLB7/mrFkYLthb2aRDOqn1mtYrN329fePXlRelOtRWebEJzfMkYbAzsO3s2XMPPrjyyJGjFsvvu+/ec+fOo5GDBDQAk6ej/XLRse/ljBn3xt679OfVV76oViOkrPz0rRrunHUvrjAeff9Ahelib4Stypi2/dI/P/hndb+Lwtl6WFtr2TwemB0QEcSqs7xg3OCWbehmsqhpN/ovCXnEuBi57X4PrX7F8Hgt/b3vXfQ/uZbVGjesRaf2uLW2I98HjE/Od22toKkXdC6+4NI+qzOM7vbFtzjR7HJDhqav7VzFRnXX0eq1RvoxV5yAxm1O/4Vx1QPI74Jr1ffoaoUrvb3z8bXoDM5HN7qo2/s3bmXrfT1jsbtvalw0Q+/UHYdg8YWhAWyC4Rcyg/jP3r/b+75h4ph/3eNopXc2Os+fo2qe/CmmIb7ObYrH11EeJg4LHr/ODeI7MeD1d1zA8/MQLGJkMQUHLuVyuRqN2mDQD7kuGB3V+YzUHYLMhXkp26Vr3ktFmRs/pEYgqypVOPdvUZcUhC8USE+fLvBcunBBuOfBJimu2GStpvXKOmndeam5bGHCKsGVvRd65oH2DE/58HgCvq3F+eyX0guaYAw06G/hwgXmxzv+i7PSaLRgCg4AxmrevLn4X/8l8+fPmzMnchirauWSxivV5afP1KgZPB6LGL/KI2BsV7QYfXEGetQtUsOfLfgGdqsrXOsq3N77X1rBZSr/q25x/XeF641216rzrldx/lfvclXeHRVhHvWMULvLjcuuZ791O/uta1WrC9K53EBdqx7uol936Xm3Q+8OC3QpP+/iPb+bhVyuXnQ7i1u7jltzK7/sohjY+OCt2+8twLStFWcKTl+SMQx1Rz8vbp2kac/tv4udrFJb6P6Lk3f8acf2LfGhbDRJeFGb0uND6SNYg+4fsyk1TkQfXim+n5yWssKfblmKb254fUfWBzsSR7T10YP4Ds/I4us4Jjq+IzySt/dhQvePTd7ikGEZN/D4HR54/A4XvP7ezicWeH6+o56fLabgwKUCge+1a9eGs66Hh8fg+aPBMHACwgWqyqtaz5Bw0v6lAT3DFwSoKiuvNl2oRDMWhtj/VGu7MhnyaHr6vCvZ27+s69mYrun07h3bsczsg5VwcUJgiewHjQGMgAZgrC5eLP35zx9YuvTnp0//C1EXBl3a2dn57bffDWNVBk8YGMriRSyN9NLWyNXG0VQm2KGPbNi8AhmN6qbTXx6tVqIRIpC64QoKighkt1oUDLtlwvZV6dSNrnU2im5UuLIWdHmbL3/F7g57WP/3eKS/7vZZJoFI1NqAIhd0l1908TaV0+/qnkG6nvoWrU7s8qW71g1vHIPVrRN3yjX0RowhjHnoXqKqQKaFq25S6P5RK+bQdaSQrC86Ud6sR3RRTNyKME79d/mF1XJcgRMWG6XKT8k4YzqJB5TaX5cd+tDDYSTikDJ8l7oCHFW6JBhVfVdY0nu3/4YGdosXuSIuNpLXXPLVscJqki8KjkJPciIl/ZoauG7/JbrQuE0bEmOjyUh+ZHnh/j2F4v4PJbZF6Xe6qCc3xJCS8nqVfnBp4Z7M+rjtW4XU2xD9oCOAHB7Ed2Cp0xnZkZyshwk+lai7/pHBzcN51wB6wePXuR+/EF8nf2KB52cH5urqdvPmzf5LeDyeWFxvfy2CIITCAL1e39p6bdo0b4VCCZdQGr6lGZ9mr5/HkH56PFUQ4KkNz7za9tKHF1XWqnJCFoZPD/d87/iDiBQIpPNnkOcv2kwW26pMBqzJeG8jY2/KloN1fStr2yovni6wvlUAxg2MgAZgHPzrX9/ib4BxDnok2WcqwxtwX+yKmAgv2YXcz48NMdeFzcoGdYvkypW6hgZJU/vopu01yq5Uq70iZliOgR52y8RovspyUV92/YHeFXWX6avzdpeqHPqv4xm/3kg7/SO1QH+eeOdt2pmfemp7B3aG+XWuWtvlG9gVchcaCwK+eLNBK//3VwUV7vc+8eQiIVysEb89Ey5O3JAYyfGPSdu+OYrNi0nNSI5COv/4renxommRyR/kZMRHr91+OP+z9BjewFK63XXpnODYDYkx/mRoYub2OH+6uZQkQzdkbMelFpUtesUOS9oc7y8ub/aPfWwJVUoKg0N5A5vqv+7AJd2y+pLyejn+W4T/azntjs6iVK9qrioRc+bEhHHog0st2O+2A4L4OrcRHcnJepjgu5mb8bkhChZyYBLGEYHHr3OD+Dr3Ews8PzsyLy+uxShmHx9fuXyIgQU8Hr+tTaVQtF2/rsA3WCwmAsN2eseOvHMF6U+sfCLj9Lm9KWvWf2grD0zOmB+OTm9Z8/MFC37+RPo5zwXhAbZPTuuVyYBVGR+meB5M2bK3ErLNYNh0Oi1m/ovGYHwSMf7+fs3NLQiAOxjOQUdHR7m4uHz//bAv0WCUlR3+6OuG4T2GbVU2apv+U/h19VgmNTZqFXWXFPfGBOAU5Kha1mkRw33AEr0O0elUZjkyyRhWS+z/3tpFUnUu5RfRqqRuq0Ok9XqXqosoLMJ8r3v6vO7W88SZi2gG2zgnsPt0o72rrtrfug6urmeLVimpK5Nr+U/+PIBVLIFx0KhdVZ+//7NCVB8XpqJzwvBHECQKJUkOX8TX5+56Pql+W2bkVymZJe2ILorvX0raXZcsRrr64sO7PpGtEKUK+WwOn6MqOvDZrvJduxA1AP/VRTkAABAASURBVGfOwKYGDnPTqcQqzrrYGF1Rbs4JsZ4fZtGUxbpo4BKX3JKS4vK4GH75icLyQcPn9PJqi1JxSTFnTnyojdL+H87pgzbt+KPzIL7ObCRHkl02OQ8TvF3TufGJShWaSsLvXUcGHr/ODeLrzE8s8PzsyDw8mP1HQHt6euK7VieA7s/NzRXnpsy38Q0m0wOBYSMFMwLQ1S+lKCCEo6q8aj6OZMjGz//11kLzkKDP65Pavn7p5y9dCF8gkJ42z5AhvXJRKlgYLjjYRK4fVHPjwSYUYL3y0k2Pzo/wnP+vR3dS9a/sXrkyvRLfEMzferx+q6kN7YXtq9ZkV8LbEtDPuXPfo/EAIwEBGDfFxSVo7AgGL0AYEMAiCGNAUIiiRSKRjyJhSjC4gTNmsHAG0dihbDE3YadlrbyhWr5i9QxiVF8kueh13QMT0C51511939T/YwN+s+e25xsq/zv9Yf2rm7pC7uqe/lHXZ28Qpuk+XK6ed72R1EW9/eudggPpXcr/Qau12AKrOyTIpWy36+kKl7ppnS/N62Z969I/MT6wcdrZQVsf2FsEBmEErVq/WJG7v1hOsFiEUQbJ51v0zUWHm/Hn0jCVpPBA+i5bn/wHlLKj7K3rH2etAeoXqTFk2QkZsrchvfjw5vh8XmRs8ub0X+nSjtnthunD1eAllN4fnFo3glK2rU1PFRBf5zSSI0kXCSflYYK3O3AFMGLw+HVuEF+7pVP2iQWenx0WSZJGo6Gzs7NvCZ8vkMuH/s1FZ2cXg0Gac9D4BlyZ0AwfSTc3t/7H0ypd3d71CaZbGQnnby38cE3Ah5ZV9yYs2NtzU3Uxe81S801rNRGqs15575qQvZZVVXkbw/M2InBHGM452V91de3SpT8fuKy7uroGjQokoAFwMKyQBxN/OdOUzl3wxDMRpZ9mHa6zlwxksO95Mu0e8+2WE3/dfdaU2qV53fPgk+al7RV73//iitp6y33NKK9UNHXMmGm/ZVv9aFchtidy6ZfpvfE97dcrBsy1fPUY/fn+7zDfpv+b+g+xeYXpaegE+eh7/Uq/7nl3WZVDf910Y/9vepZczaWnmm9dJl7/jY3GkeXW++D3Qyr4uZEV2qb/nFc/+uSL91KD7f99rFoJGWgLeklxkSwjJTuS5JBlu1KziwZcUN2ytMzuuvWWpYW4NDMUcThVu4rVdjeE2KHrMjLiSImKQ8r2yHRIOEQnBy+R1Ys5ye8eji3Zlbo113Kccv/S7cXBmzPTYsOEfF2wKGbPH1L3V1usq6ov1yVuO5Cvq9rzu212u+3w7sD4Di51KiM6ksWT9DApq69GiakZIglHSI7HN9h3LHj8Ojd4/XW2JxZ4fnZYHh4eFhNAT5vGa2n5acgVcZJaKBS6uzNcXV1pNOL6dQUC1A96DTinb3FIAZhc+JzEZ+bw6x88+Pm99853d7813LCjQ3vw4D/RqLgQxDhM1AhTcICpKDBwenNz65DV/P19W1quIWBX9zReN4eLHJ5Lm8LlxnUExsDPz2eYD5xr14YeMYG/g1WrVUajY+W7CYJgsTgj+nIYjLuJOzcgvo4A4uvcIL7ODeLr3CC+zs1OfO+6yz84OOTMmVtXM3r44TWnThXevKlBw8DhcGbOnFlbewVNJB8f/jA/iZirpaS8+I9/FKDx9vTTq7Kz3++/ocHYbJZer1UqlQgAh+Hl5UWj0dvbh/WgHndwEUIAwHi4cQM5/rtJowFB9hkAAAAAAAAABvLw8NBoNP3uUtcSHGb22VTzJsPiskB3NoPBgNP9CABHgs9JfGaiSQJTcAAAxoFLdxdqauzm+yAmCzkmjdpFds0FAQAAAAAAAAAYgMlk9Z8vgs8XyGRSNPU9/fQqNBm0Wp23N9fd3b2jowMB4ADwl0wkSd640YYmCSSgAQDjw6W720Xa2s1iUxckJElEd4wLduh1SK936bjpom5HwOG5uLjYuW7JZJUCRwDxdW4QX+cG8XVuEF/nBvF1bv1jxGKxbvT7tSifz7d/BcIpEV/zRBmTRaFQ+vn5icViBIADwGfjTz9N5uyykIAGAIwnnOeFVC8YNfvvYierFDgCiK9zg/g6N4ivc4P4OjeIr3PrHyMmk6VWq/vucrncy5drhrmuozEYjAThZjRO7BSReBN4Q3Yq4CMklytw1q+lBS6ZBiYZPg9lskmej9Th5oCeOXMG/ocAAAAAAAAAAAAAwMRjsW4loBkMBr6rUqnQ1NTR0eHuPuETUru7Mzo6tPbrGAyGmze1IpHoNvQHAKs8PDyCg4M1mg7735fcBo4yAvrBB1c999xzERHhfUv++99L+/fvz809jAAAAAAAAAAAAADABKDT6Qh1Gwx6812BwOfatcn8qf4Y4VybtzcXISZOEE/EOGiCcMPZZ9N0usohK+v1hpYWqbf3NJ1O29nZqTPBNxAAE8bNzY00Md1gTO7MG30mPwHN5XL/+Me3ly9fnpd3ZPfuDy9cuIAXzp8/PyZm8Z/+9MeNG59LSdlcW3sZjR6NKxD6MDUSiVQzLhd7ZApmCZkKcYP0Vms0QfS655Yxi/d/eqphuFeJBQAAAAAAAAAAAJhcTCazre3WeGcfH1+pdAonoLu6unBqmMn08Pb2otHGP+tlMBhxahtvAm9omKvgygwGSaPRPTyYdDoNpwURABMGf8Ohx199GIx6vVGjGfprkttj8hPQO3fu+NnPfvbMM0nnz583L9m8OQX/fe211//61/d37sz829/ef+SRNRrNaBK7NEHUc2+mPhhA1+sRHV0r+ujtvxQ0GHqKFj/34mLJ/qyjtSNrmSl85OU3w4vfSN1ba+i3MGLePK6i4MCpBgQAAAAAAAAAAAAwJbDZnJs3byVGBAKf6uof0FSGU8Pt7Wr8DzkMrVaH/yEA7lSTPAf044+vfeCBB37zm5daW1sLC088/fRTeOHixYtjYmLwjZ9++unFF3/j4eGBk9RoNJgRa9fHoDMZv4p/7LF1L30kiUh8JkZI6ymkc0WzgkRMNB4MDYdSH3vsub+VOsoXCwAAAAAAAAAAAABD4nA47e09I6BxBkav1/W/ICEAAIzdJI+A/tWvfnXgwMGLF0tFIlFHx03zwueff8Fo7JkbW6FQvPtu1ltvZfD5fJlMhkaExvTxYRokpTXUZBmGhqIDOcxZGj1izopPe3GZgMkNYLFEL2bO0uPCa8Uf7dxbw1z83PP3Sz79y1FqlDRNuPTF5+bWfpRVIMH3uLOWrV0bE4SuFRfV0lC/yTeEyza/vFrExMs0kpPvZx5t6Ctjzlq2bnVMkICpl4pLC/Yfr1COywwgAAAAAAAAAAAAAOODw/GUSJrMt/387sJ5GAQAAONqMhPQJEnOmBHy1ltv49tisfiRR9aYl5sTzTglvXv3rk8//fT8+e/xXaHQf8QJaINGLFYwVz2yem7F3lIl0lw+dYiaS5pGl1RUlAq8Znn5BCkktRXX9AaDVKzAeWiul2hWEGLSkSnDzBSKZok01D0kfCT1zSRhQ9HRIqlw+epoH2bf07FBLa2sqNAwvUQx0UFCVs+qeCNBj7xmXuVUhSB61frXRV5vvPFpLUwQPTX5+fkgAMAEoNNpHh4eU/cS2wAAAAAAAEx1bDan7w05TkA3NIgRAACMq8lMQN9zTwT+W1lZuWjRooSEX/7hD/9748aN/hXMY6Kbm5vxXxaLjUZMIy7ILY5JfXzbp6uaLhYdOrC/6LLSgAySkkMfldCED4vmciVHPv5baW9WmGajGZpgbkyQpmhnxrtU1e8l9D+/HNRXqKw4vrcC55vjRXNX9l8lot8qRbWGna/PjRbm1kIGempqaZnCV2AAYHyN1/cxrq6u3t5cvV5PEGxvb2+JRNL32xcAAAAAAADAbcPh4AR0m/k2TkCfP38WAQDAuJrMOaC7u7vxX4IgliyJ8fPzmz49oH+peUz0P/6xLzz8Z6g3DT1SBumZHcnPvJTxUZHUJ+a3O3dti581ikmf6UwfJtIo1HpzmwqNfoSr6BXXNIjpNT7zTQMAgDNgsZhKperGjTaFoq2trZ3H4+OFLi4udlaZrFLgCCC+zg3i69wgvs4N4uvcIL7OzRwjFoutVrd3dXXh23y+oLW11Xwb4gsAGEeTOQK6uroG/w0NDX3rrbdnzpxx+fIViwoMBmPBggVbt75eVlaO89FodAzKhuJjfys+tnfWM++8+cjqiFM7iifhUoEw/TMAAPSH37P2XQYa3/DwYDz+eILexGDQ97l586ZCceP6dbnRaDR/bWnLxJUCRwDxdW4QX+cG8XVuEF/nBvF1buYYeXt7K5U9SZLp0+9uaWnuX2p/XYfl6urKZLpjNNr4Z70MBmNHR4dG02HO1A8Tg0HS6TSCIPBfNzc3BMCE6ezsxJ+q8Sdo/LfvQ/ekm8wEtEajaWxsTEj45ZkzZ/pnnx955OH09Nfxk6D5bklJye9+9yoaBWb4+pfj6QVZH5VST6aaa7USzTKmF51mMx1swOh0uvkOvkFDGoVej/QGvQHR6Khngmc6behNW6xCo1MXKYQkNAAA9MLvWfGbMPPLIb7R2dl1+PAXNBrdBP+HNN/Gb9FCQ8OmTePdvKmRy+U4E33tWit++UAAAAAAAACAMfPy8lYoemZDvfvuwGPH8tAUZ57rT6fT37ihMBo70XgjCDec2sabuHFDOZwctIuLi7e3pxZ/8tFp29v1Op0O5wcRABMGf8NBkqT50/S0adSJ6ghfGE1mAhr75JM927a9uXjxYpyD7lv4+uuvHTuWf+LECfywbGqSXL9+HY2OXiGlz3ruuWevfXSgWMKMWP1IBFN6pEZhzgMb9EqFgSmMmDsXaZBBLRFflmo04hqF1/L4tdGKgmteMWsX+yiKxVIDMihqJYbVMetWXfy4SCGMWTvXh96X+6AJZs0SMul0nyDqz6y5c2kag0JS0yCtqFHiVdZWfFog8YpOXCnS1B5qgowJAAD0aG9Xe3t7eXjo8WshfnFsamrqpHRotR0WNaurf8B/PT09cRoa/5sxY6ZerxeL63/8sREBAAAAAAAAxsDb27uqqhKZZn+Wy2UGw5QfOsdkuuPsM/64gSYGTmqbGmcymR5DboVOp02b5tXS0tLR0YEAuC3w5+qbJvg2/rLEz89PLldM+kN7khPQ+/cfWL582Y4df3zlldTz58+bF+IvqWg0WknJv9EYGZpP/mWn4LfPb9z2wUZ8V1379fuZRxp6j7i09OjJ5tcfT932OL4jOfJK6ke1mtr9mTvozz6XlvU4HSkqCv6y41PTFQqVF784cHHWC0nb5iUhvfhihULv1dMIM2j1y2+v7p28OiApdR7+j3jvS6/klu7N/Mgr9bn0LKr5axdz3v14Mmb+AAAAB9Xd3X39+g13dwbOOP/0k2rI+m0mOO+Mb/v4+AQFBd93X7RYXHf58uX29qFXBwAAAAAAAAxGkqRCocA3/P2FP/7YgKY+nHHDaSU0wTo6tN7eXvYT0ARBuLsMvVz0AAAQAElEQVSTo59RFoAxw9984DMQ56DV6q6J+EHA8LkQBB2Nmb+/X3NzCxoVLpf7xz++vXz58iNHjhYUHC8rK3v44biUlJfmzp2PxgmNKfDx0l+TKIeb7adxBUyDVGkxYJkpCAryQdKaBinMpeEcAgOnNze3DlnN39+3peUaAgCY+Pn5DPOBc+2abMhqbm5uarXKaDSikXN1dQ0KEs2aFapUKn74oQKnp9E4we8UWSwO/DJuco3l3LAP4usIIL7ODeLr3CC+zg3i69wGx9fLy/vee6NOnCig0+kPPfTIl18eQiPnSeHS6bS2NtWETjjr48Mf5ieR4VQbO/sbcnFx8fXlQ/YZOAiRSNTSIkWTZ5JHQGNKpTI5+YXY2NgXXnh+166/mRd+8skeNH4MGqlkRLNfGJRSK6OVNdKGysmMFQAAgH66urrq6+vwv4CA6QsWLGpvb6+svNR3BRUAAAAAAACAfT4+PteuUSnU2bPDamqq0cjh3DOLxVIoqDfhbDYL5121Wi1yDCkpL6KJkZ39/pB1vL09W1pGOVITgHGHz0Zv72k3bkza5+XJT0CbFZog6llvFv5S9MqVOgTAFGSa6J1GEG40GlzZFjg6/GRrMBiMxk6dTo+hKaup6Sr+JxQGzJkz32g0/PBD5Y0bo714AAAAAAAAAHcMHx/fy5drEJWKCf3ii4No5HACWqFoM/+033yVF8dJQGP/r3T8f838f3N9hqzDYJAdHVqY9xk4Dnw26nRafGZO6M8U7HCUBHSfmppaBMDU5OXFNf2aqRu/4uKX3m5HuM4oALa5uLjQ8NclBEGn01ksj0n8LnRcSCRN+N9dd/nPmzdfrzdUVlZcvz70HCAAAAAAAADcmVxdXXk8/nff/Ss8/J6Kiv/CB9hxRKPR9HoHSsQDgExD0Gg0OiSgAZjCcBYPf9OrVLZNxHRpAEwQ/BYTJ2rxP3zbYCB8fPg4Bz3VL3v900/N+J+vr19oaKinZ7SYUo+/6UUAAAAAAACAfoKCRD/+2Mjlevn7C7/55ms0Km1tKg6HpVJR1+Jjs1kw5tcMpwjU6in8G1PglHQ6nYcHE41QYGCgSBSEb4jFDY2NjWi0XBEAYGzwSwuLxZTLr0P2GUxd+OzF5zCL5YG/q0eTx8XFZVxKW1tbzp4tKir6Fu/OqlUPxcQ8MH363SwWazjrmpEkncNhu7rCq+QkwIfd05ONQ9B/4XidG2YQ30kE8XVuEF/nBvF1bhBf52Y1vv7+/g0N4kWLYr777vTgVYYZ37Y2pUaj8fLi+vjw8WeKjg4Y+UGh02k42YfGHScgJERAovFGTkyzwMHgcxKfmSNaBWefly37uYsJvoHvotGCp34Axsrb20ulakcATH34TPb25qLJY/93fyMtbW9vv3SpPC8vt67uikDgu2TJ0kcfjV+8eElY2M98fHxIktH3+WfwuhpNB373PLlH446FD/vNm1ocgv4Lx/fcgPhOIoivc4P4OjeIr3OD+Dq3wfGdOXMWzgg98MDSU6dOWJ21efjxVSqV5t8gQva5j5ubW2dn57CqkuEb9+5NmccRLM04mL0mgMTZ4DUfVsr6NBWkhFO5Yc68jXvPl57/178u/nA6OyGc07+JkIQPzxdkLhX0LhAszb44qAFz1YBV2afPf0htp6fqgpS9F38wNXv+w/XzOAg4L3xODv9aZQsXLnj66SfN2eduE7xw+fKleOHChfejkYMpOAAYE/xNb1ubCgHgLPD5jN+eTvX5oC2Y5+VApsuETpvGw8LCwj08mB4eHvh11GDQ63R6/BcTi+ubmyXmtfAbaAYDr0FOyOAFYAM+4DgQ+OD3vTfy9xdi5tsGg5FGo966dHZ2ubm5mpYY+g/b77vbr0LPKoiaKFwC8Z1cEF/nBvF1bhBf5wbxdW6D4zt37vylS5eVlZUdPfrlVJ+Cb8rzDJhBSk9LkSA8QFf3ZZv5kSG9sH39E9kXb6UaOAvSMjd5Hnxm3u6L5NKtezMzkyqfyK40lZMhj25NCTmXnoAb6UWitgtZq5/IOG+RrBAsTEmd37T7mYIm83bI8FVp6wMKXlqw/TRalfn51pQHT2882ASPTmD6lUNo6OySkv+4uPT84kEuv47/e99994rFDWjkIAENwOjhF3KDCQLAWZjOaBpJ0nFOFjkd/FGnLxltht+F03uQ+P8ajQYBB4ODIpX2vJvu6uoyj1vvu9H3Qbe3Qqerq5vVmuamEHAwEF/nBvF1bhBf5wbxdW7Xr8v/+tdsrXac52tety4BTaTTp08h58JZkP7hzoSFAYylny9EggBBm2fKhWcym6zUZHgKGNIL5yql+Lubi6cvShcECBgIqXrSzwHntqeekw5aZ3r4PLLtysUmVd/mNqYuVOW89GVdb4qZ5Mwg23B7TbjZ86crdUkCT4SaEADo7NlzDz648siRoxbLcQL63LnzaOQgAQ3A6PV9qw+AM+nu7iYIwikT0IN1dnZ2mAwucndn4ER8e7sagdsIf0nAZjPxwTdfHhNRP+pU4H9ovEF8JwXE17lBfJ0bxNe5QXyd2+D4/vhjIxpvlZU/XLxYhiaSv78vci6q8xmpOwSZC/NStkvXvJeKMjd+WKkjAxDyDE/58HgCThNrpecyX0ovaNJKK6WeSxeGcy5eZIQvnSfQ5UnbkGnyDZx+vrA9/Rxn6cY16PTeAlNumcQJ6/CEjMxwqef8cPT1lidS85p0nPCktKRwjpT8sDQNXdixceOHvSOsOfM2Zi7VFVxEMIUKGGzhwgXmWTjwX5yVRqMF6TMARg8noK3OlgXAlNbZaWQwGHf4UBUm0x1n4Z1sKpKpAh92FotpeoKdqLMQ4juJIL7ODeLr3CC+zg3i69xuQ3zBqHACwgWqyqtaz/BwsilP2jsyWdd0OmfHl9RcGDqceab+c/Hgjq9Xffp56forUnIGpzL99BWdafTzphkXtj9xugnNS0lIQHUHzQnotqavd2//kkpHkwsy8nY+ulBQcLAtPGFNQGXmxo3mSTwyUhNOr/+wZ9Q0KfAkpQgAa0iS7EtAozGABDQAo0ej0ex8e98lnN4ZEdnt5Y3ok3Q5Wb3ORXHDraLcVXIVAWfk7u5OoxBDXkmgEyeVjUaDwXDz5tC/szMYjGz2yK6N63x0Ov1wjhWYCF1dXSpV+/CvjzEKEN9JBPF1bhBf5wbxdW4QX+d2G+ILRmFpxqfZ6+cxpJ8eTxUEeGrDM6+2vfRhJS7QtlVePF1wsf8MztLzGatCMjgL0j9/T3Uw88tKnGjmCMJnCAScjM//tRXnkAPQl711VZV5pmao1a5IUQhJDprEo23BjOmeyJx1Vp3P2JiHBGvmMxAAEwUS0ACMHn79tnVp4K7pgZ0LYlwvlbn++zyarFHSDEaXj1/nogfQ+SLXq40IOBH8JSSbzdJoNFptR3u70f4lqpHpAgI4T+3q6srn81Qqlf3pNXBr8N4UAAAAAAAAACbU6R078kKSKtO3nJu/MzP84Mb009Sszp4263PmJaQ9iL7ckmNOTasqc7ZsPOdJDXgjZ6zfemsGbsHS9IxVdTvSDzYFzF84HUmlKh3SSq+2Ceb3TeLhqToobUM61RWd5/ql4YJz58gFS8PJttNtCIABdDqc0XLBeQLT39GDBDQAE6IzItKt/IJL06QOPdZqXX9scOnqxJ0ZawKa7h8ZLSJl1WXV8smZGHjSO+BISJKO/8nl14e/Cs4pm2d802p1HA4bv3LAlccBAAAAAAAAE4jhe9+SgJbv/tNkOSKL4M0IoTXVtFDLWUFzhe2XauTGwevbKXISpGBGALr6pRQFhHBUlVdvfUITzN96vH6r6ab2wvZVa7KpAc9kyKMpSeTp9A/P946MVtWdP11nusVpW5qypm916YWCcwnvfX4+3VPg2XY6fb3pAoWVe7ML5md8/kMKVeFc9kt5VJuVBTv2rnrvw4vrSaRrKtj+0tdN8DERDHTu3PdoPEACGoAJ0e3JdWn5Cd/QvvHHzp/dY7WO2w+XGG/+fu7/3OPF5VqtoFAqS/97yVYFc+mahVv8+bOtrt4sq8k7t9PlWmv33PvQ8LBDH0reEB8pYiNZdX5Odm5JT7aXHRa3fVeqsHhrfPIB8cQmgHEXEuM45Xv6tj0eHaD2K2VT/JJgUlaeuyMj66vqdtvbmhh0/4fSdyRH6vLf2ry7pB2NHkmhq1QD2mCz2XFxcQaD/ptvTrS3Dyiii5ZvSIwRUt+K6+qLcvYXNuN1TTno7jvkMoMAAAAAAACA24/w8uMzeEYvoqnFlEImWEEzhGx3mqFD4zItiMt25yuuiFFEGF9bgnPN990/0wu1t1RcknFn+rkbZVfEhLkIl917Dx+pZdXXp87Hl87OTjc3N/zXfjVd3d715nHLGQnn+xY25W0Mz9tovfaCvdZbUp1PXbq0392LezdaVsUJ5vQ1BekWK0rPZyfMy0bgTjCcc7K/6urapUt/PnBZd3V1DRoVVwQAmAh0EhmpV1lb2ee+IlvZ574iWxXMy21ln28V6fXDnYSatzgtKys5ht1cUiLnx2Xs+WRzFNtc0l6+f3Pik4lbc8UT/ZJP54jikhLjI/kDF4+pA+yozTu2x/Or92zP2F/FS8zYlhjJtrOtCUHnR66ImRMcHB23OJiNxoLNZvXPPgcEBPz2t7/9+98/bmtrwwllfGPz5s133XXXrRVk4vKiouIqFBobF8PjmJeZctCcISfuuP3sX9ZgskqBI4D4OjeIr3OD+Do3iK9zg/g6twmOL8Hi+xJGwo/P6hn5iD8fe/G5LC6fTRj1clmLgsHnGhsqqhSIRhIMQk1dYInF9WSyWQzU0WFUm4sIBp+PmqoqxLKpNBBarzeQ5CRdCwoAG/A5af5h9DAdPPi5Vqt16Uer1R08+E80KjACGgDQg84PDuWrvtvxu/QDYiQS67bHkRwSJ6+jEjfFBVOvnZJiWX2zKQPMjnwseTlZVc1ZEh/DluTuzj5cLqda8F+cuHlDLDWAuty0sN1cNzGWzxdG8qsKv+PHxnHKc7L2FDXr6f5R8YmPxUYKUXPRgV37C8U6/6jEDXGRoWEcDrk8OcNfpVOV5e4+XGWtA/0Ga+vEJ02rt9veL1GoEFXt2L0H71ehWLJhsUqHN55kZVvl7XgXNmzeENN/F+j+MYnrQlVi3ZzYWBEq35+966tqMvKxDbGcov37S5pxft8/NjFJJDuw5yvb6XGOKDqUrP+uhDNnTqSQXl49ykS+u7u7RnPrutX33nvvr3/9q9zcw3/5y1/MS44dO/aLX/zit799+dNP/1FRUYGX6NvFZVX+aZtCxVm/2n7g1obx2zsPD4+ODse6Doz9nPhklQJHAPF1bhBf5wbxdW4QX+cG8XVuExxfwovR+u9zLX4zuQykVFNLtFojyx0ZCaP6KuFpSmC7TQu9f+E9AR10Q0OXeS1XNwbOUzFE06e188OoIkJ1Qc0Imrs4TP1D5bUuNEUYDEY6nX7z5k0EgMPACWiDQk7CQAAAEABJREFUYQQJaFz5/PnxmX8DQQIaANAPSc0vr1JROUrx4bQnD1PL6DxTCT80NiaGLMr9SiynUrqh8YnJc1RVxVVyMiw+M4ujS0z7ShW8YUfWZmF1bn4JJyoxI4tPLWxGfFHchkReSX5zaHIqr7AQRW1KTSwp24WSsz5I5JQXlqv8o1KyIkWbN2yvste1AR3A6efE7TuSgyXFxWISrx4VmrohzVb6Vy+rLq8nN2xI3SDPzv2u5EBmCZUqj7JWlR1K7UIYbraZE9a7Cyp+VPyGZKGkrEysIiM3ZH/A1z+5TcKJTEyJlJVsyKkmw9albI6TbM+x0322MCqSoyovLOSFpUSF8vdXN48uA02j0bTaWynj5uZmb2/v4GBRaem069epKaHx3enTpwcGBkokklurcfh8jjB26wds9Pzm3hx0Z2enh4e7oyWgAQAAAAAAAE5B2/DvMvyfln/3LTG2/Lugpec2NV9lA3Xnx33Vlmv2Xkmpubeo/kfTf/z9fdEUgTN3cF134GjwOTmiBPT4ggQ0AMAuvbwk560SeugmUVTigAJV1f7fJe+uJqNez90VuySMUyiJig3TfZeetvWrZnpo+/79SSsiOV81m6/OW52fW6SL5MlyD0t4sRs4bKSrzs/cXCgpKW/WsyO37N8TFxvGKCzMySjzfygrKox/clf67t7Buu2DO0DnR8UEq05s/9Xmw83If3FiYhiift9kI6nbXr5raxpn+/a0XcfSkKpsz+bkHWeaS6xsix5q2oXtz+NmSapX8dQuFFFFsuLszZu/auYs35GbFRkjdNlelFu8aWtcTHCuhIyNEapKdpXIbOeUccZ+Dl9XXVxeLpSRidGhnMPNcjQaNBrR3n7rp2e+vr4vvZQSHR317rt/OXv2bHc3iolZfOhQbkrKZpyDVigU5mp68eHNDxdGbvokKzZSmFttTtQbjUaCgJcAAAAAAAAAgNP6v7k+aDJotTpvb667O4z4AY7Cw8ODJMkbN9rQJHGs7MNdd931008/9V9y9913478//vgjAgA4GJXKdH1cnU5nGjtNpYBJ/pKtn5zYjG9zhBxShmxPeqXXIU5YfHrK9mAOSfKDOToxGgm8EtLp200X0Ws+k5N5xn719uqvtq4tzBJFxSanbk1M31z05NYiaxlgKovd26xOjveL3rsLunbTFfvkJbvSkvmqep1eXnS4SLXjobg5VSSVf84uababf44RcXQSTmgoR6XjR0YFs0/Kx3Ihwl7Xrl3Lzs7KzT2clLQhOjraxQXt2bMnPj7+//7vz//v/71i3rboofTU6JKM7UUIAAAAAAAAAO4Y2dnvo8mjUCj9/PzE4pF90gVgguCz8aefrqHJ40AXIXz++U3ffnv6yy9z+5akpm45daoQ/9u48TkEAJhwpoSy+VIJvMh1qVseixzJ9fLw2jpJ/tYnV6z4xYol94cFz33+q2ZbddmRm7ZvX8cp/EPiil/Eb95fZc5lj2hbiOy5uCLdPzJmcSiPbqsunRcaFRMpYuvl4jO5Wbu/U/FDQ/l0e82a71jNnreLS86UVMupXHTZ4UKJMG5TcqxQVpRfbm9EM0e0JIyPOFEbNm+KDSZJYWSkkI5GxWg00mi3vjhksVivvPIK/l49L+/LwMDAu+8OPHToCzqd/sorW9hsc+z0EnG1PjJ1f+GxrERUklsi6c2TEwRhNE6l63gAAAAAAAAAnB/BDfBjWV2OhsdgMBLEhE9/gTeBN2SnQnc3kssVvr5TZtoQ4MRw9lkmu44mlQONgP7ppxZXV1elUmm+m5Ly0qZNG7du/QOHw0lLSz158tTIvziicYNmibxwokevENc2KMc40QlNEL3uuWXM4v2fnmrQIACcjl4mEav4sYlJseKv6PHbtsaTuSU5h+mcyOhQPlsYxiE5ONMbi+Sy6lKVtdVV9c0qTmhUKO+7EhSdsmMTPz9j6+Fq69ui84VCDmrW6XR03pzYKCGH7Hl463V6vY7kR0bFLhe2t9eXlYl1/MEdoC5GqOLHJK6Lrc6RRKbvyhDlb1ibIbc+BpkUPpSelaja9avkPVWcsKhgjq5eprO+LdMuxOAj0HySnfhYGCnbQ00hwre+D/Ky/Pz6xLQosn5/fpW9/DNbGBXKkeSnrU0rlNNF63btT4mKFH4j3PTeJl12Rnnc9nWyzLfq122LK/9D8u5y+wOjDQYDfp7su9vZ2bl9+/bPP//nww8/snLlShcXtHr1mgcfXLVt27Z33nmn54hWH9j88IHBTZneME3a9E8AAAAAAAAA58YKuvcePlLLqsUo9B4/wthS1cSe6YeMxvYr1JJ+RdqWqhZTEWq/esNv6cowVHWu6LLRy0Wm5PKNTWreTD93o+zK9eFdg7Cjo8Pd3b29XY0mkrs7o6NDa78O/sDV0YFEIlFraytckBBMCg8PD3P22f73JbfB5CegAwICNmxI2rZt+5EjR3/88ce6unq8MClpPU5A/+EPbxw4cPD3v/8dMuVK0EjRBDEv/u/G2T0jDdXioo/+8sFYcsdMYcS8eVxFwYFTDQgAJyQv2pW1X5S2YVfuBmrS4/0Ze4rl9OCk9F3pc8yjgYOTM6ORrjjj0W3WBiw3l+zKKtyxdU/JBuqeJHdzSb0eIetDfa8X5+z67t2t2SdiVTJJvUSl62tQXrwnp3D7pq3ZsbiN/RvWbpfFDu5A3IbcXVm5orTkXYXJiJrWOW1Pmc3MbXtVTsau4O3Jh8rT8D1ZWW5mdqF5GmTLbW0twruQL9qavCs3GekkxXsy91e1255HRF9fcrJeF4aKvrKbf6YLI+cIddV7qqi0vV5WXS0j46JnTvuOzxfq2BwOj89HbLZOKOTLhx5vfvNmB5/P02p7DlddXd1rr73+y18+/txzz/7jH/vwktzc3G+//ddrr70mlUrtN8VisaRSmYuLCwIAAAAAAACAcUbgDzpNVRUKRPLDUMvlFr7IxwN/OmtSeAUI/FFv0T1cpJUTbE8PBlKIFXwRu/VS2SWt+t/VbX73TSfUWraX0U2mVHR4hQXwrv+oHc6GNZoOb28uTuHgBLHR2InGG05P4eyzaTpd5ZCV9XpDS4vU29vb3d2jq6tTZ9LZOf69AqCPm5sbaWK+Mbkzb/RxIYhR/hK8P39/v+bmFjRybDYbZ59xrvmXv3yirKy8u7sbL0xLS9248bmsrOz33vvr66+/hiv8/vevHjqUO+LWaf6PvJO5WrIz5d0K2qzox5OeXcUtfmPLBxUwfBmYBAZOb25uHbKav79vS4v1h6ufnw9O4Vkt0idton3xGb6h+efXyDbmLx9ctiTGToVT3xXZqYBLX1zzsZ3V3897Fv81PP4kPWc3Gi62f6gQSaqbRzdJMZ0tCosUks1lJeKhGqDzRGF8Xf1ot4RMXQ0mZVViuX7ourhjwUKdZAxbG9SiaN2e3DT2/g1PZpaPvFHTYa6vV/Fxr+rrdcJgvqp+ODtCknSSZKhUA0ah4281H3xwFb6Rn/+VVjv02zL83KvX60zTWlsnEPDtnPbDfOBcuyYbshp+RVSrVY42GQhBECwWB94XTq6JOzcgvo4A4uvcIL7ODeLr3CC+zm2i4zvw8wXBu+f+MC7DXX3pv8Z7/scPoZYfahn+Lk0yfkB3s3Z6cE/RzJkMrbJF3B60IAwpjerqU1WM+34xh6g6f9k9bCYLIXX9VcbPpjMIL1R9oV47nE8imKurK5PpgdPE/ScwHC8GgxGntjWam11dwxuSbcJgkHQ6DR8o/BcHAgEwYfAzLf7mAz/SdTqDTjfC+U4nzCSPgP7Vrza89NJv8I1//ONTnIP+4YeqxMR1OPvc2tqKb/j4+CQkPPGHP7wxmuzzAAZl7Zn9ObPmvhk+V8isqMUZaOasZetWxwQJmHqpuKRg//EK8xdXNEFEzMpl0bOEXvjLt9JTBceLqRHTNOGyzS+vFjFpyKCRnHw/82hD/9+t9zRFu1ZaVKq/f5Xo+4/+dkbiFf3C88s0p08pwpfdL0TiM4e+OFWrhF+7gymhvbm6Go2avl1cfmZ40+Xo5WK7UycPDXe1fLh1ccfGsl+D0YUxcaGofnd+/ahS2r2Huec/4uphtmJ6V+fC4bBVqltr3Lx5c/jPk3hd3Iid7DMAAAAAAAAAjI1RfulM75XQC1svmW/8hP/fQA1f/LH3ekHXTBllRoBfa1XVfxpM02acPyIxFZ3pTTb/1Gj6j7//cOdTxqnh9nb1RM/CMSJara7vl6wA3IEm+SKEWVnZL7zwG/zU8LOfRZizz9u2vZmR8VZc3CMuLi7m7PP+/QfQeNDrFRpEZ1IDvmlBj7z25otRzGvFp4qamRHPvp7+zCwmtVy4/PnXn5uLak8dOnRK4rXs5W1blglpOH+tllZWYA0agShIyOo/ZpwmXLXlzRcXeylKS6WC5YlroyOCfPAaNJpAFHH/qnWrRZqKixJW9LPvbFtn2gQAwGmoSrI3J6ftrx63IdXDZfrZlp7P57m7u9PpdFfXoafRcHV1xTXd3Rl4LfPPvpBDsj8lyGSVAkcA8XVuEF/nBvF1bhBf5wbxdW6OFF9t0797ss8AAKc0+XNAnz9//pe/fALf6Ms+5+Ts3bRpI4/H27MnZ7yyzwPQBPNighQn397xt0oNQidr9X9OnxstzK2tRV5BPkhScOjIaYkBFRef3tu7hrLi+N4KnLeOF81dObApr4hokab4b396t0SJ0PcS+p9fDuot0ysqDv3l3dNShE6J6dlpERECWm0DDIK+47j9cKnzZ/fYKsJ/FUqlF9f69XwVpmty2qpgLm2W1fjzZ1tdHRchMHH08uqSM2iS4AyyTKZzpzAIgu3mNsS3iZ2dnUaj0WAwOPi8z+aJmBytFDgCiK9zg/g6N4ivc4P4OjeIr3OD+AIAbpvJT0Cr1ery8v+as8+ZmTvN2efU1C3mTPRdd93V0tIyzk9tdKYXk+4lWrn+hcXUXZbQi4mX4Fsa8Zli6fLn3nkn4vtaiVRcWVxcKhliwmi8Jk0vUZhrGRQajeFWilmvUWp6buAKs7zodFwFgTsM483f269Q+t9LY6mQd24nAneqDpMRrQJDUQAAAAAAAAAAAHA7TX4CGvWOfc7Kyt69+8OkpPV92WdclJv7xYEDB7Oz30MTRy0pKii+KKGmQ9VUfPpqSmXMssXREYuXr16b1HT01S0fD+Oihb2pZTqi0RAA/Wnf+KOdEdA4PT33f+6xMwIaZ59tVTCXrlm4xc4IaEhPAwAAAAAAAAC4/RhcLkFdIF2rtn2VdAZPyKcpW1rUjnVRcgDAeJv8BPTatfE4+7xr1+733vsrzj6np79uHgcdERH+xRf/JAgiJeUlXG3sOWi6l8AL6TV6PdIb8P+kFUc/2nt58IBkjaS0YG9pATVR9MPvvPPIslkHKkrtZKA1CgXyEgV50So1BppXUJAPHTLQYABb2ee+IlvZ574iWxXMy21ln+0XAQAAAAAAAAAAE4YREPVzkUJyvaOtTbNhLFYAABAASURBVKtXNEmM/EA+w3hTz/CZhlqqalqorDSDP92L0REwl1FWquAF8Ym+aiqVkcOxvHvzphYBAKamSU5A4+zzO++8jbPPO3f+OTFxHc4+40Tz7t0f4qKGhsb165M++2xfVtZ7eXl5aExo3IhlG19cxmw4UCQxIIO0oka5Ombd6oqPCyo0otWpaas1Oa9knpIyo9Oy0oKKM179oFSJvHyETKQxTa5BE8yaJWTS6T5B1J9Zc+fSNAaFpKZBasBNFZRo0p/bmR1dIWUKBUy9fujx0gAAAAAAAAAAAABOzKhQE35+09rcuvRsP9TR5MU2ysj/mWWsqNb5+bFaTNccJPizo/jo6neXWHw+m8/rreYaOpOm6mRb3L35Y8UwN+3q6spkUhfModHGP+tlMBg7Ojo0mo6urq7hr8VgkHQ6jSAI/NfNzQ0BMGE6Ozv1eoPRaMR/tVodcgyTmYCeNWvmH//4zscf/x1nn598MvHNN//3gw929Y10VqvVJSX/3rv3U5x9bmpqQqNE91n+v58vNzVYc3THn3IbqPywpnRv5kdeqc9t+yCJKqg9siPrlNRAXWvwyFHxm+u37Vtl7kLNkZ1HxBrEnLn65bdXB/S0GJCUOg//R7z3pVdyGwxIWpyVknwmeq4/XVq7Vx/zetosBAAAAAAAAAAAAHAnM8qbFLPvmTYN3XTtkOG7WFcHEoaF6WWXrvTUaVeKO5CRYHnxeXw2o7cag+RO4+tdLe5eG95mcfbZ25ur0+lv3FAYjZ1ovBGEG05t403cuKEcTg7axcXF29tTixOBOm17u16n0+H8IAJgwuBvOEgSf+FBx194TJtGnaiOcNHQyZ+C48aNG4mJ63D2edeu3X/+8/9ZlG7fnoFGzdB8dMvao1aLNA0Fb71wkikQeiGpRNo3aFlTm7slIXdQO5c/ev6Rj5BNGknpKUkpvsGdu4qOkN5g3nRi36YNtZ+mJHyKAAAAAAAAAAAAAJwLzsO6ulpc7VzbUFqGUNmlW0uoBHJT038H1Dlf2GC+2dB7o6eaxVrULX9/XzQMTKY7zj63t6vRxMBJbVPjTCbTY8it0Om0adO8WlpaRnr1eABGDX/DcdME38Zflvj5+cnlCoPBgCbVZCaga2sv44xzWloqvr1nT87OnX9Gt5dBI20YhwkzuLNWPRITxKTRBRHR87wke2sVkxxUAEaJFbI2+akItvmOseHYrn0X5FauBUFwIxOSH53BsFfHIXHD1yZEK4/vO9k4xqnDpuwRAAAAAAAAAIBxhxPQLi4uyDHgjNuNGwo0wTo6tN7eXvYT0ARBuLuTYrEYATBJ8Dcf+AzEOWi1umsifhAwfJM8AvqDD3adO3cOP0/997+X0FSnby4tOFN05EwtzAINpih13aGd/3sIp1dnL4+bbyyuUVrPqxqV5fv+WI7TuQkJkYNLCRaPS6jlSu3gAi4LqZUDLm9MLTOqldoBG2JwfakW5ON7IWSCG758EbfxeP7Q2WeCweUytBa70L+r9o+A7XatHgErh2tijgAAAAAAAAAATBCttsPNza2zcwTTIk8QGo24DYk2vAn7E0zjTBef7w3ZZ+AIWlpaRCJRS4sUTZ7Jn4Lj0qXhziLvqJS1BZ/WIgCcA8Gbv2ZNSOvJvLONI/7FEiNwecLaaF+kRYS2Jn9ffqU5g80NfyrpAYbayOLyWMa6/H2HyqkRw4Qv3tADgSwqnVtzMu94JbWQEbjyqYT5PKPayGCoLxzad7zOVidYgfPDGY0XauSEb+R839YL5a1288pUUv0BXmP+UOln3FrcmgdCWPiram1d/sG8SptdtYYb+dRTs8v3HaxU4sOYsDawfN+hSrXNI2D1cA3/CDgn/C6t2/b0VJNVChwBxNe5QXydG8TXuUF8nRvE17mNb3w1Go2397SODke54hmWkvIimhjZ2e8PWcfb2xNn/RAAjgGfjfgReuOGEk2SyU9AAwAcCTX4l+E7f2Uc42T+yZElPwkGQ1mZ99d9dUokXP7Uymhh3fG+dK+x8XjOSQkKXJm0cr6wBi9nzV40n3Eh590LcuS76Kk10YF1+XVaBi9ESFQefDe/zsgNjAxhMAhkaxCwWq7kJiQ8Fd5K+DJq8mqGSCub08/Hj0uIwPnzUU15o41mWSGLornlB98tbsW7kBS3KLAxr05NdZVVvq93obmraKQGHQGrh2sER8A52f+UMlmlwBFAfJ0bxNe5QXydG8TXuUF8ndu4x/fGjes4w6XXGxxhHLTZrlPDvHLhCCQv8xmyDoNBdnRoYd5n4Djw2ajTafGZqdVOzrdEkIAGAPSnrju576/f8uavTVgeXdN4UjKC7KdRWVfTOjv8gZVcBkvIZSlZfc8vRqNarsY5WwL/BwVSywkGi8Xizl60kqdFDB6XgVg41arVKiWtaPmiuLgQZWtjZU2dvbmV1XXfftuY/HSkuvDjYon9fHBP+nkfzqcLo+fPJ1rLbYzuJhi35siQnPx4V89CVt9C3H9itqmrI8wKDz4C1g/XSI4AAAAAAAAAADgUnINmMpnu7gxETQx9534JQaPR9PoxXnoIgHHW2dlJo9EhAQ0AmGzU1MNI3qo0GpWNjcr5QhZ+1zD8MdCEb/RTa2fLi4tr6owsQujLGGoFrbq1roYaI11XWa42z3esrsnf1cgLnD07MnJlUnTdoY9tjjUmfOfHPcCt/PI4I3LlSnnecVsTVlNVWb48FpexMuk3pmmYjeVoIhH9nlXtZY9tHK7hHwEAAAAAAAAAcDgaE1cTNK54PG80RdBohFqtRwA4Ep1O5+HBRCMUGBgoEgXhG2JxQ2NjIxotSEADAHoQvPlxa4WVB/cVy7nCQJyKtj/5g9FoJAjGrecQnOdlaCUXymtajYyQ2YT9JxejVq3Gee7Wxjo54oZEhrCUElMPwucHqivLy89KJFpWQoi9scba1uK8Solci+okgSz7HW29kHew0TTAGO/i8kh7vVKqicgQX1ZNnVa4KCmO9+2+vDq1Vq0leNTCRkIYwsN5894uWR4BXKRG3EBfVqUa16QOoJ3csfXDZfMIULOILA9Xlx8/e4dNCg0AAAAAAACYerpM0J2KTqfhZB8aCzIgJEDXVCe9HaNVb+e2wOTB5yQ+M0e0Cs4+L1v288bGH/FtfOPUqX+NOgcNCWgAJpbbD5c6f3aPrSL8V6FUenG5VivgIjsVzKXNshp//myrq+MiNBJGSfG3lWvXPPv7B6jbF/KK7V/XT42zpygheWssQgbJsV05F1rLG4mEpJdnK9VqnHk12s+TqmvOXgiJS0iORgwWIT+bV0llWY1qJRGekLwIJ3LVauWFs3W2hzUblRJJT0utQ10ukUp0myfaJ7SBD0TaedpT1509G75m7ctbtGqjVnLykKlldc23xbPXrn05nUBGeWX+ob6JrQcdAXnj2bOtT63d8ntcKL9w6HirncS41urhsnkECG7I7IgIo7K4uO7OmhQaAAAAAAAAAKYYNze3zs7OYVUlwzd+mMrIfumgZ1r2mgupqXlNOsGClMz3UpYKSKRrKtj+0pa9F1VkQMLegsxwXZPKlCRuq9yd+tLeK4I17xV89GjPlNTac6+veuLDyn5JZDIk4b1P17elr089Le1dFLAqc+9WRvYTL+HtUAusbAsBJ4XPSXxmDrPywoULRKIgOp3e/4qjy5cvxVlssVh87tz3aIRcCIKOxszf36+5GS7uCaaYwMDpzc2tQ1bz9/dtabF+4QI/Px+pVGa1SJ+0ifbFZ8gxGB5/kp6zGwEwbAIB385pP8wHzrVrsiGr4dc/tVplNDpWVp0gCBaLM9y3jGBiTNy5AfF1BBBf5wbxdW4QX+cG8XVujvnee/hCQkKG+UnEXC0l5cUJughhdvb7/TdktQ91dXVoOASrMrOXnk7d3rT0vVTP7JeyL+rC13++d31l+vrtp9GqzM+3emav2XhQKkj48PM1555Z/2Hd4GHKONGcsXONbnfq9oImXf+lH366UZqecCv9jARLMw9mCPY+s3GvuRnS2raaYCC08xrmgwhbtGjhgw+uLCn5j4sLam+nRsyxWCx8+7777v3qq4Jz586jEYIR0ABMLO0bf7QzAprx5u/n/s89dkZAl/73kq0K5tI1C7fYGQGdd24nAgAAAAAAAAAAgIPhLEj/cGfCwgDG0s8XIkGAoM0z5cIz2WgG2Xbx9MUmnQ6dP12pSxJ4IiS13ca8je9lLL2SmZp5umnA6OdHt6YEnNueek7ab3MbUxeqcl76si+JTXKsbKsJAYDOnj2HE9BHjhy1WI4T0KPIPiNIQAMw0Wxln/uKbGWf+4psVTAvt5V9tl8EAAAAAAAAAACASaQ6n5G6Q5C5MC9lu3TNe6koc+OHlTrOAqoI55Uzl+oKLqJbE2OSMx5Ny5zRhpPHuqbTu3ebRzuTnoLpnp4zHk3PZJC3RkCTIQk4/Xxhe/o5ztKNa9DpvQV1Ok54UlpSOEdKfliahi7s2Ljxw97ZNqxsC4BeCxcuMM/Cgf/irDQarXG+JikAAAAAAAAAAAAAAGAonIBwgaryqtYzJJwceBVAUuBJkgMrk1Ya0DUVpK9Z8PP1B9Gq1E3zOOZ6IY9u3TTjQmbm6SYkWJqQsHQ6XpMTnrAmoDJz45pVC37+UoFgU2pCCGlnWwD0IPtBYwAjoAEAAEyI4Vz22uIaCP2vbzDYZJUCRwDxdW4QX+cG8XVuEF/nBvF1bo753vuOOnOWZnyavX4eQ/rp8VRBgKc2PPNq20sfXjEVqc5nbMxDgjXzGX21dXVfZqf2v8ogKQifF6CtvFinUl05f74pKXy6J3lepaOWzxAIOBmf/2srvh2AvqQqMzwFDOmFc5VSnQ5dPH2xbcGM6Z49M3tY2RYA4w0S0AAAACZEV9eI3zjaf685WaXAEUB8nRvE17lBfJ0bxNe5QXydm2O+976jzpzTO3bkhSRVpm85N39nZvjBjemnVTitrLqi81y/NFxw7hy5YGk42Xa6zcbq1MUH3wvP2/jM7ivTFywI0DZJ20zZaVVlzpaN5zyp4arkjPVbE0yVtdKrbYL5C8M5Fy8ywpfO81QdlLYh3bC3Be5YOp0WfzGEH5qmv6MHCWgAAAAAAAAAAAAAAG4rUjAjAF39UooCQjiqyqvmsc26yoIde1e99+HF9SQ1wcb2l75u0lmdfQOpLu7OLHgvM++HFJxfrjyYnn6uZ1JnVd3503WmW5y2pSlrzMsq92YXzM/4nKqMpOeyX8qjxlJb2xYA/Z079z0aD5CABgAAAAAAAAAAAABgfHR2drq5ueG/9qvp6vauN49Pzkg4f2ux9Hx2wrzsgTWbDq5fcHDQ+tQE0AXpyDbV+dSlS+1VtrIt4KyGc072V11du3Tpzwcu666urkGjAgloAEAPhnDls0+Fy/M/PliD5ickL2eczck522pEwBGxQtYmPxXBNt8xNhzbte+CHGIFAAAAAAAAAJNOrzeQJHnz5k0EgMPA5yQ+M4dyvf8/AAAQAElEQVRf/+DBz++9d767u3vfko4O7cGD/0SjAgloAEAfo1qt5c4W8lqJEJZare6XzyRYXJZRrdQOSHEyuL5cQi2XD6jIYCCtFjFYSKseUNlqC9YRDC6LUCsHrG9jdQaXx9AqByy21ivbLVBL0aBt8agWlNqBy1hGpbW1Ldu0eQSs7+toW1DXHdr5v4cQwZ29PG6+sbhGCdlnAAAAAAAAAHAEBoORTqdDAho4FJyANhhGkIDGlc+fH5/5NxAkoAEAA6hblazwyEjEUMq1hPn5gfCdv2bNA4EsnJ9W1pzMO15JDbRlBK58KmE+z6g2MhjqC4f2Ha9Ts2avTXqAaNXyeEZJKxIKtWf35ZWb0qJWW7CGG/4UbkJp5PJwVlhyct/BYmoAtrXVCd9FSU/NZxgRg4Fz1eV5+/JrlFZ7ZXMXTNtiqI0sLs4s1+XvO1Ru3q/lCWujfZEWEdqa/H35ldQOMISLEhIe8EVKnIBmMOTHc/Jq1NbatH0ErBqHFni4hZDWk3lnG9UIAAAAAAAAAIAjwJk7Nzc3BIAjwefkiBLQ42uSE9BMJvOZZ56+//5okUjU2tqq092a7Rwn5n19fcViMU63/+Mf+zQaDQIATDSjsk4dsijcWHeh1TfEtIQ1e9F8xoWcdy/Ike+ip9ZEB9bl12kZvBAhUXnw3fw6IzcwMoTBIJDatHbNt2dZKxdpi7+VLF/pyyUQlTylWmCV73u3GKdUlyfFmVuw3QPJyZwcidFcszKPSmxb6YCpprx438ELcsbsNU9Fh/vWnW0lrPTKiOx0wNh4POekBAWuTFo5X1hzvFFLMBjKyry/7qtT4ppPrYwW1uGFrMDocFT88U68gZC4Z1cSNg+LzSNg1dhbQAwul8Hwnb8yjnEy/2Qd5KABAAAAAAAAoJ/kZT5oMmi1Om9vrru7e0dHBwLAAXh4eOBE640bbWiSTHICevXqR1555f9dvFiKc83t7e39E9AsFgsv/Omnli1bXmlraztw4OCIW2f6zxLRr9U0KHvz+0zhTCFNKr61gCZYlvpOEvPIH94+2jAowc0UzBIyFeIG6aR9PQDAbUYQhFF+4SxO1EqUgXGmBDTBwI9F7uxFK3laxOBxGYiF07parVLSipYviosLUbY2VtbU9Q5ppv5jNBp7G0O9LfROcqGWq4nZphZsJFWNRlxF21PTl4WbsN4Bqq7W3KhaUl5cSVBLbPTKegdubYvA/0GBLKq3OP9e0zo7/IGVXAZLyGUpqYV4dUa/1Y2+Ng+L0cYRsH6sx9wCNQ3HyX1//ZY3f23C8uiaxpMSmIUDAAAAAAAAAMyys99Hk0ehUPr5+YnFYgSAA8Bn408/XUOTxxVNqvvuu+/EiRNPPEFd9TM7+69PPvl037/s7Pfwwl/+8onCwkJcDY0cTRD94uupibOZvfeDVr38vy+vEtL7KgStfDFRWPthVkGDleHVTOEjL7+5eZWIhgAYA7cfLtkvUiiVtiqYi2xVMC9vltm8AqmdIju0rZXFxZXy/kOUterWupq6uprK4ry8k3XmTGxN/q6P8y9I1KzwlUlJK0MYaAIY7XSgH3Vj+YU65Xj0ivCNfippeaBRgrdV19qTJMfJYCPBMKeCCVa/jLD9Xg3HWFpgcH2p4dFU0ryxUYm4rAkJAQAAAAAAAABMKQaDkSAmfPoLvAm8ITsVuruRXK7AWT8EwGTD56FMdh1NqkkeAR0QIMQ+++wf+Pa0adP6F5nv4qKQkJAff7yKRs4gra1RxM+eJaBVNBhwutkrKMJH03BI0pdsNjQce+PXxxAAE0GvQ3Q60usZb/7efsXS/14aS4W8czuRfVQ3dGi0jFq12mhUtjbWyRE3JDKEpZQgavLh8PmB6sry8rMSiZaVENI7etdGC1qCF+LLqmkkhCE8nHW1cyFCgmD5chkIJ1R9udQl+Iw2OmB9ZSu90hpH0AG8cYZWcqG8ptXICJndm2tWt0rUD8yPDtc2EiGBXEJu+7CMxBhbIHjz49YKKw/uK5ZzhYFcZLrmIitw+crZrWcrWdGR2uILaH40o/x4sUSLphAXF5du/E7NwUqBI4D4OjeIr3OD+Do3iK9zg/g6N8d87z32M6ejo8Pd3b29fWLnKHR3Z3R0DPFZy2Aw3LyJRCJRS0sLzMUBJoWHh4c5+2z/+5LbYGpchNDVdVQjtTWS0gZNzLxZXkeoaTSYorlCJNkvVuJctHDZ5pdXi5g0ZNBITr6febShb5YN7qxla9fGBKFrxUW1uLivLeasZetWxwQJmHqpuKRg//EKpdWiUlMRzNkBkEubslvg6yIZzXcn46vbxxd3Bo2auubshZC4hORoxGAR8rN5laYpItRKIjwheRFOoqrVygtnqQHILNstfFs8e+3al9NxklpemX+o0c6rNM44c6MTkuO4LNT67SHTpfWsdsD6ylZ6NaIOaFvLG4mEpJdnK3EDWtyeudnW4rx87fyQQJ68VaIUMmwflhEZWwtGSfG3lWvXPPv7B6jbF/KKW/FOcbk8X181o9FX6KtlsYy+vlQKfmqx/15zskqBI4D4OjeIr3OD+Do3iK9zg/g6N8d87z32M0ej6fD25uJcDU4QG42daLwRhBvOPpum0x36g7Zeb2hpkXp7T9PptJ2dnToTfAMBMGHc3NxIE9MNxuTOvNHHhSDoaMz8/f2am1vQyGVnZ+Enl82bX66ru/zSS5sLCgr6ih58cBUuDQmZ2VcHjZxg2Rt/TtS8/8rOYiUz4rnM12cVbHn1mMSAuBErV0cHMb1EMdHcojde/luFeVQ0TfjI/+5MEjYUHS2SCKJjoiOEiiOvpu6tRUGP/O87SYLak0eLJT7Rq1bO0hx9441Pa6mVaKai3lVWLZul6CsCji4wcHpzc+uQ1fz9fVtarD9c/fx8pFKZ1aKu6YGdC2Jc/1vqeq0V6SZpDCrDvcvHt+ueOW7ni1yvNiLHxw1PeCqyZt++8jEkzCcSg7pcIXE8J79xSo0qHg2BgG/ntB/mA2c41UiSrlareie9dhQEQbBYHHhfOLnwu6UJOjcgvo4A4uvcIL7ODeLr3CC+zm3i4nt7hISEDOcjBjKNYmQyPXCamEYb/yE5BoMRp7Y1mptdXV3DX4vBIHFnaDQanU7DgUAATBj8TKvHX30YjHq9sf/F9ibXJI+O8/e/q28KjpSU3zz1VGJf0din4MAU4spr9GVzA5jFGsGsWUxpba3CNDpZWXF8bwVOHseL5q68VZsmmBsTpCnamfFuKU4gfy+h//nlIPPyeTFBipNv7/hbJV5+slb/5/S50cLcWpxmpgki+q1SVGvY+XpvEbizUQnfrq7OiMjOOfMRnUSTQq9zUdxwO/utqwMMxJ7SGCFrfvN0JBuh9qbyk/lTa04LAAAAAAAAALiz4NRwe7t6omfhGBGtVof/IQDuVE49BQc1DXRFrTp+1iwB81pQhI9evL/ZXmKYzvRhIo1CrTevq9Doe5d7MeleopXrX1hM3WUJvZh4iZVV9IprGhTlxUQAYDjtC5nfkVFWHvxrJXI82rq8nW/kIQAAAAAAAAAAAAAwQpOcgG5u/kkiaTZPwZGd/dfBU3A8+eTT5ik40OhopBUNmpiIWcJr4UJ9w0nJeAxMVkuKCoovSvRWC2H6ZwAAAAAAAAAAAAAAADBzoCk4zHNu9BmXKTgQUoovSlBiVMz9PnTp0QaF3bp6g96AaHREN+eR6bR+y/XSiqMf7b1ssL8KjU5d1xCS0AAAAAAAAAAAAAAAAIDQKKe2uM1GPQUHpqgtvcaMWDaXe+1i7bWe1DBNMCt87ty582YHMel0n1n45tyIIAHNoKiVGHxi1q2a6y8Iilq1dq6P+QKNBmlFjVIYs271XH8mjRux9q1//OO1ZQJaXxFeZW10kEA4d1XiSpFGXNEEE0ADAAAAAAAAAAAAAADAZI+AbmqStLS0/OY3KXV1l69fv96/yHz3ySef/utfsw2G0V+kFWeVKxT02QEKca20J//MDFr98turA3oqBCSlzsP/Ee996ZXci18cuDjrhaRt85KQXnyxQqH3MlXRlO7N/Mgr9bltHyThe+raIzuyTvU01luUnvU4vnftYs67HxcrEQAAAAAAAAAAAAAAAAAXgqCjMfP392tubkEjl5i4Li0t9YcffoiKirpy5cqNGzf6iqZNmxYSElJSUhIeHv6nP+3Yv/8Auk2YgqAgHyStaZBazKVBYwqEXkgqkcIIZ+cQGDi9ubl1yGr+/r4tLdesFvn5+UilMgSA0xEI+HZO+2E+cIZTjSTparXKaBz9t4wTgSAIFovT2dmJwORxc3OboHMD4usIIL7ODeLr3CC+zg3i69wmLr63B84RDecjBjL9jJ7JdMdotPEfdmkwGDs6OjSajq6uruGvxWCQdDoNPxDwXxwIBMCEwc+0er0BP9LxX61WhxzDJI+APnLkqKen5/33R7e2tmo0A/K6arUaL8RH7YMPduFq6PbRSBsqpdYKDLgEcs8AADBhXFxc7Fx1drJKgSOA+Do3iK9zg/g6N4ivc4P4OjfHfO899jMHZ5+9vbk6nf7GDYXROP7feRCEG05t403cuKEcTg4a75G3t6cWJwJ12vZ2vU6ng29iwITC33CQJP7Cg46/8Jg2jTpRHeHJeJIT0DjpjPPL+B8CAABw53F1den/ps3+e83bXDoR71bB8FkMDIH4OhmIr3OD+Do3iK9zg/g6t4mO720oHQ4m0x1nn9vb1Whi4NPY1DiTyfQYcit0Om3aNK+WlpaOjg4EwG2Bv+G4aYJv4y9L/Pz85HKFwWBAk2pqXIQQAACAU3JxQSP65RoAAAAAAAAA2IEzbrch29vRoXV3Z9ivQxCEuzspFosh+wwmCz738BnIZDIIYpInfoEENAAAgMnh5uaK37chAAAAAAAAABgnNBpxG8ba403Yn2DaxcWFz/dubR3WpNUATKiWlhY+fxqaVJM8BQcAwPExeEJfQi1pVZqvVUGwfENmB3KRsrGmrlVNLSO4wtkhpiV1NRLlOF/Rwrw5HlIP1TjBnf3AA8LGk9/WqW/bRTVw54Q8FoGMamWrXKk1jrontxqSS1r7rTUZO3Ub0em0GzdUCAAAAAAAAADGW0rKi2hiZGe/P2Qdb29PnPVDADgGfDZ6e0+7cUOJJgkkoAEAthGskAfWrIz0ZSiL9+WcbcU5UMI3OiEh0tgqR7zoSN5BvJAxO+6pOKFaIkeR0dEheTl5deM41xYjcPlTa0O0EmpzQzRu1KpbqeTtbUzUErzwlWsitXUSIy8whKc8mXPwgtw4qp4QXF/hbKEwMIRxYd8+UyNmk7BTt4ebm6sp+3wdTR0Mv4j75vqqS8+UttgetU1wA/jGppaRPgZYQXOF7Zdq5EYrDc647/6Z2rJvSlsHFRK8GSG0phpTdyxa6F80bLa2dWunbPdz6oP4QnwhvlMXxBfiC/GduiC+zh1fR/CHxVI03radEQxZh8EgOzq0MPMGcBz4bNTpUR2kNAAAEABJREFUtPjM1Gp1aDJAAhoAYBPBDQxE5Xl5vssX9S5i+QqNNfkHjzeiwJUJ0b4spOQG8pRnDx4spnLECWtCeIw6tZU3ZQzf2bN9GQRhlCsRj6VtrKmTa3F+WxgyW8g1yutMd6ktUksCeUiOK0jURoIr9DVWUpsz8iJXRrMYBMILB9Yxd3T2/OhALlK39n6bxxKGh3C1RgaPoZXU1Jir4T6Ehwi5SNna2LtozIzKurMnT0q0rJA1Tz0wm1derA2x6ElPZ1haLQvvuKR3HPfAvdBKys9KagJX8hb1P/rD2SkrR8NhkCR98EJXVxf8F7/yTbWxz4RfAKvp3PcK5MYNvXemu9HY3iA2zgjzI7QtFVVaYZifu1F2VRGw9KEwVHXuX5e0Qeai0oaeD0sMv9mmOlcuNVkuERMRYXxtCd7EPXP8EG75ihgFzWQTBGoqvSS/cqnaaya+jRhB994zoE2CzQ/yY7vzFbi+uQX8CSbCtOK1G6wgganoUm9lbugcG93GHQjFLRtbKv7duy2j+SOWTMnlu3bwF67s2akZvVu511S/qok909zh3q1MXRBfiC/Ed+qC+EJ8Ib5TF8TXueN7R6PRaHo9TDYIHEtnZyeNRp+sBDTMAQ0A6IXzzZGLFs0PZBEEKzAy3JdhlFeePFnZ2v91U91Yo/SNXhQZuSjaV1nTSL0pIoxGLWKwWATSGo02vtQiGL6R8wORljd/USBCIQ88EMKiRjcnxEVyjVpW+JqkNeFcarzzyoS4cIZazQiPS1gZyKDWQ0Y1NbWFUV6en18uN1qpg6iBwnIJ7gyP6rSpBzgtG/3AokguMnLD1zwVh7eGGCHL1ywPYchbtbzwRdGBrKGPRXggd7jf0REMHovQ4o4O6om5M/MfeCCSh7SM2XEJ5s7gfV9p3ouVCcsDrV67Ylg7NYx2Jo9arRr8T6lU3LhxXaPRoKnHiLRqpVJH0AiF+EqL1oPnx0VaLcFmkR1KRQcjIIAtu1R2qfTM+Wq1V2/RrZj01OH1LSEYVHFHh1HdUFGlQDSCwOd7u0zB4At8+AyFrB3X6HcGMviD2jQa5bIWXJ9r7GmB4dW7YndvEZMbOPe+OUFct8HdZvZ0wI3PRy2XWxCf1+8MIty92Ax3BtvLtbVnp+TK3q301vfx6Okw18FOvdGB+EJ8Ib5TF8QX4gvxnbogvs4d3zsXjUbo9XoEgCPR6XT4qxE0QoGBgUuX/hz/wzfQGEACGgDQgzV7+fLZDESlhR9Y9ED0bJ617KtRXVdZR4QsWhSC8I3eEbcM30UJax/wtf8mCb+3lLcq1XK5XKnFbwVJXoivsfLbby+Un80/mFcsUSOCF8IzVp4tLi8vPltpxHesdMBGHZyrbWyUKPunyrXKxuILFy6cPVtDDT3G1XB+WKtVatWtF/IOnRxinhCCG748bs3y2UNmoBm+89c++5uXtzy7iKg5S/1yzkpPqMNm6gzVZy0Xp7XxXggJeaNcrcZ/CKHVPR3OTg2vnUljtKarqwtNTe1a7swlsb+4Zxp1lI3qliapUk2dyVqFgTMzIoDPNY1s0aKAexfMYHb0FPX9HIDB76vTgzB9/GGJpk/zDb1/4T1zFsyd7k59CMP0SpmRHzTDz/w1iZEam7PsPh+9ZZvmQsxtWk8Lvvp+K5ofnZ3KxtJ/lzUoTZdhGdDtjs6eDrA68K7Nm+GlpSZ7MW1LiL/56dAyAoICGPhx07NTff307+qt39m7FfxIuOe+ENZU/lUVxBfiC/GduiC+EF+I79QF8XXu+N7J6HQaTvYhABwJPifxmTmiVXDSedmyn7uY4BtjyUG7EAQdjZm/v19zM8ytDqaYwMDpzc1DX5HW39+3peWa1SI/Px+pVIacBcM3fDajsVJCCCPnhxCS8gs9M5ERwuVPLdce30fNAU3wohPiWGcPnmykEtWL1PkHy1krE6IleYfKlYgbuXaNsPhgfuPgnxoRuCyOV3xSHhmNist5y6Pl+cfk89c9oM47WNw33xkDb8i8xDSbB+vbfd+iRX2btlXnpKRnc4zAuKcWtR46eEFpNE1VvZL17cGTEqOvqfcHcRMESxgeHR0ZHiI01hzKyasZ82/abm1l4B7378mAasaePp9FDyStFcrNc2YY5TUXyhuV5sHdi+T5B/vNAT3ETl0glltpZzwIBHw7p/0wHzh1dXVoasKfH1gsjk43aWMWCG7IfQtD2U1nTl0aWURHveIYEazAGXx59bj+UJQk6Wq1yjgBM6BDfEcK4juyDkB8Ib7juuIYQXxH1gGIL8R3XFcco6kV39sjJCRkmJ9EzNVSUl6coDmgzRch7NuQ1T4M99MQGb7xw1RG9ksHPdOy11xITc2TChL2FmSG65pUpgx2W+Xu1Jf2VnouzS74fN108zraC9tXrcmuRCHr9x7PCG9r0iFS13R6x5b0vLr+WW8yJOG9T9e3pa9PPd17GMiAVZl7tzKyn3gpr8lcVTBvfUbm1kdnSHPWr0w9DZeId3LDfBBhCxcuEImC6HQ6Tj2LxQ14SVBQIL6Ns9hisfjcue/RCMG3aQCAHtrWynLTjcYLOL9sHcGgZtqg5sSg/hIsBmHUKhE1/wRSIhaPYVRqh/tuxmhUGxk8LoHkyHf+ykjt2ZM1WrW2ZwmXx9DKqaaURkJI/SLOGLgSJ57z9xVbqTM8BIvHUtecPFT+Lc5hrwzkMWrUt29OLoLBNQ1ewH02yqlxwHK1El04ebzRyA2JFBp79sI0p/NInpWNWqvtODT8itXd3T21Sm8/o7Lu/FejSd+PesUxMqobqyd4lkKIL4L4jqr09oP4DgbxRRDfUZXefhDfwSC+COLrYKVOyDNgBinFCWJBeICu7ss2U1ZYpzqX/cz6Dwdmk1HbhazVT2ScV/VbhJD0XOYz6/dKA9a/93laytLzKQV9GXcy5NGtKSHn0hNO30rCCxampM5v2v1MQU/2GaeoM99brzu448CaBARAP/iRGBo6u6TkPy4u1G28RC6/jv973333mvPRIwUJaACATQQ3PG7NIiGXy/dCCc+G1J3NO15TWaleszY5EidKtXUnD7XilGf5WcmauGd/Q+D3ZjUn81qHmwPtlNeVy8NXPvsbqqma44fUOC1bebZxDV6ykmrq+Lc4U0vUVcojVyb9Btc3thbnya3UofrpO39N3HxfFo/P0iYlz2+9kPdlo5WdCVmZsIinxWlvhrYmTz4h2efBPTlU3Gre+vy1ycu5LNR69gK1FzX4oK2kDhrer7OHzIl/rby8xogP7nyjFq94TBL48FA7ZZRba8ex2X836ZilwBFAfEeCwWIhtXoqXfcG4uvcIL7ODeLr3CC+zg3emU86zoL0D3cmLAxgLP18IRIECNo8Uy48k9lkewXG9PB5ZNuVi00WI5VV0itXpFpBvyWm9HPAue2p56T9NrcxdaEq56Uv+zLbOip//fUV1fyMNQiA/s6ePffggyuPHDlqsRwnoM+dO49GDhLQAACbjMrKvJxKi4UXDu26MGCBuu7kvrqTQ7VUfnAfdaMxj/q7r9G0tDzv44EpU3XjyX27Tg5cb8g6VO71wqGPB3YKte7L6blxMse0ZSQ5m7PzLBpPOCfeuxU7PaGeZ43qxoEzdVjZC2oMevHBXcV9d+XD2Cmr7YAJw/ANDTBeuSIf4msWgjvjvvtnasu+KR32FzKm1agLozfVtGiHvV2CG8A3NrWoR9PmMDcxcHMz5t7rp63496VW57ykt6PFd0Sd7HcyEH6h93Ab/l1t/k3EgO2yguYEtFdUW93U0KfTFOcI8R1m47diwQqaK2y/VCMfSVfMLTj5o3Uwx3r8Dvu5t7dXTv7oG7s7M753zgN5Srz+9vZhrI/WO/D5GdilOp+RukOQuTAvZbt0zXupKHPjh5U6MgCnj2c8mpY5gxoOrWs6vXt3QZOORAzP8ISMzHCp5/xw9PWWJ1LzTIlqDlVzIWdGuOeV7H4zbYQk4PTzhe3p5zhLN65Bp/cW1Ok44UlpSeEcKflhaRq6sGPjxg8vqpCqqRLnsgUIAFsWLlxg/l0C/ouz0mi0IAENAAATTKuWt2qnwvQYwA6CFRQx04vhx2iRGoNm+RHalqoW9kw/ZDS2X7msFYb5uRtlV8RE6D1UUUXppWqvmQSBGPzQQNSi5PqhhmrzxwzC7545eC1kWmtm31p8pJaJFWw2wyswlKVuMQaFmdtp0PZtt6H3AxLDb7Zpc1cVAUsfCkNV5/51SUvVN7ZUXWbMnOmOu/STlPDqpLZL7/IKmMZ291NcEaNQU52KSz29FV9lmStfFRuniwZugvp4FDrHVNogNs4wdeayjB+z5B6iqRQxg+6dazoC4p7N9dW5dUzw5kw7VU3d6NkXR86tOE58+1oQX2XMFPU7vDi+VUhkqixVIV6XTMnlG6mmzI379ZwM56vVfn4M2WUlI+jee6i1cOAC/MzngDE06h6e7FwFovKa95r35TLq7d6tFuRO93TlMPE1Kq/0NI56A1RR1ftg6e1J/4f2jDC+tqQ3XvgcaOrt9qWeB9TghyrerjFg7s+d99E6mAM9P1ORMtVv5wfhxx1f0deBvqfchstqX8vG/QY8mfeP16UryoHPDFTo+06eS4P3borFbjjuiPj2PZDxEkbP87Nzv+z2ccD4Xr5qeZwrqiyfn4suG71cqBfibhkxXWT5JAzPz2BEOAHhAlXlVa1neDjZlCftm3ODtKzY1vT17u1fUplkckFG3s5HFwoKDlLpZl3blXOnz5E6waalCUvDv67ESWXT6OdNMy5sf+J0E5qXkpCA6g7i1cIT1gRUZm7cuPsiuXTr3ozUhNMWk3wAYA1Jkn0JaDQGrggAAMBEMiorjx8vd76Mzp2GzycUV1tkRleeHxdptQTb04OB2mUKBp/LZLBZDNTR4cbvKaLmLTfRKtTsGfdQFzTvHeRCEAyk+ElB8HluHUpFByMg4C5/PmqqqhDLjIjhGzZ3BpJ1eN1qh+jd7q0TiOjZnKbpUtml0jM44ejFRy2XWxCfx6QRCvGVFm2nsme7mptGZctVvLm7fHrrkD3b7atM8gZtgtpKT6lH7/7SZFVlly59/12pktPbPaZlnb5jIujdqcHHxEE5THxvtUD2Hd6e2Pn491TuZnixGe4MthfHp6fxvpNBbmTw/IiWFjWD37PWNNeec4CnbfrPuUtywp1Kfvbui7f/4BaQE3Kcx2+vvgD1a6GnTbasNxbKhooqBaIRfZV9+rrd94Aa9FDF29U2OfWjdTCHiS8VKXN9o1Eua6E6MOgpl0CWjfd7MreMV99QoVt9I26dPDzbe+dU7oD49j2Q+z8/O/nLbh8HjO/g51XS8vm5jdbzQswgrTwJ9/YJnp/BMCzN+PTDTQuXpnx6vACnlNekZ26cxzEV6Oq+zE41Sc82z9esqsz78MMCKmGsk16RUklBcxM6aeW5grwPU1/aflGw6tEZptVJQfgMgWBpxuf/On/8vUdneJoqMjwFDCNS6IkAABAASURBVOmFc5VSna7p4umLbYIZ0z0RALcNJKABGL3Ozk5X1zF9BQSAA8JnNT630ZgR483VdTJfs7RGbsDM0ACGi1qtxZ3RKjR684UjkRvBwJ8YWaLprI6eIrXWSA1vXHafEMlwjoAlk90arkLgT0FhAV5GvdfMiAA+lyA61VpG0NzFC2cy3bTyy1Vyvoir72sHGXu32z8NYd4clzBqUcC9C2YwO7TcmfOoj2FU2Izqlia5ume7GmpzM/HmNG09dfq2a2qMqizVWG6il6lUeaszPUvbe5foLOv0HZO+nWL0HpNuv3vmzL1vztx7AlnIETlMfPta6IumVNkTu7beSLlotYyAoACGFofV3Dir92Tgcv38kKxVjcPUe1a49JwDPTNymD5r9wWx7bplC3eFOHakRsdx4ot6GvfR94a1N4jevn2PzZ5YTPMNvX/hPXMWzPXv6vcYt/INgfWHKnLWR+tgDhNf/Ljrrd/TATrP8ilXPahx1q0nc8t43fpCqO+ZwXjr0d3hYrl3Uy92w3EnxBfdWnLrYevcL7t9HC++pguHDzjOBo7l8zPT0PNCrO1Edp6E4fkZDO30jh155wrSn1j5RMbpc3tT1qynZsWwTrA0/cPMhBASkQHzF05HUqlqwBUKBTPmh3AQTi5T91SVOVs2vpSavn379h17L/QMq9ZKr7YJ5i8M51D56aXzPFVXpG0IgCHpdFrM/BeNgQtB0NGY+fv7NTe3IACmlMDA6c3NrUNW8/f3bWm5ZrXIy4ur1Xbo9QYEgBOh0+kMBkOhUFot9fPzGeYDRy6/gcYVzoy7uKCODu3Nmxo0kfBbfBaLo9Pp0dixQhbcYyw939j7Ws0IuC+CqPrPhP+A0nK7Uw9J0tVqldE4/uNxHTu+Y2yBYPn5EjKJ0sphI3ih987ja6v+XdbkAKfFnRrfOwXEd7w5Vt8gvs4N4uvcJi6+t0dISMgwP4mYq6WkvPiHxVI03radEWRnv99/Q1b7UFdXN2RTZMj6DzMCsjdmkykfJtWlv3SQGuFMBiR8+HnCuY1PfFjZP8fMmbd+53sp8zieAs+20+nrX9pbqcKrf35850LzQOZr57JSXso83TRwUg3Ogsy8DJSxJvW0igxYtfW9jPXzqOrSc9kvpWSfl5IhGz//11sL+0bXt3390s83HmyCiTmc1jAfRGZvv739tde2DmfhcEACGty5xp6AZrGY+G9HRwcCwIl4eLh3dyO12nqSd/gJ6OG/sI2Im5srnU67ceM6mjDj+QEJjNbU+AAMRgvi69wgvs4N4uvcIL7ODRLQ42I4CWhfX/7Vq1fH5XelAIwXNze36dOnt7bKhln/6aefam5uHris29/f/x//+AyNnGNdhDA0dDaHw7FYqFKpqqtrEACOx2AwkiQNAeBcXFxc9HrH/WzQ2dnV0aHz9p42oTloAAAAAAAAABgdvd5AkuTNmzcRAA4Dn5Mj+gX/wYOf33vvfHd3974lHR3agwf/iUbFgRLQX3/91cyZM6wW1dZefuihOASAg9HpdEymO51Og1k4gNOg0+kEQahUt+kXjN10AtHcXGzPpd7d1Y0MnS56y2Ea+EHHZDI1momaiwOmd590ExoCiO+kg/gCAAAAwIkZDEb8wQoS0MCh4AS0wTCC5BWufP7892icOMpFCHFOHWefly5dHhIy0+Lf8uUrZs2aOW/eXDRKNG5Q+NyIIAEMVAUT4MYNpacnXDsWOA9PTw4+q9HE63ZxQTyWC4/t4umB2O62/uFSXAd5M7sHZpQ6O7sYjAFXAqfmh7ZtpKUuLpavjwwul8Vg2L/6OIMnDPBjjfirXQYvIIA38BKALL8gIddz8HITghsQxGMMuktwhUF+E3VNGoLqpO+tfSNYPJ75HsFg2d7lvmqmfRzRobEIAcQX4jv8UoivhdsfXwvjG9/BIL4QX4jvoNUgvhDfYZm4+E70meP4cObOzc0NAeBI8Dk5ogT0+HKUEdA8Hh//vXr16v/8zz3JyZvOnj332Wf7zUWNjY34L58vQKPDnJWY9vaDAYqijM07iickq0ITLH7uxcWS/VlHayf2uljAMV2/foPD4ahUKgTAFIfPZHw+o9vCxcsD0akvBrtdEMH2wP/tVFlOp+4qYHZLNd34FoPu4tmNFANGEHR3I1dX166urt673XY2N5ZSE0ZA1M9FCsn1jrY2rV7RJDHyA/kM4009w2caaqmqaaEugsPgT/didATMZZSVKnhBfKKvmkpl5HAG322Um9byoz7esMP81KW914YjuL581N7+sxmMlhYjQ6lgh4T50QydBM3NqBBfVvBnBLg3yagPRri17k66t68bvouMSqVxupAlq1GP/7R+rIB7ghgK5Bek/ncTY0YAqTIKZgV0XDpfo+aH3sNtKa22OmQe93BGGFWt0SssiNGB/AK0/6YuD8TwCw31czdq1HqSofvpcqPaa3aYX99htA7iC/EdXakJxBfiC/G1APFFEF+IL8QXTWR8J/jMGYFtZ0abShobrVbn7c11d3eHS0YBB+Hh4UGS5I0bbWiSTH4COjg4uL6+vu/uY489FhsbO3/+/L4E9BjRBLNErGviJnpQhJBZrJyQDDGdK5oVRGcicGcyGIxqtYbP5ymVbZP4bRIAY0Gj0bhcT5x9xuczmnjdhJsLg7oELs4+ez4QYWhVIjcXguep+vaSC3JxnXkPNwrdPFbvumgWqryODK03G3TInexu17kYb13Ho6uru38CehzhZge/7zUq1ISf37Q2ty492w91NHmxjTLyf2YZK6p1fn6sFtNl1wn+7Cg+uvrdJRafz+bzequ5hs6kqTrZg+7Ki67gtbQtV1pnzGUrmm4decKdTRgVyGhkB8zwQh0svwBGl87Hs7utXcv3c2+6ckUxl8cg1F5+uDXE725WeLMYBNJSF5Rxn5jXdW17O/IT8dBlI9Iqm5rwtjTefF/8wSlohtDL3fc+7ffnzReeZwjvmYkuX5KYPukYlU0NMqoaQRCImjrMiP+L/zBYbAaDcPP1M1z67gctYvn50WQy1HcYzcxfMKAJAPEdBOIL8R3n+N5mEF+IL8QX4gvxdcz4TjrzpQIni0Kh9PPzE4vFCAAHgM/Gn366hibPJE/B8fXXX33zTUFo6Oy+JRcvXtRoNOfOnce3H3jggb/97a/PP5+MRo/mMzvcR115slTKmjXr1iwcNEHEsmdefv2tnTvfev2F+Ogg5hDLEXPWsmfT3sTL30h7YWUEt29p/JvZf8t+c91slk/Mi5kffPC3D7LfWB/BtNsUcEI479zaKvXwcGcymfhrJTqdBhNQAseHz1I6nY7PWHze4i/n8Tl8e7LPFHrP79EItoex7aZW3NJt7EI0N9pd3ojG9Agn9JcJj1kcV8EsXsJMV4XOYq3JYZQ3KZh8r2l8tunXmfjTiLGjA/mEhfnijws9ddqV4qtKLcHy4vP6VXMludOs36UwAu6LvYdo7z82RduuMDKQwcjwckdarVqt1SKjpu1ml+lrYzcWP2A6fvvAJU2tdbl53mW6y6B+rInbmZAYGuUNLVrFlUtNWsTgBgTwPPm+0/34fFY37l07tc3erWoll3o+HZn2rbeaWkswGAyjun/vug2IE3JPqB/DoEW+Aw7jpID4QnwhvhBfiG8PiC/E9zaC+Dp3fCcJ/lBDEBP+wQFvwv6nJ/yNuFyuwOcRAmCy4fNQJruOJpULQdDRmPn7+zU3t6ARuvfe+QcO7F+6dPnVq1dXrVr13ntZISEz+0qTktanp79eV1cXEhKC727ZkpqXdwSNGHdxWmYS+viNk3Nf/63g6KtvF0gMODcsXPXazvVexYeOFkvQrGVrV82+9tGrb5+SIFvLgx7533eSBLUn8XKf6FUrZ2mOvvHGp7Ua3FDU6lURAq9ZMTFBiotnKq7pDQZpTcHRMzabguGxDiQwcHpzc+uQ1fz9fVtahvs1EUnSaT0ImPIJOLjOzk78nslAMep0umGu5efnM8wHjp1q3R50Fy71tZwbx4PuP627s1PfqvCYI9JebjG2aBgPr/CeibTfnNXODKUbSBfJvxVl1M9XupUal5v6vkbww02tVlGjUsabaTy4l1o9idcMIbgBQkJm/g3pcDF4gX6otWFE6zgwFstDqVRMxM9KIL6OAOJrwcni6+5O4vhO0C9UcHw7Oob7mjUBIL4QX0sQ32GC+DqCiYvv7YGzQ8P5JMJm4w8aLu3tEzv0e5hbodNp06Z5tbS0wFwcYFJ4eHiYs8+3b7SZDZM5BUffvM+Di55++imcff7rX99/992s0NDZx44d9fX1QaPAFM0LoksONVwTI4n+2blBzAKJEj8DeAX5IEnBoSOncUK4uPj03t7a1pfT/Ofh/PLJt3f8rRKnQE7W6v+cPjdamFtbqzFISg59VEITPiyay5Uc+fhvpX0zfNhoCjg7nU6P/yEAgH36npk0jO03mb7BhmttjLsFrt3I0HLdBblojx37yVxceX5ADkl/m14y8ZvyCZocYNiMyqZGNEJaeWMDch4TNL8Kgvg6BoivBSeLr4sLmrj4TvbFqSC+EF9LEN9hgvg6gomLr0PRaDq8vbk4LdPRoTX2m8FvvBCEm7s7wzSd7tCXGdPrDS0tUm/vaTqdtrOzU2eCbyAAJoybmxtpYrrBmNyZN/o4ykUI+0tMXPfGG3/YtWs3zj7ju9XVNYi6FOHVUTTFFM4VsaRFYoVBQyuV0h+JEDHP4CSxRnymWLr8uXfeifi+ViIVVxYXl0qo1LGN5XSmF5PuJVq5/oXFVKMsoRcTL7G/ZVubAAAAgKipnLV66tKC3ajt2wrqIoTd3TcrfsTZZ5vrdOhcjLfp7TL+dNTZ2eXm5or/IjAZTAe/c4I+pkJ8J91Ex5f66TTEd/Lgg48/8KMJo9V24E9TEN/JAvF1bhBf5zbR8XUcOMmOU8NMpoe3txeNNv5ZL4PBiI8k3sTws/m4MoNB0mh0Dw8mnU6DX0uDCYXfaevxVx8Go15v1GiG/prk9nCUBLRcLsN/77777nvvnb9t25t79uTs3Plnc1FQUBD+K5NJ0YjRvGbNEnoFrU7LWobTyD5ePsxwIbO0FmegKz59NaUyZtni6IjFy1evTWo6+uqWjytsLbdoVS0pKii+KBlilKutTQAAAEDUfBo3EZ9wcXPFOehO1RA/lu/G7+2UN2/nmBmDweDuzpjUX/Hf0fDBx2+Z0ISB+E6uiY6v0QjxnUz4c/WNGyo0YTQajbf3tEn9Ff8dDeLr3CC+zm2i4+tQcGq4vV090bNwjIhWq8P/EAB3KkdJQP/nPxcuX75y6lSh+e6GDUn4X19pTU3txYulaMS8Zs0TaCqOfvgFNXUGXbTyubURs7xotRrqM49GUlqwt7QAZ6mDHn7nnUeWzTpQYZpAw8ryCoPeoJdWHP1o7+URfVqytQkAAAAuXd3oWls3nUA0NxfbF+3sxtUMnS76SZivqr1dw2ZTP9yDcTq3k5ubK04d4oM5rQhaAAAQAElEQVRPkuNwjQo7IL6TAuLr3HB8TdmNCb/EDd4EzmHhrzEgvrcTxNe5QXyd222LLwAA2OJAU3A8+OBDc+fOCQ//WW3t5f7LVSqVeRaOEeMGzRMi8aHjxaVSKnEsYS5b/SzOQB+V6KPTstKCijNe/aBUibx8hEykUVCZYa715QZpRY1ydcy61RUfF1RoRKtT01Zrcl7JPCXtSUcb9EqFgSmMmDsXaZBBLRFflmpsNAUAAKAfKrNsN7k8WTMFmicHMKfJcL6sq6u7uxs+Jk0sFxdXTK/X48OOekMwYduC+N5uEF+n49rVdWv+SlfT94g6nfa2ja3DaRQmk4nji6hhbt0ITCSIr3OD+Dq32x9fAACwyrHmgC4tLcP/zLf9/f2bm5vRGDADIoKYilM1ip48sUJcIaGtjgjiniqpOHJU/Ob6bftWmQrUNUd2HhFTH4dsLS/dm/mRV+pz2z5IohbXHtmR1Zd9pkhLj55sfv3x1G2P4zuSI6+kflSrtNUUAACAiYBTTjjJNI6l5oXmK4vi9+6Tfdkc50flCHs/hQ4+2hDfqQ7i62TodNrNm+q+uS+7TGxVHvf4mmlMXE0QmEgQX+cG8XVukxLfCS0FAExRLgQxDj+B9Pf3a25uQSN0773zDxzYv2xZ7I8//mhRFBQUVFj4zWOPxV+6VIEcBo0pEHohqUQKiWTnEBg4vbm5dchq/v6+LS3DvWYoSZL4IxlBEDQaARcWAA6us7PTYDBiej2VoxnmWn5+PsN84KhUEzvnmtFoUKnacP/ReMMPYQ7HEz+O+5bAm+Dbo3+WEOLrfCC+zsQcQfw6ggAAAIDbJSQkZDifRAAADmgyR0BbzPtsoaam1qGyz5hBI22A3DOwAX+u9vLyxOk8/FFXq+1Qq43wgzLg4Fxd8XeQFDqdzmR63LgxzpfH7ejoQBNpQr/j4XK9Dv7zUN/djo6bH+764OjRowjcLhBf5zah8XV1dQ0I8EdgIv3441UYVw4AAAAAAIZpkqfgePDBh0JDZ3M4HIvlo5/3GYDJQKPRvL25bW1tpgQ0AFMD/o5Erzfgf8h0Dvv6Cq5fvwHncJ9pwvAOfZcv161V2Ulo5H//+0cZGYHvvpsFORfnAPEFAAAAAAAAgNtj8ueAhkQzmOpw5o7F8pDL4ZrCYAozGAwymZzDYavVN/FtBBB1AcRQf8LV1cXY2fVTB/37ktLYXzxYW3v5+PHjCDgBZ4svnefPUTXLhzuZDgAAAAAAAADcLo51EUIAphwXFxdvby5kn4FzUKna+Xxea6sU3fG6u7u1+q5/12nNd11d3Dn+/8N0p3V3d/FitmQkClUqnU5WtH/XV9XtCEw5zhdfun9MclpM+Y6M/ObRpqDp/rG/WkeeyM4XQxIbAAAAAAAAMJ4gAQ3AmHh5eba1qRAAzkKpbMPfqYzLfNB0OjtsRQxZVljFiX04jEQcUlacXzh18rVdXd2dxu5u1K3tVLm7eRoQOv1N7jffnPCPW4bqD2zPrApO3pG8ojo1VyKMiVsRxqn/Du+dnO4ftWIOXUcKyfqiE+XNejovckVcbCSvueSrY9TO00X9KrNDH+o5MviuGB8Zdmhs3JJgXdmJwhLqLm4MVyZxLlRyIr9Ejvqtq/KPiVsi5CCVDHFQ2YmvquUW3aePpDKy6DYZunwFp/pYmcocwRK8YEDHnMFUji/ONseFyQoLq3X4xhxZ4QlV5JMbYkhJeb1K31tjYD8HbnpQx8w94fhHBjd/hwaePIPPFXu7jAAAAAAAAABgEFcEABgtkiQNBiPMVwCciYFixOc2GjMS8YNxdoxPcoJjNyTG+JOixIzt8SI6mhq6O7tQs7p6z5XEv9c9/ln9c/s++fO23ycHBQX1lNNJPg/pdIgXk5qRHIV0/vFb0/HekcLFiRsSIzn+MWnbN0ex2WFJm+P9xeXN/rGPLRHReyoj/8QMqnLvkQlNzNwe50+nh8bGx3BkqtDkjHR8lx2Vmrk5iiRD4xPj5wgtNsQWRsVG+fNi4qI4uHwOz6L3I6qMDez2NNyxWBy53ghadAw5gykdXz3iRMbHR/LYwUviY/hIp1c1V5WIOXNiwjg90bHop8WmLTqGN23qiShYyMEPfYu9sDhw1ne59/ggAAAAAAAAABgERkADMHo0GtHd3Y0AcDr43Nbh3Nu40dUXH971iWSJf3oozmpOhR/440e2tOPKkeZXuhB1Vcaij4uv/qtgV+6X/3z/vVqc3ItO2oqzedU5O05IOA/jpB0ShZIkhy/Ce4faVfX5+z8rRPVxYSqcwRSrOOtiY3RFuTknxEg4h6MqOvDZJzKJiDoUxT1HRrZClCrE60qqy8WiKFzA4Qv5bI7QXFmlCk0ldXS8rN+G6BKkk4nFiMORNHP8Lb8wGFFlswHdRvyBhbL+HSNR85SfomGKxxfJyopkcTFhYeJIVL6nXo/04pJizpz40H5VBgZ0YATLBnSMzeFb9GTAXiBZWOLWlFg+UlXt35F1Uqay2OWBxwem7wAAAAAAAAAMAgloAEaPRqNptR0IAOdiNBoYDHc0HnDezJzI7smf9aXR2KLIMFJSVu2wV0zD3y19V7xnmp4aD5u/91RHQ/fTbz98+adTnV04X6mTFB/YnllimoqCzkEqSeGB9F3l5l1hR5kb0DcXHW6mbhzeHJ/Pi4xN3pz+K136CXvbpIetTYlDOek7VA9nppBIr1PpyCh/Pp+N83py6tD13xA7KgbZNaLKfXq67R+MV6I2aYpg98COOYOpHl+9rLpElhgfL0Tl2fX2HkTmftIjk4cdwcHF7eX70361v++u2GKXBxwfAAAAAIAJ5e/viwAAUxAkoAEYPRqNUKuNtkq7hNM7IyK7vbwRfZIyNnqdi+KGW0W5q+QqAs7Iw8MDfwtCEISb2xDzKXXivBrOKxv0N28O/ZUJrolbRWOWmZnOIUuyJHoUTHLmrEvL4ARzSrKqqLSe/5JNGfHVqZvGc8pYFxcXO79IGGlpW1tb9uaP+y/5x2vHzDf84x7qt1gvKS6SZaRkR5IcsmxXanbZwJbZoesyMuJIiYpDyvbI2iWywvrNSVszEKkq3IUPxZIBlWX1Mk5yUppIxeeTJQjJv8vJjUzNyObglGihzmJDe+wOUB9RZStkVSWqxE2ZmcgcQYuOTQqI7wB6WVmJKm0rf/9+/ACj+8emZqbFhgn5umBRzJ4/pO6vtqhuN4I4vtUoMTVDJOEIcSnuycC9GGKXBxyfotF+pzS+8QW338RFEEqhFEqhFEqhtL/m5lYEAJiCXAhiHCbs8/f3a25uQQBMKYGB04fz6oW/Ym1puWa1yM/PRyqVWS3qmh7YuSDG9VKZ67UWpNWiScFgdPn4dd0zx+18kevVRgScCEmSHA5brVZ3dnbifHFX1xDJF1dXF1Oe2o3FYqlUKp1uiCSRQMC3c9oP84Fz7VrPo8M/7k9bQw+n9gwpxdgx6Vlx1RnpuWP6uT7eHbVahXcfjTd8rFgsDj62aJLR/SOjwoTCmPio8u1puXfY5AYQX+c2ofHlcr3uvns6AhPpxx+vKpWKiYggAAAAYEtISAgkoAGYosZnBDRknwGw0BkR6VZ+waVpUocea7WuPza4dHXizkAC2pmQJjLZCEYP4wy1Xm9AyNDRocWZa/zt47hO8TwEVX1hoUrSb3u6qtzM+nqYLHYodI4wLCZGJC/ZkXECjpbzgfgCAAAAAAAA7gwwBQcAE6Lbk+vS8hO+oX3jj50/u8dqHbcfLjHe/P3c/7nHi8u1WkGhVJb+95KtCubSNQu3+PNnW129WVaTd26ny7XW7rn3oWFgR23KSn9Il/uHtJwqTmzqjpTI5j2/Sz88mrwIPXRdZnpMVWba7vJ26xX8l2/dkRLFJ5FOJakuL8zPyS0az+uaDdkBxI5M2rEtMbhndhSdrChz81tFcisdjaU6ysP1VNU5W9MPVLejyWVKPtNVKlX/hWw2Oy4uzmDQf/PNifb2AV2ki5ZvSIwRmnZUUpSzp1CsUrVzOBx897bloNurT+YOmBJAL6+uRmBIennJ/rcma8oLMOEgvgAAAAAAAIA7gysCAEwEOolMv0u1lX3uK7KVfe4rslXBvNxW9vlWkV4/zEmoSY4oODg4Ov6hMB4/Mi52TnCwKJiDRoXk+IvCQoP5trdL8kVhQlVJTtaek+2h8RlZOxJDx2E6oJF0gB0cFszXictLKOXl1TKryVi9SlZWVl5SXo+EYaGiUR6OccXhsHEGue9uQEDAb3/727///eO2tja93oBvvPzy5rvuuquvAimMiY+L8h94JHD+2jQOGgAAAAAAAAAAAGBiwQhoAMAtOlm9hBMZOyeKI9LVS1TINMqW7r94w+YNMSI2kpXn7s4+bBpTbH2haPmGzYkx9PrCEs7QOW+dTlZWVHi4uUjMFu2JnyPk5FTLbWwrKj7xsdhIIWouOrBrf6G4HS+KSVwXqhLr5sTGilD5/uxdX1FDk0fUAVKnkxTt3p5ZbndMc3v54Z3lh9lR2yOjowYUWOkVO/Kx5OVkVTVnSXwMW2Lqv7y38uLEzRtiB+7XKHh4uKvV6r679957769//avc3MN/+ctfzEuOHj36i1/84v/9v9/u3ftpRUUFtZtUWMtz9x8QyyTVzbe2q1ZrPDw8bt68iQAAAAAAAAAAAAAmDIyABgD0115dz4laFx+qqxbrSMRBiB26YUfW5lieTiYnwxIzsrY/5E+3sTByc1ZWWgxPh4Jje+d8GBo7NDY+SqirLq5X2W72g7RYvrxZRUalZO1Kj8ULSX5U/Ia0rZvi/JGOjNyQ/cFWvHSkHSARKVqX8ckXn32ybV0Ub2QDsK31is4PjU9M3pq2KYqNyLD4zKx0qv+o5ximRZHikhI5P75nv0aFRqP3v3Jac3Ozt7d3cHAwjzfNvGTatGl3m0gkkr5qnODYzanp2/cf+yw1qm/YM26HRoPvIAFwBHSeP288fwMCAAAAAAAAAI4EEtAAgFtIUldfIuYvwbnScvMcw3RhVGyY7rvtzyc///yGzXtwdnpFJMfGwshIoeoEtfBXmzMKZUNvjL8i87vq8mOZiWGyotwSid5qs0gnyc/cvGFDclra88l4IR/X6ZkJQ1acvRlvLHlrvoQfGSNkj6wDOD/NEQZzZFRSOA4nheNEI8n/2OyVqmr/73AHNqTtr+dELjEt7NmvHWlbM3embt1dZd6vUSEIwmia2sXM19f3pZdSWlpa3n333U2bNmJZWVkymSwlZXNgYKC5jrzoD0vC5q54ckPaLjF1hHr30mg0EAQNTR66//Lt+78pLPwmN2td6ODpQOi8yMRte/Zsi+tL1tNF8albRhamicSL2pQeHzoRvWFHJaUnhkI6cnLZiy/dP2bD6zuyPrA9cxCusSl12Ccrrp2clrLCH2IOAAAAAAAAcE4w/A0A0B+pK8lI3pCDZPT4LNMQYpKawkHfrqOuEKiT63CuhBo5bH0h2btQp1Ophry+nU525gQhwQAAEABJREFUInXt5kJySfL27RvSU4vLU8XWmtWrECcsPj1lezCHJPnBHJ24r4F2HVVVXrIrLZmvqteRkSPogPxk2pKQNNNNdgkS7YlfEsw5LJajYdLrbPWqZ8OmC/z1DMLGB4bkL9n6yYnN1OzUQg4pQ8McHz6Ea9euZWdnHz58OClpw/3334+X7NmzJz4+/v/+78//7/+9Yq7DDn0oMUpXuL+INEWt31FxQagbTRp68Io4fuHLD32mWpGxPX5OYUaRHOecV0Szy06cadYjXnR8HKe6ShdDXS6xmaovenhTLMpPF4/jtSqH7qQoJm5JMKr6rrBErPOPiZujKswv1+GFYbLCMr4oOAo9yYmUFOcXmieAiYlbEcap/w7fldP9o1bMoetIIVlfdKK8mQx96OEwEuHQmyqzQ5ev4FQfK1OFrYghywqrOLE9pXhdcTs1G7t/NYnYwti4MEl+/sALX7L7mjJVttjuoLuD64Ne1AkXFxvJay756hgVwgGHjrSMbz/65qI9mfVx27cKqQeV6Yzsv64uNG7ThsTYaDKSH1leuH/Pd7o5/U8GveWpsvjJDTGkpLxeRbVkceboBwXUwojOBzgZAAAAAAAAAJMCRkADAAZSScqLSsr7xg9TCUsS9YzMI4ex0HyXHG6GtV1cuGdPiYwUhglJa82yIzdt376OU/iHxBW/iN+8v8pKXrldXHKmpFquH10HqKRsO7UqfQRJ4WH0qv8GTCOmtz65YsUvViy5Pyx47vNfNaNRMRqNBHHri0MWi/XKK6+4u7t/+eWXd989/e67787NPUSS9C1btrDZPYOKcco5LHFHbtGJPRvohTmFkt78rcVg6slAkjweh+RwOD3BIvmhUTFhwRzqDJAX7c74pLwv30YXxW7eEEryY5M3LL5t40R5MakZyVEkGboBp8hFOIyh8YmxIl5YfGIMx/T9Aj9YRJKiRKqUbq6MdP7xW9PxXVK4OHFDYiTHPyZt++YoNic4dkNijH9PZRa+GzuHTyJ+ME5q88ne0tDEzO19I745kfGb4/1lMsssoUVli+323EX+iRnU3cH1EejFDkvCR1hc3uwf+9gSK4duQHztNzUwCt2y+pLyejn+i59K6/HXTQNPBouQ6VXNVSVizpyYMNOZb71yv4BaGNH5ACcDAAAAAAAAYFJAAhoAYI9eVd+s4sQkJsVGRsZteCyMlImbVVYX4sy1TMeJXBLqT2cHx0QKhznJBFsUu2FDFF8nLpO0W2uW5AuppnQ6HZ0XFhsltHNxwZF0gO7/2AfFPxxLX8zDlaOigpGkqlllu7pOJ8E9iYqLeyg2dnlMpD97+L3qPYahUaE8Os4Hbfnksz89Fkr3j/3TsUPbYiMfyzr2RXpM5LoPjn62KZKNhmAwGNzc3PrudnZ2bt++rbW19eGHH75+/cb169cfeWS1TCZ7881tfVNF68VfbV4xd070A9FLHs8obO4bP+zm5mowTGICWl9/LKdEmJyd88HmYElRFZVqbq8+sDVtd5F88BhnevCSOH7Z7h27CnUxGxLnWD9OLi4udrY3ilIOn6MqOvDZrreSE1/OFevlZSerODFLliwPVhUVU4l8naT48Gef5ORWkSI+m8PHZwFHFIrTyXwRzi0jfDrn7/8sO2tXvmk6G1198YFdPZUHny09pfn1pJAqJflLNmVsjZXtzymxMua1f2WL7bJ7+ow3VN+3IYvGp6pxj69OJVZxImNj/Jtzc06I0aBD1z++9o8bfWAUXOTVJcXlEpm4/ERhibhdP/BkoFueKvgbtOLy6ltfYllUHhxQy/0YyfnguCfDuMcX3GYTF0EohVIohVIohVIAgBOAKTgAAHY1l+zKyhdtTd6Vm0wlZPZk7q9qR3orC/X6opw95bvSdhXFI1lV1dBTcJjngKZuqcr2pO3AuVG9anCzcjJn13fvbs0+EauSSeolKp3NdvXNI+iAvrkwOysqa+uekg3mDmzOrbLzg3R9Vf7u3LgdiRlZibh28db4lOH2ikIdw8IdPdtCktzNJfWIDOXzhTo2h8Pj8xGbrRMK+fIh88/o5s2bfD6vo0NrvltXV/faa6//8pePP/fcs//4xz68JDc399tv//Xaa69JpVL7TbFYLJls2FOOjBpbFBlGSsqqB2eV9fKSXalbZRnbY0p2fzdER6jpQ2TV1fhIl0tQDJXutxKs7m57M4qMvpSaqCGGLMsvaa4qLOdsTYyq33MA55/5t6ZYMfdGJSk8kL6r3Lyj7ChzGT4rDzcj5B98q3LPnA1s0rRj5slaLOhkxXt2ieM3RAXziuRDBan/dukiIRqa7aA4snGPr158eHN8Pi8yNnlz+q906ScGVRgYX2tuPWQHRB/1+x1Hv2NsPhnoojCLylb1VUYjNPLzwTFM1OMX3C4TF0EohVIohVIohVIAgBOABDQAoIe88HdLCvvunNm6Yq75ZvXh3z18+HcD67ZbXViy+8mY/FAhKak3jfqzQy8+8OScA4MWW2tWX57z/Ip8URhfV1/d3JcIkmc+/LPMQasPvwOm4ba/W5GbGRom1EmqxEOl4vTNJ7c+PHdrvyViK726tVP68p0Pz9k5YL/yM0RhkUKyuazENPdq4dYN1ai+XlWyoURXX6+rfjJXVT+cOVlVqnYOh6NS9YzXbmlpycrK/uijjx98cBW+++STT2q12iEb4XDYuB008fyXbMqIr07dVC23XpoUh3K3H+uZ15kX+6fDGcJd6zbsF+t5Ma9np8WGBfN1wXtEO9I+KC4ht757IJ6apHxHlgrdFpLiQllGSmYoPlxVu4r11PcQ3xXp4iKLymSmDpOcOevSMjhhwvqs+usSSRGunB1JcsiyXanZZZaN9VQO5pRkVbXL+CWqxE2ZmYhDlmThZHbwoG3r9FXHckoyUzZE1WeW2ElB6yXFA7ZbXFxYvzlpawYiVYW7bHynYj8odw526LqMjDhSouKQsj2ydols4KFb0j++g4+kXlVfrkvcdiBfV7Xnd9sGRqFIrpfViznJ7x6Opb5lGZjatgjZrvo5mzPxqS7Ep7ooZs8fttVbVB46oLYbH3Q+LEEAAAAAAAAAcPu5EARMAgjuUIGB05ubW4es5u/v29JyzWqRn5+PVCqzWqRP2kT74jN8Q/PPr5FtzF8+uGxJjJ0Kp74rslMBl7645mM7q7+f9yz+a3j8SXrObgScBUmhjzqDjLPPOp1eZ3fUtkDAt3PaD/OBc+2aNiY9K646Iz13Qi4d6ObmplarJmIma4IgWCxO3zQmfXix2zJjilK3nxzp2GH/uD9tDT2cmlniANd9Y09oUMbR7Y8vuJ0mNL5crtfdd09HYCL9+ONVpVIx2dcSAAAAcGcJCQkZzicRAIADGp8R0BER4fhvRUUlAgAAMMHMuWM+n6dWa3ASzWg0dHUN8Ts1V1dXnJRxc3NlsVgqlQonoNHtoKvKzayvd/RE57DRObry3P0lo5i5QlVfWKiSDDktzW3hZEEBwLru7m4XFxf4O3F/EQAAAAAAAMM2pgQ0nU5/8MFVjz32qLe3N757/fr1L7/M+/rrAr0ePtgC0MPth0udP7vHVhH+q1AqvbhcqxVwkZ0K5tJmWY0/f7bV1XERAk4K56BlMp07hUEQbJxZtl/flKc2GgwGqVR2GxMHenl1NXIeenHRYTEajfbqk7mOciScLCgA2GSeQbLvrzlzeicvH/eWAQAAAMdEsHwD+EjW1KpGLL8AHpJJWtTUT3YIrjBsZhAXKRsuVzcprS9BDG6AH4+BjGpFq0yphV/6ADBeRpmA9vDwePjhuNWrH+FwOF999fWhQ7l44dq18c8+++vHH1979OixY8fyb968iUaPxhUKfZhIIZFINQZ0uzHnPvfWbyNq//KHD0qVgwsFs4RMhbhBOrp+0ZgCoT9TI5VIlcNuYHKPxqDOBM3yMTTUSjQIDAPjzd/br1D630tjqZB3bicCd6oOkxGtAsPWAAB3Jls50ztn+URvEQAAAHAMBPeeB5/6Bbfq4CffoJ8/lRCq+ObDnPNyIzci4flfhjHwxyf3lcsuHfzgi0to0BIlYvgtTnhuDqHAuWsvoqUoJ6ewSYsAAGM3mgT0L3/5OM4yu7m54dRzbu5hpbInR/vBB7sOHDgYH/8YLsXJ6C++OPTPf36BRo4mXPzbN1NjfJBaj1h0dUXO2xmHKkeX7KQJFj/34mLJ/qyjtSNoQBD97HPRmi92fGol+4zzz8JHXn4zvPiN1L21I84FcyOe3fbmIyK8Z3QW/VrRX17NOjVUGnscj8b4oAliXnxttWRnyrulkIEeDu0bf7QzAhqnp+f+zz12RkDj7LOtCubSNQu32BkBDelpAAAAdyaLWSPMCwfPJnHnLB/flgEAAABHplVq+TODZiJ+h7Inf8zgh/ihKwf/8uklNCfp+Z/P4DMuI8sll0yVjYq6bz7Yf4mIeOq52PsCzjRdgQw0AOPAdYT1qemen3nm6e++K1q/fsPf//5JX/bZDN/FC5OSflVYeBJXi4iIQCPGnZf4zFxNwR9+FZ/w2LpXPqwVrl2/LIiGRofOFc0KEjFHtA6SFmc9/+vXR5SzHh5uxCOLBbV7X3o68YlfZRahuatjhEPt2LgeDTAZbGWf+4psZZ/7imxVMC+3lX22XwQAAGAQOs+fB5dmdg6D546A5ePbMgAAAODIjO0yrd+99/lpZe19s2gQyNhhwPeMHR1G82DMwUv60XbgVd3dx+fCaQCAET+Wfvqppb29feXKXxiNxqNHj/30008WFe66665HHnk4Lu4hXG1w6dBoXkIBU1FzppYaGmyoPXUghz5L05MKZs5atm51TJCAqZeKSwv2H6+gJrEQRL/w/DLN6VOK8GX3C5H4zKEvTtUqDcxZ8WkvLhMwuQEslujFzFl63Ni14o927q3QDGqqxNSUebz08/dLPv3L0QYDNfR46YvPza39KKtAgu9xZy1buzYmCF0rLqqloVujlq12ySaDQW9AGo0eGTRndvz6DBrb0QiKXro8Zq7IC10TlxQVnCmVaKg9eC7KIEVCL2XRyVrh8qVCxZn9+083aExHSXr8lCZiWTS1F0cPHa/oGXxtpR3TcusHtqdjdMHcR56PsVxuoymaICJm5bLoWUIvpBCXnio4XtwwsuT+Aw8sYTKZX331tcXyhx56UK1W469DEAAAjDde1KZkYdGO3GorlzWg+8c8mRQXKUQl2en7qyf3ugd0/8W/2hwn0slKvjgqm/f4UL3CXd+QyCnMyh/FdQjHsu4UgHcvOS2mfEdGfvNI928Cj8wI4wsAAAAAAHBOubWqxT2MuKLk389GAIDJN+IE9PXr13/96+dWrIhds2Y1zjJfvHixoOCb4uJiXBQdHb1q1S/mzZt348aNTz7ZU1BwfKSTk/ag41xr73UMNZdPHbpsukULeuS1N5OEDUVHT1UIoletf13k9cYbn9bqaQJRxP1CH1Zx8fcXJfevevadCMGrr34q1kgqKkoFXvaDQ34AABAASURBVLO8fIIUktqKa3qDQSpW6Ps1Jag9efSUxCd61bOvpwvMTXmJZgUhJrV9RM21IZol0lD3kPCRVPOmi6TC5aujfZgKe12ymVxV1pwsVf925erZxR9VKNEw2TgawlVbtiWyLh45dVIftHz1C9uig/7wygcVTHwwIgxFR8XMR1580b+goJm1en2SuPKNItNRivGhF58qvkiLXr3+zdle+CjVaqy3Q809QrN+YGuprtB95j6yXI+bQjF9y202RRMuf/719V7Fh44ekiCcx395W/hHr759SjKCCUzc3d2ffz4Z/zXPNm62dm18UtL6v/71fQQAAL2/Ex/HUpIvCo5CT3IiJd/lF4rb8VOfKCZuRRinHt+tbi7ak1kft32rkCQRMj1F9y+VU2nDKHyXVOl0khP5ZeScFXPoOlJI1hedKMfZTXZobNySYF3ZicISsc4/Jm6JkINUMsRBZSe+qpb3L21HdF7kirjYSF5zyVfHCqvbB3WeExYbpcpPyThDFV2y6BXe0vIVnOpjZaqwFTFkWbFqzoYNibHRZCQ/srxw/55iMqZfaWFJM9l/0+zQhx4OIxGHlFFHAIXGbeq/Ll4yYJeH6ucYjXt8B8Uo6skNMaSkvF6lH1xaIh/DkbELb2bguWFxIg0RX4sTjxf5EA7ooWJV2MOxnLLcopHEaOBOtQ86pSfWuMcXxureZhPwCIVSKIVSKIVSKB09Amkvf/PpvxH3vqT7A9AoweBnAMbRiB9Qvr6+OPW8a9fuvLwjCxcuxLfT018zj3S+6667qqtr/vjHP509ew7ffeGF53G6UCqVonFBjaIN0hTtzDBNPVxUa9j5+txoYW6tGJfpFRWH/vLuabylU2J6dlpEhIBW21By6KMSmvBh0Vyu5MjHf+s/XzFNMC8mSHHy7R1/oyZTPlmr/3N6X1PWNz2336a/l9D//HKQvS7ZykBT9SN8vISrX15f8WpW8dgOjLriQMarzeYrARZLUHbaLJEXrQLfMUgvFhwvEs6au7y0oKAiYt7iVUIuDWnMR+l901HCXX3nTdzVA7W11tsp7RnRbO3AStCApm4dcFtN0b2CfJCk4NCR0zjnXFx8ei8aMfxlBpPJxOlmfLvvipf4bk7O3uPHv0EAADBUvmlUpaQwOJQnVsVkRpEpacXBqRnJnKIiVWJGOic1LXfgSwYvZkDpCX5q5mZ8VxcfH1xUlV9FLk7cEFyWX89P2x6atTlLFRsfw6mu5iVnRPFTd8iiYqNQPRkjKpcJE2Ul2yUx/Uq3fsdP2hxP5ueKRbGPLanPHDjElh2ZvCNjQ0wwGXM4uvm7HZszilQDd4HOCY6NFcpPlJHBMXF8SfGh+pLy+jnBZElRSXW9jM5Z0r+0qIzTv2Nby4JjNySiE4WqWOoIpBcPWLd3lwtV8VvTOelpJzh2+jkOxj2+7KgBMSqpb64qEUduiAnj5Fe36y1Ky/ijPzK5dg8FKRxwbuwhU/qtu71+RYbd+Fpu65hMJ0retJYvi4lqzjqm58W8PuC0tBsjzoCdGnzCT+yQ63GP79g/uIIRmYBnYCiFUiiFUiiF0jEYnOvSqjuIAL4XowHxvQhtAzWx8+Alt9Zn8IP8GMaGWzN4AADGZMQJaHd3RlzcQyEhIV9+mXfOZMaMkDVr1uAinHoWixvwjcWLF+Els2bN/Prrr9F4oTN9mEijUJs/AOkV1zQoyqt3cme9RqnpuaHQoFle9J5BzLaa8mLSvUQr17+wmLrLEnoxmV7M4W7aoNDoh9GlwZizH0mMRkXvZyqWPfvcc0sl7zdEp7+1Spr1yo6SYQ+H7mNQShroEYsfWSbyodNogllMOp3aa8uPhwMOQr+jZO4qPkoa6+30rmjtwNpabqspjfhMsXT5c++8E/F9rUQqriwu7p3kYyTMeWdzDtp8A2ef+w+IBmPHEK589qlwef7HB2vQ/ITk5YyzOTlnW+EF1zExAuOSk+71Mt8xNhzbte+CHGI13nT1xYd3fSJbIUoV8tkcPkdVdOCzT2QSUXoon0RiXb+a9IGlbI7QfFelCk0lcUWyXVWfv/+zQlQfF4ZTiLLqcrEoCrfC4Qv5dBnSycRixOFImjn+JDmwlNSpxCrOutgYXVFuzgnLJGB7+a7nk+q3ZUZ+lZJZYhrQan8GY728uqS4PC6GX36isFyP6P4W5QM3XTbgCLjIywesK+ILOSQShZK4sgj3U2ann47IMkbt4pJizpz4UFMh3bJ0DEcGDXE0+p8bdE5Y/3X1uUPEF594A7alLynakx+XkzZnf8ruaj3uyYCTdqgY2T/hp9icH90Dr5sHf8f9LwIAAACmFG3L96eqAtY+//pK1HG15HBJi1aLLJeYaxJeoQmvvYHwwnOHzzXBFQgBGB8jTkA3NDT+7ne/f/TRNa+++ju5XJ6f/1VBwfHMzJ24iMlkrl0bj9PTPB6vuLh4y5bUxsYf0YQZwQwO9qklRQXFFyXj8MlqiC7RuHSkqK0oPllBE7357OvpUi+f2r3vlo48+4xxo194++V5moqK3mlFRmm82rHXlKbi01dTKmOWLY6OWLx89dqkpqOvbvm4Ymw5aMg+TwyjWq3lzhbyWokQllqt7pfPJFhcllGt1A5IcTK4vlxCLZcPqMhgIPxSzmDhb5gHVLbagnUEg8si1MoB69tYncHlMbTKAYut9cp2C9RSNGhbPKoFpXbgMpZRaW1tyzZtHgHr+zqGFtSNhQf3wVcEk8z6lHJ6nUpHRvnz+WycE5STt5Y3Fx1uRvTI5JQ4lJO+Q/VwZgppuS49bO2AUr348Ob4fF5kbPLm9F/p0naVD2Nyi1u9Mj0ds6mN4My2TncraW6aw8GitNti07b0zv+gkhQeSN9V3vuUP6ifbFFkGCkpq5Y7ZOrSRozMLCJIH9uRQcM4FD3nhihs0LqDDTjrBtan+8+J4kiqdJFzgtnlVZbbGMW5NJWZx0/B34n7CwAAADgko/z8J5nnzbeV//74//7ds1hZfeTD7Uf61xy8BGkbjmW+dgwBAMbbaOa0kcnkGRlv+/r64jR0YuI6nBDMyzvi5ub28MNxer3+xIlCfLe1tVUgEKDRwG0gOq1nFC51Vb0XF0v2Zx0VU9fvo9FRz+hcGp2GDJrRJaH1uCm9tOLoR3svD2iAZsDovYN88Q0a0ihwb/QDN40X32pnRF3qKTNITr+fE/3n30UrjmwpGmIqZOtHo0ATvfp+Wun7b+0optLXzFnPRkTMRUPBO9TTdVNXqc4LR9OOVfab0khKC/aWFlDTZj/8zjuPLJt1oKJ05BloUw7aaKTSbfgcQ2AiqFuVrPDISMRQyrWE+fmB8J2/Zs0DgSzqJbvmZN7xSmqgLSNw5VMJ83lGtZHBUF84tO94nZo1e23SA0SrlsczSlqRUKg9uy+vXGm01YI13PCncBNKI5eHs8KSk/sOFlPZVWurE76Lkp6azzAiBgPnqsvz9uXXKK32yuYumLbFUBtZXJxZrsvfd6jcvF/LE9ZG+yItIrQ1+fvyK6kdYAgXJSQ84IuUOAHNYMiP5+TVqK21afsIWDXGFszXbWbxfAnt4Gw7GH96SXFh/eakrRmIVBXuqqIyd6r6cl3itgP5uqo9v9s2sFSuy8mNTM3I5uA8Z6HOlJjsR1Yv4yQnpYlUfD5ZMmhLFqXs0HUZGXGkRMUhZXtkuiH72b9X6bliWVWJKnFTZibikCVZpq9aZfViTvK7h2NLdqVuPTaw1H7HcOMD1i0ukmWkZEeSHLJsV2p2GT/eop/+SzZlxFenbpr4+YNHRf5d/xjR/WNTM9Niw4R8XbAoZs8fUg8NiOBYjkyRXD/sQ4FPM8t1LSpYxHdg/V2S6JR4tD89vT0xY9OTZWmfDDwtR3IuWTnhpxbIkAIAAAAAAOA4RpyADg//2R//+M6BAwdxBvCDD3bl5OxdsSI2Pv4xXPTRRx/j7HNHRweLxXryycR16xLS0n5XVVU9ovaRQVlbK/WKWbe29OMCCXNe4rrlIslfFBpkkFbUKFfj5RWfFki8ohNXijS1h5pwEpNrrzG9UmFgCiPmzkW4BbVEfFmqQX1Nra74uKBCI1qdmrZak/NK5impRlyj8FoevzZaUXDNK2btYh9FsVhqQAZFrcSA66+6+HGRQhizdq4P3ZQ8tdkl6/QKiQbNjQjyOnmNFnF/kBfO0kbEiLiX7V2P0MbRMOg1auQljBBxi0uV1NTSs7zoQx5ZulfEytWLpQUNTKqrhoYj10bXjo2eqm01xY1Oy0oLKs54lbq2oZePkJq2ZDTJ5x6Qep5YRmWdOmRRuLHuQqtviGkJa/ai+YwLOe9ekCPfRU+tiQ6sy6/TMnghQqLy4Lv5dUZuYGQIg0EgtWntmm/PslYu0hZ/K1m+0pdLICp5SrXAKt/3bjFOqS5PijO3YLsHkpM5ORKjuWZlHpXYttIBU0158b6DF+SM2Wueig73rTvbSljplRHZ6YCx8XjOSQkKXJm0cr6w5nijlmAwlJV5f91Xp8Q1n1oZLazDC1mB0eGo+OOdeAMhcc+uJGweFptHwKoxtkDg5LNv9Jo1gWqW0BdV5uXk16gRGFfN+b9Lzqdu5KY9b1pwMjPtZP8K7dUHNice6L0nHlgqKSvcr6sWxsRHqXSovWR38q20pb658A+Jhf3qlr9MFZp+1GHa4MBSdGBz/AFkm7zwDxsKbfUK9+twWuLhAd0u350Yu7v33sBSy45ZHAGLdb/auuGrfv2w6Cc7OJJflb+73mFnbtD3jxEOyluJhW/1K6YPLB3DkbF7KAaeG/jksFh3qPha1M//3QZTxzJ7Gh140lbbO5eGPOGnBE8K19XVRafT9Q0pAONOr9ezWEwPD4+2NmVbWxsCAAAAAADArhEnoCsrf9i//8Cjj67B/woKjufmHj5y5Cj+Zy7lcrmJieseeujBzs7Offs+G3H2maKp3Z/1kVfqc+lZj+N7ioov/vK3M9T1+jSlezNvLb92Mefdj6mxtjS7jUlLj55sfv3x1G3UOpIjr6R+RF0hsLepbR8k4cXq2iM7sk7hRDMy1O7P3EF/9rm0rMfpeMsFf9nxqWmcrvLiFwcuznohadu8JKQXX6xQ6M0Tr9rokg2GhlM5p6LTf/fxl9RuHf3DS6XzfrvlhaSKV9+1Mwe0raNRvDcn6s0X/3ffKrVar2kobVDomWgIOAFuiHgx63EW9an75F8+Lh5lOzYobTWlrDhyVPzm+m37VpnuqmuO7DwiHkMGGkwggiCM8gtncaJWogyMMyWgCQb+Rok7e9FKnhYxeFwGYuG0rlarlLSi5Yvi4kKUrY2VNXW9Q5qp/5gHqZsaQ70t9E5yoZaridmmFmykZY1GXEXbU9OXhZuw3gGqrtbcqFpSXlxJUEts9Mp6B25ti8D/QYEsqrc4/17TOjv8gZVcBkvIZSmphXh1Rr/Vjb42D4vRxhGwfqzH2IJWXnP2ZGVduSlXnrQmXMiqgQy0I6FzhGExMSIvW1UvAAAQAElEQVR5yY6MKTEh8gTQVeVm1tc78M7bj9F4RtDhD4WzwLln/MSqUChNt9nd3d2Qg54IOPvc0dHR1kaNi2ez8dtKBDloAAAAAABg32im4MAJ6Ly8I4888jD+h3PNJ04UfvHFIVdX17Vr4/Fd/B7088//eexY/s2bN9HoaBoKdrxQ8L5A6KW/JlEa+i9/64UCi8qG5qNbEo/23av9NCXh0/5tVexNTdhrbRNvvXCSiTeBpBKppl9rxR+9WZzDFTANUmW/xQ3H3/r1GUFQkA+S1jRIh+iSTcrSj1Kf+MLfh640b7M0JXHolawfDYPk1M5fF30sFDLVkuZ+xyh3y9OmQXQNbz9/hvqv5NX1VPdo1IWm9NeO7/jLAR8v1CRuUBrst2PnwGpsHXBbTWlqc7ckwHzNU4a2tbJYghiBgf0WqVvrahpxqrauslxtnu1BXZO/q5EXOHt2ZOTKpOi6Qx+bRu+OM6PtDvR/6lI3ll/ouTW4VyO6ZgThG/3U2tny4uKaOiOLEPoyTL3ACIY5FUyw+mWEB/WKgUZoLC0YlTUXencbJ9B5DKpnMBGH49DLS/a/VYLuZHp59Si+hL6N7MdoPCPo8IdiinNxcZk2bRqX66XX6xSKNqOxE1Ep0XacfYaJOCZCZ2cnPrzm49zervby8oQENAAAAAAAsG80CWgMJ5cPHvz88OEvH3xw1WOPPRoX9xBeeP369Y8//vvXXxdQ8xaPnUYqmeBhsgaNtMHqJgxKqdJahxoqpWjMG1U2S9DIWT0aBqWkYWSXMMT7UCEdh3ZsGsemgGMwatVqo1HZ2lgnR9yQyBCWkjqBCV74/EB1ZXn5WYlEy0oI6R29a6MFLcEL8WXVNBLCEB7Outq5ECFBsHy5DKREXF8udQk+o40OWF/ZSq+0xhF0AG+coZVcKK9pNTJCZvfmmtWtEvUD86PDtY1ESCCXkNs+LCMx1hYYgYtWzpZ/e7JGzRIG8pBarYXsMwDgzjN9+t333PM/Wq1WqVRKpa0WpZCABgAAAAAAwBGMMgFthhPNeXlH8L+IiHB8t6KiEgHHZFDWFuQe0Ujg97+3n9sPlzp/do+tIvxXoVR6ca1PZY6L7FQwlzbLavz5s62ujovQ2Klrzl4IiUtIjkYMFiE/m1dpmiJCrSTCE5IX4SSqWq28cLZOaUQs2y18Wzx77dqX03GSWl6Zf6jRzqhknHHmRickx3FZqPXbQ41qWx2wvrKVXo2oA9rW8kYiIenl2UrcgBa3Z262tTgvXzs/JJAnb5UohQzbh2VExtiCVlLTGLk26TcrGSyWuibvYOOIxnoDAIATwNnnWbNCv/nmuMFAvcHx9ORyOCyVinruNk8N0dXVhUxDpPsy0Xfm7fFuzbX/cVapVAgAAAAAAAC7XAgCZscDd6jAwOnNza1DVvP3921puWa1yM/PRyqVWS3SJ22iffEZcgyGx5+k5+xGjo8bnvBUZM2+feUOOoyeQV2ukDiek+/82V6BgG/ntB/mA+faNRmaSG5ubmq1qnfC7AFZksFGVEoQBIvF6ezsRGDyQHyd29jjO3fufLW6/fLl2v6lXC7OQXu6urq4uroOnkXf1lbunOXj1XKnSVdXt0rVpjR9HT6Oj1AohVIohVIohVJbpSEhIcP5JAIAcEBjGgENABiS9o0/2hkBzXjz93P/5x47I6BL/3vJVgVz6ZqFW+yMgM47txOBMWOErPnN05FshNqbyk/mS2CssWOy/1v7UZTS/ZdvzUyN5iNVVU56+oHqdotiXuTalM2xKDc9I7/Z9PMSuih+82O63Ox8uNrcBBj3+A6J7r/4V5vjRDpZyf7duf3DT/ePeTIpLlKISrLT91frexZtSOQUZo089nCamY00grNnh+p0Wpx9tijFyVC1Wo3T0F5eXoPXsrWVO2f5eLWM8/ttbVTque8rhIl7hEIplEIplEIplAIAnAAkoAGYWLayz31FtrLPfUW2KpiX28o+2y9yUMrKg391xJl8tHV5O9/IQ+AOE7wijl/48kOfqVZkbI+fU5hRJMfJwBXR7LITZ3AmkBcdH8eprtLFcDj42x5E5QUf3hSL8tMh+zxlsENj45YE68pOFJaI26lU74q42Ehec8lXxwqpPDAnLDZKlZ+ScabdsnJz0Z7M+rjtW4UkiZAeF8Vt2pAYG01G8iPLC/fvKRQjUUzcijBO/Xf5hdVyu32gw2k2Cmw2Ozg45Kuvjtmp09nZ2X/2iVH/RQNnsRjF366urnHpiaP9RQAAAAAAAAybKwIAAACAFSTJ43FIDodD5Rmp+/zQqJiwYA41dZW8aHfGJ+V9yUW6KHbzhlCSH5u8YbE/TG01FdBDY+NjODJVaHJGepw/nR2WtDneX1ze7B/72BLRtMjkD3Iy4qPXbj+c/1l6DM+i8sCWdLL6kvJ6Of5bhP8rQ7yY1IzkKPwlYGJGerxoyLMBTrMRmzfv3rNni4asZh4/Nca/GM4gj+XvePXEAf8CAAAAAAAwTJCABgAAAKyoP5ZTIkzOzvlgc7CkqIrKAbZXH9iatrtIPnjwKT14SRy/bPeOXYW6mA2Jc9gIOD5ZdbmYHRnKJzlCIZ/UqcQqTmRsjH9zbs4J8fXyXc8npecWf/a7x+KezCiSW1Qe2ND/Z+9+AJq67sWBH+AmN5oQgk0ilGD5ExRYcCisULXoQ+mkoxWr2yh1E/dateurdm/F/Sm+vVb25yfdW7Wvm9K+Cc5aummlLS20KFP8U+gAM8kA5W8lFEiihBAkN7nI79wEkD9JSIAo4PezLibnnHvOuefcKPnmcK5RU1teJleqm+SWtdR8EV9X+t67f8452UgGjS08hhEuM2f5+y8yGo3d3d32i/X39+Mg6dQfpxh9npY+zMxHBAAAAAAAgMNgCw4AAADACqOm/FD6XnXmvrjyw+fs76OASJLEIcraRqVOrkRxfBxz7EFgZgvfvCsJ5WTs1z2RtYvZSaPpg92bCoSRCTt3Z/yI2nNIPnIG2WMKDxoXATbvyGGNZ1BkOKm8XDs+qgyXmbOWLv1maelZR0paVh9P/XHqK4Wnqycz7REAAACYLTgcks1mEQSBHz08PBAAwEn9/f1Go4mmafxoMFDIeRCABgDMHhweD+n1cBNAcLf4rU5LQif3fTy44a4w4f99kCk59PS2401GYdwrB/ckhAeLqOAjQfv3/KmsnNz7xnubEEmV7z+gQ2DGUzeq+TvT9gTpRCKynNnj+enMzCRSqeOT6iNqyn5hHDfWNcqp1NfeK6Bqjvws42STurGJv/ONDxKYaPLHZcWNu9P2ZiJSV3yohokR+63ekbmpNn2H9Q2h4TJznL//ohs3bvT0TBB5x9FR/COyu7s7jpNO8XFgynslT70PM/URAQAAADMf/rd4wQIvAw6YUYaeHiNFUfiHBAQAcBL+5oYk8Rc5bPxFzgMPCG7e1Dr7G3Fu+BsgBMB9KSBgUVtbx4TF/Px82ts7rWb5+i5UqdRWs4xpO1h/exc/6f3rp8g27vceX7s6zk6BM+dK7RTAuS8kv2Pn8Lfyn8WPpu8+w845jGY5nnR9SnKotuCdE3V6BFxMLBbZuewdfON0dqqRK+F/AvV6Hf4OFk03/G8qj8eHn03vrTk0v55xGQeSajNxnBruUDlscvO7dm3ClSv/VKtVdsrg+eXzBfPncxBwpVu3DDqd1hXvUAAAAMAWqVTqyCeRYWw264EHvNvb2/v6+hAAYJrMmzfP19dXo+kymUyOHwV7QAMAph3hE5u2MzmUh6YNR7IqaRVRlvO/k4k+C2Qp/7ElUoDuGZ5s884t0UL4jRMA7k9UzcmsAx9D9HmqBAIBi8WyH30eNvf2gMah3hlVDwIAAABmNvyd9Lx5ZFNTE0SfAZhe+D2F31lcLocgnNjQBgLQAIBRCA6HYB55DoRLCZ5AMKYchycUcAgbZcdlcAQ+PsKJWyKEkWsiCfmFOg09pq8C3BpyEC49trfWe8X0a/xZWDvcRkM8R0sCAO4HRk1tbRuEn6csKEja0FDvYOFpjPy6KAbt4eGxaNEiy3N3d/cHH3zQ09PTTk/QNEXVHaln/vz5jtQDAAAAzFhubm4i0YKODieWSwMAnNLe3i4SPeB4eYiRAAAG8UI3p60hOgxCIa3sQBKJ4cKxfLmWF7llS6j8WJ5CSwijUzYHyI+dUOgFsi1pazh6micQ8uiGgmMn5ExomCNZlbJljQ+t1Wr0BKEdrpjwiU5OXhPAQ4jW1p3OL1KYCwes35ISLaT1NIejrzhxrKjB9tJmjtCHp2/o0I8IPxM+kUnJa6Q8/L22oaEgLx/XyZEmpa0jTh/LxzXxQpPTVunzj51WWjaMJgSRyc+uEQp4SFl0LK+ig7beK8JnVdqWaA6NODgAr5fnHyuo0yLzyRJaWmA+/PSxvDJ8uMDxYRmJ8IlN2SxtOGGuA0wvy46rrsgFMwHM79zmyAwGB0tPnvyrg8cO78I8vgyO8/r6+jY2NuIoqq0yw8/t1DPF5yaTCcedg4ODv/76ax8fH51OFxkZefXq1eGPyo7X6e/vHxYW1tnZ+c9//nPp0qW4trq6uuvXr9saJfvPBQLBww8//OWXX2q1WvvlbdUPuZALuZALuZB7z39yW7DAC0fHEADAlfC7bMGCB27e1DpSGALQAIA7cCj27AXe+lWGsrPKdet9BASy/RcJ3VKUc1qJAtanrY+W1BW1GATSVZHo7KHXyzSENOnZpOGVybzQVdE8+bE3ynBUe11aUmxAQ0GDgSOUSghF3hsFDbQgIFLKLLvW2wzJEgSHGL3PJE+6KlYgzxuqc1VACw47K+UNdHKkhNdQhyQyiaHuRMfQ7QoJRCtP5+QoaUsHFPkNBqZXnIqcNyo0yGfVlmRLr8znpSnDIWoNJzR5S6zMp+GCORIw9nC948MyIo8jiV0fSV84UQHRZ1ew/3PqVHLBTADzO7dNOIMPPRSgVLbetnbnO6vH3rZ9jzyc9dBDD4nF4urq6q6uLmTXmM/Ak3hu69Tw96cajSYoKAj3R6lU8ni8L774IioqCsejkZNwDf/6179aW1vxc7lcjuPRyO4I2Hfz5s3z58/39vY6dZTr3qGQC7mQC7mQC7nO4nDIvj4D7LwBgKvhdxlFGfA7zmCgJiwMAWgAwAhMYHQo1Is/HNspSOs1ehxcJfAfKIDZcIIgeBxarzUwBzN5PoMlCQ6Ph/Ra/WA6EcrDwWaDQavsQOtWJSVJtR0tiroGjVMhWYIjGK5TefqdQ5ZUQ4eiTr85MkDQgWRCveLCnTqHemvugA/TARr3iicIXbVeaEAcZh8Pc6/MtVjqxeHsMgVhsHa4nXEZPyxDHRbK1iSF+kj0Z4/JNRB+BgAA5/j7L7p27arj5Qdsr/C1mDdv3re+9S0ctL127drITY3HlB8O4077OmhPT0/cAfx8wYIFuBWKooxGo16vxx3DP8o7VadKpRqOdOP0zs5ONGLttrM9nD9/Pg6LX716FXfJTnkEJ3imGwAAEABJREFUAAAAzFQsFstoNCAAgOvhH6RZLDYEoAG49zz+daX/G0ttZeHHLq3WW2D9Bnld5t9+tVXAktumrvMThVo9HGeh6TEy4jpdwVN9XcGhFmFAaGhk5Pq02IYT7wwuQLaGNhhou+HwoXKaOoU2MjI6msbx57O24rzDyQZ9R0Mds0S5QSHHAWN69N+I+hZ5hd3DnRoW2qBpadFyAmQBQp5C6/yNFAEA4P7FZrNFIvGFC6WOH2Jn/e9wDNryHJe0s6PxcKR10uugbS3jum1mef7ggw8qlUqdTocLu7u7O7vDsqWe4dosLU56BbTlW2jLyNgtCDeSAQAAMEOxWIReD/ffAOBuoChq/nyuIyUhAA2Aaxgp/IkZGY2cV39uv2DVP69MpUD+xdeRfUw3Jv4yyiaDXo8EAT48hZ6QSAXIshLYGtqg1RMy5paCeo7AvMp4KF1vIIRSH15dC65BiCtkFkkTQll0gF4hl19QKg28FKl5AbKtKK5Bq9TzcA0VHVr6TluRTJ0NBsmqtCThWfPOz4jWNsg1q5KiUUtR0cj4M0EIfAQcpEX4D6RnOoB7padpbUdLgwYJpJFSnlaJbCII3p3DDXrms7nDwzI4CLS+o0Uhb0CSLetWBSiHduYgBLL1STLDhYLTLeaYNC9g3frQjgsKXmykoawCRcdy5EVlSvjyHgBwf3vooYCvvmpx5gh7ezdbos99fX1XrlzRarX2VwQPuGwP6O7u7vLych6P941vfANHny0bg3R0dOB0Z+sUiUT4eWtrqyUdv8TpX3311cgBcbw2PDLXrl0zGAz2y8MaaAAAADMWm83CQTEEAHA9/F7D7zhHSkIAGgCXcOvWDoh93JTX0b02sNAHdwZNmqHlwoWOLZtfZuLomooTRba3L9a3lMljU7b8R6Rei+PE9HCb+rqzZaGbN7+UQSBaoyg4YQ6+0notIUvZuQoHcvV6bcWFBq2dNcS0pq5CGb1mjbSloM5STt9w4YIsefNLL+NwsEF5+kTL4JpiWtuiUBp8CEXL2FP2WZWyM0nAIzQX8swd0NddqJAmpeyMRRwmMV9hr30aCWLNh6OOs5a2HB+WkfVoFafLZCnrVkkG747IkchChXSRZmhFNCEQ+vjoOS0+Eh8Dj0f7jIjjAwDAfcvHx7emRuHUIXZW7/b39zc3N1t23kATcd0e0Lh1jRkO+OIwNI47L1++vLGx0VbPLaFwW1nh4eHe3t6XL19etmyZj4/Pv/71r0nUY4HriY2N/eKLL4ZvQmiVh4cHAgAAAGYk/I+Us79OBACYHPxec/DHQjeCYCMA7ksBAYva2jomLObn59Pe3mk1y9d3oUqltpp1e1FA/4o4939WuXd2IOoeLWHlzLu90Of20mUel0rdr7eg2Y3wiUxOXsVrKTpRZOcWgIhg7hPIu3Asv27atrkQyFK2RNYdOyafQhjfOo40KW0dOp1jZ/eRe0UsFtm57B1843R2qpEr4X/n9Hrd6NtTTg+CIHg8PvzYem/B/M5tjs8vl8uNj1/38ccfIsfg+eXzBTQ9bb94O3In5ck9TtiEu7v7okWLenp6cPAXB8fv+cWJx3zCmxDiTxA6ndYV71AAAADAFqlU6uAnkYaGBgQAuCscfGPC4joAXIIJ+N6+3R8R2b8sGrFJdE8YKbeumx4XzrrPgIXYU0Z3yE8cUnA4yG6sliORSQnl6ZZZsckyweHQygp5C2yxAQAANj30UGBLSwty0qR3QB5j5F4ck3t0JACNe9vU1ISfqNU2v7ebcOWygxypB4fCEQAAAAAAANMHAtAAuAoO+86JyO9MQhsmCNYaWooOHULTS6vI+1/nfvXbQbRWUVSAAAAA2OHr6/vll+XISY6Efe+OaezJdFU1cwYHAAAAuJdIsWxllNhQX3GpQYdf+UetlHl1Ky5Wtk5t/2i+dEW0WGWp1HbbuDV/SlGpUN2Nzaod6pJ9pDR5794UfklWRm7l5GuZqfgrMt7Pfrw144cv5jeMnRB8mUTJ/L1I1F1/cWgE5/ZouArcwBoAAAAAAMxEDzzwgLu7e0/PZH6yHxgylefY7SGTez71Pkz9uYtqBgAAAGY1Urwi/eDR949mPi4lERLHp2e/fzR7b2LIFH9/mS9Lez07M0XGt1eIDNmYmf3m9igvdDc41KUJkF6yqPiVOGDPQXcXKU05mJ+7a8VUOj9BC/6Je19PIfMzMsZGn3FOVknDv/7+4ftHsTd3DI/gPRuNWW06V0ALBIKFC8Xd3bqOjon3/gAAAACmkf29VqeSC2YCmN+5zdYcBQYGNzU1TmJ++/v7ceQax3/xo+X5yMeR6faf48fh3Zwn99zxtlz3fOo14DMak+7ILEAu5EIu5EIu5E577jTTXb+OQhKj/U/p8CN5/Xo3bI9og64yM9E/E90DXuIQmQx54VCvi9YaU62F6SsKreV4yTbGh7Tm/PD7GYWjl8Xfu9GYzaYnAC0Wi3/60//8xjfCLS+7urreeONgZWUlAgAAAO4K+z+nTiUXzAQwv3ObrTny85NUVv5jcvNr2QbasgbZclu/4RSnHodX/k76cXLtzrRHPIaWeDqytsW2696hkAu5kAu5kAu5LoNjmt31Co4sMVrWHSVDDYpu/8Hlz6R4RUr6jo0yMUmpFCW5Bw+XWAKQNtP9V6Ts2rExhLxekl/p8Fpdjjh+e1bi4/ioT7OzcidqQhyVmJKyMV7mZWitLzmVm1eoYDYOkW19M3Pl9bwKTvzjMnG34tThg3mXzNt6TKJLTNO7diRGib266y/m52afqmRqYprI2iFjFmsb6vPSXzxo2XSClKZkvZ6sysvXrUiOX0TVf3r4YO4lK6fwae5B5tSY4pmJVCvyF6sKT1WGbEyRqk5lZeVVqmyeHX9FRnbm44twANrLS5aVH70Xd0BVkrk9o0Q10QThs67IL9ElpkgLM9PzFMj2KFkd1aHxwBClqm8dsU+KjdGwOXq2J/T+Mw1bcHC53N//Puvrr7/+z//86VNPbd6+fedf//q39PSfRkdHo8ngSpbIIgLFLPMLliAwIkIWKGChu4cljv3hK688vzaQi6afIPa5rL/85Y2X1i4OXPv8j9f63c0TAwAAAACYLYKCgr/+um1yn0KH47+WADS6pztg3Nvn01jbcER+4O6FBgAAAABXIjk6xUVVSHLKxihOfUU3fs2k8qN2ZB/NTBRfv3jq4nWv+PTc3L3mHSDspL9pTq8oUUmTt8b7O7SLBw5M7kiRdV8sqees3Jubm263CRz3zM7NTPaq/zSvRCVO/PXRXFyISeeHyKI2pu16nH/904rr4uTMo9lbZeSkumRpOlmsu1hY2LpoY1Z+3t54pgnU3VpRefFiRb1BHCKT3tl0giMOiVqbtitFprtUcd0rce/7uKvi4Xriva4XniqsJ+P3ZptPjfSSyqJxlL++1SsxMzOFrK/nJKbvTbT0y8bZ6RSKyosVivpuZGhVVFzEKisUKoP9URo6a3Hynu3xK2VSHEO2OUq2RhXx47Mq1Wpl1ds4/r3y139XqhmVWUwjNkbD1ujZ6ur9aBpWQG/bltbU1HTgwME1a1b/4Adb3nzzrY8/Lujr69u16z9++MM05CyBbGvGK4+gsv/309+cV3Ej0n752jpu5VsvZRaqTGg6scSPPvfCo8rjBz662jsmiyuJiIoSdBW+d6YZTTOuRMKt/sN/XY3a/spvxU3H92un96QAAAAAAOaGxYuXlJVdQpMycvHyVIz5LeBJPJ+uWO2AeVsPNGVTrMeyrwgCAAAA5ggSNZRUdmelrNB9mtmAdlnSFq1MlHUXvrh1V6EKofxLVH52/OMy/qVKu+mnBtMLFdmFr0sdaJqiFIdfTs9toFBeBVV0FFd10GYTl6juyv3bUxosNy0srEeFb8qi/PlMIex6yf4X0/NbKZRfiTM2xofk1iOnu8QPSUw2N72dOSSnRPF6ZrzUn1+i0rWWZGeU4EhqhmzlxjGn0F1x+OUXzafAtLwi3p9/yWCu59T27btKcD341PKPPo5PTUEhyqC6mJedFxKyMuVibvalFdGJKSFiPAH4jKyfXWV+Zno+GbUrZKW4PjczffBsmbixjYkQr3gcp7+83TwYY896/Cjh0Lb1UdVRFYdf/H6Jl3jlrsytXp9m7C9kCnTXK3SI0lkdDVuj121rQu/HWxdOQwB66dKIjz762PJ82bJlISEhKpXq8mX5Sy/tfuihRV99dR05yaTvbGUHxi0Rl/WKY5ewOzt7kSuwBUFLAtlWVjmbmk+kP3UCuUSv4sQbCvxn1S/K30YAAAAAAMAKoVB469YtrVaLJsUSZp1Lj9N1XtNbDwAAADC7MXss1OcdzEZRqlOK7q2WZcIk398LUZWD+0F3q1q7cZIXZ4J03XC6SoccCUCbS5o3Y6B0qm7kZa8JpGutVJDxG3dkyvxJRIplXiSHM7SomaK6Vd3miroV+YdzpMxB/s53icTtUKrBQ3SK3O3JuRMdcucUDN34T0uXcD2kl2xrRlYiZb5bn5g0n4LKyuFD64cpO2dnrae2JsJLzEdU/dBg4L4Z7py1lVGy3S6la7hU0kD6kyndKZSisrBQMdGuGTZGj29zQtH9ZxoC0AKBAH9CwE/Onj338ss/tSTq9Xr86OUlwN8yIKf1KpuQ5JElkt4loaipqWshezCdu2Tt0xviAsVco6qpqvB4UTWzgFgc++Pn1/aWnOmSrX1EgprOn/jbmauDC4tHli83l7ekbtrzwloxV+DP4wW9kLXEiGPOnWVvv55bbZSs3f3ShiAuC5l6laffyvqo2VKPIGLr7udiFw5vl2FSVeX84Z0qpjZuYGz8urjlQd6os6m8tPB8ldISLucGrn36u7hpdq+y8syHheXNg1F0W+VtnR1grFmzmsvlfvLJp2PSv/Odx/GVdu5cKQIAAADAHCKTLa2trUGTgqOjlgjpmEeRSLR8+XIWC/Y/c5TJZKqqqlKr1dbGEwEAAABzAI431hcezChEyD9xB5qpSP/krPdfjzdUXFK0dtuOhVKtJdmZJfgJ3x/NDFS3ojC39WI9DrDbLuTg2TmGHAprM7FkjrUSw6M0re2CCU0+AL1p01P48eTJD5qamn19fYfTLbd5kUj88GNLSwuaDHbv1eretY+ui/NGzWVdEslCJpEV+OQvX02TNJd+dKZaHJu49ZUg71/96uhVI0scFPGIZCGvrOyLSuUjic/+NkL8i18cvdprKS++evqjM8qFsYnPvpIhZsr3ImOvsrq6Suy9xHthYJfyanWn0WRSNXUxcWi9SlFd3cv1DoqLDZTwcNzbEgI26ZsU1WyV+QML2z9qbYTkqjmdJUl8+bVUXuWHZ04bA9dt+PFrsYH/9dM/VWmZpn+bJlGWflTaJI7akP77uI8sXbJR3vbZuWbx96wzb96855/fiR9PnDg5nLh586a0tK3/+79vIQAAAADMIWLxQhzl7OzsQJM1vHPxhInAPtjxGQAAwP2Hok4vyHwAABAASURBVAxocDtoZpE0n8QplL307hHpHA7foS2gmUWzzAJsRE3cBBmSmBbPL8n4/vb8VmTeoTh65Uq7dU+iS6ObFq9I2R6tyjtc2OBsZBbXQ6kuHc7IGLXNBD/K5gGTODvrE0F1t+qQl0y2iF+i0JFimcz+ztfOt+twl4ZHT2XrmrkfTSYA/cADD+zb9yqfzz9yJAe/LC4ufvbZf//882K1Wv3Tn758/Tozc1u2PFNWVqbTTWZVOYvNQp3l1b27E6N6y7KVKNW8AJoljogL7C19PfONKhyVLb1qev2V5bGSk1ebcJ6xq/rEH95g9pc508Q+uCciQsy6qhRHxQV2nf7N/j8qcPnTV42/zzCXv9prUpafeLucJXkiaLlA+eE7f6y6E+XVVhflVuNg8Kag5etH9Ki3+fzJt88zz8SP7n71kaYP/5BrjhojffV7mb9ou2pexVymRAf3LAnyZlX1Mk3jrv7K3NXCqqs/eW55EO5Ss43yWpPNs4MItFlhYRGXy8XhZvzcEoO2RJ9zcnKLij5DAAAAAJhDQkPDrlyRoymwGmtWqVSFhYUIAAAAAMAOXetFRffWxF27LnbnNYgfT98Y0l15sL4b6ZD1dIpUtBp2WNJb/VO2rxST3Q40Qy6MStuxsTVHYa4K1edet90E0nXjyOpKmX9hayspjU+MEtuPKFMqp7s0dNZ7LnbnNHjF78rcs+J6Rt5hHJiVrogOwbFy/0X4YVFUfCLqprrrKyrt1KPamoyb1mVf7Jbtyj6Y0p2VvPWUnaa77Z5dt6rb4BWykmkXMQ1farA1QVT3xZyS7rf35hfFV6j4If5eFGX3rLudHFWGjdG4ZGP0bHXVgpRtzy/8tUzxSmJytmLuh6UnE4DeuvWHOl3PSy/9J4fDRPHPnClZt27tkSP/d/78hYsXL65YsSI+/t/YbPauXS+hScIRaOWZ4ydQkLa02bRhMI27kIt6u/RG8ytjV2cvivEe2sHZ2KvtHXzS1YuWeLPZuLw3l+0dtH7rjx9lMngSby7Xm4umgrvkiZ9slylz/jvHEn5GJq2ymR3x6JNrgxayWSzxEi6bPdT0na6alCX7f1ViqcF6eWSyf3YADcWdLTFoyxMcfR65IBq4CCGQhEoDBEjTUteg1NNMCs9HGopTtDilw5IyWEbb0lCn1NJoWlmaEyL9RJUTgtA1ayQtp8826Ke5C3Y7JxHyCETrtR0arYGedE/uVKRRdow46l6cFAAA3FNhYeHd3dobN26gKbi3+zXfD48IAAAAmLNUhZnb93ll7327aDd+1XnxwK59ha2U7fTWkoMHL2b/ejeTbqg/U6mi+A60QnW2GlZkFu3wMte17+CpBptNUOjTg1mJ2ZlHq1K6uylDPQ7xUovs1j2JLlmafhM3zWxFYqg/lZH5Ke4SP2rH6++nhQwWWrT7TWaRcPWB9d/Lt13Pi8wpHP07cwrdFTkvZuQ1UGSUnc7aOzuqoSQ7vz53x5tHmW7VH96wPuOSrYlADfnb/63h1Mb4EPJ6RSa1MfvNKIQm2a51fJn10UjOtD56Nq8ZBukviw/hdJbkFtbfF4uinQ5Ai8ViHF/es+dnK1eu+OlP//P3v/+fv//97C9+8Upq6tOPProqJubh7u7umpqa7Ox3pvjJQVn1cW4VQoLliG29gHMbJOuVpYVllUojmjRxzHMvbWaVZr1xpm2oaUHsj3/zUlRvdbV5A4+JOVEetn8eb2QMGqLPdwchkCWnrRdqlFoiMjZaeiKnoIX2iU1JiaQ7NEgYGynMy7nQwQlN2pIk0Ss1KDI2Vpqfk9+gR9OGE7Buy2apQck0N0HltEHfwQRv72KglhDK1idHGhqUtDBAKtSezsmr0NCT6gkh8JGESiQBUk7FsWPmSizuwUkBAMA9xOVyJRL/4uJp+PWmkYug4XEaHy0xaAQAAADMclRr3lZZ3p3XrYXbo4Z+U0pVmb01Knv8MTbSdZXZKSvypLLoRTjwealh4q0AKMXBROlBZq/mqGgcLFVUNqgou03oKnO3rjjlHxLi1V2vaB3RwKWMFVZvL+h0lwabXpErlsr8UatiqEe6S+krROnWileaT2GwuZH9MJ8CU48Y1dc3DN5osTIzUZZpPmzrCvOoK5Jl2ROdnaW6koxE/4zxXbU2QcwNAAtzFcw8ihPTSETpzHtz2Bgl++3iKyR/a9ToOLvt0WBGfPzo2e2qWBYvI68X5pW03h+bcjgdgPb05OHHtrav+/v7y8rK/v3ff1RWVt7X13f8+Hv4P+Q6RpPRhFhsNLgxM7NPh6nXZL+8UVX90du516YhmMsNfPKFH0coc3+VoxjeFIMlid3wCKvqrV/vLzPfjnDJsxERy0d0lT3YVcHiteuWdJUWVbNtlJ/E2d2vcNCZNofi8vM/RMD1CB6Pris4VlSn50jWb1knERAtBh8JTsorakEB61NifXhIKwgQai/k5ZUxMeKUZKmQ06A3jK+K4xMa6sMhCFqjRUKeoaWuQWPA9UukoRIBrWkwvzS3KDGvdx5ccE0IJD60gmmOFkauj+VxCIQTR5cxHyYIjY4NECB9h3awPZ5EJhUYaI6QY1DW1VmK4T7IpBIB0na0DCVNGa1tuHD6tNLAkyZvWRMqlJcZpGN6MtgZnsHAwyeuHFrHPfosDEr5BWVdwHrhqhGj79BJWRmN+4C7u7unJ9dkovUjvpCwHxNxNpck2QRB6PW9t2/fRuDugvmd2+zML44+P/bY+lOnxn7BPJXZB3fH9L5DIRdyIRdyIRdy0axD6RoqSxqQc3StlSWtjhamdK2KSodLT7ZLlKqhUoWmztl6nD47q0hx/NZdiSEk6eUfHb9WfP1AxXXqbrQ7XJsTZ80PWSnj1J/Kuzgdwz0buCMn4Y8N+JHH4129eu1//ucNDw+PzZs34ZTw8LDh7RFcwqSqrtMujHt6c2ygWLI8MXV9UG9TdWuv/fKSuKc3LPfjsgQRm3/9l7/8cq34zn3PTUZtl4kriVjOiFgsZva7YImXyPCrqNBALpu9cIk5JxAfw12+NT0tSFlaphWPKG/S9+qRtyQiSIAsW1Qv8WaP76oscftLz22IwMVtlp/E2d3HcOgZos+uQggCIletig7gEQQvIFLmg8OcZfk4+oyzOAIe0jN7TOhb6rQ+sasiI1fF+mjrWpg8gqYNiMPjEchA0za+1CI4PpHRAcggjF4VgJB0zRopj1ndnJIUKaANPFlyWrJMwKx3Xp+SJOPo9RxZUsr6AA5zHKL1zNYWtEZeUCDX0FbKIGahsEaJOyNkOm3uAQ7Lxq5ZFSlAtECWvCUJt4Y40nXJ66QcTYdBKFsVG8CbeCxkAQJHv6MjOEIeYcAdHdcTS2ei16yJFCIDJzQpxdIZfO7rLWexPmVdgNWb8zp0Ug7UMxctWCC4dcvQ29s3MtH+z6nO5uLK+/oMuCEE7jqY37nN1vwuXfrNRx5ZOT76jCY1+wNmw0/AdBk5tlOcI8iFXMiFXMiF3EnkAuAIqrv1Ys7LW7dmXZrMnenuDqo+7+Ufbj9YOXN7OM2cXgFdX9+gVqt/8INnfve7/bdu3dq//3WaZlbqpqe/XFx8GrlQb1Vu1tve6c9lHPguftVZmfPGO8xKYtZE5V/7Uxp+pb/64f4DZ1QjFhWrqj463fbKd9NfY6pTfvjT9LeVfhte+s0G/8F8/7R0ZreYptwXf14mCRKzvSXf/UnEdwczzeWvluXmxLz6wn8fS9Trjb3NVc1dRu6dpnlDXTUqS9/KLWO+0rBV3vbZAXAX8ULXrQvV1tHrUiQtSoGUV9Gg6DBnEALZulUCZVEDc03qGxQN+OUqpJGfZjYmNv8lwvFZlRKNyurs1m/QazUarR5pNMggJQhSKPWhFUVnKzpoeUODkNAjwkcqxCll8g7UwZOulwoJ5bhKCOHYMi1KHJ/GsdoWPSEzBIxoTttSVlGhRB0CyRocHW7Q4viwgdAa9B0V+XKNwf5aYeaUk9ag04dyyjR2S3J8ojc/G4q/lCM6Kk7UMWXH9wQxC6XNnaGVuM84rN2CpBJCI9fo9ahFQ0QOncXYAZvwpFoIR+qZa0iSNBqNOHqIvwG1pPj5STDLc5OJZrGYq7K//7aHh7s5xcRijfj2cejliAKDh2BKpbKtbfC6w01wOLg18v69UfG9APM7t1mdX5lsKZ61pqbG06c/R9MN1kdPI9j6GQAAAAAzGqUqyc4oQbMC1Vp5adqWXs8Gk7kJ4ZtvvvXaa//9k58YT5w4efny5YCAh/btexWn/+1vJ9DUact//e/lI15WvfHvWwef9zYX/vrHY29ebmr76OXUj4ZfXT26K+XoyPKnuWKJN1IpVeOWE/dW56an5I5Mufb280++jaxofnnzR9bSlWde//fSdyQSrl7Zph25YwZu+g//bUS/TERFb79VdHWwbZPN8rbODoC7iNbUVZS1KJQVyshoacfZs+alz0woNmlztP503ukWAxP/jU5exbmQ878tKGBdSnK0Nk/OFDIoT7+jQILIzdGON0eY106bw6W0voMJdXNGpJjXUhP2jxoqYyvkOljKchTu49m8Ills7JpVUglddyInv05vbywuvJN5AU3M0FFRlHdaaZiwoKWTg30m8H8cYYBUiiP4hga5M7tmjzqpKdQzp/T29qpUg7+4dPv2bctv6gw/GQ5EDhXod3f3sFrSUhUCMwzM79yGJ6W8/Ivubq3rwsSWsCmEoacCQs8AAAAAAGAqJhOArqqqeu21zF27/mPt2nhLytmz5/7nf142mWbipsWmXlWzSz9vmrTKZmtrlU2q0pw/cl945dVXWS//4mOlaaLyANxrhg6FOZqMWipOt1iSmOhzyiriQp55sTOTwGF22jAvH8aPBI9D0AYtYvafQFrEE3JorcHRFbg0rac5QgGBNMgnen2k4cLpOoPeMJgiEHIM5lXKWpqQ8HBkmg5Yv2WNvuBYmZUyjiF4Qp6+7vQJ+VnJui3rA4ScOv3EYePpQnAEPOavW9xnWoOj0LRGr0UVp4taaIE0UkIPnoU5rOzM38q0wWo9cxxFUZ6e3HnzOEbj4F+sWm0X/g9NN9wESbJ7eu7XuP49AvM7t1mdX+QCA0P3yht+REOroeFxWh4RAAAAAAAADptMABr78ssvt2z5oZ+f34IF3lptd2vrfbVs3CEs8aMv/GRTEFdZ+qGiE24nCGYnQhgaK8Nh2zVbdq6haa2i6MQFpUKhT968MxIHSg0Np0904JCn/IIyOenZ/yAQra07nd/haAy0X9Mg18jWP/sfTFV1RSf0OCyruNCSjFPWM1UVncWRWqJBoYlcn/YfuDzdUZavsVKG6adPdHJStA9PKOIZ0nZGd1Tkn2oZfzIC6fqUVUIDDntzDHX5GpdEn8f35ERZh6X16M071wl4qONCBXMWdXjQ1jODhs/rwglL4N+gkdfReHCjaQM+8GNlwBMTnRStsVbPfeDmTS2Px2WxCIPBVV8wcrnzCILADSEQ7DUoAAAQAElEQVRw18H8zm13YX4thjcshkcXPQIAAAAAAOAgN4JgIwDuSwEBi9raOiYs5ufn097eaTXL13ehSqVGANhF+MSmrOeddWinjplCLBbZuewdfON0drr23eHh4aHX6wZ3ZJlWODTJ4/H7+/sRuHdgfuc2l86vl5fgxg0NAq70wAPC7m6tK2YQAAAAsEUqlTr4SaShoQEBAO4KB9+Yk1wBDQAAwFEGvabDcH9sjwEAAPdef//tefN4CLgSHmQEAAAAAACAY9wRAAAAV2I2LymSayAADQAAAAAAAAAAAEfwpSviV0j5aG6AADQAk9ff3+/uDvfhAXMNvqphdwIAAAAAAAAAADMTKU05mJ+7a8Vcic5aw5elvZ6dmSKbI+cIAWgAJs9kogkC9rEBcw1BsPC1jWYbNzc3F+WCmQDmd26D+Z3tXDeDkAu5kAu5kAu5AFjhJQ6RyaReHARmCYidATB5JpPJwwO/iUwIgDmEIDzwtY1mm4GBARflgpkA5nduc/X8coQS33mG9laNYfilJ93V2qE1f9dGcHiEQW8gBP7+hLpZY2Be0/qJdu7nCCS+3qirXak1TEOx6XKnOST0F+EnGr0T3ye6ebij/tvWxtPN3R3dvm17pF03g5ALuZALuZALuS5CSlOyMhOpVuQvVhWeqgzZmCJVncrKyqtUUYgUr0hJ37FRJiYpleLT3IO5Ja2U5Zj4lLSUxCipGKkUF/NyswsrVchOPcwhI6sqyT14eLAqm316PVGVc0q1cuPjIeT1kmxcvmF8PcNdImVb38xceT2vghP/uEzcrTh1+GDeJXPD1ro62LDVLpmbTlbl5etWJMcvouo/PXww99LgWYujElNSNsbLvAyt9SWncvMKFboR9eB+VuSX6BJTpIWZ6XkK66NH2h8lmwNipWn+iozszMcX4QC0l5csKz96L0IGVUnm9oySbtujYaUe89jFK/a9eLDScjrSrVmvM6+zza+duQbsDbjV0bM32v4rUnaZR7Ukv5I/ciicuJBmJFgBDcDkmUw0bMEB5h43N7fZGIAGAAAbOL6LRAQv8JuRS5cvD/Xl8HwXedO0KDxEYF6IQYgWh/jyCEFgiL8nTuAErngqZXPCcl8OxzfUXN56nd5BvkzYmiMJCQkQ2lx842CxaWPQ65G3yJvgBIYH8niB4f6WmzFyfMOWLV8esWTxkqVLmW6MOzUcYHZzx+FnNw9i6MOBBwt/HYnjzkwayYbVaAAAAOYa0ksqi46SofpWr8TMzBSyvp6TmL430Z9E/Kgd2Ucz472uF54qrCfj92bnppt3esARy9ez965AiryDB/MUXo+/mZudIiNt14NZqkoUX7946uJ1r/j03Ny9djeN4IhDoh5P25Mm675YUs9ZmZ6bbSlvs0v8EFnUxrRdj/Ovf1pxXZyceTR7q4y01VVkr0tM02vTdqXIdJcqrnsl7n0fp4stZ52dm5nsVf9pXolKnPjro7n44MF0cz0VODl5z/b4lTIpSdrqqt1RsjlF1pvWKRSVFysU9d3I0KqouIhVVihUBrujYaUeStXaLV6ZsnFwhwsyJD4l3r+7tVWH7A24jYG1k2519GyNNm73zaFRlSZvjR8aIGcvpJkIVkADMHkURXG589hsltEI0TowR7DZbIIgdDo9AgCAuYM26AmBP7umdsDXl9sjCl0uUtZUjlzkTGub67uWCzlER+uVqqr2jivtROAKfw6t9RVx2lvNq5c5kqWL0bUrSvMLuk/dI/L/5qMCr/lurVXtLXdqcrCYy86Upjnentw+As2bh18xO4XRBIfnyeEQHj6+pivn/mVAPF9fllqNfH157c3M3/buLBZJINpouu3uMXBnUAYGcPDZw41JGEB3aTUaAAAAcBdRBtXFvOy8kJCVKRdzsy+tiE5MCRGTfK/EZFn3qe3bd5WoEMqroPKPPv647OClS0gc4o/qcw9m5SoolJ+fm2muhB9lox7UQJGLVibKugtf3LqrEFeVf4nKz45/XMa/dElnp1PdFYdfTs9toJimi46uYMorQmx1iXG9ZP+L6fmtuE+VqPDNjfEhuYrrVrvKsNWlyqGmXzQ3zdS0It6ff0lFdVfu357SUKlg1vMW1uN0WZQ/v7BbjHvWXfjydnPLhYrswtel5uGw3lXcDZujZHssrDddmZ+Znk9G7QpZKa7PzUxnzsOCb2M06m3UU1F4UbVxhWVCyJAVj/tTFw9Wquycha1rAB9gI520MXo2RrvbPDunBmfnzqhO5kKacSAADcCU3Lyp9fERq9UaBMCc4OXF7+hQIQAAmJ1u375t5ZeTOD6BgfjLYk54+G31la9pdd2lK9Xtw5FWjtA3KNhdz1vky0cCZa2B5oj8Re3X9AaDCPWou4bKGZRXroyok5jH4yD9TWU3m+frzWnVG5wr5hIc/+WPhHsjtZrZUkTEIwztI4PsAybEly4Na6u5okc+S8OR+kq9JeO2yUT1M2ue2ajfeKf44MMAHlP8MDoCjQeZSQYAAADmFvNvB5FeHNJLtjUjK5HZ5MJLJiZxUBrnqBSFhddT9ublR5UoWlWKi/mFJQobO0gM/pYRyff3QlRlt+Wf/25VazeyVGUvbtitUunMtVI6VTfyMpe31SWmYorqVnWbD+hW5B/OkeJGkM5mV212aVTThm78J4fDLL+lWisVZPzGHZkyfxKRYpkXaU4nvcR8RNUPtYwPNEiRndFT2R4lm2w0bf8YK6Nhqx48SkMR6EocT5dSFw9XDvbT2WvA1oDbOwUro22ZHd3w7Kh0SGp31iAADcD95MaNm3w+X6ebTe98AKzCVzK+nhEAAMxaOCo67uZFhuZLxc0jE9pvjHhBt39Z3G5+1thkSWkYXE9Udb7dVjPMiunLl5rRRBwsNl0MrV8Wt1qetn/RPqIX9V9+UT+yYFXx6FMbYILJt40jo+P9dP9wrql/bEt4jCEADQAA4H5AdSsKc1sv1jNrVlUlGcmJF1NSEuNXJG9M27F7R873k9Mr0N02okujw7FUa0l2Zon5qdWulkxioRHpn5z1/uvxhopLitbusdF2ciiGzERPOXa76oWmt+mJDY+G7XpUQxFosS4kfmT82dZZ2B5Y6+ndUzuFuQUC0ABMlclE6/W9IpFQq+2GnXPBLMVisQQCLxx9xtczAgCA2cxg6PPw8Ojvh/Coq3h4uPf13ZWbKgIAAAD3AEUZKNWlwxkZVjY40CkKszMKs5mdN3a9//7WlChxhcp+VTgAOrQemuSTzEaeyD7Si2T2UqYs5ZG5vK0u2VsPPL6rJcz+Dc51iQxJTIvnl2R8f3s+8x03Pz4reuVK85l1t+qQl0y2iF+i0JFimWxot2LrXeVHIWfZbHoa61EN7sKx4rpURl1MvxN/du4aMA+slfSLrc6eAtU9YnY4HD55pz9OX0gzDdyEEIBpgOPOHR2q+fPncbnc+fPns9ksuDkhmPnwVcpms/EVi6/befPm4WsYos8AgDmgt7cX/0OMgMvg4b11qxcBAAAAc5Ku9aJC5Z+8a1eiTMz3j88oVCjytkpJZiFtrqL10kHznfNIsb/UC1GqbsNEVXX7J+7alRwllSWmpW8M6VZYFtLaRi6MStuxcQVTftfGEEN95fVum12yWYftrjrbpW5dN44zrzTHl/nS+MQosaVZqvViTkl39N78ovy8/MLcreLBeKizXbXDVtODufiEvEJWxidi8Suk/MnVY96FQxyfliLTXSy8E3929hqwlW7/FMajVIpWw+DsRCVv375ysPxkLqQZB1ZAAzBtbt7UkiSbxWJxOPNYLMLDwwMBMIP19/fjiDP++sRoNM2+708BAMC2mzdvLFjwAP7LDdZBTy8PD3ccfcbDiwAAAIA5S1WY+eI+r+y9R/++G7/qrsh5MSOPuVVe66XDeYqju49WPW0u1l2d8/LhSh2S2a9qO1PV20VMVZ0XD+zaV9hq/5MX1dnavSLzwx1eCBnqT6VnnmKattUlG+FMykZX7XTJZk2fHsxKzM48WpXS3U0Z6nFcllpkyWnI3/5vDac2xoeQ1ysyqY3Zb0bZGT3S+RXQtpu2NF+SnV+fu+PNozvwq/rDG9ZnXJpMPcwuHLq0tIjOU1kj999w8hqgdFbTKcpe01b7WnLw4MXsX+9mZsdQf6ZSRfGH+uPshTTjuBEEGwFwXwoIWNTW1jFhMT8/n/b2TgQAMPP1XejgG6ezU41cCX/Ho9fraHr6V20TBMHj8XGAHoF7B+Z3bnPd/I7E5XJJ8+8q3h5zBz3gPMuvdlGUobcX1j4DAAC4N6RSqYOfRBoaGtCUkWKpTIzq6xt0dy3QR8p25edvrX/x+wdVixah+orKVt297pKlXb5/SIhXd72i1catr8SJ2YVv+ucmJx9UDPZsuro6YdMurWdazsLppkm+VBa9CMf1LzXMiluNOfjGhBXQAAAA5gI3N7eBgQFX5IKZAOZ3bnPR/PaauZshMDW3zWzluu4dCrmQC7mQC7mQe69QqobKSdy1bzroGipLrIXQ71WXKF2rorJ1bCopjt+6KzGEJL38o+PXiq8fqLh+J0w7XV213vTdqmdazsLppilb8z+7QQAaAADAXGD/59Sp5IKZAOZ3bnPp/NqPnIJp4boZhFzIhVzIhVzIvZ+oKvJyUPcs29yX6m69mPNyYW7epVmxXhfcIxCABgAAAAAAAAAAAADgnqJUl3IzL6FZglKVZGeUIAAcAr+QCAAAAAAAAAAAAAAAAMAlIAANAAAAAAAAAAAAAAAAwCVgCw4AphNJkmw2iyAIFovw8PBAAMxg/f39JhONGY1GijIiAAAAAAAAAAAAgOkGAWgApoebm5u3txcO5yE0YDD06fX07dv3880TwCzg7u5GmLHZbC53/s2bWgQAAAAAAAAAAAAwrSAADcA0YLFYCxYIuru7zQFoAGYH/B2J0WjC/yHzNezjI75x4yZcwwAAAAAAAAAAAJhGU9oDOiREWlDwkeW/Z55JRdOEK14csXyEJX5cNJ24ksVDVS+WWKmaJY794SuvPL820KFmWeKYl/6ER+DtPWv9WGiKnGvaKrujxxIEypZHBIqn3FEwEo7c8XjzNZobELkDs5fJZFKrNTweF1/PCAAAAAAAAADAJPClK+JXSPnoLiKlyZm5eQe3Rrmu1eluwsooTVcTd2E0wGRMaQW0Utn2i1/8Ej9JTX1aIpGg6cEN2pz+28cX3knoKst88Tdldn81nCV+9LkXHlUeP/DR1V40AUFE6isZcd7m5/rSzB/vH1c1VxIRFSXoKnzvTPOElS1/LuPHEcq3Mz8K2pr2ygvG/37rvMqEJs+Jpm1UYG/0uEtS9/zmcf+u0szd+8vgd+2nh5ub24IFAhx9RgDMfjpdj0gk7OhQIQAAAAAAAAAATuLL0l7PXvHpD5MzL+nQXUJ6yaLiV4q7czm5yEWNTnMT1kbJuSZIaUrW64kN+188OHacp6seMM0mH4AWCAT+/oNB54EB5OXlFREh+UENgwAAEABJREFUs7xsbVVqtZOOb/ZW//G5pD+yArdm/Tb26q9f/lP1hCFljC0IWhLIdmjdsLZs/9ak/QiJ41/9/VZrBUzNJ9KfOoEcoq36467BSsoK0ZQ507R19kaPJV4SxOtsamUHRki4ZVpHxhVMyNvbq7sb/p4Cc4dW242/U5mN+0Hjb4MGBgZckQtmApjfuc118wu5kAu5kAu5kAu5cykXWKOrzEz0z0SuNPOa8BKHyGTIi4PGRpmnqx4wzSYZgE5NfRr/NyZx6dKI4efHj7+H/0PTSRz74+fX9pac6ZKtfUSCms6f+NuZq1oTd8mmPS+sFXMF/jxe0AtZS4w4ittZ9vbruUzklbtk7dMb4gLFXKOqqbzweFH1BBEVlmTt7pc2BHFZyNSrPP1W1kfNw6uZB6tidVaVVhkfSQz64u0/nleabDRhvauWegLXPv1dXJ7dq6w882FheXPvxE0Hxsavi1se5I06m8pLC89XKScXOmYtDJUt1Cv+ViX57pIlYpaieSpLte+uNWtWc7ncTz75dEz6d77zuF6vP3euFN0jJEmaTLTJNHuGEoCJmBgsfG1TFIVmFfs/p04lF8wEML9zm+vmF3IhF3IhF3IhF3LnUu40Ypa+ZiZSrchfrCo8VRmyMUWqOpWVlVfZ7W9eE7vvxYOVOmat7tbXM1dW7Hs5WyHG6cmqvHzdiuT4RVT9p4cP5l5qNX9oIv1XpOzasTGEvF6SXzl65wdSvCIlfcdGmZikVIqS3IOHSwYPkcanpKUkRknFSKW4mJebXVipsvUBjJRtfTMzXjHYI+bYrVmvM6+zFYu2vpm1Q+aFEw31eelDBezUP7jid9zZ4VekOCoxJWVjvMzL0Fpfcio3r1ChszTuXBM2R9zWKDnXBLkiIzvz8UU4cOzlJcvKj96Lj1KVZG7PKOm2Xo/5lMdPHN9mParpmjgw0iT3gH788cScnNykpCet/veXvxxbv/7baHqxWOKgiEcSn94Q1FtdqeTFPvvb155ewkXGXmV1dVX11TY9MnYqr1YzLxRNXTgOzQp88pevvhDD7Sw7U9rGjXj2lYwfLplgibRJr1LgGqqbe8VBgRIee7htSeLLr77wqHdXVZVKvC51c2xE4EJml1QbTdjoqqX8b194VNxVVfpFl3di+u9/O9wle02/9kIct6n89BeqhbE/fu3VHy4XoEnhBkZIjM1lVZVN+oWy0IWzaZvXefPmPf/8zs2bN41MxC9xIs5C9w6LRdy1fx0BuJvwtY0AAAAAAAAAYI4ivaSy6CgZqm/1SszMTCHr6zmJ6XsT/UnEYdbESr0Gy/HxC9kiEj/D6VFr03alyHSXKq57Je59P3fvCjFTImrHm0czE8XXK0pU0uSt8f7kcCM4K9ucdfHUxete8em5+BAm9IpDrq9n712BFHkHD+YpvB5/Mzc7RUba6iqlau0Wr0zZKLNEbcmQ+JR4/+7WVhxe7W6tqLx4saLegPssFXOGT852/bbODh+SnZuZ7FX/aV6JSpz466O5uN9MEeebsMrOKDnZhE6hqLxYoajvRoZWRcVFrLJCoTLYrsfGxNmuZ7omDow0yRCDQCBob++wlatUti1YsABNP2NX9Yk/vMF8GXGmiX1wT0SEmHW1ufzE2+UsyRNBywXKD9/5Y9XQ6mCWX1RcYNfp3+z/owInnb5q/H3G8ljJyat2N4nWVhflVuM48aag5evvpLK8I2KDesv++P/eKNci9IWS/fuXAs3pYutNNNnoqpIp31v6+q/eYHpZWHX1J88tD2JOwWSzaYT01e9l/qLtqnnVc5kSHdyzJMibVaV1fsktNygqkK080dzZhJTGZ5cHcguVs+ZX7AsLi7hcblraVvz8xImTyBx9xi/xtyBFRZ+he4fFYhkMfQiAuYWmTRzOvfxqBwAAAAAAAABcjTKoLuZl54WErEy5mJt9aUV0YkqImLS3FQPVXXH45RdzGyiUV4kK31wR78+/1L1oZaKs+9SLW3cV4hBQoSK78HXpYHHSnFU4mJV/icrPjn9cxr90CYlD/FF97sGsXAWF8vNzJ9gxQlVReFG1cYX5UB0ZsuJxf+riwUpmoW5rSXZGCQ6XZshWbhxxAOlc/Wbdlfu3pzRUKpj1vIX1+OxkUf78QpVuepogbY8SopxsIj8zPZ+M2hWyUlyfm5leeOcORjbqQdYnrtJmPdM2cWCEyQSgw8PDhp//8Ic/wI9Hj/5lzHMsLCy0trYOTStj7+DOxcberl60xJvNRshGKJbN9eayvYPWb/3xo8xLnsSbi1PQpOAjWUZll6VpU1dvr2XLBbtNWOkqUx71dumNlnqUJft/VTJR0yatspkd8eiTa4MWslks8RIum23vrO2cg2R5EE9V2tRl6mVVqdhPRgRxz1fNom2gLXFnSwza8gRHny2J9xCLRej1tK3c25JF/RGRA94LEPsefSFmpNy6bnpUy92V1xGYi+bPn4+/BSEIwsNjgl9n6e+/TeO4ssl469bEX5ngkrACGgAAAAAAAHC/4UxUoFul0pk3XDB04z85HPxZn+T7eyFK120YLoCGA9DmrMrhrNZunMRsN6xSFBZeT9mblx9VomhVKS7mF5Yo7G3koFMMR6ArxSsel1IXD1fau3O8zsn6ERMFrlSQ8Rt3ZMr8SRz6lXmR5rObribsjNJ0NWGXlYmzY9omDtzhdIghODho//7/h58sXLgQP/r6+g5nDT+3ZGVl7d+9+6XGxiY0E+iVpYVllUojmryhuC8bhx1d1MR4gtgf/+alqN7qavO2IpPH8l6yROIduGHPgbX4DBZ6L+TKJNyqq7PqRoQjY9AzIfqMeXh43L5tfQuO24sC+lfEuV+57P7lJWQwoHuCw7m90Ld/1Rp0qdT9egsCcwhJkny+p16v7+u7hePFtq7DYe7ubuY4tYdIJNTpdBRl7y8UXBsuiQAAAAAAAAAAuICqJCM58WJKSmL8iuSNaTt278j5fnJ6ie2YsmooAi3WhcRPGH92vn5E+idnvf96vKHikqK126GIqtNNOO8uNDEHujRbOB2AxgHlpKQnCwo+6uzsxC/Ly8uHs4afW7JwMXQPGU34f6rqj97OvTblO8T1dnUh76BAb5ai18TyDgxcyGbZa4Jlp0uIxR4KZAsWr123pKu0qEpls4MsSeyGR1hVb/16fxmzXQZ3ybMREcvRZHgviRL3Vn+U/TdmtxB20PrnNkcs8WZd7Z1ld8/DQWcca8NP8vM/RDNbf0Skh7zCrfWeLj02GNy/ana73Y87AwFoz7DvpG6KpEpzjpe2TebbHLZfZGwQqa69XKuZ3m+ZJoE0U6s1jh+CY8pG/BcQMvX1GXDkGiG3WXePQQAAAAAAAAC4Cwz4oxKH5CBmMw7zWlmDwd6HJ4pZKEsOLp7mcPgjFtdS1IgsksRZdz6H6RSF2RmF2cx+w7vef39rSpS4pNBOBHpwF44V16Uy6mJ65cQhT1v1Wz07MiQxLZ5fkvH97fmtuAw/Pit65cpJN4GcG6XpamIaTd/EgSFT/SXrs2fPWX0+FVzx4iCJd+BCLpsnXrJ8OUvVefVqm/2luiajtsvElUQsX456kUmvbLqm6lVV12k3xD29ofqdwureoA3pezb05vw068xwtLdX1annRq1d+6ixuZfZWKOprrmXWSbMZbMXBjIPTNu9pi5lXbOqurC8N+O51w/GVqu4EjHXaDR3x2SjiS5bvRwsvxmXV3KjUn+8NUL5VunH5jyW2GrTXb165C2JCBKUVWlZ4oi4Jd5sNJnREwRGSVDTiaIyS7RbyV274Vkcgf5IOfveJDM/9Gwx4CVwa/8aPzH86nf931hqtYzHv65wXv358m8u9RZYv7Nkl1Zb9c8rtgpYcpNXvuwnCrV6eJu6Lv/i626dHQPLH0YOYPut27t/V4wI/0NA6ZS1xe8dPlLc5Giwle2XwBwsxAfranP2ZrxX24MmAYeJd+7asWl1MKmWn9yfeeCTyVUzvtqn9x/YIVE2kQl/Cs58fl+x0zFoz/CkfYfSJWV7N+18r8m5g9lBT+3bl6Q7vOfXpRrm1Xcy921SH9qTdd6J+PEI5uAzW6cbtTGZp6dnUlKSyWT87LPPe3p6xrSfsG3H03ES1Faac+AIDr/rdD18PnMDBYhBAwAAAAAAAMAo1HWF4ro4ZdeuZFVOq3/KrkT/7pLKVtsbQ1MqRathR+KuXRe783D57SvFZPdglq71oqJ7qyWrQfx4+saQ7sqD9d3McuPswjdDSrZ/P72wFYn9pSP2e7DFvAtHYnxaCl93J/7Ml66IDvEiSf9F+GFRVHwi6qa66ysqqXhb9ds6O1LXjbxkK2X+ha2tpDQ+MUpMTrYJZ0dpck10q7oNXiErmcKIKX2pQWerHnvDaq2e6Z04MGiSAeivvroeE/OwTtdtNXflyhW4AJokbtDm9N8+vtD8fGHaz6JQV1nmi78psx+BVlV9dLrtle+mv/Zd/EL54U/T377aW5Wb9bZ3+nOv/SkNp+mvfrj/wJmRa417r3504nzEC1t/9gjzylj99q7fXU186Tcb/Afz/dPSo/AfTbkv/vRkc9mBXTvPxy73Y6uu5hrjXtmzxFKF9SZsrYC2lOelP5dxgOmmUVn6Vm6Z5W8NbuAG601/lJsT8+oL/30sUa839jZXNXcZuZMYvWr/iEBu15m6rsHz72qqVrI2RAQKzqhmzY0IZx02icyLtW1Fn4ezbEWfh7NsFbCk24o+38kyGh3dhJoUBYUH82uKS9uQMCxu94Ew/rZnssodiwAbderLl+VIJIxJWh0WxEeT4hmze/++JKr4yL73+HFp2zJfU7f96LB86iFofP5N7+390eXLSjJ4WTiO3+L+Iuf0yI/vTpWT6stNTq9/Nuo0lGRZXEL4wdLSHrYoLCkujDyk0aFJ4vM9R6599vf337x58yOPxObk5BIE8X//986lS5f++te/ff311+Z8/M3AroxUUenxUpTwdMbuxtQ9p/HBOH4tEgnVaghAAwAAAAAAAMBIukv7d6WTmelvFu3goM6KnPTt+5gVrrY+VVOtJQcPXsz+9e63i3YjQ/2ZShU1/IFYVZi5fZ9X9l4mC6HOiwd27StsxZ/CWi8dzlMc3X206mlzse7qnJcPV07wGZHZhUOXlhbReSprOP4s2/H6+2khgwUW7X6TWbRcfWB9cqbt+m2cHfr0YFZidubRqpTubspQf1GhohZNtgknR2lSTVANJdn59bk73jy6A7+qP7xhfYbCRj3fy0e2Wannkm56Jw5YuBHEREtqrVm5cuXWrT948MEHreZev379L39594svvkAzAIsrlngjlVI1XdsdC5bv/v0eyYcv//IjpWmSTXDFgWJzeQc3wGAJJBKuXtmmnWUbZsx0AQGL2to6Jizm5+fT3t5pNcvXd6FKpbaaZUzbwfrbu/hJ718/RbZxv/f42tVxdgqcOVdqpwDOfSH5HTuHv5X/LH40ffcZds5hNBF20NNHTk0MCwwAABAASURBVKZT+zbv/KAJ+X0n6/i+oIIfpWbJKb9HU3dvSwjyRGr5ycMHPzBHhNnWEpkQ8r4Th2JKd2769cjAtWfYutTUTXGRfqipvODkeydLrUdxBzuwf/PO95qQMGbTtkd1BYc/qe2x2hY7aN22nakxno3FBXIyXNJ28kixLvzpbeuogsMfMIfEpKZGqk8e/6TJRm89I5/auY6sqeWv3hTnqTQnapBlCfa2TZFBnlTT6fcOHS/Gh7OFMak7koKZHzeUZTlHPhnsPG5iU+pTCZHMyuLBkrYG1u87B07uEx35UephOT/uteMHIot3OhzZH23+/HkDAwN9fYNfsX7rW9/693//0cmTHxQXFw+X+fa3v52QsC4392h1dTVzRkGR4aTycq0ufMe7B2I+2Da0gnvevHlubm63bt2y2pBYLLJz2Tv4xunsVCNX8vDw0Ot1lm15phcO5fN4/P7+fgTuHZjfuc118wsAAACAuUoqlTr4SaShoQFNHd9f6tXd2qpzaNkOyZfKoheR1y0raGcBa2dH8v1DQry66xWtLjqHWTdKwAEOvjEnuQL6ohmaDUy9quZpiD0LliQ+GRfIZbHFEbFR3srcq12myTeByzc7U96kVTbDSmVwd/FFfnykU+ooz7Bt+w/sltSeLCjnx6RmHhBRqXs+0QVbSbS1rYVn5M79B1LJ8uJyOfKL23MoRmJjYbVRXStvJLdtS9+mOXjyXPl7WeZt5a13IHz3/gM7gxvPlaGk3UnLJFSB/OS5xsik1E26xvcKantI0aObUpOa5CeZALS1GorJsE2pO5fpaspqNGT4pqwDfMt5pe7bvzNYWVbWRMbsOhATlr5tzydKc+dIUVhCXBxZims0B6ojdx/4UypfXizX+eGSkUG7t+21tbEHPq/SRrQ7JkxypJEfEybS1ZY3TnJZN4vF7uu7EzJua2tbsGBBcHDw5ctVGs0NnPLAAw88ZKZUWvqNeprk5eb9VVI3iRqPy4fvk4qjb/PmTXiT59kEx9NxdN4VuWAmgPmd21w3v5ALuZALuZALuZA7l3LvKl2rE1FSStdQWTIdYe+7xdrZUbpWRWUrcp1ZN0pg+kx1D+j7jrGtqvB86Yfnr07XgmoAZhZ+7J4/F+ykSJGE33hkZ7ESSVITwqlzGXv2ftLGDus5fjztsUh+cVPM+MRP2mzsaUx68kmklh/fv+/0BPfv65Ef2ruHv2/fnkMf70G6y0d279x/Xiex0lZxbVhkMHVu/0s732vix7128pC9VeRs6zXgHF3N8Z/tPFxLxrxy8lDC6nB+cWNMXLDu830/2v1BG/J7NDU1HJEkMmrKc35dzg7bERSTOlwppSzI2l2sLJe3GT0jXz5+JCkBH25rBJjIupJMigmWlAvDJFTNe42T/baXIIiRCwZ9fHxefHFXbGzsG2+8cf78efxzWlxc3MmTJ3ft2h0QENDVNbQhvTBm9/6MyNqDO4/XDs8ATZsIwhPNIfZ/Tp1KLpgJYH7nNtfNL+RCLuRCLuRCLuTOpVwAwCwFAWgHaa8WHr2KAJjzKF2jvJGMeUwkz9h7sFxjZEtIRIpW7/3z57uZ35eR8Ek1Ipmw7PhEWzTyk0cKwnYfKJdTjTXlpSdzjpwst7Vauqf2k72biw8ExSTsTN+bmrG79Jl9OqsdYO5Cq9PpjMyd9HQT/E6U7d4OHmm+GR+TxMdFKWMPxfSu7XxO1nmbdRopxA/flLFrXzA+RhTMp5rs9aAHR6rVqTExYZGiYNR4pFbt9EbS1nV2dh48ePCDDz5IS9v2yCPMfvZHjhzZtGnT//zP7//zP39qKcMWPrr7wL64toM7930weusTN/zTHQIAAAAAAAAAAABwJQhAAwBGompOHtxTG8c/np6aFF5QK2dCs5SyYO8ze4rvLO9lh1lJtK1H/t7PNr+31zNoWULqrj173xDpNu/+pG18ObYwbFk4qb4sb2o6f/IAPy5uX1iYiF1qtQOWkLMljkwOBb8pS7B5OIcaTh5fQ5C1nlLmIy33bGT7RcYGUTXltdaWbXtG7ti3L6lt//Opz9ci8wpoZJeusbxWlxSTlECS6uI722A4jaZpgiCMxsEtgHg83k9/+tN169adOnXq/ffzcEw5Pf3lkydPvvzyy56enu3t7biMKCY1NVbCR/uLN+3Hwe/Uoe25xyymBgAAAAAAAAAAAHAFdwQAAKNRjQU5pergpLQ4P7ZR19im44fFhAnZbGHcy39+9/89FWY90XIopdSRopikpO8kJKyLi/Rjm3cfzvjz3w6kLUNN5aXFNWoc0jZaX7FMSr6TceDP+1IjPdlsUXhMMJ9SqynrbelwDj98NW7AMzguUmK+fa5R3VSrJpelPr06MiYpNSEYtV1WMltd2O7tWOaSorjUpxOChGFJGYcOZWwKJplIdNy6hISYcD7Jx0/N5+UpkjCNUhTFFoYnxEj4pP0hNapryxpR8Oo4iU5ermQCwH4J/+/jE68lRD514OO/ZcRFPv2nj97dETnhjhgmk8nDw2P4ZX9//759r3V0dDzxxBM3bty8cePGk09uUKvVr7762vAN1to+eX5ZsDTY8t9jd24O6eHhbjJBABoAAAAAAAAAAACuBQFoAMA4Rk3Z8YJGUdy2pGB2W/mhA8Vo05Hy2pryIzuD20rLG43IaqL5yJqCwyeVktTMA4cOHTqQHidh49irvLjWGLf3XXljQ/nxbfyyw4fKrK+b7qnJyTxULtp5Ql5bU3ooQVeQdbC4yWitLWNbac4ROX/TgdLay4fiyMEtOHouHz9QoA7fdujku5lJ/MuHDhZbdjy22dtxmJInlcE7DxWXFWTFKI9nHbncww5OwKHoQwczkoJJfuzOLPw8PYFTlXPoHEo6+Lm8/ON9MUhHTXRjZKOytrwRkSRzA0ImKs4mPUUiiciTzxeKRCJPT4lEIpJMvCPzrVu3eDze8MuGhoZf/vKVJUsWnzx5gjQ7efJkcHDwL3/5y8bGRvtV4XpwbQgAAAAAAAAA5pD+/v6Rq3YAAK6D32vDq9/scyMINgLgvhQQsKitrWPCYn5+Pu3tnVazfH0XqlRqq1nGtB2sv72Ln/T+9VNkG/d7j69dbe8GemfOldopgHNfSH7HzuFv5T+LH03ffYadcxhNBdszKDxSQrZdLm/qsZ84dbjaYAmlrG3rmaADnn5hElKtFqUdOZRUu2fz4A4bbL+wcBGlrGkas3WGE73FFQeT6nE1jOuoMAi31Di6ow5jeo8aG3UifLKNjZQkWKRrnKhFhiXQrNONuo/h/PnzH388ET8pKPjEYDBMWAmf70lRRsp23FwsFtm57B1843R2qpEr4X/q9HqdKzYSIQiCx+M7+O8ocBGY37nNdfMLAAAAgLlKKpU68klkwQJBV9dNWG0DwF2AYxHe3gtu3tROWBL2gAYAOMDY0yQ/3+RI4rS0VVuLHGirp40p5ykaU7KtVt5mvVpHe4srljtQzKhpkjuyB7bNRsxnOfhHU62DYWxL1BhHkHW6O0fgn65OnDjpWAUTR58BAAAAAAAAYJYymWg2mw0BaADuApIkTSaTIyUhAA0AmN16aj7I3H1eV6ND9w1L7FgkEur1vf39/TRtun17wP4h7u7uBEF4eLjzeDydTocD0AgAAAAAAAAA5pwxN84BALgOfq9BABqAGcHjX1f6v7HUVhZ+7NJqvQUCqwVwlp0Cltw2dZ2fKNTq4TgL3Q96mspLp38d9gyHY9BqNTWPwSEITxxZtl/eHKem8T8MKpXazc0NAQAAAAAAAMBcZDBQCxYI8Celvr4+BABwmfnz55MkefNmtyOFIQANgGtxXv25/QJV/7wylQL5F19H4H7VZ+bUIXM4+oxPbWBgwBW5YCaA+Z3bXDe/kAu5kAu5kAu5kDuXch3U1aX19fVtarrvFioBcDfhd9nXX3c6WBgC0AC4luFXv7OzAhqHp5d/c6mdFdA4+myrgCU3eeXLdlZAQ3ga3D/s/5w6lVwwE8D8zm2um1/IhVzIhVzIhVzInUu5DsJ1aDRdODrW3t6OAAAugN9favUNx8u7IwCAK9mKPg9n2Yo+D2fZKmBJtxV9tp8FAAAAAAAAAADMVSaT6dYtQ1BQ0Lx58xAAYPrMnz8/ODi4t7fPZKIdPwpWQAMAAAAAAAAAAACAOcVoNLW3qxYseICiDP39/ZQZfoIAAE7y8PAgzcxPOI7vvDEMAtAAAAAAAAAAAAAAYA66eVPL4ZAsFnv+fC6bzcLhMwQAcBL+5saIv9Ix0UYj3durRc6DADQAYDSCJ+DReq3BiV+lAAAAAAAAAAAAZiSDgcL/IQDAvQMBaADAMI4kNnnzGimPQAaNvCivSKG1FoUmBJEpOzeGcBCimz8+dKxCM1tC1QLZ5pRYbdGx0y0GNCWzdgQAAAAAAAAAAAAA7jIIQAMABhE+keuiORXHXr/QwYlM3rJmVUBDQYOVUC2tlR/7nRyHc1NSIq3UwhMKCL1GaxifIeAhvVZPj0kbt9qaI/BhatDopzWsSwhk61YJWooKJo4+ExyBgGMYcwoju2p/BGzXa3UErAyXa0YAAAAAAAAAAAAA4O6DADQAYBCtrSs6UafpwLFQWqnUIwnHyb8gOAHrUjbH+iADIgx1BccKBhdQC2Rb0tZw9DRPIOTRDQXHTsiZFcOET3Ry8poAnrnd0/lFCiaRE7B+S0q0kNbTHI6+4sSxoga9jbZ4AdEyTktFnQaHzaN9OirkHXbjyoQgdN0aYUvBROFnXFtSMrMGnCAMDQV5+QqbXbVGELllS6j8WJ5CSwijUzYHyI+dUOhtjoDV4XJ8BAAAAAAAAAAAAABmAQhAAwCGGLQdHeYnHAmO7naUKZ2LfRIcjlaR/7/HGrRIsm7L+lhJQ9FwuJduKco5rUQB69PWR0vqcDovdFU0pyLnjQoN8lm1JTnWvNqaI5RKCEXeGwUNtCAgUsrBEXBbi4D1Gq0gJWWLrIPw4dTl100QVraEn4uKlERAdDSqk7fYqJYnXRUrkOe9UdaBTyEtaVVAS36DnukqT35sKDHWxsLwCYwbAavD5cQIAAAAAAAAAAAAAMwCEIAGAIzGRGvXB2jO5tU5eWNTWttQ1xEqW7NewOFJBDwtb/jvF5rWa/Q4ZkvgP1AAk05weDyeIHTVeqEBcYQCDuLhUKvBoFV2oHWrkpKk2o4WRV2Dvb2V9Q1nz7bs/EGkvvidMqX9ePBg+PlYgx5JYqOjiQ4cgLZakODc2SNDefqdQ4OJvOFE3H8i1NxVJ6PC40fA+nA5MwJgDDc3t4GBAVfkgpkA5nduc938Qi7kQi7kQi7kQu5cygUAzFIQgAYAjEDwpOuSVxFlJwrqtE7GPgmf2C2bQzVlZXUNNI+Q+HAmOsCg72ioY9ZINyjkest+x/q6gkMtwoDQ0MjI9WmxDSfesbnWmPCJTlojUJwq4kSuX6/JL7LTXYLnI+QJOOvT/sO8DTMtR65EjPhb1d4I2hgux0dgFqA1g44GAAAQAElEQVTpfuRKHh4eI1/a/zl1Ermu7j+wD+Z3bnP1/EIu5EIu5EIu5ELunMwFAEwZwfMVEl0d2rsba4AANABgGE+6ZvMajjy/QO7AyluapglixDbROM7LMSgr5HUdNEcaStj/y4U26PU0re1oadAggTRSytMqmSqEsugAvUIuv6BUGngpUntrjQ0dZfkKpcaAGpQBPLu9pTsq8vNazAuMCWH0ukh7vdLqiUipD6+uwSBZlZYkPHssv0Fv0BsIIZPYQkikQhw3H+rS2BHAWXokCPDhKfS4pACZ1zzbYn24bI4Asy59nUwvL7oAm0IDAAAAAAAAAAD3LRxPCAkP9EZdzTUN7XpLyEASvjhQgNQ4pdXuRp6EICJ5g/RK3t9sBaDHV2W7OW3ztdpWx1YvQgAaANfy+NeV/m8stZWFH7u0Wm+BwGoBnGWngCW3TV3nJwq1ejjOQk4RBMRGB/jPC3hxWTLzsv3Cn9453WHzbxI9jp6ilJ17ExAyKT8+lFPRIW8hUtJeCtXq9TjyStuPk+rrLlRIk1J2xiIOj9BcyFcw7dB6LSFL2bkKB3L1em3FhQbbf4/RWqVysKaOlglCskyg27KdCGEIWBNp5689fcOFC7LkzS+9bNDTBuXpE+aa9XVny0I3b34pg0C0RlFwYnhj63EjoGm5cKFjy+aXf44zNRUnijrs/DVssDpcNkeAEEhDIyJobVlZA2wKDQAAAAAAAAAA3J8InxVbUqPoDjX61srlomPvnFfzIjY9lyhSK7XEspUPh+S983GzzdVwhGBxhED9ZZPWVva4quixzbVzQjdse3JRj1KNlq1cKT3x9ql6B9bJuREEGwFwXwoIWNTW1jFhMT8/n/b2TqtZvr4LVSq11Sxj2g7W395FM4Ppu8+wcw4jABwmFovsXPYOvnEcKTYVJMnW63U0Pf0ReYIgeDw+RRkRuHdgfuc2180vAAAAAOYqqVTq6o8YAMwCgmVbNvtcPFbYjAK+s2VF+4njNZ6PfGdp12ef1Ok5ku+kPdbz4dHSdhs/ZhM+cVue9Dx39BMbIWqO/7iq+iLGNuedmLZae+LYFxokXLHlKW/btY1qGQEAXMnwq9/ZWQHNefXny7+51M4K6Kp/XrFVwJKbvPJlOyug8y++jgC4hwiBv4hubZ8D+4YQvg8nrPBFrTVfVNVrZ0/MjBCGSFmtde1Ob+816QNnqbs8v7zA5ZKeK3UTb3bE8Qnzp+vrp3I/UmtTSQhCHn5kseHyZ1UjflHD3rvV4Q4DAAAAAAAAXErfXNO1bOXqZd4ozLer9qIeGbRfnGw1Z3G8eaintc/mT+0c34jFRPNntj/mGVrHVTWuOeRN0LQBcXg8Ghlo2sHIMgSgAXAtW9Hn4Sxb0efhLFsFLOm2os/2swC4C5YGPtDlG/+dcFRz8e9VWuFi33m0uv5K62B4ixf4raW+hKG9uqp5doSnCaSpOtfqvdR/4UDIQ2Lc85omzuLF82i6p/ma3sdydk1EGD4pur2m1XOxL8JZ9dcMkvDBrMDFngSBWq/1BIYzJ97UJVq62Bv1tFd/eWUwCDg0JlaymOhg2DJzc9e/RiI3tVaAY4V6a6MqQnp1k5ojQu1agS/7trf/A57zfLvqm1CYud3hbl9XzQsSIxr1NH1N+JorHOiZt0hs7vaVZnqepyfHOyCMpx+KfhK+S5dZTgpXZZm7a2js+V6ZJbM5nuvnl+MbJjG1ar39iZuGwHCRodzc7NC0DrfSpPa2VN7UhIIWe3N8Oe0qOnAJ0271l0PDy/ENDR/RpZHvozFZdPs1tcjf13wN4NkZ2sFeW3+l1nsxs/s8Z/Cqu6YefLeW1qBFQeYuNdEh4YMTHWHu8J3eWrJGdgkAAAAAAABwN9D6a1fql3770dVIU/lZ/Z1NOgkBTvRu/fSa1taRHN+lgejaRxMvMxpV1djmzKFkzoOrUx9GX9QgR7kjAAAAwAU4onnqK5evVJ2/VKuh+7RdfRx/fyFnONNXgAwGwpPHQbMD4R3y8OoI1Pw1WzzYcy6L6GqqbzcQBIc5jb4+DxGO+l5rR6KF8zmoR93FEQnIwRN/cKGI06XuQQR/oeXEvfh8Qt/To0c8AW/wu+ChMbGSZe7AYHMkx9uTM4/j6c3xGD+qItRaU92k7u3Se4YsDfE29N6ite3XuwjRgwt9x3SbJDio62uctZA7WCGXHOo2UyHHJ3x5CFIPLwfGp2nJFfsNVrXAb9z5zpbZHM/182vooUWLw0NEtP5Gc3VNF2KZ04emlUCDVQ1X/oCfiOi63q6m3YWD7Qq5goDlDy8LFIzo0rj30bjePuA+eA0IrS06GH4nsoberTfQYJfmC4cqp4c6TAxnDXVp9s44AAAAAAAAsxEh/Nbm1Zxz7xz8wzuX5q1+6mHLj/k4ZLzhew/rPz/2WYvN8DJPstzfcKVmol9rHF2V9eaQ4fpn2e981ur4b8xCABoAAIDL0Abk/60VIQt9Fkf4iwTEnQAY3aPHgT3C0KWfLXs80F31X54prmrtHu45xaTq21u1iINPjBe0iNdnECyOwmFffT/OYQ5iCwdP3KhV06LAEF9ev95yuLZ33A7EQ2NiJWu4CG5OpTdw/AP9OYbb3uNH1cAJXP7oysU8Wo2Dgzy1upfAceTF/t50b/fYbt90w1nhOKu7d7BCw1C3zQyaazUaUdCoCKM5d+gUurpvjD1fJmy99GEpbxb+epXr5xfp1V3egYIutUEY9sjKpctWLA/gDbaNW9GPnE3LOBtogf/iMH+Om36oXUrbUvXl5WYtjjIPdWns+4ggxvXWbfAaMIz6QZNm1j6vfXihcbiGwXerFzHYJZV2MKuPN9jhh7jDWUOVw54cAAAAAAAA3E3EPPx5y8D8cE8b+mjCcx5hDhmnxhFfnPiswc4P6IKgZSJ99TX7Ow6Oq2p8c7QBf0QSeuKPDQRPxKG7DA59JoCbEIL71925CWHvXz9FtnG/9/ja1XF2Cpw5V2qnAM59IfkdO4e/lf8sgpsQAufBTQin/SZ1hED68Mowz9bzZ67clS2kedIVS+mqS7a//UYc/4cjiJp/TO8OCgQvIESkqZ2OSmF+5za4CSEAAAAAnAU3IQSAQfg8vOmplQ/iuDPRd60475NqveiRZ3cmeOu1OBRsMmmvfPLX0vF3BSQEy1NSQ64cff+KvQ9rhO+4qloFY5rTIl7I2qe+HS5gIbqr5nMmVI0c6DUCAAAAZj83N7eBgQFX5E4LWttw6ZMGdNfoGy5dsl/C0PrlP9B0o/Utta7ZExjmd25z3fxCLuRCLuRCLuRC7lzKBQAguuPL9//45ciU9i8O/eoL+wcRgrClvNaLTRN8WqOtVDWuOaSv/+xo/WfIKRCABgDMMByf0FCepq5BM1u2ZgAzg/2fU6eSC2YCmN+5zXXzC7mQC7mQC7mQC7lzKRcAMDm05oucQ+geggA0AGCIQJayJbLu2DG5lvCJ3ZLsU3Ysv86JtYw82eYtkS0n8io0U/qVao5QGhnp09DRoumYjl/NJgSRKTs3hnDw37fNHx86NsXO3RUcn+ik5HURvhzUJf/LO/mW32axmgjuIkIYImW11t25XzAhCHn4kcWGy59VdUzbRYXrXP4tX2PLjfnSgPE1EwJ/Ed3arrdfw8RlhvD8l61cKlRf+aKqdbA8x3fZ2uVE1Zl/mE+TF7hU0lNTNwveM/cSL3C5pOeK3VFyZlLGHGjveph2luYM1V9e6TCg0Vf4pE8BAAAAAAAAACAADQBwCMET8GjzLkATJU6ZQXkhL2dcKkfgIyD0Gs3Ed7wieEKmpHYwTkhr5cd+J2eC6ymRyDFMW0jT4chGrgRHwCP02lG9GtOBiXo7bgw5kuhoniJn36GOiRLBXeUpCvT1nCfqqm9CYUt9Cbodx+lqvRczN43jBH7LklKDAhd74pSvm0yLgubRdE/zNb3PYt95tPrrHt+li71RT3v1FbXAnFJ/jZaEm59cGYz/cvyX/9vqpURrVU/jlVquuWbaEvhWawUi9z7RyvXhqOZi6TXa241JoVv1QnNVTWrvxb4IN3e9yzf+O0yZv18xBIb7EgbcJcOYVobxfP2Ja+X1vot9eO3aoOW+X1fV6k3qpi5fy10HOYHLlgraz6D7BOG7dJl5DAfnFw/dtcGJrmn1tAxv/ZWhva15gRHmiW691hMSLjKUj0ipUU88KVVW9sgmBGHLFpuvmSY6xFzsmloUN+Z6sFxphvaaJiJoEaJxc5bC+Nq7Mnaix54Rc8WOaJfjGxo+6jrE/bQ0h8ihrCuDVzjH9+GEkacwpqqZz93dncViubt7EAT83DslAwMD/QzaaJzOLdQBAAAAAMCcBz+IAwDsI3yik5PXBPCYWG7d6fwiBbPSz2riiENiUzZLG07kldkKl/KkyVtWafKPXcAFOAHrt6xDp48VtdDCyKTkWIlAyNOefienbLBOJj8lWkjraQ5HX3HiWFGDHgkit2wJlR/LU2gJYXTK5gD5sRMKPS65LmVzrA8yIMJQV3CsQDGpm4FxfFYlr9Fa+maTQLYlbQ2hpQVCAQ8pTx+znKr1DnCkSWnriNPHmGXLvNDktFX6/GOnlQYrY8jxkUVHSgMCBELDqvU8vUHbUlFRZxBaSYTbnN19NK1Rt3d5+4v9EGq/1i4KEnIGb0HKEYksKQ8uRJyu1i6RL4dERFdTrd6Tg/q0XX3e4Q+JlLf1PT340hdwvzan+Avb2j15HLq9b3guDa01l68g+kpVh4EXMJRIzPP2JPQGT2+6+crlKwb9l7Xdvg8vsqR4qC1VLeylUU8r7ts89WAZvf8KATJoCE8eF41pZZi+tblnadQyUfvfDbT2ypcaJk2jMQT5mnN5/v6ouZVYujyg6suW+2E7HIJjGUOxH2EZugV+HMu0LpyPLFkCTrPePBQcb9HgRBuaq2tEISyCM28oxaNv4knhIP34ISVYlmuGL/S3FGOpx14PHJGvJWueoakvcHPItRP13uGDVyNXPWaiiTtnNHzFNo9ot2/Mddg7fPkhAbJkXeuyFDW0Dp/Cw9aqmtk4nHkcDv5WxY2m++E3eqcIDyCbTbq5cXg8pNPBPSQBAAAAAICjIAANALiD4Agj1yT5GBBPIiTM8SgcMV0VzZMfe6OsA0nWpSXFBjQUNBisJg5VwpHEro+kL5yosBPA1XcolJw1UmFZRwfhEyrBIVzzr3xr5PnvyHGMdkvsnaIcoVRCKPLeKGigBQGRUg6HQDaWQRMcjlaR/7/HGrS4V1vWx0oailwaOKOVp3NylLRlBBQ4vGyjAwalvIFOjpTwGuqQRCYx1J1gTtbaGKK5xd3dDU0rHPu4V1vCubmh2yaTcaDfZKJ11LwlskVI9a/+/vnuPrKVyxQ1+sGUa73sQIm/t0d9q8HYT/d2ttG+33x4IelB3+6iTUaTuSavhxYvYOEU5MG6bTSx/Xz5LTep/sF2cP233dzd3Pv7zTXfvvRP9S29e4hkIdI39PffmmpXLAAAEABJREFUNokiooMqm/XufkzKV16Bi82V9zPdGjAf239rsIxWd5sc0N+41c8daqWXHxLKva5ouTXUmFFzs+9m3YXa7tusB8Jl4k5FQ3/gNyOCA2hTW8c/b/Z0GQUC7u2+m0x/0N0wU+ZXr/Nmhk6r8QqIYKb1Wgc5321gaGqY4lRXZ1+IeaK9Fy9fFuxrGNBUdPYJmZQm78CgiSZFb5wnDh89F7gLA7TlmqG8PXVCSzHEGn09KGqGplWwyO/6l628Rd439fPCmE7WItYDYy4nK1fsnakkHxi8eEZch82Wc+QsGLqu3PrR4HVYN3QKg839q3/wFNQPhATwSTwk3c11ylt2B/mezO+8efNJkkNRsFx32hiNty1P+HyBTqeFGDQAAAAAAHAEBKABACPQBk1LHY6kCjgSH3MCwaxzGtxjQq/RE6E8HACmrSUazPFr2ZqkUB+J/uwxuf2NY/XKOiWxRupToUVSCWop6rAZKTZolR1o3aqkJKm2o0VR12C7XlrbUNcRKluzXsDhSQQ8Lc/Zv+A4Aes2r5cKOEKRN52yU6bXyIvyy5Q2ekbT+NSZPGYEfHjm7RJsdMDQoajTb44MEHQgmVCvuGBeQ25tDLUdigtFLZpkn9iOC0XDy8etJs4GJMlG08rNzR0HtY1GmqIoN7dpjm5bheNl+Cyw27dv36yrxSmqbvygLm9mcvF3If/8u8pccDAFuX/V0tt+3dR3y6jWIjZJDtysK785ttam1sEn7f80PyNI9uCl0q+qq8MDxyaRarBm0v1Ws/yfaLA5RWmp+elgCkLl6hH1mvuGxpa5qRhsxY3V1tjTT7DJO2+M7gZFN8IpSN9cp0eEO2qVF7fKze3iPHm3pRTTn7th5syv1pJ9s3xwWlHXYNbQUPRr7kx0oWU63bVDKR2dI5qwOimk261xc4FuNStuMdcMGp5xfBmMvR7u9E0xODtouJOK0ZfTgJUrdvhKQyOvzKHrECFzc2jkRTvU7vApDDY3dDndVjXXD5aY6Dq5+/NLMrNLQvTZRfr6DF5egps3b8CtogAAAAAAwIQgAA2Aa3n860r/N5baysKPXVqtt0BgtQDOslPAktumrvMThVo9HGchJ+GgqrKloUFL+AhjaR/kNCZ+3aLlBMgChDyF1u4WoQYmAr0qVNKBAuiWIo2dlcr6uoJDLcKA0NDIyPVpsQ0n3hlcbT1yL08mKsvcOXFzqKasrK6B5hESHw5ylqHl9LFDpzkBSWkTbsExhrmk7Q7QmjqFNjIyOprG8eez98093fr6KOQCHh7unp68nh6Xb0GLoyqentxbtwxGY6/DB1F9jpe926g+NAvM7PkdNn6inZr62TEXdk3yFO7a/GLz53MNBog+Ow1/TzDmG4IBBsLf04xJpygTHuTeXrg7JQAAAAAAmAAEoAFwDSOF2GxkNHJe/bn9glX/vDKVAvkXX0f2Md2YfByQNugNhFDqw6trISRSIcIvaeuJyBy/7mhRyBuQZMu6VQFK+xtgMBFozrrYWISUBR12ChJCWXSAXiGXX1AqDbwUqXm1tUGvR4IAH55CjzsgQOalyATPh2NQVsjrOmiONHTMraZomiYIznT+jUfg9gQcpEXMLQsNepq21wFa2yDXrEqKRi1FRZb4s60xdBAvYN360I4LCl5spKGsAkXHcuRFNhdrzzH9/bf1+l4ej2symZDLmKOTPNwQAncXzO/cdnfmFzGRbo+7s856zsBvCneGlUFzM0ek3ZjNYEbFoHFImiTZvfA2AgAAAAAAE4EANAAu4datHRD7uCmvo3ttYKEP7gyaNH3d2bLQzZtfyiAQrVEUnDAHla0mDqG1itNlspR1qyTMrfZs14wj0B2cH8gM588OLjUmhLFpO9f7s8wvXsxIRB3Ff3rnQodeS8hSdq7CMWe9XltxoYG5/x7dcuFCx5bNLzPRfU3FiSKmBrpD3kKkpL0UqsUFDYgetSRLjwPDKGXn3gSETMqPD+VU2F6GbGgpOJSDJoQjzoLYlJ1JAh7qOHuihWnNTgdobYtCafAhFC1aewPrMEIg9PHRc1p8JD4GHo/28eFxZudf5wNsArE83GzvFj1wewCZ+t2MY+fLYDCQpAt3hmCxiL6++yOi70owv3PbjJ1fZA5A9/f3j0zB0VI87zjMip9YNo2wGaHmB4WL1DWNPeh+gkPPg9FnN2ZK8SANZphfMlNp3kVl5IYbA5al0QAAAAAAAEzEjSCmeY9OAGaLgIBFbW0dExbz8/Npb++0muXru1ClUlvNur0ooH9FnPs/q9w7OxB1j8IcnHm3F/rcXrrM41Kp+/UWBKaRQJayJbLu2DG5o7F9grnTIO/Csfy6WfG7ymKxyM5l7+Abx36xARz7eYCL2CzkCINxQHvL7faoSAefz7txQzN8Cyxcn51QiFO5BEE88IBQp4PfK588mN+5bSbPrwUOcHM4843GO+uszct1WTiuStP9BIEDqfh7xH4cUcVZsU9sEtXUkFs2U//3/z5WIkns6mD1uXON5u07yLAf/eqJxj/sP6dGtnnG/vzNnwSra7448cd3y9Uu2XzI5YZ33vBgEW4D5rtG4jA03e9mfsnch7OfGWQ8aCMD9/PmkV1dN/H4T/sMQi7kQi7kQi7kjieVSh35JAIAmIFgBTQALsEEfG/f7o+I7F8Wje7SHbzGMVJuXTc9Lpx1nwELse93HIlMSihPt0DEa5ib93xL9GrADRGe8/Gf/bqxm8q6i7kDql7mx08O281rAHXdGpk7ZkNS+wvxnMrF1eLKrRbz8GB+CZ3NZplMrt7Lmy0KD+Yraxt1EybORDC/NsyaGbRvJs+vLQThgYOnTFjVzY3FIkymwegzplSjNcvCEar5mxpJVv/o5z+O/dfvys4hctmP/muLVEeK2KZNWW/LSESV/eGXH5PPvP6rJ0VIeeKXPz1ecyfWTDHUfQ8+kfnzR5DuX5//8d3SWRSJNkeQ3YefD9xGHoRbPz3g7oHwgLm7D+Dnllw3G8vGXTeDkAu5kAu5kAu5AIA5AALQALgKDvtC5HfO0iry/lfhRHlDS9GhQwgMGSA83DjM79/g6JXXmghThxZ5uBFCL93ZK2442LF4qSAG3fq40X3VEqS4gUwdt5opNI8c6KHc6Du/U9/fP+Dmmj1ecbX9/QPW0pH5V9TdRzfLXv2r3B9LlI1V5469W1DjdGCRLXnspd/8/DHq89de/UOp8k7EiuTzRXyyEX+VNKLwuEQy6LGf/OzH4Zd/+dyhmhkT7YL5HcFz9a+yRxxudVrNZuRUWjXD59cWHPJmdjh2Y9bw4v/wy/7+fg8PD5ylVutE332M+te7asqoO/fusXAJjkbjd5vIn/ribx/zv7/pwQgJOaDW4SRPPt9ffezVP5HffUzEx0da6u6p+dsbr1Lk6p9856FzeI4lfDF5j755niTLWjPLjOBINEGg2wM4ZO92mwnZ36ZN/cPf2AwXAwAAAAAAwHEQgAYAAHDXsT0sfxKe8+nuW4amdjLQB7E8WA8uoNXG+TLCeA3NX8I3ipcsSNHcPPjVnaPofnQv4JgLQXjgR4oysVgeNE2PisJQusYvzn1W89WCZw6/7a/Wkcq//e7PjcFP/Pu3l4k8lI2esasfJHXqyzhopX7sv37yiGUd5fDaSaPy3ImP1vCpY2VKSrj6V7/+LoljWtUnS7w3PRf7r99dvqwmw5/BRyGdrrrg/PxNaZZEJIo1148u//Gdd8teCEYzCszvL0esjR08vEapY0tWP/MTZnXtdf6Pf2Ge6Mt/fPVj9bIZPJVWzbb5HWKJrroRBLP82bzgffBEKLWSCg6mPlLqkGf4E8//+7djRdLNNb/7SN3K/+6WZxDfUFqplMoodVVNY49O1Mr/+U9eQurPf3fn2wi2JPZH5qmv+NDrIUqH+JJgEVmsnFV7cZjXhjNP+vHojMy43T+6DESfAQAAAACA06Y3AM0VSwRIr1JpXXtncwAAAHPGQJ+RfEhs/PoGsdCLWVFpommT34JVyPBZ823VV7o2khXIRZd7xx/oxtwm6zZyAfPmAGMTzRFJy68EWvJGLaEdXO1I6ao++tMJNYl0pEgkIkm+RCrtalJexsFI/OIBIX+5hETmdZT4AKvBKRzj+uxj9OTq2//807Gzg8swJVLqsz+8doLZkdazL8CciIbqDw6XeJ5DMxjM753DmS8bhlbXDk20CBedJVNp1QycXzvMN9YbMLfuNiqQqqv9ZfJTlqc1H+9/7uP9g+l/3vXcUJG/DD1R/3nXD/88pmJjzbvpz707+KLgL2g2Mr8v3O3El/G7o7//NgSgAQAAAADAJEwqAC1Y/GhcbFSomN3V9kXpR+evDn2uEC9JTF2/UPnRW8cVvfYrWLI8lK2srFZBoBoAAO5HxsEldXTPLa5PsKmzm/OQ2H0AmdpvuCE3w8cff23JVlwatWus0dXbLtvj7u6Go1fz5pH9zO/uj/oldArp/nX53LnLiNlFFunUjT2I9Fu2PFbC11EjN1ow6RqrlNQj5nWUd6KTbMnqzU/GxlK62Mt/qBlOXPTY83FDyzCVrfyf//zNb+vKPywXbrAkqs7yLfXjenrUrfznf/Ir9H9/eLdMbUQzAczviOjz0OE96M7q2o5Cvfvgj0BsvmQmT6VVs3B+wYTMW9MM7lIyJsrM7Ao9MHbbbgAAAAAAABznRhBs545giR9N+2GUUVFapWQHxsaFGk/nHK1SDWZyxWJWr0prP/yMuEuefHYD73z28SotAuCeCQhY5MgtdP38fNrbO61m+fouVKnUCIA5RywW2bnsHXzjTFBsARcNbSPL3MRsYKC/p89e+T5qzE3McKxQp+um6emPahEEwed79fXdCSKat2hwp2kcnRmM0SBgH8zv3DaD59eCJEkOZ77RCEsdXAvPY1fXTbhbFAAAgLtDKpUiAMDs5PwKaLbYn2tSlZ2vqu5FdapeVaCRWaPDEi+PjfDmspGxU1leNbwmWhC4/JHloWIu6mqurqqqVvZyxcuXR/j5S1gstiwuUdxr7FJWV121rITm+i2Piw0Vs1GXsrKsDCeyxIsjgnhccaC3svoqd0mEd1vZmSplLxPnjoiIWRLEQ11Xy0rNKQAAAGaVAe0tJCLcPNzdBlC/7tYEhW/fRtpbY5bemX+b3lXGVG65bZ35Pl0IopOOgPmd22b4/AIAAABgrnJkKQwAYAZyPgDdq2rqYsXFxi/Xn69uVlWXqe5ksVniJbJAbnP11WZzRFkcu2FTHLu5WqlicZckpi7h5rxTbbNewfINT68TtFVWNXGXPLphs+DD3I+V3hFxcd5NlZ0L1yXyqquRJH5thDK3DMVu/iGutq5Tz5PEp6aK/3a8qBli0AAAMKu44fBTZ/cAm0AsDzd327uO4mKmfjf45f3ZBuZ3boP5BQAAAAAAADhuEntAq8pOfMTd/GRiakQiMjaXvvfh+bZeZFJVnT+Dg8jiJbHDBVksb2Y1c9XpQiYe/dFgKr0eRHUAABAASURBVC53dQk3SMJTlBaO2IJDEBQqMdV9+NGZq72ozsTbHrNEzFUiZOzqrK6+ioJ4qkpFr3dELBcX7aorPNrUq1LhoLNY9Vza8lBvVnMv/IolAADMPkxkym5wCjYcndVgfue2GT6/Hh7u3t5eCLjSrVu3EAAAAAAAABOZ1E0Ie6+dyX29lOsXujYx8ZHE2ObcM0pr8V9T2xdlig2PbtqzB6mUV+uqy6uqVXZWKrMQN3Tt0wvj8FOuN4tVZ3NvahPiSqLi1kq8uYglELNMnSwEAADgPmfeP2HAFblgJoD5ndtcMb8sFtvX1wcBV2pp+cryxHXvUMiFXMiFXMiFXADAHOB8ABrHfBeye5Wq3t626jOlgZInF4q5SGn9boLa6qLc6iIWVxy0HMeqn/Y2vvPRVTsh6K66wtyPmu/EsrlLrJUSx2zYENFVeOLtq1r8fGvacgQAAGDm8fTkIVei6VHffdr/OdXZXHd3N1f3H9gH8zu3uXR+wd3nuhmEXMiFXMiFXMgFAMwBzgegvZckpj5qOn30b1UqtliykGfqYra/4IolYi7XW8JGPJ44KBD19qqUveJHN8R6150prFI1XVX2PiJARksVRiN+JvALWtLVhct1qpgKTF1deu5CiZjV3MaWPJoYJ6j+8GOltfZxOJvLZnUhE3Pnw6CghSx2FwIAuBBHKPEh9MoOreUXrQmBJFQaIECalroGpZ4ekaJtaahTaqd5r0+C5yMNDRAi/USVE4LQNWskLafPNujv2najuHMSIY9AtF7bodEa6En35E5FGmXHiKPuxUlNn76+PuRKHh4eyGUEAu+8v54YftnXdyv70J8++ugjBO4WmN+5zaXzCwAAAAAAAJhRnA9Aq6oKT4s3rHt2TyJ+0avEr672IsHydanrAwe3wli7ORCZmoveOl59tQmlJT4bwZREXdUflQ7eK9CkLCuvS3w0cXMETq7KfadQaUK9zaVnFBs2bN0TZ26k+oTSxlJpU/P5srqnEzfvDjX1dilVepMRAQBchOBJ1ySvj/ThaMuO5VzooHFAVJactl6oUWqJyNho6YmcghYiNGlLkkSv1KDI2Fhpfk5+gx5NG07Aui2bpQZcuXCiymmDvoMJ3t7FQC0hlK1PjjQ0KGlhgFSoPZ2TV6GhJ9UTQuAjCZVIAqScimPHzJVY3IOTAsMekMj6jLd9BB4d2n6iV/N///d2ZmbAG28ccHODjYvnAphfAAAAAAAAALg7JrEHtElV9fHbVR9zBQKk1Q5GibVVx/dXjS/aW/be/jLrVXyUWzVmoZH2alHu/iKu2M8baZWWzaKvnvzjVebP5revMX8cP1BtLln10Z+qzwi4d5oHALgEIQgIQPL8fJ91q4ZSeDy6ruBYUZ2eI1m/ZZ1EQHRwAoTaC3l5ZUyMOCVZKuQ06A3jq+L4hIb6cAiC1miRkGdoqWvQGHBtEmmoREBrGswvzfVLzOudB5dXEwKJD60oyCtqoYWR62N5HALhxNFlLB0NjY4NECB9x9B2QDyJTCow0Bwhx6Csq7MUw32QSSX4b66OlqGkKaO1DRdOn1YaeNLkLWtChfIyg3RMTwY7wzMYePjElUPruEefhUEpv6CsC1gvXDVy9B05KSujAaaLGwrzI9zd3ej+21/3sb8or0r49uNXr14rKipCsxJb6MfXtWnga9tBM3F+YY4AAAAAAAAAc5A7mqxe14R/e1VtStXEFZt6IfoMwHTD8ebIVauiA3gEwQuIlPlwaI3i9GlFx4h4skFZlo+jz/gZR8BDevOuEwRNGxCHxyOQgaZtfKlFcHwiowOQQRi9KgAh6Zo1Uh6zujklKVJAG3iy5LRkmYBZ77w+JUnG0es5sqSU9QEc5jhE65lGaI28oECuoa2UQcxCYY2yrkUvZDpt7gEOy8auWRUpQLRAlrwlCbeGONJ1yeukHE2HQShbFRvAm3gsZAECR7+jIzhCHmHAHR3XE0tnotesiRQiAyc0KcXSGXzu6y1nsT5l3eBZjOHQSTlQD5iUgYEBg/H2lw23yq71Nqsok9s8vt83FwZFDQzcxrmekWkHDr2S4MdGMxfbL25HelIQe8TrnXt2PTb1PuOKtr2y/8Cf9qeGsW20NfNNdX7Zfgk7X7Z2xlMaCqfnyGY3AAAAAAAAAGAGmcQKaADA3MQLXbcuVFtHr0uRtCgFUl5Fg6LDRlFCIFu3SqAsatAihAPHiOOzKiUaldXZrd+g12o0Wj3SaJBBShCkUOpDK4rOVnTQ8oYGIaFHhI9UiFPK5B2ogyddLxUS4zeCJ4Rjy7QocXwax2pb9ITMEDCiOW1LWUWFEnUIJGtwdLhBi+PDBkJr0HdU5Ms1BvtrhZkTTFqDTh/KKdPYLcnxid78bCjC4feOihN1TNnxPUHMQmlzZ2gl7jMOa7cgqYTQyDV6PWrREJFDZzF2wCY8qRbCkXrAJN2+PdBPDwygAUO/bp6Hlwmhks9OfvbZ5zjsFxwbIxHx48L5xW2aMUd5hn3niXAS8Ul1WUFxbQ/bL+axZWyKlJCNpZ/L24yIHRSX9Fg4v/EcztUwEcQY/JLUUZTy84LL5LLRhT3DEpJWB1OXPy8ub6L84pJWS/hIp0Z8hFN04SNfflKrGVkYhSXt2JaaEEtGiiLlxcePnKNintkWRyrljbrhxbVMT1YHo5pzuHyP/aHwDFv3GL/248u68MfiyMvFpUeyGpP27ZWQJEJMJ8e2ZecsetCMMbn5HZoyvl9kcNs5hEZNKDVmKIqb0MjpHn0xqEWjJvSTRvLRkXN050LCxzLjZvXKGe7GuE7GJS3TFRfIKXxUuLq4oJYaefiYCa3hJ4xpa+RlWQ4LsgEAAAAAAABTM/kV0ACAOYbW1FWUlZXlnzitRHTd2bN1NrZbxsHZpM3R+tN5p1uG1kYblKffyTmtNCAnEOa10+ZwKa3vYG5xODLFvJaasH+UrTLDJ2QpZTkK9/FsXlGLQLZm87Mv70wOtb8CmtZceCcz850Jos9MrTju/M7/vvG7372ec7rF3ubXlooG+0zg/zjCAKlUGiA0NMid2TV71ElNoR4woYH+26hNX3ukPvX/Gr77buNzx/78+9d+vjMwMBCxJeFBuoKTjfzIYM9xh/GDE7alxvmRQamZ+zYFsUnJo6nbUiP5fnF79u2O8RTGpWfujEHILzUzA+d6xqRn7Y4hybBNqZuWSdCYwuywhE1xfLUubGdmRpKfpyQmIcZPGJcUw8fFlz04+qVwdOEBdWO5vFGDH0vxn2pk1LXVlDfxl+GY6uBqWUtPcNPbzP20OxRsfFIJy0QkEgXjsCb+cxRqTFt2z2LmrNWd5PzicTNPWVCwhI8D8IMTSvlt2osndOywj84dczE8MGYGx8zR0IUUlpq1D4/bmKrGdGMcI4VwpQlBwvBNqXF8ihp94fHGTOiYtsZclgAAAAAAAAAwRbACGgAwyNChkJuftFScbrFViIk+p6wiLuSdbrBsOEwbtIjZfwJpEU/IobUGR1fg0rSe5ggFBNIgn+j1kYYLp+sMesNgikDIMZhXKWtpQsLj4NIB67es0RccK7NSxjEET8jT150+IT8rWbdlfYCQU6d3KmA+JQRHwGP+usV9pjU4Ck1r9FpUcbqohRZIIyX04FmYw8rO/K1MG6zWA6bBwABS9dV/2PbT2+Z5KX2n7PrfCw+dPPXXt95sM86LFKEmkuIH4whluXzsol6qseyDQ39WrvbLCGNitT26xoLj7xajxqRwHZsfzteVvvfun9XKIJzryZdYXup0YekkhRA5sjBC6lp5U1AMroUvkojYahzqbWpCfL6yje/HBB1HvxxV2E0jLy+TJ8WJ5J8Xy83rV5vKy/jLNoUNdZLNF5mbPiQ/dAhNjVFTO6otT2TnLEikC0/duytBhHQ1x/cfON12jxbXTnZ+h8ZtcMrwSxwARkFhJD67IJHbyfKRQ8EOGpU75mJAY2ewZ8wcWS4k9WNB6RJ8qYyqyvOyaPSVM47m8uma1KdXrw4K1pWeVCL+spEXHjnu9hyj25JMUDkAAAAAAAAAOAUC0AAAm5hoc/IqiUAg8kYpz0obLuQXa0JjZTiQu2bLzjU0rVUUnbjA3D4vOenZ/yAQra07nd/haAy0X9Mg18jWP/sfOOZqqCs6ocdhWcWFlmScsp6pqugsjtQSDQpN5Pq0/8Dl6Y6yfI2VMkw/faKTk6J9eEIRz5C2M7qjIv9Ui5WTka5PWSU04LA3x1CXr3FJ9Hl8T06UdVhaj968c52AhzouVDBnUYcHbT0zaPi8LpywBP4NGnkdnbx5ZzRtwAd+rAx4YqKTojXW6gHTYWBg4FzZkQeMgfh5Qe6ZvuaBH/zmiWtfn+m/TfPDY4L5fIRDgSJJuIQtrx0bQyVH/WFhbCv9oA1HJMNHJVI6iozxE4k8cXRSQ44tHLlzVxLKydiveyJrF4nsY4dvtl7YvEuGneOEkcwmDAXlzFYZQZHhpPJy7bgdF8yvPZlacZiUooZCkuOWB49uy8ZZ9MiP7/nRcXSPTWV+72DOR6csfi/jkHyoEHs4x5wyKtczxpJpGRnPmCTkjJFVsYMkY7oxTk9NsZy/NzWm8ch7SiMavY7ZxoQO5dq4LAEAAAAAAABgkiAADQCwCUeY83MUo9PK3skcu3iu4fSxhtNogprkeceYJy35zOOxFnOqPP+d0SFTfcvpY4dOjz5uwjJM7LXixDsVo1vsOJYz+OR0jrllpLyQ8/oFNJ1wTHyoFTs9Yf6epfUtZ/NG7lFi5SyYNehleYfujK7GgZOyWs99ys3NDUcVpyu3u7v74O53Rqb85Zcfm//0jEl/uvFIZkaBbln6/k3BohO1Y1bxkvxlT+/J5Afzyw/U9KDREWdlWXHj7rS9mYjUFR+q6dFQOScj0zMP8hGiiqmxkUR1o5q/M21PkE4kIsvRBMYVNqobm/g73/ggofxQ+r6y4N1ZexLCJSIqOCjuyH+lH6/FPVFn7soKQ3x+zaEy5gz8Vu/I3FSbvqN2/LbH6ppyXeqOrCzEJ8sPKJnCukY5lfraewVUzZGfZZxsGtHW3s/R5M/Cjpkxv3hUa1FqemaQki/Bp4MntBQP48FIkk9ePpR+sFQzctj3fjw69zKyg+2X8MrIOXpDNzJ3bEOXR3XDqp6ac6VUUmTpZbVx3IWnFo2e0OBRR2rOjb4s74rpnV9w97luBiEXciEXciEXcu9PHN/Q5SHz2uvVHAHdXNtx9357FwDXcCMIuHk6uE8FBCxqa+uYsJifn097e6fVLF/fhSqVGgFgF3NHw1ii4rRcM3t2yBCLRXYuewffOJ2drn13eHh46PW6wS3BpxVBEDwev7+/HznPL+n/7Q37ID2r3LHb7bH9ImPCJZK4TTHyfXtONt3Du715xmUcSKrNzLinnRhpZs7vLCJMeC0rrjR932nnbyJ4Ny5L182vBUmSAsECieRBBFyppeWrmzdvQJgAAADA3SGVSh35JDIn8ELi/i0O/3xPAAAQAElEQVQI0b5REbxrf33nkxYIQIPZDlZAAwCAazFblRQhcJ/QNRYX65SOLhtl8yXhcXFBmvL9mZ/f48AvVXMyq7FxpkSfwZSx+ZT85PFyzSRmdAZdlgAAAAAAzuMI/H2FHIKm9dp29dBdioYSDXpNe7v5fkaEwNdfwLPchIc2dLUrmW0aLcUQre/qGDzUajFC4O+PazPXTNNdapzI8fUXWorhhtWtHUwbHKG/L6ePOYQj8BUSXUoNzbNSjKlPEr44UEBoW2tqm7U4SV9fWqj2lXjXf9Harh3+xn6wGNI2X6tt1dL2Tn/CUxjPRjFzo/48Wn2tpgGncAQSXxFnKJhIG9QdrVoDIsafFz55IVKPbcuhUwBzEQSgAZi8/v5+d3e327dh4Q+YU/BVPecXh7pOT+3pk7UOlzZqyo//eiobU0wfo6bW8X6Dmc/YVPpBE5qUGXRZAgAAAAA4jeP7aEraMkKrpXkCb9RRlHO0tNXAJD63jFDjRJG34Ure26dq5kVsSnvMW6/GIWCTSXvlw7/eKdalRzxvor00J6e43dtqsUc2p32Lo8WRVyax/rMPzqglD699LNxf5Il61K21RScKa7U0x//RLduW95w7/M45YuWmJzmfZX9orRgShG56/plvcvr60Lx5a+tP/Ol4lQYnhiWlfS8c1f7lzeO1evOJCSJSnv9euLnY+rVX8v70tytaG6fvwCmMP5AQWSvGu9O3b68ozXnn74bFcd9+WOgtMp+CWqv+8qO8LzsQb9x50QFrUx6n8/94sn5EW46dApiTIAANwOSZTDRBEEajCQEwhxAEC1/bCAAAAAAAAABmIVrf8NmR41f0goe3bF+53OfL1hYmscucaJB859nUh8MF15pxseYzR45eGr1VIlPsT8evEBFbnkt42P/8h3rrxUz6Fpw4In5a9+E7ymvf356EPn37/Tr9cG19fZ6BYaLy+sGXWivFOKKwRaj+xB+OVhkCvr15Bc+TQBqaIwoQ0e1fI+FiX06tOYbLEUl9UX3eH45eQcvSnv+3EBHnitb6zhwOnoK1cRtbjCMKeRA15//h6JcG4dLlgQQHtX95/NCXvLBN5lM4OXSm48+LZ6V+x08BzD0QgAZg8kwmk4cHfhNBABrMKQThga9tBAAAAAAAAACzF8Hz5hGoa3Qax5s3DxkM5jtREDzfIGmIN00btO2to/eKMPT10MhzHoH01ouxCJ5/kLSvZ9ROGuPReqUaBS71bbUbfSOYQDWuwdDy2bEWS4ooyJ9or65Ey8KDhES9kh4qZl4pxBSeOJw30SlY68jYYnSXsgtFPPztR7rO/OPKpS/QVDl5CmAOgekGYPJMJpokWQiAucXNzc1ohI1fp44t9OPr2jQzbyjvWsdm7AiAyYEJBQAAAMDsQHiHpezZl4KfdVX95ZyS2dt5KBGnma5fyrmmRZ44GC0KX/3YIpruU1/+5ISm1UZc1noxT9+Vm7euZKprLXjzzzYXF5t6rrUSS8P9nbs/O7PHNKerprkZhcSE+woI5RRvaD/pM6W11fn5wqS1j2z7z39T//Pjv5y8rIHflQWTAgFoACaPoigudx6bzYJdOMCcwWazCYLQ6fQIWLD9En70NPn5wYKxd2Nj+8VtS+UXHyiwfps2nL1zT5x8f2aBWhT3TFpSpASVH8w4Xmt0siG237q9WemxIqSrycnIeK+2Z8xRwsjNu3YnoJMZmQVt5gPZQZt2P0WdPGijXyM61jbFQKLDI9B2X0cshTE7dkpK95+sdcUoTGPlE1YFEwoAAACA2YLuab34Scm1HoO6XTm8xwPdVXvi2Jf+KU96fvlFK/644znBxhTD8TLrxbrqT7x9tGriLYxpdU2t4TsRonnIiRg0zzfI19tf9NRmJPBGhgd5/9BMaq/kCU5hfF+tFKO1tcXHaouZ/ay3/NvqkPqTtfBREUwGBKABmJKbN7U+PmK1WoMAmBO8vPgdHSoEGGy/mKTHwvl+kcFt55iXQXHMy8ZzBcW1VFjSjm2pCbFkpChSXnz8SHETGZaQtDqYuvx5cXlTD9vv0We2xZFKeaPOiIxtpUeyGpP27ZWQJEKDQeI7VWnGNTSqD8GPJYmKX/rOu7rHMvdtWlacWarBMefHYj0vf34ehwGFsZuS+LU1VByfj1CbueYndiSgggyb0ecRHUPm+PVjSQmRwrbyTz4uxsHtkR3T+cUlrZbwkU6N+Ojy55/UauyNwDlq2WPL2BQpIRtLP5e3oTENmWteHYxqzjHjg+49dmTCSqpRE7zMs+ayMVikPFeultg7d8+R8+sZ9p0nwknEJ9W48ESnQ4qCgmPQM/xI5WDhUbOP537kuI2btjHtrnuMX/vxZV34Y3Hk5eLyNuOdystwbWMLXEajJoW02+1x/fS0eUmbL1m73QYAAAAAuKdofev1hvpxQVu6T/llpT5txbd8a4rb7R1PcESBvhy6uWfqy31pWt18zfDot0W2A9AGbR8RKPLm1HtGpKU9oj6R/RmS+tLNlz4pbUKBq78TMbhXskHfR/jjYs1I5E0YmifYPHl6TkGwNPX5b6PPjvz1Sp/eQCNiir8B7twpgDnFHQEApubGjZt8vicCYPbDVzK+nhEwE8alZ+2OIcmgYAkfR47xy8ydMYjy27Q3Y1PQgLqxXN6owY+l+E81YoclbIrjq3VhOzMzkvzYRl1bTXkTf1lcOJ9tteYRVbHHNDQOSQqFfJLPH8okRWExceHB5po1pYcz/ywf/gaMHZSwe1sYKUrYue1RPystozEd8wxP273Jr0ne5pfw1GpzT5iOIb/UTNwxT0lMQoyfMC4phh+2KXWZ0P4IkJJHU7elRvL94vbs2x3jOaYhy7EkGbYNh9GD2GgGEMUkrF62LmlTQuyydXES0v65j5lffnDCttQ4PzIsNWtfkt+Ep0NKgsOEQ4XHzP6YcRtz5Oh2ebjdhGUiEomC45KYP82Vi4KD8MWTygzs2AJjKp+o26P6af+Stt9tAAAAAICZyqC+8o92z2WrFwsQsylHYNJ//uo3v9n3m9/s+X4Ix1KC2anjl7/6r+e/RV/5/KJ5rwqrxcYghI/sfPVnP/imt/c3n/nlq9tXCEcs96Q1165oEMtmMUP7P85cQauff+W1FxM51/5+rpkWLfYl1NXlNQ31NZevqAnfxUw5Q/sXZ2qYYv/1/KOopqS83fZOzpM6BavFtE1fXuny2fCfv3rtP58QXf/7mRq946fPIryjtr1iru2/nn3YuVMAcw+sgAZgqkwmWq+/JRQ+oNPpYC8OMEuxWCyBwEujuUnTs3VPLzc3t4GBgWnM5Yv4utL33v2zTheWTlJsvgiHh1FQGEnyRUEit5Pl5WXypDiR/PNiuREHCtW18qagmDARzpXgAGBbU3kZf9mmMGutjanK8/KohsYUNjZ+nFO+d9fBHL9gfnlGDRNq7ql9b+8eq+fBDl6dJLp8eN8RXdLebak18qzycYtze0Z1jNI16fhPJ8RRpSdzPm9CkmWWnqiVQRlhIrYSUeqmJvy9hLKN70d68vn2RsAT9egaC46/W4wak8J1YxpiDw7mIfmhQ2hypnt+jeo2lBBE6pTILwz3zcAR2Tl3Eo2e38uIaiz74NCf1Y8FpZun2/4K4JGFPUfPPg4ijx63Mca2a6VyZdkH7/5ZqfTD3SbLxuaOrlxkv9ujc5X2L2m73XbetL9/wV3muhmEXMiFXMiFXMh1lqH54z9k2Um8nPNby09V5//3l+fHF8v65cejktqtFWstHNMErfni0K/G3qPPUH/qD/XmZ1/++VdfWtKsFGN2ufjkeF5PwlLUcOnLai2NtJ/88beDeZov39n/5XCxD7P3fYjsc/AUxqOtFtM3fPLO/3wyLrX25P/UjjzWyunXHfvt3nFtOHQKYE6CADQA08BkMnV2qhcsEHh4MO+p/n4aR6Xh8zCY4fDPdoSZmxvCj7N95w3777ip5DKYxaY6ZfF7GYfkQ0E79nCOEbHDN+9KQjkZ+3VPZO0ibVVyZ53oyKrYQZIxDY1i1JQfSt+rztwXV3743ASb/ZDmSGlto1InV6I4PhPctH+AsemD3ZsKhJEJO3dn/IjK+Nx+aXsjcKfKttIP2mxVwOz4EUdeLih3fs+GaZ9ftZISxZCl5VQkflTqkMhOBQ7Mr2dQZDipvFzrwB36Rg2jZ4wl0eq4jWnXfIQn0z6eaIoa/LKCHPqjZ3wBclTlfsHIYY5d0van2xmuff8C13PdDEIu5EIu5EIu5N4XCM48hLyXfiukub69FdYFgzkIAtAATKC/v9/d3f327dsTlrx5U8tmsDgcjqcny8PDAwEwg+Fr28SgjUZTT0+vI4fg9wI+Ct0f1I21KDU9M0jJl5DlyKgsK1Vn7joYSfLJy4fSD5ZqjOrGJv7ONz5IwAHifWWNav7OtD1BOpEIF2b7JbyStSchXCKigoPijvxX+vFaXaOcSn3tvQKq5sjPXhtd1eVRDVnhtzotCZ3c9/Hgvs7ChP/3Qabk0NPbjjcZhXGvHMQNBeOGjgTt3/OnsnJy7xvvbUIkVb7/wPiFqbhj6SM79trlyP/KTCKVOj6pPqLuUaqLG3en7c1EpK74UI2eHzfyWPsjsPdzuw29cq4YH5sVhvj8mkNlM2LHYJ1aR4r4TBg6iVLr9MoyO+eOL4aR82uF3+odmZtq03fUTnRDgLHDeNlu6THtqmvKdak7srIQnyw/oLQMI8lf9vSeTH64pPFAY49aPbpAOJo0td1L+rVGNCvgT7CWVVTw6KJHBAAAAIBpQeu/bv5H/pcdGsNs/YVUAOxzI4gZsRUjAHdfQMCitraOCYs98IDg1q0+ioJ7LAGASJI9b948/F3LhCX9/Hw6O524z/Mk4O949HqdK/YMIQiCx+PfP6H2mWlWza9nXMaBpNrMjJNN8E+Fg1w3vxYkSQoEC/z8fBFwpa++un7z5o37dKkaAACAu04qlTryER4AMAPBCmgAJmA00jhaAQFoAJA5cmcywUbnAIxB1ZzMamyE6DMAAAAAAAAAWDH5APT8+fPXr//2kiWL8fO6uqtFRZ/19fWtWbP6ypXqmzdvIgDmChxuY7PhFwUAYLi7uw/vPAsAGGLU1NYiMPNYVubaupfR/ZPu6hYBAAAAAACwz8PdfZLb1P7+96/Hx/+bp6enSCRasWLFN7/5zc8///y5555NS9va3t5+/XormiSWIDA8PEji6+sr5Pf33uh1bq0dV7wkSOyh0/ZOvGGv8x0TP/SQmG3o7TVNqXKWOHbLS1tXsJW1zVoHT24Sh4CJCQRePT36CYvRdD+Px719+zb8Pj64z5EkmyRJB3eL5vN5vb23kCvhaLjRSDmyP/skamazSYiz3Fswv3Ob6+bXgiAIDmeepycPAVfq7tb19fUhAAAA4K5YsGCBIx/hAQAz0CRXQAcFBeL/jh17Ny/vffwyJeX7W7Y84+/v/8ore3EA+vnnd164cBFNDksc98J/bw8dWnBq5MiUiQAAEABJREFUVJa+/cZbhdccCnjg+LPkyZdelZX9Kj336nQGalnimOdeTX/cn200IjbqLH37N38obJ50A1xJRFSUoKvwvTPNLjwETKObN7t8fBZ2dqoQAPcxb2/B1193IgAAmCXgawYAAAAAAABmAnc0KUKhCD8WFX1mefnZZ8zd70UiJjE//0MvLy/L1hyTZew8/d/fT3oy6fvPZ37Ytfy5l7Yu56J7iRuxeWscOp/5o01PPfX0i28rI1J/GCdhoUkyNZ9If+qp5/5YNfFdvKZwCJhO+AOsRnNTIPBCANyv8PWvVt9AzmP7rduW/nSkJwL3DlvoJ2RPMhfYMnPGDWYQAAAAAAAAMKNNcgW0Xt+DHyUSP61Wa3mCH3t7mV+F8PFZiB9VKjWaut62shPvlcb+MjRCzKpqNiHukrVPb4gLFHONqqbywuNF1YPxWMGStZs3xwWizrLSqyx0Z2WyrfLMkuaIuPVrY5dIvFFXU9WZwqKyZttrrFnchQu5JmVVncrExIJL38vhLuk1jm+iytyEpXlu4Nqnv4vT2b3KyjMfFpabq2dJ1u5+aUMQF/exV3n6rayPRq2i5gbGxq+LWx7kjTqbyksLz1cpe+0d4tQpgCkzmUx6fa+Pj/jmzS6jETZCAfcRNpu1YIE3jj6bTDRyEo4+783cpDueVdODhHEvZ6ZKdDqKUpceP/SJOnzHzuDS/Sd0q3/0NPn5wYImo2dkWuZOv4J9WcVtRrbw0d1Z6Y9JkLIsZ9/+D3DhzG1hlBof3FZ6/EjxjL3ZG9svYeh00BSw/R790e6kIEpdfvzwydoe5KzR3WD7xe3cEyffn1nQZrRWdmQufrUtlV98YPwJ4Jxn0pIiJaj8YMbx2rlxt7074/y3j9RR33Xq7OyPqiPHT8ul4kRPxszgXJzQ8WAFNAAAAAAAADPBJPeA7unRf/vbj8lksv7+/tDQJSkpKbdv3z569C9PPbXx+ed3trYq8/Pz0eR48JeseyxUd6mwrB0H+VgLlz/++DdvlxX9vcHw0JN7M7cv0VWfOV99O2jl9zY+wqm++M8bJpbkyVd+uz3i1tWzZe2+cd+ODRIarp4p/ucNj0Dr5RET1f32f2b+KEh5vujzsmZ2eNIPvvvNrn9catbZ2IjwNvJ4aEXiyhDU9I9/thuQ6UZzzTUls8k0y9xEhOHq2bM1KChu48aH2ZYu4XTcpf6rZ0urPYKStvwgjiMvxem33Xl8b7axy8ALj/DtulT8D9VwHJMlSfzZr/89RFN2vuwr9tJ1qSn/xq0rrWg32DrEyVMA1ji4B/Sw/v7bPT29Xl58FsuDzWZbbsUDH27BnGTeJJc1bx6HJEkOh6NSaZzdqtW8BzS9ePMLK6/9cd+H9Ti85R2xYbXH3zJePdmx9IXnfGvLUMLmxU3F5dSy1CS+vEiu8QhPfvaJCMn8r/7+96Zb3iuffcb7Lzt2HNNI4wI6KpS+SU/wC37xam5RaWVTV/9wJ0fuIYvfknb641SuZY9g1oMPJ64OeihiZTjZ1dLR04/YQXEbvp8Y492rbNLc8gz7zubVERGxkT66r5q6zKHbmA2b14aHRUf0VzCnM7Iwzhtd1RijasavvWOf3SYq+sWreXLN+MCgZ1jCps2PLfa4qWzrGp87phv9OMb6zLZ4UZe89KJCYxwq8FhkcPhifnuj2nvFiFzPsKQXdm5LWhsdvngxjv1XN3XNv9OWRvOVvLyGWPmYqLakouMuxCtdPb/4b+8749x5Y9zZjZyU+ZEJK7wRPzY+hKZ8oxcjFYpMGTGq1i+GoUFuuzVmwkfOUYk6PGm1t/JaB/4pYsPK+cp2UcLoqkZON/KL2/DEypiIh/wiohfT7fX4Yhk/v7ie5PgwUme5PDxtzmB/z+hTxgHpDSN7ck3j2kl23fxaWPaA5nLnW/6xhkcXPep0PZY9oKd9BiEXciEXciEXcseDPaABmL0muQLaYDD8+te/+fnPf/bii/+BmB1yb/7mN781Go0bNyZ/+eU//vKXY2hK2N5LnnjuxzH449DCiEcj9Gcyv2gzsfyi4gK7Tv9m/x8VvQidvmr8fcbyWMnJq02C5XGBvaWvZ75RhdO/ULJ//1IgUwdLbL381V6m/sCFSFl44sMSpQmVlZXkTtCf3qbCk2Vx6d997Whia2XpifeOl15jFjoza5DvNF161fT6K4NdijKn/8qcXlh19SfPLQ8Ss642m7TVRbnVOG69KWj5+jFt6Kvfy/xF21Vm1TMqU6KDe5YEebOqtLYOcfYUwLS5caOLwyFZLGL+/Pn40cNjkrfxBGAmw18umkw0/ludokwU5fwK3EGkyI/UlatHxbHYpEiIKCXORKQkcvVjujA+2UTidEl4kK7gpDoyMtizWEMpm6jwbXt+dPL4xweL24zCYFw4ZnUCSenaLl+utRoZs/9t0CRyScmjqduCLxc0ivbsCzuw+wi5K3Mnv7RYt2lvBj9jT1lwwrZU9HmxLiErhtyFX6Zn4dxSKljC15BIGJc+svDnolFVZZWPGtLBwqW61MwMfvq+xscyM7fFBZNxH8S2ndu/O7NUM2r8cEAxjl9bK9yZGSNK3ztm0SuuamQ3MKOuraa8KXJbXDi/oLbH6BmTnrWbKbBpU3BpTUF548hcSt1YLm9cFkyWl5bXNqrHt4XuoemeX3bkzv8ZPc66kdmjJ2W/LiYhmK+O3MTnIyoMvXeuZtSo8kdfDOckowd51ASOmSMjhcI2paIaZdOm1Li2/QX88FFVfc4fOQX71TEJMaiRjAuSqyWp6vK9xZox8zvc7W2ZcZKMPR+Tjs/g2J6gu2va37/DLDFuS7T0vn3u0ppdPYOQC7mQC7mQC7kAgDlgkgForKam9oc/TBuTmJq6BU0H9kLJEiTx9l/Irsv9xa9OMkFjLteby/YOWr/1x48yJXgSbyYFF+Uu5KLeLr3lI7ipa2hvDLaN8ozepvNlqnXP/fa3EV9cVaqaFGVl5u0ubDOpzu/fWf23qEcTExPjfvJ63LrcX2WevIpGNW3s6uxFMZYueY/skrJk/69K0ARMWmUzO+LRJ9cGLWSzWOIlXDbbm81GyNZWD06fAphGBgOF/8OzgAAAEyBHPpfEpu3lq3W1Ofs/b0KPjSrHFoVFilATSfGDcQS6XF6bs2tX7ROpaZkHYw7syryM7okeXWPB8XeLUWNSuI7ND5fwSRQURpJ8UZCILENUY9kHh/6sfiwoXSLy5Iv4utL33v2zTheWTlJsvmhU4dFVjWmFPXSsWhmUESYynjz0fFrja1mRn+waE6i2UNfKm4JiwkS4ZgmueVQAmj26G5aTaCov4y/bFDZYQDK6wKhco6a2vEyeFCeSf14sZ9bxjm2LQnOHUT52nEfuojxmUqjiNpQQROqUyC8Mp+uMPZoR44aNvhgk42bBSs2DuZrLp2tSn169OihYV3pSaUThI6sikXLkFLDViFI3NSE+X9nG9yPNb64x82up/JD80CHza6ETMzi2J7Mch8Nxd3fHcdLhtbr383PX1Yy/iWez2RQ1l/5yAAAAMAdxOCSbzSII/M8WC9aQATAJ/f39RqOJpmn8aA6IOW0yAej58+evX//tJUsW8/n84USdTldXd7Wo6LO+vr41a1ZfuVJ98+ZNNEnGztI/vfzGVcnWX/923RIxF10dH+jTK0sLyyod/4A0unxv9dFf7FLErX00NuLRdRs2p7V+9IuX36m2H040aZvLPv5j2ce5S37421ef3BBxZn/1uCJo0gSxP/7NS1G91dVNXY6d02ROAQAA7ipK3aYj+Xw2sixZppRl7+0bCqoKKfxafu5zNT8hDofh+OExwfjfFByxFUnCJTwlf3UsVX7ywF4dfz/OuMwcXH6u+PykF2NPgbGt9IM2xA4K1ymL38s4JLf8Je2XZPsIJjA4qrBnzMiqpoIdvnlXEsrJ2K97ImsXab+slWwjpaPIGD+RyBOHxTWkvUONttqa2/eTtH52RrWSEsWQpeVUJH5U6uxW4eggM5jvJmqK5fy9qTGNR97DP6SIRmU7M92jjhNGPhZHXv6cesKBGRx+Obon5qygyHBSaeN3DmYs/NnyoYce6u29hWOjvb298+bNs0Si0X28DtoVNZt/UQb/5Ou+cOFCmu5vb/8aFqwBAACYgfA/XgsWeBlwwIwy9PQY8Zem+J8wBABwEv7mhiTxFzls/MP2Aw8Ibt7UOvuj32QC0L/73W+DggK7urqUSuVwYnh4+MqVK1etWvXTn76ckLDuhRd+fODAwQsXLqLJ6206U1Sd+Ox34xaXnbhmMjL/U1V/9HbutVFxXhZORyw2GlwtzGYNptsqP1y7sqowt6qQ2cj5id/+9sm1S96rrrIRvuXKtr60iV144O0q5iaGvZ1Xlb1rud5slnF00yw2c6dAk6Vp/GpoAbNg8dp1S7pKi6pUNgPULEnshkdYVW/9en8Z0wR3ybMREcvRhAPk+CkAAMA9YGwsK0U7E2LLjpROcKM2z+BIUeORzIwC3bL0/ZuCvT5rJOP27E/QUXyy/FCNBi0jJU/s+2A1hXRNx/ftOSK/+4Foo7KsVJ2562AkyScvH0o/2Dg6V91Yi1LTM4OUfAlZPq7w5QlqLm7cnbY3E5G64kM1E5yaulHN35m2J0gnEuGGxlY1uhvIfKu79Kw9CeESERUcFHfkv9JP5JyMTM88iL8/poqpcbnHa9WNTfydb3yQUH4ofV/Z2LaMukY5lfraewVUzZGfZZycsfeCnJxRZ/fa6EnRBetIEZ8JQydRah3yS3hl5Li9MToirTk3cpDHtjJujnpqzpVSSZGll9Xjx9PudKPx8/vKuWJ84WWFIT6/5lCZUTnRDI55OaYnfqt3ZG6qTd9Rq0Gzia+v7/BNU/l8Hv4RmcVi3efroF1RM0UZb9y4OTzOAoEAfzRAAAAAwEzCZrMeeMC7vb3dcscCAMCk4W9ubpnh5/PmzcM/cms0XeblCI5yIwg2cgYOPR88eODYsXfz8t4fk5WS8v0tW555/vkXWltbt21LW7du7TPP/AA5i+X35G+zNihf38VsoCxY/lJWRsTV/T99vUzLXf7jrIyozuNvvVNY3Ru0IX3Pht6cn2adUXFj9xzYE9F0/A/vlHZJ4tKeTY3o/fAX6blX2TbKm5jlxviQwLLMX/wJh5TFsc+/+tKSsl+9knu111aXEjOynhNX5bz9XpmSG7Fha9pa9oe/+OWJZnMTj3R++NbRQqV37Nbn04JGdPWRrg9x00puVOqPt0Yo3/rpb86rWOIlSyRcNnth/NbnIlTH3/mwqdfUpaxrVpkEj77y5u6Fpb/5LxzkZolj09JfSuSe+UX621eNNg4xRjl1CsCagIBFbW0dCADgAn5+Pp2daiZAFrdtzyZ0PONw+XQHjfF3sHq9jqZpNN1wxIrH48/RxRFsv8iYcIkkblOMfN+emRxDns3z69wgCxNey4orTd93+p4vNB7dE8+4jANJtZku+qZh2uc3NMlIKKkAABAASURBVDTsgQeEODba3Nyk1eqGWxGJFnA4HASmFY5E9/UZcKDf8hKPM483r6MDfqYCAADgWlKp1PGP8PhHPi6XA/88AeAiOAat19+iaUc/VTm9AlooZH49tLCwaHxWUdFnOAAtFotxAPqDD05t2vTUN74R/q9/1aDJ01Z/WNQUt2lDXGDlR81VuVlve6c/99qf0nCO/uqH+w+Yo8nayr+9V7nkx2mvRaUhY1NldZfR23xsr43ylmo/anp162vHEs0v9XUfvo4DuzZ7YWo7/YfXxT95fvtrf9pururTt7I+bMZVmQabyDjwXZzeWZnzxjvmFczmpnlD6UZl6Vu5ZSqEuIEbXvrNBv/BWv3T0qPwH025L/70ZLO2LDcn5tUX/vtYol5v7G2uau4ymvertn2Ic6cAAAD3hrGt9PDuUgRmCjZfEh4XF6Qp35/5+RxbwTxzODfIbD4lP3m8fAZsczGmJ1TNyazGxllwlQgEgjVr1l67VvfVVy03b94UiYQE4WH5UXjePGYn6DFbQ1jW8I6vZ66mu6JmnIIHeeQ4O7X+BQAAAHA1/E8V/hK6qakJAQBco729PSgoqL1d5WB5p1dAr1y58he/+FlS0pNWcwsKPvrtb//fxYsXxzyfRiyuWOKNVErV6GgrVxwYuBCpmNXEDpWfZNMLvY2dSq2jP2LjTonNTTt4AEsgkXD1yjYt/Ax/V8AKaABcZ2gFtAvBCui5DeZ3bpuu+fX1fVAmiygtPUdRBksKh8Px8fEx7wHNIkm2Zf8NBKZbv5lef8sSif7666/hPQUAAMDVHF8B/cADghs3bsDOGwC41Lx58xYseODmTa0jhZ1eAd3Y2FhQ8Imt3E8++bS+vn7882lk6lU1W4kl41SFyonyk2xa6VRVuOlmZ8qbtMpmh6YNAAAAAOA+5++/CP9XXPzZyESDwaBUKgUCAY474zD3gBmamqmHsOfeDfosw8tiefSYIQAAAGDG4HDIvj4DRJ8BcDX8LqMoA37HGQzUhIWdDkB3dHQcOnTYVu6f/nTI6nMAAAAAAACmi5eXV3j4Nz77rHB8Fk3TOCTq5kZwOAPTEvmdOQFoyw0A0ZRNVz0UZdTr9QgAAACYSVgsltFoQAAA1+vv72ex2C4JQAMA8Nc7bOaXegn8fw8PDwTAnIP/FTExaKPR5Mi/JTOB/f1Pp5ILZgKY37ltEjO4atXqc+dK7B87c+Z9GnsyjbFsNH1c9w6FXMiFXMiFXMh1Fv6ortfDzU4AuBsoipo/n+tISQhAA+AE/G/hggUCHJbD/yLeutVnMvXcvn0bATDnuLu745/bMPxdC5c7/+bNrkn8EBiWtCM1LlIiQepGpbzg3ZrwZ5bVHD5SrgtK2rWJeu9Acdv0/lRo/+fUqeROCtsvblsqv/hAweA93Nh+39mzjTy+/wPn7+k2tqq7e/hMcVfnF4/ZM2lJkRJUfjDjeC0eN8+YtN3B5fvNz11oXLvWStiezYkPn7mcncFvfCOivv6qZe2t7WMHpuut7YK/IuYa171DIRdyIRdyIRdynYU/wuCgGAIAuB5+r+F3nCMlPdzdYf0muE8JBF49PU783ih+U4nFD3R39xgMBhyD7u/vn/o/jQDMTPjatiyCNhpNt2/3i0RCijI69XULn89ruVx6sYaMje05/t9/KG7S9qLwbT+UNF7jf39beOXJovqeqd6uCkfJjUbKFV8C4ZrZbHJggBeWsGnzY4s9birbuoyILYxM/N4PvrcugOxqadIYx7xE7KC4Dd9PjPHuVTZpPMKSXti5LWltdPjixRKkrG7q6veQrPz+E/yKgkoNPu+xx442KpcKHl2Vcn504uqghyJWhuPcjp75YeueCKYa1SgiMeGh3q/aejxwN5Ljw0iduc/Ic3xP0Czh4vn1/Oa6Nd6IHxsfQlO+0YuRsg0tHp5ujeYreXkNsfIxUW1JRQceR374U99ffL34kk6SsGkl+dU1Hd/ODLL9YkbOUf+oa+MWsnPldHaOaddz1Pze5K/eOW427RyOA9IbVnsrr3UgXGblfOU1zQwKSk9lflks1sqVj164UGqnDP7+jCQ5BDG4B/QUoSkbmKPwvxGwwyYAAIC7ZsGCBY58hPfy4t+4cQMBAFwP/0AoFAodeWO6IwCAA3D0mcfjdnaqcUgOAXA/wfGFzk6VpyfXwS82bempKSigEnbv3iYp/6CsbRaszmTj8HMcX60L25mZkeTH9gxP273Jr0ne5pfw1OqgsS+FcemZO2MQ5bdpb8amoAF1Y7m8UYMfS/GfaqY2o7L85PFytfm8xxw7pt3RuWOrIiWPpm5LjeT7xe3ZtzvmAX5wQsIyEYlEwXFJ+E9LN0gybFvmvk1MzdT4ngALUUzC6mXrkjYlxC5bFychx0y31UP4kZvw1KjVPfZncPQceY6+NmxcOcgvNTNj09iq2KPnF42fzTGVjz7cSKGwTakJQcLwTalx/Dm0Digi4ptXrsgdKTkwTW5P2cAchQAAAAAAAHAAbMEBwMTc3NweeMAbR58RAPcrrbbbx0f89dedaNKMbedO1mzbKzmyv6YHzQbqWnlTUEyYiOSLJCKS0jXp+E8nxFGlJ3M+bzKioJEvkWSZhE+ioDASFw4SuZ0sLy+TJ8WJ5J8Xywdj7T21xcWDFY+tarTRuXojGlWVJ+rRNRYcf7cYNSaF63AYdeShbL6Iryt9791D8kNDtwHW1I7rCWAY1W0oIYjUKZFfGB40nXH0dKO2MeFaUrR6R2Ys2Xhgd7kGD7S9GUSj5ojNDx95bZCUesyVY56yP6uVQRm4cdRkJ0xsHDebeMZHVT7mcM3l0zWpT69eHRSsKz2pnCPzT5Kkj49PVVWFI4WnawX9zLkJIQAAAACmD+kftVImJkekUCrFxcrW2fK1PSmWRUX5e5mfU62VFxWqsT/BSpP37k3hl2Rl5FbqEAD3FASgAZjYggWCrq5uBMD97ebNLvxNzI0bXWiyKGVTo7JHqZsdgbDwzbuSUE7Gft0TWbvwj6XGpg92byoQRibs3J3xI2rPIfnIlxmfI52y+L2MQ8NB3sG1qMyB42oeV1WP3VzKWlXGttIP2hDyC8YxaeaHZpJEd7a6YwsjH4sjLxeUj1hpbrUn9zO1khLFkKXlVCR+VBrGTPcgz+FnlLrsyKGmTdtigoWlGo3dGRximSN2UPiYa2PMlWPNYLuWBfPj5nfUbFq78Ia73VNTLOfvTY1pPPLeXIk/o5CQJV999ZWDhacr7AvhYwAAAGAOIv0T9+b+eiVnRJLh4iuJ389W2IlAk9KUrNcTG/a/ePDSvQ7pkuIVu7Lf3rjQ/KL70+f+bWt+65gSXrKo+JXi7lxOLnKotzPo7MCcAwFoACbA4ZDmnXAhdAPud0ajic024XeEwXBf3NND3ajm70zbE6QTichyZjfepzMzk0iljk+qj6ip0S97lOpSdeaug5Ekn7x8KP1gqcaobmzi73zjg4TyQ+l7T45eJDumqjHtjssdVdWYeKW6plyXuiMrC/HJ8gNKvVJXjLuRFYb4/JpDZZZG7fXkfqZT60gRnwlDJ1FqnXHMdONx0zXKqdTX3iugao787A38EzhlrPk4pzxr17aYxkO6BDszOJpRWTbq2rgs2jT6yilu3J22NxORuuJD5t8NGNnua5dHzi8zd2Nmc0zl+MIbeXjGyaaac6VUUmTpZfWcmfjFi5d8/PGHDhaeFSugWSyW47t74Xqm3plprAcAAACY5bqvn3oxcXu+yvEjvMQhMhnywmHrex2ipVrzt8vyt+Oo8db389OtldBVZib6ZyInzJyzA3OOG0GwEQD3pYCARW1tHRMW4/N5+HNab+8tBMB9j8udj2MWOt3Edxjw8/Nx9a41Hh4eer2Opmk03QiC4PH4/f2z5n59cxLM77QQJryWFVeavu/0TLoBIWNy8+vv/5BYLK6s/MeEJUmS5PMFHh5udjowE66B+fPnf+Mb37h8+TK+LNlstr+//40bNzo6Jv7hxGpV+KwNBkNfXx+fz8cn2NPTM+l3EK4hICDgX//6l/1RMpnomzdvwApxAAAAd4dUKnXkIzz+JNLQ0DBhMRy43f5+/g5VhpUANClekZK+Y6NMTFIqRUnuwcMlrRR/RUZ25uOLcIh2kZehs74VR2gNqpLM7RklKqvlLRXJtr6ZufJ6XgUn/nGZuFtx6vDBvEsqymb6mKY/zT2YO1gVKY5KTEnZGC/zMrTWl5zKzStU6IbOgwlAd2ckjlgBzdSftUPGbM9hqM9Lf/HgyC04SGl8SlpKYpRUjFSKi3m52YWVKtLu2dlqGsxe4eHh+EdH/FPomPRly5bhnydra2uRwxx8Y8JNCAGYAItFuCICAsBshN8L+B2BAACzA5tPyU8eL59p0edJwz/dKpXXHS9v5+553t7e3/rWt3DQduCe6u3tvXr1amRkJAv/3UoQNTU1QqFw4cKFA86TSCQPPvggh8PBzz09PUNCQvDjwBRYqrIPAQAAAHMQP2pH9tHMRPH1i6cuXveKT8/N3buCj5BOoai8WKGo70aGVkXFRayyQqEy2CzPIPkhsqiNabse51//tOK6ODnzaPZWGWk73VJVvNf1wlOF9WT83uzcdHNVOKCcnZuZ7FX/aV6JSpz466O5uD1759DdWlF58WJFvUEcIpOKR24zgqt6PXvvCqTIO3gwT+H1+Ju52Sm4aZtn53TTYFZgs9kJCQkxMTEjE/FLnIizkAtAHAGACZh/N3Z23DINAFczmXAAmoUAALODsan0gyY0R8yfz+XxPDs7Hb8Vqr0dOHDw1MvL65FHHvnqq68aGxvv1TfNIpEoMDAQh3rDwsL+8Y9/+Pn5/fOf/8Q/+n/99dfISTiWrdVqdTpmRdL160yY3mg0TnoTElwV7onje4MAAAAAsxNnUWJm4aU9luXKBtXFrBczClWLVibKugtf3LqrUIVQ/iUqPzv+cRn/0qX8zPR8MmpXyEpxfW5meuHQsmlSZqP80DLh6yX7X0zPb6VQfiUqfHNjfEiu4rr19OtkYrKs+9T27btKcFV5FVT+0ccflx28dInqrty/PaWh0nyfwcJ6XFwW5c8vVNlaiUy1lmRnlOB4doZs5cbRWaQ4xB/V5x7MylXglvNzh7bosHF2iHSyaTA7yOVykiRXr16Nn5eXM3sQ4h9B8ctz587hHwKRC0AAGoAJeHh4TNcmklYQPAGP1msNU/rgS3AEPEKv1cM6bTBlHKGPwKDpsHUx4fcCfkegGcnNzc3Ocryp5IKZAOZ3bnNkBh96KKCxsd6pY/v7+93d3fFfXOMf8SH4ER+7aNGiBx544NKlS5YUq+UHzDsmT+XRVs34Kz2BQIDL4A8Ay5cvr6urIwjC8lOHnf5YfcSR9JEpzc3Njh87/lEikchksrNnzxoMBjslHZkFyIVcyIVcyIXcacyddgZVQ2VFfbclAt1dqcLPSL6/F6Iquw2WNFVrN06ysy3yROUpqltlaaBbkX82FZMDAAAQAElEQVQ4R4rzbab7e3FIL9nWjKxEynwPQTE5WFVrpYKM37gjU+ZP4hCyzIvkcEg0KTpFYeH1lL15+VElilaV4mJ+YYk5tmwLNX1Ng5nFEne2xKAtT3D02ZLoChCABmAaLFjgjf+hvHnzpjMH8QIf3fhUfIg3C5nUtZ++f+ofHcw/WBxJ4o6tAbW5b3+uJAKffD7V9x+H/++Chif74QvfWzxv8MieqqMHPmgw//PGkTyycdNjYSJcSVft5++f+kJpICQJO7aGNue+/akSBT7+3A/DlMcPn6qfeM9eAAjhso2bQmrf/2Ay24/ec/Z/Tp1KLpgJYH7nNkdmMCgo+Ny5EsePtSRbgrnjHy1H4cfOzk6FQjG80/GE5Sf9aLVmHN69ceMGl8vFAeju7u7FixdXVlbiD94T9mf844IFC3p7e/v6+iwpQqHQ8tLxGkY+KpVKiqJw9+yXdHNztz8LkAu5kAu5kAu505s77boVOfvMq5Dv4CNXYdYlZ5aMb2M4ne8/KrlbUZjberEeB7T9k7Pefz3eUHFJ0do91RvCq0oykhMvpqQkxq9I3pi2Y/eOnO8np5fYug/jtDYNZpqRMWiXRp8RBKABmBY3b3b927+twZ8YS0r+7uAhhE/k43E+6k+z/6+eiPj+0499R1afW6G1tYZZqzj66zrBsqdfeIz+6K33qoeiyYQw8tvxAfqSP+dW02GbfhD/7cj63DLtcBOC0EcieB2lXzRD9Bk4QhAatxxVfajQwlp6AMAM88ADDxiNlF7v3L9ndj7BWoK///rXv1QqJ+57P+1UZvPmzXvkkUfw19gajSY6OhrHoCfx2RtHnHEgG8fTLTch9PPza21tvXVrkrdQxjX4+vri4Lj9mxC6uSEAAABgzsHfweLA6+C+ySTJJ3EKNY3l7VdFqS4dzsi4NHK5NSlLTIvnl2R8f7v5NoP8+KzolStHHmZAztEpCrMzCrOZPad3vf/+1pQocUmh9Z+IyJAJmgazHQ46W37eq6ioQK4EAWgApsff/34Wx6Dj4//NwRg04SniIG1Vc4dWi5qb9XEh3jwCORv4Izy9ebiSeqVWS//j5JEOjuFODSyOz8OPBNINH1R3QDgROIAXEveId1dLe0hkGFFX2wHfWgAAZpCHHgpsaWlBTrITPO3u7j579qyDWz+7TTnOaj+gjAPrZWVlHA4Hx3xx+DgiImISy086Ojq8vb1JksS1eXp66nQ6/MR++NgOHKDH/ek3s1PM3X2GbsoEAAAATJ6u9aKie2virl0Xu/MaxI+nbwzprjxYP7hvBupWdRu8QlbGJ6JuRHXXV1xqsF/e6aZVW5NxVbrsi92yXdkHU7qzkrfmdeu6kZdspcy/sLWVlMYnRolHbIJB6VpVlNfKlK0pVCVulVIpLlZ2+6+IDvEiSf9F+GFRFNPbwc6S/snZhW+GlGz/fnphKxL7S0dsH2Ll7FrtNg3mBleHni0gAA3AtLHEoJ96KvmDD/KRs4ipvhlpbUezpSbm/6Jl39u2zJOnLf0YNt8AjiB8ZHFhAlTbR4giHo+LEOT+5Qv45gIAMGP4+DyoUBSh6ePU0uC78LvAPUMMBsPk7vWqMbM8t9yEcCpwgP7SpUsIAAAAuB+pCjO37/PK3vt20W78qvPigV37Coc26aAaSrLz63N3vHl0B35Vf3jD+oxL9so73/SLTFVH/85U1V2R82JGXgNFoU8PZiVmZx6tSunupgz1OEpNLRpxUEX2wcLozN1vrmVeGSr2Jf6wYuvr76eFDOYv2v0ms2i5+sD65MxKXeulw3mKo7uPVj1tzuyuznn5cKXO9tnZbRoAh0EAGoDp5O7ufvmyHN17fdp2HD4MEwgFPEIJOyqACXFE/pzW4nc/kmuRQs97OkTE+QIWQQMAZgZf3wf1+h6j0YicZLnZoOX5yDsaOfvcch/CqdRjeTlh+d7eXvzcsvPyFPs8/g5Otu7pNJWaJxUqBwAAAGYGqiE7WZptNUtVmb01ynoWs4Vyon+Gg+V1lzJWSJ1IH6wqVyyViVF9fYNuMI6tq8zduuKUf0iIV3e9onXs3RB1itztK3K3j0xKXyFKRzZO4FJmojTTVub4s7PbNACOggA0ANNm7dr4/v7+5uYWNAk2fwvY0eAxIfDx5xhaO8xbQNP65vMff+nD2fHYoxHCuvOwlBVMhNYbaIJjXoiP/6D1erhmAAAzRUBA4FdfNSPnjYy3TuW55Z57yBx7nfTzaeyPs89tpUxXzQAAAACYXpSqoXLcnsyUrlVR2YruhXvYNJgzIAANwPSIjo7C0eezZ885WJ7uURuQNNCf9w8tx9+fhwxdlogfrVfrUaSPr4DQEBJfDt2D44JMSFDoL8HFCIL2D5R2tSuVGoO5ki5cONBf8IUGLXty22Osvx8evgmhidZUf1G74rsPrwj4xwcNzt6UANxvDK3nL2k3PvPCt/BzffPfT7bCJQMAmClEIvEXX1xEznMk5Aoc4QZ3GwQAAAAAAFMAAWgApodT0WeM7pB/Whr41Kb//O9NCPXUf/KuwrJRBq1VlJRGpG7Y9d8bmPQPP6xj9kHgSR9P/d7ieUyBFd//YUTV0QPmmDKtkX9WErjpcaawqav+8/flGnrEu1rfcOlLTUTcI2GClsuwDQewj9ZWf3SkGgEAwMwSGBjU0dGOJsXW6mNnufomhLMIRKIBAADMfPizuYeHx6TvxAsAcJzj7zU3gmAjAO5LAQGL2to6Jizm5+fT3t6JXIUQfusHOx5DJf8H93wDs4Ov70IH3zidnWrkSvifOr1eR9PT/8YhCILH48PPrPcWzO/c5vj8rl2b8M9/yjUa5/4+IUnS05Ov1/dYXsKS5+k1HIbmcnk3b96A4QUAAHB3SKVSRz6JLFgg6Oq66dQNhwEAkzN//nxv7wU3b2onLOmOAAB24SCFu7vr3im0prq4VOMTFy8TwC8kgBkPvxdmbNjO/rq8qeSCmQDmd26zNUeenp4cDufGDc0kjkXmuDNwKUdmAXIhF3IhF3IhdxpzHWEy0Ww2LLUE4G4gSdJkMjlSEiJeAEwAv5dYLIKijMhFDMrzh397HgEwC+D3gtHo0L8ud9+A3SV4U8kFMwHM79xma46CgoIbGuonN7+3bw9uwTH1C2DmbMGB65l6Z6Zez/hjXfcOhVzIhVzIhVzIdRb+CO/h4YEAAK6H32uuDUAHBgbweDw7BfR6fXNzC5o8liBwSRCvV1nXrJpSrIMljn36ubXcsuNHzzT3IgCcZzTSBOHKADQAswd+Lzj4rwsAAEzd4sWhJ0/+FU0KjpFaPsGO+Rw7b948Pz8/p8Kv93kAmqbpr776asyG2tPSDQAAAMAVDAZqwQIB/he/r68PAQBcZv78+SRJ3rzZ7UjhyQSg33rrfx96aNGExVpavvqP/3gRTQ53Seqe3zzu31WauXt/2cQ7idirSRIRFSXoKvz/7N0NQFzVnTf+A9x5IfPiTJxLGGeImeElYSoUSBOibiZbI9EYYp6VdLdSt026dUXdJu3TJl1rotVg3Sbd1eS/rbG6JrqKPm1IHxNiVIx9MtlGiBUo6GAgDFGGTMIdM5OZIcwMF/jfeYHAvMDwMgmQ72e7ONxz7rm/c85Fh98czn3zWDuZDF7K8gcfXW6u2H3oNBLZ1xcu3Ya/3wEISExM9Hg8BAAg/tLTM86ebR+e95wSGo1Gq9USGA+n02m1WgkAAMAMYbPZlUqlyWQiABA33E/ZuXOxPjJt3Anor31Nx2Wff/CDfz5/frSt32+66abf/W6vTpdtNDaT8eOlLNSKL5g6+JoctajGPomMb2/7gS33HSBTgC/TLtTwRQSuN9zHpyLRHC4H7fViETRc1wQCPkVRly45CQBA/Gk06bW1J8lUa29v5/6DjgW8sWNZ9uLFiwQAAGDmGBggVquNy45ZLBYCAHHA/XwxzFex1x93Alomk3NfR88+c86dO8d9lcvnkongzVt0yzzXp3+oU39r4cIU3qftgT/45qXk6O9euWyhWk5sprpjR9+tCeyqEfk4T71y84/WaUU80ttt/uA3uw61D/3ZeMqyRx5e2f3hMdstK29VE9OJA384dtoeKBVplt1xp75AKycXTLWGoyfqzN2ihSVbH12ZIpKlicXaR3ct5JKQvRdqXvr1q5+Llj/48K3m157zN81T3/HogwWnX9p91EzUKx95cLH5gybRrcsWirpPG96uPBZcNx2hfQLT3sWLttTUeRcudBGA65hcLov9400AgMnQaLRO5yWnc1KfeEXcguPy5cutra0EAAAAZrXe3t7Ll4lWq+Vy0NiLA2AKzZkzJ5B97u1lYz9r3AlopTKV+1pVdSj2yuMn0uSove3v1n1SsFp/y6J5h9rN/gTvnQ8//j15zYFDB8xk4cr1P3r6lpce++UxLtsb+Xivq+vTpqZukVyrX6ZRi/ncv3+CzfN4KdqcW9XzxDU1H31ivnX1D57NSXnssddOd/PUq3/6dKn4k7ePfeDV3LnukaeXaZ74yQtN3eamproU+UL5PI3NfLrpgre3t8tk4/LQMrl2oYaIgk2L1NqF2m7fd16RWpOjL0wRnThWU5eiv/vRpxbyf/oLX2I6Uvt1k9piBK4G/8enF2WyG+z2mLa2AZh9uPt/XB9vAgBMRm5u3nvvHSWTE9iqGF/j95UAAABMY15vr8XSNXfujR6Pu6+vz+PHvSAAME5JSUkCP/8L4QSWpo07Af3VV74/wXvssZ+PWfPZZ38ZqDxuIu1iDd98oP2CiZi9PyjQiI6auRwtX66ZR8xHD7z9IZeOrqn58NXB2lGOE3vTu682EZ6mRFtwd9g1vLamA889/2EXIcdM/D1bc3JSeKfbiavpzfLHOk/7VyXXmMmerQu1cl5de+2Bl2p56rXaApn57Zd/Wze4Zpk3ai8u1L363Au+/asN7fxf/1RfkPKBuSty+3Y80WsG4D4+dbm6U1NTLl60cf8ZIwDXDT6fN3eufLwfbwIATJhOd8uZMy1u9xQsVhq+CBpfp+rr8LEFAACY5i5etAuFAh6PP2eOiPvVhkufEQAYJ+6TGy+XC+tlvV62u3siC2nHnYAObIPb1PRp7JXHS6Qu0Iq7DCZbbzevrot/b45WdIJL+nabTtR03fngs8/mfHTa3GX6tKYmsH1FtONjxdYd3Fra223rJgvlvqfMddvN7fyc5feu1M7j83gpC7l/OfmPTyTb6PXabYHzuk3HDlWqzd29pHcK24erj/tZ4z7kufFGuUDQy/3O1evDTvnDkQCmg8TERB6P4vF4CQkJFEVh5w0AuGpkMtn8+fPfffcdMmnDV+lOt7XDWAENAABw1bjdHu5/BACunXEnoOOPJ1+4UC3XrNu6eyUh/HnyeaJb1KK601wGuum1xzZ9ql+5fFnO8jvXrd/Qceixn77cFP34+MmWPfLLHy3ubmryb7AxZexNRyub4tg+XFVffWXzf3xKzZkzh/uKj09hVuI+3vR/tun1Exlx5QAAEABJREFUeHo9Hjx1EACuniVLCg2G42SKTJ9Vw7P1KwAAAADAmKZhAlq+cHFKd9Oh3/3hUy6HzNfe/eD6nIVy3ulu3zLhbnPd0VfrjnJZas3aZ5+9d+XCN5v8G2JEOz4uPPWydbfy6n7zzE7fxhlEtPAHOTkFo57hWwHL9y1h9uFe8Ei3Lfqi7/G3D9PU4MeneIAkwLWRmJgokYi4FLnLdeVgYEVetFPGWyoQ8CmKcrm68VcOVx/md3YbZX65r8XF93744QeXL4/4L+xkZj/2OhCLaKuep/YnFKUoRSlKUYpSAgCzSyIZJ7vdRnxPF1SOXk2lUnFfbbbx7wEt0yxWE5Ph3Zo6nxrDCVNvCpeB9i0f3vrqwRceLpD5asnnqUXEt3dG9OO8lIW3FBQULF6kEfH58xZyLwtyNCmj7Nvc6+p2Ebk6Ryvzn52jXyjnDyv1bakhUucU+BvKShFxh7pNn9vki0vWL9OkaApWr18+z2YydfVOrH0AAIjR3Lmyy5fd3d0j9ocd/X3qeEu5xnt63NyFCFx1mN/ZLdr8Lly46Fvfuv+dd6q6u0M/35387A8M7heBXSMmZmj0oq2AntqfUJSiFKUoRSlKAWCWGfcK6M8+M37xxZcvvfTimDXb288ajc1knERpORqR7djnwf2Tic3UZOaty9HIjtU2vX3I9NT3nn59tb/A9fnbv37b5PsVJfJxUda6H/1yXVqw2bQNWxZz/zC9+sOfVLZHu7a95tX9hU89+ovXV7tc3u72unabV3SltKvu0Aedj39ry9Pf4r4xv/2TLS+d7j5dsWsn/wcPbt39LT6xNR19budroy28Hr19AACIgUAg8Hq9XPZwaAMclUrNCbzu7WV5PN9/2vr6+pOSEv1Henm8Kx8+Dn07rELwFI7ZbO7sNAdec5cQCn3P+fV4sGHc1YP5nd0izu8tt+QIBMkdHWd///sKMqUGrvs9muP9lQAAAAAAxCCBoiayClejWSAWi0ep4HK5uAQ0mYl4MrVa5DJ32mN/NCBPliLq7bLHtiHDBNqH+FiwYH5n53kCAHGgUqVeuMCQOPClDAW8ixcvcQkst7ubZVmZTM4JlPb39ycmJg5/MZSIHKzQl5iYFLEm8f3hjs1ut1EUJRSK+vr65PIbvN5eJCivJszv7BZxfrk05qVLl6Z2OxTuMmKx9Kuv4vJvIRhy442Kixe/wlI1AAC4OjIyMvArPMAMNcE9oGdqcjkWvXZzu328p3TFfsYE2gcAgEFculAiESUnC7nUYeAIl1IMbA81tbhLCAR8p9NF4CrC/M5uEeeXxAf3GcONN9IE4qmvjyUAAAAAAGOZhg8hBAAAGM3Fi3axWMTjUW53vJ4FKhIlUxTFXYjAVYf5nd2uwvwGDAwMXL7cQyCekpMFBAAAAABgLEhAAwDADNPf3+9wOIf2kI0Hj8eL1NW1gvmd3a7C/AIAAAAAwLSSSAAAAAAAAAAAAAAA4gAJaAAAAACY5SixQpOmEA47IlSoNZpU2dBfAwplSoWYooRiYZQ/EPQVjee4r0nuEmpZlNLxVhsb10muC74WFWlcZ6mJtZyQlJQQpSQxMYEAAAAAAIwXtuAAAAAAgFlORospIa1LcxnZBTolsRjNwvlyliG6TPepZjtLhGkFS2jmi/mLl+TQF+uO/amxR6GhBX39CUmJrK3jrEu8QDNfKbE11dlkGpryeCnRHGLvOGsTqgPHT7WHP9BSKNcqKUury00oLhFMU1w7VjcZs1pH61k3mQBKlpapS+tpPHk2WcOl2iU6Za+FDrYcuJAyO1uZzHa7vAKh51zLWZd8kX8oPrf4KnDZZdLfT5J4SaSf8JL6evsGuKNJPCqhv7+/r38gieJTA6yXAAAAAACMFxLQAAAwGyQkJAwMDMSjFKYDzO/sdlXml3W73BLqBiXNYxiiVIqc9KIC2mz8xM36St1M+/k0zQ0XWxvqTJ2NFlacSUto5fy5F//6mUer7GHkErfNLSFJYpo7TmfdcLnl48+J8Abl/MDxQUJ1bhZpaTT7U75sD+Ok03KWChtb5Dk6+nyd5Wws1TrazxKWjB9r72hn6FSuL5bW85kFEluHu4cEWq4/yeXHKaFYIhRSSanK3sbjn7mJWKkMDIXY0u5K5PEEFGG93j4uB52UQPqGhpQbXN+aaF9EAyTaQMdvBlGKUpSiFKUoHU6lSiUAMAMhAQ0AALPB6BmoyZTCdID5nd2mfH4H/EYcosSaNJmrtcVNcnN1hGk8xzKfn2xssgRTvUK5UkZJxCkuMytOoy1fCmkFLRGSPtaH4v6nztVRbMs5efC4g3VZLW5hmjZwvDV4Fbe5sXH4RZPFQuJ2s26b2SKUKeXCjsBq5FGriSnKzU4kAy2kU+craVbcIdEV5ZKmk8NaHj42vUSakZvdaWx0kVT/UPiC7+/t9fT5VkBzLxMTSV/fUPXgl4F+rnCgf+Sg9vcHxzl+P6EoRSlKUYpSlA7X2XmeAMAMlEBRfAJwXVqwYD7+6wUQJypV6oULDImnpKQkl8vBTihNMzqKosRiad+VBAxcA5jf2S1+8xvAzbJEInW7sWFEHCUkJAiFvIsXLxIAAICrIiMjA7/CA8xQWAENAAAAALNK/FLbMIRLQPf29hIAAAAAgLEkEgAAAACA2cXt7uHzeQTiRiDgX758mQAAAAAAjAUJaIDxoMRKzYJMjVopEw4/KssuKrkrQxzHvyigZMrU2NrnQlygyczQaFInHU+0pq5Cf+MkrpFPReOBGyxzQdrIO+xahgQAMDP19PT09/chBx0nyclCl8uBrWwAAAAAIBZISwCMA0XnrFmf7zYxQm2m/MujL1XW231/48u6Xec7LK44/r2vMLVwzR3OIxUnLWNeg5Ir03RpaZos4al9r52yTiamaE3Fv7/xEtfIp6Dx4A3W0tEjUc4XW6peP9zqIpMQFpI4o+SBpe1vVdTZCQDArOd0OsRiMZeDHhjwbcqRkJBAYBIGBgaSkhI5/i28nV4vttgGAAAAgJggAQ0wPqyt9fiR6g5qUcmG23SyppN2cfbSW7Vy4rTYhupQYnWmLk3OMi3GM1b/4+6FigxdllLo7mgxng0c8ROmFSzRkPZTdWZ3lMtRMrUuK03odgu5X6S578Xq3CzK1HjWRcSaXA3b0tRBuCPinh4JLeFab+6wuzvqTnQYF6yh9aFN+aLS0IRpN57pcEXOko6MPFJTlCxif3U6LkjGSSW7uJBckeJ0xRCAOKQvbISho2SZuRqKJXIxYVqaWwdHM8oIk9Ei911O3sMKae40Y3MgJKFyUW5mmpzYLe3NRv+h0LAjBhDeeJQ4x+S7wd6r7nDLcv+htEArbm10RRy38HssPM6QkMSaJbcXZM+nFfKVa5Uua0vtx612NnzcwkcAAGDmcrlcPB++P22KBPSkDAwkDAz0c3lnt9vNJaMJAAAAAEBssAUHwIS47YybSJJ9a0yZjmaTk16cqxQGPtARLrjrgXsXy1m3OGf9D/4uV+Zbdrrm2/foJG5WvGT9hrWZ4sFGKLGyYPmKAmXUHRLEGeseuDdbyBJZRprcV4mSaAoKMiX+sqyCfI2EoiRpS1feUUATt3DRugeGNR5CuGDNA/fmCl0uYc66B1ZrhJHrhEYeLkJ/M9Zs4FrmgsxfuXJJmiRynP7G7wkEsOaBoogBROhL+NAJFbkrilZkCt1s6u3fLr1NSQUGKvIIjxo5d7nbVi4vkBFWnjPYeMZdJauykq0WN3eVWzViEiHsiAFEGJZI1WInlnE5YJeTjTxu4TMVXi0sJLeto6XV4nS5uMxyS0sH42YjDW/YCAAAzHC9vb2XL3e7XM5LMDkOxyWn09nT04PsMwAAAACMC1ZAA0yS29px1kXl9GiD31N0ppJtOnLsYwtb39KqoFxcKvBM5X/+TqZMpWWUjcqmJVRrYF0paz318i9PRW+akmvk7qYjJz+2UBY6645o1Vhb+8lTH3ewHeKse7TywcZDmqIzaS6qk/UWYuGqZdFUeweVdtvau3K5xDZra3z/7ZNmNjzyWPorV9Lu1vdOftwxapBcAGkUU8c4neQsQ+X7A2DH7ktH2NA5Cdtzvu74x3VWiqG4TCuXanURV5QRHjVy36HA5YhFnnaH7yyb2826KVuP0/LxgTorl6Gl0sLCtkUKIFLjkaqNTZimf/gJPSE9pncr3mp3Rwiggw2/xyhleLXQkFj7+XZWbLuNtpjOtAa34Agbt7ARAAAAAAAAAACYDCSgASauJ9JB7oeKYtle30vWZTnvO6LIL1m/JJmxMKxQnkxZSKyGNUVGzQQGClmWpfwnsaM2NVTN3XHq8FuNvn8JsG6Xm0t9hkUeW5TcecFEJTtaXygqmdZkcXlw4m6tb3GSWPpCKXIiDR1XylVjO04e7gg0PtERDl7Ov0eybyDc5mOvv5N7+60rV2Smsc1vvfTH9shhhwYQrfHYqo3g7jC8cKBZs/4+pd3u8k1KhADC7zFhrMM7QoRxCxuB5kltQn1VJSQkjLIobzKlMB1gfme3+M0vSlGKUpSiFKUonU2lADBDYQsOgIkQ0hqthHVFSvOxrIsVKnwbZlCpS9etzpVR4psy5IzhQOXhI8fqLc7hSVpKpsnP1ciifRDE9rjcwabEMv82CtwR1veai0AmpnrsPf7Mqe+1rzFayDrZK6lgihexKa6a29kTSLy6XX5uNnLkEZsK1WNnKYVYeCXIiHGyPVaXrePUe0ePvPdRi83NRllbG9KX6EM3QozVxkaJaYnL+N4fXn7utZNOWssFEVvYsV9g9BkPcp9vrLPetDRbSZGIAYTPVKxxstz/UZzAdxHGLWwEyMwx+vvUyZTCdID5nd3iN78oRSlKUYpSlKJ0NpUCwAyFFdAA4yNULvn2D/OFQrb92O+NXOpVuaRk3ZKbJApa7H7wh0sstQffOtVax+QUP7yJS/T1GN95y8W6zp2x6fXr/yGHJCcLk8mwh/fJcu9au5JUn3v5I2ukhCFrb65jvrv+h5ucNjvLI75VtPbmP7fnr394092E2GoPttgJSSaEJy/89iN3y8XEcuIU42/Iba0zsiXffqSw133u1MHKU1bW2nS8/b41D28qJqzN+M6xSNdjmdDIw5t6u0OzLqS/J5trmVu5kK4EGSlOljQf7/AFwKWye8+deKsuyviO7IurN8rQjRR1hIcJn6kD7eGVZJlrSlfQbi6/K+xpPsC4WVdY2FRMjb/VGDGIMWZ8EGs3nmxZes9STdPbrRHGLXymWDa0WoSQTp5n3edbGNn6BzctZdoNBw4bw8ctbAQIAAAAAAAAAMAkJFAUnwBclxYsmN/ZGfNGE9MVpbz1gTXiY69Xd1zzVKFQfdcDdziPVJy0THCZ8DTqC0yaSpV64QJD4ikpKcnlcrDs1O9UTVGUWCzt6+sjcO1gfme3+M0vAAAAzFYZGRmz4Fd4gOsTVkADzHA9Lsbi7pkOv8Kzbt9mwj1k4qZPXwAAAAAAAPSpL5UAABAASURBVAAAYCogAQ0ws7H2piNHyLTAWuuOHCWTMI36AgAAAAAAAAAAU2FqEtByuZz7arPZCAAAAAAAAAAAwDUhlKUpFUKKZV12C2MPPqB98KDbZbVY/M87omTKNJk48IR21m2zmK1uIlSoaWLtsPo2hQy+tlPKNEWgGtci03Hed3LouedZuYLYrG6hQk7sjFtIywljsbPRYiOsy3Z+KDR/LGpdlkZG7O0tzR12NtZ+hXcqUmuUODWNJr7IiZjrC2HMvrphrQllaiUtHMwSsm7mfIcdm2PClJmCBPSjjz6yevXd3IsjR9554YW9BAAAAAAAAAAA4KoTKpd/e0M+ZbezYpmcnH93/2uGDrfv4IP5FMMdpOXuxrde+qMxOadkwyq5i+GSsb299sa3f2/oYOW6ex7QNe9/+YSFKArWl+YaX9vfKFu6cpUujZYQJ9PR/O6Bo81cSpceeW7VMfbOkrRTv2/M/Pu7qT+91ZxRsvT8W/sjPHk+GIaNSwXLKYth/37/A5BkOd9++O91wp4eknz3ysa3XvhDoz2mfp2iQjvVyCWvQ1v74zmuU3fJjG+98h755gPfzra997v9J61UaGtvtCr1dy1VyGl/Txk7c+rQW6fOY4NMmCqTTUDPmzePyz4//XR5YmLitm0/f+ut/zNF66B5MrV6nojYzOau7l4yOTyRSqudJ+J5u82nT3cNtcZLWXb/gytFNRWvHWvvJtccL2X5oz//58W9H/3ut8fEd+tdlftPdE225wAAAAAAAAAA1xPWdea9fRWNLtnSB/759oLUUx1nfQdt/oNu9ZoflC7VyVrauWrtx/a9dnJYntjW0eG+XaMUf2QhSq3E1dFhd9vPv/2yueUf/rmYvPPS//ncdeUSw88V5zrZZLFYQrl7eWKxMJk4Xe4ouVtfGC9UNFI5DzxYtDTtREerW0hnKEnrW8+91kjyNzz8zUxa2Bhl6XFIv/7aGNopI5dZDm1NcI4Qt91NZ2myCN0zrOWRrdGn3q7Ye0qcXeLvaeWVngJMiQkmoO+77+++9jXdF198qdEs+PLLL0+dOsUdNJvN//Ivj3AHFyy4+a9/bXz77UNkQnjq5T9+aot+HnF5iZjvatr/y/IDn040QywreOQX2+7R8v3fdLz9000vtQxldUXqnMWLZbajbx5rJ9eeSK0lx3Y+YV/+6C+eEp1+6Rkbss8AAAAAAAAAABNBieViioxcJEkJ5eJk4naz/l04xEptRqacZd12i3/fDTfTfo7NzlQKW9gMmmU+YdyjND7sXJfTRYS+3WltTK9YTgtZl3OMtcPuHq6GJDmQlKMI29PrO6Gnh40hTxfWr+GdoiK1xjoZt3LJUq5/TqFkrNYA4mEiCeg77vjm97+/0WA4kZ29qLu7+xe/eDpwnHvxgx98nztos9kffPAHly5d+n//7zgZN9ni0u8WdB994vsv13XxF977022l31v5yc8PtU8oHyvT6henXHjnF4+9VGcPbaC3/cCW+w6Q6cJe9+rzddw/m3564rcEpitpZn9B1oCAJDi+TKhrSvAEjgoG7n2qt+Bj3rOVg0fGJBgoWN5PC4inK7Hu4wTHsOPjbmoyKFn2N1fOb3/v2BnXdP/TGkqmVLDM+cnFOUP6SykK7lpC1f3plGXw7Q4llNGpciH3fsE8uLXXDJq7qyQhIWFgYCAepTAdYH5nt/jNL0pRilKUohSlKJ1NpTGi5Nnf3rrj29wrW91/Hzdzv1YJBw9yx3q/PLm/xU4k3K9ZtG7Fqvks28PUHzlg9e2G4T7fypDbtKk0S1O2jy2j5J9HnPux2+amtKniHrudiGmx0N0Rl9/SQvrlkeeEdioa9rzRkqyjWu30rZIorWG/Z4iriSSgv/a1r/31r3/duXNX4Ntly5Zt2PA97sWxYx+Wl/8ycJD74Een000kAc2Tq1NEts9P+PfK6D197M39/IXdwfXPooUr71+n16SIvF2muqMV7zb5ksopyx55eGX3h8dst6y8VU1MJw784djpK8lmHp/0drWbR27jwVOv3PyjdVoRj/R2mz/4za5h2e3gJXgX6gx13ltXaz966bcnLsiXP/jwrebXnvPX46nvePTBgtMv7T5qJuqVjzy42PxBk+jWZQtF3acNb1ceOx2IVaRZdsed+gKtnFww1RqOnqgzDx5fef+3uC7wu82fHHv7aO2wzT8i9i7keK3/eKATKTn6u1cuW6jmPmIz1R07+m7NdNhIZLYbyCju/bf1CR81EvXyvowvef90P1V3yVfAtCR+dmEcDQluGPjanVwuu+9WIfX9v6OMw5LN420qduKMkgeWtr9VUXflv0qs23W+g8toTv8MpjC1cM0dziMVJy2TiTWe/Y0wvBMkpBXE9HHdleyzrODb318p7GixnG+vOz+YgJ45c3e1jP4+dTKlMB1gfme3+M0vSlGKUpSiFKUonU2lMWKdHX8+8mGL081YzEN7TrC25gOvn0r79r2SUx91uAiXgA7fgoM7ZGmxJ+dm57Jim3G0LHLIuTKXmyejk2317YTOTSM9ze4xf1GbQD4upF9CeVinol7L3fLea6eIbOmGW9OitAYQVxNJQL/77rvPPfcfS5cuPXXq1O233/7YYz87d+5cUlKSXr/8F794+i9/+cutt96ak3PLSy+9RCaGz2Wevd7A6+6WYwda/K94mnt//tQGdbvh0LGmlGWrv/e4Vv7kk6+d9vJStDm3queJa2o++sR86+ofPJuT8thjr5m1P/j1s/cGf64effmPj/r+ObgFR6+r69Ompm6RXKtfplGLfdcLXEK9+qdPPajlLmHoSrmzdFmO2mbi+Y7LtQs1RBSsJ1JrF2q7fd95RWpNjr4wRXTiWE1div7uR59ayP/pL3yJ6dU/fbpU/Mnbxz7wau5c98jTyzRP/OSFOruvC89uUJu59k0pi9dt+Xf9IS5Uf8o6Su+6A8dTTn9w6Jh53rLVP3h8W0rguPrOhx//nrzmwKEDZrJw5fofPX3LS4/98pgZ+3bEX8cJ6sl/TfTM73vuj+xdOUlnLvX/4z/1q0mCsSVYQf037N03J1y6YSDlUuK7VYltvgz1QPrf9H+zaIC0JP7Jf8TTlfjf/5r47p3kvx650rI0py9aUzdwTR1INHsiNBWJUJGhy1Jyn7q2GM/6n99LxJoltxdkz6cV8pVrlS5rS+3HrS5x9tJbuc9InJbgH9sIlTk6cUdjq53lUp6ZOfNdzY0Wd0hTQuUinTKZoljGRmhJj8l4xhrlP1SUWJ2p09CEaTeeifjf7YhNhZ/lf4BvmtDt5j6ydsbW8rAA0uQs0xIIkpKF9JeI1blZ8h5WSHPdMzYHLzey8YhBxjS8vmcNh/VFrNbpuL4wTirZZWzqYGWZuRqKJXIx97lDc2vwUcsZ3Elcf2VC6+DYchFaa4/80TCUfA/vS3h/Yx4oAAAAAACAWYV1dXx5pjVsbRDbYz71iWvDbUuUxmpLlDNtHR09K5fkEvup98bxS5Tb6SRytbDRZksW0nJiHGMHDkpIa5RCtj1Qze3qodJouZBLXsspd7t7fP0a3in/Iu5IrVGxtgYQJ4lk/Fpbz/z+93946KEHudcFBfkmU/s//3PZP/3Tg1wa+hvfWMwdfPTRh9988y3uOJlCvgW/mm7D7vLnK48eeGHn8+/a1AXL1CJ/mdfWdOC55187dOCF8t+csKXk5KTwuk2Hnn/sF0/86sDnLq/pnefLn/jFE0/8/Pm3g0ud7U3vvvrSCy/9ocbsHX4Jec4ybXfNb3/lv8RzFXU2bwyBXah79bkXDhyt/G35CwabRl+QwqWsXU1vlj/2i+cPvHvsEBfS0QuihVo5j+vCYn8Xnny+8hB3/Mnf1thStL7q0XvnP8X2we6dvz189NDL5c8f6poX6DVfrplHzMcOvP1hTc2Hrz7zyLf/8Slkn68qwbwBmhDmUoLnQkJddaJjPntvbuCD2oGUJX0/+N99X+MSysXeF/6tTy0g9Br2uV/10RcIXdz73FN9dJQ2Izb1qL8pdYn3jb2xNiXOWPPte3QSNytesn7D2kyx75jb1tHSanG6XJb25paWDob7OJZ1Mx3NJie9OFcp9P/XiKVkBStylJRvC4jc2/NlXGY0tClKqCxYqiFueskKLSGZd6zMEkfui3DBmgfuzRW6XMKcdQ+s1gjDa0RqKvwscca6B+7NFrJElpEmp2JrORjAXQ/cu1jOusU563/wd7kyEt5fSpJ228rlBTLCynOCA+U7655A42seKNIIIwUZ4/CGxynMWLOBO8L1JX/lyiVpYopLNueuKFqRKXSzqbd/u/Q2bujDBlx52z8/9fSjK7SZd//wyV/+8okNBTJf7GF9idDfGAcKAAAAAADgeuFmGj+2SPJXZHG/MhFKrin+39zvWTt++cut/5AZ/JXJbWu3sMnJrMVk8+VuKcWtZU/97B+/Lpd//Ts/f+qfb1MEU7kh57Juey9FsS6X20aEQtYWPQHt2/ji508+8fAStvH9P/sSxsRt+eiYkax4+PEnHl5OjB/WWsa7GnlEp8JauxqbewKMaYIPIeQkJSUR/x9HJCZeyWIHXvf39yckJJCpxRfNE5FumyuQE/baLnSTQrkoWOjttncHX9i6yUI5n0+6u043dREZ787ublH7p5/UdcWQnRWJ5Dyv2RZoqtfW3d079klerz34uMBu07FDlWrfbh+9dnM7P2f5vSu18/g8XspCEZ/vC4kvkg/rQq/5w51PfjhG73yn8OXau7/3yHJfgVgtF4n8ve42najpuvPBZ5/N+ei0ucv0aU3N4CYfEF8y8rXveA8XEXo++ey/+O+2EI8n8aMjA9LihK8Nq9V1gvrNbxM9H5OCf+tPEyaS5f3ClqTPvuB+KhK+WdKfcUMSE2nlsqcrQlMdgaYaBwp+PpAiHBDE0JTrTOV//k6mTKVllI3KpiVUq4tl7efbWbHtNtpiGvqE023tOOuicnq0wfNYS2sLe49G+ZGF1WhJ63sWLkkd0lQS4/s81cYwNidhGOLOoijuXyLh/2ml6EyabTpyst5CLOKse7Joqr0jwn+AQ5oShp3VQTRyN3fkYwtlobPuiL1lrpqSq3bsYwtb39KqoFwR+kv87y1Onvq4g1jkaXdwA9VOZaZRTB3DfXh9lqHys+ik2vD+xja8VFpYX1gl7W597+THHYN98Y15z/m64x/XWSmG4vLdQmIJaZy0nvzdk6dS79qwqudIxZUV0GF9Ce8vpYxpoAAAAAAAAGYTd/vh53aNcrB+/7P1/hcn/vPnJyKcz/3G9+z2ysHvWOtHe5/8KKQKawk/98R/Phk48sqOU2SU2Hb9/HDoUdbe/PbvdrxNRhfer0iditTayVd2nQy8sp96+T8C0bGRRonrfHPlfzQTgKk3kQT00qVL//7vv/X00+Xc608+qbv77rtefvl3XD6apumXXvov7uBvf7t327aff/aZsb6+nsRN3Jb78oNbbfAJjzeuE+3W6axAAAAQAElEQVRNRyubfC9kyx755Y8Wdzc1mWJaQx1J5N65zIajNZ/4l213N7322KZP9SuXL8tZfue69Rs6Dj3205ebkIOOOzv57A3+P/1romPUWh438fi/cgTc/wsHpPP7v1mU4CYJJ6sSu8bzeWagKd8L/1fB2E1RivyS9UuSGQvDCuXJlCX2a7HWVhN7l0bdzmYS0/sMO/GmfKuoWdZ/G7MsS/kPjJ39DD9r2JHg+TG2PLyay3I++jXZQEvBU7grJtOaLC51S9yt9S1OQsLWmMc4JpHijBwA67s623HycAeZmgEP9Fc4oSkAAAAAAAAAAJhaE0lAf+MbixsaGk6d8n1q8tFHH5WX/3LFCn1fX9+f/vT/PvnkE+5gTU3Np59+xlWbUALa6/USPi+YBealLH/w0eXmit2HTL3eXt8jBYPZYR7f9wTBKU5Cd9tsRK7VyHmfdvfy5BrNPH4gA93L4fsi8uFe8Lia3qipZZ562bpbeXW/eWZnjW8lpGjhD3JyCvw9C3RhMMEty1p550Kb4V3f4mxvlN75jnu7mg699GpLeF+7zXVHX6076ttAeu2zz967cuGbTXXIQE8PKTcP0ALimN9/g8efqv4ioYtQv/xRoien7++XJIxIXguJUDiYXY6BY5SmgsQ3ZcgZw+uVn7vEGeuU+isFLPd/VJQly8EaTGs7te62FSwxHfE9TEEWramxsD0ut1Ahp4iVyGihm+mJKfUZfhZLBo9QYpmQcsbcMsu62GC11KVr8t3HqxvtY8fA9lhdNnLqvaPtrCyzII1194XXiXF4I/TFbWGEqwp03KdU+Ro5ZYsUgHjCAx7WX+OEpgAAAAAAAAAAYGpNJAF9+vTpe+5ZvWXLT+fOlXd2nvv97//AZZy54/Pmzdu8eVNq6ryLF2233PK1o0ePkgnotZ8+3SXX37++7uWjZtHi0vvv1Jqfs3WT3q6mz+3ruONNrx01y5eV3q3tPn2go9u3JcK48VIWLlSL+Px5Gt+XhQUFvO5em/nz9q6mo7Xd2x789Z5lTV0idYrI6/Xnc3u7TZ/b5HeWrF9mO3pBrl+/fJ6txuTb0iPyAuleV7eLyNU5WllNnd23ufNCeSB3faULga498r0c828Mh0cWjezd4PF13ClN3dp1W7au697/k13HukTLtu7eqqkpf+yFOjuRz1P7NvBA8vlaGCh4pPcX/9SfNn9AWux9/zuJv/8Z5fvrnBT2uQ97U+aRM7+hzlxK8FRSdXu9Bz4hAgH57D/4vx9MNzMfJ73n9v72Q9bjTvzvH1F1S9gITY2Q8FmUpoZxnTtj0+vX/0MOSU4WJpMriU73+RZGtv7BTUuZdsOBw8bk/JJ1S26SKGix+8EfLrHUHnzr5HkuA91BffM26qNjDDtaU2NhrU3H2+9b8/CmYsLajO8cs8aWgA47i6Wa65jvrv/hJqfNzvJIR8wtcx2pY3KKH97E5YR7jO+85WIp5ZKQ/h5oDw+g+XiHr3HuZ7v33Im36iK0HOPwNkaI88x7b8vvWnFHwZftFqc8YtgxDnh4X946Fdpflp3IFAAAAAAAAAAATK0EiuKT8fvxj3+UkkKfOdOmVqtSUuY9+ui/cAf37v2txWIxmzszMtIvXOh6/vndZGJEmtWPbnlQr/ZFZmv6w3O7Xq2zB4//aMuDt/qPX/hk//O7DzTZCU9177O71pl/vel53+pf3sLv/vtTy5qe3PLSaX86Vla49d8fER3YUn502B7QoqwHf/3rdWkjL2p69Yc/qWzvJSJ1wbICFb/rdJNX//jWhcce+/kB7ihPtWzDDx5cvXgen4vo6O9+99qJdv/VvrfrqWWfPvnTl0+PSP7y1Cs3P/Wofh5xubzd7XXtsgJ1XSCk4V3zmg2/eea5Y529Q70O713Icdfpt3fueqmuy3d4YclTT31vUfAJcK7P3/51+f46Ox5DOB4LFszv7DxPptpAwY+9j83jjblNB1y3ZDn/8EB+6+sVdfbZnBRWqVIvXGBIPCUlJblcDv8eJlOMoiixWNrX10fg2sH8zm7xm18AAACYrTIyMuLxKzwAXAUTTEAPoWl6377/euqpHTwe7+c//9d//Mfv2Wyxr5IclShFLfdeMF+znKqsYPO/b1W//dOfHzIPhsCTpYh6u+yxrTTmydRqkcvcGdoBXsrKH/98NXn3pd+8ezrmNcs832iQLnMXVjlPoXgloNO/w/5AkPTsK0hAQwhZ9tr1K9OEbkvjn0+cbJ7la5KRgIZJwvzObkhAAwAAwHghAQ0wc01kC47hGIY5evTdJ5/czr2uqjoyZdlnTneX+RpkW2ULV9+r14h4/JScZYvl5ldP24blj3vtXfaYW+q1m9sj1e7tMuz/rejRx596ivfTxw6bY8uv93Z3tSP3PEMktL3Be4wAhLM3H34ZTxSOm4SEhIGBgXiUwnSA+Z3d4je/KEUpSlGKUpSidDaVAsAMNdkENOc3v/ntm2++1dfXd+nSJTJreDvrjp4wvH3i9FSnfXkpyx/9cYlWZDa8/ekF7JgBADBFRn+fOplSmA4wv7Nb/OYXpShFKUpRilKUzqZSAJihpiABzbl48SKZJeynj752msRRb9eJ5x87QQAAAAAAAAAAAABmu0QCAAAAAAAAAAAAABAHSEADTIhQoclUi6fmTwhg0ihxWuYChZAAAAAAAAAAAMC0ggQ0wPiJF9z17dI1uXKKS3wqF2gyMzSa1JmWjJ65kQ+hZMqh4Cl57j3/+O0ijZgAAAAAAAAAAMD0gQWcAONEyQrWrKKNFXtPWVkiTFOm6dLSNFnCU/te8x2YMSh5jJGLM0oeWNr+VkWdnUwvwtTCNXc4j1SctLCEtTdW/u7c0r9fvybnrcom+wyaBwAAAAAAAJhSPB6VnCxMSkpMSMCyS4C4GBjo7+vr7+lx9/bGlIJBAhpgfChZZq7c8ue3Aylbd0fdiQ7jgjW0fngdoSJDl6UUujtajGetbi6Hq87NkvewQpo7ZGzucAV/OCmxOlOnoQnTbjwTOChULsrNTJMTu6W92ThULzyE3KLbyUfvNUZJtPouJ+7pkdASLoLmjsFaI6OKHHlISGLNktsLsufTCvnKtUqXtaX241Y7G9q7UYZq1Di5zuqUyRTFMjZCS3pMxjNca+FjEuGITK3LShO63UJCnFfaY63GU5aCpVmy5hn1SQAAAAAAAABMGR6PN2eO0Ovt7elhBwYGCADEQUJCAkVRc+YkX77M5aB7x6yPz4IAxodKllFuq22UDKc4Y82379FJ3Kx4yfoNazPFhJKk3bZyeYGMsPKcwBEf4YK7HrgnV+hyCXPWPFCk4ZKpwoy7SlZlJVstbkXuiltH2U0iWUbTsqgbHnOXW7ryjgKauIWL1j0weLmwqCIIC8lt62hptThdLi4h3tLSwbjZmNqJKU5KqCxYqiFueskKLSGZd6zMEnMBrHng3kAA6x5Y7R+TsCPijHUP3JstZIksI00+8iM0t8vmFsqT8bkaAAAAAADAdSo5WeDxeLmMGLLPAPHD/XxxP2Xczxr3ExdLfWRqAMZtjB8b15nK//ydTJlKyygblU1LqHYuNWprP3nq4w5ikafdwR1pdbEUnZlGMXWM00nOMlR+Fk21M24366ZsPU7LxwfqrO5IOW5x5upv35Upl9Nyovhhrr3lvd8faXWFV2MDl2M7xFn3aOW+y4VH1Rq2wDpCSB3n21mx7TbaYjrTGtyCY+x2Yo+TyxgzjM1JGIa4syhKSGfSbNORk/UWYuEi5wLoIOFHNHI3d+RjC2Whs+4I6TeLf6cBAAAAAABcx5KSElkWfxQLcDVwP2tIQAPEBUu4zDDFi16BUuSXrF+SzFgY1rca1zJ0HvEnSAd/6ihCUcm0JotLsBJ3a32Lk0vHmo+9/k7u7beuXJGZxja/9dIfm8Nytq7Woy+3Viv1pXeR9183nGdHCTNwPZbyX5CNEtXIyMNDirV3E44zJABCsWzvsMhHPULCmuVK2R6CtxrXqYSEhFHWOEymFKYDzO/sFr/5RSlKUYpSlKIUpbOpNBbY9xngaorxJw4JaIDxYZ12p3ARLSSWK9lhf1p5MCctvilDzhher/zcJc5Yp9RHbafH6rKRU+8dbWdlmQVprC+tLaYlLuN7f6g7pr5rwz1aWtjscpMJoYQyse+HW0YLWcaf9Y4S1YjII4Tkr8JFRvkSv6O0MzXYHpdbqJBTxOqL3M30cKFHP0KJZUJqRJJcTCuF7mbnUAKakmly5pN2YzueSnhdGP196mRKYTrA/M5u8ZtflKIUpShFKUpROptKAWCGQgIaYJzsrac6lty1ctGXRz4P5jXd1jojW/LtRwp73edOHXzbdMam16//hxySnCxMJrYozbDW5uMd9615eBOX/u09d+KtOv/zDdeUrqDdLlYo7Gk+wETLPrMWw2v7yah48sJvP3K3XEwsJ04xvihd5yJFNTLyylNhIfnqnG9hZOsf3LSUaTccOGw8F1PvYo0zdEyajrf7AigmrM34zjErl24OO0I11zHfXf/DTU6bneWRjqGTKVn2ilslHe+32K8cyb1r7UpSfe7lj/BUQgAAAAAAAACAayKBovgE4Lq0YMH8zs7zZCLEmtvuvSur4+3XT1imX2aTUt76wBrxsderOya4fnoGolL1D9w7v+X9/3vyrIvAtKBSpV64wJB4SkpKcrkc8djfjaIosVja19dH4NrB/M5u8ZtfAAAAmK0yMjJi+RV+7lyZw+EkAHBVSKWSixftY1bDCmiACXC1n6zYe4qipucvzj0uxuLuua5+qWetJ1//nQF5DAAAAAAAAACAaQYJaICJmq4Lt1h705Ej5DqDVXQAAAAAAAAAANMRng0KAAAAAAAAAAAAAHGBBDQAAAAAAAAAAAAAxAUS0AAAAAAAAAAAAAAQF0hAAwAAAAAAAAAAAEBcIAENAACzQUJCQpxKYTrA/M5u8ZtflKIUpShFKUpROptK4VqQqFQSAjA5FAEAAIgDlu0j8ZSUlDT824GBgVEqT6A03vHD6DC/s1u85xelKEUpSlGKUpTOytKpIslbU1ZSlC5lmquPvFHVYPUdUxQWFwrqjxg6I56h0G/ZtjGfFnjMVbu3VzR4yWQolm/Z7mvM/42nrWrXjormSC2OHtIUGq132pKdL2507HzoZ9VRw5iaOPl592/fqG3Yu6uyLb10+0PZDS/uqGwez0BLCss2LTO+uNtgjf+1Rr2cavmWjbrq3S82OMnUGUfvpickoAEAAAAAAAAA4PrApfLKiknFrp2ewrLNW8ocm8u5pB5fvay4hM9UGzoj5iGtxqo399Wq9GUlWimXOJ5cAlogpWlH7b7Keo/vO0dbW+TmxghpCo3WO9Ph8k1GT9soyeUpilMgVanVedIVuuOCQr1ORayCcTegSFdJYzpr0tca9XICmk5X+EqmMgE9jt5NT0hAAwAAAAAAAADA9UGqoAVMdZvJ1Gnasa1Z7XFoix7fujEvXU2TrfvytwGN+AAAEABJREFUPQ5jxa7dTNHWIvO+8iMmQrTFj5eqP9i9t9bQrNWVFitGNqYovK+sRK8WONoMB/dVBhdT+xYU06a9O/bURktBepj6+hPDF7OGtCMNC6m8yhThcvzskq33ZxNC01LGVFX5ygfNnrAjzvAg+dqistKibLXA3Fx95JWqBmtzpN7xs0u3bylOF3jMht07Aut5+dnFm0qL0tVSYjZWVew94lkWHqc5pPHY07Aes4lo9csEWmK2Rhve8CMq/f0biwtpD8Ncyc+OPQXh15rE5UIJBLS+7OkS7j4zHNxbWWuNfJ+EzoKTH2HuYrncjIA9oAEAAAAAAAAA4PrQ2VDdlr65/OnNJcvVjobmTq+p+pmyDc9UGU3v79xYWvowl+p1thmJrnhVHp/LuK4q0hFjW+Q0pmJ5WZneWbVr2+5qUrSpTB/I3zocnQ6Hw+zwRI9BQOfnL9fruf/laSWBdoqcVXuG2gkPafByI6oRgVSry1Nbj+zc+WKzYuPm72Tzw4+EBynRrdJLrL4jBn7xps16ReQgvc0V279fuqPKQSuCyU9JYUmJzlO1a9OWPYZOqVrNjxBnjI1H5GHMgrzSPGJmuLETROhvhCN3+nu3Z0dFLaH5gw3FMAUh14o4vLFeLnx+pR7D/h27qzxFD0VuxzeYYQMVYe5iu9xMgAQ0AADExW3ZNy0oWP0PD3xrTYFaSGY+YerSu5akxbUnlCxNKfa/EmsKFili/CMlSpZ52+o1BanUiBZGJUzNzhzWfOSz/DEIhzUevQVxWv5da4oK0q40IlTmr1mzRCn0t5Mbc1+uoYjzG9NAhRh17kIavGYoReYi5bhv5omdBQAAADDddFaXb95R5dGWbNuz/+kiVaQq1oZqo6CwKF+l0+dJjQZj5I13+WqdWuBgBFruH06HgFbT/sPehoonNpcfHGVTYYFApS3UF/qpab6vHU9bTb3JamqoNZPBdiJdLryao7Ohpr6zs/n9yn3VRk/4kQhBOhv27tx/3KHijng9ApqWkhh5rFaPIr/4/rX5AuOBN6sj9nDCjXOjQjprDW3mNoNvzTA/Qn8jHUmnHf4jzQ21Vz4mGHMKQq9FyGQuF8bRVmscrZ2oAxU6d7FdbibAFhwAABAXJ5vPEepysjDV0mh2kxmPkitpoYKVUx0WNnBAmZuvJCxxmr4UZmmTWdbZbmIzdUqKtTQZiSZLQlHknKl3fqCoxZWapUxmmXNOZW6WnDgtbV3C9HTfi6ZGRuYv+tKWdscaHTH++U+N7kwd7a71X0asWZJLExfT3NjuColIkZnBY+wymm1tbJZncZcTKpcW+VswGEnIdVsbOwKnU2JNTpZcqBRauljNQiXltrQwyuB16+yKocpcNV8MrH2wcSLkIvHVN7YQbaCF9larfyzEyjSqpbZVmZUqtti1Bcpzdc2uXsZk8+UqhZr8XJnlGJnuwud3lIFqdGt0/qEwCbOyfON8wSH/WmA2jU6Nf+6CtwfrbDWR7CjjRnyJ+uwFxGKXKUmXO22h7+Yxmiilf1oHnMnzU4ItBG6njrpG/4lcaJlqSTKvt8d2sVeZnsKdZWLowH01dDuZGHlWIICwO8fXhITWKCXJtO1KeIN9aW9stbPB4Bbp/E2dEwZCSuyl01IkyUqb6RylTPAHyVCBO+3LrmRtStTLAQAAAEw31trKZ2orX9Rv21myNvv43vBEpbO+2rhx85r1ArWgbV/96A9+82V9PcaqPcfb2khsPI7m6r3PVA82y88jk+ds+KCS+4eEDjkSbHxYkPy8h/ZszW6uqKx3kPHxNu/d9jPjqqLCwvvLyx5q2Ll1d9gOFxNvnPgWIpsrn9lK+NllejIBnvFUnuS1Rr1cLIGMPlAj5i72RqcxrIAGAIC4UMpm02eclJhOpVhKSYsHe0VRQmI7Z6NohYBH2UytFvccBU0sLRZC3zSPFtoYJ6GEg0UU6bHbeoRpN9NSyuV0uohULuP7X4hlol5/UZqEaaxvrDtxstlqb28y2gjPdyUhTZMOY5OJYcNDSpZLhMlCiVw4GJK7I9jCVyTkumkKkWxBwdJ8jYz7aJ2yfWlh2ESFUkbcbkrCG7ouO1iZSxy7rsQQIKSD9W9QBVsYCsnV0e6kF+fTLqubtTaearKyrNvKvSa+tdFppL2Dyi1YML0XzkaY3+gD5ZIHj4hFgXHuFQip4GySjsC4+W4PJ2MT0imqqOPGcdtckszcTLm7Vxq8eebdEJxWkWCwhaHbKRgb14CclolltGTOjXP9Z80bvK+u3E7z5gRPl0UceZa1Mpbh4Q32xT3sxzZ4PwyFJBxg7ZYvuXt+nmjwyOAdLqBGvRwAAADA9MEv3LRv308LJSSQ0hMEtl8gHt9GDIIr2+w66z+odeQVrxAYq6/sYuzwCILbNfh5/Zs8MG0nDIYGh0ClHlzsq8i7s6QoT0Ji5XUwHqnUvwRWKpUKPMGdI0JDilJtzMZDg5RKVVLGcLiKO2IyD6sZ0rsIJNlFq7SOw3t2lZfvqxdo89X8sDijNM7PLnl8x7Y12ePZRiK8v1GO+FcP8+l09ZUhH+8UTPJyIQSBOsGzHBEnLtoshIU09uVmBKyABgCAuNAoZUwrS2YJSi48f+rPFmUWl1+zB9cSC1N1OiHravmSpBDWZelwK+RfW7xYRiz1LU5RliZTSRk77cRfxKYtXZ4mpKhEZ9gTs3lzM3JoPkURC2HdJG3Jbc6TLVTB7blpPZTtvZNmp1uoK1iuc9UfM8p0uWJT3RlXcFDZHq5Ik0ZczSwrFmqWrKTIscbBFsjI6xJLn/1s3amzvoXbrCwzS0FTLZ129zwub8q43CzlP+vUl/KcQGXf8ursW4Mx1BF/43UNLjflq3/JQS/0t9DcONgHN2NnnWf+bLSzlCLXvwKazVyyNDeTJV/9xUVoWk6x7WRaC59f1h11oE62BIfC5ZGTOdw4mynZTan+dhLnLrr1Nt+4dTexpNd3pM/lCpweYdyIb+gsZGkOU3fJKZH5b57GL8m8LN+0tvUJSb+vitfOsOm+26lp8ES3mxUnE5ZiL7WwN3+dO+vCmc45gfejQ7fTV1yeOninCFNzR9w5QeyI8Ab70jG0fllIZwXuhy63S5juDylBlqrLErJu05dsIMiWPjJ4pylVCQQAAABgBvDWV1ebt2zd/4Yvb2qu3bu3wfcO3dt2vLptc9neio1M/b5duwydxGs8bugsFjRX1w/ln001VcaizS9UlHkdxoqd5UdMJkNFdeHmXW9sJHyBo2H3joP+aqr80i2bdbVMfYPBGltMpup9VYWb97xR6uF72g7uPO7f8Tk8pAjV6BgaDw3S6jC0qbe8WFnCOBjmysrasN5p12zbWqqjFWqapL+o22is3PmrBmnehq0bNzAOAS3orNxmjjB0bREbp9WF+hU6QbX0SHOMYxJxWJxM2BFPpbF464t/KDV3MtKhy41/CiZ1uXC0fvMrJWqF1GHYWdNJrBHm1xp5oEJCqo3tcjNAAkXN7E2sASZswYL5nZ3nCQDEgUqVGu+fL4GA73I5WHbqc9wURYnFUo/HO2otYdrSHMr4ccT9BihZxtLbsyUdJ4412qcqPkq8IJO2Nl83+xtc6/m9WsQZt+WydSfPjrJNzSRvp+l558RvfgEAAGC2ysjIiOVXjLlzZQ7HlOyWq/Bt0GHdtWVv8/R44wgwHUmlkosX7WNWwwpoAACYDRISEgYGBuJRGoW749TH0cpY+5mTR86QKcW6zjZfx5vrXvX5vVpcZ06eHKPKJG+nGXHnxG9+UYpSlKIUpShF6WwqvapUeUXpjtrKNmSfASYPCWgAALimKIqaimWQo79PnUwpTAeY39ktfvOLUpSiFKUoRSlKZ1PpVdX5wfaNHxAAmAp4CCEAAMTFmgK1UJi69K4laVeeSiZMy86QCWWZ2WohoWSaHI2MEsoyli5dIB72eagwLf+uNUUFyun2MDOxpmCRIsbPbSlZmlI88dNDCFOzM2M7lZJlLi3S56YKY2owPKRhR0K6wLV82+o1Banj7sFQO1wLuQvEZHqiFJmLwu646FMWGOe8zK+NNiYxz3js8xutzaHZmcQ0DZ4YcSgAAAAAAAAmDiugAQAgLv7caGbpfFqoYOVUhyWwxJllk+n5ymQxz9IhW5AltzW2s25ypoXOV4rNrcHtbYVKJWWqa5enpQoto22Me5WJNTk62l3ri2+RTpnMMq0mKjtXSbEWE0PnZsmJ09JkdKbplJTb0sIo71ijI8Y/G4xkvjaZZZ3tJjY7cLpYsySXJi6muTG4Jy8ly87PCtbJ9J9utEiylNxYOVsb293cdbPkQqXQ0sVqFvpLTcKsQP3GwSHztemLpMVC61fkUh11V8IeirYx+HA5aliDmYMh5WRJKIp0tDiDR/w7XBf5u/CnOrsiK9BCY7M8i6tG2LDGW1h1yIvA4Awbij+dbHazvWykkKYFCa1RSpJpW2uLe6gLgRm/MkGDAy5MK/imf5ydbY3NIv+YCANT0GVieHJJMq+3x3axNy1wujI3PzCbJqIJjHNdo3VwDIem46vLlMJrscuUSZd5N93orz8YyTmncugG04TcRUPRBmeHtbcGp0lIZy8gvgZJe/P50J8j7rKZ6kCcXU7xzSnD55dKlkiE8gXZYleHa3Dqp9NMAQAAAADAjIMV0AAAECeUmE6lWEpJD61vZm0Mq8xKZW29tC5TKNSsXJrqT2hSyVc+D+VeUXKlnJpmn5G62puMNsLj8nNCiVhIenqSaJpwKV8yj5ZSLqfTRcR0mkpG3G5KwmMa6xvrTpxs/oo7wWZqtbipwdOF3FkdxiYTc2XTESpYZ45CGTj9hjlC4mRsQlomJBRNU7YvLQybOFgqFg22OdiAMBgJLWGM9Y2NHx2vG5Zw7LHbeoRpaYrBJa1DDbLdgyHJaaGNcXIdcw/20bfDdbALVja0hWEGi0TBMWGvDI4yZCi4lKurvdnMJTIH60yvp8+xrJWx+MZcMNgpdmjGQwfc3RE6zoNTMHcuX07LxDJaQnWfCZxOUcHZTJk3OM7Dbuyh6bhsd0kyczPlbnf/4OwHI7l56AaTkY6wuyjq7LhtwQZdET7F4cZ+ME7iCmtBmKoryCSMnUzLmQIAAAAAgBkHK6ABACA+EoQ3JHXU/rmL1kiEiZcu+495bVYiklltDuvlv/LmpWkE/Qk8UcoN/Zc6+hITE/xVPA5Xv0LQ3+9iad0tGgF34FL75+bLvv3grtmWcAkJ1NzMgvx0pXvAVn+p39vLVynnNLuSs2+ZT6xnHckCfiDyHoeIN+D6yuXtS+ylc76h/aSd9fax3Rc6PfKsWwOnN7kSVbcsTe/+7M+fefr8bQ8M1ZE4FALf6e6UudRAX29vf0JiX09P8gKNZm5ie4fdIfeVOt03eAW++t0kMcH/MXKfw5Wcw0XS9VkfmeM/K2Hw42XBjZqseYIktr9v8OCVBuVZgR5Z/3KhR6FOkye1Dh1xfmK+3HfZ34W+c4Z+LGYAABAASURBVDcMttBHElNvuT2//+RfLZ4RjZMkXmBM5Bc9g4Njd/QLhg9FzydnHf7+UlSw8jw2RSKeLvNL+nt7vb4xT5JrtIFODY6Grak7MEFDA+4bxuA49/X5x+RToyt5oW8Kms2CVCXVl+TuFgVPd5wOtuy1Xey52TfOp4dN0NB0nGmydnpzFnYx3f2ykEhsbK+311e5/4aMgpF3UYuJCpudz/sGXwQbTExOWbRI9OWnZy/3DfXY09NDJfridIs0IS00tznPNXd65qbRX3kiz9TEXMP5TfQjMDn9fgQAAAAAYPwSKIpPAK5LCxbM7+w8TwAgDlSq1IsXbTFVTeTxEvp6+8bOayQkcEmkBK+X9Xg8CQkJAgHf5XJMxfMLQ1EUJRZLPR4vly/jrsLh0i4DA7M385LIFybzE3t7Lnv7yLUz++d39HFO4AsFAx5375TlaIcaTODxqT5v7zW+ga/a/A4nEomEwmRuorkZJjA53PRxH9X09LgvX+4mAAAA10JGRkYsv8LPnStzOJwEAK4KqVRy8aJ9zGpYAQ0AAHHR0+OJraKnh4xDUlKiRCL27UgQZ1zSSiIRXb7s9npnfbbF0zNtujir53f0cfb0THh18RgNju9HLK6u2vxybrzxRre7l5tiAlMnKSlp7twbL178igAAAMxCEpWKdHbOgOQ1X5GtkzINJmv0KjOmL3CdwB8kAgDATNLX1+9ydYvForj+Ob8/Oyl2uS7jT86vMszv7HZ15pf4ss+Ky5c9mN8px80g9+Eil4MmAAAAs462ZOf+F7cVqUgcKAqL1+inqmXF8s3bH1pBX1nuw1ctL9v2/L6KV3ZvXi7xH4lnXwAmAiugAQDgmhngU4SXlBDc/TlShf4B0tuX4A39O3232y0QCEjc8HhUTw8WTk4W5nd2m7bzKxaLPZ5eAuPBfSSQ4BN+PEJlr7dXJBJ1d2MvDgAAmFVMh8s3GT1tnWTq8dXLikv4TLWh00smz9NZvbe8oXlodbNiRVlZnqNi316Hx9wQOBrHvgBMCBLQAABwDfhSHTeKEvi80asFkyFu74D9csKwXVz7+vopKmlEzYSEUdZUjrc0KSmpr+9abog802F+Z7dpPr8CgRA7b4xLgm+L7kjpZ7/+/oH+/v7hpdwMzpkjHJ6AntoZRClKUYpSlKKUxJmi8L6yYr1awDQbjrxS1eDkZ5du31KcLvCYDbt3vOhL4qqWbynTE49ATROz4ci+ylpr4KwS7ixHm+HgvsoG3xH9Jl8tIvGarHytwml4ca/BoS0qKy3KVgvMzdW+xumix7duzEvnGtq6L9/jMFbsKq8yhTelKrxvY4me9pjNHoHX8OLuGrpk6/3ZhNC0lDFVVb7ygT/hzA9p3KPIztdpC9V8T8PggujwvoT3N1JfYhq3CP21hjXFzy7eVFqUrpYSs7GqYu8RJj+WsyLhZmGj3usRaLnQa6v2VZzoDI+cnx02UKEBcEMXelak+Q0fXmf4vIRFTiKNCYEw2IIDAACugQT5HOLPXg0kkCTpnCRpcnidxBRRMOEh5CfcEFohJCEy+vvUcZVyzUb8y32uGpej4b7yeFfh41s+rctOl8ZycDrC/EYxY2ZwdNN5fhMTEyf+W6tUq0uXkOuMf+2z7+fC/6TIYTnoQFba//hBblTDziLDD07hDKIUpShFKUpRSuJNsbysrMhTvWfbboNH/9BmvYJ4myu2f790R5WDVkgDf6YloNW6dGLYv2N3taD4oTK9xH+W3lm1a9vualLE5RwVvlpShZoYq2qJVmusbhDk6bMVEt0qvcTqq2bgF2/iGjdVP1O24Zkqo+n9nRtLSx/mss+BAJxVe640pVi+kQupas+OigaBLk/FBSHg3pfkqa1Hdu58sVmxcfN3svnc9cIap3X3bSzbsEJN64oeKivbWLo2TxLel/D+hgcQmwj9DR8WSWFJic5TtWvTlj2GTqlazY9yVgwBcLOQn86v5WahyqPfuDEY+cjLhQ9UWAAR+hs+v5GGN8K8hAUQoXcEIkACGgAArrYBKonLSRF/9uqGv83hq27kz6clf5szQHxvNxOzcuf+Y65QJhL+zcLkrJvnaPzvm5IFAyOXTPb1DSQkJJA44JrlGo903JeISUpKHHlZ/oon3/w/L+365cPFuokkFvnqVVtf+/CDl/6V+xR9+HGBVEpLBfyRlcMOCrSr/vXF//tamS6O+xmMG+Z3GMnI0yNOq9+0nMqIpvn8clnR/v4R88v9HisU8vh8HvfRgr+0b9gnEIr1vyxfm569/snta9Vi7vcQmgyuHhJkf/+XW1fQo19Nsuxf93Pz++T3C+lpP3HRJPoXP3MvkqikxETuSxLFvbjybYK/TuhkcYMcnpUGAACYEfhqndrTZqg3WTtP7N36cHm09aqOtlqjyWpqNrQRKU37zhI4GIGW+4fTweUvh94leDwe7v+Jg/t/IiDOhr079x93qLhqXo+ApqXRAqjhAjA11JoJ1xTf15y5ljvS3FDbNri3hqOzoaa+s7P5/cp91Ub/W5SwxjsNz5SV/mhvven4zu+Xln5/8+4Tzhj6Gx4AGYcR/Y0wLB6r1aPIL75/bb7AeODN6mZv5LNiDCA4C4MDFXEWQgYqLIDIlxs5vxGHN3xeotwGI+8BiARbcAAAwFXHD6aiKMkc9tJlt8ki0KQSXhLvprks451zC+VtIXMWSr0pC+d+23pxzxdXzmKvzbYJXAKLy8hwXz2eXh4viWVZ/5rBwYyMx9H20fH3jF/M/c6LL6UxDoH5D//2Slv62n+6K59OMrdJlq24iXuTUv/6Uy8wq5748a0C4ql57ucVxmCay2s+fuDQ30o9r9eYPYoVTz7zLQFDSFPlh/KSB5d99m/19YxA9x3uLOJwNFWdmFOyIXCQ0Mv87ZP63778Rs2j6WRawfxemd+h041mB1+94js/foSbwS+ljzzmn+j63z51mMmfxlMZ0UybX24qPR42sJxK6EudDwzLUDuMn5F783WEtBgWPfCvvh+6muNEkP/9Jx7I4H6l4PeW7HrplsCcHhZ859dP3sv9DnLg5z8ZNr++3zc8Hob7dYOfvv6JR7gf1c/ef+oVA5k5hu50bogG+rm8c0IfO5CYxH2ekJCYOMC9Hqx2Nf4gGgAAYPrwRD3qMVbtOd7WFrGcn/fQ3q3ZzRWV9Q4Su+DO0Fzq0hkhfels+KBysPE942/8ahg+LF7v3m0/M64qKiy8v7zsoYadWw+QiYthFvKHDg8NVEgAL3hiajl8eKPOy/AA8gnE4lqtXBClqFUpMh4BAIDr20CPV3BzivfcVwPeXt+Kyl6W7VVJ/0ZFut39XV846lmeRhTxRC5pEnEjhcnzbw4QejDwV+r+/EvC0N62Q4LvRzyOukMv/Ntv32/jMlc0LRBI1Ysy5nrM9UYjd0R6oyK9wLfK2UME0mifi3uYukOH68jN/X994/X/Z/a9seEayfC899zjP/n5a386OniQDLav06mn94YBmN8rp/s+bBicweBEp9PSGTOVEU3D+Y1yueCcDk7xEK+5zUzfukzacfrTD6780NFpno/+cLjuK3JTzuCcSriDzOtPPf0Hh3rYSian8Q/PP/VvB7r+di33GYKD+3hCKpWmzNRlLwkJiTwqkZtHyveVG6t+1sv2Xb1ZAgAAuEq8DsYjDSxNVhXveGVHsSq2s8wOD2HaThgMDQ6BSh3lb+PEUpWUMRyu4qqZzFcO+1fGDj6E2R+A1B8A99ZB4OHaNZsZQV7x+jv1xcVFuqhbOEgjNz5m5KH9jRCAn0p/f1np8piG40rjYcMiyS5apXUc3rOrvHxfvUCbr+ZHDilCAOEEwcgD1RwxzUJYACS2y0UY3rB5ifE2gHATXAEtWnjHOr3a+8m7b9d1hT5lXHbLvfdozB8cruuKfn7KwtWld88zH/pNxad4fjYAwHXHG1wIyTovi1LTey9cEt6ckjhAei1fJZAE9+HD5wLFn568POIsllw7iYkJ/f0DycmCPt+f74/YPcBDHJ/VHz9eT3zLKLl3N21OIlDlFyxTSx2e4Y+57nW01Zk9t3KpR2Pblfc8fPWK9fcuW+ZxLKt/zjh0cP6qh/V3LaMz1hv/7ZC5Q/qv//r/3eWofbtWsS5wsOv/SQPtc+04mQ7pwz9+kvzXc2/UMFPxWO3Jw/wOe087eLrTt6vc2of/yTeD54+6EoNvn/hS9XSeyohm2vwG1rPzfZtWD/T29vX29g5tOkF8f3zZ5klf5TlkVwdnx/dDx83Etx74DpG6DZ+YM27xz6nTQXM/iT/+EWHe/7cra4746mXfDyx7r/EQ7qMEj4NI1emEVJOZg8vJBwaDG5oRa9T7R343cttuAACAGcxUva8qb/OeN0qJRND25o73O4l2zbatpTpaoaZJ+ou6jcbKna+Hn2WoqC7cvOuNjYQvcDTs3nEwYtsX2wxt6i0vVpYwDoYZWmbrbTte3ba5bG/FRqZ+365dBi6AQl8AHr6n7eDO4ybiNO3cIdhcWlQkaOhsc0ZLAVsjNh4ivC87wvrrDQvAR7Ws5H49s+sNMq7BDBsWj0eat2Hrxg3cR/O0oLNym9mrDj8rYgCReKT6zS+UqFUC8wc7j3cSp2PsWQgPwGQOvRydF35ehOF1ngidl9huAwiXQFH8cZ/E5Z/v/e66RSJiq93/0onQPHPK8gc33GKuePmouXe0JlJSeN1ddqSf4dpZsGB+Z+d5AgBxoFKljvHzNVc0tI0sJZnDpUD6nD2j1e/xENuIdBaXK3Q4LrHs1Ge1KIqSSm/o6bnyjs6/RUMiy/ZzaSsuQYmdT8eG+Z3dpvf8isVSj2caZ/CnGe7+9299PlpymftUJmT/DYGA73I54jGDAAAA0WRkZMTyK/zcuTKHw0lmKH522Z5tqsrN26ut5CpT3LljT0nnzs17G6bN+yjtfTu3Z1dtecZw1Qcj1DWcl2lPKpVcvGgfs9qEVkDzROp5/Auft/O1arWMdAWuItIUrFy2iFz43BzMaPNSsnK0YlGKRm5uOi1amCPvrDlWZ+7mpRQsy5GL+MR7wVxbd3owA81LWbhYw7fZeNqcRTzbJzUnTnf1EgAAmKUG7JcJTSVwWY8B0ue4PEbl/n5ivxySHQl5ztjUCmk88Ng6/xaoBNnJWGB+Z7dpPr8wLoHNnUdJQPu2hsbyZwAAgDhTFf9q/9ZCAfGYa/bvrLkGWU4+LfXUVx6ePtnn6eGaz8usMaEEtFyjFnWbT5+Wq1dq54nqfMuYU5atL1kpt7eb5IsWq+XEa+buXXmOXi83fXJh3p2rxU1NRH3HyhzzqzU2Xwt8Lt98i0bU3nS6ffBPUFMW61eqXWZzVzdJKVi/XnTg1cOnsT4aAGCWSuDSTxcuDfApwktKSIye+OCq9fYleLHIbobB/M5umN9ZhvvohWX7EhISIm2P7vuK7DMAAEC8dVb9rKiKXEPe5oPlzWR6MR3cupFcW9d8XmaNiSSgRfO0cu+FGrOV2ub3AAAQAElEQVTZZifLFqbwuCSyTK2d13v67TcPnO7mqe/eUKoJ1PTaLjQ1nSZacdcnn3bLc5b5nkPT21V34hiRFaQsXBbasNdcc6iizs5LWb5hwy1aOe90NxZBAwDMZr7M1KjJKeQ8ZjTM7+yG+Z1NAinmASxMBwAAAIA4mMDfmYrUmhR+L+GrU/iEiOep5TzfUR7xcrgXvd6Jrlvmzu71ZZx7ia8hHo8AAADEaPQFepMphekA8zu7YX5nuvjNIEpRilKUohSlADALjH8FNE+mnSfistDL9PO4JDFPrFGLAs8h5BM+l5HuRd4YAAA4EomYxBPLjvgrmYFRV+6NtzQxMSHe8cPoML+zG+Z3povrDKIUpShFKUpRCgCzzPgT0HK1Wt7VVPHqUXMvEd1S+uBKbZqozuTq9vLmaVNEp80irUbOI+ao54tS1CkikVzNJ2JxilZDuru7fPs+AwDA7NLT00PiKSkpicSNTCZ/6/cHhr7t6bn8u70vHDp0iMDVgvmd3eI6v4mJiWlpKgLx9MUXXxIAAAAAgNiMOwEtU2vlXpvB5l/10N1lsvEKNCm8pnaDoXPD6vt/VEC6zWbvKFs3yxbeWXq3JrhMeuV6Deltf/c3FXXIQAMAwLRyo/qWHm9/qizpvL2P6rb+13+9VF6+4Pnnd+OvAmcHzC8AAAAAAMDVkUBRfDJVRDIZ6bbjyYEwQyxYML+z8zwBgDhQqVIvXGBIPCUlJblcDpZlyVSjKGr+/AXVH32+QJGYmJhwwc6e67p06XwL9/o/9zz/7rvvkqnEV6ikjk6rl8TbVbvQ1Jgt8zsuM2yOJiOu8yuTyW++eT6BePriiy/tdls8ZhAAACCajIyMWH6FnztX5nA4CcwAEpWKdHZOyWRd86amMIAZRiqVXLxoH7PaBB5CGF23HdlnAAAI2FKsnbpPOK+2gYEBt7f/1JnLNS3d7V2e3oRkqerr87SLBwb6uVJJ3obdex8vUo2zf3yVfuPjO3e/sLM0mz/sWNnWTauCTXHfPTRV48ZXLS/b+audO35aki0Ju9D1boLzG2kGJ2MGzxFfVVT205n8Iw4AAAAQQlFYvEY/YzbxkhSWPb5ZryBXSVwupy3Zuf/FbUVTMeaTaCq0azE0FeFWmdhZU0VReN+WHc/v3f2rbSWFUSZJod/y/L6KNyr2/ao079q8hx//HtAAAAAxWLtxC53XUF2xr9o0Ixd09vcP9LEDA2TA3edITrqB+3z1w/cq33vvfS73lr6sUE1L9Tppdac19DS+Im9VcVGeorP2yOHqZifha/XFq3TStuNV1c2dhn272op3bFcLBIR4/fnH72zUC8wNbQ7uO0l28UMbS4uWCfIGx02QXVS8It1T/351rcnJVxWuyud7BGpBm+H9BobWF+c7qqsaPFz7Oqa6qjn0w3aprqjQUbWp/IQz9ELBQFWFXGACh8djfr/KSOtXSZsP1zt0q/SC+up6kj/sWp3eEb2wkllhIvPrDZ1BMnJkJNlr1uoERCpguG9NTjLWuI06R1M7QZLh91LEu3RFOjEe95eO1Sl/YFJVXnrn8fAbftTrAgAAAExbfPWy4hI+U23onBG/vAikinSVVECukrhcznS4fJPR09ZJJm8STYV2beymIt0qEztraiiWl22+X2rYs7tKvXHzpjJmc7kh/DcCq7HqzX21Kn1ZiVY6+KvM1YUENAAAxAXTVmuobW6L7z4c8TPQ1086Xc3vWZ6+3P+VnLp54PiiN373nEajae9M0GkdVZVMXl66pNoaklST6DZsLhFUVZq0RfetaNtVo95SXiY1GByl5dukW7ZWmkZU9jo6jbWmvI1cqpNLIHu4EWtoy08XBMeNn11Uopc2NyvKygvpLduPq5eXbkyvr2qjt+7I3r15H8kuKSVGs6mkVN+5syokiryyneUb9ekC/cFlncd3bi6vH34h37sNSeGWXZu5wDwlJekG4/tmdVGR2vp+vSBdX0ybDUbByGsJNvl6Ue0o2b5Nuo3rxSzYImKC8xtCoR8xvzXpRRtLyfvVjqJdhYJN3Ldboo/bGHM0tRMUei/Rke/SjeV69batx9Ujwg7v1C5fZU+6WmoVhN7wVSMvHXLdqpnx6xwAAADMenxtUVlpUbZaYG6uPvJKVQNd9PjWjXnpapps3ZfvcRgrdpW/LyjZen82ITQtZUxVla980OwMPcvpezf4UFm+ce/uE1zCT6XftFFXu3tvraDwvrISvVrgaDMc3FfZYOXeExVvKi3i3j0Rs7GqYu8RrqnwI6GNq5ZvKdMTj4ALymw4sq+yNpBTVOnv31hcSHsYZjBnqgi9XCiFfpOvJSLxmqx8rcJpeHFvW96WjXT17jcbnJLCsk164/5dbdqJXi68L+EBhI3SK46127cUpws8ZsPuHS82BE8Ja0p6Z2icBiZ0oPjZpaFNjR1SxK6RGJryLItwq4SeFTZ30vAbrMo0scGMcDfTatrTUHngRLOV7N7ryXdEviuszbWGZq2utHj4EunQavzssNueTJUp3YIDAABgEGNq8K96nJEpp4EB0tXT+nbnT7jsJPet4eUaLju5t/KPXIKST2fn0UQg8EjTuQxl6Ikeh8khzSvSqzor979vIlJa6jC8+cYr+yvbBFo6bMmA01Rb09Ds8Pi/8XLvCWoazFfGjWluMEnysmmBVK32net0tFVVvLFn996qBgex1n9glOpXrLgz3WGoMYcMsrNh78MbtlXWvPGz+4q/4/sAfMSFOHypOhhYVZvD4wkfgOHX4ktptVQg1foioSP0Ygaa8PyOxA+bX09bzZt7faPKvd2UjDpuo8/RVE/QyHsp8l2695my0h9V+r4NaS2kU8HAqv2BjWzKO/p1CQAAAMB0INGt0kusVbu27Tbwizdt1itM1c+UbXimymh6f+fG0tKHfclB7u2QLk9tPbJz54vNio2bv5PNDzuLa8lqNnNvhZb59lVQ5RflCdrMTsXysjK901etmhRxmV8FkRSWlOg8Vbs2bdlj6OTeFfEjHQlrXECrdenEsH/H7mpB8UNlev8bU8Wd/sb37KioJbR/IwXf5Yq4I1cuF0YgVaiJsaqWaLXG6gZBnj5bwb3hS/cvhOXe9irSae592oQvF96XMBFGydtcsf37pTuqHLTiyuLj8KbC4wwfqPCmYggpQtc4MTQV4VYJPytsMCOcNdHBjMr/K0On4WAVl22O4a6IHED4bU+mDFZAAwBAvFybv+2ZCgMDA8dr9t3o1XCvq1491tM+8I+/XNty7lhfPyvVFaZLpSRb4HtfoeY3NI/ootd0cHNJlSKvqGzztu97tr0fsfUx0pqBcePr1m8qJvu37XSs3bVpWOrOy72r8P9pF/f2Ubq9tLBt35vmcY+y1+PwCApVNC3hMoxWgf98SeCdHfFwaUXB8GvxtTqHufrNbXsbrlxHos3TCcz1zTP0eXkTnt+gsWZwUNi4xWrSEzRC6L0U+S71baahF9S/z4wMW1UcPUwB9357eFNb9zY4R7kuAAAAwLTgbNi7k8lO1+rUAq9vmaqUy5FGqObobKip7+z0vl+5j0g9xNkc4SxTg4EpKcxXvU/yCtVmg7GTry5WCxwGga+a0yHgPoQnNVarR1FUfP9acuT4gTd9fxLGDztCwkIycwG01RpNVqvD0EaKaZqLm69Opx1tVfUmq9NR2+Ys8u3roFN72vb5jjC1ZlLCXS5iX/xvIbn/+Zc2RHlfNrHLhfcuXNgoRQ7AE9ZUNpnI3HnGDim8a7GGFKOwwYwUw4QGMwYx3hURqtWH3fZTBwloAACIC2nJ8weLavdu2X51dmxISEjgsopTVXrp0qU9m18efuS/f37Y/09J4Zb72/aVb6ty5G/ZWZJOH2ge8cZAkn1/eXmxwOyQCph9jNPMVLdt3rC9nAgc1XuNvrcdjrYGT+nTb1Z5jPu2veBY/8zWIp2a9qRr9fue2FLRzLSZpGWBcdtR08ZIyzZs1Tq4j/prI0TtNB43eIrzDPXMWOPLVxVt2TXyQtbj+yvztpTv4d6xeao9hDHWOkof2rWLSAW1u7l8tm746V5zjYEp37QnTyAV1O/lPo23elUrHiovad7y0NXbEHqazK9v35QrM/izp2tGzu+KETXDx41EFTZHByY1QSGtMyPvpfC7lDt9VzaRSo17a1whrbWN7D7T1kxKt5RrzVJ1eFOe0a87iqmdX7j64jeDKEUpSlGKUpROOX7eQ3u2ZjdXVNY7YqrvbPig0n/W3ghnddYbmFJ94TJBXjCzSvsP+94WeYxVe463tRGvd++2nxlXFRUW3l9e9lDDzq27a5tDjrzgKQ0PaYzk31TmBidxOW9zWO/Ck61hoxRjU2ETFNPcxRRSDF2bQFMxNDmaiV4uHgK3/RRCAhoAAOKitOhvyVU0+vvUyZSO5Kzd9XAglTb0YkRx85ubS94cduCDXVs/CK1QOlThmdLqZ4aXehteLC16MfiN6YnS6uGFL5aNvJ5UrfXUV9VEyT9bq5/YGDzd21kdeiEuaVlfXeFpVutLCh0e35LYraUHr5TWjriWt/PI9o1Hhp0sSc+jjVUvtl3F5c/TZH5J6AyaRsxv1c/K/NtxV2592P99yLiFGnWO+JOYoBBc4yH3Uuhdun3j8Lt0ZGuhndpfVrI/elOjXzeqqzW/EC/xm0GUohSlKEUpSqecVKqSMobDVSdMREuXEG3wsG9tsEQQ9W84o5zly62aS0tKpAJz5Yu+zKrD7PComLYThk5JXlGRWlrf7MguWqVlDu/Z5ZTot+0uyVfzjWTFyCMKY+TGQ3gdjEeq9a369dDpaglpCBxR+Y44pVKpwOOILfPpcHgEUt9ZDqlvf7Zax8QvJwnrXW2EPyEMHaWIwps6HBpntFkYo52wkMK7RsbR1Bi3ShShZ8U8mPzski2l2Q0VO49E/ONMr8fDjZLUt8xaVbRjZ3HD9s31Ue8KbkAVviXwzsgBxBMS0AAAADMRX+ppqKyoneAmGHypWqfXa621O8vfH/cSdY+xcldb22x4FuH0NakJAgAAAICorG2GNvWWFytLGAfDDC1W9bYdr27bXLa3YiNTv2/XrvrYzuJ0NhjMm7bqGnYEVvaaDBXVhZt3vbGR8AWOht07DnKJR2nehq0bNzAOAS3orNxm9nrokCPnmCiNhzDVVhqLt774h1JzJyP1VzNV76sq3LznjVIP39N2cOdxE4lFp6HSULR1zx9KPQJP25s7a6zBhdsTuJxHG9q7yFccOUraNdu2lupohZom6S/qNhord+442Bw+UJ3mkDit0rCBCm/qVw1jhxTetdibCrlVzHmhZ70eaQRCzjJ0xjyYtLpQv0InqJYeifz3p6aqiqo87pbztWM+uPt9E3EyUe4KU02VsWjzCxVlXoexYmd5+M0T8T6YGgkUNYU7SgPMJAsWzO/sPE8AIA5UqtQLFxgST0lJSS6Xg2VZMtUoihKLpX19fQSuHczv7BbX+ZXJ5DffPJ9APH3xsKwAkgAAEABJREFUxZd2uy0eMwgAABBNRkZGLL/Cz50rcziu2cYFANcbqVRy8aJ9zGqJBAAAAAAAAAAAAAAgDpCABgAAAAAAAAAAAIC4QAIaAAAgRnyFSoGNq6LD+AAAAAAAAEAoJKABAABiwlfpy7ZuWqXi+15tfHzn7hd2lmYH8q2Kwoe2lWRPNPfKNffQlmItP/K34zC5MCbryvjEVHeCfbyW+Kqisp9GjXr00qtkZg4sAAAAAADMakmJiUkE4Lokk93gdLoIAMSBVCrOvO02OZEuuyOT9Si/kUXMnSSrqGT9qqyki+ZOm5evKly9Qntzzu06ge3seU+qft3a2wtzblblfCOLtbRaL499icTERK/X09/fT6Ya1zKfLxjg3Zi3+u//8e/vXMBFaLIS1fLvbLyDtjUY/vyptcf5RUOtkbp9Fd384V/OewmR5//9+tulN6izaMcXJht3gK/Vr/uH1YXybrPJelmSfefadE8bQ3JWF93c/UWnM2lYaVJ28aNlG4tXfkOXlaUm5rOC28uGfdtksg2vHDYufMXwIEWhYXAk2VGH3Tkne836FTk5y/JSPV+YrOFPhx5xri+5Wbhu/aq8dF2W1NLWeXnOyJaHjY+XO3Ow5UAkI+L0pI/oMtfHPnKt59c7srOh8Qf6vlKX/Y2cvr+822ANCXhEaRv9zeHT7VDfHdLUaBPqL/1fd2QLHBHmqy/83PEP7DQR1/kVCpO5/8QTiKdLly653e54zCAAAEA0c+fOjeVX+ORkocfjJQBwVQgEgp4e95jVsAIaAADigi4sWpF/Z3FJ0bL8O/VqAZ9L7+mljCO7rHxbsYovUC8v3ViaJ1Xpt+7YXHijurCoUKXQFxdKs0tK8xVkGpDoNmwuUZkaOlVF963Q8r2OTmOtSZqv10kjri4VqNOzFYLs0l07uN4p9FvKywoJUZWWbyvRiqXpRUX5tIDQ6fpi7p/BUo+qZDtXOsC01Ta0WbmvBu6fjGfkt2RkZf7oQYaEwVUYddglXGAbS/Uqgba0fEd44yHnSgq37NpcKBBwM1SSrw4tDRmfwZaDkYyMM6TL5JoIGbqQ7oTEz82Cv+/adLVUIAhtamQpP2S6w5saZUIDpdwgb/TPSMh8hZ87DQcWAAAAAAAgBBLQAAAQF0wn0WoFDjNRZUsdjMPLNDeYJHnZXEJOreayc8TpaKuqeGPP7r1VDQ6uuocxmcyMydzpIOEZvhgkJCRMbanHYXJI84r0qs7K/e+bvMRpqq1paHZ4orThaat5c+8r+6vaBGpaIqWlDsObb7yyv7JNoKVDusOX0lyeUqr1DQWtpROszVzDXNcb3q+uNTldI78lIysLxghyRBj+ymMNe6B+pTE8zpBzJVJ1sFNVbQ6PJ6zl0PEZEcnIOEP6GNP6lLjPb+hARZ7Q6kDfR+CPWkrCmhplQgeb2vtMWemPKn0TOny++OHnTn5gp4kpn1+4yuI3gyhFKUpRilKUAsAsQBEAAIA4YMweulBgqPXkcV/Nbt36TcVk/7adjrW7Ng3Lunk7DQc7iaSwOOx8iTZPJzDXN1tjS6MNDAxMbanXdHBzSZUir6hs87bve7bubXBGOFNCYuDvgMTXaS617vFlKB3m6je37W0Y7FlwGawgWJWM/Dak8mhBHg4t54867ESVTgRDFxvjXK/H4REUqmhawqU+rYJoLUcZgtDB9ETs8ijiPL/bapbF3J3RiwXh0x1itAkN4ivyVukF9VXGwWD988XX6kLPHXtgx/lzdK1M+fzCVRa/GUQpSlGKUpSiFABmASSgAQAgLhyMQ0BLfWnoYo9vAXQbIy3bsFXroGlBbQynq1Y8VF7SvOWhZiu5NiTZ95eXFwvMDqmA2ccMqIoe37W1SKemPela/b4ntlQ0O9oaPKVPv1nlMe772Qsj0oxec0112+YN28uJwFG91+hk6FpH6UO7dhGpoHa32WV2GJjyTXvyBFJB/d4tewxWbnBM0rLnDxbV7t2yvdI04tvDNaGVowfpIerQXow17AJp/v1by6Xp0trdRufo51qP76/M21K+R0qIp9oTUsoPGZ/nHWS0OElol8lVFxLSqAPFRdtMSreUa81S9diljHH4dHtJ+ojK5tEm1HfncKW7solUatxbEzIsEc4dc2Cv+c8RAAAAwAyk0G/ZtjGfFnjMVbu3VzSM/mZVUVhcKKg/Yugc5cjEaIs2FzpeqTTnb1xLKvca/G/o+NrirZtKaNO+bXsMzijnxVBHpb9/Y3GhWuBoMxzcV9kwufeKkeIMCUi/sbQ4W80NaG3VvooTQwOjKvrpRl3t3t0nfOdI8sq2b9Kr/cs9HG2Vu8srmwNrOwrLNt9prthV5f+tYTByj9lwcG9lbcyRhwYZrR2+avn3N5YU6qSO2n3bXvF+v/yhwsCfLTqMFTufqTJFinzKgow8mCNDcn4nZJQchVs26qp3vxi+Yio0yLA4Y7qdpkgCReFJ6XCdWrBgfmfneQIAcaBSpV64MJk9aCX6bbuLm8u3Rc9NJiUluVwOlmXJVKMoSiyW9vVN3we4TRVV8a+2Zx/csqs2tjcbfFVeoU6t1pcUNuzYGu+sMeZ3Koz9c3StxHV+ZTL5zTfPJxBPX3zxpd1ui8cMAgAARJORkRHLr/Bz58ocjsnm0hTZhTpapS8rIXvLykfPzPHzNu/ZxN9XtqvWG/XIBINYvm2zrmpnheD72/T15bu4MLgUbfnjRQKrh3bs2/Sz6ogJ7ljqaO/bvauY2beHy12WbdYzu8fq43jjDKFas2NXiadiTyWjLSkrEVRs3R4IS7tmx/aizt1bg3/gx7WzZyOp2GdwEOJxttU3dPoOc6O5e7OkYku5P4uqunOHr86eCrO2dPN9nr0Plxtiy+6GBNlWGKUdRdGO3SWOiopah8fcUGsi2sI8LtkrLSwpTTfv3fbrYK2QyKcqyMiDOTIkR17oKKnv27k9u2rLM6EXCQ0yLM5YbpUYSKWSixftY1abmhXQX/uabmBgwGhsJgAAAFPAY6zc1dY27bJms4yjrbraYfbEWJsvVev0eq21dmf5+5iZmeH6/Tni3pcmJCTga/y+EgAAgJlLtXzLRr3XI9CqBUxwQS5fW1RWWpStFpibq4+8UtVgba41NGt1pcXDH4+uKLyvrEQ/fNWwtujxrRvz0tU02bov3+MwVuyq8NwfcqS8yhR+YnCRNW3au2NPxMUgfO2d3y8tydd5yOZNdL5WwC/U1nxgEgjaKp840KbaXK6/UnFk5M5Y6ngYw74973MviLlSX1hM04Q4IwU5tohxOvJHNEXS89RM1Y6qBhNpqEzXby3USqo7nURVvLFUWrtrx/AF5h6mof7E8JXj/OyS0jxzxbbgGl4+raPNht2Ha5u99ZW1+jKdmm8Ye6u58CAX9kRoh/vYIV+nLVTzPQ1DvyE5TbUnPPqfblUPyz6HRT4lQUaO80ynLCMkpAijJBDQ+rKnS2gBc2XBdYThDYmTRLhV4miyDyEUiUT/+3//+Fe/+redO3+1efOm5ORkAgAAMFlea3NzJ5KcceZs/qDSEPMwe621Fc9sL3+xarrvJwxDrt+fo0CelAzLRF/Pr+PRMgEAAJi5BLQ6P51fu3/H7iqPfuNGvYJIdKv0EmvVrm27DfziTZv1ighnKZaXlemdvjrVpGhTmb+OqfqZsg3PVBlN7+/cWFr6MJdrDj8S8URCHI5Oh8NhjvaMcy/T2cbliesNhlqrh2k21HYy3Js6a221YeTWauGRx1Kn80RllX/DBkW2Pp0wZiZKkGOLEKc0tCnfY1EEWqnv8TkSWiX1OJ1cp7XFD5XShn1vtOmK7tNrBx+KI80uLX+jsupQxc6H8nz1VatK70v3SIu2Pr9j853ZXC2Br6Ygfblenx77k+vDg7QmRmiH1t23sWzDCjWtK3qorGxj6Vp/CES7dmNRukCg02UHogyLfGqCjBgnyYgQUtgo+Q55DP77mavmn7tIwxsWZ/itEk8TTEBziebFixf/8z8/+OKLL+Tk3LJt2xPbtz+Zn5/Hffvggz/giiadiebJNLcU5GhSeFHKRSkLF0YvHdZOyrLvPv74wys1IhKrCZwSV7JlD+767/9+/kcrszQrH35kpWrsTgMAAABcx4ZnSPE6Hi0DAADMbI62WqPJamqoNRNaTRNnw96d+487VDq1wOsR0LQ0/Ay+mit0MAIt9w+nQ+A7KzZRTvQ2VDyxufxgc7S1As42xuMwGww1ZsZjrj1uaI68R0YMkUetw88u2bpJ17ZvX61zwr0Lj9MT1pSz/mClOb98/x8qKl7Zvoo0Hzd6VWs2ltK1eysanNL0ouLBHY07DZX7927bWHL/M7XSO0uWqfh5xSX53vqqN/dVGDyFD21cpQpcU5peWFSoGkduN8pghrTTaXimrPRHe+tNx3d+v7T0+5t3n/BXM+3deNf9O2sVGzc9XCghYZFPWZCR4jwdHlLYKPmHbuT9HGl4o8V51UxwC47/+I9f0zTd2tr6zjtHKysPBh7y/vDDj95339/dcsstd9216vz5C//yLz8kEyZaWLr1l/ek2Qzlm3fWRNhJRKS+90dP3VLz5JZXT/eO0ZI6Z/Fime3om8faSawXH88pvJTlDz663Fyx+9DpbhIPIrVa1PTcE6cX//Pjz6aYKnbaewkAAAAAjGbgquxEcd1+JQAAADNZyLJjft5De7ZmN1dU1jtiOdNjrNpzvK2NjMv4TpToN+/YXJwtLdqtEyhogUNg7dy2N8LDEGOJPHIdvrZ4+9Ol5OC2nb4NGfgTCTJynE/XhDXl9VaVf6eKSAo3796sqDjQ4OUXZqcLBKT4oS3FgvR0iTnQmNdUXRF4xp+x3uwsoaVSj0LQVlkR2LujSr81Tyup9o0B8/6vt1fx8zaXTDzI+vG14zQ1GNpKi9U0n4RGLpVOSZAk1kkPGyXSFnY/qyMMb4Q4qzrj/NzBESaYgE5LS3v22V/9+c9/Hn6wp6fnjTcquBe33377Y4/9jEwCL2WhVnzB1MHX5KhFNfZJZHZ72w9sue9APE/hy7QLNfz4rZbu/vTA859y/6x7rPYlAgAA1wO+QiV1dGKni6sMwz57DM+Thny93o7HqWUAAIAZTSD1rwO2SqVSgcfhkEpVUsZwuOqEiWjpEqIdrObwCBREwKUfudde33YZKqbthKFTkldUpJbWNwc34fUtyZRw+T4y9C5yxJFoJyry7lxBW9+vboiUBHQaXnkzX7G8fvceZtW2EubF8ihPiIsW+Vh1VEVbd2yUfrBj25uBJdjRe0dU+vvXqs2HfTtlxxanVhWxKX5e6cZCc8W2D3zf1b+5c6dW6luYKxWk64KNKZZvLtPV733RMDgvHo40O11FTIw2PZsmVqeTYbgjapo0d9Jq7q17rcM7wSCzI7YTQlL40z0byd4tv671+BYWOwwOb1jkUxQkiXXSw0aJhN3P3kjDGx5nlN1f+NklW0qzGyp2Hmme0t+LpuYhhFONN2/RLRsgPEsAABAASURBVPNcn/6hTv2thQtTeJ+2Bxf9yhauXL9eryEXagynecR/0LcA+cHC3i6iltsNH5xW33mH2naiouLD9m6eeuXmH63TiriK3eYPfrPrUPvQ0uGUZY88vLL7w2O2W1beqiamEwf+cOy0b2Fx9FN4KTn6u1cuW6iWE5up7tjRd2vau0ULS7Y+ujJFJEsTi7WP7lrITUzvhZqXfv1qk1e98pEHF5s/aBLdumyhqPu04e3KY8H10SLNsjvu1Bdo5eSCqdZw9ESdeSi7LtKsvP9bek0Kv9v8ybG3j9a2d5NRTxEtXHn/Oq6+yNtlqjta8W4T1kYDAFxlfFXR9+8XvL+nalKPeeOr9BtLpdW7B1vhvi/bqm/YWV4V4/a9UxNGhEji5qpdaByuDDtD67+zoThPTWr3bKvwve9SFD5UpjbsrJzYe7CQzsbQ9ymbUK6l5d/fXKz1MLUVL1Y2j3+JQyCSPx1w3Pad4QMyI0TLk15vx69mywAAADOGR6rf/EKJWiUwf7DzeKdVamhTb3mxsoRxMMyV9dGmmipj0eYXKsq8DmPFznJDRXXh5l1vbCR8gaNh946DwVretuPVbZvL9lZsZOr37dpl6Aw7EvFEVX7pls26Wqa+wRBxF15aISEms4NO1xKrkQkeVN25bftGHS2haUH+njeKa/buqAiLPJY62sKSFVxmVL/1RT13oK1qF1cncu+IalnJ/Xpm1xvRRjI8TlOkpvjZ6zfqHZXbqwKLd72dDbWB7KqKLi7JDjRlba4nG7fuv3OzR0DMR3bWdDqtb+7Tb9u6/72tviiP7Nzd4LW2VdTmBRr3mD/Y/b5pokFWRWonlLPWF8Dm/W9wo+a7B2qs3GcKIZEH6kxBkCTKpIcIGyXi21KF1m9+pUStkDoMviNhQZKIcYbfKrtOWAmtLtSv0AmqpUemdn/oBIrik/GrqjoUvgJ6SGAFdHHxvWSCZMu37tpAXn7yg4LHf5xy6LFfHjX7s8P3/uLXG9TthkMGc8oy/bIcte3tx7ZUeO999tl7ew2HTPPuXa02HT3aqV233Lt/y5PHumQ5d69bphHJtfplMsOTP/pt02Cql6e699nd/6zuaqqp+cgsunX1yoXdhx577DUuRRzlFJ569c9//T15zYFDNWbCJcFXL7rw0mO/NJCCdatzUuQL9XqN7ZMTTRe8vb1dnx89dIKr871dz34r5cInJ47VdKXo775T0/XST39x1Ey4dp4tFX/y9rEmr+ZO7mRy9ImfvFDn22KEp7n3F89uUJu53plSFq9bmRMMiRfllGD94GhwXbAdevLJ1+K0C8hstWDB/M7O8wQA4kClSr1w4ZKqsHiVTsB9cm1+v6p2qteVJiUluVwOlmUD347+V+HjKqUoSiyW9vXNyS4qXpHuqX+/utYUnrnj+3snVRUWdu7e/IYjf1U+3yNQC9oM7zdwaWPJsHM9Kn3xCrWUOBjuzUH9+9x/yIeXkuzihzaWFi0TmGrqG6or9h33FH5nY5HW01Cx96A/YcjXcqenE+PxscPY10y4yty3bcerqgPvF/iKvFXFRXmKztojh6u59vjDK3AnDwvbkT4ykuqQ7OfIpkj2naukzYfrHbpVekF9tVFatFYn4D5iZ7iWuThHu64ne/QLXZ35TZIPj9CjWh4y7KriHdvVb27Z61uToir+VbneZGh2mAO9GzmMkpFDwb3Zi97ZA2bdxpF9D5mykAkdMTKS7DXBQa6pqg5GWTjyxuOH3ACKoqd3FVZvKg9sYDda2KEzGHZrDRsQLodenO+ormrwcA3qmOqq8ae24zq/Mplcrb7au9pdb8zmTrvdFo8ZRClKUYpSlKI0WmlGRkYsv8LPnStzOEZ9c6K9b+f27Kotzxiu2vPXZi7FnTv2lHTu3Bxp/49pA0FeU1Kp5OJF+5jVJvgQwvgSaRdr+OZP2i+Y6sxedUHgYYC8lAK9ptuwu/z5yqMHXniuos42NGW9XZ8cffftD05fMNcePXrUYCZytYxHiL3p3VdfeuGlP9SYI0yu19Z04LnnXzt04IXy35ywpeTk+B9oGOUUvlwzj5iPHXj7w5qaD1995pFv/+NTx8y9vebaAy+9/FKFweyynX775d/+9oWXXqo8YR5chnyh7tXnXjhwtPK35S8YbBp9ge8CrqY3yx/7xfMH3j12iLvu0QuihVo5L9C7xf7ePfl85SGu6Mnf1thStP6QIp/iW5F9ZTR2Pv+uTV2wTD1NnpoIAOAjKdyya3OhQJBdUlqSrybxNvoavQmU8rOLSvRSxpFdVr6tWBX6Ya1CH+idNl0tFQiIQL28dGNpnlSl37pjc6Fk5LkSte/5Ewp9caGUG4x8xcjSAaattqHNyn01cP9kiNfRaaw1SfP1Oik/cKHyMt8wbizfUaIdI4xAZeJRlWzfFqgs0W3YXKIyNXSqiu5boeWHVBgZNj8kkhAjmxJL04uK8mkBodO5XCQt4L7dWKpXCbJLd+3ghmvU6w6MfqHY52gypSERhgx7GIE6PVsx2Ltgd4iqtJzrTuhQjNpZT0jfQ2YkZEJDDA6ytnTwZgi58UYGdmNe2Qv7y0uWrd9xsOqNbXrF6GGHzOCokXg9hLuVi7QKXUmpXuqJ8td74zHl8zsAcTb5OUIpSlGKUpSidAKlcJXxaamnvvLw9M6ZIsgZIS5bcCQkkMkQqQu04i6Dydbbzavr4t+boxWdqOvmi+aJSLfNFZirXlt3lEmLdRsKb3dwa2lvt62bLJTz+dHP7TadqOm688Fnn8356LS5y/RpTc2wnTOite+123qDZx87VKk2d/eSXru5nZ+z/N6V2nl8Hi9loYjPD16XL5IP7535w51PfhhoJ/IpI0fDa7vQTQrlyD8DwHQiVUsdhjffeMXhyN4imIIM1VXHNDeYtIXZXGaOVnNpuhG7YfCl9MjeCZyOtqqKN6pJW7HOEXIunyEexmTiPho2d0pVXDJvRGmCtaG2pqFYTze8Xx14P2KqrZHmB/9SavBCexv27g0PMSQM7lsuWUi02QKuZS0Xs8nrcZgc0vuL9B5D5f73TUSdP7ICGR6219ocEskII5vy0rrQ8raag3tfYVZpt3DDNep1EyprR7vQ1RHSnZHDHqH6sN5JBoedMWu3cdNYM6JmyCyEdXbEIPO1IypL6unRf2oCYZhXqHzXJb6wh88gX6obHpi3cu/DG9qe3pV3ZNOuWt8i9JJRwo7Wx8iRWOs/MJbev2KFNt1hqDRPx7fRA9fT8wCvyVcCAAAwc5kObt1IIBbe5oPlzWSaQ5AzwgQT0BcuXKBpRbTSlJSU8+cnvLMBT75woVquWbd190ru17h58nmiW9SiutPkWupueu2xTZ/qVy5flrP8znXrN3QceuynLzfFut+FveloZZPvhWzZI7/80eLupiaTLdZf1mI9Bds/A8B043F4BIUqmpZwiU5rYAUlX6KiBcwMecibbv2mYrJ/207H2l2bBKNXvVLs7TQc7CT8vLJRzuVHa3n4g0vCTlLk+fZJqKodZVdoX1sOc/Wbw5+V7DUd3FxSpcgrKtu87fuebe+PrCApHB42GXr8dcRIRja19bDvfN8luYy6J2wN7OjXjXChq35vhHRnb8Snv0hiaslfc/hQjNXZEd8Or8zXqkfWCCOIXBS88bQ6ErPwsKMbutzQgDiN1Q3S7aWFbfvenJb5Z5/A+il8jd9XAAAAAIAYTTABbTabFy5cGK100aKFHR0dZILkCxendDcd+t0fPu32/Sp294PrcxbKeacv9Hp7CY9PgguV+TxydXWb646+WnfUt1vz2mefvXflwjeb6sa34zJPvWzdrby63zyzs8a3N4po4Q9ycgqCZd5A7waXYcuyVt650GZ4t4kf5RTvyNHg8X3PTUQSGgCmE+vx/ZV5W8r3SLlcdLU/u6VYse3NcvXe+zdWTKMnz0XFtDHSsg1btQ6aFtSGFnqZtmZSuqVca5aqw0tHPze8lGvNJC17/mBR7d4tO2rSN+/aWqRT0550rX7fE48fr2bKN+3KJlKpcW+Nd9QwvOYaA1d5T55AKqjfu2WPweqVZN9fXl4sMDukAmYf4zQzIyrUR+jXUCTbK00hGxAPb8rDOGodpQ/t2kWkgtrdXA4ynUSvHHpdLrCQC139e2NkhAOqoseHD/uWimZHW4On9Ok3qzzGfT97YUR6lhvn6rbNG7aXE4Gjeq/RydDDh8JldozR2eHfHh45ZfWj3le+B1zn37+1XJourd1tDM+YhwY2eunIsENmMPwO9w4fkG2VJuNxg6c4z1DPTM8fZmRIAQAAAACmjwk+hHD58r/52c+2btq02WRqDynKzMx47rn/GOURhWOQFW7990dEB7aUH+3yJVRTlj/+7z8g+7c8c8y7bOvurTmmiudeNtjU+g0/KM3pDj6E8OllNU/8wqDe/NSddc/srMvZtmv158/85NV230pqEZ8/747vPZjTVfHy26buXpv58/auXt9DCHetM/960/O+FDJv4Xf//allTU9ueem0NyXyKd7F3KU1NeWP+R4YmLLs4ad+tLDmycdfDTzyzxfhw/IPXqho6ia9LrOppaubt/B7u55a9umTP315xFMBZcsf//82zzP88omX6uy8lGUbtvxotejYY9x1uUqigkd2bbvV9vZvXj5qFi0ufeR7Oebf/OSXJ7zRTiH++hfe/s1rR83yZd97eIP29M6f/Lpm7F2/4Qo8hBAgfoIPIcwr1KnV+pLChh1bK6c6sRjyELMpNPgQwj4C1w7mN5yq+Ffbsw9u8e2nce35Hm+oN2zZ8cHEVq3HaX5v8JElJibw/QjEh9evv3/g0iX7pUuXCAAAwFUxZQ8hBICpE+NDCCe4AvrEif+5557V27dv+8Uvnvriiy+Hjmu1Gu5gQ0PDBLPPXCI2LUcjsh37PLh/MrGZmsy8dTka2bHaT/7w5icLH9nw9OINxGv6pMnmlY/akGbdj365Li34XdqGLYu5f5he/eFPKtvHf0rT24dMT33v6ddX+0tcn7/9ay43HazXVXfog87Hv7Xl6W9x35jf/okvkR25fXvNq/sLn3r0F6+vdrm83e117Tbv0LbN3XWv7npJvOXBbbt9zXjNht+8WtPFvYp2ir++fLD+hU/2P/8yss8AML3wpWqdXq+11u4sf38mLHkGmOYcbdXVDvP02FCdL/U0VFbUTqv9dLjcs1gsttns/teSgYEB5KDjgUs99/T0XLrk+8VeIhFzX5GDBgAAAIDRTXAFNEcoFP7sZ1u+9rWvvfPO0WPHPuTxqL/927/lstKNjY2/+tUujydOvx+JUjSaeaTLt5CZzEw8mVotcpk77eEd4KWs/PHPV5N3X/rNuyOWTo9yCkwCVkADxI9/BTRD4gkrZGc3zO/sNoXzm5CQcOONN8pkcq/XY7NdYlnfzFJUEk3fyL1ZJTDV3G43w3w1NM5y+Q1ffvklAQAAiD+sgAaYhmJcAZ2UmJhEJoT7neH4cYPT6VwQIhZdAAAQAElEQVSxYsUDD3xn9erVAoHwzTffeuWV/fH8pa63297VZe/uJzNWv9thd7ojdqC/29xq4t/+yKZVfTV/anH0x3AKTIJMdoPT6SIAEAdSqbi7+zKJp8TERC7f1N8/9f9y5Frm8wXYQ/bawvzOblM1v/Pn37x8uV6hoLlEdHe3y+3m2hwItC8SzeHS3ASmGvc+//LlnqFxTk4WYgU0AABcHXPnzo3lV3juv00eTyx/pUXJMpauvutvM8mXpq5ZmHGhZKkpYtZ1maUUt6wpuWPhHFfXeTsySzDlBAJBT497zGoT3IJjyLvvvsf9Lz1dy/0iF74fNIwLL2X5oz8u0YrMhrc/vYDFzgAAAADRcdnnhQuz33vv3d5e3y+ZN9wg4z76cjh8v5cGtoYYnuBOSEiI+KnD9XN86lpOHD7ODoeDAAAAzETijKKiW1wf/b/6s66p/5u7EJR4wS0Z5OynZ+1jXkq44G/uzjz/QfWZya2Wky1a/XffsFUfOE8Iazd//BG15Jt3f9P6+h/PYBEeXBuTTUAHtLWZCExab9eJ5x87QQAAYPyi5UomXxoffIVK6uicVjvoTmvTYH6v1ZRdF7fKBGawoOAbLpezuvpdrjRw5NIlO/dSLvc9hDAxMZHH4w2dxdUZSkYPb+16OD7lLSclJQoEghtv5PX3Dzgcl+x2O4nnTyhKUYpSlKIUpfFCURRxdZw9c/5qpGTFmfnfoKyfx5CApsTKVIVrssk6irV+fPjAeat/XSprP3/2bIdrWebUpAABJgJ3HwAAzAajv0+dQKmk8KHyjdkexuHxdBoq9lVP6XMU+Sp92VZ9w87yqk6koGMy5fM7XuOZMq7uxlJp9e6qKbhphl9XUfhQmdqws7J59t00453BRYuyPR53S8vpkFIuGepyuWQymVwuH56BHV7nensdj5aTkpIcDgc32kO7eMfvJxSlKEUpSlGK0nhhWTeXhPalxVgizli9ehHrEqamUvammj81nHURxTfW/m0aV6IQulobPvrLp+fdRLzgG9+89RYF5T7f/D8n/mLmEtfiBX9TlCN0U2LWcp5SpjrrP/gfa+rIpszUouJvfXOBgpaRb/0gw+02f/R/DzdYw/LQlCzjG8uXLJKxVpc4eCj8chH4IyduoUJGWblqDWYXG/FESkgRNxv3pd4A0Ux8D2iAmQ57QAPEzyzYA1q8aO1aadVjT736ruETk61Pkbfmf2X1nbYk5fyvdVmeloupd69fkZOzLC/V84XJtzhVkl1Usn5VVtJFc6fNK8leEyx1fGGyeQlfkbf67//x7+9cILCdNVmJavl3Nt5B2xoMf/7U6uUSjOuWzTH7DuvXrZhjbrESrX7dP6wulHdzB+M7htNZ/PeAFg+fMl+mt3Dd+lV56bosqaWt8/Kc4aX8EVNGRp1fT3rxo2Ubi1d+Q5eVpSbmJu7mGXl9ycjrDhd6M5wVFA6/rjz/79ffLr1BnUUH7zpf0KtXaG/OuV3HXfq8s2/0+3A6mcz8SiSS/PyCP//5f6K1LBQK+XzfQ7YD7U/ma+B34Ml8nXwM0/Orh/sEwO2Ox08oAABANFO2BzQlS52vVs/PyrzB/mnjGQdLKKn29uWLLn/8znsNF9O+uWqh/fPPXeKvL/8bxRcfvP1hC8lftVxq/vSienVJweUT//e9T+03f/PudMfnLRe9c9RLl9BnjrcqFqvMJ9pSb/+au+2cdMmIpowNnzfW1Z1Nnp/adXj/Gx+e+vz85Qj/+RRnrf27b7hOHKz+3Hvz1xfNMTc0uhasCbtchK74I3fVvvNeoyP9m6s01k9b2IwIJ/b3U6pFX7uRdREh3+tyefFfcJgyMe4BnUgAAAAgEoG6cEXRnUWF2Qo+cTAebelD69duKCskjNkrTS/aWKpXCbSl5TtKtHw+l/bTSxlHdln5tmIVf7A0u3TXDu5biW7D5hKVqaFTVXTfCi3f6+g01pqk+XqdlMuReYk0r6QkTyFJX1Gip4lHod9Szl3DoyrZvo1rmUB8hEyZpHDLrs2FAkF2SWlJvjq0dOSUkVHnd4Bpq21os3JfDdw/mTGuO7Iw9GYIuS53S9LpWsHgXef7Xr28dGNpnlSl37pjc6Fk9PuQzBaLFy/5n/8xjFlt8rnjAT8uxzqZr1MVyTT8CgAAMENRsgW3Ft29+psLiNU8tP0z6zrfara6rObm86xYIfRtF8BaW8+Y7a7zn5/4nyYrmyRWyFiujj1QRxao46vGsm42IGpTY4YkVohZc6Dxdqub9R+JfLkwQ5drtRKZQiyIfCJr7zhPFt25dvXfLlkgxmYIcPUhAQ0AADA2b6dhX5Vg4+b82ooq/w4InraaN/e+sr/SKNDSAsI0N5gkedm0QKpWc98Olla1CbhvPQ6TQ5pXpFd1Vu5/3+QlTlNtTUOzwxNomak3MGq9TpeXRxpq2oiUVksFUq2vKdrXMsTJiCmTSNVSh+HNN3xT5vB4SOiEjpyyUefXZW3m6poZU8P71bUmp3fU64bO78ibwRt+XXPNwTeG7jofp6OtquKNPbv3VjU4yOj3IZkV0tLme73eS5cujV6tr6+PS5JO/usks89TEsP0/EoAAABmLNba8MeX/vO5Fz5wLfhGxGQsNXK7Wvf5T//yubVv1DrRUFO08+2E2wmeSMkW5S+wH9773P+3//CnduzEAVcfEtAAAACRecy1x6s/qK5t9u12wKfzC6VmoycvP13iLw3m83z/4OvWbyoWnNi988VqsyO8Ha/p4OaS72yraNaWbft+niS0lGmuZdJLSvSChto2X7rSYa5+cdvWH20s/s6uWieB+Bg5ZV6PwyPQqmhaxSV2BYIxJjREtPmNlPEd61YJvRlCDd11I+8M7vORg9XNnnGFPUPl5n69qemvsdSckr0mJp+DnqpIpuFXAACAmY/1/89PKJYJuWytUCam3G53hBQt62YpmVhIhupEbTVSUz3+hx5GD2SocbE4kBOP/XIxxYntn+Eaw7p7AACAiATqtTsOrvAQh6lix7bj6k0lpGLbNmdp+UPfqd96mAik+fdvLZemS2t3G52MlJGWbdiqddC0oDasIUn2/eXlxQKzQypg9jEDqqLHd20t0qlpT7pWv++JLRVt9bWOrdvpigqzl3jNNQamfNOePIFUUL93yx6DFU8pjAumbcSUWY/vr8zbUr5Hyn3uUO0JKeWHTNnzI7O7I+fX40sjt5mkZc8fLKrdu2V75cgnEYZcN5SXGXYzcNfdMvK6wbtOp27b3eYcs1OzT1ra/K+++srpHOODGS472tfXl5iYyOVJJ/mVSyInJCRM5uvkY5iuXwkAAMDM5ksIs8PysuLs1RuWcJlb16d//NzOfRtSnbV++qf6jLX/+C/f5F6fr+HqRE/phjTlO/lM0/m1a3/wQ9Z15k8Hjn4eupM1a//8Y/M31j74L8vtdjdF3OO73Ah9UU7kekoJCcC1kkBR2F8SrlMLFszv7DxPACAOVKrUCxcYEk9JSUkul4ONw2f53HtRsVjKJbBGqaMq/tX27INbsEQ5bq76/PJVeYU6tVpfUtiwY2tI1him3MTmd+XKosbGvzJM1yh1uPmVSmVz5uAXrPi6fNntcNhZrKYCAICrKCMjI5Zf4efOlTkcMbxJp2SL1n577QL2TPWBd85n/P3fqT968/+eGfsZh2O1qvjG/VPU1FShFHlrv3VnBvn8j/9dNX2igllDKpVcvGgfsxpWQAMAAIybo6262mH2EJgt+FK1Tq/XWmt3lr+P7PO0JJPJeDze6NnnIbNvBTTXIy5rP33aIQAAADMda//8j/utagVld/XN6k+uWfvZjw6/9Ser2R7zNh4AUw4roOH6hRXQAPEz61dAQ7xhfme3CcxvQcE3HI5LZ860jl4tsAKaz5+aNRZcBplMTrTn9XFxpqWltbe3E/9o3HTTTZcuXXI4psXm3SKRqLu7e/Q6Xi+LFdAAAHCVTfEKaACYCjGugMb6BQAAmA1GzxNNphSmA8zv7BbLDKanZ5hMbTGeOzAo/DWXXc3MzORyvqPUGXrdPyjwRMEJvI7Wfm9vLxdDenq6UCicP39+T09PXl4eTdOjxxPxNZfILioqysnJ4V5//etf516rVKqhOuNtTSaT3XbbbVKpdPT6scwCSlGKUpSiFKVTXgoAMxS24AAAgNlgIMoyw8mXwnSA+Z3dxpzBm29eYDZ39Ed68l3Ec/ujPyPP39rNKSkpTU1NNpuNjGrod+DhVxnX64HoK6AZhtFqtVyoZrNZLBZ/9NFHixcvPn9+3H+b1dfX99lnn3V0dHCv6+rquHw0GXUERvfVV1+dOHFizBXQIeL3E4pSlKIUpShFKQDMAkhAAwAAAMC0lpY2v6XldOz1BwZ3YQ58O/x1oFQoFC5ZsoTL/J4+fTqwj0TE+qO0M8nXEonkG9/4Bvf6xhtv5JLFPT09fD6fS/smJydfvnx5XG1euHBhqF/cV+7bkP6OqzVuZLi0eGtrKxfS6PUBAAAAAGKEBDQAAAAATF9cZpamU/7nfwyxnzLK+t+hbTHIsB02olUOz1yP93W0dO3w3TluuukmLhVusViGnvJHxiPQztC25oGLTngFdOBErrWxWsA+fgAAAAAQKySgAQAAAGD6uvnmBV98cXY8Z5BRVvgGMr9ut/uvf/1rYAuOUVYEDyVhp3wd9KVLl06dOiUSiXQ6HZd99nfzZi4HzR0fb5spKSnc6y+//DJwnKZp7gX3baDOeFvjRqalpSWw/HmU+gQAAAAAIGZIQAMAAADA9JWaqjQaPx3XKaOvgG5vb+dyrENLhkcRvz2gvV4v48elesViMZd3LigoaGtrixZ5IJVMovSIy2LL5fL6+vr8/PzU1NTPPvtsAu0EcO0sW7bso48+sttHe5p5UhJWQAMAAABArJCABgAAAIBpSiQSyWSyr776alxnjbJPscPhMBqNJOZ2hq8jntjX0S9x/vz5xMTE+fPn/+Uvf+GSv9zraJnxaE2d9Qu8rqurIzF0apTSixcvHj9+fLwPIQQAAAAAGAUS0AAAAAAwTd18s2Youxq7Ce+AHGL40wgn9jWWR/Zx0ZpMJu4FwzDR6oy5cjlGsbTjdDoJAAAAAMDUQQIaAAAAAKYppVJ56lQtGadY0r5XxxRGMlVNTZ/BAQAAAIDrBLZvAwAAAIDp6MYbb0xMTHQ6HWT8JrlymQyuXw48tHDCX6cqkmn4FQAAYHri/gtMAOBqifEnDiugAQBgNhh9r9XJlMJ0gPmd3aLNkUaTbjK1TWB++/r6hm+mzL1mWTZwJOT40JGIx7kMMtf+0IYegdfDv455fPT2r8LxKWl5qEdDR2KZBZSiFKUoRSlKp7w0Fn19/RRFcf/pJwAQZ9zPGvcTF1NNAgAAMPON/j51MqUwHWB+Z7doc6RSqT/55OOJze9QzpSrEMirBo4M3x56+JFox4e3H20V8OjHJ3bdqTo+hS0P5dbDt9iO308oSlGKUpSiFKXj1dPj+tYAmQAAEABJREFUmTNHyL1ADhogfrh3hlz2WSDgd3f3xFIfCWgAAAAAmHa02vRz5zon9lvogP9Re0MZ4cBrfJ3kVy7vnJiYODBFj0MEAACIk97e3suXB5KThcnJgoQEbDwLEBcDA/19ff3d3Zd7e2P6pAcJaAAAAACYdrKyFtbUnCQTEr54eWKGZ7En9nXyMQRMVdp3ku0E9hghAAAA0xuXEevtdREAmDbwWRAAAAAATC8KheLy5ct2u51MyCSzxtPw61T1a2rbAQAAAACIBVZAAwAAAMD0csstuc3NRjIhCQkksEo35CtN0wUFBTwej0Bsent76+rqGIaJNJ4EAAAAACBGSEADAAAAwDSSkjKPy3JeuHCeTFTEtbpYwDsBU7iLCAAAAABct5CABgAAAIBpZNGi7MbGBjIJEXPNXV1dR48eJQAAAAAAcHVhD2gAAAAAmC6ys3WXLtm/+uorMgnXaqfm6+crAAAAAEDskIAGAAAAgGlBJBKp1Wl//euklj8HIEeMHDQAAAAATBNIQAMAwAyTmJh4ww0SgYA//GDCqI/EGm8p17hUKuEuROCqw/zObqPML5d9XrXq7urq90JOmczsw9UxtT+hKEUpSlGKUpQCwCyTlJiYRACuSzLZDU6niwBAHEil4u7uyyQ+brxR7nJddrs9LNvb399PphqXIBsYSBgYGJDLb7h8uYfA1YX5nd2izW9u7tcXLcp+550qMjnc/AqFwp6e4L9/sFZ3ag0lBZKT53g87nj8hAIAAEQzd+7cmH6Fp8TKm29S0oobb5x74w1z+t0ON0uuAUqcWbRmCf/8F1b3dPjvpThz+dp7FtOU5OY0/oVO+zUZkvGgZMoUyu3y9k+yzrVFybJXrlmc2PHFxWkc5FWChxACAMBMIhAIvF5vT487KSn4AapKpeYEXvf2sjye7z9tfX39SUmJ/iO9PB5v6PShb4dVCJ7CMZvNnZ3mwGvuEkIhdzWBx+MhcLVgfme3iPN7yy253KyZTG0ffPA+mWpcwhQ56KmCJWkAADAziDPvWr+cmFoZNyGsndjO269JBpplXRazxTXOa4szSh5Y2v5WRZ2dTCmKYpm6Yx10Zhrbft5Npj1hauGaO5xHKk5a2EnVGdNUDXjkdli363yHxcVenRswXjfP1EACGgAAZrbu7u6urq7A6/7+/sC+CkMvhhKRgxX6An/6E14z0BSBaQbzO7txk1Jb+9GlS/b4pYkDaVOkoScDqWcAAJhZWGd77XtHW4etlhYqF+VmpsmJ3dLebOxwsZGOUGJ1pk5DE6bdeMZ/IPKJ4YSKDF2WUujuaDGetbp9y14zly7JknMJN1cH468hVudmUabGsy4i1uRq2JamDleElsWaJbcXZM+nFfKVa5Uua0vtx612NjyqmEIKrcO6naw8K41ydZiYK/nniF0ewRe5uKdHQku47jV32Flf73I1FEvkYsK0NLf6OhzWTvhZES/nqybvYYU0N3bG5kAAlEyty0oTut1CQpxRggyvM/akRJoFGz32gHMjqVMm+/L3NkJLekzGM1xrIY1HnDjf6uelt2rlxGmxjRzwNDnLtPjbCY8z4uViGbcYb55wsfR3SmALDrh+YQsOgPiJ3xYcfX19EomYSzty/wv8Cb/b7bbbbYH/cWmsaC8Gv700SgWuKeL/E36K4guFApFoDv4tcZVhfme3iPMbmJepEtiC4/Lly4G1z0NfyWAWFV8n8HX4SAa+YgsOAAC4+mLdgkOozM27ud/RzZfOvUHk34FDmLHmgbtvcnze5krJXazqNpkuJoYfWbD6u3en2c6ep7K/uTLtq0/P+LKm4Sd6wy4nzlj3wD03uc4yiV9bWZR+6fOWi27ST7zuSx7+oiVZl5uNFnfijV+/a8W8jgaTi8wtXP034i8++4LVhrfcT/rZvjkqtcjS8HFL50XGbndTYVFRMYQUHjY/LEjuLOGCtd8tVtlMXONFKzXMpy3hG3NQN35tzf+67UbbuS4qo6go02b8/CKl/uZ9xTrq3Bd2xZK7bpvT0dTBzg8J0nVD2Fn+y4VXW/e/CuVfnbsoyb57pfYrrho/4+++e8+8r8x2oVaXkWxp/Gt443ZhWB1X/9iT4uX6EjoL7U42fMBHjomJ1d55l8baLlh86w3nGJW+YOD0Z93zQxq3esMmjhtJX1Bu7xydfpH700/P+fZh8Y1AsdZttiRmFq3O9rZ8foEKidPkXRB2uUs3jT1uMd484Sno0Ek5G6G/F7xkKmAFNAAAzDAXL9rFYhGPR7nd8VrQKhJxn/pS3IUIXHWY39ntKsxvQGDJM77G7ysAAMC0RSXLtJmZEjdhbcRmsbuJ2826KVuP0/LxgTqrLzkoDD1CpWWmUUwd43SSswyVn0VT7R1cvbATw7nOVP7n72TKVFpG2ahsWkK1utz2jrN2IiS6W+dHjTFCy6z9fDsrtt1GW0xnWv1vVCNExcQQUoTGw4NkKTqTZpuOnKy3EIs4657BLodibe0nT33cwXZwdbRyqtVG2J7zdcc/rrNSDFWkEQq5dkKC5JoJPct/ufBq7kA1YpGn3cFF1U5p5G4upI8tlIXOusM3AuFnkdA6sU1KpK5FGvCRY5JUy42my8YwNidhGOLO4n6LCG/cEtpOYBasHWddVE6PNvg91xcl1/ixjy1sfUurguI+TGFDmkpiwi4njGHcuN7FdPOEzW/Y8EbqLxcmmQJIQAMAwAzT39/vcDiH9pCNB4/Hi8fTXSuY39ntKsxvwPDdn6/n1/FuGQAAYBoK3YKDNR97/Z3c229duSIzjW1+66U/NrtCj7QTikqmNVlc/pG4W+tbAjs7uMNPDL0WpcgvWb8kmbEwrFCeTFlIbGJo2dd4eFSxnBhWp1UYIUguIUixbK9/gFiW8h+ImGkMHByqE3jNHWQ7Th7u4JL5aWFBJoefxUboy1A1/x7J1IiQgueHn0VJQutEGLeJTUrkMYlL4y7L+RibimXcSIwnxlKHJnGCBDQAAAAAzB59ff3JyWIC8cQNMgEAAJgpKDEtcRnf+0PdMfVdG+7R0sJmNxVypNVpddnIqfeOtrOyzII0NrC0OPxEV+jWYeKbMuSM4fXKz13ijHVKfcTrsz0ullLIhMRCZGKqx9LDRm2Z5f6PGlp1yvaERRVDSOF1LJIIQXJRuYUKOUWsREYL3UxPlD2ChVzM3D+5OiwT6Wl6EYJMjnBWxGrhAxUMiRLLhJQz0lksFVonXMRJiTALEQZ87DGJPOMj24mIZV1ssPHUpWvy3cerv4zp5hl73CLGEOHEsRvvI3GDBDQAAAAAAAAAAMwSlDxn/YMaLi/b22Ote/v3J22yzDWlK2g3l/8T9jQfYNyEUoccYV3NxzvuW/PwJh531rkTb9UFGgo7MYzr3BmbXr/+H3JIcrIwmdjCKvjSfvbmP7fnr394092E2GoPttgJEUZp2X2+hZGtf3DTUqbdcOBwozUsqhhCCq/jckYIkrU2HW/3NV5MWJvxnWPWKJlTnrzw24/cLRcTy4lTDEuEYR20Rhq6kLOiVQtpyt5cx3x3/Q83OW12lkc6Ip0VXifWSQmfhQgDHjImfdT82BoPacfOUsolJeuW3CRR0GL3gz9cYqk9+Nap1jomp/jhTVyWuMf4zlsudsybJ8ZxIxFjiGXAY2980hIoik8ArksLFszv7DxPACAOVKrUCxcYEk9JSUkul4Nlp2RDqhG4D43FYmlfXxw//oUxYX5nt3jPr8czNQ9LgWgEAn6cZhAAACCajIyMmfQrvHDBXQ/cQd6reK9jKp+3fJVRylsfWCM+9nr1uDoxsbNgdsMKaAAAmA1G35l0MqUwHWB+ZzfM70wXvxlEKUpRilKUonTGCSx9pSmWqXvn7Zmegu1xMRZ3z3g/cZ7YWTCrJSUmxv0hMADTk0x2g9PpIgAQB1KpuLv7MomnxMREr9fT3z/1+5ByLfP5gpn+xnemw/zObvGe35AV7kKFOu1GvttxmR36dt4c4nK5A9cXypQyyu1NnMMnXjZSSJRQzGe9bMzHfU2q05RS4na4R/3VK8ZqMaHEirl8b79UpZzjvXyZkk6g5YSkpITIPxkJiYkjSygqKU4zCAAAEM3cuXNnxK/w/a5zn/3l41OnPvmswzHTc7D97q7W1vOXx/kf/ImdBbMbVkADAAAAwCwmVM6nqR7q63k39SZ6LUazcL6cZYgu032q2c4SYVrBEpr5Yv7iJTn0xbpjf2rsUWhoytZhZukFtJC9fJlI5ykltqY6m4w77vFSojnE3nHWJlRr5vuOn2oP/01YKNcqKUury00omdrf2llrhPVPodUs7WddE/w9lZKlZerS2PMXewf6JDplr4UOthwcgexsZTLb7fIKhJ5zLWdd8kU6JbEYP7cEK3AJZl/6mfQTXlJfb58v1ZzEoxK4BHNf/0ASxacGWGxqAgAAAAATlUgAAAAAAGYz1u0ishQ+w/CUShFFL1qqE9uYwOJgN9N+XkjfcKm1oa72o0YLK6ZpCc0lc2+UKyUsm/r1ryncNi5Nm+Q/npWjS2UZOxHeoJwv8R8fJFTn5qoHn8rD9jDO5LScpZobZNocnVaeTMVUbRILQ1h7Rzvj7u06c55IiM3mHmxZ7CukhGKJUCi8IT1TdtHEZcLFSiXPPxTiwMmJPJ5AwEtKIInc/5Ohhc4DA/410f6XBH8yAAAAAAAThgQ0AAAAAMwS/f39iYkJoUeFqRrNHG/vjTpdKnGzLPP5yWMfNQfXJAvlShklUaSIE4V0Gi0WyWkFLfGniFmO10vdpNOp5ZQweLyPZV1Wi7WbpdT+44OXcJsbG81XEtJUslhI3G7WbTNbnGKlXBhLNYl44iloIZ06X6nU3X5XLuV0D2t5WJWBXiLNyM1WCnvdJDUwFMFB6+31eHq93v6BgT52aPOSgeCXAf866P6RGWhukLH/BgAAAADEKIGi+ATgurRgwfyZ9AhdgBlFpUq9cIEh8ZSUlORyObj8EJlqFEWJxdKQPWThKsP8zm7xm1/OjTcqLl/GM9fja84cwVdffUUAAACuooyMjDj8Ck/JlAqWOe+arrs1izOX31WoYIxmQjGnTp3FWxyYobACGgAAAABmD7e7JykJb3HjiBvenh78/gsAALOCMLVwzapceto+II2iWKbuWL1bLHRZzuO/vjBz4SGEAAAAADB7dHd3z517Y0+Ph0B88Pm8ixcdBAAAYLqixOpMXZqcZVqMZwJ7bgkVGbospdDd0WIMPhmYkql1WWlCt1tIiJNErhO9cQ1NmHbjmQ4XS8kyCrJIS90ZOxFrcrMpU32rnQ2pEyEksTo3izI1nnX5ztKwLU0droiRs24nK89Ko1wdJsYdMQACMBNgeQgAAAAAzCoXL36VnCzAOugpxw0pN7Dc8BIAAIBpS7jgrgfuXSxn3eKc9T/4u1wZl+3NWPPte3QSNytesn7D2kyx78i6B+7NFrJElpEWeKRDeJ2ojd+TK3S5hDlrHijSCAnrsrmslLUAABAASURBVFO6VXflKhS61WtyKReXEQ6rEx4SJdEUFGRK/BfOKsjXSKhYIxcuWPPAvYHG1z2wWiMkADMCVkADAAAAwGzDJUlFIlFysu/XstAn6MH4BR7t6PG4sfYZAACmOYrOVLJNR459bGHrW1oVlIsQ9kzlf/5OpkylZZSNyqYlVDulkbubjpz82EJZ6Kw7fKe5Quu0RlpczDWeRjF1jNNJzjJUfhZNtXdYT733cda3S/+R2Gvf4i5KKGVonQ4SFlLyhCPPpLk6J+stxCLOuscfABZBwwyABDQAAMwGCQkJAwMD8SiF6QDzO7vFaX67/RL9CExOv1+00vj9hKIUpShFKUpROl5cnoti2V7fS9Zl8T20kFLkl6xfksxYGFYoT6YsI+qQQPo2vE6UxikqmdZkcVlg4m6tb/Fv3sHaOkw9RStIc4eNjViHkoSFNAWRsyxL+Q8gAQ0zABLQAAAwG4z+PnUypTAdYH5nt7jO7+iZU5gS8ZtBlKIUpShFKUrHi2VdrFAhp4iVpC5dk+8+Xv3lTRlyxvB65ecuccY6pd5Xp8flDtShxDIhxaWRxWF1IjfeY3XZyKn3jrazssyCNNbNJX+FaUtX6Zg/HSM5dy1Vv24wh9dhk0NDauxxsZRCJiQWIhNTPZYedtyRExktdDM9wfy5TJMzn7Qb2+3IRsP0hAQ0AAAAAAAAAADMBizTWsfkFD+8iVBUj/Gdt1ys69wZm16//h9ySHKyMJnYuDr25jrmu+t/uMlps7M80kFIeJ3IjVubj3fct+bhTTxCes+deKuOCDXL79LZjr3+USth6AdWreioeK89tE54SIRt/nN7/vqHN91NiK32YIs95sitTcfbfY0XE9ZmfOeY1Z9wpmS5d61dSarPvfyRFRlomJYSKIpPAK5LCxbM7+w8TwAgDlSq1AsXGBJPSUlJLpeDZaf+HRZFUWKxtK+vj8C1g/md3eI3vwAAADBbZWRkXAe/wgs1+tUFbNOxU2ewmBlmE+yIBwAAAAAAAAAAcK1RYmFysrIgf74YOxbArIIbGgAAAAAAAAAA4Fpjrc3vVTS/RwBmGayABgAAAAAAAAAAAIC4QAIaAAAAAAAAAAAAAOICCWgAAAAAAAAAAAAAiAskoAEAAAAAAAAAAAAgLpCABgCA2SAhISFOpTAdYH5nt/jNL0pRilKUohSlKJ1NpQAwQ1EEAABg5hsYGIhTKUwHmN/ZLX7zi1KUohSlKEUpSmdTKQDMUFgBDQAAAAAAAAAAAABxgQQ0AAAAAAAAAAAAAMQFEtAAAAAAAAAAAAAAEBdIQAMAAAAAAAAAAABAXCABDQAAAAAAAAAAAABxgQQ0AAAAAAAAAAAAAMQFEtAAAAAAAAAAAAAAEBcUAQAAAAAAAAAAmN5UqlQCADMQEtAAADAbJCQkDAwMxKMUpgPM7+wWv/lFKUpRilKUohSls6m0s/M8AYAZCAloAACYDUbPME6mFKYDzO/sFr/5RSlKUYpSlKIUpbOpFABmKOwBDQAAAAAAAAAAAABxgQQ0AAAAAAAAAAAAAMQFEtAAAAAAAAAAAAAAEBdIQAMAAAAAAAAAAABAXCABDQAAAAAAAAAAAABxgQQ0AAAAAAAAAAAAAMQFEtAAAAAAAAAAAAAAEBdIQAMAAAAAAAAAAABAXCABDQAAs0FCQkKcSmE6wPzObvGbX5SiFKUoRSlKUTqbSgFghqIIAADAzDcwMBCnUpgOML+zW/zmF6UoRSlKUYpSlM6mUgCYobACGgAAAAAAAAAAAADiAgloAAAAAAAAAAAAAIgLJKABAAAAAAAAAAAAIC6QgAYAAAAAAAAAAACAuEACGgAAAAAAAAAAAADiAgloAAAAAAAAAAAAAIgLJKABAAAAAAAAAAAAIC6QgAYAAAAAAAAAAACAuEACGgAAZoOEhIQ4lcJ0gPmd3eI3vyhFKUpRilKUonQ2lQLADEURAACAOGDZPhJPSUlJw78dGBgYpfIESuMdP4wO8zu7xXt+UYpSlKIUpShF6awsBYAZCiugAQAAAAAAAAAAACAukIAGAAAAAAAAAAAAgLhAAhoAAAAAAAAAAAAA4gIJaAAAiBtKlqYUc/9QZC5SCsNKhanZmYphzyIQawoWKabtswmEqUvvWpImjF6BkmXetnpNQaq/B4N9CY5AbLgWlhbpc1OFUzkU/qaEQ7FFmYtIwQQjH7sLMbc5nYXM74jZjEFc5m5UoT8+U9rUFDYOAAAAAADXPfxyAQAAcZGbdqMt7Y41OmL885/PyTUpkmTa1moi2blKym0xthBtllyoFFraW62sv75Yk6Oj3bWEUubmKwnLOlsb211k2qDkSlqoYOVUhyUQLxEqF+mUySzTaqJ8nWItTacam+VZFPdfVmGwL8K0pUX+EfhTnV2R5ats+lKclZXM9e5cFyXvs9hlStLefN7tby+t4JsrcqmOOiIKnu7DDUuWhGvz3Jc98gTGLqMHGGq+1tdCu4nN1PkGs6kubKCGxeZvirW3BmOjJLRGOWwuWIvRRCl5vpZZC6sZbJAdjPzPX8pvv9vfhUa3JuRyg1f50jnYZotbrRvRzS+7krUphCX+2WTJ9BU6v1dGjJvNJYGB6pBkBe7Mwdt4aCgizN14J25oylpY9ZX7iiYupnnop8YSDMBkGvzxOedSpPsrN3aETEqEI0MtN3a4B3/KrjQ1+JNI+SL3HelyEEW/P3Jn8vyUyB0HAAAAAAAYG1ZAAwBAXKSlSZjG+sa6EyebL3pYK2OxCekUlVJG3G5KcoOKpmxfWhj2Sk7S1d5ktBEeRVFC4mS4yrLptKaWEtOpFEspafHQJ7eUUCIWkp6eJJomlhYLoRVDAQ/2xd0RHAEr22O39QjT0hQiHmUztVrcfXaXJDM3U+52uYMnuTuM9Y2NHx2vO/9V8HTuoFBOC22Mk1AikVwiTBZK5EJBsIU5iuBgisMHajA21nWlqSB2aC6CYc+7IdiydN6VBociP3c2+MIlD7vc0FUG25QJQrsp4GbTds5G0dN8OW2E+R0kHJzfeXOCd+bQbTw0FOFzN/6JGxq6YfdVh7HJxCTRgz81gwHcOPTjMzQF4e2ET9OwoqGfshvDfhIpOnhkQBiMXCSI2nEAAAAAAICxIQENAABx4Vs7yrpJ2pLbMm9I4l76jvW5XG4uw+y2XXKwsrSs7DThlXSuIvvW23PzbyuYnxysPK1QcuH5U3/+2CIcSotzKTwueLF2vrjHLcta7Eslc0k8oWbJyqU3q4J9WSAOjsC81KycNFpGBbrLuiwdVhfD5TTFDBO+knRoKBaIidvGsLQmUynuc7uFaZo0odvdF2yhyx4cTJdbmJq7NGNY6nQothtTr0QSiO0m/tBcBMO+1B1sufvSUINkaO5kVPCFqGd46YirDM0vXxHazYsJwlSdLk3OTuvlz5Hm19cl/4jN8w7Ob1/obTw0FFfaGZy7VG8sE3flRCEdHLqkYfeVUFOw/PYs4eDId3sHA3AHf3wEg5VlVGg7V0IarJOSOrJoZFNDJ7CDRxKGRz5WxwEAAAAAAKJKoCg+AbguLVgwv7PzPAGAOFCpUuP98yUQ8F0uB8tOfWKTS7GJxVKPx0viSpxxWy5bd/Ls6Lk8Spax9PZsSceJY432aF2lxAsyaWvzdNwVQZi2NIcyfjyB0Gb6/MYycdez+M0vAAAAzFYZGRn4FR5ghsIe0AAAMBskJCQMDAzEozReXGdOnhy7Fms/c/LImTHquM42T9Mted0dpz4mU2HGzW8sEwdD4je/KEUpSlGKUpSidDaVAsAMhQQ0AADMBqO/T51MKUwHmN/ZLX7zi1KUohSlKEUpSmdTKQDMUNgDGgAArgVKlqYU+1+JNQWLpvkj6sYSvQtXujkqYWp2ZsxjEOPQxd5mjEHGtYUZIaZu+idFKMu8bfWaglSKUIrMRcpYntk31HjEq4xnNjOXFulzU8e+JtfmIs2iYJzjNel7HgAAAAAArhtYAQ0AAHFRkClrcaVmKZNZ5pxTmZslJ05LUyMj8x/50pZ2xxodMf75T43uTB3trvUltJbk0sTFNDdOx72MiVC5SOeLvNVEabIkFEU6jIwiK3gkx98FSpmbryQs62xtcat1I7t5stnKjmynsSPQTUqsycmSC5XCrouU5uZk7vT2wXHj6hDN0lvHP3RDbVq6WM1CJeW2NBmDIXHRZuf6jhhNwqws3+XOXaT1d48MclicpnNCJY+xy+gBZ/L8lBG9G2qqhVGGdnPGGRzDli+Dw9JuYjN1I4YuwmwOGXZ7+G8G1t7a2CzP4u4TSkJrlJJk2tZqIr7hYrmRpwJDyra2WoXcdUeM4Z+/lN9+d3B+Nf4AjC1EG5jN9tbAdYN3GnGauGi1w6JlLS0WWr8il+qoIyLNkoIRl7syg43t7qE75Fhjs9QXp5DOXkAsdpmStDefd4d2alL3PAAAAAAAXOewAhoAAOLC4qZIj93WI0y7mZZSLqfTRcQyUa//SJqEaaxvrDvBpajs7U1GG+FRQprm8ltNJma65qwCfUm7aR4ttDFOQgmTgkcUbLALFCUkTsYmpGUioUQsJD093R2D3WRD21EMLlClaJqyfWlhWJbiUTZT65Vx4+pwTU5k6IbaTFQoZcTtpiTiwZCS6KEjwcv1mcOD5JoI1ifJcokwWSiRiwShvRtqisdEamFGoYbGcHAW5oQNXaTZHDo/WId1BSflShHLWhkLN24pKppw+WFCz7shOKRCX9o3dAzPnQ2+cMmDRTeoBu+Qoatxd5rtnI2iFYKhaIONSxhjfWPjR8fr7NLQy12ZQeGwu26wTbfNJcnMzZS7XVeeijlV9zwAAAAAAFzfkIAGAIC4sHS45Fk5abSMupKM483NGDzCuknaktsyb0zNvvX23PzbClT9bqGmYPntWSkZufkFS/MLchdMpz/jp+hgX7x2hqU1mUoxXxE8knRjsAvzk7lu+SoncWljQsTa+TIq2E3Z4BgI6dAxYd2sLC0rO03oP8S6Io0biW3oxFRomwkul5tLErptPX3BkMQ9wSMuT/ByVjY0SOJPcQbr97qFaZo0odvdF9q7K025h1oQpi69a4lSKNZMx0kcjXP4GPqGpcseOnTDZlOYmrs0Q3xlvIaGa2hSFohZItQsWbn0Jn5w3PpcblnWYi7De6l7cEhZwjrDxzD4QjQ4vP8/e/cC31Z9H/z/J+lIOrZlWY6lxIplY8cXEpMYEiAkBEiBAaVcC2nLBi0djO6hW7uytiu9r1vXsrbPnz7tHmjL1hUeYFBooTDKgBIaLklIIAE7ODQXJ8RO7EROLEtKfGQdSf8jyXZsR7Yl28eW5M/7FYx0vr9z0fkeSUdf/fQ7vf7hR0hyfXJ5Y2NlqRqMDG3twMKDg2VfNXDK6gYzKEYcdQPb6RFerVpt83qHfn8gT+2YX5iVT2QAAAAAs8AgSRYBzEnV1VUHD3YJADqoqCjX+/lltVqCQb+qTn8/S63qZ7PZQ6ExxmsnAAAQAElEQVT+1FFH3co1S4rbX3u52UcfT/3MVn7TWoKtut7VvXPWxoqRK1cuk1q3TvP6bXXnN6nbNu5XTonocczrl18AAJCv6urq+AgP5CjGgAYAIAOqb8/G5/YIzGFqcP/O2RyoXGnfslVMu+CejRtTRzjmAQAAAEwFQ3AAAAAAAAAAAHRBARoAAAAAAAAAoAsK0AAAXTidyYu0SbLNNuZ4T5JtoJnsrKx02qYwLpTBYNApOkB2uEdvoOyo9LjH22jt4XlqaqrdZQu0Rxe/SFuaD3NotwzcdVTWOGUxVVJ87eUnl3tyLePmKLHNGWz8CIYR+9ZgNJmMqfe1wWg0TLAgnaJJssNhk2XbuHtZdnoq3ZkfpEM78CSbu8bjKDl1esKodA/elRyeGrde1/Ob5LGRC89fokSJEiVKlGg+RQHkKJPRaBLAnORwlAQCszmKJ5DH7Hbb6afP7znYrS4446wFSmf3iWiKVpLjtCVL6wp7DgbdS08vNJZ6ivwHff1aNcu9ZFlDlcteXFpRURzp9UVdi5sanKKnOzjsimWSZOrvD0WjUTHdjEajxWKNRCLDN7Vy5ZoFUUV2VtScViZ6fJJrniQs9sISjzN8uFsZYyOMhSWSIjzL6uUTqtNjPS5X1xUayxpq5pkLC40nfCdSX4BtaLcklys5as+oK+qPzltUW+WS+44F5YW1lfO02aOO6poKZ6nTndikYHF9fKf19RxT1JSbYzttRX2hWuJZIBU6Ck4cU2yDaxk3R7K7fmGhZcHgxqeZo3g5ORYTBpPJLBmikdjA7pBMhlg0OnBPaDGT9vlCa2eSrGYRi8Riw/fCjOZXrll72ZklBUV2W1FJsfFE0OJeVLnAXlBcXl879KBk9+IKWapcVNx9WJQnUjDQzGy2LVx46t1kfod24LFO/0C+JUdVdUGfcVFd4Yl+Q39QLWtoanA751d4KrT89oqKxrqiYOdhxVapLa3UscBTIWt3g/1KtHiRJ3q0u3/6d8ngsVHqP3jCXl9Tai6uWjLxsZGlz18AAJCv5s2bx0d4IEfRAxoAoAuvov2x1dR7SquWr6wZ7Lkpe5qaPIO9O1Vf+75EM0mSREFB8v+JPpfFsiyX1NY7jrV1K8Lmdpu9XrNbt+6faVC9+7pkl2dhuZTYkrJSt7u01F1eYhnRasSji8/l61RKXX3vbzsgikVPj0g8THOhyx5Tixe5bWPONbBbBu/u291TWDqvRNsnsstd4nC5il31jZUL3FWlqupccnq1LBVrm5LYaXLxmN1QlUBAlC5ySieOtrdre3VoLePnSOnc3TVs49PKkdFstlrNZpNWUx4qPsfFYrF4Sdo0bEK8Rp3o5BITMTGb1J6gpOW1bF5i32r5LVbV8jNPtw0/8CTX4vPO9siqyTaQgmSzsiUNnlR3k3MN7cCTxVepoFhSVaGqxZX1Na6yyppK2VLqKbcl8lsQ1NIt22RJTizN7gwdTNyNb6MqCvS5ePTgsaGtQfG1tx8+nNaxkUPPXwAAAACziQI0AEAXVW6XyxZTgsFAQNGKbQNTlY7m5o6h4qrsKk82CyqSVrJSg8qwLpKxsLDXNS1xy2FFlDc2lgtFFbNGKnU7pGK7vciT2JKgIhzajeiJiFxVU+kYrAqOfHRxtnKX2ms987ImKaDVfBMP0xoT809v8MTLiWPMNbhbkouVbK7KqvL58wq1u9o/q8PldBXL8aJhn1TZMC+magsOeAfqm+PUJ9XufZ1Kz+5mb0F85IdhO3/cHMmVK4dvfFo5iobDoVA4HIl3NjYZDYmxNYySFD/lMBjEyX7OsYE/sWg0GjnZM3p2qN3tPUWu0rLEvo0Xe1W1r08sGHHgBXxtB3yKZCsdSEGymdHqKEt9N25oB56kBHpUWYRVubRAKNreV7S9e7w33slYS58pnm632+2wJpYWNZUsTNyV44VdKaDPk2Dw2GhX4uPKVDpL0jo2cuj5CwAAAGA2GSTJIoA5qbq66uDBLgFABxUV5Xo/vwoKrD5fj05DNDgcpX19IaEL2V1f3rdvv2/q5TjZWd9QKQ607PblYWkvZ/ObDslR6ZG8+7uVDOaRndVu0bUvo3mymH75BQAA+aquro6P8ECO0uennAAA6MxgEDpVr7TF6nnxE6Vz934xLZTu3c3dIk/lbH7Tofra94sMKd3794n8oV9+AQAAAGQbhuAAAOQek8nY16djV1BF6dNWITBLyG9+0zu/AAAAALIKn74AALnHYjGfOHFc6Ob48ePaKgRmCfnNb3rnFwAAAEBWoQANAMglJpOxoMB67NhRoTNtFdqK6Cc7w8hvfpux/AIAAADIHowBDQDQhdU6zRe5NRrj4/aGQsqxY34xI7QyWVFRUUGBLOIDB8cE9ER+89vM5xcAAABAlqAADQDQRTA4zWWmaMJYUYPBEIvFpj16PMGYIKAn8pvfZiW/RIkSJUqUKNE8iwLIURSgAQC6UFVVzKDxz1OnEhUT1c4wA8hvftMvv0SJEiVKlCjRfIoCyFH09wEAAAAAAAAA6IICNAAAAAAAAABAFxSgAQAAAAAAAAC6oAANAAAAAAAAANAFBWgAAAAAAAAAgC4oQAMAAAAAAAAAdEEBGgAAAAAAAACgCwrQAAAAAAAAAABdUIAGAMwcg8FAlChRokSJEiVKlChRopOIAshRJqPRJIA5yeEoCQSCAoAO7HbbsWPHBAAAAABMh3nz5vERHshR9IAGAAAAAAAAAOiCAjQAAAAAAAAAQBcUoAEAAAAAAAAAupAEAAA6kKQ8eYuJJojZYEwQ0BP5zW/kN9fNYgYBAAAwXShAAwB0YbPZRV4wGuPX4u7rU06cOC5mSlFRkSwXxGKxaDQmoCfym9/Ib66blQwCAABgelGABgDoIhTqF3nEZDLNm1d27NhRob+ysjJFCZ84oQjMFPKb38hvrpvJDAIAAGDa8cNAAAAmFolE+/pCWgVE6KyszHniRIifnM8w8pvfyG+um7EMAgAAQA/0gAYAzFEmU/yn3fFfd58i/tP5aIqfz/f3h4uKio4f1+uX4DabLRQKC0wH8pvfyG9+iMViKdMYSzV4id4ZBAAAgE4oQAMA5hxJMlksUsrS1XDhsKr9G14HiUSihYXy8PKHtpBYbMxhXjONWq0yv9yfOvKb38hv3tD2YWKI59SpTHyLEB0e1TuDRIkSJUo0+6MAchRDcAAA5hatmjFQvTKVVC1aYE1ONc3zVFcuKDENb2k2SxaLedTs2vmw0Wgcdne88+OMotpiU7bXJmo1Gu2vtj1CdxZX45JaezoTsxT5TSWXMji+nMtvWuyLGmuLxRyT6PscrzKIRBn6ZCBZlU5cfnB4sgbn0iuDRIkSJUo0J6IAchQFaADA3KLVpBJd6kwlpzVU2OIVK+uChuUXnd9Ue0bTaQ7tvnVh0+rVTQuL4o0lyTSiMpLolHdqTWRaaIs9ddAAkai4aduQGHBg+GTL2m//1+MP/PB7d17dOJnCosVz+T88tP4PD9x9kcc6fLrVbnfZrZaRjU+ZaF10+d0/f/qh/9VoFdmG/CYUj5w9ZVoTsjiVKeVQfrXPz7Js1jZYK4UnopFhY0M7133vu9fULln37W9e47F5GmtdIjQQsS657Xv/sNY1/tqKV939Ky2/377tPFeOJO5UxkTnZ+2GKZ4m7Y8pnq+Tdw2JNqM7R+uXQQAAAOiHITgAAHPLYPEi0vtB2/EVC2RTb1lVSe/Bw4XFsURxqOi0MxsqiiRH7weHWnvFQF0pImaDVsDSKjLa31AobDabVFVN9BkcrMiE/Hs3bXih9YN5N//8gUqv39rxxD2/3Ft7ze1XLHeZOvYWr1q70Or3bn/4O/d7L//WXautIrT53q892jpQ5urv2PDkMx+yhx7e3BFyrv32v3zM6hWi5TfrS2+8Y9V792zf7rU23qzNJfz+lv9+rfDGTycnCteqxPLF9vv+/ZHNf1Mrsg/5HTl7a4ff4ll7812f1TJ4wP7ZryYSvf2+7zzrXZ7tqUwph/KrpTIUUpPduGRZq/4PH5ba3/qeuHZ5oxC7Xl18y93xJ93mDcK6/LZv3VLnt7os4Rt/+MDSZE6ftd78o29f6xIdT37ti8PyK0JxXn8oZKld963Pak/V9178zi9fFblj6EjXdpGWPJNkiKgxo0nEhMFojGm3B5vxQ2wAAICcRwEaADA3mRacsaLxjLKyo949wrm01mrwdsQWrVwRfKurq/eo3P3BwaDIAslfqSfqL8lqzcgxZ5P/C/m3PXP/k16r0CpXLpfVavfU1fW0dWzXilXanTKnfYXHKrx+YbVrM4RSrSbk3fbCs+LatdF373/4j57G+KK1hYReuPefntzbL0RxX3Viohhcfm2jp3iDyGrkd3D2+JcNjzzcmMjgYKJdWtOcSWVKuZHfoeLpYIqH8tvfsbfD9bFVofce2fGHvQ/XDzzpXJWhTU88a//EjQuXeayxRE6L7fZKr/Y1g/Vjl7vsQniTswdan/jxd0LWtXdds3zzj1u1ryfsHvv8XO0LbTAYJUloxXlJMkTViFaNVsORqAAAAED+oAANAJhbotGo0WgSInK4+aXHmhOT2p5vT8beSv7vpfZh7SOR2ek+mWQ0GqLRWEGBNRL/+f6w7rHxSqP/ve0bNmwX8W6Uwu/dGxDWiuUrVnns/lD/sEWE/Xu3dYRWa6XH1r0nq5MWz9p1165aFfKv2n5v69DEqsvvvOiKVa66da33PNPRbr/77p9e4X/zd286r0tOPPJHe3L52nIC3nb7nXd9W/zHvY9s9vaLrEF+R84e0L4/aLzmztvjGex6PmgMJ8MWuyfrU5lSDuU32Z89MQ51LByOhMPhoUEnNP69e0O1l4ee8XkGshN/0mmZ+NgtNwu78urbHXVLEzkN+F3aM/GuLwjvi/f4h5Zt8ay6LdntfXMo/lVCyC+0LxO0xy5yh1aTT+4MbdeMSNLIHuujrkMIAACAXGSQJIsA5qTq6qqDB7sEAB1UVJRn7fNLK2Vo9b40KxqqGgmFwsOnWK2WYNCvqqqYbpIk2Wz20LDiYmKIBqOqahU3g1agZOTTdJDf/JZD+cX4tOM/MfT5eKnUvpUZNf6GfhkEAGS/uro6PsIDOYqPOgCAuUWrZoTDaRUvotHoqOrVDNNKM5FILPErfkF1Mk3kN7/lUH4xvgkHd44PDR1lKA4AAIB8wBAcAIA5JxyOqGok+XP4lP3vEnWP4VcMQy4hv/mN/OYNrf6spTJlGpOlaQbfAAAAyA8UoAEAc5FW3Yhwmav8RX7zG/nNG8kSc4wvCwAAAPIav/cEAGDyxu+gN5UosgH5zW/kN9fpl0GiRIkSJZqdUQA5ih7QAABdFBfbRD5S1RGjyk44hmlGUaPRkK/7LVeQ3/xGfnOdrhkkSpQoUaLZHwWQoyhAAwB00dfXJ/KRyWQSuolGY/m633IF+c1v5DfX6ZpBAAAA6IQhOAAAAAAAAAAAuqAADQAAAAAAAADQBQVoC0SNwgAAEABJREFUAAAAAAAAAIAuKEADAAAAAAAAAHRBARoAAAAAAAAAoAsK0AAAAAAAAAAAXVCABgAAAAAAAADoggI0AACTZzAYdIoiG5Df/EZ+c51+GSRKlChRotkZBZCjJAEAACYrFovpFEU2IL/5jfzmOv0ySJQoUaJEszMKIEfRAxoAAAAAAAAAoAsK0AAAAAAAAAAAXVCABgAAAAAAAADoggI0AAAAAAAAAEAXFKABAAAAAAAAALqgAA0AAAAAAAAA0AUFaAAAAAAAAACALihAAwAAAAAAAAB0QQEaAIDJMxgMOkWRDchvfiO/uU6/DBIlSpQo0eyMAshRFKABAJi8WCymUxTZgPzmt2nMb2FhocViFtCZtpO1XT10V79nKFGiRIkSzc4ogBxFARoAAACYJEmSqqtrbLZis1kqK5tnNHJ2rQttxzqd87SdrO3q6upqbbcLAAAA5AhO3QAAAIBJcjpdvb1+RQlpt2XZarMV+f0Bgemm7Vif7+R+1nZ7V1enAAAAQC6gjwYAAACQmbIy56pVq6+55jqTyZisimq0G/qNXCmXL73gyj87q1xOdwbJ4Sm3icmzVZ+12Jk1nVW0HTt8P2u7XQAAACBH0AMaAAAAyMCiRbVVVaft37+vpaW5uNguy9ahnrm6jVwpl3tsHZs2++KF4XOWlktq184OW325UNXgnh37g8mJSteOPWLxUqcIdu/zlV985RKxc9MfW5TqJYnQO/uDiUVJzro6qdvncFrCjoZFpSLQuaOl21FfLqvde3Z0JNtoa1m6xKVsja9tVf3INvul6jqbJImOd3Z0ywPrbfM5m5LN3trRpYrpp+3Y4fs5EokKAAAA5AgK0AAAAEC65s9fcNppNa+88ofk3VAo5PF4Cgpkg0FYLJajR3uEXlShBH2KXF0nuvZ0OasXFAoR7PA5PA55v+osdwilW7LNWyiLjvd3aHXqYPc7LUrwrfeDnlXJkE0WQSW+HEl22KSgYpsn9xuDgYBWbHbYOn0+rU7tce7pSLYRwf07djrrJKskS6PaLDyhyr4On7NcloQ8sF57iX2omdTl06ECHQgE580rLSzs1yr8Vqulvb1dAAAAIEfw4zUAAAAgLU6n68wzlw9VnzWqqu7fvz8YDITDanf3Md16QKtBxVF/4Z9dtrSkT7uxvK5UCUbiNenBaFCRJEnx9R7TKtRnXbC6ziapiqg8Z1VdUd9AaKCyrDVWFNlT7ZGVUGRgirm0bqnH6Rh2YT/JuXjV6mVnrT7TI49u09/brTqr69y2YevtPd4v9KXt2KNHj2k7WdvV+/bt03a7AAAAQI4wSJJFAHNSdXXVwYNdAoAOKirKDx/2inxkMpmCQb8etQ+tiGOz2SORiMDsIb/5ber5/ehHb3z22d+duoQ5lV/JUXfO6sXF7a+/ssM3w2Vg/Z6hAIDsV1dXx0d4IEcxBAcAAAAwsTPPPOv993dS/VR9ezY/v0cAAAAA6WEIDgAAJs9gMOgURTYgv/ktowwajcbTT1+yc2drOvNiZuj3DCVKlChRotkZBZCj6AENAMDkjT/e61SiyAbkN79llMEzzli6Y0dLmvNiZuj3DCVKlChRotkZBZCj6AENAAAATKCurmHXrvcFAAAAgAzRAxoAAAAYj8dTeeTIYUZ/BgAAACaBHtAAAADAeGpqFu3b1yYAAAAAZI4e0AAAAMCYLBaLzWY7dOigAAAAAJA5CtAAAADAmCorq7q7uwUAAACASWEIDgAAAGBMCxdWHDzYIQAAAABMCgVoAAAAIDWDwaAVoBl/AwAAAJg0huAAAAAAUnO7Kz74YL8AAAAAMFn0gAYAYPIMBoNOUWQD8pvf0sngwoULvd4jmc6LmaHfM5QoUaJEiWZnFECOogANAMDkxWIxnaLIBuQ3v6WTQbfb3dXVmem8mBn6PUOJEiVKlGh2RgHkKIbgAAAAAFIoLi6ORKLHjx8XAAAAACaLAjQAAACQQnl56u7PAAAAANLHEBwAAABACk6niwI0AAAAMEX0gAYAAABSWLiw4q23tggAgBAmk1kA0y0SCQsAcwAFaAAAAGC00tJ5gUAgHOaDMQAAADAlFKABAACA0ebPX3DkyGEBAAAAYGoYAxoAAAAYbd680sOHuwQAAACAqaEHNAAAADBaRUXlli1vCgAA8p7BEPNUptu265AIqwIAMkEBGgCAyTNo5+uxmB5RZAPym9/GyVFZWVlvb28kEsloXlUdsz2mhclkGn5Xv2coUaJE04kib8TmL4h+4pY0Gxt/+2tD2x6hG446IC9RgAYAYPLGPz+eShTZgPzmt3FyNH9++fjjb5DfbKDfM5QoUaLpRAE9cNQBeYkxoAEAAIARFixYcOQIA0ADAAAA04Ae0AAAAMAIDkdpVxcFaAAAAGAa0AMaAAAAOGnBgnKfr0dMmez01FQ65eF3a8odg90/JNkWD0mOyppEm/j9ibuGyA5tIR6HPD3NpsvJ1cnOykqnLbMuLgaT0TBGxDhWBAAAADmEAjQAAABwUnm5u6urU0yV7K5ySbaaM89qWrFisVu2uatKVdXVWJ8sQUuuhnq3TXLU1FcWaxPkmvNvuGndZSvcsuxenGifepmli9ySElRkT319tXPM+nKazaaNEgyKUlepJNc01thsNY2VtuRmuJcsX7Fi2ekNpzc1xTfjlIcWLzAbTUatBC0NfigxmSXJZDTGy9KS1WKg/gwAAJAHKEADAAAAJ7nd01KA1qhKUDjmW7xes9tdJLkWr2y09XgVdVgD377dPfGuz0p787Ztb25q7pQqayplqdjtGizTyp6mJs/gHbXPGyioPPPClSsaF5UWDO9onGYzvaiqKhcXF0mSKCjQqutSfJ2SbCuWZbmktt5xrK1bETa325zYFcnytDCazVar2SSi2ieSYVec0m4aTKZE5TkmuBAVAABAHqAADQAAAAywWq2xWMzn82U0VzQaTTFahFxeU1PYHy5rbCwXiqp639/48qadWiV2IOp0L6qtrTqtSit4O+R4BddV6bKFg4oi1IC3Z7BMrXQ0N3coQ8uUCmyyCB7r6AzY3KXD+jan2UwXcuWK1Y1umySUoCJpJWc1OLzIHgsLe13TErccVkR5clckA9FwOBQKR7Q69Ij688CfmLZPI9HoyAq0tpO1yQIAAAA5xSBJFgHMSdXVVQcPcn0hQBcVFeWHD3tFPjKZTMGgXysViekmSZLNZo9EIgKzh/zmt3TyW1tbN29e2datb4oMlZU5T5xQBPRUWGg9evSoADAbTCazQJ6KLSiPfvK2NBsbf/trQ9seMU0ikXD6jevq6vgID+QoekADAAAAAyoqPAcPdojMKUqfycSptY603dvXR4kfAAAg93CWDADA5BnGvUTWVKLIBuQ3v52aI22K273w0KGDIvP8Hj9+3GKhe6COtN174sTx4VP0e4YSJUo0nSigB446IC9RgAYAYPJisZhOUWQD8pvfTs1RefnCDz7YN1Z0/Hk1x44dLSiw0g962mm7VNux2u4dNV2/ZyhRokTTiQJ64KgD8tJMXBUbAAAAyH61tbX79+8TU6AVSYuKigoK4tf9G30FPWQueWnHUEg5dswvAAD6MBzrNj7+cLqNvUcEAGSIAjQAAAAgzGbzggXlr7/+qpia4wnGBIGpiSYIAHOMyWQyGHgJnUHaF6adnQM3Y1GumQxg2lGABgDMAslRt7Ra9u1/f79PHbuVrfosT3DH+93Dm8jliz3qnj3dqsD0kJ11S+vK1a53duwPTtdeJb/Zg/ymr6Zm0b59e8U0oXIKAAAAJFGABgDowrH4nDpZVYP7dwfL68tltXvPfmnxUqcIdr+vFcIkWXsDkmw22eZYvLRcUrt2vLU/mJxRq1AtHmi/dIlL2Sqk8qVnlQttUfv2i5o6h+yWuzqDzppEmx0dQYEpkRyeatH1zv5uVa4+R8uF0tXmczbVl4pA5463dnQlC4W26qV1NkkSHbuD1UvibXbul+vJby4gvxnweDxvv/22AAAAADCt+FULAEAXRZLk27+nS5GE4vMpcqVn4UKn6NCKV8m+j8Mmdu3pEk6nPDTnQMip7t+xs0dIGlkre/lkZ9lCp+Tr6PKq6lAbWWCK1K733/GVn3Nu9bwF5Q6hKJK9xC4FA4GgsDlsA99Tyw6n7OsOCsk+0MZmI785gvymq6LC098f7u31CQAAAADTigI0AEAXIe0/NdjVESytW+pxOiQpclyRq8+6YHWdVvWKjwowONFRv7yuVBkaHGAoZCpbvGr1srNWn1VVoC0pHoooqsNTt7hSLiwbaCMwZVL54rNqJFVIhmBQ0aqFSu/x/tFtFF+36qyuc9six5NtfEHymyPIb7qWLl323nstAgAAAMB0M0iSRQBzUnV11cGDXQKADioqyg8f9o6eKjmXrqr2vfVWhyJyl8lkCgb9qjr9Y9hqhT+bzZ6dV32RHHXnrF5c3P76KzvGHvSX/I6L/GaDsfLrdldUVVW9+eYmAQAYg8lkFjOFixDOohm+CGEkEk6/cV1dHR/hgRxF5yIAwExRu3e83i2Qg1Tfns3P75moEfnNVXM8v0aj8YILLnziiccEAEB/0ZWrYxddPH6byCfvMOzdbfn4VSNmrKkNv/GuMBhEekw/+Gfp3nuSt/v/sCl2RlOaMxp27rBccl7ytvq5L0W+9p00Z9Rqt+YLlxv37o5vbV1D+NVtGWzt974t/fRHA1u7/s3YkqVpzmho3m654oKBrf3i1yNf+lqaM8a3ds2ZxsTVd6P1p4c3vD2wtQc7xMP/PsFKN6w3bt0sACBtfKkIAEBatCpVSUmx1Tril0OGcT9XZBrVFm63F2srEphx5De/jZPfD3/4Iy+//OKps0xv9okSJUo0/6KTlOYYTAWFo6fIBSKj7ZGHXWvAmsl1B4Y3LiwU6dM2T9vIgbVnuLUFBSdvywUifcN3lDWTH7hrmzf0SLWFZLS1Zh27w+ty1AGYbXwEAgAgLfPmOU6cUI4f7xs+MRaLjTNLplFt4X19irYigRlHfvNbyvxardarrrp248Y3jh07duos05t9okSJEs2/KKAHjjogLzEEBwAAE9MKVf39/Vr10GQyJadUVHg0ydvhsGo2x99SI5GoyWRMTAmbh/UNGbo7rMHALJqOjo6DBzuSt7VVyLK2NmsoFBKYKeQ3v6XM74oVZ2tZ2LDhlWAwIAAAAADohgI0AACTcfz48SNHjiRvR6PR5LgKQzeGCpGDDSJGoylly+SiBLIM+c1vWlLWr/8DqQEAAABmAAVoAAAmFgqFiouLCgrk/v6BS3X7fD3aPzHdtFVYrZZAICgwg8hvfkuZXwEAAABgRjAGNAAAaTl2zKcVsIqKMrksTIa0hWur0FYkMOPIb36bgfwCAAAASIke0AAApCUajfr9gaExZPUQCvWfONEnMBvIb36bgfwCAAAASIke0AAAAAAAAAAAXVCABgAAAAAAAADoggI0AAAAAAAAAEAXFKABAJg8g6Ejjl8AABAASURBVMGgUxTZgPzmN/3yS5QoUaJzIQrogaMOyEtchBAAgMmLxWI6RZENyG9+0y+/RIkSJToXooAeOOqAvEQBGgAAAAAAYK6KRDJqLqgRA8gQBWgAAAAAAIA5ytDaYv7o5cIYH6M1pijRzo4J2nd7BQBkggI0AAAAAADAHGWIxQyb30jejsWisUw7RAPARLgIIQAAAAAAAABAFxSgAQAAAAAAAAC6YAgOAAAAAAAwE4w73o21fzBBm9f+aFBCAgCQLyhAAwBmWUyH62gbDAYBAACALBMrd0fPOmf8NtErrjaUueK3IhHznbcajh2Nz+hyiUxEG5acXKlrftrziVjZyRVF604XAIApowANAJhNelSfk4ulBg0AAJBtYs75ouq0CRqdsyq2sGKgfUVlsgAtiopFRuaVnbxdUCjSN7yxM7Oqt4hGR9/IdEYRP5EV6Rs+Y6YXD9TnPBwATkUBGgAwa2J6nvXOTA1aW8U4j2IqUWQD8pvf9MsvUaJEic6F6Awz7G/LqL1x8+sn5z2wP1bXkOaMho4Phi8ksmpNWrP191tPKz05Y2uL1V0kJsWy5kwxKdK//pP2T+S4rDrqAEwXCtAAgNnn9/vE9LHbHWKmjH9+PJUosgH5zW/65ZcoUaJE50IU0ANHHZCXjAIAAAAAAAAAAB1QgAYAAAAAAAAA6IICNAAAAAAAAABAFxSgAQAAAAAAAAC6oAANAAAAAAAAANAFBWgAAAAAAAAAgC4kAQBALujt7dX+lpSUCAAAAAAAkCPoAQ0AAAAAAAAA0AUFaAAAJs9gMOgURTYgv/lNv/wSJUqU6FyIzgmBQNot/QLTgaMOyEsMwQEAwOTFYjGdosgG5De/6ZdfokSJEp0L0blAuu9e7Z/ADOKoA/ISPaABAAAAAAAAALqgBzQAIEv5/SN+yaiq6qkT7Xa7AAAAAAAA2Yoe0AAAAAAAAAAAXdADGgCQpUb1bu7t7RV0eQYAAAAAIKfQAxoAAAAAAAAAoAt6QAMAAAAAgBlhNmfUPGY0jrqR7oxFRSdvW6xpz6c1tpy8vbAi8uefTnM+0wP/1+DvFQCAU1CABgAAAAAAMyFWvjCj9mJRnXh3W/xG9aKM5oudueLknXK3SN+Ck42jjU2RL30tzfmMf3je8O52AQA4BUNwAAAAAACAmWA40pVRe9H+wcCNQ+0iE4aWd0/eOZzJSjPdQgDARChAAwByQ0mCyDIGg0GnKLIB+c1v+uWXKFGiROdCdJJCoYyaGwbbG5QMZwz4hy1ESXu+k2vErNDlqAMw2xiCAwCAyYvFYjpFkQ3Ib37TL79EiRIlOheigB446oC8RA9oAAAAAAAAAIAuKEADAAAAAAAAAHRBARoAAAAAAAAAoAsK0AAAAAAAAAAAXXARQgDA7PP5fAIAAAAAAOQdCtAAgNnncDgEAAAAAADIOwzBAQAAAAAAAADQBT2gAQAAAAAAThGLZdA4EhUAgFQoQAMAMHkGgyE29ieTqUSRDchvftMvv0SJEiU6F6Jzgenl/zG5iwRmEEcdkJcoQAMAMHnjnx9PJYpsQH7zm375JUqUKNG5EAX0wFEH5CXGgAYAAAAAAAAA6IICNAAAAAAAAABAFxSgAQAAAAAAAAC6oAANAAAAAAAAANAFBWgAAAAAAAAAgC4kAQAAAAAAoL9YRWVm7SurRMs78RuezGaMrlw9bCGnpT2ftqKqodvq574U+dp30prN77ee7hYAgFToAQ0AAAAAAGZEuD+j5iKijr6RpmDw5O1QSKRveOPCwjRnErIsAABjoAc0ACBLKYoyYRuZc30AAIDcYThyOFbXkEH7Q4cGbnR2ikwYW1uGrbQrZrenOaPBe1gAAKYVBWgAQJbKieKywWCIxWJ6RJENyG9+0y+/RIkSJToXooAeOOqAvEQBGgCgC1WNTNhGp5PLoVVr569iuplMpuF3x38Ik4ims9+gH/Kb3/TOL1GiRInOqSigB446IC8xBjQAAAAAAAAAQBcUoAEAAAAAAAAAuqAADQAAAAAAAADQBQVoAMCcITnqz7/yqhXluXMBBMm98sobr7tyZb0jW7Y51T6UHHUrViyrSb2NtpoVi52jInL5knqnNMbyK9228ZaQe0kcRzbkd1SCJGf9Yvc4l/8cJ3cinblSHQ8jjXc4actZUp4DFycFAAAAMAwXIQQA6KKpxtYmljS5JbWzdZfc0FCgqoEDRwoWzReqCOzWQo1uKXyoecu+oJhuJaetaFxoCXXt2L7/+IiA6tvdvLO0QZLiVcw6s9fncMW8YtF5TeVi92svNHerIutIonvbhvbSpsoFsfrT5ktKZ2vbwM7ctytY3uAuUL2726SB/dxe3OAWWmj3LsXTOBCqaSjWHm/7rkCNtsOVzrYeV1NDqQh0tmxp7ko+XlvNuU1jhBLRZckltHqdydU1D+5DV9NydyKbuxTtdEIqLpZtpcktaRlKqzZ7o0t5U6u0JhqrgbY2saihVHbLR/zCGY2nQG0PDi65Xa1cedlVjaL1jVdbRdWixMNsU5ckliBk9+LGERsgsjBfmZqh/LpE0LtzaK7mdlGzcnWyWas244gEHQi4atzFBa6eobW0eUsbRuau84hac/roRI91FEnxQygx177d3fLg8eBYsrxhIL/1iS1v2aW9XAxs55iHk1zqKCgoaKgMNrdP/+sGAAAAAJ3QAxoAoIs2r8nlEp27OoXLWWSWetp2dypWSRY9h3ok18IFgyE9OjM6ykuEokjFtrEXLhWUFssFcnGpObhvZ1v7/ua2bKw+a6TS+pVrl4l9hyzzHckHNbgzJUmOP8K+vqH9vKBQFgFvj+xyWPt8PX1yZaW2n+Ueb0BI9gXuxOwldrsUDASCwuawDXwHLbvGDMWjpQNLkE0DyxxKmTSYTedgaGHFKWkN7mtp7RFmKd44sW1lFS6p50CnV43JAymQrQMPRMuA0t68vXnbaxt3HhWDD3NwCUKM3oB8MBP5dWnfHrS0edWTO1Bb9mAz0T4qQSVGtdvbOXwtQ+sdyp3ROTrR4xxFkmtgrvgzbCib0sDDLHQmZyyeVzF6O1McTnl5DAAAAAB5jwI0AEAXaxrkPsXRcHZ9qRKMaPfVYGf7MYNc3thYWar29g6G9Cj7KsdDWj1N6QkqcnnTyjrb8F/7qEKuOffSlQuiilxZUykrYefKj5xXU17pzpoxLkZSe3Zvefmlbe29gaCSfFAhkdyZPiFrm2xbVGUbvp8T+9PibFhW6XJIUr/Pq7pq6t22SDA5u+94/ylrCIwZ0ig9A0sYWubQPlxYOJDN/tKBUCQ4Oq2Sc8nqNU3Lz19RVTCwbRFFdVQ2LKmUDcpgCgwDDySRAlURleeeX18iDT5Mx8ASGqpGb4AnD6qQM5FfRa5ZceGahnnlQzvwJOO8xaMSlJhnxFqGppzM3SmJHucoUgfnkoYdD6cVDTzMI76BB957dPR2nno4ya4UDwEAAABAtjNIkkUAc1J1ddXBg10CgA4qKspTPb/kypXLpNatQ6NuxGKx5I0TJwJi+hQWFidvmItr6l3dO6d1lA+r1RIM+lV1+ivnWhnOZrOHQv1i+kiOupVrlhS3v/Zys29yWzz2EkZnMz/MtfxmEcnZdH5Nz5at7YrQj375BYC8ZzKZxXSInn9h7PwLJ2j0yTvEworkTfPla4wt78RnXLI0vP5NkTbTT34off8fk7f7X9seq2tIc0ZD2x7LmjMHtnb1BdHz16Y1W7hf+skPRe6LxaKRSETMlEgknH7juro6PsIDOYo+JACAGaO0b9kqZpAa3L9T5/KowWAYKqNPb3RaqL49G5/bI6Zg7CXMdDZnRd7nN4uo3c2vdouZpV9+iRIlSnQuROcC46bXtX8CM4ijDshLFKABAJi88c+PpxJFNiC/+U2//BIlSpToXIgCeuCoA/ISBWgAwOzz+XwC45Gc9XXm9vc7xxqdQC5fUqnu3j3upRTHbyM56leublC2v7CtK93hCSRHpUtt75zuTuZjb6etZnlloGXnWI9yEg8hm423e201KzyB1q7SFeM83kSb5vfHPCbSOWZO2aT6Fee6lZYtzV3KpBZoq1y+psnpbd60rX3gccnu5ZeukLa9vLVTsdU0aQ/q/Sy9HigAAACAyaIADQCYfQ6HQyAV2b240V2geg8EXJXu4gJ3z+5diqchPqXNW9rgFqoaaGsTixpKZbfceUStOd0tqZ2t7cXJULxxYva2NmlUm5YtowZvVn27m3eWNiQv8peod3t9DlfMKxad11Qudr/2QvNAYXBok3oqL7mqUbS+8WqrqFpUoK1u365geWLbDnhtpeF2X2mldEyp1FandLa0DmzJ7l3qqBtDD2R38z6tBrlsrO20VZ4br12+0TK4ASdnbBNLmhJr2Tb4EKSBNidX19yehYNVS+6m5dpDEImH0JjI3S65oSG+Mw8dc1304fjufWWbz9kw8iFoe6nRpbx5MmVaYTiZL0u49PTaUhHQdnigJt5mcBXDDgZtOSf386Ggs3bkwgd37+42Kb5Xh6VArlxx8domqX2bqax+cTRxeAQKquanPghPOcASG+6ulHa9udvdUG7r9C1a4T60bWcw7G3rccva0muWNzk6XxYAAAAA8o1RAACArNXn6+mTKyvLjKqv80CP5HKaBqYsKJRFwNsju8oqXFLPgU6vanS6ROeuTuEaCjmsg41PaeOUx1urVFBaLBfIxaXm4L6dbe37m9uGdUsdWGaxt3l787bXNu48KsxST9vuTkUaCvWrrobGepcatrsdQlGkYluRXGyTRV+fKg3eEKMfiEMWkmvs7Qy2b32juVsqkE6ZcX7F4Frk0RvpHFqvyEqSLHoOaWlduGDw8RYN7MxIx8Du7VYHH8vJXbGvpbVH2+snFzOQr7LCIikYCASFzSHak20kafTB4By2n4ey4Dxl1y2sGJ0Cpb11e3Pzpg3bjhoHDo8i65gHYcoDLNi+L+A6e7kr2K2o3c1bWrpVVenWbov49wuVYl+71LSiWhYAAAAA8go9oAEAujAaDRO20WmEt6FVGwwTb8OEtI2craHoDAaprKZhgdWkRiMGo2NRjTHSd7BkcEokHFZj8T8n1IKKmpp5xn3t/oLTl1aJI7u6rIWGeMhUWrMo0bj/RN+oNu9FCuY3Li46sGP/iaHrnEcixvKla5ZHN77rPRE01nsWiGDbvOUfWlbeu6+7pOuEP9HQenKTIv1h17JzFr29T+2PqMcPH1TdZ65Mhk54vQVLKtt3+f1m/wJrLHj0RKQo2h+2VLhLj4WSN5whadHIBxI1aI+vr6B61HYaDSe/LY9G+8KWslP2gD/oL42vJdgfMScegmmvOC3RRpjMydUtUOcX26xChHr3vd9xYthOntX8aseqY1GdMXK87YNI+ZL4492pCkdiZx4XVkti90YOlQwdA8ldIZXWrVhe61Zi3YEdyZTtaA0aK+L56gwVFFnibaIlA238fwqH+0ccDJFh+/nAkZNYmcqNAAAQAElEQVQTkwsfym+/P3hqCgbSNHh4fBC22g2pD8JUB5gQ/d3H+o69//rO3qi5rHHp/MM79kRqzlxWW62Gj7T09DscRdG+Y4bhGZ+yWcyvMUFgaqIJAgAAALnMIEkWAcxJ1dVVBw92CQA6qKgoP3asZ8JmQ4Who0e7xfQpK3Mmb0xLAdpg0IpIhv5+NRQKaQu0Wi3BoF9Vp79HrSRJNps9FOrXdou2Fo1WdonFdKu8GMwWSSsh50plx2CyyFZTrF9R1GktJ85qfmMmq8UQ6gvn5bV2suMAm7H8DldUVCTLBVqitRQLTI2WPu2FvK9POXHiuAAwq0wms5gO0fMvjJ1/4QSNPnmHWFiRvGm+fI2x5Z34jEuWhte/KdJm+skPpe//Y/J2/2vbY3UNac5oaNtjWXOmmKu0t69IJCJmSiQSTr9xXV0dH+GBHEUPaACALvr6QhO20aln4tCqp6UAnWQyGYuLbfHBDXSm7ZPi4qITJ5T+fr2rLaE+kVP6FP32/qzl98QJkbey6ACbsfyK+BdgZYoS1lIsMH1MJtO8eWXHjh0VAOagoWJopr+HmHQVlR9eAMB0owc05i56QAP6qagoT+f5NVSAPnEiIKZPYWFx8sY0FqCTiooKw+Hw8eMBnXrIFhUVWyyWYJCOfrOD/OY3XfObVFbmpPSsn4ICKzVoYBZNVw/o9NZlMhgYxWh20AMagB7oAQ0AmKNMpvhPu1MWqeM/nY+m+Pm8oihWq1XoxmyW+vqoXk0P8pvfsjC/NpstFMrgUzRE4mvIlGlM+fOY/v5wUVHR8eN8hQMAc1dFRbkAkIMoQAMAspRWLerr69MqSRaLpbi4eGh6IBDo7+/XKhaFhYWyLIvMSZLJYpEm7B8dDqvxq9wNq4NEIlFt3uFttIWMM5BIplGTyTSTXU7yFfnNb1mbX6tVpvtzRgzxIboNY6Uy8S1CdHhUy6D2qj+8AD29GSRKlGim0WkR/ci1scaloyZGho0BPYKiWOoXGBI/ZIl8+Gr1Px8XaTO0vCMsltjCSjHsrBJTEgiIgwdER7vhYLvY/b7hud8ZOg6IKRv/qOvo6BQAchC/agEAZCmtyiBJklZl1grQw6drd7WJZrNZK0+LzGnVjIHqlamkatGCgf6Qpnme6soFJSOKU2azZLGM/rXpqILI+J/KMopqi42mGnNQa6bVaLS/2vYI3VlcjUtq7elMzFLkN5VcyuD4sja/RqNx8jUa+6LG2jlXDUn0fU4MlJQoQ58MJKvSicsPanv1lLnE8InTmEGiRIlOIjo9pEze/mRZDL0IyAUiE7FlZ8VOb6T6PJ20nbn4DPFnH47dekfsu/87un1P5LXt0a//c2zplC7hOBNHHYAZRwEaAJC9tCpzQUHBqF/Na3e1iVooOqlLxGg1qUQFylRyWkOFLV6xsi5oWH7R+U21ZzSd5tDuWxc2rV7dtLAo3liSTCMqI/EueDHDdA8tnaQtVlt4qunxQkxiwIHhky1rv/1fjz/ww+/deXXjZAqLFs/l//DQ+j88cPdFnpF712532a2jrg9xykTrosvv/vnTD/2vRh3HM5gk8ptQPHL2lGlNyOJUppS1+dWqoqMG/dA+P8uyWdtgrRSeiEaGvWQ5133vu9fULln37W9e47F5GmtdYvCqrdYlt33vH9a6xl9b8aq7f6Xl99u3nefKkcSdypjo/KzdMMXTpP0xxfN18q4h0WZ0srSdfGpVGgBGiCX+YVYsPiP2ha9E12+JPPBorLZeAMAghuAAAGQprWwzTqFBC2kNROYGlxnp/aDt+IoFsqm3rKqk9+DhwuJYojhUdNqZDRVFkqP3g0OtvWKgrjQ7wyZoBSytIqP9DYXCZrNJVdXkeKkD4ZB/76YNL7R+MO/mnz9Q6fVbO56455d7a6+5/YrlLlPH3uJVaxda/d7tD3/nfu/l37prtVWENt/7tUdbB8pc/R0bnnzmQ/bQw5s7Qs613/6Xj1m9QrT8Zn3pjXeseu+e7du91sabtbmE39/y368V3vjp5EThWpVYvth+378/svlvakX2Ib8jZ2/t8Fs8a2++67NaBg/YP/vVRKK33/edZ73Lsz2VKeVQfrVUhkJqshuXLGvV/+HDUvtb3xPXLm8UYteri2+5O/6k27xBWJff9q1b6vxWlyV84w8fWJrM6bPWm3/07WtdouPJr31xWH5FKM7rD4Usteu+9Vntqfrei9/55asidwwd6dou0pJnkgwRNWY0aVUjg9EY024PNjPQFQ5AurSXi/jvKgRmmZaF69dFr75ePPKfhh/+s/Ewlw0EQAEaAJCt7Pbxen5aEsTkmRacsaLxjLKyo949wrm01mrwdsQWrVwRfKurq/eo3P3BwWDK2bQz6sn1vJ5QYnCA0ROTv1JP1F+SsZFjzib/F/Jve+b+J71WoVWuXC6r1e6pq+tp69iuFau0O2VO+wqPVXj9wmrXZgilWnfIu+2FZ8W1a6Pv3v/wHz2N8UVrCwm9cO8/Pbm3X4jivurERDG4/NpGT/EGkdXI7+Ds8S8bHnm4MZHBwUS7tKY5k8qUsi6/Y6xuoHg6mOKh/PZ37O1wfWxV6L1Hdvxh78P1A086V2Vo0xPP2j9x48JlHmsskdNiu73Sq33NYP3Y5S7tFdGbnD3Q+sSPvxOyrr3rmuWbf9yqfT1h99jn52pfaIPBKElCK85LkiGqRrRqtBqOzFySAOSH5DdVBmrP2UR7cb/1jthHPx69/c8Nr7xkIDvA3EYBGgAwt2jlJ6PRJETkcPNLjzUnJrU9356MvZX830vtw9rP7lXjjEZDNBorKLBG4j/fHzF6QEj439u+YcN2Ee9GKfzevQFhrVi+YpXH7g/1D1tE2L93W0dotVZ6bN17sjpp8axdd+2qVSH/qu33tg5NrLr8zouuWOWqW9d6zzMd7fa77/7pFf43f/em87rkxCN/tCeXry0n4G2333nXt8V/3PvIZm+/yBrkd+TsAe37g8Zr7rw9nsGu54PGcDJssXuyPpUp5VB+k/3ZE+NQx8LhSDgcHhp0QuPfuzdUe3noGZ9nIDvxJ52WiY/dcrOwK6++3VG3NJHTgN+lPRPv+oLwvniPf2jZFs+q25Ld3jeH4l8lhPxC+zJBe+widyT7KWq0XTMiSSN7rI8athsAUoi/oAhBz+fsZC+JPfas+Pxficcf5vUcmMsMkjSV7mNADquurjp4kF8DAbqoqChP5/k19MPqEycCYvoUFg5cXiblaa42Tav3pXkGrKqRUCg8fIo2r9/fqyYuvz69JEmy20v6+k4WERNDNBhVVau4GbQCJSOfpoP85rdszq/NZg+Fsr2Cnz204z8x9Pl4qdS+lRk1/obVagkG/XpkEMCETKbJDH02oei1N8QaFo+e+sk7xMKKlO0tp5Ua+uMvtpHrP6be95+JaQy7kQt+9C+Ge/7RcMr5eSQSTn8ZdXV1HR2dAkAO4qMOACBL9fX1jVNl0EJaA5E5rZoRDqdVvIhGo6OqV4mJOo5GOmrhycvWJX7FL6hOpon85rdszi8yMuHgzvGhoaMMxQFgTCdfQ6g+54QvfV186q/E8MQBmEsYggMAkKVOnDhRVFQkSanfqrQCtNagoKBAZC4cjqhqJPlz+JT97xJ1jxi1qhxFfvMb+c0bWglCS2XKNA6O5kpVCUAKIyqYvFDkjti//kT8aafhzTeSGeRFHphTKEADALJUon/owMCpJpNpaHokMVyu9ncqp63aeW+Ey1zlL/Kb38hv3ki+jNMZDkD64iPsJ2+UzqP6nGPM5tiDT4hLVhoOdYjBiyUIAHMDv/cEAGSpwsJCRVH8fv+JEyeGT9fuahO1kNZAzLbxz5unEkU2IL/5jfzmOv0ySJQo0XSis2DYF1bRW24TyDlOV+zenw/dSzkcB++wQF6iBzQAQBfFxbYJ2yRPOscaCU5OSLXkYjEum60oeeaqx/mrqo4YVXbCMUwzihqNhnT2G/RDfvMb+c11umaQKFGimUZn2vDq8/kXijOWCeSiSy+PrVlreGPDWPHsOuoATBMK0AAAXaRzhUCdzi8VRUne0KMAPXwwkGkXjcYmd2VFTBfym9/Ib67TNYMAckjkq98RyFmxr/6j4eqLxQySZavFYjGbJe0PbyXAJEQikf7+cDishsP9fX0hkTkK0AAAAAAAIIsN67UQuW5d7NxVArlr1QWxj1xr+P0zQn8Gg6GszKEoSn+/Egz2h0IhrY4mAGRI++bGao1/kSNJUllZ6bFjPZn2JaMADQAAAAAAstVQnSNxI3rlNQI5LnbldTNQgLZYzE7nvM7OTn6iBEyR9s3NiQTtdkFBgdvt7u4+1t8fTn8JXIQQAAAAAADkgJjZHLvkCoFc96E/03ukZ7NZKiyU29raqD4D00t7TmnPrKKiAu1Zlv5cFKABAAAAAEBWGtn9OXb2SmG3iynq9cX/TYZiaN1q2rzV4B8j7t9l2t4yLNpruv/q4qZzC549INLeuMxnmT2hA+YvnWu/4DZzh5LZjO6FsRUrhW4MBoPLVdbV1SUA6KOzs1N7lqXfngI0AAAAAADIPiOrz5roh/5MTFnRX9+s/ROT0PFcwa2X2f786oJnd6WMGzbfU3jTzdbW3pOT/Ioh0CsyMolZZodifPar8oty/4++H/bIIlNXXSd0M2+eQ6uOCQB60p5lZWWlaTZmDGgAwOzz+SbXCQUAAABzhlaGblwmpixW5prk+A97Xzf650ecvabNuw03N6SxkJLIV/7g/4rIxCRmmS1ydN0jgXVikpaeKfRRUGBVFIWRNwC9ac+yUEiRZe0ZF5qwMQVoAMDsczgcAgAAAHNMbN7Yv+Ae1f1Z+xuNxeaXi1mjmDa/ZXSdG1q1y7r9D0b/VZHkWCChw6Ynf2zZcEAsvyrsOtnY+OTfFzyS7Ci9QP3KfaFVJcMWpc1yv+XFFkOoJLrqxv6br4rax59loL0xJEdrL+2/8y8iLlmEdpm//lWz/S/6lx+Qnn3L4Lm0/7a/iAz0RO41vvgb84svm7zWaOMF6rob1dqS+PIf+ay8eVn/5bL04utGUaXefGf/qqrxHvF4q0i1SRkpccRiugwEbTab+/snLocBmLpIJGKxWNIpQDMEBwAAk2cwGHSKIhuQ3/xGfnOdfhkkSpRoOtHpYc2oahkTrvlitoQOmLYfiDVepa5dFvO+Je1Njnrca/rlzUXfuN+8VzFs/qV8/+vG/hEzGfwHpHe2Gr3Dh0juNd1/c9GXf2zeK2KukDa77aa7JO84swxrLw6Y//Pvbbd+x+TXtqfX2Pq6+ZGvFtz/sjGUnP7VxHIUo7bMv/6qucOqLV968u+Lbr3L3BF/AIbWFvN/31P4T48aQ4pxw/0Ff36zdfO4Y32MuYoxNikjC1J/lzD1oy5RgO4XAPQXCoW0Z1w6LekBDQDA5I3fcWMqUWQD8pvfyG+u0y+DRIkSTSc6LQydB2PFiyduN7Ql9hKROeOB/QVf/4IIhwfu7n5fW17RH5mL8QAAEABJREFUTVcNLNtsVv7lx9Gq6gmW4m3Ris7R25ZFGkVEvCy1HggtbxD+XdKzLeK87wcfvDNqVYz3X237wZFEazm67r7j64TY/o+2mx4dsZwRswjDhrtsn3nZvP2wevmC1LOMWsWTN9u+/Jy59W5tM7Tij6i98cRj34/YtaLzOtu/vm7q6FVdQriuCv3w2/3rztX2muHZm21fatGmhz2J9pZzlQef7G+URev9RR/9qvnFltCqC8Z92KlWYR1jk1Zlkp0xOrNP/aizWMxaUUwA0J/2XNOecem0pAANAAAAAACyySmXH5zq8rRS7FgxQ1o/DTfsfdnkrwovrxIeEfEolg0t8WGgQ71Gv4g11sesWhM5VlsVsxyZYEEjZhGxtfcG/pR+eznqaYhaWgwD/aOtMdey6NCq+w8Y492QS6KX3xDe/rr5/ucMfm2zdxn6Q4aBeqzWviqaHCuj9qrQtxTjxD3KU61izE3KpAAdUoQ+TCZTJBIRAPSnPde0Z1w6LSlAAwAAAACA7KZVorV/3sPCU5XprNGq6hP/7+mhu4V/82mtHt33f38lMtBr3NBi7D9g/vrVJrsw7g0Z/S+bvDeqIgtYR971t1g/c7XcWhW+5oKI3Tr2XFXqzXeJya1iWhzuEgDmDArQAAAAAAAgWw3vBH3kyCQK0NMgPgD0LlFxQXjtsphVGFzxHtDxwShq5Xgv4KEBH7QbEw4+bB05S8cfLM/ujl7+l9qi0mofUuJducepCHe8LrUq6hf+48RtDdo9w4sHzC+9JaZXppuU0hEK0MAcQgEaAAAAAABkn1PG3zB4D8/OGPzeFqlDRNbdrXzl3Pjd1gWmzf8obT8QaqyK1JZYN9xvfdIadh2RntxqFMk6cq+htcUYHwHjgKE/ZGx93eRaIOz1kcb4X3X5AuuL9yZm6ZV++VV5e0Pf2r8ce5Zk+/sH2z9ntJ+rNo492IV9fswaMm1vMfirxN7fWn/5+uAmTR97hpuU0pHDApgp9rNv+vxH5+947FdP78j0cpmYHmkNdQQAwKw7fvy4z+fr6+sTAAAAmFOS42/EYob3WsSUxQwGYcysGGLQysH+BZFVg52vPedEPMK0ucUgqsLfuk9ZdcD65XW2T99jsjdELYkG/hbr5662/fnVRd/4rVH0Sj+7Xbtt+/qjxnin4QXqt/6jb22vJT7L7fLmkv6vfD9+VcAxZ0m0X3V4oP3eZcpP/7+wZ+yasufPlC/cIP77dvuZ5fab7jXULhvYpOmU4Sal1PKOwCyxn/2N9e3epD1vP/3d6+umbZAV69Jbf/HYT26q02PUlilsgLWk8pKP3nrrmsrEUWqt+8zTA4//7R+ebxeYCQZJmv6XIiAnVFdXHTzIr34AXVRUlB8+7J2w2dBFrv1+n0hDf39/IBAoLi62WMZ787LbHckbBoNBTDeTyRQM+lV1+kf8kyTJZrNzyZTZRX7zG/nNdfplEMCETCaz0EH02htiDYtHTx3V8Tl5N1mDfn2DeP41MTXGA/tFYmBoMY32tphEvDd0BrP4Dxi9IuqpSnfwCq29vyTqSW8VocPGjlAGC5+cjDZplLVnG3a8G4tl8NZZV1fX0dE5YTOPx71nzx6BsWkF6McfvOSNz1z/kyNr/uGnP7215Klbr//y+qHLZ9or6+aH2vccCQ2bxTp/6dl1ov3tHe3Dp57a0n72d59+8Oz1t17/3bdDI1ZZubTeemTHyIUKq72uvip0YEd7Gr2S09yqsTbgVNaln3/6sZt2fObDX97on2hFGEeaT0x6QAMAcoZWdy4sLNTK0AIAAABz0NtbhL9XTI1Wep7m6rOmdllm1WeNvSpam0mBWGuffqnXuiCzhU9ORps0XOchseNdgdnm37P+V0/t6LWW2K2JY8U6//zPP/b2extfeUX78+Bnzk50DrbW3fSLjXvefvoXv3ha+98vbl1qTd3Sfv53N3r3/s9fL1twzt/9T4fX613/jfhka+X1P1y/572Nzz+96e2ND966NLHM+Vf+5O32HW9v3PbKK69s2/jYwJrGkO5WjbEB8y/5yduD3Z0vmS8mXtG2TZve26Nt6tn0jZ5OFKABALnEaDRGo1EBAACAuWBkb+j4r9u2bhbIda0t0/9DRWTCKpfUn3PJ9bd+90efP1vsWL8j0d/XWn/9P3ym/u0vX1x3xpU/OHD257/8kTqrVpU958qz7eu/fPHZS1dc+bkHDwh7SeqW/o3fON9V++Gftxx+6/982ONyuS757tt+YdXWU3nkV7eeXXfGxf/cfvbnP39J5eD3IqG3//nDZ5zxiV/51/z1X6+pHHtT092q1Bsgjqz//Nkuz+ovvXx4oi7R8RUt3f3P161e/YmfH1nz5cSKMF24CCEAIHspinL8+PFTpx87dsxut0vS7L+LGQyGWCymRxTZgPzmN/Kb6/TLIFGiRNOJzppf/UJceoVATtOSiNllrVpz6zfXVFWJt/7Pp7781J5EbdZqr5ovW62XfP67Z4v58+USUSdrZeLeHW/sFt/87tNPX7n++eefeuypjUfiYx6maJlS6Mj6H3xDuURreaU93tJapdWv2+OR3t1v7Gj3Hzny4A9+2FsyzoAX6W/VVHeJtiLR/tjGt/fssa7fceDT59dN9+U75zQK0ACA7BUOh1NO1z4LaaFsKECP/6lsKlFkA/Kb36Yxv4WFhRaLua+PMaD1pe1kbVf7/QNDNer3DCVKlGg60dli+P3vYjveFUvPFMhRWzZqSRSYVaHell997tb1lzz40EerSob381WO7H5j/XqtHrz++Qd7dx/Q6sKhHb+46eynl15y5U0fvfUbj3/m+i9ff+tjR1K2TMV+/nef/sUl7Y/95Kn1SlXlJWtOGbLFv+Ppn+wQE0hvq/YwbHMWYwgOAAAAYJK0b8Kqq2tstmKzWSorm2c0cnatC23HOp3ztJ2s7erq6ups+AISwGz6ztcEctd3vymQFXrffuzBt6yX/PWV9ckSdMh/4IgokUM71q9/40jJ2efHOysLa+Uln/nGX5+trH/wG1/6xtO75fl1WsE6ZcvkMpSQPF8zUNS2llRVzg/tfurBp55ev2Nyw7env1WpNmAcSm9I2OefrL8nVlR5/tn1dnvV0qXzlSN7FIFpwykyACAHGAyG0tJSu50LQQDILk6nq7fX39PTe+xYr3bDZisS0IG2Y30+v7aTtV3d2xvQdrsAMAcZBsYNNqx/QWzbKpCLXn7B8MaG5E2DgYGgZ1loz/MPru9d+ulb1yQuzhfa/fQPfrH77O++8t7b2x7/xpqS3vjAGKEjB47Mv+mhTR1e796HLjnyqx8+tsOfumWcf/djDz515JKHtnV49zx9a501dOStpzaGLvnp8xs3Pv+jK+Ol44yLuulvVaoNEPbzv7HR6+3Y9KNLF9R/+vH3vN6N3z0/8aEy1L7+50+3r/nptsHrFSZWtKP+u6/s3fvKN+e//ZMf/p4u1dPIIEkWAcxJ1dVVBw92CQA6qKgoP3zYO2Gzod91+v2+lA0CgUB/f78YLEBHIhGt8JAMFRYWFhQUpJzLbnckb+hxUmsymYJBv6qqYrpJkmSz2bXHKDB7yG9+m8b8lpU56+vrXa7527a9pVVFh00v1crQQgdy+dJzlpcHt7/+Tld6n9wkh8epdnQFxSTZqs/yBHe83z39z4bJKCmxHz3aM3R33rySgwcPCgAzyGQyCx1Er70h1rB49NThQ38M3U7cMPz4ByLxZhq78GLxyNOiiK/9csrRbrH2bEPnwAu4dq4ejWbwNlNXV9fR0TlhM4/HvWfPHgFgRqT5xOTHawCAHKCVqnt6ehhUF0A2WLSotqrqtP3797W0NBcX22XZqijxHjLaDd1epuRyj61j02ZfvDB8ztJySe3a2WGrLxeqGtyzY38wOVHp2rFHLF7qFMHufb7yi69cInZu+mOLUr0kEXpnf7IYLTnr6qRun8NpCTsaFpWKQOeOlm5Hfbmsdu/Z0TFQsLZVL13iUrbG17aqfmSb/VJ1nU2SRMc7O7rlgfW2+ZxNyWZv7ejSo2St7djh+zkSiQoAc4TBIFK+tB7pEo8/JG79jFYaF8gJ4bD4i+uHqs8A5hSG4AAA5AaqzwCywfz5C047reaPf1yvFaCPHz/e3e0tKSkuLS2ZN6/E4bAHApPucTwhVShBn084naJrT5dwLiiUtUKzT3Y6ZCE7yx1CUSTbvIVO0fH+jv3dxzt2vNOy/fXN7wdLB0K2wSu5S7LDJsuybV5hkRSMb7DNYQv7fIpc6XEOXe09uH/Hzh4hWSV5dJuF852yrzuoLUYaWq+9xD7UTJ/+LdrCS0rs2k7WdrW2n7XdLgDMSSN+33Zgv/j90wK54u//l+GtzUP3GH8DmFMoQAMAspfVmvriEUajcawQAOjH6XSdeebyV175w9AUVVX3798fDAbCYbW7+5huX5WpQcVRf+GfXba0pE+7sbyuVAlG4jXpwWhQkSRJ8fUeU+Tqsy5YXWeTVEVUnrOqrqhvIBQcHLlDVRTZU+2RldDgiDDm0rqlHqdj2IX9JOfiVauXnbX6TI88uk1/b7fqrK5z24att/d4v9CXtmOPHj2m7WRtV+/bt0+PcXIA5B6tgvn2m2LrZoHs939+YHj0QQFgrmIIDgBA9rJYLGVlZQIAssOFF1707LO/O3X6iRMnjEZdz6vV7h1/eGlH8vbhwRuHtP/2J65noex4/fXktI7BG0JsfrYj8f/XD49e1FCbfYMTW0av7v0//Nf7I6cNtpEcddISSWkPqsMX9cEhob/+/rC2qwWAvJdy2I3BiQaD4eS3fQajeO634oM2cf0nhMRYHFmpv1/ceavh6SeGT9O1+3MkEjGZTFx4A5gB6T/XKEADAAAAEzvzzLPef38nfW9V357Nz3NxJwCzKV6DFvHfxIloNF6YbnlH9BwVn7hV2O0CWaWrU3xqneHtN4dP03vwDe3bSqvVyheWwAzQnmv9/Wn9EI4CNAAAkzeiD860RpENyG9+yyiDRqPx9NOX/PrX/5XOvJgZ+j1DiRIlmk50WhjeeNWw/a1Tp6derzZxsKudof2D2JP/NSL60APijs+Jm24VFovArNNqUv9+n/jRdw29PjGzwuGwxWKhAA3MAK0AHQ6n1TmDAjQAAJM3/qeyqUSRDchvfssog2ecsXTHjpY058XM0O8ZSpQo0XSi08JwtFscFSnXPcGMfX2io3301LvujP1/94hvfU989OOCa9zNlljs9J3vXrj+9w6/z3DH7do3uIYE7f+JLzUMyR7Qg/2gY8NuDzCMkbuHH35YpEErQJtMjMcCzATtudbfH06nJQVoAAAAYAJ1dQ3PPvu0AADMiHQ6X6dsY2j/QNxxc+z//EBc/zFx5TVi8RkCM6XM27VoV+vpre8sONIZrzsPlp5PKTqPZ+oDdPT1hcrKHAUFBX3atxQAdFNYWGi1WoPBtH7lQAEaAAAAGI/HU3nkyGFGfwaAbDNWndqw412h/XVBeYEAABAASURBVPvuN2KeKnH19aJ+sfBUCu12RZUoLhaYDpZQqNjfU9wb/1fmPVy7670Sv88w1Nt5NC1ZRjFYXx5eZTbo0Ff92DGf2+1ua2sTAHSjPcsOHuxKszEFaAAAAGA8NTWL9u7lsnsAkI0mGMa644D42U/EHPZ3f/d5MTUTFoiNRuNAy8G689DE8avPBt0GGdeW2t19TKuOdXZ2CgA60J5fR44cTb89BWgAwOyz2x0CALKSxWKx2WyHDh0UADCHRSJpjfKJbJMYeVkXwwrTsWGDbMTvJqrPscSU2PCxnrVyc7LonJw4dCPVMqcqOS7tokWLtBo0Y3EA06iwsDBZfQ6HM3hfoAANAJg1Bj0vra7Hr/kAzEGVlVXd3d0CAIAcNNQ9WbtpMptMBhGNRCORyHSdgg+VnketzmAwShazlOgTLWJRNaxGtWhikohF1HB8A/Q+Xddq0IcOHS4rKwuFFO0hhxK0GwJAhkwmkzUheSP9kTeGUIAGAMwmnWrQVJ8BTJeFCysYfwMAkKNOnhVLcomjMBbqj5rMFmM44AuEomJy4ss0Wuwlhf29PiWaYmCN+F+pML66/nBiJRFDVO2PGiSLRTZbLFZDX0/PiUiqxerg6NEeWbaazZbCwkKLxaKVzwSADGnf3PTHqeFwOM2rDo5CARoAMMsoFgPIWtoLlFaAfu21DQIAgBw0rAe0QUT7jx8/HhEGi91RYDGF+xO9QAwms9UiCbU/FB7oF20wW62SIRYOhdSBfiLxNmZTLKK1icbjBYWyxWoxm+0l1qgaOtHXnygzDxuIIzHCRqT/eCCYvIBvckq477iqhO1mmxj+EcBotsoWsyHSr8SXbrLKJjWkmmSrCPWpkmyOKKGp9llWlJD2TwCYPUYBAAAAIBW3u+KDD/YLAAByXeICgfERobWCr2QcrCxbiktLCrXKkLGwpLTYEo9a7fNKCiSt5lxUOq/YahQGo8U+z2EzGw1SYWlZiRwfxSMcDkejsZga7g+HI9F4lTvOMHTNQZGsRouhmwNrG5okBqvPWjG8tKTAEI0aCkpK7ZZ41+qCArPJLBcVFZgls1wgUbYC8gE9oAEAmLwJLrw+hSiyAfnNb+lkcOHChV7vkUznxczQ7xlKlCjRbI4iIyd7QBuNkmx3ue1CREN+X69qiF+f0CxbTdG++M5Wo6YC2XJcDYeDPT0mySyZ1JhJliRj2CCbRShwXFGFEg5LhpghPo60qsaEJRIO9w+O4zH8R43J20ap0OEsiF9+MBIO9Pr7Y6l+9ShZpVhf4IS2cFUrfVslcUKNGk2SSYTDMe1/xmhksgOFAMgmFKABAJi88T8dTSWKbEB+81s6GXS73Tt3vpfpvJgZ+j1DiRIlms1RZGRYXdgQCx8/2qtYShzmaCQ2ENAK1GarVcSrvP1Kf9RgMMWHijbErxJolIxGNd5j2aDVsJPtY5HBGQeH2hg1lt7J+9q3CBHF7wv0x5ITBztBj9q8xA/zE/nW0h5vFq84Wy2SVts2SGazUE9QgAbyAb9lAAAAAFIoLi6ORKLHjx8XAADkumTJOKaGFNVcKA/0RtQqypFwXzAQCJzoj8a0MrPJIkuR4/5AMHhcUWPJgTSiwmQ2x29JhXa7bEqUnRMh48lq87DBNwaG3xh9ccLB2/Fqs2GwFhXT6s1GSYq3lqR4d+dYLKLGTJIxoqoRY3zY6SjfRgD5gB7QAAAAQArl5e6urk4BAEDOGt4lOV4xNhiiob5wYXGRHPKHokK7E7Hbna54YTh83Ncnomp/xGYrKYlo7Y1GEdUCar+iFtidTm0Z0f5A78D1BtVQxOwocxWq/cf9fiUycl1CjB7r+WRU7QsZHKWuolg0fMLX2xc63i9rG2AXMVXxB7XlGCJRQ3zojYhB+1+EETiA/EABGgAAAEjB6XRxBUIAQE47WRSO9PX6EhNEONBzbDAUCwd7jwWHtY4q/mPKyAVElUCPMnqJsX5/95HBCSkG4oj2+XpO2YYE9URP94mT0/sDPd2BYeH4gr2JWz3ePgEgPzAEBwAAAJDCwoUVKa9ACADAHGQYw6kNRs011tIEgDmDHtAAAADAaKWl8wKBQDgcFgAA5Cy967zjLJ/SM4Ah01mAtlgsF1ywpr6+LvlqsmnT5nffbRYAAABArpk/f8GRI4cFAABzydSrw+MvgeozMDdN5xAcZ5+94sorP2wyTUtRWyp2uasWlsrpLkxedOXf/NP3vnLzOaV06gYAAMAUzZtXevhwlwAAIJcZMiQma8IlTHH5AHLadFZra2pqWlpaHnroYTE10sLzbr79hqX25L1j7//u0Udeb1cmnM0sFZgLZAEAAABMVUVF5ZYtbwoAADDSJOrIlJ6BOc4gSRYxTT75yZtjMfHww4+cGvriF//+tdde27Jl68RLkUrPufXvPrGw7TcPPvtOj1R78V/cvEp96d9+/sohVQDTqrq6SgAAAAAA8kJMK0kgm1B3BpA0Q+NVvPfeex/72DpJkjZu3DRBU8m2cF5BuGfv3kM9iir+9Nrzvw8vDIQHQlVnnHnW0tMXFovAoT+989bb7x1S4h2mV/3FDatcBWYRDvf86flfP/+nYKK1XHXBxz9Se2TTO0rtWQ3zhXfH5j9u/lMPZWwMd/AgP60FAAAAgPxBGTobUHoGMJzJaDSJaXLmmU3a3+bmllNDe/bstVgsV1754ePHj7e3d4y7GFPx6Wc31Z1W0rv7vY6gqhw9sGf/4RPReKF57e2fvXF5Scjr7TUubFqz5sz5R1reO6yIYs+yJZ4is7XYvaAk1Lp1++HkcB1S+aor/2z5oiX1pWqgv7S+afm5Dda92ylBY4jDURIIBAUAAAAAIF9My4jGmAT2PICx6NUDevnys847b+WoiceOHbv++usWLFjw1FNPjzmn2vPOM8+fsfCGpTd+4fsfOfbBjtd///ybbQGtaixJgfde+83zr29uCwhRes5td33CXVsqvdujHNr80L9tFnLVNZ/7X2ePXlrY+9LP/u8rh1Rp4Yf+9m+vPOOshS+2tU08nDQAAAAAAMhxp1ZC6R89XagyA0jfDA3BkaS9zmuv9SaTcfxmqvfNR3584IxzLjjnjEW1515752nz//1nT/0poBx45y21tvbMK6+ZZxayy1UgzAVmMYG+niPx4rVQj7z30u/l+YEA/Z8BAAAAAJibKJsCwMzTqwC9ffs72r/hU6666iO1tbVPPfX0xMNAa/XiQOe7rzzx7iui9Iw//9tPn33xGa/vfUe+7K/++pKFPe+/1+adRBlZ9b73+v+8JwAAAAAAAAAAM2SGekB/5CNXfuhDa3/zm99u3vzmBE1LG2/4xMUF7/z68c1ercwc6OkMhM+SSyVpXu3pC8XBlx598JVObXrxmaVLF1cJAAAAAAAAAEC2mqEC9FlnnfnrXz+xdetbEzcN9PTJ7tWXXXNMfb0tULBw1XkV5iOv/alH7QsoqtlVtbBU7lEXnnnZxYsKRLIftFxatXB+gSS5SmWzVHzaotOVQDjgPXCoTwAAAAAAAAAAZs90FqAjkehY4zt/73v3iDSpnS89+Kj55hsu+cTtl2h3+w5tffzR37cpqnjv9y/+6dbrPv4PS7Wpx95/55C/Yn68vVx12c23nztvYG77hR//qwuFOPLKvff+UQAAAAAAAAAAZo9BkiximqxeveojH7ny4MGDybubNm1+991mMVmSXDq/OHzEGxwx3rNc6ponAkd6FC4miCmrrq46eLBLAAAAAAAAANDHdPaAfvvtbQUFBfX1ddNyVVlV6TmknDJV6fEeEgAAAAAAAACA7DedPaCB3EIP6Mm5/gJrvyp+vzkkkJpkc9hUn08RyJRkczqL1W6vYnPJSie7EAAAAACS5PKmFZWB1u37fIwJkMTnx1wyQxchBPKGZKteecUla5o8sm//hv9+ZuPulK/9tvorbrii3mEWas++F598bk8wRZO6K65a0vnC881Tf/Own3Xb975Q98I/fefZtpB10brv/eizy+3JSGjvk9/54s82h1JN9Atr7WW3ffbmD9Xahbf1mf/48ZObu8cvKn94peXX/zjvqdcUiyR+9vclN36zZ+ufwkJXknPFdTecXyWbE/fCYV/z7379avuY7yu2mnMb5X3bdnbP4huyXHnZHX91buC5+361ZbzNmPZNtdZe/b3//YXBJGv8rfd9/YtP7hSei26+6+Yral2iY/sTWpa3B0S2stVfectaOSi5bEIozb9+eCODLQFAbpArV6+7aknfxt/+bqLTmmx4p55pUzjlm4u7CwByWbxccOn5jW5Z7els3vjatvZ4JUByVK9cOzjx1Ve2dU6uThovMlwkrf/VFn3fE1I8hBGfytW+Q1t/95utnVnwzpQHnx8lR93KtSsbXLIIdLZu2bRNz+8WJnNSMY1lKwrQQGYkx4p1H18rNj35s9+L+svXXf+R4AO/3pbiqah0vr3+uTaba8Xla13FqZ9mUoF7obuvQAifmJriVZ/9yu2e7V/c0BYvH1vtdbUe/+Yf3/dHbzzo79gbGmOi67y7//e3lrf++J4vttov/8Ld//tH4o7PPNLaP86atOqz/SNdf/vRwn976kSF07j1586FNx4R+pJcbofS+vwLbX3xe6rS4x3n3VoqbTx3jS3QurM7KGaN0v7Kf/5su+od/2Vdh021emo9Yvt9P36hI6RVoz929812a0jYz7vr3350ecf93/nadvvHvnL3v/1IfOpzT+7tF1lJad/05JO+bp/kcNsm2oEAgOwhuRqXVZY61KYaW/P2cc9rsuKdeqZN/pRvTu4uAMhdcvUVn/54TftLv3uy03betdffdK36wKPNiufSm26IT3ysU268+PqbbhD/mbKGMBFJ9Gz7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', 'media_type': 'image/png'}}]
> ```

## 🤖 Claude *(22:50:46)*


## 🤖 Claude *(22:50:49)*

O screenshot confirma visualmente: canvas saudável (29 nós), **mcoCoins como texto limpo** ("4559 mcoCoins" no topo com Coins gold, "~180 mcoCoins" nas receitas — sem `💎`), MIV intacto (void/cyan/gold). Cadeia material da Lei 1 completa: grep-zero + tsc 0 + build 0 + 3 revisores clean + Vision APROVADO + gate Canvas Studio exit 0.

Commito a cauda de brand como milestone (trabalho verificado + deployado, seguindo o ritmo granular do projeto):

## 🤖 Claude *(22:51:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add src/hooks/useCampaigns.ts src/pages/CampaignWizard.tsx \\\n  src/hooks/useSocialAccounts.ts src/pages/SocialAccountsPage.tsx \\\n  src/components/spaces/SpaceIcon.tsx src/components/spaces/SpaceNodeCard.tsx \\\n  src/components/spaces/ParamHUD.tsx src/lib/spaces-schema.ts \\\n  src/components/canvas/nodes/GenerateImageNode.tsx src/components/canvas/nodes/ImageToVideoNode.tsx \\\n  src/components/canvas/nodes/SceneComposeNode.tsx src/components/canvas/nodes/StyleTransferNode.tsx \\\n  src/components/canvas/RightPanel/inspectors/CharacterReferenceInspector.tsx \\\n  src/components/canvas/nodes/AvatarIdentityNode.tsx src/components/orchestrator/nodes/AgentNode.tsx \\\n  src/hooks/useCrewOverlay.ts src/hooks/useConstellationSigma.ts src/components/orchestrator/ConstellationMatrix.tsx\ngit commit -q -m \"feat(brand): fecha a cauda de brand \u2014 pictogramas \u2192 lucide/MIV nas superf\u00edcies cross-file\n\nFecha os deferidos honestos do brand-100: templates de campanha, \u00edcones sociais,\nn\u00f3s de Space, glyphs de canvas e o avatar do crew \u2014 as \u00faltimas superf\u00edcies que\nainda renderizavam emoji decorativo.\n\n- Campanha: templates \ud83d\ude80\ud83c\udf81\ud83d\udce3\ud83d\udcac \u2192 lucide-names + componente TemplateIcon no wizard\n- Social: \u00edcones de plataforma vestigiais limpos; PlatformGlyph cai em Globe (sem emoji)\n- Spaces: novo SpaceIcon (sprite-name\u2192lucide) fecha bug real \u2014 SpaceNodeCard/ParamHUD\n  renderizavam o nome-sprite/\u2728 como texto cru; default do schema \u2728\u2192sparkles\n- Canvas/orquestrador: \ud83d\udc8e\u2192mco, \ud83d\udcf7\u2192Camera, \u26a1\u2192Zap em 7 n\u00f3s/inspectors\n- Crew: fallback \ud83e\udd16\u2192bot + removido o prefixo texto-avatar de 2 render sites do sigma\n  (label + tooltip) \u2014 o avatar nunca passava pelo AgentAvatar lucide (anticorpo cross-file)\n\nVerificado: tsc 0 \u00b7 build 0 (rollup limpa o trap de brand-icon lucide) \u00b7 grep-zero de\npictogramas \u00b7 3 revisores adversariais clean \u00b7 gate Canvas Studio E2E 1920\u00d71080 Vision-APROVADO.\"\ngit log --oneline -1",
  "description": "Commit brand tail milestone"
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
> [90m7:51PM[0m [32mINF[0m 1 commits scanned.
> [90m7:51PM[0m [32mINF[0m scan completed in 18.2ms
> [90m7:51PM[0m [32mINF[0m no leaks found
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.65 seconds)
> ✔️ e2e-output-tripwire (0.14 seconds)
> ✔️ secret-scan (0.42 seconds)
> ✔️ gitleaks-staged (0.43 seconds)
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpost-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m╯[m
> ┃  mesh-reingest ❯ 
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.00 seconds)
> ✔️ mesh-reingest (0.00 seconds)
> 6af3181 feat(brand): fecha a cauda de brand — pictogramas → lucide/MIV nas superfícies cross-file
> ```

## 🤖 Claude *(22:51:52)*


## 🤖 Claude *(22:51:57)*

Committed **`6af3181`** — lefthook verde (gitleaks: no leaks · secret-scan · e2e-tripwire), mesh-reingest disparado. 

**Item 1 (cauda de brand) — FECHADO, deployado e verificado.** Isso encerra o deferido honesto "não-100% literal" dos 2 últimos seals: agora não há pictograma decorativo renderizado em nenhuma superfície de produto (confirmado por grep-zero + 3 revisores adversariais + Vision-QA).

Antes de mergulhar no próximo item grande, preciso da direção do Sovereign — os itens 2 e 3 são esforços multi-fase de perfis muito diferentes, e o item 2 tem partes que **eu não consigo destravar sozinho** (ação Sovereign). A escolha muda horas de trabalho:

## 🤖 Claude *(22:52:05)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "Item 1 (cauda de brand) fechado. Qual frente atacar agora?",
      "header": "Pr\u00f3xima frente",
      "multiSelect": false,
      "options": [
        {
          "label": "Unified Canvas 3.5-3.10",
          "description": "Fases restantes do Phase Epsilon V9 (/dashboard/universe). Puro c\u00f3digo, BoK j\u00e1 selada (PR-025), ZERO gate Sovereign \u2014 100% aut\u00f4nomo. 3.5 sinapses reais c\u00f3digo\u2194mem\u00f3ria (mcorch_edges), 3.6 fly-to, 3.7 perf (~30s query), 3.8 poda squad-color, 3.9 paridade/cutover, 3.10 seal. Recomendado por ser destrav\u00e1vel agora."
        },
        {
          "label": "Viral Autopilot \u2014 v\u00eddeo",
          "description": "Revenue-critical, mas os pr\u00f3ximos passos s\u00e3o majoritariamente Sovereign-gated: editor HyperFrames Studio exige NOVO BoK (deepsearch\u2192suite) + DNS studio.mcorch.com (Sovereign); 1\u00ba ciclo pago de v\u00eddeo exige GO com dinheiro real; postback ML + publish TikTok/IG/YT exigem OAuth/App Review. Eu preparo o que der, mas travo nos gates."
        },
        {
          "label": "Outro loose-end de brand",
          "description": "Varredura fina extra: emoji em superf\u00edcies internas/tooling (console.logs de testes, BlogEditor templates se houver) ou paletas categ\u00f3ricas data-viz remanescentes. Menor leverage, mas 100% aut\u00f4nomo e r\u00e1pido."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "Item 1 (cauda de brand) fechado. Qual frente atacar agora?"="Unified Canvas 3.5 - 3.10 para ficar 100% depois Viral Autopilot - Video". You can now continue with these answers in mind.
> ```

## 🤖 Claude *(22:55:58)*


## 🤖 Claude *(22:56:01)*

Direção do Sovereign: **Unified Canvas 3.5-3.10 primeiro (chegar a 100%), depois Viral Autopilot - Vídeo.** 

A memória (`[[project_unified_sensorial_canvas]]`) indica que **3.5 (sinapses) e 3.6 (fly-to) já estão LIVE** (2026-07-01) — restam 3.7 perf · 3.8 poda · 3.9 paridade/cutover · 3.10 seal. Mas o HANDOFF que li era snapshot mais antigo. Não confio em doc stale (Lei 1) — verifico o estado real pelo plano vivo e pelo código.

## 🤖 Claude *(22:56:03)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Unified Canvas 3.5-3.10",
  "summary": "Phase Epsilon V9 \u2014 fechar as fases restantes (perf/poda/paridade/cutover/seal) rumo a 100%"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Unified Canvas 3.5-3.10". Continue your current work.'}]
> ```

## 🤖 Claude *(22:56:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== plan file ===\"; ls -la .claude/context/unified-core-sensorial-canvas-plan.md 2>/dev/null && wc -l .claude/context/unified-core-sensorial-canvas-plan.md\necho \"\"; echo \"=== unified canvas files present ===\"; ls -la src/store/useUnifiedCanvasStore.ts src/hooks/useSynapses.ts src/pages/UnifiedCanvasPage.tsx 2>/dev/null\necho \"\"; echo \"=== canvas layers ===\"; ls -la src/components/canvas-universe/ 2>/dev/null || find src -path '*CodeNetworkLayer*' -o -path '*MemoryNetworkLayer*' 2>/dev/null | head\necho \"\"; echo \"=== route registered? ===\"; python3 -c \"import subprocess; print(subprocess.run(['grep','-rn','universe','src/App.tsx'],capture_output=True,text=True).stdout)\"",
  "description": "Locate Unified Canvas plan + files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === plan file ===
> -rw-rw-r-- 1 ubuntu ubuntu 6658 Jun 17 12:29 .claude/context/unified-core-sensorial-canvas-plan.md
> 83 .claude/context/unified-core-sensorial-canvas-plan.md
> 
> === unified canvas files present ===
> -rw-rw-r-- 1 ubuntu ubuntu  3467 Jul  1 23:34 src/hooks/useSynapses.ts
> -rw-rw-r-- 1 ubuntu ubuntu 14357 Jul  4 00:35 src/pages/UnifiedCanvasPage.tsx
> -rw-rw-r-- 1 ubuntu ubuntu  2529 Jul  2 00:20 src/store/useUnifiedCanvasStore.ts
> 
> === canvas layers ===
> src/components/universe/MemoryNetworkLayer.tsx
> src/components/universe/CodeNetworkLayer.tsx
> 
> === route registered? ===
> 133:                <Route path="universe" element={<UnifiedCanvasPage />} />
> ```

## 🤖 Claude *(22:56:13)*


## 🤖 Claude *(22:56:14)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/unified-core-sensorial-canvas-plan.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Plano — Unified Core Sensorial Canvas (Phase Epsilon V9 Consolidation)
> 2	
> 3	> Plano de trabalho para fundir **Core-Fable (CoreFablePage)** + **Matrix (ConstellationMatrix)** + **Memória (MemoryPage)** em um canvas 3D soberano único, herdando o *Unified Relativistic Black Hole & Cymatics Visualizer*.
> 4	> Status: **PLANO** (Fase 1 auditoria fechada · implementação gated). Operator=MCORCH Agent · Reviewer/Owner=Sovereign.
> 5	> Criado 2026-06-17. Fonte da auditoria: nó mesh `a576216e` não — ver auditoria de clusters desta sessão.
> 6	
> 7	---
> 8	
> 9	## 0. Veredito da Auditoria (Fase 1 — fechada, material)
> 10	
> 11	| Sistema | Status | Prova |
> 12	|---|---|---|
> 13	| **Louvain clustering** | ✅ REAL/VIVO | `useConstellationSigma.ts:227` `louvain(g,{resolution:1.0})`; deps `graphology-communities-louvain@2.0.2` + FA2 `0.10.1`; input **8560 nós / 8816 arestas** vivos |
> 14	| **Squad-territory coloring** | ⚠️ MORTO + heurístico | `crew_module_ownership` = **0 linhas**; fallback sempre cai no Louvain (`:247`); atribuição = `inferSquad` keyword-match (`useCrewOverlay.ts:34`) |
> 15	| **Mocks cosméticos** | fora do motor | `LandingConstellation:7` (decorativo) · `CrewGraph:11 SQUAD_META` (crew 3D, página diferente) |
> 16	
> 17	**Número canônico do grafo:** 8816 arestas (não "1801" — esse era endpoints de import não-sincronizados, `HANDOFF.md:7396`).
> 18	
> 19	## Decisão B (Sovereign delegou → Agent decidiu)
> 20	**PODAR:** Louvain = esquema oficial de cor da Rede de Código. Squad-coloring dormante **não migra** pro canvas novo. Overlay de agente (`crew_agents`, vivo) sobrevive. `OTD-SQUAD-OWNERSHIP-REVIVAL` registra a futura posse a partir de sinal REAL (telemetria), não keyword.
> 21	
> 22	---
> 23	
> 24	## 1. Realidade dos motores (o eixo do refactor)
> 25	
> 26	| Página | Motor | Componente |
> 27	|---|---|---|
> 28	| Matrix | **Sigma.js 2D** (`sigma@3.0.2`) | `ConstellationMatrix.tsx` + `useConstellationSigma` (graphology+louvain) |
> 29	| Core-Fable | **R3F/Three.js 3D** | `MegaBrainVisualizer.tsx` (Schwarzschild + cymatics raymarch) |
> 30	| Memória | React/DOM + d3 widget | `MemoryPage.tsx` + `MemoryGraphWidget` |
> 31	
> 32	**Sigma 2D não compõe numa cena Three 3D.** Estratégia de reconciliação:
> 33	- **graphology permanece o CÉREBRO** (modelo de grafo + `louvain` + `forceAtlas2` para seed de layout) — é renderer-agnóstico.
> 34	- **O CORPO migra de Sigma → R3F** (rede de código renderizada nativamente em Three).
> 35	- **Posições 3D:** FA2 é 2D → projetar no **plano equatorial** (x,z) ao redor do buraco negro com jitter-y por comunidade/stability (≈ "nós orbitando o disco de acreção"). Rede de Memória = nuvem 3D mais orgânica.
> 36	
> 37	**Realidade de performance (Lei 1):** 8560 nós + 8816 arestas em R3F **não** batem <50ms como meshes individuais. Obrigatório **InstancedMesh** (nós) + `LineSegments`/BufferGeometry batched (arestas). Sigma fazia esse batching nativo; em R3F é explícito. Gate de perf no passo 3.7.
> 38	
> 39	---
> 40	
> 41	## 2. Arquitetura de dados (contexto unificado do visualizador)
> 42	
> 43	Novo store/contexto global `useUnifiedCanvas` (Zustand — padrão do projeto) que hospeda:
> 44	- `codeGraph` (graphology Graph — de `useConstellationSigma`, compute extraído p/ selector renderer-agnóstico)
> 45	- `memoryNodes`/`memoryEdges` (`McorchNode[]`/`McorchEdge[]` — de `useMcorchMemory`)
> 46	- `selection` + `cameraTarget` (fly-to) + `viewMode` (`matrix` | `memory` | `universe`)
> 47	- `synapseEdges` (acoplamento inter-rede)
> 48	
> 49	Hooks a unificar: `useConstellationSigma` (código) + `useMcorchMemory` (pensamento) + `useNodeIntelligence` (análise on-select).
> 50	
> 51	**Sinapses inter-rede (Lei 1 — sem fabricar):** as arestas Memória→Código **devem** vir de relação REAL:
> 52	- Fase A: arestas já existentes em `mcorch_edges` que cruzam a partição AST↔knowledge (`DERIVES_FROM`/`REQUIRES`/`observes`).
> 53	- Fase B (OTD): similaridade por embedding (768d cosine) como enriquecimento. **Nunca** linha decorativa sem lastro.
> 54	
> 55	---
> 56	
> 57	## 3. Ordem de Trabalho (commits granulares, não-quebrante)
> 58	
> 59	### Fase 2 — Plano & Gate (agora)
> 60	- **2.0** ✅ Auditoria de clusters (fechada, material).
> 61	- **2.1** ✅ Decisão B (podar) registrada + `OTD-SQUAD-OWNERSHIP-REVIVAL`.
> 62	- **2.2** 🚦 **GATE (decisão Sovereign):** emenda BoK em `docs/bok/mcorch-constellation/` (PRD/FRD/SDD: Unified Sensorial Canvas) **OU** override consciente (precedente viralmind, débito selado no `/handoff`).
> 63	- **2.3** Este plano selado (nó mesh + commit).
> 64	
> 65	### Fase 3 — Implementação (pós-gate · 1 commit por passo · 3 páginas legadas PRESERVADAS)
> 66	- **3.1 Scaffold não-quebrante:** nova rota `/dashboard/universe` → `UnifiedCanvasPage` (vazia + shell 72/28). KEEP `constellation/matrix`, `constellation/memory`, `core-fable`. Novo `useUnifiedCanvas`. Zero deleção.
> 67	- **3.2 Rede de Código em R3F:** extrair o build graphology+louvain de `useConstellationSigma` p/ selector puro; renderizar InstancedMesh no plano equatorial; cor = Louvain (`COMMUNITY_PALETTE`).
> 68	- **3.3 Rede de Memória em R3F:** nós de conhecimento como nuvem orgânica + anéis cymatics por node_type (Ciano/Alfa · Violeta/Gama · Ouro/Escalar); feed `useMcorchMemory`.
> 69	- **3.4 Herdar o Black Hole:** montar `MegaBrainVisualizer` como fundo compartilhado; as 2 redes dividem a cena negra.
> 70	- **3.5 Sinapses:** arestas cross-partition REAIS (`mcorch_edges`) como linhas baixa-opacidade; acendem só em `universe`.
> 71	- **3.6 Unificar hooks/interação:** select → painel `useNodeIntelligence`; fly-to câmera; toggles `matrix`/`memory`/`universe` no Sidebar.
> 72	- **3.7 Layout 72/28 + estabilização + perf:** árvore flex única, terminal tático flutuante; instancing; verificar <50ms; corrigir `absolute inset-0` escapando flex (padrão `DashboardLayout`).
> 73	- **3.8 Executar a poda:** aposentar squad-coloring dormante no canvas novo; legado Matrix intacto como backup.
> 74	- **3.9 Paridade + cutover:** ao atingir paridade, nav aponta pro `/universe`; rotas legadas acessíveis como backup. **Gate E2E Lei 1:** `bun run scripts/qa/audit-canvas-ui.ts` (screenshot 1920×1080) obrigatório p/ mudança de Canvas.
> 75	- **3.10 Seal:** tsc 0 · testes · nó mesh · `/handoff` · resolução do débito BoK.
> 76	
> 77	---
> 78	
> 79	## 4. Riscos & Diretrizes
> 80	- **Maior risco:** reescrita do renderer (Sigma→R3F) + perf em 8.5k nós → mitigado por InstancedMesh + extração do compute (graphology reusado, não reescrito).
> 81	- **Não-quebrante:** cada passo compila (tsc 0) e as 3 páginas legadas seguem roteadas até a paridade (3.9).
> 82	- **Idioma:** código/comentários EN · relatórios PT-BR.
> 83	- **OTDs abertas:** `OTD-SQUAD-OWNERSHIP-REVIVAL` (posse por sinal real) · `OTD-SYNAPSE-EMBEDDING` (sinapses por similaridade 768d) · `OTD-UCANVAS-PERF` (orçamento <50ms em 8.5k nós).
> 84	
> ```

## 🤖 Claude *(22:56:14)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/UnifiedCanvasPage.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useEffect, useMemo } from 'react';
> 2	import { Canvas } from '@react-three/fiber';
> 3	import { OrbitControls } from '@react-three/drei';
> 4	import { Orbit, Boxes, BrainCircuit, Network, Cpu, Loader2, Sparkles, X } from 'lucide-react';
> 5	import type Graph from 'graphology';
> 6	import {
> 7	  useUnifiedCanvasStore,
> 8	  codeNetworkVisible,
> 9	  memoryNetworkVisible,
> 10	  synapsesVisible,
> 11	  type CanvasViewMode,
> 12	} from '@/store/useUnifiedCanvasStore';
> 13	import { useConstellationSigma } from '@/hooks/useConstellationSigma';
> 14	import { useMemoryNetwork, type MemoryNode } from '@/hooks/useMemoryNetwork';
> 15	import { useSynapses } from '@/hooks/useSynapses';
> 16	import { useNodeIntelligence } from '@/hooks/useNodeIntelligence';
> 17	import { useCrewOverlay } from '@/hooks/useCrewOverlay';
> 18	import { CodeNetworkLayer } from '@/components/universe/CodeNetworkLayer';
> 19	import { MemoryNetworkLayer } from '@/components/universe/MemoryNetworkLayer';
> 20	import { SynapseLayer } from '@/components/universe/SynapseLayer';
> 21	import { CameraRig } from '@/components/universe/CameraRig';
> 22	import { MegaBrainVisualizer } from '@/components/core-fable/MegaBrainVisualizer';
> 23	
> 24	// Phase Epsilon V9 — Unified Sensorial Canvas (PR-025).
> 25	// Phase 3.5/3.6: real inter-network synapses (mcorch_edges anchored by set
> 26	// membership — never decorative) lit in 'universe' view, plus click-to-select
> 27	// with camera fly-to on both networks. Backdrop = inherited Mega Brain
> 28	// visualizer (3.4). Legacy routes remain live as backup until 3.9 parity.
> 29	
> 30	const VIEW_OPTIONS: { mode: CanvasViewMode; label: string; icon: typeof Orbit }[] = [
> 31	  { mode: 'matrix', label: 'Matrix', icon: Boxes },
> 32	  { mode: 'memory', label: 'Memória', icon: BrainCircuit },
> 33	  { mode: 'universe', label: 'Universo', icon: Orbit },
> 34	];
> 35	
> 36	function ViewToggle() {
> 37	  const viewMode = useUnifiedCanvasStore((s) => s.viewMode);
> 38	  const setViewMode = useUnifiedCanvasStore((s) => s.setViewMode);
> 39	
> 40	  return (
> 41	    <div className="flex items-center gap-1 rounded-full border border-violet-500/20 bg-violet-500/5 p-0.5">
> 42	      {VIEW_OPTIONS.map(({ mode, label, icon: Icon }) => {
> 43	        const active = viewMode === mode;
> 44	        return (
> 45	          <button
> 46	            key={mode}
> 47	            onClick={() => setViewMode(mode)}
> 48	            className={`flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[10px] font-mono font-bold uppercase tracking-wider transition-all ${
> 49	              active
> 50	                ? 'border border-cyan-500/50 bg-cyan-500/15 text-cyan-300 shadow-[0_0_8px_rgba(0,242,255,0.2)]'
> 51	                : 'border border-transparent text-violet-400/70 hover:text-cyan-400'
> 52	            }`}
> 53	            title={`Visão: ${label}`}
> 54	          >
> 55	            <Icon className="w-3 h-3" />
> 56	            {label}
> 57	          </button>
> 58	        );
> 59	      })}
> 60	    </div>
> 61	  );
> 62	}
> 63	
> 64	function NetworkBadge({ on, label, color }: { on: boolean; label: string; color: string }) {
> 65	  return (
> 66	    <div
> 67	      className={`flex items-center gap-1.5 px-2 py-0.5 rounded-full border text-[9px] font-mono uppercase tracking-wider transition-opacity ${color} ${
> 68	        on ? 'opacity-100' : 'opacity-30'
> 69	      }`}
> 70	    >
> 71	      <span className={`w-1.5 h-1.5 rounded-full ${on ? 'animate-pulse' : ''}`} style={{ background: 'currentColor' }} />
> 72	      {label}
> 73	    </div>
> 74	  );
> 75	}
> 76	
> 77	// Selection intelligence (3.9 parity with the legacy Matrix NodeDetailsPanel): free content
> 78	// fetch on select + explicit "Analisar" action (LLM analyze-node — user-triggered, never auto).
> 79	function SelectionPanel({ graph, memoryNodes }: { graph: Graph | null; memoryNodes: MemoryNode[] }) {
> 80	  const selection = useUnifiedCanvasStore((s) => s.selection);
> 81	  const clearSelection = useUnifiedCanvasStore((s) => s.clearSelection);
> 82	  const intel = useNodeIntelligence();
> 83	  const nodeId = selection?.nodeId ?? null;
> 84	
> 85	  useEffect(() => {
> 86	    // crew_agent__* ids are overlay-injected (not mcorch_nodes rows) — nothing to fetch.
> 87	    if (nodeId && !nodeId.startsWith('crew_agent__')) intel.fetchNodeContent(nodeId);
> 88	    else intel.clear();
> 89	    // eslint-disable-next-line react-hooks/exhaustive-deps
> 90	  }, [nodeId]);
> 91	
> 92	  if (!selection) {
> 93	    return <div className="font-mono text-xs text-white/60">nenhum nó selecionado</div>;
> 94	  }
> 95	
> 96	  const attrs = selection.network === 'code' && graph?.hasNode(selection.nodeId)
> 97	    ? (graph.getNodeAttributes(selection.nodeId) as Record<string, unknown>)
> 98	    : null;
> 99	  const memNode = selection.network === 'memory'
> 100	    ? memoryNodes.find((n) => n.id === selection.nodeId) ?? null
> 101	    : null;
> 102	  const name = (attrs?.label as string) ?? memNode?.name ?? selection.nodeId.slice(0, 12) + '…';
> 103	  const kind = (attrs?.kind as string) ?? memNode?.node_type ?? '—';
> 104	  const stability = (attrs?.stability as number) ?? memNode?.stability_score ?? null;
> 105	
> 106	  return (
> 107	    <div className="space-y-2">
> 108	      <div className="flex items-start justify-between gap-2">
> 109	        <div className="font-mono text-xs text-cyan-300 break-all">{name}</div>
> 110	        <button onClick={clearSelection} title="Limpar seleção" className="text-violet-400/60 hover:text-cyan-400 flex-shrink-0">
> 111	          <X className="w-3 h-3" />
> 112	        </button>
> 113	      </div>
> 114	      <div className="grid grid-cols-2 gap-x-2 gap-y-1 font-mono text-[10px] text-white/60">
> 115	        <span>rede: <span className="text-cyan-300">{selection.network === 'code' ? 'código' : 'memória'}</span></span>
> 116	        <span>tipo: <span className="text-cyan-300">{kind}</span></span>
> 117	        {stability != null && <span>estab.: <span className="text-cyan-300">{Number(stability).toFixed(2)}</span></span>}
> 118	        {attrs != null && <span>comun.: <span className="text-cyan-300">{String(attrs.community ?? '—')}</span></span>}
> 119	        {attrs != null && <span>calls→: <span className="text-cyan-300">{String(attrs.callsOut ?? 0)}</span></span>}
> 120	        {attrs != null && <span>→calls: <span className="text-cyan-300">{String(attrs.callsIn ?? 0)}</span></span>}
> 121	      </div>
> 122	      {intel.isLoading && <div className="font-mono text-[10px] text-violet-400/50">carregando conteúdo…</div>}
> 123	      {intel.content && (
> 124	        <div className="max-h-32 overflow-auto rounded border border-violet-500/10 bg-violet-500/5 p-2 font-mono text-[10px] leading-relaxed text-white/70 whitespace-pre-wrap">
> 125	          {intel.content.slice(0, 1200)}
> 126	        </div>
> 127	      )}
> 128	      <button
> 129	        onClick={() => intel.analyzeNode(selection.nodeId, intel.content ?? '', attrs?.metadata ?? {})}
> 130	        disabled={intel.isAnalyzing}
> 131	        className="flex items-center gap-1.5 rounded border border-fuchsia-500/30 bg-fuchsia-500/10 px-2 py-1 font-mono text-[10px] uppercase tracking-wider text-fuchsia-300 hover:bg-fuchsia-500/20 disabled:opacity-40"
> 132	      >
> 133	        <Sparkles className="w-3 h-3" />
> 134	        {intel.isAnalyzing ? 'analisando…' : 'Analisar (IA)'}
> 135	      </button>
> 136	      {intel.analysis && (
> 137	        <div className="max-h-40 overflow-auto rounded border border-fuchsia-500/15 bg-fuchsia-500/5 p-2 font-mono text-[10px] leading-relaxed text-fuchsia-100/80 whitespace-pre-wrap">
> 138	          {intel.analysis}
> 139	        </div>
> 140	      )}
> 141	      {intel.error && <div className="font-mono text-[10px] text-rose-400/80">{intel.error}</div>}
> 142	    </div>
> 143	  );
> 144	}
> 145	
> 146	function Stat({ label, value }: { label: string; value: string | number }) {
> 147	  return (
> 148	    <div>
> 149	      <div className="font-mono text-[9px] text-violet-400/50 uppercase tracking-widest mb-0.5">{label}</div>
> 150	      <div className="font-mono text-sm text-cyan-300">{value}</div>
> 151	    </div>
> 152	  );
> 153	}
> 154	
> 155	export default function UnifiedCanvasPage() {
> 156	  const viewMode = useUnifiedCanvasStore((s) => s.viewMode);
> 157	  // Crew overlay (3.9 parity — plan: "overlay de agente sobrevive"): the sigma hook injects
> 158	  // crew_agent nodes + INHABITS edges into the graph, so the code layer renders them natively.
> 159	  const { overlayAgents, agentCount } = useCrewOverlay();
> 160	  const sigmaOptions = useMemo(() => ({ overlayAgents }), [overlayAgents]);
> 161	  const { graph, nodeCount, edgeCount, communityCount, isLoading } = useConstellationSigma(sigmaOptions);
> 162	  const { nodes: memoryNodes, count: memoryCount, isLoading: memoryLoading } = useMemoryNetwork();
> 163	  const { positions: synapsePositions, count: synapseCount } = useSynapses(graph, memoryNodes);
> 164	
> 165	  const showCode = codeNetworkVisible(viewMode);
> 166	  const showMemory = memoryNetworkVisible(viewMode);
> 167	  const showSynapses = synapsesVisible(viewMode);
> 168	  const loading = isLoading || memoryLoading;
> 169	
> 170	  return (
> 171	    <div className="flex flex-col h-full bg-[#050210] overflow-hidden">
> 172	      {/* ── HUD bar ── */}
> 173	      <div className="flex-shrink-0 flex items-center justify-between px-4 py-2 border-b border-violet-500/15 bg-[#050210] z-20">
> 174	        <div className="flex items-center gap-2">
> 175	          <Cpu className="w-4 h-4 text-cyan-400" />
> 176	          <span className="font-mono text-xs font-bold text-white/90 tracking-wider uppercase">
> 177	            Unified Sensorial Canvas
> 178	          </span>
> 179	          <span className="font-mono text-[9px] text-violet-400/50 uppercase tracking-widest">Epsilon V9 · 3.8</span>
> 180	        </div>
> 181	        <ViewToggle />
> 182	      </div>
> 183	
> 184	      {/* ── Main layout (72 / 28) ── */}
> 185	      <div className="flex flex-1 min-h-0 overflow-hidden">
> 186	        {/* Canvas — 72% */}
> 187	        <div className="relative min-w-0 min-h-0 h-full overflow-hidden" style={{ width: '72%' }}>
> 188	          {/* Black hole backdrop (3.4) — inherited Mega Brain visualizer. Mounted only AFTER the
> 189	              graph data settles (3.7): its raymarch shader compile stalls the main thread for
> 190	              seconds (worst under software GL), which was delaying the network page bursts. */}
> 191	          {!loading && (
> 192	            <div className="absolute inset-0 z-0">
> 193	              <MegaBrainVisualizer isThinking={false} />
> 194	            </div>
> 195	          )}
> 196	
> 197	          {/* Networks — transparent canvas over the black hole (shared black space) */}
> 198	          <Canvas
> 199	            className="!absolute inset-0 z-10"
> 200	            camera={{ position: [0, 9, 26], fov: 50 }}
> 201	            gl={{ antialias: true, alpha: true, stencil: false, depth: true }}
> 202	            style={{ background: 'transparent' }}
> 203	          >
> 204	            <fog attach="fog" args={['#050210', 32, 95]} />
> 205	            <ambientLight intensity={0.5} />
> 206	            <CodeNetworkLayer graph={graph} visible={showCode} />
> 207	            <MemoryNetworkLayer nodes={memoryNodes} visible={showMemory} />
> 208	            <SynapseLayer positions={synapsePositions} visible={showSynapses} />
> 209	            <OrbitControls makeDefault enableDamping dampingFactor={0.06} minDistance={4} maxDistance={75} />
> 210	            <CameraRig />
> 211	          </Canvas>
> 212	
> 213	          {/* Loading overlay */}
> 214	          {loading && (
> 215	            <div className="absolute inset-0 z-20 flex items-center justify-center pointer-events-none">
> 216	              <Loader2 className="w-6 h-6 text-violet-400/70 animate-spin" />
> 217	            </div>
> 218	          )}
> 219	
> 220	          {/* Active-mode label (top-left) */}
> 221	          <div className="absolute top-3 left-3 z-20 pointer-events-none font-mono text-[10px] text-white/60 uppercase tracking-widest">
> 222	            {viewMode === 'matrix' ? 'Rede de Código' : viewMode === 'memory' ? 'Rede de Memória' : 'Universo'}
> 223	          </div>
> 224	
> 225	          {/* Network badges (bottom-center) */}
> 226	          <div className="absolute bottom-3 left-1/2 -translate-x-1/2 z-20 flex items-center gap-2 pointer-events-none">
> 227	            <NetworkBadge on={showCode} label="Código" color="border-emerald-500/30 bg-emerald-500/5 text-emerald-400" />
> 228	            <NetworkBadge on={showMemory} label="Memória" color="border-cyan-500/30 bg-cyan-500/5 text-cyan-400" />
> 229	            <NetworkBadge on={showSynapses && synapseCount > 0} label={`Sinapses${synapseCount > 0 ? ` ${synapseCount}` : ''}`} color="border-fuchsia-500/30 bg-fuchsia-500/5 text-fuchsia-400" />
> 230	          </div>
> 231	        </div>
> 232	
> 233	        {/* Tactical terminal — 28% */}
> 234	        <div
> 235	          className="relative flex flex-col min-w-0 min-h-0 h-full border-l border-violet-500/10 bg-[#070414] overflow-hidden"
> 236	          style={{ width: '28%' }}
> 237	        >
> 238	          <div className="flex-shrink-0 flex items-center gap-2 px-3 py-2 border-b border-violet-500/10">
> 239	            <Network className="w-3.5 h-3.5 text-cyan-400" />
> 240	            <span className="font-mono text-[10px] text-cyan-400/80 uppercase tracking-wider font-bold">
> 241	              Terminal Tático
> 242	            </span>
> 243	          </div>
> 244	
> 245	          <div className="flex-1 min-h-0 overflow-auto p-3 space-y-4">
> 246	            <Stat label="Visão ativa" value={viewMode.toUpperCase()} />
> 247	
> 248	            <div>
> 249	              <div className="font-mono text-[9px] text-emerald-400/50 uppercase tracking-widest mb-1">Rede de Código (Louvain)</div>
> 250	              <div className="grid grid-cols-3 gap-2">
> 251	                <Stat label="Nós" value={isLoading ? '…' : nodeCount.toLocaleString('pt-BR')} />
> 252	                <Stat label="Arestas" value={isLoading ? '…' : edgeCount.toLocaleString('pt-BR')} />
> 253	                <Stat label="Comun." value={isLoading ? '…' : communityCount} />
> 254	              </div>
> 255	              <div className="mt-1">
> 256	                <Stat label="Agentes (crew)" value={agentCount} />
> 257	              </div>
> 258	            </div>
> 259	
> 260	            <div>
> 261	              <div className="font-mono text-[9px] text-cyan-400/50 uppercase tracking-widest mb-1">Rede de Memória (GraphRAG)</div>
> 262	              <Stat label="Pensamentos" value={memoryLoading ? '…' : memoryCount.toLocaleString('pt-BR')} />
> 263	            </div>
> 264	
> 265	            <div>
> 266	              <div className="font-mono text-[9px] text-fuchsia-400/50 uppercase tracking-widest mb-1">Sinapses (arestas reais)</div>
> 267	              <Stat label="Código ↔ Memória" value={synapseCount} />
> 268	            </div>
> 269	
> 270	            <div>
> 271	              <div className="font-mono text-[9px] text-violet-400/50 uppercase tracking-widest mb-1">Seleção</div>
> 272	              <SelectionPanel graph={graph} memoryNodes={memoryNodes} />
> 273	            </div>
> 274	
> 275	            <div>
> 276	              <div className="font-mono text-[9px] text-violet-400/50 uppercase tracking-widest mb-1">Próximas fases</div>
> 277	              <div className="font-mono text-[10px] text-violet-400/40 leading-relaxed">
> 278	                3.9 paridade + cutover · 3.10 seal
> 279	              </div>
> 280	            </div>
> 281	          </div>
> 282	        </div>
> 283	      </div>
> 284	    </div>
> 285	  );
> 286	}
> 287	
> ```

## 🤖 Claude *(22:56:45)*


## 🤖 Claude *(22:56:48)*

Estado real confirmado (Lei 1, não confio no doc stale): a página (Jul 4) traz HUD **"Epsilon V9 · 3.8"** e painel "Próximas fases: **3.9 paridade + cutover · 3.10 seal**". Ou seja, **3.5-3.8 estão VIVAS** (sinapses reais, fly-to via CameraRig, perf com backdrop pós-load, poda do squad-coloring). Restam **3.9 (paridade + cutover de nav)** e **3.10 (seal)**.

Vou verificar o instancing (3.7), a estrutura de nav atual (para o cutover) e o débito BoK (gate 2.2 do plano):

## 🤖 Claude *(22:56:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== InstancedMesh in CodeNetworkLayer (3.7 proof) ===\"; python3 -c \"import subprocess; print(subprocess.run(['grep','-n','instancedMesh\\|InstancedMesh\\|LineSegments\\|BufferGeometry','src/components/universe/CodeNetworkLayer.tsx','src/components/universe/MemoryNetworkLayer.tsx','src/components/universe/SynapseLayer.tsx'],capture_output=True,text=True).stdout)\"\necho \"=== nav: how are universe/matrix/memory/core-fable exposed? ===\"; python3 -c \"import subprocess; print(subprocess.run(['grep','-rn','universe\\|constellation/matrix\\|constellation/memory\\|core-fable\\|Universo\\|Matrix\\|Mem\u00f3ria','src/components/dashboard/DashboardSidebar.tsx'],capture_output=True,text=True).stdout)\" 2>/dev/null\necho \"=== sidebar file location ===\"; find src -iname '*sidebar*' -o -iname '*DashboardLayout*' | head\necho \"=== BoK debt: unified canvas in mcorch-constellation BoK? ===\"; python3 -c \"import subprocess; print(subprocess.run(['grep','-rln','Unified Sensorial\\|unified.canvas\\|PR-025\\|Epsilon V9','docs/bok/mcorch-constellation'],capture_output=True,text=True).stdout or 'not found in BoK')\"",
  "description": "Verify 3.7 instancing + nav structure + BoK debt"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === InstancedMesh in CodeNetworkLayer (3.7 proof) ===
> <string>:1: SyntaxWarning: invalid escape sequence '\|'
> src/components/universe/CodeNetworkLayer.tsx:10:// origin and draw as a SINGLE InstancedMesh (NFR-023 — no per-node meshes);
> src/components/universe/CodeNetworkLayer.tsx:11:// edges as one batched LineSegments. Node color = Louvain community, reused
> src/components/universe/CodeNetworkLayer.tsx:29:  const meshRef = useRef<THREE.InstancedMesh>(null);
> src/components/universe/CodeNetworkLayer.tsx:71:    const g = new THREE.BufferGeometry();
> src/components/universe/CodeNetworkLayer.tsx:102:      <instancedMesh
> src/components/universe/CodeNetworkLayer.tsx:105:        args={[undefined as unknown as THREE.BufferGeometry, undefined as unknown as THREE.Material, count]}
> src/components/universe/CodeNetworkLayer.tsx:110:      </instancedMesh>
> src/components/universe/MemoryNetworkLayer.tsx:11:// Gold/Scalar). Single InstancedMesh (NFR-023).
> src/components/universe/MemoryNetworkLayer.tsx:33:  const meshRef = useRef<THREE.InstancedMesh>(null);
> src/components/universe/MemoryNetworkLayer.tsx:85:    <instancedMesh
> src/components/universe/MemoryNetworkLayer.tsx:88:      args={[undefined as unknown as THREE.BufferGeometry, undefined as unknown as THREE.Material, count]}
> src/components/universe/MemoryNetworkLayer.tsx:99:    </instancedMesh>
> src/components/universe/SynapseLayer.tsx:16:    const g = new THREE.BufferGeometry();
> 
> === nav: how are universe/matrix/memory/core-fable exposed? ===
> 103:      { title: 'Core Fable', url: '/dashboard/core-fable', icon: Brain },
> 250:                  {/* Constelação — collapsible with Matrix + Memória sub-items */}
> 280:                                to="/dashboard/constellation/matrix"
> 285:                                <span>Matrix</span>
> 292:                                to="/dashboard/constellation/memory"
> 297:                                <span>Memória</span>
> 306:                                to="/dashboard/universe"
> 311:                                <span>Universo</span>
> 
> === sidebar file location ===
> src/components/dashboard/DashboardSidebar.tsx
> src/components/dashboard/DashboardLayout.tsx
> src/components/ui/sidebar.tsx
> === BoK debt: unified canvas in mcorch-constellation BoK? ===
> <string>:1: SyntaxWarning: invalid escape sequence '\|'
> docs/bok/mcorch-constellation/05-sdd.md
> docs/bok/mcorch-constellation/04-frd.md
> docs/bok/mcorch-constellation/03-prd.md
> ```

## 🤖 Claude *(22:57:28)*


## 🤖 Claude *(22:57:32)*

Confirmado (Lei 1):
- **3.7 done**: `CodeNetworkLayer`/`MemoryNetworkLayer` usam `InstancedMesh` (NFR-023) + edges em `LineSegments`/`BufferGeometry` batched.
- **Débito BoK resolvido**: Unified Sensorial Canvas está documentado no BoK (PRD/FRD/SDD do mcorch-constellation) — gate 2.2 fechado por emenda BoK, não override.
- **Nav atual**: "Constelação" (collapsible) → sub-itens Matrix · Memória · **Universo** (por último); Core Fable é item separado.

Resta **3.9 (cutover de nav: promover /universe a primário, legado como backup)** + gate E2E, e **3.10 (seal)**. Leio a seção exata do sidebar:

## 🤖 Claude *(22:57:37)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/dashboard/DashboardSidebar.tsx",
  "offset": 248,
  "limit": 72
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 248	                  </SidebarMenuItem>
> 249	
> 250	                  {/* Constelação — collapsible with Matrix + Memória sub-items */}
> 251	                  <Collapsible defaultOpen={isConstellationActive} className="group/collapsible">
> 252	                    <SidebarMenuItem>
> 253	                      <div className="flex items-center">
> 254	                        <SidebarMenuButton asChild className="flex-1">
> 255	                          <NavLink
> 256	                            to="/dashboard/constellation"
> 257	                            end
> 258	                            className="hover:bg-muted/50"
> 259	                            activeClassName="bg-primary/10 text-primary font-medium"
> 260	                          >
> 261	                            <Orbit className="mr-2 h-4 w-4 shrink-0" />
> 262	                            <span>Constelação</span>
> 263	                          </NavLink>
> 264	                        </SidebarMenuButton>
> 265	                        <CollapsibleTrigger asChild>
> 266	                          <Button
> 267	                            variant="ghost"
> 268	                            size="icon"
> 269	                            className="h-6 w-6 ml-auto shrink-0 [&[data-state=open]>svg]:rotate-180"
> 270	                          >
> 271	                            <ChevronDown className="h-3.5 w-3.5 transition-transform duration-200" />
> 272	                          </Button>
> 273	                        </CollapsibleTrigger>
> 274	                      </div>
> 275	                      <CollapsibleContent>
> 276	                        <SidebarMenuSub>
> 277	                          <SidebarMenuSubItem>
> 278	                            <SidebarMenuSubButton asChild>
> 279	                              <NavLink
> 280	                                to="/dashboard/constellation/matrix"
> 281	                                className="hover:bg-muted/50"
> 282	                                activeClassName="text-primary font-medium"
> 283	                              >
> 284	                                <Network className="mr-2 h-3.5 w-3.5 shrink-0" />
> 285	                                <span>Matrix</span>
> 286	                              </NavLink>
> 287	                            </SidebarMenuSubButton>
> 288	                          </SidebarMenuSubItem>
> 289	                          <SidebarMenuSubItem>
> 290	                            <SidebarMenuSubButton asChild>
> 291	                              <NavLink
> 292	                                to="/dashboard/constellation/memory"
> 293	                                className="hover:bg-muted/50"
> 294	                                activeClassName="text-primary font-medium"
> 295	                              >
> 296	                                <Brain className="mr-2 h-3.5 w-3.5 shrink-0" />
> 297	                                <span>Memória</span>
> 298	                              </NavLink>
> 299	                            </SidebarMenuSubButton>
> 300	                          </SidebarMenuSubItem>
> 301	                          {/* Unified Sensorial Canvas (Epsilon V9) — additive entry; legacy routes stay
> 302	                              until the 3.9 nav cutover decision (Sovereign). */}
> 303	                          <SidebarMenuSubItem>
> 304	                            <SidebarMenuSubButton asChild>
> 305	                              <NavLink
> 306	                                to="/dashboard/universe"
> 307	                                className="hover:bg-muted/50"
> 308	                                activeClassName="text-primary font-medium"
> 309	                              >
> 310	                                <Orbit className="mr-2 h-3.5 w-3.5 shrink-0" />
> 311	                                <span>Universo</span>
> 312	                              </NavLink>
> 313	                            </SidebarMenuSubButton>
> 314	                          </SidebarMenuSubItem>
> 315	                        </SidebarMenuSub>
> 316	                      </CollapsibleContent>
> 317	                    </SidebarMenuItem>
> 318	                  </Collapsible>
> 319	
> ```

## 🤖 Claude *(22:58:18)*


## 🤖 Claude *(22:58:21)*

Entendi a nav. "Constelação" (parent → `/dashboard/constellation`, o grafo 3D do crew) tem sub-itens Matrix · Memória · **Universo** (aditivo, por último — o comentário confirma que o cutover 3.9 estava pendente). O Universo funde Matrix+Memória+backdrop Core-Fable, mas **não** substitui o grafo do crew nem o Core-Fable-chat.

**Cutover 3.9 (mínimo, não-quebrante):** promover Universo a **primário (primeiro)**, Matrix/Memória permanecem acessíveis como backup:

## 🤖 Claude *(22:58:35)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/components/dashboard/DashboardSidebar.tsx",
  "old_string": "                      <CollapsibleContent>\n                        <SidebarMenuSub>\n                          <SidebarMenuSubItem>\n                            <SidebarMenuSubButton asChild>\n                              <NavLink\n                                to=\"/dashboard/constellation/matrix\"\n                                className=\"hover:bg-muted/50\"\n                                activeClassName=\"text-primary font-medium\"\n                              >\n                                <Network className=\"mr-2 h-3.5 w-3.5 shrink-0\" />\n                                <span>Matrix</span>\n                              </NavLink>\n                            </SidebarMenuSubButton>\n                          </SidebarMenuSubItem>\n                          <SidebarMenuSubItem>\n                            <SidebarMenuSubButton asChild>\n                              <NavLink\n                                to=\"/dashboard/constellation/memory\"\n                                className=\"hover:bg-muted/50\"\n                                activeClassName=\"text-primary font-medium\"\n                              >\n                                <Brain className=\"mr-2 h-3.5 w-3.5 shrink-0\" />\n                                <span>Mem\u00f3ria</span>\n                              </NavLink>\n                            </SidebarMenuSubButton>\n                          </SidebarMenuSubItem>\n                          {/* Unified Sensorial Canvas (Epsilon V9) \u2014 additive entry; legacy routes stay\n                              until the 3.9 nav cutover decision (Sovereign). */}\n                          <SidebarMenuSubItem>\n                            <SidebarMenuSubButton asChild>\n                              <NavLink\n                                to=\"/dashboard/universe\"\n                                className=\"hover:bg-muted/50\"\n                                activeClassName=\"text-primary font-medium\"\n                              >\n                                <Orbit className=\"mr-2 h-3.5 w-3.5 shrink-0\" />\n                                <span>Universo</span>\n                              </NavLink>\n                            </SidebarMenuSubButton>\n                          </SidebarMenuSubItem>\n                        </SidebarMenuSub>\n                      </CollapsibleContent>",
  "new_string": "                      <CollapsibleContent>\n                        <SidebarMenuSub>\n                          {/* Epsilon V9 \u00b7 3.9 cutover: the Unified Sensorial Canvas is now the PRIMARY\n                              constellation surface (fuses the code + memory networks over the Mega Brain\n                              backdrop). The legacy Matrix/Mem\u00f3ria pages stay routed below as backup. */}\n                          <SidebarMenuSubItem>\n                            <SidebarMenuSubButton asChild>\n                              <NavLink\n                                to=\"/dashboard/universe\"\n                                className=\"hover:bg-muted/50\"\n                                activeClassName=\"text-primary font-medium\"\n                              >\n                                <Orbit className=\"mr-2 h-3.5 w-3.5 shrink-0\" />\n                                <span>Universo</span>\n                              </NavLink>\n                            </SidebarMenuSubButton>\n                          </SidebarMenuSubItem>\n                          <SidebarMenuSubItem>\n                            <SidebarMenuSubButton asChild>\n                              <NavLink\n                                to=\"/dashboard/constellation/matrix\"\n                                className=\"hover:bg-muted/50\"\n                                activeClassName=\"text-primary font-medium\"\n                              >\n                                <Network className=\"mr-2 h-3.5 w-3.5 shrink-0\" />\n                                <span>Matrix <span className=\"text-[9px] uppercase tracking-wider opacity-40\">backup</span></span>\n                              </NavLink>\n                            </SidebarMenuSubButton>\n                          </SidebarMenuSubItem>\n                          <SidebarMenuSubItem>\n                            <SidebarMenuSubButton asChild>\n                              <NavLink\n                                to=\"/dashboard/constellation/memory\"\n                                className=\"hover:bg-muted/50\"\n                                activeClassName=\"text-primary font-medium\"\n                              >\n                                <Brain className=\"mr-2 h-3.5 w-3.5 shrink-0\" />\n                                <span>Mem\u00f3ria <span className=\"text-[9px] uppercase tracking-wider opacity-40\">backup</span></span>\n                              </NavLink>\n                            </SidebarMenuSubButton>\n                          </SidebarMenuSubItem>\n                        </SidebarMenuSub>\n                      </CollapsibleContent>"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/components/dashboard/DashboardSidebar.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:58:56)*


## 🤖 Claude *(22:58:56)*

Agora atualizo o HUD da página para refletir 3.9 e a lista de próximas fases:

## 🤖 Claude *(22:58:59)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/UnifiedCanvasPage.tsx",
  "old_string": "          <span className=\"font-mono text-[9px] text-violet-400/50 uppercase tracking-widest\">Epsilon V9 \u00b7 3.8</span>",
  "new_string": "          <span className=\"font-mono text-[9px] text-violet-400/50 uppercase tracking-widest\">Epsilon V9 \u00b7 3.9</span>"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/UnifiedCanvasPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:59:02)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/UnifiedCanvasPage.tsx",
  "old_string": "            <div>\n              <div className=\"font-mono text-[9px] text-violet-400/50 uppercase tracking-widest mb-1\">Pr\u00f3ximas fases</div>\n              <div className=\"font-mono text-[10px] text-violet-400/40 leading-relaxed\">\n                3.9 paridade + cutover \u00b7 3.10 seal\n              </div>\n            </div>",
  "new_string": "            <div>\n              <div className=\"font-mono text-[9px] text-violet-400/50 uppercase tracking-widest mb-1\">Superf\u00edcie prim\u00e1ria</div>\n              <div className=\"font-mono text-[10px] text-violet-400/40 leading-relaxed\">\n                Cutover 3.9 conclu\u00eddo \u00b7 Matrix/Mem\u00f3ria seguem roteadas como backup\n              </div>\n            </div>"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/UnifiedCanvasPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(22:59:23)*


## 🤖 Claude *(22:59:24)*

Agora crio o gate E2E Lei-1 para a superfície `/universe` (anticorpo re-executável — Lei 2), espelhando o padrão provado do `audit-canvas-ui.ts` (magic-link → Playwright 1920×1080 → Vision QA), adaptado ao canvas R3F do Universo:

## 🤖 Claude *(22:59:56)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/audit-universe-ui.ts",
  "content": "/// <reference types=\"node\" />\n// Epsilon V9 \u00b7 3.9 \u2014 Lei-1 Canvas E2E gate for the Unified Sensorial Canvas (/dashboard/universe).\n// Mirrors scripts/qa/audit-canvas-ui.ts (magic-link auth \u2192 headless 1920x1080 \u2192 structural asserts \u2192\n// Vision QA gate). The code network query is slow (OTD-UCANVAS-PERF ~30s), so waits are generous.\n// Run: bun run scripts/qa/audit-universe-ui.ts   (use --no-vision only as an explicit, logged exception)\nimport { chromium } from 'playwright';\nimport { createClient } from '@supabase/supabase-js';\nimport { existsSync, readFileSync } from 'fs';\nimport { spawnSync } from 'child_process';\nimport { join } from 'path';\n\nconst ROOT = '/home/gcrUX/htdocs/constellation-orchestra';\nconst envPath = join(ROOT, '.env');\nif (existsSync(envPath)) {\n  const raw = readFileSync(envPath, 'utf-8');\n  for (const line of raw.split('\\n')) {\n    const m = line.match(/^([^#=\\s][^=]*)=(.*)$/);\n    if (m) process.env[m[1].trim()] = m[2].trim().replace(/^[\"']|[\"']$/g, '');\n  }\n}\n\nconst supabaseUrl = process.env.SUPABASE_URL;\nconst serviceKey = process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY;\nif (!supabaseUrl || !serviceKey) {\n  console.error('\u274c Missing Supabase credentials in env.');\n  process.exit(1);\n}\n\nconst redirectTarget = 'https://login.mcorch.com/dashboard/universe';\n\nasync function runAudit() {\n  console.log('\ud83d\ude80 Starting Unified Sensorial Canvas (Universo) E2E audit...');\n  const supabase = createClient(supabaseUrl!, serviceKey!, { auth: { autoRefreshToken: false, persistSession: false } });\n\n  console.log('\ud83d\udd10 Generating one-time Magic Link for gabrielcall@gmail.com...');\n  const { data: linkData, error: linkErr } = await supabase.auth.admin.generateLink({\n    type: 'magiclink',\n    email: 'gabrielcall@gmail.com',\n    options: { redirectTo: redirectTarget },\n  });\n  if (linkErr || !linkData?.properties?.action_link) {\n    console.error('\u274c Failed to generate magic login link:', linkErr);\n    process.exit(1);\n  }\n  const magicLink = linkData.properties.action_link;\n  console.log('\ud83d\udd17 Magic Link generated.');\n\n  console.log('\ud83c\udf10 Launching headless Chromium...');\n  const browser = await chromium.launch({ headless: true });\n  const context = await browser.newContext({ viewport: { width: 1920, height: 1080 } });\n  const page = await context.newPage();\n\n  console.log('\u2708\ufe0f Navigating via magic link...');\n  await page.goto(magicLink);\n  try {\n    await page.waitForURL('**/dashboard/universe*', { timeout: 20000 });\n    console.log(`\ud83d\udccd Redirected to: ${page.url().split('#')[0]}`);\n  } catch {\n    console.error('\u274c Timeout waiting for auth redirection. Current URL:', page.url());\n    await browser.close();\n    process.exit(1);\n  }\n\n  // Structural assert: the Unified Sensorial Canvas HUD must mount.\n  console.log('\u23f3 Waiting for the Unified Sensorial Canvas HUD...');\n  try {\n    await page.waitForFunction(\n      () => document.body.innerText.includes('Unified Sensorial Canvas'),\n      { timeout: 20000 },\n    );\n  } catch {\n    console.error('\u274c Assert Failed: \"Unified Sensorial Canvas\" HUD not found.');\n    await browser.close();\n    process.exit(1);\n  }\n\n  // Force the 'universe' view so the screenshot shows the full fusion (code + memory + synapses).\n  try {\n    await page.getByTitle('Vis\u00e3o: Universo').click({ timeout: 5000 });\n    console.log('\ud83e\ude90 Switched to Universo view.');\n  } catch {\n    console.warn('\u26a0\ufe0f Could not click the Universo toggle (continuing with default view).');\n  }\n\n  // The code network query is slow (OTD-UCANVAS-PERF). Wait for the \"N\u00f3s\" stat to become numeric\n  // (loading shows \"\u2026\"), up to 75s, then let R3F settle.\n  console.log('\u23f3 Waiting for network data to settle (code query is slow)...');\n  try {\n    await page.waitForFunction(\n      () => {\n        const t = document.body.innerText;\n        // The N\u00f3s stat renders \"\u2026\" while loading; a digit means the graph resolved.\n        const m = t.match(/N[\u00f3o]s\\s*\\n?\\s*([\\d.\u00a0]+)/i);\n        return !!m && /\\d/.test(m[1]);\n      },\n      { timeout: 75000 },\n    );\n    console.log('\ud83d\udcca Code network resolved.');\n  } catch {\n    console.warn('\u26a0\ufe0f Timeout waiting for the code network stat; capturing anyway.');\n  }\n\n  const canvasCount = await page.locator('canvas').count();\n  console.log(`\ud83c\udfa8 WebGL <canvas> elements: ${canvasCount}`);\n  if (canvasCount === 0) {\n    console.error('\u274c Assert Failed: no <canvas> (R3F) element rendered.');\n    await browser.close();\n    process.exit(1);\n  }\n\n  // Let the R3F scene draw a couple of frames.\n  await page.waitForTimeout(4000);\n\n  console.log('\ud83d\udcf8 Capturing Full HD (1920x1080) screenshot...');\n  const shotBuffer = await page.screenshot({ type: 'png', fullPage: false });\n  await browser.close();\n\n  if (process.argv.includes('--no-vision')) {\n    console.warn('\u26a0\ufe0f Vision gate SKIPPED via --no-vision (explicit exception \u2014 log the reason in the seal)');\n    console.log('\ud83c\udf89 Universo E2E audit completed (no-vision).');\n    return;\n  }\n  if (!process.env.VISION_MCP_PAT) {\n    console.error('\u274c Vision gate: VISION_MCP_PAT missing (.env). Use --no-vision only as an explicit exception.');\n    process.exit(1);\n  }\n  const supa = createClient(supabaseUrl!, serviceKey!, { auth: { persistSession: false } });\n  const shotKey = `qa-audits/universe-e2e-${Date.now()}.png`;\n  const up = await supa.storage.from('generated-images').upload(shotKey, shotBuffer, { contentType: 'image/png', upsert: true });\n  if (up.error) {\n    console.error('\u274c Vision gate: screenshot upload failed:', up.error.message);\n    process.exit(1);\n  }\n  const { data: signed } = await supa.storage.from('generated-images').createSignedUrl(shotKey, 3600);\n  if (!signed?.signedUrl) {\n    console.error('\u274c Vision gate: signed URL failed');\n    process.exit(1);\n  }\n  console.log(`\ud83d\udd17 Screenshot (signed, 1h): ${signed.signedUrl}`);\n  const question =\n    'Print 1920x1080 do Unified Sensorial Canvas (visualizador 3D de rede \u2014 dashboard MCORCH). ' +\n    'Avalie SO problemas visuais objetivos: tela toda preta/vazia SEM nenhum n\u00f3 ou elemento, mensagem de erro visivel, ' +\n    'layout quebrado/sobreposto, texto ilegivel. Um fundo escuro com pontos/rede 3D e um painel lateral e o resultado ESPERADO (nao e erro). ' +\n    'Comece a resposta com exatamente APROVADO ou REPROVADO, seguido do motivo em 1 frase.';\n  console.log('\ud83d\udc41\ufe0f Vision QA gate \u2014 judging the real screenshot...');\n  const vq = spawnSync('bun', ['run', join(ROOT, 'scripts/qa/vision-qa.ts'), 'image', signed.signedUrl, question], {\n    encoding: 'utf-8', env: process.env, timeout: 120000,\n  });\n  const out = `${vq.stdout ?? ''}${vq.stderr ?? ''}`;\n  console.log(out.trim());\n  await supa.storage.from('generated-images').remove([shotKey]).then(() => {}, () => {});\n  const approved = vq.status === 0 && /APROVADO/i.test(out) && !/REPROVADO/i.test(out);\n  if (!approved) {\n    console.error(`\u274c Vision gate REPROVED the print (exit=${vq.status}). Audit BLOCKED.`);\n    process.exit(1);\n  }\n  console.log('\u2705 Vision gate APROVADO');\n  console.log('\ud83c\udf89 Unified Sensorial Canvas (Universo) E2E audit completed successfully!');\n}\n\nrunAudit().catch((err) => {\n  console.error('\u274c Audit failed unexpectedly:', err);\n  process.exit(1);\n});\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/scripts/qa/audit-universe-ui.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(23:00:05)*


## 🤖 Claude *(23:00:05)*

tsc + build (deploy do cutover) e depois o gate E2E do Universo:

## 🤖 Claude *(23:00:07)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== tsc ===\"; npx tsc --noEmit 2>&1 | tail -12; echo \"tsc exit: ${PIPESTATUS[0]}\"\necho \"=== build (deploy cutover) ===\"; bun run build 2>&1 | tail -4; echo \"build exit: ${PIPESTATUS[0]}\"",
  "description": "tsc + build the nav cutover",
  "timeout": 240000
}
```

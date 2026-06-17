# Usar Model Council para verificar respostas de IA
**Date:** 2026-06-17 | **Session ID:** `8e7d8f29-84c2-4f23-ba65-90aee169a485`

---

## 👤 User *(05:20:53)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(05:20:53)*

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


## 🤖 Claude *(05:21:03)*


## 🤖 Claude *(05:21:04)*

I'll execute the ShakeHands /handson protocol. Starting with all pre-flight checks in parallel.

## 🤖 Claude *(05:21:05)*


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
> 1f1a7c4 docs: adiciona paper de referência "From AGI to ASI" (arXiv 2606.12683)
> 3a9b634 chore(sprint): register v6.40.0 Vision MCP Fatia 3 remainder (PAT UI + Plugin/Registry + caps) + proof manifest
> 129dcca docs(handoff): seal Vision MCP Fatia 3 remainder — PAT UI + install + Plugin/Registry + caps
> cf5ef7c docs(readme): v6.40.0 — Vision MCP conector consumível (PAT UI + Plugin Zip + Registry) + caps de custo
> ee0bc63 feat(vision-mcp): MCP Registry manifest com.mcorch/vision-mcp + runbook de publish (FR-VM-011)
> 54151e8 docs(vision-mcp): SOP de instalação do conector + registro dos Key Files (Lei 2)
> 74c7a27 docs(vision-mcp): sela motor dual do deepsearch (OTD-VM-024) + fecha cap diário (OTD-VM-025)
> ```

## 🤖 Claude *(05:21:05)*


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

> **Tool Result (Unknown Tool)** - ✅ Success
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
> --- scratch ---
> ⚠️ scratch/ has files
> --- HANDOFF lines ---
> 7996 HANDOFF.md
> ```

## 🤖 Claude *(05:21:06)*


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

## 🤖 Claude *(05:21:07)*


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

## 🤖 Claude *(05:21:08)*


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
> mcorch_vision_mcp: Up 2 hours (healthy)
> mcorch_claude_mem: Up 37 hours (healthy)
> mcorch_chroma: Up 37 hours (healthy)
> ---
> mega-brain-dashboard: Up 37 hours
> mega-brain-webhook: Up 37 hours (healthy)
> mega-brain-daemon: Up 37 hours (healthy)
> ```

## 🤖 Claude *(05:21:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "curl -s http://localhost:8001/api/v2/heartbeat; echo \"\"; echo \"--- vision mcp ---\"; curl -s -o /dev/null -w \"%{http_code}\" http://127.0.0.1:3200/ 2>/dev/null; echo \"\"",
  "description": "Chroma + Vision MCP health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {"nanosecond heartbeat":1781673669907505839}
> --- vision mcp ---
> 401
> ```

## 🤖 Claude *(05:21:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/ 2>/dev/null; echo \"--- scratch ---\"; ls scratch/ 2>/dev/null && echo \"\u26a0\ufe0f scratch/ has files\" || echo \"scratch/ clean \u2705\"; echo \"--- HANDOFF lines ---\"; wc -l HANDOFF.md",
  "description": "BoK suites, scratch, HANDOFF size"
}
```

## 🤖 Claude *(05:21:18)*


## 🤖 Claude *(05:21:18)*

TypeScript: zero errors. Now reading HANDOFF head + tail, sprint priorities, and scratch contents.

## 🤖 Claude *(05:21:19)*


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
> 14	## Session Seal — Vision MCP Fatia 3 remainder: PAT UI + Claude Code install + Plugin/Registry + caps de custo (2026-06-17)
> 15	
> 16	`/handson` → o Sovereign puxou as 3 frentes do roadmap vision-mcp ("continue"). Closed-Loop respeitado — mapeei o contrato BoK vivo (FR-VM-003/011 · DD-VM-003 · OTD-VM-024/025) ANTES de codar. Tudo o que restava da Fatia 3 até o **limite não-gated** foi entregue e provado material; o que sobra é gated (OAuth browser-flow → 1º tenant externo), deferido (`mistral`/`vision.ocr`) ou Sovereign-side (publish DNS, Stripe live, Resend, atribuição ML).
> 17	
> 18	**O que foi entregue:**
> 19	1. **PAT issuance UI + install no Claude Code (FR-VM-003):** `useMcpTokens` gera PAT **100% client-side** (CSPRNG 32B → base64url → `mcorch_pat_…`; **SHA-256 só do hash** persiste, byte-idêntico ao verifier do container; plaintext exibido **uma vez**), lista e revoga (UPDATE `revoked_at`) — tudo RLS-own. `useVisionMcp` (estado do conector). `McpConnectorsCard` em **Settings → Connectors** (URL copiável + snippet `.mcp.json` + escopos + reveal-once + download do plugin). `.mcp.json` ganhou o bloco `vision-mcp` (`Bearer ${VISION_MCP_PAT}` — sem segredo versionado). `types.ts` regenerado do schema vivo (purely additive: `mcp_access_tokens`/`vision_jobs`/`vision_artifacts`). PAT do Usuário Zero mintado e gravado em `.env` (gitignored).
> 20	2. **Plugin Zip + MCP Registry (FR-VM-011):** `packages/vision-mcp-plugin/` (.claude-plugin + .mcp.json + 3 skills PT-BR `/vision-essence` `/reference-brief` `/competitive-vision`) → `public/plugins/vision-mcp-plugin-1.0.0.zip` (build script reprodutível). Manifesto `packages/vision-mcp-core/server.json` (`com.mcorch/vision-mcp`, schema oficial **2025-12-11**, remote `streamable-http` → `mcp.mcorch.com/mcp`, header Bearer PAT) + runbook de publish (DNS TXT `v=MCPv1` em `mcorch.com` = **gate Sovereign**).
> 21	3. **OTD-VM-024 — motor dual selado:** blueprint **§8-A** sela Gemini Google-Search grounding como 2º motor legítimo do `deepsearch.run` (Firecrawl permanece no `deepsearch.scrape`), fundamentado em ai.google.dev/gemini-api/docs/google-search; `source_allowlist` best-effort no run (redirect `vertexaisearch`) é propriedade aceita. SDD OTD-VM-024 → **FECHADA**.
> 22	4. **Caps de custo (DD-VM-003 / OTD-VM-025):** `deepsearch.run` ganhou cap de `planned_units` **per-plano** (10/25/50, resolvido da subscription, fail-soft→starter) + **cap diário per-tenant** (25/100/500, conta `vision_jobs` charged>0 do dia, BYOK bypassa, fail-open em erro de contagem) — throw **antes** do deduct. `validation_failed` agora carrega `field`+`message` (FRD §4.4). SDD OTD-VM-025 → cap diário implementado.
> 23	5. **Anticorpo (Lei 2):** SOP `docs/processes/vision-mcp-connector-install.md` (Operator/Sequence/Gates/Recovery/Success do fluxo de install + gotcha do CF bot-challenge no curl cru) + Key Files registrados em CLAUDE.md.
> 24	
> 25	**ORO:** Operator=MCORCH Agent · Reviewer=Sovereign + `/security-review` independente (SAFE) · Owner=Sovereign (PAT = credencial que gasta carteira FM-VM-06; caps = proteção financeira da chave-plataforma).
> 26	
> 27	| Verificação (material) | Resultado |
> 28	|---|---|
> 29	| **Handshake PAT pela URL pública** `mcp.mcorch.com` | ✅ `initialize` + `tools/list`(7) + `mesh_search` tenant-scoped `scope:user:<sub>+system` `isError=false` · revoke HTTP 204 |
> 30	| Plugin Zip servido | ✅ origem nginx **200 `application/zip` 4650B** byte-idêntico (CF 403 no curl público = bot-challenge; browser passa) |
> 31	| Caps de custo (smoke LIVE zero-cost) | ✅ **3/3** — C1 per-plano over→`validation_failed` `1..10` · C2 boundary 10→`insufficient_balance` · C3 daily→`daily_cap_reached` rate_limit, balance intacto, sem 26º job |
> 32	| Testes / tsc | ✅ pkg **55/55** (+5 caps) · tsc 0 (root+pkg) |
> 33	| Container | ✅ rebuild→image `7710b832` healthy · `/health` 7 tools |
> 34	| `server.json` | ✅ JSON válido + required fields (`$schema`/name/description/version/remotes) |
> 35	| Revisão | ✅ `/security-review` independente **SAFE** (0 achados) — sub/encodeURIComponent, RLS-own, CSPRNG, sem secret exposto |
> 36	| Commits | `08739b3` (PAT UI+install) · `2f3e4df` (Plugin Zip) · `d3b8aeb` (caps) · `74c7a27` (OTD-VM-024) · `54151e8` (SOP+KeyFiles) · `ee0bc63` (Registry) · `cf5ef7c` (readme) (+ handoff) |
> 37	
> 38	### Survival Laws Self-audit
> 39	```
> 40	Law 1 (Materiality): ✅ Cada claim provada — handshake MCP+PAT REAL pela URL pública (não loopback/browser), smoke 3/3 zero-cost contra o container SERVIDO, origem nginx 200 byte-idêntico, pkg 55/55, /security-review independente SAFE. Embed do handoff node falhou no 1º payload (param drift `{record}`→`{node_id}`) e foi re-emitido + verificado (embedded=true). Fase 5c executada.
> 41	Law 2 (Process): ✅ Mapeei o contrato BoK vivo antes de codar (pegou que per-plan/daily caps fechavam OTD-VM-025); SOP de install (anticorpo) escrita ANTES do seal; caps/PAT são extensões de features com SOP existente (deepsearch-async / pat-and-erasure). Sem migration nova (types regen ≠ migration).
> 42	Law 3 (Pruning): ✅ Sessão longa empacotada — puxei 5 itens (PAT→Plugin→caps→OTD→Registry) em vez de selar a 45%; só selei com o roadmap NÃO-gated esgotado (calibração [[feedback_context_budget_calibration]]).
> 43	Law 4 (ORO): ✅ Triplet declarado no início; split Sovereign(DNS/gate)/Agent(código) explícito; "continue" como GO incremental.
> 44	```
> 45	
> 46	## Session Seal — Vision MCP público: `mcp.mcorch.com` LIVE pelo Cloudflare (OTD-VM-013 fechada) (2026-06-16)
> 47	
> 48	Ativação do vhost (último item Sovereign-side da Fatia 3). O Sovereign cuidou do Cloudflare (DNS + WAF) e eu do nginx/origem + verificação material. **`mcp.mcorch.com` está LIVE ponta-a-ponta** — o Vision MCP saiu do loopback `127.0.0.1:3200` e agora é consumível por hosts MCP externos.
> 49	
> 50	**Setup em produção:**
> 51	- **Cloudflare:** A record `mcp` → `137.131.243.179`, **proxy laranja** (esconde o IP da origem; escolha Sovereign). SSL/TLS mode **Full**.
> 52	- **Origem (eu, sudo):** vhost `nginx/mcp.mcorch.com.conf` instalado em `/etc/nginx/sites-enabled/` (SSE-tuned: `proxy_buffering off`, 3600s) + cert **self-signed** em `/etc/nginx/ssl-certificates/mcp.mcorch.com.{crt,key}` (CF Full aceita — não valida origem).
> 53	- **⚠️ DESCOBERTA crítica:** CF laranja **desafia clientes não-browser** por padrão (`cf-mitigated: challenge` "Just a moment") — o browser passa o JS, mas SDK/curl/Claude-connector **não**, então o endpoint MCP ficava silenciosamente bloqueado. Fix: **WAF Custom Rule "Skip" por host** (`http.host eq mcp.mcorch.com` → ignora Managed rules + Super Bot Fight + Browser Integrity Check + Security Level). Sem isso, laranja mata o MCP.
> 54	
> 55	**ORO:** Operator=MCORCH Agent (nginx/origem) + Sovereign (Cloudflare DNS/WAF) · Reviewer=Sovereign · Owner=Sovereign (exposição pública do endpoint).
> 56	
> 57	| Verificação (material, do datacenter pelo CF público) | Resultado |
> 58	|---|---|
> 59	| `GET /health` via CF | ✅ **200** · 7 tools JSON · sem challenge |
> 60	| `POST /mcp` sem bearer | ✅ **401** `identity_unverified` · `server: cloudflare` · sem `cf-mitigated` |
> 61	| **Handshake MCP real + JWT** (`https://mcp.mcorch.com/mcp`) | ✅ `mesh_search` retornou nós **tenant-scoped** (`scope: user:<sub>+system`, `cost_mco:0`) |
> 62	| Adversarial sem token | ✅ rejeitado no handshake (`identity_unverified`, layer identity) |
> 63	| Cleanup | ✅ usuário throwaway deletado (zero resíduo; lição: `$UID` é readonly no bash) |
> 64	| Commits | `d9a0fea` (OTD-VM-013 + runbook) · `b973787` (readme) (+ handoff) |
> 65	
> 66	**Caveat selado:** cert self-signed só funciona em CF SSL **Full** (não strict). Se o zone virar Full-strict → emitir CF Origin Certificate (`*.mcorch.com`) e trocar.
> 67	
> 68	### Survival Laws Self-audit
> 69	```
> 70	Law 1 (Materiality): ✅ Cada claim provada por curl/handshake REAL do datacenter pelo CF público (não browser, não loopback) — pegou que o browser passava mas o cliente programático era bloqueado (cf-mitigated: challenge); só declarei LIVE após o handshake MCP+JWT retornar tenant-scoped. Throwaway user limpo (zero resíduo).
> 71	Law 2 (Process): ✅ Verifiquei materialmente ANTES de afirmar (browser ≠ cliente programático); BoK/runbook atualizados pra refletir a realidade (OTD-VM-013 fechada, WAF-skip obrigatória) na MESMA sessão.
> ```

## 🤖 Claude *(05:21:20)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 7596,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 7596	       campaign_id · content_id · metadata{affiliate_id, resolved_url, self_healed_from}
> 7597	
> 7598	  6. Return: {success, original_url, resolved_url, affiliate_url, self_healed, link_id}
> 7599	
> 7600	ContentLibraryPage monetization flow:
> 7601	  Card (text, body contains mercadolivre.com.br)
> 7602	    └── DropdownMenu → "Monetizar Links ML"
> 7603	          → handleMonetizeLinks(item):
> 7604	               match(ML_URL_RE) → unique URLs
> 7605	               for url of unique:
> 7606	                 POST process-affiliate-link → affiliate_url
> 7607	                 body.split(url).join(affiliate_url)
> 7608	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 7609	          → Badge 💰 ML (emerald) exibido após monetização
> 7610	```
> 7611	
> 7612	---
> 7613	
> 7614	## Pending Actions (Commercial Launch)
> 7615	
> 7616	### CRITICAL — Must complete before first client
> 7617	
> 7618	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 7619	
> 7620	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 7621	
> 7622	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 7623	
> 7624	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 7625	
> 7626	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 7627	
> 7628	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 7629	
> 7630	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 7631	
> 7632	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 7633	
> 7634	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 7635	
> 7636	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 7637	   ```bash
> 7638	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 7639	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 7640	   ```
> 7641	
> 7642	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 7643	
> 7644	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 7645	
> 7646	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 7647	
> 7648	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 7649	
> 7650	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 7651	
> 7652	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 7653	
> 7654	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 7655	
> 7656	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 7657	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 7658	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 7659	
> 7660	### SOCIAL — Next steps
> 7661	
> 7662	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 7663	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 7664	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 7665	
> 7666	### NON-CRITICAL
> 7667	
> 7668	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 7669	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 7670	- `browserslist` — ✅ updated (2026-04-26)
> 7671	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 7672	
> 7673	### GITNEXUS MCP — Next steps
> 7674	
> 7675	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 7676	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 7677	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 7678	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 7679	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 7680	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 7681	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 7682	
> 7683	### PHASE EPSILON — Next iterations
> 7684	
> 7685	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 7686	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 7687	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 7688	
> 7689	### CORE — Next iterations
> 7690	
> 7691	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 7692	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 7693	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 7694	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 7695	
> 7696	### PHASE DELTA — Next iterations
> 7697	
> 7698	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 7699	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 7700	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 7701	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 7702	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 7703	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 7704	
> 7705	### USUÁRIO ZERO — Checklist de validação
> 7706	
> 7707	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 7708	- ✅ Stripe sandbox secrets no vault
> 7709	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 7710	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 7711	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 7712	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 7713	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 7714	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 7715	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 7716	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 7717	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 7718	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 7719	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 7720	
> 7721	---
> 7722	
> 7723	## Infrastructure
> 7724	
> 7725	| Service | Container | Port | Status |
> 7726	|---------|-----------|------|--------|
> 7727	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 7728	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 7729	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 7730	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 7731	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 7732	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 7733	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 7734	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 7735	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 7736	
> 7737	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 7738	
> 7739	```bash
> 7740	docker compose up -d
> 7741	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 7742	```
> 7743	
> 7744	---
> 7745	
> 7746	## Security Model (Post-Go-Live)
> 7747	
> 7748	| Table | Isolation |
> 7749	|-------|-----------|
> 7750	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 7751	| `mcorch_edges` | Same pattern |
> 7752	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 7753	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 7754	
> 7755	---
> 7756	
> 7757	## Billing Architecture
> 7758	
> 7759	| Decision | Value |
> 7760	|----------|-------|
> 7761	| Canonical billing ledger | `profiles.mco_balance` |
> 7762	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 7763	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 7764	| Orchestration cost | 10 mcoCoins/run |
> 7765	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 7766	| Stripe | Sandbox keys active — swap to live before first client |
> 7767	
> 7768	---
> 7769	
> 7770	## GraphRAG State
> 7771	
> 7772	- **8922 total nodes** (verificado live 2026-06-17 via REST count=exact, vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 7773	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 7774	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 7775	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 7776	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 7777	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 7778	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 7779	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 7780	- HNSW cosine index operational
> 7781	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 7782	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 7783	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 7784	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 7785	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 7786	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 7787	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 7788	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 7789	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 7790	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 7791	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 7792	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 7793	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 7794	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 7795	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 7796	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 7797	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 7798	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 7799	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 7800	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 7801	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 7802	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 7803	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 7804	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 7805	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 7806	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 7807	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 7808	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 7809	
> 7810	### Embedding Model
> 7811	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 7812	Schema: `vector(768)` — HNSW cosine index.
> 7813	
> 7814	### Embedding Pipeline (Autônomo — 2026-05-03)
> 7815	Três camadas eliminam intervenção manual:
> 7816	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 7817	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 7818	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 7819	
> 7820	### Comandos de manutenção da Mesh
> 7821	```bash
> 7822	# Verificar nós sem embedding (deveria retornar array vazio):
> 7823	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 7824	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 7825	
> 7826	# Backfill manual (Bun-native — requer .env):
> 7827	bun run scripts/backfill-embeddings.ts
> 7828	
> 7829	# Backfill de código-fonte nos nós AST:
> 7830	bun run scripts/backfill-node-content.ts
> 7831	
> 7832	# Re-sync AST completo:
> 7833	cd packages/gitnexus-core && npm run sync-mesh
> 7834	
> 7835	# Acompanhar re-ingesta pós-commit:
> 7836	tail -f /tmp/mcorch-ingest.log
> 7837	```
> 7838	
> 7839	---
> 7840	
> 7841	## Video Rescue Protocol
> 7842	
> 7843	When a video generation operation (Google Veo) times out or client disconnects:
> 7844	```bash
> 7845	# Via edge function (production):
> 7846	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 7847	  -H "Authorization: Bearer <user_jwt>" \
> 7848	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 7849	
> 7850	# Via local script (admin/debug):
> 7851	source .env && bun run rescue.ts <operation_id> <content_id>
> 7852	```
> 7853	
> 7854	---
> 7855	
> 7856	## Architecture Pillars
> 7857	
> 7858	| Layer | Implementation |
> 7859	|-------|---------------|
> 7860	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 7861	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 7862	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 7863	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 7864	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 7865	
> 7866	---
> 7867	
> 7868	## Phase Delta — Architecture
> 7869	
> 7870	```
> 7871	OrchestrationPage (full-canvas, p-0)
> 7872	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 7873	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 7874	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 7875	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 7876	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 7877	        ├── nodes/PublishNode.tsx    ← final distribution output
> 7878	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 7879	        └── NodePalette.tsx          ← top toolbar to add nodes
> 7880	
> 7881	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 7882	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 7883	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 7884	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 7885	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 7886	```
> 7887	
> 7888	### Canvas State Architecture (Hybrid)
> 7889	
> 7890	```
> 7891	User interaction → ReactFlow internal state (positions, drag)
> 7892	                         ↓ (debounced 600ms)
> 7893	                   localStorage (positions persist across refresh)
> 7894	                         ↑
> 7895	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 7896	     ↓ (status changes sync to ReactFlow via useEffect)
> 7897	ReactFlow renders visual status (idle/running/done/error/blocked)
> 7898	```
> 7899	
> 7900	## Key Files
> 7901	
> 7902	| Purpose | Path |
> 7903	|---------|------|
> 7904	| Architecture rules | `CLAUDE.md` |
> 7905	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 7906	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 7907	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 7908	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 7909	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 7910	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 7911	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 7912	| **Node types** | `src/components/orchestrator/nodes/` |
> 7913	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 7914	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 7915	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 7916	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 7917	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 7918	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 7919	| Billing utilities | `src/lib/billing.ts` |
> 7920	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 7921	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 7922	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 7923	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 7924	| Video rescue (local) | `rescue.ts` |
> 7925	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 7926	| Backfill script | `scripts/backfill-embeddings.ts` |
> 7927	| Deploy harness | `scripts/harness-deploy.sh` |
> 7928	
> 7929	---
> 7930	
> 7931	## First Client Onboarding Checklist
> 7932	
> 7933	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 7934	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 7935	3. ~~Activate watchdog cron~~ ✅ Done
> 7936	4. ~~Deploy rescue-video function~~ ✅ Done
> 7937	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 7938	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 7939	7. Monitor `infra_health_logs` for first 24h.
> 7940	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 7941	
> 7942	---
> 7943	
> 7944	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 7945	
> 7946	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 7947	
> 7948	| Action | Result |
> 7949	|--------|--------|
> 7950	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 7951	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 7952	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 7953	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 7954	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 7955	
> 7956	| Commit | Conteúdo |
> 7957	|--------|----------|
> 7958	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 7959	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 7960	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 7961	
> 7962	### Arquitetura Matrix Intelligence
> 7963	
> 7964	```
> 7965	ConstellationMatrix (Stabilized Engine)
> 7966	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 7967	  └── NodeDetailsPanel (Tabbed Navigation)
> 7968	        ├── Tab Meta: Neighbor exploration + Net Context
> 7969	        ├── Tab Code: Source code preview (Supabase sync)
> 7970	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 7971	
> 7972	useNodeIntelligence Hook:
> 7973	  - contentQuery: fetch nodes.content column
> 7974	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 7975	  - state: isAnalyzing, analysisResult, progress
> 7976	```
> 7977	
> 7978	---
> 7979	
> 7980	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 7981	
> 7982	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 7983	
> 7984	| Action | Result |
> 7985	|--------|--------|
> 7986	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 7987	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 7988	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 7989	
> 7990	**Output da análise (estruturado em pt-BR):**
> 7991	- Visão Geral — papel do módulo no sistema
> 7992	- Padrões Detectados — design patterns, antipatterns
> 7993	- Acoplamento & Dependências — análise In/Out-Degree
> 7994	- Recomendações — 1-3 ações priorizadas
> 7995	
> ```

> **Tool Result (Unknown Tool)** - ✅ Success
>
> ```
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun  7 14:41 .
> drwx------ 30 ubuntu ubuntu 4096 Jun 17 01:06 ..
> --- sprint priorities ---
> -rw-rw-r-- 1 ubuntu ubuntu 117715 Jun 17 01:07 .claude/context/sprint-priorities.md
> EXISTS
> ```

## 🤖 Claude *(05:21:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la scratch/ 2>/dev/null; echo \"--- sprint priorities ---\"; ls -la .claude/context/sprint-priorities.md 2>/dev/null && echo \"EXISTS\" || echo \"MISSING\"",
  "description": "Scratch contents and sprint file check"
}
```

## 🤖 Claude *(05:21:28)*


## 🤖 Claude *(05:21:29)*

Now the sprint goal (head of sprint-priorities.md) and the BoK gate completeness check.

## 🤖 Claude *(05:21:30)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md",
  "limit": 60
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
> 7	**Sprint v6.40.0 — Vision MCP Fatia 3 remainder: PAT UI + install Claude Code + Plugin/Registry + caps de custo (2026-06-17)** — `/handson` → Sovereign puxou as 3 frentes do roadmap ("continue"). Closed-Loop: mapeei o contrato BoK vivo (FR-VM-003/011 · DD-VM-003 · OTD-VM-024/025) antes de codar. **Entregue (até o limite NÃO-gated):** **(1) PAT UI (FR-VM-003)** — `useMcpTokens` gera PAT 100% client-side (CSPRNG 32B→SHA-256, só o hash persiste byte-idêntico ao verifier; plaintext uma vez), lista/revoga RLS-own; `McpConnectorsCard` em Settings→Connectors; `.mcp.json` wired (`Bearer ${VISION_MCP_PAT}`); types regen. **Install no Claude Code provado por handshake MCP+PAT REAL pela URL pública** (`initialize`+`tools/list`7+`mesh_search` tenant-scoped); **(2) Plugin Zip + MCP Registry (FR-VM-011)** — `packages/vision-mcp-plugin/`→`public/plugins/…zip` + 3 skills PT-BR; manifesto `server.json` `com.mcorch/vision-mcp` (schema oficial 2025-12-11, remote streamable-http) + runbook (publish **gated** no DNS TXT Sovereign); **(3) OTD-VM-024** — blueprint §8-A sela motor dual (Firecrawl scrape + Gemini grounding run, fundamentado ai.google.dev) → FECHADA; **(4) caps (DD-VM-003/OTD-VM-025)** — `deepsearch.run` cap per-plano 10/25/50 + diário 25/100/500 (BYOK bypassa, fail-open em count error, throw antes do deduct); `validation_failed` ganha field+message (FRD §4.4). Anticorpo Lei 2: SOP `vision-mcp-connector-install.md`. **Prova:** pkg **55/55** · tsc 0 · smoke-vision-cost-caps **3/3 LIVE** zero-cost · origem serve plugin 200 byte-idêntico · `/security-review` independente **SAFE** · container `7710b832` · 8 commits · Phase 5c **SEAL ALLOWED** (10) · mesh **8922** · handoff `c21c53db`. **Top Gap restante (tudo gated/Sovereign-side):** OAuth browser-flow (1º tenant externo) · `mistral`/`vision.ocr` (deferidos) · publish no MCP Registry (DNS challenge) · Stripe live · domínio Resend · atribuição compra ML. **Lição:** mapear o contrato BoK vivo antes de codar mostrou que per-plan+daily caps fechavam OTD-VM-025 na mesma sessão; e provar o install pelo handshake REAL da URL pública (não loopback/browser) é o que valida "Claude Code conecta" (Lei 1).
> 8	
> 9	**Sprint v6.39.1 — Vision MCP público: mcp.mcorch.com LIVE pelo Cloudflare (OTD-VM-013 fechada) (2026-06-16)** — ativação do vhost (último item Sovereign-side da Fatia 3). Split: Sovereign cuidou do Cloudflare (A record `mcp`→137.131.243.179 proxy **laranja** + SSL **Full** + **WAF Custom Rule Skip** por host), eu do nginx/origem (vhost `sites-enabled` SSE-tuned + cert **self-signed**, CF Full aceita) + verificação. **`mcp.mcorch.com` LIVE ponta-a-ponta** — Vision MCP saiu do loopback, consumível por hosts MCP externos. **DESCOBERTA crítica (gravada na BoK + memória):** CF laranja **desafia clientes não-browser** por padrão (`cf-mitigated: challenge` "Just a moment") → browser passa o JS mas SDK/curl/Claude-connector NÃO → **WAF skip por host é OBRIGATÓRIA** pra qualquer endpoint MCP/API atrás de CF laranja. Provado material (do datacenter, pelo CF público): `/health` 200, `/mcp` sem token 401, **handshake MCP real+JWT → mesh_search tenant-scoped 200**, sem-token rejeitado. Caveat: self-signed só em Full (não strict). 3 commits · Phase 5c **SEAL ALLOWED** (10) · mesh **8921** · handoff `0632e1f8`. **OTD-VM-013 FECHADA.** **Lição:** browser ≠ cliente programático — só declarei LIVE após o handshake MCP+JWT do datacenter (não o `/health` no navegador do Sovereign), que é o que pegou o challenge bloqueando os clientes reais (Lei 1).
> 10	
> 11	**Sprint v6.39.0 — Vision MCP Fatia 3 core: PAT external auth + LGPD erasure + nginx vhost (2026-06-15)** — próximos passos, Sovereign escolheu "Fatia 3 core + vhost config" (de 4 opções). Closed-Loop: mapeei o contrato BoK (data-model §2.1/§2.3 + SDD §5.2/§5.3/§7) antes de codar. **Entregue:** (1) **PAT** (FR-VM-003) — `mcp_access_tokens` (SHA-256 + **allowlist de scopes no DB** + teto 365d + RLS own) + `auth/pat.ts` + **dispatch PAT-vs-JWT** em `verifyBearer` (JWT→ALL_SCOPES; PAT→subset) + **scope-gate por tool** (`requireScope` → 403, default-deny); (2) **erase LGPD** (FR-VM-009) — `vision_artifacts` + `erase_vision_artifacts` (cascade **re-escopo `user_id` por DELETE**, sem primitiva cross-tenant) + retention-sweep diário; (3) **nginx** `mcp.mcorch.com.conf` SSE-tuned + runbook (ativação = DNS Sovereign). **Correção apply-reality OTD-VM-026:** `storage.objects` storage-admin-owned → deleção via Storage API pelo caller (RPC retorna `storage_paths`); bucket privado + RLS bucket-scoped default-deny já isolam. `mistral_api_key`/`vision.ocr` deferidos. 3 migrations aplicadas+registradas (Management API) · `/security-review` independente **SAFE** (0≥8) · smoke **7/7** LIVE (PAT scope-gate/revoke/expiry + erase zero-residue + cross-tenant guard) · pkg **50/50** · tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8920** · handoff `e0695dad` · 6 commits · container `fda2784f`. OTD-VM-020 marcada **PAT-first IMPLEMENTADA**. **Top Gap novo:** ativação do vhost (DNS Cloudflare — Sovereign) · OTD-VM-024 emenda BoK do engine + per-plan `planned_units` (DD-VM-003) + cap diário per-tenant (OTD-VM-025) · resto Fatia 3 (OAuth 2.1 browser-flow + Plugin Zip + UI de emissão de PAT + `mistral_api_key`/`vision.ocr`). **Lição:** o 42501 do `DELETE storage.objects` (SECURITY DEFINER não-owner) só apareceu no smoke contra o DB servido — testar o artefato servido pegou um defeito de realidade-de-apply do stub SDD (corrigido + OTD-VM-026); o mapeamento do contrato BoK antes de codar evitou improviso (Lei 2).
> 12	
> 13	**Sprint v6.38.0 — Vision MCP `deepsearch.run`/`poll` async (FR-VM-007 · job→poll→partial-refund §4.5) (2026-06-15)** — `/handson` → Sovereign puxou o item #1 do roadmap vision-mcp. Closed-Loop: workflow de **mapeamento (5 readers)** leu contrato selado + schema vivo + wiring ANTES do código — e **pegou que minha premissa contradizia a BoK** (a SDD sela **Firecrawl**, não "google/gemini"). Surfaceei; Sovereign decidiu (custom): *"não pagar Firecrawl agora; usar chaves já disponíveis"* → motor = **Gemini Google-Search grounding** (chave `google` já provisionada; BYOK→plataforma→402), **desvio consciente OTD-VM-024** (débito de emenda BoK); contrato job/refund/state 100% fiel à BoK. **Entregue:** `deepsearch.run` (3 mco, débito-na-entrada→`job_id`→worker in-process→refund parcial §4.5 floor-a-favor-do-tenant) + `deepsearch.poll` (grátis, tenant-bound, **self-heal de órfão**); `vision_jobs` (SELECT-own RLS) + **RPC atômico `finalize_vision_job`** (service-role-only, terminal+refund 1×/job); menores (`infra_health_logs` event/metadata + OTD-VM-023 orphan-sub). **Reviews:** workflow adversarial 5-lentes (2 HIGH: charge-without-value + refund-atomicity → fechados com finalize+reconcile) + **recuperação dos 3 verify mortos por session-limit** dos transcripts (achado novo: sem teto GLOBAL da chave-plataforma → **OTD-VM-025** semáforo; bucket era só per-sub) + allowlist de telemetria (side-channel cross-tenant) + erro de provider opaco + sentinel no `source_allowlist` + URLs http(s) + CHECK `refunded_mco≤charged_mco`. `/security-review` independente **SAFE** (0≥8). pkg **46/46** · tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8918** · handoff `fc0b5efc` · 6 commits · container `b24360c8` smoke **10/10** LIVE. **Top Gap novo:** Fatia 3 (PAT/OAuth/Plugin/jobs/erase LGPD) · vhost nginx OTD-VM-013 (root Sovereign) · cap diário per-tenant + rate-limiter compartilhado (OTD-VM-014/025) · emenda BoK do engine (OTD-VM-024) · per-plan `planned_units` (DD-VM-003). **Lição:** o workflow de mapeamento pré-código pegou a contradição Firecrawl-vs-Gemini ANTES de eu codar a coisa errada (Lei 2); e recuperar findings órfãos de transcript (em vez de re-rodar) achou 1 HIGH novo de custo que o /security-review (classe DoS excluída) não pegaria.
> 14	
> 15	**Sprint v6.37.0 — Vision MCP Fatia 2: 4 Billable Tools + BYOK Foundation (+ Fatia 1 handshake/interop close) (2026-06-15)** — diretiva começou em "fechar a última ponta não-provada da Fatia 1 (mesh.search E2E com JWT)" e o Sovereign mandou seguir até a Fatia 2 inteira ("algo completo", "você escolhe a ordem"). **(1) mesh.search E2E fechado + bug crítico de Fatia 1:** o E2E com cliente MCP real pegou que o servidor reusava **um** `StreamableHTTPServerTransport` stateless (SDK proíbe reuso → `notifications/initialized` **500**, nenhum cliente completava handshake) → fix fresh-per-request; provado **7/7** + adversarial **6/6** (forja ES256 ×3 + injeção PostgREST ×7). **(2) Interop de protocolo** (achado pelo `/security-review` independente): gate aceitava só `2025-11-25`, 400-ando clientes 3rd-party → ampliado p/ `SUPPORTED_PROTOCOL_VERSIONS`; cliente cru heterogêneo **8/8** (`2025-03-26`/`2025-06-18`). **(3) Fatia 2 — fundação** (SOP Lei 2 + `infra/billing.ts` + `auth/credentials.ts` + `safety/duty-of-care.ts`: BYOK→plataforma→402 · deduct-on-entry+refund-on-failure · sentinel · duty-of-care) + **4 tools billable provados:** `vision.describe_image` (FR-VM-018, 7/7), `vision.analyze_video` (FR-VM-024 Gemini — **não Higgsfield** — cobrança/min, 7/7), `deepsearch.scrape` (FR-VM-007 Firecrawl BYOK-only, 4/4), `mesh.consolidate_reference` (FR-VM-021 escrita tenant-escopada, 5/5). **(4)** migration `firecrawl_api_key` Vault (`/security-review` limpo · aplicada+registrada) + UI Settings **deployada** + SSRF redirect-fix (achado do review). pkg **34/34** · tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8917** · handoff `7a45d8ef` · 7 commits. **Top Gap novo:** `deepsearch.run` async (a metade "google/gemini" — FR-VM-007 job/poll) · Fatia 3 (PAT/OAuth/Plugin/jobs/erase LGPD) · vhost nginx OTD-VM-013 · OTD orphan-sub. **Lição:** o `/security-review` independente pagou de novo (achou o SSRF por redirect + o defeito de interop de protocolo que o cliente do mesmo-SDK mascarava); testar contra o ARTEFATO SERVIDO pegou o bug de handshake.
> 16	
> 17	**Sprint v6.36.2 — Vision MCP: OTD Gates Closed + Fatia 1 Built & Deployed ON (2026-06-15)** — diretiva Sovereign "ambos em sequência" (gates por pesquisa → código). **(1) Gates OTD pré-GA** (workflow `wf_0040a939-232`, 3 lentes verify adversarial): **OTD-VM-004 CLOSEABLE** (grade mcoCoins 4×-floor sobrevive — custo fonteado por provider, nenhuma sub-margem; `segment` cost-aware obrigatório; SOP `vision-mcp-cost-calibration.md`); **OTD-VM-001 CLOSEABLE** (corrigiu 2 erros factuais do blueprint — UEyes/Imp1k EXISTEM, SOTA=**SUM**/MIT self-hostável não DeepGaze; recall≥0.95 fundamentado); **OTD-VM-006 CLOSEABLE** (14 licenças verdes LICENSE-fetched + 3 minas banidas; SpikingJelly não-MIT); **OTD-VM-005 PARTIAL** (SCCs-ANPD inviável; Res. 32/2026 UE adequada; Mistral=default candidato). **(2) Fatia 1 construída + DEPLOYADA ON** (`packages/vision-mcp-core/` → container `mcorch_vision_mcp` Sovereign Mesh, restart=unless-stopped, UID1001, read-only, `127.0.0.1:3200`): Streamable HTTP + ES256 JWKS fail-closed + Origin/protocol gates + sentinel + `mesh.search` tenant-safe. Provado material **contra o container**: health 200/401+WWW-Authenticate RFC9728/403/400 + row infra_health_logs + 14/14 testes. **2 bugs que só o deploy pegou:** bind `0.0.0.0` (port-map do bridge) + schema real de `infra_health_logs` (sem `metadata` — o padrão do sentinel edge falha silencioso). tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8916** · handoff `98fa83d7` · 4 commits. **Top Gap novo:** mesh.search E2E com JWT (handshake MCP) · vhost nginx `mcp.mcorch.com` (OTD-VM-013, root Sovereign) · Fatia 2 (foveal billable + per-user creds) · migration `infra_health_logs ADD metadata jsonb` (telemetria rica). **Lição:** testar o ARTEFATO SERVIDO (container), não o node local — Lei 1 pegou 2 bugs + 1 schema drift que unit/local não veriam.
> 18	
> 19	**Sprint v6.36.1 — Vision MCP: BoK 9/9 + 8-Agent System + Adversarial Validation (2026-06-15)** — diretiva Sovereign (ref. sandcastles.ai): MCP Interno nativo de **percepção visual + deepsearch fundamentado** ("Essência Humana"), interno + ecossistemas externos. Closed-Loop BoK-first em 3 atos: **(1) Blueprint-semente v0.2.0** (workflow ultracode 19 agentes · 140 refs · verify adversarial — 5 pilares CV/Motion/Neuromorphic/Peripheral/**Cognitive** + vertical **Tecnologia Assistiva** beachhead demand-provado); **(2) Suíte BoK 9/9** (`/bok-scribe`) selada na malha (node `318862b7`, DERIVES_FROM mcorch-constellation, embedding 768d) — runtime container `mcorch_vision_mcp` Sovereign Mesh, **0 edge fns**; **(3) Sistema de 8 agentes BoK** (`/bok-agents-generator`) com Pantheon Reconciliation (eleva, não recria). **Validação adversarial independente (3 lentes) = SUITE VALIDATED** após pegar+corrigir **1 blocker cross-tenant real** (`erase_vision_artifacts` cascade DELETE sem re-escopar `user_id`) + hardening (scopes allowlist física, expiry CHECK, Storage policy DDL, colisão OTD-VM-020→021, FMEA-VM-004 RPN175→OTD-VM-022). Anticorpo **`deepsearch-blueprint`** (skill+agent+SOP) — padrão rodou 2× (Cyber-Sentinel+Vision MCP). tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8915** · handoff `b73d141d` · README badge `6.36.0-vision-mcp`. 4 workflows mortos por cota recuperados (resumeFromRunId/main loop) — zero perda. **Top Gap novo:** Fatias MVP do vision-mcp (BoK gate ABERTO) — Fatia 1 esqueleto MCP autenticado internal · gates OTD-VM-001 (recall Tier1) / -004 (unit economics) / -005 (DPA) / -013 (nginx vhost) / -020 (OAuth AS). **Lição:** validação adversarial por agente que NÃO escreveu a suíte pega o que self-review não pega (vetor cross-tenant que minha mão + 1ª lente deixaram passar).
> 20	
> 21	**Sprint v6.36.0 — Native OpenDesign Integration + MIV Redesign Backlog (2026-06-14)** — Configuração do OpenDesign de forma nativa e inclusão da meta de redesign completo baseada no MIV (Manual de Identidade Visual) no roadmap. **(1) Nativização do OpenDesign** (`CanvasDesignPage.tsx`): o editor foi simplificado para renderizar o iframe do OpenDesign em tela cheia na rota `/dashboard/canvas/design`, removendo o controle local antigo e as abas redundantes, criando uma experiência 100% nativa. **(2) Backlog de Redesign MIV**: adicionado o OTD-MIV-REDESIGN na lista de Top Gaps e no roadmap do Canvas Studio.
> 22	
> 23	**Sprint v6.35.0 — Core-Fable: Fable 5 Flagship + Metering + Mega Brain Interstellar (2026-06-10)** — Diretiva Sovereign "Refatore todo o nosso Core-v2 para Core-Fable" em 3 arcos: **(1) Rebrand** (`914f8dd`): rota `/dashboard/core-fable` (+redirects compat), `CoreFablePage`/`components/core-fable/`, Claude Fable 5 (`anthropic/claude-fable-5` via OpenRouter, verificado live no catálogo) como default do Core; seletor de chat **desacoplado** do `pref_ai_model` (localStorage) — 1 clique não re-modela o flywheel pago. **(2) Review adversarial pré-deploy confirmou 4 P1 econômicos** (`997b307`): aios-chat OpenRouter nascia SEM metering (billing bypass na chave-plataforma) → `_shared/agent-metering.ts` compartilhado fiado nos 2 paths; `agent_pricing` sem rows novas → under-billing 133-167× via fallback flash → migration `20260610010000` seeda fable-5 1000/5000 + sonnet-4.6 300/1500 + dropa id morto; `/security-review` SAFE. Provado live: probe `{"output":"Claude"}` + ledger correto + `calc_agent_cost_mcoin`=120. **(3) Mega Brain Interstellar** (`3b15e41`→`47f9316`): loop iterativo de 8 screenshots dirigido por referência visual do Sovereign — câmera quase equatorial + 210 steps adaptativos = arco lensado contínuo sobre a sombra; **raios capturados = preto** (matou anel de névoa + bola branca do glow artificial — críticos precisam ~310 steps/órbita); disco blackbody edge-on, reação por energia (surge/spin/shimmer). tsc 0 · suíte **295** · Phase 5c **SEAL ALLOWED** (10) · mesh **8865** · handoff `4728b8aa`. **Top Gap novo:** OTD-FABLE-MARGIN (margem 2.0 do calc < 4×-floor p/ chat premium) · fallback `pricing_not_found` silencioso (fail-caro + telemetria). **Lição:** o screenshot-loop com sessão real no preview local (sem tocar o dist servido) pegou 2 bugs visuais que tsc/testes jamais veriam (GLSL só falha em runtime); e o review adversarial pagou de novo — 4 P1 econômicos numa feature "só de rename".
> 24	
> 25	**Sprint v6.34.0 — Cyber-Sentinel: Security BoK 4/4 + Prompt Gate Live + Infra Hardening (2026-06-10)** — diretiva CISO executada em 2 fases na mesma sessão. **(1) BoK de segurança 4/4** (`docs/bok/security/`, schema CISO 01-brd/02-srs/03-sdd/04-fmea — 12 BR-SEC + Risk Ledger · 15 FR-SEC + matriz RLS canônica + `SET LOCAL` · SDD lefthook/Arcjet/sentinel/Dockerfile UID1001/compose cap_drop integrais · FMEA 12 modos RPN AIOS). **(2) Aplicação no ecossistema vivo** (`6f2f75a`): **Sentinel LIVE** em `orchestrate-content` (prod **v52**) — `_shared/sentinel.ts` barra injeção/bypass/ANSI **depois da identidade, antes do `deduct_mco_coins`**; provado em prod com JWT real (`HTTP 403 layer=sentinel` score=3, **zero mcoCoins**). Infra recriada e endurecida: `claude_mem` uid1001+read_only+8caps (healthy), `chroma` caps conservadoras+no-new-privileges (heartbeat vivo), `gitnexus` imagem não-root buildada; env `SUPABASE_SERVICE_ROLE_KEY` revogada removida do compose (FM-04). Gate git **dual-engine** lefthook+gitleaks (pre-commit/pre-push, degrada sem gitleaks — OTD-SEC-003). **Review adversarial pegou 4 bugs reais ANTES de qualquer deploy quente**: rate-limiter falsava o fan-out paralelo de `campaign-run`; `cap_drop SETUID/SETGID` quebraria o `chroma` de terceiros; regex de 1 qualificador; guard `&&||` do gitleaks engolia a detecção. tsc 0 · suíte **295** · Phase 5c **SEAL ALLOWED** (10) · mesh **8862** · handoff `0a9865a9` + BoK seal `424f0fe4`. **Próximos:** FM-10 gitnexus (imagem pronta, roda stdio) · OTD-SEC-006/007 (fiar sentinel + migration `security_events`/quarentena <50ms nas demais fns pagas) · Arcjet aguarda superfície Next/BFF. **Lição:** verificar **materialmente** (dry-run dos containers, exploit real em prod) antes de declarar — pegou o `name:` que orfanaria os containers e os 4 bugs do review.
> 26	
> 27	**Sprint v6.33.1 — Hotfix Kanban ScrollArea + E2E à Prova de Cloudflare (2026-06-09)** — bug report do Sovereign no `/dashboard/kanban`: `ReferenceError: ScrollArea is not defined` ao criar coluna. **Causa:** `KanbanPage.tsx` usava `<ScrollArea>` (área scrollável de tarefas) sem importar — só quebrava *depois* da 1ª coluna (empty-state não exercita o componente). **Fix de 1 linha** (`e55ce70`): import `@/components/ui/scroll-area`; deploy material (chunk novo `KanbanPage-CW7WBYjZ.js` ≠ o do stack trace, import scroll-area + env baked); **confirmado em prod pelo print do Sovereign**. **E2E completo** via preview local do `dist` + sessão injetada (CF Turnstile barra agent-browser do datacenter até no `login.mcorch.com`): CRUD + drag-drop bidirecional **provado pelo DB** (3× PATCH 200 + SELECT, não pelo DOM). Helper `gen-user-session.ts` (`761ea6f`) p/ E2E logado à prova de CF. **Incidente de concorrência** (Sovereign mexendo em prod junto) resolvido sem perda de dado — board/coluna intactos, a "divergência" da 1ª rodada era o Sovereign movendo o mesmo card. tsc 0 · suíte **284** · Phase 5c **SEAL ALLOWED** (10) · mesh **8860** · handoff `fd20b125`. **Lição:** E2E mutável vai em board descartável, nunca no dado real do Sovereign; DB-prod é compartilhado. **Diretiva CISO de hardening DEFERIDA** (blueprint `6b1571a` commitado; 4 artefatos BoK de segurança p/ sessão dedicada).
> 28	
> 29	**Sprint v6.33.0 — ML Attribution Fix + Browser Operator BoK (2026-06-08)** — o teste **real** do Sovereign no branded link expôs o flywheel emitindo link **MORTO**. **(1) Fix do auto-monetize** (`34d7ef0`): `_shared/affiliate.ts` `buildMlProductUrl` montava o formato BARE `mercadolivre.com.br/MLB-<id>` (404) com 2/3 ids stale → agora resolve `vm_affiliate_products.product_url` real (fonte única Apify), fail-open `/p/`; **reconcilia "ML não conta clique"** (era 404, não falha do matt_word — o painel ML já contara matt_word em produto VÁLIDO em 2026-06-04); provado E2E `7993c6a4` 302 → `/p/MLB27834876`; deploy `orchestrate-step` 122.8kB. **(2) BoK 9/9 do Operador de Browser Autenticado** (`/bok-scribe`, `24ba435`): suíte 756 LOC MR→SDD+STRIDE+FMEA; **gate pagou** — o link oficial é per-user → nova `user_affiliate_links` (não a `vm_affiliate_products.affiliate_template_url` COMPARTILHADA, que vazaria entre tenants — OTD-ABO-003); runtime residencial cravado (datacenter **403** reprovado em produto real `/p/`, bare e `/afiliados/hub`); mesh seal `31323fe3` + DERIVES_FROM edge `9ea18d26` → mercado-livre-api. tsc 0 · suíte **284** · Phase 5c **SEAL ALLOWED** (10) · mesh **8852** · handoff `630509e2`. **Top Gap:** **BUILD do Operador** (gate ABERTO; runtime residencial = Sovereign roda `agent-browser` logado no ML) · domínio Resend · conversão ML real. **Lição:** o teste por **mão do Sovereign** (clicks 0→4) achou o link morto que meu curl-403 do datacenter mascarava; o BoK-first pegou o vazamento cross-tenant **antes** do código.
> 30	
> 31	**Sprint — Stored-XSS Hardening + Antibody (2026-06-08)** — `/security-review` (v6.28.0) havia flagado stored-XSS em `DashboardHome` (`content_library.body` cru via `dangerouslySetInnerHTML`); fechado **ponta-a-ponta** nesta sessão. Sanitização `DOMPurify.sanitize` (já shipada via Antigravity em `da9da4c`/`e5a661a`) + guarda de regressão **6 testes** (`dashboard-html-sanitize.test.ts`: preserva `<a href>` de afiliado + tags de artigo, remove `<script>`/`onerror`/`javascript:`) + **antibody ESLint `no-restricted-syntax`** (`2522e71`, sem dep nova — `eslint-plugin-react` ausente) que faz todo `dangerouslySetInnerHTML` futuro acusar no lint até ser sanitizado+justificado (sink cru plantado → **pego** material; 2 sinks legítimos justificados: DashboardHome DOMPurify · chart.tsx CSS shadcn) + limpeza dos **7 `no-explicit-any`** do data-layer de DashboardHome (`3129369`). Handoff node `e12ed58e` + obs antibody `505fb670` (embedded 768d). tsc 0 · suíte verde · mesh **8849**. **Anticorpo Permanente cumprido** — reincidência do sink barrada no lint. **Top gaps restantes (herdados de v6.28.0, gated no Sovereign):** domínio `RESEND_FROM` (entrega Resend real) · branded redirect `login.mcorch.com/go` · 2 rascunhos WP de teste · atribuição de compra ML.
> 32	
> 33	**Sprint v6.32.x — arco Core-v2 Black Hole (2026-06-07, via Antigravity)** — sessões conduzidas no Antigravity, seladas e versionadas no git, registradas aqui retroativamente a partir dos records do HANDOFF.md (não reauditadas em detalhe — Lei 1): **v6.32.6** Unified Relativistic Black Hole & Cymatics (fusão dos visualizadores num único shader WebGL Schwarzschild — raymarching + disco de acreção + Doppler beaming + ondas de cymatics; layout 30/70; `CymaticsLayer` removido; 284 testes; handoff `ec6204a4`; mesh 8847); **v6.32.5** Model Selector Fix & Reacting Black Hole (fix case-collision dos hooks `useAiosTerminalChat`/`useAiosWorkspaceChat`; persistência do modelo selecionado em `user_api_keys`; redesign MegaBrainVisualizer + CymaticsLayer; 260 testes; handoff `8627661a`; mesh 8839); **v6.32.2** Gemini 3.1 Live Mode (Live API → Gemini 3.1 Flash Live audio-only + Gemini Docs MCP + API Skills; handoff `5acba7aa`; mesh 8818). Os seals intermediários (v6.29–v6.32.4) existem em HANDOFF.md/README mas não foram back-filled aqui.
> 34	
> 35	**Sprint v6.28.0 selado em 2026-06-04** — **Quatro next-steps fechados numa sessão (probe-first)**. Diretiva Sovereign "ataque os 4 pontos numa sessão só, não pare até terminar; o ponto 4 do link não funcionou a contabilidade de clicks" (+ screenshot ML com 1 clique). Cada gap verificado **no código** antes de tocar. **(1) OTD-INTENT-DISPATCH-REFUND FECHADA:** `orchestrate-content` estorna os 10 em falha pós-débito (`!runId` ou erro do kick `async_orchestrate_step`) + marca run `error` — estende o contrato refund da v6.27.2 ao núcleo do flywheel. **(2) nurture-dispatch entrega Resend real (FR-MH-008):** resolve `resend_api_key` per-user (BYOK) + `leads.contact` → POST Resend quando email+chave+endereço; senão `gated`; send `failed` estorna. Live a inbox real ainda gated em `RESEND_FROM` (domínio Sovereign). **(3) Click ledger in-system (OTD-ML-CLICKS):** links publicados passam pelo redirect `process-affiliate-link` GET, que registra o clique atômico (RPC `record_affiliate_click` service-role-only, atribuído ao dono) + 302 pro ML; `link-forge` emite o redirect; **ROIWidget já soma `affiliate_links.clicks`** → "Cliques Totais" reflete cliques reais antes de compra; migration 120000 + fix 130000 (`content_id` UUID). **(4) 1º dispatch pago E2E agentic:** intent→policy→execute→orchestrate-content WP **draft**, run `43048d8e` **done**, **delta 10 exato** (valida ponto 1 em prod), HITL gate provado, blast-radius wordpress-only. **Prova:** `/security-review` independente **SAFE** · drift audit **exit 0** · smoke-affiliate-click **10/10** + smoke-nurture **10/10** · suíte **269** · tsc 0 · deploys 107.9/83.72/87.96kB · Phase 5c **SEAL ALLOWED** (7 verified) · Mesh **8783**. 6 commits. **Novo Top Gap:** entrega Resend a inbox real (domínio `RESEND_FROM` — Sovereign) · branded redirect domain (`login.mcorch.com/go` proxy nginx — link limpo+rastreado) · 2 rascunhos WP de teste a limpar · atribuição de compra ML (aguardando conversão). **Lição:** probe-first economizou retrabalho (ROIWidget já somava clicks → zero UI nova; `resend_api_key` já existia → só o canal) e pegou o bug 22P02 do RPC (content_id UUID) no smoke antes de declarar — corrigi via migration na mesma sessão (regra hotfix→migration). **Follow-up (mesma sessão, "continue com os próximos"):** click ledger estendido ao caminho **interativo** de monetização — POST `process-affiliate-link` retorna redirect rastreável `?link_id` (migration `20260604140000` + RPC `record_affiliate_click_by_link`). O smoke estendido (G8) expôs um insert de `affiliate_links` quebrado há tempo (`campaign_id` UUID vs slug `"ai_orchestration"` → 22P02 silencioso, nenhuma linha de afiliado nunca persistida) + o `/security-review` independente pegou um **open-redirect** no branch novo (302 pro `short_url` tenant-writável) — ambos corrigidos (gate de domínio ML + UUID-só); smoke **9/9** (G9 prova o open-redirect bloqueado), commit `b2c39f6`. **Follow-up 2 ("faça todos os 3"):** (A) **auto-monetização** no `orchestrate-step` — o artigo gerado embute o redirect rastreável `?link_id` per-owner (`_shared/affiliate.ts`), o flywheel monetiza+rastreia automático; provado E2E pago run `cee55b11` (Roborock → link rastreável no `content_mesh_asset`). (B) **matt_tool** per-user (coluna `affiliate_config` + threading GET/POST/orchestrate + UI `AffiliatesPage`; caveat honesto: efeito na atribuição ML não-verificável, mas aditivo). (C) **campaign-run assíncrono** p/ >8 passos (`EdgeRuntime.waitUntil`, batches; pequenas seguem síncronas). `/security-review` independente **SAFE** (flagou XSS **pré-existente** `DashboardHome:677` dangerouslySetInnerHTML → tarefa spawned). Smokes click **G1-G9+G1b** · campaign **A-H** · e2e auto-monetize ✅ · tsc 0 · drift exit 0. 4 commits (`9bb5bba`/`bb999c1`/`7cbd036`/`b468c98`).
> 36	
> 37	**Sprint v6.27.2 selado em 2026-06-04** — **Refund-on-failure: charge-without-value fechado (OTD-AEO-REFUND)**. Diretiva Sovereign "continue com os próximos passos". Probe-first material elegeu o item de **menor blast radius e maior valor seguro** dos 3 next-steps (refund protege saldo do usuário, zero ação outward); os outros 2 dependem do Sovereign (nurturing externo precisa de domínio Resend verificado — **zero refs RESEND no código**; 1º pago E2E precisa de GO econômico). **OTD-AEO-REFUND FECHADA:** `aeo-audit` debitava 5 mco na entrada e, se o persist falhasse, devolvia 500 **sem estornar** (charge-without-value, verificado no código). Helper compartilhado **`refundMco`** (`_shared/billing.ts` → `add_mco_coins`, service-role-only, simétrico a deduct, guarda `p_amount>0`, nunca lança); `aeo-audit` (5) e `lead-score` (1) rastreiam `charged` e estornam em qualquer falha pós-cobrança (persist-fail + catch). **Prova:** smoke `smoke-aeo-refund.ts` **6/6 LIVE** (deduct 5→15 / add 5→20 restaurado · guarda nega -10 · net-zero) + unit `_shared/billing.test.ts` **4/4** + regressão aeo-audit intacta. **Honestidade Lei 1:** persist-fail não é forçável por input → fiação coberta por unit+code, não por falha forçada (declarado). Contrato refund-on-failure no billing SSOT (`mcoin-cost-calibration.md`). Deploys 86.69/85.62kB · tsc 0 · suíte **269** (265→269) · Phase 5c **SEAL ALLOWED** (8 verified) · Mesh **8774** (1 órfão `aeo:` podado). 3 commits. **Novo Top Gap:** entrega externa de nurturing (bloqueada por domínio Resend — Sovereign) · 1º pago E2E (GO econômico) · **OTD-INTENT-DISPATCH-REFUND** = aplicar `refundMco` ao gap pós-débito do `orchestrate-content` (flywheel, sessão dedicada). **Lição:** probe-first descartou 2 dos 3 next-steps (dependência externa) e leu o código pra confirmar que o gap de refund era REAL (linha 56 débito → 118 persist-fail sem refund) antes de construir — não assumi o bug, verifiquei.
> 38	
> 39	**Sprint v6.27.1 selado em 2026-06-03** — **Intent executor un-gated: dispatch outward REAL + OTD-INTENT-TRANSITION-GUARD**. Diretiva Sovereign "ACTIVATE AGENTIC OUTWARD EXECUTION" (Step 1 guard ANTES do Step 2 dispatch). **(1) OTD-INTENT-TRANSITION-GUARD (migration `20260603270000`):** trigger `tr_guard_intent_plan_transition` (`SECURITY DEFINER`/`search_path=''`) deixa **só `service_role`** colocar uma linha em `status='approved'`/`'executed'`. **O `/security-review` (subagente independente) pegou que meu guard inicial era BEFORE UPDATE-only → vetor INSERT aberto** (tenant `POST intent_plans {status:'approved'}` pulava o HITL e cavalgava a re-validação até dispatch). Estendi p/ **BEFORE INSERT OR UPDATE** + endureci a RLS `insert_own` (`status IN proposed/auto_approved/pending_hitl`) + `tr_validate_intent_plan_bindings` (binding = mesmo tenant). **Prova material before/after**: INSERT `status='approved'` por JWT de tenant → **201 ANTES / 403+42501 DEPOIS**. **(2) Dispatch outward REAL (un-gate):** `intent-execute` pós-`executed` roteia por precedência — `campaign_id`→campaign-run · `enrollment_id`→nurture-dispatch · senão canais content/social/affiliate→orchestrate-content — encaminhando o **JWT do chamador** (cascata self-bila o mesmo tenant). Kill-switch `INTENT_OUTWARD_DISPATCH_ENABLED=false`→governança-only. Idempotência: marca executed 1º (re-execute=already, sem dobro de dispatch/cobrança). `db push` Finished · types regen · deploy 83.01kB. **Smoke 28/28 LIVE throwaway** (guard INSERT+UPDATE 42501 · golden rule · dispatch REAL provado por **downstream guard a saldo 0**: orchestrate-content **402** + campaign-run **422**, zero gasto · binding foreign rejeitado). tsc 0 · eslint 0 · suíte **265** · drift audit **exit 0**. BoK patcheada (SDD + data-model) + SOP reescrita (gates 4/5/6 + OTD-INTENT-DISPATCH-REFUND). **Novo Top Gap:** entrega externa real de nurturing (gated; `resend_api_key` pronto) · **OTD-INTENT-DISPATCH-REFUND** (refund pós-dispatch-fail) · 1º dispatch pago E2E real (gated em GO Sovereign — UI HITL + guard já armados). **Lição:** o `/security-review` independente pegou o furo INSERT que o self-review (focado no PATCH) deixou passar — exatamente o vetor que a diretiva mandava fechar; provar before/after material (201→403) separa "guard escrito" de "guard que funciona" (Lei 1).
> 40	
> 41	**Sprint v6.27.0 selado em 2026-06-03** — **Marketing-Hub: rosto + executor + AEO (FR-MH-009/010)**. `/handson` → `/goal` Sovereign com os 3 próximos passos ("backend pronto, falta o rosto"). **(1) Executor de `intent_plans` (FR-MH-009 HITL):** edge fn `intent-execute` (approve/reject/execute) na máquina `proposed→pending_hitl→approved|rejected→executed`; **golden rule** = o `execute` **re-valida** o alto-impacto sobre o plano **armazenado** (gate compartilhado `_shared/intent-policy.ts`) e recusa `409 hitl_required` todo outward sem aprovação humana — **nunca confia em `auto_approved`**; tenant-guard 404; `/security-review` SAFE → adotada **fail-closed** em plano não-array; smoke **17/17**. **(2) AEO (FR-MH-010 — última FR):** `aeo_audits` (RLS) + `aeo-audit` (JWT · 5 mco atômico · provider **degradado documentado** OTD-MH-003 LLM-as-answer-engine · 1 snapshot/query); `db push` Finished; smoke **12/12** (RLS cross-tenant leaked=0). **(3) UI follows:** `useIntentOrchestrator`/`useAEO` + `IntentOrchestratorPanel`/`HITLApprovalCard`/`AEOAuditPanel` + enroll de nurturing no Customer 360 → `/dashboard/marketing`; **+8 testes (257→265)**; **UI logada verificada** (magic link Usuário Zero + agent-browser, chunk novo, zero crash). tsc 0 · eslint 0 (tocados) · build 22.88s deploy nginx. 5 commits. **Novo Top Gap:** dispatch outward real do executor (hoje gated) + **OTD-INTENT-TRANSITION-GUARD** (CHECK de transição antes de ligar o envio real) · entrega externa de nurturing (gated; credencial pronta) · **OTD-AEO-REFUND** (refund pós-débito). **Marketing-hub: TODAS as FRs backend+UI entregues** (001..012). **Lição:** probe-first viu que o gate de policy já existia inline no orchestrate → extraí p/ `_shared` em vez de duplicar (o `execute` re-roda **o mesmo** gate, não uma cópia); o `/security-review` independente pegou o fail-open que o self-review deixaria passar.
> 42	
> 43	**Sprint v6.26.0 selado em 2026-06-03** — **Drift audit + P0 ledger + 3 FRs marketing-hub**. `/handson` → diretiva Sovereign "🔴 auditar drift deployado↔migrations" (irmãos do hotfix `async_orchestrate_step`) → "faça 2+3+4". **(1) Drift audit:** 9 superfícies via Management API read-only (ledger 96==96 · contrato RPC 12/12 · verify_jwt edge 23==23 · 34 triggers · RLS toda-tabela · pg_net siblings) → **incidente ISOLADO**; único drift real `rls_auto_enable` (event-trigger out-of-band benigno que liga RLS em tabela nova) **capturado** + 6 SECURITY DEFINER `search_path` travado + trigger pg_net morto (kong:8000) dropado. Anticorpo `scripts/qa/audit-schema-drift.sh` (8 checagens, exit 0) + SOP `schema-drift-audit.md`. **(2) 🔴 P0 ledger:** os 3 RPCs (award/add_user_score/deduct) davam EXECUTE a anon/authenticated + confiavam `p_user_id` → cunhagem de mcoCoins via PostgREST direto; REVOKE (edge-only) + guardas em deduct (sinal + posse NULL-safe); **exploits provados BLOQUEADOS** em prod (erro/42501/permission denied). **(3) functionName 13/13** fallback LLM. **(4) FR-MH-008 cron** (`nurture-cron`+pg_cron `*/15`, modo service-role em nurture-dispatch; smoke 5/5+USER 10/10). **(5) FR-MH-012 BYOK** (`resend_api_key` per-tenant Vault — defs VIVAS verbatim — +Settings; round-trip 8/8). **(6) FR-MH-009 Intent+HITL backend** (`intent_plans`+`intent-orchestrate`: policy auto/HITL canal-outward-fail-safe + rationale XAI; smoke 8/8). 9 commits · 3 migrations · 4 deploys · `/security-review` independente por migration (todas SAFE) · Phase 5c **SEAL ALLOWED** (11 verified) · Mesh **8770** (orphan de smoke limpo) · Survival Laws **4/4**. **Novo Top Gap:** UI follows (enroll nurturing — hook já existe — + `useIntentOrchestrator`/`HITLApprovalCard`) · executor de `intent_plans` (re-validar ação outward no execute) · entrega externa nurturing (gated; credencial pronta) · FR-MH-010 AEO (última FR). **Lição:** probe-first viu que a metade-IA do FR-MH-012 já existia (só a metade-canal era nova) + evitou o trap do template stale de credenciais (reproduzir defs VIVAS, não migration antiga); o drift audit virou anticorpo reexecutável.
> 44	
> 45	**Sprint v6.25.0 selado em 2026-06-03** — **Flywheel ressuscitado + calibração mcoCoins**. `/handson` → diretiva Sovereign ("o que falta pro 1º run pago E2E + já calibrar o COIN_COST?"). Calibrei **antes** do run (não rodar a 1ª transação econômica a preços inventados): **OTD-MCOIN-CALIBRATION FECHADA** — modelo `mco=ceil(custo_usd/$0.018_piso×4)` (piso=Enterprise); surpresa honesta — `10` (orchestrate) e `125` (canvas vídeo) **já** eram ~4× sobre custo real, único furo `IMAGE_GENERATION 3→9` (`CONTENT_GENERATION 5→2`). O **1º run pago E2E então expôs que o flywheel de conteúdo estava MORTO desde o cutover de chaves (01-06)** — 3 P0s compostos deixavam todo run preso em `running`: **#1** `orchestrate-step` faltava no `config.toml` (`verify_jwt=true` → gateway **401** na chave opaca `sb_secret_` do pg_net); **#2** `async_orchestrate_step` hotfixada em prod **sem migration** (`p_service_jwt_legacy`≠`p_service_key` → **PGRST202** → auto-chain morto) → migration `20260603190000` realinha + `GRANT service_role`, `/security-review` SAFE, RPC **204**; **#3** `wp_site_url` não-www → **301 → POST vira GET** → WP devolve LISTA de posts → `publish-wordpress` endurecido (valida `id`, 502 honesto) + `wp_site_url→www`. **Provado E2E**: run `89f18bea` **auto-completou 6/6 passos sem kick** → rascunho WP `?p=14` + `content_mesh_asset` done. Phase 5c **SEAL ALLOWED** (11 verified). Mesh **8769**. Survival Laws **4/4**. 7 commits. **Novo Top Gap:** auditar **drift deployado↔migrations** (outras RPCs/fns hotfixadas em prod?) · limpar artefatos de teste (5 posts parqueados 2027 + 2 rascunhos WP) · FR-MH-009/010/012 + Nurturing follow-up · functionName nas 9 fns. **Lição:** o 1º run pago **não "falhou"** — fez seu trabalho: expôs 3 P0s silenciosos no coração do produto (falha sem erro visível, sem auto-refund); calibrar **antes** do run foi a decisão certa (transação econômica honesta).
> 46	
> 47	**Sprint v6.24.0 selado em 2026-06-03** — **Sessão de alta densidade** (diretiva Sovereign: selar a 45% é desperdício → usar a janela 1M inteira, selar só a ~95%; **Lei 3 recalibrada** em survival.md: poda≠selar). Resposta ao "faça os três, foco em endurecer o flywheel": 5 entregas pós-v6.23.0, cada uma com **smoke LIVE throwaway**. **(1) MVP-5 Atribuição (FR-MH-007)**: `handle-ml-postback`→`marketing_attribution` (campaign_id FK-safe, fail-soft) + `useCampaignAttribution`+card "Receita Atribuída"; smoke DB 4/4 (FK 23503 + de-linked). **(2) Hardening+observabilidade (FOCO)**: `eslint .` **honesto** (Deno `supabase/functions`+tailwind excluídos — ~3716 erros falsos, exit mascarado por `| tail`) + functionName telemetry no flywheel + smoke integração lead→score→campaign→attribution 5/5. **(3) Customer 360 (FR-MH-011)**: VIEW `security_invoker` RLS-safe + `useCustomer360`+drawer; /security-review SAFE + **isolation smoke 4/4** (B não vaza p/ A). **(4) Nurturing (FR-MH-008)**: engine `sequences`+`sequence_enrollments` (FK composta CASCADE) + `nurture-dispatch` **consent-gated** (envio gated) + `useNurturing`+`NurturingPanel`; /security-review SAFE + **consent-gate smoke 10/10**. 2 migrations /security-review SAFE (subagentes independentes) · tsc 0 · suíte **259** · eslint exit 0 honesto · 4 deploys · 5 smokes LIVE. Phase 5c **SEAL ALLOWED** (11 verified). Mesh **8761** (orphan obs de smoke limpo + smoke vacinado). Survival Laws **4/4**. 8 commits. **Novo Top Gap:** 1º run pago E2E (gated GO) · Nurturing follow-up (entrega externa real + cron + UI enroll/dispatch) · OTD-MCOIN-CALIBRATION · FRs restantes FR-MH-009/010/012. **Lição:** densidade máxima por sessão (5 frentes numa só) sem perda de materialidade — cada uma provada por smoke LIVE; o gate de lint estava mentindo (exit mascarado) — fix de raiz restaura honestidade da Lei 1.
> 48	
> 49	**Sprint v6.23.0 selado em 2026-06-03** — Marketing Hub backend completo + **MVP-4 UI live**: `campaign-run` (FR-MH-004) fechou o backend, depois o módulo inteiro ganhou rosto em `/dashboard/marketing` **absorvendo a UI v1** (não duplicando). **(1) campaign-run** JWT + débito atômico do FEE `CAMPAIGN_RUN` (10) → dispatch **paralelo** (`Promise.allSettled`) dos passos p/ `orchestrate-content` (self-bila 10) = **cascata fiel 10+10×N**; `email`→blocked; cap 8; smoke **13/13 zero-custo** (guards + isolamento de tenant + email-blocked + débito atômico 100→90 + cleanup); deploy 80.92kB; cascata paga **gated em GO**. **(2) MVP-4 UI**: `/dashboard/marketing` (LeadBoard 5 colunas + Pontuar/`lead-score` + overview campanhas; nav Target) + absorção v1 (`CampaignWizard` +Intenção/passo **Passos** composer→persiste `campaign_steps`; `CampaignDetail` +card **Passos & Execução** status vivo + `CampaignRunButton`). **(3) Hooks**: `useLeads`/`useLeadScore`/`useCampaignSteps`/`useCampaignRun`/`createCampaignWithSteps` + `src/lib/edge.ts`. tsc 0 · **11 testes** (suíte **255/257**) · eslint limpo nos tocados · build 22.32s deploy nginx · **UI LOGADA verificada** (magic link + agent-browser: `/dashboard/marketing` + wizard 6-passos/Passos renderizam, 0 erros console, zero mutação prod). Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8760**. Survival Laws **4/4**. 4 commits. **Novo Top Gap:** 1º run pago E2E (Sovereign cria campanha→Rodar, gated em GO) · OTD-MCOIN-CALIBRATION ($) · OTD-CAMPAIGN-RUN-ASYNC (fila p/ campanha grande) · MVP-5 attribution→ROIWidget · **dívida de lint repo-wide** (~3716 erros pré-existentes em `supabase/functions` Deno, exit mascarado por `| tail` — não introduzidos nesta sessão). **Lição:** a diretiva Sovereign de calibração de contexto (1M/Max → não adiar por "contexto" antes de ~400k) destravou rodar o MVP-4 completo numa sessão; probe-first pegou a UI v1 existente ANTES de codar (absorver, não duplicar); a11y do agent-browser estava stale na transição framer-motion → li o stepper-text em vez de fabricar (Lei 1).
> 50	
> 51	**Sprint v6.22.0 selado em 2026-06-03** — Campaign Core + LLM Fallback + Lead Scoring: 4 entregas materiais via `/handson`→ação nos alertas→próximos priores. **(1) Alerta meta_config** verificado **VAZIO** (0 linhas · `auth.users` 1==`profiles` 1 — não fabriquei limpeza inexistente, Lei 1). **(2) MVP-2 Campaign Core LIVE** (migration `20260603025256`): `campaigns` **ABSORVIDA** via `ALTER` (+intent/channels/mesh_node_id + `UNIQUE(id,user_id)`) + `campaign_steps` (FK composta tenant-`CASCADE`, espelha lead_events) + `marketing_attribution` (FK simples `SET NULL` + RLS `WITH CHECK`, espelha consents); tenant-FK provado **comportamental** (23503 + 42501 autenticado + 201 + zero-resíduo); `/security-review` **SAFE** (subagente independente); mesh `7628892b`. **(3) OTD-LLM-FALLBACK FECHADA cedo** (SLA 06-07, owner engineer): probe-first achou o helper já live em 11 fns → fechei o gap de observabilidade do SOP (telemetria `infra_health_logs` autossuficiente em Deno) + **1º teste de edge-helper do projeto** (6 casos) + 11 fns redeploy; mesh `6061a6d2`. **(4) lead-score LIVE** (FR-MH-003): JWT + 1 mco atômico + IA per-user→sistema fail-soft; **smoke E2E** 200 · score=80 (`source=ai`) · débito 100→99 · zero-resíduo. **Calibração mcoCoins**: `COIN_COSTS` centralizado + dívida **OTD-MCOIN-CALIBRATION** (o `10` é redondo, não $-calibrado; `orchestrate` cobra 10 flat < soma dos componentes 18; vídeo é o maior custo real). Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8759**. Survival Laws **4/4**. 6 commits. **Novo Top Gap:** `campaign-run` cascata fiel (**ADIADA por decisão Sovereign** — código financeiro + contexto saturado, Lei 3) + OTD-MCOIN-CALIBRATION (preços $ por-modelo/vídeo) · MVP-4 hooks+UI `/dashboard/marketing` · MVP-5 attribution. **Lição:** probe-first pegou a OTD já 80% pronta (zero retrabalho) e a divergência `campaigns`/`campaign_metrics` já-existentes; decisão financeira de `campaign-run` **registrada ao Sovereign em vez de improvisada** (Master Protocol).
> 52	
> 53	**Sprint v6.21.0 selado em 2026-06-03** — Marketing Hub (v2): BoK 9/9 + 11 agentes + MVP-1 Lead Core LIVE. Novo **módulo soberano** criado do zero seguindo o Master Execution Protocol (BoK-first), dirigido pela diretiva Sovereign de um "Framework Universal de Marketing (Plataforma Agentic)" (benchmarks HubSpot/Salesforce). `/bok-scribe` selou a **suíte BoK 9/9** (1732 LOC, `docs/bok/marketing-hub/`, traceability **0 órfãos**, mesh seal `d5163fed` DERIVES_FROM meta-api) — módulo nasce como **v2 de consolidação** que **absorve e escala** o marketing v1 disperso (orchestrate-content → executor de campanha; whatsapp_leads → tutela meta-api→marketing-hub; marketing-growth Pantheon **elevado, não recriado**), natureza **Ambos** (interno Usuário Zero + comercial per-tenant). `/bok-agents-generator` produziu o **sistema de 11 agentes** (8 BoK + AEO/Intent-Orchestration/Demand-gen + Pantheon Reconciliation). Após revisão Sovereign ("aprovado"), **MVP-1 Lead Core** foi ao ar: migration `20260603000000` (`leads`/`lead_events`/`marketing_consents` + RPC `erase_lead()` LGPD SECURITY DEFINER), aplicada via `db push`. O `/security-review` (subagente **independente**) pegou **1 cross-tenant MEDIUM** (FK de tabela-filha sem co-escopar `user_id` → A injeta evento no lead de B) → fechado com **FK composta tenant-escopada `(lead_id,user_id)→leads(id,user_id)`** + provado **material** (23503 no ataque, 201 no legítimo, cleanup zero-resíduo). Phase 5c **SEAL ALLOWED** (7 verified). Mesh **8755**. Survival Laws **4/4**. 4 commits. **Novo Top Gap:** MVP-2 Campaign Core deve **ABSORVER** a `campaigns` já existente (colisão real achada por probe-first), NÃO criar nova; + MVP-3 edge fns (`lead-score`/`campaign-run`) · MVP-4 hooks+UI (`/dashboard/marketing`) · MVP-5 attribution. **Lição:** probe-first do schema ANTES de codar pegou 2 divergências doc↔realidade (`campaigns` existe, `projects` não) que quebrariam o apply; e o `/security-review` por subagente independente (não auto-avaliação) pegou o furo de tenant que o self-review deixou passar.
> 54	
> 55	**Sprint v6.20.4 selado em 2026-06-02** — Probe OAuth ML + verificação visual do disconnect (**seal de conhecimento — zero código de produção**): dirigido por 2 diretivas do Sovereign no padrão **probe-first material**. **(#1)** Fechado o resíduo visual da v6.20.3 — disconnect Meta/social verificado **NON-DESTRUTIVO** na UI logada: login como Usuário Zero via Supabase **Admin API `generate_link`** (magic link, método per-user reproduzível, sem token do DevTools nem senha) dirigindo `agent-browser` 0.27.0; `/dashboard/social` renderiza 3 contas Ativa (LinkedIn/IG/FB) com botão Desconectar **interativo** wired a `rpc('disconnect_social')` (`useMetaConfig`/`useSocialAccounts` chamam `disconnect_meta`/`disconnect_social`, zero `.delete()`); **nenhum clique** → 3 contas intactas. **(#2) probe-first do OAuth ML CONCLUÍDO** — veredito material: ML **sem API oficial de afiliados** (403 até no WebFetch da Anthropic); link oficial **exige portal LOGADO** (segui o `meli.la` → `/social/…?matt_word=…&matt_tool=…&ref=<ASSINADO>`, token `ref` **não-fabricável**); **datacenter BLOQUEADO p/ Chromium real** (`agent-browser` no portal → "Hubo un error accediendo a esta pagina"). ⇒ Browser Operator (#2) **não roda do datacenter** (runtime = navegador do user / IP residencial); resolver `src/lib/affiliate.ts` tem `matt_word` mas **falta `matt_tool`** (per-user). **Experimento de atribuição de clique em curso** (Sovereign, dispositivo independente, ~06-03) → **decisão do #2 PAUSADA aguardando o dado** (Cérebro sem mãos: não vejo o painel de afiliados — logado + IP bloqueado). Phase 5c **SEAL ALLOWED** (4 verified). Mesh **8753**. 2 commits (docs). **Novo gap (Top Gap):** decisão do Browser Operator/`matt_tool` aguarda o nº de cliques de amanhã. **Lição:** probe-first poupou construir um Browser Operator no datacenter que **nunca funcionaria** (IP bloqueado, provado material) — e refutou "OAuth resolve" (ML não tem API).
> 56	
> 57	**Sprint v6.20.3 selado em 2026-06-02** — Disconnect RPC + revogação de segredo órfão: **FECHADO o Top Gap que a v6.20.2 sinalizou** — desconectar Meta/social fazia `.delete()` pela view → INSTEAD OF DELETE só apagava a linha base, deixando o segredo Vault **órfão** (plaintext retido; 12 órfãos Meta observados em prod). RPCs `disconnect_meta()`/`disconnect_social(p_account_id uuid)` (migration `20260602160000`) espelham `disconnect_wordpress` (`SECURITY DEFINER`, `search_path=''`, fail-closed `28000`, EXECUTE só authenticated): deletam a linha **E** revogam o segredo. Guard de tenant por name-binding (`id`-de-linha + PK ⇒ atacante nunca casa nome de segredo alheio; UUID bruto nunca vaza ao cliente). Limpeza one-time **12→0** órfãos Meta (orphan-scoped via `NOT EXISTS`+`right(name,36)`), 3 sociais vivos intactos. Hooks migrados `.delete()`→`.rpc()`; `types.ts` regenerado. **Também (diretiva A):** `/security-review` redundante do `87c926f` (guard de tenant v6.20.2) → **LIMPO 9/10**. Ambos os reviews SAFE; suíte RPC 5/5 em `BEGIN…ROLLBACK` (happy meta+social · foreign-id no-op · planted-ref name-binding · unauth 28000); Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8752**. 4 commits. **Lição:** verificar materialidade ANTES de codar (Lei 1) — o gap de tenant guard da diretiva original já estava 100% fechado em prod, então a Parte B virou o foco real em vez de uma migration redundante.
> 58	
> 59	**Sprint v6.20.2 selado em 2026-06-02** — Idempotência da encriptação + guard de tenant nas views irmãs: **FECHADO o Top Gap que a v6.20.1 sinalizou** — `trg_encrypt_user_api_keys` (+ irmãos meta/social) chamava `vault.create_secret` incondicionalmente → re-salvar segredo p/ valor novo colidia no índice único `vault.secrets.name` (`23505`). Helper `public.vault_upsert_secret(value,name,desc)` (`SECURITY DEFINER`, `search_path=''`, EXECUTE revogado de PUBLIC/anon/authenticated) rotaciona in-place via `vault.update_secret` (mesmo UUID, sem órfãos) senão cria; as 3 encrypt triggers passam a usá-lo (migration `20260602140000`). O `/security-review` dessa migration **expôs um gap pré-existente** nas INSTEAD OF de `meta_config`/`social_accounts` (sem guard `auth.uid()` → injeção cross-tenant id-novo; o overwrite id-colidente já era fail-closed pelo PK — achado HIGH do review REFUTADO material) → guard `42501` portado pras 2 (migration `20260602150000`). Ambas `/security-review` **SAFE**; tudo provado material via Management API em `BEGIN…ROLLBACK` (antes 23505/injeção OK, depois OK/42501); Phase 5c **SEAL ALLOWED** (7 verified). Mesh **8751**. 6 commits. **Novo gap (Top Gap):** desconectar Meta/social deixa o segredo Vault **órfão** (INSTEAD OF DELETE só apaga a linha base) — precisa de RPC dedicada de disconnect (nula+revoga) no padrão `disconnect_wordpress()`, débito LGPD. **Lição:** adversarial-verify material (PK fail-closed + md5 da vítima) refutou um HIGH e ao mesmo tempo revelou o gap real adjacente — resolvido na mesma sessão em vez de empurrar pra fria.
> 60	
> ```

## 🤖 Claude *(05:21:33)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for slug in $(ls docs/bok/ 2>/dev/null); do\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug\" || echo \"\u26a0\ufe0f $slug \u2014 missing: ${missing[*]}\"\ndone",
  "description": "BoK gate completeness per suite"
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
> ⚠️ security — missing: 00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics
> ✅ viral-daily-canvas
> ✅ viralmind
> ✅ vision-mcp
> ```

## 🤖 Claude *(05:21:42)*


## 🤖 Claude *(05:21:43)*

Let me confirm the security BoK contents — it uses the CISO schema, not the standard 9-doc naming.

## 🤖 Claude *(05:21:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/security/ 2>/dev/null",
  "description": "List security BoK files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 00-deepsearch-blueprint.md
> 01-brd-security.md
> 02-srs-secure-spec.md
> 03-sdd-hardening-architecture.md
> 04-fmea-security.md
> ```

## 🤖 Claude *(05:22:04)*


## 🤖 Claude *(05:22:25)*

═══════════════════════════════════════════════════════════
  HANDSON — Vision MCP Fatia 3 *remainder* (selo 2026-06-17)
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
  **Fase selada:** Vision MCP Fatia 3 remainder — PAT UI + install Claude Code + Plugin/Registry + caps de custo (v6.40.0)
  Últimos commits:
   `1f1a7c4` — docs: paper de referência "From AGI to ASI" (arXiv 2606.12683)
   `3a9b634` — chore(sprint): registra v6.40.0 (PAT UI + Plugin/Registry + caps) + proof manifest
   `129dcca` — docs(handoff): sela Vision MCP Fatia 3 remainder
   `cf5ef7c` — docs(readme): v6.40.0 — conector consumível + caps de custo
   `ee0bc63` — feat(vision-mcp): MCP Registry manifest `com.mcorch/vision-mcp`

📂 **MUDANÇAS PENDENTES**
  Worktree limpo ✅ (nada uncommitted)

🏗️ **INFRA** — tudo saudável
  `mcorch_vision_mcp`: Up 2h (healthy) · `/` → **401** (esperado — exige bearer)
  `mcorch_chroma`: Up 37h (healthy) — heartbeat API v2 ✅
  `mcorch_claude_mem`: Up 37h (healthy)
  `mega-brain-{daemon,webhook,dashboard}`: Up 37h ✅

🧠 **KNOWLEDGE MESH**
  **8922 nós** (verificado live 2026-06-17 — +handoff `c21c53db` embedded 768d) · **9070 arestas** (snapshot 2026-06-01) · 100% embedded (HNSW cosine 768d)

🔧 **TYPESCRIPT** — Zero erros ✅ (`tsc --noEmit` limpo, root)

📚 **BoK SUITES** (MCORCH Master Execution Protocol)
  **19 suítes completas** (9/9 docs) — incluindo `vision-mcp` (seal `318862b7`)
  `security` aparece como "incompleto" no gate padrão **mas é falso-positivo**: usa o schema CISO (`00-deepsearch-blueprint` · `01-brd-security` · `02-srs-secure-spec` · `03-sdd-hardening-architecture` · `04-fmea-security`) — **4/4 selada em v6.34.0** (seal `424f0fe4`), não os 9 docs canônicos.
  ⚠️ **GATE alert:** nenhum bloqueador — BoK Gate ABERTO para todos os módulos ativos.

📌 **SPRINT**
  Goal: *Distribuição social autônoma operacional* (LinkedIn auto-publica; Twitter/Instagram gated em tier/App Review)
  Top gap: tudo o que resta do vision-mcp está **gated/Sovereign-side** (ver abaixo)

⚡ **PRÓXIMOS PASSOS**
O roadmap **não-gated** do vision-mcp foi esgotado no último selo. O que resta exige ação do Sovereign ou é dívida de outro módulo:

  1. **Vision MCP — itens gated (precisam de você):** publicar no MCP Registry (challenge DNS TXT em `mcorch.com`) · OAuth 2.1 browser-flow (destrava 1º tenant externo) · `mistral_api_key`/`vision.ocr` (deferidos).
  2. **Security hardening — dívida ABERTA da suíte Cyber-Sentinel:** FM-10 (Dockerfile gitnexus roda root) · OTD-SEC-006/007 (fiar sentinel + migration `security_events`/quarentena <50ms nas demais edge fns pagas) · FM-04 (env `SUPABASE_SERVICE_ROLE_KEY` legada no compose).
  3. **Flywheel comercial gated:** Stripe live keys (Usuário Zero) · domínio `RESEND_FROM` (entrega real de nurturing) · atribuição de compra ML (aguardando conversão).

⚠️ **ALERTAS**
  Nenhum alerta ✅ — TS limpo, containers saudáveis, worktree limpo, `scratch/` vazio.

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

O que destravamos agora, Maestro? Posso atacar a **dívida de Security hardening** (item 2 — é o único trilho substantivo que roda 100% do nosso lado, sem gate Sovereign), ou prefere apontar outra frente?

## 👤 User *(05:29:51)*

tive uma ideia verifique se isso faz sentido.: How to finally know if AI is lying to you (using Perplexity's Model Council)
Every time you use AI, you never know for sure if you’re getting the full truth. 
This can lose you deals, trust, money, and even your job if you're not careful. 
So I found a way to pressure-test every AI answer, so you know it's right before you act on it.
One question gets researched by 3+ models at the same time, and the final answer catches things no single model would've found on its own.
This is the same concept behind Andrej Karpathy's LLM Council method (which I wrote about previously). 
But in one click. And fully non-technical.
Here's exactly how you can set it up so you can effortlessly use it for anything you're researching:
P.S. If you want more AI workflows like this one delivered to your inbox every week, join 35k readers getting them free: aisolo.beehiiv.com/subscribe
The Blind Spot Problem
When Stanford researchers asked AI models about specific court cases, the models fabricated fake cases up to 82% of the time. 
Real-sounding case names, detailed reasoning, confident delivery.
Completely made up.
And you'd have no way of knowing, because AI models sound exactly as confident when they're wrong as when they're right.
There's zero hedge. 
No "I'm not sure about this part." 
No yellow highlight on the sentence it's least confident about. 
It all comes out the same way.
You've probably experienced this. Asked AI something important, used the answer in your work, and found out later one of the details was wrong.
After a client already noticed it…
Or after it got (embarrassingly) posted to social media…
Or after you got scolded in a meeting about it.
Why one model isn't enough
Think about it like how most people consume news.
If you only read one outlet, you get one perspective.
Their editorial angle.
Their sources.
Their framing of the story.
You already know this intuitively.
If you read a story about a new regulation on CNN, then check Reuters and the Wall Street Journal, you'll get 3 different angles on the same event.
CNN highlights the consumer impact. 
Reuters gives you the raw policy details. 
The WSJ frames it through a business lens.
None of them are lying. They're pulling from different sources, talking to different experts, and weighing different parts of the story.
You read multiple sources because that's how you get the full picture. 
The places where outlets disagree or emphasize different things are exactly the places where the real nuance lives.
AI models work the same way.
Each one was trained on different data by a different company. 
When you ask Claude a research question, it searches certain sources and weighs them a certain way.
GPT searches different sources. Gemini pulls from different places entirely.
They're all covering the same story through a different editorial lens.
So when you only ask one model, you're reading one headline and treating it like the full story.
Perplexity Model Council-maxxing
The obvious fix is to ask multiple AI models the same question and compare.
But in practice, nobody does this.
You're not going to paste the same question into ChatGPT, then Claude, then Gemini, then read all three answers and figure out where they disagree. 
That's messy and takes forever. 
But you can't ask Claude to have ChatGPT review its output.
Perplexity is the only tool that can do this effortlessly, because it's a model aggregator.
It has GPT, Claude, Gemini, and others all under one roof. 
And they built a feature called Model Council that does exactly what the news analogy suggests:
It sends your question to three models at the same time (like Claude Opus, GPT, and Gemini) and lets each one research independently.
A synthesizer model reviews all three outputs, resolves conflicts where it can, and combines the strongest findings from each.
You get one final answer that shows you a final verdict, unique findings from each model, where the models agreed, and where they disagreed.
That last part is the whole point.
The places where they disagree are the places where a single model would've given you a confident answer that missed something.
The disagreement is the signal.
This is why it's become my go-to for any question where I need to be sure I'm getting the full picture.
Here's how to turn it on:
Open Perplexity
Click the "+" on the chat bar
Select "Model Council"
Ask your question
That's it. Same interface, same search bar. The only difference is your question now gets pressure-tested by multiple models instead of one.
What happened when I counciled a legal decision
I'm considering running a live experience for my audience in Barcelona this year.
So I asked Perplexity Model Council: "I'm selling tickets from my Cyprus company for a live event in Spain. What are the tax and VAT implications?"
Three models (Opus 4.6, GPT 5.4, Gemini 3.1) researched the same question independently. Here's what happened:
Where all three models agreed:
Spanish VAT at 21% applies (not Cyprus VAT), because EU law taxes events where they physically take place
A one-off event doesn't create tax residency in Spain, so business profits stay taxed in Cyprus at 15%
I can recover VAT on local costs like venue rental and AV equipment
If I'd asked one model, I would've stopped here.
Where they disagreed:
The models split on whether I need to register directly for Spanish VAT or use the EU's One-Stop Shop system (a simplified way to handle VAT across EU countries without registering in each one).
Gemini said OSS is enough for B2C ticket sales
GPT and Claude said direct registration is better because OSS won't let me deduct local VAT costs
Same question, but totally different recommendations.
Unique discoveries only one model caught:
GPT found that bundling accommodation and meals into the ticket price (which most retreats do) triggers Spain's Travel Agency Margin Scheme. Completely different VAT structure. The fix: keep the event ticket separate and let attendees book hotels themselves.
GPT also flagged a March 2026 EU court ruling that Spain can deny VAT deductions on entertainment expenses. Group dinners at the retreat? Non-recoverable VAT. One model out of three found that ruling.
Claude caught that I should get a Cyprus tax residency certificate before the event as proof, and that I need to deregister from Spanish VAT within one month after or I'm stuck filing quarterly returns.
One question. Three models. Three different layers of the answer.
That's the blind spot problem in action.
Where else to use this
I find Model Council most useful for when the cost of bad information is high.
Derisking any big decision. Every model carries biases from its training data. One model might lean toward a certain framework, tool, or approach because of what it was trained on. Running the same question through multiple models exposes those biases so you can see the full spectrum of a topic and form your own informed take.
Market research before you launch something. One model might pull industry reports another one misses entirely.
Competitor analysis. You want to know what a competitor is actually doing, and different models pull from different sources about the same company.
Vetting any claim someone made to you. A potential partner says they did $2M last year. A supplier says their product has a certain spec. Run it through Model Council and see if the models agree.
Complex financial or legal questions where getting a detail wrong means overpaying, triggering an audit, or signing something you shouldn't.
Basically any question where you'd normally get one confident answer and act on it. 
Those are exactly the questions worth running through multiple models.
Because the thing about blind spots is you never know you have one until it costs you something.
Go try it
Think about the last important question you asked AI. The one where you got an answer, felt good about it, and made a decision.
Now go ask it again in Perplexity with Model Council turned on.
See what the other models caught.
P.S. If you want more AI workflows that help you get more customers, more attention, and more done (without working more hours)...
I send them to 35k readers every week for free.
Plus you get a free Claude Cowork masterclass when you join: aisolo.beehiiv.com/subscribe
Want to publish your own Article?
Upgrade to Premium
2:23 PM · Apr 2, 2026
·
13.6K
 Views
-------
https://github.com/harry0703/MoneyPrinterTurbo
------
https://github.com/elder-plinius/CL4R1T4S/blob/main/ANTHROPIC/CLAUDE-FABLE-5.md

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-17 - Implement OAuth 2.1 browser-flow and vision-mcp roadmap tasks]]
> * **Próxima Sessão**: [[2026-06-17 - agent-ac71eb815829bc61b]]
%% --- TIMELINE END --- %%

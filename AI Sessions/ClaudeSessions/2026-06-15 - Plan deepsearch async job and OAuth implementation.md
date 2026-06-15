# Plan deepsearch async job and OAuth implementation
**Date:** 2026-06-15 | **Session ID:** `dfc038c3-0ab3-428f-80e3-e30dca27edaa`

---

## 👤 User *(18:21:08)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(18:21:08)*

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


## 🤖 Claude *(18:21:18)*


## 🤖 Claude *(18:21:19)*

I'll execute the ShakeHands /handson pickup protocol. Starting with parallel pre-flight checks.

## 🤖 Claude *(18:21:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git fetch origin --quiet 2>&1 | tail -3; echo \"--- LOG ---\"; git log --oneline -7; echo \"--- STATUS ---\"; git status --short; echo \"--- DIFFSTAT ---\"; git diff HEAD --stat; echo \"--- vs origin/main ---\"; git rev-list --left-right --count HEAD...origin/main 2>/dev/null",
  "description": "Git fetch + log + status + diff scope + ahead/behind"
}
```

## 🤖 Claude *(18:21:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"--- TSC ---\"; npx tsc --noEmit 2>&1 | tail -20; echo \"EXIT:$?\"",
  "description": "TypeScript strict no-emit check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> --- LOG ---
> 1a110fb chore(sprint): register v6.37.0 vision-mcp Fatia 2 (4 billable tools + BYOK) + proof manifest
> 2676f91 docs(handoff): seal Vision MCP Fatia 2 — 4 billable tools + BYOK foundation + Fatia 1 handshake/interop close
> 70846b0 docs(readme): v6.37.0 — Vision MCP Fatia 2 (4 billable tools + BYOK foundation) + Fatia 1 handshake/interop close
> 88730c3 test(vision-mcp): handshake/adversarial E2E + Fatia 2 smokes (anticorpos)
> 93d2abb feat(settings): Firecrawl BYOK field + vision-mcp mcoCoin classes
> 138d935 feat(db): per-user firecrawl_api_key Vault BYOK column
> 54fd61e docs(vision-mcp): Fatia 2 billing/credential SOP + FRD protocol-version contract
> --- STATUS ---
> --- DIFFSTAT ---
> --- vs origin/main ---
> 0	0
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> --- TSC ---
> EXIT:0
> ```

## 🤖 Claude *(18:21:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"--- mcorch containers ---\"; docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\" 2>&1; echo \"--- mega-brain ---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\" 2>&1; echo \"--- vision ---\"; docker ps --filter \"name=vision\" --format \"{{.Names}}: {{.Status}}\" 2>&1; echo \"--- chroma heartbeat ---\"; curl -s -m 5 http://localhost:8001/api/v2/heartbeat 2>&1; echo \"\"; echo \"--- vision-mcp :3200 ---\"; curl -s -m 5 http://127.0.0.1:3200/health 2>&1 || echo \"(no /health)\"",
  "description": "Docker mesh + chroma + vision-mcp health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> --- mcorch containers ---
> mcorch_vision_mcp: Up 23 minutes (healthy)
> mcorch_claude_mem: Up 2 hours (healthy)
> mcorch_chroma: Up 2 hours (healthy)
> --- mega-brain ---
> mega-brain-dashboard: Up 2 hours
> mega-brain-webhook: Up 2 hours (healthy)
> mega-brain-daemon: Up 2 hours (healthy)
> --- vision ---
> mcorch_vision_mcp: Up 23 minutes (healthy)
> --- chroma heartbeat ---
> {"nanosecond heartbeat":1781547685505568379}
> --- vision-mcp :3200 ---
> {"status":"ok","protocol":"2025-11-25","tools":["mesh_search","vision_describe_image","vision_analyze_video","deepsearch_scrape","mesh_consolidate_reference"]}
> ```

## 🤖 Claude *(18:21:27)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"--- BoK suites ---\"; ls docs/bok/ 2>/dev/null; echo \"--- HANDOFF lines ---\"; wc -l HANDOFF.md; echo \"--- scratch ---\"; ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean/absent\"; echo \"--- sprint-priorities exists? ---\"; ls -la .claude/context/sprint-priorities.md 2>/dev/null || echo \"no sprint-priorities.md\"",
  "description": "BoK suites + HANDOFF line count + scratch + sprint file"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> --- BoK suites ---
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
> --- HANDOFF lines ---
> 7853 HANDOFF.md
> --- scratch ---
> scratch has files
> --- sprint-priorities exists? ---
> -rw-rw-r-- 1 ubuntu ubuntu 109678 Jun 15 15:10 .claude/context/sprint-priorities.md
> ```

## 🤖 Claude *(18:21:28)*


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
> 14	## Session Seal — Vision MCP Fatia 2: 4 Billable Tools + BYOK Foundation (+ Fatia 1 handshake/interop close) (2026-06-15)
> 15	
> 16	Continuação direta do seal anterior. A diretiva começou em "fechar a última ponta não-provada da Fatia 1 (mesh.search E2E com JWT)" e o Sovereign, vendo a janela de contexto (1M), pediu para seguir até a Fatia 2 inteira ("algo completo": describe_image + **describe_video** + deepsearch.scrape Firecrawl + mesh.consolidate, BYOK per-user, "você escolhe a ordem"). Entregue tudo, cada peça provada **contra o container/DB servido** (Lei 1).
> 17	
> 18	**O que foi entregue (em ordem de execução):**
> 19	
> 20	1. **`mesh.search` E2E fechado + 1 bug crítico de Fatia 1 corrigido:** o E2E com o cliente MCP real (SDK) expôs que o servidor reusava **um único** `StreamableHTTPServerTransport` stateless — o SDK proíbe reuso (guard `_hasHandledRequest`) → `initialize` 200 mas `notifications/initialized` **500**, logo **nenhum cliente MCP completava o handshake**. Os gates curl do deploy só testaram 401/403/400, nunca uma sessão. Corrigido para `McpServer`+transport **frescos por request**. Provado **7/7** (handshake + isolamento tenant + sentinel) + **adversarial 6/6** (forja ES256 ×3 — payload adulterado/`alg:none`/HS256 → 401; injeção PostgREST ×7 no `query` → zero leak).
> 21	
> 22	2. **Defeito de interop de protocolo (achado pelo `/security-review` independente, lente de completude):** o gate `isProtocolVersionOk` aceitava **só** `2025-11-25`, 400-ando clientes 3rd-party que negociam revs antigas suportadas (o SDK default é `2025-03-26`). Ampliado para `SUPPORTED_PROTOCOL_VERSIONS`. Provado com cliente **cru heterogêneo 8/8** (sequência completa negociando `2025-03-26`/`2025-06-18`). Endurecido o `sub` (trim). FRD FR-VM-001 alinhado.
> 23	
> 24	3. **Fatia 2 — fundação compartilhada (SOP Lei 2 + `infra/billing.ts` + `auth/credentials.ts` + `safety/duty-of-care.ts`):** resolução de credencial per-user **BYOK→plataforma→402**, **deduct-on-entry + refund-on-failure** (RPCs service-role com o `sub` verificado), sentinel, duty-of-care assistivo (red-line medicação/alérgeno/mobilidade/emergência). BYOK=grátis · Sovereign isento · plataforma cobra a classe selada (OTD-VM-004).
> 25	
> 26	4. **4 tools billable provados:**
> 27	   - **`vision.describe_image`** (FR-VM-018, 2 mco) — VLM OpenRouter. Smoke **7/7** (SSRF · sentinel · red-line · 402-antes-do-leg · leg real US$0,0004 débito 50→48 · refund-on-failure 48→48).
> 28	   - **`vision.analyze_video`** (FR-VM-024, 2 mco/min) — **Gemini video understanding** (não Higgsfield). Smoke **7/7** (leg Gemini real descreveu o vídeo · **cobrança por minuto** min=2→cost 4 · refund). SSRF por redirect corrigido (`redirect:manual` + revalidação por hop — achado do `/security-review`).
> 29	   - **`deepsearch.scrape`** (FR-VM-007, Firecrawl **BYOK-only**) — smoke **4/4** (402 `firecrawl_not_configured` · scrape BYOK real de example.com → markdown · grátis, balance 0→0).
> 30	   - **`mesh.consolidate_reference`** (FR-VM-021, 1 mco) — contraparte WRITE. Smoke **5/5** (sentinel L2 · 402 · **escrita tenant-escopada** `user_id===sub` · par read+write · isolamento tenant B).
> 31	
> 32	5. **Migration `firecrawl_api_key` Vault BYOK** (replicação verbatim do padrão vivo `20260603240000` + coluna nova) — `/security-review` independente **limpo** (pegou só o SSRF do analyze_video, corrigido) · aplicada via Management API + registrada no migration history · coluna presente em base+masked+decrypted. **UI Settings** (campo Firecrawl) — frontend **rebuildado + deployado** (chunk novo `Cwl4HRcg` · campo + env baked).
> 33	
> 34	**ORO:** Operator=MCORCH Agent · Reviewer=Sovereign + `/security-review` independente · Owner=Sovereign (1º serviço tenant-facing que debita mcoCoins + chama provider pago).
> 35	
> 36	| Verificação | Resultado |
> 37	|---|---|
> 38	| Commits | `9247452` (tools+foundation+fixes) · `54fd61e` (SOP+FRD) · `138d935` (migration+types) · `93d2abb` (settings+billing) · `88730c3` (QA harness) · `70846b0` (readme) (+ handoff) |
> 39	| Container `mcorch_vision_mcp` | ✅ healthy · 5 tools no `/health` · artefato servido verificado a cada deploy |
> 40	| E2E / adversarial / interop | ✅ mesh.search 7/7 · heterogêneo 8/8 · adversarial 6/6 · protocolo before/after |
> 41	| Smokes Fatia 2 | ✅ describe 7/7 · analyze 7/7 · consolidate 5/5 · deepsearch 4/4 (zero resíduo) |
> 42	| Migration | ✅ `/security-review` limpo · aplicada+registrada · coluna em 3 relações |
> 43	| Testes / tsc | ✅ pkg 34/34 · frontend billing 22/22 · tsc 0 (root+pkg) |
> 44	
> 45	### Arquitetura Fatia 2 (tool billable — pipeline por request)
> 46	```
> 47	[HTTP gate: Origin 403 → MCP-Protocol-Version 400 → ES256 JWKS 401 fail-closed → ALS(sub)]
> 48	  → MCP tool → sentinel.inspectPrompt(args) (FR-VM-005)
> 49	            → resolveProviderKey(sub, provider): decrypted_user_api_keys[col] (BYOK, free)
> 50	                                                 senão env plataforma (charged) senão 402 <provider>_not_configured
> 51	            → costFor(tool, sub, isUserCustomKey, units): Sovereign→0 · BYOK→0 · senão classe×units
> 52	            → deductOnEntry (402 insufficient ANTES do leg)  ──┐
> 53	            → provider leg (OpenRouter VLM / Gemini video / Firecrawl)  │ refund-on-failure
> 54	            → [consolidate: INSERT mcorch_nodes user_id=sub]  ──────────┘
> 55	```
> 56	
> 57	**Pendências/Próximos (vision-mcp):**
> 58	- **`deepsearch.run`** (a metade "google/gemini" do deepsearch que o Sovereign citou) — fiel à FR-VM-007 é **assíncrono** (job_id→poll + partial-delivery refund §4.5); feature distinta e mais pesada, teed-up para sessão própria.
> 59	- **Fatia 3** (PAT/OAuth 2.1/RFC 9728 AS · Plugin Zip · jobs assíncronos · erase LGPD `erase_vision_artifacts`).
> 60	- **vhost nginx `mcp.mcorch.com`** (OTD-VM-013, root/DNS Cloudflare — ação Sovereign): hoje só loopback `127.0.0.1:3200`.
> 61	- **Risco residual orphan-sub** (LOW, documentado no código): registrar como OTD na emenda BoK da Fatia 2.
> 62	- Follow-up: migration `infra_health_logs ADD metadata jsonb` (telemetria rica) · platform `FIRECRAWL_API_KEY` se o Sovereign quiser default cobrado p/ scrape.
> 63	
> 64	### Survival Laws Self-audit
> 65	```
> 66	Law 1 (Materiality): ✅ Cada claim ancorada em smoke/probe/E2E contra o container/DB servido (não o node local) — e isso pegou o bug de handshake + o SSRF. Bugs achados pelo /security-review independente corrigidos antes do seal. Leftover de QA (user deepsearch) limpo → zero resíduo verificado. tsc 0. Phase 5c a seguir.
> 67	Law 2 (Process): ✅ SOP de billing/credencial ANTES do código (Lei 2); migration `/security-review` ANTES de aplicar (FMEA-011); FRD alinhado ao contrato real.
> 68	Law 3 (Pruning): ✅ Janela usada densamente até o GO de selar do Sovereign (Fatia 1 + Fatia 2 inteira numa sessão); workflow adversarial retornou síntese, não dumps.
> 69	Law 4 (ORO): ✅ Triplet declarado por sub-task; Owner=Sovereign; GO explícito do Sovereign p/ cada expansão de escopo + a escolha de selar.
> 70	```
> 71	
> ```

## 🤖 Claude *(18:21:35)*


## 🤖 Claude *(18:21:35)*

Now the tail of HANDOFF, sprint priorities head, scratch contents, and BoK gate check.

## 🤖 Claude *(18:21:36)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 7453,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 7453	       campaign_id · content_id · metadata{affiliate_id, resolved_url, self_healed_from}
> 7454	
> 7455	  6. Return: {success, original_url, resolved_url, affiliate_url, self_healed, link_id}
> 7456	
> 7457	ContentLibraryPage monetization flow:
> 7458	  Card (text, body contains mercadolivre.com.br)
> 7459	    └── DropdownMenu → "Monetizar Links ML"
> 7460	          → handleMonetizeLinks(item):
> 7461	               match(ML_URL_RE) → unique URLs
> 7462	               for url of unique:
> 7463	                 POST process-affiliate-link → affiliate_url
> 7464	                 body.split(url).join(affiliate_url)
> 7465	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 7466	          → Badge 💰 ML (emerald) exibido após monetização
> 7467	```
> 7468	
> 7469	---
> 7470	
> 7471	## Pending Actions (Commercial Launch)
> 7472	
> 7473	### CRITICAL — Must complete before first client
> 7474	
> 7475	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 7476	
> 7477	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 7478	
> 7479	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 7480	
> 7481	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 7482	
> 7483	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 7484	
> 7485	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 7486	
> 7487	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 7488	
> 7489	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 7490	
> 7491	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 7492	
> 7493	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 7494	   ```bash
> 7495	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 7496	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 7497	   ```
> 7498	
> 7499	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 7500	
> 7501	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 7502	
> 7503	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 7504	
> 7505	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 7506	
> 7507	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 7508	
> 7509	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 7510	
> 7511	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 7512	
> 7513	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 7514	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 7515	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 7516	
> 7517	### SOCIAL — Next steps
> 7518	
> 7519	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 7520	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 7521	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 7522	
> 7523	### NON-CRITICAL
> 7524	
> 7525	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 7526	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 7527	- `browserslist` — ✅ updated (2026-04-26)
> 7528	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 7529	
> 7530	### GITNEXUS MCP — Next steps
> 7531	
> 7532	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 7533	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 7534	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 7535	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 7536	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 7537	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 7538	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 7539	
> 7540	### PHASE EPSILON — Next iterations
> 7541	
> 7542	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 7543	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 7544	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 7545	
> 7546	### CORE — Next iterations
> 7547	
> 7548	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 7549	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 7550	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 7551	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 7552	
> 7553	### PHASE DELTA — Next iterations
> 7554	
> 7555	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 7556	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 7557	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 7558	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 7559	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 7560	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 7561	
> 7562	### USUÁRIO ZERO — Checklist de validação
> 7563	
> 7564	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 7565	- ✅ Stripe sandbox secrets no vault
> 7566	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 7567	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 7568	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 7569	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 7570	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 7571	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 7572	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 7573	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 7574	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 7575	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 7576	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 7577	
> 7578	---
> 7579	
> 7580	## Infrastructure
> 7581	
> 7582	| Service | Container | Port | Status |
> 7583	|---------|-----------|------|--------|
> 7584	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 7585	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 7586	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 7587	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 7588	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 7589	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 7590	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 7591	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 7592	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 7593	
> 7594	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 7595	
> 7596	```bash
> 7597	docker compose up -d
> 7598	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 7599	```
> 7600	
> 7601	---
> 7602	
> 7603	## Security Model (Post-Go-Live)
> 7604	
> 7605	| Table | Isolation |
> 7606	|-------|-----------|
> 7607	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 7608	| `mcorch_edges` | Same pattern |
> 7609	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 7610	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 7611	
> 7612	---
> 7613	
> 7614	## Billing Architecture
> 7615	
> 7616	| Decision | Value |
> 7617	|----------|-------|
> 7618	| Canonical billing ledger | `profiles.mco_balance` |
> 7619	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 7620	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 7621	| Orchestration cost | 10 mcoCoins/run |
> 7622	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 7623	| Stripe | Sandbox keys active — swap to live before first client |
> 7624	
> 7625	---
> 7626	
> 7627	## GraphRAG State
> 7628	
> 7629	- **8917 total nodes** (verificado live 2026-06-15 via REST count=exact, vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 7630	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 7631	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 7632	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 7633	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 7634	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 7635	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 7636	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 7637	- HNSW cosine index operational
> 7638	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 7639	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 7640	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 7641	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 7642	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 7643	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 7644	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 7645	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 7646	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 7647	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 7648	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 7649	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 7650	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 7651	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 7652	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 7653	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 7654	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 7655	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 7656	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 7657	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 7658	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 7659	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 7660	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 7661	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 7662	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 7663	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 7664	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 7665	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 7666	
> 7667	### Embedding Model
> 7668	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 7669	Schema: `vector(768)` — HNSW cosine index.
> 7670	
> 7671	### Embedding Pipeline (Autônomo — 2026-05-03)
> 7672	Três camadas eliminam intervenção manual:
> 7673	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 7674	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 7675	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 7676	
> 7677	### Comandos de manutenção da Mesh
> 7678	```bash
> 7679	# Verificar nós sem embedding (deveria retornar array vazio):
> 7680	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 7681	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 7682	
> 7683	# Backfill manual (Bun-native — requer .env):
> 7684	bun run scripts/backfill-embeddings.ts
> 7685	
> 7686	# Backfill de código-fonte nos nós AST:
> 7687	bun run scripts/backfill-node-content.ts
> 7688	
> 7689	# Re-sync AST completo:
> 7690	cd packages/gitnexus-core && npm run sync-mesh
> 7691	
> 7692	# Acompanhar re-ingesta pós-commit:
> 7693	tail -f /tmp/mcorch-ingest.log
> 7694	```
> 7695	
> 7696	---
> 7697	
> 7698	## Video Rescue Protocol
> 7699	
> 7700	When a video generation operation (Google Veo) times out or client disconnects:
> 7701	```bash
> 7702	# Via edge function (production):
> 7703	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 7704	  -H "Authorization: Bearer <user_jwt>" \
> 7705	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 7706	
> 7707	# Via local script (admin/debug):
> 7708	source .env && bun run rescue.ts <operation_id> <content_id>
> 7709	```
> 7710	
> 7711	---
> 7712	
> 7713	## Architecture Pillars
> 7714	
> 7715	| Layer | Implementation |
> 7716	|-------|---------------|
> 7717	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 7718	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 7719	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 7720	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 7721	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 7722	
> 7723	---
> 7724	
> 7725	## Phase Delta — Architecture
> 7726	
> 7727	```
> 7728	OrchestrationPage (full-canvas, p-0)
> 7729	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 7730	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 7731	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 7732	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 7733	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 7734	        ├── nodes/PublishNode.tsx    ← final distribution output
> 7735	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 7736	        └── NodePalette.tsx          ← top toolbar to add nodes
> 7737	
> 7738	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 7739	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 7740	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 7741	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 7742	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 7743	```
> 7744	
> 7745	### Canvas State Architecture (Hybrid)
> 7746	
> 7747	```
> 7748	User interaction → ReactFlow internal state (positions, drag)
> 7749	                         ↓ (debounced 600ms)
> 7750	                   localStorage (positions persist across refresh)
> 7751	                         ↑
> 7752	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 7753	     ↓ (status changes sync to ReactFlow via useEffect)
> 7754	ReactFlow renders visual status (idle/running/done/error/blocked)
> 7755	```
> 7756	
> 7757	## Key Files
> 7758	
> 7759	| Purpose | Path |
> 7760	|---------|------|
> 7761	| Architecture rules | `CLAUDE.md` |
> 7762	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 7763	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 7764	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 7765	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 7766	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 7767	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 7768	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 7769	| **Node types** | `src/components/orchestrator/nodes/` |
> 7770	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 7771	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 7772	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 7773	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 7774	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 7775	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 7776	| Billing utilities | `src/lib/billing.ts` |
> 7777	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 7778	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 7779	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 7780	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 7781	| Video rescue (local) | `rescue.ts` |
> 7782	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 7783	| Backfill script | `scripts/backfill-embeddings.ts` |
> 7784	| Deploy harness | `scripts/harness-deploy.sh` |
> 7785	
> 7786	---
> 7787	
> 7788	## First Client Onboarding Checklist
> 7789	
> 7790	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 7791	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 7792	3. ~~Activate watchdog cron~~ ✅ Done
> 7793	4. ~~Deploy rescue-video function~~ ✅ Done
> 7794	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 7795	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 7796	7. Monitor `infra_health_logs` for first 24h.
> 7797	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 7798	
> 7799	---
> 7800	
> 7801	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 7802	
> 7803	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 7804	
> 7805	| Action | Result |
> 7806	|--------|--------|
> 7807	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 7808	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 7809	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 7810	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 7811	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 7812	
> 7813	| Commit | Conteúdo |
> 7814	|--------|----------|
> 7815	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 7816	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 7817	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 7818	
> 7819	### Arquitetura Matrix Intelligence
> 7820	
> 7821	```
> 7822	ConstellationMatrix (Stabilized Engine)
> 7823	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 7824	  └── NodeDetailsPanel (Tabbed Navigation)
> 7825	        ├── Tab Meta: Neighbor exploration + Net Context
> 7826	        ├── Tab Code: Source code preview (Supabase sync)
> 7827	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 7828	
> 7829	useNodeIntelligence Hook:
> 7830	  - contentQuery: fetch nodes.content column
> 7831	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 7832	  - state: isAnalyzing, analysisResult, progress
> 7833	```
> 7834	
> 7835	---
> 7836	
> 7837	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 7838	
> 7839	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 7840	
> 7841	| Action | Result |
> 7842	|--------|--------|
> 7843	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 7844	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 7845	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 7846	
> 7847	**Output da análise (estruturado em pt-BR):**
> 7848	- Visão Geral — papel do módulo no sistema
> 7849	- Padrões Detectados — design patterns, antipatterns
> 7850	- Acoplamento & Dependências — análise In/Out-Degree
> 7851	- Recomendações — 1-3 ações priorizadas
> 7852	
> ```

## 🤖 Claude *(18:21:37)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md",
  "limit": 90
}
```

> **Tool Result (Read)** - ❌ Error
>
> ```
> File content (30700 tokens) exceeds maximum allowed tokens (25000). Use offset and limit parameters to read specific portions of the file, or search for specific content instead of reading the whole file.
> ```

> **Tool Result (Unknown Tool)** - ✅ Success
>
> ```
> --- scratch contents ---
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun  7 14:41 .
> drwx------ 30 ubuntu ubuntu 4096 Jun 15 15:09 ..
> --- vision-mcp BoK gate ---
> ✅ vision-mcp — BoK complete (9/9)
> --- vision-mcp bok files ---
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
> 09-agent-system.md
> ```

## 🤖 Claude *(18:21:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"--- scratch contents ---\"; ls -la scratch/ 2>/dev/null; echo \"--- vision-mcp BoK gate ---\"; slug=vision-mcp; required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics); missing=(); for doc in \"${required[@]}\"; do [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\"); done; [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug \u2014 BoK complete (9/9)\" || echo \"\u26a0\ufe0f $slug \u2014 missing: ${missing[*]}\"; echo \"--- vision-mcp bok files ---\"; ls docs/bok/vision-mcp/ 2>/dev/null",
  "description": "Scratch contents + vision-mcp BoK gate"
}
```

## 🤖 Claude *(18:21:48)*


## 🤖 Claude *(18:21:49)*

Let me grab the sprint goal head precisely.

## 🤖 Claude *(18:21:50)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md",
  "offset": 0,
  "limit": 55
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 0	# 🧠 Sprint Priorities — Constellation Orchestra
> 1	
> 2	**Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 3	
> 4	**90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 5	
> 6	**Sprint v6.37.0 — Vision MCP Fatia 2: 4 Billable Tools + BYOK Foundation (+ Fatia 1 handshake/interop close) (2026-06-15)** — diretiva começou em "fechar a última ponta não-provada da Fatia 1 (mesh.search E2E com JWT)" e o Sovereign mandou seguir até a Fatia 2 inteira ("algo completo", "você escolhe a ordem"). **(1) mesh.search E2E fechado + bug crítico de Fatia 1:** o E2E com cliente MCP real pegou que o servidor reusava **um** `StreamableHTTPServerTransport` stateless (SDK proíbe reuso → `notifications/initialized` **500**, nenhum cliente completava handshake) → fix fresh-per-request; provado **7/7** + adversarial **6/6** (forja ES256 ×3 + injeção PostgREST ×7). **(2) Interop de protocolo** (achado pelo `/security-review` independente): gate aceitava só `2025-11-25`, 400-ando clientes 3rd-party → ampliado p/ `SUPPORTED_PROTOCOL_VERSIONS`; cliente cru heterogêneo **8/8** (`2025-03-26`/`2025-06-18`). **(3) Fatia 2 — fundação** (SOP Lei 2 + `infra/billing.ts` + `auth/credentials.ts` + `safety/duty-of-care.ts`: BYOK→plataforma→402 · deduct-on-entry+refund-on-failure · sentinel · duty-of-care) + **4 tools billable provados:** `vision.describe_image` (FR-VM-018, 7/7), `vision.analyze_video` (FR-VM-024 Gemini — **não Higgsfield** — cobrança/min, 7/7), `deepsearch.scrape` (FR-VM-007 Firecrawl BYOK-only, 4/4), `mesh.consolidate_reference` (FR-VM-021 escrita tenant-escopada, 5/5). **(4)** migration `firecrawl_api_key` Vault (`/security-review` limpo · aplicada+registrada) + UI Settings **deployada** + SSRF redirect-fix (achado do review). pkg **34/34** · tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8917** · handoff `7a45d8ef` · 7 commits. **Top Gap novo:** `deepsearch.run` async (a metade "google/gemini" — FR-VM-007 job/poll) · Fatia 3 (PAT/OAuth/Plugin/jobs/erase LGPD) · vhost nginx OTD-VM-013 · OTD orphan-sub. **Lição:** o `/security-review` independente pagou de novo (achou o SSRF por redirect + o defeito de interop de protocolo que o cliente do mesmo-SDK mascarava); testar contra o ARTEFATO SERVIDO pegou o bug de handshake.
> 7	
> 8	**Sprint v6.36.2 — Vision MCP: OTD Gates Closed + Fatia 1 Built & Deployed ON (2026-06-15)** — diretiva Sovereign "ambos em sequência" (gates por pesquisa → código). **(1) Gates OTD pré-GA** (workflow `wf_0040a939-232`, 3 lentes verify adversarial): **OTD-VM-004 CLOSEABLE** (grade mcoCoins 4×-floor sobrevive — custo fonteado por provider, nenhuma sub-margem; `segment` cost-aware obrigatório; SOP `vision-mcp-cost-calibration.md`); **OTD-VM-001 CLOSEABLE** (corrigiu 2 erros factuais do blueprint — UEyes/Imp1k EXISTEM, SOTA=**SUM**/MIT self-hostável não DeepGaze; recall≥0.95 fundamentado); **OTD-VM-006 CLOSEABLE** (14 licenças verdes LICENSE-fetched + 3 minas banidas; SpikingJelly não-MIT); **OTD-VM-005 PARTIAL** (SCCs-ANPD inviável; Res. 32/2026 UE adequada; Mistral=default candidato). **(2) Fatia 1 construída + DEPLOYADA ON** (`packages/vision-mcp-core/` → container `mcorch_vision_mcp` Sovereign Mesh, restart=unless-stopped, UID1001, read-only, `127.0.0.1:3200`): Streamable HTTP + ES256 JWKS fail-closed + Origin/protocol gates + sentinel + `mesh.search` tenant-safe. Provado material **contra o container**: health 200/401+WWW-Authenticate RFC9728/403/400 + row infra_health_logs + 14/14 testes. **2 bugs que só o deploy pegou:** bind `0.0.0.0` (port-map do bridge) + schema real de `infra_health_logs` (sem `metadata` — o padrão do sentinel edge falha silencioso). tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8916** · handoff `98fa83d7` · 4 commits. **Top Gap novo:** mesh.search E2E com JWT (handshake MCP) · vhost nginx `mcp.mcorch.com` (OTD-VM-013, root Sovereign) · Fatia 2 (foveal billable + per-user creds) · migration `infra_health_logs ADD metadata jsonb` (telemetria rica). **Lição:** testar o ARTEFATO SERVIDO (container), não o node local — Lei 1 pegou 2 bugs + 1 schema drift que unit/local não veriam.
> 9	
> 10	**Sprint v6.36.1 — Vision MCP: BoK 9/9 + 8-Agent System + Adversarial Validation (2026-06-15)** — diretiva Sovereign (ref. sandcastles.ai): MCP Interno nativo de **percepção visual + deepsearch fundamentado** ("Essência Humana"), interno + ecossistemas externos. Closed-Loop BoK-first em 3 atos: **(1) Blueprint-semente v0.2.0** (workflow ultracode 19 agentes · 140 refs · verify adversarial — 5 pilares CV/Motion/Neuromorphic/Peripheral/**Cognitive** + vertical **Tecnologia Assistiva** beachhead demand-provado); **(2) Suíte BoK 9/9** (`/bok-scribe`) selada na malha (node `318862b7`, DERIVES_FROM mcorch-constellation, embedding 768d) — runtime container `mcorch_vision_mcp` Sovereign Mesh, **0 edge fns**; **(3) Sistema de 8 agentes BoK** (`/bok-agents-generator`) com Pantheon Reconciliation (eleva, não recria). **Validação adversarial independente (3 lentes) = SUITE VALIDATED** após pegar+corrigir **1 blocker cross-tenant real** (`erase_vision_artifacts` cascade DELETE sem re-escopar `user_id`) + hardening (scopes allowlist física, expiry CHECK, Storage policy DDL, colisão OTD-VM-020→021, FMEA-VM-004 RPN175→OTD-VM-022). Anticorpo **`deepsearch-blueprint`** (skill+agent+SOP) — padrão rodou 2× (Cyber-Sentinel+Vision MCP). tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8915** · handoff `b73d141d` · README badge `6.36.0-vision-mcp`. 4 workflows mortos por cota recuperados (resumeFromRunId/main loop) — zero perda. **Top Gap novo:** Fatias MVP do vision-mcp (BoK gate ABERTO) — Fatia 1 esqueleto MCP autenticado internal · gates OTD-VM-001 (recall Tier1) / -004 (unit economics) / -005 (DPA) / -013 (nginx vhost) / -020 (OAuth AS). **Lição:** validação adversarial por agente que NÃO escreveu a suíte pega o que self-review não pega (vetor cross-tenant que minha mão + 1ª lente deixaram passar).
> 11	
> 12	**Sprint v6.36.0 — Native OpenDesign Integration + MIV Redesign Backlog (2026-06-14)** — Configuração do OpenDesign de forma nativa e inclusão da meta de redesign completo baseada no MIV (Manual de Identidade Visual) no roadmap. **(1) Nativização do OpenDesign** (`CanvasDesignPage.tsx`): o editor foi simplificado para renderizar o iframe do OpenDesign em tela cheia na rota `/dashboard/canvas/design`, removendo o controle local antigo e as abas redundantes, criando uma experiência 100% nativa. **(2) Backlog de Redesign MIV**: adicionado o OTD-MIV-REDESIGN na lista de Top Gaps e no roadmap do Canvas Studio.
> 13	
> 14	**Sprint v6.35.0 — Core-Fable: Fable 5 Flagship + Metering + Mega Brain Interstellar (2026-06-10)** — Diretiva Sovereign "Refatore todo o nosso Core-v2 para Core-Fable" em 3 arcos: **(1) Rebrand** (`914f8dd`): rota `/dashboard/core-fable` (+redirects compat), `CoreFablePage`/`components/core-fable/`, Claude Fable 5 (`anthropic/claude-fable-5` via OpenRouter, verificado live no catálogo) como default do Core; seletor de chat **desacoplado** do `pref_ai_model` (localStorage) — 1 clique não re-modela o flywheel pago. **(2) Review adversarial pré-deploy confirmou 4 P1 econômicos** (`997b307`): aios-chat OpenRouter nascia SEM metering (billing bypass na chave-plataforma) → `_shared/agent-metering.ts` compartilhado fiado nos 2 paths; `agent_pricing` sem rows novas → under-billing 133-167× via fallback flash → migration `20260610010000` seeda fable-5 1000/5000 + sonnet-4.6 300/1500 + dropa id morto; `/security-review` SAFE. Provado live: probe `{"output":"Claude"}` + ledger correto + `calc_agent_cost_mcoin`=120. **(3) Mega Brain Interstellar** (`3b15e41`→`47f9316`): loop iterativo de 8 screenshots dirigido por referência visual do Sovereign — câmera quase equatorial + 210 steps adaptativos = arco lensado contínuo sobre a sombra; **raios capturados = preto** (matou anel de névoa + bola branca do glow artificial — críticos precisam ~310 steps/órbita); disco blackbody edge-on, reação por energia (surge/spin/shimmer). tsc 0 · suíte **295** · Phase 5c **SEAL ALLOWED** (10) · mesh **8865** · handoff `4728b8aa`. **Top Gap novo:** OTD-FABLE-MARGIN (margem 2.0 do calc < 4×-floor p/ chat premium) · fallback `pricing_not_found` silencioso (fail-caro + telemetria). **Lição:** o screenshot-loop com sessão real no preview local (sem tocar o dist servido) pegou 2 bugs visuais que tsc/testes jamais veriam (GLSL só falha em runtime); e o review adversarial pagou de novo — 4 P1 econômicos numa feature "só de rename".
> 15	
> 16	**Sprint v6.34.0 — Cyber-Sentinel: Security BoK 4/4 + Prompt Gate Live + Infra Hardening (2026-06-10)** — diretiva CISO executada em 2 fases na mesma sessão. **(1) BoK de segurança 4/4** (`docs/bok/security/`, schema CISO 01-brd/02-srs/03-sdd/04-fmea — 12 BR-SEC + Risk Ledger · 15 FR-SEC + matriz RLS canônica + `SET LOCAL` · SDD lefthook/Arcjet/sentinel/Dockerfile UID1001/compose cap_drop integrais · FMEA 12 modos RPN AIOS). **(2) Aplicação no ecossistema vivo** (`6f2f75a`): **Sentinel LIVE** em `orchestrate-content` (prod **v52**) — `_shared/sentinel.ts` barra injeção/bypass/ANSI **depois da identidade, antes do `deduct_mco_coins`**; provado em prod com JWT real (`HTTP 403 layer=sentinel` score=3, **zero mcoCoins**). Infra recriada e endurecida: `claude_mem` uid1001+read_only+8caps (healthy), `chroma` caps conservadoras+no-new-privileges (heartbeat vivo), `gitnexus` imagem não-root buildada; env `SUPABASE_SERVICE_ROLE_KEY` revogada removida do compose (FM-04). Gate git **dual-engine** lefthook+gitleaks (pre-commit/pre-push, degrada sem gitleaks — OTD-SEC-003). **Review adversarial pegou 4 bugs reais ANTES de qualquer deploy quente**: rate-limiter falsava o fan-out paralelo de `campaign-run`; `cap_drop SETUID/SETGID` quebraria o `chroma` de terceiros; regex de 1 qualificador; guard `&&||` do gitleaks engolia a detecção. tsc 0 · suíte **295** · Phase 5c **SEAL ALLOWED** (10) · mesh **8862** · handoff `0a9865a9` + BoK seal `424f0fe4`. **Próximos:** FM-10 gitnexus (imagem pronta, roda stdio) · OTD-SEC-006/007 (fiar sentinel + migration `security_events`/quarentena <50ms nas demais fns pagas) · Arcjet aguarda superfície Next/BFF. **Lição:** verificar **materialmente** (dry-run dos containers, exploit real em prod) antes de declarar — pegou o `name:` que orfanaria os containers e os 4 bugs do review.
> 17	
> 18	**Sprint v6.33.1 — Hotfix Kanban ScrollArea + E2E à Prova de Cloudflare (2026-06-09)** — bug report do Sovereign no `/dashboard/kanban`: `ReferenceError: ScrollArea is not defined` ao criar coluna. **Causa:** `KanbanPage.tsx` usava `<ScrollArea>` (área scrollável de tarefas) sem importar — só quebrava *depois* da 1ª coluna (empty-state não exercita o componente). **Fix de 1 linha** (`e55ce70`): import `@/components/ui/scroll-area`; deploy material (chunk novo `KanbanPage-CW7WBYjZ.js` ≠ o do stack trace, import scroll-area + env baked); **confirmado em prod pelo print do Sovereign**. **E2E completo** via preview local do `dist` + sessão injetada (CF Turnstile barra agent-browser do datacenter até no `login.mcorch.com`): CRUD + drag-drop bidirecional **provado pelo DB** (3× PATCH 200 + SELECT, não pelo DOM). Helper `gen-user-session.ts` (`761ea6f`) p/ E2E logado à prova de CF. **Incidente de concorrência** (Sovereign mexendo em prod junto) resolvido sem perda de dado — board/coluna intactos, a "divergência" da 1ª rodada era o Sovereign movendo o mesmo card. tsc 0 · suíte **284** · Phase 5c **SEAL ALLOWED** (10) · mesh **8860** · handoff `fd20b125`. **Lição:** E2E mutável vai em board descartável, nunca no dado real do Sovereign; DB-prod é compartilhado. **Diretiva CISO de hardening DEFERIDA** (blueprint `6b1571a` commitado; 4 artefatos BoK de segurança p/ sessão dedicada).
> 19	
> 20	**Sprint v6.33.0 — ML Attribution Fix + Browser Operator BoK (2026-06-08)** — o teste **real** do Sovereign no branded link expôs o flywheel emitindo link **MORTO**. **(1) Fix do auto-monetize** (`34d7ef0`): `_shared/affiliate.ts` `buildMlProductUrl` montava o formato BARE `mercadolivre.com.br/MLB-<id>` (404) com 2/3 ids stale → agora resolve `vm_affiliate_products.product_url` real (fonte única Apify), fail-open `/p/`; **reconcilia "ML não conta clique"** (era 404, não falha do matt_word — o painel ML já contara matt_word em produto VÁLIDO em 2026-06-04); provado E2E `7993c6a4` 302 → `/p/MLB27834876`; deploy `orchestrate-step` 122.8kB. **(2) BoK 9/9 do Operador de Browser Autenticado** (`/bok-scribe`, `24ba435`): suíte 756 LOC MR→SDD+STRIDE+FMEA; **gate pagou** — o link oficial é per-user → nova `user_affiliate_links` (não a `vm_affiliate_products.affiliate_template_url` COMPARTILHADA, que vazaria entre tenants — OTD-ABO-003); runtime residencial cravado (datacenter **403** reprovado em produto real `/p/`, bare e `/afiliados/hub`); mesh seal `31323fe3` + DERIVES_FROM edge `9ea18d26` → mercado-livre-api. tsc 0 · suíte **284** · Phase 5c **SEAL ALLOWED** (10) · mesh **8852** · handoff `630509e2`. **Top Gap:** **BUILD do Operador** (gate ABERTO; runtime residencial = Sovereign roda `agent-browser` logado no ML) · domínio Resend · conversão ML real. **Lição:** o teste por **mão do Sovereign** (clicks 0→4) achou o link morto que meu curl-403 do datacenter mascarava; o BoK-first pegou o vazamento cross-tenant **antes** do código.
> 21	
> 22	**Sprint — Stored-XSS Hardening + Antibody (2026-06-08)** — `/security-review` (v6.28.0) havia flagado stored-XSS em `DashboardHome` (`content_library.body` cru via `dangerouslySetInnerHTML`); fechado **ponta-a-ponta** nesta sessão. Sanitização `DOMPurify.sanitize` (já shipada via Antigravity em `da9da4c`/`e5a661a`) + guarda de regressão **6 testes** (`dashboard-html-sanitize.test.ts`: preserva `<a href>` de afiliado + tags de artigo, remove `<script>`/`onerror`/`javascript:`) + **antibody ESLint `no-restricted-syntax`** (`2522e71`, sem dep nova — `eslint-plugin-react` ausente) que faz todo `dangerouslySetInnerHTML` futuro acusar no lint até ser sanitizado+justificado (sink cru plantado → **pego** material; 2 sinks legítimos justificados: DashboardHome DOMPurify · chart.tsx CSS shadcn) + limpeza dos **7 `no-explicit-any`** do data-layer de DashboardHome (`3129369`). Handoff node `e12ed58e` + obs antibody `505fb670` (embedded 768d). tsc 0 · suíte verde · mesh **8849**. **Anticorpo Permanente cumprido** — reincidência do sink barrada no lint. **Top gaps restantes (herdados de v6.28.0, gated no Sovereign):** domínio `RESEND_FROM` (entrega Resend real) · branded redirect `login.mcorch.com/go` · 2 rascunhos WP de teste · atribuição de compra ML.
> 23	
> 24	**Sprint v6.32.x — arco Core-v2 Black Hole (2026-06-07, via Antigravity)** — sessões conduzidas no Antigravity, seladas e versionadas no git, registradas aqui retroativamente a partir dos records do HANDOFF.md (não reauditadas em detalhe — Lei 1): **v6.32.6** Unified Relativistic Black Hole & Cymatics (fusão dos visualizadores num único shader WebGL Schwarzschild — raymarching + disco de acreção + Doppler beaming + ondas de cymatics; layout 30/70; `CymaticsLayer` removido; 284 testes; handoff `ec6204a4`; mesh 8847); **v6.32.5** Model Selector Fix & Reacting Black Hole (fix case-collision dos hooks `useAiosTerminalChat`/`useAiosWorkspaceChat`; persistência do modelo selecionado em `user_api_keys`; redesign MegaBrainVisualizer + CymaticsLayer; 260 testes; handoff `8627661a`; mesh 8839); **v6.32.2** Gemini 3.1 Live Mode (Live API → Gemini 3.1 Flash Live audio-only + Gemini Docs MCP + API Skills; handoff `5acba7aa`; mesh 8818). Os seals intermediários (v6.29–v6.32.4) existem em HANDOFF.md/README mas não foram back-filled aqui.
> 25	
> 26	**Sprint v6.28.0 selado em 2026-06-04** — **Quatro next-steps fechados numa sessão (probe-first)**. Diretiva Sovereign "ataque os 4 pontos numa sessão só, não pare até terminar; o ponto 4 do link não funcionou a contabilidade de clicks" (+ screenshot ML com 1 clique). Cada gap verificado **no código** antes de tocar. **(1) OTD-INTENT-DISPATCH-REFUND FECHADA:** `orchestrate-content` estorna os 10 em falha pós-débito (`!runId` ou erro do kick `async_orchestrate_step`) + marca run `error` — estende o contrato refund da v6.27.2 ao núcleo do flywheel. **(2) nurture-dispatch entrega Resend real (FR-MH-008):** resolve `resend_api_key` per-user (BYOK) + `leads.contact` → POST Resend quando email+chave+endereço; senão `gated`; send `failed` estorna. Live a inbox real ainda gated em `RESEND_FROM` (domínio Sovereign). **(3) Click ledger in-system (OTD-ML-CLICKS):** links publicados passam pelo redirect `process-affiliate-link` GET, que registra o clique atômico (RPC `record_affiliate_click` service-role-only, atribuído ao dono) + 302 pro ML; `link-forge` emite o redirect; **ROIWidget já soma `affiliate_links.clicks`** → "Cliques Totais" reflete cliques reais antes de compra; migration 120000 + fix 130000 (`content_id` UUID). **(4) 1º dispatch pago E2E agentic:** intent→policy→execute→orchestrate-content WP **draft**, run `43048d8e` **done**, **delta 10 exato** (valida ponto 1 em prod), HITL gate provado, blast-radius wordpress-only. **Prova:** `/security-review` independente **SAFE** · drift audit **exit 0** · smoke-affiliate-click **10/10** + smoke-nurture **10/10** · suíte **269** · tsc 0 · deploys 107.9/83.72/87.96kB · Phase 5c **SEAL ALLOWED** (7 verified) · Mesh **8783**. 6 commits. **Novo Top Gap:** entrega Resend a inbox real (domínio `RESEND_FROM` — Sovereign) · branded redirect domain (`login.mcorch.com/go` proxy nginx — link limpo+rastreado) · 2 rascunhos WP de teste a limpar · atribuição de compra ML (aguardando conversão). **Lição:** probe-first economizou retrabalho (ROIWidget já somava clicks → zero UI nova; `resend_api_key` já existia → só o canal) e pegou o bug 22P02 do RPC (content_id UUID) no smoke antes de declarar — corrigi via migration na mesma sessão (regra hotfix→migration). **Follow-up (mesma sessão, "continue com os próximos"):** click ledger estendido ao caminho **interativo** de monetização — POST `process-affiliate-link` retorna redirect rastreável `?link_id` (migration `20260604140000` + RPC `record_affiliate_click_by_link`). O smoke estendido (G8) expôs um insert de `affiliate_links` quebrado há tempo (`campaign_id` UUID vs slug `"ai_orchestration"` → 22P02 silencioso, nenhuma linha de afiliado nunca persistida) + o `/security-review` independente pegou um **open-redirect** no branch novo (302 pro `short_url` tenant-writável) — ambos corrigidos (gate de domínio ML + UUID-só); smoke **9/9** (G9 prova o open-redirect bloqueado), commit `b2c39f6`. **Follow-up 2 ("faça todos os 3"):** (A) **auto-monetização** no `orchestrate-step` — o artigo gerado embute o redirect rastreável `?link_id` per-owner (`_shared/affiliate.ts`), o flywheel monetiza+rastreia automático; provado E2E pago run `cee55b11` (Roborock → link rastreável no `content_mesh_asset`). (B) **matt_tool** per-user (coluna `affiliate_config` + threading GET/POST/orchestrate + UI `AffiliatesPage`; caveat honesto: efeito na atribuição ML não-verificável, mas aditivo). (C) **campaign-run assíncrono** p/ >8 passos (`EdgeRuntime.waitUntil`, batches; pequenas seguem síncronas). `/security-review` independente **SAFE** (flagou XSS **pré-existente** `DashboardHome:677` dangerouslySetInnerHTML → tarefa spawned). Smokes click **G1-G9+G1b** · campaign **A-H** · e2e auto-monetize ✅ · tsc 0 · drift exit 0. 4 commits (`9bb5bba`/`bb999c1`/`7cbd036`/`b468c98`).
> 27	
> 28	**Sprint v6.27.2 selado em 2026-06-04** — **Refund-on-failure: charge-without-value fechado (OTD-AEO-REFUND)**. Diretiva Sovereign "continue com os próximos passos". Probe-first material elegeu o item de **menor blast radius e maior valor seguro** dos 3 next-steps (refund protege saldo do usuário, zero ação outward); os outros 2 dependem do Sovereign (nurturing externo precisa de domínio Resend verificado — **zero refs RESEND no código**; 1º pago E2E precisa de GO econômico). **OTD-AEO-REFUND FECHADA:** `aeo-audit` debitava 5 mco na entrada e, se o persist falhasse, devolvia 500 **sem estornar** (charge-without-value, verificado no código). Helper compartilhado **`refundMco`** (`_shared/billing.ts` → `add_mco_coins`, service-role-only, simétrico a deduct, guarda `p_amount>0`, nunca lança); `aeo-audit` (5) e `lead-score` (1) rastreiam `charged` e estornam em qualquer falha pós-cobrança (persist-fail + catch). **Prova:** smoke `smoke-aeo-refund.ts` **6/6 LIVE** (deduct 5→15 / add 5→20 restaurado · guarda nega -10 · net-zero) + unit `_shared/billing.test.ts` **4/4** + regressão [[aeo-audit|aeo-audit]] intacta. **Honestidade Lei 1:** persist-fail não é forçável por input → fiação coberta por unit+code, não por falha forçada (declarado). Contrato refund-on-failure no billing SSOT (`mcoin-cost-calibration.md`). Deploys 86.69/85.62kB · tsc 0 · suíte **269** (265→269) · Phase 5c **SEAL ALLOWED** (8 verified) · Mesh **8774** (1 órfão `aeo:` podado). 3 commits. **Novo Top Gap:** entrega externa de nurturing (bloqueada por domínio Resend — Sovereign) · 1º pago E2E (GO econômico) · **OTD-INTENT-DISPATCH-REFUND** = aplicar `refundMco` ao gap pós-débito do `orchestrate-content` (flywheel, sessão dedicada). **Lição:** probe-first descartou 2 dos 3 next-steps (dependência externa) e leu o código pra confirmar que o gap de refund era REAL (linha 56 débito → 118 persist-fail sem refund) antes de construir — não assumi o bug, verifiquei.
> 29	
> 30	**Sprint v6.27.1 selado em 2026-06-03** — **Intent executor un-gated: dispatch outward REAL + OTD-INTENT-TRANSITION-GUARD**. Diretiva Sovereign "ACTIVATE AGENTIC OUTWARD EXECUTION" (Step 1 guard ANTES do Step 2 dispatch). **(1) OTD-INTENT-TRANSITION-GUARD (migration `20260603270000`):** trigger `tr_guard_intent_plan_transition` (`SECURITY DEFINER`/`search_path=''`) deixa **só `service_role`** colocar uma linha em `status='approved'`/`'executed'`. **O `/security-review` (subagente independente) pegou que meu guard inicial era BEFORE UPDATE-only → vetor INSERT aberto** (tenant `POST intent_plans {status:'approved'}` pulava o HITL e cavalgava a re-validação até dispatch). Estendi p/ **BEFORE INSERT OR UPDATE** + endureci a RLS `insert_own` (`status IN proposed/auto_approved/pending_hitl`) + `tr_validate_intent_plan_bindings` (binding = mesmo tenant). **Prova material before/after**: INSERT `status='approved'` por JWT de tenant → **201 ANTES / 403+42501 DEPOIS**. **(2) Dispatch outward REAL (un-gate):** `intent-execute` pós-`executed` roteia por precedência — `campaign_id`→campaign-run · `enrollment_id`→nurture-dispatch · senão canais content/social/affiliate→orchestrate-content — encaminhando o **JWT do chamador** (cascata self-bila o mesmo tenant). Kill-switch `INTENT_OUTWARD_DISPATCH_ENABLED=false`→governança-only. Idempotência: marca executed 1º (re-execute=already, sem dobro de dispatch/cobrança). `db push` Finished · types regen · deploy 83.01kB. **Smoke 28/28 LIVE throwaway** (guard INSERT+UPDATE 42501 · golden rule · dispatch REAL provado por **downstream guard a saldo 0**: orchestrate-content **402** + campaign-run **422**, zero gasto · binding foreign rejeitado). tsc 0 · eslint 0 · suíte **265** · drift audit **exit 0**. BoK patcheada (SDD + data-model) + SOP reescrita (gates 4/5/6 + OTD-INTENT-DISPATCH-REFUND). **Novo Top Gap:** entrega externa real de nurturing (gated; `resend_api_key` pronto) · **OTD-INTENT-DISPATCH-REFUND** (refund pós-dispatch-fail) · 1º dispatch pago E2E real (gated em GO Sovereign — UI HITL + guard já armados). **Lição:** o `/security-review` independente pegou o furo INSERT que o self-review (focado no PATCH) deixou passar — exatamente o vetor que a diretiva mandava fechar; provar before/after material (201→403) separa "guard escrito" de "guard que funciona" (Lei 1).
> 31	
> 32	**Sprint v6.27.0 selado em 2026-06-03** — **Marketing-Hub: rosto + executor + AEO (FR-MH-009/010)**. `/handson` → `/goal` Sovereign com os 3 próximos passos ("backend pronto, falta o rosto"). **(1) Executor de `intent_plans` (FR-MH-009 HITL):** edge fn `intent-execute` (approve/reject/execute) na máquina `proposed→pending_hitl→approved|rejected→executed`; **golden rule** = o `execute` **re-valida** o alto-impacto sobre o plano **armazenado** (gate compartilhado `_shared/intent-policy.ts`) e recusa `409 hitl_required` todo outward sem aprovação humana — **nunca confia em `auto_approved`**; tenant-guard 404; `/security-review` SAFE → adotada **fail-closed** em plano não-array; smoke **17/17**. **(2) AEO (FR-MH-010 — última FR):** `aeo_audits` (RLS) + `aeo-audit` (JWT · 5 mco atômico · provider **degradado documentado** OTD-MH-003 LLM-as-answer-engine · 1 snapshot/query); `db push` Finished; smoke **12/12** (RLS cross-tenant leaked=0). **(3) UI follows:** `useIntentOrchestrator`/`useAEO` + `IntentOrchestratorPanel`/`HITLApprovalCard`/`AEOAuditPanel` + enroll de nurturing no Customer 360 → `/dashboard/marketing`; **+8 testes (257→265)**; **UI logada verificada** (magic link Usuário Zero + agent-browser, chunk novo, zero crash). tsc 0 · eslint 0 (tocados) · build 22.88s deploy nginx. 5 commits. **Novo Top Gap:** dispatch outward real do executor (hoje gated) + **OTD-INTENT-TRANSITION-GUARD** (CHECK de transição antes de ligar o envio real) · entrega externa de nurturing (gated; credencial pronta) · **OTD-AEO-REFUND** (refund pós-débito). **Marketing-hub: TODAS as FRs backend+UI entregues** (001..012). **Lição:** probe-first viu que o gate de policy já existia inline no orchestrate → extraí p/ `_shared` em vez de duplicar (o `execute` re-roda **o mesmo** gate, não uma cópia); o `/security-review` independente pegou o fail-open que o self-review deixaria passar.
> 33	
> 34	**Sprint v6.26.0 selado em 2026-06-03** — **Drift audit + P0 ledger + 3 FRs marketing-hub**. `/handson` → diretiva Sovereign "🔴 auditar drift deployado↔migrations" (irmãos do hotfix `async_orchestrate_step`) → "faça 2+3+4". **(1) Drift audit:** 9 superfícies via Management API read-only (ledger 96==96 · contrato RPC 12/12 · verify_jwt edge 23==23 · 34 triggers · RLS toda-tabela · pg_net siblings) → **incidente ISOLADO**; único drift real `rls_auto_enable` (event-trigger out-of-band benigno que liga RLS em tabela nova) **capturado** + 6 SECURITY DEFINER `search_path` travado + trigger pg_net morto (kong:8000) dropado. Anticorpo `scripts/qa/audit-schema-drift.sh` (8 checagens, exit 0) + SOP `schema-drift-audit.md`. **(2) 🔴 P0 ledger:** os 3 RPCs (award/add_user_score/deduct) davam EXECUTE a anon/authenticated + confiavam `p_user_id` → cunhagem de mcoCoins via PostgREST direto; REVOKE (edge-only) + guardas em deduct (sinal + posse NULL-safe); **exploits provados BLOQUEADOS** em prod (erro/42501/permission denied). **(3) functionName 13/13** fallback LLM. **(4) FR-MH-008 cron** (`nurture-cron`+pg_cron `*/15`, modo service-role em nurture-dispatch; smoke 5/5+USER 10/10). **(5) FR-MH-012 BYOK** (`resend_api_key` per-tenant Vault — defs VIVAS verbatim — +Settings; round-trip 8/8). **(6) FR-MH-009 Intent+HITL backend** (`intent_plans`+`intent-orchestrate`: policy auto/HITL canal-outward-fail-safe + rationale XAI; smoke 8/8). 9 commits · 3 migrations · 4 deploys · `/security-review` independente por migration (todas SAFE) · Phase 5c **SEAL ALLOWED** (11 verified) · Mesh **8770** (orphan de smoke limpo) · Survival Laws **4/4**. **Novo Top Gap:** UI follows (enroll nurturing — hook já existe — + `useIntentOrchestrator`/`HITLApprovalCard`) · executor de `intent_plans` (re-validar ação outward no execute) · entrega externa nurturing (gated; credencial pronta) · FR-MH-010 AEO (última FR). **Lição:** probe-first viu que a metade-IA do FR-MH-012 já existia (só a metade-canal era nova) + evitou o trap do template stale de credenciais (reproduzir defs VIVAS, não migration antiga); o drift audit virou anticorpo reexecutável.
> 35	
> 36	**Sprint v6.25.0 selado em 2026-06-03** — **Flywheel ressuscitado + calibração mcoCoins**. `/handson` → diretiva Sovereign ("o que falta pro 1º run pago E2E + já calibrar o COIN_COST?"). Calibrei **antes** do run (não rodar a 1ª transação econômica a preços inventados): **OTD-MCOIN-CALIBRATION FECHADA** — modelo `mco=ceil(custo_usd/$0.018_piso×4)` (piso=Enterprise); surpresa honesta — `10` (orchestrate) e `125` (canvas vídeo) **já** eram ~4× sobre custo real, único furo `IMAGE_GENERATION 3→9` (`CONTENT_GENERATION 5→2`). O **1º run pago E2E então expôs que o flywheel de conteúdo estava MORTO desde o cutover de chaves (01-06)** — 3 P0s compostos deixavam todo run preso em `running`: **#1** `orchestrate-step` faltava no `config.toml` (`verify_jwt=true` → gateway **401** na chave opaca `sb_secret_` do pg_net); **#2** `async_orchestrate_step` hotfixada em prod **sem migration** (`p_service_jwt_legacy`≠`p_service_key` → **PGRST202** → auto-chain morto) → migration `20260603190000` realinha + `GRANT service_role`, `/security-review` SAFE, RPC **204**; **#3** `wp_site_url` não-www → **301 → POST vira GET** → WP devolve LISTA de posts → `publish-wordpress` endurecido (valida `id`, 502 honesto) + `wp_site_url→www`. **Provado E2E**: run `89f18bea` **auto-completou 6/6 passos sem kick** → rascunho WP `?p=14` + `content_mesh_asset` done. Phase 5c **SEAL ALLOWED** (11 verified). Mesh **8769**. Survival Laws **4/4**. 7 commits. **Novo Top Gap:** auditar **drift deployado↔migrations** (outras RPCs/fns hotfixadas em prod?) · limpar artefatos de teste (5 posts parqueados 2027 + 2 rascunhos WP) · FR-MH-009/010/012 + Nurturing follow-up · functionName nas 9 fns. **Lição:** o 1º run pago **não "falhou"** — fez seu trabalho: expôs 3 P0s silenciosos no coração do produto (falha sem erro visível, sem auto-refund); calibrar **antes** do run foi a decisão certa (transação econômica honesta).
> 37	
> 38	**Sprint v6.24.0 selado em 2026-06-03** — **Sessão de alta densidade** (diretiva Sovereign: selar a 45% é desperdício → usar a janela 1M inteira, selar só a ~95%; **Lei 3 recalibrada** em survival.md: poda≠selar). Resposta ao "faça os três, foco em endurecer o flywheel": 5 entregas pós-v6.23.0, cada uma com **smoke LIVE throwaway**. **(1) MVP-5 Atribuição (FR-MH-007)**: `handle-ml-postback`→`marketing_attribution` (campaign_id FK-safe, fail-soft) + `useCampaignAttribution`+card "Receita Atribuída"; smoke DB 4/4 (FK 23503 + de-linked). **(2) Hardening+observabilidade (FOCO)**: `eslint .` **honesto** (Deno `supabase/functions`+tailwind excluídos — ~3716 erros falsos, exit mascarado por `| tail`) + functionName telemetry no flywheel + smoke integração lead→score→campaign→attribution 5/5. **(3) Customer 360 (FR-MH-011)**: VIEW `security_invoker` RLS-safe + `useCustomer360`+drawer; /security-review SAFE + **isolation smoke 4/4** (B não vaza p/ A). **(4) Nurturing (FR-MH-008)**: engine `sequences`+`sequence_enrollments` (FK composta CASCADE) + `nurture-dispatch` **consent-gated** (envio gated) + `useNurturing`+`NurturingPanel`; /security-review SAFE + **consent-gate smoke 10/10**. 2 migrations /security-review SAFE (subagentes independentes) · tsc 0 · suíte **259** · eslint exit 0 honesto · 4 deploys · 5 smokes LIVE. Phase 5c **SEAL ALLOWED** (11 verified). Mesh **8761** (orphan obs de smoke limpo + smoke vacinado). Survival Laws **4/4**. 8 commits. **Novo Top Gap:** 1º run pago E2E (gated GO) · Nurturing follow-up (entrega externa real + cron + UI enroll/dispatch) · OTD-MCOIN-CALIBRATION · FRs restantes FR-MH-009/010/012. **Lição:** densidade máxima por sessão (5 frentes numa só) sem perda de materialidade — cada uma provada por smoke LIVE; o gate de lint estava mentindo (exit mascarado) — fix de raiz restaura honestidade da Lei 1.
> 39	
> 40	**Sprint v6.23.0 selado em 2026-06-03** — Marketing Hub backend completo + **MVP-4 UI live**: `campaign-run` (FR-MH-004) fechou o backend, depois o módulo inteiro ganhou rosto em `/dashboard/marketing` **absorvendo a UI v1** (não duplicando). **(1) campaign-run** JWT + débito atômico do FEE `CAMPAIGN_RUN` (10) → dispatch **paralelo** (`Promise.allSettled`) dos passos p/ `orchestrate-content` (self-bila 10) = **cascata fiel 10+10×N**; `email`→blocked; cap 8; smoke **13/13 zero-custo** (guards + isolamento de tenant + email-blocked + débito atômico 100→90 + cleanup); deploy 80.92kB; cascata paga **gated em GO**. **(2) MVP-4 UI**: `/dashboard/marketing` (LeadBoard 5 colunas + Pontuar/`lead-score` + overview campanhas; nav Target) + absorção v1 (`CampaignWizard` +Intenção/passo **Passos** composer→persiste `campaign_steps`; `CampaignDetail` +card **Passos & Execução** status vivo + `CampaignRunButton`). **(3) Hooks**: `useLeads`/`useLeadScore`/`useCampaignSteps`/`useCampaignRun`/`createCampaignWithSteps` + `src/lib/edge.ts`. tsc 0 · **11 testes** (suíte **255/257**) · eslint limpo nos tocados · build 22.32s deploy nginx · **UI LOGADA verificada** (magic link + agent-browser: `/dashboard/marketing` + wizard 6-passos/Passos renderizam, 0 erros console, zero mutação prod). Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8760**. Survival Laws **4/4**. 4 commits. **Novo Top Gap:** 1º run pago E2E (Sovereign cria campanha→Rodar, gated em GO) · OTD-MCOIN-CALIBRATION ($) · OTD-CAMPAIGN-RUN-ASYNC (fila p/ campanha grande) · MVP-5 attribution→ROIWidget · **dívida de lint repo-wide** (~3716 erros pré-existentes em `supabase/functions` Deno, exit mascarado por `| tail` — não introduzidos nesta sessão). **Lição:** a diretiva Sovereign de calibração de contexto (1M/Max → não adiar por "contexto" antes de ~400k) destravou rodar o MVP-4 completo numa sessão; probe-first pegou a UI v1 existente ANTES de codar (absorver, não duplicar); a11y do agent-browser estava stale na transição framer-motion → li o stepper-text em vez de fabricar (Lei 1).
> 41	
> 42	**Sprint v6.22.0 selado em 2026-06-03** — Campaign Core + LLM Fallback + Lead Scoring: 4 entregas materiais via `/handson`→ação nos alertas→próximos priores. **(1) Alerta meta_config** verificado **VAZIO** (0 linhas · `auth.users` 1==`profiles` 1 — não fabriquei limpeza inexistente, Lei 1). **(2) MVP-2 Campaign Core LIVE** (migration `20260603025256`): `campaigns` **ABSORVIDA** via `ALTER` (+intent/channels/mesh_node_id + `UNIQUE(id,user_id)`) + `campaign_steps` (FK composta tenant-`CASCADE`, espelha lead_events) + `marketing_attribution` (FK simples `SET NULL` + RLS `WITH CHECK`, espelha consents); tenant-FK provado **comportamental** (23503 + 42501 autenticado + 201 + zero-resíduo); `/security-review` **SAFE** (subagente independente); mesh `7628892b`. **(3) OTD-LLM-FALLBACK FECHADA cedo** (SLA 06-07, owner engineer): probe-first achou o helper já live em 11 fns → fechei o gap de observabilidade do SOP (telemetria `infra_health_logs` autossuficiente em Deno) + **1º teste de edge-helper do projeto** (6 casos) + 11 fns redeploy; mesh `6061a6d2`. **(4) lead-score LIVE** (FR-MH-003): JWT + 1 mco atômico + IA per-user→sistema fail-soft; **smoke E2E** 200 · score=80 (`source=ai`) · débito 100→99 · zero-resíduo. **Calibração mcoCoins**: `COIN_COSTS` centralizado + dívida **OTD-MCOIN-CALIBRATION** (o `10` é redondo, não $-calibrado; `orchestrate` cobra 10 flat < soma dos componentes 18; vídeo é o maior custo real). Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8759**. Survival Laws **4/4**. 6 commits. **Novo Top Gap:** `campaign-run` cascata fiel (**ADIADA por decisão Sovereign** — código financeiro + contexto saturado, Lei 3) + OTD-MCOIN-CALIBRATION (preços $ por-modelo/vídeo) · MVP-4 hooks+UI `/dashboard/marketing` · MVP-5 attribution. **Lição:** probe-first pegou a OTD já 80% pronta (zero retrabalho) e a divergência `campaigns`/`campaign_metrics` já-existentes; decisão financeira de `campaign-run` **registrada ao Sovereign em vez de improvisada** (Master Protocol).
> 43	
> 44	**Sprint v6.21.0 selado em 2026-06-03** — Marketing Hub (v2): BoK 9/9 + 11 agentes + MVP-1 Lead Core LIVE. Novo **módulo soberano** criado do zero seguindo o Master Execution Protocol (BoK-first), dirigido pela diretiva Sovereign de um "Framework Universal de Marketing (Plataforma Agentic)" (benchmarks HubSpot/Salesforce). `/bok-scribe` selou a **suíte BoK 9/9** (1732 LOC, `docs/bok/marketing-hub/`, traceability **0 órfãos**, mesh seal `d5163fed` DERIVES_FROM meta-api) — módulo nasce como **v2 de consolidação** que **absorve e escala** o marketing v1 disperso (orchestrate-content → executor de campanha; whatsapp_leads → tutela meta-api→marketing-hub; marketing-growth Pantheon **elevado, não recriado**), natureza **Ambos** (interno Usuário Zero + comercial per-tenant). `/bok-agents-generator` produziu o **sistema de 11 agentes** (8 BoK + AEO/Intent-Orchestration/Demand-gen + Pantheon Reconciliation). Após revisão Sovereign ("aprovado"), **MVP-1 Lead Core** foi ao ar: migration `20260603000000` (`leads`/`lead_events`/`marketing_consents` + RPC `erase_lead()` LGPD SECURITY DEFINER), aplicada via `db push`. O `/security-review` (subagente **independente**) pegou **1 cross-tenant MEDIUM** (FK de tabela-filha sem co-escopar `user_id` → A injeta evento no lead de B) → fechado com **FK composta tenant-escopada `(lead_id,user_id)→leads(id,user_id)`** + provado **material** (23503 no ataque, 201 no legítimo, cleanup zero-resíduo). Phase 5c **SEAL ALLOWED** (7 verified). Mesh **8755**. Survival Laws **4/4**. 4 commits. **Novo Top Gap:** MVP-2 Campaign Core deve **ABSORVER** a `campaigns` já existente (colisão real achada por probe-first), NÃO criar nova; + MVP-3 edge fns (`lead-score`/`campaign-run`) · MVP-4 hooks+UI (`/dashboard/marketing`) · MVP-5 attribution. **Lição:** probe-first do schema ANTES de codar pegou 2 divergências doc↔realidade (`campaigns` existe, `projects` não) que quebrariam o apply; e o `/security-review` por subagente independente (não auto-avaliação) pegou o furo de tenant que o self-review deixou passar.
> 45	
> 46	**Sprint v6.20.4 selado em 2026-06-02** — Probe OAuth ML + verificação visual do disconnect (**seal de conhecimento — zero código de produção**): dirigido por 2 diretivas do Sovereign no padrão **probe-first material**. **(#1)** Fechado o resíduo visual da v6.20.3 — disconnect Meta/social verificado **NON-DESTRUTIVO** na UI logada: login como Usuário Zero via Supabase **Admin API `generate_link`** (magic link, método per-user reproduzível, sem token do DevTools nem senha) dirigindo `agent-browser` 0.27.0; `/dashboard/social` renderiza 3 contas Ativa (LinkedIn/IG/FB) com botão Desconectar **interativo** wired a `rpc('disconnect_social')` (`useMetaConfig`/`useSocialAccounts` chamam `disconnect_meta`/`disconnect_social`, zero `.delete()`); **nenhum clique** → 3 contas intactas. **(#2) probe-first do OAuth ML CONCLUÍDO** — veredito material: ML **sem API oficial de afiliados** (403 até no WebFetch da Anthropic); link oficial **exige portal LOGADO** (segui o `meli.la` → `/social/…?matt_word=…&matt_tool=…&ref=<ASSINADO>`, token `ref` **não-fabricável**); **datacenter BLOQUEADO p/ Chromium real** (`agent-browser` no portal → "Hubo un error accediendo a esta pagina"). ⇒ Browser Operator (#2) **não roda do datacenter** (runtime = navegador do user / IP residencial); resolver `src/lib/affiliate.ts` tem `matt_word` mas **falta `matt_tool`** (per-user). **Experimento de atribuição de clique em curso** (Sovereign, dispositivo independente, ~06-03) → **decisão do #2 PAUSADA aguardando o dado** (Cérebro sem mãos: não vejo o painel de afiliados — logado + IP bloqueado). Phase 5c **SEAL ALLOWED** (4 verified). Mesh **8753**. 2 commits (docs). **Novo gap (Top Gap):** decisão do Browser Operator/`matt_tool` aguarda o nº de cliques de amanhã. **Lição:** probe-first poupou construir um Browser Operator no datacenter que **nunca funcionaria** (IP bloqueado, provado material) — e refutou "OAuth resolve" (ML não tem API).
> 47	
> 48	**Sprint v6.20.3 selado em 2026-06-02** — Disconnect RPC + revogação de segredo órfão: **FECHADO o Top Gap que a v6.20.2 sinalizou** — desconectar Meta/social fazia `.delete()` pela view → INSTEAD OF DELETE só apagava a linha base, deixando o segredo Vault **órfão** (plaintext retido; 12 órfãos Meta observados em prod). RPCs `disconnect_meta()`/`disconnect_social(p_account_id uuid)` (migration `20260602160000`) espelham `disconnect_wordpress` (`SECURITY DEFINER`, `search_path=''`, fail-closed `28000`, EXECUTE só authenticated): deletam a linha **E** revogam o segredo. Guard de tenant por name-binding (`id`-de-linha + PK ⇒ atacante nunca casa nome de segredo alheio; UUID bruto nunca vaza ao cliente). Limpeza one-time **12→0** órfãos Meta (orphan-scoped via `NOT EXISTS`+`right(name,36)`), 3 sociais vivos intactos. Hooks migrados `.delete()`→`.rpc()`; `types.ts` regenerado. **Também (diretiva A):** `/security-review` redundante do `87c926f` (guard de tenant v6.20.2) → **LIMPO 9/10**. Ambos os reviews SAFE; suíte RPC 5/5 em `BEGIN…ROLLBACK` (happy meta+social · foreign-id no-op · planted-ref name-binding · unauth 28000); Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8752**. 4 commits. **Lição:** verificar materialidade ANTES de codar (Lei 1) — o gap de tenant guard da diretiva original já estava 100% fechado em prod, então a Parte B virou o foco real em vez de uma migration redundante.
> 49	
> 50	**Sprint v6.20.2 selado em 2026-06-02** — Idempotência da encriptação + guard de tenant nas views irmãs: **FECHADO o Top Gap que a v6.20.1 sinalizou** — `trg_encrypt_user_api_keys` (+ irmãos meta/social) chamava `vault.create_secret` incondicionalmente → re-salvar segredo p/ valor novo colidia no índice único `vault.secrets.name` (`23505`). Helper `public.vault_upsert_secret(value,name,desc)` (`SECURITY DEFINER`, `search_path=''`, EXECUTE revogado de PUBLIC/anon/authenticated) rotaciona in-place via `vault.update_secret` (mesmo UUID, sem órfãos) senão cria; as 3 encrypt triggers passam a usá-lo (migration `20260602140000`). O `/security-review` dessa migration **expôs um gap pré-existente** nas INSTEAD OF de `meta_config`/`social_accounts` (sem guard `auth.uid()` → injeção cross-tenant id-novo; o overwrite id-colidente já era fail-closed pelo PK — achado HIGH do review REFUTADO material) → guard `42501` portado pras 2 (migration `20260602150000`). Ambas `/security-review` **SAFE**; tudo provado material via Management API em `BEGIN…ROLLBACK` (antes 23505/injeção OK, depois OK/42501); Phase 5c **SEAL ALLOWED** (7 verified). Mesh **8751**. 6 commits. **Novo gap (Top Gap):** desconectar Meta/social deixa o segredo Vault **órfão** (INSTEAD OF DELETE só apaga a linha base) — precisa de RPC dedicada de disconnect (nula+revoga) no padrão `disconnect_wordpress()`, débito LGPD. **Lição:** adversarial-verify material (PK fail-closed + md5 da vítima) refutou um HIGH e ao mesmo tempo revelou o gap real adjacente — resolvido na mesma sessão em vez de empurrar pra fria.
> 51	
> 52	**Sprint v6.20.1 selado em 2026-06-02** — WordPress BYOK + fix do double-fire da encriptação de credenciais: fechado o P0 que a v6.20.0 sinalizou (`SocialAccountsPage` salvava/desconectava WP via `.upsert(onConflict)` numa VIEW → HTTP 400 `42P10`). Save → `.insert()`; disconnect → RPC **`disconnect_wordpress()`** (`SECURITY DEFINER`, `auth.uid()`, nula 3 cols WP + **deleta o segredo do Vault** — revogação LGPD) (migration `20260602120000`). Corrigir isso revelou bug **muito maior**: o `trg_instead_of_user_api_keys` usava `INSERT...ON CONFLICT DO UPDATE` → trigger de encriptação dispara **2×** numa só statement → `vault.create_secret` nome duplicado → **`23505`**, quebrando connect/save de **todo** usuário com linha pré-existente (e `.update` re-encriptava o `••••`). Trocado p/ **UPDATE-first / INSERT-if-not-found** + **guard de tenant** (`auth.uid()` → `42501`, fecha escrita cross-tenant que o ON CONFLICT mascarava) (migration `20260602130000`). Tudo provado material via Management API; 2 migrations `/security-review` **SAFE**; Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8750**. 5 commits. **Novo gap (Top Gap — task spawned):** `trg_encrypt_user_api_keys` (+ irmãos meta/social) não-idempotente → editar segredo p/ valor novo sem desconectar antes ainda dá `23505`; conserto = update-or-create por nome nas 3 tabelas, precisa de `/security-review` próprio. **Lição:** probe-first material pegou que o `.insert` sozinho NÃO bastava (o bug estava na camada de encriptação, não nos 2 `.upsert` reportados).
> 53	
> 54	**Sprint v6.20.0 selado em 2026-06-01** — Afiliados híbrido + catálogo Apify real + BYOK per-user: corrigido o link de afiliado que abria login do CloudPanel (`panel.gcrux.com` proxy morto + `app_id` como affiliate id) → resolver **híbrido** `meli.la` cravado (per-user `metadata.shortlinks`) senão `product_url?matt_word=<affiliate_tag>` fail-closed (`src/lib/affiliate.ts` + 14 testes; 302s reais provados). ML bloqueia todo server-side (API 403/401, página→account-verification, nosso IP **e** Supabase Edge) → enriquecimento via actor **Apify** residencial (`enrich-affiliate-products.ts` SKU-match + `discover-affiliate-products.ts` descoberta real validando "viral mind") + gate de verificação em `useAffiliateProducts` + cron 6/6h. **2 IDs fabricados removidos** → catálogo com **3 produtos reais** (Roborock R$17.770 · Family Hub R$18.946 · 8K Neo QLED R$39.000). **BYOK per-user `apify_token`** no padrão Vault (migration `20260601060000`, `/security-review` PASS — pegou regressão `security_invoker`) + campo Settings + fix do P0 de `000600` (`.upsert()`→`.insert()` em view sem constraint). Phase 5c **SEAL ALLOWED** (12 verified). Mesh **8748**. Survival Laws 4/4. 6 commits. **Próximo:** Operador de Browser Autenticado (probe-first) p/ ações logadas (ML Compartilhar→meli.la). **Lição:** probe-first economizou 3 becos (API ML/Firecrawl/actor velho) e pegou IDs fakes + regressão de credencial.
> ```

## 🤖 Claude *(18:22:07)*


## 🤖 Claude *(18:22:28)*

═══════════════════════════════════════════════════════════
  HANDSON — Vision MCP Fatia 2 (selo 2026-06-15 · v6.37.0)
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
  Fase selada: **Vision MCP Fatia 2 — 4 Billable Tools + BYOK Foundation** (+ fechamento do handshake/interop da Fatia 1)
  Últimos commits:
```
1a110fb chore(sprint): register v6.37.0 vision-mcp Fatia 2 (4 billable tools + BYOK) + proof manifest
2676f91 docs(handoff): seal Vision MCP Fatia 2 — 4 billable tools + BYOK
70846b0 docs(readme): v6.37.0 — Vision MCP Fatia 2 + Fatia 1 handshake/interop close
88730c3 test(vision-mcp): handshake/adversarial E2E + Fatia 2 smokes (anticorpos)
93d2abb feat(settings): Firecrawl BYOK field + vision-mcp mcoCoin classes
```

📂 **MUDANÇAS PENDENTES**
  Worktree limpo ✅ — em sincronia com `origin/main` (0 ahead / 0 behind). `scratch/` limpo ✅.

🏗️ **INFRA** (todos saudáveis)
```
mcorch_vision_mcp:    Up 23min (healthy) — /health 200 · 5 tools · proto 2025-11-25
mcorch_claude_mem:    Up 2h (healthy)
mcorch_chroma:        Up 2h (healthy) — API v2 heartbeat OK
mega-brain-daemon:    Up 2h (healthy)
mega-brain-webhook:   Up 2h (healthy)  ·  mega-brain-dashboard: Up 2h
```
  Tools no `127.0.0.1:3200`: `mesh_search · vision_describe_image · vision_analyze_video · deepsearch_scrape · mesh_consolidate_reference`

🧠 **KNOWLEDGE MESH**
  **8917 nós** · **9070 arestas** · 100% embedded (768d HNSW cosine)
  Último handoff node: `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64`

🔧 **TYPESCRIPT**
  Zero erros ✅ (`tsc --noEmit` exit 0 — root + pkg)

📚 **BoK SUITES**
  `vision-mcp` — **completo (9/9 + blueprint + agent-system)** ✅ — BoK Gate **ABERTO** para as próximas Fatias.
  20 suítes presentes em `docs/bok/`; nenhuma incompleta detectada no módulo ativo.
  Seal na malha: `318862b7` (documentation_suite vision-mcp · DERIVES_FROM mcorch-constellation)

📌 **SPRINT**
  Goal (sprint-priorities.md): *Distribuição social autônoma operacional — pipeline publica LinkedIn auto; Twitter ao subir tier; Instagram após App Review Meta.*
  Foco vivo das últimas sessões: **Vision MCP** (MCP nativo de percepção visual + deepsearch, container Sovereign Mesh, 0 edge fns).

⚡ **PRÓXIMOS PASSOS** (do Pending do seal vision-mcp)
  1. **`deepsearch.run` (FR-VM-007 — assíncrono)** — a metade "google/gemini" do deepsearch; fiel à FRD é job_id→poll + partial-delivery refund (§4.5). Feature distinta e mais pesada, teed-up para sessão própria.
  2. **Fatia 3** — PAT/OAuth 2.1 (RFC 9728 AS) · Plugin Zip · jobs assíncronos · erase LGPD (`erase_vision_artifacts`).
  3. **vhost nginx `mcp.mcorch.com`** (OTD-VM-013) — hoje só loopback `127.0.0.1:3200`; **ação do Sovereign** (root/DNS Cloudflare).
  4. Menores: registrar **OTD orphan-sub** (risco residual LOW) na emenda BoK da Fatia 2 · migration `infra_health_logs ADD metadata jsonb` (telemetria rica) · platform `FIRECRAWL_API_KEY` se quiser default cobrado p/ scrape.

⚠️ **ALERTAS**
  Nenhum alerta ✅ — worktree limpo, tsc 0, 6 containers saudáveis, scratch vazio, BoK do módulo ativo completa, em sync com origin.

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

O caminho natural é **`deepsearch.run` assíncrono** (item 1) — é a única tool do conjunto vision-mcp ainda não construída e fecha o "deepsearch fundamentado" prometido no blueprint. Os itens 3 (vhost) e parte do 2 dependem de ação sua (DNS/root). Qual frente abro?

## 👤 User *(18:27:47)*

⚡ PRÓXIMOS PASSOS (do Pending do seal vision-mcp)

1. `deepsearch.run` (FR-VM-007 — assíncrono) — a metade "google/gemini" do deepsearch; fiel à FRD é job_id→poll + partial-delivery refund (§4.5). Feature distinta e mais pesada, teed-up para sessão própria.
2. Fatia 3 — PAT/OAuth 2.1 (RFC 9728 AS) · Plugin Zip · jobs assíncronos · erase LGPD (`erase_vision_artifacts`).
3. vhost nginx `mcp.mcorch.com` (OTD-VM-013) — hoje só loopback `127.0.0.1:3200`; ação do Sovereign (root/DNS Cloudflare).
4. Menores: registrar OTD orphan-sub (risco residual LOW) na emenda BoK da Fatia 2 · migration `infra_health_logs ADD metadata jsonb` (telemetria rica) · platform `FIRECRAWL_API_KEY` se quiser default cobrado p/ scrape.

## 🤖 Claude *(18:28:45)*


## 🤖 Claude *(18:28:48)*

You pasted the roadmap back — I read that as "proceed." Before I commit the session (and possibly a multi-hour paid-async build), one scope fork is genuinely yours to call, because the answer changes the whole plan: `deepsearch.run` async is heavy (Google/Gemini legs + job→poll→partial-refund infra), while the "menores" are cheap antibodies. Item 3 (vhost nginx) is your action (root/DNS), and item 2 (Fatia 3) is a separate big arc.

## 🤖 Claude *(18:28:53)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "Por onde executo nesta sess\u00e3o de vision-mcp? (janela 1M fresca \u2014 d\u00e1 pra empacotar)",
      "header": "Escopo",
      "multiSelect": false,
      "options": [
        {
          "label": "deepsearch.run + menores",
          "description": "Construir a feature headline \u2014 deepsearch.run ass\u00edncrono (FR-VM-007: job_id\u2192poll\u2192partial-delivery refund \u00a74.5, legs Google/Gemini) \u2014 E, aproveitando a janela, fechar os ant\u00eddotos baratos: registrar OTD orphan-sub na emenda BoK da Fatia 2 + migration infra_health_logs ADD metadata jsonb. Empacota a sess\u00e3o (Lei 3)."
        },
        {
          "label": "S\u00f3 deepsearch.run async",
          "description": "Foco 100% na feature pesada (infra de jobs ass\u00edncronos + poll + refund parcial sobre legs pagas). Deixa os menores e a config FIRECRAWL_API_KEY para depois."
        },
        {
          "label": "S\u00f3 os menores primeiro",
          "description": "Fechar os ant\u00eddotos r\u00e1pidos e de baixo risco (OTD orphan-sub na BoK + migration metadata jsonb) e reavaliar antes de abrir a feature paga pesada. Sem gasto de provider nesta sess\u00e3o."
        },
        {
          "label": "Iniciar Fatia 3",
          "description": "Abrir o arco maior de auth/jobs/LGPD \u2014 PAT/OAuth 2.1 (RFC 9728 AS) + erase_vision_artifacts \u2014 em vez do deepsearch.run. Sess\u00e3o pr\u00f3pria, mais pesada."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "Por onde executo nesta sessão de vision-mcp? (janela 1M fresca — dá pra empacotar)"="deepsearch.run + menores". You can now continue with these answers in mind.
> ```

## 🤖 Claude *(18:31:48)*


## 🤖 Claude *(18:31:54)*

O Sovereign escolheu **deepsearch.run async + menores**. Plano travado.

**ORO triplet desta task:**
- **Operator:** MCORCH Master Execution Agent
- **Reviewer:** Sovereign + `/security-review` independente (subagente)
- **Owner:** Sovereign — 1ª tool *assíncrona* que debita mcoCoins + chama providers pagos (Google/Gemini) com refund parcial; blast radius = saldo do tenant + container `mcorch_vision_mcp`

BoK gate: **ABERTO** — `deepsearch.run` é a FR-VM-007 já documentada na suíte 9/9 selada. Sem improvisação além do documentado (Lei 2).

Vou primeiro **escotear inline** a estrutura real (pacote + seções exatas da BoK + schema) para montar o work-list, depois disparo um Workflow de mapeamento/design fundamentado.

## 🤖 Claude *(18:31:55)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Vision MCP: deepsearch.run async + menores",
  "summary": "Construir a tool ass\u00edncrona deepsearch.run (FR-VM-007: job\u2192poll\u2192partial-refund) + ant\u00eddotos (OTD orphan-sub na BoK + migration infra_health_logs metadata jsonb)"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Vision MCP: deepsearch.run async + menores". Continue your current work.'}]
> ```

## 🤖 Claude *(18:31:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"=== pkg tree ===\"; find packages/vision-mcp-core -type f -not -path '*/node_modules/*' -not -path '*/dist/*' | sort; echo \"\"; echo \"=== pkg package.json ===\"; cat packages/vision-mcp-core/package.json 2>/dev/null | head -60",
  "description": "Vision MCP core package file tree + package.json"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === pkg tree ===
> packages/vision-mcp-core/bun.lock
> packages/vision-mcp-core/Dockerfile
> packages/vision-mcp-core/package.json
> packages/vision-mcp-core/src/auth/credentials.ts
> packages/vision-mcp-core/src/auth/identity.ts
> packages/vision-mcp-core/src/infra/billing.ts
> packages/vision-mcp-core/src/infra/telemetry.ts
> packages/vision-mcp-core/src/mcp/server.ts
> packages/vision-mcp-core/src/safety/duty-of-care.ts
> packages/vision-mcp-core/src/safety/sentinel.ts
> packages/vision-mcp-core/src/__tests__/fatia2.test.ts
> packages/vision-mcp-core/src/__tests__/gates.test.ts
> packages/vision-mcp-core/src/tools/analyze-video.ts
> packages/vision-mcp-core/src/tools/consolidate-reference.ts
> packages/vision-mcp-core/src/tools/deepsearch-scrape.ts
> packages/vision-mcp-core/src/tools/describe-image.ts
> packages/vision-mcp-core/src/tools/mesh-search.ts
> packages/vision-mcp-core/tsconfig.json
> packages/vision-mcp-core/vitest.config.ts
> 
> === pkg package.json ===
> {
>   "name": "vision-mcp-core",
>   "version": "0.1.0",
>   "private": true,
>   "type": "module",
>   "description": "MCORCH Vision MCP — Fatia 1 skeleton: Streamable HTTP MCP server with ES256 JWKS identity, Origin gate, sentinel, and mesh.search (internal, read-only).",
>   "bin": {
>     "vision-mcp": "dist/mcp/server.js"
>   },
>   "scripts": {
>     "build": "tsc -p tsconfig.json",
>     "start": "node dist/mcp/server.js",
>     "dev": "bun run src/mcp/server.ts",
>     "test": "vitest run"
>   },
>   "dependencies": {
>     "@modelcontextprotocol/sdk": "^1.11.0",
>     "jose": "^5.9.6",
>     "zod": "^3.23.8"
>   },
>   "devDependencies": {
>     "typescript": "^5.5.0",
>     "vitest": "^2.0.0",
>     "@types/node": "^22.0.0"
>   }
> }
> ```

## 🤖 Claude *(18:31:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"=== FRD FR-VM-007 + \u00a74.5 (deepsearch async) ===\"; grep -n -i \"FR-VM-007\\|deepsearch\\|partial.delivery\\|job_id\\|\u00a74.5\\|4\\.5\\|async\\|poll\" docs/bok/vision-mcp/04-frd.md | head -60",
  "description": "Grep FRD for FR-VM-007 + async/poll/partial-refund refs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === FRD FR-VM-007 + §4.5 (deepsearch async) ===
> 7:**Source of Truth:** `docs/bok/vision-mcp/00-deepsearch-blueprint.md` (v0.2.0) + `01-mrd.md` (MR-VM-001..016) + `02-brd.md` (BR-VM-001..012) + `03-prd.md` (PR-VM-001..025) — todo FR-VM deste documento rastreia ≥1 PR-VM; IDs do blueprint (FM-VM-01..18, OTD-VM-001..019) preservados verbatim; ambiguidades viram OTD, nunca improvisação.  
> 17:**In scope:** servidor MCP soberano de percepção visual + deepsearch fundamentado em container `mcorch_vision_mcp` (Sovereign Mesh, precedente gitnexus) — transporte Streamable HTTP 2025-11-25; identidade ES256 JWKS fail-closed + OAuth 2.1/RFC 9728 + PAT `mcp_access_tokens`; resolução de credencial per-user fail-closed (coluna `user_api_keys.firecrawl_api_key`); sentinel duplo (inbound + texto extraído); superfície de tools com classes mcoCoin (débito atômico + refund-on-failure + **regra de partial-delivery refund selada neste documento**, §4.5); Mesh Connection Mandate com dois regimes de persistência; erasure LGPD em cascata + retention clock; gate periférico Tier 1 com alvo de recall; distribuição Plugin Zip + skills + MCP Registry; expansão assistiva (`vision.alt_text`/`vision.describe_screen` + duty-of-care) e cognitiva (resources/prompts) gated.
> 43:| FR-VM-006 | Tool surface billable (classes mcoCoin) | Registro de tools com classe mco por tool (BRD §6: describe_image 2, ocr 1/página, scrape 1, run 3, poll 0, mesh.search 0–1, consolidate_reference 1, alt_text/describe_screen 2, peripheral_scan 0–1, track 1, detect 2, segment 2/5, video 2/min). Débito **na entrada** via `deduct_mco_coins(p_user_id, p_amount, p_action, p_context)` (PostgREST + secret name `SB_SECRET_KEY`) contra `sub` verificado; saldo insuficiente → **402** antes de qualquer leg de provider. `refundMco` em TODA falha billable (credit service-role-only, nunca lança). Metering por leg em `agent_executions`; **BYOK anda de graça** (`isUserCustomKey → cost 0`); exempção `SOVEREIGN_USER_ID`. Classes espelhadas em `src/lib/billing.ts → COIN_COSTS` + constante hardcoded no serviço + asserção em `src/test/billing.test.ts`; fix de preço só após medição material do $ (OTD-VM-004) | Critical | PR-VM-008 | Container service + DB | AT-VM-006 |
> 44:| FR-VM-007 | Async job semantics + partial-delivery refund | `deepsearch.run` → débito integral na entrada → retorna `job_id` imediato (p95 <2s) + progress notifications quando o host suporta; `deepsearch.poll(job_id)` custo 0 entrega estado/resultado (tools-only hosts — OTD-VM-003). Máquina de estados `queued→running→done|partial|failed`; jobs tenant-scoped (poll exige mesma identidade verificada); resultado disponível p/ poll ≥24h pós-terminal; nunca chamada bloqueante. **Regra de partial-delivery refund selada em §4.5** (FM-VM-07): 0 unidades entregues → refund integral; entrega parcial → cobrança proporcional arredondada A FAVOR do tenant, resultado com `partial:true` | Critical | PR-VM-013 | Container service | AT-VM-007 |
> 53:| FR-VM-020 | `deepsearch.scrape` | Scrape de 1 URL pública via Firecrawl BYOK (fail-closed FR-VM-004), logged-out only. Gates: robots.txt honrado, login-wall block, allowlist de fontes permissivas, CDSM Art. 4 opt-out. Saída markdown + metadata de proveniência/licença. Classe 1 mco | Critical | PR-VM-006 | Container service | AT-VM-020 |
> 54:| FR-VM-021 | `mesh.consolidate_reference` | Grava referência consolidada (saída de visão fundamentada por deepsearch) como nó `observation` + `content_mesh_asset` (template `orchestrate-step`): PII-strip antes do insert, tag `scraped` + proveniência/licença/`retention_until`, `metadata.cost_mco`, BR/FR ID de traceabilidade, embed-on-insert grátis via `embed-mcorch-node`. **NUNCA em system nodes** (`user_id IS NULL`). Edge ao nó do run instrumenta o gate do cruzado (KPI-VM-003). Classe 1 mco | Critical | PR-VM-010 | Container service + DB | AT-VM-021 |
> 76:| FR-VM-022 | BYOK Settings card | Card Vision/Deepsearch em `/dashboard/settings` estendendo `useUserApiKeys` com `firecrawl_api_key`. `user_api_keys` é VIEW mascarada → write via `.insert` (NUNCA `.upsert`); null não limpa (clear via RPC); teste de chave server-side (cliente só vê máscara). Estados: conectado / não-configurado + CTA / erro com mensagem PT-BR acionável | Critical | PR-VM-007 | UI + Hook + DB | AT-VM-022 |
> 104:| NFR-VM-003 | Performance (async) | `deepsearch.run` submit→`job_id`; SSE heartbeat anti-idle Cloudflare (~100s — OTD-VM-013); resultado poll-able pós-terminal | submit p95 < 2s; heartbeat ≤ 25s; retenção ≥ 24h | Teste de job >150s + curl do poll |
> 108:| NFR-VM-007 | Security (identity) | 100% das requests com identidade verificada (ES256 JWKS ou PAT hash) ANTES de qualquer efeito; Origin 403; fail-closed se JWKS inalcançável; `SB_SECRET_KEY` jamais em path client-reachable; migrations (`mcp_access_tokens`, `firecrawl_api_key`, `erase_vision_artifacts`) passam `/security-review` | 100% / SAFE | `/security-review` + smoke 401/403 |
> 170:#### `deepsearch.run` / `deepsearch.poll` (FR-VM-007 · 3 / 0 mco)
> 172:**Output run:** `{ job_id: string, state: 'queued', planned_units: number, charged_mco: number }`  
> 173:**Output poll:** `{ job_id, state: 'queued'|'running'|'done'|'partial'|'failed', delivered_units, planned_units, partial: boolean, failed_units?: string[], refunded_mco?: number, result?: {...} }`
> 194:| 404 | `job_not_found` | `job_id` inexistente ou de outro tenant |
> 199:### 4.5 Async Job & Partial-Delivery Refund Contract (sela FM-VM-07 / BR-VM-003 / BAC-VM-007)
> 203:1. **Débito integral na entrada:** `deepsearch.run` debita a classe inteira (3 mco) via `deduct_mco_coins` antes do enqueue. Saldo insuficiente → 402, job não nasce.
> 207:5. **Transparência:** resultado parcial entregue com `partial: true` + `failed_units[]` + `refunded_mco` explícito no payload do poll.
> 208:6. **Idempotência:** refund por job é executado no máximo uma vez (guard por `job_id` no contexto do RPC); retries de poll nunca re-disparam refund.
> 233:| `planned_units` (`deepsearch.run`) | `int` | NOT NULL (default 1) | 1 ≤ N ≤ cap do plano (valor selado no SDD) | "Número de unidades do job fora do limite" |
> 234:| `job_id` | `uuid` | NOT NULL (`poll`) | UUID v4 existente e pertencente ao tenant | "Job não encontrado" |
> 256:| FR-VM-007 | ✅ Required | ✅ Required | ✅ Required | Job >150s via poll; refund parcial bate §4.5 (floor a favor do tenant); idempotência |
> 293:| PR-VM-002 | FR-VM-002 | NFR-VM-007 |
> 298:| PR-VM-007 | FR-VM-004, FR-VM-022 | NFR-VM-006, NFR-VM-007 |
> 300:| PR-VM-009 | FR-VM-005 | NFR-VM-007, NFR-VM-010 |
> 302:| PR-VM-011 | FR-VM-001, FR-VM-002 | NFR-VM-003, NFR-VM-007, NFR-VM-013 |
> 303:| PR-VM-012 | FR-VM-003 | NFR-VM-007 |
> 304:| PR-VM-013 | FR-VM-007 | NFR-VM-003, NFR-VM-008 |
> ```

## 🤖 Claude *(18:33:08)*


## 🤖 Claude *(18:33:09)*

FRD §4.5 is the sealed async/refund contract. Now I'll fan out a grounded **mapping** workflow — 5 parallel readers over the BoK contract, the persistence/schema reality (live DB), the code wiring, the provider semantics, and the migration patterns — so the design rests on what's actually sealed and what's actually deployed, not assumptions.

## 🤖 Claude *(18:34:07)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'vision-deepsearch-run-map',\n  description: 'Map the sealed contract + live schema + code wiring for building deepsearch.run async (FR-VM-007) + the two menores',\n  phases: [{ title: 'Map' }],\n}\n\nconst REPO = '/home/gcrUX/htdocs/constellation-orchestra'\n\nconst MAP_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  required: ['summary', 'findings', 'open_questions'],\n  properties: {\n    summary: { type: 'string', description: '3-6 sentence synthesis of this subsystem as it pertains to building deepsearch.run async + menores' },\n    findings: {\n      type: 'array',\n      items: {\n        type: 'object',\n        additionalProperties: false,\n        required: ['topic', 'detail', 'source'],\n        properties: {\n          topic: { type: 'string' },\n          detail: { type: 'string', description: 'Concrete fact, signature, schema, or verbatim contract clause \u2014 be exact, quote where it matters' },\n          source: { type: 'string', description: 'file:line or live-query result that backs this (Lei 1 \u2014 material)' },\n        },\n      },\n    },\n    open_questions: {\n      type: 'array',\n      description: 'Ambiguities that are NOT resolved by the sealed BoK \u2014 candidate OTDs, never to be improvised',\n      items: { type: 'string' },\n    },\n  },\n}\n\nphase('Map')\n\nconst READERS = [\n  {\n    label: 'R1:async-contract',\n    prompt: `You are mapping the SEALED async-job + partial-refund contract for the MCORCH Vision MCP tool \\`deepsearch.run\\` / \\`deepsearch.poll\\` (FR-VM-007).\n\nRead these EXACTLY (do not skim):\n- ${REPO}/docs/bok/vision-mcp/04-frd.md \u2014 focus on: FR-VM-007 row (~line 44); the \\`deepsearch.run / deepsearch.poll\\` tool spec block (~lines 168-200) with its Output run/poll shapes + error codes table; \u00a74.5 \"Async Job & Partial-Delivery Refund Contract\" (~lines 199-210); the data dictionary rows for \\`planned_units\\` and \\`job_id\\` (~lines 230-235); NFR-VM-003 (performance/async, ~line 104) and AT-VM-007 acceptance test (~line 256).\n\nExtract VERBATIM where it matters:\n1. The exact \\`deepsearch.run\\` output shape and \\`deepsearch.poll\\` output shape (every field + type).\n2. The full state machine (queued\u2192running\u2192done|partial|failed) and any transition rules.\n3. The complete error-code table for these tools (status, code, when).\n4. The partial-delivery refund rule from \u00a74.5 \u2014 all 6 (or N) numbered clauses verbatim, especially: full-debit-on-entry, 0-units\u2192full refund, partial\u2192proportional rounded IN FAVOR of tenant, partial:true + failed_units + refunded_mco in payload, refund idempotency guard by job_id.\n5. \\`planned_units\\` validation bounds (and where the cap value is \"selado no SDD\").\n6. The mcoCoin classes: run=3, poll=0 \u2014 confirm from FR-VM-006 (~line 43) and BRD \u00a76.\n7. Retention requirement (\u226524h post-terminal) and the SSE heartbeat anti-idle requirement (OTD-VM-013, ~25s / ~100s Cloudflare).\n\nReturn the structured map. open_questions = anything the contract leaves genuinely undefined.`,\n  },\n  {\n    label: 'R2:schema-reality',\n    prompt: `You are mapping the PERSISTENCE & SCHEMA REALITY for building \\`deepsearch.run\\` async in the MCORCH Vision MCP, plus the \\`infra_health_logs metadata jsonb\\` menor.\n\n(A) Read the sealed design docs:\n- ${REPO}/docs/bok/vision-mcp/06-data-model.md \u2014 does it define a jobs table (e.g. \\`vision_jobs\\`, \\`deepsearch_jobs\\`)? What columns/constraints/RLS? Also note \\`mcp_access_tokens\\` and \\`erase_vision_artifacts\\` definitions if present (Fatia 3 scope markers).\n- ${REPO}/docs/bok/vision-mcp/05-sdd.md \u2014 find: (i) the SEALED \\`planned_units\\` cap value; (ii) the async architecture decision \u2014 is job state held IN-MEMORY in the container or in a DB table? SSE heartbeat design; retention; how poll resolves; any worker/queue design. Quote the relevant SDD passages.\n- ${REPO}/docs/bok/vision-mcp/07-process-flow.md \u2014 the deepsearch.run lifecycle / sequence if present.\n\n(B) Probe the LIVE deployed DB (Lei 1 \u2014 material). Supabase REST base: https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1 . The service key is in the repo .env as SB_SECRET_KEY (run \\`cd ${REPO} && set -a && . ./.env && set +a\\` then use \\`$SB_SECRET_KEY\\` as both apikey and Bearer). Determine MATERIALLY:\n  1. Does a vision_jobs / deepsearch_jobs table exist? (GET \\`/<table>?limit=1\\` \u2192 200 = exists, PGRST205/404 = absent). Try the names you found in 06-data-model.\n  2. \\`infra_health_logs\\` \u2014 does it currently have a \\`metadata\\` column? GET \\`/infra_health_logs?select=*&limit=1\\` and list the JSON keys of the returned row; if empty, say so and fall back to declared columns from the migration files in ${REPO}/supabase/migrations/ (grep for infra_health_logs CREATE TABLE / ALTER).\n  3. Confirm \\`deduct_mco_coins\\` and any \\`add_mco_coins\\`/refund RPC exist (the billing foundation already proven in Fatia 2).\n\nReturn the structured map. open_questions = schema decisions not yet sealed (e.g. \"is the job table deferred to Fatia 3 or built now?\").`,\n  },\n  {\n    label: 'R3:code-wiring',\n    prompt: `You are mapping the EXISTING CODE WIRING in packages/vision-mcp-core so a new tool \\`deepsearch.run\\`/\\`deepsearch.poll\\` follows the EXACT established pattern (no reinvention).\n\nRead fully:\n- ${REPO}/packages/vision-mcp-core/src/mcp/server.ts \u2014 how tools are registered (the McpServer fresh-per-request pattern from the Fatia 1 handshake fix); the HTTP gate order (Origin\u2192protocol\u2192ES256 JWKS\u2192ALS sub); how a tool handler receives the verified \\`sub\\`; the list of currently registered tools.\n- ${REPO}/packages/vision-mcp-core/src/tools/deepsearch-scrape.ts \u2014 the CLOSEST sibling. Map its full structure: sentinel call, resolveProviderKey, costFor, deductOnEntry, provider leg, refund-on-failure, telemetry. This is the template deepsearch.run must mirror.\n- ${REPO}/packages/vision-mcp-core/src/infra/billing.ts \u2014 exact signatures of deductOnEntry / refundMco / costFor (and any COIN class table / how 'deepsearch.run'=3, 'deepsearch.poll'=0 would be added).\n- ${REPO}/packages/vision-mcp-core/src/auth/credentials.ts \u2014 resolveProviderKey signature; which providers it supports today; does it already know 'google'/'gemini' (analyze-video uses Gemini \u2014 see tools/analyze-video.ts briefly)?\n- ${REPO}/packages/vision-mcp-core/src/infra/telemetry.ts \u2014 the telemetry helper signature + what fields it writes to infra_health_logs (relevant to the metadata jsonb menor).\n- ${REPO}/packages/vision-mcp-core/src/tools/analyze-video.ts \u2014 ONLY to extract how it calls Gemini (endpoint, auth, request shape) since deepsearch.run is the \"google/gemini\" research half.\n\nReturn the structured map with EXACT function signatures (copy them verbatim) and the canonical per-request tool pipeline. open_questions = wiring gaps a new async tool exposes (e.g. \"no job store exists in-process today\").`,\n  },\n  {\n    label: 'R4:provider-semantics',\n    prompt: `You are determining WHAT \\`deepsearch.run\\` actually DOES \u2014 the \"google/gemini grounded research half\" of the Vision MCP deepsearch surface (distinct from \\`deepsearch.scrape\\` which is Firecrawl single-URL). Be rigorous: report only what the sealed BoK specifies; flag everything underspecified as a candidate OTD (Lei 2 \u2014 never improvise).\n\nRead:\n- ${REPO}/docs/bok/vision-mcp/00-deepsearch-blueprint.md \u2014 the \"Cognitive\"/deepsearch pillar; what grounded research means here; any provider named (Gemini grounding / Google Search grounding / google CSE).\n- ${REPO}/docs/bok/vision-mcp/03-prd.md \u2014 PR-VM-013 (and neighbors) for the deepsearch.run product behavior.\n- ${REPO}/docs/bok/vision-mcp/01-mrd.md \u2014 the market/job-to-be-done for deepsearch.run.\n- ${REPO}/docs/bok/vision-mcp/04-frd.md \u2014 re-read FR-VM-007 + the tool spec for what a \"unit\" is (planned_units) and the result shape.\n- Cross-check how the EXISTING repo does grounded deep research: ${REPO}/docs/processes/deepsearch-blueprint.md and any deep-research skill, to see what \"units\" naturally map to (search fronts? sources? sub-queries?).\n\nDetermine, with sources:\n1. The provider + API for the grounded-research leg (Gemini with Google Search grounding? raw Google API? Is the key 'gemini_api_key' per-user \u2014 confirm it's a column in user_api_keys).\n2. What ONE \\`unit\\` is (so planned_units + partial-delivery has concrete meaning).\n3. The result payload contents (citations? synthesized report? per the FRD poll \\`result\\` field).\n4. How partial delivery physically happens (some units fail \u2192 partial).\n\nReturn the structured map. open_questions = every place the provider/unit/result is NOT pinned by the BoK (these become OTDs for the design, not guesses).`,\n  },\n  {\n    label: 'R5:migration-and-menores',\n    prompt: `You are mapping MIGRATION MECHANICS for this session: (a) a possible \\`vision_jobs\\` table for deepsearch.run, (b) the \\`infra_health_logs ADD metadata jsonb\\` menor, and (c) WHERE to register the OTD orphan-sub menor in the BoK.\n\nRead:\n- ${REPO}/supabase/migrations/ \u2014 find the Fatia 2 firecrawl_api_key Vault migration (grep \\`firecrawl_api_key\\`) and read it fully: it is the canonical recent pattern (RLS, search_path='', GRANT/REVOKE, encrypted-view triggers). Also find the canonical CREATE TABLE migration for a tenant-scoped table with RLS default-deny + the composite-FK tenant-scope pattern (e.g. the marketing-hub leads migration, or campaign_steps) to mirror for vision_jobs.\n- grep the migrations for \\`infra_health_logs\\` \u2014 find its CREATE TABLE and current columns; determine the exact ALTER to add \\`metadata jsonb\\` safely (nullable default '{}'::jsonb, or NULL). Check whether any RLS/grant must change.\n- ${REPO}/docs/processes/vision-mcp-cost-calibration.md \u2014 note the OTD-VM-004 SOP style.\n- ${REPO}/docs/bok/vision-mcp/02-brd.md AND 00-deepsearch-blueprint.md \u2014 find the OTD ledger (OTD-VM-001..020/022). Identify the EXACT file + section where a new \"OTD-VM-orphan-sub\" (residual LOW risk: a verified \\`sub\\` that no longer maps to a live profile) should be registered as an amendment, and what the existing OTD rows look like (format to mirror).\n- ${REPO}/CLAUDE.md \"Every new migration MUST pass /security-review before commit\" \u2014 note this gate.\n\nReturn the structured map: (1) exact ALTER for infra_health_logs metadata; (2) a vision_jobs CREATE TABLE skeleton matching the repo's RLS/tenant-scope conventions (columns from FR-VM-007 data dict: id uuid, user_id, state, planned_units, delivered_units, charged_mco, refunded_mco, partial bool, result jsonb, failed_units, timestamps, retention_until); (3) the exact BoK location + row format for the OTD orphan-sub amendment. open_questions = anything blocking a clean migration.`,\n  },\n]\n\nconst maps = await parallel(\n  READERS.map((r) => () => agent(r.prompt, { label: r.label, phase: 'Map', schema: MAP_SCHEMA }))\n)\n\nreturn READERS.map((r, i) => ({ reader: r.label, map: maps[i] }))\n"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wynxmg0hh
> Summary: Map the sealed contract + live schema + code wiring for building deepsearch.run async (FR-VM-007) + the two menores
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/dfc038c3-0ab3-428f-80e3-e30dca27edaa/subagents/workflows/wf_3e45dc82-e96
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/dfc038c3-0ab3-428f-80e3-e30dca27edaa/workflows/scripts/vision-deepsearch-run-map-wf_3e45dc82-e96.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/dfc038c3-0ab3-428f-80e3-e30dca27edaa/workflows/scripts/vision-deepsearch-run-map-wf_3e45dc82-e96.js"} to iterate without resending the script.)
> Run ID: wf_3e45dc82-e96
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/dfc038c3-0ab3-428f-80e3-e30dca27edaa/workflows/scripts/vision-deepsearch-run-map-wf_3e45dc82-e96.js", resumeFromRunId: "wf_3e45dc82-e96"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(18:34:16)*


## 🤖 Claude *(18:34:23)*

Workflow `wf_3e45dc82-e96` (5 readers) está rodando em background — vou ser reinvocado quando concluir. Ele mapeia, em paralelo e com prova material:

1. **R1** — contrato selado (§4.5 refund parcial + state machine + shapes I/O + error codes)
2. **R2** — realidade do schema (existe tabela de jobs? `infra_health_logs` já tem `metadata`? RPCs de billing) — query LIVE no DB
3. **R3** — wiring do código existente (assinaturas exatas de `deductOnEntry`/`refundMco`/`resolveProviderKey` + o template `deepsearch.scrape`)
4. **R4** — semântica do provider (o que `deepsearch.run` faz de fato: Gemini grounding? o que é uma "unit"? como a entrega parcial acontece) — flag de OTD para o que não estiver pinado
5. **R5** — mecânica das migrations (ALTER do `metadata jsonb` + skeleton `vision_jobs` + onde registrar a OTD orphan-sub na BoK)

Aguardando a síntese para travar o design antes de escrever qualquer linha (Lei 2 — sem improvisar além do que a BoK sela). Acompanhe em `/workflows`.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-15 - Build trading dashboard with AI strategy validation]]
> * **Próxima Sessão**: [[2026-06-15 - agent-a0075c7d26db1bb8b]]
%% --- TIMELINE END --- %%

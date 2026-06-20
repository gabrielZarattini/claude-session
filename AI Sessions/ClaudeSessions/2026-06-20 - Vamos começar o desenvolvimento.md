# Vamos começar o desenvolvimento
**Date:** 2026-06-20 | **Session ID:** `034e4fdb-b4b4-4ef6-bae7-10d32bd4551c`

---

## 👤 User *(17:11:52)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(17:11:52)*

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


## 🤖 Claude *(17:11:58)*


## 🤖 Claude *(17:11:58)*

I'll execute the ShakeHands /handson ritual. Starting with all pre-flight checks in parallel.

## 🤖 Claude *(17:11:59)*


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
> 44e5887 chore(sprint): registra v6.43.0 — Viral Autopilot Fatias 1 + 1b + diagnóstico saída visível
> 7e6fcd5 docs(handoff): seal Viral Autopilot Fatias 1 + 1b — product-aware + monetização cross-surface + imagem + diagnóstico saída visível
> 0f24ce3 docs(readme): v6.43.0 — Viral Autopilot Fatias 1 + 1b (product-aware + monetização cross-surface + imagem) + diagnóstico saída visível
> 803f946 fix(generate-image): OpenAI image endpoint rejeita response_format + trata url/b64
> ba5d281 feat: Viral Autopilot Fatia 1b — imagem product-referenced no pipeline (FR-VA-013)
> 4af8b8b feat: Viral Autopilot Fatia 1 — gerador product-aware + monetização cross-surface
> a8f14a3 chore(sprint): registra v6.42.0 — Viral Autopilot BoK 9/9 (motor de conteúdo viral autônomo)
> ```

## 🤖 Claude *(17:11:59)*


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

## 🤖 Claude *(17:12:00)*


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

## 🤖 Claude *(17:12:01)*


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

## 🤖 Claude *(17:12:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\"; echo \"---\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\"; echo \"--- chroma ---\"; curl -s http://localhost:8001/api/v2/heartbeat",
  "description": "Docker mesh + Chroma health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> mcorch_vision_mcp: Up 3 days (healthy)
> mcorch_claude_mem: Up 5 days (healthy)
> mcorch_chroma: Up 5 days (healthy)
> ---
> mega-brain-dashboard: Up 5 days
> mega-brain-webhook: Up 5 days (healthy)
> mega-brain-daemon: Up 5 days (healthy)
> --- chroma ---
> {"nanosecond heartbeat":1781975522902503639}
> ```

## 🤖 Claude *(17:12:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/ 2>/dev/null; echo \"--- scratch ---\"; ls scratch/ 2>/dev/null && echo \"scratch has files\" || echo \"scratch clean\"; echo \"--- handoff lines ---\"; wc -l HANDOFF.md",
  "description": "BoK suites, scratch, HANDOFF line count"
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
> viral-autopilot
> viral-daily-canvas
> viralmind
> vision-mcp
> --- scratch ---
> scratch has files
> --- handoff lines ---
> 8095 HANDOFF.md
> ```

## 🤖 Claude *(17:12:05)*


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
> 14	## Session Seal — Viral Autopilot Fatias 1 + 1b: gerador product-aware + monetização cross-surface + imagem (FR-VA-003/004/009/012/013/016) (2026-06-20)
> 15	
> 16	`/handson` → diretiva "vamos aos próximos passos" sobre o roadmap do Viral Autopilot (BoK gate ABERTO). Arco Closed-Loop por fatia: **mapeamento (workflow) → escopo cravado → SOP Lei 2 → código → /security-review → deploy → E2E pago material → seal**. Três fatias de trabalho numa sessão, todas provadas em produção; nenhuma improvisação além do BoK + correções materiais declaradas honestamente.
> 17	
> 18	**O que foi entregue:**
> 19	1. **Fatia 1 (commit `4af8b8b`) — gerador product-aware + monetização cross-surface.** Workflow de mapeamento (6 readers BoK + 5 readers código) cravou o escopo. **FR-VA-003:** prompts virais de consumo featuring o produto escolhido (artigo/LinkedIn/X); fallback B2B quando sem produto (backward-compat — campaign-run/intent-execute intactos). **FR-VA-004:** `monetizeForProduct` (`_shared/affiliate.ts`) monetiza as 3 superfícies determinístico por produto; grava `affiliate_links.content_id = content_library.id` (ANTES sempre null — defeito-núcleo FECHADO). **FR-VA-016 (metade-produto):** orchestrate-content resolve `product_ids` do catálogo (authoritative), sanitiza cada nome pelo Cyber-Sentinel (Apify = dado externo, fail-closed por produto), grava em `pipeline_runs.metadata.products`. **FR-VA-009:** nova migration `creative_metrics` (`20260619140000`, RLS SELECT-own + service-role-write default-deny + RESTRICTIVE no-delete + UNIQUE(content_variant_id,source) + 5 CHECKs; cycle_id reservado NULL p/ a fatia do cron). **UI:** picker de produtos na TriggerNode substitui o input de URL livre dropado.
> 20	2. **Fatia 1b (commit `ba5d281`) — imagem product-referenced (FR-VA-013).** Workflow de mapeamento (4 readers) cravou a fiação. `generate-image` ganhou **dual-path auth** (service-role + `user_id` no body, espelha publish-wordpress) + retorna o `path` durável do storage. orchestrate-step: bloco de imagem DENTRO do article_generation (não novo step na ladder — evita drift), gated `hasProducts`, **FAIL-OPEN com status `skipped`** (não `error` — senão o finalize marcaria o run error), guarda PATH em `content_library.media_url` (bucket privado → re-assina na leitura). Sem migration, sem mudança de frontend, **sem cobrança extra** (imagem já no bundle de 10).
> 21	3. **fix(generate-image) (commit `803f946`) — bug universal `response_format`.** OpenAI removeu o parâmetro do endpoint de imagens (400 "Unknown parameter"); removido + tratamento url/b64/data-URI (baixa bytes da url) + surfacing do `upstream` error.
> 22	4. **Diagnóstico cravado da saída visível** (Sovereign pediu "destravar"): **WP publish = Cloudflare bot-challenge** no `/wp-json` (403 "Just a moment...", mesmo autenticado — creds OK; ação: regra WAF Skip como no `mcp.mcorch.com`); **imagem nanobana = `api.nanobana.com` não resolve DNS** (endpoint morto); **imagem openai = chave-projeto `proj_rWo9…` sem acesso a NENHUM modelo de imagem** (chave válida `/v1/models`→200; ação: habilitar model access no OpenAI dashboard).
> 23	
> 24	**Correções materiais ao contrato BoK (declaradas):** imagem é DALL·E text-only (sem image-to-image) → product-referenced = prompt descritivo, não o image_url como referência visual (deferido); generate-image precisou do dual-path auth (orchestrate-step roda com service-key). Anexo de imagem no publish-layer (LinkedIn/X/Meta/WP featured) = fatias seguintes.
> 25	
> 26	**ORO:** Operator=MCORCH Master Execution Agent · Reviewer=Sovereign (4 decisões via AskUserQuestion: ship Fatia 1 · próxima fatia=1b · destravar=diagnóstico · selar) + `/security-review` independente (SAFE em ambas as fatias) · Owner=Sovereign (blast radius = comportamento de geração + carteira do tenant + links/conteúdo publicados).
> 27	
> 28	| Verificação (material) | Resultado |
> 29	|---|---|
> 30	| Migration `creative_metrics` | ✅ aplicada (`db push` exit 0) + verificada (RLS on · 2 policies · UNIQUE + 5 CHECKs via Management API) |
> 31	| Edge fns deployadas | ✅ orchestrate-content 113.8kB · orchestrate-step 130.9kB · generate-image 127.2kB |
> 32	| Frontend (nginx) | ✅ buildado (exit 0); picker no chunk servido; input antigo removido |
> 33	| E2E Fatia 1 (`158ba7fc`) | ✅ 3 criativos product-aware · 3/3 `affiliate_links.content_id` NON-NULL casando content_library.id · 3 creative_metrics · delta saldo 10 |
> 34	| E2E Fatia 1b (`46a98963`) | ✅ step `image_generation` `skipped` (fail-open) · `article_generation` `done` · run não-errado pela imagem · 3/3 content_id NON-NULL (zero regressão) · delta 10 |
> 35	| Auth generate-image (direto) | ✅ 400 sem user_id · 401 não-service · alcança provider |
> 36	| UI ocular | ✅ TriggerNode com PRODUTOS (3 SKUs) @ 1920×1080 (preview local + sessão injetada) |
> 37	| `/security-review` | ✅ SAFE (Fatia 1) · SAFE 9/10 (Fatia 1b dual-path) |
> 38	| tsc · suíte | ✅ 0 erros · 295 passed |
> 39	| Commits | `4af8b8b` · `ba5d281` · `803f946` · `0f24ce3` (readme) · (handoff) |
> 40	
> 41	### Survival Laws Self-audit
> 42	```
> 43	Law 1 (Materiality): ✅ Toda claim provada por output verificado NESTE turno — migration via Management API real, E2E via SELECT real (content_id NON-NULL, delta saldo), auth via curl 400/401, UI via screenshot ocular. Diagnóstico dos blockers cravado por status/headers reais (CF challenge, DNS fail, OpenAI model access) — não a mensagem genérica. NÃO fabriquei imagem visível: declarei honestamente que os providers do tenant estão quebrados (config, não código). Fase 5c a executar abaixo.
> 44	Law 2 (Process): ✅ SOP `viral-autopilot-product-aware-monetization.md` (+ addendum imagem) ANTES do código. Mapeamento (workflow) ANTES de codar cada fatia pegou correções materiais (imagem text-only, dual-path auth, response_format). generate-image=bug-fix (exempt do BoK gate).
> 45	Law 3 (Pruning): ✅ Sessão longa empacotada (3 fatias + diagnóstico) sob GO explícito do Sovereign por fatia; outputs de workflow referenciados por path, não recarregados; não selei cedo (calibração 1M).
> 46	Law 4 (ORO): ✅ Triplet declarado; 4 decisões de escopo pelo Sovereign (AskUserQuestion); /security-review independente como Reviewer mecânico em cada fatia.
> 47	```
> 48	
> 49	## Session Seal — Viral Autopilot BoK 9/9: motor de conteúdo viral autônomo monetizado por afiliado ML (R1-R4) (2026-06-17)
> 50	
> 51	`/handson` → diretiva do Sovereign de **retomar o objetivo-núcleo de receita**: alimentar contas de redes sociais com conteúdo viral gerado automaticamente e agendado (tudo de uma vez OU a cada N dias), que a cada ciclo analisa o desempenho anterior para melhorar os próximos criativos — monetizado com afiliado do Mercado Livre. Arco Closed-Loop respeitado de ponta a ponta: **auditoria material → 4 decisões soberanas → BoK 9/9 → validação adversarial → seal**. Nenhum código de produto foi escrito (BoK-only); o BoK Gate está agora ABERTO.
> 52	
> 53	**O que foi entregue:**
> 54	1. **Auditoria material (workflow 7 agentes, prova path:linha):** o pipeline existente é um gerador de blog/social B2B genérico com receita ML madura — **R1/R4 parciais e vivos** (`orchestrate-content`→`orchestrate-step` gera texto; `affiliate_config`/click-ledger/`handle-ml-postback` per-user provados), mas **R2 (recorrência a cada 3 dias) e R3 (loop auto-melhorável) AUSENTES**: `campaign_metrics` sem writer, `optimization_policy` nunca lida por gerador, `self-optimize` sem cron; monetização só no artigo (3 SKUs hardcoded por regex), `affiliate_url` da UI dropado, `fetch-trends` desconectado.
> 55	2. **4 decisões soberanas (AskUserQuestion):** suite-mãe NOVO `viral-autopilot` (não emenda nem override) · MVP texto+imagem nas redes atuais (WP/LinkedIn/X; vídeo+TikTok/IG/YT fase 2) · sinal R3 **combo** (cliques afiliado + engajamento orgânico + receita postback) · 3 SKUs semente (Roborock S8 / Samsung Neo QLED 8K / Family Hub).
> 56	3. **BoK 9/9 selada (1889 LOC)** em `docs/bok/viral-autopilot/` (MR/BR-VA-001..008 · PR-VA-001..022 · **FR-VA-001..021** · 8 NFR · 8 OTD · 12 FMEA com 4 RPN>100). Unifica R1-R4 e é dona explícita do orquestrador do ciclo.
> 57	4. **Validação Fase 6 — 4 rodadas adversariais** (workflow 4 críticos/rodada) + grep determinístico: R1 NO_GO (2 blockers+7 high) → R2 NO_GO (2 blockers, **1 que eu introduzi**: refund por `deduct` negativo viola o RPC anti-mint `20260603220000:45`) → R3 GO_WITH_FIXES → R4 GO_WITH_FIXES (síntese caiu por session-limit; críticos OK). Pegou um **buraco de segurança real**: cron `verify_jwt=false` confiava no header `x-autopilot-user-id` sem provar service-role in-function → drenaria saldo de vítima.
> 58	5. **Design final cravado pela validação:** cron prova service-role in-function (`Bearer SB_SECRET_KEY`, padrão `orchestrate-step:50-53`) ANTES de confiar no header · RPCs `begin_autopilot_cycle` (advisory-lock anti-TOCTOU do cap diário + pré-débito atômico) + `finalize_autopilot_cycle` (refund **crédito positivo** via `add_mco_coins` ledgered) · `N_runs = produtos×redes×ab_variants` (imagem no bundle de 10) · FK COMPOSTA tenant-escopada · `campaign_metrics` deprecada → `creative_metrics` canônica · `optimization_policy` com `scope='viral_autopilot:<plan_id>'`.
> 59	
> 60	**ORO:** Operator=MCORCH Master Execution Agent · Reviewer=Sovereign (4 decisões via AskUserQuestion + GO de seal) + 4 rodadas de validação adversarial independente · Owner=Sovereign (blast radius = conteúdo autônomo publicado + gasto de carteira do tenant).
> 61	
> 62	| Verificação (material) | Resultado |
> 63	|---|---|
> 64	| BoK 9/9 selada | ✅ `docs/bok/viral-autopilot/` 9 docs · 1889 LOC (wc -l) |
> 65	| Seal node na malha | ✅ `documentation_suite` `b3398294-aa75-4810-845b-3a15cfe802e7` · embedding **NOT NULL 768d** |
> 66	| DERIVES_FROM edge | ✅ `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed` |
> 67	| Validação adversarial | ✅ 4 rodadas (9→4→4→2 high; 0 blocker desde R3) + grep determinístico limpo |
> 68	| tsc | ✅ zero erros |
> 69	| Commits | `8da7a58` (BoK suite+seed) · `2c56211` (readme) · (handoff) |
> 70	
> 71	### Survival Laws Self-audit
> ```

## 🤖 Claude *(17:12:05)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>[Truncated: PARTIAL view — showing lines 1-41 of 240 total (59618 tokens, cap 25000). Call Read with offset=42 limit=41 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>
> 
> 1	# 🧠 Sprint Priorities — Constellation Orchestra
> 2	
> 3	**Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 4	
> 5	**90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 6	
> 7	**Sprint v6.43.0 — Viral Autopilot Fatias 1 + 1b: gerador product-aware + monetização cross-surface + imagem (2026-06-20)** — `/handson` → "vamos aos próximos passos" sobre o roadmap do Viral Autopilot (BoK gate ABERTO). Closed-Loop por fatia (mapeamento workflow → escopo → SOP Lei 2 → código → /security-review → deploy → E2E pago → seal). **(1) Fatia 1** (`4af8b8b`): gerador product-aware (FR-VA-003, prompts virais featuring o produto escolhido; fallback B2B backward-compat) + monetização nas **3 superfícies** (FR-VA-004, `affiliate_links.content_id` antes-null **FECHADO**) + threading `product_ids` sanitizado pelo sentinel (FR-VA-016) + tabela `creative_metrics` (FR-VA-009, RLS provada) + picker na TriggerNode. **(2) Fatia 1b** (`ba5d281`): imagem product-referenced (FR-VA-013) DENTRO do article_generation, **fail-open** (`skipped`, nunca quebra a geração), PATH durável em `content_library.media_url`, dual-path auth na generate-image; sem migration/frontend/cobrança extra. **(3) fix generate-image** (`803f946`): bug universal `response_format` (OpenAI removeu o param) → removido + tratamento url/b64 + surfacing. **(4) Diagnóstico saída visível** (Sovereign pediu "destravar"): WP=Cloudflare challenge no /wp-json (ação: WAF Skip como mcp.mcorch.com), nanobana=DNS morto, openai=chave-projeto sem acesso a modelo de imagem (config OpenAI). **Prova:** 2 E2E pagos (`158ba7fc`/`46a98963`, delta 10 cada · 3/3 content_id NON-NULL · fail-open) · UI ocular 1920×1080 · /security-review SAFE 2× · tsc 0 · 295 testes · Phase 5c **SEAL ALLOWED** (10) · mesh **8934** · handoff `385d3dd5`. **Pending:** Fatia 2 cron/cadência R2 (SOP `autopilot-cron-identity.md` Lei 2/OTD-VA-008) · loop R3 · anexo imagem no publish-layer · **2 ações Sovereign** (CF WAF skip /wp-json + OpenAI image model access). **Lição:** mapear o contrato vivo ANTES de codar pegou 3 correções materiais (imagem text-only, dual-path auth, response_format); diagnóstico por status/headers reais cravou as causas; não fabriquei imagem visível (providers do tenant quebrados = config, declarado).
> 8	
> 9	**Sprint v6.42.0 — Viral Autopilot BoK 9/9: motor de conteúdo viral autônomo (R1-R4) (2026-06-17)** — `/handson` → diretiva Sovereign de **retomar o objetivo-núcleo de receita** (= o próprio Sprint Goal "distribuição social autônoma operacional"): alimentar redes com conteúdo viral auto-gerado/agendado (tudo de uma vez OU a cada N dias), que a cada ciclo analisa o anterior p/ melhorar os próximos criativos, monetizado c/ afiliado ML. Arco Closed-Loop puro (zero código de produto): **(1) Auditoria material** (workflow 7 agentes, prova path:linha) — R1/R4 parciais vivos, **R2 (recorrência) e R3 (loop auto-melhorável) AUSENTES** (`campaign_metrics` sem writer, `optimization_policy` nunca lida, `self-optimize` sem cron); **(2) 4 decisões soberanas** (AskUserQuestion: suite NOVO · MVP texto+imagem · sinal R3 combo · 3 SKUs); **(3) BoK 9/9** (1889 LOC, FR-VA-001..021, 12 FMEA 4×RPN>100); **(4) Validação Fase 6 em 4 rodadas adversariais** (4 críticos/rodada) + grep determinístico — pegou buraco de segurança real (cron `verify_jwt=false` sem prova service-role in-function) + anti-mint (refund por deduct negativo, que EU introduzi); **(5) seal** (node `b3398294` embedded 768d, DERIVES_FROM marketing-hub). **Prova:** tsc 0 · 3 commits pushed · Phase 5c **SEAL ALLOWED** (10) · mesh **8928** · handoff `496ec17c`. **BoK Gate ABERTO.** Pending: fatia 1 (product-aware + monetize, NÃO depende do cron) + SOP `autopilot-cron-identity.md` (Lei 2/OTD-VA-008) antes da cadência. **Lição:** verificação adversarial multi-rodada foi essencial — cada "fix" meu deixava um resíduo que a rodada seguinte pegava; não auto-declarar GO (Lei 1).
> 10	
> 11	**Sprint v6.41.0 — Unified Sensorial Canvas (Phase Epsilon V9): AGI→ASI ref + emenda BoK + Fases 3.1-3.4 (2026-06-17)** — `/handson` → conversa estratégica (Model Council; plugin `claude-code-setup`; paper *From AGI to ASI* DeepMind) → diretiva arquitetural **Unified Core Sensorial Canvas** (fundir Core-Fable + Matrix + Memória num canvas 3D R3F). Arco Closed-Loop: **(1) Fundamentação** — arXiv 2606.12683 (Legg/Hutter/Leibo) lido inteiro (57p) + selado como nó `architecture` `a576216e` (edge INFORMS→openclaw) + checklist Via 4 (`.claude/context/agi-asi-via4-design-checklist.md`); tese: o MCORCH é a Via 4 (group agent formation) instanciada na app layer. **(2) Auditoria de clusters (Lei 1)** — Louvain = REAL/VIVO (`useConstellationSigma.ts:227`, graphology client-side); squad-coloring = MORTO (`crew_module_ownership` 0 rows → fallback Louvain) + heurístico (`inferSquad`) → **Decisão B = PODAR** (Louvain oficial; OTD-SQUAD-OWNERSHIP-REVIVAL). **(3) Emenda BoK** (gate Sovereign-eleito sobre override) — `mcorch-constellation` +PR-025/FR-043..049/NFR-023-024/SDD §9 (reconciliação Sigma→R3F: graphology cérebro / R3F corpo). **(4) Fases 3.1-3.4** (R3F, commits granulares, 3 páginas legadas preservadas) — scaffold rota `/dashboard/universe`/store/shell 72-28 + Code Network InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop (memória corrigida: glow aditivo). **(5) E2E ocular** (preview local à prova de CF + sessão injetada) nos 3 modos — telemetria real (8.560 nós/8.816 arestas/~733 comun./159 pensamentos); "esfera órfã" desmistificada = **spinner de loading**. **Prova:** tsc 0 em cada fase · 9 commits pushed · Phase 5c **SEAL ALLOWED** (handoff `5225ff03` verificado) · mesh **8926**. **Restam (Pending):** 3.5 Sinapses (arestas REAIS de `mcorch_edges`) · 3.6 fly-to · 3.7 layout/perf (**OTD-UCANVAS-PERF** — query do código ~30s c/ 2 canvases) · 3.8 poda · 3.9 paridade+gate E2E 1920×1080 · 3.10 seal. **Lição:** auditar materialmente ANTES de codar (Louvain vivo vs squad morto) + emenda BoK ANTES da Fase 3 manteve o Closed-Loop; o E2E ocular pegou que a "esfera órfã" era o spinner — não fabriquei explicação (Lei 1).
> 12	
> 13	**Sprint v6.40.0 — Vision MCP Fatia 3 remainder: PAT UI + install Claude Code + Plugin/Registry + caps de custo (2026-06-17)** — `/handson` → Sovereign puxou as 3 frentes do roadmap ("continue"). Closed-Loop: mapeei o contrato BoK vivo (FR-VM-003/011 · DD-VM-003 · OTD-VM-024/025) antes de codar. **Entregue (até o limite NÃO-gated):** **(1) PAT UI (FR-VM-003)** — `useMcpTokens` gera PAT 100% client-side (CSPRNG 32B→SHA-256, só o hash persiste byte-idêntico ao verifier; plaintext uma vez), lista/revoga RLS-own; `McpConnectorsCard` em Settings→Connectors; `.mcp.json` wired (`Bearer ${VISION_MCP_PAT}`); types regen. **Install no Claude Code provado por handshake MCP+PAT REAL pela URL pública** (`initialize`+`tools/list`7+`mesh_search` tenant-scoped); **(2) Plugin Zip + MCP Registry (FR-VM-011)** — `packages/vision-mcp-plugin/`→`public/plugins/…zip` + 3 skills PT-BR; manifesto `server.json` `com.mcorch/vision-mcp` (schema oficial 2025-12-11, remote streamable-http) + runbook (publish **gated** no DNS TXT Sovereign); **(3) OTD-VM-024** — blueprint §8-A sela motor dual (Firecrawl scrape + Gemini grounding run, fundamentado ai.google.dev) → FECHADA; **(4) caps (DD-VM-003/OTD-VM-025)** — `deepsearch.run` cap per-plano 10/25/50 + diário 25/100/500 (BYOK bypassa, fail-open em count error, throw antes do deduct); `validation_failed` ganha field+message (FRD §4.4). Anticorpo Lei 2: SOP `vision-mcp-connector-install.md`. **Prova:** pkg **55/55** · tsc 0 · smoke-vision-cost-caps **3/3 LIVE** zero-cost · origem serve plugin 200 byte-idêntico · `/security-review` independente **SAFE** · container `7710b832` · 8 commits · Phase 5c **SEAL ALLOWED** (10) · mesh **8922** · handoff `c21c53db`. **Top Gap restante (tudo gated/Sovereign-side):** OAuth browser-flow (1º tenant externo) · `mistral`/`vision.ocr` (deferidos) · publish no MCP Registry (DNS challenge) · Stripe live · domínio Resend · atribuição compra ML. **Lição:** mapear o contrato BoK vivo antes de codar mostrou que per-plan+daily caps fechavam OTD-VM-025 na mesma sessão; e provar o install pelo handshake REAL da URL pública (não loopback/browser) é o que valida "Claude Code conecta" (Lei 1).
> 14	
> 15	**Sprint v6.39.1 — Vision MCP público: mcp.mcorch.com LIVE pelo Cloudflare (OTD-VM-013 fechada) (2026-06-16)** — ativação do vhost (último item Sovereign-side da Fatia 3). Split: Sovereign cuidou do Cloudflare (A record `mcp`→137.131.243.179 proxy **laranja** + SSL **Full** + **WAF Custom Rule Skip** por host), eu do nginx/origem (vhost `sites-enabled` SSE-tuned + cert **self-signed**, CF Full aceita) + verificação. **`mcp.mcorch.com` LIVE ponta-a-ponta** — Vision MCP saiu do loopback, consumível por hosts MCP externos. **DESCOBERTA crítica (gravada na BoK + memória):** CF laranja **desafia clientes não-browser** por padrão (`cf-mitigated: challenge` "Just a moment") → browser passa o JS mas SDK/curl/Claude-connector NÃO → **WAF skip por host é OBRIGATÓRIA** pra qualquer endpoint MCP/API atrás de CF laranja. Provado material (do datacenter, pelo CF público): `/health` 200, `/mcp` sem token 401, **handshake MCP real+JWT → mesh_search tenant-scoped 200**, sem-token rejeitado. Caveat: self-signed só em Full (não strict). 3 commits · Phase 5c **SEAL ALLOWED** (10) · mesh **8921** · handoff `0632e1f8`. **OTD-VM-013 FECHADA.** **Lição:** browser ≠ cliente programático — só declarei LIVE após o handshake MCP+JWT do datacenter (não o `/health` no navegador do Sovereign), que é o que pegou o challenge bloqueando os clientes reais (Lei 1).
> 16	
> 17	**Sprint v6.39.0 — Vision MCP Fatia 3 core: PAT external auth + LGPD erasure + nginx vhost (2026-06-15)** — próximos passos, Sovereign escolheu "Fatia 3 core + vhost config" (de 4 opções). Closed-Loop: mapeei o contrato BoK (data-model §2.1/§2.3 + SDD §5.2/§5.3/§7) antes de codar. **Entregue:** (1) **PAT** (FR-VM-003) — `mcp_access_tokens` (SHA-256 + **allowlist de scopes no DB** + teto 365d + RLS own) + `auth/pat.ts` + **dispatch PAT-vs-JWT** em `verifyBearer` (JWT→ALL_SCOPES; PAT→subset) + **scope-gate por tool** (`requireScope` → 403, default-deny); (2) **erase LGPD** (FR-VM-009) — `vision_artifacts` + `erase_vision_artifacts` (cascade **re-escopo `user_id` por DELETE**, sem primitiva cross-tenant) + retention-sweep diário; (3) **nginx** `mcp.mcorch.com.conf` SSE-tuned + runbook (ativação = DNS Sovereign). **Correção apply-reality OTD-VM-026:** `storage.objects` storage-admin-owned → deleção via Storage API pelo caller (RPC retorna `storage_paths`); bucket privado + RLS bucket-scoped default-deny já isolam. `mistral_api_key`/`vision.ocr` deferidos. 3 migrations aplicadas+registradas (Management API) · `/security-review` independente **SAFE** (0≥8) · smoke **7/7** LIVE (PAT scope-gate/revoke/expiry + erase zero-residue + cross-tenant guard) · pkg **50/50** · tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8920** · handoff `e0695dad` · 6 commits · container `fda2784f`. OTD-VM-020 marcada **PAT-first IMPLEMENTADA**. **Top Gap novo:** ativação do vhost (DNS Cloudflare — Sovereign) · OTD-VM-024 emenda BoK do engine + per-plan `planned_units` (DD-VM-003) + cap diário per-tenant (OTD-VM-025) · resto Fatia 3 (OAuth 2.1 browser-flow + Plugin Zip + UI de emissão de PAT + `mistral_api_key`/`vision.ocr`). **Lição:** o 42501 do `DELETE storage.objects` (SECURITY DEFINER não-owner) só apareceu no smoke contra o DB servido — testar o artefato servido pegou um defeito de realidade-de-apply do stub SDD (corrigido + OTD-VM-026); o mapeamento do contrato BoK antes de codar evitou improviso (Lei 2).
> 18	
> 19	**Sprint v6.38.0 — Vision MCP `deepsearch.run`/`poll` async (FR-VM-007 · job→poll→partial-refund §4.5) (2026-06-15)** — `/handson` → Sovereign puxou o item #1 do roadmap vision-mcp. Closed-Loop: workflow de **mapeamento (5 readers)** leu contrato selado + schema vivo + wiring ANTES do código — e **pegou que minha premissa contradizia a BoK** (a SDD sela **Firecrawl**, não "google/gemini"). Surfaceei; Sovereign decidiu (custom): *"não pagar Firecrawl agora; usar chaves já disponíveis"* → motor = **Gemini Google-Search grounding** (chave `google` já provisionada; BYOK→plataforma→402), **desvio consciente OTD-VM-024** (débito de emenda BoK); contrato job/refund/state 100% fiel à BoK. **Entregue:** `deepsearch.run` (3 mco, débito-na-entrada→`job_id`→worker in-process→refund parcial §4.5 floor-a-favor-do-tenant) + `deepsearch.poll` (grátis, tenant-bound, **self-heal de órfão**); `vision_jobs` (SELECT-own RLS) + **RPC atômico `finalize_vision_job`** (service-role-only, terminal+refund 1×/job); menores (`infra_health_logs` event/metadata + OTD-VM-023 orphan-sub). **Reviews:** workflow adversarial 5-lentes (2 HIGH: charge-without-value + refund-atomicity → fechados com finalize+reconcile) + **recuperação dos 3 verify mortos por session-limit** dos transcripts (achado novo: sem teto GLOBAL da chave-plataforma → **OTD-VM-025** semáforo; bucket era só per-sub) + allowlist de telemetria (side-channel cross-tenant) + erro de provider opaco + sentinel no `source_allowlist` + URLs http(s) + CHECK `refunded_mco≤charged_mco`. `/security-review` independente **SAFE** (0≥8). pkg **46/46** · tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8918** · handoff `fc0b5efc` · 6 commits · container `b24360c8` smoke **10/10** LIVE. **Top Gap novo:** Fatia 3 (PAT/OAuth/Plugin/jobs/erase LGPD) · vhost nginx OTD-VM-013 (root Sovereign) · cap diário per-tenant + rate-limiter compartilhado (OTD-VM-014/025) · emenda BoK do engine (OTD-VM-024) · per-plan `planned_units` (DD-VM-003). **Lição:** o workflow de mapeamento pré-código pegou a contradição Firecrawl-vs-Gemini ANTES de eu codar a coisa errada (Lei 2); e recuperar findings órfãos de transcript (em vez de re-rodar) achou 1 HIGH novo de custo que o /security-review (classe DoS excluída) não pegaria.
> 20	
> 21	**Sprint v6.37.0 — Vision MCP Fatia 2: 4 Billable Tools + BYOK Foundation (+ Fatia 1 handshake/interop close) (2026-06-15)** — diretiva começou em "fechar a última ponta não-provada da Fatia 1 (mesh.search E2E com JWT)" e o Sovereign mandou seguir até a Fatia 2 inteira ("algo completo", "você escolhe a ordem"). **(1) mesh.search E2E fechado + bug crítico de Fatia 1:** o E2E com cliente MCP real pegou que o servidor reusava **um** `StreamableHTTPServerTransport` stateless (SDK proíbe reuso → `notifications/initialized` **500**, nenhum cliente completava handshake) → fix fresh-per-request; provado **7/7** + adversarial **6/6** (forja ES256 ×3 + injeção PostgREST ×7). **(2) Interop de protocolo** (achado pelo `/security-review` independente): gate aceitava só `2025-11-25`, 400-ando clientes 3rd-party → ampliado p/ `SUPPORTED_PROTOCOL_VERSIONS`; cliente cru heterogêneo **8/8** (`2025-03-26`/`2025-06-18`). **(3) Fatia 2 — fundação** (SOP Lei 2 + `infra/billing.ts` + `auth/credentials.ts` + `safety/duty-of-care.ts`: BYOK→plataforma→402 · deduct-on-entry+refund-on-failure · sentinel · duty-of-care) + **4 tools billable provados:** `vision.describe_image` (FR-VM-018, 7/7), `vision.analyze_video` (FR-VM-024 Gemini — **não Higgsfield** — cobrança/min, 7/7), `deepsearch.scrape` (FR-VM-007 Firecrawl BYOK-only, 4/4), `mesh.consolidate_reference` (FR-VM-021 escrita tenant-escopada, 5/5). **(4)** migration `firecrawl_api_key` Vault (`/security-review` limpo · aplicada+registrada) + UI Settings **deployada** + SSRF redirect-fix (achado do review). pkg **34/34** · tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8917** · handoff `7a45d8ef` · 7 commits. **Top Gap novo:** `deepsearch.run` async (a metade "google/gemini" — FR-VM-007 job/poll) · Fatia 3 (PAT/OAuth/Plugin/jobs/erase LGPD) · vhost nginx OTD-VM-013 · OTD orphan-sub. **Lição:** o `/security-review` independente pagou de novo (achou o SSRF por redirect + o defeito de interop de protocolo que o cliente do mesmo-SDK mascarava); testar contra o ARTEFATO SERVIDO pegou o bug de handshake.
> 22	
> 23	**Sprint v6.36.2 — Vision MCP: OTD Gates Closed + Fatia 1 Built & Deployed ON (2026-06-15)** — diretiva Sovereign "ambos em sequência" (gates por pesquisa → código). **(1) Gates OTD pré-GA** (workflow `wf_0040a939-232`, 3 lentes verify adversarial): **OTD-VM-004 CLOSEABLE** (grade mcoCoins 4×-floor sobrevive — custo fonteado por provider, nenhuma sub-margem; `segment` cost-aware obrigatório; SOP `vision-mcp-cost-calibration.md`); **OTD-VM-001 CLOSEABLE** (corrigiu 2 erros factuais do blueprint — UEyes/Imp1k EXISTEM, SOTA=**SUM**/MIT self-hostável não DeepGaze; recall≥0.95 fundamentado); **OTD-VM-006 CLOSEABLE** (14 licenças verdes LICENSE-fetched + 3 minas banidas; SpikingJelly não-MIT); **OTD-VM-005 PARTIAL** (SCCs-ANPD inviável; Res. 32/2026 UE adequada; Mistral=default candidato). **(2) Fatia 1 construída + DEPLOYADA ON** (`packages/vision-mcp-core/` → container `mcorch_vision_mcp` Sovereign Mesh, restart=unless-stopped, UID1001, read-only, `127.0.0.1:3200`): Streamable HTTP + ES256 JWKS fail-closed + Origin/protocol gates + sentinel + `mesh.search` tenant-safe. Provado material **contra o container**: health 200/401+WWW-Authenticate RFC9728/403/400 + row infra_health_logs + 14/14 testes. **2 bugs que só o deploy pegou:** bind `0.0.0.0` (port-map do bridge) + schema real de `infra_health_logs` (sem `metadata` — o padrão do sentinel edge falha silencioso). tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8916** · handoff `98fa83d7` · 4 commits. **Top Gap novo:** mesh.search E2E com JWT (handshake MCP) · vhost nginx `mcp.mcorch.com` (OTD-VM-013, root Sovereign) · Fatia 2 (foveal billable + per-user creds) · migration `infra_health_logs ADD metadata jsonb` (telemetria rica). **Lição:** testar o ARTEFATO SERVIDO (container), não o node local — Lei 1 pegou 2 bugs + 1 schema drift que unit/local não veriam.
> 24	
> 25	**Sprint v6.36.1 — Vision MCP: BoK 9/9 + 8-Agent System + Adversarial Validation (2026-06-15)** — diretiva Sovereign (ref. sandcastles.ai): MCP Interno nativo de **percepção visual + deepsearch fundamentado** ("Essência Humana"), interno + ecossistemas externos. Closed-Loop BoK-first em 3 atos: **(1) Blueprint-semente v0.2.0** (workflow ultracode 19 agentes · 140 refs · verify adversarial — 5 pilares CV/Motion/Neuromorphic/Peripheral/**Cognitive** + vertical **Tecnologia Assistiva** beachhead demand-provado); **(2) Suíte BoK 9/9** (`/bok-scribe`) selada na malha (node `318862b7`, DERIVES_FROM mcorch-constellation, embedding 768d) — runtime container `mcorch_vision_mcp` Sovereign Mesh, **0 edge fns**; **(3) Sistema de 8 agentes BoK** (`/bok-agents-generator`) com Pantheon Reconciliation (eleva, não recria). **Validação adversarial independente (3 lentes) = SUITE VALIDATED** após pegar+corrigir **1 blocker cross-tenant real** (`erase_vision_artifacts` cascade DELETE sem re-escopar `user_id`) + hardening (scopes allowlist física, expiry CHECK, Storage policy DDL, colisão OTD-VM-020→021, FMEA-VM-004 RPN175→OTD-VM-022). Anticorpo **`deepsearch-blueprint`** (skill+agent+SOP) — padrão rodou 2× (Cyber-Sentinel+Vision MCP). tsc 0 · Phase 5c **SEAL ALLOWED** (10) · mesh **8915** · handoff `b73d141d` · README badge `6.36.0-vision-mcp`. 4 workflows mortos por cota recuperados (resumeFromRunId/main loop) — zero perda. **Top Gap novo:** Fatias MVP do vision-mcp (BoK gate ABERTO) — Fatia 1 esqueleto MCP autenticado internal · gates OTD-VM-001 (recall Tier1) / -004 (unit economics) / -005 (DPA) / -013 (nginx vhost) / -020 (OAuth AS). **Lição:** validação adversarial por agente que NÃO escreveu a suíte pega o que self-review não pega (vetor cross-tenant que minha mão + 1ª lente deixaram passar).
> 26	
> 27	**Sprint v6.36.0 — Native OpenDesign Integration + MIV Redesign Backlog (2026-06-14)** — Configuração do OpenDesign de forma nativa e inclusão da meta de redesign completo baseada no MIV (Manual de Identidade Visual) no roadmap. **(1) Nativização do OpenDesign** (`CanvasDesignPage.tsx`): o editor foi simplificado para renderizar o iframe do OpenDesign em tela cheia na rota `/dashboard/canvas/design`, removendo o controle local antigo e as abas redundantes, criando uma experiência 100% nativa. **(2) Backlog de Redesign MIV**: adicionado o OTD-MIV-REDESIGN na lista de Top Gaps e no roadmap do Canvas Studio.
> 28	
> 29	**Sprint v6.35.0 — Core-Fable: Fable 5 Flagship + Metering + Mega Brain Interstellar (2026-06-10)** — Diretiva Sovereign "Refatore todo o nosso Core-v2 para Core-Fable" em 3 arcos: **(1) Rebrand** (`914f8dd`): rota `/dashboard/core-fable` (+redirects compat), `CoreFablePage`/`components/core-fable/`, Claude Fable 5 (`anthropic/claude-fable-5` via OpenRouter, verificado live no catálogo) como default do Core; seletor de chat **desacoplado** do `pref_ai_model` (localStorage) — 1 clique não re-modela o flywheel pago. **(2) Review adversarial pré-deploy confirmou 4 P1 econômicos** (`997b307`): aios-chat OpenRouter nascia SEM metering (billing bypass na chave-plataforma) → `_shared/agent-metering.ts` compartilhado fiado nos 2 paths; `agent_pricing` sem rows novas → under-billing 133-167× via fallback flash → migration `20260610010000` seeda fable-5 1000/5000 + sonnet-4.6 300/1500 + dropa id morto; `/security-review` SAFE. Provado live: probe `{"output":"Claude"}` + ledger correto + `calc_agent_cost_mcoin`=120. **(3) Mega Brain Interstellar** (`3b15e41`→`47f9316`): loop iterativo de 8 screenshots dirigido por referência visual do Sovereign — câmera quase equatorial + 210 steps adaptativos = arco lensado contínuo sobre a sombra; **raios capturados = preto** (matou anel de névoa + bola branca do glow artificial — críticos precisam ~310 steps/órbita); disco blackbody edge-on, reação por energia (surge/spin/shimmer). tsc 0 · suíte **295** · Phase 5c **SEAL ALLOWED** (10) · mesh **8865** · handoff `4728b8aa`. **Top Gap novo:** OTD-FABLE-MARGIN (margem 2.0 do calc < 4×-floor p/ chat premium) · fallback `pricing_not_found` silencioso (fail-caro + telemetria). **Lição:** o screenshot-loop com sessão real no preview local (sem tocar o dist servido) pegou 2 bugs visuais que tsc/testes jamais veriam (GLSL só falha em runtime); e o review adversarial pagou de novo — 4 P1 econômicos numa feature "só de rename".
> 30	
> 31	**Sprint v6.34.0 — Cyber-Sentinel: Security BoK 4/4 + Prompt Gate Live + Infra Hardening (2026-06-10)** — diretiva CISO executada em 2 fases na mesma sessão. **(1) BoK de segurança 4/4** (`docs/bok/security/`, schema CISO 01-brd/02-srs/03-sdd/04-fmea — 12 BR-SEC + Risk Ledger · 15 FR-SEC + matriz RLS canônica + `SET LOCAL` · SDD lefthook/Arcjet/sentinel/Dockerfile UID1001/compose cap_drop integrais · FMEA 12 modos RPN AIOS). **(2) Aplicação no ecossistema vivo** (`6f2f75a`): **Sentinel LIVE** em `orchestrate-content` (prod **v52**) — `_shared/sentinel.ts` barra injeção/bypass/ANSI **depois da identidade, antes do `deduct_mco_coins`**; provado em prod com JWT real (`HTTP 403 layer=sentinel` score=3, **zero mcoCoins**). Infra recriada e endurecida: `claude_mem` uid1001+read_only+8caps (healthy), `chroma` caps conservadoras+no-new-privileges (heartbeat vivo), `gitnexus` imagem não-root buildada; env `SUPABASE_SERVICE_ROLE_KEY` revogada removida do compose (FM-04). Gate git **dual-engine** lefthook+gitleaks (pre-commit/pre-push, degrada sem gitleaks — OTD-SEC-003). **Review adversarial pegou 4 bugs reais ANTES de qualquer deploy quente**: rate-limiter falsava o fan-out paralelo de `campaign-run`; `cap_drop SETUID/SETGID` quebraria o `chroma` de terceiros; regex de 1 qualificador; guard `&&||` do gitleaks engolia a detecção. tsc 0 · suíte **295** · Phase 5c **SEAL ALLOWED** (10) · mesh **8862** · handoff `0a9865a9` + BoK seal `424f0fe4`. **Próximos:** FM-10 gitnexus (imagem pronta, roda stdio) · OTD-SEC-006/007 (fiar sentinel + migration `security_events`/quarentena <50ms nas demais fns pagas) · Arcjet aguarda superfície Next/BFF. **Lição:** verificar **materialmente** (dry-run dos containers, exploit real em prod) antes de declarar — pegou o `name:` que orfanaria os containers e os 4 bugs do review.
> 32	
> 33	**Sprint v6.33.1 — Hotfix Kanban ScrollArea + E2E à Prova de Cloudflare (2026-06-09)** — bug report do Sovereign no `/dashboard/kanban`: `ReferenceError: ScrollArea is not defined` ao criar coluna. **Causa:** `KanbanPage.tsx` usava `<ScrollArea>` (área scrollável de tarefas) sem importar — só quebrava *depois* da 1ª coluna (empty-state não exercita o componente). **Fix de 1 linha** (`e55ce70`): import `@/components/ui/scroll-area`; deploy material (chunk novo `KanbanPage-CW7WBYjZ.js` ≠ o do stack trace, import scroll-area + env baked); **confirmado em prod pelo print do Sovereign**. **E2E completo** via preview local do `dist` + sessão injetada (CF Turnstile barra agent-browser do datacenter até no `login.mcorch.com`): CRUD + drag-drop bidirecional **provado pelo DB** (3× PATCH 200 + SELECT, não pelo DOM). Helper `gen-user-session.ts` (`761ea6f`) p/ E2E logado à prova de CF. **Incidente de concorrência** (Sovereign mexendo em prod junto) resolvido sem perda de dado — board/coluna intactos, a "divergência" da 1ª rodada era o Sovereign movendo o mesmo card. tsc 0 · suíte **284** · Phase 5c **SEAL ALLOWED** (10) · mesh **8860** · handoff `fd20b125`. **Lição:** E2E mutável vai em board descartável, nunca no dado real do Sovereign; DB-prod é compartilhado. **Diretiva CISO de hardening DEFERIDA** (blueprint `6b1571a` commitado; 4 artefatos BoK de segurança p/ sessão dedicada).
> 34	
> 35	**Sprint v6.33.0 — ML Attribution Fix + Browser Operator BoK (2026-06-08)** — o teste **real** do Sovereign no branded link expôs o flywheel emitindo link **MORTO**. **(1) Fix do auto-monetize** (`34d7ef0`): `_shared/affiliate.ts` `buildMlProductUrl` montava o formato BARE `mercadolivre.com.br/MLB-<id>` (404) com 2/3 ids stale → agora resolve `vm_affiliate_products.product_url` real (fonte única Apify), fail-open `/p/`; **reconcilia "ML não conta clique"** (era 404, não falha do matt_word — o painel ML já contara matt_word em produto VÁLIDO em 2026-06-04); provado E2E `7993c6a4` 302 → `/p/MLB27834876`; deploy `orchestrate-step` 122.8kB. **(2) BoK 9/9 do Operador de Browser Autenticado** (`/bok-scribe`, `24ba435`): suíte 756 LOC MR→SDD+STRIDE+FMEA; **gate pagou** — o link oficial é per-user → nova `user_affiliate_links` (não a `vm_affiliate_products.affiliate_template_url` COMPARTILHADA, que vazaria entre tenants — OTD-ABO-003); runtime residencial cravado (datacenter **403** reprovado em produto real `/p/`, bare e `/afiliados/hub`); mesh seal `31323fe3` + DERIVES_FROM edge `9ea18d26` → mercado-livre-api. tsc 0 · suíte **284** · Phase 5c **SEAL ALLOWED** (10) · mesh **8852** · handoff `630509e2`. **Top Gap:** **BUILD do Operador** (gate ABERTO; runtime residencial = Sovereign roda `agent-browser` logado no ML) · domínio Resend · conversão ML real. **Lição:** o teste por **mão do Sovereign** (clicks 0→4) achou o link morto que meu curl-403 do datacenter mascarava; o BoK-first pegou o vazamento cross-tenant **antes** do código.
> 36	
> 37	**Sprint — Stored-XSS Hardening + Antibody (2026-06-08)** — `/security-review` (v6.28.0) havia flagado stored-XSS em `DashboardHome` (`content_library.body` cru via `dangerouslySetInnerHTML`); fechado **ponta-a-ponta** nesta sessão. Sanitização `DOMPurify.sanitize` (já shipada via Antigravity em `da9da4c`/`e5a661a`) + guarda de regressão **6 testes** (`dashboard-html-sanitize.test.ts`: preserva `<a href>` de afiliado + tags de artigo, remove `<script>`/`onerror`/`javascript:`) + **antibody ESLint `no-restricted-syntax`** (`2522e71`, sem dep nova — `eslint-plugin-react` ausente) que faz todo `dangerouslySetInnerHTML` futuro acusar no lint até ser sanitizado+justificado (sink cru plantado → **pego** material; 2 sinks legítimos justificados: DashboardHome DOMPurify · chart.tsx CSS shadcn) + limpeza dos **7 `no-explicit-any`** do data-layer de DashboardHome (`3129369`). Handoff node `e12ed58e` + obs antibody `505fb670` (embedded 768d). tsc 0 · suíte verde · mesh **8849**. **Anticorpo Permanente cumprido** — reincidência do sink barrada no lint. **Top gaps restantes (herdados de v6.28.0, gated no Sovereign):** domínio `RESEND_FROM` (entrega Resend real) · branded redirect `login.mcorch.com/go` · 2 rascunhos WP de teste · atribuição de compra ML.
> 38	
> 39	**Sprint v6.32.x — arco Core-v2 Black Hole (2026-06-07, via Antigravity)** — sessões conduzidas no Antigravity, seladas e versionadas no git, registradas aqui retroativamente a partir dos records do HANDOFF.md (não reauditadas em detalhe — Lei 1): **v6.32.6** Unified Relativistic Black Hole & Cymatics (fusão dos visualizadores num único shader WebGL Schwarzschild — raymarching + disco de acreção + Doppler beaming + ondas de cymatics; layout 30/70; `CymaticsLayer` removido; 284 testes; handoff `ec6204a4`; mesh 8847); **v6.32.5** Model Selector Fix & Reacting Black Hole (fix case-collision dos hooks `useAiosTerminalChat`/`useAiosWorkspaceChat`; persistência do modelo selecionado em `user_api_keys`; redesign MegaBrainVisualizer + CymaticsLayer; 260 testes; handoff `8627661a`; mesh 8839); **v6.32.2** Gemini 3.1 Live Mode (Live API → Gemini 3.1 Flash Live audio-only + Gemini Docs MCP + API Skills; handoff `5acba7aa`; mesh 8818). Os seals intermediários (v6.29–v6.32.4) existem em HANDOFF.md/README mas não foram back-filled aqui.
> 40	
> 41	**Sprint v6.28.0 selado em 2026-06-04** — **Quatro next-steps fechados numa sessão (probe-first)**. Diretiva Sovereign "ataque os 4 pontos numa sessão só, não pare até terminar; o ponto 4 do link não funcionou a contabilidade de clicks" (+ screenshot ML com 1 clique). Cada gap verificado **no código** antes de tocar. **(1) OTD-INTENT-DISPATCH-REFUND FECHADA:** `orchestrate-content` estorna os 10 em falha pós-débito (`!runId` ou erro do kick `async_orchestrate_step`) + marca run `error` — estende o contrato refund da v6.27.2 ao núcleo do flywheel. **(2) nurture-dispatch entrega Resend real (FR-MH-008):** resolve `resend_api_key` per-user (BYOK) + `leads.contact` → POST Resend quando email+chave+endereço; senão `gated`; send `failed` estorna. Live a inbox real ainda gated em `RESEND_FROM` (domínio Sovereign). **(3) Click ledger in-system (OTD-ML-CLICKS):** links publicados passam pelo redirect `process-affiliate-link` GET, que registra o clique atômico (RPC `record_affiliate_click` service-role-only, atribuído ao dono) + 302 pro ML; `link-forge` emite o redirect; **ROIWidget já soma `affiliate_links.clicks`** → "Cliques Totais" reflete cliques reais antes de compra; migration 120000 + fix 130000 (`content_id` UUID). **(4) 1º dispatch pago E2E agentic:** intent→policy→execute→orchestrate-content WP **draft**, run `43048d8e` **done**, **delta 10 exato** (valida ponto 1 em prod), HITL gate provado, blast-radius wordpress-only. **Prova:** `/security-review` independente **SAFE** · drift audit **exit 0** · smoke-affiliate-click **10/10** + smoke-nurture **10/10** · suíte **269** · tsc 0 · deploys 107.9/83.72/87.96kB · Phase 5c **SEAL ALLOWED** (7 verified) · Mesh **8783**. 6 commits. **Novo Top Gap:** entrega Resend a inbox real (domínio `RESEND_FROM` — Sovereign) · branded redirect domain (`login.mcorch.com/go` proxy nginx — link limpo+rastreado) · 2 rascunhos WP de teste a limpar · atribuição de compra ML (aguardando conversão). **Lição:** probe-first economizou retrabalho (ROIWidget já somava clicks → zero UI nova; `resend_api_key` já existia → só o canal) e pegou o bug 22P02 do RPC (content_id UUID) no smoke antes de declarar — corrigi via migration na mesma sessão (regra hotfix→migration). **Follow-up (mesma sessão, "continue com os próximos"):** click ledger estendido ao caminho **interativo** de monetização — POST `process-affiliate-link` retorna redirect rastreável `?link_id` (migration `20260604140000` + RPC `record_affiliate_click_by_link`). O smoke estendido (G8) expôs um insert de `affiliate_links` quebrado há tempo (`campaign_id` UUID vs slug `"ai_orchestration"` → 22P02 silencioso, nenhuma linha de afiliado nunca persistida) + o `/security-review` independente pegou um **open-redirect** no branch novo (302 pro `short_url` tenant-writável) — ambos corrigidos (gate de domínio ML + UUID-só); smoke **9/9** (G9 prova o open-redirect bloqueado), commit `b2c39f6`. **Follow-up 2 ("faça todos os 3"):** (A) **auto-monetização** no `orchestrate-step` — o artigo gerado embute o redirect rastreável `?link_id` per-owner (`_shared/affiliate.ts`), o flywheel monetiza+rastreia automático; provado E2E pago run `cee55b11` (Roborock → link rastreável no `content_mesh_asset`). (B) **matt_tool** per-user (coluna `affiliate_config` + threading GET/POST/orchestrate + UI `AffiliatesPage`; caveat honesto: efeito na atribuição ML não-verificável, mas aditivo). (C) **campaign-run assíncrono** p/ >8 passos (`EdgeRuntime.waitUntil`, batches; pequenas seguem síncronas). `/security-review` independente **SAFE** (flagou XSS **pré-existente** `DashboardHome:677` dangerouslySetInnerHTML → tarefa spawned). Smokes click **G1-G9+G1b** · campaign **A-H** · e2e auto-monetize ✅ · tsc 0 · drift exit 0. 4 commits (`9bb5bba`/`bb999c1`/`7cbd036`/`b468c98`).
> ```

## 🤖 Claude *(17:12:10)*


## 🤖 Claude *(17:12:11)*

Now the tail of HANDOFF.md plus the BoK gate check and the active project memory.

## 🤖 Claude *(17:12:12)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 7695,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 7695	ContentLibraryPage monetization flow:
> 7696	  Card (text, body contains mercadolivre.com.br)
> 7697	    └── DropdownMenu → "Monetizar Links ML"
> 7698	          → handleMonetizeLinks(item):
> 7699	               match(ML_URL_RE) → unique URLs
> 7700	               for url of unique:
> 7701	                 POST process-affiliate-link → affiliate_url
> 7702	                 body.split(url).join(affiliate_url)
> 7703	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 7704	          → Badge 💰 ML (emerald) exibido após monetização
> 7705	```
> 7706	
> 7707	---
> 7708	
> 7709	## Pending Actions (Commercial Launch)
> 7710	
> 7711	### CRITICAL — Must complete before first client
> 7712	
> 7713	🎯. **[BoK SELADA — código pendente] Viral Autopilot — implementação (R1-R4)** — BoK 9/9 selada 2026-06-17 (`docs/bok/viral-autopilot/`, seal node `b3398294`). **BoK Gate ABERTO.** Rota de 8 passos (do maior alavancagem): **(1)** ⚠️ **gate Lei 2** — escrever SOP `docs/processes/autopilot-cron-identity.md` (OTD-VA-008) ANTES da fatia de cadência/custo (Operator/Sequence/Verification/Recovery do mint server-trusted + pré-débito/refund); **(2) Fatia 1 (NÃO depende do cron)** — geração product-aware + monetizar TODO formato (FR-VA-003/004/016): honrar `product_target` (dropado em `orchestrate-content:79`), passar produto-alvo+imagem ao prompt do `orchestrate-step`, estender `monetizeContent` de artigo→article+LinkedIn+Twitter com `content_variant_id` (= `content_library.id`, grava `affiliate_links.content_id`); **(3)** reconectar `fetch-trends`/`vm_affiliate_products` à pauta; **(4)** cadência (tabelas `autopilot_plans`/`_cycles`/`creative_metrics` + RPCs `begin`/`finalize_autopilot_cycle` + cron `autopilot-cadence`; **cron prova service-role in-function** `Bearer SB_SECRET_KEY` antes de confiar `x-autopilot-user-id`); **(5)** coletor `autopilot-collect`; **(6)** fechar loop R3 (`autopilot-analyze` inline + feedback-inject scope=`viral_autopilot`); **(7)** mídia viral 9:16 (fase 2); **(8)** provar postback ML real (OTD-VA-007/OTD-ML-MP-PER-USER). **Toda migration passa /security-review.** Constraints chave: `N_runs=prod×rede×ab_variants`, imagem no bundle de 10 (`billing.ts:16-21`), refund crédito-positivo (NUNCA deduct negativo — RPC anti-mint `20260603220000:45`), FK composta tenant-escopada, `campaign_metrics` deprecada→`creative_metrics`.
> 7714	
> 7715	🌌. **[EM ANDAMENTO — Phase Epsilon V9] Unified Sensorial Canvas — Fases 3.5-3.10** — Fases 3.1-3.4 ✅ (scaffold rota/store/shell 72-28 + Code Network R3F InstancedMesh Louvain + Memory Network cymatics shell + Black Hole MegaBrain backdrop; E2E ocular nos 3 modos; commits `210b90d`/`d832084`/`4940b4d`/`38d9760`/`769acb1`). **Restam:** **3.5** Sinapses inter-rede (arestas **REAIS** de `mcorch_edges` cruzando código↔memória, lit só no modo Universo — nunca fabricar) · **3.6** fly-to (select→`useNodeIntelligence` + câmera anima até o cluster) · **3.7** layout/perf (`OTD-UCANVAS-PERF` — a query do código leva **~30s** com 2 canvases; considerar Louvain em Web Worker / streaming do grafo / lazy do backdrop) · **3.8** executar a poda do squad-coloring (`OTD-SQUAD-OWNERSHIP-REVIVAL`) · **3.9** paridade + cutover de nav + gate E2E 1920×1080 · **3.10** seal. Plano vivo: `.claude/context/unified-core-sensorial-canvas-plan.md`. BoK selada (PR-025 · FR-043..049 · NFR-023/024 · SDD §9). **3 páginas legadas (matrix/memory/core-fable) preservadas como backup até 3.9.**
> 7716	
> 7717	🔐. **[DEFERIDA — diretiva CISO 2026-06-09] Suíte BoK de Segurança (Production Hardening)** — o Sovereign emitiu a diretiva `MCORCH CYBER-SENTINEL` (gerar `docs/bok/security/{01-brd-security,02-srs-secure-spec,03-sdd-hardening-architecture,04-fmea-security}.md`) mas **interrompeu em favor do seal do Kanban**. O blueprint-semente está commitado (`6b1571a`, `docs/bok/security/00-deepsearch-blueprint.md`). Escopo a gerar (production-ready, sem placeholders): **01-brd** 12 BRs (BR-SEC-001..012 — proteção do ledger mcoCoins, anti-prompt-injection no edge routing, chaves Stripe live, brand protection Yachtmax/OKEAN); **02-srs** 15 FRs (FR-SEC-001..015 — verificação de prompt edge-native, validação manual de assinatura JWT por runtime, rotação OAuth social, Vault; matriz RLS canônica `CREATE POLICY` multi-tenant user_id+project_id); **03-sdd** configs reais (lefthook.yml paralelo de secret-scan, `.husky/pre-commit` p/ monorepo aninhado, middleware Edge TS multi-camada com `@arcjet/next`, Dockerfile multi-stage `appuser` UID 1001, docker-compose dropando `CAP_CHOWN/DAC_OVERRIDE/SETUID/SETGID` + `cpus`/`mem_limit`); **04-fmea** RPN p/ vetores AIOS (prompt-injection→billing bypass, log poisoning ANSI, network drift) com remediação L1 edge-reject + L2 self-heal <50ms. **Sessão dedicada** — reaplicar a diretiva com o blueprint como Fonte da Verdade.
> 7718	
> 7719	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 7720	
> 7721	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 7722	
> 7723	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 7724	
> 7725	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 7726	
> 7727	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 7728	
> 7729	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 7730	
> 7731	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 7732	
> 7733	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 7734	
> 7735	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 7736	   ```bash
> 7737	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 7738	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 7739	   ```
> 7740	
> 7741	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 7742	
> 7743	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 7744	
> 7745	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 7746	
> 7747	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 7748	
> 7749	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 7750	
> 7751	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 7752	
> 7753	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 7754	
> 7755	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 7756	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 7757	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 7758	
> 7759	### SOCIAL — Next steps
> 7760	
> 7761	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 7762	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 7763	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 7764	
> 7765	### NON-CRITICAL
> 7766	
> 7767	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 7768	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 7769	- `browserslist` — ✅ updated (2026-04-26)
> 7770	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 7771	
> 7772	### GITNEXUS MCP — Next steps
> 7773	
> 7774	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 7775	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 7776	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 7777	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 7778	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 7779	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 7780	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 7781	
> 7782	### PHASE EPSILON — Next iterations
> 7783	
> 7784	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 7785	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 7786	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 7787	
> 7788	### CORE — Next iterations
> 7789	
> 7790	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 7791	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 7792	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 7793	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 7794	
> 7795	### PHASE DELTA — Next iterations
> 7796	
> 7797	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 7798	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 7799	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 7800	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 7801	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 7802	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 7803	
> 7804	### USUÁRIO ZERO — Checklist de validação
> 7805	
> 7806	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 7807	- ✅ Stripe sandbox secrets no vault
> 7808	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 7809	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 7810	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 7811	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 7812	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 7813	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 7814	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 7815	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 7816	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 7817	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 7818	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 7819	
> 7820	---
> 7821	
> 7822	## Infrastructure
> 7823	
> 7824	| Service | Container | Port | Status |
> 7825	|---------|-----------|------|--------|
> 7826	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 7827	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 7828	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 7829	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 7830	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 7831	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 7832	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 7833	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 7834	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 7835	
> 7836	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 7837	
> 7838	```bash
> 7839	docker compose up -d
> 7840	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 7841	```
> 7842	
> 7843	---
> 7844	
> 7845	## Security Model (Post-Go-Live)
> 7846	
> 7847	| Table | Isolation |
> 7848	|-------|-----------|
> 7849	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 7850	| `mcorch_edges` | Same pattern |
> 7851	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 7852	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 7853	
> 7854	---
> 7855	
> 7856	## Billing Architecture
> 7857	
> 7858	| Decision | Value |
> 7859	|----------|-------|
> 7860	| Canonical billing ledger | `profiles.mco_balance` |
> 7861	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 7862	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 7863	| Orchestration cost | 10 mcoCoins/run |
> 7864	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 7865	| Stripe | Sandbox keys active — swap to live before first client |
> 7866	
> 7867	---
> 7868	
> 7869	## GraphRAG State
> 7870	
> 7871	- **8934 total nodes** (verificado live 2026-06-20 via REST count=exact, viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> 7872	- _(prev snapshot)_ **8755 total nodes** (verificado live 2026-06-03 via REST count=exact após o handoff node `a48d8ff4-1069-4ca0-8764-f01922e2e12f` desta seal v6.21.0, embedded 768d; inclui o BoK seal `d5163fed` marketing-hub; v6.20.4 snapshot era 8753, handoff `af6bffa2`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 7873	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 7874	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 7875	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 7876	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 7877	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 7878	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 7879	- HNSW cosine index operational
> 7880	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 7881	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 7882	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 7883	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 7884	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 7885	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 7886	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 7887	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 7888	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 7889	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 7890	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 7891	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 7892	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 7893	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 7894	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 7895	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 7896	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 7897	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 7898	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 7899	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 7900	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 7901	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 7902	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 7903	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 7904	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 7905	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 7906	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 7907	- Handoff node (2026-06-07): `session-handoff-20260607-gemini-3.1-live-mode-migration` (`5acba7aa-793e-4418-9139-a093283c12bb`) inserido (type=`handoff` · stability 1.0) — v6.32.2: Migrada a Live API para Gemini 3.1 Flash Live com audio-only, adicionados Gemini Docs MCP e as API Skills
> 7908	
> 7909	### Embedding Model
> 7910	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 7911	Schema: `vector(768)` — HNSW cosine index.
> 7912	
> 7913	### Embedding Pipeline (Autônomo — 2026-05-03)
> 7914	Três camadas eliminam intervenção manual:
> 7915	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 7916	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 7917	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 7918	
> 7919	### Comandos de manutenção da Mesh
> 7920	```bash
> 7921	# Verificar nós sem embedding (deveria retornar array vazio):
> 7922	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 7923	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 7924	
> 7925	# Backfill manual (Bun-native — requer .env):
> 7926	bun run scripts/backfill-embeddings.ts
> 7927	
> 7928	# Backfill de código-fonte nos nós AST:
> 7929	bun run scripts/backfill-node-content.ts
> 7930	
> 7931	# Re-sync AST completo:
> 7932	cd packages/gitnexus-core && npm run sync-mesh
> 7933	
> 7934	# Acompanhar re-ingesta pós-commit:
> 7935	tail -f /tmp/mcorch-ingest.log
> 7936	```
> 7937	
> 7938	---
> 7939	
> 7940	## Video Rescue Protocol
> 7941	
> 7942	When a video generation operation (Google Veo) times out or client disconnects:
> 7943	```bash
> 7944	# Via edge function (production):
> 7945	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 7946	  -H "Authorization: Bearer <user_jwt>" \
> 7947	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 7948	
> 7949	# Via local script (admin/debug):
> 7950	source .env && bun run rescue.ts <operation_id> <content_id>
> 7951	```
> 7952	
> 7953	---
> 7954	
> 7955	## Architecture Pillars
> 7956	
> 7957	| Layer | Implementation |
> 7958	|-------|---------------|
> 7959	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 7960	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 7961	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 7962	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 7963	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 7964	
> 7965	---
> 7966	
> 7967	## Phase Delta — Architecture
> 7968	
> 7969	```
> 7970	OrchestrationPage (full-canvas, p-0)
> 7971	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 7972	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 7973	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 7974	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 7975	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 7976	        ├── nodes/PublishNode.tsx    ← final distribution output
> 7977	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 7978	        └── NodePalette.tsx          ← top toolbar to add nodes
> 7979	
> 7980	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 7981	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 7982	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 7983	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 7984	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 7985	```
> 7986	
> 7987	### Canvas State Architecture (Hybrid)
> 7988	
> 7989	```
> 7990	User interaction → ReactFlow internal state (positions, drag)
> 7991	                         ↓ (debounced 600ms)
> 7992	                   localStorage (positions persist across refresh)
> 7993	                         ↑
> 7994	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 7995	     ↓ (status changes sync to ReactFlow via useEffect)
> 7996	ReactFlow renders visual status (idle/running/done/error/blocked)
> 7997	```
> 7998	
> 7999	## Key Files
> 8000	
> 8001	| Purpose | Path |
> 8002	|---------|------|
> 8003	| Architecture rules | `CLAUDE.md` |
> 8004	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 8005	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 8006	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 8007	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 8008	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 8009	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 8010	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 8011	| **Node types** | `src/components/orchestrator/nodes/` |
> 8012	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 8013	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 8014	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 8015	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 8016	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 8017	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 8018	| Billing utilities | `src/lib/billing.ts` |
> 8019	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 8020	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 8021	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 8022	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 8023	| Video rescue (local) | `rescue.ts` |
> 8024	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 8025	| Backfill script | `scripts/backfill-embeddings.ts` |
> 8026	| Deploy harness | `scripts/harness-deploy.sh` |
> 8027	
> 8028	---
> 8029	
> 8030	## First Client Onboarding Checklist
> 8031	
> 8032	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 8033	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 8034	3. ~~Activate watchdog cron~~ ✅ Done
> 8035	4. ~~Deploy rescue-video function~~ ✅ Done
> 8036	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 8037	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 8038	7. Monitor `infra_health_logs` for first 24h.
> 8039	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 8040	
> 8041	---
> 8042	
> 8043	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 8044	
> 8045	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 8046	
> 8047	| Action | Result |
> 8048	|--------|--------|
> 8049	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 8050	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 8051	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 8052	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 8053	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 8054	
> 8055	| Commit | Conteúdo |
> 8056	|--------|----------|
> 8057	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 8058	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 8059	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 8060	
> 8061	### Arquitetura Matrix Intelligence
> 8062	
> 8063	```
> 8064	ConstellationMatrix (Stabilized Engine)
> 8065	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 8066	  └── NodeDetailsPanel (Tabbed Navigation)
> 8067	        ├── Tab Meta: Neighbor exploration + Net Context
> 8068	        ├── Tab Code: Source code preview (Supabase sync)
> 8069	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 8070	
> 8071	useNodeIntelligence Hook:
> 8072	  - contentQuery: fetch nodes.content column
> 8073	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 8074	  - state: isAnalyzing, analysisResult, progress
> 8075	```
> 8076	
> 8077	---
> 8078	
> 8079	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 8080	
> 8081	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 8082	
> 8083	| Action | Result |
> 8084	|--------|--------|
> 8085	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 8086	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 8087	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 8088	
> 8089	**Output da análise (estruturado em pt-BR):**
> 8090	- Visão Geral — papel do módulo no sistema
> 8091	- Padrões Detectados — design patterns, antipatterns
> 8092	- Acoplamento & Dependências — análise In/Out-Degree
> 8093	- Recomendações — 1-3 ações priorizadas
> 8094	
> ```

## 🤖 Claude *(17:12:13)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_viral_autopilot.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	---
> 2	name: project_viral_autopilot
> 3	description: Motor de conteúdo viral autônomo monetizado (afiliado ML) — auditoria material + 4 decisões Sovereign + BoK gate (suite novo viral-autopilot)
> 4	metadata: 
> 5	  node_type: memory
> 6	  type: project
> 7	  originSessionId: 21b2d649-94ad-4468-9821-20f76eae70a3
> 8	---
> 9	
> 10	Diretiva Sovereign 2026-06-17: construir o **motor de conteúdo viral autônomo** — o coração de receita do MCORCH. Quatro requisitos:
> 11	- **R1** gerar conteúdo p/ redes sociais automaticamente · **R2** agendar (tudo de uma vez OU lote a cada 3 dias) · **R3** a cada ciclo analisar o desempenho anterior p/ melhorar os próximos criativos (loop auto-melhorável) · **R4** conteúdo viral com comissão de afiliado do Mercado Livre.
> 12	
> 13	**Auditoria material (workflow 7-agentes, 2026-06-17 — cada achado com path:linha):**
> 14	- **R1 parcial:** pipeline de TEXTO vivo (`orchestrate-content`→`orchestrate-step` gera artigo+LinkedIn+X). `generate-image`/`generate-video` são ÓRFÃS (zero callers); só publica WP/LinkedIn/X; Canvas assets não entram no publish.
> 15	- **R2 parcial:** "tudo de uma vez" existe (`campaign-run` fan-out). **A recorrência "a cada 3 dias" NÃO existe** — só 2 pg_cron (memory-decay + nurture-drip), nenhum re-gera. Agendamento é offset fixo +1h/+2h hardcoded.
> 16	- **R3 ausente:** loop aberto em 3 quebras — `campaign_metrics` tem ZERO writers (roda vazio); `optimization_policy` nunca lida por gerador; `self-optimize` sem cron (só botão UI). Engajamento orgânico por post nunca coletado.
> 17	- **R4 parcial:** receita ML madura (`affiliate_config` per-user, click ledger, `handle-ml-postback` HMAC). MAS conteúdo é product-unaware — monetiza só o artigo, catálogo hardcoded 3 SKUs por regex; `affiliate_url` da UI ignorado; `fetch-trends`/`vm_trends` desconectados; prompts são B2B "IA p/ agências", não venda de produto físico.
> 18	
> 19	**3 descasamentos centrais:** (1) a IA escreve sem saber qual produto vende; (2) não há gatilho recorrente (molde = cadência nurturing `next_run_at`+pg_cron, mas finita/lead/email); (3) o loop não fecha — desempenho passado nunca volta ao prompt.
> 20	
> 21	**STATUS: BoK 9/9 SELADA 2026-06-17** (nó `documentation_suite` `b3398294-aa75-4810-845b-3a15cfe802e7`, embedded 768d ✅; edge DERIVES_FROM `05cea16d` → marketing-hub `d5163fed`; 1889 LOC; ID space MR/BR-VA-001..008 · PR-VA-001..022 · FR-VA-001..021 · 8 OTD · 12 FMEA 4×RPN>100). Seed: `scripts/seed-viral-autopilot-bok-seal.ts`. **BoK Gate ABERTO** p/ código.
> 22	
> 23	**✅ FATIA 1 ENTREGUE + PROVADA EM PROD 2026-06-20** (commit `4af8b8b`, = passo 2 da rota "geração product-aware") — fecha R1/R4 nas 3 superfícies de TEXTO sem tocar cron (R2) nem o loop que LÊ optimization_policy (R3):
> 24	- **FR-VA-003** prompts product-aware (artigo/LinkedIn/X) featuring o produto escolhido; fallback B2B quando sem produto (backward-compat: campaign-run/intent-execute intactos).
> 25	- **FR-VA-004** `monetizeForProduct` (`_shared/affiliate.ts`) monetiza as 3 superfícies (não só artigo) determinístico por produto (não regex dos 3 SKUs); grava `affiliate_links.content_id = content_library.id` (ANTES sempre null — defeito-núcleo fechado). HTML inline-link/CTA · texto append-URL (LinkedIn/X). escapeHtml no name (DiD do /security-review).
> 26	- **FR-VA-016 metade-produto** orchestrate-content resolve `product_ids` do `vm_affiliate_products` (authoritative, descarta name/price do cliente), **sanitiza cada nome pelo sentinel** (Apify = dado externo → injeção, fail-closed por produto), grava em `pipeline_runs.metadata.products`. orchestrate-step lê e ramifica.
> 27	- **FR-VA-009** nova migration `creative_metrics` (`20260619140000`, aplicada+verificada: RLS SELECT-own · service-role-write default-deny · RESTRICTIVE no-delete · UNIQUE(content_variant_id,source) · 5 CHECKs; cycle_id NULL-able reservado p/ a fatia do cron, sem FK física ainda). Gerador escreve baseline source='organic' zeros por criativo (semeia R3).
> 28	- **UI** picker de produtos na `TriggerNode` (`useAffiliateProducts`, 3 SKUs do catálogo, 1º=★ primary) substitui o input de URL livre que era dropado. `runPipeline`/store mandam `product_ids`.
> 29	- **DESCOPES declarados:** imagem (FR-VA-013) — entregue na Fatia 1b (abaixo); cron/cadência (R2) + loop R3.
> 30	
> 31	**✅ FATIA 1b ENTREGUE + PROVADA 2026-06-20** (commit `ba5d281`, FR-VA-013 — imagem product-referenced):
> 32	- `generate-image` ganhou **dual-path auth** (service-role + `user_id` no body, espelha `publish-wordpress`; byte-equal bearer = fronteira) pra orchestrate-step invocá-la com service-key; **retorna o `path` do storage** (re-assinável) além do signed URL 1h.
> 33	- orchestrate-step: bloco de imagem **dentro do `article_generation`** (NÃO novo step na ladder — evita drift do stepsOrder), gated `hasProducts`, **FAIL-OPEN com status `skipped`** (não `error` — senão o finalize marcaria o run error). Guarda **PATH durável** em `content_library.media_url` (bucket `generated-images` é PRIVADO → re-assina na leitura; signed URL 1h morre antes do publish +1-2h). Sem migration, sem mudança de frontend, **sem cobrança extra** (imagem já no bundle de 10, billing.ts).
> 34	- **Correções materiais ao contrato:** `generate-image` é DALL·E **text-only** (sem image-to-image) → product-referenced = prompt descritivo (nome+categoria), NÃO o `image_url` como referência visual (deferido). Anexo no publish-social (LinkedIn/X/Meta) + featured-image WP = deferidos (publish-layer).
> 35	- **Prova (run `46a98963`):** auth 400(sem user_id)/401(não-service)/alcança-provider; step `image_generation` `skipped` (fail-open) com `article_generation` `done` e run NÃO-errado pela imagem; 3/3 affiliate_links content_id NON-NULL (zero regressão Fatia 1); delta saldo exatamente 10. /security-review SAFE 9/10 · tsc 0.
> 36	**🔬 DIAGNÓSTICO da saída visível 2026-06-20 (Sovereign pediu "destravar") — 3 blockers, causas raiz CRAVADAS materialmente:**
> 37	1. **WordPress publish falha (todo run) = Cloudflare bot-challenge.** `wp_site_url=https://www.mcorch.com` (já www canônico — NÃO é mais o 301). `GET /wp-json` → **403 `text/html` "Just a moment..."** com `cf-mitigated: challenge`, `server: cloudflare` — mesmo AUTENTICADO com as creds reais (Basic Auth). O CF desafia o request server-to-server da edge function (cliente não-browser) ANTES do WordPress; o `await wpRes.json()` no `publish-wordpress:133` lança na resposta HTML → catch 500 "Falha ao publicar... Verifique a conexão". **Credenciais WP estão OK.** **AÇÃO SOVEREIGN:** regra Cloudflare WAF **Skip** pro path `/wp-json/*` (idêntico ao que já fizeram pro `mcp.mcorch.com` — ver [[project_vision_mcp]]).
> 38	2. **Imagem nanobana = endpoint MORTO.** `api.nanobana.com` **não resolve DNS** (http=000). Qualquer `pref_image_provider=nanobana` sempre falha. Bug latente no `generate-image` (branch nanobana aponta pra domínio inexistente, comentado "Assuming standard proxy or mock"). **Recomendado:** remover nanobana como provider selecionável OU fiar endpoint real.
> 39	3. **Imagem openai = 2 bugs, 1 corrigido + 1 config de conta.** (a) **CORRIGIDO (commit `803f946`):** `generate-image` mandava `response_format:"b64_json"` → OpenAI 400 "Unknown parameter" (param removido pela OpenAI). Fix: remover param + tratar resposta url(dall-e-3 default)/b64/data-URI (baixa bytes da url) + surfacing `upstream`. (b) **AÇÃO SOVEREIGN:** a chave-PROJETO do Zero (`sk-proj`, `proj_rWo9VkBo6n9WQro93dzCZglr`) **não tem acesso a NENHUM modelo de imagem** (dall-e-2/3 "does not exist", gpt-image-1 "does not have access", models list sem image). Habilitar acesso a modelo de imagem no OpenAI dashboard (project → model access; gpt-image-1 exige org verification+billing) OU usar chave/projeto com acesso OU rota OpenRouter de imagem. A chave em si é VÁLIDA (`/v1/models`→200). Toggle pref nanobana→openai→nanobana usado no QA (restaurado). Cron/cadência (R2) + loop R3 (lê optimization_policy) = fatias seguintes, ainda gated no **SOP `docs/processes/autopilot-cron-identity.md` (Lei 2, OTD-VA-008)** ANTES da cadência.
> 40	- **Prova material (Lei 1):** E2E pago Usuário Zero run `158ba7fc` → 3 criativos product-aware (cada um cita Roborock + link rastreável), **3 affiliate_links content_id NON-NULL casando os 3 content_library.id**, 3 creative_metrics baseline, **delta saldo = exatamente 10**. /security-review SAFE · tsc 0 · 295 testes · picker validado oculamente 1920×1080 (preview local + sessão injetada). Edge fns deployadas (orchestrate-content 113.8kB · orchestrate-step 129.3kB), frontend buildado. **A run caiu p/ status `error` SÓ pelo wordpress_publish** (problema WP 301/config = ação Sovereign, ortogonal). SOP Lei 2 `docs/processes/viral-autopilot-product-aware-monetization.md`.
> 41	
> 42	**Validação Fase 6 = 4 rodadas adversariais** (workflow 4 críticos): R1 NO_GO (2 blockers+7 high) → R2 NO_GO (2 blockers, 1 que EU introduzi: refund por deduct negativo viola RPC anti-mint `20260603220000:45`) → R3 GO_WITH_FIXES → R4 GO_WITH_FIXES (síntese caiu por session-limit, críticos OK). **Lição:** cada "fix" meu deixou um resíduo que a rodada seguinte pegou — verificação adversarial + grep determinístico foram essenciais; não auto-declarar GO.
> 43	
> 44	**Decisões de design cravadas pela validação (entram na implementação):**
> 45	- **Identidade do cron (SEC-VA-CRIT-01):** `verify_jwt=false` → `autopilot-run`/`-analyze`/`-collect`/`-cadence-cron` PROVAM service-role in-function (`Authorization === 'Bearer '+SB_SECRET_KEY`, padrão `orchestrate-step:50-53`) ANTES de confiar no header `x-autopilot-user-id` (server-trusted = `autopilot_plans.user_id`, nunca do body). `orchestrate-content` estendida p/ aceitar esse caminho + `prepaid`. SOP `edge-jwt-identity-verification`.
> 46	- **Custo/atomicidade:** `projected = N_runs×10 + 2`, `N_runs = produtos × redes × ab_variants` (imagem JÁ no bundle de 10, `billing.ts:16-21`, NÃO somar). **RPC `begin_autopilot_cycle`** (advisory lock por user_id) = cap diário (FR-VA-021) + cap por ciclo + pré-débito atômico ÚNICO + open, anti-TOCTOU. **RPC `finalize_autopilot_cycle`** credita refund via `add_mco_coins` (POSITIVO ledgered, espelha `finalize_vision_job`; NUNCA deduct negativo). Sub-runs `prepaid` (não self-bill).
> 47	- **`autopilot-analyze` inline pós-ciclo** (não 3º cron); tenant derivado de `previous_cycle_id` (anti-IDOR, nunca do body); 2 mco só se `has_real_data` (0 senão).
> 48	- **`content_variant_id` = `content_library.id`** (ref. LÓGICA, sem FK física — retenção independente); grava `affiliate_links.content_id`. **FK COMPOSTA tenant-escopada** `(plan_id,user_id)`/`(cycle_id,user_id)` (espelha Marketing Hub) + `user_id` FK real + RESTRICTIVE no-delete nas 3 tabelas.
> 49	- **`campaign_metrics` DEPRECADA** p/ o módulo → `creative_metrics` é a unidade canônica (sem ETL). **`optimization_policy` com `scope='viral_autopilot:<plan_id>'`** (desambigua do `self-optimize` legado). KPI lift fallback p/ cliques de afiliado quando orgânico ausente.
> 50	
> 51	**4 decisões Sovereign (parametrizam o BoK):**
> 52	1. **BoK Gate** = `/bok-scribe` suite-mãe NOVO `viral-autopilot` unificando R1-R4 (R2 cadência + R3 loop não têm FR em suite algum).
> 53	2. **MVP** = texto+imagem nas redes ATUAIS (WP/LinkedIn/X) primeiro; vídeo 9:16 + TikTok/IG/YT = fase 2.
> 54	3. **Sinal R3** = combo completo (cliques afiliado [já temos] + engajamento orgânico [coletor novo] + receita postback ML).
> 55	4. **Produtos** = 3 SKUs semente (Roborock S8 / Samsung Neo QLED 8K / Family Hub) por ora, escalar catálogo depois.
> 56	
> 57	**Rota recomendada (8 passos, do maior alavancagem):** 1 BoK gate → 2 geração product-aware (honrar param produto, monetizar TODO formato c/ content_variant_id) → 3 reconectar `fetch-trends`/`vm_affiliate_products` à pauta → 4 cadência 3 dias (generalizar primitiva nurture, auto-refill) → 5 coletor de engajamento por post → 6 fechar loop R3 (gerador lê `optimization_policy`) → 7 mídia viral 9:16 (fase 2) → 8 provar postback ML real (OTD-ML-MP-PER-USER).
> 58	
> 59	**Riscos:** custo descontrolado do cron autônomo (precisa teto mcoCoins + kill-switch por ciclo); R3 pode virar "auto-melhoria teatral" se rodar sem dado real; postback ML nunca provado em prod.
> 60	
> 61	Suites a referenciar/promover: [[project_marketing_hub_v2]] (campaign-run executor), mercado-livre-api FR-ML-*, post-engine FR-PE-*, viral-daily-canvas FR-VDC-*. Relacionado: [[project_orchestrate_pipeline_repair]] (pipeline async), [[project_authenticated_browser_operator]] (atribuição ML), [[project_mcoin_calibration]] (custo por run).
> 62	
> ```

## 🤖 Claude *(17:12:15)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for slug in viral-autopilot vision-mcp mcorch-constellation; do\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug \u2014 BoK complete\" || echo \"\u26a0\ufe0f $slug \u2014 missing: ${missing[*]}\"\ndone\necho \"--- scratch contents ---\"\nls -la scratch/ 2>/dev/null",
  "description": "BoK gate check + scratch contents"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✅ viral-autopilot — BoK complete
> ✅ vision-mcp — BoK complete
> ✅ mcorch-constellation — BoK complete
> --- scratch contents ---
> total 8
> drwxr-xr-x  2 ubuntu ubuntu 4096 Jun  7 14:41 .
> drwx------ 30 ubuntu ubuntu 4096 Jun 20 11:56 ..
> ```

## 🤖 Claude *(17:12:26)*


## 🤖 Claude *(17:12:48)*

Tudo coletado e verificado. Worktree limpo, tsc sem erros, infra saudável. Segue o brief.

```
═══════════════════════════════════════════════════════════
  HANDSON — Viral Autopilot Fatias 1 + 1b (selada 2026-06-20 · v6.43.0)
═══════════════════════════════════════════════════════════
```

🏁 **ESTADO ATUAL**
Fase selada: **Viral Autopilot Fatias 1 + 1b** — gerador product-aware + monetização cross-surface + imagem fail-open. BoK Gate **ABERTO**.
Últimos commits:
- `44e5887` — chore(sprint): registra v6.43.0
- `7e6fcd5` — docs(handoff): seal Fatias 1 + 1b
- `803f946` — fix(generate-image): OpenAI rejeita `response_format` + trata url/b64
- `ba5d281` — feat: Fatia 1b — imagem product-referenced (FR-VA-013)
- `4af8b8b` — feat: Fatia 1 — gerador product-aware + monetização cross-surface

📂 **MUDANÇAS PENDENTES**
Worktree limpo ✅ · `scratch/` limpo ✅

🏗️ **INFRA** (todos saudáveis)
mcorch_chroma: Up 5 days (healthy) — Chroma API v2: ✅ heartbeat vivo
mcorch_claude_mem: Up 5 days (healthy) · mcorch_vision_mcp: Up 3 days (healthy)
mega-brain-daemon/webhook: healthy · mega-brain-dashboard: up

🧠 **KNOWLEDGE MESH**
**8934 nós** (último seal: handoff `385d3dd5` embedded 768d) · 100% embedded · HNSW cosine 768d

🔧 **TYPESCRIPT** — Zero erros ✅

📚 **BoK SUITES** (relevantes ao trabalho ativo)
Complete: ✅ `viral-autopilot` · ✅ `vision-mcp` · ✅ `mcorch-constellation` (21 suítes no total em `docs/bok/`)
Seal node ativo: `viral-autopilot` → `b3398294` (documentation_suite, 768d) · DERIVES_FROM → marketing-hub `d5163fed`
**Sem gate alert** — o trabalho pendente está coberto por BoK selada.

📌 **SPRINT**
Goal: *Distribuição social autônoma operacional* — pipeline publica LinkedIn auto, Twitter quando tier subir, Instagram pós App Review.
Top gap: **Viral Autopilot Fatia 2** (cron/cadência R2) — bloqueada pelo gate Lei 2 (SOP ausente).

⚡ **PRÓXIMOS PASSOS** (prioridade)
1. **Fatia 2 — cadência R2** (passo 4 da rota): ⚠️ **gate Lei 2 primeiro** — escrever `docs/processes/autopilot-cron-identity.md` (OTD-VA-008) antes de qualquer código de cron. Design já cravado pela validação adversarial: cron prova service-role in-function (`Bearer SB_SECRET_KEY`) antes de confiar `x-autopilot-user-id`; RPCs `begin_autopilot_cycle` (advisory-lock + pré-débito atômico) + `finalize_autopilot_cycle` (refund crédito-positivo, nunca deduct negativo); FK composta tenant-escopada.
2. **Loop R3** (passo 6): gerador lê `optimization_policy` scope=`viral_autopilot:<plan_id>` + `autopilot-analyze` inline pós-ciclo.
3. **Anexo de imagem no publish-layer** (LinkedIn/X/Meta + featured WP) — a Fatia 1b já guarda o PATH durável em `content_library.media_url`; falta fiá-lo no publish.

⚠️ **ALERTAS**
Nenhum bloqueador de código. **2 ações Sovereign-side** travam a saída visível (causas cravadas materialmente, ortogonais ao código):
- **WordPress publish** → Cloudflare bot-challenge no `/wp-json` (403 "Just a moment", mesmo autenticado). Ação: regra WAF **Skip** pro `/wp-json/*` (idêntica à de `mcp.mcorch.com`). Creds WP estão OK.
- **Imagem OpenAI** → chave-projeto do Zero sem acesso a nenhum modelo de imagem. Ação: habilitar model access no OpenAI dashboard. (nanobana = DNS morto, endpoint inexistente — candidato a remover.)

```
═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════
```

O caminho de maior alavancagem é a **Fatia 2 (cadência R2)**, mas ela exige primeiro o SOP `autopilot-cron-identity.md` (Lei 2). Quer que eu comece pelo SOP, ou prefere atacar o **anexo de imagem no publish-layer** (não tem gate, destrava saída visual assim que as 2 ações Sovereign estiverem feitas)?

## 👤 User *(17:18:17)*

ótimo vamos nessa gogo

## 🤖 Claude *(17:19:18)*


## 🤖 Claude *(17:19:23)*

Interpretei como o caminho que recomendei: **Fatia 2 (cadência R2)**, começando pelo gate Lei 2 — o SOP `autopilot-cron-identity.md`. Se você queria o anexo de imagem no publish-layer, me corrija e eu pivoto. Seguindo no Closed-Loop: **mapeamento do contrato vivo → escopo → SOP → código → /security-review → deploy → E2E → seal**.

**ORO triplet desta task:**
- **Operator:** MCORCH Master Execution Agent
- **Reviewer:** Sovereign (Gabriel) + `/security-review` independente em cada migration/edge fn
- **Owner:** Sovereign — blast radius = cron autônomo gastando carteira do tenant sem mão humana no loop (precisa teto mcoCoins + prova de identidade server-trusted)

Antes de escrever uma linha do SOP, mapeio o contrato vivo (prática que nas fatias anteriores pegou correções materiais). Disparando reconhecimento em paralelo.

## 🤖 Claude *(17:19:24)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Viral Autopilot Fatia 2 \u2014 cad\u00eancia R2",
  "summary": "Mapeamento do contrato vivo + SOP Lei 2 [[autopilot-cron-identity|autopilot-cron-identity]] (gate antes do c\u00f3digo de cron)"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Viral Autopilot Fatia 2 — cadência R2". Continue your current work.'}]
> ```

## 🤖 Claude *(17:19:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== FUNCTIONS (autopilot/nurture/auto-publish/orchestrate) ===\"; ls supabase/functions/ | grep -iE 'autopilot|nurture|auto.?publish|orchestrate' || echo \"none\"\necho \"=== MIGRATIONS (autopilot/anti-mint 20260603220000/creative_metrics/add_mco) ===\"; ls supabase/migrations/ | grep -iE 'autopilot|20260603220000|creative_metric|add_mco|begin_|finalize_' || echo \"none matched\"\necho \"=== PROCESSES (autopilot/cron/jwt/nurtur/orchestrate) ===\"; ls docs/processes/ | grep -iE 'autopilot|cron|jwt|nurtur|orchestrate' || echo \"none\"\necho \"=== config.toml verify_jwt blocks ===\"; grep -nE 'verify_jwt|\\[functions\\.' supabase/config.toml 2>/dev/null | grep -iE 'autopilot|nurture|orchestrate|verify_jwt' | head -40 || echo \"no config.toml hits\"",
  "description": "Inventory functions, migrations, SOPs, config.toml"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === FUNCTIONS (autopilot/nurture/auto-publish/orchestrate) ===
> auto-publish
> intent-orchestrate
> nurture-cron
> nurture-dispatch
> orchestrate-content
> orchestrate-step
> === MIGRATIONS (autopilot/anti-mint 20260603220000/creative_metrics/add_mco) ===
> 20260603220000_secure_ledger_rpcs.sql
> 20260619140000_viral_autopilot_creative_metrics.sql
> === PROCESSES (autopilot/cron/jwt/nurtur/orchestrate) ===
> [[edge-jwt-identity-verification|edge-jwt-identity-verification]].md
> [[orchestrate-async-pipeline|orchestrate-async-pipeline]].md
> [[viral-autopilot-product-aware-monetization|viral-autopilot-product-aware-monetization]].md
> === config.toml verify_jwt blocks ===
> 7:verify_jwt = false
> 9:verify_jwt = false
> 11:verify_jwt = false
> 13:verify_jwt = false
> 15:verify_jwt = false
> 16:[functions.orchestrate-content]
> 17:verify_jwt = false
> 18:[functions.orchestrate-step]
> 19:verify_jwt = false
> 20:[functions.nurture-dispatch]
> 21:verify_jwt = false
> 22:[functions.nurture-cron]
> 23:verify_jwt = false
> 24:[functions.intent-orchestrate]
> 25:verify_jwt = false
> 27:verify_jwt = false
> 29:verify_jwt = false
> 31:verify_jwt = false
> 33:verify_jwt = false
> 35:verify_jwt = false
> 37:verify_jwt = false
> 39:verify_jwt = false
> 41:verify_jwt = false
> 43:verify_jwt = false
> 45:verify_jwt = false
> 47:verify_jwt = false
> 50:verify_jwt = true
> 55:verify_jwt = false
> 58:verify_jwt = false
> 61:verify_jwt = false
> 64:verify_jwt = false
> 67:verify_jwt = false
> 70:verify_jwt = false
> 73:verify_jwt = false
> 76:verify_jwt = false
> 79:verify_jwt = false
> ```

## 🤖 Claude *(17:19:29)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/[[edge-jwt-identity-verification|edge-jwt-identity-verification]].md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# SOP: Edge Function JWT Identity Verification (verify_jwt=false)
> 2	
> 3	**Status:** ACTIVE · v1.0 · 2026-05-30
> 4	**Owner:** Sovereign (Gabriel Zarattini)
> 5	**Survival Law 2 compliance:** Escrita ANTES do fix de verificação de assinatura em `check-video-status`, `generate-video`, `generate-video-script`, `list-provider-models` (fecha a impersonação cross-tenant via JWT não-verificado).
> 6	**Canonical directive:** `CLAUDE.md > Architecture > "API Tenancy Model — Per-User Credentials"` · `.claude/rules/survival.md > Law 1 (Materiality)`
> 7	
> 8	---
> 9	
> 10	## Context
> 11	
> 12	Funções Edge marcadas com `verify_jwt = false` em `supabase/config.toml` **não passam pela validação de JWT do gateway** (Kong). A razão é material e confirmada: o projeto migrou para **chaves de assinatura assimétricas ES256** (JWKS público em `https://bcyvddsykvehvpwstlfa.supabase.co/auth/v1/.well-known/jwks.json`, P-256, `kid d073a3db-…`), enquanto a `SUPABASE_SERVICE_ROLE_KEY` permanece um JWT **legacy HS256**. O gateway, configurado para o segredo HS256, **rejeita** tokens de sessão ES256 dos usuários → daí `verify_jwt=false` foi adotado como workaround (comentários `"bypass ES256 gateway"`).
> 13	
> 14	Com o gateway desligado, a **resolução de identidade vira responsabilidade exclusiva da própria função**. A implementação original fazia:
> 15	
> 16	```ts
> 17	// ANTI-PATTERN (proibido) — decodifica SEM verificar a assinatura
> 18	const { data: { user } } = await supabase.auth.getUser();
> 19	userId = user?.id || extractUserIdFromJWT(authHeader); // <- atob(payload).sub cego
> 20	```
> 21	
> 22	`extractUserIdFromJWT` lê `payload.sub` via `atob` **sem verificar a assinatura**. Como o gateway também não verifica (`verify_jwt=false`), um atacante forja um JWT com 3 partes onde o payload base64 contém `{"sub":"<victim-uuid>"}` e a assinatura é lixo: `getUser()` rejeita (assinatura inválida → null), o fallback retorna o `sub` da vítima, e a função **executa como a vítima** — lendo e gastando `user_api_keys` (gemini/openrouter/replicate/google), mcoCoins e conteúdo de qualquer tenant. As checagens `admin.getUserById(userId)` presentes em 3 das 4 funções só provam que a **vítima existe** (o que o atacante quer) — é teatro de identidade, não gate de identidade.
> 23	
> 24	**Por que importa (multi-tenant readiness):** isolamento de credencial por tenant · atribuição de custo (mcoCoins/quota de API) correta · risco financeiro isolado (credencial de um tenant não vaza para outro) · LGPD. Viola diretamente o "API Tenancy Model" do `CLAUDE.md`.
> 25	
> 26	---
> 27	
> 28	## ORO triplet
> 29	
> 30	- **Operator:** MCORCH Master Execution Agent (fix) + Edge runtime Deno (execução por request)
> 31	- **Reviewer:** Sovereign (Gabriel) — aprova o diff + valida a prova local e o exploit test pós-deploy
> 32	- **Owner:** Sovereign — blast radius = impersonação cross-tenant em 4 endpoints de vídeo/modelos (roubo de API keys + mcoCoins + leitura de conteúdo)
> 33	
> 34	---
> 35	
> 36	## Operator (quem chama hoje — material)
> 37	
> 38	| Caller | Arquivo | Token enviado |
> 39	|--------|---------|---------------|
> 40	| Frontend — Video Editor | `src/pages/VideoEditorPage.tsx` | `Bearer ${supabase.auth.getSession().access_token}` (ES256 de sessão) |
> 41	| Frontend — Content Library | `src/pages/ContentLibraryPage.tsx` | idem |
> 42	
> 43	**Não existe** chamador server-side, cron, `orchestrate-content`, webhook ou script `~/.openclaw` para estas 4 funções (varredura repo-wide 2026-05-30). O "chamador ES256" é o **browser** com token de sessão Supabase padrão — NÃO um orquestrador soberano mintando tokens próprios.
> 44	
> 45	---
> 46	
> 47	## Resolution order (canonical — para funções verify_jwt=false)
> 48	
> 49	| # | Camada | Fonte | Permitido em |
> 50	|---|--------|-------|--------------|
> 51	| 1 | **getUser()** | `supabase.auth.getUser()` com `Authorization` do request → `user.id` (GoTrue valida a assinatura server-side) | SEMPRE (caminho primário, fluxo user-facing) |
> 52	| 2 | **JWKS verify (fallback)** | `verifyJwtAndGetUserId(authHeader)` → `jwtVerify(token, createRemoteJWKSet(<project>/auth/v1/.well-known/jwks.json))` → confia em `payload.sub` **SOMENTE** após a assinatura ES256 verificar | SEMPRE que (1) retornar null mas o token for legitimamente assinado pelo projeto |
> 53	| 3 | **Service-role gate** (padrão irmão) | `authHeader === \`Bearer ${SERVICE_ROLE_KEY}\`` → confia em `body.user_id` | SÓ em funções com chamador server-side/cron real (ex.: `publish-social`, `publish-wordpress`, auto-publish). **N/A** para as 4 funções deste SOP (sem caller server-side). |
> 54	| 4 | **Hard failure** | — | HTTP 401 `{ error: "Token inválido" }`. **NUNCA** decodificar `sub` sem verificar assinatura. |
> 55	
> 56	**Regra de ouro:** confiar em um claim `sub` só é permitido depois de **uma** das provas: (a) `getUser()` retornou esse user, OU (b) a assinatura ES256 do token verificou contra o JWKS do projeto, OU (c) o caller provou posse da `SERVICE_ROLE_KEY` (e aí o `user_id` vem do body, não do JWT).
> 57	
> 58	---
> 59	
> 60	## Sequence (fix aplicado — Option 1 cirúrgica)
> 61	
> 62	Em cada uma das 4 funções:
> 63	
> 64	1. Importar `{ jwtVerify, createRemoteJWKSet }` de `https://esm.sh/jose@5.9.6`.
> 65	2. Criar `const SUPABASE_JWKS = createRemoteJWKSet(new URL(\`${Deno.env.get("SUPABASE_URL")}/auth/v1/.well-known/jwks.json\`))` em module scope (cacheado entre invocações; fetch lazy no primeiro verify).
> 66	3. Substituir o corpo de `extractUserIdFromJWT` por `verifyJwtAndGetUserId(authHeader)` async:
> 67	   ```ts
> 68	   async function verifyJwtAndGetUserId(authHeader: string | null): Promise<string | null> {
> 69	     if (!authHeader) return null;
> 70	     const token = authHeader.replace("Bearer ", "").trim();
> 71	     if (!token) return null;
> 72	     try {
> 73	       const { payload } = await jwtVerify(token, SUPABASE_JWKS);
> 74	       return typeof payload.sub === "string" ? payload.sub : null;
> 75	     } catch {
> 76	       return null; // assinatura inválida/expirada/malformada → rejeita
> 77	     }
> 78	   }
> 79	   ```
> 80	4. Trocar o call-site `user?.id || extractUserIdFromJWT(authHeader)` por `user?.id || await verifyJwtAndGetUserId(authHeader)` (e o else-branch equivalente em `generate-video-script` / `list-provider-models`).
> 81	5. **Manter** `verify_jwt=false` em `config.toml` (o gateway não verifica ES256; a função agora é o gate real) e **manter** `getUser()` como caminho primário.
> 82	
> 83	---
> 84	
> 85	## Verification gates
> 86	
> 87	| Gate | Check | Pass criterion |
> 88	|------|-------|----------------|
> 89	| **G1 — Local mechanism (jose, Deno)** | `~/.deno/bin/deno run --allow-net scripts/qa/test-es256-jwt-verification.ts` | Token assinado com keypair ES256 local → `sub` retornado; assinatura adulterada → `null`; token forjado base64 (`{sub}` + sig lixo) → `null` |
> 90	| **G2 — Real-JWKS negative** | Mesmo teste, ramo que verifica o token forjado contra o **JWKS real do projeto** | `null` (a exploração real é rejeitada) |
> 91	| **G3 — Deploy materiality** | `npx supabase functions deploy <name>` + `npx supabase functions list` | VERSION de cada função **incrementa** vs. baseline |
> 92	| **G4 — Post-deploy exploit (prod)** | `curl -X POST <fn-url>` com `Authorization: Bearer <forged>` + `apikey: <anon>` | HTTP **401** (antes do fix: 200/202/processa como vítima) |
> 93	| **G5 — Positive (prod)** | Frontend logado chama a função OU Sovereign cola um `access_token` fresco para teste | Resposta normal (200/202) — sem regressão para o caller legítimo |
> 94	
> 95	G5 exige um token de sessão válido (não mintável sem credenciais de usuário) → **brain-without-hands** declarado: validar via UI logada em `login.mcorch.com` (Ctrl+Shift+R) ou token colado pelo Sovereign.
> 96	
> 97	---
> 98	
> 99	## Recovery path
> 100	
> 101	- **jose não resolve no deploy** (esm.sh indisponível / build Deno incompatível): G1 já roda o mesmo import localmente antes do deploy → se G1 passou, o import é válido. Se mesmo assim o deploy falhar no bundle, fazer rollback (abaixo) e fixar versão alternativa (`jose@5.x`) ou migrar para `djwt`.
> 102	- **JWKS inacessível em runtime** (raro — mesma infra Supabase): `jwtVerify` lança → `verifyJwtAndGetUserId` retorna `null` → 401. **Fail-closed** (nega acesso), nunca fail-open. Caller legítimo seria impactado, mas nenhuma impersonação ocorre. Mitigação: `createRemoteJWKSet` cacheia o JWKS após o primeiro fetch.
> 103	- **Rollback de deploy:** `git checkout HEAD~1 -- supabase/functions/<name>/index.ts && npx supabase functions deploy <name>` (re-deploya a versão anterior). Confirmar VERSION na `functions list`.
> 104	- **Regressão no caller legítimo (G5 falha):** rollback imediato dos 4; investigar se `getUser()` estava de fato carregando o fluxo e se o token de sessão não verifica contra o JWKS (improvável — JWKS é a chave pública do próprio GoTrue que assinou).
> 105	
> 106	---
> 107	
> 108	## Success signal
> 109	
> 110	- G1+G2 verdes localmente (output literal do `deno run` colado no handoff — Lei 1).
> 111	- G3: VERSION das 4 funções incrementada (output literal de `functions list` antes/depois).
> 112	- G4: `401` literal no exploit test contra produção para as 4 funções.
> 113	- G5: caller legítimo funcionando (UI ou token colado).
> 114	- `extractUserIdFromJWT` (atob cego) **não existe mais** em nenhuma das 4 funções (`rg extractUserIdFromJWT supabase/functions` → vazio).
> 115	
> 116	---
> 117	
> 118	## Anti-patterns proibidos
> 119	
> 120	- ❌ `atob(payload).sub` (ou qualquer decode) usado como identidade **sem** verificar a assinatura.
> 121	- ❌ `admin.getUserById(sub)` tratado como prova de identidade (só prova existência da vítima).
> 122	- ❌ Fail-open: em erro de verificação, assumir uma identidade default ou seguir sem `userId`.
> 123	- ❌ Expor `SERVICE_ROLE_KEY` ao browser para usar o gate da camada 3 (catastrófico — o caller destas 4 funções é o browser).
> 124	- ❌ Setar `verify_jwt=true` no gateway para estas funções (rejeitaria os tokens ES256 legítimos → quebra o frontend).
> 125	
> 126	---
> 127	
> 128	## Sibling reference
> 129	
> 130	- Service-role gate correto (camada 3): `supabase/functions/publish-wordpress/index.ts` (linhas ~26-47) e `supabase/functions/publish-social/index.ts` — usados por callers server-side/cron reais (auto-publish). Padrão diferente, mesma diretiva (API Tenancy).
> 131	
> ```

## 🤖 Claude *(17:19:31)*


🛠️ **Tool Call**: `Grep`
```json
{
  "pattern": "SB_SECRET_KEY|service_role|Bearer|x-autopilot-user-id|verify_jwt",
  "path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/orchestrate-step/index.ts",
  "output_mode": "content",
  "-n": "true",
  "head_limit": "30"
}
```

> **Tool Result (Grep)** - ❌ Error
>
> ```
> <tool_use_error>Error: No such tool available: Grep. Grep is not available in this session — search file contents with `grep` via the Bash tool instead.</tool_use_error>
> ```

## 🤖 Claude *(17:19:32)*


🛠️ **Tool Call**: `Grep`
```json
{
  "pattern": "OTD-VA-008|x-autopilot|service-role|cron|cadence|begin_autopilot|finalize_autopilot|verify_jwt",
  "path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot",
  "output_mode": "files_with_matches"
}
```

> **Tool Result (Grep)** - ❌ Error
>
> ```
> <tool_use_error>Error: No such tool available: Grep. Grep is not available in this session — search file contents with `grep` via the Bash tool instead.</tool_use_error>
> ```

## 🤖 Claude *(17:19:50)*


## 🤖 Claude *(17:19:52)*

`grep` tool não existe nesta sessão — uso `grep` via Bash (com `-E`, é o ugrep-shim). Reconhecimento confirma: **nenhuma função `autopilot-*`, nenhuma tabela `autopilot_plans/cycles`, nenhum SOP `autopilot-cron-identity.md`** ainda — a Fatia 2 cria tudo isso, e o gate Lei 2 está de fato aberto. Aprofundando nos contratos vivos que o SOP precisa ancorar.

## 🤖 Claude *(17:19:53)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260603220000_secure_ledger_rpcs.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- SECURITY P0 ([[schema-drift-audit|schema-drift-audit]] 2026-06-03, adjacent finding — Sovereign GO "fix completo"): lock down the
> 2	-- mcoCoin ledger RPCs against unauthorized minting / cross-tenant balance manipulation.
> 3	--
> 4	-- Discovered while auditing SECURITY DEFINER functions: all three ledger RPCs grant EXECUTE to PUBLIC/anon/
> 5	-- authenticated and trust a caller-supplied p_user_id with no auth.uid() check. Because they are SECURITY DEFINER
> 6	-- (bypass RLS) and exposed via PostgREST, any logged-in user could call them directly, skipping the edge functions
> 7	-- and their caps:
> 8	--   * award_mco_coins(p_user_id:=self, p_amount:=1000) → mint 1000 mcoCoins per call, unlimited.
> 9	--   * add_user_score(self, big)                        → self-inflate score → coins (100:1).
> 10	--   * deduct_mco_coins(p_amount:=-1000)                → `balance - (-1000)` = mint; the `balance >= p_amount`
> 11	--                                                         guard is `>= -1000` (always true). Ledger stores -(-1000)=+1000.
> 12	--   * deduct_mco_coins(p_user_id:=victim, ...)         → drain another tenant's balance.
> 13	-- (Same exposure model the team's own async_orchestrate_step fix closed by REVOKE-ing public/anon/authenticated.)
> 14	--
> 15	-- FIX, legit paths preserved:
> 16	--   * award_mco_coins / add_user_score are EDGE-ONLY (award-mco-coins / autonomic-action call them via the
> 17	--     service_role admin client; no client code calls them) → REVOKE from public/anon/authenticated, keep service_role.
> 18	--   * deduct_mco_coins IS called by the client (src/lib/billing.ts) for the user's OWN spends → keep the
> 19	--     `authenticated` grant but add internal guards (body otherwise reproduced VERBATIM: SET search_path=public,
> 20	--     row lock, GREATEST clamp, NOT FOUND check, negative-amount ledger insert):
> 21	--       - reject p_amount <= 0 (kills the negative-amount mint),
> 22	--       - non-service_role callers may only deduct from their OWN profile
> 23	--         (auth.role() <> 'service_role' AND p_user_id <> auth.uid() → 42501). service_role (edge fns:
> 24	--         orchestrate-content, canvas-execute, campaign-run, nurture-dispatch) stays exempt.
> 25	--     NOTE: the exemption keys on auth.role()='service_role', NOT on a NULL uid — anon also has a NULL uid, so anon
> 26	--     is additionally REVOKE-d from deduct (anon never legitimately spends).
> 27	
> 28	-- ── award_mco_coins → edge-only, revoke client reach ────────────────────────────────────────────────────────
> 29	REVOKE EXECUTE ON FUNCTION public.award_mco_coins(uuid, integer, text, jsonb) FROM PUBLIC, anon, authenticated;
> 30	GRANT  EXECUTE ON FUNCTION public.award_mco_coins(uuid, integer, text, jsonb) TO service_role;
> 31	
> 32	-- ── add_user_score → edge-only, revoke client reach ────────────────────────────────────────────────────────
> 33	REVOKE EXECUTE ON FUNCTION public.add_user_score(uuid, integer) FROM PUBLIC, anon, authenticated;
> 34	GRANT  EXECUTE ON FUNCTION public.add_user_score(uuid, integer) TO service_role;
> 35	
> 36	-- ── deduct_mco_coins → client-callable; add sign + own-tenant guards ────────────────────────────────────────
> 37	CREATE OR REPLACE FUNCTION public.deduct_mco_coins(p_user_id uuid, p_amount numeric, p_action text DEFAULT 'spend'::text, p_context jsonb DEFAULT '{}'::jsonb)
> 38	 RETURNS void
> 39	 LANGUAGE plpgsql
> 40	 SECURITY DEFINER
> 41	 SET search_path TO 'public'
> 42	AS $function$
> 43	BEGIN
> 44	  -- Guard 1: no negative/zero deduction (a negative amount would ADD balance = mint).
> 45	  IF p_amount IS NULL OR p_amount <= 0 THEN
> 46	    RAISE EXCEPTION 'Valor de débito de mcoCoins deve ser positivo';
> 47	  END IF;
> 48	
> 49	  -- Guard 2: a non-service_role caller may only deduct from its OWN profile (blocks cross-tenant drain).
> 50	  -- NULL-safe `IS DISTINCT FROM` (codebase standard — see 20260602150000) so a NULL role/uid fails CLOSED.
> 51	  IF auth.role() IS DISTINCT FROM 'service_role' AND p_user_id IS DISTINCT FROM auth.uid() THEN
> 52	    RAISE EXCEPTION 'cannot deduct mcoCoins for another user' USING ERRCODE = '42501';
> 53	  END IF;
> 54	
> 55	  -- Force row locking on the profile row to block concurrent executions
> 56	  PERFORM 1 FROM public.profiles WHERE id = p_user_id FOR UPDATE;
> 57	
> 58	  UPDATE public.profiles
> 59	     SET mco_balance = GREATEST(0, mco_balance - p_amount)
> 60	   WHERE id = p_user_id
> 61	     AND mco_balance >= p_amount;
> 62	
> 63	  IF NOT FOUND THEN
> 64	    RAISE EXCEPTION 'Saldo mcoCoins insuficiente para completar a operação';
> 65	  END IF;
> 66	
> 67	  -- Ledger entry. amount stored as NEGATIVE for spends.
> 68	  INSERT INTO public.mcoin_transactions (user_id, action, amount, context)
> 69	  VALUES (p_user_id, p_action, -p_amount::integer, p_context);
> 70	END;
> 71	$function$;
> 72	
> 73	REVOKE EXECUTE ON FUNCTION public.deduct_mco_coins(uuid, numeric, text, jsonb) FROM PUBLIC, anon;
> 74	GRANT  EXECUTE ON FUNCTION public.deduct_mco_coins(uuid, numeric, text, jsonb) TO authenticated, service_role;
> 75	
> ```

## 🤖 Claude *(17:19:54)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/orchestrate-step/index.ts",
  "limit": 90
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	const corsHeaders = {
> 2	  "Access-Control-Allow-Origin": "*",
> 3	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 4	  "Access-Control-Allow-Headers":
> 5	    "authorization, x-client-info, apikey, content-type, x-user-token, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version",
> 6	};
> 7	
> 8	import { createClient } from "https://esm.sh/@supabase/supabase-js@2.49.1";
> 9	import { fetchLLMWithFallback } from "../_shared/llm-fallback.ts";
> 10	import { monetizeContent, monetizeForProduct, type ChosenProduct } from "../_shared/affiliate.ts";
> 11	
> 12	// Content length/structure validation
> 13	const CONTENT_MIN_LENGTH: Record<string, number> = { article: 500, linkedin: 50, twitter_thread: 30 };
> 14	function validateContent(type: string, content: string): { valid: boolean; reason: string } {
> 15	  const trimmed = content.trim();
> 16	  if (!trimmed) return { valid: false, reason: "empty_content" };
> 17	  const min = CONTENT_MIN_LENGTH[type] ?? 30;
> 18	  if (trimmed.length < min) return { valid: false, reason: `too_short:${trimmed.length}/<${min}` };
> 19	  return { valid: true, reason: "ok" };
> 20	}
> 21	
> 22	function utmTag(platform: string, utmCampaign: string, topic: string, baseUrl?: string) {
> 23	  const params = `utm_source=${platform}&utm_medium=social&utm_campaign=${utmCampaign}&utm_term=${encodeURIComponent(topic.slice(0, 50))}`;
> 24	  return baseUrl ? `${baseUrl}${baseUrl.includes("?") ? "&" : "?"}${params}` : params;
> 25	}
> 26	
> 27	function getNextStep(currentStep: string, platforms: string[]): string | null {
> 28	  const stepsOrder = ["article_generation", "wordpress_publish", "linkedin_post", "twitter_thread", "knowledge_mesh"];
> 29	  const currentIdx = stepsOrder.indexOf(currentStep);
> 30	  
> 31	  for (let i = currentIdx + 1; i < stepsOrder.length; i++) {
> 32	    const candidate = stepsOrder[i];
> 33	    if (candidate === "article_generation" || candidate === "wordpress_publish") {
> 34	      if (platforms.includes("wordpress")) return candidate;
> 35	    } else if (candidate === "linkedin_post") {
> 36	      if (platforms.includes("linkedin")) return candidate;
> 37	    } else if (candidate === "twitter_thread") {
> 38	      if (platforms.includes("twitter")) return candidate;
> 39	    } else if (candidate === "knowledge_mesh") {
> 40	      return candidate; // Always run the final mesh step
> 41	    }
> 42	  }
> 43	  return null;
> 44	}
> 45	
> 46	// ─── Viral Autopilot Fatia 1 — product-aware prompt builders (FR-VA-003) ───────────────────────────────────
> 47	// When the run carries chosen products, the 3 B2B prompts are replaced by a consumer viral-hook framework
> 48	// (HOOK → VALUE → CTA) that features the chosen product. With NO products, the legacy B2B prompts are used
> 49	// verbatim (backward compatibility — campaign-run / intent-execute / topic-only runs are unchanged).
> 50	
> 51	function productBrief(products: ChosenProduct[]): string {
> 52	  const p = products[0];
> 53	  if (!p) return "";
> 54	  const priceNum = p.price != null ? Number(p.price) : NaN;
> 55	  const price = !Number.isNaN(priceNum) ? ` (aprox. R$ ${priceNum.toLocaleString("pt-BR")})` : "";
> 56	  const cat = p.category ? `, categoria ${p.category}` : "";
> 57	  let brief = `Produto em destaque: ${p.name}${price}${cat}.`;
> 58	  const others = products.slice(1).map((x) => x.name).filter(Boolean);
> 59	  if (others.length) brief += ` Produtos relacionados que podem ser citados: ${others.join(", ")}.`;
> 60	  return brief;
> 61	}
> 62	
> 63	function articleMessages(topic: string, siteUrl: string, products: ChosenProduct[]) {
> 64	  if (products.length > 0) {
> 65	    const p = products[0];
> 66	    return [
> 67	      { role: "system", content: `Você é um criador de conteúdo viral de consumo e reviews de produtos para o público brasileiro. Escreva artigos/reviews longos (1000+ palavras) em PT-BR, otimizados para SEO e compartilhamento, com a estrutura GANCHO (por que importa agora) → VALOR (benefícios concretos, casos de uso, para quem é, comparações) → CTA de compra forte. Mencione o produto em destaque pelo nome EXATO ao menos uma vez no corpo. Formato: retorne JSON com campos "title", "content" (HTML), "meta_description", "tags" (array de strings).` },
> 68	      { role: "user", content: `Escreva um artigo/review viral sobre o tema "${topic}". ${productBrief(products)} Foque em por que o ${p?.name ?? "produto"} resolve o problema do leitor: gancho forte na abertura, prova de valor no meio e CTA de compra no fim. Use o nome exato do produto em destaque pelo menos uma vez. Site: https://${siteUrl}` },
> 69	    ];
> 70	  }
> 71	  return [
> 72	    { role: "system", content: `Você é um especialista em marketing digital e SEO. Escreva artigos longos (1200+ palavras) em português brasileiro, otimizados para SEO. Inclua meta description e tags sugeridas. Formato: retorne JSON com campos "title", "content" (HTML), "meta_description", "tags" (array de strings).` },
> 73	    { role: "user", content: `Escreva um artigo completo sobre: "${topic}". O artigo deve ser focado em donos de agências de marketing que querem usar IA para escalar resultados. Inclua dados, exemplos práticos e um CTA forte. URL do site: https://${siteUrl}` },
> 74	  ];
> 75	}
> 76	
> 77	function linkedinMessages(topic: string, articleLink: string, products: ChosenProduct[]) {
> 78	  if (products.length > 0) {
> 79	    const p = products[0];
> 80	    return [
> 81	      { role: "system", content: "Você é um criador de conteúdo viral para LinkedIn sobre produtos de consumo e smart home. Crie posts com gancho forte na 1ª linha, storytelling curto, prova de valor e CTA de compra. Emojis moderados. Cite o produto em destaque pelo nome. Formato: retorne JSON com 'post_text'." },
> 82	      { role: "user", content: `Crie um post de LinkedIn viral sobre "${topic}". ${productBrief(products)} Link de referência: ${articleLink}. Gancho na 1ª linha, valor no meio, CTA de compra no fim. Cite o ${p?.name ?? "produto"} pelo nome.` },
> 83	    ];
> 84	  }
> 85	  return [
> 86	    { role: "system", content: "Você é um especialista em LinkedIn B2B. Crie posts de autoridade com storytelling, emojis moderados, e CTA. Formato: retorne JSON com 'post_text'." },
> 87	    { role: "user", content: `Crie um post LinkedIn sobre: "${topic}". Link do artigo: ${articleLink}. Foque em donos de agências e ROI com IA.` },
> 88	  ];
> 89	}
> 90	
> ```

## 🤖 Claude *(17:19:57)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== BoK files mentioning cron/identity design ===\"\ngrep -rlnE 'OTD-VA-008|begin_autopilot|finalize_autopilot|x-autopilot|autopilot_plan|autopilot_cycle|cadence|FR-VA-021' docs/bok/viral-autopilot/ 2>/dev/null\necho \"=== nurture-cron entry (how pg_cron invokes + identity) ===\"\nsed -n '1,60p' supabase/functions/nurture-cron/index.ts 2>/dev/null || echo \"no nurture-cron\"",
  "description": "Find BoK cron sections + nurture-cron entry"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === BoK files mentioning cron/identity design ===
> docs/bok/viral-autopilot/00-index.md
> docs/bok/viral-autopilot/04-frd.md
> docs/bok/viral-autopilot/07-process-flow.md
> docs/bok/viral-autopilot/03-prd.md
> docs/bok/viral-autopilot/06-data-model.md
> docs/bok/viral-autopilot/08-quality-metrics.md
> docs/bok/viral-autopilot/05-sdd.md
> docs/bok/viral-autopilot/02-brd.md
> === nurture-cron entry (how pg_cron invokes + identity) ===
> // nurture-cron — marketing-hub FR-MH-008 ("cron avança passos"; BoK SSOT 04-frd.md FR-MH-008 + 05-sdd.md).
> // Service-role driver that advances DUE sequence_enrollments across ALL tenants by fanning out to nurture-dispatch
> // (which owns the STRIDE-Critical consent gate + atomic billing + message generation — deliberately NOT duplicated
> // here, single source of truth). Invoked by the `nurture-advance` pg_cron schedule (every 15 min).
> //
> // SECURITY: verify_jwt=false (config.toml) + self-check Authorization === `Bearer ${SB_SECRET_KEY}` (mirrors
> // orchestrate-step) → only the service key (pg_cron via Vault) can run it. No user data crosses tenants: each
> // enrollment carries its own user_id, forwarded to nurture-dispatch's trusted service path.
> import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
> import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 
> const corsHeaders = {
>   "Access-Control-Allow-Origin": "*",
>   "Access-Control-Allow-Methods": "POST, OPTIONS",
>   "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> };
> 
> const MAX_PER_RUN = 200; // cap per tick — no silent unbounded fan-out (logged if hit).
> const CONCURRENCY = 8;    // wall-clock bound (mirrors campaign-run MAX_PARALLEL_STEPS).
> 
> serve(async (req) => {
>   if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
>   const json = (b: unknown, s = 200) =>
>     new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 
>   const url = Deno.env.get("SUPABASE_URL")!;
>   const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
>   // Only the service-role holder (pg_cron presenting the Vault key) may run the cron.
>   if (req.headers.get("Authorization") !== `Bearer ${serviceKey}`) return json({ error: "Forbidden" }, 403);
>   const admin = createClient(url, serviceKey);
> 
>   try {
>     // due = active enrollments whose next_run_at has passed (served by idx_enroll_due partial index).
>     const { data: due, error } = await admin
>       .from("sequence_enrollments")
>       .select("id, user_id")
>       .eq("status", "active")
>       .not("next_run_at", "is", null)
>       .lte("next_run_at", new Date().toISOString())
>       .order("next_run_at", { ascending: true })
>       .limit(MAX_PER_RUN);
>     if (error) throw error;
>     const list = (due ?? []) as Array<{ id: string; user_id: string }>;
>     if (list.length === 0) {
>       admin.from("infra_health_logs").insert({ service: "nurture-cron", status: "healthy" }).then(() => {}, () => {});
>       return json({ status: "ok", due: 0, dispatched: 0, completed: 0, blocked: 0, errors: 0 });
>     }
> 
>     const tally = { dispatched: 0, completed: 0, blocked: 0, errors: 0 };
>     const dispatchOne = async (e: { id: string; user_id: string }) => {
>       try {
>         const r = await fetch(`${url}/functions/v1/nurture-dispatch`, {
>           method: "POST",
>           headers: { Authorization: `Bearer ${serviceKey}`, "Content-Type": "application/json" },
>           body: JSON.stringify({ enrollment_id: e.id, user_id: e.user_id }),
>         });
>         const data = await r.json().catch(() => ({}));
>         switch (data?.status) {
>           case "dispatched": tally.dispatched++; break;
>           case "completed": tally.completed++; break;
> ```

## 🤖 Claude *(17:20:34)*


## 🤖 Claude *(17:20:38)*

`nurture-cron` é o **precedente canônico exato** do que a Fatia 2 precisa: `verify_jwt=false` + self-check `Authorization === Bearer ${SB_SECRET_KEY}` → 403, pg_cron apresenta a Vault key, cada linha carrega seu próprio `user_id` (server-trusted do DB, nunca do body), fan-out com cap `MAX_PER_RUN` + `CONCURRENCY`, telemetria. E `next_run_at` + índice parcial é a primitiva de cadência (R2 "a cada 3 dias"). O anti-mint confirma `deduct` self-only + sign-guard. Última recon: ancorar o SOP no contrato BoK selado + confirmar o RPC de refund.

## 🤖 Claude *(17:20:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== Refund/credit RPC defs in migrations (add_mco_coins vs award_mco_coins) ===\"\ngrep -rnE 'FUNCTION public\\.(add_mco_coins|award_mco_coins)' supabase/migrations/ | head -20\necho \"\"\necho \"=== orchestrate-step service-role identity proof (the cited pattern) ===\"\ngrep -nE 'SB_SECRET_KEY|Authorization\\s*===|service.?role|x-autopilot|prepaid' supabase/functions/orchestrate-step/index.ts | head -20\necho \"\"\necho \"=== finalize_vision_job migration present? (the atomic-finalize mirror) ===\"\nls supabase/migrations/ | grep -iE 'vision_mcp_jobs|finalize_vision'",
  "description": "Refund RPC, orchestrate-step proof, vision-job mirror"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === Refund/credit RPC defs in migrations (add_mco_coins vs award_mco_coins) ===
> supabase/migrations/20260520150000_admin_user_lifecycle.sql:17:REVOKE EXECUTE ON FUNCTION public.add_mco_coins(uuid, integer) FROM authenticated;
> supabase/migrations/20260520150000_admin_user_lifecycle.sql:18:GRANT  EXECUTE ON FUNCTION public.add_mco_coins(uuid, integer) TO service_role;
> supabase/migrations/20260505100000_add_pref_ai_model_and_rpc.sql:11:CREATE OR REPLACE FUNCTION public.add_mco_coins(
> supabase/migrations/20260505100000_add_pref_ai_model_and_rpc.sql:40:REVOKE ALL ON FUNCTION public.add_mco_coins(UUID, INTEGER) FROM PUBLIC;
> supabase/migrations/20260505100000_add_pref_ai_model_and_rpc.sql:41:GRANT EXECUTE ON FUNCTION public.add_mco_coins(UUID, INTEGER) TO authenticated;
> supabase/migrations/20260603210500_harden_definer_search_path.sql:51:CREATE OR REPLACE FUNCTION public.award_mco_coins(p_user_id uuid, p_amount integer, p_action text, p_context jsonb DEFAULT '{}'::jsonb)
> supabase/migrations/20260603220000_secure_ledger_rpcs.sql:29:REVOKE EXECUTE ON FUNCTION public.award_mco_coins(uuid, integer, text, jsonb) FROM PUBLIC, anon, authenticated;
> supabase/migrations/20260603220000_secure_ledger_rpcs.sql:30:GRANT  EXECUTE ON FUNCTION public.award_mco_coins(uuid, integer, text, jsonb) TO service_role;
> 
> === orchestrate-step service-role identity proof (the cited pattern) ===
> 110:    const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 
> === finalize_vision_job migration present? (the atomic-finalize mirror) ===
> 20260615160000_vision_mcp_jobs.sql
> ```

## 🤖 Claude *(17:20:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"########## 04-frd.md \u2014 OTD-VA-008 + cadence/cron/cap FRs (sealed contract) ##########\"\ngrep -nE -A6 'OTD-VA-008|FR-VA-008|FR-VA-021|x-autopilot|begin_autopilot|finalize_autopilot' docs/bok/viral-autopilot/04-frd.md | head -90",
  "description": "Read sealed cron/identity contract from FRD"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ########## 04-frd.md — OTD-VA-008 + cadence/cron/cap FRs (sealed contract) ##########
> 34:| FR-VA-007 | Cost guardrail (kill-switch, atômico) | Custo projetado = **`N_runs × ORCHESTRATION_RUN(10) + ANALYZE_COST(2)`**, onde **`N_runs = |target_product_ids| × |platforms| × ab_variants`** (cada `orchestrate-content` é bundle flat de 10 que **já inclui imagem** — `billing.ts:16-21`; `ab_variants` default 1). Se `projetado > budget_cap_mco` OU `saldo < projetado/min_balance` → aborta (`aborted_budget` 409 / `insufficient_balance` 402), pausa o plano, notifica — **sem deduzir**. Atomicidade: `autopilot-run` faz **UM `deduct_mco_coins(user_id, projetado)` ANTES do fan-out** (pré-pago, `debited_at`); sub-runs em modo `prepaid` (sem self-bill); ao fechar, **`finalize_autopilot_cycle(cycle_id, actual)`** (RPC SECURITY DEFINER service-role-only, idempotente por `refunded_at IS NULL`) **credita o não-usado** `(projetado − actual)` no `mco_balance` na MESMA transação (espelha `finalize_vision_job`). **Refund é crédito positivo — NUNCA `deduct` negativo** (`deduct_mco_coins` rejeita `p_amount<=0`, migration `20260603220000:45`). Resolve TOCTOU. | Critical | PR-VA-006 | EdgeFunction | AT-VA-007 |
> 35:| FR-VA-008 | Engagement collector | Cron `autopilot-collect` (service-role) → fn que, dado o `post_id` de `publish-social`/`publish-meta`, busca insights reais (best-effort por API tier) e grava em `creative_metrics`. **Identidade (como `autopilot-analyze`):** deriva `user_id` da linha confiável (`scheduled_posts`/`autopilot_cycles`, nunca do body) e resolve o token de insights via `social_credentials`/`meta_config` **filtrado por esse `user_id`** (per-user, NFR-VA-004); fail-soft se o tenant não tem tier de insights → grava só `affiliate_clicks`. | High | PR-VA-004 | Cron/EdgeFunction | AT-VA-008 |
> 36-| FR-VA-009 | Unified creative metrics | Tabela `creative_metrics` keyed por `content_variant_id`: affiliate_clicks, impressions, engagements, revenue_cents, source, collected_at. Unifica os 3 sinais (Decisão 3). | High | PR-VA-004 | DB | AT-VA-009 |
> 37-| FR-VA-010 | Cycle analyzer | Edge fn `autopilot-analyze` (service-role): deriva o tenant de `previous_cycle_id` (`SELECT user_id FROM autopilot_cycles` — **nunca do body**); lê `creative_metrics` do ciclo anterior; se vazio, usa baseline (`has_real_data=false`, NÃO inventa) e **não cobra** (log `analyze_empty`); se há dado, produz `optimization_policy` estruturado (top hook/produto/horário/formato) e cobra **2 mco** (`ANALYZE_COST`, 4×-floor — SOP `mcoin-cost-calibration`). **Encadeado pós-ciclo pelo `autopilot-cadence-cron`** (inline, sem cron próprio). | High | PR-VA-005 | EdgeFunction | AT-VA-010 |
> 38-| FR-VA-011 | Feedback injection | A geração (`orchestrate-step`/`autopilot-run`) LÊ o `optimization_policy` mais recente do tenant e injeta as features no system prompt do próximo ciclo. Fecha a quebra "saída sem consumo". | Critical | PR-VA-005 | Lib/EdgeFunction | AT-VA-011 |
> 39-| FR-VA-012 | Product selection by score | Seleção do produto-alvo do `vm_affiliate_products` por `commission_value`+`trend_score`+`profitability_score` (auto em v1.0). No MVP: 3 SKUs semente referenciados no plano (via FR-VA-001). | High | PR-VA-010 | EdgeFunction | AT-VA-012 |
> 40-| FR-VA-013 | Image creative (product-referenced) | Plugar `generate-image` (hoje órfã) ao ciclo, **dentro do bundle `orchestrate-content` de 10 mco** (a imagem já é coberta pelo bundle — `billing.ts:16-21`; não gera custo adicional). Usa `image_url` do produto ML como referência; formato por plataforma (quadrado MVP; 9:16 fase 2). Anexa asset a `scheduled_posts`. | High | PR-VA-008 | EdgeFunction | AT-VA-013 |
> 41-| FR-VA-014 | Autopilot hook | `useAutopilot` (TanStack Query): CRUD de plano, status de ciclos, ROI por criativo. Toda lógica de dados no hook (Harness Engineering). | High | PR-VA-001, PR-VA-007 | Hook | AT-VA-014 |
> --
> 43:| FR-VA-016 | Honor product/affiliate param + cron identity | `orchestrate-content` passa a (a) desestruturar e honrar o produto-alvo (hoje dropado em `:79`), propagando ao `orchestrate-step`; (b) **aceitar o caminho cron** — service-role + header `x-autopilot-user-id` (server-trusted) + `prepaid=true` (sub-run não cobra; já pré-debitado em FR-VA-007). Sanitiza valores externos (produto/trend) antes do prompt. | Critical | PR-VA-001, PR-VA-002 | EdgeFunction | AT-VA-016 |
> 44:| FR-VA-017 | Revenue attribution per creative | `handle-ml-postback` credita `revenue_cents` na `affiliate_links` cujo `content_id = content_variant_id` (FR-VA-004); o coletor (FR-VA-008) reflete em `creative_metrics` por `content_variant_id`. Caminho: postback → `order_id`/`click_id` → `affiliate_links.content_id` → criativo. Depende de OTD-VA-007 (secret per-user). | High | PR-VA-004, PR-VA-007 | EdgeFunction | AT-VA-017 |
> 45:| FR-VA-018 | Trend-informed angle | `autopilot-run` lê `vm_trends` (de `fetch-trends`) para pautar o ângulo viral do ciclo (reconecta a ilha de trends). Texto de trend é **fonte não-confiável** → sanitizado antes do prompt (NFR-VA-008). | High | PR-VA-011 | EdgeFunction | AT-VA-018 |
> 46-| FR-VA-019 | A/B variant generation | Gera N variantes por criativo por ciclo (config no plano); a vencedora é escolhida pelo desempenho do ciclo anterior (`creative_metrics`) e promovida no próximo. Reusa a geração; sob o mesmo teto de custo (FR-VA-007). | Should (v1.0) | PR-VA-012 | EdgeFunction | AT-VA-019 |
> 47-| FR-VA-020 | HITL approval gate (opcional) | Quando `plan.hitl_required=true`, criativos entram em estado `pending_review` antes de publicar; aprovação humana reusa o policy-engine do `intent-execute`. Default off (autônomo). | Should (v1.0) | PR-VA-013 | EdgeFunction | AT-VA-020 |
> 48:| FR-VA-021 | Daily global mcoCoins cap | Safety cap **diário por tenant** (espelha `vision-mcp`): `autopilot-run` soma `spend_mco` dos `autopilot_cycles` do tenant no dia (UTC); se `acumulado + projetado > daily_cap_mco` → aborta (`aborted_daily_cap`), sem deduzir. Computado de `autopilot_cycles` (sem tabela nova). Fecha a ação de FMEA-VA-001 (RPN 128) / BR-RISK-001. | High | PR-VA-006 | EdgeFunction | AT-VA-021 |
> 49-
> 50----
> 51-
> 52-## 3. Non-Functional Requirements
> 53-
> 54-| ID | Category | Requirement | Target | Measurement |
> --
> 63:| NFR-VA-008 | Brand-safety | Cyber-Sentinel no tópico e no conteúdo gerado antes de publicar; disclosure de afiliado | 100% dos criativos | Gate pré-publicação + revisão |
> 64-
> 65----
> 66-
> 67-## 4. Interface Requirements
> 68-
> 69-### 4.1 UI → Hook → Edge Function Contract
> --
> 77:  ↓ dispatch (service-role + x-autopilot-user-id server-trusted + prepaid=true)
> 78-[Edge Function: orchestrate-content → orchestrate-step]   (geração product-aware + monetize; prepaid → NÃO self-bill)
> 79-  ↓ reads/writes
> 80-[Tables: autopilot_plans · autopilot_cycles · creative_metrics · scheduled_posts · affiliate_links]
> 81-```
> 82-
> 83-### 4.2 External API Contracts
> --
> 87:**Auth:** Bearer JWT (user scope, "gerar agora" — asserir `user.id === plan.user_id`) — OU caminho cron: **a fn prova service-role in-function** (`Authorization === 'Bearer '+SB_SECRET_KEY`, padrão `orchestrate-step:50-53`) ANTES de confiar no header `x-autopilot-user-id` (`user_id` server-trusted de `autopilot_plans.user_id`, **nunca do body**; `verify_jwt=false`). SOP `edge-jwt-identity-verification.md`.  
> 88-**Request:**
> 89-```typescript
> 90-{
> 91-  plan_id: string,          // uuid do autopilot_plans (RLS-own)
> 92-  mode_override?: "all_at_once" | "every_n_days",  // opcional; default = plano
> 93-  dry_run?: boolean,        // se true, retorna custo projetado SEM deduzir nem publicar
> --
> 112:| 409 | Cap **diário** global do tenant excedido (FR-VA-021) — body `{ reason: "aborted_daily_cap" }` |
> 113-| 422 | Validação: plano sem produtos/redes, `interval_days` inválido (campo+mensagem PT-BR) |
> 114-| 500 | Erro interno (logado em `infra_health_logs`) |
> 115-
> 116-#### `POST /functions/v1/autopilot-analyze`
> 117-
> 118-**Auth:** service-role (`verify_jwt=false`); invocada inline pós-ciclo pelo `autopilot-cadence-cron`.  
> --
> 145:| FR-VA-002 | ✅ | ✅ | ✅ | fan-out service-role + `x-autopilot-user-id` + `prepaid` (smoke zero-cost com `dry_run`) |
> 146-| FR-VA-003 | ✅ | ✅ | — | prompt contém produto + framework viral |
> 147-| FR-VA-004 | ✅ | ✅ | ✅ | link ML + `content_variant_id` em TODO formato |
> 148-| FR-VA-005 | ✅ | ✅ | — | auto-refill `next_run_at`; janela perdida (catch-up) |
> 149-| FR-VA-006 | ✅ | ✅ | — | idempotência (plan_id, cycle_number) |
> 150-| FR-VA-007 | ✅ | ✅ | ✅ | **kill-switch smoke zero-cost** (saldo intacto pós-abort) |
> 151:| FR-VA-008 | ✅ | ✅ | — | coletor best-effort por tier; cliques sempre |
> 152-| FR-VA-009 | ✅ | — | — | unicidade por `content_variant_id`+`source` |
> 153-| FR-VA-010 | ✅ | ✅ | — | baseline quando vazio (`has_real_data=false`) |
> 154-| FR-VA-011 | ✅ | ✅ | ✅ | prova de reinjeção: prompt ciclo N+1 contém features do ciclo N |
> 155-| FR-VA-012 | ✅ | ✅ | — | ranking comissão+trend |
> 156-| FR-VA-013 | ✅ | ✅ | — | imagem product-referenced anexada a `scheduled_posts` |
> 157-| FR-VA-014 | ✅ | — | — | hook CRUD + queries |
> --
> 164:| FR-VA-021 | ✅ | ✅ | — | **cap diário smoke zero-cost** (acumulado > daily_cap → abort sem deduct) |
> 165-
> 166-**Test files location:**
> 167-- Unit: `src/hooks/__tests__/useAutopilot.test.ts`
> 168-- Integration / smokes: `scripts/qa/smoke-autopilot-run.ts`, `scripts/qa/smoke-autopilot-budget.ts` (zero-cost)
> 169-- E2E: `e2e/viral-autopilot.spec.ts` + gate `/e2e-audit` 1920×1080 para `AutopilotPage`
> 170-
> --
> 178:| PR-VA-002 | FR-VA-002, FR-VA-003, FR-VA-004, FR-VA-016 | NFR-VA-001, NFR-VA-008 |
> 179-| PR-VA-003 | FR-VA-005, FR-VA-006 | NFR-VA-003, NFR-VA-006 |
> 180:| PR-VA-004 | FR-VA-008, FR-VA-009, FR-VA-017 | NFR-VA-007 |
> 181-| PR-VA-005 | FR-VA-010, FR-VA-011 | NFR-VA-007 |
> 182:| PR-VA-006 | FR-VA-007, FR-VA-021 | NFR-VA-002 |
> 183-| PR-VA-007 | FR-VA-014, FR-VA-015, FR-VA-017 | NFR-VA-007 |
> 184:| PR-VA-008 | FR-VA-013 | NFR-VA-008 |
> 185-| PR-VA-010 | FR-VA-012 | — |
> 186-| PR-VA-011 | FR-VA-018 | — |
> 187-| PR-VA-012 | FR-VA-019 | — |
> 188-| PR-VA-013 | FR-VA-020 | — |
> 189-
> 190-> Cobertura: 21 FR (FR-VA-001..021) · 8 NFR. PRs de Fase 2/Future (PR-VA-020/021/022) não decompostos neste ciclo (FRD §1). Todo PR Must/Should rastreia ≥1 FR; todo FR rastreia ≥1 PR. **Gaps de numeração intencionais:** PR-VA-009 (saltado 008→010 entre Must e Should) e FR-VA-014..018 contínuos — sem buracos de conteúdo.
> ```

## 🤖 Claude *(17:21:12)*


## 🤖 Claude *(17:21:14)*

Contrato selado totalmente mapeado. Tenho os 4 pilares vivos: `nurture-cron` (prova de identidade cron canônica), `deduct_mco_coins` (sign-guard + self-only), o RPC de refund, e o contrato BoK (FR-VA-007/008/016/021). Última leitura antes de escrever — o `finalize_vision_job` que o design manda espelhar + a definição literal da OTD-VA-008.

## 🤖 Claude *(17:21:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== finalize_vision_job RPC (the atomic terminal+refund mirror) ===\"\nsed -n '/finalize_vision_job/,/\\$function\\$;/p' supabase/migrations/20260615160000_vision_mcp_jobs.sql 2>/dev/null | head -80\necho \"\"\necho \"=== OTD-VA-008 literal definition (across BoK) ===\"\ngrep -rnE -A3 'OTD-VA-008' docs/bok/viral-autopilot/03-prd.md docs/bok/viral-autopilot/02-brd.md docs/bok/viral-autopilot/05-sdd.md 2>/dev/null | head -30",
  "description": "Read finalize_vision_job mirror + OTD-VA-008 definition"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === finalize_vision_job RPC (the atomic terminal+refund mirror) ===
> CREATE OR REPLACE FUNCTION public.finalize_vision_job(
>   p_job_id    uuid,
>   p_state     text,
>   p_delivered int,
>   p_amount    int,    -- refund to credit (0 = no refund, e.g. 'done')
>   p_failed    jsonb,
>   p_result    jsonb
> )
> RETURNS jsonb
> LANGUAGE plpgsql
> SECURITY DEFINER
> SET search_path = ''
> AS $$
> DECLARE
>   v_uid uuid;
> BEGIN
>   IF p_state NOT IN ('done','partial','failed') THEN
>     RAISE EXCEPTION 'finalize_vision_job: terminal state required, got %', p_state USING errcode = '22023';
>   END IF;
> 
>   -- Claim + finalize a NON-TERMINAL job exactly once.
>   UPDATE public.vision_jobs
>      SET state           = p_state,
>          delivered_units = p_delivered,
>          result          = p_result,
>          failed_units    = p_failed,
>          refunded_mco    = CASE WHEN p_amount > 0 THEN p_amount ELSE refunded_mco END,
>          refunded_at     = CASE WHEN p_amount > 0 THEN now()  ELSE refunded_at END
>    WHERE id = p_job_id
>      AND state IN ('queued','running')
>    RETURNING user_id INTO v_uid;
> 
>   IF v_uid IS NULL THEN
>     RETURN jsonb_build_object('finalized', false);   -- already terminal → no-op (no double refund)
>   END IF;
> 
>   -- Guard write (above) + balance credit commit in the SAME transaction.
>   IF p_amount > 0 THEN
>     PERFORM public.add_mco_coins(v_uid, p_amount);
>     RETURN jsonb_build_object('finalized', true, 'refunded', p_amount);
>   END IF;
> 
>   RETURN jsonb_build_object('finalized', true, 'refunded', 0);
> END;
> $$;
> 
> REVOKE ALL ON FUNCTION public.finalize_vision_job(uuid, text, int, int, jsonb, jsonb) FROM PUBLIC, anon, authenticated;
> GRANT EXECUTE ON FUNCTION public.finalize_vision_job(uuid, text, int, int, jsonb, jsonb) TO service_role;
> 
> === OTD-VA-008 literal definition (across BoK) ===
> docs/bok/viral-autopilot/05-sdd.md:425:| OTD-VA-008 | Identidade do caminho cron→`orchestrate-content` (o cron não tem JWT; a fn rejeita sem `Bearer`) | Repassar JWT (impossível — cron não tem) | Service-role + `x-autopilot-user-id` derivado de `autopilot_plans.user_id` + pré-débito atômico em `autopilot-run` (sub-runs `prepaid`) | **B** — server-trusted, nunca do body; resolve blocker SEC-VA-01 + TOCTOU SEC-VA-04. **Gate Lei 2: exige SOP `docs/processes/autopilot-cron-identity.md` ANTES de qualquer código** | Open (SOP-gated) | Sovereign |
> docs/bok/viral-autopilot/05-sdd.md-426-
> docs/bok/viral-autopilot/05-sdd.md:427:> **Gate Lei 2 (Processo Antecipado):** o caminho de identidade do cron (OTD-VA-008) e o pré-débito/refund (FR-VA-007) introduzem automação financeira nova → o SOP `docs/processes/autopilot-cron-identity.md` DEVE ser escrito e revisado **antes** de a fatia de cadência/custo ganhar código. Referência cruzada: SOP `orchestrate-async-pipeline.md` (mandato `verify_jwt=false`).
> docs/bok/viral-autopilot/05-sdd.md-428-
> docs/bok/viral-autopilot/05-sdd.md-429----
> docs/bok/viral-autopilot/05-sdd.md-430-
> ```

## 🤖 Claude *(17:22:16)*


## 🤖 Claude *(17:22:18)*

Contrato 100% mapeado e materialmente ancorado. `finalize_vision_job` é o molde exato (claim-once `WHERE state IN (...) RETURNING user_id`, idempotente, credita via `add_mco_coins` positivo na mesma transação, REVOKE public/GRANT service_role). OTD-VA-008 confirmada **Open (SOP-gated)**. Escrevendo o SOP — o deliverable que abre o gate Lei 2.

## 🤖 Claude *(17:24:04)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/[[autopilot-cron-identity|autopilot-cron-identity]].md",
  "content": "# SOP: Viral Autopilot \u2014 Cron Identity + Pre-Debit/Refund Atomicity (`autopilot-cron-identity`)\n\n**Status:** ACTIVE \u00b7 v1.0 \u00b7 2026-06-20\n**Owner:** Sovereign (Gabriel Zarattini)\n**Survival Law 2 compliance:** Escrito **ANTES** de qualquer c\u00f3digo da fatia de cad\u00eancia/custo do Viral Autopilot (R2 recorr\u00eancia + R3 loop). Abre o gate **OTD-VA-008** (`docs/bok/viral-autopilot/05-sdd.md:425` \u2014 *\"Gate Lei 2: exige SOP `docs/processes/autopilot-cron-identity.md` ANTES de qualquer c\u00f3digo\"*) e cobre o pr\u00e9-d\u00e9bito/refund at\u00f4mico de **FR-VA-007** + o cap di\u00e1rio de **FR-VA-021**.\n**Canonical directive:** `CLAUDE.md > \"API Tenancy Model \u2014 Per-User Credentials\"` \u00b7 `.claude/rules/survival.md > Law 1 (Materiality) / Law 2 (Anticipated Process)` \u00b7 `docs/bok/viral-autopilot/{04-frd,05-sdd,06-data-model}.md`\n**Sibling SOPs:** `edge-jwt-identity-verification.md` (camada-3 service-role gate, base deste) \u00b7 `orchestrate-async-pipeline.md` (mandato `verify_jwt=false` + pg_net + contrato de param-name dos RPCs).\n\n---\n\n## Context\n\nA fatia de cad\u00eancia do Viral Autopilot introduz **automa\u00e7\u00e3o financeira aut\u00f4noma**: um `pg_cron` dispara a gera\u00e7\u00e3o+publica\u00e7\u00e3o de criativos a cada N dias, **sem m\u00e3o humana no loop**, gastando `mco_balance` do tenant. Dois riscos materiais nascem disso:\n\n1. **Identidade do caminho cron (SEC-VA-CRIT-01 / OTD-VA-008).** As fun\u00e7\u00f5es `autopilot-*` rodam com `verify_jwt = false` em `supabase/config.toml` \u2014 o gateway Kong **n\u00e3o** valida JWT (mesmo motivo de todo o ecossistema: a sess\u00e3o do usu\u00e1rio \u00e9 ES256, o gateway est\u00e1 configurado para o segredo HS256 legado; ver `edge-jwt-identity-verification.md`). O cron **n\u00e3o possui** um JWT de usu\u00e1rio para repassar. A tenta\u00e7\u00e3o fatal \u00e9 confiar num header `x-autopilot-user-id` vindo do request \u2014 o que deixaria **qualquer** chamador drenar a carteira de **qualquer** v\u00edtima (`POST autopilot-run` com `x-autopilot-user-id: <victim>` \u2192 d\u00e9bito + publica\u00e7\u00e3o na conta da v\u00edtima). A valida\u00e7\u00e3o adversarial da BoK (Fase 6, rodada R1) marcou exatamente este vetor como **blocker**.\n\n2. **Atomicidade do pr\u00e9-d\u00e9bito/refund (FR-VA-007 / TOCTOU SEC-VA-04).** Um ciclo gera `N_runs = |produtos| \u00d7 |redes| \u00d7 ab_variants` sub-runs, cada um um bundle flat de 10 mcoCoins (`billing.ts:16-21` \u2014 imagem **j\u00e1 inclu\u00edda**). Se cada sub-run se auto-cobrar, uma falha no meio deixa o tenant cobrado por trabalho n\u00e3o-entregue; se o cap di\u00e1rio for checado com um `SELECT` separado do `deduct`, dois ciclos concorrentes passam o cap juntos (TOCTOU). A rodada R2 da valida\u00e7\u00e3o pegou um **anti-mint** que eu mesmo introduzi: refund implementado como `deduct` de valor negativo viola o guard `p_amount <= 0` de `deduct_mco_coins` (`migration 20260603220000:45`) \u2014 refund **tem** que ser cr\u00e9dito positivo.\n\n**Regra-m\u00e3e:** confiar num `user_id` no caminho cron s\u00f3 \u00e9 permitido depois de **provar posse da `SB_SECRET_KEY` in-function** E de derivar o `user_id` de uma **linha confi\u00e1vel do banco** (`autopilot_plans.user_id` / `autopilot_cycles.user_id`), **nunca do corpo/header do request**. Todo movimento de saldo passa por **um** RPC `SECURITY DEFINER` service-role-only, com cap + d\u00e9bito na **mesma transa\u00e7\u00e3o sob advisory lock**, e refund como **cr\u00e9dito positivo idempotente**.\n\n---\n\n## ORO triplet\n\n- **Operator:** MCORCH Master Execution Agent (autoria das migrations/fun\u00e7\u00f5es) + `pg_cron` apresentando a Vault key (execu\u00e7\u00e3o por tick) + Edge runtime Deno (gate por request).\n- **Reviewer:** Sovereign (Gabriel) \u2014 aprova as migrations + valida os smokes zero-cost e o exploit test p\u00f3s-deploy \u00b7 `/security-review` independente em **cada** migration (mandato `CLAUDE.md`).\n- **Owner:** Sovereign \u2014 blast radius = **carteira do tenant gasta autonomamente** (mint/drain cross-tenant se a identidade falhar; sangria silenciosa se o cap/refund falhar).\n\n---\n\n## Operator (equivalente manual \u2014 material)\n\nA automa\u00e7\u00e3o substitui o seguinte ritual humano que o Sovereign executaria **hoje, \u00e0 m\u00e3o**, a cada janela de cad\u00eancia, para cada plano ativo:\n\n| # | Passo manual | Crit\u00e9rio de sucesso material |\n|---|--------------|------------------------------|\n| 1 | Abrir a UI do Autopilot e listar os planos cujo `next_run_at` venceu | Lista de `plan_id` vencidos vis\u00edvel |\n| 2 | Para cada plano: conferir o `mco_balance` **e** quanto j\u00e1 gastou hoje (n\u00e3o estourar o cap di\u00e1rio) | `balance` e `gasto_hoje` lidos antes de qualquer clique |\n| 3 | Calcular `N_runs = produtos \u00d7 redes \u00d7 variants` e `projetado = N_runs\u00d710 + 2` | N\u00famero conferido contra o cap do plano |\n| 4 | Clicar \"gerar agora\" **uma vez** por plano (dispara os sub-runs) | 1 d\u00e9bito de `projetado`, depois os sub-runs publicam |\n| 5 | Aguardar os sub-runs; anotar quantos **de fato** publicaram | `actual` real conhecido |\n| 6 | Reconciliar: devolver ao saldo os coins dos runs que **n\u00e3o** entregaram | `balance` final = inicial \u2212 `actual` |\n| 7 | Reagendar o plano para a pr\u00f3xima janela (`next_run_at += interval_days`) | Plano re-armado |\n\nO `pg_cron` automatiza os passos 1\u20137. **O gate Lei 2 existe porque automatizar o passo 2 (cap) e o passo 6 (refund) errado = sangria silenciosa de carteira.** O precedente vivo desta topologia \u00e9 **`nurture-cron` \u2192 `nurture-dispatch`** (`supabase/functions/nurture-cron/index.ts`): driver service-role que varre `next_run_at` vencidos e faz fan-out com cap `MAX_PER_RUN` + `CONCURRENCY`, cada linha carregando seu pr\u00f3prio `user_id` confi\u00e1vel.\n\n---\n\n## Topologia (alvo)\n\n```\npg_cron  \u2500\u2500Bearer SB_SECRET_KEY\u2500\u2500\u25b6  autopilot-cadence-cron   (driver service-role)\n  (Vault key)                          \u2502  SELECT plan_id,user_id FROM autopilot_plans\n                                       \u2502  WHERE status='active' AND next_run_at <= now()\n                                       \u2502  (user_id = SERVER-TRUSTED da linha)\n                                       \u25bc  fan-out (cap MAX_PER_RUN + CONCURRENCY)\n            \u2500\u2500Bearer SB_SECRET_KEY\u2500\u2500\u25b6  autopilot-run          (executor por plano)\n            + x-autopilot-user-id        \u2502  \u2460 prova service-role in-function\n                                         \u2502  \u2461 begin_autopilot_cycle (cap + pr\u00e9-d\u00e9bito at\u00f4mico, advisory lock)\n                                         \u2502  \u2462 fan-out sub-runs\n                                         \u25bc\n            \u2500\u2500Bearer SB_SECRET_KEY\u2500\u2500\u25b6  orchestrate-content    (prepaid=true \u2192 N\u00c3O self-bill)\n            + x-autopilot-user-id        \u2502  gera\u00e7\u00e3o product-aware + monetize (Fatia 1)\n                                         \u25bc\n                                       finalize_autopilot_cycle (refund cr\u00e9dito-positivo idempotente)\n                                         \u2502\n                                         \u25bc  inline p\u00f3s-ciclo\n                                       autopilot-analyze       (R3 loop; tenant de previous_cycle_id)\n```\n\n---\n\n## Identity resolution order (canonical \u2014 fun\u00e7\u00f5es `autopilot-*`, `verify_jwt=false`)\n\n| # | Camada | Fonte | Permitido em |\n|---|--------|-------|--------------|\n| 1 | **Service-role gate (caminho cron \u2014 PRIM\u00c1RIO aqui)** | `req.headers.get(\"Authorization\") === \\`Bearer ${SB_SECRET_KEY}\\`` \u2192 **403** se n\u00e3o. Padr\u00e3o literal vivo: `nurture-cron/index.ts` (self-check) + `orchestrate-step/index.ts:110` (`SB_SECRET_KEY ?? SUPABASE_SERVICE_ROLE_KEY`). | `autopilot-cadence-cron`, `autopilot-run` (tick), `autopilot-analyze`, `autopilot-collect` |\n| 2 | **`user_id` server-trusted** | Derivar de uma **linha do banco**: `autopilot_plans.user_id` (cadence-cron) \u00b7 `autopilot_cycles.user_id` via `previous_cycle_id` (analyze) \u00b7 `scheduled_posts`/`autopilot_cycles` (collect). O header `x-autopilot-user-id` \u00e9 s\u00f3 um **espelho** desse valor para logging/propaga\u00e7\u00e3o \u2014 **nunca a fonte de verdade**. | Idem (sempre, ap\u00f3s camada 1) |\n| 3 | **User JWT (\"gerar agora\")** | Caminho user-facing: `getUser()` / JWKS verify (sibling SOP) \u2192 **asserir `user.id === plan.user_id`** (IDOR gate). | `autopilot-run` (bot\u00e3o UI) |\n| 4 | **Hard failure** | \u2014 | **403** `{ error: \"Forbidden\" }` (cron) / **401** `{ error: \"Token inv\u00e1lido\" }` (user). **Fail-closed.** |\n\n**Regra de ouro (herdada de `edge-jwt-identity-verification.md`, estendida):** no caminho cron, confiar num `user_id` exige **(a)** posse provada da `SB_SECRET_KEY` **E** **(b)** o `user_id` ter vindo de uma linha do banco \u2014 n\u00e3o do request. As duas condi\u00e7\u00f5es, sempre, e nessa ordem.\n\n---\n\n## Sequence (o tick \u2192 ciclo \u2192 finalize)\n\n1. **`pg_cron` dispara `autopilot-cadence-cron`** via pg_net, header `Authorization: Bearer <SB_SECRET_KEY>` (Vault). Sucesso material: linha `infra_health_logs service='autopilot-cadence-cron'`.\n2. **`autopilot-cadence-cron` prova service-role** (camada 1) \u2192 403 se ausente. Varre `autopilot_plans WHERE status='active' AND next_run_at <= now()` (\u00edndice parcial, espelha `idx_enroll_due`). Sucesso: lista de `{plan_id, user_id}` (user_id **da linha**).\n3. **Fan-out** para `autopilot-run` (cap `MAX_PER_RUN`, `CONCURRENCY`), cada POST com `Bearer SB_SECRET_KEY` + `x-autopilot-user-id` = `plan.user_id`. **Sem fan-out ilimitado silencioso** (logar se o cap for atingido \u2014 padr\u00e3o `nurture-cron`).\n4. **`autopilot-run` prova service-role** (camada 1) **OU** valida JWT+IDOR (camada 3). Resolve `user_id` server-trusted. Calcula `N_runs` e `projetado = N_runs\u00d710 + ANALYZE_COST(2)`.\n5. **`begin_autopilot_cycle(p_user_id, p_plan_id, p_projected_mco, p_daily_cap_mco, p_budget_cap_mco)`** \u2014 RPC `SECURITY DEFINER`, service-role-only, **`pg_advisory_xact_lock(hashtext(user_id::text))`**:\n   - **Cap di\u00e1rio (FR-VA-021):** `SUM(spend_mco)` dos `autopilot_cycles` do tenant no dia (UTC). Se `acumulado + projetado > daily_cap_mco` \u2192 `RAISE` `aborted_daily_cap` (**sem deduzir**).\n   - **Cap por plano + saldo (FR-VA-007):** `projetado > budget_cap_mco` \u2192 `aborted_budget`; `balance < projetado` \u2192 `insufficient_balance`. Ambos `RAISE` **sem deduzir** + pausam o plano.\n   - **OK:** `INSERT autopilot_cycles (state='open', debited_at=now(), spend_mco=projetado)` **+** `deduct_mco_coins(user_id, projetado)` na **mesma transa\u00e7\u00e3o** \u2192 `RETURN cycle_id`. **Um** d\u00e9bito por ciclo. O advisory lock serializa ciclos concorrentes do mesmo tenant \u2192 mata o TOCTOU.\n6. **Fan-out dos sub-runs** \u2192 `orchestrate-content` com `prepaid=true` + service-role + `x-autopilot-user-id` (FR-VA-016). **`prepaid` \u21d2 N\u00c3O chama `deduct_mco_coins`** (j\u00e1 pr\u00e9-debitado no passo 5). Sucesso: `pipeline_runs` por sub-run; `affiliate_links.content_id` NON-NULL (herdado da Fatia 1).\n7. **`finalize_autopilot_cycle(p_cycle_id, p_actual_mco)`** \u2014 RPC `SECURITY DEFINER`, service-role-only, **espelha `finalize_vision_job` (`20260615160000`):**\n   - Claim-once: `UPDATE autopilot_cycles SET state='closed', actual_mco=p_actual, refunded_at=now() WHERE id=p_cycle_id AND state='open' RETURNING user_id`. Se `NULL` \u2192 j\u00e1 terminal \u2192 **no-op** (sem refund duplo).\n   - `refund = projetado \u2212 actual`; se `refund > 0` \u2192 **`add_mco_coins(user_id, refund)`** (cr\u00e9dito **positivo** ledgered) na **mesma transa\u00e7\u00e3o**. **NUNCA `deduct` negativo.**\n8. **`autopilot-analyze` inline** (n\u00e3o cron pr\u00f3prio) \u2014 tenant de `previous_cycle_id` (camada 2). 2 mco **s\u00f3 se `has_real_data`** (sen\u00e3o 0, log `analyze_empty`).\n9. **Reagendar:** `next_run_at += interval_days` (catch-up de janela perdida \u2014 FR-VA-005). Sucesso: `next_run_at` futuro.\n\n---\n\n## Cost & atomicity contract (resumo execut\u00e1vel)\n\n| Invariante | Como \u00e9 garantido | \u00c2ncora |\n|------------|------------------|--------|\n| **Um d\u00e9bito por ciclo** | `begin_autopilot_cycle` faz o `deduct` \u00fanico; sub-runs `prepaid` | FR-VA-007 \u00b7 FR-VA-016 |\n| **Cap + d\u00e9bito at\u00f4micos (anti-TOCTOU)** | tudo dentro de `begin_autopilot_cycle` sob `pg_advisory_xact_lock` | FR-VA-007 / SEC-VA-04 |\n| **Refund = cr\u00e9dito positivo** | `add_mco_coins(user, refund)`; `deduct_mco_coins` rejeita `p_amount<=0` | `20260603220000:45` |\n| **Refund idempotente (sem duplo)** | claim-once `WHERE state='open' RETURNING user_id` | espelha `finalize_vision_job` |\n| **Abort n\u00e3o cobra** | caps fazem `RAISE` antes do `deduct` | FR-VA-007 / FR-VA-021 |\n| **RPCs blindados** | `REVOKE ... FROM PUBLIC, anon, authenticated; GRANT ... TO service_role` | padr\u00e3o ledger `20260603220000` |\n| **`user_id` nunca do body** | derivado de `autopilot_plans/_cycles` (linha confi\u00e1vel) | OTD-VA-008 (Decis\u00e3o B) |\n\n---\n\n## Verification gates\n\n| Gate | Check | Pass criterion |\n|------|-------|----------------|\n| **G1 \u2014 Cron identity (exploit, prod)** | `curl -X POST <autopilot-run-url>` com `x-autopilot-user-id: <victim>` **sem** `Bearer SB_SECRET_KEY` (apikey anon) | **403** \u2014 nenhum d\u00e9bito, nenhum ciclo criado (sem o gate: processaria como v\u00edtima) |\n| **G2 \u2014 IDOR no caminho user** | JWT do user A com `plan_id` do user B | **401/403** \u2014 `user.id !== plan.user_id` rejeitado |\n| **G3 \u2014 Pr\u00e9-d\u00e9bito at\u00f4mico (smoke zero-cost)** | `scripts/qa/smoke-autopilot-budget.ts`: `begin_autopilot_cycle` com `projetado > balance` | `insufficient_balance`, `mco_balance` **intacto** (SELECT antes/depois) |\n| **G4 \u2014 Cap di\u00e1rio (smoke zero-cost)** | acumular `spend_mco` fict\u00edcio > `daily_cap`, chamar `begin_*` | `aborted_daily_cap`, **sem deduct** |\n| **G5 \u2014 Refund idempotente** | `finalize_autopilot_cycle` chamado **2\u00d7** no mesmo `cycle_id` | 1\u00ba credita `refund`; 2\u00ba `finalized=false` (no-op) \u2014 saldo creditado **uma** vez |\n| **G6 \u2014 Refund nunca-negativo** | `finalize_*` com `actual > projetado` (refund negativo) | `refund` clampado a 0 (nunca chama `deduct`); CHECK `actual_mco <= spend_mco` no DDL |\n| **G7 \u2014 `prepaid` n\u00e3o self-cobra** | sub-run `orchestrate-content` com `prepaid=true` | nenhuma linha `mcoin_transactions` do sub-run; s\u00f3 o d\u00e9bito \u00fanico do `begin_*` |\n| **G8 \u2014 RPC grants** | `\\df+ begin_autopilot_cycle finalize_autopilot_cycle` (ou Management API) | EXECUTE **s\u00f3** `service_role`; revogado de `public/anon/authenticated` |\n| **G9 \u2014 `/security-review`** | cada migration nova | **SAFE** (0 findings \u2265 High) antes do commit |\n| **G10 \u2014 Advisory lock real** | 2 `begin_*` concorrentes do mesmo user (teste de stress) | serializados; soma nunca passa o cap |\n\nG1/G3/G4/G5 s\u00e3o **zero-cost** (usam `dry_run`/usu\u00e1rios descart\u00e1veis/RPC isolado) \u2014 provam o gate **sem** gastar mcoCoins reais. O 1\u00ba ciclo pago real (E2E) \u00e9 **gated em GO Sovereign** (mesma disciplina das fatias anteriores).\n\n---\n\n## Recovery path\n\n- **Cron dispara mas a fn rejeita (403):** verificar que o `pg_cron` job injeta a Vault key correta no header (`SB_SECRET_KEY`, **n\u00e3o** a legada `SUPABASE_SERVICE_ROLE_KEY` revogada \u2014 ver mem\u00f3ria `reference_supabase_keys_migrated`). Recriar o job com `Authorization: Bearer <SB_SECRET_KEY>`.\n- **D\u00e9bito feito mas fan-out falha (crash entre passo 5 e 6):** o ciclo fica `state='open'` com `debited_at` setado e `actual=0`. Um **sweep de reconcilia\u00e7\u00e3o** (cron di\u00e1rio ou poll, espelha o self-heal de \u00f3rf\u00e3o do `deepsearch.poll`) chama `finalize_autopilot_cycle(cycle_id, actual_real)` \u2192 credita o n\u00e3o-usado. O claim-once garante idempot\u00eancia mesmo se o sweep e o caminho normal colidirem.\n- **Refund parece n\u00e3o creditar:** confirmar materialmente via `SELECT mco_balance` antes/depois + a linha `mcoin_transactions action='autopilot_refund'`. NUNCA \"tente de novo\" cego \u2014 `finalize_*` \u00e9 idempotente, re-chamar \u00e9 seguro e diagn\u00f3stico.\n- **Cap di\u00e1rio travando ciclos leg\u00edtimos:** ajustar `daily_cap_mco` no plano (config do tenant), nunca remover a checagem. O cap \u00e9 a feature, n\u00e3o o bug.\n- **Rollback de migration:** as migrations s\u00e3o aditivas (novas tabelas/RPCs). Rollback = `DROP FUNCTION begin_autopilot_cycle / finalize_autopilot_cycle` + `DROP TABLE autopilot_cycles / autopilot_plans` (ordem FK). Confirmar via Management API.\n\n---\n\n## Success signal\n\n- **G1 verde:** `403` literal no exploit test contra produ\u00e7\u00e3o (cron sem `Bearer` \u2192 rejeitado), colado no handoff (Lei 1).\n- **G3/G4 verdes:** smokes zero-cost com `mco_balance` **byte-id\u00eantico** antes/depois de um abort (SELECT real).\n- **G5 verde:** refund creditado **exatamente uma** vez sob dupla-finaliza\u00e7\u00e3o.\n- **G8 verde:** `service_role`-only nos dois RPCs (output literal do `\\df+` / Management API).\n- **G9 verde:** `/security-review` SAFE em cada migration.\n- **1\u00ba ciclo pago real (gated):** `autopilot_cycles` `state='closed'`, `deduct` = `projetado`, `refund` = `projetado \u2212 actual`, `mco_balance` final = inicial \u2212 `actual` (delta material exato).\n\n---\n\n## Anti-patterns proibidos\n\n- \u274c Confiar em `x-autopilot-user-id` (ou qualquer `user_id` do body/header) **sem** provar `SB_SECRET_KEY` in-function E sem derivar de linha do banco.\n- \u274c `deduct_mco_coins(user, -refund)` para \"estornar\" \u2014 viola o guard anti-mint (`20260603220000:45`). Refund \u00e9 **`add_mco_coins` positivo**.\n- \u274c Checar o cap com um `SELECT` e depois `deduct` em chamadas separadas (TOCTOU). Cap + d\u00e9bito v\u00e3o **juntos** no `begin_autopilot_cycle` sob advisory lock.\n- \u274c Sub-run `orchestrate-content` self-cobrando no caminho cron (duplo d\u00e9bito). `prepaid=true` \u21d2 sem `deduct`.\n- \u274c `finalize_*` sem claim-once \u2192 refund duplo a cada retry/sweep.\n- \u274c Fan-out ilimitado sem cap por tick (`MAX_PER_RUN`) \u2014 drift de custo silencioso.\n- \u274c `GRANT EXECUTE` dos RPCs de ciclo a `authenticated`/`anon` (qualquer um cunharia/estornaria). **Service-role-only.**\n- \u274c `verify_jwt=true` no gateway para as `autopilot-*` (quebraria o caminho cron **e** o user ES256).\n- \u274c Setar `daily_cap`/`budget_cap` como opcional/ausente \u2014 o cron **n\u00e3o** roda sem teto (kill-switch obrigat\u00f3rio, FMEA-VA-001 RPN 128).\n\n---\n\n## Sibling reference\n\n- **Camada-3 service-role gate (base):** `docs/processes/edge-jwt-identity-verification.md` + `supabase/functions/nurture-cron/index.ts` (precedente vivo id\u00eantico de cron\u2192dispatch).\n- **`verify_jwt=false` + pg_net + param-name contract:** `docs/processes/orchestrate-async-pipeline.md`.\n- **Anti-mint ledger RPCs:** `supabase/migrations/20260603220000_secure_ledger_rpcs.sql` (`deduct_mco_coins` sign+own-tenant guards; `award_mco_coins`/`add_user_score` edge-only).\n- **Atomic terminal+refund (molde):** `supabase/migrations/20260615160000_vision_mcp_jobs.sql` (`finalize_vision_job` claim-once + `add_mco_coins` positivo).\n- **Sealed contract:** `docs/bok/viral-autopilot/04-frd.md` (FR-VA-002/007/008/010/016/021) \u00b7 `05-sdd.md:425-427` (OTD-VA-008 + nota do gate Lei 2).\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/processes/[[autopilot-cron-identity|autopilot-cron-identity]].md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(17:25:03)*


## 🤖 Claude *(17:25:13)*

SOP escrito e materialmente ancorado — `docs/processes/autopilot-cron-identity.md` (gate **OTD-VA-008** aberto). Cada claim do doc cita código vivo, não invenção:

**O que o SOP trava (os 2 riscos que o gate protege):**
- **Identidade cron (OTD-VA-008 · Decisão B):** caminho `autopilot-*` com `verify_jwt=false` → prova `Bearer SB_SECRET_KEY` *in-function* (precedente vivo idêntico: [nurture-cron](supabase/functions/nurture-cron/index.ts)) **antes** de confiar em qualquer `user_id`, que vem **sempre da linha do banco** (`autopilot_plans.user_id`), nunca do header. Fecha o vetor de drenar carteira de vítima que a validação adversarial R1 marcou como blocker.
- **Atomicidade pré-débito/refund (FR-VA-007/021):** cap diário + cap de plano + **um** `deduct` único, tudo dentro de `begin_autopilot_cycle` sob `pg_advisory_xact_lock` (mata o TOCTOU); refund = **crédito positivo idempotente** via `finalize_autopilot_cycle`, espelhando exatamente o [`finalize_vision_job`](supabase/migrations/20260615160000_vision_mcp_jobs.sql) (claim-once `WHERE state='open' RETURNING user_id`). Nunca `deduct` negativo — respeita o anti-mint `20260603220000:45`.

10 gates de verificação (G1 exploit 403 · G3/G4/G5 smokes **zero-cost** provam cap+refund sem gastar mco real · G8 RPC service-role-only · G9 `/security-review` por migration).

O próprio SOP (e a nota do gate na SDD `05-sdd.md:427`) manda: **"escrito e revisado antes do código."** A revisão é sua (ORO Reviewer · Owner do blast radius financeiro). Por isso paro aqui antes de mover dinheiro em código.

## 🤖 Claude *(17:25:19)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "SOP do gate Lei 2 est\u00e1 pronto e ancorado. O BoK manda revisar antes de qualquer c\u00f3digo de automa\u00e7\u00e3o financeira. Como seguimos?",
      "header": "Pr\u00f3ximo passo",
      "multiSelect": false,
      "options": [
        {
          "label": "Bora a migration",
          "description": "Pr\u00f3xima fatia de c\u00f3digo = a funda\u00e7\u00e3o de dados + dinheiro: migration com autopilot_plans + autopilot_cycles (FK composta tenant-escopada, RESTRICTIVE no-delete) + os 2 RPCs begin_autopilot_cycle / finalize_autopilot_cycle (service-role-only). Cada migration passa /security-review independente antes do commit. As edge functions (cadence-cron, autopilot-run, analyze, collect) v\u00eam depois. Teto di\u00e1rio kill-switch eu defaulto conservador (overrid\u00e1vel per-plano na UI)."
        },
        {
          "label": "Quero ler o SOP primeiro",
          "description": "Pauso pra voc\u00ea ler docs/processes/[[autopilot-cron-identity|autopilot-cron-identity]].md inteiro e dar o GO (ou pedir ajuste) antes de eu tocar em c\u00f3digo."
        },
        {
          "label": "Ajustar tetos/escopo antes",
          "description": "Conversar sobre os defaults de teto di\u00e1rio/por-ciclo de mcoCoins, frequ\u00eancia do tick do cron, ou o escopo da primeira fatia, antes de codar."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "SOP do gate Lei 2 está pronto e ancorado. O BoK manda revisar antes de qualquer código de automação financeira. Como seguimos?"="Bora a migration". You can now continue with these answers in mind.
> ```

## 🤖 Claude *(17:45:21)*


## 🤖 Claude *(17:45:23)*

**GO recebido — bora a migration.** Mando ler o contrato selado antes de escrever DDL (Lei 2: a migration segue o `06-data-model.md`, não improvisa). Leio em paralelo: o data-model selado, o sibling `creative_metrics` (template de estilo desta suíte) e o corpo do `add_mco_coins` (o RPC de crédito que o `finalize` vai chamar).

## 🤖 Claude *(17:45:24)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/06-data-model.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Data & Knowledge Model
> 2	
> 3	**Project:** viral-autopilot  
> 4	**Version:** v0.1 | **Date:** 2026-06-17  
> 5	**BoK Applied:** DMBOK v2 (Data Modeling & Design + Data Quality)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Conceptual Data Model
> 11	
> 12	```
> 13	[autopilot_plans] ──(1:N)──▶ [autopilot_cycles] ──(1:N)──▶ [creative_metrics]
> 14	       │                            │                              │
> 15	       │ (references)               │ (cycle_id on)                │ (content_variant_id)
> 16	       ▼                            ▼                              ▼
> 17	[vm_affiliate_products]      [scheduled_posts] ──(N:1)──▶ [content_library]
> 18	       │                            │                              │
> 19	       └──(promotes)──▶ [affiliate_links] ◀──(revenue)── [handle-ml-postback]
> 20	                                    │
> 21	                                    └──(1:1 observation)──▶ [mcorch_nodes] ──OPTIMIZES_FROM──▶ [mcorch_nodes]
> 22	```
> 23	
> 24	**Entities:**
> 25	- **autopilot_plans:** configuração de cadência per-user (modo, intervalo, produtos-alvo, redes, teto de custo). Fonte da verdade do "o quê e quando".
> 26	- **autopilot_cycles:** instância de execução de um plano (ledger: status, spend, planned_units, ponteiro p/ análise). Idempotente por (plan_id, cycle_number).
> 27	- **creative_metrics:** desempenho por criativo (`content_variant_id`), unificando cliques de afiliado + engajamento orgânico + receita de postback (Decisão 3).
> 28	- **vm_affiliate_products (reuse):** catálogo ML com `commission_value`/`trend_score`/`profitability_score`/`image_url` — fonte do produto-alvo.
> 29	- **scheduled_posts (reuse + `cycle_id`):** fila de publicação; agora rastreável ao ciclo.
> 30	- **affiliate_links / optimization_policy / content_library / mcorch_nodes (reuse):** receita, política de melhoria, conteúdo, memória.
> 31	
> 32	---
> 33	
> 34	## 2. Logical Data Model
> 35	
> 36	### Table: `autopilot_plans`
> 37	
> 38	| Column | Type | Nullable | Default | FK | Description |
> 39	|--------|------|----------|---------|-----|------------|
> 40	| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | — | PK |
> 41	| `user_id` | `uuid` | NOT NULL | — | `auth.users.id` | Tenant isolation |
> 42	| `project_id` | `uuid` | NULL | — | — | Project scope opcional |
> 43	| `name` | `text` | NOT NULL | — | — | Nome do plano |
> 44	| `mode` | `text` | NOT NULL | — | — | `all_at_once` \| `every_n_days` |
> 45	| `interval_days` | `int` | NULL | `3` | — | Req. se `every_n_days`; 1–30 |
> 46	| `target_product_ids` | `text[]` | NOT NULL | — | → `vm_affiliate_products.external_id` | ≥ 1 produto (chave canônica `external_id`) |
> 47	| `platforms` | `text[]` | NOT NULL | — | — | ⊆ {wordpress,linkedin,twitter} (MVP) |
> 48	| `budget_cap_mco` | `int` | NOT NULL | — | — | Teto de custo por ciclo (gate FR-VA-007) |
> 49	| `daily_cap_mco` | `int` | NOT NULL | `200` | — | Cap diário global por tenant (FR-VA-021); safety vision-mcp |
> 50	| `min_balance_mco` | `int` | NOT NULL | `10` | — | Piso de saldo p/ disparar |
> 51	| `hitl_required` | `boolean` | NOT NULL | `false` | — | Gate HITL opcional (FR-VA-020); default off = autônomo |
> 52	| `ab_variants` | `int` | NOT NULL | `1` | — | Nº de variantes A/B por criativo (FR-VA-019); 1 = sem A/B |
> 53	| `is_active` | `boolean` | NOT NULL | `false` | — | Cadência ligada |
> 54	| `next_run_at` | `timestamptz` | NULL | — | — | Próximo disparo (cron) |
> 55	| `created_at` | `timestamptz` | NOT NULL | `now()` | — | Audit |
> 56	| `updated_at` | `timestamptz` | NOT NULL | `now()` | — | Audit |
> 57	
> 58	### Table: `autopilot_cycles`
> 59	
> 60	| Column | Type | Nullable | Default | FK | Description |
> 61	|--------|------|----------|---------|-----|------------|
> 62	| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | — | PK |
> 63	| `plan_id` | `uuid` | NOT NULL | — | `autopilot_plans(id,user_id)` | Plano pai (FK COMPOSTA tenant-escopada com `user_id`) |
> 64	| `user_id` | `uuid` | NOT NULL | — | `auth.users.id` | Tenant (FK real + parte da FK composta) |
> 65	| `cycle_number` | `int` | NOT NULL | — | — | Sequencial por plano |
> 66	| `status` | `text` | NOT NULL | `running` | — | running\|completed\|aborted_budget\|aborted_daily_cap\|failed |
> 67	| `spend_mco` | `int` | NOT NULL | `0` | — | projetado pré-debitado |
> 68	| `refunded_mco` | `int` | NOT NULL | `0` | — | creditado de volta no finalize |
> 69	| `planned_units` | `int` | NOT NULL | `0` | — | nº criativos planejados |
> 70	| `analysis_node_id` | `uuid` | NULL | — | `mcorch_nodes.id` | Nó de observação do ciclo |
> 71	| `debited_at` | `timestamptz` | NULL | — | — | estado do pré-débito (idempotência) |
> 72	| `refunded_at` | `timestamptz` | NULL | — | — | estado do refund (finalize roda 1×) |
> 73	| `started_at` | `timestamptz` | NOT NULL | `now()` | — | — |
> 74	| `completed_at` | `timestamptz` | NULL | — | — | — |
> 75	| — | — | — | — | — | **UNIQUE (plan_id, cycle_number)** |
> 76	
> 77	### Table: `creative_metrics`
> 78	
> 79	| Column | Type | Nullable | Default | FK | Description |
> 80	|--------|------|----------|---------|-----|------------|
> 81	| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | — | PK |
> 82	| `user_id` | `uuid` | NOT NULL | — | `auth.users.id` | Tenant (FK real + parte da FK composta) |
> 83	| `cycle_id` | `uuid` | NULL | — | `autopilot_cycles(id,user_id)` | Ciclo de origem (FK COMPOSTA tenant-escopada com `user_id`) |
> 84	| `content_variant_id` | `uuid` | NOT NULL | — | ref. lógica → `content_library.id` (sem FK física) | Criativo medido (= a linha de `content_library`; sem FK p/ retenção independente §7; propagado a `affiliate_links.content_id`) |
> 85	| `product_id` | `text` | NULL | — | → `vm_affiliate_products.external_id` | Produto promovido (chave canônica `external_id`) |
> 86	| `platform` | `text` | NULL | — | — | Rede |
> 87	| `source` | `text` | NOT NULL | — | — | affiliate_click\|organic\|postback |
> 88	| `impressions` | `int` | NOT NULL | `0` | — | — |
> 89	| `engagements` | `int` | NOT NULL | `0` | — | likes/shares/comments |
> 90	| `affiliate_clicks` | `int` | NOT NULL | `0` | — | do click ledger |
> 91	| `revenue_cents` | `int` | NOT NULL | `0` | — | do postback |
> 92	| `collected_at` | `timestamptz` | NOT NULL | `now()` | — | — |
> 93	| — | — | — | — | — | **UNIQUE (content_variant_id, source)** |
> 94	
> 95	> Nenhuma das 3 tabelas carrega `embedding`/`stability_score` — não são nós de conhecimento diretos. A memória semântica entra via `mcorch_nodes` (§4).
> 96	
> 97	---
> 98	
> 99	## 3. Supabase Physical Schema Stubs
> 100	
> 101	```sql
> 102	-- ============================================================
> 103	-- MIGRATION: <ts>_viral_autopilot_schema.sql  (split em 4 arquivos — ver 05-sdd §7)
> 104	-- ============================================================
> 105	-- autopilot_plans / autopilot_cycles / creative_metrics + ALTER scheduled_posts
> 106	-- (stubs CREATE TABLE completos em 05-sdd.md §7)
> 107	
> 108	-- RLS (default-deny → own-row)
> 109	ALTER TABLE public.autopilot_plans     ENABLE ROW LEVEL SECURITY;
> 110	ALTER TABLE public.autopilot_cycles    ENABLE ROW LEVEL SECURITY;
> 111	ALTER TABLE public.creative_metrics    ENABLE ROW LEVEL SECURITY;
> 112	
> 113	CREATE POLICY "autopilot_plans: users read own"    ON public.autopilot_plans  FOR SELECT USING (user_id = auth.uid());
> 114	CREATE POLICY "autopilot_plans: users write own"   ON public.autopilot_plans  FOR INSERT WITH CHECK (user_id = auth.uid());
> 115	CREATE POLICY "autopilot_plans: users update own"  ON public.autopilot_plans  FOR UPDATE USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());
> 116	-- DELETE bloqueado p/ authenticated via RESTRICTIVE (espelha 20260413183335); só service-role remove (LGPD cascade):
> 117	CREATE POLICY "autopilot_plans: no client delete" ON public.autopilot_plans AS RESTRICTIVE FOR DELETE USING (false);
> 118	
> 119	CREATE POLICY "autopilot_cycles: users read own"   ON public.autopilot_cycles FOR SELECT USING (user_id = auth.uid());
> 120	CREATE POLICY "creative_metrics: users read own"   ON public.creative_metrics FOR SELECT USING (user_id = auth.uid());
> 121	-- Tabelas FINANCEIRAS: só SELECT own + RESTRICTIVE no-delete explícito (CLAUDE.md exige RESTRICTIVE
> 122	-- em tabelas financeiras). INSERT/UPDATE não têm policy permissiva → default-deny p/ authenticated;
> 123	-- só service-role (runner/coletor, que bypassa RLS) escreve. Default-deny INTENCIONAL e explícito.
> 124	CREATE POLICY "autopilot_cycles: no client delete"  ON public.autopilot_cycles  AS RESTRICTIVE FOR DELETE USING (false);
> 125	CREATE POLICY "creative_metrics: no client delete"  ON public.creative_metrics  AS RESTRICTIVE FOR DELETE USING (false);
> 126	-- Integridade de tenant: user_id é FK real → auth.users; cycles e creative_metrics usam FK COMPOSTA
> 127	-- tenant-escopada ((plan_id,user_id)→plans; (cycle_id,user_id)→cycles) — ver 05-sdd §7.
> 128	-- ⚠️ Toda esta migration passa /security-review antes do commit (FMEA-011 cross-tenant).
> 129	
> 130	-- Índices
> 131	CREATE INDEX autopilot_plans_due_idx     ON public.autopilot_plans (next_run_at) WHERE is_active;
> 132	CREATE INDEX autopilot_cycles_plan_idx   ON public.autopilot_cycles (plan_id);
> 133	CREATE INDEX creative_metrics_cycle_idx  ON public.creative_metrics (cycle_id);
> 134	CREATE INDEX creative_metrics_variant_idx ON public.creative_metrics (content_variant_id);
> 135	
> 136	-- Updated-at trigger (reusa update_updated_at_column existente)
> 137	CREATE TRIGGER set_autopilot_plans_updated_at
> 138	  BEFORE UPDATE ON public.autopilot_plans
> 139	  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
> 140	```
> 141	
> 142	---
> 143	
> 144	## 4. GraphRAG Knowledge Nodes
> 145	
> 146	### Node Types Introduced
> 147	
> 148	| node_type | Title Pattern | Content Fields | Embedding Source |
> 149	|-----------|--------------|----------------|-----------------|
> 150	| `observation` (reuse) | `autopilot-cycle-<plan>-<n>-<date>` | resumo do ciclo: produto, redes, desempenho agregado, política aplicada | `${title} ${content}` via `embed-mcorch-node` |
> 151	
> 152	> Não introduz `node_type` novo — reusa `observation`. A novidade é o **edge** que liga ciclos para a memória de aprendizado ser navegável.
> 153	
> 154	### Edge Types Introduced
> 155	
> 156	| Edge relationship | Source node_type | Target node_type | Metadata |
> 157	|-------------------|-----------------|-----------------|----------|
> 158	| `OPTIMIZES_FROM` (new) | `observation` (ciclo N+1) | `observation` (ciclo N) | `{ lift, applied_features }` — o ciclo N+1 derivou aprendizado do ciclo N |
> 159	| `ATTRIBUTES_REVENUE_TO` (reuse) | `revenue` event | `content_mesh_asset`/criativo | `{ revenue_cents, order_id }` — atribuição por criativo |
> 160	| `PROMOTES` (new, optional) | `observation` (ciclo) | product node | `{ product_id, commission_value }` |
> 161	
> 162	### Embedding Trigger
> 163	
> 164	```typescript
> 165	// Após fechar o ciclo (autopilot-run / autopilot-analyze), insere observation node:
> 166	await supabase.functions.invoke('embed-mcorch-node', {
> 167	  body: { node_id: cycleNode.id, content: `${title} ${cycleSummary}` }
> 168	})
> 169	// O trigger trg_mcorch_embed_on_insert (pg_net) também dispara automaticamente.
> 170	```
> 171	
> 172	### FSRS-6 Parameters
> 173	
> 174	| Field | Initial Value | Decay Rule |
> 175	|-------|--------------|------------|
> 176	| `stability_score` (no `mcorch_nodes` do ciclo) | `0.7` (observação operacional relevante) | Decai por `decay_mcorch_stability()` (migration `20260425190000`) |
> 177	| `revenue_impact` (no nó do ciclo) | `SUM(creative_metrics.revenue_cents)/100` do ciclo | Atualizado quando postback credita receita atribuída ao ciclo |
> 178	
> 179	---
> 180	
> 181	## 5. Tenant Isolation Map
> 182	
> 183	| Table | `user_id` scope | `project_id` scope | System rows (user_id IS NULL) |
> 184	|-------|----------------|-------------------|-------------------------------|
> 185	| `autopilot_plans` | ✅ Required | Optional | No |
> 186	| `autopilot_cycles` | ✅ Required (denorm) | via plano | No |
> 187	| `creative_metrics` | ✅ Required | via ciclo | No |
> 188	| `scheduled_posts` (reuse) | ✅ Required (existente) | — | No |
> 189	| `vm_affiliate_products` (reuse) | catálogo compartilhado (read `USING(true)`) | — | Sim (shared) |
> 190	| `mcorch_nodes` (reuse) | Optional | Optional | Sim (system nodes) |
> 191	
> 192	---
> 193	
> 194	## 6. Data Quality Rules
> 195	
> 196	| Table | Column | Rule | Violation Message (PT-BR) |
> 197	|-------|--------|------|--------------------------|
> 198	| `autopilot_plans` | `mode` | ∈ {all_at_once, every_n_days} | "Modo de cadência inválido." |
> 199	| `autopilot_plans` | `interval_days` | 1–30; obrigatório se `every_n_days` | "Intervalo deve ser entre 1 e 30 dias." |
> 200	| `autopilot_plans` | `target_product_ids` | cardinalidade ≥ 1; ids existem no catálogo | "Selecione ao menos um produto-alvo válido." |
> 201	| `autopilot_plans` | `platforms` | ⊆ redes suportadas (MVP); ≥ 1 | "Selecione ao menos uma rede suportada." |
> 202	| `autopilot_plans` | `budget_cap_mco` | ≥ custo mínimo de 1 ciclo | "Teto de custo abaixo do mínimo de um ciclo." |
> 203	| `autopilot_cycles` | `(plan_id, cycle_number)` | UNIQUE (idempotência) | "Ciclo já existente para este plano." |
> 204	| `creative_metrics` | `(content_variant_id, source)` | UNIQUE (upsert por fonte) | — |
> 205	| `creative_metrics` | `revenue_cents`/`affiliate_clicks` | ≥ 0 | "Métrica não pode ser negativa." |
> 206	
> 207	---
> 208	
> 209	## 7. Retention & Archival Policy
> 210	
> 211	| Data | Retention Period | Archival Strategy | Deletion Trigger |
> 212	|------|-----------------|-------------------|-----------------|
> 213	| `autopilot_plans` | enquanto ativo + 1 ano | nenhum | CASCADE no delete do user (LGPD) |
> 214	| `autopilot_cycles` | 18 meses | sumário agregado em `mcorch_nodes` (observation) | CASCADE no delete do plano |
> 215	| `creative_metrics` | 18 meses | agregado por ciclo preservado no nó | CASCADE no delete do ciclo |
> 216	| `mcorch_nodes` (observation de ciclo) | Indefinido (memória) | FSRS-6 decay de stability | LGPD erase por tenant |
> 217	| `infra_health_logs` (eventos autopilot) | 90 dias | sem archival | Cron purge |
> 218	
> 219	> **LGPD:** o delete do tenant (`auth.users`) cascateia plans→cycles→creative_metrics. Métricas guardam só agregados (sem PII de terceiros que engajaram).
> 220	
> 221	---
> 222	
> 223	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 224	
> ```

## 🤖 Claude *(17:45:25)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: viral-autopilot creative_metrics — canonical per-creative performance ledger (FR-VA-009).
> 2	-- BoK SSOT: docs/bok/viral-autopilot/06-data-model.md (creative_metrics) + 04-frd.md (FR-VA-009 unified
> 3	--           3-signal metrics: affiliate_clicks + organic engagement + revenue — Decisão 3 "combo").
> 4	-- SOP: docs/processes/[[viral-autopilot-product-aware-monetization|viral-autopilot-product-aware-monetization]].md (Lei 2 — written before this code).
> 5	--
> 6	-- WHY a NEW table (not campaign_metrics): public.campaign_metrics ALREADY EXISTS (per-platform telemetry,
> 7	-- consumed by self-optimize / ROIWidget / AnalyticsPage) and is keyed by campaign, NOT by creative. The
> 8	-- viral loop needs metrics keyed by the INDIVIDUAL creative (content_variant_id = content_library.id) so the
> 9	-- future R3 analyzer (FR-VA-010) can rank creative-by-creative and the per-creative attribution (FR-VA-017)
> 10	-- has a home. campaign_metrics is left UNTOUCHED (deprecation is a later concern; no consumer is broken here).
> 11	--
> 12	-- Fatia 1 role: the generator (orchestrate-step, service-role) writes ONE baseline row per creative
> 13	-- (source='organic', zeros) at generation time — this seeds the content_variant_id↔product↔platform key that
> 14	-- the future collector (FR-VA-008) and analyzer (FR-VA-010) build on. The cron/cadence layer is NOT part of
> 15	-- this migration: cycle_id is reserved NULL-able (NO physical FK yet — autopilot_cycles does not exist) so
> 16	-- the cadence Fatia can add the composite tenant-scoped FK later with zero churn here.
> 17	--
> 18	-- Tenancy (mirrors vision_jobs 20260615160000 + lead_core 20260603000000): SELECT-own only; NO write policy
> 19	-- for authenticated → default-deny (the generator writes via the service key, which bypasses RLS). A tenant
> 20	-- can never forge a metric for another tenant nor fabricate revenue. Financial table → RESTRICTIVE no-delete
> 21	-- (clients cannot erase the ledger). Passes /security-review (FMEA-011 / FMEA-VA-001 cross-tenant family).
> 22	
> 23	CREATE TABLE IF NOT EXISTS public.creative_metrics (
> 24	  id                 uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
> 25	  user_id            uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 26	  cycle_id           uuid,                          -- reserved for the cadence Fatia (autopilot_cycles); NO FK yet
> 27	  content_variant_id uuid        NOT NULL,          -- logical ref to content_library.id; NO physical FK (independent
> 28	                                                    -- 18-month retention per Data Model §7 — content can be pruned
> 29	                                                    -- while its performance history is retained for the loop)
> 30	  product_id         text,                          -- = vm_affiliate_products.external_id (the featured product)
> 31	  platform           text,                          -- wordpress | linkedin | twitter
> 32	  source             text        NOT NULL DEFAULT 'organic'
> 33	                       CHECK (source IN ('affiliate_click','organic','postback')),
> 34	  impressions        int         NOT NULL DEFAULT 0 CHECK (impressions      >= 0),
> 35	  engagements        int         NOT NULL DEFAULT 0 CHECK (engagements      >= 0),
> 36	  affiliate_clicks   int         NOT NULL DEFAULT 0 CHECK (affiliate_clicks >= 0),
> 37	  revenue_cents      int         NOT NULL DEFAULT 0 CHECK (revenue_cents    >= 0),
> 38	  collected_at       timestamptz NOT NULL DEFAULT now(),
> 39	  created_at         timestamptz NOT NULL DEFAULT now(),
> 40	  -- One row per (creative, signal source): the baseline 'organic' row at generation, later upserted by the
> 41	  -- collector; 'affiliate_click' and 'postback' rows are written by their own writers (click ledger / postback).
> 42	  CONSTRAINT creative_metrics_variant_source_uniq UNIQUE (content_variant_id, source)
> 43	);
> 44	
> 45	ALTER TABLE public.creative_metrics ENABLE ROW LEVEL SECURITY;
> 46	
> 47	-- SELECT own only. No INSERT/UPDATE policy → authenticated default-deny; the generator/collector write via the
> 48	-- service key. A tenant reads its own creative performance (future dashboard FR-VA-015) and nothing else.
> 49	CREATE POLICY "creative_metrics_select_own" ON public.creative_metrics
> 50	  FOR SELECT USING (auth.uid() = user_id);
> 51	
> 52	-- Financial ledger → clients can NEVER delete a metric row (RESTRICTIVE forbids it even if a future permissive
> 53	-- policy is added). Mirrors the RESTRICTIVE pattern on financial/affiliate tables.
> 54	CREATE POLICY "creative_metrics_no_client_delete" ON public.creative_metrics
> 55	  AS RESTRICTIVE FOR DELETE USING (false);
> 56	
> 57	CREATE INDEX IF NOT EXISTS creative_metrics_variant_idx  ON public.creative_metrics (content_variant_id);
> 58	CREATE INDEX IF NOT EXISTS creative_metrics_user_idx     ON public.creative_metrics (user_id, collected_at DESC);
> 59	CREATE INDEX IF NOT EXISTS creative_metrics_cycle_idx    ON public.creative_metrics (cycle_id);
> 60	CREATE INDEX IF NOT EXISTS creative_metrics_product_idx  ON public.creative_metrics (product_id);
> 61	
> 62	COMMENT ON TABLE public.creative_metrics IS
> 63	  'Viral Autopilot canonical per-creative metrics ledger (FR-VA-009), keyed by content_variant_id '
> 64	  '(= content_library.id). Unifies 3 signals (affiliate_click/organic/postback — Decisão 3). SELECT-own RLS, '
> 65	  'service-role write (default-deny), RESTRICTIVE no client delete. Generator writes a baseline row at '
> 66	  'generation; collector/analyzer (R3) build on it. SOP [[viral-autopilot-product-aware-monetization|viral-autopilot-product-aware-monetization]].md.';
> 67	
> ```

## 🤖 Claude *(17:45:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== add_mco_coins body (does it ledger?) ===\"\nsed -n '/CREATE OR REPLACE FUNCTION public.add_mco_coins/,/\\$\\$;/p' supabase/migrations/20260505100000_add_pref_ai_model_and_rpc.sql 2>/dev/null | head -40\necho \"\"\necho \"=== SDD: begin/finalize_autopilot_cycle signatures + table DDL hints ===\"\ngrep -nE -A4 'begin_autopilot_cycle|finalize_autopilot_cycle|autopilot_plans|autopilot_cycles' docs/bok/viral-autopilot/05-sdd.md 2>/dev/null | head -70",
  "description": "add_mco_coins body + SDD RPC signatures"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === add_mco_coins body (does it ledger?) ===
> CREATE OR REPLACE FUNCTION public.add_mco_coins(
>   p_user_id UUID,
>   p_amount   INTEGER
> )
> RETURNS INTEGER
> LANGUAGE plpgsql
> SECURITY DEFINER
> SET search_path = public
> AS $$
> DECLARE
>   v_new_balance INTEGER;
> BEGIN
>   IF p_amount <= 0 THEN
>     RAISE EXCEPTION 'Amount must be positive';
>   END IF;
> 
>   UPDATE public.profiles
>     SET mco_balance = mco_balance + p_amount
>   WHERE id = p_user_id
>   RETURNING mco_balance INTO v_new_balance;
> 
>   IF v_new_balance IS NULL THEN
>     RAISE EXCEPTION 'User profile not found';
>   END IF;
> 
>   RETURN v_new_balance;
> END;
> $$;
> 
> === SDD: begin/finalize_autopilot_cycle signatures + table DDL hints ===
> 41:│  autopilot_plans (new)     │  │  OpenRouter/Groq (LLM, BYOK)    │
> 42:│  autopilot_cycles (new)    │  │  DALL·E/Nano Banana (image)     │
> 43-│  creative_metrics (new)    │  │  LinkedIn/X/WordPress (publish) │
> 44-│  scheduled_posts (reuse)   │  │  Mercado Livre/Pago (postback)  │
> 45-│  affiliate_links (reuse)   │  │  Apify (fetch-trends, v1.0)     │
> 46-│  optimization_policy(reuse)│  └─────────────────────────────────┘
> --
> 60:| `useAutopilot` | `useAutopilot.ts` | **FR-VA-014** | CRUD de `autopilot_plans`; lista ciclos; ROI por criativo; activate/pause | `['autopilot-plans']`, `['autopilot-cycles', planId]`, `['creative-metrics', cycleId]` |
> 61-
> 62-### 2.2 New Display Components (`src/components/autopilot/`)
> 63-
> 64-| Component | File | FR | Props | Hook consumed |
> --
> 103:| `autopilot_plans` | Table | Config de cadência per-user (FR-VA-001) | `<ts>_viral_autopilot_plans.sql` |
> 104:| `autopilot_cycles` | Table | Ledger de ciclo + spend + status (FR-VA-006) | `<ts>_viral_autopilot_cycles.sql` |
> 105-| `creative_metrics` | Table | Métricas unificadas por criativo (FR-VA-009) | `<ts>_viral_autopilot_creative_metrics.sql` |
> 106-| `scheduled_posts.cycle_id` | Column | Liga post ao ciclo (NFR-VA-007 auditabilidade) | `<ts>_scheduled_posts_cycle_id.sql` |
> 107-| `autopilot-cadence` | pg_cron | Disparo recorrente */15 (FR-VA-005) | dentro da migration de cron |
> 108-| `autopilot-collect` | pg_cron | Coleta de métricas (FR-VA-008) | dentro da migration de cron |
> 109:| `begin_autopilot_cycle(uuid, uuid, int)` | RPC (SECURITY DEFINER, service-role-only) | Atômico (advisory lock por user_id): checa cap diário + cap por ciclo + saldo, faz pré-débito (`deduct_mco_coins`) e abre `autopilot_cycles` running numa txn — anti-TOCTOU do cap diário (FR-VA-007/021) | `<ts>_begin_autopilot_cycle.sql` |
> 110:| `finalize_autopilot_cycle(uuid, int)` | RPC (SECURITY DEFINER, service-role-only) | Fecha ciclo + **credita** refund `(projected − actual)` via `add_mco_coins` (ledgered) na mesma txn; idempotente por `refunded_at IS NULL` (FR-VA-007); espelha `finalize_vision_job` | `<ts>_finalize_autopilot_cycle.sql` |
> 111-
> 112----
> 113-
> 114-## 3. Data Flow Diagrams
> --
> 129: │                 │                    │──[open cycle]─────────────────────────▶│ autopilot_cycles (running, spend_mco=projected)
> 130- │                 │                    │──[fan-out/produto×rede: service-role + x-autopilot-user-id + prepaid=true]─▶│
> 131- │                 │                    │                    │──[gen product-aware + feedback inject]─▶ LLM (BYOK por user_id)
> 132- │                 │                    │                    │  (prepaid → NÃO self-bill)
> 133- │                 │                    │                    │──[monetize all formats: content_id=content_variant_id]─▶ affiliate_links
> --
> 135: │                 │                    │──[finalize_autopilot_cycle(cycle_id, actual)]─▶│ RPC: terminal + CRÉDITO positivo do não-usado no mco_balance (1 txn; idempotente refunded_at; NUNCA deduct negativo)
> 136- │                 │                    │──[analyze INLINE pós-ciclo]───────────▶│ autopilot-analyze: creative_metrics(N) → optimization_policy(N) [feeds N+1]
> 137- │                 │◀──[re-arm next_run_at = now + interval]──────────────────────│
> 138- │                 │                    │   (auto-publish cron drains scheduled_posts → publish-*)
> 139- │                 │ (later, 6/6h) autopilot-collect: post_id → insights + cliques + receita → creative_metrics
> --
> 168://   ANTES de confiar no header x-autopilot-user-id (= autopilot_plans.user_id, server-trusted, NUNCA do body);
> 169-//   caminho "gerar agora" = JWT do user (getUser), asserir user.id === plan.user_id.
> 170-// Cost gate (FR-VA-007 + FR-VA-021) — atômico, ANTES do fan-out:
> 171-// → N_runs = |target_product_ids| × |platforms| × ab_variants        (fórmula canônica única)
> 172-// → projected = N_runs * ORCHESTRATION_RUN(10) + ANALYZE_COST(2)      // imagem JÁ no bundle de 10 (billing.ts:16-21)
> 173:// → CAP DIÁRIO (FR-VA-021): daily_spent = SELECT COALESCE(SUM(spend_mco),0) FROM autopilot_cycles
> 174-//     WHERE user_id = plan.user_id AND started_at::date = (now() AT TIME ZONE 'UTC')::date
> 175-//     AND status <> 'aborted_daily_cap';  if daily_spent + projected > plan.daily_cap_mco → 409 aborted_daily_cap (sem deduct)
> 176-// → if projected > plan.budget_cap_mco → 409 aborted_budget + pause plan (sem deduct)
> 177-// → balance check; if mco_balance < projected OR < min_balance → 402 insufficient_balance
> --
> 179://   'running' (spend_mco=projected, debited_at) acontecem DENTRO de UM RPC begin_autopilot_cycle
> 180-//   (SECURITY DEFINER service-role-only) com pg_advisory_xact_lock(hashtext(user_id::text)) — serializa
> 181-//   ciclos concorrentes do MESMO tenant, senão dois ciclos paralelos passariam o cap diário juntos
> 182-//   (read-then-act). O deduct_mco_coins (guarda mco_balance>=amount) protege o SALDO; o advisory lock
> 183-//   + o INSERT-antes-do-re-SELECT protege o AGREGADO diário. Retorna cycle_id OU motivo de abort.
> --
> 185:// → ao fechar: finalize_autopilot_cycle(cycle_id, actual) — RPC SECURITY DEFINER service-role-only,
> 186-//   idempotente (guarda refunded_at IS NULL), CREDITA o não-usado (projected - actual) no mco_balance
> 187-//   na MESMA transação (espelha finalize_vision_job). REFUND É CRÉDITO POSITIVO — deduct_mco_coins
> 188-//   rejeita p_amount<=0 (migration 20260603220000:45, anti-mint), então NÃO usar deduct negativo.
> 189-```
> --
> 203://   const { user_id, plan_id } = SELECT user_id, plan_id FROM autopilot_cycles WHERE id = previous_cycle_id
> 204-//   → usar ESSE user_id como p_user_id no deduct e como filtro de creative_metrics (RLS).
> 205-// Deduct ANALYZE_COST(2 mco) via deduct_mco_coins(user_id, 2) SOMENTE quando has_real_data === true;
> 206-//   has_real_data === false → 0 mco + log infra_health_logs event 'viral_autopilot_analyze_empty'.
> 207-```
> --
> 220:| `autopilot-analyze` | `tenant_id` forjado no body → deduct + leitura cross-tenant (IDOR) | Spoofing/Tampering | Critical | **NÃO aceitar `tenant_id`/`plan_id` no body**; derivar de `previous_cycle_id` (`SELECT user_id, plan_id FROM autopilot_cycles`, sob service-role) — identidade vem de **linha confiável**, não do body (mesmo princípio do `finalize_vision_job`; ≠ `lead-score`/`campaign-run` que derivam de user-JWT) |
> 221:| `autopilot_plans`/`_cycles`/`creative_metrics` | Leitura/escrita cross-tenant | Information Disclosure | Critical | RLS `user_id = auth.uid()`; crons usam service-role com filtro explícito por tenant derivado da linha |
> 222-| Cost gate (FR-VA-007) | Bypass do teto / saldo negativo entre check e deduct (TOCTOU) | Tampering | Critical | **Pré-débito atômico ÚNICO** de `N_runs×10+2` em `autopilot-run` ANTES do fan-out (não distribuído nos sub-runs) + refund do não-usado; `spend_mco` no ciclo; idempotência (plan_id, cycle_number) |
> ```

## 🤖 Claude *(17:47:54)*


## 🤖 Claude *(17:47:57)*

Contrato selado totalmente lido. A migration vai honrar o `06-data-model.md` exatamente — `autopilot_plans`/`autopilot_cycles` com as colunas/defaults selados, FK composta `(plan_id,user_id)`, RESTRICTIVE no-delete, e os 2 RPCs `begin/finalize_autopilot_cycle` espelhando o `finalize_vision_job`. Confirmando o timestamp livre antes de escrever (evita colisão de ordenação).

## 🤖 Claude *(17:48:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== latest 5 migration timestamps (pick next > max) ===\"\nls supabase/migrations/ | sort | tail -5\necho \"\"\necho \"=== confirm add_mco_coins is service-role-only NOW (for finalize to call) ===\"\ngrep -rnE 'add_mco_coins\\(uuid, integer\\)' supabase/migrations/20260520150000_admin_user_lifecycle.sql\necho \"\"\necho \"=== does update_updated_at_column() exist (trigger reuse)? ===\"\ngrep -rlE 'FUNCTION public\\.update_updated_at_column' supabase/migrations/ | head -1\necho \"\"\necho \"=== mcoin_transactions columns (for refund ledger row) ===\"\ngrep -rnE -A8 'CREATE TABLE.*mcoin_transactions' supabase/migrations/ | head -20",
  "description": "Verify timestamp, RPC grants, trigger fn, ledger columns"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === latest 5 migration timestamps (pick next > max) ===
> 20260615170000_infra_health_logs_metadata.sql
> 20260615180000_vision_mcp_access_tokens.sql
> 20260615190000_vision_mcp_artifacts.sql
> 20260615200000_vision_mcp_erase_rpc.sql
> 20260619140000_viral_autopilot_creative_metrics.sql
> 
> === confirm add_mco_coins is service-role-only NOW (for finalize to call) ===
> supabase/migrations/20260520150000_admin_user_lifecycle.sql:17:REVOKE EXECUTE ON FUNCTION public.add_mco_coins(uuid, integer) FROM authenticated;
> supabase/migrations/20260520150000_admin_user_lifecycle.sql:18:GRANT  EXECUTE ON FUNCTION public.add_mco_coins(uuid, integer) TO service_role;
> 
> === does update_updated_at_column() exist (trigger reuse)? ===
> supabase/migrations/20260531210000_meta_ads_metrics.sql
> 
> === mcoin_transactions columns (for refund ledger row) ===
> supabase/migrations/20260508100000_mcoin_transactions.sql:5:CREATE TABLE IF NOT EXISTS mcoin_transactions (
> supabase/migrations/20260508100000_mcoin_transactions.sql-6-  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> supabase/migrations/20260508100000_mcoin_transactions.sql-7-  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> supabase/migrations/20260508100000_mcoin_transactions.sql-8-  action TEXT NOT NULL,
> supabase/migrations/20260508100000_mcoin_transactions.sql-9-  amount INTEGER NOT NULL,
> supabase/migrations/20260508100000_mcoin_transactions.sql-10-  created_at TIMESTAMPTZ DEFAULT NOW(),
> supabase/migrations/20260508100000_mcoin_transactions.sql-11-  context JSONB DEFAULT '{}',
> supabase/migrations/20260508100000_mcoin_transactions.sql-12-  project_id UUID REFERENCES projects(id)
> supabase/migrations/20260508100000_mcoin_transactions.sql-13-);
> ```

## 🤖 Claude *(17:50:26)*


## 🤖 Claude *(17:50:28)*

Timestamp livre confirmado (max = `20260619140000` → uso `20260620120000+`), `add_mco_coins` service-role-only, `update_updated_at_column()` e colunas de `mcoin_transactions` confirmadas. Escrevendo as 4 migrations da fatia — cada uma honrando o schema selado do `06-data-model.md` e documentando no header qualquer escolha de engenharia (Lei 1).

## 🤖 Claude *(17:50:50)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120000_viral_autopilot_plans.sql",
  "content": "-- Migration: viral-autopilot autopilot_plans \u2014 per-user cadence config (FR-VA-001 / FR-VA-005).\n-- BoK SSOT: docs/bok/viral-autopilot/06-data-model.md \u00a72 (autopilot_plans) + 05-sdd.md \u00a77.\n-- SOP (Lei 2 \u2014 written BEFORE this code): docs/processes/[[autopilot-cron-identity|autopilot-cron-identity]].md.\n--\n-- The \"what & when\" source of truth for the autonomous viral loop: which products, which networks, how often,\n-- and the MANDATORY safety caps (budget_cap_mco per cycle, daily_cap_mco per tenant, min_balance_mco floor).\n-- Caps are NOT NULL by design \u2014 the cron NEVER runs without a kill-switch (FMEA-VA-001 RPN 128 / BR-RISK-001).\n--\n-- Tenancy: RLS user_id = auth.uid() (own CRUD); RESTRICTIVE no-delete for authenticated (only service-role\n-- removes, e.g. LGPD cascade). UNIQUE(id,user_id) is the target of the tenant-scoped composite FK from\n-- autopilot_cycles (next migration). Passes /security-review (FMEA-011 / FMEA-VA-001 cross-tenant family).\n--\n-- Engineering notes (deviations from sealed stub, declared per Lei 1):\n--   * CHECKs added beyond the data-model stub (mode enum, interval 1-30, platforms subset, caps >= 12 = 1-cycle\n--     floor [1 run 10 + analyze 2], ab_variants 1-5) materialize the \u00a76 Data Quality rules at the DB layer.\n--   * project_id has NO FK (matches data-model \u00a72 \"FK \u2014\"); kept as a plain scoping uuid.\n\nCREATE TABLE IF NOT EXISTS public.autopilot_plans (\n  id                 uuid        PRIMARY KEY DEFAULT gen_random_uuid(),\n  user_id            uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,\n  project_id         uuid,\n  name               text        NOT NULL,\n  mode               text        NOT NULL CHECK (mode IN ('all_at_once','every_n_days')),\n  interval_days      int         DEFAULT 3 CHECK (interval_days IS NULL OR (interval_days BETWEEN 1 AND 30)),\n  target_product_ids text[]      NOT NULL CHECK (array_length(target_product_ids, 1) >= 1),\n  platforms          text[]      NOT NULL CHECK (array_length(platforms, 1) >= 1\n                                   AND platforms <@ ARRAY['wordpress','linkedin','twitter']),\n  budget_cap_mco     int         NOT NULL CHECK (budget_cap_mco  >= 12),  -- >= 1 cycle (1 run 10 + analyze 2)\n  daily_cap_mco      int         NOT NULL DEFAULT 200 CHECK (daily_cap_mco >= 12),\n  min_balance_mco    int         NOT NULL DEFAULT 10  CHECK (min_balance_mco >= 0),\n  hitl_required      boolean     NOT NULL DEFAULT false,\n  ab_variants        int         NOT NULL DEFAULT 1   CHECK (ab_variants BETWEEN 1 AND 5),\n  is_active          boolean     NOT NULL DEFAULT false,\n  next_run_at        timestamptz,\n  created_at         timestamptz NOT NULL DEFAULT now(),\n  updated_at         timestamptz NOT NULL DEFAULT now(),\n  -- mode every_n_days REQUIRES interval_days (Data Quality \u00a76).\n  CONSTRAINT autopilot_plans_interval_req CHECK (mode <> 'every_n_days' OR interval_days IS NOT NULL),\n  -- anchor for the tenant-scoped composite FK from autopilot_cycles (id,user_id).\n  CONSTRAINT autopilot_plans_id_user_uniq UNIQUE (id, user_id)\n);\n\nALTER TABLE public.autopilot_plans ENABLE ROW LEVEL SECURITY;\n\nCREATE POLICY \"autopilot_plans_select_own\" ON public.autopilot_plans\n  FOR SELECT USING (auth.uid() = user_id);\nCREATE POLICY \"autopilot_plans_insert_own\" ON public.autopilot_plans\n  FOR INSERT WITH CHECK (auth.uid() = user_id);\nCREATE POLICY \"autopilot_plans_update_own\" ON public.autopilot_plans\n  FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);\n-- Clients can NEVER delete a plan (RESTRICTIVE forbids it even if a permissive policy is later added);\n-- only service-role (LGPD cascade) removes.\nCREATE POLICY \"autopilot_plans_no_client_delete\" ON public.autopilot_plans\n  AS RESTRICTIVE FOR DELETE USING (false);\n\n-- Due-plan scan index (cron): active plans whose next_run_at has passed.\nCREATE INDEX IF NOT EXISTS autopilot_plans_due_idx  ON public.autopilot_plans (next_run_at) WHERE is_active;\nCREATE INDEX IF NOT EXISTS autopilot_plans_user_idx ON public.autopilot_plans (user_id, created_at DESC);\n\nCREATE TRIGGER set_autopilot_plans_updated_at\n  BEFORE UPDATE ON public.autopilot_plans\n  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();\n\nCOMMENT ON TABLE public.autopilot_plans IS\n  'Viral Autopilot cadence config per user (FR-VA-001/005). Mandatory safety caps (budget/daily/min_balance) \u2014 '\n  'the cron never runs without a kill-switch. SELECT/INSERT/UPDATE own, RESTRICTIVE no client delete. '\n  'UNIQUE(id,user_id) anchors the tenant-scoped composite FK from autopilot_cycles. SOP [[autopilot-cron-identity|autopilot-cron-identity]].md.';\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120000_viral_autopilot_plans.sql (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(17:51:07)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120100_viral_autopilot_cycles.sql",
  "content": "-- Migration: viral-autopilot autopilot_cycles \u2014 per-cycle execution ledger (FR-VA-006 / FR-VA-007).\n-- BoK SSOT: docs/bok/viral-autopilot/06-data-model.md \u00a72 (autopilot_cycles) + 05-sdd.md \u00a77.\n-- SOP (Lei 2): docs/processes/[[autopilot-cron-identity|autopilot-cron-identity]].md.\n--\n-- One row per cadence cycle: the FINANCIAL ledger of a run (status, spend_mco pre-debited, refunded_mco credited\n-- on finalize, planned_units, debited_at/refunded_at idempotency stamps). Idempotent by (plan_id, cycle_number).\n-- The pre-debit/refund LOGIC lives in begin_/finalize_autopilot_cycle (next 2 migrations) \u2014 this is the schema.\n--\n-- Tenancy: user_id is a REAL FK to auth.users AND part of the tenant-scoped COMPOSITE FK\n-- (plan_id,user_id) -> autopilot_plans(id,user_id) \u2014 a cycle can never point at another tenant's plan (mirrors\n-- Marketing Hub campaign_steps composite FK). SELECT-own RLS; INSERT/UPDATE have NO permissive policy \u2192\n-- authenticated default-deny (only the service-role runner/RPCs write). Financial table \u2192 RESTRICTIVE no-delete.\n-- UNIQUE(id,user_id) anchors the composite FK from creative_metrics (closed at the end of this file).\n\nCREATE TABLE IF NOT EXISTS public.autopilot_cycles (\n  id               uuid        PRIMARY KEY DEFAULT gen_random_uuid(),\n  user_id          uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,\n  plan_id          uuid        NOT NULL,\n  cycle_number     int         NOT NULL,\n  status           text        NOT NULL DEFAULT 'running'\n                     CHECK (status IN ('running','completed','aborted_budget','aborted_daily_cap','failed')),\n  spend_mco        int         NOT NULL DEFAULT 0 CHECK (spend_mco     >= 0),\n  refunded_mco     int         NOT NULL DEFAULT 0 CHECK (refunded_mco  >= 0),\n  planned_units    int         NOT NULL DEFAULT 0 CHECK (planned_units >= 0),\n  analysis_node_id uuid,\n  debited_at       timestamptz,\n  refunded_at      timestamptz,\n  started_at       timestamptz NOT NULL DEFAULT now(),\n  completed_at     timestamptz,\n  -- refund can NEVER exceed what was committed (defense-in-depth vs a negative-refund mint).\n  CONSTRAINT autopilot_cycles_refund_le_spend CHECK (refunded_mco <= spend_mco),\n  CONSTRAINT autopilot_cycles_plan_cycle_uniq UNIQUE (plan_id, cycle_number),\n  CONSTRAINT autopilot_cycles_id_user_uniq    UNIQUE (id, user_id),\n  -- tenant-scoped composite FK: the cycle's (plan_id,user_id) must match a plan owned by the SAME tenant.\n  CONSTRAINT autopilot_cycles_plan_fk FOREIGN KEY (plan_id, user_id)\n    REFERENCES public.autopilot_plans (id, user_id) ON DELETE CASCADE\n);\n\nALTER TABLE public.autopilot_cycles ENABLE ROW LEVEL SECURITY;\n\n-- SELECT own only; INSERT/UPDATE default-deny (the service-role RPCs write). Financial \u2192 RESTRICTIVE no-delete.\nCREATE POLICY \"autopilot_cycles_select_own\" ON public.autopilot_cycles\n  FOR SELECT USING (auth.uid() = user_id);\nCREATE POLICY \"autopilot_cycles_no_client_delete\" ON public.autopilot_cycles\n  AS RESTRICTIVE FOR DELETE USING (false);\n\nCREATE INDEX IF NOT EXISTS autopilot_cycles_plan_idx     ON public.autopilot_cycles (plan_id, cycle_number DESC);\nCREATE INDEX IF NOT EXISTS autopilot_cycles_user_day_idx ON public.autopilot_cycles (user_id, started_at);\n\nCOMMENT ON TABLE public.autopilot_cycles IS\n  'Viral Autopilot per-cycle financial ledger (FR-VA-006/007). spend_mco pre-debited by begin_autopilot_cycle, '\n  'refunded_mco credited by finalize_autopilot_cycle (idempotent). Tenant-scoped composite FK to autopilot_plans. '\n  'SELECT-own, service-role write (default-deny), RESTRICTIVE no client delete. SOP autopilot-cron-identity.md.';\n\n-- \u2500\u2500 Close the deferred composite FK from creative_metrics (Fatia 1 left cycle_id NULL-able, NO FK) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- Now that autopilot_cycles exists, wire the tenant-scoped composite FK (cycle_id,user_id) -> cycles(id,user_id).\n-- MATCH SIMPLE (default): rows with cycle_id NULL (Fatia 1 baseline rows) stay valid (FK skipped when any col NULL).\n-- ON DELETE CASCADE: erasing a cycle erases its metrics (Data Model \u00a77 retention). Idempotent guard so a re-run\n-- of this migration does not error on the already-present constraint.\nDO $$\nBEGIN\n  IF NOT EXISTS (\n    SELECT 1 FROM pg_constraint WHERE conname = 'creative_metrics_cycle_fk'\n  ) THEN\n    ALTER TABLE public.creative_metrics\n      ADD CONSTRAINT creative_metrics_cycle_fk FOREIGN KEY (cycle_id, user_id)\n        REFERENCES public.autopilot_cycles (id, user_id) ON DELETE CASCADE;\n  END IF;\nEND $$;\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120100_viral_autopilot_cycles.sql (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(17:51:33)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120200_begin_autopilot_cycle.sql",
  "content": "-- Migration: begin_autopilot_cycle RPC \u2014 atomic cap-check + single pre-debit + open cycle (FR-VA-007 / FR-VA-021).\n-- BoK SSOT: docs/bok/viral-autopilot/05-sdd.md \u00a72 (RPC table line 109 + cost-gate notes lines ~170-183).\n-- SOP (Lei 2): docs/processes/[[autopilot-cron-identity|autopilot-cron-identity]].md.\n--\n-- THE anti-TOCTOU heart of the cost guardrail. Under pg_advisory_xact_lock(hashtext(user_id)) \u2014 which serializes\n-- concurrent begins for the SAME tenant so two parallel cycles cannot both slip under the daily cap \u2014 it:\n--   1. loads the plan's caps TENANT-SCOPED (plan must belong to p_user_id \u2014 cross-tenant attempt \u2192 not found),\n--   2. checks budget cap (per cycle), balance + min_balance floor, daily cap (sum of today's committed spend),\n--   3. on ANY breach \u2192 RETURNS an abort reason WITHOUT debiting (caller pauses plan / returns 409/402),\n--   4. on OK \u2192 INSERTs the cycle (status running, spend_mco=projected, debited_at) and PERFORMs the SINGLE\n--      deduct_mco_coins(projected) in the SAME transaction (sub-runs are prepaid \u2192 never self-bill).\n-- Refund is NEVER here \u2014 it is the positive credit in finalize_autopilot_cycle. deduct_mco_coins rejects\n-- p_amount<=0 (anti-mint, 20260603220000:45), so there is no negative-deduct path anywhere.\n--\n-- Identity (OTD-VA-008): service-role-only (REVOKE authenticated/anon). The caller (autopilot-run) has already\n-- proven service-role in-function and resolved p_user_id from the SERVER-TRUSTED plan row, never the request body.\n--\n-- Engineering notes (declared per Lei 1): the sealed stub hints (uuid,uuid,int); a 4th p_planned_units (DEFAULT 0)\n-- is added \u2014 backward-compatible with a 3-arg call \u2014 so the cycle row records N_runs without a follow-up UPDATE.\n-- Aborts are NOT persisted as cycle rows (the status enum has no 'insufficient_balance'); the caller logs the\n-- abort to infra_health_logs (telemetry) \u2014 every FR requirement (\"aborta sem deduzir\", pause plan, 409/402) holds.\n\nCREATE OR REPLACE FUNCTION public.begin_autopilot_cycle(\n  p_plan_id       uuid,\n  p_user_id       uuid,\n  p_projected_mco int,\n  p_planned_units int DEFAULT 0\n)\nRETURNS jsonb\nLANGUAGE plpgsql\nSECURITY DEFINER\nSET search_path = ''\nAS $$\nDECLARE\n  v_budget_cap   int;\n  v_daily_cap    int;\n  v_min_balance  int;\n  v_balance      int;\n  v_daily_spent  int;\n  v_cycle_number int;\n  v_cycle_id     uuid;\nBEGIN\n  IF p_projected_mco IS NULL OR p_projected_mco <= 0 THEN\n    RAISE EXCEPTION 'begin_autopilot_cycle: projected must be positive, got %', p_projected_mco\n      USING errcode = '22023';\n  END IF;\n\n  -- Serialize concurrent cycles for THIS tenant (anti-TOCTOU on the daily-cap aggregate). Transaction-scoped.\n  PERFORM pg_advisory_xact_lock(hashtext(p_user_id::text));\n\n  -- Tenant-scoped plan load: the plan MUST belong to p_user_id (cross-tenant attempt \u2192 not found \u2192 abort).\n  SELECT budget_cap_mco, daily_cap_mco, min_balance_mco\n    INTO v_budget_cap, v_daily_cap, v_min_balance\n    FROM public.autopilot_plans\n   WHERE id = p_plan_id AND user_id = p_user_id;\n  IF NOT FOUND THEN\n    RAISE EXCEPTION 'begin_autopilot_cycle: plan % not found for tenant', p_plan_id USING errcode = 'P0002';\n  END IF;\n\n  -- Budget cap (per cycle) \u2014 FR-VA-007 (no deduct).\n  IF p_projected_mco > v_budget_cap THEN\n    RETURN jsonb_build_object('ok', false, 'reason', 'aborted_budget',\n                              'projected', p_projected_mco, 'budget_cap', v_budget_cap);\n  END IF;\n\n  -- Balance + min-balance floor \u2014 FR-VA-007 (no deduct).\n  SELECT mco_balance INTO v_balance FROM public.profiles WHERE id = p_user_id;\n  IF v_balance IS NULL THEN\n    RAISE EXCEPTION 'begin_autopilot_cycle: profile not found for tenant' USING errcode = 'P0002';\n  END IF;\n  IF v_balance < p_projected_mco OR v_balance < v_min_balance THEN\n    RETURN jsonb_build_object('ok', false, 'reason', 'insufficient_balance',\n                              'projected', p_projected_mco, 'balance', v_balance, 'min_balance', v_min_balance);\n  END IF;\n\n  -- Daily cap (per tenant, UTC day) \u2014 FR-VA-021. Sum COMMITTED spend of today's non-aborted cycles.\n  SELECT COALESCE(SUM(spend_mco), 0) INTO v_daily_spent\n    FROM public.autopilot_cycles\n   WHERE user_id = p_user_id\n     AND (started_at AT TIME ZONE 'UTC')::date = (now() AT TIME ZONE 'UTC')::date\n     AND status NOT IN ('aborted_budget','aborted_daily_cap');\n  IF v_daily_spent + p_projected_mco > v_daily_cap THEN\n    RETURN jsonb_build_object('ok', false, 'reason', 'aborted_daily_cap',\n                              'projected', p_projected_mco, 'daily_spent', v_daily_spent, 'daily_cap', v_daily_cap);\n  END IF;\n\n  -- All caps passed \u2192 open the cycle and pre-debit atomically (advisory lock still held \u2192 serialized).\n  SELECT COALESCE(MAX(cycle_number), 0) + 1 INTO v_cycle_number\n    FROM public.autopilot_cycles WHERE plan_id = p_plan_id;\n\n  INSERT INTO public.autopilot_cycles (user_id, plan_id, cycle_number, status, spend_mco, planned_units, debited_at)\n  VALUES (p_user_id, p_plan_id, v_cycle_number, 'running', p_projected_mco, GREATEST(p_planned_units, 0), now())\n  RETURNING id INTO v_cycle_id;\n\n  -- SINGLE pre-debit. service-role caller \u2192 deduct's service_role exemption applies. If a concurrent non-autopilot\n  -- spend dropped the balance below projected, deduct RAISEs (mco_balance >= amount under FOR UPDATE) and the whole\n  -- transaction rolls back (the INSERT is undone) \u2014 atomic, no orphan debited cycle.\n  PERFORM public.deduct_mco_coins(p_user_id, p_projected_mco::numeric, 'autopilot_cycle',\n            jsonb_build_object('plan_id', p_plan_id, 'cycle_id', v_cycle_id, 'cycle_number', v_cycle_number));\n\n  RETURN jsonb_build_object('ok', true, 'cycle_id', v_cycle_id, 'cycle_number', v_cycle_number,\n                            'projected', p_projected_mco);\nEND;\n$$;\n\n-- Service-role-only: only the autopilot runner (which proved service-role in-function) may open a paid cycle.\nREVOKE ALL ON FUNCTION public.begin_autopilot_cycle(uuid, uuid, int, int) FROM PUBLIC, anon, authenticated;\nGRANT EXECUTE ON FUNCTION public.begin_autopilot_cycle(uuid, uuid, int, int) TO service_role;\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120200_begin_autopilot_cycle.sql (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(17:51:47)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120300_finalize_autopilot_cycle.sql",
  "content": "-- Migration: finalize_autopilot_cycle RPC \u2014 terminal close + idempotent POSITIVE-credit refund (FR-VA-007).\n-- BoK SSOT: docs/bok/viral-autopilot/05-sdd.md \u00a72 (RPC table line 110, \"espelha finalize_vision_job\").\n-- SOP (Lei 2): docs/processes/[[autopilot-cron-identity|autopilot-cron-identity]].md.\n--\n-- Mirrors public.finalize_vision_job (20260615160000): claim a RUNNING cycle EXACTLY ONCE, then credit the unused\n-- (spend_mco \u2212 actual) via add_mco_coins (POSITIVE \u2014 never a negative deduct) in the SAME transaction, plus a\n-- symmetric +amount ledger row in mcoin_transactions (the spend row was -projected). Idempotent: a second call\n-- finds no running cycle (guard status='running') \u2192 no-op, no double refund.\n--\n-- Identity: service-role-only (REVOKE authenticated/anon) \u2014 the runner / reconcile-sweep (both service-role) finalize.\n--\n-- Engineering note (declared per Lei 1): the sealed stub hints (uuid,int); a 3rd p_status (DEFAULT 'completed',\n-- CHECK in {completed,failed}) is added \u2014 backward-compatible with a 2-arg call \u2014 so a fully-failed cycle closes\n-- as 'failed' (with full refund when actual=0) instead of masquerading as 'completed'. Mirrors finalize_vision_job's\n-- terminal-state parameter. The refund math is identical regardless of terminal status.\n\nCREATE OR REPLACE FUNCTION public.finalize_autopilot_cycle(\n  p_cycle_id   uuid,\n  p_actual_mco int,\n  p_status     text DEFAULT 'completed'\n)\nRETURNS jsonb\nLANGUAGE plpgsql\nSECURITY DEFINER\nSET search_path = ''\nAS $$\nDECLARE\n  v_uid    uuid;\n  v_spend  int;\n  v_refund int;\nBEGIN\n  IF p_actual_mco IS NULL OR p_actual_mco < 0 THEN\n    RAISE EXCEPTION 'finalize_autopilot_cycle: actual must be >= 0, got %', p_actual_mco USING errcode = '22023';\n  END IF;\n  IF p_status NOT IN ('completed','failed') THEN\n    RAISE EXCEPTION 'finalize_autopilot_cycle: terminal status must be completed|failed, got %', p_status\n      USING errcode = '22023';\n  END IF;\n\n  -- Claim + close a RUNNING cycle exactly once. refund = unused, clamped >= 0 (actual may overshoot spend \u2192 0).\n  UPDATE public.autopilot_cycles\n     SET status       = p_status,\n         completed_at = now(),\n         refunded_mco = GREATEST(0, spend_mco - p_actual_mco),\n         refunded_at  = now()\n   WHERE id = p_cycle_id\n     AND status = 'running'\n   RETURNING user_id, spend_mco INTO v_uid, v_spend;\n\n  IF v_uid IS NULL THEN\n    RETURN jsonb_build_object('finalized', false);   -- already terminal \u2192 no-op (no double refund)\n  END IF;\n\n  v_refund := GREATEST(0, v_spend - p_actual_mco);\n\n  IF v_refund > 0 THEN\n    -- Positive credit (add_mco_coins rejects <=0) + symmetric ledger row (spend was the -projected row).\n    PERFORM public.add_mco_coins(v_uid, v_refund);\n    INSERT INTO public.mcoin_transactions (user_id, action, amount, context)\n    VALUES (v_uid, 'autopilot_refund', v_refund,\n            jsonb_build_object('cycle_id', p_cycle_id, 'actual', p_actual_mco, 'status', p_status));\n    RETURN jsonb_build_object('finalized', true, 'status', p_status, 'refunded', v_refund);\n  END IF;\n\n  RETURN jsonb_build_object('finalized', true, 'status', p_status, 'refunded', 0);\nEND;\n$$;\n\nREVOKE ALL ON FUNCTION public.finalize_autopilot_cycle(uuid, int, text) FROM PUBLIC, anon, authenticated;\nGRANT EXECUTE ON FUNCTION public.finalize_autopilot_cycle(uuid, int, text) TO service_role;\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120300_finalize_autopilot_cycle.sql (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(17:51:59)*


## 🤖 Claude *(17:52:01)*

4 migrations escritas. Agora o gate obrigatório (CLAUDE.md + SOP G9): **`/security-review` antes de qualquer commit**. Stage dos arquivos novos pra entrarem no diff revisado.

## 🤖 Claude *(17:52:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add supabase/migrations/20260620120000_viral_autopilot_plans.sql \\\n        supabase/migrations/20260620120100_viral_autopilot_cycles.sql \\\n        supabase/migrations/20260620120200_begin_autopilot_cycle.sql \\\n        supabase/migrations/20260620120300_finalize_autopilot_cycle.sql \\\n        docs/processes/[[autopilot-cron-identity|autopilot-cron-identity]].md\ngit status --short",
  "description": "Stage new migrations + SOP for review"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> A  docs/processes/[[autopilot-cron-identity|autopilot-cron-identity]].md
> A  supabase/migrations/20260620120000_viral_autopilot_plans.sql
> A  supabase/migrations/20260620120100_viral_autopilot_cycles.sql
> A  supabase/migrations/20260620120200_begin_autopilot_cycle.sql
> A  supabase/migrations/20260620120300_finalize_autopilot_cycle.sql
> ```

## 🤖 Claude *(17:52:06)*


## 🤖 Claude *(17:52:06)*

Staged. Rodando o `/security-review` independente sobre as 4 migrations (o Reviewer mecânico — Lei 1).

## 🤖 Claude *(17:52:07)*


🛠️ **Tool Call**: `Skill`
```json
{
  "skill": "security-review"
}
```

> **Tool Result (Skill)** - ✅ Success
>
> ```
> Launching skill: security-review
> ```

## 👤 User *(17:52:07)*

You are a senior security engineer conducting a focused security review of the changes on this branch.

GIT STATUS:

```
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	new file:   docs/processes/[[autopilot-cron-identity|autopilot-cron-identity]].md
	new file:   supabase/migrations/20260620120000_viral_autopilot_plans.sql
	new file:   supabase/migrations/20260620120100_viral_autopilot_cycles.sql
	new file:   supabase/migrations/20260620120200_begin_autopilot_cycle.sql
	new file:   supabase/migrations/20260620120300_finalize_autopilot_cycle.sql
```

FILES MODIFIED:

```
(Bash completed with no output)
```

COMMITS:

```
(Bash completed with no output)
```

DIFF CONTENT:

```
(Bash completed with no output)
```

Review the complete diff above. This contains all code changes in the PR.


OBJECTIVE:
Perform a security-focused code review to identify HIGH-CONFIDENCE security vulnerabilities that could have real exploitation potential. This is not a general code review - focus ONLY on security implications newly added by this PR. Do not comment on existing security concerns.

CRITICAL INSTRUCTIONS:
1. MINIMIZE FALSE POSITIVES: Only flag issues where you're >80% confident of actual exploitability
2. AVOID NOISE: Skip theoretical issues, style concerns, or low-impact findings
3. FOCUS ON IMPACT: Prioritize vulnerabilities that could lead to unauthorized access, data breaches, or system compromise
4. EXCLUSIONS: Do NOT report the following issue types:
   - Denial of Service (DOS) vulnerabilities, even if they allow service disruption
   - Secrets or sensitive data stored on disk (these are handled by other processes)
   - Rate limiting or resource exhaustion issues

SECURITY CATEGORIES TO EXAMINE:

**Input Validation Vulnerabilities:**
- SQL injection via unsanitized user input
- Command injection in system calls or subprocesses
- XXE injection in XML parsing
- Template injection in templating engines
- NoSQL injection in database queries
- Path traversal in file operations

**Authentication & Authorization Issues:**
- Authentication bypass logic
- Privilege escalation paths
- Session management flaws
- JWT token vulnerabilities
- Authorization logic bypasses

**Crypto & Secrets Management:**
- Hardcoded API keys, passwords, or tokens
- Weak cryptographic algorithms or implementations
- Improper key storage or management
- Cryptographic randomness issues
- Certificate validation bypasses

**Injection & Code Execution:**
- Remote code execution via deseralization
- Pickle injection in Python
- YAML deserialization vulnerabilities
- Eval injection in dynamic code execution
- XSS vulnerabilities in web applications (reflected, stored, DOM-based)

**Data Exposure:**
- Sensitive data logging or storage
- PII handling violations
- API endpoint data leakage
- Debug information exposure

Additional notes:
- Even if something is only exploitable from the local network, it can still be a HIGH severity issue

ANALYSIS METHODOLOGY:

Phase 1 - Repository Context Research (Use file search tools):
- Identify existing security frameworks and libraries in use
- Look for established secure coding patterns in the codebase
- Examine existing sanitization and validation patterns
- Understand the project's security model and threat model

Phase 2 - Comparative Analysis:
- Compare new code changes against existing security patterns
- Identify deviations from established secure practices
- Look for inconsistent security implementations
- Flag code that introduces new attack surfaces

Phase 3 - Vulnerability Assessment:
- Examine each modified file for security implications
- Trace data flow from user inputs to sensitive operations
- Look for privilege boundaries being crossed unsafely
- Identify injection points and unsafe deserialization

REQUIRED OUTPUT FORMAT:

You MUST output your findings in markdown. The markdown output should contain the file, line number, severity, category (e.g. `sql_injection` or `xss`), description, exploit scenario, and fix recommendation.

For example:

# Vuln 1: XSS: `foo.py:42`

* Severity: High
* Description: User input from `username` parameter is directly interpolated into HTML without escaping, allowing reflected XSS attacks
* Exploit Scenario: Attacker crafts URL like /bar?q=<script>alert(document.cookie)</script> to execute JavaScript in victim's browser, enabling session hijacking or data theft
* Recommendation: Use Flask's escape() function or Jinja2 templates with auto-escaping enabled for all user inputs rendered in HTML

SEVERITY GUIDELINES:
- **HIGH**: Directly exploitable vulnerabilities leading to RCE, data breach, or authentication bypass
- **MEDIUM**: Vulnerabilities requiring specific conditions but with significant impact
- **LOW**: Defense-in-depth issues or lower-impact vulnerabilities

CONFIDENCE SCORING:
- 0.9-1.0: Certain exploit path identified, tested if possible
- 0.8-0.9: Clear vulnerability pattern with known exploitation methods
- 0.7-0.8: Suspicious pattern requiring specific conditions to exploit
- Below 0.7: Don't report (too speculative)

FINAL REMINDER:
Focus on HIGH and MEDIUM findings only. Better to miss some theoretical issues than flood the report with false positives. Each finding should be something a security engineer would confidently raise in a PR review.

FALSE POSITIVE FILTERING:

> You do not need to run commands to reproduce the vulnerability, just read the code to determine if it is a real vulnerability. Do not use the bash tool or write to any files.
>
> HARD EXCLUSIONS - Automatically exclude findings matching these patterns:
> 1. Denial of Service (DOS) vulnerabilities or resource exhaustion attacks.
> 2. Secrets or credentials stored on disk if they are otherwise secured.
> 3. Rate limiting concerns or service overload scenarios.
> 4. Memory consumption or CPU exhaustion issues.
> 5. Lack of input validation on non-security-critical fields without proven security impact.
> 6. Input sanitization concerns for GitHub Action workflows unless they are clearly triggerable via untrusted input.
> 7. A lack of hardening measures. Code is not expected to implement all security best practices, only flag concrete vulnerabilities.
> 8. Race conditions or timing attacks that are theoretical rather than practical issues. Only report a race condition if it is concretely problematic.
> 9. Vulnerabilities related to outdated third-party libraries. These are managed separately and should not be reported here.
> 10. Memory safety issues such as buffer overflows or use-after-free-vulnerabilities are impossible in rust. Do not report memory safety issues in rust or any other memory safe languages.
> 11. Files that are only unit tests or only used as part of running tests.
> 12. Log spoofing concerns. Outputting un-sanitized user input to logs is not a vulnerability.
> 13. SSRF vulnerabilities that only control the path. SSRF is only a concern if it can control the host or protocol.
> 14. Including user-controlled content in AI system prompts is not a vulnerability.
> 15. Regex injection. Injecting untrusted content into a regex is not a vulnerability.
> 16. Regex DOS concerns.
> 16. Insecure documentation. Do not report any findings in documentation files such as markdown files.
> 17. A lack of audit logs is not a vulnerability.
>
> PRECEDENTS -
> 1. Logging high value secrets in plaintext is a vulnerability. Logging URLs is assumed to be safe.
> 2. UUIDs can be assumed to be unguessable and do not need to be validated.
> 3. Environment variables and CLI flags are trusted values. Attackers are generally not able to modify them in a secure environment. Any attack that relies on controlling an environment variable is invalid.
> 4. Resource management issues such as memory or file descriptor leaks are not valid.
> 5. Subtle or low impact web vulnerabilities such as tabnabbing, XS-Leaks, prototype pollution, and open redirects should not be reported unless they are extremely high confidence.
> 6. React and Angular are generally secure against XSS. These frameworks do not need to sanitize or escape user input unless it is using dangerouslySetInnerHTML, bypassSecurityTrustHtml, or similar methods. Do not report XSS vulnerabilities in React or Angular components or tsx files unless they are using unsafe methods.
> 7. Most vulnerabilities in github action workflows are not exploitable in practice. Before validating a github action workflow vulnerability ensure it is concrete and has a very specific attack path.
> 8. A lack of permission checking or authentication in client-side JS/TS code is not a vulnerability. Client-side code is not trusted and does not need to implement these checks, they are handled on the server-side. The same applies to all flows that send untrusted data to the backend, the backend is responsible for validating and sanitizing all inputs.
> 9. Only include MEDIUM findings if they are obvious and concrete issues.
> 10. Most vulnerabilities in ipython notebooks (*.ipynb files) are not exploitable in practice. Before validating a notebook vulnerability ensure it is concrete and has a very specific attack path where untrusted input can trigger the vulnerability.
> 11. Logging non-PII data is not a vulnerability even if the data may be sensitive. Only report logging vulnerabilities if they expose sensitive information such as secrets, passwords, or personally identifiable information (PII).
> 12. Command injection vulnerabilities in shell scripts are generally not exploitable in practice since shell scripts generally do not run with untrusted user input. Only report command injection vulnerabilities in shell scripts if they are concrete and have a very specific attack path for untrusted input.
>
> SIGNAL QUALITY CRITERIA - For remaining findings, assess:
> 1. Is there a concrete, exploitable vulnerability with a clear attack path?
> 2. Does this represent a real security risk vs theoretical best practice?
> 3. Are there specific code locations and reproduction steps?
> 4. Would this finding be actionable for a security team?
>
> For each finding, assign a confidence score from 1-10:
> - 1-3: Low confidence, likely false positive or noise
> - 4-6: Medium confidence, needs investigation
> - 7-10: High confidence, likely true vulnerability

START ANALYSIS:

Begin your analysis now. Do this in 3 steps:

1. Use a sub-task to identify vulnerabilities. Use the repository exploration tools to understand the codebase context, then analyze the PR changes for security implications. In the prompt for this sub-task, include all of the above.
2. Then for each vulnerability identified by the above sub-task, create a new sub-task to filter out false-positives. Launch these sub-tasks as parallel sub-tasks. In the prompt for these sub-tasks, include everything in the "FALSE POSITIVE FILTERING" instructions.
3. Filter out any vulnerabilities where the sub-task reported a confidence less than 8.

Your final reply must contain the markdown report and nothing else.

## 🤖 Claude *(17:52:13)*


## 🤖 Claude *(17:52:39)*


🛠️ **Tool Call**: `Agent`
```json
{
  "description": "Security review of autopilot migrations",
  "subagent_type": "general-purpose",
  "prompt": "You are a senior security engineer conducting a focused security review of NEW database migration files on this branch. The automated diff capture returned empty, so READ THE FILES DIRECTLY from disk.\n\nFILES TO REVIEW (read all four):\n- /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120000_viral_autopilot_plans.sql\n- /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120100_viral_autopilot_cycles.sql\n- /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120200_begin_autopilot_cycle.sql\n- /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120300_finalize_autopilot_cycle.sql\n\n(Ignore docs/processes/[[autopilot-cron-identity|autopilot-cron-identity]].md \u2014 it is a markdown doc, excluded from findings.)\n\nCONTEXT \u2014 this is a Supabase/Postgres multi-tenant app (RLS on every table, user_id = auth.uid() isolation). These migrations add the Viral Autopilot cadence layer: two tables (autopilot_plans, autopilot_cycles) and two SECURITY DEFINER RPCs (begin_autopilot_cycle = atomic cap-check + pre-debit of mcoCoins; finalize_autopilot_cycle = idempotent positive-credit refund). The mcoCoins ledger is money. Existing security model to compare against:\n- Existing ledger RPCs in supabase/migrations/20260603220000_secure_ledger_rpcs.sql (deduct_mco_coins: guards p_amount>0 + own-tenant; award/add_user_score service-role-only).\n- add_mco_coins(uuid,integer) is service-role-only (20260520150000); it bumps profiles.mco_balance, positive-only.\n- The mirror pattern finalize_vision_job in supabase/migrations/20260615160000_vision_mcp_jobs.sql (claim-once terminal + refund).\n- SECURITY DEFINER hardening (search_path) in 20260603210500_harden_definer_search_path.sql.\nRead those existing files to understand the established secure patterns before judging the new code.\n\nOBJECTIVE: Identify HIGH-CONFIDENCE security vulnerabilities NEWLY INTRODUCED by these 4 files, with real exploitation potential. This is security-only, not general review.\n\nFocus especially on these threat classes relevant to money-moving DB code:\n- Privilege/authorization: can a non-service-role (anon/authenticated) caller invoke begin_autopilot_cycle / finalize_autopilot_cycle (mint or drain mcoCoins)? Check the REVOKE/GRANT lines.\n- Cross-tenant: can a caller cause a debit/credit/refund against ANOTHER tenant's balance or read/write another tenant's plan/cycle? Check the tenant-scoping in the RPC bodies and the composite FK / RLS policies.\n- Mint/drain via the RPCs: negative-amount tricks, refund > spend (double-spend / mint), refund replay (idempotency), TOCTOU on the daily cap.\n- SQL injection (dynamic SQL) \u2014 there is none expected (no EXECUTE), confirm.\n- RLS gaps: default-deny correctness, RESTRICTIVE no-delete, missing policies that expose data, search_path on SECURITY DEFINER.\n- The composite FK ALTER on creative_metrics \u2014 any integrity bypass.\n\nRULES:\n1. MINIMIZE FALSE POSITIVES: only flag issues where you are >80% confident of real exploitability.\n2. Skip theoretical/style/defense-in-depth-only issues, DOS, rate-limiting, resource exhaustion.\n3. Do NOT report anything in markdown/documentation files.\n4. Remember: SECURITY DEFINER functions run with the function owner's privileges and BYPASS RLS \u2014 so the in-body tenant checks are the ONLY guard. Judge them carefully. But also remember auth.role()/auth.uid() inside a SECURITY DEFINER reflect the ORIGINAL caller (GUC-based), they are not elevated.\n5. service_role is trusted (it is the backend). A finding that \"service_role can do X\" is NOT a vulnerability \u2014 service_role is the backend and is allowed to move money. The question is whether anon/authenticated (untrusted clients) can.\n\nMETHODOLOGY: (1) read the 4 new files + the existing pattern files; (2) trace data flow from an untrusted client (anon/authenticated via PostgREST) to any money movement or cross-tenant read/write; (3) for each candidate, determine the concrete attack path.\n\nOUTPUT: A markdown report. For each finding: title with file:line, Severity (HIGH/MEDIUM), Category, Description, concrete Exploit Scenario (who calls what with what to achieve what), Fix Recommendation, and a Confidence score 1-10. If you find NO high-confidence vulnerabilities, say so explicitly and explain why the design is sound (cite the specific REVOKE/GRANT and tenant-scoping lines). Be precise with line numbers."
}
```

> **Tool Result (Agent)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'No blanket `GRANT EXECUTE ON ALL FUNCTIONS`, no `ALTER DEFAULT PRIVILEGES`, and no other migration re-grants the two RPCs. The REVOKE/GRANT lines stand as the only authorization on the money-moving functions.\n\nOne last verification: confirm that `update_updated_at_column` (the trigger function used) exists and that the `creative_metrics` table has the `UNIQUE(content_variant_id, source)` but the composite FK in `...120100` targets `autopilot_cycles(id, user_id)` which IS anchored by `CONSTRAINT autopilot_cycles_id_user_uniq UNIQUE (id, user_id)` (line 33 of `...120100`) — that\'s present. And the `creative_metrics` side has `cycle_id` + `user_id` columns (both exist, lines 25-26). Let me also sanity-check whether a tenant could exploit the `creative_metrics` composite FK to *read* cross-tenant — but FK is integrity-only, not a read vector, and `creative_metrics` writes are default-deny for authenticated. \n\nLet me do a final focused check on one TOCTOU subtlety: the daily-cap sum in `begin_autopilot_cycle` filters `status NOT IN (\'aborted_budget\',\'aborted_daily_cap\')` — but aborts are never inserted as rows (per the header comment, line 20-21 of `...120200`). So the only rows summed are real `running`/`completed`/`failed` cycles. A `failed` cycle that was refunded still counts its full `spend_mco` toward the daily cap, which is conservative (in the tenant\'s favor for safety, not exploitable). This is correct.\n\nI have everything needed. Let me also confirm there\'s no issue with the advisory-lock-after-validation ordering — the lock is taken at line 49 BEFORE the plan load and all cap checks (lines 52-99), so the entire read-check-debit sequence is serialized per tenant. Correct.\n\nThe design is sound. Here is my report.\n\n---\n\n# Security Review — Viral Autopilot Cadence Migrations (4 files)\n\n**Verdict: NO high-confidence security vulnerabilities found.** All four migrations correctly follow the established secure patterns (`secure_ledger_rpcs`, `finalize_vision_job`, `harden_definer_search_path`). The money-moving RPCs are service-role-only, every table is tenant-scoped with default-deny writes, and the refund/cap logic is mint-safe and idempotent. Detailed justification below, with the specific load-bearing lines.\n\n---\n\n## Threat-class-by-threat-class analysis\n\n### 1. Privilege / authorization on the money-moving RPCs — SOUND\n\nBoth RPCs are SECURITY DEFINER (bypass RLS), so their EXECUTE grants are the entire perimeter against untrusted clients. Both are correctly locked:\n\n- **`begin_autopilot_cycle`** (`20260620120200_begin_autopilot_cycle.sql:107-108`):\n  ```\n  REVOKE ALL ON FUNCTION public.begin_autopilot_cycle(uuid, uuid, int, int) FROM PUBLIC, anon, authenticated;\n  GRANT EXECUTE ON FUNCTION public.begin_autopilot_cycle(uuid, uuid, int, int) TO service_role;\n  ```\n- **`finalize_autopilot_cycle`** (`20260620120300_finalize_autopilot_cycle.sql:69-70`): identical pattern, `(uuid, int, text)` signature.\n\nAn authenticated/anon PostgREST client cannot invoke either. The signature in the REVOKE/GRANT matches the `CREATE OR REPLACE` signature exactly (including the new defaulted args `p_planned_units` / `p_status`), so the grant lands on the right overload — no accidentally-ungated variant. I confirmed there is no blanket `GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public`, no `ALTER DEFAULT PRIVILEGES`, and no later migration re-granting these two functions — the REVOKE/GRANT pair is the only authority. This is the exact lockdown the team applied to `award_mco_coins` / `add_user_score` / `finalize_vision_job`.\n\n### 2. Cross-tenant debit / credit / read — SOUND\n\n- **`begin_autopilot_cycle` plan load is tenant-scoped** (`...120200:52-58`): `WHERE id = p_plan_id AND user_id = p_user_id` + `IF NOT FOUND THEN RAISE`. A cross-tenant `p_plan_id` cannot leak another tenant\'s caps; it aborts. Because the function is service-role-only and the caller (autopilot-run) resolves `p_user_id` from the server-trusted plan row (not the request body, per header lines 15-16), there is no untrusted path to forge a mismatched `(p_plan_id, p_user_id)` pair anyway.\n- **Balance read, daily-cap sum, cycle INSERT, and the `deduct_mco_coins` call all key on the same `p_user_id`** (`...120200:67, 79, 91-92, 98`). No path debits or reads a different tenant.\n- **`finalize_autopilot_cycle`** derives `v_uid` from the claimed row (`...120300:48`) and credits that same `v_uid` (`:58`). It takes no `p_user_id`, so there is no caller-supplied tenant to spoof; and since it\'s service-role-only, a tenant can\'t reach it to finalize someone else\'s cycle.\n- **Tenant-scoped composite FKs** enforce integrity at the schema layer: `autopilot_cycles(plan_id, user_id) → autopilot_plans(id, user_id)` (`...120100:35-36`) and `creative_metrics(cycle_id, user_id) → autopilot_cycles(id, user_id)` (`...120100:65-67`), each anchored by the matching `UNIQUE(id, user_id)` (`...120000:40`, `...120100:33`). A cycle can never point at another tenant\'s plan. FKs are integrity-only (not a read vector), and reads on all three tables are gated by `FOR SELECT USING (auth.uid() = user_id)`.\n\n### 3. Mint / drain via the RPCs — SOUND\n\n- **Negative-amount mint is blocked at three layers.** `begin_autopilot_cycle` rejects `p_projected_mco <= 0` (`...120200:43-46`); `finalize_autopilot_cycle` rejects `p_actual_mco < 0` (`...120300:32-34`); and both ultimately route money through `deduct_mco_coins` (positive-only, `secure_ledger_rpcs.sql:45`) and `add_mco_coins` (positive-only, `...:58` "Amount must be positive"). There is no negative-deduct path.\n- **Refund cannot exceed spend (no refund-mint / double-spend).** Refund is `GREATEST(0, spend_mco - p_actual_mco)` (`...120300:44, 54`), additionally enforced by table CHECK `refunded_mco <= spend_mco` (`...120100:31`). If `p_actual_mco` overshoots `spend_mco`, refund clamps to 0. The credited `v_refund` can never exceed what `begin` pre-debited.\n- **Refund replay / idempotency.** The claim is `UPDATE ... WHERE id = p_cycle_id AND status = \'running\' RETURNING user_id` (`...120300:46-48`). A second call finds no `running` row → `v_uid IS NULL` → `RETURN {finalized:false}` no-op (`:50-51`), exactly mirroring `finalize_vision_job`\'s claim-once guard. The status transition out of `\'running\'` and the `add_mco_coins` credit commit in one transaction, so there is no money-without-guard window.\n- **TOCTOU on the daily cap.** `pg_advisory_xact_lock(hashtext(p_user_id::text))` is taken at `...120200:49` — *before* the plan load, balance read, daily-cap sum, cycle INSERT, and pre-debit (lines 52-99). Concurrent `begin` calls for the same tenant serialize, so two parallel cycles cannot both slip under the daily cap. The pre-debit additionally re-checks `mco_balance >= amount` under `FOR UPDATE` inside `deduct_mco_coins`, and a failure rolls back the cycle INSERT in the same transaction (no orphan debited cycle).\n\n### 4. SQL injection — NONE (confirmed)\n\nNo dynamic SQL. There is no `EXECUTE`/`format()`/string-concatenation anywhere in the four files. All values flow as bound plpgsql variables. The jsonb context built in `begin`/`finalize` (`...120200:99`, `...120300:60-61`) uses `jsonb_build_object` with parameterized values.\n\n### 5. RLS / search_path hardening — SOUND\n\n- Both tables `ENABLE ROW LEVEL SECURITY` (`...120000:43`, `...120100:39`).\n- `autopilot_plans`: SELECT/INSERT/UPDATE all gated `auth.uid() = user_id` (`...120000:45-50`), plus `RESTRICTIVE FOR DELETE USING (false)` (`:53-54`) — clients can never delete, even if a future permissive policy is added.\n- `autopilot_cycles`: SELECT-own only; **no INSERT/UPDATE policy → authenticated default-deny** (only the service-role RPCs, which bypass RLS, write); `RESTRICTIVE FOR DELETE USING (false)` (`...120100:42-45`). This is the correct posture for a financial ledger a tenant must never forge or mutate.\n- Both SECURITY DEFINER functions set `SET search_path = \'\'` (`...120200:32`, `...120300:25`) and fully schema-qualify every object (`public.autopilot_plans`, `public.profiles`, `public.deduct_mco_coins`, `public.add_mco_coins`, `public.mcoin_transactions`, `pg_advisory_xact_lock` is a built-in resolved via empty path) — closing the CWE-426 search-path-injection surface the `harden_definer_search_path` migration targeted.\n\n### 6. The composite FK ALTER on `creative_metrics` — no integrity bypass\n\n`...120100:60-69` adds `creative_metrics_cycle_fk (cycle_id, user_id) → autopilot_cycles(id, user_id) ON DELETE CASCADE`, wrapped in an idempotent `IF NOT EXISTS (... pg_constraint WHERE conname=...)` guard. With default `MATCH SIMPLE`, the Fatia-1 baseline rows that have `cycle_id IS NULL` remain valid (FK skipped when any referencing column is NULL) — that is the documented, intended behavior, not a bypass: those rows still carry a `NOT NULL user_id` with its own RLS, and a non-NULL `cycle_id` is forced to match a same-tenant cycle. No way for a tenant to point a metric at another tenant\'s cycle.\n\n---\n\n## Minor, non-exploitable observations (explicitly NOT findings)\n\nThese do not meet the >80%-exploitability bar and are noted only for completeness:\n\n- **`finalize_autopilot_cycle` takes no `p_user_id` and trusts the row\'s `user_id`.** This is *correct* given the service-role-only contract (the trusted backend supplies the cycle_id). It is the same shape as `finalize_vision_job`. Not a vuln.\n- **Daily-cap sum counts `failed`/`completed` cycles\' full `spend_mco` even after a refund** (`...120200:77-81` excludes only the two `aborted_*` statuses, which are never persisted as rows). This is conservative — it can only make the cap *stricter* (tenant-favorable for safety), never permit overspend. Not a security issue.\n- `add_mco_coins` and `deduct_mco_coins` (the credit/debit primitives invoked here) were already hardened in prior migrations (`secure_ledger_rpcs.sql`, `admin_user_lifecycle.sql:17-18`); these new files consume them correctly under the service-role exemption.\n\n---\n\n**Files reviewed (all absolute):**\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120000_viral_autopilot_plans.sql`\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120100_viral_autopilot_cycles.sql`\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120200_begin_autopilot_cycle.sql`\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260620120300_finalize_autopilot_cycle.sql`\n\n**Pattern files cross-referenced:** `20260603220000_secure_ledger_rpcs.sql`, `20260615160000_vision_mcp_jobs.sql`, `20260603210500_harden_definer_search_path.sql`, `20260520150000_admin_user_lifecycle.sql` (+`20260505100000` for `add_mco_coins`), `20260619140000_viral_autopilot_creative_metrics.sql`.\n\nThe migrations are safe to commit from a security standpoint.'}, {'type': 'text', 'text': "agentId: a33229f768cfc869d (use SendMessage with to: 'a33229f768cfc869d' to continue this agent)\n<usage>subagent_tokens: 90599\ntool_uses: 14\nduration_ms: 99518</usage>"}]
> ```

## 🤖 Claude *(17:55:22)*


## 🤖 Claude *(17:55:30)*

## ✅ `/security-review` — SAFE (zero findings ≥ High)

O Reviewer mecânico independente traçou cada classe de ameaça contra os padrões estabelecidos e confirmou o design sólido:

| Classe | Veredito | Linha-prova |
|---|---|---|
| **Autorização** | RPCs service-role-only; anon/authenticated não alcançam | `begin:107-108` · `finalize:69-70` REVOKE/GRANT |
| **Cross-tenant** | `begin` escopado `WHERE id AND user_id`; `finalize` deriva uid da linha | `begin:52-58` · FK composta `cycles:35-36` |
| **Mint/drain** | positivo-only 3 camadas; refund ≤ spend (`GREATEST`+CHECK); claim-once idempotente | `finalize:44,54` + CHECK `cycles:31` |
| **SQL injection** | nenhum SQL dinâmico (sem EXECUTE/format) | — |
| **RLS/search_path** | default-deny + RESTRICTIVE no-delete + `search_path=''` qualificado | `cycles:42-45` · `begin:32` |
| **TOCTOU cap diário** | `pg_advisory_xact_lock` antes de todo check+débito | `begin:49` |

Migrations seguras pra aplicar. **Gate G9 verde.** Aplicando em produção — additivo e inerte (nenhum centavo se move até as edge functions do cron existirem, que é fatia separada). Confirmo conectividade + o que está pendente antes do push.

## 🤖 Claude *(17:55:33)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== supabase CLI version ===\"; npx supabase --version 2>&1 | head -3\necho \"=== migration list (local vs remote \u2014 confirms pending = my 4) ===\"; npx supabase migration list 2>&1 | tail -15\necho \"=== env key NAMES present (no values) for apply/verify auth ===\"; grep -oE '^(SUPABASE_[A-Z_]*|SB_[A-Z_]*|VITE_SUPABASE_PROJECT_ID)=' .env 2>/dev/null | sed 's/=$//' | sort -u",
  "description": "Check CLI, pending migrations, available auth keys"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === supabase CLI version ===
> 2.92.1
> A new version of Supabase CLI is available: v2.107.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> === migration list (local vs remote — confirms pending = my 4) ===
>    20260612022953 | 20260612022953 | 2026-06-12 02:29:53 
>    20260615140000 | 20260615140000 | 2026-06-15 14:00:00 
>    20260615160000 | 20260615160000 | 2026-06-15 16:00:00 
>    20260615170000 | 20260615170000 | 2026-06-15 17:00:00 
>    20260615180000 | 20260615180000 | 2026-06-15 18:00:00 
>    20260615190000 | 20260615190000 | 2026-06-15 19:00:00 
>    20260615200000 | 20260615200000 | 2026-06-15 20:00:00 
>    20260619140000 | 20260619140000 | 2026-06-19 14:00:00 
>    20260620120000 |                | 2026-06-20 12:00:00 
>    20260620120100 |                | 2026-06-20 12:01:00 
>    20260620120200 |                | 2026-06-20 12:02:00 
>    20260620120300 |                | 2026-06-20 12:03:00 
> 
> A new version of Supabase CLI is available: v2.107.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> === env key NAMES present (no values) for apply/verify auth ===
> SB_SECRET_KEY
> SUPABASE_PUBLISHABLE_KEY
> SUPABASE_SECRET_KEY
> SUPABASE_SERVICE_ROLE_KEY
> SUPABASE_URL
> VITE_SUPABASE_PROJECT_ID
> ```

## 🤖 Claude *(17:55:46)*


## 🤖 Claude *(17:55:47)*

Confirmado: exatamente minhas 4 migrations pendentes (todas as anteriores sincronizadas até `20260619140000`), CLI linkado (lê o histórico remoto). Aplicando com auto-confirm.

## 🤖 Claude *(17:55:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nprintf 'y\\n' | npx supabase db push 2>&1 | tail -40\necho \"EXIT=${PIPESTATUS[1]}\"",
  "description": "Apply the 4 pending migrations to remote",
  "timeout": 180000
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Initialising login role...
> Connecting to remote database...
> Do you want to push these migrations to the remote database?
>  • 20260620120000_viral_autopilot_plans.sql
>  • 20260620120100_viral_autopilot_cycles.sql
>  • 20260620120200_begin_autopilot_cycle.sql
>  • 20260620120300_finalize_autopilot_cycle.sql
> 
>  [Y/n] y
> Applying migration 20260620120000_viral_autopilot_plans.sql...
> Applying migration 20260620120100_viral_autopilot_cycles.sql...
> Applying migration 20260620120200_begin_autopilot_cycle.sql...
> Applying migration 20260620120300_finalize_autopilot_cycle.sql...
> Finished supabase db push.
> A new version of Supabase CLI is available: v2.107.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> EXIT=0
> ```

## 🤖 Claude *(17:56:30)*


## 🤖 Claude *(17:56:32)*

Aplicado, **exit 0**. Agora prova material (Lei 1 — não declaro pelo "Finished"). Verifico via Management API: tabelas + RLS on + policies + RPCs + constraints + **os grants dos 2 RPCs de dinheiro** (anon/authenticated devem ser `false`, service_role `true` — o perímetro G8).

## 🤖 Claude *(17:56:41)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nREF=$(grep -oE '^VITE_SUPABASE_PROJECT_ID=.*' .env | cut -d= -f2 | tr -d '\"' | tr -d ' ')\nTOKEN=$(cat ~/.supabase/access-token 2>/dev/null | tr -d '\\n ')\n[ -z \"$REF\" ] && echo \"NO_REF\" && exit 1\n[ -z \"$TOKEN\" ] && echo \"NO_TOKEN\" && exit 1\necho \"ref=$REF (token present: ${#TOKEN} chars)\"\nread -r -d '' Q <<'SQL'\nselect jsonb_build_object(\n  'tables',(select count(*) from pg_tables where schemaname='public' and tablename in ('autopilot_plans','autopilot_cycles')),\n  'rls_on',(select count(*) from pg_class c join pg_namespace n on n.oid=c.relnamespace where n.nspname='public' and c.relname in ('autopilot_plans','autopilot_cycles') and c.relrowsecurity),\n  'policies',(select count(*) from pg_policies where schemaname='public' and tablename in ('autopilot_plans','autopilot_cycles')),\n  'rpcs',(select count(*) from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname='public' and p.proname in ('begin_autopilot_cycle','finalize_autopilot_cycle')),\n  'key_constraints',(select jsonb_agg(conname order by conname) from pg_constraint where conname in ('autopilot_cycles_plan_fk','creative_metrics_cycle_fk','autopilot_cycles_id_user_uniq','autopilot_plans_id_user_uniq','autopilot_cycles_refund_le_spend')),\n  'rpc_grants',(select jsonb_agg(jsonb_build_object('fn',proname,'anon',has_function_privilege('anon',oid,'EXECUTE'),'auth',has_function_privilege('authenticated',oid,'EXECUTE'),'svc',has_function_privilege('service_role',oid,'EXECUTE')) order by proname) from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname='public' and p.proname in ('begin_autopilot_cycle','finalize_autopilot_cycle'))\n) as result;\nSQL\nJSON=$(python3 -c \"import json,sys; print(json.dumps({'query': sys.stdin.read()}))\" <<<\"$Q\")\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"$JSON\" | python3 -m json.tool",
  "description": "Verify applied objects + RPC grants via Management API"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ref=bcyvddsykvehvpwstlfa (token present: 44 chars)
> {
>     "message": "Failed to run sql query: ERROR:  42702: column reference \"oid\" is ambiguous\nLINE 7:   'rpc_grants',(select jsonb_agg(jsonb_build_object('fn',proname,'anon',has_function_privilege('anon',oid,'EXECUTE'),'auth',has_function_privilege('authenticated',oid,'EXECUTE'),'svc',has_function_privilege('service_role',oid,'EXECUTE')) order by proname) from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname='public' and p.proname in ('begin_autopilot_cycle','finalize_autopilot_cycle'))\n                                                                                                              ^\n"
> }
> ```

## 🤖 Claude *(17:56:49)*


## 🤖 Claude *(17:56:50)*

Management API conecta (token válido) — só meu `oid` ficou ambíguo. Qualificando `p.oid` e re-rodando.

## 🤖 Claude *(17:56:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nREF=$(grep -oE '^VITE_SUPABASE_PROJECT_ID=.*' .env | cut -d= -f2 | tr -d '\"' | tr -d ' ')\nTOKEN=$(cat ~/.supabase/access-token 2>/dev/null | tr -d '\\n ')\nread -r -d '' Q <<'SQL'\nselect jsonb_build_object(\n  'tables',(select count(*) from pg_tables where schemaname='public' and tablename in ('autopilot_plans','autopilot_cycles')),\n  'rls_on',(select count(*) from pg_class c join pg_namespace n on n.oid=c.relnamespace where n.nspname='public' and c.relname in ('autopilot_plans','autopilot_cycles') and c.relrowsecurity),\n  'policies',(select count(*) from pg_policies where schemaname='public' and tablename in ('autopilot_plans','autopilot_cycles')),\n  'rpcs',(select count(*) from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname='public' and p.proname in ('begin_autopilot_cycle','finalize_autopilot_cycle')),\n  'key_constraints',(select jsonb_agg(conname order by conname) from pg_constraint where conname in ('autopilot_cycles_plan_fk','creative_metrics_cycle_fk','autopilot_cycles_id_user_uniq','autopilot_plans_id_user_uniq','autopilot_cycles_refund_le_spend')),\n  'rpc_grants',(select jsonb_agg(jsonb_build_object('fn',proname,'anon',has_function_privilege('anon',p.oid,'EXECUTE'),'auth',has_function_privilege('authenticated',p.oid,'EXECUTE'),'svc',has_function_privilege('service_role',p.oid,'EXECUTE')) order by proname) from pg_proc p join pg_namespace n on n.oid=p.pronamespace where n.nspname='public' and p.proname in ('begin_autopilot_cycle','finalize_autopilot_cycle'))\n) as result;\nSQL\nJSON=$(python3 -c \"import json,sys; print(json.dumps({'query': sys.stdin.read()}))\" <<<\"$Q\")\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"$JSON\" | python3 -m json.tool",
  "description": "Re-run verification with qualified p.oid"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [
>     {
>         "result": {
>             "rpcs": 2,
>             "rls_on": 2,
>             "tables": 2,
>             "policies": 6,
>             "rpc_grants": [
>                 {
>                     "fn": "begin_autopilot_cycle",
>                     "svc": true,
>                     "anon": false,
>                     "auth": false
>                 },
>                 {
>                     "fn": "finalize_autopilot_cycle",
>                     "svc": true,
>                     "anon": false,
>                     "auth": false
>                 }
>             ],
>             "key_constraints": [
>                 "autopilot_cycles_id_user_uniq",
>                 "autopilot_cycles_plan_fk",
>                 "autopilot_cycles_refund_le_spend",
>                 "autopilot_plans_id_user_uniq",
>                 "creative_metrics_cycle_fk"
>             ]
>         }
>     }
> ]
> ```

## 🤖 Claude *(17:57:17)*


## 🤖 Claude *(17:57:20)*

**Verificação material PASSA** — cada fato provado contra o DB vivo:

| Prova | Resultado |
|---|---|
| Tabelas | **2** (`autopilot_plans`, `autopilot_cycles`) |
| RLS habilitada | **2/2** |
| Policies | **6** (plans 4: select/insert/update/no-delete · cycles 2: select/no-delete) |
| RPCs | **2** |
| **Grants dos RPCs de dinheiro** | `anon=false · auth=false · svc=true` em **ambos** ✅ |
| Constraints-chave | **5/5** (2 FK compostas · 2 UNIQUE · CHECK refund≤spend) |

Falta a prova **comportamental** (o guard dispara vivo, não só no catálogo) — zero-cost: anon rejeitado no boundary + service-role com `projected=0` deve bater o RAISE `22023` antes de mover qualquer centavo.

## 🤖 Claude *(17:57:27)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nURL=\"$SUPABASE_URL/rest/v1/rpc/begin_autopilot_cycle\"\nANON=\"${SUPABASE_PUBLISHABLE_KEY}\"\nSVC=\"${SB_SECRET_KEY}\"\nZERO_UUID=\"00000000-0000-0000-0000-000000000000\"\n\necho \"=== [G-anon] begin_autopilot_cycle as ANON (publishable) \u2192 expect NON-200 (REVOKE live at API) ===\"\ncurl -s -o /tmp/anon.out -w \"HTTP %{http_code}\\n\" -X POST \"$URL\" \\\n  -H \"apikey: $ANON\" -H \"Authorization: Bearer $ANON\" -H \"Content-Type: application/json\" \\\n  -d \"{\\\"p_plan_id\\\":\\\"$ZERO_UUID\\\",\\\"p_user_id\\\":\\\"$ZERO_UUID\\\",\\\"p_projected_mco\\\":92}\"\nhead -c 300 /tmp/anon.out; echo\n\necho \"\"\necho \"=== [G-guard] begin as SERVICE_ROLE with projected=0 \u2192 expect 22023 guard BEFORE any money/plan lookup ===\"\ncurl -s -o /tmp/svc.out -w \"HTTP %{http_code}\\n\" -X POST \"$URL\" \\\n  -H \"apikey: $SVC\" -H \"Authorization: Bearer $SVC\" -H \"Content-Type: application/json\" \\\n  -d \"{\\\"p_plan_id\\\":\\\"$ZERO_UUID\\\",\\\"p_user_id\\\":\\\"$ZERO_UUID\\\",\\\"p_projected_mco\\\":0}\"\nhead -c 400 /tmp/svc.out; echo",
  "description": "Behavioral proof: anon rejected + service-role guard fires zero-cost"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === [G-anon] begin_autopilot_cycle as ANON (publishable) → expect NON-200 (REVOKE live at API) ===
> HTTP 401
> {"code":"42501","details":null,"hint":null,"message":"permission denied for function begin_autopilot_cycle"}
> 
> === [G-guard] begin as SERVICE_ROLE with projected=0 → expect 22023 guard BEFORE any money/plan lookup ===
> HTTP 400
> {"code":"22023","details":null,"hint":null,"message":"begin_autopilot_cycle: projected must be positive, got 0"}
> ```

## 🤖 Claude *(17:58:36)*


## 🤖 Claude *(17:58:40)*

**Prova comportamental PASSA** — o perímetro de dinheiro está vivo:

- **G-anon:** anon → `HTTP 401 · 42501 permission denied for function begin_autopilot_cycle`. O REVOKE é real no boundary da API — cliente não-confiável **não invoca** o RPC de dinheiro. ✅
- **G-guard:** service_role com `projected=0` → `HTTP 400 · 22023 "projected must be positive, got 0"`. Função existe, executa como service_role, e o guard dispara **antes de qualquer lookup de plano ou movimento de saldo** (zero-cost). ✅

Slice da migration **completa e provada materialmente** (catálogo + comportamento). Landando o commit. Localizo a âncora no Key Files do CLAUDE.md primeiro.

## 🤖 Claude *(17:58:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== CLAUDE.md anchors (autopilot/viral/creative/mcoin SOP rows) ===\"\ngrep -nE 'autopilot|viral-autopilot|creative_metrics|[[mcoin-cost-calibration|mcoin-cost-calibration]]|Affiliate credential resolution SOP' CLAUDE.md | head -20",
  "description": "Find CLAUDE.md Key Files insertion anchor"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === CLAUDE.md anchors (autopilot/viral/creative/mcoin SOP rows) ===
> 422:| **mcoCoins cost calibration SOP** | `docs/processes/mcoin-cost-calibration.md` (4×-floor model `mco=ceil(usd/$0.018×4)`; OTD-MCOIN-CALIBRATION closed) |
> 429:| **Affiliate credential resolution SOP** | `docs/processes/affiliate-credential-resolution.md` |
> ```

## 🤖 Claude *(17:58:47)*


## 🤖 Claude *(17:58:48)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/CLAUDE.md",
  "offset": 422,
  "limit": 2
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 422	| **mcoCoins cost calibration SOP** | `docs/processes/mcoin-cost-calibration.md` (4×-floor model `mco=ceil(usd/$0.018×4)`; OTD-MCOIN-CALIBRATION closed) |
> 423	| **QA user-JWT minter** | `scripts/qa/gen-user-jwt.ts` (admin generateLink→verifyOtp→access_token for authenticated edge-fn QA) |
> ```

## 🤖 Claude *(17:58:51)*


## 🤖 Claude *(17:58:58)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/CLAUDE.md",
  "old_string": "| **mcoCoins cost calibration SOP** | `docs/processes/mcoin-cost-calibration.md` (4\u00d7-floor model `mco=ceil(usd/$0.018\u00d74)`; OTD-MCOIN-CALIBRATION closed) |\n| **QA user-JWT minter** | `scripts/qa/gen-user-jwt.ts` (admin generateLink\u2192verifyOtp\u2192access_token for authenticated edge-fn QA) |",
  "new_string": "| **mcoCoins cost calibration SOP** | `docs/processes/mcoin-cost-calibration.md` (4\u00d7-floor model `mco=ceil(usd/$0.018\u00d74)`; OTD-MCOIN-CALIBRATION closed) |\n| **Viral Autopilot cron-identity SOP (Lei 2)** | `docs/processes/autopilot-cron-identity.md` (OTD-VA-008 gate \u2014 cron prova `Bearer SB_SECRET_KEY` in-function + `user_id` server-trusted da linha [nunca body]; pr\u00e9-d\u00e9bito/refund at\u00f4mico FR-VA-007/021; 10 gates) |\n| **Viral Autopilot cadence schema + money RPCs (Fatia 2)** | `supabase/migrations/20260620120000_viral_autopilot_plans.sql` \u00b7 `\u2026120100_viral_autopilot_cycles.sql` (FK composta tenant-escopada + RESTRICTIVE no-delete + fecha FK composta de `creative_metrics`) \u00b7 `\u2026120200_begin_autopilot_cycle.sql` (cap+pr\u00e9-d\u00e9bito at\u00f4mico advisory-lock, service-role-only) \u00b7 `\u2026120300_finalize_autopilot_cycle.sql` (refund cr\u00e9dito-positivo idempotente, espelha `finalize_vision_job`) |\n| **QA user-JWT minter** | `scripts/qa/gen-user-jwt.ts` (admin generateLink\u2192verifyOtp\u2192access_token for authenticated edge-fn QA) |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(17:59:09)*


## 🤖 Claude *(17:59:10)*

Commit do slice (convenção do projeto: sem `Co-Authored-By`, corpo orientado a milestone — memória `feedback_commits`; o git log confirma).

## 🤖 Claude *(17:59:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add CLAUDE.md\ngit commit -q -F - <<'MSG'\nfeat: Viral Autopilot Fatia 2 \u2014 funda\u00e7\u00e3o de cad\u00eancia (tabelas + RPCs de dinheiro) + gate Lei 2\n\nAbre o gate OTD-VA-008 com o SOP antecipado e assenta a funda\u00e7\u00e3o financeira da\ncad\u00eancia aut\u00f4noma (R2), sem ainda mover dinheiro \u2014 as edge functions do cron s\u00e3o\na fatia seguinte. Nenhum centavo se gasta at\u00e9 o runner existir.\n\nSOP (Lei 2 \u2014 escrito antes do c\u00f3digo): docs/processes/autopilot-cron-identity.md\n  Cron prova `Bearer SB_SECRET_KEY` in-function e deriva user_id da linha do banco\n  (autopilot_plans.user_id), nunca do body; pr\u00e9-d\u00e9bito/refund at\u00f4mico; 10 gates.\n\nMigrations (aplicadas + verificadas materialmente):\n  - autopilot_plans / autopilot_cycles: FK composta tenant-escopada, RESTRICTIVE\n    no-delete, write default-deny; fecha a FK composta pendente de creative_metrics.\n  - begin_autopilot_cycle: cap di\u00e1rio + cap por ciclo + saldo + pr\u00e9-d\u00e9bito \u00daNICO sob\n    pg_advisory_xact_lock (anti-TOCTOU), service-role-only.\n  - finalize_autopilot_cycle: refund cr\u00e9dito-positivo idempotente (claim-once),\n    espelha finalize_vision_job; jamais deduct negativo (anti-mint).\n\n/security-review SAFE (0 findings). Prova viva: anon -> 401 permission denied;\nservice-role projected=0 -> 22023 guard antes de qualquer lookup/d\u00e9bito.\nMSG\ngit log --oneline -1",
  "description": "Commit Fatia 2 migration slice"
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
> [90m2:59PM[0m [32mINF[0m 1 commits scanned.
> [90m2:59PM[0m [32mINF[0m scan completed in 28.2ms
> [90m2:59PM[0m [32mINF[0m no leaks found
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.08 seconds)
> ✔️ e2e-output-tripwire (0.01 seconds)
> ✔️ secret-scan (0.03 seconds)
> ✔️ gitleaks-staged (0.07 seconds)
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpost-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m╯[m
> ┃  mesh-reingest ❯ 
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.00 seconds)
> ✔️ mesh-reingest (0.00 seconds)
> 686bae3 feat: Viral Autopilot Fatia 2 — fundação de cadência (tabelas + RPCs de dinheiro) + gate Lei 2
> ```

## 🤖 Claude *(17:59:53)*


## 🤖 Claude *(17:59:56)*

Commit **`686bae3`** — gates de pre-commit (tripwire/secret-scan/gitleaks) limpos, mesh-reingest disparado.

Slice da migration: escrita → `/security-review` SAFE → aplicada → verificada (catálogo + comportamento) → commitada. Agora fecho a metade de verificação que o SOP exige (G3/G4/G5) com o smoke **zero-cost** nomeado no FRD (`smoke-autopilot-budget.ts`) — prova cap-abort/pré-débito/refund-idempotente contra os RPCs vivos, com **usuário descartável** (zero centavo do Sovereign). Modelo no estilo de um smoke existente primeiro.

## 🤖 Claude *(17:59:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== existing smoke style: env load + admin client + throwaway user + cleanup ===\"\nsed -n '1,70p' scripts/qa/smoke-campaign-run.ts 2>/dev/null || ls scripts/qa/ | grep -iE 'smoke' | head",
  "description": "Read existing smoke for house conventions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === existing smoke style: env load + admin client + throwaway user + cleanup ===
> #!/usr/bin/env bun
> /**
>  * Smoke test — campaign-run edge fn (marketing-hub FR-MH-004), USER PATH (real JWT).
>  *
>  * Proves the function's full skeleton at ZERO LLM cost: every guard path (401/422/404/no-steps/402) runs
>  * BEFORE the mcoCoins deduct and BEFORE any orchestrate-content dispatch, and an `email`-channel step is
>  * BLOCKED (never dispatched), so the happy structural path costs only the 10-coin fee on a THROWAWAY balance
>  * and fans out to NOTHING. The real paid cascade (a `social`/`content` step → real orchestrate-content spend)
>  * is intentionally NOT exercised here — it is gated on Sovereign GO.
>  *
>  * Creates two throwaway @example.com users, signs in user1 for a real access_token, asserts the gates, and
>  * CLEANS UP (deletes users → cascade removes profiles/campaigns/steps; mesh observation nodes deleted explicitly).
>  * No production data, no Sovereign balance, no LLM provider $ touched.
>  *
>  * Usage: bun run scripts/qa/smoke-campaign-run.ts
>  */
> import { createClient } from '@supabase/supabase-js';
> 
> const URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL!;
> const SVC = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY)!;
> const PUB = process.env.SUPABASE_PUBLISHABLE_KEY ?? process.env.VITE_SUPABASE_PUBLISHABLE_KEY ?? process.env.SUPABASE_ANON_KEY!;
> if (!URL || !SVC || !PUB) { console.error('Missing env (URL/SVC/PUB)'); process.exit(1); }
> 
> const admin = createClient(URL, SVC, { auth: { persistSession: false } });
> const stamp = Date.now();
> let uid1: string | null = null;
> let uid2: string | null = null;
> let pass = true;
> const createdNodeNames: string[] = [];
> 
> function check(label: string, ok: boolean, detail = '') {
>   console.log(`${ok ? '✅' : '❌'} ${label}${detail ? `  → ${detail}` : ''}`);
>   if (!ok) pass = false;
> }
> 
> interface CrBody {
>   status?: string; error?: string; campaign_id?: string;
>   run_id?: string; steps_dispatched?: number; steps_queued?: number; async?: boolean; new_balance?: number;
> }
> async function call(token: string | null, body: unknown): Promise<{ status: number; body: CrBody }> {
>   const headers: Record<string, string> = { 'Content-Type': 'application/json', apikey: PUB };
>   if (token) headers.Authorization = `Bearer ${token}`;
>   const r = await fetch(`${URL}/functions/v1/campaign-run`, { method: 'POST', headers, body: JSON.stringify(body) });
>   let j: CrBody; const t = await r.text();
>   try { j = JSON.parse(t) as CrBody; } catch { j = { error: t }; }
>   return { status: r.status, body: j };
> }
> 
> async function mkUser(tag: string) {
>   const email = `cr-smoke-${tag}-${stamp}@example.com`;
>   const password = `Aa1!${crypto.randomUUID()}`;
>   const { data, error } = await admin.auth.admin.createUser({ email, password, email_confirm: true });
>   if (error || !data?.user) throw new Error(`createUser(${tag}): ${error?.message}`);
>   return { id: data.user.id, email, password };
> }
> 
> async function mkCampaign(userId: string, name: string) {
>   const { data, error } = await admin.from('campaigns')
>     .insert({ user_id: userId, name, status: 'draft', channels: [] }).select('id').single();
>   if (error || !data) throw new Error(`insert campaign "${name}": ${error?.message}`);
>   return data.id as string;
> }
> 
> async function addStep(campaignId: string, userId: string, channel: string) {
>   const { error } = await admin.from('campaign_steps')
>     .insert({ campaign_id: campaignId, user_id: userId, position: 0, channel, action: 'generate_content' });
>   if (error) throw new Error(`insert step (${channel}): ${error.message}`);
> }
> 
> try {
> ```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-20 - Próximos passos do projeto]]
> * **Próxima Sessão**: [[2026-06-20 - agent-a0ce568b77a1d7483]]
%% --- TIMELINE END --- %%

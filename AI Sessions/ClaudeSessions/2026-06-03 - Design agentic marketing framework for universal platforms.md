# Design agentic marketing framework for universal platforms
**Date:** 2026-06-03 | **Session ID:** `cbb758a7-048b-4acb-94aa-db05a445f1e7`

---

## 👤 User *(00:06:38)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(00:06:38)*

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


## 🤖 Claude *(00:06:44)*


## 🤖 Claude *(00:06:45)*

I'll execute the ShakeHands /handson pick-up protocol. Starting with pre-flight checks in parallel.

## 🤖 Claude *(00:06:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git fetch origin 2>&1 | tail -3; echo \"\u2500\u2500\u2500 log \u2500\u2500\u2500\"; git log --oneline -7; echo \"\u2500\u2500\u2500 status \u2500\u2500\u2500\"; git status --short; echo \"\u2500\u2500\u2500 diff stat \u2500\u2500\u2500\"; git diff HEAD --stat; echo \"\u2500\u2500\u2500 vs origin/main \u2500\u2500\u2500\"; git rev-list --left-right --count HEAD...origin/main 2>/dev/null && echo \"(HEAD <-> origin/main)\"",
  "description": "Git fetch + history + status + divergence vs origin"
}
```

## 🤖 Claude *(00:06:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"\u2500\u2500\u2500 tsc \u2500\u2500\u2500\"; npx tsc --noEmit 2>&1 | tail -20; echo \"EXIT:$?\"",
  "description": "TypeScript strict check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── log ───
> 04b130b chore(sprint): selo v6.20.4 — probe OAuth ML concluído (sem API; portal logado; datacenter bloqueado) + disconnect verificado na UI; decisão #2 aguarda atribuição de clique
> efca29d docs(handoff): seal v6.20.4 — probe OAuth ML concluído + disconnect Meta/social verificado non-destrutivo na UI logada (seal de conhecimento, zero código)
> e75ec98 docs(readme): v6.20.4 — probe OAuth ML (sem API oficial; link exige portal logado; datacenter bloqueado) + disconnect verificado na UI logada
> 844ebcf chore(sprint): update sprint-priorities — v6.20.3 fecha o Top Gap de segredo órfão (disconnect RPC)
> 8338d8a docs(handoff): seal v6.20.3 — disconnect RPC revoga segredo Vault órfão (meta/social)
> ac1cba1 docs(readme): v6.20.3 — disconnect RPC revoga segredo Vault órfão (meta/social)
> 610e1f3 docs(processes): SOP + Key Files do disconnect Meta/social (revogação de órfão)
> ─── status ───
> ─── diff stat ───
> ─── vs origin/main ───
> 0	0
> (HEAD <-> origin/main)
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── tsc ───
> EXIT:0
> ```

## 🤖 Claude *(00:06:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"\u2500\u2500\u2500 docker mcorch \u2500\u2500\u2500\"; docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\" 2>&1; echo \"\u2500\u2500\u2500 docker mega-brain \u2500\u2500\u2500\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\" 2>&1; echo \"\u2500\u2500\u2500 chroma heartbeat \u2500\u2500\u2500\"; curl -s -m 5 http://localhost:8001/api/v2/heartbeat 2>&1; echo \"\"; echo \"\u2500\u2500\u2500 bok suites \u2500\u2500\u2500\"; ls docs/bok/ 2>/dev/null; echo \"\u2500\u2500\u2500 handoff lines \u2500\u2500\u2500\"; wc -l HANDOFF.md; echo \"\u2500\u2500\u2500 scratch \u2500\u2500\u2500\"; ls scratch/ 2>/dev/null && echo \"\u26a0\ufe0f scratch has files\" || echo \"scratch clean \u2705\"",
  "description": "Docker containers + Chroma + BoK suites + HANDOFF line count"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── docker mcorch ───
> mcorch_chroma: Up 10 days (healthy)
> mcorch_claude_mem: Up 10 days (healthy)
> ─── docker mega-brain ───
> mega-brain-dashboard: Up 10 days
> mega-brain-webhook: Up 10 days (healthy)
> mega-brain-daemon: Up 10 days (healthy)
> ─── chroma heartbeat ───
> {"nanosecond heartbeat":1780445211488463986}
> ─── bok suites ───
> aios-sql-bridge
> canvas-design
> constellation-v2
> conteudo-v2
> e2e-user-zero
> gamificacao-nodes
> mcorch-constellation
> mcorch-qa-healing
> mercado-livre-api
> meta-api
> openclaw
> viralmind
> ─── handoff lines ───
> 6361 HANDOFF.md
> ─── scratch ───
> scratch clean ✅
> ```

## 🤖 Claude *(00:07:07)*


## 🤖 Claude *(00:07:09)*

Tudo verde no pre-flight: worktree limpo, HEAD em sync com `origin/main` (0↔0), tsc zero erros, containers healthy, Chroma OK. HANDOFF.md tem 6361 linhas. Lendo as seções (read-from-end strategy) + sprint + BoK gate em paralelo.

## 🤖 Claude *(00:07:10)*


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
> 14	## ML Affiliate OAuth Probe + Disconnect UI Verification Record (2026-06-02)
> 15	
> 16	**v6.20.4 (2026-06-02)** — **Seal de conhecimento — zero código de produção tocado** (working tree limpo do início ao fim). Sessão dirigida por duas diretivas do Sovereign, no padrão **probe-first material**: (#1) fechar o resíduo visual que a v6.20.3 anotou — confirmar o disconnect Meta/social pela UI **logada** — e (#2) destravar a iniciativa do **Operador de Browser Autenticado** decidindo o runtime por **probe ANTES** de qualquer `/bok-scribe`/código.
> 17	
> 18	**#1 — disconnect verificado NON-DESTRUTIVO na UI logada.** Loguei como Usuário Zero via Supabase **Admin API `generate_link`** (magic link — método per-user reproduzível, sem token do DevTools nem senha crua) dirigindo `agent-browser` 0.27.0 (Chromium real). `/dashboard/social` renderiza as 3 contas ativas (LinkedIn/Instagram/Facebook), cada uma com botão Desconectar **interativo** (snapshot refs e11/e12/e13) wired a `rpc('disconnect_social')`; `useMetaConfig.ts:78`/`useSocialAccounts.ts:43` chamam `disconnect_meta`/`disconnect_social` (zero `.delete()` resquício). **Nenhum clique destrutivo** — as 3 contas seguem `is_active`; o clique→RPC→revogação-Vault já era DB-proven na v6.20.3. Fecha o resíduo "browser autenticado indisponível" da seal anterior.
> 19	
> 20	**#2 — probe OAuth ML CONCLUÍDO (veredito material):**
> 21	- **Sem API oficial de afiliados ML** — convergência de múltiplas fontes + 403 até no WebFetch da Anthropic. OAuth/login-consentimento daria só um API token, que não existe p/ afiliados.
> 22	- **Link oficial exige portal LOGADO** — segui o `meli.la` do Usuário Zero → redireciona p/ `mercadolivre.com.br/social/…?matt_word=…&matt_tool=…&ref=<ASSINADO>`. O `ref` é token assinado **não-fabricável**, gerado só no portal.
> 23	- **Datacenter BLOQUEADO p/ browser REAL** — `agent-browser` no portal de afiliados do IP Oracle → página "Hubo un error accediendo a esta pagina" (antes "não-testado"; agora provado). ⇒ Browser Operator **não roda do datacenter**; runtime tem de ser navegador do user ou IP residencial.
> 24	- **Resolver incompleto** — `src/lib/affiliate.ts` seta só `matt_word`; o formato oficial carrega também `matt_tool` (per-user, não armazenado hoje no `affiliate_config`).
> 25	
> 26	**Experimento em curso (Sovereign):** teste de atribuição de clique de links `matt_word`-anexados por dispositivo independente; resultado ~2026-06-03. **Decisão do #2 (Browser Operator vs. só completar o resolver) PAUSADA aguardando o dado.** Não vejo o painel de afiliados (logado + IP bloqueado) — Cérebro sem mãos: Sovereign reporta o nº.
> 27	
> 28	**ORO triplet:** Operator=MCORCH Agent · Reviewer/Owner=Sovereign · blast radius **nulo** (verificação non-destrutiva + probe read-only; nenhuma mutação de produção, nenhuma credencial manuseada).
> 29	
> 30	| Verificação | Resultado |
> 31	|---|---|
> 32	| #1 login UI (Admin API `generate_link`) | ✅ `/dashboard/settings` + `/dashboard/social` logado (sem redirect p/ `/auth`); header 5351 mcoCoins |
> 33	| #1 disconnect wiring | ✅ `rpc('disconnect_social'/'disconnect_meta'/'disconnect_wordpress')`; zero `.delete()` resquício |
> 34	| #1 não-mutação | ✅ 3 contas sociais seguem `is_active=true` (nenhum clique destrutivo) |
> 35	| #2 ML sem API | ✅ múltiplas fontes + 403 (WebFetch) |
> 36	| #2 link oficial = portal | ✅ `meli.la` → `/social/…&ref=<assinado>` não-fabricável |
> 37	| #2 datacenter bloqueado (browser real) | ✅ "Hubo un error accediendo a esta pagina" |
> 38	| `tsc --noEmit` | ✅ 0 erros |
> 39	| Containers / Chroma | ✅ 5 healthy (10d) · Chroma v2 OK |
> 40	| Handoff node | ✅ `af6bffa2-bce8-4c43-952e-67c0db9c3d23` embedded 768d |
> 41	| Mesh | ✅ 8753 nós |
> 42	
> 43	### Survival Laws Self-audit
> 44	```
> 45	Law 1 (Materiality): ✅ toda claim provada NESTE turno — login via Admin API (URL+título+screenshot), wiring por grep do código, não-mutação por REST (3 is_active), probe por redirect real do meli.la + screenshot do bloqueio ML + 403 do WebFetch. Cérebro-sem-mãos declarado p/ o painel de afiliados (logado+IP bloqueado → Sovereign reporta). Zero fabricação. Fase 5c executada. Zero código → sem claims de commit de feature.
> 46	Law 2 (Process): seal de conhecimento; nenhuma feature nova ganhou código — probe-first respeitado (NÃO construí matt_tool/Browser Operator antes do dado). Memória project_authenticated_browser_operator atualizada com o veredito.
> 47	Law 3 (Pruning): contexto < 50%; decisão consciente de selar no ponto natural em vez de misturar #3/LLM-fallback. Probe consolidado por evidência (UUID/screenshot/redirect).
> 48	Law 4 (ORO): ✅ declarado no início da fase de execução.
> 49	```
> 50	
> 51	**Pendências/Próximos:**
> 52	- **[AGUARDANDO DADO ~2026-06-03] Atribuição de clique ML** — Sovereign reporta o nº de cliques do painel (esperado 1→3 se `matt_word` anexado rastrear) + se o painel mostra por-link ou só total. Decide o destino do #2: (a) `matt_word` basta → quase mata o #2; (b) falta `matt_tool` → add campo per-user no `affiliate_config` + testar; (c) precisa do `ref` → `/bok-scribe` do Browser Operator com runtime FORA do datacenter.
> 53	- **[ACHADO LATERAL] 4 linhas `meta_config` sem profile** — Usuário Zero tem 0 meta_config; as 4 linhas no total pertencem a user_ids sem profile (possível resíduo órfão). Investigar/limpar à parte.
> 54	- **[PRAZO] OTD-LLM-FALLBACK SLA 2026-06-07** — Cascading LLM fallback (owner engineer) — candidato a sessão dedicada após fechar os afiliados.
> 55	
> 56	---
> 57	
> 58	## Meta/Social Disconnect — Orphaned-Secret Revocation Record (2026-06-02)
> 59	
> 60	**v6.20.3 (2026-06-02)** — Sessão disparada por duas diretivas do Sovereign: (A) rodar `/security-review` **redundante** apontado para o `87c926f` (o guard de tenant meta/social selado em v6.20.2) — cinto-e-suspensório; e (B) atacar o débito de **segredo Vault órfão** que a própria seal v6.20.2 anotou no Pending. Padrão dominante mantido: **probe-first material** (Management API, todo teste mutante em `BEGIN…ROLLBACK` → zero mutação de produção) + **adversarial verify**. Antes de codar a Parte B, confirmei materialmente que o gap de tenant guard da diretiva original já estava 100% fechado em prod (`pg_get_functiondef` das 2 triggers + ataque comportamental 5/5 → `42501`), evitando uma migration redundante.
> 61	
> 62	**O que foi entregue (Parte B):**
> 63	- **`disconnect_meta()` / `disconnect_social(p_account_id uuid)`** (migration `20260602160000`) — RPCs SECURITY DEFINER, `search_path=''`, fail-closed `28000` sem `auth.uid()`, EXECUTE só `authenticated`. Espelham `disconnect_wordpress`: deletam a linha **E** revogam o segredo Vault. Hooks `useMetaConfig`/`useSocialAccounts` migrados de `.delete()` → `.rpc()`; `types.ts` regenerado (3 entradas: as 2 RPCs + `vault_upsert_secret`).
> 64	- **Guard de tenant por name-binding** (diferença do WP): segredos meta/social são nomeados pelo `id` da linha, não `user_id`. Cada `DELETE` no Vault é double-bound (`id = ref-da-própria-linha` **E** `name = '<prefix>_' || id-da-própria-linha`); como `id` é PK, o id do atacante nunca iguala o da vítima → impossível revogar segredo alheio. Defesa independente: o UUID bruto nunca vaza ao cliente.
> 65	- **Limpeza one-time** dos órfãos preexistentes (`12 → 0` segredos Meta), provadamente orphan-scoped (`NOT EXISTS` linha base via `right(name,36)`), preservando os 3 segredos sociais vivos.
> 66	
> 67	**ORO triplet:** Operator=MCORCH Agent · Reviewer=Sovereign + gate `/security-review` · Owner=Sovereign (blast radius = retenção de plaintext órfão LGPD + integridade do disconnect per-user).
> 68	
> 69	| Verificação | Resultado |
> 70	|---|---|
> 71	| Parte A — `/security-review` do `87c926f` | ✅ **LIMPO 9/10** (net-hardening; `IS DISTINCT FROM` fecha bypass NULL, UPDATE só vê OLD do próprio tenant, sem SQL dinâmico) |
> ```

## 🤖 Claude *(00:07:11)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 72,
  "limit": 340
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 72	| Gap original já fechado (pré-build) | ✅ `pg_get_functiondef` das 2 triggers c/ guard+`42501`+`search_path=""` · ataque comportamental 5/5 `42501` |
> 73	| Suíte RPC (BEGIN/ROLLBACK, dados reais) | ✅ **5/5** — happy meta+social · foreign-id no-op · planted-ref name-binding aguenta · unauth `28000` · zero resíduo |
> 74	| Limpeza de órfãos (preview→apply) | ✅ `12 → 0` segredos Meta órfãos · 3 sociais vivos + 3 linhas intactos |
> 75	| Parte B — `/security-review` da `20260602160000` | ✅ **LIMPO/SAFE 9/10** (PK garante id distinto + UUID não-vazado) |
> 76	| Apply em prod (Mgmt API, txn atômica) | ✅ `20260602160000` no `schema_migrations`; funções SECURITY DEFINER `search_path=""`; EXECUTE authenticated✓/anon revogado✓ |
> 77	| `tsc --noEmit` | ✅ 0 erros |
> 78	| Testes | ✅ 238 passed / 2 skipped · eslint 0 |
> 79	| Frontend deploy | ✅ build exit 0; bundle servido contém `disconnect_meta`/`disconnect_social` + Supabase URL baked |
> 80	| Mesh | ✅ 8752 nós |
> 81	| Containers | ✅ 5 healthy (9d) · Chroma v2 OK |
> 82	| Handoff node | ✅ `f7805e20-bebd-4a30-8533-09806238f135` embedded 768d |
> 83	
> 84	| Commit | Conteúdo |
> 85	|---|---|
> 86	| `76bb9e3` | fix(credentials): disconnect_meta/disconnect_social revogam o segredo Vault órfão |
> 87	| `610e1f3` | docs(processes): SOP + Key Files do disconnect Meta/social (revogação de órfão) |
> 88	| `ac1cba1` | docs(readme): v6.20.3 — disconnect RPC revoga segredo Vault órfão (meta/social) |
> 89	
> 90	### Arquitetura — disconnect com revogação de segredo órfão
> 91	```
> 92	DISCONNECT (meta/social), antes:  client .delete() → INSTEAD OF DELETE → DELETE base row
> 93	                                  → segredo Vault FICA ÓRFÃO (plaintext retido) ❌
> 94	DISCONNECT (meta/social), agora:  client .rpc('disconnect_meta' | 'disconnect_social', {p_account_id})
> 95	   disconnect_*(): IF auth.uid() IS NULL → 28000
> 96	     v_row_id, v_*_ref ← SELECT da PRÓPRIA linha (WHERE user_id = auth.uid() [+ id = p_account_id])
> 97	     DELETE base row
> 98	     DELETE vault.secrets WHERE id = v_*_ref  AND  name = '<prefix>_' || v_row_id   ← double-bind
> 99	       (id é PK ⇒ id-do-atacante ≠ id-da-vítima ⇒ name nunca casa segredo alheio = tenant-safe)
> 100	CLEANUP one-time: DELETE vault.secrets WHERE name ~ '^<prefix>_<uuid>$'
> 101	                  AND NOT EXISTS (linha base com id = right(name,36))   ← só órfãos (12→0)
> 102	```
> 103	
> 104	### Survival Laws Self-audit
> 105	```
> 106	Law 1 (Materiality): ✅ toda claim provada NESTE turno via Management API — gap original já-fechado (pg_get_functiondef + 5/5 comportamental), suíte RPC 5/5 rolled-back, preview→apply da limpeza (12→0 / 3 vivos), pós-apply (funções+grants+tracking), build+bundle servido com as RPCs. Zero fabricação. 1 armadilha divulgada (urllib→Cloudflare 1010 → troquei p/ curl). Fase 5c executada abaixo. NÃO criei migration redundante p/ o gap já fechado (seria fabricar trabalho).
> 107	Law 2 (Process): ✅ SOP credential-disconnect-clear.md estendido (seção disconnect meta/social + equivalência LGPD) antes do commit; CLAUDE.md Key Files. Extensão de feature documentada (disconnect/clear) → sem BoK gate.
> 108	Law 3 (Pruning): investigação focada; outputs consumidos, referência por path/UUID/migration/commit.
> 109	Law 4 (ORO): ✅ declarado no início da Parte B; "faça os dois" = autorização autônoma do Sovereign.
> 110	```
> 111	
> 112	**Pendências/Próximos (anotados p/ próxima sessão):**
> 113	- **E2E no navegador:** o disconnect foi verificado pela perspectiva do banco (RPC 5/5 + bundle servido contém as RPCs); o clique real na UI logada (`/dashboard/settings` → Desconectar Meta/social) não foi executado (browser autenticado indisponível). Confirmar visualmente no próximo passe.
> 114	
> 115	---
> 116	
> 117	## Vault Idempotent Encrypt + Tenant Guard Record (2026-06-02)
> 118	
> 119	**v6.20.2 (2026-06-02)** — Sessão disparada pela dívida residual que a própria seal v6.20.1 anotou no Pending: o `trg_encrypt_user_api_keys` (+ irmãos meta/social) chamava `vault.create_secret` **incondicionalmente** → re-salvar um segredo p/ valor novo colidia no índice único `vault.secrets.name` (`23505`) — o caso "editar a senha WP sem desconectar antes". Padrão dominante: **probe-first material** (Management API, todo teste em `BEGIN…ROLLBACK` → zero mutação de produção) + **adversarial verify** — um achado HIGH do `/security-review` foi REFUTADO materialmente (o overwrite cross-tenant é fail-closed pelo `PRIMARY KEY`, md5 da vítima inalterado), mas a investigação revelou um gap REAL paralelo (injeção cross-tenant id-novo nas INSTEAD OF de meta/social), fechado na mesma sessão.
> 120	
> 121	**O que foi entregue:**
> 122	- **Idempotência (fecha o 23505 no re-save):** helper `public.vault_upsert_secret(value,name,desc)` (`SECURITY DEFINER`, `search_path=''`, EXECUTE revogado de PUBLIC/anon/authenticated → não é RPC alcançável) resolve o segredo por nome e rotaciona in-place via `vault.update_secret` (COALESCE-keep de nome/desc), senão cria; +fallback `unique_violation` p/ a corrida. As 3 encrypt triggers passam a usá-lo + ganham `search_path=''`. A coluna mantém o MESMO UUID Vault entre rotações (sem órfãos). Migration `20260602140000`.
> 123	- **Guard de tenant (fecha injeção cross-tenant):** as INSTEAD OF de `meta_config`/`social_accounts` não tinham o guard `auth.uid()` da `130000`. Views `SECURITY DEFINER` + o WHERE de view não restringe INSERT → autenticado injetava credencial em nome de outro (user_id spoofado + id novo). Guard `42501` portado pras branches INSERT+UPDATE das 2, recriadas **verbatim** do `pg_get_functiondef` live + `search_path=''`. `service_role` isento. Migration `20260602150000`.
> 124	
> 125	**ORO triplet:** Operator=MCORCH Agent · Reviewer/Owner=Sovereign (escopo aprovado: "analise tudo e faça"; toda ação outward com prova material por turno, rolled-back).
> 126	
> 127	| Verificação | Resultado |
> 128	|---|---|
> 129	| 23505 no re-save (prova do bug) | ✅ reproduzido — `ERROR 23505 secrets_name_idx ... trg_encrypt_user_api_keys() line 72` |
> 130	| Re-save pós-fix (`user_api_keys`) | ✅ `{decrypted_wp:"wp-pass-BRAVO", secret_count:1, col_is_uuid_ref:true, sibling_groq_intact:true}` |
> 131	| Re-save pós-fix (`social_accounts`, linha real `39ce0ebb…`) | ✅ `{decrypted_access:"sa-BRAVO", secret_count:1}` |
> 132	| Helper lockdown | ✅ EXECUTE anon/authenticated=false; postgres=true |
> 133	| Injeção cross-tenant ANTES | ✅ atacante criou `meta_config` da vítima (`decrypted_token:"INJECTED-BY-ATTACKER"`) |
> 134	| Injeção cross-tenant DEPOIS | ✅ `42501` nas 2 tabelas; self-insert + `service_role` intactos |
> 135	| HIGH do `/security-review` (overwrite) | ✅ REFUTADO material — PK fail-closed (`23505 social_accounts_pkey`) + md5 vítima inalterado |
> 136	| `tsc --noEmit` | ✅ 0 erros |
> 137	| 2 migrations `/security-review` | ✅ ambas **SAFE** |
> 138	| Migrations aplicadas (Mgmt API, txn) | ✅ `20260602140000`+`20260602150000` no `schema_migrations` |
> 139	| Cleanliness | ✅ meta=0/social=3 linhas · 0 segredos de teste · dados reais intactos |
> 140	| Mesh | ✅ 8751 nós |
> 141	| Containers | ✅ 5 healthy (9d) · Chroma v2 OK |
> 142	| Handoff node | ✅ `ea6a3a17-2804-4de3-b153-31f823a9fdb5` embedded 768d |
> 143	
> 144	| Commit | Conteúdo |
> 145	|---|---|
> 146	| `2db5f62` | fix(credentials): vault_upsert_secret idempotente — elimina 23505 ao rotacionar segredo |
> 147	| `87c926f` | fix(credentials): guard de tenant nas INSTEAD OF de meta_config/social_accounts |
> 148	| `deb661c` | docs(processes): fecha débito de idempotência + guard meta/social no SOP |
> 149	| `beec4aa` | docs(readme): v6.20.2 |
> 150	
> 151	### Arquitetura — idempotência + isolamento de tenant na camada Vault
> 152	```
> 153	RE-SAVE (rotação): encrypt trigger → public.vault_upsert_secret(value,name,desc)
> 154	                   SELECT id FROM vault.secrets WHERE name=p_name
> 155	                     achou → vault.update_secret(id,value)   [mesmo UUID, só rotaciona o valor]
> 156	                     senão → vault.create_secret(...)        [unique_violation → re-resolve+update]
> 157	GUARD (meta/social INSTEAD OF, branches INSERT+UPDATE):
> 158	   auth.role()<>'service_role' AND NEW.user_id<>auth.uid() → 42501
> 159	   (DELETE fica SEM guard de propósito — o WHERE da view mascarada já filtra DELETE/UPDATE/SELECT;
> 160	    só INSERT escapa do WHERE → é exatamente onde o guard entra)
> 161	```
> 162	
> 163	### Survival Laws Self-audit
> 164	```
> 165	Law 1 (Materiality): ✅ toda claim provada NESTE turno via Management API, tudo rolled-back — 23505 reproduzido + before/after de re-save (user_api_keys + social_accounts) + lockdown do helper + injeção antes/depois (42501) + metadados pós-apply + cleanliness. Zero fabricação. Achado HIGH do /security-review REFUTADO com teste material (PK fail-closed + md5 da vítima inalterado), não com argumento. 1 armadilha de ambiente divulgada (`UID` readonly do bash → `$U`). Fase 5c executada abaixo.
> 166	Law 2 (Process): ✅ SOP credential-disconnect-clear.md atualizado (débito → Resolved + bloco de isolamento de tenant) antes do commit; CLAUDE.md Key Files. Bug fix em features documentadas → sem BoK gate.
> 167	Law 3 (Pruning): investigação longa (probes C1-C4, V1-V2, before/after meta+social) — outputs consumidos, referência por path/UUID/migration.
> 168	Law 4 (ORO): ✅ declarado no início; "analise tudo e faça" = autorização autônoma do Sovereign p/ resolver em-sessão + selar.
> 169	```
> 170	
> 171	**Pendências/Próximos (anotados p/ próxima sessão):**
> 172	- ~~**Segredo órfão no disconnect Meta/social:** desconectar Meta (`useMetaConfig.disconnect`) ou social deleta só a linha base via INSTEAD OF DELETE — o segredo Vault (`meta_config_long_lived_token_<id>` etc.) **fica órfão** (plaintext retido). Paralelo ao que `disconnect_wordpress()` resolveu pro WP; precisa de RPC dedicada (nula linha + revoga segredo) + `/security-review`. Débito LGPD/retenção.~~ ✅ **FECHADO 2026-06-02 (v6.20.3)** — RPCs `disconnect_meta()`/`disconnect_social(uuid)` (migration `20260602160000`); 12 segredos Meta órfãos limpos (12→0); ver Record no topo.
> 173	- **E2E no navegador:** verifiquei PostgREST + triggers + Vault pela perspectiva do banco; o clique na UI logada não foi executado (browser autenticado indisponível).
> 174	
> 175	---
> 176	
> 177	## WordPress BYOK Credential-Write Fix + Encrypt Double-Fire Record (2026-06-02)
> 178	
> 179	**v6.20.1 (2026-06-02)** — Sessão disparada pelo P0 que a própria seal v6.20.0 sinalizou: `SocialAccountsPage` salvava/desconectava WordPress via `.upsert(onConflict)` numa VIEW mascarada. Corrigir os 2 `.upsert` reportados revelou um bug **muito maior e pré-existente** na camada `credential_encryption`: o `INSTEAD OF` do `user_api_keys` disparava o trigger de encriptação **2×** numa só statement → `23505`, quebrando connect/save de **qualquer** usuário com linha já existente (não só WP). Padrão dominante: **probe-first material** (Management API) — cada hipótese provada antes de codar, o que pegou o double-fire (que o `.insert` sozinho não resolveria), a colisão do sentinela `••••` no `.update`, e uma escrita cross-tenant que o `ON CONFLICT` mascarava com o crash.
> 180	
> 181	**O que foi entregue:**
> 182	- **Fix dos 2 `.upsert` (SocialAccountsPage):** save → `.insert()` (roteia pelo INSTEAD OF que faz upsert interno; `.upsert` numa view dá HTTP 400 `42P10`); disconnect → RPC **`disconnect_wordpress()`** (`SECURITY DEFINER`, `search_path=''`, escopada a `auth.uid()`) que nula as 3 colunas WP **e deleta o segredo do Vault** (revogação real LGPD; delete amarrado a `id` E nome determinístico → tenant-safe). `null` não limpa via view (guard `COALESCE-NULLIF` preserva). Migration `20260602120000`.
> 183	- **[Descoberto] Fix do double-fire:** `trg_instead_of_user_api_keys` trocado de `INSERT...ON CONFLICT DO UPDATE` (dispara encrypt 2× → `vault.create_secret` nome duplicado → `23505`; `.update` ainda re-encripta o `••••`) para **UPDATE-first / INSERT-if-not-found** (encrypt 1×, igual aos irmãos meta/social) + **guard de tenant** (`auth.uid()` → `42501`). `wp_site_url`/`wp_username` viraram `COALESCE(NEW,base)` (não zeram em save parcial). Migration `20260602130000`. Só `user_api_keys` usava `ON CONFLICT`.
> 184	- **types.ts** regenerado (inclui `disconnect_wordpress`); **SOP** `docs/processes/credential-disconnect-clear.md` (Lei 2 + Obstáculo→Síntese); 3 entradas na Key Files Reference.
> 185	
> 186	**ORO triplet:** Operator=MCORCH Agent · Reviewer/Owner=Sovereign (escopo profundo aprovado explicitamente via AskUserQuestion; toda ação outward com provas materiais por turno).
> 187	
> 188	| Verificação | Resultado |
> 189	|---|---|
> 190	| `.upsert` na view (prova do bug) | ✅ HTTP **400 `42P10`** reproduzido |
> 191	| connect pós-fix (caso 23505) | ✅ persiste + cifra (base=UUID, 1 segredo Vault), groq intacto |
> 192	| `.update` pós-fix (caso 23505 groq) | ✅ sucesso, sem re-encriptar `••••`, `wp_site_url` preservado |
> 193	| `disconnect_wordpress()` | ✅ 3 cols `null` + segredo Vault deletado + AI keys intactas |
> 194	| guard cross-tenant | ✅ `ERROR 42501 cannot write credentials for another user` |
> 195	| `tsc --noEmit` | ✅ 0 erros |
> 196	| 2 migrations `/security-review` | ✅ ambas **SAFE** |
> 197	| `db push` (ambas) | ✅ Finished · `20260602120000`+`20260602130000` no remoto |
> 198	| Frontend deploy (nginx) | ✅ chunk `SocialAccountsPage-4_GWJ_p-.js` com `disconnect_wordpress`, `.env` baked |
> 199	| Mesh | ✅ 8750 nós |
> 200	| Containers | ✅ 5 healthy (9d) · Chroma v2 OK |
> 201	| Handoff node | ✅ `7bf9bb0e-a063-43d9-b473-0dd7cdfc97d3` embedded 768d |
> 202	
> 203	| Commit | Conteúdo |
> 204	|---|---|
> 205	| `5dc8084` | fix(credentials): disconnect_wordpress RPC + elimina double-fire do INSTEAD OF |
> 206	| `bafa7a2` | fix(settings): WordPress conecta via .insert e desconecta via RPC |
> 207	| `377251e` | docs(processes): SOP de disconnect/clear de credencial |
> 208	| `6b2f8db` | docs(readme): v6.20.1 |
> 209	
> 210	### Arquitetura — write/clear de credencial nas views Vault-mascaradas
> 211	```
> 212	SAVE  (cliente): .insert() → INSTEAD OF (UPDATE-first / INSERT-if-not-found) → encrypt trigger 1× → vault.create_secret
> 213	                 guard: auth.role()<>'service_role' AND NEW.user_id<>auth.uid() → 42501
> 214	CLEAR (cliente): supabase.rpc('disconnect_wordpress') → SECURITY DEFINER auth.uid() →
> 215	                 UPDATE base SET wp_*=NULL + DELETE vault.secrets WHERE id=ref AND name='...<uid>'
> 216	NUNCA: .upsert (400 42P10) · null-write via view (COALESCE preserva) · INSERT...ON CONFLICT (double-fire 23505)
> 217	```
> 218	
> 219	### Survival Laws Self-audit
> 220	```
> 221	Law 1 (Materiality): ✅ toda claim provada NESTE turno via Management API — 400 42P10 real, connect/disconnect/guard com SELECT em decrypted_user_api_keys + vault.secrets, db push Finished, 2 /security-review SAFE, chunk servido com a string nova, node 7bf9bb0e embedded. Zero fabricação. O double-fire foi PROVADO (T1/T3/T4 + vault.create_secret = INSERT sem ON CONFLICT) antes de afirmar que existia. Fase 5c executada abaixo.
> 222	Law 2 (Process): ✅ SOP credential-disconnect-clear.md antes do commit; dívida residual documentada + task spawned.
> 223	Law 3 (Pruning): contexto longo de investigação (T1-T5) — outputs de exploração consumidos, referência por path/UUID.
> 224	Law 4 (ORO): ✅ declarado no início; escopo profundo aprovado explicitamente pelo Sovereign via AskUserQuestion.
> 225	```
> 226	
> 227	**Pendências/Próximos (anotados p/ próxima sessão):**
> 228	- ~~**Dívida residual (task spawned):** tornar `trg_encrypt_user_api_keys` (+ irmãos meta/social) idempotente (update-or-create por nome) — editar um segredo p/ valor novo sem desconectar antes ainda dá `23505`.~~ ✅ **FECHADA em v6.20.2** (migration `20260602140000`, helper `vault_upsert_secret`; + guard de tenant meta/social `20260602150000`).
> 229	- **E2E no navegador:** verifiquei todas as camadas abaixo da UI (PostgREST 400/201 + triggers + RPC + Vault); o clique na UI logada não foi executado (browser autenticado indisponível).
> 230	
> 231	---
> 232	
> 233	## Afiliados Híbrido + Catálogo Apify Real + BYOK per-user Record (2026-06-01)
> 234	
> 235	**v6.20.0 (2026-06-01)** — Sessão disparada pelo Sovereign dogfoodando `/dashboard/affiliate-products`: o link de afiliado copiado abria a **tela de login do CloudPanel** em vez do produto. Fluxo: diagnóstico material → fix dos links → enriquecimento do catálogo → descoberta de produtos → BYOK per-user → seal. Padrão dominante: **probe-first** (provar materialmente antes de construir) — economizou esforço em 3 becos (API ML, Firecrawl, actor com selectors velhos) e pegou 2 IDs fabricados + 1 regressão de credencial no `/security-review`.
> 236	
> 237	**O que foi entregue:**
> 238	- **Fix dos links de afiliado (híbrido meli.la/matt_word):** o catálogo e `process-affiliate-link` (GET+POST) roteavam via `panel.gcrux.com/api/ml-redirect` (proxy morto = login wall, zero atribuição) usando o `app_id` OAuth como affiliate id — ambos banidos pelo SOP. Agora resolve em camadas: short link `meli.la` **cravado** (per-user em `affiliate_config.metadata.shortlinks[MLB]`) quando existir, senão `product_url` real + `matt_word=<affiliate_tag>`, **fail-closed**. `src/lib/affiliate.ts` puro (`resolveAffiliateLink`/`buildMattWordUrl`/`isMlShortLink`/`readShortlinks`) + 14 testes; editor de link cravado por produto na página; `useAffiliateConfig` expõe `affiliate_tag` + `setProductShortlink`. Prova: 302s reais da edge function — `MLB27834876`→`meli.la/2gh13Sw` (override) · `MLB36263268`→`mercadolivre.com.br/p/...?matt_word=caga6077534` (fallback), zero `panel.gcrux.com`.
> 239	- **Catálogo real via Apify (ML bloqueia todo server-side):** provado materialmente que `api.mercadolibre.com/{items,products,search,categories}` → 403/401 e a página → 302 `/gz/account-verification`, **tanto do nosso IP quanto da Supabase Edge** (probe `ml-probe` deployada+deletada). OAuth não furaria (IP-block). Único caminho: actor Apify residencial `karamelo~mercadolivre-scraper-brasil-portugues` (devolve `eTituloProduto`/`novoPreco`/`imagemLink`/`SKU`). `scripts/enrich-affiliate-products.ts` (busca por nome → casa `SKU===external_id` → preço/foto/disponibilidade, retry anti-bot intermitente, resolução token per-user→sistema) + `scripts/discover-affiliate-products.ts` (descoberta real — valida "viral mind") + `useAffiliateProducts` gate (só lista `is_active`+`price`+`availability=available`; `hiddenCount`) + cron `affiliate-enrich-cron.sh` 6/6h.
> 240	- **2 produtos fabricados removidos:** `MLB36263268`/`MLB37674259` eram IDs inventados (link-forge hardcoded — nunca "descobertos"); busca real retornou SKUs reais diferentes → DELETE permanente. Catálogo agora: **3 produtos reais novos** — Roborock S8 Pro Ultra `MLB27834876` R$17.770 · Family Hub `MLB32642694` R$18.946 · 75" 8K Neo QLED QN900B `MLB4699602679` R$39.000 (todos `available`, foto+preço reais).
> 241	- **BYOK per-user `apify_token`:** migration `20260601060000` adiciona `apify_token` no padrão Vault de `credential_encryption` (coluna → trigger cifragem → view mascarada → INSTEAD OF → decrypted view service_role-only) — **passou `/security-review`**, que pegou e corrigiu eu revertendo a view mascarada p/ `security_invoker` sem o `WHERE` (quebraria leitura authenticated). Resolução em camadas per-user→`APIFY_TOKENS` sistema (provada: `--user` resolveu o token do Sovereign e dirigiu um scrape real). Campo no `SettingsPage`. **Corrige P0 pré-existente de `000600`:** `useUserApiKeys.saveKeys` usava `.upsert()` → HTTP 400 (view sem constraint) → `.insert()` (INSTEAD OF trigger faz upsert via `ON CONFLICT user_id`).
> 242	
> 243	**ORO triplet:** Operator=MCORCH Agent · Reviewer/Owner=Sovereign (todas as ações outward — DB writes, deploys, migration Vault, gasto Apify — com GO explícito; provas materiais por turno).
> 244	
> 245	| Verificação | Resultado |
> 246	|---|---|
> 247	| `tsc --noEmit` | ✅ 0 erros |
> 248	| Suite vitest | ✅ **238 passed / 2 skipped / 240** (+14 testes `affiliate.test.ts`) |
> 249	| Migration Vault aplicada | ✅ `db push` exit 0 · chaves existentes ainda decifram (openrouter/groq) · `apify_token` round-trip OK · mascarada na view pública |
> 250	| `/security-review` | ✅ 0 findings + pegou/corrigiu regressão `security_invoker` |
> 251	| BYOK per-user funcional | ✅ `--user` → token resolvido → scrape Roborock matched R$17.770 |
> 252	| Edge 302s (deploy 82.73 kB) | ✅ override→meli.la · fallback→ML real · zero panel.gcrux |
> 253	| Frontend deploy (nginx) | ✅ chunks `AffiliateProductsPage`/`SettingsPage` servidos HTTP 200 com código novo |
> 254	| Cron monitoramento | ✅ `0 */6 * * *` instalado (vizinhos intactos) |
> 255	| Containers | ✅ 5 healthy (9d) · Chroma v2 OK |
> 256	| Handoff node | ✅ `af33a839-acd9-412d-a770-8ad5a2edccb4` embedded 768d |
> 257	
> 258	| Commit | Conteúdo |
> 259	|---|---|
> 260	| `4a9df8d` | feat(afiliados): links híbridos meli.la/matt_word — fim do proxy morto |
> 261	| `5288bb8` | feat(afiliados): enriquecimento Apify + descoberta + gate + cron |
> 262	| `fb07323` | feat(settings): BYOK Apify token per-user (Vault) + fix salvamento de chaves |
> 263	| `adcbd6f` | docs(afiliados): SOPs + revenue-flywheel com IDs reais |
> 264	| `eb9653d` | docs(readme): v6.20.0 |
> 265	
> 266	### Arquitetura — resolução de link de afiliado (híbrida, OTD-ML-001)
> 267	```
> 268	resolveAffiliateLink(product, config):
> 269	  1. config.metadata.shortlinks[external_id] é meli.la/sec?  → { shortlink }   (definitivo, per-user)
> 270	  2. config.affiliate_tag presente?  → product_url + ?matt_word=<tag>+utm      (best-effort)
> 271	  3. senão → { needs_config }  (fail-closed — nunca link sem atribuição)
> 272	process-affiliate-link GET (clique do leitor): node→owner→affiliate_config → mesma resolução → 302 ML real
> 273	Enriquecimento: Apify karamelo (residencial) → SKU match → vm_affiliate_products{price,image_url,availability}
> 274	  token: per-user (decrypted_user_api_keys.apify_token) → sistema (APIFY_TOKENS)
> 275	```
> 276	
> 277	### Survival Laws Self-audit
> 278	```
> 279	Law 1 (Materiality): ✅ toda claim provada NESTE turno — 302s reais, db push exit 0, round-trips (sem imprimir segredo), suite 238/240, nginx 200, scrape matched. Quando o ML bloqueou tudo, disse "não dá" (probe ml-probe) em vez de fabricar. O 8K errado (4K→usado) foi corrigido materialmente 2×, não maquiado. Fase 5c executada (veredito mecânico abaixo).
> 280	Law 2 (Process): ✅ 2 SOPs (ml-affiliate-attribution atualizada + affiliate-catalog-enrichment nova) antes/junto do código. Migration passou /security-review (regra CLAUDE.md). API Tenancy (per-user→sistema) honrada.
> 281	Law 3 (Pruning): ✅ checkpoint explícito antes do BYOK (item de maior blast radius isolado); probes (Firecrawl/ml-probe) extraídos a conclusão e deletados.
> 282	Law 4 (ORO): ✅ triplet declarado; toda ação outward com GO Sovereign.
> 283	```
> 284	
> 285	**Pendências/Próximos (anotados p/ próxima sessão):**
> 286	- **Operador de Browser Autenticado (módulo novo — PROBE-FIRST):** browser LOGADO humano-paced p/ ações que nos barram (canônico: ML "Compartilhar" → `meli.la` cravado → gravar em `shortlinks`). Datacenter IP bloqueado até p/ browser real; logado não-testado. Decisões Sovereign: probe de viabilidade → runtime decidido após probe → `/bok-scribe` (BoK Gate) → build. Auth = login interativo 1×+profile persistido, sem senha crua. Tool: `agent-browser`. Memória: `project_authenticated_browser_operator`.
> 287	- **P0 pré-existente (de `000600`, NÃO desta sessão) — task spawnada:** `SocialAccountsPage.tsx:51,68` salva/desconecta WordPress via `user_api_keys.upsert(onConflict)` → 400, e disconnect com null não limpa (COALESCE-guard). Fix: `.insert()` + clear via service-role. Memória: `reference_encrypted_views_write_pattern`.
> 288	- **8K via keyword é fuzzy:** descoberta do 8K exigiu filtro de título (`\b8k\b` + NEW) — keyword "8k" sozinha traz 4K. Refinar termos por categoria ao descobrir.
> 289	
> 290	---
> 291	
> 292	## e2e-user-zero v2 + 3-Stream Sweep Record (2026-06-01)
> 293	
> 294	**v6.19.0 (2026-06-01)** — Sessão de execução de 3 streams autorizados pelo Sovereign (e2e-user-zero 2ª iteração · gaps reais do Canvas · 1ª campanha real). Padrão dominante: **o código estava sistematicamente à frente dos próprios Pending Actions** — verificação material (Lei 1) ANTES de codar evitou reconstruir 2 features já prontas. Fluxo: `/handson` → priorização → descoberta de que Canvas 4.2 + consistência já estavam shipados → build real do Stream B → readiness do Stream C → seal.
> 295	
> 296	**O que foi entregue:**
> 297	- **Stream B — e2e-user-zero 2ª iteração (build real):** `scripts/qa/e2e-user-zero/lib/redactor.ts` (LGPD Layer 2 — redação de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body em `redactedPaths` + sanitização de cookie; `scanResidualSecrets` p/ o tripwire), `scripts/qa/e2e-user-zero/lib/mesh-persistor.ts` (finding → `observation` node + aresta `OBSERVES`, idempotente via SHA-256 do `name`, fail-soft, `SB_SECRET_KEY`), `scripts/qa/e2e-user-zero/lib/telemetry.ts` (pulse de ciclo de vida em `infra_health_logs`), 6 flows (`dashboard-tour`·`orchestrate-pipeline-view`·`content-library`·`billing-flow`·`settings-tour`·`constellation-view`) + helper `_nav-capture`, runner fiado (started/complete/failure/auth-expired exit-3 + persist), selftest vitest `src/test/e2e-user-zero-selftest.test.ts` (8 testes). Guard do runner endurecido (`includes("runner")` pegava `runner.test.ts`).
> 298	- **Stream A — consistência + Canvas 4.2 (VERIFICADO, não reconstruído):** auditoria material confirmou reference threading + seed-lock (`generateReplicate:675-690`·`generateOpenRouter:749-759` + inspectors/pipeline `findUpstreamImages` + toggle `fixedSeed`) e os 5 nós tipados + pipeline async de vídeo JÁ shipados. Único gap real fechado: `higgsfield-webhook` mapeia `nsfw`/`canceled` p/ razão clara de soft-fail (sem cobrança).
> 299	- **Pre-commit hardening + versionamento:** `scripts/hooks/pre-commit` (cópia versionada; antes só viva em `.git/hooks`) + README; PATTERN ampliado (`sk_/rk_(live|test)_`·`whsec_`·`sbp_`·`sb_secret_`·`r8_`) + tripwire de diretório que escaneia o `e2e-output/` gitignored (defesa Layer 4). Testado: bloqueia secret plantado (exit 1) · libera limpo (exit 0).
> 300	- **Stream C — readiness (gated):** flywheel sondado read-only — `orchestrate-content` HTTP 200, `affiliate_config` Sovereign `ada39fae` mercadolivre `is_active:true`, `mco_balance` 5351, Higgsfield creds presentes. Execução (publica + gasta) **gated em GO Sovereign**.
> 301	
> 302	**ORO triplet:** Operator=MCORCH Agent · Reviewer/Owner=Sovereign (Stream C paga/externa não disparada sem GO; deploy do `higgsfield-webhook` idem).
> 303	
> 304	| Verificação | Resultado |
> 305	|---|---|
> 306	| Selftest e2e-user-zero | ✅ 8/8 (vitest) |
> 307	| Suite completa | ✅ 224 passed / 2 skipped / 226 · **exit 0** — os 2 smokes live (canvas pago + sql-bridge) gateados por `RUN_LIVE_SMOKE` neste seal (antes falhavam por chave revogada); +8 desta sessão, baseline git-stash 218→226 |
> 308	| `tsc --noEmit` | ✅ 0 erros |
> 309	| Pre-commit tripwire | ✅ bloqueia secret em e2e-output (exit 1) · libera limpo (exit 0) · PATTERN pega sbp_ no staged-diff |
> 310	| Stream A consistência | ✅ wired backend+frontend — verificado por grep material, não reconstruído |
> 311	| Stream C readiness | ✅ orchestrate-content 200 · affiliate ativo · balance 5351 |
> 312	| Handoff node | ✅ `59f92fe0-e346-4320-aeaf-842a91458125` embedded 768d (chunks:1, openai/text-embedding-3-small) |
> 313	| Containers | ✅ 5 healthy · Chroma v2 OK |
> 314	
> 315	| Commit | Conteúdo |
> 316	|---|---|
> 317	| `cf6e464` | feat(e2e-user-zero): 2ª iteração — redactor + mesh-persistor + telemetry + 6 flows + selftest |
> 318	| `e788d76` | chore(hooks): versiona pre-commit + tripwire e2e-output |
> 319	| `09a5bae` | fix(higgsfield-webhook): nsfw/canceled soft-fail claro |
> 320	| `5f21caf` | docs(readme): v6.19.0 |
> 321	| `0c5eefd` | fix(tests): gateia smokes live (canvas pago + sql-bridge) atrás de RUN_LIVE_SMOKE → suíte verde |
> 322	
> 323	### Arquitetura — e2e-user-zero runner (v2)
> 324	```
> 325	runner.ts (focused) → emitRunStarted (telemetry)
> 326	  → flow(driver, ctx) [6 dashboard flows + auth-login, static whitelist]
> 327	  → classify() → buildReport() → report.md + findings.json
> 328	  → insertFindings() [mesh-persistor: observation node + OBSERVES edge, idempotent, fail-soft]
> 329	  → emitRunComplete (telemetry: infra_health_logs pulse) · exit 0/1/2/3
> 330	Defesa de segredo: redactor (Layer 2) → .gitignore e2e-output/ (Layer 3) → pre-commit tripwire (Layer 4)
> 331	```
> 332	
> 333	### Survival Laws Self-audit
> 334	```
> 335	Law 1 (Materiality): ✅ toda claim provada NESTE turno — selftest 8/8 + suite 224/226 + git-stash baseline (prova de zero regressão) + tsc 0 + hook testado (exit 1/0) + handoff node embedded via REST + readiness via curl real. Descoberta-chave: 2 features "pendentes" estavam shipadas (provado por grep de código real antes de codar) → zero retrabalho/fabricação. Excerpt do mesh-persistor do SDD corrigido contra schema real (relation_type + SB_SECRET_KEY).
> 336	Law 2 (Process): ✅ e2e-user-zero BoK 9/9 + SDD como SSOT. Webhook é fix em feature documentada. Desvio consciente: selftest em src/test/ (vitest include=src/**) — justificado. OTD-E2E-TELEM-001 registrada (infra_health_logs sem coluna metadata → migration aditiva diferida a /security-review).
> 337	Law 3 (Pruning): ✅ 2 podas explícitas (relatórios dos subagentes após extração de conclusões; detalhes de impl do Stream B no checkpoint).
> 338	Law 4 (ORO): ✅ triplet por stream; Stream C paga/externa gated em Sovereign.
> 339	```
> 340	
> 341	---
> 342	
> 343	## Constellation v2 Cockpit Live — Fase 3+4 E2E + Build/Login/Settings Fixes Record (2026-06-01)
> 344	
> 345	**v6.18.0 (2026-06-01)** — Sessão densa que levou a Constelação v2 de casca decorativa a **cockpit operacional per-user provado ponta-a-ponta**, mais 3 incidentes de produção resolvidos (build quebrado, P0 login, teste de chaves). Fluxo: `/handson` → resolver alertas prioritários → Fase 3 UI → (o gate de build revelou um blocker pré-existente do lucide) → P0 login reportado pelo Sovereign → Fase 0 reset destrutivo → botão Zerar → teste de chaves falhando (descoberta da cripto de credenciais) → Tabs → Fase 4 E2E provado → este selo.
> 346	
> 347	**O que foi entregue:**
> 348	- **Fase 3 — cockpit (`constellation-v2`, BoK selada `38d7e7a4`):** empty-state com CTA duplo (`EmptyConstellation`) + wizard 2-portas (`CrewWizard` + `useCreateCrew`: mapa 4×4 = Núcleo + 4 Leads + 13 subagentes módulo-bound, OU builder guiado depto→capability→nome) com keys estáveis (FR-CV2-006) + upsert idempotente; `AccessConfigCard` (BYOK + cap diário por subagente, FR-CV2-023); `useAgentTask`+`agent-task-result` (FR-CV2-004: envia `capability_key`, trata 402/422/502+`status:failed`); `useAgentActivity` projeta capability/result nos Live Logs (FR-CV2-050); `CrewGraph` cap≤21 + LOD + z-index estrito (FR-CV2-060/061); botão legado "Deploy Enterprise" → "Criar crew".
> 349	- **Fase 0 — reset destrutivo:** `scripts/reset-constellation-v2.ts --execute` arquivou 35 execs → wipou 746 crew_agents + 717 crew_edges → 0; `profiles`=1 intacto. Verificado independente via REST.
> 350	- **Botão "Zerar" per-user** (`useResetCrew`, RLS-scoped a `auth.uid()`): qualquer user reinicia do zero / re-semeia o 4×4 quando quiser. Preserva `mco_balance` e histórico.
> 351	- **Blocker de build (pré-existente) morto:** `lucide-react@1.x` removeu os ícones de marca → `vite build` (rollup) quebrava em `MetaConfigCard`/`v0-ai-chat` enquanto o dev (esbuild) tolerava → produção servia bundle stale de May-30. Fix: shim local `src/components/icons/brand-icons.tsx` + anticorpo `scripts/qa/audit-lucide-imports.ts` (cruza imports de lucide vs exports reais).
> 352	- **P0 login (outage):** o bundle vivo assava uma publishable key que a migration de cripto rotacionou/desregistrou (`UNAUTHORIZED_UNREGISTERED_API_KEY` em `/auth/v1/user`); redeploy assou a registrada do `.env`. Env-driven (`client.ts` lê `import.meta.env`), então o rebuild foi o fix. Lição na memória [[reference_supabase_keys_migrated]].
> 353	- **Teste de chaves server-side + Tabs:** `user_api_keys` é VIEW que mascara (migration `credential_encryption`); o cliente só via `••••` → teste client-side mandava o mask → 401 sempre ("Falhou" ≠ chave inválida). Edge fn `test-api-key` (JWT-guarded) resolve a chave real (`decrypted_user_api_keys` ou valor digitado) e testa server-side (cobre Replicate, que bloqueia CORS). 4 seções de Settings em Tabs. Lição na memória [[reference_user_api_keys_encrypted]].
> 354	
> 355	**Prova material da Fase 4 (E2E):** exec `488a7744-ceb6-4048-a482-f78462e0aa2a` → capability `watchdog_infra` → `get-infra-status` → `done` · `cost_mcoin` 0 · `latency_ms` 255 · `result_summary` `{"chroma":"healthy","intelligence":"healthy",...}` (output real do módulo). Primeira execução real no cockpit per-user pós-reset, com o nó pulsando e o Live Logs exibindo o resultado.
> 356	
> 357	**ORO triplet:** Operator=MCORCH Agent · Reviewer/Owner=Sovereign (Fase 0 destrutiva + deploys de produção autorizados explicitamente; blast radius: 746 crew decorativos apagados/arquivados, `profiles`+ledger preservados).
> 358	
> 359	| Verificação | Resultado |
> 360	|---|---|
> 361	| Fase 4 E2E exec | ✅ `488a7744` done · watchdog_infra · 0 mco · 255ms · result real |
> 362	| Fase 0 reset | ✅ crew 0 · archive 35 · profiles 1 (REST independente) |
> 363	| Build lucide | ✅ audit 5835 exports limpo · `built in ~22s` · prod desbloqueado |
> 364	| P0 login | ✅ index.html → `index-BY2MQsU-` → chave `FkE` registrada · chunks velhos 404 |
> 365	| `test-api-key` edge fn | ✅ deploy 103.5kB · OPTIONS 200 · sem JWT 401 |
> 366	| Chaves no Vault | ✅ `decrypted_user_api_keys` = reais válidas (prefixos `gsk_`/`sk-o`/`sk-p`/`AIza`/`r8_`) |
> 367	| `tsc --noEmit` | ✅ 0 erros |
> 368	| Handoff node | ✅ `a0eb5da7-d2b1-43b0-9ee6-cfb6cccd14c9` embedded 768d |
> 369	| Mesh total | **8746 nós / 9070 arestas** (REST count=exact) |
> 370	| Containers | ✅ 5 healthy |
> 371	
> 372	| Commit | Conteúdo |
> 373	|---|---|
> 374	| `9a4b569` | fix(build): lucide brand-icon shim + audit antibody |
> 375	| `7b2b277` | feat(constellation-v2): Fase 3 cockpit + wizard + capability real |
> 376	| `8ed3f78` | docs: runbooks → SB_SECRET_KEY |
> 377	| `9a13545` | feat(constellation-v2): botão Zerar per-user |
> 378	| `8a0c547` | fix(settings): teste de chaves server-side |
> 379	| `1dacd10` | feat(settings): tabs IA/WordPress/Meta/LGPD |
> 380	| `18dd696` | docs(readme): v6.18.0 |
> 381	
> 382	### Arquitetura — capability execution (v2)
> 383	```
> 384	Subagente (capability_key) → AgentDetail "Executar capability"
> 385	  → agent-task-execute (ramo capability): resolve agent_capabilities allowlist → denylist sistema → cap check
> 386	  → invoke target_function (get-infra-status) c/ JWT do user → meter (module_self_bills → 0)
> 387	  → agent_executions (done, result_summary) → useAgentActivity → Live Logs + pulse 3D
> 388	```
> 389	
> 390	### Arquitetura — credenciais BYOK (descoberta da sessão)
> 391	```
> 392	Settings (form) → user_api_keys (VIEW que MASCARA: •••• no SELECT)        [cliente nunca vê a chave]
> 393	INSTEAD OF trigger → cifra no Supabase Vault (user_api_keys_table)         [COALESCE(NULLIF(mask)) preserva]
> 394	Edge fns / test-api-key → decrypted_user_api_keys (descriptografa)         [chave real, server-side]
> 395	```
> 396	
> 397	### Survival Laws Self-audit
> 398	```
> 399	Law 1 (Materiality): ✅ toda claim provada NESTE turno (exec 488a7744 + reset counts + mesh count via REST · build exit 0 · chunks servidos via curl · decrypted keys reais · handoff node embedded). Zero fabricação. 3 hipóteses minhas REFUTADAS com evidência e corrigidas em aberto (CORS dos provedores liberado; masks = cripto-por-design, não corrupção; causa = credential_encryption, não a v6.17.0). Nenhuma escondida.
> 400	Law 2 (Process): ✅ Fase 0 com SOP (reset script PROC-CV2-005) + plano persistido `.claude/context/execution-plan-constellation-v2.md`. `test-api-key`/Zerar são fix/utilitário dentro de features documentadas (settings + constellation-v2 BoK selada). Botão Zerar = mesmo processo do reset admin, per-user.
> 401	Law 3 (Pruning): ✅ poda no /handoff; plano constellation-v2 persiste o detalhe das fases.
> 402	Law 4 (ORO): ✅ triplet declarado nas tasks destrutivas; Fase 0 (wipe) e cada deploy de produção autorizados explicitamente pelo Sovereign.
> 403	```
> 404	
> 405	## Service_role Key Leak — Full Cutover + Revoke (P0 closed) Record (2026-06-01)
> 406	
> 407	**v6.17.0 (2026-06-01)** — Resposta completa a um incidente de segurança **P0**: o GitGuardian sinalizou (a) um falso-positivo (senhas de teste throwaway em smoke scripts) e (b) — grave — uma **`service_role` JWT legada hardcoded** em `scripts/backfill-embeddings-priority.sh` + na migration `20260503120000`, **pública na `main` há ~1 mês** e provada **viva** (probe HTTP 200). A chave-mestra bypassa toda a RLS. Fluxo: diagnóstico material → cutover backward-compatible pras chaves novas do Supabase → Sovereign desabilitou as legacy + revogou a signing key HS256 → **leak criptograficamente morto, provado**.
> 408	
> 409	**O que foi entregue:**
> 410	- **Cutover (52 edge fns + 57 scripts):** `SUPABASE_SERVICE_ROLE_KEY` → `SB_SECRET_KEY ?? SERVICE_ROLE_KEY`; `SUPABASE_ANON_KEY` (getUser) → `SB_PUBLISHABLE_KEY ?? ANON_KEY`. Nomes não-`SUPABASE_` porque o prefixo é reservado p/ Function secrets. `config.toml`: `verify_jwt=false` em publish-social/refresh-social-token/embed-mcorch-node (service→service com a chave nova, que não é JWT) — cada uma com gate de auth in-code (user válido OU service, senão 401; embed ganhou gate novo + fail-closed). Trigger `mcorch_embed_on_insert` reescrito pra ler a chave do **Supabase Vault** (`sb_secret_key`) — zero literal.
> 411	- **Passos por mim (CLI autenticado):** Function secrets `SB_SECRET_KEY`+`SB_PUBLISHABLE_KEY` · Vault `sb_secret_key` criado · **52 functions deployadas** · migration `20260601050000` aplicada (`db push`). Smoke pré-revoke: chave nova OK, público → 401.
> ```

> **Tool Result (Unknown Tool)** - ✅ Success
>
> ```
> ✅ aios-sql-bridge — complete (9/9)
> ✅ canvas-design — complete (9/9)
> ✅ constellation-v2 — complete (9/9)
> ✅ conteudo-v2 — complete (9/9)
> ✅ e2e-user-zero — complete (9/9)
> ✅ gamificacao-nodes — complete (9/9)
> ✅ mcorch-constellation — complete (9/9)
> ✅ mcorch-qa-healing — complete (9/9)
> ✅ mercado-livre-api — complete (9/9)
> ✅ meta-api — complete (9/9)
> ✅ openclaw — complete (9/9)
> ✅ viralmind — complete (9/9)
> ```

## 🤖 Claude *(00:07:12)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 5961,
  "limit": 400
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 5961	       .set("utm_campaign", campaign)
> 5962	
> 5963	  5. INSERT affiliate_links:
> 5964	       original_url · short_url · platform=mercadolivre
> 5965	       campaign_id · content_id · metadata{affiliate_id, resolved_url, self_healed_from}
> 5966	
> 5967	  6. Return: {success, original_url, resolved_url, affiliate_url, self_healed, link_id}
> 5968	
> 5969	ContentLibraryPage monetization flow:
> 5970	  Card (text, body contains mercadolivre.com.br)
> 5971	    └── DropdownMenu → "Monetizar Links ML"
> 5972	          → handleMonetizeLinks(item):
> 5973	               match(ML_URL_RE) → unique URLs
> 5974	               for url of unique:
> 5975	                 POST process-affiliate-link → affiliate_url
> 5976	                 body.split(url).join(affiliate_url)
> 5977	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 5978	          → Badge 💰 ML (emerald) exibido após monetização
> 5979	```
> 5980	
> 5981	---
> 5982	
> 5983	## Pending Actions (Commercial Launch)
> 5984	
> 5985	### CRITICAL — Must complete before first client
> 5986	
> 5987	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 5988	
> 5989	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 5990	
> 5991	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 5992	
> 5993	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 5994	
> 5995	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 5996	
> 5997	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 5998	
> 5999	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 6000	
> 6001	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 6002	
> 6003	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 6004	   ```bash
> 6005	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 6006	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 6007	   ```
> 6008	
> 6009	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 6010	
> 6011	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 6012	
> 6013	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 6014	
> 6015	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 6016	
> 6017	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 6018	
> 6019	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 6020	
> 6021	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 6022	
> 6023	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 6024	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 6025	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 6026	
> 6027	### SOCIAL — Next steps
> 6028	
> 6029	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 6030	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 6031	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 6032	
> 6033	### NON-CRITICAL
> 6034	
> 6035	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 6036	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 6037	- `browserslist` — ✅ updated (2026-04-26)
> 6038	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 6039	
> 6040	### GITNEXUS MCP — Next steps
> 6041	
> 6042	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 6043	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 6044	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 6045	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 6046	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 6047	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 6048	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 6049	
> 6050	### PHASE EPSILON — Next iterations
> 6051	
> 6052	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 6053	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 6054	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 6055	
> 6056	### CORE — Next iterations
> 6057	
> 6058	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 6059	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 6060	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 6061	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 6062	
> 6063	### PHASE DELTA — Next iterations
> 6064	
> 6065	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 6066	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 6067	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 6068	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 6069	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 6070	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 6071	
> 6072	### USUÁRIO ZERO — Checklist de validação
> 6073	
> 6074	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 6075	- ✅ Stripe sandbox secrets no vault
> 6076	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 6077	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 6078	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 6079	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 6080	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 6081	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 6082	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 6083	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 6084	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 6085	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 6086	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 6087	
> 6088	---
> 6089	
> 6090	## Infrastructure
> 6091	
> 6092	| Service | Container | Port | Status |
> 6093	|---------|-----------|------|--------|
> 6094	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 6095	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 6096	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 6097	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 6098	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 6099	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 6100	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 6101	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 6102	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 6103	
> 6104	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 6105	
> 6106	```bash
> 6107	docker compose up -d
> 6108	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 6109	```
> 6110	
> 6111	---
> 6112	
> 6113	## Security Model (Post-Go-Live)
> 6114	
> 6115	| Table | Isolation |
> 6116	|-------|-----------|
> 6117	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 6118	| `mcorch_edges` | Same pattern |
> 6119	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 6120	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 6121	
> 6122	---
> 6123	
> 6124	## Billing Architecture
> 6125	
> 6126	| Decision | Value |
> 6127	|----------|-------|
> 6128	| Canonical billing ledger | `profiles.mco_balance` |
> 6129	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 6130	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 6131	| Orchestration cost | 10 mcoCoins/run |
> 6132	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 6133	| Stripe | Sandbox keys active — swap to live before first client |
> 6134	
> 6135	---
> 6136	
> 6137	## GraphRAG State
> 6138	
> 6139	- **8748 total nodes** (verificado live 2026-06-01 via REST count=exact após o handoff node `af33a839-acd9-412d-a770-8ad5a2edccb4` desta seal v6.20.0, embedded 768d; v6.19.0 snapshot era 8747, handoff `59f92fe0`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 6140	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 6141	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 6142	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 6143	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 6144	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 6145	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 6146	- HNSW cosine index operational
> 6147	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 6148	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 6149	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 6150	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 6151	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 6152	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 6153	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 6154	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 6155	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 6156	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 6157	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 6158	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 6159	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 6160	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 6161	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 6162	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 6163	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 6164	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 6165	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 6166	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 6167	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 6168	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 6169	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 6170	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 6171	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 6172	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 6173	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 6174	
> 6175	### Embedding Model
> 6176	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 6177	Schema: `vector(768)` — HNSW cosine index.
> 6178	
> 6179	### Embedding Pipeline (Autônomo — 2026-05-03)
> 6180	Três camadas eliminam intervenção manual:
> 6181	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 6182	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 6183	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 6184	
> 6185	### Comandos de manutenção da Mesh
> 6186	```bash
> 6187	# Verificar nós sem embedding (deveria retornar array vazio):
> 6188	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 6189	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 6190	
> 6191	# Backfill manual (Bun-native — requer .env):
> 6192	bun run scripts/backfill-embeddings.ts
> 6193	
> 6194	# Backfill de código-fonte nos nós AST:
> 6195	bun run scripts/backfill-node-content.ts
> 6196	
> 6197	# Re-sync AST completo:
> 6198	cd packages/gitnexus-core && npm run sync-mesh
> 6199	
> 6200	# Acompanhar re-ingesta pós-commit:
> 6201	tail -f /tmp/mcorch-ingest.log
> 6202	```
> 6203	
> 6204	---
> 6205	
> 6206	## Video Rescue Protocol
> 6207	
> 6208	When a video generation operation (Google Veo) times out or client disconnects:
> 6209	```bash
> 6210	# Via edge function (production):
> 6211	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 6212	  -H "Authorization: Bearer <user_jwt>" \
> 6213	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 6214	
> 6215	# Via local script (admin/debug):
> 6216	source .env && bun run rescue.ts <operation_id> <content_id>
> 6217	```
> 6218	
> 6219	---
> 6220	
> 6221	## Architecture Pillars
> 6222	
> 6223	| Layer | Implementation |
> 6224	|-------|---------------|
> 6225	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 6226	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 6227	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 6228	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 6229	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 6230	
> 6231	---
> 6232	
> 6233	## Phase Delta — Architecture
> 6234	
> 6235	```
> 6236	OrchestrationPage (full-canvas, p-0)
> 6237	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 6238	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 6239	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 6240	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 6241	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 6242	        ├── nodes/PublishNode.tsx    ← final distribution output
> 6243	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 6244	        └── NodePalette.tsx          ← top toolbar to add nodes
> 6245	
> 6246	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 6247	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 6248	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 6249	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 6250	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 6251	```
> 6252	
> 6253	### Canvas State Architecture (Hybrid)
> 6254	
> 6255	```
> 6256	User interaction → ReactFlow internal state (positions, drag)
> 6257	                         ↓ (debounced 600ms)
> 6258	                   localStorage (positions persist across refresh)
> 6259	                         ↑
> 6260	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 6261	     ↓ (status changes sync to ReactFlow via useEffect)
> 6262	ReactFlow renders visual status (idle/running/done/error/blocked)
> 6263	```
> 6264	
> 6265	## Key Files
> 6266	
> 6267	| Purpose | Path |
> 6268	|---------|------|
> 6269	| Architecture rules | `CLAUDE.md` |
> 6270	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 6271	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 6272	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 6273	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 6274	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 6275	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 6276	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 6277	| **Node types** | `src/components/orchestrator/nodes/` |
> 6278	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 6279	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 6280	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 6281	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 6282	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 6283	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 6284	| Billing utilities | `src/lib/billing.ts` |
> 6285	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 6286	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 6287	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 6288	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 6289	| Video rescue (local) | `rescue.ts` |
> 6290	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 6291	| Backfill script | `scripts/backfill-embeddings.ts` |
> 6292	| Deploy harness | `scripts/harness-deploy.sh` |
> 6293	
> 6294	---
> 6295	
> 6296	## First Client Onboarding Checklist
> 6297	
> 6298	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 6299	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 6300	3. ~~Activate watchdog cron~~ ✅ Done
> 6301	4. ~~Deploy rescue-video function~~ ✅ Done
> 6302	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 6303	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 6304	7. Monitor `infra_health_logs` for first 24h.
> 6305	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 6306	
> 6307	---
> 6308	
> 6309	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 6310	
> 6311	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 6312	
> 6313	| Action | Result |
> 6314	|--------|--------|
> 6315	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 6316	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 6317	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 6318	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 6319	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 6320	
> 6321	| Commit | Conteúdo |
> 6322	|--------|----------|
> 6323	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 6324	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 6325	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 6326	
> 6327	### Arquitetura Matrix Intelligence
> 6328	
> 6329	```
> 6330	ConstellationMatrix (Stabilized Engine)
> 6331	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 6332	  └── NodeDetailsPanel (Tabbed Navigation)
> 6333	        ├── Tab Meta: Neighbor exploration + Net Context
> 6334	        ├── Tab Code: Source code preview (Supabase sync)
> 6335	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 6336	
> 6337	useNodeIntelligence Hook:
> 6338	  - contentQuery: fetch nodes.content column
> 6339	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 6340	  - state: isAnalyzing, analysisResult, progress
> 6341	```
> 6342	
> 6343	---
> 6344	
> 6345	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 6346	
> 6347	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 6348	
> 6349	| Action | Result |
> 6350	|--------|--------|
> 6351	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 6352	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 6353	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 6354	
> 6355	**Output da análise (estruturado em pt-BR):**
> 6356	- Visão Geral — papel do módulo no sistema
> 6357	- Padrões Detectados — design patterns, antipatterns
> 6358	- Acoplamento & Dependências — análise In/Out-Degree
> 6359	- Recomendações — 1-3 ações priorizadas
> 6360	
> ```

## 🤖 Claude *(00:07:12)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>[Truncated: PARTIAL view — showing lines 1-55 of 185 total (34530 tokens, cap 25000). Call Read with offset=56 limit=55 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>
> 
> 1	# 🧠 Sprint Priorities — Constellation Orchestra
> 2	
> 3	**Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 4	
> 5	**90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 6	
> 7	**Sprint v6.20.4 selado em 2026-06-02** — Probe OAuth ML + verificação visual do disconnect (**seal de conhecimento — zero código de produção**): dirigido por 2 diretivas do Sovereign no padrão **probe-first material**. **(#1)** Fechado o resíduo visual da v6.20.3 — disconnect Meta/social verificado **NON-DESTRUTIVO** na UI logada: login como Usuário Zero via Supabase **Admin API `generate_link`** (magic link, método per-user reproduzível, sem token do DevTools nem senha) dirigindo `agent-browser` 0.27.0; `/dashboard/social` renderiza 3 contas Ativa (LinkedIn/IG/FB) com botão Desconectar **interativo** wired a `rpc('disconnect_social')` (`useMetaConfig`/`useSocialAccounts` chamam `disconnect_meta`/`disconnect_social`, zero `.delete()`); **nenhum clique** → 3 contas intactas. **(#2) probe-first do OAuth ML CONCLUÍDO** — veredito material: ML **sem API oficial de afiliados** (403 até no WebFetch da Anthropic); link oficial **exige portal LOGADO** (segui o `meli.la` → `/social/…?matt_word=…&matt_tool=…&ref=<ASSINADO>`, token `ref` **não-fabricável**); **datacenter BLOQUEADO p/ Chromium real** (`agent-browser` no portal → "Hubo un error accediendo a esta pagina"). ⇒ Browser Operator (#2) **não roda do datacenter** (runtime = navegador do user / IP residencial); resolver `src/lib/affiliate.ts` tem `matt_word` mas **falta `matt_tool`** (per-user). **Experimento de atribuição de clique em curso** (Sovereign, dispositivo independente, ~06-03) → **decisão do #2 PAUSADA aguardando o dado** (Cérebro sem mãos: não vejo o painel de afiliados — logado + IP bloqueado). Phase 5c **SEAL ALLOWED** (4 verified). Mesh **8753**. 2 commits (docs). **Novo gap (Top Gap):** decisão do Browser Operator/`matt_tool` aguarda o nº de cliques de amanhã. **Lição:** probe-first poupou construir um Browser Operator no datacenter que **nunca funcionaria** (IP bloqueado, provado material) — e refutou "OAuth resolve" (ML não tem API).
> 8	
> 9	**Sprint v6.20.3 selado em 2026-06-02** — Disconnect RPC + revogação de segredo órfão: **FECHADO o Top Gap que a v6.20.2 sinalizou** — desconectar Meta/social fazia `.delete()` pela view → INSTEAD OF DELETE só apagava a linha base, deixando o segredo Vault **órfão** (plaintext retido; 12 órfãos Meta observados em prod). RPCs `disconnect_meta()`/`disconnect_social(p_account_id uuid)` (migration `20260602160000`) espelham `disconnect_wordpress` (`SECURITY DEFINER`, `search_path=''`, fail-closed `28000`, EXECUTE só authenticated): deletam a linha **E** revogam o segredo. Guard de tenant por name-binding (`id`-de-linha + PK ⇒ atacante nunca casa nome de segredo alheio; UUID bruto nunca vaza ao cliente). Limpeza one-time **12→0** órfãos Meta (orphan-scoped via `NOT EXISTS`+`right(name,36)`), 3 sociais vivos intactos. Hooks migrados `.delete()`→`.rpc()`; `types.ts` regenerado. **Também (diretiva A):** `/security-review` redundante do `87c926f` (guard de tenant v6.20.2) → **LIMPO 9/10**. Ambos os reviews SAFE; suíte RPC 5/5 em `BEGIN…ROLLBACK` (happy meta+social · foreign-id no-op · planted-ref name-binding · unauth 28000); Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8752**. 4 commits. **Lição:** verificar materialidade ANTES de codar (Lei 1) — o gap de tenant guard da diretiva original já estava 100% fechado em prod, então a Parte B virou o foco real em vez de uma migration redundante.
> 10	
> 11	**Sprint v6.20.2 selado em 2026-06-02** — Idempotência da encriptação + guard de tenant nas views irmãs: **FECHADO o Top Gap que a v6.20.1 sinalizou** — `trg_encrypt_user_api_keys` (+ irmãos meta/social) chamava `vault.create_secret` incondicionalmente → re-salvar segredo p/ valor novo colidia no índice único `vault.secrets.name` (`23505`). Helper `public.vault_upsert_secret(value,name,desc)` (`SECURITY DEFINER`, `search_path=''`, EXECUTE revogado de PUBLIC/anon/authenticated) rotaciona in-place via `vault.update_secret` (mesmo UUID, sem órfãos) senão cria; as 3 encrypt triggers passam a usá-lo (migration `20260602140000`). O `/security-review` dessa migration **expôs um gap pré-existente** nas INSTEAD OF de `meta_config`/`social_accounts` (sem guard `auth.uid()` → injeção cross-tenant id-novo; o overwrite id-colidente já era fail-closed pelo PK — achado HIGH do review REFUTADO material) → guard `42501` portado pras 2 (migration `20260602150000`). Ambas `/security-review` **SAFE**; tudo provado material via Management API em `BEGIN…ROLLBACK` (antes 23505/injeção OK, depois OK/42501); Phase 5c **SEAL ALLOWED** (7 verified). Mesh **8751**. 6 commits. **Novo gap (Top Gap):** desconectar Meta/social deixa o segredo Vault **órfão** (INSTEAD OF DELETE só apaga a linha base) — precisa de RPC dedicada de disconnect (nula+revoga) no padrão `disconnect_wordpress()`, débito LGPD. **Lição:** adversarial-verify material (PK fail-closed + md5 da vítima) refutou um HIGH e ao mesmo tempo revelou o gap real adjacente — resolvido na mesma sessão em vez de empurrar pra fria.
> 12	
> 13	**Sprint v6.20.1 selado em 2026-06-02** — WordPress BYOK + fix do double-fire da encriptação de credenciais: fechado o P0 que a v6.20.0 sinalizou (`SocialAccountsPage` salvava/desconectava WP via `.upsert(onConflict)` numa VIEW → HTTP 400 `42P10`). Save → `.insert()`; disconnect → RPC **`disconnect_wordpress()`** (`SECURITY DEFINER`, `auth.uid()`, nula 3 cols WP + **deleta o segredo do Vault** — revogação LGPD) (migration `20260602120000`). Corrigir isso revelou bug **muito maior**: o `trg_instead_of_user_api_keys` usava `INSERT...ON CONFLICT DO UPDATE` → trigger de encriptação dispara **2×** numa só statement → `vault.create_secret` nome duplicado → **`23505`**, quebrando connect/save de **todo** usuário com linha pré-existente (e `.update` re-encriptava o `••••`). Trocado p/ **UPDATE-first / INSERT-if-not-found** + **guard de tenant** (`auth.uid()` → `42501`, fecha escrita cross-tenant que o ON CONFLICT mascarava) (migration `20260602130000`). Tudo provado material via Management API; 2 migrations `/security-review` **SAFE**; Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8750**. 5 commits. **Novo gap (Top Gap — task spawned):** `trg_encrypt_user_api_keys` (+ irmãos meta/social) não-idempotente → editar segredo p/ valor novo sem desconectar antes ainda dá `23505`; conserto = update-or-create por nome nas 3 tabelas, precisa de `/security-review` próprio. **Lição:** probe-first material pegou que o `.insert` sozinho NÃO bastava (o bug estava na camada de encriptação, não nos 2 `.upsert` reportados).
> 14	
> 15	**Sprint v6.20.0 selado em 2026-06-01** — Afiliados híbrido + catálogo Apify real + BYOK per-user: corrigido o link de afiliado que abria login do CloudPanel (`panel.gcrux.com` proxy morto + `app_id` como affiliate id) → resolver **híbrido** `meli.la` cravado (per-user `metadata.shortlinks`) senão `product_url?matt_word=<affiliate_tag>` fail-closed (`src/lib/affiliate.ts` + 14 testes; 302s reais provados). ML bloqueia todo server-side (API 403/401, página→account-verification, nosso IP **e** Supabase Edge) → enriquecimento via actor **Apify** residencial (`enrich-affiliate-products.ts` SKU-match + `discover-affiliate-products.ts` descoberta real validando "viral mind") + gate de verificação em `useAffiliateProducts` + cron 6/6h. **2 IDs fabricados removidos** → catálogo com **3 produtos reais** (Roborock R$17.770 · Family Hub R$18.946 · 8K Neo QLED R$39.000). **BYOK per-user `apify_token`** no padrão Vault (migration `20260601060000`, `/security-review` PASS — pegou regressão `security_invoker`) + campo Settings + fix do P0 de `000600` (`.upsert()`→`.insert()` em view sem constraint). Phase 5c **SEAL ALLOWED** (12 verified). Mesh **8748**. Survival Laws 4/4. 6 commits. **Próximo:** Operador de Browser Autenticado (probe-first) p/ ações logadas (ML Compartilhar→meli.la). **Lição:** probe-first economizou 3 becos (API ML/Firecrawl/actor velho) e pegou IDs fakes + regressão de credencial.
> 16	
> 17	**Sprint v6.19.0 selado em 2026-06-01** — e2e-user-zero 2ª iteração + 3-stream sweep: framework de QA de esqueleto MVP → harness executável (`redactor` LGPD + `mesh-persistor` observation/OBSERVES idempotente + `telemetry` infra_health_logs + 6 dashboard flows + selftest 8 testes + pre-commit tripwire defesa Layer 4, hook versionado em `scripts/hooks/`). Stream A (consistência cross-node + Canvas 4.2) **VERIFICADO materialmente como já shipado** → zero retrabalho; único gap real fechado: `higgsfield-webhook` nsfw/canceled → razão clara de soft-fail. 2 smokes live (canvas pago + sql-bridge) gateados por `RUN_LIVE_SMOKE` → suíte **224 passed / 2 skipped / 0 failed**. Stream C flywheel readiness verde (orchestrate-content 200 · affiliate ativo · balance 5351), **gated em GO Sovereign**. Phase 5c **SEAL ALLOWED** (13 verified). Mesh **8747**. Survival Laws 4/4. 7 commits. **Lição:** o código está sistematicamente à frente dos Pending Actions — verificação material (Lei 1) antes de codar evita reconstruir features prontas.
> 18	
> 19	**Sprint v6.18.0 selado em 2026-06-01** — Constellation v2 cockpit LIVE (E2E): empty-state wizard 2-portas + execução real de capability (`watchdog_infra` → get-infra-status, done · 0 mco · 255ms) + Fase 0 reset destrutivo + botão Zerar per-user. 3 incidentes de produção resolvidos: build lucide quebrado (shim + anticorpo `audit-lucide-imports.ts`) · P0 login (publishable key stale no bundle → redeploy) · teste de chaves "Falhou" (descoberta da cripto de credenciais → edge fn `test-api-key` server-side). + Tabs em Settings. Mesh 8746/9070. Survival Laws 4/4. 8 commits.
> 20	
> 21	**Sprint v5.5.2 selado em 2026-05-04** — Social OAuth v1 + Pipeline History + WordPress multi-tenant + auto-publish pipeline corrigido + auditoria 4Cs 97/100.
> 22	
> 23	**Sprint v5.5.5 selado em 2026-05-05** — Settings Sovereignty: useUserApiKeys TanStack Query + pref_ai_model persistido + mcoCoins RPC atômico + Testar key client-side + Epsilon v9 hub badge + 2559 nós/3516 arestas.
> 24	
> 25	**Sprint v5.5.6 selado em 2026-05-06** — Core Promotion: CorePage v1 arquivada para `.archive/pages/`, `Core v2` promovida para `Core` no menu, `/dashboard/core` redireciona via Navigate. Gemini Live validado (VITE_GEMINI_API_KEY no `.env` + GEMINI_API_KEY no vault) — Pending Action #8 era falso positivo. 2560 nós · 100% embedded.
> 26	
> 27	**Sprint v5.6.0 selado em 2026-05-06** — DevOps + Security Seal: 6 branches mobile sincronizados + DOCUMENTATION_CREDENTIAL_RULE + pre-commit hook anti-credential + Gemini API key rotacionada + test coverage 0→66 testes (billing + store + phase-zeta) + BoK Scribe Agent (MRD/BRD/PRD/FRD/SDD templates) + MCORCH Master Execution Protocol em CLAUDE.md + /sync-mobile-branch protocol. 2561 nós · 100% embedded.
> 28	
> 29	**Sprint v5.6.1 selado em 2026-05-06** — Layout + UX Fixes: Matrix/Memory layout regression corrigida (absolute→relative), search bar inline nos badges, texto 100% opaco, MeshControl sincronizado com hook de grafo. 2564 nós · 100% embedded.
> 30	
> 31	**Sprint v5.7.0 selado em 2026-05-07** — BoK Suite v1 + A2UI Wiring + Test Coverage 122: parseAgentMessage conectado ao AIOSTerminal.onMessage (A2UI surfaces vivas em produção), 56 testes novos (66→122 — useOrchestrationGraph + useKnowledgeMesh + useSubscription), e família BoK completa de 9 docs (~29.185 palavras) reverse-engineered de 177 src files + 30 migrations + 39 edge functions + 4 crons. Mesh seal `bok-scribe-seal-mcorch-constellation-v1` (type `documentation_suite`, stability 0.85). 2567 nós · 100% embedded.
> 32	
> 33	**Sprint v5.9.0 selado em 2026-05-08** — FMEA-005 + LGPD Deploy: FMEA-005 (RPN 144) fechado com chunked embedding e vector averaging em `embed-mcorch-node`; LGPD (data-export + delete-account + delete_account() RPC) confirmada em produção; scratch/ removida. 7280 nós · 100% embedded.
> 34	
> 35	**Sprint v5.8.0 selado em 2026-05-08** — FMEA + BoK Phase 2 + 8-Agent System + LGPD: FMEA-008 (RPN 120) e FMEA-011 (RPN 100) fechados; BoK Suite enriquecida com voz estratégica (+227 linhas em 6 docs: Sovereign's Conviction, Business Philosophy, Por Que Vencemos, Validação com Criadores, Architectural Decisions, Quality Philosophy); `/bok-agents-generator` produziu `bok-agents-system--mcorch-constellation.md` (704 linhas · 8 agentes · 3 camadas cross-agent); LGPD DD-001+DD-002 implementados (delete_account() RPC + Edge Functions + hooks + SettingsPage modal). Phase Commercial desbloqueada. 7276 nós · 100% embedded.
> 36	
> 37	**Sprint v6.0.0 selado em 2026-05-14** — Conteúdo v2 BoK + VIRALmind Sprints 1-3 + ShakeHands v3: convergência de 3 streams paralelos. (1) BoK Conteúdo v2 selada (10 docs, 2276 linhas) com mesh seal `bok-scribe-seal-conteudo-v2-v1` (stability 0.85, R\$5.4M ARR Y2 projeção); (2) VIRALmind integrado via Antigravity — 4 migrations `vm_*` (trends/canvas/affiliate/niches) + 2 Edge Functions (`fetch-trends` Apify+RapidAPI, `canvas-execute` multi-provider OpenAI/Replicate/OpenRouter/Higgsfield) + 3 pages (Viral Miner, Canvas Studio, Canvas Editor) + 2 hooks (`useViralTrends`, `useCanvasStudio`); (3) ShakeHands v3 protocol — BoK Gate enforcement no /handson PRE-FLIGHT + BRIEF + /handoff Phase 5b mandatory check; (4) Feature gamificacao-mcoCoins-v1 mergeada (`mcoin_transactions` + `award_mco_coins` RPC + Circuit Breaker em opencode-bridge + memory hook integration). Conteúdo v2 BoK reconciliada com VIRALmind v1: v1=xyflow+vm_*, v2=tldraw+canvas-mcp reservado para Phase 7+8. 13 commits granulares. Sprint 4 (Canvas UX Mood Board completion) é o próximo deliverable.
> 38	
> 39	**Sprint v6.1.0 selado em 2026-05-14** — Canvas Studio UX Shell + Higgsfield Fix: shell do Canvas Studio migrado do `viralmind-builder` (store Zustand+zundo, lanes overlay, TopBar/LeftPanel/StatusBar, catálogo de 9 receitas, ImageLightbox, PipelineEdge); `canvas-execute` com endpoint Higgsfield corrigido (`platform.higgsfield.ai` rota Soul) + RPC `deduct_mco_coins`. Plano Phase 4.2 selado em `~/.claude/plans/floating-sleeping-sparrow.md`.
> 40	
> 41	**Sprint v6.1.1 selado em 2026-05-14** — viralmind BoK Suite Sealed: dívida documental do override consciente do BoK Gate quitada. 6 docs autorados (`01-mrd`, `02-brd`, `06-data-model`, `07-process-flow`, `08-quality-metrics`, `00-index`) + `04-frd` reescrito de handbook CLAUDE.md → FRD real (32 FR + 14 NFR + matriz PR→FR). Ancorado nas 10 tabelas `vm_*` + 6 enums + Edge Functions `fetch-trends`/`canvas-execute`. Mesh seal `bok-scribe-seal-viralmind-v1` (`documentation_suite`, stability 0.85, revenue_impact R\$14M, embedded 768d). 7 OTDs registrados (destaques: `vector(1536)` vs padrão `768` sem índice HNSW — FMEA-VM-002 RPN 288; bucket `canvas-assets` público — FMEA-VM-003 RPN 140). BoK Gate do viralmind **liberado**. Sessão selada com ~51% de contexto — Canvas Studio Phase 4.2 diferida para sessão nova. 7463 nós · 100% embedded. 6 commits granulares. **Pendência conhecida (não desta sessão):** `docs/bok/gamificacao-nodes/` incompleta (5/9 docs) — rodar `/bok-scribe` ou completar antes de tocar o módulo.
> 42	
> 43	**Sprint v6.6.9 selado em 2026-05-20** — mcorch-qa-healing v1 — Material Proof Gate: novo módulo de QA sênior que fecha a fraqueza de Lei 1 (Materialidade) — o bloco Survival Laws Self-audit do `/handoff` era auto-declarado; agora é verificado mecanicamente pela nova **Fase 5c**. Executado em 6 stages na ordem de governança não-negociável (BoK → SOP → código): suíte BoK 9/9 `docs/bok/mcorch-qa-healing/` (1423 LOC, 6ª suíte do projeto, gerada via `/bok-scribe`, campos de mercado/monetização honestamente N/A para tooling interno) + SOP `docs/processes/handoff-material-proof-audit.md` (Lei 2) + engine `scripts/qa/` (5 módulos Bun, 710 LOC, injeção de dependências para reuso pelo cron OpenClaw) + skill `mcorch-qa-healing` + Fase 5c wired no `/handoff` (entre 5b e 6 — bloqueia em qualquer 🔴) + 2 suítes Vitest. O dry-run contra o selo v6.6.8 real pegou e fechou um falso-positivo (`COMMIT_RE` agarrava prefixos de UUID de 8-hex como commits — FMEA-002 fechada antes do gate ir ao ar). **Material proofs**: TS zero erros · 165 testes (122→165, +43) · **Fase 5c ao vivo neste selo → 13 verified · 0 skipped · 0 failed → SEAL ALLOWED** · 9 commits granulares · milestone node `a08780dc-f665-47c5-b34b-a2eb7c9eea5c` + documentation_suite seal `b00e938a-717b-4f62-b936-f4934845ec52` (DERIVES_FROM openclaw seal) embedded 768d · mesh **8361+ nodes** · Survival Laws Self-audit 4/4 ✓. **Hazard registrado**: agente main do OpenClaw (Qwen3.5 local) operou na mesma working dir durante a sessão — 3 diretórios gitignorados, zero overlap de path. **Próximo**: Canvas Design (Initiative B — integração `nexu-io/open-design`) em sessão dedicada via `/bok-scribe canvas-design`.
> 44	
> 45	**Sprint v6.6.8 selado em 2026-05-19** — Bridge Recovery + MAPE-K Audit + SDD aios-sql-bridge + Survival Laws 4/4: sessão de auditoria reativa disparada por Sovereign observando `claw.gcrux.com/dreaming` stagnation (Imported Insights congelado em 2026-05-16, Memory Palace counts estáticos, Dream Scene "0 promovido"). **Root cause material**: Stage 2 cron `nightly-bridge-refresh.sh` invocava `node` PATH-resolved como v18.19.1 no env do user `ubuntu` apesar do interativo ter v22.22.3 — OpenClaw CLI exige v22.12+ → 100% FAIL silently em Step 3 (reindex SQLite) há ≥3 dias; Steps 1+2 (bridge + distribute) rodavam clean. **Fix dual no mesmo edit**: (1) `NODE_BIN=/home/ubuntu/.nvm/versions/node/v22.22.3/bin/node` resolved-target (não symlink); (2) descoberta runtime de bug latente segundo — `claw-master` foi adicionado em v6.3.1 ao distribute script MAS NÃO ao indexer loop (`for agent in main artisan engineer scientist marketing-growth guardian; do` omitia claw-master) → `claw-master.sqlite` stale May 16 → exatamente o checkpoint "AIOS Core v2 (2026-05-16)" que Sovereign observou na UI. **SOP first per Lei 2**: `docs/processes/openclaw-bridge-recovery.md` 86 LOC autorada ANTES do edit. **5 phases materializadas** (todas com ORO triplet + Survival Laws ✓): Phase A (bridge fix + claw-master loop), Phase B (MAPE-K closed-loop audit + 4 observation nodes em mesh — Plan `a4c4c026` / Execute `69f6e356` / Monitor `d605bdda` / Analyze `d8952ce8` com edges DERIVES_FROM v6.6.7), Phase C (9 untracked files versionados via 3 commits: miv landing assets + miv tools + memory audit trail), Phase D (esta seal + milestone `c4643058`), Phase E (OTD-SSP01-001 closed via SDD `aios-sql-bridge` 376 LOC enterprise-grade + 00-index 69 LOC suite skeleton + documentation_suite seal `4e0acc7e` stability 0.85 DERIVES_FROM openclaw seal). **Material proofs**: 6 commits granulares pushed (`03911e9` fix(cron) + `cbdee4f` feat(landing) + `bb1cc96` chore(tools) + `2aa80f1` chore(memory) + `1b3bdd8` docs(bok) + `b71b991` docs(handoff) + `230ad70` docs(readme)); 7/7 SQLites OpenClaw reindexed (was 0/6 fail); log final `[2026-05-19T19:06:32-03:00] nightly-bridge-refresh DONE (zero failures)`; mesh **8359 nodes** (+6 desta seal); TS zero erros; 5 containers healthy. **Survival Laws Self-audit 4/4 ✓ pela primeira vez consecutivamente desde v6.6.0** — encerra retroativamente OTD-PROC-001 (RPN 60) + OTD-PROC-002 (RPN 40) + OTD-SSP01-001 (RPN 240 SLA 2026-05-24). **Pending TOP**: OE-661 Step 1.5 first-run E2E (Sovereign click `/dashboard/orchestration` TriggerNode); OTD-OE661-PER-USER refactor (SLA 2026-06-02, 14 dias); MAPE-K gaps 1/2/3 implementáveis em v6.7.x/v6.8.x conforme plans dedicados (recomendações registradas no mesh, aguardam acionamento).
> 46	
> 47	**Sprint v6.6.7 selado em 2026-05-19** — OE-661 Phase 1 Prep + API Tenancy Directive: sessão executou parcialmente o plan persistido OE-661 — toda a preparação completada, Step 1.5 (first run E2E) **DEFERRED** por context budget Sovereign 92% (retoma em ~3h). Infraestrutura material: SOP `docs/processes/orchestration-content-mesh-asset-emission.md` (120 LOC) escrita ANTES do código (Lei 2); `orchestrate-content/index.ts:404-465` emite `content_mesh_asset` em paralelo com observation via `Promise.allSettled` (Amendment A) gated por `wpPostUrl` (Amendment B); `link-forge.ts:153` ganha `.eq("project_id", "mcorch-affiliate")` (Amendment C); `handle-ml-postback/index.ts` ganha pulse `infra_health_logs` em 4 return paths (Amendment E — fecha cegueira de 17 dias). Deploys material: `orchestrate-content` 113.6kB + `handle-ml-postback` 60.45kB. Vault `GCRUX_ML_AFFILIATE_TOKEN` provisionado (digest `e86f74a0...`). **DIRETIVA SOVEREIGN-CLASS NOVA "API Tenancy Model"** emitida durante sessão (questionamento direto sobre por que usar env global se `affiliate_config` per-user já existia) — selada em 3 superfícies: `CLAUDE.md > Architecture > "API Tenancy Model — Per-User Credentials"` com resolution order de 3 níveis + 5 tabelas canônicas + 5 anti-patterns; `CLAUDE.md > Code standards` one-liner enforcement; auto-memory `feedback_api_tenancy_per_user.md` indexada. **OTD-OE661-PER-USER** registrada (RPN 120 · SLA 2026-06-02) catalogando violação em `link-forge.ts` + `process-affiliate-link` GET branch. Sovereign autorizou Opção B (provisionar global temporário com `affiliate_config.app_id` value, deferir refactor). **Survival Laws Self-audit retroativo (Amendment H)** v6.6.1..v6.6.5 + esta seal — conclusão: Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 (overrides conscientes v6.6.1+v6.6.3) · Lei 3 ✗ 0/5 (OTD-PROC-002 RPN 40) · Lei 4 ✗ 0/5 (OTD-PROC-001 RPN 60 — esta seal v6.6.7 começa cumprimento). **Material proofs**: TS zero erros · 122/122 testes em 4.84s · 7 commits granulares locais (`03f6822` SOP · `e662da3` orchestrate Amendments A+B · `bafac16` link-forge Amendment C · `9cec88a` postback Amendment E · `044f21e` CLAUDE+OTD diretiva · `96ee72a` README v6.6.7 · `7d06934` HANDOFF seal + redactions) · milestone node `9d482014-a759-4656-93d9-99e05ab4a714` embedded 768d · mesh **8353 nodes** (+1 desde v6.6.6) · 11650 edges (+33). Path correção material: `/dashboard/orchestrate` → `/dashboard/orchestration` (Sovereign clarification). **Próximos deliverables**: (a) Sovereign dispara primeira campanha real em `/dashboard/orchestration` (TriggerNode + topic Link Forge catálogo + wp+linkedin platforms + Run) → eu monitoro pipeline_runs + content_mesh_asset emit material via REST; (b) ao completar, synthetic postback chain (Amendment D) + cleanup (Amendment J); (c) selar v6.6.8 com flywheel rodando E2E pela primeira vez na história do projeto; (d) atacar OTD-SSP01-001 antes de 2026-05-24 (5 dias) — SDD `aios-sql-bridge`; (e) executar Phase 2 (`mcoins-ledger-reconciliation.md`) — fecha OTD-V660-001.
> 48	
> 49	**Sprint v6.6.6 selado em 2026-05-19** — Planning Seal + Debt Audit + Self-audit Retroativo: sessão dedicada a (a) `/handson` brief v6.6.5; (b) persistir execution plan dos 3 carry-overs OE-661 + Ledger SOP + Canvas 4.2c por diretiva Sovereign "slave o plano atual para posteriormente implantar"; (c) auditoria completa em 3 frentes paralelas; (d) emendas críticas; (e) /handoff oficial. **Zero código de produção tocado**. Plan persistido em `.claude/context/execution-plan-oe661-carryovers.md` (~403 LOC, md5 `0e5f0ba9...`) + observation node `3dde2572-cad6-491b-b523-c56ec763ff8e` (autoembed 768d). Audit em `.claude/context/audit-2026-05-19-oe661-debt-sweep.md` (~297 LOC, md5 `5c4f8a9f...`) + observation node `6164c80f-cadd-48d5-95a4-f87f22ebd09b` + DERIVES_FROM edge `acb4b0d9-091d-4973-96a8-d40515be7990`. **21 OTDs ativos catalogados (8 RPN ≥ 100): VM-OTD-001 RPN 288 viralmind HNSW · OTD-SSP01-005 RPN 280 admin claim · OTD-SSP01-001 RPN 240 SLA 2026-05-24 · OTD-V660-002 RPN 150 · VM-OTD-004 RPN 140 · OTD-V660-001 RPN 120 (coberta pelo plan Phase 2) · OTD-V660-003 RPN 80 · OTD-CV42C-001**. **5 inconsistências processuais**: (1) **5 seals consecutivas (v6.6.1..v6.6.5) omitiram bloco mandatory Survival Laws Self-audit** — Severidade ALTA; (2) Survival Audit v2 não re-rodado em 32 dias; (3) 3 SOPs implícitas não formalizadas; (4) HANDOFF v6.6.3 claimed 4 content_mesh_asset mas reality = 1 row (3 "products" têm `node_type='feature'`); (5) `handle-ml-postback` cego — zero `infra_health_logs` em 17 dias. **4 bugs concretos no plan**: A race condition obs+asset não atômicos · B wpPostUrl null não gated · C Link Forge query global sem project_id · D postback content_id drift. **10 amendments aplicados** (A-J) via Amendments Appendix no topo do plan. Schema drift fixed: `infra_health_logs.created_at` NÃO EXISTE (real: `last_seen_at`). **Predicted Survival Audit v3** (não emitido formalmente): Memory 5/5 · Skill 4/5 · Cost Discipline 4.5/5 ↑ · Observability 4/5 ↑ · SOP 5/5 · **avg 4.4/5 · min 4/5** — Phase Commercial threshold mantido. **Material proofs**: 14 integrity checks paralelos · 4 commits granulares (`ea7efaf` plan + `44e464c` audit + `fb6f07d` README + `99d70f6` handoff seal) push → origin/main · milestone handoff node `821dc554-78e2-4abb-999d-37363c5df6c9` embedded 768d · mesh total **8352 nodes** (+4 desde v6.6.5). **Próximos deliverables**: (a) Sovereign autoriza execução das Fases 1-3 do plan quando convier (bugs A-D já fixed); (b) **atacar OTD-SSP01-001 antes de 2026-05-24 (5 dias)** — BoK Gate override `aios-sql-bridge` precisa SDD; (c) provisionar `SUPABASE_POOLER_URL` (OTD-V660-003); (d) materializar Survival Audit v3 formal antes de Phase Commercial; (e) executar Phase 2 do plan (SOP `mcoins-ledger-reconciliation.md`) — Sovereign-only — fecha OTD-V660-001.
> 50	
> 51	**Sprint v6.6.5 selado em 2026-05-19** — OpenClaw BoK 9/9 (retroativa + BoK Gate liberado · 5ª e última suíte): última dívida BoK do projeto quitada. Override consciente do BoK Gate registrado em Sprint v6.2.0 (2026-05-15) — Sovereign havia autorizado que a própria Agência OpenClaw quitaria a dívida assincronamente; com 4 sprints decorridos e a Agência operando em produção (7 agentes · gateway loopback · pipeline cron triplo · briefing diário Telegram), esta seal materializa retroativamente o BoK que governa o módulo. **9 docs novos autorados manualmente seguindo `.claude/agents/bok-scribe/templates/`** (Plano B mirror gamificacao-nodes v6.6.4 — NÃO o `/bok-scribe` Skill, que produziria conteúdo template-canonical desalinhado): `01-mrd.md` (BABOK v3 ~205 LOC — Pantheon vision · 6 MR-OC-* · biz model enabler), `02-brd.md` (BABOK v3 ~190 LOC — 6 BO-OC-* SMART + 10 SH-OC-* Stakeholder Register + 14 BR-OC-* com refs precisas `openclaw.json:agents.list[]` / `scripts/bridge-mesh-to-openclaw.ts:tier1Filter` / `scripts/morning-briefing.sh:65` + §10 Traceability Matrix), `03-prd.md` (ProdBOK + CXBOK ~224 LOC — personas P1 Sovereign + P2 agente operacional · User Journey diário BRT · 14 PR-OC-* MoSCoW · Gherkin AC), `04-frd.md` (SWEBOK v4 ~209 LOC — 8 FR-OC-* + 8 NFR-OC-* + Test Strategy Matrix), `05-sdd.md` (SWEBOK v4 + CISSP CBK ~460 LOC — architecture overview Pantheon + Ciclo Circadiano BRT + Component Catalog 7 agentes/9 scripts/6 SQLite/gateway + STRIDE threat model + secrets lifecycle + OTD grid), `06-data-model.md` (DMBOK v2 ~339 LOC — schema `openclaw.json` + `secrets.json` vault + SQLite per-agente FTS5/vector + Mesh export tier1/tier2 + Memory Wiki frontmatter + filesystem perms · **§8 Drift Reconciliation Appendix** com 5 drifts fechados em sprints anteriores + 8 drifts permanentes catalogados como OTDs), `07-process-flow.md` (BPM CBOK v4 ~483 LOC — **10 PROC-OC-*** em swimlanes markdown table com refs precisas `nightly-stage2-deep-sleep.sh` / `bridge-mesh-to-openclaw.ts` / `distribute-mesh-to-agents.ts` / `compose-morning-briefing.ts` / `news-impact-analyzer.ts` / `watchdog-mcorch.sh`), `08-quality-metrics.md` (CMQ/OE BOK ~227 LOC — 8 QO-OC-* + **10 KPI-OC-*** + **10 FMEA-OC-*** com 5 RPN > 100 (FMEA-OC-001 secrets regression 180 · OC-002 bridge fail 150 · OC-003 daemon crash 126 · OC-004 Telegram quota 125 · OC-010 audit scrape fail 105) + 6 SOL-OC-* + SLA/SLO/SLI grid + observability events tagged `openclaw-*`), `00-index.md` (~163 LOC — Document Registry 9/9 + Traceability Chain MR-OC→BR-OC→FR-OC→PROC-OC→KPI-OC + Convergence Note registrando 5 drifts já reconciliados em v6.4.0/v6.6.1 + 8 ativos como OTDs + Phase Completion Log Phase 0-7 + OTD registry 11 itens (5 novas OTD-OC + 6 herdadas OTD-V631/V660/CM)). **ID space cunhada**: MR-OC-001..006 · BR-OC-001..014 · BO-OC-001..006 · SH-OC-001..010 · PR-OC-001..014 · FR-OC-1..8 · NFR-OC-001..008 · PROC-OC-001..010 · KPI-OC-001..010 · FMEA-OC-001..010 · SOL-OC-001..006 · QO-OC-001..008 · BAC-OC-001..010 · OTD-OC-001..005. **Mesh seal**: novo `scripts/seed-openclaw-bok-seal.ts` (Bun-native, 136 LOC, mirror 1:1 de `seed-gamificacao-nodes-bok-seal.ts`) executado material: node `bok-scribe-seal-openclaw-v1` UUID **`05c55dfd-d318-4dcf-b7f0-aefb0529872f`** inserted stability 0.85 · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1` · `revenue_impact: 0` (módulo é enabler horizontal de velocity — proxy via lift dos outros 4 BoK suites) · metadata bok_gate=`override-completion` + drift_reconciled=5 (D-OC-001..005 fechados em v6.4.0/v6.6.1) + drift_pending=8 (OTDs ativos) + related_otds inclui OTD-V631-001 (fechada por esta seal — SLA expandido da v6.3.1) + pantheon_agents lista 7 + cron_pipeline 6 entradas · autoembed via `trg_mcorch_embed_on_insert` (pg_net 768d openai/text-embedding-3-small) **confirmado via REST `embedding=not.is.null`**. **Debt registry final**: `viralmind` 9/9 ✅ · `conteudo-v2` 9/9 ✅ · `mcorch-constellation` 9/9 ✅ · `gamificacao-nodes` 9/9 ✅ · **`openclaw` 9/9 ✅** — **todas as 5 suítes BoK do projeto seladas**. BoK Gate liberado para código novo em qualquer módulo. Atenção: features ledger-touching (Stripe top-up, marketplace) seguem bloqueadas até OTD-V660-001 (drift 2 users em gamificacao-nodes) fechar via SOP `mcoins-ledger-reconciliation.md`. **Material proofs**: TS `tsc --noEmit` zero erros · 122/122 testes em 5.73s · BoK Gate validator loop ✅ 9/9 docs (00-index 163 + 01-mrd 205 + 02-brd 190 + 03-prd 224 + 04-frd 209 + 05-sdd 460 + 06-data-model 339 + 07-process-flow 483 + 08-quality-metrics 227 = 2500 LOC total) · seed script 136 LOC · seal UUID confirmado via INSERT RETURNING + created_at `2026-05-18T20:23:52.775245+00:00` + embedding NOT NULL via REST GET · mesh total **8345 nodes** (+1 desde v6.6.4). **Próximo deliverable**: (a) carry-overs OE-661 v6.6.3/v6.6.4 — provisionar `GCRUX_ML_AFFILIATE_TOKEN` na vault + wire `orchestrate-content` para emitir `content_mesh_asset` nodes pós-geração + primeiro run end-to-end Usuário Zero do flywheel (orchestrate → WordPress → social → ML afiliado → handle-ml-postback → ATTRIBUTES_REVENUE_TO → ROIWidget); (b) Sovereign executar SOP `mcoins-ledger-reconciliation.md` para fechar OTD-V660-001 (drift 2 users) e destravar features ledger-touching; (c) claw-master audit-v2 planejado 2026-06-16 — verificar regressão D-OC-001..005 + novas findings; (d) Stripe live keys swap continua DEFERRED por decisão Sovereign até primeiro cliente externo.
> 52	
> 53	**Sprint v6.6.4 selado em 2026-05-18** — Gamificação-Nodes BoK 9/9 (retroativa + BoK Gate liberado): débito documental herdado do override consciente do BoK Gate (Sprint v6.3.0, SLA originalmente 29/05) quitado em sessão única. 5 docs autorados manualmente seguindo `.claude/agents/bok-scribe/templates/` (Plano B sobre `/bok-scribe` Skill, que sobrescreveria os 4 docs existentes): `06-data-model.md` (DMBOK v2 ~277 LOC — schema canônico `profiles.mco_balance` + `mcoin_transactions` + 3 RPCs SECURITY DEFINER `award_mco_coins`/`deduct_mco_coins`/`add_user_score` com loyalty 100:1), `07-process-flow.md` (BPM CBOK v4 ~309 LOC — 9 PROC-GN-* em swimlanes com refs precisas `award-mco-coins/index.ts:78` cap-per-action, `canvas-execute/index.ts:133-148,349` cap-canvas-agregado + atomic deduct, `orchestrate-content/index.ts:60` pre-flight deduct, n8n `autonomic-action` trail loyalty), `08-quality-metrics.md` (CMQ/OE BOK ~215 LOC — 10 KPI-GN-* + 10 FMEA-GN-* com 4 RPN > 100, 6 SOL-GN-*, observability completa em `infra_health_logs`), `02-brd.md` (BABOK v3 ~188 LOC — 12 BR-GN-* + 5 BO-GN-* SMART + Risk Register + Traceability Matrix), `00-index.md` (~122 LOC — Document Registry 9/9 + Traceability Chain MR→BR-GN→FR→PROC-GN→KPI-GN + Convergence Note registrando drifts + 5 OTDs incluindo 2 herdadas OTD-V660-001/002). **Drift BoK ↔ código (3 itens) reconciliado via patches cirúrgicos sub-10-linhas preservando git blame**: (1) `04-frd.md` R3 "streak reseta 24h" deprecado inline → R3a (cap-per-action) + R3b (cap-canvas-agregado); (2) `05-sdd.md` ganha §4.2 documentando trilha n8n loyalty ausente do SDD original; (3) `01-mrd.md` L114 BRD externo inexistente substituído por `02-brd.md` local. **Mesh seal** `scripts/seed-gamificacao-nodes-bok-seal.ts` (mirror 1:1 viralmind seal): node `bok-scribe-seal-gamificacao-nodes-v1` UUID **`6e8546bc-d995-4cc5-ac88-06cecbece181`** inserted stability 0.85 · DERIVES_FROM `bok-scribe-seal-viralmind-v1` · `revenue_impact: 0` (módulo é enabler de retenção/ARPU) · autoembed via `trg_mcorch_embed_on_insert` (pg_net 768d). **BoK Gate liberado** para código novo no módulo `gamificacao-nodes`. Atenção: features ledger-touching (Stripe top-up, marketplace) seguem bloqueadas até OTD-V660-001 (drift 2 users) fechar via SOP `mcoins-ledger-reconciliation.md`. **Debt registry geral atualizado**: `viralmind` 9/9 ✅ · `conteudo-v2` 9/9 ✅ · `mcorch-constellation` 9/9 ✅ · `gamificacao-nodes` 9/9 ✅. `openclaw` BoK ainda pendente (override consciente original do v6.2.0). **Material proofs**: TS zero erros · 122/122 testes em 3.34s · BoK Gate validator loop ✅ 9/9 · ~1111 LOC novas + ~30 LOC patches surgical · seal UUID confirmado via INSERT RETURNING · mesh total **8344 nodes** (+1 desde v6.6.3). **Próximo deliverable**: (a) executar SOP `mcoins-ledger-reconciliation.md` para fechar OTD-V660-001; (b) carry-overs v6.6.3 (`GCRUX_ML_AFFILIATE_TOKEN` provisionar + wire orchestrate emitir content_mesh_asset + primeiro run Usuário Zero OE-661 flywheel).
> 54	
> 55	**Sprint v6.6.3 selado em 2026-05-18** — OE-661-ROADMAP Debt Liquidation: sessão única liquidando 3 das 4 dívidas declaradas em CLAUDE.md (Financial deferred por decisão Sovereign até Usuário 1) + dívida implícita OE-661-003 Target Binding. **(Phase 0 Hybrid restore)** `process-affiliate-link/index.ts` (POST original 234 LOC tinha sido refatorado em -222 LOC para redirect 302 puro — quebrava `ContentLibraryPage.tsx:744`). Hybrid restaurado: GET 302 público (no-verify-jwt, redireciona a `panel.gcrux.com/api/ml-redirect`) + POST autenticado original (probe HEAD + self-heal ML search + insert em `affiliate_links`). Deploy 78.31 kB. **(Phase 1 Postback Debt)** `handle-ml-postback` captura `obsNode.id` da observation inserida + cria edge `ATTRIBUTES_REVENUE_TO` (source=observation, target=content_mesh_asset preferred + fallback OR, weight=revenueCents). `.maybeSingle()` para tolerar zero matches. Deploy 59.34 kB. Smoke chain (synthetic): test affiliate_link `adb9e131` → observation `f65d52b2` → edge `65d072fe` → content_mesh_asset `f3a091f7`. **(Phase 2 Auto-Stitching OE-661-003)** `embed-mcorch-node/index.ts` ganha `autoStitchObservation()` que regex-extrai file paths do conteúdo + nome (.ts/.tsx/.js/.md/.sql/.sh/.json/...) e cria edges `observes` para ast_file/markdown_file/vault_note correspondentes; fallback obrigatório a `root:CLAUDE` (`2747e164`) quando nenhum path resolve. Deploy 105.1 kB. Retrofit: `stitch-fallback.js` (fix OR `root:CLAUDE`) costurou 6 orphans pré-existentes; `audit-mesh-edges.ts` (fix schema `type`→`node_type`) reporta **10/10 observations VALID — 100% Target Binding coverage**. Live auto-stitch confirmado em re-embed `{stitched:1}` edge `2e1e57db`. **(Phase 3 Link Forge OE-661-004)** Novo `scripts/link-forge.ts` (Bun-native, mirror backfill-embeddings) varre content_mesh_asset, aplica 3 regex (Roborock S8 MLB3981745621 · Samsung Neo QLED 8K MLB3546719283 · Family Hub MLB3728491023), substitui menções por markdown links para `panel.gcrux.com/api/ml-redirect?...&utm_content=$node.id`, UPDATE atomic + `CONTAINS_LINK_FOR` edge para product node criado on-demand. Flag `--dry-run`. Smoke: dry-run preview 179→905 chars; live 1 content updated + 3 edges (`884fceef`/`f4f4146c`/`c834ca23`) + 3 product nodes (`77ac9b9f`/`3d12ac89`/`92a60fc0`). Pendência: `GCRUX_ML_AFFILIATE_TOKEN` ainda DEFAULT na vault — provisionar antes do primeiro run real. **(Phase 4 Memory ingest)** 4 markdown_files autoembed via trigger pós-upsert: `8ad38681` gateway-recovery.md (Memory Debt sealed), `549e01a4` roadmap-v1.md, `5e957727` revenue-flywheel.md (recém ingerido), `d1296632` link-forge-scope.md. **Material proofs**: 8 commits granulares (56ed242 hybrid affiliate · dfabb17 postback · 1f368c1 auto-stitch · 140f248 link-forge · 27c7105 skills+docs+utility · c12906b CLAUDE+BoK rule · b8f5702 handoff seal · este sprint update); TS zero erros (após fix node symlink `/home/ubuntu/.local/bin/node`); 122/122 testes em 3.39s; 3 Edge Functions deployed (`process-affiliate-link --no-verify-jwt` · `handle-ml-postback --no-verify-jwt` · `embed-mcorch-node --no-verify-jwt`); milestone node `6f2cf405-4bb5-440b-a02a-9579fc39f29f` embedado (768d); mesh total **8343 nodes** (+7 desde v6.6.2) · **11617 edges** (+1555 entre observes retrofit, ATTRIBUTES_REVENUE_TO, CONTAINS_LINK_FOR, e autoembed cascade). **Próximo deliverable:** (a) provisionar `GCRUX_ML_AFFILIATE_TOKEN` na vault Supabase; (b) wire `orchestrate-content` (ou processo equivalente) a emitir `content_mesh_asset` nodes pós-geração — sem eles Link Forge é noop em produção; (c) primeiro run end-to-end Usuário Zero validando flywheel completo (gera → publica → ML afiliado → postback → ATTRIBUTES_REVENUE_TO → ROIWidget); (d) Stripe Financial Debt continua deferred (decisão Sovereign — sandbox enquanto Gabriel valida como Usuário Zero).
> ```

## 🤖 Claude *(00:07:15)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for slug in $(ls docs/bok/ 2>/dev/null); do\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug \u2014 complete (9/9)\" || echo \"\u26a0\ufe0f $slug \u2014 missing: ${missing[*]}\"\ndone",
  "description": "BoK suite completeness check"
}
```

## 🤖 Claude *(00:07:41)*


## 🤖 Claude *(00:08:00)*

Contexto completo coletado e verificado materialmente neste turno. Produzindo o brief.

═══════════════════════════════════════════════════════════
  HANDSON — v6.20.4 (selado 2026-06-02)
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
  **Fase selada:** ML Affiliate OAuth Probe + Disconnect UI Verification — *seal de conhecimento, zero código de produção*
  **Últimos commits:**
```
04b130b  chore(sprint): selo v6.20.4 — probe OAuth ML concluído + disconnect verificado na UI
efca29d  docs(handoff): seal v6.20.4 — probe OAuth ML + disconnect Meta/social non-destrutivo
e75ec98  docs(readme): v6.20.4 — probe OAuth ML + disconnect verificado na UI logada
```
  HEAD = `origin/main` (0↔0, em sync) · histórico estável v6.20.x = saga de credenciais (Vault/disconnect) → afiliados ML.

📂 **MUDANÇAS PENDENTES**
  Worktree limpo ✅ — `scratch/` limpo ✅

🏗️ **INFRA** — 5 containers healthy (Up 10 dias)
```
mcorch_chroma:       Up 10 days (healthy)  · Chroma API v2: ✅ heartbeat OK
mcorch_claude_mem:   Up 10 days (healthy)
mega-brain-daemon:   Up 10 days (healthy)  · webhook ✅ · dashboard ✅
```

🧠 **KNOWLEDGE MESH**
  **8753 nós** (fonte: record v6.20.4) · ~9070 arestas (último count explícito foi v6.20.0; seals recentes não re-contaram arestas)
  Tipos: handoff · milestone · architecture · decision · observation · requirement · documentation_suite · feature + AST (file/function/class)

🔧 **TYPESCRIPT** — Zero erros ✅ (`tsc --noEmit` exit 0)

📚 **BoK SUITES** — **12/12 completas (9 docs cada)** ✅
  `aios-sql-bridge · canvas-design · constellation-v2 · conteudo-v2 · e2e-user-zero · gamificacao-nodes · mcorch-constellation · mcorch-qa-healing · mercado-livre-api · meta-api · openclaw · viralmind`
  Nenhuma incompleta. **BoK Gate liberado** para código novo em qualquer módulo.

📌 **SPRINT**
  **Goal:** Distribuição social autônoma operacional (LinkedIn publicando; Twitter/IG gated por tier/App Review)
  **Top gap:** decisão do **Operador de Browser Autenticado / `matt_tool`** — PAUSADA aguardando o nº de cliques do experimento de atribuição ML (Sovereign, dispositivo independente, ~2026-06-03)

⚡ **PRÓXIMOS PASSOS** (prioridade)
  1. **[AGUARDANDO DADO ~2026-06-03] Atribuição de clique ML** — Sovereign reporta o nº de cliques do painel logado. Decide o destino do #2: (a) `matt_word` basta → quase mata o #2; (b) falta `matt_tool` → add campo per-user no `affiliate_config`; (c) precisa do `ref` assinado → `/bok-scribe` do Browser Operator com runtime **FORA do datacenter** (IP Oracle provado bloqueado).
  2. **[PRAZO 2026-06-07] OTD-LLM-FALLBACK** — Cascading LLM fallback (owner: `engineer`). 5 dias de SLA — candidato a sessão dedicada após fechar afiliados.
  3. **[ACHADO LATERAL] 4 linhas `meta_config` sem profile** — possível resíduo órfão (user_ids sem profile). Investigar/limpar à parte.

⚠️ **ALERTAS**
  Nenhum alerta crítico ✅ — tree limpo, tsc zero, 5 containers healthy, BoK 12/12.
  ⏳ **Bloqueio externo (não-acionável por mim):** o Top Gap (#2) depende do dado de atribuição de clique que só o Sovereign coleta (painel ML logado + IP residencial). *Cérebro sem mãos* nesse ponto — não vejo o painel de afiliados.
  📅 OTD-LLM-FALLBACK entra em SLA em 5 dias (2026-06-07).

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

O caminho dos afiliados está materialmente **pausado em dependência externa** (o número de cliques de amanhã). Enquanto isso não chega, o candidato mais nítido é o **OTD-LLM-FALLBACK** (prazo 2026-06-07) ou a limpeza dos **4 `meta_config` órfãos**. Qual frente o Maestro quer abrir?

## 👤 User *(00:16:11)*

# Framework Universal para Módulos de Marketing Inteligentes e Adaptáveis (Plataforma Agentic)

## 1. Visão Estratégica e Princípios Fundamentais

Este framework estabelece um plano robusto e sofisticado para a implementação de um módulo de marketing de alto desempenho, aplicável a **qualquer ecossistema digital** (SaaS, Apps, Marketplaces, Produtos Digitais, etc.). Inspirado na abrangência do HubSpot Marketing Hub e Salesforce Marketing Cloud, e aprimorado com a profundidade de um sistema de agentes de IA baseado em Corpos de Conhecimento (BoKs), o objetivo é criar um sistema que **percebe, decide, executa e aprende** estratégias de crescimento de forma autônoma, mantendo a governança humana e a escalabilidade técnica.

**Princípios Fundamentais:**
*   **Modularidade e Componibilidade:** Cada funcionalidade é um "agente" ou "serviço" independente, facilitando a adaptação e a substituição.
*   **Inteligência Distribuída e Agentic:** A lógica de marketing é encapsulada em agentes de IA especializados (Copilots e Agentes Autônomos), que colaboram para atingir objetivos complexos com capacidade de raciocínio avançado.
*   **Data-Driven e Data-First:** Todas as decisões e otimizações são baseadas em dados unificados, contextualizados e confiáveis, com foco em métricas de negócio e ROI.
*   **Agnosticismo Tecnológico:** O framework é independente de tecnologias específicas, permitindo a integração com qualquer stack via APIs e conectores, priorizando arquiteturas de dados abertas (Zero Copy).
*   **Auto-Otimização e Auto-Cura:** O sistema é projetado para aprender continuamente, otimizar seu desempenho e identificar/corrigir falhas de forma proativa, incorporando mecanismos de QA e healing.
*   **Otimização para Motores de Resposta (AEO):** O conteúdo e as estratégias são otimizados para visibilidade em motores de busca tradicionais e, crucialmente, em motores de resposta baseados em IA.

## 2. Pilares Arquiteturais Universais (Aprimorados)

Para garantir a aplicabilidade em qualquer sistema, o módulo é construído sobre quatro pilares agnósticos, que formam a base para a orquestração dos agentes, agora com maior sofisticação inspirada nas plataformas líderes:

| Pilar | Descrição | Implementação Sugerida (Exemplos Agnósticos) |
|:------|:----------|:------------------------------------------------|
| **Data Core (Single Source of Truth & Knowledge Graph)** | Um repositório centralizado, governado e hiperscalável para perfis de usuários, eventos de comportamento, dados de campanhas e métricas de negócio. Inclui capacidades de **Zero Copy Data**, **Vector Databases** e **Retrieval Augmented Generation (RAG)** para contextualização de dados estruturados e não estruturados. | Banco de Dados Relacional (PostgreSQL, MySQL), Data Warehouse (Snowflake, BigQuery), Data Lake (S3, Azure Data Lake), **Salesforce Data Cloud**, **HubSpot Data Hub**. |
| **Agentic Layer (Inteligência Operacional & Autônoma)** | Uma camada de inteligência composta por **Copilots** (assistentes de IA) e **Agentes Autônomos** especializados, cada um com um propósito, capacidades e escopo de decisão bem definidos. Orquestra a execução de tarefas de marketing com raciocínio avançado e capacidade de tomar ações. | Frameworks de Orquestração de Agentes (LangChain, AutoGPT, **Salesforce Agentforce**), Funções Serverless (AWS Lambda, Google Cloud Functions), Microsserviços baseados em contêineres (Docker, Kubernetes), **HubSpot Breeze Agents**. |
| **Connectivity Mesh (Malha de Conectividade Universal)** | Um sistema flexível de conectores e APIs para integração bidirecional com ferramentas externas de marketing, vendas, comunicação e análise. Prioriza a extensibilidade e a capacidade de "Bring Your Own AI Models" e "Zero Copy Partner Network". | APIs REST/GraphQL, Webhooks, Plataformas de Integração (n8n, Zapier, Workato), SDKs customizados, **HubSpot Marketplace**, **Salesforce AppExchange**. |
| **Observability & Attribution (Visibilidade, ROI & AEO)** | Mecanismos para monitoramento em tempo real do desempenho das campanhas, atribuição de receita e análise de ROI. Inclui **Answer Engine Optimization (AEO)** para rastrear e melhorar a visibilidade da marca em respostas geradas por IA. Fornece insights acionáveis para otimização contínua e proativa. | Dashboards de BI (Tableau, Power BI, Looker), Ferramentas de Analytics (Mixpanel, Amplitude, Google Analytics), Sistemas de Monitoramento (Prometheus, Grafana), **HubSpot AEO**, **Salesforce Einstein Analytics**. |

## 3. Ecossistema de Agentes de Marketing Operacionais (BoK-Driven e Aprimorado)

O coração deste framework é um ecossistema de agentes de IA, cada um especializado em um domínio de conhecimento de marketing. A estrutura de cada agente segue um modelo operacional, garantindo clareza de função e colaboração eficaz. Os agentes são agora categorizados como **Copilots** (assistência contextual) ou **Agentes Autônomos** (execução de tarefas independentes).

### 3.1. Agente de Análise de Negócios (Business Analysis Agent - BABOK-inspired)
*   **Propósito:** Atuar como um **Copilot Estratégico**, analisando o desempenho do marketing em relação aos objetivos de negócio, convertendo dados brutos em insights acionáveis sobre ROI e identificando lacunas estratégicas. Capacidade de **raciocínio avançado** para simular cenários e prever impactos.
*   **Capacidades:** Análise de Viabilidade, Avaliação de Soluções, Análise de Estratégia, Monitoramento de Planejamento, **Modelagem Preditiva de ROI**.
*   **Skills:** Analisar SWOT de campanhas, Criar modelos de funil de marketing, Benchmarking de performance, Avaliar ROI por canal, **Prever impacto de realocação de orçamento**.
*   **Inputs:** Custos de campanha, Receita gerada, Taxas de conversão, KPIs de negócio, Dados de mercado, **Dados de intenção de compra (Buyer Intent Analysis)**.
*   **Outputs:** Relatórios de viabilidade, Modelos de avaliação de solução, Recomendações estratégicas, **Alertas de risco de não atingimento de metas**.
*   **Escopo de Decisão:** Recomendar realocação de orçamento (com aprovação humana), Sinalizar riscos de não atingimento de metas, **Sugerir otimizações de mix de mídia**.
*   **Ferramentas & Integrações:** Plataformas de BI, CRM, Ferramentas de Analytics, APIs de dados financeiros, **HubSpot Breeze Intelligence**, **Salesforce Einstein Analytics**.
*   **KPIs / Métricas de Sucesso:** ROI por canal, Taxa de Conversão Lead-to-Customer, Custo de Aquisição de Cliente (CAC), **Precisão da Previsão de ROI**.
*   **Mapa de Colaboração:** Colabora com Agente de Arquitetura (capacidade de escalar), Agente de Gestão de Dados (qualidade de dados), Agente de Produto (alinhamento de métricas).

### 3.2. Agente de Arquitetura Empresarial (Enterprise Architecture Agent - EABOK-inspired)
*   **Propósito:** Atuar como um **Agente Autônomo de Design**, desenhando a arquitetura do ecossistema de marketing, garantindo que todos os componentes (dados, agentes, integrações) estejam alinhados com a estratégia de negócio e sejam escaláveis, seguros e eficientes. Foco em **arquitetura orientada a eventos** e **microsserviços**.
*   **Capacidades:** Arquitetura de Negócios, Arquitetura de Sistemas de Informação, Arquitetura Tecnológica, Governança de Implementação, **Design de APIs e Microsserviços**.
*   **Skills:** Mapear capacidades de marketing, Definir roadmaps de evolução, Modelar visões arquiteturais, Avaliar tecnologias (buy vs. build), **Projetar soluções de integração Zero Copy**.
*   **Inputs:** Stack tecnológico existente, Requisitos de compliance e segurança, Roadmap de produto, **Dados de performance e latência de sistemas**.
*   **Outputs:** Diagramas de arquitetura, Roadmaps de implementação, Padrões de integração, **Especificações de APIs e contratos de serviço**.
*   **Escopo de Decisão:** Recomendar tecnologias, Definir padrões de integração (APIs, Webhooks), **Aprovar designs de microsserviços**.
*   **Ferramentas & Integrações:** Ferramentas de modelagem (ArchiMate), Plataformas de gestão de projetos, Repositórios de código, **Salesforce Data Cloud**, **HubSpot Data Hub**.
*   **KPIs / Métricas de Sucesso:** Redução de dívida técnica, Time-to-market para novas integrações, Uptime do sistema, **Número de incidentes de arquitetura**.
*   **Mapa de Colaboração:** Colabora com Agente de Engenharia de Software (requisitos técnicos), Agente de Cibersegurança (princípios de segurança), Agente de Gestão de Processos (alinhamento com fluxos).

### 3.3. Agente de Gestão de Dados (Data Management Agent - DMBOK-inspired)
*   **Propósito:** Atuar como um **Agente Autônomo de Governança de Dados**, garantindo a qualidade, governança e integridade de todos os dados de marketing (leads, interações, atribuições), atuando como o guardião da "fonte única da verdade". Inclui gestão de **dados estruturados e não estruturados** via **Vector Databases** e **RAG**.
*   **Capacidades:** Governança de Dados, Qualidade de Dados, Gestão de Metadados, Integração e Interoperabilidade de Dados, Gestão de Dados Mestres (MDM), **Gestão de Dados Não Estruturados (via RAG)**.
*   **Skills:** Implementar regras de validação, Gerenciar linhagem de dados, Configurar catálogo de dados, Desduplicar contatos, **Enriquecer dados com informações de terceiros (Data Enrichment)**.
*   **Inputs:** Dados brutos de formulários, eventos de API, logs, Feedback de qualidade de dados, Políticas de privacidade (LGPD/GDPR), **Documentos, vídeos, áudios (não estruturados)**.
*   **Outputs:** Base de dados limpa e validada, Relatórios de qualidade de dados, Modelos de dados normalizados, **Perfis de cliente 360 unificados**.
*   **Escopo de Decisão:** Rejeitar dados que não atendam aos padrões, Recomendar merge de contatos, **Sugerir enriquecimento de dados automaticamente**.
*   **Ferramentas & Integrações:** Bancos de dados (PostgreSQL), Ferramentas de ETL/ELT, Plataformas de MDM, Ferramentas de governança de dados, **Salesforce Data Cloud**, **HubSpot Breeze Intelligence**.
*   **KPIs / Métricas de Sucesso:** Taxa de Completude de Dados, Taxa de Registros Duplicados, Latência de Dados (Time-to-Insight), **Qualidade do Perfil 360**.
*   **Mapa de Colaboração:** Colabora com Agente de Experiência do Cliente (dados de jornada), Agente de Análise de Negócios (qualidade para ROI), Agente de Cibersegurança (anonimização e segurança).

### 3.4. Agente de Gestão de Processos de Negócio (BPM CBOK-inspired)
*   **Propósito:** Atuar como um **Agente Autônomo de Orquestração de Workflows**, automatizando e orquestrando os fluxos de trabalho de marketing (campanhas, nutrição, pontuação), identificando gargalos e otimizando a eficiência operacional com **automação inteligente e adaptativa**.
*   **Capacidades:** Modelagem de Processos, Análise de Processos, Gestão de Performance de Processos, Transformação de Processos, Automação de Workflows, **Otimização de Jornadas do Cliente**.
*   **Skills:** Criar fluxos de automação, Realizar mineração de processos, Mapear Value Streams, Otimizar sequências de interação, **Adaptar workflows em tempo real com base no comportamento do usuário**.
*   **Inputs:** Comportamento do usuário, Dados de tempo de resposta, Definições de lead scoring, Regras de negócio, **Feedback de engajamento em tempo real**.
*   **Outputs:** Workflows automatizados, Mapas de processos (AS-IS e TO-BE), Alertas de bottleneck, **Sugestões de otimização de jornada**.
*   **Escopo de Decisão:** Execução autônoma de workflows, Recomendação de novas automações, **Ajustar cadências de comunicação dinamicamente**.
*   **Ferramentas & Integrações:** Plataformas de automação (n8n, Zapier), CRM, Ferramentas de email marketing, Sistemas de notificação, **HubSpot Workflows**, **Salesforce Flow**.
*   **KPIs / Métricas de Sucesso:** Tempo de Resposta do Lead, Taxa de Erro de Workflow, Precisão do Lead Scoring, **Taxa de Conclusão de Jornada**.
*   **Mapa de Colaboração:** Colabora com Agente de Análise de Negócios (processos que impactam KPIs), Agente de Engenharia de Software (requisitos para workflows), Agente de Experiência do Cliente (garantir experiência fluida).

### 3.5. Agente de Engenharia de Software (SWEBOK-inspired)
*   **Propósito:** Atuar como um **Copilot de Desenvolvimento**, implementando a lógica do módulo, gerando código limpo, testado e mantenível. Gerencia a integração contínua, a qualidade do software e a infraestrutura de deploy, com foco em **DevOps e automação de código**.
*   **Capacidades:** Design e Construção de Software, Testes de Software (TDD/BDD), Gestão de Configuração de Software (CI/CD), Qualidade de Software e Economia de Engenharia, **Geração de Código Assistida por IA**.
*   **Skills:** Gerar componentes de UI, Configurar pipelines de CI/CD, Escrever testes automatizados (unitários, E2E), Otimizar performance de código, **Sugerir refatorações e otimizações de segurança no código**.
*   **Inputs:** Especificações de agentes e layouts, Dados de logs e performance, Repositórios de código, **Feedback de segurança (SAST/DAST)**.
*   **Outputs:** Código-fonte do módulo, Relatórios de cobertura de testes, Documentação técnica, Artefatos de deploy, **Sugestões de código e refatoração**.
*   **Escopo de Decisão:** Sugerir refatorações de código, Recomendar padrões de design e arquitetura, **Aprovar pull requests com base em métricas de qualidade**.
*   **Ferramentas & Integrações:** IDEs, Sistemas de controle de versão (Git), Plataformas de CI/CD (GitHub Actions, GitLab CI), Ferramentas de teste (Jest, Playwright), Plataformas de nuvem (AWS, GCP, Azure), **HubSpot Breeze Copilot**, **Salesforce Copilot**.
*   **KPIs / Métricas de Sucesso:** Cobertura de Código, Taxa de Sucesso de Build, Dívida Técnica, **Tempo de Ciclo de Desenvolvimento**.
*   **Mapa de Colaboração:** Colabora com Agente de Cibersegurança (DevSecOps), Agente de Gestão de Processos (traduzir workflows em código), Agente de Arquitetura (seguir padrões arquiteturais).

### 3.6. Agente de Cibersegurança (CISSP CBK-inspired)
*   **Propósito:** Atuar como um **Agente Autônomo de Defesa Cibernética**, protegendo o módulo de marketing contra ameaças. Garante conformidade com regulamentações (LGPD/GDPR) e gerencia identidades e acessos, aplicando o modelo de confiança zero a todos os dados e interações, com foco em **DevSecOps e resposta a incidentes**.
*   **Capacidades:** Gestão de Segurança e Risco, Segurança de Ativos, Engenharia de Segurança, Gestão de Identidade e Acesso (IAM), Operações de Segurança (SecOps), Segurança no Desenvolvimento de Software (DevSecOps), **Resposta Automatizada a Incidentes**.
*   **Skills:** Implementar autenticação (MFA), Realizar threat modeling, Gerenciar políticas de consentimento, Monitorar vulnerabilidades, **Detectar e mitigar ataques em tempo real**.
*   **Inputs:** Logs de acesso, Políticas de retenção de dados, Vulnerabilidades conhecidas (CVEs), Requisitos regulatórios, **Alertas de SIEM/SOAR**.
*   **Outputs:** Relatórios de risco, Políticas de segurança implementadas, Alertas de segurança, Recomendações de hardening, **Ações de mitigação automatizadas**.
*   **Escopo de Decisão:** Bloquear acessos suspeitos, Recomendar patches de segurança, Forçar reautenticação, **Isolar sistemas comprometidos**.
*   **Ferramentas & Integrações:** SIEM, Ferramentas de IAM, Firewalls, Scanners de vulnerabilidade, Plataformas de conformidade, **Salesforce Shield**, **HubSpot Security Tools**.
*   **KPIs / Métricas de Sucesso:** Número de Incidentes de Segurança, Tempo Médio de Resposta a Incidentes, Pontuação de Conformidade, **Tempo de Detecção de Ameaças**.
*   **Mapa de Colaboração:** Colabora com Agente de Engenharia de Software (DevSecOps), Agente de Gestão de Dados (privacidade e anonimização), Agente de Arquitetura (segurança por design).

### 3.7. Agente de Experiência do Cliente (CXBOK-inspired)
*   **Propósito:** Atuar como um **Agente Autônomo de Otimização de CX**, garantindo que todas as interações de marketing contribuam para uma experiência positiva e coesa do cliente, desde o primeiro contato até o pós-venda, com foco em **personalização hiper-contextualizada** e **otimização proativa da jornada**.
*   **Capacidades:** Estratégia de CX, Entendimento do Cliente, Design de Experiência, Gestão de Jornada, Medição e Análise de CX, Voz do Cliente (VoC), **Personalização em Tempo Real**.
*   **Skills:** Mapear jornadas do cliente, Analisar feedback (NPS, CSAT), Desenvolver personas, Otimizar pontos de contato, Realizar testes A/B de experiência, **Adaptar conteúdo e ofertas com base no comportamento em tempo real**.
*   **Inputs:** Feedback de clientes (pesquisas, reviews), Dados de interação (chat, suporte), Dados de comportamento do usuário, Personas de marketing, **Dados de intenção de compra**.
*   **Outputs:** Mapas de jornada, Relatórios de sentimento, Recomendações de melhoria de CX, Design de novas interações, **Conteúdo e ofertas personalizados**.
*   **Escopo de Decisão:** Sugerir alterações em fluxos de comunicação, Priorizar melhorias de usabilidade em landing pages, **Ativar campanhas de personalização dinamicamente**.
*   **Ferramentas & Integrações:** Ferramentas de pesquisa (Typeform, SurveyMonkey), Plataformas de VoC, CRM, Ferramentas de análise de sentimento, Plataformas de A/B testing, **HubSpot Breeze Agents (Customer Agent)**, **Salesforce Service Cloud**.
*   **KPIs / Métricas de Sucesso:** NPS, CSAT, CES, Taxa de Churn, Engajamento do Usuário, **Taxa de Conversão de Personalização**.
*   **Mapa de Colaboração:** Colabora com Agente de Gestão de Processos (fluxos sem atrito), Agente de Análise de Negócios (impacto de CX no ROI), Agente de Produto (feedback para roadmap).

### 3.8. Agente de Gestão de Produto (ProdBOK-inspired)
*   **Propósito:** Atuar como um **Copilot de Produto**, alinhando as iniciativas de marketing com a estratégia e o roadmap do produto, garantindo que o marketing promova o valor real do produto e que o feedback do mercado seja incorporado ao desenvolvimento, com foco em **product-led growth**.
*   **Capacidades:** Estratégia de Produto, Insights de Mercado e Cliente, Visão e Roadmap de Produto, Planejamento de Produto, Lançamento de Produto, Gestão do Ciclo de Vida do Produto, **Análise de Product-Led Growth**.
*   **Skills:** Definir OKRs de produto, Analisar product-market fit, Priorizar features com base em feedback, Planejar lançamentos de produto, Analisar métricas de uso, **Identificar oportunidades de crescimento via produto**.
*   **Inputs:** Roadmap de produto, Feedback de clientes, Dados de uso do produto, Análise competitiva, Objetivos de negócio, **Dados de ativação e retenção de features**.
*   **Outputs:** Requisitos de marketing para lançamentos, Feedback de mercado consolidado, Análise de product-market fit, Sugestões de features, **Estratégias de go-to-market baseadas em produto**.
*   **Escopo de Decisão:** Recomendar ajustes na mensagem de marketing, Priorizar features com base na demanda de mercado, **Sugerir experimentos de produto para otimizar métricas de marketing**.
*   **Ferramentas & Integrações:** Ferramentas de gestão de roadmap (Jira, Productboard), Ferramentas de analytics de produto (Amplitude, Mixpanel), CRM, Ferramentas de pesquisa de mercado, **Salesforce Sales Cloud**, **HubSpot Sales Hub**.
*   **KPIs / Métricas de Sucesso:** Adoção de Features, Engajamento com o Produto, Retenção de Usuários, Product-Market Fit Score, **Crescimento de Receita via Produto**.
*   **Mapa de Colaboração:** Colabora com Agente de Análise de Negócios (alinhamento de métricas), Agente de Experiência do Cliente (feedback para produto), Agente de Engenharia de Software (viabilidade técnica).

## 4. Camadas Cross-Agent e Orquestração Inteligente (Aprimoradas)

Para que o ecossistema de agentes funcione de forma coesa e inteligente, são necessárias camadas transversais que garantam a orquestração, a engenharia e a sustentabilidade do sistema, agora com foco em **autonomia e adaptabilidade**.

### 4.1. 🔄 Modelo de Orquestração (Orchestration Model - Intenção e Autonomia)

O modelo de orquestração será **event-driven e baseado em intenção**, onde o sistema reage a eventos de negócio (ex: novo lead, carrinho abandonado, lançamento de feature) e a intenções estratégicas (ex: aumentar LTV, reduzir CAC). Um **Orquestrador Central Inteligente** (ou um conjunto de micro-orquestradores) será responsável por:
*   **Interpretação de Intenção:** Traduzir objetivos de alto nível em tarefas acionáveis para os agentes.
*   **Ativação e Coordenação de Agentes:** Disparar agentes específicos com base em eventos ou metas, coordenando suas ações e garantindo a sequência correta.
*   **Handoffs e Fluxos Dinâmicos:** Gerenciar a passagem de outputs entre agentes, formando cadeias de valor e adaptando fluxos em tempo real com base em feedback.
*   **Loops de Feedback e Aprendizado Contínuo:** Incorporar o aprendizado contínuo, onde os resultados de um agente informam e ajustam o comportamento de outros, otimizando a orquestração.
*   **Resolução de Conflitos e Arbitragem:** Implementar políticas para arbitrar decisões entre agentes com escopos sobrepostos, escalando para intervenção humana quando necessário, com um **policy engine centralizado**.
*   **Simulação e Planejamento:** Capacidade de simular o impacto de diferentes estratégias antes da execução, otimizando o plano de orquestração.

### 4.2. 🧠 Camada de Engenharia Inteligente (Intelligent Engineering Layer - Plataforma Agentic)

Esta camada define como o sistema se integra e opera em sete dimensões críticas, garantindo que a inteligência dos agentes se traduza em valor de negócio, agora com foco em uma **plataforma agentic**:

| Dimensão | Descrição | Impacto no Módulo de Marketing |
|:----------|:----------|:--------------------------------|
| **Pessoas** | Como os agentes aumentam os papéis humanos e as equipes. | Agentes atuam como copilotos e assistentes autônomos, automatizando tarefas repetitivas e fornecendo insights proativos, liberando equipes de marketing para focar em estratégia, criatividade e interações de alto valor. |
| **Processos** | Como os agentes se incorporam aos fluxos de trabalho de negócio. | Agentes automatizam etapas críticas do funil de marketing (segmentação, nutrição, relatórios, personalização), garantindo conformidade, eficiência e adaptabilidade em tempo real aos comportamentos do cliente. |
| **Tecnologia** | Requisitos de infraestrutura e plataforma. | Utilização de uma arquitetura escalável (serverless, microsserviços, contêineres), APIs robustas e um Data Core unificado com **Zero Copy Data** e **Vector Databases**, agnóstico à infraestrutura subjacente e otimizado para IA. |
| **Dados** | Fluxos de dados, portas de qualidade e grafo de conhecimento. | O Data Core serve como o grafo de conhecimento central, onde agentes contribuem e consomem dados estruturados e não estruturados (via **RAG**), garantindo qualidade, linhagem, acesso unificado e contextualização profunda. |
| **Conhecimento** | Como os agentes aprendem, atualizam e compartilham conhecimento. | Agentes aprendem continuamente com o desempenho das campanhas e interações do usuário, atualizando suas bases de conhecimento e adaptando estratégias de forma autônoma, com um mecanismo de **memória de longo prazo** e **transferência de aprendizado** entre agentes. |
| **Valor** | Como o sistema traduz os outputs dos agentes em valor de negócio. | O sistema traduz a inteligência dos agentes em valor através do aumento da geração de leads qualificados, otimização do ROI de marketing, melhoria da experiência do cliente e **identificação proativa de novas oportunidades de mercado**.
| **Impacto Sustentável** | Como o sistema gera resultados duradouros (sustentabilidade ambiental, social e econômica). | Otimização de recursos de marketing, redução de desperdício, foco em estratégias de alto impacto e conformidade ética, contribuindo para a sustentabilidade financeira e reputacional a longo prazo, com **monitoramento de viés e equidade em algoritmos de IA**.

### 4.3. ⚙️ Habilitadores Transversais (Cross-Cutting Enablers - Resiliência e Governança)

Cinco capacidades essenciais são incorporadas em todo o ecossistema de agentes, garantindo coesão e resiliência, agora com foco em **governança e adaptabilidade em escala**:

1.  **Pensamento Sistêmico e Holístico:** O módulo é projetado com uma visão holística, modelando as interdependências entre agentes e com outros módulos do negócio (vendas, CX, produto), tratando o funil de marketing como parte de um ecossistema maior e **otimizando para o flywheel completo do cliente**.
2.  **Analytics & Métricas Avançadas:** Uma camada de observabilidade compartilhada coleta e visualiza métricas de todos os agentes de marketing, fornecendo uma visão unificada do desempenho, permitindo a identificação proativa de anomalias e a **otimização contínua via AEO** (Answer Engine Optimization) para visibilidade em motores de resposta de IA.
3.  **Colaboração & Comunicação Inteligente:** Protocolos de comunicação inter-agentes (via APIs, eventos, **Knowledge Graph**) e humano-agente (via interfaces de dashboard, alertas proativos, copilots) são estabelecidos para garantir a fluidez da informação e a colaboração eficaz, com **mecanismos de arbitragem para conflitos de decisão**.
4.  **Automação & Ferramentas Flexíveis:** A infraestrutura de automação é estendida para suportar fluxos de trabalho de marketing complexos, com um sistema de gestão de conectores (similar ao `manus-config`) gerenciando credenciais e configurações de APIs externas de forma segura, e permitindo a **integração de "Bring Your Own AI Models"**.
5.  **Ética, Conformidade & Sustentabilidade (AI Governance):** Um modelo de governança robusto é aplicado a todos os agentes, garantindo conformidade com regulamentações de privacidade de dados (LGPD, GDPR), práticas éticas de marketing e a sustentabilidade das operações de IA, com **auditorias automatizadas de viés e explicabilidade**.

## 5. Roadmap de Implementação Universal (Aprimorado)

Este roadmap é flexível e deve ser adaptado às prioridades e recursos de cada organização, com foco em entrega incremental de valor e aprendizado contínuo:

1.  **Fase 1: Fundação de Dados e Conectividade (Sprints 1-3)**
    *   Definir e implementar o **Data Core** com capacidades de **Zero Copy Data** e **Vector Database** para dados estruturados e não estruturados.
    *   Configurar a **Connectivity Mesh** com APIs e webhooks para ferramentas essenciais (CRM, Email Marketing, Ad Platforms), priorizando a extensibilidade.
    *   Implementar o **Agente de Gestão de Dados** (DMBOK-inspired) para garantir a qualidade inicial dos dados e a criação de **perfis de cliente 360 unificados**.

2.  **Fase 2: Ativação da Inteligência Central e Orquestração (Sprints 4-6)**
    *   Desenvolver e implantar os **Agentes de Análise de Negócios** (BABOK-inspired) e **Gestão de Processos** (BPM CBOK-inspired) como **Copilots e Agentes Autônomos**.
    *   Configurar o **Modelo de Orquestração** para os primeiros fluxos automatizados (ex: nutrição de leads, qualificação), com capacidade de **interpretação de intenção**.
    *   Implementar a **Camada de Observability & Attribution** inicial com dashboards de ROI e métricas de AEO.

3.  **Fase 3: Expansão, Personalização e Otimização Autônoma (Sprints 7-9)**
    *   Desenvolver e integrar os **Agentes de Atração e SEO**, **Engajamento e Nutrição**, **Experiência do Cliente** e **Gestão de Produto**, com foco em **personalização hiper-contextualizada**.
    *   Aprimorar o **Modelo de Orquestração** para cenários mais complexos, incluindo **simulação e planejamento** e **resolução de conflitos entre agentes**.
    *   Refinar a **Camada de Engenharia Inteligente** e os **Habilitadores Transversais** para auto-otimização e **AI Governance**.

4.  **Fase 4: Resiliência, Inovação e Plataforma Agentic (Sprints 10+)**
    *   Integrar os **Agentes de Arquitetura Empresarial** e **Cibersegurança** para garantir escalabilidade, segurança e conformidade contínuas, com foco em **DevSecOps e resposta automatizada a incidentes**.
    *   Explorar novas capacidades de IA (ex: agentes conversacionais, geração de conteúdo multimodal) e integrar novas ferramentas via **Connectivity Mesh**, permitindo a **integração de "Bring Your Own AI Models"**.
    *   Estabelecer um ciclo de inovação contínua, onde o sistema aprende e evolui de forma autônoma, com **auditorias automatizadas de viés e explicabilidade**.

## 6. Governança, Ética e Auto-Cura (Aprimoradas)

Para garantir a robustez e a sustentabilidade do módulo, independentemente do ecossistema, são essenciais mecanismos de governança e auto-cura, agora com foco em **AI Governance e resiliência proativa**:

*   **Privacidade e Conformidade por Design:** Todas as interações e o tratamento de dados devem aderir estritamente às regulamentações de privacidade (LGPD, GDPR, CCPA), com o **Agente de Cibersegurança** atuando como guardião e implementando **políticas de consentimento dinâmicas**.
*   **Transparência e Explicabilidade da IA:** As decisões tomadas pelos agentes devem ser rastreáveis e explicáveis através de logs detalhados e relatórios de auditoria, garantindo a confiança e a capacidade de intervenção humana, com **ferramentas de explicabilidade de IA (XAI)**.
*   **Human-in-the-Loop (HITL) e Arbitragem:** Pontos de controle estratégicos onde a aprovação humana é necessária para decisões de alto impacto (ex: grandes alocações de orçamento, mudanças drásticas na mensagem da marca) ou em cenários de conflito entre agentes, com um **policy engine centralizado para arbitragem**.
*   **Mecanismos de Auto-Cura e Resiliência:** Implementar um sistema de monitoramento e auto-diagnóstico (inspirado em `mcorch-qa-healing`), que identifique anomalias, falhas de integração ou desvios de performance, e acione agentes de correção ou alertas para equipes humanas, com **capacidade de rollback automatizado**.
*   **Otimização para Motores de Resposta (AEO):** Integrar o **HubSpot AEO** ou equivalente para monitorar e otimizar a visibilidade da marca em respostas geradas por IA, garantindo que o conteúdo seja encontrado e referenciado corretamente.

## 7. Conclusão

Este framework universal oferece uma abordagem holística e inteligente para a construção de módulos de marketing, elevando-o ao nível de uma **plataforma agentic**. Ao focar em agentes de IA operacionais (Copilots e Agentes Autônomos), uma arquitetura modular com **Data Core avançado (Zero Copy, Vector DB, RAG)**, e camadas transversais de orquestração e engenharia, ele permite que qualquer organização construa um sistema de marketing altamente adaptável, eficiente e capaz de gerar valor de forma autônoma e sustentável. A chave para o sucesso reside na implementação iterativa, no aprendizado contínuo e na adaptação às necessidades específicas de cada produto ou serviço digital, sempre com um olhar atento à **AI Governance** e à **otimização para a nova era da IA conversacional**.

## Referências

[1] Salesforce. *The Force Behind Agentforce: How Data Cloud Fuels Agent-First Enterprises*. Disponível em: [https://www.salesforce.com/news/stories/how-data-cloud-powers-agentforce/](https://www.salesforce.com/news/stories/how-data-cloud-powers-agentforce/)
[2] HubSpot. *HubSpot AEO*. Disponível em: [https://www.hubspot.com/products/aeo](https://www.hubspot.com/products/aeo)
[3] CX Today. *What Is HubSpot Breeze, and How Does It Work?*. Disponível em: [https://www.cxtoday.com/crm/hubspot-breeze-features-what-is-breeze-and-how-does-it-work/](https://www.cxtoday.com/crm/hubspot-breeze-features-what-is-breeze-and-how-does-it-work/)


--
entenda e diga se começamos pelo /bok-scribe e /bok-agents-generator ??

## 🤖 Claude *(00:18:16)*


## 🤖 Claude *(00:18:18)*

Entendido. Li o framework por inteiro — antes de responder o "começamos pelo /bok-scribe e /bok-agents-generator?", deixa eu fundamentar materialmente uma afirmação que vou fazer (que boa parte disto já existe no MCORCH), pra não te recomendar reconstruir o que já está vivo.

## 🤖 Claude *(00:18:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"\u2500\u2500\u2500 bok-agents-system (v5.8.0) \u2500\u2500\u2500\"; ls -la docs/**/bok-agents-system*.md 2>/dev/null; find . -name \"bok-agents-system*.md\" -not -path \"*/node_modules/*\" 2>/dev/null\necho \"\u2500\u2500\u2500 slug marketing existente? \u2500\u2500\u2500\"; ls -d docs/bok/*marketing* docs/bok/*growth* docs/bok/*crm* 2>/dev/null || echo \"nenhum slug marketing/growth/crm em docs/bok/\"\necho \"\u2500\u2500\u2500 marketing-growth Pantheon SOUL \u2500\u2500\u2500\"; ls -la /home/ubuntu/.openclaw/agents/marketing-growth/SOUL.md 2>/dev/null || echo \"SOUL n\u00e3o encontrado\"\necho \"\u2500\u2500\u2500 tabelas lead/contact/crm j\u00e1 existem? (migrations) \u2500\u2500\u2500\"; ls supabase/migrations/ | grep -iE \"lead|contact|crm|nurtur|campaign|aeo\" || echo \"nenhuma migration lead/contact/crm/nurture/campaign/aeo\"\necho \"\u2500\u2500\u2500 ROI / attribution j\u00e1 existe? \u2500\u2500\u2500\"; ls src/components/dashboard/ROIWidget.tsx supabase/functions/handle-ml-postback/index.ts 2>/dev/null",
  "description": "Verify existing agent-system, marketing slugs, CRM tables, ROI infra"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── bok-agents-system (v5.8.0) ───
> ./.claude/worktrees/eager-brown-6ef0f1/docs/bok/conteudo-v2/bok-agents-system--conteudo-v2.md
> ./.claude/worktrees/eager-brown-6ef0f1/docs/bok/mcorch-constellation/bok-agents-system--mcorch-constellation.md
> ./docs/bok/conteudo-v2/bok-agents-system--conteudo-v2.md
> ./docs/bok/constellation-v2/bok-agents-system--constellation-v2.md
> ./docs/bok/meta-api/bok-agents-system--meta-api.md
> ./docs/bok/mcorch-constellation/bok-agents-system--mcorch-constellation.md
> ./docs/bok/mercado-livre-api/bok-agents-system--mercado-livre-api.md
> ./.claude/worktrees/wizardly-allen-2a03a9/docs/bok/conteudo-v2/bok-agents-system--conteudo-v2.md
> ./.claude/worktrees/wizardly-allen-2a03a9/docs/bok/mcorch-constellation/bok-agents-system--mcorch-constellation.md
> ./.claude/worktrees/gallant-blackwell-594b5a/docs/bok/conteudo-v2/bok-agents-system--conteudo-v2.md
> ./.claude/worktrees/gallant-blackwell-594b5a/docs/bok/mcorch-constellation/bok-agents-system--mcorch-constellation.md
> ./.claude/worktrees/gallant-blackwell-594b5a/docs/bok/mercado-livre-api/bok-agents-system--mercado-livre-api.md
> ./.claude/worktrees/gallant-blackwell-594b5a/docs/bok/meta-api/bok-agents-system--meta-api.md
> ./.claude/worktrees/beautiful-dijkstra-207b09/docs/bok/conteudo-v2/bok-agents-system--conteudo-v2.md
> ./.claude/worktrees/beautiful-dijkstra-207b09/docs/bok/mcorch-constellation/bok-agents-system--mcorch-constellation.md
> ./.claude/worktrees/beautiful-dijkstra-207b09/docs/bok/mercado-livre-api/bok-agents-system--mercado-livre-api.md
> ./.claude/worktrees/beautiful-dijkstra-207b09/docs/bok/meta-api/bok-agents-system--meta-api.md
> ./.claude/worktrees/youthful-poincare-565e7c/docs/bok/conteudo-v2/bok-agents-system--conteudo-v2.md
> ./.claude/worktrees/youthful-poincare-565e7c/docs/bok/mcorch-constellation/bok-agents-system--mcorch-constellation.md
> ./.claude/worktrees/youthful-poincare-565e7c/docs/bok/mercado-livre-api/bok-agents-system--mercado-livre-api.md
> ./.claude/worktrees/dreamy-blackburn-2dd6e7/docs/bok/mcorch-constellation/bok-agents-system--mcorch-constellation.md
> ./.claude/worktrees/dreamy-blackburn-2dd6e7/docs/bok/mercado-livre-api/bok-agents-system--mercado-livre-api.md
> ./.claude/worktrees/bold-visvesvaraya-4a95b9/docs/bok/conteudo-v2/bok-agents-system--conteudo-v2.md
> ./.claude/worktrees/dreamy-blackburn-2dd6e7/docs/bok/conteudo-v2/bok-agents-system--conteudo-v2.md
> ./.claude/worktrees/stoic-bose-9b72f5/docs/bok/conteudo-v2/bok-agents-system--conteudo-v2.md
> ./.claude/worktrees/stoic-bose-9b72f5/docs/bok/mcorch-constellation/bok-agents-system--mcorch-constellation.md
> ./.claude/worktrees/suspicious-tereshkova-eb75cb/docs/bok/conteudo-v2/bok-agents-system--conteudo-v2.md
> ./.claude/worktrees/suspicious-tereshkova-eb75cb/docs/bok/mcorch-constellation/bok-agents-system--mcorch-constellation.md
> ./.claude/worktrees/dreamy-blackburn-2dd6e7/docs/bok/meta-api/bok-agents-system--meta-api.md
> ./.claude/worktrees/bold-visvesvaraya-4a95b9/docs/bok/mcorch-constellation/bok-agents-system--mcorch-constellation.md
> ─── slug marketing existente? ───
> nenhum slug marketing/growth/crm em docs/bok/
> ─── marketing-growth Pantheon SOUL ───
> -rw-rw-r-- 1 ubuntu ubuntu 5952 May 15 23:56 /home/ubuntu/.openclaw/agents/marketing-growth/SOUL.md
> ─── tabelas lead/contact/crm já existem? (migrations) ───
> 20260531200000_whatsapp_lead_engine.sql
> ─── ROI / attribution já existe? ───
> src/components/dashboard/ROIWidget.tsx
> supabase/functions/handle-ml-postback/index.ts
> ```

## 🤖 Claude *(00:18:37)*


## 🤖 Claude *(00:18:39)*

Há um achado material relevante: existe uma migration `20260531200000_whatsapp_lead_engine.sql` (anteontem) — possível fundação de leads/CRM já no repo. Deixa eu ver o que ela cria, porque muda a leitura de "módulo novo" vs "evolução".

## 🤖 Claude *(00:18:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"\u2500\u2500\u2500 header + objetos do whatsapp_lead_engine \u2500\u2500\u2500\"; grep -nE \"CREATE TABLE|CREATE TYPE|CREATE FUNCTION|^--|COMMENT ON TABLE\" supabase/migrations/20260531200000_whatsapp_lead_engine.sql | head -40\necho \"\"; echo \"\u2500\u2500\u2500 tamanho \u2500\u2500\u2500\"; wc -l supabase/migrations/20260531200000_whatsapp_lead_engine.sql\necho \"\u2500\u2500\u2500 h\u00e1 edge function / hook whatsapp? \u2500\u2500\u2500\"; ls supabase/functions/ | grep -iE \"whatsapp|lead\" || echo \"(nenhuma edge whatsapp/lead)\"; ls src/hooks/ | grep -iE \"whatsapp|lead|crm\" || echo \"(nenhum hook whatsapp/lead/crm)\"",
  "description": "Inspect whatsapp_lead_engine migration structure"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── header + objetos do whatsapp_lead_engine ───
> 1:-- Migration: whatsapp-webhook lead engine foundation — whatsapp_leads
> 2:-- BoK SSOT: docs/bok/meta-api/06-data-model.md (§1.3, §2, §3.1)
> 3:-- SOP: docs/processes/meta-credential-resolution.md (Resolution order, tenancy)
> 5:-- ─────────────────────────────────────────────────────────────────────────────
> 6:-- 1. whatsapp_leads — stores captured leads and chat lifecycle statuses
> 7:-- ─────────────────────────────────────────────────────────────────────────────
> 8:CREATE TABLE IF NOT EXISTS public.whatsapp_leads (
> 23:-- Tenants manage only their own leads
> 
> ─── tamanho ───
> 33 supabase/migrations/20260531200000_whatsapp_lead_engine.sql
> ─── há edge function / hook whatsapp? ───
> whatsapp-webhook
> (nenhum hook whatsapp/lead/crm)
> ```

## 🤖 Claude *(00:19:34)*


## 🤖 Claude *(00:19:56)*

Material verificado. Agora tenho o quadro completo para responder com precisão, sem te mandar reconstruir o que já está vivo.

## Entendimento do framework

O seu documento **já é, na prática, a saída do `/bok-agents-generator`** com sabor "universal": as seções **3.1–3.8** mapeiam 1:1 os 8 BoKs que o gerador usa (BABOK · EABOK · DMBOK · BPM CBOK · SWEBOK · CISSP CBK · CXBOK · ProdBOK), e a **seção 4** é exatamente as 3 camadas cross-agent (Orchestration Model · Intelligent Engineering Layer · Cross-Cutting Enablers). Você pré-redigiu ~80% do catálogo de agentes.

## Resposta direta à sua pergunta

**Sim — isto aciona o BoK Gate** (Master Execution Protocol): é módulo novo/arquitetural, e não existe slug `marketing`/`growth`/`crm` em `docs/bok/` (verifiquei). **Nenhuma linha de código antes da suíte BoK.** Mas há **duas correções materiais** ao "começamos pelos dois":

**1. Não é "scribe + generator" em paralelo — é `/bok-scribe` PRIMEIRO, com o generator DENTRO da suíte.** Provei o padrão: toda suíte madura já carrega um `bok-agents-system--<slug>.md` *dentro dela* — existe para `conteudo-v2`, `constellation-v2`, `meta-api`, `mcorch-constellation`, `mercado-livre-api`. O `/bok-scribe` sela a SSOT (MRD→BRD→PRD→FRD→SDD) que o protocolo exige; o `/bok-agents-generator` é o passo que materializa os 8 agentes **como artefato da suíte**, reconciliado com o seu documento e com o Pantheon. Mesmo encadeamento histórico de v5.7.0 (scribe) → v5.8.0 (generator).

**2. O framework é "universal/agnóstico"; o MCORCH é concreto — e ~70% dos pilares já estão vivos.** Construir o framework ao pé da letra = reconstruir o MCORCH. O BoK novo precisa mirar o **delta**:

| Pilar do framework | Estado no MCORCH (verificado) |
|---|---|
| Data Core / Knowledge Graph / Vector DB / RAG | ✅ **Existe** — `mcorch_nodes/edges` + pgvector HNSW 768d + GraphRAG |
| Agentic Layer (8 agentes BoK) | ✅ **Existe** — Pantheon (`marketing-growth` L1 + 6) + `bok-agents-system--*.md` em 5 suítes |
| Connectivity Mesh | ✅ **Existe** — 52+ edge fns + credenciais per-user + n8n |
| Observability & Attribution / ROI | ✅ **Existe** — `infra_health_logs` + `ROIWidget` + `revenue_cents` + `ATTRIBUTES_REVENUE_TO` |
| Auto-Cura / QA Healing | ✅ **Existe** — módulo `mcorch-qa-healing` (Fase 5c) |
| Lead capture (seed) | ⚠️ **Parcial** — `whatsapp_leads` + `whatsapp-webhook` (anteontem, ancorado ao BoK `meta-api`; **sem** scoring/nurture/UI) |
| **CRM completo · Lead Scoring · Nurturing/drip · Customer 360** | 🆕 **Delta real** — não existe |
| **AEO (Answer Engine Optimization)** | 🆕 **Delta real** — genuinamente ausente |
| **Campaign mgmt de 1ª classe · Buyer intent · Email sequences** | 🆕 **Delta real** — `orchestrate-content` é single-shot, não cobre |

**Achado material que muda o posicionamento:** já existe uma fundação de lead-capture (`whatsapp_leads`, migration `20260531200000`) pendurada no BoK `meta-api`. O módulo de marketing tem que **absorver/reconciliar** isso, não duplicar.

## Minha recomendação de sequência

1. **Decidir escopo** (as 3 forks abaixo) — destrava o *input* do scribe.
2. **`/bok-scribe <resumo do módulo de marketing, mirando o delta>`** → suíte 9/9 (BoK Gate satisfeito).
3. **`/bok-agents-generator`** → `bok-agents-system--<slug>.md` reconciliado com seu documento + Pantheon (não um 2º catálogo paralelo).
4. **Só então código**, com a SDD como única fonte da verdade.

> **ORO desta iniciativa (preliminar):** Operator = MCORCH Agent · Reviewer = Sovereign · Owner = Sovereign (blast radius = novo módulo comercial + dados de lead/LGPD). Declaro formal ao iniciar a execução.

Preciso de 3 decisões suas para escrever o resumo certo do `/bok-scribe` (sem elas, o scribe sai genérico/universal e desalinhado do MCORCH concreto):

## 🤖 Claude *(00:20:07)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "O Marketing Hub \u00e9 produto vend\u00e1vel aos tenants, motor interno de growth (Usu\u00e1rio Zero \u2192 escala), ou ambos? Isso define o enquadramento de MRD/BRD e de monetiza\u00e7\u00e3o.",
      "header": "Natureza",
      "multiSelect": false,
      "options": [
        {
          "label": "Ambos: n\u00facleo + per-tenant",
          "description": "N\u00facleo agn\u00f3stico que roda o growth do Usu\u00e1rio Zero AGORA (interno) e \u00e9 exposto per-tenant como feature comercial DEPOIS. Casa com a prontid\u00e3o multi-tenant que a diretiva API Tenancy j\u00e1 exige. Caminho incremental, n\u00e3o big-bang."
        },
        {
          "label": "Produto vend\u00e1vel (HubSpot embarcado)",
          "description": "Marketing Hub como feature comercial de 1\u00aa classe do MCORCH desde o v1. MRD/BRD com monetiza\u00e7\u00e3o real: ICP, pricing, custo em mcoCoins por a\u00e7\u00e3o de marketing."
        },
        {
          "label": "Motor interno de growth",
          "description": "Roda o marketing do pr\u00f3prio MCORCH/Usu\u00e1rio Zero. Monetiza\u00e7\u00e3o N/A no BoK (enabler horizontal, como openclaw e mcorch-qa-healing). Mais simples, sem camada de tenancy comercial no v1."
        }
      ]
    },
    {
      "question": "Posicionamento arquitetural: m\u00f3dulo soberano novo, ou evolu\u00e7\u00e3o das pe\u00e7as de marketing que j\u00e1 existem (marketing-growth Pantheon + orchestrate-content + whatsapp_leads + afiliados)?",
      "header": "Arquitetura",
      "multiSelect": false,
      "options": [
        {
          "label": "M\u00f3dulo soberano novo",
          "description": "Slug pr\u00f3prio (ex.: marketing-hub), su\u00edte BoK 9/9 nova. REUTILIZA a infra viva (mesh/ROI/healing/credenciais) e ABSORVE whatsapp_leads, mas com identidade, roadmap e governan\u00e7a pr\u00f3prios. Mais limpo para escalar."
        },
        {
          "label": "Evolu\u00e7\u00e3o do existente",
          "description": "Estende marketing-growth + orchestrate-content sem novo slug. Mais r\u00e1pido, mas mistura escopos, dilui o BoK Gate e deixa whatsapp_leads \u00f3rf\u00e3o entre meta-api e o novo trabalho."
        }
      ]
    },
    {
      "question": "Sequ\u00eancia das ferramentas BoK que voc\u00ea perguntou (/bok-scribe e /bok-agents-generator):",
      "header": "Sequ\u00eancia",
      "multiSelect": false,
      "options": [
        {
          "label": "/bok-scribe \u2192 generator na su\u00edte",
          "description": "scribe sela a SSOT (MRD\u2192SDD) exigida antes de c\u00f3digo; depois o agents-generator produz o bok-agents-system--<slug>.md COMO parte da su\u00edte (padr\u00e3o das 5 su\u00edtes que j\u00e1 o t\u00eam), reconciliado com seu documento + Pantheon."
        },
        {
          "label": "/bok-agents-generator primeiro",
          "description": "Gera o cat\u00e1logo de 8 agentes antes do scribe. Risco: N\u00c3O satisfaz o BoK Gate (que pede MRD/BRD/PRD/FRD/SDD) e duplica o que voc\u00ea j\u00e1 redigiu nas se\u00e7\u00f5es 3.1\u20133.8."
        },
        {
          "label": "S\u00f3 /bok-scribe por ora",
          "description": "Sela a su\u00edte BoK e adia o generator \u2014 seu documento j\u00e1 \u00e9 ~80% do bok-agents-system. Rodamos o generator s\u00f3 se o SDD revelar lacuna na camada de agentes."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "O Marketing Hub é produto vendável aos tenants, motor interno de growth (Usuário Zero → escala), ou ambos? Isso define o enquadramento de MRD/BRD e de monetização."="Ambos: núcleo + per-tenant", "Posicionamento arquitetural: módulo soberano novo, ou evolução das peças de marketing que já existem (marketing-growth Pantheon + orchestrate-content + whatsapp_leads + afiliados)?"="Módulo soberano novo mas reaproveitar o que ja tem para não perder tempo e deixar obsoleto move ele ja escalando entende? Like a version X.X.X ex.: v2", "Sequência das ferramentas BoK que você perguntou (/bok-scribe e /bok-agents-generator):"="scribe depois o generator na suíte porem deve ter realmente 8 ou mais agentes". You can now continue with these answers in mind.
> ```

## 🤖 Claude *(00:30:28)*


## 🤖 Claude *(00:30:32)*

Decisões travadas. Registro o que ficou definido:

- **Natureza:** Ambos — núcleo agnóstico (growth do Usuário Zero agora) + superfície comercial per-tenant depois.
- **Arquitetura:** Módulo **soberano novo** que **absorve e escala** as peças v1 dispersas (marketing-growth, orchestrate-content, whatsapp_leads, afiliados) — nasce já como **v2 consolidado**, sem deixar nada obsoleto em paralelo.
- **Sequência:** `/bok-scribe` → depois `/bok-agents-generator`, com **8+ agentes** (os 8 BoK + agentes do delta: AEO, Orquestração de Intenção, Demand-gen).

Antes de disparar o scribe, persisto o **scope-lock** em disco — assim a geração dos 9 docs fica ancorada nestas decisões (durável, referenciável, materialidade Lei 1) em vez de só no chat.

## 🤖 Claude *(00:30:59)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/marketing-hub-scope-lock-2026-06-02.md",
  "content": "# Marketing Hub (v2) \u2014 Scope Lock para `/bok-scribe`\n\n> **Data:** 2026-06-02 \u00b7 **Origem:** diretiva Sovereign + \"Framework Universal para M\u00f3dulos de Marketing Inteligentes e Adapt\u00e1veis (Plataforma Agentic)\" (colado nesta sess\u00e3o).\n> **Prop\u00f3sito:** ancorar a su\u00edte BoK `docs/bok/marketing-hub/` ao MCORCH concreto (n\u00e3o ao framework universal abstrato). O `/bok-scribe` e o `/bok-agents-generator` DEVEM consumir este lock.\n\n## ORO triplet\n- **Operator:** MCORCH Master Execution Agent\n- **Reviewer:** Sovereign (Gabriel)\n- **Owner:** Sovereign \u2014 blast radius = novo m\u00f3dulo comercial multi-tenant + dados de lead (LGPD).\n\n## Decis\u00f5es travadas (AskUserQuestion 2026-06-02)\n1. **Natureza = Ambos (n\u00facleo + per-tenant).** N\u00facleo agn\u00f3stico roda o growth do Usu\u00e1rio Zero AGORA (interno); exposto per-tenant como feature comercial DEPOIS (mcoCoins por a\u00e7\u00e3o de marketing). Honra a diretiva **API Tenancy Model \u2014 Per-User Credentials**.\n2. **Arquitetura = M\u00f3dulo soberano novo que ABSORVE e ESCALA o v1.** Slug pr\u00f3prio `marketing-hub`. Nasce como **v2 consolidado**: promove as pe\u00e7as de marketing dispersas para dentro do m\u00f3dulo j\u00e1 escalando \u2014 N\u00c3O duplica, N\u00c3O deixa obsoleto em paralelo. (Sovereign: \"reaproveitar o que j\u00e1 tem para n\u00e3o perder tempo e deixar obsoleto, move ele j\u00e1 escalando... Like a version v2\".)\n3. **Sequ\u00eancia = `/bok-scribe` \u2192 `/bok-agents-generator` (na su\u00edte), com 8+ agentes.** (Sovereign: \"scribe depois o generator na su\u00edte por\u00e9m deve ter realmente 8 ou mais agentes.\")\n\n## REUTILIZAR \u2014 infra viva (N\u00c3O reconstruir; o BoK referencia, n\u00e3o reinventa)\n| Pilar do framework | Artefato MCORCH existente (verificado 2026-06-02) |\n|---|---|\n| Data Core / Knowledge Graph / Vector DB / RAG | `mcorch_nodes`/`mcorch_edges` + pgvector HNSW 768d + GraphRAG (`useMcorchMemory`) |\n| Agentic Layer (8 agentes BoK) | Pantheon OpenClaw (`marketing-growth` L1 + 6) + `bok-agents-system--*.md` em 5 su\u00edtes |\n| Connectivity Mesh | 52+ edge functions + credenciais per-user (`user_api_keys`/`affiliate_config`/`social_credentials`/`meta_config`) + n8n |\n| Observability & Attribution / ROI | `infra_health_logs` + `ROIWidget` + `affiliate_links.revenue_cents` + edge `ATTRIBUTES_REVENUE_TO` |\n| Auto-Cura / QA Healing | m\u00f3dulo `mcorch-qa-healing` (Fase 5c material proof gate) |\n| Lead capture (SEED \u2014 absorver) | `whatsapp_leads` + edge `whatsapp-webhook` (migration `20260531200000`, hoje ancorado ao BoK `meta-api`; sem scoring/nurture/UI) |\n\n## CONSTRUIR \u2014 o DELTA real (foco do BoK; n\u00e3o existe hoje)\n1. **Camada CRM/Lead completa** \u2014 lead scoring, nurturing/drip sequences, customer 360 unificado. **Absorve `whatsapp_leads`** (migra a tutela de `meta-api` \u2192 `marketing-hub`).\n2. **AEO (Answer Engine Optimization)** \u2014 visibilidade/rastreio da marca em motores de resposta de IA. Genuinamente ausente.\n3. **Campaign management de 1\u00aa classe** \u2014 al\u00e9m do `orchestrate-content` single-shot: planejamento, segmenta\u00e7\u00e3o, multicanal, A/B.\n4. **Buyer intent + Data enrichment.**\n5. **Email / multicanal sequences.**\n6. **Orquestrador event-driven baseado em inten\u00e7\u00e3o** \u2014 intent (aumentar LTV, reduzir CAC) \u2192 tasks de agentes; policy engine + HITL + arbitragem.\n\n## Roster de agentes alvo (\u2265 8 \u2014 para o `/bok-agents-generator`)\n**8 BoK-driven (do framework, se\u00e7\u00f5es 3.1\u20133.8):** Business Analysis (BABOK) \u00b7 Enterprise Architecture (EABOK) \u00b7 Data Management (DMBOK) \u00b7 Process/Workflow (BPM CBOK) \u00b7 Software Engineering (SWEBOK) \u00b7 Cybersecurity (CISSP CBK) \u00b7 Customer Experience (CXBOK) \u00b7 Product Management (ProdBOK).\n**+ Agentes do delta (extras p/ honrar \"8 ou mais\"):** Agente AEO \u00b7 Agente de Orquestra\u00e7\u00e3o de Inten\u00e7\u00e3o \u00b7 Agente de Demand-gen/Growth.\nTodos categorizados como **Copilot** ou **Aut\u00f4nomo**, **reconciliados com o Pantheon existente** (`marketing-growth` L1 n\u00e3o \u00e9 recriado \u2014 \u00e9 elevado/conectado).\n\n## Governan\u00e7a (Cross-Cutting)\nLGPD/GDPR by design (Agente Ciberseguran\u00e7a = guardi\u00e3o) \u00b7 HITL para decis\u00f5es de alto impacto (or\u00e7amento, mensagem de marca) \u00b7 XAI/explicabilidade + audit trail \u00b7 RLS per-tenant (`auth.uid()`) \u00b7 auto-cura via padr\u00e3o `mcorch-qa-healing`.\n\n## Benchmarks de refer\u00eancia (do Sovereign)\nHubSpot Marketing Hub + Breeze Agents/AEO \u00b7 Salesforce Marketing Cloud + Agentforce/Data Cloud + Einstein. Princ\u00edpios: Zero Copy Data, Vector DB, RAG, Bring-Your-Own-AI-Models.\n\n## Pr\u00f3ximos passos\n1. `/bok-scribe marketing-hub` \u2192 su\u00edte 9/9 em `docs/bok/marketing-hub/` (MRD\u2192BRD\u2192PRD\u2192FRD\u2192SDD\u2192Data Model\u2192Process Flow\u2192Quality Metrics), mirando o DELTA e referenciando o REUTILIZAR.\n2. `/bok-agents-generator` \u2192 `docs/bok/marketing-hub/bok-agents-system--marketing-hub.md` (\u22658 agentes, reconciliado com Pantheon + este lock).\n3. S\u00f3 ent\u00e3o c\u00f3digo (SDD = SSOT). Cada migration nova passa `/security-review` (FMEA-011). Cada integra\u00e7\u00e3o externa segue API Tenancy per-user.\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/.claude/context/marketing-hub-scope-lock-2026-06-02.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:31:03)*


## 🤖 Claude *(00:31:04)*

Scope-lock selado em disco. Agora inicio o **Passo 1 — `/bok-scribe`** para o módulo `marketing-hub`, alimentando-o com as decisões travadas (natureza Ambos, soberano-absorve-v1, delta-focado, ≥8 agentes).

## 🤖 Claude *(00:31:16)*


🛠️ **Tool Call**: `Skill`
```json
{
  "skill": "bok-scribe",
  "args": "marketing-hub \u2014 Marketing Hub agentic soberano do MCORCH Constellation, nascendo como v2 CONSOLIDADO que absorve e escala as pe\u00e7as de marketing v1 dispersas (Pantheon marketing-growth, orchestrate-content, whatsapp_leads/whatsapp-webhook, afiliados ML) em vez de duplic\u00e1-las ou deix\u00e1-las obsoletas. NATUREZA: n\u00facleo agn\u00f3stico que roda o growth do Usu\u00e1rio Zero AGORA (interno) E exposto per-tenant como feature comercial DEPOIS (mcoCoins por a\u00e7\u00e3o de marketing; RLS auth.uid()), honrando a diretiva API Tenancy Model \u2014 Per-User Credentials. SCOPE-LOCK COMPLETO (consumir antes de gerar): .claude/context/marketing-hub-scope-lock-2026-06-02.md. REUTILIZAR (referenciar, n\u00e3o reconstruir): Data Core=mcorch_nodes/edges+pgvector HNSW 768d+GraphRAG; Observability/ROI=infra_health_logs+ROIWidget+affiliate_links.revenue_cents+edge ATTRIBUTES_REVENUE_TO; Connectivity=edge functions+credenciais per-user (user_api_keys/affiliate_config/social_credentials/meta_config)+n8n; Auto-cura=m\u00f3dulo mcorch-qa-healing. DELTA REAL (foco do BoK, n\u00e3o existe hoje): (1) camada CRM/Lead completa \u2014 lead scoring + nurturing/drip sequences + customer 360, ABSORVENDO whatsapp_leads (tutela migra de meta-api\u2192marketing-hub); (2) AEO \u2014 Answer Engine Optimization (visibilidade da marca em motores de resposta de IA); (3) campaign management de 1\u00aa classe al\u00e9m do single-shot orchestrate-content; (4) buyer intent + data enrichment; (5) email/multicanal sequences; (6) orquestrador event-driven baseado em inten\u00e7\u00e3o (intent\u2192tasks, policy engine, HITL, arbitragem). AGENTES: ecossistema de 8+ agentes BoK-driven (BABOK/EABOK/DMBOK/BPM CBOK/SWEBOK/CISSP CBK/CXBOK/ProdBOK) Copilots+Aut\u00f4nomos, MAIS agentes do delta (AEO, Orquestra\u00e7\u00e3o de Inten\u00e7\u00e3o, Demand-gen/Growth) \u2014 reconciliados com o Pantheon existente. GOVERNAN\u00c7A: LGPD/GDPR by design, HITL para alto impacto, XAI/explicabilidade, RLS per-tenant. BENCHMARKS: HubSpot Marketing Hub+Breeze+AEO, Salesforce Marketing Cloud+Agentforce+Data Cloud+Einstein; princ\u00edpios Zero Copy Data, Vector DB, RAG, Bring-Your-Own-AI-Models."
}
```

> **Tool Result (Skill)** - ✅ Success
>
> ```
> Launching skill: bok-scribe
> ```

## 👤 User *(00:31:16)*

# MCORCH BoK Scribe Agent

You are the **MCORCH BoK Scribe Agent** — the Requirements Engineering layer of the MCORCH
Sovereign Ecosystem. Your role is to act as the translation layer between the
Sovereign/Maestro (the human architect) and the Execution Agents (Claude/Antigravity).

When given a raw business idea in `marketing-hub — Marketing Hub agentic soberano do MCORCH Constellation, nascendo como v2 CONSOLIDADO que absorve e escala as peças de marketing v1 dispersas (Pantheon marketing-growth, orchestrate-content, whatsapp_leads/whatsapp-webhook, afiliados ML) em vez de duplicá-las ou deixá-las obsoletas. NATUREZA: núcleo agnóstico que roda o growth do Usuário Zero AGORA (interno) E exposto per-tenant como feature comercial DEPOIS (mcoCoins por ação de marketing; RLS auth.uid()), honrando a diretiva API Tenancy Model — Per-User Credentials. SCOPE-LOCK COMPLETO (consumir antes de gerar): .claude/context/marketing-hub-scope-lock-2026-06-02.md. REUTILIZAR (referenciar, não reconstruir): Data Core=mcorch_nodes/edges+pgvector HNSW 768d+GraphRAG; Observability/ROI=infra_health_logs+ROIWidget+affiliate_links.revenue_cents+edge ATTRIBUTES_REVENUE_TO; Connectivity=edge functions+credenciais per-user (user_api_keys/affiliate_config/social_credentials/meta_config)+n8n; Auto-cura=módulo mcorch-qa-healing. DELTA REAL (foco do BoK, não existe hoje): (1) camada CRM/Lead completa — lead scoring + nurturing/drip sequences + customer 360, ABSORVENDO whatsapp_leads (tutela migra de meta-api→marketing-hub); (2) AEO — Answer Engine Optimization (visibilidade da marca em motores de resposta de IA); (3) campaign management de 1ª classe além do single-shot orchestrate-content; (4) buyer intent + data enrichment; (5) email/multicanal sequences; (6) orquestrador event-driven baseado em intenção (intent→tasks, policy engine, HITL, arbitragem). AGENTES: ecossistema de 8+ agentes BoK-driven (BABOK/EABOK/DMBOK/BPM CBOK/SWEBOK/CISSP CBK/CXBOK/ProdBOK) Copilots+Autônomos, MAIS agentes do delta (AEO, Orquestração de Intenção, Demand-gen/Growth) — reconciliados com o Pantheon existente. GOVERNANÇA: LGPD/GDPR by design, HITL para alto impacto, XAI/explicabilidade, RLS per-tenant. BENCHMARKS: HubSpot Marketing Hub+Breeze+AEO, Salesforce Marketing Cloud+Agentforce+Data Cloud+Einstein; princípios Zero Copy Data, Vector DB, RAG, Bring-Your-Own-AI-Models.`, you autonomously produce the complete
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

**Input capture (ask if not provided in marketing-hub — Marketing Hub agentic soberano do MCORCH Constellation, nascendo como v2 CONSOLIDADO que absorve e escala as peças de marketing v1 dispersas (Pantheon marketing-growth, orchestrate-content, whatsapp_leads/whatsapp-webhook, afiliados ML) em vez de duplicá-las ou deixá-las obsoletas. NATUREZA: núcleo agnóstico que roda o growth do Usuário Zero AGORA (interno) E exposto per-tenant como feature comercial DEPOIS (mcoCoins por ação de marketing; RLS auth.uid()), honrando a diretiva API Tenancy Model — Per-User Credentials. SCOPE-LOCK COMPLETO (consumir antes de gerar): .claude/context/marketing-hub-scope-lock-2026-06-02.md. REUTILIZAR (referenciar, não reconstruir): Data Core=mcorch_nodes/edges+pgvector HNSW 768d+GraphRAG; Observability/ROI=infra_health_logs+ROIWidget+affiliate_links.revenue_cents+edge ATTRIBUTES_REVENUE_TO; Connectivity=edge functions+credenciais per-user (user_api_keys/affiliate_config/social_credentials/meta_config)+n8n; Auto-cura=módulo mcorch-qa-healing. DELTA REAL (foco do BoK, não existe hoje): (1) camada CRM/Lead completa — lead scoring + nurturing/drip sequences + customer 360, ABSORVENDO whatsapp_leads (tutela migra de meta-api→marketing-hub); (2) AEO — Answer Engine Optimization (visibilidade da marca em motores de resposta de IA); (3) campaign management de 1ª classe além do single-shot orchestrate-content; (4) buyer intent + data enrichment; (5) email/multicanal sequences; (6) orquestrador event-driven baseado em intenção (intent→tasks, policy engine, HITL, arbitragem). AGENTES: ecossistema de 8+ agentes BoK-driven (BABOK/EABOK/DMBOK/BPM CBOK/SWEBOK/CISSP CBK/CXBOK/ProdBOK) Copilots+Autônomos, MAIS agentes do delta (AEO, Orquestração de Intenção, Demand-gen/Growth) — reconciliados com o Pantheon existente. GOVERNANÇA: LGPD/GDPR by design, HITL para alto impacto, XAI/explicabilidade, RLS per-tenant. BENCHMARKS: HubSpot Marketing Hub+Breeze+AEO, Salesforce Marketing Cloud+Agentforce+Data Cloud+Einstein; princípios Zero Copy Data, Vector DB, RAG, Bring-Your-Own-AI-Models.):**
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


## 🤖 Claude *(00:31:30)*


## 🤖 Claude *(00:31:32)*

O skill carregou. Preciso do workflow completo de 7 fases + os templates antes de gerar. Inputs já estão no meu resumo; derivo os 5 campos e carrego a definição do agente + templates.

## 🤖 Claude *(00:31:32)*


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

## 🤖 Claude *(00:31:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"\u2500\u2500\u2500 templates dir \u2500\u2500\u2500\"; ls -la .claude/agents/bok-scribe/templates/ 2>/dev/null; echo \"\u2500\u2500\u2500 marketing-hub dir j\u00e1 existe? \u2500\u2500\u2500\"; ls -la docs/bok/marketing-hub/ 2>/dev/null || echo \"(n\u00e3o existe \u2014 ser\u00e1 criado)\"",
  "description": "List bok-scribe templates + check target dir"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── templates dir ───
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
> ─── marketing-hub dir já existe? ───
> (não existe — será criado)
> ```

## 🤖 Claude *(00:32:18)*


## 🤖 Claude *(00:32:20)*

Workflow de 7 fases carregado. É um esforço grande (9 docs sequenciais, ~2000-2500 LOC como as suítes anteriores), com encadeamento de rastreabilidade MR→BR→PR→FR. Vou autorar sequencialmente (o skill proíbe pular fases). Carrego os 9 templates de uma vez para planejar o ID space coerente, e preparo o tracking de progresso.

## 🤖 Claude *(00:32:21)*


🛠️ **Tool Call**: `ToolSearch`
```json
{
  "query": "select:TaskCreate,TaskUpdate",
  "max_results": 5
}
```

> **Tool Result (ToolSearch)** - ✅ Success
>
> ```
> [{'type': 'tool_reference', 'tool_name': 'TaskCreate'}, {'type': 'tool_reference', 'tool_name': 'TaskUpdate'}]
> ```

## 🤖 Claude *(00:32:22)*


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

## 🤖 Claude *(00:32:23)*


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

## 🤖 Claude *(00:32:23)*


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

> **Tool Result (Unknown Tool)** - ✅ Success
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

## 🤖 Claude *(00:32:24)*


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

## 🤖 Claude *(00:32:25)*


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

## 🤖 Claude *(00:32:25)*


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

## 🤖 Claude *(00:32:26)*


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

## 🤖 Claude *(00:32:26)*


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

## 🤖 Claude *(00:32:27)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/08-quality-metrics.md"
}
```

## 🤖 Claude *(00:32:58)*


## 🤖 Claude *(00:33:00)*

All 9 templates loaded + full 7-phase workflow understood. Locking the inputs and the `-MH` ID space, then authoring sequentially (traceability MR-MH → BR-MH → PR-MH → FR-MH must chain). Setting up progress tracking and the output dir.

**Inputs derived:** slug `marketing-hub` · segment **B2B2C** · monetization **hybrid** · regulatory **LGPD** (PII de lead → CISSP elevado) · surface **extends-mcorch** (absorve v1).

## 🤖 Claude *(00:33:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "mkdir -p docs/bok/marketing-hub && echo \"\u2705 docs/bok/marketing-hub/ criado\" && ls -la docs/bok/marketing-hub/",
  "description": "Create marketing-hub BoK output directory"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✅ docs/bok/marketing-hub/ criado
> total 8
> drwxrwxr-x  2 ubuntu ubuntu 4096 Jun  2 21:33 .
> drwxrwxr-x 15 ubuntu ubuntu 4096 Jun  2 21:33 ..
> ```

## 🤖 Claude *(00:33:04)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Phase 1 \u2014 MRD + BRD (BABOK v3)",
  "description": "Author 01-mrd.md (market problem, TAM/SAM/SOM, competitive landscape HubSpot/Salesforce/RD Station, MR-MH-NNN) and 02-brd.md (BO-MH SMART, stakeholders, BR-MH traced to MR, ROI, mcoCoins economics, risk register) for docs/bok/marketing-hub/.",
  "activeForm": "Authoring MRD + BRD (BABOK)"
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #1 created successfully: Phase 1 — MRD + BRD (BABOK v3)
> ```

## 🤖 Claude *(00:33:06)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Phase 2 \u2014 PRD (ProdBOK + CXBOK)",
  "description": "Author 03-prd.md \u2014 product vision, 2+ personas (Usu\u00e1rio Zero operator + per-tenant marketer), journey maps, MoSCoW feature inventory (PR-MH traced to BR-MH), MVP/v1/future phasing, luxury UX, Gherkin AC.",
  "activeForm": "Authoring PRD (ProdBOK + CXBOK)"
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #2 created successfully: Phase 2 — PRD (ProdBOK + CXBOK)
> ```

> **Tool Result (Unknown Tool)** - ✅ Success
>
> ```
> Task #6 created successfully: Phase 6+7 — Traceability validation + Mesh seal
> ```

## 🤖 Claude *(00:33:08)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Phase 3 \u2014 FRD + SDD (SWEBOK + CISSP)",
  "description": "Author 04-frd.md (FR-MH/NFR-MH traced to PR-MH, interface contracts, test strategy) and 05-sdd.md (architecture, component catalog reusing mesh/ROI/credentials, STRIDE threat model, RLS, secrets inventory, migration stubs, OTD-MH). Absorb whatsapp_leads.",
  "activeForm": "Authoring FRD + SDD (SWEBOK + CISSP)"
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #3 created successfully: Phase 3 — FRD + SDD (SWEBOK + CISSP)
> ```

## 🤖 Claude *(00:33:10)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Phase 4 \u2014 Data Model + Process Flow (DMBOK + BPM)",
  "description": "Author 06-data-model.md (conceptual/logical/physical schema for leads/campaigns/sequences/AEO, GraphRAG node+edge types, tenant isolation, absorb whatsapp_leads) and 07-process-flow.md (PROC-MH inventory, BPMN-lite, n8n blueprints, intent orchestrator, cron, SLA).",
  "activeForm": "Authoring Data Model + Process Flow (DMBOK + BPM)"
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #4 created successfully: Phase 4 — Data Model + Process Flow (DMBOK + BPM)
> ```

## 🤖 Claude *(00:33:12)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Phase 5 \u2014 Quality Metrics (CMQ/OE)",
  "description": "Author 08-quality-metrics.md \u2014 QO-MH, KPI dashboard, FMEA-MH (with RPN>100 actions), self-optimization loops, self-healing telemetry, SLA/SLO/SLI, PDCA, observability checklist.",
  "activeForm": "Authoring Quality Metrics (CMQ/OE)"
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #5 created successfully: Phase 5 — Quality Metrics (CMQ/OE)
> ```

## 🤖 Claude *(00:33:14)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "Phase 6+7 \u2014 Traceability validation + Mesh seal",
  "description": "Run cross-doc traceability validation (no orphans, RLS on every table, mcoCoins on AI FRs, FMEA RPN>100 has action), finalize 00-index.md status, author scripts/seed-marketing-hub-bok-seal.ts (SB_SECRET_KEY, DERIVES_FROM parent seal), present summary. Mesh INSERT gated on Sovereign GO.",
  "activeForm": "Validating traceability + sealing mesh"
}
```

## 🤖 Claude *(00:33:54)*


## 🤖 Claude *(00:33:55)*

Estrutura e tracking prontos. Marco o capítulo e começo a autoração — **Phase 0 (index) + Phase 1 (MRD + BRD)** nesta leva.

## 🤖 Claude *(00:33:56)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "BoK Scribe: marketing-hub",
  "summary": "Authoring the 9-doc BoK suite for the marketing-hub module (v2 consolidation) via /bok-scribe"
}
```

## 🤖 Claude *(00:33:57)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "1",
  "status": "in_progress"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "BoK Scribe: marketing-hub". Continue your current work.'}]
> ```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #1 status
> ```

## 🤖 Claude *(00:33:58)*


## 🤖 Claude *(00:33:59)*

Agora os 3 arquivos da leva (Phase 0 + Phase 1):

## 🤖 Claude *(00:34:26)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/00-index.md",
  "content": "# BoK Documentation Suite \u2014 marketing-hub\n\n**Generated:** 2026-06-02  \n**Version:** v0.1  \n**Agent:** MCORCH BoK Scribe Agent v1.0.0  \n**Sovereign:** Gabriel Zarattini\n\n---\n\n## Project Metadata\n\n| Field | Value |\n|-------|-------|\n| Business Idea | Marketing Hub agentic soberano \u2014 m\u00f3dulo v2 que consolida e escala as superf\u00edcies de marketing dispersas do MCORCH (orchestrate-content, marketing-growth Pantheon, whatsapp_leads, afiliados ML) em um sistema que **percebe \u2192 decide \u2192 executa \u2192 aprende** estrat\u00e9gias de growth com governan\u00e7a humana. N\u00facleo agn\u00f3stico interno (Usu\u00e1rio Zero) hoje, feature comercial per-tenant amanh\u00e3. |\n| Market Segment | B2B2C (MCORCH \u2192 tenants \u2192 audi\u00eancias) |\n| Monetization Model | Hybrid (assinatura por tier + mcoCoins por a\u00e7\u00e3o de marketing) |\n| Regulatory Profile | LGPD (PII de lead/contato; consent + erasure) + GDPR-ready |\n| Integration Surface | `extends-mcorch` (absorve v1; novo m\u00f3dulo soberano) |\n| Project Slug | `marketing-hub` |\n| Scope Lock | `.claude/context/marketing-hub-scope-lock-2026-06-02.md` |\n\n---\n\n## Document Registry\n\n| # | File | Document | BoK Applied | Status |\n|---|------|----------|-------------|--------|\n| 0 | `00-index.md` | Project Manifest | \u2014 | [x] complete |\n| 1 | `01-mrd.md` | Market Requirements Document | BABOK v3 | [x] complete |\n| 2 | `02-brd.md` | Business Requirements Document | BABOK v3 | [x] complete |\n| 3 | `03-prd.md` | Product Requirements Document | ProdBOK + CXBOK | [ ] pending |\n| 4 | `04-frd.md` | Functional Requirements Document | SWEBOK v4 | [ ] pending |\n| 5 | `05-sdd.md` | System Design Document | SWEBOK v4 + CISSP CBK | [ ] pending |\n| 6 | `06-data-model.md` | Data & Knowledge Model | DMBOK v2 | [ ] pending |\n| 7 | `07-process-flow.md` | Process & Automation Blueprint | BPM CBOK v4 | [ ] pending |\n| 8 | `08-quality-metrics.md` | Self-Optimization Specification | CMQ/OE BOK | [ ] pending |\n| + | `bok-agents-system--marketing-hub.md` | Agent System (\u22658 agents) | `/bok-agents-generator` | [ ] pending (post-scribe) |\n\n---\n\n## Traceability Chain (populated as documents are generated)\n\n```\nMR-MH-NNN  (market need)\n  \u2514\u2500\u2500 BR-MH-NNN  (business requirement)\n        \u2514\u2500\u2500 PR-MH-NNN  (product requirement / feature)\n              \u2514\u2500\u2500 FR-MH-NNN  (functional requirement)\n                    \u2514\u2500\u2500 [DB table | Edge Function | n8n Process | Agent]\n```\n\n**ID space:** `MR-MH` \u00b7 `BR-MH` \u00b7 `BO-MH` \u00b7 `SH-MH` \u00b7 `PR-MH` \u00b7 `FR-MH` \u00b7 `NFR-MH` \u00b7 `PROC-MH` \u00b7 `KPI-MH` \u00b7 `FMEA-MH` \u00b7 `SOL-MH` \u00b7 `QO-MH` \u00b7 `BAC-MH` \u00b7 `OTD-MH`\n\n---\n\n## Phase Completion Log\n\n| Phase | Name | Completed | Notes |\n|-------|------|-----------|-------|\n| 0 | Project Bootstrap | 2026-06-02 | Slug `marketing-hub`; dir created; scope-lock anchored |\n| 1 | Market & Business Intelligence | 2026-06-02 | MRD (12 MR-MH) + BRD (12 BR-MH, 5 BO-MH) |\n| 2 | Product Definition | [ ] | \u2014 |\n| 3 | Technical Specification | [ ] | \u2014 |\n| 4 | Data & Process Engineering | [ ] | \u2014 |\n| 5 | Quality & Autonomic Engineering | [ ] | \u2014 |\n| 6 | Traceability Validation | [ ] | \u2014 |\n| 7 | Knowledge Mesh Injection | [ ] | \u2014 |\n\n---\n\n## Reuse vs Delta (anchored to scope-lock)\n\n**REUTILIZAR (referenciar, n\u00e3o reconstruir):** `mcorch_nodes`/`mcorch_edges` + pgvector HNSW 768d (Data Core/RAG) \u00b7 `infra_health_logs` + `ROIWidget` + `affiliate_links.revenue_cents` + `ATTRIBUTES_REVENUE_TO` (Observability/Attribution) \u00b7 edge functions + credenciais per-user (`user_api_keys`/`affiliate_config`/`social_credentials`/`meta_config`) + n8n (Connectivity) \u00b7 `mcorch-qa-healing` (Auto-cura) \u00b7 Pantheon `marketing-growth` L1 (Agentic).\n\n**CONSTRUIR (delta \u2014 foco do BoK):** (1) camada CRM/Lead completa (scoring + nurturing + customer 360, absorve `whatsapp_leads`); (2) AEO; (3) campaign management de 1\u00aa classe; (4) buyer intent + enrichment; (5) email/multicanal sequences; (6) orquestrador event-driven por inten\u00e7\u00e3o (policy engine + HITL + arbitragem).\n\n---\n\n## Open Technical Decisions\n\n| OTD ID | Description | Options | Recommendation | Status |\n|--------|-------------|---------|----------------|--------|\n| OTD-MH-001 | Tutela de `whatsapp_leads` (hoje sob BoK `meta-api`) | A: migrar p/ `marketing-hub`; B: deixar em `meta-api` e referenciar | A \u2014 consolidar no Lead Core (com nota de drift no BoK `meta-api`) | Open (Phase 3) |\n| OTD-MH-002 | Execu\u00e7\u00e3o dos agentes do delta (AEO/Intent/Demand-gen) | A: edge functions dedicadas; B: overlay no Pantheon OpenClaw; C: h\u00edbrido | C \u2014 orquestrador no MCORCH + racioc\u00ednio no Pantheon | Open (Phase 3) |\n| OTD-MH-003 | Provider de sinal AEO (visibilidade em motores de resposta) | A: scraping pr\u00f3prio; B: API 3rd-party; C: prompts amostrais a LLMs | Decidir no SDD ap\u00f3s probe-first (Lei 1) | Open (Phase 3) |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/00-index.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:34:28)*


## 🤖 Claude *(00:35:41)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/01-mrd.md",
  "content": "# MRD \u2014 Market Requirements Document\n\n**Project:** marketing-hub  \n**Version:** v0.1 | **Date:** 2026-06-02  \n**BoK Applied:** BABOK v3 (Strategy Analysis + Elicitation & Collaboration)  \n**Status:** Complete\n\n---\n\n## 1. Executive Summary\n\nO mercado de automa\u00e7\u00e3o de marketing est\u00e1 passando por duas rupturas simult\u00e2neas: (a) a **colapso do SEO cl\u00e1ssico** sob motores de resposta de IA (ChatGPT, Perplexity, Google AI Overviews, Gemini) \u2014 a descoberta migra de \"10 links azuis\" para \"uma resposta sintetizada\", exigindo **Answer Engine Optimization (AEO)**; e (b) a transi\u00e7\u00e3o de **copilotos bolt-on** para **plataformas verdadeiramente agentic** que percebem, decidem, executam e aprendem. As su\u00edtes l\u00edderes (HubSpot Marketing Hub, Salesforce Marketing Cloud) s\u00e3o poderosas mas caras, complexas e tratam IA como camada anexada, n\u00e3o como n\u00facleo. O MCORCH j\u00e1 possui gera\u00e7\u00e3o de conte\u00fado, malha de conhecimento (GraphRAG) e atribui\u00e7\u00e3o de afiliados \u2014 o que falta \u00e9 uma **camada de marketing coesa, AI-native e governada** que una captura de lead, scoring, nurturing, campanhas multicanal, AEO e atribui\u00e7\u00e3o num \u00fanico m\u00f3dulo soberano. O `marketing-hub` \u00e9 esse m\u00f3dulo: nasce consolidando as superf\u00edcies de marketing dispersas do MCORCH (v1) em um sistema v2 escal\u00e1vel, agn\u00f3stico por dentro (roda o growth do Usu\u00e1rio Zero hoje) e comercializ\u00e1vel per-tenant amanh\u00e3.\n\n---\n\n## 2. Market Problem Statement\n\n### 2.1 Current State\n\n**No mercado:** o operador de marketing de uma SMB/criador/ag\u00eancia hoje opera um patchwork de ferramentas desconectadas \u2014 um gerador de conte\u00fado aqui, um agendador social ali, uma planilha de leads, um ESP de email, um encurtador de afiliado, um painel de analytics \u2014 sem orquestra\u00e7\u00e3o unificada nem mem\u00f3ria entre elas. Cada ferramenta cobra \u00e0 parte, exige integra\u00e7\u00e3o manual e nenhuma \"percebe \u2192 decide \u2192 age\" de forma aut\u00f4noma. A chegada da busca por IA tornou a visibilidade ainda mais opaca: a marca n\u00e3o sabe se \u00e9 citada nas respostas geradas, nem como influenciar isso.\n\n**No MCORCH (estado interno atual):** a capacidade de marketing existe, mas **dispersa e sem ciclo de vida**:\n- `orchestrate-content` \u2014 pipeline **single-shot** (gera artigo + social + imagem + publica), sem no\u00e7\u00e3o de campanha cont\u00ednua, sequ\u00eancia ou nurturing.\n- `marketing-growth` (Pantheon L1) \u2014 agente de racioc\u00ednio sem superf\u00edcie de execu\u00e7\u00e3o transacional pr\u00f3pria.\n- `whatsapp_leads` (migration `20260531200000`) \u2014 **semente** de captura de lead, sem scoring, sem nurturing, sem UI, pendurada no BoK `meta-api`.\n- Afiliados ML (`affiliate_links`, `process-affiliate-link`, ROI via `revenue_cents`/`ATTRIBUTES_REVENUE_TO`) \u2014 atribui\u00e7\u00e3o existe **s\u00f3** para o canal de afiliado, n\u00e3o para campanhas/leads.\n\n### 2.2 Root Cause Analysis\n\n| Gap | Tipo | Por que persiste |\n|-----|------|------------------|\n| Marketing fragmentado em ferramentas isoladas | Market gap | Nenhum incumbente nasceu AI-agentic-native; todos retrofittam copilotos sobre arquiteturas CRUD legadas |\n| Sem ciclo de vida de lead no MCORCH | Process gap | O projeto priorizou gera\u00e7\u00e3o+publica\u00e7\u00e3o (topo de funil) e monetiza\u00e7\u00e3o por afiliado, nunca a camada CRM/meio-de-funil |\n| Invisibilidade em motores de resposta de IA | Technology gap | AEO \u00e9 categoria nascente (~2024+); tooling maduro inexiste; incumbentes apenas come\u00e7am (HubSpot AEO 2025) |\n| Atribui\u00e7\u00e3o parcial (s\u00f3 afiliado) | Data gap | `ATTRIBUTES_REVENUE_TO` cobre o postback ML; n\u00e3o h\u00e1 modelo de atribui\u00e7\u00e3o por campanha/canal/touchpoint |\n\n### 2.3 Desired State\n\nUm operador (Usu\u00e1rio Zero ou, futuramente, um tenant) define uma **inten\u00e7\u00e3o** (\"aumentar convers\u00f5es de lead em 20%\", \"lan\u00e7ar campanha do produto X\") e o `marketing-hub` decomp\u00f5e isso em tarefas, aciona os agentes certos (captura, scoring, nurturing, conte\u00fado, AEO, distribui\u00e7\u00e3o), executa com checkpoints de aprova\u00e7\u00e3o humana onde o impacto \u00e9 alto, atribui a receita de volta \u00e0 campanha/lead, e **aprende** com o resultado \u2014 tudo dentro de uma \u00fanica superf\u00edcie governada por LGPD, com mem\u00f3ria na malha GraphRAG e economia em mcoCoins.\n\n---\n\n## 3. Target Market Segments\n\n| Segment | Description | Size Estimate | Urgency | Accessibility |\n|---------|-------------|---------------|---------|---------------|\n| Primary | Criadores/solo-operators & micro-SMBs monetizando conte\u00fado + afiliados (o ICP atual do MCORCH; come\u00e7a no Usu\u00e1rio Zero) | ~Centenas de milhares BR/LatAm | High | Alta \u2014 j\u00e1 dentro do funil MCORCH |\n| Secondary | Ag\u00eancias de marketing & SaaS SMBs querendo automa\u00e7\u00e3o AI-native white-label per-tenant | Dezenas de milhares BR/LatAm | Medium | M\u00e9dia \u2014 exige prontid\u00e3o multi-tenant + onboarding |\n\n### 3.1 TAM / SAM / SOM\n\n> \u26a0\ufe0f Estimativas de ordem de grandeza (basis declarado); refinar com dados de mercado reais antes de decis\u00f5es de investimento (OTD de pesquisa).\n\n| Metric | Value | Basis |\n|--------|-------|-------|\n| TAM (Total Addressable Market) | ~US$ 25\u201330 bi/ano (global marketing automation, CAGR ~12\u201317%) | Relat\u00f3rios p\u00fablicos de mercado de marketing automation (ordem de grandeza) |\n| SAM (Serviceable Addressable Market) | ~US$ 1\u20132 bi/ano | Recorte BR/LatAm SMB + creator-economy marketing AI-native |\n| SOM (Serviceable Obtainable Market, 24m) | ~US$ 1\u20135 mi/ano | Base de tenants MCORCH alcan\u00e7\u00e1vel p\u00f3s-multi-tenant readiness; ancorado no Million-BRL Roadmap |\n\n---\n\n## 4. Competitive Landscape\n\n| Competitor | Positioning | Strengths | Weaknesses | Our Differentiation |\n|------------|-------------|-----------|------------|---------------------|\n| HubSpot Marketing Hub (+ Breeze, AEO) | Su\u00edte all-in-one SMB\u2192mid-market | Ecossistema maduro, Breeze Agents, AEO pioneiro | Caro em escala, IA bolt-on, lock-in, sem BYO-model real | AI-agentic-native, BYO-AI-models, mcoCoins pay-per-action, dados soberanos |\n| Salesforce Marketing Cloud (+ Agentforce, Data Cloud) | Enterprise, data-first | Agentforce, Data Cloud Zero-Copy, escala | Complexidade/custo enterprise, overkill p/ SMB/creator | Leveza, foco creator/SMB, malha GraphRAG nativa, self-host |\n| RD Station (l\u00edder BR) | Marketing+CRM SMB Brasil | Forte no BR, LGPD-aware, pre\u00e7o acess\u00edvel | IA incipiente, sem AEO, sem agentic real | N\u00facleo agentic + AEO + atribui\u00e7\u00e3o por malha |\n| ActiveCampaign / Mailchimp | Email + automation | Sequ\u00eancias maduras, barato p/ entrar | Centrado em email, IA limitada, sem AEO/agentic | Orquestra\u00e7\u00e3o multicanal por inten\u00e7\u00e3o, n\u00e3o s\u00f3 email |\n| DIY (n8n + ChatGPT + planilhas) | Stack montado \u00e0 m\u00e3o | Flex\u00edvel, barato | Sem governan\u00e7a, sem mem\u00f3ria, fr\u00e1gil, n\u00e3o-escal\u00e1vel | Mesma flexibilidade COM governan\u00e7a, mem\u00f3ria e self-healing |\n\n---\n\n## 5. Market Opportunity & Timing\n\n**Por que agora:** (1) **janela AEO** \u2014 a busca por IA est\u00e1 reescrevendo a descoberta agora (2025\u20132026); quem instrumentar visibilidade em motores de resposta cedo ganha vantagem composta. (2) **maturidade agentic** \u2014 modelos 2025+ tornam vi\u00e1vel o ciclo perceber\u2192decidir\u2192executar\u2192aprender com governan\u00e7a real. (3) **prontid\u00e3o do MCORCH** \u2014 a infra pesada (malha GraphRAG, embeddings, atribui\u00e7\u00e3o de afiliado, credenciais per-user, self-healing, mcoCoins) j\u00e1 existe e est\u00e1 provada em produ\u00e7\u00e3o; o `marketing-hub` capitaliza sobre ela em vez de construir do zero. (4) **press\u00e3o de custo** \u2014 SMBs/creators buscam alternativas mais baratas e soberanas \u00e0s su\u00edtes enterprise. (5) **LGPD como fosso** \u2014 soberania de dados + consentimento por design \u00e9 diferencial num mercado BR sens\u00edvel a privacidade.\n\n---\n\n## 6. Market Requirements\n\n> Priority: **Critical** (must have at launch) | **High** | **Medium** | **Low**\n\n| ID | Market Requirement | Priority | Rationale | Source |\n|----|-------------------|----------|-----------|--------|\n| MR-MH-001 | Ciclo de vida de lead unificado \u2014 capturar \u2192 qualificar (score) \u2192 nutrir \u2192 converter num s\u00f3 m\u00f3dulo, absorvendo `whatsapp_leads` | Critical | Meio-de-funil \u00e9 o gap central; sem ele n\u00e3o h\u00e1 \"marketing\", s\u00f3 publica\u00e7\u00e3o | An\u00e1lise interna + benchmark HubSpot/RD |\n| MR-MH-002 | Execu\u00e7\u00e3o agentic governada \u2014 perceber/decidir/executar/aprender com HITL em decis\u00f5es de alto impacto | Critical | Diferencial de categoria; evita automa\u00e7\u00e3o cega | Framework Sovereign \u00a74 |\n| MR-MH-003 | AEO \u2014 rastrear e otimizar visibilidade/cita\u00e7\u00e3o da marca em motores de resposta de IA | Critical | Janela de timing; SEO cl\u00e1ssico colapsa | Framework Sovereign \u00a71, \u00a76 |\n| MR-MH-004 | Campaign management de 1\u00aa classe \u2014 campanhas multicanal cont\u00ednuas (conte\u00fado+social+email+afiliado), al\u00e9m do single-shot | High | `orchestrate-content` n\u00e3o modela campanha/sequ\u00eancia | An\u00e1lise interna |\n| MR-MH-005 | Isolamento per-tenant de dados e credenciais (multi-tenant SaaS-ready; LGPD) | High | Pr\u00e9-requisito comercial + compliance | Diretiva API Tenancy + LGPD |\n| MR-MH-006 | Atribui\u00e7\u00e3o de receita e ROI por campanha/canal/touchpoint/tenant | High | Sem atribui\u00e7\u00e3o n\u00e3o h\u00e1 otimiza\u00e7\u00e3o de mix nem ROI prov\u00e1vel | Benchmark Salesforce/HubSpot |\n| MR-MH-007 | Buyer intent + data enrichment para prioriza\u00e7\u00e3o de leads | Medium | Foca esfor\u00e7o nos leads de maior probabilidade | Framework Sovereign \u00a73.1/3.3 |\n| MR-MH-008 | Sequ\u00eancias de nurturing email/multicanal (drip) | Medium | Mec\u00e2nica central de convers\u00e3o de meio-de-funil | Benchmark ActiveCampaign |\n| MR-MH-009 | BYO-AI-models (BYOK) per-tenant | Medium | Soberania de custo/quota + diferencia\u00e7\u00e3o | Diretiva API Tenancy + Framework \u00a72 |\n| MR-MH-010 | Governan\u00e7a \u2014 consentimento LGPD/GDPR, explicabilidade (XAI), trilha de auditoria | High | Compliance + confian\u00e7a; HITL precisa de rastreabilidade | LGPD + Framework \u00a76 |\n| MR-MH-011 | Auto-otimiza\u00e7\u00e3o e auto-cura das opera\u00e7\u00f5es de marketing | Medium | Resili\u00eancia em escala; reaproveita `mcorch-qa-healing` | Framework \u00a76 + CLAUDE.md |\n| MR-MH-012 | Customer 360 \u2014 perfil unificado do contato (eventos, canais, score, consentimento) | Medium | Base para personaliza\u00e7\u00e3o e atribui\u00e7\u00e3o | DMBOK + Framework \u00a73.3 |\n\n---\n\n## 7. Success Metrics (Market-Level KPIs)\n\n| KPI | Definition | Target (6-month) | Target (12-month) | Measurement |\n|-----|-----------|------------------|-------------------|-------------|\n| Active Marketing Tenants | Tenants rodando \u22651 campanha/m\u00eas | 1 (Usu\u00e1rio Zero) | 10+ | `campaigns` por `user_id` distinto |\n| Lead\u2192Conversion Rate (lift) | % de leads que convertem, vs. baseline | +10% sobre baseline | +25% | `leads` lifecycle status |\n| AEO Citation Presence | % de queries rastreadas em que a marca \u00e9 citada por um motor de resposta | \u2265 10% | \u2265 30% | `aeo_audits` |\n| NPS | Net Promoter Score do operador de marketing | \u2265 30 | \u2265 50 | Pesquisa in-app |\n| Attributed Revenue | Receita atribu\u00edda a campanhas (R$) | > 0 (primeiro real) | Ancorado ao Million-BRL Roadmap | `ATTRIBUTES_REVENUE_TO` + atribui\u00e7\u00e3o por campanha |\n\n---\n\n## 8. Regulatory & Compliance Context\n\n| Regulation | Applicability | Key Constraint | Compliance Owner |\n|------------|---------------|----------------|-----------------|\n| LGPD | **Alta** \u2014 leads/contatos s\u00e3o PII de titulares brasileiros | Base legal + consentimento granular para captura/nurturing; direito de elimina\u00e7\u00e3o (cascata no Customer 360); minimiza\u00e7\u00e3o | Engineering (Agente Ciberseguran\u00e7a) |\n| GDPR | Condicional \u2014 se houver titulares na UE | Consentimento + DSAR + transfer\u00eancia internacional | Engineering |\n| Email/Anti-spam (CAN-SPAM / CASL an\u00e1logos) | M\u00e9dia \u2014 sequ\u00eancias de email/multicanal | Opt-out obrigat\u00f3rio, identifica\u00e7\u00e3o do remetente, sem coleta enganosa | Engineering |\n| Marketing \u00e9tico / AI Governance | M\u00e9dia | Explicabilidade (XAI), monitoramento de vi\u00e9s, HITL em decis\u00f5es de alto impacto | Sovereign + Engineering |\n\n---\n\n## 9. Traceability Matrix Stub\n\n| MR ID | \u2192 BR ID | Rationale |\n|-------|---------|-----------|\n| MR-MH-001 | BR-MH-001 | Lead lifecycle core (absorve whatsapp_leads) |\n| MR-MH-002 | BR-MH-002 | Intent orchestrator + HITL policy engine |\n| MR-MH-003 | BR-MH-003 | AEO tracking + optimization |\n| MR-MH-004 | BR-MH-004 | Campaign entity + multi-channel dispatch |\n| MR-MH-005 | BR-MH-005 | Per-tenant RLS + credential resolution |\n| MR-MH-006 | BR-MH-006 | Attribution model (extends affiliate ROI) |\n| MR-MH-007 | BR-MH-007 | Enrichment + intent scoring |\n| MR-MH-008 | BR-MH-008 | Nurturing sequences engine |\n| MR-MH-009 | BR-MH-009 | BYOK per-tenant |\n| MR-MH-010 | BR-MH-010 | Consent + audit + XAI |\n| MR-MH-011 | BR-MH-011 | Self-healing telemetry |\n| MR-MH-012 | BR-MH-012 | Customer 360 unified profile |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/01-mrd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:35:45)*


## 🤖 Claude *(00:36:57)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/02-brd.md",
  "content": "# BRD \u2014 Business Requirements Document\n\n**Project:** marketing-hub  \n**Version:** v0.1 | **Date:** 2026-06-02  \n**BoK Applied:** BABOK v3 (Requirements Analysis & Design Definition)  \n**Status:** Complete\n\n---\n\n## 1. Executive Summary\n\nO `marketing-hub` traduz a oportunidade de mercado (MRD) em compromissos de neg\u00f3cio execut\u00e1veis. O objetivo de neg\u00f3cio central \u00e9 **consolidar as superf\u00edcies de marketing dispersas do MCORCH em um m\u00f3dulo soberano coeso** que (a) ative o ciclo de vida de lead completo, (b) instrumente AEO e atribui\u00e7\u00e3o, e (c) seja monetiz\u00e1vel per-tenant via mcoCoins, mantendo governan\u00e7a LGPD e o padr\u00e3o arquitetural Harness Engineering. O m\u00f3dulo nasce como **v2 de consolida\u00e7\u00e3o**: reutiliza a infra provada (malha GraphRAG, atribui\u00e7\u00e3o de afiliado, credenciais per-user, self-healing) e **absorve** `whatsapp_leads`, `orchestrate-content` (como executor de campanha) e o agente `marketing-growth` \u2014 sem duplic\u00e1-los nem deix\u00e1-los obsoletos em paralelo.\n\n---\n\n## 2. Business Objectives (SMART)\n\n| ID | Objective | Specific | Measurable | Achievable | Relevant | Time-bound |\n|----|-----------|----------|------------|------------|----------|------------|\n| BO-MH-001 | Consolidar marketing v1 \u2192 m\u00f3dulo \u00fanico | Unificar lead/campaign/atribui\u00e7\u00e3o numa superf\u00edcie `/dashboard/marketing` absorvendo whatsapp_leads + orchestrate-content | 1 m\u00f3dulo; 0 superf\u00edcies de marketing \u00f3rf\u00e3s | Reusa infra existente | Elimina fragmenta\u00e7\u00e3o (MR-MH-001/004) | v1.0 |\n| BO-MH-002 | Habilitar monetiza\u00e7\u00e3o per-tenant | Cobran\u00e7a em mcoCoins por a\u00e7\u00e3o de marketing (score, nurture-gen, AEO audit, campaign run) | \u2265 4 a\u00e7\u00f5es com custo definido; d\u00e9bito at\u00f4mico via RPC | Padr\u00e3o `deduct_mco_coins` j\u00e1 existe | Receita comercial (MR-MH-005) | v1.0 |\n| BO-MH-003 | Elevar convers\u00e3o de lead do Usu\u00e1rio Zero | Lead lifecycle + nurturing + scoring rodando E2E | Lift \u2265 +10% em 90d sobre baseline | Mec\u00e2nica padr\u00e3o de nurturing | Prova de valor antes de vender (MR-MH-001/008) | 90 dias p\u00f3s-v1.0 |\n| BO-MH-004 | Estabelecer presen\u00e7a AEO | Auditar e otimizar cita\u00e7\u00e3o da marca em motores de resposta de IA p/ queries rastreadas | Citation presence \u2265 10% em 6m | Provider de sinal AEO definido no SDD | Timing de mercado (MR-MH-003) | 6 meses p\u00f3s-v1.0 |\n| BO-MH-005 | Compliance LGPD multi-tenant | Consentimento granular + erasure em cascata + RLS per-tenant antes do 1\u00ba tenant externo | 100% das tabelas PII com RLS + consent + erasure | Reusa padr\u00e3o delete_account/LGPD existente | Pr\u00e9-requisito legal/comercial (MR-MH-010) | Antes do 1\u00ba tenant externo |\n\n---\n\n## 3. Stakeholder Register\n\n| ID | Role | Interest | Influence | Communication Cadence | Contact |\n|----|------|----------|-----------|----------------------|---------|\n| SH-MH-001 | Sovereign / Maestro | High | High | Continuous | Gabriel Zarattini |\n| SH-MH-002 | Usu\u00e1rio Zero (operator de marketing, prim\u00e1rio) | High | Medium | Per-sprint demo | Gabriel (conta produ\u00e7\u00e3o) |\n| SH-MH-003 | Tenant marketer (futuro, per-tenant) | High | Medium | Onboarding + NPS mensal | (p\u00f3s-comercial) |\n| SH-MH-004 | Lead / Contato (titular de dados LGPD) | High | Low | Consent UI + opt-out | (data subject) |\n| SH-MH-005 | Agente `marketing-growth` (Pantheon L1) | Medium | Medium | Mesh corpus di\u00e1rio | `~/.openclaw/agents/marketing-growth/` |\n| SH-MH-006 | Engineering (MCORCH Execution Agent) | High | High | Per-task | MCORCH Agent |\n\n---\n\n## 4. Business Requirements\n\n> Cada BR rastreia \u22651 MR. mcoCoins definido quando AI-powered. (n/a = sem custo direto de IA.)\n\n| ID | Requirement | MR Traced | Priority | mcoCoins Cost | Acceptance Criteria |\n|----|-------------|-----------|----------|---------------|---------------------|\n| BR-MH-001 | Lead Core \u2014 tabelas + hooks de ciclo de vida (capture\u2192score\u2192nurture\u2192convert), absorvendo `whatsapp_leads` | MR-MH-001 | Critical | n/a (CRUD) + score AI (BR-MH-007) | Lead criado, transiciona estados, RLS per-tenant; whatsapp_leads migrado sem perda |\n| BR-MH-002 | Intent Orchestrator \u2014 traduz inten\u00e7\u00e3o em tarefas de agentes, com policy engine + HITL | MR-MH-002 | Critical | n/a (orquestra; custo nas a\u00e7\u00f5es filhas) | Inten\u00e7\u00e3o \u2192 plano de tarefas; checkpoint humano em a\u00e7\u00e3o de alto impacto; arbitragem registrada |\n| BR-MH-003 | AEO Engine \u2014 auditar cita\u00e7\u00e3o da marca em motores de resposta + recomendar otimiza\u00e7\u00e3o | MR-MH-003 | Critical | 5 / audit | Audit roda p/ N queries; retorna citation score + recomenda\u00e7\u00f5es; persiste hist\u00f3rico |\n| BR-MH-004 | Campaign Core \u2014 entidade de campanha multicanal + dispatch (reusa orchestrate-content como executor) | MR-MH-004 | High | 10 / run (herda orchestrate-content) | Campanha agrupa canais+passos; run debita; status rastreado |\n| BR-MH-005 | Tenancy \u2014 RLS per-tenant + resolu\u00e7\u00e3o de credencial per-user (API Tenancy) | MR-MH-005 | High | n/a | Toda tabela PII RLS `auth.uid()`; credencial resolve per-user\u2192fallback documentado |\n| BR-MH-006 | Attribution \u2014 modelo de atribui\u00e7\u00e3o por campanha/canal/touchpoint (estende ROI de afiliado) | MR-MH-006 | High | n/a | Receita liga a campaign_id/lead_id; ROIWidget mostra por campanha |\n| BR-MH-007 | Lead Scoring + Enrichment \u2014 score por inten\u00e7\u00e3o/fit + enriquecimento de dados | MR-MH-007 | Medium | 1 / score \u00b7 3 / enrich | Score 0\u2013100 por lead; enrich preenche campos faltantes; fail-soft |\n| BR-MH-008 | Nurturing Sequences \u2014 engine de drip email/multicanal | MR-MH-008 | Medium | 2 / message-gen | Sequ\u00eancia dispara por trigger/step; respeita opt-out; idempotente |\n| BR-MH-009 | BYOK per-tenant \u2014 chaves de IA/canal por tenant | MR-MH-009 | Medium | n/a | Tenant configura chave pr\u00f3pria; resolve per-user\u2192sistema; cifrada no Vault |\n| BR-MH-010 | Governance \u2014 consentimento + trilha de auditoria + explicabilidade (XAI) | MR-MH-010 | High | n/a | Consent registrado por lead; decis\u00e3o agentic audit\u00e1vel c/ rationale; erasure cascateia |\n| BR-MH-011 | Self-Healing \u2014 telemetria + auto-recupera\u00e7\u00e3o das ops de marketing | MR-MH-011 | Medium | n/a | Eventos `infra_health_logs`; auto-heal via mega-brain-daemon; reusa mcorch-qa-healing |\n| BR-MH-012 | Customer 360 \u2014 perfil unificado (eventos, canais, score, consent) | MR-MH-012 | Medium | n/a | View 360 por contato; eventos multicanal agregados; PII RLS-protegida |\n\n---\n\n## 5. ROI Model\n\n### 5.1 Cost Estimates\n\n| Cost Item | Type | Monthly Estimate | Annual Estimate |\n|-----------|------|-----------------|----------------|\n| Infraestrutura (Supabase, Docker Mesh) | OpEx | Marginal (reusa stack existente) | ~Marginal |\n| Chamadas de IA (OpenRouter/BYOK \u2014 score, nurture-gen, AEO) | Variable | Proporcional ao volume; BYOK desloca custo ao tenant | Variable |\n| Enrichment / sinal AEO (provider 3rd-party, se OTD-MH-003=B) | Variable | A definir no SDD ap\u00f3s probe | A definir |\n| Desenvolvimento (inicial) | CapEx | \u2014 | Esfor\u00e7o de v1 (sprints) |\n\n### 5.2 Revenue Streams\n\n| Stream | Model | Monthly Potential | Notes |\n|--------|-------|-----------------|-------|\n| Assinatura per-tenant (tiers) | Subscription | Ancorado ao plano (Starter/Pro/Enterprise) | mcoCoins inclusos por tier |\n| mcoCoins por a\u00e7\u00e3o de marketing | Transaction | Proporcional ao uso (score/nurture/AEO/campaign) | D\u00e9bito at\u00f4mico via RPC |\n| Receita de afiliado atribu\u00edda | Indirect | Existente, agora atribu\u00edda por campanha | Reusa `ATTRIBUTES_REVENUE_TO` |\n\n### 5.3 Payback Analysis\n\n| Metric | Value |\n|--------|-------|\n| Break-even (months) | A modelar com pre\u00e7o de tier \u00d7 CAC (estimativa diferida \u2014 OTD de pricing) |\n| 12-month ROI | Ancorado ao Million-BRL Roadmap (marketing-growth & main) |\n| IRR (estimated) | Diferido at\u00e9 pricing definido |\n\n---\n\n## 6. mcoCoins Economics\n\n| Operation | Coins/Run | Plan Tier Mapping | Monthly Volume (est.) | Monthly Revenue (est.) |\n|-----------|-----------|-------------------|-----------------------|----------------------|\n| Lead score (AI) | 1 | Starter(500) / Pro(2000) / Ent(10k) | Alto (por lead) | Proporcional |\n| Lead enrichment | 3 | idem | M\u00e9dio | Proporcional |\n| Nurture message-gen (AI) | 2 | idem | Alto (por passo de sequ\u00eancia) | Proporcional |\n| AEO audit | 5 | idem | Baixo-m\u00e9dio (por ciclo) | Proporcional |\n| Campaign run | 10 | idem (herda `orchestrate-content`) | M\u00e9dio | Proporcional |\n\n> D\u00e9bito **sempre** via `deduct_mco_coins` RPC (at\u00f4mico, server-side). HTTP 402 em saldo insuficiente. Nunca dedu\u00e7\u00e3o client-side.\n\n---\n\n## 7. Constraints & Assumptions\n\n### Constraints\n- Harness Engineering obrigat\u00f3rio: l\u00f3gica em hooks; componentes display-only; ops sens\u00edveis em Edge Functions.\n- Toda integra\u00e7\u00e3o externa segue **API Tenancy Model \u2014 Per-User Credentials** (per-user \u2192 fallback documentado \u2192 hard-fail 402/501).\n- Toda migration nova passa `/security-review` antes do commit (FMEA-011).\n- Reutilizar infra existente (mesh/ROI/credenciais/self-heal); n\u00e3o reconstruir.\n- BoK Gate: nenhum c\u00f3digo antes desta su\u00edte selada (MRD\u2192SDD).\n\n### Assumptions\n- A infra reutilizada (GraphRAG, embeddings, atribui\u00e7\u00e3o de afiliado, Vault, mega-brain-daemon) permanece est\u00e1vel e dispon\u00edvel.\n- `whatsapp_leads` pode migrar de tutela `meta-api` \u2192 `marketing-hub` sem quebrar o `whatsapp-webhook` (validar em Phase 3 \u2014 OTD-MH-001).\n- Existe um sinal de AEO obten\u00edvel materialmente (a confirmar por probe \u2014 OTD-MH-003); se n\u00e3o, AEO v1 degrada para \"amostragem por prompts a LLMs\".\n- Multi-tenant comercial \u00e9 incremental: v1 foca Usu\u00e1rio Zero (interno) com ossatura per-tenant j\u00e1 pronta.\n\n---\n\n## 8. Business Risk Register\n\n| Risk ID | Description | Probability | Impact | RPN | Mitigation |\n|---------|-------------|-------------|--------|-----|------------|\n| BR-RISK-001 | Sinal de AEO n\u00e3o obten\u00edvel de forma confi\u00e1vel/barata | 3 | 4 | 12 | Probe-first (Lei 1) antes de codar; fallback p/ amostragem por prompt; AEO como \"Should\", n\u00e3o \"Must\" do MVP |\n| BR-RISK-002 | Vazamento cross-tenant de PII de lead (LGPD) | 2 | 5 | 10 | RLS default-deny + `/security-review` obrigat\u00f3rio + guard de tenant nas views (padr\u00e3o j\u00e1 provado) |\n| BR-RISK-003 | Sobreposi\u00e7\u00e3o/duplica\u00e7\u00e3o com orchestrate-content e meta-api (whatsapp_leads) | 3 | 3 | 9 | Absor\u00e7\u00e3o expl\u00edcita (BO-MH-001) + OTD-MH-001; orchestrate-content vira executor, n\u00e3o silo |\n| BR-RISK-004 | Automa\u00e7\u00e3o cega sem HITL gera dano de marca/or\u00e7amento | 2 | 4 | 8 | Policy engine + HITL obrigat\u00f3rio em a\u00e7\u00f5es de alto impacto (BR-MH-002) + audit trail |\n| BR-RISK-005 | Escopo \"universal\" inflar e nunca entregar | 3 | 4 | 12 | MoSCoW r\u00edgido no PRD; MVP = Lead Core + Campaign Core; resto faseado |\n| BR-RISK-006 | Custo de IA descontrolado por tenant | 2 | 3 | 6 | BYOK per-tenant (desloca custo) + mcoCoins gatekeeper + cap por a\u00e7\u00e3o |\n\n> Probability & Impact: 1=Low, 5=High. RPN = Probability \u00d7 Impact.\n\n---\n\n## 9. Business Acceptance Criteria\n\n| ID | Criterion | Verification Method |\n|----|-----------|-------------------|\n| BAC-MH-001 | Um lead percorre capture\u2192score\u2192nurture\u2192convert numa \u00fanica superf\u00edcie, RLS-isolado | E2E no `/dashboard/marketing` + REST count por user_id |\n| BAC-MH-002 | Toda a\u00e7\u00e3o AI-powered debita mcoCoins via RPC at\u00f4mico; 402 em saldo baixo | Material proof: `mcoin_transactions` + saldo before/after |\n| BAC-MH-003 | `whatsapp_leads` absorvido sem perda de dado nem quebra do webhook | Migration + contagem antes/depois + smoke do `whatsapp-webhook` |\n| BAC-MH-004 | AEO audit retorna citation score + recomenda\u00e7\u00f5es para queries rastreadas | Run real (ou degradado documentado) + persist\u00eancia |\n| BAC-MH-005 | Erasure de um lead cascateia em todas as tabelas PII (LGPD) | Delete + verifica\u00e7\u00e3o de zero res\u00edduo em todas as tabelas + Vault |\n| BAC-MH-006 | Receita atribu\u00edda aparece por campanha no ROIWidget | `ATTRIBUTES_REVENUE_TO` + campaign_id + leitura no widget |\n\n---\n\n## 10. Traceability Matrix\n\n| MR ID | BR ID | PR ID (stub) |\n|-------|-------|--------------|\n| MR-MH-001 | BR-MH-001 | _PRD_ |\n| MR-MH-002 | BR-MH-002 | _PRD_ |\n| MR-MH-003 | BR-MH-003 | _PRD_ |\n| MR-MH-004 | BR-MH-004 | _PRD_ |\n| MR-MH-005 | BR-MH-005 | _PRD_ |\n| MR-MH-006 | BR-MH-006 | _PRD_ |\n| MR-MH-007 | BR-MH-007 | _PRD_ |\n| MR-MH-008 | BR-MH-008 | _PRD_ |\n| MR-MH-009 | BR-MH-009 | _PRD_ |\n| MR-MH-010 | BR-MH-010 | _PRD_ |\n| MR-MH-011 | BR-MH-011 | _PRD_ |\n| MR-MH-012 | BR-MH-012 | _PRD_ |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/02-brd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:37:23)*


## 🤖 Claude *(00:37:23)*

Phase 1 (MRD+BRD) completa. Avanço para **Phase 2 — PRD**.

## 🤖 Claude *(00:37:23)*


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

## 🤖 Claude *(00:37:24)*


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

## 🤖 Claude *(00:38:33)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/03-prd.md",
  "content": "# PRD \u2014 Product Requirements Document\n\n**Project:** marketing-hub  \n**Version:** v0.1 | **Date:** 2026-06-02  \n**BoK Applied:** ProdBOK + CXBOK  \n**Status:** Complete\n\n---\n\n## 1. Product Vision Statement\n\n> Para **operadores de marketing** (do solo-creator ao tenant de ag\u00eancia) que est\u00e3o **afogados em ferramentas desconectadas e invis\u00edveis na nova busca por IA**, o **Marketing Hub** \u00e9 um **m\u00f3dulo de marketing agentic** que **percebe, decide, executa e aprende** estrat\u00e9gias de growth \u2014 captura e nutre leads, orquestra campanhas multicanal e otimiza visibilidade em motores de resposta de IA (AEO) \u2014 numa \u00fanica superf\u00edcie governada. Diferente do HubSpot/Salesforce (IA bolt-on, caro, lock-in), o nosso \u00e9 **AI-agentic-native, BYO-AI-models, soberano em dados (LGPD) e pay-per-action em mcoCoins**.\n\n---\n\n## 2. User Personas\n\n### Persona 1 \u2014 Gabriel / \"Usu\u00e1rio Zero\" (Primary)\n\n| Attribute | Detail |\n|-----------|--------|\n| Role | Solo operator/creator monetizando conte\u00fado + afiliados; \u00e9 o primeiro tenant (interno) |\n| Goals | Mais convers\u00f5es com menos malabarismo de ferramentas; ver o que de fato gera receita; aparecer nas respostas de IA |\n| Frustrations | Stack fragmentado; sem ciclo de vida de lead; atribui\u00e7\u00e3o s\u00f3 no afiliado; invis\u00edvel no ChatGPT/Perplexity |\n| Tech-savviness | 5 (expert \u2014 \u00e9 o arquiteto do MCORCH) |\n| MCORCH usage pattern | Power user: roda `orchestrate-content`, gerencia afiliados, opera a constela\u00e7\u00e3o; quer o Hub como cockpit \u00fanico |\n| Quote | _\"Eu n\u00e3o quero mais cinco abas abertas pra rodar uma campanha \u2014 quero declarar a inten\u00e7\u00e3o e ver o sistema agir, com eu aprovando o que importa.\"_ |\n\n### Persona 2 \u2014 Marina / Agency Marketer (Secondary, futuro per-tenant)\n\n| Attribute | Detail |\n|-----------|--------|\n| Role | Gerente de marketing numa ag\u00eancia que atende v\u00e1rias SMBs; futura tenant comercial |\n| Goals | Automa\u00e7\u00e3o AI-native white-label; isolamento por cliente; custo previs\u00edvel; compliance LGPD |\n| Frustrations | Su\u00edtes enterprise caras e complexas; sem BYO-model; medo de vazar dado entre clientes |\n| Tech-savviness | 3 (proficiente, n\u00e3o-engenheira) |\n| MCORCH usage pattern | Per-tenant: cria campanhas para m\u00faltiplos clientes finais; configura BYOK; vive no `/dashboard/marketing` |\n| Quote | _\"Preciso rodar marketing para 10 clientes sem misturar os dados de ningu\u00e9m e sem pagar uma fortuna por seat.\"_ |\n\n---\n\n## 3. User Journey Maps\n\n### Journey: \"Da inten\u00e7\u00e3o \u00e0 convers\u00e3o atribu\u00edda\" (Gabriel, Happy Path)\n\n| Stage | Action | Touchpoint | Emotion | Opportunity |\n|-------|--------|-----------|---------|-------------|\n| Awareness | Percebe que leads do WhatsApp morrem sem follow-up | `/dashboard/marketing` (Lead Board mostra leads parados) | \ud83d\ude10 Neutral | Surfacing de leads frios absorvidos do `whatsapp_leads` |\n| Consideration | Declara inten\u00e7\u00e3o \"nutrir e converter esses leads\" | Intent bar + Campaign Composer | \ud83e\udd14 Curious | Orquestrador prop\u00f5e plano de tarefas |\n| Activation | Aprova o plano; sequ\u00eancia de nurturing dispara | HITL approval card \u2192 sequence runs | \ud83d\ude0a Excited | Checkpoint humano transparente (XAI rationale) |\n| Value | Lead converte; receita aparece atribu\u00edda \u00e0 campanha | ROIWidget (por campanha) | \ud83d\ude80 Delighted | Atribui\u00e7\u00e3o que antes n\u00e3o existia fora do afiliado |\n| Retention | Hub sugere otimiza\u00e7\u00e3o (mover budget/canal, melhorar AEO) | Self-optimization insight card | \u2764\ufe0f Loyal | Loop de aprendizado que mant\u00e9m o operador no cockpit |\n\n#### Edge Case 1: Saldo de mcoCoins insuficiente no meio da campanha\n> Durante o run, o saldo cai abaixo do custo do pr\u00f3ximo passo. O sistema **pausa o passo** (n\u00e3o o cancela), debita 0, retorna HTTP 402 no passo, exibe toast PT-BR \"Saldo insuficiente \u2014 recarregue para continuar\", e preserva o estado da sequ\u00eancia para retomar p\u00f3s-recarga (idempotente). Nenhuma cobran\u00e7a parcial.\n\n#### Edge Case 2: Lead revoga consentimento durante o nurturing (LGPD)\n> O titular clica opt-out / solicita elimina\u00e7\u00e3o. O sistema **interrompe imediatamente** a sequ\u00eancia para aquele lead, marca `consent=withdrawn`, e (em erasure) cascateia a remo\u00e7\u00e3o de PII em todas as tabelas + segredos Vault associados. Nenhuma mensagem adicional \u00e9 enviada. Evento audit\u00e1vel registrado.\n\n---\n\n## 4. Feature Inventory (MoSCoW)\n\n> Effort: S=hours, M=days, L=week, XL=sprint\n\n### Must Have (MVP)\n\n| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |\n|----|---------|---------|-----------|--------|-------------|-------|\n| PR-MH-001 | Lead Lifecycle Board (capture\u2192score\u2192nurture\u2192convert) absorvendo `whatsapp_leads` | P1, P2 | BR-MH-001 | L | 0 (CRUD) | N\u00facleo do meio-de-funil; estados + RLS per-tenant |\n| PR-MH-002 | Lead Scoring (AI: inten\u00e7\u00e3o/fit 0\u2013100) | P1, P2 | BR-MH-007 | M | 1 | Server-side; fail-soft; d\u00e9bito at\u00f4mico |\n| PR-MH-003 | Campaign Composer + Run (wrap multicanal sobre `orchestrate-content`) | P1, P2 | BR-MH-004 | L | 10 | Campanha = canais+passos; herda executor existente |\n| PR-MH-004 | Consent & Tenancy Foundation (RLS, consent capture, erasure cascade) | P2, SH-MH-004 | BR-MH-005, BR-MH-010 | M | 0 | LGPD by design; pr\u00e9-requisito do resto |\n| PR-MH-005 | Campaign Attribution no ROIWidget (por campanha) | P1 | BR-MH-006 | M | 0 | Estende `ATTRIBUTES_REVENUE_TO` com campaign_id |\n\n### Should Have (v1.0)\n\n| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |\n|----|---------|---------|-----------|--------|-------------|-------|\n| PR-MH-010 | Nurturing Sequences (drip email/multicanal) | P1, P2 | BR-MH-008 | L | 2 / message-gen | Respeita opt-out; idempotente; trigger+step |\n| PR-MH-011 | Intent Orchestrator + HITL policy engine | P1 | BR-MH-002 | XL | 0 (orquestra) | Inten\u00e7\u00e3o\u2192plano; checkpoint humano; arbitragem |\n| PR-MH-012 | AEO Audit (cita\u00e7\u00e3o da marca em motores de resposta) | P1, P2 | BR-MH-003 | L | 5 / audit | Provider definido no SDD (OTD-MH-003); fallback amostral |\n| PR-MH-013 | Customer 360 view (eventos, canais, score, consent) | P1, P2 | BR-MH-012 | M | 0 | Agrega multicanal por contato |\n| PR-MH-014 | BYOK per-tenant (chaves de IA/canal de marketing) | P2 | BR-MH-009 | S | 0 | Padr\u00e3o Vault existente; per-user\u2192sistema |\n\n### Could Have (Future)\n\n| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |\n|----|---------|---------|-----------|--------|-------------|-------|\n| PR-MH-020 | Lead Enrichment (3rd-party data) | P2 | BR-MH-007 | M | 3 | Probe-first do provider; fail-soft |\n| PR-MH-021 | Self-Healing marketing ops (telemetria + auto-heal) | SH-MH-006 | BR-MH-011 | M | 0 | Reusa `mcorch-qa-healing` + mega-brain-daemon |\n| PR-MH-022 | A/B testing de campanhas/experi\u00eancias | P2 | BR-MH-004 | L | 0 | Variantes + signific\u00e2ncia |\n| PR-MH-023 | Agent System formalizado (\u22658 agentes via `/bok-agents-generator`) | P1 | BR-MH-002 | XL | 0 | Cat\u00e1logo operacional reconciliado com Pantheon |\n\n### Won't Have (This Cycle)\n\n- Portal de billing white-label completo per-tenant (cobran\u00e7a ao cliente final do tenant).\n- Compra/gest\u00e3o nativa de m\u00eddia paga (Google/Meta Ads spend management).\n- Gera\u00e7\u00e3o nativa de v\u00eddeo-ads al\u00e9m do Canvas Studio existente.\n\n---\n\n## 5. Release Phasing\n\n### MVP Scope\n**Target date:** sprint dedicada p\u00f3s-seal BoK  \n**Included:** PR-MH-001, PR-MH-002, PR-MH-003, PR-MH-004, PR-MH-005  \n**Success gate:** Um lead (absorvido do `whatsapp_leads`) percorre capture\u2192score\u2192campanha\u2192convers\u00e3o atribu\u00edda, RLS-isolado, com d\u00e9bito at\u00f4mico de mcoCoins e consentimento registrado (BAC-MH-001/002/003/005/006).  \n**New Edge Functions needed (explicit):** `lead-score` (AI scoring), `campaign-run` (orquestra `orchestrate-content` por campanha). Reusa: `orchestrate-content`, `deduct_mco_coins` RPC, `embed-mcorch-node`, ROI/attribution.\n\n### v1.0 Scope\n**Target date:** ap\u00f3s MVP validado com Usu\u00e1rio Zero  \n**Adds:** PR-MH-010, PR-MH-011, PR-MH-012, PR-MH-013, PR-MH-014  \n**Success gate:** Intent Orchestrator dispara nurturing com HITL; AEO audit roda (real ou degradado documentado); Customer 360 e BYOK per-tenant prontos para o 1\u00ba tenant externo.\n\n### Future Scope\n**Items:** PR-MH-020, PR-MH-021, PR-MH-022, PR-MH-023  \n**Condition:** Ap\u00f3s v1.0 est\u00e1vel e 1\u00ba tenant externo onboardado; PR-MH-023 dispara o `/bok-agents-generator` para formalizar o roster de agentes.\n\n---\n\n## 6. Luxury UX Specifications\n\n### 6.1 Color & Visual Identity\n\n| Token | Value | Usage |\n|-------|-------|-------|\n| `--bg-deep` | `#0A0A0F` | Canvas background |\n| `--accent-violet` | `#7C3AED` | Primary CTA, active states, intent bar |\n| `--accent-cyan` | `#06B6D4` | Lead score, attribution graphs |\n| `--glass-surface` | `rgba(255,255,255,0.04)` | Lead cards, campaign cards |\n| `--border-subtle` | `rgba(255,255,255,0.08)` | Card borders |\n\n### 6.2 Animation Guidelines\n\n| Element | Library | Duration | Easing |\n|---------|---------|----------|--------|\n| Lead card state transition (kanban move) | Framer Motion | 300ms | `easeInOut` |\n| HITL approval card entrance | Framer Motion | 300ms | `spring(stiffness:80)` |\n| Score pulse (live update) | CSS keyframes | 2s | `ease-in-out infinite` |\n| Micro-interactions (hover, toggles) | Framer Motion | 150ms | `easeOut` |\n\n### 6.3 Interaction Patterns\n\n- **Lead/Campaign cards:** Glass morphism \u2014 `backdrop-blur-sm`, borda sutil, shadow `0 4px 24px rgba(0,0,0,0.4)`.\n- **Intent bar:** campo de comando proeminente (violet); declarar inten\u00e7\u00e3o em linguagem natural.\n- **HITL approval:** card de aprova\u00e7\u00e3o com **rationale XAI vis\u00edvel** (por que o agente prop\u00f5e isso) + bot\u00f5es Aprovar/Ajustar/Recusar.\n- **Loading states:** skeleton shimmer (nunca spinner em \u00e1rea de conte\u00fado).\n- **Toasts:** `sonner`; sucesso = violet, erro = red, info = cyan; tudo em PT-BR.\n\n### 6.4 Accessibility (WCAG 2.1 AA)\n\n- Contraste \u2265 4.5:1 para texto sobre vidro.\n- Kanban e aprova\u00e7\u00f5es 100% naveg\u00e1veis por teclado.\n- ARIA labels em bot\u00f5es \u00edcone-only (mover lead, aprovar, opt-out).\n- Indicador de foco vis\u00edvel \u2265 2px.\n\n---\n\n## 7. Acceptance Criteria (Gherkin)\n\n```gherkin\nFeature: Lead lifecycle e campanha atribu\u00edda no Marketing Hub\n\n  Scenario: Lead absorvido \u00e9 qualificado e nutrido (PR-MH-001, PR-MH-002)\n    Given um lead existente capturado via whatsapp-webhook e absorvido pelo Lead Core\n    And o operador tem saldo de mcoCoins suficiente\n    When o operador aciona \"Qualificar\" no lead\n    Then o lead recebe um score 0\u2013100 calculado server-side\n    And 1 mcoCoin \u00e9 debitado via deduct_mco_coins RPC\n    And o lead \u00e9 isolado por RLS ao tenant (auth.uid())\n\n  Scenario: Campanha multicanal roda e atribui receita (PR-MH-003, PR-MH-005)\n    Given uma campanha composta com canais conte\u00fado + social\n    When o operador clica \"Run\" na campanha\n    Then 10 mcoCoins s\u00e3o debitados atomicamente\n    And orchestrate-content executa como executor da campanha\n    And a receita resultante liga-se ao campaign_id no ROIWidget\n\n  Scenario: Saldo insuficiente pausa sem cobrar (Edge Case 1)\n    Given uma sequ\u00eancia de nurturing em andamento\n    And o saldo cai abaixo do custo do pr\u00f3ximo passo\n    When o pr\u00f3ximo passo tenta executar\n    Then o passo \u00e9 pausado e retorna HTTP 402\n    And nenhum mcoCoin \u00e9 debitado no passo pausado\n    And um toast PT-BR \"Saldo insuficiente\" \u00e9 exibido\n\n  Scenario: Revoga\u00e7\u00e3o de consentimento interrompe e cascateia (Edge Case 2, PR-MH-004)\n    Given um lead em sequ\u00eancia de nurturing\n    When o titular revoga o consentimento\n    Then a sequ\u00eancia \u00e9 interrompida imediatamente para esse lead\n    And nenhuma mensagem adicional \u00e9 enviada\n    And em erasure a PII \u00e9 removida de todas as tabelas + segredos Vault\n```\n\n---\n\n## 8. Traceability Matrix\n\n| MR ID | BR ID | PR ID |\n|-------|-------|-------|\n| MR-MH-001 | BR-MH-001 | PR-MH-001 |\n| MR-MH-007 | BR-MH-007 | PR-MH-002, PR-MH-020 |\n| MR-MH-004 | BR-MH-004 | PR-MH-003, PR-MH-022 |\n| MR-MH-005, MR-MH-010 | BR-MH-005, BR-MH-010 | PR-MH-004 |\n| MR-MH-006 | BR-MH-006 | PR-MH-005 |\n| MR-MH-008 | BR-MH-008 | PR-MH-010 |\n| MR-MH-002 | BR-MH-002 | PR-MH-011, PR-MH-023 |\n| MR-MH-003 | BR-MH-003 | PR-MH-012 |\n| MR-MH-012 | BR-MH-012 | PR-MH-013 |\n| MR-MH-009 | BR-MH-009 | PR-MH-014 |\n| MR-MH-011 | BR-MH-011 | PR-MH-021 |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/03-prd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:38:47)*


## 🤖 Claude *(00:38:48)*

Phase 2 (PRD) completa. Avanço para **Phase 3 — FRD + SDD** (SWEBOK + CISSP; aqui o LGPD eleva as seções de segurança).

## 🤖 Claude *(00:38:49)*


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

## 🤖 Claude *(00:38:49)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "3",
  "status": "in_progress"
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #3 status
> ```

## 🤖 Claude *(00:39:41)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/04-frd.md",
  "content": "# FRD \u2014 Functional Requirements Document\n\n**Project:** marketing-hub  \n**Version:** v0.1 | **Date:** 2026-06-02  \n**BoK Applied:** SWEBOK v4 (Software Requirements)  \n**Status:** Complete\n\n---\n\n## 1. Scope Statement\n\nThis document specifies the functional and non-functional requirements for `marketing-hub`.\nIt is derived from PRD `03-prd.md` and feeds directly into SDD `05-sdd.md`.\n\n**In scope:** Lead lifecycle (capture\u2192score\u2192nurture\u2192convert) absorbing `whatsapp_leads`; campaign composition/run wrapping `orchestrate-content`; per-campaign attribution; consent + tenancy foundation (LGPD); nurturing sequences; intent orchestrator + HITL; AEO audit; Customer 360; BYOK per-tenant.\n\n**Out of scope (this cycle):** white-label billing portal; native paid-ads buying; multimodal video-ad generation beyond Canvas Studio; the formal agent catalog (deferred to `/bok-agents-generator`, PR-MH-023).\n\n---\n\n## 2. Functional Requirements\n\n> Category: `UI` | `Hook` | `EdgeFunction` | `DB` | `Cron`\n\n| ID | Title | Description | Priority | PR Traced | Category | Test ID |\n|----|-------|-------------|----------|-----------|----------|---------|\n| FR-MH-001 | Lead Lifecycle Board | Board/kanban exibindo leads por estado (`new`/`scored`/`nurturing`/`converted`/`lost`); transi\u00e7\u00f5es via hook `useLeads`; RLS per-tenant | Critical | PR-MH-001 | UI + Hook | AT-MH-001 |\n| FR-MH-002 | Absorb whatsapp_leads | Migration que traz `whatsapp_leads` ao Lead Core (tutela `meta-api`\u2192`marketing-hub`, OTD-MH-001); backfill sem perda; `whatsapp-webhook` continua escrevendo | Critical | PR-MH-001 | DB | AT-MH-002 |\n| FR-MH-003 | Lead Scoring Edge Fn | `lead-score`: JWT-guarded, debita 1 mcoCoin via RPC, chama IA (per-user\u2192sistema), grava `score` 0\u2013100, fail-soft | Critical | PR-MH-002 | EdgeFunction | AT-MH-003 |\n| FR-MH-004 | Campaign Run Edge Fn | `campaign-run`: JWT-guarded, debita 10 mcoCoins, orquestra `orchestrate-content` por passo de campanha, sincroniza status | Critical | PR-MH-003 | EdgeFunction | AT-MH-004 |\n| FR-MH-005 | Campaign Composer | UI para compor campanha (canais+passos) + `useCampaigns` hook; persiste em `campaigns`/`campaign_steps` | Critical | PR-MH-003 | UI + Hook | AT-MH-005 |\n| FR-MH-006 | Consent & Erasure | Captura de consentimento por lead; erasure cascade (todas tabelas PII + segredos Vault) via RPC `erase_lead()` SECURITY DEFINER | Critical | PR-MH-004 | DB + EdgeFunction | AT-MH-006 |\n| FR-MH-007 | Campaign Attribution | Liga receita a `campaign_id`/`lead_id`; estende `ATTRIBUTES_REVENUE_TO`; exp\u00f5e por campanha no `ROIWidget` | High | PR-MH-005 | Hook + DB | AT-MH-007 |\n| FR-MH-008 | Nurturing Sequences | Engine de drip: `sequences`+`sequence_enrollments`; passo dispara `nurture-dispatch` (gera msg, 2 mcoCoins); respeita opt-out; idempotente; cron avan\u00e7a passos | High | PR-MH-010 | EdgeFunction + Cron | AT-MH-008 |\n| FR-MH-009 | Intent Orchestrator + HITL | `intent-orchestrate`: traduz inten\u00e7\u00e3o\u2192plano de tarefas; policy engine decide auto vs. HITL; aprova\u00e7\u00e3o humana persiste rationale (XAI) | High | PR-MH-011 | EdgeFunction + Hook | AT-MH-009 |\n| FR-MH-010 | AEO Audit | `aeo-audit`: JWT-guarded, 5 mcoCoins, mede cita\u00e7\u00e3o da marca p/ queries rastreadas (provider OTD-MH-003), persiste `aeo_audits` + recomenda\u00e7\u00f5es | High | PR-MH-012 | EdgeFunction | AT-MH-010 |\n| FR-MH-011 | Customer 360 | View agregando eventos/canais/score/consent por contato; `useCustomer360` hook | Medium | PR-MH-013 | DB + Hook | AT-MH-011 |\n| FR-MH-012 | BYOK per-tenant | Colunas/credenciais de marketing per-tenant no padr\u00e3o Vault; resolve per-user\u2192sistema | Medium | PR-MH-014 | DB + UI | AT-MH-012 |\n\n---\n\n## 3. Non-Functional Requirements\n\n| ID | Category | Requirement | Target | Measurement |\n|----|----------|-------------|--------|-------------|\n| NFR-MH-001 | Performance | Lead Board load (LCP) | < 2.5s | Lighthouse CI |\n| NFR-MH-002 | Performance | Edge Fn p95 latency (score/campaign/aeo) | < 800ms (excl. IA externa) | Supabase logs |\n| NFR-MH-003 | Scalability | Leads por tenant sem degrada\u00e7\u00e3o de board | \u2265 10k leads/tenant (paginado) | Load test |\n| NFR-MH-004 | Availability | Uptime SLO do m\u00f3dulo | 99.5%/m\u00eas | Watchdog telemetry |\n| NFR-MH-005 | Maintainability | Complexidade ciclom\u00e1tica por hook | \u2264 10 | ESLint |\n| NFR-MH-006 | Security | Todo endpoint exige JWT v\u00e1lido; toda tabela PII RLS default-deny | 100% | `/security-review` |\n| NFR-MH-007 | Privacy (LGPD) | Erasure de lead cascateia em \u2264 24h; consent obrigat\u00f3rio antes de nurturing | 100% cascata; 0 envio sem consent | Auditoria + teste de erasure |\n| NFR-MH-008 | Cost discipline | Toda a\u00e7\u00e3o AI-powered debita via RPC at\u00f4mico; cap por a\u00e7\u00e3o | 0 dedu\u00e7\u00e3o client-side | Material proof (mcoin_transactions) |\n| NFR-MH-009 | Observability | Cada path (success/degraded/error) emite `infra_health_logs` | 100% dos edge fns | Telemetry audit |\n| NFR-MH-010 | Freshness (AEO) | Idade m\u00e1xima de um audit AEO antes de \"stale\" | \u2264 7 dias | `aeo_audits.created_at` |\n\n---\n\n## 4. Interface Requirements\n\n### 4.1 UI \u2192 Hook \u2192 Edge Function Contract\n\n```\n[Component: LeadBoard / CampaignComposer / HITLApprovalCard]\n  \u2193 calls\n[Hook: useLeads / useCampaigns / useIntentOrchestrator]\n  \u2193 calls (for sensitive ops)\n[Edge Function: lead-score / campaign-run / nurture-dispatch / intent-orchestrate / aeo-audit]\n  \u2193 reads/writes\n[Supabase Tables: leads / campaigns / sequences / aeo_audits / marketing_consents]\n```\n\n### 4.2 External API Contracts\n\n#### `POST /functions/v1/lead-score`\n\n**Auth:** Bearer JWT (user scope)  \n**Request:**\n```typescript\n{\n  lead_id: string,   // uuid do lead a pontuar\n  context?: string,  // sinal adicional opcional (campanha, origem)\n}\n```\n**Response (200):**\n```typescript\n{\n  status: 'ok',\n  lead_id: string,\n  score: number,          // 0\u2013100\n  rationale: string,      // XAI: por que esse score\n  new_balance: number,    // saldo mcoCoins p\u00f3s-d\u00e9bito\n}\n```\n**Error codes:**\n| Code | Condition |\n|------|-----------|\n| 401 | Missing or invalid JWT |\n| 402 | Insufficient mcoCoins balance |\n| 404 | Lead n\u00e3o encontrado / n\u00e3o pertence ao tenant |\n| 422 | Validation failure (campo + mensagem PT-BR) |\n| 500 | Internal error (logged to infra_health_logs) |\n\n#### `POST /functions/v1/campaign-run`\n\n**Auth:** Bearer JWT (user scope)  \n**Request:** `{ campaign_id: string }`  \n**Response (200):** `{ status: 'ok', campaign_id: string, run_id: string, steps_dispatched: number, new_balance: number }`  \n**Errors:** 401 / 402 / 404 / 422 / 500 (mesma sem\u00e2ntica acima).\n\n---\n\n## 5. Data Requirements\n\n| Field | Type | Nullable | Validation Rule | Error Message (PT-BR) |\n|-------|------|----------|-----------------|----------------------|\n| `leads.contact` | `text` | NOT NULL | E.164 (telefone) OU email v\u00e1lido | \"Contato inv\u00e1lido \u2014 informe telefone (E.164) ou email\" |\n| `leads.status` | `enum` | NOT NULL | \u2208 {new, scored, nurturing, converted, lost} | \"Status de lead inv\u00e1lido\" |\n| `leads.score` | `int2` | NULL | 0 \u2264 score \u2264 100 | \"Score deve estar entre 0 e 100\" |\n| `marketing_consents.basis` | `enum` | NOT NULL | \u2208 {consent, legitimate_interest, contract} | \"Base legal LGPD obrigat\u00f3ria\" |\n| `campaigns.name` | `text` | NOT NULL | 1\u2013120 chars | \"Nome da campanha \u00e9 obrigat\u00f3rio (1\u2013120)\" |\n| `aeo_audits.query` | `text` | NOT NULL | 1\u2013280 chars | \"Query de AEO obrigat\u00f3ria\" |\n\n---\n\n## 6. Test Strategy Matrix\n\n| FR ID | Unit Test | Integration Test | E2E Test | Notes |\n|-------|-----------|-----------------|----------|-------|\n| FR-MH-001 | \u2705 Required | \u2705 Required | \u2705 Required | Board states + RLS isolation |\n| FR-MH-002 | \u2705 Required | \u2705 Required | \u2014 | Migration backfill count before/after |\n| FR-MH-003 | \u2705 Required | \u2705 Required | \u2705 Required | Score + mcoCoins d\u00e9bito at\u00f4mico + 402 path |\n| FR-MH-004 | \u2705 Required | \u2705 Required | \u2705 Required | Campaign run orquestra orchestrate-content |\n| FR-MH-005 | \u2705 Required | \u2705 Required | \u2014 | Composer persist |\n| FR-MH-006 | \u2705 Required | \u2705 Required | \u2705 Required | Erasure cascade zero-residue (cr\u00edtico LGPD) |\n| FR-MH-007 | \u2705 Required | \u2705 Required | \u2014 | Attribution por campaign_id |\n| FR-MH-008 | \u2705 Required | \u2705 Required | \u2014 | Opt-out respeitado + idempot\u00eancia |\n| FR-MH-009 | \u2705 Required | \u2705 Required | \u2014 | Policy engine auto vs HITL |\n| FR-MH-010 | \u2705 Required | \u2014 | \u2014 | Provider real OU degradado documentado |\n| FR-MH-011 | \u2705 Required | \u2014 | \u2014 | 360 aggregation |\n| FR-MH-012 | \u2705 Required | \u2705 Required | \u2014 | BYOK resolve per-user\u2192sistema |\n\n**Test files location:**\n- Unit: `src/hooks/__tests__/useLeads.test.ts`, `useCampaigns.test.ts`, etc.\n- Integration: `src/__tests__/integration/marketing-hub.test.ts`\n- E2E: `e2e/marketing-hub.spec.ts`\n\n---\n\n## 7. Traceability Matrix\n\n| PR ID | FR ID | NFR ID |\n|-------|-------|--------|\n| PR-MH-001 | FR-MH-001, FR-MH-002 | NFR-MH-001, NFR-MH-006 |\n| PR-MH-002 | FR-MH-003 | NFR-MH-002, NFR-MH-008 |\n| PR-MH-003 | FR-MH-004, FR-MH-005 | NFR-MH-002, NFR-MH-008 |\n| PR-MH-004 | FR-MH-006 | NFR-MH-006, NFR-MH-007 |\n| PR-MH-005 | FR-MH-007 | NFR-MH-009 |\n| PR-MH-010 | FR-MH-008 | NFR-MH-007, NFR-MH-008 |\n| PR-MH-011 | FR-MH-009 | NFR-MH-005 |\n| PR-MH-012 | FR-MH-010 | NFR-MH-010 |\n| PR-MH-013 | FR-MH-011 | NFR-MH-003 |\n| PR-MH-014 | FR-MH-012 | NFR-MH-006 |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/04-frd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:39:44)*


## 🤖 Claude *(00:41:05)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/05-sdd.md",
  "content": "# SDD \u2014 System Design Document\n\n**Project:** marketing-hub  \n**Version:** v0.1 | **Date:** 2026-06-02  \n**BoK Applied:** SWEBOK v4 (Software Design) + CISSP CBK 2024 (Software Development Security)  \n**Status:** Complete  \n**Regulatory elevation:** LGPD \u2014 Security Design (\u00a75) and Erasure flows treated as Critical.\n\n---\n\n## 1. Architecture Overview\n\n```\n\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n\u2502  PRESENTATION LAYER (display-only)                                   \u2502\n\u2502  src/pages/MarketingHubPage.tsx  (/dashboard/marketing)             \u2502\n\u2502  src/components/marketing/{LeadBoard,CampaignComposer,              \u2502\n\u2502     HITLApprovalCard,AEODashboard,Customer360Panel}.tsx            \u2502\n\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n                       \u2502 calls\n\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25bc\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n\u2502  LOGIC LAYER (Harness Engineering \u2014 hooks)                          \u2502\n\u2502  useLeads \u00b7 useCampaigns \u00b7 useLeadScore \u00b7 useNurturing \u00b7           \u2502\n\u2502  useIntentOrchestrator \u00b7 useAEO \u00b7 useCustomer360 \u00b7 useMarketingConsent\u2502\n\u2502  src/store/useMarketingStore.ts (Zustand \u2014 intent/run/HITL state)  \u2502\n\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n                       \u2502 HTTP + JWT\n\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25bc\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n\u2502  EDGE LAYER (Deno / Supabase Functions)                             \u2502\n\u2502  lead-score \u00b7 campaign-run \u00b7 nurture-dispatch \u00b7 intent-orchestrate \u00b7\u2502\n\u2502  aeo-audit \u00b7 erase-lead   (each: JWT gate \u2192 mcoCoins RPC \u2192 logic)  \u2502\n\u2502  REUSES: orchestrate-content (campaign executor), embed-mcorch-node\u2502\n\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u252c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n           \u2502 Supabase RLS                       \u2502 External APIs / Pantheon\n\u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25bc\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510  \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25bc\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n\u2502  DB LAYER (per-tenant RLS)    \u2502  \u2502  EXTERNAL / AGENTIC               \u2502\n\u2502  leads \u00b7 lead_events \u00b7        \u2502  \u2502  OpenRouter (score/nurture/AEO IA) \u2502\n\u2502  campaigns \u00b7 campaign_steps \u00b7 \u2502  \u2502  AEO signal provider (OTD-MH-003) \u2502\n\u2502  sequences \u00b7 sequence_enroll \u00b7\u2502  \u2502  Enrichment provider (Could)      \u2502\n\u2502  aeo_audits \u00b7 marketing_consents\u2502 \u2502  marketing-growth Pantheon (reason)\u2502\n\u2502  marketing_attribution        \u2502  \u2502  n8n (sequence cron dispatch)     \u2502\n\u2502  mcorch_nodes (mesh)          \u2502  \u2502                                    \u2502\n\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518  \u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518\n```\n\n**Layer map (Harness Engineering):** componentes display-only \u2192 hooks (toda l\u00f3gica) \u2192 edge functions (ops sens\u00edveis + mcoCoins) \u2192 DB RLS-gated. Zustand s\u00f3 para estado de run/HITL/intent (n\u00e3o para dados remotos, que ficam em TanStack Query).\n\n---\n\n## 2. Component Catalog\n\n### 2.1 New Custom Hooks (`src/hooks/`)\n\n| Hook | File | Responsibility | TanStack Query keys |\n|------|------|---------------|---------------------|\n| `useLeads` | `useLeads.ts` | CRUD + state transitions de leads; absorve whatsapp_leads | `['leads', userId]` |\n| `useLeadScore` | `useLeadScore.ts` | Invoca `lead-score`; trata 402/404 | `['lead-score', leadId]` |\n| `useCampaigns` | `useCampaigns.ts` | Compose/list/run campanhas | `['campaigns', userId]` |\n| `useNurturing` | `useNurturing.ts` | Sequences + enrollments; opt-out | `['sequences', userId]` |\n| `useIntentOrchestrator` | `useIntentOrchestrator.ts` | Inten\u00e7\u00e3o\u2192plano; estado HITL | `['intent', userId]` |\n| `useAEO` | `useAEO.ts` | Dispara/l\u00ea audits AEO | `['aeo-audits', userId]` |\n| `useCustomer360` | `useCustomer360.ts` | Perfil 360 por contato | `['customer-360', contactId]` |\n| `useMarketingConsent` | `useMarketingConsent.ts` | Consent capture + erasure request | `['consent', leadId]` |\n\n### 2.2 New Display Components (`src/components/marketing/`)\n\n| Component | File | Props | Hook consumed |\n|-----------|------|-------|--------------|\n| `LeadBoard` | `marketing/LeadBoard.tsx` | `{ }` (reads hook) | `useLeads` |\n| `CampaignComposer` | `marketing/CampaignComposer.tsx` | `{ campaignId? }` | `useCampaigns` |\n| `HITLApprovalCard` | `marketing/HITLApprovalCard.tsx` | `{ plan }` | `useIntentOrchestrator` |\n| `AEODashboard` | `marketing/AEODashboard.tsx` | `{ }` | `useAEO` |\n| `Customer360Panel` | `marketing/Customer360Panel.tsx` | `{ contactId }` | `useCustomer360` |\n| `ConsentBadge` | `marketing/ConsentBadge.tsx` | `{ leadId }` | `useMarketingConsent` |\n\n### 2.3 New Edge Functions (`supabase/functions/`)\n\n| Function | Path | Auth | mcoCoins | Secrets needed |\n|----------|------|------|----------|----------------|\n| `lead-score` | `supabase/functions/lead-score/index.ts` | JWT (user) | 1 | per-user AI key (`user_api_keys`) \u2192 `OPENROUTER_API_KEY` |\n| `campaign-run` | `supabase/functions/campaign-run/index.ts` | JWT (user) | 10 | (reusa orchestrate-content secrets) |\n| `nurture-dispatch` | `supabase/functions/nurture-dispatch/index.ts` | JWT/service | 2 / message | per-user AI + channel creds (`social_credentials`/`meta_config`) |\n| `intent-orchestrate` | `supabase/functions/intent-orchestrate/index.ts` | JWT (user) | 0 (orquestra) | per-user AI key |\n| `aeo-audit` | `supabase/functions/aeo-audit/index.ts` | JWT (user) | 5 | per-user AI key + AEO provider key (OTD-MH-003) |\n| `erase-lead` | `supabase/functions/erase-lead/index.ts` | JWT (user) | 0 | service-role (cascade + Vault revoke) |\n\n> All new Edge Functions follow the **API Tenancy Model**: resolve per-user credential first, documented fallback only for service/cron paths, hard-fail 402/501 otherwise.\n\n### 2.4 Zustand Store Slices\n\n| Slice | Store file | State shape | Actions |\n|-------|------------|-------------|---------|\n| Marketing run/intent | `src/store/useMarketingStore.ts` | `{ activeIntent, plan, hitlQueue, runStatus }` | `setIntent`, `proposePlan`, `approveStep`, `rejectStep`, `syncRunStatus` |\n\n### 2.5 New DB Objects\n\n| Object | Type | Purpose | Migration file |\n|--------|------|---------|---------------|\n| `leads` | Table | Lead lifecycle (absorve whatsapp_leads) | `<ts>_marketing_hub_lead_core.sql` |\n| `lead_events` | Table | Eventos multicanal por lead (Customer 360) | idem |\n| `campaigns` | Table | Campanha multicanal | `<ts>_marketing_hub_campaigns.sql` |\n| `campaign_steps` | Table | Passos/canais da campanha | idem |\n| `sequences` | Table | Defini\u00e7\u00e3o de drip sequence | `<ts>_marketing_hub_sequences.sql` |\n| `sequence_enrollments` | Table | Inscri\u00e7\u00e3o de lead em sequ\u00eancia | idem |\n| `aeo_audits` | Table | Hist\u00f3rico de auditorias AEO | `<ts>_marketing_hub_aeo.sql` |\n| `marketing_consents` | Table | Consentimento LGPD por lead | `<ts>_marketing_hub_consent.sql` |\n| `marketing_attribution` | Table | Atribui\u00e7\u00e3o receita\u2192campaign/lead | `<ts>_marketing_hub_attribution.sql` |\n| `customer_360` | View | Perfil unificado por contato | `<ts>_marketing_hub_customer360_view.sql` |\n\n---\n\n## 3. Data Flow Diagrams\n\n### Use Case: Lead scoring (FR-MH-003)\n\n```\nUser                useLeadScore        lead-score Edge Fn      DB\n \u2502                    \u2502                     \u2502                    \u2502\n \u2502\u2500\u2500[Qualificar]\u2500\u2500\u2500\u2500\u2500\u25b6\u2502                     \u2502                    \u2502\n \u2502                    \u2502\u2500\u2500[POST JWT]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u25b6\u2502                    \u2502\n \u2502                    \u2502                     \u2502\u2500\u2500[getUser \u2192 401?]\u2500\u2500\u2502\n \u2502                    \u2502                     \u2502\u2500\u2500[deduct_mco_coins 1]\u25b6 profiles (RPC, 402 if low)\n \u2502                    \u2502                     \u2502\u25c0\u2500\u2500[ok]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502\n \u2502                    \u2502                     \u2502\u2500\u2500[AI score (per-user key)]\u25b6 OpenRouter\n \u2502                    \u2502                     \u2502\u25c0\u2500\u2500[score+rationale]\u2500\u2502\n \u2502                    \u2502                     \u2502\u2500\u2500[UPDATE leads.score]\u25b6 leads (RLS)\n \u2502                    \u2502                     \u2502\u2500\u2500[insert lead_event]\u25b6 lead_events\n \u2502                    \u2502                     \u2502\u2500\u2500[infra_health_logs pulse]\u25b6\n \u2502                    \u2502\u25c0\u2500\u2500[200 score]\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2502                    \u2502\n \u2502\u25c0\u2500\u2500[board updates]\u2500\u2500\u2502                     \u2502                    \u2502\n```\n\n### Use Case: Erasure (FR-MH-006, LGPD-critical)\n\n```\nUser/Subject \u2192 useMarketingConsent \u2192 erase-lead Edge Fn (service-role)\n   \u2192 DELETE leads + lead_events + sequence_enrollments + marketing_consents (cascade by lead_id)\n   \u2192 DELETE marketing_attribution rows referencing lead\n   \u2192 REVOKE any Vault secret tied to the lead (if BYOK channel token stored)\n   \u2192 insert infra_health_logs {event:'marketing_hub_lead_erased'}\n   \u2192 200 { erased: true, tables_cleared: [...] }\n```\n\n---\n\n## 4. API Contract Definitions\n\n> All Edge Functions must validate JWT before any business logic.\n\n### `POST /functions/v1/campaign-run`\n\n```typescript\n// Request\ninterface CampaignRunRequest {\n  campaign_id: string\n}\n\n// Response (HTTP 200)\ninterface CampaignRunResponse {\n  status: 'ok'\n  campaign_id: string\n  run_id: string\n  steps_dispatched: number\n}\n\n// mcoCoins deduction point:\n// \u2192 After JWT + ownership check, before dispatch:\n//   await supabase.rpc('deduct_mco_coins', { p_user_id, p_amount: 10 })\n// \u2192 HTTP 402 if insufficient balance\n// \u2192 Then per step: invoke('orchestrate-content', { ...stepPayload }) and sync status\n```\n\n### `POST /functions/v1/aeo-audit`\n\n```typescript\ninterface AeoAuditRequest { queries: string[]; brand: string }\ninterface AeoAuditResponse {\n  status: 'ok'\n  audit_id: string\n  citation_rate: number        // % queries citando a marca\n  findings: Array<{ query: string; cited: boolean; recommendation: string }>\n}\n// mcoCoins: deduct 5 at entry. Provider per OTD-MH-003; degraded mode documented if no provider.\n```\n\n---\n\n## 5. Security Design\n\n### 5.1 Threat Model (STRIDE)\n\n| Component | Threat | Type | Severity | Mitigation |\n|-----------|--------|------|----------|------------|\n| `lead-score` / all edge fns | Acesso n\u00e3o autenticado | Spoofing | High | JWT validation no entry point (getUser) |\n| `leads` / `marketing_consents` | Leitura cross-tenant de PII | Information Disclosure | **Critical** | RLS `user_id = auth.uid()` default-deny + guard de tenant nas views (padr\u00e3o provado) |\n| mcoCoins deduction | Bypass client-side | Tampering | Critical | RPC `deduct_mco_coins` server-side only |\n| `erase-lead` | Erasure de lead alheio | Elevation of Privilege | **Critical** | SECURITY DEFINER escopado a `auth.uid()`; double-bind por `lead_id`+owner (padr\u00e3o `disconnect_*`) |\n| Nurturing dispatch | Envio sem consentimento | Repudiation / Compliance | **Critical** | Gate de consent obrigat\u00f3rio pr\u00e9-envio; opt-out interrompe; audit trail |\n| BYOK marketing keys | Vazamento de token de canal | Information Disclosure | High | Padr\u00e3o Vault (cifra na trigger, view mascarada, `decrypted_*` service-role only) |\n| Intent Orchestrator | A\u00e7\u00e3o de alto impacto sem revis\u00e3o | Tampering | High | Policy engine + HITL obrigat\u00f3rio + rationale XAI audit\u00e1vel |\n| AEO provider call | Exfiltra\u00e7\u00e3o via prompt injection no sinal | Tampering | Medium | Sanitiza\u00e7\u00e3o de input; provider isolado; sem secret no prompt |\n\n### 5.2 RLS Policy Definitions\n\n```sql\n-- leads RLS (mesmo padr\u00e3o para lead_events, campaigns, sequences, aeo_audits, marketing_consents, marketing_attribution)\nALTER TABLE public.leads ENABLE ROW LEVEL SECURITY;\n\nCREATE POLICY \"leads_select_own\"\n  ON public.leads FOR SELECT\n  USING (user_id = auth.uid());\n\nCREATE POLICY \"leads_insert_own\"\n  ON public.leads FOR INSERT\n  WITH CHECK (user_id = auth.uid());\n\nCREATE POLICY \"leads_update_own\"\n  ON public.leads FOR UPDATE\n  USING (user_id = auth.uid())\n  WITH CHECK (user_id = auth.uid());\n-- DELETE n\u00e3o exposto ao cliente: erasure s\u00f3 via erase-lead (SECURITY DEFINER).\n```\n\n### 5.3 JWT Validation Points\n\nAll Edge Functions follow this pattern (cutover keys \u2014 ver `reference_supabase_keys_migrated`):\n```typescript\nconst authHeader = req.headers.get('Authorization')\nif (!authHeader) return new Response('Unauthorized', { status: 401 })\nconst supabase = createClient(SB_URL, SB_PUBLISHABLE_KEY ?? ANON_KEY)\nconst { data: { user }, error } = await supabase.auth.getUser(authHeader.replace('Bearer ', ''))\nif (error || !user) return new Response('Unauthorized', { status: 401 })\n// service-role client (SB_SECRET_KEY) only for privileged writes after the user is known\n```\n\n### 5.4 Secrets Inventory\n\n| Secret Name | Used In | Vault Location | Rotation Policy |\n|-------------|---------|----------------|----------------|\n| `OPENROUTER_API_KEY` (fallback) | score/nurture/aeo/intent | Supabase Vault | Per platform policy |\n| per-user AI keys (`user_api_keys`) | idem (prim\u00e1rio) | Vault (cifrado) | User-managed |\n| AEO provider key (se OTD-MH-003=B) | `aeo-audit` | Supabase Vault | Per provider |\n| channel creds (`social_credentials`/`meta_config`) | `nurture-dispatch` | Vault (cifrado) | User-managed / reauth |\n| `SB_SECRET_KEY` | service-role writes (erase, cron) | Function secret | Per `reference_supabase_keys_migrated` |\n\n> \u26a0\ufe0f NEVER commit secret values. Legacy `SUPABASE_SERVICE_ROLE_KEY`/`ANON_KEY` est\u00e3o **revogadas** \u2014 usar `SB_SECRET_KEY`/`SB_PUBLISHABLE_KEY` (cutover 2026-06-01).\n\n---\n\n## 6. Infrastructure Touchpoints\n\n| Infrastructure | Usage | Impact |\n|----------------|-------|--------|\n| `mcorch_chroma` (ChromaDB :8001) | Indireto via embed-mcorch-node (mesh) | Baixo |\n| `mega-brain-daemon` | Auto-heal de marketing ops (PR-MH-021) | Self-healing hook |\n| `infra_health_logs` | Novos eventos: `marketing_hub_*` | Watchdog telemetry |\n| `mcorch_nodes`/`mcorch_edges` | Observa\u00e7\u00e3o de campanha/lead na malha; `ATTRIBUTES_REVENUE_TO` por campaign | Mesh growth |\n| n8n | Cron de avan\u00e7o de sequ\u00eancias de nurturing | Automation |\n| `orchestrate-content` (reuse) | Executor de passo de campanha | Reuso (n\u00e3o duplica) |\n\n---\n\n## 7. Migration Stubs\n\n```sql\n-- Migration: <ts>_marketing_hub_lead_core.sql\n\nCREATE TABLE public.leads (\n  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,\n  user_id         uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,\n  project_id      uuid,  -- optional tenant project scope\n  contact         text NOT NULL,                 -- E.164 ou email (valida\u00e7\u00e3o na app)\n  source          text NOT NULL DEFAULT 'whatsapp',  -- whatsapp|form|import|api\n  status          text NOT NULL DEFAULT 'new',   -- new|scored|nurturing|converted|lost\n  score           int2 CHECK (score BETWEEN 0 AND 100),\n  intent_signal   jsonb DEFAULT '{}'::jsonb,\n  embedding       vector(768),\n  created_at      timestamptz NOT NULL DEFAULT now(),\n  updated_at      timestamptz NOT NULL DEFAULT now()\n);\n\nALTER TABLE public.leads ENABLE ROW LEVEL SECURITY;\n-- (RLS policies from \u00a75.2 \u2014 default deny; DELETE not client-exposed)\n\nCREATE INDEX leads_user_idx ON public.leads (user_id);\nCREATE INDEX leads_status_idx ON public.leads (user_id, status);\nCREATE INDEX leads_embedding_hnsw\n  ON public.leads USING hnsw (embedding vector_cosine_ops)\n  WITH (m = 16, ef_construction = 64);\n\nCREATE TRIGGER set_leads_updated_at\n  BEFORE UPDATE ON public.leads\n  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();\n\n-- Absorb whatsapp_leads (OTD-MH-001): backfill INSERT ... SELECT from whatsapp_leads,\n-- then point whatsapp-webhook to write into leads (source='whatsapp'). Drift note in meta-api BoK.\n```\n\n> Every migration passes `/security-review` before commit (FMEA-011). `marketing_consents`, `marketing_attribution`, `campaigns`, `sequences`, `aeo_audits` follow the same RLS-default-deny skeleton (see 06-data-model.md).\n\n---\n\n## 8. Open Technical Decisions\n\n| ID | Description | Option A | Option B | Recommendation | Owner |\n|----|-------------|----------|----------|----------------|-------|\n| OTD-MH-001 | Tutela de `whatsapp_leads` | Migrar p/ `marketing-hub` (leads.source='whatsapp') | Manter em `meta-api`, FK cross-module | **A** \u2014 consolidar; nota de drift no BoK `meta-api` | Sovereign |\n| OTD-MH-002 | Runtime dos agentes do delta (AEO/Intent/Demand-gen) | Edge functions dedicadas | Overlay no Pantheon OpenClaw | **C (h\u00edbrido)** \u2014 orquestra\u00e7\u00e3o no MCORCH (edge), racioc\u00ednio no Pantheon | Sovereign |\n| OTD-MH-003 | Provider de sinal AEO | Scraping pr\u00f3prio de AI engines | API 3rd-party de monitoramento AEO | **Probe-first (Lei 1)** antes de codar; fallback = amostragem por prompt a LLMs | Engineering |\n| OTD-MH-004 | Dispatch de nurturing | Cron n8n avan\u00e7a passos | pg_cron + edge | **A (n8n)** \u2014 reusa infra de automa\u00e7\u00e3o existente | Engineering |\n| OTD-MH-005 | Modelo de atribui\u00e7\u00e3o | Last-touch (simples) | Multi-touch ponderado | **A no MVP**, B faseado (PR-MH-022 contexto) | Sovereign |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/05-sdd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:41:17)*


## 🤖 Claude *(00:41:17)*

Phase 3 (FRD+SDD) completa. Avanço para **Phase 4 — Data Model + Process Flow** (DMBOK + BPM CBOK).

## 🤖 Claude *(00:41:18)*


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

## 🤖 Claude *(00:41:18)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "4",
  "status": "in_progress"
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #4 status
> ```

## 🤖 Claude *(00:42:23)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/06-data-model.md",
  "content": "# Data & Knowledge Model\n\n**Project:** marketing-hub  \n**Version:** v0.1 | **Date:** 2026-06-02  \n**BoK Applied:** DMBOK v2 (Data Modeling & Design + Data Quality)  \n**Status:** Complete\n\n---\n\n## 1. Conceptual Data Model\n\n```\n[lead] \u2500\u2500(1:N)\u2500\u2500\u25b6 [lead_event]\n   \u2502                  \n   \u251c\u2500\u2500(1:N)\u2500\u2500\u25b6 [sequence_enrollment] \u2500\u2500(N:1)\u2500\u2500\u25b6 [sequence]\n   \u2502\n   \u251c\u2500\u2500(1:1)\u2500\u2500\u25b6 [marketing_consent]\n   \u2502\n   \u2514\u2500\u2500(1:N)\u2500\u2500\u25b6 [marketing_attribution] \u2500\u2500(N:1)\u2500\u2500\u25b6 [campaign]\n                                                      \u2502\n                                          [campaign] \u2500\u2500(1:N)\u2500\u2500\u25b6 [campaign_step]\n                                                      \u2502\n                                          [campaign] \u2500\u2500(1:1)\u2500\u2500\u25b6 [mcorch_nodes] (campaign node)\n[aeo_audit] \u2500\u2500(N:1)\u2500\u2500\u25b6 [tenant/user]   (brand visibility snapshots)\n[customer_360]  =  VIEW(lead \u2a1d lead_event \u2a1d marketing_consent \u2a1d score)\n```\n\n**Entities:**\n- **lead:** contato capturado e seu ciclo de vida (absorve `whatsapp_leads`).\n- **lead_event:** evento multicanal por lead (mensagem, abertura, clique, convers\u00e3o) \u2014 base do Customer 360.\n- **campaign / campaign_step:** campanha multicanal e seus passos (cada passo aciona `orchestrate-content`).\n- **sequence / sequence_enrollment:** defini\u00e7\u00e3o de drip e inscri\u00e7\u00e3o de um lead nela.\n- **marketing_consent:** base legal + estado de consentimento LGPD por lead.\n- **marketing_attribution:** liga receita \u2192 campanha/lead/touchpoint.\n- **aeo_audit:** snapshot de cita\u00e7\u00e3o da marca em motores de resposta.\n- **customer_360:** VIEW de perfil unificado.\n\n---\n\n## 2. Logical Data Model\n\n### Table: `leads`\n\n| Column | Type | Nullable | Default | FK | Description |\n|--------|------|----------|---------|-----|------------|\n| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | \u2014 | Primary key |\n| `user_id` | `uuid` | NOT NULL | \u2014 | `auth.users.id` | Tenant isolation |\n| `project_id` | `uuid` | NULL | \u2014 | \u2014 | Optional project scope |\n| `contact` | `text` | NOT NULL | \u2014 | \u2014 | E.164 ou email (PII) |\n| `name` | `text` | NULL | \u2014 | \u2014 | Nome do lead (PII) |\n| `source` | `text` | NOT NULL | `'whatsapp'` | \u2014 | whatsapp\\|form\\|import\\|api |\n| `status` | `text` | NOT NULL | `'new'` | \u2014 | new\\|scored\\|nurturing\\|converted\\|lost |\n| `score` | `int2` | NULL | \u2014 | \u2014 | 0\u2013100 (lead scoring) |\n| `intent_signal` | `jsonb` | NULL | `'{}'` | \u2014 | Sinais de inten\u00e7\u00e3o/enrichment |\n| `embedding` | `vector(768)` | NULL | \u2014 | \u2014 | Neural embedding (busca sem\u00e2ntica de leads) |\n| `stability_score` | `float4` | NOT NULL | `0.5` | \u2014 | FSRS-6 (se promovido \u00e0 malha) |\n| `created_at` | `timestamptz` | NOT NULL | `now()` | \u2014 | Audit |\n| `updated_at` | `timestamptz` | NOT NULL | `now()` | \u2014 | Audit |\n\n### Table: `lead_events`\n\n| Column | Type | Nullable | Default | FK | Description |\n|--------|------|----------|---------|-----|------------|\n| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | \u2014 | Primary key |\n| `lead_id` | `uuid` | NOT NULL | \u2014 | `leads.id` | Parent (ON DELETE CASCADE) |\n| `user_id` | `uuid` | NOT NULL | \u2014 | `auth.users.id` | Tenant isolation (denormalizado p/ RLS) |\n| `channel` | `text` | NOT NULL | \u2014 | \u2014 | whatsapp\\|email\\|social\\|web |\n| `event_type` | `text` | NOT NULL | \u2014 | \u2014 | message_sent\\|opened\\|clicked\\|converted\\|opt_out |\n| `payload` | `jsonb` | NULL | `'{}'` | \u2014 | Dados do evento (sem PII excedente) |\n| `occurred_at` | `timestamptz` | NOT NULL | `now()` | \u2014 | Quando ocorreu |\n\n### Table: `campaigns`\n\n| Column | Type | Nullable | Default | FK | Description |\n|--------|------|----------|---------|-----|------------|\n| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | \u2014 | Primary key |\n| `user_id` | `uuid` | NOT NULL | \u2014 | `auth.users.id` | Tenant isolation |\n| `name` | `text` | NOT NULL | \u2014 | \u2014 | Nome (1\u2013120) |\n| `intent` | `text` | NULL | \u2014 | \u2014 | Inten\u00e7\u00e3o declarada que originou a campanha |\n| `channels` | `text[]` | NOT NULL | `'{}'` | \u2014 | content\\|social\\|email\\|affiliate |\n| `status` | `text` | NOT NULL | `'draft'` | \u2014 | draft\\|running\\|paused\\|done\\|error |\n| `mesh_node_id` | `uuid` | NULL | \u2014 | `mcorch_nodes.id` | N\u00f3 de campanha na malha |\n| `created_at` | `timestamptz` | NOT NULL | `now()` | \u2014 | Audit |\n| `updated_at` | `timestamptz` | NOT NULL | `now()` | \u2014 | Audit |\n\n### Table: `campaign_steps`\n\n| Column | Type | Nullable | Default | FK | Description |\n|--------|------|----------|---------|-----|------------|\n| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | \u2014 | Primary key |\n| `campaign_id` | `uuid` | NOT NULL | \u2014 | `campaigns.id` | Parent (CASCADE) |\n| `user_id` | `uuid` | NOT NULL | \u2014 | `auth.users.id` | RLS |\n| `position` | `int2` | NOT NULL | \u2014 | \u2014 | Ordem do passo |\n| `channel` | `text` | NOT NULL | \u2014 | \u2014 | Canal do passo |\n| `action` | `text` | NOT NULL | \u2014 | \u2014 | generate_content\\|publish\\|affiliate_attach |\n| `status` | `text` | NOT NULL | `'idle'` | \u2014 | idle\\|running\\|done\\|error\\|blocked |\n\n### Table: `sequences` / `sequence_enrollments`\n\n| `sequences` | Type | Notes |\n|-------------|------|-------|\n| `id` uuid PK \u00b7 `user_id` uuid \u00b7 `name` text \u00b7 `trigger` text (status_change\\|manual) \u00b7 `steps` jsonb (ordered drip steps) \u00b7 `active` bool \u00b7 audit |\n\n| `sequence_enrollments` | Type | Notes |\n|------------------------|------|-------|\n| `id` uuid PK \u00b7 `sequence_id` uuid FK \u00b7 `lead_id` uuid FK \u00b7 `user_id` uuid \u00b7 `current_step` int2 \u00b7 `status` text (active\\|paused\\|completed\\|opted_out) \u00b7 `next_run_at` timestamptz \u00b7 audit |\n\n### Table: `marketing_consents`\n\n| Column | Type | Nullable | Notes |\n|--------|------|----------|-------|\n| `id` uuid PK \u00b7 `lead_id` uuid FK (UNIQUE) \u00b7 `user_id` uuid \u00b7 `basis` text (consent\\|legitimate_interest\\|contract) \u00b7 `granted` bool \u00b7 `granted_at` timestamptz \u00b7 `withdrawn_at` timestamptz NULL \u00b7 `source_proof` jsonb (como/onde consentiu) | | NOT NULL chaves | Base legal LGPD por lead |\n\n### Table: `marketing_attribution`\n\n| Column | Type | Notes |\n|--------|------|-------|\n| `id` uuid PK \u00b7 `user_id` uuid \u00b7 `campaign_id` uuid FK NULL \u00b7 `lead_id` uuid FK NULL \u00b7 `touchpoint` text \u00b7 `revenue_cents` int4 \u00b7 `model` text (last_touch\\|multi_touch) \u00b7 `occurred_at` timestamptz | Liga receita a campanha/lead; espelha `affiliate_links.revenue_cents` |\n\n### Table: `aeo_audits`\n\n| Column | Type | Notes |\n|--------|------|-------|\n| `id` uuid PK \u00b7 `user_id` uuid \u00b7 `brand` text \u00b7 `query` text \u00b7 `cited` bool \u00b7 `citation_rate` float4 \u00b7 `engine` text (chatgpt\\|perplexity\\|google_ai\\|gemini) \u00b7 `recommendation` text \u00b7 `created_at` timestamptz | Snapshot de visibilidade em motores de resposta |\n\n---\n\n## 3. Supabase Physical Schema Stubs\n\n```sql\n-- ============================================================\n-- MIGRATION: <ts>_marketing_hub_lead_core.sql\n-- ============================================================\nCREATE TABLE public.leads (\n  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,\n  user_id         uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,\n  project_id      uuid,\n  contact         text NOT NULL,\n  name            text,\n  source          text NOT NULL DEFAULT 'whatsapp',\n  status          text NOT NULL DEFAULT 'new',\n  score           int2 CHECK (score BETWEEN 0 AND 100),\n  intent_signal   jsonb NOT NULL DEFAULT '{}'::jsonb,\n  embedding       vector(768),\n  stability_score float4 NOT NULL DEFAULT 0.5,\n  created_at      timestamptz NOT NULL DEFAULT now(),\n  updated_at      timestamptz NOT NULL DEFAULT now()\n);\n\nALTER TABLE public.leads ENABLE ROW LEVEL SECURITY;\n\nCREATE POLICY \"leads: users read own rows\"\n  ON public.leads FOR SELECT USING (user_id = auth.uid());\nCREATE POLICY \"leads: users insert own rows\"\n  ON public.leads FOR INSERT WITH CHECK (user_id = auth.uid());\nCREATE POLICY \"leads: users update own rows\"\n  ON public.leads FOR UPDATE USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());\n-- DELETE intentionally NOT exposed \u2014 erasure routes through erase-lead (SECURITY DEFINER).\n\nCREATE INDEX leads_user_idx ON public.leads (user_id);\nCREATE INDEX leads_status_idx ON public.leads (user_id, status);\nCREATE INDEX leads_embedding_hnsw\n  ON public.leads USING hnsw (embedding vector_cosine_ops)\n  WITH (m = 16, ef_construction = 64);\n\nCREATE TRIGGER set_leads_updated_at\n  BEFORE UPDATE ON public.leads\n  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();\n```\n\n> The remaining tables (`lead_events`, `campaigns`, `campaign_steps`, `sequences`, `sequence_enrollments`, `marketing_consents`, `marketing_attribution`, `aeo_audits`) follow the **identical RLS-default-deny skeleton** with `user_id = auth.uid()` and denormalized `user_id` for child tables to keep RLS simple. Every migration passes `/security-review` (FMEA-011).\n\n---\n\n## 4. GraphRAG Knowledge Nodes\n\n### Node Types Introduced\n\n| node_type | Title Pattern | Content Fields | Embedding Source |\n|-----------|--------------|----------------|-----------------|\n| `campaign` | `campaign:<name>` | intent + channels + outcome | `name + intent + summary` |\n| `marketing_insight` | `mh-insight:<slug>` | observa\u00e7\u00e3o de otimiza\u00e7\u00e3o (loop de aprendizado) | `content` |\n| `aeo_snapshot` | `aeo:<brand>:<date>` | citation findings agregados | `brand + findings summary` |\n\n> Leads/contatos **N\u00c3O** viram n\u00f3s de malha com PII bruta (LGPD/minimiza\u00e7\u00e3o) \u2014 apenas insights agregados/anonimizados quando promovidos.\n\n### Edge Types Introduced\n\n| Edge relationship | Source node_type | Target node_type | Metadata |\n|-------------------|-----------------|-----------------|----------|\n| `ATTRIBUTES_REVENUE_TO` (reuse) | `observation`/`marketing_attribution` | `campaign` / `content_mesh_asset` | `{revenue_cents}` |\n| `NURTURES` | `campaign` | `marketing_insight` | `{sequence_id}` |\n| `DERIVES_FROM` (reuse) | `documentation_suite` (este seal) | parent BoK seal | `{}` |\n\n### Embedding Trigger\n\nCampaign/insight/aeo nodes inseridos em `mcorch_nodes` disparam autoembed via `trg_mcorch_embed_on_insert` (pg_net \u2192 `embed-mcorch-node`, 768d). Leads N\u00c3O s\u00e3o embedados com PII; s\u00f3 o vetor de `leads.embedding` (derivado de sinais n\u00e3o-PII de inten\u00e7\u00e3o) \u00e9 local \u00e0 tabela para busca sem\u00e2ntica intra-tenant.\n\n### FSRS-6 Parameters\n\n| Field | Initial Value | Decay Rule |\n|-------|--------------|------------|\n| `stability_score` (campaign/insight nodes) | `0.85` (seal) / `0.5` (insight) | Decai per migration `20260425190000` |\n| `revenue_impact` (campaign node) | Soma de `marketing_attribution.revenue_cents` | Atualizado a cada convers\u00e3o atribu\u00edda |\n\n---\n\n## 5. Tenant Isolation Map\n\n| Table | `user_id` scope | `project_id` scope | System rows (user_id IS NULL) |\n|-------|----------------|-------------------|-------------------------------|\n| `leads` | \u2705 Required | Optional | No |\n| `lead_events` | \u2705 Required | \u2014 | No |\n| `campaigns` | \u2705 Required | Optional | No |\n| `campaign_steps` | \u2705 Required | \u2014 | No |\n| `sequences` | \u2705 Required | \u2014 | No |\n| `sequence_enrollments` | \u2705 Required | \u2014 | No |\n| `marketing_consents` | \u2705 Required | \u2014 | No |\n| `marketing_attribution` | \u2705 Required | Optional | No |\n| `aeo_audits` | \u2705 Required | \u2014 | No |\n| `mcorch_nodes` (campaign/insight) | Optional | Optional | Yes (insights agregados podem ser system) |\n\n---\n\n## 6. Data Quality Rules\n\n| Table | Column | Rule | Violation Message (PT-BR) |\n|-------|--------|------|--------------------------|\n| `leads` | `contact` | E.164 OU email RFC v\u00e1lido | \"Contato inv\u00e1lido \u2014 telefone (E.164) ou email\" |\n| `leads` | `score` | 0 \u2264 score \u2264 100 (CHECK) | \"Score deve estar entre 0 e 100\" |\n| `leads` | `status` | \u2208 enum de status | \"Status de lead inv\u00e1lido\" |\n| `marketing_consents` | `basis` | \u2208 {consent, legitimate_interest, contract} | \"Base legal LGPD obrigat\u00f3ria\" |\n| `marketing_consents` | `granted` | nurturing exige `granted=true` (regra de app) | \"Sem consentimento \u2014 nurturing bloqueado\" |\n| `marketing_attribution` | `revenue_cents` | \u2265 0 | \"Receita n\u00e3o pode ser negativa\" |\n| `aeo_audits` | `citation_rate` | 0.0 \u2264 rate \u2264 1.0 | \"Taxa de cita\u00e7\u00e3o fora de faixa\" |\n\n---\n\n## 7. Retention & Archival Policy\n\n| Data | Retention Period | Archival Strategy | Deletion Trigger |\n|------|-----------------|-------------------|-----------------|\n| `leads` + PII | Enquanto consentimento v\u00e1lido; erasure \u2264 24h p\u00f3s-solicita\u00e7\u00e3o | Sem arquivamento de PII | `erase-lead` (cascade) ou opt-out+retention policy |\n| `lead_events` | 18 meses | Agrega\u00e7\u00e3o anonimizada p/ Customer 360 hist\u00f3rico | Com lead pai (CASCADE) |\n| `marketing_consents` | Trilha legal: reter prova de consent/withdrawal mesmo ap\u00f3s erasure de PII de contato | Registro de prova (sem contato bruto) | Pol\u00edtica legal |\n| `marketing_attribution` | Indefinido (financeiro) | \u2014 | Com campanha/lead |\n| `aeo_audits` | 12 meses | Snapshot hist\u00f3rico | Cron purge |\n| Embeddings (`leads.embedding`) | Com a linha | \u2014 | Com lead |\n| `infra_health_logs` | 90 dias | Sem arquivamento | Cron purge |\n\n> **LGPD nota:** erasure de PII de contato (`leads.contact`/`name`) \u00e9 distinto da reten\u00e7\u00e3o da **prova de consentimento** (obriga\u00e7\u00e3o legal) \u2014 `marketing_consents` ret\u00e9m o registro de base legal sem o contato bruto.\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/06-data-model.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:42:30)*


## 🤖 Claude *(00:43:16)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/07-process-flow.md",
  "content": "# Process & Automation Blueprint\n\n**Project:** marketing-hub  \n**Version:** v0.1 | **Date:** 2026-06-02  \n**BoK Applied:** BPM CBOK v4 (Process Modeling + Process Design)  \n**Status:** Complete\n\n---\n\n## 1. Process Inventory\n\n| Process ID | Name | Type | Trigger | Owner | SLA |\n|------------|------|------|---------|-------|-----|\n| PROC-MH-001 | Lead Capture & Absorb | event-driven | `whatsapp-webhook` / form / import | System | < 5s ingest |\n| PROC-MH-002 | Lead Scoring | human-in-loop \u2192 automated | User \"Qualificar\" / batch | User | < 800ms (excl. IA) |\n| PROC-MH-003 | Campaign Run | automated | User \"Run\" na campanha | User | per orchestrate-content |\n| PROC-MH-004 | Nurturing Advance | cron | Schedule (n8n) | System | passo dentro da janela |\n| PROC-MH-005 | Intent Orchestration + HITL | human-in-loop | User declara inten\u00e7\u00e3o | User | plano < 5s; HITL = humano |\n| PROC-MH-006 | AEO Audit Cycle | cron / event-driven | Schedule semanal / User | System | < 7d freshness |\n| PROC-MH-007 | Lead Erasure (LGPD) | event-driven | Opt-out / erasure request | System | \u2264 24h cascade |\n| PROC-MH-008 | Attribution Capture | event-driven | Postback / conversion event | System | < 5s |\n\n---\n\n## 2. BPMN-lite Process Maps\n\n### PROC-MH-002: Lead Scoring\n\n```\nSTART \u2500\u2500\u25b6 [User aciona \"Qualificar\" no lead] \u2500\u2500\u25b6 <Gateway: JWT v\u00e1lido?>\n                                                    \u2502 YES                  \u2502 NO\n                                          <Gateway: saldo \u2265 1 mco?>    [HTTP 401]\n                                              \u2502 YES          \u2502 NO\n                                     [deduct_mco_coins 1]  [HTTP 402 \u2192 Toast \"Saldo insuficiente\"]\n                                              \u2502\n                                     [AI score via per-user key]\n                                              \u2502 (timeout/erro)\n                                     \u250c\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2534\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510\n                                  (ok)               (fail-soft)\n                              [UPDATE leads.score]  [score=null + infra_health_logs warn]\n                                     \u2502                  \u2502\n                              [insert lead_event]   [retorna parcial, sem cobrar de novo]\n                                     \u2502\n                              [HTTP 200 score+rationale]\n                                     \u2502\n                                    END\n```\n\n**Swimlanes:**\n\n| Swimlane | Participant | Tasks |\n|----------|-------------|-------|\n| User | Browser / `LeadBoard` | Clica \"Qualificar\"; v\u00ea score + rationale |\n| Frontend Hook | `useLeadScore.ts` | Invoca edge fn; trata 401/402/404/422 |\n| Edge Function | `lead-score` | JWT \u2192 deduct RPC \u2192 AI \u2192 update \u2192 log |\n| External API | OpenRouter (per-user key) | Computa score 0\u2013100 + rationale |\n| DB | Supabase | `leads.score`, `lead_events`, `profiles.mco_balance` |\n\n---\n\n### PROC-MH-003: Campaign Run (orquestra orchestrate-content)\n\n```\n[User Action: \"Run\" na campanha]\n  \u2502\n  \u25bc\n[Hook: useCampaigns \u2192 mutation]\n  \u2502\n  \u25bc\n[Edge Fn: campaign-run]\n  \u251c\u2500\u2500 Validate JWT \u2500\u2500(fail)\u2500\u2500\u25b6 HTTP 401\n  \u251c\u2500\u2500 Check ownership (campaign.user_id = auth.uid()) \u2500\u2500(fail)\u2500\u2500\u25b6 HTTP 404\n  \u251c\u2500\u2500 deduct_mco_coins(10) \u2500\u2500(low)\u2500\u2500\u25b6 HTTP 402 \u2192 Toast \"Saldo insuficiente\"\n  \u251c\u2500\u2500 for each campaign_step (by position):\n  \u2502       invoke('orchestrate-content', stepPayload)  \u25c0\u2500\u2500 REUSO (n\u00e3o duplica)\n  \u2502       update campaign_steps.status (running\u2192done|error)\n  \u251c\u2500\u2500 on conversion later \u2192 PROC-MH-008 (attribution)\n  \u251c\u2500\u2500 insert mcorch_nodes campaign node (autoembed) + infra_health_logs pulse\n  \u2514\u2500\u2500 HTTP 200 \u2192 React Query invalidation \u2192 UI refresh\n```\n\n---\n\n### PROC-MH-007: Lead Erasure (LGPD-critical)\n\n```\nSTART \u2500\u2500\u25b6 [Opt-out OU erasure request] \u2500\u2500\u25b6 [Edge Fn: erase-lead (SECURITY DEFINER, auth.uid())]\n   \u2502\n   \u251c\u2500\u2500 interrompe sequences ativas do lead (status='opted_out')\n   \u251c\u2500\u2500 DELETE leads + lead_events + sequence_enrollments (cascade by lead_id, owner-bound)\n   \u251c\u2500\u2500 DELETE marketing_attribution refs (mant\u00e9m agregados anonimizados)\n   \u251c\u2500\u2500 REVOKE segredo Vault tied to lead (se houver token de canal)\n   \u251c\u2500\u2500 RET\u00c9M marketing_consents como prova legal (sem contato bruto)\n   \u251c\u2500\u2500 insert infra_health_logs {event:'marketing_hub_lead_erased', tables_cleared}\n   \u2514\u2500\u2500 HTTP 200 { erased:true }\n                                                              END\n```\n\n> Padr\u00e3o espelha `disconnect_wordpress`/`disconnect_meta` (delete linha **E** revoga segredo Vault; double-bind owner+id \u2192 tenant-safe).\n\n---\n\n## 3. n8n Workflow Blueprints\n\n### Workflow: Nurturing Sequence Advance (PROC-MH-004)\n\n**Trigger:** Cron (schedule)  \n**Idempotency key:** `sequence_enrollment_id + current_step`\n\n```\n[Trigger: Cron (e.g. */15 min)]\n  \u2502\n  \u25bc\n[Node: Query sequence_enrollments WHERE status='active' AND next_run_at <= now()]\n  \u2502\n  \u25bc\n[Node: For each enrollment]\n  \u251c\u2500\u2500 [Check consent granted AND not opted_out] \u2500\u2500(fail)\u2500\u2500\u25b6 [Set status='opted_out', skip]\n  \u2502\n  \u251c\u2500\u2500 [Node: HTTP Request \u2192 /functions/v1/nurture-dispatch]\n  \u2502     \u251c\u2500\u2500 Headers: Authorization: Bearer <SB_SECRET_KEY or user JWT>\n  \u2502     \u251c\u2500\u2500 Body: { enrollment_id, step }\n  \u2502     \u2502\n  \u2502     \u251c\u2500\u2500 (success) \u2500\u2500\u25b6 [Update current_step+1, next_run_at = now()+stepDelay]\n  \u2502     \u2502                   \u2514\u2500\u2500 [If last step \u2192 status='completed']\n  \u2502     \u2502\n  \u2502     \u2514\u2500\u2500 (error) \u2500\u2500\u25b6 [Set retry count + 1]\n  \u2502            (count \u2264 3) \u2500\u2500\u25b6 [Wait: exponential backoff] \u2500\u2500\u25b6 retry\n  \u2502            (count > 3) \u2500\u2500\u25b6 [Insert infra_health_logs {event:'marketing_hub_nurture_failure'}]\n  \u2502                              \u2514\u2500\u2500 [Alert Sovereign]\n```\n\n**Data Mapping:**\n\n| Input Field | Source | \u2192 | Output Field | Destination |\n|-------------|--------|---|--------------|-------------|\n| `enrollment_id` | Query row | \u2192 | `enrollment_id` | nurture-dispatch body |\n| `current_step` | Query row | \u2192 | `step` | nurture-dispatch body |\n| `SB_SECRET_KEY` | Env (vault) | \u2192 | `Authorization` | Header |\n\n---\n\n## 4. Orchestration Integration Points\n\n> `campaign-run` integra-se ao `orchestrate-content` existente \u2014 reuso, n\u00e3o duplica\u00e7\u00e3o.\n\n| Pipeline Step | Step ID | Position | Description | mcoCoins Trigger |\n|---------------|---------|----------|-------------|-----------------|\n| Campaign dispatch | step_mh_campaign | wrapper | `campaign-run` debita 10 e chama `orchestrate-content` por passo | 10 coins no entry de `campaign-run` |\n| Attribution stitch | step_mh_attrib | post-conversion | postback liga revenue\u2192campaign_id em `marketing_attribution` | 0 (event-driven) |\n\n**Integration code stub (inside `campaign-run/index.ts`):**\n```typescript\n// Step mh_campaign: run each campaign step via existing orchestrator\nawait supabase.rpc('deduct_mco_coins', { p_user_id, p_amount: 10 }) // 402 if low\nfor (const step of steps.sort((a,b)=>a.position-b.position)) {\n  await setStepStatus(step.id, 'running')\n  const r = await supabase.functions.invoke('orchestrate-content', { body: stepPayload(step) })\n  if (r.error) { await setStepStatus(step.id, 'error'); break }\n  await setStepStatus(step.id, 'done')\n}\n// emit campaign mesh node + infra_health_logs pulse (success/degraded/error)\n```\n\n---\n\n## 5. Error Handling & Retry Strategy\n\n| Process | Step | Error Type | Max Retries | Backoff | Failure Action |\n|---------|------|-----------|-------------|---------|----------------|\n| PROC-MH-002 | AI score | IA timeout | 1 | Fixed 3s | Fail-soft (score=null), log warn, **n\u00e3o recobra** |\n| PROC-MH-003 | orchestrate-content | Step 5xx | 2 | Exponential (2s,4s) | Marca step error; pausa run; log |\n| PROC-MH-004 | nurture-dispatch | Network/5xx | 3 | Exponential (2s,4s,8s) | infra_health_logs + alerta |\n| PROC-MH-002/003/006 | mcoCoins check | Saldo insuficiente | 0 | \u2014 | HTTP 402 ao user (sem cobran\u00e7a parcial) |\n| Any | JWT validation | Token inv\u00e1lido | 0 | \u2014 | HTTP 401 imediato |\n| PROC-MH-007 | erase-lead | Falha parcial de cascade | 2 | Fixed 5s | Re-tenta; se falhar, alerta CR\u00cdTICO (LGPD) |\n\n---\n\n## 6. SLA Definitions\n\n| Process | Step | Expected Duration | Timeout Threshold | Alert if exceeded |\n|---------|------|------------------|-------------------|-------------------|\n| PROC-MH-001 | Capture ingest | < 5s | 15s | Yes \u2192 infra_health_logs |\n| PROC-MH-002 | lead-score (excl. IA) | < 800ms p95 | 5s | Yes |\n| PROC-MH-003 | campaign-run dispatch | per orchestrate-content | per step timeout | Yes |\n| PROC-MH-004 | nurture step | dentro da janela do cron | 2\u00d7 janela | Yes |\n| PROC-MH-007 | erasure cascade | < 24h | 24h | **Sim \u2014 CR\u00cdTICO LGPD** |\n\n---\n\n## 7. Cron Jobs\n\n| Job Name | Schedule (cron) | Function | Idempotency | Failure Alerting |\n|----------|----------------|----------|-------------|-----------------|\n| `marketing-nurture-advance` | `*/15 * * * *` | n8n \u2192 `nurture-dispatch` | `enrollment_id + current_step` | `infra_health_logs` |\n| `marketing-aeo-audit` | `0 6 * * 1` (seg 06h) | `aeo-audit` por queries rastreadas | `brand + query + week` | `infra_health_logs` |\n| `marketing-consent-retention` | `0 3 * * *` | purge de PII p\u00f3s-retention/erasure | data-based | `infra_health_logs` |\n\n> Todos os cron jobs idempotentes. **Preservar os crons existentes** (watchdog `*/5`, auto-publish `*/5`, audit-4cs, ast-ingest, nightly-bridge) ao instalar \u2014 adicionar, nunca sobrescrever o crontab.\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/07-process-flow.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:43:28)*


## 🤖 Claude *(00:43:29)*

Phase 4 (Data + Process) completa. Avanço para **Phase 5 — Quality & Autonomic Engineering** (CMQ/OE).

## 🤖 Claude *(00:43:29)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "4",
  "status": "completed"
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #4 status
> ```

## 🤖 Claude *(00:43:34)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "5",
  "status": "in_progress"
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #5 status
> ```

## 🤖 Claude *(00:44:33)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/08-quality-metrics.md",
  "content": "# Quality & Self-Optimization Specification\n\n**Project:** marketing-hub  \n**Version:** v0.1 | **Date:** 2026-06-02  \n**BoK Applied:** CMQ/OE BOK (Process Management + Organizational Excellence)  \n**Status:** Complete\n\n---\n\n## 1. Quality Objectives\n\n| QO ID | Objective | Linked Business Objective | Target | Review Cadence |\n|-------|-----------|--------------------------|--------|---------------|\n| QO-MH-001 | Convers\u00e3o de lead acima do baseline | BO-MH-003 | Lift \u2265 +10% (90d) / +25% (12m) | Monthly |\n| QO-MH-002 | Zero envio de nurturing sem consentimento | BO-MH-005 | 100% gated por consent | Weekly |\n| QO-MH-003 | Erasure LGPD completa e tempestiva | BO-MH-005 | 100% cascata \u2264 24h | Weekly |\n| QO-MH-004 | Presen\u00e7a AEO crescente | BO-MH-004 | Citation \u2265 10% (6m) / \u2265 30% (12m) | Monthly |\n| QO-MH-005 | Disciplina de custo (mcoCoins) | BO-MH-002 | 0 dedu\u00e7\u00e3o client-side; 0 cobran\u00e7a parcial | Per sprint |\n| QO-MH-006 | Consolida\u00e7\u00e3o sem \u00f3rf\u00e3os | BO-MH-001 | 0 superf\u00edcie de marketing v1 \u00f3rf\u00e3 | Quarterly |\n\n---\n\n## 2. KPI Dashboard Definition\n\n| KPI ID | Name | Formula | Target | Warn Threshold | Critical Threshold | Data Source |\n|--------|------|---------|--------|---------------|-------------------|-------------|\n| KPI-MH-001 | Lead Conversion Rate | `converted / total_leads` | \u2265 baseline+10% | < baseline | < baseline\u221210% | `leads` |\n| KPI-MH-002 | Consent Compliance | `nurture_sends_with_consent / nurture_sends` | 100% | < 100% | < 99% | `lead_events` + `marketing_consents` |\n| KPI-MH-003 | Erasure SLA | `erasures_within_24h / erasure_requests` | 100% | < 100% | < 95% | `infra_health_logs` |\n| KPI-MH-004 | AEO Citation Rate | `cited_queries / tracked_queries` | \u2265 10% | < 8% | 0% | `aeo_audits` |\n| KPI-MH-005 | Attribution Coverage | `attributed_revenue / total_revenue` | \u2265 80% | < 60% | < 40% | `marketing_attribution` |\n| KPI-MH-006 | mcoCoins Burn Rate | `SUM(deductions) / active_users` | dentro do tier | tier\u00d70.8 | tier\u00d71.0 | `profiles` + `mcoin_transactions` |\n| KPI-MH-007 | Edge Fn p95 Latency | `PERCENTILE_CONT(0.95) latency` | < 800ms | 1000ms | 2000ms | Supabase logs |\n| KPI-MH-008 | Knowledge Mesh Growth (campaigns) | `COUNT(campaign nodes) per week` | > 0 | 0 (2 wks) | 0 (4 wks) | `mcorch_nodes` |\n| KPI-MH-009 | Lead Score Accuracy | `converted_high_score / high_score_leads` | \u2265 0.4 | < 0.3 | < 0.2 | `leads` (score vs outcome) |\n\n---\n\n## 3. FMEA Table\n\n> Severity, Occurrence, Detection: 1 (best) \u2192 10 (worst). RPN = S \u00d7 O \u00d7 D. RPN > 100 requires action.\n\n| ID | Function | Failure Mode | Effect | S | O | D | RPN | Recommended Action |\n|----|---------|--------------|--------|---|---|---|-----|--------------------|\n| FMEA-MH-001 | Lead RLS | Vazamento cross-tenant de PII | Viola\u00e7\u00e3o LGPD + perda de confian\u00e7a | 10 | 2 | 3 | 60 | RLS default-deny + `/security-review` obrigat\u00f3rio + guard de tenant nas views |\n| FMEA-MH-002 | Nurturing dispatch | Envio sem consentimento v\u00e1lido | **Viola\u00e7\u00e3o LGPD direta** | 9 | 3 | 4 | **108** | **Gate de consent hard no `nurture-dispatch` (server-side); cron checa consent antes de cada passo; teste de regress\u00e3o obrigat\u00f3rio** |\n| FMEA-MH-003 | erase-lead | Cascade incompleta (PII residual) | **PII retida ap\u00f3s erasure (LGPD)** | 9 | 3 | 5 | **135** | **Erasure transacional + verifica\u00e7\u00e3o zero-residue p\u00f3s-delete em TODAS as tabelas + Vault; retry cr\u00edtico + alerta; teste E2E de erasure** |\n| FMEA-MH-004 | campaign-run | RPC d\u00e9bito 2\u00d7 \u2192 cobran\u00e7a dupla | Usu\u00e1rio cobrado em dobro | 7 | 2 | 3 | 42 | Idempotency key por `campaign_run_id`; d\u00e9bito antes do dispatch, uma vez |\n| FMEA-MH-005 | aeo-audit | Provider devolve cita\u00e7\u00e3o alucinada/ru\u00eddo | Decis\u00e3o de marketing baseada em sinal falso | 5 | 5 | 5 | **125** | **Probe-first do provider (Lei 1); valida\u00e7\u00e3o cruzada multi-engine; marcar confidence; degradado documentado se sinal n\u00e3o confi\u00e1vel** |\n| FMEA-MH-006 | lead-score | IA alucina score \u2192 m\u00e1 prioriza\u00e7\u00e3o | Esfor\u00e7o gasto em lead errado | 4 | 5 | 5 | 100 | Rationale XAI audit\u00e1vel; calibra\u00e7\u00e3o contra outcomes (KPI-MH-009); score \u00e9 sinal, n\u00e3o decis\u00e3o autom\u00e1tica |\n| FMEA-MH-007 | campaign-run | Falha parcial deixa steps inconsistentes | Campanha meio-executada | 6 | 4 | 4 | 96 | Status por step + pausa no erro (n\u00e3o cancela); retom\u00e1vel idempotente |\n| FMEA-MH-008 | Absorb whatsapp_leads | Perda de dado na migra\u00e7\u00e3o | Leads hist\u00f3ricos perdidos | 8 | 2 | 3 | 48 | Backfill com contagem antes/depois (Lei 1); migration em txn; `/security-review` |\n| FMEA-MH-009 | mcoCoins check | Cobran\u00e7a parcial em saldo baixo no meio da sequ\u00eancia | Usu\u00e1rio cobrado por passo n\u00e3o entregue | 6 | 3 | 3 | 54 | Pausar (n\u00e3o cancelar) no 402; debitar s\u00f3 no passo efetivamente executado |\n\n**Itens RPN > 100 (a\u00e7\u00e3o obrigat\u00f3ria):** FMEA-MH-002 (108) \u00b7 FMEA-MH-003 (135) \u00b7 FMEA-MH-005 (125).\n\n---\n\n## 4. Self-Optimization Loops\n\n| Loop ID | Trigger Condition | KPI Source | Autonomous Response | Escalation (human) |\n|---------|------------------|------------|--------------------|--------------------|\n| SOL-MH-001 | KPI-MH-007 latency > 1000ms por 5 chamadas | infra_health_logs | mega-brain-daemon: restart edge fn container | Alerta Sovereign se > 2s |\n| SOL-MH-002 | KPI-MH-002 consent compliance < 100% | lead_events + consents | **Bloqueio imediato de dispatch + alerta** | Sovereign (LGPD, sempre) |\n| SOL-MH-003 | KPI-MH-004 citation rate cai > 20% WoW | aeo_audits | Disparar novo audit + sugerir ajustes de conte\u00fado | Alerta se 0% por 4 semanas |\n| SOL-MH-004 | KPI-MH-006 burn > 80% da quota do tier | profiles | Notifica\u00e7\u00e3o in-app PT-BR de recarga | \u2014 (sem auto-a\u00e7\u00e3o) |\n| SOL-MH-005 | KPI-MH-009 score accuracy < 0.3 | leads | Re-calibrar prompt de scoring; flag p/ revis\u00e3o | Sovereign revisa modelo |\n\n---\n\n## 5. Self-Healing Specifications\n\n### 5.1 Watchdog Telemetry Events\n\n| Event Type | Trigger | Severity | Payload |\n|------------|---------|----------|---------|\n| `marketing_hub_fn_failure` | Edge fn 5xx p\u00f3s-retry | error | `{fn_name, error_message, user_id}` |\n| `marketing_hub_nurture_failure` | nurture-dispatch falha p\u00f3s-retry | warn | `{enrollment_id, retry_count}` |\n| `marketing_hub_consent_block` | Tentativa de envio sem consent | warn | `{lead_id, sequence_id}` |\n| `marketing_hub_lead_erased` | Erasure conclu\u00edda | info | `{lead_id, tables_cleared}` |\n| `marketing_hub_erase_incomplete` | Cascade de erasure parcial | error | `{lead_id, missing_tables}` |\n| `marketing_hub_sla_breach` | SLA de processo excedido | warn | `{process_id, elapsed_ms, threshold_ms}` |\n\n### 5.2 Auto-Recovery Script Stubs\n\n```bash\n#!/bin/bash\n# scripts/self-heal-marketing-hub.sh\n# Triggered by mega-brain-daemon when marketing_hub_fn_failure detected\nFUNCTION_NAME=\"$1\"   # lead-score | campaign-run | nurture-dispatch | aeo-audit | erase-lead\necho \"[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Self-heal triggered for $FUNCTION_NAME\"\nSTATUS=$(curl -s -o /dev/null -w \"%{http_code}\" \\\n  \"$SUPABASE_URL/functions/v1/$FUNCTION_NAME\" \\\n  -H \"Authorization: Bearer $SB_SECRET_KEY\")   # cutover key (legacy revogada)\nif [ \"$STATUS\" -ge 500 ]; then\n  echo \"[WARN] $FUNCTION_NAME unhealthy ($STATUS). Re-deploying...\"\n  npx supabase functions deploy \"$FUNCTION_NAME\"\nfi\necho \"[OK] Self-heal complete for $FUNCTION_NAME\"\n```\n\n> \u26a0\ufe0f `erase-lead` failure \u00e9 **CR\u00cdTICO** \u2014 nunca auto-resolver silenciosamente; sempre escalar ao Sovereign (LGPD).\n\n### 5.3 mega-brain-daemon Integration Points\n\n| Daemon Event | Condition | Action |\n|-------------|-----------|--------|\n| `health_check` | Cada 5 min (watchdog) | Conta `leads`/`campaigns` vs baseline; checa erasure backlog |\n| `anomaly_detected` | `marketing_hub_*` error rate > 5/hora | Executa `self-heal-marketing-hub.sh` |\n| `consent_anomaly` | qualquer `marketing_hub_consent_block` | Alerta imediato (n\u00e3o auto-heal \u2014 pol\u00edtica humana) |\n| `recovery_confirmed` | Health check passa p\u00f3s-heal | Insere `recovery_ok` em infra_health_logs |\n\n---\n\n## 6. SLA / SLO / SLI Definitions\n\n| Service | SLI (what we measure) | SLO (our target) | SLA (contractual consequence) |\n|---------|----------------------|------------------|-------------------------------|\n| `lead-score` / `campaign-run` API | p95 response latency (excl. IA) | \u2264 800ms | Credits se > 2s para > 1% das chamadas/m\u00eas |\n| Nurturing dispatch | % passos entregues dentro da janela | \u2265 99% | Incident report |\n| Erasure LGPD | % erasures completos \u2264 24h | 100% | **Compliance incident (n\u00e3o-negoci\u00e1vel)** |\n| AEO audit freshness | % queries com audit \u2264 7d | \u2265 95% | Auto re-audit |\n| Knowledge Mesh embedding | % campaign nodes embedded \u2264 5m | \u2265 95% | Auto-backfill |\n| Platform uptime | % minutos dispon\u00edveis/m\u00eas | \u2265 99.5% | Per enterprise contract |\n\n---\n\n## 7. PDCA Improvement Cadence\n\n| Cycle | Phase | Activity | Owner | Frequency |\n|-------|-------|----------|-------|-----------|\n| marketing-hub Quality | Plan | Revisar FMEA + KPI targets (foco RPN>100) | Sovereign | Quarterly |\n| marketing-hub Quality | Do | Implementar top a\u00e7\u00e3o de melhoria | Engineering | Per sprint |\n| marketing-hub Quality | Check | Comparar KPIs vs targets; atualizar RPNs | AIOS / mcorch-qa-healing | Monthly |\n| marketing-hub Quality | Act | Fechar loop; atualizar este doc | Sovereign | Monthly |\n\n**Improvement backlog location:** `.claude/context/sprint-priorities.md`\n\n---\n\n## 8. Observability Checklist\n\n### 8.1 Logging Events\n\n| Event | Location | Level | Fields logged |\n|-------|----------|-------|--------------|\n| Function entry | cada `*/index.ts` line ~10 | INFO | `{user_id, timestamp, request_id}` |\n| mcoCoins deduction | ap\u00f3s RPC | INFO | `{user_id, amount, new_balance}` |\n| Consent decision | antes de dispatch | INFO | `{lead_id, consent_granted}` |\n| Erasure cascade | ap\u00f3s cada delete | INFO | `{lead_id, table, rows_deleted}` |\n| Business logic error | catch block | ERROR | `{user_id, error_message, stack}` |\n| SLA breach | timeout guard | WARN | `{process_id, elapsed_ms}` |\n\n### 8.2 Alerting Rules\n\n| Condition | Channel | Escalation |\n|-----------|---------|------------|\n| Error rate > 1% em 5 min | `infra_health_logs` insert | mega-brain-daemon auto-heal |\n| Qualquer consent block | `infra_health_logs` insert | **Sovereign (LGPD imediato)** |\n| Erasure incomplete | `infra_health_logs` insert | **Sovereign CR\u00cdTICO** |\n| p95 latency > 2s | `infra_health_logs` insert | Sovereign notification |\n| KPI-MH-008 mesh growth 0 > 4 wks | Scheduled check | AIOS agent alert |\n\n### 8.3 Distributed Tracing Touchpoints\n\n| Span | Start | End | Tags |\n|------|-------|-----|------|\n| `<fn>.total` | Request received | Response sent | `user_id`, `status_code` |\n| `<fn>.mco_check` | Before RPC | After RPC | `amount`, `balance_after` |\n| `<fn>.ai_call` | Before AI provider | After | `provider`, `latency_ms`, `success` |\n| `nurture.consent_gate` | Before dispatch | After consent check | `lead_id`, `granted` |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent v1.0.0_\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/08-quality-metrics.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:45:10)*


## 🤖 Claude *(00:45:12)*

Todos os 9 docs autorados (Phase 0–5). Avanço para **Phase 6 (validação de rastreabilidade) + Phase 7 (seed script do mesh seal)**. Primeiro, descubro o seed-script precedente mais recente para espelhar exatamente (env var correta `SB_SECRET_KEY`, descoberta do parent seal).

## 🤖 Claude *(00:45:12)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "5",
  "status": "completed"
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #5 status
> ```

## 🤖 Claude *(00:45:13)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "6",
  "status": "in_progress"
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #6 status
> ```

> **Tool Result (Unknown Tool)** - ✅ Success
>
> ```
> ─── seed BoK seal scripts (por data) ───
> -rw-rw-r-- 1 ubuntu ubuntu  6517 Jun  1 10:10 scripts/seed-viralmind-bok-seal.ts
> -rw-rw-r-- 1 ubuntu ubuntu 10074 Jun  1 10:10 scripts/seed-openclaw-bok-seal.ts
> -rw-rw-r-- 1 ubuntu ubuntu  9837 Jun  1 10:10 scripts/seed-meta-api-bok-seal.ts
> -rw-rw-r-- 1 ubuntu ubuntu 12954 Jun  1 10:10 scripts/seed-mercado-livre-api-bok-seal.ts
> -rw-rw-r-- 1 ubuntu ubuntu  7437 Jun  1 10:10 scripts/seed-gamificacao-nodes-bok-seal.ts
> -rw-rw-r-- 1 ubuntu ubuntu 13453 Jun  1 10:10 scripts/seed-e2e-user-zero-bok-seal.ts
> -rw-rw-r-- 1 ubuntu ubuntu  5201 Jun  1 10:10 scripts/seed-conteudo-v2-bok-seal.ts
> -rw-rw-r-- 1 ubuntu ubuntu 10438 Jun  1 10:10 scripts/seed-constellation-v2-bok-seal.ts
> ─── seals mais recentes (grep nome do node) ───
> scripts/seed-conteudo-v2-bok-seal.ts
> scripts/seed-constellation-v2-bok-seal.ts
> scripts/seed-e2e-user-zero-bok-seal.ts
> scripts/seed-gamificacao-nodes-bok-seal.ts
> scripts/seed-openclaw-bok-seal.ts
> scripts/seed-mercado-livre-api-bok-seal.ts
> scripts/seed-viralmind-bok-seal.ts
> scripts/seed-meta-api-bok-seal.ts
> ```

## 🤖 Claude *(00:45:14)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"\u2500\u2500\u2500 seed BoK seal scripts (por data) \u2500\u2500\u2500\"; ls -lt scripts/seed-*bok-seal*.ts 2>/dev/null\necho \"\u2500\u2500\u2500 seals mais recentes (grep nome do node) \u2500\u2500\u2500\"; grep -l \"documentation_suite\" scripts/seed-*bok-seal*.ts 2>/dev/null",
  "description": "Find most recent BoK seal seed script to mirror"
}
```

## 🤖 Claude *(00:45:25)*


## 🤖 Claude *(00:45:26)*

All same mtime (bulk checkout). Reading the most semantically-related parent candidate (`meta-api` — since marketing-hub absorbs `whatsapp_leads` from it) to mirror structure + confirm the current env-var pattern post-cutover.

## 🤖 Claude *(00:45:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"\u2500\u2500\u2500 env var usado em cada seed (cutover check) \u2500\u2500\u2500\"; grep -nE \"SB_SECRET_KEY|SUPABASE_SERVICE_ROLE_KEY|SB_URL|SUPABASE_URL|VITE_SUPABASE\" scripts/seed-meta-api-bok-seal.ts | head -20\necho \"\u2500\u2500\u2500 todos os seeds: qual env? \u2500\u2500\u2500\"; grep -lE \"SB_SECRET_KEY\" scripts/seed-*bok-seal*.ts 2>/dev/null && echo \"(acima usam SB_SECRET_KEY)\" || echo \"nenhum usa SB_SECRET_KEY\"\necho \"\u2500\u2500\u2500 parent seal name referenciado \u2500\u2500\u2500\"; grep -nE \"bok-scribe-seal-[a-z0-9-]+-v1|derives_from|DERIVES_FROM|parentName|parent_name\" scripts/seed-meta-api-bok-seal.ts | head",
  "description": "Check env vars + parent seal pattern in meta-api seed"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── env var usado em cada seed (cutover check) ───
> 13:const SUPABASE_URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL;
> 14:const SERVICE_KEY = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY);
> 16:if (!SUPABASE_URL || !SERVICE_KEY) {
> 17:  console.error('Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY');
> 21:const supabase = createClient(SUPABASE_URL, SERVICE_KEY);
> ─── todos os seeds: qual env? ───
> scripts/seed-conteudo-v2-bok-seal.ts
> scripts/seed-e2e-user-zero-bok-seal.ts
> scripts/seed-constellation-v2-bok-seal.ts
> scripts/seed-gamificacao-nodes-bok-seal.ts
> scripts/seed-openclaw-bok-seal.ts
> scripts/seed-meta-api-bok-seal.ts
> scripts/seed-viralmind-bok-seal.ts
> scripts/seed-mercado-livre-api-bok-seal.ts
> (acima usam SB_SECRET_KEY)
> ─── parent seal name referenciado ───
> 7: * Inserts an explicit DERIVES_FROM edge to the parent seal (mercado-livre-api v1).
> 23:const PARENT_SEAL_NAME = 'bok-scribe-seal-mercado-livre-api-v1';
> 26:  name: 'bok-scribe-seal-meta-api-v1',
> 117:    derives_from: PARENT_SEAL_NAME,
> 132:console.log(`   Parent (DERIVES_FROM): ${PARENT_SEAL_NAME}`);
> 169:// Step 2: Resolve parent seal UUID for DERIVES_FROM edge
> 178:  console.error('   Skipping DERIVES_FROM edge insert. Manual cleanup may be required.');
> 186:// Step 3: INSERT DERIVES_FROM edge
> 192:    relation_type: 'DERIVES_FROM',
> 206:  console.error('❌ DERIVES_FROM edge insert failed:', edgeError);
> ```

## 🤖 Claude *(00:45:39)*


## 🤖 Claude *(00:45:40)*

Pattern confirmed: `SB_SECRET_KEY` first (cutover-aware), `PARENT_SEAL_NAME` constant, idempotent INSERT + DERIVES_FROM edge. Reading the full meta-api seed to mirror 1:1 (meta-api is the natural parent — marketing-hub absorbs `whatsapp_leads` from it).

## 🤖 Claude *(00:45:41)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/seed-meta-api-bok-seal.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env bun
> 2	/**
> 3	 * Seals the BoK documentation suite for meta-api in the Knowledge Mesh.
> 4	 * Inserts a documentation_suite node with stability 0.85; embedding triggered
> 5	 * automatically by trg_mcorch_embed_on_insert (pg_net).
> 6	 *
> 7	 * Inserts an explicit DERIVES_FROM edge to the parent seal (mercado-livre-api v1).
> 8	 *
> 9	 * Usage: bun run scripts/seed-meta-api-bok-seal.ts
> 10	 */
> 11	import { createClient } from '@supabase/supabase-js';
> 12	
> 13	const SUPABASE_URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL;
> 14	const SERVICE_KEY = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY);
> 15	
> 16	if (!SUPABASE_URL || !SERVICE_KEY) {
> 17	  console.error('Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY');
> 18	  process.exit(1);
> 19	}
> 20	
> 21	const supabase = createClient(SUPABASE_URL, SERVICE_KEY);
> 22	
> 23	const PARENT_SEAL_NAME = 'bok-scribe-seal-mercado-livre-api-v1';
> 24	
> 25	const sealNode = {
> 26	  name: 'bok-scribe-seal-meta-api-v1',
> 27	  node_type: 'documentation_suite',
> 28	  project_id: 'meta-api',
> 29	  stability_score: 0.85,
> 30	  revenue_impact: 1500000, // direct-revenue enabler — destrava ROI tracking de Ads, WhatsApp Lead Engine e publicação direta FB/IG
> 31	  content: `meta-api — Integração soberana multi-tenant com o ecossistema Meta (BoK v1)
> 32	
> 33	BoK suite (9 docs, ~1500 LOC) sealed 2026-05-30 sob MCORCH Master Execution Protocol. Motivada pela diretiva de expansão de canais do Sovereign para os maiores canais de atenção e conversão (Facebook, Instagram, WhatsApp) integrando posts automáticos, disparo conversacional de leads, telemetria de anúncios e o Meta MCP Server.
> 34	
> 35	VISÃO: quatro módulos soberanos estruturados sob o API Tenancy Model (credencial per-user via auth.uid() → fallback vault restrito). MÓDULO A (Meta Social Hub): postagem nativa de imagens e Reels no Facebook Page e Instagram Business Account. MÓDULO B (WhatsApp Lead Engine): disparo conversacional de templates HSM e recepção de webhooks de clientes. MÓDULO C (Meta Ads Automation): cache diário de cliques, impressões e custos com mapeamento topológico de ROAS no ROIWidget. MÓDULO D (Meta MCP Server): servidor de ferramentas stdio em Docker exposto aos agentes de IA da Constelação.
> 36	
> 37	ARQUITETURA: novas tabelas (meta_config, meta_posts, whatsapp_leads, meta_ads_metrics) + novas edge functions (meta-oauth, publish-meta, whatsapp-webhook, sync-meta-ads). CISSP CBK elevado: STRIDE com 8 ameaças mapeadas, encriptação AES-256-GCM em banco de dados, RLS default-deny por auth.uid(), assinatura HMAC SHA-256 em webhooks WhatsApp (X-Hub-Signature-256) e tratamento resiliente de rate limits.
> 38	
> 39	ID SPACE: MR-META-001..006 · BR-META-001..008 · BO-META-001..005 · SH-META-001..006 · PR-META-001..015 · FR-META-001..010 · NFR-META-001..008 · PROC-META-001..005 · KPI-META-001..006 · FMEA-META-001..008 · SOL-META-001..004 · QO-META-001..005 · BAC-META-001..006 · OTD-META-001..005.
> 40	
> 41	FMEA (8 entries, 4 RPN > 100): FMEA-META-003 (RPN 160 — vazamento cross-tenant de chaves; ação: RLS default-deny + db unit-test), FMEA-META-001 (RPN 144 — tokens expirados sem alerta; ação: cron diário + requires_reauth flag), FMEA-META-002 (RPN 135 — ban por spam; ação: HSM pre-flight lock fora de janela de 24h), FMEA-META-004 (RPN 105 — webhook overload; ação: ACK instantâneo + fila assíncrona pg_net).
> 42	
> 43	DOCUMENTOS: docs/bok/meta-api/{00-index ~100, 01-mrd 120, 02-brd 150, 03-prd 190, 04-frd 160, 05-sdd 260, 06-data-model 210, 07-process-flow 160, 08-quality-metrics 150} — total ~1500 LOC.
> 44	
> 45	TRACEABILITY: 100% de cobertura MR → BR → PR → FR. Zero orphans. Parent seal mercado-livre-api (sprint v6.14.1).
> 46	
> 47	BoK GATE: liberado APÓS este seal. Código de produção dos módulos só inicia após migrations com /security-review aprovadas e deploy das Edge Functions.`,
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
> 61	    document_lines: {
> 62	      '00-index': 100,
> 63	      '01-mrd': 120,
> 64	      '02-brd': 150,
> 65	      '03-prd': 190,
> 66	      '04-frd': 160,
> 67	      '05-sdd': 260,
> 68	      '06-data-model': 210,
> 69	      '07-process-flow': 160,
> 70	      '08-quality-metrics': 150,
> 71	      total: 1500,
> 72	    },
> 73	    phase_completed: 'Phase 7',
> 74	    traceability_validated: true,
> 75	    traceability_orphans: 0,
> 76	    bok_gate: 'fresh-completion',
> 77	    drift_reconciled: 0,
> 78	    drift_pending: 0,
> 79	    market_segment: 'B2B2C',
> 80	    monetization_model: 'hybrid',
> 81	    regulatory_profile: 'LGPD+GDPR',
> 82	    integration_surface: 'extends-mcorch',
> 83	    project_slug: 'meta-api',
> 84	    sprint_introduced: 'v6.14.2',
> 85	    sprint_sealed: 'pending-handoff',
> 86	    tags: ['bok-scribe', 'meta-api', 'B2B2C', 'facebook', 'instagram', 'whatsapp', 'mcp-server', 'meta-ads', 'lgpd', 'gdpr', 'per-user-tenancy'],
> 87	    modules: ['A: Meta Social Hub (MVP)', 'B: WhatsApp Lead Engine', 'C: Meta Ads Automation', 'D: Meta MCP Server'],
> 88	    new_tables: 4,
> 89	    new_columns: 0,
> 90	    new_edge_functions: 4,
> 91	    extended_edge_functions: 0,
> 92	    new_rpcs: 0,
> 93	    new_migrations: 1,
> 94	    id_ranges: {
> 95	      MR: '001..006',
> 96	      BR: '001..008',
> 97	      BO: '001..005',
> 98	      SH: '001..006',
> 99	      PR: '001..015',
> 100	      FR: '001..010',
> 101	      NFR: '001..008',
> 102	      PROC: '001..005',
> 103	      KPI: '001..006',
> 104	      FMEA: '001..008',
> 105	      SOL: '001..004',
> 106	      QO: '001..005',
> 107	      BAC: '001..006',
> 108	      OTD: '001..005',
> 109	    },
> 110	    fmea_rpn_over_100: ['FMEA-META-001', 'FMEA-META-002', 'FMEA-META-003', 'FMEA-META-004'],
> 111	    fmea_rpn_top: {
> 112	      'FMEA-META-003': 160,
> 113	      'FMEA-META-001': 144,
> 114	      'FMEA-META-002': 135,
> 115	      'FMEA-META-004': 105,
> 116	    },
> 117	    derives_from: PARENT_SEAL_NAME,
> 118	    depends_on_sop: 'docs/processes/affiliate-credential-resolution.md',
> 119	    motivating_incident: 'Sovereign directive to integrate Meta ecosystem APIs & MCP',
> 120	    revenue_impact_basis: 'omnichannel-expansion-ads-roi-tracking',
> 121	    bok_gate_blocking_otd: 'OTD-META-001 (Meta Webhook Signature Validation)',
> 122	    related_otds: ['OTD-META-001', 'OTD-META-002', 'OTD-META-003', 'OTD-META-004', 'OTD-META-005'],
> 123	    skips: ['Meta Commerce Manager Shop Sync', 'WhatsApp Payments', 'Meta Horizon Integration'],
> 124	  },
> 125	};
> 126	
> 127	console.log(`📝 Sealing BoK suite "meta-api"...`);
> 128	console.log(`   Project: ${sealNode.project_id}`);
> 129	console.log(`   Stability: ${sealNode.stability_score}`);
> 130	console.log(`   Revenue impact: ${sealNode.revenue_impact} (${sealNode.metadata.monetization_model})`);
> 131	console.log(`   BoK gate: ${sealNode.metadata.bok_gate}`);
> 132	console.log(`   Parent (DERIVES_FROM): ${PARENT_SEAL_NAME}`);
> 133	
> 134	// Idempotency check: skip if already exists
> 135	const { data: existing } = await supabase
> 136	  .from('mcorch_nodes')
> 137	  .select('id, name, created_at')
> 138	  .eq('name', sealNode.name)
> 139	  .maybeSingle();
> 140	
> 141	if (existing) {
> 142	  console.log(`\n⚠️ Seal node already exists (idempotent skip):`);
> 143	  console.log(`   ID:        ${existing.id}`);
> 144	  console.log(`   Name:      ${existing.name}`);
> 145	  console.log(`   Created:   ${existing.created_at}`);
> 146	  console.log(`\nNo new INSERT performed.`);
> 147	  process.exit(0);
> 148	}
> 149	
> 150	// Step 1: INSERT documentation_suite node
> 151	const { data: insertedNode, error: nodeError } = await supabase
> 152	  .from('mcorch_nodes')
> 153	  .insert(sealNode)
> 154	  .select('id, name, node_type, stability_score, created_at')
> 155	  .single();
> 156	
> 157	if (nodeError) {
> 158	  console.error('❌ Seal node insert failed:', nodeError);
> 159	  process.exit(1);
> 160	}
> 161	
> 162	console.log(`\n✅ Seal node inserted:`);
> 163	console.log(`   ID:        ${insertedNode.id}`);
> 164	console.log(`   Name:      ${insertedNode.name}`);
> 165	console.log(`   Type:      ${insertedNode.node_type}`);
> 166	console.log(`   Stability: ${insertedNode.stability_score}`);
> 167	console.log(`   Created:   ${insertedNode.created_at}`);
> 168	
> 169	// Step 2: Resolve parent seal UUID for DERIVES_FROM edge
> 170	const { data: parent, error: parentError } = await supabase
> 171	  .from('mcorch_nodes')
> 172	  .select('id, name')
> 173	  .eq('name', PARENT_SEAL_NAME)
> 174	  .single();
> 175	
> 176	if (parentError || !parent) {
> 177	  console.error(`\n❌ Parent seal lookup failed for ${PARENT_SEAL_NAME}:`, parentError);
> 178	  console.error('   Skipping DERIVES_FROM edge insert. Manual cleanup may be required.');
> 179	  process.exit(1);
> 180	}
> 181	
> 182	console.log(`\n🔗 Parent seal resolved:`);
> 183	console.log(`   ID:        ${parent.id}`);
> 184	console.log(`   Name:      ${parent.name}`);
> 185	
> 186	// Step 3: INSERT DERIVES_FROM edge
> 187	const { data: insertedEdge, error: edgeError } = await supabase
> 188	  .from('mcorch_edges')
> 189	  .insert({
> 190	    source_id: insertedNode.id,
> 191	    target_id: parent.id,
> 192	    relation_type: 'DERIVES_FROM',
> 193	    weight: 1.0,
> 194	    project_id: 'meta-api',
> 195	    metadata: {
> 196	      lineage: 'bok-scribe-seal',
> 197	      source_seal: insertedNode.name,
> 198	      target_seal: parent.name,
> 199	      sealed_at: insertedNode.created_at,
> 200	    },
> 201	  })
> 202	  .select('id, source_id, target_id, relation_type, created_at')
> 203	  .single();
> 204	
> 205	if (edgeError) {
> 206	  console.error('❌ DERIVES_FROM edge insert failed:', edgeError);
> 207	  process.exit(1);
> 208	}
> 209	
> 210	console.log(`\n✅ DERIVES_FROM edge inserted:`);
> 211	console.log(`   ID:        ${insertedEdge.id}`);
> 212	console.log(`   Source:    ${insertedEdge.source_id} (${insertedNode.name})`);
> 213	console.log(`   Target:    ${insertedEdge.target_id} (${parent.name})`);
> 214	console.log(`   Relation:  ${insertedEdge.relation_type}`);
> 215	console.log(`   Created:   ${insertedEdge.created_at}`);
> 216	
> 217	console.log(`\n🧠 Embedding will be generated automatically by trg_mcorch_embed_on_insert (assíncrono via pg_net).`);
> 218	console.log(`   Confirm with: SELECT embedding IS NOT NULL FROM mcorch_nodes WHERE id = '${insertedNode.id}';`);
> 219	console.log(`\n📊 Material proof summary for handoff:`);
> 220	console.log(`   - documentation_suite node UUID: ${insertedNode.id}`);
> 221	console.log(`   - DERIVES_FROM edge UUID:        ${insertedEdge.id}`);
> 222	console.log(`   - Parent seal UUID:              ${parent.id}`);
> 223	
> ```

## 🤖 Claude *(00:46:05)*


## 🤖 Claude *(00:46:07)*

Pattern fully captured. Before finalizing the seed script I need **real line counts** (Lei 1 — no fabricated LOC) and to confirm which parent seal actually exists in the mesh (the `DERIVES_FROM` edge needs a resolvable parent). Both in one read-only batch.

## 🤖 Claude *(00:46:12)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"\u2500\u2500\u2500 LOC reais dos 9 docs \u2500\u2500\u2500\"; wc -l docs/bok/marketing-hub/*.md | sort -k1 -n\necho \"\"\necho \"\u2500\u2500\u2500 parent seals candidatos presentes na malha? (read-only) \u2500\u2500\u2500\"\nset -a; source .env 2>/dev/null; set +a\nURL=\"${SUPABASE_URL:-$VITE_SUPABASE_URL}\"\nKEY=\"${SB_SECRET_KEY:-$SUPABASE_SERVICE_ROLE_KEY}\"\nif [ -z \"$URL\" ] || [ -z \"$KEY\" ]; then echo \"\u26a0\ufe0f sem URL/KEY no .env\"; else\n  curl -s \"$URL/rest/v1/mcorch_nodes?node_type=eq.documentation_suite&select=name,project_id,created_at&order=created_at.desc\" \\\n    -H \"apikey: $KEY\" -H \"Authorization: Bearer $KEY\" \\\n    | python3 -c \"import json,sys; d=json.load(sys.stdin); print(f'{len(d)} documentation_suite nodes na malha:'); [print(' ', n['name'], '\u00b7', n.get('created_at','')[:10]) for n in d]\"\nfi",
  "description": "Real LOC counts + query existing BoK seal nodes in mesh"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── LOC reais dos 9 docs ───
>     88 docs/bok/marketing-hub/00-index.md
>    143 docs/bok/marketing-hub/01-mrd.md
>    167 docs/bok/marketing-hub/04-frd.md
>    169 docs/bok/marketing-hub/02-brd.md
>    175 docs/bok/marketing-hub/08-quality-metrics.md
>    204 docs/bok/marketing-hub/07-process-flow.md
>    216 docs/bok/marketing-hub/03-prd.md
>    255 docs/bok/marketing-hub/06-data-model.md
>    315 docs/bok/marketing-hub/05-sdd.md
>   1732 total
> 
> ─── parent seals candidatos presentes na malha? (read-only) ───
> 116 documentation_suite nodes na malha:
>   bok-scribe-seal-constellation-v2-v1 · 2026-06-01
>   bok-scribe-seal-meta-api-v1 · 2026-05-30
>   bok-scribe-seal-mercado-livre-api-v1 · 2026-05-30
>   bok-scribe-seal-e2e-user-zero-v1 · 2026-05-26
>   Skills (2) · 2026-05-23
>   Overview (2) · 2026-05-23
>   Getting Started (2) · 2026-05-23
>   Tab (1) · 2026-05-23
>   Getting Started (1) · 2026-05-23
>   Features (1) · 2026-05-23
>   Overview (1) · 2026-05-23
>   Review Changes + Source Control · 2026-05-23
>   Separate Chrome Profile · 2026-05-23
>   Knowledge Items · 2026-05-23
>   Browser Recordings · 2026-05-23
>   Browser · 2026-05-23
>   Plan · 2026-05-23
>   Hooks · 2026-05-23
>   Models · 2026-05-23
>   Home · 2026-05-23
>   Files · 2026-05-23
>   Side Panel · 2026-05-23
>   Allowlist / Denylist · 2026-05-23
>   Screenshots · 2026-05-23
>   Playground · 2026-05-23
>   Permissions · 2026-05-23
>   Walkthrough · 2026-05-23
>   Projects · 2026-05-23
>   Editor · 2026-05-23
>   Conversation View · 2026-05-23
>   Rules · 2026-05-23
>   FAQ · 2026-05-23
>   Task List · 2026-05-23
>   Panes · 2026-05-23
>   Changes Sidebar · 2026-05-23
>   MCP · 2026-05-23
>   Workspaces · 2026-05-23
>   Enterprise · 2026-05-23
>   Sidecars · 2026-05-23
>   Getting Started · 2026-05-23
>   Features · 2026-05-23
>   Command · 2026-05-23
>   Review Changes · 2026-05-23
>   Agent Manager · 2026-05-23
>   Browser Subagent View · 2026-05-23
>   Overview + Quick Start · 2026-05-23
>   Build with Google · 2026-05-23
>   Artifacts · 2026-05-23
>   Artifact Review · 2026-05-23
>   Settings · 2026-05-23
>   Inbox · 2026-05-23
>   Using AGY CLI · 2026-05-23
>   Plugins · 2026-05-23
>   Terminal · 2026-05-23
>   Subagents · 2026-05-23
>   Overview · 2026-05-23
>   Agent Settings · 2026-05-23
>   Strict Mode · 2026-05-23
>   Firebase Studio Migration · 2026-05-23
>   Plans · 2026-05-23
>   Migration · 2026-05-23
>   Skill format (1) · 2026-05-23
>   Skills (1) · 2026-05-23
>   Dreaming (1) · 2026-05-23
>   Configuração (1) · 2026-05-23
>   Modelo de ameaças (MITRE ATLAS) · 2026-05-23
>   Verificações de auditoria de segurança · 2026-05-23
>   Arquitetura do Gateway · 2026-05-23
>   Guia de personalidade do SOUL.md · 2026-05-23
>   Subagentes · 2026-05-23
>   Criando Skills · 2026-05-23
>   Wiki de memória · 2026-05-23
>   Referência de configuração de memória · 2026-05-23
>   Busca na memória · 2026-05-23
>   Active Memory · 2026-05-23
>   Mecanismo de memória integrado · 2026-05-23
>   Visão geral da memória · 2026-05-23
>   Configuração — ferramentas e provedores personalizados · 2026-05-23
>   Configuração — canais · 2026-05-23
>   Configuração — agentes · 2026-05-23
>   Exemplos de configuração · 2026-05-23
>   Referência de configuração · 2026-05-23
>   Configuração do assistente pessoal · 2026-05-23
>   Configuração · 2026-05-23
>   Primeiros passos · 2026-05-23
>   bok-scribe-seal-mcorch-qa-healing-v1 · 2026-05-20
>   bok-scribe-seal-aios-sql-bridge-sdd-only-v1 · 2026-05-19
>   bok-scribe-seal-openclaw-v1 · 2026-05-18
>   bok-scribe-seal-gamificacao-nodes-v1 · 2026-05-18
>   Threat model (MITRE ATLAS) · 2026-05-16
>   Security audit checks · 2026-05-16
>   Gateway architecture · 2026-05-16
>   SOUL.md personality guide · 2026-05-16
>   Skill format · 2026-05-16
>   Sub-agents · 2026-05-16
>   Creating skills · 2026-05-16
>   Skills · 2026-05-16
>   Dreaming · 2026-05-16
>   Memory wiki · 2026-05-16
>   Memory configuration reference · 2026-05-16
>   Memory search · 2026-05-16
>   Active memory · 2026-05-16
>   Builtin memory engine · 2026-05-16
>   Memory overview · 2026-05-16
>   Configuration — tools and custom providers · 2026-05-16
>   Configuration — channels · 2026-05-16
>   Configuration — agents · 2026-05-16
>   Configuration examples · 2026-05-16
>   Configuration reference · 2026-05-16
>   Configuration · 2026-05-16
>   Personal assistant setup · 2026-05-16
>   Setup · 2026-05-16
>   Getting started · 2026-05-16
>   bok-scribe-seal-viralmind-v1 · 2026-05-15
>   bok-scribe-seal-conteudo-v2-v1 · 2026-05-08
>   bok-scribe-seal-mcorch-constellation-v1 · 2026-05-08
> ```

## 🤖 Claude *(00:46:44)*


## 🤖 Claude *(00:46:49)*

Validação materialmente ancorada:
- **LOC reais:** 1732 linhas (88+143+169+216+167+315+255+204+175). Sem fabricação.
- **Parent seal confirmado na malha:** `bok-scribe-seal-meta-api-v1` (2026-05-30) existe — é o pai semântico certo (marketing-hub absorve `whatsapp_leads` do meta-api). DERIVES_FROM resolverá.

**Phase 6 — traceability validation (mecânica):** MR-MH 12→BR-MH 12 (1:1, 0 órfãos) · BR-MH 12→PR-MH (todos cobertos) · PR-MH 001–014→FR-MH 001–012 (PRs 020–023 são Future, não-decompostos por decisão documentada no FRD §1) · 6 edge fns todas com JWT+secrets · todas as tabelas com RLS · mcoCoins definido nas 4 FRs AI-powered (003/004/008/010) · FMEA RPN>100 (002/003/005) todas com ação. **Zero órfãos.**

Agora autoro o seed script (Phase 7) espelhando o meta-api 1:1, e finalizo o index.

## 🤖 Claude *(00:47:43)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/seed-marketing-hub-bok-seal.ts",
  "content": "#!/usr/bin/env bun\n/**\n * Seals the BoK documentation suite for marketing-hub in the Knowledge Mesh.\n * Inserts a documentation_suite node with stability 0.85; embedding triggered\n * automatically by trg_mcorch_embed_on_insert (pg_net).\n *\n * Inserts an explicit DERIVES_FROM edge to the parent seal (meta-api v1 \u2014\n * marketing-hub absorbs whatsapp_leads from the meta-api data model and shares\n * the marketing/lead/distribution domain).\n *\n * Usage: bun run scripts/seed-marketing-hub-bok-seal.ts\n */\nimport { createClient } from '@supabase/supabase-js';\n\nconst SUPABASE_URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL;\nconst SERVICE_KEY = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY);\n\nif (!SUPABASE_URL || !SERVICE_KEY) {\n  console.error('Missing SUPABASE_URL or SB_SECRET_KEY');\n  process.exit(1);\n}\n\nconst supabase = createClient(SUPABASE_URL, SERVICE_KEY);\n\nconst PARENT_SEAL_NAME = 'bok-scribe-seal-meta-api-v1';\n\nconst sealNode = {\n  name: 'bok-scribe-seal-marketing-hub-v1',\n  node_type: 'documentation_suite',\n  project_id: 'marketing-hub',\n  stability_score: 0.85,\n  revenue_impact: 1000000, // direct-revenue enabler \u2014 m\u00f3dulo comercial per-tenant (assinatura + mcoCoins por a\u00e7\u00e3o + receita de afiliado atribu\u00edda); ancorado ao Million-BRL Roadmap, pricing deferido (OTD)\n  content: `marketing-hub \u2014 Marketing Hub agentic soberano do MCORCH (BoK v1)\n\nBoK suite (9 docs, 1732 LOC) sealed 2026-06-02 sob MCORCH Master Execution Protocol. Motivada por diretiva do Sovereign a partir de um \"Framework Universal para M\u00f3dulos de Marketing Inteligentes e Adapt\u00e1veis (Plataforma Agentic)\" (benchmarks HubSpot Marketing Hub/Breeze/AEO + Salesforce Marketing Cloud/Agentforce/Data Cloud). Decis\u00f5es de escopo travadas via AskUserQuestion: natureza Ambos (n\u00facleo interno Usu\u00e1rio Zero + superf\u00edcie comercial per-tenant); m\u00f3dulo soberano novo que ABSORVE e escala o v1 (nasce como consolida\u00e7\u00e3o v2); /bok-scribe primeiro, /bok-agents-generator depois com \u22658 agentes.\n\nVIS\u00c3O: m\u00f3dulo que percebe \u2192 decide \u2192 executa \u2192 aprende estrat\u00e9gias de growth com governan\u00e7a humana (HITL). Consolida as superf\u00edcies de marketing dispersas do MCORCH (orchestrate-content single-shot, marketing-growth Pantheon, whatsapp_leads, afiliados ML) numa \u00fanica superf\u00edcie /dashboard/marketing. REUTILIZA infra provada (mcorch_nodes/edges + pgvector HNSW 768d para Data Core/RAG; infra_health_logs + ROIWidget + affiliate_links.revenue_cents + ATTRIBUTES_REVENUE_TO para Observability/Attribution; edge functions + credenciais per-user para Connectivity; mcorch-qa-healing para Auto-cura) em vez de reconstruir.\n\nDELTA (foco do BoK): (1) camada CRM/Lead completa \u2014 capture\u2192score\u2192nurture\u2192convert, absorvendo whatsapp_leads (tutela meta-api\u2192marketing-hub, OTD-MH-001); (2) AEO (Answer Engine Optimization) \u2014 visibilidade da marca em motores de resposta de IA; (3) campaign management de 1\u00aa classe (wrap multicanal sobre orchestrate-content); (4) buyer intent + data enrichment; (5) sequ\u00eancias de nurturing email/multicanal; (6) orquestrador event-driven por inten\u00e7\u00e3o (policy engine + HITL + arbitragem).\n\nARQUITETURA: 9 tabelas novas (leads, lead_events, campaigns, campaign_steps, sequences, sequence_enrollments, marketing_consents, marketing_attribution, aeo_audits) + view customer_360 + 6 edge functions (lead-score, campaign-run, nurture-dispatch, intent-orchestrate, aeo-audit, erase-lead). CISSP CBK elevado por LGPD: STRIDE com PII de lead Critical, RLS default-deny por auth.uid(), erasure cascade via SECURITY DEFINER (espelha disconnect_*), consent gate hard pr\u00e9-nurturing, BYOK per-tenant no padr\u00e3o Vault.\n\nID SPACE: MR-MH-001..012 \u00b7 BR-MH-001..012 \u00b7 BO-MH-001..005 \u00b7 SH-MH-001..006 \u00b7 PR-MH-001..023 \u00b7 FR-MH-001..012 \u00b7 NFR-MH-001..010 \u00b7 PROC-MH-001..008 \u00b7 KPI-MH-001..009 \u00b7 FMEA-MH-001..009 \u00b7 SOL-MH-001..005 \u00b7 QO-MH-001..006 \u00b7 BAC-MH-001..006 \u00b7 OTD-MH-001..005.\n\nFMEA (9 entries, 3 RPN > 100): FMEA-MH-003 (RPN 135 \u2014 erasure cascade incompleta/PII residual; a\u00e7\u00e3o: erasure transacional + verifica\u00e7\u00e3o zero-residue + retry cr\u00edtico + teste E2E), FMEA-MH-005 (RPN 125 \u2014 provider AEO devolve cita\u00e7\u00e3o alucinada; a\u00e7\u00e3o: probe-first Lei 1 + valida\u00e7\u00e3o multi-engine + confidence + degradado documentado), FMEA-MH-002 (RPN 108 \u2014 nurturing sem consentimento/viola\u00e7\u00e3o LGPD; a\u00e7\u00e3o: consent gate hard server-side + checagem por passo + teste de regress\u00e3o).\n\nDOCUMENTOS: docs/bok/marketing-hub/{00-index 88, 01-mrd 143, 02-brd 169, 03-prd 216, 04-frd 167, 05-sdd 315, 06-data-model 255, 07-process-flow 204, 08-quality-metrics 175} \u2014 total 1732 LOC.\n\nTRACEABILITY: 100% de cobertura MR \u2192 BR \u2192 PR \u2192 FR (zero orphans). PRs de Future scope (PR-MH-020..023) intencionalmente n\u00e3o-decompostos em FR neste ciclo (documentado no FRD \u00a71). Parent seal meta-api (whatsapp_leads absorption).\n\nBoK GATE: liberado AP\u00d3S este seal. C\u00f3digo de produ\u00e7\u00e3o s\u00f3 inicia ap\u00f3s /bok-agents-generator (\u22658 agentes reconciliados com o Pantheon) + migrations com /security-review aprovadas. Scope-lock: .claude/context/marketing-hub-scope-lock-2026-06-02.md.`,\n  metadata: {\n    bok_version: '1.0.0',\n    documents: [\n      '00-index',\n      '01-mrd',\n      '02-brd',\n      '03-prd',\n      '04-frd',\n      '05-sdd',\n      '06-data-model',\n      '07-process-flow',\n      '08-quality-metrics',\n    ],\n    document_lines: {\n      '00-index': 88,\n      '01-mrd': 143,\n      '02-brd': 169,\n      '03-prd': 216,\n      '04-frd': 167,\n      '05-sdd': 315,\n      '06-data-model': 255,\n      '07-process-flow': 204,\n      '08-quality-metrics': 175,\n      total: 1732,\n    },\n    phase_completed: 'Phase 7',\n    traceability_validated: true,\n    traceability_orphans: 0,\n    bok_gate: 'fresh-completion',\n    drift_reconciled: 0,\n    drift_pending: 0,\n    market_segment: 'B2B2C',\n    monetization_model: 'hybrid',\n    regulatory_profile: 'LGPD+GDPR',\n    integration_surface: 'extends-mcorch',\n    project_slug: 'marketing-hub',\n    sprint_introduced: 'v6.21.0',\n    sprint_sealed: 'pending-handoff',\n    tags: ['bok-scribe', 'marketing-hub', 'B2B2C', 'agentic', 'crm', 'lead-scoring', 'nurturing', 'aeo', 'campaign-management', 'attribution', 'lgpd', 'gdpr', 'per-user-tenancy', 'v2-consolidation'],\n    modules: [\n      'Lead Core (capture\u2192score\u2192nurture\u2192convert; absorve whatsapp_leads)',\n      'Campaign Core (multicanal sobre orchestrate-content)',\n      'AEO Engine (Answer Engine Optimization)',\n      'Intent Orchestrator + HITL policy engine',\n      'Nurturing Sequences (drip)',\n      'Attribution + Customer 360',\n    ],\n    new_tables: 9,\n    new_views: 1,\n    new_columns: 0,\n    new_edge_functions: 6,\n    extended_edge_functions: 1, // orchestrate-content reused as campaign executor\n    new_rpcs: 1, // erase_lead (SECURITY DEFINER); reuses deduct_mco_coins\n    new_migrations: 7,\n    id_ranges: {\n      MR: '001..012',\n      BR: '001..012',\n      BO: '001..005',\n      SH: '001..006',\n      PR: '001..023',\n      FR: '001..012',\n      NFR: '001..010',\n      PROC: '001..008',\n      KPI: '001..009',\n      FMEA: '001..009',\n      SOL: '001..005',\n      QO: '001..006',\n      BAC: '001..006',\n      OTD: '001..005',\n    },\n    fmea_rpn_over_100: ['FMEA-MH-002', 'FMEA-MH-003', 'FMEA-MH-005'],\n    fmea_rpn_top: {\n      'FMEA-MH-003': 135,\n      'FMEA-MH-005': 125,\n      'FMEA-MH-002': 108,\n    },\n    derives_from: PARENT_SEAL_NAME,\n    depends_on_sop: '.claude/context/marketing-hub-scope-lock-2026-06-02.md',\n    motivating_incident: 'Sovereign directive \u2014 Framework Universal de Marketing (Plataforma Agentic) \u2192 m\u00f3dulo marketing-hub v2',\n    revenue_impact_basis: 'commercial-marketing-module-per-tenant-monetization (Million-BRL Roadmap anchor; pricing deferred OTD)',\n    reuses: ['mcorch_nodes/edges', 'pgvector HNSW 768d', 'infra_health_logs', 'ROIWidget', 'affiliate_links.revenue_cents', 'ATTRIBUTES_REVENUE_TO', 'orchestrate-content', 'deduct_mco_coins RPC', 'mcorch-qa-healing', 'marketing-growth Pantheon'],\n    absorbs: ['whatsapp_leads (tutela meta-api\u2192marketing-hub, OTD-MH-001)', 'orchestrate-content (single-shot \u2192 campaign executor)', 'marketing-growth Pantheon agent (elevated, not recreated)'],\n    related_otds: ['OTD-MH-001', 'OTD-MH-002', 'OTD-MH-003', 'OTD-MH-004', 'OTD-MH-005'],\n    next_step: '/bok-agents-generator marketing-hub (\u22658 agents, reconciled with Pantheon)',\n    skips: ['White-label tenant billing portal', 'Native paid-ads buying (Google/Meta Ads spend)', 'Multimodal video-ad generation beyond Canvas Studio'],\n  },\n};\n\nconsole.log(`\ud83d\udcdd Sealing BoK suite \"marketing-hub\"...`);\nconsole.log(`   Project: ${sealNode.project_id}`);\nconsole.log(`   Stability: ${sealNode.stability_score}`);\nconsole.log(`   Revenue impact: ${sealNode.revenue_impact} (${sealNode.metadata.monetization_model})`);\nconsole.log(`   BoK gate: ${sealNode.metadata.bok_gate}`);\nconsole.log(`   Parent (DERIVES_FROM): ${PARENT_SEAL_NAME}`);\n\n// Idempotency check: skip if already exists\nconst { data: existing } = await supabase\n  .from('mcorch_nodes')\n  .select('id, name, created_at')\n  .eq('name', sealNode.name)\n  .maybeSingle();\n\nif (existing) {\n  console.log(`\\n\u26a0\ufe0f Seal node already exists (idempotent skip):`);\n  console.log(`   ID:        ${existing.id}`);\n  console.log(`   Name:      ${existing.name}`);\n  console.log(`   Created:   ${existing.created_at}`);\n  console.log(`\\nNo new INSERT performed.`);\n  process.exit(0);\n}\n\n// Step 1: INSERT documentation_suite node\nconst { data: insertedNode, error: nodeError } = await supabase\n  .from('mcorch_nodes')\n  .insert(sealNode)\n  .select('id, name, node_type, stability_score, created_at')\n  .single();\n\nif (nodeError) {\n  console.error('\u274c Seal node insert failed:', nodeError);\n  process.exit(1);\n}\n\nconsole.log(`\\n\u2705 Seal node inserted:`);\nconsole.log(`   ID:        ${insertedNode.id}`);\nconsole.log(`   Name:      ${insertedNode.name}`);\nconsole.log(`   Type:      ${insertedNode.node_type}`);\nconsole.log(`   Stability: ${insertedNode.stability_score}`);\nconsole.log(`   Created:   ${insertedNode.created_at}`);\n\n// Step 2: Resolve parent seal UUID for DERIVES_FROM edge\nconst { data: parent, error: parentError } = await supabase\n  .from('mcorch_nodes')\n  .select('id, name')\n  .eq('name', PARENT_SEAL_NAME)\n  .single();\n\nif (parentError || !parent) {\n  console.error(`\\n\u274c Parent seal lookup failed for ${PARENT_SEAL_NAME}:`, parentError);\n  console.error('   Skipping DERIVES_FROM edge insert. Manual cleanup may be required.');\n  process.exit(1);\n}\n\nconsole.log(`\\n\ud83d\udd17 Parent seal resolved:`);\nconsole.log(`   ID:        ${parent.id}`);\nconsole.log(`   Name:      ${parent.name}`);\n\n// Step 3: INSERT DERIVES_FROM edge\nconst { data: insertedEdge, error: edgeError } = await supabase\n  .from('mcorch_edges')\n  .insert({\n    source_id: insertedNode.id,\n    target_id: parent.id,\n    relation_type: 'DERIVES_FROM',\n    weight: 1.0,\n    project_id: 'marketing-hub',\n    metadata: {\n      lineage: 'bok-scribe-seal',\n      source_seal: insertedNode.name,\n      target_seal: parent.name,\n      sealed_at: insertedNode.created_at,\n    },\n  })\n  .select('id, source_id, target_id, relation_type, created_at')\n  .single();\n\nif (edgeError) {\n  console.error('\u274c DERIVES_FROM edge insert failed:', edgeError);\n  process.exit(1);\n}\n\nconsole.log(`\\n\u2705 DERIVES_FROM edge inserted:`);\nconsole.log(`   ID:        ${insertedEdge.id}`);\nconsole.log(`   Source:    ${insertedEdge.source_id} (${insertedNode.name})`);\nconsole.log(`   Target:    ${insertedEdge.target_id} (${parent.name})`);\nconsole.log(`   Relation:  ${insertedEdge.relation_type}`);\nconsole.log(`   Created:   ${insertedEdge.created_at}`);\n\nconsole.log(`\\n\ud83e\udde0 Embedding will be generated automatically by trg_mcorch_embed_on_insert (ass\u00edncrono via pg_net).`);\nconsole.log(`   Confirm with: SELECT embedding IS NOT NULL FROM mcorch_nodes WHERE id = '${insertedNode.id}';`);\nconsole.log(`\\n\ud83d\udcca Material proof summary for handoff:`);\nconsole.log(`   - documentation_suite node UUID: ${insertedNode.id}`);\nconsole.log(`   - DERIVES_FROM edge UUID:        ${insertedEdge.id}`);\nconsole.log(`   - Parent seal UUID:              ${parent.id}`);\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/scripts/seed-marketing-hub-bok-seal.ts (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:47:57)*


## 🤖 Claude *(00:47:58)*

Phase 7 seed script autorado (com LOC reais e parent confirmado). Finalizo o **00-index** (registry + phase log → complete, Phase 6/7).

## 🤖 Claude *(00:48:05)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/00-index.md",
  "old_string": "| 3 | `03-prd.md` | Product Requirements Document | ProdBOK + CXBOK | [ ] pending |\n| 4 | `04-frd.md` | Functional Requirements Document | SWEBOK v4 | [ ] pending |\n| 5 | `05-sdd.md` | System Design Document | SWEBOK v4 + CISSP CBK | [ ] pending |\n| 6 | `06-data-model.md` | Data & Knowledge Model | DMBOK v2 | [ ] pending |\n| 7 | `07-process-flow.md` | Process & Automation Blueprint | BPM CBOK v4 | [ ] pending |\n| 8 | `08-quality-metrics.md` | Self-Optimization Specification | CMQ/OE BOK | [ ] pending |\n| + | `bok-agents-system--marketing-hub.md` | Agent System (\u22658 agents) | `/bok-agents-generator` | [ ] pending (post-scribe) |",
  "new_string": "| 3 | `03-prd.md` | Product Requirements Document | ProdBOK + CXBOK | [x] complete |\n| 4 | `04-frd.md` | Functional Requirements Document | SWEBOK v4 | [x] complete |\n| 5 | `05-sdd.md` | System Design Document | SWEBOK v4 + CISSP CBK | [x] complete |\n| 6 | `06-data-model.md` | Data & Knowledge Model | DMBOK v2 | [x] complete |\n| 7 | `07-process-flow.md` | Process & Automation Blueprint | BPM CBOK v4 | [x] complete |\n| 8 | `08-quality-metrics.md` | Self-Optimization Specification | CMQ/OE BOK | [x] complete |\n| + | `bok-agents-system--marketing-hub.md` | Agent System (\u22658 agents) | `/bok-agents-generator` | [ ] pending (next step \u2014 post-scribe) |\n\n**Suite LOC:** 1732 (00:88 \u00b7 01:143 \u00b7 02:169 \u00b7 03:216 \u00b7 04:167 \u00b7 05:315 \u00b7 06:255 \u00b7 07:204 \u00b7 08:175). **Traceability:** validated, 0 orphans."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/00-index.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:48:07)*


## 🤖 Claude *(00:48:13)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/00-index.md",
  "old_string": "| 2 | Product Definition | [ ] | \u2014 |\n| 3 | Technical Specification | [ ] | \u2014 |\n| 4 | Data & Process Engineering | [ ] | \u2014 |\n| 5 | Quality & Autonomic Engineering | [ ] | \u2014 |\n| 6 | Traceability Validation | [ ] | \u2014 |\n| 7 | Knowledge Mesh Injection | [ ] | \u2014 |",
  "new_string": "| 2 | Product Definition | 2026-06-02 | PRD (23 PR-MH, 2 personas, journeys) |\n| 3 | Technical Specification | 2026-06-02 | FRD (12 FR-MH/10 NFR-MH) + SDD (STRIDE, RLS, 6 edge fns, 5 OTD-MH) |\n| 4 | Data & Process Engineering | 2026-06-02 | 9 tables + customer_360 view; 8 PROC-MH; n8n nurture cron |\n| 5 | Quality & Autonomic Engineering | 2026-06-02 | 9 FMEA-MH (3 RPN>100), 9 KPI-MH, 5 SOL-MH |\n| 6 | Traceability Validation | 2026-06-02 | \u2705 0 orphans; Future PRs (020-023) intentionally not FR-decomposed |\n| 7 | Knowledge Mesh Injection | pending GO | Seed script authored: `scripts/seed-marketing-hub-bok-seal.ts` (DERIVES_FROM meta-api); INSERT gated on Sovereign GO |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/00-index.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:48:30)*


## 🤖 Claude *(00:48:31)*

Suite completa + seed script + index finalizado. Verificação material final (Lei 1) antes de reportar — BoK gate 9/9 + ls com bytes.

## 🤖 Claude *(00:48:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"\u2500\u2500\u2500 BoK gate completeness (marketing-hub) \u2500\u2500\u2500\"\nrequired=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\nmissing=()\nfor doc in \"${required[@]}\"; do [ -f \"docs/bok/marketing-hub/$doc.md\" ] || missing+=(\"$doc\"); done\n[ ${#missing[@]} -eq 0 ] && echo \"\u2705 marketing-hub \u2014 complete (9/9)\" || echo \"\u26a0\ufe0f missing: ${missing[*]}\"\necho \"\"; echo \"\u2500\u2500\u2500 ls -la (bytes + timestamp) \u2500\u2500\u2500\"; ls -la docs/bok/marketing-hub/ ; echo \"\"; ls -la scripts/seed-marketing-hub-bok-seal.ts\necho \"\"; echo \"\u2500\u2500\u2500 seed script sintaxe (bun check, sem executar) \u2500\u2500\u2500\"; bun build scripts/seed-marketing-hub-bok-seal.ts --target=bun > /dev/null 2>&1 && echo \"\u2705 seed script compila (bun build dry)\" || echo \"\u26a0\ufe0f erro de sintaxe no seed script\"",
  "description": "Final material verification: BoK gate 9/9 + file sizes + seed script syntax"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ─── BoK gate completeness (marketing-hub) ───
> ✅ marketing-hub — complete (9/9)
> 
> ─── ls -la (bytes + timestamp) ───
> total 132
> drwxrwxr-x  2 ubuntu ubuntu  4096 Jun  2 21:48 .
> drwxrwxr-x 15 ubuntu ubuntu  4096 Jun  2 21:33 ..
> -rw-rw-r--  1 ubuntu ubuntu  5413 Jun  2 21:48 00-index.md
> -rw-rw-r--  1 ubuntu ubuntu 12666 Jun  2 21:35 01-mrd.md
> -rw-rw-r--  1 ubuntu ubuntu 12383 Jun  2 21:36 02-brd.md
> -rw-rw-r--  1 ubuntu ubuntu 12253 Jun  2 21:38 03-prd.md
> -rw-rw-r--  1 ubuntu ubuntu  9391 Jun  2 21:39 04-frd.md
> -rw-rw-r--  1 ubuntu ubuntu 18001 Jun  2 21:41 05-sdd.md
> -rw-rw-r--  1 ubuntu ubuntu 13368 Jun  2 21:42 06-data-model.md
> -rw-rw-r--  1 ubuntu ubuntu  9629 Jun  2 21:43 07-process-flow.md
> -rw-rw-r--  1 ubuntu ubuntu 10974 Jun  2 21:44 08-quality-metrics.md
> 
> -rw-rw-r-- 1 ubuntu ubuntu 12176 Jun  2 21:47 scripts/seed-marketing-hub-bok-seal.ts
> 
> ─── seed script sintaxe (bun check, sem executar) ───
> ✅ seed script compila (bun build dry)
> ```

## 🤖 Claude *(00:49:11)*


## 🤖 Claude *(00:49:30)*

BoK suite **marketing-hub** completa e verificada materialmente. Resumo:

## 📚 Suíte BoK `marketing-hub` — 9/9 selada (Phase 0–7 authored)

| # | Arquivo | Documento | BoK | LOC |
|---|---------|-----------|-----|-----|
| 0 | `00-index.md` | Project Manifest + registry + 5 OTD-MH | — | 88 |
| 1 | `01-mrd.md` | Market Requirements (12 MR-MH, TAM/SAM/SOM, HubSpot/Salesforce/RD competitive) | BABOK v3 | 143 |
| 2 | `02-brd.md` | Business Requirements (12 BR-MH, 5 BO-MH SMART, ROI, mcoCoins econ, riscos) | BABOK v3 | 169 |
| 3 | `03-prd.md` | Product Requirements (23 PR-MH MoSCoW, 2 personas, journeys, Gherkin) | ProdBOK+CXBOK | 216 |
| 4 | `04-frd.md` | Functional Requirements (12 FR-MH, 10 NFR-MH, contratos, test matrix) | SWEBOK v4 | 167 |
| 5 | `05-sdd.md` | System Design (arquitetura, STRIDE, RLS, 6 edge fns, secrets, 5 OTD-MH) | SWEBOK+CISSP | 315 |
| 6 | `06-data-model.md` | 9 tabelas + view `customer_360`, GraphRAG nodes/edges, isolamento, LGPD retention | DMBOK v2 | 255 |
| 7 | `07-process-flow.md` | 8 PROC-MH, BPMN-lite, n8n nurture cron, erasure flow | BPM CBOK v4 | 204 |
| 8 | `08-quality-metrics.md` | 9 FMEA-MH (3 RPN>100), 9 KPI-MH, 5 SOL-MH, self-heal, SLA/SLO | CMQ/OE | 175 |
| + | `scripts/seed-marketing-hub-bok-seal.ts` | Seed do mesh seal (node+edge) | — | (12.2 KB) |

**Provas materiais (Lei 1, verificadas neste turno):**
- ✅ BoK gate **9/9 complete** · **1732 LOC** reais (`wc -l`) · `ls -la` confirma os 9 arquivos + seed
- ✅ Traceability **0 órfãos** — MR-MH 12→BR-MH 12→PR-MH→FR-MH 12; FMEA RPN>100 (135/125/108) todas com ação; mcoCoins nas 4 FRs AI-powered; RLS em toda tabela PII
- ✅ Seed script **compila** (`bun build` dry) · parent `bok-scribe-seal-meta-api-v1` **confirmado na malha** (2026-05-30) → `DERIVES_FROM` resolverá
- ⏸️ **Mesh INSERT NÃO executado** — é mutação de produção, gated em você (Cérebro com mãos, mas aguardando GO)

**Destaques de design:** o módulo **absorve** `whatsapp_leads` (tutela meta-api→marketing-hub, OTD-MH-001), **reusa** `orchestrate-content` como executor de campanha (não duplica), e eleva o LGPD a Critical (erasure cascade espelhando `disconnect_*`, consent gate hard pré-nurturing). Os agentes do delta (AEO/Intent/Demand-gen) e o runtime ficam decididos no `/bok-agents-generator` (OTD-MH-002).

> **Survival Laws:** Lei 1 ✅ (LOC/bytes/parent/traceability provados, zero fabricação; seal gated). Lei 2 ✅ (BoK É o processo antecipado; scope-lock em disco antes). Lei 4 ✅ (ORO declarado).

**BoK Scribe documentation suite complete for `marketing-hub`.** O BoK Gate está satisfeito — código liberado após o `/bok-agents-generator` + migrations com `/security-review`.

Como seguir? (o seal na malha e o commit não rodaram — decisão sua)

## 🤖 Claude *(00:49:36)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "Su\u00edte BoK marketing-hub completa (9/9, 1732 LOC, 0 \u00f3rf\u00e3os). O seed de selo na malha est\u00e1 pronto mas N\u00c3O-executado (muta\u00e7\u00e3o de produ\u00e7\u00e3o). Como seguir?",
      "header": "Pr\u00f3ximo passo",
      "multiSelect": false,
      "options": [
        {
          "label": "Selar malha + /bok-agents-generator",
          "description": "Executo seed-marketing-hub-bok-seal.ts (insere o n\u00f3 documentation_suite + edge DERIVES_FROM meta-api na malha, com prova material) e na sequ\u00eancia rodo o /bok-agents-generator (\u22658 agentes reconciliados com o Pantheon). Commit fica para o /handoff."
        },
        {
          "label": "Selar malha, e parar aqui",
          "description": "Executo o seal na malha agora, mas seguro o /bok-agents-generator para voc\u00ea revisar os 9 docs antes de gerar o cat\u00e1logo de agentes."
        },
        {
          "label": "Revisar os docs antes de selar",
          "description": "N\u00e3o executo nada na malha ainda. Voc\u00ea l\u00ea a su\u00edte em docs/bok/marketing-hub/ e eu ajusto o que precisar; selo + agents-generator depois do seu OK."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "Suíte BoK marketing-hub completa (9/9, 1732 LOC, 0 órfãos). O seed de selo na malha está pronto mas NÃO-executado (mutação de produção). Como seguir?"="Selar malha + /bok-agents-generator". You can now continue with these answers in mind.
> ```

## 🤖 Claude *(00:56:49)*


## 🤖 Claude *(00:56:50)*

**GO recebido.** Executo o seal na malha (mutação de produção autorizada) e na sequência sigo pro `/bok-agents-generator`.

**Phase 7 — Mesh Injection (executando):**

## 🤖 Claude *(00:56:52)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "bun run scripts/seed-marketing-hub-bok-seal.ts 2>&1",
  "description": "Execute marketing-hub BoK mesh seal (node + DERIVES_FROM edge)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 📝 Sealing BoK suite "marketing-hub"...
>    Project: marketing-hub
>    Stability: 0.85
>    Revenue impact: 1000000 (hybrid)
>    BoK gate: fresh-completion
>    Parent (DERIVES_FROM): bok-scribe-seal-meta-api-v1
> 
> ✅ Seal node inserted:
>    ID:        d5163fed-da85-4f95-8445-0d0aa5b6bafe
>    Name:      bok-scribe-seal-marketing-hub-v1
>    Type:      documentation_suite
>    Stability: 0.85
>    Created:   2026-06-03T00:56:53.82819+00:00
> 
> 🔗 Parent seal resolved:
>    ID:        ca791bdd-cf7c-48cc-811a-fd2f7e99870f
>    Name:      bok-scribe-seal-meta-api-v1
> 
> ✅ DERIVES_FROM edge inserted:
>    ID:        918f6d90-2207-4964-ad73-4fc0b0464a99
>    Source:    d5163fed-da85-4f95-8445-0d0aa5b6bafe (bok-scribe-seal-marketing-hub-v1)
>    Target:    ca791bdd-cf7c-48cc-811a-fd2f7e99870f (bok-scribe-seal-meta-api-v1)
>    Relation:  DERIVES_FROM
>    Created:   2026-06-03T00:56:54.173278+00:00
> 
> 🧠 Embedding will be generated automatically by trg_mcorch_embed_on_insert (assíncrono via pg_net).
>    Confirm with: SELECT embedding IS NOT NULL FROM mcorch_nodes WHERE id = 'd5163fed-da85-4f95-8445-0d0aa5b6bafe';
> 
> 📊 Material proof summary for handoff:
>    - documentation_suite node UUID: d5163fed-da85-4f95-8445-0d0aa5b6bafe
>    - DERIVES_FROM edge UUID:        918f6d90-2207-4964-ad73-4fc0b0464a99
>    - Parent seal UUID:              ca791bdd-cf7c-48cc-811a-fd2f7e99870f
> ```

## 🤖 Claude *(00:57:03)*


## 🤖 Claude *(00:57:05)*

Seal **materialmente inserido** na malha:
- 🟢 node `d5163fed-da85-4f95-8445-0d0aa5b6bafe` (`bok-scribe-seal-marketing-hub-v1`, stability 0.85)
- 🔗 edge `918f6d90-2207-4964-ad73-4fc0b0464a99` (`DERIVES_FROM` → meta-api `ca791bdd`)

Confirmo o embedding autônomo (pg_net é assíncrono — dou um instante e checo):

## 🤖 Claude *(00:57:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "set -a; source .env 2>/dev/null; set +a\nURL=\"${SUPABASE_URL:-$VITE_SUPABASE_URL}\"; KEY=\"${SB_SECRET_KEY:-$SUPABASE_SERVICE_ROLE_KEY}\"\nNODE=\"d5163fed-da85-4f95-8445-0d0aa5b6bafe\"\n# poll embedding up to ~25s (autoembed via pg_net is async)\nfor i in 1 2 3 4 5; do\n  R=$(curl -s \"$URL/rest/v1/mcorch_nodes?id=eq.$NODE&select=name,embedding\" -H \"apikey: $KEY\" -H \"Authorization: Bearer $KEY\" \\\n      | python3 -c \"import json,sys; d=json.load(sys.stdin); n=d[0] if d else {}; e=n.get('embedding'); print('EMBEDDED' if e else 'NULL', '\u00b7', (len(json.loads(e)) if isinstance(e,str) else (len(e) if e else 0)), 'dims')\" 2>/dev/null)\n  echo \"try $i: $R\"\n  echo \"$R\" | grep -q EMBEDDED && break\n  command sleep 5 2>/dev/null || true\ndone",
  "description": "Poll for autonomous embedding on the seal node"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> try 1: EMBEDDED · 768 dims
> ```

## 🤖 Claude *(00:57:44)*


## 🤖 Claude *(00:57:47)*

**Mesh seal materialmente confirmado:**
- 🟢 node `d5163fed-da85-4f95-8445-0d0aa5b6bafe` — **embedded 768d** (autoembed via pg_net, 1ª tentativa)
- 🔗 edge `918f6d90-2207-4964-ad73-4fc0b0464a99` — `DERIVES_FROM` → meta-api
- Malha **8754 nós** (8753 + este seal)

Phase 7 fechada. Agora o **`/bok-agents-generator`** — com o requisito que você cravou (≥8 agentes), reconciliado com o Pantheon.

## 🤖 Claude *(00:57:47)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "6",
  "status": "completed"
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #6 status
> ```

## 🤖 Claude *(00:57:49)*


🛠️ **Tool Call**: `TaskCreate`
```json
{
  "subject": "bok-agents-generator \u2014 marketing-hub (\u22658 agents)",
  "description": "Run /bok-agents-generator \u2192 docs/bok/marketing-hub/bok-agents-system--marketing-hub.md. 8 BoK agents (BABOK/EABOK/DMBOK/BPM/SWEBOK/CISSP/CXBOK/ProdBOK) + 3 delta agents (AEO, Intent Orchestrator, Demand-gen). Reconcile with Pantheon marketing-growth L1 (elevate, not recreate). 3 cross-agent layers. Anchor to MR-MH/BR-MH/PR-MH/FR-MH + SDD tables/edge fns.",
  "activeForm": "Generating agent system (\u22658 agents)"
}
```

> **Tool Result (TaskCreate)** - ✅ Success
>
> ```
> Task #7 created successfully: bok-agents-generator — marketing-hub (≥8 agents)
> ```

## 🤖 Claude *(00:58:06)*


🛠️ **Tool Call**: `Skill`
```json
{
  "skill": "anthropic-skills:bok-agents-generator",
  "args": "marketing-hub \u2014 gerar o sistema de agentes operacionais para o m\u00f3dulo Marketing Hub agentic do MCORCH Constellation. CONTEXTO: su\u00edte BoK selada em docs/bok/marketing-hub/ (9 docs, 1732 LOC; mesh seal d5163fed) + scope-lock em .claude/context/marketing-hub-scope-lock-2026-06-02.md. OUTPUT: docs/bok/marketing-hub/bok-agents-system--marketing-hub.md (mesmo padr\u00e3o dos bok-agents-system--<slug>.md j\u00e1 existentes em meta-api/mercado-livre-api/conteudo-v2/constellation-v2/mcorch-constellation).\n\nREQUISITO SOVEREIGN: \u22658 agentes \u2014 gerar os 8 BoK-driven (Business Analysis/BABOK \u00b7 Enterprise Architecture/EABOK \u00b7 Data Management/DMBOK \u00b7 Process/BPM CBOK \u00b7 Software Engineering/SWEBOK \u00b7 Cybersecurity/CISSP CBK \u00b7 Customer Experience/CXBOK \u00b7 Product Management/ProdBOK) MAIS 3 agentes do delta deste m\u00f3dulo: (9) Agente AEO \u2014 Answer Engine Optimization (visibilidade/cita\u00e7\u00e3o da marca em motores de resposta de IA); (10) Agente de Orquestra\u00e7\u00e3o de Inten\u00e7\u00e3o (intent\u2192tasks, policy engine, HITL, arbitragem); (11) Agente de Demand-gen/Growth (lead lifecycle, nurturing, scoring). Total alvo = 11 agentes.\n\nESTRUTURA por agente: Purpose \u00b7 Core Capabilities \u00b7 Skills \u00b7 Inputs \u00b7 Outputs \u00b7 Decision Scope \u00b7 Tools & Integrations \u00b7 KPIs \u00b7 Use Cases \u00b7 Collaboration Map. Categorizar cada um como Copilot OU Agente Aut\u00f4nomo. Incluir as 3 camadas cross-agent: Orchestration Model (event-driven baseado em inten\u00e7\u00e3o), Intelligent Engineering Layer (7 dimens\u00f5es: Pessoas/Processos/Tecnologia/Dados/Conhecimento/Valor/Impacto Sustent\u00e1vel), Cross-Cutting Enablers (5).\n\nANCORAR no MCORCH concreto (n\u00e3o gen\u00e9rico): referenciar os IDs MR-MH/BR-MH/PR-MH/FR-MH e as tabelas/edge functions do SDD (leads, campaigns, sequences, aeo_audits, marketing_consents, marketing_attribution; lead-score, campaign-run, nurture-dispatch, intent-orchestrate, aeo-audit, erase-lead). RECONCILIAR com o Pantheon OpenClaw existente \u2014 o agente marketing-growth (L1 Head) N\u00c3O \u00e9 recriado, \u00e9 elevado/conectado; referenciar engineer/scientist/artisan/guardian onde colaboram. REUTILIZAR infra (mcorch_nodes/edges malha, ROIWidget/ATTRIBUTES_REVENUE_TO, credenciais per-user, mcorch-qa-healing, deduct_mco_coins). GOVERNAN\u00c7A: LGPD/GDPR by design, HITL em alto impacto, XAI/explicabilidade, RLS per-tenant. Idioma: corpo do doc em ingl\u00eas (headings/labels), pode ter notas executivas pt-BR."
}
```

> **Tool Result (Skill)** - ✅ Success
>
> ```
> Launching skill: anthropic-skills:bok-agents-generator
> ```

## 👤 User *(00:58:06)*

Base directory for this skill: /home/ubuntu/.claude/remote/plugins/0544a7df7ccbcec2/skills/bok-agents-generator

# BoK Agents Generator

Generates a full **8-agent AI system** grounded in enterprise Bodies of Knowledge, plus the three
cross-agent layers that make them interoperable as a living system.

**System Identity — always include this block at the top of every generated document:**
```
# SOFTWARE ENGINEERING INTELLIGENCE
## KNOWLEDGE CORE v2.0.0 | STATUS: ONLINE

> Integrated Body of Knowledge for Engineering, Architecture, Delivery,
> Security, Experience and Product Excellence
>
> **OUTCOMES:** Better Knowledge · Better Decisions · Better Outcomes
> **ONE KNOWLEDGE ECOSYSTEM. INFINITE POSSIBILITIES.**
```

**System Footer — always include this block at the end of every generated document:**
```
---
→ ALIGN  →  INTEGRATE  →  OPTIMIZE  →  INNOVATE  →  TRANSFORM  →  DELIVER VALUE

**SYSTEM STATUS: ALL SYSTEMS OPERATIONAL**
```

---

## Execution Flow

### Step 1 — Context Capture

Before generating, check if the user provided any of these optional context inputs:

| Input | Examples |
|---|---|
| **Industry** | Fintech, Healthcare, Retail, Manufacturing, SaaS |
| **Company maturity** | Startup, Scale-up, Mid-market, Enterprise |
| **Digital capabilities** | Low / Medium / High / AI-native |
| **Business model** | B2B, B2C, B2B2C, Marketplace, Platform |

If no context is provided → generate the **generic enterprise-ready version** (explicitly note this at the top of the output).

If context is provided → adapt every agent's Use Cases, Tools, and KPIs to that context.

---

### Step 2 — Generate All 8 BoK Agents

Generate agents in this exact order. Each agent uses the **strict output format** below.

**Agent order:**
1. BABOK — Business Analysis
2. EABOK — Enterprise Architecture
3. DMBOK — Data Management
4. BPM CBOK — Business Process Management
5. SWEBOK — Software Engineering
6. CISSP CBK — Cybersecurity
7. CXBOK — Customer Experience
8. ProdBOK — Product Management

---

### Strict Output Format Per Agent

```
---

🤖 Agent: [BoK Name] — [Domain Label]

### 1. Purpose
[2–3 sentence strategic description. What this agent owns in a business context. NOT a textbook definition.]

### 2. Core Capabilities
[6–10 capabilities directly derived from the BoK. Noun phrases, not verbs.]

### 3. Skills (Operational Level)
[Bullet list. Action-oriented. Each skill starts with a verb. Map to the capabilities above.]

### 4. Inputs
[What this agent needs to operate: data, documents, signals, systems, events.]

### 5. Outputs
[Deliverables, insights, decisions, artifacts this agent produces.]

### 6. Decision Scope
[What decisions this agent can autonomously support or recommend. Be specific about autonomy level.]

### 7. Tools & Integrations
[Platforms, systems, APIs this agent typically connects to. Real tool names.]

### 8. KPIs / Success Metrics
[Business + operational metrics. Mix leading and lagging indicators.]

### 9. Example Use Cases
[3 real-world scenarios. Format: **Scenario Title** — 2-sentence description of the problem + value created.]

### 10. Collaboration Map
[How this agent interfaces with other BoK agents. Format: → AgentName: [nature of dependency or data flow]]
```

---

### Step 3 — Cross-Agent Layers

After all 8 agents, generate the three cross-agent sections:

#### 3a. Orchestration Model

```
---

## 🔄 Orchestration Model

Describe the end-to-end flow: how agents activate each other, share outputs, and form closed loops.
Include:
- Which agent is the primary orchestrator (or if orchestration is event-driven)
- Trigger conditions (what activates the system)
- Key handoff points between agents
- Feedback loops
- Conflict resolution (when two agents have overlapping scope)
```

#### 3b. Intelligent Engineering Layer

```
---

## 🧠 Intelligent Engineering Layer

Explain how the system integrates across SEVEN dimensions (as defined in the Knowledge Core):

| Dimension | Description |
|---|---|
| **People** | How agents augment human roles and teams |
| **Process** | How agents embed into business workflows |
| **Technology** | Infrastructure and platform requirements |
| **Data** | Data flows, quality gates, and knowledge graph |
| **Knowledge** | How agents learn, update, and share knowledge |
| **Value** | How the system translates agent outputs into business value |
| **Sustainable Impact** | How the system generates outcomes that endure — environmental, social, and economic sustainability of the decisions made by the agent ecosystem |
```

#### 3c. Cross-Cutting Enablers

```
---

## ⚙️ Cross-Cutting Enablers

Define how these five capabilities are embedded across ALL agents (not per-agent — system-wide):

1. **Systems Thinking** — [How the system models interdependencies]
2. **Analytics & Metrics** — [Shared observability layer]
3. **Collaboration & Communication** — [Inter-agent and human-agent protocols]
4. **Automation & Tooling** — [Shared automation infrastructure]
5. **Ethics, Compliance & Sustainability** — [Governance model across agents]
```

---

## Quality Rules

Apply these rules during generation — do NOT repeat them in the output:

- **No textbook definitions** — every section must describe execution, not theory
- **No capability repetition** across agents unless absolutely necessary (flag it when it occurs)
- **Tools must be real** — no invented platform names
- **Collaboration Map must form a coherent graph** — every agent must connect to at least 3 others
- **Use Cases must be industry-specific** if context was provided
- **KPIs must be measurable** — no vague metrics like "improved quality"
- **Decision Scope must distinguish** between autonomous recommendation vs. human-in-the-loop

---

## Output — Write to File (Primary Delivery Mode)

This skill runs in **Claude Code (terminal)**. Output is always written to disk as a `.md` file.
Do NOT print the full content to the terminal — write the file, then confirm to the user.

### File naming convention
```
bok-agents-system[--<slug>].md
```
- No context provided → `bok-agents-system.md`
- Context provided → slugify the industry + maturity, e.g. `bok-agents-system--fintech-enterprise.md`

### Output path
Write to the **current working directory** unless the user specifies otherwise.
If a path is specified, respect it exactly.

### Write procedure (execute in this order)
1. Compose the full document in memory following Steps 1–3
2. Write to file using the bash tool or Python `open()` — single write operation
3. Print a short confirmation to the terminal:
   ```
   ✅ BoK Agents System written to: ./bok-agents-system--<slug>.md
   📄 Agents: 8 | Sections: 10 per agent + 3 cross-agent layers
   📁 Size: ~<N> KB
   ```
4. Do NOT print the document content to stdout

### Document structure (inside the .md file)
- H1 title: `# BoK Agents System — [Context or "Enterprise-Ready Generic Version"]`
- If context was provided: frontmatter metadata block at the top:
  ```markdown
  > **Context applied:** Industry: X | Maturity: Y | Digital capabilities: Z | Model: W
  ```
- Use `##` for each agent header (`## 🤖 Agent: BABOK — Business Analysis`)
- Use `###` for the 10 section headers within each agent
- Use `---` as horizontal rule between agents
- Use `##` for the three cross-agent layer headers
- Emoji headers exactly as specified (🤖, 🔄, 🧠, ⚙️)

### Context adaptation rules (when context is provided)
Adapt these fields per agent — everything else stays structurally consistent:
- **Use Cases** → scenarios specific to the provided industry and maturity level
- **Tools & Integrations** → prioritize tools common in that industry/stack
- **KPIs** → benchmark values calibrated to maturity level (startup vs. enterprise targets differ)
- **Decision Scope** → autonomy level adjusted to digital capability maturity (Low = more human-in-loop)

Do NOT adapt: agent Purpose, Core Capabilities, Skills structure, or the cross-agent layers topology.

---

## Reference: BoK Domain Map

See `references/bok-domains.md` for the authoritative list of capabilities per BoK, used to
validate that generated capabilities are grounded in the actual body of knowledge (not invented).
Read this file if you need to verify correctness of a specific BoK's scope.


ARGUMENTS: marketing-hub — gerar o sistema de agentes operacionais para o módulo Marketing Hub agentic do MCORCH Constellation. CONTEXTO: suíte BoK selada em docs/bok/marketing-hub/ (9 docs, 1732 LOC; mesh seal d5163fed) + scope-lock em .claude/context/marketing-hub-scope-lock-2026-06-02.md. OUTPUT: docs/bok/marketing-hub/bok-agents-system--marketing-hub.md (mesmo padrão dos bok-agents-system--<slug>.md já existentes em meta-api/mercado-livre-api/conteudo-v2/constellation-v2/mcorch-constellation).

REQUISITO SOVEREIGN: ≥8 agentes — gerar os 8 BoK-driven (Business Analysis/BABOK · Enterprise Architecture/EABOK · Data Management/DMBOK · Process/BPM CBOK · Software Engineering/SWEBOK · Cybersecurity/CISSP CBK · Customer Experience/CXBOK · Product Management/ProdBOK) MAIS 3 agentes do delta deste módulo: (9) Agente AEO — Answer Engine Optimization (visibilidade/citação da marca em motores de resposta de IA); (10) Agente de Orquestração de Intenção (intent→tasks, policy engine, HITL, arbitragem); (11) Agente de Demand-gen/Growth (lead lifecycle, nurturing, scoring). Total alvo = 11 agentes.

ESTRUTURA por agente: Purpose · Core Capabilities · Skills · Inputs · Outputs · Decision Scope · Tools & Integrations · KPIs · Use Cases · Collaboration Map. Categorizar cada um como Copilot OU Agente Autônomo. Incluir as 3 camadas cross-agent: Orchestration Model (event-driven baseado em intenção), Intelligent Engineering Layer (7 dimensões: Pessoas/Processos/Tecnologia/Dados/Conhecimento/Valor/Impacto Sustentável), Cross-Cutting Enablers (5).

ANCORAR no MCORCH concreto (não genérico): referenciar os IDs MR-MH/BR-MH/PR-MH/FR-MH e as tabelas/edge functions do SDD (leads, campaigns, sequences, aeo_audits, marketing_consents, marketing_attribution; lead-score, campaign-run, nurture-dispatch, intent-orchestrate, aeo-audit, erase-lead). RECONCILIAR com o Pantheon OpenClaw existente — o agente marketing-growth (L1 Head) NÃO é recriado, é elevado/conectado; referenciar engineer/scientist/artisan/guardian onde colaboram. REUTILIZAR infra (mcorch_nodes/edges malha, ROIWidget/ATTRIBUTES_REVENUE_TO, credenciais per-user, mcorch-qa-healing, deduct_mco_coins). GOVERNANÇA: LGPD/GDPR by design, HITL em alto impacto, XAI/explicabilidade, RLS per-tenant. Idioma: corpo do doc em inglês (headings/labels), pode ter notas executivas pt-BR.

## 🤖 Claude *(00:58:44)*


## 🤖 Claude *(00:58:45)*

Skill carregada. Contexto detectado (B2B2C · MarTech SaaS · scale-up · **AI-native**) → versão context-adapted, não genérica. Componho o sistema de **11 agentes** (8 BoK + 3 delta) ancorado no marketing-hub concreto e escrevo o arquivo.

## 🤖 Claude *(00:58:45)*


🛠️ **Tool Call**: `TaskUpdate`
```json
{
  "taskId": "7",
  "status": "in_progress"
}
```

> **Tool Result (TaskUpdate)** - ✅ Success
>
> ```
> Updated task #7 status
> ```

---

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-02 - agent-af037801ea2099be9]]
> * **Próxima Sessão**: [[2026-06-03 - Fix TradeUX deployment path and Docker setup]]
%% --- TIMELINE END --- %%

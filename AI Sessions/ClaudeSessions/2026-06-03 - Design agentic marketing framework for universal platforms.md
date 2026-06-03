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

---

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-02 - agent-af037801ea2099be9]]
> * **Próxima Sessão**: [[2026-06-03 - Fix TradeUX deployment path and Docker setup]]
%% --- TIMELINE END --- %%

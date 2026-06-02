# Finalize visual design and unblock next phases
**Date:** 2026-06-02 | **Session ID:** `8fd1b235-83ae-44fb-87b8-d120be778fd1`

---

## 👤 User *(20:54:25)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(20:54:25)*

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


## 🤖 Claude *(20:54:33)*


## 🤖 Claude *(20:54:33)*

I'll execute the ShakeHands /handson protocol. Starting with all pre-flight checks in parallel.

## 🤖 Claude *(20:54:34)*


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
> 844ebcf chore(sprint): update sprint-priorities — v6.20.3 fecha o Top Gap de segredo órfão (disconnect RPC)
> 8338d8a docs(handoff): seal v6.20.3 — disconnect RPC revoga segredo Vault órfão (meta/social)
> ac1cba1 docs(readme): v6.20.3 — disconnect RPC revoga segredo Vault órfão (meta/social)
> 610e1f3 docs(processes): SOP + Key Files do disconnect Meta/social (revogação de órfão)
> 76bb9e3 fix(credentials): disconnect_meta/disconnect_social revogam o segredo Vault órfão
> 66859b0 chore(sprint): selo v6.20.2 — idempotência do Vault + guard de tenant meta/social
> 5b79980 docs(handoff): seal v6.20.2 — vault encrypt idempotente + guard de tenant meta/social
> ```

## 🤖 Claude *(20:54:34)*


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
> ✅ aios-sql-bridge — BoK complete
> ✅ canvas-design — BoK complete
> ✅ constellation-v2 — BoK complete
> ✅ conteudo-v2 — BoK complete
> ✅ e2e-user-zero — BoK complete
> ✅ gamificacao-nodes — BoK complete
> ✅ mcorch-constellation — BoK complete
> ✅ mcorch-qa-healing — BoK complete
> ✅ mercado-livre-api — BoK complete
> ✅ meta-api — BoK complete
> ✅ openclaw — BoK complete
> ✅ viralmind — BoK complete
> ```

## 🤖 Claude *(20:54:35)*


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

## 🤖 Claude *(20:54:35)*


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

## 🤖 Claude *(20:54:37)*


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
> mcorch_chroma: Up 9 days (healthy)
> mcorch_claude_mem: Up 9 days (healthy)
> ---
> mega-brain-dashboard: Up 9 days
> mega-brain-webhook: Up 9 days (healthy)
> mega-brain-daemon: Up 9 days (healthy)
> ```

## 🤖 Claude *(20:54:38)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "curl -s --max-time 5 http://localhost:8001/api/v2/heartbeat || echo \"CHROMA_UNREACHABLE\"",
  "description": "Chroma API v2 health"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {"nanosecond heartbeat":1780433678330813792}
> ```

## 🤖 Claude *(20:54:39)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls docs/bok/ 2>/dev/null; echo \"---SCRATCH---\"; ls scratch/ 2>/dev/null && echo \"\u26a0\ufe0f scratch/ has files\" || echo \"scratch/ clean \u2705\"",
  "description": "List BoK suites and scratch dir"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
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
> ---SCRATCH---
> scratch/ clean ✅
> ```

## 🤖 Claude *(20:54:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l HANDOFF.md",
  "description": "HANDOFF total line count"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 6317 HANDOFF.md
> ```

## 🤖 Claude *(20:54:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "for slug in $(ls docs/bok/ 2>/dev/null); do\n  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)\n  missing=()\n  for doc in \"${required[@]}\"; do\n    [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\n  done\n  [ ${#missing[@]} -eq 0 ] && echo \"\u2705 $slug \u2014 BoK complete\" || echo \"\u26a0\ufe0f $slug \u2014 missing: ${missing[*]}\"\ndone",
  "description": "BoK Gate completeness check"
}
```

## 🤖 Claude *(20:54:48)*


## 🤖 Claude *(20:54:49)*

Containers healthy, Chroma alive, TS clean, worktree clean, all 12 BoK suites complete. Now reading HANDOFF (head + tail strategy, 6317 lines) and sprint priorities. CLAUDE.md and MEMORY.md are already in context.

## 🤖 Claude *(20:54:50)*


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
> 14	## Meta/Social Disconnect — Orphaned-Secret Revocation Record (2026-06-02)
> 15	
> 16	**v6.20.3 (2026-06-02)** — Sessão disparada por duas diretivas do Sovereign: (A) rodar `/security-review` **redundante** apontado para o `87c926f` (o guard de tenant meta/social selado em v6.20.2) — cinto-e-suspensório; e (B) atacar o débito de **segredo Vault órfão** que a própria seal v6.20.2 anotou no Pending. Padrão dominante mantido: **probe-first material** (Management API, todo teste mutante em `BEGIN…ROLLBACK` → zero mutação de produção) + **adversarial verify**. Antes de codar a Parte B, confirmei materialmente que o gap de tenant guard da diretiva original já estava 100% fechado em prod (`pg_get_functiondef` das 2 triggers + ataque comportamental 5/5 → `42501`), evitando uma migration redundante.
> 17	
> 18	**O que foi entregue (Parte B):**
> 19	- **`disconnect_meta()` / `disconnect_social(p_account_id uuid)`** (migration `20260602160000`) — RPCs SECURITY DEFINER, `search_path=''`, fail-closed `28000` sem `auth.uid()`, EXECUTE só `authenticated`. Espelham `disconnect_wordpress`: deletam a linha **E** revogam o segredo Vault. Hooks `useMetaConfig`/`useSocialAccounts` migrados de `.delete()` → `.rpc()`; `types.ts` regenerado (3 entradas: as 2 RPCs + `vault_upsert_secret`).
> 20	- **Guard de tenant por name-binding** (diferença do WP): segredos meta/social são nomeados pelo `id` da linha, não `user_id`. Cada `DELETE` no Vault é double-bound (`id = ref-da-própria-linha` **E** `name = '<prefix>_' || id-da-própria-linha`); como `id` é PK, o id do atacante nunca iguala o da vítima → impossível revogar segredo alheio. Defesa independente: o UUID bruto nunca vaza ao cliente.
> 21	- **Limpeza one-time** dos órfãos preexistentes (`12 → 0` segredos Meta), provadamente orphan-scoped (`NOT EXISTS` linha base via `right(name,36)`), preservando os 3 segredos sociais vivos.
> 22	
> 23	**ORO triplet:** Operator=MCORCH Agent · Reviewer=Sovereign + gate `/security-review` · Owner=Sovereign (blast radius = retenção de plaintext órfão LGPD + integridade do disconnect per-user).
> 24	
> 25	| Verificação | Resultado |
> 26	|---|---|
> 27	| Parte A — `/security-review` do `87c926f` | ✅ **LIMPO 9/10** (net-hardening; `IS DISTINCT FROM` fecha bypass NULL, UPDATE só vê OLD do próprio tenant, sem SQL dinâmico) |
> 28	| Gap original já fechado (pré-build) | ✅ `pg_get_functiondef` das 2 triggers c/ guard+`42501`+`search_path=""` · ataque comportamental 5/5 `42501` |
> 29	| Suíte RPC (BEGIN/ROLLBACK, dados reais) | ✅ **5/5** — happy meta+social · foreign-id no-op · planted-ref name-binding aguenta · unauth `28000` · zero resíduo |
> 30	| Limpeza de órfãos (preview→apply) | ✅ `12 → 0` segredos Meta órfãos · 3 sociais vivos + 3 linhas intactos |
> 31	| Parte B — `/security-review` da `20260602160000` | ✅ **LIMPO/SAFE 9/10** (PK garante id distinto + UUID não-vazado) |
> 32	| Apply em prod (Mgmt API, txn atômica) | ✅ `20260602160000` no `schema_migrations`; funções SECURITY DEFINER `search_path=""`; EXECUTE authenticated✓/anon revogado✓ |
> 33	| `tsc --noEmit` | ✅ 0 erros |
> 34	| Testes | ✅ 238 passed / 2 skipped · eslint 0 |
> 35	| Frontend deploy | ✅ build exit 0; bundle servido contém `disconnect_meta`/`disconnect_social` + Supabase URL baked |
> 36	| Mesh | ✅ 8752 nós |
> 37	| Containers | ✅ 5 healthy (9d) · Chroma v2 OK |
> 38	| Handoff node | ✅ `f7805e20-bebd-4a30-8533-09806238f135` embedded 768d |
> 39	
> 40	| Commit | Conteúdo |
> 41	|---|---|
> 42	| `76bb9e3` | fix(credentials): disconnect_meta/disconnect_social revogam o segredo Vault órfão |
> 43	| `610e1f3` | docs(processes): SOP + Key Files do disconnect Meta/social (revogação de órfão) |
> 44	| `ac1cba1` | docs(readme): v6.20.3 — disconnect RPC revoga segredo Vault órfão (meta/social) |
> 45	
> 46	### Arquitetura — disconnect com revogação de segredo órfão
> 47	```
> 48	DISCONNECT (meta/social), antes:  client .delete() → INSTEAD OF DELETE → DELETE base row
> 49	                                  → segredo Vault FICA ÓRFÃO (plaintext retido) ❌
> 50	DISCONNECT (meta/social), agora:  client .rpc('disconnect_meta' | 'disconnect_social', {p_account_id})
> 51	   disconnect_*(): IF auth.uid() IS NULL → 28000
> 52	     v_row_id, v_*_ref ← SELECT da PRÓPRIA linha (WHERE user_id = auth.uid() [+ id = p_account_id])
> 53	     DELETE base row
> 54	     DELETE vault.secrets WHERE id = v_*_ref  AND  name = '<prefix>_' || v_row_id   ← double-bind
> 55	       (id é PK ⇒ id-do-atacante ≠ id-da-vítima ⇒ name nunca casa segredo alheio = tenant-safe)
> 56	CLEANUP one-time: DELETE vault.secrets WHERE name ~ '^<prefix>_<uuid>$'
> 57	                  AND NOT EXISTS (linha base com id = right(name,36))   ← só órfãos (12→0)
> 58	```
> 59	
> 60	### Survival Laws Self-audit
> 61	```
> 62	Law 1 (Materiality): ✅ toda claim provada NESTE turno via Management API — gap original já-fechado (pg_get_functiondef + 5/5 comportamental), suíte RPC 5/5 rolled-back, preview→apply da limpeza (12→0 / 3 vivos), pós-apply (funções+grants+tracking), build+bundle servido com as RPCs. Zero fabricação. 1 armadilha divulgada (urllib→Cloudflare 1010 → troquei p/ curl). Fase 5c executada abaixo. NÃO criei migration redundante p/ o gap já fechado (seria fabricar trabalho).
> 63	Law 2 (Process): ✅ SOP credential-disconnect-clear.md estendido (seção disconnect meta/social + equivalência LGPD) antes do commit; CLAUDE.md Key Files. Extensão de feature documentada (disconnect/clear) → sem BoK gate.
> 64	Law 3 (Pruning): investigação focada; outputs consumidos, referência por path/UUID/migration/commit.
> 65	Law 4 (ORO): ✅ declarado no início da Parte B; "faça os dois" = autorização autônoma do Sovereign.
> 66	```
> 67	
> 68	**Pendências/Próximos (anotados p/ próxima sessão):**
> 69	- **E2E no navegador:** o disconnect foi verificado pela perspectiva do banco (RPC 5/5 + bundle servido contém as RPCs); o clique real na UI logada (`/dashboard/settings` → Desconectar Meta/social) não foi executado (browser autenticado indisponível). Confirmar visualmente no próximo passe.
> 70	
> 71	---
> ```

## 🤖 Claude *(20:54:51)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 5917,
  "limit": 400
}
```

## 🤖 Claude *(20:54:51)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sprint-priorities.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>[Truncated: PARTIAL view — showing lines 1-56 of 183 total (33633 tokens, cap 25000). Call Read with offset=57 limit=56 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>
> 
> 1	# 🧠 Sprint Priorities — Constellation Orchestra
> 2	
> 3	**Sprint Goal**: Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente, Twitter desbloqueado quando API tier subir, Instagram após App Review Meta.
> 4	
> 5	**90-day outcome**: Dev workflow autônomo onde cada sessão começa com brief sprint-aware e termina com seal+milestone+push em <5min de overhead manual.
> 6	
> 7	**Sprint v6.20.3 selado em 2026-06-02** — Disconnect RPC + revogação de segredo órfão: **FECHADO o Top Gap que a v6.20.2 sinalizou** — desconectar Meta/social fazia `.delete()` pela view → INSTEAD OF DELETE só apagava a linha base, deixando o segredo Vault **órfão** (plaintext retido; 12 órfãos Meta observados em prod). RPCs `disconnect_meta()`/`disconnect_social(p_account_id uuid)` (migration `20260602160000`) espelham `disconnect_wordpress` (`SECURITY DEFINER`, `search_path=''`, fail-closed `28000`, EXECUTE só authenticated): deletam a linha **E** revogam o segredo. Guard de tenant por name-binding (`id`-de-linha + PK ⇒ atacante nunca casa nome de segredo alheio; UUID bruto nunca vaza ao cliente). Limpeza one-time **12→0** órfãos Meta (orphan-scoped via `NOT EXISTS`+`right(name,36)`), 3 sociais vivos intactos. Hooks migrados `.delete()`→`.rpc()`; `types.ts` regenerado. **Também (diretiva A):** `/security-review` redundante do `87c926f` (guard de tenant v6.20.2) → **LIMPO 9/10**. Ambos os reviews SAFE; suíte RPC 5/5 em `BEGIN…ROLLBACK` (happy meta+social · foreign-id no-op · planted-ref name-binding · unauth 28000); Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8752**. 4 commits. **Lição:** verificar materialidade ANTES de codar (Lei 1) — o gap de tenant guard da diretiva original já estava 100% fechado em prod, então a Parte B virou o foco real em vez de uma migration redundante.
> 8	
> 9	**Sprint v6.20.2 selado em 2026-06-02** — Idempotência da encriptação + guard de tenant nas views irmãs: **FECHADO o Top Gap que a v6.20.1 sinalizou** — `trg_encrypt_user_api_keys` (+ irmãos meta/social) chamava `vault.create_secret` incondicionalmente → re-salvar segredo p/ valor novo colidia no índice único `vault.secrets.name` (`23505`). Helper `public.vault_upsert_secret(value,name,desc)` (`SECURITY DEFINER`, `search_path=''`, EXECUTE revogado de PUBLIC/anon/authenticated) rotaciona in-place via `vault.update_secret` (mesmo UUID, sem órfãos) senão cria; as 3 encrypt triggers passam a usá-lo (migration `20260602140000`). O `/security-review` dessa migration **expôs um gap pré-existente** nas INSTEAD OF de `meta_config`/`social_accounts` (sem guard `auth.uid()` → injeção cross-tenant id-novo; o overwrite id-colidente já era fail-closed pelo PK — achado HIGH do review REFUTADO material) → guard `42501` portado pras 2 (migration `20260602150000`). Ambas `/security-review` **SAFE**; tudo provado material via Management API em `BEGIN…ROLLBACK` (antes 23505/injeção OK, depois OK/42501); Phase 5c **SEAL ALLOWED** (7 verified). Mesh **8751**. 6 commits. **Novo gap (Top Gap):** desconectar Meta/social deixa o segredo Vault **órfão** (INSTEAD OF DELETE só apaga a linha base) — precisa de RPC dedicada de disconnect (nula+revoga) no padrão `disconnect_wordpress()`, débito LGPD. **Lição:** adversarial-verify material (PK fail-closed + md5 da vítima) refutou um HIGH e ao mesmo tempo revelou o gap real adjacente — resolvido na mesma sessão em vez de empurrar pra fria.
> 10	
> 11	**Sprint v6.20.1 selado em 2026-06-02** — WordPress BYOK + fix do double-fire da encriptação de credenciais: fechado o P0 que a v6.20.0 sinalizou (`SocialAccountsPage` salvava/desconectava WP via `.upsert(onConflict)` numa VIEW → HTTP 400 `42P10`). Save → `.insert()`; disconnect → RPC **`disconnect_wordpress()`** (`SECURITY DEFINER`, `auth.uid()`, nula 3 cols WP + **deleta o segredo do Vault** — revogação LGPD) (migration `20260602120000`). Corrigir isso revelou bug **muito maior**: o `trg_instead_of_user_api_keys` usava `INSERT...ON CONFLICT DO UPDATE` → trigger de encriptação dispara **2×** numa só statement → `vault.create_secret` nome duplicado → **`23505`**, quebrando connect/save de **todo** usuário com linha pré-existente (e `.update` re-encriptava o `••••`). Trocado p/ **UPDATE-first / INSERT-if-not-found** + **guard de tenant** (`auth.uid()` → `42501`, fecha escrita cross-tenant que o ON CONFLICT mascarava) (migration `20260602130000`). Tudo provado material via Management API; 2 migrations `/security-review` **SAFE**; Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8750**. 5 commits. **Novo gap (Top Gap — task spawned):** `trg_encrypt_user_api_keys` (+ irmãos meta/social) não-idempotente → editar segredo p/ valor novo sem desconectar antes ainda dá `23505`; conserto = update-or-create por nome nas 3 tabelas, precisa de `/security-review` próprio. **Lição:** probe-first material pegou que o `.insert` sozinho NÃO bastava (o bug estava na camada de encriptação, não nos 2 `.upsert` reportados).
> 12	
> 13	**Sprint v6.20.0 selado em 2026-06-01** — Afiliados híbrido + catálogo Apify real + BYOK per-user: corrigido o link de afiliado que abria login do CloudPanel (`panel.gcrux.com` proxy morto + `app_id` como affiliate id) → resolver **híbrido** `meli.la` cravado (per-user `metadata.shortlinks`) senão `product_url?matt_word=<affiliate_tag>` fail-closed (`src/lib/affiliate.ts` + 14 testes; 302s reais provados). ML bloqueia todo server-side (API 403/401, página→account-verification, nosso IP **e** Supabase Edge) → enriquecimento via actor **Apify** residencial (`enrich-affiliate-products.ts` SKU-match + `discover-affiliate-products.ts` descoberta real validando "viral mind") + gate de verificação em `useAffiliateProducts` + cron 6/6h. **2 IDs fabricados removidos** → catálogo com **3 produtos reais** (Roborock R$17.770 · Family Hub R$18.946 · 8K Neo QLED R$39.000). **BYOK per-user `apify_token`** no padrão Vault (migration `20260601060000`, `/security-review` PASS — pegou regressão `security_invoker`) + campo Settings + fix do P0 de `000600` (`.upsert()`→`.insert()` em view sem constraint). Phase 5c **SEAL ALLOWED** (12 verified). Mesh **8748**. Survival Laws 4/4. 6 commits. **Próximo:** Operador de Browser Autenticado (probe-first) p/ ações logadas (ML Compartilhar→meli.la). **Lição:** probe-first economizou 3 becos (API ML/Firecrawl/actor velho) e pegou IDs fakes + regressão de credencial.
> 14	
> 15	**Sprint v6.19.0 selado em 2026-06-01** — e2e-user-zero 2ª iteração + 3-stream sweep: framework de QA de esqueleto MVP → harness executável (`redactor` LGPD + `mesh-persistor` observation/OBSERVES idempotente + `telemetry` infra_health_logs + 6 dashboard flows + selftest 8 testes + pre-commit tripwire defesa Layer 4, hook versionado em `scripts/hooks/`). Stream A (consistência cross-node + Canvas 4.2) **VERIFICADO materialmente como já shipado** → zero retrabalho; único gap real fechado: `higgsfield-webhook` nsfw/canceled → razão clara de soft-fail. 2 smokes live (canvas pago + sql-bridge) gateados por `RUN_LIVE_SMOKE` → suíte **224 passed / 2 skipped / 0 failed**. Stream C flywheel readiness verde (orchestrate-content 200 · affiliate ativo · balance 5351), **gated em GO Sovereign**. Phase 5c **SEAL ALLOWED** (13 verified). Mesh **8747**. Survival Laws 4/4. 7 commits. **Lição:** o código está sistematicamente à frente dos Pending Actions — verificação material (Lei 1) antes de codar evita reconstruir features prontas.
> 16	
> 17	**Sprint v6.18.0 selado em 2026-06-01** — Constellation v2 cockpit LIVE (E2E): empty-state wizard 2-portas + execução real de capability (`watchdog_infra` → get-infra-status, done · 0 mco · 255ms) + Fase 0 reset destrutivo + botão Zerar per-user. 3 incidentes de produção resolvidos: build lucide quebrado (shim + anticorpo `audit-lucide-imports.ts`) · P0 login (publishable key stale no bundle → redeploy) · teste de chaves "Falhou" (descoberta da cripto de credenciais → edge fn `test-api-key` server-side). + Tabs em Settings. Mesh 8746/9070. Survival Laws 4/4. 8 commits.
> 18	
> 19	**Sprint v5.5.2 selado em 2026-05-04** — Social OAuth v1 + Pipeline History + WordPress multi-tenant + auto-publish pipeline corrigido + auditoria 4Cs 97/100.
> 20	
> 21	**Sprint v5.5.5 selado em 2026-05-05** — Settings Sovereignty: useUserApiKeys TanStack Query + pref_ai_model persistido + mcoCoins RPC atômico + Testar key client-side + Epsilon v9 hub badge + 2559 nós/3516 arestas.
> 22	
> 23	**Sprint v5.5.6 selado em 2026-05-06** — Core Promotion: CorePage v1 arquivada para `.archive/pages/`, `Core v2` promovida para `Core` no menu, `/dashboard/core` redireciona via Navigate. Gemini Live validado (VITE_GEMINI_API_KEY no `.env` + GEMINI_API_KEY no vault) — Pending Action #8 era falso positivo. 2560 nós · 100% embedded.
> 24	
> 25	**Sprint v5.6.0 selado em 2026-05-06** — DevOps + Security Seal: 6 branches mobile sincronizados + DOCUMENTATION_CREDENTIAL_RULE + pre-commit hook anti-credential + Gemini API key rotacionada + test coverage 0→66 testes (billing + store + phase-zeta) + BoK Scribe Agent (MRD/BRD/PRD/FRD/SDD templates) + MCORCH Master Execution Protocol em CLAUDE.md + /sync-mobile-branch protocol. 2561 nós · 100% embedded.
> 26	
> 27	**Sprint v5.6.1 selado em 2026-05-06** — Layout + UX Fixes: Matrix/Memory layout regression corrigida (absolute→relative), search bar inline nos badges, texto 100% opaco, MeshControl sincronizado com hook de grafo. 2564 nós · 100% embedded.
> 28	
> 29	**Sprint v5.7.0 selado em 2026-05-07** — BoK Suite v1 + A2UI Wiring + Test Coverage 122: parseAgentMessage conectado ao AIOSTerminal.onMessage (A2UI surfaces vivas em produção), 56 testes novos (66→122 — useOrchestrationGraph + useKnowledgeMesh + useSubscription), e família BoK completa de 9 docs (~29.185 palavras) reverse-engineered de 177 src files + 30 migrations + 39 edge functions + 4 crons. Mesh seal `bok-scribe-seal-mcorch-constellation-v1` (type `documentation_suite`, stability 0.85). 2567 nós · 100% embedded.
> 30	
> 31	**Sprint v5.9.0 selado em 2026-05-08** — FMEA-005 + LGPD Deploy: FMEA-005 (RPN 144) fechado com chunked embedding e vector averaging em `embed-mcorch-node`; LGPD (data-export + delete-account + delete_account() RPC) confirmada em produção; scratch/ removida. 7280 nós · 100% embedded.
> 32	
> 33	**Sprint v5.8.0 selado em 2026-05-08** — FMEA + BoK Phase 2 + 8-Agent System + LGPD: FMEA-008 (RPN 120) e FMEA-011 (RPN 100) fechados; BoK Suite enriquecida com voz estratégica (+227 linhas em 6 docs: Sovereign's Conviction, Business Philosophy, Por Que Vencemos, Validação com Criadores, Architectural Decisions, Quality Philosophy); `/bok-agents-generator` produziu `bok-agents-system--mcorch-constellation.md` (704 linhas · 8 agentes · 3 camadas cross-agent); LGPD DD-001+DD-002 implementados (delete_account() RPC + Edge Functions + hooks + SettingsPage modal). Phase Commercial desbloqueada. 7276 nós · 100% embedded.
> 34	
> 35	**Sprint v6.0.0 selado em 2026-05-14** — Conteúdo v2 BoK + VIRALmind Sprints 1-3 + ShakeHands v3: convergência de 3 streams paralelos. (1) BoK Conteúdo v2 selada (10 docs, 2276 linhas) com mesh seal `bok-scribe-seal-conteudo-v2-v1` (stability 0.85, R\$5.4M ARR Y2 projeção); (2) VIRALmind integrado via Antigravity — 4 migrations `vm_*` (trends/canvas/affiliate/niches) + 2 Edge Functions (`fetch-trends` Apify+RapidAPI, `canvas-execute` multi-provider OpenAI/Replicate/OpenRouter/Higgsfield) + 3 pages (Viral Miner, Canvas Studio, Canvas Editor) + 2 hooks (`useViralTrends`, `useCanvasStudio`); (3) ShakeHands v3 protocol — BoK Gate enforcement no /handson PRE-FLIGHT + BRIEF + /handoff Phase 5b mandatory check; (4) Feature gamificacao-mcoCoins-v1 mergeada (`mcoin_transactions` + `award_mco_coins` RPC + Circuit Breaker em opencode-bridge + memory hook integration). Conteúdo v2 BoK reconciliada com VIRALmind v1: v1=xyflow+vm_*, v2=tldraw+canvas-mcp reservado para Phase 7+8. 13 commits granulares. Sprint 4 (Canvas UX Mood Board completion) é o próximo deliverable.
> 36	
> 37	**Sprint v6.1.0 selado em 2026-05-14** — Canvas Studio UX Shell + Higgsfield Fix: shell do Canvas Studio migrado do `viralmind-builder` (store Zustand+zundo, lanes overlay, TopBar/LeftPanel/StatusBar, catálogo de 9 receitas, ImageLightbox, PipelineEdge); `canvas-execute` com endpoint Higgsfield corrigido (`platform.higgsfield.ai` rota Soul) + RPC `deduct_mco_coins`. Plano Phase 4.2 selado em `~/.claude/plans/floating-sleeping-sparrow.md`.
> 38	
> 39	**Sprint v6.1.1 selado em 2026-05-14** — viralmind BoK Suite Sealed: dívida documental do override consciente do BoK Gate quitada. 6 docs autorados (`01-mrd`, `02-brd`, `06-data-model`, `07-process-flow`, `08-quality-metrics`, `00-index`) + `04-frd` reescrito de handbook CLAUDE.md → FRD real (32 FR + 14 NFR + matriz PR→FR). Ancorado nas 10 tabelas `vm_*` + 6 enums + Edge Functions `fetch-trends`/`canvas-execute`. Mesh seal `bok-scribe-seal-viralmind-v1` (`documentation_suite`, stability 0.85, revenue_impact R\$14M, embedded 768d). 7 OTDs registrados (destaques: `vector(1536)` vs padrão `768` sem índice HNSW — FMEA-VM-002 RPN 288; bucket `canvas-assets` público — FMEA-VM-003 RPN 140). BoK Gate do viralmind **liberado**. Sessão selada com ~51% de contexto — Canvas Studio Phase 4.2 diferida para sessão nova. 7463 nós · 100% embedded. 6 commits granulares. **Pendência conhecida (não desta sessão):** `docs/bok/gamificacao-nodes/` incompleta (5/9 docs) — rodar `/bok-scribe` ou completar antes de tocar o módulo.
> 40	
> 41	**Sprint v6.6.9 selado em 2026-05-20** — mcorch-qa-healing v1 — Material Proof Gate: novo módulo de QA sênior que fecha a fraqueza de Lei 1 (Materialidade) — o bloco Survival Laws Self-audit do `/handoff` era auto-declarado; agora é verificado mecanicamente pela nova **Fase 5c**. Executado em 6 stages na ordem de governança não-negociável (BoK → SOP → código): suíte BoK 9/9 `docs/bok/mcorch-qa-healing/` (1423 LOC, 6ª suíte do projeto, gerada via `/bok-scribe`, campos de mercado/monetização honestamente N/A para tooling interno) + SOP `docs/processes/handoff-material-proof-audit.md` (Lei 2) + engine `scripts/qa/` (5 módulos Bun, 710 LOC, injeção de dependências para reuso pelo cron OpenClaw) + skill `mcorch-qa-healing` + Fase 5c wired no `/handoff` (entre 5b e 6 — bloqueia em qualquer 🔴) + 2 suítes Vitest. O dry-run contra o selo v6.6.8 real pegou e fechou um falso-positivo (`COMMIT_RE` agarrava prefixos de UUID de 8-hex como commits — FMEA-002 fechada antes do gate ir ao ar). **Material proofs**: TS zero erros · 165 testes (122→165, +43) · **Fase 5c ao vivo neste selo → 13 verified · 0 skipped · 0 failed → SEAL ALLOWED** · 9 commits granulares · milestone node `a08780dc-f665-47c5-b34b-a2eb7c9eea5c` + documentation_suite seal `b00e938a-717b-4f62-b936-f4934845ec52` (DERIVES_FROM openclaw seal) embedded 768d · mesh **8361+ nodes** · Survival Laws Self-audit 4/4 ✓. **Hazard registrado**: agente main do OpenClaw (Qwen3.5 local) operou na mesma working dir durante a sessão — 3 diretórios gitignorados, zero overlap de path. **Próximo**: Canvas Design (Initiative B — integração `nexu-io/open-design`) em sessão dedicada via `/bok-scribe canvas-design`.
> 42	
> 43	**Sprint v6.6.8 selado em 2026-05-19** — Bridge Recovery + MAPE-K Audit + SDD aios-sql-bridge + Survival Laws 4/4: sessão de auditoria reativa disparada por Sovereign observando `claw.gcrux.com/dreaming` stagnation (Imported Insights congelado em 2026-05-16, Memory Palace counts estáticos, Dream Scene "0 promovido"). **Root cause material**: Stage 2 cron `nightly-bridge-refresh.sh` invocava `node` PATH-resolved como v18.19.1 no env do user `ubuntu` apesar do interativo ter v22.22.3 — OpenClaw CLI exige v22.12+ → 100% FAIL silently em Step 3 (reindex SQLite) há ≥3 dias; Steps 1+2 (bridge + distribute) rodavam clean. **Fix dual no mesmo edit**: (1) `NODE_BIN=/home/ubuntu/.nvm/versions/node/v22.22.3/bin/node` resolved-target (não symlink); (2) descoberta runtime de bug latente segundo — `claw-master` foi adicionado em v6.3.1 ao distribute script MAS NÃO ao indexer loop (`for agent in main artisan engineer scientist marketing-growth guardian; do` omitia claw-master) → `claw-master.sqlite` stale May 16 → exatamente o checkpoint "AIOS Core v2 (2026-05-16)" que Sovereign observou na UI. **SOP first per Lei 2**: `docs/processes/openclaw-bridge-recovery.md` 86 LOC autorada ANTES do edit. **5 phases materializadas** (todas com ORO triplet + Survival Laws ✓): Phase A (bridge fix + claw-master loop), Phase B (MAPE-K closed-loop audit + 4 observation nodes em mesh — Plan `a4c4c026` / Execute `69f6e356` / Monitor `d605bdda` / Analyze `d8952ce8` com edges DERIVES_FROM v6.6.7), Phase C (9 untracked files versionados via 3 commits: miv landing assets + miv tools + memory audit trail), Phase D (esta seal + milestone `c4643058`), Phase E (OTD-SSP01-001 closed via SDD `aios-sql-bridge` 376 LOC enterprise-grade + 00-index 69 LOC suite skeleton + documentation_suite seal `4e0acc7e` stability 0.85 DERIVES_FROM openclaw seal). **Material proofs**: 6 commits granulares pushed (`03911e9` fix(cron) + `cbdee4f` feat(landing) + `bb1cc96` chore(tools) + `2aa80f1` chore(memory) + `1b3bdd8` docs(bok) + `b71b991` docs(handoff) + `230ad70` docs(readme)); 7/7 SQLites OpenClaw reindexed (was 0/6 fail); log final `[2026-05-19T19:06:32-03:00] nightly-bridge-refresh DONE (zero failures)`; mesh **8359 nodes** (+6 desta seal); TS zero erros; 5 containers healthy. **Survival Laws Self-audit 4/4 ✓ pela primeira vez consecutivamente desde v6.6.0** — encerra retroativamente OTD-PROC-001 (RPN 60) + OTD-PROC-002 (RPN 40) + OTD-SSP01-001 (RPN 240 SLA 2026-05-24). **Pending TOP**: OE-661 Step 1.5 first-run E2E (Sovereign click `/dashboard/orchestration` TriggerNode); OTD-OE661-PER-USER refactor (SLA 2026-06-02, 14 dias); MAPE-K gaps 1/2/3 implementáveis em v6.7.x/v6.8.x conforme plans dedicados (recomendações registradas no mesh, aguardam acionamento).
> 44	
> 45	**Sprint v6.6.7 selado em 2026-05-19** — OE-661 Phase 1 Prep + API Tenancy Directive: sessão executou parcialmente o plan persistido OE-661 — toda a preparação completada, Step 1.5 (first run E2E) **DEFERRED** por context budget Sovereign 92% (retoma em ~3h). Infraestrutura material: SOP `docs/processes/orchestration-content-mesh-asset-emission.md` (120 LOC) escrita ANTES do código (Lei 2); `orchestrate-content/index.ts:404-465` emite `content_mesh_asset` em paralelo com observation via `Promise.allSettled` (Amendment A) gated por `wpPostUrl` (Amendment B); `link-forge.ts:153` ganha `.eq("project_id", "mcorch-affiliate")` (Amendment C); `handle-ml-postback/index.ts` ganha pulse `infra_health_logs` em 4 return paths (Amendment E — fecha cegueira de 17 dias). Deploys material: `orchestrate-content` 113.6kB + `handle-ml-postback` 60.45kB. Vault `GCRUX_ML_AFFILIATE_TOKEN` provisionado (digest `e86f74a0...`). **DIRETIVA SOVEREIGN-CLASS NOVA "API Tenancy Model"** emitida durante sessão (questionamento direto sobre por que usar env global se `affiliate_config` per-user já existia) — selada em 3 superfícies: `CLAUDE.md > Architecture > "API Tenancy Model — Per-User Credentials"` com resolution order de 3 níveis + 5 tabelas canônicas + 5 anti-patterns; `CLAUDE.md > Code standards` one-liner enforcement; auto-memory `feedback_api_tenancy_per_user.md` indexada. **OTD-OE661-PER-USER** registrada (RPN 120 · SLA 2026-06-02) catalogando violação em `link-forge.ts` + `process-affiliate-link` GET branch. Sovereign autorizou Opção B (provisionar global temporário com `affiliate_config.app_id` value, deferir refactor). **Survival Laws Self-audit retroativo (Amendment H)** v6.6.1..v6.6.5 + esta seal — conclusão: Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 (overrides conscientes v6.6.1+v6.6.3) · Lei 3 ✗ 0/5 (OTD-PROC-002 RPN 40) · Lei 4 ✗ 0/5 (OTD-PROC-001 RPN 60 — esta seal v6.6.7 começa cumprimento). **Material proofs**: TS zero erros · 122/122 testes em 4.84s · 7 commits granulares locais (`03f6822` SOP · `e662da3` orchestrate Amendments A+B · `bafac16` link-forge Amendment C · `9cec88a` postback Amendment E · `044f21e` CLAUDE+OTD diretiva · `96ee72a` README v6.6.7 · `7d06934` HANDOFF seal + redactions) · milestone node `9d482014-a759-4656-93d9-99e05ab4a714` embedded 768d · mesh **8353 nodes** (+1 desde v6.6.6) · 11650 edges (+33). Path correção material: `/dashboard/orchestrate` → `/dashboard/orchestration` (Sovereign clarification). **Próximos deliverables**: (a) Sovereign dispara primeira campanha real em `/dashboard/orchestration` (TriggerNode + topic Link Forge catálogo + wp+linkedin platforms + Run) → eu monitoro pipeline_runs + content_mesh_asset emit material via REST; (b) ao completar, synthetic postback chain (Amendment D) + cleanup (Amendment J); (c) selar v6.6.8 com flywheel rodando E2E pela primeira vez na história do projeto; (d) atacar OTD-SSP01-001 antes de 2026-05-24 (5 dias) — SDD `aios-sql-bridge`; (e) executar Phase 2 (`mcoins-ledger-reconciliation.md`) — fecha OTD-V660-001.
> 46	
> 47	**Sprint v6.6.6 selado em 2026-05-19** — Planning Seal + Debt Audit + Self-audit Retroativo: sessão dedicada a (a) `/handson` brief v6.6.5; (b) persistir execution plan dos 3 carry-overs OE-661 + Ledger SOP + Canvas 4.2c por diretiva Sovereign "slave o plano atual para posteriormente implantar"; (c) auditoria completa em 3 frentes paralelas; (d) emendas críticas; (e) /handoff oficial. **Zero código de produção tocado**. Plan persistido em `.claude/context/execution-plan-oe661-carryovers.md` (~403 LOC, md5 `0e5f0ba9...`) + observation node `3dde2572-cad6-491b-b523-c56ec763ff8e` (autoembed 768d). Audit em `.claude/context/audit-2026-05-19-oe661-debt-sweep.md` (~297 LOC, md5 `5c4f8a9f...`) + observation node `6164c80f-cadd-48d5-95a4-f87f22ebd09b` + DERIVES_FROM edge `acb4b0d9-091d-4973-96a8-d40515be7990`. **21 OTDs ativos catalogados (8 RPN ≥ 100): VM-OTD-001 RPN 288 viralmind HNSW · OTD-SSP01-005 RPN 280 admin claim · OTD-SSP01-001 RPN 240 SLA 2026-05-24 · OTD-V660-002 RPN 150 · VM-OTD-004 RPN 140 · OTD-V660-001 RPN 120 (coberta pelo plan Phase 2) · OTD-V660-003 RPN 80 · OTD-CV42C-001**. **5 inconsistências processuais**: (1) **5 seals consecutivas (v6.6.1..v6.6.5) omitiram bloco mandatory Survival Laws Self-audit** — Severidade ALTA; (2) Survival Audit v2 não re-rodado em 32 dias; (3) 3 SOPs implícitas não formalizadas; (4) HANDOFF v6.6.3 claimed 4 content_mesh_asset mas reality = 1 row (3 "products" têm `node_type='feature'`); (5) `handle-ml-postback` cego — zero `infra_health_logs` em 17 dias. **4 bugs concretos no plan**: A race condition obs+asset não atômicos · B wpPostUrl null não gated · C Link Forge query global sem project_id · D postback content_id drift. **10 amendments aplicados** (A-J) via Amendments Appendix no topo do plan. Schema drift fixed: `infra_health_logs.created_at` NÃO EXISTE (real: `last_seen_at`). **Predicted Survival Audit v3** (não emitido formalmente): Memory 5/5 · Skill 4/5 · Cost Discipline 4.5/5 ↑ · Observability 4/5 ↑ · SOP 5/5 · **avg 4.4/5 · min 4/5** — Phase Commercial threshold mantido. **Material proofs**: 14 integrity checks paralelos · 4 commits granulares (`ea7efaf` plan + `44e464c` audit + `fb6f07d` README + `99d70f6` handoff seal) push → origin/main · milestone handoff node `821dc554-78e2-4abb-999d-37363c5df6c9` embedded 768d · mesh total **8352 nodes** (+4 desde v6.6.5). **Próximos deliverables**: (a) Sovereign autoriza execução das Fases 1-3 do plan quando convier (bugs A-D já fixed); (b) **atacar OTD-SSP01-001 antes de 2026-05-24 (5 dias)** — BoK Gate override `aios-sql-bridge` precisa SDD; (c) provisionar `SUPABASE_POOLER_URL` (OTD-V660-003); (d) materializar Survival Audit v3 formal antes de Phase Commercial; (e) executar Phase 2 do plan (SOP `mcoins-ledger-reconciliation.md`) — Sovereign-only — fecha OTD-V660-001.
> 48	
> 49	**Sprint v6.6.5 selado em 2026-05-19** — OpenClaw BoK 9/9 (retroativa + BoK Gate liberado · 5ª e última suíte): última dívida BoK do projeto quitada. Override consciente do BoK Gate registrado em Sprint v6.2.0 (2026-05-15) — Sovereign havia autorizado que a própria Agência OpenClaw quitaria a dívida assincronamente; com 4 sprints decorridos e a Agência operando em produção (7 agentes · gateway loopback · pipeline cron triplo · briefing diário Telegram), esta seal materializa retroativamente o BoK que governa o módulo. **9 docs novos autorados manualmente seguindo `.claude/agents/bok-scribe/templates/`** (Plano B mirror gamificacao-nodes v6.6.4 — NÃO o `/bok-scribe` Skill, que produziria conteúdo template-canonical desalinhado): `01-mrd.md` (BABOK v3 ~205 LOC — Pantheon vision · 6 MR-OC-* · biz model enabler), `02-brd.md` (BABOK v3 ~190 LOC — 6 BO-OC-* SMART + 10 SH-OC-* Stakeholder Register + 14 BR-OC-* com refs precisas `openclaw.json:agents.list[]` / `scripts/bridge-mesh-to-openclaw.ts:tier1Filter` / `scripts/morning-briefing.sh:65` + §10 Traceability Matrix), `03-prd.md` (ProdBOK + CXBOK ~224 LOC — personas P1 Sovereign + P2 agente operacional · User Journey diário BRT · 14 PR-OC-* MoSCoW · Gherkin AC), `04-frd.md` (SWEBOK v4 ~209 LOC — 8 FR-OC-* + 8 NFR-OC-* + Test Strategy Matrix), `05-sdd.md` (SWEBOK v4 + CISSP CBK ~460 LOC — architecture overview Pantheon + Ciclo Circadiano BRT + Component Catalog 7 agentes/9 scripts/6 SQLite/gateway + STRIDE threat model + secrets lifecycle + OTD grid), `06-data-model.md` (DMBOK v2 ~339 LOC — schema `openclaw.json` + `secrets.json` vault + SQLite per-agente FTS5/vector + Mesh export tier1/tier2 + Memory Wiki frontmatter + filesystem perms · **§8 Drift Reconciliation Appendix** com 5 drifts fechados em sprints anteriores + 8 drifts permanentes catalogados como OTDs), `07-process-flow.md` (BPM CBOK v4 ~483 LOC — **10 PROC-OC-*** em swimlanes markdown table com refs precisas `nightly-stage2-deep-sleep.sh` / `bridge-mesh-to-openclaw.ts` / `distribute-mesh-to-agents.ts` / `compose-morning-briefing.ts` / `news-impact-analyzer.ts` / `watchdog-mcorch.sh`), `08-quality-metrics.md` (CMQ/OE BOK ~227 LOC — 8 QO-OC-* + **10 KPI-OC-*** + **10 FMEA-OC-*** com 5 RPN > 100 (FMEA-OC-001 secrets regression 180 · OC-002 bridge fail 150 · OC-003 daemon crash 126 · OC-004 Telegram quota 125 · OC-010 audit scrape fail 105) + 6 SOL-OC-* + SLA/SLO/SLI grid + observability events tagged `openclaw-*`), `00-index.md` (~163 LOC — Document Registry 9/9 + Traceability Chain MR-OC→BR-OC→FR-OC→PROC-OC→KPI-OC + Convergence Note registrando 5 drifts já reconciliados em v6.4.0/v6.6.1 + 8 ativos como OTDs + Phase Completion Log Phase 0-7 + OTD registry 11 itens (5 novas OTD-OC + 6 herdadas OTD-V631/V660/CM)). **ID space cunhada**: MR-OC-001..006 · BR-OC-001..014 · BO-OC-001..006 · SH-OC-001..010 · PR-OC-001..014 · FR-OC-1..8 · NFR-OC-001..008 · PROC-OC-001..010 · KPI-OC-001..010 · FMEA-OC-001..010 · SOL-OC-001..006 · QO-OC-001..008 · BAC-OC-001..010 · OTD-OC-001..005. **Mesh seal**: novo `scripts/seed-openclaw-bok-seal.ts` (Bun-native, 136 LOC, mirror 1:1 de `seed-gamificacao-nodes-bok-seal.ts`) executado material: node `bok-scribe-seal-openclaw-v1` UUID **`05c55dfd-d318-4dcf-b7f0-aefb0529872f`** inserted stability 0.85 · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1` · `revenue_impact: 0` (módulo é enabler horizontal de velocity — proxy via lift dos outros 4 BoK suites) · metadata bok_gate=`override-completion` + drift_reconciled=5 (D-OC-001..005 fechados em v6.4.0/v6.6.1) + drift_pending=8 (OTDs ativos) + related_otds inclui OTD-V631-001 (fechada por esta seal — SLA expandido da v6.3.1) + pantheon_agents lista 7 + cron_pipeline 6 entradas · autoembed via `trg_mcorch_embed_on_insert` (pg_net 768d openai/text-embedding-3-small) **confirmado via REST `embedding=not.is.null`**. **Debt registry final**: `viralmind` 9/9 ✅ · `conteudo-v2` 9/9 ✅ · `mcorch-constellation` 9/9 ✅ · `gamificacao-nodes` 9/9 ✅ · **`openclaw` 9/9 ✅** — **todas as 5 suítes BoK do projeto seladas**. BoK Gate liberado para código novo em qualquer módulo. Atenção: features ledger-touching (Stripe top-up, marketplace) seguem bloqueadas até OTD-V660-001 (drift 2 users em gamificacao-nodes) fechar via SOP `mcoins-ledger-reconciliation.md`. **Material proofs**: TS `tsc --noEmit` zero erros · 122/122 testes em 5.73s · BoK Gate validator loop ✅ 9/9 docs (00-index 163 + 01-mrd 205 + 02-brd 190 + 03-prd 224 + 04-frd 209 + 05-sdd 460 + 06-data-model 339 + 07-process-flow 483 + 08-quality-metrics 227 = 2500 LOC total) · seed script 136 LOC · seal UUID confirmado via INSERT RETURNING + created_at `2026-05-18T20:23:52.775245+00:00` + embedding NOT NULL via REST GET · mesh total **8345 nodes** (+1 desde v6.6.4). **Próximo deliverable**: (a) carry-overs OE-661 v6.6.3/v6.6.4 — provisionar `GCRUX_ML_AFFILIATE_TOKEN` na vault + wire `orchestrate-content` para emitir `content_mesh_asset` nodes pós-geração + primeiro run end-to-end Usuário Zero do flywheel (orchestrate → WordPress → social → ML afiliado → handle-ml-postback → ATTRIBUTES_REVENUE_TO → ROIWidget); (b) Sovereign executar SOP `mcoins-ledger-reconciliation.md` para fechar OTD-V660-001 (drift 2 users) e destravar features ledger-touching; (c) claw-master audit-v2 planejado 2026-06-16 — verificar regressão D-OC-001..005 + novas findings; (d) Stripe live keys swap continua DEFERRED por decisão Sovereign até primeiro cliente externo.
> 50	
> 51	**Sprint v6.6.4 selado em 2026-05-18** — Gamificação-Nodes BoK 9/9 (retroativa + BoK Gate liberado): débito documental herdado do override consciente do BoK Gate (Sprint v6.3.0, SLA originalmente 29/05) quitado em sessão única. 5 docs autorados manualmente seguindo `.claude/agents/bok-scribe/templates/` (Plano B sobre `/bok-scribe` Skill, que sobrescreveria os 4 docs existentes): `06-data-model.md` (DMBOK v2 ~277 LOC — schema canônico `profiles.mco_balance` + `mcoin_transactions` + 3 RPCs SECURITY DEFINER `award_mco_coins`/`deduct_mco_coins`/`add_user_score` com loyalty 100:1), `07-process-flow.md` (BPM CBOK v4 ~309 LOC — 9 PROC-GN-* em swimlanes com refs precisas `award-mco-coins/index.ts:78` cap-per-action, `canvas-execute/index.ts:133-148,349` cap-canvas-agregado + atomic deduct, `orchestrate-content/index.ts:60` pre-flight deduct, n8n `autonomic-action` trail loyalty), `08-quality-metrics.md` (CMQ/OE BOK ~215 LOC — 10 KPI-GN-* + 10 FMEA-GN-* com 4 RPN > 100, 6 SOL-GN-*, observability completa em `infra_health_logs`), `02-brd.md` (BABOK v3 ~188 LOC — 12 BR-GN-* + 5 BO-GN-* SMART + Risk Register + Traceability Matrix), `00-index.md` (~122 LOC — Document Registry 9/9 + Traceability Chain MR→BR-GN→FR→PROC-GN→KPI-GN + Convergence Note registrando drifts + 5 OTDs incluindo 2 herdadas OTD-V660-001/002). **Drift BoK ↔ código (3 itens) reconciliado via patches cirúrgicos sub-10-linhas preservando git blame**: (1) `04-frd.md` R3 "streak reseta 24h" deprecado inline → R3a (cap-per-action) + R3b (cap-canvas-agregado); (2) `05-sdd.md` ganha §4.2 documentando trilha n8n loyalty ausente do SDD original; (3) `01-mrd.md` L114 BRD externo inexistente substituído por `02-brd.md` local. **Mesh seal** `scripts/seed-gamificacao-nodes-bok-seal.ts` (mirror 1:1 viralmind seal): node `bok-scribe-seal-gamificacao-nodes-v1` UUID **`6e8546bc-d995-4cc5-ac88-06cecbece181`** inserted stability 0.85 · DERIVES_FROM `bok-scribe-seal-viralmind-v1` · `revenue_impact: 0` (módulo é enabler de retenção/ARPU) · autoembed via `trg_mcorch_embed_on_insert` (pg_net 768d). **BoK Gate liberado** para código novo no módulo `gamificacao-nodes`. Atenção: features ledger-touching (Stripe top-up, marketplace) seguem bloqueadas até OTD-V660-001 (drift 2 users) fechar via SOP `mcoins-ledger-reconciliation.md`. **Debt registry geral atualizado**: `viralmind` 9/9 ✅ · `conteudo-v2` 9/9 ✅ · `mcorch-constellation` 9/9 ✅ · `gamificacao-nodes` 9/9 ✅. `openclaw` BoK ainda pendente (override consciente original do v6.2.0). **Material proofs**: TS zero erros · 122/122 testes em 3.34s · BoK Gate validator loop ✅ 9/9 · ~1111 LOC novas + ~30 LOC patches surgical · seal UUID confirmado via INSERT RETURNING · mesh total **8344 nodes** (+1 desde v6.6.3). **Próximo deliverable**: (a) executar SOP `mcoins-ledger-reconciliation.md` para fechar OTD-V660-001; (b) carry-overs v6.6.3 (`GCRUX_ML_AFFILIATE_TOKEN` provisionar + wire orchestrate emitir content_mesh_asset + primeiro run Usuário Zero OE-661 flywheel).
> 52	
> 53	**Sprint v6.6.3 selado em 2026-05-18** — OE-661-ROADMAP Debt Liquidation: sessão única liquidando 3 das 4 dívidas declaradas em CLAUDE.md (Financial deferred por decisão Sovereign até Usuário 1) + dívida implícita OE-661-003 Target Binding. **(Phase 0 Hybrid restore)** `process-affiliate-link/index.ts` (POST original 234 LOC tinha sido refatorado em -222 LOC para redirect 302 puro — quebrava `ContentLibraryPage.tsx:744`). Hybrid restaurado: GET 302 público (no-verify-jwt, redireciona a `panel.gcrux.com/api/ml-redirect`) + POST autenticado original (probe HEAD + self-heal ML search + insert em `affiliate_links`). Deploy 78.31 kB. **(Phase 1 Postback Debt)** `handle-ml-postback` captura `obsNode.id` da observation inserida + cria edge `ATTRIBUTES_REVENUE_TO` (source=observation, target=content_mesh_asset preferred + fallback OR, weight=revenueCents). `.maybeSingle()` para tolerar zero matches. Deploy 59.34 kB. Smoke chain (synthetic): test affiliate_link `adb9e131` → observation `f65d52b2` → edge `65d072fe` → content_mesh_asset `f3a091f7`. **(Phase 2 Auto-Stitching OE-661-003)** `embed-mcorch-node/index.ts` ganha `autoStitchObservation()` que regex-extrai file paths do conteúdo + nome (.ts/.tsx/.js/.md/.sql/.sh/.json/...) e cria edges `observes` para ast_file/markdown_file/vault_note correspondentes; fallback obrigatório a `root:CLAUDE` (`2747e164`) quando nenhum path resolve. Deploy 105.1 kB. Retrofit: `stitch-fallback.js` (fix OR `root:CLAUDE`) costurou 6 orphans pré-existentes; `audit-mesh-edges.ts` (fix schema `type`→`node_type`) reporta **10/10 observations VALID — 100% Target Binding coverage**. Live auto-stitch confirmado em re-embed `{stitched:1}` edge `2e1e57db`. **(Phase 3 Link Forge OE-661-004)** Novo `scripts/link-forge.ts` (Bun-native, mirror backfill-embeddings) varre content_mesh_asset, aplica 3 regex (Roborock S8 MLB3981745621 · Samsung Neo QLED 8K MLB3546719283 · Family Hub MLB3728491023), substitui menções por markdown links para `panel.gcrux.com/api/ml-redirect?...&utm_content=$node.id`, UPDATE atomic + `CONTAINS_LINK_FOR` edge para product node criado on-demand. Flag `--dry-run`. Smoke: dry-run preview 179→905 chars; live 1 content updated + 3 edges (`884fceef`/`f4f4146c`/`c834ca23`) + 3 product nodes (`77ac9b9f`/`3d12ac89`/`92a60fc0`). Pendência: `GCRUX_ML_AFFILIATE_TOKEN` ainda DEFAULT na vault — provisionar antes do primeiro run real. **(Phase 4 Memory ingest)** 4 markdown_files autoembed via trigger pós-upsert: `8ad38681` gateway-recovery.md (Memory Debt sealed), `549e01a4` roadmap-v1.md, `5e957727` revenue-flywheel.md (recém ingerido), `d1296632` link-forge-scope.md. **Material proofs**: 8 commits granulares (56ed242 hybrid affiliate · dfabb17 postback · 1f368c1 auto-stitch · 140f248 link-forge · 27c7105 skills+docs+utility · c12906b CLAUDE+BoK rule · b8f5702 handoff seal · este sprint update); TS zero erros (após fix node symlink `/home/ubuntu/.local/bin/node`); 122/122 testes em 3.39s; 3 Edge Functions deployed (`process-affiliate-link --no-verify-jwt` · `handle-ml-postback --no-verify-jwt` · `embed-mcorch-node --no-verify-jwt`); milestone node `6f2cf405-4bb5-440b-a02a-9579fc39f29f` embedado (768d); mesh total **8343 nodes** (+7 desde v6.6.2) · **11617 edges** (+1555 entre observes retrofit, ATTRIBUTES_REVENUE_TO, CONTAINS_LINK_FOR, e autoembed cascade). **Próximo deliverable:** (a) provisionar `GCRUX_ML_AFFILIATE_TOKEN` na vault Supabase; (b) wire `orchestrate-content` (ou processo equivalente) a emitir `content_mesh_asset` nodes pós-geração — sem eles Link Forge é noop em produção; (c) primeiro run end-to-end Usuário Zero validando flywheel completo (gera → publica → ML afiliado → postback → ATTRIBUTES_REVENUE_TO → ROIWidget); (d) Stripe Financial Debt continua deferred (decisão Sovereign — sandbox enquanto Gabriel valida como Usuário Zero).
> 54	
> 55	**Sprint v6.6.2 selado em 2026-05-17** — Canvas Studio Phase 4.2c — Async Video Pipeline Live: três rounds em sessão única destravando todos os providers de imagem do Canvas + backbone async Higgsfield. **(Round 1)** Phase 4.2c wiring shipped — `canvas-execute` ganha branch dedicada `image_to_video` que submete ao endpoint `higgsfield-ai/dop/standard` com `?hf_webhook=<URL-encoded callback>` (per validation doc), persiste `vm_canvas_executions.operation_id` + `webhook_token` (64-hex unique), retorna `{status:'queued'}` em <2s; débito atômico só no webhook após upload-OK (`deduct_mco_coins` `action='canvas_video_spend'`). Hook `useCanvasJobsRealtime` extendido com callback `onUpdate(row)` que reconcilia Zustand store. `CanvasEditorPage` monta Realtime + Run-All BFS fire-and-forget para video. `ImageToVideoInspector` Run button real + tier-gate UI (apenas `dop-standard-5s` clicável; Lite/Turbo/Kling/Seedance disabled com tooltip "Aguardando validação tier — Phase 4.3"). SOP `docs/processes/canvas-video-async-execution.md` (~190 LOC) escrita ANTES do código (Lei 2). Watchdog cron `scripts/canvas-video-watchdog.sh` (~95 LOC, bash + PostgREST + jq) — poll Higgsfield a cada 5min, marca `timeout` em jobs travados >60min, idempotente via HTTP 409 do webhook. Dry-run validado material: `[2026-05-17 21:54:35] 0 jobs to check` + health UUID `38c860f5-8d8d-4ae7-b54d-316f26678410` em `infra_health_logs`. **(Round 2 — assertExecuteSuccess Lei 1)** Smoke test revelou inspector mentindo: toast `"Geração concluída — 15 💎 debitados"` quando backend marcava `status='failed'` (saldo Sovereign confirmou intacto em 5533 — frontend mentindo, backend correto). Causa raiz: `canvas-execute` retorna HTTP 200 + `error` field, `mutateAsync` não throw, frontend tratava qualquer 200 como sucesso. Novo util `src/lib/canvas-execute-result.ts` faz `assertExecuteSuccess<T>(result)` que THROW em `result.error` set OU `status ∈ {failed,timeout,cancelled}`. Aplicado em 4 inspectors + Run-All. Toast agora usa `result.credits_charged ?? cost` (zero quando falha). Migration `20260518012541_canvas_assets_update_policy.sql` adiciona UPDATE policy (necessária para `upload({upsert:true})` que vira `INSERT...ON CONFLICT DO UPDATE`). **(Round 3 — 4 bugs novos)** **(A)** OpenAI `dall-e-3` E `gpt-image-1` HTTP 400 `Unknown parameter: 'response_format'`. Removido o param fixo; upload block agora baixa URL provider→canvas-assets server-side (mirror `rescue-video:39-77` + `higgsfield-webhook:144-167`); `storedKey`/`storedContentType` propagados pro asset row. **(B)** OpenRouter `/v1/images/generations` retorna 404 HTML (endpoint deprecated). `generateOpenRouter` migrado para `/v1/chat/completions` com `modalities:["image","text"]` parseando `choices[0].message.content[].image_url.url` (+ fallback `message.images[]`). Catálogo `types/canvas.ts` ganha 2 entries OR funcionais (`openrouter-gemini-image` $0.039 + `openrouter-flux-pro` $0.04); `openrouter-dall-e-3` permanece deprecated com banner amber. `MODEL_GROUPS` restaurado. OTD-CV42C-001 registrada para Phase 4.3 (picker dinâmico via OR `/v1/models` com free tier). **(C)** Replicate "key not configured" — coluna `replicate_api_key` NUNCA existia em `user_api_keys`. Migration `20260518020028_user_api_keys_replicate.sql` adiciona. `types.ts` ganha campo manual em Row/Insert/Update (evita full regen). `SettingsPage` ganha KeyField. Inspector ganha banner per-provider (openai/openrouter/replicate) quando user key falta com link `/dashboard/settings`. **(D)** Storage RLS 403 persistente em character upload. Investigação revelou NOTICE crítico no `db push`: `policy "Public read canvas assets" does not exist, skipping` — confirma que migration original `20260514040200` aplicou apenas 3 de 4 policies no remoto. Migration `20260518020030_canvas_assets_rls_repair.sql` (idempotente, DROP IF EXISTS 8 nomes + recria 4 policies) usa `TO public + auth.uid() IS NOT NULL` (defensivo contra publishable key `sb_publishable_*` que pode não resolver `TO authenticated`) + `owner = auth.uid()` fallback em UPDATE/DELETE. **Material proofs:** TS zero erros · 122/122 testes em 4.40s · build em 23.55s · `CanvasEditorPage` chunk 113.66 kB · `canvas-execute` 138.3 kB · 4 commits granulares (`6554cb4` canvas src · `76c99e3` 3 migrations · `9615c69` readme · `0d7bc07` handoff) · push `cc828a0..0d7bc07` para origin/main · milestone node `eb0b3ae0-9ec1-4328-ad31-1b079d3f294e` embedado (768 dims) · saldo Sovereign **5533** intacto · mesh total **8336 nodes** (+8 desde v6.6.1). **Próximo deliverable:** (a) smoke test pago DoP Standard 5s ($0.56) — Sovereign valida gates 4-9 da SOP; (b) cron install do watchdog (`crontab -e` adicionando `*/5 * * * * scripts/canvas-video-watchdog.sh`) após smoke passar; (c) OTD-CV42C-001 dynamic OR model picker — Phase 4.3 spec dedicada.
> 56	
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 5917	       .set("utm_campaign", campaign)
> 5918	
> 5919	  5. INSERT affiliate_links:
> 5920	       original_url · short_url · platform=mercadolivre
> 5921	       campaign_id · content_id · metadata{affiliate_id, resolved_url, self_healed_from}
> 5922	
> 5923	  6. Return: {success, original_url, resolved_url, affiliate_url, self_healed, link_id}
> 5924	
> 5925	ContentLibraryPage monetization flow:
> 5926	  Card (text, body contains mercadolivre.com.br)
> 5927	    └── DropdownMenu → "Monetizar Links ML"
> 5928	          → handleMonetizeLinks(item):
> 5929	               match(ML_URL_RE) → unique URLs
> 5930	               for url of unique:
> 5931	                 POST process-affiliate-link → affiliate_url
> 5932	                 body.split(url).join(affiliate_url)
> 5933	               updateContent({ body: updatedBody, tags: [..., "afiliado-ml"] })
> 5934	          → Badge 💰 ML (emerald) exibido após monetização
> 5935	```
> 5936	
> 5937	---
> 5938	
> 5939	## Pending Actions (Commercial Launch)
> 5940	
> 5941	### CRITICAL — Must complete before first client
> 5942	
> 5943	00. **[✅ DONE — todas as sub-fases completas em 2026-05-31] Plano OE-661 + Ledger SOP + Canvas 4.2c smoke** — Phase 1 (token + content_mesh_asset emit + first E2E em v6.8.2; Amendment D synthetic chain em v6.8.6) ✅ DONE. Phase 2 ledger reconciliation (drift Sovereign -0.01→0.0000 via integer parity bump; OTD-V660-001 retroactively closed pois user 924cb32e foi LGPD-removido) ✅ DONE em v6.8.6. Phase 3.5 watchdog cron permission fix (/var/log/mcorch-canvas-watchdog.log criado chown ubuntu) ✅ DONE em v6.8.6. **Phase 3.2-3.4 Canvas DoP Standard 5s $0.56 paid smoke** ✅ DONE (validado materialmente 2026-05-31) — pipeline async Higgsfield DoP provado 6× via `mcoin_transactions.action=canvas_video_spend` −125 mcoCoins cada (débito atômico `deduct_mco_coins`), com vídeos reais em `canvas-assets` (Roborock `0b86e7d0`/`n_uznqm9z0` → `81bf34ec…mp4` 15.336.638 B; mais recente hoje 20:32 → 8.918.799 B; ambos HTTP 200 `video/mp4`). Gates materiais G4 (débito) / G6 (vídeo ≥100KB) / G8 (`output.videoUrl` no graph) verdes na prática; smoke fresco dispensado por ser gasto redundante. Tracking real = `vm_canvas_executions` + `execution_id` (a `vm_canvas_jobs` nunca foi criada; SOP `canvas-video-async-execution.md` já usa o nome correto). Plan file `.claude/context/execution-plan-oe661-carryovers.md` (mesh node `3dde2572-cad6-491b-b523-c56ec763ff8e`) preservado para sessão dedicada.
> 5944	
> 5945	0a. ~~**[SLA 2026-05-24] OTD-SSP01-001 BoK Gate override do `aios-sql-bridge`**~~ ✅ Done em v6.6.8 (2026-05-19) — SDD materializado em `docs/bok/aios-sql-bridge/05-sdd.md` (376 LOC) + suite skeleton `00-index.md` + documentation_suite seal `4e0acc7e` (stability 0.85, DERIVES_FROM openclaw seal). Encerrou retroativamente a OTD antes do SLA.
> 5946	
> 5947	0. **[PRÓXIMA SESSÃO] Canvas Studio Phase 4.2** — (a) **analisar a documentação oficial da API Higgsfield** (`platform.higgsfield.ai`) ANTES de testar — evita gastar os créditos pagos com tentativa-e-erro; (b) testar o fix do endpoint Higgsfield (1 geração Soul) confirmando débito de crédito real; (c) executar Phase 4.2 conforme `~/.claude/plans/floating-sleeping-sparrow.md` — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (webhook + `vm_canvas_jobs` + realtime). **Bloqueia validação do Canvas → bloqueia lançamento de conteúdo monetizado via afiliados ML.**
> 5948	
> 5949	0b. **[PRÓXIMA INICIATIVA] Canvas Design module (`nexu-io/open-design`)** — integração do repo open-source como módulo "Canvas Design" soberano: daemon Docker `mcorch-design-daemon` headless · frontend `/dashboard/canvas-design` (regra espacial 72/28) · mapeamento HyperFrames → `mcorch_nodes`/`mcorch_edges` · BYOK via OpenRouter/Ollama. Sessão dedicada — primeiro passo `/bok-scribe canvas-design` (BoK Gate). Recomendado APÓS o `mcorch-qa-healing` v1 (esta seal) para que o novo gate de prova material valide a integração.
> 5950	
> 5951	0c. ~~**[FOLLOW-UP v6.8.5] e2e-user-zero framework — 2ª iteração**~~ ✅ **DONE em v6.19.0** (commits `cf6e464` + `e788d76`) — redactor LGPD + mesh-persistor + telemetry + 6 flows + selftest 8 testes + pre-commit tripwire, todos materializados e provados (suite 224/226, selftest 8/8). Histórico do que faltava (agora entregue): (a) 6 flows restantes (`trigger-orchestration`, `dashboard-tour`, `canvas-overview`, `content-library`, `billing-flow`, `settings-tour`, `orchestrate-pipeline-view`) conforme MR-E2E priorizados na `02-brd.md`; (b) **redactor LGPD Layer 2** (`lib/redactor.ts` ~120 LOC) — sed de headers `Authorization|Cookie|apikey|x-api-key|x-supabase-*` + body redaction em `redactedPaths` + sanitização de cookies — BEFORE qualquer commit de HAR; (c) **mesh-persistor** (`lib/mesh-persistor.ts` ~100 LOC) — insere `observation` node + `OBSERVES` edge por finding com idempotency key SHA-256; (d) **telemetry** (`lib/telemetry.ts` ~60 LOC) — emit `infra_health_logs` events `e2e_user_zero_run_started/complete/failure/auth_expired`; (e) **runner selftest** (`__selftest__/runner.test.ts` ~150 LOC) — runner executado contra mock browser fixtures; (f) **Pre-commit hook extension** — scan `e2e-output/` por padrões `eyJ.*\.eyJ`, `sk_(live|test)_`, `sbp_`, `whsec_` antes de aceitar commit. Total estimado: +590 LOC restantes do SDD. Recomendado executar JUNTO com Canvas Studio Phase 4.2 — primeira sessão real de UI permite testar dogfood mode + redactor sobre flows credentialed e PRIMEIRA emissão do claim `e2e_user_zero_last_pass: <id>` no Phase 5c.
> 5952	
> 5953	1. ~~**[DQP 🔴] Implementar `process-affiliate-link`**~~ ✅ Done (2026-04-26)
> 5954	
> 5955	2. ~~**[DQP 🔴] Revenue webhook (`handle-ml-postback`)**~~ ✅ Done (2026-05-01) — deployed 58.74 kB · ML Dev Center callback configurado · revenue_cents agora flui do ML para o banco
> 5956	
> 5957	3. ~~**[DQP ⚠️] utm_campaign dinâmico**~~ ✅ Done (2026-05-01) — `orchestrate-content` usa `campaign_id` real + `utm_term={keyword}`
> 5958	
> 5959	4. **Stripe live keys** — Intencional: sandbox enquanto Gabriel valida como Usuário Zero. Trocar apenas quando primeiro cliente externo:
> 5960	   ```bash
> 5961	   npx supabase secrets set STRIPE_SECRET_KEY=sk_live_...
> 5962	   npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_live_...
> 5963	   ```
> 5964	
> 5965	5. ~~**Bug autonomic-action n8n**~~ ✅ Resolvido — comportamento correto: +10pts/run via endpoint n8n é feature de acúmulo autônomo, não bug.
> 5966	
> 5967	6. ~~**Primeiro run end-to-end como Usuário Zero**~~ ✅ Done (2026-05-25 em v6.8.2) — pipeline_run `76702931` status=done, WP draft p=10, content_mesh_asset `6a8bd475`, mco_balance debit -10 atomic. Falta apenas: WP swap draft→publish + processar primeiro affiliate link real + esperar primeira conversão ML para fechar `revenue_cents > 0` no ROIWidget.
> 5968	
> 5969	7. ~~**AIOS — modelo gemini-2.0-flash deprecado**~~ ✅ Resolvido (2026-05-02) — migrado para `gemini-2.5-flash` em toda a stack (CorePage, useAIOSChat, aios-chat edge function). Fallback vault captura 404.
> 5970	
> 5971	8. ~~**AIOS — provisionar chave Gemini Live**~~ ✅ Resolvido (2026-05-06) — `VITE_GEMINI_API_KEY` no `.env` local + `GEMINI_API_KEY` no vault Supabase. Live Mode (BidiGenerateContent WS) ativo no AIOSTerminal; text chat usa vault.
> 5972	
> 5973	8. ~~**[Arena] Deploy `openrouter-swarm`**~~ ✅ Done (2026-04-26)
> 5974	
> 5975	9. ~~**[Arena] Injetar secrets LinkedIn**~~ ✅ Done (2026-04-26)
> 5976	
> 5977	### SPRINT — Query Consolidation (Issues #002 #003 #009)
> 5978	
> 5979	- ~~**#002 user_roles 3x/load** — centralizar em hook com `staleTime: Infinity`~~ ✅ Done (2026-05-04) — `useAdminData` migrado para TanStack Query `staleTime: Infinity, gcTime: Infinity`
> 5980	- ~~**#003 mcorch_nodes N+1 (6 queries)** — consolidar com `fetchAllPages<T>()` module-level~~ ✅ Done (2026-05-04) — `useMcorchMemory` reescrito, múltiplos mounts compartilham 1 cache
> 5981	- ~~**#009 aios_conversations 4x/navegação** — único hook com `staleTime: 60_000`~~ ✅ Done (2026-05-04) — `staleTime: 60_000` adicionado ao `useInfiniteQuery`
> 5982	
> 5983	### SOCIAL — Next steps
> 5984	
> 5985	- **Twitter API Basic tier** — Twitter `CreditsDepleted` (Free tier write limit). Upgrade para Basic ($100/mo) para auto-publish funcionar no Twitter. LinkedIn está publicando ✅.
> 5986	- **Instagram App Review** — App MCORCH-IG em modo desenvolvimento (funciona para Usuário Zero). Submeter App Review Meta para habilitar publicação com terceiros. Permissões necessárias: `instagram_business_content_publish`, `instagram_business_basic`.
> 5987	- ~~**Knowledge Mesh ADRs** — Inserir nós `decision` para Twitter PKCE e Instagram Login API v21~~ ✅ Done (2026-05-04) — 5 nós ADR via `seed-social-oauth-adrs.ts`
> 5988	
> 5989	### NON-CRITICAL
> 5990	
> 5991	- `login.mcorch.com` DNS → redirect to `/auth` (não configurado)
> 5992	- `decay_mcorch_stability()` — ✅ now callable manually: `SELECT * FROM decay_mcorch_stability();`
> 5993	- `browserslist` — ✅ updated (2026-04-26)
> 5994	- **[Arena] Swarm Arena Phase 2:** Integrar `fastest_model` como roteador padrão em `orchestrate-content` — se latência < 2s, usar o modelo vencedor para geração de content rápido em vez de modelo fixo
> 5995	
> 5996	### GITNEXUS MCP — Next steps
> 5997	
> 5998	- ~~**Build + integrar:** `cd packages/gitnexus-core && npm run build` → adicionar ao `.mcp.json`~~ ✅ Done
> 5999	- ~~**Delta v2 bridge:** SupabaseAdapter.syncFromGraph() + CLI sync-to-mesh~~ ✅ Done — 493 nós, 344 edges
> 6000	- ~~**Delta v3 — Call-graph intra-file:** scope-tracked walker no TypeScript visitor~~ ✅ Done
> 6001	- ~~**Delta v4 — Cross-file calls:** Two-pass ingestion + globalFunctionMap → +259 edges~~ ✅ Done (2026-04-26) — 646 edges total
> 6002	- ~~**Embeddings dos nós AST:** 493/493 embedded~~ ✅ Done
> 6003	- ~~**Delta v5 — Embeddings para novos edges (192):** Disparar `embed-mcorch-node` para os 192 CALLS edges inseridos no Delta v4~~ ✅ Done (2026-05-05) — sync-mesh pós-commit → 2559 nós 100% embedded · 3516 edges
> 6004	- **Subir container Docker:** `docker compose up -d mcorch-gitnexus-mcp` (opcional — stdio já funciona)
> 6005	
> 6006	### PHASE EPSILON — Next iterations
> 6007	
> 6008	- ~~**Epsilon v1–v8:** Sigma WebGL, Louvain, Semantic Probe, Crew Overlay, MatrixPage, Ownership coloring, Territory UX, CALLS counter~~ ✅ All done
> 6009	- **Epsilon v9 — WebGPU upgrade:** Monitorar `sigma@next` — não disponível em npm (2026-05-01). Migrar quando estável.
> 6010	- ~~**Epsilon v9 — Nó de maior conectividade:** Badge/highlight no nó com maior `callsIn` (hub da arquitetura)~~ ✅ Done (2026-05-05) — badge dourado ★ + pulse + fly-to animado
> 6011	
> 6012	### CORE — Next iterations
> 6013	
> 6014	- ~~**Core v2 — AIOS Consciousness:** Gemini TTS neural (AudioContext AnalyserNode), divider drag, model selector tri-provider, 429 fallback~~ ✅ Done (2026-05-01)
> 6015	- **Core v3 — Gemini Live WebSocket:** Upgrade do tri-mode para WebSocket nativo da Gemini Live API (Barge-in real com áudio PCM bidirecional) — requer `GEMINI_API_KEY` provisionada
> 6016	- **Phase Zeta — Social Consciousness:** Cada sessão AIOS persistida como nó `conversation` em `mcorch_nodes`. Feed timeline no CorePage (X/Twitter arch). DERIVES_FROM edges para reasoning threads. Fork de sessão (copy context → novo nó). "Boost": compartilhar conversa para Antigravity ou Claude Code.
> 6017	- **Core v3 — Ondas reativas a voz:** Conectar AudioContext (frequência do microfone) ao `intensity` das VibrationalWaves — campo visual responde ao timbre da voz em tempo real
> 6018	
> 6019	### PHASE DELTA — Next iterations
> 6020	
> 6021	- ~~**Delta v2:** Persist canvas pipelines to `mcorch_nodes`~~ ✅ Done
> 6022	- ~~**Delta v3:** Call-graph intra-file~~ ✅ Done
> 6023	- ~~**Delta v4:** Cross-file call resolution~~ ✅ Done
> 6024	- **Delta v5:** Agentic Consensus UI — real-time Auditor/Estrategista triangulation panel no OrchestrationCanvas
> 6025	- **Delta v6:** Video pipeline canvas — SceneNodes → TransitionNodes wired to `generate-video`
> 6026	- **Delta v7:** Dynamic sub-agent spawning from failed nodes (AOrchestra pattern)
> 6027	
> 6028	### USUÁRIO ZERO — Checklist de validação
> 6029	
> 6030	- ✅ mco_balance injetado: 5003 mcoCoins (2026-04-26)
> 6031	- ✅ Stripe sandbox secrets no vault
> 6032	- ✅ Token expiry UI visível (DQP auditado 2026-04-26)
> 6033	- ✅ Latência visual <50ms confirmada (DQP auditado 2026-04-26)
> 6034	- ✅ Bug autonomic-action resolvido — comportamento correto (+10pts/run via n8n)
> 6035	- ✅ affiliate_links.revenue_cents: process-affiliate-link + handle-ml-postback implementados (2026-05-01)
> 6036	- ✅ Neural density 100% — 1993/1993 nós embedded (2026-05-03)
> 6037	- ✅ Code tab real — 1758 nós com código-fonte (2026-05-03)
> 6038	- ✅ AI Brain real — analyze-node edge function deployed (2026-05-03)
> 6039	- ✅ Pipeline embedding autônomo — pg_net trigger + post-commit hook + MeshControlPanel (2026-05-03)
> 6040	- ✅ **Primeiro run end-to-end** — orchestrate-content → WordPress (draft p=10) → LinkedIn scheduled → content_mesh_asset `6a8bd475` (2026-05-25). Faltam: WP draft→publish swap, affiliate link real, ML conversion para `revenue_cents > 0`.
> 6041	- ⬜ Verificar `infra_health_logs` populando após 1ª campanha
> 6042	- ⬜ Swap para Stripe live keys (intencional — sandbox enquanto valida como Usuário Zero)
> 6043	
> 6044	---
> 6045	
> 6046	## Infrastructure
> 6047	
> 6048	| Service | Container | Port | Status |
> 6049	|---------|-----------|------|--------|
> 6050	| Vector Engine | `mcorch_chroma` | `localhost:8001` | ✅ healthy (healthcheck fix :1F40 — 2026-05-01) |
> 6051	| Intelligence Node | `mcorch_claude_mem` | — | ✅ healthy |
> 6052	| Autonomic Daemon | `mega-brain-daemon` | — | ✅ healthy |
> 6053	| Brain Webhook | `mega-brain-webhook` | — | ✅ healthy |
> 6054	| Brain Dashboard | `mega-brain-dashboard` | — | ✅ up |
> 6055	| **GitNexus MCP** | `mcorch_gitnexus` | `localhost:3100` | ✅ built (stdio ativo) · Docker opcional |
> 6056	| Watchdog Cron | crontab (ubuntu + gcrUX) | — | ✅ `*/5 * * * *` watchdog-mcorch.sh |
> 6057	| Auto-publish Cron | crontab gcrUX | — | ✅ `*/5 * * * *` auto-publish-cron.sh |
> 6058	| Audit 4Cs Cron | crontab gcrUX | — | ✅ `0 12 * * 1` audit-4cs.sh (seg 09h BRT) |
> 6059	
> 6060	**Chroma API is v2** — use `http://localhost:8001/api/v2/heartbeat`
> 6061	
> 6062	```bash
> 6063	docker compose up -d
> 6064	docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> 6065	```
> 6066	
> 6067	---
> 6068	
> 6069	## Security Model (Post-Go-Live)
> 6070	
> 6071	| Table | Isolation |
> 6072	|-------|-----------|
> 6073	| `mcorch_nodes` | `user_id IS NULL OR auth.uid() = user_id` (system nodes visible to all) |
> 6074	| `mcorch_edges` | Same pattern |
> 6075	| `infra_health_logs` | Read-all for authenticated; write only service_role |
> 6076	| All other tables | `user_id = auth.uid()` via existing RESTRICTIVE policies |
> 6077	
> 6078	---
> 6079	
> 6080	## Billing Architecture
> 6081	
> 6082	| Decision | Value |
> 6083	|----------|-------|
> 6084	| Canonical billing ledger | `profiles.mco_balance` |
> 6085	| Deduction RPC | `public.deduct_mco_coins(p_user_id uuid, p_amount decimal)` |
> 6086	| Cost constants | `src/lib/billing.ts` → `COIN_COSTS` |
> 6087	| Orchestration cost | 10 mcoCoins/run |
> 6088	| Plan allocation | Starter: 500 · Pro: 2000 · Enterprise: 10000 |
> 6089	| Stripe | Sandbox keys active — swap to live before first client |
> 6090	
> 6091	---
> 6092	
> 6093	## GraphRAG State
> 6094	
> 6095	- **8748 total nodes** (verificado live 2026-06-01 via REST count=exact após o handoff node `af33a839-acd9-412d-a770-8ad5a2edccb4` desta seal v6.20.0, embedded 768d; v6.19.0 snapshot era 8747, handoff `59f92fe0`) — **100% embedded** (768d HNSW cosine) — handoff · milestone · architecture · decision · system · observation · requirement · conversation · documentation_suite (BoK seal) · crew_agent · markdown_file · vault_note · feature · ui-ux · content_mesh_asset + AST (file · function · arrow_function · interface · type_alias · class)
> 6096	- **9070 total edges** (verificado live 2026-06-01 via REST count=exact; v6.6.9 snapshot registrava 11925, cujo +1 foi DERIVES_FROM edge `4254225d-a666-4363-a4bd-98947efc434f` → mcorch-qa-healing parent) — defines · calls · INHABITS · DERIVES_FROM · REQUIRES · observes (OE-661-003) · ATTRIBUTES_REVENUE_TO (OE-661-EXECUTE) · CONTAINS_LINK_FOR (OE-661-004) · OBSERVES (e2e-user-zero finding observations — when runner.ts lands)
> 6097	- Neural density: **100%** — trigger INSERT autônomo garante embedding imediato
> 6098	- Paginação completa na Matrix (fetchAll() 1000 rows/page)
> 6099	- AIOS grounding: 26+ nós por sessão via multi-bucket + semantic search (pgvector HNSW cosine 768d)
> 6100	- Phase Zeta: node_type `conversation` persistido — cada sessão AIOS vira nó + DERIVES_FROM edges
> 6101	- `useKnowledgeMesh` exporta `meshStats` com totalNodes/totalEdges/dominantTypes — `contextString` e `contextNodeIds` memoizados
> 6102	- HNSW cosine index operational
> 6103	- Milestone node (2026-05-04): `session-handoff-20260504-social-pipeline-live` inserido
> 6104	- ADR nodes (2026-05-04): 5 decision/milestone nodes via `seed-social-oauth-adrs.ts` — Social OAuth ADRs pesquisáveis semanticamente
> 6105	- Content backfill: 1758 nós AST com código-fonte real via `scripts/backfill-node-content.ts`
> 6106	- Milestone node (2026-05-05): `session-handoff-20260505-settings-sovereignty` inserido
> 6107	- Milestone node (2026-05-06): `session-handoff-20260506-core-promotion` inserido
> 6108	- Milestone node (2026-05-06): `session-handoff-20260506-devops-security-seal` inserido
> 6109	- Milestone node (2026-05-06): `session-handoff-20260506-layout-ux-fixes` inserido
> 6110	- Documentation suite (2026-05-07): `bok-scribe-seal-mcorch-constellation-v1` inserido (type=`documentation_suite` · stability 0.85)
> 6111	- Milestone node (2026-05-08): `session-handoff-20260508-fmea005-lgpd-deploy` inserido (esta sessão · FMEA-005 closed + LGPD em produção)
> 6112	- Milestone node (2026-05-07): `session-handoff-20260507-bok-suite-v1` inserido
> 6113	- Milestone node (2026-05-08): `session-handoff-20260508-sprint-v580` será inserido nesta seal
> 6114	- Milestone node (2026-05-14): `session-handoff-20260514-canvas-4-1-shell` (`c93c74c3-42cd-4f4b-92d9-775bd9cbfa86`) inserido + embedded (768d) — Canvas 4.1 shell + Higgsfield endpoint fix
> 6115	- Documentation suite (2026-05-14): `bok-scribe-seal-viralmind-v1` (`5c4bf1e9-b7cb-4896-a3b8-038f64f56ecf`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact R$ 14M) — suíte BoK viralmind 9/9 selada (04-frd reescrito de handbook CLAUDE.md → FRD real; handbook realocado p/ `viralmind-dev-handbook.md`; 7 OTDs registrados; DERIVES_FROM `bok-scribe-seal-conteudo-v2-v1`)
> 6116	- Milestone node (2026-05-16): `session-handoff-20260516-openclaw-v631-neural-bridge` (`c1dbc53b-3a27-4da7-aef3-debd5c4047a0`) inserido (type=`milestone` · stability 1.0) — Sprint v6.3.1 selada (OpenClaw Neural Bridge + Departmental Army Pantheon; 9185 chunks indexados across 6 agentes; cron pipeline 02:30/03:00/03:30 ativo; primeira Telegram briefing entregue msg_id 201)
> 6117	- Observation node (2026-05-17): `pantheon-config-audit-2026-05-17` (`ccecdbd1-8007-40c4-8c88-fb3463b6fe55`) inserido (type=`observation` · stability 0.85) — Phase 1 v6.6.1 (Pantheon canonical files unificados: 7 MEMORY.md + 7 BOOTSTRAP.md + main SOUL enhanced + HEARTBEAT tasks + pantheon-role-matrix.md)
> 6118	- Observation node (2026-05-17): `memory-wiki-population-2026-05-17` (`569ba6bf-b2df-443e-9bba-b0c064032ab7`) inserido (type=`observation` · stability 0.85) — Phase 2 v6.6.1 (Memory Wiki seed manual MCORCH-aware: 20 wiki pages autorados; 5 syntheses + 8 entities + 6 concepts + 1 chatgpt-export source)
> 6119	- Handoff node (2026-05-17): `session-handoff-20260517-pantheon-config-memory-wiki-unblock` (`d48f59d4-cf7b-44c5-83a3-2eb3db0b7e17`) inserido (type=`handoff` · stability 1.0) — v6.6.1 selada consolidando 3 trilhos sequenciais (Pantheon config audit + Memory Wiki seed manual + agents.list enabled key drift fix); confirmação visual Sovereign: Memory Palace renderiza 5 syntheses · 18 claims · 11 questions · 2 contradictions + Imported Insights 1 cluster AIOS medium risk
> 6120	- Handoff node (2026-05-17): `session-handoff-20260517-canvas-4-2c-async-video` (`eb0b3ae0-9ec1-4328-ad31-1b079d3f294e`) inserido (type=`handoff` · stability 1.0) — v6.6.2 selada com Phase 4.2c async video pipeline live (canvas-execute branch image_to_video + Realtime callback + tier-gate dop-standard + watchdog cron) + 3 rounds de hotfix (assertExecuteSuccess unifica fail handling; OpenAI sem response_format + URL download server-side; OpenRouter migrado pra chat-completions multimodal Gemini+FLUX; Replicate column + SettingsPage; canvas-assets RLS reparada via DROP+CREATE com TO public guard); saldo Sovereign 5533 intacto pré e pós-sessão (zero cobrança em failed paths)
> 6121	- Handoff node (2026-05-18): `session-handoff-20260518-oe661-debt-liquidation` (`6f2cf405-4bb5-440b-a02a-9579fc39f29f`) inserido (type=`handoff` · stability 1.0) — v6.6.3 selada com OE-661-ROADMAP debt liquidation completa (Postback ATTRIBUTES_REVENUE_TO + Memory gateway-recovery skill + Million-BRL Link Forge + OE-661-003 Target Binding) + Financial Stripe DEFERRED por decisão Sovereign; +7 nodes (8336→8343), +1555 edges (10062+→11617 com observes retrofit + autoembed cascade); 3 Edge Functions redeployed (process-affiliate-link 78.31kB Hybrid POST+GET · handle-ml-postback 59.34kB · embed-mcorch-node 105.1kB com auto-stitch); 10/10 observations VALID em Target Binding audit; 4 markdown_files autoembed (gateway-recovery + revenue-flywheel + roadmap-v1 + link-forge-scope)
> 6122	- Documentation suite (2026-05-18): `bok-scribe-seal-gamificacao-nodes-v1` (`6e8546bc-d995-4cc5-ac88-06cecbece181`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.4 selada com gamificacao-nodes BoK 9/9 retroativa (5 docs novos + 3 drifts reconciliados; DERIVES_FROM `bok-scribe-seal-viralmind-v1`; 12 BR-GN + 9 PROC-GN + 10 KPI-GN + 10 FMEA-GN com 4 RPN > 100)
> 6123	- Documentation suite (2026-05-19): `bok-scribe-seal-openclaw-v1` (`05c55dfd-d318-4dcf-b7f0-aefb0529872f`) inserido (type=`documentation_suite` · stability 0.85 · revenue_impact 0) — Sprint v6.6.5 selada com openclaw BoK 9/9 retroativa (9 docs novos · 2500 LOC total · DERIVES_FROM `bok-scribe-seal-gamificacao-nodes-v1`; 14 BR-OC + 10 PROC-OC + 10 KPI-OC + 10 FMEA-OC com 5 RPN > 100; 5 drifts FECHADOS em v6.4.0/v6.6.1 + 8 ATIVOS como OTDs; OTD-V631-001 RPN 280 fechada por esta seal — 5ª e última suíte BoK do projeto)
> 6124	- Handoff node (2026-05-19): `session-handoff-20260519-openclaw-bok-9-of-9-v665` (`8455932c-1486-490b-99a2-894022e2ba5a`) inserido (type=`handoff` · stability 1.0) — v6.6.5 selada quitando última dívida BoK do projeto; **5/5 suítes BoK seladas** (viralmind · conteudo-v2 · mcorch-constellation · gamificacao-nodes · openclaw); BoK Gate liberado para código novo em qualquer módulo; carry-overs OE-661 (GCRUX_ML_AFFILIATE_TOKEN + content_mesh_asset emission + primeiro run Usuário Zero) seguem pendentes
> 6125	- Observation node (2026-05-19): `execution-plan-oe661-carryovers-2026-05-19` (`3dde2572-cad6-491b-b523-c56ec763ff8e`) inserido (type=`observation` · stability 0.85) — plan persistido para Fases 1-3 (OE-661 wire + Ledger SOP + Canvas 4.2c paid smoke) por diretiva Sovereign "slave o plano atual"; emendado com 10 fixes pós-audit (A-J); md5 `0e5f0ba995e89bc7ef76cda00733f941`
> 6126	- Observation node (2026-05-19): `audit-oe661-debt-sweep-2026-05-19` (`6164c80f-cadd-48d5-95a4-f87f22ebd09b`) inserido (type=`observation` · stability 0.9) — audit completo: 3 Explore agents + 12 REST queries materiais; 21 OTDs ativos catalogados (8 RPN ≥ 100); 5 inconsistências processuais incluindo 5 seals consecutivas omitindo Survival Laws Self-audit; 4 bugs concretos no plan original fixed via amendments
> 6127	- Edge DERIVES_FROM (2026-05-19): `acb4b0d9-091d-4973-96a8-d40515be7990` (audit `6164c80f` → plan `3dde2572`) weight=1.0 — audit derivou-se do plan + recomendou as 10 emendas
> 6128	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-plan-audit-v666` (`821dc554-78e2-4abb-999d-37363c5df6c9`) inserido (type=`handoff` · stability 1.0) — v6.6.6 sealed: Planning Seal + Debt Audit + Self-audit Retroativo das 5 seals omitidas; zero código tocado; mesh 8352 nodes; predicted Survival v3 aggregate 4.4/5
> 6129	- Handoff node (2026-05-19): `session-handoff-20260519-oe661-phase1-prep-v667` (`9d482014-a759-4656-93d9-99e05ab4a714`) inserido (type=`handoff` · stability 1.0) — v6.6.7 sealed: OE-661 Phase 1 prep complete (SOP Law 2 + Amendments A/B/C/E shipped + 2 Edge Functions deployed + vault provisioned + API Tenancy directive Sovereign-class em CLAUDE.md + OTD-OE661-PER-USER); Step 1.5 first run E2E deferido por context budget Sovereign 92% (retoma em ~3h); mesh 8353 nodes; Survival Audit retroativo das 5 seals omitidas incluído (Lei 1 ✓ 5/5 · Lei 2 ✓ 3/5 · Lei 3 ✗ 0/5 · Lei 4 ✗ 0/5 — OTD-PROC-001 RPN 60 / OTD-PROC-002 RPN 40 registradas)
> 6130	
> 6131	### Embedding Model
> 6132	`openai/text-embedding-3-small`, `dimensions: 768` (truncated output via OpenRouter).
> 6133	Schema: `vector(768)` — HNSW cosine index.
> 6134	
> 6135	### Embedding Pipeline (Autônomo — 2026-05-03)
> 6136	Três camadas eliminam intervenção manual:
> 6137	1. **INSERT trigger** — `trg_mcorch_embed_on_insert` (pg_net) dispara `embed-mcorch-node` assincronamente em todo INSERT onde `embedding IS NULL`. Nunca bloqueia o INSERT.
> 6138	2. **Post-commit hook** — `.git/hooks/post-commit` roda `node scripts/ingest-codebase.ts --quiet` em background após cada commit → re-ingesta AST.
> 6139	3. **MeshControlPanel** — UI bottom-left do MatrixPage: "Sync Embeddings" (`trigger-embeddings`) e "Refresh Mesh Stats" (`trigger-ingest`).
> 6140	
> 6141	### Comandos de manutenção da Mesh
> 6142	```bash
> 6143	# Verificar nós sem embedding (deveria retornar array vazio):
> 6144	curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?embedding=is.null&select=id,name" \
> 6145	  -H "apikey: $SB_SECRET_KEY" | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'{len(d)} nós sem embedding')"
> 6146	
> 6147	# Backfill manual (Bun-native — requer .env):
> 6148	bun run scripts/backfill-embeddings.ts
> 6149	
> 6150	# Backfill de código-fonte nos nós AST:
> 6151	bun run scripts/backfill-node-content.ts
> 6152	
> 6153	# Re-sync AST completo:
> 6154	cd packages/gitnexus-core && npm run sync-mesh
> 6155	
> 6156	# Acompanhar re-ingesta pós-commit:
> 6157	tail -f /tmp/mcorch-ingest.log
> 6158	```
> 6159	
> 6160	---
> 6161	
> 6162	## Video Rescue Protocol
> 6163	
> 6164	When a video generation operation (Google Veo) times out or client disconnects:
> 6165	```bash
> 6166	# Via edge function (production):
> 6167	curl -X POST "https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/rescue-video" \
> 6168	  -H "Authorization: Bearer <user_jwt>" \
> 6169	  -d '{"content_id":"<uuid>","operation_id":"<operation_name>"}'
> 6170	
> 6171	# Via local script (admin/debug):
> 6172	source .env && bun run rescue.ts <operation_id> <content_id>
> 6173	```
> 6174	
> 6175	---
> 6176	
> 6177	## Architecture Pillars
> 6178	
> 6179	| Layer | Implementation |
> 6180	|-------|---------------|
> 6181	| **Infra** | Docker Sovereign Mesh (`mcorch_chroma` + `mcorch_claude_mem` + `mega-brain-daemon`) + `watchdog-mcorch.sh` telemetry |
> 6182	| **Memory** | GraphRAG (`mcorch_nodes`/`mcorch_edges`) + Neural Embeddings via OpenRouter (openai/text-embedding-3-small, 768d) + HNSW cosine index |
> 6183	| **Economics** | mcoCoins Gatekeeper (`profiles.mco_balance` → `deduct_mco_coins` RPC) + Real ROI (`affiliate_links.revenue_cents`) + Stripe Sandbox |
> 6184	| **Rescue** | Video recovery via `rescue-video` edge function + `rescue.ts` local companion |
> 6185	| **Protocol** | ShakeHands (`/handson` pick-up, `/handoff` seal) |
> 6186	
> 6187	---
> 6188	
> 6189	## Phase Delta — Architecture
> 6190	
> 6191	```
> 6192	OrchestrationPage (full-canvas, p-0)
> 6193	  └── OrchestrationCanvas.tsx        ← @xyflow/react, nodeTypes/edgeTypes registry
> 6194	        ├── nodes/TriggerNode.tsx    ← topic input + platform toggles + Run button
> 6195	        ├── nodes/AgentNode.tsx      ← AI step display (status pulse animation)
> 6196	        ├── nodes/SceneNode.tsx      ← video scene (stability + coin cost)
> 6197	        ├── nodes/QualityGateNode.tsx← blocks downstream on error
> 6198	        ├── nodes/PublishNode.tsx    ← final distribution output
> 6199	        ├── edges/OrchestrationEdge.tsx ← glowing bezier (violet when animated)
> 6200	        └── NodePalette.tsx          ← top toolbar to add nodes
> 6201	
> 6202	src/store/useOrchestrationStore.ts   ← Zustand (nodes, edges, run state)
> 6203	src/hooks/useOrchestrationGraph.ts   ← runPipeline → orchestrate-content → node status sync
> 6204	supabase/migrations/20260426120000_delta_graph_positioning.sql
> 6205	  ├── GIN indexes on mcorch_nodes.metadata + mcorch_edges.metadata
> 6206	  └── decay_mcorch_stability() — FSRS-6 manual decay (free tier safe)
> 6207	```
> 6208	
> 6209	### Canvas State Architecture (Hybrid)
> 6210	
> 6211	```
> 6212	User interaction → ReactFlow internal state (positions, drag)
> 6213	                         ↓ (debounced 600ms)
> 6214	                   localStorage (positions persist across refresh)
> 6215	                         ↑
> 6216	Store (Zustand) ← runPipeline → orchestrate-content Edge Function
> 6217	     ↓ (status changes sync to ReactFlow via useEffect)
> 6218	ReactFlow renders visual status (idle/running/done/error/blocked)
> 6219	```
> 6220	
> 6221	## Key Files
> 6222	
> 6223	| Purpose | Path |
> 6224	|---------|------|
> 6225	| Architecture rules | `CLAUDE.md` |
> 6226	| **3D Constellation Graph** | `src/components/graph/CrewGraph.tsx` |
> 6227	| **Crew data hook** | `src/hooks/useCrewData.ts` |
> 6228	| **Agent edges (particles)** | `src/components/graph/AgentEdge.tsx` |
> 6229	| **Squad hull (3D bubble)** | `src/components/graph/SquadHull.tsx` |
> 6230	| **Visual Orchestrator Canvas** | `src/components/orchestrator/OrchestrationCanvas.tsx` |
> 6231	| **Orchestration Store (Zustand)** | `src/store/useOrchestrationStore.ts` |
> 6232	| **Pipeline hook** | `src/hooks/useOrchestrationGraph.ts` |
> 6233	| **Node types** | `src/components/orchestrator/nodes/` |
> 6234	| GraphRAG hook | `src/hooks/useMcorchMemory.ts` |
> 6235	| Memory graph (d3-force + stability) | `src/components/dashboard/MemoryGraphWidget.tsx` |
> 6236	| Real ROI widget | `src/components/dashboard/ROIWidget.tsx` |
> 6237	| Dashboard header (mcoCoins HUD) | `src/components/dashboard/DashboardLayout.tsx` |
> 6238	| Neural Mesh HUD | `src/components/HUD.tsx` |
> 6239	| Infra status hook | `src/hooks/useInfraStatus.ts` |
> 6240	| Billing utilities | `src/lib/billing.ts` |
> 6241	| Orchestration function | `supabase/functions/orchestrate-content/index.ts` |
> 6242	| Infra status function | `supabase/functions/get-infra-status/index.ts` |
> 6243	| Embed function | `supabase/functions/embed-mcorch-node/index.ts` |
> 6244	| Video rescue function | `supabase/functions/rescue-video/index.ts` |
> 6245	| Video rescue (local) | `rescue.ts` |
> 6246	| Watchdog + telemetry | `scripts/watchdog-mcorch.sh` |
> 6247	| Backfill script | `scripts/backfill-embeddings.ts` |
> 6248	| Deploy harness | `scripts/harness-deploy.sh` |
> 6249	
> 6250	---
> 6251	
> 6252	## First Client Onboarding Checklist
> 6253	
> 6254	1. ~~Set OPENROUTER_API_KEY in vault~~ ✅ Done
> 6255	2. ~~Run backfill~~ ✅ Done (9/9 nodes)
> 6256	3. ~~Activate watchdog cron~~ ✅ Done
> 6257	4. ~~Deploy rescue-video function~~ ✅ Done
> 6258	5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 6259	6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 6260	7. Monitor `infra_health_logs` for first 24h.
> 6261	8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 6262	
> 6263	---
> 6264	
> 6265	## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 6266	
> 6267	Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 6268	
> 6269	| Action | Result |
> 6270	|--------|--------|
> 6271	| `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> 6272	| `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> 6273	| `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> 6274	| `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> 6275	| `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 6276	
> 6277	| Commit | Conteúdo |
> 6278	|--------|----------|
> 6279	| `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> 6280	| `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> 6281	| `c7b5a1d` | chore(ui): progress indicator styling support |
> 6282	
> 6283	### Arquitetura Matrix Intelligence
> 6284	
> 6285	```
> 6286	ConstellationMatrix (Stabilized Engine)
> 6287	  ├── useConstellationSigma (stable refs, no re-bind on render)
> 6288	  └── NodeDetailsPanel (Tabbed Navigation)
> 6289	        ├── Tab Meta: Neighbor exploration + Net Context
> 6290	        ├── Tab Code: Source code preview (Supabase sync)
> 6291	        └── Tab Brain: semantic analysis (Gemini orchestrator)
> 6292	
> 6293	useNodeIntelligence Hook:
> 6294	  - contentQuery: fetch nodes.content column
> 6295	  - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
> 6296	  - state: isAnalyzing, analysisResult, progress
> 6297	```
> 6298	
> 6299	---
> 6300	
> 6301	## AI Brain — Real Intelligence Wiring (2026-05-03)
> 6302	
> 6303	Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 6304	
> 6305	| Action | Result |
> 6306	|--------|--------|
> 6307	| `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> 6308	| `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> 6309	| Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 6310	
> 6311	**Output da análise (estruturado em pt-BR):**
> 6312	- Visão Geral — papel do módulo no sistema
> 6313	- Padrões Detectados — design patterns, antipatterns
> 6314	- Acoplamento & Dependências — análise In/Out-Degree
> 6315	- Recomendações — 1-3 ações priorizadas
> 6316	
> ```

## 🤖 Claude *(20:55:09)*


## 🤖 Claude *(20:55:10)*

Brief assembled. Let me grab the "Top 3 Gap Closures" section from sprint-priorities (file is 183 lines, I've seen 56) to report the precise top gap.

## 🤖 Claude *(20:55:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n -A 25 -iE \"Top 3 Gap|Top Gap|Gap Closure\" .claude/context/sprint-priorities.md | head -50",
  "description": "Extract Top Gap Closures section"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 7:**Sprint v6.20.3 selado em 2026-06-02** — Disconnect RPC + revogação de segredo órfão: **FECHADO o Top Gap que a v6.20.2 sinalizou** — desconectar Meta/social fazia `.delete()` pela view → INSTEAD OF DELETE só apagava a linha base, deixando o segredo Vault **órfão** (plaintext retido; 12 órfãos Meta observados em prod). RPCs `disconnect_meta()`/`disconnect_social(p_account_id uuid)` (migration `20260602160000`) espelham `disconnect_wordpress` (`SECURITY DEFINER`, `search_path=''`, fail-closed `28000`, EXECUTE só authenticated): deletam a linha **E** revogam o segredo. Guard de tenant por name-binding (`id`-de-linha + PK ⇒ atacante nunca casa nome de segredo alheio; UUID bruto nunca vaza ao cliente). Limpeza one-time **12→0** órfãos Meta (orphan-scoped via `NOT EXISTS`+`right(name,36)`), 3 sociais vivos intactos. Hooks migrados `.delete()`→`.rpc()`; `types.ts` regenerado. **Também (diretiva A):** `/security-review` redundante do `87c926f` (guard de tenant v6.20.2) → **LIMPO 9/10**. Ambos os reviews SAFE; suíte RPC 5/5 em `BEGIN…ROLLBACK` (happy meta+social · foreign-id no-op · planted-ref name-binding · unauth 28000); Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8752**. 4 commits. **Lição:** verificar materialidade ANTES de codar (Lei 1) — o gap de tenant guard da diretiva original já estava 100% fechado em prod, então a Parte B virou o foco real em vez de uma migration redundante.
> 8-
> 9:**Sprint v6.20.2 selado em 2026-06-02** — Idempotência da encriptação + guard de tenant nas views irmãs: **FECHADO o Top Gap que a v6.20.1 sinalizou** — `trg_encrypt_user_api_keys` (+ irmãos meta/social) chamava `vault.create_secret` incondicionalmente → re-salvar segredo p/ valor novo colidia no índice único `vault.secrets.name` (`23505`). Helper `public.vault_upsert_secret(value,name,desc)` (`SECURITY DEFINER`, `search_path=''`, EXECUTE revogado de PUBLIC/anon/authenticated) rotaciona in-place via `vault.update_secret` (mesmo UUID, sem órfãos) senão cria; as 3 encrypt triggers passam a usá-lo (migration `20260602140000`). O `/security-review` dessa migration **expôs um gap pré-existente** nas INSTEAD OF de `meta_config`/`social_accounts` (sem guard `auth.uid()` → injeção cross-tenant id-novo; o overwrite id-colidente já era fail-closed pelo PK — achado HIGH do review REFUTADO material) → guard `42501` portado pras 2 (migration `20260602150000`). Ambas `/security-review` **SAFE**; tudo provado material via Management API em `BEGIN…ROLLBACK` (antes 23505/injeção OK, depois OK/42501); Phase 5c **SEAL ALLOWED** (7 verified). Mesh **8751**. 6 commits. **Novo gap (Top Gap):** desconectar Meta/social deixa o segredo Vault **órfão** (INSTEAD OF DELETE só apaga a linha base) — precisa de RPC dedicada de disconnect (nula+revoga) no padrão `disconnect_wordpress()`, débito LGPD. **Lição:** adversarial-verify material (PK fail-closed + md5 da vítima) refutou um HIGH e ao mesmo tempo revelou o gap real adjacente — resolvido na mesma sessão em vez de empurrar pra fria.
> 10-
> 11:**Sprint v6.20.1 selado em 2026-06-02** — WordPress BYOK + fix do double-fire da encriptação de credenciais: fechado o P0 que a v6.20.0 sinalizou (`SocialAccountsPage` salvava/desconectava WP via `.upsert(onConflict)` numa VIEW → HTTP 400 `42P10`). Save → `.insert()`; disconnect → RPC **`disconnect_wordpress()`** (`SECURITY DEFINER`, `auth.uid()`, nula 3 cols WP + **deleta o segredo do Vault** — revogação LGPD) (migration `20260602120000`). Corrigir isso revelou bug **muito maior**: o `trg_instead_of_user_api_keys` usava `INSERT...ON CONFLICT DO UPDATE` → trigger de encriptação dispara **2×** numa só statement → `vault.create_secret` nome duplicado → **`23505`**, quebrando connect/save de **todo** usuário com linha pré-existente (e `.update` re-encriptava o `••••`). Trocado p/ **UPDATE-first / INSERT-if-not-found** + **guard de tenant** (`auth.uid()` → `42501`, fecha escrita cross-tenant que o ON CONFLICT mascarava) (migration `20260602130000`). Tudo provado material via Management API; 2 migrations `/security-review` **SAFE**; Phase 5c **SEAL ALLOWED** (8 verified). Mesh **8750**. 5 commits. **Novo gap (Top Gap — task spawned):** `trg_encrypt_user_api_keys` (+ irmãos meta/social) não-idempotente → editar segredo p/ valor novo sem desconectar antes ainda dá `23505`; conserto = update-or-create por nome nas 3 tabelas, precisa de `/security-review` próprio. **Lição:** probe-first material pegou que o `.insert` sozinho NÃO bastava (o bug estava na camada de encriptação, não nos 2 `.upsert` reportados).
> 12-
> 13-**Sprint v6.20.0 selado em 2026-06-01** — Afiliados híbrido + catálogo Apify real + BYOK per-user: corrigido o link de afiliado que abria login do CloudPanel (`panel.gcrux.com` proxy morto + `app_id` como affiliate id) → resolver **híbrido** `meli.la` cravado (per-user `metadata.shortlinks`) senão `product_url?matt_word=<affiliate_tag>` fail-closed (`src/lib/affiliate.ts` + 14 testes; 302s reais provados). ML bloqueia todo server-side (API 403/401, página→account-verification, nosso IP **e** Supabase Edge) → enriquecimento via actor **Apify** residencial (`enrich-affiliate-products.ts` SKU-match + `discover-affiliate-products.ts` descoberta real validando "viral mind") + gate de verificação em `useAffiliateProducts` + cron 6/6h. **2 IDs fabricados removidos** → catálogo com **3 produtos reais** (Roborock R$17.770 · Family Hub R$18.946 · 8K Neo QLED R$39.000). **BYOK per-user `apify_token`** no padrão Vault (migration `20260601060000`, `/security-review` PASS — pegou regressão `security_invoker`) + campo Settings + fix do P0 de `000600` (`.upsert()`→`.insert()` em view sem constraint). Phase 5c **SEAL ALLOWED** (12 verified). Mesh **8748**. Survival Laws 4/4. 6 commits. **Próximo:** Operador de Browser Autenticado (probe-first) p/ ações logadas (ML Compartilhar→meli.la). **Lição:** probe-first economizou 3 becos (API ML/Firecrawl/actor velho) e pegou IDs fakes + regressão de credencial.
> 14-
> 15-**Sprint v6.19.0 selado em 2026-06-01** — e2e-user-zero 2ª iteração + 3-stream sweep: framework de QA de esqueleto MVP → harness executável (`redactor` LGPD + `mesh-persistor` observation/OBSERVES idempotente + `telemetry` infra_health_logs + 6 dashboard flows + selftest 8 testes + pre-commit tripwire defesa Layer 4, hook versionado em `scripts/hooks/`). Stream A (consistência cross-node + Canvas 4.2) **VERIFICADO materialmente como já shipado** → zero retrabalho; único gap real fechado: `higgsfield-webhook` nsfw/canceled → razão clara de soft-fail. 2 smokes live (canvas pago + sql-bridge) gateados por `RUN_LIVE_SMOKE` → suíte **224 passed / 2 skipped / 0 failed**. Stream C flywheel readiness verde (orchestrate-content 200 · affiliate ativo · balance 5351), **gated em GO Sovereign**. Phase 5c **SEAL ALLOWED** (13 verified). Mesh **8747**. Survival Laws 4/4. 7 commits. **Lição:** o código está sistematicamente à frente dos Pending Actions — verificação material (Lei 1) antes de codar evita reconstruir features prontas.
> 16-
> 17-**Sprint v6.18.0 selado em 2026-06-01** — Constellation v2 cockpit LIVE (E2E): empty-state wizard 2-portas + execução real de capability (`watchdog_infra` → get-infra-status, done · 0 mco · 255ms) + Fase 0 reset destrutivo + botão Zerar per-user. 3 incidentes de produção resolvidos: build lucide quebrado (shim + anticorpo `audit-lucide-imports.ts`) · P0 login (publishable key stale no bundle → redeploy) · teste de chaves "Falhou" (descoberta da cripto de credenciais → edge fn `test-api-key` server-side). + Tabs em Settings. Mesh 8746/9070. Survival Laws 4/4. 8 commits.
> 18-
> 19-**Sprint v5.5.2 selado em 2026-05-04** — Social OAuth v1 + Pipeline History + WordPress multi-tenant + auto-publish pipeline corrigido + auditoria 4Cs 97/100.
> 20-
> 21-**Sprint v5.5.5 selado em 2026-05-05** — Settings Sovereignty: useUserApiKeys TanStack Query + pref_ai_model persistido + mcoCoins RPC atômico + Testar key client-side + Epsilon v9 hub badge + 2559 nós/3516 arestas.
> 22-
> 23-**Sprint v5.5.6 selado em 2026-05-06** — Core Promotion: CorePage v1 arquivada para `.archive/pages/`, `Core v2` promovida para `Core` no menu, `/dashboard/core` redireciona via Navigate. Gemini Live validado (VITE_GEMINI_API_KEY no `.env` + GEMINI_API_KEY no vault) — Pending Action #8 era falso positivo. 2560 nós · 100% embedded.
> 24-
> 25-**Sprint v5.6.0 selado em 2026-05-06** — DevOps + Security Seal: 6 branches mobile sincronizados + DOCUMENTATION_CREDENTIAL_RULE + pre-commit hook anti-credential + Gemini API key rotacionada + test coverage 0→66 testes (billing + store + phase-zeta) + BoK Scribe Agent (MRD/BRD/PRD/FRD/SDD templates) + MCORCH Master Execution Protocol em CLAUDE.md + /sync-mobile-branch protocol. 2561 nós · 100% embedded.
> 26-
> 27-**Sprint v5.6.1 selado em 2026-05-06** — Layout + UX Fixes: Matrix/Memory layout regression corrigida (absolute→relative), search bar inline nos badges, texto 100% opaco, MeshControl sincronizado com hook de grafo. 2564 nós · 100% embedded.
> 28-
> 29-**Sprint v5.7.0 selado em 2026-05-07** — BoK Suite v1 + A2UI Wiring + Test Coverage 122: parseAgentMessage conectado ao AIOSTerminal.onMessage (A2UI surfaces vivas em produção), 56 testes novos (66→122 — useOrchestrationGraph + useKnowledgeMesh + useSubscription), e família BoK completa de 9 docs (~29.185 palavras) reverse-engineered de 177 src files + 30 migrations + 39 edge functions + 4 crons. Mesh seal `bok-scribe-seal-mcorch-constellation-v1` (type `documentation_suite`, stability 0.85). 2567 nós · 100% embedded.
> 30-
> 31-**Sprint v5.9.0 selado em 2026-05-08** — FMEA-005 + LGPD Deploy: FMEA-005 (RPN 144) fechado com chunked embedding e vector averaging em `embed-mcorch-node`; LGPD (data-export + delete-account + delete_account() RPC) confirmada em produção; scratch/ removida. 7280 nós · 100% embedded.
> 32-
> 33-**Sprint v5.8.0 selado em 2026-05-08** — FMEA + BoK Phase 2 + 8-Agent System + LGPD: FMEA-008 (RPN 120) e FMEA-011 (RPN 100) fechados; BoK Suite enriquecida com voz estratégica (+227 linhas em 6 docs: Sovereign's Conviction, Business Philosophy, Por Que Vencemos, Validação com Criadores, Architectural Decisions, Quality Philosophy); `/bok-agents-generator` produziu `bok-agents-system--mcorch-constellation.md` (704 linhas · 8 agentes · 3 camadas cross-agent); LGPD DD-001+DD-002 implementados (delete_account() RPC + Edge Functions + hooks + SettingsPage modal). Phase Commercial desbloqueada. 7276 nós · 100% embedded.
> 34-
> 35-**Sprint v6.0.0 selado em 2026-05-14** — Conteúdo v2 BoK + VIRALmind Sprints 1-3 + ShakeHands v3: convergência de 3 streams paralelos. (1) BoK Conteúdo v2 selada (10 docs, 2276 linhas) com mesh seal `bok-scribe-seal-conteudo-v2-v1` (stability 0.85, R\$5.4M ARR Y2 projeção); (2) VIRALmind integrado via Antigravity — 4 migrations `vm_*` (trends/canvas/affiliate/niches) + 2 Edge Functions (`fetch-trends` Apify+RapidAPI, `canvas-execute` multi-provider OpenAI/Replicate/OpenRouter/Higgsfield) + 3 pages (Viral Miner, Canvas Studio, Canvas Editor) + 2 hooks (`useViralTrends`, `useCanvasStudio`); (3) ShakeHands v3 protocol — BoK Gate enforcement no /handson PRE-FLIGHT + BRIEF + /handoff Phase 5b mandatory check; (4) Feature gamificacao-mcoCoins-v1 mergeada (`mcoin_transactions` + `award_mco_coins` RPC + Circuit Breaker em opencode-bridge + memory hook integration). Conteúdo v2 BoK reconciliada com VIRALmind v1: v1=xyflow+vm_*, v2=tldraw+canvas-mcp reservado para Phase 7+8. 13 commits granulares. Sprint 4 (Canvas UX Mood Board completion) é o próximo deliverable.
> 36-
> --
> 86:## 🔴 Top Gap Closures (by leverage)
> 87-
> 88-1. ~~**Loop/rotina de cadência**~~ ✅ `audit-4cs.sh` toda segunda 09:00 BRT · `auto-publish-cron.sh` */5min · `watchdog` */5min
> 89-2. ~~**Primeiro run Usuário Zero**~~ ✅ Publicado em mcorch.com · LinkedIn + Twitter gerados · pipeline_runs persistido
> 90-3. ~~**`publish-social` realmente publicar**~~ ✅ Bug JWT corrigido · LinkedIn publicando · Twitter: CreditsDepleted (Free tier API X)
> 91-4. **Instagram App Review Meta** — verificação empresarial necessária para produção com terceiros → bloqueante para onboarding clientes (diferir até User 1)
> 92-5. **Twitter API tier upgrade** — Free tier esgotou créditos de escrita. Upgrade para Basic ($100/mês) desbloqueia publicação no X (diferir até User 1)
> 93-6. ~~**Consolidação N+1 queries**~~ ✅ issues #002/#003/#009 resolvidos (2026-05-04)
> 94-7. ~~**Settings Overhaul**~~ ✅ useUserApiKeys + pref_ai_model + mcoCoins RPC + Testar key + ConfigPanel real data (2026-05-05)
> 95-8. ~~**A2UI live em produção**~~ ✅ parseAgentMessage → AIOSTerminal.onMessage (2026-05-07) — surfaces dinâmicas spawnam automaticamente
> 96-9. ~~**Test coverage hooks críticos**~~ ✅ 66 → 122 testes (useOrchestrationGraph + useKnowledgeMesh + useSubscription) (2026-05-07)
> 97-10. ~~**BoK Scribe v1**~~ ✅ 9 docs · ~29k palavras · grounded em código real · selada na mesh (2026-05-07)
> 98-11. ~~**Phase 2 BoK enrichment**~~ ✅ 6 docs enriquecidos (+227 linhas voz estratégica) (2026-05-08)
> 99-12. ~~**Phase 3 BoK → Agents**~~ ✅ 8-agent system gerado (704 linhas) via /bok-agents-generator (2026-05-08)
> 100-13. ~~**Endurecer FMEA-008 + FMEA-011**~~ ✅ validateContent() em orchestrate-content + checklist obrigatório /migration (2026-05-08)
> 101-14. ~~**LGPD data export**~~ ✅ data-export Edge Function + useDataExport hook + UI (2026-05-08)
> 102-15. ~~**Self-service account deletion**~~ ✅ delete_account() RPC + delete-account Edge Function + useDeleteAccount + modal (2026-05-08)
> 103-16. ~~**FMEA-005** (RPN 144) — smart chunked embeddings~~ ✅ Selado 2026-05-08 — `splitChunks()` + batch API + `averageVectors()` · zero truncação silenciosa para nós grandes
> 104-17. ~~**Deploy para produção**~~ ✅ Confirmado 2026-05-08 — data-export + delete-account em produção · migration aplicada
> ```

## 🤖 Claude *(20:55:34)*


## 🤖 Claude *(20:55:59)*

Tenho todo o contexto necessário. O "Top Gap Closures" (linhas 86+) é histórico — itens ativos são só Instagram/Twitter (diferidos até User 1). O gap real da próxima sessão está na nota Pending do seal v6.20.3.

═══════════════════════════════════════════════════════════
  HANDSON — v6.20.3 · Disconnect RPC / Revogação de Segredo Órfão (2026-06-02)
═══════════════════════════════════════════════════════════

🏁 **ESTADO ATUAL**
  **Fase selada:** v6.20.3 — `disconnect_meta()`/`disconnect_social()` revogam o segredo Vault órfão (meta/social)
  **Últimos commits:**
    `844ebcf` — chore(sprint): update sprint-priorities v6.20.3
    `8338d8a` — docs(handoff): seal v6.20.3
    `ac1cba1` — docs(readme): v6.20.3
    `610e1f3` — docs(processes): SOP + Key Files do disconnect Meta/social
    `76bb9e3` — fix(credentials): disconnect_meta/disconnect_social revogam o segredo órfão

📂 **MUDANÇAS PENDENTES**
  Worktree limpo ✅ (`git status` e `git diff HEAD` vazios) · scratch/ limpo ✅

🏗️ **INFRA**
  `mcorch_chroma`:     Up 9 days (healthy) — Chroma API v2 **OK** (`heartbeat` respondeu)
  `mcorch_claude_mem`: Up 9 days (healthy)
  `mega-brain-daemon`: Up 9 days (healthy) · `mega-brain-webhook`: healthy · `mega-brain-dashboard`: up
  → 5/5 containers saudáveis

🧠 **KNOWLEDGE MESH**
  **8752 nós** · ~9070 arestas (count de arestas é snapshot 2026-06-01; v6.20.x só recontou nós) · 100% embedded (768d HNSW cosine)
  Handoff node desta seal: `f7805e20-bebd-4a30-8533-09806238f135` (embedded 768d)
  Tipos dominantes: handoff · milestone · architecture · decision · observation · documentation_suite + AST (file/function/interface/...)

🔧 **TYPESCRIPT**
  Zero erros ✅ (`tsc --noEmit` limpo)

📚 **BoK SUITES (MCORCH Master Execution Protocol)**
  **Sealed: 12/12 — todas completas (9 docs cada)** ✅
    aios-sql-bridge · canvas-design · constellation-v2 · conteudo-v2 · e2e-user-zero · gamificacao-nodes · mcorch-constellation · mcorch-qa-healing · mercado-livre-api · meta-api · openclaw · viralmind
  Incomplete: nenhum ✅ → **BoK Gate liberado para código novo em qualquer módulo**
  Mesh seal nodes (IDs materiais que constam no HANDOFF):
    viralmind → `5c4bf1e9` · gamificacao-nodes → `6e8546bc` · openclaw → `05c55dfd` · mcorch-qa-healing → `b00e938a` · aios-sql-bridge → `4e0acc7e` (todos stability 0.85)

📌 **SPRINT**
  **Goal:** Distribuição social autônoma operacional — pipeline publica LinkedIn automaticamente; Twitter desbloqueia ao subir API tier; Instagram após App Review Meta.
  **Top Gap ativo:** v6.20.3 **fechou** o gap de segredo órfão que a v6.20.2 sinalizou — e **não abriu** novo Top Gap de código. O resíduo é uma verificação visual (ver Próximos Passos #1). Gaps de longo prazo seguem diferidos até Usuário 1: Instagram App Review + Twitter Basic tier.

⚡ **PRÓXIMOS PASSOS (prioridade)**
  1. **E2E no navegador do disconnect Meta/social** — a revogação foi provada só pela ótica do banco (suíte RPC 5/5 em `BEGIN…ROLLBACK` + bundle servido contém `disconnect_meta`/`disconnect_social`). O clique real na UI logada (`/dashboard/settings` → Desconectar Meta/social) **não foi executado** (browser autenticado indisponível na seal). Confirmar visualmente.
  2. **Operador de Browser Autenticado (probe-first)** — iniciativa sinalizada na v6.20.0 para ações que nos barram server-side (ML Compartilhar → `meli.la`). Decisão registrada: PROBE-FIRST → runtime → `/bok-scribe` (BoK Gate) → build. *(memória `project_authenticated_browser_operator`)*
  3. **Canvas Studio Phase 4.2** — port dos 5 nós tipados + inspectors ricos + pipeline de vídeo Higgsfield async (gates DoP Standard já provados materialmente; smoke pago dispensado como gasto redundante).

⚠️ **ALERTAS**
  Nenhum alerta ✅ — TS limpo, worktree limpo, 5/5 containers healthy, Chroma v2 OK, 12/12 BoK completas.

═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

A base está selada e sem dívida bloqueante. O caminho natural é fechar a verificação visual do disconnect (#1, barata) ou destravar uma das iniciativas maiores (#2 Browser Operator / #3 Canvas 4.2). Qual direção, Maestro?

## 👤 User *(20:59:19)*

Vamos fechar o visual #1 depois vamos destravar o 2 e 3. É possivel fazer isso de uma vez só por aqui?

## 🤖 Claude *(21:00:22)*


## 🤖 Claude *(21:00:24)*

Boa — antes de responder "dá ou não dá de uma vez", deixa eu checar materialmente as mãos que tenho (Lei 1). O ponto-chave: **#1 e #2 dependem do mesmo recurso — um browser autenticado rodando deste ambiente**. Vou sondar o estado real antes de prometer qualquer coisa.

## 🤖 Claude *(21:00:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== agent-browser bin\u00e1rio ===\"; which agent-browser 2>/dev/null && agent-browser --version 2>&1 | head -3 || echo \"N\u00c3O no PATH\"\necho \"\"\necho \"=== npx agent-browser ===\"; timeout 20 npx -y agent-browser --version 2>&1 | tail -3 || echo \"npx falhou/timeout\"",
  "description": "Probe agent-browser availability"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === agent-browser binário ===
> /home/ubuntu/.nvm/versions/node/v22.22.3/bin/agent-browser
> agent-browser 0.27.0
> 
> === npx agent-browser ===
> agent-browser 0.27.0
> ```

## 🤖 Claude *(21:00:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== BoK do browser operator (espera-se AUSENTE) ===\"; ls docs/bok/ | grep -iE \"browser|operator|operador\" || echo \"\u2705 confirmado: nenhuma BoK suite de browser-operator (BoK Gate fechado p/ #2)\"\necho \"\"\necho \"=== profiles de browser persistidos ===\"\nfor d in ~/.agent-browser ~/.config/agent-browser ~/.cache/ms-playwright \"$HOME/.mozilla\" /home/ubuntu/.agent-browser; do\n  [ -e \"$d\" ] && echo \"EXISTE: $d ($(du -sh \"$d\" 2>/dev/null | cut -f1))\" || echo \"ausente: $d\"\ndone",
  "description": "Confirm BoK gate + check browser profiles"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === BoK do browser operator (espera-se AUSENTE) ===
> ✅ confirmado: nenhuma BoK suite de browser-operator (BoK Gate fechado p/ #2)
> 
> === profiles de browser persistidos ===
> EXISTE: /home/ubuntu/.agent-browser (8.0K)
> ausente: /home/ubuntu/.config/agent-browser
> EXISTE: /home/ubuntu/.cache/ms-playwright (2.0G)
> ausente: /home/ubuntu/.mozilla
> EXISTE: /home/ubuntu/.agent-browser (8.0K)
> ```

> **Tool Result (Unknown Tool)** - ✅ Success
>
> ```
> === SOP agent-browser-install (head) ===
> # SOP — agent-browser CLI Install & Smoke Test
> 
> > **Survival Law 2 (Anticipated Process) anchor.** This SOP documents the human-equivalent procedure that the AI must mirror when (re)installing or verifying the [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) CLI on a MCORCH host. It is the prerequisite SOP behind any AI-driven E2E "Usuário Zero" run that uses agent-browser instead of (or alongside) the existing Playwright-based `scripts/qa/audit-canvas-ui.ts`.
> >
> > Status: Sealed v6.8.4 — 2026-05-25.
> 
> ---
> 
> ## Why this exists
> 
> The existing E2E gate enforced by Survival Law 1 (`scripts/qa/audit-canvas-ui.ts`) is a Playwright script tightly coupled to the Canvas Studio surface (1920×1080, 22-node assertion, hardcoded selectors). The Vercel Labs `agent-browser` CLI gives the AI a generic, snapshot-and-ref browser primitive that lets it explore *any* surface (landing page, dashboard, orchestrator canvas, settings, billing flow) on demand — closer to how a real Usuário Zero would dogfood the product. The `dogfood` skill bundled with the CLI captures that exploratory testing workflow verbatim.
> 
> This SOP keeps the install reproducible so we can rebuild the environment on any other MCORCH host (laptop, VM, sandbox) without rediscovering the steps.
> 
> ---
> 
> ## Operator
> 
> Default: **Sovereign (Gabriel Zarattini)** running on the host where the AI executes (`ubuntu` user under `/home/ubuntu/.nvm`). Secondary: any L1/L2 agent with shell access for a verification check.
> 
> The AI is allowed to run the verification steps unattended (read-only). The AI is **not** allowed to invoke `npm install -g` or `agent-browser install` without an explicit Sovereign green light — those touch the global node_modules and download a Chromium payload.
> 
> ---
> 
> ## Sequence
> 
> ### Step 1 — Pre-flight: detect existing install
> 
> ```bash
> command -v agent-browser && agent-browser --version
> ls -la $(command -v agent-browser) 2>/dev/null
> ```
> 
> **Expected success output:**
> 
> ```
> /home/ubuntu/.nvm/versions/node/v22.22.3/bin/agent-browser
> agent-browser 0.27.0
> lrwxrwxrwx ... -> .../lib/node_modules/agent-browser/bin/agent-browser-linux-arm64
> ```
> ```

## 🤖 Claude *(21:00:31)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== SOP agent-browser-install (head) ===\"; sed -n '1,40p' docs/processes/agent-browser-install.md 2>/dev/null || echo \"SOP ausente\"",
  "description": "Read agent-browser install SOP head"
}
```

## 🤖 Claude *(21:02:26)*


## 🤖 Claude *(21:02:30)*

Probe material confirmado:
- **agent-browser 0.27.0** instalado ✅ + Chromium Playwright (2.0 GB) presente ✅ — tenho o driver.
- **Sem sessão autenticada persistida** — `/home/ubuntu/.agent-browser` é só 8 KB (config, não um profile logado com cookies).
- **BoK Gate do #2 fechado** ✅ — não existe `docs/bok/*browser-operator*` (módulo novo exige `/bok-scribe` antes de código).
- SOP permite eu rodar verificação **read-only** não-supervisionada; `install` exige luz verde sua.

Deixa eu fazer um smoke read-only (não loga, não desconecta nada) pra provar que o driver abre a NOSSA app deste datacenter — isso desarma o "logado não-testado" pelo lado do driver. Primeiro a sintaxe:

## 🤖 Claude *(21:02:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "agent-browser --help 2>&1 | head -60",
  "description": "agent-browser CLI usage"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> agent-browser - fast browser automation CLI for AI agents
> 
> Usage: agent-browser <command> [args] [options]
> 
> Start here (for AI agents):
>   agent-browser skills get core --full
> 
>   Skills ship with the CLI (always version-matched) and include workflow
>   patterns, ref/selector usage, and copy-paste examples. Prefer this over
>   guessing commands from flag docs alone. Specialized skills cover Electron
>   apps, Slack, exploratory testing, and cloud browser providers.
> 
>   skills [list]                List available skills
>   skills get core              Core usage guide (overview + common patterns)
>   skills get core --full       Include full command reference and templates
>   skills get <name>            Load a specialized skill (electron, slack, ...)
>   skills path [name]           Print skill directory path
> 
> Core Commands:
>   open <url>                 Navigate to URL
>   click <sel>                Click element (or @ref)
>   dblclick <sel>             Double-click element
>   type <sel> <text>          Type into element
>   fill <sel> <text>          Clear and fill
>   press <key>                Press key (Enter, Tab, Control+a)
>   keyboard type <text>       Type text with real keystrokes (no selector)
>   keyboard inserttext <text> Insert text without key events
>   hover <sel>                Hover element
>   focus <sel>                Focus element
>   check <sel>                Check checkbox
>   uncheck <sel>              Uncheck checkbox
>   select <sel> <val...>      Select dropdown option
>   drag <src> <dst>           Drag and drop
>   upload <sel> <files...>    Upload files
>   download <sel> <path>      Download file by clicking element
>   scroll <dir> [px]          Scroll (up/down/left/right)
>   scrollintoview <sel>       Scroll element into view
>   wait <sel|ms>              Wait for element or time
>   screenshot [path]          Take screenshot
>   pdf <path>                 Save as PDF
>   snapshot                   Accessibility tree with refs (for AI)
>   eval <js>                  Run JavaScript
>   connect <port|url>         Connect to browser via CDP
>   close [--all]              Close browser (--all closes every session)
> 
> Navigation:
>   back                       Go back
>   forward                    Go forward
>   reload                     Reload page
> 
> Get Info:  agent-browser get <what> [selector]
>   text, html, value, attr <name>, title, url, count, box, styles, cdp-url
> 
> Check State:  agent-browser is <what> <selector>
>   visible, enabled, checked
> 
> Find Elements:  agent-browser find <locator> <value> <action> [text]
>   role, text, label, placeholder, alt, title, testid, first, last, nth
> ```

## 🤖 Claude *(21:02:40)*


## 🤖 Claude *(21:02:41)*

Sintaxe entendida. Smoke read-only contra a nossa app (não loga, não toca em nada — só navega e fotografa a tela de login):

## 🤖 Claude *(21:02:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== open ===\"; timeout 120 agent-browser open https://login.mcorch.com 2>&1 | tail -8\necho \"=== url ===\"; timeout 20 agent-browser get url 2>&1 | tail -2\necho \"=== title ===\"; timeout 20 agent-browser get title 2>&1 | tail -2\necho \"=== screenshot ===\"; timeout 30 agent-browser screenshot /tmp/mcorch-login-smoke.png 2>&1 | tail -3\nls -la /tmp/mcorch-login-smoke.png 2>/dev/null && echo \"BYTES_OK\" || echo \"NO_SCREENSHOT\"",
  "description": "Read-only smoke: open login.mcorch.com + screenshot"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === open ===
> ✓ MCORCH · Sovereign Intelligence · Pare de ser variável.
>   https://login.mcorch.com/
> === url ===
> https://login.mcorch.com/
> === title ===
> MCORCH · Sovereign Intelligence · Pare de ser variável.
> === screenshot ===
> ✓ Screenshot saved to /tmp/mcorch-login-smoke.png
> -rw-rw-r-- 1 ubuntu ubuntu 113870 Jun  2 18:02 /tmp/mcorch-login-smoke.png
> BYTES_OK
> ```

## 🤖 Claude *(21:02:55)*


## 🤖 Claude *(21:02:56)*

Smoke verde — driver funciona deste datacenter contra a nossa app (o bloqueio de IP da memória era específico do ML, não da `login.mcorch.com`). Deixa eu confirmar visualmente que renderizou a UI real (não tela branca):

## 🤖 Claude *(21:02:56)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/mcorch-login-smoke.png"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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', 'media_type': 'image/png'}}]
> ```

## 🤖 Claude *(21:04:55)*


## 🤖 Claude *(21:05:09)*

Tela real renderizada (113 KB) — é a landing pública do MCORCH. **O driver funciona deste datacenter contra a nossa app.** O "logado não-testado / IP bloqueado" da memória era específico do Mercado Livre, não da `login.mcorch.com`.

Com isso, o veredito material:

## Dá pra encadear numa sessão — mas não os três "de uma vez". Eis o porquê

Os três têm **gates diferentes**, e dois deles convergem na mesma ferramenta:

| | O que falta de fato | Gate | Cabe nesta sessão? |
|---|---|---|---|
| **#1** disconnect visual | Ver a UI **logada** renderizar o controle de Desconectar (o resto — RPC 5/5 + bundle servido — já está provado) | **Sua sessão** em login.mcorch.com (não há profile persistido; sem senha crua pra mim) | ✅ Sim — terreno fácil, driver já provado |
| **#2** Browser Operator | Decidir o **runtime** via probe: *o agent-browser logado passa pelo bloqueio de IP do ML deste datacenter?* | **Probe-first** (read-only, permitido) → só depois **`/bok-scribe`** (BoK Gate fechado — confirmei: não há `docs/bok/*browser-operator*`) → build | ⚠️ Probe sim; **build não** (módulo novo = BoK antes de código) |
| **#3** Canvas 4.2 | Port de 5 nós + inspectors + pipeline vídeo async | Trabalho grande, **ortogonal** a #1/#2 | ❌ Sessão dedicada (empacotar viola Lei 3 / Pruning) |

**O elo real entre #1 e #2 é a ferramenta, não o alvo:** ambos usam `agent-browser` + uma sessão injetada. O #1 exercita isso contra a **nossa app** (fácil); o #2 contra o **ML logado** (hostil, IP de datacenter historicamente barrado). Então fazer #1 valida o fluxo logado — degrau útil — mas o **veredito do #2 depende especificamente do probe do ML**, que é o gargalo real.

**Plano que respeita os gates, numa sessão:**
1. **Bloco A — #1:** sua sessão → navego `/dashboard/settings` logado → verifico o controle de Desconectar → screenshot. Fecha o resíduo da seal v6.20.3.
2. **Bloco B — probe do #2:** com sessão do ML, testo *read-only* se passo do bloqueio de IP. O resultado decide o runtime (este datacenter / proxy residencial / sua máquina / Vercel Sandbox) → aí rodo `/bok-scribe authenticated-browser-operator` pra abrir o BoK Gate. **Build do módulo = próxima sessão.**
3. **Bloco C — #3 Canvas:** sessão dedicada.

Para destravar o **Bloco A agora**, preciso de duas decisões suas (são genuinamente suas — auth e ação destrutiva):

## 🤖 Claude *(21:05:18)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "N\u00e3o h\u00e1 sess\u00e3o autenticada persistida e eu n\u00e3o devo manusear sua senha crua. Como prover a sess\u00e3o de login.mcorch.com pro agent-browser dirigir o #1? (a escolha vira o molde reutiliz\u00e1vel pro probe do ML no #2)",
      "header": "Sess\u00e3o logada",
      "multiSelect": false,
      "options": [
        {
          "label": "Token Supabase do localStorage",
          "description": "Voc\u00ea cola o `sb-<project>-auth-token` do localStorage do seu navegador (DevTools \u2192 Application). Eu injeto via `agent-browser eval` e fico logado como Usu\u00e1rio Zero. Sem senha crua, sess\u00e3o real. Exercita a ferramenta logada que o #2 vai precisar."
        },
        {
          "label": "Voc\u00ea dirige o #1",
          "description": "Voc\u00ea abre /dashboard/settings na sua m\u00e1quina, observa o controle de Desconectar (e clica, se autorizar), cola o screenshot. Fecha #1 em ~2min, mas n\u00e3o exercita o agent-browser logado \u2014 n\u00e3o adianta o #2."
        },
        {
          "label": "Login assistido via CDP",
          "description": "Eu exponho o Chromium via CDP/t\u00fanel e voc\u00ea digita as credenciais ao vivo. Mais setup, mas voc\u00ea n\u00e3o exp\u00f5e nenhum token a mim."
        }
      ]
    },
    {
      "question": "Clicar 'Desconectar Meta/social' revoga a credencial REAL do Usu\u00e1rio Zero (reconex\u00e3o depois \u00e9 via OAuth). Qual profundidade de verifica\u00e7\u00e3o?",
      "header": "Profundidade #1",
      "multiSelect": false,
      "options": [
        {
          "label": "N\u00e3o-destrutivo (s\u00f3 renderiza\u00e7\u00e3o)",
          "description": "Logado, confirmo que /dashboard/settings mostra o estado conectado + o bot\u00e3o Desconectar presente e habilitado, sem clicar. Fecha o gap real (UI logada renderiza o controle) \u2014 o clique\u2192RPC j\u00e1 est\u00e1 provado por banco. Zero revoga\u00e7\u00e3o."
        },
        {
          "label": "Disconnect real end-to-end",
          "description": "Clico Desconectar de fato, capturo a chamada `disconnect_meta`/`disconnect_social` no network + a UI virando 'desconectado' + o segredo Vault sumindo. Prova completa, mas voc\u00ea reconecta a conta depois."
        },
        {
          "label": "Conta de teste/secund\u00e1ria",
          "description": "Se voc\u00ea tiver uma conta Meta/social descart\u00e1vel, desconecto nela \u2014 destrutivo mas sem afetar o Usu\u00e1rio Zero."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "Não há sessão autenticada persistida e eu não devo manusear sua senha crua. Como prover a sessão de login.mcorch.com pro agent-browser dirigir o #1? (a escolha vira o molde reutilizável pro probe do ML no #2)"="Pensando em que isso deveria ser usado per user no ecossistema, qual seria a melhor opção? Criar uma autenticação real com o login do cliente? Igual quando fazemos login com as redes sociais ou até mesmo com o google para criar conta no MCORCH, onde os usuários logariam com suas contas da mercado livre, dando concentimento de que o agente poderá usar para compartilhar os links de produtos afiliados.", "Clicar 'Desconectar Meta/social' revoga a credencial REAL do Usuário Zero (reconexão depois é via OAuth). Qual profundidade de verificação?"="Disconnect real end-to-end". You can now continue with these answers in mind.
> ```

## 🤖 Claude *(21:18:21)*


## 🤖 Claude *(21:18:23)*

Sua resposta na P1 muda o jogo — você não escolheu um mecanismo, você elevou a pergunta certa: **"qual o modelo per-user do ecossistema?"**. Antes de teorizar, deixa eu ancorar no que já existe materialmente no código (Lei 1 — não responder arquitetura de cabeça):

## 🤖 Claude *(21:18:27)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== Edge functions relacionadas a ML/afiliado/oauth ===\"\nls supabase/functions/ | grep -iE \"affiliate|meli|mercado|oauth|ml-\" || echo \"(nenhuma com esses nomes)\"\necho \"\"\necho \"=== Fluxos OAuth existentes (social) como refer\u00eancia de padr\u00e3o ===\"\nls supabase/functions/ | grep -iE \"linkedin|twitter|instagram|meta|social|oauth\" || echo \"(nenhuma)\"",
  "description": "List ML + OAuth-related edge functions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === Edge functions relacionadas a ML/afiliado/oauth ===
> handle-ml-postback
> process-affiliate-link
> 
> === Fluxos OAuth existentes (social) como referência de padrão ===
> instagram-webhook
> publish-meta
> publish-social
> refresh-social-token
> social-auth-callback
> social-auth-init
> sync-meta-ads
> ```

## 🤖 Claude *(21:18:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== affiliate_config: como \u00e9 populado? OAuth flow ou input manual? ===\"\ngrep -rInE \"affiliate_config\" supabase/migrations/ src/ supabase/functions/ 2>/dev/null | grep -iE \"oauth|access_token|refresh_token|authorize|grant|app_id|client_secret|redirect_uri\" | head -20\necho \"\"\necho \"=== Mercado Livre API endpoints chamados no c\u00f3digo ===\"\ngrep -rInE \"api\\.mercadol|auth\\.mercadol|mercadolibre\\.com|mercadolivre\\.com|meli\\.la\" supabase/functions/ src/ scripts/ 2>/dev/null | grep -iE \"https?://|fetch|auth/token|/oauth\" | head -20",
  "description": "Probe affiliate_config population + ML API calls"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === affiliate_config: como é populado? OAuth flow ou input manual? ===
> 
> === Mercado Livre API endpoints chamados no código ===
> supabase/functions/process-affiliate-link/index.ts:11:const ML_SEARCH_BASE = "https://api.mercadolibre.com/sites/MLB/search";
> supabase/functions/process-affiliate-link/index.ts:47:const ML_PRODUCT_BASE = "https://www.mercadolivre.com.br";
> src/lib/affiliate.ts:17:export const ML_PRODUCT_BASE = "https://www.mercadolivre.com.br";
> src/lib/affiliate.ts:33:  /** Verified product URL (preferred base, e.g. https://www.mercadolivre.com.br/p/MLB27834876). */
> src/lib/affiliate.test.ts:11:    expect(isMlShortLink("https://meli.la/2gh13Sw")).toBe(true);
> src/lib/affiliate.test.ts:12:    expect(isMlShortLink("https://www.mercadolivre.com.br/sec/abc123")).toBe(true);
> src/lib/affiliate.test.ts:13:    expect(isMlShortLink("https://mercadolivre.com/sec/abc123")).toBe(true);
> src/lib/affiliate.test.ts:17:    expect(isMlShortLink("https://www.mercadolivre.com.br/p/MLB27834876")).toBe(false);
> src/lib/affiliate.test.ts:28:      productUrl: "https://www.mercadolivre.com.br/p/MLB27834876",
> src/lib/affiliate.test.ts:33:    expect(u.origin + u.pathname).toBe("https://www.mercadolivre.com.br/p/MLB27834876");
> src/lib/affiliate.test.ts:41:      productUrl: "https://www.mercadolivre.com.br/p/MLB27834876",
> src/lib/affiliate.test.ts:52:      "https://www.mercadolivre.com.br/MLB-27834876?matt_word=caga6077534" +
> src/lib/affiliate.test.ts:67:    productUrl: "https://www.mercadolivre.com.br/p/MLB27834876",
> src/lib/affiliate.test.ts:74:      shortlinks: { MLB27834876: "https://meli.la/2gh13Sw" },
> src/lib/affiliate.test.ts:76:    expect(r).toEqual({ kind: "shortlink", url: "https://meli.la/2gh13Sw" });
> src/lib/affiliate.test.ts:102:      shortlinks: { MLB27834876: "https://meli.la/2gh13Sw" },
> src/lib/affiliate.test.ts:104:    expect(r).toEqual({ kind: "shortlink", url: "https://meli.la/2gh13Sw" });
> src/lib/affiliate.test.ts:117:      readShortlinks({ shortlinks: { MLB1: "https://meli.la/a", MLB2: "  ", MLB3: 42 } }),
> src/lib/affiliate.test.ts:118:    ).toEqual({ MLB1: "https://meli.la/a" });
> src/pages/AffiliateProductsPage.tsx:189:            placeholder="https://meli.la/2gh13Sw"
> ```

## 🤖 Claude *(21:21:26)*


## 🤖 Claude *(21:21:26)*

Achado material (não é teoria — é o que está no código agora):

## 🤖 Claude *(21:21:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== social-auth-init: \u00e9 o padr\u00e3o OAuth 'login com consentimento'? ===\"\nsed -n '1,60p' supabase/functions/social-auth-init/index.ts 2>/dev/null | grep -inE \"platform|oauth|authorize|scope|redirect|linkedin|twitter|instagram|switch|case\" | head -25",
  "description": "Inspect social-auth-init OAuth pattern"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === social-auth-init: é o padrão OAuth 'login com consentimento'? ===
> 6:  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-user-token, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version",
> 9:const LINKEDIN_AUTH_URL = "https://www.linkedin.com/oauth/v2/authorization";
> 10:const INSTAGRAM_AUTH_URL = "https://api.instagram.com/oauth/authorize";
> 11:const TWITTER_AUTH_URL = "https://twitter.com/i/oauth2/authorize";
> 21:      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 35:      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 42:    const { platform, redirect_uri } = await req.json();
> 44:    if (!platform || !redirect_uri) {
> 45:      return new Response(JSON.stringify({ error: "platform and redirect_uri required" }), {
> 52:    const state = btoa(JSON.stringify({ userId, platform, redirect_uri }));
> 56:    if (platform === "linkedin") {
> 57:      const clientId = Deno.env.get("LINKEDIN_CLIENT_ID");
> 59:        return new Response(JSON.stringify({ error: "LinkedIn not configured" }), {
> ```

## 🤖 Claude *(21:21:39)*


## 🤖 Claude *(21:22:03)*

Material confirmado. Agora posso responder sua pergunta com autoridade, não de cabeça.

## O que existe hoje (provado no código)

| Fato material | Evidência |
|---|---|
| **O padrão "login social + consentimento" já existe e é robusto** | `social-auth-init` gera a URL de `authorization` (LinkedIn/Instagram/Twitter) com `state` carregando `userId+platform+redirect_uri`; `social-auth-callback` troca o code por token; `refresh-social-token` renova. É **exatamente** o molde que você descreveu. |
| **O Mercado Livre NÃO está nesse fluxo** | O `switch` de plataformas só tem `linkedin`/`instagram`/`twitter`. Não há `ml-auth-init`/`ml-auth-callback`. |
| **`affiliate_config` já é per-user e já guarda credenciais OAuth** | CLAUDE.md API Tenancy: `affiliate_config` tem `app_id · client_secret · redirect_uri` (UNIQUE por `user_id+platform`) — a infra de OAuth do ML está **meio-construída**, mas hoje é preenchida à mão. |
| **O `meli.la` hoje é manual** | `AffiliateProductsPage` tem um input pra você **colar** `https://meli.la/...`; o resolver usa `affiliate_config.metadata.shortlinks` ou cai no fallback `?matt_word=`. Nenhum código gera o shortlink automaticamente. |

## A distinção que decide o #2 inteiro

Sua intuição ("OAuth igual social login") está **certa como princípio** e é o caminho per-user correto. Mas há uma bifurcação técnica que muda tudo, e é empírica:

> **OAuth te dá um _API token_ — opera a API REST do ML server-side.**
> **Um Browser Operator te dá uma _sessão de cookies_ — opera a UI web logada do ML.**
> **São coisas diferentes.**

O #2 (Browser Operator) só nasceu porque presumimos que o `meli.la` **só** sai do botão "Compartilhar" da UI logada. **Se isso for falso** — se a API oficial de afiliados do ML, com um token OAuth per-user, devolver o link/shortlink — então:

- ✅ Você espelha o `social-auth-init/callback` que já tem → cria `ml-auth-*` → o agente gera links **via API, server-side, per-user, com consentimento OAuth**.
- ✅ **O Browser Operator (#2) deixa de ser necessário.** Sem Chromium, sem cookies que expiram, sem fragilidade de scraping, sem o problema de IP de datacenter. Essa é de longe a melhor notícia possível para o ecossistema.

Se for verdade (só a UI gera o `meli.la`), aí sim o #2 se justifica — e o "login com consentimento" teria que capturar a **sessão de navegador** do cliente (cookies), não um API token. Mais delicado (LGPD de sessão, expiração, segurança).

**A melhor opção, então:** OAuth oficial do ML per-user (espelhando o que já temos pro social). Mas isso é uma hipótese a **provar com um probe** antes de cravar — e era exatamente o "probe-first" que a decisão do #2 já mandava. Agora o probe tem alvo preciso: *a Affiliates/Marketplace API do ML, autenticada via OAuth, devolve o link de afiliação per-user? E o bloqueio de IP que vimos some sob tráfego OAuth legítimo?*

Documentar/`bok-scribe` o "Browser Operator" **antes** desse probe seria construir no escuro — e potencialmente um módulo inteiro que o OAuth torna obsoleto.

## Correção de rumo (erro meu)

Eu liguei as duas autenticações dizendo "molde reutilizável" — **estava errado e te induzi à conflação**. A auth do **#1** é só logar na **nossa app** como Usuário Zero (não tem nada a ver com ML/OAuth). A auth do **#2** é o cliente autorizar o MCORCH no **ML dele**. São desacopladas.

## Plano revisado

1. **#1 agora** — fechar o disconnect Meta/social end-to-end (você confirmou). Auth = só sua sessão na nossa app.
2. **Probe do #2 a seguir** — provar se a API oficial de afiliados ML (OAuth) entrega o link/shortlink. **O resultado decide** se #2 é "implementar `ml-auth` OAuth" (ótimo) ou "Browser Operator" (último recurso). Só depois do probe → `/bok-scribe`.
3. **#3 Canvas 4.2** — sessão dedicada.

Para destravar o **#1**, só preciso de uma coisa sua (a auth da nossa app, trivial e desacoplada do ML):

## 🤖 Claude *(21:22:13)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "Pra fechar o #1 (disconnect Meta/social real end-to-end) eu preciso operar a NOSSA app logado como Usu\u00e1rio Zero \u2014 isso \u00e9 s\u00f3 a sua sess\u00e3o em login.mcorch.com, sem rela\u00e7\u00e3o com OAuth do ML. Qual mec\u00e2nica voc\u00ea prefere?",
      "header": "Mec\u00e2nica #1",
      "multiSelect": false,
      "options": [
        {
          "label": "Token de sess\u00e3o \u2192 eu fecho 100% por aqui",
          "description": "Voc\u00ea cola o `sb-bcyvddsykvehvpwstlfa-auth-token` do localStorage (DevTools \u2192 Application). Eu injeto no agent-browser, clico Desconectar, e capturo a prova completa: chamada `disconnect_meta`/`disconnect_social` no network + UI virando 'desconectado' + segredo Vault revogado. \u00c9 token de sess\u00e3o (sua conta, revog\u00e1vel com logout) \u2014 n\u00e3o senha."
        },
        {
          "label": "H\u00edbrido: voc\u00ea clica, eu provo no banco",
          "description": "Voc\u00ea abre /dashboard/settings e clica Desconectar (~2min, zero token exposto a mim). Em paralelo eu provo o antes/depois materialmente via REST + Management API: linha meta_config/social_accounts limpa + segredo Vault sumindo. Verifica\u00e7\u00e3o visual (sua) + prova de banco (minha)."
        },
        {
          "label": "Conta de teste descart\u00e1vel",
          "description": "Se voc\u00ea tiver uma conta Meta/social secund\u00e1ria, fa\u00e7o o end-to-end nela e o Usu\u00e1rio Zero fica intacto (n\u00e3o precisa reconectar nada depois)."
        }
      ]
    }
  ]
}
```

---

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-02 - Add tenant guard to credential encryption triggers]]
> * **Próxima Sessão**: [[2026-06-02 - Fix WordPress credentials save and disconnect in SocialAccountsPage]]
%% --- TIMELINE END --- %%

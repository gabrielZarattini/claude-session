# SOP — Resolução per-user de credenciais de Trends (Apify / RapidAPI)

> **Slug:** `trends-credential-resolution` · **Criado:** 2026-06-22 · **Lei 2 (Processo Antecipado)** · **API Tenancy Model**
> **Origem:** diretiva Sovereign 2026-06-22 — *"tudo que é per-user sempre é prioridade ser resolvido per-user"*. Fecha o item **#3** da auditoria de prontidão per-user (`fetch-trends` era a última violação user-facing: `APIFY_TOKENS`/`RAPIDAPI_KEY` resolvidos do env global num fluxo iniciado por JWT).

## Problema

`supabase/functions/fetch-trends/index.ts` resolve `Deno.env.get("APIFY_TOKENS")` (`:54`) e `Deno.env.get("RAPIDAPI_KEY")` (`:109`) — chaves **globais** — num fluxo **user-facing** (`getUser` + 401). Viola o API Tenancy Model (atribuição/quota/risco não isolados por tenant; um tenant esgota a quota de scraping global).

## Modelo da solução (per-user puro, fail-closed)

- `fetch-trends` resolve **per-user**: `decrypted_user_api_keys.apify_token` (coluna **já existe**) + `decrypted_user_api_keys.rapidapi_key` (**coluna nova**). **Sem fallback de env** (env = só infra). Sem chave → `402 {error:"trends_not_configured", action:"Configure sua chave Apify/RapidAPI em /dashboard/settings"}` + telemetria.
- **Exceção legítima registrada:** os scripts cron/sistema `scripts/enrich-affiliate-products.ts` / `discover-affiliate-products.ts` rodam do `.env` local em contexto **system/cron** (sem `auth.uid()`) → continuam usando `APIFY_TOKENS` (documentado, não é fluxo user-facing). `vm_trends`/`vm_affiliate_products` são caches globais por design; a credencial é que vira per-user.

## ORO

- **Operator:** MCORCH Master Execution Agent (migration + edge fn + UI) + Tenant (configura a própria chave Apify/RapidAPI).
- **Reviewer:** `/security-review` (migration) + Sovereign.
- **Owner:** Sovereign — blast radius = quota de scraping per-tenant + isolamento.

## Sequence (cada step com critério material)

1. **Migration `rapidapi_key`** — adiciona a coluna ao maquinário cifrado do `user_api_keys` espelhando **verbatim** o último live def (`20260615140000_user_api_keys_firecrawl_channel.sql`): base column + encrypt trigger (`vault_upsert_secret` idempotente) + masked view (`••••`) + INSTEAD OF (UPDATE-first + tenant guard `auth.uid()`) + decrypted view (service-role + JOIN vault). `apify_token` já existe — só `rapidapi_key` é novo. **`/security-review` obrigatório.** Sucesso: `db push` exit 0 · `SELECT rapidapi_key FROM user_api_keys` = `••••`/null · write cross-tenant → 42501.
2. **fetch-trends per-user** — `userKeys?.apify_token` / `userKeys?.rapidapi_key` (service-role read de `decrypted_user_api_keys` por `user.id`), fail-closed 402, telemetria `infra_health_logs service='fetch-trends'`. Sucesso: deploy + 402 quando sem chave.
3. **Seed do Usuário Zero** — popula `apify_token`/`rapidapi_key` per-user a partir do `.env` (BYOK do tenant-zero, como User 1 faria). Sucesso: masked = `••••` + match de comprimento.
4. **UI** — inputs Apify/RapidAPI em Settings (hook `useUserApiKeys`). Sucesso: render + persiste cifrado.

## Verification gates

| Gate | Esperado |
|---|---|
| Coluna cifrada | `rapidapi_key` = `••••`/null no masked view; valor real só em `decrypted_user_api_keys` (service-role) |
| Tenant guard | write per JWT de outro tenant → `42501` |
| fail-closed | tenant sem chave → `402 trends_not_configured` |
| per-user resolve | tenant com chave → fetch-trends usa a chave dele (não env) |

## Recovery path

- **402 com chave setada:** confira `apify_token`/`rapidapi_key` no `.select()` do decrypted view + `user.id` correto.
- **23505 ao salvar:** trigger de encrypt não-idempotente → garantir `vault_upsert_secret` (já é o padrão).
- **Rollback:** edge fn volta ao env? **Não** — env removido por design; rollback = re-adicionar fallback só em emergência documentada (OTD).

## Success signal

Um tenant com a própria chave Apify configurada dispara `fetch-trends` e recebe trends populados em `vm_trends` usando **a chave dele** (quota isolada), sem nenhuma chave global ter sido tocada.

## Referências
- Template de coluna cifrada: `supabase/migrations/20260615140000_user_api_keys_firecrawl_channel.sql`
- API Tenancy Model (CLAUDE.md) · `feedback_api_tenancy_per_user`
- Auditoria per-user 2026-06-22 (#3) · edge fn alvo `supabase/functions/fetch-trends/index.ts`

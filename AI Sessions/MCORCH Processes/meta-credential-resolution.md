# SOP: Meta Credential Resolution (Per-User)

**Status:** ACTIVE · v1.0 · 2026-05-30
**Owner:** Sovereign (Gabriel Zarattini)
**Survival Law 2 compliance:** Escrita ANTES do código de `supabase/functions/publish-meta/index.ts` + migration `meta_config` (requisito explícito da diretiva API Tenancy item 5).
**Canonical directive:** `CLAUDE.md > Architecture > "API Tenancy Model — Per-User Credentials"`
**BoK SSOT:** `docs/bok/meta-api/` (FR-META-002 · FR-META-003 · FR-META-008 · FR-META-009 · NFR-META-001/002 · PROC-META-002)

---

## Context

A publicação omnichannel na Meta (Instagram Business + Facebook Page) exige um **long-lived user token** (60 dias) e tokens de página/IG derivados, escopados **por tenant**. A natureza da Meta é per-usuário: cada criador conecta a sua própria conta. Não existe — e não pode existir — credencial Meta global compartilhada em fluxo user-facing (vazaria controle total de páginas de terceiros + atribuição de receita errada).

`publish-meta` é invocada pelo `PublishNode` do pipeline de orquestração (PROC-META-002). Ela DEVE resolver as credenciais de `meta_config` filtrando por `user_id` do **dono do conteúdo**, nunca de um env global.

**Por que importa (multi-tenant readiness):** controle de páginas isolado por tenant · atribuição de receita correta · LGPD (cada user controla/revoga sua credencial Meta) · anti-fraude (um user não publica pela conta de outro) · blast radius de credencial roubada confinado a um tenant.

---

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (build) + Edge runtime `publish-meta` (execução)
- **Reviewer:** Sovereign (Gabriel) — aprova migration via `/security-review` + valida o smoke
- **Owner:** Sovereign — blast radius = controle de páginas Meta por tenant + atribuição de receita + tokens OAuth perpétuos

---

## Operator (quem executa manualmente hoje)

- **Usuário Zero / cliente:** configura suas credenciais Meta em `/dashboard/settings` (card "Meta Integration", hook `useMetaConfig` → upsert `meta_config` com `long_lived_token` + `instagram_business_account_id` + `pages[]`). Modelo BYOK (Bring Your Own Key), idêntico ao fluxo de `user_api_keys`. O fluxo OAuth completo (`meta-oauth`, FR-META-001) é incremento futuro que popula a mesma tabela.
- **Edge function `publish-meta`:** resolve a credencial por request e publica no IG/FB do dono do conteúdo.

---

## Resolution order (canonical — espelha API Tenancy Model)

| # | Camada | Fonte | Permitido em |
|---|--------|-------|--------------|
| 1 | **Per-user** | `meta_config` WHERE `user_id = <owner>` → `long_lived_token` + `instagram_business_account_id` / `pages[].access_token` | SEMPRE (caminho primário) |
| 2 | **Global vault fallback** | — | **PROIBIDO** em publish user-facing. Meta é per-tenant por natureza; não há env global legítimo aqui. |
| 3 | **Hard failure** | — | HTTP 402 `{ error: "meta_not_configured", action: "Configure your Meta credentials at /dashboard/settings" }` · pulse `infra_health_logs status=degraded reason=no_config` |

**Owner resolution:** o request traz `user_id` (JWT do frontend OU body em chamada service-role do pipeline). A receita/publicação pertence ao **dono do conteúdo**. Token expirado/`requires_reauth=true` → HTTP 402 `meta_requires_reauth` (camada 3), nunca publicar com token morto.

---

## Sequence (`publish-meta`)

1. **Auth:** validar `Authorization: Bearer`. Resolver `userId` via `auth.getUser()` (JWT frontend) OU `body.user_id` (service-role pipeline) — espelha `publish-social:38-59`.
2. **Resolve config (camada 1):** SELECT `meta_config` WHERE `user_id = userId` (service-role client, bypassa RLS para ler token). Se ausente → 402 `meta_not_configured` (camada 3) + pulse degraded.
3. **Reauth gate:** se `requires_reauth = true` OU `token_expires_at < now()` → 402 `meta_requires_reauth` + pulse degraded. **Não** publicar.
4. **Publish por plataforma:**
   - **Instagram (FR-META-002):** POST `/{ig_business_account_id}/media` (`image_url` + `caption` + `access_token`) → container id → publica via POST `/{ig_business_account_id}/media_publish` (`creation_id`). (Poll de status do container quando `status_code != FINISHED`, NFR-META-003 ≤ 12s.)
   - **Facebook (FR-META-003):** POST `/{page_id}/feed` (`message` + page `access_token`).
5. **Persistir (PROC-META-002):** INSERT `meta_posts` (`platform`, `meta_post_id`, `post_url`, `caption`, `media_url`, `status`, `user_id`).
6. **Mesh observation:** INSERT `mcorch_nodes` (`node_type='observation'`, `name='post:<platform>:<post_id>'`, `user_id`) + `mcorch_edges` (`relation_type='observes'`, `target_id=<asset/content node>`) — quando houver content node de origem. Autoembed via trigger.
7. **Telemetry (FR-META-009):** pulse `infra_health_logs.service='publish-meta'` em todo path (`healthy` / `degraded`).
8. **Return:** `{ success, posts: [{ platform, meta_post_id, post_url }] }`.

---

## Verification gates

| Gate | Check | Pass criterion |
|------|-------|----------------|
| G1 | User COM config → publish IG | HTTP 200 · `meta_post_id` retornado · row em `meta_posts` (status=published) |
| G2 | User SEM config → publish | HTTP 402 · body `meta_not_configured` · ZERO row em `meta_posts` |
| G3 | Token expirado / `requires_reauth` → publish | HTTP 402 `meta_requires_reauth` · ZERO chamada à Graph API |
| G4 | RLS isolation (TC-META-002) | User A não lê/escreve `meta_config` de User B (REST com JWT de A → 0 rows de B) |
| G5 | Column-grant | `select=long_lived_token` via JWT (anon/authenticated) → `permission denied` (token nunca volta ao client) |
| G6 | Telemetria | `infra_health_logs.service='publish-meta'` recebe pulse em cada path |
| G7 | Zero global em path user-facing | `grep -i "META.*TOKEN\|FACEBOOK.*SECRET" publish-meta` → 0 refs de env como fonte primária de publish |

---

## Recovery path

| Cenário | Detecção | Recovery |
|---------|----------|----------|
| User reclama "post não saiu" | `meta_posts.status='failed'` + `error_message` | Ler `error_message`; se token → orientar reauth em /dashboard/settings |
| Token expirou (60d) | Graph API 190 / `OAuthException` | `publish-meta` seta `meta_config.requires_reauth=true` + 402; UI mostra banner vermelho (PROC self-healing) |
| Circuit (Meta 5xx contínuo) | pulses `degraded` repetidos | NFR-META-005: suspender tentativas do tenant por 15min (incremento futuro — registrar OTD se ainda não implementado) |
| Regressão (env global reintroduzido) | G7 falha em grep/CI | Reverter; Meta nunca usa env global em publish |
| `meta_config` lookup erro DB | `console.error` no edge log + pulse `status=degraded` | Fail-closed (camada 3), nunca publicar sem credencial resolvida |

---

## Success signal (whole protocol)

- G1–G7 verdes no smoke.
- `publish-meta` deployado (script size + ACTIVE em `supabase functions list`).
- Migration `meta_config` aplicada (aprovada por `/security-review`).
- `infra_health_logs.service='publish-meta'` com pulses recentes (`last_seen_at` < 1h pós-smoke).

---

## Anti-patterns prohibited

- ❌ `Deno.env.get('META_*_TOKEN')` / `FACEBOOK_*` como fonte primária de publish user-facing.
- ❌ Publicar com `requires_reauth=true` ou token expirado (post falha silenciosa na Meta).
- ❌ Retornar `long_lived_token` ou page tokens ao client (column-grant REVOKE obrigatório).
- ❌ Resolver `meta_config` sem filtrar `user_id` do dono (vazamento cross-tenant — TC-META-002).
- ❌ Compartilhar conta Meta de um user com outro via credencial global (fraude por design).

---

## Known debt — OTD-META-ENCRYPT

`long_lived_token` e page tokens são gravados em **TEXT plaintext** protegido por RLS + column-grant REVOKE (decisão Sovereign 2026-05-30: consistente com `social_accounts.access_token` e `user_api_keys`, que já guardam tokens da mesma classe em plaintext). A NFR-META-001 (AES-256-GCM / pgsodium at-rest) fica registrada como **OTD-META-ENCRYPT** — dívida de cifragem-at-rest do **projeto inteiro** (cobre `social_accounts` + `user_api_keys` + `meta_config`), pois cifrar só `meta_config` seria teatro enquanto a mesma classe de token vaza pela tabela antiga. Critério de fechamento: pgsodium/Vault habilitado + colunas de token migradas em TODAS as tabelas de credencial.

---

## Connection to Survival Laws

- **Lei 1 (Materialidade):** cada gate produz prova material (HTTP status + body + `meta_posts` row + pulse + REST permission-denied).
- **Lei 2 (Anticipated Process):** este SOP escrito ANTES do código (requisito API Tenancy item 5).
- **Lei 3 (Pruning):** resolução stateless por request; nada acumulado.
- **Lei 4 (ORO):** triplet declarado acima; Reviewer = Sovereign aprova migration + smoke antes do deploy.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

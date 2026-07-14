# SOP: Pinterest Publish — Credential Resolution (Per-User) + Video-Pin Publish

**Status:** ACTIVE · v1.0 · 2026-06-27
**Owner:** Sovereign (Gabriel Zarattini)
**Survival Law 2 compliance:** Escrita ANTES do código do branch `pinterest` em `supabase/functions/publish-social/index.ts` + migration `social_app_config` (requisito explícito da diretiva API Tenancy item 5).
**Canonical directive:** `CLAUDE.md > Architecture > "API Tenancy Model — Per-User Credentials"`
**Source of Truth (blueprint):** `.claude/context/social-connect-3platforms-blueprint-2026-06-27.md` (§2.3 seams · §3 fatos fundamentados · §5.3 SOP skeleton · §6 audit gates)
**Mirrors:** `docs/processes/meta-credential-resolution.md` (estrutura · resolution-order · telemetria · column-REVOKE)

---

## Context

A distribuição de conteúdo no Pinterest (video pin, API v5) exige **dois níveis de credencial distintos**, e o SOP precisa separá-los:

1. **App credentials** (`client_id` + `client_secret`) — identificam o **app OAuth** registrado pelo Sovereign no Pinterest Developer Portal. São o que assina a troca `code→token` e o `grant_type=refresh_token` (header `Authorization: Basic base64(client_id:client_secret)`). Resolvidos pela ordem da API Tenancy (per-user `social_app_config` → env fallback → fail-closed).
2. **User tokens** (`access_token` 30d + `refresh_token` rotativo contínuo) — identificam o **criador** (conta Business do Gabriel AI / CCIO). Já fluem para `social_accounts` (VIEW Vault-mascarada, INSTEAD OF tenant-guarded, `.upsert({onConflict:'user_id,platform'})`) — **reuso verbatim, nenhuma tabela nova de token**.

O branch publish (`else if (platform==='pinterest')` em `publish-social`) é invocado pelo `PublishNode` do pipeline de orquestração e pelo cron `auto-publish`. Ele DEVE resolver as **app credentials** pela ordem canônica abaixo e os **user tokens** de `social_accounts` filtrando pelo `user_id` do **dono do conteúdo**, nunca de um env global em fluxo user-facing sem fallback registrado.

**Por que importa (multi-tenant readiness):** atribuição de receita correta por tenant · quota/rate-limit `org_write` isolada por app (um tenant não esgota o limite global) · LGPD (cada user controla/revoga seu app + tokens) · blast radius de credencial roubada confinado a um tenant.

---

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (build do branch + migration) + Sovereign (registro do app no Developer Portal, Business account, Trial→Standard) + Edge runtime `publish-social` (execução do publish)
- **Reviewer:** Sovereign (Gabriel) — aprova migration `social_app_config` via `/security-review` + valida o smoke
- **Owner:** Sovereign — blast radius = controle da conta Pinterest por tenant + atribuição de receita ML + quota `org_write` + tokens OAuth rotativos

---

## Operator (quem executa manualmente hoje)

- **Sovereign:** registra o app no Pinterest Developer Portal a partir de uma **conta Business** + aceita os Developer Terms + fornece uma **privacy-policy URL** → recebe `client_id`/`client_secret` (Trial) e depois submete o upgrade **Trial→Standard** (ver "Audit / app-registration gate" abaixo). Sem o app NÃO há `client_id`/`secret` → nenhum OAuth começa.
- **Usuário Zero / cliente:** configura suas **app credentials** em `/dashboard/settings` (card "Pinterest Integration", hook `useSocialAppConfig` → upsert `social_app_config` WHERE `platform='pinterest'` com `client_id` + `client_secret` + `scopes` + `metadata.board_id`). Modelo BYOK, idêntico ao fluxo de `user_api_keys`/`meta_config`. O fluxo OAuth (`social-auth-init`/`social-auth-callback`, branch Pinterest) popula `social_accounts` com os **user tokens**.
- **Edge function `publish-social`:** resolve as app credentials por request (ordem canônica) + os user tokens de `social_accounts`, e publica o video pin no board do dono do conteúdo.

---

## Schema — `social_app_config` (single per-user table p/ app credentials)

> **Decisão autoritativa (2026-06-27, sobrepõe a sugestão "mirror meta_config / 3 tabelas" do blueprint §2.3):** uma ÚNICA tabela per-user `social_app_config`, keyed `UNIQUE(user_id, platform)`, serve TikTok + YouTube + Pinterest. Espelha o hardening de `meta_config`: VIEW mascarada + INSTEAD OF tenant-guard + column-level REVOKE no segredo.

```sql
-- social_app_config: per-user OAuth APP credentials (NOT user tokens — those live in social_accounts)
create table public.social_app_config (
  id            uuid primary key default gen_random_uuid(),
  user_id       uuid not null references auth.users(id) on delete cascade,
  platform      social_platform not null,            -- enum vivo: ...|tiktok|youtube|pinterest|...
  client_id     text,
  client_secret text,                                 -- Vault-encrypted + column-level REVOKE (mirror meta_config.long_lived_token)
  scopes        text[],
  metadata      jsonb default '{}'::jsonb,            -- pinterest: board_id · youtube: channel_id
  is_active     boolean not null default true,
  created_at    timestamptz not null default now(),
  updated_at    timestamptz not null default now(),
  unique (user_id, platform)
);

alter table public.social_app_config enable row level security;
-- default-deny + auth.uid() = user_id (mirror meta_config / social_accounts)
revoke select (client_secret) on public.social_app_config from anon, authenticated;
```

- **RLS default-deny** + política `auth.uid() = user_id` (SELECT/INSERT/UPDATE/DELETE own-only).
- **Masked VIEW** (`social_app_config` exposta ao client com `client_secret` mascarado) + **INSTEAD OF trigger** tenant-guarded (`auth.uid() = user_id`) escrevendo o segredo no Vault — exatamente o padrão de `meta_config`/`social_accounts`.
- **Column-level REVOKE** em `client_secret` p/ anon+authenticated (o segredo nunca volta ao client; o teste de chave é server-side).
- **`/security-review` obrigatório** antes do commit da migration (FMEA-011 — cross-tenant data leak).

---

## Resolution order — Pinterest APP credentials (canonical — espelha API Tenancy Model)

> Aplica-se às **app credentials** (`client_id`/`client_secret`). Os **user tokens** (`access_token`/`refresh_token`) sempre vêm de `social_accounts` filtrado pelo `user_id` do dono.

| # | Camada | Fonte | Permitido em |
|---|--------|-------|--------------|
| 1 | **Per-user** | `social_app_config` WHERE `user_id = <owner>` AND `platform='pinterest'` AND `is_active = true` → `client_id` + `client_secret` (decifrado server-side) + `metadata.board_id` | SEMPRE (caminho primário) |
| 2 | **Env fallback** | `Deno.env.get('PINTEREST_CLIENT_ID')` + `Deno.env.get('PINTEREST_CLIENT_SECRET')` | **Sovereign-only onboarding default** — Usuário Zero único tenant, slices probe-first. **OTD + SLA registrados** (ver "Known debt"); promover a per-user antes do 2º tenant. NUNCA caminho primário em fluxo multi-tenant. |
| 3 | **Hard failure** | — | HTTP 402/501 `{ error: "pinterest_not_configured", action: "Configure your Pinterest credentials at /dashboard/settings" }` · pulse `infra_health_logs status=degraded reason=no_config` |

**Owner resolution:** o request traz `user_id` (JWT do frontend OU `body.user_id` em chamada service-role do pipeline/cron — espelha `publish-social:38-59`). A receita/publicação pertence ao **dono do conteúdo**.

**Token-state gate (user tokens, não app credentials):** se a linha `social_accounts` (platform=pinterest) estiver ausente → 402 `pinterest_not_connected`; se `token_expires_at < now()` → o pre-check de refresh de `publish-social:85` dispara `refresh-social-token` (branch Pinterest, **rotativo atômico** — ver Recovery) ANTES de publicar; refresh falho → 402 `pinterest_requires_reauth`. **Nunca** publicar com token morto.

**Sibling env names (mesma tabela `social_app_config`, outras plataformas):** TikTok `TIKTOK_CLIENT_KEY`/`TIKTOK_CLIENT_SECRET` · YouTube `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET`.

---

## Media transfer (nota) — register → multipart upload → poll → create pin

> Pinterest v5 video pin é **assíncrono em 4 passos**. O binário do vídeo é **enviado** (multipart presigned-POST S3); a **cover é PUXADA** async pela Pinterest (precisa de URL público resolvível). Paths corretos: `/v5/media`, `/v5/boards`, `/v5/pins` (NÃO `/v5/pins/create` — slugs de doc dão 404).

- **(0) Board destino — cachear, NUNCA criar por run.** `GET https://api.pinterest.com/v5/boards` → achar `board_id`. Se ausente, `POST .../v5/boards` UMA vez e gravar em `social_app_config.metadata.board_id`. Runs subsequentes leem do cache.
- **(1) register:** `POST https://api.pinterest.com/v5/media` body `{ media_type: 'video' }` (Bearer user token) → resposta `{ media_id, upload_url, upload_parameters }`.
- **(2) upload (multipart):** `POST` o MP4 no `upload_url` como **`multipart/form-data`**, **SEM header `Authorization`**, com TODOS os `upload_parameters` **VERBATIM** (não mutar nenhum valor) e o **campo `file` por ÚLTIMO** — é uma presigned-POST do S3, onde a ordem dos campos e os valores são parte da assinatura; ordem errada ou param mutado → **403**. Sucesso = **`204`** (sem body).

  Ordem dos campos do form (file por último, literal):
  ```
  for (const [k, v] of Object.entries(upload_parameters)) form.append(k, v); // params VERBATIM, na ordem
  form.append('file', mp4Blob, 'video.mp4');                                  // file SEMPRE por ÚLTIMO
  ```
- **(3) poll:** `GET https://api.pinterest.com/v5/media/{media_id}` (Bearer) com backoff até `status === 'succeeded'` (tratar `failed` → re-register + re-upload).
- **(4) create pin:** `POST https://api.pinterest.com/v5/pins` (Bearer) body:
  ```json
  {
    "board_id": "<cached board_id>",
    "title": "<≤100 chars>",
    "description": "<≤800 chars>",
    "link": "<affiliate/UTM link>",
    "media_source": {
      "source_type": "video_id",
      "media_id": "<media_id>",
      "cover_image_url": "<URL https PÚBLICA / signed TTL-longo>"
    }
  }
  ```
  → **`201`** com pin id = `result.id`.

  **`cover_image_url` é OBRIGATÓRIA e PUXADA async** pela Pinterest. A cover precisa sobreviver num URL público OU signed-URL de **TTL longo** (horas) — TTL curto expira antes do fetch e o pin **falha em silêncio**. Para o cron `auto-publish`, isso casa com o gap de transporte de mídia (blueprint §7 decisão #4: resolver+assinar `content_library.media_url` no dispatch com TTL longo).

---

## Sequence — branch `pinterest` em `publish-social` (Lei 2)

| # | Step | Material success criterion (artefato real) |
|---|------|--------------------------------------------|
| 1 | **Auth:** validar `Authorization: Bearer`. Resolver `userId` via `auth.getUser()` (JWT frontend) OU `body.user_id` (service-role pipeline/cron) — espelha `publish-social:38-59`. | `userId` resolvido (não-null) · request rejeitado com 401 se ausente |
| 2 | **Resolve app credentials (camadas 1→2):** SELECT `social_app_config` WHERE `user_id=userId` AND `platform='pinterest'` AND `is_active=true` (service-role decifra `client_secret`). Ausente → env fallback `PINTEREST_CLIENT_ID`/`PINTEREST_CLIENT_SECRET`. Nenhum dos dois → **402/501** (camada 3). | `client_id`/`client_secret` resolvidos · OU HTTP **402** body `pinterest_not_configured` + pulse degraded |
| 3 | **Resolve user token + reauth gate:** SELECT `social_accounts` WHERE `user_id=userId` AND `platform='pinterest'`. Ausente → 402 `pinterest_not_connected`. `token_expires_at < now()` → `refresh-social-token` (Pinterest rotativo atômico) ANTES de publicar; falho → 402 `pinterest_requires_reauth`. | `access_token` válido em mãos · OU 402 `pinterest_not_connected`/`pinterest_requires_reauth` · ZERO chamada à v5 com token morto |
| 4 | **Board destino (cachear):** ler `social_app_config.metadata.board_id`; ausente → `GET /v5/boards` (achar) senão `POST /v5/boards` UMA vez + persistir `metadata.board_id`. | `board_id` não-null (do cache OU HTTP **201** do `POST /v5/boards`) — gravado em `metadata.board_id` |
| 5 | **register:** `POST /v5/media {media_type:'video'}`. | resposta com `media_id` + `upload_url` + `upload_parameters` (não-null) |
| 6 | **upload (multipart):** `POST` MP4 no `upload_url`, params VERBATIM, campo `file` por ÚLTIMO, SEM Bearer. | HTTP **204** (sucesso do presigned-POST) |
| 7 | **poll:** `GET /v5/media/{media_id}` com backoff até `status='succeeded'`. | `status === 'succeeded'` retornado pela v5 |
| 8 | **create pin:** `POST /v5/pins {board_id, title, description, link, media_source:{source_type:'video_id', media_id, cover_image_url:<URL público>}}`. | HTTP **201** + **pin id** (`result.id`) |
| 9 | **Persistir:** INSERT `social_posts` (`platform='pinterest'`, `platform_post_id=<pin id>`, `post_url`, `caption`, `media_url`, `status`, `user_id`). | row em `social_posts` (status=published) com `platform_post_id` = pin id (SELECT id = UUID) |
| 10 | **Mesh observation:** INSERT `mcorch_nodes` (`node_type='observation'`, `name='pin:pinterest:<pin id>'`, `user_id`) + `mcorch_edges` (`relation_type='observes'`, `target_id=<content node>`) quando houver content node de origem. Autoembed via trigger. | UUID do `mcorch_nodes` retornado (`INSERT ... RETURNING id`) |
| 11 | **Telemetry:** pulse `infra_health_logs.service='publish-pinterest'` em todo path (`healthy` / `degraded`). | row em `infra_health_logs.service='publish-pinterest'` (`last_seen_at` < 1h) |
| 12 | **Return:** `{ success, posts: [{ platform:'pinterest', platform_post_id, post_url }] }`. | body 200 com `platform_post_id` = pin id |

---

## Verification gates

| Gate | Check | Pass criterion |
|------|-------|----------------|
| G1 | User COM app config + token → publish video pin | HTTP **201** na create-pin · `platform_post_id` (pin id) retornado · row em `social_posts` (status=published) |
| G2 | User SEM app config (e sem env) → publish | HTTP **402** · body `pinterest_not_configured` · ZERO row em `social_posts` · pulse `degraded reason=no_config` |
| G3 | User SEM linha `social_accounts` (não conectado) → publish | HTTP **402** `pinterest_not_connected` · ZERO chamada à v5 |
| G4 | Token expirado → publish | refresh rotativo dispara; falho → **402** `pinterest_requires_reauth` · ZERO `POST /v5/pins` com token morto |
| G5 | Multipart upload com params na ordem certa + `file` por último | HTTP **204** no `upload_url` (params VERBATIM provados) |
| G6 | RLS isolation | User A não lê/escreve `social_app_config` de User B (REST com JWT de A → 0 rows de B) |
| G7 | Column-grant | `select=client_secret` via JWT (anon/authenticated) → `permission denied` (segredo nunca volta ao client) |
| G8 | Telemetria | `infra_health_logs.service='publish-pinterest'` recebe pulse em cada path (success/degraded/error) |
| G9 | Zero global em path user-facing sem fallback | `grep -i "PINTEREST_CLIENT" publish-social` → as únicas refs de env são o fallback camada-2 explícito (nunca fonte primária) |
| G10 | **Materialidade (Lei 1) — público** | POST-Standard: `https://pinterest.com/pin/<id>` resolve público (`curl` 200). PRE-Standard (Trial): apenas `201` pin id sandbox/creator-only — NÃO afirmar "ao vivo" |

---

## Recovery path (por modo de falha — blueprint §5.3)

| Cenário | Detecção | Recovery (exato) |
|---------|----------|------------------|
| **App não configurado** | SELECT `social_app_config` vazio + env vazio | 402/501 `pinterest_not_configured` + pulse degraded; orientar config em `/dashboard/settings`. Fail-closed — nunca prosseguir com chave compartilhada silenciosa. |
| **Mídia `failed` no poll** (passo 3) | `GET /v5/media/{media_id}` retorna `status='failed'` | **re-register** (`POST /v5/media`) + **re-upload** do MP4 (novo `media_id`+`upload_url`). Não reusar `upload_url` morto. |
| **Multipart 403** (passo 2) | `POST upload_url` retorna 403 | Reconstruir o form: TODOS os `upload_parameters` **VERBATIM** (sem mutar) + campo **`file` por ÚLTIMO** + **SEM** header `Authorization`. 403 = ordem/param violou a assinatura do presigned-POST. |
| **Cover expirada / pin sem capa** | create-pin 201 mas pin sem cover (fetch async falhou) | Re-gerar `cover_image_url` como **signed TTL-longo** (horas) OU bucket público; a Pinterest puxa async, TTL curto expira antes do fetch. Re-criar o pin com a cover durável. |
| **429 `org_write`** | HTTP 429 da v5 | Backoff exponencial contra o limite `org_write` (**300/dia Trial · 100/min Standard**); capturar o envelope de erro; re-tentar dentro do orçamento de quota. |
| **Refresh token rotativo perdido** (concorrência cron × run manual) | re-OAuth forçado / `invalid_grant` no próximo refresh | Persistir `access_token` + `refresh_token` retornados **ATOMICAMENTE** (advisory-lock / SELECT-FOR-UPDATE em torno do refresh→persist, espelhando `begin_autopilot_cycle`). Cada refresh devolve NOVO access_token E NOVO refresh_token — gravar AMBOS. Refrescar dentro da janela de 60d mantém a cadeia viva. |
| **Path 404 (`/v5/pins/create` etc.)** | HTTP 404 da v5 | Usar os paths corretos: `/v5/pins`, `/v5/boards`, `/v5/media` (os `*/create` são slugs de doc). |
| **Trial → pin sandbox (não público)** | `201` pin id mas sem URL `pinterest.com/pin/<id>` resolvível | Esperado sob **Trial** (sandbox/creator-only). Transporte está provado; **halt** nas afirmações de "ao vivo" até o upgrade **Standard** (ação Sovereign — ver gate abaixo). Se Standard foi negado → re-gravar a demo (OAuth + ação v5 ao vivo). |
| **Regressão (env global reintroduzido como primário)** | G9 falha em grep/CI | Reverter; env é fallback Sovereign-only de onboarding, nunca fonte primária em fluxo multi-tenant. |

---

## Success signal (whole protocol)

- G1–G10 verdes no smoke.
- Branch `pinterest` deployado em `publish-social` (script size + ACTIVE em `supabase functions list`).
- Migration `social_app_config` aplicada (aprovada por `/security-review`).
- `infra_health_logs.service='publish-pinterest'` com pulses recentes (`last_seen_at` < 1h pós-smoke).
- **Materialidade (Lei 1) — o gate de "publicado":**
  - **PRE-Standard (Trial sandbox):** HTTP **201** com pin id (`result.id`) — transporte (register→upload 204→poll succeeded→create 201) **provado**. NÃO afirmar "publicado ao vivo".
  - **POST-Standard:** URL público **`https://pinterest.com/pin/<id>`** resolve (`curl` 200) — única afirmação honesta de "ao vivo".

---

## Audit / app-registration gate (ação Sovereign — caminho crítico, lead-time de dias)

> **Sem o registro do app não há `client_id`/`secret` → nenhum OAuth começa.** Estes passos são **fora do código** e do Sovereign (Human-in-the-Loop). Começar HOJE.

| # | Ação | Destrava | Lead-time |
|---|------|----------|-----------|
| 1 | **Conta Business** + aceitar **Developer Terms** + fornecer **privacy-policy URL** + registrar app (redirect URI **EXATO**, sem wildcard, match a uma entrada Configure>Redirect URIs) → pedir **Trial** | Qualquer acesso v5 + `client_id`/`client_secret` (Trial) | ~1 dia útil |
| 2 | Submeter **Trial → Standard** (demo: fluxo OAuth + uma **ação API v5 ao vivo**) | Pins **PÚBLICOS** (URL resolvível) + rate maior (`org_write` 100/min vs 300/dia) | sem SLA (~dias) |

**Sem o gate #2 (Standard), todo pin é sandbox/creator-only** — sem URL público resolvível. O transporte se prova sob Trial; a afirmação de "ao vivo" só pós-Standard (Lei 1).

**Scopes (planejar o set COMPLETO de cara):** `boards:read,boards:write,pins:read,pins:write,user_accounts:read`. Adicionar scope DEPOIS força re-autorização total (o refresh token existente não ganha o scope novo).

---

## Telemetry — `infra_health_logs` service='publish-pinterest'

Pulse em **todo path** (alinhado a FR-VA / padrão `publish-meta`):

| Path | `status` | `reason` / `event` |
|------|----------|--------------------|
| Pin criado (201) | `healthy` | `event='pin_published'` · `metadata.pin_id` (PRE-Standard: anotar `sandbox=true`) |
| App não configurado | `degraded` | `reason='no_config'` |
| Não conectado / reauth | `degraded` | `reason='not_connected'` / `reason='requires_reauth'` |
| Mídia `failed` / multipart 403 / cover expirada | `degraded` | `reason='media_transfer_failed'` · `metadata.step` |
| 429 `org_write` | `degraded` | `reason='rate_limited'` |
| 5xx v5 contínuo / exceção | `error` | `reason='pinterest_api_error'` · `metadata.log` (envelope de erro) |

> O chokepoint de telemetria respeita a allowlist de `infra_health_logs` (migration `20260615170000`) — não vazar dados per-tenant na tabela global-read; `metadata` carrega só ids/steps não-sensíveis.

---

## Anti-patterns prohibited

- ❌ `Deno.env.get('PINTEREST_CLIENT_SECRET')` como fonte **primária** em fluxo multi-tenant (env é fallback Sovereign-only de onboarding, com OTD+SLA).
- ❌ Publicar com `token_expires_at < now()` sem refresh, ou após refresh falho (pin falha silenciosa).
- ❌ Retornar `client_secret` (ou user tokens) ao client (column-REVOKE + Vault obrigatórios).
- ❌ Resolver `social_app_config` sem filtrar `user_id` do dono (vazamento cross-tenant).
- ❌ **Criar board por run** — sempre cachear `metadata.board_id` (`POST /v5/boards` UMA vez).
- ❌ Mutar `upload_parameters` ou pôr o campo `file` antes deles no multipart (quebra a assinatura presigned-POST → 403).
- ❌ `cover_image_url` com TTL curto (a Pinterest puxa async → fetch falha → pin sem capa silencioso).
- ❌ Usar paths `*/create` (`/v5/pins/create`) — são slugs de doc → 404. Usar `/v5/pins`, `/v5/boards`, `/v5/media`.
- ❌ Gravar só o novo `access_token` no refresh e **descartar** o novo `refresh_token` rotativo (quebra a cadeia → re-OAuth forçado).
- ❌ Afirmar "publicado ao vivo" sob Trial (pin sandbox sem URL público — viola Lei 1).

---

## Known debt

### OTD-SOCIAL-APP-ENV-FALLBACK (env-override Sovereign-only — SLA: 2º tenant)
As **app credentials** das 3 plataformas (Pinterest/TikTok/YouTube) podem resolver via env (`PINTEREST_CLIENT_ID/SECRET`, `TIKTOK_CLIENT_KEY/SECRET`, `GOOGLE_CLIENT_ID/SECRET`) como default de onboarding **enquanto o Usuário Zero é o único tenant** (slices probe-first; os audits são o caminho crítico real, não a tabela de config). **Critério de fechamento:** promover 100% das resoluções a `social_app_config` per-user (migration + UI Settings + hook `useSocialAppConfig`) **antes do 2º tenant**. Tokens per-USER já vão p/ `social_accounts` de qualquer forma. Rastreado como decisão #1 do blueprint §7.

### OTD-META-ENCRYPT (cifragem-at-rest do projeto inteiro)
`client_secret` (e os user tokens em `social_accounts`) são protegidos por RLS + column-grant REVOKE + Vault; a cifragem AES-256-GCM/pgsodium at-rest de TODA tabela de credencial (`user_api_keys` + `social_accounts` + `meta_config` + `social_app_config`) é a mesma dívida registrada em `docs/processes/meta-credential-resolution.md`. Critério de fechamento idêntico (pgsodium habilitado + todas as colunas de token migradas).

---

## Connection to Survival Laws

- **Lei 1 (Materialidade):** cada gate produz prova material (HTTP status + body + pin id + `social_posts` row + pulse + REST permission-denied). O gate de "público" exige URL `pinterest.com/pin/<id>` resolvível pós-Standard — `201` sob Trial prova só o transporte.
- **Lei 2 (Anticipated Process):** este SOP escrito ANTES do código do branch Pinterest + migration `social_app_config` (requisito API Tenancy item 5).
- **Lei 3 (Pruning):** resolução stateless por request; nada acumulado além do `board_id` cacheado (durável por design, não contexto).
- **Lei 4 (ORO):** triplet declarado acima; Reviewer = Sovereign aprova migration + smoke + os gates de audit antes do deploy.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

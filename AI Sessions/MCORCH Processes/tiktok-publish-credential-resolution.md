# SOP: TikTok Publish Credential Resolution (Per-User)

**Status:** ACTIVE · v1.0 · 2026-06-27
**Owner:** Sovereign (Gabriel Zarattini)
**Survival Law 2 compliance:** Escrita ANTES do código do branch TikTok em `supabase/functions/publish-social/index.ts` (seam `:233`), dos branches OAuth (`social-auth-init:95` · `social-auth-callback:171` · `refresh-social-token:133`) e da migration `social_app_config` (requisito explícito da diretiva API Tenancy item 5).
**Canonical directive:** `CLAUDE.md > Architecture > "API Tenancy Model — Per-User Credentials"`
**Source of Truth:** `.claude/context/social-connect-3platforms-blueprint-2026-06-27.md` (§2.1 seams · §3 fatos fundamentados · §5.1 SOP esqueleto · §6 audit gates) — workflow `wf_b5a35451-7dc`, confiança ALTA, cada claim ancorado em `developers.tiktok.com`.
**Sibling SOP (template):** `docs/processes/meta-credential-resolution.md`

---

## Context

A publicação autônoma no TikTok (Content Posting API — **Direct Post**) exige dois planos de credencial **distintos** que esta SOP separa explicitamente:

1. **App credentials (`client_key` / `client_secret`):** identificam o app do MCORCH no TikTok Developer Portal. São o INPUT do fluxo OAuth e da troca `code → token`. Resolvidos por `social_app_config` per-user (ver Resolution order).
2. **User tokens (`access_token` / `refresh_token` / `open_id`):** identificam a conta TikTok do criador. São o OUTPUT do OAuth, gravados em `social_accounts` (VIEW Vault-mascarada, INSTEAD OF tenant-guarded, `onConflict:'user_id,platform'`).

A natureza do TikTok é per-usuário: cada criador conecta a sua própria conta TikTok via Login Kit. O `video.publish` scope (Direct Post autônomo) é o crítico — **NUNCA `video.upload`** (draft-to-inbox exige humano finalizar no app, não é autônomo).

`publish-social` é invocada pelo `PublishNode` do pipeline de orquestração e pelo `auto-publish` cron (cadência do Viral Autopilot). Ela DEVE resolver as **app credentials** de `social_app_config` filtrando por `user_id = <dono do conteúdo>` e os **user tokens** de `social_accounts` do mesmo dono — nunca de um env global em fluxo user-facing.

**Por que importa (multi-tenant readiness):** controle de conta TikTok isolado por tenant · atribuição de receita de afiliado correta · LGPD (cada user controla/revoga sua credencial) · anti-fraude (um user não publica pela conta de outro) · blast radius de credencial roubada confinado a um tenant · segregação de rate-limit (um user não esgota o limite global de init 6/min).

**Status de prontidão (Lei 1):** o transporte FILE_UPLOAD + `create→poll→publish` é provável end-to-end já na fase pré-audit, mas todo post nasce **SELF_ONLY / privado** até o TikTok Content Posting API audit passar (gate Sovereign, ~2–6 semanas — ver Audit gate). Afirmação honesta de "ao vivo" só pós-audit.

---

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (build do branch + migration) + Edge runtime `publish-social`/`social-auth-*`/`refresh-social-token` (execução) + Sovereign (registro do app no TikTok Developer Portal · submissão do audit · autorização OAuth da conta da persona)
- **Reviewer:** Sovereign (Gabriel) — aprova migration `social_app_config` via `/security-review` + valida o smoke + autoriza ir-público pós-audit
- **Owner:** Sovereign — blast radius = controle da conta TikTok da persona por tenant + atribuição de receita de afiliado + tokens OAuth rotativos de 365d

---

## Operator (quem executa manualmente hoje)

- **Usuário Zero / cliente:** configura as **app credentials** em `/dashboard/settings` (card "TikTok Integration", hook TanStack Query `useSocialAppConfig` → upsert `social_app_config` WHERE `platform='tiktok'` com `client_id` (= `client_key`) + `client_secret` + `scopes[]`). Modelo BYOK, idêntico ao fluxo de `user_api_keys`/`meta_config`. Em seguida conecta a conta TikTok via fluxo OAuth (Login Kit) que popula `social_accounts`.
- **Edge function `social-auth-init`/`social-auth-callback`:** lê as app credentials e troca `code → token`, gravando os user tokens em `social_accounts`.
- **Edge function `publish-social`:** resolve app credentials + user tokens por request e publica no TikTok do dono do conteúdo via FILE_UPLOAD chunked.
- **Edge function `refresh-social-token`:** refresca proativamente o `access_token` de 24h antes do expiry, re-armazenando o `refresh_token` **rotativo**.

---

## Resolution order — App credentials (canonical — espelha API Tenancy Model)

> Aplica-se às **app credentials** (`client_key`/`client_secret`). Os **user tokens** vêm sempre de `social_accounts` per-user (não há fallback env para tokens de usuário — eles SÃO a conexão do tenant).

| # | Camada | Fonte | Permitido em |
|---|--------|-------|--------------|
| 1 | **Per-user** | `social_app_config` WHERE `user_id = <owner>` AND `platform = 'tiktok'` AND `is_active = true` → `client_id` (client_key) + `client_secret` + `scopes[]` | SEMPRE (caminho primário) |
| 2 | **Global vault fallback** | `Deno.env.get('TIKTOK_CLIENT_KEY')` + `Deno.env.get('TIKTOK_CLIENT_SECRET')` | **SÓ** como default de onboarding **Sovereign-only / Usuário Zero** (single-tenant probe-phase) OU cron/service-role sem `auth.uid()` no path. **Registrado como OTD-SOCIAL-APP-ENV** (SLA: promover a `social_app_config` per-user ANTES do 2º tenant). NUNCA shared key silenciosa em fluxo de tenant. |
| 3 | **Hard failure** | — | HTTP 402/501 `{ error: "tiktok_not_configured", action: "Configure your TikTok credentials at /dashboard/settings" }` · pulse `infra_health_logs status=degraded reason=no_config` |

**Owner resolution:** o request traz `user_id` (JWT do frontend OU `body.user_id` em chamada service-role do pipeline/`auto-publish`). A receita/publicação pertence ao **dono do conteúdo** — espelha `publish-social:38-59`. User token expirado sem refresh viável → 402 `tiktok_requires_reauth` (camada 3), nunca publicar com token morto.

### `social_app_config` — schema (authoritative)

Tabela ÚNICA per-user para app credentials das 3 plataformas (TikTok/YouTube/Pinterest), keyed `UNIQUE(user_id, platform)` — substitui a sugestão `tiktok_config`/`youtube_config`/`pinterest_config` do blueprint §2/§7.

| Coluna | Tipo | Notas |
|--------|------|-------|
| `id` | `uuid` PK | `default gen_random_uuid()` |
| `user_id` | `uuid` | FK `auth.users(id)` ON DELETE CASCADE |
| `platform` | `social_platform` | enum vivo (`tiktok` já existe — migration `20260402014040:12`) |
| `client_id` | `text` | = `client_key` no léxico TikTok |
| `client_secret` | `text` | **Vault-encrypted + column-level REVOKE** (espelha `meta_config.long_lived_token`) |
| `scopes` | `text[]` | TikTok: `{video.publish,user.info.basic}` |
| `metadata` | `jsonb` | reservado p/ YouTube `channel_id` / Pinterest `board_id` (no-op p/ TikTok) |
| `is_active` | `boolean` | `default true` |
| `created_at` / `updated_at` | `timestamptz` | `default now()` |

- **`UNIQUE(user_id, platform)`** → `onConflict` do upsert.
- **RLS default-deny** + policy `auth.uid() = user_id` (SELECT/INSERT/UPDATE/DELETE).
- **Masked VIEW** (`client_secret` → `••••`) + **INSTEAD OF trigger tenant-guard** (`auth.uid() = user_id`, `search_path=''`, `service_role` isento) — espelha `meta_config`/`social_accounts` (migration `20260602150000`). Edge fns leem `client_secret` real via `decrypted_social_app_config` (service-role, bypassa RLS para resolver).
- **`/security-review` obrigatório** antes do commit (FMEA-011 — cross-tenant leak).

---

## Sequence — OAuth connect (`social-auth-init` → `social-auth-callback`)

| # | Step | Material success criterion |
|---|------|----------------------------|
| 1 | **Init authorize URL** (`social-auth-init:95`): resolver app creds (Resolution order). `else if (platform==='tiktok')` → redirect `https://www.tiktok.com/v2/auth/authorize/` com `client_key`, `response_type=code`, `redirect_uri` (pré-registrada, https, estática, ≤512 chars), `state` (HMAC-SHA256 já assinado `:56`), `scope=video.publish,user.info.basic` **separado por VÍRGULA** (espaço falha o consent em silêncio). PKCE opcional (defense-in-depth). | HTTP 302 `Location: https://www.tiktok.com/v2/auth/authorize/?...` com `client_key` per-user + scope vírgula-separado |
| 2 | **Callback token exchange** (`social-auth-callback:171`): verificar `state` (janela replay 10min) → `POST https://open.tiktokapis.com/v2/oauth/token/` `grant_type=authorization_code` + `client_key` + `client_secret` + `code` + `redirect_uri`. Resposta: `access_token` (86400s), `refresh_token` (31536000s), `open_id`, `scope`. | HTTP 200 da TikTok com `access_token`+`refresh_token`+`open_id` |
| 3 | **Upsert user tokens:** `social_accounts` `.upsert({onConflict:'user_id,platform'})` com `platform='tiktok'`, `platform_user_id=open_id`, `access_token`, `refresh_token`, `token_expires_at=now()+86400s`, `scopes`. | `SELECT id FROM social_accounts WHERE user_id=<owner> AND platform='tiktok'` retorna **UUID** (prova material da conexão) |

---

## Sequence — Publish (`publish-social` branch TikTok, seam `:233`)

> Padrão **create→poll→publish** espelhando o IG REELS provado (`:141-196`). Toda chamada respeita os rate limits do §3.

| # | Step | Material success criterion |
|---|------|----------------------------|
| 1 | **Auth + owner:** validar `Authorization: Bearer`. Resolver `userId` via `auth.getUser()` (JWT frontend) OU `body.user_id` (service-role pipeline/`auto-publish`) — espelha `publish-social:38-59`. | `userId` resolvido (não-null) |
| 2 | **Resolve credenciais:** app creds via Resolution order (camada 1 → 2 → 402); user tokens via `social_accounts` WHERE `user_id=userId AND platform='tiktok'`. Ausente → 402 `tiktok_not_configured` + pulse degraded. Token 24h expirado → invocar `refresh-social-token` (re-store rotativo) ou 402 `tiktok_requires_reauth`. | App creds + `access_token` vivo em mãos; senão HTTP 402 (zero chamada à API TikTok) |
| 3 | **Idempotency guard (ANTES do init):** guard keyed em content/run id. Re-init cunha NOVO `publish_id` → double-post. Abortar se já existe `publish_id` para o id. | Guard row/check presente; nenhum init duplicado para o mesmo content/run id |
| 4 | **Creator info pre-flight (OBRIGATÓRIO):** `POST /v2/post/publish/creator_info/query/` (20/min). Ecoar um valor DE `privacy_level_options` (conta não-auditada/privada: só `FOLLOWER_OF_CREATOR`/`MUTUAL_FOLLOW_FRIENDS`/`SELF_ONLY`, sem `PUBLIC_TO_EVERYONE`). **NÃO** setar `disable_comment/duet/stitch=false` quando o respectivo `*_disabled=true`. | HTTP 200 + array `privacy_level_options` não-vazio |
| 5 | **Init upload (FILE_UPLOAD):** `POST /v2/post/publish/video/init/` (6/min) com `post_info{ title ≤2200 runes UTF-16, privacy_level, is_aigc:true [compliance MUST p/ persona IA], brand_content_toggle SÓ se NÃO SELF_ONLY }` + `source_info{ source:'FILE_UPLOAD', video_size, chunk_size, total_chunk_count }`. Chunks 5–64MB · final ≤128MB · <5MB single · 1–1000 chunks. **Supabase signed URL NÃO passa no domain-ownership do PULL_FROM_URL** → FILE_UPLOAD é mandatório. | HTTP 200 + `publish_id` retornado |
| 6 | **PUT chunks:** PUT cada chunk no `upload_url` com header `Content-Range` correto. `upload_url` expirado → 403 → re-init guardado pela idempotency key. | HTTP 2xx por chunk (todos os `total_chunk_count` enviados) |
| 7 | **Poll status:** `POST /v2/post/publish/status/fetch/` (30/min) com backoff até `status='PUBLISH_COMPLETE'`. Persistir envelope `{code,message,log_id}`. `result.id` ← `publicaly_available_post_id` (grafia literal da TikTok; só populado quando público+aprovado). | HTTP 200 + `status='PUBLISH_COMPLETE'` (pré-audit: SELF_ONLY visível ao criador) |
| 8 | **Persistir + mesh + telemetry:** UPDATE `social_accounts`/registro de post com `platform_post_id`; INSERT observation node `mcorch_nodes` (`node_type='observation'`, `name='post:tiktok:<publish_id>'`) + edge `observes` quando houver content node; pulse `infra_health_logs.service='publish-tiktok'` healthy. | Row de post com `platform_post_id` · observation node UUID · pulse `last_seen_at < 1h` |

---

## Verification gates

| Gate | Check | Pass criterion |
|------|-------|----------------|
| G1 | User COM app config + conta conectada → publish | HTTP 200 · `publish_id` → poll `PUBLISH_COMPLETE` · `platform_post_id` persistido |
| G2 | User SEM `social_app_config` (tiktok) → publish | HTTP 402 · body `tiktok_not_configured` · ZERO chamada `video/init/` |
| G3 | Token 24h expirado sem refresh viável → publish | HTTP 402 `tiktok_requires_reauth` · ZERO chamada à API TikTok |
| G4 | RLS isolation | User A não lê/escreve `social_app_config` de User B (REST com JWT de A → 0 rows de B) |
| G5 | Column-grant | `select=client_secret` via JWT (anon/authenticated) → `permission denied` (secret nunca volta ao client) |
| G6 | Telemetria | `infra_health_logs.service='publish-tiktok'` recebe pulse em cada path (healthy/degraded/error) |
| G7 | Idempotência | 2ª invocação para o mesmo content/run id NÃO cunha novo `publish_id` (zero double-post) |
| G8 | Zero global em path user-facing | `grep -i "TIKTOK_CLIENT" publish-social` → app creds vêm de `social_app_config` (env só fallback Sovereign/cron documentado, não fonte primária de tenant) |

---

## Recovery path (por failure mode — §5.1 do blueprint)

| Cenário | Detecção | Recovery (exato) |
|---------|----------|------------------|
| `file_format_check_failed` / `duration_check_failed` / `frame_rate_check_failed` / `picture_size_check_failed` | `fail_reason` no `status/fetch` | Reencode o MP4 9:16 (HyperFrames in-spec: 1080×1920 H.264, 23–60fps, 360–4096px) e re-init com NOVO content/run id (idempotency key nova) |
| `video_pull_failed` | `fail_reason` (PULL_FROM_URL) | Não usar PULL_FROM_URL — Supabase signed URL falha o domain-ownership; forçar `source=FILE_UPLOAD` chunked |
| `auth_removed` | `fail_reason` no poll | Re-autorizar via Login Kit (`social-auth-init`) — **NÃO-automatizável** (humano reconcede); setar flag de reauth, 402 nos próximos publishes |
| `spam_risk_*` | `fail_reason` | Back off para ~15 posts/dia/criador (rate de criador); não retry imediato |
| `publish_cancelled` / `internal` | `fail_reason` | Retry com NOVO content/run id após backoff; persistir `log_id` no envelope |
| `upload_url` 403 (expirado) | PUT do chunk retorna 403 | Re-init `video/init/` **guardado pela idempotency key** (não cunhar publish_id solto) e re-PUT chunks |
| 429 (rate limit) | HTTP 429 | Backoff exponencial capturando `log_id`; respeitar init 6/min · creator_info 20/min · status 30/min |
| Refresh token rotacionado | `refresh-social-token` recebe `refresh_token` diferente | Re-store atômico do NOVO `refresh_token` em `social_accounts` (senão outage em câmera lenta no dia 365); cron diário refresca proativamente antes do expiry de 24h do access_token |
| `social_app_config` lookup erro DB | `console.error` no edge log + pulse `degraded` | Fail-closed (camada 3), nunca publicar sem app cred resolvida |
| Regressão (env global em path de tenant) | G8 falha em grep/CI | Reverter; env TikTok só fallback Sovereign/cron documentado |

---

## Success signal (whole protocol)

- **G1–G8 verdes no smoke** (throwaway users provando 402/RLS/column-grant/idempotência sem custo).
- **PRE-AUDIT (transporte provado, Lei 1):** `status='PUBLISH_COMPLETE'` em `SELF_ONLY` visível ao criador no app TikTok — prova que FILE_UPLOAD + create→poll→publish funciona E2E. **NÃO** afirmar "ao vivo / público".
- **POST-AUDIT (afirmação honesta de "ao vivo"):** URL público `tiktok.com` resolvível, populado em `publicaly_available_post_id` — única afirmação honesta de publicação ao vivo. Requer o audit (gate Sovereign abaixo) passado.
- `publish-social` (branch TikTok) deployado (script size + ACTIVE em `supabase functions list`).
- Migration `social_app_config` aplicada (aprovada por `/security-review`).
- `infra_health_logs.service='publish-tiktok'` com pulses recentes (`last_seen_at < 1h` pós-smoke).

---

## Audit / app-registration gate (Sovereign action — CAMINHO CRÍTICO, lead-time de semanas)

> **Sem o registro do app não há `client_key`/`client_secret` → nenhum OAuth começa.** Esses são blockers DUROS 100% fora do código. Começar HOJE — o audit tem o maior lead-time.

| # | Ação Sovereign | Destrava | Lead-time |
|---|----------------|----------|-----------|
| 1 | Registrar app no TikTok Developer Portal + habilitar **Content Posting API (Direct Post)** + scope `video.publish` + **adicionar a conta da persona como sandbox target user** | `client_key`/`client_secret` (→ `social_app_config` ou env fallback) + teste E2E pré-audit (SELF_ONLY) | horas–2 dias |
| 2 | Submeter o **TikTok Content Posting API audit** (usage-estimates + walkthrough/screencast de UX compliant) | posts **PÚBLICOS** — levanta o teto SELF_ONLY + conta privada + ≤5 users/24h | **~2–6 semanas (sem SLA)** |

**Gate de materialidade (Lei 1):** enquanto o audit não passa, a conta é forçada a `SELF_ONLY`/privada (≤5 users em 24h, sem `PUBLIC_TO_EVERYONE` em `privacy_level_options`). O transporte é provável (PRE-AUDIT success), mas **nenhuma afirmação de "publicado ao vivo" é honesta até o audit aprovar** e um `publicaly_available_post_id` resolver num URL público `tiktok.com`.

---

## Telemetry — `infra_health_logs` (`service='publish-tiktok'`)

Pulse em **todo path**, espelhando `publish-meta` (FR-META-009) e o padrão de telemetria do §6:

| Path | `status` | `event` / `reason` | `metadata` (allowlist — NÃO vazar per-tenant na tabela global-read) |
|------|----------|--------------------|---------------------------------------------------------------------|
| Publish OK | `healthy` | `event='publish_complete'` | `{ platform:'tiktok', step:'status_fetch', privacy_level }` (sem token, sem open_id) |
| Sem config / token morto | `degraded` | `reason='no_config'` / `reason='requires_reauth'` | `{ platform:'tiktok', stage:'resolve' }` |
| `fail_reason` da TikTok | `degraded` | `reason=<fail_reason>` (ex: `file_format_check_failed`) | `{ platform:'tiktok', step:'status_fetch', log_id }` |
| Rate limit 429 | `degraded` | `reason='rate_limited'` | `{ platform:'tiktok', step:<init\|status>, log_id }` |
| Erro inesperado (5xx / exceção) | `error` | `event='publish_error'` | `{ platform:'tiktok', step, log_id }` |

A telemetria é o sinal monitorado dos gates de materialidade (Pattern: Goal Setting & Monitoring). O envelope `{code,message,log_id}` da TikTok é persistido para diagnóstico — `log_id` é a chave de correlação com o suporte TikTok.

---

## Media transfer note — FILE_UPLOAD chunked (NÃO PULL_FROM_URL)

O TikTok oferece dois modos de transferência: `PULL_FROM_URL` e `FILE_UPLOAD`. **Esta SOP exige FILE_UPLOAD chunked** por uma razão material verificada (§3):

- **`PULL_FROM_URL` falha** — exige **domain-ownership verification** do host do vídeo no TikTok Developer Portal. Uma Supabase signed URL (host `*.supabase.co`, TTL curto) **NÃO passa** nessa verificação → `fail_reason='video_pull_failed'`. Verificar o domínio seria mais um passo Sovereign-gated.
- **`FILE_UPLOAD` desacopla** do domain verification e funciona direto do bucket privado `video-studio-assets`: o edge fn lê os bytes do MP4, fatia em chunks (5–64MB, final ≤128MB, total ≤128MB, 1–1000 chunks; <5MB = single chunk) e faz PUT de cada um no `upload_url` com `Content-Range`. O binário é **enviado** (push), nunca puxado.
- **Mídia in-spec:** o MP4 9:16 1080×1920 H.264 do HyperFrames (`video-studio-assets`, NFR-VS-016) está dentro do envelope TikTok (360–4096px, 23–60fps) — reuso verbatim, sem reencode no caminho feliz.

Decisão registrada no blueprint §7 #2 (FILE_UPLOAD vence verificar-domínio).

---

## Anti-patterns prohibited

- ❌ `Deno.env.get('TIKTOK_CLIENT_KEY'/'TIKTOK_CLIENT_SECRET')` como fonte **primária** de app creds em fluxo user-facing (só fallback Sovereign/cron documentado com OTD-SOCIAL-APP-ENV + SLA).
- ❌ Usar scope `video.upload` (draft-to-inbox, exige humano no app) em vez de `video.publish` (Direct Post autônomo).
- ❌ Scope separado por **espaço** no authorize URL (falha o consent em silêncio) — usar **vírgula**.
- ❌ Re-init `video/init/` sem idempotency guard (cunha novo `publish_id` → double-post).
- ❌ Setar `brand_content_toggle=true` ou `PUBLIC_TO_EVERYONE` enquanto não-auditado (SELF_ONLY) — incompatível, falha o publish.
- ❌ Omitir `is_aigc=true` em conteúdo de persona IA (compliance MUST, não opcional).
- ❌ Sobrescrever um `refresh_token` bom com null/stale após rotação (quebra a cadeia → re-OAuth forçado).
- ❌ Retornar `client_secret` ou `access_token` ao client (column-grant REVOKE + masked VIEW obrigatórios).
- ❌ Resolver `social_app_config`/`social_accounts` sem filtrar `user_id` do dono (vazamento cross-tenant).
- ❌ Afirmar "publicado ao vivo" com base num `PUBLISH_COMPLETE` pré-audit (é SELF_ONLY — não há URL público).

---

## Known debt

- **OTD-SOCIAL-APP-ENV:** app creds via env (`TIKTOK_CLIENT_KEY`/`TIKTOK_CLIENT_SECRET`) é default Sovereign-only de onboarding para a probe-phase single-tenant (Usuário Zero). **Critério de fechamento:** promover a `social_app_config` per-user + UI Settings ANTES do 2º tenant. Registrar SLA no seal. (Tokens per-user já vão para `social_accounts` desde o dia 1.)
- **OTD-META-ENCRYPT (herdada):** `social_app_config.client_secret` e os tokens de `social_accounts` seguem o mesmo regime de cifragem-at-rest do projeto inteiro (Vault/column-REVOKE hoje; pgsodium AES-256-GCM é dívida cross-tabela). Cifrar só uma tabela seria teatro enquanto a mesma classe de segredo vaza por outra.

---

## Connection to Survival Laws

- **Lei 1 (Materialidade):** cada gate produz prova material (HTTP status + body + `social_accounts`/post UUID + `publish_id` + `PUBLISH_COMPLETE` + pulse + REST permission-denied). PRE-AUDIT prova transporte; POST-AUDIT URL público é a única afirmação honesta de "ao vivo".
- **Lei 2 (Anticipated Process):** este SOP escrito ANTES do código (requisito API Tenancy item 5 + PASSO 0 do fatiamento §8).
- **Lei 3 (Pruning):** resolução stateless por request; nada acumulado além da idempotency guard keyed por content/run id.
- **Lei 4 (ORO):** triplet declarado acima; Reviewer = Sovereign aprova migration + smoke + autoriza ir-público pós-audit.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

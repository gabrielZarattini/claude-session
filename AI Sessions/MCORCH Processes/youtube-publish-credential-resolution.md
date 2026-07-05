# SOP: YouTube Publish Credential Resolution (Per-User)

**Status:** ACTIVE · v1.0 · 2026-06-27
**Owner:** Sovereign (Gabriel Zarattini)
**Survival Law 2 compliance:** Escrita ANTES do código do branch `youtube` em `supabase/functions/publish-social/index.ts` + branches `social-auth-init`/`social-auth-callback`/`refresh-social-token` + migration `social_app_config` (requisito explícito da diretiva API Tenancy item 5).
**Canonical directive:** `CLAUDE.md > Architecture > "API Tenancy Model — Per-User Credentials"`
**Source of Truth (blueprint):** `.claude/context/social-connect-3platforms-blueprint-2026-06-27.md` §2.2 · §3 · §5.2 · §6
**BoK gate:** `docs/bok/post-engine/` (emenda bloqueante PASSO 0 — scopes `youtube.upload` · audit gates A+B · refresh não-rotativo · Pattern Conformance §4 do blueprint). Este SOP é a Fonte da Verdade do branch enquanto a emenda do BoK não sela.

---

## Context

A publicação de Shorts no YouTube usa a **Data API v3 `videos.insert`** com upload **resumable** (sem ingest remoto: o MP4 9:16 1080×1920 do HyperFrames é buscado da signed URL do bucket privado `video-studio-assets` e enviado via `PUT`). A autenticação é **OAuth 2.0 do Google** — cada criador conecta o seu próprio canal Brand (a persona Gabriel AI / CCIO). Os **tokens por-usuário** (access + refresh + scopes + `channel_id`) vão para `social_accounts` (VIEW Vault-mascarada já existente). As **credenciais de app** (`client_id` / `client_secret` do projeto Google Cloud) resolvem-se por uma nova tabela per-user `social_app_config`.

`publish-social` é invocada pelo `PublishNode` do pipeline de orquestração e pelo cron `auto-publish`. O branch `youtube` DEVE resolver as credenciais de app por `user_id` do **dono do conteúdo** (per-user antes de env global), e os tokens OAuth da linha `social_accounts WHERE platform='youtube'` do mesmo dono — nunca um app credential global compartilhado em fluxo user-facing.

**Por que importa (multi-tenant readiness):** controle de canal isolado por tenant · atribuição de receita correta por publicação · quota da `videos.insert` segregada por app/tenant (um user não esgota o cap diário do outro) · LGPD (cada user controla/revoga sua credencial Google) · anti-fraude (um user não publica no canal de outro) · blast radius de credencial roubada confinado a um tenant.

**Particularidade YouTube vs Meta:** o refresh token do Google **só vem na 1ª autorização** (ou re-consent forçado com `prompt=consent`) e o Google geralmente **NÃO rotaciona** refresh tokens não-DPoP. Logo: `access_type=offline`+`prompt=consent` no init, e **NUNCA sobrescrever um refresh token bom com `null`** numa resposta de refresh que não traga refresh.

---

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (build do branch) + Edge runtime `publish-social` (execução) + **Sovereign** (registro do app Google Cloud + criação do canal Brand + submissão dos 2 audits — caminho crítico fora do código, §6 do blueprint).
- **Reviewer:** Sovereign (Gabriel) — aprova migration `social_app_config` via `/security-review` + valida o smoke.
- **Owner:** Sovereign — blast radius = controle de canal YouTube por tenant + atribuição de receita por publicação + tokens OAuth de longa duração + quota `videos.insert`.

---

## Operator (quem executa manualmente hoje)

- **Sovereign (ação fora do código — caminho crítico):** registra o app no Google Cloud (`client_id`/`client_secret`), cria/converte o canal Brand Gabriel AI / CCIO, e submete os **2 audits** (verification de scope sensível + API Audit & Quota Extension). Sem isso não há credencial de app nem upload público — ver §"App-registration / Audit gate".
- **Usuário Zero / cliente:** configura as credenciais de app em `/dashboard/settings` (card "YouTube Integration", hook TanStack Query `useSocialAppConfig` → upsert `social_app_config` com `platform='youtube'` + `client_id` + `client_secret` + `scopes`). Modelo BYOK, idêntico ao fluxo de `meta_config`/`user_api_keys`. O fluxo OAuth (`social-auth-init`/`social-auth-callback`, branch `youtube`) popula `social_accounts` com os tokens + `metadata.channel_id`.
- **Edge function `publish-social` (branch youtube):** resolve o app credential por request e os tokens do dono, e publica no canal do dono do conteúdo.

---

## Resolution order — app credentials (canonical — espelha API Tenancy Model)

> **Escopo:** esta ordem resolve as **credenciais de APP** (`client_id`/`client_secret`). Os **tokens OAuth por-usuário** vivem sempre em `social_accounts` (camada per-user única — não há fallback de token).

| # | Camada | Fonte (nomes exatos) | Permitido em |
|---|--------|----------------------|--------------|
| 1 | **Per-user** | `social_app_config` WHERE `user_id = <owner>` AND `platform = 'youtube'` AND `is_active = true` → `client_id` + `client_secret` (+ `scopes`, `metadata.channel_id`) | SEMPRE (caminho primário) |
| 2 | **Global vault fallback** | `Deno.env.get('GOOGLE_CLIENT_ID')` + `Deno.env.get('GOOGLE_CLIENT_SECRET')` | **APENAS** como default Sovereign-only de onboarding do Usuário Zero (single-tenant, slices probe). **OTD registrada com SLA** (ver "Known debt"). Promover a per-user antes do 2º tenant. NUNCA uma shared key silenciosa. |
| 3 | **Hard failure** | — | HTTP 402/501 `{ error: "youtube_not_configured", action: "Configure your YouTube credentials at /dashboard/settings" }` · pulse `infra_health_logs status=degraded reason=no_config` |

**Token resolution (per-user, sem fallback):** `social_accounts WHERE user_id = <owner> AND platform = 'youtube'` → `access_token` (válido por ~3600s) + `refresh_token` + `token_expires_at` + `metadata.channel_id`. Se ausente → 402 `youtube_not_connected` (camada 3). Se `token_expires_at < now()` → refrescar (`refresh-social-token` branch youtube) antes de publicar; se o refresh falhar com `invalid_grant` → 402 `youtube_requires_reauth` (camada 3), nunca publicar com token morto.

**Owner resolution:** o request traz `user_id` (JWT do frontend OU `body.user_id` em chamada service-role do pipeline/cron). A receita/publicação pertence ao **dono do conteúdo** (espelha `publish-social:38-59`).

---

## Schema — `social_app_config` (decisão autoritativa)

> **Decisão (overrides o blueprint §2.3/§7-#1 que sugeria `youtube_config`/`tiktok_config`/`pinterest_config` separados):** uma **única** tabela per-user `social_app_config` chaveada `UNIQUE(user_id, platform)` cobre as 3 plataformas de app-credentials. Tokens OAuth continuam em `social_accounts` (zero migration de enum — `social_platform` já tem `youtube`).

| Coluna | Tipo | Nota |
|--------|------|------|
| `id` | `uuid` PK `default gen_random_uuid()` | |
| `user_id` | `uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE` | dono do tenant |
| `platform` | `social_platform NOT NULL` | enum vivo (`youtube`/`tiktok`/`pinterest`/…) |
| `client_id` | `text` | app id (não sensível, mas escopado per-user) |
| `client_secret` | `text` | **token-class** — column-level `REVOKE SELECT … FROM anon, authenticated` (espelha `meta_config.long_lived_token`); service_role lê para o code→token exchange |
| `scopes` | `text[] NOT NULL DEFAULT '{}'` | YouTube: `{'https://www.googleapis.com/auth/youtube.upload'}` |
| `metadata` | `jsonb NOT NULL DEFAULT '{}'` | YouTube: `{ channel_id }` · Pinterest: `{ board_id }` |
| `is_active` | `boolean NOT NULL DEFAULT true` | resolução camada 1 filtra `is_active = true` |
| `created_at` / `updated_at` | `timestamptz` | trigger `update_updated_at_column()` |

**Hardening (espelha `meta_config` / `social_accounts`):**
- RLS default-deny: `CREATE POLICY … FOR ALL USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id)`.
- `CONSTRAINT unique_user_platform UNIQUE (user_id, platform)`.
- Column-level: `REVOKE SELECT (client_secret) ON public.social_app_config FROM anon, authenticated;` — o secret nunca volta ao client; o card de Settings seleciona colunas seguras explícitas.
- **Masked VIEW + INSTEAD OF tenant-guard trigger** no padrão `social_accounts`/`meta_config` (`auth.uid() = user_id` no INSTEAD OF; `service_role` isento), para escrita BYOK do secret sem expor o valor no SELECT mascarado. Guard de tenant idêntico ao da migration `20260602150000_meta_social_instead_of_tenant_guard.sql` (impede injeção cross-tenant com id-novo).
- `/security-review` obrigatório antes do commit da migration (FMEA-011 — cross-tenant data leak).

---

## App-registration / Audit gate (Sovereign action — lead-time de semanas)

> **Sem o registro do app não há `client_id`/`secret` → nenhum OAuth começa. Os 2 audits são SERIAIS + independentes → prontidão pública = a SOMA (~10d + semanas), não o máximo. Submeter ambos no dia 1.** (blueprint §6, ações #3–#5.)

| # | Ação Sovereign | Destrava | Lead-time |
|---|----------------|----------|-----------|
| G-A0 | Criar/converter o canal YouTube Gabriel AI / CCIO no Brand Account correto | alvo do upload (`channels?mine=true` retorna o id) | minutos |
| G-A | **OAuth consent verification** (Google Cloud) p/ o scope sensível `youtube.upload` + mover o app de **Testing → In production** | tira o warning de unverified app + **mata o expiry de 7 dias do refresh token** (em Testing o refresh expira em 7d → `invalid_grant` no dia 8) | **~10 dias** |
| G-B | Submeter o **YouTube API Services Audit & Quota Extension Form** | uploads **PÚBLICOS** — sem ele, projeto não-verificado **FORÇA todo upload a `private`** ignorando o `privacyStatus:'public'` pedido | semanas (sem SLA) |

**Materialidade (Lei 1):** enquanto G-B não passa, um `201` da `videos.insert` é transporte provado mas o vídeo nasce `private`. **NÃO afirmar "publicado ao vivo / público"** até `videos.get?part=status` retornar `privacyStatus == 'public'`. Em **Testing** (G-A não passou), o refresh token expira em 7d — o fix é o gate A, **não** um retry-loop.

---

## Sequence (`publish-social` branch youtube) — Lei 2

Padrão **fetch-bytes → resumable PUT** (sem `PULL_FROM_URL` — o YouTube não tem ingest remoto).

| # | Step | Critério de sucesso MATERIAL (artefato real) |
|---|------|----------------------------------------------|
| 1 | **Auth & owner:** validar `Authorization: Bearer`; resolver `userId` via `auth.getUser()` (JWT frontend) OU `body.user_id` (service-role pipeline/cron) — espelha `publish-social:38-59`. | `userId` resolvido (UUID não-nulo); request 401 quando ausente. |
| 2 | **Resolve app credential (camada 1→2→3):** `social_app_config` WHERE `user_id`+`platform='youtube'`+`is_active` → `client_id`/`client_secret`; senão env `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET` (Sovereign-only default); senão **402 `youtube_not_configured`**. | `client_id`/`client_secret` em mãos **OU** HTTP 402 body `youtube_not_configured` + pulse `degraded`. |
| 3 | **Resolve tokens (per-user):** `social_accounts` WHERE `user_id`+`platform='youtube'` → `access_token`+`refresh_token`+`token_expires_at`+`metadata.channel_id`. Ausente → 402 `youtube_not_connected`. | linha `social_accounts` lida (`SELECT id` = UUID) **OU** 402 `youtube_not_connected`. |
| 4 | **Refresh gate:** se `token_expires_at < now()` → `refresh-social-token` branch youtube (`POST https://oauth2.googleapis.com/token` `grant_type=refresh_token`) → novo `access_token`+`expires_in`; `token_expires_at = now()+3600`. **NUNCA** sobrescrever o `refresh_token` armazenado com `null`; tolerar um novo só se a resposta trouxer um. `invalid_grant` → 402 `youtube_requires_reauth`. | novo `access_token` + `token_expires_at` persistidos (UPDATE 1 row) **OU** 402 `youtube_requires_reauth`. |
| 5 | **Fetch media bytes:** `GET` da signed URL do bucket privado `video-studio-assets` (resolvida pelo dispatch / `auto-publish`) → buffer do MP4. | HTTP 200 + `Content-Length` ≥ ~100 KB (rejeitar stub JSON de erro). |
| 6 | **Initiate resumable session:** `POST https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status` headers `Authorization: Bearer <access_token>`, `X-Upload-Content-Length:<bytes>`, `X-Upload-Content-Type: video/mp4`; body `{ snippet:{ title, description, tags, categoryId:'22' }, status:{ privacyStatus:'public', selfDeclaredMadeForKids:false, containsSyntheticMedia:true } }`. | HTTP 200 + header `Location` (session URI) capturado. |
| 7 | **PUT bytes:** `PUT` no session URI em chunks múltiplos de 256 KB com `Content-Range`. `308` (Resume Incomplete) → retomar do byte do header `Range` (tolerar `Range` AUSENTE = restart do byte 0; session URI expira ~1 semana = re-iniciar). | cada chunk → `308`/`200`; chunk final → **`201`** com video resource id (`result.id`). |
| 8 | **Materiality probe (Lei 1 — NÃO um 201 cru):** `GET https://www.googleapis.com/youtube/v3/videos?id=<videoId>&part=status` → ler `status.privacyStatus`. | `privacyStatus == 'public'` (gates A+B passados) **OU** `'private'` (transporte provado, audit pendente — declarar só "upload aceito", não "público"). |
| 9 | **Persistir:** INSERT em `social_accounts`-adjacent / tabela de posts (`platform`, `platform_post_id=<videoId>`, `post_url='https://youtube.com/shorts/<videoId>'`, `status`, `user_id`). Shorts é IMPLÍCITO (1080×1920 + ≤3min auto-classifica). | row de post (`SELECT id` = UUID) com `platform_post_id` não-nulo. |
| 10 | **Mesh observation:** INSERT `mcorch_nodes` (`node_type='observation'`, `name='post:youtube:<videoId>'`, `user_id`) + `mcorch_edges` (`relation_type='observes'`, `target_id=<content node>`) quando houver content node de origem. Autoembed via trigger. | `mcorch_nodes.id` = UUID retornado. |
| 11 | **Telemetry:** pulse `infra_health_logs.service='publish-youtube'` em todo path (`healthy`/`degraded`/`error`). | `infra_health_logs` row com `last_seen_at` recente. |
| 12 | **Return:** `{ success, post: { platform:'youtube', video_id, post_url, privacy_status } }`. | corpo JSON com `privacy_status` ecoando o step 8. |

---

## Verification gates

| Gate | Check | Pass criterion (material) |
|------|-------|---------------------------|
| G1 | User COM app config + conectado → publish | HTTP `201` + video id + `videos.get` `privacyStatus` (não bare 201) + row de post (UUID) |
| G2 | User SEM app config → publish | HTTP 402 · body `youtube_not_configured` · ZERO chamada à `videos.insert` |
| G3 | User não-conectado (sem `social_accounts`) → publish | HTTP 402 · body `youtube_not_connected` · ZERO chamada à `videos.insert` |
| G4 | Token expirado, refresh `invalid_grant` → publish | HTTP 402 `youtube_requires_reauth` · ZERO chamada à `videos.insert` (não publicar com token morto) |
| G5 | RLS isolation | User A não lê/escreve `social_app_config` de User B (REST com JWT de A → 0 rows de B) |
| G6 | Column-grant | `select=client_secret` via JWT (anon/authenticated) → `permission denied` (secret nunca volta ao client) |
| G7 | Materialidade público (Lei 1) | Antes de afirmar "público": `videos.get?part=status` `privacyStatus == 'public'` E `youtube.com/shorts/<id>` resolve. Projeto não-auditado → `private` → halt na afirmação. |
| G8 | Telemetria | `infra_health_logs.service='publish-youtube'` recebe pulse em cada path |
| G9 | Zero global em path user-facing | `client_secret` resolvido de `social_app_config` quando o user tem config; env `GOOGLE_CLIENT_SECRET` só dispara no fallback Sovereign-only (OTD registrada) |

---

## Recovery path (por failure mode — blueprint §5.2)

| Cenário | Detecção | Recovery (exato) |
|---------|----------|------------------|
| `308` Resume Incomplete no PUT | resposta `308` com header `Range` | retomar o `PUT` do byte indicado em `Range` (`Content-Range: bytes <next>-…/<total>`) |
| `Range` AUSENTE no `308` | `308` sem header `Range` | **restart do byte 0** (reenviar o arquivo inteiro na mesma session URI) |
| Session URI expirada (~1 semana) | `404`/`410` no PUT | **re-iniciar** a sessão resumable (novo step 6) e re-PUT |
| `invalid_grant` no refresh | resposta `invalid_grant` de `oauth2.googleapis.com/token` | app ainda em **Testing** (refresh expira 7d) → escalar o **gate A** (In production); **não** retry-loop. Setar 402 `youtube_requires_reauth` + UI banner de re-conexão |
| Forced-private apesar de `privacyStatus:'public'` | `videos.get` retorna `private` mesmo com `201` | o **gate B** (API Audit & Quota Extension) não passou → **halt** em qualquer afirmação de "público"; manter "upload aceito (private)" até o email de aprovação |
| Refresh response sem `refresh_token` | corpo do refresh sem `refresh_token` | **NÃO** anular o `refresh_token` armazenado — manter o existente (Google não rotaciona não-DPoP) |
| Quota diária `videos.insert` esgotada | `403 quotaExceeded` | back off até a janela diária resetar; **ler a Quota Calculator viva** (o modelo de bucket é móvel; Dec-2025 caiu de ~1600 → ~100 units/call) — não hardcodar o cap |
| Bytes inválidos (stub de erro) | `Content-Length` < ~100 KB no fetch | rejeitar o upload (não enviar JSON de erro como vídeo); re-resolver/assinar a `media_url` |
| `social_app_config` lookup erro DB | `console.error` no edge log + pulse `degraded` | fail-closed (camada 3), nunca publicar sem app credential resolvido |
| Regressão (env global reintroduzido como primário) | G9 falha em smoke/CI | reverter; env só no fallback Sovereign-only com OTD/SLA |

---

## Success signal (whole protocol — Lei 1 materiality gate)

A afirmação honesta de **"publicado ao vivo"** exige **TODAS** as condições — um bare `201` **NÃO** basta:

- video id retornado pelo `201` da `videos.insert`, **E**
- `videos.get?part=status` retorna **`privacyStatus == 'public'`** (prova que gates A+B passaram), **E**
- a URL `https://youtube.com/shorts/<videoId>` resolve.

Pré-audit (G-B pendente): o sinal honesto é **"upload aceito, `private`"** (transporte resumable provado E2E) — **nunca** "público".

Além disso, para selar a feature:
- branch `youtube` do `publish-social` deployado (script size + ACTIVE em `supabase functions list`).
- Migration `social_app_config` aplicada (aprovada por `/security-review`).
- `infra_health_logs.service='publish-youtube'` com pulses recentes (`last_seen_at` < 1h pós-smoke).
- G1–G9 verdes no smoke.

---

## Telemetry (`infra_health_logs.service='publish-youtube'`)

Pulse em **todo** path (chokepoint único, espelha `publish-meta`):

| Path | `status` | `reason` / `event` | Quando |
|------|----------|---------------------|--------|
| Sucesso público | `healthy` | `event='youtube_publish_public'`, `metadata={ video_id, privacy_status:'public' }` | step 8 retorna `public` |
| Sucesso transporte (private) | `degraded` | `reason='forced_private_pending_audit'` | `201` mas `privacyStatus='private'` (gate B pendente) |
| Sem app config | `degraded` | `reason='no_config'` | camada 3, 402 `youtube_not_configured` |
| Não-conectado | `degraded` | `reason='not_connected'` | 402 `youtube_not_connected` |
| Reauth necessário | `degraded` | `reason='requires_reauth'` | `invalid_grant` no refresh, 402 `youtube_requires_reauth` |
| Quota esgotada | `degraded` | `reason='quota_exceeded'` | `403 quotaExceeded` |
| Erro de upload / API 5xx | `error` | `event='youtube_publish_error'`, `metadata={ http_status, log }` | falha do PUT / `videos.insert` |

> A allowlist de telemetria no chokepoint NÃO deve vazar `client_secret`/`access_token`/`refresh_token` na `infra_health_logs` (tabela global-read) — só ids/status/reason (espelha `20260615170000_infra_health_logs_metadata.sql`).

---

## Media transfer note (resumable PUT — sem ingest remoto)

O YouTube **não** tem ingest remoto (não existe `PULL_FROM_URL` na `videos.insert`). O fluxo é **fetch-then-PUT**:

1. `auto-publish` / dispatch resolve e **assina** a `content_library.media_url` (signed URL de TTL longo, horas) do bucket privado `video-studio-assets`.
2. O branch `youtube` faz `GET` dessa signed URL → buffer de bytes (valida `Content-Length` ≥ ~100 KB).
3. `PUT` resumable dos bytes no session URI capturado do header `Location`, em chunks múltiplos de **256 KB** com `Content-Range`, retomando do `Range` em `308`.

A signed URL precisa de TTL suficiente para o fetch + upload completos; um TTL curto pode expirar no meio do PUT de um arquivo grande. (Diferente do TikTok FILE_UPLOAD chunked e do Pinterest register→multipart — cada plataforma tem o seu transporte; ver blueprint §3.)

---

## Anti-patterns prohibited

- ❌ `Deno.env.get('GOOGLE_CLIENT_SECRET')` como fonte **primária** em publish user-facing (só fallback Sovereign-only com OTD/SLA).
- ❌ Afirmar "publicado / público" com base num bare `201` sem o `videos.get` `privacyStatus == 'public'` (Lei 1).
- ❌ Sobrescrever um `refresh_token` bom com `null` numa resposta de refresh sem refresh (Google não rotaciona não-DPoP → mata a conexão).
- ❌ OAuth init sem `access_type=offline`+`prompt=consent` (re-auth devolve `refresh_token` NULO em silêncio).
- ❌ Retornar `client_secret`/`access_token`/`refresh_token` ao client (column-REVOKE + safe-columns obrigatório).
- ❌ Resolver `social_app_config` sem filtrar `user_id`+`platform` do dono (vazamento cross-tenant).
- ❌ Publicar com token expirado/`invalid_grant` (upload falha; nunca publicar com token morto).
- ❌ Compartilhar app credential Google de um user com outro via env global silencioso (fraude por design + quota cruzada).

---

## Known debt

- **OTD-SOCIAL-APP-ENV-FALLBACK** (SLA: antes do 2º tenant): o fallback env `GOOGLE_CLIENT_ID`/`GOOGLE_CLIENT_SECRET` é default Sovereign-only de onboarding do Usuário Zero (single-tenant, slices probe — blueprint §7-#1). Critério de fechamento: todo tenant tem app credential em `social_app_config` (camada 1) + UI Settings que escreve o secret; remover o ramo env do branch `youtube` do path user-facing.
- **OTD-META-ENCRYPT** (project-wide): `client_secret` em `social_app_config` é gravado como TEXT plaintext protegido por RLS + column-REVOKE, consistente com `meta_config.long_lived_token` / `social_accounts.access_token` / `user_api_keys`. Cifragem-at-rest (pgsodium/Vault) é dívida do projeto inteiro; cifrar só `social_app_config` seria teatro. Critério: pgsodium habilitado + colunas de credencial migradas em TODAS as tabelas.

---

## Connection to Survival Laws

- **Lei 1 (Materialidade):** cada gate produz prova material (HTTP status + body + `videos.get` `privacyStatus` + row de post + pulse + REST permission-denied). O success signal é o `privacyStatus == 'public'`, **não** um 201 cru.
- **Lei 2 (Anticipated Process):** este SOP escrito ANTES do código do branch `youtube` + migration `social_app_config` (requisito API Tenancy item 5).
- **Lei 3 (Pruning):** resolução stateless por request; nada acumulado.
- **Lei 4 (ORO):** triplet declarado acima; Reviewer = Sovereign aprova migration + smoke; Owner absorve o blast radius de canal/quota/atribuição.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

# SOP — Publish WordPress per-user atrás do Cloudflare (multi-tenant)

> **Slug:** `wordpress-cf-per-user-publish` · **Criado:** 2026-06-22 · **Lei 2 (Processo Antecipado)** · **API Tenancy Model — Per-User Credentials**
> **Origem:** diretiva Sovereign 2026-06-22 — *"o que resolvemos do WP com CF agora deve ser per-user dentro do ecossistema; se o usuário precisar adicionar uma regra no Cloudflare, devemos deixar explícito e claro na UI do painel para o usuário fazer o passo correto"* + *"tudo que é per-user sempre é prioridade ser resolvido per-user"*.
> **Generaliza** o unblock **global/tenant-zero** já vivo (`docs/processes/wordpress-cf-publish-unblock.md`, secret global `WP_PUBLISH_SECRET`/`_HOST` → `www.mcorch.com`) para **qualquer tenant** cujo WordPress self-hosted esteja atrás do **próprio** Cloudflare.

---

## Problema

O unblock atual é **single-tenant**: um único `WP_PUBLISH_SECRET` global bound a `WP_PUBLISH_SECRET_HOST=www.mcorch.com` (o site do Usuário Zero). Quando o Usuário 1+ conecta o **próprio** WP (`user_api_keys.wp_site_url` ≠ `www.mcorch.com`), atrás do **próprio** Cloudflare, o `publish-wordpress` faz `fetch` server-side (Deno, sem engine JS) e morre no **managed challenge** do CF *daquele* tenant → publish 502. Estender o secret global a hosts de tenant é **proibido** (o segredo de skip do CF do MCORCH é bound a UMA origem nossa; mandá-lo a um host escolhido pelo tenant permitiria replay/exfil — ver fail-closed em `publish-wordpress/index.ts:80-99`).

## Modelo da solução (per-user, fail-closed)

Cada tenant que tem WP atrás do próprio Cloudflare ganha o **seu próprio segredo compartilhado**, guardado **cifrado por-usuário** no Vault, e a **UI o guia** a criar a regra de WAF Skip correta no **Cloudflare dele** — com a expressão e o segredo **dele** já preenchidos.

**Resolution order (API Tenancy Model):**
1. **Per-user primeiro** — `decrypted_user_api_keys.wp_cf_publish_secret` (do `user_id`). Anexa `X-MCORCH-Publish: <segredo-do-tenant>` **somente** quando o host de destino == host do `wp_site_url` **do próprio tenant** (sempre é — publicamos no site dele; o segredo nunca viaja para outro host).
2. **Global fallback restrito** — `Deno.env.get('WP_PUBLISH_SECRET')` SÓ quando o host de destino == `WP_PUBLISH_SECRET_HOST` (= `www.mcorch.com`, tenant-zero / onboarding default documentado).
3. **No-op fail-closed** — sem secret per-user e host ≠ tenant-zero ⇒ **header nunca é anexado** (o publish segue sem o skip; correto se o WP do tenant **não** está atrás de um CF que desafia).

**Segurança:** o segredo per-user é do **próprio** tenant, bound ao **próprio** host → zero exfil cross-tenant. Cifrado em repouso como qualquer BYOK (`wp_app_password`). É **retrievable** (a edge fn precisa replayá-lo como header) — diferente de um PAT (hash-only); portanto a UI o exibe na geração e a rotação = re-gerar.

---

## ORO

- **Operator:** MCORCH Master Execution Agent (migration + edge fn + UI) **+ o TENANT** (cria a regra de WAF Skip no Cloudflare **dele**, na conta CF dele).
- **Reviewer:** `/security-review` independente (migration + edge fn) + Sovereign.
- **Owner:** Sovereign — blast radius = publish multi-tenant + manuseio de segredo per-user + isolamento entre tenants. (O Owner da regra CF de cada tenant é o próprio tenant.)

---

## Sequence (passos numerados, cada um com critério material)

### Step 1 — Schema: coluna per-user cifrada `wp_cf_publish_secret`
Migration adicionando a coluna ao **backing table** do `user_api_keys` (VIEW mascarada Vault — ver `reference_encrypted_views_write_pattern`), com:
- Trigger de encriptação Vault idempotente (padrão `vault_upsert_secret`, migration `20260602140000`) — re-save não dá 23505.
- VIEW mascarada expõe `wp_cf_publish_secret` como `••••`; `decrypted_user_api_keys` expõe o claro (só service_role).
- INSTEAD OF trigger **UPDATE-first** + guard de tenant `auth.uid()` (padrão migrations `20260602130000`/`150000` — NUNCA `INSERT...ON CONFLICT` [double-fire] nem injeção cross-tenant).
- `/security-review` **obrigatório** antes do commit (FMEA-011).

**Sucesso material:** `db push` exit 0; `SELECT wp_cf_publish_secret FROM user_api_keys` mostra `••••`; service-role `SELECT ... FROM decrypted_user_api_keys` retorna o claro; INSERT por JWT de outro tenant → 42501.

### Step 2 — Edge fn `publish-wordpress`: lookup per-user
Estender o gate de host (`publish-wordpress/index.ts:90-99`) para a resolution order acima:
```
const perUser = userKeys?.wp_cf_publish_secret;            // já vem do decrypted_user_api_keys select
const targetHost = new URL(apiBase).hostname.toLowerCase();
if (perUser && targetHost === new URL(wpSiteUrl).hostname.toLowerCase()) {
  wpAuthHeaders["X-MCORCH-Publish"] = perUser;             // per-user: segredo do tenant → host do tenant
} else if (wpPublishSecret && wpPublishSecretHost && targetHost === wpPublishSecretHost.toLowerCase()) {
  wpAuthHeaders["X-MCORCH-Publish"] = wpPublishSecret;     // fallback restrito: tenant-zero
}                                                          // senão: nada (fail-closed)
```
Adicionar `wp_cf_publish_secret` ao `.select()` do `decrypted_user_api_keys` (linha ~53). Telemetria `infra_health_logs` service `wordpress-cf-publish` com path (`per_user` / `global_fallback` / `no_secret`).

**Sucesso material:** deploy com script size; boot-smoke 401 sem auth; um tenant ≠ zero com secret per-user + host próprio → header anexado (provado pelo Step 4).

### Step 3 — UI: Settings → WordPress → seção "Cloudflare" (guia explícito)
Hook `useWpCloudflare` (TanStack Query) + card em `MetaConfigCard`-style:
- Toggle **"Meu WordPress está atrás do Cloudflare"**.
- Ao ativar: **gerar segredo client-side** (CSPRNG 32B → hex; padrão `useMcpTokens`), **exibir uma vez**, persistir via `.insert()` (NÃO `.upsert` — `reference_encrypted_views_write_pattern`).
- Renderizar a **regra CF exata**, pré-preenchida com `new URL(wp_site_url).hostname` + o segredo do tenant:
  ```
  (http.host eq "<HOST_DO_TENANT>" and starts_with(http.request.uri.path, "/wp-json/") and http.request.headers["x-mcorch-publish"][0] eq "<SEGREDO_DO_TENANT>")
  ```
  + passo-a-passo: **Action: Skip** → marcar **All managed rules + Super Bot Fight + Nível de segurança** (ver caveat datacenter em `wordpress-cf-publish-unblock.md`) → **Place at: First** → Save/Deploy. Botão "copiar regra".
- Botão **"Verificar"** → chama o Step 4.

**Sucesso material:** UI renderiza (E2E ocular 1920×1080 à prova de CF); `SELECT` mostra `wp_cf_publish_secret` = `••••` (não null, não claro) após salvar.

### Step 4 — Edge fn `verify-wp-cf`: gate de verificação per-user
JWT do user → resolve `wp_site_url` + `wp_cf_publish_secret` per-user → `fetch(<wp_site_url>/wp-json/wp/v2/types, { header X-MCORCH-Publish })` → retorna `{ ok, http_status, cf_challenge: boolean }`.

**Sucesso material:** `http_status=200, cf_challenge=false` quando a regra do tenant está certa; `403 + cf_challenge=true` quando não (a UI mostra a recovery: confira **Nível de segurança** + Deploy + valor byte-a-byte).

### Step 5 — Telemetria
`infra_health_logs` em cada path do publish e do verify (success/degraded/error), service `wordpress-cf-publish` / `verify-wp-cf`.

---

## Verification gates (material, antes de declarar "pronto")

| Gate | Comando | Esperado |
|---|---|---|
| G1 coluna cifrada | `SELECT wp_cf_publish_secret FROM user_api_keys WHERE user_id=<t>` | `••••` (não null/claro) |
| G2 tenant guard | INSERT/UPDATE per JWT de outro tenant | `42501` |
| G3 per-user header | `verify-wp-cf` (JWT do tenant, regra CF do tenant no ar) | `http_status=200, cf_challenge=false` |
| G4 fail-closed | tenant SEM secret, host ≠ zero | header não anexado (publish segue sem skip; sem vazar global) |
| G5 fallback intacto | tenant-zero (`www.mcorch.com`) sem regressão | continua publicando (Step do SOP global) |
| G6 isolamento | secret do tenant A nunca anexado a host do tenant B | code-review + grep do gate de host |

## Recovery path

- **G3 dá 403 com header:** mesmíssima recovery do `wordpress-cf-publish-unblock.md` — Security → Events do tenant nomeia o culpado; #1 datacenter = **Nível de segurança** não-marcado.
- **Header não anexa (deveria):** confira `wp_cf_publish_secret` no `.select()` do decrypted view + match de host case-insensitive.
- **23505 ao salvar o secret:** trigger de encrypt não-idempotente — aplicar o padrão `vault_upsert_secret` (Step 1).
- **Rollback:** UI desliga o toggle → RPC nula a coluna + revoga o segredo Vault (padrão `disconnect_wordpress`, migration `20260602120000`). Volta ao fail-closed sem regressão.

## Success signal (flow completo)

Um tenant **≠ tenant-zero**, com WP atrás do **próprio** Cloudflare + **próprio** segredo + a regra CF dele no ar, dispara `orchestrate-content` (ou Viral Autopilot) com publish WP e recebe `{ success: true, post_id }` — e o post aparece como rascunho no WP-admin **dele**, sem nenhum secret global ter sido usado.

## Referências

- SOP global/tenant-zero: `docs/processes/wordpress-cf-publish-unblock.md` (achado datacenter "Nível de segurança")
- API Tenancy Model — Per-User Credentials (CLAUDE.md) + `feedback_api_tenancy_per_user`
- Padrões de escrita em VIEW cifrada: `reference_encrypted_views_write_pattern` · `reference_user_api_keys_encrypted`
- Geração de segredo client-side CSPRNG: `src/hooks/useMcpTokens.ts`
- Disconnect/revogação de segredo Vault: `supabase/migrations/20260602120000_wordpress_disconnect_rpc.sql`
- Idempotência do encrypt: `supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql`
- Edge fn alvo: `supabase/functions/publish-wordpress/index.ts:49-99`

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

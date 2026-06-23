# Session agent-af1bcc5d008dba1ef
**Date:** 2026-06-23 | **Session ID:** `agent-af1bcc5d008dba1ef`

---

## 👤 User *(02:02:49)*

You are a senior security engineer reviewing a focused PR diff in the MCORCH repo at /home/gcrUX/htdocs/constellation-orchestra.

The full diff is persisted at: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/57ddea14-715c-47a6-ad8d-1cb57387c027/tool-results/b5vbxlb4e.txt — read it.

ALSO review these two NEW untracked files directly:
- supabase/migrations/20260622210000_user_api_keys_rapidapi_channel.sql (new migration adding a per-user encrypted `rapidapi_key` column to user_api_keys machinery)
- docs/processes/trends-credential-resolution.md (markdown SOP — EXCLUDED, do not review docs)

CONTEXT of the PR (what it does):
1. Removes the global `|| Deno.env.get("<PROVIDER>")` fallback from 25 user-facing edge functions → pure per-user credential resolution (reads `decrypted_user_api_keys` scoped to the authenticated `user.id`). This REMOVES a shared global key — a tenancy/security improvement.
2. embed-mcorch-node + search-constellation (system/pg_net flows, no user) renamed their env key reads from OPENROUTER_API_KEY/GEMINI_API_KEY to MESH_EMBED_OPENROUTER_KEY/MESH_EMBED_GEMINI_KEY (env-only, infra).
3. aios-chat-gateway removed a hardcoded literal token fallback → env-only + fail-closed 501.
4. New migration adds `rapidapi_key` — it is a VERBATIM mirror of the already-reviewed live migration supabase/migrations/20260615140000_user_api_keys_firecrawl_channel.sql, adding only the rapidapi_key column in each section (base column, encrypt trigger, masked view, INSTEAD OF trigger, decrypted view).

YOUR TASK: Identify ONLY high-confidence, newly-introduced, concretely-exploitable security vulnerabilities (>80% confidence). This is NOT a general review.

Focus areas: SQL injection, authn/authz bypass, privilege escalation, cross-tenant data access, hardcoded secrets, crypto issues, injection/RCE, sensitive data exposure.

Key things to verify in the NEW migration (compare against the firecrawl template it mirrors):
- Is the new `rapidapi_key` handled identically to the other encrypted columns (encrypt trigger uses vault_upsert_secret; masked view shows '••••'; INSTEAD OF has the tenant guard `auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid()` → 42501; decrypted view REVOKEd from anon/authenticated, GRANTed only to service_role; functions are SECURITY DEFINER SET search_path TO '')?
- Any deviation from the template that opens a cross-tenant read/write, secret exposure, or privilege escalation?
- Does CREATE OR REPLACE VIEW / FUNCTION drop any GRANT/REVOKE or RLS that the template had?

For the edge fn changes: does removing the env fallback or the per-user resolution introduce any cross-tenant access (e.g., reading another user's key)? Verify the `decrypted_user_api_keys` reads are scoped to the authenticated user's id.

EXCLUSIONS: No DOS, no rate-limiting, no "secrets on disk", no library-version issues, no theoretical races, no findings in markdown/docs, no lack-of-hardening, no log-spoofing. Environment variables are trusted. Client-side checks are not vulns.

OUTPUT: For each REAL finding (>80% confidence), give: file:line, severity (HIGH/MEDIUM), category, description, concrete exploit scenario, fix recommendation, and a confidence score 1-10. If you find NO high-confidence vulnerabilities, say so explicitly. Read the actual files — do not speculate.

## 🤖 Claude *(02:02:52)*

I'll review the PR diff and the new migration file. Let me start by reading all three sources.

## 🤖 Claude *(02:02:54)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/57ddea14-715c-47a6-ad8d-1cb57387c027/tool-results/b5vbxlb4e.txt"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	diff --git a/CLAUDE.md b/CLAUDE.md
> 2	index d99b2f8..ebf8fdb 100644
> 3	--- a/CLAUDE.md
> 4	+++ b/CLAUDE.md
> 5	@@ -417,7 +417,8 @@ Edge Function secrets (configured in Lovable Cloud vault, not in `.env`): `STRIP
> 6	 | Deploy harness | `scripts/harness-deploy.sh` |
> 7	 | **Build & Deploy materiality SOP** | `docs/processes/build-deploy-materiality.md` (worktree trap + gates) |
> 8	 | **Orchestrate async pipeline SOP** | `docs/processes/orchestrate-async-pipeline.md` (pg_net→`verify_jwt=false` mandate + RPC param-name contract + WP canonical-URL; the 3 key-migration failure modes + recovery) |
> 9	-| **WordPress CF publish-unblock SOP** | `docs/processes/wordpress-cf-publish-unblock.md` (CF managed challenge 403 em `/wp-json/*` mata o publish server-side; fix = header secreto `X-MCORCH-Publish` host-gated fail-closed na edge fn + CF WAF Skip gated por header; secrets `WP_PUBLISH_SECRET`/`_HOST` = ação Sovereign; gates de verificação curl) |
> 10	+| **WordPress CF publish-unblock SOP (tenant-zero/global)** | `docs/processes/wordpress-cf-publish-unblock.md` (**RESOLVIDO 2026-06-22**: CF managed challenge 403 em `/wp-json/*` matava o publish server-side; fix = header secreto `X-MCORCH-Publish` host-gated fail-closed na edge fn + CF WAF Skip gated por header. **Achado material decisivo: o componente de skip que faltava era "Nível de segurança" (Security Level)** — challenge por reputação do IP de **datacenter** (Oracle AS31898), não bot/UA; `All managed rules`+`Super Bot Fight` sozinhos não resolviam. Provado E2E `publish-wordpress`→`{"success":true,"post_id":18}`. Diagnóstico via Security→Events. Secrets `WP_PUBLISH_SECRET`/`_HOST` provisionados) |
> 11	+| **WordPress CF publish per-user SOP (multi-tenant)** | `docs/processes/wordpress-cf-per-user-publish.md` (generaliza o unblock global p/ QUALQUER tenant atrás do PRÓPRIO Cloudflare — Lei 2/API Tenancy Model. Coluna per-user cifrada `wp_cf_publish_secret` (Vault) + lookup per-user em `publish-wordpress` (global vira fallback restrito do tenant-zero) + UI Settings→WordPress que GERA o segredo do tenant e MOSTRA a regra CF dele pré-preenchida + edge `verify-wp-cf`. Segredo per-user bound ao host do próprio tenant = zero exfil cross-tenant. **SOP selado; código pendente**) |
> 12	 | **Schema drift audit SOP + tool** | `docs/processes/schema-drift-audit.md` + `scripts/qa/audit-schema-drift.sh` (deployed↔migration drift: ledger · out-of-band fns/triggers · RPC caller-contract · edge `verify_jwt` · RLS/search_path advisory; exit 1=drift. Born do P0 do hotfix-sem-migration. **Regra: todo hotfix de prod vira migration na MESMA sessão**) |
> 13	 | **Drift audit report + remediation (2026-06-03)** | `.claude/context/drift-audit-2026-06-03.md` (1 drift real benigno `rls_auto_enable` capturado · 7 SECURITY DEFINER search_path travados · trigger pg_net morto kong:8000 dropado — migrations `20260603210000`/`210500`/`211000`, /security-review SAFE, re-audit exit 0) |
> 14	 | **mcoCoins cost calibration SOP** | `docs/processes/mcoin-cost-calibration.md` (4×-floor model `mco=ceil(usd/$0.018×4)`; OTD-MCOIN-CALIBRATION closed) |
> 15	diff --git a/docs/processes/wordpress-cf-per-user-publish.md b/docs/processes/wordpress-cf-per-user-publish.md
> 16	new file mode 100644
> 17	index 0000000..29b7424
> 18	--- /dev/null
> 19	+++ b/docs/processes/wordpress-cf-per-user-publish.md
> 20	@@ -0,0 +1,113 @@
> 21	+# SOP — Publish WordPress per-user atrás do Cloudflare (multi-tenant)
> 22	+
> 23	+> **Slug:** `wordpress-cf-per-user-publish` · **Criado:** 2026-06-22 · **Lei 2 (Processo Antecipado)** · **API Tenancy Model — Per-User Credentials**
> 24	+> **Origem:** diretiva Sovereign 2026-06-22 — *"o que resolvemos do WP com CF agora deve ser per-user dentro do ecossistema; se o usuário precisar adicionar uma regra no Cloudflare, devemos deixar explícito e claro na UI do painel para o usuário fazer o passo correto"* + *"tudo que é per-user sempre é prioridade ser resolvido per-user"*.
> 25	+> **Generaliza** o unblock **global/tenant-zero** já vivo (`docs/processes/wordpress-cf-publish-unblock.md`, secret global `WP_PUBLISH_SECRET`/`_HOST` → `www.mcorch.com`) para **qualquer tenant** cujo WordPress self-hosted esteja atrás do **próprio** Cloudflare.
> 26	+
> 27	+---
> 28	+
> 29	+## Problema
> 30	+
> 31	+O unblock atual é **single-tenant**: um único `WP_PUBLISH_SECRET` global bound a `WP_PUBLISH_SECRET_HOST=www.mcorch.com` (o site do Usuário Zero). Quando o Usuário 1+ conecta o **próprio** WP (`user_api_keys.wp_site_url` ≠ `www.mcorch.com`), atrás do **próprio** Cloudflare, o `publish-wordpress` faz `fetch` server-side (Deno, sem engine JS) e morre no **managed challenge** do CF *daquele* tenant → publish 502. Estender o secret global a hosts de tenant é **proibido** (o segredo de skip do CF do MCORCH é bound a UMA origem nossa; mandá-lo a um host escolhido pelo tenant permitiria replay/exfil — ver fail-closed em `publish-wordpress/index.ts:80-99`).
> 32	+
> 33	+## Modelo da solução (per-user, fail-closed)
> 34	+
> 35	+Cada tenant que tem WP atrás do próprio Cloudflare ganha o **seu próprio segredo compartilhado**, guardado **cifrado por-usuário** no Vault, e a **UI o guia** a criar a regra de WAF Skip correta no **Cloudflare dele** — com a expressão e o segredo **dele** já preenchidos.
> 36	+
> 37	+**Resolution order (API Tenancy Model):**
> 38	+1. **Per-user primeiro** — `decrypted_user_api_keys.wp_cf_publish_secret` (do `user_id`). Anexa `X-MCORCH-Publish: <segredo-do-tenant>` **somente** quando o host de destino == host do `wp_site_url` **do próprio tenant** (sempre é — publicamos no site dele; o segredo nunca viaja para outro host).
> 39	+2. **Global fallback restrito** — `Deno.env.get('WP_PUBLISH_SECRET')` SÓ quando o host de destino == `WP_PUBLISH_SECRET_HOST` (= `www.mcorch.com`, tenant-zero / onboarding default documentado).
> 40	+3. **No-op fail-closed** — sem secret per-user e host ≠ tenant-zero ⇒ **header nunca é anexado** (o publish segue sem o skip; correto se o WP do tenant **não** está atrás de um CF que desafia).
> 41	+
> 42	+**Segurança:** o segredo per-user é do **próprio** tenant, bound ao **próprio** host → zero exfil cross-tenant. Cifrado em repouso como qualquer BYOK (`wp_app_password`). É **retrievable** (a edge fn precisa replayá-lo como header) — diferente de um PAT (hash-only); portanto a UI o exibe na geração e a rotação = re-gerar.
> 43	+
> 44	+---
> 45	+
> 46	+## ORO
> 47	+
> 48	+- **Operator:** MCORCH Master Execution Agent (migration + edge fn + UI) **+ o TENANT** (cria a regra de WAF Skip no Cloudflare **dele**, na conta CF dele).
> 49	+- **Reviewer:** `/security-review` independente (migration + edge fn) + Sovereign.
> 50	+- **Owner:** Sovereign — blast radius = publish multi-tenant + manuseio de segredo per-user + isolamento entre tenants. (O Owner da regra CF de cada tenant é o próprio tenant.)
> 51	+
> 52	+---
> 53	+
> 54	+## Sequence (passos numerados, cada um com critério material)
> 55	+
> 56	+### Step 1 — Schema: coluna per-user cifrada `wp_cf_publish_secret`
> 57	+Migration adicionando a coluna ao **backing table** do `user_api_keys` (VIEW mascarada Vault — ver `reference_encrypted_views_write_pattern`), com:
> 58	+- Trigger de encriptação Vault idempotente (padrão `vault_upsert_secret`, migration `20260602140000`) — re-save não dá 23505.
> 59	+- VIEW mascarada expõe `wp_cf_publish_secret` como `••••`; `decrypted_user_api_keys` expõe o claro (só service_role).
> 60	+- INSTEAD OF trigger **UPDATE-first** + guard de tenant `auth.uid()` (padrão migrations `20260602130000`/`150000` — NUNCA `INSERT...ON CONFLICT` [double-fire] nem injeção cross-tenant).
> 61	+- `/security-review` **obrigatório** antes do commit (FMEA-011).
> 62	+
> 63	+**Sucesso material:** `db push` exit 0; `SELECT wp_cf_publish_secret FROM user_api_keys` mostra `••••`; service-role `SELECT ... FROM decrypted_user_api_keys` retorna o claro; INSERT por JWT de outro tenant → 42501.
> 64	+
> 65	+### Step 2 — Edge fn `publish-wordpress`: lookup per-user
> 66	+Estender o gate de host (`publish-wordpress/index.ts:90-99`) para a resolution order acima:
> 67	+```
> 68	+const perUser = userKeys?.wp_cf_publish_secret;            // já vem do decrypted_user_api_keys select
> 69	+const targetHost = new URL(apiBase).hostname.toLowerCase();
> 70	+if (perUser && targetHost === new URL(wpSiteUrl).hostname.toLowerCase()) {
> 71	+  wpAuthHeaders["X-MCORCH-Publish"] = perUser;             // per-user: segredo do tenant → host do tenant
> 72	+} else if (wpPublishSecret && wpPublishSecretHost && targetHost === wpPublishSecretHost.toLowerCase()) {
> 73	+  wpAuthHeaders["X-MCORCH-Publish"] = wpPublishSecret;     // fallback restrito: tenant-zero
> 74	+}                                                          // senão: nada (fail-closed)
> 75	+```
> 76	+Adicionar `wp_cf_publish_secret` ao `.select()` do `decrypted_user_api_keys` (linha ~53). Telemetria `infra_health_logs` service `wordpress-cf-publish` com path (`per_user` / `global_fallback` / `no_secret`).
> 77	+
> 78	+**Sucesso material:** deploy com script size; boot-smoke 401 sem auth; um tenant ≠ zero com secret per-user + host próprio → header anexado (provado pelo Step 4).
> 79	+
> 80	+### Step 3 — UI: Settings → WordPress → seção "Cloudflare" (guia explícito)
> 81	+Hook `useWpCloudflare` (TanStack Query) + card em `MetaConfigCard`-style:
> 82	+- Toggle **"Meu WordPress está atrás do Cloudflare"**.
> 83	+- Ao ativar: **gerar segredo client-side** (CSPRNG 32B → hex; padrão `useMcpTokens`), **exibir uma vez**, persistir via `.insert()` (NÃO `.upsert` — `reference_encrypted_views_write_pattern`).
> 84	+- Renderizar a **regra CF exata**, pré-preenchida com `new URL(wp_site_url).hostname` + o segredo do tenant:
> 85	+  ```
> 86	+  (http.host eq "<HOST_DO_TENANT>" and starts_with(http.request.uri.path, "/wp-json/") and http.request.headers["x-mcorch-publish"][0] eq "<SEGREDO_DO_TENANT>")
> 87	+  ```
> 88	+  + passo-a-passo: **Action: Skip** → marcar **All managed rules + Super Bot Fight + Nível de segurança** (ver caveat datacenter em `wordpress-cf-publish-unblock.md`) → **Place at: First** → Save/Deploy. Botão "copiar regra".
> 89	+- Botão **"Verificar"** → chama o Step 4.
> 90	+
> 91	+**Sucesso material:** UI renderiza (E2E ocular 1920×1080 à prova de CF); `SELECT` mostra `wp_cf_publish_secret` = `••••` (não null, não claro) após salvar.
> 92	+
> 93	+### Step 4 — Edge fn `verify-wp-cf`: gate de verificação per-user
> 94	+JWT do user → resolve `wp_site_url` + `wp_cf_publish_secret` per-user → `fetch(<wp_site_url>/wp-json/wp/v2/types, { header X-MCORCH-Publish })` → retorna `{ ok, http_status, cf_challenge: boolean }`.
> 95	+
> 96	+**Sucesso material:** `http_status=200, cf_challenge=false` quando a regra do tenant está certa; `403 + cf_challenge=true` quando não (a UI mostra a recovery: confira **Nível de segurança** + Deploy + valor byte-a-byte).
> 97	+
> 98	+### Step 5 — Telemetria
> 99	+`infra_health_logs` em cada path do publish e do verify (success/degraded/error), service `wordpress-cf-publish` / `verify-wp-cf`.
> 100	+
> 101	+---
> 102	+
> 103	+## Verification gates (material, antes de declarar "pronto")
> 104	+
> 105	+| Gate | Comando | Esperado |
> 106	+|---|---|---|
> 107	+| G1 coluna cifrada | `SELECT wp_cf_publish_secret FROM user_api_keys WHERE user_id=<t>` | `••••` (não null/claro) |
> 108	+| G2 tenant guard | INSERT/UPDATE per JWT de outro tenant | `42501` |
> 109	+| G3 per-user header | `verify-wp-cf` (JWT do tenant, regra CF do tenant no ar) | `http_status=200, cf_challenge=false` |
> 110	+| G4 fail-closed | tenant SEM secret, host ≠ zero | header não anexado (publish segue sem skip; sem vazar global) |
> 111	+| G5 fallback intacto | tenant-zero (`www.mcorch.com`) sem regressão | continua publicando (Step do SOP global) |
> 112	+| G6 isolamento | secret do tenant A nunca anexado a host do tenant B | code-review + grep do gate de host |
> 113	+
> 114	+## Recovery path
> 115	+
> 116	+- **G3 dá 403 com header:** mesmíssima recovery do `wordpress-cf-publish-unblock.md` — Security → Events do tenant nomeia o culpado; #1 datacenter = **Nível de segurança** não-marcado.
> 117	+- **Header não anexa (deveria):** confira `wp_cf_publish_secret` no `.select()` do decrypted view + match de host case-insensitive.
> 118	+- **23505 ao salvar o secret:** trigger de encrypt não-idempotente — aplicar o padrão `vault_upsert_secret` (Step 1).
> 119	+- **Rollback:** UI desliga o toggle → RPC nula a coluna + revoga o segredo Vault (padrão `disconnect_wordpress`, migration `20260602120000`). Volta ao fail-closed sem regressão.
> 120	+
> 121	+## Success signal (flow completo)
> 122	+
> 123	+Um tenant **≠ tenant-zero**, com WP atrás do **próprio** Cloudflare + **próprio** segredo + a regra CF dele no ar, dispara `orchestrate-content` (ou Viral Autopilot) com publish WP e recebe `{ success: true, post_id }` — e o post aparece como rascunho no WP-admin **dele**, sem nenhum secret global ter sido usado.
> 124	+
> 125	+## Referências
> 126	+
> 127	+- SOP global/tenant-zero: `docs/processes/wordpress-cf-publish-unblock.md` (achado datacenter "Nível de segurança")
> 128	+- API Tenancy Model — Per-User Credentials (CLAUDE.md) + `feedback_api_tenancy_per_user`
> 129	+- Padrões de escrita em VIEW cifrada: `reference_encrypted_views_write_pattern` · `reference_user_api_keys_encrypted`
> 130	+- Geração de segredo client-side CSPRNG: `src/hooks/useMcpTokens.ts`
> 131	+- Disconnect/revogação de segredo Vault: `supabase/migrations/20260602120000_wordpress_disconnect_rpc.sql`
> 132	+- Idempotência do encrypt: `supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql`
> 133	+- Edge fn alvo: `supabase/functions/publish-wordpress/index.ts:49-99`
> 134	diff --git a/docs/processes/wordpress-cf-publish-unblock.md b/docs/processes/wordpress-cf-publish-unblock.md
> 135	index 70b7c93..16a55a7 100644
> 136	--- a/docs/processes/wordpress-cf-publish-unblock.md
> 137	+++ b/docs/processes/wordpress-cf-publish-unblock.md
> 138	@@ -47,11 +47,14 @@ Painel Cloudflare → zona `mcorch.com` → **Security → WAF → Custom rules
> 139	   ```
> 140	   (http.host eq "www.mcorch.com" and starts_with(http.request.uri.path, "/wp-json/") and http.request.headers["x-mcorch-publish"][0] eq "<o-hex-do-step-1>")
> 141	   ```
> 142	-- **Action:** `Skip` → marcar:
> 143	-  - ✅ All managed rules
> 144	-  - ✅ Super Bot Fight Mode (se o plano expõe a opção)
> 145	-  - ✅ qualquer "Managed Challenge / Bot Fight"
> 146	+- **Action:** `Skip` → marcar (o **Nível de segurança** é o que mais escapa — ver nota abaixo):
> 147	+  - ✅ All managed rules (Todas as regras gerenciadas)
> 148	+  - ✅ Super Bot Fight Mode (Todas as regras do modo Super Bot Fight)
> 149	+  - ✅ **Nível de segurança (Security Level)** — **IMPRESCINDÍVEL quando a edge function egressa de um IP de _datacenter_** (Oracle/AWS/GCP). O CF emite **Managed Challenge por reputação de IP** via *Security Level*, que **não** é coberto por "managed rules" nem por "Super Bot Fight". Sem marcar esta, o `curl` com header continua **403 mesmo com a regra de Skip disparando** (o Events mostra dois eventos no mesmo request: a nossa regra com ação `Ignorar` **e** o `Nível de segurança` com `Desafio gerenciado`).
> 150	+  - ❌ **NÃO** marque "Verificação da integridade do navegador" (Browser Integrity Check) — o challenge é **cego ao User-Agent** (provado: UA de Chrome → ainda 403), logo BIC não é a fonte; marcá-la só amplia o skip à toa.
> 151	 - **Place at:** topo da ordem de execução (First).
> 152	+
> 153	+> 📌 **Achado material 2026-06-22 (verificado):** a fonte real do challenge era o **Nível de segurança** emitindo `Desafio gerenciado` ao IP `137.131.243.179` (AS31898 **Oracle Corporation**) — o IP de datacenter onde a edge/QA roda. `All managed rules` + `Super Bot Fight` sozinhos **não** resolviam; só ao adicionar **Nível de segurança** ao Skip é que o `curl` com header saiu do 403 (→ 200 + JSON real do WP) e o `publish-wordpress` E2E retornou `{"success":true,"post_id":18}`. Defense-in-depth preservado: sem o header, segue 403.
> 154	 - Save + Deploy.
> 155	 
> 156	 > ⚠️ **Caveat de plano:** em planos onde o **Bot Fight Mode global** não é "skippável" por regra, ele pode reintroduzir o challenge mesmo com o Skip de WAF. Se o Step 4 ainda der 403, revisar **Security → Bots** e desligar/ajustar o Bot Fight Mode global para esse path, ou subir de plano.
> 157	@@ -80,7 +83,11 @@ curl -sS -D - -o /dev/null -H "X-MCORCH-Publish: <o-hex-do-step-1>" \
> 158	 
> 159	 ## Recovery path (falha no step N)
> 160	 
> 161	-- **Step 4a dá 403 mesmo COM o header:** o Skip não pegou. Conferir (i) que a expressão usa `http.request.headers["x-mcorch-publish"]` em **lowercase** (CF normaliza nomes de header), (ii) que o valor no rule bate byte-a-byte com o `WP_PUBLISH_SECRET`, (iii) que a regra está no topo da ordem, (iv) o caveat de Bot Fight Mode global acima.
> 162	+- **Step 4a dá 403 mesmo COM o header:** **diagnóstico definitivo primeiro** → Cloudflare → **Security → Events**, clica num request 403 pra `/wp-json/`, lê o campo **"Service" / "Ação realizada"**. Ele **nomeia o culpado exato**:
> 163	+  - `Regras personalizadas` + `Ignorar` apontando pra nossa regra ⇒ a regra **casou e disparou** (header/expressão/hex OK); o 403 vem de **outro** componente não-skippado — olhe o(s) outro(s) evento(s) do mesmo request.
> 164	+  - `Nível de segurança` + `Desafio gerenciado` ⇒ **marque "Nível de segurança"** no Skip (causa #1 para IPs de datacenter — ver Step 3).
> 165	+  - `Bot Fight Mode` (sem "Super") ⇒ tier **não-skippável**; ajuste em Security → Bots (ou suba pra Super Bot Fight).
> 166	+  - Nenhum evento da nossa regra (0 matches) ⇒ aí sim o Skip não casou: conferir (i) header em **lowercase** na expressão (CF normaliza), (ii) valor byte-a-byte com `WP_PUBLISH_SECRET`, (iii) regra no topo (First), (iv) regra **Deployed** (não rascunho).
> 167	 - **Step 4a dá 200 SEM o header:** a regra está aberta demais (não exige o header) — `/wp-json` ficou exposto. **Corrigir imediatamente** adicionando a cláusula do header à expressão; é uma regressão de segurança.
> 168	 - **Step 4 com header correto mas publish ainda 502:** não é mais o CF — investigar Basic Auth do WP (`wp_app_password` válido?) ou a resposta do WP REST (a função já distingue 403-CF de array-por-redirect; ler `wp_http_status` no corpo do 502).
> 169	 - **Rollback total:** remover a CF rule + `npx supabase secrets unset WP_PUBLISH_SECRET WP_PUBLISH_SECRET_HOST`. A função volta ao comportamento fail-closed (sem header) — sem regressão, só sem publish (estado pré-fix).
> 170	diff --git a/supabase/functions/aeo-audit/index.ts b/supabase/functions/aeo-audit/index.ts
> 171	index 23966c3..4417a1b 100644
> 172	--- a/supabase/functions/aeo-audit/index.ts
> 173	+++ b/supabase/functions/aeo-audit/index.ts
> 174	@@ -65,8 +65,8 @@ serve(async (req) => {
> 175	     // resolve per-user AI key → system fallback (API Tenancy Model).
> 176	     const { data: keys } = await admin.from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 177	     const groqKey = keys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 178	-    const openRouterKey = keys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 179	-    const geminiKey = keys?.google_api_key || Deno.env.get("GEMINI_API_KEY");
> 180	+    const openRouterKey = keys?.openrouter_api_key;
> 181	+    const geminiKey = keys?.google_api_key;
> 182	     const aiKey = groqKey || openRouterKey;
> 183	 
> 184	     // ── Answer-engine proxy: ONE batched LLM call rates citation for every query (fail-soft to heuristic). ──
> 185	diff --git a/supabase/functions/agent-task-execute/index.ts b/supabase/functions/agent-task-execute/index.ts
> 186	index d120278..decd755 100644
> 187	--- a/supabase/functions/agent-task-execute/index.ts
> 188	+++ b/supabase/functions/agent-task-execute/index.ts
> 189	@@ -160,8 +160,8 @@ Deno.serve(async (req) => {
> 190	       .maybeSingle();
> 191	 
> 192	     const groqKey = keys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 193	-    const openRouterKey = keys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 194	-    const geminiKey = keys?.google_api_key || Deno.env.get("GEMINI_API_KEY");
> 195	+    const openRouterKey = keys?.openrouter_api_key;
> 196	+    const geminiKey = keys?.google_api_key;
> 197	 
> 198	     const apiKey =
> 199	       provider === "groq" ? groqKey :
> 200	diff --git a/supabase/functions/aios-chat-gateway/index.ts b/supabase/functions/aios-chat-gateway/index.ts
> 201	index e6b9d6b..ac0ad49 100644
> 202	--- a/supabase/functions/aios-chat-gateway/index.ts
> 203	+++ b/supabase/functions/aios-chat-gateway/index.ts
> 204	@@ -196,8 +196,31 @@ Deno.serve(async (req) => {
> 205	     }
> 206	     const execId = execRow?.id;
> 207	 
> 208	-    // Trigger OpenClaw Gateway locally via Docker Host bridge
> 209	-    const openClawToken = Deno.env.get("OPENCLAW_GATEWAY_TOKEN") || "3bdfc718fb880d4d585c540339ba6d3c2a72d7510b2479d7";
> 210	+    // Trigger OpenClaw Gateway locally via Docker Host bridge.
> 211	+    // SECURITY: the gateway bearer MUST resolve from the edge-function secret ONLY. A committed literal fallback
> 212	+    // both (a) leaks the gateway secret into source control and (b) fails OPEN — the fn would keep forwarding with
> 213	+    // a default even when the secret is unset, masking misconfiguration. Resolve env-only and fail CLOSED.
> 214	+    const openClawToken = Deno.env.get("OPENCLAW_GATEWAY_TOKEN");
> 215	+    if (!openClawToken) {
> 216	+      console.error("[aios-chat-gateway] OPENCLAW_GATEWAY_TOKEN not configured — refusing to forward (fail-closed).");
> 217	+      if (execId) {
> 218	+        await supabase
> 219	+          .from("agent_executions")
> 220	+          .update({
> 221	+            status: "failed",
> 222	+            error_msg: "OPENCLAW_GATEWAY_TOKEN not configured",
> 223	+            completed_at: new Date().toISOString(),
> 224	+          })
> 225	+          .eq("id", execId);
> 226	+      }
> 227	+      await supabase.from("infra_health_logs").insert({
> 228	+        service: "aios-chat-gateway",
> 229	+        status: "error",
> 230	+        message: "OPENCLAW_GATEWAY_TOKEN not configured — forwarding refused (fail-closed)",
> 231	+        metadata: { thread_id: record.thread_id, agent_id: targetAgent },
> 232	+      });
> 233	+      return respond({ error: "openclaw_gateway_not_configured" }, 501);
> 234	+    }
> 235	     const openClawUrl = "http://host.docker.internal:18789/v1/chat/completions";
> 236	 
> 237	     console.log(`[aios-chat-gateway] Forwarding request to OpenClaw: ${openClawUrl}`);
> 238	diff --git a/supabase/functions/aios-chat-stream/index.ts b/supabase/functions/aios-chat-stream/index.ts
> 239	index d9c86fd..354273e 100644
> 240	--- a/supabase/functions/aios-chat-stream/index.ts
> 241	+++ b/supabase/functions/aios-chat-stream/index.ts
> 242	@@ -98,12 +98,12 @@ Deno.serve(async (req) => {
> 243	   // Resolve API Key
> 244	   let apiKey = "";
> 245	   if (isOpenRouter) {
> 246	-    apiKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY") || "";
> 247	+    apiKey = userKeys?.openrouter_api_key || "";
> 248	     if (!apiKey) {
> 249	       return respond({ error: "OPENROUTER_API_KEY not configured" }, 500);
> 250	     }
> 251	   } else {
> 252	-    apiKey = (forceVault ? null : userKeys?.google_api_key) || Deno.env.get("GEMINI_API_KEY") || "";
> 253	+    apiKey = (forceVault ? null : userKeys?.google_api_key) || "";
> 254	     if (!apiKey) {
> 255	       return respond({ error: "GEMINI_API_KEY not configured" }, 500);
> 256	     }
> 257	diff --git a/supabase/functions/aios-chat/index.ts b/supabase/functions/aios-chat/index.ts
> 258	index 3b63dd2..648c2c8 100644
> 259	--- a/supabase/functions/aios-chat/index.ts
> 260	+++ b/supabase/functions/aios-chat/index.ts
> 261	@@ -101,7 +101,7 @@ Deno.serve(async (req) => {
> 262	   const t0 = Date.now();
> 263	 
> 264	   if (isOpenRouter) {
> 265	-    const apiKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY") || "";
> 266	+    const apiKey = userKeys?.openrouter_api_key || "";
> 267	     if (!apiKey) {
> 268	       return respond({ error: "OPENROUTER_API_KEY not configured" }, 500);
> 269	     }
> 270	@@ -160,7 +160,7 @@ Deno.serve(async (req) => {
> 271	   }
> 272	 
> 273	   // User key takes precedence over vault (vault: prefix forces the platform key)
> 274	-  const geminiKey = (forceVault ? null : userKeys?.google_api_key) || Deno.env.get("GEMINI_API_KEY");
> 275	+  const geminiKey = (forceVault ? null : userKeys?.google_api_key);
> 276	   if (!geminiKey) {
> 277	     return respond({ error: "GEMINI_API_KEY not configured" }, 500);
> 278	   }
> 279	diff --git a/supabase/functions/aios-live-proxy/index.ts b/supabase/functions/aios-live-proxy/index.ts
> 280	index 900bf45..a889a28 100644
> 281	--- a/supabase/functions/aios-live-proxy/index.ts
> 282	+++ b/supabase/functions/aios-live-proxy/index.ts
> 283	@@ -58,7 +58,7 @@ Deno.serve(async (req) => {
> 284	     .eq("user_id", user.id)
> 285	     .maybeSingle();
> 286	 
> 287	-  const geminiKey = userKeys?.google_api_key || Deno.env.get("GEMINI_API_KEY");
> 288	+  const geminiKey = userKeys?.google_api_key;
> 289	   if (!geminiKey) {
> 290	     return new Response("GEMINI_API_KEY not configured", { 
> 291	       status: 500,
> 292	diff --git a/supabase/functions/analyze-node/index.ts b/supabase/functions/analyze-node/index.ts
> 293	index 2c71d79..ef1c907 100644
> 294	--- a/supabase/functions/analyze-node/index.ts
> 295	+++ b/supabase/functions/analyze-node/index.ts
> 296	@@ -44,8 +44,8 @@ Deno.serve(async (req) => {
> 297	     const adminClient = createClient(Deno.env.get("SUPABASE_URL")!, (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!);
> 298	     const { data: userKeys } = await adminClient.from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 299	 
> 300	-    const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 301	-    const geminiKey = userKeys?.google_api_key || Deno.env.get("GEMINI_API_KEY");
> 302	+    const openRouterKey = userKeys?.openrouter_api_key;
> 303	+    const geminiKey = userKeys?.google_api_key;
> 304	 
> 305	     if (!openRouterKey) {
> 306	       return new Response(JSON.stringify({ error: "OPENROUTER_API_KEY not configured" }), {
> 307	diff --git a/supabase/functions/analyze-sem/index.ts b/supabase/functions/analyze-sem/index.ts
> 308	index 994eb37..910723a 100644
> 309	--- a/supabase/functions/analyze-sem/index.ts
> 310	+++ b/supabase/functions/analyze-sem/index.ts
> 311	@@ -32,8 +32,8 @@ serve(async (req) => {
> 312	     const { data: userKeys } = await adminClient.from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 313	     
> 314	     const groqKey = userKeys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 315	-    const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 316	-    const geminiKey = userKeys?.google_api_key || Deno.env.get("GEMINI_API_KEY");
> 317	+    const openRouterKey = userKeys?.openrouter_api_key;
> 318	+    const geminiKey = userKeys?.google_api_key;
> 319	     const aiKey = groqKey || openRouterKey;
> 320	 
> 321	     if (!aiKey) throw new Error("AI not configured");
> 322	diff --git a/supabase/functions/analyze-seo/index.ts b/supabase/functions/analyze-seo/index.ts
> 323	index 478717b..9335639 100644
> 324	--- a/supabase/functions/analyze-seo/index.ts
> 325	+++ b/supabase/functions/analyze-seo/index.ts
> 326	@@ -31,8 +31,8 @@ serve(async (req) => {
> 327	     const { data: userKeys } = await adminClient.from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 328	     
> 329	     const groqKey = userKeys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 330	-    const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 331	-    const geminiKey = userKeys?.google_api_key || Deno.env.get("GEMINI_API_KEY");
> 332	+    const openRouterKey = userKeys?.openrouter_api_key;
> 333	+    const geminiKey = userKeys?.google_api_key;
> 334	     const aiKey = groqKey || openRouterKey;
> 335	 
> 336	     if (!aiKey) throw new Error("AI not configured");
> 337	diff --git a/supabase/functions/canvas-execute/index.ts b/supabase/functions/canvas-execute/index.ts
> 338	index e73bd15..6465345 100644
> 339	--- a/supabase/functions/canvas-execute/index.ts
> 340	+++ b/supabase/functions/canvas-execute/index.ts
> 341	@@ -131,13 +131,16 @@ serve(async (req) => {
> 342	     const { data: userKeys } = await admin
> 343	       .from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 344	 
> 345	+    // Pure per-user credential resolution (API Tenancy Model) — NO global env fallback for provider keys (env is
> 346	+    // infra-only). Higgsfield is a key+secret PAIR; both come from the tenant's own BYOK (a half-populated row just
> 347	+    // fails closed at the provider, which is the correct BYOK behavior).
> 348	     const keys = {
> 349	-      openai: userKeys?.openai_api_key || Deno.env.get("OPENAI_API_KEY") || "",
> 350	-      replicate: userKeys?.replicate_api_key || Deno.env.get("REPLICATE_API_KEY") || "",
> 351	-      openrouter: userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY") || "",
> 352	-      gemini: userKeys?.google_api_key || Deno.env.get("GEMINI_API_KEY") || "",
> 353	-      higgsfield: Deno.env.get("HIGGSFIELD_API_KEY") || "",
> 354	-      higgsfield_secret: Deno.env.get("HIGGSFIELD_API_KEY_SECRET") || "",
> 355	+      openai: userKeys?.openai_api_key || "",
> 356	+      replicate: userKeys?.replicate_api_key || "",
> 357	+      openrouter: userKeys?.openrouter_api_key || "",
> 358	+      gemini: userKeys?.google_api_key || "",
> 359	+      higgsfield: userKeys?.higgsfield_api_key || "",
> 360	+      higgsfield_secret: userKeys?.higgsfield_api_key_secret || "",
> 361	     };
> 362	 
> 363	     // ── Calculate credit cost ────────────────────────────────────────
> 364	diff --git a/supabase/functions/check-video-status/index.ts b/supabase/functions/check-video-status/index.ts
> 365	index 0bb66f6..57ff6d2 100644
> 366	--- a/supabase/functions/check-video-status/index.ts
> 367	+++ b/supabase/functions/check-video-status/index.ts
> 368	@@ -103,7 +103,7 @@ serve(async (req) => {
> 369	     // OPENROUTER: GET /api/v1/videos/{jobId}
> 370	     // ==========================================
> 371	     if (provider === "openrouter") {
> 372	-      const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 373	+      const openRouterKey = userKeys?.openrouter_api_key;
> 374	       if (!openRouterKey) {
> 375	         return new Response(JSON.stringify({ status: "error", error: "Chave OpenRouter não encontrada" }), {
> 376	           status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" },
> 377	diff --git a/supabase/functions/embed-mcorch-node/index.ts b/supabase/functions/embed-mcorch-node/index.ts
> 378	index d1c93e9..9fb155e 100644
> 379	--- a/supabase/functions/embed-mcorch-node/index.ts
> 380	+++ b/supabase/functions/embed-mcorch-node/index.ts
> 381	@@ -184,11 +184,14 @@ Deno.serve(async (req) => {
> 382	     serviceKey,
> 383	   );
> 384	 
> 385	-  const openRouterKey = Deno.env.get("OPENROUTER_API_KEY");
> 386	-  const geminiKey = Deno.env.get("GEMINI_API_KEY");
> 387	+  // INFRA: dedicated mesh-embedding system keys. This pipeline is pg_net-triggered (no user in scope), so it is
> 388	+  // NOT a user-facing flow — these are NOT BYOK fallbacks. User flows resolve per-user (API Tenancy Model); the
> 389	+  // distinct MESH_EMBED_* names make the infra-only role unambiguous (env = infra only).
> 390	+  const openRouterKey = Deno.env.get("MESH_EMBED_OPENROUTER_KEY");
> 391	+  const geminiKey = Deno.env.get("MESH_EMBED_GEMINI_KEY");
> 392	   if (!openRouterKey && !geminiKey) {
> 393	     return new Response(
> 394	-      JSON.stringify({ error: "Neither OPENROUTER_API_KEY nor GEMINI_API_KEY configured" }),
> 395	+      JSON.stringify({ error: "Neither MESH_EMBED_OPENROUTER_KEY nor MESH_EMBED_GEMINI_KEY configured" }),
> 396	       { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } },
> 397	     );
> 398	   }
> 399	diff --git a/supabase/functions/generate-audio-script/index.ts b/supabase/functions/generate-audio-script/index.ts
> 400	index ee017be..4513cfb 100644
> 401	--- a/supabase/functions/generate-audio-script/index.ts
> 402	+++ b/supabase/functions/generate-audio-script/index.ts
> 403	@@ -48,7 +48,7 @@ serve(async (req) => {
> 404	     
> 405	     const prefAudio = userKeys?.pref_audio_provider || "openai";
> 406	     const groqKey = userKeys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 407	-    const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 408	+    const openRouterKey = userKeys?.openrouter_api_key;
> 409	     const elevenLabsKey = userKeys?.elevenlabs_api_key || Deno.env.get("ELEVENLABS_API_KEY");
> 410	     const googleKey = userKeys?.google_api_key || Deno.env.get("GOOGLE_API_KEY");
> 411	 
> 412	diff --git a/supabase/functions/generate-content/index.ts b/supabase/functions/generate-content/index.ts
> 413	index b3b5621..fbed507 100644
> 414	--- a/supabase/functions/generate-content/index.ts
> 415	+++ b/supabase/functions/generate-content/index.ts
> 416	@@ -43,8 +43,8 @@ serve(async (req) => {
> 417	     const { data: userKeys } = await adminClient.from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 418	     
> 419	     const groqKey = userKeys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 420	-    const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 421	-    const geminiKey = userKeys?.google_api_key || Deno.env.get("GEMINI_API_KEY");
> 422	+    const openRouterKey = userKeys?.openrouter_api_key;
> 423	+    const geminiKey = userKeys?.google_api_key;
> 424	     const aiKey = groqKey || openRouterKey;
> 425	 
> 426	     if (!aiKey) {
> 427	diff --git a/supabase/functions/generate-image/index.ts b/supabase/functions/generate-image/index.ts
> 428	index f68739b..4a5f25f 100644
> 429	--- a/supabase/functions/generate-image/index.ts
> 430	+++ b/supabase/functions/generate-image/index.ts
> 431	@@ -70,9 +70,9 @@ serve(async (req) => {
> 432	     const adminClient = createClient(supabaseUrl, serviceKey);
> 433	     const { data: userKeys } = await adminClient.from("decrypted_user_api_keys").select("*").eq("user_id", userId).maybeSingle();
> 434	 
> 435	-    const openaiKey = userKeys?.openai_api_key || Deno.env.get("OPENAI_API_KEY") || "";
> 436	-    const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY") || "";
> 437	-    const replicateKey = userKeys?.replicate_api_key || Deno.env.get("REPLICATE_API_KEY") || "";
> 438	+    const openaiKey = userKeys?.openai_api_key || "";
> 439	+    const openRouterKey = userKeys?.openrouter_api_key || "";
> 440	+    const replicateKey = userKeys?.replicate_api_key || "";
> 441	     const prefImage = userKeys?.pref_image_provider || "";
> 442	 
> 443	     const stylePrompt = style ? ` Style: ${style}.` : "";
> 444	diff --git a/supabase/functions/generate-video-script/index.ts b/supabase/functions/generate-video-script/index.ts
> 445	index 41b2659..8d370d9 100644
> 446	--- a/supabase/functions/generate-video-script/index.ts
> 447	+++ b/supabase/functions/generate-video-script/index.ts
> 448	@@ -122,7 +122,7 @@ serve(async (req) => {
> 449	       aiEndpoint = `https://generativelanguage.googleapis.com/v1beta/models/${selectedModel}:generateContent?key=${googleKey}`;
> 450	       isGoogleGemini = true;
> 451	     } else if (selectedProvider === "openrouter") {
> 452	-      const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 453	+      const openRouterKey = userKeys?.openrouter_api_key;
> 454	       if (!openRouterKey) {
> 455	         return new Response(JSON.stringify({ error: "Configure sua chave do OpenRouter em Configurações" }), {
> 456	           status: 400,
> 457	@@ -135,7 +135,7 @@ serve(async (req) => {
> 458	     } else {
> 459	       // Legacy fallback: Groq -> OpenRouter
> 460	       const groqKey = userKeys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 461	-      const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 462	+      const openRouterKey = userKeys?.openrouter_api_key;
> 463	       activeKey = groqKey || openRouterKey || "";
> 464	       const isGroq = !!groqKey;
> 465	       aiEndpoint = isGroq ? "https://api.groq.com/openai/v1/chat/completions" : "https://openrouter.ai/api/v1/chat/completions";
> 466	@@ -208,8 +208,8 @@ Responda sempre em português brasileiro. Seja criativo e profissional.`;
> 467	       });
> 468	 
> 469	       const groqKey = userKeys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 470	-      const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 471	-      const geminiKey = userKeys?.google_api_key || Deno.env.get("GEMINI_API_KEY");
> 472	+      const openRouterKey = userKeys?.openrouter_api_key;
> 473	+      const geminiKey = userKeys?.google_api_key;
> 474	 
> 475	       aiResponse = await fetchLLMWithFallback(aiEndpoint, {
> 476	         method: "POST",
> 477	diff --git a/supabase/functions/generate-video/index.ts b/supabase/functions/generate-video/index.ts
> 478	index 707c807..8fcb8b9 100644
> 479	--- a/supabase/functions/generate-video/index.ts
> 480	+++ b/supabase/functions/generate-video/index.ts
> 481	@@ -99,7 +99,7 @@ serve(async (req) => {
> 482	     // =====================================================
> 483	 
> 484	     if (selectedProvider === "openrouter") {
> 485	-      const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 486	+      const openRouterKey = userKeys?.openrouter_api_key;
> 487	       if (!openRouterKey) {
> 488	         return new Response(JSON.stringify({ error: "Configure sua chave do OpenRouter em Configurações" }), {
> 489	           status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" },
> 490	diff --git a/supabase/functions/intent-orchestrate/index.ts b/supabase/functions/intent-orchestrate/index.ts
> 491	index 41ca50d..406619a 100644
> 492	--- a/supabase/functions/intent-orchestrate/index.ts
> 493	+++ b/supabase/functions/intent-orchestrate/index.ts
> 494	@@ -38,8 +38,8 @@ serve(async (req) => {
> 495	     // resolve per-user AI key → system fallback (API Tenancy Model).
> 496	     const { data: keys } = await admin.from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 497	     const groqKey = keys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 498	-    const openRouterKey = keys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 499	-    const geminiKey = keys?.google_api_key || Deno.env.get("GEMINI_API_KEY");
> 500	+    const openRouterKey = keys?.openrouter_api_key;
> 501	+    const geminiKey = keys?.google_api_key;
> 502	     const aiKey = groqKey || openRouterKey;
> 503	 
> 504	     // generate the plan via AI (fail-soft to a single review task).
> 505	diff --git a/supabase/functions/lead-score/index.ts b/supabase/functions/lead-score/index.ts
> 506	index 310cd6f..24ce9fd 100644
> 507	--- a/supabase/functions/lead-score/index.ts
> 508	+++ b/supabase/functions/lead-score/index.ts
> 509	@@ -80,8 +80,8 @@ serve(async (req) => {
> 510	     // per-user AI key (API Tenancy Model) -> system fallback.
> 511	     const { data: userKeys } = await admin.from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 512	     const groqKey = userKeys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 513	-    const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 514	-    const geminiKey = userKeys?.google_api_key || Deno.env.get("GEMINI_API_KEY");
> 515	+    const openRouterKey = userKeys?.openrouter_api_key;
> 516	+    const geminiKey = userKeys?.google_api_key;
> 517	     const aiKey = groqKey || openRouterKey;
> 518	 
> 519	     let score: number | null = null;
> 520	diff --git a/supabase/functions/list-provider-models/index.ts b/supabase/functions/list-provider-models/index.ts
> 521	index 023bcce..1e751b6 100644
> 522	--- a/supabase/functions/list-provider-models/index.ts
> 523	+++ b/supabase/functions/list-provider-models/index.ts
> 524	@@ -169,7 +169,7 @@ serve(async (req) => {
> 525	         );
> 526	       }
> 527	     } else if (provider === "openrouter") {
> 528	-      const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 529	+      const openRouterKey = userKeys?.openrouter_api_key;
> 530	       if (!openRouterKey) {
> 531	         return new Response(JSON.stringify({ error: "key_missing", provider: "OpenRouter", models: [] }), {
> 532	           status: 200,
> 533	diff --git a/supabase/functions/nurture-dispatch/index.ts b/supabase/functions/nurture-dispatch/index.ts
> 534	index 4dfc903..3862ce6 100644
> 535	--- a/supabase/functions/nurture-dispatch/index.ts
> 536	+++ b/supabase/functions/nurture-dispatch/index.ts
> 537	@@ -108,8 +108,8 @@ serve(async (req) => {
> 538	     // generate the message (per-user AI key → system fallback, shared cascade). Fail-soft to a template.
> 539	     const { data: keys } = await admin.from("decrypted_user_api_keys").select("*").eq("user_id", userId).maybeSingle();
> 540	     const groqKey = keys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 541	-    const openRouterKey = keys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 542	-    const geminiKey = keys?.google_api_key || Deno.env.get("GEMINI_API_KEY");
> 543	+    const openRouterKey = keys?.openrouter_api_key;
> 544	+    const geminiKey = keys?.google_api_key;
> 545	     const aiKey = groqKey || openRouterKey;
> 546	     let message = step.prompt ? `(${step.prompt})` : `Mensagem da sequência "${seq.name}" (passo ${enr.current_step + 1}).`;
> 547	     if (aiKey && step.prompt) {
> 548	diff --git a/supabase/functions/openrouter-swarm/index.ts b/supabase/functions/openrouter-swarm/index.ts
> 549	index f160b8d..5d63a1a 100644
> 550	--- a/supabase/functions/openrouter-swarm/index.ts
> 551	+++ b/supabase/functions/openrouter-swarm/index.ts
> 552	@@ -111,9 +111,30 @@ Deno.serve(async (req) => {
> 553	     return respond({ error: "Unauthorized" }, 401);
> 554	   }
> 555	 
> 556	-  const apiKey = Deno.env.get("OPENROUTER_API_KEY");
> 557	+  // Per-user credential resolution (API Tenancy Model): the user's BYOK OpenRouter key FIRST; the platform key is a
> 558	+  // restricted fallback only — so a tenant's swarm spend is attributed to / quota-isolated by their own credential.
> 559	+  const adminClient = createClient(
> 560	+    Deno.env.get("SUPABASE_URL")!,
> 561	+    (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
> 562	+  );
> 563	+  const { data: userKeys } = await adminClient
> 564	+    .from("decrypted_user_api_keys")
> 565	+    .select("openrouter_api_key")
> 566	+    .eq("user_id", user.id)
> 567	+    .maybeSingle();
> 568	+
> 569	+  const apiKey = userKeys?.openrouter_api_key;
> 570	   if (!apiKey) {
> 571	-    return respond({ error: "OPENROUTER_API_KEY not configured" }, 500);
> 572	+    await adminClient.from("infra_health_logs").insert({
> 573	+      service: "openrouter-swarm",
> 574	+      status: "error",
> 575	+      message: "OpenRouter não configurado (nem per-user nem fallback de plataforma)",
> 576	+      metadata: { user_id: user.id },
> 577	+    }).then(() => {}, () => {});
> 578	+    return respond(
> 579	+      { error: "openrouter_not_configured", action: "Configure sua chave OpenRouter em /dashboard/settings" },
> 580	+      501,
> 581	+    );
> 582	   }
> 583	 
> 584	   let prompt: string;
> 585	diff --git a/supabase/functions/optimize-schedule/index.ts b/supabase/functions/optimize-schedule/index.ts
> 586	index be79e19..84b6938 100644
> 587	--- a/supabase/functions/optimize-schedule/index.ts
> 588	+++ b/supabase/functions/optimize-schedule/index.ts
> 589	@@ -51,8 +51,8 @@ Deno.serve(async (req) => {
> 590	     const { data: userKeys } = await admin.from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 591	 
> 592	     const groqKey = userKeys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 593	-    const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 594	-    const geminiKey = userKeys?.google_api_key || Deno.env.get("GEMINI_API_KEY");
> 595	+    const openRouterKey = userKeys?.openrouter_api_key;
> 596	+    const geminiKey = userKeys?.google_api_key;
> 597	     const aiKey = groqKey || openRouterKey;
> 598	 
> 599	     if (!aiKey) {
> 600	diff --git a/supabase/functions/orchestrate-content/index.ts b/supabase/functions/orchestrate-content/index.ts
> 601	index cd02f1f..788493d 100644
> 602	--- a/supabase/functions/orchestrate-content/index.ts
> 603	+++ b/supabase/functions/orchestrate-content/index.ts
> 604	@@ -78,7 +78,7 @@ Deno.serve(async (req) => {
> 605	     // pre-flight: check AI keys before charging user
> 606	     const { data: userKeys } = await admin.from("decrypted_user_api_keys").select("*").eq("user_id", userId).maybeSingle();
> 607	     const groqKey = userKeys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 608	-    const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 609	+    const openRouterKey = userKeys?.openrouter_api_key;
> 610	 
> 611	     const prefModel = userKeys?.pref_ai_model ?? null;
> 612	     const prefRequiresOR = prefModel && (prefModel.includes("/") || prefModel.startsWith("gemini-"));
> 613	diff --git a/supabase/functions/orchestrate-step/index.ts b/supabase/functions/orchestrate-step/index.ts
> 614	index 658036f..1a89da8 100644
> 615	--- a/supabase/functions/orchestrate-step/index.ts
> 616	+++ b/supabase/functions/orchestrate-step/index.ts
> 617	@@ -240,8 +240,8 @@ Deno.serve(async (req) => {
> 618	       .maybeSingle();
> 619	 
> 620	     const groqKey = userKeys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 621	-    const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 622	-    const geminiKey = userKeys?.google_api_key || Deno.env.get("GEMINI_API_KEY");
> 623	+    const openRouterKey = userKeys?.openrouter_api_key;
> 624	+    const geminiKey = userKeys?.google_api_key;
> 625	     const prefModel = userKeys?.pref_ai_model ?? null;
> 626	     const prefRequiresOR = prefModel && (prefModel.includes("/") || prefModel.startsWith("gemini-"));
> 627	     const aiKey = prefRequiresOR ? (openRouterKey || groqKey) : (groqKey || openRouterKey);
> 628	diff --git a/supabase/functions/search-constellation/index.ts b/supabase/functions/search-constellation/index.ts
> 629	index e629f1b..719812c 100644
> 630	--- a/supabase/functions/search-constellation/index.ts
> 631	+++ b/supabase/functions/search-constellation/index.ts
> 632	@@ -112,9 +112,10 @@ Deno.serve(async (req) => {
> 633	     (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
> 634	   );
> 635	 
> 636	-  const openRouterKey = Deno.env.get("OPENROUTER_API_KEY");
> 637	-  const geminiKey = Deno.env.get("GEMINI_API_KEY");
> 638	-  if (!openRouterKey && !geminiKey) return err(500, "Neither OPENROUTER_API_KEY nor GEMINI_API_KEY configured");
> 639	+  // INFRA: dedicated mesh-embedding system keys (system-role search, no user-facing BYOK fallback — API Tenancy Model).
> 640	+  const openRouterKey = Deno.env.get("MESH_EMBED_OPENROUTER_KEY");
> 641	+  const geminiKey = Deno.env.get("MESH_EMBED_GEMINI_KEY");
> 642	+  if (!openRouterKey && !geminiKey) return err(500, "Neither MESH_EMBED_OPENROUTER_KEY nor MESH_EMBED_GEMINI_KEY configured");
> 643	 
> 644	   let query: string;
> 645	   let project_id: string;
> 646	diff --git a/supabase/functions/self-optimize/index.ts b/supabase/functions/self-optimize/index.ts
> 647	index 3144f21..c6301c9 100644
> 648	--- a/supabase/functions/self-optimize/index.ts
> 649	+++ b/supabase/functions/self-optimize/index.ts
> 650	@@ -50,8 +50,8 @@ Deno.serve(async (req) => {
> 651	     
> 652	     // Adaptive Lookup with Fallback
> 653	     const groqKey = userKeys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 654	-    const openRouterKey = userKeys?.openrouter_api_key || Deno.env.get("OPENROUTER_API_KEY");
> 655	-    const geminiKey = userKeys?.google_api_key || Deno.env.get("GEMINI_API_KEY");
> 656	+    const openRouterKey = userKeys?.openrouter_api_key;
> 657	+    const geminiKey = userKeys?.google_api_key;
> 658	     const aiKey = groqKey || openRouterKey;
> 659	 
> 660	     if (!aiKey) throw new Error("GROQ_API_KEY or OPENROUTER_API_KEY not configured");
> 661	diff --git a/supabase/functions/tts-speak/index.ts b/supabase/functions/tts-speak/index.ts
> 662	index 1362564..58d23aa 100644
> 663	--- a/supabase/functions/tts-speak/index.ts
> 664	+++ b/supabase/functions/tts-speak/index.ts
> 665	@@ -73,7 +73,7 @@ Deno.serve(async (req) => {
> 666	     .eq("user_id", user.id)
> 667	     .maybeSingle();
> 668	 
> 669	-  const geminiKey = userKeys?.google_api_key || Deno.env.get("GEMINI_API_KEY");
> 670	+  const geminiKey = userKeys?.google_api_key;
> 671	   if (!geminiKey) return respond({ error: "GEMINI_API_KEY not configured" }, 500);
> 672	 
> 673	   let text: string;
> 674	
> ```

## 🤖 Claude *(02:02:55)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260622210000_user_api_keys_rapidapi_channel.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: per-user RapidAPI BYOK — fetch-trends per-user (#3 do sweep de prontidão per-user, API Tenancy Model).
> 2	-- SOP SSOT: docs/processes/trends-credential-resolution.md + API Tenancy Model (CLAUDE.md).
> 3	--
> 4	-- Sovereign directive 2026-06-22 ("tudo que é per-user sempre é prioridade"): fetch-trends resolve as credenciais
> 5	-- de trends per-user. apify_token JÁ EXISTE (20260615140000); aqui só acrescentamos rapidapi_key ao maquinário
> 6	-- cifrado do user_api_keys, reproduzindo o ÚLTIMO live def VERBATIM (20260615140000_user_api_keys_firecrawl_channel.sql):
> 7	-- encrypt trigger usa vault_upsert_secret idempotente (20260602140000); INSTEAD OF é UPDATE-first + tenant guard
> 8	-- (20260602130000); search_path='' preservado. Aditivo: views acrescentam a coluna nova no FIM.
> 9	
> 10	-- ── 1. base column ──────────────────────────────────────────────────────────────────────────────
> 11	ALTER TABLE public.user_api_keys_table ADD COLUMN IF NOT EXISTS rapidapi_key text;
> 12	COMMENT ON COLUMN public.user_api_keys_table.rapidapi_key
> 13	  IS 'Per-user RapidAPI key (BYOK) for fetch-trends. Vault-encrypted at rest. NULL → 402 trends_not_configured (no system fallback in user-facing flow).';
> 14	
> 15	-- ── 2. encrypt trigger (live verbatim + rapidapi_key; idempotent vault_upsert_secret) ────────────
> 16	CREATE OR REPLACE FUNCTION public.trg_encrypt_user_api_keys()
> 17	 RETURNS trigger
> 18	 LANGUAGE plpgsql
> 19	 SECURITY DEFINER
> 20	 SET search_path TO ''
> 21	AS $function$
> 22	DECLARE
> 23	  v_id UUID;
> 24	BEGIN
> 25	  IF NEW.groq_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.groq_api_key IS DISTINCT FROM OLD.groq_api_key) THEN
> 26	    IF NEW.groq_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 27	      v_id := public.vault_upsert_secret(NEW.groq_api_key, 'user_api_keys_groq_api_key_' || NEW.user_id::text, 'Groq API Key'); NEW.groq_api_key = v_id::text;
> 28	    END IF;
> 29	  END IF;
> 30	  IF NEW.openrouter_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openrouter_api_key IS DISTINCT FROM OLD.openrouter_api_key) THEN
> 31	    IF NEW.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 32	      v_id := public.vault_upsert_secret(NEW.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || NEW.user_id::text, 'OpenRouter API Key'); NEW.openrouter_api_key = v_id::text;
> 33	    END IF;
> 34	  END IF;
> 35	  IF NEW.openai_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openai_api_key IS DISTINCT FROM OLD.openai_api_key) THEN
> 36	    IF NEW.openai_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 37	      v_id := public.vault_upsert_secret(NEW.openai_api_key, 'user_api_keys_openai_api_key_' || NEW.user_id::text, 'OpenAI API Key'); NEW.openai_api_key = v_id::text;
> 38	    END IF;
> 39	  END IF;
> 40	  IF NEW.elevenlabs_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.elevenlabs_api_key IS DISTINCT FROM OLD.elevenlabs_api_key) THEN
> 41	    IF NEW.elevenlabs_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 42	      v_id := public.vault_upsert_secret(NEW.elevenlabs_api_key, 'user_api_keys_elevenlabs_api_key_' || NEW.user_id::text, 'ElevenLabs API Key'); NEW.elevenlabs_api_key = v_id::text;
> 43	    END IF;
> 44	  END IF;
> 45	  IF NEW.google_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.google_api_key IS DISTINCT FROM OLD.google_api_key) THEN
> 46	    IF NEW.google_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 47	      v_id := public.vault_upsert_secret(NEW.google_api_key, 'user_api_keys_google_api_key_' || NEW.user_id::text, 'Google API Key'); NEW.google_api_key = v_id::text;
> 48	    END IF;
> 49	  END IF;
> 50	  IF NEW.nanobana_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.nanobana_api_key IS DISTINCT FROM OLD.nanobana_api_key) THEN
> 51	    IF NEW.nanobana_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 52	      v_id := public.vault_upsert_secret(NEW.nanobana_api_key, 'user_api_keys_nanobana_api_key_' || NEW.user_id::text, 'Nanobana API Key'); NEW.nanobana_api_key = v_id::text;
> 53	    END IF;
> 54	  END IF;
> 55	  IF NEW.seedance_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.seedance_api_key IS DISTINCT FROM OLD.seedance_api_key) THEN
> 56	    IF NEW.seedance_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 57	      v_id := public.vault_upsert_secret(NEW.seedance_api_key, 'user_api_keys_seedance_api_key_' || NEW.user_id::text, 'Seedance API Key'); NEW.seedance_api_key = v_id::text;
> 58	    END IF;
> 59	  END IF;
> 60	  IF NEW.wp_app_password IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.wp_app_password IS DISTINCT FROM OLD.wp_app_password) THEN
> 61	    IF NEW.wp_app_password ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 62	      v_id := public.vault_upsert_secret(NEW.wp_app_password, 'user_api_keys_wp_app_password_' || NEW.user_id::text, 'WordPress App Password'); NEW.wp_app_password = v_id::text;
> 63	    END IF;
> 64	  END IF;
> 65	  IF NEW.replicate_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.replicate_api_key IS DISTINCT FROM OLD.replicate_api_key) THEN
> 66	    IF NEW.replicate_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 67	      v_id := public.vault_upsert_secret(NEW.replicate_api_key, 'user_api_keys_replicate_api_key_' || NEW.user_id::text, 'Replicate API Key'); NEW.replicate_api_key = v_id::text;
> 68	    END IF;
> 69	  END IF;
> 70	  IF NEW.higgsfield_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.higgsfield_api_key IS DISTINCT FROM OLD.higgsfield_api_key) THEN
> 71	    IF NEW.higgsfield_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 72	      v_id := public.vault_upsert_secret(NEW.higgsfield_api_key, 'user_api_keys_higgsfield_api_key_' || NEW.user_id::text, 'Higgsfield API Key'); NEW.higgsfield_api_key = v_id::text;
> 73	    END IF;
> 74	  END IF;
> 75	  IF NEW.higgsfield_api_key_secret IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.higgsfield_api_key_secret IS DISTINCT FROM OLD.higgsfield_api_key_secret) THEN
> 76	    IF NEW.higgsfield_api_key_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 77	      v_id := public.vault_upsert_secret(NEW.higgsfield_api_key_secret, 'user_api_keys_higgsfield_api_key_secret_' || NEW.user_id::text, 'Higgsfield API Key Secret'); NEW.higgsfield_api_key_secret = v_id::text;
> 78	    END IF;
> 79	  END IF;
> 80	  IF NEW.apify_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.apify_token IS DISTINCT FROM OLD.apify_token) THEN
> 81	    IF NEW.apify_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 82	      v_id := public.vault_upsert_secret(NEW.apify_token, 'user_api_keys_apify_token_' || NEW.user_id::text, 'Apify Token'); NEW.apify_token = v_id::text;
> 83	    END IF;
> 84	  END IF;
> 85	  IF NEW.resend_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.resend_api_key IS DISTINCT FROM OLD.resend_api_key) THEN
> 86	    IF NEW.resend_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 87	      v_id := public.vault_upsert_secret(NEW.resend_api_key, 'user_api_keys_resend_api_key_' || NEW.user_id::text, 'Resend API Key'); NEW.resend_api_key = v_id::text;
> 88	    END IF;
> 89	  END IF;
> 90	  IF NEW.firecrawl_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.firecrawl_api_key IS DISTINCT FROM OLD.firecrawl_api_key) THEN
> 91	    IF NEW.firecrawl_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 92	      v_id := public.vault_upsert_secret(NEW.firecrawl_api_key, 'user_api_keys_firecrawl_api_key_' || NEW.user_id::text, 'Firecrawl API Key'); NEW.firecrawl_api_key = v_id::text;
> 93	    END IF;
> 94	  END IF;
> 95	  -- rapidapi_key (NEW — per-user fetch-trends BYOK)
> 96	  IF NEW.rapidapi_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.rapidapi_key IS DISTINCT FROM OLD.rapidapi_key) THEN
> 97	    IF NEW.rapidapi_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 98	      v_id := public.vault_upsert_secret(NEW.rapidapi_key, 'user_api_keys_rapidapi_key_' || NEW.user_id::text, 'RapidAPI Key'); NEW.rapidapi_key = v_id::text;
> 99	    END IF;
> 100	  END IF;
> 101	  RETURN NEW;
> 102	END;
> 103	$function$;
> 104	
> 105	-- ── 3. masked public view (live verbatim + rapidapi_key masked, appended at END) ─────────────────
> 106	CREATE OR REPLACE VIEW public.user_api_keys AS
> 107	SELECT
> 108	  user_id, created_at, updated_at, pref_audio_provider, pref_image_provider, pref_video_provider,
> 109	  wp_site_url, wp_username, pref_ai_model,
> 110	  CASE WHEN groq_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS groq_api_key,
> 111	  CASE WHEN openrouter_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS openrouter_api_key,
> 112	  CASE WHEN openai_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS openai_api_key,
> 113	  CASE WHEN elevenlabs_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS elevenlabs_api_key,
> 114	  CASE WHEN google_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS google_api_key,
> 115	  CASE WHEN nanobana_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS nanobana_api_key,
> 116	  CASE WHEN seedance_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS seedance_api_key,
> 117	  CASE WHEN wp_app_password IS NOT NULL THEN '••••••••••••' ELSE NULL END AS wp_app_password,
> 118	  CASE WHEN replicate_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS replicate_api_key,
> 119	  CASE WHEN higgsfield_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS higgsfield_api_key,
> 120	  CASE WHEN higgsfield_api_key_secret IS NOT NULL THEN '••••••••••••' ELSE NULL END AS higgsfield_api_key_secret,
> 121	  CASE WHEN apify_token IS NOT NULL THEN '••••••••••••' ELSE NULL END AS apify_token,
> 122	  CASE WHEN resend_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS resend_api_key,
> 123	  CASE WHEN firecrawl_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS firecrawl_api_key,
> 124	  CASE WHEN rapidapi_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS rapidapi_key
> 125	FROM public.user_api_keys_table
> 126	WHERE (auth.uid() = user_id OR auth.role() = 'service_role');
> 127	GRANT SELECT, INSERT, UPDATE, DELETE ON public.user_api_keys TO anon, authenticated;
> 128	
> 129	-- ── 4. INSTEAD OF trigger (live verbatim + rapidapi_key in UPDATE-first/INSERT, tenant-guarded) ───
> 130	CREATE OR REPLACE FUNCTION public.trg_instead_of_user_api_keys()
> 131	 RETURNS trigger
> 132	 LANGUAGE plpgsql
> 133	 SECURITY DEFINER
> 134	 SET search_path TO ''
> 135	AS $function$
> 136	BEGIN
> 137	  IF TG_OP = 'DELETE' THEN
> 138	    DELETE FROM public.user_api_keys_table WHERE user_id = OLD.user_id;
> 139	    RETURN OLD;
> 140	  ELSIF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
> 141	    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN
> 142	      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';
> 143	    END IF;
> 144	    UPDATE public.user_api_keys_table SET
> 145	      groq_api_key              = COALESCE(NULLIF(NEW.groq_api_key, '••••••••••••'), public.user_api_keys_table.groq_api_key),
> 146	      openrouter_api_key        = COALESCE(NULLIF(NEW.openrouter_api_key, '••••••••••••'), public.user_api_keys_table.openrouter_api_key),
> 147	      openai_api_key            = COALESCE(NULLIF(NEW.openai_api_key, '••••••••••••'), public.user_api_keys_table.openai_api_key),
> 148	      pref_audio_provider       = COALESCE(NEW.pref_audio_provider, public.user_api_keys_table.pref_audio_provider),
> 149	      pref_image_provider       = COALESCE(NEW.pref_image_provider, public.user_api_keys_table.pref_image_provider),
> 150	      pref_video_provider       = COALESCE(NEW.pref_video_provider, public.user_api_keys_table.pref_video_provider),
> 151	      elevenlabs_api_key        = COALESCE(NULLIF(NEW.elevenlabs_api_key, '••••••••••••'), public.user_api_keys_table.elevenlabs_api_key),
> 152	      google_api_key            = COALESCE(NULLIF(NEW.google_api_key, '••••••••••••'), public.user_api_keys_table.google_api_key),
> 153	      nanobana_api_key          = COALESCE(NULLIF(NEW.nanobana_api_key, '••••••••••••'), public.user_api_keys_table.nanobana_api_key),
> 154	      seedance_api_key          = COALESCE(NULLIF(NEW.seedance_api_key, '••••••••••••'), public.user_api_keys_table.seedance_api_key),
> 155	      wp_site_url               = COALESCE(NEW.wp_site_url, public.user_api_keys_table.wp_site_url),
> 156	      wp_username               = COALESCE(NEW.wp_username, public.user_api_keys_table.wp_username),
> 157	      wp_app_password           = COALESCE(NULLIF(NEW.wp_app_password, '••••••••••••'), public.user_api_keys_table.wp_app_password),
> 158	      pref_ai_model             = COALESCE(NEW.pref_ai_model, public.user_api_keys_table.pref_ai_model),
> 159	      replicate_api_key         = COALESCE(NULLIF(NEW.replicate_api_key, '••••••••••••'), public.user_api_keys_table.replicate_api_key),
> 160	      higgsfield_api_key        = COALESCE(NULLIF(NEW.higgsfield_api_key, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key),
> 161	      higgsfield_api_key_secret = COALESCE(NULLIF(NEW.higgsfield_api_key_secret, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key_secret),
> 162	      apify_token               = COALESCE(NULLIF(NEW.apify_token, '••••••••••••'), public.user_api_keys_table.apify_token),
> 163	      resend_api_key            = COALESCE(NULLIF(NEW.resend_api_key, '••••••••••••'), public.user_api_keys_table.resend_api_key),
> 164	      firecrawl_api_key         = COALESCE(NULLIF(NEW.firecrawl_api_key, '••••••••••••'), public.user_api_keys_table.firecrawl_api_key),
> 165	      rapidapi_key              = COALESCE(NULLIF(NEW.rapidapi_key, '••••••••••••'), public.user_api_keys_table.rapidapi_key),
> 166	      updated_at                = now()
> 167	    WHERE user_id = NEW.user_id;
> 168	    IF NOT FOUND THEN
> 169	      INSERT INTO public.user_api_keys_table (
> 170	        user_id, groq_api_key, openrouter_api_key, openai_api_key, pref_audio_provider, pref_image_provider, pref_video_provider, elevenlabs_api_key, google_api_key, nanobana_api_key, seedance_api_key, wp_site_url, wp_username, wp_app_password, pref_ai_model, replicate_api_key, higgsfield_api_key, higgsfield_api_key_secret, apify_token, resend_api_key, firecrawl_api_key, rapidapi_key
> 171	      ) VALUES (
> 172	        NEW.user_id, NEW.groq_api_key, NEW.openrouter_api_key, NEW.openai_api_key, NEW.pref_audio_provider, NEW.pref_image_provider, NEW.pref_video_provider, NEW.elevenlabs_api_key, NEW.google_api_key, NEW.nanobana_api_key, NEW.seedance_api_key, NEW.wp_site_url, NEW.wp_username, NEW.wp_app_password, NEW.pref_ai_model, NEW.replicate_api_key, NEW.higgsfield_api_key, NEW.higgsfield_api_key_secret, NEW.apify_token, NEW.resend_api_key, NEW.firecrawl_api_key, NEW.rapidapi_key
> 173	      );
> 174	    END IF;
> 175	    RETURN NEW;
> 176	  END IF;
> 177	  RETURN NULL;
> 178	END;
> 179	$function$;
> 180	
> 181	-- ── 5. decrypted view (service_role only; live verbatim + rapidapi_key COALESCE + join at END) ────
> 182	CREATE OR REPLACE VIEW public.decrypted_user_api_keys AS
> 183	SELECT
> 184	  uak.user_id,
> 185	  COALESCE(s_groq.decrypted_secret, uak.groq_api_key) AS groq_api_key,
> 186	  COALESCE(s_openrouter.decrypted_secret, uak.openrouter_api_key) AS openrouter_api_key,
> 187	  COALESCE(s_openai.decrypted_secret, uak.openai_api_key) AS openai_api_key,
> 188	  uak.created_at, uak.updated_at, uak.pref_audio_provider, uak.pref_image_provider, uak.pref_video_provider,
> 189	  COALESCE(s_elevenlabs.decrypted_secret, uak.elevenlabs_api_key) AS elevenlabs_api_key,
> 190	  COALESCE(s_google.decrypted_secret, uak.google_api_key) AS google_api_key,
> 191	  COALESCE(s_nanobana.decrypted_secret, uak.nanobana_api_key) AS nanobana_api_key,
> 192	  COALESCE(s_seedance.decrypted_secret, uak.seedance_api_key) AS seedance_api_key,
> 193	  uak.wp_site_url, uak.wp_username,
> 194	  COALESCE(s_wp_pwd.decrypted_secret, uak.wp_app_password) AS wp_app_password,
> 195	  uak.pref_ai_model,
> 196	  COALESCE(s_replicate.decrypted_secret, uak.replicate_api_key) AS replicate_api_key,
> 197	  COALESCE(s_higgsfield.decrypted_secret, uak.higgsfield_api_key) AS higgsfield_api_key,
> 198	  COALESCE(s_higgsfield_sec.decrypted_secret, uak.higgsfield_api_key_secret) AS higgsfield_api_key_secret,
> 199	  COALESCE(s_apify.decrypted_secret, uak.apify_token) AS apify_token,
> 200	  COALESCE(s_resend.decrypted_secret, uak.resend_api_key) AS resend_api_key,
> 201	  COALESCE(s_firecrawl.decrypted_secret, uak.firecrawl_api_key) AS firecrawl_api_key,
> 202	  COALESCE(s_rapidapi.decrypted_secret, uak.rapidapi_key) AS rapidapi_key
> 203	FROM public.user_api_keys_table uak
> 204	LEFT JOIN vault.decrypted_secrets s_groq ON uak.groq_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_groq.id = uak.groq_api_key::uuid
> 205	LEFT JOIN vault.decrypted_secrets s_openrouter ON uak.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_openrouter.id = uak.openrouter_api_key::uuid
> 206	LEFT JOIN vault.decrypted_secrets s_openai ON uak.openai_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_openai.id = uak.openai_api_key::uuid
> 207	LEFT JOIN vault.decrypted_secrets s_elevenlabs ON uak.elevenlabs_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_elevenlabs.id = uak.elevenlabs_api_key::uuid
> 208	LEFT JOIN vault.decrypted_secrets s_google ON uak.google_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_google.id = uak.google_api_key::uuid
> 209	LEFT JOIN vault.decrypted_secrets s_nanobana ON uak.nanobana_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_nanobana.id = uak.nanobana_api_key::uuid
> 210	LEFT JOIN vault.decrypted_secrets s_seedance ON uak.seedance_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_seedance.id = uak.seedance_api_key::uuid
> 211	LEFT JOIN vault.decrypted_secrets s_wp_pwd ON uak.wp_app_password ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_wp_pwd.id = uak.wp_app_password::uuid
> 212	LEFT JOIN vault.decrypted_secrets s_replicate ON uak.replicate_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_replicate.id = uak.replicate_api_key::uuid
> 213	LEFT JOIN vault.decrypted_secrets s_higgsfield ON uak.higgsfield_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_higgsfield.id = uak.higgsfield_api_key::uuid
> 214	LEFT JOIN vault.decrypted_secrets s_higgsfield_sec ON uak.higgsfield_api_key_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_higgsfield_sec.id = uak.higgsfield_api_key_secret::uuid
> 215	LEFT JOIN vault.decrypted_secrets s_apify ON uak.apify_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_apify.id = uak.apify_token::uuid
> 216	LEFT JOIN vault.decrypted_secrets s_resend ON uak.resend_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_resend.id = uak.resend_api_key::uuid
> 217	LEFT JOIN vault.decrypted_secrets s_firecrawl ON uak.firecrawl_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_firecrawl.id = uak.firecrawl_api_key::uuid
> 218	LEFT JOIN vault.decrypted_secrets s_rapidapi ON uak.rapidapi_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_rapidapi.id = uak.rapidapi_key::uuid;
> 219	REVOKE ALL ON public.decrypted_user_api_keys FROM PUBLIC, anon, authenticated;
> 220	GRANT SELECT ON public.decrypted_user_api_keys TO service_role;
> 221	
> ```

## 🤖 Claude *(02:02:55)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260615140000_user_api_keys_firecrawl_channel.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: per-user Firecrawl (deepsearch.scrape) BYOK — vision-mcp Fatia 2 / FR-VM-007.
> 2	-- BoK SSOT: docs/bok/vision-mcp/04-frd.md FR-VM-007 (deepsearch) + 03-prd PR-VM-008 + API Tenancy Model
> 3	-- (CLAUDE.md) + SOP docs/processes/vision-mcp-billing-credential-resolution.md.
> 4	--
> 5	-- Sovereign directive 2026-06-15 ("usar as chaves já configuradas per-user BYOK para o deepsearch"):
> 6	-- deepsearch.scrape resolves the Firecrawl key per-user (BYOK). Lays the credential column the
> 7	-- vision-mcp container reads from `decrypted_user_api_keys` (service-role) by the verified sub.
> 8	--
> 9	-- Appends `firecrawl_api_key` to the user_api_keys credential machinery, reproducing the CURRENT live
> 10	-- definitions VERBATIM (from 20260603240000_user_api_keys_resend_channel.sql — the latest live def):
> 11	-- encrypt trigger uses the IDEMPOTENT `vault_upsert_secret` (20260602140000); the INSTEAD OF is
> 12	-- UPDATE-first + tenant guard (20260602130000); search_path='' preserved. Additive only: views append
> 13	-- the new column at the END (CREATE OR REPLACE VIEW constraint).
> 14	
> 15	-- ── 1. base column ──────────────────────────────────────────────────────────────────────────────
> 16	ALTER TABLE public.user_api_keys_table ADD COLUMN IF NOT EXISTS firecrawl_api_key text;
> 17	COMMENT ON COLUMN public.user_api_keys_table.firecrawl_api_key
> 18	  IS 'Per-user Firecrawl API key (BYOK) for vision-mcp deepsearch.scrape. Vault-encrypted at rest. NULL → 402 firecrawl_not_configured (no system fallback).';
> 19	
> 20	-- ── 2. encrypt trigger (live verbatim + firecrawl block; idempotent vault_upsert_secret) ─────────
> 21	CREATE OR REPLACE FUNCTION public.trg_encrypt_user_api_keys()
> 22	 RETURNS trigger
> 23	 LANGUAGE plpgsql
> 24	 SECURITY DEFINER
> 25	 SET search_path TO ''
> 26	AS $function$
> 27	DECLARE
> 28	  v_id UUID;
> 29	BEGIN
> 30	  IF NEW.groq_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.groq_api_key IS DISTINCT FROM OLD.groq_api_key) THEN
> 31	    IF NEW.groq_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 32	      v_id := public.vault_upsert_secret(NEW.groq_api_key, 'user_api_keys_groq_api_key_' || NEW.user_id::text, 'Groq API Key'); NEW.groq_api_key = v_id::text;
> 33	    END IF;
> 34	  END IF;
> 35	  IF NEW.openrouter_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openrouter_api_key IS DISTINCT FROM OLD.openrouter_api_key) THEN
> 36	    IF NEW.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 37	      v_id := public.vault_upsert_secret(NEW.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || NEW.user_id::text, 'OpenRouter API Key'); NEW.openrouter_api_key = v_id::text;
> 38	    END IF;
> 39	  END IF;
> 40	  IF NEW.openai_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openai_api_key IS DISTINCT FROM OLD.openai_api_key) THEN
> 41	    IF NEW.openai_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 42	      v_id := public.vault_upsert_secret(NEW.openai_api_key, 'user_api_keys_openai_api_key_' || NEW.user_id::text, 'OpenAI API Key'); NEW.openai_api_key = v_id::text;
> 43	    END IF;
> 44	  END IF;
> 45	  IF NEW.elevenlabs_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.elevenlabs_api_key IS DISTINCT FROM OLD.elevenlabs_api_key) THEN
> 46	    IF NEW.elevenlabs_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 47	      v_id := public.vault_upsert_secret(NEW.elevenlabs_api_key, 'user_api_keys_elevenlabs_api_key_' || NEW.user_id::text, 'ElevenLabs API Key'); NEW.elevenlabs_api_key = v_id::text;
> 48	    END IF;
> 49	  END IF;
> 50	  IF NEW.google_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.google_api_key IS DISTINCT FROM OLD.google_api_key) THEN
> 51	    IF NEW.google_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 52	      v_id := public.vault_upsert_secret(NEW.google_api_key, 'user_api_keys_google_api_key_' || NEW.user_id::text, 'Google API Key'); NEW.google_api_key = v_id::text;
> 53	    END IF;
> 54	  END IF;
> 55	  IF NEW.nanobana_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.nanobana_api_key IS DISTINCT FROM OLD.nanobana_api_key) THEN
> 56	    IF NEW.nanobana_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 57	      v_id := public.vault_upsert_secret(NEW.nanobana_api_key, 'user_api_keys_nanobana_api_key_' || NEW.user_id::text, 'Nanobana API Key'); NEW.nanobana_api_key = v_id::text;
> 58	    END IF;
> 59	  END IF;
> 60	  IF NEW.seedance_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.seedance_api_key IS DISTINCT FROM OLD.seedance_api_key) THEN
> 61	    IF NEW.seedance_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 62	      v_id := public.vault_upsert_secret(NEW.seedance_api_key, 'user_api_keys_seedance_api_key_' || NEW.user_id::text, 'Seedance API Key'); NEW.seedance_api_key = v_id::text;
> 63	    END IF;
> 64	  END IF;
> 65	  IF NEW.wp_app_password IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.wp_app_password IS DISTINCT FROM OLD.wp_app_password) THEN
> 66	    IF NEW.wp_app_password ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 67	      v_id := public.vault_upsert_secret(NEW.wp_app_password, 'user_api_keys_wp_app_password_' || NEW.user_id::text, 'WordPress App Password'); NEW.wp_app_password = v_id::text;
> 68	    END IF;
> 69	  END IF;
> 70	  IF NEW.replicate_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.replicate_api_key IS DISTINCT FROM OLD.replicate_api_key) THEN
> 71	    IF NEW.replicate_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 72	      v_id := public.vault_upsert_secret(NEW.replicate_api_key, 'user_api_keys_replicate_api_key_' || NEW.user_id::text, 'Replicate API Key'); NEW.replicate_api_key = v_id::text;
> 73	    END IF;
> 74	  END IF;
> 75	  IF NEW.higgsfield_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.higgsfield_api_key IS DISTINCT FROM OLD.higgsfield_api_key) THEN
> 76	    IF NEW.higgsfield_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 77	      v_id := public.vault_upsert_secret(NEW.higgsfield_api_key, 'user_api_keys_higgsfield_api_key_' || NEW.user_id::text, 'Higgsfield API Key'); NEW.higgsfield_api_key = v_id::text;
> 78	    END IF;
> 79	  END IF;
> 80	  IF NEW.higgsfield_api_key_secret IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.higgsfield_api_key_secret IS DISTINCT FROM OLD.higgsfield_api_key_secret) THEN
> 81	    IF NEW.higgsfield_api_key_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 82	      v_id := public.vault_upsert_secret(NEW.higgsfield_api_key_secret, 'user_api_keys_higgsfield_api_key_secret_' || NEW.user_id::text, 'Higgsfield API Key Secret'); NEW.higgsfield_api_key_secret = v_id::text;
> 83	    END IF;
> 84	  END IF;
> 85	  IF NEW.apify_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.apify_token IS DISTINCT FROM OLD.apify_token) THEN
> 86	    IF NEW.apify_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 87	      v_id := public.vault_upsert_secret(NEW.apify_token, 'user_api_keys_apify_token_' || NEW.user_id::text, 'Apify Token'); NEW.apify_token = v_id::text;
> 88	    END IF;
> 89	  END IF;
> 90	  IF NEW.resend_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.resend_api_key IS DISTINCT FROM OLD.resend_api_key) THEN
> 91	    IF NEW.resend_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 92	      v_id := public.vault_upsert_secret(NEW.resend_api_key, 'user_api_keys_resend_api_key_' || NEW.user_id::text, 'Resend API Key'); NEW.resend_api_key = v_id::text;
> 93	    END IF;
> 94	  END IF;
> 95	  -- firecrawl_api_key (NEW — per-user deepsearch.scrape BYOK)
> 96	  IF NEW.firecrawl_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.firecrawl_api_key IS DISTINCT FROM OLD.firecrawl_api_key) THEN
> 97	    IF NEW.firecrawl_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 98	      v_id := public.vault_upsert_secret(NEW.firecrawl_api_key, 'user_api_keys_firecrawl_api_key_' || NEW.user_id::text, 'Firecrawl API Key'); NEW.firecrawl_api_key = v_id::text;
> 99	    END IF;
> 100	  END IF;
> 101	  RETURN NEW;
> 102	END;
> 103	$function$;
> 104	
> 105	-- ── 3. masked public view (live verbatim + firecrawl masked, appended at END) ────────────────────
> 106	CREATE OR REPLACE VIEW public.user_api_keys AS
> 107	SELECT
> 108	  user_id, created_at, updated_at, pref_audio_provider, pref_image_provider, pref_video_provider,
> 109	  wp_site_url, wp_username, pref_ai_model,
> 110	  CASE WHEN groq_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS groq_api_key,
> 111	  CASE WHEN openrouter_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS openrouter_api_key,
> 112	  CASE WHEN openai_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS openai_api_key,
> 113	  CASE WHEN elevenlabs_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS elevenlabs_api_key,
> 114	  CASE WHEN google_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS google_api_key,
> 115	  CASE WHEN nanobana_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS nanobana_api_key,
> 116	  CASE WHEN seedance_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS seedance_api_key,
> 117	  CASE WHEN wp_app_password IS NOT NULL THEN '••••••••••••' ELSE NULL END AS wp_app_password,
> 118	  CASE WHEN replicate_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS replicate_api_key,
> 119	  CASE WHEN higgsfield_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS higgsfield_api_key,
> 120	  CASE WHEN higgsfield_api_key_secret IS NOT NULL THEN '••••••••••••' ELSE NULL END AS higgsfield_api_key_secret,
> 121	  CASE WHEN apify_token IS NOT NULL THEN '••••••••••••' ELSE NULL END AS apify_token,
> 122	  CASE WHEN resend_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS resend_api_key,
> 123	  CASE WHEN firecrawl_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS firecrawl_api_key
> 124	FROM public.user_api_keys_table
> 125	WHERE (auth.uid() = user_id OR auth.role() = 'service_role');
> 126	GRANT SELECT, INSERT, UPDATE, DELETE ON public.user_api_keys TO anon, authenticated;
> 127	
> 128	-- ── 4. INSTEAD OF trigger (live verbatim + firecrawl in guard-preserving UPDATE-first/INSERT) ────
> 129	CREATE OR REPLACE FUNCTION public.trg_instead_of_user_api_keys()
> 130	 RETURNS trigger
> 131	 LANGUAGE plpgsql
> 132	 SECURITY DEFINER
> 133	 SET search_path TO ''
> 134	AS $function$
> 135	BEGIN
> 136	  IF TG_OP = 'DELETE' THEN
> 137	    DELETE FROM public.user_api_keys_table WHERE user_id = OLD.user_id;
> 138	    RETURN OLD;
> 139	  ELSIF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
> 140	    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN
> 141	      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';
> 142	    END IF;
> 143	    UPDATE public.user_api_keys_table SET
> 144	      groq_api_key              = COALESCE(NULLIF(NEW.groq_api_key, '••••••••••••'), public.user_api_keys_table.groq_api_key),
> 145	      openrouter_api_key        = COALESCE(NULLIF(NEW.openrouter_api_key, '••••••••••••'), public.user_api_keys_table.openrouter_api_key),
> 146	      openai_api_key            = COALESCE(NULLIF(NEW.openai_api_key, '••••••••••••'), public.user_api_keys_table.openai_api_key),
> 147	      pref_audio_provider       = COALESCE(NEW.pref_audio_provider, public.user_api_keys_table.pref_audio_provider),
> 148	      pref_image_provider       = COALESCE(NEW.pref_image_provider, public.user_api_keys_table.pref_image_provider),
> 149	      pref_video_provider       = COALESCE(NEW.pref_video_provider, public.user_api_keys_table.pref_video_provider),
> 150	      elevenlabs_api_key        = COALESCE(NULLIF(NEW.elevenlabs_api_key, '••••••••••••'), public.user_api_keys_table.elevenlabs_api_key),
> 151	      google_api_key            = COALESCE(NULLIF(NEW.google_api_key, '••••••••••••'), public.user_api_keys_table.google_api_key),
> 152	      nanobana_api_key          = COALESCE(NULLIF(NEW.nanobana_api_key, '••••••••••••'), public.user_api_keys_table.nanobana_api_key),
> 153	      seedance_api_key          = COALESCE(NULLIF(NEW.seedance_api_key, '••••••••••••'), public.user_api_keys_table.seedance_api_key),
> 154	      wp_site_url               = COALESCE(NEW.wp_site_url, public.user_api_keys_table.wp_site_url),
> 155	      wp_username               = COALESCE(NEW.wp_username, public.user_api_keys_table.wp_username),
> 156	      wp_app_password           = COALESCE(NULLIF(NEW.wp_app_password, '••••••••••••'), public.user_api_keys_table.wp_app_password),
> 157	      pref_ai_model             = COALESCE(NEW.pref_ai_model, public.user_api_keys_table.pref_ai_model),
> 158	      replicate_api_key         = COALESCE(NULLIF(NEW.replicate_api_key, '••••••••••••'), public.user_api_keys_table.replicate_api_key),
> 159	      higgsfield_api_key        = COALESCE(NULLIF(NEW.higgsfield_api_key, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key),
> 160	      higgsfield_api_key_secret = COALESCE(NULLIF(NEW.higgsfield_api_key_secret, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key_secret),
> 161	      apify_token               = COALESCE(NULLIF(NEW.apify_token, '••••••••••••'), public.user_api_keys_table.apify_token),
> 162	      resend_api_key            = COALESCE(NULLIF(NEW.resend_api_key, '••••••••••••'), public.user_api_keys_table.resend_api_key),
> 163	      firecrawl_api_key         = COALESCE(NULLIF(NEW.firecrawl_api_key, '••••••••••••'), public.user_api_keys_table.firecrawl_api_key),
> 164	      updated_at                = now()
> 165	    WHERE user_id = NEW.user_id;
> 166	    IF NOT FOUND THEN
> 167	      INSERT INTO public.user_api_keys_table (
> 168	        user_id, groq_api_key, openrouter_api_key, openai_api_key, pref_audio_provider, pref_image_provider, pref_video_provider, elevenlabs_api_key, google_api_key, nanobana_api_key, seedance_api_key, wp_site_url, wp_username, wp_app_password, pref_ai_model, replicate_api_key, higgsfield_api_key, higgsfield_api_key_secret, apify_token, resend_api_key, firecrawl_api_key
> 169	      ) VALUES (
> 170	        NEW.user_id, NEW.groq_api_key, NEW.openrouter_api_key, NEW.openai_api_key, NEW.pref_audio_provider, NEW.pref_image_provider, NEW.pref_video_provider, NEW.elevenlabs_api_key, NEW.google_api_key, NEW.nanobana_api_key, NEW.seedance_api_key, NEW.wp_site_url, NEW.wp_username, NEW.wp_app_password, NEW.pref_ai_model, NEW.replicate_api_key, NEW.higgsfield_api_key, NEW.higgsfield_api_key_secret, NEW.apify_token, NEW.resend_api_key, NEW.firecrawl_api_key
> 171	      );
> 172	    END IF;
> 173	    RETURN NEW;
> 174	  END IF;
> 175	  RETURN NULL;
> 176	END;
> 177	$function$;
> 178	
> 179	-- ── 5. decrypted view (service_role only; live verbatim + firecrawl COALESCE + join, appended at END) ─
> 180	CREATE OR REPLACE VIEW public.decrypted_user_api_keys AS
> 181	SELECT
> 182	  uak.user_id,
> 183	  COALESCE(s_groq.decrypted_secret, uak.groq_api_key) AS groq_api_key,
> 184	  COALESCE(s_openrouter.decrypted_secret, uak.openrouter_api_key) AS openrouter_api_key,
> 185	  COALESCE(s_openai.decrypted_secret, uak.openai_api_key) AS openai_api_key,
> 186	  uak.created_at, uak.updated_at, uak.pref_audio_provider, uak.pref_image_provider, uak.pref_video_provider,
> 187	  COALESCE(s_elevenlabs.decrypted_secret, uak.elevenlabs_api_key) AS elevenlabs_api_key,
> 188	  COALESCE(s_google.decrypted_secret, uak.google_api_key) AS google_api_key,
> 189	  COALESCE(s_nanobana.decrypted_secret, uak.nanobana_api_key) AS nanobana_api_key,
> 190	  COALESCE(s_seedance.decrypted_secret, uak.seedance_api_key) AS seedance_api_key,
> 191	  uak.wp_site_url, uak.wp_username,
> 192	  COALESCE(s_wp_pwd.decrypted_secret, uak.wp_app_password) AS wp_app_password,
> 193	  uak.pref_ai_model,
> 194	  COALESCE(s_replicate.decrypted_secret, uak.replicate_api_key) AS replicate_api_key,
> 195	  COALESCE(s_higgsfield.decrypted_secret, uak.higgsfield_api_key) AS higgsfield_api_key,
> 196	  COALESCE(s_higgsfield_sec.decrypted_secret, uak.higgsfield_api_key_secret) AS higgsfield_api_key_secret,
> 197	  COALESCE(s_apify.decrypted_secret, uak.apify_token) AS apify_token,
> 198	  COALESCE(s_resend.decrypted_secret, uak.resend_api_key) AS resend_api_key,
> 199	  COALESCE(s_firecrawl.decrypted_secret, uak.firecrawl_api_key) AS firecrawl_api_key
> 200	FROM public.user_api_keys_table uak
> 201	LEFT JOIN vault.decrypted_secrets s_groq ON uak.groq_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_groq.id = uak.groq_api_key::uuid
> 202	LEFT JOIN vault.decrypted_secrets s_openrouter ON uak.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_openrouter.id = uak.openrouter_api_key::uuid
> 203	LEFT JOIN vault.decrypted_secrets s_openai ON uak.openai_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_openai.id = uak.openai_api_key::uuid
> 204	LEFT JOIN vault.decrypted_secrets s_elevenlabs ON uak.elevenlabs_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_elevenlabs.id = uak.elevenlabs_api_key::uuid
> 205	LEFT JOIN vault.decrypted_secrets s_google ON uak.google_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_google.id = uak.google_api_key::uuid
> 206	LEFT JOIN vault.decrypted_secrets s_nanobana ON uak.nanobana_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_nanobana.id = uak.nanobana_api_key::uuid
> 207	LEFT JOIN vault.decrypted_secrets s_seedance ON uak.seedance_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_seedance.id = uak.seedance_api_key::uuid
> 208	LEFT JOIN vault.decrypted_secrets s_wp_pwd ON uak.wp_app_password ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_wp_pwd.id = uak.wp_app_password::uuid
> 209	LEFT JOIN vault.decrypted_secrets s_replicate ON uak.replicate_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_replicate.id = uak.replicate_api_key::uuid
> 210	LEFT JOIN vault.decrypted_secrets s_higgsfield ON uak.higgsfield_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_higgsfield.id = uak.higgsfield_api_key::uuid
> 211	LEFT JOIN vault.decrypted_secrets s_higgsfield_sec ON uak.higgsfield_api_key_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_higgsfield_sec.id = uak.higgsfield_api_key_secret::uuid
> 212	LEFT JOIN vault.decrypted_secrets s_apify ON uak.apify_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_apify.id = uak.apify_token::uuid
> 213	LEFT JOIN vault.decrypted_secrets s_resend ON uak.resend_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_resend.id = uak.resend_api_key::uuid
> 214	LEFT JOIN vault.decrypted_secrets s_firecrawl ON uak.firecrawl_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_firecrawl.id = uak.firecrawl_api_key::uuid;
> 215	REVOKE ALL ON public.decrypted_user_api_keys FROM PUBLIC, anon, authenticated;
> 216	GRANT SELECT ON public.decrypted_user_api_keys TO service_role;
> 217	
> ```

## 🤖 Claude *(02:03:26)*

Both files read in full. Let me verify the firecrawl template's GRANT/REVOKE/tenant-guard lines against the new rapidapi migration — they are line-for-line identical except for the added `rapidapi_key` references. Let me now do a focused analysis.

## Analysis

### New migration `20260622210000_user_api_keys_rapidapi_channel.sql`

Compared section-by-section against the already-reviewed firecrawl template `20260615140000`:

| Security control | Template | New migration | Match? |
|---|---|---|---|
| Encrypt trigger uses `vault_upsert_secret` + UUID-passthrough guard | L96-100 | L96-100 (`rapidapi_key`) | Identical pattern |
| `SECURITY DEFINER SET search_path TO ''` on both functions | yes | yes (L19-20, L133-134) | Identical |
| Masked view shows `'••••••••••••'` | L123 | L124 (`rapidapi_key`) | Identical |
| Masked view `WHERE (auth.uid() = user_id OR auth.role() = 'service_role')` | L125 | L126 | Identical |
| INSTEAD OF tenant guard `auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid()` → 42501 | L140-142 | L141-143 | Identical |
| INSTEAD OF UPDATE-first, COALESCE/NULLIF masked-sentinel preservation | L163 | L165 (`rapidapi_key`) | Identical |
| Decrypted view `REVOKE ALL ... FROM PUBLIC, anon, authenticated` | L215 | L219 | Identical |
| Decrypted view `GRANT SELECT ... TO service_role` only | L216 | L220 | Identical |
| Decrypted-view UUID-anchored vault JOIN (`s_rapidapi.id = uak.rapidapi_key::uuid`) | L214 | L218 | Identical |

The new column is wired identically to every other encrypted column. No GRANT/REVOKE dropped. The `CREATE OR REPLACE VIEW` reissues `GRANT SELECT,INSERT,UPDATE,DELETE ... TO anon,authenticated` on the masked view and `REVOKE ALL ... / GRANT SELECT TO service_role` on the decrypted view — so replacing the view does not lose any grant/revoke. No deviation that opens cross-tenant read/write, secret exposure, or privesc.

### Edge function changes

- All 25 per-user resolutions read `decrypted_user_api_keys ... .eq("user_id", user.id|userId).maybeSingle()` — scoped to the authenticated principal. `user.id` is the JWT-verified caller; `userId` in service-role-invoked fns (`generate-image`, `orchestrate-content`) is the row-owner the function already trusts. Removing `|| Deno.env.get(...)` only *narrows* access (drops a shared global key). No new cross-tenant path introduced.
- `canvas-execute`: higgsfield now reads `userKeys?.higgsfield_api_key`/`_secret` per-user instead of global env — strictly tighter.
- `openrouter-swarm`: adds a properly scoped `decrypted_user_api_keys.select("openrouter_api_key").eq("user_id", user.id)` lookup; `user` is from the 401-gated auth check above. Correct.
- `aios-chat-gateway`: removes a **hardcoded literal bearer token** (`"3bdfc718fb880d4d585c540339ba6d3c2a72d7510b2479d7"`) and replaces it with env-only + fail-closed 501. This *removes* a committed secret — a security improvement, not a regression.
- `embed-mcorch-node` / `search-constellation`: env key var renamed (`OPENROUTER_API_KEY`→`MESH_EMBED_OPENROUTER_KEY`, etc.). These are system/pg_net flows with no user in scope; env is trusted; no authz change.

No edge change introduces reading another user's key, an authz bypass, or secret exposure. (The literal token that *was* in source control is now removed; it lives in git history but that is pre-existing and out of this PR's introduced-vulnerability scope — and rotation of that token is an ops action, not a code finding.)

## Verdict

**No high-confidence, newly-introduced, concretely-exploitable security vulnerabilities found.**

The new `rapidapi_key` migration is a verbatim, control-preserving mirror of the already-reviewed firecrawl template — encrypt trigger (idempotent `vault_upsert_secret`), masked view (`••••` + `auth.uid()=user_id OR service_role`), INSTEAD OF tenant guard (`42501` on cross-tenant write), and decrypted view (`REVOKE ALL FROM PUBLIC/anon/authenticated`, `GRANT SELECT TO service_role` only) are all identical, with `search_path TO ''` and `SECURITY DEFINER` preserved on both functions. No GRANT/REVOKE/RLS was dropped by the `CREATE OR REPLACE`.

The 25 edge-function edits only *remove* a shared global key fallback (or, for `aios-chat-gateway`, a hardcoded literal token) and resolve credentials per-authenticated-user via `decrypted_user_api_keys.eq("user_id", <verified caller>)`. Every change tightens tenancy; none opens a cross-tenant read, authz bypass, privilege escalation, or new secret exposure.

Relevant files:
- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260622210000_user_api_keys_rapidapi_channel.sql`
- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260615140000_user_api_keys_firecrawl_channel.sql` (template compared against)

One non-blocking, pre-existing note (explicitly out of the introduced-vuln scope you asked for, so not counted as a finding): the literal OpenClaw gateway token previously hardcoded in `aios-chat-gateway/index.ts` remains in git history — it should be rotated as an ops follow-up since the PR correctly removes it from the working tree.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-23 - agent-ad712f9ef0400f04b]]
%% --- TIMELINE END --- %%

# SOP — Credenciais Globais de Aplicativo (Admin Tier) + Rotação

> **Status:** ATIVA v1.0 · 2026-07-16 · Lei 2 (Processo Antecipado) — escrita ANTES do código.
> **BoK SSOT:** `docs/bok/post-engine/16-amendment-global-app-credentials-admin-tier.md` (FR-PE-017..021).
> **Escopo:** credenciais de APP OAuth (client_id + client_secret) das 6 plataformas sociais, gerenciadas pelo admin em `/dashboard/admin` → tab "Chaves", gravadas como linhas `user_id IS NULL` de `social_app_config` (Vault-cifradas). Inclui o ciclo de rotação com lembretes persistentes.

---

## Operator

| Papel | Quem | Ferramenta |
|---|---|---|
| Admin (tier global) | Sovereign (Gabriel) | `/dashboard/admin` → tab **Chaves** |
| Tenant (BYOK per-user) | qualquer usuário | `/dashboard/settings` → tab Social (inalterado) |
| Runtime | edge fns `social-auth-init` / `social-auth-callback` / `refresh-social-token` / `tiktok-login-*` | `resolveSocialAppCreds` (per-user → global → env → 402) |

## Sequence (fluxo manual completo)

1. **Console da plataforma** — criar/abrir o app no developer console (Pinterest: developers.pinterest.com; Google: console.cloud.google.com; TikTok: developers.tiktok.com; etc.). Critério: App ID + App Secret visíveis.
2. **Registrar o redirect URI** no console — valor EXATO (sem wildcard):
   `https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/social-auth-callback`
   Critério: URI listado no console. (Pinterest exige match exato; TikTok/Google idem.)
3. **Colar as credenciais** em `/dashboard/admin` → tab **Chaves** → seção da plataforma → App ID no campo `client_id`, Secret no campo write-only → **Salvar**. Critério: toast de sucesso + badge **"Configurado"**.
4. **Verificar materialmente (Lei 1)** — linha global existe e o secret virou referência Vault (nunca plaintext):
   ```sql
   SELECT platform, user_id, is_active,
          client_secret ~ '^[0-9a-f-]{36}$' AS secret_is_vault_uuid
   FROM social_app_config_table WHERE user_id IS NULL;
   ```
   Critério: `user_id NULL · is_active t · secret_is_vault_uuid t`.
5. **Conectar como usuário** — `/dashboard/social` → card da plataforma → Conectar → consent → volta conectado. Critério: linha em `social_accounts` com `is_active=true` + scopes concedidos.
6. **Rotação (ciclo recorrente)** — no console: *Redefinir segredo* → colar o secret novo na mesma seção da tab Chaves (client_id intocado; UPDATE in-place re-cifra no Vault) → no banner de lembretes, **"Marcar como resolvido"** no item correspondente. Critério: `resolved_at` preenchido + conexões novas funcionando com o secret novo.

## Verification gates

| Gate | Prova material |
|---|---|
| **G1** Linha global cifrada | Query do passo 4 — `secret_is_vault_uuid = t` |
| **G2** Resolver usa o tier global | Tenant SEM linha per-user conecta com sucesso; log do resolver `source="global"` |
| **G3** Isolamento (FMEA-011) | User não-admin: SELECT na view → 0 linhas globais; INSERT/UPDATE com `user_id NULL` → erro 42501 |
| **G4** Mask round-trip | Re-salvar só o client_id (secret vazio) NÃO destrói o secret armazenado; view segue mascarando `••••••••••••` |
| **G5** Env nunca primário | `grep` nos edge fns: zero leitura crua de `LINKEDIN_/INSTAGRAM_/TWITTER_CLIENT` fora do `ENV_MAP` do resolver |
| **G6** Lembrete persiste | `admin_reminders` não-resolvido sobrevive a reload/nova sessão; some do banner só com `resolved_at` |

## Recovery path

- **⚠️ ANTICORPO (witnessed 2026-07-16): "Authentication failed." no callback com credencial global VÁLIDA** → uma **linha per-user antiga** (degrau 1) está sombreando a global (degrau 2). Caso real: o Sovereign redefiniu o secret no console Pinterest → o secret da linha per-user de 28/jun morreu → o init montou o consent (client_id igual, parece ok) mas o token exchange usou o secret VELHO per-user → 401 `{"code":2,"message":"Authentication failed."}` do próprio Pinterest. **Diagnóstico discriminante (zero-custo):** sondar o token exchange com `code` falso usando cada credencial — `invalid_client`/`Authentication failed` = secret errado; `invalid grant (283)` = credencial válida. **Fix:** `UPDATE social_app_config_table SET is_active=false WHERE platform='<p>' AND user_id IS NOT NULL` (service-role) → resolver cai na global. Regra: ao promover uma plataforma para o tier global, DESATIVAR (ou atualizar) as linhas per-user do mesmo app.
- **Seed do que já existe**: edge fn `seed-global-app-creds` (service-role-only, idempotente — nunca sobrescreve linha global existente) materializa credenciais do env-vault como linhas globais; per-user→global promotion via script service-role (o decrypted view fornece o plaintext ao service_role; o trigger Vault re-cifra no insert).
- **Secret colado errado** → recolar o correto na mesma seção (UPDATE in-place; `vault_upsert_secret` re-cifra por nome — sem 23505).
- **Falha no OAuth pós-troca** (401/invalid_client) → conferir no console se o secret foi *redefinido* (o antigo morre na hora em algumas plataformas); recolar o vigente.
- **Linha global órfã/indevida** → deletar pela UI admin (DELETE via view; visibilidade RLS garante que só admin alcança) e recriar.
- **Rollback da migration** → restaurar `NOT NULL` exige antes remover as linhas globais; policies/índice parcial têm `DROP ... IF EXISTS` determinístico.
- **429/rate-limit da plataforma** com credencial global compartilhada → tenant afetado migra para BYOK per-user (degrau 1 já resolve na frente do global).

## Success signal

Connect Pinterest E2E do Usuário Zero **usando a credencial global colada pela UI admin** (zero `.env`, zero CLI): linha `social_accounts` `platform='pinterest' · is_active=true` + badge conectado em `/dashboard/social` + nó observation na malha.

## Known debt

- **OTD-PE-GLOBAL-OTHER-SECRETS** — segredos globais não-OAuth (Telegram bot, chaves de sistema `MESH_EMBED_*`) seguem em env; cobertos operacionalmente pelo lembrete de rotação, migração de leitura é fatia futura.
- Webhooks Meta (verify token / HMAC) são system-level por definição — permanecem env (não é violação do Tenancy Model).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

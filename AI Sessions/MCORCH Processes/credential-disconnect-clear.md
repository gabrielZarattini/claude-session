# SOP — Clearing / revoking per-user credentials stored behind masked Vault views

**Status:** active · **Owner (ROI/risk):** Sovereign · **Created:** 2026-06-02
**Applies to:** `user_api_keys` (WordPress + AI keys), and by analogy `meta_config`, `social_accounts` — all masked SECURITY-DEFINER views over `*_table` with Vault-encrypted secret columns (migrations `20260601000000_credential_encryption.sql`, `20260601000600_secure_definer_views.sql`).

## Problem this SOP anticipates (the trap)

After credential-encryption, a credential column on the masked view cannot be cleared by a
client writing `NULL`. The view's INSTEAD OF trigger writes secret columns through
`COALESCE(NULLIF(NEW.x, '••••••••••••'), base.x)` — a **load-bearing guard** that lets a partial
save touch only some fields without wiping the others. Its side effect: **`NULL` preserves the old
value**, so a disconnect that nulls columns from the client silently leaves the secret (and its
plaintext in the Vault) in place. Worse, SELECT on the base table is REVOKED from `authenticated`,
so the client has no privileged path to a true clear.

A true clear/revoke therefore MUST run server-side with elevated privileges.

## Operator

Today: an **authenticated end-user** clicking "Desconectar" on `/dashboard/settings`
(SocialAccounts page) for WordPress. The privileged work is delegated to the
`disconnect_wordpress()` RPC (SECURITY DEFINER, owner `postgres`), scoped to `auth.uid()`.

Manual equivalent (Sovereign / support, e.g. an LGPD erasure request): run the same clear via the
Supabase SQL editor or Management API as a privileged role (see Recovery).

## Sequence (per disconnect)

1. Client calls `supabase.rpc('disconnect_wordpress')` — no parameters (identity comes from the JWT).
   - **Success criterion:** RPC returns `{ error: null }`.
2. RPC reads the caller's `wp_app_password` reference from `user_api_keys_table WHERE user_id = auth.uid()`.
3. RPC nulls `wp_site_url`, `wp_username`, `wp_app_password` on the base table (privileged — bypasses the masked view's COALESCE-NULLIF guard).
4. RPC deletes the Vault secret, scoped to BOTH `id = <ref>` AND `name = 'user_api_keys_wp_app_password_' || auth.uid()` (the name binding makes it provably impossible to delete another tenant's secret, even though `wp_app_password` is client-writable).

## Verification gates (material — Law 1)

Query the decrypted view for the affected user (service_role / Management API):
```sql
SELECT wp_site_url, wp_username, wp_app_password
FROM public.decrypted_user_api_keys WHERE user_id = '<uid>';
-- PASS: all three NULL
SELECT count(*) FROM vault.secrets WHERE name = 'user_api_keys_wp_app_password_<uid>';
-- PASS: 0
```
UI gate: the WordPress card shows the "Desconectado" badge; the AI keys (groq/openrouter/…) for the
same user are UNCHANGED (the clear must be surgical — never wipe sibling credentials).

## Recovery path (failure in any step)

- **RPC errors `authentication required` (28000):** the caller had no `sub` claim — re-authenticate; do not retry as anon.
- **RPC succeeds but verification shows a lingering secret:** the secret name diverged from the
  deterministic pattern (legacy/backfill). Clear manually as a privileged role:
  ```sql
  UPDATE public.user_api_keys_table
    SET wp_site_url = NULL, wp_username = NULL, wp_app_password = NULL, updated_at = now()
  WHERE user_id = '<uid>';
  DELETE FROM vault.secrets WHERE name LIKE 'user_api_keys_wp_app_password_<uid>%';
  ```
- **Reconnect fails with `unique_violation` on `vault.secrets.name`:** a stale secret with the
  deterministic name survived a prior clear. Delete it (query above), then reconnect.

## Success signal

Decrypted view shows all three WP columns NULL, zero matching `vault.secrets` rows, sibling AI keys
intact, and a fresh connect (save) succeeds and re-creates exactly one Vault secret.

## Saving / connecting (companion fix)

`user_api_keys` is a VIEW with no unique constraint → PostgREST `.upsert()`/`onConflict` returns
**HTTP 400 (42P10)**. Writes MUST use `.insert()`, which routes through the INSTEAD OF INSERT trigger
that does `INSERT ... ON CONFLICT (user_id) DO UPDATE` internally (upserts). Canonical reference:
`src/hooks/useUserApiKeys.ts`. The same applies to `meta_config`/`social_accounts`, except those
INSTEAD OF INSERT triggers have **no** ON CONFLICT, so their hooks use `.update()`-if-exists /
`.insert()`-if-not (`useMetaConfig`, `useAffiliateConfig`).

## Resolved latent debt — idempotent encryption (closed 2026-06-02)

**Was:** the encryption triggers (`trg_encrypt_user_api_keys` + its `meta_config`/`social_accounts`
siblings) called `vault.create_secret(value, '<deterministic-name>')` **unconditionally** on a secret
change. `vault.create_secret` does a plain INSERT with **no ON CONFLICT** and `vault.secrets.name` is
UNIQUE (`secrets_name_idx`) → **rotating a credential in place (new value, same name) threw
`unique_violation` (23505)**. User-facing: WordPress "Editar → save a new password without
disconnecting first". (connect → disconnect → reconnect always worked because `disconnect_wordpress()`
deletes the secret first; only the rotate-in-place path was broken.)

**Fix:** migration `20260602140000_vault_upsert_secret_idempotent_encrypt.sql` introduces
`public.vault_upsert_secret(value, name, desc)` — SECURITY DEFINER, `search_path=''`, EXECUTE revoked
from PUBLIC/anon/authenticated (internal primitive, never a PostgREST RPC) — which resolves an
existing secret by name and rotates it in place via `vault.update_secret` (COALESCE-keeps
name+description, re-encrypts only the value), else creates it; a `unique_violation` handler absorbs
the create race. All three encryption triggers now call this helper instead of `vault.create_secret`
and were pinned to `search_path=''`. The stored column keeps the SAME Vault UUID across rotations, so
`decrypted_*` views reflect the new value and no orphan secrets accumulate.

**Material proof (2026-06-02, Management API, every test rolled back — no production mutation):**
- BEFORE: `user_api_keys` double-save of `wp_app_password` → `ERROR 23505 ... secrets_name_idx ...
  Key (name)=(user_api_keys_wp_app_password_<uid>) already exists` raised inside
  `trg_encrypt_user_api_keys`.
- AFTER (`user_api_keys`): same double-save → `{decrypted_wp:"wp-pass-BRAVO", secret_count:1,
  col_is_uuid_ref:true, sibling_groq_intact:true}`, no error.
- AFTER (`social_accounts`, real row `39ce0ebb-3579-481a-93ce-8a20759cd22e`): double-rotation of
  `access_token` → `{decrypted_access:"sa-BRAVO", secret_count:1}`, no error.
- (`meta_config` has 0 rows to exercise live; covered by the shared helper + source verification —
  all three triggers verified `calls_helper=true, calls_create_secret=false`.)

**Residual nuance (not a defect):** the helper opens a per-call subtransaction (its `EXCEPTION` block)
only to absorb the rare concurrent-create race; the common rotate path takes the no-exception
SELECT→`update_secret` branch.

## Tenant isolation on the masked-view INSTEAD OF triggers (hardened 2026-06-02)

Surfaced during the `/security-review` of `20260602140000`: the `meta_config` / `social_accounts`
INSTEAD OF triggers lacked the `auth.uid()` tenant guard that `user_api_keys` got in `20260602130000`.
Because those triggers are SECURITY DEFINER (bypass base-table RLS) and PostgreSQL does not apply a
view's WHERE qualification to INSERT, an authenticated caller could `POST` a row with a **spoofed
`user_id`** (a victim's) + a **fresh `id`** → a credential row owned by the victim with attacker
tokens (the *overwrite* variant — colliding `id` — was already fail-closed by `PRIMARY KEY(id)`).
Migration `20260602150000_meta_social_instead_of_tenant_guard.sql` ports the same guard
(`auth.role() <> 'service_role' AND NEW.user_id <> auth.uid()` → `42501`) to the INSERT and UPDATE
branches of both, pins `search_path=''`, and reproduces the live bodies verbatim (column maps,
COALESCE defaults, masked sentinels). **Material proof (2026-06-02, rolled back):** BEFORE — attacker
`sub=1111…` injected a `meta_config` for victim `ada39fae…` → `{rows_owned_by_victim:1,
decrypted_token:"INJECTED-BY-ATTACKER"}`. AFTER — same → `42501` on both tables; legit self-insert
(`user_id=auth.uid()`) → `{inserted:1, decrypted:"my-own-token"}`; service_role with arbitrary
`user_id` → `{inserted:1}` (exempt). Every legit writer is service_role (edge OAuth/cron) or a client
writing its own row, so the guard breaks nothing.

## Meta / social disconnect — orphaned-secret revocation (closed 2026-06-02)

**Was:** disconnecting a Meta connection (`useMetaConfig.disconnect`) or a social account
(`useSocialAccounts.disconnectAccount`) issued a plain `.delete()` through the masked view → the
INSTEAD OF DELETE trigger only ran `DELETE FROM <base>_table WHERE id = OLD.id`. The encrypted token
columns hold Vault secret references, so the base-row delete left the underlying Vault secret
**orphaned** (retained plaintext, no owning row) — the same LGPD/retention gap `disconnect_wordpress()`
closed for WordPress, but for `meta_config` (`long_lived_token`, `pages`) and `social_accounts`
(`access_token`, `refresh_token`). **Materially observed on prod:** the sole tenant had 0 rows in
`meta_config_table` yet **12 orphaned Meta Vault secrets** (6× `meta_config_long_lived_token_*` + 6×
`meta_config_pages_*`) — residue of ~6 connect/disconnect cycles.

**Fix:** migration `20260602160000_meta_social_disconnect_rpc.sql` adds two privileged RPCs mirroring
`disconnect_wordpress()` (SECURITY DEFINER, `search_path=''`, fail-closed on NULL `auth.uid()` →
`28000`, EXECUTE granted to `authenticated` only):
- `disconnect_meta()` — no params (`UNIQUE(user_id)` ⇒ one row). Deletes the caller's row and revokes
  `meta_config_long_lived_token_<id>` + `meta_config_pages_<id>`.
- `disconnect_social(p_account_id uuid)` — deletes the caller's row with that id and revokes
  `social_accounts_access_token_<id>` + `social_accounts_refresh_token_<id>`. A foreign / non-existent
  id is a silent no-op (`SELECT … WHERE id = p_account_id AND user_id = auth.uid()` yields no row).

**Tenant safety (key difference vs WordPress):** meta/social secret names are keyed by the **row id**,
not the `user_id`. Each Vault `DELETE` is double-bound — `id = <ref read from the caller's OWN row>`
**AND** `name = '<prefix>_' || <caller's own row id>`. Because `id` is `PRIMARY KEY` on both base
tables, the caller's own row id can never equal a victim's, so the name clause can never match a
victim's secret name — a planted foreign reference UUID can only ever no-op. (And the raw Vault UUID
is never exposed to clients: token columns are masked, base-table SELECT is REVOKED from
`authenticated`, `decrypted_*` is service_role-only — so the ref cannot even be learned.) The hooks
were switched from `.delete()` to `supabase.rpc('disconnect_meta')` / `rpc('disconnect_social',
{ p_account_id })`. The migration also one-time revokes the already-orphaned secrets, provably
orphan-scoped (`NOT EXISTS` a base row whose `id::text = right(name,36)` → live connections preserved).

**Material proof (2026-06-02, Management API):**
- RPC suite (BEGIN/ROLLBACK, against the tenant's real rows): `disconnect_social` happy path → row
  deleted **and** `social_accounts_access_token_<id>` revoked; foreign-id call by a different uid →
  no-op (victim row+secret intact); planted-ref attack (instagram secret UUID planted in facebook's
  row) → instagram secret SURVIVED (name binding held); `disconnect_meta` happy path → row deleted and
  **both** token+pages secrets revoked; unauthenticated call → `28000`. 5/5 PASS, zero residue.
- Apply (committed): functions live (`SECURITY DEFINER`, `proconfig=search_path=""`), EXECUTE granted
  to `authenticated` / revoked from `anon`, the **12 orphaned Meta secrets revoked → 0** (`meta_config_%`
  count now 0), **3 live social secrets + 3 social rows intact**, migration recorded in
  `schema_migrations`. `tsc` 0 errors · 238 tests pass · served bundle contains both RPC calls.

### Manual / LGPD-erasure equivalent
```sql
-- as a privileged role (service_role / Management API), for a given <uid>:
SELECT public.disconnect_meta();                 -- if run within the user's JWT context, OR:
DELETE FROM public.meta_config_table   WHERE user_id = '<uid>';
DELETE FROM public.social_accounts_table WHERE user_id = '<uid>';
DELETE FROM vault.secrets s
WHERE s.name ~ '^(meta_config_(long_lived_token|pages)|social_accounts_(access_token|refresh_token))_[0-9a-f-]{36}$'
  AND NOT EXISTS (SELECT 1 FROM public.meta_config_table m   WHERE m.id::text  = right(s.name,36))
  AND NOT EXISTS (SELECT 1 FROM public.social_accounts_table sa WHERE sa.id::text = right(s.name,36));
```

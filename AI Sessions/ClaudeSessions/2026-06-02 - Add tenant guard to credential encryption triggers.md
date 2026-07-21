---
type: session-stub
archived: true
original_size_bytes: 378730
original_size: 370 KB
date: 2026-06-02
session_id: 85c240d0-59c3-4bae-b829-c36ef83a7a9f
full_path: _full-sessions/ClaudeSessions/2026-06-02 - Add tenant guard to credential encryption triggers.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-02%20-%20Add%20tenant%20guard%20to%20credential%20encryption%20triggers.md
---

# Add tenant guard to credential encryption triggers

> [!abstract] Sessao arquivada
> O conteudo completo (**370 KB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-02%20-%20Add%20tenant%20guard%20to%20credential%20encryption%20triggers.md)**

- **Data:** 2026-06-02
- **Session ID:** `85c240d0-59c3-4bae-b829-c36ef83a7a9f`
- **Tamanho original:** 370 KB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-06-02 - Add tenant guard to credential encryption triggers.md`

## Roteiro da sessao

- Pre-existing multi-tenant gap surfaced during the /security-review of migration `20260602140000_vault_upsert_s
- faça os dois /security-review apontado para o commit 87c926f como redundância de cinto-e-suspensório, e também
- You are a senior security engineer conducting a focused security review of the changes on this branch.

## Previa

> # Add tenant guard to credential encryption triggers
> **Date:** 2026-06-02 | **Session ID:** `85c240d0-59c3-4bae-b829-c36ef83a7a9f`
> 
> ---
> 
> ## 👤 User *(15:38:53)*
> 
> Pre-existing multi-tenant gap surfaced during the /security-review of migration `20260602140000_vault_upsert_secret_idempotent_encrypt.sql` (credential-encryption layer). NOT a regression from that migration — it predates it — but it should be closed with its own focused migration + /security-review.
> 
> ## The gap
> The masked-view INSTEAD OF INSERT triggers for `meta_config` and `social_accounts` lack the `auth.uid()` tenant guard that `user_api_keys` received in `supabase/migrations/20260602130000_fix_user_api_keys_instead_of_double_fire.sql`. Confirmed materially 2026-06-02: `position('auth.uid' in pg_get_functiondef('public.trg_instead_of_meta_config()'::regprocedure)) = 0` and same for `trg_instead_of_social_accounts()`.
> 
> Because those INSTEAD OF triggers are SECURITY DEFINER (owner postgres, bypass base-table RLS) and PostgreSQL does not apply a view's WHERE qualification to INSERT, an authenticated attacker can `POST /rest/v1/social_accounts` (or `/rest/v1/meta_config`) with a **spoofed `user_id` = victim** and a **fresh `id`** (no PK collision) → a row owned by the victim with attacker-controlled `access_token`/`long_lived_token` gets committed. A service-role publisher iterating that victim's `decrypted_social_accounts`/`decrypted_meta_config` could then use the attacker's injected credential/account (credential confusion / content redirection). meta_config has `UNIQUE(user_id)` so it's only injectable when the victim has no row yet; social_accounts is injectable on any unused `platform`.
> 
> NOTE: the cross-tenant *overwrite* variant (colliding `id`) is already fail-closed by `PRIMARY KEY (id)` on both base tables (proven materially — the base PK 23505 rolls the whole statement back, including the BEFORE-trigger Vault write). So this follow-up is specifically about the *injection* (spoofed user_id, fresh id) path.
> 
> ## Fix (established pattern from 20260602130000)
> Recreate `trg_instead_of_meta_config` (current def: `supabase/migrations/20260601000500_fix_meta_config_instead_of_trigger.sql`) and `trg_instead_of_social_accounts` (current def: `supabase/migrations/20260601000000_credential_encryption.sql` lines ~457-492), preserving ALL existing column-mapping logic verbatim, and prepend to the INSERT/UPDATE branch:
> ```sql
> IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN
>   RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';
> END IF;
> ```
> Add `SET search_path = ''` to match the hardening precedent. New migration timestamp > 20260602140000.
> 
> ## Material verification (Management API: token in ~/.supabase/access-token, project ref bcyvddsykvehvpwstlfa, POST https://api.supabase.com/v1/projects/<ref>/database/query)
> Simulate a user via `set_config('request.jwt.claims', '{"sub":"<attacker_uid>","role":"authenticated"}', false)` then attempt an INSERT into `public.social_accounts` with `user_id` = a DIFFERENT real auth.users id and a fresh `id`; prove it now raises `42501` (was: succeeded). Confirm a legitimate self-insert (user_id = auth.uid()) and a service_role insert still succeed. Wrap tests in BEGIN/ROLLBACK. Update SOP `docs/processes/credential-disconnect-clear.md`. MANDATORY /security-review (touches credential encryption layer, per CLAUDE.md). Only one real tenant exists today (`ada39fae-67e1-4e53-af1c-5a18e1c108e8`), so you may need a second throwaway auth.users row (respect the FK) or assert the guard logic against `auth.uid()` mismatch directly.
> 
> ## 🤖 Claude *(15:39:25)*
> 
> 
> ## 🤖 Claude *(15:39:29)*
> 
> Vou começar verificando materialmente o estado atual — porque tanto o `CLAUDE.md` (Key Files Reference) quanto o git log mais recente (`87c926f`, `66859b0`) quanto minha memória indicam que esse exato gap já foi selado na migration `20260602150000_meta_social_instead_of_tenant_guard.sql` (v6.20.2). Antes de criar qualquer migration nova, preciso confirmar a realidade material (Lei 1) — não posso assumir que o gap está aberto só porque o prompt o descreve assim, nem assumir que está fechado só porque a memória diz.
> 

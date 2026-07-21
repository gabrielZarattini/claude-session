---
type: session-stub
archived: true
original_size_bytes: 398431
original_size: 389 KB
date: 2026-06-02
session_id: 8ca7b6b8-2a47-4c90-a095-83d1d676489d
full_path: _full-sessions/ClaudeSessions/2026-06-02 - Fix WordPress credentials save and disconnect in SocialAccountsPage.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-02%20-%20Fix%20WordPress%20credentials%20save%20and%20disconnect%20in%20SocialAccountsPage.md
---

# Fix WordPress credentials save and disconnect in SocialAccountsPage

> [!abstract] Sessao arquivada
> O conteudo completo (**389 KB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-02%20-%20Fix%20WordPress%20credentials%20save%20and%20disconnect%20in%20SocialAccountsPage.md)**

- **Data:** 2026-06-02
- **Session ID:** `8ca7b6b8-2a47-4c90-a095-83d1d676489d`
- **Tamanho original:** 389 KB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-06-02 - Fix WordPress credentials save and disconnect in SocialAccountsPage.md`

## Roteiro da sessao

- `src/pages/SocialAccountsPage.tsx` (around lines 51 and 68) saves and disconnects WordPress credentials by cal
- You are a senior security engineer conducting a focused security review of the changes on this branch.

## Previa

> # Fix WordPress credentials save and disconnect in SocialAccountsPage
> **Date:** 2026-06-02 | **Session ID:** `8ca7b6b8-2a47-4c90-a095-83d1d676489d`
> 
> ---
> 
> ## 👤 User *(12:31:22)*
> 
> `src/pages/SocialAccountsPage.tsx` (around lines 51 and 68) saves and disconnects WordPress credentials by calling `supabase.from('user_api_keys').upsert({...}, { onConflict: 'user_id' })`. This is BROKEN by the 2026-06-01 credential-encryption migrations (`supabase/migrations/20260601000000_credential_encryption.sql` + `20260601000600_secure_definer_views.sql`), which turned `user_api_keys` from a table into a masked security-definer VIEW over `user_api_keys_table`.
> 
> Two concrete bugs:
> 1. `.upsert()` / `onConflict:'user_id'` on the VIEW → HTTP 400 `42P10 "no unique or exclusion constraint matching the ON CONFLICT"` (views have no unique constraint). The save (line ~51) therefore fails.
>    FIX: use `.insert({...})` instead — the view's INSTEAD OF INSERT trigger (`trg_instead_of_user_api_keys`) runs `INSERT ... ON CONFLICT (user_id) DO UPDATE`, i.e. it upserts internally. This exact fix was already applied to `src/hooks/useUserApiKeys.ts` (see its comment) — mirror it here.
> 2. The disconnect handler (line ~68) sets `wp_site_url/wp_username/wp_app_password = null` to CLEAR them. But the INSTEAD OF UPDATE path uses `COALESCE(NULLIF(NEW.x, '••••••••••••'), base.x)` which PRESERVES the existing value when NEW is null — so nulls do NOT clear. To truly clear WP credentials, do a direct UPDATE on the base table `user_api_keys_table` via a service-role edge function (client can't touch the base table — SELECT was REVOKED from authenticated), OR add explicit null-clear handling to the trigger.
> 
> Verify the fix end-to-end: in the Settings/SocialAccounts UI, connecting WordPress should persist (no 400), and disconnecting should actually null the columns. Check `decrypted_user_api_keys` for the affected user after each. Also audit for any OTHER `.upsert()`/`onConflict` calls against the `user_api_keys`, `meta_config`, or `social_accounts` views across `src/` (same class of bug). See memory `reference_encrypted_views_write_pattern.md` for the full pattern. Run `npx tsc --noEmit` and `bun run build` after; the frontend deploys from the main repo's `dist/` via nginx (build = deploy).
> 
> ## 🤖 Claude *(12:31:48)*
> 
> 
> ## 🤖 Claude *(12:31:52)*
> 
> Vou começar declarando o triplet ORO desta tarefa e explorando materialmente o código afetado antes de qualquer alteração.
> 
> **ORO triplet desta task:**
> - **Operator:** MCORCH Master Execution Agent (eu)
> - **Reviewer:** Sovereign (Gabriel)
> - **Owner:** Sovereign — blast radius é o fluxo BYOK WordPress no `/dashboard/settings` (save quebrado = usuário não conecta WP; disconnect quebrado = credencial "fantasma" persiste no Vault, risco LGPD de não-revogação)
> 
> Antes de tocar em qualquer linha, vou verificar a base contra `origin/main` (memória de worktree stale) e ler materialmente os arquivos envolvidos.
> 
> ## 🤖 Claude *(12:31:55)*
> 
> 
> 🛠️ **Tool Call**: `Bash`
> ```json

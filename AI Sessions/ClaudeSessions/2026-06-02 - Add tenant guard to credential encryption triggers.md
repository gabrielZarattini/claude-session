# Add tenant guard to credential encryption triggers
**Date:** 2026-06-02 | **Session ID:** `85c240d0-59c3-4bae-b829-c36ef83a7a9f`

---

## 👤 User *(15:38:53)*

Pre-existing multi-tenant gap surfaced during the /security-review of migration `20260602140000_vault_upsert_secret_idempotent_encrypt.sql` (credential-encryption layer). NOT a regression from that migration — it predates it — but it should be closed with its own focused migration + /security-review.

## The gap
The masked-view INSTEAD OF INSERT triggers for `meta_config` and `social_accounts` lack the `auth.uid()` tenant guard that `user_api_keys` received in `supabase/migrations/20260602130000_fix_user_api_keys_instead_of_double_fire.sql`. Confirmed materially 2026-06-02: `position('auth.uid' in pg_get_functiondef('public.trg_instead_of_meta_config()'::regprocedure)) = 0` and same for `trg_instead_of_social_accounts()`.

Because those INSTEAD OF triggers are SECURITY DEFINER (owner postgres, bypass base-table RLS) and PostgreSQL does not apply a view's WHERE qualification to INSERT, an authenticated attacker can `POST /rest/v1/social_accounts` (or `/rest/v1/meta_config`) with a **spoofed `user_id` = victim** and a **fresh `id`** (no PK collision) → a row owned by the victim with attacker-controlled `access_token`/`long_lived_token` gets committed. A service-role publisher iterating that victim's `decrypted_social_accounts`/`decrypted_meta_config` could then use the attacker's injected credential/account (credential confusion / content redirection). meta_config has `UNIQUE(user_id)` so it's only injectable when the victim has no row yet; social_accounts is injectable on any unused `platform`.

NOTE: the cross-tenant *overwrite* variant (colliding `id`) is already fail-closed by `PRIMARY KEY (id)` on both base tables (proven materially — the base PK 23505 rolls the whole statement back, including the BEFORE-trigger Vault write). So this follow-up is specifically about the *injection* (spoofed user_id, fresh id) path.

## Fix (established pattern from 20260602130000)
Recreate `trg_instead_of_meta_config` (current def: `supabase/migrations/20260601000500_fix_meta_config_instead_of_trigger.sql`) and `trg_instead_of_social_accounts` (current def: `supabase/migrations/20260601000000_credential_encryption.sql` lines ~457-492), preserving ALL existing column-mapping logic verbatim, and prepend to the INSERT/UPDATE branch:
```sql
IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN
  RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';
END IF;
```
Add `SET search_path = ''` to match the hardening precedent. New migration timestamp > 20260602140000.

## Material verification (Management API: token in ~/.supabase/access-token, project ref bcyvddsykvehvpwstlfa, POST https://api.supabase.com/v1/projects/<ref>/database/query)
Simulate a user via `set_config('request.jwt.claims', '{"sub":"<attacker_uid>","role":"authenticated"}', false)` then attempt an INSERT into `public.social_accounts` with `user_id` = a DIFFERENT real auth.users id and a fresh `id`; prove it now raises `42501` (was: succeeded). Confirm a legitimate self-insert (user_id = auth.uid()) and a service_role insert still succeed. Wrap tests in BEGIN/ROLLBACK. Update SOP `docs/processes/credential-disconnect-clear.md`. MANDATORY /security-review (touches credential encryption layer, per CLAUDE.md). Only one real tenant exists today (`ada39fae-67e1-4e53-af1c-5a18e1c108e8`), so you may need a second throwaway auth.users row (respect the FK) or assert the guard logic against `auth.uid()` mismatch directly.

## 🤖 Claude *(15:39:25)*


## 🤖 Claude *(15:39:29)*

Vou começar verificando materialmente o estado atual — porque tanto o `CLAUDE.md` (Key Files Reference) quanto o git log mais recente (`87c926f`, `66859b0`) quanto minha memória indicam que esse exato gap já foi selado na migration `20260602150000_meta_social_instead_of_tenant_guard.sql` (v6.20.2). Antes de criar qualquer migration nova, preciso confirmar a realidade material (Lei 1) — não posso assumir que o gap está aberto só porque o prompt o descreve assim, nem assumir que está fechado só porque a memória diz.

Deixa eu reunir os fatos materiais em paralelo.

## 🤖 Claude *(15:39:31)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la supabase/migrations/ | grep -E \"202606021[3-9]0000|2026060215\" || echo \"NENHUM ARQUIVO 2026060215xxxx ENCONTRADO\"",
  "description": "List recent credential-layer migration files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> -rw-rw-r-- 1 ubuntu ubuntu  7581 Jun  2 10:10 20260602130000_fix_user_api_keys_instead_of_double_fire.sql
> -rw-rw-r-- 1 ubuntu ubuntu 16861 Jun  2 11:23 20260602140000_vault_upsert_secret_idempotent_encrypt.sql
> -rw-rw-r-- 1 ubuntu ubuntu  8251 Jun  2 11:47 20260602150000_meta_social_instead_of_tenant_guard.sql
> ```

## 🤖 Claude *(15:39:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -12",
  "description": "Show recent commit history"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 66859b0 chore(sprint): selo v6.20.2 — idempotência do Vault + guard de tenant meta/social
> 5b79980 docs(handoff): seal v6.20.2 — vault encrypt idempotente + guard de tenant meta/social
> beec4aa docs(readme): v6.20.2 — vault encrypt idempotente + guard de tenant meta/social
> deb661c docs(processes): fecha débito de idempotência + guard meta/social no SOP de credenciais
> 87c926f fix(credentials): guard de tenant nas INSTEAD OF de meta_config/social_accounts
> 2db5f62 fix(credentials): vault_upsert_secret idempotente — elimina 23505 ao rotacionar segredo
> ec80563 chore(sprint): selo v6.20.1 — WordPress BYOK + fix do double-fire da encriptação
> dcf5abb docs(handoff): seal v6.20.1 — WordPress BYOK + fix do double-fire da encriptação de credenciais
> 6b2f8db docs(readme): v6.20.1 — WordPress BYOK + fix do double-fire da encriptação de credenciais
> 377251e docs(processes): SOP de disconnect/clear de credencial em views Vault-mascaradas
> bafa7a2 fix(settings): WordPress conecta via .insert e desconecta via RPC disconnect_wordpress
> 5dc8084 fix(credentials): disconnect_wordpress RPC + elimina double-fire do INSTEAD OF de user_api_keys
> ```

## 🤖 Claude *(15:39:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git fetch origin --quiet 2>&1; echo \"--- local main vs origin/main ---\"; git rev-parse HEAD; git rev-parse origin/main 2>/dev/null || echo \"(no origin/main)\"; echo \"--- behind/ahead ---\"; git rev-list --left-right --count origin/main...HEAD 2>/dev/null || echo \"(cannot compare)\"",
  "description": "Check local HEAD against origin/main"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> --- local main vs origin/main ---
> 66859b065e81de8adddda8fa41f35f1c9137d65b
> 66859b065e81de8adddda8fa41f35f1c9137d65b
> --- behind/ahead ---
> 0	0
> ```

## 🤖 Claude *(15:39:41)*


## 🤖 Claude *(15:39:44)*

Material fact #1: o arquivo `20260602150000_meta_social_instead_of_tenant_guard.sql` **existe** (8251 bytes), o commit `87c926f` existe, e estou em `main` sincronizado com `origin/main` (0 behind / 0 ahead — não é worktree stale). Deixa eu ler o conteúdo da migration e a definição-fonte das duas triggers para confirmar o que foi realmente escrito.

## 🤖 Claude *(15:39:44)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260602150000_meta_social_instead_of_tenant_guard.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: tenant guard on meta_config / social_accounts masked-view INSTEAD OF triggers.
> 2	-- ─────────────────────────────────────────────────────────────────────────────
> 3	-- Closes a PRE-EXISTING cross-tenant injection gap surfaced during the /security-review of
> 4	-- 20260602140000 (NOT a regression of that migration). trg_instead_of_meta_config and
> 5	-- trg_instead_of_social_accounts are SECURITY DEFINER (owner postgres, bypass base-table RLS) and
> 6	-- the masked public views grant INSERT to authenticated. PostgreSQL does not apply a view's WHERE
> 7	-- qualification to INSERT, so an authenticated caller could POST a row with a SPOOFED user_id (a
> 8	-- victim's) and a FRESH id — committing a credential row OWNED BY the victim with attacker-controlled
> 9	-- tokens. A service-role publisher iterating that victim's decrypted_* rows would then use the
> 10	-- injected credential (credential confusion / content redirection). The overwrite variant (colliding
> 11	-- id) is already fail-closed by PRIMARY KEY(id) on both base tables; this fixes the injection variant.
> 12	--
> 13	-- Fix: port the exact tenant guard user_api_keys received in 20260602130000 to the INSERT and UPDATE
> 14	-- branches of both sibling INSTEAD OF triggers, and pin SET search_path = '' (they had no pin).
> 15	-- The function bodies below are reproduced VERBATIM from the live definitions (pg_get_functiondef,
> 16	-- 2026-06-02) — preserving every column mapping, COALESCE default, and masked sentinel byte-for-byte —
> 17	-- with ONLY the guard + search_path added. Triggers keep their bindings (CREATE OR REPLACE preserves
> 18	-- the oid) — no trigger re-create.
> 19	--
> 20	-- Production safety (verified 2026-06-02): every legitimate writer is either service_role (the social
> 21	-- OAuth callback — the sole social INSERT — plus refresh-social-token / publish-meta / sync-meta-ads /
> 22	-- self-heal, all using SB_SECRET_KEY → exempt) or an authenticated client writing its OWN row with
> 23	-- user_id = auth.uid() (useMetaConfig.insert; useSocialAccounts never inserts client-side). No legit
> 24	-- non-service-role path writes user_id <> auth.uid(), so the guard only blocks the attack.
> 25	--
> 26	-- SOP: docs/processes/credential-disconnect-clear.md. MANDATORY /security-review (credential layer).
> 27	
> 28	CREATE OR REPLACE FUNCTION public.trg_instead_of_meta_config()
> 29	 RETURNS trigger
> 30	 LANGUAGE plpgsql
> 31	 SECURITY DEFINER
> 32	 SET search_path = ''
> 33	AS $function$
> 34	BEGIN
> 35	  IF TG_OP = 'DELETE' THEN
> 36	    DELETE FROM public.meta_config_table WHERE id = OLD.id;
> 37	    RETURN OLD;
> 38	  ELSIF TG_OP = 'INSERT' THEN
> 39	    -- Tenant guard (mirrors 20260602130000 for user_api_keys): a non-service-role caller may only
> 40	    -- write its OWN credential row. Closes a pre-existing cross-tenant injection (spoofed user_id +
> 41	    -- fresh id) that the masked view's WHERE filter does not constrain for INSERT. service_role
> 42	    -- (edge OAuth callbacks / cron) is exempt and legitimately writes arbitrary user_ids.
> 43	    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN
> 44	      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';
> 45	    END IF;
> 46	    INSERT INTO public.meta_config_table (
> 47	      id,
> 48	      user_id,
> 49	      facebook_user_id,
> 50	      long_lived_token,
> 51	      scopes,
> 52	      pages,
> 53	      instagram_business_account_id,
> 54	      whatsapp_phone_number_id,
> 55	      whatsapp_waba_id,
> 56	      meta_ad_account_id,
> 57	      requires_reauth,
> 58	      token_expires_at
> 59	    ) VALUES (
> 60	      COALESCE(NEW.id, gen_random_uuid()),
> 61	      NEW.user_id,
> 62	      NEW.facebook_user_id,
> 63	      NEW.long_lived_token,
> 64	      COALESCE(NEW.scopes, '{}'),
> 65	      COALESCE(NEW.pages, '[]'::jsonb),
> 66	      NEW.instagram_business_account_id,
> 67	      NEW.whatsapp_phone_number_id,
> 68	      NEW.whatsapp_waba_id,
> 69	      NEW.meta_ad_account_id,
> 70	      COALESCE(NEW.requires_reauth, FALSE),
> 71	      NEW.token_expires_at
> 72	    );
> 73	    RETURN NEW;
> 74	  ELSIF TG_OP = 'UPDATE' THEN
> 75	    -- Tenant guard (mirrors 20260602130000 for user_api_keys): a non-service-role caller may only
> 76	    -- write its OWN credential row. Closes a pre-existing cross-tenant injection (spoofed user_id +
> 77	    -- fresh id) that the masked view's WHERE filter does not constrain for INSERT. service_role
> 78	    -- (edge OAuth callbacks / cron) is exempt and legitimately writes arbitrary user_ids.
> 79	    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN
> 80	      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';
> 81	    END IF;
> 82	    UPDATE public.meta_config_table SET
> 83	      user_id = NEW.user_id,
> 84	      facebook_user_id = NEW.facebook_user_id,
> 85	      long_lived_token = COALESCE(NULLIF(NEW.long_lived_token, '••••••••••••'), public.meta_config_table.long_lived_token),
> 86	      scopes = COALESCE(NEW.scopes, public.meta_config_table.scopes),
> 87	      pages = COALESCE(NULLIF(NEW.pages, to_jsonb('••••••••••••'::text)), public.meta_config_table.pages),
> 88	      instagram_business_account_id = NEW.instagram_business_account_id,
> 89	      whatsapp_phone_number_id = NEW.whatsapp_phone_number_id,
> 90	      whatsapp_waba_id = NEW.whatsapp_waba_id,
> 91	      meta_ad_account_id = NEW.meta_ad_account_id,
> 92	      requires_reauth = COALESCE(NEW.requires_reauth, public.meta_config_table.requires_reauth),
> 93	      token_expires_at = NEW.token_expires_at,
> 94	      updated_at = now()
> 95	    WHERE id = OLD.id;
> 96	    RETURN NEW;
> 97	  END IF;
> 98	  RETURN NULL;
> 99	END;
> 100	$function$;
> 101	
> 102	CREATE OR REPLACE FUNCTION public.trg_instead_of_social_accounts()
> 103	 RETURNS trigger
> 104	 LANGUAGE plpgsql
> 105	 SECURITY DEFINER
> 106	 SET search_path = ''
> 107	AS $function$
> 108	BEGIN
> 109	  IF TG_OP = 'DELETE' THEN
> 110	    DELETE FROM public.social_accounts_table WHERE id = OLD.id;
> 111	    RETURN OLD;
> 112	  ELSIF TG_OP = 'INSERT' THEN
> 113	    -- Tenant guard (mirrors 20260602130000 for user_api_keys): a non-service-role caller may only
> 114	    -- write its OWN credential row. Closes a pre-existing cross-tenant injection (spoofed user_id +
> 115	    -- fresh id) that the masked view's WHERE filter does not constrain for INSERT. service_role
> 116	    -- (edge OAuth callbacks / cron) is exempt and legitimately writes arbitrary user_ids.
> 117	    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN
> 118	      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';
> 119	    END IF;
> 120	    INSERT INTO public.social_accounts_table (
> 121	      id, user_id, platform, platform_user_id, platform_username, access_token, refresh_token, token_expires_at, scopes, is_active, metadata
> 122	    ) VALUES (
> 123	      COALESCE(NEW.id, gen_random_uuid()), NEW.user_id, NEW.platform, NEW.platform_user_id, NEW.platform_username, NEW.access_token, NEW.refresh_token, NEW.token_expires_at, NEW.scopes, NEW.is_active, NEW.metadata
> 124	    );
> 125	    RETURN NEW;
> 126	  ELSIF TG_OP = 'UPDATE' THEN
> 127	    -- Tenant guard (mirrors 20260602130000 for user_api_keys): a non-service-role caller may only
> 128	    -- write its OWN credential row. Closes a pre-existing cross-tenant injection (spoofed user_id +
> 129	    -- fresh id) that the masked view's WHERE filter does not constrain for INSERT. service_role
> 130	    -- (edge OAuth callbacks / cron) is exempt and legitimately writes arbitrary user_ids.
> 131	    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN
> 132	      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';
> 133	    END IF;
> 134	    UPDATE public.social_accounts_table SET
> 135	      user_id = NEW.user_id,
> 136	      platform = NEW.platform,
> 137	      platform_user_id = NEW.platform_user_id,
> 138	      platform_username = NEW.platform_username,
> 139	      access_token = COALESCE(NULLIF(NEW.access_token, '••••••••••••'), public.social_accounts_table.access_token),
> 140	      refresh_token = COALESCE(NULLIF(NEW.refresh_token, '••••••••••••'), public.social_accounts_table.refresh_token),
> 141	      token_expires_at = NEW.token_expires_at,
> 142	      scopes = NEW.scopes,
> 143	      is_active = NEW.is_active,
> 144	      metadata = NEW.metadata,
> 145	      updated_at = now()
> 146	    WHERE id = OLD.id;
> 147	    RETURN NEW;
> 148	  END IF;
> 149	  RETURN NULL;
> 150	END;
> 151	$function$;
> 152	
> ```

## 🤖 Claude *(15:40:03)*


## 🤖 Claude *(15:40:07)*

Material fact #2: o arquivo da migration está **completo e correto** — ambas as funções (`trg_instead_of_meta_config` e `trg_instead_of_social_accounts`) têm `SET search_path = ''`, são SECURITY DEFINER, e têm o guard `auth.uid()` exato (`errcode = '42501'`) nos DOIS branches (INSERT + UPDATE), com isenção de `service_role`. Isso é precisamente o fix que o prompt prescreve.

Mas arquivo commitado **não é** prova de função deployada (Lei 1). A questão material decisiva: **o guard está aplicado no banco vivo?** O prompt registra o estado *antes* (`position('auth.uid' ...) = 0`). Preciso checar o estado *atual* via Management API.

## 🤖 Claude *(15:40:08)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "test -f ~/.supabase/access-token && echo \"TOKEN FILE EXISTS ($(wc -c < ~/.supabase/access-token) bytes)\" || echo \"NO TOKEN FILE\"",
  "description": "Verify Supabase Management API token file exists"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> TOKEN FILE EXISTS (44 bytes)
> ```

## 🤖 Claude *(15:40:11)*


## 🤖 Claude *(15:40:12)*

O token existe. Agora a verificação material decisiva — checar as definições deployadas das duas funções no banco vivo:

## 🤖 Claude *(15:40:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "TOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\nQUERY='SELECT p.proname AS fn, (position('\"'\"'auth.uid'\"'\"' in pg_get_functiondef(p.oid)) > 0) AS has_uid_guard, (position('\"'\"'42501'\"'\"' in pg_get_functiondef(p.oid)) > 0) AS has_42501, (position('\"'\"'service_role'\"'\"' in pg_get_functiondef(p.oid)) > 0) AS has_service_role_exempt, (array_to_string(p.proconfig, '\"'\"','\"'\"')) AS proconfig FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace WHERE n.nspname = '\"'\"'public'\"'\"' AND p.proname IN ('\"'\"'trg_instead_of_meta_config'\"'\"','\"'\"'trg_instead_of_social_accounts'\"'\"') ORDER BY p.proname;'\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" \\\n  -H \"Content-Type: application/json\" \\\n  -d \"{\\\"query\\\": $(printf '%s' \"$QUERY\" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}\"\necho \"\"",
  "description": "Query live DB for deployed trigger function guard state"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [{"fn":"trg_instead_of_meta_config","has_uid_guard":true,"has_42501":true,"has_service_role_exempt":true,"proconfig":"search_path=\"\""},{"fn":"trg_instead_of_social_accounts","has_uid_guard":true,"has_42501":true,"has_service_role_exempt":true,"proconfig":"search_path=\"\""}]
> ```

## 🤖 Claude *(15:42:41)*


## 🤖 Claude *(15:42:46)*

**Material proof decisiva (banco vivo):** ambas as funções deployadas têm `has_uid_guard=true`, `has_42501=true`, `has_service_role_exempt=true`, e `proconfig=search_path=""`. **O gap já está fechado em produção**, não só no arquivo. A migration `20260602150000` foi commitada (`87c926f`) E aplicada.

Isso contradiz o enquadramento do prompt (que cita `position('auth.uid'...) = 0` como estado atual) — mas aquele `= 0` era o estado *antes* do fix; já foi selado em v6.20.2.

Antes de concluir, vou fazer a verificação **comportamental independente** (Lei 1 — não auto-declarada): simular o ataque e provar que realmente levanta `42501`, não só que o texto está presente. Primeiro vou sondar como a Management API retorna multi-statement, e em paralelo confirmar o SOP e o que o seal já registrou.

## 🤖 Claude *(15:42:50)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "TOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\n# Probe: does the /database/query endpoint return the SELECT result when a ROLLBACK follows in the same batch?\nPROBE='BEGIN; CREATE TEMP TABLE _probe(a int) ON COMMIT DROP; INSERT INTO _probe VALUES (42); SELECT a AS probe_value FROM _probe; ROLLBACK;'\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"{\\\"query\\\": $(printf '%s' \"$PROBE\" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}\"\necho \"\"",
  "description": "Probe Management API multi-statement return behavior"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [{"probe_value":42}]
> ```

## 🤖 Claude *(15:42:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== git: commit that introduced the migration ===\"; git log --oneline --follow -- supabase/migrations/20260602150000_meta_social_instead_of_tenant_guard.sql\necho \"\"; echo \"=== SOP mentions of the tenant guard / cross-tenant injection ===\"; grep -nE \"tenant guard|cross-tenant|injection|42501|20260602150000|auth\\.uid\" docs/processes/credential-disconnect-clear.md 2>/dev/null | head -40 || echo \"(SOP file not found)\"",
  "description": "Check migration commit and SOP coverage"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === git: commit that introduced the migration ===
> 87c926f fix(credentials): guard de tenant nas INSTEAD OF de meta_config/social_accounts
> 
> === SOP mentions of the tenant guard / cross-tenant injection ===
> 22:`disconnect_wordpress()` RPC (SECURITY DEFINER, owner `postgres`), scoped to `auth.uid()`.
> 31:2. RPC reads the caller's `wp_app_password` reference from `user_api_keys_table WHERE user_id = auth.uid()`.
> 33:4. RPC deletes the Vault secret, scoped to BOTH `id = <ref>` AND `name = 'user_api_keys_wp_app_password_' || auth.uid()` (the name binding makes it provably impossible to delete another tenant's secret, even though `wp_app_password` is client-writable).
> 113:INSTEAD OF triggers lacked the `auth.uid()` tenant guard that `user_api_keys` got in `20260602130000`.
> 118:Migration `20260602150000_meta_social_instead_of_tenant_guard.sql` ports the same guard
> 119:(`auth.role() <> 'service_role' AND NEW.user_id <> auth.uid()` → `42501`) to the INSERT and UPDATE
> 123:decrypted_token:"INJECTED-BY-ATTACKER"}`. AFTER — same → `42501` on both tables; legit self-insert
> 124:(`user_id=auth.uid()`) → `{inserted:1, decrypted:"my-own-token"}`; service_role with arbitrary
> ```

## 🤖 Claude *(15:44:09)*


## 🤖 Claude *(15:44:12)*

Probe confirma: a Management API retorna o resultado do `SELECT` mesmo com `ROLLBACK` na sequência (`[{"probe_value":42}]`). E o SOP `credential-disconnect-clear.md` **já foi atualizado** (linhas 113-124) documentando o gap, o fix (`20260602150000`) e até a prova antes/depois.

Agora a prova comportamental independente desta sessão. Vou escrever o ataque num arquivo e disparar via Management API (tudo em `BEGIN…ROLLBACK` — zero efeito colateral):

## 🤖 Claude *(15:44:29)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/tmp/guard_attack_sim.sql",
  "content": "BEGIN;\nCREATE TEMP TABLE _guard_results(test text, outcome text) ON COMMIT DROP;\nDO $$\nDECLARE\n  v_attacker uuid := gen_random_uuid();\n  v_victim   uuid := 'ada39fae-67e1-4e53-af1c-5a18e1c108e8';\nBEGIN\n  -- T1: authenticated ATTACKER injects a social_accounts row OWNED BY victim (fresh id) -> must be 42501\n  PERFORM set_config('request.jwt.claims', json_build_object('sub', v_attacker::text, 'role','authenticated')::text, true);\n  BEGIN\n    INSERT INTO public.social_accounts(id, user_id, platform, platform_user_id, platform_username, access_token, refresh_token, is_active, metadata)\n      VALUES (gen_random_uuid(), v_victim, '_gt_attack', 'x', 'x', 'ATTACKER_TOKEN', NULL, true, '{}'::jsonb);\n    INSERT INTO _guard_results VALUES ('1_social_attack_injection','FAIL -- injection COMMITTED (GAP OPEN)');\n  EXCEPTION\n    WHEN insufficient_privilege THEN INSERT INTO _guard_results VALUES ('1_social_attack_injection','PASS -- blocked 42501: '||SQLERRM);\n    WHEN others THEN INSERT INTO _guard_results VALUES ('1_social_attack_injection','UNEXPECTED '||SQLSTATE||': '||SQLERRM);\n  END;\n\n  -- T2: same attack vs meta_config -> must be 42501 (guard fires before any UNIQUE check)\n  BEGIN\n    INSERT INTO public.meta_config(id, user_id, facebook_user_id, long_lived_token)\n      VALUES (gen_random_uuid(), v_victim, 'fb_attacker', 'ATTACKER_TOKEN');\n    INSERT INTO _guard_results VALUES ('2_meta_attack_injection','FAIL -- injection COMMITTED (GAP OPEN)');\n  EXCEPTION\n    WHEN insufficient_privilege THEN INSERT INTO _guard_results VALUES ('2_meta_attack_injection','PASS -- blocked 42501: '||SQLERRM);\n    WHEN others THEN INSERT INTO _guard_results VALUES ('2_meta_attack_injection','UNEXPECTED '||SQLSTATE||': '||SQLERRM);\n  END;\n\n  -- T3: legitimate self-insert (authenticated, user_id = auth.uid()) must STILL succeed\n  PERFORM set_config('request.jwt.claims', json_build_object('sub', v_victim::text, 'role','authenticated')::text, true);\n  BEGIN\n    INSERT INTO public.social_accounts(id, user_id, platform, platform_user_id, platform_username, access_token, refresh_token, is_active, metadata)\n      VALUES (gen_random_uuid(), v_victim, '_gt_legit', 'x', 'x', 'SELF_TOKEN', NULL, true, '{}'::jsonb);\n    INSERT INTO _guard_results VALUES ('3_social_legit_self_insert','PASS -- self-insert allowed');\n  EXCEPTION\n    WHEN insufficient_privilege THEN INSERT INTO _guard_results VALUES ('3_social_legit_self_insert','FAIL -- guard wrongly blocked legit self-insert (42501)');\n    WHEN others THEN INSERT INTO _guard_results VALUES ('3_social_legit_self_insert','OTHER '||SQLSTATE||': '||SQLERRM);\n  END;\n\n  -- T4: service_role insert with ARBITRARY user_id (OAuth callback path) must STILL succeed\n  PERFORM set_config('request.jwt.claims', json_build_object('role','service_role')::text, true);\n  BEGIN\n    INSERT INTO public.social_accounts(id, user_id, platform, platform_user_id, platform_username, access_token, refresh_token, is_active, metadata)\n      VALUES (gen_random_uuid(), v_victim, '_gt_svc', 'x', 'x', 'SVC_TOKEN', NULL, true, '{}'::jsonb);\n    INSERT INTO _guard_results VALUES ('4_social_service_role_insert','PASS -- service_role insert allowed');\n  EXCEPTION\n    WHEN insufficient_privilege THEN INSERT INTO _guard_results VALUES ('4_social_service_role_insert','FAIL -- guard wrongly blocked service_role (42501)');\n    WHEN others THEN INSERT INTO _guard_results VALUES ('4_social_service_role_insert','OTHER '||SQLSTATE||': '||SQLERRM);\n  END;\n\n  -- T5: meta legit self-insert. success OR unique_violation(23505) both prove guard ALLOWED the owner;\n  -- only 42501 would be a regression.\n  PERFORM set_config('request.jwt.claims', json_build_object('sub', v_victim::text, 'role','authenticated')::text, true);\n  BEGIN\n    INSERT INTO public.meta_config(id, user_id, facebook_user_id, long_lived_token)\n      VALUES (gen_random_uuid(), v_victim, 'fb_self', 'SELF_TOKEN');\n    INSERT INTO _guard_results VALUES ('5_meta_legit_self_insert','PASS -- self-insert allowed');\n  EXCEPTION\n    WHEN insufficient_privilege THEN INSERT INTO _guard_results VALUES ('5_meta_legit_self_insert','FAIL -- guard wrongly blocked legit self-insert (42501)');\n    WHEN unique_violation THEN INSERT INTO _guard_results VALUES ('5_meta_legit_self_insert','PASS -- guard allowed; reached pre-existing UNIQUE(user_id) 23505 (expected: victim already configured)');\n    WHEN others THEN INSERT INTO _guard_results VALUES ('5_meta_legit_self_insert','OTHER '||SQLSTATE||': '||SQLERRM);\n  END;\n\n  PERFORM set_config('request.jwt.claims', NULL, true);\nEND $$;\nSELECT test, outcome FROM _guard_results ORDER BY test;\nROLLBACK;\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /tmp/guard_attack_sim.sql (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(15:44:33)*


## 🤖 Claude *(15:44:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "TOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"$(python3 -c 'import json,sys; print(json.dumps({\"query\": open(\"/tmp/guard_attack_sim.sql\").read()}))')\"\necho \"\"",
  "description": "Run behavioral attack simulation against live DB"
}
```

## 🤖 Claude *(15:44:37)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/credential-disconnect-clear.md",
  "offset": 104,
  "limit": 35
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [{"test":"1_social_attack_injection","outcome":"UNEXPECTED 22P02: invalid input value for enum social_platform: \"_gt_attack\""},{"test":"2_meta_attack_injection","outcome":"PASS -- blocked 42501: cannot write credentials for another user"},{"test":"3_social_legit_self_insert","outcome":"OTHER 22P02: invalid input value for enum social_platform: \"_gt_legit\""},{"test":"4_social_service_role_insert","outcome":"OTHER 22P02: invalid input value for enum social_platform: \"_gt_svc\""},{"test":"5_meta_legit_self_insert","outcome":"PASS -- self-insert allowed"}]
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 104	  all three triggers verified `calls_helper=true, calls_create_secret=false`.)
> 105	
> 106	**Residual nuance (not a defect):** the helper opens a per-call subtransaction (its `EXCEPTION` block)
> 107	only to absorb the rare concurrent-create race; the common rotate path takes the no-exception
> 108	SELECT→`update_secret` branch.
> 109	
> 110	## Tenant isolation on the masked-view INSTEAD OF triggers (hardened 2026-06-02)
> 111	
> 112	Surfaced during the `/security-review` of `20260602140000`: the `meta_config` / `social_accounts`
> 113	INSTEAD OF triggers lacked the `auth.uid()` tenant guard that `user_api_keys` got in `20260602130000`.
> 114	Because those triggers are SECURITY DEFINER (bypass base-table RLS) and PostgreSQL does not apply a
> 115	view's WHERE qualification to INSERT, an authenticated caller could `POST` a row with a **spoofed
> 116	`user_id`** (a victim's) + a **fresh `id`** → a credential row owned by the victim with attacker
> 117	tokens (the *overwrite* variant — colliding `id` — was already fail-closed by `PRIMARY KEY(id)`).
> 118	Migration `20260602150000_meta_social_instead_of_tenant_guard.sql` ports the same guard
> 119	(`auth.role() <> 'service_role' AND NEW.user_id <> auth.uid()` → `42501`) to the INSERT and UPDATE
> 120	branches of both, pins `search_path=''`, and reproduces the live bodies verbatim (column maps,
> 121	COALESCE defaults, masked sentinels). **Material proof (2026-06-02, rolled back):** BEFORE — attacker
> 122	`sub=1111…` injected a `meta_config` for victim `ada39fae…` → `{rows_owned_by_victim:1,
> 123	decrypted_token:"INJECTED-BY-ATTACKER"}`. AFTER — same → `42501` on both tables; legit self-insert
> 124	(`user_id=auth.uid()`) → `{inserted:1, decrypted:"my-own-token"}`; service_role with arbitrary
> 125	`user_id` → `{inserted:1}` (exempt). Every legit writer is service_role (edge OAuth/cron) or a client
> 126	writing its own row, so the guard breaks nothing.
> 127	
> ```

## 🤖 Claude *(15:44:54)*


## 🤖 Claude *(15:44:59)*

Resultado misto, e diagnóstico claro:

- **T2 `meta_attack_injection`: PASS** — `42501: cannot write credentials for another user` ✅ (a prova de segurança crítica para meta_config — o guard dispara).
- **T5 `meta_legit_self_insert`: PASS** — owner legítimo passa ✅.
- **T1/T3/T4 (social_accounts): 22P02** — `invalid input value for enum social_platform: "_gt_attack"`. A coluna `platform` é um ENUM `social_platform`; meus valores fake são rejeitados no cast **antes** do trigger rodar. Teste inválido por construção minha, não falha do guard.

E o SOP (linhas 110-126) confirma: já documenta o gap, o fix `20260602150000`, e a prova material antes/depois. 

Preciso re-rodar os testes de `social_accounts` com um valor de enum **real**. Vou descobrir os valores válidos:

## 🤖 Claude *(15:45:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "TOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\nQUERY='SELECT e.enumlabel FROM pg_enum e JOIN pg_type t ON t.oid = e.enumtypid WHERE t.typname = '\"'\"'social_platform'\"'\"' ORDER BY e.enumsortorder;'\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"{\\\"query\\\": $(printf '%s' \"$QUERY\" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}\"\necho \"\"\necho \"--- existing social_accounts platforms for victim (to anticipate UNIQUE) ---\"\nQUERY2='SELECT platform, count(*) FROM public.social_accounts_table WHERE user_id = '\"'\"'ada39fae-67e1-4e53-af1c-5a18e1c108e8'\"'\"' GROUP BY platform;'\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"{\\\"query\\\": $(printf '%s' \"$QUERY2\" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}\"\necho \"\"",
  "description": "Get social_platform enum values and victim's existing rows"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [{"enumlabel":"linkedin"},{"enumlabel":"instagram"},{"enumlabel":"facebook"},{"enumlabel":"twitter"},{"enumlabel":"tiktok"},{"enumlabel":"youtube"},{"enumlabel":"pinterest"},{"enumlabel":"wordpress"}]
> --- existing social_accounts platforms for victim (to anticipate UNIQUE) ---
> [{"platform":"linkedin","count":1},{"platform":"instagram","count":1},{"platform":"facebook","count":1}]
> ```

## 🤖 Claude *(15:45:16)*


## 🤖 Claude *(15:45:18)*

Enum válido: `linkedin, instagram, facebook, twitter, tiktok, youtube, pinterest, wordpress`. Vítima já tem `linkedin/instagram/facebook` — vou usar `tiktok` (ataque), `youtube` (legit), `pinterest` (service_role) para os positivos não colidirem com `UNIQUE(user_id, platform)`. Re-rodando a suíte completa com enums reais:

## 🤖 Claude *(15:45:20)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/tmp/guard_attack_sim.sql",
  "old_string": "      VALUES (gen_random_uuid(), v_victim, '_gt_attack', 'x', 'x', 'ATTACKER_TOKEN', NULL, true, '{}'::jsonb);",
  "new_string": "      VALUES (gen_random_uuid(), v_victim, 'tiktok', 'x', 'x', 'ATTACKER_TOKEN', NULL, true, '{}'::jsonb);"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /tmp/guard_attack_sim.sql has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(15:45:24)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/tmp/guard_attack_sim.sql",
  "old_string": "      VALUES (gen_random_uuid(), v_victim, '_gt_legit', 'x', 'x', 'SELF_TOKEN', NULL, true, '{}'::jsonb);",
  "new_string": "      VALUES (gen_random_uuid(), v_victim, 'youtube', 'x', 'x', 'SELF_TOKEN', NULL, true, '{}'::jsonb);"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /tmp/guard_attack_sim.sql has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(15:45:28)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/tmp/guard_attack_sim.sql",
  "old_string": "      VALUES (gen_random_uuid(), v_victim, '_gt_svc', 'x', 'x', 'SVC_TOKEN', NULL, true, '{}'::jsonb);",
  "new_string": "      VALUES (gen_random_uuid(), v_victim, 'pinterest', 'x', 'x', 'SVC_TOKEN', NULL, true, '{}'::jsonb);"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /tmp/guard_attack_sim.sql has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(15:45:33)*


## 🤖 Claude *(15:45:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "TOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"$(python3 -c 'import json,sys; print(json.dumps({\"query\": open(\"/tmp/guard_attack_sim.sql\").read()}))')\" | python3 -m json.tool\necho \"\"",
  "description": "Re-run behavioral attack simulation with valid enum platforms"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [
>     {
>         "test": "1_social_attack_injection",
>         "outcome": "PASS -- blocked 42501: cannot write credentials for another user"
>     },
>     {
>         "test": "2_meta_attack_injection",
>         "outcome": "PASS -- blocked 42501: cannot write credentials for another user"
>     },
>     {
>         "test": "3_social_legit_self_insert",
>         "outcome": "PASS -- self-insert allowed"
>     },
>     {
>         "test": "4_social_service_role_insert",
>         "outcome": "PASS -- service_role insert allowed"
>     },
>     {
>         "test": "5_meta_legit_self_insert",
>         "outcome": "PASS -- self-insert allowed"
>     }
> ]
> ```

## 🤖 Claude *(15:45:49)*


## 🤖 Claude *(15:45:53)*

**Cinco de cinco PASS** — prova comportamental independente, toda em `BEGIN…ROLLBACK`:

| Teste | Resultado |
|-------|-----------|
| `1_social_attack_injection` | **PASS** — bloqueado `42501` |
| `2_meta_attack_injection` | **PASS** — bloqueado `42501` |
| `3_social_legit_self_insert` | **PASS** — owner legítimo passa |
| `4_social_service_role_insert` | **PASS** — service_role (OAuth/cron) isento passa |
| `5_meta_legit_self_insert` | **PASS** — owner legítimo passa |

Agora, rigor de Lei 1: provar que meu teste **não deixou resíduo** (o `ROLLBACK` deve ter desfeito os inserts legítimos/service das tentativas):

## 🤖 Claude *(15:45:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "TOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\nQUERY='SELECT '\"'\"'social_accounts'\"'\"' AS tbl, string_agg(platform::text, '\"'\"','\"'\"' ORDER BY platform::text) AS platforms, count(*) AS n FROM public.social_accounts_table WHERE user_id = '\"'\"'ada39fae-67e1-4e53-af1c-5a18e1c108e8'\"'\"' UNION ALL SELECT '\"'\"'meta_config'\"'\"', NULL, count(*) FROM public.meta_config_table WHERE user_id = '\"'\"'ada39fae-67e1-4e53-af1c-5a18e1c108e8'\"'\"' UNION ALL SELECT '\"'\"'any_test_residue (tiktok/youtube/pinterest)'\"'\"', string_agg(DISTINCT platform::text, '\"'\"','\"'\"'), count(*) FROM public.social_accounts_table WHERE platform IN ('\"'\"'tiktok'\"'\"','\"'\"'youtube'\"'\"','\"'\"'pinterest'\"'\"');'\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"{\\\"query\\\": $(printf '%s' \"$QUERY\" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}\" | python3 -m json.tool\necho \"\"\nrm -f /tmp/guard_attack_sim.sql && echo \"(temp sql removed)\"",
  "description": "Verify rollback left zero residue in credential tables"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [
>     {
>         "tbl": "social_accounts",
>         "platforms": "facebook,instagram,linkedin",
>         "n": 3
>     },
>     {
>         "tbl": "meta_config",
>         "platforms": null,
>         "n": 0
>     },
>     {
>         "tbl": "any_test_residue (tiktok/youtube/pinterest)",
>         "platforms": null,
>         "n": 0
>     }
> ]
> 
> (temp sql removed)
> ```

## 🤖 Claude *(15:46:25)*


## 🤖 Claude *(15:46:29)*

Zero resíduo — `ROLLBACK` perfeito:
- `social_accounts` da vítima: ainda exatamente `facebook,instagram,linkedin` (3 linhas), intacto.
- `meta_config` da vítima: 0 linhas (o que confirma *por que* a injeção era explorável de verdade — sem linha, o `UNIQUE(user_id)` não barrava o atacante).
- Nenhuma linha `tiktok/youtube/pinterest` em lugar nenhum — meus inserts positivos foram totalmente revertidos.

Agora confirmar o estado de governança: a migration está commitada e houve `/security-review`? Vou checar o commit e os docs de seal.

## 🤖 Claude *(15:46:33)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== git status (working tree) ===\"; git status --porcelain | grep -v '^?? /tmp' || echo \"(clean \u2014 nothing staged/modified)\"\necho \"\"; echo \"=== commit 87c926f contents ===\"; git show 87c926f --stat --format=\"%H%n%an %ad%n%s\" | head -20\necho \"\"; echo \"=== committed migration == file on disk? ===\"; git show 87c926f:supabase/migrations/20260602150000_meta_social_instead_of_tenant_guard.sql > /tmp/committed_mig.sql 2>/dev/null && diff -q /tmp/committed_mig.sql supabase/migrations/20260602150000_meta_social_instead_of_tenant_guard.sql && echo \"IDENTICAL (committed == working tree)\"; rm -f /tmp/committed_mig.sql",
  "description": "Confirm migration committed and matches working tree"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === git status (working tree) ===
> (clean — nothing staged/modified)
> 
> === commit 87c926f contents ===
> 87c926fbcf4c2ff1de3833ce5330d5f14223d4fe
> Gabriel Zarattini Tue Jun 2 11:57:02 2026 -0300
> fix(credentials): guard de tenant nas INSTEAD OF de meta_config/social_accounts
> 
>  ...2150000_meta_social_instead_of_tenant_guard.sql | 151 +++++++++++++++++++++
>  1 file changed, 151 insertions(+)
> 
> === committed migration == file on disk? ===
> IDENTICAL (committed == working tree)
> ```

## 🤖 Claude *(15:46:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== security-review evidence around v6.20.2 seal ===\"; grep -rniE \"security[- ]review|/security-review\" HANDOFF.md docs/handoff* 2>/dev/null | grep -iE \"2026060215|meta.?social|tenant guard|v6\\.20\\.2|20260602\" | head -20\necho \"\"; echo \"=== broader: any security-review mention in HANDOFF.md tail ===\"; grep -niE \"security[- ]review\" HANDOFF.md | tail -10 || echo \"(none in HANDOFF.md)\"",
  "description": "Search seal docs for security-review evidence"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === security-review evidence around v6.20.2 seal ===
> HANDOFF.md:16:**v6.20.2 (2026-06-02)** — Sessão disparada pela dívida residual que a própria seal v6.20.1 anotou no Pending: o `trg_encrypt_user_api_keys` (+ irmãos meta/social) chamava `vault.create_secret` **incondicionalmente** → re-salvar um segredo p/ valor novo colidia no índice único `vault.secrets.name` (`23505`) — o caso "editar a senha WP sem desconectar antes". Padrão dominante: **probe-first material** (Management API, todo teste em `BEGIN…ROLLBACK` → zero mutação de produção) + **adversarial verify** — um achado HIGH do `/security-review` foi REFUTADO materialmente (o overwrite cross-tenant é fail-closed pelo `PRIMARY KEY`, md5 da vítima inalterado), mas a investigação revelou um gap REAL paralelo (injeção cross-tenant id-novo nas INSTEAD OF de meta/social), fechado na mesma sessão.
> HANDOFF.md:69:- **Segredo órfão no disconnect Meta/social:** desconectar Meta (`useMetaConfig.disconnect`) ou social deleta só a linha base via INSTEAD OF DELETE — o segredo Vault (`meta_config_long_lived_token_<id>` etc.) **fica órfão** (plaintext retido). Paralelo ao que `disconnect_wordpress()` resolveu pro WP; precisa de RPC dedicada (nula linha + revoga segredo) + `/security-review`. Débito LGPD/retenção.
> 
> === broader: any security-review mention in HANDOFF.md tail ===
> 717:- [x] Toda claim tem prova? SIM — tsc exit 0, 216 testes, security-review, node UUID, rebase verificado por git rev-list
> 769:→ `/security-review` → `db push` → **anticorpo**: edge functions (`generate-video`, `check-video-status`) DEVEM checar o `{error}` do `.update()`; adicionar teste que pega "update com enum/coluna inválida falhando em silêncio". Depois disso, o código **já deployado** (check-video-status v27) passa a persistir sem novo deploy.
> 782:- [x] Pendência do enum registrada (migration exige /security-review antes de db push)
> 1038:- **OTD-ML-002 RESOLVIDO** — migration `20260530183000_affiliate_tag_per_user.sql` aplicada em prod (`supabase db push` exit 0; `/security-review` passou); coluna `affiliate_config.affiliate_tag` + tag do Usuário Zero populada (`ada39fae`→`caga6077534`). Antes o script passava o `app_id` OAuth (compartilhado entre 2 tenants — `3286108278277786`) como "affiliate id"; agora usa a TAG per-user via `matt_word`, fail-closed (sem tag → sem link).
> 1048:| Migration `20260530183000` | ✅ aplicada em prod (`supabase db push` exit 0); `/security-review` PASSED |
> 2588:| `/security-review` | ✅ Zero vulnerabilidades — gate admin fail-closed, queries parametrizadas |
> 2610:**Material proofs:** `tsc --noEmit` zero erros · `/security-review` limpo · migration `Finished supabase db push` · Edge Function `Deployed ... admin-manage-user (106.3kB)` · build `built in 21.36s` · 4 commits (`3d63cc9` `7e2c0bd` `c80dd21` `e220e67`) · milestone node `92270198-ca27-443f-8bdc-715a08cf0930` (handoff, embedded 768d) · mesh 8363 nodes.
> 3717:Sessão de fechamento de cinco grandes iniciativas em sequência: dois FMEA críticos, enriquecimento estratégico da BoK Suite, geração do sistema de 8 agentes, e compliance LGPD. FMEA-008 (RPN 120): a função `orchestrate-content` recebia conteúdo do LLM e inseria diretamente em `content_library` sem qualquer validação — artigos truncados, posts LinkedIn de 3 palavras e threads de 1 tweet chegavam ao WordPress e às redes. A correção adiciona `validateContent()` com thresholds por tipo (article: 500, linkedin: 50, twitter_thread: 30) imediatamente após a geração de cada tipo, zerando `articleContent` na falha para bloquear o step WordPress, e emitindo erro estruturado via `addStep`. FMEA-011 (RPN 100): 47 migrations sem review gate — uma tabela nova sem RLS poderia vazar dados entre tenants. A correção é processual: checklist obrigatório Fase 4b no skill `/migration` com 5 itens (RLS, default-deny, PII, `/security-review`, sem secrets hardcoded) e entrada em `CLAUDE.md` como padrão de código não-negociável. Phase 2 BoK Enrichment adicionou a "voz estratégica" que o reverse-engineering não consegue capturar: Sovereign's Conviction (por que MCORCH existe), Business Philosophy (5 não-negociáveis + north-star M3 retention), Por Que Vencemos (4 moats compounding), Validação com Criadores (3 observações compostas PT-BR), Architectural Decisions (5 decisões com rationale de lock-in), e Quality Philosophy (por que 98% é o alvo correto no estágio atual). `/bok-agents-generator` foi invocado contra o BoK enriquecido e gerou `bok-agents-system--mcorch-constellation.md` (704 linhas): 8 agentes (BABOK/EABOK/DMBOK/BPM-CBOK/SWEBOK/CISSP-CBK/CXBOK/ProdBOK), cada um com 10 seções, adaptados ao contexto Creator Economy SaaS B2B2C AI-native, mais 3 camadas cross-agent. LGPD: `delete_account()` SECURITY DEFINER RPC com cascade DELETE em 9 tabelas em ordem de dependência retorna audit summary JSON; Edge Function `delete-account` chama o RPC + `auth.admin.deleteUser()` via service role, com log antes da deleção; `data-export` coleta 7 tabelas PII e retorna JSON estruturado com `Content-Disposition: attachment`; SettingsPage ganha card "Dados & Privacidade (LGPD)" com modal de confirmação gatekeado por digitação "DELETE". Phase Commercial desbloqueada.
> 3722:| `.claude/commands/migration.md` — FMEA-011 Fase 4b | ✅ Security Checklist obrigatório: RLS, default-deny, PII, /security-review, no hardcoded secrets |
> 3723:| `CLAUDE.md` — Code standards | ✅ Entrada FMEA-011: "Every new migration MUST pass /security-review before commit" |
> ```

## 🤖 Claude *(15:47:30)*


## 🤖 Claude *(15:47:53)*

Quadro completo, materialmente fechado. O HANDOFF.md (linha 16) é a peça final: o `/security-review` do `20260602140000` **foi** rodado, gerou um achado HIGH que foi refutado materialmente (overwrite cross-tenant é fail-closed pelo `PRIMARY KEY`), e *nessa mesma investigação* revelou este gap paralelo real (injeção id-novo) — **fechado na mesma sessão**, exatamente com a metodologia probe-first/`BEGIN…ROLLBACK` que reproduzi.

---

## Veredito: o gap já está fechado — nenhuma migration nova é necessária

O prompt descreve o gap como aberto citando `position('auth.uid'...) = 0`. Isso era o estado **ANTES** — capturado no instante em que o gap aflorou durante o `/security-review` do `20260602140000`. O fix foi aplicado e selado na **mesma sessão (2026-06-02)**, antes desta tarefa chegar até mim. Confirmei materialmente que tudo o que o prompt pede já existe. Criar uma `20260602160000` redundante seria um `CREATE OR REPLACE` no-op — lixo de manutenção, e fabricação de trabalho que a Lei 1 proíbe.

### Prova material (verificada NESTA sessão)

**1. Função deployada no banco vivo** (`pg_get_functiondef`, Management API):

| Função | `auth.uid` guard | errcode `42501` | `service_role` isento | `search_path` |
|--------|:---:|:---:|:---:|:---:|
| `trg_instead_of_meta_config` | ✅ | ✅ | ✅ | `""` |
| `trg_instead_of_social_accounts` | ✅ | ✅ | ✅ | `""` |

**2. Simulação de ataque comportamental** (set_config JWT spoof, tudo em `BEGIN…ROLLBACK`):

| Teste | Resultado |
|-------|-----------|
| Atacante injeta `social_accounts` com `user_id`=vítima + id novo | **PASS — 42501** `cannot write credentials for another user` |
| Atacante injeta `meta_config` com `user_id`=vítima + id novo | **PASS — 42501** |
| Self-insert legítimo (`user_id`=`auth.uid()`) — social | **PASS — permitido** |
| Insert service_role com `user_id` arbitrário (OAuth/cron) — social | **PASS — permitido** (isento) |
| Self-insert legítimo — meta | **PASS — permitido** |

**3. Zero resíduo pós-`ROLLBACK`:** `social_accounts` da vítima inalterada (`facebook,instagram,linkedin`, 3 linhas); `meta_config` em 0 linhas; nenhuma linha de teste (`tiktok/youtube/pinterest`) persistida. *(Detalhe relevante: a vítima não tem linha `meta_config` — o que torna o vetor de injeção realmente explorável antes do fix, não meramente teórico.)*

> Nota sobre a FK/segundo tenant que o prompt antecipa: não precisei de auth.users descartável. O `auth.uid()` do atacante vive só no claim JWT (nunca é inserido → sem FK), e o alvo `user_id` é a vítima real. O guard dispara no mismatch `auth.uid()` **antes** de qualquer INSERT/FK.

### Governança (já selada em v6.20.2)

- **Migration** `20260602150000_meta_social_instead_of_tenant_guard.sql`: commitada em `87c926f` (151 inserções), working-tree-idêntica, em `main` sincronizado com `origin/main`. Guard nos branches INSERT **e** UPDATE de ambas as funções, corpos reproduzidos verbatim, `search_path=''`.
- **`/security-review`**: rodado durante a seal (HANDOFF.md:16). Sem diff pendente hoje (working tree limpa) → não há o que re-revisar.
- **SOP** `docs/processes/credential-disconnect-clear.md`: já atualizado (linhas 110-126), com a prova antes/depois.

---

### Um débito **distinto** e ainda ABERTO que encontrei ao lado (heads-up, fora do escopo desta tarefa)

HANDOFF.md:69 registra: desconectar Meta/social (`INSTEAD OF DELETE`) apaga só a linha base — **o segredo Vault fica órfão** (plaintext retido). É o paralelo do que `disconnect_wordpress()` resolveu pro WordPress; precisa de RPC dedicada (nula linha + revoga segredo) + `/security-review`. É um gap LGPD/retenção **diferente** do guard de tenant — já está no ledger de Pending, então não abri task automática.

Quer que eu (a) rode o `/security-review` apontado para o commit `87c926f` como redundância de cinto-e-suspensório, ou (b) ataque o débito do segredo órfão Meta/social (RPC `disconnect_meta`/`disconnect_social` espelhando `disconnect_wordpress`)? Ou encerro aqui, já que o gap solicitado está materialmente fechado.

---

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-01 - agent-af11d6fa76341891b]]
> * **Próxima Sessão**: [[2026-06-02 - Fix WordPress credentials save and disconnect in SocialAccountsPage]]
%% --- TIMELINE END --- %%

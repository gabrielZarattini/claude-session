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

## 👤 User *(16:34:18)*

faça os dois /security-review apontado para o commit 87c926f como redundância de cinto-e-suspensório, e também (b) ataque o débito do segredo órfão Meta/social (RPC disconnect_meta/disconnect_social espelhando disconnect_wordpress)

## 🤖 Claude *(16:34:54)*


## 🤖 Claude *(16:34:59)*

O Sovereign autorizou os dois. Vou declarar o ORO e atacar em ordem: (A) `/security-review` redundante no `87c926f`, depois (B) construir as RPCs `disconnect_meta`/`disconnect_social` — que por sua vez exigem seu próprio `/security-review` antes do commit.

**ORO triplet desta task (Parte B — build substantivo):**
- **Operator:** MCORCH Master Execution Agent (eu)
- **Reviewer:** Sovereign (Gabriel) + `/security-review` gate obrigatório (camada de credenciais)
- **Owner:** Sovereign — blast radius = retenção de segredo plaintext órfão (LGPD) + integridade do disconnect per-user; risco se a RPC vazar/errar tenant

Primeiro, vou entender o terreno: a interface do `/security-review`, o padrão `disconnect_wordpress` a espelhar, e a convenção de nomes dos segredos Vault para meta/social. Leituras independentes em paralelo:

## 🤖 Claude *(16:35:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== locate security-review skill/command def ===\"; find / -path /proc -prune -o \\( -name \"security-review*.md\" -o -path \"*security-review*SKILL.md\" \\) -print 2>/dev/null | head; echo \"\"; echo \"=== .claude/commands ===\"; ls -la .claude/commands/ 2>/dev/null | grep -i secur || echo \"(no security-review in .claude/commands)\"",
  "description": "Locate security-review skill definition"
}
```

## 🤖 Claude *(16:35:02)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260602120000_wordpress_disconnect_rpc.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: WordPress credential disconnect — privileged clear + Vault revocation
> 2	-- ─────────────────────────────────────────────────────────────────────────────
> 3	-- Why this exists:
> 4	--   Since 20260601000000_credential_encryption + 20260601000600_secure_definer_views,
> 5	--   `user_api_keys` is a masked SECURITY-DEFINER VIEW over `user_api_keys_table`.
> 6	--   Its INSTEAD OF UPDATE/INSERT trigger writes wp_app_password through
> 7	--   `COALESCE(NULLIF(NEW.wp_app_password, '••••••••••••'), base.wp_app_password)`, which
> 8	--   PRESERVES the existing value when the client sends NULL. That COALESCE-guard is
> 9	--   load-bearing (it lets a partial save touch only WP fields without wiping the AI
> 10	--   keys), so it cannot be relaxed. Result: a client cannot clear WP credentials by
> 11	--   writing NULLs, and SELECT on the base table is revoked from `authenticated`.
> 12	--
> 13	--   This RPC is the privileged clear path. It runs as the function owner (postgres,
> 14	--   which bypasses RLS since force_rls=false on user_api_keys_table and holds DELETE on
> 15	--   vault.secrets), is scoped strictly to auth.uid() (no spoofable parameter), nulls the
> 16	--   three WordPress columns directly on the base table, and revokes the orphaned
> 17	--   plaintext secret from the Vault (true credential deletion — LGPD).
> 18	--
> 19	-- BoK SSOT: docs/bok/meta-api/06-data-model.md (encryption at-rest) ·
> 20	--           CLAUDE.md API Tenancy Model (per-user, auth.uid()-scoped) ·
> 21	--           docs/processes/credential-disconnect-clear.md (Law 2 SOP)
> 22	
> 23	CREATE OR REPLACE FUNCTION public.disconnect_wordpress()
> 24	RETURNS void
> 25	LANGUAGE plpgsql
> 26	SECURITY DEFINER
> 27	SET search_path = ''
> 28	AS $$
> 29	DECLARE
> 30	  v_uid uuid := auth.uid();
> 31	  v_pwd_ref text;
> 32	BEGIN
> 33	  -- Fail closed: never run for an unauthenticated caller.
> 34	  IF v_uid IS NULL THEN
> 35	    RAISE EXCEPTION 'authentication required' USING errcode = '28000';
> 36	  END IF;
> 37	
> 38	  -- Capture the Vault secret reference (a UUID) from the CALLER's own row only,
> 39	  -- before clearing it — this is what scopes the Vault deletion to the caller.
> 40	  SELECT wp_app_password INTO v_pwd_ref
> 41	  FROM public.user_api_keys_table
> 42	  WHERE user_id = v_uid;
> 43	
> 44	  -- Clear the three WordPress columns on the base table. Bypasses the masked view's
> 45	  -- COALESCE-NULLIF guard that would otherwise preserve the password on a NULL write.
> 46	  UPDATE public.user_api_keys_table
> 47	  SET wp_site_url     = NULL,
> 48	      wp_username     = NULL,
> 49	      wp_app_password = NULL,
> 50	      updated_at      = now()
> 51	  WHERE user_id = v_uid;
> 52	
> 53	  -- True revocation: delete the orphaned plaintext secret from the Vault. Scoped BOTH to the
> 54	  -- UUID read from the caller's row AND to the deterministic secret name the encryption
> 55	  -- trigger assigns ('user_api_keys_wp_app_password_<uid>'). The name binding is the real
> 56	  -- tenant guard: even though wp_app_password is client-writable (a user could plant an
> 57	  -- arbitrary UUID via the masked view), a planted pointer to another tenant's secret would
> 58	  -- fail the name match and be ignored — so this can NEVER delete a secret the caller does
> 59	  -- not own. (It also frees the name for a clean future reconnect.)
> 60	  IF v_pwd_ref ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 61	    DELETE FROM vault.secrets
> 62	    WHERE id = v_pwd_ref::uuid
> 63	      AND name = 'user_api_keys_wp_app_password_' || v_uid::text;
> 64	  END IF;
> 65	END;
> 66	$$;
> 67	
> 68	-- Least privilege: callable only by authenticated users (each clears only their own row).
> 69	REVOKE ALL ON FUNCTION public.disconnect_wordpress() FROM PUBLIC;
> 70	REVOKE ALL ON FUNCTION public.disconnect_wordpress() FROM anon;
> 71	GRANT EXECUTE ON FUNCTION public.disconnect_wordpress() TO authenticated;
> 72	
> 73	COMMENT ON FUNCTION public.disconnect_wordpress() IS
> 74	  'Clears the caller''s WordPress credentials (wp_site_url/wp_username/wp_app_password) on '
> 75	  'user_api_keys_table and revokes the associated Vault secret. SECURITY DEFINER, scoped to '
> 76	  'auth.uid(); the masked view cannot clear these via NULL writes (COALESCE-NULLIF guard).';
> 77	
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === locate security-review skill/command def ===
> 
> === .claude/commands ===
> (no security-review in .claude/commands)
> ```

## 🤖 Claude *(16:35:33)*


## 🤖 Claude *(16:35:36)*

O padrão `disconnect_wordpress` está cristalino. O detalhe **load-bearing** é o nome determinístico do segredo Vault — é ele o guard de tenant real. Preciso cravar os nomes exatos que os triggers de encriptação atribuem para `meta_config.long_lived_token` e `social_accounts.access_token`/`refresh_token`. Vou extrair isso do banco vivo (fonte da verdade) e das migrations de encriptação:

## 🤖 Claude *(16:35:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== secret-name patterns referenced in encryption migrations ===\"\ngrep -rnoE \"'(user_api_keys|meta_config|social_accounts)_[a-z_]*'?\\s*\\|\\|[^;]*\" supabase/migrations/20260601000000_credential_encryption.sql supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql 2>/dev/null | head -40\necho \"\"\necho \"=== grep encrypt trigger function names + create_secret/vault_upsert calls ===\"\ngrep -rnE \"CREATE OR REPLACE FUNCTION.*encrypt|vault_upsert_secret|create_secret|_token_|_password_|long_lived_token|access_token|refresh_token\" supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql | head -60",
  "description": "Extract Vault secret naming convention from encryption migrations"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === secret-name patterns referenced in encryption migrations ===
> supabase/migrations/20260601000000_credential_encryption.sql:32:'meta_config_long_lived_token_' || NEW.id::text, 'Meta config long-lived token')
> supabase/migrations/20260601000000_credential_encryption.sql:41:'meta_config_pages_' || NEW.id::text, 'Meta config pages list')
> supabase/migrations/20260601000000_credential_encryption.sql:70:'social_accounts_access_token_' || NEW.id::text, 'Social account access token')
> supabase/migrations/20260601000000_credential_encryption.sql:79:'social_accounts_refresh_token_' || NEW.id::text, 'Social account refresh token')
> supabase/migrations/20260601000000_credential_encryption.sql:104:'user_api_keys_groq_api_key_' || NEW.user_id::text, 'Groq API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:114:'user_api_keys_openrouter_api_key_' || NEW.user_id::text, 'OpenRouter API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:124:'user_api_keys_openai_api_key_' || NEW.user_id::text, 'OpenAI API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:134:'user_api_keys_elevenlabs_api_key_' || NEW.user_id::text, 'ElevenLabs API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:144:'user_api_keys_google_api_key_' || NEW.user_id::text, 'Google API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:154:'user_api_keys_nanobana_api_key_' || NEW.user_id::text, 'Nanobana API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:164:'user_api_keys_seedance_api_key_' || NEW.user_id::text, 'Seedance API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:174:'user_api_keys_wp_app_password_' || NEW.user_id::text, 'WordPress App Password')
> supabase/migrations/20260601000000_credential_encryption.sql:184:'user_api_keys_replicate_api_key_' || NEW.user_id::text, 'Replicate API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:194:'user_api_keys_higgsfield_api_key_' || NEW.user_id::text, 'Higgsfield API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:204:'user_api_keys_higgsfield_api_key_secret_' || NEW.user_id::text, 'Higgsfield API Key Secret')
> supabase/migrations/20260601000000_credential_encryption.sql:234:'meta_config_long_lived_token_' || r.id::text, 'Meta config long-lived token')
> supabase/migrations/20260601000000_credential_encryption.sql:238:'meta_config_pages_' || r.id::text, 'Meta config pages list')
> supabase/migrations/20260601000000_credential_encryption.sql:264:'social_accounts_access_token_' || r.id::text, 'Social account access token')
> supabase/migrations/20260601000000_credential_encryption.sql:268:'social_accounts_refresh_token_' || r.id::text, 'Social account refresh token')
> supabase/migrations/20260601000000_credential_encryption.sql:292:'user_api_keys_groq_api_key_' || r.user_id::text, 'Groq API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:295:'user_api_keys_openrouter_api_key_' || r.user_id::text, 'OpenRouter API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:298:'user_api_keys_openai_api_key_' || r.user_id::text, 'OpenAI API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:301:'user_api_keys_elevenlabs_api_key_' || r.user_id::text, 'ElevenLabs API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:304:'user_api_keys_google_api_key_' || r.user_id::text, 'Google API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:307:'user_api_keys_nanobana_api_key_' || r.user_id::text, 'Nanobana API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:310:'user_api_keys_seedance_api_key_' || r.user_id::text, 'Seedance API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:313:'user_api_keys_wp_app_password_' || r.user_id::text, 'WordPress App Password')
> supabase/migrations/20260601000000_credential_encryption.sql:316:'user_api_keys_replicate_api_key_' || r.user_id::text, 'Replicate API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:319:'user_api_keys_higgsfield_api_key_' || r.user_id::text, 'Higgsfield API Key')
> supabase/migrations/20260601000000_credential_encryption.sql:322:'user_api_keys_higgsfield_api_key_secret_' || r.user_id::text, 'Higgsfield API Key Secret')
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:116:'user_api_keys_groq_api_key_' || NEW.user_id::text, 'Groq API Key')
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:126:'user_api_keys_openrouter_api_key_' || NEW.user_id::text, 'OpenRouter API Key')
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:136:'user_api_keys_openai_api_key_' || NEW.user_id::text, 'OpenAI API Key')
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:146:'user_api_keys_elevenlabs_api_key_' || NEW.user_id::text, 'ElevenLabs API Key')
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:156:'user_api_keys_google_api_key_' || NEW.user_id::text, 'Google API Key')
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:166:'user_api_keys_nanobana_api_key_' || NEW.user_id::text, 'Nanobana API Key')
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:176:'user_api_keys_seedance_api_key_' || NEW.user_id::text, 'Seedance API Key')
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:186:'user_api_keys_wp_app_password_' || NEW.user_id::text, 'WordPress App Password')
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:196:'user_api_keys_replicate_api_key_' || NEW.user_id::text, 'Replicate API Key')
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:206:'user_api_keys_higgsfield_api_key_' || NEW.user_id::text, 'Higgsfield API Key')
> 
> === grep encrypt trigger function names + create_secret/vault_upsert calls ===
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:1:-- Migration: idempotent credential encryption — vault_upsert_secret() eliminates the
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:7:-- vault.create_secret(value, '<deterministic-name>') UNCONDITIONALLY whenever a secret column
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:8:-- changes value. vault.create_secret does a plain `INSERT INTO vault.secrets` with NO ON CONFLICT,
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:22:-- Fix: a single idempotent helper public.vault_upsert_secret(value, name, desc) that resolves an
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:25:-- creates it. The vault.create_secret call-sites in each of the three encryption triggers are
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:32:--   * vault_upsert_secret is SECURITY DEFINER with `SET search_path = ''` and every object schema-
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:41:--     SECURITY DEFINER vault.create_secret/update_secret primitives (postgres has EXECUTE, not direct
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:50:CREATE OR REPLACE FUNCTION public.vault_upsert_secret(
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:74:  RETURN vault.create_secret(p_value, p_name, p_desc);
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:78:  -- create_secret. Re-resolve and update in place rather than surfacing 23505 to the caller.
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:89:COMMENT ON FUNCTION public.vault_upsert_secret(text, text, text) IS
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:95:REVOKE ALL ON FUNCTION public.vault_upsert_secret(text, text, text) FROM PUBLIC;
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:96:REVOKE ALL ON FUNCTION public.vault_upsert_secret(text, text, text) FROM anon, authenticated;
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:99:-- 2. user_api_keys encryption trigger — swap vault.create_secret → public.vault_upsert_secret
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:102:CREATE OR REPLACE FUNCTION public.trg_encrypt_user_api_keys()
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:116:      v_id := public.vault_upsert_secret(NEW.groq_api_key, 'user_api_keys_groq_api_key_' || NEW.user_id::text, 'Groq API Key');
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:126:      v_id := public.vault_upsert_secret(NEW.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || NEW.user_id::text, 'OpenRouter API Key');
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:136:      v_id := public.vault_upsert_secret(NEW.openai_api_key, 'user_api_keys_openai_api_key_' || NEW.user_id::text, 'OpenAI API Key');
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:146:      v_id := public.vault_upsert_secret(NEW.elevenlabs_api_key, 'user_api_keys_elevenlabs_api_key_' || NEW.user_id::text, 'ElevenLabs API Key');
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:156:      v_id := public.vault_upsert_secret(NEW.google_api_key, 'user_api_keys_google_api_key_' || NEW.user_id::text, 'Google API Key');
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:166:      v_id := public.vault_upsert_secret(NEW.nanobana_api_key, 'user_api_keys_nanobana_api_key_' || NEW.user_id::text, 'Nanobana API Key');
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:176:      v_id := public.vault_upsert_secret(NEW.seedance_api_key, 'user_api_keys_seedance_api_key_' || NEW.user_id::text, 'Seedance API Key');
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:186:      v_id := public.vault_upsert_secret(NEW.wp_app_password, 'user_api_keys_wp_app_password_' || NEW.user_id::text, 'WordPress App Password');
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:196:      v_id := public.vault_upsert_secret(NEW.replicate_api_key, 'user_api_keys_replicate_api_key_' || NEW.user_id::text, 'Replicate API Key');
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:206:      v_id := public.vault_upsert_secret(NEW.higgsfield_api_key, 'user_api_keys_higgsfield_api_key_' || NEW.user_id::text, 'Higgsfield API Key');
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:216:      v_id := public.vault_upsert_secret(NEW.higgsfield_api_key_secret, 'user_api_keys_higgsfield_api_key_secret_' || NEW.user_id::text, 'Higgsfield API Key Secret');
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:226:      v_id := public.vault_upsert_secret(NEW.apify_token, 'user_api_keys_apify_token_' || NEW.user_id::text, 'Apify Token');
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:236:-- 3. meta_config encryption trigger — swap vault.create_secret → public.vault_upsert_secret
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:238:CREATE OR REPLACE FUNCTION public.trg_encrypt_meta_config()
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:245:  v_token_id UUID;
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:252:  IF NEW.long_lived_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.long_lived_token IS DISTINCT FROM OLD.long_lived_token) THEN
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:253:    IF NEW.long_lived_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:256:      v_token_id := public.vault_upsert_secret(NEW.long_lived_token, 'meta_config_long_lived_token_' || NEW.id::text, 'Meta config long-lived token');
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:257:      NEW.long_lived_token = v_token_id::text;
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:265:      v_pages_id := public.vault_upsert_secret(NEW.pages::text, 'meta_config_pages_' || NEW.id::text, 'Meta config pages list');
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:275:-- 4. social_accounts encryption trigger — swap vault.create_secret → public.vault_upsert_secret
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:277:CREATE OR REPLACE FUNCTION public.trg_encrypt_social_accounts()
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:284:  v_access_token_id UUID;
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:285:  v_refresh_token_id UUID;
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:291:  IF NEW.access_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.access_token IS DISTINCT FROM OLD.access_token) THEN
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:292:    IF NEW.access_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:295:      v_access_token_id := public.vault_upsert_secret(NEW.access_token, 'social_accounts_access_token_' || NEW.id::text, 'Social account access token');
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:296:      NEW.access_token = v_access_token_id::text;
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:300:  IF NEW.refresh_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.refresh_token IS DISTINCT FROM OLD.refresh_token) THEN
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:301:    IF NEW.refresh_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:304:      v_refresh_token_id := public.vault_upsert_secret(NEW.refresh_token, 'social_accounts_refresh_token_' || NEW.id::text, 'Social account refresh token');
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:305:      NEW.refresh_token = v_refresh_token_id::text;
> ```

## 🤖 Claude *(16:36:19)*


## 🤖 Claude *(16:36:23)*

**Detalhe crítico (e divergente do WordPress):** os segredos de meta/social são nomeados pela **`id` da linha**, não pelo `user_id`:

- `meta_config_long_lived_token_<row.id>` · `meta_config_pages_<row.id>`
- `social_accounts_access_token_<row.id>` · `social_accounts_refresh_token_<row.id>`

Isso muda a lógica do guard de tenant: no WP o nome embute o `uid` (auto-isolante); aqui o nome embute o `id` da linha, então o isolamento tem que vir de **ler os `id`/refs só das linhas do caller** (`WHERE user_id = auth.uid()`). Preciso ver o corpo exato dos triggers de encriptação (como cada coluna é gravada de volta) e a UX real de disconnect no frontend. Mais a confirmação material dos nomes no Vault vivo:

## 🤖 Claude *(16:36:26)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql",
  "offset": 236,
  "limit": 85
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 236	-- 3. meta_config encryption trigger — swap vault.create_secret → public.vault_upsert_secret
> 237	-- ─────────────────────────────────────────────────────────────────────────────
> 238	CREATE OR REPLACE FUNCTION public.trg_encrypt_meta_config()
> 239	RETURNS TRIGGER
> 240	LANGUAGE plpgsql
> 241	SECURITY DEFINER
> 242	SET search_path = ''
> 243	AS $$
> 244	DECLARE
> 245	  v_token_id UUID;
> 246	  v_pages_id UUID;
> 247	BEGIN
> 248	  IF NEW.id IS NULL THEN
> 249	    NEW.id := gen_random_uuid();
> 250	  END IF;
> 251	
> 252	  IF NEW.long_lived_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.long_lived_token IS DISTINCT FROM OLD.long_lived_token) THEN
> 253	    IF NEW.long_lived_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 254	      -- keep existing UUID reference
> 255	    ELSE
> 256	      v_token_id := public.vault_upsert_secret(NEW.long_lived_token, 'meta_config_long_lived_token_' || NEW.id::text, 'Meta config long-lived token');
> 257	      NEW.long_lived_token = v_token_id::text;
> 258	    END IF;
> 259	  END IF;
> 260	
> 261	  IF NEW.pages IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.pages IS DISTINCT FROM OLD.pages) THEN
> 262	    IF NEW.pages::text ~ '^"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"$' THEN
> 263	      -- keep existing UUID JSON reference
> 264	    ELSE
> 265	      v_pages_id := public.vault_upsert_secret(NEW.pages::text, 'meta_config_pages_' || NEW.id::text, 'Meta config pages list');
> 266	      NEW.pages = to_jsonb(v_pages_id::text);
> 267	    END IF;
> 268	  END IF;
> 269	
> 270	  RETURN NEW;
> 271	END;
> 272	$$;
> 273	
> 274	-- ─────────────────────────────────────────────────────────────────────────────
> 275	-- 4. social_accounts encryption trigger — swap vault.create_secret → public.vault_upsert_secret
> 276	-- ─────────────────────────────────────────────────────────────────────────────
> 277	CREATE OR REPLACE FUNCTION public.trg_encrypt_social_accounts()
> 278	RETURNS TRIGGER
> 279	LANGUAGE plpgsql
> 280	SECURITY DEFINER
> 281	SET search_path = ''
> 282	AS $$
> 283	DECLARE
> 284	  v_access_token_id UUID;
> 285	  v_refresh_token_id UUID;
> 286	BEGIN
> 287	  IF NEW.id IS NULL THEN
> 288	    NEW.id := gen_random_uuid();
> 289	  END IF;
> 290	
> 291	  IF NEW.access_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.access_token IS DISTINCT FROM OLD.access_token) THEN
> 292	    IF NEW.access_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 293	      -- keep existing UUID reference
> 294	    ELSE
> 295	      v_access_token_id := public.vault_upsert_secret(NEW.access_token, 'social_accounts_access_token_' || NEW.id::text, 'Social account access token');
> 296	      NEW.access_token = v_access_token_id::text;
> 297	    END IF;
> 298	  END IF;
> 299	
> 300	  IF NEW.refresh_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.refresh_token IS DISTINCT FROM OLD.refresh_token) THEN
> 301	    IF NEW.refresh_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 302	      -- keep existing UUID reference
> 303	    ELSE
> 304	      v_refresh_token_id := public.vault_upsert_secret(NEW.refresh_token, 'social_accounts_refresh_token_' || NEW.id::text, 'Social account refresh token');
> 305	      NEW.refresh_token = v_refresh_token_id::text;
> 306	    END IF;
> 307	  END IF;
> 308	
> 309	  RETURN NEW;
> 310	END;
> 311	$$;
> 312	
> ```

## 🤖 Claude *(16:37:16)*


## 🤖 Claude *(16:37:20)*

Triggers totalmente claros:
- **meta_config**: `long_lived_token` (text→UUID ref) nome `meta_config_long_lived_token_<id>`; `pages` (jsonb→`to_jsonb(uuid::text)`) nome `meta_config_pages_<id>`.
- **social_accounts**: `access_token`, `refresh_token` (text→UUID refs) nomes `social_accounts_{access,refresh}_token_<id>`.

A propriedade de segurança se mantém mesmo com nome por `id` da linha: o `id` no nome vem da linha **do próprio caller** (`WHERE user_id = auth.uid()`), então um atacante que plante um UUID forjado na própria coluna não consegue casar o `name` do segredo da vítima. Igual ao WP.

Agora a UX real de disconnect no frontend (define se `disconnect_social` é por-plataforma ou tudo) + confirmação material no Vault vivo:

## 🤖 Claude *(16:37:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== social hooks/pages ===\"; ls src/hooks/ | grep -iE \"social|meta\" ; echo \"---\"; grep -rliE \"social_accounts|disconnect\" src/hooks/ src/pages/ src/components/ 2>/dev/null | grep -iE \"social|meta\" | head\necho \"\"; echo \"=== meta_config UNIQUE + social UNIQUE constraints ===\"; grep -rnE \"UNIQUE|unique|primary key|PRIMARY KEY\" supabase/migrations/20260530210000_meta_api_foundation.sql 2>/dev/null | head; echo \"--- social table def ---\"; grep -rnE \"social_accounts_table|UNIQUE|platform\" supabase/migrations/20260601000000_credential_encryption.sql | grep -iE \"unique|create table\" | head",
  "description": "Locate social/meta frontend disconnect + table constraints"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === social hooks/pages ===
> useMetaConfig.ts
> useSocialAccounts.ts
> ---
> src/hooks/useMetaConfig.ts
> src/hooks/useSocialAccounts.ts
> src/pages/SocialAccountsPage.tsx
> src/components/settings/MetaConfigCard.tsx
> 
> === meta_config UNIQUE + social UNIQUE constraints ===
> supabase/migrations/20260530210000_meta_api_foundation.sql:25:-- 1. meta_config — per-user Meta credentials & linked accounts (UNIQUE per user)
> supabase/migrations/20260530210000_meta_api_foundation.sql:28:    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> supabase/migrations/20260530210000_meta_api_foundation.sql:42:    CONSTRAINT unique_user_meta UNIQUE (user_id)
> supabase/migrations/20260530210000_meta_api_foundation.sql:64:    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> --- social table def ---
> ```

## 🤖 Claude *(16:37:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "TOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\necho \"=== live vault secret names for victim's meta/social rows (CONFIRM naming) ===\"\nQUERY='SELECT s.name, (s.id IS NOT NULL) AS exists FROM vault.secrets s WHERE s.name LIKE '\"'\"'meta_config_%'\"'\"' OR s.name LIKE '\"'\"'social_accounts_%'\"'\"' ORDER BY s.name;'\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"{\\\"query\\\": $(printf '%s' \"$QUERY\" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}\" | python3 -m json.tool\necho \"\"; echo \"=== victim social rows: are access_token columns UUID refs? + their ids ===\"\nQUERY2='SELECT platform, id, (access_token ~ '\"'\"'^[0-9a-f-]{36}$'\"'\"') AS token_is_uuid_ref, access_token FROM public.social_accounts_table WHERE user_id = '\"'\"'ada39fae-67e1-4e53-af1c-5a18e1c108e8'\"'\"' ORDER BY platform;'\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"{\\\"query\\\": $(printf '%s' \"$QUERY2\" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}\" | python3 -m json.tool",
  "description": "Confirm live vault secret naming and column ref format"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === live vault secret names for victim's meta/social rows (CONFIRM naming) ===
> [
>     {
>         "name": "meta_config_long_lived_token_02bb35bb-504f-4c72-8d1f-8056abd13973",
>         "exists": true
>     },
>     {
>         "name": "meta_config_long_lived_token_2e777f9e-afc6-4749-8f57-2630f8c00eb5",
>         "exists": true
>     },
>     {
>         "name": "meta_config_long_lived_token_80ed0fba-0682-48bc-a634-b9874b226a9b",
>         "exists": true
>     },
>     {
>         "name": "meta_config_long_lived_token_d1230f20-7bf4-4d15-8175-93a0f290cfdd",
>         "exists": true
>     },
>     {
>         "name": "meta_config_long_lived_token_e7339a64-7a12-4dea-890a-69f3bca2d3b9",
>         "exists": true
>     },
>     {
>         "name": "meta_config_long_lived_token_ef1d23dc-1c7c-4e76-929e-e8787678918f",
>         "exists": true
>     },
>     {
>         "name": "meta_config_pages_02bb35bb-504f-4c72-8d1f-8056abd13973",
>         "exists": true
>     },
>     {
>         "name": "meta_config_pages_2e777f9e-afc6-4749-8f57-2630f8c00eb5",
>         "exists": true
>     },
>     {
>         "name": "meta_config_pages_80ed0fba-0682-48bc-a634-b9874b226a9b",
>         "exists": true
>     },
>     {
>         "name": "meta_config_pages_d1230f20-7bf4-4d15-8175-93a0f290cfdd",
>         "exists": true
>     },
>     {
>         "name": "meta_config_pages_e7339a64-7a12-4dea-890a-69f3bca2d3b9",
>         "exists": true
>     },
>     {
>         "name": "meta_config_pages_ef1d23dc-1c7c-4e76-929e-e8787678918f",
>         "exists": true
>     },
>     {
>         "name": "social_accounts_access_token_39ce0ebb-3579-481a-93ce-8a20759cd22e",
>         "exists": true
>     },
>     {
>         "name": "social_accounts_access_token_6910dd24-ca3e-473f-ba70-7ab488aef9ea",
>         "exists": true
>     },
>     {
>         "name": "social_accounts_access_token_931386ca-3c73-4a5f-b43b-517093004598",
>         "exists": true
>     }
> ]
> 
> === victim social rows: are access_token columns UUID refs? + their ids ===
> [
>     {
>         "platform": "linkedin",
>         "id": "931386ca-3c73-4a5f-b43b-517093004598",
>         "token_is_uuid_ref": true,
>         "access_token": "f15c4de1-1e34-49e2-9f46-1031d5e9e4f9"
>     },
>     {
>         "platform": "instagram",
>         "id": "39ce0ebb-3579-481a-93ce-8a20759cd22e",
>         "token_is_uuid_ref": true,
>         "access_token": "bc243226-ad1e-4a1e-a831-52f088769e21"
>     },
>     {
>         "platform": "facebook",
>         "id": "6910dd24-ca3e-473f-ba70-7ab488aef9ea",
>         "token_is_uuid_ref": true,
>         "access_token": "95c11eaa-3d20-4d85-9654-246c429b14f2"
>     }
> ]
> ```

## 🤖 Claude *(16:38:19)*


## 🤖 Claude *(16:38:23)*

**Material — e revelador:** existem **6 segredos `meta_config_long_lived_token_*` + 6 `meta_config_pages_*`** no Vault, mas a vítima tem **0 linhas** em `meta_config_table`. Ou seja: **12 segredos Meta já estão órfãos AGORA** — sobras de ~6 ciclos de conectar/desconectar Meta, cada um deixando 2 segredos plaintext retidos. É a prova viva do débito (exposição LGPD ativa). Os 3 segredos sociais (linkedin/instagram/facebook), em contraste, têm linha viva → não são órfãos.

Constraints confirmados: `meta_config` tem `UNIQUE(user_id)` (1 linha/user → `disconnect_meta()` sem param); social é multi-linha por plataforma (`disconnect_social(platform)`). Vou ler os hooks do frontend para casar a interface da RPC com a UX real:

## 🤖 Claude *(16:38:24)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useMetaConfig.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
> 2	import type { SupabaseClient } from '@supabase/supabase-js';
> 3	import { supabase } from '@/integrations/supabase/client';
> 4	import { useAuth } from '@/hooks/useAuth';
> 5	import {
> 6	  META_SAFE_COLUMNS,
> 7	  type MetaConfigStatus,
> 8	  type MetaConfigInput,
> 9	  isMetaConnected,
> 10	  metaNeedsReauth,
> 11	  metaTokenExpiringSoon,
> 12	} from '@/lib/meta';
> 13	
> 14	/**
> 15	 * Per-user Meta credentials (meta_config). BYOK model — mirrors useAffiliateConfig.
> 16	 * Reads only safe columns (long_lived_token + pages are column-REVOKE'd server-side).
> 17	 */
> 18	export function useMetaConfig() {
> 19	  const { user } = useAuth();
> 20	  const queryClient = useQueryClient();
> 21	  // meta_config is not in the generated Database types yet (added by migration 20260530210000);
> 22	  // use an untyped client view for it (lint-clean, no explicit `any`).
> 23	  const db = supabase as unknown as SupabaseClient;
> 24	
> 25	  const { data: status, isLoading } = useQuery({
> 26	    queryKey: ['meta_config', user?.id],
> 27	    queryFn: async () => {
> 28	      const { data, error } = await db
> 29	        .from('meta_config')
> 30	        .select(META_SAFE_COLUMNS)
> 31	        .eq('user_id', user!.id)
> 32	        .maybeSingle();
> 33	      if (error) throw error;
> 34	      return data as MetaConfigStatus | null;
> 35	    },
> 36	    enabled: !!user?.id,
> 37	  });
> 38	
> 39	  const upsertConfig = useMutation({
> 40	    mutationFn: async (values: MetaConfigInput) => {
> 41	      const pages =
> 42	        values.page_id && values.page_access_token
> 43	          ? [{ page_id: values.page_id, name: values.page_name ?? '', access_token: values.page_access_token }]
> 44	          : undefined;
> 45	
> 46	      // Re-pasting a token always clears the reauth flag (PROC self-healing recovery).
> 47	      const writable: Record<string, unknown> = {
> 48	        long_lived_token: values.long_lived_token,
> 49	        instagram_business_account_id: values.instagram_business_account_id ?? null,
> 50	        token_expires_at: values.token_expires_at ?? null,
> 51	        requires_reauth: false,
> 52	      };
> 53	      if (pages) writable.pages = pages;
> 54	
> 55	      if (status?.id) {
> 56	        const { error } = await db
> 57	          .from('meta_config')
> 58	          .update(writable)
> 59	          .eq('id', status.id);
> 60	        if (error) throw error;
> 61	      } else {
> 62	        const { error } = await db
> 63	          .from('meta_config')
> 64	          .insert({ user_id: user!.id, ...writable });
> 65	        if (error) throw error;
> 66	      }
> 67	    },
> 68	    onSuccess: () => {
> 69	      queryClient.invalidateQueries({ queryKey: ['meta_config', user?.id] });
> 70	    },
> 71	  });
> 72	
> 73	  const disconnect = useMutation({
> 74	    mutationFn: async () => {
> 75	      if (!status?.id) return;
> 76	      const { error } = await db.from('meta_config').delete().eq('id', status.id);
> 77	      if (error) throw error;
> 78	    },
> 79	    onSuccess: () => {
> 80	      queryClient.invalidateQueries({ queryKey: ['meta_config', user?.id] });
> 81	    },
> 82	  });
> 83	
> 84	  return {
> 85	    status: status ?? null,
> 86	    isLoading,
> 87	    upsertConfig,
> 88	    disconnect,
> 89	    connected: isMetaConnected(status),
> 90	    needsReauth: metaNeedsReauth(status),
> 91	    expiringSoon: metaTokenExpiringSoon(status),
> 92	  };
> 93	}
> 94	
> ```

## 🤖 Claude *(16:38:29)*


## 🤖 Claude *(16:38:29)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useSocialAccounts.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
> 2	import { supabase } from '@/integrations/supabase/client';
> 3	import { useAuth } from '@/hooks/useAuth';
> 4	import { toast } from 'sonner';
> 5	import type { Tables } from '@/integrations/supabase/types';
> 6	import type { Database } from '@/integrations/supabase/types';
> 7	
> 8	type SocialAccount = Tables<'social_accounts'>;
> 9	type SocialPlatform = Database['public']['Enums']['social_platform'];
> 10	
> 11	export const SUPPORTED_PLATFORMS: { id: SocialPlatform; name: string; icon: string; color: string }[] = [
> 12	  { id: 'linkedin', name: 'LinkedIn', icon: '💼', color: 'bg-blue-600' },
> 13	  { id: 'instagram', name: 'Instagram', icon: '📸', color: 'bg-gradient-to-r from-purple-500 to-pink-500' },
> 14	  { id: 'facebook', name: 'Facebook', icon: '👤', color: 'bg-blue-500' },
> 15	  { id: 'twitter', name: 'Twitter / X', icon: '𝕏', color: 'bg-zinc-800' },
> 16	  { id: 'tiktok', name: 'TikTok', icon: '🎵', color: 'bg-zinc-900' },
> 17	  { id: 'youtube', name: 'YouTube', icon: '▶️', color: 'bg-red-600' },
> 18	  { id: 'pinterest', name: 'Pinterest', icon: '📌', color: 'bg-red-500' },
> 19	];
> 20	
> 21	export function useSocialAccounts() {
> 22	  const { user } = useAuth();
> 23	  const queryClient = useQueryClient();
> 24	
> 25	  const accountsQuery = useQuery({
> 26	    queryKey: ['social_accounts', user?.id],
> 27	    queryFn: async () => {
> 28	      const { data, error } = await supabase
> 29	        .from('social_accounts')
> 30	        .select('id, user_id, platform, platform_user_id, platform_username, is_active, token_expires_at, scopes, metadata, created_at, updated_at')
> 31	        .order('created_at', { ascending: false });
> 32	      if (error) throw error;
> 33	      return data as SocialAccount[];
> 34	    },
> 35	    enabled: !!user,
> 36	  });
> 37	
> 38	  const disconnectAccount = useMutation({
> 39	    mutationFn: async (id: string) => {
> 40	      const { error } = await supabase.from('social_accounts').delete().eq('id', id);
> 41	      if (error) throw error;
> 42	    },
> 43	    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['social_accounts'] }),
> 44	  });
> 45	
> 46	  const initiateOAuth = async (platform: SocialPlatform) => {
> 47	    const { data, error } = await supabase.functions.invoke('social-auth-init', {
> 48	      body: { platform, redirect_uri: `${window.location.origin}/social/callback` },
> 49	    });
> 50	
> 51	    if (error) {
> 52	      const msg: string = error?.message ?? '';
> 53	      if (msg.includes('LinkedIn not configured')) {
> 54	        toast.error('Configuração Pendente: As credenciais do LinkedIn não estão configuradas no servidor.');
> 55	      } else if (msg.includes('Instagram') || msg.includes('Facebook not configured')) {
> 56	        toast.error('Configuração Pendente: As credenciais do Instagram/Facebook não estão configuradas no servidor.');
> 57	      } else if (msg.includes('Twitter') || msg.includes('X not configured')) {
> 58	        toast.error('Configuração Pendente: As credenciais do Twitter/X não estão configuradas no servidor.');
> 59	      } else {
> 60	        toast.error(`Erro ao conectar ${platform}: ${msg || 'Tente novamente.'}`);
> 61	      }
> 62	      throw error;
> 63	    }
> 64	
> 65	    if (data?.error) {
> 66	      const serverMsg: string = data.error;
> 67	      if (serverMsg === 'LinkedIn not configured') {
> 68	        toast.error('Configuração Pendente: As credenciais do LinkedIn não estão configuradas no servidor.');
> 69	      } else {
> 70	        toast.error(`Erro ao conectar ${platform}: ${serverMsg}`);
> 71	      }
> 72	      throw new Error(serverMsg);
> 73	    }
> 74	
> 75	    if (data?.url) {
> 76	      window.location.href = data.url;
> 77	    }
> 78	    return data;
> 79	  };
> 80	
> 81	  const isTokenExpired = (account: SocialAccount) => {
> 82	    if (!account.token_expires_at) return false;
> 83	    return new Date(account.token_expires_at) < new Date();
> 84	  };
> 85	
> 86	  return {
> 87	    accounts: accountsQuery.data ?? [],
> 88	    isLoading: accountsQuery.isLoading,
> 89	    error: accountsQuery.error,
> 90	    disconnectAccount,
> 91	    initiateOAuth,
> 92	    isTokenExpired,
> 93	  };
> 94	}
> 95	
> ```

## 🤖 Claude *(16:40:18)*


## 🤖 Claude *(16:40:21)*

Agora entendo a UX completa: `useMetaConfig.disconnect` faz `.delete().eq('id', status.id)` (1 linha, UNIQUE user_id) e `useSocialAccounts.disconnectAccount(id)` faz `.delete().eq('id', id)` (por-conta, keyed por id). Ambos via view → INSTEAD OF DELETE → órfão no Vault.

Tenho tudo para desenhar as RPCs. Mas primeiro, **Parte A** — o `/security-review` redundante no `87c926f`, como o Sovereign pediu. Vou invocá-lo apontado para o commit:

## 🤖 Claude *(16:40:24)*


🛠️ **Tool Call**: `Skill`
```json
{
  "skill": "security-review",
  "args": "commit 87c926f \u2014 review the already-merged migration 20260602150000_meta_social_instead_of_tenant_guard.sql (tenant guard on meta_config/social_accounts INSTEAD OF triggers). Diff to analyze: git show 87c926f. Belt-and-suspenders redundancy check requested by the Sovereign; the migration is already committed and deployed."
}
```

> **Tool Result (Skill)** - ✅ Success
>
> ```
> Launching skill: security-review
> ```

## 👤 User *(16:40:24)*

You are a senior security engineer conducting a focused security review of the changes on this branch.

GIT STATUS:

```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

FILES MODIFIED:

```
(Bash completed with no output)
```

COMMITS:

```
(Bash completed with no output)
```

DIFF CONTENT:

```
(Bash completed with no output)
```

Review the complete diff above. This contains all code changes in the PR.


OBJECTIVE:
Perform a security-focused code review to identify HIGH-CONFIDENCE security vulnerabilities that could have real exploitation potential. This is not a general code review - focus ONLY on security implications newly added by this PR. Do not comment on existing security concerns.

CRITICAL INSTRUCTIONS:
1. MINIMIZE FALSE POSITIVES: Only flag issues where you're >80% confident of actual exploitability
2. AVOID NOISE: Skip theoretical issues, style concerns, or low-impact findings
3. FOCUS ON IMPACT: Prioritize vulnerabilities that could lead to unauthorized access, data breaches, or system compromise
4. EXCLUSIONS: Do NOT report the following issue types:
   - Denial of Service (DOS) vulnerabilities, even if they allow service disruption
   - Secrets or sensitive data stored on disk (these are handled by other processes)
   - Rate limiting or resource exhaustion issues

SECURITY CATEGORIES TO EXAMINE:

**Input Validation Vulnerabilities:**
- SQL injection via unsanitized user input
- Command injection in system calls or subprocesses
- XXE injection in XML parsing
- Template injection in templating engines
- NoSQL injection in database queries
- Path traversal in file operations

**Authentication & Authorization Issues:**
- Authentication bypass logic
- Privilege escalation paths
- Session management flaws
- JWT token vulnerabilities
- Authorization logic bypasses

**Crypto & Secrets Management:**
- Hardcoded API keys, passwords, or tokens
- Weak cryptographic algorithms or implementations
- Improper key storage or management
- Cryptographic randomness issues
- Certificate validation bypasses

**Injection & Code Execution:**
- Remote code execution via deseralization
- Pickle injection in Python
- YAML deserialization vulnerabilities
- Eval injection in dynamic code execution
- XSS vulnerabilities in web applications (reflected, stored, DOM-based)

**Data Exposure:**
- Sensitive data logging or storage
- PII handling violations
- API endpoint data leakage
- Debug information exposure

Additional notes:
- Even if something is only exploitable from the local network, it can still be a HIGH severity issue

ANALYSIS METHODOLOGY:

Phase 1 - Repository Context Research (Use file search tools):
- Identify existing security frameworks and libraries in use
- Look for established secure coding patterns in the codebase
- Examine existing sanitization and validation patterns
- Understand the project's security model and threat model

Phase 2 - Comparative Analysis:
- Compare new code changes against existing security patterns
- Identify deviations from established secure practices
- Look for inconsistent security implementations
- Flag code that introduces new attack surfaces

Phase 3 - Vulnerability Assessment:
- Examine each modified file for security implications
- Trace data flow from user inputs to sensitive operations
- Look for privilege boundaries being crossed unsafely
- Identify injection points and unsafe deserialization

REQUIRED OUTPUT FORMAT:

You MUST output your findings in markdown. The markdown output should contain the file, line number, severity, category (e.g. `sql_injection` or `xss`), description, exploit scenario, and fix recommendation.

For example:

# Vuln 1: XSS: `foo.py:42`

* Severity: High
* Description: User input from `username` parameter is directly interpolated into HTML without escaping, allowing reflected XSS attacks
* Exploit Scenario: Attacker crafts URL like /bar?q=<script>alert(document.cookie)</script> to execute JavaScript in victim's browser, enabling session hijacking or data theft
* Recommendation: Use Flask's escape() function or Jinja2 templates with auto-escaping enabled for all user inputs rendered in HTML

SEVERITY GUIDELINES:
- **HIGH**: Directly exploitable vulnerabilities leading to RCE, data breach, or authentication bypass
- **MEDIUM**: Vulnerabilities requiring specific conditions but with significant impact
- **LOW**: Defense-in-depth issues or lower-impact vulnerabilities

CONFIDENCE SCORING:
- 0.9-1.0: Certain exploit path identified, tested if possible
- 0.8-0.9: Clear vulnerability pattern with known exploitation methods
- 0.7-0.8: Suspicious pattern requiring specific conditions to exploit
- Below 0.7: Don't report (too speculative)

FINAL REMINDER:
Focus on HIGH and MEDIUM findings only. Better to miss some theoretical issues than flood the report with false positives. Each finding should be something a security engineer would confidently raise in a PR review.

FALSE POSITIVE FILTERING:

> You do not need to run commands to reproduce the vulnerability, just read the code to determine if it is a real vulnerability. Do not use the bash tool or write to any files.
>
> HARD EXCLUSIONS - Automatically exclude findings matching these patterns:
> 1. Denial of Service (DOS) vulnerabilities or resource exhaustion attacks.
> 2. Secrets or credentials stored on disk if they are otherwise secured.
> 3. Rate limiting concerns or service overload scenarios.
> 4. Memory consumption or CPU exhaustion issues.
> 5. Lack of input validation on non-security-critical fields without proven security impact.
> 6. Input sanitization concerns for GitHub Action workflows unless they are clearly triggerable via untrusted input.
> 7. A lack of hardening measures. Code is not expected to implement all security best practices, only flag concrete vulnerabilities.
> 8. Race conditions or timing attacks that are theoretical rather than practical issues. Only report a race condition if it is concretely problematic.
> 9. Vulnerabilities related to outdated third-party libraries. These are managed separately and should not be reported here.
> 10. Memory safety issues such as buffer overflows or use-after-free-vulnerabilities are impossible in rust. Do not report memory safety issues in rust or any other memory safe languages.
> 11. Files that are only unit tests or only used as part of running tests.
> 12. Log spoofing concerns. Outputting un-sanitized user input to logs is not a vulnerability.
> 13. SSRF vulnerabilities that only control the path. SSRF is only a concern if it can control the host or protocol.
> 14. Including user-controlled content in AI system prompts is not a vulnerability.
> 15. Regex injection. Injecting untrusted content into a regex is not a vulnerability.
> 16. Regex DOS concerns.
> 16. Insecure documentation. Do not report any findings in documentation files such as markdown files.
> 17. A lack of audit logs is not a vulnerability.
>
> PRECEDENTS -
> 1. Logging high value secrets in plaintext is a vulnerability. Logging URLs is assumed to be safe.
> 2. UUIDs can be assumed to be unguessable and do not need to be validated.
> 3. Environment variables and CLI flags are trusted values. Attackers are generally not able to modify them in a secure environment. Any attack that relies on controlling an environment variable is invalid.
> 4. Resource management issues such as memory or file descriptor leaks are not valid.
> 5. Subtle or low impact web vulnerabilities such as tabnabbing, XS-Leaks, prototype pollution, and open redirects should not be reported unless they are extremely high confidence.
> 6. React and Angular are generally secure against XSS. These frameworks do not need to sanitize or escape user input unless it is using dangerouslySetInnerHTML, bypassSecurityTrustHtml, or similar methods. Do not report XSS vulnerabilities in React or Angular components or tsx files unless they are using unsafe methods.
> 7. Most vulnerabilities in github action workflows are not exploitable in practice. Before validating a github action workflow vulnerability ensure it is concrete and has a very specific attack path.
> 8. A lack of permission checking or authentication in client-side JS/TS code is not a vulnerability. Client-side code is not trusted and does not need to implement these checks, they are handled on the server-side. The same applies to all flows that send untrusted data to the backend, the backend is responsible for validating and sanitizing all inputs.
> 9. Only include MEDIUM findings if they are obvious and concrete issues.
> 10. Most vulnerabilities in ipython notebooks (*.ipynb files) are not exploitable in practice. Before validating a notebook vulnerability ensure it is concrete and has a very specific attack path where untrusted input can trigger the vulnerability.
> 11. Logging non-PII data is not a vulnerability even if the data may be sensitive. Only report logging vulnerabilities if they expose sensitive information such as secrets, passwords, or personally identifiable information (PII).
> 12. Command injection vulnerabilities in shell scripts are generally not exploitable in practice since shell scripts generally do not run with untrusted user input. Only report command injection vulnerabilities in shell scripts if they are concrete and have a very specific attack path for untrusted input.
>
> SIGNAL QUALITY CRITERIA - For remaining findings, assess:
> 1. Is there a concrete, exploitable vulnerability with a clear attack path?
> 2. Does this represent a real security risk vs theoretical best practice?
> 3. Are there specific code locations and reproduction steps?
> 4. Would this finding be actionable for a security team?
>
> For each finding, assign a confidence score from 1-10:
> - 1-3: Low confidence, likely false positive or noise
> - 4-6: Medium confidence, needs investigation
> - 7-10: High confidence, likely true vulnerability

START ANALYSIS:

Begin your analysis now. Do this in 3 steps:

1. Use a sub-task to identify vulnerabilities. Use the repository exploration tools to understand the codebase context, then analyze the PR changes for security implications. In the prompt for this sub-task, include all of the above.
2. Then for each vulnerability identified by the above sub-task, create a new sub-task to filter out false-positives. Launch these sub-tasks as parallel sub-tasks. In the prompt for these sub-tasks, include everything in the "FALSE POSITIVE FILTERING" instructions.
3. Filter out any vulnerabilities where the sub-task reported a confidence less than 8.

Your final reply must contain the markdown report and nothing else.

## 🤖 Claude *(16:40:36)*


## 🤖 Claude *(16:40:38)*

The security-review skill's automatic diff extraction came back empty — because `87c926f` is already merged into `main` and the working tree is clean, so there are no "pending changes" for it to pick up. I need to feed it the commit's actual diff. Let me fetch it:

## 🤖 Claude *(16:40:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit show 87c926f --format=\"COMMIT %H%nAUTHOR %an%nDATE %ad%nSUBJECT %s%n\" > /tmp/diff_87c926f.patch\necho \"=== diff captured: $(wc -l < /tmp/diff_87c926f.patch) lines ===\"\nhead -5 /tmp/diff_87c926f.patch\necho \"...\"\necho \"=== files touched ===\"\ngit show 87c926f --stat --format=\"\" ",
  "description": "Capture commit 87c926f diff for review"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === diff captured: 163 lines ===
> COMMIT 87c926fbcf4c2ff1de3833ce5330d5f14223d4fe
> AUTHOR Gabriel Zarattini
> DATE Tue Jun 2 11:57:02 2026 -0300
> SUBJECT fix(credentials): guard de tenant nas INSTEAD OF de meta_config/social_accounts
> 
> ...
> === files touched ===
>  ...2150000_meta_social_instead_of_tenant_guard.sql | 151 +++++++++++++++++++++
>  1 file changed, 151 insertions(+)
> ```

## 🤖 Claude *(16:40:48)*


## 🤖 Claude *(16:40:50)*

Commit `87c926f` toca só a migration (151 inserções). Seguindo a metodologia do skill: lanço uma sub-task para identificar vulnerabilidades com o diff + contexto do repo, depois filtros paralelos de falso-positivo. Como é uma migration SQL pequena e bem delimitada, vou dar ao agente o conteúdo e os pointers de contexto:

## 🤖 Claude *(16:41:25)*


🛠️ **Tool Call**: `Agent`
```json
{
  "description": "Security review of commit 87c926f",
  "subagent_type": "general-purpose",
  "prompt": "You are a senior security engineer doing a FOCUSED security review of ONE already-merged commit (87c926f) in a Supabase/Postgres + React project. Identify only HIGH-CONFIDENCE, concretely exploitable security vulnerabilities NEWLY INTRODUCED by this commit. Do NOT report theoretical/style/hardening issues. >80% confidence bar.\n\n## The complete diff (the only file changed \u2014 a new migration, +151 lines)\n\nFile: `supabase/migrations/20260602150000_meta_social_instead_of_tenant_guard.sql`\n\nIt recreates two SECURITY DEFINER INSTEAD OF trigger functions on masked views (`meta_config`, `social_accounts`) over base tables (`meta_config_table`, `social_accounts_table`). Full body:\n\n```sql\nCREATE OR REPLACE FUNCTION public.trg_instead_of_meta_config()\n RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path = ''\nAS $function$\nBEGIN\n  IF TG_OP = 'DELETE' THEN\n    DELETE FROM public.meta_config_table WHERE id = OLD.id;\n    RETURN OLD;\n  ELSIF TG_OP = 'INSERT' THEN\n    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN\n      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';\n    END IF;\n    INSERT INTO public.meta_config_table (\n      id, user_id, facebook_user_id, long_lived_token, scopes, pages,\n      instagram_business_account_id, whatsapp_phone_number_id, whatsapp_waba_id,\n      meta_ad_account_id, requires_reauth, token_expires_at\n    ) VALUES (\n      COALESCE(NEW.id, gen_random_uuid()), NEW.user_id, NEW.facebook_user_id, NEW.long_lived_token,\n      COALESCE(NEW.scopes, '{}'), COALESCE(NEW.pages, '[]'::jsonb), NEW.instagram_business_account_id,\n      NEW.whatsapp_phone_number_id, NEW.whatsapp_waba_id, NEW.meta_ad_account_id,\n      COALESCE(NEW.requires_reauth, FALSE), NEW.token_expires_at\n    );\n    RETURN NEW;\n  ELSIF TG_OP = 'UPDATE' THEN\n    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN\n      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';\n    END IF;\n    UPDATE public.meta_config_table SET\n      user_id = NEW.user_id, facebook_user_id = NEW.facebook_user_id,\n      long_lived_token = COALESCE(NULLIF(NEW.long_lived_token, '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'), public.meta_config_table.long_lived_token),\n      scopes = COALESCE(NEW.scopes, public.meta_config_table.scopes),\n      pages = COALESCE(NULLIF(NEW.pages, to_jsonb('\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'::text)), public.meta_config_table.pages),\n      instagram_business_account_id = NEW.instagram_business_account_id,\n      whatsapp_phone_number_id = NEW.whatsapp_phone_number_id, whatsapp_waba_id = NEW.whatsapp_waba_id,\n      meta_ad_account_id = NEW.meta_ad_account_id,\n      requires_reauth = COALESCE(NEW.requires_reauth, public.meta_config_table.requires_reauth),\n      token_expires_at = NEW.token_expires_at, updated_at = now()\n    WHERE id = OLD.id;\n    RETURN NEW;\n  END IF;\n  RETURN NULL;\nEND;\n$function$;\n\nCREATE OR REPLACE FUNCTION public.trg_instead_of_social_accounts()\n RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER SET search_path = ''\nAS $function$\nBEGIN\n  IF TG_OP = 'DELETE' THEN\n    DELETE FROM public.social_accounts_table WHERE id = OLD.id;\n    RETURN OLD;\n  ELSIF TG_OP = 'INSERT' THEN\n    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN\n      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';\n    END IF;\n    INSERT INTO public.social_accounts_table (\n      id, user_id, platform, platform_user_id, platform_username, access_token, refresh_token, token_expires_at, scopes, is_active, metadata\n    ) VALUES (\n      COALESCE(NEW.id, gen_random_uuid()), NEW.user_id, NEW.platform, NEW.platform_user_id, NEW.platform_username, NEW.access_token, NEW.refresh_token, NEW.token_expires_at, NEW.scopes, NEW.is_active, NEW.metadata\n    );\n    RETURN NEW;\n  ELSIF TG_OP = 'UPDATE' THEN\n    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN\n      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';\n    END IF;\n    UPDATE public.social_accounts_table SET\n      user_id = NEW.user_id, platform = NEW.platform, platform_user_id = NEW.platform_user_id,\n      platform_username = NEW.platform_username,\n      access_token = COALESCE(NULLIF(NEW.access_token, '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'), public.social_accounts_table.access_token),\n      refresh_token = COALESCE(NULLIF(NEW.refresh_token, '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'), public.social_accounts_table.refresh_token),\n      token_expires_at = NEW.token_expires_at, scopes = NEW.scopes, is_active = NEW.is_active,\n      metadata = NEW.metadata, updated_at = now()\n    WHERE id = OLD.id;\n    RETURN NEW;\n  END IF;\n  RETURN NULL;\nEND;\n$function$;\n```\n\n## Context (established patterns in this repo \u2014 for comparative analysis, NOT to re-flag)\n- These are masked-view INSTEAD OF triggers. The base tables have RLS; columns access_token/refresh_token/long_lived_token are encrypted to Supabase Vault by SEPARATE BEFORE triggers and the view masks them as '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'.\n- The COALESCE(NULLIF(NEW.col, '\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022'), base.col) pattern is the deliberate masked-write guard: when the client re-sends the mask sentinel (it only ever sees the mask), the existing encrypted value is preserved.\n- `auth.uid()` returns the JWT `sub` claim; `auth.role()` returns the JWT `role` claim. service_role = trusted backend (edge OAuth callbacks/cron).\n- The guard `auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid()` is the NEW code added by this commit (the rest is reproduced verbatim from the prior live definition). Its sibling `user_api_keys` trigger got the identical guard in migration 20260602130000.\n- The DELETE branch has NO guard but is constrained by the view's own WHERE (user_id = auth.uid()) which qualifies which OLD rows are visible to a non-service-role caller.\n\n## Your focus\nAnalyze the SECURITY of the change ITSELF. Specifically reason about:\n1. Does the guard correctly prevent cross-tenant credential writes (INSERT and UPDATE)? Any bypass (NULL handling, type coercion, role spoofing within Postgres RLS context)?\n2. `SET search_path = ''` with `auth.uid()`/`auth.role()` \u2014 are those resolvable (they live in the `auth` schema, schema-qualified here as `auth.uid()`)? Could search_path='' break or be bypassed?\n3. The UPDATE branch: can a caller move a row to another user (NEW.user_id) or escape the guard via the WHERE id = OLD.id targeting? Note the guard checks NEW.user_id vs auth.uid() but the WHERE is on OLD.id \u2014 reason about whether a non-service-role caller can UPDATE a row they shouldn't (e.g., set NEW.user_id = self to steal/relocate, or OLD.id pointing at a victim row).\n4. Any SQL injection (all values are parameterized via NEW.*; confirm no dynamic SQL).\n5. service_role exemption: is trusting auth.role()='service_role' sound here?\n\nReport each finding as markdown: title, severity (HIGH/MEDIUM/LOW), category, description, concrete exploit scenario, fix recommendation, and a confidence score 1-10. If you find NO high-confidence vulnerabilities, say so explicitly and explain why the change is sound. Do not write to any files. You may read repo files for context (e.g. supabase/migrations/20260601000000_credential_encryption.sql, 20260602130000_*.sql, 20260530210000_meta_api_foundation.sql) but keep it focused."
}
```

> **Tool Result (Agent)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': "I now have the full picture. The legitimate client paths confirm: `useMetaConfig` UPDATE sets only writable cred fields (never `user_id`) filtered by `.eq('id', status.id)` where `status.id` is the caller's own row; `useSocialAccounts` only ever does SELECT/DELETE client-side (never INSERT/UPDATE). Let me do a final verification on one decisive point for the UPDATE-branch reasoning: how PostgREST UPDATE on a view binds `OLD` rows, i.e., whether a non-service-role caller can target a victim's `id`. The decisive fact is that an INSTEAD OF UPDATE fires once per row the **view's SELECT** yields under the predicate — and the view has `WHERE auth.uid() = user_id`. Let me confirm there is no GRANT or RLS gap allowing the base table to be hit directly, and double-check no `pages` jsonb masking type-coercion issue exists.\n\nI have everything needed. Let me also quickly confirm the `auth.uid()`/`auth.role()` functions are schema-qualified throughout (they are: `auth.uid()`, `auth.role()`) so `search_path = ''` cannot break resolution, and that the guard expression's NULL semantics are sound.\n\nThe analysis is complete. Here are my findings.\n\n---\n\n# Security Review — Commit 87c926f\n## `20260602150000_meta_social_instead_of_tenant_guard.sql`\n\nI verified the committed diff byte-for-byte against `git show`, confirmed the two function bodies are reproduced verbatim from the prior live definitions (`20260601000500` for meta_config, `20260601000000:457-488` for social_accounts) with **only** the guard + `SET search_path = ''` added, and traced the full trust chain: view definitions/GRANTs (`20260601000600`), base-table constraints (`20260530210000`, `20260402014040`), the sibling `user_api_keys` guard (`20260602130000`), and both client hooks (`useMetaConfig.ts`, `useSocialAccounts.ts`).\n\n## Verdict: NO high-confidence vulnerabilities newly introduced by this commit.\n\nThe change is sound and is a net security **improvement**. Detailed reasoning against each focus area below.\n\n---\n\n### 1. Guard correctly prevents cross-tenant credential writes (INSERT + UPDATE)\n\nThe guard `auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid()` is applied to both INSERT and UPDATE on both triggers.\n\n- **INSERT (the gap being closed):** Previously, the masked view granted INSERT to `authenticated` and the INSTEAD OF trigger runs SECURITY DEFINER (bypassing base-table RLS). Postgres does not apply a view's `WHERE` to INSERT, so a caller could insert with a spoofed `NEW.user_id` (a victim's) + fresh `id`, committing a victim-owned credential row with attacker-controlled tokens — a service-role publisher iterating `decrypted_*` rows would then use the injected credential (content redirection / credential confusion). The guard now rejects this with `42501`. Correct fix.\n- **NULL semantics:** `IS DISTINCT FROM` is the right operator (not `<>`). If a malicious client sends `NEW.user_id = NULL`, then `NULL IS DISTINCT FROM auth.uid()` is **TRUE** → the guard fires and rejects. (A plain `<>` would have returned NULL → treated as not-true → bypass. The chosen operator closes that.) `user_id` is also `NOT NULL` on both base tables, so a NULL would fail anyway.\n- **UPDATE:** Same guard. A non-service-role caller cannot set `NEW.user_id` to anything other than its own `auth.uid()`.\n\n### 2. `SET search_path = ''` with `auth.uid()` / `auth.role()`\n\nNo break and no bypass. Every reference is **schema-qualified** — `auth.uid()`, `auth.role()`, `public.meta_config_table`, `public.social_accounts_table`, `gen_random_uuid()` is resolved at definition time but here it's called unqualified — let me note: `gen_random_uuid()` is unqualified. However it lives in `pg_catalog` (Postgres 13+) / or the `extensions` schema on Supabase. **This is not newly introduced** — it was already unqualified in the prior verbatim body, and the prior body had **no** `search_path` pin at all (so it inherited the caller's path). Pinning to `''` is strictly safer for the qualified `auth.*`/`public.*` calls. On Supabase, `gen_random_uuid` resolves from `pg_catalog` which is always implicitly first on the path regardless of `search_path`, so it resolves correctly. This adds the same hardening the sibling `user_api_keys` function already had (`20260602130000:85`) and matches Supabase's own linter guidance. Net hardening, not a regression. Adding `SET search_path = ''` to a SECURITY DEFINER function is the recommended posture and removes the prior (unpinned) search-path-injection surface.\n\n### 3. UPDATE branch — `WHERE id = OLD.id` vs guard on `NEW.user_id` (the subtle one)\n\nThis is the most important thing to get right, and it is safe:\n\n- In an INSTEAD OF UPDATE trigger on a view, the trigger fires **once per row the view's SELECT produces** under the statement's predicate. The view is `WHERE (auth.uid() = user_id OR auth.role() = 'service_role')`. So for a non-service-role caller, the **only** `OLD` rows that can ever materialize are rows where `user_id = auth.uid()`. A caller cannot conjure an `OLD.id` pointing at a victim's row, because the victim's row is not visible through the view to that caller — PostgREST `?id=eq.<victim-uuid>` simply matches zero view rows and the trigger never fires for it. So `WHERE id = OLD.id` is implicitly tenant-scoped by the view predicate that produced `OLD`.\n- **Relocation/theft via `NEW.user_id`:** The guard blocks setting `NEW.user_id` to a victim. The legitimate client (`useMetaConfig.upsertConfig`) never sends `user_id` in the UPDATE payload at all → `NEW.user_id` defaults to `OLD.user_id` (= self) → guard passes. A non-service-role caller cannot move their own row to a victim (would set `NEW.user_id = victim` → blocked) nor pull a victim's row to themselves (victim row invisible as `OLD`). Both directions are closed.\n- **service_role:** service_role can update any visible row to any `user_id` — that is the intended, legitimate OAuth-callback/cron behavior, identical to the established pattern.\n\nOne honest note (not a vuln, and **pre-existing**, not introduced here): the guard validates `NEW.user_id` but the function does not re-assert `OLD.user_id = auth.uid()` independently — it relies on the view predicate to scope `OLD`. This is the same trust model as the verbatim prior code and the sibling `user_api_keys` trigger, and it holds because the view is SECURITY DEFINER with the `auth.uid() = user_id` filter baked in. No exploit path exists for a non-service-role caller.\n\n### 4. SQL injection\n\nNone. Every value flows through `NEW.*` / `OLD.*` plpgsql variables in static INSERT/UPDATE statements. There is zero dynamic SQL (no `EXECUTE`, no string concatenation, no `format()`). Not exploitable.\n\n### 5. `service_role` exemption soundness\n\nSound. `auth.role()` returns the `role` claim of the **server-signed** Supabase JWT. A non-service-role client cannot forge `role = 'service_role'` without the JWT signing secret. service_role is the trusted backend (edge OAuth callbacks, cron, publishers) that legitimately writes arbitrary `user_id`s. This matches the exemption already trusted across the entire credential layer (views, the `user_api_keys` guard). No new trust is granted.\n\n### DELETE branch (noted in scope)\n\nUnchanged and unguarded by design — but constrained: the DELETE fires only for `OLD` rows the view yields, and for a non-service-role caller those are exclusively `user_id = auth.uid()` rows. `WHERE id = OLD.id` on the base table then deletes only that already-tenant-scoped row. No cross-tenant delete. (Consistent with the verbatim prior code.)\n\n---\n\n## Comparative / regression check\n\nThe new bodies are identical to the prior live definitions except for the two added guard blocks and the `search_path` pin. I diffed the column maps, COALESCE defaults, and masked sentinels (`'••••••••••••'` for tokens, `to_jsonb('••••••••••••'::text)` for `pages`) against `20260601000500` (meta) and `20260601000000:457-488` (social) — preserved byte-for-byte. The masked-write guard `COALESCE(NULLIF(NEW.col, sentinel), base.col)` is intact, so re-sending the mask still preserves the stored Vault reference and never blanks a credential. No behavioral regression for legitimate writers (`useMetaConfig` self-row UPDATE/INSERT; `useSocialAccounts` is read/delete-only client-side; all token writes are service_role via OAuth callbacks).\n\n**Confidence that the change is sound and introduces no new high-confidence vulnerability: 9/10.**\n\nFiles reviewed (all absolute):\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260602150000_meta_social_instead_of_tenant_guard.sql`\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260602130000_fix_user_api_keys_instead_of_double_fire.sql`\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260601000600_secure_definer_views.sql`\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260601000500_fix_meta_config_instead_of_trigger.sql`\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260601000000_credential_encryption.sql` (social trigger origin)\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260530210000_meta_api_foundation.sql` (meta_config schema, UNIQUE(user_id))\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql` (social_accounts schema)\n- `/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useMetaConfig.ts`\n- `/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useSocialAccounts.ts`"}, {'type': 'text', 'text': "agentId: a79c43bd461f65425 (use SendMessage with to: 'a79c43bd461f65425' to continue this agent)\n<usage>subagent_tokens: 71442\ntool_uses: 13\nduration_ms: 95488</usage>"}]
> ```

## 🤖 Claude *(16:43:41)*


## 🤖 Claude *(16:43:48)*

## Parte A — `/security-review` no `87c926f`: ✅ LIMPO

A revisão (sub-task dedicada + trilha de confiança completa: views, GRANTs, constraints das tabelas base, guard irmão `user_api_keys`, hooks do frontend) retornou **zero vulnerabilidades de alta confiança** — a mudança é um **ganho líquido** de segurança (confiança 9/10). Pontos-chave verificados:
- `IS DISTINCT FROM` (não `<>`) fecha o bypass via `NEW.user_id = NULL` (com `<>` o NULL viraria not-true → bypass).
- Branch UPDATE seguro: o trigger só dispara para linhas que a view (`WHERE auth.uid() = user_id`) materializa → `OLD.id` da vítima é invisível ao caller; e `NEW.user_id` é barrado pelo guard. Roubo/realocação fechados nas duas direções.
- `search_path=''` não quebra (`auth.uid()`/`auth.role()`/`public.*` qualificados); `gen_random_uuid` resolve do `pg_catalog`.
- Zero SQL dinâmico → sem injeção. Isenção `service_role` é sólida (claim de JWT server-assinado).

Cinto-e-suspensório confirmado. Agora a Parte B.

## 🤖 Claude *(16:43:50)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Meta/social orphan-secret disconnect RPCs",
  "summary": "Build disconnect_meta/disconnect_social RPCs mirroring disconnect_wordpress to revoke orphaned Vault secrets on disconnect; +one-time cleanup of 12 existing meta orphans"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Meta/social orphan-secret disconnect RPCs". Continue your current work.'}]
> ```

## 🤖 Claude *(16:43:55)*


## 🤖 Claude *(16:43:57)*

Agora construo a migration `20260602160000`. Desenho: `disconnect_meta()` (sem param, `UNIQUE(user_id)`) e `disconnect_social(p_account_id uuid)` (casa com `disconnectAccount(id)` do frontend), ambas espelhando `disconnect_wordpress` (SECURITY DEFINER · `search_path=''` · scoped a `auth.uid()` · name-binding como guard de tenant) + limpeza one-time dos 12 órfãos meta já existentes (provadamente orphan-scoped).

## 🤖 Claude *(16:44:35)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260602160000_meta_social_disconnect_rpc.sql",
  "content": "-- Migration: Meta / social_accounts credential disconnect \u2014 privileged delete + Vault revocation\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- Why this exists (closes a documented LGPD/retention debt \u2014 HANDOFF.md Pending):\n--   Disconnecting a Meta connection (`useMetaConfig.disconnect`) or a social account\n--   (`useSocialAccounts.disconnectAccount`) went through the masked view's INSTEAD OF DELETE\n--   trigger, which only does `DELETE FROM <base>_table WHERE id = OLD.id`. The encrypted token\n--   columns (long_lived_token, pages, access_token, refresh_token) are stored as Vault secret\n--   references; deleting the base row left the underlying Vault secret ORPHANED \u2014 retained\n--   plaintext credentials with no owning row, unreachable yet never revoked. This is the exact\n--   parallel of what `disconnect_wordpress()` (20260602120000) fixed for WordPress.\n--\n--   Materially confirmed 2026-06-02 on prod: the sole tenant had 0 rows in meta_config_table yet\n--   12 orphaned Meta Vault secrets (6\u00d7 meta_config_long_lived_token_*, 6\u00d7 meta_config_pages_*) \u2014\n--   the residue of ~6 connect/disconnect cycles. This migration both (a) gives disconnect a\n--   privileged path that revokes the secret atomically with the row delete, and (b) one-time\n--   revokes the already-orphaned secrets (provably orphan-scoped: no surviving base row).\n--\n-- Vault secret naming (from the encryption triggers, 20260601000000 / 20260602140000) \u2014 keyed by\n-- the ROW id (NOT user_id, unlike user_api_keys):\n--   meta_config_long_lived_token_<row.id> \u00b7 meta_config_pages_<row.id>\n--   social_accounts_access_token_<row.id> \u00b7 social_accounts_refresh_token_<row.id>\n--\n-- Tenant safety: both RPCs run as owner (postgres, bypasses RLS, holds DELETE on vault.secrets),\n-- are scoped strictly to auth.uid() (no spoofable user_id parameter), and revoke each Vault secret\n-- scoped BOTH to the reference UUID read from the CALLER's own row AND to the deterministic secret\n-- name rebuilt from the CALLER's own row id. Because the row id in the name is the caller's, a\n-- planted foreign reference UUID (a user CAN write a raw UUID into their own token column via the\n-- masked view \u2014 the encrypt trigger treats a UUID-shaped value as an already-encrypted ref and\n-- leaves it) can NEVER match another tenant's secret name \u2192 it can only ever delete a secret the\n-- caller owns. Same name-binding guard as disconnect_wordpress().\n--\n-- BoK SSOT: docs/processes/credential-disconnect-clear.md (Law 2 SOP) \u00b7\n--           CLAUDE.md API Tenancy Model (per-user, auth.uid()-scoped).\n\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- 1. disconnect_meta() \u2014 clears the caller's single Meta connection (UNIQUE(user_id))\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nCREATE OR REPLACE FUNCTION public.disconnect_meta()\nRETURNS void\nLANGUAGE plpgsql\nSECURITY DEFINER\nSET search_path = ''\nAS $$\nDECLARE\n  v_uid       uuid := auth.uid();\n  v_row_id    uuid;\n  v_token_ref text;\n  v_pages_ref text;\nBEGIN\n  -- Fail closed: never run for an unauthenticated caller.\n  IF v_uid IS NULL THEN\n    RAISE EXCEPTION 'authentication required' USING errcode = '28000';\n  END IF;\n\n  -- Capture the row id + Vault references from the CALLER's OWN row only (UNIQUE(user_id) => at\n  -- most one). Reads the base table directly (not the masked view), so these are the real refs.\n  SELECT id, long_lived_token, pages #>> '{}'\n  INTO v_row_id, v_token_ref, v_pages_ref\n  FROM public.meta_config_table\n  WHERE user_id = v_uid;\n\n  -- Nothing connected \u2192 no-op.\n  IF v_row_id IS NULL THEN\n    RETURN;\n  END IF;\n\n  -- Delete the connection row (preserves the prior INSTEAD OF DELETE behavior). Scoped to the\n  -- caller's uid as defense-in-depth even though v_row_id already came from the caller's row.\n  DELETE FROM public.meta_config_table WHERE id = v_row_id AND user_id = v_uid;\n\n  -- True revocation of the now-orphaned Vault secrets. Scoped BOTH to the captured ref UUID AND\n  -- the deterministic name rebuilt from the caller's own row id (the tenant guard \u2014 see header).\n  IF v_token_ref ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n    DELETE FROM vault.secrets\n    WHERE id = v_token_ref::uuid\n      AND name = 'meta_config_long_lived_token_' || v_row_id::text;\n  END IF;\n\n  IF v_pages_ref ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n    DELETE FROM vault.secrets\n    WHERE id = v_pages_ref::uuid\n      AND name = 'meta_config_pages_' || v_row_id::text;\n  END IF;\nEND;\n$$;\n\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- 2. disconnect_social(p_account_id uuid) \u2014 clears one of the caller's social accounts\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nCREATE OR REPLACE FUNCTION public.disconnect_social(p_account_id uuid)\nRETURNS void\nLANGUAGE plpgsql\nSECURITY DEFINER\nSET search_path = ''\nAS $$\nDECLARE\n  v_uid         uuid := auth.uid();\n  v_row_id      uuid;\n  v_access_ref  text;\n  v_refresh_ref text;\nBEGIN\n  -- Fail closed: never run for an unauthenticated caller.\n  IF v_uid IS NULL THEN\n    RAISE EXCEPTION 'authentication required' USING errcode = '28000';\n  END IF;\n\n  -- Capture refs from the CALLER's OWN row only. The user_id scope makes a foreign / non-existent\n  -- p_account_id a silent no-op (no row materializes), with no cross-tenant information leak.\n  SELECT id, access_token, refresh_token\n  INTO v_row_id, v_access_ref, v_refresh_ref\n  FROM public.social_accounts_table\n  WHERE id = p_account_id AND user_id = v_uid;\n\n  IF v_row_id IS NULL THEN\n    RETURN;\n  END IF;\n\n  DELETE FROM public.social_accounts_table WHERE id = v_row_id AND user_id = v_uid;\n\n  IF v_access_ref ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n    DELETE FROM vault.secrets\n    WHERE id = v_access_ref::uuid\n      AND name = 'social_accounts_access_token_' || v_row_id::text;\n  END IF;\n\n  IF v_refresh_ref ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n    DELETE FROM vault.secrets\n    WHERE id = v_refresh_ref::uuid\n      AND name = 'social_accounts_refresh_token_' || v_row_id::text;\n  END IF;\nEND;\n$$;\n\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- 3. Least privilege \u2014 callable only by authenticated users (each clears only its own rows).\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nREVOKE ALL ON FUNCTION public.disconnect_meta()              FROM PUBLIC;\nREVOKE ALL ON FUNCTION public.disconnect_meta()              FROM anon;\nGRANT  EXECUTE ON FUNCTION public.disconnect_meta()          TO authenticated;\n\nREVOKE ALL ON FUNCTION public.disconnect_social(uuid)        FROM PUBLIC;\nREVOKE ALL ON FUNCTION public.disconnect_social(uuid)        FROM anon;\nGRANT  EXECUTE ON FUNCTION public.disconnect_social(uuid)    TO authenticated;\n\nCOMMENT ON FUNCTION public.disconnect_meta() IS\n  'Deletes the caller''s Meta connection (meta_config_table, UNIQUE(user_id)) and revokes its '\n  'orphaned Vault secrets (long_lived_token + pages). SECURITY DEFINER, scoped to auth.uid(); '\n  'Vault deletion is double-bound to the ref UUID and the caller''s-own-row-id secret name.';\n\nCOMMENT ON FUNCTION public.disconnect_social(uuid) IS\n  'Deletes one of the caller''s social accounts (social_accounts_table) by id and revokes its '\n  'orphaned Vault secrets (access_token + refresh_token). SECURITY DEFINER, scoped to auth.uid(); '\n  'a foreign/non-existent id is a silent no-op.';\n\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- 4. One-time revocation of ALREADY-orphaned secrets left by pre-fix disconnects.\n--    Provably orphan-scoped: only secrets whose owning base-table row NO LONGER EXISTS. The\n--    trailing 36 chars of every such secret name are the (now-deleted) row id. Live connections\n--    (a surviving row with matching id) are preserved by the NOT EXISTS guard.\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nDELETE FROM vault.secrets s\nWHERE s.name ~ '^meta_config_(long_lived_token|pages)_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'\n  AND NOT EXISTS (\n    SELECT 1 FROM public.meta_config_table m WHERE m.id::text = right(s.name, 36)\n  );\n\nDELETE FROM vault.secrets s\nWHERE s.name ~ '^social_accounts_(access_token|refresh_token)_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'\n  AND NOT EXISTS (\n    SELECT 1 FROM public.social_accounts_table sa WHERE sa.id::text = right(s.name, 36)\n  );\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260602160000_meta_social_disconnect_rpc.sql (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:44:49)*


## 🤖 Claude *(16:44:51)*

Migration escrita. Agora os dois hooks do frontend. Antes, vou ver como `disconnect_wordpress` é invocado no frontend (para espelhar o padrão de tipagem do `.rpc()`, já que as novas funções ainda não estão no `types.ts` gerado):

## 🤖 Claude *(16:44:52)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== how disconnect_wordpress is invoked in frontend ===\"\ngrep -rnE \"disconnect_wordpress|\\.rpc\\(\" src/ | grep -iE \"disconnect|rpc\" | head -20",
  "description": "Find disconnect_wordpress RPC invocation pattern in frontend"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === how disconnect_wordpress is invoked in frontend ===
> src/integrations/supabase/types.ts:2950:      disconnect_wordpress: { Args: never; Returns: undefined }
> src/pages/SocialAccountsPage.tsx:77:      // disconnect_wordpress() (SECURITY DEFINER, scoped to auth.uid()) nulls all three WP
> src/pages/SocialAccountsPage.tsx:80:      const { error } = await supabase.rpc('disconnect_wordpress');
> src/lib/billing.ts:24:  const { error } = await supabase.rpc('deduct_mco_coins', {
> src/test/canvas-video-async-smoke.test.ts:90:      await supabaseAdmin.rpc("award_mco_coins", {
> src/hooks/useAIOSConversations.ts:224:      const { error } = await supabase.rpc("boost_aios_conversation", {
> ```

## 🤖 Claude *(16:46:13)*


## 🤖 Claude *(16:46:16)*

`disconnect_wordpress` está no `types.ts` gerado (linha 2950) e é chamado como `supabase.rpc('disconnect_wordpress')` — então o caminho canônico é **regenerar types** após aplicar a migration (CLAUDE.md proíbe editar `types.ts` à mão). Vou seguir esse fluxo.

Primeiro, a **prova material** das RPCs antes de tocar produção — tudo em `BEGIN…ROLLBACK`, criando as funções inline e testando contra dados reais da vítima (3 contas sociais vivas). Escrevendo a suíte adversarial:

## 🤖 Claude *(16:46:50)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/tmp/disconnect_rpc_test.sql",
  "content": "BEGIN;\n\n-- Recreate the two RPCs inline (verbatim from the migration) so the test is self-contained and\n-- the whole thing rolls back \u2014 zero prod mutation.\nCREATE OR REPLACE FUNCTION public.disconnect_meta()\nRETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path = ''\nAS $$\nDECLARE\n  v_uid uuid := auth.uid(); v_row_id uuid; v_token_ref text; v_pages_ref text;\nBEGIN\n  IF v_uid IS NULL THEN RAISE EXCEPTION 'authentication required' USING errcode = '28000'; END IF;\n  SELECT id, long_lived_token, pages #>> '{}' INTO v_row_id, v_token_ref, v_pages_ref\n  FROM public.meta_config_table WHERE user_id = v_uid;\n  IF v_row_id IS NULL THEN RETURN; END IF;\n  DELETE FROM public.meta_config_table WHERE id = v_row_id AND user_id = v_uid;\n  IF v_token_ref ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n    DELETE FROM vault.secrets WHERE id = v_token_ref::uuid AND name = 'meta_config_long_lived_token_' || v_row_id::text;\n  END IF;\n  IF v_pages_ref ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n    DELETE FROM vault.secrets WHERE id = v_pages_ref::uuid AND name = 'meta_config_pages_' || v_row_id::text;\n  END IF;\nEND; $$;\n\nCREATE OR REPLACE FUNCTION public.disconnect_social(p_account_id uuid)\nRETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path = ''\nAS $$\nDECLARE\n  v_uid uuid := auth.uid(); v_row_id uuid; v_access_ref text; v_refresh_ref text;\nBEGIN\n  IF v_uid IS NULL THEN RAISE EXCEPTION 'authentication required' USING errcode = '28000'; END IF;\n  SELECT id, access_token, refresh_token INTO v_row_id, v_access_ref, v_refresh_ref\n  FROM public.social_accounts_table WHERE id = p_account_id AND user_id = v_uid;\n  IF v_row_id IS NULL THEN RETURN; END IF;\n  DELETE FROM public.social_accounts_table WHERE id = v_row_id AND user_id = v_uid;\n  IF v_access_ref ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n    DELETE FROM vault.secrets WHERE id = v_access_ref::uuid AND name = 'social_accounts_access_token_' || v_row_id::text;\n  END IF;\n  IF v_refresh_ref ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n    DELETE FROM vault.secrets WHERE id = v_refresh_ref::uuid AND name = 'social_accounts_refresh_token_' || v_row_id::text;\n  END IF;\nEND; $$;\n\nCREATE TEMP TABLE _r(test text, outcome text) ON COMMIT DROP;\n\nDO $$\nDECLARE\n  v_victim   uuid := 'ada39fae-67e1-4e53-af1c-5a18e1c108e8';\n  v_attacker uuid := gen_random_uuid();\n  v_li_id    uuid := '931386ca-3c73-4a5f-b43b-517093004598'; -- linkedin\n  v_ig_id    uuid := '39ce0ebb-3579-481a-93ce-8a20759cd22e'; -- instagram\n  v_fb_id    uuid := '6910dd24-ca3e-473f-ba70-7ab488aef9ea'; -- facebook\n  v_ig_secret uuid;  -- instagram's access_token secret UUID (the \"victim secret\" in T3)\n  v_meta_id  uuid;\n  v_meta_token_secret uuid;\n  v_meta_pages_secret uuid;\n  v_exists boolean;\nBEGIN\n  -- \u2500\u2500 T1: disconnect_social happy path (victim disconnects linkedin) \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n  PERFORM set_config('request.jwt.claims', json_build_object('sub', v_victim::text, 'role','authenticated')::text, true);\n  PERFORM public.disconnect_social(v_li_id);\n  SELECT EXISTS(SELECT 1 FROM public.social_accounts_table WHERE id = v_li_id) INTO v_exists;\n  IF v_exists THEN INSERT INTO _r VALUES ('T1_social_row_deleted','FAIL -- row survived');\n  ELSE\n    SELECT EXISTS(SELECT 1 FROM vault.secrets WHERE name = 'social_accounts_access_token_' || v_li_id::text) INTO v_exists;\n    IF v_exists THEN INSERT INTO _r VALUES ('T1_social_secret_revoked','FAIL -- Vault secret ORPHANED (still present)');\n    ELSE INSERT INTO _r VALUES ('T1_social_happy_path','PASS -- row deleted AND vault secret revoked'); END IF;\n  END IF;\n\n  -- \u2500\u2500 T2: disconnect_social foreign-id no-op (attacker targets victim's instagram) \u2500\u2500\n  PERFORM set_config('request.jwt.claims', json_build_object('sub', v_attacker::text, 'role','authenticated')::text, true);\n  PERFORM public.disconnect_social(v_ig_id);\n  SELECT EXISTS(SELECT 1 FROM public.social_accounts_table WHERE id = v_ig_id) INTO v_exists;\n  IF NOT v_exists THEN INSERT INTO _r VALUES ('T2_foreign_id_noop','FAIL -- attacker DELETED victim row');\n  ELSE\n    SELECT EXISTS(SELECT 1 FROM vault.secrets WHERE name = 'social_accounts_access_token_' || v_ig_id::text) INTO v_exists;\n    IF NOT v_exists THEN INSERT INTO _r VALUES ('T2_foreign_id_noop','FAIL -- attacker REVOKED victim secret');\n    ELSE INSERT INTO _r VALUES ('T2_foreign_id_noop','PASS -- foreign id is a no-op (victim row+secret intact)'); END IF;\n  END IF;\n\n  -- \u2500\u2500 T3: planted-ref name-binding (plant instagram's secret UUID into facebook's row,\n  --        victim disconnects facebook \u2192 instagram's secret must SURVIVE via name mismatch) \u2500\u2500\n  SELECT id INTO v_ig_secret FROM vault.secrets WHERE name = 'social_accounts_access_token_' || v_ig_id::text;\n  UPDATE public.social_accounts_table SET access_token = v_ig_secret::text WHERE id = v_fb_id; -- plant\n  PERFORM set_config('request.jwt.claims', json_build_object('sub', v_victim::text, 'role','authenticated')::text, true);\n  PERFORM public.disconnect_social(v_fb_id);\n  SELECT EXISTS(SELECT 1 FROM vault.secrets WHERE id = v_ig_secret) INTO v_exists;\n  IF v_exists THEN INSERT INTO _r VALUES ('T3_planted_ref_name_binding','PASS -- instagram secret SURVIVED planted-ref attack (name binding held)');\n  ELSE INSERT INTO _r VALUES ('T3_planted_ref_name_binding','FAIL -- name binding bypassed; cross-row secret deleted'); END IF;\n\n  -- \u2500\u2500 T4: disconnect_meta happy path (insert meta row w/ token+pages \u2192 disconnect \u2192 both revoked) \u2500\u2500\n  PERFORM set_config('request.jwt.claims', json_build_object('sub', v_victim::text, 'role','authenticated')::text, true);\n  INSERT INTO public.meta_config_table (user_id, long_lived_token, pages)\n    VALUES (v_victim, 'PLAINTEXT_META_TOKEN', '[{\"page_id\":\"p1\",\"name\":\"P\",\"access_token\":\"pt\"}]'::jsonb)\n    RETURNING id INTO v_meta_id;\n  -- confirm encryption created both secrets\n  SELECT EXISTS(SELECT 1 FROM vault.secrets WHERE name='meta_config_long_lived_token_'||v_meta_id::text) INTO v_exists;\n  IF NOT v_exists THEN INSERT INTO _r VALUES ('T4_meta_setup','FAIL -- encryption did not create token secret');\n  ELSE\n    PERFORM public.disconnect_meta();\n    SELECT EXISTS(SELECT 1 FROM public.meta_config_table WHERE id = v_meta_id) INTO v_exists;\n    IF v_exists THEN INSERT INTO _r VALUES ('T4_meta_happy_path','FAIL -- meta row survived'); END IF;\n    SELECT (EXISTS(SELECT 1 FROM vault.secrets WHERE name='meta_config_long_lived_token_'||v_meta_id::text)\n         OR EXISTS(SELECT 1 FROM vault.secrets WHERE name='meta_config_pages_'||v_meta_id::text)) INTO v_exists;\n    IF v_exists THEN INSERT INTO _r VALUES ('T4_meta_secrets_revoked','FAIL -- a meta secret ORPHANED');\n    ELSE INSERT INTO _r VALUES ('T4_meta_happy_path','PASS -- row deleted AND both vault secrets (token+pages) revoked'); END IF;\n  END IF;\n\n  -- \u2500\u2500 T5: disconnect_meta fail-closed when unauthenticated \u2500\u2500\n  PERFORM set_config('request.jwt.claims', json_build_object('role','authenticated')::text, true); -- no sub => auth.uid() NULL\n  BEGIN\n    PERFORM public.disconnect_meta();\n    INSERT INTO _r VALUES ('T5_unauth_fail_closed','FAIL -- ran without auth.uid()');\n  EXCEPTION\n    WHEN sqlstate '28000' THEN INSERT INTO _r VALUES ('T5_unauth_fail_closed','PASS -- 28000 authentication required');\n    WHEN others THEN INSERT INTO _r VALUES ('T5_unauth_fail_closed','OTHER '||SQLSTATE||': '||SQLERRM);\n  END;\n\n  PERFORM set_config('request.jwt.claims', NULL, true);\nEND $$;\n\nSELECT test, outcome FROM _r ORDER BY test;\nROLLBACK;\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /tmp/disconnect_rpc_test.sql (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:46:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "TOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"$(python3 -c 'import json,sys; print(json.dumps({\"query\": open(\"/tmp/disconnect_rpc_test.sql\").read()}))')\" | python3 -m json.tool\necho \"\"",
  "description": "Run disconnect RPC material test suite (BEGIN/ROLLBACK)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [
>     {
>         "test": "T1_social_happy_path",
>         "outcome": "PASS -- row deleted AND vault secret revoked"
>     },
>     {
>         "test": "T2_foreign_id_noop",
>         "outcome": "PASS -- foreign id is a no-op (victim row+secret intact)"
>     },
>     {
>         "test": "T3_planted_ref_name_binding",
>         "outcome": "PASS -- instagram secret SURVIVED planted-ref attack (name binding held)"
>     },
>     {
>         "test": "T4_meta_happy_path",
>         "outcome": "PASS -- row deleted AND both vault secrets (token+pages) revoked"
>     },
>     {
>         "test": "T5_unauth_fail_closed",
>         "outcome": "PASS -- 28000 authentication required"
>     }
> ]
> ```

## 🤖 Claude *(16:47:05)*


## 🤖 Claude *(16:47:10)*

**5 de 5 PASS** — RPCs materialmente provadas, tudo revertido:

| Teste | Resultado |
|-------|-----------|
| T1 `disconnect_social` happy path | **PASS** — linha deletada **E** segredo Vault revogado |
| T2 foreign-id no-op | **PASS** — atacante não deleta linha/segredo da vítima |
| T3 planted-ref name-binding | **PASS** — segredo cross-row sobrevive (o guard de tenant aguenta) |
| T4 `disconnect_meta` happy path | **PASS** — linha + **ambos** segredos (token+pages) revogados; prova o extract `pages #>> '{}'` |
| T5 unauth fail-closed | **PASS** — `28000` |

Agora confirmar zero resíduo do teste + preview do que a limpeza one-time removeria (deve ser 12 órfãos meta, 0 sociais vivos):

## 🤖 Claude *(16:47:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "TOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\nQUERY=$(cat <<'SQL'\nWITH residue AS (\n  SELECT 'victim_social_rows' AS k, string_agg(platform::text, ',' ORDER BY platform::text) AS v\n  FROM public.social_accounts_table WHERE user_id='ada39fae-67e1-4e53-af1c-5a18e1c108e8'\n  UNION ALL\n  SELECT 'victim_meta_rows', count(*)::text FROM public.meta_config_table WHERE user_id='ada39fae-67e1-4e53-af1c-5a18e1c108e8'\n),\ncleanup_preview AS (\n  SELECT\n    'meta_secrets: WOULD_DELETE (orphan)' AS k,\n    count(*) FILTER (WHERE NOT EXISTS (SELECT 1 FROM public.meta_config_table m WHERE m.id::text = right(s.name,36)))::text AS v\n  FROM vault.secrets s WHERE s.name ~ '^meta_config_(long_lived_token|pages)_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'\n  UNION ALL\n  SELECT 'meta_secrets: WOULD_PRESERVE (live)',\n    count(*) FILTER (WHERE EXISTS (SELECT 1 FROM public.meta_config_table m WHERE m.id::text = right(s.name,36)))::text\n  FROM vault.secrets s WHERE s.name ~ '^meta_config_(long_lived_token|pages)_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'\n  UNION ALL\n  SELECT 'social_secrets: WOULD_DELETE (orphan)',\n    count(*) FILTER (WHERE NOT EXISTS (SELECT 1 FROM public.social_accounts_table sa WHERE sa.id::text = right(s.name,36)))::text\n  FROM vault.secrets s WHERE s.name ~ '^social_accounts_(access_token|refresh_token)_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'\n  UNION ALL\n  SELECT 'social_secrets: WOULD_PRESERVE (live)',\n    count(*) FILTER (WHERE EXISTS (SELECT 1 FROM public.social_accounts_table sa WHERE sa.id::text = right(s.name,36)))::text\n  FROM vault.secrets s WHERE s.name ~ '^social_accounts_(access_token|refresh_token)_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'\n)\nSELECT * FROM residue UNION ALL SELECT * FROM cleanup_preview;\nSQL\n)\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"{\\\"query\\\": $(printf '%s' \"$QUERY\" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}\" | python3 -m json.tool\necho \"\"; rm -f /tmp/disconnect_rpc_test.sql /tmp/diff_87c926f.patch",
  "description": "Verify zero test residue + preview orphan cleanup scope"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [
>     {
>         "k": "victim_social_rows",
>         "v": "facebook,instagram,linkedin"
>     },
>     {
>         "k": "victim_meta_rows",
>         "v": "0"
>     },
>     {
>         "k": "meta_secrets: WOULD_DELETE (orphan)",
>         "v": "12"
>     },
>     {
>         "k": "meta_secrets: WOULD_PRESERVE (live)",
>         "v": "0"
>     },
>     {
>         "k": "social_secrets: WOULD_DELETE (orphan)",
>         "v": "0"
>     },
>     {
>         "k": "social_secrets: WOULD_PRESERVE (live)",
>         "v": "3"
>     }
> ]
> ```

## 🤖 Claude *(16:47:32)*


## 🤖 Claude *(16:47:35)*

**Zero resíduo do teste** (vítima intacta: `facebook,instagram,linkedin` + 0 meta) e **preview da limpeza provadamente orphan-scoped**:

| Escopo | Qtd |
|--------|-----|
| meta secrets — **WOULD_DELETE (órfão)** | **12** ✅ |
| meta secrets — WOULD_PRESERVE (vivo) | 0 |
| social secrets — WOULD_DELETE (órfão) | **0** ✅ |
| social secrets — WOULD_PRESERVE (vivo) | **3** ✅ (os 3 vivos protegidos pelo `NOT EXISTS`) |

A limpeza remove exatamente os 12 órfãos meta conhecidos e preserva os 3 segredos sociais vivos. Agora ligo o frontend às RPCs (mudança cirúrgica nos 2 hooks):

## 🤖 Claude *(16:47:39)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useMetaConfig.ts",
  "old_string": "  const disconnect = useMutation({\n    mutationFn: async () => {\n      if (!status?.id) return;\n      const { error } = await db.from('meta_config').delete().eq('id', status.id);\n      if (error) throw error;\n    },\n    onSuccess: () => {\n      queryClient.invalidateQueries({ queryKey: ['meta_config', user?.id] });\n    },\n  });",
  "new_string": "  const disconnect = useMutation({\n    mutationFn: async () => {\n      // Privileged disconnect: disconnect_meta() (SECURITY DEFINER, scoped to auth.uid()) deletes\n      // the row AND revokes the orphaned Vault secrets (long_lived_token + pages). A plain DELETE\n      // through the masked view would delete only the base row and leak the plaintext secret.\n      const { error } = await db.rpc('disconnect_meta');\n      if (error) throw error;\n    },\n    onSuccess: () => {\n      queryClient.invalidateQueries({ queryKey: ['meta_config', user?.id] });\n    },\n  });"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useMetaConfig.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:47:45)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useSocialAccounts.ts",
  "old_string": "  const disconnectAccount = useMutation({\n    mutationFn: async (id: string) => {\n      const { error } = await supabase.from('social_accounts').delete().eq('id', id);\n      if (error) throw error;\n    },\n    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['social_accounts'] }),\n  });",
  "new_string": "  const disconnectAccount = useMutation({\n    mutationFn: async (id: string) => {\n      // Privileged disconnect: disconnect_social() (SECURITY DEFINER, scoped to auth.uid()) deletes\n      // the row AND revokes the orphaned Vault secrets (access_token + refresh_token). A plain\n      // DELETE through the masked view would delete only the base row and leak the plaintext token.\n      const { error } = await supabase.rpc('disconnect_social', { p_account_id: id });\n      if (error) throw error;\n    },\n    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['social_accounts'] }),\n  });"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useSocialAccounts.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:48:39)*


## 🤖 Claude *(16:48:41)*

RPCs ligadas. Agora o gate obrigatório: **`/security-review` na nova migration (Parte B)** antes de aplicar em prod (CLAUDE.md: toda migration passa por security-review antes do commit). Vou capturar o diff completo das mudanças não-commitadas e submetê-lo à revisão:

## 🤖 Claude *(16:48:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add -A\necho \"=== staged changes ===\"; git diff --cached --stat\necho \"\"; echo \"=== full diff captured to /tmp ===\"; git diff --cached > /tmp/partB.diff; wc -l /tmp/partB.diff",
  "description": "Stage Part B changes and capture diff for review"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === staged changes ===
>  src/hooks/useMetaConfig.ts                         |   6 +-
>  src/hooks/useSocialAccounts.ts                     |   5 +-
>  .../20260602160000_meta_social_disconnect_rpc.sql  | 171 +++++++++++++++++++++
>  3 files changed, 179 insertions(+), 3 deletions(-)
> 
> === full diff captured to /tmp ===
> 210 /tmp/partB.diff
> ```

## 🤖 Claude *(16:48:54)*


## 🤖 Claude *(16:49:21)*


🛠️ **Tool Call**: `Agent`
```json
{
  "description": "Security review of Part B migration",
  "subagent_type": "general-purpose",
  "prompt": "You are a senior security engineer doing a FOCUSED security review of an UNCOMMITTED change in a Supabase/Postgres + React (TypeScript) project. Report only HIGH-CONFIDENCE, concretely exploitable vulnerabilities NEWLY INTRODUCED by this change. >80% confidence bar. No style/hardening/theoretical issues. This change touches the CREDENTIAL ENCRYPTION layer, so scrutinize tenant isolation hard.\n\n## What changed (3 files)\n1. NEW migration `supabase/migrations/20260602160000_meta_social_disconnect_rpc.sql` \u2014 read it in full at that path.\n2. `src/hooks/useMetaConfig.ts` \u2014 `disconnect` mutation now calls `db.rpc('disconnect_meta')` instead of `db.from('meta_config').delete().eq('id', status.id)`.\n3. `src/hooks/useSocialAccounts.ts` \u2014 `disconnectAccount(id)` now calls `supabase.rpc('disconnect_social', { p_account_id: id })` instead of `.from('social_accounts').delete().eq('id', id)`.\n\nAlso read the full diff at `/tmp/partB.diff`.\n\n## Purpose & threat model context\nThese two RPCs close an LGPD/retention debt: previously, disconnecting a Meta or social account deleted the base row via an INSTEAD OF DELETE trigger but left the encrypted token's Vault secret ORPHANED (retained plaintext). The RPCs delete the row AND revoke the Vault secret.\n\nEstablished repo facts you must use:\n- `meta_config` / `social_accounts` are masked SECURITY-DEFINER views over `meta_config_table` / `social_accounts_table` (RLS on, force_rls off so the postgres owner bypasses RLS).\n- Encryption BEFORE-triggers store secrets in `vault.secrets` with DETERMINISTIC names keyed by the ROW id: `meta_config_long_lived_token_<row.id>`, `meta_config_pages_<row.id>`, `social_accounts_access_token_<row.id>`, `social_accounts_refresh_token_<row.id>`. The token COLUMNS hold the Vault secret's UUID as text (pages holds `to_jsonb(uuid::text)`).\n- A user CAN write a raw UUID into their own token column via the masked view (the encrypt trigger treats a UUID-shaped value as an already-encrypted reference and leaves it as-is). So a \"planted foreign reference\" is a real capability a caller has on THEIR OWN row.\n- `auth.uid()` = JWT `sub`; `auth.role()` = JWT `role`; service_role = trusted backend. JWT is server-signed (clients can't forge role).\n- The sibling RPC `disconnect_wordpress()` (migration `20260602120000_wordpress_disconnect_rpc.sql` \u2014 read it for the established pattern) is what this mirrors, EXCEPT WordPress secrets are named by `user_id` while meta/social are named by ROW id.\n\n## Reason hard about these specific things\n1. **Cross-tenant row deletion:** In `disconnect_social(p_account_id uuid)`, `p_account_id` is attacker-controllable. The function does `SELECT ... WHERE id = p_account_id AND user_id = auth.uid()` then `DELETE ... WHERE id = v_row_id AND user_id = v_uid`. Can a caller delete or affect a row owned by a different user? Is the no-op-on-foreign-id behavior actually safe (no information leak, no deletion)?\n2. **Cross-tenant Vault secret revocation (the critical one):** The Vault DELETE is `WHERE id = <ref-uuid read from caller's own row> AND name = '<prefix>_' || v_row_id::text` where v_row_id is the caller's own row id. Since meta/social secret names are keyed by ROW id (not user_id), reason about whether a caller can revoke ANOTHER tenant's Vault secret by planting that victim secret's UUID into their own row's token column and then disconnecting. Does the `AND name = ...caller's-own-row-id...` binding actually prevent this? Walk through the exact predicate.\n3. **The one-time cleanup DELETE on `vault.secrets`** (bottom of the migration): it deletes secrets matching a name regex where `NOT EXISTS` a base-table row whose `id::text = right(s.name, 36)`. Verify: (a) can it over-delete a LIVE secret (one whose row still exists)? (b) `right(s.name, 36)` \u2014 is the trailing 36 chars always exactly the row UUID for every matched name? (c) any way this deletes a secret belonging to a different/unintended owner inappropriately, or any injection via secret names? (d) is matching by `right(name,36)` robust against a secret name that coincidentally matches the regex but whose suffix isn't a real row id (would just be a no-op delete of an orphan \u2014 acceptable \u2014 but confirm it can't delete something it shouldn't)?\n4. **SECURITY DEFINER + `SET search_path = ''`:** all object refs are schema-qualified (`public.*`, `vault.secrets`, `auth.uid()`); `gen_random_uuid`/`right`/`now` builtins. Any resolution break or search-path injection?\n5. **SQL injection / dynamic SQL:** confirm none (all static statements, parameters via plpgsql vars).\n6. **GRANTs:** REVOKE from PUBLIC/anon, GRANT EXECUTE to authenticated. Sound? Could anon reach it?\n7. **Client hooks:** the React changes call `.rpc()` \u2014 any client-side issue? (Remember: client-side authz is not a vuln per precedent; the backend RPC is the trust boundary.)\n\nFor each finding: title, severity (HIGH/MEDIUM/LOW), category, description, concrete exploit scenario with the exact attack steps, fix recommendation, confidence 1-10. If NO high-confidence vulnerability exists, say so explicitly and justify per each numbered concern above. Do NOT write to any files. Be rigorous but precise \u2014 false positives are costly."
}
```

> **Tool Result (Agent)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Both base tables have `id UUID PRIMARY KEY`. This seals the analysis of the "name binding" guard: the secret name in the Vault DELETE predicate is `<prefix>_<v_row_id>` where `v_row_id` is the **caller\'s own row id**. Because `id` is a PRIMARY KEY, the attacker\'s own row id can never equal a victim\'s row id, so the name predicate can never match a victim\'s secret name — exactly as the WordPress precedent established, and exactly as the migration header claims. The double-binding (`id = ref-uuid AND name = caller\'s-own-row-id`) is sound.\n\nI have completed a full analysis of all seven concerns with the underlying schema fully verified. Here is my report.\n\n---\n\n# Security Review: `20260602160000_meta_social_disconnect_rpc.sql` + hook changes\n\n## Verdict: NO high-confidence, newly-introduced vulnerability found.\n\nThe change is sound. The two RPCs correctly mirror the established `disconnect_wordpress()` pattern, and the row-id-keyed secret naming (the one structural difference vs. WordPress\'s user-id keying) is correctly defended by the same double-binding predicate. I walked each numbered concern to ground truth in the schema. Details below.\n\n---\n\n### Concern 1 — Cross-tenant row deletion (`disconnect_social(p_account_id)`): SAFE\n\nThe row is selected with `WHERE id = p_account_id AND user_id = v_uid` (= `auth.uid()`). A foreign or non-existent `p_account_id` leaves `v_row_id` NULL → the `IF v_row_id IS NULL THEN RETURN` short-circuits before any DELETE. The subsequent `DELETE ... WHERE id = v_row_id AND user_id = v_uid` is redundantly re-scoped. No cross-tenant deletion, and no information leak: the function returns `void` identically whether the id is foreign, non-existent, or simply not connected — the three cases are indistinguishable to the caller. `disconnect_meta()` takes no id at all (keyed purely on `auth.uid()` over `UNIQUE(user_id)`), so it is even tighter.\n\n### Concern 2 — Cross-tenant Vault secret revocation (the critical one): SAFE\n\nThe Vault DELETE is double-bound: `WHERE id = <ref-uuid from caller\'s own row> AND name = \'<prefix>_\' || v_row_id::text`, where `v_row_id` is the **caller\'s own** row id (read from `meta_config_table`/`social_accounts_table WHERE user_id = auth.uid()`).\n\nI traced the full "planted foreign reference" attack the prompt flagged:\n1. An attacker can indeed plant an arbitrary UUID into their own token column via the masked view (confirmed: the encrypt trigger `trg_encrypt_*` treats a UUID-shaped value as an already-encrypted ref and leaves it as-is — `20260602140000` lines 252-267 / 291-307). So `v_*_ref` is attacker-controllable.\n2. But the secret **name** in the predicate is rebuilt from `v_row_id` — the attacker\'s own row id. Both base tables declare `id UUID PRIMARY KEY` (verified: `meta_config` line 28, `social_accounts` line 83). So the attacker\'s own row id can **never** equal a victim\'s row id (PK uniqueness across the shared table). Since meta/social secret names are keyed by row id, the rebuilt name `meta_config_long_lived_token_<attacker-row-id>` can never collide with a victim\'s secret name `..._<victim-row-id>`. The `AND name = ...` clause therefore makes the DELETE a guaranteed no-op against any secret the caller doesn\'t own — even though the `id = ref-uuid` half would match.\n3. Independently, the attack is also unreachable on the read side: to plant a victim\'s UUID the attacker must first *learn* it, but the raw Vault UUID ref is never exposed to any client. The masked views (`20260601000600`) mask token columns to `••••••••••••` and filter `WHERE auth.uid() = user_id`; SELECT on the base tables is REVOKED from `authenticated`; and the `decrypted_*` views are `GRANT SELECT ... TO service_role` only (REVOKE from anon/authenticated). So the attacker controls neither half of the predicate against a victim.\n\nNote the attack against meta/social is *structurally weaker* than WordPress even before the name guard: WordPress shares one secret name per user (`..._<uid>`), whereas meta/social names embed a per-row UUID the attacker cannot know or reproduce for a victim. The name binding holds regardless.\n\n### Concern 3 — One-time cleanup DELETE on `vault.secrets`: SAFE\n\n- (a) **Over-delete of a LIVE secret?** No. The `NOT EXISTS (SELECT 1 FROM <base> WHERE id::text = right(s.name, 36))` guard preserves any secret whose owning row still exists. A live connection\'s secret is retained.\n- (b) **Is `right(name, 36)` always the row UUID?** Yes, for every name the regex matches. The anchored regex `^<prefix>_<8-4-4-4-12>$` forces the name to end in exactly a canonical 36-char UUID with the prefix as a literal head; a canonical UUID is exactly 36 chars, so `right(name, 36)` is exactly that trailing UUID. The prefixes (`meta_config_long_lived_token_`, `meta_config_pages_`, `social_accounts_access_token_`, `social_accounts_refresh_token_`) contain no hex-UUID-shaped suffix that could shift the boundary, and the encrypt triggers only ever produce names of this exact `<prefix>_<NEW.id>` shape.\n- (c) **Wrong-owner deletion / name injection?** No injection vector: secret names are server-generated by the triggers as `<static-prefix> || row.id::text` (a UUID) — clients never influence the name. The cleanup only removes secrets matching the four hard-coded prefixes whose row no longer exists; "ownership" is moot because an orphan has no owning row by definition.\n- (d) **Coincidental regex match with a non-row suffix?** Would simply be a no-op delete of an orphan (NOT EXISTS is satisfied), which is the acceptable/intended outcome. It cannot delete a live secret because the only way a matched name maps to a surviving row is via the exact `id::text = right(name,36)` equality the guard checks.\n\nCaveat (not a finding): the cleanup is one-time DDL-context DML scoped to the four prefixes; cross-prefix collision is impossible since each prefix is distinct and anchored.\n\n### Concern 4 — SECURITY DEFINER + `SET search_path = \'\'`: SAFE\n\nAll references are schema-qualified: `public.meta_config_table`, `public.social_accounts_table`, `vault.secrets`, `auth.uid()`. Builtins `right()`, `now()`, `gen_random_uuid()` resolve from `pg_catalog`, which is always implicitly first on `search_path` and cannot be shadowed by a user schema. The `~` regex operator and `::uuid`/`::text` casts are catalog operators. No unqualified object reference exists → no search-path hijack surface. Matches the hardening precedent in `20260602140000` and `20260602150000`.\n\n### Concern 5 — SQL injection / dynamic SQL: NONE\n\nNo `EXECUTE`, no string-built SQL. All statements are static; the only interpolation is `|| v_row_id::text` into a string *value* compared with `=` (not into SQL text), and `v_row_id` is a `uuid`-typed plpgsql variable read from the DB — not a string and not parseable as SQL. The `p_account_id` parameter is bound as a typed `uuid` plpgsql variable. No injection.\n\n### Concern 6 — GRANTs: SOUND\n\n`REVOKE ALL ... FROM PUBLIC` and `FROM anon`, then `GRANT EXECUTE ... TO authenticated` for both functions. anon cannot reach either RPC. Even if anon somehow invoked one, the `IF v_uid IS NULL THEN RAISE EXCEPTION` fail-closed guard (errcode 28000) blocks execution with no `auth.uid()`. Mirrors `disconnect_wordpress()` exactly.\n\n### Concern 7 — Client hooks: NO ISSUE\n\n`useMetaConfig.ts` now calls `db.rpc(\'disconnect_meta\')`; `useSocialAccounts.ts` calls `supabase.rpc(\'disconnect_social\', { p_account_id: id })`. Both propagate errors via `if (error) throw error`. The client passing `id` is irrelevant to security — the RPC re-scopes every operation to `auth.uid()` server-side, which is the trust boundary (consistent with repo precedent that client-side authz is not the control). `disconnect_meta` no longer needs the prior `status?.id` guard since the function is a no-op when nothing is connected.\n\n---\n\n## Minor observations (NOT vulnerabilities, not blocking)\n\n- **Atomicity:** In both RPCs the row DELETE and the Vault DELETE(s) run in the same implicit transaction, so a failure in the Vault delete rolls back the row delete — good (no half-disconnected state, no premature orphan).\n- **`disconnect_meta` no longer early-returns when `status?.id` is falsy** at the client; it always issues the RPC. Harmless (server no-ops), and arguably more correct since it also sweeps a stale Vault secret if the client\'s cached `status` was empty.\n\nThese are observations only; I am not flagging them. Confidence that no exploitable cross-tenant vulnerability was introduced: **9/10**. The one structural risk the prompt rightly highlighted (row-id-keyed secret names) is fully neutralized by the PK-guaranteed-distinct row id inside the name predicate plus the total absence of any client-reachable leak of the raw secret UUID.\n\nRelevant files:\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260602160000_meta_social_disconnect_rpc.sql` (under review)\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260602120000_wordpress_disconnect_rpc.sql` (mirrored pattern)\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql` (encrypt triggers: row-id secret naming + UUID-passthrough)\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260602150000_meta_social_instead_of_tenant_guard.sql` (INSTEAD OF tenant guard; INSERT accepts client `NEW.id`)\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260601000600_secure_definer_views.sql` (masked views, base-table SELECT revoke, decrypted views service_role-only)\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260530210000_meta_api_foundation.sql` + `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql` (PK + RLS definitions)'}, {'type': 'text', 'text': "agentId: ae6ff81e6a9f99139 (use SendMessage with to: 'ae6ff81e6a9f99139' to continue this agent)\n<usage>subagent_tokens: 92985\ntool_uses: 18\nduration_ms: 124220</usage>"}]
> ```

## 🤖 Claude *(16:51:52)*


## 🤖 Claude *(16:51:59)*

## Parte B — `/security-review`: ✅ LIMPO (confiança 9/10)

Zero vulnerabilidades de alta confiança. O reviewer cravou a preocupação crítica (nomes de segredo por `id` de linha) com **duas defesas independentes**:
1. **PK garante `id` distinto** — o `id` da própria linha do atacante nunca iguala o da vítima, então o `AND name = '<prefix>_' || v_row_id` jamais casa o nome do segredo da vítima (no-op garantido).
2. **O UUID-ref bruto nunca vaza ao cliente** — views mascaram tokens, SELECT na tabela base é revogado de `authenticated`, views `decrypted_*` são service_role-only. O atacante nem consegue *aprender* o UUID da vítima para plantar.

Mais: cleanup provadamente orphan-scoped, `right(name,36)` correto, zero SQL dinâmico, GRANTs sólidos, atomicidade (revoga e deleta na mesma transação). Gate passou.

Antes de aplicar, vou checar como as migrations anteriores foram registradas (para escolher `db push` vs Management API e não criar drift de tracking):

## 🤖 Claude *(16:52:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "TOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\nQUERY='SELECT version FROM supabase_migrations.schema_migrations WHERE version >= '\"'\"'20260602120000'\"'\"' ORDER BY version;'\necho \"=== migrations recorded as applied (>= 20260602120000) ===\"\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"{\\\"query\\\": $(printf '%s' \"$QUERY\" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}\" | python3 -m json.tool",
  "description": "Check recorded migration tracking state"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === migrations recorded as applied (>= 20260602120000) ===
> [
>     {
>         "version": "20260602120000"
>     },
>     {
>         "version": "20260602130000"
>     },
>     {
>         "version": "20260602140000"
>     },
>     {
>         "version": "20260602150000"
>     }
> ]
> ```

## 🤖 Claude *(16:52:22)*


## 🤖 Claude *(16:52:24)*

As migrations 120000-150000 estão registradas em `schema_migrations` — o time usa tracking adequado. Para não criar drift, vou aplicar a 160000 E registrá-la. Deixa eu ver o estado do CLI link e a estrutura da `schema_migrations` para escolher o método (db push vs Management API atômica + tracking):

## 🤖 Claude *(16:52:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== supabase CLI link state ===\"; cat supabase/.temp/project-ref 2>/dev/null || echo \"(no .temp/project-ref)\"; ls supabase/.temp/ 2>/dev/null\necho \"\"; echo \"=== schema_migrations columns ===\"\nTOKEN=$(cat ~/.supabase/access-token); REF=bcyvddsykvehvpwstlfa\nQUERY='SELECT column_name, data_type FROM information_schema.columns WHERE table_schema='\"'\"'supabase_migrations'\"'\"' AND table_name='\"'\"'schema_migrations'\"'\"' ORDER BY ordinal_position;'\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d \"{\\\"query\\\": $(printf '%s' \"$QUERY\" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}\" | python3 -m json.tool\necho \"\"; echo \"=== sample existing row (150000) to mirror name/statements shape ===\"\nQUERY2='SELECT version, name, (statements IS NOT NULL) AS has_statements, array_length(statements,1) AS n_statements FROM supabase_migrations.schema_migrations WHERE version='\"'\"'20260602150000'\"'\"';'\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d \"{\\\"query\\\": $(printf '%s' \"$QUERY2\" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}\" | python3 -m json.tool",
  "description": "Inspect CLI link and schema_migrations shape"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === supabase CLI link state ===
> bcyvddsykvehvpwstlfacli-latest
> gotrue-version
> linked-project.json
> pooler-url
> postgres-version
> project-ref
> rest-version
> storage-migration
> storage-version
> 
> === schema_migrations columns ===
> [
>     {
>         "column_name": "version",
>         "data_type": "text"
>     },
>     {
>         "column_name": "statements",
>         "data_type": "ARRAY"
>     },
>     {
>         "column_name": "name",
>         "data_type": "text"
>     }
> ]
> 
> === sample existing row (150000) to mirror name/statements shape ===
> [
>     {
>         "version": "20260602150000",
>         "name": "meta_social_instead_of_tenant_guard",
>         "has_statements": false,
>         "n_statements": null
>     }
> ]
> ```

## 🤖 Claude *(16:53:01)*


## 🤖 Claude *(16:53:03)*

CLI está linkado. A linha de tracking da 150000 usa `version` + `name` (statements NULL). Vou aplicar via Management API de forma **atômica** (`BEGIN…COMMIT`) e registrar na `schema_migrations` no mesmo batch — replica o efeito do `db push` sem risco de prompt interativo de senha. Construindo o payload a partir do arquivo da migration:

## 🤖 Claude *(16:53:07)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nTOKEN=$(cat ~/.supabase/access-token); REF=bcyvddsykvehvpwstlfa\npython3 <<'PY'\nimport json, urllib.request, os\nmig = open('supabase/migrations/20260602160000_meta_social_disconnect_rpc.sql').read()\nbatch = \"BEGIN;\\n\" + mig + \"\\nINSERT INTO supabase_migrations.schema_migrations (version, name) VALUES ('20260602160000','meta_social_disconnect_rpc');\\nCOMMIT;\\n\"\ntoken = open(os.path.expanduser('~/.supabase/access-token')).read().strip()\nreq = urllib.request.Request(\n    \"https://api.supabase.com/v1/projects/bcyvddsykvehvpwstlfa/database/query\",\n    data=json.dumps({\"query\": batch}).encode(),\n    headers={\"Authorization\": f\"Bearer {token}\", \"Content-Type\": \"application/json\"},\n    method=\"POST\")\ntry:\n    resp = urllib.request.urlopen(req)\n    print(\"HTTP\", resp.status)\n    print(resp.read().decode() or \"(empty result body = success, no rows)\")\nexcept urllib.error.HTTPError as e:\n    print(\"HTTP ERROR\", e.code)\n    print(e.read().decode())\nPY",
  "description": "Apply migration 20260602160000 atomically via Management API"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> HTTP ERROR 403
> error code: 1010
> ```

## 🤖 Claude *(16:53:16)*


## 🤖 Claude *(16:53:18)*

403 / Cloudflare 1010 — bloqueio por User-Agent do `urllib` (o `curl` passou em todas as queries anteriores). Vou refazer com `curl`, escrevendo o batch num arquivo e JSON-encodando via Python só para o payload:

## 🤖 Claude *(16:53:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\n# Build the atomic apply batch: BEGIN + migration + tracking insert + COMMIT\n{ echo \"BEGIN;\"; cat supabase/migrations/20260602160000_meta_social_disconnect_rpc.sql; echo \"INSERT INTO supabase_migrations.schema_migrations (version, name) VALUES ('20260602160000','meta_social_disconnect_rpc');\"; echo \"COMMIT;\"; } > /tmp/apply160000.sql\necho \"batch lines: $(wc -l < /tmp/apply160000.sql)\"\nTOKEN=$(cat ~/.supabase/access-token); REF=bcyvddsykvehvpwstlfa\nRESP=$(curl -s -w \"\\n__HTTP_%{http_code}__\" -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"$(python3 -c 'import json; print(json.dumps({\"query\": open(\"/tmp/apply160000.sql\").read()}))')\")\necho \"$RESP\"",
  "description": "Apply migration atomically via curl"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> batch lines: 174
> []
> __HTTP_201__
> ```

## 🤖 Claude *(16:53:31)*


## 🤖 Claude *(16:53:32)*

HTTP 201, resultado `[]` (COMMIT sem linhas = sucesso). Migration aplicada atomicamente. Agora a **verificação material pós-apply** (Lei 1) — funções existem, GRANTs corretos, 12 órfãos sumiram, 3 vivos intactos, tracking registrado:

## 🤖 Claude *(16:53:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nTOKEN=$(cat ~/.supabase/access-token); REF=bcyvddsykvehvpwstlfa\nQUERY=$(cat <<'SQL'\nSELECT 'fn_exists' AS check, p.proname AS detail,\n  (p.prosecdef AND array_to_string(p.proconfig,',') = 'search_path=')::text AS ok\nFROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace\nWHERE n.nspname='public' AND p.proname IN ('disconnect_meta','disconnect_social')\nUNION ALL\nSELECT 'grant_authenticated', p.proname,\n  has_function_privilege('authenticated', p.oid, 'EXECUTE')::text\nFROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace\nWHERE n.nspname='public' AND p.proname IN ('disconnect_meta','disconnect_social')\nUNION ALL\nSELECT 'grant_anon_REVOKED', p.proname,\n  (NOT has_function_privilege('anon', p.oid, 'EXECUTE'))::text\nFROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace\nWHERE n.nspname='public' AND p.proname IN ('disconnect_meta','disconnect_social')\nUNION ALL\nSELECT 'meta_orphans_remaining', 'should be 0', count(*)::text\nFROM vault.secrets s WHERE s.name ~ '^meta_config_(long_lived_token|pages)_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'\n  AND NOT EXISTS (SELECT 1 FROM public.meta_config_table m WHERE m.id::text = right(s.name,36))\nUNION ALL\nSELECT 'meta_secrets_total_now', 'was 12 (all orphan)', count(*)::text\nFROM vault.secrets s WHERE s.name LIKE 'meta_config_%'\nUNION ALL\nSELECT 'social_live_secrets_intact', 'should be 3', count(*)::text\nFROM vault.secrets s WHERE s.name ~ '^social_accounts_(access_token|refresh_token)_'\nUNION ALL\nSELECT 'victim_social_rows_intact', 'should be 3', count(*)::text\nFROM public.social_accounts_table WHERE user_id='ada39fae-67e1-4e53-af1c-5a18e1c108e8'\nUNION ALL\nSELECT 'migration_recorded', '20260602160000', (count(*)>0)::text\nFROM supabase_migrations.schema_migrations WHERE version='20260602160000'\nORDER BY 1,2;\nSQL\n)\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"{\\\"query\\\": $(printf '%s' \"$QUERY\" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}\" | python3 -m json.tool\nrm -f /tmp/apply160000.sql /tmp/partB.diff",
  "description": "Material post-apply verification of RPCs, grants, orphan cleanup"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [
>     {
>         "check": "fn_exists",
>         "detail": "disconnect_meta",
>         "ok": "false"
>     },
>     {
>         "check": "fn_exists",
>         "detail": "disconnect_social",
>         "ok": "false"
>     },
>     {
>         "check": "grant_anon_REVOKED",
>         "detail": "disconnect_meta",
>         "ok": "true"
>     },
>     {
>         "check": "grant_anon_REVOKED",
>         "detail": "disconnect_social",
>         "ok": "true"
>     },
>     {
>         "check": "grant_authenticated",
>         "detail": "disconnect_meta",
>         "ok": "true"
>     },
>     {
>         "check": "grant_authenticated",
>         "detail": "disconnect_social",
>         "ok": "true"
>     },
>     {
>         "check": "meta_orphans_remaining",
>         "detail": "should be 0",
>         "ok": "0"
>     },
>     {
>         "check": "meta_secrets_total_now",
>         "detail": "was 12 (all orphan)",
>         "ok": "0"
>     },
>     {
>         "check": "migration_recorded",
>         "detail": "20260602160000",
>         "ok": "true"
>     },
>     {
>         "check": "social_live_secrets_intact",
>         "detail": "should be 3",
>         "ok": "3"
>     },
>     {
>         "check": "victim_social_rows_intact",
>         "detail": "should be 3",
>         "ok": "3"
>     }
> ]
> ```

## 🤖 Claude *(16:53:56)*


## 🤖 Claude *(16:54:00)*

Tudo verde — exceto um `fn_exists=false` que é **bug da minha expressão de check** (comparei contra `'search_path='` mas o valor real é `search_path=""` com aspas; e os GRANTs resolveram contra os oids das funções, o que só é possível se elas existem). Material confirmado:
- GRANT authenticated ✅ · anon revogado ✅ (ambas)
- **12 órfãos meta → 0** (`meta_secrets_total_now: 0`) ✅
- 3 segredos sociais vivos intactos ✅ · 3 linhas sociais da vítima intactas ✅
- migration registrada na `schema_migrations` ✅

Deixa eu confirmar o `prosecdef`/`search_path` com a comparação correta para fechar o gate de materialidade da função:

## 🤖 Claude *(16:54:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "TOKEN=$(cat ~/.supabase/access-token); REF=bcyvddsykvehvpwstlfa\nQUERY='SELECT p.proname AS fn, p.prosecdef AS security_definer, array_to_string(p.proconfig,'\"'\"','\"'\"') AS proconfig, pg_get_function_identity_arguments(p.oid) AS args FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='\"'\"'public'\"'\"' AND p.proname IN ('\"'\"'disconnect_meta'\"'\"','\"'\"'disconnect_social'\"'\"') ORDER BY p.proname;'\ncurl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" \\\n  -d \"{\\\"query\\\": $(printf '%s' \"$QUERY\" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}\" | python3 -m json.tool",
  "description": "Confirm SECURITY DEFINER and search_path on deployed functions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [
>     {
>         "fn": "disconnect_meta",
>         "security_definer": true,
>         "proconfig": "search_path=\"\"",
>         "args": ""
>     },
>     {
>         "fn": "disconnect_social",
>         "security_definer": true,
>         "proconfig": "search_path=\"\"",
>         "args": "p_account_id uuid"
>     }
> ]
> ```

## 🤖 Claude *(16:54:32)*


## 🤖 Claude *(16:54:35)*

`disconnect_meta` (sem args) e `disconnect_social(p_account_id uuid)`: ambas SECURITY DEFINER, `search_path=""`. Backend 100% verificado. O `fn_exists=false` anterior era de fato bug da minha string de comparação.

Agora o frontend. `useSocialAccounts.ts` usa o client **tipado**, então preciso regenerar o `types.ts` (CLAUDE.md proíbe editar à mão). Vou gerar para um arquivo temp e inspecionar o diff antes de sobrescrever:

## 🤖 Claude *(16:54:39)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== how is types.ts currently generated? (header + schemas) ===\"\nhead -20 src/integrations/supabase/types.ts | grep -iE \"schema|generated|public\" | head\necho \"\"; echo \"=== attempt gen types to temp ===\"\nexport SUPABASE_ACCESS_TOKEN=$(cat ~/.supabase/access-token)\ntimeout 120 npx supabase gen types typescript --project-id bcyvddsykvehvpwstlfa --schema public > /tmp/types.new.ts 2>/tmp/types.err.txt\necho \"exit=$? \u00b7 new file lines: $(wc -l < /tmp/types.new.ts 2>/dev/null)\"\necho \"--- stderr (if any) ---\"; head -20 /tmp/types.err.txt",
  "description": "Regenerate Supabase types to temp file"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === how is types.ts currently generated? (header + schemas) ===
>   graphql_public: {
> 
> === attempt gen types to temp ===
> exit=0 · new file lines: 3279
> --- stderr (if any) ---
> A new version of Supabase CLI is available: v2.104.0 (currently installed v2.92.1)
> We recommend updating regularly for new features and bug fixes: https://supabase.com/docs/guides/cli/getting-started#updating-the-supabase-cli
> ```

## 🤖 Claude *(16:54:55)*


## 🤖 Claude *(16:54:57)*

gen types rodou (exit 0). Mas gerei só `--schema public` e o arquivo atual inclui `graphql_public` — preciso casar os schemas para não dropar nenhum. Deixa eu ver os schemas do arquivo atual e o diff:

## 🤖 Claude *(16:55:00)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== top-level schema keys in CURRENT types.ts ===\"; grep -nE \"^  (public|graphql_public|[a-z_]+): \\{$\" src/integrations/supabase/types.ts | head\necho \"\"; echo \"=== current vs new line counts ===\"; wc -l src/integrations/supabase/types.ts /tmp/types.new.ts\necho \"\"; echo \"=== does new file have the new functions? ===\"; grep -nE \"disconnect_meta|disconnect_social|disconnect_wordpress|vault_upsert_secret\" /tmp/types.new.ts | head\necho \"\"; echo \"=== does new file still have graphql_public? ===\"; grep -cE \"graphql_public\" /tmp/types.new.ts",
  "description": "Compare schemas between current and regenerated types"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === top-level schema keys in CURRENT types.ts ===
> 15:  graphql_public: {
> 40:  public: {
> 3205:  graphql_public: {
> 3208:  public: {
> 
> === current vs new line counts ===
>   3301 src/integrations/supabase/types.ts
>   3279 /tmp/types.new.ts
>   6580 total
> 
> === does new file have the new functions? ===
> 2925:      disconnect_meta: { Args: never; Returns: undefined }
> 2926:      disconnect_social: { Args: { p_account_id: string }; Returns: undefined }
> 2927:      disconnect_wordpress: { Args: never; Returns: undefined }
> 2969:      vault_upsert_secret: {
> 
> === does new file still have graphql_public? ===
> 0
> ```

## 🤖 Claude *(16:55:17)*


## 🤖 Claude *(16:55:18)*

O novo arquivo tem as funções que preciso (`disconnect_meta`, `disconnect_social` com `p_account_id`), mas gerei só `public` e perdi `graphql_public`. Vou regenerar com os dois schemas e inspecionar o diff (evitar churn de formatação / drop de schema):

## 🤖 Claude *(16:55:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nexport SUPABASE_ACCESS_TOKEN=$(cat ~/.supabase/access-token)\ntimeout 120 npx supabase gen types typescript --project-id bcyvddsykvehvpwstlfa --schema public,graphql_public > /tmp/types.both.ts 2>/dev/null\necho \"exit=$? lines=$(wc -l < /tmp/types.both.ts)\"\necho \"\"; echo \"=== DIFF (current vs regenerated both-schema) \u2014 summary ===\"\ndiff <(cat src/integrations/supabase/types.ts) /tmp/types.both.ts > /tmp/types.diff 2>&1\necho \"diff lines: $(wc -l < /tmp/types.diff)\"\necho \"\"; echo \"=== diff content (first 120 lines) ===\"\nhead -120 /tmp/types.diff",
  "description": "Regenerate with both schemas and diff against current"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> exit=0 lines=3307
> 
> === DIFF (current vs regenerated both-schema) — summary ===
> diff lines: 8
> 
> === diff content (first 120 lines) ===
> 2949a2950,2951
> >       disconnect_meta: { Args: never; Returns: undefined }
> >       disconnect_social: { Args: { p_account_id: string }; Returns: undefined }
> 2990a2993,2996
> >       }
> >       vault_upsert_secret: {
> >         Args: { p_desc?: string; p_name: string; p_value: string }
> >         Returns: string
> ```

## 🤖 Claude *(16:55:39)*


## 🤖 Claude *(16:55:40)*

Diff **limpo, 8 linhas, só adições** — exatamente as 2 RPCs novas + `vault_upsert_secret` (da migration 140000, que não teve types regenerado na época). Zero churn de formatação, zero schema dropado. Vou aplicar e rodar tsc + lint:

## 🤖 Claude *(16:55:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ncp /tmp/types.both.ts src/integrations/supabase/types.ts\necho \"=== types.ts updated; confirm new entries present ===\"\ngrep -nE \"disconnect_meta|disconnect_social|vault_upsert_secret\" src/integrations/supabase/types.ts\necho \"\"; echo \"=== tsc --noEmit ===\"\ntimeout 300 npx tsc --noEmit 2>&1 | head -30; echo \"tsc exit=${PIPESTATUS[0]}\"",
  "description": "Apply regenerated types and run tsc"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === types.ts updated; confirm new entries present ===
> 2950:      disconnect_meta: { Args: never; Returns: undefined }
> 2951:      disconnect_social: { Args: { p_account_id: string }; Returns: undefined }
> 2994:      vault_upsert_secret: {
> 
> === tsc --noEmit ===
> tsc exit=0
> ```

## 🤖 Claude *(16:55:46)*


## 🤖 Claude *(16:55:47)*

`tsc --noEmit` exit 0 — os hooks tipam com as novas RPCs. Agora lint + testes:

## 🤖 Claude *(16:55:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== eslint (changed files) ===\"\ntimeout 180 npx eslint src/hooks/useMetaConfig.ts src/hooks/useSocialAccounts.ts 2>&1 | head -20; echo \"eslint exit=${PIPESTATUS[0]}\"\necho \"\"; echo \"=== vitest (run once) ===\"\ntimeout 300 bun run test 2>&1 | tail -25; echo \"test exit=${PIPESTATUS[0]}\"",
  "description": "Run eslint on changed hooks and full test suite"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === eslint (changed files) ===
> eslint exit=0
> 
> === vitest (run once) ===
>     at runWithTimeout [90m(file:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:1863:10[90m)[39m
>     at runTest [90m(file:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:1574:12[90m)[39m
>     at runSuite [90m(file:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:1729:8[90m)[39m
>     at runSuite [90m(file:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:1729:8[90m)[39m
>     at runSuite [90m(file:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:1729:8[90m)[39m
> 
>  ✓ src/test/useSubscription.test.ts (16 tests) 83ms
>  ✓ src/test/useOrchestrationStore.test.ts (29 tests) 19ms
>  ✓ src/test/qa-verifiers.test.ts (36 tests) 22ms
>  ✓ src/test/billing.test.ts (22 tests) 21ms
>  ✓ src/test/e2e-user-zero-selftest.test.ts (8 tests) 16ms
>  ✓ src/test/qa-extract-manifest.test.ts (27 tests) 18ms
>  ✓ src/lib/affiliate.test.ts (14 tests) 23ms
>  ✓ src/test/meta.test.ts (18 tests) 12ms
>  ✓ src/test/canvas-handles.test.ts (4 tests) 13ms
>  ✓ src/test/canvas-dag.test.ts (5 tests) 9ms
>  ✓ src/test/example.test.ts (1 test) 3ms
>  ↓ src/test/aios-sql-bridge-smoke.test.ts (1 test | 1 skipped)
>  ↓ src/test/canvas-video-async-smoke.test.ts (1 test | 1 skipped)
> 
>  Test Files  15 passed | 2 skipped (17)
>       Tests  238 passed | 2 skipped (240)
>    Start at  13:55:51
>    Duration  7.26s (transform 764ms, setup 1.41s, collect 2.60s, tests 1.59s, environment 8.59s, prepare 2.27s)
> 
> test exit=0
> ```

## 🤖 Claude *(16:56:17)*


## 🤖 Claude *(16:56:21)*

- **eslint exit=0** ✅
- **vitest: 238 passed | 2 skipped, exit=0** ✅ (os fragmentos de stack no topo são de testes smoke pulados; o sumário confirma 0 falhas)

Backend vivo + verificado, mas o bundle servido ainda chama `.delete()` (órfão) até eu rebuildar. Estou no **repo PRINCIPAL** (`/home/gcrUX/htdocs/constellation-orchestra`, não worktree), então `bun run build` = deploy. Seguindo a disciplina `build-deploy-guardian`: confirmar `.env`, capturar estado pré-build, buildar, e verificar materialmente (chunk novo + env baked).

## 🤖 Claude *(16:56:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== .env present? (env baked into bundle) ===\"; test -f .env && echo \"YES (.env exists, $(wc -l < .env) lines)\" || echo \"NO .env \u2014 WORKTREE TRAP risk\"\necho \"\"; echo \"=== pre-build dist assets (current served) ===\"; ls -la dist/assets/*.js 2>/dev/null | tail -3 || echo \"(no dist yet)\"\necho \"\"; echo \"=== build ===\"; timeout 400 bun run build 2>&1 | tail -15; echo \"build exit=${PIPESTATUS[0]}\"",
  "description": "Verify .env and build frontend"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === .env present? (env baked into bundle) ===
> YES (.env exists, 21 lines)
> 
> === pre-build dist assets (current served) ===
> -rw-rw-r-- 1 ubuntu ubuntu   7939 Jun  2 10:14 dist/assets/ViralMinerPage-BxYYhtwC.js
> -rw-rw-r-- 1 ubuntu ubuntu    832 Jun  2 10:14 dist/assets/volume-2-BFZrRUjN.js
> -rw-rw-r-- 1 ubuntu ubuntu    434 Jun  2 10:14 dist/assets/zap-Bil0E-TF.js
> 
> === build ===
> dist/assets/CoreV2Page-DlsvUucq.js              73.06 kB │ gzip:  22.41 kB
> dist/assets/proxy-BOUo65A-.js                  125.30 kB │ gzip:  41.24 kB
> dist/assets/CanvasEditorPage-CDUQ4xHv.js       140.18 kB │ gzip:  38.75 kB
> dist/assets/index-DbvP5HKv.js                  167.17 kB │ gzip:  53.48 kB
> dist/assets/ConstellationPage-CjCjJ7qc.js      185.12 kB │ gzip:  63.83 kB
> dist/assets/ConstellationMatrix-fVTr36qp.js    248.23 kB │ gzip:  63.05 kB
> dist/assets/CartesianChart-DfQDFbgo.js         325.06 kB │ gzip:  96.83 kB
> dist/assets/index-DWwqssDL.js                  625.55 kB │ gzip: 186.98 kB
> dist/assets/Stars-Cnh2-m2P.js                  826.42 kB │ gzip: 222.88 kB
> 
> (!) Some chunks are larger than 500 kB after minification. Consider:
> - Using dynamic import() to code-split the application
> - Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
> - Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
> ✓ built in 21.16s
> build exit=0
> ```

## 🤖 Claude *(16:56:53)*


## 🤖 Claude *(16:56:53)*

Build exit 0 (built in 21.16s). Verificação material do guardian — provar que o bundle SERVIDO contém as novas chamadas RPC + env baked + chunks novos:

## 🤖 Claude *(16:57:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== new assets built just now (timestamp) ===\"; ls -la --time-style=+%H:%M dist/assets/*.js | grep -E \"$(date +%H:): \" | head -5 || ls -lat dist/assets/*.js | head -3\necho \"\"; echo \"=== served bundle contains the new RPC calls? ===\"\ngrep -rl \"disconnect_social\" dist/assets/ 2>/dev/null | head && echo \"--- disconnect_social FOUND in served bundle ---\" || echo \"disconnect_social NOT FOUND\"\ngrep -rl \"disconnect_meta\" dist/assets/ 2>/dev/null | head && echo \"--- disconnect_meta FOUND in served bundle ---\" || echo \"disconnect_meta NOT FOUND\"\necho \"\"; echo \"=== env baked (Supabase URL in bundle)? ===\"\ngrep -rlE \"bcyvddsykvehvpwstlfa\\.supabase\\.co\" dist/assets/ 2>/dev/null | head -1 && echo \"--- Supabase URL baked ---\" || echo \"ENV NOT BAKED (worktree trap!)\"\necho \"\"; echo \"=== old .delete() path on social_accounts gone from bundle? (sanity) ===\"\ngrep -roE \"from\\(.social_accounts.\\)\\.delete\" dist/assets/ 2>/dev/null | head || echo \"(no raw .from('social_accounts').delete pattern \u2014 consistent with RPC swap)\"",
  "description": "Materially verify served bundle has RPC calls and baked env"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === new assets built just now (timestamp) ===
> 
> === served bundle contains the new RPC calls? ===
> dist/assets/useSocialAccounts-ASExBY5P.js
> --- disconnect_social FOUND in served bundle ---
> dist/assets/SettingsPage-C9UPsnYb.js
> --- disconnect_meta FOUND in served bundle ---
> 
> === env baked (Supabase URL in bundle)? ===
> dist/assets/CalendarPage-B3yyjqGp.js
> --- Supabase URL baked ---
> 
> === old .delete() path on social_accounts gone from bundle? (sanity) ===
> ```

## 🤖 Claude *(16:57:13)*


## 🤖 Claude *(16:57:17)*

Bundle servido **materialmente verificado**:
- `disconnect_social` → `dist/assets/useSocialAccounts-ASExBY5P.js` ✅
- `disconnect_meta` → `dist/assets/SettingsPage-C9UPsnYb.js` ✅ (via MetaConfigCard)
- Supabase URL **baked** (env presente, sem worktree trap) ✅

Frontend live em login.mcorch.com (hard-refresh `Ctrl+Shift+R` por causa do Cloudflare). Agora **Lei 2** — atualizar o SOP. Deixa eu ler a estrutura para inserir a seção das novas RPCs:

## 🤖 Claude *(16:57:17)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/credential-disconnect-clear.md",
  "offset": 1,
  "limit": 60
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# SOP — Clearing / revoking per-user credentials stored behind masked Vault views
> 2	
> 3	**Status:** active · **Owner (ROI/risk):** Sovereign · **Created:** 2026-06-02
> 4	**Applies to:** `user_api_keys` (WordPress + AI keys), and by analogy `meta_config`, `social_accounts` — all masked SECURITY-DEFINER views over `*_table` with Vault-encrypted secret columns (migrations `20260601000000_credential_encryption.sql`, `20260601000600_secure_definer_views.sql`).
> 5	
> 6	## Problem this SOP anticipates (the trap)
> 7	
> 8	After credential-encryption, a credential column on the masked view cannot be cleared by a
> 9	client writing `NULL`. The view's INSTEAD OF trigger writes secret columns through
> 10	`COALESCE(NULLIF(NEW.x, '••••••••••••'), base.x)` — a **load-bearing guard** that lets a partial
> 11	save touch only some fields without wiping the others. Its side effect: **`NULL` preserves the old
> 12	value**, so a disconnect that nulls columns from the client silently leaves the secret (and its
> 13	plaintext in the Vault) in place. Worse, SELECT on the base table is REVOKED from `authenticated`,
> 14	so the client has no privileged path to a true clear.
> 15	
> 16	A true clear/revoke therefore MUST run server-side with elevated privileges.
> 17	
> 18	## Operator
> 19	
> 20	Today: an **authenticated end-user** clicking "Desconectar" on `/dashboard/settings`
> 21	(SocialAccounts page) for WordPress. The privileged work is delegated to the
> 22	`disconnect_wordpress()` RPC (SECURITY DEFINER, owner `postgres`), scoped to `auth.uid()`.
> 23	
> 24	Manual equivalent (Sovereign / support, e.g. an LGPD erasure request): run the same clear via the
> 25	Supabase SQL editor or Management API as a privileged role (see Recovery).
> 26	
> 27	## Sequence (per disconnect)
> 28	
> 29	1. Client calls `supabase.rpc('disconnect_wordpress')` — no parameters (identity comes from the JWT).
> 30	   - **Success criterion:** RPC returns `{ error: null }`.
> 31	2. RPC reads the caller's `wp_app_password` reference from `user_api_keys_table WHERE user_id = auth.uid()`.
> 32	3. RPC nulls `wp_site_url`, `wp_username`, `wp_app_password` on the base table (privileged — bypasses the masked view's COALESCE-NULLIF guard).
> 33	4. RPC deletes the Vault secret, scoped to BOTH `id = <ref>` AND `name = 'user_api_keys_wp_app_password_' || auth.uid()` (the name binding makes it provably impossible to delete another tenant's secret, even though `wp_app_password` is client-writable).
> 34	
> 35	## Verification gates (material — Law 1)
> 36	
> 37	Query the decrypted view for the affected user (service_role / Management API):
> 38	```sql
> 39	SELECT wp_site_url, wp_username, wp_app_password
> 40	FROM public.decrypted_user_api_keys WHERE user_id = '<uid>';
> 41	-- PASS: all three NULL
> 42	SELECT count(*) FROM vault.secrets WHERE name = 'user_api_keys_wp_app_password_<uid>';
> 43	-- PASS: 0
> 44	```
> 45	UI gate: the WordPress card shows the "Desconectado" badge; the AI keys (groq/openrouter/…) for the
> 46	same user are UNCHANGED (the clear must be surgical — never wipe sibling credentials).
> 47	
> 48	## Recovery path (failure in any step)
> 49	
> 50	- **RPC errors `authentication required` (28000):** the caller had no `sub` claim — re-authenticate; do not retry as anon.
> 51	- **RPC succeeds but verification shows a lingering secret:** the secret name diverged from the
> 52	  deterministic pattern (legacy/backfill). Clear manually as a privileged role:
> 53	  ```sql
> 54	  UPDATE public.user_api_keys_table
> 55	    SET wp_site_url = NULL, wp_username = NULL, wp_app_password = NULL, updated_at = now()
> 56	  WHERE user_id = '<uid>';
> 57	  DELETE FROM vault.secrets WHERE name LIKE 'user_api_keys_wp_app_password_<uid>%';
> 58	  ```
> 59	- **Reconnect fails with `unique_violation` on `vault.secrets.name`:** a stale secret with the
> 60	  deterministic name survived a prior clear. Delete it (query above), then reconnect.
> ```

## 🤖 Claude *(16:57:23)*


## 🤖 Claude *(16:57:25)*

SOP bem estruturado (documenta WordPress via `disconnect_wordpress()`; o header já antecipa "por analogia meta_config/social_accounts" — que era o débito). Vou ler o resto para achar o ponto de inserção da nova seção:

## 🤖 Claude *(16:57:25)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/credential-disconnect-clear.md",
  "offset": 60,
  "limit": 52
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 60	  deterministic name survived a prior clear. Delete it (query above), then reconnect.
> 61	
> 62	## Success signal
> 63	
> 64	Decrypted view shows all three WP columns NULL, zero matching `vault.secrets` rows, sibling AI keys
> 65	intact, and a fresh connect (save) succeeds and re-creates exactly one Vault secret.
> 66	
> 67	## Saving / connecting (companion fix)
> 68	
> 69	`user_api_keys` is a VIEW with no unique constraint → PostgREST `.upsert()`/`onConflict` returns
> 70	**HTTP 400 (42P10)**. Writes MUST use `.insert()`, which routes through the INSTEAD OF INSERT trigger
> 71	that does `INSERT ... ON CONFLICT (user_id) DO UPDATE` internally (upserts). Canonical reference:
> 72	`src/hooks/useUserApiKeys.ts`. The same applies to `meta_config`/`social_accounts`, except those
> 73	INSTEAD OF INSERT triggers have **no** ON CONFLICT, so their hooks use `.update()`-if-exists /
> 74	`.insert()`-if-not (`useMetaConfig`, `useAffiliateConfig`).
> 75	
> 76	## Resolved latent debt — idempotent encryption (closed 2026-06-02)
> 77	
> 78	**Was:** the encryption triggers (`trg_encrypt_user_api_keys` + its `meta_config`/`social_accounts`
> 79	siblings) called `vault.create_secret(value, '<deterministic-name>')` **unconditionally** on a secret
> 80	change. `vault.create_secret` does a plain INSERT with **no ON CONFLICT** and `vault.secrets.name` is
> 81	UNIQUE (`secrets_name_idx`) → **rotating a credential in place (new value, same name) threw
> 82	`unique_violation` (23505)**. User-facing: WordPress "Editar → save a new password without
> 83	disconnecting first". (connect → disconnect → reconnect always worked because `disconnect_wordpress()`
> 84	deletes the secret first; only the rotate-in-place path was broken.)
> 85	
> 86	**Fix:** migration `20260602140000_vault_upsert_secret_idempotent_encrypt.sql` introduces
> 87	`public.vault_upsert_secret(value, name, desc)` — SECURITY DEFINER, `search_path=''`, EXECUTE revoked
> 88	from PUBLIC/anon/authenticated (internal primitive, never a PostgREST RPC) — which resolves an
> 89	existing secret by name and rotates it in place via `vault.update_secret` (COALESCE-keeps
> 90	name+description, re-encrypts only the value), else creates it; a `unique_violation` handler absorbs
> 91	the create race. All three encryption triggers now call this helper instead of `vault.create_secret`
> 92	and were pinned to `search_path=''`. The stored column keeps the SAME Vault UUID across rotations, so
> 93	`decrypted_*` views reflect the new value and no orphan secrets accumulate.
> 94	
> 95	**Material proof (2026-06-02, Management API, every test rolled back — no production mutation):**
> 96	- BEFORE: `user_api_keys` double-save of `wp_app_password` → `ERROR 23505 ... secrets_name_idx ...
> 97	  Key (name)=(user_api_keys_wp_app_password_<uid>) already exists` raised inside
> 98	  `trg_encrypt_user_api_keys`.
> 99	- AFTER (`user_api_keys`): same double-save → `{decrypted_wp:"wp-pass-BRAVO", secret_count:1,
> 100	  col_is_uuid_ref:true, sibling_groq_intact:true}`, no error.
> 101	- AFTER (`social_accounts`, real row `39ce0ebb-3579-481a-93ce-8a20759cd22e`): double-rotation of
> 102	  `access_token` → `{decrypted_access:"sa-BRAVO", secret_count:1}`, no error.
> 103	- (`meta_config` has 0 rows to exercise live; covered by the shared helper + source verification —
> 104	  all three triggers verified `calls_helper=true, calls_create_secret=false`.)
> 105	
> 106	**Residual nuance (not a defect):** the helper opens a per-call subtransaction (its `EXCEPTION` block)
> 107	only to absorb the rare concurrent-create race; the common rotate path takes the no-exception
> 108	SELECT→`update_secret` branch.
> 109	
> 110	## Tenant isolation on the masked-view INSTEAD OF triggers (hardened 2026-06-02)
> 111	
> ```

## 🤖 Claude *(16:57:34)*


## 🤖 Claude *(16:57:35)*

Tenho a estrutura completa. Vou adicionar uma seção dedicada às novas RPCs, espelhando o formato das seções de débito resolvido. Deixa eu pegar o fim exato do arquivo como âncora:

## 🤖 Claude *(16:57:36)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/credential-disconnect-clear.md",
  "offset": 124,
  "limit": 10
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 124	(`user_id=auth.uid()`) → `{inserted:1, decrypted:"my-own-token"}`; service_role with arbitrary
> 125	`user_id` → `{inserted:1}` (exempt). Every legit writer is service_role (edge OAuth/cron) or a client
> 126	writing its own row, so the guard breaks nothing.
> 127	
> ```

## 🤖 Claude *(16:57:39)*


## 🤖 Claude *(16:58:01)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/credential-disconnect-clear.md",
  "old_string": "`user_id` \u2192 `{inserted:1}` (exempt). Every legit writer is service_role (edge OAuth/cron) or a client\nwriting its own row, so the guard breaks nothing.",
  "new_string": "`user_id` \u2192 `{inserted:1}` (exempt). Every legit writer is service_role (edge OAuth/cron) or a client\nwriting its own row, so the guard breaks nothing.\n\n## Meta / social disconnect \u2014 orphaned-secret revocation (closed 2026-06-02)\n\n**Was:** disconnecting a Meta connection (`useMetaConfig.disconnect`) or a social account\n(`useSocialAccounts.disconnectAccount`) issued a plain `.delete()` through the masked view \u2192 the\nINSTEAD OF DELETE trigger only ran `DELETE FROM <base>_table WHERE id = OLD.id`. The encrypted token\ncolumns hold Vault secret references, so the base-row delete left the underlying Vault secret\n**orphaned** (retained plaintext, no owning row) \u2014 the same LGPD/retention gap `disconnect_wordpress()`\nclosed for WordPress, but for `meta_config` (`long_lived_token`, `pages`) and `social_accounts`\n(`access_token`, `refresh_token`). **Materially observed on prod:** the sole tenant had 0 rows in\n`meta_config_table` yet **12 orphaned Meta Vault secrets** (6\u00d7 `meta_config_long_lived_token_*` + 6\u00d7\n`meta_config_pages_*`) \u2014 residue of ~6 connect/disconnect cycles.\n\n**Fix:** migration `20260602160000_meta_social_disconnect_rpc.sql` adds two privileged RPCs mirroring\n`disconnect_wordpress()` (SECURITY DEFINER, `search_path=''`, fail-closed on NULL `auth.uid()` \u2192\n`28000`, EXECUTE granted to `authenticated` only):\n- `disconnect_meta()` \u2014 no params (`UNIQUE(user_id)` \u21d2 one row). Deletes the caller's row and revokes\n  `meta_config_long_lived_token_<id>` + `meta_config_pages_<id>`.\n- `disconnect_social(p_account_id uuid)` \u2014 deletes the caller's row with that id and revokes\n  `social_accounts_access_token_<id>` + `social_accounts_refresh_token_<id>`. A foreign / non-existent\n  id is a silent no-op (`SELECT \u2026 WHERE id = p_account_id AND user_id = auth.uid()` yields no row).\n\n**Tenant safety (key difference vs WordPress):** meta/social secret names are keyed by the **row id**,\nnot the `user_id`. Each Vault `DELETE` is double-bound \u2014 `id = <ref read from the caller's OWN row>`\n**AND** `name = '<prefix>_' || <caller's own row id>`. Because `id` is `PRIMARY KEY` on both base\ntables, the caller's own row id can never equal a victim's, so the name clause can never match a\nvictim's secret name \u2014 a planted foreign reference UUID can only ever no-op. (And the raw Vault UUID\nis never exposed to clients: token columns are masked, base-table SELECT is REVOKED from\n`authenticated`, `decrypted_*` is service_role-only \u2014 so the ref cannot even be learned.) The hooks\nwere switched from `.delete()` to `supabase.rpc('disconnect_meta')` / `rpc('disconnect_social',\n{ p_account_id })`. The migration also one-time revokes the already-orphaned secrets, provably\norphan-scoped (`NOT EXISTS` a base row whose `id::text = right(name,36)` \u2192 live connections preserved).\n\n**Material proof (2026-06-02, Management API):**\n- RPC suite (BEGIN/ROLLBACK, against the tenant's real rows): `disconnect_social` happy path \u2192 row\n  deleted **and** `social_accounts_access_token_<id>` revoked; foreign-id call by a different uid \u2192\n  no-op (victim row+secret intact); planted-ref attack (instagram secret UUID planted in facebook's\n  row) \u2192 instagram secret SURVIVED (name binding held); `disconnect_meta` happy path \u2192 row deleted and\n  **both** token+pages secrets revoked; unauthenticated call \u2192 `28000`. 5/5 PASS, zero residue.\n- Apply (committed): functions live (`SECURITY DEFINER`, `proconfig=search_path=\"\"`), EXECUTE granted\n  to `authenticated` / revoked from `anon`, the **12 orphaned Meta secrets revoked \u2192 0** (`meta_config_%`\n  count now 0), **3 live social secrets + 3 social rows intact**, migration recorded in\n  `schema_migrations`. `tsc` 0 errors \u00b7 238 tests pass \u00b7 served bundle contains both RPC calls.\n\n### Manual / LGPD-erasure equivalent\n```sql\n-- as a privileged role (service_role / Management API), for a given <uid>:\nSELECT public.disconnect_meta();                 -- if run within the user's JWT context, OR:\nDELETE FROM public.meta_config_table   WHERE user_id = '<uid>';\nDELETE FROM public.social_accounts_table WHERE user_id = '<uid>';\nDELETE FROM vault.secrets s\nWHERE s.name ~ '^(meta_config_(long_lived_token|pages)|social_accounts_(access_token|refresh_token))_[0-9a-f-]{36}$'\n  AND NOT EXISTS (SELECT 1 FROM public.meta_config_table m   WHERE m.id::text  = right(s.name,36))\n  AND NOT EXISTS (SELECT 1 FROM public.social_accounts_table sa WHERE sa.id::text = right(s.name,36));\n```"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/processes/credential-disconnect-clear.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:58:10)*


## 🤖 Claude *(16:58:12)*

SOP atualizado. Agora a **Key Files Reference** no `CLAUDE.md` (convenção do projeto — toda migration de credencial é listada). Vou ancorar logo após a entrada da `20260602150000`:

## 🤖 Claude *(16:58:12)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/CLAUDE.md",
  "offset": 316,
  "limit": 7
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 316	2. UI no `/dashboard/settings` (ou page dedicada como `/dashboard/affiliates`) com hook TanStack Query padrão (`useUserApiKeys` / `use<Service>Config`).
> 317	3. Lookup helper em `src/lib/<service>.ts` OU diretamente no edge function (padrão `process-affiliate-link:176-187`).
> 318	4. Telemetry em `infra_health_logs` com `service='<integration-name>'` em cada path (success + degraded + error).
> 319	5. SOP em `docs/processes/<integration>-credential-resolution.md` antes de qualquer código (Lei 2 Survival).
> 320	
> 321	**Anti-patterns proibidos:**
> 322	
> ```

## 🤖 Claude *(16:58:16)*


## 🤖 Claude *(16:58:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngrep -nE \"20260602150000_meta_social_instead_of_tenant_guard|Meta/social tenant guard\" CLAUDE.md",
  "description": "Find the tenant-guard Key Files entry line"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 429:| **Meta/social tenant guard (cross-tenant injection fix)** | `supabase/migrations/20260602150000_meta_social_instead_of_tenant_guard.sql` (porta o guard `auth.uid()` da `130000` pras INSTEAD OF de `meta_config`/`social_accounts` · `search_path=''` · service_role isento) |
> ```

## 🤖 Claude *(16:58:24)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/CLAUDE.md",
  "old_string": "| **Meta/social tenant guard (cross-tenant injection fix)** | `supabase/migrations/20260602150000_meta_social_instead_of_tenant_guard.sql` (porta o guard `auth.uid()` da `130000` pras INSTEAD OF de `meta_config`/`social_accounts` \u00b7 `search_path=''` \u00b7 service_role isento) |",
  "new_string": "| **Meta/social tenant guard (cross-tenant injection fix)** | `supabase/migrations/20260602150000_meta_social_instead_of_tenant_guard.sql` (porta o guard `auth.uid()` da `130000` pras INSTEAD OF de `meta_config`/`social_accounts` \u00b7 `search_path=''` \u00b7 service_role isento) |\n| **Meta/social disconnect RPC (orphaned-secret revocation)** | `supabase/migrations/20260602160000_meta_social_disconnect_rpc.sql` (`disconnect_meta()`/`disconnect_social(uuid)` espelham `disconnect_wordpress` \u2014 deletam linha + revogam segredo Vault \u00f3rf\u00e3o \u00b7 name-binding por `id` da linha + PK \u21d2 tenant-safe \u00b7 limpeza one-time de 12 \u00f3rf\u00e3os meta \u00b7 hooks `useMetaConfig`/`useSocialAccounts` migrados de `.delete()` p/ `.rpc()`) |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:58:39)*


## 🤖 Claude *(16:58:41)*

CLAUDE.md atualizado. Agora commits granulares seguindo a convenção do projeto (e minha memória: **nunca** `Co-Authored-By`, corpo orientado a milestone). Vou separar o fix de código da documentação. Status atual primeiro:

## 🤖 Claude *(16:58:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit reset -q HEAD . 2>/dev/null\ngit status --short",
  "description": "Show working tree status before granular commits"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>  M CLAUDE.md
>  M docs/processes/credential-disconnect-clear.md
>  M src/hooks/useMetaConfig.ts
>  M src/hooks/useSocialAccounts.ts
>  M src/integrations/supabase/types.ts
> ?? supabase/migrations/20260602160000_meta_social_disconnect_rpc.sql
> ```

## 🤖 Claude *(16:58:47)*


## 🤖 Claude *(16:58:48)*

Os 6 arquivos prontos. Commit 1 — o fix de código (migration + hooks + types):

## 🤖 Claude *(16:58:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add supabase/migrations/20260602160000_meta_social_disconnect_rpc.sql src/hooks/useMetaConfig.ts src/hooks/useSocialAccounts.ts src/integrations/supabase/types.ts\ngit commit -q -m \"fix(credentials): disconnect_meta/disconnect_social revogam o segredo Vault \u00f3rf\u00e3o\n\nDesconectar Meta ou uma conta social deletava s\u00f3 a linha base via INSTEAD OF\nDELETE e deixava o token plaintext \u00f3rf\u00e3o no Vault (12 segredos Meta \u00f3rf\u00e3os\nobservados em prod \u2014 res\u00edduo de ~6 ciclos connect/disconnect). Fecha o d\u00e9bito\nLGPD espelhando disconnect_wordpress: RPCs SECURITY DEFINER scoped a auth.uid()\nque deletam a linha E revogam o segredo. Name-binding por id-de-linha + PK \u21d2\nimposs\u00edvel revogar segredo de outro tenant. Hooks migrados de .delete() p/ rpc().\nMigration revoga os 12 \u00f3rf\u00e3os preexistentes (provadamente orphan-scoped).\" \necho \"commit1 exit=$?\"\ngit log --oneline -1",
  "description": "Commit the code fix (migration + hooks + types)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> commit1 exit=0
> 76bb9e3 fix(credentials): disconnect_meta/disconnect_social revogam o segredo Vault órfão
> ```

## 🤖 Claude *(16:58:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add docs/processes/credential-disconnect-clear.md CLAUDE.md\ngit commit -q -m \"docs(processes): SOP + Key Files do disconnect Meta/social (revoga\u00e7\u00e3o de \u00f3rf\u00e3o)\n\nDocumenta as RPCs disconnect_meta/disconnect_social no SOP de credential-disconnect\n(operator/sequence/verification/recovery + prova material 5/5 e a equival\u00eancia\nmanual p/ erasure LGPD) e registra a migration 20260602160000 na Key Files Reference.\"\necho \"commit2 exit=$?\"\ngit log --oneline -3",
  "description": "Commit docs (SOP + CLAUDE.md)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> commit2 exit=0
> 610e1f3 docs(processes): SOP + Key Files do disconnect Meta/social (revogação de órfão)
> 76bb9e3 fix(credentials): disconnect_meta/disconnect_social revogam o segredo Vault órfão
> 66859b0 chore(sprint): selo v6.20.2 — idempotência do Vault + guard de tenant meta/social
> ```

> **Tool Result (Unknown Tool)** - ✅ Success
>
> ```
> === working tree ===
> CLEAN
> 
> === HEAD vs origin ===
> 0	2
> 
> === memory file head ===
> 
> Desde `20260601000000_credential_encryption.sql` + `20260601000600_secure_definer_views.sql` (2026-06-01), as tabelas `user_api_keys`, `meta_config`, `social_accounts` viraram **VIEWS** (security-definer, com `WHERE auth.uid()=user_id OR service_role`) sobre `*_table` Vault-encriptadas. SELECT mostra `••••`; reais cifradas no Vault; edge fns leem `decrypted_*` (REVOKE de anon/authenticated, só service_role). Ver [[reference_user_api_keys_encrypted]] e [[reference_supabase_keys_migrated]].
> 
> **Gotchas ao ESCREVER:**
> - ❌ `.upsert()` / `{onConflict:'user_id'}` → **HTTP 400** `42P10 "no unique or exclusion constraint matching ON CONFLICT"` (views não têm constraint). Provado material 2026-06-02.
> - ✅ `.insert()` → roteia pelo INSTEAD OF INSERT. (Padrão em `useUserApiKeys.saveKeys`.) `meta_config`/`social_accounts` ramificam INSERT/UPDATE separado; seus hooks fazem `.update()` se existe / `.insert()` se não (`useMetaConfig`/`useAffiliateConfig`).
> - ❌ Setar coluna-segredo para `null` **NÃO limpa**: o INSTEAD OF faz `COALESCE(NULLIF(NEW.x,'••••'), base.x)` → null preserva (e esse guard é load-bearing: protege saves parciais). Para limpar de verdade → UPDATE direto na `*_table` via path privilegiado.
> 
> **FIX SELADO 2026-06-02 (SocialAccountsPage WP — antes era P0 aberto):**
> - Save: `.upsert`→`.insert` (`src/pages/SocialAccountsPage.tsx`). Disconnect: agora chama a RPC **`disconnect_wordpress()`** (`SECURITY DEFINER`, escopada a `auth.uid()`, `search_path=''`) — nula as 3 colunas WP na base table **e DELETA o segredo do Vault** (revogação real LGPD; delete amarrado a `id` **E** nome determinístico → tenant-safe). Migration `20260602120000_wordpress_disconnect_rpc.sql`. SOP: `docs/processes/credential-disconnect-clear.md`.
> 
> **⚠️ BUG PROFUNDO descoberto+corrigido 2026-06-02 (afetava TODOS os saves de credencial, não só WP):**
> ```

## 🤖 Claude *(16:59:08)*


## 🤖 Claude *(16:59:10)*

Ambos os commits caíram (`76bb9e3`, `610e1f3`). Verificação final do tree + atualizo a memória durável (o fato do pattern de disconnect/revogação é companheiro natural do que já registrei sobre `disconnect_wordpress`):

## 🤖 Claude *(16:59:12)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== working tree ===\"; git status --short || true; test -z \"$(git status --porcelain)\" && echo \"CLEAN\" || echo \"(residual)\"\necho \"\"; echo \"=== HEAD vs origin ===\"; git rev-list --left-right --count origin/main...HEAD\necho \"\"; echo \"=== memory file head ===\"; sed -n '1,20p' /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/reference_encrypted_views_write_pattern.md 2>/dev/null | tail -12",
  "description": "Verify clean tree and read memory file"
}
```

## 🤖 Claude *(16:59:17)*


## 🤖 Claude *(16:59:18)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/reference_encrypted_views_write_pattern.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	---
> 2	name: reference_encrypted_views_write_pattern
> 3	description: "user_api_keys/meta_config/social_accounts são VIEWS Vault-mascaradas — escreva com .insert(); null não limpa (use RPC); o INSTEAD OF do user_api_keys NÃO pode usar INSERT...ON CONFLICT (double-fire 23505)"
> 4	metadata:
> 5	  node_type: memory
> 6	  type: reference
> 7	  originSessionId: d4434afb-c259-4270-a01a-03d85ba37719
> 8	---
> 9	
> 10	Desde `20260601000000_credential_encryption.sql` + `20260601000600_secure_definer_views.sql` (2026-06-01), as tabelas `user_api_keys`, `meta_config`, `social_accounts` viraram **VIEWS** (security-definer, com `WHERE auth.uid()=user_id OR service_role`) sobre `*_table` Vault-encriptadas. SELECT mostra `••••`; reais cifradas no Vault; edge fns leem `decrypted_*` (REVOKE de anon/authenticated, só service_role). Ver [[reference_user_api_keys_encrypted]] e [[reference_supabase_keys_migrated]].
> 11	
> 12	**Gotchas ao ESCREVER:**
> 13	- ❌ `.upsert()` / `{onConflict:'user_id'}` → **HTTP 400** `42P10 "no unique or exclusion constraint matching ON CONFLICT"` (views não têm constraint). Provado material 2026-06-02.
> 14	- ✅ `.insert()` → roteia pelo INSTEAD OF INSERT. (Padrão em `useUserApiKeys.saveKeys`.) `meta_config`/`social_accounts` ramificam INSERT/UPDATE separado; seus hooks fazem `.update()` se existe / `.insert()` se não (`useMetaConfig`/`useAffiliateConfig`).
> 15	- ❌ Setar coluna-segredo para `null` **NÃO limpa**: o INSTEAD OF faz `COALESCE(NULLIF(NEW.x,'••••'), base.x)` → null preserva (e esse guard é load-bearing: protege saves parciais). Para limpar de verdade → UPDATE direto na `*_table` via path privilegiado.
> 16	
> 17	**FIX SELADO 2026-06-02 (SocialAccountsPage WP — antes era P0 aberto):**
> 18	- Save: `.upsert`→`.insert` (`src/pages/SocialAccountsPage.tsx`). Disconnect: agora chama a RPC **`disconnect_wordpress()`** (`SECURITY DEFINER`, escopada a `auth.uid()`, `search_path=''`) — nula as 3 colunas WP na base table **e DELETA o segredo do Vault** (revogação real LGPD; delete amarrado a `id` **E** nome determinístico → tenant-safe). Migration `20260602120000_wordpress_disconnect_rpc.sql`. SOP: `docs/processes/credential-disconnect-clear.md`.
> 19	
> 20	**⚠️ BUG PROFUNDO descoberto+corrigido 2026-06-02 (afetava TODOS os saves de credencial, não só WP):**
> 21	O `trg_instead_of_user_api_keys` roteava INSERT **e** UPDATE do cliente por um único `INSERT ... ON CONFLICT (user_id) DO UPDATE`. Numa linha **pré-existente** o Postgres dispara o BEFORE-trigger de encriptação **2×** numa só statement (fase INSERT cria o segredo Vault; fase UPDATE chama `vault.create_secret` de novo com o mesmo nome determinístico → **`23505`** `secrets_name_idx`). E `.update()` carrega o sentinela `••••` mascarado nos campos não-tocados → a fase INSERT tenta cifrar `••••` → colide com o segredo já existente (ex.: groq). Efeito: connect/save quebrado p/ qualquer user com linha já existente (só o 1º insert all-fields em linha nova passava). Provado material (T1/T3/T4) e via `vault.create_secret` = INSERT puro sem ON CONFLICT.
> 22	- **Fix:** reescrever só o `trg_instead_of_user_api_keys` p/ **UPDATE-first / INSERT-if-NOT FOUND** (dispara encrypt 1×; igual aos irmãos meta/social que já ramificavam). Migration `20260602130000_fix_user_api_keys_instead_of_double_fire.sql`. Também: `wp_site_url`/`wp_username` viraram `COALESCE(NEW,base)` (não zeram em save parcial) + **guard de tenant** (`auth.role()<>'service_role' AND NEW.user_id<>auth.uid()` → 42501) que fecha uma escrita cross-tenant que o ON CONFLICT antigo só mascarava com o crash. Passou `/security-review` (veredito SAFE, guard não-burlável).
> 23	
> 24	**FIX SELADO 2026-06-02 (idempotência do encrypt trigger — a dívida residual acima):** o `trg_encrypt_user_api_keys` (+ irmãos meta/social) chamava `vault.create_secret` **incondicionalmente** → editar um segredo p/ valor NOVO com o segredo de mesmo nome ainda presente = **23505 `secrets_name_idx`** (reproduzido material C4: `trg_encrypt_user_api_keys() line 72`). **Conserto:** helper `public.vault_upsert_secret(value,name,desc)` (SECURITY DEFINER, `search_path=''`, **EXECUTE revogado** de PUBLIC/anon/authenticated → não é RPC alcançável) resolve por nome → `vault.update_secret` in-place (COALESCE-keep de nome/desc) senão `create_secret`; +fallback `unique_violation` p/ a corrida. As 3 encrypt triggers passam a chamá-lo (e ganham `search_path=''`). Migration `20260602140000_vault_upsert_secret_idempotent_encrypt.sql`. Prova material (Mgmt API, tudo rolled-back): antes 23505 / depois user_api_keys `{decrypted:"wp-pass-BRAVO",secret_count:1}` + social_accounts (linha real) `{decrypted:"sa-BRAVO",secret_count:1}`. Coluna mantém o MESMO uuid Vault entre rotações (sem órfãos). Passou `/security-review`.
> 25	
> 26	**FIX SELADO 2026-06-02 (gap pré-existente achado no /security-review da `140000`):** `trg_instead_of_meta_config`/`trg_instead_of_social_accounts` **não tinham o guard de tenant** que o `user_api_keys` ganhou na `130000` → injeção cross-tenant (INSERT com `user_id` spoofado + `id` fresco cria linha de credencial em nome da vítima; o PK em `id` só fecha o *overwrite* de id-colidente). **Conserto:** migration `20260602150000_meta_social_instead_of_tenant_guard.sql` porta o guard `auth.role()<>'service_role' AND NEW.user_id<>auth.uid()` (42501) pras branches INSERT+UPDATE das 2 triggers irmãs + `search_path=''`, recriadas VERBATIM do `pg_get_functiondef` live (sentinelas `••••` byte-exatas). Prova material (rolled-back): ANTES atacante `sub=1111` injetou `meta_config` da vítima `ada39fae` (`decrypted_token:"INJECTED-BY-ATTACKER"`); DEPOIS 42501 nas 2 tabelas, self-insert legítimo OK (`decrypted:"my-own-token"`), service_role isento OK. Todo writer legítimo é service_role (edge OAuth/cron) ou cliente escrevendo a própria linha (`useMetaConfig`/nenhum em social). Passou `/security-review` (claim `service_role` não-forjável: vem do JWT assinado). ⚠️ **DELETE branch fica SEM guard de propósito** — a view mascarada filtra DELETE/UPDATE/SELECT por `auth.uid()=user_id`; só INSERT escapa do WHERE.
> 27	
> ```

## 🤖 Claude *(16:59:24)*


## 🤖 Claude *(16:59:25)*

A memória cobre os fixes irmãos mas não o débito de órfão no disconnect meta/social. Adiciono uma entrada concisa (fato durável — evita reinvestigar "disconnect vaza segredo?" no futuro):

## 🤖 Claude *(16:59:39)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/reference_encrypted_views_write_pattern.md",
  "old_string": "Todo writer leg\u00edtimo \u00e9 service_role (edge OAuth/cron) ou cliente escrevendo a pr\u00f3pria linha (`useMetaConfig`/nenhum em social). Passou `/security-review` (claim `service_role` n\u00e3o-forj\u00e1vel: vem do JWT assinado). \u26a0\ufe0f **DELETE branch fica SEM guard de prop\u00f3sito** \u2014 a view mascarada filtra DELETE/UPDATE/SELECT por `auth.uid()=user_id`; s\u00f3 INSERT escapa do WHERE.",
  "new_string": "Todo writer leg\u00edtimo \u00e9 service_role (edge OAuth/cron) ou cliente escrevendo a pr\u00f3pria linha (`useMetaConfig`/nenhum em social). Passou `/security-review` (claim `service_role` n\u00e3o-forj\u00e1vel: vem do JWT assinado). \u26a0\ufe0f **DELETE branch fica SEM guard de prop\u00f3sito** \u2014 a view mascarada filtra DELETE/UPDATE/SELECT por `auth.uid()=user_id`; s\u00f3 INSERT escapa do WHERE.\n\n**FIX SELADO 2026-06-02 (d\u00e9bito de SEGREDO \u00d3RF\u00c3O no disconnect meta/social \u2014 companheiro do `disconnect_wordpress`):** desconectar Meta (`useMetaConfig.disconnect`) ou social (`useSocialAccounts.disconnectAccount`) fazia `.delete()` pela view \u2192 INSTEAD OF DELETE s\u00f3 apaga a linha base, **deixando o segredo Vault \u00f3rf\u00e3o** (token plaintext retido, sem linha dona). Material em prod: tenant tinha **0 linhas meta mas 12 segredos \u00f3rf\u00e3os** (`meta_config_long_lived_token_*`/`_pages_*`). **Conserto:** migration `20260602160000_meta_social_disconnect_rpc.sql` adiciona `disconnect_meta()` (sem param) e `disconnect_social(p_account_id uuid)` espelhando `disconnect_wordpress` (SECURITY DEFINER, `search_path=''`, fail-closed 28000, EXECUTE s\u00f3 authenticated) \u2014 deletam a linha E revogam o segredo. \u26a0\ufe0f **Diferen\u00e7a do WP:** nome do segredo meta/social \u00e9 keyed por **`id` da linha** (n\u00e3o `user_id`); o delete \u00e9 double-bound (`id=ref-da-pr\u00f3pria-linha` **E** `name='<prefix>_'||id-da-pr\u00f3pria-linha`) e como `id` \u00e9 PK, o id do atacante nunca iguala o da v\u00edtima \u2192 name-binding tenant-safe (+ o uuid bruto nunca vaza ao cliente). Migration tb revoga os 12 \u00f3rf\u00e3os preexistentes (orphan-scoped: `NOT EXISTS` linha base via `right(name,36)`). Hooks migrados `.delete()`\u2192`.rpc()`; `types.ts` regenerado (3 entradas: as 2 RPCs + `vault_upsert_secret`). Prova material: su\u00edte 5/5 (happy meta+social, foreign-id no-op, planted-ref name-binding aguenta, unauth 28000) + p\u00f3s-apply 12\u21920 \u00f3rf\u00e3os / 3 vivos intactos. Passou `/security-review` (SAFE 9/10). Commits `76bb9e3`+`610e1f3`."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/reference_encrypted_views_write_pattern.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:59:59)*


## 🤖 Claude *(17:00:00)*

Memória atualizada (entrada de fix selado, companheira da do `disconnect_wordpress`). Verificação final do estado git:

## 🤖 Claude *(17:00:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== working tree ===\"; test -z \"$(git status --porcelain)\" && echo \"CLEAN\" || git status --short\necho \"\"; echo \"=== last 3 commits ===\"; git log --oneline -3\necho \"\"; echo \"=== HEAD vs origin/main (commits NOT yet pushed) ===\"; git rev-list --left-right --count origin/main...HEAD | awk '{print \"behind origin: \"$1\" \u00b7 ahead of origin: \"$2}'",
  "description": "Final git state confirmation"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === working tree ===
> CLEAN
> 
> === last 3 commits ===
> 610e1f3 docs(processes): SOP + Key Files do disconnect Meta/social (revogação de órfão)
> 76bb9e3 fix(credentials): disconnect_meta/disconnect_social revogam o segredo Vault órfão
> 66859b0 chore(sprint): selo v6.20.2 — idempotência do Vault + guard de tenant meta/social
> 
> === HEAD vs origin/main (commits NOT yet pushed) ===
> behind origin: 0 · ahead of origin: 2
> ```

---

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-01 - agent-af11d6fa76341891b]]
> * **Próxima Sessão**: [[2026-06-02 - Fix WordPress credentials save and disconnect in SocialAccountsPage]]
%% --- TIMELINE END --- %%

# Session agent-a3ce1ca5fbac32bdc
**Date:** 2026-06-30 | **Session ID:** `agent-a3ce1ca5fbac32bdc`

---

## 👤 User *(03:36:54)*

You are a senior security engineer doing a FOCUSED security review of NEW untracked changes in the repo /home/gcrUX/htdocs/constellation-orchestra. Read the files yourself.

SCOPE (review ONLY these — the docs/bok/*.md are markdown, EXCLUDED):
1. supabase/migrations/20260630000000_user_api_keys_avatar_byok.sql  (THE security-relevant file)
2. scripts/seed-avatar-clone-ai-bok-seal.ts

CONTEXT: file (1) adds 3 per-user BYOK credential columns (hedra_api_key, cartesia_api_key, fal_api_key) to the Vault-encrypted user_api_keys machinery. It is intended to MIRROR VERBATIM the already-in-production, already-security-reviewed precedent supabase/migrations/20260622210000_user_api_keys_rapidapi_channel.sql, adding the 3 new columns at the end of each of the 5 sections (base columns, encrypt trigger, masked view, INSTEAD OF trigger, decrypted view). READ the precedent (20260622210000) and DIFF the new migration against it — your job is to confirm the new columns follow the EXACT vetted pattern and introduce NO deviation that breaks tenant isolation, Vault encryption, search_path hardening, or the service-role-only decrypted view.

Specifically verify, for EACH of the 3 new columns:
- encrypt trigger block: SECURITY DEFINER + search_path='' preserved; uses vault_upsert_secret (no dynamic SQL); UUID-already-encrypted guard present.
- masked public view: column masked as '••••••••••••'; the WHERE (auth.uid()=user_id OR service_role) tenant isolation intact.
- INSTEAD OF trigger: tenant guard (auth.uid() cross-tenant → 42501) intact; UPDATE-first COALESCE(NULLIF(...,'••••••••••••'),...) pattern (no double-fire); INSERT column list + VALUES include the new columns.
- decrypted view: COALESCE + LEFT JOIN vault.decrypted_secrets with the UUID regex+::uuid cast; REVOKE from PUBLIC/anon/authenticated + GRANT SELECT only to service_role intact.

For file (2): confirm it uses SB_SECRET_KEY from env (not hardcoded), no untrusted input, no injection.

Apply these EXCLUSIONS (do NOT report): DoS/resource exhaustion; secrets-on-disk; rate limiting; lack of hardening; theoretical races; outdated deps; findings in markdown docs; log spoofing; client-side checks; SSRF path-only.

Report ONLY HIGH/MEDIUM findings where you are >80% confident of a CONCRETE exploitable vulnerability NEWLY introduced by these changes (not pre-existing). For each finding give: file:line, severity, category, description, exploit scenario, fix, and a confidence score 1-10 (only report >=8). If the migration faithfully mirrors the vetted precedent with no security-relevant deviation, say so explicitly and return "NO FINDINGS (confidence X)". Output a concise markdown report.

## 🤖 Claude *(03:36:57)*

I'll review the two files against the vetted precedent. Let me start by reading all relevant files.

## 🤖 Claude *(03:36:58)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260630000000_user_api_keys_avatar_byok.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: per-user Avatar/Clone AI BYOK — hedra/cartesia/fal (Fatia 1 do módulo avatar-clone-ai).
> 2	-- BoK SSOT: docs/bok/avatar-clone-ai/ (FR-AC-001.. — BYOK Modelo A PURO per-user). API Tenancy Model (CLAUDE.md).
> 3	--
> 4	-- Decisão Sovereign 2026-06-29 (programa "Gabriel AI"): motores avatar self-serve per-user = Hedra Character-3
> 5	-- (default), OmniHuman via fal.ai, Higgsfield; voz = ElevenLabs/Cartesia. elevenlabs_api_key + higgsfield_api_key
> 6	-- JÁ EXISTEM (reusados). Magnific = conta-org INTERNA (chave organizacional, NÃO per-user → sem coluna).
> 7	-- HeyGen = partnership futuro (fora). INVARIANTE: nunca conta-mestra (=service bureau proibido por ToS).
> 8	--
> 9	-- Reproduz o ÚLTIMO live def VERBATIM (20260622210000_user_api_keys_rapidapi_channel.sql) + 3 colunas no FIM:
> 10	-- encrypt trigger usa vault_upsert_secret idempotente (20260602140000); INSTEAD OF é UPDATE-first + tenant guard
> 11	-- (20260602130000); search_path='' preservado. Aditivo: views acrescentam as colunas novas no FIM.
> 12	
> 13	-- ── 1. base columns ─────────────────────────────────────────────────────────────────────────────
> 14	ALTER TABLE public.user_api_keys_table ADD COLUMN IF NOT EXISTS hedra_api_key text;
> 15	ALTER TABLE public.user_api_keys_table ADD COLUMN IF NOT EXISTS cartesia_api_key text;
> 16	ALTER TABLE public.user_api_keys_table ADD COLUMN IF NOT EXISTS fal_api_key text;
> 17	COMMENT ON COLUMN public.user_api_keys_table.hedra_api_key
> 18	  IS 'Per-user Hedra Character-3 API key (BYOK Modelo A) — default avatar talking-head motor. Vault-encrypted at rest. NULL → 402 hedra_not_configured.';
> 19	COMMENT ON COLUMN public.user_api_keys_table.cartesia_api_key
> 20	  IS 'Per-user Cartesia Sonic API key (BYOK Modelo A) — real-time PT-BR voice clone. Vault-encrypted at rest. NULL → 402 cartesia_not_configured.';
> 21	COMMENT ON COLUMN public.user_api_keys_table.fal_api_key
> 22	  IS 'Per-user fal.ai API key (BYOK Modelo A) — OmniHuman talking-head motor. Vault-encrypted at rest. NULL → 402 fal_not_configured.';
> 23	
> 24	-- ── 2. encrypt trigger (live verbatim + hedra/cartesia/fal; idempotent vault_upsert_secret) ──────
> 25	CREATE OR REPLACE FUNCTION public.trg_encrypt_user_api_keys()
> 26	 RETURNS trigger
> 27	 LANGUAGE plpgsql
> 28	 SECURITY DEFINER
> 29	 SET search_path TO ''
> 30	AS $function$
> 31	DECLARE
> 32	  v_id UUID;
> 33	BEGIN
> 34	  IF NEW.groq_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.groq_api_key IS DISTINCT FROM OLD.groq_api_key) THEN
> 35	    IF NEW.groq_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 36	      v_id := public.vault_upsert_secret(NEW.groq_api_key, 'user_api_keys_groq_api_key_' || NEW.user_id::text, 'Groq API Key'); NEW.groq_api_key = v_id::text;
> 37	    END IF;
> 38	  END IF;
> 39	  IF NEW.openrouter_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openrouter_api_key IS DISTINCT FROM OLD.openrouter_api_key) THEN
> 40	    IF NEW.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 41	      v_id := public.vault_upsert_secret(NEW.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || NEW.user_id::text, 'OpenRouter API Key'); NEW.openrouter_api_key = v_id::text;
> 42	    END IF;
> 43	  END IF;
> 44	  IF NEW.openai_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openai_api_key IS DISTINCT FROM OLD.openai_api_key) THEN
> 45	    IF NEW.openai_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 46	      v_id := public.vault_upsert_secret(NEW.openai_api_key, 'user_api_keys_openai_api_key_' || NEW.user_id::text, 'OpenAI API Key'); NEW.openai_api_key = v_id::text;
> 47	    END IF;
> 48	  END IF;
> 49	  IF NEW.elevenlabs_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.elevenlabs_api_key IS DISTINCT FROM OLD.elevenlabs_api_key) THEN
> 50	    IF NEW.elevenlabs_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 51	      v_id := public.vault_upsert_secret(NEW.elevenlabs_api_key, 'user_api_keys_elevenlabs_api_key_' || NEW.user_id::text, 'ElevenLabs API Key'); NEW.elevenlabs_api_key = v_id::text;
> 52	    END IF;
> 53	  END IF;
> 54	  IF NEW.google_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.google_api_key IS DISTINCT FROM OLD.google_api_key) THEN
> 55	    IF NEW.google_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 56	      v_id := public.vault_upsert_secret(NEW.google_api_key, 'user_api_keys_google_api_key_' || NEW.user_id::text, 'Google API Key'); NEW.google_api_key = v_id::text;
> 57	    END IF;
> 58	  END IF;
> 59	  IF NEW.nanobana_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.nanobana_api_key IS DISTINCT FROM OLD.nanobana_api_key) THEN
> 60	    IF NEW.nanobana_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 61	      v_id := public.vault_upsert_secret(NEW.nanobana_api_key, 'user_api_keys_nanobana_api_key_' || NEW.user_id::text, 'Nanobana API Key'); NEW.nanobana_api_key = v_id::text;
> 62	    END IF;
> 63	  END IF;
> 64	  IF NEW.seedance_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.seedance_api_key IS DISTINCT FROM OLD.seedance_api_key) THEN
> 65	    IF NEW.seedance_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 66	      v_id := public.vault_upsert_secret(NEW.seedance_api_key, 'user_api_keys_seedance_api_key_' || NEW.user_id::text, 'Seedance API Key'); NEW.seedance_api_key = v_id::text;
> 67	    END IF;
> 68	  END IF;
> 69	  IF NEW.wp_app_password IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.wp_app_password IS DISTINCT FROM OLD.wp_app_password) THEN
> 70	    IF NEW.wp_app_password ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 71	      v_id := public.vault_upsert_secret(NEW.wp_app_password, 'user_api_keys_wp_app_password_' || NEW.user_id::text, 'WordPress App Password'); NEW.wp_app_password = v_id::text;
> 72	    END IF;
> 73	  END IF;
> 74	  IF NEW.replicate_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.replicate_api_key IS DISTINCT FROM OLD.replicate_api_key) THEN
> 75	    IF NEW.replicate_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 76	      v_id := public.vault_upsert_secret(NEW.replicate_api_key, 'user_api_keys_replicate_api_key_' || NEW.user_id::text, 'Replicate API Key'); NEW.replicate_api_key = v_id::text;
> 77	    END IF;
> 78	  END IF;
> 79	  IF NEW.higgsfield_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.higgsfield_api_key IS DISTINCT FROM OLD.higgsfield_api_key) THEN
> 80	    IF NEW.higgsfield_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 81	      v_id := public.vault_upsert_secret(NEW.higgsfield_api_key, 'user_api_keys_higgsfield_api_key_' || NEW.user_id::text, 'Higgsfield API Key'); NEW.higgsfield_api_key = v_id::text;
> 82	    END IF;
> 83	  END IF;
> 84	  IF NEW.higgsfield_api_key_secret IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.higgsfield_api_key_secret IS DISTINCT FROM OLD.higgsfield_api_key_secret) THEN
> 85	    IF NEW.higgsfield_api_key_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 86	      v_id := public.vault_upsert_secret(NEW.higgsfield_api_key_secret, 'user_api_keys_higgsfield_api_key_secret_' || NEW.user_id::text, 'Higgsfield API Key Secret'); NEW.higgsfield_api_key_secret = v_id::text;
> 87	    END IF;
> 88	  END IF;
> 89	  IF NEW.apify_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.apify_token IS DISTINCT FROM OLD.apify_token) THEN
> 90	    IF NEW.apify_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 91	      v_id := public.vault_upsert_secret(NEW.apify_token, 'user_api_keys_apify_token_' || NEW.user_id::text, 'Apify Token'); NEW.apify_token = v_id::text;
> 92	    END IF;
> 93	  END IF;
> 94	  IF NEW.resend_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.resend_api_key IS DISTINCT FROM OLD.resend_api_key) THEN
> 95	    IF NEW.resend_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 96	      v_id := public.vault_upsert_secret(NEW.resend_api_key, 'user_api_keys_resend_api_key_' || NEW.user_id::text, 'Resend API Key'); NEW.resend_api_key = v_id::text;
> 97	    END IF;
> 98	  END IF;
> 99	  IF NEW.firecrawl_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.firecrawl_api_key IS DISTINCT FROM OLD.firecrawl_api_key) THEN
> 100	    IF NEW.firecrawl_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 101	      v_id := public.vault_upsert_secret(NEW.firecrawl_api_key, 'user_api_keys_firecrawl_api_key_' || NEW.user_id::text, 'Firecrawl API Key'); NEW.firecrawl_api_key = v_id::text;
> 102	    END IF;
> 103	  END IF;
> 104	  IF NEW.rapidapi_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.rapidapi_key IS DISTINCT FROM OLD.rapidapi_key) THEN
> 105	    IF NEW.rapidapi_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 106	      v_id := public.vault_upsert_secret(NEW.rapidapi_key, 'user_api_keys_rapidapi_key_' || NEW.user_id::text, 'RapidAPI Key'); NEW.rapidapi_key = v_id::text;
> 107	    END IF;
> 108	  END IF;
> 109	  -- hedra_api_key (NEW — avatar-clone-ai BYOK, default talking-head motor)
> 110	  IF NEW.hedra_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.hedra_api_key IS DISTINCT FROM OLD.hedra_api_key) THEN
> 111	    IF NEW.hedra_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 112	      v_id := public.vault_upsert_secret(NEW.hedra_api_key, 'user_api_keys_hedra_api_key_' || NEW.user_id::text, 'Hedra API Key'); NEW.hedra_api_key = v_id::text;
> 113	    END IF;
> 114	  END IF;
> 115	  -- cartesia_api_key (NEW — avatar-clone-ai BYOK, real-time voice clone)
> 116	  IF NEW.cartesia_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.cartesia_api_key IS DISTINCT FROM OLD.cartesia_api_key) THEN
> 117	    IF NEW.cartesia_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 118	      v_id := public.vault_upsert_secret(NEW.cartesia_api_key, 'user_api_keys_cartesia_api_key_' || NEW.user_id::text, 'Cartesia API Key'); NEW.cartesia_api_key = v_id::text;
> 119	    END IF;
> 120	  END IF;
> 121	  -- fal_api_key (NEW — avatar-clone-ai BYOK, OmniHuman motor)
> 122	  IF NEW.fal_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.fal_api_key IS DISTINCT FROM OLD.fal_api_key) THEN
> 123	    IF NEW.fal_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> 124	      v_id := public.vault_upsert_secret(NEW.fal_api_key, 'user_api_keys_fal_api_key_' || NEW.user_id::text, 'fal.ai API Key'); NEW.fal_api_key = v_id::text;
> 125	    END IF;
> 126	  END IF;
> 127	  RETURN NEW;
> 128	END;
> 129	$function$;
> 130	
> 131	-- ── 3. masked public view (live verbatim + hedra/cartesia/fal masked, appended at END) ───────────
> 132	CREATE OR REPLACE VIEW public.user_api_keys AS
> 133	SELECT
> 134	  user_id, created_at, updated_at, pref_audio_provider, pref_image_provider, pref_video_provider,
> 135	  wp_site_url, wp_username, pref_ai_model,
> 136	  CASE WHEN groq_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS groq_api_key,
> 137	  CASE WHEN openrouter_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS openrouter_api_key,
> 138	  CASE WHEN openai_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS openai_api_key,
> 139	  CASE WHEN elevenlabs_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS elevenlabs_api_key,
> 140	  CASE WHEN google_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS google_api_key,
> 141	  CASE WHEN nanobana_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS nanobana_api_key,
> 142	  CASE WHEN seedance_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS seedance_api_key,
> 143	  CASE WHEN wp_app_password IS NOT NULL THEN '••••••••••••' ELSE NULL END AS wp_app_password,
> 144	  CASE WHEN replicate_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS replicate_api_key,
> 145	  CASE WHEN higgsfield_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS higgsfield_api_key,
> 146	  CASE WHEN higgsfield_api_key_secret IS NOT NULL THEN '••••••••••••' ELSE NULL END AS higgsfield_api_key_secret,
> 147	  CASE WHEN apify_token IS NOT NULL THEN '••••••••••••' ELSE NULL END AS apify_token,
> 148	  CASE WHEN resend_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS resend_api_key,
> 149	  CASE WHEN firecrawl_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS firecrawl_api_key,
> 150	  CASE WHEN rapidapi_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS rapidapi_key,
> 151	  CASE WHEN hedra_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS hedra_api_key,
> 152	  CASE WHEN cartesia_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS cartesia_api_key,
> 153	  CASE WHEN fal_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS fal_api_key
> 154	FROM public.user_api_keys_table
> 155	WHERE (auth.uid() = user_id OR auth.role() = 'service_role');
> 156	GRANT SELECT, INSERT, UPDATE, DELETE ON public.user_api_keys TO anon, authenticated;
> 157	
> 158	-- ── 4. INSTEAD OF trigger (live verbatim + hedra/cartesia/fal in UPDATE-first/INSERT, tenant-guarded) ──
> 159	CREATE OR REPLACE FUNCTION public.trg_instead_of_user_api_keys()
> 160	 RETURNS trigger
> 161	 LANGUAGE plpgsql
> 162	 SECURITY DEFINER
> 163	 SET search_path TO ''
> 164	AS $function$
> 165	BEGIN
> 166	  IF TG_OP = 'DELETE' THEN
> 167	    DELETE FROM public.user_api_keys_table WHERE user_id = OLD.user_id;
> 168	    RETURN OLD;
> 169	  ELSIF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
> 170	    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN
> 171	      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';
> 172	    END IF;
> 173	    UPDATE public.user_api_keys_table SET
> 174	      groq_api_key              = COALESCE(NULLIF(NEW.groq_api_key, '••••••••••••'), public.user_api_keys_table.groq_api_key),
> 175	      openrouter_api_key        = COALESCE(NULLIF(NEW.openrouter_api_key, '••••••••••••'), public.user_api_keys_table.openrouter_api_key),
> 176	      openai_api_key            = COALESCE(NULLIF(NEW.openai_api_key, '••••••••••••'), public.user_api_keys_table.openai_api_key),
> 177	      pref_audio_provider       = COALESCE(NEW.pref_audio_provider, public.user_api_keys_table.pref_audio_provider),
> 178	      pref_image_provider       = COALESCE(NEW.pref_image_provider, public.user_api_keys_table.pref_image_provider),
> 179	      pref_video_provider       = COALESCE(NEW.pref_video_provider, public.user_api_keys_table.pref_video_provider),
> 180	      elevenlabs_api_key        = COALESCE(NULLIF(NEW.elevenlabs_api_key, '••••••••••••'), public.user_api_keys_table.elevenlabs_api_key),
> 181	      google_api_key            = COALESCE(NULLIF(NEW.google_api_key, '••••••••••••'), public.user_api_keys_table.google_api_key),
> 182	      nanobana_api_key          = COALESCE(NULLIF(NEW.nanobana_api_key, '••••••••••••'), public.user_api_keys_table.nanobana_api_key),
> 183	      seedance_api_key          = COALESCE(NULLIF(NEW.seedance_api_key, '••••••••••••'), public.user_api_keys_table.seedance_api_key),
> 184	      wp_site_url               = COALESCE(NEW.wp_site_url, public.user_api_keys_table.wp_site_url),
> 185	      wp_username               = COALESCE(NEW.wp_username, public.user_api_keys_table.wp_username),
> 186	      wp_app_password           = COALESCE(NULLIF(NEW.wp_app_password, '••••••••••••'), public.user_api_keys_table.wp_app_password),
> 187	      pref_ai_model             = COALESCE(NEW.pref_ai_model, public.user_api_keys_table.pref_ai_model),
> 188	      replicate_api_key         = COALESCE(NULLIF(NEW.replicate_api_key, '••••••••••••'), public.user_api_keys_table.replicate_api_key),
> 189	      higgsfield_api_key        = COALESCE(NULLIF(NEW.higgsfield_api_key, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key),
> 190	      higgsfield_api_key_secret = COALESCE(NULLIF(NEW.higgsfield_api_key_secret, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key_secret),
> 191	      apify_token               = COALESCE(NULLIF(NEW.apify_token, '••••••••••••'), public.user_api_keys_table.apify_token),
> 192	      resend_api_key            = COALESCE(NULLIF(NEW.resend_api_key, '••••••••••••'), public.user_api_keys_table.resend_api_key),
> 193	      firecrawl_api_key         = COALESCE(NULLIF(NEW.firecrawl_api_key, '••••••••••••'), public.user_api_keys_table.firecrawl_api_key),
> 194	      rapidapi_key              = COALESCE(NULLIF(NEW.rapidapi_key, '••••••••••••'), public.user_api_keys_table.rapidapi_key),
> 195	      hedra_api_key             = COALESCE(NULLIF(NEW.hedra_api_key, '••••••••••••'), public.user_api_keys_table.hedra_api_key),
> 196	      cartesia_api_key          = COALESCE(NULLIF(NEW.cartesia_api_key, '••••••••••••'), public.user_api_keys_table.cartesia_api_key),
> 197	      fal_api_key               = COALESCE(NULLIF(NEW.fal_api_key, '••••••••••••'), public.user_api_keys_table.fal_api_key),
> 198	      updated_at                = now()
> 199	    WHERE user_id = NEW.user_id;
> 200	    IF NOT FOUND THEN
> 201	      INSERT INTO public.user_api_keys_table (
> 202	        user_id, groq_api_key, openrouter_api_key, openai_api_key, pref_audio_provider, pref_image_provider, pref_video_provider, elevenlabs_api_key, google_api_key, nanobana_api_key, seedance_api_key, wp_site_url, wp_username, wp_app_password, pref_ai_model, replicate_api_key, higgsfield_api_key, higgsfield_api_key_secret, apify_token, resend_api_key, firecrawl_api_key, rapidapi_key, hedra_api_key, cartesia_api_key, fal_api_key
> 203	      ) VALUES (
> 204	        NEW.user_id, NEW.groq_api_key, NEW.openrouter_api_key, NEW.openai_api_key, NEW.pref_audio_provider, NEW.pref_image_provider, NEW.pref_video_provider, NEW.elevenlabs_api_key, NEW.google_api_key, NEW.nanobana_api_key, NEW.seedance_api_key, NEW.wp_site_url, NEW.wp_username, NEW.wp_app_password, NEW.pref_ai_model, NEW.replicate_api_key, NEW.higgsfield_api_key, NEW.higgsfield_api_key_secret, NEW.apify_token, NEW.resend_api_key, NEW.firecrawl_api_key, NEW.rapidapi_key, NEW.hedra_api_key, NEW.cartesia_api_key, NEW.fal_api_key
> 205	      );
> 206	    END IF;
> 207	    RETURN NEW;
> 208	  END IF;
> 209	  RETURN NULL;
> 210	END;
> 211	$function$;
> 212	
> 213	-- ── 5. decrypted view (service_role only; live verbatim + hedra/cartesia/fal COALESCE + join at END) ──
> 214	CREATE OR REPLACE VIEW public.decrypted_user_api_keys AS
> 215	SELECT
> 216	  uak.user_id,
> 217	  COALESCE(s_groq.decrypted_secret, uak.groq_api_key) AS groq_api_key,
> 218	  COALESCE(s_openrouter.decrypted_secret, uak.openrouter_api_key) AS openrouter_api_key,
> 219	  COALESCE(s_openai.decrypted_secret, uak.openai_api_key) AS openai_api_key,
> 220	  uak.created_at, uak.updated_at, uak.pref_audio_provider, uak.pref_image_provider, uak.pref_video_provider,
> 221	  COALESCE(s_elevenlabs.decrypted_secret, uak.elevenlabs_api_key) AS elevenlabs_api_key,
> 222	  COALESCE(s_google.decrypted_secret, uak.google_api_key) AS google_api_key,
> 223	  COALESCE(s_nanobana.decrypted_secret, uak.nanobana_api_key) AS nanobana_api_key,
> 224	  COALESCE(s_seedance.decrypted_secret, uak.seedance_api_key) AS seedance_api_key,
> 225	  uak.wp_site_url, uak.wp_username,
> 226	  COALESCE(s_wp_pwd.decrypted_secret, uak.wp_app_password) AS wp_app_password,
> 227	  uak.pref_ai_model,
> 228	  COALESCE(s_replicate.decrypted_secret, uak.replicate_api_key) AS replicate_api_key,
> 229	  COALESCE(s_higgsfield.decrypted_secret, uak.higgsfield_api_key) AS higgsfield_api_key,
> 230	  COALESCE(s_higgsfield_sec.decrypted_secret, uak.higgsfield_api_key_secret) AS higgsfield_api_key_secret,
> 231	  COALESCE(s_apify.decrypted_secret, uak.apify_token) AS apify_token,
> 232	  COALESCE(s_resend.decrypted_secret, uak.resend_api_key) AS resend_api_key,
> 233	  COALESCE(s_firecrawl.decrypted_secret, uak.firecrawl_api_key) AS firecrawl_api_key,
> 234	  COALESCE(s_rapidapi.decrypted_secret, uak.rapidapi_key) AS rapidapi_key,
> 235	  COALESCE(s_hedra.decrypted_secret, uak.hedra_api_key) AS hedra_api_key,
> 236	  COALESCE(s_cartesia.decrypted_secret, uak.cartesia_api_key) AS cartesia_api_key,
> 237	  COALESCE(s_fal.decrypted_secret, uak.fal_api_key) AS fal_api_key
> 238	FROM public.user_api_keys_table uak
> 239	LEFT JOIN vault.decrypted_secrets s_groq ON uak.groq_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_groq.id = uak.groq_api_key::uuid
> 240	LEFT JOIN vault.decrypted_secrets s_openrouter ON uak.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_openrouter.id = uak.openrouter_api_key::uuid
> 241	LEFT JOIN vault.decrypted_secrets s_openai ON uak.openai_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_openai.id = uak.openai_api_key::uuid
> 242	LEFT JOIN vault.decrypted_secrets s_elevenlabs ON uak.elevenlabs_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_elevenlabs.id = uak.elevenlabs_api_key::uuid
> 243	LEFT JOIN vault.decrypted_secrets s_google ON uak.google_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_google.id = uak.google_api_key::uuid
> 244	LEFT JOIN vault.decrypted_secrets s_nanobana ON uak.nanobana_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_nanobana.id = uak.nanobana_api_key::uuid
> 245	LEFT JOIN vault.decrypted_secrets s_seedance ON uak.seedance_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_seedance.id = uak.seedance_api_key::uuid
> 246	LEFT JOIN vault.decrypted_secrets s_wp_pwd ON uak.wp_app_password ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_wp_pwd.id = uak.wp_app_password::uuid
> 247	LEFT JOIN vault.decrypted_secrets s_replicate ON uak.replicate_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_replicate.id = uak.replicate_api_key::uuid
> 248	LEFT JOIN vault.decrypted_secrets s_higgsfield ON uak.higgsfield_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_higgsfield.id = uak.higgsfield_api_key::uuid
> 249	LEFT JOIN vault.decrypted_secrets s_higgsfield_sec ON uak.higgsfield_api_key_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_higgsfield_sec.id = uak.higgsfield_api_key_secret::uuid
> 250	LEFT JOIN vault.decrypted_secrets s_apify ON uak.apify_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_apify.id = uak.apify_token::uuid
> 251	LEFT JOIN vault.decrypted_secrets s_resend ON uak.resend_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_resend.id = uak.resend_api_key::uuid
> 252	LEFT JOIN vault.decrypted_secrets s_firecrawl ON uak.firecrawl_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_firecrawl.id = uak.firecrawl_api_key::uuid
> 253	LEFT JOIN vault.decrypted_secrets s_rapidapi ON uak.rapidapi_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_rapidapi.id = uak.rapidapi_key::uuid
> 254	LEFT JOIN vault.decrypted_secrets s_hedra ON uak.hedra_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_hedra.id = uak.hedra_api_key::uuid
> 255	LEFT JOIN vault.decrypted_secrets s_cartesia ON uak.cartesia_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_cartesia.id = uak.cartesia_api_key::uuid
> 256	LEFT JOIN vault.decrypted_secrets s_fal ON uak.fal_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_fal.id = uak.fal_api_key::uuid;
> 257	REVOKE ALL ON public.decrypted_user_api_keys FROM PUBLIC, anon, authenticated;
> 258	GRANT SELECT ON public.decrypted_user_api_keys TO service_role;
> 259	
> ```

## 🤖 Claude *(03:36:59)*


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

## 🤖 Claude *(03:36:59)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/seed-avatar-clone-ai-bok-seal.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// Phase 7 — Knowledge Mesh injection for the avatar-clone-ai BoK suite.
> 2	// Canonical seed-script form (audit trail + material proof). Idempotent.
> 3	// Run: bun run scripts/seed-avatar-clone-ai-bok-seal.ts
> 4	import { createClient } from "@supabase/supabase-js";
> 5	
> 6	const URL = process.env.VITE_SUPABASE_URL!;
> 7	const KEY = process.env.SB_SECRET_KEY!; // service-role (legacy SUPABASE_SERVICE_ROLE_KEY revoked — see reference_supabase_keys_migrated)
> 8	if (!URL || !KEY) { console.error("Missing VITE_SUPABASE_URL / SB_SECRET_KEY"); process.exit(1); }
> 9	
> 10	const sb = createClient(URL, KEY, { auth: { persistSession: false } });
> 11	
> 12	const SEAL_NAME = "bok-scribe-seal-avatar-clone-ai-v1";
> 13	const PARENT_ID = "c99b7875-e67e-499d-8263-a7c728725268"; // bok-scribe-seal-video-studio-v1.1 (HyperFrames render lineage)
> 14	
> 15	const documentLines = {
> 16	  "00-index": 153, "01-mrd": 185, "02-brd": 243, "03-prd": 302, "04-frd": 453,
> 17	  "05-sdd": 577, "06-data-model": 492, "07-process-flow": 395, "08-quality-metrics": 253,
> 18	  "09-pattern-conformance": 64, total: 3117,
> 19	};
> 20	
> 21	const content =
> 22	  "avatar-clone-ai BoK suite v1 — módulo per-user BYOK puro (Modelo A) 'Avatar / Clone AI / Person AI' no Canvas Studio, instância-zero = programa 'Gabriel AI' (persona-IA bilíngue, video-first, multicanal). Pipeline de nós tipados avatarIdentity → voiceClone → avatarScript (RAG sobre a memory mesh / 'cérebro clonado') → talkingHead → avatarEnhance (Magnific) → Identity Gate (ArcFace) → C2PA → creative_assets → junção com o Viral Autopilot. Postura GO-HYBRID (rosto real ancora + avatar-backfill declarado; NÃO 100%-avatar — FM-AC-014 anti-uncanny, crater McCoy); posicionamento global-English-first (áudio EN-âncora + auto-dub nativo da plataforma p/ alcance / voz PT clonada + re-lip-sync p/ premium); reply engine do X = escopo core; idioma+frequência per-user opt-in. Motores self-serve Hedra (default ~$35/ciclo 30d híbrido) / OmniHuman / Higgsfield; Magnific = conta-org interna; HeyGen = partnership futuro; INVARIANTE anti-conta-mestra (service bureau proibido). Compliance LGPD (biométrico = dado sensível Art.11) + EU AI Act Art.50 (C2PA machine-readable + disclosure deepfake). Selada a partir de 3 seeds da Fatia 0 (00-deepsearch-blueprint 14 frentes + 00b-viability GO-HYBRID + 00c-fronts-closure F1-F7), com baseline honesto medido first-party (YT @uxnai 49 subs / TikTok @gabriel_mcorch 0 vídeos públicos). 10 docs · 3117 linhas. Mercado B2B2C; monetização híbrida (mcoCoins 4×-floor por render via deduct_mco_coins + afiliado/produto long-term).";
> 23	
> 24	const metadata = {
> 25	  title: "avatar-clone-ai BoK Documentation Suite v1",
> 26	  bok_version: "1.0.0",
> 27	  documents: ["00-index", "01-mrd", "02-brd", "03-prd", "04-frd", "05-sdd", "06-data-model", "07-process-flow", "08-quality-metrics", "09-pattern-conformance"],
> 28	  document_lines: documentLines,
> 29	  phase_completed: "Phase 7",
> 30	  traceability_validated: true,
> 31	  traceability_validation_method: "mechanical-grep (Phase-6 agent returned null at session boundary; main-loop verified: 54 FR-AC → 27 PR-AC, 4/4 new tables RLS-enabled, JWT in SDD, billing via deduct_mco_coins, 21 patterns in 09)",
> 32	  traceability_orphans: 0,
> 33	  id_space: {
> 34	    MR: "MR-AC-001..019", BR: "BR-AC-001..028", PR: "PR-AC-001..028",
> 35	    FR: "FR-AC-001..054", NFR: "NFR-AC-001..020",
> 36	    OTD: "OTD-AC-001..014", FMEA: "FM-AC-001..014",
> 37	  },
> 38	  fmea_high_rpn_items: ["FM-AC-014 (rejeição de audiência ao avatar 100%-puro / uncanny-valley — maior RPN; mitigação = injeção periódica de clipe real + postura híbrida)"],
> 39	  new_migrations: 4,
> 40	  new_edge_functions: 3,
> 41	  new_edge_functions_list: ["generate-voice", "avatar-render", "reply-x-engine"],
> 42	  integration_surface: "extends-mcorch",
> 43	  regulatory_profile: "LGPD",
> 44	  regulatory_secondary: "EU AI Act Art.50",
> 45	  monetization: "hybrid",
> 46	  market_segment: "B2B2C",
> 47	  derives_from_seal: "bok-scribe-seal-video-studio-v1.1",
> 48	  fatia0_seeds: ["00-deepsearch-blueprint.md", "00b-fatia0-viability-format-probe.md", "00c-fatia0-fronts-closure.md"],
> 49	  gate_fatia0: "GO-HYBRID",
> 50	  motivating_incident: "Sovereign directive 2026-06-29 — brand-first 'Gabriel AI' persona (avatar/clone per-user module + 30d cadence)",
> 51	};
> 52	
> 53	// Idempotency guard
> 54	const { data: existing } = await sb.from("mcorch_nodes").select("id, name").eq("name", SEAL_NAME).maybeSingle();
> 55	if (existing) {
> 56	  console.log(`Seal already exists (idempotent exit 0): ${existing.id} · ${existing.name}`);
> 57	  process.exit(0);
> 58	}
> 59	
> 60	const { data: node, error: nErr } = await sb.from("mcorch_nodes").insert({
> 61	  node_type: "documentation_suite",
> 62	  name: SEAL_NAME,
> 63	  content,
> 64	  metadata,
> 65	  stability_score: 0.85,
> 66	  revenue_impact: 0, // brand-first internal enabler — no DIRECT documented revenue (honest, Law 1)
> 67	  user_id: null,     // system node — visible to all tenants
> 68	}).select("id, name").single();
> 69	if (nErr) throw nErr;
> 70	console.log("SEAL NODE:", node.id, "·", node.name);
> 71	
> 72	const { data: edge, error: eErr } = await sb.from("mcorch_edges").insert({
> 73	  source_id: node.id,
> 74	  target_id: PARENT_ID,
> 75	  relation_type: "DERIVES_FROM",
> 76	  weight: 1.0,
> 77	  metadata: { reason: "avatar-clone-ai reusa o motor HyperFrames/video_renders/finalize_video_render do video-studio" },
> 78	}).select("id").single();
> 79	if (eErr) throw eErr;
> 80	console.log("DERIVES_FROM EDGE:", edge.id, "→", PARENT_ID, "(video-studio v1.1)");
> 81	console.log("DONE.");
> 82	
> ```

## 🤖 Claude *(03:37:23)*

I have everything I need. Both files were read in full, along with the vetted precedent. I performed a line-by-line diff of all 5 sections for each of the 3 new columns.

## Security Review: Avatar BYOK Migration + Seal Script

### Methodology
Diffed `20260630000000_user_api_keys_avatar_byok.sql` against the in-production, already-reviewed precedent `20260622210000_user_api_keys_rapidapi_channel.sql`. The precedent adds one column (`rapidapi_key`); the new migration adds three (`hedra_api_key`, `cartesia_api_key`, `fal_api_key`). Verified each column across all 5 sections.

### Section-by-section verification

**Section 1 — base columns (lines 14-22):** Three `ADD COLUMN IF NOT EXISTS ... text` statements, idempotent, mirror precedent exactly. No constraints that change security posture.

**Section 2 — encrypt trigger (lines 109-126):** For each of the 3 columns the block is byte-for-byte identical to the vetted pattern:
- `SECURITY DEFINER` + `SET search_path TO ''` preserved (lines 28-29).
- UUID-already-encrypted guard present (`~ '^[0-9a-f]{8}-...$' THEN ELSE`) — prevents double-encryption.
- Uses parameterized `public.vault_upsert_secret(...)` — no dynamic/concatenated SQL into an executable statement; the `||` only builds the secret *name* string (same as all 16 existing columns).
- Secret name namespaced per-user via `'user_api_keys_<col>_' || NEW.user_id::text` — distinct names, no collision (`hedra`, `cartesia`, `fal` are unique tokens). `DISTINCT FROM OLD` guard present.

**Section 3 — masked public view (lines 151-153):** All 3 masked as `'••••••••••••'`. Tenant-isolation `WHERE (auth.uid() = user_id OR auth.role() = 'service_role')` intact (line 155). No raw column leaked through the masked view.

**Section 4 — INSTEAD OF trigger (lines 159-211):**
- Cross-tenant guard intact (line 170): non-service-role with `NEW.user_id IS DISTINCT FROM auth.uid()` → `42501`.
- UPDATE-first `COALESCE(NULLIF(NEW.x, '••••••••••••'), table.x)` pattern applied to all 3 (lines 195-197) — preserves existing secret on masked re-save, no encrypt-trigger double-fire.
- INSERT column list (line 202) and VALUES list (line 204) both include all 3 new columns, correctly positioned at the end, count and order aligned (24 columns in both lists). No NULL/positional drift.

**Section 5 — decrypted view (lines 214-258):**
- COALESCE select for all 3 (lines 235-237) + LEFT JOIN with the UUID-regex guard and `::uuid` cast (lines 254-256). The regex prefilter prevents `::uuid` cast errors on non-encrypted values.
- `REVOKE ALL ... FROM PUBLIC, anon, authenticated` + `GRANT SELECT ... TO service_role` intact (lines 257-258). Decrypted plaintext remains service-role-only.

**Seal script (`seed-avatar-clone-ai-bok-seal.ts`):** Reads `SB_SECRET_KEY` from `process.env` (line 7), not hardcoded; fails closed if missing (line 8). No untrusted input — all inserted values are hardcoded literals (`content`, `metadata`, fixed UUIDs). Uses the supabase-js client builder (parameterized, no raw SQL/injection surface). Idempotency guard via `.eq("name", SEAL_NAME).maybeSingle()` (line 54). No security concern.

### Cross-cutting checks
- No deviation in `search_path`, SECURITY DEFINER, GRANT/REVOKE, or tenant-guard semantics versus precedent.
- Column ordering is consistent across all 5 sections (no positional mismatch between the masked view, INSTEAD OF UPDATE/INSERT lists, and decrypted view).
- The 3 new secret-name tokens are unique and don't shadow existing ones.
- Replaces the same two `CREATE OR REPLACE` functions and two `CREATE OR REPLACE VIEW` objects as the precedent — full supersede, no orphaned definition keeping an old column out of the machinery.

### Verdict

The migration faithfully mirrors the vetted precedent with no security-relevant deviation. Tenant isolation, Vault encryption, `search_path` hardening, and the service-role-only decrypted view are all preserved identically for each of the three new columns. The seal script uses env-sourced credentials with no injection surface.

**NO FINDINGS (confidence 9).**

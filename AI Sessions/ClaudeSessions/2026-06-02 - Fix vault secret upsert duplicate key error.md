# Fix vault secret upsert duplicate key error
**Date:** 2026-06-02 | **Session ID:** `c3171bbf-a868-4311-b231-ed1a7ec72ca4`

---

## 👤 User *(14:10:11)*

Bug de availability confirmado materialmente em 2026-06-02 (sessão do fix do WordPress BYOK), deixado como dívida residual documentada.

PROBLEMA: O trigger BEFORE INSERT/UPDATE `trg_encrypt_user_api_keys` (em `supabase/migrations/20260601000000_credential_encryption.sql`, recriado em `20260601060000_user_api_keys_apify_token.sql`) chama `vault.create_secret(value, '<nome-deterministico>')` INCONDICIONALMENTE quando uma coluna-segredo muda de valor. `vault.create_secret` faz `INSERT INTO vault.secrets` puro SEM ON CONFLICT, e `vault.secrets.name` tem índice único (`secrets_name_idx`). Logo: editar um segredo para um valor NOVO enquanto o segredo de mesmo nome determinístico ainda existe → `ERROR 23505 duplicate key ... secrets_name_idx`. 

Para WordPress isso se manifesta no fluxo "Editar senha sem desconectar antes" (em `src/pages/SocialAccountsPage.tsx` o botão "Editar"). Os mesmos triggers irmãos `trg_encrypt_meta_config` e `trg_encrypt_social_accounts` têm o mesmo padrão (nomes por `id` de linha, então re-salvar token na mesma linha também colide).

CONTEXTO JÁ RESOLVIDO (não refazer): o double-fire do `INSERT...ON CONFLICT` no `trg_instead_of_user_api_keys` foi corrigido em `20260602130000_fix_user_api_keys_instead_of_double_fire.sql` (UPDATE-first). O disconnect via `disconnect_wordpress()` deleta o segredo, então connect→disconnect→reconnect funciona. Só falta o caso "trocar valor sem deletar antes".

FIX PROPOSTO: criar um helper `vault_upsert_secret(p_value text, p_name text, p_desc text) RETURNS uuid` que: `SELECT id FROM vault.secrets WHERE name=p_name`; se achou → `vault.update_secret(id, p_value)` e retorna id; senão → `vault.create_secret(...)`. Substituir as ~11 chamadas `vault.create_secret` em `trg_encrypt_user_api_keys` (e avaliar fazer o mesmo em `trg_encrypt_meta_config`/`trg_encrypt_social_accounts`) por esse helper, preservando o guard de "já é UUID → keep". 

REQUISITOS: nova migration com timestamp > 20260602130000; OBRIGATÓRIO passar `/security-review` (mexe na camada central de encriptação de credenciais — toda migration passa por /security-review por regra do CLAUDE.md). Verificar materialmente via Management API (token em ~/.supabase/access-token, project ref bcyvddsykvehvpwstlfa, endpoint POST https://api.supabase.com/v1/projects/<ref>/database/query): simular um usuário com set_config('request.jwt.claims', '{"sub":"<uid>","role":"authenticated"}', true) e provar que salvar um segredo DUAS vezes com valores diferentes não dá 23505 e que o decrypted_user_api_keys reflete o 2º valor. Atualizar o SOP `docs/processes/credential-disconnect-clear.md` (seção "Known latent debt") quando fechado.

## 🤖 Claude *(14:10:37)*


## 🤖 Claude *(14:10:41)*

Vou começar entendendo materialmente o estado atual da camada de encriptação. Deixe-me declarar o enquadramento e partir para a exploração.

**ORO triplet desta task:**
- **Operator:** AI Agent (MCORCH Master Execution Agent)
- **Reviewer:** Sovereign (Gabriel)
- **Owner:** Sovereign — blast radius = camada central de encriptação de TODAS as credenciais BYOK de TODOS os tenants; falha em produção = corrupção/perda de segredo Vault ou DoS de salvar credencial.

Lei 2 (Processo Antecipado): isto é **bug fix em feature já documentada** (SOP `docs/processes/credential-disconnect-clear.md` existe) → sem BoK gate. Mas toca a camada de encriptação → `/security-review` obrigatório.

Vou explorar o estado material primeiro.

## 🤖 Claude *(14:10:42)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260601000000_credential_encryption.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: Credential Encryption at-rest using Supabase Vault
> 2	-- OTD-META-ENCRYPT
> 3	-- BoK SSOT: docs/bok/meta-api/06-data-model.md (Data Security, encryption at-rest)
> 4	
> 5	-- ─────────────────────────────────────────────────────────────────────────────
> 6	-- 1. RENAME TABLES: Rename base tables to *_table
> 7	-- ─────────────────────────────────────────────────────────────────────────────
> 8	
> 9	ALTER TABLE IF EXISTS public.meta_config RENAME TO meta_config_table;
> 10	ALTER TABLE IF EXISTS public.social_accounts RENAME TO social_accounts_table;
> 11	ALTER TABLE IF EXISTS public.user_api_keys RENAME TO user_api_keys_table;
> 12	
> 13	-- ─────────────────────────────────────────────────────────────────────────────
> 14	-- 2. TRIGGERS: Intercept writes on base tables and encrypt to vault.secrets
> 15	-- ─────────────────────────────────────────────────────────────────────────────
> 16	
> 17	-- 2.1 meta_config_table encryption trigger
> 18	CREATE OR REPLACE FUNCTION public.trg_encrypt_meta_config()
> 19	RETURNS TRIGGER AS $$
> 20	DECLARE
> 21	  v_token_id UUID;
> 22	  v_pages_id UUID;
> 23	BEGIN
> 24	  IF NEW.id IS NULL THEN
> 25	    NEW.id := gen_random_uuid();
> 26	  END IF;
> 27	
> 28	  IF NEW.long_lived_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.long_lived_token IS DISTINCT FROM OLD.long_lived_token) THEN
> 29	    IF NEW.long_lived_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 30	      -- keep existing UUID
> 31	    ELSE
> 32	      v_token_id := vault.create_secret(NEW.long_lived_token, 'meta_config_long_lived_token_' || NEW.id::text, 'Meta config long-lived token');
> 33	      NEW.long_lived_token = v_token_id::text;
> 34	    END IF;
> 35	  END IF;
> 36	
> 37	  IF NEW.pages IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.pages IS DISTINCT FROM OLD.pages) THEN
> 38	    IF NEW.pages::text ~ '^"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"$' THEN
> 39	      -- keep existing UUID JSON
> 40	    ELSE
> 41	      v_pages_id := vault.create_secret(NEW.pages::text, 'meta_config_pages_' || NEW.id::text, 'Meta config pages list');
> 42	      NEW.pages = to_jsonb(v_pages_id::text);
> 43	    END IF;
> 44	  END IF;
> 45	
> 46	  RETURN NEW;
> 47	END;
> 48	$$ LANGUAGE plpgsql SECURITY DEFINER;
> 49	
> 50	CREATE OR REPLACE TRIGGER tr_encrypt_meta_config
> 51	  BEFORE INSERT OR UPDATE ON public.meta_config_table
> 52	  FOR EACH ROW EXECUTE FUNCTION public.trg_encrypt_meta_config();
> 53	
> 54	
> 55	-- 2.2 social_accounts_table encryption trigger
> 56	CREATE OR REPLACE FUNCTION public.trg_encrypt_social_accounts()
> 57	RETURNS TRIGGER AS $$
> 58	DECLARE
> 59	  v_access_token_id UUID;
> 60	  v_refresh_token_id UUID;
> 61	BEGIN
> 62	  IF NEW.id IS NULL THEN
> 63	    NEW.id := gen_random_uuid();
> 64	  END IF;
> 65	
> 66	  IF NEW.access_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.access_token IS DISTINCT FROM OLD.access_token) THEN
> 67	    IF NEW.access_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 68	      -- keep
> 69	    ELSE
> 70	      v_access_token_id := vault.create_secret(NEW.access_token, 'social_accounts_access_token_' || NEW.id::text, 'Social account access token');
> 71	      NEW.access_token = v_access_token_id::text;
> 72	    END IF;
> 73	  END IF;
> 74	
> 75	  IF NEW.refresh_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.refresh_token IS DISTINCT FROM OLD.refresh_token) THEN
> 76	    IF NEW.refresh_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 77	      -- keep
> 78	    ELSE
> 79	      v_refresh_token_id := vault.create_secret(NEW.refresh_token, 'social_accounts_refresh_token_' || NEW.id::text, 'Social account refresh token');
> 80	      NEW.refresh_token = v_refresh_token_id::text;
> 81	    END IF;
> 82	  END IF;
> 83	
> 84	  RETURN NEW;
> 85	END;
> 86	$$ LANGUAGE plpgsql SECURITY DEFINER;
> 87	
> 88	CREATE OR REPLACE TRIGGER tr_encrypt_social_accounts
> 89	  BEFORE INSERT OR UPDATE ON public.social_accounts_table
> 90	  FOR EACH ROW EXECUTE FUNCTION public.trg_encrypt_social_accounts();
> 91	
> 92	
> 93	-- 2.3 user_api_keys_table encryption trigger
> 94	CREATE OR REPLACE FUNCTION public.trg_encrypt_user_api_keys()
> 95	RETURNS TRIGGER AS $$
> 96	DECLARE
> 97	  v_id UUID;
> 98	BEGIN
> 99	  -- groq_api_key
> 100	  IF NEW.groq_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.groq_api_key IS DISTINCT FROM OLD.groq_api_key) THEN
> 101	    IF NEW.groq_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 102	      -- keep
> 103	    ELSE
> 104	      v_id := vault.create_secret(NEW.groq_api_key, 'user_api_keys_groq_api_key_' || NEW.user_id::text, 'Groq API Key');
> 105	      NEW.groq_api_key = v_id::text;
> 106	    END IF;
> 107	  END IF;
> 108	
> 109	  -- openrouter_api_key
> 110	  IF NEW.openrouter_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openrouter_api_key IS DISTINCT FROM OLD.openrouter_api_key) THEN
> 111	    IF NEW.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 112	      -- keep
> 113	    ELSE
> 114	      v_id := vault.create_secret(NEW.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || NEW.user_id::text, 'OpenRouter API Key');
> 115	      NEW.openrouter_api_key = v_id::text;
> 116	    END IF;
> 117	  END IF;
> 118	
> 119	  -- openai_api_key
> 120	  IF NEW.openai_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openai_api_key IS DISTINCT FROM OLD.openai_api_key) THEN
> 121	    IF NEW.openai_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 122	      -- keep
> 123	    ELSE
> 124	      v_id := vault.create_secret(NEW.openai_api_key, 'user_api_keys_openai_api_key_' || NEW.user_id::text, 'OpenAI API Key');
> 125	      NEW.openai_api_key = v_id::text;
> 126	    END IF;
> 127	  END IF;
> 128	
> 129	  -- elevenlabs_api_key
> 130	  IF NEW.elevenlabs_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.elevenlabs_api_key IS DISTINCT FROM OLD.elevenlabs_api_key) THEN
> 131	    IF NEW.elevenlabs_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 132	      -- keep
> 133	    ELSE
> 134	      v_id := vault.create_secret(NEW.elevenlabs_api_key, 'user_api_keys_elevenlabs_api_key_' || NEW.user_id::text, 'ElevenLabs API Key');
> 135	      NEW.elevenlabs_api_key = v_id::text;
> 136	    END IF;
> 137	  END IF;
> 138	
> 139	  -- google_api_key
> 140	  IF NEW.google_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.google_api_key IS DISTINCT FROM OLD.google_api_key) THEN
> 141	    IF NEW.google_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 142	      -- keep
> 143	    ELSE
> 144	      v_id := vault.create_secret(NEW.google_api_key, 'user_api_keys_google_api_key_' || NEW.user_id::text, 'Google API Key');
> 145	      NEW.google_api_key = v_id::text;
> 146	    END IF;
> 147	  END IF;
> 148	
> 149	  -- nanobana_api_key
> 150	  IF NEW.nanobana_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.nanobana_api_key IS DISTINCT FROM OLD.nanobana_api_key) THEN
> 151	    IF NEW.nanobana_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 152	      -- keep
> 153	    ELSE
> 154	      v_id := vault.create_secret(NEW.nanobana_api_key, 'user_api_keys_nanobana_api_key_' || NEW.user_id::text, 'Nanobana API Key');
> 155	      NEW.nanobana_api_key = v_id::text;
> 156	    END IF;
> 157	  END IF;
> 158	
> 159	  -- seedance_api_key
> 160	  IF NEW.seedance_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.seedance_api_key IS DISTINCT FROM OLD.seedance_api_key) THEN
> 161	    IF NEW.seedance_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 162	      -- keep
> 163	    ELSE
> 164	      v_id := vault.create_secret(NEW.seedance_api_key, 'user_api_keys_seedance_api_key_' || NEW.user_id::text, 'Seedance API Key');
> 165	      NEW.seedance_api_key = v_id::text;
> 166	    END IF;
> 167	  END IF;
> 168	
> 169	  -- wp_app_password
> 170	  IF NEW.wp_app_password IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.wp_app_password IS DISTINCT FROM OLD.wp_app_password) THEN
> 171	    IF NEW.wp_app_password ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 172	      -- keep
> 173	    ELSE
> 174	      v_id := vault.create_secret(NEW.wp_app_password, 'user_api_keys_wp_app_password_' || NEW.user_id::text, 'WordPress App Password');
> 175	      NEW.wp_app_password = v_id::text;
> 176	    END IF;
> 177	  END IF;
> 178	
> 179	  -- replicate_api_key
> 180	  IF NEW.replicate_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.replicate_api_key IS DISTINCT FROM OLD.replicate_api_key) THEN
> 181	    IF NEW.replicate_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 182	      -- keep
> 183	    ELSE
> 184	      v_id := vault.create_secret(NEW.replicate_api_key, 'user_api_keys_replicate_api_key_' || NEW.user_id::text, 'Replicate API Key');
> 185	      NEW.replicate_api_key = v_id::text;
> 186	    END IF;
> 187	  END IF;
> 188	
> 189	  -- higgsfield_api_key
> 190	  IF NEW.higgsfield_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.higgsfield_api_key IS DISTINCT FROM OLD.higgsfield_api_key) THEN
> 191	    IF NEW.higgsfield_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 192	      -- keep
> 193	    ELSE
> 194	      v_id := vault.create_secret(NEW.higgsfield_api_key, 'user_api_keys_higgsfield_api_key_' || NEW.user_id::text, 'Higgsfield API Key');
> 195	      NEW.higgsfield_api_key = v_id::text;
> 196	    END IF;
> 197	  END IF;
> 198	
> 199	  -- higgsfield_api_key_secret
> 200	  IF NEW.higgsfield_api_key_secret IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.higgsfield_api_key_secret IS DISTINCT FROM OLD.higgsfield_api_key_secret) THEN
> 201	    IF NEW.higgsfield_api_key_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 202	      -- keep
> 203	    ELSE
> 204	      v_id := vault.create_secret(NEW.higgsfield_api_key_secret, 'user_api_keys_higgsfield_api_key_secret_' || NEW.user_id::text, 'Higgsfield API Key Secret');
> 205	      NEW.higgsfield_api_key_secret = v_id::text;
> 206	    END IF;
> 207	  END IF;
> 208	
> 209	  RETURN NEW;
> 210	END;
> 211	$$ LANGUAGE plpgsql SECURITY DEFINER;
> 212	
> 213	CREATE OR REPLACE TRIGGER tr_encrypt_user_api_keys
> 214	  BEFORE INSERT OR UPDATE ON public.user_api_keys_table
> 215	  FOR EACH ROW EXECUTE FUNCTION public.trg_encrypt_user_api_keys();
> 216	
> 217	
> 218	-- ─────────────────────────────────────────────────────────────────────────────
> 219	-- 3. BACKFILL: Migrate existing plaintext credentials to vault
> 220	-- ─────────────────────────────────────────────────────────────────────────────
> 221	
> 222	-- 3.1 Backfill meta_config_table
> 223	DO $$
> 224	DECLARE
> 225	  r RECORD;
> 226	  v_token_id UUID;
> 227	  v_pages_id UUID;
> 228	BEGIN
> 229	  FOR r IN SELECT * FROM public.meta_config_table LOOP
> 230	    v_token_id := NULL;
> 231	    v_pages_id := NULL;
> 232	    
> 233	    IF r.long_lived_token IS NOT NULL AND r.long_lived_token !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 234	      v_token_id := vault.create_secret(r.long_lived_token, 'meta_config_long_lived_token_' || r.id::text, 'Meta config long-lived token');
> 235	    END IF;
> 236	    
> 237	    IF r.pages IS NOT NULL AND r.pages::text !~ '^"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"$' THEN
> 238	      v_pages_id := vault.create_secret(r.pages::text, 'meta_config_pages_' || r.id::text, 'Meta config pages list');
> 239	    END IF;
> 240	    
> 241	    IF v_token_id IS NOT NULL OR v_pages_id IS NOT NULL THEN
> 242	      UPDATE public.meta_config_table
> 243	      SET 
> 244	        long_lived_token = COALESCE(v_token_id::text, long_lived_token),
> 245	        pages = COALESCE(to_jsonb(v_pages_id::text), pages)
> 246	      WHERE id = r.id;
> 247	    END IF;
> 248	  END LOOP;
> 249	END $$;
> 250	
> 251	
> 252	-- 3.2 Backfill social_accounts_table
> 253	DO $$
> 254	DECLARE
> 255	  r RECORD;
> 256	  v_access_id UUID;
> 257	  v_refresh_id UUID;
> 258	BEGIN
> 259	  FOR r IN SELECT * FROM public.social_accounts_table LOOP
> 260	    v_access_id := NULL;
> 261	    v_refresh_id := NULL;
> 262	    
> 263	    IF r.access_token IS NOT NULL AND r.access_token !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 264	      v_access_id := vault.create_secret(r.access_token, 'social_accounts_access_token_' || r.id::text, 'Social account access token');
> 265	    END IF;
> 266	    
> 267	    IF r.refresh_token IS NOT NULL AND r.refresh_token !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 268	      v_refresh_id := vault.create_secret(r.refresh_token, 'social_accounts_refresh_token_' || r.id::text, 'Social account refresh token');
> 269	    END IF;
> 270	    
> 271	    IF v_access_id IS NOT NULL OR v_refresh_id IS NOT NULL THEN
> 272	      UPDATE public.social_accounts_table
> 273	      SET 
> 274	        access_token = COALESCE(v_access_id::text, access_token),
> 275	        refresh_token = COALESCE(v_refresh_id::text, refresh_token)
> 276	      WHERE id = r.id;
> 277	    END IF;
> 278	  END LOOP;
> 279	END $$;
> 280	
> 281	
> 282	-- 3.3 Backfill user_api_keys_table
> 283	DO $$
> 284	DECLARE
> 285	  r RECORD;
> 286	  v_groq UUID; v_or UUID; v_oa UUID; v_el UUID; v_gg UUID; v_nb UUID; v_sd UUID; v_wp UUID; v_rep UUID; v_hf UUID; v_hfs UUID;
> 287	BEGIN
> 288	  FOR r IN SELECT * FROM public.user_api_keys_table LOOP
> 289	    v_groq := NULL; v_or := NULL; v_oa := NULL; v_el := NULL; v_gg := NULL; v_nb := NULL; v_sd := NULL; v_wp := NULL; v_rep := NULL; v_hf := NULL; v_hfs := NULL;
> 290	    
> 291	    IF r.groq_api_key IS NOT NULL AND r.groq_api_key !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 292	      v_groq := vault.create_secret(r.groq_api_key, 'user_api_keys_groq_api_key_' || r.user_id::text, 'Groq API Key');
> 293	    END IF;
> 294	    IF r.openrouter_api_key IS NOT NULL AND r.openrouter_api_key !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 295	      v_or := vault.create_secret(r.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || r.user_id::text, 'OpenRouter API Key');
> 296	    END IF;
> 297	    IF r.openai_api_key IS NOT NULL AND r.openai_api_key !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 298	      v_oa := vault.create_secret(r.openai_api_key, 'user_api_keys_openai_api_key_' || r.user_id::text, 'OpenAI API Key');
> 299	    END IF;
> 300	    IF r.elevenlabs_api_key IS NOT NULL AND r.elevenlabs_api_key !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 301	      v_el := vault.create_secret(r.elevenlabs_api_key, 'user_api_keys_elevenlabs_api_key_' || r.user_id::text, 'ElevenLabs API Key');
> 302	    END IF;
> 303	    IF r.google_api_key IS NOT NULL AND r.google_api_key !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 304	      v_gg := vault.create_secret(r.google_api_key, 'user_api_keys_google_api_key_' || r.user_id::text, 'Google API Key');
> 305	    END IF;
> 306	    IF r.nanobana_api_key IS NOT NULL AND r.nanobana_api_key !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 307	      v_nb := vault.create_secret(r.nanobana_api_key, 'user_api_keys_nanobana_api_key_' || r.user_id::text, 'Nanobana API Key');
> 308	    END IF;
> 309	    IF r.seedance_api_key IS NOT NULL AND r.seedance_api_key !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 310	      v_sd := vault.create_secret(r.seedance_api_key, 'user_api_keys_seedance_api_key_' || r.user_id::text, 'Seedance API Key');
> 311	    END IF;
> 312	    IF r.wp_app_password IS NOT NULL AND r.wp_app_password !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 313	      v_wp := vault.create_secret(r.wp_app_password, 'user_api_keys_wp_app_password_' || r.user_id::text, 'WordPress App Password');
> 314	    END IF;
> 315	    IF r.replicate_api_key IS NOT NULL AND r.replicate_api_key !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 316	      v_rep := vault.create_secret(r.replicate_api_key, 'user_api_keys_replicate_api_key_' || r.user_id::text, 'Replicate API Key');
> 317	    END IF;
> 318	    IF r.higgsfield_api_key IS NOT NULL AND r.higgsfield_api_key !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 319	      v_hf := vault.create_secret(r.higgsfield_api_key, 'user_api_keys_higgsfield_api_key_' || r.user_id::text, 'Higgsfield API Key');
> 320	    END IF;
> 321	    IF r.higgsfield_api_key_secret IS NOT NULL AND r.higgsfield_api_key_secret !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 322	      v_hfs := vault.create_secret(r.higgsfield_api_key_secret, 'user_api_keys_higgsfield_api_key_secret_' || r.user_id::text, 'Higgsfield API Key Secret');
> 323	    END IF;
> 324	    
> 325	    IF v_groq IS NOT NULL OR v_or IS NOT NULL OR v_oa IS NOT NULL OR v_el IS NOT NULL OR v_gg IS NOT NULL OR v_nb IS NOT NULL OR v_sd IS NOT NULL OR v_wp IS NOT NULL OR v_rep IS NOT NULL OR v_hf IS NOT NULL OR v_hfs IS NOT NULL THEN
> 326	      UPDATE public.user_api_keys_table
> 327	      SET 
> 328	        groq_api_key = COALESCE(v_groq::text, groq_api_key),
> 329	        openrouter_api_key = COALESCE(v_or::text, openrouter_api_key),
> 330	        openai_api_key = COALESCE(v_oa::text, openai_api_key),
> 331	        elevenlabs_api_key = COALESCE(v_el::text, elevenlabs_api_key),
> 332	        google_api_key = COALESCE(v_gg::text, google_api_key),
> 333	        nanobana_api_key = COALESCE(v_nb::text, nanobana_api_key),
> 334	        seedance_api_key = COALESCE(v_sd::text, seedance_api_key),
> 335	        wp_app_password = COALESCE(v_wp::text, wp_app_password),
> 336	        replicate_api_key = COALESCE(v_rep::text, replicate_api_key),
> 337	        higgsfield_api_key = COALESCE(v_hf::text, higgsfield_api_key),
> 338	        higgsfield_api_key_secret = COALESCE(v_hfs::text, higgsfield_api_key_secret)
> 339	      WHERE user_id = r.user_id;
> 340	    END IF;
> 341	  END LOOP;
> 342	END $$;
> 343	
> 344	
> 345	-- ─────────────────────────────────────────────────────────────────────────────
> 346	-- 4. PUBLIC MASKED VIEWS: Security invoker views for client-side compat
> 347	-- ─────────────────────────────────────────────────────────────────────────────
> 348	
> 349	-- 4.1 meta_config public view
> 350	CREATE OR REPLACE VIEW public.meta_config WITH (security_invoker = true) AS
> 351	SELECT
> 352	  id,
> 353	  user_id,
> 354	  facebook_user_id,
> 355	  CASE WHEN long_lived_token IS NOT NULL THEN '••••••••••••' ELSE NULL END AS long_lived_token,
> 356	  scopes,
> 357	  CASE WHEN pages IS NOT NULL THEN to_jsonb('••••••••••••'::text) ELSE NULL END AS pages,
> 358	  instagram_business_account_id,
> 359	  whatsapp_phone_number_id,
> 360	  whatsapp_waba_id,
> 361	  meta_ad_account_id,
> 362	  requires_reauth,
> 363	  token_expires_at,
> 364	  created_at,
> 365	  updated_at
> 366	FROM public.meta_config_table;
> 367	
> 368	-- 4.2 social_accounts public view
> 369	CREATE OR REPLACE VIEW public.social_accounts WITH (security_invoker = true) AS
> 370	SELECT
> 371	  id,
> 372	  user_id,
> 373	  platform,
> 374	  platform_user_id,
> 375	  platform_username,
> 376	  CASE WHEN access_token IS NOT NULL THEN '••••••••••••' ELSE NULL END AS access_token,
> 377	  CASE WHEN refresh_token IS NOT NULL THEN '••••••••••••' ELSE NULL END AS refresh_token,
> 378	  token_expires_at,
> 379	  scopes,
> 380	  is_active,
> 381	  metadata,
> 382	  created_at,
> 383	  updated_at
> 384	FROM public.social_accounts_table;
> 385	
> 386	-- 4.3 user_api_keys public view
> 387	CREATE OR REPLACE VIEW public.user_api_keys WITH (security_invoker = true) AS
> 388	SELECT
> 389	  user_id,
> 390	  created_at,
> 391	  updated_at,
> 392	  pref_audio_provider,
> 393	  pref_image_provider,
> 394	  pref_video_provider,
> 395	  wp_site_url,
> 396	  wp_username,
> 397	  pref_ai_model,
> 398	  CASE WHEN groq_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS groq_api_key,
> 399	  CASE WHEN openrouter_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS openrouter_api_key,
> 400	  CASE WHEN openai_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS openai_api_key,
> 401	  CASE WHEN elevenlabs_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS elevenlabs_api_key,
> 402	  CASE WHEN google_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS google_api_key,
> 403	  CASE WHEN nanobana_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS nanobana_api_key,
> 404	  CASE WHEN seedance_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS seedance_api_key,
> 405	  CASE WHEN wp_app_password IS NOT NULL THEN '••••••••••••' ELSE NULL END AS wp_app_password,
> 406	  CASE WHEN replicate_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS replicate_api_key,
> 407	  CASE WHEN higgsfield_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS higgsfield_api_key,
> 408	  CASE WHEN higgsfield_api_key_secret IS NOT NULL THEN '••••••••••••' ELSE NULL END AS higgsfield_api_key_secret
> 409	FROM public.user_api_keys_table;
> 410	
> 411	
> 412	-- ─────────────────────────────────────────────────────────────────────────────
> 413	-- 5. INSTEAD OF TRIGGERS: Map view updates/inserts back to base tables
> 414	-- ─────────────────────────────────────────────────────────────────────────────
> 415	
> 416	-- 5.1 Instead of trigger for meta_config
> 417	CREATE OR REPLACE FUNCTION public.trg_instead_of_meta_config()
> 418	RETURNS TRIGGER AS $$
> 419	BEGIN
> 420	  IF TG_OP = 'DELETE' THEN
> 421	    DELETE FROM public.meta_config_table WHERE id = OLD.id;
> 422	    RETURN OLD;
> 423	  ELSIF TG_OP = 'INSERT' THEN
> 424	    INSERT INTO public.meta_config_table (
> 425	      id, user_id, facebook_user_id, long_lived_token, scopes, pages, instagram_business_account_id, whatsapp_phone_number_id, whatsapp_waba_id, meta_ad_account_id, requires_reauth, token_expires_at
> 426	    ) VALUES (
> 427	      COALESCE(NEW.id, gen_random_uuid()), NEW.user_id, NEW.facebook_user_id, NEW.long_lived_token, NEW.scopes, NEW.pages, NEW.instagram_business_account_id, NEW.whatsapp_phone_number_id, NEW.whatsapp_waba_id, NEW.meta_ad_account_id, NEW.requires_reauth, NEW.token_expires_at
> 428	    );
> 429	    RETURN NEW;
> 430	  ELSIF TG_OP = 'UPDATE' THEN
> 431	    UPDATE public.meta_config_table SET
> 432	      user_id = NEW.user_id,
> 433	      facebook_user_id = NEW.facebook_user_id,
> 434	      long_lived_token = COALESCE(NULLIF(NEW.long_lived_token, '••••••••••••'), public.meta_config_table.long_lived_token),
> 435	      scopes = NEW.scopes,
> 436	      pages = COALESCE(NULLIF(NEW.pages, to_jsonb('••••••••••••'::text)), public.meta_config_table.pages),
> 437	      instagram_business_account_id = NEW.instagram_business_account_id,
> 438	      whatsapp_phone_number_id = NEW.whatsapp_phone_number_id,
> 439	      whatsapp_waba_id = NEW.whatsapp_waba_id,
> 440	      meta_ad_account_id = NEW.meta_ad_account_id,
> 441	      requires_reauth = NEW.requires_reauth,
> 442	      token_expires_at = NEW.token_expires_at,
> 443	      updated_at = now()
> 444	    WHERE id = OLD.id;
> 445	    RETURN NEW;
> 446	  END IF;
> 447	  RETURN NULL;
> 448	END;
> 449	$$ LANGUAGE plpgsql SECURITY DEFINER;
> 450	
> 451	CREATE TRIGGER trg_instead_of_meta_config
> 452	  INSTEAD OF INSERT OR UPDATE OR DELETE ON public.meta_config
> 453	  FOR EACH ROW EXECUTE FUNCTION public.trg_instead_of_meta_config();
> 454	
> 455	
> 456	-- 5.2 Instead of trigger for social_accounts
> 457	CREATE OR REPLACE FUNCTION public.trg_instead_of_social_accounts()
> 458	RETURNS TRIGGER AS $$
> 459	BEGIN
> 460	  IF TG_OP = 'DELETE' THEN
> 461	    DELETE FROM public.social_accounts_table WHERE id = OLD.id;
> 462	    RETURN OLD;
> 463	  ELSIF TG_OP = 'INSERT' THEN
> 464	    INSERT INTO public.social_accounts_table (
> 465	      id, user_id, platform, platform_user_id, platform_username, access_token, refresh_token, token_expires_at, scopes, is_active, metadata
> 466	    ) VALUES (
> 467	      COALESCE(NEW.id, gen_random_uuid()), NEW.user_id, NEW.platform, NEW.platform_user_id, NEW.platform_username, NEW.access_token, NEW.refresh_token, NEW.token_expires_at, NEW.scopes, NEW.is_active, NEW.metadata
> 468	    );
> 469	    RETURN NEW;
> 470	  ELSIF TG_OP = 'UPDATE' THEN
> 471	    UPDATE public.social_accounts_table SET
> 472	      user_id = NEW.user_id,
> 473	      platform = NEW.platform,
> 474	      platform_user_id = NEW.platform_user_id,
> 475	      platform_username = NEW.platform_username,
> 476	      access_token = COALESCE(NULLIF(NEW.access_token, '••••••••••••'), public.social_accounts_table.access_token),
> 477	      refresh_token = COALESCE(NULLIF(NEW.refresh_token, '••••••••••••'), public.social_accounts_table.refresh_token),
> 478	      token_expires_at = NEW.token_expires_at,
> 479	      scopes = NEW.scopes,
> 480	      is_active = NEW.is_active,
> 481	      metadata = NEW.metadata,
> 482	      updated_at = now()
> 483	    WHERE id = OLD.id;
> 484	    RETURN NEW;
> 485	  END IF;
> 486	  RETURN NULL;
> 487	END;
> 488	$$ LANGUAGE plpgsql SECURITY DEFINER;
> 489	
> 490	CREATE TRIGGER trg_instead_of_social_accounts
> 491	  INSTEAD OF INSERT OR UPDATE OR DELETE ON public.social_accounts
> 492	  FOR EACH ROW EXECUTE FUNCTION public.trg_instead_of_social_accounts();
> 493	
> 494	
> 495	-- 5.3 Instead of trigger for user_api_keys
> 496	CREATE OR REPLACE FUNCTION public.trg_instead_of_user_api_keys()
> 497	RETURNS TRIGGER AS $$
> 498	BEGIN
> 499	  IF TG_OP = 'DELETE' THEN
> 500	    DELETE FROM public.user_api_keys_table WHERE user_id = OLD.user_id;
> 501	    RETURN OLD;
> 502	  ELSIF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
> 503	    INSERT INTO public.user_api_keys_table (
> 504	      user_id, groq_api_key, openrouter_api_key, openai_api_key, pref_audio_provider, pref_image_provider, pref_video_provider, elevenlabs_api_key, google_api_key, nanobana_api_key, seedance_api_key, wp_site_url, wp_username, wp_app_password, pref_ai_model, replicate_api_key, higgsfield_api_key, higgsfield_api_key_secret
> 505	    ) VALUES (
> 506	      NEW.user_id, NEW.groq_api_key, NEW.openrouter_api_key, NEW.openai_api_key, NEW.pref_audio_provider, NEW.pref_image_provider, NEW.pref_video_provider, NEW.elevenlabs_api_key, NEW.google_api_key, NEW.nanobana_api_key, NEW.seedance_api_key, NEW.wp_site_url, NEW.wp_username, NEW.wp_app_password, NEW.pref_ai_model, NEW.replicate_api_key, NEW.higgsfield_api_key, NEW.higgsfield_api_key_secret
> 507	    )
> 508	    ON CONFLICT (user_id) DO UPDATE SET
> 509	      groq_api_key = COALESCE(NULLIF(NEW.groq_api_key, '••••••••••••'), public.user_api_keys_table.groq_api_key),
> 510	      openrouter_api_key = COALESCE(NULLIF(NEW.openrouter_api_key, '••••••••••••'), public.user_api_keys_table.openrouter_api_key),
> 511	      openai_api_key = COALESCE(NULLIF(NEW.openai_api_key, '••••••••••••'), public.user_api_keys_table.openai_api_key),
> 512	      pref_audio_provider = COALESCE(NEW.pref_audio_provider, public.user_api_keys_table.pref_audio_provider),
> 513	      pref_image_provider = COALESCE(NEW.pref_image_provider, public.user_api_keys_table.pref_image_provider),
> 514	      pref_video_provider = COALESCE(NEW.pref_video_provider, public.user_api_keys_table.pref_video_provider),
> 515	      elevenlabs_api_key = COALESCE(NULLIF(NEW.elevenlabs_api_key, '••••••••••••'), public.user_api_keys_table.elevenlabs_api_key),
> 516	      google_api_key = COALESCE(NULLIF(NEW.google_api_key, '••••••••••••'), public.user_api_keys_table.google_api_key),
> 517	      nanobana_api_key = COALESCE(NULLIF(NEW.nanobana_api_key, '••••••••••••'), public.user_api_keys_table.nanobana_api_key),
> 518	      seedance_api_key = COALESCE(NULLIF(NEW.seedance_api_key, '••••••••••••'), public.user_api_keys_table.seedance_api_key),
> 519	      wp_site_url = NEW.wp_site_url,
> 520	      wp_username = NEW.wp_username,
> 521	      wp_app_password = COALESCE(NULLIF(NEW.wp_app_password, '••••••••••••'), public.user_api_keys_table.wp_app_password),
> 522	      pref_ai_model = COALESCE(NEW.pref_ai_model, public.user_api_keys_table.pref_ai_model),
> 523	      replicate_api_key = COALESCE(NULLIF(NEW.replicate_api_key, '••••••••••••'), public.user_api_keys_table.replicate_api_key),
> 524	      higgsfield_api_key = COALESCE(NULLIF(NEW.higgsfield_api_key, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key),
> 525	      higgsfield_api_key_secret = COALESCE(NULLIF(NEW.higgsfield_api_key_secret, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key_secret),
> 526	      updated_at = now();
> 527	    RETURN NEW;
> 528	  END IF;
> 529	  RETURN NULL;
> 530	END;
> 531	$$ LANGUAGE plpgsql SECURITY DEFINER;
> 532	
> 533	CREATE TRIGGER trg_instead_of_user_api_keys
> 534	  INSTEAD OF INSERT OR UPDATE OR DELETE ON public.user_api_keys
> 535	  FOR EACH ROW EXECUTE FUNCTION public.trg_instead_of_user_api_keys();
> 536	
> 537	
> 538	-- ─────────────────────────────────────────────────────────────────────────────
> 539	-- 6. PRIVATE DECRYPTED VIEWS: Real decrypted keys view for service_role
> 540	-- ─────────────────────────────────────────────────────────────────────────────
> 541	
> 542	-- 6.1 decrypted_meta_config
> 543	CREATE OR REPLACE VIEW public.decrypted_meta_config AS
> 544	SELECT 
> 545	  mc.id,
> 546	  mc.user_id,
> 547	  mc.facebook_user_id,
> 548	  COALESCE(s_token.decrypted_secret, mc.long_lived_token) AS long_lived_token,
> 549	  mc.scopes,
> 550	  COALESCE(s_pages.decrypted_secret::jsonb, mc.pages) AS pages,
> 551	  mc.instagram_business_account_id,
> 552	  mc.whatsapp_phone_number_id,
> 553	  mc.whatsapp_waba_id,
> 554	  mc.meta_ad_account_id,
> 555	  mc.requires_reauth,
> 556	  mc.token_expires_at,
> 557	  mc.created_at,
> 558	  mc.updated_at
> 559	FROM public.meta_config_table mc
> 560	LEFT JOIN vault.decrypted_secrets s_token ON mc.long_lived_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_token.id = mc.long_lived_token::uuid
> 561	LEFT JOIN vault.decrypted_secrets s_pages ON mc.pages::text ~ '^"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"$' AND s_pages.id = (mc.pages#>>'{}')::uuid;
> 562	
> 563	-- 6.2 decrypted_social_accounts
> 564	CREATE OR REPLACE VIEW public.decrypted_social_accounts AS
> 565	SELECT 
> 566	  sa.id,
> 567	  sa.user_id,
> 568	  sa.platform,
> 569	  sa.platform_user_id,
> 570	  sa.platform_username,
> 571	  COALESCE(s_access.decrypted_secret, sa.access_token) AS access_token,
> 572	  COALESCE(s_refresh.decrypted_secret, sa.refresh_token) AS refresh_token,
> 573	  sa.token_expires_at,
> 574	  sa.scopes,
> 575	  sa.is_active,
> 576	  sa.metadata,
> 577	  sa.created_at,
> 578	  sa.updated_at
> 579	FROM public.social_accounts_table sa
> 580	LEFT JOIN vault.decrypted_secrets s_access ON sa.access_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_access.id = sa.access_token::uuid
> 581	LEFT JOIN vault.decrypted_secrets s_refresh ON sa.refresh_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_refresh.id = sa.refresh_token::uuid;
> 582	
> 583	-- 6.3 decrypted_user_api_keys
> 584	CREATE OR REPLACE VIEW public.decrypted_user_api_keys AS
> 585	SELECT 
> 586	  uak.user_id,
> 587	  COALESCE(s_groq.decrypted_secret, uak.groq_api_key) AS groq_api_key,
> 588	  COALESCE(s_openrouter.decrypted_secret, uak.openrouter_api_key) AS openrouter_api_key,
> 589	  COALESCE(s_openai.decrypted_secret, uak.openai_api_key) AS openai_api_key,
> 590	  uak.created_at,
> 591	  uak.updated_at,
> 592	  uak.pref_audio_provider,
> 593	  uak.pref_image_provider,
> 594	  uak.pref_video_provider,
> 595	  COALESCE(s_elevenlabs.decrypted_secret, uak.elevenlabs_api_key) AS elevenlabs_api_key,
> 596	  COALESCE(s_google.decrypted_secret, uak.google_api_key) AS google_api_key,
> 597	  COALESCE(s_nanobana.decrypted_secret, uak.nanobana_api_key) AS nanobana_api_key,
> 598	  COALESCE(s_seedance.decrypted_secret, uak.seedance_api_key) AS seedance_api_key,
> 599	  uak.wp_site_url,
> 600	  uak.wp_username,
> 601	  COALESCE(s_wp_pwd.decrypted_secret, uak.wp_app_password) AS wp_app_password,
> 602	  uak.pref_ai_model,
> 603	  COALESCE(s_replicate.decrypted_secret, uak.replicate_api_key) AS replicate_api_key,
> 604	  COALESCE(s_higgsfield.decrypted_secret, uak.higgsfield_api_key) AS higgsfield_api_key,
> 605	  COALESCE(s_higgsfield_sec.decrypted_secret, uak.higgsfield_api_key_secret) AS higgsfield_api_key_secret
> 606	FROM public.user_api_keys_table uak
> 607	LEFT JOIN vault.decrypted_secrets s_groq ON uak.groq_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_groq.id = uak.groq_api_key::uuid
> 608	LEFT JOIN vault.decrypted_secrets s_openrouter ON uak.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_openrouter.id = uak.openrouter_api_key::uuid
> 609	LEFT JOIN vault.decrypted_secrets s_openai ON uak.openai_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_openai.id = uak.openai_api_key::uuid
> 610	LEFT JOIN vault.decrypted_secrets s_elevenlabs ON uak.elevenlabs_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_elevenlabs.id = uak.elevenlabs_api_key::uuid
> 611	LEFT JOIN vault.decrypted_secrets s_google ON uak.google_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_google.id = uak.google_api_key::uuid
> 612	LEFT JOIN vault.decrypted_secrets s_nanobana ON uak.nanobana_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_nanobana.id = uak.nanobana_api_key::uuid
> 613	LEFT JOIN vault.decrypted_secrets s_seedance ON uak.seedance_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_seedance.id = uak.seedance_api_key::uuid
> 614	LEFT JOIN vault.decrypted_secrets s_wp_pwd ON uak.wp_app_password ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_wp_pwd.id = uak.wp_app_password::uuid
> 615	LEFT JOIN vault.decrypted_secrets s_replicate ON uak.replicate_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_replicate.id = uak.replicate_api_key::uuid
> 616	LEFT JOIN vault.decrypted_secrets s_higgsfield ON uak.higgsfield_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_higgsfield.id = uak.higgsfield_api_key::uuid
> 617	LEFT JOIN vault.decrypted_secrets s_higgsfield_sec ON uak.higgsfield_api_key_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_higgsfield_sec.id = uak.higgsfield_api_key_secret::uuid;
> 618	
> 619	
> 620	-- ─────────────────────────────────────────────────────────────────────────────
> 621	-- 7. PERMISSIONS: Restrict view selects
> 622	-- ─────────────────────────────────────────────────────────────────────────────
> 623	
> 624	-- decrypted_* views are restricted to service_role exclusively
> 625	REVOKE ALL ON public.decrypted_meta_config FROM PUBLIC, anon, authenticated;
> 626	GRANT SELECT ON public.decrypted_meta_config TO service_role;
> 627	
> 628	REVOKE ALL ON public.decrypted_social_accounts FROM PUBLIC, anon, authenticated;
> 629	GRANT SELECT ON public.decrypted_social_accounts TO service_role;
> 630	
> 631	REVOKE ALL ON public.decrypted_user_api_keys FROM PUBLIC, anon, authenticated;
> 632	GRANT SELECT ON public.decrypted_user_api_keys TO service_role;
> 633	
> ```

## 🤖 Claude *(14:10:43)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260601060000_user_api_keys_apify_token.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: per-user Apify token (BYOK) for affiliate catalog enrichment
> 2	-- API Tenancy Model — layered: per-user apify_token → global APIFY_TOKENS fallback (system/cron).
> 3	-- SOP: docs/processes/affiliate-catalog-enrichment.md
> 4	-- Follows the Vault-encryption pattern of 20260601000000_credential_encryption.sql:
> 5	--   base column → encrypt trigger → masked public view → INSTEAD OF trigger → decrypted view.
> 6	-- Additive only: every existing column handler is preserved verbatim; apify_token is appended.
> 7	
> 8	-- ─────────────────────────────────────────────────────────────────────────────
> 9	-- 1. COLUMN on the base table
> 10	-- ─────────────────────────────────────────────────────────────────────────────
> 11	ALTER TABLE public.user_api_keys_table
> 12	  ADD COLUMN IF NOT EXISTS apify_token text;
> 13	
> 14	COMMENT ON COLUMN public.user_api_keys_table.apify_token
> 15	  IS 'Per-user Apify API token (BYOK) for ML scraping/enrichment. Vault-encrypted at rest. NULL falls back to global APIFY_TOKENS.';
> 16	
> 17	-- ─────────────────────────────────────────────────────────────────────────────
> 18	-- 2. ENCRYPT TRIGGER — re-create with the apify_token block appended
> 19	-- ─────────────────────────────────────────────────────────────────────────────
> 20	CREATE OR REPLACE FUNCTION public.trg_encrypt_user_api_keys()
> 21	RETURNS TRIGGER AS $$
> 22	DECLARE
> 23	  v_id UUID;
> 24	BEGIN
> 25	  -- groq_api_key
> 26	  IF NEW.groq_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.groq_api_key IS DISTINCT FROM OLD.groq_api_key) THEN
> 27	    IF NEW.groq_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 28	    ELSE
> 29	      v_id := vault.create_secret(NEW.groq_api_key, 'user_api_keys_groq_api_key_' || NEW.user_id::text, 'Groq API Key');
> 30	      NEW.groq_api_key = v_id::text;
> 31	    END IF;
> 32	  END IF;
> 33	
> 34	  -- openrouter_api_key
> 35	  IF NEW.openrouter_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openrouter_api_key IS DISTINCT FROM OLD.openrouter_api_key) THEN
> 36	    IF NEW.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 37	    ELSE
> 38	      v_id := vault.create_secret(NEW.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || NEW.user_id::text, 'OpenRouter API Key');
> 39	      NEW.openrouter_api_key = v_id::text;
> 40	    END IF;
> 41	  END IF;
> 42	
> 43	  -- openai_api_key
> 44	  IF NEW.openai_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openai_api_key IS DISTINCT FROM OLD.openai_api_key) THEN
> 45	    IF NEW.openai_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 46	    ELSE
> 47	      v_id := vault.create_secret(NEW.openai_api_key, 'user_api_keys_openai_api_key_' || NEW.user_id::text, 'OpenAI API Key');
> 48	      NEW.openai_api_key = v_id::text;
> 49	    END IF;
> 50	  END IF;
> 51	
> 52	  -- elevenlabs_api_key
> 53	  IF NEW.elevenlabs_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.elevenlabs_api_key IS DISTINCT FROM OLD.elevenlabs_api_key) THEN
> 54	    IF NEW.elevenlabs_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 55	    ELSE
> 56	      v_id := vault.create_secret(NEW.elevenlabs_api_key, 'user_api_keys_elevenlabs_api_key_' || NEW.user_id::text, 'ElevenLabs API Key');
> 57	      NEW.elevenlabs_api_key = v_id::text;
> 58	    END IF;
> 59	  END IF;
> 60	
> 61	  -- google_api_key
> 62	  IF NEW.google_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.google_api_key IS DISTINCT FROM OLD.google_api_key) THEN
> 63	    IF NEW.google_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 64	    ELSE
> 65	      v_id := vault.create_secret(NEW.google_api_key, 'user_api_keys_google_api_key_' || NEW.user_id::text, 'Google API Key');
> 66	      NEW.google_api_key = v_id::text;
> 67	    END IF;
> 68	  END IF;
> 69	
> 70	  -- nanobana_api_key
> 71	  IF NEW.nanobana_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.nanobana_api_key IS DISTINCT FROM OLD.nanobana_api_key) THEN
> 72	    IF NEW.nanobana_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 73	    ELSE
> 74	      v_id := vault.create_secret(NEW.nanobana_api_key, 'user_api_keys_nanobana_api_key_' || NEW.user_id::text, 'Nanobana API Key');
> 75	      NEW.nanobana_api_key = v_id::text;
> 76	    END IF;
> 77	  END IF;
> 78	
> 79	  -- seedance_api_key
> 80	  IF NEW.seedance_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.seedance_api_key IS DISTINCT FROM OLD.seedance_api_key) THEN
> 81	    IF NEW.seedance_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 82	    ELSE
> 83	      v_id := vault.create_secret(NEW.seedance_api_key, 'user_api_keys_seedance_api_key_' || NEW.user_id::text, 'Seedance API Key');
> 84	      NEW.seedance_api_key = v_id::text;
> 85	    END IF;
> 86	  END IF;
> 87	
> 88	  -- wp_app_password
> 89	  IF NEW.wp_app_password IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.wp_app_password IS DISTINCT FROM OLD.wp_app_password) THEN
> 90	    IF NEW.wp_app_password ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 91	    ELSE
> 92	      v_id := vault.create_secret(NEW.wp_app_password, 'user_api_keys_wp_app_password_' || NEW.user_id::text, 'WordPress App Password');
> 93	      NEW.wp_app_password = v_id::text;
> 94	    END IF;
> 95	  END IF;
> 96	
> 97	  -- replicate_api_key
> 98	  IF NEW.replicate_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.replicate_api_key IS DISTINCT FROM OLD.replicate_api_key) THEN
> 99	    IF NEW.replicate_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 100	    ELSE
> 101	      v_id := vault.create_secret(NEW.replicate_api_key, 'user_api_keys_replicate_api_key_' || NEW.user_id::text, 'Replicate API Key');
> 102	      NEW.replicate_api_key = v_id::text;
> 103	    END IF;
> 104	  END IF;
> 105	
> 106	  -- higgsfield_api_key
> 107	  IF NEW.higgsfield_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.higgsfield_api_key IS DISTINCT FROM OLD.higgsfield_api_key) THEN
> 108	    IF NEW.higgsfield_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 109	    ELSE
> 110	      v_id := vault.create_secret(NEW.higgsfield_api_key, 'user_api_keys_higgsfield_api_key_' || NEW.user_id::text, 'Higgsfield API Key');
> 111	      NEW.higgsfield_api_key = v_id::text;
> 112	    END IF;
> 113	  END IF;
> 114	
> 115	  -- higgsfield_api_key_secret
> 116	  IF NEW.higgsfield_api_key_secret IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.higgsfield_api_key_secret IS DISTINCT FROM OLD.higgsfield_api_key_secret) THEN
> 117	    IF NEW.higgsfield_api_key_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 118	    ELSE
> 119	      v_id := vault.create_secret(NEW.higgsfield_api_key_secret, 'user_api_keys_higgsfield_api_key_secret_' || NEW.user_id::text, 'Higgsfield API Key Secret');
> 120	      NEW.higgsfield_api_key_secret = v_id::text;
> 121	    END IF;
> 122	  END IF;
> 123	
> 124	  -- apify_token (NEW — per-user ML scraping BYOK)
> 125	  IF NEW.apify_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.apify_token IS DISTINCT FROM OLD.apify_token) THEN
> 126	    IF NEW.apify_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> 127	    ELSE
> 128	      v_id := vault.create_secret(NEW.apify_token, 'user_api_keys_apify_token_' || NEW.user_id::text, 'Apify Token');
> 129	      NEW.apify_token = v_id::text;
> 130	    END IF;
> 131	  END IF;
> 132	
> 133	  RETURN NEW;
> 134	END;
> 135	$$ LANGUAGE plpgsql SECURITY DEFINER;
> 136	
> 137	-- (trigger tr_encrypt_user_api_keys already bound to the function — no re-create needed)
> 138	
> 139	-- ─────────────────────────────────────────────────────────────────────────────
> 140	-- 3. MASKED PUBLIC VIEW — append apify_token (masked)
> 141	-- MUST match the CURRENT production definition from 20260601000600_secure_definer_views.sql:
> 142	-- a SECURITY DEFINER view (default, NOT security_invoker — base-table SELECT is REVOKED from
> 143	-- authenticated) with an explicit WHERE tenancy filter. Reverting to security_invoker here would
> 144	-- break authenticated reads (permission denied on the base table).
> 145	-- ─────────────────────────────────────────────────────────────────────────────
> 146	CREATE OR REPLACE VIEW public.user_api_keys AS
> 147	SELECT
> 148	  user_id,
> 149	  created_at,
> 150	  updated_at,
> 151	  pref_audio_provider,
> 152	  pref_image_provider,
> 153	  pref_video_provider,
> 154	  wp_site_url,
> 155	  wp_username,
> 156	  pref_ai_model,
> 157	  CASE WHEN groq_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS groq_api_key,
> 158	  CASE WHEN openrouter_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS openrouter_api_key,
> 159	  CASE WHEN openai_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS openai_api_key,
> 160	  CASE WHEN elevenlabs_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS elevenlabs_api_key,
> 161	  CASE WHEN google_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS google_api_key,
> 162	  CASE WHEN nanobana_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS nanobana_api_key,
> 163	  CASE WHEN seedance_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS seedance_api_key,
> 164	  CASE WHEN wp_app_password IS NOT NULL THEN '••••••••••••' ELSE NULL END AS wp_app_password,
> 165	  CASE WHEN replicate_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS replicate_api_key,
> 166	  CASE WHEN higgsfield_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS higgsfield_api_key,
> 167	  CASE WHEN higgsfield_api_key_secret IS NOT NULL THEN '••••••••••••' ELSE NULL END AS higgsfield_api_key_secret,
> 168	  CASE WHEN apify_token IS NOT NULL THEN '••••••••••••' ELSE NULL END AS apify_token
> 169	FROM public.user_api_keys_table
> 170	WHERE (auth.uid() = user_id OR auth.role() = 'service_role');
> 171	
> 172	-- Preserve client grants (CREATE OR REPLACE keeps ACLs; re-assert to be safe / idempotent).
> 173	GRANT SELECT, INSERT, UPDATE, DELETE ON public.user_api_keys TO anon, authenticated;
> 174	
> 175	-- ─────────────────────────────────────────────────────────────────────────────
> 176	-- 4. INSTEAD OF TRIGGER — add apify_token to INSERT cols/VALUES + ON CONFLICT UPDATE
> 177	-- ─────────────────────────────────────────────────────────────────────────────
> 178	CREATE OR REPLACE FUNCTION public.trg_instead_of_user_api_keys()
> 179	RETURNS TRIGGER AS $$
> 180	BEGIN
> 181	  IF TG_OP = 'DELETE' THEN
> 182	    DELETE FROM public.user_api_keys_table WHERE user_id = OLD.user_id;
> 183	    RETURN OLD;
> 184	  ELSIF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
> 185	    INSERT INTO public.user_api_keys_table (
> 186	      user_id, groq_api_key, openrouter_api_key, openai_api_key, pref_audio_provider, pref_image_provider, pref_video_provider, elevenlabs_api_key, google_api_key, nanobana_api_key, seedance_api_key, wp_site_url, wp_username, wp_app_password, pref_ai_model, replicate_api_key, higgsfield_api_key, higgsfield_api_key_secret, apify_token
> 187	    ) VALUES (
> 188	      NEW.user_id, NEW.groq_api_key, NEW.openrouter_api_key, NEW.openai_api_key, NEW.pref_audio_provider, NEW.pref_image_provider, NEW.pref_video_provider, NEW.elevenlabs_api_key, NEW.google_api_key, NEW.nanobana_api_key, NEW.seedance_api_key, NEW.wp_site_url, NEW.wp_username, NEW.wp_app_password, NEW.pref_ai_model, NEW.replicate_api_key, NEW.higgsfield_api_key, NEW.higgsfield_api_key_secret, NEW.apify_token
> 189	    )
> 190	    ON CONFLICT (user_id) DO UPDATE SET
> 191	      groq_api_key = COALESCE(NULLIF(NEW.groq_api_key, '••••••••••••'), public.user_api_keys_table.groq_api_key),
> 192	      openrouter_api_key = COALESCE(NULLIF(NEW.openrouter_api_key, '••••••••••••'), public.user_api_keys_table.openrouter_api_key),
> 193	      openai_api_key = COALESCE(NULLIF(NEW.openai_api_key, '••••••••••••'), public.user_api_keys_table.openai_api_key),
> 194	      pref_audio_provider = COALESCE(NEW.pref_audio_provider, public.user_api_keys_table.pref_audio_provider),
> 195	      pref_image_provider = COALESCE(NEW.pref_image_provider, public.user_api_keys_table.pref_image_provider),
> 196	      pref_video_provider = COALESCE(NEW.pref_video_provider, public.user_api_keys_table.pref_video_provider),
> 197	      elevenlabs_api_key = COALESCE(NULLIF(NEW.elevenlabs_api_key, '••••••••••••'), public.user_api_keys_table.elevenlabs_api_key),
> 198	      google_api_key = COALESCE(NULLIF(NEW.google_api_key, '••••••••••••'), public.user_api_keys_table.google_api_key),
> 199	      nanobana_api_key = COALESCE(NULLIF(NEW.nanobana_api_key, '••••••••••••'), public.user_api_keys_table.nanobana_api_key),
> 200	      seedance_api_key = COALESCE(NULLIF(NEW.seedance_api_key, '••••••••••••'), public.user_api_keys_table.seedance_api_key),
> 201	      wp_site_url = NEW.wp_site_url,
> 202	      wp_username = NEW.wp_username,
> 203	      wp_app_password = COALESCE(NULLIF(NEW.wp_app_password, '••••••••••••'), public.user_api_keys_table.wp_app_password),
> 204	      pref_ai_model = COALESCE(NEW.pref_ai_model, public.user_api_keys_table.pref_ai_model),
> 205	      replicate_api_key = COALESCE(NULLIF(NEW.replicate_api_key, '••••••••••••'), public.user_api_keys_table.replicate_api_key),
> 206	      higgsfield_api_key = COALESCE(NULLIF(NEW.higgsfield_api_key, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key),
> 207	      higgsfield_api_key_secret = COALESCE(NULLIF(NEW.higgsfield_api_key_secret, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key_secret),
> 208	      apify_token = COALESCE(NULLIF(NEW.apify_token, '••••••••••••'), public.user_api_keys_table.apify_token),
> 209	      updated_at = now();
> 210	    RETURN NEW;
> 211	  END IF;
> 212	  RETURN NULL;
> 213	END;
> 214	$$ LANGUAGE plpgsql SECURITY DEFINER;
> 215	
> 216	-- ─────────────────────────────────────────────────────────────────────────────
> 217	-- 5. DECRYPTED VIEW (service_role only) — append apify_token + its vault join
> 218	-- ─────────────────────────────────────────────────────────────────────────────
> 219	CREATE OR REPLACE VIEW public.decrypted_user_api_keys AS
> 220	SELECT
> 221	  uak.user_id,
> 222	  COALESCE(s_groq.decrypted_secret, uak.groq_api_key) AS groq_api_key,
> 223	  COALESCE(s_openrouter.decrypted_secret, uak.openrouter_api_key) AS openrouter_api_key,
> 224	  COALESCE(s_openai.decrypted_secret, uak.openai_api_key) AS openai_api_key,
> 225	  uak.created_at,
> 226	  uak.updated_at,
> 227	  uak.pref_audio_provider,
> 228	  uak.pref_image_provider,
> 229	  uak.pref_video_provider,
> 230	  COALESCE(s_elevenlabs.decrypted_secret, uak.elevenlabs_api_key) AS elevenlabs_api_key,
> 231	  COALESCE(s_google.decrypted_secret, uak.google_api_key) AS google_api_key,
> 232	  COALESCE(s_nanobana.decrypted_secret, uak.nanobana_api_key) AS nanobana_api_key,
> 233	  COALESCE(s_seedance.decrypted_secret, uak.seedance_api_key) AS seedance_api_key,
> 234	  uak.wp_site_url,
> 235	  uak.wp_username,
> 236	  COALESCE(s_wp_pwd.decrypted_secret, uak.wp_app_password) AS wp_app_password,
> 237	  uak.pref_ai_model,
> 238	  COALESCE(s_replicate.decrypted_secret, uak.replicate_api_key) AS replicate_api_key,
> 239	  COALESCE(s_higgsfield.decrypted_secret, uak.higgsfield_api_key) AS higgsfield_api_key,
> 240	  COALESCE(s_higgsfield_sec.decrypted_secret, uak.higgsfield_api_key_secret) AS higgsfield_api_key_secret,
> 241	  COALESCE(s_apify.decrypted_secret, uak.apify_token) AS apify_token
> 242	FROM public.user_api_keys_table uak
> 243	LEFT JOIN vault.decrypted_secrets s_groq ON uak.groq_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_groq.id = uak.groq_api_key::uuid
> 244	LEFT JOIN vault.decrypted_secrets s_openrouter ON uak.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_openrouter.id = uak.openrouter_api_key::uuid
> 245	LEFT JOIN vault.decrypted_secrets s_openai ON uak.openai_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_openai.id = uak.openai_api_key::uuid
> 246	LEFT JOIN vault.decrypted_secrets s_elevenlabs ON uak.elevenlabs_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_elevenlabs.id = uak.elevenlabs_api_key::uuid
> 247	LEFT JOIN vault.decrypted_secrets s_google ON uak.google_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_google.id = uak.google_api_key::uuid
> 248	LEFT JOIN vault.decrypted_secrets s_nanobana ON uak.nanobana_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_nanobana.id = uak.nanobana_api_key::uuid
> 249	LEFT JOIN vault.decrypted_secrets s_seedance ON uak.seedance_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_seedance.id = uak.seedance_api_key::uuid
> 250	LEFT JOIN vault.decrypted_secrets s_wp_pwd ON uak.wp_app_password ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_wp_pwd.id = uak.wp_app_password::uuid
> 251	LEFT JOIN vault.decrypted_secrets s_replicate ON uak.replicate_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_replicate.id = uak.replicate_api_key::uuid
> 252	LEFT JOIN vault.decrypted_secrets s_higgsfield ON uak.higgsfield_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_higgsfield.id = uak.higgsfield_api_key::uuid
> 253	LEFT JOIN vault.decrypted_secrets s_higgsfield_sec ON uak.higgsfield_api_key_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_higgsfield_sec.id = uak.higgsfield_api_key_secret::uuid
> 254	LEFT JOIN vault.decrypted_secrets s_apify ON uak.apify_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_apify.id = uak.apify_token::uuid;
> 255	
> 256	-- decrypted_user_api_keys stays service_role-only (grants preserved across REPLACE; re-assert to be safe)
> 257	REVOKE ALL ON public.decrypted_user_api_keys FROM PUBLIC, anon, authenticated;
> 258	GRANT SELECT ON public.decrypted_user_api_keys TO service_role;
> 259	
> ```

## 🤖 Claude *(14:10:44)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260602130000_fix_user_api_keys_instead_of_double_fire.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: fix user_api_keys INSTEAD OF trigger — eliminate encrypt double-fire (23505)
> 2	-- ─────────────────────────────────────────────────────────────────────────────
> 3	-- Bug (introduced 2026-06-01 by credential_encryption): trg_instead_of_user_api_keys routed
> 4	-- BOTH client INSERT and UPDATE through a single `INSERT ... ON CONFLICT (user_id) DO UPDATE`
> 5	-- on user_api_keys_table. When the row already exists, Postgres fires the BEFORE-row encryption
> 6	-- trigger TWICE within that one statement — once for the INSERT phase (which runs
> 7	-- vault.create_secret for each NEW secret value) and again for the DO UPDATE phase (which runs
> 8	-- vault.create_secret AGAIN with the same deterministic name) → unique_violation on
> 9	-- vault.secrets.secrets_name_idx (SQLSTATE 23505). Additionally, a client UPDATE carries the
> 10	-- masked sentinel '••••••••••••' for unchanged secret columns; the INSERT phase tried to
> 11	-- vault-encrypt that literal, colliding with the already-existing secret of the same name.
> 12	--
> 13	-- Net effect: connecting/saving ANY credential failed for every user whose user_api_keys row
> 14	-- already existed (only the very first all-fields insert on a brand-new row succeeded). Proven
> 15	-- materially 2026-06-02 (T1/T3 = .insert 23505 on the field being set; T4 = .update 23505 on
> 16	-- groq via the masked-value re-encrypt).
> 17	--
> 18	-- Fix: branch UPDATE-first / INSERT-if-not-found (the idiomatic plpgsql upsert) so the encryption
> 19	-- trigger fires EXACTLY ONCE per write. This matches how trg_instead_of_meta_config and
> 20	-- trg_instead_of_social_accounts already branch. The COALESCE-NULLIF guards are preserved, so an
> 21	-- unchanged secret (sent as '••••••••••••' or NULL) resolves to the stored Vault reference and is
> 22	-- never re-encrypted. wp_site_url/wp_username are also moved to COALESCE(NEW, base) — matching the
> 23	-- other non-secret prefs — so a partial save (e.g. saving only an AI key) can no longer wipe the
> 24	-- WordPress site/username (clearing is done exclusively by disconnect_wordpress()).
> 25	--
> 26	-- Scope: user_api_keys ONLY (meta_config/social_accounts already branch correctly).
> 27	-- Residual debt (documented, not fixed here): changing a secret to a NEW value while the row's
> 28	-- existing same-named Vault secret is still present still collides (the encrypt trigger always
> 29	-- CREATEs); fixing that requires making trg_encrypt_user_api_keys idempotent (update-or-create by
> 30	-- name) and is tracked separately. See docs/processes/credential-disconnect-clear.md.
> 31	
> 32	CREATE OR REPLACE FUNCTION public.trg_instead_of_user_api_keys()
> 33	RETURNS TRIGGER AS $$
> 34	BEGIN
> 35	  IF TG_OP = 'DELETE' THEN
> 36	    DELETE FROM public.user_api_keys_table WHERE user_id = OLD.user_id;
> 37	    RETURN OLD;
> 38	
> 39	  ELSIF TG_OP = 'INSERT' OR TG_OP = 'UPDATE' THEN
> 40	    -- Tenant guard. The view grants INSERT to anon+authenticated and this INSTEAD OF trigger runs
> 41	    -- as a definer (bypassing base-table RLS), and an INSERT cannot be constrained by the view's
> 42	    -- WHERE filter the way SELECT/UPDATE/DELETE are. Without this check an authenticated caller
> 43	    -- could INSERT with a spoofed user_id and write another tenant's credential row. (Previously
> 44	    -- "masked" only by the 23505 crash this migration removes — so closing it is mandatory here.)
> 45	    -- service_role (edge functions / cron / onboarding) legitimately writes arbitrary user_ids.
> 46	    IF auth.role() IS DISTINCT FROM 'service_role' AND NEW.user_id IS DISTINCT FROM auth.uid() THEN
> 47	      RAISE EXCEPTION 'cannot write credentials for another user' USING errcode = '42501';
> 48	    END IF;
> 49	
> 50	    -- UPDATE-first: fires the BEFORE UPDATE encryption trigger exactly once for an existing row.
> 51	    UPDATE public.user_api_keys_table SET
> 52	      groq_api_key              = COALESCE(NULLIF(NEW.groq_api_key, '••••••••••••'), public.user_api_keys_table.groq_api_key),
> 53	      openrouter_api_key        = COALESCE(NULLIF(NEW.openrouter_api_key, '••••••••••••'), public.user_api_keys_table.openrouter_api_key),
> 54	      openai_api_key            = COALESCE(NULLIF(NEW.openai_api_key, '••••••••••••'), public.user_api_keys_table.openai_api_key),
> 55	      pref_audio_provider       = COALESCE(NEW.pref_audio_provider, public.user_api_keys_table.pref_audio_provider),
> 56	      pref_image_provider       = COALESCE(NEW.pref_image_provider, public.user_api_keys_table.pref_image_provider),
> 57	      pref_video_provider       = COALESCE(NEW.pref_video_provider, public.user_api_keys_table.pref_video_provider),
> 58	      elevenlabs_api_key        = COALESCE(NULLIF(NEW.elevenlabs_api_key, '••••••••••••'), public.user_api_keys_table.elevenlabs_api_key),
> 59	      google_api_key            = COALESCE(NULLIF(NEW.google_api_key, '••••••••••••'), public.user_api_keys_table.google_api_key),
> 60	      nanobana_api_key          = COALESCE(NULLIF(NEW.nanobana_api_key, '••••••••••••'), public.user_api_keys_table.nanobana_api_key),
> 61	      seedance_api_key          = COALESCE(NULLIF(NEW.seedance_api_key, '••••••••••••'), public.user_api_keys_table.seedance_api_key),
> 62	      wp_site_url               = COALESCE(NEW.wp_site_url, public.user_api_keys_table.wp_site_url),
> 63	      wp_username               = COALESCE(NEW.wp_username, public.user_api_keys_table.wp_username),
> 64	      wp_app_password           = COALESCE(NULLIF(NEW.wp_app_password, '••••••••••••'), public.user_api_keys_table.wp_app_password),
> 65	      pref_ai_model             = COALESCE(NEW.pref_ai_model, public.user_api_keys_table.pref_ai_model),
> 66	      replicate_api_key         = COALESCE(NULLIF(NEW.replicate_api_key, '••••••••••••'), public.user_api_keys_table.replicate_api_key),
> 67	      higgsfield_api_key        = COALESCE(NULLIF(NEW.higgsfield_api_key, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key),
> 68	      higgsfield_api_key_secret = COALESCE(NULLIF(NEW.higgsfield_api_key_secret, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key_secret),
> 69	      apify_token               = COALESCE(NULLIF(NEW.apify_token, '••••••••••••'), public.user_api_keys_table.apify_token),
> 70	      updated_at                = now()
> 71	    WHERE user_id = NEW.user_id;
> 72	
> 73	    -- No existing row → first-time insert (fires the BEFORE INSERT encryption trigger exactly once).
> 74	    IF NOT FOUND THEN
> 75	      INSERT INTO public.user_api_keys_table (
> 76	        user_id, groq_api_key, openrouter_api_key, openai_api_key, pref_audio_provider, pref_image_provider, pref_video_provider, elevenlabs_api_key, google_api_key, nanobana_api_key, seedance_api_key, wp_site_url, wp_username, wp_app_password, pref_ai_model, replicate_api_key, higgsfield_api_key, higgsfield_api_key_secret, apify_token
> 77	      ) VALUES (
> 78	        NEW.user_id, NEW.groq_api_key, NEW.openrouter_api_key, NEW.openai_api_key, NEW.pref_audio_provider, NEW.pref_image_provider, NEW.pref_video_provider, NEW.elevenlabs_api_key, NEW.google_api_key, NEW.nanobana_api_key, NEW.seedance_api_key, NEW.wp_site_url, NEW.wp_username, NEW.wp_app_password, NEW.pref_ai_model, NEW.replicate_api_key, NEW.higgsfield_api_key, NEW.higgsfield_api_key_secret, NEW.apify_token
> 79	      );
> 80	    END IF;
> 81	    RETURN NEW;
> 82	  END IF;
> 83	  RETURN NULL;
> 84	END;
> 85	$$ LANGUAGE plpgsql SECURITY DEFINER SET search_path = '';
> 86	
> ```

## 🤖 Claude *(14:10:44)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/credential-disconnect-clear.md"
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
> 76	## Known latent debt (discovered 2026-06-02 — flagged, out of this fix's scope)
> 77	
> 78	The encryption trigger (`trg_encrypt_user_api_keys` and its `meta_config`/`social_accounts` siblings)
> 79	calls `vault.create_secret(value, '<deterministic-name>')` **unconditionally** when a secret column
> 80	changes. `vault.create_secret` does a plain INSERT with **no ON CONFLICT**, and `vault.secrets.name`
> 81	is UNIQUE → **re-saving a credential while one already exists for that name throws `unique_violation`**.
> 82	For WordPress this hits the "Editar → save new password without disconnecting first" path. Connect →
> 83	disconnect → reconnect works because `disconnect_wordpress()` deletes the secret. The robust fix is to
> 84	make the encryption trigger idempotent (update-in-place when the deterministic name already exists)
> 85	across all three tables — tracked as a follow-up; it touches the security-critical encryption trigger
> 86	for 3 tables and warrants its own `/security-review`.
> 87	
> ```

## 🤖 Claude *(14:13:01)*


## 🤖 Claude *(14:13:03)*

Tenho o quadro completo das três triggers e do INSTEAD OF já corrigido. Antes de escrever qualquer SQL, preciso de prova material de três fatos que sustentam o fix: (1) a assinatura real de `vault.update_secret` neste banco, (2) que `secrets_name_idx` é mesmo único, (3) se há FK em `user_api_keys_table.user_id` (decide se posso usar um uid sintético no teste). Vou sondar via Management API e listar as migrations locais em paralelo.

## 🤖 Claude *(14:13:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -1 /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/ | tail -20",
  "description": "List most recent migration files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 20260527012253_inspect_net_responses_rpc.sql
> 20260527012332_inspect_net_request.sql
> 20260527012404_inspect_net_v2.sql
> 20260527012421_inspect_net_v3.sql
> 20260527012500_async_orchestrate_step_debug.sql
> 20260527012945_agent_metering_minimal.sql
> 20260528093200_add_asset_lineage_fields.sql
> 20260530183000_affiliate_tag_per_user.sql
> 20260530210000_meta_api_foundation.sql
> 20260531193000_fix_meta_config_column_privileges.sql
> 20260531200000_whatsapp_lead_engine.sql
> 20260531210000_meta_ads_metrics.sql
> 20260601000000_credential_encryption.sql
> 20260601000500_fix_meta_config_instead_of_trigger.sql
> 20260601000600_secure_definer_views.sql
> 20260601031300_constellation_v2_foundation.sql
> 20260601050000_embed_trigger_vault_key.sql
> 20260601060000_user_api_keys_apify_token.sql
> 20260602120000_wordpress_disconnect_rpc.sql
> 20260602130000_fix_user_api_keys_instead_of_double_fire.sql
> ```

## 🤖 Claude *(14:13:13)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nTOKEN=$(cat ~/.supabase/access-token 2>/dev/null)\nREF=bcyvddsykvehvpwstlfa\nif [ -z \"$TOKEN\" ]; then echo \"NO_TOKEN\"; exit 0; fi\nSQL=$(cat <<'EOF'\nSELECT json_build_object(\n  'vault_fns', (\n    SELECT json_agg(json_build_object(\n      'name', p.proname,\n      'args', pg_get_function_arguments(p.oid),\n      'result', pg_get_function_result(p.oid),\n      'secdef', p.prosecdef\n    ))\n    FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace\n    WHERE n.nspname = 'vault' AND p.proname IN ('create_secret','update_secret')\n  ),\n  'name_idx', (\n    SELECT json_build_object('indisunique', i.indisunique, 'indexname', c.relname)\n    FROM pg_index i JOIN pg_class c ON c.oid = i.indexrelid\n    WHERE c.relname = 'secrets_name_idx'\n  ),\n  'uak_fks', (\n    SELECT json_agg(json_build_object('name', conname, 'def', pg_get_constraintdef(oid)))\n    FROM pg_constraint\n    WHERE conrelid = 'public.user_api_keys_table'::regclass AND contype = 'f'\n  ),\n  'encrypt_fns', (\n    SELECT json_agg(json_build_object('name', p.proname, 'secdef', p.prosecdef, 'config', p.proconfig, 'owner', pg_get_userbyid(p.proowner)))\n    FROM pg_proc p JOIN pg_namespace n ON n.oid = p.pronamespace\n    WHERE n.nspname = 'public' AND p.proname IN ('trg_encrypt_user_api_keys','trg_encrypt_meta_config','trg_encrypt_social_accounts')\n  ),\n  'sample_user', (\n    SELECT json_build_object('user_id', user_id, 'has_groq', groq_api_key IS NOT NULL, 'has_wp', wp_app_password IS NOT NULL)\n    FROM public.user_api_keys_table LIMIT 1\n  )\n) AS probe;\nEOF\n)\necho \"=== CORE PROBE ===\"\njq -Rs '{query: .}' <<<\"$SQL\" | curl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d @-\necho\necho \"=== MIGRATIONS PROBE ===\"\njq -Rs '{query: .}' <<<\"SELECT json_agg(version ORDER BY version DESC) FROM (SELECT version FROM supabase_migrations.schema_migrations ORDER BY version DESC LIMIT 8) z;\" | curl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d @-\necho",
  "description": "Probe Vault API signatures, index uniqueness, FK, encrypt fn attrs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === CORE PROBE ===
> [{"probe":{"vault_fns":[{"name":"create_secret","args":"new_secret text, new_name text DEFAULT NULL::text, new_description text DEFAULT ''::text, new_key_id uuid DEFAULT NULL::uuid","result":"uuid","secdef":true},{"name":"update_secret","args":"secret_id uuid, new_secret text DEFAULT NULL::text, new_name text DEFAULT NULL::text, new_description text DEFAULT NULL::text, new_key_id uuid DEFAULT NULL::uuid","result":"void","secdef":true}],"name_idx":{"indisunique":true,"indexname":"secrets_name_idx"},"uak_fks":[{"name":"user_api_keys_user_id_fkey","def":"FOREIGN KEY (user_id) REFERENCES auth.users(id)"}],"encrypt_fns":[{"name":"trg_encrypt_meta_config","secdef":true,"config":null,"owner":"postgres"},{"name":"trg_encrypt_social_accounts","secdef":true,"config":null,"owner":"postgres"},{"name":"trg_encrypt_user_api_keys","secdef":true,"config":null,"owner":"postgres"}],"sample_user":{"user_id":"ada39fae-67e1-4e53-af1c-5a18e1c108e8","has_groq":true,"has_wp":false}}}]
> === MIGRATIONS PROBE ===
> [{"json_agg":["20260602130000","20260602120000","20260601060000","20260601050000","20260601031300","20260601000600","20260601000500","20260601000000"]}]
> ```

## 🤖 Claude *(14:16:36)*


## 🤖 Claude *(14:16:43)*

Probes materiais retornaram tudo que eu precisava confirmar:

- **`vault.update_secret(secret_id uuid, new_secret text DEFAULT NULL, ...)` EXISTE** e retorna `void` — o helper pode chamá-lo posicionalmente com `(v_id, p_value)`. ✅
- **`secrets_name_idx` `indisunique = true`** — confirma a premissa do bug. ✅
- **FK material:** `user_api_keys_user_id_fkey → auth.users(id)` — não posso usar uid sintético; tenho usuário real `ada39fae-67e1-4e53-af1c-5a18e1c108e8` (`has_wp=false`, coluna sacrificial perfeita). ✅
- As 3 encrypt fns são `secdef=true`, `config=null` (**sem search_path pinado** — fraqueza que o `/security-review` sinalizaria), owner `postgres`. ✅
- Última migration no DB e local: `20260602130000` → minha nova será `20260602140000`. ✅

Antes de escrever o teste, preciso caracterizar o endpoint `database/query` sem assumir nada: ele persiste GUC entre statements numa call? Retorna o último SELECT? Respeita BEGIN/ROLLBACK retornando o SELECT pré-rollback? Isso decide se faço o teste com rollback (zero persistência) ou com cleanup. Vou sondar.

## 🤖 Claude *(14:16:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nTOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\nq(){ jq -Rs '{query: .}' <<<\"$1\" | curl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d @-; echo; }\n\necho \"P1 jwt-context (GUC persists across statements in one call?):\"\nq \"SELECT set_config('request.jwt.claims', '{\\\"sub\\\":\\\"ada39fae-67e1-4e53-af1c-5a18e1c108e8\\\",\\\"role\\\":\\\"authenticated\\\"}', false); SELECT auth.uid()::text AS uid, auth.role() AS role;\"\n\necho \"P2 inventory (which columns are empty on the real user?):\"\nq \"SELECT json_build_object('wp_secret_count',(SELECT count(*) FROM vault.secrets WHERE name='user_api_keys_wp_app_password_ada39fae-67e1-4e53-af1c-5a18e1c108e8'),'row',(SELECT json_build_object('groq',groq_api_key IS NOT NULL,'openai',openai_api_key IS NOT NULL,'wp',wp_app_password IS NOT NULL,'apify',apify_token IS NOT NULL) FROM public.user_api_keys_table WHERE user_id='ada39fae-67e1-4e53-af1c-5a18e1c108e8'));\"\n\necho \"P3a which result set is returned (multi-statement)?:\"\nq \"SELECT 1 AS a; SELECT 2 AS b;\"\n\necho \"P3b txn rollback \u2014 does pre-ROLLBACK SELECT come back?:\"\nq \"BEGIN; SELECT 222 AS proof; ROLLBACK;\"",
  "description": "Characterize Management API query endpoint behavior"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> P1 jwt-context (GUC persists across statements in one call?):
> [{"uid":"ada39fae-67e1-4e53-af1c-5a18e1c108e8","role":"authenticated"}]
> P2 inventory (which columns are empty on the real user?):
> [{"json_build_object":{"wp_secret_count":0,"row":{"groq":true,"openai":true,"wp":false,"apify":true}}}]
> P3a which result set is returned (multi-statement)?:
> [{"b":2}]
> P3b txn rollback — does pre-ROLLBACK SELECT come back?:
> [{"proof":222}]
> ```

## 🤖 Claude *(14:19:00)*


## 🤖 Claude *(14:19:06)*

Endpoint totalmente caracterizado — resultado ideal:

- **P1:** GUC `request.jwt.claims` (is_local=false) persiste entre statements numa call; `auth.uid()`/`auth.role()` leem corretamente. ✅
- **P2:** usuário real tem `wp=false` e `wp_secret_count=0` → **`wp_app_password` é a coluna sacrificial perfeita** (vazia, sem segredo). ✅
- **P3a/P3b:** o endpoint retorna o **último SELECT** mesmo com `ROLLBACK` depois, e **o ROLLBACK desfaz tudo**. Logo posso rodar o teste inteiro em `BEGIN; … ; ROLLBACK;` → prova material na resposta, **zero persistência**, sem tocar dados reais. ✅✅

Mais três checagens materiais antes de escrever o SQL (não vou assumir): onde vive `gen_random_uuid` (impacta o `search_path=''` nas triggers meta/social), a semântica COALESCE-keep do `vault.update_secret`, as colunas de `schema_migrations`, e **reproduzir o bug 23505 na schema atual** (gold standard before/after).

## 🤖 Claude *(14:19:07)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Vault upsert-secret idempotent fix",
  "summary": "Fix 23505 on re-saving a credential: vault_upsert_secret helper + recreate 3 encrypt triggers"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Vault upsert-secret idempotent fix". Continue your current work.'}]
> ```

## 🤖 Claude *(14:19:15)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nTOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\nq(){ jq -Rs '{query: .}' <<<\"$1\" | curl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d @-; echo; }\n\necho \"C1 gen_random_uuid location(s):\"\nq \"SELECT json_agg(json_build_object('schema',n.nspname,'args',pg_get_function_arguments(p.oid))) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE p.proname='gen_random_uuid';\"\n\necho \"C2 vault.update_secret definition (verify COALESCE-keep of name):\"\nq \"SELECT pg_get_functiondef('vault.update_secret(uuid,text,text,text,uuid)'::regprocedure);\"\n\necho \"C3 schema_migrations columns:\"\nq \"SELECT json_agg(json_build_object('col',column_name,'type',data_type,'nullable',is_nullable)) FROM information_schema.columns WHERE table_schema='supabase_migrations' AND table_name='schema_migrations';\"\n\necho \"C4 REPRODUCE THE BUG (expect 23505 on 2nd save) \u2014 fully rolled back:\"\nq \"BEGIN; SELECT set_config('request.jwt.claims','{\\\"sub\\\":\\\"ada39fae-67e1-4e53-af1c-5a18e1c108e8\\\",\\\"role\\\":\\\"authenticated\\\"}', false); INSERT INTO public.user_api_keys (user_id, wp_site_url, wp_username, wp_app_password) VALUES ('ada39fae-67e1-4e53-af1c-5a18e1c108e8','https://test.example','tester','wp-pass-ALPHA'); INSERT INTO public.user_api_keys (user_id, wp_app_password) VALUES ('ada39fae-67e1-4e53-af1c-5a18e1c108e8','wp-pass-BRAVO'); SELECT 'should-not-reach' AS proof; ROLLBACK;\"",
  "description": "Verify gen_random_uuid/update_secret, get migrations cols, reproduce 23505"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> C1 gen_random_uuid location(s):
> [{"json_agg":[{"schema":"pg_catalog","args":""},{"schema":"extensions","args":""}]}]
> C2 vault.update_secret definition (verify COALESCE-keep of name):
> [{"pg_get_functiondef":"CREATE OR REPLACE FUNCTION vault.update_secret(secret_id uuid, new_secret text DEFAULT NULL::text, new_name text DEFAULT NULL::text, new_description text DEFAULT NULL::text, new_key_id uuid DEFAULT NULL::uuid)\n RETURNS void\n LANGUAGE plpgsql\n SECURITY DEFINER\n SET search_path TO ''\nAS $function$\nDECLARE\n  decrypted_secret text := (SELECT decrypted_secret FROM vault.decrypted_secrets WHERE id = secret_id);\nBEGIN\n  UPDATE vault.secrets s\n  SET\n    secret = CASE WHEN new_secret IS NULL THEN s.secret\n                  ELSE encode(vault._crypto_aead_det_encrypt(\n                    message := convert_to(new_secret, 'utf8'),\n                    additional := convert_to(s.id::text, 'utf8'),\n                    key_id := 0,\n                    context := 'pgsodium'::bytea,\n                    nonce := s.nonce\n                  ), 'base64') END,\n    name = coalesce(new_name, s.name),\n    description = coalesce(new_description, s.description),\n    updated_at = now()\n  WHERE s.id = secret_id;\nEND\n$function$\n"}]
> C3 schema_migrations columns:
> [{"json_agg":[{"col":"version","type":"text","nullable":"NO"},{"col":"statements","type":"ARRAY","nullable":"YES"},{"col":"name","type":"text","nullable":"YES"}]}]
> C4 REPRODUCE THE BUG (expect 23505 on 2nd save) — fully rolled back:
> {"message":"Failed to run sql query: ERROR:  23505: duplicate key value violates unique constraint \"secrets_name_idx\"\nDETAIL:  Key (name)=(user_api_keys_wp_app_password_ada39fae-67e1-4e53-af1c-5a18e1c108e8) already exists.\nCONTEXT:  SQL statement \"INSERT INTO vault.secrets (secret, name, description)\n  VALUES (\n    new_secret,\n    new_name,\n    new_description\n  )\n  RETURNING *\"\nPL/pgSQL function vault.create_secret(text,text,text,uuid) line 5 at SQL statement\nPL/pgSQL function public.trg_encrypt_user_api_keys() line 72 at assignment\nSQL statement \"UPDATE public.user_api_keys_table SET\n      groq_api_key              = COALESCE(NULLIF(NEW.groq_api_key, '••••••••••••'), public.user_api_keys_table.groq_api_key),\n      openrouter_api_key        = COALESCE(NULLIF(NEW.openrouter_api_key, '••••••••••••'), public.user_api_keys_table.openrouter_api_key),\n      openai_api_key            = COALESCE(NULLIF(NEW.openai_api_key, '••••••••••••'), public.user_api_keys_table.openai_api_key),\n      pref_audio_provider       = COALESCE(NEW.pref_audio_provider, public.user_api_keys_table.pref_audio_provider),\n      pref_image_provider       = COALESCE(NEW.pref_image_provider, public.user_api_keys_table.pref_image_provider),\n      pref_video_provider       = COALESCE(NEW.pref_video_provider, public.user_api_keys_table.pref_video_provider),\n      elevenlabs_api_key        = COALESCE(NULLIF(NEW.elevenlabs_api_key, '••••••••••••'), public.user_api_keys_table.elevenlabs_api_key),\n      google_api_key            = COALESCE(NULLIF(NEW.google_api_key, '••••••••••••'), public.user_api_keys_table.google_api_key),\n      nanobana_api_key          = COALESCE(NULLIF(NEW.nanobana_api_key, '••••••••••••'), public.user_api_keys_table.nanobana_api_key),\n      seedance_api_key          = COALESCE(NULLIF(NEW.seedance_api_key, '••••••••••••'), public.user_api_keys_table.seedance_api_key),\n      wp_site_url               = COALESCE(NEW.wp_site_url, public.user_api_keys_table.wp_site_url),\n      wp_username               = COALESCE(NEW.wp_username, public.user_api_keys_table.wp_username),\n      wp_app_password           = COALESCE(NULLIF(NEW.wp_app_password, '••••••••••••'), public.user_api_keys_table.wp_app_password),\n      pref_ai_model             = COALESCE(NEW.pref_ai_model, public.user_api_keys_table.pref_ai_model),\n      replicate_api_key         = COALESCE(NULLIF(NEW.replicate_api_key, '••••••••••••'), public.user_api_keys_table.replicate_api_key),\n      higgsfield_api_key        = COALESCE(NULLIF(NEW.higgsfield_api_key, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key),\n      higgsfield_api_key_secret = COALESCE(NULLIF(NEW.higgsfield_api_key_secret, '••••••••••••'), public.user_api_keys_table.higgsfield_api_key_secret),\n      apify_token               = COALESCE(NULLIF(NEW.apify_token, '••••••••••••'), public.user_api_keys_table.apify_token),\n      updated_at                = now()\n    WHERE user_id = NEW.user_id\"\nPL/pgSQL function public.trg_instead_of_user_api_keys() line 19 at SQL statement\n"}
> ```

## 🤖 Claude *(14:20:28)*


## 🤖 Claude *(14:20:34)*

Quatro confirmações materiais decisivas:

- **C1:** `gen_random_uuid` está em `pg_catalog` **e** `extensions` → bareword resolve via pg_catalog mesmo com `search_path=''`. Seguro manter nas triggers meta/social. ✅
- **C2:** `vault.update_secret` faz `name = coalesce(new_name, s.name)` → chamar com 2 args **preserva nome+descrição** e só rotaciona o valor. Exatamente o que o helper precisa. ✅
- **C3:** `schema_migrations(version text NOT NULL, statements text[], name text)` → posso registrar histórico. ✅
- **C4: BUG REPRODUZIDO MATERIALMENTE** — `ERROR 23505 duplicate key ... secrets_name_idx ... Key (name)=(user_api_keys_wp_app_password_ada39fae...) already exists ... vault.create_secret ... trg_encrypt_user_api_keys() line 72`. Gold-standard before. Txn revertida, dados reais intactos. ✅

Uma última checagem load-bearing: o helper roda como `postgres` (definer) e faz `SELECT ... FROM vault.secrets` direto — preciso confirmar que `postgres` tem esse privilégio em produção (não via função SD da Vault).

## 🤖 Claude *(14:20:39)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nTOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\nq(){ jq -Rs '{query: .}' <<<\"$1\" | curl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d @-; echo; }\n\necho \"Role + postgres privileges on vault.secrets (load-bearing for the helper's direct SELECT):\"\nq \"SELECT json_build_object('conn_role',current_user,'pg_select',has_table_privilege('postgres','vault.secrets','SELECT'),'pg_insert',has_table_privilege('postgres','vault.secrets','INSERT'),'pg_update',has_table_privilege('postgres','vault.secrets','UPDATE'),'disconnect_wp_owner',(SELECT pg_get_userbyid(proowner) FROM pg_proc WHERE proname='disconnect_wordpress' LIMIT 1));\"",
  "description": "Confirm postgres can SELECT vault.secrets directly"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Role + postgres privileges on vault.secrets (load-bearing for the helper's direct SELECT):
> [{"json_build_object":{"conn_role":"postgres","pg_select":true,"pg_insert":false,"pg_update":false,"disconnect_wp_owner":"postgres"}}]
> ```

## 🤖 Claude *(14:22:11)*


## 🤖 Claude *(14:22:15)*

Decisivo:
- `conn_role = postgres`; **`pg_select = true`** em `vault.secrets` → o `SELECT id ... WHERE name=` do helper funciona em produção (helper roda como postgres). ✅
- `pg_insert/pg_update = false` → postgres **não** escreve direto em `vault.secrets`; por isso o helper delega a escrita às primitivas `vault.create_secret`/`vault.update_secret` (SECURITY DEFINER de outro owner), que o postgres já invoca com sucesso hoje (provado em C4). Design correto. ✅
- `disconnect_wordpress` owner = postgres (consistente com o SOP). ✅

Tenho certeza total. Vou escrever a migration.

## 🤖 Claude *(14:23:16)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql",
  "content": "-- Migration: idempotent credential encryption \u2014 vault_upsert_secret() eliminates the\n--            re-save unique_violation (23505) across all three Vault-backed credential tables.\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- Bug (latent debt flagged 2026-06-02 in docs/processes/credential-disconnect-clear.md, and\n-- reproduced materially the same day): the BEFORE INSERT/UPDATE encryption triggers\n-- (trg_encrypt_user_api_keys, trg_encrypt_meta_config, trg_encrypt_social_accounts) call\n-- vault.create_secret(value, '<deterministic-name>') UNCONDITIONALLY whenever a secret column\n-- changes value. vault.create_secret does a plain `INSERT INTO vault.secrets` with NO ON CONFLICT,\n-- and vault.secrets.name carries a UNIQUE index (secrets_name_idx). So rotating a stored secret to\n-- a NEW value while the same-named secret still exists throws:\n--     ERROR 23505 duplicate key value violates unique constraint \"secrets_name_idx\"\n-- User-facing manifestation: WordPress \"Editar \u2192 save a new app-password WITHOUT disconnecting\n-- first\" (src/pages/SocialAccountsPage.tsx). Sibling tables share the shape (names keyed by row id),\n-- so re-saving a Meta long-lived token / pages list, or a social access/refresh token, on an\n-- existing row collides identically.\n--\n-- Already fixed separately (NOT this migration): the INSTEAD OF double-fire of the encrypt trigger\n-- (20260602130000_fix_user_api_keys_instead_of_double_fire.sql, UPDATE-first). connect \u2192 disconnect\n-- \u2192 reconnect already works because disconnect_wordpress() deletes the secret first. The case left\n-- open was strictly \"rotate the value in place without deleting first\".\n--\n-- Fix: a single idempotent helper public.vault_upsert_secret(value, name, desc) that resolves an\n-- existing secret BY NAME (vault.secrets.name is unique) and rotates it in place via\n-- vault.update_secret (which COALESCE-keeps name + description, re-encrypting only the value), else\n-- creates it. The vault.create_secret call-sites in each of the three encryption triggers are\n-- swapped for this helper, preserving the existing \"already a UUID reference \u2192 keep\" guard and the\n-- \"only when the value actually changed\" (IS DISTINCT FROM) guard. The stored column keeps pointing\n-- at the SAME Vault UUID across rotations (update-in-place), so decrypted_* views transparently\n-- reflect the new value and no orphan secrets accumulate.\n--\n-- Security posture (this migration HARDENS; per CLAUDE.md every migration passes /security-review):\n--   * vault_upsert_secret is SECURITY DEFINER with `SET search_path = ''` and every object schema-\n--     qualified \u2014 closing the search_path-injection vector a definer function otherwise carries.\n--   * EXECUTE on the helper is REVOKED from PUBLIC/anon/authenticated. It is an internal primitive\n--     called only by the (already definer, owner=postgres) encryption triggers; it must NOT be a\n--     PostgREST-reachable RPC, since by-name access would otherwise let a caller overwrite ANY\n--     tenant's secret. The triggers run as postgres (their definer) and retain EXECUTE as owner.\n--   * The three encryption trigger functions are ALSO pinned to `SET search_path = ''` (they had no\n--     pin before \u2014 proconfig was null), matching the precedent set by 20260602130000. postgres keeps\n--     the SELECT it already holds on vault.secrets; the privileged Vault writes stay inside the\n--     SECURITY DEFINER vault.create_secret/update_secret primitives (postgres has EXECUTE, not direct\n--     INSERT/UPDATE on vault.secrets \u2014 verified materially 2026-06-02).\n--\n-- Scope: all three credential tables (user_api_keys, meta_config, social_accounts). Triggers keep\n-- their bindings (CREATE OR REPLACE FUNCTION preserves the function oid) \u2014 no trigger re-create.\n\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- 1. IDEMPOTENT VAULT HELPER\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nCREATE OR REPLACE FUNCTION public.vault_upsert_secret(\n  p_value text,\n  p_name  text,\n  p_desc  text DEFAULT ''\n)\nRETURNS uuid\nLANGUAGE plpgsql\nSECURITY DEFINER\nSET search_path = ''\nAS $$\nDECLARE\n  v_id uuid;\nBEGIN\n  -- vault.secrets.name is UNIQUE (secrets_name_idx). Resolve an existing secret by its\n  -- deterministic name and rotate the value in place \u2014 this is what makes re-saving a credential\n  -- idempotent instead of throwing unique_violation (23505). vault.update_secret COALESCE-keeps the\n  -- name + description and re-encrypts only the value, so the stored UUID reference never changes.\n  SELECT id INTO v_id FROM vault.secrets WHERE name = p_name;\n\n  IF v_id IS NOT NULL THEN\n    PERFORM vault.update_secret(v_id, p_value);\n    RETURN v_id;\n  END IF;\n\n  RETURN vault.create_secret(p_value, p_name, p_desc);\n\nEXCEPTION\n  -- Concurrency guard: a parallel writer created the same name between our SELECT and\n  -- create_secret. Re-resolve and update in place rather than surfacing 23505 to the caller.\n  WHEN unique_violation THEN\n    SELECT id INTO v_id FROM vault.secrets WHERE name = p_name;\n    IF v_id IS NOT NULL THEN\n      PERFORM vault.update_secret(v_id, p_value);\n      RETURN v_id;\n    END IF;\n    RAISE;\nEND;\n$$;\n\nCOMMENT ON FUNCTION public.vault_upsert_secret(text, text, text) IS\n  'Internal: idempotent Vault secret write keyed by deterministic name (update-in-place when the '\n  'name exists, else create). Called ONLY by the credential encryption triggers \u2014 EXECUTE is revoked '\n  'from clients. Eliminates the secrets_name_idx 23505 on credential re-save.';\n\n-- Internal primitive only \u2014 never a client-reachable RPC (would allow by-name cross-tenant overwrite).\nREVOKE ALL ON FUNCTION public.vault_upsert_secret(text, text, text) FROM PUBLIC;\nREVOKE ALL ON FUNCTION public.vault_upsert_secret(text, text, text) FROM anon, authenticated;\n\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- 2. user_api_keys encryption trigger \u2014 swap vault.create_secret \u2192 public.vault_upsert_secret\n--    (latest definition as of 20260601060000, incl. apify_token; + search_path pin)\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nCREATE OR REPLACE FUNCTION public.trg_encrypt_user_api_keys()\nRETURNS TRIGGER\nLANGUAGE plpgsql\nSECURITY DEFINER\nSET search_path = ''\nAS $$\nDECLARE\n  v_id UUID;\nBEGIN\n  -- groq_api_key\n  IF NEW.groq_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.groq_api_key IS DISTINCT FROM OLD.groq_api_key) THEN\n    IF NEW.groq_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n      -- keep existing UUID reference\n    ELSE\n      v_id := public.vault_upsert_secret(NEW.groq_api_key, 'user_api_keys_groq_api_key_' || NEW.user_id::text, 'Groq API Key');\n      NEW.groq_api_key = v_id::text;\n    END IF;\n  END IF;\n\n  -- openrouter_api_key\n  IF NEW.openrouter_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openrouter_api_key IS DISTINCT FROM OLD.openrouter_api_key) THEN\n    IF NEW.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n      -- keep existing UUID reference\n    ELSE\n      v_id := public.vault_upsert_secret(NEW.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || NEW.user_id::text, 'OpenRouter API Key');\n      NEW.openrouter_api_key = v_id::text;\n    END IF;\n  END IF;\n\n  -- openai_api_key\n  IF NEW.openai_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openai_api_key IS DISTINCT FROM OLD.openai_api_key) THEN\n    IF NEW.openai_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n      -- keep existing UUID reference\n    ELSE\n      v_id := public.vault_upsert_secret(NEW.openai_api_key, 'user_api_keys_openai_api_key_' || NEW.user_id::text, 'OpenAI API Key');\n      NEW.openai_api_key = v_id::text;\n    END IF;\n  END IF;\n\n  -- elevenlabs_api_key\n  IF NEW.elevenlabs_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.elevenlabs_api_key IS DISTINCT FROM OLD.elevenlabs_api_key) THEN\n    IF NEW.elevenlabs_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n      -- keep existing UUID reference\n    ELSE\n      v_id := public.vault_upsert_secret(NEW.elevenlabs_api_key, 'user_api_keys_elevenlabs_api_key_' || NEW.user_id::text, 'ElevenLabs API Key');\n      NEW.elevenlabs_api_key = v_id::text;\n    END IF;\n  END IF;\n\n  -- google_api_key\n  IF NEW.google_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.google_api_key IS DISTINCT FROM OLD.google_api_key) THEN\n    IF NEW.google_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n      -- keep existing UUID reference\n    ELSE\n      v_id := public.vault_upsert_secret(NEW.google_api_key, 'user_api_keys_google_api_key_' || NEW.user_id::text, 'Google API Key');\n      NEW.google_api_key = v_id::text;\n    END IF;\n  END IF;\n\n  -- nanobana_api_key\n  IF NEW.nanobana_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.nanobana_api_key IS DISTINCT FROM OLD.nanobana_api_key) THEN\n    IF NEW.nanobana_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n      -- keep existing UUID reference\n    ELSE\n      v_id := public.vault_upsert_secret(NEW.nanobana_api_key, 'user_api_keys_nanobana_api_key_' || NEW.user_id::text, 'Nanobana API Key');\n      NEW.nanobana_api_key = v_id::text;\n    END IF;\n  END IF;\n\n  -- seedance_api_key\n  IF NEW.seedance_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.seedance_api_key IS DISTINCT FROM OLD.seedance_api_key) THEN\n    IF NEW.seedance_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n      -- keep existing UUID reference\n    ELSE\n      v_id := public.vault_upsert_secret(NEW.seedance_api_key, 'user_api_keys_seedance_api_key_' || NEW.user_id::text, 'Seedance API Key');\n      NEW.seedance_api_key = v_id::text;\n    END IF;\n  END IF;\n\n  -- wp_app_password\n  IF NEW.wp_app_password IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.wp_app_password IS DISTINCT FROM OLD.wp_app_password) THEN\n    IF NEW.wp_app_password ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n      -- keep existing UUID reference\n    ELSE\n      v_id := public.vault_upsert_secret(NEW.wp_app_password, 'user_api_keys_wp_app_password_' || NEW.user_id::text, 'WordPress App Password');\n      NEW.wp_app_password = v_id::text;\n    END IF;\n  END IF;\n\n  -- replicate_api_key\n  IF NEW.replicate_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.replicate_api_key IS DISTINCT FROM OLD.replicate_api_key) THEN\n    IF NEW.replicate_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n      -- keep existing UUID reference\n    ELSE\n      v_id := public.vault_upsert_secret(NEW.replicate_api_key, 'user_api_keys_replicate_api_key_' || NEW.user_id::text, 'Replicate API Key');\n      NEW.replicate_api_key = v_id::text;\n    END IF;\n  END IF;\n\n  -- higgsfield_api_key\n  IF NEW.higgsfield_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.higgsfield_api_key IS DISTINCT FROM OLD.higgsfield_api_key) THEN\n    IF NEW.higgsfield_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n      -- keep existing UUID reference\n    ELSE\n      v_id := public.vault_upsert_secret(NEW.higgsfield_api_key, 'user_api_keys_higgsfield_api_key_' || NEW.user_id::text, 'Higgsfield API Key');\n      NEW.higgsfield_api_key = v_id::text;\n    END IF;\n  END IF;\n\n  -- higgsfield_api_key_secret\n  IF NEW.higgsfield_api_key_secret IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.higgsfield_api_key_secret IS DISTINCT FROM OLD.higgsfield_api_key_secret) THEN\n    IF NEW.higgsfield_api_key_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n      -- keep existing UUID reference\n    ELSE\n      v_id := public.vault_upsert_secret(NEW.higgsfield_api_key_secret, 'user_api_keys_higgsfield_api_key_secret_' || NEW.user_id::text, 'Higgsfield API Key Secret');\n      NEW.higgsfield_api_key_secret = v_id::text;\n    END IF;\n  END IF;\n\n  -- apify_token\n  IF NEW.apify_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.apify_token IS DISTINCT FROM OLD.apify_token) THEN\n    IF NEW.apify_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n      -- keep existing UUID reference\n    ELSE\n      v_id := public.vault_upsert_secret(NEW.apify_token, 'user_api_keys_apify_token_' || NEW.user_id::text, 'Apify Token');\n      NEW.apify_token = v_id::text;\n    END IF;\n  END IF;\n\n  RETURN NEW;\nEND;\n$$;\n\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- 3. meta_config encryption trigger \u2014 swap vault.create_secret \u2192 public.vault_upsert_secret\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nCREATE OR REPLACE FUNCTION public.trg_encrypt_meta_config()\nRETURNS TRIGGER\nLANGUAGE plpgsql\nSECURITY DEFINER\nSET search_path = ''\nAS $$\nDECLARE\n  v_token_id UUID;\n  v_pages_id UUID;\nBEGIN\n  IF NEW.id IS NULL THEN\n    NEW.id := gen_random_uuid();\n  END IF;\n\n  IF NEW.long_lived_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.long_lived_token IS DISTINCT FROM OLD.long_lived_token) THEN\n    IF NEW.long_lived_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n      -- keep existing UUID reference\n    ELSE\n      v_token_id := public.vault_upsert_secret(NEW.long_lived_token, 'meta_config_long_lived_token_' || NEW.id::text, 'Meta config long-lived token');\n      NEW.long_lived_token = v_token_id::text;\n    END IF;\n  END IF;\n\n  IF NEW.pages IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.pages IS DISTINCT FROM OLD.pages) THEN\n    IF NEW.pages::text ~ '^\"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\"$' THEN\n      -- keep existing UUID JSON reference\n    ELSE\n      v_pages_id := public.vault_upsert_secret(NEW.pages::text, 'meta_config_pages_' || NEW.id::text, 'Meta config pages list');\n      NEW.pages = to_jsonb(v_pages_id::text);\n    END IF;\n  END IF;\n\n  RETURN NEW;\nEND;\n$$;\n\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\n-- 4. social_accounts encryption trigger \u2014 swap vault.create_secret \u2192 public.vault_upsert_secret\n-- \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\nCREATE OR REPLACE FUNCTION public.trg_encrypt_social_accounts()\nRETURNS TRIGGER\nLANGUAGE plpgsql\nSECURITY DEFINER\nSET search_path = ''\nAS $$\nDECLARE\n  v_access_token_id UUID;\n  v_refresh_token_id UUID;\nBEGIN\n  IF NEW.id IS NULL THEN\n    NEW.id := gen_random_uuid();\n  END IF;\n\n  IF NEW.access_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.access_token IS DISTINCT FROM OLD.access_token) THEN\n    IF NEW.access_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n      -- keep existing UUID reference\n    ELSE\n      v_access_token_id := public.vault_upsert_secret(NEW.access_token, 'social_accounts_access_token_' || NEW.id::text, 'Social account access token');\n      NEW.access_token = v_access_token_id::text;\n    END IF;\n  END IF;\n\n  IF NEW.refresh_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.refresh_token IS DISTINCT FROM OLD.refresh_token) THEN\n    IF NEW.refresh_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN\n      -- keep existing UUID reference\n    ELSE\n      v_refresh_token_id := public.vault_upsert_secret(NEW.refresh_token, 'social_accounts_refresh_token_' || NEW.id::text, 'Social account refresh token');\n      NEW.refresh_token = v_refresh_token_id::text;\n    END IF;\n  END IF;\n\n  RETURN NEW;\nEND;\n$$;\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(14:23:34)*


## 🤖 Claude *(14:23:35)*

Migration escrita. Agora aplico via Management API, **envelopada em `BEGIN; … COMMIT;`** para atomicidade (tudo-ou-nada), com registro idempotente em `schema_migrations` (via `WHERE NOT EXISTS`, robusto a ausência de constraint).

## 🤖 Claude *(14:23:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nTOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\nAPPLY=/tmp/apply_20260602140000.sql\n{\n  echo \"BEGIN;\"\n  cat supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql\n  echo \"INSERT INTO supabase_migrations.schema_migrations (version, name)\"\n  echo \"SELECT '20260602140000','vault_upsert_secret_idempotent_encrypt'\"\n  echo \"WHERE NOT EXISTS (SELECT 1 FROM supabase_migrations.schema_migrations WHERE version='20260602140000');\"\n  echo \"COMMIT;\"\n  echo \"SELECT 'applied' AS status;\"\n} > \"$APPLY\"\necho \"Payload bytes: $(wc -c < \"$APPLY\")\"\necho \"=== APPLY RESULT ===\"\njq -Rs '{query: .}' < \"$APPLY\" | curl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" \\\n  -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d @-\necho",
  "description": "Apply migration in a transaction via Management API"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Payload bytes: 17138
> === APPLY RESULT ===
> [{"status":"applied"}]
> ```

## 🤖 Claude *(14:24:01)*


## 🤖 Claude *(14:24:03)*

Migration aplicada e commitada: **`[{"status":"applied"}]`**. Agora a verificação material do artefato aplicado — metadados das 4 funções (secdef, search_path pinado, fonte chama o helper e não mais `vault.create_secret`), o lockdown de EXECUTE do helper, e o registro em `schema_migrations`.

## 🤖 Claude *(14:24:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nTOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\nq(){ jq -Rs '{query: .}' <<<\"$1\" | curl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d @-; echo; }\n\necho \"V1 function metadata (secdef + search_path pin + source references helper, not create_secret):\"\nq \"SELECT json_agg(json_build_object('name',p.proname,'secdef',p.prosecdef,'config',p.proconfig,'calls_helper',position('vault_upsert_secret' in pg_get_functiondef(p.oid))>0,'calls_create_secret',position('vault.create_secret' in pg_get_functiondef(p.oid))>0) ORDER BY p.proname) FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='public' AND p.proname IN ('vault_upsert_secret','trg_encrypt_user_api_keys','trg_encrypt_meta_config','trg_encrypt_social_accounts');\"\n\necho \"V2 helper EXECUTE lockdown (anon/authenticated must be FALSE):\"\nq \"SELECT json_build_object('anon',has_function_privilege('anon','public.vault_upsert_secret(text,text,text)','EXECUTE'),'authenticated',has_function_privilege('authenticated','public.vault_upsert_secret(text,text,text)','EXECUTE'),'postgres',has_function_privilege('postgres','public.vault_upsert_secret(text,text,text)','EXECUTE'));\"\n\necho \"V3 schema_migrations row registered:\"\nq \"SELECT json_agg(json_build_object('version',version,'name',name)) FROM supabase_migrations.schema_migrations WHERE version='20260602140000';\"",
  "description": "Verify applied function metadata, grants, migration record"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> V1 function metadata (secdef + search_path pin + source references helper, not create_secret):
> [{"json_agg":[{"name":"trg_encrypt_meta_config","secdef":true,"config":["search_path=\"\""],"calls_helper":true,"calls_create_secret":false},{"name":"trg_encrypt_social_accounts","secdef":true,"config":["search_path=\"\""],"calls_helper":true,"calls_create_secret":false},{"name":"trg_encrypt_user_api_keys","secdef":true,"config":["search_path=\"\""],"calls_helper":true,"calls_create_secret":false},{"name":"vault_upsert_secret","secdef":true,"config":["search_path=\"\""],"calls_helper":true,"calls_create_secret":true}]}]
> V2 helper EXECUTE lockdown (anon/authenticated must be FALSE):
> [{"json_build_object":{"anon":false,"authenticated":false,"postgres":true}}]
> V3 schema_migrations row registered:
> [{"json_agg":[{"version":"20260602140000","name":"vault_upsert_secret_idempotent_encrypt"}]}]
> ```

## 🤖 Claude *(14:24:32)*


## 🤖 Claude *(14:24:36)*

Verificação material do artefato aplicado — tudo verde:

- **V1:** as 3 triggers agora `calls_create_secret=false` + `calls_helper=true`, todas com `search_path=""` pinado e `secdef=true`. O helper é o único lugar com `create_secret` (fallback). ✅
- **V2:** lockdown do helper — `anon=false`, `authenticated=false`, `postgres=true`. Não é RPC alcançável por cliente. ✅
- **V3:** migration registrada em `schema_migrations`. ✅

Agora o **fix-test (o "depois" do gold-standard)**: o mesmo duplo-save que deu 23505 em C4, agora dentro de `BEGIN; … ; ROLLBACK;`. Mais o no-leakage check provando que os dados reais continuam intactos.

## 🤖 Claude *(14:24:45)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nTOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\nUID=ada39fae-67e1-4e53-af1c-5a18e1c108e8\nq(){ jq -Rs '{query: .}' <<<\"$1\" | curl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d @-; echo; }\n\necho \"FIX-TEST (same double-save that threw 23505 in C4 \u2014 now must succeed; fully rolled back):\"\nq \"BEGIN;\nSELECT set_config('request.jwt.claims','{\\\"sub\\\":\\\"$UID\\\",\\\"role\\\":\\\"authenticated\\\"}', false);\nINSERT INTO public.user_api_keys (user_id, wp_site_url, wp_username, wp_app_password) VALUES ('$UID','https://test.example','tester','wp-pass-ALPHA');\nINSERT INTO public.user_api_keys (user_id, wp_app_password) VALUES ('$UID','wp-pass-BRAVO');\nSELECT json_build_object(\n  'decrypted_wp', (SELECT wp_app_password FROM public.decrypted_user_api_keys WHERE user_id='$UID'),\n  'secret_count', (SELECT count(*) FROM vault.secrets WHERE name='user_api_keys_wp_app_password_$UID'),\n  'col_is_uuid_ref', (SELECT wp_app_password ~ '^[0-9a-f]{8}-[0-9a-f]{4}-' FROM public.user_api_keys_table WHERE user_id='$UID'),\n  'sibling_groq_intact', (SELECT groq_api_key IS NOT NULL FROM public.user_api_keys_table WHERE user_id='$UID')\n) AS proof;\nROLLBACK;\"\n\necho \"NO-LEAKAGE (real user untouched after rollback) + sibling-table row counts:\"\nq \"SELECT json_build_object('wp_still_null',(SELECT wp_app_password IS NULL FROM public.user_api_keys_table WHERE user_id='$UID'),'wp_secret_count',(SELECT count(*) FROM vault.secrets WHERE name='user_api_keys_wp_app_password_$UID'),'meta_config_rows',(SELECT count(*) FROM public.meta_config_table),'social_accounts_rows',(SELECT count(*) FROM public.social_accounts_table));\"",
  "description": "Run after-fix double-save proof and no-leakage check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /bin/bash: line 24: UID: readonly variable
> FIX-TEST (same double-save that threw 23505 in C4 — now must succeed; fully rolled back):
> {"message":"Failed to run sql query: ERROR:  22P02: invalid input syntax for type uuid: \"1001\"\nLINE 3: INSERT INTO public.user_api_keys (user_id, wp_site_url, wp_username, wp_app_password) VALUES ('1001','https://test.example','tester','wp-pass-ALPHA');\n                                                                                                      ^\n"}
> NO-LEAKAGE (real user untouched after rollback) + sibling-table row counts:
> {"message":"Failed to run sql query: ERROR:  22P02: invalid input syntax for type uuid: \"1001\"\nLINE 1: SELECT json_build_object('wp_still_null',(SELECT wp_app_password IS NULL FROM public.user_api_keys_table WHERE user_id='1001'),'wp_secret_count',(SELECT count(*) FROM vault.secrets WHERE name='user_api_keys_wp_app_password_1001'),'meta_config_rows',(SELECT count(*) FROM public.meta_config_table),'social_accounts_rows',(SELECT count(*) FROM public.social_accounts_table));\n                                                                                                                               ^\n"}
> ```

## 🤖 Claude *(14:24:54)*


## 🤖 Claude *(14:24:56)*

`UID` é variável readonly do bash (= 1001, o uid do shell), então `$UID` virou `'1001'` e o cast pra uuid falhou antes de tocar a lógica — resultado inválido, nada foi executado no trigger. Armadilha de ambiente. Vou refazer com outro nome de variável.

## 🤖 Claude *(14:25:05)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nTOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\nU=ada39fae-67e1-4e53-af1c-5a18e1c108e8\nq(){ jq -Rs '{query: .}' <<<\"$1\" | curl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d @-; echo; }\n\necho \"FIX-TEST (same double-save that threw 23505 in C4 \u2014 now must succeed; fully rolled back):\"\nq \"BEGIN;\nSELECT set_config('request.jwt.claims','{\\\"sub\\\":\\\"$U\\\",\\\"role\\\":\\\"authenticated\\\"}', false);\nINSERT INTO public.user_api_keys (user_id, wp_site_url, wp_username, wp_app_password) VALUES ('$U','https://test.example','tester','wp-pass-ALPHA');\nINSERT INTO public.user_api_keys (user_id, wp_app_password) VALUES ('$U','wp-pass-BRAVO');\nSELECT json_build_object(\n  'decrypted_wp', (SELECT wp_app_password FROM public.decrypted_user_api_keys WHERE user_id='$U'),\n  'secret_count', (SELECT count(*) FROM vault.secrets WHERE name='user_api_keys_wp_app_password_$U'),\n  'col_is_uuid_ref', (SELECT wp_app_password ~ '^[0-9a-f]{8}-[0-9a-f]{4}-' FROM public.user_api_keys_table WHERE user_id='$U'),\n  'sibling_groq_intact', (SELECT groq_api_key IS NOT NULL FROM public.user_api_keys_table WHERE user_id='$U')\n) AS proof;\nROLLBACK;\"\n\necho \"NO-LEAKAGE (real user untouched after rollback) + sibling-table row counts:\"\nq \"SELECT json_build_object('wp_still_null',(SELECT wp_app_password IS NULL FROM public.user_api_keys_table WHERE user_id='$U'),'wp_secret_count',(SELECT count(*) FROM vault.secrets WHERE name='user_api_keys_wp_app_password_$U'),'meta_config_rows',(SELECT count(*) FROM public.meta_config_table),'social_accounts_rows',(SELECT count(*) FROM public.social_accounts_table));\"",
  "description": "Rerun after-fix double-save proof with non-readonly var"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> FIX-TEST (same double-save that threw 23505 in C4 — now must succeed; fully rolled back):
> [{"proof":{"decrypted_wp":"wp-pass-BRAVO","secret_count":1,"col_is_uuid_ref":true,"sibling_groq_intact":true}}]
> NO-LEAKAGE (real user untouched after rollback) + sibling-table row counts:
> [{"json_build_object":{"wp_still_null":true,"wp_secret_count":0,"meta_config_rows":0,"social_accounts_rows":3}}]
> ```

## 🤖 Claude *(14:26:20)*


## 🤖 Claude *(14:26:24)*

**FIX-TEST passou materialmente** — o mesmo duplo-save que deu 23505 em C4 agora retorna:
- `decrypted_wp: "wp-pass-BRAVO"` ✅ (2º valor refletido na view decifrada)
- `secret_count: 1` ✅ (update-in-place, sem órfão/duplicata)
- `col_is_uuid_ref: true` ✅ (coluna mantém a referência UUID rotacionada)
- `sibling_groq_intact: true` ✅ (chave irmã não tocada) · **sem 23505** ✅

**No-leakage:** `wp_still_null: true`, `wp_secret_count: 0` → ROLLBACK funcionou, dados reais intactos. ✅

`social_accounts_rows: 3` (meta_config: 0). Como há linhas reais de social_accounts, vou **provar materialmente o fix da trigger irmã** com um duplo-save direto na base table (que dispara a mesma BEFORE trigger corrigida), tudo revertido.

## 🤖 Claude *(14:26:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nTOKEN=$(cat ~/.supabase/access-token)\nREF=bcyvddsykvehvpwstlfa\nq(){ jq -Rs '{query: .}' <<<\"$1\" | curl -s -X POST \"https://api.supabase.com/v1/projects/$REF/database/query\" -H \"Authorization: Bearer $TOKEN\" -H \"Content-Type: application/json\" -d @-; echo; }\n\necho \"SIBLING FIX-TEST \u2014 social_accounts double-rotation of access_token on a real row (fires tr_encrypt_social_accounts \u2192 vault_upsert_secret); fully rolled back:\"\nq \"BEGIN;\nUPDATE public.social_accounts_table SET access_token='sa-ALPHA' WHERE id = (SELECT id FROM public.social_accounts_table ORDER BY id LIMIT 1);\nUPDATE public.social_accounts_table SET access_token='sa-BRAVO' WHERE id = (SELECT id FROM public.social_accounts_table ORDER BY id LIMIT 1);\nSELECT json_build_object(\n  'row_id', (SELECT id FROM public.social_accounts_table ORDER BY id LIMIT 1),\n  'decrypted_access', (SELECT access_token FROM public.decrypted_social_accounts WHERE id=(SELECT id FROM public.social_accounts_table ORDER BY id LIMIT 1)),\n  'secret_count', (SELECT count(*) FROM vault.secrets WHERE name='social_accounts_access_token_'||(SELECT id::text FROM public.social_accounts_table ORDER BY id LIMIT 1)),\n  'col_is_uuid_ref', (SELECT access_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-' FROM public.social_accounts_table ORDER BY id LIMIT 1)\n) AS proof;\nROLLBACK;\"\n\necho \"POST-ROLLBACK sanity (social rows still 3, first row access_token shape unchanged):\"\nq \"SELECT json_build_object('social_rows',(SELECT count(*) FROM public.social_accounts_table),'first_row_access_present',(SELECT access_token IS NOT NULL FROM public.social_accounts_table ORDER BY id LIMIT 1));\"",
  "description": "Material double-save proof on social_accounts sibling trigger"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> SIBLING FIX-TEST — social_accounts double-rotation of access_token on a real row (fires tr_encrypt_social_accounts → vault_upsert_secret); fully rolled back:
> [{"proof":{"row_id":"39ce0ebb-3579-481a-93ce-8a20759cd22e","decrypted_access":"sa-BRAVO","secret_count":1,"col_is_uuid_ref":true}}]
> POST-ROLLBACK sanity (social rows still 3, first row access_token shape unchanged):
> [{"json_build_object":{"social_rows":3,"first_row_access_present":true}}]
> ```

## 🤖 Claude *(14:27:31)*


## 🤖 Claude *(14:27:35)*

**Sibling fix-test passou materialmente** (social_accounts, linha real `39ce0ebb-…`): `decrypted_access: "sa-BRAVO"`, `secret_count: 1`, `col_is_uuid_ref: true`, **sem 23505**. Pós-rollback: 3 linhas intactas, token original preservado. ✅

Prova material agora completa: **user_api_keys (antes 23505 / depois OK)** + **social_accounts (depois OK)** em segredos reais do Vault; meta_config tem 0 linhas (coberto pelo helper compartilhado + V1 source-level). 

Falta: atualizar docs (SOP + CLAUDE.md) e rodar o **`/security-review` obrigatório**. Vou editar o SOP e localizar a âncora no CLAUDE.md em paralelo.

## 🤖 Claude *(14:27:48)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/credential-disconnect-clear.md",
  "old_string": "## Known latent debt (discovered 2026-06-02 \u2014 flagged, out of this fix's scope)\n\nThe encryption trigger (`trg_encrypt_user_api_keys` and its `meta_config`/`social_accounts` siblings)\ncalls `vault.create_secret(value, '<deterministic-name>')` **unconditionally** when a secret column\nchanges. `vault.create_secret` does a plain INSERT with **no ON CONFLICT**, and `vault.secrets.name`\nis UNIQUE \u2192 **re-saving a credential while one already exists for that name throws `unique_violation`**.\nFor WordPress this hits the \"Editar \u2192 save new password without disconnecting first\" path. Connect \u2192\ndisconnect \u2192 reconnect works because `disconnect_wordpress()` deletes the secret. The robust fix is to\nmake the encryption trigger idempotent (update-in-place when the deterministic name already exists)\nacross all three tables \u2014 tracked as a follow-up; it touches the security-critical encryption trigger\nfor 3 tables and warrants its own `/security-review`.",
  "new_string": "## Resolved latent debt \u2014 idempotent encryption (closed 2026-06-02)\n\n**Was:** the encryption triggers (`trg_encrypt_user_api_keys` + its `meta_config`/`social_accounts`\nsiblings) called `vault.create_secret(value, '<deterministic-name>')` **unconditionally** on a secret\nchange. `vault.create_secret` does a plain INSERT with **no ON CONFLICT** and `vault.secrets.name` is\nUNIQUE (`secrets_name_idx`) \u2192 **rotating a credential in place (new value, same name) threw\n`unique_violation` (23505)**. User-facing: WordPress \"Editar \u2192 save a new password without\ndisconnecting first\". (connect \u2192 disconnect \u2192 reconnect always worked because `disconnect_wordpress()`\ndeletes the secret first; only the rotate-in-place path was broken.)\n\n**Fix:** migration `20260602140000_vault_upsert_secret_idempotent_encrypt.sql` introduces\n`public.vault_upsert_secret(value, name, desc)` \u2014 SECURITY DEFINER, `search_path=''`, EXECUTE revoked\nfrom PUBLIC/anon/authenticated (internal primitive, never a PostgREST RPC) \u2014 which resolves an\nexisting secret by name and rotates it in place via `vault.update_secret` (COALESCE-keeps\nname+description, re-encrypts only the value), else creates it; a `unique_violation` handler absorbs\nthe create race. All three encryption triggers now call this helper instead of `vault.create_secret`\nand were pinned to `search_path=''`. The stored column keeps the SAME Vault UUID across rotations, so\n`decrypted_*` views reflect the new value and no orphan secrets accumulate.\n\n**Material proof (2026-06-02, Management API, every test rolled back \u2014 no production mutation):**\n- BEFORE: `user_api_keys` double-save of `wp_app_password` \u2192 `ERROR 23505 ... secrets_name_idx ...\n  Key (name)=(user_api_keys_wp_app_password_<uid>) already exists` raised inside\n  `trg_encrypt_user_api_keys`.\n- AFTER (`user_api_keys`): same double-save \u2192 `{decrypted_wp:\"wp-pass-BRAVO\", secret_count:1,\n  col_is_uuid_ref:true, sibling_groq_intact:true}`, no error.\n- AFTER (`social_accounts`, real row `39ce0ebb-3579-481a-93ce-8a20759cd22e`): double-rotation of\n  `access_token` \u2192 `{decrypted_access:\"sa-BRAVO\", secret_count:1}`, no error.\n- (`meta_config` has 0 rows to exercise live; covered by the shared helper + source verification \u2014\n  all three triggers verified `calls_helper=true, calls_create_secret=false`.)\n\n**Residual nuance (not a defect):** the helper opens a per-call subtransaction (its `EXCEPTION` block)\nonly to absorb the rare concurrent-create race; the common rotate path takes the no-exception\nSELECT\u2192`update_secret` branch."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/docs/processes/credential-disconnect-clear.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(14:27:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngrep -n \"double-fire fix\" CLAUDE.md",
  "description": "Locate CLAUDE.md anchor line for Key Files insert"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 427:| **user_api_keys INSTEAD OF double-fire fix** | `supabase/migrations/20260602130000_fix_user_api_keys_instead_of_double_fire.sql` (UPDATE-first/INSERT-if-not-found + guard de tenant) |
> ```

## 🤖 Claude *(14:27:53)*


## 🤖 Claude *(14:27:54)*

SOP atualizado. Agora a linha na Key Files Reference do CLAUDE.md (após a âncora na linha 427).

## 🤖 Claude *(14:27:57)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/CLAUDE.md",
  "old_string": "| **user_api_keys INSTEAD OF double-fire fix** | `supabase/migrations/20260602130000_fix_user_api_keys_instead_of_double_fire.sql` (UPDATE-first/INSERT-if-not-found + guard de tenant) |",
  "new_string": "| **user_api_keys INSTEAD OF double-fire fix** | `supabase/migrations/20260602130000_fix_user_api_keys_instead_of_double_fire.sql` (UPDATE-first/INSERT-if-not-found + guard de tenant) |\n| **Vault idempotent encrypt (re-save 23505 fix)** | `supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql` (`vault_upsert_secret()` update-in-place por nome \u00b7 `search_path=''` \u00b7 EXECUTE revogado \u00b7 3 triggers de encripta\u00e7\u00e3o) |"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(14:28:00)*


## 🤖 Claude *(14:28:00)*

Preciso ler o CLAUDE.md antes de editar (o harness exige). Vou ler ao redor da linha 427.

## 🤖 Claude *(14:28:01)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/CLAUDE.md",
  "offset": 424,
  "limit": 8
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 424	| **Affiliate credential resolution SOP** | `docs/processes/affiliate-credential-resolution.md` |
> 425	| **Credential disconnect/clear SOP** | `docs/processes/credential-disconnect-clear.md` (masked-view null NÃO limpa; `.insert` não `.upsert`; INSTEAD OF do user_api_keys NÃO pode usar `INSERT...ON CONFLICT` → double-fire 23505) |
> 426	| **WordPress disconnect RPC** | `supabase/migrations/20260602120000_wordpress_disconnect_rpc.sql` (`disconnect_wordpress()` SECURITY DEFINER · nula 3 cols WP + revoga segredo Vault · auth.uid()-scoped) |
> 427	| **user_api_keys INSTEAD OF double-fire fix** | `supabase/migrations/20260602130000_fix_user_api_keys_instead_of_double_fire.sql` (UPDATE-first/INSERT-if-not-found + guard de tenant) |
> 428	| **Edge JWT identity verification SOP** | `docs/processes/edge-jwt-identity-verification.md` (verify_jwt=false → ES256 JWKS verify; NUNCA atob cego) |
> 429	| **ES256 JWT verification test** | `scripts/qa/test-es256-jwt-verification.ts` (Deno; G1/G2 gates do SOP acima) |
> 430	| **Meta credential resolution SOP** | `docs/processes/meta-credential-resolution.md` (per-user `meta_config`, fail-closed, OTD-META-ENCRYPT) |
> 431	| **Meta publisher function** | `supabase/functions/publish-meta/index.ts` (IG container + FB feed · reauth gate · mesh observation) |
> ```

## 🤖 Claude *(14:28:04)*


## 🤖 Claude *(14:28:08)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/CLAUDE.md",
  "old_string": "| **user_api_keys INSTEAD OF double-fire fix** | `supabase/migrations/20260602130000_fix_user_api_keys_instead_of_double_fire.sql` (UPDATE-first/INSERT-if-not-found + guard de tenant) |\n| **Edge JWT identity verification SOP** |",
  "new_string": "| **user_api_keys INSTEAD OF double-fire fix** | `supabase/migrations/20260602130000_fix_user_api_keys_instead_of_double_fire.sql` (UPDATE-first/INSERT-if-not-found + guard de tenant) |\n| **Vault idempotent encrypt (re-save 23505 fix)** | `supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql` (`vault_upsert_secret()` update-in-place por nome \u00b7 `search_path=''` \u00b7 EXECUTE revogado \u00b7 3 triggers de encripta\u00e7\u00e3o) |\n| **Edge JWT identity verification SOP** |"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/CLAUDE.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(14:28:16)*


## 🤖 Claude *(14:28:17)*

Docs atualizados (SOP "Resolved latent debt" + linha na Key Files Reference). Agora o **`/security-review` obrigatório**. Vou preparar (stage) as mudanças para que o review veja o diff completo — a migration é arquivo novo/untracked.

## 🤖 Claude *(14:28:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql docs/processes/credential-disconnect-clear.md CLAUDE.md\ngit status --short\necho \"--- staged files diffstat ---\"\ngit diff --cached --stat",
  "description": "Stage migration and doc changes for security review"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> M  CLAUDE.md
> M  docs/processes/credential-disconnect-clear.md
> A  supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql
> --- staged files diffstat ---
>  CLAUDE.md                                          |   1 +
>  docs/processes/credential-disconnect-clear.md      |  44 ++-
>  ...0000_vault_upsert_secret_idempotent_encrypt.sql | 311 +++++++++++++++++++++
>  3 files changed, 345 insertions(+), 11 deletions(-)
> ```

## 🤖 Claude *(14:28:20)*


## 🤖 Claude *(14:28:21)*

Mudanças staged. Agora executo o gate obrigatório `/security-review` sobre as mudanças pendentes.

## 🤖 Claude *(14:28:21)*


🛠️ **Tool Call**: `Skill`
```json
{
  "skill": "security-review"
}
```

> **Tool Result (Skill)** - ✅ Success
>
> ```
> Launching skill: security-review
> ```

## 👤 User *(14:28:21)*

You are a senior security engineer conducting a focused security review of the changes on this branch.

GIT STATUS:

```
On branch main
Your branch is up to date with 'origin/main'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   CLAUDE.md
	modified:   docs/processes/credential-disconnect-clear.md
	new file:   supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql
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

## 🤖 Claude *(14:28:40)*


## 🤖 Claude *(14:28:41)*

I'll run the security review per the skill's methodology: an identification sub-task, then parallel false-positive filters, then compile findings at confidence ≥ 8. First, let me capture the exact diff to hand to the analysis sub-agent.

## 🤖 Claude *(14:28:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit diff --cached -- supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql | head -360",
  "description": "Capture staged migration diff for review sub-agent"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> diff --git a/supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql b/supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql
> new file mode 100644
> index 0000000..9a720c0
> --- /dev/null
> +++ b/supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql
> @@ -0,0 +1,311 @@
> +-- Migration: idempotent credential encryption — vault_upsert_secret() eliminates the
> +--            re-save unique_violation (23505) across all three Vault-backed credential tables.
> +-- ─────────────────────────────────────────────────────────────────────────────
> +-- Bug (latent debt flagged 2026-06-02 in docs/processes/credential-disconnect-clear.md, and
> +-- reproduced materially the same day): the BEFORE INSERT/UPDATE encryption triggers
> +-- (trg_encrypt_user_api_keys, trg_encrypt_meta_config, trg_encrypt_social_accounts) call
> +-- vault.create_secret(value, '<deterministic-name>') UNCONDITIONALLY whenever a secret column
> +-- changes value. vault.create_secret does a plain `INSERT INTO vault.secrets` with NO ON CONFLICT,
> +-- and vault.secrets.name carries a UNIQUE index (secrets_name_idx). So rotating a stored secret to
> +-- a NEW value while the same-named secret still exists throws:
> +--     ERROR 23505 duplicate key value violates unique constraint "secrets_name_idx"
> +-- User-facing manifestation: WordPress "Editar → save a new app-password WITHOUT disconnecting
> +-- first" (src/pages/SocialAccountsPage.tsx). Sibling tables share the shape (names keyed by row id),
> +-- so re-saving a Meta long-lived token / pages list, or a social access/refresh token, on an
> +-- existing row collides identically.
> +--
> +-- Already fixed separately (NOT this migration): the INSTEAD OF double-fire of the encrypt trigger
> +-- (20260602130000_fix_user_api_keys_instead_of_double_fire.sql, UPDATE-first). connect → disconnect
> +-- → reconnect already works because disconnect_wordpress() deletes the secret first. The case left
> +-- open was strictly "rotate the value in place without deleting first".
> +--
> +-- Fix: a single idempotent helper public.vault_upsert_secret(value, name, desc) that resolves an
> +-- existing secret BY NAME (vault.secrets.name is unique) and rotates it in place via
> +-- vault.update_secret (which COALESCE-keeps name + description, re-encrypting only the value), else
> +-- creates it. The vault.create_secret call-sites in each of the three encryption triggers are
> +-- swapped for this helper, preserving the existing "already a UUID reference → keep" guard and the
> +-- "only when the value actually changed" (IS DISTINCT FROM) guard. The stored column keeps pointing
> +-- at the SAME Vault UUID across rotations (update-in-place), so decrypted_* views transparently
> +-- reflect the new value and no orphan secrets accumulate.
> +--
> +-- Security posture (this migration HARDENS; per CLAUDE.md every migration passes /security-review):
> +--   * vault_upsert_secret is SECURITY DEFINER with `SET search_path = ''` and every object schema-
> +--     qualified — closing the search_path-injection vector a definer function otherwise carries.
> +--   * EXECUTE on the helper is REVOKED from PUBLIC/anon/authenticated. It is an internal primitive
> +--     called only by the (already definer, owner=postgres) encryption triggers; it must NOT be a
> +--     PostgREST-reachable RPC, since by-name access would otherwise let a caller overwrite ANY
> +--     tenant's secret. The triggers run as postgres (their definer) and retain EXECUTE as owner.
> +--   * The three encryption trigger functions are ALSO pinned to `SET search_path = ''` (they had no
> +--     pin before — proconfig was null), matching the precedent set by 20260602130000. postgres keeps
> +--     the SELECT it already holds on vault.secrets; the privileged Vault writes stay inside the
> +--     SECURITY DEFINER vault.create_secret/update_secret primitives (postgres has EXECUTE, not direct
> +--     INSERT/UPDATE on vault.secrets — verified materially 2026-06-02).
> +--
> +-- Scope: all three credential tables (user_api_keys, meta_config, social_accounts). Triggers keep
> +-- their bindings (CREATE OR REPLACE FUNCTION preserves the function oid) — no trigger re-create.
> +
> +-- ─────────────────────────────────────────────────────────────────────────────
> +-- 1. IDEMPOTENT VAULT HELPER
> +-- ─────────────────────────────────────────────────────────────────────────────
> +CREATE OR REPLACE FUNCTION public.vault_upsert_secret(
> +  p_value text,
> +  p_name  text,
> +  p_desc  text DEFAULT ''
> +)
> +RETURNS uuid
> +LANGUAGE plpgsql
> +SECURITY DEFINER
> +SET search_path = ''
> +AS $$
> +DECLARE
> +  v_id uuid;
> +BEGIN
> +  -- vault.secrets.name is UNIQUE (secrets_name_idx). Resolve an existing secret by its
> +  -- deterministic name and rotate the value in place — this is what makes re-saving a credential
> +  -- idempotent instead of throwing unique_violation (23505). vault.update_secret COALESCE-keeps the
> +  -- name + description and re-encrypts only the value, so the stored UUID reference never changes.
> +  SELECT id INTO v_id FROM vault.secrets WHERE name = p_name;
> +
> +  IF v_id IS NOT NULL THEN
> +    PERFORM vault.update_secret(v_id, p_value);
> +    RETURN v_id;
> +  END IF;
> +
> +  RETURN vault.create_secret(p_value, p_name, p_desc);
> +
> +EXCEPTION
> +  -- Concurrency guard: a parallel writer created the same name between our SELECT and
> +  -- create_secret. Re-resolve and update in place rather than surfacing 23505 to the caller.
> +  WHEN unique_violation THEN
> +    SELECT id INTO v_id FROM vault.secrets WHERE name = p_name;
> +    IF v_id IS NOT NULL THEN
> +      PERFORM vault.update_secret(v_id, p_value);
> +      RETURN v_id;
> +    END IF;
> +    RAISE;
> +END;
> +$$;
> +
> +COMMENT ON FUNCTION public.vault_upsert_secret(text, text, text) IS
> +  'Internal: idempotent Vault secret write keyed by deterministic name (update-in-place when the '
> +  'name exists, else create). Called ONLY by the credential encryption triggers — EXECUTE is revoked '
> +  'from clients. Eliminates the secrets_name_idx 23505 on credential re-save.';
> +
> +-- Internal primitive only — never a client-reachable RPC (would allow by-name cross-tenant overwrite).
> +REVOKE ALL ON FUNCTION public.vault_upsert_secret(text, text, text) FROM PUBLIC;
> +REVOKE ALL ON FUNCTION public.vault_upsert_secret(text, text, text) FROM anon, authenticated;
> +
> +-- ─────────────────────────────────────────────────────────────────────────────
> +-- 2. user_api_keys encryption trigger — swap vault.create_secret → public.vault_upsert_secret
> +--    (latest definition as of 20260601060000, incl. apify_token; + search_path pin)
> +-- ─────────────────────────────────────────────────────────────────────────────
> +CREATE OR REPLACE FUNCTION public.trg_encrypt_user_api_keys()
> +RETURNS TRIGGER
> +LANGUAGE plpgsql
> +SECURITY DEFINER
> +SET search_path = ''
> +AS $$
> +DECLARE
> +  v_id UUID;
> +BEGIN
> +  -- groq_api_key
> +  IF NEW.groq_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.groq_api_key IS DISTINCT FROM OLD.groq_api_key) THEN
> +    IF NEW.groq_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> +      -- keep existing UUID reference
> +    ELSE
> +      v_id := public.vault_upsert_secret(NEW.groq_api_key, 'user_api_keys_groq_api_key_' || NEW.user_id::text, 'Groq API Key');
> +      NEW.groq_api_key = v_id::text;
> +    END IF;
> +  END IF;
> +
> +  -- openrouter_api_key
> +  IF NEW.openrouter_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openrouter_api_key IS DISTINCT FROM OLD.openrouter_api_key) THEN
> +    IF NEW.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> +      -- keep existing UUID reference
> +    ELSE
> +      v_id := public.vault_upsert_secret(NEW.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || NEW.user_id::text, 'OpenRouter API Key');
> +      NEW.openrouter_api_key = v_id::text;
> +    END IF;
> +  END IF;
> +
> +  -- openai_api_key
> +  IF NEW.openai_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openai_api_key IS DISTINCT FROM OLD.openai_api_key) THEN
> +    IF NEW.openai_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> +      -- keep existing UUID reference
> +    ELSE
> +      v_id := public.vault_upsert_secret(NEW.openai_api_key, 'user_api_keys_openai_api_key_' || NEW.user_id::text, 'OpenAI API Key');
> +      NEW.openai_api_key = v_id::text;
> +    END IF;
> +  END IF;
> +
> +  -- elevenlabs_api_key
> +  IF NEW.elevenlabs_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.elevenlabs_api_key IS DISTINCT FROM OLD.elevenlabs_api_key) THEN
> +    IF NEW.elevenlabs_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> +      -- keep existing UUID reference
> +    ELSE
> +      v_id := public.vault_upsert_secret(NEW.elevenlabs_api_key, 'user_api_keys_elevenlabs_api_key_' || NEW.user_id::text, 'ElevenLabs API Key');
> +      NEW.elevenlabs_api_key = v_id::text;
> +    END IF;
> +  END IF;
> +
> +  -- google_api_key
> +  IF NEW.google_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.google_api_key IS DISTINCT FROM OLD.google_api_key) THEN
> +    IF NEW.google_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> +      -- keep existing UUID reference
> +    ELSE
> +      v_id := public.vault_upsert_secret(NEW.google_api_key, 'user_api_keys_google_api_key_' || NEW.user_id::text, 'Google API Key');
> +      NEW.google_api_key = v_id::text;
> +    END IF;
> +  END IF;
> +
> +  -- nanobana_api_key
> +  IF NEW.nanobana_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.nanobana_api_key IS DISTINCT FROM OLD.nanobana_api_key) THEN
> +    IF NEW.nanobana_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> +      -- keep existing UUID reference
> +    ELSE
> +      v_id := public.vault_upsert_secret(NEW.nanobana_api_key, 'user_api_keys_nanobana_api_key_' || NEW.user_id::text, 'Nanobana API Key');
> +      NEW.nanobana_api_key = v_id::text;
> +    END IF;
> +  END IF;
> +
> +  -- seedance_api_key
> +  IF NEW.seedance_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.seedance_api_key IS DISTINCT FROM OLD.seedance_api_key) THEN
> +    IF NEW.seedance_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> +      -- keep existing UUID reference
> +    ELSE
> +      v_id := public.vault_upsert_secret(NEW.seedance_api_key, 'user_api_keys_seedance_api_key_' || NEW.user_id::text, 'Seedance API Key');
> +      NEW.seedance_api_key = v_id::text;
> +    END IF;
> +  END IF;
> +
> +  -- wp_app_password
> +  IF NEW.wp_app_password IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.wp_app_password IS DISTINCT FROM OLD.wp_app_password) THEN
> +    IF NEW.wp_app_password ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> +      -- keep existing UUID reference
> +    ELSE
> +      v_id := public.vault_upsert_secret(NEW.wp_app_password, 'user_api_keys_wp_app_password_' || NEW.user_id::text, 'WordPress App Password');
> +      NEW.wp_app_password = v_id::text;
> +    END IF;
> +  END IF;
> +
> +  -- replicate_api_key
> +  IF NEW.replicate_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.replicate_api_key IS DISTINCT FROM OLD.replicate_api_key) THEN
> +    IF NEW.replicate_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> +      -- keep existing UUID reference
> +    ELSE
> +      v_id := public.vault_upsert_secret(NEW.replicate_api_key, 'user_api_keys_replicate_api_key_' || NEW.user_id::text, 'Replicate API Key');
> +      NEW.replicate_api_key = v_id::text;
> +    END IF;
> +  END IF;
> +
> +  -- higgsfield_api_key
> +  IF NEW.higgsfield_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.higgsfield_api_key IS DISTINCT FROM OLD.higgsfield_api_key) THEN
> +    IF NEW.higgsfield_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> +      -- keep existing UUID reference
> +    ELSE
> +      v_id := public.vault_upsert_secret(NEW.higgsfield_api_key, 'user_api_keys_higgsfield_api_key_' || NEW.user_id::text, 'Higgsfield API Key');
> +      NEW.higgsfield_api_key = v_id::text;
> +    END IF;
> +  END IF;
> +
> +  -- higgsfield_api_key_secret
> +  IF NEW.higgsfield_api_key_secret IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.higgsfield_api_key_secret IS DISTINCT FROM OLD.higgsfield_api_key_secret) THEN
> +    IF NEW.higgsfield_api_key_secret ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> +      -- keep existing UUID reference
> +    ELSE
> +      v_id := public.vault_upsert_secret(NEW.higgsfield_api_key_secret, 'user_api_keys_higgsfield_api_key_secret_' || NEW.user_id::text, 'Higgsfield API Key Secret');
> +      NEW.higgsfield_api_key_secret = v_id::text;
> +    END IF;
> +  END IF;
> +
> +  -- apify_token
> +  IF NEW.apify_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.apify_token IS DISTINCT FROM OLD.apify_token) THEN
> +    IF NEW.apify_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> +      -- keep existing UUID reference
> +    ELSE
> +      v_id := public.vault_upsert_secret(NEW.apify_token, 'user_api_keys_apify_token_' || NEW.user_id::text, 'Apify Token');
> +      NEW.apify_token = v_id::text;
> +    END IF;
> +  END IF;
> +
> +  RETURN NEW;
> +END;
> +$$;
> +
> +-- ─────────────────────────────────────────────────────────────────────────────
> +-- 3. meta_config encryption trigger — swap vault.create_secret → public.vault_upsert_secret
> +-- ─────────────────────────────────────────────────────────────────────────────
> +CREATE OR REPLACE FUNCTION public.trg_encrypt_meta_config()
> +RETURNS TRIGGER
> +LANGUAGE plpgsql
> +SECURITY DEFINER
> +SET search_path = ''
> +AS $$
> +DECLARE
> +  v_token_id UUID;
> +  v_pages_id UUID;
> +BEGIN
> +  IF NEW.id IS NULL THEN
> +    NEW.id := gen_random_uuid();
> +  END IF;
> +
> +  IF NEW.long_lived_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.long_lived_token IS DISTINCT FROM OLD.long_lived_token) THEN
> +    IF NEW.long_lived_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> +      -- keep existing UUID reference
> +    ELSE
> +      v_token_id := public.vault_upsert_secret(NEW.long_lived_token, 'meta_config_long_lived_token_' || NEW.id::text, 'Meta config long-lived token');
> +      NEW.long_lived_token = v_token_id::text;
> +    END IF;
> +  END IF;
> +
> +  IF NEW.pages IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.pages IS DISTINCT FROM OLD.pages) THEN
> +    IF NEW.pages::text ~ '^"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"$' THEN
> +      -- keep existing UUID JSON reference
> +    ELSE
> +      v_pages_id := public.vault_upsert_secret(NEW.pages::text, 'meta_config_pages_' || NEW.id::text, 'Meta config pages list');
> +      NEW.pages = to_jsonb(v_pages_id::text);
> +    END IF;
> +  END IF;
> +
> +  RETURN NEW;
> +END;
> +$$;
> +
> +-- ─────────────────────────────────────────────────────────────────────────────
> +-- 4. social_accounts encryption trigger — swap vault.create_secret → public.vault_upsert_secret
> +-- ─────────────────────────────────────────────────────────────────────────────
> +CREATE OR REPLACE FUNCTION public.trg_encrypt_social_accounts()
> +RETURNS TRIGGER
> +LANGUAGE plpgsql
> +SECURITY DEFINER
> +SET search_path = ''
> +AS $$
> +DECLARE
> +  v_access_token_id UUID;
> +  v_refresh_token_id UUID;
> +BEGIN
> +  IF NEW.id IS NULL THEN
> +    NEW.id := gen_random_uuid();
> +  END IF;
> +
> +  IF NEW.access_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.access_token IS DISTINCT FROM OLD.access_token) THEN
> +    IF NEW.access_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> +      -- keep existing UUID reference
> +    ELSE
> +      v_access_token_id := public.vault_upsert_secret(NEW.access_token, 'social_accounts_access_token_' || NEW.id::text, 'Social account access token');
> +      NEW.access_token = v_access_token_id::text;
> +    END IF;
> +  END IF;
> +
> +  IF NEW.refresh_token IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.refresh_token IS DISTINCT FROM OLD.refresh_token) THEN
> +    IF NEW.refresh_token ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> +      -- keep existing UUID reference
> +    ELSE
> +      v_refresh_token_id := public.vault_upsert_secret(NEW.refresh_token, 'social_accounts_refresh_token_' || NEW.id::text, 'Social account refresh token');
> +      NEW.refresh_token = v_refresh_token_id::text;
> +    END IF;
> +  END IF;
> +
> +  RETURN NEW;
> +END;
> +$$;
> ```

## 🤖 Claude *(14:28:48)*


## 🤖 Claude *(14:28:48)*

Full diff captured. Now I'll launch the identification sub-task with repo context, per the skill's methodology.

## 🤖 Claude *(14:29:19)*


🛠️ **Tool Call**: `Agent`
```json
{
  "description": "Identify security vulns in migration",
  "subagent_type": "general-purpose",
  "prompt": "You are a senior security engineer performing a focused security review of ONE staged change in a Supabase/Postgres project: a new SQL migration that modifies the credential-encryption layer. Identify ONLY high-confidence, newly-introduced security vulnerabilities with real exploitation potential. This is not a general code review.\n\n## The change under review (staged diff)\n\nFile: `supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql`\n\nIt does three things:\n1. Creates `public.vault_upsert_secret(p_value text, p_name text, p_desc text DEFAULT '')` \u2014 `SECURITY DEFINER`, `SET search_path = ''`, owned by `postgres`. Body: `SELECT id INTO v_id FROM vault.secrets WHERE name = p_name;` then if found `PERFORM vault.update_secret(v_id, p_value)` else `RETURN vault.create_secret(p_value, p_name, p_desc)`. Has an `EXCEPTION WHEN unique_violation` handler that re-selects by name and updates. Then: `REVOKE ALL ON FUNCTION public.vault_upsert_secret(text,text,text) FROM PUBLIC;` and `REVOKE ALL ... FROM anon, authenticated;`\n2. Recreates the three BEFORE INSERT/UPDATE encryption triggers (`trg_encrypt_user_api_keys`, `trg_encrypt_meta_config`, `trg_encrypt_social_accounts`) \u2014 all `SECURITY DEFINER`, now `SET search_path = ''`, swapping every `vault.create_secret(...)` call for `public.vault_upsert_secret(...)`. They preserve the existing \"value already matches a UUID regex \u2192 keep\" guard and the `IS DISTINCT FROM` change-guard. Secret names are deterministic: `user_api_keys_<col>_<user_id>`, `meta_config_<...>_<id>`, `social_accounts_<...>_<id>`.\n\nFull diff content:\n\n```sql\nCREATE OR REPLACE FUNCTION public.vault_upsert_secret(\n  p_value text, p_name text, p_desc text DEFAULT ''\n) RETURNS uuid LANGUAGE plpgsql SECURITY DEFINER SET search_path = ''\nAS $$\nDECLARE v_id uuid;\nBEGIN\n  SELECT id INTO v_id FROM vault.secrets WHERE name = p_name;\n  IF v_id IS NOT NULL THEN\n    PERFORM vault.update_secret(v_id, p_value);\n    RETURN v_id;\n  END IF;\n  RETURN vault.create_secret(p_value, p_name, p_desc);\nEXCEPTION\n  WHEN unique_violation THEN\n    SELECT id INTO v_id FROM vault.secrets WHERE name = p_name;\n    IF v_id IS NOT NULL THEN\n      PERFORM vault.update_secret(v_id, p_value);\n      RETURN v_id;\n    END IF;\n    RAISE;\nEND;\n$$;\nREVOKE ALL ON FUNCTION public.vault_upsert_secret(text, text, text) FROM PUBLIC;\nREVOKE ALL ON FUNCTION public.vault_upsert_secret(text, text, text) FROM anon, authenticated;\n-- then the 3 encrypt triggers, each block of the form:\n--   IF NEW.x IS NOT NULL AND (TG_OP='INSERT' OR NEW.x IS DISTINCT FROM OLD.x) THEN\n--     IF NEW.x ~ '^[0-9a-f]{8}-...uuid...$' THEN  -- keep\n--     ELSE v_id := public.vault_upsert_secret(NEW.x, '<table>_<col>_'||NEW.user_id::text, 'desc'); NEW.x = v_id::text;\n--     END IF;\n--   END IF;\n```\n\n## Context to research in the repo (read these to ground your analysis)\n- `supabase/migrations/20260601000000_credential_encryption.sql` \u2014 original encrypt triggers + masked views + INSTEAD OF triggers + decrypted_* views (the pattern being modified).\n- `supabase/migrations/20260601060000_user_api_keys_apify_token.sql` \u2014 latest user_api_keys trigger/view definition.\n- `supabase/migrations/20260602130000_fix_user_api_keys_instead_of_double_fire.sql` \u2014 the INSTEAD OF tenant guard + UPDATE-first (precedent for `SET search_path=''`).\n- `supabase/migrations/20260602120000_wordpress_disconnect_rpc.sql` \u2014 disconnect_wordpress() SECURITY DEFINER pattern.\n- `docs/processes/credential-disconnect-clear.md` \u2014 the SOP describing the masked-view + Vault model.\n\n## Materially verified facts (already confirmed against the live DB \u2014 treat as ground truth)\n- `vault.secrets.name` has a UNIQUE index `secrets_name_idx`.\n- `vault.update_secret(secret_id, new_secret, new_name DEFAULT NULL, ...)` does `name = coalesce(new_name, s.name)` \u2192 calling with only `(v_id, p_value)` keeps name+description, rotates only the value.\n- After apply: `has_function_privilege('anon'|'authenticated', 'public.vault_upsert_secret(text,text,text)', 'EXECUTE')` = FALSE; `postgres` = TRUE. The 3 triggers now have `proconfig = {search_path=\"\"}` and their source calls `vault_upsert_secret`, not `vault.create_secret`.\n- `postgres` has SELECT on `vault.secrets` but NOT direct INSERT/UPDATE (those happen inside the SECURITY DEFINER vault.* primitives).\n\n## Your job\nExamine for NEWLY-INTRODUCED, high-confidence security vulnerabilities (>80% confident of real exploitability) in these categories: SQL injection, privilege escalation, authorization bypass, cross-tenant secret access, SECURITY DEFINER / search_path abuse, secret exposure. Specifically reason about:\n- Can any untrusted (anon/authenticated) caller reach `vault_upsert_secret` directly (PostgREST RPC) or indirectly to overwrite/read ANOTHER tenant's Vault secret by controlling `p_name`?\n- Does the secret-name construction (`'<table>_<col>_' || NEW.user_id::text`) let one tenant collide with / hijack another tenant's secret name? Consider whether a caller controls `NEW.user_id` and whether the INSTEAD OF tenant guard (in 20260602130000 for user_api_keys; check meta_config/social_accounts INSTEAD OF triggers too) constrains it.\n- Is the `SET search_path = ''` correct and complete (every referenced object schema-qualified, including `gen_random_uuid()`, `to_jsonb()`)? Could an unqualified reference resolve to an attacker-controlled object?\n- Any way the EXCEPTION handler or update-in-place introduces a confused-deputy or data-exposure path?\n\nDo NOT report: DoS/resource exhaustion, \"secrets stored on disk\", rate limiting, lack-of-hardening that isn't a concrete exploit, theoretical races, documentation issues, or pre-existing issues not introduced by this diff.\n\nFor EACH candidate finding output: a title, file:line, severity (HIGH/MEDIUM/LOW), category, description, concrete exploit scenario (who the attacker is, what they control, the exact steps), and a fix recommendation. If you find NO high-confidence vulnerabilities, say so explicitly and explain why the change is secure (this is an acceptable and expected outcome). Return your findings as a structured list."
}
```

---

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-02 - Fix WordPress credentials save and disconnect in SocialAccountsPage]]
> * **Próxima Sessão**: [[2026-06-02 - agent-a5d10b1c82e30c144]]
%% --- TIMELINE END --- %%

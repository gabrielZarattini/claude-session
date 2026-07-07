# SOP: Avatar Voice Credential Resolution (Per-User · ElevenLabs/Cartesia)

**Status:** ACTIVE · v0.1 · 2026-06-30
**Owner:** Sovereign (Gabriel Zarattini)
**Survival Law 2 compliance:** Escrita **ANTES** de qualquer código da Fatia 2 (voice clone) do módulo `avatar-clone-ai`. Fecha o gate **OTD-AC-VOICE** (`docs/bok/avatar-clone-ai/05-sdd.md §9` — *"SOP `avatar-byok-credential-resolution.md` antes de codar"*, instanciado aqui para a fatia de voz) e cobre FR-AC-009 (edge fn `generate-voice`) + FR-AC-010 (code-switching guard) + FR-AC-011 (`voice_profiles`).
**Canonical directive:** `CLAUDE.md > Architecture > "API Tenancy Model — Per-User Credentials"` · `.claude/rules/survival.md > Law 1 (Materiality) / Law 2 (Anticipated Process)`
**BoK SSOT:** `docs/bok/avatar-clone-ai/{04-frd.md,05-sdd.md,06-data-model.md}` (FR-AC-008/009/010/011 · NFR-AC-002/017/019/020)
**Sibling SOPs:** `trends-credential-resolution.md` (Apify/RapidAPI per-user blueprint) · `affiliate-credential-resolution.md` (mercadolivre per-user) · `meta-credential-resolution.md` (OAuth per-user base pattern)

---

## Context

A síntese e a clonagem de voz para os avatares talking-head (programa "Gabriel AI") exigem credenciais de provider escopadas por tenant. A Fatia 2 integra voz via **ElevenLabs** (TTS Multilingual v2 + Instant Voice Cloning) e **Cartesia** (Sonic — TTS em tempo real, pt-BR nativo). Ambas as credenciais são **per-user (BYOK Modelo A puro)**: cada criador conecta a própria conta; cada tenant isolado; **nunca conta-mestra multiplexada** (service bureau proibido — invariante OTD-AC-011).

`supabase/functions/generate-voice/index.ts` (net-new, paralelo a `generate-image`) DEVE resolver `elevenlabs_api_key` e `cartesia_api_key` filtrando por `user_id` do **dono do avatar**, lendo de `decrypted_user_api_keys` (service-role), **nunca** de um env global. As colunas já existem cifradas no Vault: `elevenlabs_api_key` (pré-existente) e `cartesia_api_key` (migração `20260630000000_user_api_keys_avatar_byok.sql`) — encrypt trigger idempotente, masked view (`••••`), decrypted view service-role-only, INSTEAD OF com guard de tenant.

**Por que importa (multi-tenant readiness):** quota de síntese isolada por tenant · sem vazamento de quota cross-tenant · LGPD (cada user controla/revoga a própria credencial de voz — voiceprint é dado biométrico, Art. 11) · anti-fraude (um user não sintetiza/cobra pela conta de outro).

> **Escopo da Fatia 2 (BoK SSOT):** o **consent gate** (`avatar_consents` + wizard) é **diferido para a Fatia 3/6** (FR-AC-030/031). FR-AC-009/010 **não** referenciam `avatar_consents`. A Fatia 2 assume consentimento válido e foca em síntese + persistência. `voice_profiles.status` (`active`/`revoked`) já deixa a revogação representável; o erase RPC chega na fatia de erasure. **Deferral declarado, não silencioso.**

---

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (edge fn `generate-voice`) + Tenant (configura as próprias chaves ElevenLabs/Cartesia em `/dashboard/settings`).
- **Reviewer:** Sovereign (Gabriel) — aprova a edge fn + valida o smoke zero-cost + `/security-review` da migration.
- **Owner:** Sovereign — blast radius = quota de síntese de voz per-tenant + voiceprint biométrico per-tenant (PII).

---

## Operator (quem executa manualmente hoje)

- **Usuário Zero / cliente:** configura `elevenlabs_api_key` e/ou `cartesia_api_key` em `/dashboard/settings` (seção Avatar BYOK — hook `useUserApiKeys` → `.insert()` na view `user_api_keys` → INSTEAD OF → Vault).
- **Edge fn `generate-voice`:** resolve a credencial por request e clona/sintetiza a voz do tenant.

---

## Resolution order (canonical — espelha o API Tenancy Model)

| # | Camada | Fonte | Permitido em |
|---|--------|-------|--------------|
| 1 | **Per-user** | `decrypted_user_api_keys` WHERE `user_id = <owner>` → `elevenlabs_api_key` / `cartesia_api_key` (read service-role) | SEMPRE (caminho primário) |
| 2 | **Global vault fallback** | `Deno.env.get('ELEVENLABS_API_KEY' / 'CARTESIA_API_KEY')` | **PROIBIDO** em síntese user-facing. Não há fallback global nesta fatia. |
| 3 | **Hard failure** | — | HTTP 402 `{ error: "<provider>_not_configured", action: "Configure suas credenciais de voz em /dashboard/settings" }` + pulse `infra_health_logs status=degraded` |

**Owner resolution:** o request traz `user_id` via JWT do dono (caminho user) OU `body.user_id` numa chamada service-role do pipeline (caminho dual-path, molde `generate-image`). A voz pertence ao **dono do avatar**, nunca ao chamador.

---

## Sequence

### `generate-voice` — `action: 'clone'` (Instant Voice Cloning · sem cobrança mco)

1. **Auth:** validar `Authorization: Bearer`. Resolver `userId` via `auth.getUser()` (JWT) OU `body.user_id` (bearer == `SB_SECRET_KEY`, dual-path).
2. **Resolve config (camada 1):** SELECT da `decrypted_user_api_keys` por `userId`. Provider-gate: `provider='elevenlabs'`→`elevenlabs_api_key`; `provider='cartesia'`→`cartesia_api_key`. Ausente → 402 `<provider>_not_configured` (camada 3) + pulse degraded.
3. **Upload de amostras:** POST das amostras de referência ao provider IVC (`POST https://api.elevenlabs.io/v1/voices/add` multipart `{name, files[]}` → `{voice_id}`; ou `POST https://api.cartesia.ai/voices/clone`). BYOK = conta do próprio user.
4. **Persistir:** guardar o `voice_id` cifrado no Vault (`vault_upsert_secret` → `voiceprint_vault_ref`) + INSERT `voice_profiles` (`user_id`, `provider`, `clone_method`, `voiceprint_vault_ref`, `language`, `status='active'`). RLS own.
5. **Mesh + telemetry:** observation node na mesh (1º clone bem-sucedido) + pulse `infra_health_logs.service='avatar-clone-ai' event='avatar_voice_clone'`.
6. **Return:** `{ voice_profile_id, provider, language }`. **Zero mco** (clone é config; o render/synthesize subsequente cobra).

### `generate-voice` — `action: 'synthesize'` (TTS · cobra `VOICE_COST` = 36 mco)

1. **Auth** (idem).
2. **Resolve config (camada 1)** (idem) → 402 fail-closed se ausente.
3. **Resolve voice profile:** SELECT `voice_profiles` por `id` + `user_id` (owner-scoped). Ausente → 404.
4. **Code-switching guard (FR-AC-010 / FM-AC-013) — ANTES do débito:**
   - **Hard gate (determinístico):** `voice_profile.language` ≠ `request.language` → 422 `language_mismatch` (accent-bleed: voz não clonada no idioma-alvo).
   - **Soft gate (heurístico):** `detectCodeSwitch(script, language)` detecta mistura intra-frase clara (diacríticos pt em script `en`, ou função-words EN densas em script `pt-BR`) → 422 `code_switch_detected`. Conservador (evitar falso-positivo num caminho pago).
5. **Sentinel:** `inspectPrompt(script)` (pt-BR + EN) — bloqueio de injection no roteiro de fonte não-confiável.
6. **Débito atômico:** `deduct_mco_coins(p_user_id, p_amount=36)` **DEPOIS** dos gates fail-closed. Saldo insuficiente → 402 SEM gerar áudio.
7. **Síntese:** POST TTS ao provider (`POST https://api.elevenlabs.io/v1/text-to-speech/{voice_id}` header `xi-api-key`, body `{text, model_id:'eleven_multilingual_v2', language_code, voice_settings}`; ou `POST https://api.cartesia.ai/tts/bytes` headers `X-Api-Key`+`Cartesia-Version`, body `{model_id:'sonic-3.5', transcript, voice:{mode:'id',id}, output_format, language}`). Falha → **refund** `add_mco_coins` + 502.
8. **Persistir asset:** upload do áudio em `video-studio-assets` prefixo `user_id/voice/` (privado) → `register_creative_asset(p_kind='audio', p_source_module='avatar-studio', p_mime_type, p_duration_seconds, p_file_size_bytes)` (fail-soft).
9. **Telemetry:** pulse `infra_health_logs.service='avatar-clone-ai' event='avatar_voice'` (healthy/degraded/unhealthy).
10. **Return:** `{ audio_url (signed, TTL curto), creative_asset_id, mco_charged: 36 }`.

---

## Verification gates

| Gate | Check | Pass criterion |
|------|-------|----------------|
| G1 | User COM config + voice_profile → synthesize | HTTP 200 · `audio_url` assinada válida · row `creative_assets` (kind=audio, source_module=avatar-studio) · `mco_charged=36` · saldo −36 *(GATED — gasto real, ação Sovereign)* |
| G2 | User SEM config → synthesize/clone | HTTP 402 · `<provider>_not_configured` · **ZERO** débito · pulse degraded *(zero-cost)* |
| G3 | `language` ≠ `voice_profile.language` | HTTP 422 `language_mismatch` · ZERO débito *(zero-cost)* |
| G4 | Script com code-switch intra-frase claro | HTTP 422 `code_switch_detected` · ZERO débito *(zero-cost)* |
| G5 | Tenant guard | User A não lê voice_profile/credential de User B (REST com JWT de A → 0 rows de B) *(zero-cost)* |
| G6 | Column-grant | SELECT `elevenlabs_api_key`/`cartesia_api_key` via JWT authenticated → mask `••••` (nunca plaintext ao client) *(zero-cost)* |
| G7 | Saldo insuficiente | synthesize com saldo < 36 → HTTP 402 · ZERO áudio gerado *(zero-cost)* |
| G8 | Telemetria | `infra_health_logs.service='avatar-clone-ai'` recebe pulse em cada path (success/degraded/error) |
| G9 | Zero global em path user-facing | `grep -i "ELEVENLABS_API_KEY\|CARTESIA_API_KEY" generate-voice/index.ts` → 0 refs de `Deno.env` como fonte primária |
| G10 | No-auth | request sem `Authorization` → HTTP 401 *(zero-cost)* |

---

## Recovery path

| Cenário | Detecção | Recovery |
|---------|----------|----------|
| Provider TTS falha após débito | resposta non-2xx do provider | `add_mco_coins` (refund 36) + retornar 502; nunca charge-without-value (FM-AC-005) |
| `decrypted_user_api_keys` lookup erro DB | `console.error` no edge log + pulse degraded | Fail-closed (camada 3); nunca sintetizar sem credencial resolvida |
| Regressão (env global reintroduzido) | G9 falha em grep/CI | Reverter; voz nunca usa env global em path user-facing |
| Clone de amostras falha no provider (400/429) | non-2xx do IVC | Logar; retornar 402/502 ao client; orientar retry / upgrade de plano BYOK; NÃO inserir `voice_profiles` |
| Áudio sintetizado mas upload/asset falha | upload error / register erro | asset register é fail-soft (não quebra a resposta); áudio retornado mesmo sem row em creative_assets; logar |

---

## Success signal (whole protocol)

- G2–G10 verdes no smoke zero-cost (`scripts/qa/smoke-generate-voice.ts`).
- `generate-voice` deployada (script size + ACTIVE em `supabase functions list`).
- `infra_health_logs.service='avatar-clone-ai'` com pulses recentes pós-smoke.
- G1 (synthesize pago real) provado quando o Sovereign autorizar o gasto (BYOK + 36 mco) — voz sintetizada com a **chave do próprio user**, não env global.

---

## Anti-patterns prohibited

- ❌ `Deno.env.get('ELEVENLABS_API_KEY' / 'CARTESIA_API_KEY')` como fonte primária de síntese user-facing.
- ❌ Sintetizar/clonar com chave NULL silenciosamente (perda sem erro).
- ❌ Retornar `elevenlabs_api_key`/`cartesia_api_key` ao client (column-grant via masked view obrigatório).
- ❌ Resolver `user_api_keys` sem filtrar `user_id` do dono (vazamento cross-tenant).
- ❌ Debitar 36 mco ANTES dos gates fail-closed (402/422) — débito só após todos os gates.
- ❌ Compartilhar quota/voiceprint de um user com outro via credencial global (fraude por design).
- ❌ Persistir `voice_profiles` com `clone_method` fora de `{pvc,ivc,voice_design}` ou `language` fora de `{en,pt-BR}` (code-switch por construção).

---

## Connection to Survival Laws

- **Lei 1 (Materialidade):** cada gate produz prova material (HTTP status + body + row `voice_profiles`/`creative_assets` + pulse).
- **Lei 2 (Anticipated Process):** este SOP escrito ANTES do código da edge fn (requisito API Tenancy item 5).
- **Lei 3 (Pruning):** resolução stateless por request; nada acumulado.
- **Lei 4 (ORO):** triplet declarado; Reviewer = Sovereign aprova edge fn + migration antes do deploy.

---

## Sibling reference

- **Blueprint per-user base:** `docs/processes/trends-credential-resolution.md` (Apify/RapidAPI → per-user + masked view + idempotent encrypt trigger).
- **Affiliate pattern:** `docs/processes/affiliate-credential-resolution.md` (mercadolivre → per-user lookup + fail-closed 402).
- **Meta pattern:** `docs/processes/meta-credential-resolution.md` (OAuth per-user + reauth gate).
- **DB schema:** `supabase/migrations/20260630000000_user_api_keys_avatar_byok.sql` (`elevenlabs_api_key` pré-existente · `cartesia_api_key` nova; ambas cifradas) + `20260630120000_avatar_clone_ai_voice_profiles.sql` (`voice_profiles` + `creative_assets.source_module += 'avatar-studio'`).
- **Sealed contract:** `docs/bok/avatar-clone-ai/{04-frd,05-sdd,06-data-model}.md` (FR-AC-008/009/010/011 · NFR-AC-002/017/019/020).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

# SOP: Avatar Biometric Consent · Retention · Erasure (LGPD Art. 11/18)

**Status:** ACTIVE · v0.1 · 2026-06-30
**Owner:** Sovereign (Gabriel Zarattini)
**Survival Law 2 compliance:** Escrita **ANTES** do código da Fatia 3a (consent + erasure) do módulo `avatar-clone-ai`. Cobre FR-AC-030 (consent wizard 3-checkbox), FR-AC-031 (per-render consent fail-closed), FR-AC-027/028 (erasure + retention). Fecha o **deferral de consent da Fatia 2** (a `generate-voice` passa a exigir consent ativo). Molde: `vision-mcp-pat-and-erasure.md`.
**Canonical directive:** `CLAUDE.md > Security model` + `> API Tenancy Model` · `.claude/rules/survival.md > Law 1 (Materiality) / Law 2 (Anticipated Process)`
**BoK SSOT:** `docs/bok/avatar-clone-ai/{04-frd.md,05-sdd.md,06-data-model.md}` (FR-AC-027/028/030/031 · NFR-AC-013/015/025)
**Sibling SOPs:** `avatar-voice-credential-resolution.md` (Fatia 2 voz) · `vision-mcp-pat-and-erasure.md` (molde erasure) · `avatar-identity-verification-gate.md` (Fatia 3b, futura) · `avatar-disclosure-c2pa-gate.md` (Fatia 6, futura)

---

## Context

Voiceprint (Fatia 2) e, em breve, embedding facial / LoRA (Fatia 3b) são **dados biométricos = dados pessoais sensíveis** (LGPD Art. 5 II + Art. 11). Persistir biometria exige **consentimento específico, destacado e por finalidade** (Art. 11 §1; nunca legítimo interesse/contrato), e o titular tem **direito de revogar + eliminar** (Art. 18). Esta SOP rege o ciclo: **consent grant → per-render fail-closed gate → revoke → erasure cascade (SQL + Storage + Vault + terceiros) → retention sweep**.

Tabelas: `avatar_consents` (imutável, por finalidade `train_lora`/`face_embedding`/`voice_clone`) + `avatar_identities`/`voice_profiles` (artefatos biométricos, RLS own). Erasure via RPC `erase_avatar_artifacts` (SECURITY DEFINER, tenant-guarded) + edge fn `erase-avatar-artifacts` (Storage API + Vault + Art. 18 best-effort). **Por que importa:** compliance LGPD per-tenant; revogação materialmente efetiva (não cosmética); zero resíduo biométrico após erase; isolamento cross-tenant (FM-AC-011).

---

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (edge fn `erase-avatar-artifacts` + gate in `generate-voice`/`avatar-identity-train`) + Tenant (concede/revoga consent na UI).
- **Reviewer:** Sovereign (Gabriel) — aprova migration via `/security-review` + valida smoke de zero-residue.
- **Owner:** Sovereign — blast radius = biometria facial/vocal per-tenant (PII sensível) + obrigação legal de eliminação.

---

## Operator (quem executa manualmente hoje)

- **Titular:** abre o wizard de consentimento (3 checkboxes separados), concede por finalidade; depois pode revogar + pedir eliminação na UI (Settings → Privacidade do Avatar).
- **Edge fns:** `generate-voice`/`avatar-identity-train` checam consent ativo antes de criar/usar biometria; `erase-avatar-artifacts` executa a cascata de eliminação.

---

## Resolution order (consent gate — canonical)

| # | Camada | Fonte | Resultado |
|---|--------|-------|-----------|
| 1 | **Consent ativo por finalidade** | `avatar_consents` WHERE `user_id=<owner>` AND `purpose=<p>` AND `consent_granted=true` AND `revoked_at IS NULL` | prossegue |
| 2 | **Ausente** | sem linha de consent concedido | HTTP 403 `consent_required` + action "Conceda consentimento biométrico em /dashboard/settings" |
| 3 | **Revogado** | `revoked_at IS NOT NULL` | HTTP 403 `consent_revoked` (fail-closed, NÃO gera mídia) |

---

## Sequence

### Consent grant (wizard)
1. Titular marca cada checkbox de finalidade desejada (separados: `train_lora` / `face_embedding` / `voice_clone`) — nunca "aceito tudo".
2. `INSERT avatar_consents` (1 linha por finalidade concedida) com `term_version`, `ip_address`, `consent_granted=true`, `attestation_titular`, `attestation_commercial_tier`. **Imutável** (trigger bloqueia UPDATE de qualquer coluna ≠ `revoked_at`).

### Per-render fail-closed gate (FR-AC-031)
3. `generate-voice` (clone) / `avatar-identity-train`: ANTES de persistir biometria, exigir consent ativo da finalidade (`voice_clone` / `train_lora`+`face_embedding`). Ausente/revogado → 403 (resolution order acima). `generate-voice` (synthesize): consent `voice_clone` não-revogado, senão 403 `consent_revoked`.

### Revoke + erasure (Art. 18)
4. Titular revoga: `UPDATE avatar_consents SET revoked_at=now()` (única coluna mutável).
5. Titular pede eliminação: edge fn `erase-avatar-artifacts` → RPC `erase_avatar_artifacts(p_avatar_identity_id?, p_voice_profile_id?)` (SECURITY DEFINER, tenant-guard `user_id=auth.uid() OR service_role` em CADA delete) → retorna `storage_keys`.
6. Edge fn (service-role): remove objetos de Storage via **Storage API** (não SQL — `storage.objects` é storage-admin, OTD-VM-026) + **revoga segredos Vault** dos voiceprints + dispara delete nas APIs terceiras (Art. 18, best-effort) + **atestado** em `infra_health_logs` (`event='avatar_erase'`).

### Retention sweep (diário)
7. Job `scripts/avatar-retention-sweep.ts` (molde `retention-sweep.ts`): `SELECT avatar_identities/voice_profiles WHERE last_used_at < now() - <retention>` → `erase_avatar_artifacts` por linha (service-role) → Storage API delete. Best-effort, nunca lança; telemetria `avatar_retention_sweep`.

---

## Verification gates

| Gate | Check | Pass criterion |
|------|-------|----------------|
| G1 | Clone/persist SEM consent | 403 `consent_required` · ZERO linha biométrica criada |
| G2 | Clone COM consent `voice_clone` ativo | prossegue ao gate BYOK (não bloqueado por consent) |
| G3 | Synth com consent REVOGADO | 403 `consent_revoked` · ZERO mídia · ZERO débito |
| G4 | `avatar_consents` imutável | UPDATE de coluna ≠ `revoked_at` → `42501` (trigger) |
| G5 | Erase do dono | `{erased:true}` + `SELECT count` identities/voice_profiles/objetos = **0** (zero-residue) |
| G6 | Erase tenant-guard | id de outro tenant → `*_not_found` (não apaga nada alheio) |
| G7 | EXECUTE grant | `erase_avatar_artifacts` revogado de PUBLIC/anon; só authenticated(self)/service_role |
| G8 | Telemetria | `infra_health_logs.service='avatar-clone-ai' event='avatar_erase'` atestado por erase |
| G9 | Storage zero-residue | após erase, `list` do prefixo `user_id/` do artefato = vazio |

---

## Recovery path

| Cenário | Detecção | Recovery |
|---------|----------|----------|
| Erase falha no Storage API (objeto órfão) | edge log + atestado degraded | retry idempotente do prefixo; SQL já apagado, re-remoção é no-op |
| Cópias já transmitidas a providers terceiros | inerente (Hedra/fal.ai/ElevenLabs) | depende do DPA; `provider_copies`/dispatch torna a deleção **solicitável e auditável** (Art. 18 best-effort, reconcile ≤24h) |
| Sweep falha numa linha | telemetria degraded | loga + continua o lote (uma erasure ruim não trava as demais) |
| Consent ausente mas biometria legada existe | gate 403 no próximo uso | titular concede consent OU pede erase; biometria sem consent não é reutilizável |

---

## Success signal (whole protocol)

- G1–G9 verdes no smoke `scripts/qa/smoke-avatar-consent-erase.ts` (zero-cost, sem biometria real).
- `erase-avatar-artifacts` deployada (ACTIVE em `supabase functions list`).
- `generate-voice` redeployada com o consent gate (smoke de voz atualizado verde).
- Migration `/security-review` SAFE; objetos verificados materialmente (HTTP 201 + query).

---

## Anti-patterns prohibited

- ❌ Persistir biometria (voiceprint/face embedding/LoRA) sem consent ativo da finalidade.
- ❌ Consent "aceito tudo" único / legítimo interesse / contrato (LGPD Art. 11 exige específico+destacado).
- ❌ UPDATE de `avatar_consents` em qualquer coluna ≠ `revoked_at` (imutabilidade).
- ❌ Revogação cosmética (marcar revoked sem fail-closed efetivo no próximo render).
- ❌ Apagar `storage.objects` via SQL no RPC (storage-admin → 42501); usar Storage API no caller.
- ❌ Erase sem re-escopar `user_id` em CADA delete (id poisoned vira primitiva cross-tenant — FM-AC-011).
- ❌ EXECUTE de `erase_avatar_artifacts` a anon/PUBLIC.

---

## Connection to Survival Laws

- **Lei 1 (Materialidade):** cada gate = prova material (HTTP status + `count=0` pós-erase + atestado pulse).
- **Lei 2 (Anticipated Process):** esta SOP antes do código (consent + erasure).
- **Lei 3 (Pruning):** erase stateless por request; sweep batched.
- **Lei 4 (ORO):** triplet declarado; Reviewer aprova migration + smoke antes do deploy.

---

## Sibling reference

- **Molde erasure/retention:** `docs/processes/vision-mcp-pat-and-erasure.md` (erase_vision_artifacts + retention-sweep).
- **Fatia 2 voz:** `docs/processes/avatar-voice-credential-resolution.md`.
- **DB:** `supabase/migrations/20260630130000_avatar_clone_ai_identity_consent.sql` (avatar_identities + avatar_consents + erase_avatar_artifacts).
- **Sealed contract:** `docs/bok/avatar-clone-ai/{04-frd,05-sdd,06-data-model}.md` (FR-AC-027/028/030/031).

# SOP — Treino de identidade LoRA grátis (avatar-identity-train, Replicate BYOK)

> **Lei 2 (Processo Antecipado).** BoK SSOT: `docs/bok/avatar-clone-ai/11-amendment-free-lora-training.md` (fecha OTD-AC-017). Fundamentação: workflow `wf_85d1558b-7bf` (30 fontes citadas).
> **API Tenancy Model:** credencial Replicate resolvida per-user (`decrypted_user_api_keys.replicate_api_key`), fail-closed. Env NÃO é fallback (BYOK puro — treino debita na conta do próprio user, USD 0 para o MCORCH).

## Operator (quem executa hoje, manualmente)

O Sovereign, se fosse fazer à mão no dashboard da Replicate: (1) cria um modelo destino vazio; (2) zipa 12-26 retratos; (3) sobe o zip; (4) dispara `POST /trainings` contra `ostris/flux-dev-lora-trainer`; (5) espera ~20-30 min; (6) copia a URL dos pesos. A edge fn `avatar-identity-train` automatiza exatamente isso, escopado por `auth.uid()`.

## Sequence (edge fn — 2 ações, async)

**`action:'start'`** — cada step com critério material:
1. **Auth** — user-JWT válido → `user.id`. Falha → 401.
2. **Consent gate** — `train_lora` + `face_embedding` ativos (não-revogados) em `avatar_consents`. Falha → 403 `consent_required`.
3. **BYOK** — `replicate_api_key` do user. Falha → 402 `replicate_not_configured`.
4. **Dataset** — baixa os retratos de `canvas-assets` (paths do corpo, escopo `${user.id}/`), zipa (jszip), sobe `avatars/train/<identityId>.zip`, assina URL (TTL 24h). Critério: zip > 0 bytes + N ≥ 4 imagens.
5. **Versão viva** — `GET /v1/models/ostris/flux-dev-lora-trainer` → `latest_version.id` (nunca hardcode; OTD-AC-016-VERSION-HASH-ROTATION).
6. **Username** — `GET /v1/account` → `username`.
7. **Destination** — `POST /v1/models {owner:username, name:'flux-<8hex>', visibility:'private', hardware:'gpu-t4'}` (409 → reusa).
8. **Training** — `POST /v1/models/ostris/flux-dev-lora-trainer/versions/<version>/trainings {destination, input:{input_images:<zip url>, trigger_word, steps:1000, lora_rank:16, ...}}`. Critério: HTTP 201 + `id`.
9. **Persistência** — INSERT `avatar_identities` status='training', provider='lora_flux', substrate='flux-dev-lora', `training_ref`=<training id>, `replicate_destination_slug`, `trigger_word`, `commercial_license_ok=true` (gate FR-AC-016 §3 — on-platform).
10. Retorna `{identityId, trainingId, status:'training'}`.

**`action:'poll'`** — grátis, owner-scoped, idempotente:
1. Lê a linha (owner). `GET /v1/trainings/{training_ref}`.
2. `succeeded` → `identity_storage_key`=`output.weights` + `status='active'` + observation node na mesh. `failed`/`canceled` → `status='revoked'` + error. Guard `status='training'` (reconcile 1×).

## Verification gates (material)

- 401 sem JWT · 403 sem consent · 402 sem replicate key (curl com JWT throwaway).
- Plumbing zero-custo: `GET /v1/account` + `GET /v1/models/ostris/flux-dev-lora-trainer` com a key do user retornam 200 (autentica sem gastar).
- Witness pago (ação do Sovereign): `action:start` com retratos reais → HTTP 201 + training id → `avatar_identities` row `status='training'`. `action:poll` após ~20-30 min → `status='active'` + `identity_storage_key` não-nulo.

## Recovery path

- **start falhou pós-INSERT** (training criado, linha não): a linha só existe após o `POST /trainings` retornar id → sem órfão. Se o INSERT falhar depois do training criar, o training roda mas fica sem linha; recovery = `action:poll` não acha → operador re-dispara start (novo training; o antigo expira sem uso — custo perdido, logado em `infra_health_logs`).
- **poll perdido** (edge caiu no meio): `action:poll` é reexecutável (idempotente, guard `status='training'`) → reconcilia. Self-heal molde `finalize_vision_job`.
- **training failed na Replicate**: poll seta `status='revoked'` + error surfaced no inspector; operador sobe retratos melhores e re-dispara.

## Success signal

`avatar_identities` row do user com `status='active'` + `identity_storage_key` (URL do `.tar`) + `commercial_license_ok=true` + observation node na mesh. Materialmente: `SELECT status, identity_storage_key FROM avatar_identities WHERE id=<id>` → `active` + URL não-nula.

## Compliance (FR-AC-016 — 3 travas)

1. **On-platform only** — inferência (fatia futura) roda SÓ na Replicate hospedada; `substrate='flux-dev-lora'` nunca despacha para gerador local.
2. **No-export** — `identity_storage_key` é server-side only, usado só como `lora_weights` de predição Replicate; **nunca** exposto como download ao cliente.
3. **License-version pin** — FLUX.1-dev v1.1.1 (HF); re-verificar em updates (OTD-AC-016-LICENSE-VERSION-PIN).

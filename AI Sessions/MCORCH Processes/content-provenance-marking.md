# SOP — Marcação de Proveniência (AI Act Art. 50) · content-provenance Fatia 0-1

> **Status:** ATIVA v1.0 · 2026-07-16 · Lei 2. **BoK SSOT:** `docs/bok/content-provenance/` (FR-CP-006/007/009/010/012/013).
> **Escopo desta SOP:** camada **C3 (IPTC/XMP)** — o marcador machine-readable "gerado por IA" que Meta/LinkedIn/X leem, embutido em imagem/vídeo via ExifTool, USD=0, zero cert/modelo. C1 (C2PA) e C2 (watermark) são Fatias 2-3 (gated).
> **Deadline regulatório:** AI Act Art. 50(2) vigora **2026-08-02** (multa Art. 99 até €15M/3%).

---

## Operator

| Papel | Quem | Ferramenta |
|---|---|---|
| Marcador (runtime) | host worker `provenance-bridge` | `scripts/provenance-bridge.ts` + `exiftool` (host binary, `libimage-exiftool-perl`) |
| Owner | Sovereign | blast radius: falso-sucesso de declarar "marcado" um asset que saiu sem o tag (FM-CP-01) |

## Sequence (o worker, por asset)

1. **Sweep** `creative_assets WHERE provenance_status='pending' AND kind IN ('image','video')` (usa o index parcial da migration `20260716230000`; áudio excluído — IPTC não cobre áudio, OTD-CP-007). Critério: N linhas pendentes.
2. **Download** do objeto do bucket privado (service-role — RLS bypass; objeto owner-scoped). Critério: bytes no temp.
3. **Embed + verify** (`embed-iptc-core`): `exiftool -XMP-iptcExt:DigitalSourceType=<URI>` → **lê de volta** e só segue se o round-trip bate (verify-before-claim, DG-3). URI = `http://cv.iptc.org/newscodes/digitalsourcetype/{trainedAlgorithmicMedia|compositeWithTrainedAlgorithmicMedia}`. Critério: `res.ok === true`.
4. **Re-upload** in-place (`upsert`, mesma key → signed URLs seguem válidas). Critério: sem erro de upload.
5. **Flip** `provenance_status='embedded'`, `provenance_layers={iptc}`, `provenance_source_type`, `provenance_embedded_at=now()`, `file_size_bytes` (service-role). Critério: linha atualizada.
6. **Observação na malha** (`mcorch_nodes` observation + `embed-mcorch-node`, best-effort fail-soft) — FR-CP-012 §4.
7. **Telemetria** `infra_health_logs service='content-provenance'` (`provenance_embedded` | `provenance_failed`).

Falha em qualquer passo → `provenance_status='failed'` (fail-soft) + telemetria degraded; NUNCA declara marcado sem verify.

## Verification gates

| Gate | Prova material |
|---|---|
| **G1** round-trip | worker só marca `embedded` se `exiftool` relê o mesmo URI que escreveu |
| **G2** objeto real carrega o tag | baixar fresco do bucket + `exiftool -s3 -XMP-iptcExt:DigitalSourceType <obj>` = a URI (provado 2026-07-16 no asset `bc03a65a`: roadmap-master PNG 2480×8474 íntegro) |
| **G3** DB terminal | `SELECT provenance_status, provenance_layers` = `embedded, {iptc}` |
| **G4** sem falso-positivo | arquivo virgem → `readIptcMarker` = null (smoke P3) |
| **G5** vídeo | MP4 também aceita o XMP (provado 2026-07-16 no asset `d57e3341`) |
| **G6** hermético re-executável | `bun run scripts/qa/smoke-provenance-iptc.ts` 6/6 (gera PNGs próprios; zero DB/bucket/rede) |

## Recovery path

- **Embed falha** (formato exótico) → status `failed`; re-rodar após corrigir o formato; o sweep re-pega `pending`, não `failed` (evita loop). Para re-tentar um `failed`: `UPDATE creative_assets SET provenance_status='pending' WHERE id=<id>` (service-role).
- **Objeto corrompido pós-embed** → o verify-before-claim bloqueia antes do re-upload; o original no bucket permanece intacto.
- **Backlog** (todos os assets nasceram `pending` com a migration) → `bun run scripts/provenance-bridge.ts --once --limit N` em lotes, OU habilitar o daemon (systemd, gate Sovereign).
- **Re-embed após transformação** (reshape dropa XMP, OTD-CP-008) → a transformação deve resetar `provenance_status='pending'`; o sweep re-marca. (wire-up = fatia futura.)

## Success signal

Um asset de imagem/vídeo REAL, baixado do bucket, carrega `XMP-iptcExt:DigitalSourceType` = a URI IPTC — legível por qualquer verificador (ExifTool, Meta, LinkedIn, X). Provado E2E 2026-07-16 (`bc03a65a` imagem + `d57e3341` vídeo).

## Operational: habilitar o daemon (GATE SOVEREIGN)

O worker roda on-demand (`--once`) hoje. Para marcação contínua (backfill dos ~90 assets legados + todo novo asset):
```bash
systemctl --user enable --now provenance-bridge.service   # unit em ~/.config/systemd/user/ (ação Sovereign)
```
O unit file de referência está versionado em `scripts/systemd/provenance-bridge.service`. **Não habilitado nesta sessão** — habilitar re-uploada todos os objetos legados (mutação de produção), decisão do Owner.

## Known debt / gates

- **Fatia 2 (C2PA)** cobre a **voz** (IPTC não cobre áudio) — gated em OTD-CP-003 (cert).
- **Fatia 3 (watermark)** embute o `creative_assets.id` opaco (nunca PII, OTD-CP-013) — gated em OTD-CP-009 (compute).
- **Upload-teste Meta/LinkedIn/X** que prova o rótulo VISÍVEL (não só embutido) = próximo witness quando as contas estiverem conectadas (o rótulo IPTC→auto-label é MEDIUM confidence, §10 blueprint — validar por upload real).
- **Injection point ideal** (marcar ANTES de `register_creative_asset` finalizar) vs o sweep atual (marca pós-registro): o sweep é o MVP; o inline no render é hardening.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

# SOP — Worker de segmentação/reframe/caption (video-repurpose Fatia 2) (Lei 2)

> **Feature:** Pilar II do motor `video-repurpose` — 1 master 16:9 → N shorts verticais (9:16/1:1, reframe center-safe + legenda queimada), pela fila `video_renders` (engine `repurpose`, rail FFmpeg **grátis**).
> **BoK SSOT:** `docs/bok/video-repurpose/00-deepsearch-blueprint.md` §Pilar II + §8. Molde do worker: `scripts/video-bridge.ts`.

## ORO triplet
- **Operator:** o worker host (`video-repurpose-bridge.service`, systemd --user); dispara pelo nó/edge `video-repurpose-run`.
- **Reviewer:** `/security-review` (migration + enqueue + worker) + Vision QA no clipe + Sovereign.
- **Owner:** Sovereign — rail grátis (charged_mco=0), sem cobrança.

## Operator — manual equivalente
Hoje o operador abriria um editor, cortaria N trechos, reenquadraria cada um p/ 9:16 e queimaria legenda à mão. Este SOP automatiza isso via FFmpeg determinístico (o núcleo `segment-core.ts`, provado por Vision QA 2026-07-12).

## Sequence
| # | Passo | Executor | Sucesso material |
|---|-------|----------|------------------|
| 1 | Client/nó chama `video-repurpose-run` (user-JWT) com `{ source_asset_id, clips:[{in_sec,out_sec,caption?,reframe?}], fps? }`. | Client | HTTP 202 `{ ok, render_id }`. |
| 2 | `video-repurpose-run` resolve o source **owner-scoped** (`creative_assets` `.eq id .eq user_id`, kind='video') + re-valida `(bucket allowlist, prefixo ${uid}/, no ..)` → escreve `video_renders` (engine='repurpose', charged 0, `composition`={source,clips,fps}). | Edge (service-role) | linha `video_renders` queued de A com a cut-spec. |
| 3 | O worker `video-repurpose-bridge` faz claim atômico (queued→running) + reaper de dead-worker (15min). | Worker | 1 worker pega o job. |
| 4 | **OTD-VR-006:** o worker RE-VALIDA `comp.source` (allowlist+prefixo+`..`) no READ (não confia na linha) → baixa o master → `segmentVideo` (FFmpeg: `-ss/-t` trim + crop-9:16/1:1 center + `drawtext` caption via textfile). | Worker | N clipes MP4 no /tmp. |
| 5 | Upload de cada clipe → `${uid}/repurpose/${renderId}/clip_NNN.mp4` + `register_creative_asset` (kind='video', parent=master) + `finalize_video_render(done, refund 0)`. | Worker | N `creative_assets` do dono; `video_renders` done. |
| 6 | Os clipes (creative_assets) já são publicáveis pelo nó "Publicar em Rede Social" (`publish-space-asset`). | — | disponível na Biblioteca/picker. |

## Verification gates
- **G1 owner-scoping (FMEA-011/OTD-VR-006):** enqueue de source alheio → 404; o worker rejeita `comp.source` fora do allowlist/prefixo → `source_ref_rejected` (finalize failed). Nunca baixa/assina objeto de outro tenant.
- **G2 core FFmpeg:** 1 clipe 9:16 renderizado e **INSPECIONADO** (Vision QA) — center-crop mantém o sujeito, ESQ/DIR cortados, legenda queimada. **PROVADO 2026-07-12** (master sintético → clipe 9:16 + 1:1).
- **G3 grátis:** charged_mco=0; finalize refund=0 (sem money-mint).
- **G4 sem injeção:** `spawn('ffmpeg', args[])` (sem shell); caption via `textfile=` (sem escaping inline); paths derivam do renderId (UUID). 
- **G5 enqueue contract:** smoke `smoke-video-repurpose.ts` 5 gates (own→202, cross→404, bad-range→422, too-many→422, cross-select=0).

## Recovery path
- **Passo 4 (source_ref_rejected/download_failed):** o master não existe/não é do dono/bucket inválido → re-ingerir (Fatia 1) e re-enfileirar.
- **Passo 4/5 (FFmpeg falha num clipe):** o worker finaliza `failed` (refund 0) — reexecutar com a cut-spec corrigida (in/out válidos).
- **Worker morto:** o reaper (15min) devolve `running`→`queued` p/ re-claim.

## Success signal
`video_renders` do dono `state='done'` + N `creative_assets` kind='video' `parent_asset_id`=master sob `${uid}/repurpose/` — prontos p/ o sink social.

## Modo carrossel (Fatia 3 — Pilar III)
O MESMO worker/fila (`engine='repurpose'`) atende `composition.mode='carousel'`: extrai key-frames do master (nos `t_sec` dos slides, ex. capítulos/`atos`), compõe slides 1080×1350 (4:5) via `carousel-core.ts` (key-frame center-crop + legenda wrapped + handle), e registra cada um como `creative_assets` **kind='image'** (`parent`=master). Enqueue via `video-repurpose-run` com `slides:[{t_sec,caption?}]` (≤10, IG max) + `handle?`. Publicação: `publish-space-carousel` resolve os slides owner-scoped → assina → `publish-social` branch **media_type=CAROUSEL** (N children `is_carousel_item` → parent → `media_publish`, contrato Meta). **Alcance real gated na auditoria de app IG (ação Sovereign).** Legenda: wrap conservador (OTD-VR-007 — curtas saem limpas; typografia pixel-perfect via render-core = refinamento). **PROVADO E2E na produção 2026-07-12** (master → 3 slides 1080×1350 registrados + Vision QA no slide real).

## Notas de design
- **Reframe source-agnóstico** (crop por expressão: maior retângulo centrado do aspect-alvo). Center-safe MVP; **OTD-VR-002** crop subject-aware diferido.
- **Caption = texto por clipe** (drawtext textfile). Burn de SRT com offset ao timeline do clipe = refinamento (OTD).
- **Clipes registrados `source_module='hyperframes'`** (família de vídeo FFmpeg-renderizado; evita migration de source_module) + `parent_asset_id`=master + `metadata.repurpose` p/ lineage.
- **systemd:** `video-repurpose-bridge.service` (ação Sovereign, molde `video-bridge.service`); secrets do `../.env` (nunca na unit).

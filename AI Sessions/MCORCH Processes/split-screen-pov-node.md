# SOP — Nó Tela Dividida (POV) · split-screen 9:16 (Lei 2)

**Status:** ACTIVE · v1.0 · 2026-07-21 · SSOT: `docs/bok/spaces-evolution/27-amendment-split-screen-pov.md` (FR-SPACES-097..100)

## Operator

Hoje (manual): o Sovereign — ou o Agent em scratch — compõe com FFmpeg à mão (witness 2026-07-20: `vstack` do corte finale + POV Veo). Com o nó: **qualquer usuário do Spaces**, pela UI.

## Sequence (fluxo manual equivalente, que o nó automatiza)

| # | Passo | Critério de sucesso material |
|---|-------|------------------------------|
| 1 | Produzir o TOPO: um corte 9:16 com legenda queimada (rail repurpose — `video-repurpose-run` → worker → asset em `video-studio-assets`) | asset `kind=video` na biblioteca, `provenance_status=embedded` |
| 2 | Produzir o BAIXO: POV Veo no nó Imagem→Vídeo (Amendment 25 — refs de identidade do personagem, 9:16, 8s; prompt selfie/vlog, "He does not speak") | `veo-poll` → `status:done`, asset em `canvas-assets/<uid>/veo/` |
| 3 | Abrir o nó Tela Dividida no projeto Spaces → escolher topo + baixo (pickers da biblioteca; baixo auto-preenche se um nó de vídeo com output estiver conectado em `input_bottom_video`) → áudio (default: topo) | inspector mostra os 2 títulos escolhidos |
| 4 | Renderizar (12 mco) → `video-render` valida/resolve owner-scoped → 202 `{render_id}` → linha `video_renders` queued | HTTP 202 com `render_id`; 422 sem débito quando fonte/áudio inválidos |
| 5 | Worker `video-bridge` claim → download Storage service-role (re-valida `${uid}/` + bucket) → `split-screen-core` (vstack 1080×1920, `-shortest`, piso 100KB) → upload → `register_creative_asset` → `finalize_video_render done` | `state=done` + `storage_key` preenchido; asset novo na biblioteca com parent = topo |
| 6 | Inspector poll (SELECT-own) detecta done → assina URL → preview no nó | vídeo toca no inspector; asset visível em /dashboard/spaces/assets |

## Verification gates

- **G1 (zero-custo):** anon → 401; `mode:'split_screen'` sem fontes → 422 `split_sources_required` SEM débito; `audio:'x'` → 422; `dry_run` → `cost_mco: 12` sem linha.
- **G2 (tenancy):** `top_asset_id` de OUTRO tenant → 422/404 sem débito (resolve owner-scoped devolve nada).
- **G3 (materialidade):** render real → `video_renders.state=done`, MP4 ≥100KB, `ffprobe` = 1080×1920, asset registrado (`source_job_id = render_id`).
- **G4 (ocular, Lei 1):** frame extraído mostra as DUAS metades com conteúdo (topo = corte, baixo = POV) e divisão no meio. Vision QA em mídia real é o detector honesto.
- Smoke re-executável: `scripts/qa/smoke-split-screen.ts` (G1+G2 sempre; G3/G4 gated por flag `--live` porque debitam 12 mco).

## Recovery path

- 422 no enqueue → nada debitado, nada criado; corrigir fontes/áudio e reenviar.
- Worker morto/timeout → reaper do rail devolve running→queued (60 min); refund automático via `finalize_video_render(failed, refund)` quando o render falha de verdade.
- Render `done` mas vídeo errado (metade congelada/preta) → é conteúdo, não infra: refazer com outras fontes; o débito foi por render entregue (mesma semântica do cinematicVideo).
- Worker stale após mudar código: `systemctl --user restart video-bridge.service` (lição `reference_hyperframes_worker_restart`).

## Success signal

Asset novo `kind=video` 1080×1920 na biblioteca do usuário, com as duas metades vivas, áudio conforme seleção, proveniência embedada pelo provenance-bridge, e o nó no Spaces exibindo o preview — reproduzindo pela UI o witness manual de 2026-07-20 sem nenhum passo de terminal.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

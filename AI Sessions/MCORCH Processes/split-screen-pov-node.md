# SOP — Nó Tela Dividida (POV) · split-screen / split-grid 9:16 (Lei 2)

**Status:** ACTIVE · v1.2 · 2026-08-11 · SSOT: `docs/bok/spaces-evolution/27-amendment-split-screen-pov.md` (FR-SPACES-097..100) + [`28-amendment-split-grid.md`](../bok/spaces-evolution/28-amendment-split-grid.md) + [`28-bis`](../bok/spaces-evolution/28-bis-amendment-split-grid-layouts-and-framing.md) (FR-SPACES-118/119) + [`46-amendment-grid-caption-layer.md`](../bok/spaces-evolution/46-amendment-grid-caption-layer.md) (FR-SPACES-185..188)

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

## Adendo v1.2 (2026-08-11) — grid de N linhas · corte 16:9 nativo · legenda alpha livre

Diretiva Sovereign de 2026-08-11: cortes em **16:9 nativo** compostos num grid vertical de **2 e de 3 linhas**,
com a legenda como **camada alpha posicionável livremente**, inclusive na costura entre linhas.

### Sequence (o que muda em relação ao fluxo acima)

| # | Passo | Critério de sucesso material |
|---|-------|------------------------------|
| 1' | Cortar em **16:9 nativo** (não 9:16): no wizard de Cortes, Formato = **"16:9 (Horizontal)"** → `reframe:'16:9'` → alvo 1920×1080 | `ffprobe` do corte = 1920×1080, não 1080×1920 |
| 2' | ⚠️ **A legenda de beats NÃO acompanha o corte 16:9.** `segment-core` recusa o overlay fora de 9:16 (os templates são safe-area 9:16) e **avisa em vez de renderizar errado** — guarda OTD-VR-008. Corte 16:9 sai **sem legenda queimada**, por design: quem legenda é o `caption_layer` do grid | log `overlay de beats indisponível em 16:9`; clipe limpo |
| 3' | Escolher o layout: **`2v`** (2 linhas, célula 1080×960) ou **`1x3`** (3 linhas, célula 1080×640) | botão do layout marcado; `CELL_COUNTS` exige 2 ou 3 células |
| 4' | Escolher o encaixe (FR-SPACES-186): **Preencher** corta as laterais (`2v` −37%, `1x3` −5%); **Encaixar** preserva o quadro e abre faixa (`2v` = 352px contíguos na costura; `1x3` = 32px, praticamente nada) | preview espelha o encaixe escolhido |
| 5' | Posicionar a legenda (FR-SPACES-185): texto + `y ∈ [0,1]` + faixa `none/solid/gradient` | preview mostra a legenda na altura pedida |

### Verification gates adicionais

- **G5' (determinismo):** sem `caption_layer` e sem `cell_fit`, o render sai **sha-idêntico** ao anterior — `sha256sum` de duas saídas da mesma spec (NFR-VS-016).
- **G6' (injeção):** legenda com `"` `\` `%` `:` e emoji renderiza correto e **não escapa o filtergraph** — o texto vai por `textContent` no template HTML, nunca na string do filtro.
- **G7' (o falso-sucesso conhecido):** layout ausente do `CELL_COUNTS` deve **falhar**, não colapsar para `2x2` em silêncio (armadilha registrada em `video-bridge.ts:154-156`).
- **G8' (ocular):** frame extraído com Vision QA — a legenda está legível **e** na altura pedida; a faixa, quando `fit`, não engole imagem.

### Escolha de formato — a aritmética que decide

| Grid | Preencher (perda lateral) | Encaixar (faixa contígua) | Quando usar |
|------|---------------------------|---------------------------|-------------|
| `2v`  | −37% da largura | **352px** de faixa | quando a legenda precisa de faixa própria |
| `1x3` | **−5%** da largura | 32px (inútil) | quando o quadro 16:9 precisa sobreviver inteiro → legenda **sobreposta** |

**Regra prática:** `1x3` + Preencher + legenda sobreposta é o formato barato que quase não corta.
`2v` + Encaixar + faixa é o formato com tarja. Nunca `2v` + Preencher com material que tenha informação nas
bordas — 37% da largura vai embora.

### Recovery path adicional

- Legenda ilegível/na altura errada → é composição, não infra: re-renderizar com outro `y`/faixa. O débito
  foi por render entregue (mesma semântica das demais falhas de conteúdo).
- Corte 16:9 saiu com legenda queimada indevida → veio de spec com `caption_mode` explícito; o default correto
  para célula de grid é `caption_mode:'none'`.

# SOP — Ingest de vídeo externo (porta de 1ª classe) (Lei 2)

> **Feature:** Pilar I / Fatia 1 do motor `video-repurpose` — ingerir um master MP4 externo (documentário 16:9) + metadados estruturados + SRT como um `creative_assets` owner-scoped, para o worker de segmentação (Fatia 2) cortá-lo em N shorts.
> **BoK SSOT:** `docs/bok/video-repurpose/00-deepsearch-blueprint.md` §Pilar I + §5 (decisão de schema).
> **Decisão de schema (provada §5):** `source_module='external'` aditivo em `creative_assets` (não tabela dedicada — o spine é lido por todos os consumidores). Money-path intocado.

## ORO triplet
- **Operator:** MCORCH Master Execution Agent (constrói/prova) — na operação, o Usuário Zero pela UI.
- **Reviewer:** `/security-review` no seam + na migration (cross-tenant é o gate-mãe) + Sovereign.
- **Owner:** Sovereign — nenhuma cobrança mcoCoins (ingest é grátis).

## Operator — manual equivalente
Hoje, para reaproveitar um documentário, o operador baixaria o MP4, abriria um editor e cortaria à mão. Este SOP dá a **porta de entrada** in-system (o resto — cortar/reenquadrar/legendar — são as fatias seguintes).

## Sequence — ordem (cada passo com critério material)
| # | Passo | Executor | Sucesso material |
|---|-------|----------|------------------|
| 1 | Client sobe o MP4 do master para `canvas-assets` sob `${uid}/external/<id>/master.mp4` (bucket privado owner-scoped já selado, migration `20260703030000`). | Client (Storage) | objeto existe sob o prefixo do dono. |
| 2 | Client invoca `ingest-external-asset` (user-JWT) com `{ storage_key, provider:'upload', title, mime_type, duration_seconds?, width?, height?, srt_pt?, srt_en?, episode:{titulo,subtitulo,atos[],creditos,teaser,tags} }`. | Client | HTTP 200 `{ ok, asset_id }`. |
| 3 | `ingest-external-asset` re-verifica o caller (`getUser`), valida `storage_key` começa com `${user.id}/` (owner-scoped — nunca confia em path cross-tenant), e registra via `register_creative_asset(source_module='external', kind='video', ...)` com os metadados + SRT inline no `metadata` jsonb. | Edge (service-role) | linha `creative_assets` do dono com `source_module='external'`, `metadata.episode` + `metadata.srt`. |
| 4 | (Fallback) `provider:'youtube'` → **gated** (OTD-VR-001: download server-side bloqueado por IP de datacenter). Retorna 501 estruturado orientando upload do MP4. | Edge | 501 `youtube_ingest_gated`. |

## Verification gates
- **G1 owner-scoping (FM-VR-01):** `storage_key` que não começa com `${user.id}/` → 400 (nunca registra asset de outro prefixo). O asset registrado é sempre do caller (`register_creative_asset` seta `user_id=caller`).
- **G2 source_module='external' aceito:** `register_creative_asset('external')` insere (não mais `22023 invalid source_module`).
- **G3 default-deny:** INSERT direto autenticado em `creative_assets` continua negado (RLS já selada); escritor = a RPC service-role.
- **G4 metadados preservados:** `metadata.episode.atos`/`creditos.blocos`/`teaser`/`tags` + `metadata.srt.{pt,en}` presentes na linha (para o mapeador da Fatia 4 não perder capítulos/fontes).
- **G5 money-path intocado:** `channel_variants`/reshaper inalterados; `smoke-reshape-pillar` 17/17 verde.

## Recovery path
- **Passo 2 (400 owner-scope):** o client subiu num prefixo errado — re-upload sob `${uid}/external/`.
- **Passo 3 (register falha):** a migration não foi aplicada (`22023 invalid source_module 'external'`) → aplicar `20260712xxxxxx_creative_assets_external_source.sql` (apply-gate Sovereign).
- **Fallback YouTube:** enquanto OTD-VR-001 aberta, o caminho é upload do MP4 (preferido de qualquer modo por qualidade).

## Success signal
`creative_assets` do dono com `source_module='external'`, `kind='video'`, apontando o MP4 no bucket privado, `metadata` carregando episódio+SRT — pronto para o worker de segmentação (Fatia 2) enfileirar em `video_renders` (engine 'repurpose').

## Notas de design
- **SRT inline no metadata jsonb** (não como storage object): SRT é texto pequeno (~10-30KB/episódio) e `canvas-assets` restringe MIME a image/video/audio (rejeitaria `.srt`). Inline evita bucket extra + o objeto órfão.
- **Bucket = `canvas-assets`** (reuso do bucket privado owner-scoped já selado) sob prefixo `${uid}/external/`. Sem migration de storage nova na Fatia 1.
- **YouTube fallback gated (OTD-VR-001):** `reference_youtube_datacenter_workarounds` — datacenter bloqueado; download real = host worker / ação Sovereign, fatia posterior.

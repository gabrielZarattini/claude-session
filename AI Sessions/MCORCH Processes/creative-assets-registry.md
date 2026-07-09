# SOP — creative_assets registry (bidirectional asset interop spine)

> **Lei 2 (Processo Antecipado).** Como cada módulo do ecossistema (canvas-studio · hyperframes · open-design ·
> content-pipeline · generate-image · faceless) **registra e reusa** assets uns dos outros, bidirecional, com
> proveniência. Fatia 1 do [[project_creative_ecosystem_program]]. Migration `20260625120000_creative_assets_registry.sql`.

Relacionado: `supabase/functions/canvas-execute` · `scripts/video-bridge.ts` · `supabase/functions/generate-image` ·
`scripts/design-bridge.ts` · buckets `canvas-assets`/`video-studio-assets`/`generated-images`/`public`.

## ORO
| Papel | Quem |
|-------|------|
| Operator | MCORCH Master Execution Agent (dual-write nos produtores) |
| Reviewer | Sovereign + `/security-review` (migration cross-tenant) |
| Owner | Sovereign — blast radius = índice de assets per-tenant (RLS own-or-org) |

## Contrato (a tabela = índice fino sobre os buckets que já existem)
`creative_assets {id, user_id(RLS), org_id?, kind(image|video|audio|design|article|template), storage_bucket,
storage_key, is_public, mime_type, file_size_bytes, width, height, duration_seconds, parent_asset_id(proveniência),
source_module, source_job_id, mesh_node_id, provider, model, prompt, title, tags[], is_favorite, metadata}`.
**Um objeto de Storage = uma linha** (UNIQUE bucket+key). Bytes NÃO migram — a linha só aponta.

## Sequence
| # | Passo | Critério material |
|---|-------|-------------------|
| 1 | Migration aplicada (tabela + RLS + `register_creative_asset`) | `/security-review` SAFE · tabela existe no DB live |
| 2 | **Dual-write fail-soft** em cada produtor: no caminho de sucesso, chamar `register_creative_asset` via service-role. NUNCA quebrar o produtor se o registro falhar (try/catch silencioso + telemetria) | a linha aparece em creative_assets após uma geração real |
| 3 | Asset-picker lê `creative_assets` por `kind` (own-or-org RLS) | o picker mostra assets de OUTRO módulo |

## Verification gates
1. `register_creative_asset` é service-role-only (anon/authenticated → permission denied).
2. RLS: tenant A não vê asset de tenant B (cross-tenant SELECT = 0 linhas).
3. Idempotência: 2 registros do MESMO objeto → 1 linha (ON CONFLICT refresh).
4. Produtor real (ex.: video-bridge no finalize) grava a linha sem quebrar o render.

## Recovery
| Falha | Fix |
|-------|-----|
| dual-write lança e quebra o produtor | envolver em try/catch fail-soft; o asset já está no bucket — registro é best-effort |
| ON CONFLICT sobrescreve tenant errado | guard `WHERE user_id = EXCLUDED.user_id` no DO UPDATE (já no RPC) |
| asset privado sem preview no picker | `is_public=false` → o cliente pede signed URL; público → URL direta |

## Success signal
Um asset gerado no Canvas Studio aparece no asset-picker do editor HyperFrames (e vice-versa), com a cadeia de
proveniência (`parent_asset_id`) visível — o bidirecional do "poder das saídas".

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

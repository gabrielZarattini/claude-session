# SOP — space_publish_variants: publicação media-social de asset do Spaces (Lei 2)

> **Feature:** destrava a **Fatia B media-social** do Spaces (OTD-SPACES-036) — publica um asset (vídeo/imagem) criado no Spaces em IG/TikTok/YouTube/etc. pela via owner-scoped já selada (`auto-publish` → `publish-social`), **sem** acoplar a `channel_variants` (que é `pillar_run_id NOT NULL`, do money-path).
> **Decisão de schema:** opção (b) do ADR `docs/bok/spaces-evolution/16-decision-otd-spaces-036-media-social-schema.md` (GO Sovereign 2026-07-09) — tabela dedicada `space_publish_variants`.
> **BoK SSOT:** ADR 16 + Amendment 15 (`15-amendment-social-publish-nodes.md`, FR-SPACES-031 seam `publish-space-asset`).
> **Invariantes (do ADR §1):** I1 money-path intocado · I2 FMEA-011 owner-scoping · I3 idempotência · I4 verdade financeira limpa (`pipeline_runs` intocado).

---

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (constrói e prova) — na operação viva, o Usuário Zero pela UI do nó Spaces.
- **Reviewer:** `/security-review` independente na migration + no branch do `auto-publish` (gate-mãe FMEA-011) + Sovereign.
- **Owner:** Sovereign — blast radius sobre a distribuição social per-tenant; nenhuma cobrança mcoCoins nova (publish social é grátis, igual ao pillar).

---

## Operator — quem executa hoje (manual equivalente)

Hoje, para publicar um criativo do Spaces numa rede social, o operador humano teria que: (1) baixar o MP4/imagem do bucket; (2) abrir o app da rede; (3) subir manualmente com legenda. **Não há via in-system** (só WordPress, que publica direto). Este SOP automatiza esse gesto reusando o publisher owner-scoped já selado.

## Sequence — ordem de execução (cada passo com critério material)

| # | Passo | Executor | Critério de sucesso material |
|---|-------|----------|------------------------------|
| 1 | O nó **"Publicar em Rede Social"** (media-social) no canvas Spaces recebe um asset upstream (imagem/vídeo já registrado em `creative_assets`) + o usuário escolhe canal/superfície + legenda + Rascunho/Publicar. | Usuário (UI) | O inspector tem `source_asset_id` resolvido do nó upstream + `channel`/`surface`/`platform` + `native_text.caption`. |
| 2 | O nó invoca `publish-space-asset` (user-JWT). | Client | HTTP 200 `{ ok, space_publish_variant_id, status }`. |
| 3 | `publish-space-asset` re-verifica o caller (`getUser`), resolve o asset **owner-scoped** de `creative_assets` (`.eq id` + `.eq user_id`) → extrai `storage_bucket`/`storage_key`/`kind` **server-trusted**. | Edge (service-role) | 404 `asset_not_found` se o asset não é do caller; senão bucket/key resolvidos da linha do dono. |
| 4 | Upsert idempotente em `space_publish_variants` (âncora `UNIQUE(user_id, source_asset_id, channel, surface)`) com o asset ref server-trusted + `native_text`. `status='draft'`. | Edge (service-role) | Linha existe com `user_id = caller`, `asset_bucket/asset_key` = os do dono. Retry (mesmo asset/canal/surface) NÃO duplica (upsert). |
| 5 | Se `publish=true`: enfileira `scheduled_posts` (`user_id = caller`, `platform`, `metadata.reshape.{content, space_publish_variant_id}`) + marca a variant `status='scheduled'` + `scheduled_post_id`. Default (`publish=false`) para em rascunho. | Edge (service-role) | `scheduled_posts` tem 1 linha `queued` do dono; a variant aponta pro `scheduled_post_id`. |
| 6 | O cron `auto-publish` (já vivo) pega a linha `queued`, resolve o asset da variant **owner-scoped** (`space_publish_variants` `.eq user_id = post.user_id`), assina URL 6h e chama `publish-social`. | Edge (service-role, cron) | `publish-social` recebe `content.{video_url|image_url}` assinado do dono; publica na rede. |

## Verification gates (como o operador confirma cada passo)

- **G1 — owner-scoping (I2/FMEA-011):** um `source_asset_id` de OUTRO tenant → passo 3 retorna 404 (o `.eq user_id` não casa). O `asset_bucket/asset_key` gravados vêm SEMPRE da linha do dono, nunca de metadata client-writable.
- **G2 — default-deny writes:** `INSERT`/`UPDATE` autenticado direto em `space_publish_variants` é NEGADO (RLS sem policy de escrita). Único escritor = `publish-space-asset` (service-role).
- **G3 — cross-tenant SELECT = 0:** um user lendo `space_publish_variants` só vê as próprias linhas.
- **G4 — idempotência (I3):** re-invocar `publish-space-asset` com o mesmo `(source_asset_id, channel, surface)` → mesma variant (upsert), zero duplicata.
- **G5 — auto-publish fail-closed:** se o `space_publish_variant_id` no metadata for de outro tenant, o `.eq user_id = post.user_id` retorna nada → nenhum asset assinado (sem vazamento).
- **G6 — money-path intocado (I1):** `smoke-reshape-pillar.ts` 17/17 continua verde; `channel_variants` e `reshape-pillar` inalterados.

## Recovery path — falha no passo N

- **Passo 3 (asset_not_found):** o nó upstream não registrou o asset em `creative_assets` (ou é de outro projeto/tenant). Recovery: re-executar o nó gerador (canvas-execute registra o asset) e reconectar.
- **Passo 5 (enqueue_failed):** rollback natural — a variant fica `draft` (não `scheduled`); reexecutar `publish-space-asset` com `publish=true` (idempotente).
- **Passo 6 (publish falha na rede):** `auto-publish` já tem retry (`retry_count`/`max_retries`); após `max_retries` a `scheduled_posts` vira `failed` com `error_message`. Recovery: corrigir a credencial social (Configurações) e re-enfileirar.

## Success signal — sinal materialmente observável do flow completo

`scheduled_posts` do dono em `status='published'` **E** a variant em `space_publish_variants` com `status='scheduled'`/`published` **E** o post real na rede (id retornado por `publish-social`). Para o modo rascunho: a variant existe `status='draft'`, publicável depois.

---

## Notas de design (fidelidade + desvios honestos vs. ADR §3.1)

- **Sem coluna `scheduled_posts.source` (SD-1 reconciliado):** o dispatch no `auto-publish` é por **presença de `metadata.reshape.space_publish_variant_id`** — espelha exatamente o padrão selado de `channel_variant_id` (`auto-publish/index.ts:112-132`). Adicionar uma coluna seria superfície extra sem ganho; a presença do campo no reshape É o marcador de origem. Zero mudança em `scheduled_posts`.
- **Âncora de idempotência = `UNIQUE(user_id, source_asset_id, channel, surface)`** (não `(node_run_id, channel, surface)` do sketch): `node_run_id` é um id de nó do canvas (string client-supplied, **não** UUID como `pillar_run_id`) → incluí-lo numa UNIQUE global arriscaria **colisão cross-tenant** (dois tenants com o mesmo id de nó → o 2º INSERT falha, DoS + leak). Chavear por `(user_id, source_asset_id, channel, surface)` é tenant-scoped por construção e idempotente pela intenção real ("publicar ESTE asset neste canal/superfície uma vez"). `node_run_id` vira campo de linhagem/auditoria (nullable, fora da unique). Refinamento material sobre o sketch (Lei 1).
- **`asset_status` default `'ready'`:** o asset do Spaces já existe (≠ pillar, onde o render é async). Sem estados de render pendente.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

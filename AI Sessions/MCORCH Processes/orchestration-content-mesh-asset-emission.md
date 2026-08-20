# SOP — Orchestration content_mesh_asset Emission

**Versão:** v1 · **Selada:** 2026-05-19 · **Lei 2 (Processo Antecipado)** · **OE-661 Phase 1**

## ORO triplet

- **Operator:** `orchestrate-content` Edge Function (automatizado por trigger de campanha do Usuário Zero ou de cliente)
- **Reviewer:** Sovereign (Gabriel) — aprova primeira execução e valida campos da row no Supabase Studio
- **Owner:** Sovereign — risco reputacional do post WordPress e risco financeiro do affiliate token (`GCRUX_ML_AFFILIATE_TOKEN`)

## Contexto

A função `orchestrate-content` já materializa o flywheel completo (article → WordPress → social → observation node). Falta a peça que conecta o output a Link Forge: um nó `mcorch_nodes(node_type='content_mesh_asset')` carregando o `articleContent` no campo `content`, com `metadata.wordpress_url` populado e `project_id='mcorch-affiliate'`. Link Forge (`scripts/link-forge.ts`) varre essa tabela buscando matches de regex de produtos ML; sem a emissão, o flywheel para no observation node e nunca vira receita monetizável.

**Por que existe:** A v6.6.3 fechou todas as dependências (postback → ATTRIBUTES_REVENUE_TO; auto-stitch observation → file; Link Forge dry-run validado). O único nó faltante é o asset emit. Sem este SOP + código, **o flywheel afiliado nunca rodou end-to-end uma vez em produção** (3 dias com `revenue_cents=0`).

**Decisão de design:** emissão é **paralela** à observation (não sequencial) via `Promise.allSettled` — falha em uma não cancela a outra. Mas com **gate de validade de WordPress URL**: se `wpPostUrl` é null/vazio (WP publish falhou), asset emit é skipped explicitamente (status `skipped`, não `error`) — Link Forge nunca consome row órfã sem URL para republish.

## Shape esperado do node

```json
{
  "user_id": "<sovereign_uuid>",
  "node_type": "content_mesh_asset",
  "name": "content:<campaign_id|ad-hoc>:<topic[:50]>",
  "content": "<articleContent full body>",
  "metadata": {
    "media_type": "article",
    "source": "orchestration",
    "platforms": ["linkedin", "twitter"],
    "campaign_id": "<uuid|null>",
    "wordpress_url": "https://...",
    "wordpress_post_id": 12345,
    "utm_base": "?utm_source=wordpress&utm_medium=social&utm_campaign=...",
    "orchestration_run_id": "<pipeline_run_uuid>"
  },
  "project_id": "mcorch-affiliate",
  "revenue_impact": 0,
  "stability_score": 1.0
}
```

**Por que esses campos:**
- `content` = `articleContent` completo: Link Forge faz regex scan por menções de produto direto no body (linhas 74-83 de `link-forge.ts`)
- `metadata.wordpress_url` = obrigatório: Link Forge precisa do URL para fazer republish via WordPress API após monetizar
- `project_id='mcorch-affiliate'` = tenant scope; Amendment C garante que Link Forge filtra por isso (não cross-tenant)
- `revenue_impact: 0` = populado depois por `handle-ml-postback` via `ATTRIBUTES_REVENUE_TO` edge weight
- `stability_score: 1.0` = baseline; FSRS-6 decay aplica natural ao longo do tempo

## Sequence — fluxo happy path

| # | Action | Output esperado | Verification gate |
|---|--------|-----------------|-------------------|
| 1 | Trigger campaign via `/dashboard/orchestrate` (Usuário Zero) ou cron `auto-publish` (cliente) | POST `/functions/v1/orchestrate-content` com JWT válido | Network HAR: request com Authorization header |
| 2 | `orchestrate-content` valida JWT + deduct atômico 10 mcoCoins via `deduct_mco_coins` RPC | HTTP 200 não-bloqueante se saldo OK; HTTP 402 se balance < 10 | `SELECT mco_balance FROM profiles WHERE id=<user>` → balance−10 |
| 3 | Generate article via OpenRouter (LovableAI fallback) | `articleContent` non-empty string | `pipeline_runs.steps[0].status='done'` |
| 4 | Publish WordPress via `publish-wordpress` Edge Function | `wpPostUrl` populated string ou null em falha | `pipeline_runs.wordpress_url IS NOT NULL` em success path |
| 5 | Schedule social posts (LinkedIn + Twitter via `social_posts` table) | Rows com `scheduled_at +1h/+2h` | `SELECT scheduled_at FROM social_posts WHERE user_id=<user> AND status='queued' ORDER BY created_at DESC LIMIT 2` |
| 6 | `Promise.allSettled([observation_insert, asset_insert])` — **paralelo** | Ambos resultam em fulfilled/rejected granular | `pipeline_runs.steps[]` contém entries `knowledge_mesh` + `content_mesh_asset` |
| 7 | **NEW** Asset insert (com wpPostUrl gate — Amendment B) | Row `node_type='content_mesh_asset'` em `mcorch_nodes` OR skipped se WP falhou | `SELECT id, content, metadata->>'wordpress_url' FROM mcorch_nodes WHERE node_type='content_mesh_asset' AND user_id=<user> ORDER BY created_at DESC LIMIT 1` → 1 row com URL non-null |
| 8 | `trg_mcorch_embed_on_insert` (pg_net) dispara embed assíncrono | `embedding` populated em ≤10s | `SELECT embedding IS NOT NULL FROM mcorch_nodes WHERE id=<asset_uuid>` → true |

## Verification gates (Lei 1 — Materiality)

Comandos reproduzíveis a serem citados no `/handoff`:

```bash
# Gate 6 — observation + asset emitted granular
curl -s "$SUPABASE_URL/rest/v1/pipeline_runs?order=started_at.desc&limit=1&select=id,steps" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" | jq '.[0].steps[] | select(.name | test("knowledge_mesh|content_mesh_asset"))'

# Gate 7 — asset row visible com URL
curl -s "$SUPABASE_URL/rest/v1/mcorch_nodes?node_type=eq.content_mesh_asset&user_id=eq.<sovereign>&order=created_at.desc&limit=1&select=id,name,content,metadata,project_id" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" | jq '.[0]'

# Gate 8 — embedding populated (após ~10s)
curl -s "$SUPABASE_URL/rest/v1/mcorch_nodes?id=eq.<asset_uuid>&select=embedding" \
  -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" | jq '.[0].embedding | length'   # 768

# Link Forge dry-run consumindo o asset
bun run scripts/link-forge.ts --dry-run
# Esperado: preview com `Found N matches` > 0 no novo asset
```

## Recovery path

| Falha | Detecção | Ação | Resultado |
|-------|----------|------|-----------|
| **WordPress publish falhou** (Step 4) — `wpPostUrl=null` | Gate em `Promise.allSettled`: `assetInsert = Promise.reject(new Error("no_wordpress_url"))` antes do submit | Asset NÃO é emitido; `addStep("content_mesh_asset", "skipped", {topic}, {reason:"no_wordpress_url"})` | Sem row em `mcorch_nodes` → Link Forge não monetiza esse run. Sovereign retry manual com fix de WP. |
| **Observation insert falhou + asset insert OK** | `obsResult.status='rejected'` mas `assetResult.status='fulfilled'` | `addStep` reflete granular; pipeline continua | Asset emitido normalmente (Link Forge funciona); observability degradada (sem mesh observation node). |
| **Asset insert falhou + observation OK** (race condition extrema) | `assetResult.status='rejected'` com error message DB | `addStep("content_mesh_asset", "error", {topic}, {reason: err})` | Pipeline declara done com error; Link Forge não pega esse run. Sovereign decide se quer reissue manual. |
| **Embedding nunca chega (>30s pós insert)** | Query no Gate 8 retorna `length=null` ou `0` | Trigger pg_net falha silenciosamente; backfill manual via `bun run scripts/backfill-embeddings.ts` | Embedding eventualmente popula; mesh density preservada. |
| **Cross-tenant Link Forge scan** (Amendment C) | Antes do fix: query global em `content_mesh_asset` sem `project_id` filter | Após fix: `.eq("project_id", "mcorch-affiliate")` força tenant scope | Link Forge só vê assets do tenant esperado; defesa-em-profundidade contra leak. |

## Success signal

- `pipeline_runs.steps[]` contém entry `content_mesh_asset` com `status='done'` em runs com WP success
- `pipeline_runs.steps[]` contém entry `content_mesh_asset` com `status='skipped'` + `reason='no_wordpress_url'` em runs com WP fail (gate funcionou)
- `SELECT count(*) FROM mcorch_nodes WHERE node_type='content_mesh_asset'` cresce monotonicamente a cada run bem-sucedido
- `bun run scripts/link-forge.ts --dry-run` retorna matches > 0 em pelo menos 1 dos novos assets
- Mesh `infra_health_logs` registra `service='orchestrate-content' status='healthy'` (pulse já existente)

## Anti-patterns

- ❌ **Try/catch separado para observation + asset** — quebra Amendment A (Bug A): cobrança 10 mcoCoins com mesh half-emitted, sem rastreabilidade granular do que falhou.
- ❌ **Emit asset sem checar `wpPostUrl`** — Bug B do audit; Link Forge consome row órfã, tenta republish em URL inexistente.
- ❌ **`project_id` ausente no shape** — quebra Amendment C: Link Forge sem filter de tenant scan = risco de cross-tenant leak quando primeiro cliente externo entrar.
- ❌ **`content` truncado ou só metadados** — Link Forge precisa do body completo para regex scan; truncar = matches perdidos = revenue perdido.
- ❌ **Sync block waiting embedding** — embedding é assíncrono via trigger pg_net; aguardar quebra latência de pipeline e não traz valor (Link Forge não depende de embedding).
- ❌ **Skipped marked as error** — confunde análise de saúde; `skipped` é decisão deliberada (Amendment B gate), `error` é bug real.

## Referências

- `supabase/functions/orchestrate-content/index.ts:404-465` (insertion point + bloco completo)
- `scripts/link-forge.ts:74-83` (consumer shape — define metadata mínimo)
- `scripts/link-forge.ts:149-153` (project_id filter — Amendment C)
- `supabase/functions/handle-ml-postback/index.ts` (consumer downstream — fecha o loop com `ATTRIBUTES_REVENUE_TO`)
- `.claude/context/execution-plan-oe661-carryovers.md` (Amendments A-J · plan persistido com 10 emendas pós-audit)
- `docs/processes/canvas-video-async-execution.md` (SOP irmã — padrão de structure deste documento)
- `.claude/rules/survival.md` (Law 2 — este SOP é precondição do código)

# SOP — Channel Reshaper (1 pilar → posts nativos por canal · FR-CP-002/003)

> Lei 2 (Processo Antecipado). O humano que faz isso hoje = um social media manager que pega 1 artigo/vídeo e **reescreve** manualmente uma versão nativa por rede (legenda, gancho, formato, cadência). Este SOP é esse processo, antes do código. SSOT técnico: [`docs/bok/post-engine/13-sdd-reshaper-atomizer.md`](../bok/post-engine/13-sdd-reshaper-atomizer.md).

## Operator
- **Hoje (manual):** social media manager. Pega o pilar (artigo WordPress + vídeo 9:16 + imagem) → para cada rede ativa, reescreve a legenda no tom da rede, escolhe o formato certo (Reel vs feed image vs thread), corta/reformata a mídia, agenda pela cadência.
- **Automatizado:** `atomize-pillar` (bloco no `orchestrate-step`) + `reshape-pillar` (edge fn service-role) + `auto-publish` cron.

## Sequence (cada step com critério material de sucesso)
1. **Atomize** — após o article validar/monetizar no `orchestrate-step`, decompor em `pillar_atoms` (hook, key_points[], stat, quote, cta). ✅ sucesso: `SELECT count(*) FROM pillar_atoms WHERE pillar_run_id=<run>` = 1.
2. **Backfill pillar_url** — após `wordpress_publish`, UPDATE `pillar_atoms.pillar_url = wpPostUrl`. ✅ `pillar_url IS NOT NULL`.
3. **Reshape static** — no fim do `knowledge_mesh`, `POST reshape-pillar {pillar_run_id, scope:'static'}`. ✅ linhas em `channel_variants` p/ surfaces `derive_from ∈ {pillar_atoms,pillar_image,pillar_article}` com `native_text` não-vazio e DISTINTO por canal.
4. **Reshape video** — `video-bridge.ts`, após `finalize_video_render(done)`, `POST reshape-pillar {pillar_run_id, scope:'video'}`. ✅ surfaces de vídeo com `asset_status='reused_master'` + `asset_key` apontando o MP4.
5. **Enqueue (OPT-IN)** — variantes `asset_status ∈ {ready,reused_master}` viram `scheduled_posts` **SÓ quando o run optou por publicar** (`metadata.auto_publish=true`). Default = rascunho (`channel_variants.status='draft'`, zero `scheduled_posts`). Opt-in: (a) per-run `auto_publish` (autopilot honra `hitl_required`), ou (b) ação manual `publish-channel-variant` num rascunho escolhido. ✅ rascunho: 0 `scheduled_posts`; publicado: `scheduled_posts.status='queued'` + `metadata.reshape`.
6. **Publish** — `auto-publish` cron drena, prefere `metadata.reshape.content`, chama `publish-social`/`publish-wordpress`. ✅ `scheduled_posts.status='published'` + `platform_post_id`.

## Verification gates (material)
- **G1 idempotência:** rodar `reshape-pillar` 2× p/ o mesmo run → `channel_variants` count inalterado (UNIQUE pillar_run_id,channel,surface).
- **G2 anti cross-post (FR-CP-007):** `native_text` de 2 canais quaisquer NÃO é byte-idêntico.
- **G3 format gate (FR-CP-006):** surface de imagem PNG marca `format_gate.coerced_format='jpeg'` (IG) / `'webp'` (TikTok); nenhuma surface enfileira publish com formato inválido.
- **G4 channel→enum:** nenhuma INSERT em `scheduled_posts` com `platform='twitter_x'` (22P02). Sempre `'twitter'`.
- **G5 honestidade:** surfaces `pending_*` NÃO aparecem como `published`; aparecem como `channel_variants.status='draft'` + diretiva registrada.
- **G6 tenancy:** `channel_variants` SELECT cross-tenant = 0 linhas (RLS own).

## Recovery path (falha no step N)
- **Atomize falha:** fail-soft heurístico (hook=título, key_points=primeiras frases). Run continua. Reshape usa o que houver.
- **Reshape static/video falha por canal:** fail-open — os outros canais seguem; o canal falho fica `channel_variants.status='failed'` + `infra_health_logs service='reshape-<canal>' status='error'`. Re-disparar `reshape-pillar` re-tenta (UPSERT).
- **Video master nunca finaliza:** surfaces de vídeo ficam `asset_status='pending_render'` (não enfileiram). Re-disparar `scope='video'` quando o master finalizar.
- **Publish falha:** mecânica existente do `auto-publish` (retry_count→max_retries→failed). Inalterada.

## Success signal (fluxo completo)
A partir de **1 pilar**: `channel_variants` com ≥6 surfaces, `native_text` distinto por canal, surfaces de vídeo reusando 1 master, e `scheduled_posts.status='published'` (ou audit-gated SELF_ONLY/private/sandbox) nos publishers vivos (IG Reel · LinkedIn texto · TikTok · YouTube · Pinterest · X). Penalidade de cross-post evitada (G2).

## Materiality caveat (Lei 1)
Publishers audit-gated (TikTok SELF_ONLY · YouTube forced-private pré-Gate-B · Pinterest sandbox) publicam **privado/sandbox** — isso é transporte provado, NÃO alcance público. "Publicado publicamente" só após os audits (ação Sovereign). Reshape ≠ publish: o reshaper prova a **variante nativa**; o alcance é gate separado.

---

## Amendment 2026-07-02 — Resolução da imagem-pilar por âncora de run (fix do `gap` do autopilot)

**Incidente material (Lei 1):** o ciclo pago `77e02fca` (2026-07-01) produziu a imagem-pilar (`content_library` type=image, 01:12) mas TODAS as 5 surfaces de imagem saíram `asset_status='gap'` — a resolução casava só por `campaign_id` (`reshape-pillar:276`), e o autopilot nunca cunha um (`content_library.campaign_id` é FK de `campaigns` do Marketing Hub; o run do ciclo carrega `campaign_id` NULL → o lookup nem dispara).

**Contrato (novo):** `reshape-pillar` resolve a imagem-pilar em 2 passos:
1. **Âncora de run (primária):** `content_library.metadata->>pillar_run_id == <run>` — tag server-set gravada pelo `orchestrate-step` (FR-VA-013) no insert da imagem. 1:1 com o pilar; imune a bleed entre produtos do mesmo ciclo.
2. **Fallback por campanha:** lookup legado por `campaign_id` (fluxos Marketing Hub + linhas anteriores ao fix).

**Gate G7 (novo, material):** run autopilot-shaped (`campaign_id` NULL) com imagem taggeada → surfaces de imagem `asset_status='ready'` (não `gap`). Provado zero-cost por `scripts/qa/smoke-reframe-image.ts` (cenário B, throwaway user, `auto_publish=false` ⇒ draft — sem side effect outward).

**Nota de índice:** o filtro `metadata->>pillar_run_id` roda sem índice (escala Usuário Zero ok); se `content_library` crescer ordens de magnitude, criar índice por expressão.

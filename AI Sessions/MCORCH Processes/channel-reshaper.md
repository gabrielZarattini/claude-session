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

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

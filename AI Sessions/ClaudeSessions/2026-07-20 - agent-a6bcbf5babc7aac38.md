# Session agent-a6bcbf5babc7aac38
**Date:** 2026-07-20 | **Session ID:** `agent-a6bcbf5babc7aac38`

---

## 👤 User *(02:10:27)*


# CONTEXTO REAL (verificado; não invente)

## Objetivo do Sovereign
Transformar /dashboard/youtube em **/dashboard/youtube/studio-yt** — um hub com TUDO do YouTube, incluindo o widget "Publicar vídeo no YouTube" (já existe: YouTubeUploadPanel). A lista "Vídeos do canal (50+)" deve virar clicável: cada vídeo abre uma **página dedicada** com as métricas e análises importantes, **enriquecidas com IA**, explorando as opções NATIVAS da API e envolvendo os **agentes de IA per-user** do ecossistema.

## Escopos OAuth REAIS (verificado em supabase/functions/social-auth-init/index.ts:152-157)
4 escopos concedidos: youtube.readonly · youtube · youtube.force-ssl · **yt-analytics-monetary.readonly**.
O monetário é SUPERSET: concede também as métricas NÃO-monetárias. Portanto SÃO legíveis: average view duration, engaged views, traffic sources, subscribers gained, impressions/CTR, audience retention.
Requer a "YouTube Analytics API" habilitada no projeto Cloud (a checar) e o usuário ter reconectado concedendo os 4.

## Stack existente (REUSAR, não reconstruir)
- Edge fn **youtube-data** (JWT-gated) já implementa: channel_summary · list_videos · video_metrics (Analytics v2) · video_categories · revenue_metrics · update_video · delete_video. Token per-user resolvido server-side de decrypted_social_accounts + refresh-social-token. Gate de escopo fail-closed → 403 youtube_scope_missing com CTA de reconexão.
- Hooks: src/hooks/useYouTubeStudio.ts (useYouTubeConnection/Channel/Videos/ChannelMetrics/Revenue/UpdateVideo/DeleteVideo) e src/hooks/useYouTubeUpload.ts (upload job store).
- Página: src/pages/YouTubeStudioPage.tsx (589 linhas; header + stats + YouTubeUploadPanel + ChannelMetrics + RevenueCard + VideosTable).
- Mapa exaustivo da API: docs/bok/youtube-studio/11-api-surface-map.md (13 recursos · 175 props · 52 métricas · 33 ações) + youtube-api-registry.json.
- IA per-user: BYOK real (user_api_keys/user_provider_keys, resolveProviderKey), edge fns generate-content (streaming), intent-orchestrate/intent-execute; Constellation = cockpit de agentes per-user; openrouter-swarm. Regra perene: seletor de provider só oferece opções BYOK disponíveis (useConfiguredProviders).
- Medição: creative_metrics (hook_rate, impressions, engagements, revenue_cents) + publication_metrics + collective_efficiency_ledger.
- CAP DURO: 100 edge functions (hoje 99). Uma fn NOVA custa um slot — prefira estender youtube-data com novas ACTIONS a criar fn nova.

## Gaps de medição REAIS (achados por crítica adversarial; o gap de escopo era FALSO POSITIVO)
1. creative_metrics.hook_rate é LIDA em 3 lugares e ESCRITA em ZERO — nenhuma edge fn a escreve.
2. Não há coluna de seguidores/inscritos em creative_metrics nem publication_metrics; creative_metrics.source é CHECK FECHADO ('affiliate_click','organic','postback').
3. Δviews de um vídeo pela Data v3 é CUMULATIVO de todas as fontes ⇒ não-atributivo. A atribuição correta Short→longo vem de **traffic source** do Analytics v2, não de subtração de views.
4. Desde 31/03/2025 "view" de Shorts = play-start sem watch-time mínimo; AVD de Shorts usa denominador de ENGAGED VIEWS. Qualquer conta manual watch-time÷views está errada.

## Regras de honestidade (Lei 1)
- NUNCA exibir métrica que a API não devolve. Se algo não é legível, a UI diz isso explicitamente.
- A camada de IA NÃO pode inventar número. Ela INTERPRETA os números que vieram da API. Toda saída de IA precisa ser rastreável ao dado que a originou.
- Nada de "garante" performance.


# SUA TAREFA
Ângulo FECHAR OS GAPS DE MEDIÇÃO REAIS. Projete o mínimo necessário para: (1) dar um ESCRITOR ao creative_metrics.hook_rate; (2) ter onde gravar inscritos/seguidores ganhos; (3) usar traffic source do Analytics v2 como atribuição Short→longo (em vez de Δviews); (4) tratar o denominador de engaged views. Proponha migration aditiva (com RLS owner-scoped) + qual edge fn escreve. Respeite: cap de 100 fns, /security-review obrigatório em migration, e o padrão de RPC service-role-only do repo.

Seja concreto e ancorado no repo real (cite arquivos). Nada de genérico.

## 🤖 Claude *(02:10:30)*


## 🤖 Claude *(02:10:31)*

I'll ground this in the real schema and edge functions before designing.

## 🤖 Claude *(02:10:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rln \"creative_metrics\" supabase/migrations/ | head -20 && echo \"---PUBMETRICS---\" && grep -rln \"publication_metrics\" supabase/migrations/ | head -20",
  "description": "Find creative_metrics and publication_metrics migrations"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> supabase/migrations/20260626130000_publication_metrics.sql
> supabase/migrations/20260624140000_autopilot_video_enqueue_refund.sql
> supabase/migrations/20260620120100_viral_autopilot_cycles.sql
> supabase/migrations/20260627150000_channel_variants.sql
> supabase/migrations/20260627140000_channel_profiles.sql
> supabase/migrations/20260716120000_cadence_recurrence.sql
> supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql
> supabase/migrations/20260622040000_video_studio_renders_and_assets.sql
> ---PUBMETRICS---
> supabase/migrations/20260626130000_publication_metrics.sql
> ```

## 🤖 Claude *(02:10:33)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"hook_rate\" --include=*.ts --include=*.tsx --include=*.sql -l . 2>/dev/null | grep -v node_modules | head -20",
  "description": "Find hook_rate references"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> src/integrations/supabase/types.ts
> src/lib/revenue-pauta.ts
> src/test/revenue-pauta.test.ts
> src/hooks/useAutopilot.ts
> supabase/migrations/20260627140000_channel_profiles.sql
> supabase/migrations/20260627150000_channel_variants.sql
> ```

## 🤖 Claude *(02:10:35)*


## 🤖 Claude *(02:10:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat supabase/migrations/20260619140000_viral_autopilot_creative_metrics.sql",
  "description": "Read creative_metrics migration"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> -- Migration: viral-autopilot creative_metrics — canonical per-creative performance ledger (FR-VA-009).
> -- BoK SSOT: docs/bok/viral-autopilot/06-data-model.md (creative_metrics) + 04-frd.md (FR-VA-009 unified
> --           3-signal metrics: affiliate_clicks + organic engagement + revenue — Decisão 3 "combo").
> -- SOP: docs/processes/viral-autopilot-product-aware-monetization.md (Lei 2 — written before this code).
> --
> -- WHY a NEW table (not campaign_metrics): public.campaign_metrics ALREADY EXISTS (per-platform telemetry,
> -- consumed by self-optimize / ROIWidget / AnalyticsPage) and is keyed by campaign, NOT by creative. The
> -- viral loop needs metrics keyed by the INDIVIDUAL creative (content_variant_id = content_library.id) so the
> -- future R3 analyzer (FR-VA-010) can rank creative-by-creative and the per-creative attribution (FR-VA-017)
> -- has a home. campaign_metrics is left UNTOUCHED (deprecation is a later concern; no consumer is broken here).
> --
> -- Fatia 1 role: the generator (orchestrate-step, service-role) writes ONE baseline row per creative
> -- (source='organic', zeros) at generation time — this seeds the content_variant_id↔product↔platform key that
> -- the future collector (FR-VA-008) and analyzer (FR-VA-010) build on. The cron/cadence layer is NOT part of
> -- this migration: cycle_id is reserved NULL-able (NO physical FK yet — autopilot_cycles does not exist) so
> -- the cadence Fatia can add the composite tenant-scoped FK later with zero churn here.
> --
> -- Tenancy (mirrors vision_jobs 20260615160000 + lead_core 20260603000000): SELECT-own only; NO write policy
> -- for authenticated → default-deny (the generator writes via the service key, which bypasses RLS). A tenant
> -- can never forge a metric for another tenant nor fabricate revenue. Financial table → RESTRICTIVE no-delete
> -- (clients cannot erase the ledger). Passes /security-review (FMEA-011 / FMEA-VA-001 cross-tenant family).
> 
> CREATE TABLE IF NOT EXISTS public.creative_metrics (
>   id                 uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
>   user_id            uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
>   cycle_id           uuid,                          -- reserved for the cadence Fatia (autopilot_cycles); NO FK yet
>   content_variant_id uuid        NOT NULL,          -- logical ref to content_library.id; NO physical FK (independent
>                                                     -- 18-month retention per Data Model §7 — content can be pruned
>                                                     -- while its performance history is retained for the loop)
>   product_id         text,                          -- = vm_affiliate_products.external_id (the featured product)
>   platform           text,                          -- wordpress | linkedin | twitter
>   source             text        NOT NULL DEFAULT 'organic'
>                        CHECK (source IN ('affiliate_click','organic','postback')),
>   impressions        int         NOT NULL DEFAULT 0 CHECK (impressions      >= 0),
>   engagements        int         NOT NULL DEFAULT 0 CHECK (engagements      >= 0),
>   affiliate_clicks   int         NOT NULL DEFAULT 0 CHECK (affiliate_clicks >= 0),
>   revenue_cents      int         NOT NULL DEFAULT 0 CHECK (revenue_cents    >= 0),
>   collected_at       timestamptz NOT NULL DEFAULT now(),
>   created_at         timestamptz NOT NULL DEFAULT now(),
>   -- One row per (creative, signal source): the baseline 'organic' row at generation, later upserted by the
>   -- collector; 'affiliate_click' and 'postback' rows are written by their own writers (click ledger / postback).
>   CONSTRAINT creative_metrics_variant_source_uniq UNIQUE (content_variant_id, source)
> );
> 
> ALTER TABLE public.creative_metrics ENABLE ROW LEVEL SECURITY;
> 
> -- SELECT own only. No INSERT/UPDATE policy → authenticated default-deny; the generator/collector write via the
> -- service key. A tenant reads its own creative performance (future dashboard FR-VA-015) and nothing else.
> CREATE POLICY "creative_metrics_select_own" ON public.creative_metrics
>   FOR SELECT USING (auth.uid() = user_id);
> 
> -- Financial ledger → clients can NEVER delete a metric row (RESTRICTIVE forbids it even if a future permissive
> -- policy is added). Mirrors the RESTRICTIVE pattern on financial/affiliate tables.
> CREATE POLICY "creative_metrics_no_client_delete" ON public.creative_metrics
>   AS RESTRICTIVE FOR DELETE USING (false);
> 
> CREATE INDEX IF NOT EXISTS creative_metrics_variant_idx  ON public.creative_metrics (content_variant_id);
> CREATE INDEX IF NOT EXISTS creative_metrics_user_idx     ON public.creative_metrics (user_id, collected_at DESC);
> CREATE INDEX IF NOT EXISTS creative_metrics_cycle_idx    ON public.creative_metrics (cycle_id);
> CREATE INDEX IF NOT EXISTS creative_metrics_product_idx  ON public.creative_metrics (product_id);
> 
> COMMENT ON TABLE public.creative_metrics IS
>   'Viral Autopilot canonical per-creative metrics ledger (FR-VA-009), keyed by content_variant_id '
>   '(= content_library.id). Unifies 3 signals (affiliate_click/organic/postback — Decisão 3). SELECT-own RLS, '
>   'service-role write (default-deny), RESTRICTIVE no client delete. Generator writes a baseline row at '
>   'generation; collector/analyzer (R3) build on it. SOP viral-autopilot-product-aware-monetization.md.';
> ```

## 🤖 Claude *(02:10:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat supabase/migrations/20260626130000_publication_metrics.sql",
  "description": "Read publication_metrics migration"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> -- Migration: publication_metrics — per-publication social outcome (time-series) + creative↔post link fix.
> -- BoK SSOT: docs/bok/viral-autopilot/06-data-model.md (Amendment v0.3) + 05-sdd.md (Amendment v0.3). FR-VA-027.
> -- SOP (Lei 2): docs/processes/publication-metrics-collection.md. Doctrine: agentic-vision.md (OTD-AG-002 sensory loop).
> --
> -- WHY: the Learning & Adaptation loop learns on a BLANK scoreboard — creative_metrics impressions/engagements are
> -- always 0 because nothing pulls the real social outcome back. This table is the sensory nerve: one TIME-SERIES
> -- snapshot per (creative, platform, snapshot_at) of the real engagement a published post earned (views/likes/
> -- comments/shares/reposts/saves/reach/impressions). Separate table (not enrich creative_metrics) because metrics
> -- GROW over days (snapshot_at) and creative_metrics is a single-snapshot affiliate-centric schema (OTD-VA-015).
> --
> -- SECURITY (mirrors creative_metrics / autopilot_cycles):
> --   * SELECT-own RLS (auth.uid() = user_id) → per-tenant; a tenant sees only their own posts' metrics.
> --   * INSERT/UPDATE have NO permissive policy → authenticated default-deny; only the service-role collector writes.
> --   * RESTRICTIVE no-delete (outcome ledger; clients can never delete a metric row).
> --   * LGPD: only numeric aggregates of the tenant's OWN posts — no PII of third parties who engaged.
> -- The collector NEVER fabricates: a platform that returns no number gets a 'skipped' telemetry event, not a row
> -- here (Lei 1 — SOP §2). Passes /security-review before commit (FMEA-011).
> 
> CREATE TABLE IF NOT EXISTS public.publication_metrics (
>   id                 uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
>   user_id            uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
>   content_variant_id uuid        REFERENCES public.content_library(id) ON DELETE CASCADE,  -- = the creative
>   platform           text        NOT NULL,            -- instagram | facebook | linkedin | youtube | tiktok
>   external_post_id   text,                             -- IG media id / urn:li:share / yt video id / ...
>   views        int NOT NULL DEFAULT 0 CHECK (views       >= 0),
>   likes        int NOT NULL DEFAULT 0 CHECK (likes       >= 0),
>   comments     int NOT NULL DEFAULT 0 CHECK (comments    >= 0),
>   shares       int NOT NULL DEFAULT 0 CHECK (shares      >= 0),
>   reposts      int NOT NULL DEFAULT 0 CHECK (reposts     >= 0),
>   saves        int NOT NULL DEFAULT 0 CHECK (saves       >= 0),
>   reach        int NOT NULL DEFAULT 0 CHECK (reach       >= 0),
>   impressions  int NOT NULL DEFAULT 0 CHECK (impressions >= 0),
>   snapshot_at        timestamptz NOT NULL,             -- the measurement window (metric grows over time)
>   collected_at       timestamptz NOT NULL DEFAULT now(),
>   CONSTRAINT publication_metrics_snapshot_uniq UNIQUE (content_variant_id, platform, snapshot_at)
> );
> 
> ALTER TABLE public.publication_metrics ENABLE ROW LEVEL SECURITY;
> 
> -- SELECT own only; INSERT/UPDATE default-deny (the service-role collector writes). Outcome ledger → RESTRICTIVE no-delete.
> CREATE POLICY "publication_metrics_select_own" ON public.publication_metrics
>   FOR SELECT USING (auth.uid() = user_id);
> CREATE POLICY "publication_metrics_no_client_delete" ON public.publication_metrics
>   AS RESTRICTIVE FOR DELETE USING (false);
> 
> -- Time-series read path for the per-publication panel + the analyze JOIN.
> CREATE INDEX IF NOT EXISTS publication_metrics_variant_idx
>   ON public.publication_metrics (content_variant_id, platform, snapshot_at DESC);
> CREATE INDEX IF NOT EXISTS publication_metrics_user_idx
>   ON public.publication_metrics (user_id, snapshot_at DESC);
> 
> COMMENT ON TABLE public.publication_metrics IS
>   'Per-publication social outcome, TIME-SERIES (FR-VA-027). One snapshot per (creative, platform, snapshot_at). '
>   'SELECT-own, service-role write (default-deny), RESTRICTIVE no client delete. Collector never fabricates (Lei 1 — '
>   'SOP publication-metrics-collection.md). Feeds the multi-metric reward R() in autopilot-analyze (FR-VA-029).';
> 
> -- ── Link fix: creative ↔ published post (06-data-model §v0.3) ───────────────────────────────────────────────
> -- scheduled_posts.content_id already links the publish-social path → content_library; add the reverse index.
> CREATE INDEX IF NOT EXISTS scheduled_posts_platform_post_id_idx
>   ON public.scheduled_posts (platform_post_id);
> 
> -- meta_posts had NO creative link (only campaign_id) → add content_id so Meta posts trace back to the creative.
> ALTER TABLE public.meta_posts
>   ADD COLUMN IF NOT EXISTS content_id uuid REFERENCES public.content_library(id) ON DELETE SET NULL;
> ```

## 🤖 Claude *(02:10:40)*


## 🤖 Claude *(02:10:41)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"hook_rate\" supabase/migrations/20260627140000_channel_profiles.sql supabase/migrations/20260627150000_channel_variants.sql src/lib/revenue-pauta.ts src/hooks/useAutopilot.ts",
  "description": "Show hook_rate definition and readers"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> src/hooks/useAutopilot.ts:126:          .select('content_variant_id, impressions, engagements, hook_rate, affiliate_clicks, revenue_cents, platform, product_id, collected_at')
> src/lib/revenue-pauta.ts:10:  hook_rate: number | null;
> src/lib/revenue-pauta.ts:84:    if (m.hook_rate != null) entry.hookRate = Math.max(entry.hookRate ?? 0, m.hook_rate);
> supabase/migrations/20260627140000_channel_profiles.sql:249:--    with service='reshape-<channel>'; creative_metrics gains hook_rate in a later slice (FR-CP-011).
> supabase/migrations/20260627150000_channel_variants.sql:1:-- Migration: channel_variants ledger + creative_metrics.hook_rate — Reshaper (FR-CP-003 / FR-CP-007 / FR-CP-011)
> supabase/migrations/20260627150000_channel_variants.sql:7:-- content_variant_id that creative_metrics keys on (FR-CP-011 hook_rate added here too).
> supabase/migrations/20260627150000_channel_variants.sql:66:-- 2. creative_metrics.hook_rate — FR-CP-011 (watch-past-3s ÷ impressions). Additive, nullable.
> supabase/migrations/20260627150000_channel_variants.sql:69:  ADD COLUMN IF NOT EXISTS hook_rate numeric
> supabase/migrations/20260627150000_channel_variants.sql:70:    CONSTRAINT creative_metrics_hook_rate_chk CHECK (hook_rate IS NULL OR (hook_rate >= 0 AND hook_rate <= 1));
> ```

## 🤖 Claude *(02:10:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls supabase/functions/ | tr '\\n' ' '; echo; echo \"COUNT: $(ls supabase/functions/ | grep -v '^_' | wc -l)\"",
  "description": "List edge functions and count"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> admin-manage-user aeo-audit agent-task-execute aios-chat aios-chat-gateway aios-chat-stream aios-live-proxy aios-sql-bridge analyze-node analyze-sem analyze-seo autopilot-analyze autopilot-cadence-cron autopilot-collect autopilot-run auto-publish avatar-consent avatar-identity-train award-mco-coins cadence-plan cadence-run campaign-run canvas-execute check-post-existence check-subscription check-video-status collect-publication-metrics connect-instagram-token create-checkout create-portal data-export delete-account delete-remote-post design-job-enqueue detect-viral-moments discover-products embed-mcorch-node erase-avatar-artifacts fetch-trends generate-audio-script generate-carousel generate-content generate-image generate-script-package generate-video generate-video-script generate-voice get-infra-status handle-ml-postback higgsfield-oauth-callback higgsfield-oauth-init higgsfield-webhook ingest-external-asset instagram-webhook intent-execute intent-orchestrate lead-score list-provider-models meta-privacy nurture-cron nurture-dispatch openrouter-swarm optimize-schedule orchestrate-content orchestrate-step pinterest-boards process-affiliate-link publish-channel-variant publish-meta publish-social publish-space-asset publish-space-carousel publish-wordpress refresh-social-token rescue-video reshape-pillar search-constellation seed-global-app-creds self-heal self-optimize _shared social-auth-callback social-auth-init stripe-webhook submit-lead-webhook sync-knowledge-mesh sync-meta-ads test-api-key tiktok-login-callback tiktok-login-init tiktok-login-session trigger-embeddings trigger-ingest tts-speak veo-poll video-render video-repurpose-run whatsapp-templates whatsapp-webhook youtube-data 
> COUNT: 99
> ```

## 🤖 Claude *(02:10:45)*


## 🤖 Claude *(02:10:46)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l supabase/functions/collect-publication-metrics/index.ts; grep -n \"youtube\\|platform\\|snapshot_at\\|upsert\\|hook_rate\\|analytics\" supabase/functions/collect-publication-metrics/index.ts | head -60",
  "description": "Inspect collect-publication-metrics"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 112 supabase/functions/collect-publication-metrics/index.ts
> 3:// a TIME-SERIES snapshot into publication_metrics. FAIL-SOFT per platform — NEVER fabricates (Lei 1):
> 19:type Post = { user_id: string; platform: string; external_post_id: string; content_variant_id: string | null };
> 35:  // snapshot_at = today @ 00:00 UTC → daily granularity; same-day re-runs UPSERT the row (UNIQUE constraint).
> 42:    .select("user_id, platform, platform_post_id, content_id")
> 43:    .eq("status", "published").not("platform_post_id", "is", null).not("content_id", "is", null);
> 47:    posts.push({ user_id: r.user_id, platform: r.platform, external_post_id: r.platform_post_id, content_variant_id: r.content_id });
> 50:    .select("user_id, platform, meta_post_id, content_id")
> 55:    posts.push({ user_id: r.user_id, platform: r.platform, external_post_id: r.meta_post_id, content_variant_id: r.content_id });
> 57:  // Token cache per (user, platform) — one decrypted lookup each.
> 59:  const resolveToken = async (userId: string, platform: string): Promise<string | null> => {
> 60:    const key = `${userId}:${platform}`;
> 63:      .eq("user_id", userId).eq("platform", platform).eq("is_active", true).limit(1).maybeSingle();
> 75:    if (!post.content_variant_id) { bump(post.platform, "skipped"); continue; }
> 77:    // ── Instagram: real media insights (the platform that lights up after the insights-scope re-OAuth). ──────
> 78:    if (post.platform === "instagram") {
> 88:        await admin.from("publication_metrics").upsert({
> 89:          user_id: post.user_id, content_variant_id: post.content_variant_id, platform: "instagram",
> 93:          snapshot_at: snapshotAt,
> 94:        }, { onConflict: "content_variant_id,platform,snapshot_at" });
> 101:    bump(post.platform, "skipped");
> 104:  // Telemetry — NO PII (allowlist counts only). Honest record of what was pulled vs skipped per platform.
> 108:    event: "collect_summary", metadata: { posts: posts.length, pulled: totalPulled, by_platform: summary, scope: scopeUserId ? "user" : "all" },
> 111:  return json({ ok: true, posts: posts.length, pulled: totalPulled, by_platform: summary, snapshot_at: snapshotAt });
> ```

## 🤖 Claude *(02:10:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"action\\|metrics\\|dimensions\\|startDate\\|ids=\\|youtubeAnalytics\\|reports\" supabase/functions/youtube-data/index.ts | head -80; echo \"---\"; wc -l supabase/functions/youtube-data/index.ts",
  "description": "Inspect youtube-data actions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 9:// Actions: channel_summary | list_videos | video_metrics | video_categories
> 10://          revenue_metrics (force: yt-analytics-monetary.readonly) | update_video · delete_video (force: youtube.force-ssl)
> 11:// Fatia 2 (Amendment 12): write ops (edit/delete the user's own videos) + monetary reports — each maps to a
> 82:      action: quota
> 114:    const action: string = body.action;
> 115:    if (!action) return json({ error: "action required" }, 400);
> 132:        { error: "youtube_not_connected", action: "Conecte seu canal do YouTube em /dashboard/social" },
> 137:    // Fail-closed scope gate (G2): read actions need youtube.readonly; metrics need yt-analytics.readonly.
> 138:    // Detecting the gap here (not letting Google 403) gives a clean, actionable reconnect CTA.
> 141:    if (action === "channel_summary" || action === "list_videos" || action === "video_categories") {
> 144:    // Non-monetary metrics accept EITHER analytics scope (monetary is a superset that also grants them).
> 146:    if (action === "video_metrics" && !hasAnalytics) {
> 149:    if (action === "revenue_metrics" && !scopes.includes(SCOPE_ANALYTICS_MONETARY)) {
> 152:    if ((action === "update_video" || action === "delete_video") && !scopes.includes(SCOPE_FORCE_SSL)) {
> 160:          action: "Reconecte o YouTube com permissões ampliadas (Redes Sociais → YouTube → Reconectar).",
> 169:      return json({ error: "youtube_token_unavailable", action: "Reconecte o YouTube." }, 401);
> 198:    if (action === "channel_summary") {
> 226:    if (action === "video_categories") {
> 233:    if (action === "list_videos") {
> 264:    if (action === "video_metrics") {
> 266:      const startDate = typeof body.startDate === "string" ? body.startDate : isoDate(28);
> 267:      const metrics =
> 268:        typeof body.metrics === "string" && body.metrics.trim()
> 269:          ? body.metrics
> 271:      const params = new URLSearchParams({ ids: "channel==MINE", startDate, endDate, metrics });
> 272:      if (typeof body.dimensions === "string" && body.dimensions) params.set("dimensions", body.dimensions);
> 276:      const r = await gfetch(`${YT_ANALYTICS}/reports?${params.toString()}`);
> 282:    // ── Fatia 2 — monetary reports (force: yt-analytics-monetary.readonly) ──
> 283:    if (action === "revenue_metrics") {
> 285:      const startDate = typeof body.startDate === "string" ? body.startDate : isoDate(28);
> 286:      const metrics =
> 287:        typeof body.metrics === "string" && body.metrics.trim()
> 288:          ? body.metrics
> 290:      const params = new URLSearchParams({ ids: "channel==MINE", startDate, endDate, metrics, currency: "USD" });
> 291:      const r = await gfetch(`${YT_ANALYTICS}/reports?${params.toString()}`);
> 293:        // A non-partner / non-monetized channel returns 403 for monetary metrics. That is NOT an app failure —
> 307:    if (action === "update_video") {
> 333:    if (action === "delete_video") {
> 355:    return json({ error: "unknown_action" }, 400);
> ---
> 361 supabase/functions/youtube-data/index.ts
> ```

## 🤖 Claude *(02:10:50)*


## 🤖 Claude *(02:10:50)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/youtube-data/index.ts",
  "offset": 255,
  "limit": 55
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 255	          `${YT_DATA}/videos?part=snippet,contentDetails,status,statistics&id=${ids.join(",")}&maxResults=50`,
> 256	        );
> 257	        if (!vids.ok) return googleError(vids, pulse);
> 258	        videos = vids.data.items ?? [];
> 259	      }
> 260	      pulse("healthy");
> 261	      return json({ videos, nextPageToken: items.data.nextPageToken ?? null, uploadsPlaylistId: uploads });
> 262	    }
> 263	
> 264	    if (action === "video_metrics") {
> 265	      const endDate = typeof body.endDate === "string" ? body.endDate : isoDate(1);
> 266	      const startDate = typeof body.startDate === "string" ? body.startDate : isoDate(28);
> 267	      const metrics =
> 268	        typeof body.metrics === "string" && body.metrics.trim()
> 269	          ? body.metrics
> 270	          : "views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,likes,comments,shares,subscribersGained,subscribersLost";
> 271	      const params = new URLSearchParams({ ids: "channel==MINE", startDate, endDate, metrics });
> 272	      if (typeof body.dimensions === "string" && body.dimensions) params.set("dimensions", body.dimensions);
> 273	      if (typeof body.videoId === "string" && body.videoId) params.set("filters", `video==${body.videoId}`);
> 274	      if (typeof body.sort === "string" && body.sort) params.set("sort", body.sort);
> 275	      if (typeof body.maxResults === "number") params.set("maxResults", String(body.maxResults));
> 276	      const r = await gfetch(`${YT_ANALYTICS}/reports?${params.toString()}`);
> 277	      if (!r.ok) return googleError(r, pulse);
> 278	      pulse("healthy");
> 279	      return json({ columnHeaders: r.data.columnHeaders ?? [], rows: r.data.rows ?? [] });
> 280	    }
> 281	
> 282	    // ── Fatia 2 — monetary reports (force: yt-analytics-monetary.readonly) ──
> 283	    if (action === "revenue_metrics") {
> 284	      const endDate = typeof body.endDate === "string" ? body.endDate : isoDate(1);
> 285	      const startDate = typeof body.startDate === "string" ? body.startDate : isoDate(28);
> 286	      const metrics =
> 287	        typeof body.metrics === "string" && body.metrics.trim()
> 288	          ? body.metrics
> 289	          : "estimatedRevenue,estimatedAdRevenue,grossRevenue,cpm,monetizedPlaybacks,adImpressions";
> 290	      const params = new URLSearchParams({ ids: "channel==MINE", startDate, endDate, metrics, currency: "USD" });
> 291	      const r = await gfetch(`${YT_ANALYTICS}/reports?${params.toString()}`);
> 292	      if (!r.ok) {
> 293	        // A non-partner / non-monetized channel returns 403 for monetary metrics. That is NOT an app failure —
> 294	        // the CALL itself demonstrates the scope. Return a clean, monetized:false state (never a crash).
> 295	        if (r.status === 403) {
> 296	          pulse("healthy");
> 297	          const reason = r.data?.error?.errors?.[0]?.reason ?? r.data?.error?.status ?? "not_monetized";
> 298	          return json({ columnHeaders: [], rows: [], monetized: false, reason });
> 299	        }
> 300	        return googleError(r, pulse);
> 301	      }
> 302	      pulse("healthy");
> 303	      return json({ columnHeaders: r.data.columnHeaders ?? [], rows: r.data.rows ?? [], monetized: true });
> 304	    }
> 305	
> 306	    // ── Fatia 2 — edit the user's own video (force: youtube.force-ssl) ──
> 307	    if (action === "update_video") {
> 308	      const videoId = typeof body.videoId === "string" ? body.videoId : "";
> 309	      if (!videoId) return json({ error: "videoId required" }, 400);
> ```

## 🤖 Claude *(02:10:52)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"collect-publication-metrics\" --include=*.toml --include=*.sql --include=*.sh --include=*.ts . 2>/dev/null | grep -v node_modules | grep -v \"functions/collect-publication-metrics\" | head -20",
  "description": "Find how collector is invoked (cron?)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> supabase/config.toml:46:[functions.collect-publication-metrics]
> ```

## 🤖 Claude *(02:10:55)*


## 🤖 Claude *(02:10:57)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '40,60p' supabase/config.toml; echo \"=== youtube_uploads ===\"; grep -n \"CREATE TABLE\\|^  [a-z_]* \\|video_id\\|content_\\|POLICY\" supabase/migrations/20260719170000_youtube_uploads.sql | head -50",
  "description": "Check config.toml and youtube_uploads schema"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [functions.cadence-run]
> verify_jwt = false
> [functions.autopilot-analyze]
> verify_jwt = false
> [functions.autopilot-collect]
> verify_jwt = false
> [functions.collect-publication-metrics]
> verify_jwt = false
> [functions.video-render]
> verify_jwt = false
> [functions.intent-orchestrate]
> verify_jwt = false
> [functions.intent-execute]
> verify_jwt = false
> [functions.aeo-audit]
> verify_jwt = false
> [functions.generate-content]
> verify_jwt = false
> [functions.generate-audio-script]
> verify_jwt = false
> [functions.generate-video-script]
> === youtube_uploads ===
> 9:--   • O CLIENTE insere o próprio job via RLS owner (auth.uid()=user_id, state='queued', sem video_id) — não há
> 21:CREATE TABLE IF NOT EXISTS public.youtube_uploads (
> 22:  id               uuid        PRIMARY KEY DEFAULT gen_random_uuid(),   -- = job_id (poll-able)
> 23:  user_id          uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 24:  source_key       text        NOT NULL,                                -- master no inbox do host: <uid>/<arquivo>
> 25:  snippet          jsonb       NOT NULL DEFAULT '{}'::jsonb,            -- {title,description,tags[],categoryId,defaultLanguage,defaultAudioLanguage}
> 26:  status_opts      jsonb       NOT NULL DEFAULT '{}'::jsonb,            -- {privacyStatus,publishAt,selfDeclaredMadeForKids,notifySubscribers,license,embeddable}
> 27:  localizations    jsonb,                                               -- {<lang>:{title,description}} (vantagem API — FR-YT-030)
> 28:  thumbnail_key    text,                                                -- imagem custom no inbox do host (opcional, force-ssl)
> 29:  caption_key      text,                                                -- SRT no inbox do host (opcional, force-ssl)
> 30:  playlist_id      text,                                                -- playlist de destino (opcional)
> 31:  state            text        NOT NULL DEFAULT 'queued'
> 32:                     CHECK (state IN ('queued','running','done','failed')),
> 33:  youtube_video_id text,                                                -- id retornado pelo videos.insert (prova Lei 1)
> 34:  session_uri      text,                                                -- resumable session URI (retomada pós-restart)
> 35:  bytes_sent       bigint      NOT NULL DEFAULT 0 CHECK (bytes_sent >= 0),
> 36:  progress         int         NOT NULL DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
> 37:  attempts         int         NOT NULL DEFAULT 0 CHECK (attempts >= 0),
> 38:  warnings         jsonb       NOT NULL DEFAULT '[]'::jsonb,            -- extras fail-soft (thumbnail/caption/playlist)
> 39:  error            text,
> 40:  node_id          uuid,                                                -- mesh observation (Mesh Mandate); lógico → mcorch_nodes.id
> 41:  expires_at       timestamptz NOT NULL DEFAULT (now() + interval '7 days'),
> 42:  created_at       timestamptz NOT NULL DEFAULT now(),
> 43:  updated_at       timestamptz NOT NULL DEFAULT now(),
> 53:CREATE POLICY "youtube_uploads_select_own" ON public.youtube_uploads
> 57:CREATE POLICY "youtube_uploads_insert_own" ON public.youtube_uploads
> 59:    auth.uid() = user_id
> 60:    AND state = 'queued'
> 61:    AND youtube_video_id IS NULL
> 62:    AND session_uri IS NULL
> 66:CREATE POLICY "youtube_uploads_delete_own" ON public.youtube_uploads
> 69:-- SEM policy de UPDATE p/ authenticated ⇒ default-deny: só o worker (service-role) muda state/progress/video_id.
> 96:  v_row public.youtube_uploads;
> 99:     SET state    = 'running',
> 100:         attempts = attempts + 1
> 101:   WHERE id = p_job_id
> 102:     AND state = 'queued'
> 103:   RETURNING * INTO v_row;
> 106:    RETURN jsonb_build_object('claimed', false);
> 118:--    Guard state IN (queued,running) ⇒ o primeiro finalizador vence, idempotente (sem money — só estado/video_id).
> 121:  p_job_id   uuid,
> 122:  p_state    text,      -- 'done' | 'failed'
> 123:  p_video_id text,      -- set on done
> 124:  p_error    text,      -- set on failed
> 125:  p_warnings jsonb,     -- NULL keeps existing (extras fail-soft)
> 126:  p_node_id  uuid       -- NULL keeps existing (mesh observation)
> 134:  v_uid uuid;
> 137:    RAISE EXCEPTION 'finalize_youtube_upload: terminal state required, got %', p_state USING errcode = '22023';
> 141:     SET state            = p_state,
> 142:         youtube_video_id = COALESCE(p_video_id, youtube_video_id),
> ```

## 🤖 Claude *(02:10:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"collect-publication-metrics\\|publication_metrics\\|cron.schedule\" supabase/functions/autopilot-collect/index.ts 2>/dev/null | head; echo \"=== cron jobs ===\"; grep -rn \"cron.schedule\" supabase/migrations/*.sql | grep -io \"cron.schedule([^,]*,[^,]*\" | head -20",
  "description": "Check cron scheduling"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === cron jobs ===
> ```

## 🤖 Claude *(02:11:46)*


## 🤖 Claude *(02:11:48)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/youtube-data/index.ts",
  "offset": 130,
  "limit": 40
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 130	    if (!account) {
> 131	      return json(
> 132	        { error: "youtube_not_connected", action: "Conecte seu canal do YouTube em /dashboard/social" },
> 133	        409,
> 134	      );
> 135	    }
> 136	
> 137	    // Fail-closed scope gate (G2): read actions need youtube.readonly; metrics need yt-analytics.readonly.
> 138	    // Detecting the gap here (not letting Google 403) gives a clean, actionable reconnect CTA.
> 139	    const scopes: string[] = (account.scopes as string[] | null) ?? [];
> 140	    const missing: string[] = [];
> 141	    if (action === "channel_summary" || action === "list_videos" || action === "video_categories") {
> 142	      if (!scopes.includes(SCOPE_READONLY)) missing.push(SCOPE_READONLY);
> 143	    }
> 144	    // Non-monetary metrics accept EITHER analytics scope (monetary is a superset that also grants them).
> 145	    const hasAnalytics = scopes.includes(SCOPE_ANALYTICS) || scopes.includes(SCOPE_ANALYTICS_MONETARY);
> 146	    if (action === "video_metrics" && !hasAnalytics) {
> 147	      missing.push(SCOPE_ANALYTICS);
> 148	    }
> 149	    if (action === "revenue_metrics" && !scopes.includes(SCOPE_ANALYTICS_MONETARY)) {
> 150	      missing.push(SCOPE_ANALYTICS_MONETARY);
> 151	    }
> 152	    if ((action === "update_video" || action === "delete_video") && !scopes.includes(SCOPE_FORCE_SSL)) {
> 153	      missing.push(SCOPE_FORCE_SSL);
> 154	    }
> 155	    if (missing.length) {
> 156	      return json(
> 157	        {
> 158	          error: "youtube_scope_missing",
> 159	          missing,
> 160	          action: "Reconecte o YouTube com permissões ampliadas (Redes Sociais → YouTube → Reconectar).",
> 161	        },
> 162	        403,
> 163	      );
> 164	    }
> 165	
> 166	    const token = await ensureFreshToken(admin, account, supabaseUrl, serviceKey);
> 167	    if (!token) {
> 168	      pulse("degraded");
> 169	      return json({ error: "youtube_token_unavailable", action: "Reconecte o YouTube." }, 401);
> ```

## 🤖 Claude *(02:11:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '25,45p;70,100p' supabase/functions/collect-publication-metrics/index.ts",
  "description": "Read collector core"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>   if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 
>   // Service-role gate (in-function — verify_jwt=false at the gateway; the cron/admin presents the secret key).
>   const auth = req.headers.get("Authorization") ?? "";
>   if (auth !== `Bearer ${SERVICE_KEY}`) return json({ error: "unauthorized" }, 401);
> 
>   const admin = createClient(SUPABASE_URL, SERVICE_KEY);
>   const body = await req.json().catch(() => ({}));
>   const scopeUserId: string | null = typeof body.user_id === "string" ? body.user_id : null;
> 
>   // snapshot_at = today @ 00:00 UTC → daily granularity; same-day re-runs UPSERT the row (UNIQUE constraint).
>   const now = new Date();
>   const snapshotAt = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate())).toISOString();
> 
>   // ── Enumerate the published posts to measure (the link creative↔post — 06-data-model §v0.3) ──────────────
>   const posts: Post[] = [];
>   let sp = admin.from("scheduled_posts")
>     .select("user_id, platform, platform_post_id, content_id")
>     .eq("status", "published").not("platform_post_id", "is", null).not("content_id", "is", null);
>   if (scopeUserId) sp = sp.eq("user_id", scopeUserId);
>   const { data: spRows } = await sp.limit(500);
>   const bump = (p: string, k: "pulled" | "skipped") => {
>     summary[p] ??= { pulled: 0, skipped: 0 }; summary[p][k]++;
>   };
> 
>   for (const post of posts) {
>     if (!post.content_variant_id) { bump(post.platform, "skipped"); continue; }
> 
>     // ── Instagram: real media insights (the platform that lights up after the insights-scope re-OAuth). ──────
>     if (post.platform === "instagram") {
>       const token = await resolveToken(post.user_id, "instagram");
>       if (!token) { bump("instagram", "skipped"); continue; }
>       try {
>         const url = `${IG_BASE}/${post.external_post_id}/insights?metric=likes,comments,shares,saved,reach,views&access_token=${token}`;
>         const res = await fetch(url);
>         const j = await res.json().catch(() => ({}));
>         if (!res.ok || !Array.isArray(j.data)) { bump("instagram", "skipped"); continue; }  // no insights scope → skip, NO fabrication
>         const m: Record<string, number> = {};
>         for (const item of j.data) m[item.name] = Number(item.values?.[0]?.value ?? 0);
>         await admin.from("publication_metrics").upsert({
>           user_id: post.user_id, content_variant_id: post.content_variant_id, platform: "instagram",
>           external_post_id: post.external_post_id,
>           views: m.views ?? 0, likes: m.likes ?? 0, comments: m.comments ?? 0,
>           shares: m.shares ?? 0, saves: m.saved ?? 0, reach: m.reach ?? 0, impressions: m.views ?? 0,
>           snapshot_at: snapshotAt,
>         }, { onConflict: "content_variant_id,platform,snapshot_at" });
>         bump("instagram", "pulled");
>       } catch { bump("instagram", "skipped"); }
>       continue;
>     }
> 
>     // ── Facebook Page / LinkedIn personal: no reliable public per-post metric in v1 → honest skip (no row). ──
> ```

## 🤖 Claude *(02:12:35)*


## 🤖 Claude *(02:12:35)*

Tenho o quadro real. Vou consolidar.

## 🤖 Claude *(02:15:10)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "title": "Fechar os 4 gaps de medi\u00e7\u00e3o do YouTube Studio \u2014 spine `youtube_video_metrics` + `youtube_traffic_sources`, RPC service-role-only e um escritor real para `hook_rate` (zero fn nova)",
  "summary": "Os 4 gaps s\u00e3o reais e verificados no repo. `creative_metrics.hook_rate` (adicionada em `supabase/migrations/20260627150000_channel_variants.sql:69`) \u00e9 lida em `src/lib/revenue-pauta.ts:84` e `src/hooks/useAutopilot.ts:126` e escrita em lugar nenhum. N\u00e3o existe coluna de inscritos em `creative_metrics` (`20260619140000`) nem em `publication_metrics` (`20260626130000`). O \u00fanico coletor real, `supabase/functions/collect-publication-metrics/index.ts`, cobre APENAS Instagram (linhas 78-99) e faz `skipped` honesto no resto (linha 101) \u2014 YouTube nunca entra.\n\nH\u00e1 um QUINTO gap que ningu\u00e9m listou e que invalida os outros quatro se n\u00e3o for fechado primeiro: **n\u00e3o existe identidade dos v\u00eddeos do canal na spine de m\u00e9tricas**. `publication_metrics` \u00e9 chaveada por `content_variant_id` (FK \u2192 `content_library`), e os 50+ v\u00eddeos do canal foram publicados fora da plataforma \u2014 n\u00e3o t\u00eam linha em `content_library`. Pior: `supabase/migrations/20260719170000_youtube_uploads.sql` N\u00c3O tem `content_variant_id`, ent\u00e3o nem o que sobe pela Upload Factory chega ao ledger. For\u00e7ar YouTube dentro de `publication_metrics` produziria linhas com `content_variant_id IS NULL` \u2014 e como NULL n\u00e3o dedupa em UNIQUE no Postgres, a constraint `publication_metrics_snapshot_uniq` deixaria de deduplicar e o coletor duplicaria a cada execu\u00e7\u00e3o.\n\nDa\u00ed o desenho: uma tabela nova chaveada pelo `video_id` do YouTube (a chave que a Analytics v2 realmente usa), uma tabela de traffic source que substitui o \u0394views n\u00e3o-atributivo, e um \u00fanico RPC service-role-only que grava o bruto e deriva o `hook_rate` na MESMA transa\u00e7\u00e3o \u2014 de forma que um `hook_rate` nunca possa existir sem a linha bruta que o originou.\n\nSobre o `hook_rate`: a defini\u00e7\u00e3o de FR-CP-011 (\"watch-past-3s \u00f7 impressions\") **n\u00e3o \u00e9 obten\u00edvel da API do YouTube** \u2014 n\u00e3o existe m\u00e9trica de 3 segundos na Analytics v2. Existem duas f\u00f3rmulas honestas e elas s\u00e3o DIFERENTES entre si (Shorts vs longo), o que torna a coluna `numeric` isolada uma mentira por omiss\u00e3o. Por isso o desenho adiciona `hook_rate_basis` e o RPC recusa gravar `hook_rate` sem ela.",
  "decisions": [
    "GAP-0 (pr\u00e9-requisito, n\u00e3o listado no briefing): a spine de m\u00e9tricas n\u00e3o consegue representar um v\u00eddeo do canal. `publication_metrics.content_variant_id` \u00e9 FK \u2192 `content_library` e os 50+ v\u00eddeos existentes n\u00e3o est\u00e3o l\u00e1. Decis\u00e3o: tabela nova chaveada por `(user_id, video_id text, snapshot_at)` \u2014 o `video_id` do YouTube \u00e9 a chave natural da Analytics v2 \u2014 com `content_variant_id` NULLABLE como ponte quando o v\u00eddeo nasceu no ecossistema. N\u00c3O empurrar YouTube para dentro de `publication_metrics`: linhas com `content_variant_id IS NULL` quebram a dedup de `publication_metrics_snapshot_uniq` (NULLs s\u00e3o distintos em UNIQUE no Postgres) e o coletor duplicaria diariamente.",
    "GAP-1 (escritor do hook_rate): o escritor \u00e9 o RPC `record_youtube_video_snapshot`, chamado pelo ramo `youtube` novo do `collect-publication-metrics`. Mas a defini\u00e7\u00e3o de FR-CP-011 (`watch-past-3s \u00f7 impressions`) \u00e9 INEXEQU\u00cdVEL \u2014 a Analytics v2 n\u00e3o exp\u00f5e nenhuma m\u00e9trica de 3s. Duas f\u00f3rmulas honestas e distintas: (a) Shorts \u2192 `engagedViews / views`, que \u00e9 literalmente a defini\u00e7\u00e3o do YouTube p\u00f3s-31/03/2025 (view = play-start; engaged view = passou do limiar) \u21d2 \u00e9 o hook rate nativo, n\u00e3o uma aproxima\u00e7\u00e3o; (b) longo \u2192 `audienceWatchRatio` no bucket de `elapsedVideoTimeRatio` mais pr\u00f3ximo de `3 / duration_seconds` (relat\u00f3rio de reten\u00e7\u00e3o de audi\u00eancia). Como as duas produzem n\u00fameros n\u00e3o-compar\u00e1veis entre si, gravar s\u00f3 o `numeric` \u00e9 desonesto.",
    "Consequ\u00eancia direta: `creative_metrics` ganha `hook_rate_basis text` (CHECK fechado em `engaged_views_ratio` | `retention_at_3s` | `ig_plays_ratio`) e `hook_rate_source_ref text` (ex.: `youtube_video_metrics:<uuid>`). O RPC RAISE EXCEPTION se `p_hook_rate IS NOT NULL AND p_hook_rate_basis IS NULL` \u2014 \u00e9 o gate central que impede um n\u00famero sem proced\u00eancia de entrar no ledger. Todo consumidor (`revenue-pauta.ts:84` faz `Math.max` sobre hook_rates) passa a poder recusar comparar bases diferentes.",
    "GAP-2 (inscritos): N\u00c3O tocar em `creative_metrics.source` \u2014 o CHECK \u00e9 fechado em ('affiliate_click','organic','postback') e inscritos ganhos n\u00e3o s\u00e3o um *signal source*, s\u00e3o outcome de publica\u00e7\u00e3o. Decis\u00e3o: `publication_metrics` ganha `subscribers_gained int NOT NULL DEFAULT 0 CHECK >= 0` e `subscribers_lost` idem (aditivo, casa com o padr\u00e3o de todas as colunas existentes da tabela), e `youtube_video_metrics` carrega os mesmos campos verbatim da Analytics v2 (`subscribersGained`/`subscribersLost` j\u00e1 est\u00e3o no default de m\u00e9tricas do `youtube-data/index.ts:270` \u2014 o dado j\u00e1 vem, s\u00f3 n\u00e3o tem onde pousar).",
    "GAP-3 (atribui\u00e7\u00e3o Short\u2192longo): abandonar \u0394views por completo. `views` da Data v3 (`youtube-data/index.ts:255`, `part=statistics`) \u00e9 contador cumulativo de todas as fontes \u2014 subtrair duas leituras n\u00e3o atribui nada. A atribui\u00e7\u00e3o real vem de `youtube_traffic_sources`: dimens\u00e3o `insightTrafficSourceType` (valores `RELATED_VIDEO`, `SHORTS`, `YT_SEARCH`, `PLAYLIST`, `END_SCREEN`, `SUBSCRIBER`...) e, filtrando por tipo, `insightTrafficSourceDetail` \u2014 que para `RELATED_VIDEO` devolve o **videoId do v\u00eddeo referente**. Ou seja: no v\u00eddeo longo, as linhas com `traffic_source_type='RELATED_VIDEO'` e `source_detail=<id do Short>` S\u00c3O a atribui\u00e7\u00e3o declarada pela pr\u00f3pria API. Nada de infer\u00eancia nossa.",
    "Dedup de `youtube_traffic_sources`: `source_detail` \u00e9 NULL no relat\u00f3rio agregado por tipo, ent\u00e3o UNIQUE simples n\u00e3o deduplicaria. Usar \u00edndice \u00fanico em express\u00e3o: `CREATE UNIQUE INDEX ... ON (user_id, video_id, snapshot_at, traffic_source_type, COALESCE(source_detail, ''))`. Isso \u00e9 exatamente a armadilha que `publication_metrics` j\u00e1 tem latente e que n\u00e3o queremos repetir.",
    "GAP-4 (denominador de engaged views): proibir qualquer conta derivada nossa. NUNCA calcular AVD = `estimatedMinutesWatched \u00f7 views`. Guardar `average_view_duration_seconds` e `average_view_percentage` VERBATIM como a API devolve, mais `engaged_views` e `creator_content_type` \u2014 este \u00faltimo vindo da dimens\u00e3o `creatorContentType` da Analytics v2 (valores `shorts`/`videoOnDemand`/`liveStream`), NUNCA inferido de dura\u00e7\u00e3o \u2264 3min. Com `creator_content_type='shorts'` a UI rotula explicitamente que o denominador do AVD \u00e9 engaged views.",
    "Honestidade de aus\u00eancia: `engaged_views int NULL` + `engaged_views_available boolean NOT NULL DEFAULT false`. `NULL`/`false` significa 'a API n\u00e3o devolveu', e a UI renderiza 'n\u00e3o leg\u00edvel' \u2014 jamais `0`. Zero e aus\u00eancia s\u00e3o fatos diferentes e a tabela precisa distingui-los, sen\u00e3o o ledger mente por default (\u00e9 o mesmo motivo pelo qual o ramo Instagram faz `skipped` sem gravar linha, linha 95 do coletor).",
    "Escritor \u00fanico = ramo `youtube` novo dentro de `supabase/functions/collect-publication-metrics/index.ts`. NENHUMA fn nova \u2014 o cap est\u00e1 em 99/100 (`ls supabase/functions | grep -v '^_' | wc -l` = 99). Ele j\u00e1 \u00e9 service-role-gated in-function (`auth !== \\`Bearer ${SERVICE_KEY}\\`` \u2192 401, linha 29-30), j\u00e1 tem `verify_jwt = false` (`supabase/config.toml:46`), j\u00e1 calcula `snapshotAt` di\u00e1rio em UTC (linha 36-37) e j\u00e1 resolve token per-user de `decrypted_social_accounts` com cache (linha 59-63). O ramo YouTube \u00e9 estruturalmente id\u00eantico ao ramo Instagram: fail-soft por v\u00eddeo, `bump('youtube','skipped')` sem gravar linha quando a API n\u00e3o responde.",
    "Leitura na UI: 2 ACTIONS novas em `youtube-data` (`traffic_sources`, `audience_retention`) \u2014 de novo, zero fn nova. Ambas precisam entrar no gate de escopo em `youtube-data/index.ts:146` junto de `video_metrics`, usando o `hasAnalytics` da linha 145 (que j\u00e1 aceita o monet\u00e1rio como superset). Esquecer isso faz o Google devolver 403 cru em vez do CTA de reconex\u00e3o \u2014 \u00e9 o gate G2 do pr\u00f3prio arquivo.",
    "Refresh de token duplicado: `ensureFreshToken` vive dentro de `youtube-data`. Extrair para `supabase/functions/_shared/youtube-token.ts` antes de o coletor precisar dele \u2014 duas c\u00f3pias divergentes do refresh \u00e9 como se perde o canal em produ\u00e7\u00e3o silenciosamente."
  ],
  "api_surfaces": [
    "YouTube Analytics v2 `reports` \u2014 m\u00e9tricas core por v\u00eddeo: `ids=channel==MINE&filters=video==<VIDEO_ID>&metrics=views,engagedViews,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,likes,comments,shares,subscribersGained,subscribersLost`. J\u00e1 implementado em `youtube-data/index.ts:264-280` (aceita `body.videoId` \u2192 `filters=video==`, `body.metrics`, `body.dimensions`) \u2014 o coletor reusa o MESMO shape.",
    "YouTube Analytics v2 \u2014 tipo de conte\u00fado: `dimensions=creatorContentType` (\u2192 `shorts` | `videoOnDemand` | `liveStream`). \u00c9 a \u00daNICA fonte leg\u00edtima de 'isto \u00e9 um Short'; a Data v3 n\u00e3o exp\u00f5e a flag. Sem ela o denominador de engaged views n\u00e3o pode ser rotulado corretamente.",
    "YouTube Analytics v2 \u2014 atribui\u00e7\u00e3o agregada: `dimensions=insightTrafficSourceType&filters=video==<VIDEO_ID>&metrics=views,estimatedMinutesWatched`. Substitui integralmente o \u0394views.",
    "YouTube Analytics v2 \u2014 atribui\u00e7\u00e3o nominal (o cora\u00e7\u00e3o do Short\u2192longo): `dimensions=insightTrafficSourceDetail&filters=video==<VIDEO_ID>;insightTrafficSourceType==RELATED_VIDEO&metrics=views&sort=-views&maxResults=25`. O `insightTrafficSourceDetail` devolve o videoId do referente. Chamada obrigatoriamente separada da anterior \u2014 o detail s\u00f3 existe filtrado por um tipo.",
    "YouTube Analytics v2 \u2014 reten\u00e7\u00e3o (hook_rate de v\u00eddeo longo): `dimensions=elapsedVideoTimeRatio&filters=video==<VIDEO_ID>;audienceType==ORGANIC&metrics=audienceWatchRatio,relativeRetentionPerformance`. Pega-se o bucket mais pr\u00f3ximo de `3 / duration_seconds`.",
    "YouTube Analytics v2 \u2014 CTR/impress\u00f5es (opcional, mesma fam\u00edlia): `metrics=impressions,impressionClickThroughRate` (relat\u00f3rio separado dos core; n\u00e3o misturar num \u00fanico `metrics=` sem sondar).",
    "YouTube Data v3 `videos?part=contentDetails` \u2014 S\u00d3 para `duration` (ISO-8601), necess\u00e1ria para converter 3s em `elapsedVideoTimeRatio`. J\u00e1 dispon\u00edvel em `youtube-data/index.ts:255` (`part=snippet,contentDetails,status,statistics`). O `statistics.viewCount` daqui \u00e9 explicitamente N\u00c3O-atributivo e n\u00e3o deve alimentar nenhuma conta de atribui\u00e7\u00e3o.",
    "Escopo: os 4 escopos concedidos (`social-auth-init/index.ts:152-157`) j\u00e1 cobrem tudo acima \u2014 `yt-analytics-monetary.readonly` \u00e9 superset e o c\u00f3digo j\u00e1 trata isso (`hasAnalytics`, linha 145). Nenhum re-OAuth necess\u00e1rio para este \u00e2ngulo."
  ],
  "stack_changes": [
    "`supabase/migrations/20260720120000_youtube_metrics_spine.sql` (NOVA, 100% aditiva, `/security-review` obrigat\u00f3rio antes do commit \u2014 FMEA-011). Conte\u00fado em 4 blocos: (1) `public.youtube_video_metrics`; (2) `public.youtube_traffic_sources`; (3) ALTERs aditivos em `publication_metrics`, `creative_metrics` e `youtube_uploads`; (4) RPC `record_youtube_video_snapshot`.",
    "Bloco 1 \u2014 `public.youtube_video_metrics`: `id uuid PK`, `user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE`, `video_id text NOT NULL`, `content_variant_id uuid REFERENCES public.content_library(id) ON DELETE SET NULL`, `creator_content_type text CHECK (creator_content_type IS NULL OR creator_content_type IN ('shorts','videoOnDemand','liveStream'))`, `views int NOT NULL DEFAULT 0 CHECK >= 0`, `engaged_views int CHECK (engaged_views IS NULL OR engaged_views >= 0)`, `engaged_views_available boolean NOT NULL DEFAULT false`, `estimated_minutes_watched int NOT NULL DEFAULT 0`, `average_view_duration_seconds int`, `average_view_percentage numeric`, `likes/comments/shares int NOT NULL DEFAULT 0`, `subscribers_gained/subscribers_lost int NOT NULL DEFAULT 0 CHECK >= 0`, `impressions bigint`, `impressions_ctr numeric CHECK (0..1)`, `snapshot_at timestamptz NOT NULL`, `collected_at timestamptz NOT NULL DEFAULT now()`. `UNIQUE (user_id, video_id, snapshot_at)`. RLS: `ENABLE`, policy `SELECT USING (auth.uid() = user_id)`, SEM policy de INSERT/UPDATE (default-deny \u2192 s\u00f3 service-role escreve), `AS RESTRICTIVE FOR DELETE USING (false)`. \u00cdndice `(user_id, video_id, snapshot_at DESC)`. Molde copiado literalmente de `20260626130000_publication_metrics.sql`.",
    "Bloco 2 \u2014 `public.youtube_traffic_sources`: `id uuid PK`, `user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE`, `video_id text NOT NULL` (destino), `traffic_source_type text NOT NULL`, `source_detail text` (para `RELATED_VIDEO` = videoId referente), `views int NOT NULL DEFAULT 0 CHECK >= 0`, `estimated_minutes_watched int NOT NULL DEFAULT 0`, `window_start date NOT NULL`, `window_end date NOT NULL`, `snapshot_at timestamptz NOT NULL`, `collected_at`. Dedup: `CREATE UNIQUE INDEX youtube_traffic_sources_uniq ON public.youtube_traffic_sources (user_id, video_id, snapshot_at, traffic_source_type, COALESCE(source_detail, ''))` \u2014 \u00edndice em express\u00e3o, N\u00c3O constraint UNIQUE simples (NULL n\u00e3o dedupa). Mesma tr\u00edade de RLS do bloco 1. \u00cdndice de leitura `(user_id, video_id, snapshot_at DESC, views DESC)`.",
    "Bloco 3a \u2014 `ALTER TABLE public.publication_metrics ADD COLUMN IF NOT EXISTS subscribers_gained int NOT NULL DEFAULT 0 CHECK (subscribers_gained >= 0)`, idem `subscribers_lost`, e `ADD COLUMN IF NOT EXISTS engaged_views int CHECK (engaged_views IS NULL OR engaged_views >= 0)` (NULLABLE de prop\u00f3sito: aus\u00eancia \u2260 zero).",
    "Bloco 3b \u2014 `ALTER TABLE public.creative_metrics ADD COLUMN IF NOT EXISTS hook_rate_basis text CHECK (hook_rate_basis IS NULL OR hook_rate_basis IN ('engaged_views_ratio','retention_at_3s','ig_plays_ratio'))` + `ADD COLUMN IF NOT EXISTS hook_rate_source_ref text`. N\u00c3O tocar no CHECK de `source` (fechado) nem na constraint `creative_metrics_variant_source_uniq`.",
    "Bloco 3c \u2014 `ALTER TABLE public.youtube_uploads ADD COLUMN IF NOT EXISTS content_variant_id uuid REFERENCES public.content_library(id) ON DELETE SET NULL` + \u00edndice parcial `WHERE content_variant_id IS NOT NULL`. Aten\u00e7\u00e3o: `20260719170000_youtube_uploads.sql` est\u00e1 untracked no git mas a mem\u00f3ria indica migration VIVA (h\u00e1 `scripts/qa/apply-youtube-uploads-migration.sh`) \u2014 por isso ALTER separado com `IF NOT EXISTS`, n\u00e3o edi\u00e7\u00e3o do arquivo original. A policy `youtube_uploads_insert_own` (linha 57-62) restringe as colunas que o cliente pode setar no INSERT; verificar se `content_variant_id` precisa entrar no WITH CHECK ou se o cliente n\u00e3o deve set\u00e1-la.",
    "Bloco 4 \u2014 RPC `public.record_youtube_video_snapshot(p_user_id uuid, p_video_id text, p_snapshot_at timestamptz, p_metrics jsonb, p_traffic jsonb, p_content_variant_id uuid DEFAULT NULL, p_hook_rate numeric DEFAULT NULL, p_hook_rate_basis text DEFAULT NULL)` \u2014 `LANGUAGE plpgsql SECURITY DEFINER SET search_path = ''`, seguido de `REVOKE EXECUTE ON FUNCTION ... FROM PUBLIC, anon, authenticated; GRANT EXECUTE ... TO service_role`. Molde: `finalize_youtube_upload` (`20260719170000:118-142`) e `finalize_video_render`. Corpo: (i) `IF p_hook_rate IS NOT NULL AND p_hook_rate_basis IS NULL THEN RAISE EXCEPTION 'hook_rate requires basis' USING errcode='22023'` \u2014 o gate de proced\u00eancia; (ii) upsert `youtube_video_metrics` ON CONFLICT `(user_id, video_id, snapshot_at)`; (iii) loop sobre `p_traffic` com upsert nas `youtube_traffic_sources`; (iv) `UPDATE public.creative_metrics SET hook_rate = p_hook_rate, hook_rate_basis = p_hook_rate_basis, hook_rate_source_ref = 'youtube_video_metrics:'||v_snapshot_id WHERE content_variant_id = p_content_variant_id AND source = 'organic' AND user_id = p_user_id` \u2014 s\u00f3 quando `p_content_variant_id IS NOT NULL`. Tudo numa transa\u00e7\u00e3o \u21d2 \u00e9 imposs\u00edvel existir hook_rate sem a linha bruta que o originou.",
    "`supabase/functions/collect-publication-metrics/index.ts` \u2014 ramo `youtube` novo, espelhando o ramo Instagram (linhas 78-99). Enumera\u00e7\u00e3o de v\u00eddeos: `youtube_uploads` com `state='done' AND youtube_video_id IS NOT NULL` (\u222a `scheduled_posts` platform='youtube'), e, para os 50+ v\u00eddeos hist\u00f3ricos do canal, a uploads playlist. 4 chamadas Analytics por v\u00eddeo (core / creatorContentType / traffic type / traffic detail RELATED_VIDEO) + 1 de reten\u00e7\u00e3o s\u00f3 para n\u00e3o-Shorts. Grava tudo via UMA chamada `record_youtube_video_snapshot`. Fail-soft por v\u00eddeo com `bump('youtube','skipped')` \u2014 jamais linha fabricada. Adicionar `youtube` ao `summary` de telemetria (linha 108).",
    "`supabase/functions/_shared/youtube-token.ts` (NOVO arquivo compartilhado, n\u00e3o \u00e9 edge fn \u2014 n\u00e3o conta no cap). Extrair `ensureFreshToken` de `youtube-data/index.ts:166` para c\u00e1 e reapontar ambos os chamadores. Duas c\u00f3pias divergentes do refresh de token \u00e9 falha silenciosa de canal em produ\u00e7\u00e3o.",
    "`supabase/functions/youtube-data/index.ts` \u2014 2 ACTIONS novas (`traffic_sources`, `audience_retention`) modeladas no bloco `video_metrics` (linhas 264-280), MAIS a entrada delas no gate de escopo da linha 146: `if ((action === 'video_metrics' || action === 'traffic_sources' || action === 'audience_retention') && !hasAnalytics)`.",
    "`src/hooks/useYouTubeStudio.ts` \u2014 `useYouTubeTrafficSources(videoId)` e `useYouTubeRetention(videoId)` (TanStack Query, molde do `useYouTubeChannelMetrics` existente) + `useYouTubeVideoSnapshots(videoId)` lendo `youtube_video_metrics` direto pelo client sob RLS SELECT-own.",
    "`src/pages/YouTubeStudioPage.tsx` (589 linhas) + rota nova `/dashboard/youtube/studio-yt/:videoId` em `src/App.tsx` (lazy, dentro do subtree `DashboardLayout`). A p\u00e1gina dedicada por v\u00eddeo renderiza: s\u00e9rie temporal de `youtube_video_metrics`, painel de fontes de tr\u00e1fego com os Shorts referentes nomeados, e o `hook_rate` SEMPRE com o r\u00f3tulo da `hook_rate_basis` ao lado.",
    "`docs/processes/youtube-metrics-collection.md` (SOP Lei 2, ANTES do c\u00f3digo): Operator (hoje o Sovereign l\u00ea \u00e0 m\u00e3o no YouTube Studio) / Sequence (as 4-5 chamadas por v\u00eddeo, em ordem) / Verification gates (a sonda de cada m\u00e9trica, item por item) / Recovery (falha no v\u00eddeo N \u21d2 skip + telemetria, re-run di\u00e1rio \u00e9 idempotente pela UNIQUE) / Success signal (`SELECT count(*) FROM youtube_traffic_sources WHERE traffic_source_type='RELATED_VIDEO'` > 0 com `source_detail` batendo num Short real do canal).",
    "`scripts/qa/smoke-youtube-metrics.ts` (molde `smoke-reshape-pillar.ts`): gates zero-custo \u2014 (G1) RPC nega `authenticated`; (G2) `hook_rate` sem `basis` \u2192 exce\u00e7\u00e3o; (G3) cross-tenant SELECT = 0 linhas; (G4) re-run mesmo dia n\u00e3o duplica (UNIQUE + \u00edndice em express\u00e3o); (G5) `engaged_views_available=false` nunca vira 0 na UI; (G6) nenhuma linha gravada quando a Analytics devolve erro.",
    "`src/integrations/supabase/types.ts` \u2014 regenerar via `npx supabase gen types typescript --linked` ap\u00f3s aplicar (fica stale silenciosamente; `tsc` n\u00e3o acusa at\u00e9 algu\u00e9m ler a coluna nova)."
  ],
  "ai_layer": "A IA entra DEPOIS da coleta, como int\u00e9rprete de linhas que j\u00e1 existem no banco \u2014 nunca como fonte de n\u00famero.\n\nComo entra: a p\u00e1gina dedicada do v\u00eddeo monta um payload fechado a partir de (a) a s\u00e9rie de `youtube_video_metrics` daquele `video_id`, (b) as linhas de `youtube_traffic_sources` com os Shorts referentes j\u00e1 resolvidos para t\u00edtulo via `list_videos`, e (c) o `hook_rate` com sua `hook_rate_basis`. Esse payload vai para `generate-content` (streaming, j\u00e1 existente) ou `intent-execute`, com credencial BYOK per-user resolvida por `resolveProviderKey` \u2014 e o seletor de provider na UI s\u00f3 oferece o que o usu\u00e1rio tem configurado (`useConfiguredProviders`, regra perene). Sem BYOK \u21d2 402 estruturado com CTA, nunca uma chave global de sistema.\n\nO que ela produz: leitura em linguagem natural das fontes de tr\u00e1fego (\"62% das views deste v\u00eddeo vieram de RELATED_VIDEO, e 41% desse total do Short X\"), hip\u00f3teses de reten\u00e7\u00e3o ancoradas na curva `audienceWatchRatio`, e sugest\u00f5es de pr\u00f3ximo formato \u2014 cada afirma\u00e7\u00e3o carregando o id da linha que a originou (`youtube_traffic_sources:<uuid>`), renderizado como refer\u00eancia clic\u00e1vel.\n\nO que ela N\u00c3O pode fazer, e como isso \u00e9 imposto e n\u00e3o s\u00f3 pedido:\n1. N\u00e3o pode emitir n\u00famero ausente do payload. Imposi\u00e7\u00e3o estrutural: o payload \u00e9 montado por c\u00f3digo a partir de SELECTs, e a resposta \u00e9 validada contra o conjunto de valores enviados antes de renderizar \u2014 n\u00famero n\u00e3o-reconhecido \u00e9 bloqueado, n\u00e3o exibido com ressalva.\n2. N\u00e3o pode inferir atribui\u00e7\u00e3o. Se n\u00e3o h\u00e1 linha `RELATED_VIDEO` com `source_detail` preenchido, a UI diz \"atribui\u00e7\u00e3o n\u00e3o dispon\u00edvel para este v\u00eddeo\" \u2014 a IA n\u00e3o recebe permiss\u00e3o de conjecturar qual Short trouxe as views.\n3. N\u00e3o pode preencher aus\u00eancia com zero. `engaged_views_available = false` \u21d2 o campo nem entra no payload; a IA n\u00e3o v\u00ea um 0 que interpretaria como \"engajamento nulo\".\n4. N\u00e3o pode comparar hook_rates de bases diferentes. `engaged_views_ratio` (Shorts) e `retention_at_3s` (longo) s\u00e3o grandezas distintas; o montador do payload separa por basis e a IA recebe os grupos rotulados.\n5. N\u00e3o pode escrever no ledger. Nenhum caminho de IA chama `record_youtube_video_snapshot` \u2014 o RPC \u00e9 service-role-only e o \u00fanico chamador \u00e9 o coletor.\n6. N\u00e3o pode prometer resultado. O prompt de sistema pro\u00edbe linguagem de garantia; sa\u00eddas s\u00e3o hip\u00f3teses test\u00e1veis com o experimento que as verificaria.\n\nToda execu\u00e7\u00e3o emite n\u00f3 de observa\u00e7\u00e3o na Knowledge Mesh e telemetria em `infra_health_logs` com `service='youtube-metrics-ai'` (Mesh Mandate).",
  "honesty_guards": [
    "`engaged_views_available boolean` + `engaged_views` NULLABLE: aus\u00eancia e zero s\u00e3o fatos diferentes. Sem essa separa\u00e7\u00e3o o ledger mente por default \u2014 um v\u00eddeo cuja m\u00e9trica a API n\u00e3o devolveu apareceria como engajamento nulo. UI renderiza 'n\u00e3o leg\u00edvel', jamais 0.",
    "RPC recusa `hook_rate` sem `hook_rate_basis` (RAISE EXCEPTION, errcode 22023). Um hook_rate sem proced\u00eancia \u00e9 um n\u00famero inventado com apar\u00eancia de medi\u00e7\u00e3o \u2014 e como as duas f\u00f3rmulas (Shorts vs longo) n\u00e3o s\u00e3o compar\u00e1veis, a coluna `numeric` sozinha convida \u00e0 compara\u00e7\u00e3o errada. `revenue-pauta.ts:84` faz `Math.max` sobre hook_rates de creativos diferentes; sem basis isso j\u00e1 \u00e9 um bug latente hoje.",
    "`creator_content_type` vem EXCLUSIVAMENTE da dimens\u00e3o `creatorContentType` da Analytics v2. Nunca inferir '\u00e9 Short' de `duration <= 180s` \u2014 a heur\u00edstica erra em v\u00eddeos curtos verticais que n\u00e3o s\u00e3o Shorts e o denominador do AVD sai errado silenciosamente.",
    "AVD e average_view_percentage gravados VERBATIM. Proibido calcular `estimatedMinutesWatched \u00f7 views`: desde 31/03/2025 o denominador de Shorts \u00e9 engaged views, n\u00e3o views, e a conta manual produz um n\u00famero plaus\u00edvel e errado \u2014 o pior tipo de erro.",
    "`statistics.viewCount` da Data v3 (`youtube-data/index.ts:255`) \u00e9 marcado no COMMENT da tabela como N\u00c3O-ATRIBUTIVO. Nenhum caminho de c\u00f3digo pode derivar atribui\u00e7\u00e3o de subtra\u00e7\u00e3o de views; a atribui\u00e7\u00e3o tem uma \u00fanica fonte, `youtube_traffic_sources`.",
    "Coletor fail-soft por v\u00eddeo, espelhando o ramo Instagram (linha 95 do coletor: erro \u21d2 `continue` sem upsert). V\u00eddeo cuja Analytics falhou n\u00e3o gera linha \u2014 gera `bump('youtube','skipped')` e entra no `collect_summary`. Zero fabrica\u00e7\u00e3o sob falha parcial.",
    "Telemetria em `infra_health_logs` sem PII, s\u00f3 contagens em allowlist \u2014 mant\u00e9m o padr\u00e3o da linha 104-108 do coletor (a tabela \u00e9 global-read, n\u00e3o pode vazar per-tenant).",
    "RLS uniforme nas 2 tabelas novas: SELECT-own, INSERT/UPDATE sem policy permissiva (default-deny para `authenticated`), RESTRICTIVE no-delete. Um tenant nunca forja m\u00e9trica de outro nem apaga a pr\u00f3pria hist\u00f3ria. \u00cdndice em express\u00e3o com `COALESCE(source_detail,'')` fecha o furo de dedup que UNIQUE simples deixaria aberto.",
    "`/security-review` obrigat\u00f3rio na migration antes do commit (CLAUDE.md, sem exce\u00e7\u00e3o \u2014 FMEA-011), e o smoke `scripts/qa/smoke-youtube-metrics.ts` como anticorpo re-execut\u00e1vel antes de qualquer mexida futura no RPC ou nas policies."
  ],
  "open_questions": [
    "SONDAR ANTES DE ESCREVER QUALQUER C\u00d3DIGO (precedente OTD-CI-002 \u2014 'sondar, n\u00e3o assumir'): a m\u00e9trica `engagedViews` \u00e9 aceita pela Analytics v2 para ESTE canal? Rodar `youtube-data` com `action=video_metrics, metrics='views,engagedViews', videoId=<id real>` e ler o corpo do 400 se houver. O GAP-4 inteiro depende disso; se n\u00e3o existir, o hook_rate de Shorts cai para `retention_at_3s` e a decis\u00e3o de basis muda.",
    "`creatorContentType` \u00e9 aceito como dimens\u00e3o em combina\u00e7\u00e3o com `filters=video==<id>`? Combina\u00e7\u00f5es dimens\u00e3o\u00d7filtro na Analytics v2 s\u00e3o uma matriz restrita e nem toda combina\u00e7\u00e3o v\u00e1lida isoladamente \u00e9 v\u00e1lida junta. Se n\u00e3o for, `creator_content_type` precisa vir de uma chamada agregada separada por canal.",
    "`insightTrafficSourceDetail` devolve mesmo o videoId do referente para `RELATED_VIDEO` neste canal, ou vem redigido/agregado por baixo volume? Toda a atribui\u00e7\u00e3o Short\u2192longo (GAP-3) repousa nisso. Sondar com o Short mais visto do canal como alvo.",
    "A 'YouTube Analytics API' est\u00e1 habilitada no projeto Google Cloud? O contexto marca como 'a checar'. Sem ela, `video_metrics` j\u00e1 retornaria erro hoje \u2014 vale confirmar se as a\u00e7\u00f5es existentes de Analytics alguma vez rodaram com sucesso em produ\u00e7\u00e3o, porque isso muda o diagn\u00f3stico de 'gap de medi\u00e7\u00e3o' para 'API nunca ligada'.",
    "Relat\u00f3rios de reten\u00e7\u00e3o (`audienceWatchRatio` \u00d7 `elapsedVideoTimeRatio`) t\u00eam m\u00ednimo de views para n\u00e3o serem suprimidos? Se os v\u00eddeos do canal estiverem abaixo do limiar, o `hook_rate` de v\u00eddeo longo nasce sempre NULL e s\u00f3 o caminho de Shorts funciona \u2014 o que \u00e9 aceit\u00e1vel, mas precisa estar decidido antes de a UI prometer o campo.",
    "Agendamento do coletor: `grep -rn 'cron.schedule' supabase/migrations/*.sql` retorna VAZIO \u2014 nenhuma migration agenda `collect-publication-metrics`, apesar de a mem\u00f3ria registrar 'pg_cron jobid 3'. O agendamento \u00e9 out-of-band. Confirmar com `SELECT jobid, schedule, command FROM cron.job` antes de assumir que o ramo YouTube novo vai rodar sozinho; e, se for out-of-band, isso \u00e9 drift que a `docs/processes/schema-drift-audit.md` manda virar migration na MESMA sess\u00e3o.",
    "`youtube_uploads` est\u00e1 untracked no git mas a mem\u00f3ria diz 'migration viva'. Confirmar materialmente se a tabela existe no banco deployado (`\\\\d public.youtube_uploads`) antes de emitir o ALTER do bloco 3c \u2014 e verificar se `content_variant_id` deve entrar no WITH CHECK da policy `youtube_uploads_insert_own` (linhas 57-62) ou se s\u00f3 o worker service-role a preenche.",
    "Os 50+ v\u00eddeos hist\u00f3ricos do canal: coletar m\u00e9tricas para todos, ou s\u00f3 para os que a Upload Factory publicar daqui em diante? Coletar todos multiplica as chamadas Analytics por 4-5 e pode bater em quota. Sugest\u00e3o a validar com o Sovereign: janela inicial dos N v\u00eddeos mais recentes + backfill sob demanda ao abrir a p\u00e1gina dedicada.",
    "Quota da Analytics v2 para a cad\u00eancia di\u00e1ria \u00d7 4-5 chamadas \u00d7 N v\u00eddeos \u2014 precisa de um teto antes de ligar o cron, sen\u00e3o o coletor esgota a quota e passa a produzir `skipped` em massa, que \u00e9 honesto mas in\u00fatil."
  ]
}
```

> **Tool Result (StructuredOutput)** - ✅ Success
>
> ```
> Structured output provided successfully
> ```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-20 - agent-a6b3f8ff95d37a5ad]]
> * **Próxima Sessão**: [[2026-07-20 - agent-a6d666d80603fb2e8]]
%% --- TIMELINE END --- %%

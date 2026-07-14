# Session agent-a9bbe88a5dded31da
**Date:** 2026-07-14 | **Session ID:** `agent-a9bbe88a5dded31da`

---

## 👤 User *(13:25:10)*

You are a senior security engineer reviewing UNCOMMITTED changes in /home/gcrUX/htdocs/constellation-orchestra (run `git status --short` and `git diff` and read new untracked files).

Changes under review (Amendment 24 — media rails, FR-SPACES-082/083/084/085):
- supabase/functions/publish-social/index.ts: (a) LinkedIn branch — when content.image_url exists: registerUpload (v2 assets, owner=urn:li:person:<platform_user_id>) → fetch(content.image_url) → PUT bytes to LinkedIn's uploadUrl → ugcPost IMAGE; (b) IG branch — content.surface 'story'/'stories' + media → container media_type=STORIES; (c) twitter branch — content.image_url → fetch bytes → POST api.x.com/2/media/upload multipart → tweet with media_ids; 401/403 on upload → actionable error (scope missing).
- supabase/functions/social-auth-init/index.ts: twitter scopes += media.write.
- supabase/functions/auto-publish/index.ts: copies reshape.content.surface (string, 60-char cap) into the native payload as a surface discriminator.
- src/lib/format-specs.ts: 4 catalog note strings (client display only).
- docs: markdown (excluded).

TRUST MODEL context (verify in code): publish-social callers are (1) the cron auto-publish with service-role Bearer + user_id in body — content there is server-built: text from content_library, surface a plain string from owner-writable scheduled_posts.metadata, image_url/video_url/images[] ONLY from server-resolved owner-bound ledger rows signed in auto-publish (FMEA-011); (2) user-JWT callers where content can be FULLY CLIENT-CONTROLLED (verify how publish-social authenticates user-JWT callers and whether a user can pass arbitrary content.image_url for their own account — that was ALREADY true for IG image_url pre-change; assess what the NEW code changes about that).

Evaluate:
(a) SSRF via content.image_url in the NEW fetch() calls (LinkedIn branch, twitter branch): who controls image_url per caller path? For user-JWT callers it is attacker-controlled (their own JWT) — fetch(url) from the edge function = SSRF primitive? Compare with the PRE-EXISTING exposure (IG branch already passed image_url to Meta's servers — Meta fetched it, NOT our function; TikTok branch already fetch()es video_url ourselves — read publish-social's TikTok FILE_UPLOAD code and whether this SSRF class was already accepted/mitigated). Edge runtime = Deno Deploy isolate — what internal surface is reachable (metadata endpoints? localhost services?)? Rate the NEW delta honestly.
(b) The response bytes of fetch(image_url) are forwarded to LinkedIn/X as the caller's own media — any cross-tenant angle?
(c) surface discriminator: can a crafted surface value (e.g. 'story' on a feed post) cause harm beyond the caller's own post shape?
(d) media.write scope addition — any risk to existing connections/refresh flows?
(e) leakage: do the new pulse() telemetry calls write PII/secrets into infra_health_logs (global-read)?

EXCLUSIONS: DoS-only, rate limits, theoretical races, docs, test files. Report only findings >80% confidence with file:line, severity, exploit scenario, fix, confidence 0-1; if a finding is a PRE-EXISTING class (not newly added), say so explicitly and do not count it as a new finding, but mention it in a pre-existing-notes section. If nothing meets the bar, say exactly that per vector. Your final message is the report.

## 🤖 Claude *(13:25:15)*


## 🤖 Claude *(13:25:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git status --short && echo \"---\" && git diff --stat",
  "description": "Show working tree status and diff stats"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>  M src/lib/format-specs.ts
>  M supabase/functions/auto-publish/index.ts
>  M supabase/functions/publish-social/index.ts
>  M supabase/functions/social-auth-init/index.ts
> ?? docs/bok/spaces-evolution/24-amendment-media-rails.md
> ---
>  src/lib/format-specs.ts                      |   8 +--
>  supabase/functions/auto-publish/index.ts     |   3 +
>  supabase/functions/publish-social/index.ts   | 100 ++++++++++++++++++++++++---
>  supabase/functions/social-auth-init/index.ts |   4 +-
>  4 files changed, 99 insertions(+), 16 deletions(-)
> ```

## 🤖 Claude *(13:25:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git diff supabase/functions/publish-social/index.ts supabase/functions/social-auth-init/index.ts supabase/functions/auto-publish/index.ts src/lib/format-specs.ts",
  "description": "Show full diff of changed files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> diff --git a/src/lib/format-specs.ts b/src/lib/format-specs.ts
> index 885eda5..4209f93 100644
> --- a/src/lib/format-specs.ts
> +++ b/src/lib/format-specs.ts
> @@ -87,7 +87,7 @@ export const PUBLICATION_FORMATS: PublicationFormat[] = [
>      id: "instagram_stories", label: "Instagram Stories", platform: "instagram", channel: "instagram", surface: "story",
>      kind: "any", chrome: "vertical-story", aspect: { w: 9, h: 16 }, px: { w: 1080, h: 1920 },
>      safeZone: { topPct: 12, bottomPct: 20 }, caption: { max: 2200 },
> -    publishable: "preview", previewNote: "Stories ainda não têm trilho de publicação — só pré-visualização.",
> +    publishable: "preview", previewNote: "Trilho instalado (STORIES) — libera após o primeiro teste de publicação.",
>    },
>    {
>      id: "instagram_carousel", label: "Instagram Carrossel", platform: "instagram", channel: "instagram", surface: "carousel",
> @@ -122,7 +122,7 @@ export const PUBLICATION_FORMATS: PublicationFormat[] = [
>      id: "youtube_community", label: "YouTube Comunidade", platform: "youtube", channel: "youtube", surface: "community",
>      kind: "any", chrome: "yt-community", aspect: { w: 1, h: 1 }, px: { w: 1080, h: 1080 },
>      caption: { max: 5000 },
> -    publishable: "preview", previewNote: "Posts de comunidade ainda não têm trilho na API — só pré-visualização.",
> +    publishable: "preview", previewNote: "A API do YouTube não expõe escrita de posts de comunidade — publique manualmente no Studio.",
>    },
>  
>    // ── Facebook ─────────────────────────────────────────────────────────────
> @@ -144,7 +144,7 @@ export const PUBLICATION_FORMATS: PublicationFormat[] = [
>      id: "linkedin_feed", label: "LinkedIn", platform: "linkedin", channel: "linkedin", surface: "feed_image",
>      kind: "any", chrome: "feed-portrait", aspect: { w: 4, h: 5 }, px: { w: 1080, h: 1350 },
>      caption: { max: 3000, optimal: [1300, 1900] },
> -    publishable: "preview", previewNote: "LinkedIn publica só o texto por enquanto — anexo de mídia em breve.",
> +    publishable: "preview", previewNote: "Trilho de imagem instalado — libera após o primeiro teste de publicação.",
>    },
>  
>    // ── X (Twitter) ──────────────────────────────────────────────────────────
> @@ -152,7 +152,7 @@ export const PUBLICATION_FORMATS: PublicationFormat[] = [
>      id: "twitter_post", label: "X (Twitter)", platform: "twitter", channel: "twitter_x", surface: "post",
>      kind: "any", chrome: "text-post", aspect: { w: 1, h: 1 }, px: { w: 1080, h: 1080 },
>      caption: { max: 280 },
> -    publishable: "preview", previewNote: "X publica só o texto/thread por enquanto — mídia em breve.",
> +    publishable: "preview", previewNote: "Trilho de imagem instalado — reconecte a conta X (escopo novo) e aguarde o primeiro teste.",
>    },
>  
>    // ── Pinterest ────────────────────────────────────────────────────────────
> diff --git a/supabase/functions/auto-publish/index.ts b/supabase/functions/auto-publish/index.ts
> index 444036c..bfeddbe 100644
> --- a/supabase/functions/auto-publish/index.ts
> +++ b/supabase/functions/auto-publish/index.ts
> @@ -113,6 +113,9 @@ Deno.serve(async (req) => {
>          if (reshape?.content) {
>            const c = reshape.content;
>            const native: Record<string, unknown> = { text: typeof c.text === "string" ? c.text : contentText };
> +          // FR-SPACES-083 — surface discriminator (plain string, e.g. 'stories'): lets publish-social pick the
> +          // right IG media_type. Metadata-borne but INERT (it selects a container type, never an asset ref).
> +          if (typeof c.surface === "string") native.surface = c.surface.slice(0, 60);
>            // Attach the per-row asset ref resolved from an OWNER-SCOPED ledger row (server-trusted), NEVER from metadata.
>            const attachAsset = async (bucket?: string, key?: string, kind?: string) => {
>              if (!bucket || !key) return;
> diff --git a/supabase/functions/publish-social/index.ts b/supabase/functions/publish-social/index.ts
> index 627c2e0..1618b24 100644
> --- a/supabase/functions/publish-social/index.ts
> +++ b/supabase/functions/publish-social/index.ts
> @@ -121,20 +121,61 @@ Deno.serve(async (req) => {
>          .then(() => {}, () => {});
>  
>      if (platform === "linkedin") {
> +      // FR-SPACES-082 (Amendment 24) — image attach: w_member_social ALREADY covers the assets API, so when the
> +      // pipeline hands us an image_url (a fresh owner-scoped signed URL from auto-publish) we register + upload
> +      // the bytes and publish shareMediaCategory IMAGE. No image_url → text-only ugcPost, byte-identical to before.
> +      const liHeaders = {
> +        Authorization: `Bearer ${account.access_token}`,
> +        "Content-Type": "application/json",
> +        "X-Restli-Protocol-Version": "2.0.0",
> +      };
> +      const authorUrn = `urn:li:person:${account.platform_user_id}`;
> +      let liMedia: { status: string; media: string }[] | null = null;
> +      if (typeof content.image_url === "string" && content.image_url) {
> +        const regRes = await fetch("https://api.linkedin.com/v2/assets?action=registerUpload", {
> +          method: "POST", headers: liHeaders,
> +          body: JSON.stringify({
> +            registerUploadRequest: {
> +              recipes: ["urn:li:digitalmediaRecipe:feedshare-image"],
> +              owner: authorUrn,
> +              serviceRelationships: [{ relationshipType: "OWNER", identifier: "urn:li:userGeneratedContent" }],
> +            },
> +          }),
> +        });
> +        const reg = await regRes.json().catch(() => ({}));
> +        const uploadUrl = reg?.value?.uploadMechanism?.["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]?.uploadUrl;
> +        const assetUrn = reg?.value?.asset;
> +        if (!regRes.ok || !uploadUrl || !assetUrn) {
> +          console.error("LinkedIn registerUpload error:", regRes.status, reg);
> +          pulse("error", "linkedin_image_register_failed", { status: regRes.status });
> +          throw new Error("PLATFORM_PUBLISH_FAILED");
> +        }
> +        const imgRes = await fetch(content.image_url);
> +        if (!imgRes.ok) { pulse("error", "linkedin_image_fetch_failed", { status: imgRes.status }); throw new Error("PLATFORM_PUBLISH_FAILED"); }
> +        const putRes = await fetch(uploadUrl, {
> +          method: "PUT",
> +          headers: { Authorization: `Bearer ${account.access_token}` },
> +          body: new Uint8Array(await imgRes.arrayBuffer()),
> +        });
> +        if (!putRes.ok) {
> +          console.error("LinkedIn asset upload error:", putRes.status);
> +          pulse("error", "linkedin_image_upload_failed", { status: putRes.status });
> +          throw new Error("PLATFORM_PUBLISH_FAILED");
> +        }
> +        liMedia = [{ status: "READY", media: assetUrn }];
> +        pulse("ok", "linkedin_image_uploaded");
> +      }
>        const res = await fetch("https://api.linkedin.com/v2/ugcPosts", {
>          method: "POST",
> -        headers: {
> -          Authorization: `Bearer ${account.access_token}`,
> -          "Content-Type": "application/json",
> -          "X-Restli-Protocol-Version": "2.0.0",
> -        },
> +        headers: liHeaders,
>          body: JSON.stringify({
> -          author: `urn:li:person:${account.platform_user_id}`,
> +          author: authorUrn,
>            lifecycleState: "PUBLISHED",
>            specificContent: {
>              "com.linkedin.ugc.ShareContent": {
>                shareCommentary: { text: content.text || content },
> -              shareMediaCategory: "NONE",
> +              shareMediaCategory: liMedia ? "IMAGE" : "NONE",
> +              ...(liMedia ? { media: liMedia } : {}),
>              },
>            },
>            visibility: { "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC" },
> @@ -186,15 +227,23 @@ Deno.serve(async (req) => {
>          if (!pubRes.ok) { console.error("Instagram carousel publish error:", pubRes.status, result); throw new Error("PLATFORM_PUBLISH_FAILED"); }
>        } else {
>        const videoUrl = content.video_url;
> +      // FR-SPACES-083 (Amendment 24) — IG STORIES: same container→publish flow, media_type=STORIES; the surface
> +      // discriminator rides content.surface (copied server-side by auto-publish from the reshape row, never a
> +      // trusted asset ref). Stories carry no caption (the API ignores it). Covered by the SAME scope
> +      // (instagram_business_content_publish) — reach stays gated on the Meta app audit like the whole IG rail.
> +      // catalog (format-specs) says "story"; seed/channel naming elsewhere says "stories" — accept both.
> +      const isStory = (content.surface === "story" || content.surface === "stories") && (videoUrl || content.image_url);
>        const createRes = await fetch(
>          `${IG_BASE}/${igAccountId}/media`,
>          {
>            method: "POST",
>            headers: { "Content-Type": "application/json" },
>            body: JSON.stringify(
> -            videoUrl
> -              ? { media_type: "REELS", video_url: videoUrl, caption: content.text || content, access_token: account.access_token }
> -              : { caption: content.text || content, image_url: content.image_url, access_token: account.access_token },
> +            isStory
> +              ? { media_type: "STORIES", ...(videoUrl ? { video_url: videoUrl } : { image_url: content.image_url }), access_token: account.access_token }
> +              : videoUrl
> +                ? { media_type: "REELS", video_url: videoUrl, caption: content.text || content, access_token: account.access_token }
> +                : { caption: content.text || content, image_url: content.image_url, access_token: account.access_token },
>            ),
>          }
>        );
> @@ -282,9 +331,38 @@ Deno.serve(async (req) => {
>          result = { id: ids[0] ?? null, thread_ids: ids };
>          pulse("ok", "twitter_thread_published", { tweets: ids.length });
>        } else {
> +        // FR-SPACES-084 (Amendment 24) — image attach via media upload v2. Needs the media.write scope
> +        // (added to social-auth-init; PRE-EXISTING connections lack it → 403 here). Anti false-success:
> +        // a post promised WITH media never silently goes out text-only — we fail with an actionable error.
> +        let mediaIds: string[] | null = null;
> +        if (typeof content.image_url === "string" && content.image_url) {
> +          const imgRes = await fetch(content.image_url);
> +          if (!imgRes.ok) { pulse("error", "twitter_media_fetch_failed", { status: imgRes.status }); throw new Error("PLATFORM_PUBLISH_FAILED"); }
> +          const form = new FormData();
> +          form.append("media", await imgRes.blob());
> +          form.append("media_category", "tweet_image");
> +          const upRes = await fetch("https://api.x.com/2/media/upload", {
> +            method: "POST", headers: { Authorization: `Bearer ${account.access_token}` }, body: form,
> +          });
> +          const up = await upRes.json().catch(() => ({}));
> +          if (!upRes.ok) {
> +            console.error("X media upload error:", upRes.status, up);
> +            pulse("error", "twitter_media_upload_failed", { status: upRes.status });
> +            // 401/403 on upload with a valid tweet token ⇒ the token predates the media.write scope.
> +            if (upRes.status === 401 || upRes.status === 403) throw new Error("twitter_media_scope_missing: reconecte a conta X em /dashboard/settings para conceder media.write");
> +            throw new Error("PLATFORM_PUBLISH_FAILED");
> +          }
> +          const mediaId = up?.data?.id ?? up?.media_id_string ?? null;
> +          if (!mediaId) { pulse("error", "twitter_media_no_id"); throw new Error("PLATFORM_PUBLISH_FAILED"); }
> +          mediaIds = [String(mediaId)];
> +          pulse("ok", "twitter_media_uploaded");
> +        }
>          const res = await fetch("https://api.x.com/2/tweets", {
>            method: "POST", headers: xHeaders,
> -          body: JSON.stringify({ text: (content.text || content)?.toString()?.slice(0, 280) }),
> +          body: JSON.stringify({
> +            text: (content.text || content)?.toString()?.slice(0, 280),
> +            ...(mediaIds ? { media: { media_ids: mediaIds } } : {}),
> +          }),
>          });
>          result = await res.json();
>          if (!res.ok) { console.error("Twitter publish error:", res.status, result); throw new Error("PLATFORM_PUBLISH_FAILED"); }
> diff --git a/supabase/functions/social-auth-init/index.ts b/supabase/functions/social-auth-init/index.ts
> index 0b15f51..ae87dce 100644
> --- a/supabase/functions/social-auth-init/index.ts
> +++ b/supabase/functions/social-auth-init/index.ts
> @@ -97,7 +97,9 @@ Deno.serve(async (req) => {
>        }
>        // Twitter OAuth 2.0 with PKCE
>        const codeChallenge = state.slice(0, 43); // simple challenge for demo; production should use S256
> -      const scopes = "tweet.read tweet.write users.read offline.access";
> +      // media.write (FR-SPACES-084): image/video upload for tweets. Connections made BEFORE this scope was
> +      // added lack it — publish-social fails those with an actionable "reconecte a conta X" error.
> +      const scopes = "tweet.read tweet.write users.read offline.access media.write";
>        authUrl = `${TWITTER_AUTH_URL}?response_type=code&client_id=${clientId}&redirect_uri=${encodeURIComponent(callbackUrl)}&state=${encodeURIComponent(state)}&scope=${encodeURIComponent(scopes)}&code_challenge=${codeChallenge}&code_challenge_method=plain`;
>  
>      } else if (platform === "tiktok") {
> ```

## 🤖 Claude *(13:25:28)*


## 🤖 Claude *(13:25:28)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-social/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 2	import { notify } from "../_shared/notify.ts";
> 3	
> 4	const corsHeaders = {
> 5	  "Access-Control-Allow-Origin": "*",
> 6	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 7	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-user-token, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version",
> 8	};
> 9	
> 10	Deno.serve(async (req) => {
> 11	  if (req.method === "OPTIONS") {
> 12	    return new Response("ok", { headers: corsHeaders });
> 13	  }
> 14	
> 15	  try {
> 16	    const authHeader = req.headers.get("Authorization");
> 17	    if (!authHeader?.startsWith("Bearer ")) {
> 18	      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 19	        status: 401,
> 20	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 21	      });
> 22	    }
> 23	
> 24	    const body = await req.json();
> 25	    const { platform, content, social_account_id, scheduled_post_id, user_id: bodyUserId } = body;
> 26	
> 27	    if (!platform || !content) {
> 28	      return new Response(JSON.stringify({ error: "platform and content required" }), {
> 29	        status: 400,
> 30	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 31	      });
> 32	    }
> 33	
> 34	    const adminClient = createClient(
> 35	      Deno.env.get("SUPABASE_URL")!,
> 36	      (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!
> 37	    );
> 38	
> 39	    const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 40	    const isServiceRole = authHeader === `Bearer ${serviceKey}`;
> 41	
> 42	    // Resolve caller identity:
> 43	    // - User JWT (frontend): auth.getUser() returns a user
> 44	    // - Service role (auto-publish cron): auth.getUser() returns null; trust user_id from body
> 45	    //   since Supabase infrastructure already validated the JWT signature
> 46	    const supabase = createClient(
> 47	      Deno.env.get("SUPABASE_URL")!,
> 48	      (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!,
> 49	      { global: { headers: { Authorization: authHeader } } }
> 50	    );
> 51	    const { data: { user } } = await supabase.auth.getUser();
> 52	
> 53	    let userId: string;
> 54	    if (user) {
> 55	      userId = user.id;
> 56	    } else if (isServiceRole && bodyUserId) {
> 57	      userId = bodyUserId;
> 58	    } else {
> 59	      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 60	        status: 401,
> 61	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 62	      });
> 63	    }
> 64	
> 65	    let query = adminClient
> 66	      .from("decrypted_social_accounts")
> 67	      .select("*")
> 68	      .eq("user_id", userId)
> 69	      .eq("platform", platform)
> 70	      .eq("is_active", true);
> 71	
> 72	    if (social_account_id) query = query.eq("id", social_account_id);
> 73	
> 74	    const { data: accounts, error: accError } = await query.limit(1).single();
> 75	    if (accError || !accounts) {
> 76	      return new Response(JSON.stringify({ error: `No active ${platform} account found` }), {
> 77	        status: 404,
> 78	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 79	      });
> 80	    }
> 81	
> 82	    const account = accounts;
> 83	
> 84	    // Refresh token if expired, then re-fetch account to get the new access_token
> 85	    if (account.token_expires_at && new Date(account.token_expires_at) < new Date()) {
> 86	      const refreshRes = await fetch(`${Deno.env.get("SUPABASE_URL")}/functions/v1/refresh-social-token`, {
> 87	        method: "POST",
> 88	        headers: {
> 89	          "Content-Type": "application/json",
> 90	          Authorization: `Bearer ${(Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))}`,
> 91	        },
> 92	        body: JSON.stringify({ social_account_id: account.id }),
> 93	      });
> 94	      if (!refreshRes.ok) {
> 95	        return new Response(JSON.stringify({ error: "Token expired and refresh failed" }), {
> 96	          status: 401,
> 97	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 98	        });
> 99	      }
> 100	      // refresh-social-token updates the DB but does not return the token;
> 101	      // re-fetch to get the updated access_token
> 102	      const { data: refreshedAccount } = await adminClient
> 103	        .from("decrypted_social_accounts")
> 104	        .select("access_token, refresh_token, token_expires_at")
> 105	        .eq("id", account.id)
> 106	        .single();
> 107	      if (refreshedAccount) {
> 108	        account.access_token = refreshedAccount.access_token;
> 109	        account.token_expires_at = refreshedAccount.token_expires_at;
> 110	      }
> 111	    }
> 112	
> 113	    let result: any;
> 114	
> 115	    // Best-effort materiality telemetry (Lei 1 / FR-PE-016) — fire-and-forget so a logging hiccup
> 116	    // never blocks a publish. Mirrors the publish-meta pulse pattern (service='publish-<platform>').
> 117	    const pulse = (status: "ok" | "degraded" | "error", event?: string, metadata?: Record<string, unknown>) =>
> 118	      adminClient
> 119	        .from("infra_health_logs")
> 120	        .insert({ service: `publish-${platform}`, status, event: event ?? null, metadata: metadata ?? {} })
> 121	        .then(() => {}, () => {});
> 122	
> 123	    if (platform === "linkedin") {
> 124	      // FR-SPACES-082 (Amendment 24) — image attach: w_member_social ALREADY covers the assets API, so when the
> 125	      // pipeline hands us an image_url (a fresh owner-scoped signed URL from auto-publish) we register + upload
> 126	      // the bytes and publish shareMediaCategory IMAGE. No image_url → text-only ugcPost, byte-identical to before.
> 127	      const liHeaders = {
> 128	        Authorization: `Bearer ${account.access_token}`,
> 129	        "Content-Type": "application/json",
> 130	        "X-Restli-Protocol-Version": "2.0.0",
> 131	      };
> 132	      const authorUrn = `urn:li:person:${account.platform_user_id}`;
> 133	      let liMedia: { status: string; media: string }[] | null = null;
> 134	      if (typeof content.image_url === "string" && content.image_url) {
> 135	        const regRes = await fetch("https://api.linkedin.com/v2/assets?action=registerUpload", {
> 136	          method: "POST", headers: liHeaders,
> 137	          body: JSON.stringify({
> 138	            registerUploadRequest: {
> 139	              recipes: ["urn:li:digitalmediaRecipe:feedshare-image"],
> 140	              owner: authorUrn,
> 141	              serviceRelationships: [{ relationshipType: "OWNER", identifier: "urn:li:userGeneratedContent" }],
> 142	            },
> 143	          }),
> 144	        });
> 145	        const reg = await regRes.json().catch(() => ({}));
> 146	        const uploadUrl = reg?.value?.uploadMechanism?.["com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest"]?.uploadUrl;
> 147	        const assetUrn = reg?.value?.asset;
> 148	        if (!regRes.ok || !uploadUrl || !assetUrn) {
> 149	          console.error("LinkedIn registerUpload error:", regRes.status, reg);
> 150	          pulse("error", "linkedin_image_register_failed", { status: regRes.status });
> 151	          throw new Error("PLATFORM_PUBLISH_FAILED");
> 152	        }
> 153	        const imgRes = await fetch(content.image_url);
> 154	        if (!imgRes.ok) { pulse("error", "linkedin_image_fetch_failed", { status: imgRes.status }); throw new Error("PLATFORM_PUBLISH_FAILED"); }
> 155	        const putRes = await fetch(uploadUrl, {
> 156	          method: "PUT",
> 157	          headers: { Authorization: `Bearer ${account.access_token}` },
> 158	          body: new Uint8Array(await imgRes.arrayBuffer()),
> 159	        });
> 160	        if (!putRes.ok) {
> 161	          console.error("LinkedIn asset upload error:", putRes.status);
> 162	          pulse("error", "linkedin_image_upload_failed", { status: putRes.status });
> 163	          throw new Error("PLATFORM_PUBLISH_FAILED");
> 164	        }
> 165	        liMedia = [{ status: "READY", media: assetUrn }];
> 166	        pulse("ok", "linkedin_image_uploaded");
> 167	      }
> 168	      const res = await fetch("https://api.linkedin.com/v2/ugcPosts", {
> 169	        method: "POST",
> 170	        headers: liHeaders,
> 171	        body: JSON.stringify({
> 172	          author: authorUrn,
> 173	          lifecycleState: "PUBLISHED",
> 174	          specificContent: {
> 175	            "com.linkedin.ugc.ShareContent": {
> 176	              shareCommentary: { text: content.text || content },
> 177	              shareMediaCategory: liMedia ? "IMAGE" : "NONE",
> 178	              ...(liMedia ? { media: liMedia } : {}),
> 179	            },
> 180	          },
> 181	          visibility: { "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC" },
> 182	        }),
> 183	      });
> 184	      result = await res.json();
> 185	      if (!res.ok) {
> 186	        console.error("LinkedIn publish error:", res.status, result);
> 187	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 188	      }
> 189	
> 190	    } else if (platform === "instagram") {
> 191	      // Instagram Business Login token (instagram_business_content_publish) publishes via graph.INSTAGRAM.com —
> 192	      // NOT graph.facebook.com (that base needs a Page token). video_url → REELS (Fatia 2: vídeo do ecossistema
> 193	      // vira Reel pela conexão IG que JÁ existe — sem app/token manual).
> 194	      const IG_BASE = "https://graph.instagram.com/v21.0";
> 195	      // The stored platform_user_id can be an app-scoped id that the publishing endpoint rejects (code 100/33).
> 196	      // The token's own /me?fields=user_id is the correct content-publishing id — resolve it at publish time.
> 197	      const meRes = await fetch(`${IG_BASE}/me?fields=user_id&access_token=${account.access_token}`);
> 198	      const me = await meRes.json().catch(() => ({}));
> 199	      const igAccountId = me.user_id ?? account.platform_user_id;
> 200	      // video-repurpose Fatia 3 — a SET of images → a native CAROUSEL post (media_type=CAROUSEL): N child image
> 201	      // containers (is_carousel_item) → one parent container(children) → media_publish. Meta docs: ≤10 children.
> 202	      const carouselImages = Array.isArray(content.images)
> 203	        ? (content.images as unknown[]).filter((u): u is string => typeof u === "string").slice(0, 10)
> 204	        : [];
> 205	      if (carouselImages.length >= 2) {
> 206	        const childIds: string[] = [];
> 207	        for (const imageUrl of carouselImages) {
> 208	          const chRes = await fetch(`${IG_BASE}/${igAccountId}/media`, {
> 209	            method: "POST", headers: { "Content-Type": "application/json" },
> 210	            body: JSON.stringify({ image_url: imageUrl, is_carousel_item: true, access_token: account.access_token }),
> 211	          });
> 212	          const ch = await chRes.json();
> 213	          if (!chRes.ok || !ch.id) { console.error("IG carousel child error:", chRes.status, ch); throw new Error("PLATFORM_PUBLISH_FAILED"); }
> 214	          childIds.push(ch.id);
> 215	        }
> 216	        const parentRes = await fetch(`${IG_BASE}/${igAccountId}/media`, {
> 217	          method: "POST", headers: { "Content-Type": "application/json" },
> 218	          body: JSON.stringify({ media_type: "CAROUSEL", children: childIds.join(","), caption: content.text || "", access_token: account.access_token }),
> 219	        });
> 220	        const parent = await parentRes.json();
> 221	        if (!parentRes.ok || !parent.id) { console.error("IG carousel parent error:", parentRes.status, parent); throw new Error("PLATFORM_PUBLISH_FAILED"); }
> 222	        const pubRes = await fetch(`${IG_BASE}/${igAccountId}/media_publish`, {
> 223	          method: "POST", headers: { "Content-Type": "application/json" },
> 224	          body: JSON.stringify({ creation_id: parent.id, access_token: account.access_token }),
> 225	        });
> 226	        result = await pubRes.json();
> 227	        if (!pubRes.ok) { console.error("Instagram carousel publish error:", pubRes.status, result); throw new Error("PLATFORM_PUBLISH_FAILED"); }
> 228	      } else {
> 229	      const videoUrl = content.video_url;
> 230	      // FR-SPACES-083 (Amendment 24) — IG STORIES: same container→publish flow, media_type=STORIES; the surface
> 231	      // discriminator rides content.surface (copied server-side by auto-publish from the reshape row, never a
> 232	      // trusted asset ref). Stories carry no caption (the API ignores it). Covered by the SAME scope
> 233	      // (instagram_business_content_publish) — reach stays gated on the Meta app audit like the whole IG rail.
> 234	      // catalog (format-specs) says "story"; seed/channel naming elsewhere says "stories" — accept both.
> 235	      const isStory = (content.surface === "story" || content.surface === "stories") && (videoUrl || content.image_url);
> 236	      const createRes = await fetch(
> 237	        `${IG_BASE}/${igAccountId}/media`,
> 238	        {
> 239	          method: "POST",
> 240	          headers: { "Content-Type": "application/json" },
> 241	          body: JSON.stringify(
> 242	            isStory
> 243	              ? { media_type: "STORIES", ...(videoUrl ? { video_url: videoUrl } : { image_url: content.image_url }), access_token: account.access_token }
> 244	              : videoUrl
> 245	                ? { media_type: "REELS", video_url: videoUrl, caption: content.text || content, access_token: account.access_token }
> 246	                : { caption: content.text || content, image_url: content.image_url, access_token: account.access_token },
> 247	          ),
> 248	        }
> 249	      );
> 250	      const container = await createRes.json();
> 251	      if (!createRes.ok) {
> 252	        console.error("Instagram media create error:", createRes.status, container);
> 253	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 254	      }
> 255	
> 256	      // REELS transcode is async — poll the container until FINISHED before publishing (≤ ~90s; short clips finish fast).
> 257	      if (videoUrl) {
> 258	        for (let i = 0; i < 30; i++) {
> 259	          const st = await fetch(`${IG_BASE}/${container.id}?fields=status_code&access_token=${account.access_token}`);
> 260	          const stData = await st.json().catch(() => ({}));
> 261	          if (stData.status_code === "FINISHED") break;
> 262	          if (stData.status_code === "ERROR") throw new Error("IG_REELS_CONTAINER_ERROR");
> 263	          await new Promise((r) => setTimeout(r, 3000));
> 264	        }
> 265	      }
> 266	
> 267	      const pubRes = await fetch(
> 268	        `${IG_BASE}/${igAccountId}/media_publish`,
> 269	        {
> 270	          method: "POST",
> 271	          headers: { "Content-Type": "application/json" },
> 272	          body: JSON.stringify({
> 273	            creation_id: container.id,
> 274	            access_token: account.access_token,
> 275	          }),
> 276	        }
> 277	      );
> 278	      result = await pubRes.json();
> 279	      if (!pubRes.ok) {
> 280	        console.error("Instagram publish error:", pubRes.status, result);
> 281	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 282	      }
> 283	      }
> 284	
> 285	    } else if (platform === "facebook") {
> 286	      // CP-010 — image (link_card surface → Page photo) OR text feed. FB Reels video is deferred (OTD-CP-010).
> 287	      const pageId = account.platform_user_id;
> 288	      const message = (typeof content === "object" ? content.text : content) || "";
> 289	      if (content.image_url) {
> 290	        // Page photo post: Facebook fetches the (public/signed) image URL.
> 291	        const res = await fetch(`https://graph.facebook.com/v19.0/${pageId}/photos`, {
> 292	          method: "POST",
> 293	          headers: { "Content-Type": "application/json" },
> 294	          body: JSON.stringify({ url: content.image_url, caption: message, access_token: account.access_token }),
> 295	        });
> 296	        result = await res.json();
> 297	        if (!res.ok) { console.error("Facebook photo error:", res.status, result); pulse("error", "facebook_photo_failed", { status: res.status }); throw new Error("PLATFORM_PUBLISH_FAILED"); }
> 298	        pulse("ok", "facebook_photo_published", { post_id: result?.id ?? null });
> 299	      } else {
> 300	        const res = await fetch(`https://graph.facebook.com/v19.0/${pageId}/feed`, {
> 301	          method: "POST",
> 302	          headers: { "Content-Type": "application/json" },
> 303	          body: JSON.stringify({ message, access_token: account.access_token }),
> 304	        });
> 305	        result = await res.json();
> 306	        if (!res.ok) { console.error("Facebook publish error:", res.status, result); throw new Error("PLATFORM_PUBLISH_FAILED"); }
> 307	      }
> 308	
> 309	    } else if (platform === "twitter") {
> 310	      // CP-010 — native THREAD (reply chain) when content.thread[] is present; else a single tweet. X video deferred.
> 311	      const xHeaders = { Authorization: `Bearer ${account.access_token}`, "Content-Type": "application/json" };
> 312	      const thread = Array.isArray(content.thread)
> 313	        ? content.thread.filter((t: unknown) => typeof t === "string" && t.trim()).map((t: string) => t.slice(0, 280))
> 314	        : null;
> 315	      if (thread && thread.length > 1) {
> 316	        let prevId: string | null = null;
> 317	        const ids: string[] = [];
> 318	        for (const tw of thread) {
> 319	          const body: Record<string, unknown> = { text: tw };
> 320	          if (prevId) body.reply = { in_reply_to_tweet_id: prevId };
> 321	          const res = await fetch("https://api.x.com/2/tweets", { method: "POST", headers: xHeaders, body: JSON.stringify(body) });
> 322	          const j = await res.json().catch(() => ({}));
> 323	          if (!res.ok) {
> 324	            console.error("X thread tweet error:", res.status, j);
> 325	            if (!prevId) { pulse("error", "twitter_thread_failed", { status: res.status }); throw new Error("PLATFORM_PUBLISH_FAILED"); }
> 326	            break; // first tweet anchored the thread; a later failure truncates but does not fail the post
> 327	          }
> 328	          prevId = j?.data?.id ?? null;
> 329	          if (prevId) ids.push(prevId);
> 330	        }
> 331	        result = { id: ids[0] ?? null, thread_ids: ids };
> 332	        pulse("ok", "twitter_thread_published", { tweets: ids.length });
> 333	      } else {
> 334	        // FR-SPACES-084 (Amendment 24) — image attach via media upload v2. Needs the media.write scope
> 335	        // (added to social-auth-init; PRE-EXISTING connections lack it → 403 here). Anti false-success:
> 336	        // a post promised WITH media never silently goes out text-only — we fail with an actionable error.
> 337	        let mediaIds: string[] | null = null;
> 338	        if (typeof content.image_url === "string" && content.image_url) {
> 339	          const imgRes = await fetch(content.image_url);
> 340	          if (!imgRes.ok) { pulse("error", "twitter_media_fetch_failed", { status: imgRes.status }); throw new Error("PLATFORM_PUBLISH_FAILED"); }
> 341	          const form = new FormData();
> 342	          form.append("media", await imgRes.blob());
> 343	          form.append("media_category", "tweet_image");
> 344	          const upRes = await fetch("https://api.x.com/2/media/upload", {
> 345	            method: "POST", headers: { Authorization: `Bearer ${account.access_token}` }, body: form,
> 346	          });
> 347	          const up = await upRes.json().catch(() => ({}));
> 348	          if (!upRes.ok) {
> 349	            console.error("X media upload error:", upRes.status, up);
> 350	            pulse("error", "twitter_media_upload_failed", { status: upRes.status });
> 351	            // 401/403 on upload with a valid tweet token ⇒ the token predates the media.write scope.
> 352	            if (upRes.status === 401 || upRes.status === 403) throw new Error("twitter_media_scope_missing: reconecte a conta X em /dashboard/settings para conceder media.write");
> 353	            throw new Error("PLATFORM_PUBLISH_FAILED");
> 354	          }
> 355	          const mediaId = up?.data?.id ?? up?.media_id_string ?? null;
> 356	          if (!mediaId) { pulse("error", "twitter_media_no_id"); throw new Error("PLATFORM_PUBLISH_FAILED"); }
> 357	          mediaIds = [String(mediaId)];
> 358	          pulse("ok", "twitter_media_uploaded");
> 359	        }
> 360	        const res = await fetch("https://api.x.com/2/tweets", {
> 361	          method: "POST", headers: xHeaders,
> 362	          body: JSON.stringify({
> 363	            text: (content.text || content)?.toString()?.slice(0, 280),
> 364	            ...(mediaIds ? { media: { media_ids: mediaIds } } : {}),
> 365	          }),
> 366	        });
> 367	        result = await res.json();
> 368	        if (!res.ok) { console.error("Twitter publish error:", res.status, result); throw new Error("PLATFORM_PUBLISH_FAILED"); }
> 369	      }
> 370	
> 371	    } else if (platform === "tiktok") {
> 372	      // TikTok Content Posting API — Direct Post, FILE_UPLOAD (the Supabase signed URL does NOT pass the
> 373	      // PULL_FROM_URL domain-ownership check, so we transfer the bytes ourselves). User access_token only —
> 374	      // publishing needs no client_secret. Mirrors the IG REELS create→poll→publish shape. video_url from payload.
> 375	      const TIKTOK_BASE = "https://open.tiktokapis.com";
> 376	      const videoUrl = content.video_url;
> 377	      if (!videoUrl) {
> 378	        pulse("degraded", "tiktok_no_video");
> 379	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 380	      }
> 381	
> 382	      // (1) Pre-flight creator_info — pick a privacy_level that the (possibly unaudited) account actually allows.
> 383	      const ciRes = await fetch(`${TIKTOK_BASE}/v2/post/publish/creator_info/query/`, {
> 384	        method: "POST",
> 385	        headers: {
> 386	          Authorization: `Bearer ${account.access_token}`,
> 387	          "Content-Type": "application/json; charset=UTF-8",
> 388	        },
> 389	      });
> 390	      const creatorInfo = await ciRes.json();
> 391	      if (!ciRes.ok) {
> 392	        console.error("TikTok creator_info error:", ciRes.status, creatorInfo);
> 393	        pulse("error", "tiktok_creator_info_failed", { status: ciRes.status });
> 394	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 395	      }
> 396	      const privacyOptions: string[] = creatorInfo?.data?.privacy_level_options ?? [];
> 397	      // Prefer public when available (post-audit). Otherwise an UNAUDITED client can ONLY post as
> 398	      // SELF_ONLY — TikTok rejects FOLLOWER_OF_CREATOR / MUTUAL_FOLLOW_FRIENDS with
> 399	      // `unaudited_client_can_only_post_to_private_accounts` (proven 2026-06-27). So fall back to
> 400	      // SELF_ONLY explicitly, NOT to privacyOptions[0] (which is FOLLOWER_OF_CREATOR on a private acct).
> 401	      const privacyLevel =
> 402	        privacyOptions.find((p) => p === "PUBLIC_TO_EVERYONE") ??
> 403	        privacyOptions.find((p) => p === "SELF_ONLY") ??
> 404	        privacyOptions[0] ??
> 405	        "SELF_ONLY";
> 406	
> 407	      // Fetch the MP4 bytes once (FILE_UPLOAD requires the exact size up-front).
> 408	      const mp4Res = await fetch(videoUrl);
> 409	      if (!mp4Res.ok) {
> 410	        console.error("TikTok video fetch error:", mp4Res.status);
> 411	        pulse("error", "tiktok_video_fetch_failed", { status: mp4Res.status });
> 412	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 413	      }
> 414	      const videoBytes = new Uint8Array(await mp4Res.arrayBuffer());
> 415	      const videoSize = videoBytes.byteLength;
> 416	      // Single-chunk transfer (HyperFrames clips are well under the 64MB chunk ceiling / <128MB final).
> 417	      const chunkSize = videoSize;
> 418	      const totalChunkCount = 1;
> 419	
> 420	      // IDEMPOTENCY NOTE: /video/init/ mints a fresh publish_id every call — re-running this branch on a
> 421	      // transient retry WITHOUT an external content/run-id guard would double-post. The caller is expected to
> 422	      // gate re-publish on scheduled_post_id/content state; do NOT re-init blindly inside a retry loop.
> 423	      const initRes = await fetch(`${TIKTOK_BASE}/v2/post/publish/video/init/`, {
> 424	        method: "POST",
> 425	        headers: {
> 426	          Authorization: `Bearer ${account.access_token}`,
> 427	          "Content-Type": "application/json; charset=UTF-8",
> 428	        },
> 429	        body: JSON.stringify({
> 430	          post_info: {
> 431	            title: (content.text || content)?.toString()?.slice(0, 2200) ?? "",
> 432	            privacy_level: privacyLevel,
> 433	            is_aigc: true, // AIGC disclosure is mandatory for AI-generated persona content (compliance).
> 434	          },
> 435	          source_info: {
> 436	            source: "FILE_UPLOAD",
> 437	            video_size: videoSize,
> 438	            chunk_size: chunkSize,
> 439	            total_chunk_count: totalChunkCount,
> 440	          },
> 441	        }),
> 442	      });
> 443	      const initData = await initRes.json();
> 444	      if (!initRes.ok || !initData?.data?.upload_url || !initData?.data?.publish_id) {
> 445	        console.error("TikTok init error:", initRes.status, initData);
> 446	        pulse("error", "tiktok_init_failed", { status: initRes.status });
> 447	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 448	      }
> 449	      const uploadUrl: string = initData.data.upload_url;
> 450	      const publishId: string = initData.data.publish_id;
> 451	
> 452	      // (3) PUT the bytes to the returned upload_url with a Content-Range (single chunk = whole file).
> 453	      const putRes = await fetch(uploadUrl, {
> 454	        method: "PUT",
> 455	        headers: {
> 456	          "Content-Type": "video/mp4",
> 457	          "Content-Range": `bytes 0-${videoSize - 1}/${videoSize}`,
> 458	        },
> 459	        body: videoBytes,
> 460	      });
> 461	      if (!putRes.ok) {
> 462	        console.error("TikTok upload PUT error:", putRes.status);
> 463	        pulse("error", "tiktok_upload_failed", { status: putRes.status });
> 464	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 465	      }
> 466	
> 467	      // (4) Poll status until PUBLISH_COMPLETE. publicaly_available_post_id may stay null pre-audit (SELF_ONLY).
> 468	      let publishStatus = "";
> 469	      let publicPostId: string | null = null;
> 470	      for (let i = 0; i < 30; i++) {
> 471	        const stRes = await fetch(`${TIKTOK_BASE}/v2/post/publish/status/fetch/`, {
> 472	          method: "POST",
> 473	          headers: {
> 474	            Authorization: `Bearer ${account.access_token}`,
> 475	            "Content-Type": "application/json; charset=UTF-8",
> 476	          },
> 477	          body: JSON.stringify({ publish_id: publishId }),
> 478	        });
> 479	        const stData = await stRes.json().catch(() => ({}));
> 480	        publishStatus = stData?.data?.status ?? "";
> 481	        const publicIds: string[] = stData?.data?.publicaly_available_post_id ?? [];
> 482	        if (publicIds.length) publicPostId = publicIds[0];
> 483	        if (publishStatus === "PUBLISH_COMPLETE") break;
> 484	        if (publishStatus === "FAILED") {
> 485	          console.error("TikTok publish failed:", stData?.data?.fail_reason, stData);
> 486	          pulse("error", "tiktok_publish_failed", { fail_reason: stData?.data?.fail_reason ?? null });
> 487	          throw new Error("PLATFORM_PUBLISH_FAILED");
> 488	        }
> 489	        await new Promise((r) => setTimeout(r, 3000));
> 490	      }
> 491	      if (publishStatus !== "PUBLISH_COMPLETE") {
> 492	        pulse("degraded", "tiktok_publish_timeout", { publish_id: publishId });
> 493	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 494	      }
> 495	      // Materiality (Lei 1): PUBLISH_COMPLETE proves transport; the public id is null until the account is
> 496	      // audited (SELF_ONLY) — that's expected and NOT a failure.
> 497	      result = { id: publicPostId, publish_id: publishId, status: publishStatus };
> 498	      pulse("ok", "tiktok_publish_complete", { publish_id: publishId, public: publicPostId !== null });
> 499	
> 500	    } else if (platform === "youtube") {
> 501	      // YouTube Data API v3 videos.insert — resumable upload (no remote ingest → fetch the signed bytes, then
> 502	      // PUT). User access_token only (publishing needs no client_secret). Shorts is implicit (9:16 + ≤3min).
> 503	      const videoUrl = content.video_url;
> 504	      if (!videoUrl) {
> 505	        pulse("degraded", "youtube_no_video");
> 506	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 507	      }
> 508	      const mp4Res = await fetch(videoUrl);
> 509	      if (!mp4Res.ok) {
> 510	        console.error("YouTube video fetch error:", mp4Res.status);
> 511	        pulse("error", "youtube_video_fetch_failed", { status: mp4Res.status });
> 512	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 513	      }
> 514	      const videoBytes = new Uint8Array(await mp4Res.arrayBuffer());
> 515	      const videoSize = videoBytes.byteLength;
> 516	
> 517	      // (1) Initiate the resumable session.
> 518	      const initRes = await fetch(
> 519	        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
> 520	        {
> 521	          method: "POST",
> 522	          headers: {
> 523	            Authorization: `Bearer ${account.access_token}`,
> 524	            "Content-Type": "application/json; charset=UTF-8",
> 525	            "X-Upload-Content-Length": String(videoSize),
> 526	            "X-Upload-Content-Type": "video/mp4",
> 527	          },
> 528	          body: JSON.stringify({
> 529	            snippet: {
> 530	              title: (content.text || content)?.toString()?.slice(0, 100) || "Gabriel AI",
> 531	              description: typeof content === "object" && content?.text ? String(content.text) : "",
> 532	              categoryId: "22",
> 533	            },
> 534	            status: {
> 535	              privacyStatus: "public",
> 536	              selfDeclaredMadeForKids: false,
> 537	              containsSyntheticMedia: true, // AIGC disclosure is mandatory for AI-generated content (compliance).
> 538	            },
> 539	          }),
> 540	        }
> 541	      );
> 542	      if (!initRes.ok) {
> 543	        const initErr = await initRes.json().catch(() => ({}));
> 544	        console.error("YouTube resumable init error:", initRes.status, initErr);
> 545	        pulse("error", "youtube_init_failed", { status: initRes.status });
> 546	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 547	      }
> 548	      // (2) Capture the session URI from the Location header.
> 549	      const sessionUri = initRes.headers.get("Location");
> 550	      if (!sessionUri) {
> 551	        pulse("error", "youtube_no_session_uri");
> 552	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 553	      }
> 554	
> 555	      // (3) PUT the bytes to the session URI.
> 556	      const putRes = await fetch(sessionUri, {
> 557	        method: "PUT",
> 558	        headers: { "Content-Type": "video/mp4", "Content-Length": String(videoSize) },
> 559	        body: videoBytes,
> 560	      });
> 561	      const putData = await putRes.json().catch(() => ({}));
> 562	      // (4) Success = 201 with the video resource id.
> 563	      if (putRes.status !== 200 && putRes.status !== 201) {
> 564	        console.error("YouTube upload PUT error:", putRes.status, putData);
> 565	        pulse("error", "youtube_upload_failed", { status: putRes.status });
> 566	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 567	      }
> 568	      const videoId: string | undefined = putData?.id;
> 569	      if (!videoId) {
> 570	        pulse("error", "youtube_no_video_id");
> 571	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 572	      }
> 573	
> 574	      // Materiality (Lei 1): a 201 does NOT mean public — an unaudited project FORCES the upload to private,
> 575	      // ignoring the requested privacyStatus. Read back the REAL status; never assume 'public'.
> 576	      let realPrivacyStatus: string | null = null;
> 577	      const statusRes = await fetch(
> 578	        `https://www.googleapis.com/youtube/v3/videos?id=${videoId}&part=status`,
> 579	        { headers: { Authorization: `Bearer ${account.access_token}` } }
> 580	      );
> 581	      const statusData = await statusRes.json().catch(() => ({}));
> 582	      realPrivacyStatus = statusData?.items?.[0]?.status?.privacyStatus ?? null;
> 583	
> 584	      result = { id: videoId, privacyStatus: realPrivacyStatus };
> 585	      pulse("ok", "youtube_upload_complete", { video_id: videoId, privacy_status: realPrivacyStatus });
> 586	
> 587	    } else if (platform === "pinterest") {
> 588	      // Pinterest API v5 — video pin (register → upload multipart → poll → create). User access_token only for
> 589	      // pin/board/media REST; the multipart upload itself carries NO Authorization (presigned S3 POST). video_url
> 590	      // from payload; cover_image_url must be a PUBLIC https URL (Pinterest fetches it async).
> 591	      const PIN_BASE = "https://api.pinterest.com/v5";
> 592	      const videoUrl = content.video_url;
> 593	      if (!videoUrl && !content.image_url) {
> 594	        pulse("degraded", "pinterest_no_media");
> 595	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 596	      }
> 597	      const pinHeaders = {
> 598	        Authorization: `Bearer ${account.access_token}`,
> 599	        "Content-Type": "application/json",
> 600	      };
> 601	
> 602	      // (0) Ensure a destination board — prefer a cached metadata.board_id, else the first existing board, else
> 603	      // create one once. (Do NOT create a board per run.)
> 604	      let boardId: string | null = account.metadata?.board_id ?? null;
> 605	      if (!boardId) {
> 606	        const boardsRes = await fetch(`${PIN_BASE}/boards`, { headers: pinHeaders });
> 607	        const boardsData = await boardsRes.json().catch(() => ({}));
> 608	        if (!boardsRes.ok) {
> 609	          console.error("Pinterest boards list error:", boardsRes.status, boardsData);
> 610	          pulse("error", "pinterest_boards_failed", { status: boardsRes.status });
> 611	          throw new Error("PLATFORM_PUBLISH_FAILED");
> 612	        }
> 613	        boardId = boardsData?.items?.[0]?.id ?? null;
> 614	        if (!boardId) {
> 615	          const createBoardRes = await fetch(`${PIN_BASE}/boards`, {
> 616	            method: "POST",
> 617	            headers: pinHeaders,
> 618	            body: JSON.stringify({ name: "Gabriel AI", privacy: "PUBLIC" }),
> 619	          });
> 620	          const createBoardData = await createBoardRes.json().catch(() => ({}));
> 621	          if (!createBoardRes.ok || !createBoardData?.id) {
> 622	            console.error("Pinterest board create error:", createBoardRes.status, createBoardData);
> 623	            pulse("error", "pinterest_board_create_failed", { status: createBoardRes.status });
> 624	            throw new Error("PLATFORM_PUBLISH_FAILED");
> 625	          }
> 626	          boardId = createBoardData.id;
> 627	        }
> 628	      }
> 629	
> 630	      if (videoUrl) {
> 631	      // (1) Register the media upload → media_id + upload_url + upload_parameters.
> 632	      const mediaRes = await fetch(`${PIN_BASE}/media`, {
> 633	        method: "POST",
> 634	        headers: pinHeaders,
> 635	        body: JSON.stringify({ media_type: "video" }),
> 636	      });
> 637	      const mediaData = await mediaRes.json().catch(() => ({}));
> 638	      if (!mediaRes.ok || !mediaData?.media_id || !mediaData?.upload_url) {
> 639	        console.error("Pinterest media register error:", mediaRes.status, mediaData);
> 640	        pulse("error", "pinterest_media_register_failed", { status: mediaRes.status });
> 641	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 642	      }
> 643	      const mediaId: string = mediaData.media_id;
> 644	      const uploadUrl: string = mediaData.upload_url;
> 645	      const uploadParams: Record<string, string> = mediaData.upload_parameters ?? {};
> 646	
> 647	      // (2) POST the MP4 to upload_url as multipart/form-data — ALL upload_parameters VERBATIM and the file LAST,
> 648	      // with NO Authorization header (presigned POST). Success = 204.
> 649	      const mp4Res = await fetch(videoUrl);
> 650	      if (!mp4Res.ok) {
> 651	        console.error("Pinterest video fetch error:", mp4Res.status);
> 652	        pulse("error", "pinterest_video_fetch_failed", { status: mp4Res.status });
> 653	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 654	      }
> 655	      const videoBlob = await mp4Res.blob();
> 656	      const form = new FormData();
> 657	      for (const [k, v] of Object.entries(uploadParams)) form.append(k, v);
> 658	      form.append("file", videoBlob); // file field MUST be last (presigned-POST ordering).
> 659	      const uploadRes = await fetch(uploadUrl, { method: "POST", body: form });
> 660	      if (uploadRes.status !== 204 && !uploadRes.ok) {
> 661	        console.error("Pinterest media upload error:", uploadRes.status);
> 662	        pulse("error", "pinterest_upload_failed", { status: uploadRes.status });
> 663	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 664	      }
> 665	
> 666	      // (3) Poll the media until status='succeeded'.
> 667	      let mediaStatus = "";
> 668	      for (let i = 0; i < 30; i++) {
> 669	        const stRes = await fetch(`${PIN_BASE}/media/${mediaId}`, { headers: pinHeaders });
> 670	        const stData = await stRes.json().catch(() => ({}));
> 671	        mediaStatus = stData?.status ?? "";
> 672	        if (mediaStatus === "succeeded") break;
> 673	        if (mediaStatus === "failed") {
> 674	          console.error("Pinterest media processing failed:", stData);
> 675	          pulse("error", "pinterest_media_failed", { media_id: mediaId });
> 676	          throw new Error("PLATFORM_PUBLISH_FAILED");
> 677	        }
> 678	        await new Promise((r) => setTimeout(r, 3000));
> 679	      }
> 680	      if (mediaStatus !== "succeeded") {
> 681	        pulse("degraded", "pinterest_media_timeout", { media_id: mediaId });
> 682	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 683	      }
> 684	
> 685	      // (4) Create the pin. cover_image_url must be a PUBLIC https URL (Pinterest fetches it async).
> 686	      const coverImageUrl = content.cover_image_url || content.image_url || videoUrl;
> 687	      const pinRes = await fetch(`${PIN_BASE}/pins`, {
> 688	        method: "POST",
> 689	        headers: pinHeaders,
> 690	        body: JSON.stringify({
> 691	          board_id: boardId,
> 692	          title: (content.text || content)?.toString()?.slice(0, 100) ?? "",
> 693	          description: typeof content === "object" && content?.text ? String(content.text).slice(0, 800) : "",
> 694	          media_source: {
> 695	            source_type: "video_id",
> 696	            media_id: mediaId,
> 697	            cover_image_url: coverImageUrl,
> 698	          },
> 699	        }),
> 700	      });
> 701	      result = await pinRes.json();
> 702	      if (!pinRes.ok) {
> 703	        console.error("Pinterest pin create error:", pinRes.status, result);
> 704	        pulse("error", "pinterest_pin_create_failed", { status: pinRes.status });
> 705	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 706	      }
> 707	      // Materiality (Lei 1): under Trial the pin is sandbox/creator-only (no public URL) — a 201 proves
> 708	      // transport, not live reach. Honest 'live' claim waits for Standard tier.
> 709	      pulse("ok", "pinterest_pin_created", { pin_id: result?.id ?? null, board_id: boardId });
> 710	      } else {
> 711	        // CP-010 — standard IMAGE pin (standard_pin surface): Pinterest fetches the public/signed image URL async.
> 712	        const pinRes = await fetch(`${PIN_BASE}/pins`, {
> 713	          method: "POST", headers: pinHeaders,
> 714	          body: JSON.stringify({
> 715	            board_id: boardId,
> 716	            title: (content.text || content)?.toString()?.slice(0, 100) ?? "",
> 717	            description: typeof content === "object" && content?.text ? String(content.text).slice(0, 800) : "",
> 718	            media_source: { source_type: "image_url", url: content.image_url },
> 719	          }),
> 720	        });
> 721	        result = await pinRes.json();
> 722	        if (!pinRes.ok) { console.error("Pinterest image pin error:", pinRes.status, result); pulse("error", "pinterest_image_pin_failed", { status: pinRes.status }); throw new Error("PLATFORM_PUBLISH_FAILED"); }
> 723	        pulse("ok", "pinterest_image_pin_created", { pin_id: result?.id ?? null, board_id: boardId });
> 724	      }
> 725	
> 726	    } else {
> 727	      return new Response(JSON.stringify({ error: `Publishing to ${platform} not yet supported` }), {
> 728	        status: 400,
> 729	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 730	      });
> 731	    }
> 732	
> 733	    if (scheduled_post_id) {
> 734	      await adminClient
> 735	        .from("scheduled_posts")
> 736	        .update({
> 737	          status: "published",
> 738	          published_at: new Date().toISOString(),
> 739	          platform_post_id: result.id || result.data?.id || result["X-RestLi-Id"],
> 740	        })
> 741	        .eq("id", scheduled_post_id);
> 742	    }
> 743	
> 744	    // In-app notification (best-effort) — the user sees publishes in the bell (P0 notifications).
> 745	    const platformLabel = platform === "instagram" ? "Instagram" : platform === "linkedin" ? "LinkedIn" : platform;
> 746	    await notify(adminClient, userId, {
> 747	      type: "success",
> 748	      title: `Publicado no ${platformLabel}`,
> 749	      message: typeof content === "object" && content?.text ? String(content.text).slice(0, 120) : null,
> 750	      action_url: "/dashboard/social",
> 751	      metadata: { platform, post_id: result?.id ?? null },
> 752	    });
> 753	
> 754	    return new Response(JSON.stringify({ success: true, result }), {
> 755	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 756	    });
> 757	  } catch (err) {
> 758	    console.error("publish-social error:", err);
> 759	    return new Response(
> 760	      JSON.stringify({ error: "Falha ao publicar. Tente novamente em instantes." }),
> 761	      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
> 762	    );
> 763	  }
> 764	});
> 765	
> ```

## 🤖 Claude *(13:25:34)*


## 🤖 Claude *(13:25:35)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/auto-publish/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 2	
> 3	const corsHeaders = {
> 4	  "Access-Control-Allow-Origin": "*",
> 5	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 6	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-user-token",
> 7	};
> 8	
> 9	Deno.serve(async (req) => {
> 10	  if (req.method === "OPTIONS") {
> 11	    return new Response("ok", { headers: corsHeaders });
> 12	  }
> 13	
> 14	  try {
> 15	    const adminClient = createClient(
> 16	      Deno.env.get("SUPABASE_URL")!,
> 17	      (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!
> 18	    );
> 19	
> 20	    // Find all queued posts where scheduled_at <= now
> 21	    const { data: duePosts, error } = await adminClient
> 22	      .from("scheduled_posts")
> 23	      .select("*")
> 24	      .eq("status", "queued")
> 25	      .lte("scheduled_at", new Date().toISOString())
> 26	      .order("scheduled_at")
> 27	      .limit(50);
> 28	
> 29	    if (error) {
> 30	      console.error("Error fetching due posts:", error);
> 31	      return new Response(JSON.stringify({ error: error.message }), {
> 32	        status: 500,
> 33	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 34	      });
> 35	    }
> 36	
> 37	    if (!duePosts || duePosts.length === 0) {
> 38	      return new Response(JSON.stringify({ processed: 0, message: "No posts due" }), {
> 39	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 40	      });
> 41	    }
> 42	
> 43	    const results: Array<{ id: string; status: string; error?: string }> = [];
> 44	
> 45	    for (const post of duePosts) {
> 46	      try {
> 47	        // Mark as publishing
> 48	        await adminClient
> 49	          .from("scheduled_posts")
> 50	          .update({ status: "publishing" })
> 51	          .eq("id", post.id);
> 52	
> 53	        // Get the content body if content_id exists
> 54	        let contentText = "";
> 55	        if (post.content_id) {
> 56	          const { data: content } = await adminClient
> 57	            .from("content_library")
> 58	            .select("body, title")
> 59	            .eq("id", post.content_id)
> 60	            .single();
> 61	          contentText = content?.body || content?.title || "";
> 62	        }
> 63	
> 64	        if (!contentText) {
> 65	          contentText = `Post agendado para ${post.platform}`;
> 66	        }
> 67	
> 68	        // ── FR-PE-011: video transport gap. The scheduled post's content_id points at the TEXT row; the 9:16 render
> 69	        // (video-bridge.ts) lands as a SEPARATE content_library row (type='video', media_url = a path inside the
> 70	        // private `video-studio-assets` bucket — metadata.storage_bucket) sharing this post's campaign_id. Resolve
> 71	        // that sibling and sign it to a LONG-TTL URL so the URL survives Pinterest/IG's async fetch (a 1h signed URL
> 72	        // dies before the publish window). Pass it as content.video_url → publish-social's REELS/TikTok/YouTube/Pin
> 73	        // video branches. Text-only posts keep the plain-string path UNCHANGED (no campaign_id / no video sibling).
> 74	        let videoUrl: string | null = null;
> 75	        if (post.campaign_id) {
> 76	          try {
> 77	            const { data: vid } = await adminClient
> 78	              .from("content_library")
> 79	              .select("media_url, metadata")
> 80	              .eq("campaign_id", post.campaign_id)
> 81	              .eq("type", "video")
> 82	              .eq("status", "approved")
> 83	              .order("created_at", { ascending: false })
> 84	              .limit(1)
> 85	              .maybeSingle();
> 86	            const storageKey = vid?.media_url as string | undefined;
> 87	            if (storageKey) {
> 88	              const bucket = (vid?.metadata as { storage_bucket?: string } | null)?.storage_bucket || "video-studio-assets";
> 89	              if (/^https?:\/\//i.test(storageKey)) {
> 90	                videoUrl = storageKey; // already a public URL — pass through
> 91	              } else {
> 92	                // 6h TTL — outlives the async pull (cover/video fetch) on Pinterest/IG. Private bucket → re-sign on read.
> 93	                const { data: signed } = await adminClient.storage
> 94	                  .from(bucket)
> 95	                  .createSignedUrl(storageKey, 21600);
> 96	                videoUrl = signed?.signedUrl ?? null;
> 97	              }
> 98	            }
> 99	          } catch (e) {
> 100	            console.warn(`[auto-publish] video_url resolve skipped for post ${post.id}:`, e instanceof Error ? e.message : e);
> 101	          }
> 102	        }
> 103	
> 104	        // ── FR-CP-003 — prefer the reshaper's NATIVE variant over the generic derivation. ──
> 105	        // SECURITY (FMEA-011): the asset ref is NEVER trusted from scheduled_posts.metadata (a user can write their
> 106	        // OWN scheduled_posts.metadata, so signing a bucket/key from it with the service key would read ANY tenant's
> 107	        // private object). Instead resolve it from the server-trusted channel_variants row, filtered by the post's
> 108	        // OWNER (post.user_id) — that row is written service-role-only by the reshaper under the correct user_id.
> 109	        // Signing the per-row asset key HERE (fresh 6h URL) also fixes auto-publish's single-video-per-campaign
> 110	        // collision. SSOT: docs/bok/post-engine/13-sdd-reshaper-atomizer.md §5.3. Falls back to legacy when absent.
> 111	        let contentPayload: unknown = videoUrl ? { text: contentText, video_url: videoUrl } : contentText;
> 112	        const reshape = (post.metadata as { reshape?: { content?: Record<string, unknown>; channel_variant_id?: string; space_publish_variant_id?: string; carousel_render_id?: string } } | null)?.reshape;
> 113	        if (reshape?.content) {
> 114	          const c = reshape.content;
> 115	          const native: Record<string, unknown> = { text: typeof c.text === "string" ? c.text : contentText };
> 116	          // FR-SPACES-083 — surface discriminator (plain string, e.g. 'stories'): lets publish-social pick the
> 117	          // right IG media_type. Metadata-borne but INERT (it selects a container type, never an asset ref).
> 118	          if (typeof c.surface === "string") native.surface = c.surface.slice(0, 60);
> 119	          // Attach the per-row asset ref resolved from an OWNER-SCOPED ledger row (server-trusted), NEVER from metadata.
> 120	          const attachAsset = async (bucket?: string, key?: string, kind?: string) => {
> 121	            if (!bucket || !key) return;
> 122	            let url: string | null = null;
> 123	            if (/^https?:\/\//i.test(key)) url = key;
> 124	            else { const { data: signed } = await adminClient.storage.from(bucket).createSignedUrl(key, 21600); url = signed?.signedUrl ?? null; }
> 125	            if (url) { if (kind === "video") native.video_url = url; else if (kind === "image") native.image_url = url; }
> 126	          };
> 127	          // FR-SPACES-079 (Amendment 22 — closes OTD-SPACES-044): scheduled IG CAROUSEL. carousel_render_id is a
> 128	          // GROUP MARKER, never an asset ref (FMEA-011 preserved): slides are resolved OWNER-SCOPED from
> 129	          // creative_assets with a hard tenant bind (a forged id of another tenant returns 0 rows → structured
> 130	          // failure, zero cross-tenant read), mirroring publish-space-carousel. URLs are signed FRESH here on
> 131	          // EVERY attempt (retries re-sign — an enqueue-time URL would outlive its 6h TTL). <2 resolved/signed
> 132	          // slides throws (→ retry/failed with a clear error) instead of falling into the single-image branch.
> 133	          if (typeof reshape.carousel_render_id === "string" && reshape.carousel_render_id) {
> 134	            const { data: slides } = await adminClient
> 135	              .from("creative_assets")
> 136	              .select("storage_bucket, storage_key")
> 137	              .eq("source_job_id", reshape.carousel_render_id)
> 138	              .eq("user_id", post.user_id)        // hard tenant bind — the marker alone grants nothing
> 139	              .eq("kind", "image")
> 140	              .order("storage_key", { ascending: true })
> 141	              .limit(10);                          // IG max
> 142	            const images: string[] = [];
> 143	            for (const s of slides ?? []) {
> 144	              const { data: signed } = await adminClient.storage
> 145	                .from(s.storage_bucket as string)
> 146	                .createSignedUrl(s.storage_key as string, 21600);
> 147	              if (signed?.signedUrl) images.push(signed.signedUrl);
> 148	            }
> 149	            if (images.length < 2) {
> 150	              throw new Error(`carousel_slides_unavailable (resolved ${slides?.length ?? 0}, signed ${images.length})`);
> 151	            }
> 152	            native.images = images;
> 153	          } else if (reshape.space_publish_variant_id) {
> 154	            // OTD-SPACES-036 — Spaces-origin publish: resolve the asset from space_publish_variants (dedicated table,
> 155	            // money-path/channel_variants untouched). Same tenant hard-bind as the pillar path.
> 156	            const { data: sv } = await adminClient
> 157	              .from("space_publish_variants")
> 158	              .select("asset_bucket, asset_key, asset_kind")
> 159	              .eq("id", reshape.space_publish_variant_id)
> 160	              .eq("user_id", post.user_id)        // hard tenant bind — a forged variant_id of another tenant returns nothing
> 161	              .maybeSingle();
> 162	            await attachAsset(sv?.asset_bucket as string | undefined, sv?.asset_key as string | undefined, sv?.asset_kind as string | undefined);
> 163	          } else if (reshape.channel_variant_id) {
> 164	            // FR-CP-003 pillar path (unchanged).
> 165	            const { data: cv } = await adminClient
> 166	              .from("channel_variants")
> 167	              .select("asset_bucket, asset_key, asset_kind")
> 168	              .eq("id", reshape.channel_variant_id)
> 169	              .eq("user_id", post.user_id)        // hard tenant bind — a forged variant_id of another tenant returns nothing
> 170	              .maybeSingle();
> 171	            await attachAsset(cv?.asset_bucket as string | undefined, cv?.asset_key as string | undefined, cv?.asset_kind as string | undefined);
> 172	          }
> 173	          if (Array.isArray(c.tweets)) native.thread = c.tweets;
> 174	          contentPayload = native;
> 175	        }
> 176	
> 177	        // Call publish-social
> 178	        const publishRes = await fetch(
> 179	          `${Deno.env.get("SUPABASE_URL")}/functions/v1/publish-social`,
> 180	          {
> 181	            method: "POST",
> 182	            headers: {
> 183	              "Content-Type": "application/json",
> 184	              Authorization: `Bearer ${(Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))}`,
> 185	            },
> 186	            body: JSON.stringify({
> 187	              platform: post.platform,
> 188	              content: contentPayload,
> 189	              social_account_id: post.social_account_id,
> 190	              scheduled_post_id: post.id,
> 191	              user_id: post.user_id,
> 192	            }),
> 193	          }
> 194	        );
> 195	
> 196	        if (publishRes.ok) {
> 197	          results.push({ id: post.id, status: "published" });
> 198	        } else {
> 199	          const errBody = await publishRes.json().catch(() => ({ error: "Unknown" }));
> 200	          const retryCount = (post.retry_count || 0) + 1;
> 201	          const maxRetries = post.max_retries || 3;
> 202	
> 203	          await adminClient
> 204	            .from("scheduled_posts")
> 205	            .update({
> 206	              status: retryCount >= maxRetries ? "failed" : "queued",
> 207	              retry_count: retryCount,
> 208	              error_message: errBody.error || "Publish failed",
> 209	            })
> 210	            .eq("id", post.id);
> 211	
> 212	          results.push({ id: post.id, status: "failed", error: errBody.error });
> 213	        }
> 214	      } catch (e) {
> 215	        const retryCount = (post.retry_count || 0) + 1;
> 216	        await adminClient
> 217	          .from("scheduled_posts")
> 218	          .update({
> 219	            status: retryCount >= (post.max_retries || 3) ? "failed" : "queued",
> 220	            retry_count: retryCount,
> 221	            error_message: e instanceof Error ? e.message : String(e),
> 222	          })
> 223	          .eq("id", post.id);
> 224	
> 225	        results.push({ id: post.id, status: "error", error: e instanceof Error ? e.message : String(e) });
> 226	      }
> 227	    }
> 228	
> 229	    return new Response(
> 230	      JSON.stringify({ processed: results.length, results }),
> 231	      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
> 232	    );
> 233	  } catch (err) {
> 234	    console.error("auto-publish error:", err);
> 235	    return new Response(JSON.stringify({ error: err instanceof Error ? err.message : String(err) }), {
> 236	      status: 500,
> 237	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 238	    });
> 239	  }
> 240	});
> 241	
> ```

## 🤖 Claude *(13:25:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n -A3 \"publish-social\\|auto-publish\\|social-auth-init\" /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml | head -40",
  "description": "Check verify_jwt config for the touched functions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 6:[functions.publish-social]
> 7-verify_jwt = false
> 8-[functions.check-post-existence]
> 9-verify_jwt = false
> --
> 100:[functions.social-auth-init]
> 101-verify_jwt = false
> 102-
> 103-# tiktok-login (Login Kit v2 → Supabase session). All PUBLIC: init/session are called from the pre-auth login
> ```

## 🤖 Claude *(13:25:54)*


## 🤖 Claude *(13:25:54)*


## 🤖 Claude *(13:27:19)*


## 🤖 Claude *(13:27:19)*

Let me check for any existing SSRF mitigation/URL-guard helpers that the new fetches might bypass, and confirm the trust model around who can set `content.*`.

## 🤖 Claude *(13:27:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls supabase/functions/_shared/ 2>/dev/null && echo \"=== grep for SSRF/url guards in shared + publish-social ===\" && grep -rniE \"ssrf|allowlist|allow_list|isPrivate|169\\.254|metadata|localhost|127\\.0\\.0\\.1|validateUrl|assertPublic|blocklist\" supabase/functions/_shared/ supabase/functions/publish-social/ 2>/dev/null | head -40",
  "description": "Look for existing SSRF guards / URL validation helpers"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> affiliate.ts
> agent-metering.ts
> autopilot-video-cadence.test.ts
> autopilot-video-cadence.ts
> billing.test.ts
> billing.ts
> higgsfield-oauth.test.ts
> higgsfield-oauth.ts
> higgsfield-token.ts
> intent-policy.ts
> llm-fallback.test.ts
> llm-fallback.ts
> notify.ts
> oauth-state.ts
> provider-keys.ts
> reframe.ts
> sentinel.test.ts
> sentinel.ts
> smart-delete-classify.test.ts
> smart-delete-classify.ts
> social-app-config.ts
> tiktok-login-creds.ts
> tiktok-login-flow.ts
> === grep for SSRF/url guards in shared + publish-social ===
> supabase/functions/_shared/higgsfield-token.ts:39:      service: "higgsfield-mcp", status: "degraded", event: "oauth_refresh_failed", metadata: { status: res.status },
> supabase/functions/_shared/affiliate.ts:34: *  affiliate_config.metadata.shortlinks[external_id] (e.g. meli.la/2gh13Sw → matt_word+matt_tool+ref). This is the
> supabase/functions/_shared/affiliate.ts:44:      .select("metadata").eq("user_id", ownerId).eq("platform", "mercadolivre").maybeSingle();
> supabase/functions/_shared/affiliate.ts:45:    const link = data?.metadata?.shortlinks?.[mlb];
> supabase/functions/_shared/affiliate.ts:121:        metadata: { source: "auto-monetize", display: p.display, campaign: opts.campaignId ?? null, matt_tool: opts.mattTool ?? null },
> supabase/functions/_shared/affiliate.ts:257:      metadata: {
> supabase/functions/_shared/social-app-config.ts:22:  metadata: Record<string, unknown>;
> supabase/functions/_shared/social-app-config.ts:65:      .select("client_id, client_secret, scopes, metadata, is_active")
> supabase/functions/_shared/social-app-config.ts:76:        metadata: (data.metadata as Record<string, unknown>) ?? {},
> supabase/functions/_shared/social-app-config.ts:86:    return { clientId: envId, clientSecret: envSecret, scopes: null, metadata: {}, source: "env" };
> supabase/functions/_shared/sentinel.ts:143:      metadata: { fn, ...payload, user_id: userId },
> supabase/functions/_shared/tiktok-login-flow.ts:86:        email, email_confirm: true, user_metadata: { provider: "tiktok", tiktok_open_id: openId },
> supabase/functions/_shared/provider-keys.ts:81:/** Telemetria per-chave (qual conta está queimando crédito) — allowlist: NUNCA logar a chave, só o id/source. */
> supabase/functions/_shared/notify.ts:9:  metadata?: Record<string, unknown>;
> supabase/functions/_shared/notify.ts:25:      metadata: n.metadata ?? {},
> supabase/functions/_shared/llm-fallback.ts:60:        metadata: {
> supabase/functions/_shared/llm-fallback.ts:95:        metadata: { fn: functionName, model, image_count: count },
> supabase/functions/publish-social/index.ts:117:    const pulse = (status: "ok" | "degraded" | "error", event?: string, metadata?: Record<string, unknown>) =>
> supabase/functions/publish-social/index.ts:120:        .insert({ service: `publish-${platform}`, status, event: event ?? null, metadata: metadata ?? {} })
> supabase/functions/publish-social/index.ts:602:      // (0) Ensure a destination board — prefer a cached metadata.board_id, else the first existing board, else
> supabase/functions/publish-social/index.ts:604:      let boardId: string | null = account.metadata?.board_id ?? null;
> supabase/functions/publish-social/index.ts:751:      metadata: { platform, post_id: result?.id ?? null },
> ```

## 🤖 Claude *(13:27:35)*


## 🤖 Claude *(13:28:08)*

I have everything I need. Let me confirm the trust-model facts before writing the report.

Key verifications:
- `publish-social` has `verify_jwt = false` (config.toml:6-7) → the function self-authenticates. User-JWT callers reach it via `supabase.auth.getUser()` (line 51); `content` is taken verbatim from the request body (line 25) with **no per-field gating by caller type**. So a user-JWT caller fully controls every `content.*` field for their own account.
- There is **no** URL-validation / SSRF guard anywhere in `publish-social` or `_shared/` (grep returned none). The pre-existing TikTok/YouTube/Pinterest branches already do `fetch(content.video_url)` on the same unguarded, caller-controllable URL.

---

# Security Review — Amendment 24 (media rails, FR-SPACES-082/083/084/085)

## Verdict: No NEW findings meet the >80% confidence bar.

Below is the per-vector assessment, then a pre-existing-notes section (as instructed) for the SSRF class, which is real but not newly introduced.

### (a) SSRF via `content.image_url` in the new `fetch()` calls — PRE-EXISTING CLASS, not a new finding

`publish-social/index.ts:153` (LinkedIn) and `:339` (Twitter) add `await fetch(content.image_url)`. For **user-JWT callers, `image_url` is fully attacker-controlled** (their own JWT, their own connected account). This is an SSRF primitive.

However, this exact class **already exists and is already reachable by user-JWT callers**:
- TikTok branch `:408` — `fetch(content.video_url)`
- YouTube branch `:508` — `fetch(content.video_url)`
- Pinterest branch `:649` — `fetch(content.video_url)`

`content` is read verbatim from the body regardless of caller (line 25); nothing restricts `video_url`/`image_url` to the cron. So server-side fetch of a caller-supplied URL was already an accepted primitive here, with **no URL guard** (confirmed by grep — there is no allowlist the new code bypasses; there was never one). The IG branch remains "Meta fetches it, not us" (`:243`,`:246`), so IG adds nothing server-side.

Honest delta rating: **low/incremental**. The new code widens the fetchable-URL set from `video_url` to also `image_url`, and the exfil-read-back angle (see (b)) is marginally more practical on image platforms than on video transcoders. It does not introduce a new class, a new caller-reachability, or bypass an existing guard. I did not confirm that the Supabase-hosted Deno edge runtime exposes a cloud metadata endpoint (169.254.169.254) or reachable localhost services from the isolate, so I cannot rate internal-surface reachability above the confidence bar. → documented in pre-existing notes, not counted.

### (b) Fetched bytes forwarded as the caller's own media — no cross-tenant angle. No finding.
In both new branches the account is resolved by the caller's own `userId` (line 65-70), so uploaded media lands on the **caller's own** LinkedIn/X account. In the cron path, `image_url` is a fresh owner-scoped signed URL resolved from server-trusted, tenant-hard-bound ledger rows (`auto-publish` lines 133-171, `.eq("user_id", post.user_id)`), never from `scheduled_posts.metadata`. There is no path by which one tenant's bytes reach another tenant's account. The only "exfil" is attacker → their own media (a facet of the pre-existing SSRF, noted below), not cross-tenant.

### (c) `surface` discriminator — no finding.
`auto-publish:118` copies `reshape.content.surface` only when `typeof === "string"`, capped to 60 chars. `publish-social:235` uses it as a strict-equality check against literals `"story"`/`"stories"` to pick IG `media_type=STORIES`. No SQL, no path, no injection surface; a crafted `surface` only alters the shape of the caller's **own** post (feed vs. story) and drops the caption. No blast radius beyond the caller. Confirmed clean.

### (d) `media.write` scope addition — no finding.
`social-auth-init:100` appends `media.write` to the Twitter scope string; `offline.access` and the others are retained, so refresh flows are not downgraded. Pre-existing connections lacking the scope fail closed at upload with an actionable error (`:352`) rather than silently posting text-only. The scope is exactly the capability needed; no over-broad grant. (Note: the pre-existing `code_challenge_method=plain` PKCE weakness at `social-auth-init:99` is untouched by this diff and out of scope.)

### (e) Telemetry leakage into `infra_health_logs` (global-read) — no finding.
All new `pulse()` calls write metadata containing **only HTTP status codes** (`linkedin_image_register_failed`/`_fetch_failed`/`_upload_failed`, `twitter_media_fetch_failed`/`_upload_failed`) or nothing (`linkedin_image_uploaded`, `twitter_media_uploaded`, `twitter_media_no_id`). No URLs, tokens, user content, or `user_id` are written, and `service` is the constrained `publish-<platform>` label. No PII/secret reaches the global-read table.

---

## Pre-existing notes (not counted as new findings)

- **SSRF via caller-controlled fetch URL in `publish-social`.** Already present at `:408`/`:508`/`:649` (`video_url`); Amendment 24 extends it to `image_url` at `:153`/`:339`. The function does server-side `fetch()` of an arbitrary URL supplied by a user-JWT caller, with no host allowlist and no block on internal/link-local ranges. On image platforms the fetched bytes become the caller's own viewable media, turning a blind SSRF into a semi-blind exfil-read primitive for whatever the isolate can reach.
  - Recommended hardening (applies to the whole function, pre-dates this diff): add a shared `assertPublicHttpUrl(url)` guard in `_shared/` — require `https:`, resolve+reject RFC1918/link-local/loopback/`169.254.0.0/16`, reject non-standard ports — and call it before **every** `fetch(content.video_url|image_url)`. This closes the pre-existing class and the new image branches in one place.
- **`code_challenge_method=plain`** at `social-auth-init:99` (self-described "demo") — untouched, out of scope, flagged only for awareness.

## Scope note
`src/lib/format-specs.ts` changes are client-display note strings only (no logic/security surface). Docs excluded per instructions.

**Bottom line:** the diff is clean with respect to newly-introduced vulnerabilities. The one real risk (SSRF) is a pre-existing, already-reachable, already-unguarded class that this change widens only marginally; worth fixing with a shared URL guard, but it is not a defect introduced by Amendment 24.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-14 - agent-a90a22787dc50c7a8]]
> * **Próxima Sessão**: [[2026-07-14 - agent-ab06741d5bc28e55d]]
%% --- TIMELINE END --- %%

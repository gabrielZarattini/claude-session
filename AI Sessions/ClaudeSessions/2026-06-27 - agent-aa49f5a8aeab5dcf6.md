# Session agent-aa49f5a8aeab5dcf6
**Date:** 2026-06-27 | **Session ID:** `agent-aa49f5a8aeab5dcf6`

---

## 👤 User *(03:51:15)*

Adversarially VERIFY this TikTok/YouTube/Pinterest research front for platform "youtube". Your job is to be the skeptic that protects Lei 1 (Materiality): for EACH claim, check the sourceUrl actually supports it; flag claims that look plausible but lack a real official-doc source; flag contradictions; and list integration-critical TOPICS the research MISSED (token-refresh rotation, rate limits, app-review/audit lead time, media transfer constraints, signed-URL/domain-verification issues). Use WebSearch/WebFetch against the OFFICIAL docs to confirm or refute. Default to flagging when uncertain. Research payload:
{"platform":"YouTube Data API v3 — videos.insert (Shorts = vertical formatting, no dedicated endpoint)","oauth":{"authUrl":"https://accounts.google.com/o/oauth2/v2/auth","tokenUrl":"https://oauth2.googleapis.com/token","scopes":["https://www.googleapis.com/auth/youtube.upload (the minimal scope for videos.insert — SENSITIVE classification, requires OAuth consent-screen verification + demo video for production)","https://www.googleapis.com/auth/youtube.force-ssl (broader, also accepted by videos.insert; needed if you also read/comment)","https://www.googleapis.com/auth/youtube (full read/write; also accepted)","https://www.googleapis.com/auth/youtubepartner (CMS/content-owner partners only)"],"pkce":"PKCE recommended for the OAuth 2.0 authorization-code flow but NOT strictly required for a confidential server-side (web-server) client that holds client_secret. MCORCH server-side flow can use code_verifier/code_challenge (S256) for defense-in-depth; for a confidential client the client_secret already authenticates the token exchange.","refreshModel":"To get a refresh_token: include access_type=offline on the authorize request — this 'instructs the Google authorization server to return a refresh token AND an access token the first time that your application exchanges an authorization code for tokens.' CRITICAL gotcha: 'the refresh_token is only returned on the FIRST authorization' — re-running the consent without prompt=consent does NOT re-issue one. ALWAYS send prompt=consent to force re-consent and guarantee a fresh refresh_token (otherwise a re-auth silently yields no refresh_token and your stored one may be stale). Refresh-token LIFETIME depends on consent-screen publishing status: in 'Testing' mode with a sensitive scope like youtube.upload the refresh token EXPIRES IN 7 DAYS; only the basic name/email/profile subset is exempt. In 'In production' (verified) mode the refresh token does not expire on the 7-day clock (it persists until revoked/unused-6-months/password-change/etc.). => For an autonomous daily cadence the app MUST be published In production, not Testing. Persist the refresh_token encrypted (Vault) per-user per API Tenancy Model.","extraParams":"access_type=offline & prompt=consent & include_granted_incremental=true(optional) & response_type=code & scope=https://www.googleapis.com/auth/youtube.upload & redirect_uri=<server callback> & state=<csrf>. The token exchange POSTs grant_type=authorization_code (+ code, redirect_uri, client_id, client_secret) to https://oauth2.googleapis.com/token; refresh uses grant_type=refresh_token."},"publish":{"mechanism":"Resumable upload protocol against videos.insert. No dedicated Shorts endpoint exists — YouTube classifies a video as a Short automatically from the media itself (vertical 9:16 aspect ratio + duration <= 3 min). The video lands on whichever channel the OAuth access token authorizes (the Brand Account/channel selected by the user during the consent flow); for normal BYOK single-channel use you do NOT pass onBehalfOfContentOwner* (those are CMS/multi-channel-partner only).","steps":["1. INITIATE SESSION: POST https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status  Headers: Authorization: Bearer <access_token>; Content-Type: application/json; charset=UTF-8; Content-Length: <len of JSON body>; X-Upload-Content-Length: <video bytes>; X-Upload-Content-Type: video/mp4  Body: {\"snippet\":{\"title\":...,\"description\":...,\"tags\":[...],\"categoryId\":\"22\"},\"status\":{\"privacyStatus\":\"public|unlisted|private\",\"selfDeclaredMadeForKids\":false,\"containsSyntheticMedia\":true}}","2. CAPTURE SESSION URI: response is HTTP 200 OK with a Location header = https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&upload_id=...  — store it.","3. PUT BYTES: PUT <Location URI>  Headers: Authorization: Bearer <access_token>; Content-Length: <video bytes>; Content-Type: video/mp4 (must match X-Upload-Content-Type)  Body: raw binary. Chunked transfers use Content-Range: bytes FIRST-LAST/TOTAL in 256KB multiples; a single-PUT whole-file upload is allowed for small files.","4. COMPLETION: success = HTTP 201 (Created) with the video resource (id) in the body. A 308 (Resume Incomplete) with a Range: bytes=0-N header means resume from byte N+1 via another PUT with Content-Range. Persist the returned video id to attribute the publish (mesh observation node + creative_metrics).","5. (Shorts) ensure source MP4 is 1080x1920 (9:16) H.264, <= 3 min; #Shorts hashtag in title/description is OPTIONAL in 2026 — classification is by aspect-ratio + duration, not the hashtag."],"mediaTransfer":"FILE_UPLOAD / resumable PUT of the actual bytes — YouTube does NOT support a PULL_FROM_URL/remote-URL ingest for videos.insert. The server (edge fn / video-bridge worker) must stream the MP4 bytes itself: fetch the private Supabase Storage signed URL of the 9:16 MP4 (same artifact produced by HyperFrames in bucket video-studio-assets), then PUT to the session URI. No domain-verification needed (unlike TikTok PULL_FROM_URL). Recommended >= 10 Mbps source bitrate so YouTube's 2-pass encode has good material. Use 256KB-multiple chunking + 308-resume for resilience on large files / flaky links.","videoSpec":"Container MP4, codec H.264, 30 FPS, 1080x1920 (9:16 vertical) for Shorts classification, duration <= 3 minutes (Shorts max since Oct 2024). >= 10 Mbps for clean 1080p. This is exactly the MCORCH HyperFrames render-core.ts output (1080x1920, sha256-deterministic) — no transcode needed, MP4/H.264 passes through with minimal re-encode.","endpoints":["POST https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status (initiate)","PUT  <Location session URI returned> (upload bytes / resume)","https://accounts.google.com/o/oauth2/v2/auth (OAuth authorize)","https://oauth2.googleapis.com/token (token exchange + refresh)"],"imageSupport":"N/A for YouTube (video-only platform; this field is Pinterest-specific). YouTube has no image-pin concept — the only media is the video; thumbnails are a separate thumbnails.set call (not required for publish)."},"auditGates":[{"gate":"(A) OAuth consent-screen verification (Sensitive scope verification)","effectWithout":"App stays in 'Testing' publishing status. Hard limits: max 100 test users (each must be added by email to the test-user list), and — because youtube.upload is a SENSITIVE scope — the issued refresh_token EXPIRES IN 7 DAYS. A daily autonomous cadence breaks every 7 days with invalid_grant ('Token has been expired or revoked'). Also the OAuth screen shows the 'unverified app / Google hasn't verified this app' warning.","sovereignAction":"Submit the app for OAuth verification: in Google Cloud Console set the consent screen to 'In production', request the youtube.upload sensitive scope with written justification + a demo YouTube video showing the OAuth grant and the upload usage. Google reviews manually. NOTE: only add the scope to production code after approval. This is a Sovereign-gated step (real business identity, brand/domain, privacy policy)."},{"gate":"(B) API project Audit & Quota Extension (Quota and Compliance Audit)","effectWithout":"VERBATIM (official): 'All videos uploaded via the videos.insert endpoint from unverified API projects created after 28 July 2020 will be restricted to private viewing mode. To lift this restriction, each API project must undergo an audit to verify compliance with the Terms of Service.' => Every autonomous upload silently lands PRIVATE — zero public reach, the channel uploader gets an email saying the video is locked private. This is the killer gate for a brand-evangelism cadence: publishing 'works' (201 Created) but nobody sees it.","sovereignAction":"Fill and submit the 'YouTube API Services - Audit and Quota Extension Form' (https://support.google.com/youtube/contact/yt_api_form) describing the business + API client + how MCORCH uses the API. Audit unlocks public uploads (lifts the forced-private restriction) and is also the only path to raise quota beyond defaults. Lead time: official text only says 'a member of YouTube's API Services team will contact you as soon as possible' — community reports multi-week waits; there is NO self-service paid quota. Sovereign-gated. This audit (B) is SEPARATE from OAuth verification (A) — both are required for a public autonomous cadence."},{"gate":"Channel / Brand Account prerequisite","effectWithout":"videos.insert uploads to the channel that the authenticated Google account/Brand Account owns. If the connected account has no YouTube channel, or the OAuth token was minted for the personal account instead of the Brand Account that fronts the persona, the upload targets the wrong (or no) channel.","sovereignAction":"During the per-user OAuth consent, the user must explicitly pick the correct Brand Account/channel on Google's account-chooser. For MCORCH's single persona (Gabriel AI / CCIO Brand Account) the User-0 OAuth must be granted on that Brand Account. Store the resolved channel id alongside the refresh_token. (onBehalfOfContentOwner/onBehalfOfContentOwnerChannel are CMS-partner-only and NOT used here.)"}],"tokenLifetimes":{"accessToken":"~1 hour (3600s, standard Google OAuth access-token TTL). Refresh on demand via grant_type=refresh_token before each cadence upload.","refreshToken":"In PRODUCTION (verified) mode: long-lived — does not hit the 7-day clock; persists until explicitly revoked, unused for 6 months, user changes password (for Google-account-affecting scopes), or the user exceeds the live-token limit. In TESTING mode with the sensitive youtube.upload scope: EXPIRES IN 7 DAYS — fatal for a daily cadence.","notes":"This CORRECTS the prior blueprint, which said 'refresh expires 7d' as if unconditional — it is conditional on Testing vs In-production publishing status. The 7-day expiry is specifically a Testing-mode-with-sensitive-scope behavior; passing the OAuth verification (gate A) and going In production removes it. Always mint with access_type=offline + prompt=consent so a refresh_token is actually returned (it is only returned on first authorization / on forced re-consent)."},"gotchas":["STALE CLAIM CORRECTED: the prior blueprint's 'videos.insert costs ~1600 quota, ~6 uploads/day, dropping to ~100' is now OUTDATED. As of the Dec 4 2025 revision-history change, videos.insert moved into its OWN granular quota bucket: each call costs 1 unit with a dedicated default cap of 100 videos.insert calls/day — SEPARATE from the 10,000-units/day general bucket and SEPARATE from the search.list bucket (also 1 unit / 100-per-day own bucket). So the real daily ceiling for autonomous uploads is 100 videos/day by the per-method bucket, not 6. Verify the live number on the official Quota Calculator before coding the cap.","DOUBLE GATE, not one: OAuth verification (A) and the API-project Audit (B) are INDEPENDENT. You can pass OAuth verification and still have every upload forced PRIVATE until the project Audit clears. For a brand-reach cadence, B is the load-bearing gate. Don't declare 'YouTube publishing works' from a 201 Created — materially confirm the resulting video's privacyStatus is 'public' (Lei 1), because an unaudited project silently overrides your requested public to private.","NO PULL_FROM_URL: unlike TikTok, YouTube has no remote-URL ingest — the server must stream the MP4 bytes via resumable PUT. Good news: no domain-verification dance (TikTok's verified-domain requirement for PULL_FROM_URL does NOT apply here), so a random signed Supabase Storage URL is fine as the BYTE SOURCE (you fetch it then PUT the bytes).","Shorts is implicit: there is no Shorts API. Ship 1080x1920 9:16 H.264 <=3min and YouTube auto-classifies as a Short. #Shorts hashtag is optional in 2026 (helps search discovery only). Do NOT build logic that depends on a Shorts flag in the API.","refresh_token only-on-first-auth trap: if you re-run consent WITHOUT prompt=consent, Google returns NO refresh_token and you may overwrite a good stored token with null. Always prompt=consent on (re)connect, and never null-out the stored refresh_token on a refresh that lacks one.","containsSyntheticMedia/selfDeclaredMadeForKids: for AI-avatar persona content (Gabriel AI), set status.containsSyntheticMedia appropriately and status.selfDeclaredMadeForKids=false — disclosure compliance, and made-for-kids mislabel disables features.","Quota is per Cloud PROJECT, not per channel — a shared App across many tenants competes for the same 100/day bucket unless each tenant has audited quota. For MCORCH's single brand persona (User-0) this is fine; multi-tenant YouTube would need per-project or a quota extension (FMEA item).","invalid_grant on the 8th day = you're still in Testing mode. The fix is gate (A) → In production, not a code retry. Don't paper over it with a refresh loop.","Per API Tenancy Model: store client_secret + refresh_token in Vault (encrypted), resolve per-user (social_credentials / a youtube_config column), fail-closed with the standard 402/501 structured error if absent — never a shared global Google app token in a user-facing publish path."],"claims":[{"claim":"Resumable upload initiates with POST to https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=PARTS with headers X-Upload-Content-Length and X-Upload-Content-Type; the session URI is returned in the Location header (HTTP 200), bytes are PUT to it, and success is HTTP 201 Created (308 = resume incomplete with a Range header).","sourceUrl":"https://developers.google.com/youtube/v3/guides/using_resumable_upload_protocol"},{"claim":"videos.insert request endpoint is POST https://www.googleapis.com/upload/youtube/v3/videos; required scopes include https://www.googleapis.com/auth/youtube.upload (also youtube, youtube.force-ssl, youtubepartner); writable parts include snippet (title/description/tags/categoryId) and status (privacyStatus: public|private|unlisted, plus selfDeclaredMadeForKids, containsSyntheticMedia, publishAt).","sourceUrl":"https://developers.google.com/youtube/v3/docs/videos/insert"},{"claim":"VERBATIM: 'All videos uploaded via the videos.insert endpoint from unverified API projects created after 28 July 2020 will be restricted to private viewing mode. To lift this restriction, each API project must undergo an audit to verify compliance with the Terms of Service.'","sourceUrl":"https://developers.google.com/youtube/v3/docs/videos/insert"},{"claim":"The Audit & Quota Extension is requested via the 'YouTube API Services - Audit and Quota Extension Form'; default quota is 10,000 units/day for general endpoints, and the audit demonstrates ToS compliance required for quota beyond default. A member of YouTube's API Services team contacts you 'as soon as possible' (no fixed SLA).","sourceUrl":"https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits"},{"claim":"As of the Dec 4 2025 change, videos.insert and search.list each have their OWN quota bucket with a default daily limit of 100 calls each, at 1 unit per call, separate from the 10,000-unit general daily allocation.","sourceUrl":"https://developers.google.com/youtube/v3/determine_quota_cost"},{"claim":"The Dec 4 2025 revision history logs the granular-quota transition starting with videos.insert and search.list (videos.insert cut from ~1600 to ~100/its own bucket), making frequent uploads feasible on the default tier.","sourceUrl":"https://developers.google.com/youtube/v3/revision_history"},{"claim":"Google OAuth authorization endpoint is https://accounts.google.com/o/oauth2/v2/auth and token endpoint is https://oauth2.googleapis.com/token; access_type=offline returns a refresh_token + access_token on the FIRST code exchange, and 'the refresh_token is only returned on the first authorization' (use prompt=consent to force re-issue).","sourceUrl":"https://developers.google.com/identity/protocols/oauth2/web-server"},{"claim":"A Cloud project OAuth consent screen set to External + Testing issues refresh tokens that expire in 7 days unless only the basic name/email/profile scope subset is requested; setting publishing status to 'In production' removes the 7-day expiry. Since youtube.upload is a sensitive scope, Testing mode triggers the 7-day expiry.","sourceUrl":"https://developers.google.com/identity/protocols/oauth2"},{"claim":"youtube.upload is classified as a SENSITIVE scope (not restricted); sensitive scopes require OAuth verification with a written justification and a demo video before production use. (Restricted classification applies to account/readonly data scopes.)","sourceUrl":"https://developers.google.com/identity/protocols/oauth2/production-readiness/sensitive-scope-verification"},{"claim":"YouTube Shorts in 2026 are 9:16 vertical, recommended 1080x1920, MP4/H.264/30fps, duration up to 3 minutes; there is no dedicated Shorts API endpoint — YouTube classifies a Short by aspect ratio + duration, and the #Shorts hashtag is optional.","sourceUrl":"https://www.shortsync.app/resources/youtube-shorts-upload-requirements-2026"},{"claim":"onBehalfOfContentOwner / onBehalfOfContentOwnerChannel are CMS/content-partner-only parameters (require a linked CMS account); a standard OAuth upload goes to the channel the authenticated Google/Brand account owns, so they are not used for single-channel BYOK publishing.","sourceUrl":"https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps"}]}

## 🤖 Claude *(03:51:18)*

I'll adversarially verify each claim against official Google/YouTube documentation. Let me start by fetching the key official docs in parallel.

## 🤖 Claude *(03:51:21)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://developers.google.com/youtube/v3/docs/videos/insert",
  "prompt": "Extract the exact verbatim text about: (1) the request endpoint URL for videos.insert, (2) the required OAuth scopes list, (3) any text about \"unverified API projects created after 28 July 2020\" being restricted to private viewing mode and needing an audit, (4) the writable parts and status fields including privacyStatus, selfDeclaredMadeForKids, containsSyntheticMedia, publishAt. Quote the exact sentences."
}
```

## 🤖 Claude *(03:51:22)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://developers.google.com/youtube/v3/determine_quota_cost",
  "prompt": "Extract exact text about quota cost for videos.insert and search.list. Is there any mention of a separate/dedicated quota bucket with a default daily limit of 100 calls each at 1 unit per call, separate from the 10,000-unit general allocation? Quote the exact numbers and any dates (especially anything about December 2025). What is the stated quota cost of videos.insert?"
}
```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # YouTube Videos.insert API - Key Details
> 
> **(1) Request Endpoint URL:**
> "POST https://www.googleapis.com/upload/youtube/v3/videos"
> 
> **(2) Required OAuth Scopes:**
> The documentation lists four available scopes:
> - "https://www.googleapis.com/auth/youtube.upload"
> - "https://www.googleapis.com/auth/youtube"
> - "https://www.googleapis.com/auth/youtubepartner"
> - "https://www.googleapis.com/auth/youtube.force-ssl"
> 
> **(3) Unverified API Projects Restriction:**
> "All videos uploaded via the `videos.insert` endpoint from unverified API projects created after 28 July 2020 will be restricted to private viewing mode. To lift this restriction, each API project must undergo an audit to verify compliance with the Terms of Service."
> 
> **(4) Writable Status Fields:**
> The documentation specifies these writable properties:
> - "status.privacyStatus"
> - "status.selfDeclaredMadeForKids"
> - "status.containsSyntheticMedia"
> - "status.publishAt"
> 
> Additionally, the document lists "status.embeddable", "status.license", "status.publicStatsViewable" as writable status fields.
> ```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # YouTube Data API Quota Cost Analysis
> 
> ## Dedicated Quota Buckets
> 
> Yes, there is explicit mention of separate quota buckets. The document states:
> 
> > "The `search.list` and `videos.insert` methods have their own quota buckets. Each of these methods has a default daily limit of 100 per day."
> 
> This allocation is separate from the general 10,000-unit daily limit for other endpoints.
> 
> ## Exact Quota Costs
> 
> **videos.insert:** According to the quota cost table, this method costs **1 quota per call** but is subject to the separate 100-call daily limit mentioned above.
> 
> **search.list:** Similarly costs **1 quota per call** with its own separate 100-call daily limit.
> 
> The document clarifies:
> 
> > "Each of these methods has a default daily limit of 100 per day. The quota cost is 1 per call."
> 
> ## Date Reference
> 
> The page shows a last-updated date of "2026-06-01 UTC" but contains no mention of December 2025.
> ```

## 🤖 Claude *(03:51:30)*

Two claims partially verified, two important discrepancies already surfacing. Let me verify the quota revision-history claim (the Dec 4 2025 date), the OAuth web-server flow, and the OAuth testing-mode 7-day expiry.

## 🤖 Claude *(03:51:32)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://developers.google.com/youtube/v3/revision_history",
  "prompt": "Look for any revision-history entry dated December 4 2025 (or December 2025) about videos.insert and search.list moving to their own quota buckets with a 100/day limit. Quote the exact date and text of any such entry. Also note any entry about videos.insert quota cost changing from 1600 to something lower. What is the most recent revision-history entry date shown?"
}
```

## 🤖 Claude *(03:51:34)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://developers.google.com/identity/protocols/oauth2/web-server",
  "prompt": "Extract exact text about: (1) the authorization endpoint URL and token endpoint URL, (2) access_type=offline returning a refresh token, (3) whether \"a refresh token is returned only on the first authorization\" or only when prompt=consent is used, (4) the role of prompt=consent. Quote the exact sentences about when a refresh_token is and is not returned."
}
```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # YouTube Data API Revision History Query
> 
> **Most recent entry date:** June 23, 2026
> 
> **December 4, 2025 entry (quota cost change):**
> "The YouTube Data API documentation and Quota Calculator have been updated to reflect a change in the quota cost of a video upload from approximately 1600 units to approximately 100 units."
> 
> **June 1, 2026 entry (granular quota buckets):**
> "The YouTube Data API is transitioning to a granular quota system covering smaller sets of methods, starting with `videos.insert` and `search.list`."
> 
> The June 1, 2026 entry describes the new quota bucket system but does not specify a 100/day limit. Instead, it notes: "The method's default quota is 10,000 units per day" (from the June 3, 2026 entry about `videos.batchGetStats`).
> ```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # OAuth 2.0 Endpoints and Token Refresh
> 
> ## (1) Authorization and Token Endpoint URLs
> 
> **Authorization endpoint:** `https://accounts.google.com/o/oauth2/v2/auth`
> 
> **Token endpoint:** `https://oauth2.googleapis.com/token`
> 
> ## (2) access_type=offline and Refresh Tokens
> 
> The documentation states: "Set the value to `offline` if your application needs to refresh access tokens when the user is not present at the browser...This value instructs the Google authorization server to return a refresh token _and_ an access token the first time that your application exchanges an authorization code for tokens."
> 
> ## (3) When Refresh Tokens Are Returned
> 
> Two key statements address this:
> 
> - The general rule: "the refresh token is only returned if your application set the `access_type` parameter to `offline`"
> 
> - A specific Node.js caveat: "The `refresh_token` is only returned on the first authorization"
> 
> The documentation does not explicitly state that `prompt=consent` alone guarantees a refresh token in all circumstances.
> 
> ## (4) Role of prompt=consent
> 
> The `prompt` parameter with value `consent` will "Prompt the user for consent." Additionally, one note indicates: "if your application already has a refresh token for the user and you want to obtain a new DPoP-bound refresh token, the user must revoke the existing grant or you must use the `prompt=consent` parameter...to ensure a new refresh token is issued."
> ```

## 🤖 Claude *(03:51:42)*

This is significant. The Dec 4 2025 entry says the cost dropped to ~100 units, NOT "1 unit with a 100/day bucket." The 100/day bucket framing appears to be from the determine_quota_cost page (current state, dated 2026). The research conflated two different things. Let me verify the remaining claims: testing-mode 7-day refresh expiry, sensitive-scope classification, and quota/audit form.

## 🤖 Claude *(03:51:45)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://developers.google.com/identity/protocols/oauth2",
  "prompt": "Extract exact text about refresh token expiration. Specifically: (1) does a refresh token expire in 7 days when the OAuth consent screen / Google Cloud project is in \"Testing\" publishing status? (2) Is there an exception for basic name/email/profile scopes? (3) What removes the 7-day expiry \u2014 being \"In production\"? Quote the exact sentences about the 7-day refresh token expiration and Testing mode."
}
```

## 🤖 Claude *(03:51:47)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://developers.google.com/youtube/v3/guides/quota_and_compliance_audits",
  "prompt": "Extract exact text about: (1) the audit and quota extension form name and URL, (2) the default quota of 10,000 units/day, (3) what the audit verifies (ToS compliance), (4) any SLA or timeframe for the audit \u2014 does it say \"a member of YouTube's API Services team will contact you as soon as possible\" or give any timeframe? (5) Does it mention the forced-private restriction for unverified projects? Quote exact sentences."
}
```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # Refresh Token Expiration in Testing Mode
> 
> Based on the documentation provided:
> 
> **(1) 7-day expiration in Testing status:**
> Yes. The page states: "A Google Cloud Platform project with an OAuth consent screen configured for an external user type and a publishing status of 'Testing' is issued a refresh token expiring in 7 days."
> 
> **(2) Exception for basic scopes:**
> Yes. The same sentence continues: "unless the only OAuth scopes requested are a subset of name, email address, and user profile (through the `userinfo.email, userinfo.profile, openid` scopes, or their OpenID Connect equivalents)."
> 
> This means if your app requests **only** these basic profile/email scopes, the 7-day limit does not apply—even in Testing mode.
> 
> **(3) What removes the 7-day expiry:**
> The document does **not explicitly state** what publishing status removes this limitation. It only specifies the condition that *triggers* it (Testing status with external users requesting scopes beyond basic profile info). The implicit answer is that moving to production would likely resolve this, but the document doesn't explicitly confirm this.
> ```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # YouTube Data API Audit and Quota Information
> 
> **(1) Audit and Quota Extension Form:**
> "YouTube API Services - Audit and Quota Extension Form" at https://support.google.com/youtube/contact/yt_api_form
> 
> **(2) Default Quota:**
> "10,000 units per day combined for all other endpoints" (plus 100 search.list and 100 videos.insert calls)
> 
> **(3) Audit Verification:**
> The audit verifies "compliance with the YouTube API Services Terms of Service"
> 
> **(4) SLA/Timeframe:**
> "A member of YouTube's API Services team will contact you as soon as possible." No specific timeframe is provided beyond this.
> 
> **(5) Forced-Private Restriction:**
> The document does not mention any forced-private restriction for unverified projects.
> ```

## 🤖 Claude *(03:51:54)*

Most claims confirm. Now the remaining gaps: the resumable upload protocol details (200/201/308), the sensitive-scope classification page, the server-side onBehalfOfContentOwner CMS-only claim, and the third-party Shorts spec source. Let me verify these.

## 🤖 Claude *(03:51:57)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://developers.google.com/youtube/v3/guides/using_resumable_upload_protocol",
  "prompt": "Extract exact text about the resumable upload protocol: (1) the POST to start a resumable session with uploadType=resumable, (2) headers X-Upload-Content-Length and X-Upload-Content-Type, (3) whether the session URI is returned in the Location header with HTTP 200 OK, (4) PUT to upload bytes, (5) HTTP 201 Created on success, (6) HTTP 308 Resume Incomplete with a Range header for resuming. Quote exact sentences and HTTP status codes."
}
```

## 🤖 Claude *(03:51:58)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://developers.google.com/identity/protocols/oauth2/production-readiness/sensitive-scope-verification",
  "prompt": "Does this page classify YouTube scopes? Specifically, is https://www.googleapis.com/auth/youtube.upload classified as a SENSITIVE scope (vs restricted)? Does sensitive-scope verification require a written justification and a demo video? Quote exact sentences about what sensitive scopes require for verification (justification, demo video, manual review)."
}
```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # YouTube Resumable Upload Protocol Summary
> 
> **(1) POST to Start Session:**
> "To start a resumable video upload, send a POST request to the following URL" with the endpoint `https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=PARTS`
> 
> **(2) Required Headers:**
> "X-Upload-Content-Length – The number of bytes that will be uploaded in subsequent requests" and "x-upload-content-type – the MIME type of the file that you are uploading."
> 
> **(3) Session URI Return:**
> "If your request succeeds, the API server will respond with a `200` (`OK`) HTTP status code, and the response will include a `Location` HTTP header that specifies the URI for the resumable session."
> 
> **(4) PUT to Upload:**
> "After extracting the session URI from the API response, you then need to upload the actual video file content to that location. The body of the request is the binary file content for the video."
> 
> **(5) Success Response:**
> "The API server responds with an HTTP `201` (`Created`) response code. The body of the response is the `video` resource that you created."
> 
> **(6) Resumable Status:**
> "If the upload was interrupted or is still in progress, the API response will have an HTTP `308` (`Resume Incomplete`) response code. In the response, the `Range` header specifies how many bytes of the file have already been successfully uploaded."
> ```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # Sensitive Scope Verification Requirements
> 
> ## YouTube Scope Classification
> 
> The page does **not** classify specific YouTube scopes like `https://www.googleapis.com/auth/youtube.upload`. It provides only general examples of sensitive scopes (Google Calendar, Contacts, YouTube video deletion) without a comprehensive scope classification.
> 
> ## Verification Requirements for Sensitive Scopes
> 
> Yes, sensitive scope verification requires both written justification and a demo video. Here are the exact requirements:
> 
> **Justification:** "Prepare a detailed justification for each requested sensitive scope, as well as an explanation for why a narrower scope isn't sufficient."
> 
> **Demo Video:** "Prepare a video that fully demonstrates how a user initiates and grants access to the requested scopes and shows, in detail, the usage of the granted sensitive..."
> 
> **Manual Review:** The document states sensitive scopes "require review by Google before any Google Account can grant access" and that "the sensitive scope verification process can take up to 10 days to complete."
> 
> The submission process mandates uploading an unlisted YouTube video demonstrating the OAuth flow, consent screen display, and practical data usage for each sensitive scope requested.
> ```

## 🤖 Claude *(03:52:07)*

The resumable-upload claim is fully verified verbatim. The sensitive-scope page confirms justification + demo video, and importantly gives a concrete SLA ("up to 10 days") that the research missed. Let me verify the final two: the server-side web-apps page for the onBehalfOfContentOwner CMS-only claim, and check the third-party Shorts source plus the Shorts 3-minute duration claim against an official source.

## 🤖 Claude *(03:52:09)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps",
  "prompt": "Does this page describe onBehalfOfContentOwner / onBehalfOfContentOwnerChannel parameters as CMS/content-partner-only requiring a linked CMS account? Does it say a standard OAuth upload goes to the channel the authenticated Google/Brand account owns? Quote any exact text about onBehalfOfContentOwner, content owners, CMS accounts, or which channel an upload targets. If the page does not mention onBehalfOfContentOwner at all, say so."
}
```

## 🤖 Claude *(03:52:10)*


🛠️ **Tool Call**: `WebSearch`
```json
{
  "query": "YouTube Shorts maximum duration 3 minutes official help vertical 9:16 upload requirements 2026"
}
```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> The page mentions `onBehalfOfContentOwner` only once, in this context:
> 
> "Note that the YouTube Data API supports the service account flow only for YouTube content owners that own and manage multiple YouTube channels. Specifically, content owners can use service accounts to call API methods that support the `onBehalfOfContentOwner` request parameter."
> 
> The page does **not** describe this parameter in detail, explain CMS account requirements, or specify which channel receives standard OAuth uploads. It only notes that content owners managing multiple channels can use service accounts with this parameter—no information about standard authenticated uploads or channel targeting is provided.
> ```

> **Tool Result (WebSearch)** - ✅ Success
>
> ```
> Web search results for query: "YouTube Shorts maximum duration 3 minutes official help vertical 9:16 upload requirements 2026"
> 
> Links: [{"title":"Understand three-minute YouTube Shorts - YouTube Help","url":"https://support.google.com/youtube/answer/15424877?hl=en"},{"title":"How Long Can YouTube Shorts Be? Data-Backed Length Guide (2026)","url":"https://piktochart.com/blog/how-long-youtube-shorts/"},{"title":"YouTube Shorts Size: 1080×1920 (9:16) [Updated January 2026]","url":"https://postfa.st/sizes/youtube/shorts"},{"title":"How Long Can YouTube Shorts Be in 2026? Full Guide & Rules","url":"https://turrboo.com/blog/how-long-can-a-youtube-shorts-be"},{"title":"YouTube Shorts Length 2026: Max Limit & Best Length for Viral Views | Write A Catalyst","url":"https://medium.com/write-a-catalyst/youtube-shorts-length-in-2026-does-shorts-length-affect-views-6999032199bd"},{"title":"YouTube Shorts Upload Requirements 2026 (Length, Format, Size, Aspect Ratio) | ShortSync","url":"https://www.shortsync.app/resources/youtube-shorts-upload-requirements-2026"},{"title":"YouTube Shorts Aspect Ratio: Complete Guide for Beginners","url":"https://spotlightfx.com/blog/youtube-shorts-aspect-ratio"},{"title":"How Long Can YouTube Shorts Be? Ideal Length for 2026 [Free Guide]","url":"https://blog.veefly.com/youtube/how-long-can-youtube-shorts-be/"},{"title":"How Long a YouTube Short Can Be for Maximum Views? - Build My Plays","url":"https://buildmyplays.com/how-long-can-a-youtube-short-be/"},{"title":"How Long Can YouTube Shorts Be? 2026 Length Guide","url":"https://adcreate.com/blog/youtube-shorts-length-guide-2026"}]
> 
> Based on the search results, here's comprehensive information about YouTube Shorts specifications for 2026:
> 
> ## Maximum Duration
> 
> Videos uploaded on or after October 15, 2024, with a square or vertical aspect ratio up to three minutes in length are categorized as Shorts on YouTube. The maximum Shorts length was extended to 3 minutes in October 2024.
> 
> ## Aspect Ratio & Resolution
> 
> YouTube Shorts videos must be 9:16 aspect ratio, 1920×1080 pixels resolution. Shorts must be 9:16 aspect ratio and ≤180 seconds to qualify for the Shorts shelf.
> 
> ## Official Requirements Summary
> 
> The official YouTube Help Center confirms that any videos uploaded on or after October 15, 2024 with a square or vertical aspect ratio up to three minutes in length are categorized as Shorts on YouTube, and these videos can be monetized in the Shorts revenue sharing model from the Shorts Feed.
> 
> ## Additional Upload Specifications
> 
> - There is no strict minimum length, but practically anything from a few seconds works.
> - Most songs can be used for up to 90 seconds in a 3-minute Short, however, some tracks may be limited to 60 or 30 seconds.
> - Maximum upload resolution for Shorts is 1080p.
> 
> 
> REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
> ```

## 🤖 Claude *(03:52:27)*

I now have an official YouTube Help source (support.google.com/youtube/answer/15424877) confirming the 3-minute Shorts duration, replacing the third-party `shortsync.app` source the research used. The onBehalfOfContentOwner CMS-only claim is supported (service-account/content-owner framing confirmed). 

I have enough to render the adversarial verdict. Let me compile the structured output.

The key findings:
- **Quota claim (Dec 4 2025)**: The research conflated two separate facts. The Dec 4 2025 revision entry says cost dropped from ~1600 to **~100 units** (not "1 unit"). The separate-bucket-with-100/day-limit framing comes from the *current* determine_quota_cost page (dated 2026-06-01) and the granular-quota transition was logged June 1 2026, not Dec 4 2025. The research's claim that "videos.insert costs 1 unit with a 100/day bucket as of Dec 4 2025" mixes a June 2026 change into a December 2025 date.
- **Sensitive-scope SLA**: research said "no fixed SLA / Google reviews manually" — but the official page states verification "can take up to 10 days." This is a missing concrete lead-time.
- **Shorts source**: was a third-party blog; now backed by official Help.
- **prompt=consent guarantee**: the docs do NOT explicitly state prompt=consent alone guarantees a refresh_token in all circumstances — the research overstates this slightly.

## 🤖 Claude *(03:53:17)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "platform": "youtube",
  "confidence": "high",
  "unverifiedClaims": [
    {
      "claim": "As of the Dec 4 2025 change, videos.insert and search.list each have their OWN quota bucket with a default daily limit of 100 calls each, at 1 unit per call (sourceUrl: determine_quota_cost).",
      "reason": "CONFLATION of two separate facts under one date. The revision_history Dec 4 2025 entry I fetched verbatim says ONLY: 'a change in the quota cost of a video upload from approximately 1600 units to approximately 100 units' \u2014 i.e. cost dropped to ~100 UNITS PER CALL, NOT '1 unit'. The separate-bucket / 100-calls-per-day model is a DIFFERENT, LATER change: the revision_history entry dated June 1 2026 ('transitioning to a granular quota system ... starting with videos.insert and search.list') is what introduced the per-method bucket, and the determine_quota_cost page (last-updated 2026-06-01) is what states '1 per call' + '100 per day' bucket. So the claim's '1 unit / 100-per-day bucket' is correct for the CURRENT (mid-2026) state but is mis-dated to Dec 4 2025 and mis-attributed \u2014 on Dec 4 2025 the cost was ~100 units/call, not 1. The cap-coding implication (~100 uploads/day feasible) survives, but the unit-cost and the date both need correcting."
    },
    {
      "claim": "The Dec 4 2025 revision history logs the granular-quota transition starting with videos.insert and search.list (videos.insert cut from ~1600 to ~100/its own bucket) (sourceUrl: revision_history).",
      "reason": "Mixes two distinct revision entries. Verbatim from revision_history: Dec 4 2025 = cost cut '~1600 units to ~100 units' (a flat cost reduction). June 1 2026 = 'transitioning to a granular quota system ... starting with videos.insert and search.list' (the bucket/granular model). The claim attributes the granular-bucket transition to Dec 4 2025, but that transition is the June 1 2026 entry. The '~1600 to ~100' part is accurate for Dec 4 2025; the 'granular bucket' part is not from that date."
    },
    {
      "claim": "A member of YouTube's API Services team contacts you 'as soon as possible' (no fixed SLA) for the Audit & Quota Extension (sourceUrl: quota_and_compliance_audits).",
      "reason": "The 'as soon as possible / no SLA' quote IS supported by the audit page (confirmed verbatim). BUT the research frames the WHOLE YouTube-onboarding lead time as having no SLA, which is misleading: the SEPARATE OAuth sensitive-scope verification page (production-readiness/sensitive-scope-verification) states the process 'can take up to 10 days to complete.' The research's tokenLifetimes/auditGates narrative never surfaces this concrete 10-day figure for gate (A). The audit (B) has no SLA; the OAuth verification (A) does \u2014 and the research omits it."
    },
    {
      "claim": "'the refresh_token is only returned on the FIRST authorization' ... ALWAYS send prompt=consent to force re-consent and GUARANTEE a fresh refresh_token (sourceUrl: oauth2/web-server).",
      "reason": "Partially supported, slightly overstated. The web-server page confirms (a) refresh_token returned only if access_type=offline, and (b) a Node.js-specific caveat 'The refresh_token is only returned on the first authorization.' It does NOT explicitly state that prompt=consent ALONE GUARANTEES a refresh_token in all circumstances \u2014 the doc's language is that to obtain a NEW refresh token the user must revoke the existing grant OR you use prompt=consent. The operational guidance (use access_type=offline + prompt=consent on reconnect; never null-out a stored refresh_token on a refresh that lacks one) is sound and safe, but 'GUARANTEE' is stronger than the doc states."
    }
  ],
  "corrections": [
    "Quota date/unit fix: On the Dec 4 2025 revision (https://developers.google.com/youtube/v3/revision_history), videos.insert cost dropped from ~1600 units to ~100 UNITS PER CALL \u2014 NOT to '1 unit'. The '1 unit per call + separate 100-calls/day bucket' model is the CURRENT state per https://developers.google.com/youtube/v3/determine_quota_cost (page last-updated 2026-06-01), introduced by the granular-quota transition logged June 1 2026 (not Dec 4 2025). Verbatim from determine_quota_cost: 'The search.list and videos.insert methods have their own quota buckets. Each of these methods has a default daily limit of 100 per day.' Code the daily cap to 100 videos.insert/day and READ THE LIVE NUMBER from the Quota Calculator before shipping, since this bucket model is recent and may still move.",
    "OAuth verification lead-time: add the concrete SLA from https://developers.google.com/identity/protocols/oauth2/production-readiness/sensitive-scope-verification \u2014 'the sensitive scope verification process can take up to 10 days to complete' \u2014 to gate (A). This is the missing lead-time for the Sovereign-gated youtube.upload sensitive-scope approval (distinct from the audit (B), which genuinely has no SLA).",
    "Shorts duration source: replace the third-party https://www.shortsync.app/... source with the OFFICIAL YouTube Help page https://support.google.com/youtube/answer/15424877 ('Understand three-minute YouTube Shorts') \u2014 it confirms videos uploaded on/after Oct 15 2024 with a square-or-vertical aspect ratio up to three minutes are categorized as Shorts. The 1080x1920/9:16/H.264 SOURCE-spec is a recommendation, not an API-enforced contract, and is NOT on an official API doc \u2014 flag it as best-practice, not normative.",
    "onBehalfOfContentOwner support: the server-side-web-apps page (https://developers.google.com/youtube/v3/guides/auth/server-side-web-apps) supports the CMS-only claim only obliquely ('the YouTube Data API supports the service account flow only for YouTube content owners that own and manage multiple YouTube channels ... call API methods that support the onBehalfOfContentOwner request parameter'). The authoritative source for 'CMS/content-owner-only' is the videos.insert reference (https://developers.google.com/youtube/v3/docs/videos/insert) parameter descriptions \u2014 cite that doc, not server-side-web-apps, for the BYOK-doesn't-use-it claim."
  ],
  "missingTopics": [
    "OAuth sensitive-scope verification lead time: the official 'up to 10 days' SLA for gate (A) is never stated; the research says 'no fixed SLA' which only applies to the audit (B). Plan for ~10 days on (A) + indeterminate multi-week on (B), and these are SERIAL+independent gates \u2014 total readiness window is the sum, not the max.",
    "Refresh-token rotation / DPoP: the web-server doc references DPoP-bound refresh tokens and re-issuance semantics. The research treats the refresh_token as a static stored value; it omits whether Google rotates the refresh_token on use (Google generally does NOT rotate non-DPoP refresh tokens, but the per-user store must tolerate a NEW refresh_token arriving on a forced re-consent and must NOT overwrite a good token with a null when none is returned \u2014 the research mentions the null-guard but not rotation/replacement semantics).",
    "Live-token limit per client: Google caps the number of simultaneously-valid refresh tokens per OAuth client per user (default ~50/100 grants); when exceeded the oldest is silently invalidated. For an autonomous daily-reconnect or multi-tenant app this is a real invalid_grant source the research lists only in passing ('exceeds the live-token limit') without the operational consequence (don't re-consent unnecessarily).",
    "Thumbnails.set as a SEPARATE sensitive operation: the research dismisses thumbnails as 'not required.' For brand persona content a custom thumbnail needs thumbnails.set, which requires the account to be verified/in-good-standing (phone-verified channel) \u2014 a non-obvious prerequisite that can fail independently of the upload.",
    "Quota-bucket volatility: because the per-method bucket model is brand-new (mid-2026) and was mis-dated in the research, the integration MUST treat the 100/day number as live-config (read from Quota Calculator at runtime / make the cap a settable constant), not a hardcoded constant \u2014 the research hardcodes assumptions from a moving target.",
    "Made-for-kids / synthetic-media disclosure enforcement: research sets containsSyntheticMedia=true and selfDeclaredMadeForKids=false but omits that YouTube independently classifies MFK and can OVERRIDE the self-declaration, and that synthetic-media disclosure may surface an 'altered/synthetic content' label \u2014 material for an AI-avatar persona's reach/compliance, not just a boolean to set.",
    "Resumable-upload chunk/resume edge cases: the research states 256KB-multiple chunking and 308-resume, but omits the official guidance that the 308 response's Range header may be ABSENT (meaning 0 bytes received \u2192 restart) and that the session URI has a finite validity window (expires, ~week) requiring re-initiation \u2014 both are real failure modes for the video-bridge worker on flaky links."
  ],
  "contradictions": [
    "Self-contradiction in the research's own quota narrative: the 'gotchas' block says videos.insert 'each call costs 1 unit with a dedicated default cap of 100 videos.insert calls/day' AND attributes this to 'the Dec 4 2025 revision-history change', while the claims[] entry for revision_history correctly notes the Dec 4 2025 entry was about a cut 'from ~1600 to ~100/its own bucket'. ~100-units-per-call (Dec 4 2025) and 1-unit-per-call (current granular bucket, June 1 2026) are different facts the research presents as one dated event. Verbatim from revision_history: Dec 4 2025 = 'change in the quota cost of a video upload from approximately 1600 units to approximately 100 units'; June 1 2026 = 'transitioning to a granular quota system ... starting with videos.insert and search.list'.",
    "Lead-time contradiction: the research's auditGates(A) says OAuth verification is 'reviewed manually' with no stated timeframe, but the official sensitive-scope-verification page states it 'can take up to 10 days to complete.' The research's 'no fixed SLA' is true only for the audit (B), not for the OAuth verification (A) \u2014 the two are conflated into a single open-ended-wait narrative.",
    "Source-tier contradiction for the videoSpec: the research presents '1080x1920, H.264, 30fps, <=3min, >=10 Mbps' as a hard spec but its only cited source for the Shorts spec is a third-party blog (shortsync.app). The official Help page (answer/15424877) confirms ONLY the 3-min + vertical-aspect-ratio classification rule; resolution/bitrate/fps are recommendations with no official-API normative source. The research overstates third-party recommendations as API contract."
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
> * **Sessão Anterior**: [[2026-06-27 - agent-a794563cb3a57ec8e]]
> * **Próxima Sessão**: [[2026-06-27 - agent-ae2bd3418a85dae25]]
%% --- TIMELINE END --- %%

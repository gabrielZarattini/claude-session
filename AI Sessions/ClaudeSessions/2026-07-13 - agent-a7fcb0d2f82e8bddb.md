# Session agent-a7fcb0d2f82e8bddb
**Date:** 2026-07-13 | **Session ID:** `agent-a7fcb0d2f82e8bddb`

---

## 👤 User *(21:52:59)*

Focused security review of ONE change in the repo at /home/gcrUX/htdocs/constellation-orchestra. The change adds an optional `text_beats` + `caption_mode` input to a Supabase Deno edge function and lets it flow to a video render worker.

In scope (read these):
1. supabase/functions/video-repurpose-run/index.ts — I added `sanitizeBeats()` + `caption_mode`/`text_beats` to `sanitizeClips()` (the NEW input surface). Verify: is the new input BOUNDED and VALIDATED (array length cap, phrase length cap, numeric timing checks, emphasis allowlist)? Is the master still resolved OWNER-SCOPED (.eq user_id)? Does any client-supplied value reach an unsafe sink?
2. Trace where `text_beats.phrase` ends up: composition jsonb → scripts/video-repurpose-bridge.ts (worker) → scripts/video-repurpose/segment-core.ts (the 'beats' branch) → renderAlphaFrames → scripts/hyperframes/templates/viral-caption-overlay-9x16.html. CRITICAL: does `phrase` reach an FFmpeg drawtext/shell arg (command injection risk), OR only the HTML template via textContent (XSS-safe)? Confirm which.
3. Does `phrase` ever get interpolated into a shell command, an FFmpeg filter string, or a file path in segment-core.ts? (The overlay path uses a PNG sequence + FFmpeg overlay — confirm phrase is NOT in any ffmpeg arg.)

Look ONLY for HIGH-CONFIDENCE (≥8/10) vulnerabilities: command injection, XSS to a real sink, path traversal, cross-tenant access, billing bypass. 

EXCLUSIONS: DoS/resource-exhaustion, rate-limiting, regex-DoS, lack-of-hardening, prompt-injection-into-LLM, log spoofing, theoretical races, findings in docs/markdown.

Output: either the ≥8-confidence findings (file:line, category, exploit path, fix) or "NO FINDINGS" + the 3-4 verified properties (bounded input, owner-scoping, textContent XSS-safe sink, phrase-not-in-ffmpeg-arg). Be precise, no padding.

## 🤖 Claude *(21:53:01)*


## 🤖 Claude *(21:53:02)*

I'll start by reading the in-scope files to trace the new input surface.

## 🤖 Claude *(21:53:03)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-repurpose-run/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// video-repurpose-run — enqueue a segmentation job (video-repurpose Fatia 2, FR-VR-003).
> 2	// ─────────────────────────────────────────────────────────────────────────────
> 3	// A source master (creative_assets kind='video', typically source_module='external') + a data-driven cut-spec →
> 4	// a video_renders row (engine='repurpose', charged_mco=0 — FFmpeg rail is free). The host worker
> 5	// (scripts/video-repurpose-bridge.ts) claims it, cuts N vertical shorts, registers each as a creative_asset
> 6	// (parent_asset_id = the master) and finalizes. Async: returns render_id; the client polls video_renders (RLS own).
> 7	//
> 8	// SECURITY: user-JWT → getUser → the source asset is resolved OWNER-SCOPED (.eq id .eq user_id); its bucket/key are
> 9	// re-validated (allowlist + `${uid}/` prefix + no `..`) BEFORE landing in the composition (defense-in-depth at
> 10	// enqueue; the worker re-validates AGAIN at read time — OTD-VR-006). SSOT: docs/bok/video-repurpose/00-*.md.
> 11	
> 12	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 13	
> 14	const corsHeaders = {
> 15	  "Access-Control-Allow-Origin": "*",
> 16	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 17	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> 18	};
> 19	
> 20	const ALLOWED_BUCKETS = new Set(["canvas-assets", "video-studio-assets"]);
> 21	const MAX_CLIPS = 50;
> 22	const MAX_SLIDES = 10;   // IG carousel max
> 23	const REFRAMES = new Set(["9:16", "1:1"]);
> 24	const CAPTION_MODES = new Set(["beats", "drawtext", "none"]);   // FR-VR-011/014
> 25	const EMPHASES = new Set(["hook", "punch", "normal"]);
> 26	const MAX_BEATS = 12;    // per clip
> 27	
> 28	interface TextBeatIn { t_start: number; t_end: number; phrase: string; emphasis?: string }
> 29	interface ClipIn { in_sec: number; out_sec: number; caption?: string; reframe?: string; caption_mode?: string; text_beats?: TextBeatIn[] }
> 30	interface SlideIn { t_sec: number; caption?: string }
> 31	
> 32	// FR-VR-011: validate punctual motion-graphic beats against the clip window; drop malformed (never fabricate).
> 33	function sanitizeBeats(raw: unknown, clipDur: number): TextBeatIn[] {
> 34	  if (!Array.isArray(raw)) return [];
> 35	  const out: TextBeatIn[] = [];
> 36	  for (const b of raw.slice(0, MAX_BEATS)) {
> 37	    const ts = Number((b as TextBeatIn)?.t_start), te = Number((b as TextBeatIn)?.t_end);
> 38	    const phrase = typeof (b as TextBeatIn)?.phrase === "string" ? (b as TextBeatIn).phrase.slice(0, 120) : "";
> 39	    if (!phrase || !Number.isFinite(ts) || !Number.isFinite(te) || ts < 0 || te <= ts || te > clipDur + 0.05) continue;
> 40	    const emphasis = EMPHASES.has(String((b as TextBeatIn).emphasis)) ? String((b as TextBeatIn).emphasis) : "normal";
> 41	    out.push({ t_start: ts, t_end: te, phrase, emphasis });
> 42	  }
> 43	  return out;
> 44	}
> 45	
> 46	function sanitizeClips(raw: unknown): { clips: ClipIn[]; error?: string } {
> 47	  if (!Array.isArray(raw) || raw.length === 0) return { clips: [], error: "cut_spec_empty" };
> 48	  if (raw.length > MAX_CLIPS) return { clips: [], error: "too_many_clips" };
> 49	  const clips: ClipIn[] = [];
> 50	  for (const c of raw) {
> 51	    const inS = Number((c as ClipIn)?.in_sec), outS = Number((c as ClipIn)?.out_sec);
> 52	    if (!Number.isFinite(inS) || !Number.isFinite(outS) || inS < 0 || outS <= inS) return { clips: [], error: "clip_range_invalid" };
> 53	    const caption = typeof (c as ClipIn).caption === "string" ? (c as ClipIn).caption!.slice(0, 300) : undefined;
> 54	    const reframe = REFRAMES.has(String((c as ClipIn).reframe)) ? (c as ClipIn).reframe : "9:16";
> 55	    const cmRaw = String((c as ClipIn).caption_mode ?? "");
> 56	    const caption_mode = CAPTION_MODES.has(cmRaw) ? cmRaw : undefined;
> 57	    const text_beats = caption_mode === "beats" ? sanitizeBeats((c as ClipIn).text_beats, outS - inS) : undefined;
> 58	    clips.push({ in_sec: inS, out_sec: outS, caption, reframe, caption_mode, text_beats });
> 59	  }
> 60	  return { clips };
> 61	}
> 62	
> 63	function sanitizeSlides(raw: unknown): { slides: SlideIn[]; error?: string } {
> 64	  if (!Array.isArray(raw) || raw.length === 0) return { slides: [], error: "slide_spec_empty" };
> 65	  if (raw.length > MAX_SLIDES) return { slides: [], error: "too_many_slides" };
> 66	  const slides: SlideIn[] = [];
> 67	  for (const s of raw) {
> 68	    const t = Number((s as SlideIn)?.t_sec);
> 69	    if (!Number.isFinite(t) || t < 0) return { slides: [], error: "slide_time_invalid" };
> 70	    const caption = typeof (s as SlideIn).caption === "string" ? (s as SlideIn).caption!.slice(0, 300) : undefined;
> 71	    slides.push({ t_sec: t, caption });
> 72	  }
> 73	  return { slides };
> 74	}
> 75	
> 76	Deno.serve(async (req) => {
> 77	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 78	  const json = (status: number, body: unknown) =>
> 79	    new Response(JSON.stringify(body), { status, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 80	
> 81	  try {
> 82	    const authHeader = req.headers.get("Authorization");
> 83	    if (!authHeader?.startsWith("Bearer ")) return json(401, { error: "Unauthorized" });
> 84	
> 85	    const userClient = createClient(
> 86	      Deno.env.get("SUPABASE_URL")!,
> 87	      (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!,
> 88	      { global: { headers: { Authorization: authHeader } } },
> 89	    );
> 90	    const { data: { user } } = await userClient.auth.getUser();
> 91	    if (!user) return json(401, { error: "Unauthorized" });
> 92	
> 93	    const body = await req.json().catch(() => ({}));
> 94	    const sourceAssetId = typeof body.source_asset_id === "string" ? body.source_asset_id : "";
> 95	    if (!sourceAssetId) return json(400, { error: "source_asset_id_required" });
> 96	    const mode = body.mode === "carousel" || Array.isArray(body.slides) ? "carousel" : "repurpose";
> 97	
> 98	    let clips: ClipIn[] = [], slides: SlideIn[] = [];
> 99	    if (mode === "carousel") {
> 100	      const r = sanitizeSlides(body.slides);
> 101	      if (r.error) return json(422, { error: r.error, action: "Cada slide precisa de t_sec ≥ 0 (≤10 slides)." });
> 102	      slides = r.slides;
> 103	    } else {
> 104	      const r = sanitizeClips(body.clips);
> 105	      if (r.error) return json(422, { error: r.error, action: "Cada corte precisa de in_sec < out_sec (≤50 cortes)." });
> 106	      clips = r.clips;
> 107	    }
> 108	    const fps = Number.isFinite(body.fps) && body.fps >= 1 && body.fps <= 60 ? Math.round(body.fps) : 30;
> 109	    const handle = typeof body.handle === "string" ? body.handle.slice(0, 40) : undefined;
> 110	
> 111	    const admin = createClient(
> 112	      Deno.env.get("SUPABASE_URL")!,
> 113	      (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
> 114	    );
> 115	
> 116	    // Resolve the source OWNER-SCOPED (server-trusted bucket/key; the .eq user_id is the tenant gate).
> 117	    const { data: asset } = await admin.from("creative_assets")
> 118	      .select("id, user_id, kind, storage_bucket, storage_key")
> 119	      .eq("id", sourceAssetId).eq("user_id", user.id).maybeSingle();
> 120	    if (!asset) return json(404, { error: "source_not_found", action: "O vídeo-fonte não existe ou não é seu." });
> 121	    if (asset.kind !== "video") return json(422, { error: "source_not_video" });
> 122	    const bucket = asset.storage_bucket as string, key = asset.storage_key as string;
> 123	    if (bucket === "local") {
> 124	      // Host-local master → ADMIN-ONLY (Sovereign directive 2026-07-12). The worker reads it from
> 125	      // repurpose-inbox/<uid>/ with a real-path containment guard; free-plan Supabase can't hold the master.
> 126	      const { data: adminRow } = await admin.from("user_roles").select("role").eq("user_id", user.id).eq("role", "admin").maybeSingle();
> 127	      if (!adminRow) return json(403, { error: "admin_only", action: "Repurpose de arquivo do host é restrito a administradores." });
> 128	    } else if (!ALLOWED_BUCKETS.has(bucket)) {
> 129	      return json(400, { error: "source_ref_invalid" });   // defense-in-depth; the worker re-checks (OTD-VR-006)
> 130	    }
> 131	    if (!key.startsWith(`${user.id}/`) || key.includes("..")) {
> 132	      return json(400, { error: "source_ref_invalid" });
> 133	    }
> 134	
> 135	    const composition = mode === "carousel"
> 136	      ? { mode, source: { bucket, key }, source_asset_id: asset.id, slides, handle }
> 137	      : { mode, source: { bucket, key }, source_asset_id: asset.id, clips, fps };
> 138	
> 139	    const { data: render, error: insErr } = await admin.from("video_renders").insert({
> 140	      user_id: user.id, engine: "repurpose", charged_mco: 0, composition,
> 141	    }).select("id").single();
> 142	    if (insErr || !render) return json(500, { error: "enqueue_failed", detail: insErr?.message });
> 143	
> 144	    return json(202, {
> 145	      ok: true, render_id: render.id, mode,
> 146	      count: mode === "carousel" ? slides.length : clips.length,
> 147	      transport: `poll://${render.id}`,
> 148	    });
> 149	  } catch (e) {
> 150	    console.error("video-repurpose-run error:", e);
> 151	    return json(500, { error: e instanceof Error ? e.message : "Unknown error" });
> 152	  }
> 153	});
> 154	
> ```

## 🤖 Claude *(21:53:05)*


## 🤖 Claude *(21:53:05)*

Now let me trace the composition into the worker and segment-core.

## 🤖 Claude *(21:53:06)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/video-repurpose-bridge.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env bun
> 2	/**
> 3	 * scripts/video-repurpose-bridge.ts
> 4	 *
> 5	 * video-repurpose worker (Fatia 2) — host worker that polls `video_renders` (engine='repurpose', state='queued'),
> 6	 * atomically claims each, downloads the source master, cuts N vertical shorts (segment-core.ts: 16:9→9:16/1:1
> 7	 * reframe + burned caption), uploads each to the private bucket, registers each as a creative_asset (parent = the
> 8	 * master, so the sink publish-space-asset can publish them), and finalizes via finalize_video_render.
> 9	 *
> 10	 * BoK SSOT: docs/bok/video-repurpose/00-deepsearch-blueprint.md §Pilar II + §8. Pattern: mirrors scripts/video-bridge.ts.
> 11	 * SECURITY (OTD-VR-006): the source (bucket,key) from the composition is RE-VALIDATED at read time (allowlist +
> 12	 * `${user_id}/` prefix + no `..`) — never trust the stored row. charged_mco is 0 (free FFmpeg rail).
> 13	 *
> 14	 * Supervisor: systemd --user video-repurpose-bridge.service (ação Sovereign). Usage: bun run scripts/video-repurpose-bridge.ts [--once]
> 15	 */
> 16	
> 17	import { createClient } from '@supabase/supabase-js';
> 18	import { existsSync, readFileSync, writeFileSync, rmSync, mkdirSync, realpathSync } from 'fs';
> 19	import { join, dirname, resolve } from 'path';
> 20	import { fileURLToPath } from 'url';
> 21	import { segmentVideo, type ClipSpec } from './video-repurpose/segment-core.ts';
> 22	import { buildCarousel, type SlideSpec } from './video-repurpose/carousel-core.ts';
> 23	
> 24	const __dirname = dirname(fileURLToPath(import.meta.url));
> 25	const envPath = join(__dirname, '../.env');
> 26	if (existsSync(envPath)) {
> 27	  for (const line of readFileSync(envPath, 'utf-8').split('\n')) {
> 28	    const m = line.match(/^([^#=\s][^=]*)=(.*)$/);
> 29	    if (m) process.env[m[1].trim()] = m[2].trim().replace(/^["']|["']$/g, '');
> 30	  }
> 31	}
> 32	const SUPABASE_URL = process.env.SUPABASE_URL;
> 33	const SERVICE_KEY = process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY;
> 34	if (!SUPABASE_URL || !SERVICE_KEY) { console.error('❌ Missing SUPABASE_URL or SB_SECRET_KEY in .env'); process.exit(1); }
> 35	const supabase = createClient(SUPABASE_URL, SERVICE_KEY, { auth: { persistSession: false } });
> 36	
> 37	const OUT_BUCKET = 'video-studio-assets';
> 38	const ALLOWED_SRC_BUCKETS = new Set(['canvas-assets', 'video-studio-assets']);
> 39	// Host inbox for large external masters. The free-plan Supabase caps uploads at 50MB → a full documentary can't
> 40	// go to Storage, so the master lives on host disk (uploaded via CloudPanel to repurpose-inbox/<uid>/) and the
> 41	// worker reads it locally. Only the small cortes (<50MB) go to Supabase. resolve() = canonical absolute base.
> 42	const INBOX_BASE = resolve(__dirname, '../repurpose-inbox');
> 43	const POLL_MS = 4000;
> 44	const RUNNING_TIMEOUT_MS = 15 * 60 * 1000; // repurpose can be long (N re-encodes) — generous dead-worker reaper
> 45	
> 46	function logHealth(status: string, event: string, metadata?: Record<string, unknown>) {
> 47	  return supabase.from('infra_health_logs').insert({ service: 'video-repurpose-bridge', status, event, metadata: metadata ?? null }).then(() => {}, () => {});
> 48	}
> 49	
> 50	async function claim(renderId: string) {
> 51	  const { data } = await supabase.from('video_renders')
> 52	    .update({ state: 'running', updated_at: new Date().toISOString() })
> 53	    .eq('id', renderId).eq('state', 'queued')
> 54	    .select('id, user_id, charged_mco, composition').maybeSingle();
> 55	  return data ?? null;
> 56	}
> 57	
> 58	interface Composition { mode?: string; source?: { bucket?: string; key?: string }; source_asset_id?: string; clips?: ClipSpec[]; slides?: SlideSpec[]; handle?: string; fps?: number }
> 59	type ManifestItem = { index: number; storage_key: string; width: number; height: number; bytes: number; kind: 'video' | 'image' };
> 60	
> 61	async function processRepurpose(row: { id: string; user_id: string; charged_mco: number; composition: unknown }) {
> 62	  const renderId = row.id;
> 63	  const charged = row.charged_mco ?? 0;
> 64	  const workDir = `/tmp/repurpose-${renderId}`;
> 65	  const srcPath = `${workDir}/source.mp4`;
> 66	  try {
> 67	    const comp = row.composition as Composition | null;
> 68	    const mode = comp?.mode === 'carousel' ? 'carousel' : 'repurpose';
> 69	    if (!comp || !comp.source?.bucket || !comp.source?.key) throw new Error('composition_missing_or_invalid');
> 70	    if (mode === 'repurpose' && (!Array.isArray(comp.clips) || comp.clips.length === 0)) throw new Error('cut_spec_empty');
> 71	    if (mode === 'carousel' && (!Array.isArray(comp.slides) || comp.slides.length === 0)) throw new Error('slide_spec_empty');
> 72	    // OTD-VR-006 — re-validate the source ref at READ time; never trust the stored composition row.
> 73	    const bucket = comp.source.bucket, key = comp.source.key;
> 74	    mkdirSync(join(workDir, 'out'), { recursive: true });
> 75	    let inputPath: string;
> 76	    if (bucket === 'local') {
> 77	      // Host-local master (CloudPanel upload → repurpose-inbox/<uid>/). Read from disk; no Supabase download.
> 78	      // Containment: key must be `${uid}/…`, no `..`, and the RESOLVED real path must stay strictly under
> 79	      // INBOX_BASE (defends against symlink/traversal escaping the per-user inbox).
> 80	      if (!key.startsWith(`${row.user_id}/`) || key.includes('..')) throw new Error('source_ref_rejected');
> 81	      const candidate = join(INBOX_BASE, key);
> 82	      const real = existsSync(candidate) ? realpathSync(candidate) : '';
> 83	      if (!real || !real.startsWith(INBOX_BASE + '/')) throw new Error('local_source_not_found');
> 84	      inputPath = real;
> 85	    } else {
> 86	      if (!ALLOWED_SRC_BUCKETS.has(bucket) || !key.startsWith(`${row.user_id}/`) || key.includes('..')) {
> 87	        throw new Error('source_ref_rejected');
> 88	      }
> 89	      const { data: blob, error: dlErr } = await supabase.storage.from(bucket).download(key);
> 90	      if (dlErr || !blob) throw new Error(`source_download_failed: ${dlErr?.message ?? 'no blob'}`);
> 91	      writeFileSync(srcPath, new Uint8Array(await blob.arrayBuffer()));
> 92	      inputPath = srcPath;
> 93	    }
> 94	
> 95	    const manifest: ManifestItem[] = [];
> 96	    if (mode === 'carousel') {
> 97	      // Pilar III — key-frames → 4:5 slides (still images), registered as IMAGE assets (a set = one carousel post).
> 98	      const slides = await buildCarousel({ sourcePath: inputPath, outDir: join(workDir, 'out'), slides: comp.slides!, handle: comp.handle });
> 99	      for (const s of slides) {
> 100	        const slideKey = `${row.user_id}/repurpose/${renderId}/slide_${String(s.index).padStart(3, '0')}.jpg`;
> 101	        const { error: upErr } = await supabase.storage.from(OUT_BUCKET).upload(slideKey, readFileSync(s.path), { contentType: 'image/jpeg', upsert: true });
> 102	        if (upErr) throw new Error(`slide_upload_failed[${s.index}]: ${upErr.message}`);
> 103	        await supabase.rpc('register_creative_asset', {
> 104	          p_user_id: row.user_id, p_kind: 'image',
> 105	          p_storage_bucket: OUT_BUCKET, p_storage_key: slideKey, p_is_public: false,
> 106	          p_source_module: 'hyperframes', p_source_job_id: renderId, p_parent_asset_id: comp.source_asset_id ?? null,
> 107	          p_mime_type: 'image/jpeg', p_file_size_bytes: s.bytes, p_width: s.width, p_height: s.height,
> 108	          p_title: `Carrossel slide #${s.index + 1}`,
> 109	          p_metadata: { carousel: true, source_asset_id: comp.source_asset_id ?? null, slide_index: s.index, render_id: renderId },
> 110	        }).then((r) => { if (r.error) console.warn(`[carousel] register slide ${s.index} skipped:`, r.error.message); }, () => {});
> 111	        manifest.push({ index: s.index, storage_key: slideKey, width: s.width, height: s.height, bytes: s.bytes, kind: 'image' });
> 112	      }
> 113	    } else {
> 114	      // Pilar II — trim/reframe/caption → N vertical shorts, registered as VIDEO assets.
> 115	      const clips = await segmentVideo({ sourcePath: inputPath, outDir: join(workDir, 'out'), fps: comp.fps ?? 30, clips: comp.clips! });
> 116	      for (const c of clips) {
> 117	        const clipKey = `${row.user_id}/repurpose/${renderId}/clip_${String(c.index).padStart(3, '0')}.mp4`;
> 118	        const { error: upErr } = await supabase.storage.from(OUT_BUCKET).upload(clipKey, readFileSync(c.path), { contentType: 'video/mp4', upsert: true });
> 119	        if (upErr) throw new Error(`clip_upload_failed[${c.index}]: ${upErr.message}`);
> 120	        await supabase.rpc('register_creative_asset', {
> 121	          p_user_id: row.user_id, p_kind: 'video',
> 122	          p_storage_bucket: OUT_BUCKET, p_storage_key: clipKey, p_is_public: false,
> 123	          p_source_module: 'hyperframes', p_source_job_id: renderId, p_parent_asset_id: comp.source_asset_id ?? null,
> 124	          p_mime_type: 'video/mp4', p_file_size_bytes: c.bytes, p_width: c.width, p_height: c.height, p_duration_seconds: c.durationSec,
> 125	          p_title: `Short ${c.width}x${c.height} #${c.index + 1}`,
> 126	          p_metadata: { repurpose: true, source_asset_id: comp.source_asset_id ?? null, clip_index: c.index, render_id: renderId },
> 127	        }).then((r) => { if (r.error) console.warn(`[repurpose] register clip ${c.index} skipped:`, r.error.message); }, () => {});
> 128	        manifest.push({ index: c.index, storage_key: clipKey, width: c.width, height: c.height, bytes: c.bytes, kind: 'video' });
> 129	      }
> 130	    }
> 131	
> 132	    let nodeId: string | null = null;
> 133	    const { data: node } = await supabase.from('mcorch_nodes').insert({
> 134	      user_id: row.user_id, node_type: 'observation', name: `video-repurpose:${renderId}`,
> 135	      content: `Repurpose (${mode}) ${manifest.length} asset(s) from master ${comp.source_asset_id ?? '(?)'}.`,
> 136	      metadata: { kind: 'video_repurpose', mode, render_id: renderId, items: manifest },
> 137	    }).select('id').maybeSingle();
> 138	    nodeId = node?.id ?? null;
> 139	
> 140	    const { data: fin } = await supabase.rpc('finalize_video_render', {
> 141	      p_render_id: renderId, p_state: 'done', p_storage_key: manifest[0]?.storage_key ?? null,
> 142	      p_qa: { clips: manifest }, p_node_id: nodeId, p_refund: 0,
> 143	    });
> 144	    console.log(`✅ repurpose ${renderId} → ${manifest.length} clip(s)`, fin);
> 145	    await logHealth('healthy', 'repurpose_done', { render_id: renderId, clips: manifest.length });
> 146	  } catch (e) {
> 147	    const msg = e instanceof Error ? e.message : String(e);
> 148	    console.error(`❌ repurpose ${renderId} failed: ${msg}`);
> 149	    await supabase.rpc('finalize_video_render', { p_render_id: renderId, p_state: 'failed', p_storage_key: null, p_qa: null, p_node_id: null, p_refund: charged }).then(() => {}, () => {});
> 150	    await logHealth('error', 'repurpose_failed', { render_id: renderId, error: msg });
> 151	  } finally {
> 152	    rmSync(workDir, { recursive: true, force: true });
> 153	  }
> 154	}
> 155	
> 156	async function drainOnce(): Promise<number> {
> 157	  const cutoff = new Date(Date.now() - RUNNING_TIMEOUT_MS).toISOString();
> 158	  await supabase.from('video_renders').update({ state: 'queued' })
> 159	    .eq('engine', 'repurpose').eq('state', 'running').lt('updated_at', cutoff).then(() => {}, () => {});
> 160	
> 161	  const { data: queued } = await supabase.from('video_renders')
> 162	    .select('id').eq('engine', 'repurpose').eq('state', 'queued').order('created_at', { ascending: true }).limit(5);
> 163	  if (!queued?.length) return 0;
> 164	  let n = 0;
> 165	  for (const q of queued) {
> 166	    const row = await claim(q.id);
> 167	    if (!row) continue;
> 168	    await processRepurpose(row as any);
> 169	    n++;
> 170	  }
> 171	  return n;
> 172	}
> 173	
> 174	async function main() {
> 175	  if (process.argv.includes('--once')) {
> 176	    const n = await drainOnce();
> 177	    console.log(`drained ${n} repurpose render(s)`);
> 178	    process.exit(0);
> 179	  }
> 180	  console.log('🎬 video-repurpose-bridge running — polling video_renders (engine=repurpose, queued)...');
> 181	  await logHealth('healthy', 'worker_started');
> 182	  // eslint-disable-next-line no-constant-condition
> 183	  while (true) {
> 184	    try { await drainOnce(); } catch (e) {
> 185	      console.error('poll cycle error:', e);
> 186	      await logHealth('degraded', 'poll_error', { error: e instanceof Error ? e.message : String(e) });
> 187	    }
> 188	    await new Promise((r) => setTimeout(r, POLL_MS));
> 189	  }
> 190	}
> 191	
> 192	main();
> 193	
> ```

## 🤖 Claude *(21:53:09)*

Now the critical file — segment-core.ts, the 'beats' branch.

## 🤖 Claude *(21:53:09)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/video-repurpose/segment-core.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env bun
> 2	/**
> 3	 * scripts/video-repurpose/segment-core.ts
> 4	 *
> 5	 * The FFmpeg core of the video-repurpose engine (Fatia 2): a long 16:9 master + a data-driven cut-spec →
> 6	 * N vertical shorts (9:16 or 1:1), reframed subject-safe (center-crop) with an optional burned caption.
> 7	 *
> 8	 * BoK SSOT: docs/bok/video-repurpose/00-deepsearch-blueprint.md §Pilar II (FR-VR-003/004/005).
> 9	 * PROVEN offline 2026-07-12 (Vision QA): a synthetic 16:9 master with ESQ|CENTRO|DIR labels → the 9:16 center-crop
> 10	 * kept CENTRO, dropped the side labels, and burned the caption at the base. Deterministic FFmpeg — no LLM in the core.
> 11	 *
> 12	 * Reframe is source-agnostic (expression crop): for a target aspect ar, keep the largest centered rect of that aspect.
> 13	 * Caption is written to a per-clip textfile → drawtext `textfile=` (avoids the `:'%\` escaping trap of inline text).
> 14	 * Cut is re-encoded (`-ss <in> -i -t <dur>`) → frame-accurate (the reframe re-encodes anyway).
> 15	 */
> 16	
> 17	import { spawn } from 'node:child_process';
> 18	import { writeFileSync, mkdirSync, statSync, existsSync, mkdtempSync, rmSync } from 'node:fs';
> 19	import { join } from 'node:path';
> 20	import { tmpdir } from 'node:os';
> 21	import { renderAlphaFrames } from '../hyperframes/render-core.ts';
> 22	
> 23	const FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf';
> 24	
> 25	export type Reframe = '9:16' | '1:1';
> 26	export interface TextBeat { t_start: number; t_end: number; phrase: string; emphasis?: 'hook' | 'punch' | 'normal' }
> 27	export interface ClipSpec {
> 28	  in_sec: number;
> 29	  out_sec: number;
> 30	  caption?: string;          // burned bottom-center caption (drawtext textfile); omit for none
> 31	  reframe?: Reframe;         // default '9:16'
> 32	  // FR-VR-011/014: 'beats' = punctual motion-graphic overlay (viral-caption-overlay-9x16); default legacy drawtext.
> 33	  caption_mode?: 'beats' | 'drawtext' | 'none';
> 34	  text_beats?: TextBeat[];   // clip-relative beats for caption_mode='beats'
> 35	}
> 36	export interface SegmentSpec {
> 37	  sourcePath: string;        // local path to the master MP4
> 38	  clips: ClipSpec[];
> 39	  outDir: string;
> 40	  fps?: number;              // default 30 (CFR)
> 41	}
> 42	export interface ClipResult {
> 43	  index: number; path: string; width: number; height: number; durationSec: number; bytes: number;
> 44	}
> 45	
> 46	const TARGET: Record<Reframe, { w: number; h: number; ar: number }> = {
> 47	  '9:16': { w: 1080, h: 1920, ar: 9 / 16 },
> 48	  '1:1': { w: 1080, h: 1080, ar: 1 },
> 49	};
> 50	
> 51	function run(cmd: string, args: string[]): Promise<void> {
> 52	  return new Promise((resolve, reject) => {
> 53	    const p = spawn(cmd, args, { stdio: ['ignore', 'ignore', 'pipe'] });
> 54	    let err = '';
> 55	    p.stderr.on('data', (d) => { err += d.toString(); });
> 56	    p.on('error', reject);
> 57	    p.on('close', (code) => code === 0 ? resolve() : reject(new Error(`${cmd} exit ${code}: ${err.slice(-500)}`)));
> 58	  });
> 59	}
> 60	
> 61	/** Source-agnostic center-crop to `ar`, then scale to (W,H). Keeps the largest centered rect of the target aspect. */
> 62	function reframeChain(ar: number, W: number, H: number): string {
> 63	  // crop w = min(iw, ih*ar); h = min(ih, iw/ar); centered. Expressions are evaluated by FFmpeg per input dims.
> 64	  const cw = `min(iw\\,ih*${ar})`;
> 65	  const ch = `min(ih\\,iw/${ar})`;
> 66	  return `crop=${cw}:${ch}:(iw-ow)/2:(ih-oh)/2,scale=${W}:${H}:force_original_aspect_ratio=increase,crop=${W}:${H},setsar=1`;
> 67	}
> 68	
> 69	/** Cut + reframe + optional caption for ONE clip. Returns the output path. */
> 70	async function renderClip(spec: SegmentSpec, clip: ClipSpec, index: number): Promise<ClipResult> {
> 71	  const target = TARGET[clip.reframe ?? '9:16'];
> 72	  const fps = spec.fps ?? 30;
> 73	  const dur = Math.max(0.1, clip.out_sec - clip.in_sec);
> 74	  const outPath = join(spec.outDir, `clip_${String(index).padStart(3, '0')}.mp4`);
> 75	  const reframe = reframeChain(target.ar, target.w, target.h);
> 76	
> 77	  // FR-VR-011: motion-graphic "text beats" — render the transparent (RGBA) text layer, composite OVER the
> 78	  // reframed footage in a single pass (reframe [0:v] → overlay the alpha PNG seq [1:v]). Not the drawtext bar.
> 79	  if (clip.caption_mode === 'beats' && clip.text_beats && clip.text_beats.length) {
> 80	    const alphaDir = mkdtempSync(join(tmpdir(), 'vr-beats-'));
> 81	    try {
> 82	      await renderAlphaFrames(
> 83	        { template: 'viral-caption-overlay-9x16', props: { beats: clip.text_beats }, duration_s: dur, fps, width: target.w, height: target.h },
> 84	        alphaDir,
> 85	      );
> 86	      await run('ffmpeg', [
> 87	        '-y', '-hide_banner', '-loglevel', 'error',
> 88	        // `-ss`+`-t` are INPUT options for input 0 (the master) — MUST precede its `-i`, else `-t` binds to the
> 89	        // next input (the PNG seq) and the master plays to EOF (→ a ~500s file). eof_action=pass then harmless.
> 90	        '-ss', String(clip.in_sec), '-t', String(dur), '-i', spec.sourcePath,
> 91	        '-framerate', String(fps), '-i', join(alphaDir, 'f_%05d.png'),
> 92	        '-filter_complex', `[0:v]${reframe}[bg];[bg][1:v]overlay=0:0:format=auto:eof_action=pass[v]`,
> 93	        '-map', '[v]', '-map', '0:a?', '-r', String(fps),
> 94	        '-c:v', 'libx264', '-preset', 'medium', '-pix_fmt', 'yuv420p',
> 95	        '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart',
> 96	        outPath,
> 97	      ]);
> 98	    } finally {
> 99	      rmSync(alphaDir, { recursive: true, force: true });
> 100	    }
> 101	    const bytes = statSync(outPath).size;
> 102	    return { index, path: outPath, width: target.w, height: target.h, durationSec: dur, bytes };
> 103	  }
> 104	
> 105	  // Legacy path: reframe + optional burned drawtext caption (caption_mode 'drawtext'/undefined).
> 106	  let vf = reframe;
> 107	  if (clip.caption && clip.caption.trim() && clip.caption_mode !== 'none') {
> 108	    // textfile avoids inline-escaping; drawtext reads UTF-8. Bottom-center with a translucent box.
> 109	    const capPath = join(spec.outDir, `cap_${index}.txt`);
> 110	    // drawtext(textfile) in this ffmpeg build truncates the rendered text by the number of EXTRA UTF-8 bytes
> 111	    // (byteLen − codepointLen) — a byte-vs-char bug that clips accented captions' tails ("notícia." → "notíc").
> 112	    // Pad with that many trailing spaces so the truncation eats the padding, not the caption (proven via Vision QA).
> 113	    const cap = clip.caption.trim();
> 114	    const capPad = Buffer.byteLength(cap, 'utf8') - [...cap].length;
> 115	    writeFileSync(capPath, cap + ' '.repeat(Math.max(0, capPad)));
> 116	    const fontsize = Math.round(target.w * 0.045);
> 117	    vf += `,drawtext=textfile='${capPath}':fontfile=${FONT}:fontsize=${fontsize}:fontcolor=white:` +
> 118	      `box=1:boxcolor=black@0.55:boxborderw=14:x=(w-tw)/2:y=h-th-${Math.round(target.h * 0.08)}`;
> 119	  }
> 120	
> 121	  await run('ffmpeg', [
> 122	    '-y', '-hide_banner', '-loglevel', 'error',
> 123	    '-ss', String(clip.in_sec), '-i', spec.sourcePath, '-t', String(dur),
> 124	    '-vf', vf, '-r', String(fps),
> 125	    '-c:v', 'libx264', '-preset', 'medium', '-pix_fmt', 'yuv420p',
> 126	    '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart',
> 127	    outPath,
> 128	  ]);
> 129	
> 130	  const bytes = statSync(outPath).size;
> 131	  return { index, path: outPath, width: target.w, height: target.h, durationSec: dur, bytes };
> 132	}
> 133	
> 134	/** Segment a master into N clips per the cut-spec. Serial (deterministic, memory-safe for a long master). */
> 135	export async function segmentVideo(spec: SegmentSpec): Promise<ClipResult[]> {
> 136	  if (!existsSync(spec.sourcePath)) throw new Error(`source_not_found: ${spec.sourcePath}`);
> 137	  if (!Array.isArray(spec.clips) || spec.clips.length === 0) throw new Error('cut_spec_empty');
> 138	  mkdirSync(spec.outDir, { recursive: true });
> 139	  const out: ClipResult[] = [];
> 140	  for (let i = 0; i < spec.clips.length; i++) {
> 141	    const c = spec.clips[i];
> 142	    if (!(c.out_sec > c.in_sec) || c.in_sec < 0) throw new Error(`clip_${i}_invalid_range`);
> 143	    out.push(await renderClip(spec, c, i));
> 144	  }
> 145	  return out;
> 146	}
> 147	
> ```

## 🤖 Claude *(21:53:18)*


## 🤖 Claude *(21:53:18)*

Now the sink chain: render-core.ts and the HTML template.

## 🤖 Claude *(21:53:19)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/hyperframes/render-core.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env bun
> 2	/**
> 3	 * scripts/hyperframes/render-core.ts
> 4	 *
> 5	 * HyperFrames deterministic render engine: a composition spec → 9:16 1080×1920 MP4.
> 6	 * BoK SSOT: docs/bok/video-studio/04-frd.md FR-VS-024 (deterministic HTML→MP4 via headless Chrome + FFmpeg)
> 7	 *           + FR-VS-025 (per-render sandbox) · viral-autopilot FR-VA-023/024 · SOP autopilot-video-9x16.md.
> 8	 *
> 9	 * Pipeline (no AI leg — fully deterministic, NFR-VS-016):
> 10	 *   1. Playwright Chromium headless, viewport 1080×1920, deviceScaleFactor 1.
> 11	 *   2. Load templates/<template>.html (file://), inject props via applyProps (textContent → XSS-safe).
> 12	 *   3. For each of N = duration_s × fps frames: applyFrame(i, N) → page.screenshot(PNG).
> 13	 *   4. FFmpeg: PNG sequence → H.264 yuv420p MP4, fixed fps, -fflags +bitexact (reproducible).
> 14	 *
> 15	 * This is the renderer CORE — pure (no DB, no network beyond the product image). The host worker
> 16	 * (video-bridge.ts) wraps it with the queue claim + upload + finalize_video_render.
> 17	 *
> 18	 * CLI (material proof): bun run scripts/hyperframes/render-core.ts --out /tmp/test.mp4 \
> 19	 *     --hook "Sua casa limpa sozinha" --caption "Robô aspirador..." --cta "Ver no ML" --duration 4
> 20	 */
> 21	
> 22	import { chromium } from 'playwright';
> 23	import { spawn } from 'child_process';
> 24	import { mkdtempSync, rmSync, existsSync, statSync, writeFileSync, unlinkSync } from 'fs';
> 25	import { join, dirname, resolve } from 'path';
> 26	import { tmpdir } from 'os';
> 27	import { fileURLToPath } from 'url';
> 28	
> 29	const __dirname = dirname(fileURLToPath(import.meta.url));
> 30	
> 31	export interface CompositionProps {
> 32	  hook?: string;
> 33	  caption?: string;
> 34	  cta?: string;
> 35	  brand?: string;
> 36	  product_image_url?: string;
> 37	  // video-repurpose FR-VR-011/012: punctual motion-graphic "text beats" for the transparent overlay layer.
> 38	  beats?: Array<{ t_start: number; t_end: number; phrase: string; emphasis?: 'hook' | 'punch' | 'normal' }>;
> 39	}
> 40	
> 41	export interface RenderSpec {
> 42	  template?: string;        // template name under templates/ (default 'viral-short-9x16')
> 43	  props: CompositionProps;
> 44	  duration_s?: number;      // default 6
> 45	  fps?: number;             // default 30
> 46	  width?: number;           // default 1080
> 47	  height?: number;          // default 1920
> 48	}
> 49	
> 50	/**
> 51	 * Studio-authored composition (FR-VS-047, video-studio §VS-UI-B). A project the Sovereign composed in the
> 52	 * HyperFrames Studio editor — rendered by WRAPPING the reference engine `hyperframes render <dir>` (parity is
> 53	 * definitional: same engine that drives the editor preview) instead of re-implementing the GSAP/__timelines seek.
> 54	 * Kept as a discriminated union with RenderSpec via `mode:'studio-project'`; template renders (autopilot) are untouched.
> 55	 */
> 56	export interface StudioProjectSpec {
> 57	  mode: 'studio-project';
> 58	  project_dir: string;      // absolute path to the hyperframes project dir (validated under STUDIO_PROJECTS_ROOT)
> 59	  fps?: number;             // default 30
> 60	  resolution?: string;      // hyperframes preset (portrait|landscape|square|...); default 'portrait' (9:16 1080×1920)
> 61	}
> 62	
> 63	export interface RenderResult {
> 64	  outPath: string;
> 65	  bytes: number;
> 66	  width: number;
> 67	  height: number;
> 68	  frames: number;
> 69	  fps: number;
> 70	  durationMs: number;
> 71	}
> 72	
> 73	const VALID_TEMPLATES = new Set(['viral-short-9x16', 'viral-long-16x9', 'cinematic-9x16', 'viral-caption-overlay-9x16']); // allowlist — never load an arbitrary path
> 74	
> 75	function runFfmpeg(args: string[]): Promise<void> {
> 76	  return new Promise((res, rej) => {
> 77	    const p = spawn('ffmpeg', args, { stdio: ['ignore', 'ignore', 'pipe'] });
> 78	    let err = '';
> 79	    p.stderr.on('data', (d) => { err += d.toString(); });
> 80	    p.on('error', rej);
> 81	    p.on('close', (code) => (code === 0 ? res() : rej(new Error(`ffmpeg exit ${code}: ${err.slice(-800)}`))));
> 82	  });
> 83	}
> 84	
> 85	/** PNG sequence → H.264 yuv420p MP4, bitexact + metadata-stripped → byte-reproducible (NFR-VS-016). */
> 86	function encodePngFramesBitexact(frameDir: string, fps: number, outPath: string): Promise<void> {
> 87	  return runFfmpeg([
> 88	    '-y',
> 89	    '-framerate', String(fps),
> 90	    '-i', join(frameDir, 'f_%05d.png'),
> 91	    '-c:v', 'libx264',
> 92	    '-preset', 'medium',
> 93	    '-crf', '20',
> 94	    '-pix_fmt', 'yuv420p',
> 95	    '-r', String(fps),
> 96	    '-movflags', '+faststart',
> 97	    '-fflags', '+bitexact',
> 98	    '-flags:v', '+bitexact',
> 99	    '-map_metadata', '-1',
> 100	    outPath,
> 101	  ]);
> 102	}
> 103	
> 104	// ── Free "frames → video" primitive (Sovereign vision 2026-07-09) ────────────────────────────────────────────
> 105	// A Spaces node emits a sequence of pre-generated frames; HyperFrames joins them into a 9:16 MP4 via FFmpeg —
> 106	// ZERO paid API (the composition/animation layer stays 100% free). Each image is held for `seconds_per_image`,
> 107	// scaled + letterbox-padded to the canvas (no crop → the generated frame is never mutilated), concatenated to
> 108	// H.264 yuv420p, deterministic (fixed fps + bitexact flags, mirrors encodePngFramesBitexact NFR-VS-016).
> 109	export interface ImageSequenceSpec {
> 110	  images: string[];            // ordered absolute paths to pre-generated frames (PNG/JPG)
> 111	  seconds_per_image?: number;  // hold per frame in seconds (default 2.5)
> 112	  fps?: number;                // output fps (default 30)
> 113	  width?: number;              // canvas width (default 1080)
> 114	  height?: number;             // canvas height (default 1920 → 9:16)
> 115	}
> 116	
> 117	export async function encodeImageSequence(spec: ImageSequenceSpec, outPath: string): Promise<RenderResult> {
> 118	  const started = Date.now();
> 119	  const images = (spec.images ?? []).map((p) => resolve(p));
> 120	  if (images.length === 0) throw new Error('encodeImageSequence: no images provided');
> 121	  for (const p of images) if (!existsSync(p)) throw new Error(`encodeImageSequence: missing frame ${p}`);
> 122	  const fps = spec.fps ?? 30;
> 123	  const secPer = spec.seconds_per_image ?? 2.5;
> 124	  const W = spec.width ?? 1080;
> 125	  const H = spec.height ?? 1920;
> 126	
> 127	  // FFmpeg concat demuxer: hold each image for `secPer`s. The demuxer drops the final entry's duration,
> 128	  // so the last file is repeated once (documented ffmpeg quirk) to honor its hold time.
> 129	  const listDir = mkdtempSync(join(tmpdir(), 'hf-seq-'));
> 130	  const esc = (p: string) => p.replace(/'/g, "'\\''");
> 131	  const lines: string[] = [];
> 132	  for (const p of images) { lines.push(`file '${esc(p)}'`); lines.push(`duration ${secPer}`); }
> 133	  lines.push(`file '${esc(images[images.length - 1])}'`);
> 134	  const listPath = join(listDir, 'frames.txt');
> 135	  writeFileSync(listPath, lines.join('\n') + '\n');
> 136	
> 137	  try {
> 138	    await runFfmpeg([
> 139	      '-y',
> 140	      '-f', 'concat', '-safe', '0', '-i', listPath,
> 141	      // scale to fit, pad to the exact 9:16 canvas (letterbox, no crop), normalize SAR, fix fps
> 142	      '-vf', `scale=${W}:${H}:force_original_aspect_ratio=decrease,pad=${W}:${H}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps=${fps}`,
> 143	      '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
> 144	      '-pix_fmt', 'yuv420p', '-r', String(fps),
> 145	      '-movflags', '+faststart', '-fflags', '+bitexact', '-flags:v', '+bitexact', '-map_metadata', '-1',
> 146	      outPath,
> 147	    ]);
> 148	  } finally {
> 149	    rmSync(listDir, { recursive: true, force: true });
> 150	  }
> 151	  if (!existsSync(outPath) || statSync(outPath).size < 1024) throw new Error('encodeImageSequence: output missing or too small');
> 152	  const probed = await ffprobeVideo(outPath);
> 153	  return {
> 154	    outPath,
> 155	    bytes: statSync(outPath).size,
> 156	    width: probed.width,
> 157	    height: probed.height,
> 158	    frames: probed.frames,
> 159	    fps: probed.fps,
> 160	    durationMs: Date.now() - started,
> 161	  };
> 162	}
> 163	
> 164	// ── Free image-to-video (Ken Burns) — the Sovereign's "animar as imagens geradas 5-8s cada" ──────────────────
> 165	// Deterministic pan/zoom over a single still → an animated 9:16 clip via FFmpeg zoompan. ZERO paid API — the free
> 166	// substitute for neural i2v (Higgsfield DoP/Kling/Seedance), which stay as the paid opt-in. Upscale 2× first so
> 167	// zoompan's integer stepping stays smooth (documented anti-jitter trick).
> 168	export interface KenBurnsSpec {
> 169	  image: string;               // absolute path to the still to animate
> 170	  duration_s?: number;         // default 6 (the 5-8s range)
> 171	  fps?: number;                // default 30
> 172	  width?: number;              // 1080
> 173	  height?: number;             // 1920 → 9:16
> 174	  zoom?: 'in' | 'out';         // default 'in'
> 175	  max_zoom?: number;           // default 1.25
> 176	}
> 177	
> 178	export async function encodeKenBurns(spec: KenBurnsSpec, outPath: string): Promise<RenderResult> {
> 179	  const started = Date.now();
> 180	  const img = resolve(spec.image);
> 181	  if (!existsSync(img)) throw new Error(`encodeKenBurns: missing image ${img}`);
> 182	  const fps = spec.fps ?? 30;
> 183	  const dur = spec.duration_s ?? 6;
> 184	  const W = spec.width ?? 1080;
> 185	  const H = spec.height ?? 1920;
> 186	  const totalFrames = Math.round(dur * fps);
> 187	  const maxZoom = spec.max_zoom ?? 1.25;
> 188	  const step = (maxZoom - 1) / totalFrames;
> 189	  // Ramp 1 → maxZoom (in) or maxZoom → 1 (out) across the clip; `on` = output frame index (deterministic).
> 190	  const zExpr = (spec.zoom ?? 'in') === 'in'
> 191	    ? `min(zoom+${step.toFixed(6)},${maxZoom})`
> 192	    : `max(${maxZoom.toFixed(6)}-on*${step.toFixed(6)},1.0)`;
> 193	  const vf =
> 194	    `scale=${W * 2}:${H * 2},` +
> 195	    `zoompan=z='${zExpr}':d=${totalFrames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=${W}x${H}:fps=${fps},` +
> 196	    `setsar=1`;
> 197	  await runFfmpeg([
> 198	    '-y',
> 199	    '-loop', '1', '-i', img,
> 200	    '-t', String(dur),
> 201	    '-vf', vf,
> 202	    '-c:v', 'libx264', '-preset', 'medium', '-crf', '20',
> 203	    '-pix_fmt', 'yuv420p', '-r', String(fps),
> 204	    '-movflags', '+faststart', '-map_metadata', '-1',
> 205	    outPath,
> 206	  ]);
> 207	  if (!existsSync(outPath) || statSync(outPath).size < 1024) throw new Error('encodeKenBurns: output missing or too small');
> 208	  const probed = await ffprobeVideo(outPath);
> 209	  return {
> 210	    outPath,
> 211	    bytes: statSync(outPath).size,
> 212	    width: probed.width,
> 213	    height: probed.height,
> 214	    frames: probed.frames,
> 215	    fps: probed.fps,
> 216	    durationMs: Date.now() - started,
> 217	  };
> 218	}
> 219	
> 220	// ── Studio-project render (FR-VS-047 → FR-VS-050 native, SDD §VS-UI-C) ───────────────────────────────────────
> 221	// Default engine = NATIVE on @hyperframes/core (Apache-2.0, LICENSE shipped in the npm tarball — attribution:
> 222	// © HeyGen, https://github.com/heygen-com/hyperframes). The CLI wrap is kept as emergency rollback only
> 223	// (STUDIO_RENDER_ENGINE=cli) — its npm artifact ships no license grant (OTD-VS-020).
> 224	// Single-tenant Usuário Zero root (OTD-VS-019 multi-tenant deferred). Overridable by env for portability/tests.
> 225	const STUDIO_PROJECTS_ROOT = process.env.STUDIO_PROJECTS_ROOT ?? '/home/ubuntu/.mcorch/video-studio/projects';
> 226	const HF_CLI = process.env.HYPERFRAMES_CLI ?? '/home/ubuntu/.bun/install/global/node_modules/hyperframes/dist/cli.js';
> 227	const HF_NODE = process.env.HYPERFRAMES_NODE ?? '/home/ubuntu/.local/bin/node'; // node v22 (hyperframes needs >=22)
> 228	// Preset → output dimensions (mirrors the reference CLI's CANVAS_DIMENSIONS).
> 229	const RESOLUTION_DIMENSIONS: Record<string, { width: number; height: number }> = {
> 230	  portrait: { width: 1080, height: 1920 },
> 231	  landscape: { width: 1920, height: 1080 },
> 232	  square: { width: 1080, height: 1080 },
> 233	  'portrait-4k': { width: 2160, height: 3840 },
> 234	  'landscape-4k': { width: 3840, height: 2160 },
> 235	  'square-4k': { width: 2160, height: 2160 },
> 236	};
> 237	const VALID_RESOLUTIONS = new Set(Object.keys(RESOLUTION_DIMENSIONS));
> 238	
> 239	/** ffprobe a video → real dimensions/frames/fps (the renderer derives them from the composition + preset). */
> 240	function ffprobeVideo(path: string): Promise<{ width: number; height: number; frames: number; fps: number }> {
> 241	  return new Promise((res, rej) => {
> 242	    const p = spawn('ffprobe', ['-v', 'error', '-select_streams', 'v:0',
> 243	      '-show_entries', 'stream=width,height,nb_frames,r_frame_rate,duration', '-of', 'json', path],
> 244	      { stdio: ['ignore', 'pipe', 'ignore'] });
> 245	    let out = '';
> 246	    p.stdout.on('data', (d) => { out += d.toString(); });
> 247	    p.on('error', rej);
> 248	    p.on('close', (code) => {
> 249	      if (code !== 0) return rej(new Error(`ffprobe exit ${code}`));
> 250	      try {
> 251	        const s = (JSON.parse(out).streams ?? [])[0] ?? {};
> 252	        const [rn, rd] = String(s.r_frame_rate ?? '30/1').split('/').map(Number);
> 253	        const fps = rd ? rn / rd : (rn || 30);
> 254	        const frames = Number(s.nb_frames) || Math.round((Number(s.duration) || 0) * fps);
> 255	        res({ width: Number(s.width) || 0, height: Number(s.height) || 0, frames, fps });
> 256	      } catch (e) { rej(e); }
> 257	    });
> 258	  });
> 259	}
> 260	
> 261	/**
> 262	 * Render a composition spec to a deterministic 9:16 MP4 at `outPath`.
> 263	 * Throws on any failure (the worker translates that to finalize_video_render(failed, refund)).
> 264	 */
> 265	export async function renderComposition(spec: RenderSpec, outPath: string): Promise<RenderResult> {
> 266	  const t0 = Date.now();
> 267	  const template = spec.template && VALID_TEMPLATES.has(spec.template) ? spec.template : 'viral-short-9x16';
> 268	  const fps = Math.max(1, Math.min(60, spec.fps ?? 30));
> 269	  const durationS = Math.max(1, Math.min(60, spec.duration_s ?? 6));
> 270	  const width = spec.width ?? 1080;
> 271	  const height = spec.height ?? 1920;
> 272	  const totalFrames = Math.round(durationS * fps);
> 273	
> 274	  const templatePath = resolve(__dirname, 'templates', `${template}.html`);
> 275	  if (!existsSync(templatePath)) throw new Error(`template_not_found: ${template}`);
> 276	
> 277	  const frameDir = mkdtempSync(join(tmpdir(), 'hf-frames-'));
> 278	  const browser = await chromium.launch({
> 279	    headless: true,
> 280	    // Single-tenant Usuário Zero (OTD-VA-011). Multi-tenant hardening (seccomp/egress-only container) = User 1.
> 281	    args: ['--no-sandbox', '--disable-dev-shm-usage', '--force-color-profile=srgb', '--disable-lcd-text'],
> 282	  });
> 283	  try {
> 284	    const page = await browser.newPage({
> 285	      viewport: { width, height },
> 286	      deviceScaleFactor: 1,
> 287	    });
> 288	    await page.goto(`file://${templatePath}`, { waitUntil: 'load' });
> 289	    await page.evaluate((props) => (window as any).applyProps(props), spec.props as Record<string, unknown>);
> 290	
> 291	    // Deterministically wait for the product image (if any) to settle — bounded, no wallclock leakage into frames.
> 292	    await page.evaluate(() => new Promise<void>((res) => {
> 293	      const img = document.getElementById('mediaImg') as HTMLImageElement | null;
> 294	      if (!img || img.style.display === 'none' || img.complete) return res();
> 295	      const done = () => res();
> 296	      img.addEventListener('load', done, { once: true });
> 297	      img.addEventListener('error', done, { once: true });
> 298	      setTimeout(done, 8000);
> 299	    }));
> 300	
> 301	    // Frame-by-frame capture (driven by index, not time → reproducible).
> 302	    for (let i = 0; i < totalFrames; i++) {
> 303	      await page.evaluate(([idx, total]) => (window as any).applyFrame(idx, total), [i, totalFrames] as [number, number]);
> 304	      await page.screenshot({
> 305	        path: join(frameDir, `f_${String(i).padStart(5, '0')}.png`),
> 306	        clip: { x: 0, y: 0, width, height },
> 307	        animations: 'disabled',
> 308	      });
> 309	    }
> 310	    await browser.close();
> 311	
> 312	    await encodePngFramesBitexact(frameDir, fps, outPath);
> 313	
> 314	    if (!existsSync(outPath)) throw new Error('render_produced_no_file');
> 315	    const bytes = statSync(outPath).size;
> 316	    if (bytes < 100 * 1024) throw new Error(`render_too_small: ${bytes} bytes (< 100KB, Lei 1 gate)`);
> 317	
> 318	    return { outPath, bytes, width, height, frames: totalFrames, fps, durationMs: Date.now() - t0 };
> 319	  } finally {
> 320	    await browser.close().catch(() => {});
> 321	    rmSync(frameDir, { recursive: true, force: true });
> 322	  }
> 323	}
> 324	
> 325	export interface AlphaFramesResult {
> 326	  frameDir: string;
> 327	  framePattern: string;   // e.g. 'f_%05d.png'
> 328	  frames: number;
> 329	  fps: number;
> 330	  width: number;
> 331	  height: number;
> 332	}
> 333	
> 334	/**
> 335	 * Render a composition's TEXT/GRAPHIC layer to a TRANSPARENT PNG sequence (RGBA, no background) for compositing
> 336	 * OVER real footage (video-repurpose FR-VR-011/012). Same deterministic index-driven loop as renderComposition,
> 337	 * but page.screenshot({ omitBackground: true }) → alpha preserved, and NO MP4 encode (yuv420p would drop alpha).
> 338	 * The template MUST have a transparent html/body background (e.g. 'viral-caption-overlay-9x16').
> 339	 * Injects fps + durationSec into props so time-based templates map frame index → clip seconds.
> 340	 * Returns the frame dir + %05d pattern; the CALLER overlays with FFmpeg and cleans the dir up.
> 341	 */
> 342	export async function renderAlphaFrames(spec: RenderSpec, outDir?: string): Promise<AlphaFramesResult> {
> 343	  const template = spec.template && VALID_TEMPLATES.has(spec.template) ? spec.template : 'viral-caption-overlay-9x16';
> 344	  const fps = Math.max(1, Math.min(60, spec.fps ?? 30));
> 345	  const durationS = Math.max(1, Math.min(60, spec.duration_s ?? 6));
> 346	  const width = spec.width ?? 1080;
> 347	  const height = spec.height ?? 1920;
> 348	  const totalFrames = Math.round(durationS * fps);
> 349	
> 350	  const templatePath = resolve(__dirname, 'templates', `${template}.html`);
> 351	  if (!existsSync(templatePath)) throw new Error(`template_not_found: ${template}`);
> 352	
> 353	  const frameDir = outDir ?? mkdtempSync(join(tmpdir(), 'hf-alpha-'));
> 354	  const browser = await chromium.launch({
> 355	    headless: true,
> 356	    // --allow-file-access-from-files: let the file:// template load its self-hosted @font-face (fonts/*.ttf).
> 357	    args: ['--no-sandbox', '--disable-dev-shm-usage', '--force-color-profile=srgb', '--disable-lcd-text', '--allow-file-access-from-files'],
> 358	  });
> 359	  try {
> 360	    const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
> 361	    await page.goto(`file://${templatePath}`, { waitUntil: 'load' });
> 362	    await page.evaluate(
> 363	      (props) => (window as any).applyProps(props),
> 364	      { ...spec.props, fps, durationSec: durationS } as Record<string, unknown>,
> 365	    );
> 366	
> 367	    // Wait for the self-hosted @font-face to finish loading → no fallback-font early frames (deterministic).
> 368	    await page.evaluate(() => (document as { fonts?: { ready?: Promise<unknown> } }).fonts?.ready).catch(() => {});
> 369	
> 370	    for (let i = 0; i < totalFrames; i++) {
> 371	      await page.evaluate(([idx, total]) => (window as any).applyFrame(idx, total), [i, totalFrames] as [number, number]);
> 372	      await page.screenshot({
> 373	        path: join(frameDir, `f_${String(i).padStart(5, '0')}.png`),
> 374	        clip: { x: 0, y: 0, width, height },
> 375	        omitBackground: true,           // ← RGBA, transparent bg preserved (the overlay layer)
> 376	        animations: 'disabled',
> 377	      });
> 378	    }
> 379	    await browser.close();
> 380	
> 381	    const first = join(frameDir, 'f_00000.png');
> 382	    if (!existsSync(first) || statSync(first).size < 1024) throw new Error(`alpha_frames_too_small: ${first}`);
> 383	
> 384	    return { frameDir, framePattern: 'f_%05d.png', frames: totalFrames, fps, width, height };
> 385	  } finally {
> 386	    await browser.close().catch(() => {});
> 387	  }
> 388	}
> 389	
> 390	/**
> 391	 * Render a Studio-authored project — FR-VS-050 (SDD §VS-UI-C): NATIVE engine on @hyperframes/core (Apache-2.0)
> 392	 * by default; the legacy CLI wrap (FR-VS-047 §B.3) remains available as emergency rollback via
> 393	 * STUDIO_RENDER_ENGINE=cli. Throws on any failure (worker → finalize_video_render(failed, refund)).
> 394	 *
> 395	 * Security: `project_dir` MUST resolve strictly under STUDIO_PROJECTS_ROOT (no traversal / arbitrary path exec).
> 396	 * The guard runs HERE, engine-independent, before any FS/bundle/spawn work.
> 397	 */
> 398	export async function renderStudioProject(spec: StudioProjectSpec, outPath: string): Promise<RenderResult> {
> 399	  // Path-safety: dir must be the root or strictly inside it (blocks ../ traversal + absolute escapes).
> 400	  const dir = resolve(spec.project_dir ?? '');
> 401	  const root = resolve(STUDIO_PROJECTS_ROOT);
> 402	  if (dir !== root && !dir.startsWith(root + '/')) throw new Error(`project_dir_outside_root: ${dir}`);
> 403	  if (!existsSync(join(dir, 'index.html'))) throw new Error(`studio_project_not_found: ${join(dir, 'index.html')}`);
> 404	
> 405	  const engine = process.env.STUDIO_RENDER_ENGINE ?? 'native';
> 406	  return engine === 'cli'
> 407	    ? renderStudioProjectViaCli(dir, spec, outPath)
> 408	    : renderStudioProjectNative(dir, spec, outPath);
> 409	}
> 410	
> 411	/**
> 412	 * FR-VS-050 — native studio-project render. Algorithm (mapped empirically from the reference CLI,
> 413	 * Workflow wf_bbc8402d-096; SDD §VS-UI-C C.3):
> 414	 *   bundleToSingleHtml(dir) [runtime inline] → temp bundle INSIDE dir (file:// keeps relative refs working)
> 415	 *   → init-script window.__HF_EXPORT_RENDER_SEEK_CONFIG={fps} (runtime reads at init; fps is renderer-owned)
> 416	 *   → goto + wait (__renderReady && __player.getDuration()>0) + fonts
> 417	 *   → per frame: __player.renderSeek(i/fps) (synchronous deterministic seek, quantized floor(t*fps+1e-9)/fps
> 418	 *     runtime-side) → PNG screenshot → shared bitexact FFmpeg encode (NFR-VS-016).
> 419	 * Declared limits (§C.3): no virtual-time shim (adapter-driven compositions only — GSAP/css/waapi/anime/lottie/
> 420	 * three); embedded <video> not pre-extracted; external pinned CDN refs need network.
> 421	 */
> 422	async function renderStudioProjectNative(dir: string, spec: StudioProjectSpec, outPath: string): Promise<RenderResult> {
> 423	  const t0 = Date.now();
> 424	  const fps = Math.max(1, Math.min(60, spec.fps ?? 30));
> 425	  const resolution = spec.resolution && VALID_RESOLUTIONS.has(spec.resolution) ? spec.resolution : 'portrait';
> 426	  const { width, height } = RESOLUTION_DIMENSIONS[resolution];
> 427	
> 428	  // Apache-2.0 import-only usage (© HeyGen — LICENSE ships in node_modules/@hyperframes/core/LICENSE).
> 429	  const { bundleToSingleHtml } = await import('@hyperframes/core/compiler');
> 430	  const html: string = await bundleToSingleHtml(dir);
> 431	
> 432	  // Serve via file:// from INSIDE the project dir so relative asset refs keep resolving.
> 433	  const bundlePath = join(dir, `.hf-native-bundle-${process.pid}-${Date.now().toString(36)}.html`);
> 434	  writeFileSync(bundlePath, html, 'utf8');
> 435	
> 436	  const frameDir = mkdtempSync(join(tmpdir(), 'hf-native-frames-'));
> 437	  const browser = await chromium.launch({
> 438	    headless: true,
> 439	    // Same determinism flags as the template path (single-tenant Usuário Zero, OTD-VA-011).
> 440	    args: ['--no-sandbox', '--disable-dev-shm-usage', '--force-color-profile=srgb', '--disable-lcd-text'],
> 441	  });
> 442	  try {
> 443	    const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
> 444	    // fps is renderer-owned; the embedded runtime reads this at init (fallback 30). Must precede goto.
> 445	    await page.addInitScript((v) => { (window as any).__HF_EXPORT_RENDER_SEEK_CONFIG = { fps: v, fpsSource: 'mcorch-native-render' }; }, fps);
> 446	    await page.goto(`file://${bundlePath}`, { waitUntil: 'load', timeout: 60_000 });
> 447	
> 448	    // Readiness (mirrors the reference pollHfReady): timelines bound + deterministic adapters ready + duration real.
> 449	    await page.waitForFunction(
> 450	      () => (window as any).__renderReady === true
> 451	        && (window as any).__player
> 452	        && typeof (window as any).__player.renderSeek === 'function'
> 453	        && (window as any).__player.getDuration() > 0,
> 454	      undefined,
> 455	      { timeout: 45_000 },
> 456	    ).catch(() => { throw new Error('studio_runtime_not_ready: __renderReady/__player.getDuration()>0 not reached in 45s'); });
> 457	    await page.evaluate(() => (document as any).fonts?.ready);
> 458	
> 459	    const duration: number = await page.evaluate(() => (window as any).__player.getDuration());
> 460	    if (!(duration > 0)) throw new Error('studio_composition_duration_zero'); // would produce a black video
> 461	    const totalFrames = Math.ceil(duration * fps);
> 462	
> 463	    for (let i = 0; i < totalFrames; i++) {
> 464	      // Synchronous deterministic seek: pauses timelines, seeks GSAP totalTime, fans out to adapters.
> 465	      await page.evaluate((t) => (window as any).__player.renderSeek(t), i / fps);
> 466	      await page.screenshot({
> 467	        path: join(frameDir, `f_${String(i).padStart(5, '0')}.png`),
> 468	        clip: { x: 0, y: 0, width, height },
> 469	        animations: 'allow', // css adapter seeks CSS animations; 'disabled' would force them to final state
> 470	      });
> 471	    }
> 472	    await browser.close();
> 473	
> 474	    await encodePngFramesBitexact(frameDir, fps, outPath);
> 475	
> 476	    if (!existsSync(outPath)) throw new Error('studio_render_produced_no_file');
> 477	    const bytes = statSync(outPath).size;
> 478	    if (bytes < 100 * 1024) throw new Error(`studio_render_too_small: ${bytes} bytes (< 100KB, Lei 1 gate)`);
> 479	
> 480	    const probe = await ffprobeVideo(outPath);
> 481	    return { outPath, bytes, width: probe.width, height: probe.height, frames: probe.frames, fps: probe.fps, durationMs: Date.now() - t0 };
> 482	  } finally {
> 483	    await browser.close().catch(() => {});
> 484	    rmSync(frameDir, { recursive: true, force: true });
> 485	    try { unlinkSync(bundlePath); } catch { /* already gone */ }
> 486	  }
> 487	}
> 488	
> 489	/**
> 490	 * Legacy FR-VS-047 CLI wrap — emergency rollback only (STUDIO_RENDER_ENGINE=cli). The npm `hyperframes` artifact
> 491	 * ships no license grant (OTD-VS-020) — delete this path after the first editor-initiated native render passes.
> 492	 * ARM64 trap: the hyperframes-bundled Chrome does not run on ARM64 → point it at Playwright's chromium.
> 493	 */
> 494	async function renderStudioProjectViaCli(dir: string, spec: StudioProjectSpec, outPath: string): Promise<RenderResult> {
> 495	  const t0 = Date.now();
> 496	  const fps = Math.max(1, Math.min(60, spec.fps ?? 30));
> 497	  const resolution = spec.resolution && VALID_RESOLUTIONS.has(spec.resolution) ? spec.resolution : 'portrait';
> 498	  if (!existsSync(HF_CLI)) throw new Error(`hyperframes_cli_not_found: ${HF_CLI}`);
> 499	
> 500	  const browserPath = chromium.executablePath();
> 501	
> 502	  await new Promise<void>((res, rej) => {
> 503	    const p = spawn(HF_NODE, [
> 504	      HF_CLI, 'render', dir,
> 505	      '--resolution', resolution, '--fps', String(fps),
> 506	      '-o', outPath, '--quiet',
> 507	    ], {
> 508	      stdio: ['ignore', 'ignore', 'pipe'],
> 509	      env: { ...process.env, HYPERFRAMES_BROWSER_PATH: browserPath, HOME: process.env.HOME ?? '/home/ubuntu' },
> 510	    });
> 511	    let err = '';
> 512	    p.stderr.on('data', (d) => { err += d.toString(); });
> 513	    p.on('error', rej);
> 514	    p.on('close', (code) => (code === 0 ? res() : rej(new Error(`hyperframes_render_exit_${code}: ${err.slice(-800)}`))));
> 515	  });
> 516	
> 517	  if (!existsSync(outPath)) throw new Error('studio_render_produced_no_file');
> 518	  const bytes = statSync(outPath).size;
> 519	  if (bytes < 100 * 1024) throw new Error(`studio_render_too_small: ${bytes} bytes (< 100KB, Lei 1 gate)`);
> 520	
> 521	  const probe = await ffprobeVideo(outPath);
> 522	  return { outPath, bytes, width: probe.width, height: probe.height, frames: probe.frames, fps: probe.fps, durationMs: Date.now() - t0 };
> 523	}
> 524	
> 525	// ── CLI (material proof harness) ──────────────────────────────────────────────────────────
> 526	if (import.meta.main) {
> 527	  const argv = process.argv.slice(2);
> 528	  const get = (k: string, d?: string) => {
> 529	    const i = argv.indexOf(`--${k}`);
> 530	    return i >= 0 && argv[i + 1] ? argv[i + 1] : d;
> 531	  };
> 532	  const out = get('out', '/tmp/hyperframes-test.mp4')!;
> 533	
> 534	  // Free image-to-video: --kenburns img.png [--kbdur 6] [--zoom in|out] (deterministic pan/zoom, US$0)
> 535	  const kbArg = get('kenburns');
> 536	  // Free "frames → video" mode: --images a.png,b.png,c.png [--sec 2.5] (Sovereign vision — HyperFrames joins pre-made frames)
> 537	  const imagesArg = get('images');
> 538	  const runner = kbArg
> 539	    ? encodeKenBurns(
> 540	        {
> 541	          image: kbArg,
> 542	          duration_s: Number(get('kbdur', '6')),
> 543	          zoom: (get('zoom', 'in') as 'in' | 'out'),
> 544	          fps: Number(get('fps', '30')),
> 545	        },
> 546	        out,
> 547	      )
> 548	    : imagesArg
> 549	    ? encodeImageSequence(
> 550	        {
> 551	          images: imagesArg.split(',').map((s) => s.trim()).filter(Boolean),
> 552	          seconds_per_image: Number(get('sec', '2.5')),
> 553	          fps: Number(get('fps', '30')),
> 554	        },
> 555	        out,
> 556	      )
> 557	    : renderComposition(
> 558	        {
> 559	          template: get('template', 'viral-short-9x16'),
> 560	          duration_s: Number(get('duration', '4')),
> 561	          fps: Number(get('fps', '30')),
> 562	          props: {
> 563	            hook: get('hook', 'Sua casa limpa sozinha'),
> 564	            caption: get('caption', 'O robô aspirador que faz tudo enquanto você vive a vida.'),
> 565	            cta: get('cta', 'Ver no Mercado Livre'),
> 566	            brand: get('brand', 'MCORCH'),
> 567	            product_image_url: get('image', ''),
> 568	          },
> 569	        },
> 570	        out,
> 571	      );
> 572	  runner
> 573	    .then((r) => {
> 574	      console.log(JSON.stringify(r, null, 2));
> 575	      console.log(`✅ rendered ${r.frames} frames → ${out} (${(r.bytes / 1024).toFixed(0)} KB, ${r.durationMs}ms)`);
> 576	    })
> 577	    .catch((e) => {
> 578	      console.error(`❌ render failed: ${e instanceof Error ? e.message : e}`);
> 579	      process.exit(1);
> 580	    });
> 581	}
> 582	
> ```

## 🤖 Claude *(21:53:26)*


## 🤖 Claude *(21:53:26)*

Now the final sink — the HTML template.

## 🤖 Claude *(21:53:28)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/hyperframes/templates/viral-caption-overlay-9x16.html"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	<!DOCTYPE html>
> 2	<!--
> 3	  viral-caption-overlay-9x16 — MCORCH Viral Quality overlay layer (video-repurpose FR-VR-012).
> 4	  TRANSPARENT background: rendered by render-core `renderAlphaFrames` (omitBackground:true) → RGBA PNG seq,
> 5	  composited OVER real reframed footage by segment-core (FFmpeg overlay). NO CTA button, NO dev HUD/frame-counter.
> 6	  Big kinetic word-by-word "text beats" (punctual captions, not a traditional bottom bar), legible sound-off
> 7	  over arbitrary footage (heavy weight + dark stroke/scrim). Deterministic: index-driven, no wallclock/random/net.
> 8	  Contract: applyProps({ beats:[{t_start,t_end,phrase,emphasis}], fps, durationSec, brand? }); applyFrame(i,total).
> 9	  emphasis ∈ {hook(gold), punch(cyan), normal(white)}. All text via textContent → XSS-safe.
> 10	-->
> 11	<html>
> 12	<head><meta charset="utf-8"><style>
> 13	  /* Premium/memorable typography (OFL, self-hosted, offline → deterministic). Fixes Vision "genérica" critique.
> 14	     The worker renders via file:// so the relative url() resolves next to this template. */
> 15	  @font-face{ font-family:'Montserrat'; src:url('fonts/Montserrat-variable.ttf') format('truetype');
> 16	    font-weight:100 900; font-style:normal; font-display:block; }
> 17	  html,body{ margin:0; padding:0; width:1080px; height:1920px; background:transparent; overflow:hidden; }
> 18	  /* Lower-third safe zone: clears top faces + bottom platform chrome. */
> 19	  #stage{ position:absolute; left:0; right:0; top:56%; height:34%;
> 20	    display:flex; align-items:center; justify-content:center; }
> 21	  /* Soft dark scrim ONLY behind the text block → legibility over bright footage (stays local; rest is transparent). */
> 22	  #scrim{ position:absolute; left:50%; top:50%; transform:translate(-50%,-50%);
> 23	    width:88%; height:78%; border-radius:48px;
> 24	    background:radial-gradient(ellipse at center, rgba(5,6,10,0.62) 0%, rgba(5,6,10,0.30) 55%, rgba(5,6,10,0) 78%);
> 25	    filter:blur(6px); opacity:0; }
> 26	  #beat{ position:relative; width:86%; text-align:center;
> 27	    font-family:'Montserrat','Liberation Sans',system-ui,sans-serif;
> 28	    font-weight:900; text-transform:uppercase; font-size:96px; line-height:1.02; letter-spacing:-2px;
> 29	    color:#FFFFFF;
> 30	    -webkit-text-stroke:3.2px rgba(5,6,10,0.9);
> 31	    text-shadow:0 4px 0 rgba(5,6,10,0.55), 0 0 26px rgba(5,6,10,0.75), 0 8px 40px rgba(5,6,10,0.55); }
> 32	  #beat .w{ display:inline-block; margin:0 0.16em 0.08em 0; will-change:transform,opacity;
> 33	    opacity:0; transform:translateY(22px) scale(0.62); }
> 34	  /* Emphasis accents (whole phrase). */
> 35	  #beat.hook{ color:#F5C542; -webkit-text-stroke-color:rgba(40,26,0,0.9);
> 36	    text-shadow:0 4px 0 rgba(30,18,0,0.6), 0 0 34px rgba(245,197,66,0.45), 0 8px 44px rgba(5,6,10,0.55); }
> 37	  #beat.punch{ color:#22D3EE; -webkit-text-stroke-color:rgba(0,26,32,0.9);
> 38	    text-shadow:0 4px 0 rgba(0,20,26,0.6), 0 0 34px rgba(34,211,238,0.5), 0 8px 44px rgba(5,6,10,0.55); }
> 39	  /* Thin animated accent underline (MIV cyan) that draws under the active phrase. */
> 40	  #accent{ position:absolute; left:50%; bottom:-2%; transform:translateX(-50%);
> 41	    height:8px; width:0; border-radius:6px; background:linear-gradient(90deg,#22D3EE,#F5C542);
> 42	    box-shadow:0 0 18px rgba(34,211,238,0.6); opacity:0; }
> 43	</style></head>
> 44	<body>
> 45	  <div id="stage">
> 46	    <div id="scrim"></div>
> 47	    <div id="beat"></div>
> 48	    <div id="accent"></div>
> 49	  </div>
> 50	<script>
> 51	function clamp(t){ return t<0?0:t>1?1:t; }
> 52	function easeOut(t){ t=clamp(t); return 1-Math.pow(1-t,3); }
> 53	
> 54	var BEATS=[], FPS=30, DUR=6, CUR=-1;
> 55	
> 56	// ── Props (textContent ONLY → XSS-safe) ──────────────────────────────────
> 57	window.applyProps=function(p){
> 58	  p=p||{};
> 59	  FPS=Math.max(1,Math.min(60, Number(p.fps)||30));
> 60	  DUR=Math.max(0.1, Number(p.durationSec)||6);
> 61	  BEATS=Array.isArray(p.beats)?p.beats.map(function(b){
> 62	    return { t0:Number(b.t_start)||0, t1:Number(b.t_end)||0,
> 63	             phrase:String(b.phrase||''), emphasis:String(b.emphasis||'normal') };
> 64	  }).filter(function(b){ return b.t1>b.t0 && b.phrase.length; }) : [];
> 65	  CUR=-1;
> 66	  buildBeat(-1);
> 67	};
> 68	
> 69	// Rebuild the word spans for the active beat (only when it changes → stable spans across frames).
> 70	function buildBeat(idx){
> 71	  var beatEl=document.getElementById('beat');
> 72	  beatEl.textContent=''; beatEl.className='';
> 73	  if(idx<0 || idx>=BEATS.length){ CUR=idx; return; }
> 74	  var b=BEATS[idx];
> 75	  beatEl.className=(b.emphasis==='hook'||b.emphasis==='punch')?b.emphasis:'';
> 76	  var words=b.phrase.split(/\s+/).filter(function(w){return w.length;});
> 77	  for(var i=0;i<words.length;i++){
> 78	    var s=document.createElement('span'); s.className='w'; s.textContent=words[i];
> 79	    beatEl.appendChild(s);
> 80	  }
> 81	  CUR=idx;
> 82	}
> 83	
> 84	function activeBeat(t){
> 85	  for(var i=0;i<BEATS.length;i++){ if(t>=BEATS[i].t0 && t<BEATS[i].t1) return i; }
> 86	  return -1;
> 87	}
> 88	
> 89	// ── Deterministic per-frame render (t = i/FPS). ──────────────────────────
> 90	window.applyFrame=function(i,total){
> 91	  var t=i/FPS;
> 92	  var idx=activeBeat(t);
> 93	  if(idx!==CUR) buildBeat(idx);
> 94	
> 95	  var beatEl=document.getElementById('beat');
> 96	  var scrim=document.getElementById('scrim');
> 97	  var accent=document.getElementById('accent');
> 98	
> 99	  if(idx<0){ scrim.style.opacity='0'; accent.style.opacity='0'; accent.style.width='0'; return; }
> 100	
> 101	  var b=BEATS[idx];
> 102	  var localP=clamp((t-b.t0)/(b.t1-b.t0));
> 103	  // beat envelope: quick fade-in 0..0.10, hold, fade-out 0.86..1.0
> 104	  var fin=easeOut(localP/0.10);
> 105	  var fout=localP>0.86 ? 1-clamp((localP-0.86)/0.14) : 1;
> 106	  var env=Math.min(fin,fout);
> 107	
> 108	  scrim.style.opacity=(0.92*env).toFixed(3);
> 109	
> 110	  var spans=beatEl.getElementsByClassName('w');
> 111	  var W=spans.length||1;
> 112	  for(var k=0;k<spans.length;k++){
> 113	    var wStart=(k/W)*0.42;                 // stagger the words across first 42% of the beat
> 114	    var wt=easeOut((localP-wStart)/0.16);
> 115	    var op=wt*env;
> 116	    spans[k].style.opacity=op.toFixed(3);
> 117	    spans[k].style.transform='translateY('+((1-wt)*22).toFixed(2)+'px) scale('+(0.62+0.38*wt).toFixed(3)+')';
> 118	  }
> 119	
> 120	  // accent underline draws in as words land, retracts on fade-out
> 121	  var aw=easeOut((localP-0.12)/0.5);
> 122	  accent.style.opacity=(env).toFixed(3);
> 123	  accent.style.width=(aw*62*env).toFixed(1)+'%';
> 124	};
> 125	
> 126	// standalone-open guard (render-core calls applyProps/applyFrame explicitly)
> 127	window.applyProps({ beats:[{t_start:0,t_end:3,phrase:'O SALTO NÃO É A NOTÍCIA',emphasis:'hook'}], fps:30, durationSec:3 });
> 128	window.applyFrame(0,2);
> 129	</script>
> 130	</body>
> 131	</html>
> 132	
> ```

## 🤖 Claude *(21:54:08)*


## 🤖 Claude *(21:54:24)*

I've traced the complete flow end to end. Here is my verified assessment.

## NO FINDINGS

No ≥8-confidence vulnerability in the new `text_beats`/`caption_mode` surface. The four load-bearing properties all hold:

**1. Bounded + validated input** (`video-repurpose-run/index.ts:33-61`)
- `sanitizeBeats`: `raw.slice(0, MAX_BEATS)` caps at 12 beats/clip; `phrase.slice(0, 120)` caps phrase length; timing is numeric-checked (`Number.isFinite(ts/te)`, `ts<0`, `te<=ts`, `te > clipDur+0.05` all rejected → beat dropped, never fabricated); `emphasis` is allowlisted via `EMPHASES.has()` → falls back to `"normal"`; `caption_mode` allowlisted via `CAPTION_MODES.has()`; clips capped at `MAX_CLIPS=50`. The template re-derives defensively (`String(b.phrase||'')`, `.filter(b.t1>b.t0 && b.phrase.length)` at `viral-caption-overlay-9x16.html:61-64`).

**2. Master resolved owner-scoped** (`index.ts:117-133`)
- `.eq("id", sourceAssetId).eq("user_id", user.id)` (user from JWT `getUser()`) is the tenant gate; `bucket`/`key` come from the DB row, not the client. Key prefix pinned `key.startsWith(\`${user.id}/\`)` + `!key.includes("..")`; bucket allowlisted; `bucket==='local'` requires an `admin` role. The worker re-validates at read time against `row.user_id` (`video-repurpose-bridge.ts:80-88`) with a `realpathSync` containment check under `INBOX_BASE`. `charged_mco:0` (free FFmpeg rail) → no billing path to bypass.

**3. `phrase` reaches the HTML template only via `textContent` — XSS-safe** 
- Path: composition jsonb → `comp.clips` → `segmentVideo` → `renderClip` → `renderAlphaFrames({ props:{ beats } })` → `page.evaluate((props)=>window.applyProps(props), props)`. Playwright passes `props` as a **structured-cloned argument**, not string-interpolated into page source, so no injection at the evaluate boundary. In the template, `buildBeat` does `s.textContent = words[i]` (`html:78`) — never `innerHTML`. Additionally the sink is a headless-Chromium PNG-frame render (file://, no live victim browser, no network egress), so there is no real XSS sink even hypothetically.

**4. `phrase` never touches an FFmpeg arg, shell command, or file path** (`segment-core.ts:86-97`)
- In the `beats` branch, the FFmpeg argv (`-ss`, `-t`, `-i` sourcePath, PNG pattern `f_%05d.png`, `-filter_complex` reframe+overlay) contains **no** clip/phrase-derived value — `phrase` flows only into the PNG frames via `renderAlphaFrames`. `spawn('ffmpeg', args)` runs with **no shell** (no `shell:true`). `alphaDir` is `mkdtempSync`, `outPath`/`sourcePath` are server-generated. The legacy `drawtext` path writes caption to a server-named file (`cap_${index}.txt`) and references it via `textfile='${capPath}'` — caption **content** stays in the file, never in the filter string or a path.

No command injection, no path traversal (the `local` inbox path is realpath-contained + admin-gated), no cross-tenant access (all output keys/`register_creative_asset` are `row.user_id`-bound), no billing bypass (free rail). Files reviewed: `supabase/functions/video-repurpose-run/index.ts`, `scripts/video-repurpose-bridge.ts`, `scripts/video-repurpose/segment-core.ts`, `scripts/hyperframes/render-core.ts`, `scripts/hyperframes/templates/viral-caption-overlay-9x16.html`.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-13 - agent-a75516096a8be0e6c]]
> * **Próxima Sessão**: [[2026-07-13 - agent-aa022bf46b6f1905f]]
%% --- TIMELINE END --- %%

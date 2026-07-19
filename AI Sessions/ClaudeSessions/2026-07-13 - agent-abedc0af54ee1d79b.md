# Session agent-abedc0af54ee1d79b
**Date:** 2026-07-13 | **Session ID:** `agent-abedc0af54ee1d79b`

---

## 👤 User *(20:22:20)*

You are a senior security engineer doing a FOCUSED security review of newly-added code in the repo at /home/gcrUX/htdocs/constellation-orchestra. Only these NEW/MODIFIED files are in scope (ignore everything else):

1. supabase/functions/detect-viral-moments/index.ts  (NEW — the main surface: a JWT-guarded Supabase Deno edge function)
2. scripts/hyperframes/render-core.ts  (MODIFIED — added `renderAlphaFrames` + a template to an allowlist Set + a `beats` field)
3. scripts/hyperframes/templates/viral-caption-overlay-9x16.html  (NEW — a Playwright-rendered HTML template)

Read those files. Then read 1-2 sibling edge functions for the established secure pattern: supabase/functions/lead-score/index.ts and supabase/functions/_shared/billing.ts (refundMco), _shared/llm-fallback.ts, _shared/sentinel.ts.

Look ONLY for HIGH-CONFIDENCE (≥80%) security vulnerabilities NEWLY introduced by these files:
- Authn/authz bypass, privilege escalation, cross-tenant data access (does the edge fn correctly owner-scope every resource by auth.uid()? does it ever trust a client-supplied user_id?)
- SQL/NoSQL/command/template injection; path traversal (render-core loads templates — is the template path attacker-controllable, or allowlisted?)
- XSS in the HTML template (is on-screen text set via textContent, or via innerHTML/insertAdjacentHTML/eval?)
- Secrets exposure (are per-user API keys or service keys logged or returned to the client?)
- mcoCoins billing bypass or mint (does deduct/refund have a charge-without-value or double-refund hole?)
- Untrusted LLM output used unsafely (the fn parses LLM JSON and builds a cut-spec — can the LLM output cause injection, or is it validated against real SRT cue indices?)

EXCLUSIONS (do NOT report): DoS/resource-exhaustion, rate-limiting, secrets-on-disk, regex-injection/regex-DoS, SSRF that only controls a path, lack-of-hardening, prompt-injection-into-LLM-system-prompt, log spoofing, theoretical race conditions, findings in markdown/docs files, client-side-only checks.

For EACH candidate vulnerability, assign a confidence 1-10 and ONLY keep those ≥8 with a concrete exploit path (file:line, attack steps). If there are none, say "NO FINDINGS" explicitly and briefly note the 3-4 security properties you verified as correct (owner-scoping, textContent XSS-safety, allowlisted template path, refund-on-fail).

Output a tight markdown report: either the ≥8-confidence findings (file, line, severity, category, exploit scenario, fix) or "NO FINDINGS" + the verified properties. Be precise and do not pad.

## 🤖 Claude *(20:22:26)*


## 🤖 Claude *(20:22:27)*

I'll start by reading the files in scope and the sibling reference files for the established secure pattern.

## 🤖 Claude *(20:22:27)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/detect-viral-moments/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// detect-viral-moments — video-repurpose FR-VR-010 (BoK SSOT: docs/bok/video-repurpose/10-frd-sdd-viral-quality.md §3.5).
> 2	// JWT-guarded · resolves the master creative_asset OWNER-SCOPED · reads its inline SRT · scores the best
> 3	// viral windows (Hormozi: hook/retain/reward + standalone) via the per-user AI key (API Tenancy Model,
> 4	// FAIL-CLOSED 402 — no system-env fallback in a user-facing fn) · debits mcoCoins atomically w/ refund-on-fail.
> 5	//
> 6	// Lei 1 anti-fabrication (FM-VR-Q1): the LLM only SELECTS cue indices; text_beats are BUILT from the real SRT
> 7	// cues (verbatim phrase + real timing). It never invents on-screen text. Does NOT enqueue a render — returns
> 8	// the ranked cut-spec for the client / video-repurpose-run.
> 9	import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
> 10	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 11	import { fetchLLMWithFallback, logLlmUsage } from "../_shared/llm-fallback.ts";
> 12	import { refundMco } from "../_shared/billing.ts";
> 13	import { inspectPrompt, logSentinelBlock, verdictResponse } from "../_shared/sentinel.ts";
> 14	
> 15	const corsHeaders = {
> 16	  "Access-Control-Allow-Origin": "*",
> 17	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 18	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> 19	};
> 20	
> 21	const DETECT_COST = 3;            // 4×-floor calibratable (OTD-VR-010); one analytical LLM pass over the transcript.
> 22	const MIN_CLIP_S = 6;
> 23	const MAX_CLIP_S = 90;
> 24	const MAX_CUES_SENT = 500;        // bound tokens for very long masters.
> 25	
> 26	interface Cue { i: number; start: number; end: number; text: string }
> 27	interface TextBeat { t_start: number; t_end: number; phrase: string; emphasis: "hook" | "punch" | "normal" }
> 28	interface ClipSpec { in_sec: number; out_sec: number; score: number; reason: string; hook_phrase: string; text_beats: TextBeat[] }
> 29	
> 30	// "HH:MM:SS,mmm" | "HH:MM:SS.mmm" → seconds
> 31	function tc(s: string): number {
> 32	  const m = s.trim().match(/(\d{1,2}):(\d{2}):(\d{2})[,.](\d{1,3})/);
> 33	  if (!m) return NaN;
> 34	  return (+m[1]) * 3600 + (+m[2]) * 60 + (+m[3]) + (+m[4]) / 1000;
> 35	}
> 36	
> 37	function parseSrt(raw: string): Cue[] {
> 38	  const cues: Cue[] = [];
> 39	  const blocks = raw.replace(/\r/g, "").split(/\n\s*\n/);
> 40	  for (const b of blocks) {
> 41	    const lines = b.split("\n").filter((l) => l.length);
> 42	    const tl = lines.find((l) => l.includes("-->"));
> 43	    if (!tl) continue;
> 44	    const [a, z] = tl.split("-->");
> 45	    const start = tc(a), end = tc(z);
> 46	    if (!Number.isFinite(start) || !Number.isFinite(end) || end <= start) continue;
> 47	    const text = lines.filter((l) => l !== tl && !/^\d+$/.test(l.trim())).join(" ").trim();
> 48	    if (!text) continue;
> 49	    cues.push({ i: cues.length, start, end, text });
> 50	  }
> 51	  return cues;
> 52	}
> 53	
> 54	serve(async (req) => {
> 55	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 56	  const json = (body: unknown, status = 200) =>
> 57	    new Response(JSON.stringify(body), { status, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 58	
> 59	  const url = Deno.env.get("SUPABASE_URL")!;
> 60	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 61	  const admin = createClient(url, serviceKey);
> 62	
> 63	  let charged = false;
> 64	  let chargedUser = "";
> 65	
> 66	  try {
> 67	    const authHeader = req.headers.get("Authorization");
> 68	    if (!authHeader) return json({ error: "Missing authorization" }, 401);
> 69	
> 70	    const userClient = createClient(url, (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!, {
> 71	      global: { headers: { Authorization: authHeader } },
> 72	    });
> 73	    const { data: { user }, error: authError } = await userClient.auth.getUser();
> 74	    if (authError || !user) return json({ error: "Unauthorized" }, 401);
> 75	
> 76	    const body = await req.json().catch(() => ({}));
> 77	    const masterId = body?.master_asset_id;
> 78	    const topN = Math.max(1, Math.min(8, Number(body?.top_n) || 3));
> 79	    if (!masterId || typeof masterId !== "string") return json({ error: "master_asset_id é obrigatório" }, 422);
> 80	
> 81	    // Owner-scoped master resolution (404 also covers another tenant's asset — tenant-safe).
> 82	    const { data: master } = await admin
> 83	      .from("creative_assets")
> 84	      .select("id, user_id, kind, metadata")
> 85	      .eq("id", masterId)
> 86	      .eq("user_id", user.id)
> 87	      .maybeSingle();
> 88	    if (!master) return json({ error: "Master não encontrado" }, 404);
> 89	
> 90	    // Resolve the inline SRT (ingest-external-asset stores metadata.srt as {pt,en} or a raw string).
> 91	    const meta = (master.metadata ?? {}) as Record<string, unknown>;
> 92	    const srtField = meta.srt as unknown;
> 93	    const rawSrt = typeof srtField === "string"
> 94	      ? srtField
> 95	      : (srtField && typeof srtField === "object"
> 96	        ? String((srtField as Record<string, unknown>).pt ?? (srtField as Record<string, unknown>).en ?? "")
> 97	        : String((meta.srt_pt ?? meta.srt_en ?? "")));
> 98	    if (!rawSrt || rawSrt.length < 20) return json({ error: "no_transcript", detail: "Master sem SRT — o detector precisa da legenda." }, 422);
> 99	
> 100	    const cues = parseSrt(rawSrt);
> 101	    if (cues.length < 2) return json({ error: "no_transcript", detail: "SRT não parseável em cues." }, 422);
> 102	    const sent = cues.slice(0, MAX_CUES_SENT);
> 103	
> 104	    // Cyber-Sentinel: the transcript reaches the LLM verbatim — inspect a bounded slice BEFORE the debit
> 105	    // (never bill a blocked request). It's the tenant's own content, but defense-in-depth against smuggled injection.
> 106	    const sentinelVerdict = inspectPrompt(sent.map((c) => c.text).join(" ").slice(0, 4000), user.id, { rateLimit: false });
> 107	    if (!sentinelVerdict.allow) {
> 108	      await logSentinelBlock(admin, "detect-viral-moments", sentinelVerdict, user.id);
> 109	      return verdictResponse(sentinelVerdict, corsHeaders);
> 110	    }
> 111	
> 112	    // per-user AI key (API Tenancy Model) — FAIL-CLOSED (no Deno.env provider fallback in a user-facing fn).
> 113	    const { data: userKeys } = await admin.from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 114	    const openRouterKey = userKeys?.openrouter_api_key as string | undefined;
> 115	    const groqKey = userKeys?.groq_api_key as string | undefined;
> 116	    const geminiKey = userKeys?.google_api_key as string | undefined;
> 117	    const aiKey = openRouterKey || groqKey;
> 118	    if (!aiKey) {
> 119	      return json({ error: "ai_not_configured", action: "Configure sua chave de IA em /dashboard/settings" }, 402);
> 120	    }
> 121	
> 122	    // mcoCoins gatekeeper: pre-check, then atomic deduction (never client-side).
> 123	    const { data: bal } = await admin.from("profiles").select("mco_balance").eq("id", user.id).maybeSingle();
> 124	    if ((bal?.mco_balance ?? 0) < DETECT_COST) return json({ error: "Saldo insuficiente de mcoCoins" }, 402);
> 125	    const { error: deductErr } = await admin.rpc("deduct_mco_coins", { p_user_id: user.id, p_amount: DETECT_COST });
> 126	    if (deductErr) return json({ error: "Saldo insuficiente de mcoCoins" }, 402);
> 127	    charged = true; chargedUser = user.id;
> 128	
> 129	    const usingGroq = !openRouterKey && !!groqKey;
> 130	    const endpoint = usingGroq
> 131	      ? "https://api.groq.com/openai/v1/chat/completions"
> 132	      : "https://openrouter.ai/api/v1/chat/completions";
> 133	    const model = usingGroq ? "llama-3.3-70b-versatile" : "meta-llama/llama-3.3-70b-instruct";
> 134	
> 135	    const sys =
> 136	      "Você é um editor viral especialista (estilo Alex Hormozi). Recebe a transcrição legendada (cues numeradas " +
> 137	      "com tempo em segundos). Selecione os TOP " + topN + " momentos que viralizam como Shorts verticais " +
> 138	      "INDEPENDENTES. Critérios: gancho forte nos 2s, tensão/curiosidade, frase citável, compreensível SEM " +
> 139	      "contexto externo, payoff. Para cada clipe forneça in_sec/out_sec DENTRO dos tempos das cues (ideal 12-45s), " +
> 140	      "score 0..1, reason curto em pt-BR, e beats = índices de cues a destacar como TEXTO GRANDE na tela (o gancho " +
> 141	      "+ 1 a 3 punchlines), cada beat com emphasis 'hook'|'punch'|'normal'. NUNCA invente texto — só selecione cues " +
> 142	      'existentes pelo índice. Responda APENAS JSON válido: {"clips":[{"in_sec":<n>,"out_sec":<n>,"score":<0..1>,' +
> 143	      '"reason":"<pt-BR>","beats":[{"cue":<índice>,"emphasis":"hook"}]}]}';
> 144	    const userMsg = "Transcrição (cues):\n" +
> 145	      sent.map((c) => `#${c.i} [${c.start.toFixed(1)}-${c.end.toFixed(1)}] ${c.text}`).join("\n") +
> 146	      `\n\nRetorne os ${topN} melhores clipes.`;
> 147	
> 148	    const aiResp = await fetchLLMWithFallback(
> 149	      endpoint,
> 150	      {
> 151	        method: "POST",
> 152	        headers: {
> 153	          Authorization: `Bearer ${aiKey}`,
> 154	          "Content-Type": "application/json",
> 155	          "HTTP-Referer": "https://mcorch.com",
> 156	          "X-Title": "GCRUX Constellation",
> 157	        },
> 158	        body: JSON.stringify({
> 159	          model,
> 160	          messages: [{ role: "system", content: sys }, { role: "user", content: userMsg }],
> 161	          stream: false,
> 162	          temperature: 0.3,
> 163	        }),
> 164	      },
> 165	      { openRouterKey, geminiKey, groqKey, functionName: "detect-viral-moments" },
> 166	    );
> 167	    if (!aiResp.ok) throw new Error(`llm_http_${aiResp.status}`);
> 168	    const data = await aiResp.json();
> 169	    await logLlmUsage("detect-viral-moments", model, data?.usage);
> 170	    const content: string = data?.choices?.[0]?.message?.content ?? "";
> 171	    const m = content.match(/\{[\s\S]*\}/);
> 172	    if (!m) throw new Error("llm_unparseable");
> 173	    const parsed = JSON.parse(m[0]) as { clips?: Array<Record<string, unknown>> };
> 174	
> 175	    // Build the cut-spec from REAL cues (Lei 1 — verbatim phrase + real timing; LLM only picked indices).
> 176	    const byIdx = new Map(cues.map((c) => [c.i, c]));
> 177	    const clips: ClipSpec[] = [];
> 178	    for (const raw of parsed.clips ?? []) {
> 179	      let inSec = Number(raw.in_sec);
> 180	      let outSec = Number(raw.out_sec);
> 181	      if (!Number.isFinite(inSec) || !Number.isFinite(outSec) || outSec <= inSec) continue;
> 182	      // clamp duration to a shorts-sane window
> 183	      if (outSec - inSec < MIN_CLIP_S || outSec - inSec > MAX_CLIP_S) {
> 184	        outSec = inSec + Math.max(MIN_CLIP_S, Math.min(MAX_CLIP_S, outSec - inSec));
> 185	      }
> 186	      const beatsRaw = Array.isArray(raw.beats) ? raw.beats as Array<Record<string, unknown>> : [];
> 187	      const text_beats: TextBeat[] = [];
> 188	      for (const br of beatsRaw) {
> 189	        const cue = byIdx.get(Number(br.cue));
> 190	        if (!cue) continue;                                  // index must exist → no fabrication
> 191	        const t_start = Math.max(0, cue.start - inSec);
> 192	        const t_end = Math.min(outSec - inSec, cue.end - inSec);
> 193	        if (t_end <= t_start) continue;                      // beat must fall inside the clip
> 194	        const emphasis = (["hook", "punch", "normal"].includes(String(br.emphasis)) ? br.emphasis : "normal") as TextBeat["emphasis"];
> 195	        text_beats.push({ t_start: +t_start.toFixed(2), t_end: +t_end.toFixed(2), phrase: cue.text.slice(0, 120), emphasis });
> 196	      }
> 197	      text_beats.sort((a, b) => a.t_start - b.t_start);
> 198	      const hook = text_beats.find((b) => b.emphasis === "hook") ?? text_beats[0];
> 199	      clips.push({
> 200	        in_sec: +inSec.toFixed(2),
> 201	        out_sec: +outSec.toFixed(2),
> 202	        score: Math.max(0, Math.min(1, Number(raw.score) || 0)),
> 203	        reason: String(raw.reason ?? "").slice(0, 280),
> 204	        hook_phrase: hook?.phrase ?? "",
> 205	        text_beats,
> 206	      });
> 207	    }
> 208	    clips.sort((a, b) => b.score - a.score);
> 209	    const top = clips.slice(0, topN);
> 210	    if (!top.length) throw new Error("no_viable_clips");
> 211	
> 212	    // Telemetry + best-effort mesh observation (padrão 8). Never blocks the response.
> 213	    admin.from("infra_health_logs").insert({ service: "detect-viral-moments", status: "healthy" }).then(() => {}, () => {});
> 214	    admin.from("mcorch_nodes").insert({
> 215	      user_id: user.id, node_type: "observation",
> 216	      name: `detect-viral-moments:${master.id}`,
> 217	      content: `detect-viral-moments selecionou ${top.length} janelas (top score ${top[0].score.toFixed(2)}) do master ${master.id}. FR-VR-010.`,
> 218	      metadata: { kind: "viral_moments", master_asset_id: master.id, clips: top.length, fr: "FR-VR-010" },
> 219	    }).then(() => {}, () => {});
> 220	
> 221	    const { data: newBal } = await admin.from("profiles").select("mco_balance").eq("id", user.id).maybeSingle();
> 222	    return json({ status: "ok", master_asset_id: master.id, clips: top, cue_count: cues.length, new_balance: newBal?.mco_balance ?? null });
> 223	  } catch (err) {
> 224	    if (charged) await refundMco(admin, chargedUser, DETECT_COST, "detect-viral-moments");
> 225	    admin.from("infra_health_logs").insert({ service: "detect-viral-moments", status: "unhealthy" }).then(() => {}, () => {});
> 226	    return json({ error: "Erro ao detectar momentos virais", detail: String((err as Error)?.message ?? err) }, 500);
> 227	  }
> 228	});
> 229	
> ```

## 🤖 Claude *(20:22:28)*


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
> 356	    args: ['--no-sandbox', '--disable-dev-shm-usage', '--force-color-profile=srgb', '--disable-lcd-text'],
> 357	  });
> 358	  try {
> 359	    const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
> 360	    await page.goto(`file://${templatePath}`, { waitUntil: 'load' });
> 361	    await page.evaluate(
> 362	      (props) => (window as any).applyProps(props),
> 363	      { ...spec.props, fps, durationSec: durationS } as Record<string, unknown>,
> 364	    );
> 365	
> 366	    for (let i = 0; i < totalFrames; i++) {
> 367	      await page.evaluate(([idx, total]) => (window as any).applyFrame(idx, total), [i, totalFrames] as [number, number]);
> 368	      await page.screenshot({
> 369	        path: join(frameDir, `f_${String(i).padStart(5, '0')}.png`),
> 370	        clip: { x: 0, y: 0, width, height },
> 371	        omitBackground: true,           // ← RGBA, transparent bg preserved (the overlay layer)
> 372	        animations: 'disabled',
> 373	      });
> 374	    }
> 375	    await browser.close();
> 376	
> 377	    const first = join(frameDir, 'f_00000.png');
> 378	    if (!existsSync(first) || statSync(first).size < 1024) throw new Error(`alpha_frames_too_small: ${first}`);
> 379	
> 380	    return { frameDir, framePattern: 'f_%05d.png', frames: totalFrames, fps, width, height };
> 381	  } finally {
> 382	    await browser.close().catch(() => {});
> 383	  }
> 384	}
> 385	
> 386	/**
> 387	 * Render a Studio-authored project — FR-VS-050 (SDD §VS-UI-C): NATIVE engine on @hyperframes/core (Apache-2.0)
> 388	 * by default; the legacy CLI wrap (FR-VS-047 §B.3) remains available as emergency rollback via
> 389	 * STUDIO_RENDER_ENGINE=cli. Throws on any failure (worker → finalize_video_render(failed, refund)).
> 390	 *
> 391	 * Security: `project_dir` MUST resolve strictly under STUDIO_PROJECTS_ROOT (no traversal / arbitrary path exec).
> 392	 * The guard runs HERE, engine-independent, before any FS/bundle/spawn work.
> 393	 */
> 394	export async function renderStudioProject(spec: StudioProjectSpec, outPath: string): Promise<RenderResult> {
> 395	  // Path-safety: dir must be the root or strictly inside it (blocks ../ traversal + absolute escapes).
> 396	  const dir = resolve(spec.project_dir ?? '');
> 397	  const root = resolve(STUDIO_PROJECTS_ROOT);
> 398	  if (dir !== root && !dir.startsWith(root + '/')) throw new Error(`project_dir_outside_root: ${dir}`);
> 399	  if (!existsSync(join(dir, 'index.html'))) throw new Error(`studio_project_not_found: ${join(dir, 'index.html')}`);
> 400	
> 401	  const engine = process.env.STUDIO_RENDER_ENGINE ?? 'native';
> 402	  return engine === 'cli'
> 403	    ? renderStudioProjectViaCli(dir, spec, outPath)
> 404	    : renderStudioProjectNative(dir, spec, outPath);
> 405	}
> 406	
> 407	/**
> 408	 * FR-VS-050 — native studio-project render. Algorithm (mapped empirically from the reference CLI,
> 409	 * Workflow wf_bbc8402d-096; SDD §VS-UI-C C.3):
> 410	 *   bundleToSingleHtml(dir) [runtime inline] → temp bundle INSIDE dir (file:// keeps relative refs working)
> 411	 *   → init-script window.__HF_EXPORT_RENDER_SEEK_CONFIG={fps} (runtime reads at init; fps is renderer-owned)
> 412	 *   → goto + wait (__renderReady && __player.getDuration()>0) + fonts
> 413	 *   → per frame: __player.renderSeek(i/fps) (synchronous deterministic seek, quantized floor(t*fps+1e-9)/fps
> 414	 *     runtime-side) → PNG screenshot → shared bitexact FFmpeg encode (NFR-VS-016).
> 415	 * Declared limits (§C.3): no virtual-time shim (adapter-driven compositions only — GSAP/css/waapi/anime/lottie/
> 416	 * three); embedded <video> not pre-extracted; external pinned CDN refs need network.
> 417	 */
> 418	async function renderStudioProjectNative(dir: string, spec: StudioProjectSpec, outPath: string): Promise<RenderResult> {
> 419	  const t0 = Date.now();
> 420	  const fps = Math.max(1, Math.min(60, spec.fps ?? 30));
> 421	  const resolution = spec.resolution && VALID_RESOLUTIONS.has(spec.resolution) ? spec.resolution : 'portrait';
> 422	  const { width, height } = RESOLUTION_DIMENSIONS[resolution];
> 423	
> 424	  // Apache-2.0 import-only usage (© HeyGen — LICENSE ships in node_modules/@hyperframes/core/LICENSE).
> 425	  const { bundleToSingleHtml } = await import('@hyperframes/core/compiler');
> 426	  const html: string = await bundleToSingleHtml(dir);
> 427	
> 428	  // Serve via file:// from INSIDE the project dir so relative asset refs keep resolving.
> 429	  const bundlePath = join(dir, `.hf-native-bundle-${process.pid}-${Date.now().toString(36)}.html`);
> 430	  writeFileSync(bundlePath, html, 'utf8');
> 431	
> 432	  const frameDir = mkdtempSync(join(tmpdir(), 'hf-native-frames-'));
> 433	  const browser = await chromium.launch({
> 434	    headless: true,
> 435	    // Same determinism flags as the template path (single-tenant Usuário Zero, OTD-VA-011).
> 436	    args: ['--no-sandbox', '--disable-dev-shm-usage', '--force-color-profile=srgb', '--disable-lcd-text'],
> 437	  });
> 438	  try {
> 439	    const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
> 440	    // fps is renderer-owned; the embedded runtime reads this at init (fallback 30). Must precede goto.
> 441	    await page.addInitScript((v) => { (window as any).__HF_EXPORT_RENDER_SEEK_CONFIG = { fps: v, fpsSource: 'mcorch-native-render' }; }, fps);
> 442	    await page.goto(`file://${bundlePath}`, { waitUntil: 'load', timeout: 60_000 });
> 443	
> 444	    // Readiness (mirrors the reference pollHfReady): timelines bound + deterministic adapters ready + duration real.
> 445	    await page.waitForFunction(
> 446	      () => (window as any).__renderReady === true
> 447	        && (window as any).__player
> 448	        && typeof (window as any).__player.renderSeek === 'function'
> 449	        && (window as any).__player.getDuration() > 0,
> 450	      undefined,
> 451	      { timeout: 45_000 },
> 452	    ).catch(() => { throw new Error('studio_runtime_not_ready: __renderReady/__player.getDuration()>0 not reached in 45s'); });
> 453	    await page.evaluate(() => (document as any).fonts?.ready);
> 454	
> 455	    const duration: number = await page.evaluate(() => (window as any).__player.getDuration());
> 456	    if (!(duration > 0)) throw new Error('studio_composition_duration_zero'); // would produce a black video
> 457	    const totalFrames = Math.ceil(duration * fps);
> 458	
> 459	    for (let i = 0; i < totalFrames; i++) {
> 460	      // Synchronous deterministic seek: pauses timelines, seeks GSAP totalTime, fans out to adapters.
> 461	      await page.evaluate((t) => (window as any).__player.renderSeek(t), i / fps);
> 462	      await page.screenshot({
> 463	        path: join(frameDir, `f_${String(i).padStart(5, '0')}.png`),
> 464	        clip: { x: 0, y: 0, width, height },
> 465	        animations: 'allow', // css adapter seeks CSS animations; 'disabled' would force them to final state
> 466	      });
> 467	    }
> 468	    await browser.close();
> 469	
> 470	    await encodePngFramesBitexact(frameDir, fps, outPath);
> 471	
> 472	    if (!existsSync(outPath)) throw new Error('studio_render_produced_no_file');
> 473	    const bytes = statSync(outPath).size;
> 474	    if (bytes < 100 * 1024) throw new Error(`studio_render_too_small: ${bytes} bytes (< 100KB, Lei 1 gate)`);
> 475	
> 476	    const probe = await ffprobeVideo(outPath);
> 477	    return { outPath, bytes, width: probe.width, height: probe.height, frames: probe.frames, fps: probe.fps, durationMs: Date.now() - t0 };
> 478	  } finally {
> 479	    await browser.close().catch(() => {});
> 480	    rmSync(frameDir, { recursive: true, force: true });
> 481	    try { unlinkSync(bundlePath); } catch { /* already gone */ }
> 482	  }
> 483	}
> 484	
> 485	/**
> 486	 * Legacy FR-VS-047 CLI wrap — emergency rollback only (STUDIO_RENDER_ENGINE=cli). The npm `hyperframes` artifact
> 487	 * ships no license grant (OTD-VS-020) — delete this path after the first editor-initiated native render passes.
> 488	 * ARM64 trap: the hyperframes-bundled Chrome does not run on ARM64 → point it at Playwright's chromium.
> 489	 */
> 490	async function renderStudioProjectViaCli(dir: string, spec: StudioProjectSpec, outPath: string): Promise<RenderResult> {
> 491	  const t0 = Date.now();
> 492	  const fps = Math.max(1, Math.min(60, spec.fps ?? 30));
> 493	  const resolution = spec.resolution && VALID_RESOLUTIONS.has(spec.resolution) ? spec.resolution : 'portrait';
> 494	  if (!existsSync(HF_CLI)) throw new Error(`hyperframes_cli_not_found: ${HF_CLI}`);
> 495	
> 496	  const browserPath = chromium.executablePath();
> 497	
> 498	  await new Promise<void>((res, rej) => {
> 499	    const p = spawn(HF_NODE, [
> 500	      HF_CLI, 'render', dir,
> 501	      '--resolution', resolution, '--fps', String(fps),
> 502	      '-o', outPath, '--quiet',
> 503	    ], {
> 504	      stdio: ['ignore', 'ignore', 'pipe'],
> 505	      env: { ...process.env, HYPERFRAMES_BROWSER_PATH: browserPath, HOME: process.env.HOME ?? '/home/ubuntu' },
> 506	    });
> 507	    let err = '';
> 508	    p.stderr.on('data', (d) => { err += d.toString(); });
> 509	    p.on('error', rej);
> 510	    p.on('close', (code) => (code === 0 ? res() : rej(new Error(`hyperframes_render_exit_${code}: ${err.slice(-800)}`))));
> 511	  });
> 512	
> 513	  if (!existsSync(outPath)) throw new Error('studio_render_produced_no_file');
> 514	  const bytes = statSync(outPath).size;
> 515	  if (bytes < 100 * 1024) throw new Error(`studio_render_too_small: ${bytes} bytes (< 100KB, Lei 1 gate)`);
> 516	
> 517	  const probe = await ffprobeVideo(outPath);
> 518	  return { outPath, bytes, width: probe.width, height: probe.height, frames: probe.frames, fps: probe.fps, durationMs: Date.now() - t0 };
> 519	}
> 520	
> 521	// ── CLI (material proof harness) ──────────────────────────────────────────────────────────
> 522	if (import.meta.main) {
> 523	  const argv = process.argv.slice(2);
> 524	  const get = (k: string, d?: string) => {
> 525	    const i = argv.indexOf(`--${k}`);
> 526	    return i >= 0 && argv[i + 1] ? argv[i + 1] : d;
> 527	  };
> 528	  const out = get('out', '/tmp/hyperframes-test.mp4')!;
> 529	
> 530	  // Free image-to-video: --kenburns img.png [--kbdur 6] [--zoom in|out] (deterministic pan/zoom, US$0)
> 531	  const kbArg = get('kenburns');
> 532	  // Free "frames → video" mode: --images a.png,b.png,c.png [--sec 2.5] (Sovereign vision — HyperFrames joins pre-made frames)
> 533	  const imagesArg = get('images');
> 534	  const runner = kbArg
> 535	    ? encodeKenBurns(
> 536	        {
> 537	          image: kbArg,
> 538	          duration_s: Number(get('kbdur', '6')),
> 539	          zoom: (get('zoom', 'in') as 'in' | 'out'),
> 540	          fps: Number(get('fps', '30')),
> 541	        },
> 542	        out,
> 543	      )
> 544	    : imagesArg
> 545	    ? encodeImageSequence(
> 546	        {
> 547	          images: imagesArg.split(',').map((s) => s.trim()).filter(Boolean),
> 548	          seconds_per_image: Number(get('sec', '2.5')),
> 549	          fps: Number(get('fps', '30')),
> 550	        },
> 551	        out,
> 552	      )
> 553	    : renderComposition(
> 554	        {
> 555	          template: get('template', 'viral-short-9x16'),
> 556	          duration_s: Number(get('duration', '4')),
> 557	          fps: Number(get('fps', '30')),
> 558	          props: {
> 559	            hook: get('hook', 'Sua casa limpa sozinha'),
> 560	            caption: get('caption', 'O robô aspirador que faz tudo enquanto você vive a vida.'),
> 561	            cta: get('cta', 'Ver no Mercado Livre'),
> 562	            brand: get('brand', 'MCORCH'),
> 563	            product_image_url: get('image', ''),
> 564	          },
> 565	        },
> 566	        out,
> 567	      );
> 568	  runner
> 569	    .then((r) => {
> 570	      console.log(JSON.stringify(r, null, 2));
> 571	      console.log(`✅ rendered ${r.frames} frames → ${out} (${(r.bytes / 1024).toFixed(0)} KB, ${r.durationMs}ms)`);
> 572	    })
> 573	    .catch((e) => {
> 574	      console.error(`❌ render failed: ${e instanceof Error ? e.message : e}`);
> 575	      process.exit(1);
> 576	    });
> 577	}
> 578	
> ```

## 🤖 Claude *(20:22:28)*


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
> 13	  html,body{ margin:0; padding:0; width:1080px; height:1920px; background:transparent; overflow:hidden; }
> 14	  /* Lower-third safe zone: clears top faces + bottom platform chrome. */
> 15	  #stage{ position:absolute; left:0; right:0; top:56%; height:34%;
> 16	    display:flex; align-items:center; justify-content:center; }
> 17	  /* Soft dark scrim ONLY behind the text block → legibility over bright footage (stays local; rest is transparent). */
> 18	  #scrim{ position:absolute; left:50%; top:50%; transform:translate(-50%,-50%);
> 19	    width:88%; height:78%; border-radius:48px;
> 20	    background:radial-gradient(ellipse at center, rgba(5,6,10,0.62) 0%, rgba(5,6,10,0.30) 55%, rgba(5,6,10,0) 78%);
> 21	    filter:blur(6px); opacity:0; }
> 22	  #beat{ position:relative; width:86%; text-align:center;
> 23	    font-family:'Liberation Sans','Arial Black','DejaVu Sans',system-ui,sans-serif;
> 24	    font-weight:900; text-transform:uppercase; font-size:98px; line-height:1.04; letter-spacing:-1.5px;
> 25	    color:#FFFFFF;
> 26	    -webkit-text-stroke:3.2px rgba(5,6,10,0.9);
> 27	    text-shadow:0 4px 0 rgba(5,6,10,0.55), 0 0 26px rgba(5,6,10,0.75), 0 8px 40px rgba(5,6,10,0.55); }
> 28	  #beat .w{ display:inline-block; margin:0 0.16em 0.08em 0; will-change:transform,opacity;
> 29	    opacity:0; transform:translateY(22px) scale(0.62); }
> 30	  /* Emphasis accents (whole phrase). */
> 31	  #beat.hook{ color:#F5C542; -webkit-text-stroke-color:rgba(40,26,0,0.9);
> 32	    text-shadow:0 4px 0 rgba(30,18,0,0.6), 0 0 34px rgba(245,197,66,0.45), 0 8px 44px rgba(5,6,10,0.55); }
> 33	  #beat.punch{ color:#22D3EE; -webkit-text-stroke-color:rgba(0,26,32,0.9);
> 34	    text-shadow:0 4px 0 rgba(0,20,26,0.6), 0 0 34px rgba(34,211,238,0.5), 0 8px 44px rgba(5,6,10,0.55); }
> 35	  /* Thin animated accent underline (MIV cyan) that draws under the active phrase. */
> 36	  #accent{ position:absolute; left:50%; bottom:-2%; transform:translateX(-50%);
> 37	    height:8px; width:0; border-radius:6px; background:linear-gradient(90deg,#22D3EE,#F5C542);
> 38	    box-shadow:0 0 18px rgba(34,211,238,0.6); opacity:0; }
> 39	</style></head>
> 40	<body>
> 41	  <div id="stage">
> 42	    <div id="scrim"></div>
> 43	    <div id="beat"></div>
> 44	    <div id="accent"></div>
> 45	  </div>
> 46	<script>
> 47	function clamp(t){ return t<0?0:t>1?1:t; }
> 48	function easeOut(t){ t=clamp(t); return 1-Math.pow(1-t,3); }
> 49	
> 50	var BEATS=[], FPS=30, DUR=6, CUR=-1;
> 51	
> 52	// ── Props (textContent ONLY → XSS-safe) ──────────────────────────────────
> 53	window.applyProps=function(p){
> 54	  p=p||{};
> 55	  FPS=Math.max(1,Math.min(60, Number(p.fps)||30));
> 56	  DUR=Math.max(0.1, Number(p.durationSec)||6);
> 57	  BEATS=Array.isArray(p.beats)?p.beats.map(function(b){
> 58	    return { t0:Number(b.t_start)||0, t1:Number(b.t_end)||0,
> 59	             phrase:String(b.phrase||''), emphasis:String(b.emphasis||'normal') };
> 60	  }).filter(function(b){ return b.t1>b.t0 && b.phrase.length; }) : [];
> 61	  CUR=-1;
> 62	  buildBeat(-1);
> 63	};
> 64	
> 65	// Rebuild the word spans for the active beat (only when it changes → stable spans across frames).
> 66	function buildBeat(idx){
> 67	  var beatEl=document.getElementById('beat');
> 68	  beatEl.textContent=''; beatEl.className='';
> 69	  if(idx<0 || idx>=BEATS.length){ CUR=idx; return; }
> 70	  var b=BEATS[idx];
> 71	  beatEl.className=(b.emphasis==='hook'||b.emphasis==='punch')?b.emphasis:'';
> 72	  var words=b.phrase.split(/\s+/).filter(function(w){return w.length;});
> 73	  for(var i=0;i<words.length;i++){
> 74	    var s=document.createElement('span'); s.className='w'; s.textContent=words[i];
> 75	    beatEl.appendChild(s);
> 76	  }
> 77	  CUR=idx;
> 78	}
> 79	
> 80	function activeBeat(t){
> 81	  for(var i=0;i<BEATS.length;i++){ if(t>=BEATS[i].t0 && t<BEATS[i].t1) return i; }
> 82	  return -1;
> 83	}
> 84	
> 85	// ── Deterministic per-frame render (t = i/FPS). ──────────────────────────
> 86	window.applyFrame=function(i,total){
> 87	  var t=i/FPS;
> 88	  var idx=activeBeat(t);
> 89	  if(idx!==CUR) buildBeat(idx);
> 90	
> 91	  var beatEl=document.getElementById('beat');
> 92	  var scrim=document.getElementById('scrim');
> 93	  var accent=document.getElementById('accent');
> 94	
> 95	  if(idx<0){ scrim.style.opacity='0'; accent.style.opacity='0'; accent.style.width='0'; return; }
> 96	
> 97	  var b=BEATS[idx];
> 98	  var localP=clamp((t-b.t0)/(b.t1-b.t0));
> 99	  // beat envelope: quick fade-in 0..0.10, hold, fade-out 0.86..1.0
> 100	  var fin=easeOut(localP/0.10);
> 101	  var fout=localP>0.86 ? 1-clamp((localP-0.86)/0.14) : 1;
> 102	  var env=Math.min(fin,fout);
> 103	
> 104	  scrim.style.opacity=(0.92*env).toFixed(3);
> 105	
> 106	  var spans=beatEl.getElementsByClassName('w');
> 107	  var W=spans.length||1;
> 108	  for(var k=0;k<spans.length;k++){
> 109	    var wStart=(k/W)*0.42;                 // stagger the words across first 42% of the beat
> 110	    var wt=easeOut((localP-wStart)/0.16);
> 111	    var op=wt*env;
> 112	    spans[k].style.opacity=op.toFixed(3);
> 113	    spans[k].style.transform='translateY('+((1-wt)*22).toFixed(2)+'px) scale('+(0.62+0.38*wt).toFixed(3)+')';
> 114	  }
> 115	
> 116	  // accent underline draws in as words land, retracts on fade-out
> 117	  var aw=easeOut((localP-0.12)/0.5);
> 118	  accent.style.opacity=(env).toFixed(3);
> 119	  accent.style.width=(aw*62*env).toFixed(1)+'%';
> 120	};
> 121	
> 122	// standalone-open guard (render-core calls applyProps/applyFrame explicitly)
> 123	window.applyProps({ beats:[{t_start:0,t_end:3,phrase:'O SALTO NÃO É A NOTÍCIA',emphasis:'hook'}], fps:30, durationSec:3 });
> 124	window.applyFrame(0,2);
> 125	</script>
> 126	</body>
> 127	</html>
> 128	
> ```

## 🤖 Claude *(20:22:34)*


## 🤖 Claude *(20:22:34)*

Now let me read the sibling reference files for the established secure pattern.

## 🤖 Claude *(20:22:35)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/lead-score/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// lead-score — marketing-hub FR-MH-003 (BoK SSOT: docs/bok/marketing-hub/04-frd.md §4.2 + 05-sdd.md §3).
> 2	// JWT-guarded · debits 1 mcoCoin atomically (deduct_mco_coins RPC) · scores a lead 0-100 via the
> 3	// per-user AI key (API Tenancy Model) with the shared LLM cascade fallback · FAIL-SOFT to a heuristic
> 4	// when the LLM is unavailable · persists leads.score + an immutable lead_event + an infra_health pulse.
> 5	import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
> 6	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 7	import { fetchLLMWithFallback, logLlmUsage } from "../_shared/llm-fallback.ts";
> 8	import { refundMco } from "../_shared/billing.ts";
> 9	import { inspectPrompt, logSentinelBlock, verdictResponse } from "../_shared/sentinel.ts";
> 10	
> 11	const corsHeaders = {
> 12	  "Access-Control-Allow-Origin": "*",
> 13	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 14	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> 15	};
> 16	
> 17	const SCORE_COST = 1;
> 18	
> 19	interface LeadRow {
> 20	  id: string;
> 21	  user_id: string;
> 22	  status: string;
> 23	  name: string | null;
> 24	  intent_signal: Record<string, unknown> | null;
> 25	}
> 26	
> 27	// Fail-soft heuristic when the LLM is unavailable: a rough 0-100 from non-PII lifecycle signals.
> 28	function heuristicScore(lead: LeadRow): number {
> 29	  if (lead.status === "converted") return 95;
> 30	  if (lead.status === "lost") return 15;
> 31	  let s = 40;
> 32	  if (lead.name) s += 10;
> 33	  const intentKeys = lead.intent_signal ? Object.keys(lead.intent_signal).length : 0;
> 34	  s += Math.min(intentKeys * 8, 32);
> 35	  if (lead.status === "nurturing") s += 10;
> 36	  return Math.max(0, Math.min(100, s));
> 37	}
> 38	
> 39	serve(async (req) => {
> 40	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 41	  const json = (body: unknown, status = 200) =>
> 42	    new Response(JSON.stringify(body), { status, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 43	
> 44	  const url = Deno.env.get("SUPABASE_URL")!;
> 45	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 46	  const admin = createClient(url, serviceKey);
> 47	
> 48	  // Charge-without-value guard: refund the 1-mco debit if any post-charge step throws (mirrors aeo-audit).
> 49	  let charged = false;
> 50	  let chargedUser = "";
> 51	
> 52	  try {
> 53	    const authHeader = req.headers.get("Authorization");
> 54	    if (!authHeader) return json({ error: "Missing authorization" }, 401);
> 55	
> 56	    const userClient = createClient(url, (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!, {
> 57	      global: { headers: { Authorization: authHeader } },
> 58	    });
> 59	    const { data: { user }, error: authError } = await userClient.auth.getUser();
> 60	    if (authError || !user) return json({ error: "Unauthorized" }, 401);
> 61	
> 62	    const { lead_id, context } = await req.json().catch(() => ({}));
> 63	    if (!lead_id || typeof lead_id !== "string") return json({ error: "lead_id é obrigatório" }, 422);
> 64	
> 65	    // existence + ownership (tenant-scoped); 404 also covers another tenant's lead.
> 66	    const { data: lead } = await admin
> 67	      .from("leads")
> 68	      .select("id, user_id, status, name, intent_signal")
> 69	      .eq("id", lead_id)
> 70	      .eq("user_id", user.id)
> 71	      .maybeSingle();
> 72	    if (!lead) return json({ error: "Lead não encontrado" }, 404);
> 73	
> 74	    // Cyber-Sentinel (OTD-SEC-006 · FM-01/FM-02): the lead's intent_signal (user-writable JSON) + the request
> 75	    // context are untrusted and reach the scoring LLM verbatim — inspect BEFORE the debit so a smuggled
> 76	    // prompt-injection is rejected without charging the tenant (never bill a blocked request).
> 77	    const untrusted = `${JSON.stringify((lead as { intent_signal?: unknown }).intent_signal ?? {})} ${String(context ?? "").slice(0, 240)}`;
> 78	    const sentinelVerdict = inspectPrompt(untrusted, user.id, { rateLimit: false });
> 79	    if (!sentinelVerdict.allow) {
> 80	      await logSentinelBlock(admin, "lead-score", sentinelVerdict, user.id);
> 81	      return verdictResponse(sentinelVerdict, corsHeaders);
> 82	    }
> 83	
> 84	    // mcoCoins gatekeeper: pre-check, then atomic server-side deduction (never client-side).
> 85	    const { data: bal } = await admin.from("profiles").select("mco_balance").eq("id", user.id).maybeSingle();
> 86	    if ((bal?.mco_balance ?? 0) < SCORE_COST) return json({ error: "Saldo insuficiente de mcoCoins" }, 402);
> 87	    const { error: deductErr } = await admin.rpc("deduct_mco_coins", { p_user_id: user.id, p_amount: SCORE_COST });
> 88	    if (deductErr) return json({ error: "Saldo insuficiente de mcoCoins" }, 402);
> 89	    charged = true; chargedUser = user.id;
> 90	
> 91	    // per-user AI key (API Tenancy Model) -> system fallback.
> 92	    const { data: userKeys } = await admin.from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 93	    const groqKey = userKeys?.groq_api_key || Deno.env.get("GROQ_API_KEY");
> 94	    const openRouterKey = userKeys?.openrouter_api_key;
> 95	    const geminiKey = userKeys?.google_api_key;
> 96	    const aiKey = groqKey || openRouterKey;
> 97	
> 98	    let score: number | null = null;
> 99	    let rationale = "";
> 100	
> 101	    if (aiKey) {
> 102	      const isGroq = !!groqKey;
> 103	      const endpoint = isGroq
> 104	        ? "https://api.groq.com/openai/v1/chat/completions"
> 105	        : "https://openrouter.ai/api/v1/chat/completions";
> 106	      const model = isGroq ? "llama-3.3-70b-versatile" : "meta-llama/llama-3.3-70b-instruct";
> 107	      const sys =
> 108	        'Você é um especialista em qualificação de leads. Avalie a intenção de compra do lead numa ' +
> 109	        'escala 0-100 (0=frio, 100=pronto para comprar). Responda APENAS com JSON válido: ' +
> 110	        '{"score": <inteiro 0-100>, "rationale": "<1 frase em pt-BR>"}';
> 111	      const userMsg =
> 112	        `Lead: status=${lead.status}, tem_nome=${!!lead.name}, sinais=${JSON.stringify(lead.intent_signal ?? {})}` +
> 113	        `${context ? `, contexto=${String(context).slice(0, 240)}` : ""}. Pontue.`;
> 114	      try {
> 115	        const aiResp = await fetchLLMWithFallback(
> 116	          endpoint,
> 117	          {
> 118	            method: "POST",
> 119	            headers: {
> 120	              Authorization: `Bearer ${aiKey}`,
> 121	              "Content-Type": "application/json",
> 122	              "HTTP-Referer": "https://mcorch.com",
> 123	              "X-Title": "GCRUX Constellation",
> 124	            },
> 125	            body: JSON.stringify({
> 126	              model,
> 127	              messages: [{ role: "system", content: sys }, { role: "user", content: userMsg }],
> 128	              stream: false,
> 129	              temperature: 0.2,
> 130	            }),
> 131	          },
> 132	          { openRouterKey, geminiKey, groqKey, functionName: "lead-score" },
> 133	        );
> 134	        if (aiResp.ok) {
> 135	          const data = await aiResp.json();
> 136	          await logLlmUsage("lead-score", model, data?.usage);
> 137	          const content: string = data?.choices?.[0]?.message?.content ?? "";
> 138	          const m = content.match(/\{[\s\S]*\}/);
> 139	          if (m) {
> 140	            const parsed = JSON.parse(m[0]);
> 141	            const n = Number(parsed.score);
> 142	            if (Number.isFinite(n)) {
> 143	              score = Math.max(0, Math.min(100, Math.round(n)));
> 144	              rationale = String(parsed.rationale ?? "").slice(0, 280);
> 145	            }
> 146	          }
> 147	        }
> 148	      } catch (_) {
> 149	        // fail-soft below
> 150	      }
> 151	    }
> 152	
> 153	    // FAIL-SOFT: heuristic when the LLM was unavailable, errored, or returned unparseable output.
> 154	    if (score === null) {
> 155	      score = heuristicScore(lead as LeadRow);
> 156	      rationale = rationale ||
> 157	        "Pontuação heurística (IA indisponível): baseada em status, identificação e sinais de intenção.";
> 158	    }
> 159	
> 160	    // persist: score + promote new->scored; immutable scored event; best-effort health pulse.
> 161	    await admin.from("leads")
> 162	      .update({ score, status: lead.status === "new" ? "scored" : lead.status })
> 163	      .eq("id", lead_id).eq("user_id", user.id);
> 164	    await admin.from("lead_events").insert({
> 165	      lead_id, user_id: user.id, channel: "system", event_type: "scored",
> 166	      payload: { score, rationale, source: aiKey ? "ai" : "heuristic" },
> 167	    });
> 168	    admin.from("infra_health_logs").insert({ service: "lead-score", status: "healthy" }).then(() => {}, () => {});
> 169	
> 170	    const { data: newBal } = await admin.from("profiles").select("mco_balance").eq("id", user.id).maybeSingle();
> 171	    return json({ status: "ok", lead_id, score, rationale, new_balance: newBal?.mco_balance ?? null });
> 172	  } catch (err) {
> 173	    // Any post-charge failure refunds the entry debit (charge-without-value guard).
> 174	    if (charged) await refundMco(admin, chargedUser, SCORE_COST, "lead-score");
> 175	    admin.from("infra_health_logs").insert({ service: "lead-score", status: "unhealthy" }).then(() => {}, () => {});
> 176	    return json({ error: "Erro interno ao pontuar lead", detail: String((err as Error)?.message ?? err) }, 500);
> 177	  }
> 178	});
> 179	
> ```

## 🤖 Claude *(20:22:36)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/billing.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// Shared mcoCoins billing helpers for edge functions. SSOT for the REFUND-ON-FAILURE contract:
> 2	// a function that DEBITS mcoCoins at entry MUST refund the charge if it then fails to deliver value
> 3	// (the "charge-without-value" bug — e.g. aeo-audit charges 5, then the persist fails → the tenant lost 5
> 4	// for nothing). Refund uses add_mco_coins — the service_role-only credit RPC, symmetric to deduct_mco_coins
> 5	// (guard p_amount > 0). Best-effort + logged; NEVER throws (a failed refund must not mask the original error).
> 6	// SOP: docs/processes/mcoin-cost-calibration.md (§Refund-on-failure).
> 7	
> 8	// Minimal structural shape of the admin (service-role) client — avoids a supabase-js type import so this stays
> 9	// pure and unit-testable without resolving esm.sh.
> 10	export interface BillingAdmin {
> 11	  rpc(fn: string, args: Record<string, unknown>): Promise<{ error: unknown }>;
> 12	  from(table: string): { insert(row: Record<string, unknown>): { then(onOk: () => void, onErr: () => void): void } };
> 13	}
> 14	
> 15	/**
> 16	 * Refund `amount` mcoCoins to `userId` after a charge-then-fail. Returns true if the credit landed.
> 17	 * No-op (returns false) for a non-positive amount. Never throws — on failure it logs an unhealthy pulse so a
> 18	 * stuck charge is observable, and returns false so the caller can surface it.
> 19	 */
> 20	export async function refundMco(
> 21	  admin: BillingAdmin,
> 22	  userId: string,
> 23	  amount: number,
> 24	  service: string,
> 25	): Promise<boolean> {
> 26	  if (!userId || !amount || amount <= 0) return false;
> 27	  try {
> 28	    const { error } = await admin.rpc("add_mco_coins", { p_user_id: userId, p_amount: amount });
> 29	    if (error) {
> 30	      admin.from("infra_health_logs").insert({ service, status: "unhealthy" }).then(() => {}, () => {});
> 31	      return false;
> 32	    }
> 33	    return true;
> 34	  } catch {
> 35	    admin.from("infra_health_logs").insert({ service, status: "unhealthy" }).then(() => {}, () => {});
> 36	    return false;
> 37	  }
> 38	}
> 39	
> ```

## 🤖 Claude *(20:22:36)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/llm-fallback.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// supabase/functions/_shared/llm-fallback.ts
> 2	// Shared helper for OTD-LLM-FALLBACK. Falls back gracefully when OpenRouter credits are exhausted.
> 3	
> 4	export interface FallbackOptions {
> 5	  openRouterKey?: string;
> 6	  geminiKey?: string;
> 7	  groqKey?: string;
> 8	  /** Optional caller name for granular fallback telemetry (service = `llm-fallback:<functionName>`). */
> 9	  functionName?: string;
> 10	}
> 11	
> 12	const HEAVY_MODEL_REGEX = /claude-3\.5|claude-4|gpt-4|llama-3\.1-405b/i;
> 13	
> 14	/**
> 15	 * Fire-and-forget telemetry to infra_health_logs when the cascade DEGRADES (a free tier rescued
> 16	 * the call) or FAILS (all providers exhausted). Self-sufficient inside Deno (reads SUPABASE_URL +
> 17	 * SB_SECRET_KEY straight from the function env and POSTs to PostgREST — no SDK import); a silent
> 18	 * no-op outside Deno (unit tests) and on ANY error — observability must NEVER break a generation.
> 19	 */
> 20	async function logFallbackHealth(status: "degraded" | "unhealthy", functionName?: string): Promise<void> {
> 21	  try {
> 22	    const denoEnv = (globalThis as { Deno?: { env: { get(k: string): string | undefined } } }).Deno?.env;
> 23	    if (!denoEnv) return;
> 24	    const url = denoEnv.get("SUPABASE_URL");
> 25	    const key = denoEnv.get("SB_SECRET_KEY") ?? denoEnv.get("SUPABASE_SERVICE_ROLE_KEY");
> 26	    if (!url || !key) return;
> 27	    await fetch(`${url}/rest/v1/infra_health_logs`, {
> 28	      method: "POST",
> 29	      headers: { apikey: key, Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
> 30	      body: JSON.stringify({ service: `llm-fallback:${functionName ?? "unknown"}`, status }),
> 31	    }).catch(() => {});
> 32	  } catch (_) {
> 33	    // swallow — telemetry is best-effort and must not affect the LLM cascade
> 34	  }
> 35	}
> 36	
> 37	/**
> 38	 * Observability (zero-USD audit 2026-06-30): capture the LLM `usage` (token counts) that OpenRouter/Gemini return
> 39	 * on NON-streaming completions and emit an `llm_usage` pulse to infra_health_logs. Turns the video-cycle cost from
> 40	 * ESTIMATED into MEASURED — the doctrine GO needs $0 PROVEN, not asserted. Aggregate-only (fn/model/tokens, NO
> 41	 * user_id: infra_health_logs is global-read → per-tenant attribution belongs in a scoped table). Best-effort:
> 42	 * no-op outside Deno, on missing usage, or on ANY error — observability must NEVER break a generation.
> 43	 */
> 44	export async function logLlmUsage(functionName: string, model: string, usage: unknown): Promise<void> {
> 45	  try {
> 46	    const u = (usage ?? {}) as { prompt_tokens?: number; completion_tokens?: number; total_tokens?: number };
> 47	    if (u.prompt_tokens == null && u.completion_tokens == null && u.total_tokens == null) return; // nothing measured
> 48	    const denoEnv = (globalThis as { Deno?: { env: { get(k: string): string | undefined } } }).Deno?.env;
> 49	    if (!denoEnv) return;
> 50	    const url = denoEnv.get("SUPABASE_URL");
> 51	    const key = denoEnv.get("SB_SECRET_KEY") ?? denoEnv.get("SUPABASE_SERVICE_ROLE_KEY");
> 52	    if (!url || !key) return;
> 53	    await fetch(`${url}/rest/v1/infra_health_logs`, {
> 54	      method: "POST",
> 55	      headers: { apikey: key, Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
> 56	      body: JSON.stringify({
> 57	        service: "llm-usage",
> 58	        status: "healthy",
> 59	        event: "llm_usage",
> 60	        metadata: {
> 61	          fn: functionName,
> 62	          model,
> 63	          prompt_tokens: u.prompt_tokens ?? null,
> 64	          completion_tokens: u.completion_tokens ?? null,
> 65	          total_tokens: u.total_tokens ?? null,
> 66	        },
> 67	      }),
> 68	    }).catch(() => {});
> 69	  } catch (_) {
> 70	    // swallow — observability must never break a generation
> 71	  }
> 72	}
> 73	
> 74	/**
> 75	 * Image-model observability (zero-USD audit): image APIs return NO token `usage` — cost is PER-IMAGE. Emit an
> 76	 * `image_usage` pulse (fn/model/image_count) so the video/campaign-cycle image cost becomes MEASURED, not
> 77	 * asserted (USD derived externally as model × per-image price). Aggregate-only (NO user_id — infra_health_logs
> 78	 * is global-read). Best-effort: no-op outside Deno, on a missing model, or on ANY error.
> 79	 */
> 80	export async function logImageUsage(functionName: string, model: string, count = 1): Promise<void> {
> 81	  try {
> 82	    if (!model) return;
> 83	    const denoEnv = (globalThis as { Deno?: { env: { get(k: string): string | undefined } } }).Deno?.env;
> 84	    if (!denoEnv) return;
> 85	    const url = denoEnv.get("SUPABASE_URL");
> 86	    const key = denoEnv.get("SB_SECRET_KEY") ?? denoEnv.get("SUPABASE_SERVICE_ROLE_KEY");
> 87	    if (!url || !key) return;
> 88	    await fetch(`${url}/rest/v1/infra_health_logs`, {
> 89	      method: "POST",
> 90	      headers: { apikey: key, Authorization: `Bearer ${key}`, "Content-Type": "application/json" },
> 91	      body: JSON.stringify({
> 92	        service: "image-usage",
> 93	        status: "healthy",
> 94	        event: "image_usage",
> 95	        metadata: { fn: functionName, model, image_count: count },
> 96	      }),
> 97	    }).catch(() => {});
> 98	  } catch (_) {
> 99	    // swallow — observability must never break a generation
> 100	  }
> 101	}
> 102	
> 103	/**
> 104	 * Executes a chat completion fetch request, falling back gracefully to free alternatives
> 105	 * if the primary provider fails due to credit exhaustion (402), rate-limits (429), or network errors.
> 106	 * 
> 107	 * Cascade order:
> 108	 * 1. Primary provider (OpenRouter / Groq)
> 109	 * 2. Gemini Free OpenAI-Compatible Endpoint:
> 110	 *    - Heavy models -> gemini-2.5-pro -> gemini-1.5-pro
> 111	 *    - Medium/Light models -> gemini-2.5-flash -> gemini-1.5-flash
> 112	 * 3. OpenRouter Free (gemma-2-9b-it:free / llama-3-8b-instruct:free)
> 113	 */
> 114	export async function fetchLLMWithFallback(
> 115	  originalEndpoint: string,
> 116	  requestInit: RequestInit,
> 117	  options: FallbackOptions
> 118	): Promise<Response> {
> 119	  const openRouterKey = options.openRouterKey;
> 120	  const geminiKey = options.geminiKey;
> 121	  const groqKey = options.groqKey;
> 122	
> 123	  let requestBodyObj: any = {};
> 124	  if (requestInit.body && typeof requestInit.body === "string") {
> 125	    try {
> 126	      requestBodyObj = JSON.parse(requestInit.body);
> 127	    } catch (_) {
> 128	      console.warn("[llm-fallback] Failed to parse request body as JSON");
> 129	    }
> 130	  }
> 131	
> 132	  const originalModel = requestBodyObj.model || "";
> 133	
> 134	  // Helper to execute fetch and handle potential network errors
> 135	  const safeFetch = async (url: string, init: RequestInit): Promise<Response> => {
> 136	    try {
> 137	      return await fetch(url, init);
> 138	    } catch (err) {
> 139	      console.warn(`[llm-fallback] Fetch error to ${url}:`, err);
> 140	      // Return a synthetic 500 response to trigger the next level of cascade
> 141	      return new Response(
> 142	        JSON.stringify({ error: "Network fetch failed", details: String(err) }),
> 143	        { status: 500, headers: { "Content-Type": "application/json" } }
> 144	      );
> 145	    }
> 146	  };
> 147	
> 148	  // --- Step 1: Attempt Primary Request ---
> 149	  console.log(`[llm-fallback] Attempting primary LLM request with model "${originalModel}"`);
> 150	  let response = await safeFetch(originalEndpoint, requestInit);
> 151	
> 152	  // If successful, return immediately
> 153	  if (response.ok) {
> 154	    return response;
> 155	  }
> 156	
> 157	  // Detect billing or rate limit errors
> 158	  const isCreditError = response.status === 402;
> 159	  const isRateLimitError = response.status === 429;
> 160	  const isServerError = response.status >= 500;
> 161	  
> 162	  const shouldFallback = isCreditError || isRateLimitError || isServerError;
> 163	
> 164	  if (!shouldFallback) {
> 165	    console.warn(`[llm-fallback] Primary request failed with status ${response.status} (no fallback triggered)`);
> 166	    return response;
> 167	  }
> 168	
> 169	  const errBodyText = await response.clone().text().catch(() => "unknown error body");
> 170	  console.warn(
> 171	    `[llm-fallback] Primary request failed (status=${response.status}). Initiating cascade. Details: ${errBodyText.slice(0, 200)}`
> 172	  );
> 173	
> 174	  // --- Step 2: Gemini Free Fallback (OpenAI-compatible) ---
> 175	  if (geminiKey) {
> 176	    const isHeavy = HEAVY_MODEL_REGEX.test(originalModel);
> 177	    const geminiCandidates = isHeavy
> 178	      ? ["gemini-2.5-pro", "gemini-1.5-pro"]
> 179	      : ["gemini-2.5-flash", "gemini-1.5-flash"];
> 180	
> 181	    console.log(`[llm-fallback] Attempting Gemini Free fallback. Candidates: ${geminiCandidates.join(", ")}`);
> 182	
> 183	    for (const model of geminiCandidates) {
> 184	      const geminiBody = {
> 185	        ...requestBodyObj,
> 186	        model,
> 187	      };
> 188	
> 189	      const geminiHeaders = new Headers(requestInit.headers || {});
> 190	      geminiHeaders.set("Authorization", `Bearer ${geminiKey}`);
> 191	      geminiHeaders.set("Content-Type", "application/json");
> 192	      // Remove OpenRouter-specific headers that might throw errors or pollute logs
> 193	      geminiHeaders.delete("HTTP-Referer");
> 194	      geminiHeaders.delete("X-Title");
> 195	
> 196	      const geminiEndpoint = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions";
> 197	      
> 198	      console.log(`[llm-fallback] Dispatching fallback request to Gemini Free using model "${model}"`);
> 199	      const geminiResp = await safeFetch(geminiEndpoint, {
> 200	        ...requestInit,
> 201	        headers: geminiHeaders,
> 202	        body: JSON.stringify(geminiBody),
> 203	      });
> 204	
> 205	      if (geminiResp.ok) {
> 206	        console.log(`[llm-fallback] Gemini Free fallback succeeded with model "${model}"`);
> 207	        await logFallbackHealth("degraded", options.functionName);
> 208	        return geminiResp;
> 209	      }
> 210	
> 211	      const geminiErrText = await geminiResp.text().catch(() => "unknown");
> 212	      console.warn(`[llm-fallback] Gemini model "${model}" failed (status=${geminiResp.status}): ${geminiErrText.slice(0, 200)}`);
> 213	    }
> 214	  } else {
> 215	    console.log("[llm-fallback] GEMINI_API_KEY unavailable - skipping Gemini Free fallback");
> 216	  }
> 217	
> 218	  // --- Step 3: OpenRouter Free Fallback ---
> 219	  const routerKey = openRouterKey || groqKey;
> 220	  if (routerKey) {
> 221	    const freeModels = ["google/gemma-2-9b-it:free", "meta-llama/llama-3-8b-instruct:free"];
> 222	    console.log(`[llm-fallback] Attempting OpenRouter Free fallback. Candidates: ${freeModels.join(", ")}`);
> 223	
> 224	    for (const model of freeModels) {
> 225	      const freeBody = {
> 226	        ...requestBodyObj,
> 227	        model,
> 228	      };
> 229	
> 230	      const freeHeaders = new Headers(requestInit.headers || {});
> 231	      freeHeaders.set("Authorization", `Bearer ${routerKey}`);
> 232	      freeHeaders.set("Content-Type", "application/json");
> 233	
> 234	      const freeEndpoint = "https://openrouter.ai/api/v1/chat/completions";
> 235	      
> 236	      console.log(`[llm-fallback] Dispatching fallback request to OpenRouter Free using model "${model}"`);
> 237	      const freeResp = await safeFetch(freeEndpoint, {
> 238	        ...requestInit,
> 239	        headers: freeHeaders,
> 240	        body: JSON.stringify(freeBody),
> 241	      });
> 242	
> 243	      if (freeResp.ok) {
> 244	        console.log(`[llm-fallback] OpenRouter Free fallback succeeded with model "${model}"`);
> 245	        await logFallbackHealth("degraded", options.functionName);
> 246	        return freeResp;
> 247	      }
> 248	
> 249	      const freeErrText = await freeResp.text().catch(() => "unknown");
> 250	      console.warn(`[llm-fallback] OpenRouter Free model "${model}" failed (status=${freeResp.status}): ${freeErrText.slice(0, 200)}`);
> 251	    }
> 252	  } else {
> 253	    console.log("[llm-fallback] OpenRouter API Key unavailable - skipping OpenRouter Free fallback");
> 254	  }
> 255	
> 256	  // If all fallbacks fail, return the original failure response
> 257	  console.error("[llm-fallback] All LLM providers in cascade failed.");
> 258	  await logFallbackHealth("unhealthy", options.functionName);
> 259	  return new Response(
> 260	    JSON.stringify({
> 261	      error: "LLM fallback exhaustion",
> 262	      message: "Both primary LLM and all fallback alternatives failed.",
> 263	    }),
> 264	    { status: 502, headers: { "Content-Type": "application/json" } }
> 265	  );
> 266	}
> 267	
> ```

## 🤖 Claude *(20:22:37)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/sentinel.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// _shared/sentinel.ts — MCORCH edge-native prompt verification pipeline (FR-SEC-002).
> 2	// SSOT: docs/bok/security/02-srs-secure-spec.md FR-SEC-002 + 03-sdd-hardening-architecture.md §3.2.
> 3	// Fail-closed layers executed BEFORE any LLM dispatch AND before any mcoCoins charge:
> 4	//   L1 structural guard (size / shape)
> 5	//   L2 lexical injection triage (instruction override, exfil, ANSI smuggling, base64 blobs, billing-bypass)
> 6	//   L3 per-identity token bucket (per-isolate; the hard economic cap is FR-SEC-003 deduct_mco_coins)
> 7	// The caller runs L4 = deduct_mco_coins AFTER an allow verdict. Sentinel NEVER bills.
> 8	
> 9	export interface SentinelVerdict {
> 10	  allow: boolean;
> 11	  status: number;
> 12	  code: string;
> 13	  detail?: string;
> 14	}
> 15	
> 16	const MAX_PROMPT_BYTES = 64_000;
> 17	
> 18	// Independent injection pattern families. A score >= 2 (two distinct families) blocks — one isolated
> 19	// match tolerates benign content that happens to contain a single trigger phrase.
> 20	const INJECTION_PATTERNS: RegExp[] = [
> 21	  // Chained qualifiers: catches "ignore previous instructions" AND "ignore all previous instructions".
> 22	  /ignore\s+(?:(?:all|any|the|every|previous|prior|above|earlier|preceding)\s+){1,3}(instructions?|rules?|prompts?|directions?|commands?|context|guidelines?)/i,
> 23	  /disregard\s+(the\s+)?(above|previous|prior|system)/i,
> 24	  /reveal\s+(your\s+)?(system\s+prompt|hidden\s+instructions|secrets?)/i,
> 25	  /you\s+are\s+now\s+(in\s+)?(developer|dan|jailbreak|god)\s*mode/i,
> 26	  /act\s+as\s+(if\s+you\s+were\s+)?(root|admin|system|the\s+operator)/i,
> 27	  /\bBEGIN\s+(SYSTEM|ADMIN|OVERRIDE)\b/,
> 28	  /<\s*\/?\s*(system|assistant|tool)\s*>/i,
> 29	  /\[[0-9;]*[A-Za-z]/, // ANSI CSI escape smuggled into a prompt
> 30	  /[A-Za-z0-9+/]{400,}={0,2}/, // anomalous base64 blob (payload smuggling)
> 31	  /\bdo\s+not\s+(charge|bill|debit|deduct)\b/i, // explicit billing-bypass coaching
> 32	  // ── pt-BR injection families (OTD-VA-018-SENTINEL-PTBR) ──────────────────────────────────────────────────────
> 33	  // The English families above miss injections in the language this product actually generates/ingests (pt-BR:
> 34	  // vm_trends, user topics, ML product copy). These MIRROR the English families with the SAME phrase-level
> 35	  // specificity, so the score>=2 threshold still tolerates a lone trigger in benign copy. Tuned to 0 false
> 36	  // positives over a real pt-BR marketing corpus incl. trope-traps ("esqueça tudo o que você sabe", "ignore os
> 37	  // sistemas tradicionais", "a partir de agora sua casa", "atua como o sistema nervoso") — those score <= 1.
> 38	  // f1: ignore/desconsidere/esqueça [as/todas/anteriores…] instruções/regras/comandos/diretrizes/prompt/contexto/o sistema
> 39	  /(ignore|ignora|ignorar|desconsidere|desconsiderar|despreze|esque[çc]a|esque[çc]er)\s+(?:(?:as?|os?|todas?|todos?|quaisquer|anteriores?|pr[ée]vias?|o|do|de)\s+){0,3}(instru[çc][õo]es|regras?|comandos?|dire(?:triz|trizes|[çc][õo]es)|prompts?|orienta[çc][õo]es|o\s+contexto|o\s+sistema)/i,
> 40	  // f2: desconsidere/ignore (o que foi dito) acima / anteriormente  (mirror "disregard the above/previous")
> 41	  /(desconsidere|desconsiderar|despreze|ignore|esque[çc]a)\s+(o\s+|a\s+|tudo\s+(o\s+)?que\s+(foi\s+)?dito\s+|o\s+que\s+(foi\s+)?dito\s+)?(acima|anteriormente|previamente)\b/i,
> 42	  // f3: revele/mostre/exiba/repita (seu) prompt do sistema / instruções ocultas|do sistema|secretas|iniciais.
> 43	  // NOT bare "segredos" — "revele os segredos de X" is a ubiquitous legit pt-BR marketing trope (false-positive).
> 44	  /(revele|revelar|mostre|mostrar|exiba|exibir|imprima|imprimir|repita|repetir)\s+(o\s+|a\s+|as\s+|os\s+|seu\s+|sua\s+)?(prompt\s+(do\s+sistema|inicial)|system\s+prompt|instru[çc][õo]es\s+(ocultas|secretas|do\s+sistema|anteriores|iniciais|de\s+configura[çc][ãa]o))/i,
> 45	  // f4: aja/age/atua/comporte-se/finja como root/admin/administrador/sistema/operador/superusuário.
> 46	  // NOT "desenvolvedor" — "atua como o desenvolvedor de X" is legit copy; the jailbreak "modo desenvolvedor" is f5.
> 47	  /(aja|age|atu[ae]|comporte-se|finja\s+(ser|que\s+[ée]))\s+como\s+(o\s+|um\s+|uma\s+|a\s+)?(root|admin|administrador|sistema|operador|super\s*usu[áa]rio)\b/i,
> 48	  // f5: modo desenvolvedor/deus/jailbreak/dan/irrestrito/sem filtro/sem restrições  (mirror "developer/god mode").
> 49	  // NOT bare "modo livre" — "modo livre" is a real product feature (drone/free-flight) (false-positive).
> 50	  /\bmodo\s+(desenvolvedor|deus|jailbreak|dan|irrestrito|sem\s+(filtro|restri[çc][õo]es))\b/i,
> 51	  // f6: INÍCIO/COMEÇO SISTEMA/ADMIN/OVERRIDE  |  "novas instruções do sistema:"  (mirror "BEGIN SYSTEM")
> 52	  /(\b(IN[IÍ]CIO|COME[ÇC]O)\s+(DE\s+)?(SISTEMA|ADMIN|OVERRIDE)\b|nova[s]?\s+instru[çc][õo]es\s+(do\s+sistema|a\s+seguir)\s*:?)/i,
> 53	  // f7: billing-bypass coaching in pt  (mirror "do not charge/bill/debit/deduct")
> 54	  /n[ãa]o\s+(cobre|cobrar|debite|debitar|deduza|deduzir|fa[çc]a\s+a\s+cobran[çc]a|retire|tire)\s+(o\s+usu[áa]rio|cr[ée]ditos?|mcocoins?|do\s+saldo|nada)/i,
> 55	];
> 56	
> 57	// ANSI/C0-C1 detection (FR-SEC-012). In a PROMPT we BLOCK on presence rather than sanitize-and-continue:
> 58	// a smuggled escape sequence is hostile intent, not noise. (\n, \t, \r are intentionally allowed.)
> 59	// deno-lint-ignore no-control-regex
> 60	const ANSI_OR_CONTROL_RE = /[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]/;
> 61	
> 62	export function lexicalScore(text: string): number {
> 63	  let score = 0;
> 64	  for (const re of INJECTION_PATTERNS) {
> 65	    if (re.test(text)) score += 1;
> 66	  }
> 67	  return score;
> 68	}
> 69	
> 70	// L3 — token bucket per identity per isolate. Resets on cold start by design: defense in depth against
> 71	// burst loops, NOT the billing limiter (that is L4 = deduct_mco_coins).
> 72	const BUCKETS = new Map<string, { tokens: number; refillAt: number }>();
> 73	const RATE = { capacity: 30, refillMs: 60_000 };
> 74	
> 75	export function takeToken(identity: string): boolean {
> 76	  const now = Date.now();
> 77	  const bucket = BUCKETS.get(identity) ?? { tokens: RATE.capacity, refillAt: now + RATE.refillMs };
> 78	  if (now >= bucket.refillAt) {
> 79	    bucket.tokens = RATE.capacity;
> 80	    bucket.refillAt = now + RATE.refillMs;
> 81	  }
> 82	  if (bucket.tokens <= 0) {
> 83	    BUCKETS.set(identity, bucket);
> 84	    return false;
> 85	  }
> 86	  bucket.tokens -= 1;
> 87	  BUCKETS.set(identity, bucket);
> 88	  return true;
> 89	}
> 90	
> 91	export interface InspectOptions {
> 92	  // L3 per-identity rate bucket. Default true. Set FALSE for fan-out TARGETS (orchestrate-content,
> 93	  // dispatched in parallel by campaign-run / intent-execute with one shared JWT) — there the burst is
> 94	  // legitimate and the economic gate (deduct_mco_coins) is the real limiter; per-isolate rate-limiting a
> 95	  // fan-out target would 429 already-authorized paid steps. Per-IP rate-limiting belongs at the edge
> 96	  // gateway (Arcjet, SDD §3.1), not inside the dispatch target.
> 97	  rateLimit?: boolean;
> 98	}
> 99	
> 100	export function inspectPrompt(raw: string, identity: string, opts: InspectOptions = {}): SentinelVerdict {
> 101	  const { rateLimit = true } = opts;
> 102	  // L1 — structural
> 103	  if (typeof raw !== "string" || raw.length === 0) {
> 104	    return { allow: false, status: 400, code: "empty_prompt" };
> 105	  }
> 106	  if (raw.length > MAX_PROMPT_BYTES) {
> 107	    return { allow: false, status: 413, code: "payload_too_large" };
> 108	  }
> 109	  // L3 — rate (cheap, before regex work) — skippable for fan-out targets
> 110	  if (rateLimit && !takeToken(identity)) {
> 111	    return { allow: false, status: 429, code: "rate_limited" };
> 112	  }
> 113	  // L2 — control-char smuggling: hostile by definition in a prompt
> 114	  if (ANSI_OR_CONTROL_RE.test(raw)) {
> 115	    return { allow: false, status: 403, code: "control_chars_in_prompt" };
> 116	  }
> 117	  // L2 — lexical injection score (2+ independent pattern families => block)
> 118	  const score = lexicalScore(raw);
> 119	  if (score >= 2) {
> 120	    return { allow: false, status: 403, code: "prompt_injection_suspected", detail: `score=${score}` };
> 121	  }
> 122	  return { allow: true, status: 200, code: "ok" };
> 123	}
> 124	
> 125	// Telemetry — best-effort, never throws (NFR-SEC-01 ∩ FR-SEC-013).
> 126	interface AdminLike {
> 127	  from(table: string): {
> 128	    insert(row: Record<string, unknown>): PromiseLike<{ error: unknown }>;
> 129	  };
> 130	}
> 131	
> 132	export async function logSentinelBlock(
> 133	  admin: AdminLike,
> 134	  fn: string,
> 135	  verdict: SentinelVerdict,
> 136	  userId: string | null,
> 137	): Promise<void> {
> 138	  const payload = { code: verdict.code, detail: verdict.detail ?? null };
> 139	  try {
> 140	    await admin.from("infra_health_logs").insert({
> 141	      service: "sentinel",
> 142	      status: "degraded",
> 143	      metadata: { fn, ...payload, user_id: userId },
> 144	    });
> 145	  } catch {
> 146	    // swallowing is intentional: telemetry must never break the request path
> 147	  }
> 148	  // FR-SEC-014 (part 1): mirror the block into the immutable security ledger (security_events) — queryable by
> 149	  // admins, distinct from the infra heartbeat. severity='warning': a blocked injection is CONTAINED, not a
> 150	  // critical freeze event (the freeze escalation is part 2). Best-effort; the table may predate this on old deploys.
> 151	  try {
> 152	    await admin.from("security_events").insert({
> 153	      user_id: userId,
> 154	      event_type: verdict.code,
> 155	      severity: "warning",
> 156	      source: fn,
> 157	      payload,
> 158	    });
> 159	  } catch {
> 160	    // best-effort — never break the request path
> 161	  }
> 162	}
> 163	
> 164	export function verdictResponse(v: SentinelVerdict, corsHeaders: Record<string, string>): Response {
> 165	  return new Response(
> 166	    JSON.stringify({ error: v.code, detail: v.detail ?? null, layer: "sentinel" }),
> 167	    { status: v.status, headers: { ...corsHeaders, "Content-Type": "application/json" } },
> 168	  );
> 169	}
> 170	
> ```

## 🤖 Claude *(20:24:03)*


## 🤖 Claude *(20:24:28)*

I've read all files in scope plus the reference patterns. Let me trace the security-critical paths carefully.

**Owner-scoping verification** — In `detect-viral-moments/index.ts`:
- Line 73: `user` comes only from `userClient.auth.getUser()` (verified JWT); the body (line 76-77) supplies only `master_asset_id` and `top_n` — never a `user_id`.
- Line 82-88: master resolved via the service-role `admin` client BUT with an explicit `.eq("user_id", user.id)` filter → tenant-safe (404 covers another tenant's asset).
- Line 113 (`decrypted_user_api_keys`), 123/221 (`profiles`), 125 (`deduct_mco_coins p_user_id`), 214 (`mcorch_nodes`), 224 (`refundMco chargedUser`) — every resource is scoped to `user.id` from the token. No client-supplied identity is ever trusted.

**Billing correctness** — Sentinel (106-110) and AI-key check (113-120) both run BEFORE the debit (never bill a blocked/misconfigured request). `charged` is set only after a successful atomic `deduct_mco_coins`; any post-charge throw hits the single catch (223-224) → exactly one `refundMco`. No mint (server-trusted `user.id`), no double-refund, no charge-without-value.

**LLM-output safety (Lei 1)** — Line 176 builds `byIdx` from the REAL parsed SRT cues. Per beat (188-196), `byIdx.get(Number(br.cue))` must resolve or the beat is skipped; the on-screen `phrase` is `cue.text.slice(0,120)` (verbatim SRT), never LLM free-text. `in_sec/out_sec` are `Number()`-coerced + finite-checked + clamped; `emphasis` is allowlist-validated. The only LLM free-text (`reason`) is returned as inert JSON data, used in no sink.

**Template path** — `renderAlphaFrames` (line 343) and `renderComposition` (267) gate `spec.template` through `VALID_TEMPLATES.has(...)`, falling back to a fixed safe name; `resolve(__dirname,'templates',`${template}.html`)` therefore can never be attacker-steered (`'../../x'` fails `.has()` → default). No traversal.

**XSS** — `viral-caption-overlay-9x16.html`: `applyProps` stores `String(b.phrase||'')`; `buildBeat` sets `beatEl.textContent=''` then per-word `s.textContent=words[i]`. `className` is only ever `'hook'|'punch'|''` (strict-equality gated). No `innerHTML`/`insertAdjacentHTML`/`eval`/`document.write`. XSS-safe.

**Secrets** — `aiKey` is used only as a Bearer header (153); `userKeys`/decrypted keys are never returned or logged; `logLlmUsage` is aggregate-only; error `detail` (226) carries only controlled strings (`llm_http_*`, `llm_unparseable`, `no_viable_clips`), no key material.

---

# Security Review — detect-viral-moments / render-core / viral-caption-overlay

## NO FINDINGS

No ≥8-confidence vulnerability was newly introduced by the three in-scope files. Each candidate category was checked against a concrete exploit path and closed:

| Category | Verdict | Why (file:line) |
|---|---|---|
| Cross-tenant / authz bypass / client-supplied user_id | Safe | `detect-viral-moments/index.ts:82-88` filters `.eq("user_id", user.id)` on the service-role query; every other resource is scoped to the JWT `user.id`; body carries no identity (`:76-79`). |
| Path traversal / template injection | Safe | `render-core.ts:343` + `:267` allowlist via `VALID_TEMPLATES.has()`; non-member input falls back to a fixed template before `resolve()`. |
| XSS in overlay template | Safe | `viral-caption-overlay-9x16.html:66-77` renders all text via `textContent`; `className` restricted to `hook`/`punch`/`""`; no `innerHTML`/`eval`. |
| Untrusted LLM → cut-spec injection / fabrication | Safe | `index.ts:176-196` — LLM supplies only cue indices; on-screen `phrase` is verbatim SRT (`cue.text`), timings `Number()`+finite+clamp validated, `emphasis` allowlisted. |
| mcoCoins mint / double-refund / charge-without-value | Safe | `index.ts:106-127,223-224` — checks precede debit; `deduct` uses server-trusted `user.id`; single refund-on-throw. |
| Secrets exposure | Safe | `index.ts:113-166,222,226` — per-user key only in Bearer header; never logged/returned; error detail is controlled strings. |

**Verified-correct security properties:** (1) every resource owner-scoped by `auth.uid()`/JWT `user.id`; (2) on-screen text is `textContent`-only (XSS-safe); (3) template path is allowlisted (no traversal); (4) refund-on-fail is atomic, single, and server-trusted (no mint/double-refund).

Note: the un-cleaned `frameDir` in `renderAlphaFrames` (caller-owned cleanup by design) and `product_image_url`/token-bounding concerns are resource-exhaustion/SSRF-path items explicitly out of scope.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-13 - agent-abd884395d76d9014]]
> * **Próxima Sessão**: [[2026-07-13 - agent-abf67c6215ae9e548]]
%% --- TIMELINE END --- %%

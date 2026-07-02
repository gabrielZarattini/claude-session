# Session agent-a53edeeded7f8a8e0
**Date:** 2026-07-02 | **Session ID:** `agent-a53edeeded7f8a8e0`

---

## 👤 User *(18:41:24)*

You are mapping the canvas-execute edge function contract in the MCORCH repo at /home/gcrUX/htdocs/constellation-orchestra.
Read IN FULL: supabase/functions/canvas-execute/index.ts. Also find and read the client-side caller used by Canvas Studio (grep src/ for "canvas-execute" — likely a hook like useCanvasExecution or inside CanvasEditorPage/useCanvasStore) and read the relevant file(s).
Extract with file:line refs:
1. Request payload shape (exact fields: node type, prompt, params, reference images, project id, execution id...).
2. Auth model (user JWT? service-role paths?), per-user BYOK credential resolution, which providers per node type.
3. Billing: which actions debit, how much (COIN_COSTS refs), atomic RPC used, refund path, the async video path (vm_canvas_executions, realtime callback).
4. Response shape (sync image vs async video), error codes (402/422/501...), and how the client polls/subscribes.
5. Which node types canvas-execute supports today (imageGeneration, videoGeneration, etc.) and exact type strings.
6. Whether there is an execution_id/idempotency mechanism.
Quote exact identifiers. Report gaps (e.g. node types in Spaces registry with NO backend support).

## 🤖 Claude *(18:41:28)*


## 🤖 Claude *(18:41:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/canvas-execute/index.ts && grep -rn \"canvas-execute\" /home/gcrUX/htdocs/constellation-orchestra/src/ | head -50",
  "description": "Count lines of canvas-execute and find client callers"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 1216 /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/canvas-execute/index.ts
> /home/gcrUX/htdocs/constellation-orchestra/src/pages/CanvasEditorPage.tsx:29:import { assertExecuteSuccess } from "@/lib/canvas-execute-result";
> /home/gcrUX/htdocs/constellation-orchestra/src/lib/canvas-execute-result.ts:2: * Shared helper to validate canvas-execute responses. The Edge Function
> /home/gcrUX/htdocs/constellation-orchestra/src/lib/canvas-execute-result.ts:35:    throw new Error("canvas-execute retornou resposta vazia");
> /home/gcrUX/htdocs/constellation-orchestra/src/lib/agent-task-result.ts:8: * Like canvas-execute, the capability path can return HTTP 200 with `status: "failed"` when the
> /home/gcrUX/htdocs/constellation-orchestra/src/lib/agent-task-result.ts:12: * Mirrors `canvas-execute-result.ts` so the cockpit has one consistent failure-handling idiom.
> /home/gcrUX/htdocs/constellation-orchestra/src/lib/billing.ts:14://   orchestrate run (3 texts + 1 image) ≈ $0.04 · Higgsfield DoP 5s video = $0.56 (canvas-execute, validated 4×).
> /home/gcrUX/htdocs/constellation-orchestra/src/test/canvas-video-async-smoke.test.ts:101:    console.log("🎥 [GATE 1] Dispatching video generation request to canvas-execute edge function...");
> /home/gcrUX/htdocs/constellation-orchestra/src/test/canvas-video-async-smoke.test.ts:117:    const funcResp = await fetch(`${supabaseUrl}/functions/v1/canvas-execute`, {
> /home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/RightPanel/inspectors/GenerateImageInspector.tsx:44:import { assertExecuteSuccess } from "@/lib/canvas-execute-result";
> /home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/RightPanel/StyleSettingsPanel.tsx:21: * Aplicado a todos os prompts no momento da execução (canvas-execute prepends
> /home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/RightPanel/inspectors/SceneComposeInspector.tsx:28:import { assertExecuteSuccess } from "@/lib/canvas-execute-result";
> /home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/RightPanel/inspectors/StyleTransferInspector.tsx:15:import { assertExecuteSuccess } from "@/lib/canvas-execute-result";
> /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCanvasStudio.ts:239:      const { data, error } = await supabase.functions.invoke("canvas-execute", { body: params });
> /home/gcrUX/htdocs/constellation-orchestra/src/types/canvas.ts:9: * OpenAI / Replicate / OpenRouter já suportados pelo `canvas-execute`.
> /home/gcrUX/htdocs/constellation-orchestra/src/types/canvas.ts:51: * the suffix; canvas-execute resolves these to the canonical tier key
> /home/gcrUX/htdocs/constellation-orchestra/src/types/canvas.ts:52: * `higgsfield/soul-<res>-<batch>` (see CREDIT_COSTS in canvas-execute).
> /home/gcrUX/htdocs/constellation-orchestra/src/types/canvas.ts:76:  /** Model name passed to canvas-execute (`body.model`). */
> /home/gcrUX/htdocs/constellation-orchestra/src/types/canvas.ts:463: * Runs against the net-new `generate-voice` Edge Function (NOT canvas-execute).
> /home/gcrUX/htdocs/constellation-orchestra/src/types/canvas.ts:491: * net-new `avatar-identity-train` Edge Function (gated OTD-AC-017) — NOT canvas-execute. The
> /home/gcrUX/htdocs/constellation-orchestra/src/types/canvas.ts:802: * `canvas-execute` Edge Function. Soul models split into provider/model
> /home/gcrUX/htdocs/constellation-orchestra/src/types/canvas.ts:882:      // CharacterReference doesn't trigger canvas-execute by itself —
> /home/gcrUX/htdocs/constellation-orchestra/src/types/canvas.ts:887:      // NOT canvas-execute — its inspector calls useAvatarVoice directly.
> /home/gcrUX/htdocs/constellation-orchestra/src/types/canvas.ts:891:      // (FR-AC-012, gated OTD-AC-017), NOT canvas-execute — inspector handles it directly.
> /home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/RightPanel/inspectors/ImageToVideoInspector.tsx:17:import { assertExecuteSuccess } from "@/lib/canvas-execute-result";
> /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCanvasPipeline.ts:7:import { assertExecuteSuccess } from "@/lib/canvas-execute-result";
> /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useSpaces.ts:3:// this layer NEVER touches deduct_mco_coins/canvas-execute (SOP gate G5).
> /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useParamRegistry.ts:26: * Verified server-side cost authority lives in `supabase/functions/canvas-execute`
> ```

## 🤖 Claude *(18:41:34)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/canvas-execute/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
> 2	import { createClient } from "https://esm.sh/@supabase/supabase-js@2.49.4";
> 3	import { fetchLLMWithFallback } from "../_shared/llm-fallback.ts";
> 4	
> 5	const corsHeaders = {
> 6	  "Access-Control-Allow-Origin": "*",
> 7	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 8	  "Access-Control-Allow-Headers":
> 9	    "authorization, x-client-info, apikey, content-type",
> 10	};
> 11	
> 12	// ── Credit costs per operation (in mcoCoins) ─────────────────────────────
> 13	// Aligned with .claude/context/higgsfield-api-validation-2026-05-15.md:
> 14	// Higgsfield pricing is $1 = 16 credits; mcoCoins markup ~13x over USD cost.
> 15	const CREDIT_COSTS: Record<string, number> = {
> 16	  "openai/dall-e-3": 15,
> 17	  "openai/gpt-image-1": 18,
> 18	  "replicate/flux-1.1-pro": 12,
> 19	  "replicate/sdxl": 4,
> 20	  "replicate/flux-schnell": 3,
> 21	  "openrouter/dall-e-3": 15,
> 22	  "openrouter/google/gemini-2.5-flash-image": 10,
> 23	  "openrouter/black-forest-labs/flux-1.1-pro": 12,
> 24	  // Higgsfield Soul (text-to-image) — tiered by resolution × batch.
> 25	  // "higgsfield/generate" kept as legacy alias → resolves to soul-1080p-1.
> 26	  "higgsfield/generate": 40,
> 27	  "higgsfield/soul-720p-1": 20,   // 1.5 hf credits ≈ $0.09
> 28	  "higgsfield/soul-720p-4": 26,   // 2.0 hf credits ≈ $0.13
> 29	  "higgsfield/soul-1080p-1": 40,  // 3.0 hf credits ≈ $0.19
> 30	  "higgsfield/soul-1080p-4": 65,  // 5.0 hf credits ≈ $0.31
> 31	  // Higgsfield DoP (image-to-video) — added in Phase 5.3 along with webhook flow.
> 32	  "higgsfield/dop-lite-5s": 30,       // placeholder; 2 hf credits ≈ $0.13
> 33	  "higgsfield/dop-turbo-5s": 90,      // placeholder; 6.5 hf credits ≈ $0.41
> 34	  "higgsfield/dop-standard-5s": 125,  // placeholder; 9 hf credits ≈ $0.56
> 35	  // Kling 2.1 Pro pricing not tabulated by Higgsfield; placeholder, confirm via Cloud Dashboard.
> 36	  "higgsfield/kling-2.1-pro-5s": 160,
> 37	  "higgsfield/seedance-v1-pro-5s": 130,
> 38	  "upscale-2x": 8,
> 39	  "upscale-4x": 20,
> 40	  "inpaint": 6,
> 41	  "scene-compose": 18,
> 42	  "style-transfer": 14,
> 43	  "remove-background": 3,
> 44	};
> 45	
> 46	// Image-gen prompts above this length get rejected with a clear error.
> 47	// Image models (Nano Banana 2, FLUX, DALL-E) read very long prompts as
> 48	// instructions and return text — Sovereign hit this on 2026-05-26 with a
> 49	// 600-word protocol template. 1800 chars ≈ 280 words ≈ Midjourney guidance.
> 50	const MAX_IMAGE_PROMPT_CHARS = 1800;
> 51	
> 52	// Lowercase signals that a prompt is a system-instruction, not a description.
> 53	// Used by detectInstructionStylePrompt to flag prompts before sending; surfaces
> 54	// a clearer error than the downstream "no image_url" symptom.
> 55	const INSTRUCTION_SIGNAL_RE =
> 56	  /\b(you are |your (core )?function (is|will)|your objective|identity & protocol|output only|system instruction|return only|do not (add|write|include))\b/i;
> 57	
> 58	function isImagePromptTooLong(prompt: string): boolean {
> 59	  return prompt.length > MAX_IMAGE_PROMPT_CHARS;
> 60	}
> 61	
> 62	function detectInstructionStylePrompt(prompt: string): boolean {
> 63	  return INSTRUCTION_SIGNAL_RE.test(prompt);
> 64	}
> 65	
> 66	// Resolve Higgsfield Soul cost from resolution × batch parameters.
> 67	// Returns undefined if the body isn't a Soul/legacy Higgsfield request.
> 68	function resolveHiggsfieldSoulKey(body: ExecuteRequest): string | undefined {
> 69	  if (body.provider !== "higgsfield") return undefined;
> 70	  if (body.model !== "soul" && body.model !== "generate") return undefined;
> 71	  const res = body.parameters?.resolution === "720p" ? "720p" : "1080p";
> 72	  const batch = body.parameters?.batch === 4 ? 4 : 1;
> 73	  return `higgsfield/soul-${res}-${batch}`;
> 74	}
> 75	
> 76	interface ExecuteRequest {
> 77	  project_id: string;
> 78	  node_id: string;
> 79	  node_type: string;
> 80	  provider: string;
> 81	  model: string;
> 82	  prompt: string;
> 83	  negative_prompt?: string;
> 84	  parameters?: Record<string, any>;
> 85	  input_asset_url?: string;
> 86	  input_asset_id?: string;
> 87	  input_image_1?: string;
> 88	  input_image_2?: string;
> 89	  input_layout?: string;
> 90	  // Cross-node consistency (Phase 4.3): upstream connected node outputs passed
> 91	  // as reference images, + a locked seed propagated across the connected graph.
> 92	  // SOP: docs/processes/canvas-node-consistency.md. Fail-open: absent = current behavior.
> 93	  reference_image_urls?: string[];
> 94	  seed?: number;
> 95	}
> 96	
> 97	serve(async (req) => {
> 98	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 99	
> 100	  try {
> 101	    const authHeader = req.headers.get("Authorization");
> 102	    if (!authHeader) {
> 103	      return new Response(JSON.stringify({ error: "Missing authorization" }), {
> 104	        status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" },
> 105	      });
> 106	    }
> 107	
> 108	    const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
> 109	    const supabaseAnonKey = (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!;
> 110	    const supabase = createClient(supabaseUrl, supabaseAnonKey, {
> 111	      global: { headers: { Authorization: authHeader } },
> 112	    });
> 113	
> 114	    const { data: { user }, error: authError } = await supabase.auth.getUser();
> 115	    if (authError || !user) {
> 116	      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 117	        status: 401, headers: { ...corsHeaders, "Content-Type": "application/json" },
> 118	      });
> 119	    }
> 120	
> 121	    const body: ExecuteRequest = await req.json();
> 122	    if (!body.project_id || !body.node_id || !body.prompt) {
> 123	      return new Response(JSON.stringify({ error: "project_id, node_id, and prompt are required" }), {
> 124	        status: 400, headers: { ...corsHeaders, "Content-Type": "application/json" },
> 125	      });
> 126	    }
> 127	
> 128	    const admin = createClient(supabaseUrl, (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!);
> 129	
> 130	    // ── Resolve API keys (user keys > vault secrets) ─────────────────
> 131	    const { data: userKeys } = await admin
> 132	      .from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 133	
> 134	    // Pure per-user credential resolution (API Tenancy Model) — NO global env fallback for provider keys (env is
> 135	    // infra-only). Higgsfield is a key+secret PAIR; both come from the tenant's own BYOK (a half-populated row just
> 136	    // fails closed at the provider, which is the correct BYOK behavior).
> 137	    const keys = {
> 138	      openai: userKeys?.openai_api_key || "",
> 139	      replicate: userKeys?.replicate_api_key || "",
> 140	      openrouter: userKeys?.openrouter_api_key || "",
> 141	      gemini: userKeys?.google_api_key || "",
> 142	      higgsfield: userKeys?.higgsfield_api_key || "",
> 143	      higgsfield_secret: userKeys?.higgsfield_api_key_secret || "",
> 144	    };
> 145	
> 146	    // ── Calculate credit cost ────────────────────────────────────────
> 147	    // Higgsfield Soul resolves to a tiered key (resolution × batch); other
> 148	    // providers fall back to the provider/model lookup or the node_type slug.
> 149	    let creditCost = 10;
> 150	    if (body.node_type === "magic_prompt") {
> 151	      const level = body.parameters?.level || "curto";
> 152	      creditCost = level === "longo" ? 5 : (level === "medio" ? 2 : 1);
> 153	    } else {
> 154	      const higgsfieldSoulKey = resolveHiggsfieldSoulKey(body);
> 155	      const costKey = higgsfieldSoulKey
> 156	        ?? (body.node_type === "image_to_video"
> 157	          ? `${body.provider}/${body.model}-${body.parameters?.duration || 5}s`
> 158	          : (body.node_type === "generate_image"
> 159	            ? `${body.provider}/${body.model}`
> 160	            : body.node_type.replace("_", "-")));
> 161	      creditCost = CREDIT_COSTS[costKey] || 10;
> 162	    }
> 163	
> 164	    // ── Check user credits (mco_balance in profiles) ─────────────────
> 165	    const { data: profile } = await admin
> 166	      .from("profiles").select("mco_balance").eq("id", user.id).single();
> 167	
> 168	    if (!profile || (profile.mco_balance || 0) < creditCost) {
> 169	      return new Response(JSON.stringify({
> 170	        error: "Insufficient mcoCoins",
> 171	        required: creditCost,
> 172	        balance: profile?.mco_balance || 0,
> 173	      }), { status: 402, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 174	    }
> 175	
> 176	    // ── SSP-01 OE04 — Daily cap enforcement (dinâmico com base na role) ──
> 177	    // Sums abs(amount) of canvas_* ledger entries in the rolling 24h window.
> 178	    // Fail-open on query error to avoid blocking UX when observability is down.
> 179	    let dailyCap = 100;
> 180	    const { data: roleRow, error: roleErr } = await admin
> 181	      .from("user_roles")
> 182	      .select("role")
> 183	      .eq("user_id", user.id)
> 184	      .maybeSingle();
> 185	
> 186	    if (roleErr) {
> 187	      console.error("[canvas-execute] failed to fetch user role for daily cap:", roleErr);
> 188	    } else if (roleRow?.role === "admin") {
> 189	      dailyCap = 10000;
> 190	    } else if (roleRow?.role === "editor") {
> 191	      dailyCap = 1000;
> 192	    }
> 193	
> 194	    const dayAgoIso = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();
> 195	    const { data: spendRows, error: spendErr } = await admin
> 196	      .from("mcoin_transactions")
> 197	      .select("amount")
> 198	      .eq("user_id", user.id)
> 199	      .like("action", "canvas_%spend")
> 200	      .gte("created_at", dayAgoIso);
> 201	
> 202	    if (spendErr) {
> 203	      console.error("[canvas-execute] daily cap query error:", spendErr);
> 204	    }
> 205	    const spentToday = (spendRows ?? []).reduce(
> 206	      (sum, r) => sum + Math.abs(Number(r.amount) || 0),
> 207	      0,
> 208	    );
> 209	    if (spentToday + creditCost > dailyCap) {
> 210	      return new Response(JSON.stringify({
> 211	        error: "Daily Canvas cap reached",
> 212	        cap: dailyCap,
> 213	        spent_today: spentToday,
> 214	        required: creditCost,
> 215	        resets_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString(),
> 216	      }), { status: 402, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 217	    }
> 218	
> 219	    const ALLOWED_VIDEO_MODELS = [
> 220	      "dop-lite",
> 221	      "dop-turbo",
> 222	      "dop-standard",
> 223	      "kling-2.1-pro",
> 224	      "seedance-v1-pro",
> 225	    ];
> 226	    if (body.node_type === "image_to_video" && !ALLOWED_VIDEO_MODELS.includes(body.model)) {
> 227	      return new Response(JSON.stringify({
> 228	        error: "Tier indisponível — selecione um modelo de vídeo válido nesta fase",
> 229	        model_requested: body.model,
> 230	        allowed: ALLOWED_VIDEO_MODELS,
> 231	      }), { status: 422, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 232	    }
> 233	
> 234	    // ── Map node_type for database enum compliance ───────────────────
> 235	    // vm_node_type enum: generate_image, generate_video, upscale, inpaint,
> 236	    // outpaint, style_transfer, relight, remove_background, extend, remix, compose, export
> 237	    const NODE_TYPE_MAP: Record<string, string> = {
> 238	      image_to_video: "generate_video",
> 239	      scene_compose: "compose",
> 240	      magic_prompt: "generate_image",
> 241	      generate_image: "generate_image",
> 242	      style_transfer: "style_transfer",
> 243	      upscale: "upscale",
> 244	      inpaint: "inpaint",
> 245	      outpaint: "outpaint",
> 246	      relight: "relight",
> 247	      remove_background: "remove_background",
> 248	      extend: "extend",
> 249	      remix: "remix",
> 250	      compose: "compose",
> 251	      export: "export",
> 252	    };
> 253	    const dbNodeType = NODE_TYPE_MAP[body.node_type] ?? body.node_type;
> 254	    if (!NODE_TYPE_MAP[body.node_type]) {
> 255	      console.warn(`[canvas-execute] unmapped node_type "${body.node_type}" — passing through as-is`);
> 256	    }
> 257	
> 258	    // ── Resolve parent/input asset ID ────────────────────────────────
> 259	    let resolvedInputAssetId: string | null = null;
> 260	    if (body.input_asset_id) {
> 261	      resolvedInputAssetId = body.input_asset_id;
> 262	    } else if (body.input_asset_url) {
> 263	      const { data: matchedAsset } = await admin
> 264	        .from("vm_canvas_assets")
> 265	        .select("id")
> 266	        .eq("public_url", body.input_asset_url)
> 267	        .limit(1)
> 268	        .maybeSingle();
> 269	      if (matchedAsset) {
> 270	        resolvedInputAssetId = matchedAsset.id;
> 271	      }
> 272	    }
> 273	
> 274	    // ── Create execution record ──────────────────────────────────────
> 275	    // For async video jobs we insert as 'queued' (no deduct yet — webhook
> 276	    // finalizes atomically). Sync image jobs go 'running' as before.
> 277	    const initialStatus = body.node_type === "image_to_video" ? "queued" : "running";
> 278	    const { data: execution, error: execErr } = await admin
> 279	      .from("vm_canvas_executions")
> 280	      .insert({
> 281	        project_id: body.project_id,
> 282	        user_id: user.id,
> 283	        node_id: body.node_id,
> 284	        node_type: dbNodeType,
> 285	        provider: body.provider,
> 286	        model: body.model,
> 287	        prompt: body.prompt,
> 288	        negative_prompt: body.negative_prompt,
> 289	        parameters: body.parameters || {},
> 290	        credits_charged: creditCost,
> 291	        status: initialStatus,
> 292	        started_at: new Date().toISOString(),
> 293	        input_asset_id: resolvedInputAssetId,
> 294	      })
> 295	      .select()
> 296	      .single();
> 297	
> 298	    if (execErr) {
> 299	      console.error("Execution insert error:", execErr);
> 300	      return new Response(JSON.stringify({
> 301	        error: "Failed to create execution record",
> 302	        detail: execErr.message,
> 303	        code: execErr.code,
> 304	        hint: execErr.hint ?? undefined,
> 305	        node_type_received: body.node_type,
> 306	        node_type_mapped: dbNodeType,
> 307	      }), {
> 308	        status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" },
> 309	      });
> 310	    }
> 311	
> 312	    // ── Magic Prompt generation ──────────────────────────────────────
> 313	    if (body.node_type === "magic_prompt") {
> 314	      let campaignContext = "Nenhum contexto de campanha disponível.";
> 315	      try {
> 316	        if (body.project_id) {
> 317	          const { data: project } = await admin
> 318	            .from("vm_canvas_projects")
> 319	            .select("name, description, campaign_id")
> 320	            .eq("id", body.project_id)
> 321	            .maybeSingle();
> 322	          
> 323	          if (project) {
> 324	            let campaignId = project.campaign_id;
> 325	            if (!campaignId) {
> 326	              const { data: latestCampaign } = await admin
> 327	                .from("campaigns")
> 328	                .select("id")
> 329	                .eq("user_id", user.id)
> 330	                .order("created_at", { ascending: false })
> 331	                .limit(1)
> 332	                .maybeSingle();
> 333	              if (latestCampaign) campaignId = latestCampaign.id;
> 334	            }
> 335	
> 336	            if (campaignId) {
> 337	              const { data: campaign } = await admin
> 338	                .from("campaigns")
> 339	                .select("name, description, target_audience, keywords")
> 340	                .eq("id", campaignId)
> 341	                .maybeSingle();
> 342	              if (campaign) {
> 343	                campaignContext = `Campanha: ${campaign.name}
> 344	Descrição: ${campaign.description || ""}
> 345	Público-Alvo: ${campaign.target_audience || ""}
> 346	Palavras-chave: ${Array.isArray(campaign.keywords) ? campaign.keywords.join(", ") : (campaign.keywords || "")}`;
> 347	              }
> 348	            }
> 349	          }
> 350	        }
> 351	
> 352	        const level = body.parameters?.level || "curto";
> 353	        const modelName = body.parameters?.target_model || "generic";
> 354	        const enhancedPrompt = await generateMagicPrompt(
> 355	          keys.openrouter,
> 356	          keys.gemini,
> 357	          body.prompt,
> 358	          level,
> 359	          modelName,
> 360	          campaignContext,
> 361	        );
> 362	
> 363	        // Finalize execution with success state and result payload
> 364	        await admin
> 365	          .from("vm_canvas_executions")
> 366	          .update({
> 367	            status: "success",
> 368	            output_url: null,
> 369	            response_payload: { enhanced_prompt: enhancedPrompt },
> 370	            completed_at: new Date().toISOString(),
> 371	          })
> 372	          .eq("id", execution.id);
> 373	
> 374	        // Deduct mcoCoins
> 375	        await admin.rpc("deduct_mco_coins", {
> 376	          p_user_id: user.id,
> 377	          p_amount: creditCost,
> 378	          p_action: "canvas_magic_prompt_spend",
> 379	          p_context: {
> 380	            execution_id: execution.id,
> 381	            node_id: body.node_id,
> 382	            level,
> 383	          },
> 384	        });
> 385	
> 386	        await admin
> 387	          .from("infra_health_logs")
> 388	          .insert({ service: "canvas-execute", status: "healthy" })
> 389	          .then(() => {}, (e: unknown) => console.error("[canvas-execute] health log failed:", e));
> 390	
> 391	        return new Response(
> 392	          JSON.stringify({
> 393	            execution_id: execution.id,
> 394	            status: "success",
> 395	            enhanced_prompt: enhancedPrompt,
> 396	            credits_charged: creditCost,
> 397	          }),
> 398	          { headers: { ...corsHeaders, "Content-Type": "application/json" } },
> 399	        );
> 400	      } catch (err: any) {
> 401	        console.error("Magic Prompt generation failed:", err);
> 402	        await admin
> 403	          .from("vm_canvas_executions")
> 404	          .update({
> 405	            status: "failed",
> 406	            error_message: err.message || "Failed to generate magic prompt",
> 407	            completed_at: new Date().toISOString(),
> 408	          })
> 409	          .eq("id", execution.id);
> 410	
> 411	        await admin
> 412	          .from("infra_health_logs")
> 413	          .insert({ service: "canvas-execute", status: "unhealthy" })
> 414	          .then(() => {}, (e: unknown) => console.error("[canvas-execute] health log failed:", e));
> 415	
> 416	        return new Response(JSON.stringify({ error: err.message || "Failed to generate magic prompt" }), {
> 417	          status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" },
> 418	        });
> 419	      }
> 420	    }
> 421	
> 422	    // ── Phase 4.2c async video branch ────────────────────────────────
> 423	    // image_to_video: submit to Higgsfield with ?hf_webhook=<callback>,
> 424	    // return immediately with status='queued'. Webhook does atomic deduct
> 425	    // after upload-OK; useCanvasJobsRealtime flips the UI when status moves.
> 426	    if (body.node_type === "image_to_video") {
> 427	      return await submitHiggsfieldVideo({
> 428	        admin,
> 429	        supabaseUrl,
> 430	        apiKey: keys.higgsfield,
> 431	        apiSecret: keys.higgsfield_secret,
> 432	        body,
> 433	        execution,
> 434	        corsHeaders,
> 435	      });
> 436	    }
> 437	
> 438	    // ── Route to provider ────────────────────────────────────────────
> 439	    let outputUrl = "";
> 440	    let outputB64 = "";
> 441	    let error = "";
> 442	
> 443	    try {
> 444	      if (body.provider === "openai") {
> 445	        const result = await generateOpenAI(keys.openai, body);
> 446	        outputUrl = result.url;
> 447	        outputB64 = result.b64;
> 448	      } else if (body.provider === "replicate") {
> 449	        const result = await generateReplicate(keys.replicate, body);
> 450	        outputUrl = result.url;
> 451	      } else if (body.provider === "openrouter") {
> 452	        const result = await generateOpenRouter(keys.openrouter, body);
> 453	        outputUrl = result.url;
> 454	        outputB64 = result.b64;
> 455	      } else if (body.provider === "higgsfield") {
> 456	        const result = await generateHiggsfield(keys.higgsfield, keys.higgsfield_secret, body);
> 457	        outputUrl = result.url;
> 458	      } else {
> 459	        throw new Error(`Unknown provider: ${body.provider}`);
> 460	      }
> 461	    } catch (providerErr: any) {
> 462	      error = providerErr.message || "Provider error";
> 463	      console.error(`Provider ${body.provider} error:`, providerErr);
> 464	    }
> 465	
> 466	    // ── Upload to storage (b64 OR URL response) ──────────────────────
> 467	    // Round 3 hotfix: OpenAI defaults to URL response (no response_format).
> 468	    // OpenRouter chat-completions multimodal returns URL. Both paths must
> 469	    // persist to canvas-assets so the provider URL's short TTL doesn't break
> 470	    // the asset_url stored in vm_canvas_assets. Pattern mirrors rescue-video
> 471	    // (Google Veo) + higgsfield-webhook (DoP video) download+upload flow.
> 472	    let storedUrl = outputUrl;
> 473	    let storedKey: string | null = null;
> 474	    let storedContentType = "image/png";
> 475	    if (!error && (outputB64 || outputUrl)) {
> 476	      try {
> 477	        let bytes: Uint8Array | null = null;
> 478	        let contentType = "image/png";
> 479	
> 480	        if (outputB64) {
> 481	          bytes = Uint8Array.from(atob(outputB64), (c) => c.charCodeAt(0));
> 482	        } else if (outputUrl) {
> 483	          // Fetch the provider's signed URL, validate, then re-host in bucket.
> 484	          const dlResp = await fetch(outputUrl);
> 485	          if (dlResp.ok) {
> 486	            const ct = dlResp.headers.get("content-type") || "";
> 487	            if (ct.startsWith("image/")) contentType = ct;
> 488	            bytes = new Uint8Array(await dlResp.arrayBuffer());
> 489	          } else {
> 490	            console.error("[canvas-execute] provider URL fetch failed:", dlResp.status);
> 491	          }
> 492	        }
> 493	
> 494	        if (bytes && bytes.byteLength > 0) {
> 495	          const ext = contentType.split("/")[1]?.split(";")[0] || "png";
> 496	          const fileName = `${user.id}/${execution.id}.${ext}`;
> 497	          const { error: uploadErr } = await admin.storage
> 498	            .from("canvas-assets")
> 499	            .upload(fileName, bytes, { contentType, upsert: true });
> 500	          if (!uploadErr) {
> 501	            const { data: urlData } = admin.storage
> 502	              .from("canvas-assets")
> 503	              .getPublicUrl(fileName);
> 504	            storedUrl = urlData.publicUrl;
> 505	            storedKey = fileName;
> 506	            storedContentType = contentType;
> 507	          } else {
> 508	            console.error("[canvas-execute] upload error:", uploadErr);
> 509	          }
> 510	        }
> 511	      } catch (uploadErr) {
> 512	        console.error("Upload error:", uploadErr);
> 513	      }
> 514	    }
> 515	
> 516	    // ── Save asset record ────────────────────────────────────────────
> 517	    let assetId: string | null = null;
> 518	    if (!error && storedUrl) {
> 519	      const { data: asset } = await admin
> 520	        .from("vm_canvas_assets")
> 521	        .insert({
> 522	          user_id: user.id,
> 523	          project_id: body.project_id,
> 524	          asset_type: "image",
> 525	          storage_key: storedKey ?? `${user.id}/${execution.id}.png`,
> 526	          storage_bucket: "canvas-assets",
> 527	          public_url: storedUrl,
> 528	          mime_type: storedContentType,
> 529	          provider: body.provider,
> 530	          model_used: body.model,
> 531	          node_type: dbNodeType,
> 532	          prompt: body.prompt,
> 533	          negative_prompt: body.negative_prompt,
> 534	          parameters: body.parameters || {},
> 535	          credits_cost: creditCost,
> 536	          node_id: body.node_id,
> 537	          input_asset_id: resolvedInputAssetId,
> 538	        })
> 539	        .select("id")
> 540	        .single();
> 541	      assetId = asset?.id;
> 542	
> 543	      // Dual-write to the canonical asset registry (creative_assets) so the HyperFrames editor / other modules can
> 544	      // reuse this Canvas output bidirectionally (the "power of the outputs" spine). Fail-soft — never break exec.
> 545	      try {
> 546	        await admin.rpc("register_creative_asset", {
> 547	          p_user_id: user.id,
> 548	          p_kind: "image",
> 549	          p_storage_bucket: "canvas-assets",
> 550	          p_storage_key: storedKey ?? `${user.id}/${execution.id}.png`,
> 551	          p_is_public: true,
> 552	          p_source_module: "canvas-studio",
> 553	          p_source_job_id: execution.id,
> 554	          p_mime_type: storedContentType,
> 555	          p_provider: body.provider,
> 556	          p_model: body.model,
> 557	          p_prompt: body.prompt,
> 558	        });
> 559	      } catch (e) {
> 560	        console.error("[canvas-execute] creative_assets register skipped:", e);
> 561	      }
> 562	    }
> 563	
> 564	    // ── Update execution status ──────────────────────────────────────
> 565	    const finalStatus = error ? "failed" : "success";
> 566	    await admin
> 567	      .from("vm_canvas_executions")
> 568	      .update({
> 569	        status: finalStatus,
> 570	        output_url: storedUrl || null,
> 571	        output_asset_id: assetId,
> 572	        error_message: error || null,
> 573	        completed_at: new Date().toISOString(),
> 574	      })
> 575	      .eq("id", execution.id);
> 576	
> 577	    // ── SSP-01 OE03 Pillar 4 (Observability) ─────────────────────────
> 578	    // Best-effort health pulse; failure to log MUST NOT block the response.
> 579	    await admin
> 580	      .from("infra_health_logs")
> 581	      .insert({ service: "canvas-execute", status: error ? "unhealthy" : "healthy" })
> 582	      .then(() => {}, (e: unknown) => console.error("[canvas-execute] health log failed:", e));
> 583	
> 584	    // ── Deduct credits on success ────────────────────────────────────
> 585	    // SSP-01 OE04: action tagging is REQUIRED for the daily cap query to work.
> 586	    // canvas_image_spend / canvas_video_spend are the canonical action tags.
> 587	    if (!error) {
> 588	      const spendAction = body.node_type === "image_to_video"
> 589	        ? "canvas_video_spend"
> 590	        : "canvas_image_spend";
> 591	      await admin.rpc("deduct_mco_coins", {
> 592	        p_user_id: user.id,
> 593	        p_amount: creditCost,
> 594	        p_action: spendAction,
> 595	        p_context: {
> 596	          execution_id: execution.id,
> 597	          provider: body.provider,
> 598	          model: body.model,
> 599	          node_type: body.node_type,
> 600	        },
> 601	      });
> 602	
> 603	      // Update project stats
> 604	      await admin
> 605	        .from("vm_canvas_projects")
> 606	        .update({
> 607	          total_executions: (await admin.from("vm_canvas_executions")
> 608	            .select("id", { count: "exact" })
> 609	            .eq("project_id", body.project_id)
> 610	            .eq("status", "success")).count || 0,
> 611	          last_execution_at: new Date().toISOString(),
> 612	        })
> 613	        .eq("id", body.project_id);
> 614	    }
> 615	
> 616	    return new Response(JSON.stringify({
> 617	      execution_id: execution.id,
> 618	      status: finalStatus,
> 619	      output_url: storedUrl || null,
> 620	      asset_id: assetId,
> 621	      credits_charged: error ? 0 : creditCost,
> 622	      credits_remaining: error ? profile.mco_balance : (profile.mco_balance || 0) - creditCost,
> 623	      error: error || undefined,
> 624	    }), { headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 625	
> 626	  } catch (e) {
> 627	    console.error("canvas-execute error:", e);
> 628	    return new Response(JSON.stringify({ error: e instanceof Error ? e.message : "Unknown error" }), {
> 629	      status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" },
> 630	    });
> 631	  }
> 632	});
> 633	
> 634	// ═══════════════════════════════════════════════════════════════════════════
> 635	// PROVIDER IMPLEMENTATIONS
> 636	// ═══════════════════════════════════════════════════════════════════════════
> 637	
> 638	async function generateOpenAI(apiKey: string, body: ExecuteRequest) {
> 639	  if (!apiKey) throw new Error("OpenAI API key not configured");
> 640	
> 641	  const model = body.model || "dall-e-3";
> 642	  const size = body.parameters?.size || "1024x1024";
> 643	
> 644	  // Round 3 hotfix (2026-05-17): OpenAI rejected `response_format` for both
> 645	  // `gpt-image-1` AND `dall-e-3` on the /v1/images/generations endpoint with
> 646	  // HTTP 400 "Unknown parameter". We now omit the param — OpenAI defaults to
> 647	  // returning a URL (for dall-e-*) or b64_json (for gpt-image-1). The caller
> 648	  // upload block already handles both shapes via {url, b64} return contract.
> 649	  const payload: Record<string, unknown> = {
> 650	    model,
> 651	    prompt: body.prompt,
> 652	    n: 1,
> 653	    size,
> 654	  };
> 655	  // quality + style only apply to dall-e-3; gpt-image-1 ignores them.
> 656	  if (body.parameters?.quality) payload.quality = body.parameters.quality;
> 657	  if (body.parameters?.style) payload.style = body.parameters.style;
> 658	
> 659	  const resp = await fetch("https://api.openai.com/v1/images/generations", {
> 660	    method: "POST",
> 661	    headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
> 662	    body: JSON.stringify(payload),
> 663	  });
> 664	
> 665	  if (!resp.ok) {
> 666	    const t = await resp.text();
> 667	    throw new Error(`OpenAI error ${resp.status}: ${t}`);
> 668	  }
> 669	
> 670	  const data = await resp.json();
> 671	  // gpt-image-1 returns b64_json by default; dall-e-* returns url. Caller's
> 672	  // upload block prefers b64 (direct upload) but falls back to URL download.
> 673	  return { url: data.data?.[0]?.url || "", b64: data.data?.[0]?.b64_json || "" };
> 674	}
> 675	
> 676	async function generateReplicate(apiKey: string, body: ExecuteRequest) {
> 677	  if (!apiKey) throw new Error("Replicate API key not configured");
> 678	
> 679	  const modelMap: Record<string, string> = {
> 680	    "flux-1.1-pro": "black-forest-labs/flux-1.1-pro",
> 681	    "flux-schnell": "black-forest-labs/flux-schnell",
> 682	    "sdxl": "stability-ai/sdxl:39ed52f2a78e934b3ba6e2a89f5b1c712de7dfea535525255b1aa35c5565e08b",
> 683	  };
> 684	
> 685	  const modelId = modelMap[body.model] || body.model;
> 686	  const input: Record<string, any> = {
> 687	    prompt: body.prompt,
> 688	    ...(body.negative_prompt ? { negative_prompt: body.negative_prompt } : {}),
> 689	    ...(body.parameters?.width ? { width: body.parameters.width } : {}),
> 690	    ...(body.parameters?.height ? { height: body.parameters.height } : {}),
> 691	    ...(body.parameters?.num_inference_steps ? { num_inference_steps: body.parameters.num_inference_steps } : {}),
> 692	    ...(body.parameters?.guidance_scale ? { guidance_scale: body.parameters.guidance_scale } : {}),
> 693	  };
> 694	
> 695	  // Cross-node consistency: seed (reproducibility, all models) + reference image
> 696	  // mapped to each model's img2img param. flux-schnell has no image input → skip.
> 697	  // SOP: docs/processes/canvas-node-consistency.md. Fail-open if no reference/seed.
> 698	  const seedVal = typeof body.seed === "number"
> 699	    ? body.seed
> 700	    : (typeof body.parameters?.seed === "number" ? body.parameters.seed : undefined);
> 701	  if (typeof seedVal === "number") input.seed = seedVal;
> 702	  const refUrl = (body.reference_image_urls ?? []).filter(Boolean)[0];
> 703	  if (refUrl) {
> 704	    if (body.model === "flux-1.1-pro") {
> 705	      input.image_prompt = refUrl; // FLUX 1.1 Pro: composition reference
> 706	    } else if (body.model === "sdxl") {
> 707	      input.image = refUrl; // SDXL img2img
> 708	      input.prompt_strength = typeof body.parameters?.prompt_strength === "number"
> 709	        ? body.parameters.prompt_strength
> 710	        : 0.75;
> 711	    }
> 712	    // flux-schnell intentionally omitted (text-to-image only).
> 713	  }
> 714	
> 715	  // Create prediction
> 716	  const createResp = await fetch("https://api.replicate.com/v1/predictions", {
> 717	    method: "POST",
> 718	    headers: { Authorization: `Bearer ${apiKey}`, "Content-Type": "application/json" },
> 719	    body: JSON.stringify({ model: modelId.includes(":") ? undefined : modelId, version: modelId.includes(":") ? modelId.split(":")[1] : undefined, input }),
> 720	  });
> 721	
> 722	  if (!createResp.ok) {
> 723	    const t = await createResp.text();
> 724	    throw new Error(`Replicate error ${createResp.status}: ${t}`);
> 725	  }
> 726	
> 727	  let prediction = await createResp.json();
> 728	
> 729	  // Poll for completion (max 120s)
> 730	  const maxWait = 120_000;
> 731	  const start = Date.now();
> 732	  while (prediction.status !== "succeeded" && prediction.status !== "failed" && Date.now() - start < maxWait) {
> 733	    await new Promise((r) => setTimeout(r, 2000));
> 734	    const pollResp = await fetch(prediction.urls.get, {
> 735	      headers: { Authorization: `Bearer ${apiKey}` },
> 736	    });
> 737	    prediction = await pollResp.json();
> 738	  }
> 739	
> 740	  if (prediction.status === "failed") {
> 741	    throw new Error(`Replicate failed: ${prediction.error}`);
> 742	  }
> 743	
> 744	  const output = Array.isArray(prediction.output) ? prediction.output[0] : prediction.output;
> 745	  return { url: output || "" };
> 746	}
> 747	
> 748	async function generateOpenRouter(apiKey: string, body: ExecuteRequest) {
> 749	  if (!apiKey) throw new Error("OpenRouter API key not configured");
> 750	
> 751	  if (isImagePromptTooLong(body.prompt)) {
> 752	    throw new Error(
> 753	      `Prompt muito longo (${body.prompt.length} chars; máximo ${MAX_IMAGE_PROMPT_CHARS}). Modelos de imagem interpretam prompts longos como instruções de texto e devolvem texto, não imagem. Use o botão Magic Prompt para reformular como descrição visual concisa.`,
> 754	    );
> 755	  }
> 756	
> 757	  if (detectInstructionStylePrompt(body.prompt)) {
> 758	    throw new Error(
> 759	      `Prompt parece uma instrução de sistema (contém "You are X" / "Output ONLY" / similar), não uma descrição visual. Modelos como Nano Banana 2 responderão com texto em vez de imagem. Reformule como descrição: "A [sujeito], [detalhes], [iluminação/estilo]" ou use o Magic Prompt.`,
> 760	    );
> 761	  }
> 762	
> 763	  // Round 3 hotfix (2026-05-17): /v1/images/generations returns 404 HTML on
> 764	  // OpenRouter — endpoint was deprecated. OpenRouter image generation now
> 765	  // routes through /v1/chat/completions with `modalities: ["image", "text"]`
> 766	  // for models that support image OUTPUT (e.g. google/gemini-2.5-flash-image-preview,
> 767	  // black-forest-labs/flux-1.1-pro). Response shape: choices[0].message.content
> 768	  // is an array of multimodal parts; image parts have type `image_url` with
> 769	  // `image_url.url` carrying the asset URL.
> 770	  const model = body.model || "google/gemini-2.5-flash-image";
> 771	
> 772	  // Cross-node consistency: attach upstream reference images as image_url parts.
> 773	  // Gemini ("Nano Banana") accepts up to 4 character refs to preserve identity.
> 774	  // image_url.url takes both https (preferred — bucket URLs) and data: URIs.
> 775	  // Fail-open: no references → plain text content (current behavior, zero regression).
> 776	  const refUrls = (body.reference_image_urls ?? []).filter(Boolean).slice(0, 4);
> 777	  const userContent: unknown = refUrls.length === 0
> 778	    ? body.prompt
> 779	    : [
> 780	        { type: "text", text: body.prompt },
> 781	        ...refUrls.map((url) => ({ type: "image_url", image_url: { url } })),
> 782	      ];
> 783	
> 784	  const resp = await fetch("https://openrouter.ai/api/v1/chat/completions", {
> 785	    method: "POST",
> 786	    headers: {
> 787	      Authorization: `Bearer ${apiKey}`,
> 788	      "Content-Type": "application/json",
> 789	      "HTTP-Referer": "https://mcorch.com",
> 790	      "X-Title": "GCRUX Canvas Studio",
> 791	    },
> 792	    body: JSON.stringify({
> 793	      model,
> 794	      modalities: ["image", "text"],
> 795	      messages: [{ role: "user", content: userContent }],
> 796	    }),
> 797	  });
> 798	
> 799	  if (!resp.ok) {
> 800	    const t = await resp.text();
> 801	    throw new Error(`OpenRouter error ${resp.status}: ${t.slice(0, 200)}`);
> 802	  }
> 803	
> 804	  const data = await resp.json();
> 805	  const message = data?.choices?.[0]?.message;
> 806	  if (!message) throw new Error("OpenRouter: resposta sem message");
> 807	
> 808	  // Two output shapes seen in the wild:
> 809	  //   1. message.content = string (text only — image missing)
> 810	  //   2. message.content = [{type:'text',text:...}, {type:'image_url', image_url:{url:'data:...' | 'https://...'}}]
> 811	  //   3. message.images = [{url:'...'}] (some OR providers return separate field)
> 812	  let outUrl = "";
> 813	  let outB64 = "";
> 814	
> 815	  if (Array.isArray(message.content)) {
> 816	    for (const part of message.content) {
> 817	      if (part?.type === "image_url" && part?.image_url?.url) {
> 818	        const u = String(part.image_url.url);
> 819	        if (u.startsWith("data:image/")) {
> 820	          outB64 = u.split(",", 2)[1] ?? "";
> 821	        } else {
> 822	          outUrl = u;
> 823	        }
> 824	        break;
> 825	      }
> 826	    }
> 827	  }
> 828	
> 829	  if (!outUrl && !outB64 && Array.isArray(message?.images) && message.images.length > 0) {
> 830	    const first = message.images[0];
> 831	    let u = "";
> 832	    if (typeof first === "string") {
> 833	      u = first;
> 834	    } else if (first) {
> 835	      if (first.url) {
> 836	        u = String(first.url);
> 837	      } else if (first.image_url?.url) {
> 838	        u = String(first.image_url.url);
> 839	      }
> 840	    }
> 841	
> 842	    if (u) {
> 843	      if (u.startsWith("data:image/")) {
> 844	        outB64 = u.split(",", 2)[1] ?? "";
> 845	      } else {
> 846	        outUrl = u;
> 847	      }
> 848	    }
> 849	  }
> 850	
> 851	  if (!outUrl && !outB64) {
> 852	    // Text-only response = model treated the prompt as a text-generation
> 853	    // request (typical when prompt looks like an instruction). Pre-flight
> 854	    // guards catch the obvious cases; this is the runtime safety net.
> 855	    if (typeof message.content === "string" && message.content.trim().length > 0) {
> 856	      throw new Error(
> 857	        `O modelo respondeu com texto em vez de imagem (provável: prompt parece instrução). Reformule como descrição visual ou use o Magic Prompt. Prévia: ${message.content.slice(0, 150)}…`,
> 858	      );
> 859	    }
> 860	    throw new Error(`OpenRouter: resposta multimodal sem image_url. Response keys: ${Object.keys(data || {})}. Message keys: ${Object.keys(message || {})}. Raw response: ${JSON.stringify(data).slice(0, 400)}`);
> 861	  }
> 862	
> 863	  return { url: outUrl, b64: outB64 };
> 864	}
> 865	
> 866	async function generateHiggsfield(apiKey: string, apiSecret: string, body: ExecuteRequest) {
> 867	  if (!apiKey || !apiSecret) {
> 868	    throw new Error("Higgsfield credentials not configured (HIGGSFIELD_API_KEY / HIGGSFIELD_API_KEY_SECRET)");
> 869	  }
> 870	
> 871	  // Correct Higgsfield Platform API — base + auth + routes per the tested
> 872	  // viralmind integration (src/lib/higgsfield.server.ts). The previous
> 873	  // api.higgsfield.ai/v1/generations endpoint was wrong and never worked.
> 874	  const BASE_URL = "https://platform.higgsfield.ai";
> 875	  const authHeader = `Key ${apiKey}:${apiSecret}`;
> 876	  const POLL_INTERVAL_MS = 3000;
> 877	  const MAX_POLL_MS = 90_000;
> 878	
> 879	  // Derive Soul aspect ratio from incoming size / aspect_ratio params.
> 880	  // Canonical Higgsfield ARs (per /docs/guides/images): 16:9 · 9:16 · 1:1 · 4:5.
> 881	  const SIZE_TO_AR: Record<string, string> = {
> 882	    "1024x1024": "1:1",
> 883	    "1792x1024": "16:9",
> 884	    "1024x1792": "9:16",
> 885	    "1024x1280": "4:5",
> 886	    "1280x1024": "5:4",
> 887	  };
> 888	  const VALID_AR = new Set(["16:9", "9:16", "1:1", "4:5"]);
> 889	  const sizeKey = body.parameters?.size ? String(body.parameters.size) : "";
> 890	  const requestedAr = body.parameters?.aspect_ratio || SIZE_TO_AR[sizeKey] || "1:1";
> 891	  const aspectRatio = VALID_AR.has(requestedAr) ? requestedAr : "1:1";
> 892	  const resolution = body.parameters?.resolution === "720p" ? "720p" : "1080p";
> 893	
> 894	  // Video routes (DoP/Kling/Seedance) are handled by submitHiggsfieldVideo()
> 895	  // below — async path with `?hf_webhook=URL` query param. Soul (image) stays
> 896	  // sync because gens complete within the 90s edge function window.
> 897	
> 898	  // ── Submit Soul text-to-image job ──────────────────────────────────
> 899	  const isCompose = body.node_type === "scene_compose" || body.node_type === "compose";
> 900	  const endpoint = isCompose
> 901	    ? `${BASE_URL}/higgsfield-ai/soul/compose`
> 902	    : `${BASE_URL}/higgsfield-ai/soul/standard`;
> 903	
> 904	  const payload: Record<string, any> = {
> 905	    prompt: body.prompt,
> 906	    aspect_ratio: aspectRatio,
> 907	    resolution,
> 908	  };
> 909	
> 910	  if (isCompose) {
> 911	    // Cross-node consistency: explicit input_image_* wins; otherwise fall back to
> 912	    // upstream connected references so compose preserves identity automatically.
> 913	    const refs = (body.reference_image_urls ?? []).filter(Boolean);
> 914	    const image1 = body.input_image_1 || refs[0];
> 915	    const image2 = body.input_image_2 || refs[1];
> 916	    if (image1) {
> 917	      payload.image_1_url = image1;
> 918	      payload.input_image_1 = image1;
> 919	    }
> 920	    if (image2) {
> 921	      payload.image_2_url = image2;
> 922	      payload.input_image_2 = image2;
> 923	    }
> 924	    if (body.input_layout) {
> 925	      payload.layout_url = body.input_layout;
> 926	      payload.input_layout = body.input_layout;
> 927	    }
> 928	  }
> 929	
> 930	  const submitResp = await fetch(endpoint, {
> 931	    method: "POST",
> 932	    headers: {
> 933	      Authorization: authHeader,
> 934	      "Content-Type": "application/json",
> 935	      Accept: "application/json",
> 936	    },
> 937	    body: JSON.stringify(payload),
> 938	  });
> 939	
> 940	  if (!submitResp.ok) {
> 941	    const t = await submitResp.text();
> 942	    if (submitResp.status === 401 || submitResp.status === 403) {
> 943	      throw new Error("Higgsfield: credenciais inválidas");
> 944	    }
> 945	    if (submitResp.status === 402) {
> 946	      throw new Error("Higgsfield: saldo de créditos esgotado");
> 947	    }
> 948	    if (submitResp.status === 429) {
> 949	      throw new Error("Higgsfield: limite de requisições atingido");
> 950	    }
> 951	    throw new Error(`Higgsfield submit error ${submitResp.status}: ${t.slice(0, 200)}`);
> 952	  }
> 953	
> 954	  const submitData = await submitResp.json();
> 955	  const requestId = submitData.request_id || submitData.id;
> 956	  if (!requestId) throw new Error("Higgsfield: resposta de submit inválida (sem request_id)");
> 957	
> 958	  // ── Poll until terminal state ──────────────────────────────────────
> 959	  const started = Date.now();
> 960	  while (Date.now() - started < MAX_POLL_MS) {
> 961	    await new Promise((r) => setTimeout(r, POLL_INTERVAL_MS));
> 962	    const statusResp = await fetch(`${BASE_URL}/requests/${requestId}/status`, {
> 963	      method: "GET",
> 964	      headers: { Authorization: authHeader, Accept: "application/json" },
> 965	    });
> 966	    if (!statusResp.ok) {
> 967	      const t = await statusResp.text();
> 968	      throw new Error(`Higgsfield status error ${statusResp.status}: ${t.slice(0, 200)}`);
> 969	    }
> 970	    const statusData = await statusResp.json();
> 971	    if (statusData.status === "completed") {
> 972	      const url = statusData.images?.[0]?.url || statusData.video?.url || "";
> 973	      if (!url) throw new Error("Higgsfield: geração concluída sem URL de saída");
> 974	      return { url };
> 975	    }
> 976	    if (statusData.status === "failed") throw new Error("Higgsfield: a geração falhou no provedor");
> 977	    if (statusData.status === "nsfw") throw new Error("Higgsfield: conteúdo bloqueado por moderação");
> 978	    if (statusData.status === "cancelled") throw new Error("Higgsfield: geração cancelada");
> 979	  }
> 980	  throw new Error("Higgsfield: geração demorou demais (timeout >90s)");
> 981	}
> 982	
> 983	// ═══════════════════════════════════════════════════════════════════════════
> 984	// Phase 4.2c — Async video submit (image_to_video)
> 985	// ═══════════════════════════════════════════════════════════════════════════
> 986	// Fire-and-forget: POST Higgsfield with `?hf_webhook=<callback>`, capture
> 987	// `request_id`, UPDATE execution.operation_id, return 200 with status='queued'.
> 988	// `higgsfield-webhook` finalizes atomically (download → upload → deduct → asset row).
> 989	// Lei 1 trail: every gate inserts a row visible via REST (execution row, asset row,
> 990	// ledger row, infra_health_logs pulse).
> 991	// SOP: docs/processes/canvas-video-async-execution.md
> 992	// Validation doc: .claude/context/higgsfield-api-validation-2026-05-15.md
> 993	
> 994	interface SubmitVideoOpts {
> 995	  // eslint-disable-next-line @typescript-eslint/no-explicit-any
> 996	  admin: any; // SupabaseClient — looser type avoids createClient generic friction
> 997	  supabaseUrl: string;
> 998	  apiKey: string;
> 999	  apiSecret: string;
> 1000	  body: ExecuteRequest;
> 1001	  execution: { id: string; webhook_token: string; credits_charged: number };
> 1002	  corsHeaders: Record<string, string>;
> 1003	}
> 1004	
> 1005	async function submitHiggsfieldVideo(opts: SubmitVideoOpts): Promise<Response> {
> 1006	  const { admin, supabaseUrl, apiKey, apiSecret, body, execution, corsHeaders } = opts;
> 1007	
> 1008	  const fail = async (msg: string, httpStatus: number) => {
> 1009	    await admin
> 1010	      .from("vm_canvas_executions")
> 1011	      .update({
> 1012	        status: "failed",
> 1013	        error_message: msg,
> 1014	        completed_at: new Date().toISOString(),
> 1015	      })
> 1016	      .eq("id", execution.id);
> 1017	    await admin
> 1018	      .from("infra_health_logs")
> 1019	      .insert({ service: "canvas-execute", status: "unhealthy" })
> 1020	      .then(() => {}, (e: unknown) => console.error("[canvas-execute] health log failed:", e));
> 1021	    return new Response(
> 1022	      JSON.stringify({ error: msg, execution_id: execution.id, status: "failed" }),
> 1023	      { status: httpStatus, headers: { ...corsHeaders, "Content-Type": "application/json" } },
> 1024	    );
> 1025	  };
> 1026	
> 1027	  if (!apiKey || !apiSecret) {
> 1028	    return fail(
> 1029	      "Higgsfield credentials not configured (HIGGSFIELD_API_KEY / HIGGSFIELD_API_KEY_SECRET)",
> 1030	      500,
> 1031	    );
> 1032	  }
> 1033	
> 1034	  const imageUrl = body.input_asset_url;
> 1035	  if (!imageUrl) {
> 1036	    return fail(
> 1037	      "image_to_video requer input_asset_url (conecte uma imagem upstream antes de gerar)",
> 1038	      400,
> 1039	    );
> 1040	  }
> 1041	
> 1042	  const duration = typeof body.parameters?.duration === "number" ? body.parameters.duration : 5;
> 1043	  const motionStrength = typeof body.parameters?.motion_strength === "number"
> 1044	    ? body.parameters.motion_strength
> 1045	    : 0.5;
> 1046	
> 1047	  // Routing based on model parameter (aligned with .claude/context/higgsfield-api-validation-2026-05-15.md)
> 1048	  const BASE_URL = "https://platform.higgsfield.ai";
> 1049	  let modelPath = "higgsfield-ai/dop/standard";
> 1050	  if (body.model === "dop-lite") {
> 1051	    modelPath = "higgsfield-ai/dop/lite";
> 1052	  } else if (body.model === "dop-turbo") {
> 1053	    modelPath = "higgsfield-ai/dop/turbo";
> 1054	  } else if (body.model === "kling-2.1-pro") {
> 1055	    modelPath = "kling-video/v2.1/pro/image-to-video";
> 1056	  } else if (body.model === "seedance-v1-pro") {
> 1057	    modelPath = "bytedance/seedance/v1/pro/image-to-video";
> 1058	  }
> 1059	  const authHeader = `Key ${apiKey}:${apiSecret}`;
> 1060	
> 1061	  // Per-execution token guards against URL leak across rows (UNIQUE index on
> 1062	  // vm_canvas_executions.webhook_token). Higgsfield POSTs back with this token
> 1063	  // and the webhook idempotency check rejects replays via HTTP 409.
> 1064	  const webhookUrl = `${supabaseUrl}/functions/v1/higgsfield-webhook?token=${execution.webhook_token}`;
> 1065	
> 1066	  const submitUrl = new URL(`${BASE_URL}/${modelPath}`);
> 1067	  submitUrl.searchParams.set("hf_webhook", webhookUrl);
> 1068	
> 1069	  let submitResp: Response;
> 1070	  try {
> 1071	    submitResp = await fetch(submitUrl.toString(), {
> 1072	      method: "POST",
> 1073	      headers: {
> 1074	        Authorization: authHeader,
> 1075	        "Content-Type": "application/json",
> 1076	        Accept: "application/json",
> 1077	      },
> 1078	      body: JSON.stringify({
> 1079	        image_url: imageUrl,
> 1080	        prompt: body.prompt,
> 1081	        duration,
> 1082	        motion_strength: motionStrength,
> 1083	      }),
> 1084	    });
> 1085	  } catch (e) {
> 1086	    const msg = e instanceof Error ? e.message : "Higgsfield submit network error";
> 1087	    return fail(`Higgsfield submit network error: ${msg}`, 502);
> 1088	  }
> 1089	
> 1090	  if (!submitResp.ok) {
> 1091	    const text = await submitResp.text().catch(() => "");
> 1092	    let msg = `Higgsfield submit ${submitResp.status}: ${text.slice(0, 200)}`;
> 1093	    if (submitResp.status === 401 || submitResp.status === 403) {
> 1094	      msg = "Higgsfield: credenciais inválidas";
> 1095	    } else if (submitResp.status === 402) {
> 1096	      msg = "Higgsfield: saldo de créditos esgotado";
> 1097	    } else if (submitResp.status === 429) {
> 1098	      msg = "Higgsfield: limite de requisições atingido";
> 1099	    }
> 1100	    return fail(msg, 502);
> 1101	  }
> 1102	
> 1103	  let submitData: { request_id?: string; id?: string; status?: string };
> 1104	  try {
> 1105	    submitData = await submitResp.json();
> 1106	  } catch {
> 1107	    return fail("Higgsfield: resposta inválida (JSON parse failed)", 502);
> 1108	  }
> 1109	
> 1110	  const operationId = submitData.request_id ?? submitData.id;
> 1111	  if (!operationId) {
> 1112	    return fail("Higgsfield: resposta de submit sem request_id", 502);
> 1113	  }
> 1114	
> 1115	  const { error: updErr } = await admin
> 1116	    .from("vm_canvas_executions")
> 1117	    .update({ operation_id: operationId })
> 1118	    .eq("id", execution.id);
> 1119	  if (updErr) {
> 1120	    console.error("[canvas-execute] failed to persist operation_id:", updErr);
> 1121	    // The job is in-flight at Higgsfield but we lost the polling handle.
> 1122	    // Webhook will still finalize via webhook_token; watchdog poll falls back to noop.
> 1123	  }
> 1124	
> 1125	  await admin
> 1126	    .from("infra_health_logs")
> 1127	    .insert({ service: "canvas-execute", status: "healthy" })
> 1128	    .then(() => {}, (e: unknown) => console.error("[canvas-execute] health log failed:", e));
> 1129	
> 1130	  return new Response(
> 1131	    JSON.stringify({
> 1132	      execution_id: execution.id,
> 1133	      status: "queued",
> 1134	      webhook_token: execution.webhook_token,
> 1135	      operation_id: operationId,
> 1136	      credits_charged: execution.credits_charged, // intent, not yet deducted
> 1137	      higgsfield_status: submitData.status ?? "queued",
> 1138	    }),
> 1139	    { headers: { ...corsHeaders, "Content-Type": "application/json" } },
> 1140	  );
> 1141	}
> 1142	
> 1143	// ═══════════════════════════════════════════════════════════════════════════
> 1144	// Magic Prompt Enhancement (using OpenRouter Gemini 2.5 Flash)
> 1145	// ═══════════════════════════════════════════════════════════════════════════
> 1146	async function generateMagicPrompt(
> 1147	  apiKey: string,
> 1148	  geminiKey: string,
> 1149	  prompt: string,
> 1150	  level: "curto" | "medio" | "longo",
> 1151	  modelName: string,
> 1152	  campaignContext: string,
> 1153	) {
> 1154	  if (!apiKey) throw new Error("OpenRouter API key not configured");
> 1155	
> 1156	  const systemInstruction = `Você é o MCORCH Magic Prompt Engineer, um especialista em engenharia de prompt para modelos de IA generativa de imagem e vídeo (como Gemini 2.5 Flash, FLUX, Dall-E 3, e Higgsfield/Seedance).
> 1157	Seu objetivo é expandir e aprimorar o prompt genérico fornecido pelo usuário com base no contexto da campanha do usuário e no modelo de destino especificado.
> 1158	
> 1159	Nível de expansão solicitado:
> 1160	- curto: prompt conciso e direto, enriquecido (~25-40 palavras / máximo 400 caracteres).
> 1161	- medio: prompt moderadamente detalhado, focando em iluminação, composição e estilo (~60-90 palavras / máximo 900 caracteres).
> 1162	- longo: prompt altamente descritivo, cinemático e rico em detalhes visuais (~120-180 palavras / máximo 1500 caracteres — NUNCA exceda).
> 1163	
> 1164	Regras cruciais:
> 1165	1. Retorne APENAS o prompt final expandido em inglês (ideal para os geradores de imagem/vídeo).
> 1166	2. Não adicione observações, explicações, aspas extras ou introduções como "Here is your prompt:". Retorne apenas o texto do prompt.
> 1167	3. Se o modelo de destino for de vídeo (Higgsfield, Seedance, etc.), descreva o movimento da câmera, ações e efeitos temporais.
> 1168	4. Utilize o contexto da campanha (se fornecido) para alinhar o estilo do prompt com a marca/audiência.
> 1169	5. NUNCA inclua instruções de comportamento, definições de papel, ou estruturas de saída no output expandido. Proibido: "You are X", "Your function is Y", "Output ONLY", "IDENTITY & PROTOCOL CONTEXT", "Return only JSON", listas numeradas de regras, blocos de código. O output deve ser PURA DESCRIÇÃO VISUAL (substantivos + adjetivos + cenário + iluminação + estilo) — modelos de imagem leem qualquer estrutura instrucional como "gere texto" e devolvem texto em vez de imagem.`;
> 1170	
> 1171	  const userContent = `Prompt do usuário a ser expandido: "${prompt}"
> 1172	Modelo de destino: "${modelName}"
> 1173	Contexto de Campanha do Usuário:
> 1174	${campaignContext}`;
> 1175	
> 1176	  const resp = await fetchLLMWithFallback("https://openrouter.ai/api/v1/chat/completions", {
> 1177	    method: "POST",
> 1178	    headers: {
> 1179	      Authorization: `Bearer ${apiKey}`,
> 1180	      "Content-Type": "application/json",
> 1181	      "HTTP-Referer": "https://mcorch.com",
> 1182	      "X-Title": "GCRUX Magic Prompt Generator",
> 1183	    },
> 1184	    body: JSON.stringify({
> 1185	      model: "google/gemini-2.5-flash",
> 1186	      messages: [
> 1187	        { role: "system", content: systemInstruction },
> 1188	        { role: "user", content: userContent },
> 1189	      ],
> 1190	    }),
> 1191	  }, {
> 1192	    functionName: "canvas-execute",
> 1193	    openRouterKey: apiKey,
> 1194	    geminiKey,
> 1195	  });
> 1196	
> 1197	  if (!resp.ok) {
> 1198	    const t = await resp.text();
> 1199	    throw new Error(`OpenRouter error ${resp.status}: ${t.slice(0, 200)}`);
> 1200	  }
> 1201	
> 1202	  const data = await resp.json();
> 1203	  const text = data?.choices?.[0]?.message?.content?.trim() || "";
> 1204	  if (!text) throw new Error("OpenRouter: resposta de magic prompt vazia");
> 1205	
> 1206	  // Hard cap output so even an over-eager "longo" stays under the
> 1207	  // downstream image-gen guard. Trims at last sentence boundary when possible.
> 1208	  if (text.length > MAX_IMAGE_PROMPT_CHARS) {
> 1209	    const truncated = text.slice(0, MAX_IMAGE_PROMPT_CHARS);
> 1210	    const lastPeriod = truncated.lastIndexOf(". ");
> 1211	    return lastPeriod > MAX_IMAGE_PROMPT_CHARS * 0.6
> 1212	      ? truncated.slice(0, lastPeriod + 1).trim()
> 1213	      : truncated.trim();
> 1214	  }
> 1215	  return text;
> 1216	}
> 1217	
> ```

## 🤖 Claude *(18:41:40)*


## 🤖 Claude *(18:41:40)*

Now let me read the client-side callers and supporting files.

## 🤖 Claude *(18:41:41)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/lib/canvas-execute-result.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	/**
> 2	 * Shared helper to validate canvas-execute responses. The Edge Function
> 3	 * returns HTTP 200 even when the underlying provider fails (it logs the
> 4	 * error into `vm_canvas_executions.error_message` and returns a structured
> 5	 * body with `status: 'failed'` + `error: <msg>`). Inspectors must not
> 6	 * blindly treat the resolved mutation as success — they MUST inspect the
> 7	 * payload and re-throw on backend-reported failure.
> 8	 *
> 9	 * Root cause memory: smoke test 2026-05-17 — OpenRouter image endpoint
> 10	 * returned 404 HTML, backend correctly set status='failed' with
> 11	 * credits_charged=0, but inspector toast lied "Geração concluída".
> 12	 */
> 13	
> 14	export interface CanvasExecuteResult {
> 15	  execution_id?: string;
> 16	  status?: string;
> 17	  output_url?: string | null;
> 18	  asset_id?: string | null;
> 19	  credits_charged?: number;
> 20	  credits_remaining?: number;
> 21	  webhook_token?: string;
> 22	  operation_id?: string;
> 23	  error?: string;
> 24	}
> 25	
> 26	/**
> 27	 * Returns the result unchanged on success. Throws on backend-reported failure
> 28	 * so callers can use a single try/catch path. The thrown Error carries the
> 29	 * backend's pt-BR message verbatim — safe to surface via toast.
> 30	 */
> 31	export function assertExecuteSuccess<T extends CanvasExecuteResult | undefined | null>(
> 32	  result: T,
> 33	): T {
> 34	  if (!result) {
> 35	    throw new Error("canvas-execute retornou resposta vazia");
> 36	  }
> 37	  if (result.error) {
> 38	    throw new Error(result.error);
> 39	  }
> 40	  if (result.status === "failed" || result.status === "timeout" || result.status === "cancelled") {
> 41	    throw new Error(`Geração ${result.status}`);
> 42	  }
> 43	  return result;
> 44	}
> 45	
> ```

## 🤖 Claude *(18:41:41)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCanvasStudio.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
> 2	import { supabase } from "@/integrations/supabase/client";
> 3	import { useAuth } from "@/hooks/useAuth";
> 4	import type { CanvasGraph, PersistedCanvasGraph } from "@/types/canvas";
> 5	
> 6	export interface CanvasProject {
> 7	  id: string;
> 8	  user_id: string;
> 9	  name: string;
> 10	  description: string | null;
> 11	  thumbnail_url: string | null;
> 12	  graph: PersistedCanvasGraph;
> 13	  viewport: { x: number; y: number; zoom: number };
> 14	  status: string;
> 15	  total_executions: number;
> 16	  total_credits_used: number;
> 17	  last_execution_at: string | null;
> 18	  tags: string[];
> 19	  created_at: string;
> 20	  updated_at: string;
> 21	}
> 22	
> 23	export interface CanvasAsset {
> 24	  id: string;
> 25	  user_id: string;
> 26	  project_id: string | null;
> 27	  asset_type: string;
> 28	  public_url: string | null;
> 29	  provider: string | null;
> 30	  model_used: string | null;
> 31	  node_type: string | null;
> 32	  prompt: string | null;
> 33	  negative_prompt?: string | null;
> 34	  parameters?: Record<string, any> | null;
> 35	  credits_cost: number;
> 36	  created_at: string;
> 37	  node_id?: string | null;
> 38	  input_asset_id?: string | null;
> 39	}
> 40	
> 41	export interface CanvasExecution {
> 42	  id: string;
> 43	  project_id: string;
> 44	  node_id: string;
> 45	  node_type: string;
> 46	  provider: string;
> 47	  model: string;
> 48	  prompt: string | null;
> 49	  status: string;
> 50	  output_url: string | null;
> 51	  credits_charged: number;
> 52	  error_message: string | null;
> 53	  created_at: string;
> 54	}
> 55	
> 56	// ── Available providers and models for Canvas Studio ──────────────────
> 57	export const CANVAS_PROVIDERS = [
> 58	  {
> 59	    id: "openai",
> 60	    name: "OpenAI",
> 61	    models: [
> 62	      { id: "dall-e-3", name: "DALL·E 3", credits: 15, description: "High quality, creative" },
> 63	      { id: "gpt-image-1", name: "GPT Image 1", credits: 18, description: "Latest GPT-powered image gen" },
> 64	    ],
> 65	  },
> 66	  {
> 67	    id: "replicate",
> 68	    name: "Replicate",
> 69	    models: [
> 70	      { id: "flux-1.1-pro", name: "FLUX 1.1 Pro", credits: 12, description: "Best quality, photorealistic" },
> 71	      { id: "flux-schnell", name: "FLUX Schnell", credits: 3, description: "Fast, good quality" },
> 72	      { id: "sdxl", name: "Stable Diffusion XL", credits: 4, description: "Versatile, controllable" },
> 73	    ],
> 74	  },
> 75	  {
> 76	    id: "openrouter",
> 77	    name: "OpenRouter",
> 78	    models: [
> 79	      { id: "dall-e-3", name: "DALL·E 3 (via OR)", credits: 15, description: "Routed via OpenRouter" },
> 80	    ],
> 81	  },
> 82	  {
> 83	    id: "higgsfield",
> 84	    name: "Higgsfield",
> 85	    models: [
> 86	      { id: "generate", name: "Higgsfield Gen", credits: 20, description: "High-end generation" },
> 87	    ],
> 88	  },
> 89	] as const;
> 90	
> 91	// ── Projects CRUD ────────────────────────────────────────────────────
> 92	
> 93	export function useCanvasProjects() {
> 94	  const { user } = useAuth();
> 95	
> 96	  return useQuery({
> 97	    queryKey: ["vm-canvas-projects", user?.id],
> 98	    queryFn: async () => {
> 99	      if (!user) return [];
> 100	      const { data, error } = await supabase
> 101	        .from("vm_canvas_projects")
> 102	        .select("*")
> 103	        .eq("user_id", user.id)
> 104	        .eq("status", "active")
> 105	        .order("updated_at", { ascending: false });
> 106	      if (error) throw error;
> 107	      return (data || []) as CanvasProject[];
> 108	    },
> 109	    enabled: !!user,
> 110	  });
> 111	}
> 112	
> 113	export function useCanvasProject(projectId: string | undefined) {
> 114	  return useQuery({
> 115	    queryKey: ["vm-canvas-project", projectId],
> 116	    queryFn: async () => {
> 117	      if (!projectId) return null;
> 118	      const { data, error } = await supabase
> 119	        .from("vm_canvas_projects")
> 120	        .select("*")
> 121	        .eq("id", projectId)
> 122	        .single();
> 123	      if (error) throw error;
> 124	      return data as CanvasProject;
> 125	    },
> 126	    enabled: !!projectId,
> 127	  });
> 128	}
> 129	
> 130	export function useCreateCanvasProject() {
> 131	  const { user } = useAuth();
> 132	  const queryClient = useQueryClient();
> 133	
> 134	  return useMutation({
> 135	    mutationFn: async ({ name, description }: { name: string; description?: string }) => {
> 136	      if (!user) throw new Error("Not authenticated");
> 137	      const { data, error } = await supabase
> 138	        .from("vm_canvas_projects")
> 139	        .insert({ user_id: user.id, name, description })
> 140	        .select()
> 141	        .single();
> 142	      if (error) throw error;
> 143	      return data as CanvasProject;
> 144	    },
> 145	    onSuccess: () => {
> 146	      queryClient.invalidateQueries({ queryKey: ["vm-canvas-projects"] });
> 147	    },
> 148	  });
> 149	}
> 150	
> 151	export function useSaveCanvasGraph() {
> 152	  const queryClient = useQueryClient();
> 153	
> 154	  return useMutation({
> 155	    mutationFn: async ({ projectId, graph, viewport }: {
> 156	      projectId: string;
> 157	      graph: PersistedCanvasGraph;
> 158	      viewport?: { x: number; y: number; zoom: number };
> 159	    }) => {
> 160	      // Hydration-race guard (data-loss fix): NEVER overwrite a non-empty saved graph with an empty one.
> 161	      // useAutoSave can flush (debounce / pagehide / unmount) BEFORE initialize() hydrates the store, so the
> 162	      // empty boot state {nodes:[]} would clobber a rich DB row → all canvas nodes lost (assets survive in
> 163	      // vm_canvas_executions, which is why the project still shows assets but no nodes). When the incoming
> 164	      // graph is empty, read-before-write and skip the clobber (viewport-only updates still persist).
> 165	      if (graph.nodes.length === 0) {
> 166	        const { data: existing } = await supabase
> 167	          .from("vm_canvas_projects")
> 168	          .select("graph")
> 169	          .eq("id", projectId)
> 170	          .maybeSingle();
> 171	        const existingNodes = (existing?.graph as PersistedCanvasGraph | null)?.nodes ?? [];
> 172	        if (existingNodes.length > 0) {
> 173	          console.warn(
> 174	            `[saveCanvasGraph] blocked empty-graph overwrite of ${existingNodes.length}-node project ${projectId} (hydration race)`,
> 175	          );
> 176	          if (viewport) {
> 177	            await supabase.from("vm_canvas_projects").update({ viewport }).eq("id", projectId);
> 178	          }
> 179	          return;
> 180	        }
> 181	      }
> 182	
> 183	      const updateData: any = { graph };
> 184	      if (viewport) updateData.viewport = viewport;
> 185	
> 186	      const { error } = await supabase
> 187	        .from("vm_canvas_projects")
> 188	        .update(updateData)
> 189	        .eq("id", projectId);
> 190	      if (error) throw error;
> 191	    },
> 192	    onSuccess: (_, vars) => {
> 193	      queryClient.invalidateQueries({ queryKey: ["vm-canvas-project", vars.projectId] });
> 194	    },
> 195	  });
> 196	}
> 197	
> 198	export function useDeleteCanvasProject() {
> 199	  const queryClient = useQueryClient();
> 200	
> 201	  return useMutation({
> 202	    mutationFn: async (projectId: string) => {
> 203	      const { error } = await supabase
> 204	        .from("vm_canvas_projects")
> 205	        .update({ status: "archived" })
> 206	        .eq("id", projectId);
> 207	      if (error) throw error;
> 208	    },
> 209	    onSuccess: () => {
> 210	      queryClient.invalidateQueries({ queryKey: ["vm-canvas-projects"] });
> 211	    },
> 212	  });
> 213	}
> 214	
> 215	// ── Canvas Execute ───────────────────────────────────────────────────
> 216	
> 217	export function useCanvasExecute() {
> 218	  const queryClient = useQueryClient();
> 219	
> 220	  return useMutation({
> 221	    mutationFn: async (params: {
> 222	      project_id: string;
> 223	      node_id: string;
> 224	      node_type: string;
> 225	      provider: string;
> 226	      model: string;
> 227	      prompt: string;
> 228	      negative_prompt?: string;
> 229	      parameters?: Record<string, any>;
> 230	      /** Phase 4.2c — required for image_to_video (upstream image URL). */
> 231	      input_asset_url?: string;
> 232	      input_asset_id?: string;
> 233	      input_image_1?: string;
> 234	      input_image_2?: string;
> 235	      input_layout?: string;
> 236	      /** Phase 4.3 — cross-node consistency: upstream connected images as references. */
> 237	      reference_image_urls?: string[];
> 238	    }) => {
> 239	      const { data, error } = await supabase.functions.invoke("canvas-execute", { body: params });
> 240	      if (error) {
> 241	        let message = error.message;
> 242	        try {
> 243	          const ctx = (error as { context?: Response }).context;
> 244	          const parsed = ctx ? await ctx.json() : null;
> 245	          if (parsed?.error) message = parsed.error as string;
> 246	        } catch {
> 247	          // Fall back to original error message
> 248	        }
> 249	        throw new Error(message);
> 250	      }
> 251	      return data;
> 252	    },
> 253	    onSuccess: (_, vars) => {
> 254	      queryClient.invalidateQueries({ queryKey: ["vm-canvas-project", vars.project_id] });
> 255	      queryClient.invalidateQueries({ queryKey: ["vm-canvas-assets"] });
> 256	      queryClient.invalidateQueries({ queryKey: ["vm-canvas-executions"] });
> 257	    },
> 258	  });
> 259	}
> 260	
> 261	// ── Assets & Executions ──────────────────────────────────────────────
> 262	
> 263	export function useCanvasAssets(projectId?: string) {
> 264	  const { user } = useAuth();
> 265	
> 266	  return useQuery({
> 267	    queryKey: ["vm-canvas-assets", projectId, user?.id],
> 268	    queryFn: async () => {
> 269	      if (!user) return [];
> 270	      let query = supabase
> 271	        .from("vm_canvas_assets")
> 272	        .select("*")
> 273	        .eq("user_id", user.id)
> 274	        .order("created_at", { ascending: false })
> 275	        .limit(50);
> 276	
> 277	      if (projectId) query = query.eq("project_id", projectId);
> 278	
> 279	      const { data, error } = await query;
> 280	      if (error) throw error;
> 281	      return (data || []) as CanvasAsset[];
> 282	    },
> 283	    enabled: !!user,
> 284	  });
> 285	}
> 286	
> 287	export function useCanvasExecutions(projectId?: string) {
> 288	  const { user } = useAuth();
> 289	
> 290	  return useQuery({
> 291	    queryKey: ["vm-canvas-executions", projectId, user?.id],
> 292	    queryFn: async () => {
> 293	      if (!user) return [];
> 294	      let query = supabase
> 295	        .from("vm_canvas_executions")
> 296	        .select("*")
> 297	        .eq("user_id", user.id)
> 298	        .order("created_at", { ascending: false })
> 299	        .limit(30);
> 300	
> 301	      if (projectId) query = query.eq("project_id", projectId);
> 302	
> 303	      const { data, error } = await query;
> 304	      if (error) throw error;
> 305	      return (data || []) as CanvasExecution[];
> 306	    },
> 307	    enabled: !!user,
> 308	  });
> 309	}
> 310	
> 311	// ── Recipes ──────────────────────────────────────────────────────────
> 312	
> 313	export interface CanvasRecipe {
> 314	  id: string;
> 315	  user_id: string | null;
> 316	  name: string;
> 317	  description: string | null;
> 318	  thumbnail_url: string | null;
> 319	  graph: CanvasGraph;
> 320	  estimated_credits: number;
> 321	  category: string | null;
> 322	  tags: string[];
> 323	  is_public: boolean;
> 324	  is_official: boolean;
> 325	  uses_count: number;
> 326	  created_at: string;
> 327	}
> 328	
> 329	/** Public + own recipes. RLS gates the result to is_public OR auth.uid() = user_id. */
> 330	export function useCanvasRecipes() {
> 331	  return useQuery({
> 332	    queryKey: ["vm-canvas-recipes"],
> 333	    queryFn: async () => {
> 334	      const { data, error } = await supabase
> 335	        .from("vm_canvas_recipes")
> 336	        .select("*")
> 337	        .order("is_official", { ascending: false })
> 338	        .order("uses_count", { ascending: false });
> 339	      if (error) throw error;
> 340	      return (data || []) as CanvasRecipe[];
> 341	    },
> 342	    staleTime: 5 * 60 * 1000,
> 343	  });
> 344	}
> 345	
> 346	// ── Project metadata ─────────────────────────────────────────────────
> 347	
> 348	export function useUpdateCanvasProject() {
> 349	  const queryClient = useQueryClient();
> 350	
> 351	  return useMutation({
> 352	    mutationFn: async ({ projectId, name, description }: {
> 353	      projectId: string;
> 354	      name?: string;
> 355	      description?: string;
> 356	    }) => {
> 357	      const patch: Record<string, string> = {};
> 358	      if (name !== undefined) patch.name = name;
> 359	      if (description !== undefined) patch.description = description;
> 360	      const { error } = await supabase
> 361	        .from("vm_canvas_projects")
> 362	        .update(patch)
> 363	        .eq("id", projectId);
> 364	      if (error) throw error;
> 365	    },
> 366	    onSuccess: (_, vars) => {
> 367	      queryClient.invalidateQueries({ queryKey: ["vm-canvas-project", vars.projectId] });
> 368	      queryClient.invalidateQueries({ queryKey: ["vm-canvas-projects"] });
> 369	    },
> 370	  });
> 371	}
> 372	
> ```

## 🤖 Claude *(18:41:48)*


## 🤖 Claude *(18:41:50)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l /home/gcrUX/htdocs/constellation-orchestra/src/types/canvas.ts /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCanvasPipeline.ts /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/higgsfield-webhook/index.ts /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useParamRegistry.ts 2>/dev/null; ls /home/gcrUX/htdocs/constellation-orchestra/src/hooks/ | grep -iE \"canvasjobs|realtime|spaces\"",
  "description": "Check file sizes and find realtime/spaces hooks"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>   940 /home/gcrUX/htdocs/constellation-orchestra/src/types/canvas.ts
>   253 /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCanvasPipeline.ts
>   350 /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/higgsfield-webhook/index.ts
>    86 /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useParamRegistry.ts
>  1629 total
> useCanvasJobsRealtime.ts
> useSpaces.ts
> ```

## 🤖 Claude *(18:41:54)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/types/canvas.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	/**
> 2	 * Canvas Studio — type definitions (Phase 4.2a).
> 3	 *
> 4	 * Discriminated union por `kind` para os 5 tipos de nó portados do
> 5	 * viralmind-builder (GenerateImage · CharacterReference · SceneCompose ·
> 6	 * StyleTransfer · ImageToVideo), com catálogos `MODEL_INFO` /
> 7	 * `VIDEO_MODEL_INFO` populados pelo pricing canônico do Higgsfield
> 8	 * (.claude/context/higgsfield-api-validation-2026-05-15.md) + provedores
> 9	 * OpenAI / Replicate / OpenRouter já suportados pelo `canvas-execute`.
> 10	 *
> 11	 * Preserva as constantes de pipeline (LANE_HEIGHT, COL_WIDTH, STYLE_PRESETS,
> 12	 * DEFAULT_STYLE_SETTINGS, PersistedCanvasGraph) do Sprint 4.1 — viewport
> 13	 * fica em coluna própria, não no jsonb `graph`.
> 14	 */
> 15	import type { Node, Edge, Viewport } from "@xyflow/react";
> 16	
> 17	/* ── Node kind discrimination ────────────────────────────────────────── */
> 18	
> 19	export type CanvasNodeKind =
> 20	  | "generateImage"
> 21	  | "characterReference"
> 22	  | "sceneCompose"
> 23	  | "styleTransfer"
> 24	  | "imageToVideo"
> 25	  | "voiceClone"
> 26	  | "avatarIdentity";
> 27	
> 28	export type NodeStatus =
> 29	  | "idle"
> 30	  | "queued"
> 31	  | "running"
> 32	  | "success"
> 33	  | "failed"
> 34	  | "cancelled";
> 35	
> 36	/* ── Provider catalog ────────────────────────────────────────────────── */
> 37	
> 38	export type ProviderId = "higgsfield" | "openai" | "replicate" | "openrouter";
> 39	
> 40	export type AspectRatio =
> 41	  | "1:1"
> 42	  | "9:16"
> 43	  | "16:9"
> 44	  | "4:5"
> 45	  | "3:4"
> 46	  | "custom";
> 47	
> 48	/**
> 49	 * Image model identifier — union of all models exposed in the Canvas
> 50	 * studio catalog. Higgsfield Soul entries encode resolution × batch in
> 51	 * the suffix; canvas-execute resolves these to the canonical tier key
> 52	 * `higgsfield/soul-<res>-<batch>` (see CREDIT_COSTS in canvas-execute).
> 53	 */
> 54	export type ImageModelId =
> 55	  // Higgsfield Soul (text-to-image)
> 56	  | "soul-720p-x1"
> 57	  | "soul-720p-x4"
> 58	  | "soul-1080p-x1"
> 59	  | "soul-1080p-x4"
> 60	  // OpenAI
> 61	  | "dall-e-3"
> 62	  | "gpt-image-1"
> 63	  // Replicate
> 64	  | "flux-1.1-pro"
> 65	  | "flux-schnell"
> 66	  | "sdxl"
> 67	  // OpenRouter (chat-completions multimodal — Round 3 hotfix 2026-05-17)
> 68	  | "openrouter-gemini-image"
> 69	  | "openrouter-flux-pro"
> 70	  // Legacy — kept in union for saved-state compat; UI banner steers users to the new entries.
> 71	  | "openrouter-dall-e-3";
> 72	
> 73	export interface ImageModelInfo {
> 74	  label: string;
> 75	  provider: ProviderId;
> 76	  /** Model name passed to canvas-execute (`body.model`). */
> 77	  modelParam: string;
> 78	  tier: "Premium" | "Padrão" | "Rápido" | "Validação";
> 79	  /** mcoCoins debitados na conta MCORCH. */
> 80	  coinCost: number;
> 81	  /** Créditos Higgsfield reais consumidos da conta paga (se aplicável). */
> 82	  higgsfieldCost?: number;
> 83	  /** ETA estimado para a geração. */
> 84	  eta: string;
> 85	  /** Soul-only: resolução nativa (sent via parameters.resolution). */
> 86	  resolution?: "720p" | "1080p";
> 87	  /** Soul-only: batch size (sent via parameters.batch). */
> 88	  batch?: 1 | 4;
> 89	}
> 90	
> 91	/**
> 92	 * Catálogo central de modelos image-to-text. Pricing Soul vem da
> 93	 * validação canônica (commit 076f6b8 / docs/higgsfield-api-validation).
> 94	 * `coinCost` ≈ ~13× o USD cost (margem MCORCH).
> 95	 */
> 96	export const MODEL_INFO: Record<ImageModelId, ImageModelInfo> = {
> 97	  "soul-720p-x1": {
> 98	    label: "Soul · 720p · 1 imagem",
> 99	    provider: "higgsfield",
> 100	    modelParam: "soul",
> 101	    tier: "Validação",
> 102	    coinCost: 20,
> 103	    higgsfieldCost: 1.5,
> 104	    eta: "4–8s",
> 105	    resolution: "720p",
> 106	    batch: 1,
> 107	  },
> 108	  "soul-720p-x4": {
> 109	    label: "Soul · 720p · 4 imagens (mood board)",
> 110	    provider: "higgsfield",
> 111	    modelParam: "soul",
> 112	    tier: "Padrão",
> 113	    coinCost: 26,
> 114	    higgsfieldCost: 2,
> 115	    eta: "8–14s",
> 116	    resolution: "720p",
> 117	    batch: 4,
> 118	  },
> 119	  "soul-1080p-x1": {
> 120	    label: "Soul · 1080p · 1 imagem",
> 121	    provider: "higgsfield",
> 122	    modelParam: "soul",
> 123	    tier: "Premium",
> 124	    coinCost: 40,
> 125	    higgsfieldCost: 3,
> 126	    eta: "6–12s",
> 127	    resolution: "1080p",
> 128	    batch: 1,
> 129	  },
> 130	  "soul-1080p-x4": {
> 131	    label: "Soul · 1080p · 4 imagens",
> 132	    provider: "higgsfield",
> 133	    modelParam: "soul",
> 134	    tier: "Premium",
> 135	    coinCost: 65,
> 136	    higgsfieldCost: 5,
> 137	    eta: "12–20s",
> 138	    resolution: "1080p",
> 139	    batch: 4,
> 140	  },
> 141	  "dall-e-3": {
> 142	    label: "DALL·E 3",
> 143	    provider: "openai",
> 144	    modelParam: "dall-e-3",
> 145	    tier: "Premium",
> 146	    coinCost: 15,
> 147	    eta: "10–15s",
> 148	  },
> 149	  "gpt-image-1": {
> 150	    label: "GPT Image 1",
> 151	    provider: "openai",
> 152	    modelParam: "gpt-image-1",
> 153	    tier: "Premium",
> 154	    coinCost: 18,
> 155	    eta: "12–20s",
> 156	  },
> 157	  "flux-1.1-pro": {
> 158	    label: "FLUX 1.1 Pro",
> 159	    provider: "replicate",
> 160	    modelParam: "flux-1.1-pro",
> 161	    tier: "Premium",
> 162	    coinCost: 12,
> 163	    eta: "8–15s",
> 164	  },
> 165	  "flux-schnell": {
> 166	    label: "FLUX Schnell",
> 167	    provider: "replicate",
> 168	    modelParam: "flux-schnell",
> 169	    tier: "Rápido",
> 170	    coinCost: 3,
> 171	    eta: "3–5s",
> 172	  },
> 173	  sdxl: {
> 174	    label: "SDXL",
> 175	    provider: "replicate",
> 176	    modelParam: "sdxl",
> 177	    tier: "Padrão",
> 178	    coinCost: 4,
> 179	    eta: "5–8s",
> 180	  },
> 181	  "openrouter-gemini-image": {
> 182	    label: "Nano Banana 2 (Gemini)",
> 183	    provider: "openrouter",
> 184	    modelParam: "google/gemini-2.5-flash-image",
> 185	    tier: "Rápido",
> 186	    coinCost: 10,
> 187	    eta: "4–8s",
> 188	  },
> 189	  "openrouter-flux-pro": {
> 190	    label: "FLUX 1.1 Pro (OpenRouter)",
> 191	    provider: "openrouter",
> 192	    modelParam: "black-forest-labs/flux-1.1-pro",
> 193	    tier: "Premium",
> 194	    coinCost: 12,
> 195	    eta: "8–15s",
> 196	  },
> 197	  "openrouter-dall-e-3": {
> 198	    label: "DALL·E 3 (OpenRouter — deprecado)",
> 199	    provider: "openrouter",
> 200	    modelParam: "dall-e-3",
> 201	    tier: "Premium",
> 202	    coinCost: 15,
> 203	    eta: "10–15s",
> 204	  },
> 205	};
> 206	
> 207	export const DEFAULT_IMAGE_MODEL: ImageModelId = "openrouter-gemini-image";
> 208	
> 209	/* ── Video models (Phase 4.2b will wire async pipeline) ──────────────── */
> 210	
> 211	export type VideoModelId =
> 212	  | "dop-lite-5s"
> 213	  | "dop-turbo-5s"
> 214	  | "dop-standard-5s"
> 215	  | "kling-2.1-pro-5s"
> 216	  | "seedance-v1-pro-5s";
> 217	
> 218	export type VideoAspectRatio = "9:16" | "16:9" | "1:1";
> 219	export type VideoDuration = 5 | 10 | 15;
> 220	
> 221	export interface VideoModelInfo {
> 222	  label: string;
> 223	  provider: ProviderId;
> 224	  modelParam: string;
> 225	  tier: "Premium" | "Padrão" | "Rápido";
> 226	  coinCost: number;
> 227	  higgsfieldCost?: number;
> 228	  eta: string;
> 229	  /** Phase 4.2b will switch ImageToVideo from sync poll to async webhook. */
> 230	  asyncOnly?: boolean;
> 231	}
> 232	
> 233	export const VIDEO_MODEL_INFO: Record<VideoModelId, VideoModelInfo> = {
> 234	  "dop-lite-5s": {
> 235	    label: "DoP Lite · 5s",
> 236	    provider: "higgsfield",
> 237	    modelParam: "dop-lite",
> 238	    tier: "Rápido",
> 239	    coinCost: 30,
> 240	    higgsfieldCost: 2,
> 241	    eta: "20–40s",
> 242	  },
> 243	  "dop-turbo-5s": {
> 244	    label: "DoP Turbo · 5s",
> 245	    provider: "higgsfield",
> 246	    modelParam: "dop-turbo",
> 247	    tier: "Padrão",
> 248	    coinCost: 90,
> 249	    higgsfieldCost: 6.5,
> 250	    eta: "15–30s (fila prioritária)",
> 251	  },
> 252	  "dop-standard-5s": {
> 253	    label: "DoP Standard · 5s",
> 254	    provider: "higgsfield",
> 255	    modelParam: "dop-standard",
> 256	    tier: "Premium",
> 257	    coinCost: 125,
> 258	    higgsfieldCost: 9,
> 259	    eta: "30–60s (qualidade máxima)",
> 260	    asyncOnly: true,
> 261	  },
> 262	  "kling-2.1-pro-5s": {
> 263	    label: "Kling 2.1 Pro · 5s",
> 264	    provider: "higgsfield",
> 265	    modelParam: "kling-2.1-pro",
> 266	    tier: "Premium",
> 267	    coinCost: 160,
> 268	    higgsfieldCost: 12,
> 269	    eta: "60–120s (cinematográfico)",
> 270	    asyncOnly: true,
> 271	  },
> 272	  "seedance-v1-pro-5s": {
> 273	    label: "Seedance v1 Pro · 5s",
> 274	    provider: "higgsfield",
> 275	    modelParam: "seedance-v1-pro",
> 276	    tier: "Premium",
> 277	    coinCost: 130,
> 278	    higgsfieldCost: 9,
> 279	    eta: "40–80s",
> 280	    asyncOnly: true,
> 281	  },
> 282	};
> 283	
> 284	export const DEFAULT_VIDEO_MODEL: VideoModelId = "dop-standard-5s";
> 285	
> 286	/* ── Safe catalog lookups (NEVER white-screen on an unknown modelId) ──────
> 287	 * A project can be saved/recovered with a modelId that isn't a catalog key —
> 288	 * e.g. a graph rebuilt from vm_canvas_executions stores the RAW execution model
> 289	 * ("google/gemini-2.5-flash-image", "dop-standard") instead of the UI key
> 290	 * ("openrouter-gemini-image", "dop-standard-5s"). Direct `MODEL_INFO[id].coinCost`
> 291	 * then throws "Cannot read properties of undefined", which crashed the ENTIRE
> 292	 * editor (white page + only the footer). These accessors degrade gracefully so a
> 293	 * stale/foreign modelId renders a neutral node instead of taking down the page. */
> 294	const FALLBACK_IMAGE_MODEL_INFO: ImageModelInfo = {
> 295	  label: "Modelo fora do catálogo",
> 296	  provider: "openrouter",
> 297	  modelParam: "",
> 298	  tier: "Padrão",
> 299	  coinCost: 0,
> 300	  eta: "—",
> 301	};
> 302	const FALLBACK_VIDEO_MODEL_INFO: VideoModelInfo = {
> 303	  label: "Modelo de vídeo fora do catálogo",
> 304	  provider: "higgsfield",
> 305	  modelParam: "",
> 306	  tier: "Padrão",
> 307	  coinCost: 0,
> 308	  eta: "—",
> 309	};
> 310	
> 311	export function getImageModelInfo(id: string | null | undefined): ImageModelInfo {
> 312	  return (id != null && MODEL_INFO[id as ImageModelId]) || FALLBACK_IMAGE_MODEL_INFO;
> 313	}
> 314	export function getVideoModelInfo(id: string | null | undefined): VideoModelInfo {
> 315	  return (id != null && VIDEO_MODEL_INFO[id as VideoModelId]) || FALLBACK_VIDEO_MODEL_INFO;
> 316	}
> 317	
> 318	/* ── Aspect ratios + controls ────────────────────────────────────────── */
> 319	
> 320	export const ASPECT_RATIOS: { id: AspectRatio; label: string; w: number; h: number }[] = [
> 321	  { id: "1:1", label: "Quadrado (Feed)", w: 1, h: 1 },
> 322	  { id: "9:16", label: "Vertical (Reels/Stories)", w: 9, h: 16 },
> 323	  { id: "16:9", label: "Horizontal (YT)", w: 16, h: 9 },
> 324	  { id: "4:5", label: "Feed alto", w: 4, h: 5 },
> 325	  { id: "3:4", label: "Retrato", w: 3, h: 4 },
> 326	  { id: "custom", label: "Custom", w: 1, h: 1 },
> 327	];
> 328	
> 329	export interface ControlValues {
> 330	  creativity: number;
> 331	  resemblance: number;
> 332	  hdr: number;
> 333	  fractality: number;
> 334	  sharpness: number;
> 335	}
> 336	
> 337	export const DEFAULT_CONTROLS: ControlValues = {
> 338	  creativity: 0.7,
> 339	  resemblance: 0.3,
> 340	  hdr: 0.5,
> 341	  fractality: 0.3,
> 342	  sharpness: 0.8,
> 343	};
> 344	
> 345	/* ── Style Transfer presets (8 — viralmind C3) ───────────────────────── */
> 346	
> 347	export const STYLE_TRANSFER_PRESETS = [
> 348	  { id: "cinematic", label: "Cinematográfico", suffix: "cinematic film still, anamorphic lens, dramatic lighting, 35mm film grain, shallow depth of field" },
> 349	  { id: "neon", label: "Neon", suffix: "neon-soaked cyberpunk aesthetic, vibrant magenta and cyan rim light, wet streets, high contrast" },
> 350	  { id: "analog", label: "Analógico", suffix: "analog film photograph, kodak portra 400, soft grain, warm tones, slight light leak" },
> 351	  { id: "minimal", label: "Minimalista", suffix: "minimalist composition, negative space, muted palette, clean geometry, soft natural light" },
> 352	  { id: "noir", label: "Noir", suffix: "film noir, high contrast black and white, hard shadows, venetian blind light, moody atmosphere" },
> 353	  { id: "anime", label: "Anime", suffix: "modern anime illustration, cel shading, expressive line art, vibrant colors, ghibli-inspired" },
> 354	  { id: "vaporwave", label: "Vaporwave", suffix: "vaporwave aesthetic, pastel pink and teal gradient, retro 80s, glitch artifacts, chrome surfaces" },
> 355	  { id: "documentary", label: "Documentário", suffix: "documentary photography, natural light, candid moment, photojournalistic, Magnum-style" },
> 356	] as const;
> 357	
> 358	export type StyleTransferPresetId = (typeof STYLE_TRANSFER_PRESETS)[number]["id"];
> 359	
> 360	export const STYLE_TRANSFER_COST = 14;
> 361	
> 362	/* ── Typed node data shapes ──────────────────────────────────────────── */
> 363	
> 364	export interface GenerateImageData {
> 365	  kind: "generateImage";
> 366	  label: string;
> 367	  modelId: ImageModelId;
> 368	  prompt: string;
> 369	  negativePrompt: string;
> 370	  aspectRatio: AspectRatio;
> 371	  controls: ControlValues;
> 372	  seed: number | null;
> 373	  fixedSeed: boolean;
> 374	  status: NodeStatus;
> 375	  inheritStyle?: boolean;
> 376	  output?: {
> 377	    imageUrl?: string;
> 378	    storagePath?: string;
> 379	    imageDataUrl?: string;
> 380	    generatedAt: string;
> 381	  };
> 382	  error?: string;
> 383	}
> 384	
> 385	export interface CharacterReferenceData {
> 386	  kind: "characterReference";
> 387	  label: string;
> 388	  characterName: string;
> 389	  /** Primary photo = imageUrls[0] (back-compat: legacy single-photo nodes set only this). */
> 390	  imageUrl?: string;
> 391	  storagePath?: string;
> 392	  /** Mood board — múltiplas fotos do MESMO rosto (ângulos diferentes). Todas viram referência facial
> 393	   *  downstream (findUpstreamImages coleta todas; o modelo usa até 4 — limite de consistência do Gemini). */
> 394	  imageUrls?: string[];
> 395	  storagePaths?: string[];
> 396	  /** Higgsfield Soul Character id (Phase 4.5 — registro real). */
> 397	  soulId?: string;
> 398	  soulIdStatus?: "idle" | "registering" | "ready" | "failed";
> 399	  soulIdError?: string;
> 400	  status: NodeStatus;
> 401	  error?: string;
> 402	}
> 403	
> 404	export interface SceneComposeData {
> 405	  kind: "sceneCompose";
> 406	  label: string;
> 407	  prompt: string;
> 408	  aspectRatio: AspectRatio;
> 409	  modelId: ImageModelId;
> 410	  /** mcoCoins estimados — derivado de MODEL_INFO[modelId]. */
> 411	  cost: number;
> 412	  status: NodeStatus;
> 413	  inheritStyle?: boolean;
> 414	  /** Smart Inheritance — id do nó characterReference upstream. */
> 415	  characterRefId?: string;
> 416	  output?: {
> 417	    imageUrl?: string;
> 418	    storagePath?: string;
> 419	    generatedAt: string;
> 420	  };
> 421	  error?: string;
> 422	}
> 423	
> 424	export interface StyleTransferData {
> 425	  kind: "styleTransfer";
> 426	  label: string;
> 427	  strength: number;
> 428	  cost: number;
> 429	  presetId: StyleTransferPresetId;
> 430	  status: NodeStatus;
> 431	  characterRefId?: string;
> 432	  output?: {
> 433	    imageUrl?: string;
> 434	    storagePath?: string;
> 435	    generatedAt: string;
> 436	  };
> 437	  error?: string;
> 438	}
> 439	
> 440	export interface ImageToVideoData {
> 441	  kind: "imageToVideo";
> 442	  label: string;
> 443	  prompt: string;
> 444	  duration: VideoDuration;
> 445	  aspectRatio: VideoAspectRatio;
> 446	  videoModel: VideoModelId;
> 447	  motionStrength: number;
> 448	  status: NodeStatus;
> 449	  characterRefId?: string;
> 450	  /** Phase 4.2b — populated by submit; webhook updates result. */
> 451	  higgsfieldRequestId?: string;
> 452	  output?: {
> 453	    videoUrl?: string;
> 454	    storagePath?: string;
> 455	    generatedAt: string;
> 456	  };
> 457	  error?: string;
> 458	}
> 459	
> 460	/**
> 461	 * avatar-clone-ai Fatia 2 — voiceClone node (FR-AC-008/009/010/011).
> 462	 * Clones a reference voice (ElevenLabs IVC / Cartesia) then synthesizes a script with it.
> 463	 * Runs against the net-new `generate-voice` Edge Function (NOT canvas-execute).
> 464	 */
> 465	export interface VoiceCloneData {
> 466	  kind: "voiceClone";
> 467	  label: string;
> 468	  /** Provider for both the clone and the synthesis (BYOK per-user). */
> 469	  provider: "elevenlabs" | "cartesia";
> 470	  /** Single language per generation — never code-switch intra-sentence (FM-AC-013). */
> 471	  language: "en" | "pt-BR";
> 472	  /** Uploaded reference-audio sample used to clone the voice. */
> 473	  sampleAudioUrl?: string;
> 474	  sampleStoragePath?: string;
> 475	  /** voice_profiles row id — set after a successful clone; required to synthesize. */
> 476	  voiceProfileId?: string;
> 477	  /** Text to synthesize with the cloned voice. */
> 478	  prompt: string;
> 479	  status: NodeStatus;
> 480	  output?: {
> 481	    audioUrl?: string;
> 482	    creativeAssetId?: string;
> 483	    generatedAt: string;
> 484	  };
> 485	  error?: string;
> 486	}
> 487	
> 488	/**
> 489	 * avatar-clone-ai Fatia 3b — avatarIdentity node (FR-AC-012).
> 490	 * Holds a consented reference-portrait set + the trained identity profile. Trains against the
> 491	 * net-new `avatar-identity-train` Edge Function (gated OTD-AC-017) — NOT canvas-execute. The
> 492	 * Identity Gate runs the VLM-soft compare (FR-AC-013b, src/lib/avatar-identity.ts) post-generation.
> 493	 */
> 494	export interface AvatarIdentityData {
> 495	  kind: "avatarIdentity";
> 496	  label: string;
> 497	  /** self_clone (titular cloning themselves) drives the FR-AC-032 verification + compliance template. */
> 498	  personaType: "self_clone" | "fictional";
> 499	  /** Identity ladder tier (1 InstantID/IP-Adapter · 2 PuLID-Flux · 3 LoRA per-person). */
> 500	  tier: 1 | 2 | 3;
> 501	  provider: "higgsfield" | "lora_flux";
> 502	  /** Identity Gate mode — VLM-soft MVP default (FR-AC-013/014); arcface deferred OTD-AC-015. */
> 503	  gateMode: "vlm_soft" | "arcface";
> 504	  /** Uploaded reference-portrait signed URLs (≥20 recommended for Soul ID). */
> 505	  referenceUrls: string[];
> 506	  referenceStoragePaths?: string[];
> 507	  /** avatar_identities row id — set after a successful train (gated OTD-AC-017). */
> 508	  avatarIdentityId?: string;
> 509	  status: NodeStatus;
> 510	  output?: {
> 511	    /** last generated frame URL that ran through the Identity Gate */
> 512	    frameUrl?: string;
> 513	    softMatch?: "pass" | "review" | "fail";
> 514	    generatedAt: string;
> 515	  };
> 516	  error?: string;
> 517	}
> 518	
> 519	export type CanvasNodeData =
> 520	  | GenerateImageData
> 521	  | CharacterReferenceData
> 522	  | SceneComposeData
> 523	  | StyleTransferData
> 524	  | ImageToVideoData
> 525	  | VoiceCloneData
> 526	  | AvatarIdentityData;
> 527	
> 528	export type CanvasNode = Node<CanvasNodeData, CanvasNodeKind>;
> 529	export type CanvasEdge = Edge;
> 530	
> 531	export interface CanvasGraph {
> 532	  nodes: CanvasNode[];
> 533	  edges: CanvasEdge[];
> 534	}
> 535	
> 536	export const EMPTY_GRAPH: CanvasGraph = { nodes: [], edges: [] };
> 537	
> 538	/* ── Pipeline mode (Sprint 4.1 — preserved) ──────────────────────────── */
> 539	
> 540	export const LANE_HEIGHT = 320;
> 541	export const COL_WIDTH = 320;
> 542	export const MIN_LANES = 4;
> 543	
> 544	export interface LaneConfig {
> 545	  id: string;
> 546	  label: string;
> 547	}
> 548	
> 549	export function makeLane(label = "Nova lane"): LaneConfig {
> 550	  return { id: `lane_${Math.random().toString(36).slice(2, 10)}`, label };
> 551	}
> 552	
> 553	export function laneIndexFromY(y: number): number {
> 554	  return Math.max(0, Math.floor(y / LANE_HEIGHT));
> 555	}
> 556	
> 557	export const STYLE_PRESETS = [
> 558	  { id: "none", label: "Sem preset" },
> 559	  { id: "cinematic", label: "Cinematográfico" },
> 560	  { id: "photorealistic", label: "Fotorrealista" },
> 561	  { id: "anime", label: "Anime" },
> 562	  { id: "illustration", label: "Ilustração" },
> 563	  { id: "noir", label: "Noir" },
> 564	  { id: "documentary", label: "Documentário" },
> 565	] as const;
> 566	
> 567	export type StylePresetId = (typeof STYLE_PRESETS)[number]["id"];
> 568	
> 569	export interface StyleSettings {
> 570	  palette: string[];
> 571	  mood: string;
> 572	  stylePreset: StylePresetId;
> 573	}
> 574	
> 575	export const DEFAULT_STYLE_SETTINGS: StyleSettings = {
> 576	  palette: [],
> 577	  mood: "",
> 578	  stylePreset: "none",
> 579	};
> 580	
> 581	/* ── Persisted graph blob (Sprint 4.1 — preserved) ───────────────────── */
> 582	
> 583	export interface PersistedCanvasGraph extends CanvasGraph {
> 584	  pipelineMode?: boolean;
> 585	  lanes?: LaneConfig[];
> 586	  styleSettings?: StyleSettings;
> 587	}
> 588	
> 589	export interface CanvasInitPayload extends PersistedCanvasGraph {
> 590	  viewport?: Viewport;
> 591	}
> 592	
> 593	/* ── Factories ──────────────────────────────────────────────────────── */
> 594	
> 595	function makeNodeId(): string {
> 596	  return `n_${Math.random().toString(36).slice(2, 10)}`;
> 597	}
> 598	
> 599	export function makeDefaultGenerateImage(
> 600	  position: { x: number; y: number },
> 601	  overrides: Partial<GenerateImageData> = {},
> 602	): CanvasNode {
> 603	  return {
> 604	    id: makeNodeId(),
> 605	    type: "generateImage",
> 606	    position,
> 607	    data: {
> 608	      kind: "generateImage",
> 609	      label: "Gerar Imagem",
> 610	      modelId: DEFAULT_IMAGE_MODEL,
> 611	      prompt: "",
> 612	      negativePrompt: "",
> 613	      aspectRatio: "9:16",
> 614	      controls: { ...DEFAULT_CONTROLS },
> 615	      seed: null,
> 616	      fixedSeed: false,
> 617	      status: "idle",
> 618	      inheritStyle: true,
> 619	      ...overrides,
> 620	    },
> 621	  };
> 622	}
> 623	
> 624	export function makeDefaultCharacterReference(
> 625	  position: { x: number; y: number },
> 626	  overrides: Partial<CharacterReferenceData> = {},
> 627	): CanvasNode {
> 628	  return {
> 629	    id: makeNodeId(),
> 630	    type: "characterReference",
> 631	    position,
> 632	    data: {
> 633	      kind: "characterReference",
> 634	      label: "Personagem",
> 635	      characterName: "",
> 636	      status: "idle",
> 637	      ...overrides,
> 638	    },
> 639	  };
> 640	}
> 641	
> 642	export function makeDefaultSceneCompose(
> 643	  position: { x: number; y: number },
> 644	  overrides: Partial<SceneComposeData> = {},
> 645	): CanvasNode {
> 646	  const modelId = overrides.modelId ?? "openrouter-gemini-image";
> 647	  return {
> 648	    id: makeNodeId(),
> 649	    type: "sceneCompose",
> 650	    position,
> 651	    data: {
> 652	      kind: "sceneCompose",
> 653	      label: "Compor Cena",
> 654	      prompt: "",
> 655	      aspectRatio: "9:16",
> 656	      modelId,
> 657	      cost: 18,
> 658	      status: "idle",
> 659	      inheritStyle: true,
> 660	      ...overrides,
> 661	    },
> 662	  };
> 663	}
> 664	
> 665	export function makeDefaultStyleTransfer(
> 666	  position: { x: number; y: number },
> 667	  overrides: Partial<StyleTransferData> = {},
> 668	): CanvasNode {
> 669	  return {
> 670	    id: makeNodeId(),
> 671	    type: "styleTransfer",
> 672	    position,
> 673	    data: {
> 674	      kind: "styleTransfer",
> 675	      label: "Estilizar",
> 676	      strength: 0.65,
> 677	      cost: STYLE_TRANSFER_COST,
> 678	      presetId: "cinematic",
> 679	      status: "idle",
> 680	      ...overrides,
> 681	    },
> 682	  };
> 683	}
> 684	
> 685	export function makeDefaultImageToVideo(
> 686	  position: { x: number; y: number },
> 687	  overrides: Partial<ImageToVideoData> = {},
> 688	): CanvasNode {
> 689	  return {
> 690	    id: makeNodeId(),
> 691	    type: "imageToVideo",
> 692	    position,
> 693	    data: {
> 694	      kind: "imageToVideo",
> 695	      label: "Imagem → Vídeo",
> 696	      prompt: "",
> 697	      duration: 5,
> 698	      aspectRatio: "9:16",
> 699	      videoModel: DEFAULT_VIDEO_MODEL,
> 700	      motionStrength: 0.5,
> 701	      status: "idle",
> 702	      ...overrides,
> 703	    },
> 704	  };
> 705	}
> 706	
> 707	/** avatar-clone-ai Fatia 2 — voiceClone node default (global EN-first per the BoK decisions). */
> 708	export function makeDefaultVoiceClone(
> 709	  position: { x: number; y: number },
> 710	  overrides: Partial<VoiceCloneData> = {},
> 711	): CanvasNode {
> 712	  return {
> 713	    id: makeNodeId(),
> 714	    type: "voiceClone",
> 715	    position,
> 716	    data: {
> 717	      kind: "voiceClone",
> 718	      label: "Clone de Voz",
> 719	      provider: "elevenlabs",
> 720	      language: "en",
> 721	      prompt: "",
> 722	      status: "idle",
> 723	      ...overrides,
> 724	    },
> 725	  };
> 726	}
> 727	
> 728	/** avatar-clone-ai Fatia 3b — avatarIdentity node default (FR-AC-012). */
> 729	export function makeDefaultAvatarIdentity(
> 730	  position: { x: number; y: number },
> 731	  overrides: Partial<AvatarIdentityData> = {},
> 732	): CanvasNode {
> 733	  return {
> 734	    id: makeNodeId(),
> 735	    type: "avatarIdentity",
> 736	    position,
> 737	    data: {
> 738	      kind: "avatarIdentity",
> 739	      label: "Identidade (avatar)",
> 740	      personaType: "self_clone",
> 741	      tier: 1,
> 742	      provider: "higgsfield",
> 743	      gateMode: "vlm_soft",
> 744	      referenceUrls: [],
> 745	      status: "idle",
> 746	      ...overrides,
> 747	    },
> 748	  };
> 749	}
> 750	
> 751	/* ── Canvas-execute payload helper ───────────────────────────────────── */
> 752	
> 753	/**
> 754	 * Helper to compile prompt incorporating project level StyleSettings
> 755	 */
> 756	export function compileFinalPrompt(
> 757	  prompt: string,
> 758	  styleSettings?: StyleSettings,
> 759	  inheritStyle?: boolean,
> 760	): string {
> 761	  if (!inheritStyle || !styleSettings) return prompt;
> 762	
> 763	  const parts: string[] = [];
> 764	  if (prompt.trim()) {
> 765	    parts.push(prompt.trim());
> 766	  }
> 767	
> 768	  const { stylePreset, mood, palette } = styleSettings;
> 769	
> 770	  if (mood && mood.trim()) {
> 771	    parts.push(`mood: ${mood.trim()}`);
> 772	  }
> 773	
> 774	  if (stylePreset && stylePreset !== "none") {
> 775	    const presetSuffixes: Record<StylePresetId, string> = {
> 776	      none: "",
> 777	      cinematic: "cinematic film still, anamorphic lens, dramatic lighting, 35mm film grain, shallow depth of field",
> 778	      photorealistic: "highly detailed photorealistic image, 8k resolution, natural lighting, high dynamic range",
> 779	      anime: "anime illustration style, cel shaded, vibrant colors, expressive line art",
> 780	      illustration: "artistic illustration, hand-drawn texture, stylized composition",
> 781	      noir: "film noir aesthetic, high contrast black and white, dramatic shadows, moody lighting",
> 782	      documentary: "documentary style photography, candid capture, natural lighting, realistic grain",
> 783	    };
> 784	    const suffix = presetSuffixes[stylePreset];
> 785	    if (suffix) {
> 786	      parts.push(suffix);
> 787	    }
> 788	  }
> 789	
> 790	  if (palette && palette.length > 0) {
> 791	    const validColors = palette.filter(c => c && c.trim());
> 792	    if (validColors.length > 0) {
> 793	      parts.push(`color palette: ${validColors.join(", ")}`);
> 794	    }
> 795	  }
> 796	
> 797	  return parts.join(", ");
> 798	}
> 799	
> 800	/**
> 801	 * Translate a typed node's data into the request body accepted by the
> 802	 * `canvas-execute` Edge Function. Soul models split into provider/model
> 803	 * plus parameters.resolution/batch so the function's tiering helper
> 804	 * (`resolveHiggsfieldSoulKey`) computes the correct cost.
> 805	 */
> 806	export function resolveExecutePayload(
> 807	  data: CanvasNodeData,
> 808	  styleSettings?: StyleSettings,
> 809	): {
> 810	  node_type: string;
> 811	  provider: ProviderId;
> 812	  model: string;
> 813	  prompt: string;
> 814	  negative_prompt?: string;
> 815	  parameters: Record<string, unknown>;
> 816	} | null {
> 817	  switch (data.kind) {
> 818	    case "generateImage": {
> 819	      const info = getImageModelInfo(data.modelId);
> 820	      const parameters: Record<string, unknown> = {
> 821	        aspect_ratio: data.aspectRatio,
> 822	        controls: data.controls,
> 823	        seed: data.fixedSeed && data.seed != null ? data.seed : undefined,
> 824	      };
> 825	      if (info.resolution) parameters.resolution = info.resolution;
> 826	      if (info.batch) parameters.batch = info.batch;
> 827	      return {
> 828	        node_type: "generate_image",
> 829	        provider: info.provider,
> 830	        model: info.modelParam,
> 831	        prompt: compileFinalPrompt(data.prompt, styleSettings, data.inheritStyle),
> 832	        negative_prompt: data.negativePrompt || undefined,
> 833	        parameters,
> 834	      };
> 835	    }
> 836	    case "sceneCompose": {
> 837	      const info = getImageModelInfo(data.modelId);
> 838	      const parameters: Record<string, unknown> = {
> 839	        aspect_ratio: data.aspectRatio,
> 840	      };
> 841	      if (info.resolution) parameters.resolution = info.resolution;
> 842	      if (info.batch) parameters.batch = info.batch;
> 843	      return {
> 844	        node_type: "scene_compose",
> 845	        provider: info.provider,
> 846	        model: info.modelParam,
> 847	        prompt: compileFinalPrompt(data.prompt, styleSettings, data.inheritStyle),
> 848	        parameters,
> 849	      };
> 850	    }
> 851	    case "styleTransfer": {
> 852	      const preset = STYLE_TRANSFER_PRESETS.find((p) => p.id === data.presetId);
> 853	      return {
> 854	        node_type: "style_transfer",
> 855	        provider: "higgsfield",
> 856	        model: "soul",
> 857	        prompt: preset?.suffix ?? "",
> 858	        parameters: {
> 859	          strength: data.strength,
> 860	          preset_id: data.presetId,
> 861	          resolution: "720p",
> 862	          batch: 1,
> 863	        },
> 864	      };
> 865	    }
> 866	    case "imageToVideo": {
> 867	      const info = getVideoModelInfo(data.videoModel);
> 868	      return {
> 869	        node_type: "image_to_video",
> 870	        provider: info.provider,
> 871	        model: info.modelParam,
> 872	        prompt: data.prompt,
> 873	        parameters: {
> 874	          duration: data.duration,
> 875	          aspect_ratio: data.aspectRatio,
> 876	          motion_strength: data.motionStrength,
> 877	          async_only: info.asyncOnly ?? false,
> 878	        },
> 879	      };
> 880	    }
> 881	    case "characterReference":
> 882	      // CharacterReference doesn't trigger canvas-execute by itself —
> 883	      // it's a data source consumed by downstream sceneCompose/styleTransfer.
> 884	      return null;
> 885	    case "voiceClone":
> 886	      // voiceClone runs against the net-new `generate-voice` Edge Function (FR-AC-009),
> 887	      // NOT canvas-execute — its inspector calls useAvatarVoice directly.
> 888	      return null;
> 889	    case "avatarIdentity":
> 890	      // avatarIdentity trains against the net-new `avatar-identity-train` Edge Function
> 891	      // (FR-AC-012, gated OTD-AC-017), NOT canvas-execute — inspector handles it directly.
> 892	      return null;
> 893	  }
> 894	}
> 895	
> 896	/**
> 897	 * Type-guard helpers (used by node components and inspectors to narrow
> 898	 * the union via switch/case on `kind`).
> 899	 */
> 900	export function isGenerateImage(data: CanvasNodeData): data is GenerateImageData {
> 901	  return data.kind === "generateImage";
> 902	}
> 903	export function isCharacterReference(data: CanvasNodeData): data is CharacterReferenceData {
> 904	  return data.kind === "characterReference";
> 905	}
> 906	export function isSceneCompose(data: CanvasNodeData): data is SceneComposeData {
> 907	  return data.kind === "sceneCompose";
> 908	}
> 909	export function isStyleTransfer(data: CanvasNodeData): data is StyleTransferData {
> 910	  return data.kind === "styleTransfer";
> 911	}
> 912	export function isImageToVideo(data: CanvasNodeData): data is ImageToVideoData {
> 913	  return data.kind === "imageToVideo";
> 914	}
> 915	export function isVoiceClone(data: CanvasNodeData): data is VoiceCloneData {
> 916	  return data.kind === "voiceClone";
> 917	}
> 918	export function isAvatarIdentity(data: CanvasNodeData): data is AvatarIdentityData {
> 919	  return data.kind === "avatarIdentity";
> 920	}
> 921	
> 922	/** Resolve the mcoCoins cost of a single node from MODEL_INFO/VIDEO_MODEL_INFO. */
> 923	export function estimateNodeCost(data: CanvasNodeData): number {
> 924	  switch (data.kind) {
> 925	    case "generateImage":
> 926	      return getImageModelInfo(data.modelId).coinCost;
> 927	    case "sceneCompose":
> 928	      return data.cost;
> 929	    case "styleTransfer":
> 930	      return data.cost;
> 931	    case "imageToVideo":
> 932	      return getVideoModelInfo(data.videoModel).coinCost;
> 933	    case "characterReference":
> 934	      return 0;
> 935	    case "voiceClone":
> 936	      return 36; // COIN_COSTS.VOICE_GENERATION (charged on synthesize; clone is free)
> 937	    case "avatarIdentity":
> 938	      return 0; // train (FR-AC-012) is gated OTD-AC-017; cost charged server-side when wired (OTD-AC-006)
> 939	  }
> 940	}
> 941	
> ```

## 🤖 Claude *(18:42:00)*


## 🤖 Claude *(18:42:01)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCanvasPipeline.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useState, useCallback, useMemo, useEffect } from "react";
> 2	import { toast } from "sonner";
> 3	import { useCanvasStore } from "@/store/useCanvasStore";
> 4	import { useCanvasExecute } from "@/hooks/useCanvasStudio";
> 5	import { getTopologicalLayers } from "@/lib/canvas-dag";
> 6	import { findUpstreamImage, findUpstreamImages, findUpstreamHandleAsset } from "@/lib/canvas-utils";
> 7	import { assertExecuteSuccess } from "@/lib/canvas-execute-result";
> 8	import {
> 9	  CanvasNode,
> 10	  estimateNodeCost,
> 11	  resolveExecutePayload,
> 12	} from "@/types/canvas";
> 13	
> 14	export type PipelineStatus = "pending" | "running" | "done" | "error" | "blocked";
> 15	
> 16	export function useCanvasPipeline({
> 17	  projectId,
> 18	  refetchDashboard,
> 19	}: {
> 20	  projectId?: string;
> 21	  refetchDashboard?: () => void;
> 22	}) {
> 23	  const [pipelineStatus, setPipelineStatus] = useState<PipelineStatus>("pending");
> 24	
> 25	  const nodes = useCanvasStore((s) => s.nodes);
> 26	  const edges = useCanvasStore((s) => s.edges);
> 27	  const updateNodeData = useCanvasStore((s) => s.updateNodeData);
> 28	  const styleSettings = useCanvasStore((s) => s.styleSettings);
> 29	  const executeNode = useCanvasExecute();
> 30	
> 31	  // Determine if a node is currently runnable
> 32	  const runnable = useMemo(() => {
> 33	    return nodes.filter((n) => {
> 34	      if (n.data.kind === "characterReference") return false;
> 35	      if (n.data.status === "running" || n.data.status === "queued") return false;
> 36	
> 37	      const prompt = "prompt" in n.data ? n.data.prompt : "";
> 38	      if (!prompt || !prompt.trim()) return false;
> 39	
> 40	      if (n.data.kind === "imageToVideo") {
> 41	        const hasUpstream = edges.some((e) => e.target === n.id);
> 42	        if (!hasUpstream) return false;
> 43	      }
> 44	      return true;
> 45	    });
> 46	  }, [nodes, edges]);
> 47	
> 48	  const runnableCount = runnable.length;
> 49	
> 50	  const runAllCost = useMemo(() => {
> 51	    return runnable.reduce((sum, n) => sum + estimateNodeCost(n.data), 0);
> 52	  }, [runnable]);
> 53	
> 54	  // Check on load/graph change if there's any cycle
> 55	  useEffect(() => {
> 56	    if (nodes.length === 0) {
> 57	      setPipelineStatus("pending");
> 58	      return;
> 59	    }
> 60	    try {
> 61	      getTopologicalLayers(nodes, edges);
> 62	      setPipelineStatus((prev) => (prev === "blocked" ? "pending" : prev));
> 63	    } catch (e) {
> 64	      setPipelineStatus("blocked");
> 65	    }
> 66	  }, [nodes, edges]);
> 67	
> 68	  // Run a single node
> 69	  const runSingleNode = useCallback(
> 70	    async (nodeId: string) => {
> 71	      const currentNodes = useCanvasStore.getState().nodes;
> 72	      const currentEdges = useCanvasStore.getState().edges;
> 73	      const currentStyleSettings = useCanvasStore.getState().styleSettings;
> 74	
> 75	      const n = currentNodes.find((node) => node.id === nodeId);
> 76	      if (!n) return;
> 77	
> 78	      const payload = resolveExecutePayload(n.data, currentStyleSettings);
> 79	      if (!payload) return;
> 80	
> 81	      const isVideo = n.data.kind === "imageToVideo";
> 82	      const inputAssetUrl = isVideo
> 83	        ? findUpstreamImage(n.id, currentNodes, currentEdges)
> 84	        : undefined;
> 85	
> 86	      if (isVideo && !inputAssetUrl) {
> 87	        updateNodeData(n.id, {
> 88	          status: "failed",
> 89	          error: "Imagem de entrada não disponível",
> 90	        });
> 91	        return;
> 92	      }
> 93	
> 94	      const isSceneCompose = n.data.kind === "sceneCompose";
> 95	      const sceneComposeInputs = isSceneCompose
> 96	        ? {
> 97	            input_image_1: findUpstreamHandleAsset(n.id, "input_image_1", currentNodes, currentEdges),
> 98	            input_image_2: findUpstreamHandleAsset(n.id, "input_image_2", currentNodes, currentEdges),
> 99	            input_layout: findUpstreamHandleAsset(n.id, "input_layout", currentNodes, currentEdges),
> 100	          }
> 101	        : {};
> 102	
> 103	      // Cross-node consistency (Phase 4.3): image/style nodes inherit the
> 104	      // upstream connected creative(s) as reference images so identity is
> 105	      // preserved across the chain. SOP: docs/processes/canvas-node-consistency.md.
> 106	      const wantsReference = n.data.kind === "generateImage" || n.data.kind === "styleTransfer";
> 107	      const referenceImageUrls = wantsReference
> 108	        ? findUpstreamImages(n.id, currentNodes, currentEdges)
> 109	        : [];
> 110	
> 111	      updateNodeData(n.id, { status: "running", error: undefined });
> 112	
> 113	      try {
> 114	        const raw = await executeNode.mutateAsync({
> 115	          project_id: projectId!,
> 116	          node_id: n.id,
> 117	          ...payload,
> 118	          ...(inputAssetUrl ? { input_asset_url: inputAssetUrl } : {}),
> 119	          ...sceneComposeInputs,
> 120	          ...(referenceImageUrls.length ? { reference_image_urls: referenceImageUrls } : {}),
> 121	        });
> 122	        const result = assertExecuteSuccess(raw);
> 123	
> 124	        if (isVideo) {
> 125	          // Async job submitted — let Realtime or polling finalize it
> 126	        } else {
> 127	          updateNodeData(n.id, {
> 128	            status: "success",
> 129	            output: {
> 130	              imageUrl: result.output_url ?? undefined,
> 131	              generatedAt: new Date().toISOString(),
> 132	            },
> 133	            error: undefined,
> 134	          });
> 135	        }
> 136	      } catch (e) {
> 137	        const msg = e instanceof Error ? e.message : String(e);
> 138	        updateNodeData(n.id, { status: "failed", error: msg });
> 139	      }
> 140	    },
> 141	    [projectId, updateNodeData, executeNode]
> 142	  );
> 143	
> 144	  // Helper: wait for nodes to complete in Zustand
> 145	  const waitForNodesToComplete = useCallback(async (nodeIds: string[]): Promise<boolean> => {
> 146	    return new Promise((resolve) => {
> 147	      const checkComplete = () => {
> 148	        const currentNodes = useCanvasStore.getState().nodes;
> 149	        const relevantNodes = currentNodes.filter((n) => nodeIds.includes(n.id));
> 150	
> 151	        const allDone = relevantNodes.every(
> 152	          (n) => n.data.status === "success" || n.data.status === "failed"
> 153	        );
> 154	        const anyFailed = relevantNodes.some((n) => n.data.status === "failed");
> 155	
> 156	        return { allDone, anyFailed };
> 157	      };
> 158	
> 159	      const initial = checkComplete();
> 160	      if (initial.allDone) {
> 161	        resolve(!initial.anyFailed);
> 162	        return;
> 163	      }
> 164	
> 165	      const unsubscribe = useCanvasStore.subscribe(() => {
> 166	        const { allDone, anyFailed } = checkComplete();
> 167	        if (allDone) {
> 168	          unsubscribe();
> 169	          resolve(!anyFailed);
> 170	        }
> 171	      });
> 172	    });
> 173	  }, []);
> 174	
> 175	  // Execute pipeline
> 176	  const runPipeline = useCallback(async () => {
> 177	    if (!projectId) return;
> 178	
> 179	    let layers: CanvasNode[][];
> 180	    try {
> 181	      layers = getTopologicalLayers(nodes, edges);
> 182	    } catch (e) {
> 183	      setPipelineStatus("blocked");
> 184	      toast.error("Ciclo detectado no grafo! O pipeline não pode ser executado.");
> 185	      return;
> 186	    }
> 187	
> 188	    const runnableIds = runnable.map((n) => n.id);
> 189	    if (runnableIds.length === 0) {
> 190	      toast.error("Nenhum nó qualificado para execução.");
> 191	      return;
> 192	    }
> 193	
> 194	    setPipelineStatus("running");
> 195	    toast.info(`Iniciando execução em camadas de ${runnableIds.length} nós...`);
> 196	
> 197	    let executionSuccess = true;
> 198	
> 199	    for (let i = 0; i < layers.length; i++) {
> 200	      const layer = layers[i];
> 201	      const layerRunnable = layer.filter((n) => runnableIds.includes(n.id));
> 202	
> 203	      if (layerRunnable.length === 0) {
> 204	        continue;
> 205	      }
> 206	
> 207	      // Mark layer nodes as queued
> 208	      for (const n of layerRunnable) {
> 209	        updateNodeData(n.id, { status: "queued", error: undefined });
> 210	      }
> 211	
> 212	      // Wait 100ms for UI status update
> 213	      await new Promise((resolve) => setTimeout(resolve, 100));
> 214	
> 215	      // Execute all nodes in this layer in parallel
> 216	      const runPromises = layerRunnable.map((n) => runSingleNode(n.id));
> 217	      await Promise.all(runPromises);
> 218	
> 219	      // Wait for all nodes in this layer to reach success/failed
> 220	      const layerIds = layerRunnable.map((n) => n.id);
> 221	      const layerSuccess = await waitForNodesToComplete(layerIds);
> 222	
> 223	      if (!layerSuccess) {
> 224	        executionSuccess = false;
> 225	        break;
> 226	      }
> 227	    }
> 228	
> 229	    if (executionSuccess) {
> 230	      setPipelineStatus("done");
> 231	      toast.success("Pipeline executado com sucesso!");
> 232	    } else {
> 233	      setPipelineStatus("error");
> 234	      toast.error("Erro na execução do pipeline. Algumas etapas falharam.");
> 235	    }
> 236	
> 237	    refetchDashboard?.();
> 238	  }, [nodes, edges, runnable, projectId, runSingleNode, waitForNodesToComplete, updateNodeData, refetchDashboard]);
> 239	
> 240	  const resetPipeline = useCallback(() => {
> 241	    setPipelineStatus("pending");
> 242	  }, []);
> 243	
> 244	  return {
> 245	    pipelineStatus,
> 246	    runPipeline,
> 247	    resetPipeline,
> 248	    runnable,
> 249	    runnableCount,
> 250	    runAllCost,
> 251	    runSingleNode,
> 252	  };
> 253	}
> 254	
> ```

## 🤖 Claude *(18:42:01)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useCanvasJobsRealtime.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useEffect } from 'react';
> 2	import { useQueryClient } from '@tanstack/react-query';
> 3	import { supabase } from '@/integrations/supabase/client';
> 4	import { useAuth } from '@/hooks/useAuth';
> 5	
> 6	/**
> 7	 * vm_canvas_executions row shape relayed by the Realtime callback. Includes
> 8	 * the columns Phase 4.2c needs to reconcile the Zustand store on the client.
> 9	 */
> 10	export interface CanvasExecutionRow {
> 11	  id: string;
> 12	  project_id: string;
> 13	  node_id: string | null;
> 14	  status: 'pending' | 'queued' | 'running' | 'success' | 'failed' | 'cancelled' | 'timeout';
> 15	  output_url: string | null;
> 16	  error_message: string | null;
> 17	  completed_at: string | null;
> 18	}
> 19	
> 20	/**
> 21	 * Subscribes to vm_canvas_executions UPDATEs for the current user via Supabase Realtime.
> 22	 * Invalidates TanStack Query keys on every status transition AND invokes the optional
> 23	 * `onUpdate` callback so callers can reconcile the Zustand canvas store with the row.
> 24	 *
> 25	 * Used by Phase 4.2c async video flow: higgsfield-webhook flips status
> 26	 * `queued → success/failed/timeout`, this hook (a) refetches query caches and
> 27	 * (b) delegates the node-level status sync to the caller via `onUpdate`.
> 28	 *
> 29	 * Pattern mirrors `useMcorchMemory.ts:91-112` (canonical Realtime subscription).
> 30	 * RLS-aligned: `user_id=eq.<auth.uid>` filter ensures cross-tenant isolation at
> 31	 * the channel level. The callback is the single bridge between Realtime → Zustand,
> 32	 * keeping the store as the source of truth for node visual state.
> 33	 */
> 34	export function useCanvasJobsRealtime(
> 35	  projectId?: string,
> 36	  onUpdate?: (row: CanvasExecutionRow) => void,
> 37	): void {
> 38	  const qc = useQueryClient();
> 39	  const { user } = useAuth();
> 40	
> 41	  useEffect(() => {
> 42	    if (!user) return;
> 43	
> 44	    const channel = supabase
> 45	      .channel(`canvas_jobs_${user.id}`)
> 46	      .on(
> 47	        'postgres_changes',
> 48	        {
> 49	          event: 'UPDATE',
> 50	          schema: 'public',
> 51	          table: 'vm_canvas_executions',
> 52	          filter: `user_id=eq.${user.id}`,
> 53	        },
> 54	        (payload) => {
> 55	          const row = payload.new as CanvasExecutionRow;
> 56	          qc.invalidateQueries({ queryKey: ['canvas-execution', row.id] });
> 57	          if (projectId && row.project_id === projectId) {
> 58	            qc.invalidateQueries({ queryKey: ['vm-canvas-assets', projectId] });
> 59	            qc.invalidateQueries({ queryKey: ['vm-canvas-executions', projectId] });
> 60	          }
> 61	          onUpdate?.(row);
> 62	        },
> 63	      )
> 64	      .subscribe();
> 65	
> 66	    return () => {
> 67	      supabase.removeChannel(channel);
> 68	    };
> 69	  }, [user?.id, projectId, qc, onUpdate]);
> 70	}
> 71	
> ```

## 🤖 Claude *(18:42:08)*


## 🤖 Claude *(18:42:09)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/higgsfield-webhook/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// higgsfield-webhook — Receives Higgsfield video generation callbacks (Phase 4.2b).
> 2	//
> 3	// URL pattern: https://<project>.supabase.co/functions/v1/higgsfield-webhook?token=<webhook_token>
> 4	//
> 5	// Auth: token query param matched against vm_canvas_executions.webhook_token (unique index).
> 6	// NOT JWT-protected — external caller is Higgsfield. Token = 64 hex chars (2 concatenated UUIDs).
> 7	//
> 8	// Aligned with .claude/context/higgsfield-api-validation-2026-05-15.md
> 9	// Spec source: .claude/proposals/vm-canvas-jobs-async-video-v1.md
> 10	// Migration:   supabase/migrations/20260516224542_vm_canvas_executions_async_video.sql
> 11	
> 12	import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
> 13	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 14	
> 15	const corsHeaders = {
> 16	  "Access-Control-Allow-Origin": "*",
> 17	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 18	  "Access-Control-Allow-Headers": "content-type",
> 19	};
> 20	
> 21	const MIN_VIDEO_BYTES = 100 * 1024; // 100 KB — pattern from rescue-video.ts to reject JSON error stubs
> 22	const TOKEN_LENGTH = 64;             // 2× UUID without dashes (per migration default)
> 23	
> 24	interface ExecutionRow {
> 25	  id: string;
> 26	  user_id: string;
> 27	  project_id: string;
> 28	  credits_charged: number;
> 29	  status: string;
> 30	  node_id: string;
> 31	  node_type: string;
> 32	  model: string;
> 33	  prompt: string | null;
> 34	  negative_prompt: string | null;
> 35	  parameters: Record<string, unknown>;
> 36	  input_asset_id: string | null;
> 37	}
> 38	
> 39	async function updateProjectGraph(
> 40	  admin: any,
> 41	  projectId: string,
> 42	  nodeId: string,
> 43	  status: "success" | "failed",
> 44	  payload: { videoUrl?: string | null; errorMessage?: string }
> 45	) {
> 46	  try {
> 47	    const { data: proj, error: projErr } = await admin
> 48	      .from("vm_canvas_projects")
> 49	      .select("graph")
> 50	      .eq("id", projectId)
> 51	      .maybeSingle();
> 52	
> 53	    if (projErr) {
> 54	      console.error(`[webhook] failed to fetch project graph for sync:`, projErr.message);
> 55	      return;
> 56	    }
> 57	    if (!proj || !proj.graph || typeof proj.graph !== "object") {
> 58	      return;
> 59	    }
> 60	
> 61	    const graph = proj.graph as any;
> 62	    const nodes = graph.nodes || [];
> 63	    let updated = false;
> 64	
> 65	    const updatedNodes = nodes.map((node: any) => {
> 66	      if (node.id === nodeId) {
> 67	        updated = true;
> 68	        const currentData = node.data || {};
> 69	        return {
> 70	          ...node,
> 71	          data: {
> 72	            ...currentData,
> 73	            status: status,
> 74	            ...(status === "success"
> 75	              ? {
> 76	                  output: {
> 77	                    ...currentData.output,
> 78	                    videoUrl: payload.videoUrl || undefined,
> 79	                    generatedAt: new Date().toISOString(),
> 80	                  },
> 81	                  error: undefined,
> 82	                }
> 83	              : {
> 84	                  error: payload.errorMessage || "Generation failed",
> 85	                }),
> 86	          },
> 87	        };
> 88	      }
> 89	      return node;
> 90	    });
> 91	
> 92	    if (updated) {
> 93	      graph.nodes = updatedNodes;
> 94	      const { error: saveErr } = await admin
> 95	        .from("vm_canvas_projects")
> 96	        .update({ graph })
> 97	        .eq("id", projectId);
> 98	
> 99	      if (saveErr) {
> 100	        console.error(`[webhook] failed to update project graph:`, saveErr.message);
> 101	      } else {
> 102	        console.log(`[webhook] successfully synced node ${nodeId} to status ${status} in project ${projectId}`);
> 103	      }
> 104	    }
> 105	  } catch (e) {
> 106	    console.error(`[webhook] error in updateProjectGraph:`, e);
> 107	  }
> 108	}
> 109	
> 110	serve(async (req) => {
> 111	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 112	  if (req.method !== "POST") {
> 113	    return new Response("Method not allowed", { status: 405, headers: corsHeaders });
> 114	  }
> 115	
> 116	  const url = new URL(req.url);
> 117	  const token = url.searchParams.get("token");
> 118	  if (!token || token.length !== TOKEN_LENGTH) {
> 119	    return new Response(JSON.stringify({ error: "missing or malformed token" }), {
> 120	      status: 400,
> 121	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 122	    });
> 123	  }
> 124	
> 125	  const supabaseUrl = Deno.env.get("SUPABASE_URL")!;
> 126	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 127	  const admin = createClient(supabaseUrl, serviceKey);
> 128	
> 129	  // Look up execution by webhook_token (unique index — single-row query)
> 130	  const { data: exec, error: lookupErr } = await admin
> 131	    .from("vm_canvas_executions")
> 132	    .select("id, user_id, project_id, credits_charged, status, node_id, node_type, model, prompt, negative_prompt, parameters, input_asset_id")
> 133	    .eq("webhook_token", token)
> 134	    .maybeSingle();
> 135	
> 136	  if (lookupErr || !exec) {
> 137	    return new Response(JSON.stringify({ error: "invalid token" }), {
> 138	      status: 404,
> 139	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 140	    });
> 141	  }
> 142	
> 143	  const execution = exec as ExecutionRow;
> 144	
> 145	  // Idempotent: only accept callback if still in flight
> 146	  if (!["queued", "running"].includes(execution.status)) {
> 147	    return new Response(
> 148	      JSON.stringify({ error: "execution already finalized", status: execution.status }),
> 149	      { status: 409, headers: { ...corsHeaders, "Content-Type": "application/json" } },
> 150	    );
> 151	  }
> 152	
> 153	  let body: Record<string, unknown> = {};
> 154	  try {
> 155	    body = (await req.json()) as Record<string, unknown>;
> 156	  } catch {
> 157	    /* empty body is fine; treat as failure below */
> 158	  }
> 159	
> 160	  const nowIso = new Date().toISOString();
> 161	
> 162	  // Failure path: mark exec failed, NO deduct, NO upload.
> 163	  // Higgsfield terminal states `nsfw` and `canceled` are soft-fails that REFUND
> 164	  // credits upstream — they previously fell through to the success path and
> 165	  // surfaced the generic "no result_url" message. Map them to clear reasons here
> 166	  // (no deduct either way: deduct only fires after a verified upload).
> 167	  const terminalStatus = typeof body.status === "string" ? body.status.toLowerCase() : "";
> 168	  const isSoftFail =
> 169	    terminalStatus === "nsfw" || terminalStatus === "canceled" || terminalStatus === "cancelled";
> 170	  if (body.status === "failed" || body.error || isSoftFail) {
> 171	    const errMsg = isSoftFail
> 172	      ? terminalStatus === "nsfw"
> 173	        ? "Geração bloqueada pelo filtro NSFW do Higgsfield (crédito reembolsado)"
> 174	        : "Geração cancelada no Higgsfield (crédito reembolsado)"
> 175	      : (body.error as string) || "Higgsfield reported failure";
> 176	    await admin
> 177	      .from("vm_canvas_executions")
> 178	      .update({
> 179	        status: "failed",
> 180	        error_message: errMsg,
> 181	        response_payload: body,
> 182	        webhook_received_at: nowIso,
> 183	        completed_at: nowIso,
> 184	      })
> 185	      .eq("id", execution.id);
> 186	
> 187	    // Sync node status in project graph
> 188	    await updateProjectGraph(admin, execution.project_id, execution.node_id, "failed", { errorMessage: errMsg });
> 189	
> 190	    // SSP-01 OE03 Pillar 4 (Observability) — best-effort health pulse
> 191	    await admin
> 192	      .from("infra_health_logs")
> 193	      .insert({ service: "higgsfield-webhook", status: "unhealthy" })
> 194	      .then(() => {}, (e) => console.error("[higgsfield-webhook] health log failed:", e));
> 195	
> 196	    return new Response(JSON.stringify({ ok: true, status: "failed" }), {
> 197	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 198	    });
> 199	  }
> 200	
> 201	  // Success path: resolve result URL from payload variants
> 202	  const payload = body.payload as { video?: { url?: string }; result_url?: string; url?: string } | undefined;
> 203	  const video = body.video as { url?: string } | undefined;
> 204	  const resultUrl =
> 205	    (body.result_url as string | undefined) ||
> 206	    (body.url as string | undefined) ||
> 207	    video?.url ||
> 208	    payload?.video?.url ||
> 209	    payload?.result_url ||
> 210	    payload?.url;
> 211	
> 212	  if (!resultUrl) {
> 213	    const errMsg = "no result_url in webhook payload";
> 214	    await admin
> 215	      .from("vm_canvas_executions")
> 216	      .update({
> 217	        status: "failed",
> 218	        error_message: errMsg,
> 219	        response_payload: body,
> 220	        webhook_received_at: nowIso,
> 221	        completed_at: nowIso,
> 222	      })
> 223	      .eq("id", execution.id);
> 224	
> 225	    await updateProjectGraph(admin, execution.project_id, execution.node_id, "failed", { errorMessage: errMsg });
> 226	
> 227	    // SSP-01 OE03 Pillar 4 (Observability)
> 228	    await admin
> 229	      .from("infra_health_logs")
> 230	      .insert({ service: "higgsfield-webhook", status: "unhealthy" })
> 231	      .then(() => {}, (e) => console.error("[higgsfield-webhook] health log failed:", e));
> 232	
> 233	    return new Response(JSON.stringify({ error: errMsg }), {
> 234	      status: 400,
> 235	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 236	    });
> 237	  }
> 238	
> 239	  try {
> 240	    // Download → validate ≥ 100 KB + content-type starts with 'video/'
> 241	    const videoResp = await fetch(resultUrl);
> 242	    if (!videoResp.ok) throw new Error(`fetch result_url failed: ${videoResp.status}`);
> 243	    const videoBytes = new Uint8Array(await videoResp.arrayBuffer());
> 244	    if (videoBytes.byteLength < MIN_VIDEO_BYTES) {
> 245	      throw new Error(`video too small (${videoBytes.byteLength} bytes) — likely error stub`);
> 246	    }
> 247	    const contentType = videoResp.headers.get("content-type") || "video/mp4";
> 248	    if (!contentType.startsWith("video/")) {
> 249	      throw new Error(`unexpected content-type: ${contentType}`);
> 250	    }
> 251	
> 252	    // Upload to canvas-assets bucket — private; client uses signed URL
> 253	    const fileName = `${execution.project_id}/${execution.id}.mp4`;
> 254	    const { error: upErr } = await admin.storage
> 255	      .from("canvas-assets")
> 256	      .upload(fileName, videoBytes, { contentType, upsert: true });
> 257	    if (upErr) throw new Error(`storage upload: ${upErr.message}`);
> 258	
> 259	    const { data: signed } = await admin.storage
> 260	      .from("canvas-assets")
> 261	      .createSignedUrl(fileName, 7 * 24 * 60 * 60); // 7d
> 262	
> 263	    const signedUrl = signed?.signedUrl || null;
> 264	
> 265	    // Atomic finalize: update exec → deduct → insert asset row
> 266	    // (deduct is via the post-migration 4-arg deduct_mco_coins that ALSO logs to mcoin_transactions)
> 267	    await admin
> 268	      .from("vm_canvas_executions")
> 269	      .update({
> 270	        status: "success",
> 271	        output_url: signedUrl,
> 272	        response_payload: body,
> 273	        webhook_received_at: nowIso,
> 274	        completed_at: nowIso,
> 275	      })
> 276	      .eq("id", execution.id);
> 277	
> 278	    // Sync node status in project graph
> 279	    await updateProjectGraph(admin, execution.project_id, execution.node_id, "success", { videoUrl: signedUrl });
> 280	
> 281	    // Deduct ONLY after upload-OK (atomic per Sovereign requirement; logs negative-amount ledger row)
> 282	    await admin.rpc("deduct_mco_coins", {
> 283	      p_user_id: execution.user_id,
> 284	      p_amount: execution.credits_charged,
> 285	      p_action: "canvas_video_spend",
> 286	      p_context: {
> 287	        execution_id: execution.id,
> 288	        node_id: execution.node_id,
> 289	        model: execution.model,
> 290	        video_path: fileName,
> 291	      },
> 292	    });
> 293	
> 294	    // Asset row for the new video (vm_canvas_assets schema requires mime_type)
> 295	    await admin.from("vm_canvas_assets").insert({
> 296	      user_id: execution.user_id,
> 297	      project_id: execution.project_id,
> 298	      asset_type: "video",
> 299	      storage_key: fileName,
> 300	      storage_bucket: "canvas-assets",
> 301	      public_url: signedUrl,
> 302	      mime_type: contentType,
> 303	      file_size_bytes: videoBytes.byteLength,
> 304	      provider: "higgsfield",
> 305	      model_used: execution.model,
> 306	      node_type: execution.node_type,
> 307	      prompt: execution.prompt,
> 308	      negative_prompt: execution.negative_prompt,
> 309	      parameters: execution.parameters,
> 310	      credits_cost: execution.credits_charged,
> 311	      node_id: execution.node_id,
> 312	      input_asset_id: execution.input_asset_id,
> 313	    });
> 314	
> 315	    // SSP-01 OE03 Pillar 4 (Observability) — success heartbeat
> 316	    await admin
> 317	      .from("infra_health_logs")
> 318	      .insert({ service: "higgsfield-webhook", status: "healthy" })
> 319	      .then(() => {}, (e) => console.error("[higgsfield-webhook] health log failed:", e));
> 320	
> 321	    return new Response(JSON.stringify({ ok: true, status: "success", url: signedUrl }), {
> 322	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 323	    });
> 324	  } catch (e) {
> 325	    const msg = e instanceof Error ? e.message : "unknown finalize error";
> 326	    await admin
> 327	      .from("vm_canvas_executions")
> 328	      .update({
> 329	        status: "failed",
> 330	        error_message: msg,
> 331	        response_payload: body,
> 332	        webhook_received_at: nowIso,
> 333	        completed_at: nowIso,
> 334	      })
> 335	      .eq("id", execution.id);
> 336	
> 337	    await updateProjectGraph(admin, execution.project_id, execution.node_id, "failed", { errorMessage: msg });
> 338	
> 339	    // SSP-01 OE03 Pillar 4 (Observability) — catch path
> 340	    await admin
> 341	      .from("infra_health_logs")
> 342	      .insert({ service: "higgsfield-webhook", status: "unhealthy" })
> 343	      .then(() => {}, (logErr) => console.error("[higgsfield-webhook] health log failed:", logErr));
> 344	
> 345	    return new Response(JSON.stringify({ error: msg }), {
> 346	      status: 500,
> 347	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 348	    });
> 349	  }
> 350	});
> 351	
> ```

## 🤖 Claude *(18:42:09)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useParamRegistry.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	/**
> 2	 * useParamRegistry.ts — Declarative parameter schema + cost estimation for nodes.
> 3	 *
> 4	 * Separates "what params a node exposes" (data) from "how the HUD draws them" (UI).
> 5	 * Drives both the inline node controls AND the right-side Settings panel (the
> 6	 * verified hybrid HUD — UI-SPACES-009). Trace: SD-SPACES-002, BR-SPACES-002.
> 7	 *
> 8	 * Promotion target: src/hooks/useParamRegistry.ts
> 9	 */
> 10	import {
> 11	  ASPECT_RATIOS, IMAGE_MODELS,
> 12	  type SpaceNode, type AspectRatio, type ImageModel,
> 13	} from '@/lib/spaces-schema';
> 14	
> 15	export interface ParamField {
> 16	  key: string;
> 17	  kind: 'text' | 'textarea' | 'select' | 'slider' | 'stepper' | 'toggle' | 'mask' | 'references';
> 18	  labelPt: string;                                   // pt-BR label
> 19	  options?: { value: string; labelPt: string }[];
> 20	  min?: number; max?: number; step?: number;
> 21	  /** mcoCoins delta when this option is enabled (shown inline — BR-SPACES-002) */
> 22	  costDelta?: number;
> 23	}
> 24	
> 25	/**
> 26	 * Verified server-side cost authority lives in `supabase/functions/canvas-execute`
> 27	 * (CREDIT_COSTS). The client mirror below is display-only — NEVER the source of truth.
> 28	 * Keys are a representative subset; keep in sync with the edge function.
> 29	 */
> 30	export const CLIENT_COST_MIRROR: Record<string, number> = {
> 31	  'auto': 15,                 // routed server-side; estimate only
> 32	  'flux.2-pro': 12, 'flux.2-max': 18, 'flux.1.1': 12, 'flux.1-fast': 6,
> 33	  'google-imagen-4': 18, 'google-imagen-4-ultra': 28, 'google-imagen-4-fast': 8,
> 34	  'seedream-4': 10, 'seedream-4-4k': 20, 'gpt-1.5': 18,
> 35	  'recraft-v4': 14, 'krea-2': 16, 'mystic-2.5-fluid': 14,
> 36	  // editing/utility ops (verified families)
> 37	  'upscale-2x': 8, 'upscale-4x': 20, 'inpaint': 6, 'remove-background': 3,
> 38	  'scene-compose': 18, 'style-transfer': 14,
> 39	};
> 40	
> 41	const IMAGE_MODEL_OPTIONS = IMAGE_MODELS.map((m) => ({
> 42	  value: m,
> 43	  labelPt: m === 'auto' ? 'Automático' : m.replace(/-/g, ' '),
> 44	}));
> 45	
> 46	const ASPECT_OPTIONS = ASPECT_RATIOS.map((r) => ({ value: r, labelPt: r }));
> 47	
> 48	/** Param schema per node category (extend as nodes are added). */
> 49	export function getSchema(node: SpaceNode): ParamField[] {
> 50	  switch (node.data.category) {
> 51	    case 'image':
> 52	      return [
> 53	        { key: 'modelKey', kind: 'select', labelPt: 'Modelo', options: IMAGE_MODEL_OPTIONS },
> 54	        { key: 'references', kind: 'references', labelPt: 'Referências (0/8)' },
> 55	        { key: 'prompt', kind: 'textarea', labelPt: 'Descreva a imagem que deseja gerar…' },
> 56	        { key: 'aspectRatio', kind: 'select', labelPt: 'Proporção', options: ASPECT_OPTIONS },
> 57	        { key: 'batch', kind: 'stepper', labelPt: 'Quantidade', min: 1, max: 8, step: 1 },
> 58	      ];
> 59	    case 'video':
> 60	      return [
> 61	        { key: 'modelKey', kind: 'select', labelPt: 'Modelo de vídeo' },
> 62	        { key: 'prompt', kind: 'textarea', labelPt: 'Descreva o vídeo…' },
> 63	        { key: 'aspectRatio', kind: 'select', labelPt: 'Proporção', options: ASPECT_OPTIONS },
> 64	      ];
> 65	    case 'audio':
> 66	      return [{ key: 'prompt', kind: 'textarea', labelPt: 'Texto / roteiro…' }];
> 67	    case 'text':
> 68	      return [{ key: 'prompt', kind: 'textarea', labelPt: 'Escreva o texto…' }];
> 69	    default:
> 70	      return [];
> 71	  }
> 72	}
> 73	
> 74	/** Estimate mcoCoins for a single node run (display only; server reconciles). */
> 75	export function estimateCost(node: SpaceNode): number {
> 76	  if (node.data.byok) return 0; // BR-SPACES-006
> 77	  const base = CLIENT_COST_MIRROR[node.data.modelKey ?? 'auto'] ?? 0;
> 78	  return base * Math.max(1, node.data.batch ?? 1);
> 79	}
> 80	
> 81	/** Project total cost for a set of nodes (pre-run — BR-SPACES-008). */
> 82	export function projectGraphCost(nodes: SpaceNode[]): number {
> 83	  return nodes.reduce((sum, n) => sum + estimateCost(n), 0);
> 84	}
> 85	
> 86	export type { AspectRatio, ImageModel };
> 87	
> ```

## 🤖 Claude *(18:42:17)*


## 🤖 Claude *(18:42:17)*

Now the Spaces registry and billing constants.

## 🤖 Claude *(18:42:19)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l /home/gcrUX/htdocs/constellation-orchestra/src/lib/spaces-schema.ts /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useSpaces.ts; grep -n \"canvas\\|CANVAS\\|VOICE\\|VIDEO\\|IMAGE\" /home/gcrUX/htdocs/constellation-orchestra/src/lib/billing.ts | head -30",
  "description": "Sizes of spaces files and canvas entries in billing.ts"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>   191 /home/gcrUX/htdocs/constellation-orchestra/src/lib/spaces-schema.ts
>   132 /home/gcrUX/htdocs/constellation-orchestra/src/hooks/useSpaces.ts
>   323 total
> 11://   FX:         R$5.5/USD assumed; conclusions hold across R$5–7 except IMAGE near R$7 (kept at 4× headroom).
> 14://   orchestrate run (3 texts + 1 image) ≈ $0.04 · Higgsfield DoP 5s video = $0.56 (canvas-execute, validated 4×).
> 15://   Per-op markup at the floor: ORCHESTRATION_RUN 10 → 4.4× ✓ · canvas video 125 → 4.0× ✓ · canvas image 12 → 5.4× ✓.
> 16://   ORCHESTRATION_RUN stays a FLAT 10 (bundle): covers 3×CONTENT_GENERATION + IMAGE_GENERATION (sum 15) at a
> 21:  IMAGE_GENERATION: 9,     // 1 DALL·E 3 1024² image ($0.04 → 4× at floor). WAS 3 = 1.36× (under-margined) → fixed.
> 31:  // generate-voice edge fn hardcodes its own VOICE_COST mirror (Deno can't import src/lib) — keep in sync.
> 32:  VOICE_GENERATION: 36,
> 36:  VISION_DESCRIBE_IMAGE: 2,      // VLM ~$0.0004/img (Gemini Flash) → 4×-floor
> 37:  VISION_ANALYZE_VIDEO: 2,       // per minute (Gemini video @1FPS ~$0.0054/min)
> 45:  VIDEO_FACELESS_RENDER: 125,    // faceless E2E pipeline (n8n Gemini→Pollinations→VoxCPM→Remotion→LTX→FFmpeg→QA) ≈ canvas DoP video
> 46:  VIDEO_HYPERFRAMES_RENDER: 12,  // deterministic HTML→MP4 via headless Chrome (no AI legs) ≈ canvas image class
> ```

## 🤖 Claude *(18:42:23)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/lib/spaces-schema.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	/**
> 2	 * spaces-schema.ts — Canonical domain types & runtime guards for the Spaces layer.
> 3	 *
> 4	 * Reverse-engineered from Magnific Spaces (live recon 2026-06-29) and anchored to the
> 5	 * existing MCORCH canvas (`useOrchestrationStore.ts`, `canvas-dag.ts`, `@xyflow/react`).
> 6	 *
> 7	 * Trace: SD-SPACES-006, UI-SPACES-010/011/012, LR-SPACES-005.
> 8	 * Rule (Sovereign): code in English; UI strings (pt-BR) live in i18n, never here.
> 9	 *
> 10	 * Promotion target: src/lib/spaces-schema.ts
> 11	 */
> 12	import { z } from 'zod';
> 13	import type { Node, Edge, Viewport } from '@xyflow/react';
> 14	
> 15	/* ── Port data types (type-safe connections; verified in Magnific) ─────────── */
> 16	export const PORT_DATA_TYPES = ['image', 'text', 'video', 'audio', 'svg', '3d'] as const;
> 17	export type PortDataType = (typeof PORT_DATA_TYPES)[number];
> 18	
> 19	/* ── Node run status — reused VERBATIM from useOrchestrationStore (no drift) ── */
> 20	export const NODE_STATUSES = ['idle', 'pending', 'running', 'done', 'error', 'blocked'] as const;
> 21	export type NodeStatus = (typeof NODE_STATUSES)[number];
> 22	
> 23	/* ── Node categories — 8 groups verified live (UI-SPACES-004) ──────────────── */
> 24	export const NODE_CATEGORIES = [
> 25	  'media', 'references', 'image', 'video', 'audio', 'text', 'utility', 'designer',
> 26	] as const;
> 27	export type NodeCategory = (typeof NODE_CATEGORIES)[number];
> 28	
> 29	/* ── Reference kinds — 9 verified in the References picker (UI-SPACES-012) ──── */
> 30	export const REFERENCE_KINDS = [
> 31	  'stock', 'style', 'character', 'element', 'location', 'color', 'effects', 'camera', 'sketch',
> 32	] as const;
> 33	export type ReferenceKind = (typeof REFERENCE_KINDS)[number];
> 34	
> 35	/* ── Aspect ratios — 10 verified (UI-SPACES-011) ───────────────────────────── */
> 36	export const ASPECT_RATIOS = [
> 37	  '1:1', '16:9', '9:16', '2:3', '3:4', '1:2', '2:1', '4:5', '3:2', '4:3',
> 38	] as const;
> 39	export type AspectRatio = (typeof ASPECT_RATIOS)[number];
> 40	
> 41	/* ── Image models — 38 verified in the model selector (UI-SPACES-010) ──────── *
> 42	 * `Auto` routes server-side by cost/quality (mirrors calc_agent_cost_mcoin).   */
> 43	export const IMAGE_MODELS = [
> 44	  'auto',
> 45	  'gpt-2', 'seedream-5-lite',
> 46	  'flux.2-max', 'flux.2-pro', 'flux.2-flex', 'flux.1-kontext-max', 'flux.2-klein',
> 47	  'flux.1-kontext-pro', 'mystic-2.5-fluid', 'flux.1', 'flux.1.1', 'flux.1-realism',
> 48	  'google-imagen-3', 'google-imagen-4-fast', 'google-imagen-4', 'google-imagen-4-ultra',
> 49	  'flux.1-fast', 'luma-uni-1.1', 'gpt', 'gpt-1-hq', 'gpt-1.5', 'gpt-1.5-high',
> 50	  'seedream-4', 'seedream-4-4k', 'seedream-4.5', 'runway', 'classic-fast', 'classic',
> 51	  'z-image', 'qwen', 'grok', 'recraft-v4', 'recraft-v4-pro', 'recraft-v4.1', 'krea-2',
> 52	  'mai-image-2.5',
> 53	] as const;
> 54	export type ImageModel = (typeof IMAGE_MODELS)[number];
> 55	
> 56	/* ── Port (verified handle ids: reference | prompt | output) ────────────────── */
> 57	export const PortSchema = z.object({
> 58	  /** stable handle id (e.g. 'reference', 'prompt', 'output') */
> 59	  id: z.string().min(1),
> 60	  direction: z.enum(['in', 'out']),
> 61	  dataType: z.enum(PORT_DATA_TYPES),
> 62	  /** pt-BR label rendered on the node edge */
> 63	  label: z.string(),
> 64	  /** for 'in' reference ports, the accepted reference kind */
> 65	  referenceKind: z.enum(REFERENCE_KINDS).optional(),
> 66	  required: z.boolean().optional(),
> 67	});
> 68	export type Port = z.infer<typeof PortSchema>;
> 69	
> 70	/* ── Reference attached to a generator node (0..8 — verified limit) ─────────── */
> 71	export const ReferenceSchema = z.object({
> 72	  kind: z.enum(REFERENCE_KINDS),
> 73	  assetId: z.string().uuid().optional(),
> 74	  /** external/library source id (e.g. '@kat' for a Magnific preset character) */
> 75	  presetId: z.string().optional(),
> 76	  url: z.string().url().optional(),
> 77	});
> 78	export type SpaceReference = z.infer<typeof ReferenceSchema>;
> 79	export const MAX_REFERENCES = 8;
> 80	
> 81	/* ── Node data — extends OrchestrationNodeData (coinCost/status/config kept) ── */
> 82	export const SpaceNodeDataSchema = z.object({
> 83	  label: z.string(),                                   // pt-BR
> 84	  category: z.enum(NODE_CATEGORIES),
> 85	  modelKey: z.string().optional(),                     // e.g. 'flux.2-pro' → CREDIT_COSTS
> 86	  aspectRatio: z.enum(ASPECT_RATIOS).default('1:1'),
> 87	  batch: z.number().int().min(1).max(8).default(1),    // 'x1..x8' stepper
> 88	  references: z.array(ReferenceSchema).max(MAX_REFERENCES).default([]),
> 89	  coinCost: z.number().min(0).default(0),              // mcoCoins (server is source of truth)
> 90	  stabilityScore: z.number().min(0).max(1).default(1), // carried from orchestration model
> 91	  status: z.enum(NODE_STATUSES).default('idle'),
> 92	  ports: z.array(PortSchema),
> 93	  params: z.record(z.string(), z.unknown()).default({}),
> 94	  byok: z.boolean().optional(),                        // BR-SPACES-006
> 95	  locked: z.boolean().optional(),                      // node "Lock" action (UI-SPACES-008)
> 96	  headerHidden: z.boolean().optional(),                // "Hide header" action
> 97	  icon: z.string().default('✨'),
> 98	});
> 99	export type SpaceNodeData = z.infer<typeof SpaceNodeDataSchema>;
> 100	
> 101	/* ── @xyflow/react bindings ────────────────────────────────────────────────── */
> 102	export type SpaceNode = Node<SpaceNodeData>;
> 103	export interface SpaceEdgeData extends Record<string, unknown> {
> 104	  dataType: PortDataType; // typed connection (FR-SPACES-004)
> 105	}
> 106	export type SpaceEdge = Edge<SpaceEdgeData>;
> 107	
> 108	/* ── Space + pages (pages verified live — UI-SPACES-003) ───────────────────── */
> 109	export const SpacePageSchema = z.object({
> 110	  id: z.string().uuid(),
> 111	  index: z.number().int().min(0),
> 112	  title: z.string(),                                   // e.g. 'Page 1' / pt-BR
> 113	});
> 114	export type SpacePage = z.infer<typeof SpacePageSchema>;
> 115	
> 116	export interface SpaceEntity {
> 117	  id: string;
> 118	  ownerId: string;          // = auth.uid() (RLS, FR-SPACES-007)
> 119	  title: string;
> 120	  pages: SpacePage[];
> 121	  nodes: SpaceNode[];
> 122	  edges: SpaceEdge[];
> 123	  viewport: Viewport;
> 124	  isTemplate: boolean;
> 125	  createdAt: string;
> 126	  updatedAt: string;
> 127	}
> 128	
> 129	/* ── Generation (cluster card — FR-SPACES-012) ─────────────────────────────── */
> 130	export const GenerationSchema = z.object({
> 131	  id: z.string().uuid(),
> 132	  spaceId: z.string().uuid(),
> 133	  nodeId: z.string(),
> 134	  outputType: z.enum(PORT_DATA_TYPES),
> 135	  assetId: z.string().uuid().optional(),               // cross-space ref (FR-SPACES-009)
> 136	  modelKey: z.string(),
> 137	  mcoCharged: z.number().min(0),                       // BR-SPACES-007
> 138	  mcoRefunded: z.number().min(0).optional(),           // BR-SPACES-004
> 139	  usdCost: z.number().min(0).optional(),
> 140	  latencyMs: z.number().int().min(0).optional(),
> 141	  status: z.enum(NODE_STATUSES),
> 142	  createdAt: z.string(),
> 143	});
> 144	export type Generation = z.infer<typeof GenerationSchema>;
> 145	
> 146	/* ── Canonical Image Generator factory (verified ports) ────────────────────── */
> 147	export function imageGeneratorPorts(): Port[] {
> 148	  return [
> 149	    { id: 'reference', direction: 'in', dataType: 'image', label: 'Referência', referenceKind: 'character' },
> 150	    { id: 'prompt', direction: 'in', dataType: 'text', label: 'Texto' },
> 151	    { id: 'output', direction: 'out', dataType: 'image', label: 'Imagem gerada' },
> 152	  ];
> 153	}
> 154	
> 155	/* ── Runtime guards for the remaining interfaces (Phase 0: z.object for every interface) ───── *
> 156	 * Trace: SD-SPACES-006. The full @xyflow Node/Edge shape is library-owned; we guard OUR data
> 157	 * and use passthrough() so xyflow-internal fields survive validation.                          */
> 158	export const SpaceEdgeDataSchema = z.object({
> 159	  dataType: z.enum(PORT_DATA_TYPES),
> 160	});
> 161	
> 162	export const ViewportSchema = z.object({ x: z.number(), y: z.number(), zoom: z.number() });
> 163	
> 164	export const SpaceNodeGuard = z.object({
> 165	  id: z.string().min(1),
> 166	  type: z.string().optional(),
> 167	  position: z.object({ x: z.number(), y: z.number() }),
> 168	  data: SpaceNodeDataSchema,
> 169	}).passthrough();
> 170	
> 171	export const SpaceEdgeGuard = z.object({
> 172	  id: z.string().min(1),
> 173	  source: z.string(),
> 174	  target: z.string(),
> 175	  sourceHandle: z.string().nullish(),
> 176	  targetHandle: z.string().nullish(),
> 177	  data: SpaceEdgeDataSchema.optional(),
> 178	}).passthrough();
> 179	
> 180	export const SpaceEntitySchema = z.object({
> 181	  id: z.string().uuid(),
> 182	  ownerId: z.string().uuid(),
> 183	  title: z.string(),
> 184	  pages: z.array(SpacePageSchema),
> 185	  nodes: z.array(SpaceNodeGuard),
> 186	  edges: z.array(SpaceEdgeGuard),
> 187	  viewport: ViewportSchema,
> 188	  isTemplate: z.boolean(),
> 189	  createdAt: z.string(),
> 190	  updatedAt: z.string(),
> 191	});
> 192	
> ```

## 🤖 Claude *(18:42:23)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useSpaces.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// useSpaces — Spaces Fase 1a data harness (FR-SPACES-001/003 + PROC-SPACES-006). All server state via
> 2	// TanStack Query; display components render only (Harness Engineering). Execution/ledger is Fase 1b —
> 3	// this layer NEVER touches deduct_mco_coins/canvas-execute (SOP gate G5).
> 4	import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
> 5	import { supabase } from '@/integrations/supabase/client';
> 6	import { useAuth } from '@/hooks/useAuth';
> 7	import {
> 8	  SpaceNodeGuard, SpaceEdgeGuard, ViewportSchema,
> 9	  type SpaceNode, type SpaceEdge, type SpaceEntity, type SpacePage,
> 10	} from '@/lib/spaces-schema';
> 11	import type { Tables } from '@/integrations/supabase/types';
> 12	import type { Viewport } from '@xyflow/react';
> 13	
> 14	export type SpaceRow = Tables<'spaces'>;
> 15	export interface SpaceGraphSnapshot { nodes: SpaceNode[]; edges: SpaceEdge[]; viewport: Viewport }
> 16	
> 17	const DEFAULT_VIEWPORT: Viewport = { x: 0, y: 0, zoom: 1 };
> 18	
> 19	/** Hydration guard (FMEA-SPACES-007): invalid nodes/edges are DROPPED with a warn — the canvas opens
> 20	 *  with the rest, never white-screens (FMEA-SPACES-005: fallback nunca white-screena). */
> 21	export function parseSpaceRow(row: SpaceRow): SpaceEntity {
> 22	  const g = (row.graph ?? {}) as Record<string, unknown>;
> 23	  const nodes: SpaceNode[] = [];
> 24	  for (const n of Array.isArray(g.nodes) ? g.nodes : []) {
> 25	    const p = SpaceNodeGuard.safeParse(n);
> 26	    if (p.success) nodes.push(p.data as unknown as SpaceNode);
> 27	    else console.warn('[spaces] dropped invalid node on hydrate (FMEA-SPACES-007)', p.error.issues[0]);
> 28	  }
> 29	  const edges: SpaceEdge[] = [];
> 30	  for (const e of Array.isArray(g.edges) ? g.edges : []) {
> 31	    const p = SpaceEdgeGuard.safeParse(e);
> 32	    if (p.success) edges.push(p.data as unknown as SpaceEdge);
> 33	    else console.warn('[spaces] dropped invalid edge on hydrate (FMEA-SPACES-007)', p.error.issues[0]);
> 34	  }
> 35	  const vp = ViewportSchema.safeParse(g.viewport);
> 36	  return {
> 37	    id: row.id,
> 38	    ownerId: row.owner_id,
> 39	    title: row.title,
> 40	    pages: (Array.isArray(row.pages) ? row.pages : []) as SpacePage[],
> 41	    nodes,
> 42	    edges,
> 43	    viewport: vp.success ? vp.data : DEFAULT_VIEWPORT,
> 44	    isTemplate: row.is_template,
> 45	    createdAt: row.created_at,
> 46	    updatedAt: row.updated_at,
> 47	  };
> 48	}
> 49	
> 50	export function spaceNodeCount(row: Pick<SpaceRow, 'graph'>): number {
> 51	  const g = (row.graph ?? {}) as Record<string, unknown>;
> 52	  return Array.isArray(g.nodes) ? g.nodes.length : 0;
> 53	}
> 54	
> 55	export function useSpacesList() {
> 56	  const { user } = useAuth();
> 57	  return useQuery({
> 58	    queryKey: ['spaces'],
> 59	    enabled: !!user,
> 60	    queryFn: async (): Promise<SpaceRow[]> => {
> 61	      const { data, error } = await supabase
> 62	        .from('spaces').select('*').order('updated_at', { ascending: false });
> 63	      if (error) throw error;
> 64	      return (data ?? []) as SpaceRow[];
> 65	    },
> 66	  });
> 67	}
> 68	
> 69	export function useSpace(spaceId?: string) {
> 70	  const { user } = useAuth();
> 71	  return useQuery({
> 72	    queryKey: ['space', spaceId],
> 73	    enabled: !!user && !!spaceId,
> 74	    queryFn: async (): Promise<SpaceEntity | null> => {
> 75	      const { data, error } = await supabase
> 76	        .from('spaces').select('*').eq('id', spaceId!).maybeSingle();
> 77	      if (error) throw error;
> 78	      return data ? parseSpaceRow(data as SpaceRow) : null;   // RLS: outro tenant → null → "não encontrado"
> 79	    },
> 80	  });
> 81	}
> 82	
> 83	export function useCreateSpace() {
> 84	  const qc = useQueryClient();
> 85	  const { user } = useAuth();
> 86	  return useMutation({
> 87	    mutationFn: async (title: string): Promise<string> => {
> 88	      if (!user) throw new Error('Sessão expirada — faça login novamente.');
> 89	      const { data, error } = await supabase
> 90	        .from('spaces')
> 91	        .insert({ owner_id: user.id, title: title.trim() || 'Untitled space' })
> 92	        .select('id').single();
> 93	      if (error) throw error;
> 94	      return data.id as string;
> 95	    },
> 96	    onSuccess: () => qc.invalidateQueries({ queryKey: ['spaces'] }),
> 97	  });
> 98	}
> 99	
> 100	/** Strip xyflow-volatile fields before persisting (selection/drag state is session-local). */
> 101	function serializeGraph(s: SpaceGraphSnapshot) {
> 102	  return {
> 103	    nodes: s.nodes.map((n) => ({ ...n, selected: undefined, dragging: undefined, measured: undefined })),
> 104	    edges: s.edges.map((e) => ({ ...e, selected: undefined })),
> 105	    viewport: s.viewport,
> 106	  };
> 107	}
> 108	
> 109	export function useSaveSpaceGraph() {
> 110	  const qc = useQueryClient();
> 111	  return useMutation({
> 112	    mutationFn: async ({ spaceId, snapshot }: { spaceId: string; snapshot: SpaceGraphSnapshot }) => {
> 113	      // Hydration-race guard (FMEA-SPACES-006, mirrors useSaveCanvasGraph): NEVER overwrite a non-empty
> 114	      // saved graph with an empty one — a debounce flush before hydrate would clobber the DB row.
> 115	      if (snapshot.nodes.length === 0) {
> 116	        const { data } = await supabase.from('spaces').select('graph').eq('id', spaceId).maybeSingle();
> 117	        if (data && spaceNodeCount(data as Pick<SpaceRow, 'graph'>) > 0) {
> 118	          console.warn('[spaces] save skipped: empty snapshot over non-empty graph (FMEA-SPACES-006)');
> 119	          return { skipped: true };
> 120	        }
> 121	      }
> 122	      const { error } = await supabase
> 123	        .from('spaces').update({ graph: serializeGraph(snapshot) }).eq('id', spaceId);
> 124	      if (error) throw error;
> 125	      return { skipped: false };
> 126	    },
> 127	    onSuccess: (_r, vars) => {
> 128	      qc.invalidateQueries({ queryKey: ['spaces'] });
> 129	      qc.invalidateQueries({ queryKey: ['space', vars.spaceId] });
> 130	    },
> 131	  });
> 132	}
> 133	
> ```

## 🤖 Claude *(18:42:32)*


## 🤖 Claude *(18:42:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rln \"webhook_token\\|vm_node_type\" /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/ | head; echo ---; grep -rn \"operation_id\" /home/gcrUX/htdocs/constellation-orchestra/src/ | head; echo ---; ls /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/ | grep -iE \"canvas|higgs|poll\"",
  "description": "Find canvas executions migration, client polling usage, related edge functions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040000_viralmind_enums_and_niches.sql
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260516224542_vm_canvas_executions_async_video.sql
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040200_viralmind_canvas_studio.sql
> ---
> /home/gcrUX/htdocs/constellation-orchestra/src/integrations/supabase/types.ts:1337:          operation_id: string | null
> /home/gcrUX/htdocs/constellation-orchestra/src/integrations/supabase/types.ts:1357:          operation_id?: string | null
> /home/gcrUX/htdocs/constellation-orchestra/src/integrations/supabase/types.ts:1377:          operation_id?: string | null
> /home/gcrUX/htdocs/constellation-orchestra/src/integrations/supabase/types.ts:4107:          operation_id: string | null
> /home/gcrUX/htdocs/constellation-orchestra/src/integrations/supabase/types.ts:4134:          operation_id?: string | null
> /home/gcrUX/htdocs/constellation-orchestra/src/integrations/supabase/types.ts:4161:          operation_id?: string | null
> /home/gcrUX/htdocs/constellation-orchestra/src/pages/VideoEditorPage.tsx:86:  operation_id?: string;
> /home/gcrUX/htdocs/constellation-orchestra/src/pages/VideoEditorPage.tsx:293:        .select('status, media_url, operation_id, metadata')
> /home/gcrUX/htdocs/constellation-orchestra/src/pages/VideoEditorPage.tsx:303:        if (data.operation_id && data.status === 'processing') {
> /home/gcrUX/htdocs/constellation-orchestra/src/pages/VideoEditorPage.tsx:304:          console.log(`Detectada operação em curso: [${data.operation_id}]. Retomando monitoramento...`);
> ---
> canvas-execute
> higgsfield-webhook
> video-render-poll
> ```

## 🤖 Claude *(18:42:35)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/lib/billing.ts",
  "limit": 60
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import type { SupabaseClient } from '@supabase/supabase-js';
> 2	
> 3	// mcoCoins cost per operation — single source of truth (frontend).
> 4	//
> 5	// CALIBRATION MODEL (2026-06-03 · OTD-MCOIN-CALIBRATION CLOSED) — derived from REAL provider cost, not round figures.
> 6	// SOP: docs/processes/mcoin-cost-calibration.md.
> 7	//   formula:    mco(op) = ceil( real_cost_usd(op) / USD_PER_MCO_FLOOR × MARGIN )
> 8	//   floor rate: USD_PER_MCO_FLOOR = $0.018/mco — the CHEAPEST sale: Enterprise R$997 / 10000 mco ÷ R$5.5/USD.
> 9	//               (Starter R$147/500 = $0.053/mco and Pro R$397/2000 = $0.036/mco sell DEARER → more margin there.)
> 10	//   margin:     MARGIN = 4× (target gross markup at the worst-case sale price).
> 11	//   FX:         R$5.5/USD assumed; conclusions hold across R$5–7 except IMAGE near R$7 (kept at 4× headroom).
> 12	//
> 13	//   Measured real costs (USD): text llama-3.3-70b ≈ $0.001 (Groq ~free) · DALL·E 3 1024² image = $0.04 ·
> 14	//   orchestrate run (3 texts + 1 image) ≈ $0.04 · Higgsfield DoP 5s video = $0.56 (canvas-execute, validated 4×).
> 15	//   Per-op markup at the floor: ORCHESTRATION_RUN 10 → 4.4× ✓ · canvas video 125 → 4.0× ✓ · canvas image 12 → 5.4× ✓.
> 16	//   ORCHESTRATION_RUN stays a FLAT 10 (bundle): covers 3×CONTENT_GENERATION + IMAGE_GENERATION (sum 15) at a
> 17	//   deliberate bundle discount. Edge fns hardcode their own copies (Deno can't import src/lib) — keep in sync.
> 18	export const COIN_COSTS = {
> 19	  ORCHESTRATION_RUN: 10,   // 3 texts + 1 image, charged flat (bundle discount vs the 15 below). ~4.4× at floor.
> 20	  CONTENT_GENERATION: 2,   // 1 LLM article (~$0.0006). Strict floor is 1; held at 2 as a conservative minimum. (was 5)
> 21	  IMAGE_GENERATION: 9,     // 1 DALL·E 3 1024² image ($0.04 → 4× at floor). WAS 3 = 1.36× (under-margined) → fixed.
> 22	  EMBED_NODE: 1,           // 1 embedding call (~$0.000002). Floor minimum.
> 23	  LEAD_SCORE: 1,           // 1 LLM scoring call (~$0.0005). marketing-hub FR-MH-003 (lead-score edge fn mirrors this).
> 24	  CAMPAIGN_RUN: 10,        // marketing-hub FR-MH-004 — orchestration FEE on top of the cascaded per-step ORCHESTRATION_RUN.
> 25	  NURTURE_DISPATCH: 2,     // marketing-hub FR-MH-008 — 1 LLM message (~$0.0006). nurture-dispatch edge fn mirrors this.
> 26	  RESHAPE_CREATIVE: 2,     // post-engine FR-CP-003 — 1 batched LLM voicing call (~$0.0006) → 4×-floor. Charged ONLY on the
> 27	                           // standalone path; within the (already-charged) pillar/autopilot run the reshape is bundled (no deduct).
> 28	  // avatar-clone-ai Fatia 2 (FR-AC-009 · docs/processes/avatar-voice-credential-resolution.md).
> 29	  // ElevenLabs PVC/IVC ~$0.182/1k chars (Multilingual v2) → 36 mco / ~900 chars EN at 4×-floor. Charged on
> 30	  // synthesize only (clone = free config). Flash/Turbo halves char cost → recalibrate when those tiers ship.
> 31	  // generate-voice edge fn hardcodes its own VOICE_COST mirror (Deno can't import src/lib) — keep in sync.
> 32	  VOICE_GENERATION: 36,
> 33	  // vision-mcp Fatia 2 (sealed grade — docs/processes/vision-mcp-cost-calibration.md, OTD-VM-004).
> 34	  // Mirrored from packages/vision-mcp-core/src/infra/billing.ts COIN_COSTS (G3 triple-mirror gate).
> 35	  // Charged on the PLATFORM-key path only; per-user BYOK runs free; Sovereign exempt (FR-VM-006).
> 36	  VISION_DESCRIBE_IMAGE: 2,      // VLM ~$0.0004/img (Gemini Flash) → 4×-floor
> 37	  VISION_ANALYZE_VIDEO: 2,       // per minute (Gemini video @1FPS ~$0.0054/min)
> 38	  VISION_OCR: 1,                 // per page (Mistral OCR ~$0.002)
> 39	  VISION_DETECT: 2,              // Gemini native boxes
> 40	  DEEPSEARCH_SCRAPE: 1,          // Firecrawl (~$0.0006/pág Growth)
> 41	  DEEPSEARCH_RUN: 3,             // deepsearch orchestration
> 42	  MESH_CONSOLIDATE_REFERENCE: 1, // mesh write (embedding async ~free)
> 43	  // video-studio Fatia 1 (PROVISIONAL — OTD-VS-007 · docs/bok/video-studio/05-sdd.md §4.4 4×-floor).
> 44	  // Calibrate against REAL cost at the first PAID render (slice 2), then seal. Edge fns mirror these copies.
> 45	  VIDEO_FACELESS_RENDER: 125,    // faceless E2E pipeline (n8n Gemini→Pollinations→VoxCPM→Remotion→LTX→FFmpeg→QA) ≈ canvas DoP video
> 46	  VIDEO_HYPERFRAMES_RENDER: 12,  // deterministic HTML→MP4 via headless Chrome (no AI legs) ≈ canvas image class
> 47	} as const;
> 48	
> 49	export type CoinOperation = keyof typeof COIN_COSTS;
> 50	
> 51	/**
> 52	 * Deducts mcoCoins from the authenticated user's profile.
> 53	 * Calls the `deduct_mco_coins` SECURITY DEFINER RPC which enforces
> 54	 * the balance check atomically in the database.
> 55	 * Throws if balance is insufficient or the RPC fails.
> 56	 */
> 57	export async function deductMcoCoins(
> 58	  supabase: SupabaseClient,
> 59	  userId: string,
> 60	  amount: number,
> ```

## 🤖 Claude *(18:42:43)*


## 🤖 Claude *(18:42:46)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"vm_node_type\\|webhook_token\\|operation_id\\|CREATE TYPE\" /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040000_viralmind_enums_and_niches.sql /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260516224542_vm_canvas_executions_async_video.sql | head -30; echo ===; grep -n \"AS ENUM\" -A3 /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040000_viralmind_enums_and_niches.sql | head -40",
  "description": "Inspect vm_node_type enum and webhook_token migration"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260516224542_vm_canvas_executions_async_video.sql:9:  ADD COLUMN IF NOT EXISTS operation_id         TEXT,
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260516224542_vm_canvas_executions_async_video.sql:10:  ADD COLUMN IF NOT EXISTS webhook_token        TEXT NOT NULL DEFAULT (replace(gen_random_uuid()::text, '-', '') || replace(gen_random_uuid()::text, '-', '')),
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260516224542_vm_canvas_executions_async_video.sql:20:CREATE UNIQUE INDEX IF NOT EXISTS idx_vm_canvas_executions_webhook_token
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260516224542_vm_canvas_executions_async_video.sql:21:  ON public.vm_canvas_executions(webhook_token);
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260516224542_vm_canvas_executions_async_video.sql:25:  ON public.vm_canvas_executions(operation_id, status, started_at)
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260516224542_vm_canvas_executions_async_video.sql:26:  WHERE status IN ('queued','running') AND operation_id IS NOT NULL;
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040000_viralmind_enums_and_niches.sql:13:    CREATE TYPE vm_platform AS ENUM (
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040000_viralmind_enums_and_niches.sql:22:    CREATE TYPE vm_content_type AS ENUM (
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040000_viralmind_enums_and_niches.sql:31:    CREATE TYPE vm_content_status AS ENUM (
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040000_viralmind_enums_and_niches.sql:40:    CREATE TYPE vm_affiliate_network AS ENUM (
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040000_viralmind_enums_and_niches.sql:49:  IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'vm_node_type') THEN
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040000_viralmind_enums_and_niches.sql:50:    CREATE TYPE vm_node_type AS ENUM (
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040000_viralmind_enums_and_niches.sql:60:    CREATE TYPE vm_credit_operation AS ENUM (
> ===
> 13:    CREATE TYPE vm_platform AS ENUM (
> 14-      'tiktok', 'instagram', 'youtube', 'youtube_shorts',
> 15-      'facebook', 'pinterest', 'twitter', 'linkedin', 'threads'
> 16-    );
> --
> 22:    CREATE TYPE vm_content_type AS ENUM (
> 23-      'image', 'video', 'carousel', 'story', 'reel',
> 24-      'short', 'post_text', 'ad_creative'
> 25-    );
> --
> 31:    CREATE TYPE vm_content_status AS ENUM (
> 32-      'draft', 'generating', 'ready', 'scheduled',
> 33-      'published', 'failed', 'archived'
> 34-    );
> --
> 40:    CREATE TYPE vm_affiliate_network AS ENUM (
> 41-      'amazon', 'hotmart', 'monetizze', 'eduzz', 'impact',
> 42-      'shareasale', 'clickbank', 'rakuten', 'cj_affiliate',
> 43-      'awin', 'mercadolivre', 'custom'
> --
> 50:    CREATE TYPE vm_node_type AS ENUM (
> 51-      'generate_image', 'generate_video', 'upscale', 'inpaint',
> 52-      'outpaint', 'style_transfer', 'relight', 'remove_background',
> 53-      'extend', 'remix', 'compose', 'export'
> --
> 60:    CREATE TYPE vm_credit_operation AS ENUM (
> 61-      'credit_grant', 'credit_purchase', 'credit_consume',
> 62-      'credit_refund', 'credit_expire', 'credit_bonus'
> 63-    );
> ```

## 🤖 Claude *(18:42:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"useCanvasJobsRealtime\\|onUpdate\\|reconcile\\|poll\" /home/gcrUX/htdocs/constellation-orchestra/src/pages/CanvasEditorPage.tsx | head -20; echo ===; grep -rn \"verify_jwt\\|canvas-execute\" /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml | head",
  "description": "Check editor realtime wiring and edge fn config"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 26:import { useCanvasJobsRealtime } from "@/hooks/useCanvasJobsRealtime";
> 98:        const reconciledNodes = state.nodes.map((node) => {
> 149:          useCanvasStore.setState({ nodes: reconciledNodes });
> 158:    const reconciledNodes = (graph.nodes ?? []).map((node) => {
> 190:      nodes: reconciledNodes,
> 262:  // we reconcile the Zustand store so the canvas node UI updates without refresh.
> 263:  useCanvasJobsRealtime(projectId, (row) => {
> ===
> /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml:7:verify_jwt = false
> /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml:9:verify_jwt = false
> /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml:11:verify_jwt = false
> /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml:13:verify_jwt = false
> /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml:15:verify_jwt = false
> /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml:17:verify_jwt = false
> /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml:19:verify_jwt = false
> /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml:21:verify_jwt = false
> /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml:23:verify_jwt = false
> /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml:25:verify_jwt = false
> ```

## 🤖 Claude *(18:42:55)*


## 🤖 Claude *(18:42:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n -B1 \"verify_jwt\" /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml | grep -A1 -E \"canvas|higgsfield\" ",
  "description": "Check verify_jwt for canvas-execute and higgsfield-webhook"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 82-[functions.higgsfield-webhook]
> 83:verify_jwt = false
> ```

## 🤖 Claude *(18:42:57)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CanvasEditorPage.tsx",
  "offset": 255,
  "limit": 70
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 255	    pipelineStatus,
> 256	    runPipeline,
> 257	    runnableCount,
> 258	    runAllCost,
> 259	  } = useCanvasPipeline({ projectId, refetchDashboard });
> 260	
> 261	  // Phase 4.2c — Realtime bridge: webhook flips vm_canvas_executions.status,
> 262	  // we reconcile the Zustand store so the canvas node UI updates without refresh.
> 263	  useCanvasJobsRealtime(projectId, (row) => {
> 264	    if (!row.node_id) return;
> 265	    if (row.status === "success") {
> 266	      updateNodeData(row.node_id, {
> 267	        status: "success",
> 268	        output: {
> 269	          videoUrl: row.output_url ?? undefined,
> 270	          imageUrl: row.output_url ?? undefined,
> 271	          generatedAt: row.completed_at ?? new Date().toISOString(),
> 272	        },
> 273	        error: undefined,
> 274	      });
> 275	      refetchDashboard?.();
> 276	    } else if (
> 277	      row.status === "failed" ||
> 278	      row.status === "timeout" ||
> 279	      row.status === "cancelled"
> 280	    ) {
> 281	      updateNodeData(row.node_id, {
> 282	        status: "failed",
> 283	        error: row.error_message ?? row.status,
> 284	      });
> 285	    } else if (row.status === "queued" || row.status === "running") {
> 286	      updateNodeData(row.node_id, { status: "running" });
> 287	    }
> 288	  });
> 289	
> 290	  return (
> 291	    <>
> 292	      <TopBar
> 293	        name={project?.name ?? "Sem título"}
> 294	        onRename={(name) => {
> 295	          if (projectId) updateProject.mutate({ projectId, name });
> 296	        }}
> 297	        saving={autoSave.status === "saving"}
> 298	        onSaveNow={() => autoSave.saveNow()}
> 299	        onRunAll={runPipeline}
> 300	        pipelineStatus={pipelineStatus}
> 301	        runnableCount={runnableCount}
> 302	        runAllCost={runAllCost}
> 303	        runAllDisabled={!projectId}
> 304	      />
> 305	
> 306	      <div className="flex min-h-0 flex-1">
> 307	        <LeftPanel projectId={projectId} />
> 308	
> 309	        <div className="relative flex-1 min-w-0">
> 310	          <ReactFlow
> 311	            nodes={nodes}
> 312	            edges={edges}
> 313	            onNodesChange={onNodesChange}
> 314	            onEdgesChange={onEdgesChange}
> 315	            onConnect={onConnect}
> 316	            onNodeClick={onNodeClick}
> 317	            onPaneClick={() => selectNode(null)}
> 318	            onMoveEnd={(_, vp) => setViewport(vp)}
> 319	            nodeTypes={nodeTypes}
> 320	            edgeTypes={edgeTypes}
> 321	            defaultViewport={project?.viewport ?? { x: 0, y: 0, zoom: 1 }}
> 322	            snapToGrid={pipelineMode}
> 323	            snapGrid={[COL_WIDTH, LANE_HEIGHT]}
> 324	            deleteKeyCode={["Backspace", "Delete"]}
> ```

## 🤖 Claude *(18:43:04)*


## 🤖 Claude *(18:43:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"canvas-execute\" /home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml; echo \"exit=$?\"; echo ===; grep -rln \"vm_canvas_executions\" /home/gcrUX/htdocs/constellation-orchestra/scripts/ /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/ 2>/dev/null; echo ===; grep -rn \"magic_prompt\" /home/gcrUX/htdocs/constellation-orchestra/src/ | head -10",
  "description": "Check config.toml, watchdog pollers, magic_prompt client usage"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> exit=1
> ===
> /home/gcrUX/htdocs/constellation-orchestra/scripts/seed-viral-daily-canvas-bok-seal.ts
> /home/gcrUX/htdocs/constellation-orchestra/scripts/canvas-campaign-build.ts
> /home/gcrUX/htdocs/constellation-orchestra/scripts/nightly-stage2-deep-sleep.sh
> /home/gcrUX/htdocs/constellation-orchestra/scripts/sync-canvas-nodes.ts
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/aios-sql-bridge/whitelist.ts
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/higgsfield-webhook/index.ts
> /home/gcrUX/htdocs/constellation-orchestra/scripts/canvas-video-watchdog.sh
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/canvas-execute/index.ts
> ===
> /home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/RightPanel/inspectors/GenerateImageInspector.tsx:113:        node_type: "magic_prompt",
> /home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/RightPanel/inspectors/ImageToVideoInspector.tsx:77:        node_type: "magic_prompt",
> /home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/RightPanel/inspectors/SceneComposeInspector.tsx:104:        node_type: "magic_prompt",
> ```

## 🤖 Claude *(18:43:14)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "head -80 /home/gcrUX/htdocs/constellation-orchestra/scripts/canvas-video-watchdog.sh; echo ===; sed -n '60,140p' /home/gcrUX/htdocs/constellation-orchestra/src/components/canvas/RightPanel/inspectors/GenerateImageInspector.tsx",
  "description": "Read video watchdog script and magic prompt inspector call"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> #!/bin/bash
> # canvas-video-watchdog — defense-in-depth poll for Higgsfield video jobs (Phase 4.2c)
> #
> # Cron: */5 * * * * /home/gcrUX/htdocs/constellation-orchestra/scripts/canvas-video-watchdog.sh
> #       >> /var/log/mcorch-canvas-watchdog.log 2>&1
> #
> # Picks up `vm_canvas_executions` rows that are still queued/running after 10 min
> # (webhook missed or delayed). Polls Higgsfield request status_url and resolves:
> #   - completed → POST the webhook URL manually (idempotent via webhook_token + status 409)
> #   - failed/nsfw/cancelled → PATCH row to status='failed' + error_message
> #   - still queued/in_progress, started_at > 60 min → PATCH status='timeout' (no deduct)
> #
> # SOP: docs/processes/canvas-video-async-execution.md § Recovery path
> # Pattern source: scripts/watchdog-mcorch.sh + scripts/auto-publish-cron.sh
> 
> set -uo pipefail
> 
> # Log target — when invoked via cron the line `>> /var/log/mcorch-canvas-watchdog.log`
> # captures stdout. Standalone runs simply print to stdout.
> COMPOSE_DIR="/home/gcrUX/htdocs/constellation-orchestra"
> DATE=$(date '+%Y-%m-%d %H:%M:%S')
> HF_BASE_URL="https://platform.higgsfield.ai"
> STALE_THRESHOLD_MIN=10
> TIMEOUT_THRESHOLD_MIN=60
> 
> log() { echo "[${DATE}] $*"; }
> 
> # ── Load environment ─────────────────────────────────────────────────────────
> if [ -f "${COMPOSE_DIR}/.env" ]; then
>     # shellcheck disable=SC1090
>     set -a; source "${COMPOSE_DIR}/.env"; set +a
> [ -n "${SB_SECRET_KEY:-}" ] && SUPABASE_SERVICE_ROLE_KEY="$SB_SECRET_KEY"
> fi
> 
> # Fall back to the canonical project URL if .env doesn't set SUPABASE_URL.
> SUPABASE_URL="${SUPABASE_URL:-https://bcyvddsykvehvpwstlfa.supabase.co}"
> 
> if [ -z "${SUPABASE_SERVICE_ROLE_KEY:-}" ]; then
>     log "ERROR: SUPABASE_SERVICE_ROLE_KEY not set — aborting"
>     exit 1
> fi
> if [ -z "${HIGGSFIELD_API_KEY:-}" ] || [ -z "${HIGGSFIELD_API_KEY_SECRET:-}" ]; then
>     log "ERROR: HIGGSFIELD_API_KEY / HIGGSFIELD_API_KEY_SECRET not set — aborting"
>     exit 1
> fi
> 
> if ! command -v jq >/dev/null 2>&1; then
>     log "ERROR: jq not found — install with: sudo apt-get install -y jq"
>     exit 1
> fi
> 
> REST="${SUPABASE_URL}/rest/v1"
> AUTH_HEADER="Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}"
> APIKEY_HEADER="apikey: ${SUPABASE_SERVICE_ROLE_KEY}"
> HF_AUTH="Authorization: Key ${HIGGSFIELD_API_KEY}:${HIGGSFIELD_API_KEY_SECRET}"
> 
> # ── Helpers ──────────────────────────────────────────────────────────────────
> write_health() {
>     local STATUS="$1"
>     curl -s -X POST "${REST}/infra_health_logs" \
>         -H "${APIKEY_HEADER}" -H "${AUTH_HEADER}" \
>         -H "Content-Type: application/json" \
>         -d "{\"service\":\"canvas-video-watchdog\",\"status\":\"${STATUS}\"}" \
>         >/dev/null 2>&1
> }
> 
> patch_execution() {
>     local EXEC_ID="$1"
>     local PAYLOAD="$2"  # JSON body
>     curl -s -X PATCH "${REST}/vm_canvas_executions?id=eq.${EXEC_ID}" \
>         -H "${APIKEY_HEADER}" -H "${AUTH_HEADER}" \
>         -H "Content-Type: application/json" \
>         -H "Prefer: return=minimal" \
>         -d "${PAYLOAD}" >/dev/null 2>&1
> }
> 
> # ── Fetch stale in-flight rows ───────────────────────────────────────────────
> STALE_ISO=$(date -u -d "${STALE_THRESHOLD_MIN} minutes ago" +'%Y-%m-%dT%H:%M:%SZ')
> TIMEOUT_ISO=$(date -u -d "${TIMEOUT_THRESHOLD_MIN} minutes ago" +'%Y-%m-%dT%H:%M:%SZ')
> 
> ===
>     models: ["openrouter-gemini-image", "openrouter-flux-pro"],
>   },
>   {
>     provider: "openai",
>     label: "OpenAI",
>     models: ["dall-e-3", "gpt-image-1"],
>   },
>   {
>     provider: "replicate",
>     label: "Replicate",
>     models: ["flux-1.1-pro", "flux-schnell", "sdxl"],
>   },
> ];
> const DEPRECATED_MODEL_IDS: ReadonlySet<ImageModelId> = new Set(["openrouter-dall-e-3"]);
> 
> export function GenerateImageInspector({
>   node,
>   projectId,
>   creditsBalance,
>   onCreditsChanged,
> }: Props) {
>   const updateNodeData = useCanvasStore((s) => s.updateNodeData);
>   const styleSettings = useCanvasStore((s) => s.styleSettings);
>   const edges = useCanvasStore((s) => s.edges);
>   const nodes = useCanvasStore((s) => s.nodes);
>   const execute = useCanvasExecute();
>   const { userKeys } = useUserApiKeys();
>   const info = getImageModelInfo(node.data.modelId);
>   const cost = info.coinCost;
>   const inheritStyle = node.data.inheritStyle ?? true;
> 
>   const finalPromptPreview = useMemo(() => {
>     return compileFinalPrompt(node.data.prompt, styleSettings, inheritStyle);
>   }, [node.data.prompt, styleSettings, inheritStyle]);
>   const insufficient = cost > creditsBalance;
>   const modelDeprecated = DEPRECATED_MODEL_IDS.has(node.data.modelId);
>   // Per-user key gating — vault fallback may still kick in server-side, but
>   // we surface a hint when the user hasn't filled their personal key.
>   const replicateKeyMissing =
>     info.provider === "replicate" && !userKeys?.replicate_api_key;
>   const openrouterKeyMissing =
>     info.provider === "openrouter" && !userKeys?.openrouter_api_key;
>   const openaiKeyMissing =
>     info.provider === "openai" && !userKeys?.openai_api_key;
> 
>   const [isMagicLoading, setIsMagicLoading] = useState(false);
> 
>   const handleMagicPrompt = async (level: "curto" | "medio" | "longo") => {
>     setIsMagicLoading(true);
>     try {
>       const raw = await execute.mutateAsync({
>         project_id: projectId,
>         node_id: node.id,
>         node_type: "magic_prompt",
>         provider: "openrouter",
>         model: "google/gemini-2.5-flash",
>         prompt: node.data.prompt.trim() || "creative image",
>         parameters: {
>           level,
>           target_model: node.data.modelId,
>         },
>       });
>       const result = assertExecuteSuccess(raw as any);
>       if (result && (result as any).enhanced_prompt) {
>         updateNodeData(node.id, { prompt: (result as any).enhanced_prompt });
>         toast.success(`Magic Prompt gerado (${result.credits_charged} 💎)`);
>         onCreditsChanged();
>       } else {
>         throw new Error("Resposta do Magic Prompt não continha o prompt expandido");
>       }
>     } catch (e) {
>       const msg = e instanceof Error ? e.message : String(e);
>       toast.error(msg);
>     } finally {
>       setIsMagicLoading(false);
>     }
>   };
> 
>   const handleExecute = async () => {
>     const payload = resolveExecutePayload(node.data, styleSettings);
>     if (!payload) return;
> ```

## 🤖 Claude *(18:44:21)*


## 🤖 Claude *(18:44:21)*


## 🤖 Claude *(18:45:32)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "findings": "# canvas-execute Edge Function \u2014 Contract Map\n\n## 1. Request payload (`ExecuteRequest`, supabase/functions/canvas-execute/index.ts:76-95)\n\n```ts\n{\n  project_id: string;            // required (index.ts:122)\n  node_id: string;               // required \u2014 ReactFlow node id, echoed to vm_canvas_executions.node_id\n  node_type: string;             // \"generate_image\" | \"scene_compose\" | \"style_transfer\" | \"image_to_video\" | \"magic_prompt\" (+ pass-through)\n  provider: string;              // \"openai\" | \"replicate\" | \"openrouter\" | \"higgsfield\"\n  model: string;                 // provider-native model string (e.g. \"soul\", \"dop-standard\", \"google/gemini-2.5-flash-image\")\n  prompt: string;                // required (index.ts:122)\n  negative_prompt?: string;      // only forwarded to Replicate (index.ts:688)\n  parameters?: Record<string, any>; // size, aspect_ratio, resolution (\"720p\"|\"1080p\"), batch (1|4), duration, motion_strength, level, target_model, seed, controls, strength, preset_id\n  input_asset_url?: string;      // REQUIRED for image_to_video (index.ts:1034-1040 \u2192 400)\n  input_asset_id?: string;       // else resolved by matching vm_canvas_assets.public_url (index.ts:259-272)\n  input_image_1?: string; input_image_2?: string; input_layout?: string; // scene_compose (higgsfield soul/compose, index.ts:910-928)\n  reference_image_urls?: string[]; // Phase 4.3 cross-node consistency; fail-open (index.ts:90-94)\n  seed?: number;                 // Replicate only; also read from parameters.seed (index.ts:698-701)\n}\n```\nClient builder: `resolveExecutePayload()` src/types/canvas.ts:806-894 (maps node `kind` \u2192 `node_type`+provider+model+parameters; `compileFinalPrompt` prepends StyleSettings, canvas.ts:756-798). Caller: `useCanvasExecute()` src/hooks/useCanvasStudio.ts:217-259 (`supabase.functions.invoke(\"canvas-execute\", { body })`; parses non-2xx body via `error.context.json()` for pt-BR message). Orchestration: `useCanvasPipeline.runSingleNode` src/hooks/useCanvasPipeline.ts:69-142 (threads `input_asset_url` from `findUpstreamImage`, `input_image_1/2/layout` from `findUpstreamHandleAsset`, `reference_image_urls` from `findUpstreamImages` for generateImage/styleTransfer). Inspectors call the same mutation directly (GenerateImageInspector.tsx:110-124 for `magic_prompt`; also SceneComposeInspector.tsx:104, ImageToVideoInspector.tsx:77).\n\n## 2. Auth + BYOK\n\n- **User JWT required**: `Authorization` header \u2192 anon-key client \u2192 `supabase.auth.getUser()` (index.ts:101-119, 401 on both misses). canvas-execute is NOT in supabase/config.toml \u2192 platform default `verify_jwt=true`.\n- **Service-role admin client** (`SB_SECRET_KEY`, index.ts:128) does all DB writes/ledger.\n- **BYOK pure per-user, NO env fallback** (index.ts:130-144): reads `decrypted_user_api_keys` by `user_id`: `openai_api_key`, `replicate_api_key`, `openrouter_api_key`, `google_api_key` (Gemini \u2014 NOT `gemini_api_key`), `higgsfield_api_key` + `higgsfield_api_key_secret` (pair). Missing key \u2192 provider fn throws \"X API key not configured\" \u2192 HTTP **200 with `status:\"failed\"`** (sync path) or **500** (video path, index.ts:1027-1032). No 501 anywhere.\n- **Providers per node_type**: `generate_image`/`scene_compose` \u2192 openai | replicate | openrouter | higgsfield-soul (index.ts:444-460); `style_transfer` \u2192 client hardcodes higgsfield/soul (canvas.ts:851-864); `image_to_video` \u2192 higgsfield ONLY (index.ts:426-436); `magic_prompt` \u2192 openrouter `google/gemini-2.5-flash` with Gemini-key fallback via `fetchLLMWithFallback` (index.ts:1176-1195, `_shared/llm-fallback.ts`).\n- **higgsfield-webhook** companion: `verify_jwt=false` (config.toml:82-83); auth = 64-hex `webhook_token` query param, unique index (migration 20260516224542:10,20-21).\n\n## 3. Billing (charge-on-success; no pre-debit, hence no refund RPC)\n\n- Cost table `CREDIT_COSTS` lives IN the edge fn (index.ts:15-44) \u2014 NOT `src/lib/billing.ts` COIN_COSTS (billing.ts only documents canvas video 125/image 12 in calibration comments, billing.ts:14-15). Client mirrors: `MODEL_INFO`/`VIDEO_MODEL_INFO.coinCost` (canvas.ts:96-282), `CLIENT_COST_MIRROR` (useParamRegistry.ts:30-39, display-only).\n- Cost resolution (index.ts:149-162): `magic_prompt` \u2192 level curto=1/medio=2/longo=5; higgsfield soul \u2192 `higgsfield/soul-<res>-<batch>` (720p-1=20, 720p-4=26, 1080p-1=40, 1080p-4=65) via `resolveHiggsfieldSoulKey` (index.ts:68-74); `image_to_video` \u2192 `<provider>/<model>-<duration>s` (dop-lite-5s=30, dop-turbo-5s=90, dop-standard-5s=125, kling-2.1-pro-5s=160, seedance-v1-pro-5s=130); `generate_image` \u2192 `<provider>/<model>` (dall-e-3=15, gpt-image-1=18, flux-1.1-pro=12, sdxl=4, flux-schnell=3, gemini-2.5-flash-image=10); else `node_type.replace(\"_\",\"-\")` (scene-compose=18, style-transfer=14); **unknown \u2192 default 10**.\n- Balance gate: `profiles.mco_balance < cost` \u2192 **402** `{error:\"Insufficient mcoCoins\", required, balance}` (index.ts:164-174).\n- **Daily cap** (SSP-01 OE04, index.ts:176-217): sums `abs(amount)` of `mcoin_transactions` where `action LIKE 'canvas_%spend'` in rolling 24h; cap 100 default / 1000 editor / 10000 admin (from `user_roles`); over \u2192 **402** `{error:\"Daily Canvas cap reached\", cap, spent_today, required, resets_at}`. Fail-open on query error.\n- **Atomic deduct**: `deduct_mco_coins(p_user_id, p_amount, p_action, p_context)` RPC, only AFTER success \u2014 actions `canvas_magic_prompt_spend` (index.ts:375-384), `canvas_image_spend` (index.ts:587-601), `canvas_video_spend` (webhook, higgsfield-webhook/index.ts:282-292 \u2014 only after downloaded video \u2265100KB + content-type video/* + storage upload OK). Failure paths never deduct (\"cr\u00e9dito reembolsado\" messages for nsfw/cancelled are cosmetic \u2014 nothing was charged, webhook:167-175).\n- **Async video accounting**: execution row inserted with `credits_charged` = intent at status `queued` (index.ts:277-296); response `credits_charged` is \"intent, not yet deducted\" (index.ts:1136).\n- Dual-write `register_creative_asset` RPC fail-soft (index.ts:546-561); project stats `total_executions`/`last_execution_at` (index.ts:603-613); `infra_health_logs` service `canvas-execute` on every path.\n\n## 4. Response shapes + error codes + client sync\n\n- **Sync image (200 ALWAYS, even on provider failure)**: `{execution_id, status:\"success\"|\"failed\", output_url, asset_id, credits_charged (0 on fail), credits_remaining, error?}` (index.ts:616-624). Client MUST run `assertExecuteSuccess()` (src/lib/canvas-execute-result.ts:31-44 \u2014 throws on `error` or status failed/timeout/cancelled; `CanvasExecuteResult` interface :14-24).\n- **magic_prompt (200)**: `{execution_id, status:\"success\", enhanced_prompt, credits_charged}` (index.ts:391-399); errors \u2192 500.\n- **Async video (200)**: `{execution_id, status:\"queued\", webhook_token, operation_id, credits_charged, higgsfield_status}` (index.ts:1130-1140).\n- **Error codes**: 401 missing/invalid JWT (:102-119); 400 missing project_id/node_id/prompt (:122-126) or video without input_asset_url (:1036-1040); 402 balance/daily-cap (:169,210); 422 video model not in `ALLOWED_VIDEO_MODELS` = [\"dop-lite\",\"dop-turbo\",\"dop-standard\",\"kling-2.1-pro\",\"seedance-v1-pro\"] (:219-232); 500 execution-insert fail (:300), magic-prompt fail (:416), missing higgsfield creds on video (:1027); 502 higgsfield submit network/HTTP errors (:1087,1100-1107,1112). **No 501.**\n- **Client completion for video**: no polling \u2014 Supabase **Realtime** `postgres_changes` UPDATE on `vm_canvas_executions` filtered `user_id=eq.<uid>` (src/hooks/useCanvasJobsRealtime.ts:34-70); CanvasEditorPage.tsx:263-288 reconciles Zustand node status (`queued|running`\u2192running, `success`\u2192output.videoUrl, `failed|timeout|cancelled`\u2192error). Server-side defense: cron `scripts/canvas-video-watchdog.sh` (*/5min) polls Higgsfield for rows stale >10min, replays webhook (idempotent) or sets `timeout` at 60min, no deduct (watchdog:6-14).\n\n## 5. Supported node types (exact strings)\n\nServer `NODE_TYPE_MAP` \u2192 `vm_node_type` enum (index.ts:237-256; enum = generate_image, generate_video, upscale, inpaint, outpaint, style_transfer, relight, remove_background, extend, remix, compose, export \u2014 migration 20260514040000:50-54). **Actually implemented paths**: `magic_prompt` (index.ts:313-420), `image_to_video` (async, :426-436), `generate_image`, `scene_compose` (higgsfield soul/compose endpoint :899-902; other providers treat as plain generation), `style_transfer` (executed as higgsfield Soul gen). `upscale/inpaint/outpaint/relight/remove_background/extend/remix/export` are enum-mapped but have NO dedicated implementation \u2014 they'd route through the same text-to-image provider fns. Unmapped node_type passes through with a warn (:254-256). Client node kinds (canvas.ts:19-27): generateImage, characterReference (no execute, canvas.ts:881-884), sceneCompose, styleTransfer, imageToVideo, voiceClone (\u2192 `generate-voice` fn, canvas.ts:885-888), avatarIdentity (\u2192 `avatar-identity-train`, gated OTD-AC-017, canvas.ts:889-892).\n\n## 6. execution_id / idempotency\n\n- `execution_id` is **server-generated** (`vm_canvas_executions.id`, insert at index.ts:277-296) and returned in every response \u2014 traceability only; the client CANNOT supply one. **No request-level idempotency key: a double-submit creates two executions and two charges** (client mitigates via `runnable` filter excluding running/queued nodes, useCanvasPipeline.ts:35, and disabled buttons).\n- Async video idempotency is real: per-execution `webhook_token` (unique index, migration 20260516224542:10,20-21); webhook rejects replay with **409** if status not in queued/running (higgsfield-webhook/index.ts:146-151); `operation_id` persisted for watchdog polling (index.ts:1115-1123).\n\n## 7. Gaps / drift found\n\n1. **Spaces registry has ZERO backend support**: `IMAGE_MODELS` 38 keys (spaces-schema.ts:43-53 \u2014 flux.2-*, google-imagen-3/4*, seedream-4/4.5/5-lite, gpt-1.5*, recraft-v4*, krea-2, z-image, qwen, grok, runway, luma-uni-1.1, mystic-2.5-fluid, mai-image-2.5, classic*, 'auto'...) \u2014 NONE exist in `CREDIT_COSTS` and no provider routing exists for them; any would fall to default cost 10 then die at `Unknown provider` (index.ts:459). `useSpaces.ts:2-3` explicitly declares execution = Fase 1b, \"NEVER touches deduct_mco_coins/canvas-execute (SOP gate G5)\". Spaces categories video/audio/text/utility/designer/media/references (spaces-schema.ts:24-27) also have no backend.\n2. **`CLIENT_COST_MIRROR` is out of sync by design-claim violation**: useParamRegistry.ts:27-29 says \"keep in sync with the edge function\", but its model keys (flux.2-pro, google-imagen-4, seedream-4, gpt-1.5, recraft-v4, krea-2, mystic-2.5-fluid...) don't exist server-side; only the op-family keys (upscale-2x/4x, inpaint, remove-background, scene-compose, style-transfer) match CREDIT_COSTS.\n3. **styleTransfer cost drift**: UI shows 14 (`STYLE_TRANSFER_COST`, canvas.ts:360) but the payload (provider=higgsfield, model=soul, resolution=720p, batch=1, canvas.ts:851-864) matches `resolveHiggsfieldSoulKey` first \u2192 server charges `higgsfield/soul-720p-1` = **20** (index.ts:154-161); `CREDIT_COSTS[\"style-transfer\"]=14` is unreachable for this payload.\n4. **Orphaned cost keys**: `upscale-2x`, `upscale-4x` (index.ts:38-39) \u2014 no request shape ever produces these costKeys (`node_type.replace` yields \"upscale\", \u2192 default 10).\n5. **Video duration undercharge**: `VideoDuration = 5|10|15` (canvas.ts:219) but only `-5s` keys exist in CREDIT_COSTS; duration 10 \u2192 costKey `higgsfield/dop-standard-10s` \u2192 miss \u2192 default **10 mco** for a premium video.\n6. **Soul batch is billing-only**: x4 tiers charge 26/65 but `generateHiggsfield` payload never sends a batch/count param (index.ts:904-908) and returns only `images[0].url` (index.ts:972) \u2014 user pays 4x tier, receives 1 image.\n7. `negative_prompt` silently ignored by openai/openrouter/higgsfield (only Replicate, index.ts:688); `seed` only honored by Replicate; `reference_image_urls` ignored by OpenAI and by the video path.\n8. Cost-computation trusts client `provider`/`model` strings for the lookup \u2014 a mismatched pair (e.g. provider=openrouter model=flux-schnell) prices at default 10 regardless of true provider cost.",
  "gaps": [
    "Spaces Fase 1b execution layer does not exist: spaces-schema IMAGE_MODELS (38 keys, src/lib/spaces-schema.ts:43-53) and node categories video/audio/text/utility/designer have no canvas-execute provider routing or CREDIT_COSTS entries; useSpaces.ts:2-3 gates this behind SOP G5",
    "CLIENT_COST_MIRROR (src/hooks/useParamRegistry.ts:30-39) claims to mirror canvas-execute CREDIT_COSTS but its model keys (flux.2-pro, google-imagen-4, seedream-4, gpt-1.5, recraft-v4, krea-2...) do not exist server-side",
    "styleTransfer client/server cost drift: UI estimates 14 (STYLE_TRANSfer_COST canvas.ts:360) but server charges 20 via higgsfield/soul-720p-1 tier because resolveHiggsfieldSoulKey wins the cost lookup (index.ts:154-161)",
    "Video duration 10s/15s (VideoDuration type canvas.ts:219) has no CREDIT_COSTS key \u2192 falls to default 10 mco (undercharge vs 125 for 5s dop-standard)",
    "Higgsfield Soul batch=4 tiers charge 26/65 mco but the submit payload sends no batch param and only images[0] is returned (index.ts:904-908,972) \u2014 paid batch not delivered",
    "No request-level idempotency: execution_id is server-generated; double-submit = double execution + double charge (only client-side UI guards)",
    "upscale/inpaint/outpaint/relight/remove_background/extend/remix/export are NODE_TYPE_MAP-mapped but have no dedicated implementation \u2014 they route through generic provider text-to-image fns; upscale-2x/4x cost keys are unreachable",
    "No 501 error code exists despite the API Tenancy Model prescribing structured 402/501 for unconfigured credentials \u2014 missing BYOK key surfaces as HTTP 200 status:'failed' (sync) or 500 (video)",
    "vm_canvas_executions status 'timeout' is set only by the external watchdog cron (scripts/canvas-video-watchdog.sh), not by any edge function \u2014 deploy environments without the cron will strand queued rows if the webhook is missed"
  ],
  "keyRefs": [
    "supabase/functions/canvas-execute/index.ts:76-95 (ExecuteRequest payload shape)",
    "supabase/functions/canvas-execute/index.ts:15-44 (CREDIT_COSTS server cost authority)",
    "supabase/functions/canvas-execute/index.ts:149-162 (cost-key resolution incl. resolveHiggsfieldSoulKey)",
    "supabase/functions/canvas-execute/index.ts:164-217 (402 balance gate + role-based daily cap)",
    "supabase/functions/canvas-execute/index.ts:130-144 (pure per-user BYOK from decrypted_user_api_keys, no env fallback)",
    "supabase/functions/canvas-execute/index.ts:237-256 (NODE_TYPE_MAP \u2192 vm_node_type enum)",
    "supabase/functions/canvas-execute/index.ts:616-624 (sync response shape \u2014 HTTP 200 even on provider failure)",
    "supabase/functions/canvas-execute/index.ts:1005-1141 (submitHiggsfieldVideo async branch + queued response)",
    "supabase/functions/higgsfield-webhook/index.ts:146-151,282-292 (409 idempotency + deduct-after-upload)",
    "src/types/canvas.ts:806-894 (resolveExecutePayload \u2014 node kind \u2192 request body)",
    "src/hooks/useCanvasStudio.ts:217-259 (useCanvasExecute mutation)",
    "src/hooks/useCanvasPipeline.ts:69-142 (runSingleNode \u2014 reference/input threading)",
    "src/hooks/useCanvasJobsRealtime.ts:34-70 + src/pages/CanvasEditorPage.tsx:263-288 (Realtime subscribe + Zustand reconcile)",
    "src/lib/canvas-execute-result.ts:14-44 (CanvasExecuteResult + assertExecuteSuccess)",
    "src/lib/spaces-schema.ts:43-53 + src/hooks/useParamRegistry.ts:30-39 + src/hooks/useSpaces.ts:2-3 (Spaces registry with no backend)",
    "supabase/migrations/20260516224542_vm_canvas_executions_async_video.sql:9-26 (operation_id + webhook_token unique index)",
    "scripts/canvas-video-watchdog.sh:1-14 (stale-job recovery cron)"
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
> * **Sessão Anterior**: [[2026-07-02 - agent-a4b225217e4334389]]
> * **Próxima Sessão**: [[2026-07-02 - agent-a5a79c320e0997619]]
%% --- TIMELINE END --- %%

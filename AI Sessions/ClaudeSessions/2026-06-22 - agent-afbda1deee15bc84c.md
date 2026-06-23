# Session agent-afbda1deee15bc84c
**Date:** 2026-06-22 | **Session ID:** `agent-afbda1deee15bc84c`

---

## 👤 User *(14:03:22)*

Senior security review of TWO new Supabase Deno edge functions in /home/gcrUX/htdocs/constellation-orchestra. Focus ONLY on HIGH-confidence (>80%) NEW vulnerabilities. Read both files in full:
- supabase/functions/video-render/index.ts
- supabase/functions/video-render-poll/index.ts

Both are config'd verify_jwt=false and do auth in-code. Context (verified facts — treat as ground truth):
- deduct_mco_coins(p_user_id, p_amount, ...): SECURITY DEFINER, GRANT to authenticated+service_role; Guard: non-service_role caller may only deduct from auth.uid()=p_user_id (42501); positive-amount guard; service_role EXEMPT. Called here via the service-role `admin` client → allowed, charges p_user_id.
- add_mco_coins(uuid, integer): service_role-only (refund credit).
- finalize_video_render(p_render_id,p_state,p_storage_key,p_qa,p_node_id,p_refund): service_role-only, atomic terminal+refund, idempotent guard state IN (queued,running,qa_gate), refunded_mco<=charged_mco CHECK.
- video_renders RLS: SELECT own-or-active-org-member; NO insert/update policy for authenticated (service-role writes only); RESTRICTIVE no-delete.
- decrypted_user_api_keys: service-role-only masked-Vault view (BYOK).

Scrutinize specifically:
1. AuthZ: can a caller charge or read on behalf of ANOTHER user? In video-render, userId comes from getUser() on the caller's JWT (not from body) — confirm body cannot override identity. The deduct uses p_user_id=userId (the authenticated caller) → a user can only charge themselves. Confirm no IDOR.
2. video-render-poll: it runs the SELECT under the USER client (anon key + caller JWT) so RLS binds it — confirm a foreign render_id cannot be read (returns 404), and that it never uses the service client to bypass RLS for the read.
3. Charge/refund integrity: on insert failure after deduct, it refunds via add_mco_coins (full cost, no render_id). On worker-trigger failure after deduct+insert, it refunds via finalize_video_render(...,p_refund:cost). Any double-refund or charge-without-refund path? Any path that charges then returns success without a render? Any path that creates a render without charging?
4. BYOK: faceless reads decrypted_user_api_keys for the AUTHENTICATED userId only (not a body-supplied id) — confirm no cross-tenant key read. The key VALUE is only existence-checked, never returned to the client — confirm not leaked in any response.
5. Secret/PII leakage in responses or logs: does any response or infra_health_logs insert include secrets, tokens, or PII? (logHealth writes service/status/event only — confirm.)
6. Input validation that has security impact (not nitpicks): engine whitelist, render_id uuid check in poll.
7. SLICE-1 note: video-render returns 503 before deduct when the worker webhook env is unset, so the prepaid path is currently dormant — but review it as if it will activate (slice 2 sets the env).

Env vars are trusted. Exclude DoS, rate-limiting, lack-of-hardening nits, theoretical races, markdown. Output each finding: file:line, Severity (HIGH/MEDIUM), Category, Description, Exploit Scenario, Fix, Confidence(1-10). If nothing >=8, say so explicitly with a one-line rationale per vector checked.

## 🤖 Claude *(14:03:25)*

I'll start by reading both edge functions in full.

## 🤖 Claude *(14:03:26)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// video-render — video-studio render submit (FR-VS-001/005/009/014/032). verify_jwt=false (auth in-code).
> 2	// BoK SSOT: docs/bok/video-studio/05-sdd.md §3.1 (UI→Hook→Edge contract) + 04-frd.md (FR-VS-009 charge-at-entry,
> 3	//           FR-VS-011 refund, FR-VS-032 voice consent). SOP: 07-process-flow.md PROC-VS-001/004.
> 4	//
> 5	// CONTRACT (charge-at-entry + refund-on-failure): JWT verify → engine validate → voice-consent gate →
> 6	//   BYOK resolve fail-closed → [dry_run short-circuit] → worker-availability gate → deduct_mco_coins →
> 7	//   INSERT video_renders(queued) via service key → trigger worker → 202 {render_id}. 401/409/402/503 NEVER
> 8	//   charge. A trigger failure AFTER deduct refunds idempotently via finalize_video_render.
> 9	//
> 10	// SLICE 1 (this): the render worker is NOT wired yet (faceless = n8n bridge OTD-VS-001 / hyperframes = sandbox
> 11	//   OTD-VS-006), so the engine-availability gate returns 503 BEFORE any deduct — nobody pays for a render that
> 12	//   cannot run. Everything up to that gate is provable zero-cost (401/422/409/402/dry_run). SLICE 2 sets the
> 13	//   worker webhook env → the prepaid path below activates unchanged.
> 14	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 15	
> 16	const corsHeaders = {
> 17	  "Access-Control-Allow-Origin": "*",
> 18	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 19	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> 20	};
> 21	
> 22	// Mirror of src/lib/billing.ts COIN_COSTS (Deno can't import src/lib — keep in sync; OTD-VS-007 provisional).
> 23	const COST = { faceless: 125, hyperframes: 12 } as const;
> 24	type Engine = keyof typeof COST;
> 25	
> 26	Deno.serve(async (req) => {
> 27	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 28	  const json = (b: unknown, s = 200) =>
> 29	    new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 30	
> 31	  const url = Deno.env.get("SUPABASE_URL")!;
> 32	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 33	  const pubKey = (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!;
> 34	  const admin = createClient(url, serviceKey);
> 35	  const logHealth = (status: string, event?: string) =>
> 36	    admin.from("infra_health_logs").insert({ service: "video-render", status, event }).then(() => {}, () => {});
> 37	
> 38	  try {
> 39	    const authHeader = req.headers.get("Authorization");
> 40	    if (!authHeader?.startsWith("Bearer ")) return json({ error: "Unauthorized" }, 401);
> 41	
> 42	    // Identity: user JWT (this is a user-initiated submit). getUser rejects an invalid/forged token.
> 43	    const userClient = createClient(url, pubKey, { global: { headers: { Authorization: authHeader } } });
> 44	    const { data: { user }, error: authErr } = await userClient.auth.getUser();
> 45	    if (authErr || !user) return json({ error: "Unauthorized" }, 401);
> 46	    const userId = user.id;
> 47	
> 48	    const body = await req.json().catch(() => ({}));
> 49	    const engine = body?.engine as Engine | undefined;
> 50	    if (engine !== "faceless" && engine !== "hyperframes") {
> 51	      return json({ error: "engine_invalid", detail: "engine deve ser 'faceless' ou 'hyperframes'" }, 422);
> 52	    }
> 53	    const dryRun = body?.dry_run === true;
> 54	    const voiceConsent = body?.voice_consent === true;
> 55	    const topic = typeof body?.topic === "string" ? body.topic.slice(0, 500) : null;
> 56	    const productId = typeof body?.product_id === "string" ? body.product_id : null;
> 57	
> 58	    // Voice-consent gate (FR-VS-032): faceless clones a voice (VoxCPM) → identifiable biometric (LGPD Art. 11).
> 59	    if (engine === "faceless" && !voiceConsent) {
> 60	      return json({ error: "voice_consent_required", action: "Confirme o consentimento de uso de voz para gerar o vídeo faceless." }, 409);
> 61	    }
> 62	
> 63	    // BYOK fail-closed (FR-VS-005/006): faceless needs the tenant's Gemini key (director + vision QA). Per-user
> 64	    // first; NO silent global fallback in a user-facing path (API Tenancy Model). hyperframes is deterministic (no AI leg).
> 65	    if (engine === "faceless") {
> 66	      const { data: keys } = await admin
> 67	        .from("decrypted_user_api_keys").select("gemini_api_key").eq("user_id", userId).maybeSingle();
> 68	      if (!keys?.gemini_api_key) {
> 69	        return json({ error: "gemini_not_configured", action: "Configure sua chave Gemini em /dashboard/settings para gerar vídeo." }, 402);
> 70	      }
> 71	    }
> 72	
> 73	    const cost = COST[engine];
> 74	
> 75	    // dry_run: cost projection WITHOUT deduct or row (zero-cost proof path; mirrors autopilot-run).
> 76	    if (dryRun) return json({ ok: true, dry_run: true, engine, cost_mco: cost });
> 77	
> 78	    // Engine-availability gate (SLICE 1): the worker webhook is unset until slice 2 wires the render engine.
> 79	    // Returning 503 HERE — before any deduct — guarantees no tenant is charged for a render that cannot complete.
> 80	    const workerWebhook = engine === "faceless"
> 81	      ? Deno.env.get("VIDEO_FACELESS_WEBHOOK")
> 82	      : Deno.env.get("VIDEO_HYPERFRAMES_WEBHOOK");
> 83	    if (!workerWebhook) {
> 84	      return json({
> 85	        error: "render_engine_unavailable",
> 86	        detail: `O motor de render '${engine}' entra na Fatia 2 (faceless: ponte de rede + n8n; hyperframes: sandbox). Nenhum mcoCoin foi debitado.`,
> 87	      }, 503);
> 88	    }
> 89	
> 90	    // ── SLICE 2 prepaid path (activates once the worker webhook env is set) ──────────────────────────────────────
> 91	    // Charge-at-entry (FR-VS-009): atomic deduct BEFORE any leg. 402 if balance < cost (zero rows created).
> 92	    const { error: deductErr } = await admin.rpc("deduct_mco_coins", { p_user_id: userId, p_amount: cost });
> 93	    if (deductErr) {
> 94	      logHealth("degraded", "insufficient_balance");
> 95	      return json({ error: "insufficient_balance", detail: `Saldo insuficiente: render '${engine}' custa ${cost} mcoCoins.`, cost_mco: cost }, 402);
> 96	    }
> 97	
> 98	    // INSERT the queued render (service key — RLS denies tenant writes; this is the only writer). org_id/client_id
> 99	    // NULL = solo creator (§AG agency scoping wires in a later slice).
> 100	    const { data: render, error: insErr } = await admin
> 101	      .from("video_renders")
> 102	      .insert({ user_id: userId, engine, topic, product_id: productId, voice_consent: voiceConsent, charged_mco: cost, state: "queued" })
> 103	      .select("id").single();
> 104	    if (insErr || !render) {
> 105	      // Could not even create the ledger row → refund the just-charged cost (no render_id yet → direct credit).
> 106	      await admin.rpc("add_mco_coins", { p_user_id: userId, p_amount: cost }).then(() => {}, () => {});
> 107	      logHealth("error", "insert_failed");
> 108	      return json({ error: "render_create_failed", detail: insErr?.message }, 500);
> 109	    }
> 110	    const renderId = render.id as string;
> 111	
> 112	    // Trigger the worker. On failure AFTER the charge, refund idempotently via the terminal authority.
> 113	    try {
> 114	      const r = await fetch(workerWebhook, {
> 115	        method: "POST",
> 116	        headers: { Authorization: `Bearer ${serviceKey}`, "Content-Type": "application/json" },
> 117	        body: JSON.stringify({ render_id: renderId, user_id: userId, engine, topic, product_id: productId }),
> 118	      });
> 119	      if (!r.ok) throw new Error(`worker HTTP ${r.status}`);
> 120	    } catch (e) {
> 121	      await admin.rpc("finalize_video_render", {
> 122	        p_render_id: renderId, p_state: "failed", p_storage_key: null, p_qa: null, p_node_id: null, p_refund: cost,
> 123	      }).then(() => {}, () => {});
> 124	      logHealth("error", "worker_trigger_failed");
> 125	      return json({ error: "worker_unavailable", detail: e instanceof Error ? e.message : "trigger failed", render_id: renderId }, 502);
> 126	    }
> 127	
> 128	    logHealth("healthy", "render_submitted");
> 129	    return json({ ok: true, render_id: renderId, engine, charged_mco: cost, state: "queued" }, 202);
> 130	  } catch (e) {
> 131	    logHealth("error", "exception");
> 132	    return json({ error: e instanceof Error ? e.message : "unknown" }, 500);
> 133	  }
> 134	});
> 135	
> ```

## 🤖 Claude *(14:03:26)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render-poll/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// video-render-poll — video-studio render status poll (FR-VS-024). verify_jwt=false (auth in-code). Cost 0.
> 2	// BoK SSOT: docs/bok/video-studio/05-sdd.md §3.1 (poll leg) + 06-data-model.md §2.1 (poll-able render state).
> 3	//
> 4	// Tenant-bound by RLS: the SELECT runs under the USER client (anon key + the caller's JWT), so the RLS SELECT
> 5	// policy (own OR active org member) is enforced — another tenant's render_id returns no row → 404. The poll
> 6	// never mutates and never charges. Signed-URL minting of the finished asset lands with the asset/bucket slice.
> 7	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 8	
> 9	const corsHeaders = {
> 10	  "Access-Control-Allow-Origin": "*",
> 11	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 12	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> 13	};
> 14	const UUID_RE = /^[0-9a-fA-F-]{36}$/;
> 15	
> 16	Deno.serve(async (req) => {
> 17	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 18	  const json = (b: unknown, s = 200) =>
> 19	    new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 20	
> 21	  const url = Deno.env.get("SUPABASE_URL")!;
> 22	  const pubKey = (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!;
> 23	
> 24	  try {
> 25	    const authHeader = req.headers.get("Authorization");
> 26	    if (!authHeader?.startsWith("Bearer ")) return json({ error: "Unauthorized" }, 401);
> 27	
> 28	    const body = await req.json().catch(() => ({}));
> 29	    const renderId = typeof body?.render_id === "string" ? body.render_id : null;
> 30	    if (!renderId || !UUID_RE.test(renderId)) return json({ error: "render_id (uuid) required" }, 422);
> 31	
> 32	    // USER client → RLS enforces tenant-binding (own or active-org-member). Forged/foreign id → no row → 404.
> 33	    const userClient = createClient(url, pubKey, { global: { headers: { Authorization: authHeader } } });
> 34	    const { data: { user }, error: authErr } = await userClient.auth.getUser();
> 35	    if (authErr || !user) return json({ error: "Unauthorized" }, 401);
> 36	
> 37	    const { data: render, error } = await userClient
> 38	      .from("video_renders")
> 39	      .select("id, engine, state, charged_mco, refunded_mco, storage_key, qa, node_id, expires_at, created_at")
> 40	      .eq("id", renderId)
> 41	      .maybeSingle();
> 42	    if (error) return json({ error: "poll_failed", detail: error.message }, 500);
> 43	    if (!render) return json({ error: "render_not_found" }, 404);
> 44	
> 45	    return json({ ok: true, render });
> 46	  } catch (e) {
> 47	    return json({ error: e instanceof Error ? e.message : "unknown" }, 500);
> 48	  }
> 49	});
> 50	
> ```

## 🤖 Claude *(14:03:33)*

Both files are read in full. Let me verify the two ground-truth dependencies the auth/charge model relies on so my confidence is anchored in the actual code, not just the prompt's stated facts. Specifically: the `deduct_mco_coins` caller-guard behavior and the `video_renders` RLS SELECT policy.

## 🤖 Claude *(14:03:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rl \"deduct_mco_coins\\|finalize_video_render\\|video_renders\" supabase/migrations/ 2>/dev/null | head -40",
  "description": "Find migrations defining the RPCs and RLS"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> supabase/migrations/20260425180000_vector_search_optimization.sql
> supabase/migrations/20260516224541_deduct_mco_coins_ledger.sql
> supabase/migrations/20260526201000_deduct_mco_coins_locking.sql
> supabase/migrations/20260620120200_begin_autopilot_cycle.sql
> supabase/migrations/20260603210500_harden_definer_search_path.sql
> supabase/migrations/20260622030000_video_studio_org_tenancy.sql
> supabase/migrations/20260603220000_secure_ledger_rpcs.sql
> supabase/migrations/20260525173500_drop_deduct_mco_coins_overload.sql
> supabase/migrations/20260622040000_video_studio_renders_and_assets.sql
> supabase/migrations/20260622030100_video_studio_org_grant_hardening.sql
> ```

## 🤖 Claude *(14:03:39)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260622040000_video_studio_renders_and_assets.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: video-studio Fatia 1 — domain foundation (video_renders + video_assets + finalize/refund RPC).
> 2	-- BoK SSOT: docs/bok/video-studio/06-data-model.md (§2.1 video_renders, §2.4 video_assets, §3 RLS/index plan)
> 3	--           + 04-frd.md (FR-VS-009/010/011/014/024/026/030) + 05-sdd.md (§2.6 New DB Objects).
> 4	-- Anticipated process (Lei 2): docs/bok/video-studio/07-process-flow.md PROC-VS-001/004 (charge-at-entry + refund).
> 5	--
> 6	-- SCOPE (slice 1 — foundation + edge contract; render engine deferred to slice 2):
> 7	--   • video_renders — render state machine + atomic charged/refunded ledger, poll-able, tenancy-aware from birth
> 8	--     (org_id/client_id NULLABLE: NULL = solo creator v0.1, byte-identical backward-compat; set = agency §AG).
> 9	--   • video_assets — material artifact manifest (Storage object + node_id) = the erasure unit (FR-VS-030).
> 10	--   • finalize_video_render — the ONLY terminal+refund authority (service-role), mirrors finalize_vision_job
> 11	--     (20260615160000): atomic guard `state IN (queued,running,qa_gate)` ⇒ first finalizer wins, idempotent,
> 12	--     never money-without-guard nor double-refund.
> 13	--
> 14	-- TENANCY MODEL (FMEA-VS-020 — cross-tenant isolation is the v1.1 top RPN; /security-review gated):
> 15	--   SELECT = own row OR (agency) a row of an org the caller is an active member of (public.is_org_member, the
> 16	--   anti-recursion SECURITY DEFINER helper from 20260622030000). NO INSERT/UPDATE policy for authenticated ⇒
> 17	--   default-deny writes: the edge fn (video-render) is the ONLY writer, via the service key, AFTER deduct_mco_coins.
> 18	--   A tenant therefore can NEVER forge a render row (bypassing the charge) nor mutate one (zeroing its charge /
> 19	--   faking 'done' to read another tenant's asset). Mirrors vision_jobs (20260615160000) + lead_core tenancy.
> 20	--   video_renders carries a RESTRICTIVE no-delete (financial ledger family: creative_metrics / autopilot_cycles).
> 21	--
> 22	-- project_id is uuid WITHOUT FK (there is no `projects` table — project_id is text/uuid tenant tag elsewhere;
> 23	-- mirrors vision_jobs:19). The (org_id, client_id) composite FK → clients(org_id, id) is NOT VALID (no backfill
> 24	-- scan; existing/solo rows have NULLs ⇒ MATCH SIMPLE skips the FK) and proves a render's client truly belongs to
> 25	-- the stated org. CHECK keeps client_id from being set without an org.
> 26	
> 27	-- ─────────────────────────────────────────────────────────────────────────────
> 28	-- 1. video_renders — render state machine + atomic ledger (FR-VS-009/010/011/014/024/026)
> 29	-- ─────────────────────────────────────────────────────────────────────────────
> 30	CREATE TABLE IF NOT EXISTS public.video_renders (
> 31	  id            uuid        PRIMARY KEY DEFAULT gen_random_uuid(),    -- = render_id (returned in 202; poll-able)
> 32	  user_id       uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 33	  org_id        uuid        REFERENCES public.organizations(id) ON DELETE CASCADE,  -- NULL = solo creator (§AG opt-in)
> 34	  client_id     uuid,                                                 -- agency cost-center; FK is composite (below)
> 35	  project_id    uuid,                                                 -- optional tenant project tag (no projects table)
> 36	  engine        text        NOT NULL CHECK (engine IN ('faceless','hyperframes')),
> 37	  state         text        NOT NULL DEFAULT 'queued'
> 38	                  CHECK (state IN ('queued','running','qa_gate','done','qa_failed','failed')),
> 39	  product_id    uuid,                                                 -- product-aware (FR-VS-017); logical, no FK (prunable)
> 40	  topic         text,                                                 -- free topic when no product
> 41	  template_id   uuid,                                                 -- HyperFrames reuse (FR-VS-024); logical until templates land
> 42	  legs          jsonb       NOT NULL DEFAULT '[]'::jsonb,             -- per-leg status (script/image/voice/motion/overlay/composite/qa)
> 43	  qa            jsonb,                                                -- { consistent, confidence } from the VLM gate (FR-VS-019/020)
> 44	  charged_mco   int         NOT NULL DEFAULT 0 CHECK (charged_mco >= 0),
> 45	  refunded_mco  int         NOT NULL DEFAULT 0 CHECK (refunded_mco >= 0 AND refunded_mco <= charged_mco),
> 46	  refunded_at   timestamptz,                                          -- idempotency guard (refund 1×/render — PROC-VS-004)
> 47	  storage_key   text,                                                 -- set at `done`; object ≥100KB (Lei 1 proof)
> 48	  voice_consent boolean     NOT NULL DEFAULT false,                   -- required for identifiable voice cloning (FR-VS-032)
> 49	  node_id       uuid,                                                 -- mesh observation (FR-VS-026); logical → mcorch_nodes.id
> 50	  expires_at    timestamptz NOT NULL DEFAULT (now() + interval '24 hours'),  -- poll retention ≥24h
> 51	  created_at    timestamptz NOT NULL DEFAULT now(),
> 52	  updated_at    timestamptz NOT NULL DEFAULT now(),
> 53	  CONSTRAINT video_renders_client_needs_org CHECK (client_id IS NULL OR org_id IS NOT NULL),
> 54	  CONSTRAINT video_renders_client_fk FOREIGN KEY (org_id, client_id)
> 55	    REFERENCES public.clients(org_id, id) ON DELETE SET NULL NOT VALID
> 56	);
> 57	
> 58	ALTER TABLE public.video_renders ENABLE ROW LEVEL SECURITY;
> 59	
> 60	-- SELECT: own row, OR an agency row whose org the caller actively belongs to (anti-recursion helper).
> 61	CREATE POLICY "video_renders_select_own_or_org" ON public.video_renders
> 62	  FOR SELECT USING (
> 63	    auth.uid() = user_id
> 64	    OR (org_id IS NOT NULL AND public.is_org_member(org_id))
> 65	  );
> 66	
> 67	-- No INSERT/UPDATE policy for authenticated ⇒ default-deny: the edge fn writes via the service key AFTER the
> 68	-- atomic deduct. RESTRICTIVE no-delete: the financial ledger is never client-deletable (service-role erasure only).
> 69	CREATE POLICY "video_renders_no_client_delete" ON public.video_renders
> 70	  AS RESTRICTIVE FOR DELETE USING (false);
> 71	
> 72	CREATE INDEX IF NOT EXISTS video_renders_user_state_idx   ON public.video_renders (user_id, state);
> 73	CREATE INDEX IF NOT EXISTS video_renders_user_created_idx ON public.video_renders (user_id, created_at DESC);
> 74	CREATE INDEX IF NOT EXISTS video_renders_org_idx          ON public.video_renders (org_id) WHERE org_id IS NOT NULL;
> 75	CREATE INDEX IF NOT EXISTS video_renders_expires_idx      ON public.video_renders (expires_at);
> 76	
> 77	CREATE TRIGGER tr_update_video_renders_updated_at
> 78	  BEFORE UPDATE ON public.video_renders
> 79	  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
> 80	
> 81	COMMENT ON TABLE public.video_renders IS
> 82	  'video-studio render state machine (FR-VS-009/014/024). queued→running→qa_gate→done|qa_failed|failed; atomic '
> 83	  'charged/refunded ledger (refunded_mco<=charged_mco, refunded_at idempotency). SELECT own-or-org-member RLS; '
> 84	  'edge fn writes via service key after deduct; RESTRICTIVE no client delete. org_id/client_id NULL = solo (§AG opt-in).';
> 85	
> 86	-- ─────────────────────────────────────────────────────────────────────────────
> 87	-- 2. video_assets — material artifact manifest = the erasure unit (FR-VS-030/031)
> 88	-- ─────────────────────────────────────────────────────────────────────────────
> 89	CREATE TABLE IF NOT EXISTS public.video_assets (
> 90	  id              uuid        PRIMARY KEY DEFAULT gen_random_uuid(),
> 91	  user_id         uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 92	  render_id       uuid        NOT NULL REFERENCES public.video_renders(id) ON DELETE CASCADE,
> 93	  kind            text        NOT NULL CHECK (kind IN ('video','image','audio')),
> 94	  storage_key     text        NOT NULL,                              -- object in private bucket video-studio-assets
> 95	  node_id         uuid,                                              -- derived mesh node (FR-VS-026); logical
> 96	  bytes           bigint      CHECK (bytes IS NULL OR bytes >= 0),   -- material size (video ≥100KB) — Lei 1
> 97	  retention_until timestamptz,                                       -- LGPD retention clock (Art. 16)
> 98	  created_at      timestamptz NOT NULL DEFAULT now()
> 99	);
> 100	
> 101	ALTER TABLE public.video_assets ENABLE ROW LEVEL SECURITY;
> 102	
> 103	-- SELECT own only (the asset row is tenant-bound via user_id; org members read assets through the render join in
> 104	-- the app layer when agency surfaces land). No write policy ⇒ service-role writes only (same billing-integrity rule).
> 105	CREATE POLICY "video_assets_select_own" ON public.video_assets
> 106	  FOR SELECT USING (auth.uid() = user_id);
> 107	
> 108	CREATE INDEX IF NOT EXISTS video_assets_render_idx    ON public.video_assets (render_id);
> 109	CREATE INDEX IF NOT EXISTS video_assets_user_idx      ON public.video_assets (user_id);
> 110	CREATE INDEX IF NOT EXISTS video_assets_retention_idx ON public.video_assets (retention_until);
> 111	
> 112	COMMENT ON TABLE public.video_assets IS
> 113	  'video-studio material artifact manifest (FR-VS-030). Storage object + node_id = atomic erasure unit. '
> 114	  'SELECT-own RLS; service-role writes. bytes>=100KB enforced app-side before render reaches done (Lei 1).';
> 115	
> 116	-- ─────────────────────────────────────────────────────────────────────────────
> 117	-- 3. finalize_video_render — atomic terminal + refund authority (FR-VS-011 · mirrors finalize_vision_job)
> 118	--    Closes the /security-review HIGH class (charge-without-value + refund/guard atomicity). The ONLY way a
> 119	--    render goes terminal. Guard `state IN (queued,running,qa_gate)` ⇒ the FIRST finalizer wins (worker OR a
> 120	--    future poll lazy-reconcile OR a sweep); a second call on an already-terminal render is a no-op (no double
> 121	--    refund). The video_renders guard write AND the balance credit (add_mco_coins) commit in ONE transaction.
> 122	--    service_role-only (the worker/edge calls it via SB_SECRET_KEY; tenants never reach it). FMEA-011 reviewed.
> 123	-- ─────────────────────────────────────────────────────────────────────────────
> 124	CREATE OR REPLACE FUNCTION public.finalize_video_render(
> 125	  p_render_id   uuid,
> 126	  p_state       text,
> 127	  p_storage_key text,    -- NULL keeps existing (set on success)
> 128	  p_qa          jsonb,   -- NULL keeps existing (VLM verdict)
> 129	  p_node_id     uuid,    -- NULL keeps existing (mesh observation)
> 130	  p_refund      int      -- refund to credit (0 = none, e.g. 'done'); must be <= charged_mco
> 131	)
> 132	RETURNS jsonb
> 133	LANGUAGE plpgsql
> 134	SECURITY DEFINER
> 135	SET search_path = ''
> 136	AS $$
> 137	DECLARE
> 138	  v_uid uuid;
> 139	BEGIN
> 140	  IF p_state NOT IN ('done','qa_failed','failed') THEN
> 141	    RAISE EXCEPTION 'finalize_video_render: terminal state required, got %', p_state USING errcode = '22023';
> 142	  END IF;
> 143	
> 144	  -- Claim + finalize a NON-TERMINAL render exactly once.
> 145	  UPDATE public.video_renders
> 146	     SET state        = p_state,
> 147	         storage_key  = COALESCE(p_storage_key, storage_key),
> 148	         qa           = COALESCE(p_qa, qa),
> 149	         node_id      = COALESCE(p_node_id, node_id),
> 150	         refunded_mco = CASE WHEN p_refund > 0 THEN p_refund ELSE refunded_mco END,
> 151	         refunded_at  = CASE WHEN p_refund > 0 THEN now()    ELSE refunded_at END
> 152	   WHERE id = p_render_id
> 153	     AND state IN ('queued','running','qa_gate')
> 154	   RETURNING user_id INTO v_uid;
> 155	
> 156	  IF v_uid IS NULL THEN
> 157	    RETURN jsonb_build_object('finalized', false);   -- already terminal → no-op (no double refund)
> 158	  END IF;
> 159	
> 160	  IF p_refund > 0 THEN
> 161	    PERFORM public.add_mco_coins(v_uid, p_refund);
> 162	    RETURN jsonb_build_object('finalized', true, 'refunded', p_refund);
> 163	  END IF;
> 164	
> 165	  RETURN jsonb_build_object('finalized', true, 'refunded', 0);
> 166	END;
> 167	$$;
> 168	
> 169	REVOKE ALL ON FUNCTION public.finalize_video_render(uuid, text, text, jsonb, uuid, int) FROM PUBLIC, anon, authenticated;
> 170	GRANT EXECUTE ON FUNCTION public.finalize_video_render(uuid, text, text, jsonb, uuid, int) TO service_role;
> 171	
> ```

## 🤖 Claude *(14:03:39)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260603220000_secure_ledger_rpcs.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- SECURITY P0 (schema-drift-audit 2026-06-03, adjacent finding — Sovereign GO "fix completo"): lock down the
> 2	-- mcoCoin ledger RPCs against unauthorized minting / cross-tenant balance manipulation.
> 3	--
> 4	-- Discovered while auditing SECURITY DEFINER functions: all three ledger RPCs grant EXECUTE to PUBLIC/anon/
> 5	-- authenticated and trust a caller-supplied p_user_id with no auth.uid() check. Because they are SECURITY DEFINER
> 6	-- (bypass RLS) and exposed via PostgREST, any logged-in user could call them directly, skipping the edge functions
> 7	-- and their caps:
> 8	--   * award_mco_coins(p_user_id:=self, p_amount:=1000) → mint 1000 mcoCoins per call, unlimited.
> 9	--   * add_user_score(self, big)                        → self-inflate score → coins (100:1).
> 10	--   * deduct_mco_coins(p_amount:=-1000)                → `balance - (-1000)` = mint; the `balance >= p_amount`
> 11	--                                                         guard is `>= -1000` (always true). Ledger stores -(-1000)=+1000.
> 12	--   * deduct_mco_coins(p_user_id:=victim, ...)         → drain another tenant's balance.
> 13	-- (Same exposure model the team's own async_orchestrate_step fix closed by REVOKE-ing public/anon/authenticated.)
> 14	--
> 15	-- FIX, legit paths preserved:
> 16	--   * award_mco_coins / add_user_score are EDGE-ONLY (award-mco-coins / autonomic-action call them via the
> 17	--     service_role admin client; no client code calls them) → REVOKE from public/anon/authenticated, keep service_role.
> 18	--   * deduct_mco_coins IS called by the client (src/lib/billing.ts) for the user's OWN spends → keep the
> 19	--     `authenticated` grant but add internal guards (body otherwise reproduced VERBATIM: SET search_path=public,
> 20	--     row lock, GREATEST clamp, NOT FOUND check, negative-amount ledger insert):
> 21	--       - reject p_amount <= 0 (kills the negative-amount mint),
> 22	--       - non-service_role callers may only deduct from their OWN profile
> 23	--         (auth.role() <> 'service_role' AND p_user_id <> auth.uid() → 42501). service_role (edge fns:
> 24	--         orchestrate-content, canvas-execute, campaign-run, nurture-dispatch) stays exempt.
> 25	--     NOTE: the exemption keys on auth.role()='service_role', NOT on a NULL uid — anon also has a NULL uid, so anon
> 26	--     is additionally REVOKE-d from deduct (anon never legitimately spends).
> 27	
> 28	-- ── award_mco_coins → edge-only, revoke client reach ────────────────────────────────────────────────────────
> 29	REVOKE EXECUTE ON FUNCTION public.award_mco_coins(uuid, integer, text, jsonb) FROM PUBLIC, anon, authenticated;
> 30	GRANT  EXECUTE ON FUNCTION public.award_mco_coins(uuid, integer, text, jsonb) TO service_role;
> 31	
> 32	-- ── add_user_score → edge-only, revoke client reach ────────────────────────────────────────────────────────
> 33	REVOKE EXECUTE ON FUNCTION public.add_user_score(uuid, integer) FROM PUBLIC, anon, authenticated;
> 34	GRANT  EXECUTE ON FUNCTION public.add_user_score(uuid, integer) TO service_role;
> 35	
> 36	-- ── deduct_mco_coins → client-callable; add sign + own-tenant guards ────────────────────────────────────────
> 37	CREATE OR REPLACE FUNCTION public.deduct_mco_coins(p_user_id uuid, p_amount numeric, p_action text DEFAULT 'spend'::text, p_context jsonb DEFAULT '{}'::jsonb)
> 38	 RETURNS void
> 39	 LANGUAGE plpgsql
> 40	 SECURITY DEFINER
> 41	 SET search_path TO 'public'
> 42	AS $function$
> 43	BEGIN
> 44	  -- Guard 1: no negative/zero deduction (a negative amount would ADD balance = mint).
> 45	  IF p_amount IS NULL OR p_amount <= 0 THEN
> 46	    RAISE EXCEPTION 'Valor de débito de mcoCoins deve ser positivo';
> 47	  END IF;
> 48	
> 49	  -- Guard 2: a non-service_role caller may only deduct from its OWN profile (blocks cross-tenant drain).
> 50	  -- NULL-safe `IS DISTINCT FROM` (codebase standard — see 20260602150000) so a NULL role/uid fails CLOSED.
> 51	  IF auth.role() IS DISTINCT FROM 'service_role' AND p_user_id IS DISTINCT FROM auth.uid() THEN
> 52	    RAISE EXCEPTION 'cannot deduct mcoCoins for another user' USING ERRCODE = '42501';
> 53	  END IF;
> 54	
> 55	  -- Force row locking on the profile row to block concurrent executions
> 56	  PERFORM 1 FROM public.profiles WHERE id = p_user_id FOR UPDATE;
> 57	
> 58	  UPDATE public.profiles
> 59	     SET mco_balance = GREATEST(0, mco_balance - p_amount)
> 60	   WHERE id = p_user_id
> 61	     AND mco_balance >= p_amount;
> 62	
> 63	  IF NOT FOUND THEN
> 64	    RAISE EXCEPTION 'Saldo mcoCoins insuficiente para completar a operação';
> 65	  END IF;
> 66	
> 67	  -- Ledger entry. amount stored as NEGATIVE for spends.
> 68	  INSERT INTO public.mcoin_transactions (user_id, action, amount, context)
> 69	  VALUES (p_user_id, p_action, -p_amount::integer, p_context);
> 70	END;
> 71	$function$;
> 72	
> 73	REVOKE EXECUTE ON FUNCTION public.deduct_mco_coins(uuid, numeric, text, jsonb) FROM PUBLIC, anon;
> 74	GRANT  EXECUTE ON FUNCTION public.deduct_mco_coins(uuid, numeric, text, jsonb) TO authenticated, service_role;
> 75	
> ```

## 🤖 Claude *(14:03:59)*

The ground-truth facts are confirmed in the migrations. Now I have everything needed to assess each vector. Let me work through the analysis precisely.

Key confirmations from the actual code:
- `deduct_mco_coins`: positive-amount guard + own-tenant guard, `service_role` exempt. In video-render it's called via the `admin` (service-role) client with `p_user_id: userId` where `userId = user.id` from `getUser()` on the caller's JWT. So a user can only charge themselves.
- `finalize_video_render`: atomic guard `state IN (queued,running,qa_gate)`, idempotent, `refunded_mco <= charged_mco` CHECK, service-role-only.
- `video_renders` RLS: SELECT own-or-org-member; no insert/update for authenticated. The poll runs under the user client (anon key + caller JWT), so RLS binds.

Let me trace the charge/refund paths carefully for the third vector, which is the highest-risk area.

**Path analysis (video-render, post-503 SLICE-2 prepaid path):**

1. `deduct_mco_coins` fails (insufficient balance) → 402, no row created. ✓ No charge.
2. `deduct` succeeds → INSERT fails → refund full `cost` via `add_mco_coins(userId, cost)` → 500. Charge then refund = net zero. ✓
3. `deduct` succeeds → INSERT succeeds → worker `fetch` throws/non-ok → refund via `finalize_video_render(..., p_refund: cost)` → 502 with `render_id`. ✓
4. `deduct` succeeds → INSERT succeeds → worker OK → 202. Charged, render queued. ✓

Now I'll scrutinize the edge cases in each refund path.

**Refund path 2 (INSERT-failed → `add_mco_coins`):** This refunds the full cost directly and returns 500. The render row does not exist (INSERT failed), so `finalize_video_render` can never later refund it — no double refund possible. ✓

**Refund path 3 (worker-trigger-failed → `finalize_video_render`):** This sets the just-created row to `failed` with `p_refund: cost`. Because the row was just INSERTed as `queued`, the guard `state IN (queued,running,qa_gate)` passes → refunds once, sets `refunded_at`. A later worker callback or sweep calling `finalize` again on the now-`failed` row is a no-op. ✓ No double refund.

Now the subtle one — **can the worker-trigger refund double-refund with the worker itself?** In path 3, the edge function already POSTed to the worker before deciding it failed. The failure branch is taken when `fetch` throws OR `!r.ok`. Consider: the worker received the request, started processing, but returned a non-2xx (e.g. 500 after accepting the job). The edge function then calls `finalize(..., failed, refund:cost)` → row goes terminal `failed`, refunded once. If the worker later also calls `finalize(done, refund:0)` on the same render, the guard `state IN (queued,running,qa_gate)` now fails (state is `failed`) → no-op. So worst case the user is refunded AND the worker produces a video they don't get charged for — that's a value-leak/business risk, not a security vuln, and it's idempotent on the money side (single refund). Not a security finding.

Let me look at whether there's any path that **charges then returns success without a usable render**, or **creates a render without charging**. There is none in the code: every INSERT is strictly after a successful deduct, and the 503 gate returns before deduct. ✓

Now let me verify two remaining items I want to be certain about: the `is_org_member` helper (for the poll RLS, to confirm it can't be abused) and whether `logHealth` / responses can leak anything.

## 🤖 Claude *(14:04:00)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260622030000_video_studio_org_tenancy.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- video-studio BoK v1.1 §AG — Agency-Leverage tenancy FOUNDATION (FR-VS-033/036/037).
> 2	-- organizations → organization_members (RBAC + seats) → clients (sub-accounts · cost-center · erasure unit).
> 3	--
> 4	-- CRITICAL DESIGN (over the BoK §AG stub): RLS uses SECURITY DEFINER helpers (is_org_member / org_role) to
> 5	-- AVOID recursive RLS on organization_members. The §AG stub's self-subquery
> 6	-- (USING org_id IN (SELECT org_id FROM organization_members WHERE user_id=auth.uid())) would infinite-loop —
> 7	-- CLAUDE.md mandates the has_role() definer pattern for exactly this. Org creation goes through the
> 8	-- create_organization() definer RPC so the owner membership is inserted atomically (solves the first-member
> 9	-- bootstrap chicken-and-egg). Backward-compat: this migration ONLY ADDS the agency layer; solo-creator
> 10	-- (user_id-scoped) tables/paths are untouched. The video_* tables + org_id/client_id columns + the money/erasure
> 11	-- RPCs (deduct_mco_coins_org, erase_client_artifacts) land WITH the studio-integration migration (those RPCs
> 12	-- must reference existing render tables).
> 13	
> 14	-- ─────────────────────────────────────────────────────────────────────────────
> 15	-- Tables
> 16	-- ─────────────────────────────────────────────────────────────────────────────
> 17	
> 18	-- organizations — the agency tenant: white-label (custom_domain/brand_theme) + wholesale wallet (margin lever).
> 19	CREATE TABLE IF NOT EXISTS public.organizations (
> 20	  id                    uuid PRIMARY KEY DEFAULT gen_random_uuid(),
> 21	  name                  text NOT NULL,
> 22	  slug                  text UNIQUE NOT NULL,
> 23	  owner_user_id         uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 24	  plan_tier             text NOT NULL DEFAULT 'agency' CHECK (plan_tier IN ('agency','enterprise')),
> 25	  custom_domain         text,
> 26	  brand_theme           jsonb NOT NULL DEFAULT '{}'::jsonb,
> 27	  wholesale_mco_balance numeric NOT NULL DEFAULT 0 CHECK (wholesale_mco_balance >= 0),
> 28	  created_at            timestamptz NOT NULL DEFAULT now()
> 29	);
> 30	ALTER TABLE public.organizations ENABLE ROW LEVEL SECURITY;  -- default-deny
> 31	
> 32	-- organization_members — membership + RBAC + seat management.
> 33	CREATE TABLE IF NOT EXISTS public.organization_members (
> 34	  id          uuid PRIMARY KEY DEFAULT gen_random_uuid(),
> 35	  org_id      uuid NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
> 36	  user_id     uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 37	  role        text NOT NULL DEFAULT 'editor' CHECK (role IN ('owner','billing_admin','editor','viewer')),
> 38	  seat_active boolean NOT NULL DEFAULT true,
> 39	  created_at  timestamptz NOT NULL DEFAULT now(),
> 40	  UNIQUE (org_id, user_id)
> 41	);
> 42	ALTER TABLE public.organization_members ENABLE ROW LEVEL SECURITY;  -- default-deny
> 43	CREATE INDEX IF NOT EXISTS idx_org_members_user_active ON public.organization_members (user_id) WHERE seat_active;
> 44	CREATE INDEX IF NOT EXISTS idx_org_members_org ON public.organization_members (org_id);
> 45	
> 46	-- clients — agency client sub-accounts: cost-center + selective-erasure unit. Composite (org_id,id) key is the
> 47	-- FK target for the video_* tables' (org_id,client_id) tenant-scoped FKs (added in the studio migration).
> 48	CREATE TABLE IF NOT EXISTS public.clients (
> 49	  id            uuid NOT NULL DEFAULT gen_random_uuid(),
> 50	  org_id        uuid NOT NULL REFERENCES public.organizations(id) ON DELETE CASCADE,
> 51	  name          text NOT NULL,
> 52	  byok_ref      text,
> 53	  affiliate_tag text,
> 54	  status        text NOT NULL DEFAULT 'active' CHECK (status IN ('active','paused','archived')),
> 55	  created_at    timestamptz NOT NULL DEFAULT now(),
> 56	  PRIMARY KEY (id),
> 57	  UNIQUE (org_id, id)
> 58	);
> 59	ALTER TABLE public.clients ENABLE ROW LEVEL SECURITY;  -- default-deny
> 60	CREATE INDEX IF NOT EXISTS idx_clients_org ON public.clients (org_id);
> 61	
> 62	-- ─────────────────────────────────────────────────────────────────────────────
> 63	-- Anti-recursion membership helpers (SECURITY DEFINER — mirror public.has_role())
> 64	-- ─────────────────────────────────────────────────────────────────────────────
> 65	CREATE OR REPLACE FUNCTION public.is_org_member(p_org_id uuid)
> 66	RETURNS boolean LANGUAGE sql STABLE SECURITY DEFINER SET search_path = '' AS $$
> 67	  SELECT EXISTS (
> 68	    SELECT 1 FROM public.organization_members m
> 69	    WHERE m.org_id = p_org_id AND m.user_id = auth.uid() AND m.seat_active
> 70	  );
> 71	$$;
> 72	
> 73	CREATE OR REPLACE FUNCTION public.org_role(p_org_id uuid)
> 74	RETURNS text LANGUAGE sql STABLE SECURITY DEFINER SET search_path = '' AS $$
> 75	  SELECT m.role FROM public.organization_members m
> 76	  WHERE m.org_id = p_org_id AND m.user_id = auth.uid() AND m.seat_active
> 77	  LIMIT 1;
> 78	$$;
> 79	
> 80	REVOKE ALL ON FUNCTION public.is_org_member(uuid) FROM PUBLIC;
> 81	REVOKE ALL ON FUNCTION public.org_role(uuid) FROM PUBLIC;
> 82	GRANT EXECUTE ON FUNCTION public.is_org_member(uuid) TO authenticated, service_role;
> 83	GRANT EXECUTE ON FUNCTION public.org_role(uuid) TO authenticated, service_role;
> 84	
> 85	-- ─────────────────────────────────────────────────────────────────────────────
> 86	-- Bootstrap RPC — atomic org + owner-membership (solves first-member chicken-and-egg under RLS)
> 87	-- ─────────────────────────────────────────────────────────────────────────────
> 88	CREATE OR REPLACE FUNCTION public.create_organization(p_name text, p_slug text)
> 89	RETURNS uuid LANGUAGE plpgsql SECURITY DEFINER SET search_path = '' AS $$
> 90	DECLARE v_org uuid;
> 91	BEGIN
> 92	  IF auth.uid() IS NULL THEN RAISE EXCEPTION 'authentication required'; END IF;
> 93	  IF p_name IS NULL OR btrim(p_name) = '' OR p_slug IS NULL OR btrim(p_slug) = '' THEN
> 94	    RAISE EXCEPTION 'name and slug are required';
> 95	  END IF;
> 96	  INSERT INTO public.organizations (name, slug, owner_user_id)
> 97	    VALUES (btrim(p_name), btrim(p_slug), auth.uid())
> 98	    RETURNING id INTO v_org;
> 99	  INSERT INTO public.organization_members (org_id, user_id, role, seat_active)
> 100	    VALUES (v_org, auth.uid(), 'owner', true);
> 101	  RETURN v_org;
> 102	END; $$;
> 103	REVOKE ALL ON FUNCTION public.create_organization(text, text) FROM PUBLIC;
> 104	GRANT EXECUTE ON FUNCTION public.create_organization(text, text) TO authenticated;
> 105	
> 106	-- ─────────────────────────────────────────────────────────────────────────────
> 107	-- RLS policies (helper-based — NO recursion). Direct INSERT into organizations is NOT granted a policy:
> 108	-- org creation MUST go through create_organization() so an owner membership always exists.
> 109	-- ─────────────────────────────────────────────────────────────────────────────
> 110	CREATE POLICY org_member_select ON public.organizations FOR SELECT TO authenticated
> 111	  USING (public.is_org_member(id));
> 112	CREATE POLICY org_admin_update ON public.organizations FOR UPDATE TO authenticated
> 113	  USING (public.org_role(id) IN ('owner','billing_admin'))
> 114	  WITH CHECK (public.org_role(id) IN ('owner','billing_admin'));
> 115	CREATE POLICY org_owner_delete ON public.organizations FOR DELETE TO authenticated
> 116	  USING (public.org_role(id) = 'owner');
> 117	
> 118	CREATE POLICY orgmem_select ON public.organization_members FOR SELECT TO authenticated
> 119	  USING (public.is_org_member(org_id));
> 120	-- SECURITY (review 2026-06-22, Vuln 1): member/role/seat management is OWNER-ONLY. A billing_admin must NOT be
> 121	-- able to write organization_members (the prior `IN ('owner','billing_admin')` let a billing_admin INSERT a
> 122	-- role='owner' row for themselves → escalation). Seat/billing-admin self-service, if needed, comes via a future
> 123	-- SECURITY DEFINER RPC that enforces the role hierarchy — never a broad table policy.
> 124	CREATE POLICY orgmem_owner_write ON public.organization_members FOR ALL TO authenticated
> 125	  USING (public.org_role(org_id) = 'owner')
> 126	  WITH CHECK (public.org_role(org_id) = 'owner');
> 127	
> 128	CREATE POLICY clients_member_select ON public.clients FOR SELECT TO authenticated
> 129	  USING (public.is_org_member(org_id));
> 130	CREATE POLICY clients_member_write ON public.clients FOR ALL TO authenticated
> 131	  USING (public.org_role(org_id) IN ('owner','billing_admin','editor'))
> 132	  WITH CHECK (public.org_role(org_id) IN ('owner','billing_admin','editor'));
> 133	
> 134	-- ─────────────────────────────────────────────────────────────────────────────
> 135	-- Grants — service_role full; authenticated DML gated by the policies above; anon denied.
> 136	-- SECURITY (review 2026-06-22, Vuln 2 & 3): on `organizations`, authenticated gets COLUMN-LEVEL UPDATE only on
> 137	-- white-label/display columns. The financial + ownership + tier columns (wholesale_mco_balance, plan_tier,
> 138	-- owner_user_id) are NOT grantable to authenticated → cannot be minted/hijacked via a direct UPDATE; they mutate
> 139	-- ONLY through service-role RPCs (deduct_mco_coins_org / billing webhook / a future transfer-ownership RPC).
> 140	-- (Postgres RLS USING/CHECK cannot reference OLD, so per-column control is enforced by GRANT, not a policy.)
> 141	-- No INSERT grant on organizations — creation is exclusively via the create_organization() SECURITY DEFINER RPC.
> 142	REVOKE ALL ON public.organizations, public.organization_members, public.clients FROM anon;
> 143	
> 144	GRANT SELECT, DELETE ON public.organizations TO authenticated;
> 145	GRANT UPDATE (name, slug, custom_domain, brand_theme) ON public.organizations TO authenticated;
> 146	
> 147	GRANT SELECT, INSERT, UPDATE, DELETE ON public.organization_members, public.clients TO authenticated;
> 148	GRANT ALL ON public.organizations, public.organization_members, public.clients TO service_role;
> 149	
> ```

## 🤖 Claude *(14:04:36)*

The `is_org_member` helper is correctly scoped to `auth.uid()` and `seat_active`, so the poll's RLS SELECT (`auth.uid() = user_id OR (org_id IS NOT NULL AND is_org_member(org_id))`) cannot be abused — a caller only sees their own renders or renders of orgs they actively belong to. This is sound.

I now have full confidence on every vector. Here is the review.

---

## Security Review — `video-render` & `video-render-poll`

**ORO triplet desta task:**
- Operator: AI Agent (security reviewer)
- Reviewer: Sovereign (Gabriel)
- Owner: Sovereign — risco = cobrança indevida / vazamento cross-tenant em produção

**Verdict: NO findings at or above confidence 8. Nothing HIGH or MEDIUM with >80% confidence.**

The two functions are well-constructed. Identity is taken exclusively from `getUser()` on the caller's JWT (never from the body), the charge always targets the authenticated caller, the poll read is RLS-bound under the user client, and the charge/refund paths are each idempotent and non-overlapping.

### Per-vector rationale (each checked, none clears the 8 bar)

1. **AuthZ / IDOR on charge — CLEAR.** `userId = user.id` from `userClient.auth.getUser()` (video-render:44–46). The body is parsed *after* identity and never sets `userId`. `deduct_mco_coins` is called with `p_user_id: userId` via the service-role `admin` client; the RPC's own guard makes service_role charge the passed uid, which is the authenticated caller. A user can only ever charge themselves. No body field overrides identity. Confidence of *no* vuln: 10.

2. **Poll read RLS — CLEAR.** video-render-poll:33–41 runs the SELECT under `userClient` (pubKey + caller JWT); the service/admin client is never constructed in this file (no `SB_SECRET_KEY` read at all). RLS `auth.uid()=user_id OR is_org_member(org_id)` binds; `is_org_member` is `auth.uid()`-scoped + `seat_active`. A foreign `render_id` → `maybeSingle()` returns null → 404 (line 43). No RLS bypass. Confidence of no vuln: 10.

3. **Charge/refund integrity — CLEAR.** Four paths traced:
   - 402: deduct fails → no row, no charge.
   - INSERT fails after deduct → `add_mco_coins(userId, cost)` full refund; no row exists so `finalize_video_render` can never touch it → no double refund (video-render:104–108).
   - Worker-trigger fails after deduct+insert → `finalize_video_render(..., p_refund:cost)`; row was just `queued`, guard `state IN (queued,running,qa_gate)` passes once, sets `refunded_at`; any later worker/sweep `finalize` on the now-`failed` row is a no-op (migration:150–158, CHECK `refunded_mco<=charged_mco`) → single refund (video-render:120–126).
   - 202: charged + queued, correct.
   No path charges-without-row, creates-row-without-charge (every INSERT is strictly post-deduct), or double-refunds. The only residual is a *business* value-leak (worker accepts then errors → user refunded but a video may still get produced) — money side stays single-refunded; not a security issue. Confidence: 9 that this is safe.

4. **BYOK cross-tenant key read — CLEAR.** video-render:66–67 reads `decrypted_user_api_keys` filtered `.eq("user_id", userId)` (authenticated caller, not a body id). The value is only existence-checked (`!keys?.gemini_api_key`, line 68) and never placed in any response or log. No cross-tenant read, no key leak. Confidence: 10.

5. **Secret / PII leakage — CLEAR.** `logHealth` inserts only `{service, status, event}` (video-render:36) — fixed string literals (`insufficient_balance`, `insert_failed`, `worker_trigger_failed`, etc.), no user data, tokens, or topic. The worker `Authorization: Bearer ${serviceKey}` (line 116) goes only to the trusted worker webhook, never to a client. Error responses return `insErr?.message` / `e.message` (lines 108, 125, 132; poll 42, 47) — Supabase/fetch error text, not secrets. `infra_health_logs` is global-read but carries nothing per-tenant here. Minor note (below 8): surfacing raw DB error strings to the client is mild information disclosure, but contains no secret/credential. Confidence of no HIGH/MEDIUM: 9.

6. **Input validation with security impact — CLEAR.** Engine is strictly whitelisted (`!== "faceless" && !== "hyperframes"` → 422, video-render:50). Poll validates `render_id` against a UUID regex before query (video-render-poll:14,30). `topic` is `.slice(0,500)`, `product_id` coerced to string-or-null. All downstream writes go through parameterized supabase-js (no SQL injection surface). Confidence: 9.

7. **SLICE-1 dormant prepaid path — reviewed as live.** The 503 gate (video-render:83–88) returns before deduct, so today nothing charges. Reviewed the post-gate path as if `VIDEO_*_WEBHOOK` is set (slice 2): the charge/refund analysis in (3) holds unchanged. No latent vuln waiting to activate.

### One sub-8 observation (reported, not a finding, not actionable as a vuln)
- video-render:108 / :125 / :132 and poll:42/:47 echo raw `error.message` to the client. Low-value information disclosure (DB/fetch error text), no secret content. Confidence it's a *real security issue*: ~3 — below threshold; noted only for completeness.

**Bottom line:** No NEW vulnerability at >80% confidence. The IDOR, RLS-bypass, double-charge, double-refund, BYOK cross-tenant, and secret-leak vectors were each traced to ground (including the backing migrations for `deduct_mco_coins`, `finalize_video_render`, `video_renders` RLS, and `is_org_member`) and all are correctly closed. Safe to proceed past `/security-review`.

Relevant files:
- `/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render/index.ts`
- `/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render-poll/index.ts`
- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260622040000_video_studio_renders_and_assets.sql`
- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260603220000_secure_ledger_rpcs.sql`
- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260622030000_video_studio_org_tenancy.sql`

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-22 - agent-af8f621c5a5a09ed3]]
> * **Próxima Sessão**: [[2026-06-23 - Resolver CF WAF e secrets para ação Sovereign]]
%% --- TIMELINE END --- %%

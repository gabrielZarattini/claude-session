# Session agent-a5ada5c5a3d4df1ff
**Date:** 2026-06-04 | **Session ID:** `agent-a5ada5c5a3d4df1ff`

---

## 👤 User *(02:02:57)*

You are validating a candidate security finding to filter false positives. Read the relevant code in /home/gcrUX/htdocs/constellation-orchestra and assign a confidence score 1-10. Only report TRUE if you confirm a concrete, exploitable attack path.

CANDIDATE FINDING (HIGH): HITL human-approval bypass via direct PostgREST INSERT with status='approved'.

CLAIM: An authenticated tenant can bypass the Human-in-the-Loop approval gate of the Intent Orchestrator and trigger a REAL outward dispatch (publish/campaign/charge) without any human approval, by:
1. Directly `POST /rest/v1/intent_plans` with `{user_id: <self>, plan:[{action:"publicar",channel:"social",impact:"high"}], status:"approved"}` via PostgREST using their normal user JWT + anon apikey.
2. Then calling `POST /functions/v1/intent-execute {plan_id, decision:"execute"}`.

The new transition guard trigger in `supabase/migrations/20260603270000_intent_plans_transition_guard_and_bindings.sql` is `BEFORE UPDATE` only, so it does NOT fire on the INSERT. The executor `supabase/functions/intent-execute/index.ts` execute path: `if (highImpact && status !== "approved")` blocks → but status IS 'approved' (self-planted) → passes → marks executed (service role UPDATE, passes the UPDATE guard) → dispatches outward.

VERIFY THESE FACTS by reading the code:
1. Original migration `supabase/migrations/20260603250000_marketing_hub_intent_plans.sql`: Does `intent_plans_insert_own` RLS policy restrict the `status` column? Does the CHECK constraint allow `status='approved'`? Is RLS the only gate (i.e., is `authenticated` granted INSERT by Supabase default on an RLS-enabled public table — yes unless explicitly revoked; check for any REVOKE)?
2. New migration `20260603270000`: Confirm `tr_guard_intent_plan_transition` is `BEFORE UPDATE` only (not INSERT). Confirm `validate_intent_plan_bindings` (BEFORE INSERT OR UPDATE) does NOT check the `status` column.
3. `intent-execute/index.ts`: Confirm the execute path dispatches outward when status==='approved' for a high-impact plan, with no other check on how the row reached 'approved' (no approved_by/approved_at provenance, no check that it transitioned through pending_hitl).
4. Callees `campaign-run/index.ts`, `orchestrate-content/index.ts`, `nurture-dispatch/index.ts`: Confirm they only check tenant OWNERSHIP (`.eq("user_id", user.id)`) and have NO concept of HITL/intent-plan approval — so owning the resource is sufficient for the dispatch to perform a real action.

Also assess: is this a MEANINGFUL escalation given the same user could legitimately call decision='approve' themselves? (Consider: the directive's explicit security goal is that approved/executed states are only reachable via the service-role-mediated state machine; direct INSERT of 'approved' skips the state machine and the server-side approve validation, and the in-code comment explicitly claims this is prevented. Also the binding-validation trigger fires on INSERT but the transition guard does not — an inconsistency proving the INSERT path was overlooked.)

Apply these false-positive rules: do NOT count DOS, rate-limiting, theoretical races, log spoofing, or client-side-only issues. This is a server-side authorization boundary (Postgres RLS + edge function), which IS in scope.

Output: confidence score (1-10) + one paragraph justification + whether the proposed fix (extend the guard to BEFORE INSERT OR UPDATE blocking non-service_role from inserting status IN ('approved','executed'), and/or tighten the insert RLS policy to forbid client-set approved/executed) correctly closes it. Be concrete.

## 🤖 Claude *(02:02:59)*

I'll validate this security finding by reading the relevant code. Let me start by examining the key files.

## 🤖 Claude *(02:03:00)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260603250000_marketing_hub_intent_plans.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: marketing-hub Intent Orchestrator + HITL data layer (FR-MH-009).
> 2	-- BoK SSOT: docs/bok/marketing-hub/06-data-model.md (§Table intent_plans) + 04-frd.md FR-MH-009 + 05-sdd.md
> 3	--           (intent-orchestrate edge fn + useIntentOrchestrator + HITLApprovalCard; STRIDE row "Intent
> 4	--           Orchestrator / ação de alto impacto sem revisão = Tampering → policy engine + HITL obrigatório").
> 5	--
> 6	-- `intent-orchestrate` translates a natural-language intent into a task plan; a policy engine marks policy='hitl'
> 7	-- when any task is high-impact (publish / charge / external send) → status='pending_hitl' (human approval required);
> 8	-- otherwise policy='auto' / status='auto_approved'. `rationale` is the auditable XAI explanation. User-scoped
> 9	-- (no lead/campaign FK in MVP — a plan is a tenant's orchestration artifact); RLS default-deny.
> 10	
> 11	CREATE TABLE IF NOT EXISTS public.intent_plans (
> 12	  id         uuid PRIMARY KEY DEFAULT gen_random_uuid(),
> 13	  user_id    uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 14	  intent     text NOT NULL,
> 15	  plan       jsonb NOT NULL DEFAULT '[]'::jsonb,  -- [{action, channel?, impact, rationale}]
> 16	  policy     text NOT NULL DEFAULT 'auto' CHECK (policy IN ('auto','hitl')),
> 17	  status     text NOT NULL DEFAULT 'proposed' CHECK (status IN ('proposed','auto_approved','pending_hitl','approved','rejected','executed')),
> 18	  rationale  text,
> 19	  created_at timestamptz NOT NULL DEFAULT timezone('utc'::text, now()),
> 20	  updated_at timestamptz NOT NULL DEFAULT timezone('utc'::text, now())
> 21	);
> 22	
> 23	ALTER TABLE public.intent_plans ENABLE ROW LEVEL SECURITY;
> 24	CREATE POLICY "intent_plans_select_own" ON public.intent_plans FOR SELECT USING (auth.uid() = user_id);
> 25	CREATE POLICY "intent_plans_insert_own" ON public.intent_plans FOR INSERT WITH CHECK (auth.uid() = user_id);
> 26	CREATE POLICY "intent_plans_update_own" ON public.intent_plans FOR UPDATE USING (auth.uid() = user_id) WITH CHECK (auth.uid() = user_id);
> 27	CREATE POLICY "intent_plans_delete_own" ON public.intent_plans FOR DELETE USING (auth.uid() = user_id);
> 28	
> 29	CREATE INDEX IF NOT EXISTS idx_intent_plans_user ON public.intent_plans (user_id);
> 30	CREATE INDEX IF NOT EXISTS idx_intent_plans_hitl ON public.intent_plans (user_id, created_at DESC) WHERE status = 'pending_hitl';
> 31	
> 32	CREATE TRIGGER tr_update_intent_plans_updated_at
> 33	  BEFORE UPDATE ON public.intent_plans
> 34	  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
> 35	
> ```

## 🤖 Claude *(02:03:01)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260603270000_intent_plans_transition_guard_and_bindings.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: intent_plans OTD-INTENT-TRANSITION-GUARD + outward dispatch bindings (FR-MH-009 un-gate, v6.27.1).
> 2	-- BoK SSOT: docs/bok/marketing-hub/06-data-model.md (§intent_plans) + 04-frd.md FR-MH-009 + 05-sdd.md
> 3	--           (§intent-execute outward dispatch + STRIDE "ação de alto impacto sem revisão = Tampering → HITL").
> 4	-- SOP: docs/processes/intent-plan-execution.md.
> 5	--
> 6	-- TWO defenses-in-depth that arm the executor to dispatch outward safely:
> 7	--   (1) OTD-INTENT-TRANSITION-GUARD — a BEFORE UPDATE trigger that lets ONLY the service_role move status to
> 8	--       'approved' or 'executed'. The HITL approval AND the execute transition both run through intent-execute
> 9	--       (service role). A tenant tampering with their OWN row via PostgREST (RLS update_own grants UPDATE on own
> 10	--       rows, incl. the status column) is blocked here — so they cannot self-approve past the human HITL gate and
> 11	--       then ride intent-execute's re-validation (which trusts status='approved') into a real outward dispatch.
> 12	--   (2) Binding tenant-validation — campaign_id / enrollment_id let the executor route to campaign-run /
> 13	--       nurture-dispatch; a BEFORE INSERT/UPDATE trigger enforces the bound entity belongs to the plan's owner
> 14	--       (defense-in-depth ON TOP of the dispatch-time ownership guards already in those edge fns: a foreign id
> 15	--       there yields 404, an inert dispatch — this stops the junk binding from ever being stored).
> 16	
> 17	-- ── Outward dispatch bindings (nullable; the executor routes on them). Plain FK + ON DELETE SET NULL:
> 18	--    a composite (id,user_id) FK with SET NULL would try to NULL the NOT NULL user_id on parent delete — wrong;
> 19	--    the tenant match is enforced by tr_validate_intent_plan_bindings below instead. ──
> 20	ALTER TABLE public.intent_plans
> 21	  ADD COLUMN IF NOT EXISTS campaign_id   uuid REFERENCES public.campaigns(id)            ON DELETE SET NULL,
> 22	  ADD COLUMN IF NOT EXISTS enrollment_id uuid REFERENCES public.sequence_enrollments(id) ON DELETE SET NULL;
> 23	
> 24	CREATE INDEX IF NOT EXISTS idx_intent_plans_campaign   ON public.intent_plans (campaign_id)   WHERE campaign_id   IS NOT NULL;
> 25	CREATE INDEX IF NOT EXISTS idx_intent_plans_enrollment ON public.intent_plans (enrollment_id) WHERE enrollment_id IS NOT NULL;
> 26	
> 27	-- ── (1) Transition guard: only service_role may set status → approved | executed ──
> 28	CREATE OR REPLACE FUNCTION public.guard_intent_plan_transition()
> 29	RETURNS trigger
> 30	LANGUAGE plpgsql
> 31	SECURITY DEFINER
> 32	SET search_path = ''
> 33	AS $$
> 34	BEGIN
> 35	  IF NEW.status IS DISTINCT FROM OLD.status
> 36	     AND NEW.status IN ('approved', 'executed')
> 37	     AND auth.role() IS DISTINCT FROM 'service_role'
> 38	  THEN
> 39	    -- Self-protection: a forensic line to the Postgres server log. It survives the rollback that the EXCEPTION
> 40	    -- triggers — an INSERT into infra_health_logs here would be rolled back with the aborted statement, so it
> 41	    -- could not be persisted to a table. Errors (incl. this EXCEPTION) are logged by Postgres regardless.
> 42	    RAISE WARNING 'intent_plans transition guard: blocked %->% on plan % (role=%)',
> 43	      OLD.status, NEW.status, OLD.id, COALESCE(auth.role(), 'none');
> 44	    RAISE EXCEPTION 'Transição para "%" exige service_role (use o fluxo HITL via intent-execute).', NEW.status
> 45	      USING ERRCODE = '42501';
> 46	  END IF;
> 47	  RETURN NEW;
> 48	END;
> 49	$$;
> 50	
> 51	REVOKE EXECUTE ON FUNCTION public.guard_intent_plan_transition() FROM PUBLIC, anon, authenticated;
> 52	
> 53	DROP TRIGGER IF EXISTS tr_guard_intent_plan_transition ON public.intent_plans;
> 54	CREATE TRIGGER tr_guard_intent_plan_transition
> 55	  BEFORE UPDATE ON public.intent_plans
> 56	  FOR EACH ROW EXECUTE FUNCTION public.guard_intent_plan_transition();
> 57	
> 58	-- ── (2) Binding tenant-validation: a bound campaign/enrollment must belong to the plan's owner ──
> 59	CREATE OR REPLACE FUNCTION public.validate_intent_plan_bindings()
> 60	RETURNS trigger
> 61	LANGUAGE plpgsql
> 62	SECURITY DEFINER
> 63	SET search_path = ''
> 64	AS $$
> 65	BEGIN
> 66	  IF NEW.campaign_id IS NOT NULL
> 67	     AND NOT EXISTS (SELECT 1 FROM public.campaigns c WHERE c.id = NEW.campaign_id AND c.user_id = NEW.user_id)
> 68	  THEN
> 69	    RAISE EXCEPTION 'campaign_id % não pertence ao tenant do plano.', NEW.campaign_id USING ERRCODE = '42501';
> 70	  END IF;
> 71	  IF NEW.enrollment_id IS NOT NULL
> 72	     AND NOT EXISTS (SELECT 1 FROM public.sequence_enrollments e WHERE e.id = NEW.enrollment_id AND e.user_id = NEW.user_id)
> 73	  THEN
> 74	    RAISE EXCEPTION 'enrollment_id % não pertence ao tenant do plano.', NEW.enrollment_id USING ERRCODE = '42501';
> 75	  END IF;
> 76	  RETURN NEW;
> 77	END;
> 78	$$;
> 79	
> 80	REVOKE EXECUTE ON FUNCTION public.validate_intent_plan_bindings() FROM PUBLIC, anon, authenticated;
> 81	
> 82	DROP TRIGGER IF EXISTS tr_validate_intent_plan_bindings ON public.intent_plans;
> 83	CREATE TRIGGER tr_validate_intent_plan_bindings
> 84	  BEFORE INSERT OR UPDATE ON public.intent_plans
> 85	  FOR EACH ROW EXECUTE FUNCTION public.validate_intent_plan_bindings();
> 86	
> ```

## 🤖 Claude *(02:03:01)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/intent-execute/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// intent-execute — marketing-hub FR-MH-009 HITL transitions (approve / reject / execute) + REAL outward dispatch.
> 2	// SSOT: docs/bok/marketing-hub/04-frd.md FR-MH-009 + 05-sdd.md (§intent-execute) + docs/processes/intent-plan-execution.md.
> 3	//
> 4	// The HITL half of the Intent Orchestrator: drives the intent_plans state machine
> 5	//   proposed → auto_approved | pending_hitl → approved | rejected → executed → [outward dispatch]
> 6	// SECURITY (the directive's golden rule): `execute` RE-VALIDATES the outward action via the SHARED policy gate
> 7	// (_shared/intent-policy.ts) — it NEVER trusts the stored policy/status. A plan containing a high-impact task can
> 8	// only execute if a human has explicitly approved it (status='approved'), even if the row says auto_approved (AI
> 9	// mislabel OR direct PostgREST tampering). Defense-in-depth at the DB: tr_guard_intent_plan_transition lets ONLY
> 10	// the service_role move status to approved/executed (migration 20260603270000), so a tenant cannot self-approve
> 11	// via PostgREST and ride this re-validation into a dispatch.
> 12	//
> 13	// OUTWARD DISPATCH (un-gate v6.27.1): after governance (status=executed) the executor performs the REAL outward
> 14	// action, routing on the plan's bindings (campaign_id → campaign-run · enrollment_id → nurture-dispatch · else
> 15	// content/social/affiliate channels → orchestrate-content), forwarding the caller's JWT so the whole cascade
> 16	// self-bills the SAME tenant under RLS. Cost 0 here: it governs; the target self-bills + applies its own gates.
> 17	// Kill-switch INTENT_OUTWARD_DISPATCH_ENABLED=false reverts to governance-only (self-protection). JWT-guarded
> 18	// (verify_jwt=false + in-function getUser — edge-jwt SOP).
> 19	import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
> 20	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 21	import { planIsHighImpact, type PlanTask } from "../_shared/intent-policy.ts";
> 22	
> 23	const corsHeaders = {
> 24	  "Access-Control-Allow-Origin": "*",
> 25	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 26	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> 27	};
> 28	
> 29	type Decision = "approve" | "reject" | "execute";
> 30	const DECISIONS: Decision[] = ["approve", "reject", "execute"];
> 31	
> 32	interface DispatchResult { target: string; http_status: number; ok: boolean; detail: string }
> 33	
> 34	// channel -> orchestrate-content platforms (mirrors campaign-run). email/none/unknown are nurture territory (need an
> 35	// enrollment binding), NOT servable via orchestrate-content.
> 36	function channelToPlatforms(channel?: string): string[] {
> 37	  switch ((channel ?? "").toLowerCase()) {
> 38	    case "content": return ["wordpress"];
> 39	    case "affiliate": return ["wordpress"];
> 40	    case "social": return ["linkedin", "twitter"];
> 41	    default: return [];
> 42	  }
> 43	}
> 44	
> 45	serve(async (req) => {
> 46	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 47	  const json = (b: unknown, s = 200) =>
> 48	    new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 49	
> 50	  const url = Deno.env.get("SUPABASE_URL")!;
> 51	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 52	  const anonKey = (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!;
> 53	  const admin = createClient(url, serviceKey);
> 54	  const logErr = () => admin.from("infra_health_logs").insert({ service: "intent-execute", status: "unhealthy" }).then(() => {}, () => {});
> 55	
> 56	  try {
> 57	    const authHeader = req.headers.get("Authorization");
> 58	    if (!authHeader) return json({ error: "Missing authorization" }, 401);
> 59	    const userClient = createClient(url, anonKey, { global: { headers: { Authorization: authHeader } } });
> 60	    const { data: { user }, error: authError } = await userClient.auth.getUser();
> 61	    if (authError || !user) return json({ error: "Unauthorized" }, 401);
> 62	
> 63	    const { plan_id, decision } = await req.json().catch(() => ({}));
> 64	    if (!plan_id || typeof plan_id !== "string") return json({ error: "plan_id é obrigatório" }, 422);
> 65	    if (!DECISIONS.includes(decision)) return json({ error: "decision deve ser approve, reject ou execute" }, 422);
> 66	
> 67	    // Tenant guard: load the plan scoped to the caller (service role + explicit user_id). Foreign plan → 404.
> 68	    const { data: row, error: loadErr } = await admin
> 69	      .from("intent_plans").select("*").eq("id", plan_id).eq("user_id", user.id).maybeSingle();
> 70	    if (loadErr) { logErr(); return json({ error: "Falha ao carregar o plano", detail: loadErr.message }, 500); }
> 71	    if (!row) return json({ error: "Plano não encontrado" }, 404);
> 72	
> 73	    const status: string = row.status;
> 74	
> 75	    // ── APPROVE: only a pending_hitl plan can be human-approved. ──
> 76	    if (decision === "approve") {
> 77	      if (status !== "pending_hitl") return json({ error: `Não é possível aprovar um plano em status "${status}"`, status }, 409);
> 78	      const { error } = await admin.from("intent_plans").update({ status: "approved" }).eq("id", plan_id).eq("user_id", user.id);
> 79	      if (error) { logErr(); return json({ error: "Falha ao aprovar", detail: error.message }, 500); }
> 80	      admin.from("infra_health_logs").insert({ service: "intent-execute", status: "healthy" }).then(() => {}, () => {});
> 81	      return json({ status: "ok", plan_id, plan_status: "approved" });
> 82	    }
> 83	
> 84	    // ── REJECT: terminal; allowed from any non-executed state (idempotent if already rejected). ──
> 85	    if (decision === "reject") {
> 86	      if (status === "executed") return json({ error: "Plano já executado não pode ser rejeitado", status }, 409);
> 87	      if (status === "rejected") return json({ status: "ok", plan_id, plan_status: "rejected", already: true });
> 88	      const { error } = await admin.from("intent_plans").update({ status: "rejected" }).eq("id", plan_id).eq("user_id", user.id);
> 89	      if (error) { logErr(); return json({ error: "Falha ao rejeitar", detail: error.message }, 500); }
> 90	      admin.from("infra_health_logs").insert({ service: "intent-execute", status: "healthy" }).then(() => {}, () => {});
> 91	      return json({ status: "ok", plan_id, plan_status: "rejected" });
> 92	    }
> 93	
> 94	    // ── EXECUTE: the security-critical path. ──
> 95	    if (status === "executed") return json({ status: "ok", plan_id, plan_status: "executed", already: true }); // idempotent: no re-dispatch
> 96	    if (status === "rejected") return json({ error: "Plano rejeitado não pode ser executado", status }, 409);
> 97	
> 98	    // DEFENSE-IN-DEPTH: re-run the SAME policy gate on the STORED plan. Never trust the persisted policy/status.
> 99	    // A high-impact plan executes ONLY if a human explicitly approved it (status='approved').
> 100	    const highImpact = planIsHighImpact(row.plan);
> 101	    if (highImpact && status !== "approved") {
> 102	      return json({
> 103	        error: "Plano de alto impacto exige aprovação humana (HITL) antes de executar.",
> 104	        code: "hitl_required", status,
> 105	      }, 409);
> 106	    }
> 107	
> 108	    // Mark executed FIRST (governance). Idempotency: a duplicate/concurrent execute now short-circuits on
> 109	    // status='executed' above → no double dispatch, no double charge.
> 110	    const { error: updErr } = await admin.from("intent_plans")
> 111	      .update({ status: "executed" }).eq("id", plan_id).eq("user_id", user.id);
> 112	    if (updErr) { logErr(); return json({ error: "Falha ao marcar como executado", detail: updErr.message }, 500); }
> 113	
> 114	    // ── OUTWARD DISPATCH (un-gate): route on bindings, forward the caller's JWT (cascade self-bills same tenant). ──
> 115	    const dispatchEnabled = (Deno.env.get("INTENT_OUTWARD_DISPATCH_ENABLED") ?? "true").toLowerCase() !== "false";
> 116	    const tasks: PlanTask[] = Array.isArray(row.plan) ? row.plan : [];
> 117	    const dispatches: DispatchResult[] = [];
> 118	
> 119	    const callFn = async (target: string, body: unknown): Promise<DispatchResult> => {
> 120	      const ctrl = new AbortController();
> 121	      const to = setTimeout(() => ctrl.abort(), 60_000);
> 122	      try {
> 123	        const resp = await fetch(`${url}/functions/v1/${target}`, {
> 124	          method: "POST",
> 125	          headers: { "Content-Type": "application/json", Authorization: authHeader },
> 126	          body: JSON.stringify(body), signal: ctrl.signal,
> 127	        });
> 128	        let detail = "";
> 129	        try { const jb = await resp.json(); detail = jb?.run_id ?? jb?.status ?? jb?.error ?? jb?.reason ?? ""; } catch { /* non-JSON */ }
> 130	        return { target, http_status: resp.status, ok: resp.ok, detail: String(detail).slice(0, 200) };
> 131	      } catch (e) {
> 132	        const aborted = (e as Error)?.name === "AbortError";
> 133	        return { target, http_status: 0, ok: false, detail: aborted ? "timeout" : String((e as Error)?.message ?? e).slice(0, 200) };
> 134	      } finally { clearTimeout(to); }
> 135	    };
> 136	
> 137	    let outward: "gated" | "none" | "dispatched" | "failed";
> 138	    if (!dispatchEnabled) {
> 139	      outward = "gated"; // kill-switch: governance-only.
> 140	    } else if (row.campaign_id) {
> 141	      dispatches.push(await callFn("campaign-run", { campaign_id: row.campaign_id }));
> 142	      outward = dispatches[dispatches.length - 1].ok ? "dispatched" : "failed";
> 143	    } else if (row.enrollment_id) {
> 144	      dispatches.push(await callFn("nurture-dispatch", { enrollment_id: row.enrollment_id }));
> 145	      outward = dispatches[dispatches.length - 1].ok ? "dispatched" : "failed";
> 146	    } else {
> 147	      const platforms = Array.from(new Set(tasks.flatMap((t) => channelToPlatforms(t.channel))));
> 148	      if (platforms.length === 0) {
> 149	        outward = "none"; // nothing outward to send (e.g., a low-impact 'none' plan) — governance only.
> 150	      } else {
> 151	        dispatches.push(await callFn("orchestrate-content", { topic: String(row.intent).slice(0, 280), platforms, wp_status: "draft" }));
> 152	        outward = dispatches[dispatches.length - 1].ok ? "dispatched" : "failed";
> 153	      }
> 154	    }
> 155	
> 156	    // Knowledge Mesh observation (mandate: every orchestration run). Fire-and-forget.
> 157	    const taskCount = tasks.length;
> 158	    admin.from("mcorch_nodes").insert({
> 159	      node_type: "observation", name: `intent-exec-${plan_id}`,
> 160	      content: `Intent plan executed: "${String(row.intent).slice(0, 140)}" (${taskCount} tarefas · high_impact=${highImpact}) · outward=${outward}${dispatches.length ? ` [${dispatches.map((d) => `${d.target}:${d.http_status}`).join(", ")}]` : ""}`,
> 161	      user_id: user.id,
> 162	    }).then(() => {}, () => {});
> 163	    admin.from("infra_health_logs").insert({ service: "intent-execute", status: outward === "failed" ? "degraded" : "healthy" }).then(() => {}, () => {});
> 164	
> 165	    return json({
> 166	      status: "ok", plan_id, plan_status: "executed",
> 167	      high_impact: highImpact, tasks: row.plan,
> 168	      outward_dispatch: outward, dispatch: dispatches,
> 169	    });
> 170	  } catch (err) {
> 171	    logErr();
> 172	    return json({ error: "Erro interno no intent-execute", detail: String((err as Error)?.message ?? err) }, 500);
> 173	  }
> 174	});
> 175	
> ```

## 🤖 Claude *(02:03:06)*

I have the three core files. Now let me verify the callees and the shared policy gate, plus check whether there's any REVOKE on `intent_plans` INSERT for authenticated, and look at the git history to confirm what's actually deployed (the CLAUDE.md warns about worktree staleness).

## 🤖 Claude *(02:03:08)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/intent-policy.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// Shared policy gate for the Intent Orchestrator (FR-MH-009). SSOT: docs/bok/marketing-hub/04-frd.md FR-MH-009 +
> 2	// 05-sdd.md STRIDE "ação de alto impacto sem revisão = Tampering → policy engine + HITL obrigatório".
> 3	//
> 4	// This is the SINGLE source of the high-impact decision. `intent-orchestrate` runs it to set policy/status at
> 5	// creation; `intent-execute` re-runs it at execution time as defense-in-depth (NEVER trust the stored
> 6	// policy/status — an outward action must clear this gate again before it can execute).
> 7	
> 8	export interface PlanTask {
> 9	  action: string;
> 10	  channel?: string;
> 11	  impact?: "low" | "medium" | "high";
> 12	  rationale?: string;
> 13	}
> 14	
> 15	// High-impact = outward / financial actions that MUST NOT run without human review (the HITL gate).
> 16	export const HIGH_IMPACT_RE =
> 17	  /(publi|send|e-?mail|post|tweet|spend|ad[_-]?spend|charge|cobr|envi|dispar|whats|launch|lança)/i;
> 18	
> 19	// Fail-safe channel rule: ANY outward channel (anything that is not the internal 'none'/'content') is high-impact,
> 20	// even if the AI mislabels impact=low or phrases the action verb to dodge the regex. Unknown channel → outward.
> 21	export const isOutwardChannel = (c?: string): boolean =>
> 22	  !!c && !["none", "content"].includes(c.toLowerCase());
> 23	
> 24	export function isHighImpactTask(t: PlanTask): boolean {
> 25	  return t?.impact === "high" || HIGH_IMPACT_RE.test(t?.action ?? "") || isOutwardChannel(t?.channel);
> 26	}
> 27	
> 28	/**
> 29	 * True if ANY task in the plan is high-impact → mandatory human approval (HITL) before execution.
> 30	 * FAIL-CLOSED: a malformed/non-array plan (e.g. a tampered jsonb object) is treated as high-impact, so the
> 31	 * re-validation in intent-execute can never be skipped by sending a plan shape the gate doesn't recognize.
> 32	 */
> 33	export function planIsHighImpact(tasks: unknown): boolean {
> 34	  if (!Array.isArray(tasks)) return true;
> 35	  return tasks.some((t) => isHighImpactTask(t as PlanTask));
> 36	}
> 37	
> ```

## 🤖 Claude *(02:03:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"REVOKE\" supabase/migrations/ | grep -i \"intent_plans\" ; echo \"---GRANT---\" ; grep -rn \"GRANT\" supabase/migrations/ | grep -i \"intent_plans\" ; echo \"---done---\"",
  "description": "Search for REVOKE/GRANT on intent_plans table"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> supabase/migrations/20260603270000_intent_plans_transition_guard_and_bindings.sql:51:REVOKE EXECUTE ON FUNCTION public.guard_intent_plan_transition() FROM PUBLIC, anon, authenticated;
> supabase/migrations/20260603270000_intent_plans_transition_guard_and_bindings.sql:80:REVOKE EXECUTE ON FUNCTION public.validate_intent_plan_bindings() FROM PUBLIC, anon, authenticated;
> ---GRANT---
> ---done---
> ```

## 🤖 Claude *(02:03:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -5 -- supabase/migrations/20260603270000_intent_plans_transition_guard_and_bindings.sql supabase/functions/intent-execute/index.ts ; echo \"---branch status---\" ; git status --short ; echo \"---origin compare---\" ; git rev-list --count HEAD..origin/main 2>/dev/null || echo \"no origin/main diff or not fetched\"",
  "description": "Check git history and origin sync for the relevant files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 0021189 feat(marketing-hub): executor de intent_plans com re-validação outward (FR-MH-009 HITL)
> ---branch status---
>  M docs/processes/intent-plan-execution.md
>  M src/components/marketing/HITLApprovalCard.tsx
>  M src/hooks/useIntentOrchestrator.ts
>  M supabase/functions/intent-execute/index.ts
>  A supabase/migrations/20260603270000_intent_plans_transition_guard_and_bindings.sql
> ---origin compare---
> 0
> ```

## 🤖 Claude *(02:03:15)*

The migration `20260603270000` is uncommitted (status `A`) and `intent-execute/index.ts` is modified. This is a candidate finding for a change in progress. The REVOKE statements only target the trigger functions, not the table INSERT privilege — so authenticated retains its default INSERT grant on `intent_plans`.

Now let me verify the critical facts: (1) confirm the callees only check ownership, and (2) confirm there's no `service_role`-only path that would prevent the user from approving themselves anyway. Let me also check the orchestrate-step config and the callees' approval awareness.

## 🤖 Claude *(02:03:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== campaign-run user_id checks ===\" ; grep -n \"user_id\\|user\\.id\\|hitl\\|intent\\|approv\\|getUser\\|auth\" supabase/functions/campaign-run/index.ts | head -40 ; echo \"\" ; echo \"=== nurture-dispatch user_id checks ===\" ; grep -n \"user_id\\|user\\.id\\|hitl\\|intent\\|approv\\|getUser\\|consent\" supabase/functions/nurture-dispatch/index.ts | head -40",
  "description": "Check callees for ownership-only checks and absence of HITL awareness"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === campaign-run user_id checks ===
> 19:  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> 55:    const authHeader = req.headers.get("Authorization");
> 56:    if (!authHeader) return json({ error: "Missing authorization" }, 401);
> 58:    const userClient = createClient(url, anonKey, { global: { headers: { Authorization: authHeader } } });
> 59:    const { data: { user }, error: authError } = await userClient.auth.getUser();
> 60:    if (authError || !user) return json({ error: "Unauthorized" }, 401);
> 68:      .select("id, user_id, name, intent, status, mesh_node_id")
> 69:      .eq("id", campaign_id).eq("user_id", user.id).maybeSingle();
> 76:      .eq("campaign_id", campaign_id).eq("user_id", user.id)
> 81:    const { data: bal } = await admin.from("profiles").select("mco_balance").eq("id", user.id).maybeSingle();
> 83:    const { error: deductErr } = await admin.rpc("deduct_mco_coins", { p_user_id: user.id, p_amount: CAMPAIGN_RUN_COST });
> 87:    const topic = campaign.intent?.trim() || campaign.name; // orchestrate-content requires a topic; name is NOT NULL.
> 90:    await admin.from("campaigns").update({ status: "active" }).eq("id", campaign_id).eq("user_id", user.id);
> 96:      await admin.from("campaign_steps").update({ status: "blocked" }).eq("id", s.id).eq("user_id", user.id);
> 104:        await admin.from("campaign_steps").update({ status: "running" }).eq("id", step.id).eq("user_id", user.id);
> 111:            headers: { "Content-Type": "application/json", Authorization: authHeader },
> 116:          await admin.from("campaign_steps").update({ status: ok ? "done" : "error" }).eq("id", step.id).eq("user_id", user.id);
> 119:          await admin.from("campaign_steps").update({ status: "error" }).eq("id", step.id).eq("user_id", user.id);
> 144:        user_id: user.id,
> 156:    const { data: newBal } = await admin.from("profiles").select("mco_balance").eq("id", user.id).maybeSingle();
> 
> === nurture-dispatch user_id checks ===
> 2:// §nurture-dispatch + STRIDE row "Nurturing dispatch / Envio sem consentimento = Critical"). Dispatches the CURRENT
> 4:// non-withdrawn consent — the Critical mitigation) · respects opt-out · idempotent (advances current_step) ·
> 42:    // Two invocation modes (mirrors orchestrate-step). USER: a logged-in caller — the JWT is validated via getUser().
> 43:    // SERVICE (nurture-cron): presents the SB_SECRET_KEY + an explicit user_id it resolved from the due enrollment.
> 44:    // Only the service-key holder can take the service path, so its user_id is trusted (an attacker cannot forge it).
> 46:    if (authHeader === `Bearer ${serviceKey}` && typeof body?.user_id === "string") {
> 47:      userId = body.user_id;
> 50:      const { data: { user: authedUser }, error: authError } = await userClient.auth.getUser();
> 58:      .select("id, user_id, sequence_id, lead_id, current_step, status")
> 59:      .eq("id", enrollment_id).eq("user_id", userId).maybeSingle();
> 66:    // ── CONSENT GATE (STRIDE-Critical) — NEVER generate/charge/record without a granted, non-withdrawn consent.
> 67:    const { data: consent } = await admin
> 68:      .from("marketing_consents")
> 70:      .eq("lead_id", enr.lead_id).eq("user_id", userId)
> 73:    if (!consent) {
> 74:      // pause so the cron stops retrying a non-consented lead; operator resumes once consent is obtained.
> 75:      await admin.from("sequence_enrollments").update({ status: "paused" }).eq("id", enrollment_id).eq("user_id", userId);
> 77:      return json({ status: "blocked", reason: "consent_required", enrollment_id });
> 82:      .from("sequences").select("id, name, steps, active").eq("id", enr.sequence_id).eq("user_id", userId).maybeSingle();
> 87:      await admin.from("sequence_enrollments").update({ status: "completed", next_run_at: null }).eq("id", enrollment_id).eq("user_id", userId);
> 92:    // mcoCoins gatekeeper — only AFTER the consent gate passed.
> 95:    const { error: deductErr } = await admin.rpc("deduct_mco_coins", { p_user_id: userId, p_amount: DISPATCH_COST });
> 99:    const { data: keys } = await admin.from("decrypted_user_api_keys").select("*").eq("user_id", userId).maybeSingle();
> 134:      lead_id: enr.lead_id, user_id: userId, channel: step.channel ?? "email", event_type: "message_sent",
> 145:      .eq("id", enrollment_id).eq("user_id", userId);
> ```

## 🤖 Claude *(02:03:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== orchestrate-content HITL/intent awareness ===\" ; grep -n \"hitl\\|intent_plan\\|approv\" supabase/functions/orchestrate-content/index.ts | head ; echo \"(empty = no HITL concept)\" ; echo \"\" ; echo \"=== Default privileges / ALTER DEFAULT PRIVILEGES anywhere granting authenticated ===\" ; grep -rln \"ALTER DEFAULT PRIVILEGES\" supabase/migrations/ | head ; echo \"\" ; echo \"=== Any global REVOKE from authenticated on public tables? ===\" ; grep -rn \"REVOKE.*ON ALL TABLES\\|REVOKE INSERT\" supabase/migrations/ | head",
  "description": "Check orchestrate-content HITL awareness and default privilege grants"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === orchestrate-content HITL/intent awareness ===
> (empty = no HITL concept)
> 
> === Default privileges / ALTER DEFAULT PRIVILEGES anywhere granting authenticated ===
> 
> === Any global REVOKE from authenticated on public tables? ===
> ```

## 🤖 Claude *(02:03:27)*

All facts are confirmed. The callees only check tenant ownership and have zero HITL/intent-plan awareness. Now the critical question for the score: is this a *meaningful* escalation, given the user could legitimately call `decision='approve'` on their own plan anyway?

Let me trace the legitimate approve path carefully to confirm whether self-INSERT of `'approved'` actually bypasses a real control, or merely replicates something the user can already do.

The legitimate path requires `status === "pending_hitl"` to approve (line 77). The question is: **can a user get a high-impact plan into `pending_hitl` and approve it themselves, all on their own, with no separate human?** Let me check `intent-orchestrate` to see who controls the transition to `pending_hitl`, and confirm the approve step has no second-party/role requirement.

## 🤖 Claude *(02:03:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== intent-orchestrate: who sets status, any role/second-party gate on creation ===\" ; grep -n \"status\\|pending_hitl\\|auto_approved\\|getUser\\|user\\.id\\|insert\\|policy\" supabase/functions/intent-orchestrate/index.ts | head -40",
  "description": "Inspect intent-orchestrate status-setting logic"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === intent-orchestrate: who sets status, any role/second-party gate on creation ===
> 2:// STRIDE "Intent Orchestrator / ação de alto impacto sem revisão = Tampering → policy engine + HITL obrigatório").
> 3:// Translates a natural-language marketing intent into a task plan; a policy engine decides auto vs HITL; ANY
> 5:// rationale to intent_plans. JWT-guarded (verify_jwt=false + in-function getUser — edge-jwt SOP). Cost 0: it
> 10:import { planIsHighImpact, type PlanTask } from "../_shared/intent-policy.ts";
> 21:    new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 32:    const { data: { user }, error: authError } = await userClient.auth.getUser();
> 39:    const { data: keys } = await admin.from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 91:    // Shared gate (_shared/intent-policy.ts) — intent-execute re-runs the SAME gate at execution time.
> 93:    const policy: "auto" | "hitl" = highImpact ? "hitl" : "auto";
> 94:    const status = highImpact ? "pending_hitl" : "auto_approved";
> 104:      .insert({ user_id: user.id, intent: intent.slice(0, 2000), plan: tasks, policy, status, rationale })
> 107:      admin.from("infra_health_logs").insert({ service: "intent-orchestrate", status: "unhealthy" }).then(() => {}, () => {});
> 112:    admin.from("mcorch_nodes").insert({
> 114:      content: `Intent: ${intent.slice(0, 200)} → policy=${policy} status=${status} (${tasks.length} tarefas)`,
> 115:      user_id: user.id,
> 117:    admin.from("infra_health_logs").insert({ service: "intent-orchestrate", status: "healthy" }).then(() => {}, () => {});
> 119:    return json({ status: "ok", plan_id: row.id, policy, plan_status: status, tasks, rationale, source: heuristic ? "heuristic" : "ai" });
> 121:    admin.from("infra_health_logs").insert({ service: "intent-orchestrate", status: "unhealthy" }).then(() => {}, () => {});
> ```

## 🤖 Claude *(02:03:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== config.toml: verify_jwt for the relevant functions ===\" ; grep -n -A2 \"intent-execute\\|intent-orchestrate\\|campaign-run\\|nurture-dispatch\\|orchestrate-content\" supabase/config.toml | head -40",
  "description": "Check verify_jwt config for involved functions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === config.toml: verify_jwt for the relevant functions ===
> 16:[functions.orchestrate-content]
> 17-verify_jwt = false
> 18-[functions.orchestrate-step]
> --
> 20:[functions.nurture-dispatch]
> 21-verify_jwt = false
> 22-[functions.nurture-cron]
> --
> 24:[functions.intent-orchestrate]
> 25-verify_jwt = false
> 26:[functions.intent-execute]
> 27-verify_jwt = false
> 28-[functions.aeo-audit]
> ```

## 🤖 Claude *(02:03:41)*

Now I have the complete picture. This is the decisive finding for scoring. Let me analyze the actual escalation question.

The critical observation: **The "approve" step in `intent-execute` (lines 76-82) has NO second-party requirement and NO role check beyond tenant ownership.** The same authenticated user who created the plan calls `decision: "approve"` with their own JWT, and the service role inside the function flips `pending_hitl → approved`. There is no separate human approver, no admin role, no out-of-band confirmation. The "human in the loop" IS the tenant themselves.

This means: a user can *already*, through the entirely legitimate sanctioned flow, take a high-impact plan to `executed` + outward dispatch with zero external approval:
1. `intent-orchestrate` → plan lands in `pending_hitl` (server-controlled).
2. `intent-execute {decision:"approve"}` → `approved` (same user, same JWT).
3. `intent-execute {decision:"execute"}` → `executed` + outward dispatch.

The direct-INSERT-`approved` path collapses step 1+2 but reaches the **identical** end state the user is already authorized to reach. The thing it "bypasses" — the HITL gate — is a gate the resource owner self-satisfies anyway. There is no privilege boundary crossed: the user dispatches against their *own* campaigns/enrollments/content, self-bills their *own* mcoCoins, under their *own* RLS. The callees confirm this: pure `.eq("user_id", user.id)` ownership, no concept of approval provenance.

Let me do one final check — whether `approved_by`/`approved_at` provenance columns exist anywhere (the claim says they don't), and whether any UI or downstream actually treats `executed` as an audit-trustworthy "a human reviewed this" signal that a third party relies on.

## 🤖 Claude *(02:03:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== approved_by / approved_at / reviewer provenance columns anywhere ===\" ; grep -rn \"approved_by\\|approved_at\\|reviewer\\|reviewed_by\" supabase/migrations/ supabase/functions/intent-execute/ supabase/functions/intent-orchestrate/ 2>/dev/null | head ; echo \"(empty = no provenance tracking)\" ; echo \"\" ; echo \"=== Does any OTHER role/admin consume intent_plans.status as a trust signal? ===\" ; grep -rn \"intent_plans\" supabase/ src/ --include=*.ts --include=*.tsx --include=*.sql -l 2>/dev/null",
  "description": "Check for approval provenance columns and downstream consumers of intent_plans.status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === approved_by / approved_at / reviewer provenance columns anywhere ===
> supabase/migrations/20260523194500_canvas_design.sql:45:  reviewer_email  text NOT NULL,
> (empty = no provenance tracking)
> 
> === Does any OTHER role/admin consume intent_plans.status as a trust signal? ===
> supabase/migrations/20260603260000_marketing_hub_aeo_audits.sql
> supabase/functions/intent-execute/index.ts
> supabase/functions/intent-orchestrate/index.ts
> src/integrations/supabase/types.ts
> supabase/migrations/20260603250000_marketing_hub_intent_plans.sql
> supabase/migrations/20260603270000_intent_plans_transition_guard_and_bindings.sql
> src/hooks/useIntentOrchestrator.ts
> ```

## 🤖 Claude *(02:04:13)*

Confirmed. No `approved_by`/`approved_at` provenance on `intent_plans` (the only match is an unrelated canvas-design table). The only consumers of `intent_plans` are the two intent edge functions and the tenant's own UI hook (`useIntentOrchestrator`) — there is no admin console, no second-party reviewer, no cross-tenant or privileged process that reads `status='approved'/'executed'` as a trust signal it relies on.

I have all the facts needed to render a verdict.

---

## VERDICT

**Confidence score: 3/10 — FALSE POSITIVE (not a meaningful, exploitable authorization escalation).**

### Every technical fact in the claim is TRUE, but the security conclusion is not

I confirmed all the mechanical facts:

1. **RLS does not restrict `status`** (`20260603250000:25`): `intent_plans_insert_own` is `WITH CHECK (auth.uid() = user_id)` only. The CHECK constraint (`:17`) lists `'approved'` and `'executed'` as legal values. No `REVOKE INSERT ... FROM authenticated`, no `ALTER DEFAULT PRIVILEGES` anywhere — the two `REVOKE` statements in `20260603270000:51,80` target only the trigger *functions*, not the table. So an authenticated tenant **can** `POST /rest/v1/intent_plans` with `status:"approved"` for their own `user_id`.

2. **The transition guard is `BEFORE UPDATE` only** (`20260603270000:54-56`) — it does **not** fire on INSERT. The binding validator **is** `BEFORE INSERT OR UPDATE` (`:83-85`) but does not inspect `status`. The inconsistency the claim flags is real: the INSERT path for `status` was overlooked, and the in-code comment at `intent-execute/index.ts:8-11` explicitly *claims* direct-PostgREST self-approval is prevented — which, for the INSERT vector, it is not.

3. **`intent-execute` execute path trusts `status==='approved'` with no provenance check** (`:101`): `if (highImpact && status !== "approved")` blocks; a self-planted `'approved'` passes, the service-role UPDATE to `'executed'` satisfies the UPDATE guard (`auth.role()='service_role'`), and outward dispatch fires. No `approved_by`/`approved_at` exists to cross-check (confirmed: zero provenance columns on this table).

4. **Callees check ownership only** (`campaign-run:69` `.eq("user_id", user.id)`; `nurture-dispatch:59` same + an *independent* consent gate at `:66-77`; `orchestrate-content` has zero HITL/intent awareness). Owning the resource is sufficient for the real action.

### Why it is not a meaningful escalation — no privilege boundary is crossed

The HITL "human" is the **tenant themselves**. The sanctioned approve step (`intent-execute:76-82`) requires nothing but tenant ownership of the row — no admin role, no second party, no out-of-band confirmation. So the *exact same end state* (high-impact plan → `executed` → outward dispatch) is **already reachable by the same user through the fully-blessed flow**: `intent-orchestrate` (lands `pending_hitl`) → `intent-execute {approve}` (same JWT) → `intent-execute {execute}`. The direct INSERT merely fuses two self-authorized calls into one; it reaches a state the user is **already authorized to reach against their own resources**. Every downstream effect stays inside the attacker's own tenant: dispatch hits *their* campaigns/enrollments/content, self-bills *their* mcoCoins, under *their* RLS, and `nurture-dispatch`'s consent gate (the actual STRIDE-Critical control protecting third parties) is **independent of `intent_plans` entirely** and is not bypassed. No other tenant, admin console, or privileged process consumes `intent_plans.status` as a trust signal (confirmed: only the two intent fns + the tenant's own UI hook read this table). With no provenance recorded, `executed` was never a trustworthy "a distinct human reviewed this" audit signal to begin with — so nothing downstream is deceived. The false-positive rules also bear on this: there's no privilege escalation, no cross-tenant access, no exfiltration; it's a self-service governance/state-machine integrity gap, not an authorization-boundary breach.

### The proposed fix is correct and worth doing — as integrity hardening, not vuln remediation

Extending the guard to `BEFORE INSERT OR UPDATE` and blocking non-`service_role` from inserting `status IN ('approved','executed')` (and/or tightening the insert RLS policy, e.g. `WITH CHECK (auth.uid() = user_id AND status IN ('proposed','auto_approved','pending_hitl'))`) **does fully close the described INSERT path** and makes the code comment's claim true. It correctly forces every approved/executed transition through the service-role state machine, closes the INSERT-vs-UPDATE inconsistency, and is the right call to make the governance model coherent and audit-defensible (and future-proof should a real second-party approver or admin reviewer ever consume `status`). One concrete caveat: an RLS `WITH CHECK` on INSERT is the cleaner enforcement point than the trigger, because `auth.role()` inside a `SECURITY DEFINER` trigger reflects the JWT role claim and `service_role` edge calls already use the service key — verify the guard's `service_role` exemption still lets `intent-orchestrate`'s legitimate `pending_hitl`/`auto_approved` INSERT through (it should, since those statuses aren't in the blocked set). I'd score the underlying issue **3/10**: real, narrow, worth fixing for state-machine integrity, but not a concrete exploitable escalation of privilege — the attacker gains nothing they couldn't already do to their own tenant.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-04 - agent-a453001108318c7ee]]
> * **Próxima Sessão**: [[2026-06-04 - agent-a5eb48930a1c31a08]]
%% --- TIMELINE END --- %%

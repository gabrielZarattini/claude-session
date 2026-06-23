# Session agent-abebbcac649b3cd15
**Date:** 2026-06-23 | **Session ID:** `agent-abebbcac649b3cd15`

---

## 👤 User *(04:34:51)*

You are a correctness reviewer.
The change implements FR-VA-018 ("Trend-informed angle") in `supabase/functions/autopilot-run/index.ts`. Read that file fully (focus the new trend
block roughly between the projected-cost line and the dry_run short-circuit, the new `import { inspectPrompt }`,
and the fan-out body where `topic: viralTopic`). The feature: autopilot-run reads a trend title from the GLOBAL
`vm_trends` table and weaves it into the per-cycle `topic` sent to the `orchestrate-content` edge function,
which feeds an LLM prompt. Trend text is UNTRUSTED (Apify/RapidAPI-mined). Before weaving, the code calls
`inspectPrompt(raw, userId, { rateLimit: false })` from `supabase/functions/_shared/sentinel.ts` and only uses
the trend when `.allow` is true (skip-and-continue across the top-5 candidates, mirroring the per-product gate in
`supabase/functions/orchestrate-content/index.ts` ~lines 158-183).
Return ONLY real, >=80%-confidence issues. Do not invent files. Do not run paid actions.
Read the sealed contract: FR-VA-018 row in `docs/bok/viral-autopilot/04-frd.md` and the sealed flow line
`topic: buildViralAngle(sanitize(product), sanitize(trends), variant)` in
`docs/bok/viral-autopilot/07-process-flow.md` (~line 181). Verify:
 (a) trend selection logic is correct: niche-filtered candidates first, GLOBAL fallback only when the niche-filtered
     query returns zero, top-5 by viral_score, iterate and take the first that passes the sentinel;
 (b) GRACEFUL when vm_trends is empty (the real current state) — viralTopic stays `plan.name`, no throw;
 (c) NO regression to the PAID path: the whole trend block is BEFORE the dry_run short-circuit AND wrapped in
     try/catch, so any trend/query error degrades to the plain angle and never aborts the cycle; begin_cycle /
     fan-out / finalize are otherwise unchanged;
 (d) dry_run response surfaces `trend_applied` + `viral_topic` for zero-cost verification;
 (e) the trend is resolved ONCE per cycle and reused across all sub-runs/variants (not re-queried per sub-run).
Flag genuine bugs (e.g. a fallback that never triggers, a query that throws on empty, a type error). Ignore style.

## 🤖 Claude *(04:34:53)*

I'll review the FR-VA-018 implementation. Let me start by reading the key files.

## 🤖 Claude *(04:34:55)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-run/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// autopilot-run — Viral Autopilot per-plan executor (FR-VA-002 / FR-VA-007 / FR-VA-016 / FR-VA-021). verify_jwt=false.
> 2	// SOP: docs/processes/autopilot-cron-identity.md.
> 3	//
> 4	// Identity (two paths):
> 5	//   - cron/service: Authorization === Bearer SB_SECRET_KEY + x-autopilot-user-id (the autopilot-cadence-cron
> 6	//     derived it from autopilot_plans.user_id). The header is re-validated by the TENANT-SCOPED plan load below.
> 7	//   - user "gerar agora": user JWT → getUser → the plan load is scoped to that user (IDOR-safe).
> 8	// Flow: load plan (tenant-scoped) → N_runs = products×platforms×ab_variants → projected = N_runs*10 + 2 →
> 9	//   begin_autopilot_cycle (ATOMIC cap-check + single pre-debit) → fan-out orchestrate-content (prepaid, no
> 10	//   self-bill) → finalize_autopilot_cycle(actual) → re-arm next_run_at. dry_run short-circuits after the cost
> 11	//   projection (no cycle, no deduct) — the zero-cost proof path.
> 12	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 13	import { inspectPrompt } from "../_shared/sentinel.ts";
> 14	
> 15	const corsHeaders = {
> 16	  "Access-Control-Allow-Origin": "*",
> 17	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 18	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-autopilot-user-id",
> 19	};
> 20	const ORCH_COST = 10;     // orchestrate-content flat bundle (image already included — billing.ts:16-21)
> 21	const ANALYZE_COST = 2;   // reserved for autopilot-analyze (R3); REFUNDED until that slice lands (see actual below)
> 22	const CONCURRENCY = 6;    // wall-clock bound on the fan-out (mirrors nurture-cron / campaign-run)
> 23	const UUID_RE = /^[0-9a-fA-F-]{36}$/;
> 24	
> 25	Deno.serve(async (req) => {
> 26	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 27	  const json = (b: unknown, s = 200) =>
> 28	    new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 29	
> 30	  const url = Deno.env.get("SUPABASE_URL")!;
> 31	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 32	  const pubKey = (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!;
> 33	  const admin = createClient(url, serviceKey);
> 34	  const logHealth = (status: string) =>
> 35	    admin.from("infra_health_logs").insert({ service: "autopilot-run", status }).then(() => {}, () => {});
> 36	
> 37	  try {
> 38	    const authHeader = req.headers.get("Authorization");
> 39	    if (!authHeader?.startsWith("Bearer ")) return json({ error: "Unauthorized" }, 401);
> 40	
> 41	    const body = await req.json().catch(() => ({}));
> 42	    const planId = typeof body?.plan_id === "string" ? body.plan_id : null;
> 43	    const dryRun = body?.dry_run === true;
> 44	    if (!planId || !UUID_RE.test(planId)) return json({ error: "plan_id (uuid) required" }, 422);
> 45	
> 46	    // ── Identity: service path (proven key + server-trusted header) OR user JWT path. ──────────────────────────
> 47	    const isService = authHeader === `Bearer ${serviceKey}`;
> 48	    let userId: string;
> 49	    if (isService) {
> 50	      const hdr = req.headers.get("x-autopilot-user-id");
> 51	      if (!hdr || !UUID_RE.test(hdr)) return json({ error: "x-autopilot-user-id (uuid) required for service path" }, 400);
> 52	      userId = hdr;
> 53	    } else {
> 54	      const userClient = createClient(url, pubKey, { global: { headers: { Authorization: authHeader } } });
> 55	      const { data: { user }, error } = await userClient.auth.getUser();
> 56	      if (error || !user) return json({ error: "Unauthorized" }, 401);
> 57	      userId = user.id;
> 58	    }
> 59	
> 60	    // ── Load plan TENANT-SCOPED (plan MUST belong to userId — cross-tenant/missing → 404). ───────────────────────
> 61	    const { data: plan } = await admin
> 62	      .from("autopilot_plans")
> 63	      .select("id, user_id, name, mode, interval_days, target_product_ids, platforms, ab_variants")
> 64	      .eq("id", planId).eq("user_id", userId).maybeSingle();
> 65	    if (!plan) return json({ error: "plan_not_found" }, 404);
> 66	
> 67	    const products = ((plan.target_product_ids ?? []) as unknown[]).filter((x): x is string => typeof x === "string" && x.length > 0);
> 68	    const platforms = ((plan.platforms ?? []) as unknown[]).filter((x): x is string => typeof x === "string" && x.length > 0);
> 69	    const abVariants = Math.max(1, Math.min(5, Number(plan.ab_variants ?? 1)));
> 70	    const nRuns = products.length * platforms.length * abVariants;
> 71	    if (nRuns < 1) return json({ error: "plan_has_no_targets", detail: "plano sem produtos/redes válidos" }, 422);
> 72	
> 73	    const projected = nRuns * ORCH_COST + ANALYZE_COST;
> 74	
> 75	    // ── FR-VA-018: trend-informed angle (cycle-level). Reconnects the trends island: pick a trend from vm_trends
> 76	    // (a GLOBAL shared catalog — no tenant scope) to steer THIS cycle's viral angle. Trend text is UNTRUSTED
> 77	    // (Apify/RapidAPI-mined) → the Cyber-Sentinel gates it BEFORE it reaches any prompt (NFR-VA-008), mirroring the
> 78	    // per-product gate in orchestrate-content (skip-and-continue: a blocked trend is dropped, not the whole angle).
> 79	    // Relevance: prefer a trend whose niche overlaps the cycle's products; else the freshest top-viral active trend.
> 80	    // Defense-in-depth: orchestrate-content re-inspects the full topic, so this is the first of two gates.
> 81	    // Graceful: empty vm_trends (the steady state until fetch-trends runs) → angle stays the plain product topic.
> 82	    let viralTopic = plan.name;
> 83	    let trendApplied: string | null = null;
> 84	    try {
> 85	      const { data: prodRows } = await admin
> 86	        .from("vm_affiliate_products").select("niches").in("external_id", products).eq("is_active", true);
> 87	      const productNiches = [...new Set(((prodRows ?? []) as Array<{ niches?: string[] | null }>)
> 88	        .flatMap((p) => p.niches ?? []).filter((n): n is string => typeof n === "string" && n.length > 0))];
> 89	      const fetchTrends = async (filterNiche: boolean) => {
> 90	        let q = admin.from("vm_trends").select("title, niche, viral_score")
> 91	          .eq("is_active", true).order("viral_score", { ascending: false }).limit(5);
> 92	        if (filterNiche && productNiches.length > 0) q = q.in("niche", productNiches);
> 93	        const { data } = await q;
> 94	        return (data ?? []) as Array<{ title: string | null; niche: string | null }>;
> 95	      };
> 96	      let candidates = await fetchTrends(true);
> 97	      if (candidates.length === 0) candidates = await fetchTrends(false);
> 98	      for (const t of candidates) {
> 99	        const raw = String(t.title ?? "").replace(/\s+/g, " ").trim().slice(0, 160);
> 100	        if (!raw) continue;
> 101	        const v = inspectPrompt(raw, userId, { rateLimit: false });
> 102	        if (!v.allow) { console.warn(`[autopilot-run] trend in niche '${t.niche}' blocked by sentinel (${v.code}) — skipped`); continue; }
> 103	        trendApplied = raw;
> 104	        viralTopic = `${plan.name} — conectando com a tendência viral do momento: "${raw}"`;
> 105	        break;
> 106	      }
> 107	    } catch (e) { console.warn(`[autopilot-run] trend angle skipped: ${e}`); }
> 108	
> 109	    // dry_run: return the cost projection (+ resolved trend angle) WITHOUT opening a cycle or deducting (zero-cost).
> 110	    if (dryRun) {
> 111	      return json({ ok: true, dry_run: true, n_runs: nRuns, projected_mco: projected,
> 112	        trend_applied: trendApplied, viral_topic: viralTopic,
> 113	        breakdown: { products: products.length, platforms: platforms.length, ab_variants: abVariants } });
> 114	    }
> 115	
> 116	    // ── begin_autopilot_cycle: ATOMIC cap-check + single pre-debit (or abort reason, no deduct). ────────────────
> 117	    const { data: begun, error: beginErr } = await admin.rpc("begin_autopilot_cycle", {
> 118	      p_plan_id: planId, p_user_id: userId, p_projected_mco: projected, p_planned_units: nRuns,
> 119	    });
> 120	    if (beginErr) { logHealth("error"); return json({ error: "begin_failed", detail: beginErr.message }, 500); }
> 121	    if (!begun?.ok) {
> 122	      const reason = begun?.reason ?? "aborted";
> 123	      // Hard stop (budget too low / insufficient balance) → pause the plan so it stops re-firing every tick.
> 124	      if (reason === "aborted_budget" || reason === "insufficient_balance") {
> 125	        await admin.from("autopilot_plans").update({ is_active: false }).eq("id", planId).eq("user_id", userId);
> 126	      }
> 127	      logHealth("degraded");
> 128	      return json({ ok: false, reason, projected_mco: projected }, reason === "insufficient_balance" ? 402 : 409);
> 129	    }
> 130	    const cycleId = begun.cycle_id as string;
> 131	
> 132	    // ── R3 loop (FR-VA-010/011): analyze the PREVIOUS completed cycle to steer THIS cycle's generation. ─────────
> 133	    // collect (sync the live click ledger → creative_metrics) then analyze (→ optimization_policy). Both inline and
> 134	    // PREPAID — the cycle reserved ANALYZE_COST(2); analyzeCharged consumes it only when real data produced a policy
> 135	    // (else finalize refunds the 2). Best-effort — a missing/empty previous cycle just means no steering this round.
> 136	    let analyzeCharged = 0;
> 137	    const svcCall = (fn: string, payload: unknown) => fetch(`${url}/functions/v1/${fn}`, {
> 138	      method: "POST",
> 139	      headers: { Authorization: `Bearer ${serviceKey}`, "Content-Type": "application/json" },
> 140	      body: JSON.stringify(payload),
> 141	    });
> 142	    try {
> 143	      const { data: prev } = await admin.from("autopilot_cycles")
> 144	        .select("id").eq("plan_id", planId).eq("user_id", userId).eq("status", "completed")
> 145	        .neq("id", cycleId).order("cycle_number", { ascending: false }).limit(1).maybeSingle();
> 146	      if (prev?.id) {
> 147	        await svcCall("autopilot-collect", { cycle_id: prev.id }).catch(() => {});
> 148	        const ar = await svcCall("autopilot-analyze", { previous_cycle_id: prev.id, prepaid: true })
> 149	          .then((r) => r.json()).catch(() => null);
> 150	        if (ar?.has_real_data) analyzeCharged = ANALYZE_COST;
> 151	      }
> 152	    } catch (e) { console.warn(`[autopilot-run] R3 analyze skipped: ${e}`); }
> 153	
> 154	    // ── Fan-out: product × platform × variant → orchestrate-content (prepaid → NO self-bill). ───────────────────
> 155	    let succeeded = 0;
> 156	    const tasks: Array<() => Promise<void>> = [];
> 157	    for (const productId of products) {
> 158	      for (const platform of platforms) {
> 159	        for (let v = 0; v < abVariants; v++) {
> 160	          tasks.push(async () => {
> 161	            try {
> 162	              const r = await fetch(`${url}/functions/v1/orchestrate-content`, {
> 163	                method: "POST",
> 164	                headers: {
> 165	                  Authorization: `Bearer ${serviceKey}`,
> 166	                  "x-autopilot-user-id": userId,
> 167	                  "Content-Type": "application/json",
> 168	                },
> 169	                body: JSON.stringify({
> 170	                  topic: viralTopic, platforms: [platform], product_ids: [productId],
> 171	                  prepaid: true, cycle_id: cycleId, wp_status: "draft",
> 172	                }),
> 173	              });
> 174	              if (r.ok) succeeded++;
> 175	              else console.warn(`[autopilot-run] sub-run ${productId}/${platform} → HTTP ${r.status}`);
> 176	            } catch (e) {
> 177	              console.warn(`[autopilot-run] sub-run ${productId}/${platform} error: ${e}`);
> 178	            }
> 179	          });
> 180	        }
> 181	      }
> 182	    }
> 183	    for (let i = 0; i < tasks.length; i += CONCURRENCY) {
> 184	      await Promise.all(tasks.slice(i, i + CONCURRENCY).map((t) => t()));
> 185	    }
> 186	
> 187	    // actual = successful runs × 10 + analyzeCharged (the reserved 2 is consumed only when the R3 analyze produced
> 188	    // a policy from real data; otherwise finalize refunds it). Zero successes → actual = analyzeCharged.
> 189	    const actual = succeeded * ORCH_COST + analyzeCharged;
> 190	    const status = succeeded > 0 ? "completed" : "failed";
> 191	    const { data: fin } = await admin.rpc("finalize_autopilot_cycle", {
> 192	      p_cycle_id: cycleId, p_actual_mco: actual, p_status: status,
> 193	    });
> 194	
> 195	    // ── Re-arm cadence (every_n_days) or deactivate after a single all_at_once run. ─────────────────────────────
> 196	    if (plan.mode === "every_n_days") {
> 197	      const days = Math.min(30, Math.max(1, Number(plan.interval_days ?? 3)));
> 198	      const next = new Date(Date.now() + days * 86_400_000).toISOString();
> 199	      await admin.from("autopilot_plans").update({ next_run_at: next }).eq("id", planId).eq("user_id", userId);
> 200	    } else {
> 201	      await admin.from("autopilot_plans").update({ is_active: false }).eq("id", planId).eq("user_id", userId);
> 202	    }
> 203	
> 204	    logHealth("healthy");
> 205	    return json({
> 206	      ok: true, cycle_id: cycleId, n_runs: nRuns, succeeded,
> 207	      projected_mco: projected, actual_mco: actual, refunded_mco: fin?.refunded ?? 0, status,
> 208	    });
> 209	  } catch (e) {
> 210	    logHealth("error");
> 211	    return json({ error: e instanceof Error ? e.message : "unknown" }, 500);
> 212	  }
> 213	});
> 214	
> ```

## 🤖 Claude *(04:34:55)*


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
> 32	];
> 33	
> 34	// ANSI/C0-C1 detection (FR-SEC-012). In a PROMPT we BLOCK on presence rather than sanitize-and-continue:
> 35	// a smuggled escape sequence is hostile intent, not noise. (\n, \t, \r are intentionally allowed.)
> 36	// deno-lint-ignore no-control-regex
> 37	const ANSI_OR_CONTROL_RE = /[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]/;
> 38	
> 39	export function lexicalScore(text: string): number {
> 40	  let score = 0;
> 41	  for (const re of INJECTION_PATTERNS) {
> 42	    if (re.test(text)) score += 1;
> 43	  }
> 44	  return score;
> 45	}
> 46	
> 47	// L3 — token bucket per identity per isolate. Resets on cold start by design: defense in depth against
> 48	// burst loops, NOT the billing limiter (that is L4 = deduct_mco_coins).
> 49	const BUCKETS = new Map<string, { tokens: number; refillAt: number }>();
> 50	const RATE = { capacity: 30, refillMs: 60_000 };
> 51	
> 52	export function takeToken(identity: string): boolean {
> 53	  const now = Date.now();
> 54	  const bucket = BUCKETS.get(identity) ?? { tokens: RATE.capacity, refillAt: now + RATE.refillMs };
> 55	  if (now >= bucket.refillAt) {
> 56	    bucket.tokens = RATE.capacity;
> 57	    bucket.refillAt = now + RATE.refillMs;
> 58	  }
> 59	  if (bucket.tokens <= 0) {
> 60	    BUCKETS.set(identity, bucket);
> 61	    return false;
> 62	  }
> 63	  bucket.tokens -= 1;
> 64	  BUCKETS.set(identity, bucket);
> 65	  return true;
> 66	}
> 67	
> 68	export interface InspectOptions {
> 69	  // L3 per-identity rate bucket. Default true. Set FALSE for fan-out TARGETS (orchestrate-content,
> 70	  // dispatched in parallel by campaign-run / intent-execute with one shared JWT) — there the burst is
> 71	  // legitimate and the economic gate (deduct_mco_coins) is the real limiter; per-isolate rate-limiting a
> 72	  // fan-out target would 429 already-authorized paid steps. Per-IP rate-limiting belongs at the edge
> 73	  // gateway (Arcjet, SDD §3.1), not inside the dispatch target.
> 74	  rateLimit?: boolean;
> 75	}
> 76	
> 77	export function inspectPrompt(raw: string, identity: string, opts: InspectOptions = {}): SentinelVerdict {
> 78	  const { rateLimit = true } = opts;
> 79	  // L1 — structural
> 80	  if (typeof raw !== "string" || raw.length === 0) {
> 81	    return { allow: false, status: 400, code: "empty_prompt" };
> 82	  }
> 83	  if (raw.length > MAX_PROMPT_BYTES) {
> 84	    return { allow: false, status: 413, code: "payload_too_large" };
> 85	  }
> 86	  // L3 — rate (cheap, before regex work) — skippable for fan-out targets
> 87	  if (rateLimit && !takeToken(identity)) {
> 88	    return { allow: false, status: 429, code: "rate_limited" };
> 89	  }
> 90	  // L2 — control-char smuggling: hostile by definition in a prompt
> 91	  if (ANSI_OR_CONTROL_RE.test(raw)) {
> 92	    return { allow: false, status: 403, code: "control_chars_in_prompt" };
> 93	  }
> 94	  // L2 — lexical injection score (2+ independent pattern families => block)
> 95	  const score = lexicalScore(raw);
> 96	  if (score >= 2) {
> 97	    return { allow: false, status: 403, code: "prompt_injection_suspected", detail: `score=${score}` };
> 98	  }
> 99	  return { allow: true, status: 200, code: "ok" };
> 100	}
> 101	
> 102	// Telemetry — best-effort, never throws (NFR-SEC-01 ∩ FR-SEC-013).
> 103	interface AdminLike {
> 104	  from(table: string): {
> 105	    insert(row: Record<string, unknown>): PromiseLike<{ error: unknown }>;
> 106	  };
> 107	}
> 108	
> 109	export async function logSentinelBlock(
> 110	  admin: AdminLike,
> 111	  fn: string,
> 112	  verdict: SentinelVerdict,
> 113	  userId: string | null,
> 114	): Promise<void> {
> 115	  try {
> 116	    await admin.from("infra_health_logs").insert({
> 117	      service: "sentinel",
> 118	      status: "degraded",
> 119	      metadata: { fn, code: verdict.code, detail: verdict.detail ?? null, user_id: userId },
> 120	    });
> 121	  } catch {
> 122	    // swallowing is intentional: telemetry must never break the request path
> 123	  }
> 124	}
> 125	
> 126	export function verdictResponse(v: SentinelVerdict, corsHeaders: Record<string, string>): Response {
> 127	  return new Response(
> 128	    JSON.stringify({ error: v.code, detail: v.detail ?? null, layer: "sentinel" }),
> 129	    { status: v.status, headers: { ...corsHeaders, "Content-Type": "application/json" } },
> 130	  );
> 131	}
> 132	
> ```

## 🤖 Claude *(04:34:57)*

Now let me read the sealed contract documents to verify against spec.

## 🤖 Claude *(04:34:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"FR-VA-018\" /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md",
  "description": "Find FR-VA-018 in FRD"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 45:| FR-VA-018 | Trend-informed angle | `autopilot-run` lê `vm_trends` (de `fetch-trends`) para pautar o ângulo viral do ciclo (reconecta a ilha de trends). Texto de trend é **fonte não-confiável** → sanitizado antes do prompt (NFR-VA-008). | High | PR-VA-011 | EdgeFunction | AT-VA-018 |
> 161:| FR-VA-018 | ✅ | ✅ | — | ângulo lê `vm_trends`; sanitização de fonte externa |
> 186:| PR-VA-011 | FR-VA-018 | — |
> ```

## 🤖 Claude *(04:35:00)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '170,195p' /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/07-process-flow.md",
  "description": "Read process flow sealed line"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> for (const product of selectedProducts) {
>   for (const platform of plan.platforms) {
>     for (let variant = 1; variant <= plan.ab_variants; variant++) {   // FR-VA-019 — N_runs = prod×rede×ab_variants
>       await updateCycleStatus(cycleId, 'running')
>       const run = await supabase.functions.invoke('orchestrate-content', {
>         // SEM Authorization de user — caminho cron service-role:
>         headers: {
>           Authorization: `Bearer ${SB_SECRET_KEY}`,   // service-role (a fn valida in-function, §5.3)
>           'x-autopilot-user-id': userId,               // server-trusted (NUNCA do body do cliente)
>         },
>         body: {
>           topic: buildViralAngle(sanitize(product), sanitize(trends), variant),  // FR-VA-018/019 + sanitização (NFR-VA-008)
>           product_target: { id: product.external_id, meta: product, feedback: policyFeatures }, // FR-VA-016
>           platforms: [platform],
>           cycle_id: cycleId,                            // NFR-VA-007 auditabilidade
>           prepaid: true,                                // FR-VA-007 — sub-run NÃO self-bills (já pré-debitado)
>         },
>       })
>       if (!run.data?.ok) await logHealth('viral_autopilot_cycle_failed', { cycleId, platform, variant })
>     }
>   }
> }
> // Ao fim: actual = soma real; finalize_autopilot_cycle(cycleId, actual) credita (projetado − actual)
> // no mco_balance — CRÉDITO POSITIVO via RPC atômico (idempotente por refunded_at). NUNCA deduct negativo
> // (deduct_mco_coins rejeita p_amount<=0, migration 20260603220000:45).
> ```
> ```

## 🤖 Claude *(04:35:02)*

Now let me verify the per-product gate pattern in orchestrate-content and check the `vm_trends` / `vm_affiliate_products` schemas.

## 🤖 Claude *(04:35:03)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/orchestrate-content/index.ts",
  "offset": 150,
  "limit": 40
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 150	
> 151	    // utm_campaign uses the campaign_id for per-campaign attribution; fallback to slug for unnamed runs
> 152	    const utmCampaign = campaign_id
> 153	      ? encodeURIComponent(campaign_id)
> 154	      : `mcorch_${topic.slice(0, 24).replace(/\s+/g, "_").toLowerCase()}`;
> 155	
> 156	    // ── Viral Autopilot Fatia 1 (FR-VA-016 product-half / FR-VA-012): resolve the chosen products from the
> 157	    // catalog (authoritative — never trust client-sent name/price) and SANITIZE each product name through the
> 158	    // same Cyber-Sentinel gate (product names are external/Apify-enriched data → prompt-injection vector). A
> 159	    // product whose name fails the gate is dropped (fail-closed per product, not per run). Order preserved so
> 160	    // products[0] = the featured product. Empty/absent → legacy topic-only generation (backward compat).
> 161	    const resolvedProducts: Array<{ external_id: string; name: string; price: number | null; category: string | null; image_url: string | null; url: string | null }> = [];
> 162	    if (Array.isArray(product_ids) && product_ids.length > 0) {
> 163	      const ids = product_ids.filter((x: unknown): x is string => typeof x === "string").slice(0, 5);
> 164	      const { data: prows } = await admin
> 165	        .from("vm_affiliate_products")
> 166	        .select("external_id, name, price, category, image_url, product_url")
> 167	        .in("external_id", ids)
> 168	        .eq("is_active", true);
> 169	      const order = new Map(ids.map((id, i) => [id, i] as const));
> 170	      for (const pr of (prows ?? [])) {
> 171	        const nm = String((pr as { name?: string }).name ?? "");
> 172	        const v = inspectPrompt(nm, userId, { rateLimit: false });
> 173	        if (!v.allow) { console.warn(`[orchestrate-content] product name blocked by sentinel, skipped: ${(pr as { external_id?: string }).external_id}`); continue; }
> 174	        resolvedProducts.push({
> 175	          external_id: (pr as { external_id: string }).external_id,
> 176	          name: nm,
> 177	          price: (pr as { price?: number | null }).price ?? null,
> 178	          category: (pr as { category?: string | null }).category ?? null,
> 179	          image_url: (pr as { image_url?: string | null }).image_url ?? null,
> 180	          url: (pr as { product_url?: string | null }).product_url ?? null,
> 181	        });
> 182	      }
> 183	      resolvedProducts.sort((a, b) => (order.get(a.external_id) ?? 99) - (order.get(b.external_id) ?? 99));
> 184	    }
> 185	
> 186	    // --- Create pipeline_run record ---
> 187	    const runStarted = new Date().toISOString();
> 188	    const { data: runRow } = await admin
> 189	      .from("pipeline_runs")
> ```

## 🤖 Claude *(04:35:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"vm_trends\" /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/ | head -40",
  "description": "Find vm_trends schema in migrations"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040100_viralmind_trends.sql:11:CREATE TABLE IF NOT EXISTS public.vm_trends (
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040100_viralmind_trends.sql:47:COMMENT ON TABLE public.vm_trends IS 'VIRALmind: Mined viral trends. Global pool shared across all users. Feeds Canvas Studio and Content Factory.';
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040100_viralmind_trends.sql:56:  trend_id            UUID NOT NULL REFERENCES public.vm_trends(id) ON DELETE CASCADE,
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040100_viralmind_trends.sql:70:CREATE INDEX IF NOT EXISTS idx_vm_trends_platform ON public.vm_trends(platform);
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040100_viralmind_trends.sql:71:CREATE INDEX IF NOT EXISTS idx_vm_trends_niche ON public.vm_trends(niche);
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040100_viralmind_trends.sql:72:CREATE INDEX IF NOT EXISTS idx_vm_trends_viral_score ON public.vm_trends(viral_score DESC);
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040100_viralmind_trends.sql:73:CREATE INDEX IF NOT EXISTS idx_vm_trends_is_active ON public.vm_trends(is_active) WHERE is_active = TRUE;
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040100_viralmind_trends.sql:74:CREATE INDEX IF NOT EXISTS idx_vm_trends_detected_at ON public.vm_trends(detected_at DESC);
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040100_viralmind_trends.sql:81:ALTER TABLE public.vm_trends ENABLE ROW LEVEL SECURITY;
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040100_viralmind_trends.sql:85:CREATE POLICY "Authenticated users can read trends" ON public.vm_trends
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040100_viralmind_trends.sql:89:CREATE POLICY "Service role manages trends" ON public.vm_trends
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040100_viralmind_trends.sql:110:DROP TRIGGER IF EXISTS vm_trends_updated_at ON public.vm_trends;
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040100_viralmind_trends.sql:111:CREATE TRIGGER vm_trends_updated_at
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040100_viralmind_trends.sql:112:  BEFORE UPDATE ON public.vm_trends
> ```

## 🤖 Claude *(04:35:07)*

Let me check the `vm_trends` table schema (columns: title, niche, viral_score, is_active) and `vm_affiliate_products` (niches column).

## 🤖 Claude *(04:35:09)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040100_viralmind_trends.sql",
  "offset": 11,
  "limit": 36
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 11	CREATE TABLE IF NOT EXISTS public.vm_trends (
> 12	  id                  UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> 13	  external_id         TEXT,                          -- platform's native ID
> 14	  platform            vm_platform NOT NULL,
> 15	  niche               TEXT NOT NULL,                 -- slug ref to vm_niches
> 16	  sub_niches          TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
> 17	  title               TEXT NOT NULL,
> 18	  description         TEXT,
> 19	  thumbnail_url       TEXT,
> 20	  source_url          TEXT,
> 21	  hashtags            TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
> 22	  sounds              JSONB NOT NULL DEFAULT '[]'::jsonb,
> 23	  effects             JSONB NOT NULL DEFAULT '[]'::jsonb,
> 24	  language            TEXT DEFAULT 'pt',
> 25	  region              TEXT DEFAULT 'BR',
> 26	  -- Scoring
> 27	  viral_score         NUMERIC(5,2) NOT NULL DEFAULT 0
> 28	    CHECK (viral_score >= 0 AND viral_score <= 100),
> 29	  velocity            NUMERIC(10,4),                 -- growth rate
> 30	  engagement_rate     NUMERIC(8,4),
> 31	  share_rate          NUMERIC(8,4),
> 32	  estimated_cpc       NUMERIC(8,2),
> 33	  competition_index   NUMERIC(5,2),
> 34	  -- Lifecycle
> 35	  detected_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
> 36	  peaked_at           TIMESTAMPTZ,
> 37	  expires_at          TIMESTAMPTZ,
> 38	  is_active           BOOLEAN NOT NULL DEFAULT TRUE,
> 39	  -- Embedding for GraphRAG similarity search
> 40	  embedding           VECTOR(1536),
> 41	  -- Raw payload
> 42	  metadata            JSONB NOT NULL DEFAULT '{}'::jsonb,
> 43	  created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
> 44	  updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
> 45	);
> 46	
> ```

## 🤖 Claude *(04:35:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"niches\\|external_id\\|is_active\" /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/*affiliate_products*.sql /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/*vm_affiliate* 2>/dev/null | head -30; echo \"---SEARCH niches col---\"; grep -rln \"niches\" /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/ | head",
  "description": "Find vm_affiliate_products columns"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ---SEARCH niches col---
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040000_viralmind_enums_and_niches.sql
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040100_viralmind_trends.sql
> /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040300_viralmind_affiliate_radar.sql
> ```

## 🤖 Claude *(04:35:15)*

`vm_trends` confirms columns: `title`, `niche`, `viral_score`, `is_active`. Now I need to verify the `vm_affiliate_products.niches` column actually exists (the trend niche-filtering hinges on it).

## 🤖 Claude *(04:35:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"niches\\|external_id\\|is_active\\|CREATE TABLE\" /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260514040300_viralmind_affiliate_radar.sql | head -30",
  "description": "Check vm_affiliate_products niches column"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 3:CREATE TABLE IF NOT EXISTS public.vm_affiliate_products (
> 6:  external_id TEXT NOT NULL,
> 11:  niches TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
> 25:  is_active BOOLEAN NOT NULL DEFAULT TRUE,
> 30:  UNIQUE(network, external_id)
> 33:CREATE TABLE IF NOT EXISTS public.vm_affiliate_links (
> 45:  is_active BOOLEAN NOT NULL DEFAULT TRUE,
> 56:CREATE TABLE IF NOT EXISTS public.vm_affiliate_clicks (
> ```

## 🤖 Claude *(04:35:25)*

All schema columns are confirmed: `vm_affiliate_products` has `external_id`, `niches` (TEXT[]), `is_active`; `vm_trends` has `title`, `niche`, `viral_score`, `is_active`. 

Now let me verify each acceptance criterion carefully against the code.

Let me trace the logic systematically:

**(a) Trend selection logic** — lines 89-106:
- `fetchTrends(true)`: filters `.in("niche", productNiches)` only when `filterNiche && productNiches.length > 0`. Orders by `viral_score DESC`, limit 5. ✓ niche-filtered first.
- `if (candidates.length === 0) candidates = await fetchTrends(false)`: GLOBAL fallback only when niche-filtered returns zero. ✓
- Loop iterates, takes first that passes sentinel (`v.allow`), breaks. ✓

Let me examine an important edge case in the fallback logic. When `productNiches.length === 0` (no niches resolved for the products), `fetchTrends(true)` does NOT apply the niche filter (because the guard is `filterNiche && productNiches.length > 0`). So `fetchTrends(true)` returns the GLOBAL top-5 already. Then if that's non-empty, the fallback `fetchTrends(false)` never runs — but it doesn't need to, since `fetchTrends(true)` already returned global results. That's correct, not a bug.

But there's a subtler case to check: what if `fetchTrends(true)` with a niche filter returns a non-empty set, but all candidates are blocked by the sentinel? Then the loop completes without setting `trendApplied`, and the GLOBAL fallback is NOT attempted. This is a graceful degradation (angle stays plain), and the spec says "GLOBAL fallback only when the niche-filtered query returns zero" — which is about the *query* returning zero rows, not about sentinel blocks. So this matches the sealed contract.

Let me verify the `.in()` behavior with an empty array doesn't cause issues, and check the dry_run/fan-out criteria.

## 🤖 Claude *(04:35:27)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"\\.in(\\\"external_id\\\", products)\" /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-run/index.ts; echo \"--- products filter ---\"; sed -n '67p;85,97p' /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-run/index.ts",
  "description": "Check products array handling for .in() empty case"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-run/index.ts:86:        .from("vm_affiliate_products").select("niches").in("external_id", products).eq("is_active", true);
> --- products filter ---
>     const products = ((plan.target_product_ids ?? []) as unknown[]).filter((x): x is string => typeof x === "string" && x.length > 0);
>       const { data: prodRows } = await admin
>         .from("vm_affiliate_products").select("niches").in("external_id", products).eq("is_active", true);
>       const productNiches = [...new Set(((prodRows ?? []) as Array<{ niches?: string[] | null }>)
>         .flatMap((p) => p.niches ?? []).filter((n): n is string => typeof n === "string" && n.length > 0))];
>       const fetchTrends = async (filterNiche: boolean) => {
>         let q = admin.from("vm_trends").select("title, niche, viral_score")
>           .eq("is_active", true).order("viral_score", { ascending: false }).limit(5);
>         if (filterNiche && productNiches.length > 0) q = q.in("niche", productNiches);
>         const { data } = await q;
>         return (data ?? []) as Array<{ title: string | null; niche: string | null }>;
>       };
>       let candidates = await fetchTrends(true);
>       if (candidates.length === 0) candidates = await fetchTrends(false);
> ```

## 🤖 Claude *(04:35:39)*

Note: `nRuns < 1` returns 422 at line 71 (before the trend block), so `products` is guaranteed non-empty by the time the trend block runs. So `.in("external_id", products)` is never called with an empty array. Good.

Now let me verify all the criteria are met and check for any genuine bug. Let me re-examine the critical ordering and try/catch boundaries.

**(b) Graceful when vm_trends empty**: `fetchTrends` returns `(data ?? [])`, so empty/null → `[]`. `candidates.length === 0` → fallback returns `[]` too. Loop doesn't execute. `viralTopic` stays `plan.name`, `trendApplied` stays `null`. No throw. ✓

**(c) No regression to PAID path**: 
- The entire trend block (lines 82-107) is BEFORE the `dry_run` short-circuit (line 110) and BEFORE `begin_autopilot_cycle` (line 117). ✓
- Wrapped in `try { ... } catch (e) { console.warn(...) }` (lines 84-107). Any query/trend error degrades — `viralTopic` retains whatever value it had (defaults to `plan.name`). ✓
- `begin_cycle` / fan-out / finalize unchanged except `topic: viralTopic`. ✓

**(d) dry_run response**: lines 110-114 surface `trend_applied: trendApplied` and `viral_topic: viralTopic`. ✓

**(e) Resolved ONCE per cycle, reused across sub-runs**: `viralTopic` is computed once (lines 82-107), then used inside the fan-out loop at line 170 (`topic: viralTopic`) for every product×platform×variant. No re-query per sub-run. ✓

Let me double-check one potential concern: the sentinel's `inspectPrompt` is called with `{ rateLimit: false }`, which matches the fan-out pattern and avoids 429 on the top-5 iteration within the same isolate. Let me confirm there's no `await` missing on `inspectPrompt` (it's synchronous — returns `SentinelVerdict`, not a Promise).

Confirmed from sentinel.ts line 77: `export function inspectPrompt(...): SentinelVerdict` — synchronous, correctly called without `await` at line 101.

Let me check one more subtle thing — whether `viral_score` being selected but the type cast omitting it causes any issue, and whether the order-by direction is correct.

## 🤖 Claude *(04:35:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '89,106p' /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-run/index.ts",
  "description": "Re-read trend selection block"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>       const fetchTrends = async (filterNiche: boolean) => {
>         let q = admin.from("vm_trends").select("title, niche, viral_score")
>           .eq("is_active", true).order("viral_score", { ascending: false }).limit(5);
>         if (filterNiche && productNiches.length > 0) q = q.in("niche", productNiches);
>         const { data } = await q;
>         return (data ?? []) as Array<{ title: string | null; niche: string | null }>;
>       };
>       let candidates = await fetchTrends(true);
>       if (candidates.length === 0) candidates = await fetchTrends(false);
>       for (const t of candidates) {
>         const raw = String(t.title ?? "").replace(/\s+/g, " ").trim().slice(0, 160);
>         if (!raw) continue;
>         const v = inspectPrompt(raw, userId, { rateLimit: false });
>         if (!v.allow) { console.warn(`[autopilot-run] trend in niche '${t.niche}' blocked by sentinel (${v.code}) — skipped`); continue; }
>         trendApplied = raw;
>         viralTopic = `${plan.name} — conectando com a tendência viral do momento: "${raw}"`;
>         break;
>       }
> ```

## 🤖 Claude *(04:35:48)*

Verification complete. The implementation is correct against all five acceptance criteria and the sealed contract.

Let me do a final check on the order-by direction (`{ ascending: false }` = DESC = highest viral_score first = "top-5 by viral_score"). ✓ Correct. And `.limit(5)` = top-5. ✓

Let me also confirm there's no subtle issue with `fetchTrends(true)` returning a non-empty set whose rows are all sentinel-blocked AND it was niche-filtered — meaning global never gets a chance. I noted this matches the sealed contract ("GLOBAL fallback only when the niche-filtered query returns zero" — about rows, not sentinel verdicts). This is the documented design; a fully-blocked niche set degrades to the plain angle rather than falling through to global. Not a bug per the contract, but worth noting as a low-severity behavioral observation since it's a plausible "fallback that never triggers" scenario the reviewer flagged — but it is intentional and contract-aligned, so I will not flag it as a bug.

Let me verify one last thing: that the `inspectPrompt` import is the only new import and there's no duplicate/unused concern, and confirm the file compiles conceptually (the `viral_score` is selected but not in the cast type — harmless since it's only used for ordering server-side).

All criteria pass. I found no genuine bugs at ≥80% confidence. Let me compile the structured output.

## 🤖 Claude *(04:36:03)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "lens": "correctness",
  "verdict": "safe",
  "findings": [],
  "summary": "FR-VA-018 (\"trend-informed angle\") in supabase/functions/autopilot-run/index.ts (lines 75-114, plus the `import { inspectPrompt }` at line 13 and `topic: viralTopic` at line 170) is implemented correctly. I verified it against the sealed contract (docs/bok/viral-autopilot/04-frd.md FR-VA-018 row + 07-process-flow.md `topic: buildViralAngle(sanitize(product), sanitize(trends), variant)` ~line 181), the per-product sentinel gate pattern in orchestrate-content/index.ts:162-184, the sentinel API in _shared/sentinel.ts, and the live table schemas (vm_trends has title/niche/viral_score/is_active per migration 20260514040100; vm_affiliate_products has external_id/niches[]/is_active per 20260514040300).\n\nAll five acceptance criteria hold:\n\n(a) Selection logic is correct. `fetchTrends(true)` niche-filters (`.in(\"niche\", productNiches)`) only when `productNiches.length > 0`, ordered `viral_score` DESC (`{ ascending: false }`), `.limit(5)` = top-5. GLOBAL fallback (`fetchTrends(false)`) fires only when the niche-filtered query returns zero rows (`candidates.length === 0`). The loop takes the first candidate that passes `inspectPrompt(...).allow` and `break`s; blocked trends are skip-and-continue (line 102), mirroring orchestrate-content:172-173. When products have no resolvable niches, the niche filter is skipped so `fetchTrends(true)` already returns the global top-5 \u2014 correct, no redundant second query needed.\n\n(b) Graceful on empty vm_trends (the real current state). `fetchTrends` returns `(data ?? [])`; empty \u2192 `[]`, fallback also `[]`, loop body never runs, `viralTopic` stays `plan.name`, `trendApplied` stays null. No throw. `products` is guaranteed non-empty here (nRuns<1 already returned 422 at line 71), so `.in(\"external_id\", products)` is never called with an empty array.\n\n(c) No regression to the PAID path. The whole trend block (82-107) is BEFORE the dry_run short-circuit (110) and BEFORE begin_autopilot_cycle (117), and is wrapped in try/catch (84-107) whose catch only `console.warn`s \u2014 any query/trend error degrades to the plain angle (`viralTopic` retains `plan.name`) and never aborts the cycle. begin_cycle / fan-out / finalize are unchanged except the topic value.\n\n(d) dry_run response surfaces `trend_applied` and `viral_topic` (lines 111-113) for zero-cost verification.\n\n(e) Trend is resolved ONCE per cycle (82-107) and the resulting `viralTopic` is reused for every product\u00d7platform\u00d7variant sub-run via `topic: viralTopic` at line 170 \u2014 not re-queried per sub-run.\n\nAdditional correctness checks: `inspectPrompt` is synchronous (returns SentinelVerdict, not a Promise) so the no-`await` call at line 101 is correct; `{ rateLimit: false }` correctly mirrors the fan-out-target convention (sentinel.ts:68-74) so iterating the top-5 within one isolate cannot self-429; the `viral_score` column is selected for server-side ordering and intentionally omitted from the client-side cast (harmless). One intentional, contract-aligned behavior worth noting (not a bug): if a niche-filtered query returns rows but ALL of them are sentinel-blocked, the GLOBAL fallback does not fire and the angle degrades to plain \u2014 this matches the sealed contract's \"fallback only when the niche-filtered query returns zero [rows]\" wording and is the documented skip-and-continue design.\n\nNo genuine bugs found at >=80% confidence."
}
```

> **Tool Result (StructuredOutput)** - ✅ Success
>
> ```
> Structured output provided successfully
> ```

## 🤖 Claude *(04:36:10)*

Review complete. Verdict: **safe** — no genuine bugs at ≥80% confidence.

The FR-VA-018 implementation in `/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-run/index.ts` (trend block lines 82-114, import line 13, fan-out `topic: viralTopic` line 170) is correct against all five acceptance criteria and the sealed contract. I verified the live table schemas back the queries (`vm_trends.title/niche/viral_score/is_active`, `vm_affiliate_products.external_id/niches[]/is_active`), the niche-first → global-fallback ordering and top-5-by-viral_score selection, the sentinel skip-and-continue gate mirroring `orchestrate-content/index.ts:162-184`, graceful no-throw on empty `vm_trends`, the try/catch + pre-dry_run placement protecting the paid path, the dry_run surfacing of `trend_applied`/`viral_topic`, and once-per-cycle resolution reused across all sub-runs.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-23 - agent-a98f6a48601b6a832]]
> * **Próxima Sessão**: [[2026-06-23 - agent-ac88e66c748ac7f49]]
%% --- TIMELINE END --- %%

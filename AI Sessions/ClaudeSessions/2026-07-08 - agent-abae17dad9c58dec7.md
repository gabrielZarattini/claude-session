# Session agent-abae17dad9c58dec7
**Date:** 2026-07-08 | **Session ID:** `agent-abae17dad9c58dec7`

---

## 👤 User *(10:10:26)*

You are an adversarial false-positive filter for a security finding in the MCORCH repo at /home/gcrUX/htdocs/constellation-orchestra. Independently RE-VERIFY this candidate by READING the actual code — is it a REAL, concretely-exploitable vulnerability, or a false positive?

CANDIDATE: Unauthenticated public endpoints amplify into privileged GoTrue admin APIs with no throttle
File: supabase/functions/tiktok-login-session/index.ts:28 · Severity(claimed): low · Category: resource-exhaustion
Description: All three functions are verify_jwt=false with no rate limiting and no apikey requirement. tiktok-login-session accepts arbitrary POST {code} from anyone and per request performs a DB UPDATE plus, on match, admin.getUserById + admin.generateLink + anon.verifyOtp — privileged auth operations.
Claimed exploit: Attacker floods tiktok-login-session with junk codes: each miss still costs a DB UPDATE round-trip, and any grind against a possibly-leaked code drives load; a valid-but-guessed hit chains into three GoTrue admin/auth calls. Codes are 256-bit so not brute-forceable, but the endpoint is an open, unauthenticated amplification surface into the service-role admin auth path (and tiktok-login-callback similarly triggers createUser + token exchange for any request bearing a replayable state), usable for cost/DoS pressure on the auth subsystem.

FALSE-POSITIVE FILTERING (apply strictly):
- Exclude: DoS/resource exhaustion, rate-limiting, secrets-on-disk (env vars are TRUSTED — attacks needing env control are invalid), outdated deps, log spoofing, SSRF that only controls path, open redirects unless EXTREMELY high confidence, theoretical race conditions (only report if concretely exploitable), memory safety in safe languages, findings in markdown/docs, lack-of-hardening, client-side JS/TS lacking auth checks (backend is responsible).
- React/tsx: NOT an XSS risk unless dangerouslySetInnerHTML/similar.
- UUIDs are unguessable (no validation needed). Environment variables/CLI flags are trusted.
- Only report a vuln with a CONCRETE, exploitable attack path where UNTRUSTED input triggers it. Confidence 1-10; only keep >=8.
- This is auth code (session-minting) so genuinely-exploitable auth-bypass / session-forgery / cross-tenant / injection findings ARE in scope and high value.

Read supabase/functions/tiktok-login-session/index.ts (and any related file) to confirm or refute. Default to is_real=false unless you can articulate a concrete attack path with untrusted input. Assign confidence 1-10 that it is a REAL exploitable vuln. Provide a one-line fix if real.

## 🤖 Claude *(10:10:29)*


## 🤖 Claude *(10:10:30)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/tiktok-login-session/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// tiktok-login-session (FR-TL-006) — PUBLIC (verify_jwt=false): the SPA callback has no session yet.
> 2	// Redeems the single-use hand-off code (atomic consume → replay-proof) and re-mints a Supabase session for the
> 3	// mapped user via the proven admin.generateLink → verifyOtp pattern (scripts/qa/gen-user-jwt.ts). Returns the
> 4	// session ONCE; the code is invalidated on first redeem. NO session tokens were ever in a URL.
> 5	// SOP: docs/processes/tiktok-login-oauth.md · BoK: docs/bok/tiktok-login/05-sdd.md §4.
> 6	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 7	
> 8	const ALLOWED_ORIGINS = [
> 9	  "https://login.mcorch.com",
> 10	  "http://localhost:8080",
> 11	  "http://localhost:5173",
> 12	  "http://localhost:4173",
> 13	];
> 14	function cors(origin: string | null) {
> 15	  const allow = origin && ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
> 16	  return {
> 17	    "Access-Control-Allow-Origin": allow,
> 18	    "Access-Control-Allow-Methods": "POST, OPTIONS",
> 19	    "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> 20	    "Vary": "Origin",
> 21	  };
> 22	}
> 23	async function sha256Hex(s: string): Promise<string> {
> 24	  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(s));
> 25	  return Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, "0")).join("");
> 26	}
> 27	
> 28	Deno.serve(async (req) => {
> 29	  const origin = req.headers.get("Origin");
> 30	  const headers = { ...cors(origin), "Content-Type": "application/json" };
> 31	  if (req.method === "OPTIONS") return new Response("ok", { headers: cors(origin) });
> 32	  if (req.method !== "POST") return new Response(JSON.stringify({ error: "method_not_allowed" }), { status: 405, headers });
> 33	
> 34	  let code: string | null = null;
> 35	  try { code = (await req.json())?.code ?? null; } catch { /* noop */ }
> 36	  if (!code || typeof code !== "string") return new Response(JSON.stringify({ error: "missing_code" }), { status: 400, headers });
> 37	
> 38	  const admin = createClient(
> 39	    Deno.env.get("SUPABASE_URL")!,
> 40	    (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
> 41	    { auth: { persistSession: false } },
> 42	  );
> 43	  const anon = createClient(
> 44	    Deno.env.get("SUPABASE_URL")!,
> 45	    (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!,
> 46	    { auth: { persistSession: false } },
> 47	  );
> 48	
> 49	  try {
> 50	    const codeHash = await sha256Hex(code);
> 51	    // ATOMIC consume: mark consumed only if still unconsumed AND unexpired, RETURNING user_id. A second redeem
> 52	    // (replay) matches 0 rows → null. This single UPDATE is the replay guard (no read-then-write race).
> 53	    const { data: consumed } = await admin
> 54	      .from("tiktok_login_codes")
> 55	      .update({ consumed_at: new Date().toISOString() })
> 56	      .eq("code_hash", codeHash)
> 57	      .is("consumed_at", null)
> 58	      .gt("expires_at", new Date().toISOString())
> 59	      .select("user_id")
> 60	      .maybeSingle();
> 61	
> 62	    if (!consumed?.user_id) {
> 63	      return new Response(JSON.stringify({ error: "code_invalid_or_expired" }), { status: 410, headers });
> 64	    }
> 65	
> 66	    // Resolve the mapped user's (synthetic) email, then mint a fresh session (generateLink → verifyOtp).
> 67	    const { data: userRes, error: uErr } = await admin.auth.admin.getUserById(consumed.user_id);
> 68	    if (uErr || !userRes?.user?.email) {
> 69	      admin.from("infra_health_logs").insert({ service: "tiktok-login", event: "session_user_lookup", status: "error" }).then(() => {}, () => {});
> 70	      return new Response(JSON.stringify({ error: "server_error" }), { status: 500, headers });
> 71	    }
> 72	    const email = userRes.user.email;
> 73	
> 74	    const { data: link, error: lErr } = await admin.auth.admin.generateLink({ type: "magiclink", email });
> 75	    if (lErr || !link.properties?.hashed_token) {
> 76	      admin.from("infra_health_logs").insert({ service: "tiktok-login", event: "generate_link", status: "error" }).then(() => {}, () => {});
> 77	      return new Response(JSON.stringify({ error: "server_error" }), { status: 500, headers });
> 78	    }
> 79	    const tokenHash = link.properties.hashed_token;
> 80	
> 81	    let session: { access_token: string; refresh_token: string } | null = null;
> 82	    for (const type of ["magiclink", "email"] as const) {
> 83	      const { data: sess, error: vErr } = await anon.auth.verifyOtp({ token_hash: tokenHash, type });
> 84	      if (!vErr && sess?.session?.access_token && sess.session.refresh_token) {
> 85	        session = { access_token: sess.session.access_token, refresh_token: sess.session.refresh_token };
> 86	        break;
> 87	      }
> 88	    }
> 89	    if (!session) {
> 90	      admin.from("infra_health_logs").insert({ service: "tiktok-login", event: "verify_otp", status: "error" }).then(() => {}, () => {});
> 91	      return new Response(JSON.stringify({ error: "server_error" }), { status: 500, headers });
> 92	    }
> 93	
> 94	    admin.from("infra_health_logs").insert({ service: "tiktok-login", event: "session_minted", status: "healthy" }).then(() => {}, () => {});
> 95	    return new Response(JSON.stringify(session), { headers });
> 96	  } catch (err) {
> 97	    console.error("[tiktok-login-session] error:", err instanceof Error ? err.message : String(err));
> 98	    return new Response(JSON.stringify({ error: "server_error" }), { status: 500, headers });
> 99	  }
> 100	});
> 101	
> ```

## 🤖 Claude *(10:10:37)*


## 🤖 Claude *(10:10:42)*

This finding is explicitly a DoS/resource-exhaustion concern, which is on the exclusion list. Let me confirm there's no hidden auth-bypass angle in the actual code.

The code hashes the incoming `code` with SHA-256 and does a single atomic `UPDATE ... WHERE code_hash = ? AND consumed_at IS NULL AND expires_at > now() RETURNING user_id`. Only a valid, unconsumed, unexpired 256-bit code yields a `user_id` and proceeds to mint a session. The query is parameterized via the Supabase client (no injection), the atomic update is replay-proof, and there's no cross-tenant surface. The description itself concedes codes are 256-bit and not brute-forceable.

The entire claimed exploit reduces to "unauthenticated endpoint costs a DB round-trip per request and could be flooded" — pure cost/DoS pressure with no concrete auth-bypass, forgery, or injection path from untrusted input. That is squarely in the excluded category (DoS/resource-exhaustion, rate-limiting, lack-of-hardening).

## 🤖 Claude *(10:10:50)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "title": "Unauthenticated public endpoints amplify into privileged GoTrue admin APIs with no throttle",
  "confidence": 2,
  "is_real": false,
  "reasoning": "The finding is self-described as a resource-exhaustion/DoS concern (flooding an open endpoint to drive DB and GoTrue admin load), which is explicitly excluded from scope. Reading the actual code confirms no concrete auth-bypass exists: the incoming code is SHA-256 hashed and matched via a single atomic UPDATE (WHERE code_hash=? AND consumed_at IS NULL AND expires_at>now() RETURNING user_id). Only a valid, unconsumed, unexpired code advances to the admin.generateLink/verifyOtp session-mint chain. Codes are 256-bit (the description concedes they are not brute-forceable), the atomic consume is replay-proof, the query is parameterized (no injection), and user_id comes from the trusted DB row (no cross-tenant or forgery vector from attacker input). There is no exploitable path where untrusted input mints a session or bypasses auth \u2014 only theoretical cost/load pressure, which is a lack-of-hardening/rate-limiting issue, not a concrete vulnerability.",
  "fix": "No fix required (excluded DoS/rate-limiting class); if throttling is desired for defense-in-depth, add per-IP rate limiting or require the anon apikey at the gateway \u2014 but this is hardening, not a vuln fix.",
  "severity": "low",
  "file": "supabase/functions/tiktok-login-session/index.ts",
  "line": 28
}
```

> **Tool Result (StructuredOutput)** - ✅ Success
>
> ```
> Structured output provided successfully
> ```

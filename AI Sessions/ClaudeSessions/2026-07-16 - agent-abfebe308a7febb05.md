# Session agent-abfebe308a7febb05
**Date:** 2026-07-16 | **Session ID:** `agent-abfebe308a7febb05`

---

## 👤 User *(17:14:19)*

You are a senior security engineer reviewing code changes on a branch of the MCORCH constellation-orchestra repo (/home/gcrUX/htdocs/constellation-orchestra). Identify HIGH-CONFIDENCE security vulnerabilities NEWLY INTRODUCED by these changes. Do not comment on pre-existing concerns.

The security-relevant changed files to focus on (ignore docs/*.md, seed scripts, and test files):
1. `supabase/migrations/20260716190000_pat_allowlist_swarm_read.sql` — extends the PAT scope allowlist CHECK on mcp_access_tokens to add 'swarm:read'
2. `scripts/landing-bundler/public-url.ts` — host-side anti-SSRF fetch guard (port of supabase/functions/_shared/public-url.ts)
3. `scripts/landing-bundler/bundle-core.ts` — fetches external refs from tenant HTML and inlines as data: URIs
4. `scripts/landing-bundler/cli.ts` — CLI wrapper
5. `supabase/functions/detect-viral-moments/index.ts` — added Gemini-only BYOK path (endpoint/model/headers selection)
6. `supabase/functions/youtube-data/index.ts` — added mesh observation node on channel_summary + delete telemetry
7. `src/hooks/useMcpTokens.ts` and `scripts/qa/mint-vision-pat.ts` — added 'swarm:read' to scope vocabulary
8. `scripts/qa/e2e-user-zero/runner.ts` and related — regex change for auth-error classification

ANALYSIS APPROACH:
- Read each file fully. For the migration, compare against the original constraint in supabase/migrations/20260615180000_vision_mcp_access_tokens.sql.
- For the SSRF guard, verify the redirect re-validation and DNS check logic is sound; compare against the canonical supabase/functions/_shared/public-url.ts.
- For bundle-core.ts, trace how external URLs from tenant HTML flow into fetches — is the host controllable? Can it reach internal services? Note this is anti-SSRF-guarded via fetchPublicUrl.
- For the edge functions, look for injection, auth bypass, data exposure, secret leakage.

Focus ONLY on: SQL injection, command injection, path traversal, auth/authorization bypass, privilege escalation, SSRF (host/protocol control, not path-only), secret leakage, XSS via unsafe methods, code execution. 

EXCLUDE: DoS/resource exhaustion, secrets-on-disk, rate limiting, theoretical races, outdated deps, findings in markdown docs, findings only in test files, log spoofing, path-only SSRF, client-side authz checks (backend is trusted to validate).

For EACH candidate vulnerability, provide: file path, line number, severity (HIGH/MEDIUM), category, description, concrete exploit scenario, fix recommendation, and a confidence score 1-10. Only include candidates with confidence >= 7.

Use Read/Grep/Glob to explore. Do NOT write files or run destructive commands. Return a structured list of candidate findings (or explicitly state "NO FINDINGS" if none reach confidence 7).

## 🤖 Claude *(17:14:25)*

<details>
<summary>💭 Thinking Process</summary>

I'm starting by examining the git diff to see what changed, then reading through the relevant files to understand the modifications.

</details>


## 🤖 Claude *(17:14:25)*

I'll start by examining the changed files. Let me look at the git state and read the relevant files in parallel.

## 🤖 Claude *(17:14:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -15 && echo \"---STATUS---\" && git status && echo \"---DIFF STAT vs origin/main---\" && git diff --stat origin/main...HEAD 2>/dev/null | head -60",
  "description": "Inspect git state and diff stat"
}
```

## 🤖 Claude *(17:14:25)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260716190000_pat_allowlist_swarm_read.sql"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 76e5a8a fix(scripts): idempotência CHECK-BEFORE-INSERT nos 13 seed seals restantes (anticorpo 0718101 completo)
> 4d59f69 docs(loop): charter — it.0-it.3 fechadas (diretiva 2026-07-16 drenada até it.4)
> 0718101 chore(mesh): seal nodes das BoKs retroativas + anticorpo de idempotência
> a8265eb docs(bok): video-repurpose + youtube-studio — suítes 9/9 RETROATIVAS seladas (32/32 famílias verdes)
> 885fa77 test(spaces-cadence): witness E2E de despacho — smoke re-executável 7/7 (fecha ressalva do seal 2026-07-15)
> 762c641 feat(landing-factory): landing-bundler core — Fatia 1 P0 (FR-LF-002/003 seam)
> a729f83 fix(edge): micro-reparos pré-BoK 9/9 — mesh mandate youtube-data + gate Gemini-only do detector
> 7a00511 fix(ui): ReactFlow Controls no tema MIV via --xy-* vars (INC-8cba901a)
> 50bd550 fix(qa): UX-Explorer enxerga pela 1ª vez — 4 causas empilhadas do INC-39626fcd
> 5534eda chore(sprint): landing-factory na Fila Sovereign (item 5) — BoK 9/9 selada, Fatia 1 = landing-bundler
> 29a8b06 docs(handoff): seal landing-factory BoK 9/9 + fix imagem + fix egress (malha 9122)
> 10444b7 docs(readme): v6.104.0 — landing-factory BoK 9/9 + fix imagem + fix egress (malha 9122)
> 11a5adb docs(bok): landing-factory — blueprint v0.2 + BoK 9/9 selada (Closed-Loop aberto)
> 5a46f2f docs(roadmap): artefato roadmap master do motor de conteudo (2 maquinas)
> 3abbe59 fix: egress — reusa signed URL 24h em vez de re-assinar a cada render
> ---STATUS---
> On branch main
> Your branch is ahead of 'origin/main' by 9 commits.
>   (use "git push" to publish your local commits)
> 
> Changes not staged for commit:
>   (use "git add <file>..." to update what will be committed)
>   (use "git restore <file>..." to discard changes in working directory)
> 	modified:   scripts/qa/mint-vision-pat.ts
> 	modified:   src/hooks/useMcpTokens.ts
> 
> Untracked files:
>   (use "git add <file>..." to include in what will be committed)
> 	supabase/migrations/20260716190000_pat_allowlist_swarm_read.sql
> 
> no changes added to commit (use "git add" and/or "git commit -a")
> ---DIFF STAT vs origin/main---
>  .claude/context/autonomous-loop-charter.md         |  17 +-
>  .../context/bok-readiness-audit-2026-07-16.json    | 330 +++++++++++++++++++
>  docs/bok/video-repurpose/00-index.md               | 133 ++++++++
>  docs/bok/video-repurpose/01-mrd.md                 | 170 ++++++++++
>  docs/bok/video-repurpose/02-brd.md                 | 180 +++++++++++
>  docs/bok/video-repurpose/03-prd.md                 | 197 ++++++++++++
>  docs/bok/video-repurpose/04-frd.md                 | 129 ++++++++
>  docs/bok/video-repurpose/05-sdd.md                 | 263 +++++++++++++++
>  docs/bok/video-repurpose/06-data-model.md          | 352 +++++++++++++++++++++
>  docs/bok/video-repurpose/07-process-flow.md        | 327 +++++++++++++++++++
>  docs/bok/video-repurpose/08-quality-metrics.md     | 199 ++++++++++++
>  docs/bok/youtube-studio/00-index.md                | 111 +++++++
>  docs/bok/youtube-studio/01-mrd.md                  | 153 +++++++++
>  docs/bok/youtube-studio/02-brd.md                  | 179 +++++++++++
>  docs/bok/youtube-studio/03-prd.md                  | 227 +++++++++++++
>  docs/bok/youtube-studio/04-frd.md                  | 196 ++++++++++++
>  docs/bok/youtube-studio/05-sdd.md                  | 309 ++++++++++++++++++
>  docs/bok/youtube-studio/06-data-model.md           | 309 ++++++++++++++++++
>  docs/bok/youtube-studio/07-process-flow.md         | 284 +++++++++++++++++
>  docs/bok/youtube-studio/08-quality-metrics.md      | 229 ++++++++++++++
>  docs/bok/youtube-studio/11-api-surface-map.md      |   4 +
>  docs/processes/landing-bundler.md                  |  69 ++++
>  docs/processes/youtube-studio-panel.md             |   1 +
>  scripts/landing-bundler/bundle-core.ts             | Bin 0 -> 17711 bytes
>  scripts/landing-bundler/cli.ts                     |  30 ++
>  scripts/landing-bundler/public-url.ts              |  76 +++++
>  scripts/qa/e2e-user-zero/flows/_nav-capture.ts     |   5 +-
>  scripts/qa/e2e-user-zero/flows/auth-login.ts       |   5 +-
>  scripts/qa/e2e-user-zero/lib/browser-driver.ts     |   7 +-
>  scripts/qa/e2e-user-zero/runner.ts                 |  14 +-
>  scripts/qa/smoke-cadence-dispatch.ts               | 182 +++++++++++
>  scripts/qa/ux-explorer-cron.sh                     |  12 +-
>  scripts/seed-agentic-governance-bok-seal.ts        |   9 +
>  ...seed-authenticated-browser-operator-bok-seal.ts |  13 +-
>  scripts/seed-claw-master-audit-v1-seal.ts          |  12 +
>  scripts/seed-conteudo-v2-bok-seal.ts               |   9 +
>  scripts/seed-gamificacao-nodes-bok-seal.ts         |   9 +
>  scripts/seed-landing-factory-bok-seal.ts           |   9 +
>  scripts/seed-openclaw-bok-seal.ts                  |   9 +
>  scripts/seed-retroactive-bok-seals-20260716.ts     | 146 +++++++++
>  scripts/seed-spaces-evolution-bok-seal.ts          |   9 +
>  scripts/seed-tiktok-login-bok-seal.ts              |  12 +-
>  scripts/seed-video-studio-agency-amendment.ts      |   9 +
>  scripts/seed-video-studio-bok-seal.ts              |   9 +
>  scripts/seed-viralmind-bok-seal.ts                 |   9 +
>  scripts/seed-vision-mcp-bok-seal.ts                |  11 +-
>  src/index.css                                      |  17 +
>  src/test/landing-bundler.test.ts                   | 178 +++++++++++
>  supabase/functions/detect-viral-moments/index.ts   |  24 +-
>  supabase/functions/youtube-data/index.ts           |  33 +-
>  50 files changed, 5209 insertions(+), 17 deletions(-)
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- 20260716190000_pat_allowlist_swarm_read.sql
> 2	-- predictive-swarm Fatia 2 (sub-fatia PAT) — FR-PSW-002 / NFR-PSW-005 / BoK 00-index §"Scopes novos".
> 3	--
> 4	-- WHY: the Tier 1 sensory gate tool (`vision.parse_sensory_gate`, scope `swarm:read`) shipped LIVE in
> 5	-- the mcorch_vision_mcp container on 2026-07-15 (Fatia 1) and is already reachable by internal tenant
> 6	-- JWTs (ALL_SCOPES in identity.ts:17 includes swarm:read). But an EXTERNAL PAT cannot carry the scope:
> 7	-- the closed-vocabulary allowlist CHECK on mcp_access_tokens (migration 20260615180000, constraint
> 8	-- `scopes_allowed`) predates the swarm surface and rejects the write. This migration extends the
> 9	-- vocabulary with `swarm:read` ONLY — `swarm:run`/`swarm:write` enter with their own tools
> 10	-- (swarm-initialize / consolidate-sensory-insight, Fatias 2-full/3), never before a live tool exists
> 11	-- (fail-closed: no PAT may carry a scope that gates nothing).
> 12	--
> 13	-- Security posture unchanged: still an ALLOWLIST (not blocklist); still `scopes <@ ARRAY[...]` with
> 14	-- array_length >= 1; RLS and every other constraint untouched. The constraint name is DECLARED in the
> 15	-- original migration (not auto-generated), so drop-by-name is deterministic; IF EXISTS keeps the
> 16	-- migration re-runnable.
> 17	
> 18	ALTER TABLE public.mcp_access_tokens
> 19	  DROP CONSTRAINT IF EXISTS scopes_allowed;
> 20	
> 21	ALTER TABLE public.mcp_access_tokens
> 22	  ADD CONSTRAINT scopes_allowed CHECK (
> 23	    scopes <@ ARRAY['vision:read','deepsearch:run','mesh:read','mesh:write','swarm:read']
> 24	    AND array_length(scopes, 1) >= 1
> 25	  );
> 26	
> 27	COMMENT ON CONSTRAINT scopes_allowed ON public.mcp_access_tokens IS
> 28	  'Closed scope vocabulary (allowlist, never blocklist). swarm:read added 2026-07-16 (predictive-swarm '
> 29	  'Fatia 2 sub-fatia PAT — Tier 1 gate tool live since Fatia 1); swarm:run/swarm:write enter only with '
> 30	  'their own live tools.';
> 31	
> ```

## 🤖 Claude *(17:14:26)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260615180000_vision_mcp_access_tokens.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: vision-mcp PAT — mcp_access_tokens (FR-VM-003 · FM-VM-06). Fatia 3 core.
> 2	-- BoK SSOT: docs/bok/vision-mcp/05-sdd.md §7 (migration 1) + §5.2 (RLS) + 06-data-model.md §2.1.
> 3	-- SOP: docs/processes/vision-mcp-pat-and-erasure.md (Lei 2 — Parte A).
> 4	--
> 5	-- External MCP clients authenticate with a bearer PAT `mcorch_pat_<rand>`; the DB stores ONLY the SHA-256
> 6	-- hash (never plaintext / never Vault-reversible). The container looks up the hash via the service key (sole
> 7	-- reader). Scopes are a CLOSED vocabulary enforced at the DB by an ALLOWLIST CHECK (subsumes the old
> 8	-- credentials:*/billing:* blocklist — a leaked PAT can never reach credential mgmt nor the wallet beyond tool
> 9	-- consumption, FM-VM-06). Expiry has a physical 365d ceiling (DD-VM-002). Revocation = UPDATE revoked_at (no
> 10	-- client DELETE). RLS: own SELECT/INSERT/UPDATE only. Passes /security-review before commit (FMEA-011/NFR-VM-007).
> 11	
> 12	CREATE TABLE IF NOT EXISTS public.mcp_access_tokens (
> 13	  id            uuid        DEFAULT gen_random_uuid() PRIMARY KEY,
> 14	  user_id       uuid        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 15	  token_hash    char(64)    NOT NULL UNIQUE,          -- SHA-256 hex; NUNCA plaintext
> 16	  token_prefix  text        NOT NULL,                 -- ex.: 'mcorch_pat_3f9a…' p/ exibição
> 17	  label         text,
> 18	  scopes        text[]      NOT NULL,
> 19	  expires_at    timestamptz NOT NULL,
> 20	  revoked_at    timestamptz,
> 21	  last_used_at  timestamptz,
> 22	  created_at    timestamptz NOT NULL DEFAULT now(),
> 23	  -- ALLOWLIST no DB (não blocklist): scope fora do vocabulário fechado é rejeitado na escrita.
> 24	  CONSTRAINT scopes_allowed CHECK (
> 25	    scopes <@ ARRAY['vision:read','deepsearch:run','mesh:read','mesh:write']
> 26	    AND array_length(scopes, 1) >= 1
> 27	  ),
> 28	  -- Teto de validade físico no DB (DD-VM-002): default 90d na app, máximo 365d hard no schema.
> 29	  CONSTRAINT pat_expiry_ceiling CHECK (expires_at <= created_at + interval '365 days')
> 30	);
> 31	
> 32	ALTER TABLE public.mcp_access_tokens ENABLE ROW LEVEL SECURITY;
> 33	
> 34	-- Own SELECT/INSERT/UPDATE only (revocation = UPDATE revoked_at). NO DELETE policy → client cannot delete.
> 35	-- The container reads the hash via the service key (bypasses RLS) — it is the ONLY reader of token_hash.
> 36	CREATE POLICY "mcp_tokens_select_own" ON public.mcp_access_tokens
> 37	  FOR SELECT USING (user_id = auth.uid());
> 38	CREATE POLICY "mcp_tokens_insert_own" ON public.mcp_access_tokens
> 39	  FOR INSERT WITH CHECK (user_id = auth.uid());
> 40	CREATE POLICY "mcp_tokens_update_own" ON public.mcp_access_tokens
> 41	  FOR UPDATE USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());
> 42	
> 43	CREATE INDEX IF NOT EXISTS mcp_tokens_hash_idx ON public.mcp_access_tokens (token_hash) WHERE revoked_at IS NULL;
> 44	CREATE INDEX IF NOT EXISTS mcp_tokens_user_idx ON public.mcp_access_tokens (user_id);
> 45	
> 46	COMMENT ON TABLE public.mcp_access_tokens IS
> 47	  'Vision MCP external bearer PATs (FR-VM-003). SHA-256 hash only; closed-vocabulary scopes (DB allowlist CHECK); '
> 48	  '365d expiry ceiling; revoke via UPDATE revoked_at. Container reads hash via service key (sole reader).';
> 49	
> ```

## 🤖 Claude *(17:14:29)*

<details>
<summary>💭 Thinking Process</summary>

Now I'm reviewing the remaining modified files—the SSRF guard, bundle-core, CLI, and edge functions.

</details>


## 🤖 Claude *(17:14:29)*

Now let me read the landing-bundler files and the canonical SSRF guard for comparison.

## 🤖 Claude *(17:14:30)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/landing-bundler/public-url.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// public-url (host port) — SSRF guard for landing-bundler asset fetches (FR-LF-002).
> 2	// ─────────────────────────────────────────────────────────────────────────────
> 3	// Faithful port of supabase/functions/_shared/public-url.ts to the host worker
> 4	// runtime (bun/node): the bundler fetches every external ref found in tenant
> 5	// HTML — caller-controlled input — so the same class of blind-SSRF applies.
> 6	// Invariants (identical to the Deno guard, /security-review 2026-07-14 finding):
> 7	//   · https-only, standard port, no private/loopback/link-local literals
> 8	//   · best-effort DNS resolve check (resolver hiccup does NOT block)
> 9	//   · every 3xx hop is RE-validated — `fetch` with redirect:follow is the bypass
> 10	// Test seam: `deps.fetchImpl` / `deps.resolveIps` are injectable so unit tests
> 11	// prove the internal request is NEVER emitted without touching the network.
> 12	
> 13	import { promises as dns } from "node:dns";
> 14	
> 15	const PRIVATE_V4 = [
> 16	  /^10\./, /^127\./, /^169\.254\./, /^192\.168\./, /^0\./,
> 17	  /^172\.(1[6-9]|2\d|3[01])\./,
> 18	];
> 19	
> 20	export function isPrivateIp(ip: string): boolean {
> 21	  if (ip.includes(":")) {
> 22	    const low = ip.toLowerCase();
> 23	    return low === "::1" || low === "::" || low.startsWith("fe80:") || low.startsWith("fc") || low.startsWith("fd") ||
> 24	      low.startsWith("::ffff:127.") || low.startsWith("::ffff:10.") || low.startsWith("::ffff:192.168.") || low.startsWith("::ffff:169.254.");
> 25	  }
> 26	  return PRIVATE_V4.some((re) => re.test(ip));
> 27	}
> 28	
> 29	export interface GuardDeps {
> 30	  fetchImpl?: typeof fetch;
> 31	  /** Resolve a hostname to its IPs. Defaults to node:dns lookup (A + AAAA). */
> 32	  resolveIps?: (host: string) => Promise<string[]>;
> 33	}
> 34	
> 35	async function defaultResolveIps(host: string): Promise<string[]> {
> 36	  const out: string[] = [];
> 37	  try { out.push(...(await dns.resolve4(host))); } catch { /* best-effort */ }
> 38	  try { out.push(...(await dns.resolve6(host))); } catch { /* best-effort */ }
> 39	  return out;
> 40	}
> 41	
> 42	/** Throws if the URL is not a safe public https endpoint. Returns the parsed URL. */
> 43	export async function assertPublicHttpUrl(raw: string, deps: GuardDeps = {}): Promise<URL> {
> 44	  let url: URL;
> 45	  try { url = new URL(raw); } catch { throw new Error("media_url_invalid"); }
> 46	  if (url.protocol !== "https:") throw new Error("media_url_not_https");
> 47	  if (url.port && url.port !== "443") throw new Error("media_url_nonstandard_port");
> 48	  const host = url.hostname;
> 49	  if (isPrivateIp(host)) throw new Error("media_url_private_address");
> 50	  const resolve = deps.resolveIps ?? defaultResolveIps;
> 51	  const ips = await resolve(host).catch(() => [] as string[]);
> 52	  if (ips.some(isPrivateIp)) throw new Error("media_url_private_address");
> 53	  return url;
> 54	}
> 55	
> 56	/** Máximo de saltos 3xx seguidos manualmente (cada salto é RE-validado). */
> 57	const MAX_REDIRECTS = 3;
> 58	
> 59	/**
> 60	 * fetch() que mantém a garantia do guard ATÉ O ÚLTIMO SALTO (fecha o bypass por
> 61	 * redirect): um host público respondendo `302 Location: http://169.254.169.254/…`
> 62	 * jamais vira requisição interna — o Location é re-validado ANTES de qualquer fetch.
> 63	 */
> 64	export async function fetchPublicUrl(raw: string, init?: RequestInit, deps: GuardDeps = {}): Promise<Response> {
> 65	  const fetchImpl = deps.fetchImpl ?? fetch;
> 66	  let url = await assertPublicHttpUrl(raw, deps);
> 67	  for (let hop = 0; hop <= MAX_REDIRECTS; hop++) {
> 68	    const resp = await fetchImpl(url.toString(), { ...init, redirect: "manual" });
> 69	    if (resp.status < 300 || resp.status > 399) return resp;
> 70	    const location = resp.headers.get("location");
> 71	    if (!location) return resp; // 3xx sem Location: devolve como veio
> 72	    await resp.body?.cancel().catch(() => {}); // não vaza o corpo do redirect
> 73	    url = await assertPublicHttpUrl(new URL(location, url).toString(), deps); // RE-valida o destino
> 74	  }
> 75	  throw new Error("media_url_too_many_redirects");
> 76	}
> 77	
> ```

## 🤖 Claude *(17:14:31)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/_shared/public-url.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// public-url — SSRF guard for server-side fetches of caller-supplied media URLs (Amendment 24 hardening).
> 2	// ─────────────────────────────────────────────────────────────────────────────
> 3	// publish-social fetch()es content.image_url/video_url to forward bytes to a platform. For user-JWT callers
> 4	// that URL is caller-controlled → blind-SSRF primitive against whatever the isolate can reach. This guard
> 5	// closes the class in one place: https-only, standard port, no private/loopback/link-local literals, and a
> 6	// best-effort DNS resolve check (a resolver hiccup does NOT block a legit publish — the residual risk is the
> 7	// caller publishing to their OWN account; the guard's job is killing the internal-network primitive).
> 8	
> 9	const PRIVATE_V4 = [
> 10	  /^10\./, /^127\./, /^169\.254\./, /^192\.168\./, /^0\./,
> 11	  /^172\.(1[6-9]|2\d|3[01])\./,
> 12	];
> 13	
> 14	function isPrivateIp(ip: string): boolean {
> 15	  if (ip.includes(":")) {
> 16	    const low = ip.toLowerCase();
> 17	    return low === "::1" || low === "::" || low.startsWith("fe80:") || low.startsWith("fc") || low.startsWith("fd") ||
> 18	      low.startsWith("::ffff:127.") || low.startsWith("::ffff:10.") || low.startsWith("::ffff:192.168.") || low.startsWith("::ffff:169.254.");
> 19	  }
> 20	  return PRIVATE_V4.some((re) => re.test(ip));
> 21	}
> 22	
> 23	/** Máximo de saltos 3xx que seguimos manualmente (cada salto é RE-validado). */
> 24	const MAX_REDIRECTS = 3;
> 25	
> 26	/**
> 27	 * fetch() que mantém a garantia do guard ATÉ O ÚLTIMO SALTO (fecha o bypass por redirect).
> 28	 *
> 29	 * `assertPublicHttpUrl` só valida a URL INICIAL. Com o `redirect: "follow"` padrão do Deno, um host
> 30	 * público que responde `302 Location: http://169.254.169.254/...` faz o isolate emitir a requisição
> 31	 * para a rede interna — exatamente o primitivo que o guard existe para matar (achado do
> 32	 * /security-review 2026-07-14, Amendment 25). Aqui seguimos os 3xx à MÃO, re-validando cada
> 33	 * `Location` com o mesmo guard, e nunca repassando headers de autenticação entre hosts.
> 34	 *
> 35	 * Use SEMPRE que a URL vier do caller. Para URLs internas/de provider (não caller-controlled),
> 36	 * `fetch` direto continua correto.
> 37	 */
> 38	export async function fetchPublicUrl(raw: string, init?: RequestInit): Promise<Response> {
> 39	  let url = await assertPublicHttpUrl(raw);
> 40	  for (let hop = 0; hop <= MAX_REDIRECTS; hop++) {
> 41	    const resp = await fetch(url.toString(), { ...init, redirect: "manual" });
> 42	    if (resp.status < 300 || resp.status > 399) return resp;
> 43	    const location = resp.headers.get("location");
> 44	    if (!location) return resp;                       // 3xx sem Location: devolve como veio
> 45	    await resp.body?.cancel();                        // não vaza o corpo do redirect
> 46	    url = await assertPublicHttpUrl(new URL(location, url).toString()); // RE-valida o destino
> 47	  }
> 48	  throw new Error("media_url_too_many_redirects");
> 49	}
> 50	
> 51	/** Throws if the URL is not a safe public https endpoint. Returns the parsed URL otherwise. */
> 52	export async function assertPublicHttpUrl(raw: string): Promise<URL> {
> 53	  let url: URL;
> 54	  try { url = new URL(raw); } catch { throw new Error("media_url_invalid"); }
> 55	  if (url.protocol !== "https:") throw new Error("media_url_not_https");
> 56	  if (url.port && url.port !== "443") throw new Error("media_url_nonstandard_port");
> 57	  const host = url.hostname;
> 58	  if (isPrivateIp(host)) throw new Error("media_url_private_address");
> 59	  // Best-effort DNS check (kills name→private-IP tricks; a resolver failure falls through — the fetch itself
> 60	  // would fail the same way, and hard-failing here would break legit publishes on DNS hiccups).
> 61	  try {
> 62	    const [a, aaaa] = await Promise.allSettled([
> 63	      Deno.resolveDns(host, "A"),
> 64	      Deno.resolveDns(host, "AAAA"),
> 65	    ]);
> 66	    const ips = [
> 67	      ...(a.status === "fulfilled" ? a.value : []),
> 68	      ...(aaaa.status === "fulfilled" ? aaaa.value : []),
> 69	    ];
> 70	    if (ips.some(isPrivateIp)) throw new Error("media_url_private_address");
> 71	  } catch (e) {
> 72	    if (e instanceof Error && e.message === "media_url_private_address") throw e;
> 73	    // resolver unavailable → fall through (see note above)
> 74	  }
> 75	  return url;
> 76	}
> 77	
> ```

## 🤖 Claude *(17:14:31)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/landing-bundler/cli.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env bun
> 2	// landing-bundler CLI — the SOP's manual Operator path (docs/processes/landing-bundler.md).
> 3	// Usage: bun run scripts/landing-bundler/cli.ts <input.html> <output.html> [--base <url>]
> 4	// Exit: 0 = bundled (report on stdout) · 1 = structural failure (no partial output written).
> 5	
> 6	import { readFileSync, writeFileSync, renameSync } from "node:fs";
> 7	import { bundleHtml } from "./bundle-core";
> 8	
> 9	const [input, output] = process.argv.slice(2).filter((a) => !a.startsWith("--"));
> 10	const baseIdx = process.argv.indexOf("--base");
> 11	const baseUrl = baseIdx > -1 ? process.argv[baseIdx + 1] : undefined;
> 12	
> 13	if (!input || !output) {
> 14	  console.error("Usage: bun run scripts/landing-bundler/cli.ts <input.html> <output.html> [--base <url>]");
> 15	  process.exit(1);
> 16	}
> 17	
> 18	try {
> 19	  const html = readFileSync(input, "utf8");
> 20	  const { html: bundled, report } = await bundleHtml(html, { baseUrl });
> 21	  // Atomic write (SOP recovery path: no partial output on failure).
> 22	  const tmp = `${output}.tmp-${process.pid}`;
> 23	  writeFileSync(tmp, bundled);
> 24	  renameSync(tmp, output);
> 25	  console.log(JSON.stringify(report, null, 2));
> 26	  process.exit(0);
> 27	} catch (e) {
> 28	  console.error(`landing-bundler structural failure: ${(e as Error).message}`);
> 29	  process.exit(1);
> 30	}
> 31	
> ```

## 🤖 Claude *(17:14:36)*

<details>
<summary>💭 Thinking Process</summary>

The `bundle-core.ts` file shows up as binary in the diff, which is unusual—I should check what's actually in there since it might contain unexpected characters.

</details>


## 🤖 Claude *(17:14:36)*

The SSRF guard port looks faithful. Now let me read the core bundler and the two edge functions.

## 🤖 Claude *(17:14:36)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/landing-bundler/bundle-core.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// bundle-core — landing-bundler FR-LF-002 (P0 centerpiece, landing-factory Fatia 1).
> 2	// ─────────────────────────────────────────────────────────────────────────────
> 3	// Open Design v0.10.0 (pinned) exports HTML with only top-level CSS/JS inlined
> 4	// (inline-assets.ts, byte-identical v0.10.0→main; single-file export does not
> 5	// exist upstream — issue #368). This module makes the document SELF-CONTAINED:
> 6	// every external ref (<img>/<source>/<video poster>/<link stylesheet>/<script src>/
> 7	// CSS url()/@import) is fetched through the SSRF guard, verified by MAGIC BYTES
> 8	// (never the server's Content-Type), and inlined as a data: URI. Stylesheets are
> 9	// bundled recursively (that's where @font-face lives) with a depth cap.
> 10	//
> 11	// Failure semantics (SOP docs/processes/landing-bundler.md):
> 12	//   · fail-OPEN per ref  — one bad asset keeps its original URL + warning entry;
> 13	//     the document is never corrupted by a single fetch failure.
> 14	//   · fail-CLOSED structurally — unparseable input / empty output throws.
> 15	// SSOT: docs/bok/landing-factory/05-sdd.md §2.3/§3.1 · 04-frd.md FR-LF-002/003.
> 16	
> 17	import { fetchPublicUrl, type GuardDeps } from "./public-url";
> 18	
> 19	export interface BundleOptions {
> 20	  /** Base URL to resolve relative refs against. Relative refs without a base are kept + warned. */
> 21	  baseUrl?: string;
> 22	  /** Per-asset byte ceiling (default 5 MiB). Oversized assets are kept + warned (G2). */
> 23	  maxAssetBytes?: number;
> 24	  /** Per-asset byte floor — rejects error stubs masquerading as assets (default 24 B). */
> 25	  minAssetBytes?: number;
> 26	  /** Per-asset fetch timeout ms (default 15_000). */
> 27	  timeoutMs?: number;
> 28	  /** Max recursive stylesheet depth for @import / url() inside fetched CSS (default 3). */
> 29	  maxCssDepth?: number;
> 30	  /** Injectable fetch/DNS for tests (proves the internal request is never emitted). */
> 31	  guardDeps?: GuardDeps;
> 32	}
> 33	
> 34	export interface KeptRef {
> 35	  ref: string;
> 36	  reason: string;
> 37	}
> 38	
> 39	export interface BundleReport {
> 40	  inlined: number;
> 41	  kept: KeptRef[];
> 42	  bytes_in: number;
> 43	  bytes_out: number;
> 44	}
> 45	
> 46	export interface BundleResult {
> 47	  html: string;
> 48	  report: BundleReport;
> 49	}
> 50	
> 51	// ── Magic-byte sniffing (the server's Content-Type is NOT trusted — G3) ──────
> 52	
> 53	interface Sniffed {
> 54	  mime: string;
> 55	  kind: "image" | "font" | "media" | "text";
> 56	}
> 57	
> 58	function sniff(bytes: Uint8Array): Sniffed | null {
> 59	  const b = bytes;
> 60	  const ascii = (start: number, len: number) =>
> 61	    Array.from(b.slice(start, start + len)).map((c) => String.fromCharCode(c)).join("");
> 62	  if (b.length >= 8 && b[0] === 0x89 && ascii(1, 3) === "PNG") return { mime: "image/png", kind: "image" };
> 63	  if (b.length >= 3 && b[0] === 0xff && b[1] === 0xd8 && b[2] === 0xff) return { mime: "image/jpeg", kind: "image" };
> 64	  if (ascii(0, 6) === "GIF87a" || ascii(0, 6) === "GIF89a") return { mime: "image/gif", kind: "image" };
> 65	  if (ascii(0, 4) === "RIFF" && ascii(8, 4) === "WEBP") return { mime: "image/webp", kind: "image" };
> 66	  if (ascii(0, 4) === "wOFF") return { mime: "font/woff", kind: "font" };
> 67	  if (ascii(0, 4) === "wOF2") return { mime: "font/woff2", kind: "font" };
> 68	  if (ascii(0, 4) === "OTTO") return { mime: "font/otf", kind: "font" };
> 69	  if (b.length >= 4 && b[0] === 0x00 && b[1] === 0x01 && b[2] === 0x00 && b[3] === 0x00) return { mime: "font/ttf", kind: "font" };
> 70	  if (b.length >= 12 && ascii(4, 4) === "ftyp") return { mime: "video/mp4", kind: "media" };
> 71	  if (b.length >= 4 && b[0] === 0x1a && b[1] === 0x45 && b[2] === 0xdf && b[3] === 0xa3) return { mime: "video/webm", kind: "media" };
> 72	  if (b.length >= 2 && b[0] === 0x49 && b[1] === 0x44 && b[2] === 0x33) return { mime: "audio/mpeg", kind: "media" };
> 73	  if (b.length >= 2 && b[0] === 0x00 && b[1] === 0x00 && (b[2] === 0x01 || b[2] === 0x02)) return { mime: "image/x-icon", kind: "image" };
> 74	  // Text formats: reject anything with NUL bytes, then look at content.
> 75	  const head = ascii(0, Math.min(b.length, 512));
> 76	  if (head.includes(" ")) return null;
> 77	  const trimmed = head.replace(/^﻿/, "").trimStart().toLowerCase();
> 78	  if (trimmed.startsWith("<svg") || (trimmed.startsWith("<?xml") && head.toLowerCase().includes("<svg"))) {
> 79	    return { mime: "image/svg+xml", kind: "image" };
> 80	  }
> 81	  if (trimmed.startsWith("<!doctype html") || trimmed.startsWith("<html")) return null; // challenge page ≠ asset (G3)
> 82	  return { mime: "text/plain", kind: "text" };
> 83	}
> 84	
> 85	/** Expected kind by ref context — a stylesheet must sniff as text, an <img> as image, etc. */
> 86	type ExpectKind = "image" | "font" | "media" | "css" | "js" | "any";
> 87	
> 88	function kindAccepts(expect: ExpectKind, s: Sniffed): boolean {
> 89	  switch (expect) {
> 90	    case "image": return s.kind === "image";
> 91	    case "font": return s.kind === "font";
> 92	    case "media": return s.kind === "media" || s.kind === "image"; // <video poster> et al.
> 93	    case "css":
> 94	    case "js": return s.kind === "text" || s.kind === "image"; // svg-in-css never happens; text is the bar
> 95	    case "any": return true;
> 96	  }
> 97	}
> 98	
> 99	function mimeFor(expect: ExpectKind, s: Sniffed): string {
> 100	  if (expect === "css" && s.kind === "text") return "text/css";
> 101	  if (expect === "js" && s.kind === "text") return "text/javascript";
> 102	  return s.mime;
> 103	}
> 104	
> 105	// ── Guarded fetch → bytes (fail-open per ref: null + reason) ─────────────────
> 106	
> 107	interface FetchedAsset {
> 108	  bytes: Uint8Array;
> 109	  mime: string;
> 110	}
> 111	
> 112	async function fetchAsset(
> 113	  url: string,
> 114	  expect: ExpectKind,
> 115	  opts: Required<Pick<BundleOptions, "maxAssetBytes" | "minAssetBytes" | "timeoutMs">> & { guardDeps?: GuardDeps },
> 116	): Promise<FetchedAsset | { error: string }> {
> 117	  try {
> 118	    const ctrl = new AbortController();
> 119	    const timer = setTimeout(() => ctrl.abort(), opts.timeoutMs);
> 120	    let resp: Response;
> 121	    try {
> 122	      resp = await fetchPublicUrl(url, { signal: ctrl.signal }, opts.guardDeps);
> 123	    } finally {
> 124	      clearTimeout(timer);
> 125	    }
> 126	    if (!resp.ok) return { error: `http_${resp.status}` };
> 127	    const buf = new Uint8Array(await resp.arrayBuffer());
> 128	    // The anti-stub floor targets BINARY assets (an error-JSON stub is never a
> 129	    // valid PNG/font/video). Tiny css/js files are legitimate — for text the
> 130	    // challenge-page magic-byte check below is the honest gate.
> 131	    const binary = expect === "image" || expect === "font" || expect === "media";
> 132	    if (binary && buf.length < opts.minAssetBytes) return { error: "asset_below_floor" };
> 133	    if (buf.length > opts.maxAssetBytes) return { error: "asset_above_ceiling" };
> 134	    const sniffed = sniff(buf);
> 135	    if (!sniffed || !kindAccepts(expect, sniffed)) return { error: "magic_bytes_mismatch" };
> 136	    return { bytes: buf, mime: mimeFor(expect, sniffed) };
> 137	  } catch (e) {
> 138	    return { error: (e as Error).message || "fetch_failed" };
> 139	  }
> 140	}
> 141	
> 142	function toDataUri(asset: FetchedAsset): string {
> 143	  return `data:${asset.mime};base64,${Buffer.from(asset.bytes).toString("base64")}`;
> 144	}
> 145	
> 146	// ── Ref resolution ───────────────────────────────────────────────────────────
> 147	
> 148	/** Resolve a raw ref to an absolute https URL, or classify why it is skipped. */
> 149	function resolveRef(raw: string, baseUrl?: string): { url: string } | { skip: string } {
> 150	  const t = raw.trim();
> 151	  if (!t) return { skip: "empty" };
> 152	  if (t.startsWith("data:") || t.startsWith("#") || t.startsWith("blob:") || t.startsWith("javascript:") || t.startsWith("about:")) {
> 153	    return { skip: "non_fetchable_scheme" };
> 154	  }
> 155	  if (/^https:\/\//i.test(t)) return { url: t };
> 156	  if (/^http:\/\//i.test(t)) return { skip: "insecure_http" };
> 157	  if (t.startsWith("//")) return { url: `https:${t}` };
> 158	  if (baseUrl) {
> 159	    try { return { url: new URL(t, baseUrl).toString() }; } catch { return { skip: "unresolvable_relative" }; }
> 160	  }
> 161	  return { skip: "relative_without_base" };
> 162	}
> 163	
> 164	// ── CSS bundling (recursive — @font-face lives here) ─────────────────────────
> 165	
> 166	const CSS_URL_RE = /url\(\s*(?:'([^']*)'|"([^"]*)"|([^)'"\s][^)]*?))\s*\)/g;
> 167	const CSS_IMPORT_RE = /@import\s+(?:url\(\s*(?:'([^']*)'|"([^"]*)"|([^)'"\s][^)]*?))\s*\)|'([^']*)'|"([^"]*)")\s*([^;]*);/g;
> 168	
> 169	interface BundleCtx {
> 170	  opts: Required<Omit<BundleOptions, "guardDeps" | "baseUrl">> & { baseUrl?: string; guardDeps?: GuardDeps };
> 171	  inlined: number;
> 172	  kept: KeptRef[];
> 173	}
> 174	
> 175	function expectKindForCssUrl(ref: string): ExpectKind {
> 176	  if (/\.(woff2?|ttf|otf|eot)(\?|#|$)/i.test(ref)) return "font";
> 177	  if (/\.(png|jpe?g|gif|webp|svg|ico|avif)(\?|#|$)/i.test(ref)) return "image";
> 178	  return "any";
> 179	}
> 180	
> 181	async function bundleCss(css: string, cssBase: string | undefined, depth: number, ctx: BundleCtx): Promise<string> {
> 182	  if (depth > ctx.opts.maxCssDepth) return css;
> 183	
> 184	  // 1. @import — fetch the imported sheet, bundle it recursively, splice it in.
> 185	  const imports: Array<{ match: string; ref: string; media: string }> = [];
> 186	  for (const m of css.matchAll(CSS_IMPORT_RE)) {
> 187	    imports.push({ match: m[0], ref: m[1] ?? m[2] ?? m[3] ?? m[4] ?? m[5] ?? "", media: (m[6] ?? "").trim() });
> 188	  }
> 189	  for (const imp of imports) {
> 190	    const resolved = resolveRef(imp.ref, cssBase ?? ctx.opts.baseUrl);
> 191	    if ("skip" in resolved) {
> 192	      if (resolved.skip !== "non_fetchable_scheme") ctx.kept.push({ ref: imp.ref, reason: resolved.skip });
> 193	      continue;
> 194	    }
> 195	    const asset = await fetchAsset(resolved.url, "css", ctx.opts);
> 196	    if ("error" in asset) {
> 197	      ctx.kept.push({ ref: resolved.url, reason: asset.error });
> 198	      continue;
> 199	    }
> 200	    let imported = new TextDecoder().decode(asset.bytes);
> 201	    imported = await bundleCss(imported, resolved.url, depth + 1, ctx);
> 202	    const replacement = imp.media ? `@media ${imp.media} {\n${imported}\n}` : imported;
> 203	    css = css.replace(imp.match, replacement);
> 204	    ctx.inlined++;
> 205	  }
> 206	
> 207	  // 2. url(...) — fonts/images referenced by the sheet.
> 208	  const urlJobs: Array<{ match: string; ref: string }> = [];
> 209	  for (const m of css.matchAll(CSS_URL_RE)) {
> 210	    const ref = m[1] ?? m[2] ?? m[3] ?? "";
> 211	    if (!ref || ref.startsWith("data:")) continue;
> 212	    urlJobs.push({ match: m[0], ref });
> 213	  }
> 214	  for (const job of urlJobs) {
> 215	    const resolved = resolveRef(job.ref, cssBase ?? ctx.opts.baseUrl);
> 216	    if ("skip" in resolved) {
> 217	      if (resolved.skip !== "non_fetchable_scheme") ctx.kept.push({ ref: job.ref, reason: resolved.skip });
> 218	      continue;
> 219	    }
> 220	    const asset = await fetchAsset(resolved.url, expectKindForCssUrl(job.ref), ctx.opts);
> 221	    if ("error" in asset) {
> 222	      ctx.kept.push({ ref: resolved.url, reason: asset.error });
> 223	      continue;
> 224	    }
> 225	    css = css.split(job.match).join(`url(${toDataUri(asset)})`);
> 226	    ctx.inlined++;
> 227	  }
> 228	  return css;
> 229	}
> 230	
> 231	// ── HTML attribute refs ──────────────────────────────────────────────────────
> 232	
> 233	interface AttrTarget {
> 234	  tagRe: RegExp;
> 235	  attr: string;
> 236	  expect: ExpectKind;
> 237	}
> 238	
> 239	// Machine-generated Open Design HTML — attribute regexes are adequate here
> 240	// (no exotic authoring); a full DOM parser is deliberately avoided on the host.
> 241	const ATTR_TARGETS: AttrTarget[] = [
> 242	  { tagRe: /<img\b[^>]*>/gi, attr: "src", expect: "image" },
> 243	  { tagRe: /<source\b[^>]*>/gi, attr: "src", expect: "media" },
> 244	  { tagRe: /<source\b[^>]*>/gi, attr: "srcset", expect: "media" },
> 245	  { tagRe: /<video\b[^>]*>/gi, attr: "src", expect: "media" },
> 246	  { tagRe: /<video\b[^>]*>/gi, attr: "poster", expect: "image" },
> 247	  { tagRe: /<audio\b[^>]*>/gi, attr: "src", expect: "media" },
> 248	];
> 249	
> 250	function attrValue(tag: string, attr: string): { raw: string; quoted: string } | null {
> 251	  const m = tag.match(new RegExp(`\\b${attr}\\s*=\\s*("([^"]*)"|'([^']*)')`, "i"));
> 252	  if (!m) return null;
> 253	  return { raw: m[2] ?? m[3] ?? "", quoted: m[1] };
> 254	}
> 255	
> 256	// ── Public API ───────────────────────────────────────────────────────────────
> 257	
> 258	export async function bundleHtml(html: string, options: BundleOptions = {}): Promise<BundleResult> {
> 259	  if (typeof html !== "string" || !/<html[\s>]|<!doctype/i.test(html)) {
> 260	    throw new Error("bundle_input_not_html"); // structural fail-closed
> 261	  }
> 262	  const ctx: BundleCtx = {
> 263	    opts: {
> 264	      baseUrl: options.baseUrl,
> 265	      maxAssetBytes: options.maxAssetBytes ?? 5 * 1024 * 1024,
> 266	      minAssetBytes: options.minAssetBytes ?? 24,
> 267	      timeoutMs: options.timeoutMs ?? 15_000,
> 268	      maxCssDepth: options.maxCssDepth ?? 3,
> 269	      guardDeps: options.guardDeps,
> 270	    },
> 271	    inlined: 0,
> 272	    kept: [],
> 273	  };
> 274	  const bytesIn = Buffer.byteLength(html);
> 275	  let out = html;
> 276	
> 277	  // 1. <link rel="stylesheet" href> → <style>bundled css</style>
> 278	  const linkTags = [...out.matchAll(/<link\b[^>]*>/gi)].map((m) => m[0])
> 279	    .filter((t) => /rel\s*=\s*["']?stylesheet["']?/i.test(t));
> 280	  for (const tag of linkTags) {
> 281	    const href = attrValue(tag, "href");
> 282	    if (!href) continue;
> 283	    const resolved = resolveRef(href.raw, ctx.opts.baseUrl);
> 284	    if ("skip" in resolved) {
> 285	      if (resolved.skip !== "non_fetchable_scheme") ctx.kept.push({ ref: href.raw, reason: resolved.skip });
> 286	      continue;
> 287	    }
> 288	    const asset = await fetchAsset(resolved.url, "css", ctx.opts);
> 289	    if ("error" in asset) {
> 290	      ctx.kept.push({ ref: resolved.url, reason: asset.error });
> 291	      continue;
> 292	    }
> 293	    let css = new TextDecoder().decode(asset.bytes);
> 294	    css = await bundleCss(css, resolved.url, 1, ctx);
> 295	    out = out.replace(tag, `<style data-bundled-from="${resolved.url}">\n${css}\n</style>`);
> 296	    ctx.inlined++;
> 297	  }
> 298	
> 299	  // 2. <script src> → inline <script> (same type attribute preserved).
> 300	  const scriptTags = [...out.matchAll(/<script\b[^>]*\bsrc\s*=\s*("[^"]*"|'[^']*')[^>]*>\s*<\/script>/gi)].map((m) => m[0]);
> 301	  for (const tag of scriptTags) {
> 302	    const src = attrValue(tag, "src");
> 303	    if (!src) continue;
> 304	    const resolved = resolveRef(src.raw, ctx.opts.baseUrl);
> 305	    if ("skip" in resolved) {
> 306	      if (resolved.skip !== "non_fetchable_scheme") ctx.kept.push({ ref: src.raw, reason: resolved.skip });
> 307	      continue;
> 308	    }
> 309	    const asset = await fetchAsset(resolved.url, "js", ctx.opts);
> 310	    if ("error" in asset) {
> 311	      ctx.kept.push({ ref: resolved.url, reason: asset.error });
> 312	      continue;
> 313	    }
> 314	    const body = new TextDecoder().decode(asset.bytes);
> 315	    // A module that itself imports other externals cannot be naively inlined — keep + warn (honest MVP limit).
> 316	    const isModule = /type\s*=\s*["']?module["']?/i.test(tag);
> 317	    if (isModule && /(^|\n)\s*import\s.+from\s+["']https?:/m.test(body)) {
> 318	      ctx.kept.push({ ref: resolved.url, reason: "esm_with_external_imports" });
> 319	      continue;
> 320	    }
> 321	    const openTag = tag.replace(/\bsrc\s*=\s*("[^"]*"|'[^']*')/i, "").replace(/></, `>${"\n"}<`).split("\n")[0];
> 322	    out = out.replace(tag, `${openTag}\n${body}\n</script>`);
> 323	    ctx.inlined++;
> 324	  }
> 325	
> 326	  // 3. Media/img attributes → data: URIs.
> 327	  for (const target of ATTR_TARGETS) {
> 328	    const tags = [...out.matchAll(target.tagRe)].map((m) => m[0]);
> 329	    for (const tag of tags) {
> 330	      const val = attrValue(tag, target.attr);
> 331	      if (!val || val.raw.startsWith("data:")) continue;
> 332	      if (target.attr === "srcset") { // srcset is a list — MVP: keep + warn if external
> 333	        if (/https?:\/\//i.test(val.raw)) ctx.kept.push({ ref: val.raw.slice(0, 120), reason: "srcset_not_bundled" });
> 334	        continue;
> 335	      }
> 336	      const resolved = resolveRef(val.raw, ctx.opts.baseUrl);
> 337	      if ("skip" in resolved) {
> 338	        if (resolved.skip !== "non_fetchable_scheme") ctx.kept.push({ ref: val.raw, reason: resolved.skip });
> 339	        continue;
> 340	      }
> 341	      const asset = await fetchAsset(resolved.url, target.expect, ctx.opts);
> 342	      if ("error" in asset) {
> 343	        ctx.kept.push({ ref: resolved.url, reason: asset.error });
> 344	        continue;
> 345	      }
> 346	      const newTag = tag.replace(val.quoted, `"${toDataUri(asset)}"`);
> 347	      out = out.split(tag).join(newTag);
> 348	      ctx.inlined++;
> 349	    }
> 350	  }
> 351	
> 352	  // 4. Inline <style> blocks + style="" attributes (url() refs — backgrounds, fonts).
> 353	  const styleBlocks = [...out.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style>/gi)];
> 354	  for (const m of styleBlocks) {
> 355	    const bundled = await bundleCss(m[1], ctx.opts.baseUrl, 1, ctx);
> 356	    if (bundled !== m[1]) out = out.replace(m[0], m[0].replace(m[1], bundled));
> 357	  }
> 358	  const styleAttrs = [...out.matchAll(/style\s*=\s*"([^"]*url\([^"]*)"/gi)];
> 359	  for (const m of styleAttrs) {
> 360	    const bundled = await bundleCss(m[1], ctx.opts.baseUrl, ctx.opts.maxCssDepth, ctx); // no recursion budget needed
> 361	    if (bundled !== m[1]) out = out.split(m[0]).join(m[0].replace(m[1], bundled));
> 362	  }
> 363	
> 364	  if (!out.trim()) throw new Error("bundle_output_empty"); // structural fail-closed
> 365	  return {
> 366	    html: out,
> 367	    report: { inlined: ctx.inlined, kept: ctx.kept, bytes_in: bytesIn, bytes_out: Buffer.byteLength(out) },
> 368	  };
> 369	}
> 370	
> 371	/**
> 372	 * Seam FR-LF-003: inject a fragment (tokens.css MIV / posthog phc_ snippet / OSS NOTICE)
> 373	 * as the LAST children of <head>. Idempotent by marker attribute.
> 374	 */
> 375	export function injectHead(html: string, fragment: string, markerId: string): string {
> 376	  if (html.includes(`data-lf-inject="${markerId}"`)) return html; // idempotent
> 377	  const wrapped = `<!-- landing-factory inject:${markerId} --><meta data-lf-inject="${markerId}">${fragment}`;
> 378	  const closeHead = html.match(/<\/head\s*>/i);
> 379	  if (closeHead) return html.replace(closeHead[0], `${wrapped}\n${closeHead[0]}`);
> 380	  // Document without <head> (WordPress-page body sink, OTD-LF-003): prepend.
> 381	  return `${wrapped}\n${html}`;
> 382	}
> 383	
> ```

## 🤖 Claude *(17:15:33)*

<details>
<summary>💭 Thinking Process</summary>

Looking at the SSRF protections in bundle-core.ts, I can see how external references flow through `fetchAsset` into `fetchPublicUrl` where the actual guard sits. The `resolveRef` function filters out unsafe protocols like `data:`, `javascript:`, and `about:`, while also rejecting plain HTTP URLs. Interestingly, protocol-relative URLs get upgraded to HTTPS automatically rather than being blocked.

All fetches go through `fetchPublicUrl`, which enforces HTTPS-only access, blocks private IP ranges, performs DNS resolution checks, and re-validates redirects. This looks solid overall. However, there's a potential DNS rebinding vulnerability here — the guard resolves DNS and validates the IP is public, but then `fetch()` performs its own DNS resolution. An attacker controlling DNS could return a public IP during the validation check and a private IP during the actual fetch, exploiting the time-of-check-time-of-use window. That said, this is a known limitation that exists in the canonical guard too, so it's not a newly introduced issue.

Looking at the actual implementation differences, the port appears faithful to the original. One key difference is that the canonical version uses `Deno.resolveDns` while the port uses Node's `dns.resolve4` and `dns.resolve6` — both resolve A and AAAA records and are best-effort, so that's equivalent. The port's `defaultResolveIps` uses `dns.resolve*` which bypasses the local hosts file and performs actual DNS queries, which is appropriate for SSRF protection since it queries authoritative DNS servers.

However, there's a subtle issue: `dns.resolve4` won't resolve hostnames that only exist in `/etc/hosts` like `localhost`, so it returns an empty array. This means the private-IP check passes (no IPs to validate), but then `fetch('https://localhost/')` uses the OS resolver which does honor `/etc/hosts` and resolves to 127.0.0.1. The earlier `isPrivateIp(host)` check on the hostname "localhost" itself returns false since it's not an IP literal and doesn't match the private IP regexes.

The same vulnerability exists in Deno's guard — `Deno.resolveDns` also relies on the system resolver and may not honor `/etc/hosts` entries.

But exploiting this requires HTTPS on localhost with port 443, and the tenant would need to explicitly put `https://localhost/` in their HTML, which seems unlikely since the whole point is that tenant HTML is controlled by...

actually, wait, that's the attack surface. Still, this DNS behavior gap exists in the canonical implementation too, so it's not a new issue introduced by this port. The task says not to flag pre-existing concerns.

Let me look more carefully at whether `Deno.resolveDns` actually behaves differently from `node:dns` here. Both bypass /etc/hosts, so the behavior should be equivalent. Now I need to examine the redirect handling logic to see if there's a meaningful difference in how the port implements `fetchPublicUrl`.

The port uses `deps.fetchImpl ?? fetch` and passes `deps` to `assertPublicHttpUrl`, which is faithful to the original. The landing-bundler SSRF protection looks solid.

Now I'm examining the CSS bundling logic. When `bundleCss` fetches external stylesheets from URLs controlled by tenant HTML, it decodes the bytes and inlines them directly into `<style>` blocks. This creates a potential XSS vector — if the fetched CSS contains something like `</style><script>alert(1)</script>`, it could break out of the style context and execute arbitrary code.

Looking at the code that handles this, there's no escaping of `</style>` sequences in the CSS content before it gets spliced into the output HTML. However, the key question is whether this actually constitutes a vulnerability: the landing page is tenant-controlled to begin with, so the tenant is essentially injecting into their own page. The real threat would be if an attacker could control the external CSS URL that gets fetched, but that depends on who controls those external resources.

The magic-byte sniffing for CSS files checks whether the content is actually CSS or something else, requiring the sniff to identify it as text or image content rather than HTML or other formats. Actually, I need to check if that's a space character or a NUL byte — the comment mentions rejecting NUL bytes, but the code is checking for a space, which would mean any CSS with whitespace in the first 512 characters gets rejected from inlining. > injection would let a tenant inject `</style><script>` into the CSS, breaking out of the style tag and executing arbitrary code. But since the tenant controls both the HTML source and which URLs get referenced, this is really just self-XSS — they could inject the script directly into their own HTML anyway. The real question is whether the landing-factory accepts untrusted third-party HTML, but even then, any malicious scripts in the original HTML would already be present, so inlining CSS doesn't introduce a new attack surface.

Looking at `injectHead`, the fragment gets injected raw, but it's caller-provided (tokens.css, PostHog snippet) rather than tenant-controlled, so that's not a concern either.

Now I'm examining the edge functions, starting with the detect-viral-moments and youtube-data diffs.

</details>


## 🤖 Claude *(17:15:33)*

Now let me examine the two edge function changes with their diffs.

## 🤖 Claude *(17:15:33)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git diff origin/main...HEAD -- supabase/functions/detect-viral-moments/index.ts supabase/functions/youtube-data/index.ts",
  "description": "Show diffs for the two edge functions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> diff --git a/supabase/functions/detect-viral-moments/index.ts b/supabase/functions/detect-viral-moments/index.ts
> index 547c113..5671fdf 100644
> --- a/supabase/functions/detect-viral-moments/index.ts
> +++ b/supabase/functions/detect-viral-moments/index.ts
> @@ -114,7 +114,10 @@ serve(async (req) => {
>      const openRouterKey = userKeys?.openrouter_api_key as string | undefined;
>      const groqKey = userKeys?.groq_api_key as string | undefined;
>      const geminiKey = userKeys?.google_api_key as string | undefined;
> -    const aiKey = openRouterKey || groqKey;
> +    // FR-VR-010 contract: openrouter OR gemini OR groq — a Gemini-only tenant is
> +    // valid (the cascade in fetchLLMWithFallback already speaks Gemini; the gate
> +    // must not reject what the dispatcher supports).
> +    const aiKey = openRouterKey || groqKey || geminiKey;
>      if (!aiKey) {
>        return json({ error: "ai_not_configured", action: "Configure sua chave de IA em /dashboard/settings" }, 402);
>      }
> @@ -127,10 +130,17 @@ serve(async (req) => {
>      charged = true; chargedUser = user.id;
>  
>      const usingGroq = !openRouterKey && !!groqKey;
> -    const endpoint = usingGroq
> +    const usingGemini = !openRouterKey && !groqKey && !!geminiKey;
> +    const endpoint = usingGemini
> +      ? "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
> +      : usingGroq
>        ? "https://api.groq.com/openai/v1/chat/completions"
>        : "https://openrouter.ai/api/v1/chat/completions";
> -    const model = usingGroq ? "llama-3.3-70b-versatile" : "meta-llama/llama-3.3-70b-instruct";
> +    const model = usingGemini
> +      ? "gemini-2.5-flash"
> +      : usingGroq
> +      ? "llama-3.3-70b-versatile"
> +      : "meta-llama/llama-3.3-70b-instruct";
>  
>      const sys =
>        "Você é um editor viral especialista (estilo Alex Hormozi). Recebe a transcrição legendada (cues numeradas " +
> @@ -154,8 +164,12 @@ serve(async (req) => {
>          headers: {
>            Authorization: `Bearer ${aiKey}`,
>            "Content-Type": "application/json",
> -          "HTTP-Referer": "https://mcorch.com",
> -          "X-Title": "GCRUX Constellation",
> +          // OpenRouter-specific attribution headers — the Gemini OpenAI-compat
> +          // endpoint rejects unknown headers (mirrors the cascade's deletes).
> +          ...(usingGemini ? {} : {
> +            "HTTP-Referer": "https://mcorch.com",
> +            "X-Title": "GCRUX Constellation",
> +          }),
>          },
>          body: JSON.stringify({
>            model,
> diff --git a/supabase/functions/youtube-data/index.ts b/supabase/functions/youtube-data/index.ts
> index d69b2fd..4f6c4d6 100644
> --- a/supabase/functions/youtube-data/index.ts
> +++ b/supabase/functions/youtube-data/index.ts
> @@ -201,6 +201,25 @@ Deno.serve(async (req) => {
>        );
>        if (!r.ok) return googleError(r, pulse);
>        pulse("healthy");
> +      // Mesh Connection Mandate (CLAUDE.md §3): observation node on FIRST successful
> +      // sync — dedup by deterministic name, best-effort, never blocks the response.
> +      const syncName = `youtube-studio:first-sync:${user.id}`;
> +      const channelId = r.data.items?.[0]?.id ?? null;
> +      admin.from("mcorch_nodes").select("id").eq("name", syncName).limit(1).maybeSingle().then(
> +        ({ data: existing }) => {
> +          if (existing) return;
> +          admin.from("mcorch_nodes").insert({
> +            user_id: user.id,
> +            node_type: "observation",
> +            name: syncName,
> +            content:
> +              `Primeiro sync bem-sucedido do painel YouTube Studio (channel_summary${channelId ? `, canal ${channelId}` : ""}). ` +
> +              `Fecha o Mesh Connection Mandate do módulo youtube-studio (Pattern #8).`,
> +            metadata: { kind: "youtube_first_sync", channel_id: channelId, fr: "FR-YT-panel" },
> +          }).then(() => {}, () => {});
> +        },
> +        () => {},
> +      );
>        return json({ channel: r.data.items?.[0] ?? null });
>      }
>  
> @@ -317,7 +336,19 @@ Deno.serve(async (req) => {
>        const r = await gsend(`${YT_DATA}/videos?id=${encodeURIComponent(videoId)}`, "DELETE");
>        // 204 = deleted (no body). Anything else that is not ok is a real error.
>        if (!r.ok && r.status !== 204) return googleError(r, pulse);
> -      pulse("healthy");
> +      // Distinguishable telemetry: a permanent delete must never look like a plain
> +      // list in the HUD. The event carries NO per-tenant payload (infra_health_logs
> +      // is global-read); the audit trail with the videoId lives in the mesh (RLS-scoped).
> +      admin.from("infra_health_logs").insert({
> +        service: "youtube-studio", status: "healthy", event: "video_deleted",
> +      }).then(() => {}, () => {});
> +      admin.from("mcorch_nodes").insert({
> +        user_id: user.id,
> +        node_type: "observation",
> +        name: `youtube-studio:delete:${videoId}`,
> +        content: `delete_video PERMANENTE do vídeo ${videoId} via painel YouTube Studio (escopo force-ssl, Amendment 12). Trilha de auditoria.`,
> +        metadata: { kind: "youtube_delete", video_id: videoId },
> +      }).then(() => {}, () => {});
>        return json({ deleted: true, videoId });
>      }
> ```

## 🤖 Claude *(17:15:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "python3 -c \"\ndata=open('scripts/landing-bundler/bundle-core.ts','rb').read()\nprint('has NUL byte:', b'\\x00' in data)\nimport re\nfor i,ln in enumerate(data.split(b'\\n'),1):\n    if b'\\x00' in ln:\n        print('NUL on line', i, repr(ln[:90]))\n\"",
  "description": "Check for NUL byte in bundle-core line 76"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> has NUL byte: True
> NUL on line 76 b'  if (head.includes("\x00")) return null;'
> ```

## 🤖 Claude *(17:16:03)*

<details>
<summary>💭 Thinking Process</summary>

I'm verifying that line 76 correctly checks for NUL bytes as documented. Now I'm looking at the detect-viral-moments function, which adds a Gemini-only BYOK path that prioritizes the user's own API key over shared ones, then configures the appropriate endpoint and headers based on which key is available.

The logic chains the keys with fallback precedence — if OpenRouter is set, use that; otherwise Groq; otherwise Gemini — and the endpoint/model/headers are hardcoded, not user-controlled, so there's no injection risk. The Authorization header correctly sends the selected key to its matching provider endpoint, preventing any cross-provider key leakage. The `usingGemini` flag accurately reflects when only the Gemini key is present, ensuring the right key reaches the right service.

For the YouTube data additions, the channel summary success path inserts an observation node into the database using the service role client with the user's ID and a channel ID from Google's API response — all parameterized queries, no injection risk. On delete, a video ID from the request gets inserted into the node's name, content, and metadata fields, also via parameterized queries, so even though it's user-supplied, there's no SQL injection vulnerability. The video ID was already URL-encoded for the Google API call, and storing it as a plain string value in the mesh node is safe.

The service role client bypasses row-level security but correctly inserts with the user's ID, and since these operations run after JWT authentication, authorization is properly enforced. I should verify that the surrounding code confirms the user is authenticated before these operations execute and that the delete action itself is properly authorized.

The mcorch_nodes table is scoped per-user via RLS, so each user only sees their own nodes containing their own video IDs. The infra_health_logs table deliberately avoids leaking sensitive data like videoId into the globally-readable logs, which is good design. The edge functions appear secure overall.

Now I need to check the remaining files—useMcpTokens.ts, mint-vision-pat.ts, and the e2e runner regex change. The PAT allowlist migration adds 'swarm:read' to the allowlist, which I should verify is a safe scope addition.

The 'swarm:read' scope gates the Tier 1 sensory tool in read-only mode. The allowlist still enforces the closed vocabulary constraint and the subset check remains in place, so this is just a straightforward extension of the allowlist for an existing live tool—no privilege escalation beyond what's intended. Not a finding.

Let me verify that useMcpTokens.ts and mint-vision-pat.ts haven't removed any scope validation logic.

</details>


## 🤖 Claude *(17:16:03)*

Now let me check the PAT scope vocabulary changes and the e2e runner regex change.

## 🤖 Claude *(17:16:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git diff -- src/hooks/useMcpTokens.ts && echo \"=== mint-vision-pat ===\" && git diff -- scripts/qa/mint-vision-pat.ts && echo \"=== e2e runner + related (vs origin) ===\" && git diff origin/main...HEAD -- scripts/qa/e2e-user-zero/runner.ts scripts/qa/e2e-user-zero/lib/browser-driver.ts scripts/qa/e2e-user-zero/flows/auth-login.ts scripts/qa/e2e-user-zero/flows/_nav-capture.ts",
  "description": "Diffs for PAT scope and e2e changes"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> diff --git a/src/hooks/useMcpTokens.ts b/src/hooks/useMcpTokens.ts
> index 747aca3..c000f94 100644
> --- a/src/hooks/useMcpTokens.ts
> +++ b/src/hooks/useMcpTokens.ts
> @@ -17,7 +17,7 @@ export const PAT_PREFIX = "mcorch_pat_";
>  // Closed scope vocabulary — MUST mirror ALL_SCOPES in packages/vision-mcp-core/src/auth/identity.ts and the
>  // DB allowlist CHECK in migration 20260615180000. Scopes EXCLUDE credential/billing management (FM-VM-06): a
>  // leaked PAT can only consume tools, never reach the wallet or other tenants' credentials.
> -export const MCP_SCOPES = ["mesh:read", "vision:read", "deepsearch:run", "mesh:write"] as const;
> +export const MCP_SCOPES = ["mesh:read", "vision:read", "deepsearch:run", "mesh:write", "swarm:read"] as const;
>  export type McpScope = (typeof MCP_SCOPES)[number];
>  
>  export const SCOPE_LABELS: Record<McpScope, string> = {
> @@ -25,6 +25,7 @@ export const SCOPE_LABELS: Record<McpScope, string> = {
>    "vision:read": "Percepção visual (descrever imagem/vídeo)",
>    "deepsearch:run": "Deepsearch fundamentado (scrape + run)",
>    "mesh:write": "Consolidar referências na malha (escrita)",
> +  "swarm:read": "Gate sensorial Tier 1 (loudness + contraste, 0 mco)",
>  };
>  
>  // DB ceiling is 365d (pat_expiry_ceiling CHECK); the app default is 90d (DD-VM-002).
> === mint-vision-pat ===
> diff --git a/scripts/qa/mint-vision-pat.ts b/scripts/qa/mint-vision-pat.ts
> index e58d3f6..2f29b2e 100644
> --- a/scripts/qa/mint-vision-pat.ts
> +++ b/scripts/qa/mint-vision-pat.ts
> @@ -22,7 +22,7 @@ if (!URL || !SVC || !email) {
>    process.exit(1);
>  }
>  
> -const ALL_SCOPES = ["mesh:read", "vision:read", "deepsearch:run", "mesh:write"];
> +const ALL_SCOPES = ["mesh:read", "vision:read", "deepsearch:run", "mesh:write", "swarm:read"];
>  const arg = (flag: string) => {
>    const i = process.argv.indexOf(flag);
>    return i >= 0 ? process.argv[i + 1] : undefined;
> === e2e runner + related (vs origin) ===
> diff --git a/scripts/qa/e2e-user-zero/flows/_nav-capture.ts b/scripts/qa/e2e-user-zero/flows/_nav-capture.ts
> index 851e439..34d2b79 100644
> --- a/scripts/qa/e2e-user-zero/flows/_nav-capture.ts
> +++ b/scripts/qa/e2e-user-zero/flows/_nav-capture.ts
> @@ -44,7 +44,10 @@ export function navCaptureFlow(
>    };
>  
>    driver.open(`${BASE_URL}${route}`);
> -  driver.wait({ load: "networkidle" });
> +  // domcontent (NOT networkidle): logged-in surfaces poll forever (HUD /
> +  // TanStack refetch) so networkidle never resolves under --state
> +  // (INC-20260708T0837Z-39626fcd). Hydration is covered by the ms wait below.
> +  driver.wait({ load: "domcontent" });
>    driver.wait({ ms: HYDRATION_WAIT_MS });
>    shot("01-initial");
>  
> diff --git a/scripts/qa/e2e-user-zero/flows/auth-login.ts b/scripts/qa/e2e-user-zero/flows/auth-login.ts
> index f35a206..1b1ec00 100644
> --- a/scripts/qa/e2e-user-zero/flows/auth-login.ts
> +++ b/scripts/qa/e2e-user-zero/flows/auth-login.ts
> @@ -34,7 +34,10 @@ export default function authLoginFlow(
>  
>    // Step 1 — navigate
>    driver.open(AUTH_URL);
> -  driver.wait({ load: "networkidle" });
> +  // domcontent (NOT networkidle): under --state the app redirects /auth →
> +  // /dashboard, whose HUD/query polling never goes network-idle — networkidle
> +  // times out after 30s on every logged-in surface (INC-20260708T0837Z-39626fcd).
> +  driver.wait({ load: "domcontent" });
>    driver.wait({ ms: HYDRATION_WAIT_MS });
>  
>    // Step 2 — capture landing state
> diff --git a/scripts/qa/e2e-user-zero/lib/browser-driver.ts b/scripts/qa/e2e-user-zero/lib/browser-driver.ts
> index fabc91a..7d35ce0 100644
> --- a/scripts/qa/e2e-user-zero/lib/browser-driver.ts
> +++ b/scripts/qa/e2e-user-zero/lib/browser-driver.ts
> @@ -157,12 +157,15 @@ export class BrowserDriverImpl implements BrowserDriver {
>        this.exec(["wait", opts.selector]);
>        return;
>      }
> +    // agent-browser CLI contract: load states go through `--load <state>`
> +    // (a bare arg is treated as a SELECTOR — `wait networkidle` waits for an
> +    // element named "networkidle" and times out; INC-20260708T0837Z-39626fcd).
>      if (opts.load === "networkidle") {
> -      this.exec(["wait", "networkidle"]);
> +      this.exec(["wait", "--load", "networkidle"]);
>        return;
>      }
>      if (opts.load === "domcontent") {
> -      this.exec(["wait", "domcontent"]);
> +      this.exec(["wait", "--load", "domcontentloaded"]);
>        return;
>      }
>      throw new BrowserDriverError("wait() called without ms / selector / load");
> diff --git a/scripts/qa/e2e-user-zero/runner.ts b/scripts/qa/e2e-user-zero/runner.ts
> index b9dd93a..f536e31 100644
> --- a/scripts/qa/e2e-user-zero/runner.ts
> +++ b/scripts/qa/e2e-user-zero/runner.ts
> @@ -265,8 +265,18 @@ async function mainCli(): Promise<void> {
>    } catch (e) {
>      driver.close();
>      const msg = (e as Error).message;
> -    // Auth-state expiry surfaces as a driver error mentioning auth/state/401 → exit 3.
> -    if (e instanceof BrowserDriverError && /auth|state|401|expired|unauthor/i.test(msg)) {
> +    // Spawn failure (`exited -1` = ENOENT/signal) is INFRA, never auth — the old
> +    // broad regex matched the literal "/auth" inside the page URL and turned a
> +    // missing agent-browser binary into 9 days of a synthetic "auth expirado"
> +    // incident (INC-20260708T0837Z-39626fcd).
> +    const spawnFailure = /exited -1\b/.test(msg);
> +    // Auth-state expiry: match auth-SIGNALS only (401/unauthorized/expired/state
> +    // file), never bare "auth" (present in every URL under /auth).
> +    if (
> +      !spawnFailure &&
> +      e instanceof BrowserDriverError &&
> +      /401|unauthor|expired|auth.?state/i.test(msg)
> +    ) {
>        await emitAuthExpired(runId, args.state);
>        process.stderr.write(`Estado de auth expirado/ausente: ${msg}\n`);
>        process.exit(3);
> ```

## 🤖 Claude *(17:16:16)*

<details>
<summary>💭 Thinking Process</summary>

Looking at the test files and client-side scope vocabulary updates, these don't represent actual security issues since the real enforcement happens server-side through the database allowlist and identity checks. The e2e test runner's regex change for auth-error classification is just a test adjustment.

I should verify that the server-side scope enforcement in identity.ts properly gates swarm:read to read-only operations and prevents privilege escalation, but the migration itself is just adding an allowlist entry—the security depends on whether the tool's requireScope logic is correctly configured to restrict what swarm:read can access.

</details>


## 🤖 Claude *(17:16:16)*

Let me verify the server-side scope enforcement for `swarm:read` to confirm the migration doesn't enable privilege escalation.

## 🤖 Claude *(17:16:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"swarm:read\\|swarm:run\\|swarm:write\\|ALL_SCOPES\\|requireScope\" packages/vision-mcp-core/src/ 2>/dev/null | head -40",
  "description": "Check server-side swarm scope enforcement"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> packages/vision-mcp-core/src/auth/identity.ts:14:// `swarm:read` (predictive-swarm SDD §1/§5.3, FR-PSW-002 · NFR-PSW-005) is added for the Tier 1 gate
> packages/vision-mcp-core/src/auth/identity.ts:15:// `vision.parse_sensory_gate` (Fatia 1). The write/run swarm scopes (`swarm:write`/`swarm:run`) land WITH
> packages/vision-mcp-core/src/auth/identity.ts:17:export const ALL_SCOPES = ["vision:read", "deepsearch:run", "mesh:read", "mesh:write", "swarm:read"] as const;
> packages/vision-mcp-core/src/auth/identity.ts:32:  scopes: string[]; // JWT (internal tenant) → ALL_SCOPES; PAT → its sealed subset (tool scope-gate)
> packages/vision-mcp-core/src/auth/identity.ts:78:    return { ok: true, identity: { sub, scopes: [...ALL_SCOPES] } };
> packages/vision-mcp-core/src/tools/parse-sensory-gate.ts:88: * by the HTTP handler BEFORE this runs; scope `swarm:read` is enforced there too). 0 mco — no deduct path.
> packages/vision-mcp-core/src/mcp/server.ts:62:function requireScope(scope: string): ReturnType<typeof toolError> | null {
> packages/vision-mcp-core/src/mcp/server.ts:81:      const scopeDenied = requireScope("mesh:read");
> packages/vision-mcp-core/src/mcp/server.ts:112:      const scopeDenied = requireScope("vision:read");
> packages/vision-mcp-core/src/mcp/server.ts:153:      const scopeDenied = requireScope("vision:read");
> packages/vision-mcp-core/src/mcp/server.ts:185:      const scopeDenied = requireScope("deepsearch:run");
> packages/vision-mcp-core/src/mcp/server.ts:230:      const scopeDenied = requireScope("mesh:write");
> packages/vision-mcp-core/src/mcp/server.ts:264:      const scopeDenied = requireScope("deepsearch:run");
> packages/vision-mcp-core/src/mcp/server.ts:314:      const scopeDenied = requireScope("deepsearch:run");
> packages/vision-mcp-core/src/mcp/server.ts:359:      const scopeDenied = requireScope("swarm:read");
> packages/vision-mcp-core/src/__tests__/pat.test.ts:5:import { ALL_SCOPES } from "../auth/identity.js";
> packages/vision-mcp-core/src/__tests__/pat.test.ts:20:  it("ALL_SCOPES is the closed vocabulary (internal JWT gets the full set)", () => {
> packages/vision-mcp-core/src/__tests__/pat.test.ts:21:    // `swarm:read` (predictive-swarm Fatia 1, FR-PSW-002 / NFR-PSW-005) grants the internal tenant JWT the
> packages/vision-mcp-core/src/__tests__/pat.test.ts:23:    // the Fatia 2/3 swarm migration — Fatia 1 does no DDL (SDD §9). Until then swarm:read is internal-JWT-only.
> packages/vision-mcp-core/src/__tests__/pat.test.ts:24:    expect([...ALL_SCOPES].sort()).toEqual(["deepsearch:run", "mesh:read", "mesh:write", "swarm:read", "vision:read"]);
> ```

## 🤖 Claude *(17:17:23)*

<details>
<summary>💭 Thinking Process</summary>

The server-side scope enforcement is straightforward — `swarm:read` only gates a single read-only, zero-cost sensory tool, with no privilege escalation risk. The allowlist migration simply enables external PATs to use this already-live read-only capability.

Let me walk through the remaining components: the migration itself is sound with proper constraints and no SQL injection vectors. The public URL handling preserves all the original security checks — redirect validation, DNS verification, HTTPS enforcement, port restrictions, and private IP blocking. For the bundle core, all external fetches route through the SSRF guard, scheme resolution correctly rejects HTTP and skips data/blob/javascript/about URIs while upgrading protocol-relative URLs to HTTPS. The magic-byte sniffing blocks challenge pages. The potential `</style>`/`</script>` breakout is self-XSS since tenants control both their input HTML and output landing page — not a cross-boundary vulnerability. I should reconsider the XSS threat model more carefully to determine if there's actually a meaningful attack surface here.

The real question is whether the input HTML and output landing page cross a security boundary. If a malicious tenant embeds external CSS or JS containing `</style><script>evil</script>`, the bundler inlines it verbatim, but that landing page is the tenant's own — they already have full script control over it. The bundler's lack of escaping doesn't grant new capabilities. The only concern would be if landing pages are served on a shared domain with cross-tenant cookie/session sharing, but that's a pre-existing architectural issue, not something the bundler introduces.

For the CLI tool, the input and output are operator-controlled local files, so no path traversal or injection risk. The Gemini BYOK integration sends per-user keys to the correct provider endpoint with no cross-provider leakage. The YouTube data integration uses parameterized queries via Supabase with user_id from JWT and videoId stored rather than concatenated, while the infra health logs don't carry per-tenant payloads.

The token utilities and e2e test regex are out of scope—enforcement happens server-side and tests aren't security controls. So across all eight areas, I'm not finding any newly-introduced high-confidence vulnerabilities.

Let me verify the SSRF guard one more time though. The `assertPublicHttpUrl` check looks at private IPs first, then DNS resolution, and validates the port. I need to check if there's any edge case with an IP address hostname that has no explicit port specified.

For instance, a URL like `https://169.254.169.254/` would have the hostname "169.254.169.254", which the private IP regex catches immediately. But what about encoded IP formats like `https://2130706433/` (which represents 127.0.0.1 in decimal)? The URL parser would set hostname to "2130706433", which wouldn't match the standard dotted-quad regex patterns. When the code tries to resolve "2130706433" via DNS, it would fail and return an empty list, so the guard would pass—but then the actual fetch would attempt to resolve it as a hostname, which would also fail, so there's no actual SSRF risk here.

Wait, I need to reconsider. The WHATWG URL parser for special schemes like `https:` actually does convert bare decimal IPs to their dotted-quad form. So `new URL("https://2130706433/").hostname` would return "127.0.0.1", not "2130706433". That means the private IP check would catch it after all.

The same applies to hex and octal forms like `https://0x7f.0.0.1/` or `https://0177.0.0.1/` — the parser normalizes these to "127.0.0.1" before the check runs. So there's no bypass there either.

Now I'm checking IPv6 addresses like `https://[::1]/` to see if those are handled correctly too. Let me verify Node's actual behavior with IPv6 addresses in URLs — when you parse `https://[::1]:443/`, the hostname property returns `[::1]` with the brackets included. So when `isPrivateIp` receives `[::1]`, the equality check for `::1` fails because of those brackets, creating a bypass. However, this same vulnerability exists in the canonical implementation, so it's a pre-existing issue rather than something introduced by this port. So the bracketed IPv6 literal would fail DNS resolution and pass the guard, allowing a fetch to the loopback address — but this same gap exists in the canonical implementation that I'm supposed to compare against, and since the task says not to report pre-existing concerns, this isn't a new issue introduced here. The IPv6-bracket issue is inherited from the canonical code, not newly introduced, so I won't flag it as a new finding per the instructions. Let me systematically compare the port against the canonical to catch any actual differences that could introduce gaps — checking the exported versus private function visibility, the DNS resolution logic, and other implementation details. The port's error handling with `.catch(() => [])` swallows all errors from the resolver, but since the default resolver doesn't throw `media_url_private_address`, both approaches are functionally equivalent — if a private IP is found, both throw; if resolution fails, both continue. This isn't a new vulnerability.

For my final answer: no new findings at confidence 7 or higher. I should note the inherited IPv6-bracket loopback behavior that exists in the canonical version and clarify that the bundler's CSS/JS inlining only poses a self-XSS risk, so the reviewer understands what I've considered. Now checking whether the bundler could be invoked server-side with attacker-controlled base URLs — the `baseUrl` parameter gets used to resolve relative references through `new URL()`, but `resolveRef` only returns URLs for https or protocol-relative paths, so even if `baseUrl` were something like `http://internal/`, relative refs would still resolve safely. Now I'm ready to compile the final report.

</details>


## 🤖 Claude *(17:17:23)*

I've completed a full review of all the changed files. Let me confirm my analysis of the IPv6 handling parity between the port and canonical guard.

## 🤖 Claude *(17:17:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "node -e '\nfor (const u of [\"https://2130706433/\",\"https://[::1]/\",\"https://169.254.169.254/\",\"https://0x7f000001/\"]) {\n  try { console.log(u, \"=> hostname:\", JSON.stringify(new URL(u).hostname)); }\n  catch(e){ console.log(u, \"=> parse error\"); }\n}'",
  "description": "Verify URL hostname normalization behavior"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> https://2130706433/ => hostname: "127.0.0.1"
> https://[::1]/ => hostname: "[::1]"
> https://169.254.169.254/ => hostname: "169.254.169.254"
> https://0x7f000001/ => hostname: "127.0.0.1"
> ```

## 🤖 Claude *(17:17:34)*

<details>
<summary>💭 Thinking Process</summary>

I've confirmed that the decimal/hex IPv4 normalization and IPv6 bracket handling are both pre-existing behaviors, not newly introduced issues, so there are no new findings to report at the required confidence level. Now I'm drafting the final report.

</details>


## 🤖 Claude *(17:17:55)*

I've read every security-relevant changed file in full, compared the SSRF guard port against the canonical `_shared/public-url.ts`, traced the tenant-HTML→fetch data flow in `bundle-core.ts`, and verified the server-side scope enforcement for the migration. Here are my findings.

## NO NEW FINDINGS (confidence ≥ 7)

No newly-introduced HIGH-confidence security vulnerabilities were found in the changed files.

### What I verified (and why each is clean)

**1. `supabase/migrations/20260716190000_pat_allowlist_swarm_read.sql`** — Extends the closed-vocabulary allowlist CHECK by adding only `'swarm:read'`. Structure is unchanged: still an allowlist (`scopes <@ ARRAY[...] AND array_length(scopes,1) >= 1`), static DDL (no SQLi), RLS untouched. I confirmed server-side coherence: `packages/vision-mcp-core/src/mcp/server.ts:359` gates only `parse-sensory-gate` (a 0-mco, read-only Tier 1 tool) behind `swarm:read`; `swarm:run`/`swarm:write` tools do not exist yet. No privilege escalation — the scope maps to exactly one read-only tool.

**2. `scripts/landing-bundler/public-url.ts`** — Faithful port of the canonical Deno guard. Redirect re-validation is intact (manual `redirect:"manual"`, each 3xx `Location` re-passed through `assertPublicHttpUrl`, body cancelled, `MAX_REDIRECTS=3`). https-only, port≠443 rejected, private-IP literal check, best-effort A+AAAA DNS resolve with private-IP check. I confirmed integer/hex IPv4 forms (`2130706433`, `0x7f000001`) are normalized by the WHATWG URL parser to dotted decimal and caught. The one residual gap (bracketed IPv6 loopback `[::1]` slips past `isPrivateIp` because of the brackets) is **byte-identical to and inherited from the canonical `supabase/functions/_shared/public-url.ts`** — pre-existing, not introduced by this branch, so out of scope per the instructions.

**3. `scripts/landing-bundler/bundle-core.ts`** — Every external ref from tenant HTML (`<img>/<source>/<video>/<link>/<script>/CSS url()/@import`) routes through `fetchAsset` → `fetchPublicUrl` (the SSRF guard). `resolveRef` correctly rejects `http://` (insecure_http), skips `data:/blob:/javascript:/about:`, and upgrades protocol-relative `//host` to `https:`. Magic-byte sniffing rejects HTML challenge pages (line 76 checks for embedded NUL bytes — confirmed the literal is `\x00`, matching the comment). The `</style>`/`</script>` breakout via a fetched CSS/JS body is only self-XSS: the tenant already fully controls their own input HTML and the resulting landing page, so no privilege boundary is crossed. No host/protocol control reaches internal services.

**4. `scripts/landing-bundler/cli.ts`** — Local file read/write with operator-supplied paths; no injection or traversal across a trust boundary.

**5. `supabase/functions/detect-viral-moments/index.ts`** — Gemini-only BYOK path. `aiKey = openRouterKey || groqKey || geminiKey` with mutually-exclusive `usingGemini`/`usingGroq` selection guarantees each per-user key is only ever sent to its own provider endpoint (no cross-provider key leak). Endpoints/models are hardcoded constants, not user-controlled. OpenRouter attribution headers correctly omitted for the Gemini endpoint.

**6. `supabase/functions/youtube-data/index.ts`** — Mesh observation node + delete telemetry. Inserts run via the Supabase client (parameterized — no SQLi from the user-supplied `videoId`), scoped with `user_id: user.id` from the verified JWT. The `infra_health_logs` delete event deliberately carries **no per-tenant payload** (videoId lives only in the RLS-scoped mesh node), correctly avoiding data exposure in the global-read table.

**7. `src/hooks/useMcpTokens.ts` / `scripts/qa/mint-vision-pat.ts`** — Add `'swarm:read'` to client-side/QA scope vocabulary lists only. These are not the enforcement boundary (DB allowlist CHECK + server `requireScope` enforce), so no security impact.

**8. `scripts/qa/e2e-user-zero/runner.ts` + related** — Test-harness wait-state and auth-error-classification regex changes. These are QA scripts (excluded), and the regex is a diagnostic classifier, not a security control.

All changes are self-contained and do not introduce SQL injection, command injection, auth/authorization bypass, privilege escalation, host/protocol-controllable SSRF, secret leakage, or code execution.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-16 - agent-abfa2108037f4d175]]
> * **Próxima Sessão**: [[2026-07-16 - agent-ac0b910b2aaa0f12e]]
%% --- TIMELINE END --- %%

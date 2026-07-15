# Session agent-acdfcf8db5ac6fd52
**Date:** 2026-07-15 | **Session ID:** `agent-acdfcf8db5ac6fd52`

---

## 👤 User *(19:53:28)*

Verificação de segurança FOCADA e ADVERSARIAL do fix de SSRF da Fatia 1 do predictive-swarm (repo /home/gcrUX/htdocs/constellation-orchestra). Seu único trabalho: tentar QUEBRAR o fix. Seja cético (>80% confiança p/ reportar bypass real).

CONTEXTO: o crítico achou que `ffmpeg -i <asset_url>` (em packages/vision-mcp-core/src/tier1/loudness.ts, defaultRunner) segue redirects 302 → SSRF ao IMDS (169.254.169.254). O fix aplicado: em packages/vision-mcp-core/src/tools/parse-sensory-gate.ts, antes de chamar loudnessGate, o asset_url passa por assertSafeImageUrl (https + bloqueia host privado/loopback/link-local) E por assertTenantSupabaseOrigin (host-pin: origin === SUPABASE_ORIGIN do container + pathname começa com /storage/).

LEIA: packages/vision-mcp-core/src/tools/parse-sensory-gate.ts (o guard + o helper assertTenantSupabaseOrigin + SUPABASE_ORIGIN), packages/vision-mcp-core/src/tools/describe-image.ts (assertSafeImageUrl), packages/vision-mcp-core/src/tier1/loudness.ts (defaultRunner, ffmpegLoudnormArgs).

TENTE BYPASSAR o host-pin (responda SIM/NÃO com raciocínio concreto p/ cada):
1. userinfo trick: `https://169.254.169.254@<supabase-host>/storage/...` — o que `new URL().origin` retorna? bypassa?
2. subdomínio: `https://<supabase-host>.evil.com/storage/...` — passa o pin?
3. path trick: `https://<supabase-host>/storage/../@evil` ou `//evil` — o pin de pathname startsWith('/storage/') é burlável?
4. o asset_url chega ao ffmpeg SÓ depois do pin? há algum caminho (loudnessGate chamado direto, ou outro fetch) que pule o guard?
5. redirect: mesmo pinado ao host Supabase, o Supabase Storage pode emitir um 302 para host interno? (o storage devolve o objeto 200, não redireciona — confirmar o raciocínio)
6. command injection: ffmpegLoudnormArgs usa execFile com array (sem shell)? o asset_url pode injetar flags do ffmpeg (ex.: começar com '-')? (o pin ao host Supabase já limita, mas confirmar)
7. SUPABASE_ORIGIN vazio (env ausente) → o helper faz fail-closed (rejeita tudo) ou fail-open (aceita)?

Veredito final: o fix FECHA o SSRF de redirect, ou há um bypass concreto? Liste qualquer bypass real com o payload exato. Se estiver sólido, diga "SSRF FECHADO" com o porquê de cada vetor acima estar coberto.

## 🤖 Claude *(19:53:31)*

<details>
<summary>💭 Thinking Process</summary>

I'll start by reading through the three files mentioned in the task.

</details>


## 🤖 Claude *(19:53:31)*

I'll read the three files central to this SSRF fix verification.

## 🤖 Claude *(19:53:32)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/packages/vision-mcp-core/src/tools/parse-sensory-gate.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// vision-mcp-core tools/parse-sensory-gate.ts — FR-PSW-002/004/005/012 · SDD §2.1 (Tier 1 path).
> 2	//
> 3	// vision.parse_sensory_gate — the 2-layer sensory-predictive gate. THIS FILE is the **Fatia 1** slice:
> 4	// the PURE Tier 1 objective gate ONLY (SDD §9 Fatia 1 · line ~427). It is 0 mco, deterministic, and does
> 5	// NO deduct (NFR-PSW-002 — Tier 1 is free by construction). Pipeline (SDD §3 Use Case A, Tier 1 legs):
> 6	//
> 7	//   1. SSRF-guard `asset_url`               (assertSafeImageUrl — https-only + private/loopback block)
> 8	//   2. loudnessGate(asset_url)              (ffmpeg loudnorm IL/LRA/TP — FR-PSW-004)  → Finding[]
> 9	//   3. contrastGate(layer color pair)       (WCAG 2.x certifies + APCA Lc scores — FR-PSW-005) → Finding[]
> 10	//   4. composePerceptionDrift(dimensions)   (PROXY score, drift_label:'proxy' — anti-Goodhart)
> 11	//   5. verdictFor(findings)                 (GO iff 0×P0 AND 0×P1 — FR-PSW-012, herdado report-renderer:58)
> 12	//
> 13	// Tier 2 foveal VLM (semantic escalation on salient regions, `question` → describeImage; FR-PSW-007) is
> 14	// the **Fatia 2** hook — kept as a documented, COMMENTED stub below. NOT implemented here (SDD §9): it
> 15	// depends on the saliency engine (OTD-PSW-001) + selective escalation + deduct-on-entry, none of which
> 16	// exist in Fatia 1. `tier_reached` is therefore always 1 and `escalated` always false here.
> 17	//
> 18	// ─── CONTRAST COLOR SOURCE (Lei 1 — SSOT honesty) ───────────────────────────────────────────────────
> 19	// FR-PSW-005 / SDD §2.2 fence contrastGate to "2 colors (fg/bg) that come ONLY from the tenant's own
> 20	// layer colors (channel_profiles)" and EXPLICITLY exclude extracting colors from the rendered `asset_url`
> 21	// (that needs text-region detection — non-deterministic, non-0-mco → OTD-PSW-013 → Fatia 2). Material
> 22	// finding while wiring Fatia 1: `channel_profiles` carries NO color/layer-color storage (it holds
> 23	// video/image/text/cadence specs, no per-tenant colors), and no other per-tenant layer-color store
> 24	// exists. Inventing a DB column/fetch would violate Lei 1. So the only Lei-1-honest source of the 2
> 25	// colors in Fatia 1 is the tenant DECLARING their own layer pairs — accepted via the optional
> 26	// `layer_colors` input. When absent, the contrast dimension is simply NOT measured (excluded from the
> 27	// drift mean — never scored as "clean"; see composePerceptionDrift). The server-side resolution from a
> 28	// future per-tenant layer-color store (or the OTD-PSW-013 rendered-asset extraction) is the Fatia 2 seam.
> 29	//
> 30	// Convention (CLAUDE.md): code/logic/vars/logs in ENGLISH; user-facing copy (Finding text, validation
> 31	// messages) in PT-BR. Determinism (NFR-PSW-010): same input → same Finding[] (the injectable `now`/ffmpeg
> 32	// runner are test seams; the finding SET — ids/severities/copy — is a pure function of the inputs).
> 33	
> 34	import { assertSafeImageUrl } from "./describe-image.js";
> 35	import { loudnessGate, type Finding, type FfmpegRunner } from "../tier1/loudness.js";
> 36	import { contrastGate, ContrastInputError, type ContrastTextKind } from "../tier1/contrast.js";
> 37	import { verdictFor, composePerceptionDrift, type Verdict, type DriftDimension } from "../swarm/verdict.js";
> 38	import { logHealth } from "../infra/telemetry.js";
> 39	
> 40	const SERVICE = "predictive-swarm";
> 41	
> 42	// A tenant-declared layer color pair for the contrast gate (see CONTRAST COLOR SOURCE above).
> 43	export interface LayerColorPair {
> 44	  foreground: string; // tenant layer text color (hex / rgb())
> 45	  background: string; // tenant layer background color
> 46	  text_kind?: ContrastTextKind; // WCAG size class — default 'normal' (strictest) in contrastGate
> 47	  label?: string; // optional human tag echoed into the Finding copy (never affects the math)
> 48	}
> 49	
> 50	export interface ParseSensoryGateInput {
> 51	  asset_url: string; // https signed, owner-scoped (SSRF-guarded)
> 52	  question?: string; // Tier 2 foveal semantic prompt — accepted now, consumed in Fatia 2 (hook below)
> 53	  tier?: 1; // Fatia 1 is Tier 1 only; `2` is a Fatia 2 capability (schema rejects it until then)
> 54	  layer_colors?: LayerColorPair[]; // tenant-declared layer pairs for the contrast gate (Lei 1 note above)
> 55	}
> 56	
> 57	// Test/impurity seams — NOT part of the MCP input schema (server handler never passes these).
> 58	export interface ParseSensoryGateOptions {
> 59	  now?: () => string; // injectable clock for deterministic `detected_at` (default: wall clock)
> 60	  loudnessRunner?: FfmpegRunner; // injectable ffmpeg runner (default: spawn host ffmpeg)
> 61	}
> 62	
> 63	export interface ParseSensoryGateResult {
> 64	  findings: Finding[];
> 65	  perception_drift: number; // PROXY/prediction — ALWAYS labelled (never "real quality")
> 66	  drift_label: "proxy"; // mandatory anti-Goodhart label (NFR-PSW-010 / FM-PSW-01)
> 67	  dimensions: Partial<Record<DriftDimension, number>>; // only MEASURED dimensions (loudness/contrast in Fatia 1)
> 68	  tier_reached: 1; // Fatia 1 never escalates → always 1
> 69	  escalated: boolean; // Tier 2 foveal invoked? — always false in Fatia 1
> 70	  verdict: Verdict; // GO iff 0×P0 AND 0×P1
> 71	  human_review_required?: boolean; // set when an objective signal could not be measured (fail-closed escalation)
> 72	}
> 73	
> 74	// Structured tool error. `validation_failed` carries a PT-BR field message (FRD §4.4 body contract).
> 75	export class ParseSensoryGateError extends Error {
> 76	  code: string;
> 77	  field?: string;
> 78	  constructor(code: string, opts?: { field?: string; message?: string }) {
> 79	    super(opts?.message ?? code);
> 80	    this.code = code;
> 81	    this.field = opts?.field;
> 82	    this.name = "ParseSensoryGateError";
> 83	  }
> 84	}
> 85	
> 86	/**
> 87	 * Run the Tier 1 sensory gate over an asset. `sub` is the ES256-verified tenant id (identity is resolved
> 88	 * by the HTTP handler BEFORE this runs; scope `swarm:read` is enforced there too). 0 mco — no deduct path.
> 89	 */
> 90	// HOST-PIN origin (SSRF root-cause fix): the Tier 1 gate reads the tenant's OWN creative_asset — a signed,
> 91	// owner-scoped Supabase Storage URL (SDD contract). Pinning asset_url to this origin closes the
> 92	// ffmpeg-follows-redirect SSRF at its root. Resolved once at module load from the container's Supabase env.
> 93	const SUPABASE_ORIGIN = (() => {
> 94	  const raw = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL ?? "";
> 95	  try {
> 96	    return raw ? new URL(raw).origin : "";
> 97	  } catch {
> 98	    return "";
> 99	  }
> 100	})();
> 101	
> 102	/** Throws unless `raw` is on the tenant's own Supabase Storage origin. Fail-closed: if the container has no
> 103	 *  Supabase origin configured, the pin cannot be proven, so the URL is rejected (never trusted blindly). */
> 104	function assertTenantSupabaseOrigin(raw: string): void {
> 105	  const u = new URL(raw); // already parsed+validated by assertSafeImageUrl (https, non-private host)
> 106	  if (!SUPABASE_ORIGIN || u.origin !== SUPABASE_ORIGIN || !u.pathname.startsWith("/storage/")) {
> 107	    throw new Error("asset_url_not_tenant_storage");
> 108	  }
> 109	}
> 110	
> 111	export async function parseSensoryGate(
> 112	  input: ParseSensoryGateInput,
> 113	  sub: string,
> 114	  opts: ParseSensoryGateOptions = {},
> 115	): Promise<ParseSensoryGateResult> {
> 116	  const now = opts.now ?? (() => new Date().toISOString());
> 117	
> 118	  // 1) SSRF guard BEFORE any work (NFR-PSW-006). TWO layers, because ffmpeg (loudness) follows redirects
> 119	  //    ITSELF — a first-hop-only check would be defeated by a public host that 302→169.254.169.254 (IMDS),
> 120	  //    the exact `fetchPublicUrl` lesson of this codebase (reference_ssrf_guard_survives_redirect /
> 121	  //    _shared/public-url.ts):
> 122	  //      (a) assertSafeImageUrl — https-only + private/loopback/link-local host block; AND
> 123	  //      (b) assertTenantSupabaseOrigin — HOST-PIN to the tenant's own Supabase Storage origin. The SDD
> 124	  //          contract is a signed, owner-scoped Supabase URL; ENFORCING the origin turns "Supabase does not
> 125	  //          302 to internal hosts" from an assumption into an invariant, so no caller-controlled host ever
> 126	  //          reaches ffmpeg. An invalid/blocked/off-origin URL → validation_failed (422 semantics).
> 127	  try {
> 128	    assertSafeImageUrl(input.asset_url);
> 129	    assertTenantSupabaseOrigin(input.asset_url);
> 130	  } catch {
> 131	    throw new ParseSensoryGateError("validation_failed", {
> 132	      field: "asset_url",
> 133	      message: "URL do criativo inválida — envie uma URL assinada do storage do seu próprio projeto.",
> 134	    });
> 135	  }
> 136	
> 137	  // 2) Tier 1 objective gates — 0 mco, deterministic. A dimension key is PRESENT only when it was actually
> 138	  //    measured (empty array ⇒ measured-and-clean; absent ⇒ not measured, excluded from the drift mean —
> 139	  //    silence is never scored as perfection). See composePerceptionDrift.
> 140	  const perDimension: Partial<Record<DriftDimension, Finding[]>> = {};
> 141	  const findings: Finding[] = [];
> 142	  let humanReviewRequired = false;
> 143	
> 144	  // 2a) Loudness gate (FR-PSW-004) over the asset audio. Empty ⇒ on-target OR no audio (silent image).
> 145	  try {
> 146	    const loudnessFindings = await loudnessGate(input.asset_url, { now }, opts.loudnessRunner);
> 147	    perDimension.loudness = loudnessFindings;
> 148	    findings.push(...loudnessFindings);
> 149	  } catch (e) {
> 150	    // fail-closed (NFR-PSW-012): a probe failure must NOT be scored as a clean pass. Leave `loudness`
> 151	    // UNMEASURED (absent from perDimension → excluded from the mean) and escalate to a human. No fabricated
> 152	    // Finding: the BoK defines no probe-failure Finding, so inventing severity/copy would violate Lei 1.
> 153	    const code = (e as { code?: string })?.code ?? "loudness_probe_failed";
> 154	    logHealth("degraded", "tool_error", { tool: "parse_sensory_gate", code, tier: 1 }, SERVICE);
> 155	    humanReviewRequired = true;
> 156	  }
> 157	
> 158	  // 2b) Contrast gate (FR-PSW-005) over the tenant's DECLARED layer color pairs (Lei 1 note in header).
> 159	  //     When none are declared, contrast is not measured this run (Fatia 1 does not extract from the
> 160	  //     rendered asset — OTD-PSW-013 → Fatia 2). contrastGate is PURE (no clock) → the tool stamps
> 161	  //     `detected_at` so the emitted Finding matches the SSOT shape (finding-schema.ts).
> 162	  const layerColors = input.layer_colors ?? [];
> 163	  if (layerColors.length > 0) {
> 164	    const contrastFindings: Finding[] = [];
> 165	    const stampedAt = now();
> 166	    for (const pair of layerColors) {
> 167	      let result;
> 168	      try {
> 169	        result = contrastGate(pair);
> 170	      } catch (e) {
> 171	        if (e instanceof ContrastInputError) {
> 172	          throw new ParseSensoryGateError("validation_failed", {
> 173	            field: "layer_colors",
> 174	            message: "Cor de camada inválida — use hex (#rrggbb) ou rgb() das cores do seu projeto.",
> 175	          });
> 176	        }
> 177	        throw e;
> 178	      }
> 179	      for (const f of result.findings) contrastFindings.push({ ...f, detected_at: stampedAt });
> 180	    }
> 181	    perDimension.contrast = contrastFindings;
> 182	    findings.push(...contrastFindings);
> 183	  }
> 184	
> 185	  // ─── Tier 2 foveal escalation (FR-PSW-002/007) — FATIA 2 HOOK (deferred, do NOT implement here) ──────
> 186	  // In Fatia 2, when the saliency engine (OTD-PSW-001) flags conspicuous regions OR the caller forces
> 187	  // `tier === 2`, describeImage({ image_url: asset_url, question }, sub) is invoked ONLY on those foveal
> 188	  // regions with deduct-on-entry (402 before the leg). On escalation: escalated = true, tier_reached = 2,
> 189	  // and `confidence:'low'` from the VLM sets human_review_required (FR-PSW-013). Fail-closed: VLM
> 190	  // unavailable → fall back to these Tier 1 objective signals (NFR-PSW-012). Kept commented until the
> 191	  // saliency + selective-escalation surfaces land (SDD §9 Fatia 2).
> 192	  //   if (input.tier === 2 || salientRegions.length > 0) { ... escalate ... }
> 193	
> 194	  // 3) Compose the PROXY drift + GO/NO-GO verdict from the measured objective dimensions.
> 195	  const drift = composePerceptionDrift(perDimension);
> 196	  const verdict = verdictFor(findings);
> 197	
> 198	  logHealth(
> 199	    "healthy",
> 200	    "tool_ok",
> 201	    {
> 202	      tool: "parse_sensory_gate",
> 203	      tier: 1,
> 204	      escalated: false,
> 205	      drift: drift.perception_drift,
> 206	      dimensions: Object.keys(drift.dimensions).length,
> 207	    },
> 208	    SERVICE,
> 209	  );
> 210	
> 211	  const out: ParseSensoryGateResult = {
> 212	    findings,
> 213	    perception_drift: drift.perception_drift,
> 214	    drift_label: "proxy",
> 215	    dimensions: drift.dimensions,
> 216	    tier_reached: 1,
> 217	    escalated: false,
> 218	    verdict,
> 219	  };
> 220	  if (humanReviewRequired) out.human_review_required = true;
> 221	  return out;
> 222	}
> 223	
> ```

## 🤖 Claude *(19:53:33)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/packages/vision-mcp-core/src/tools/describe-image.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// vision-mcp-core tools/describe-image.ts — FR-VM-018 (vision.describe_image, 2 mco). First Fatia 2
> 2	// billable tool. Pipeline (SOP vision-mcp-billing-credential-resolution.md): SSRF-guard the URL →
> 3	// duty-of-care red-line (assistive) → resolve provider key (BYOK free / platform charged / 402) →
> 4	// cost decision → deduct-on-entry (402 before leg) → VLM leg → refund-on-failure → structured result.
> 5	
> 6	import { resolveProviderKey } from "../auth/credentials.js";
> 7	import { costFor, deductOnEntry, refund, ProviderNotConfiguredError } from "../infra/billing.js";
> 8	import { redlineCheck, assistivePromptSuffix } from "../safety/duty-of-care.js";
> 9	import { logHealth } from "../infra/telemetry.js";
> 10	
> 11	// Platform default VLM (cheap, vision-capable). Cost SOP: Gemini Flash ~$0.0004/img → 2 mco @4×-floor.
> 12	const VISION_MODEL = process.env.VISION_VLM_MODEL ?? "google/gemini-2.5-flash";
> 13	
> 14	export interface DescribeImageInput {
> 15	  image_url: string;
> 16	  question?: string;
> 17	  assistive?: boolean;
> 18	}
> 19	export interface DescribeImageResult {
> 20	  description: string;
> 21	  confidence: "high" | "medium" | "low";
> 22	  cost_mco: number;
> 23	  human_review_required?: boolean;
> 24	}
> 25	
> 26	export class RedlineRefusalError extends Error {
> 27	  code = "assistive_redline_refusal";
> 28	  constructor(public domain?: string) {
> 29	    super("assistive_redline_refusal");
> 30	  }
> 31	}
> 32	export class ImageUrlError extends Error {
> 33	  code: string;
> 34	  constructor(code: string) {
> 35	    super(code);
> 36	    this.code = code;
> 37	  }
> 38	}
> 39	
> 40	// SSRF guard: https only + reject private/loopback/link-local hosts (FR-VM-018 "https only; host allowlist").
> 41	export function assertSafeImageUrl(raw: string): URL {
> 42	  let u: URL;
> 43	  try {
> 44	    u = new URL(raw);
> 45	  } catch {
> 46	    throw new ImageUrlError("invalid_image_url");
> 47	  }
> 48	  if (u.protocol !== "https:") throw new ImageUrlError("image_url_must_be_https");
> 49	  const h = u.hostname.toLowerCase();
> 50	  const blocked =
> 51	    h === "localhost" ||
> 52	    h.endsWith(".local") ||
> 53	    h === "0.0.0.0" ||
> 54	    h === "::1" ||
> 55	    h.startsWith("[") || // raw IPv6 literal — refuse rather than parse-classify
> 56	    /^127\./.test(h) ||
> 57	    /^10\./.test(h) ||
> 58	    /^192\.168\./.test(h) ||
> 59	    /^169\.254\./.test(h) ||
> 60	    /^172\.(1[6-9]|2\d|3[01])\./.test(h);
> 61	  if (blocked) throw new ImageUrlError("image_url_host_blocked");
> 62	  return u;
> 63	}
> 64	
> 65	export async function describeImage(input: DescribeImageInput, sub: string): Promise<DescribeImageResult> {
> 66	  // 1) SSRF guard (before any cost/leg).
> 67	  assertSafeImageUrl(input.image_url);
> 68	
> 69	  // 2) assistive duty-of-care red-line on the question — refuse free, no charge (FR-VM-014).
> 70	  if (input.assistive) {
> 71	    const v = redlineCheck(input.question);
> 72	    if (v.refuse) {
> 73	      logHealth("degraded", "assistive_redline_refusal", { domain: v.domain }, "vision-mcp");
> 74	      throw new RedlineRefusalError(v.domain);
> 75	    }
> 76	  }
> 77	
> 78	  // 3) resolve provider key (BYOK free / platform charged / 402 not_configured).
> 79	  const resolved = await resolveProviderKey(sub, "openrouter");
> 80	  if (!resolved) throw new ProviderNotConfiguredError("openrouter");
> 81	
> 82	  // 4) cost decision + deduct on entry (insufficient → throws BEFORE the provider leg).
> 83	  const cost = costFor("vision.describe_image", sub, resolved.isUserCustomKey);
> 84	  await deductOnEntry(sub, cost, "vision.describe_image", { model: VISION_MODEL, assistive: !!input.assistive });
> 85	
> 86	  // 5) provider leg — refund on ANY failure past the deduct.
> 87	  try {
> 88	    const res = await fetch("https://openrouter.ai/api/v1/chat/completions", {
> 89	      method: "POST",
> 90	      headers: { Authorization: `Bearer ${resolved.key}`, "Content-Type": "application/json" },
> 91	      body: JSON.stringify({
> 92	        model: VISION_MODEL,
> 93	        max_tokens: 700,
> 94	        messages: [
> 95	          {
> 96	            role: "user",
> 97	            content: [
> 98	              { type: "text", text: buildPrompt(input) },
> 99	              { type: "image_url", image_url: { url: input.image_url } },
> 100	            ],
> 101	          },
> 102	        ],
> 103	      }),
> 104	    });
> 105	    if (!res.ok) {
> 106	      throw new Error(`vlm_http_${res.status}:${(await res.text()).slice(0, 160)}`);
> 107	    }
> 108	    const data = (await res.json()) as { choices?: Array<{ message?: { content?: string } }> };
> 109	    const content = data?.choices?.[0]?.message?.content ?? "";
> 110	    const { description, confidence } = parseVlm(content);
> 111	    logHealth("healthy", "tool_ok", { tool: "describe_image", cost, byok: resolved.isUserCustomKey });
> 112	    const out: DescribeImageResult = { description, confidence, cost_mco: cost };
> 113	    if (input.assistive) out.human_review_required = confidence === "low";
> 114	    return out;
> 115	  } catch (e) {
> 116	    await refund(sub, cost, "describe_image_failed");
> 117	    throw e;
> 118	  }
> 119	}
> 120	
> 121	function buildPrompt(input: DescribeImageInput): string {
> 122	  const base = input.question
> 123	    ? `Descreva a imagem para responder: "${input.question}".`
> 124	    : "Descreva a imagem de forma objetiva, completa e fiel.";
> 125	  const assistive = input.assistive ? assistivePromptSuffix() : "";
> 126	  return `${base}${assistive} Responda em PT-BR. Retorne SOMENTE um objeto JSON: {"description": string, "confidence": "high"|"medium"|"low"}.`;
> 127	}
> 128	
> 129	// EXPORTED for unit testing the parse robustness without a live VLM.
> 130	export function parseVlm(content: string): { description: string; confidence: "high" | "medium" | "low" } {
> 131	  const m = content.match(/\{[\s\S]*\}/);
> 132	  if (m) {
> 133	    try {
> 134	      const j = JSON.parse(m[0]) as { description?: unknown; confidence?: unknown };
> 135	      const conf = j.confidence === "high" || j.confidence === "low" ? j.confidence : "medium";
> 136	      if (typeof j.description === "string" && j.description.trim()) {
> 137	        return { description: j.description.trim(), confidence: conf };
> 138	      }
> 139	    } catch {
> 140	      /* fall through to raw text */
> 141	    }
> 142	  }
> 143	  return { description: content.trim() || "(sem descrição)", confidence: "medium" };
> 144	}
> 145	
> ```

## 🤖 Claude *(19:53:33)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/packages/vision-mcp-core/src/tier1/loudness.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// vision-mcp-core tier1/loudness.ts — FR-PSW-004 · SDD §2.2 · OTD-PSW-006.
> 2	//
> 3	// Tier 1 loudness gate: NET-NEW, 0 mco, deterministic, model-free. Runs
> 4	// `ffmpeg loudnorm` (ITU-R BS.1770 / EBU R128) over the audio stream of an
> 5	// asset, parses integrated loudness (IL) / loudness range (LRA) / true peak
> 6	// (TP), and returns a Finding[] when the audio is off the social target
> 7	// (~-14 LUFS). No VLM, no network beyond ffmpeg's own read of the (already
> 8	// SSRF-validated) signed URL, no billing.
> 9	//
> 10	// ─── CONTAINER DEPENDENCY ────────────────────────────────────────────────
> 11	// Requires `ffmpeg` on PATH INSIDE the mcorch_vision_mcp container. It is NOT
> 12	// present by default — the HyperFrames ffmpeg runs on the HOST (systemd), a
> 13	// separate process, NOT in this container. The container Dockerfile installs it
> 14	// explicitly (`apk add --no-cache tini ffmpeg`). SDD §6 mandates ffmpeg as the
> 15	// Tier 1 foothold. If ffmpeg is absent, `loudnessGate` throws
> 16	// LoudnessError('loudness_probe_failed') — fail-closed (never a clean pass).
> 17	//
> 18	// ─── SSRF ────────────────────────────────────────────────────────────────
> 19	// `asset_url` MUST be validated upstream by the tool layer (assertSafeImageUrl
> 20	// / fetchPublicUrl in parse-sensory-gate, NFR-PSW-006) BEFORE reaching here.
> 21	// This engine trusts its input URL by contract; it performs no guard of its own.
> 22	//
> 23	// ─── DETERMINISM (NFR — "mesmo input → mesmo Finding[]") ──────────────────
> 24	// `parseLoudnormJson` and `findingsForLoudness` are pure: the finding set,
> 25	// severities, issue types and suggested fixes are a pure function of the
> 26	// ffmpeg measures + options. The only time-varying field is `detected_at`,
> 27	// which is derived from an injectable `now()` clock (default: wall clock) so
> 28	// tests can pin it and prove byte-identical output.
> 29	//
> 30	// Convention (CLAUDE.md): code/logic/vars/logs in ENGLISH; user-facing
> 31	// Finding copy (title/description/suggested_fix/repro_steps) in PT-BR.
> 32	
> 33	import { execFile } from "node:child_process";
> 34	
> 35	// ─── Finding shape ────────────────────────────────────────────────────────
> 36	// Mirrors scripts/qa/e2e-user-zero/lib/finding-schema.ts:8/69 (Severity /
> 37	// IssueType / Finding). The container is a separate package and cannot import
> 38	// across the repo tree under NodeNext; this local mirror keeps the engine
> 39	// self-contained. If psw1:foundation lands a shared in-container mirror
> 40	// (e.g. ./finding.js), swap these three declarations for the import.
> 41	export type Severity = "P0" | "P1" | "P2" | "P3";
> 42	export type IssueType = "bug" | "ux" | "perf" | "accessibility" | "security" | "regression";
> 43	
> 44	export interface Finding {
> 45	  id: string;
> 46	  flow: string;
> 47	  severity: Severity;
> 48	  issue_type: IssueType;
> 49	  title: string;
> 50	  description: string;
> 51	  repro_steps: string[];
> 52	  evidence_paths: {
> 53	    screenshot?: string;
> 54	    har_snippet?: string;
> 55	    console_snippet?: string;
> 56	    snapshot_ref?: string;
> 57	  };
> 58	  affected_module?: { node_id?: string; node_name?: string; path?: string };
> 59	  suggested_fix?: string;
> 60	  detected_at: string;
> 61	}
> 62	
> 63	// ─── Constants (documented, standards-backed — no invented numbers) ────────
> 64	// Social integrated-loudness target. FR-PSW-004 / SDD §2.2: "~-14 LUFS social".
> 65	// -14 LUFS is the normalization target used by YouTube / Spotify / Instagram.
> 66	export const SOCIAL_TARGET_LUFS = -14;
> 67	// Symmetric window treated as on-target. Anything beyond ±1 LU is audibly off
> 68	// after platform normalization; keeps GO clean for well-mastered audio.
> 69	export const LUFS_TOLERANCE = 1.0;
> 70	// EBU R128 s1 / streaming ceiling. True peak above -1 dBTP risks inter-sample
> 71	// clipping / distortion after lossy re-encode.
> 72	export const MAX_TRUE_PEAK_DBTP = -1.0;
> 73	
> 74	export const LOUDNESS_FLOW = "predictive-swarm/loudness";
> 75	
> 76	// ─── Types ─────────────────────────────────────────────────────────────────
> 77	/** Parsed `loudnorm print_format=json` analysis pass (input_* fields). */
> 78	export interface LoudnessMeasures {
> 79	  integrated_lufs: number; // input_i  — may be -Infinity for silence
> 80	  loudness_range: number; // input_lra
> 81	  true_peak_dbtp: number; // input_tp — may be -Infinity for silence
> 82	  threshold_lufs: number; // input_thresh (evidence only; NaN if absent)
> 83	}
> 84	
> 85	export interface LoudnessGateOptions {
> 86	  targetLufs?: number;
> 87	  toleranceLufs?: number;
> 88	  maxTruePeakDbtp?: number;
> 89	  /** Injectable clock for deterministic `detected_at` (default: wall clock). */
> 90	  now?: () => string;
> 91	  flow?: string;
> 92	}
> 93	
> 94	/** Result of one ffmpeg invocation. */
> 95	export interface FfmpegRun {
> 96	  stdout: string;
> 97	  stderr: string;
> 98	  code: number;
> 99	}
> 100	/** Injectable ffmpeg runner (default spawns host ffmpeg). Tests mock this. */
> 101	export type FfmpegRunner = (assetUrl: string) => Promise<FfmpegRun>;
> 102	
> 103	export class LoudnessError extends Error {
> 104	  code: string;
> 105	  constructor(code: string, message?: string) {
> 106	    super(message ?? code);
> 107	    this.code = code;
> 108	    this.name = "LoudnessError";
> 109	  }
> 110	}
> 111	
> 112	// ─── ffmpeg invocation ──────────────────────────────────────────────────────
> 113	// Two-pass loudnorm is only needed to APPLY normalization; the analysis JSON we
> 114	// need is emitted by a single measuring pass to a null sink. `-vn` drops video
> 115	// so loudnorm sees audio only. JSON is printed to STDERR by ffmpeg.
> 116	export function ffmpegLoudnormArgs(assetUrl: string): string[] {
> 117	  return [
> 118	    "-hide_banner",
> 119	    "-nostats",
> 120	    "-i",
> 121	    assetUrl,
> 122	    "-vn",
> 123	    "-af",
> 124	    "loudnorm=print_format=json",
> 125	    "-f",
> 126	    "null",
> 127	    "-",
> 128	  ];
> 129	}
> 130	
> 131	const defaultRunner: FfmpegRunner = (assetUrl) =>
> 132	  new Promise((resolve) => {
> 133	    execFile(
> 134	      "ffmpeg",
> 135	      ffmpegLoudnormArgs(assetUrl),
> 136	      { maxBuffer: 8 * 1024 * 1024, timeout: 60_000 },
> 137	      (err, stdout, stderr) => {
> 138	        const code =
> 139	          err && typeof (err as { code?: unknown }).code === "number"
> 140	            ? ((err as { code: number }).code as number)
> 141	            : err
> 142	              ? 1
> 143	              : 0;
> 144	        resolve({ stdout: stdout ?? "", stderr: stderr ?? "", code });
> 145	      },
> 146	    );
> 147	  });
> 148	
> 149	// ─── Pure parsing ────────────────────────────────────────────────────────────
> 150	/** ffmpeg emits "-inf"/"inf" for silent input; JSON.parse-friendly Number() can't. */
> 151	function toNumber(raw: unknown): number {
> 152	  const s = String(raw).trim().toLowerCase();
> 153	  if (s === "-inf") return -Infinity;
> 154	  if (s === "inf" || s === "+inf") return Infinity;
> 155	  return Number(s);
> 156	}
> 157	
> 158	/**
> 159	 * Extract the loudnorm analysis object from ffmpeg stderr. Returns null when no
> 160	 * analysis block is present (e.g. asset has no audio stream — see loudnessGate).
> 161	 */
> 162	export function parseLoudnormJson(stderr: string): LoudnessMeasures | null {
> 163	  // The loudnorm block is the JSON object containing "input_i". Match it
> 164	  // specifically (there may be other braces in the ffmpeg banner/logs).
> 165	  const match = stderr.match(/\{[^{}]*"input_i"[^{}]*\}/);
> 166	  if (!match) return null;
> 167	  let raw: Record<string, unknown>;
> 168	  try {
> 169	    raw = JSON.parse(match[0]) as Record<string, unknown>;
> 170	  } catch {
> 171	    return null;
> 172	  }
> 173	  const integrated_lufs = toNumber(raw.input_i);
> 174	  const loudness_range = toNumber(raw.input_lra);
> 175	  const true_peak_dbtp = toNumber(raw.input_tp);
> 176	  const threshold_lufs = "input_thresh" in raw ? toNumber(raw.input_thresh) : NaN;
> 177	  // input_i / input_tp may legitimately be -Infinity (silence); reject only NaN,
> 178	  // which signals a malformed / partial JSON we should not gate on.
> 179	  if (Number.isNaN(integrated_lufs) || Number.isNaN(true_peak_dbtp)) return null;
> 180	  return { integrated_lufs, loudness_range, true_peak_dbtp, threshold_lufs };
> 181	}
> 182	
> 183	/** ffmpeg messages that mean "there is simply no audio to gate" (not a failure). */
> 184	export function hasNoAudioStream(stderr: string): boolean {
> 185	  return /does not contain any stream|matches no streams|Output file .*does not contain|Audio: none/i.test(
> 186	    stderr,
> 187	  );
> 188	}
> 189	
> 190	const round1 = (n: number): string => (Number.isFinite(n) ? n.toFixed(1) : String(n));
> 191	
> 192	// ─── Pure findings derivation ────────────────────────────────────────────────
> 193	/**
> 194	 * Derive Finding[] from loudness measures. PURE: same measures + options →
> 195	 * identical findings (except `detected_at`, which comes from `now()`).
> 196	 *
> 197	 * Emits ≥P1 when the audio is off the social target (FR-PSW-004: "Finding
> 198	 * severity ≥P1 quando fora do alvo"). Two independent checks:
> 199	 *   1. Integrated loudness outside the ±tolerance window (too loud / too quiet).
> 200	 *   2. True peak above the EBU R128 ceiling (inter-sample clipping risk).
> 201	 * Silent / immeasurable audio (IL = -Infinity) yields NO finding — there is
> 202	 * nothing to gate; the caller (parse-sensory-gate) may surface that separately.
> 203	 *
> 204	 * NOTE (Lei 1): FR-PSW-004 specifies only "≥P1" for out-of-target. No P0
> 205	 * escalation band is defined by the SDD/FRD, so both checks emit P1. A finer
> 206	 * severity ladder (e.g. P0 for gross deviation) would need an explicit FR — TODO
> 207	 * cite FR-PSW-004 before adding one; do not invent thresholds here.
> 208	 */
> 209	export function findingsForLoudness(m: LoudnessMeasures, opts: LoudnessGateOptions = {}): Finding[] {
> 210	  const target = opts.targetLufs ?? SOCIAL_TARGET_LUFS;
> 211	  const tolerance = opts.toleranceLufs ?? LUFS_TOLERANCE;
> 212	  const maxTruePeak = opts.maxTruePeakDbtp ?? MAX_TRUE_PEAK_DBTP;
> 213	  const now = opts.now ?? (() => new Date().toISOString());
> 214	  const flow = opts.flow ?? LOUDNESS_FLOW;
> 215	  const detected_at = now();
> 216	
> 217	  const findings: Finding[] = [];
> 218	
> 219	  // Silence / immeasurable loudness → nothing to gate (documented above).
> 220	  if (!Number.isFinite(m.integrated_lufs)) return findings;
> 221	
> 222	  // 1) Integrated loudness vs. social target.
> 223	  const deviation = m.integrated_lufs - target; // + louder than target, - quieter
> 224	  if (Math.abs(deviation) > tolerance) {
> 225	    const tooLoud = deviation > 0;
> 226	    findings.push({
> 227	      id: tooLoud ? "loudness-il-too-loud" : "loudness-il-too-quiet",
> 228	      flow,
> 229	      severity: "P1",
> 230	      issue_type: "ux",
> 231	      title: tooLoud ? "Áudio acima do alvo de loudness" : "Áudio abaixo do alvo de loudness",
> 232	      description: tooLoud
> 233	        ? `A loudness integrada medida é ${round1(m.integrated_lufs)} LUFS, acima do alvo de ${round1(
> 234	            target,
> 235	          )} LUFS (±${round1(tolerance)} LU) para redes sociais. Áudio alto demais será atenuado na normalização da plataforma e pode soar comprimido.`
> 236	        : `A loudness integrada medida é ${round1(m.integrated_lufs)} LUFS, abaixo do alvo de ${round1(
> 237	            target,
> 238	          )} LUFS (±${round1(tolerance)} LU) para redes sociais. Áudio baixo demais será amplificado na normalização e pode elevar o ruído de fundo.`,
> 239	      repro_steps: [
> 240	        "Extrair a faixa de áudio do criativo.",
> 241	        "Medir a loudness integrada (EBU R128 / ITU-R BS.1770) com ffmpeg loudnorm.",
> 242	        `Comparar com o alvo social de ${round1(target)} LUFS (±${round1(tolerance)} LU).`,
> 243	      ],
> 244	      evidence_paths: {},
> 245	      suggested_fix: tooLoud
> 246	        ? `Reduza a loudness integrada para cerca de ${round1(target)} LUFS (normalize o áudio, ex.: ffmpeg loudnorm com alvo I=${round1(
> 247	            target,
> 248	          )}) antes de publicar.`
> 249	        : `Aumente a loudness integrada para cerca de ${round1(target)} LUFS (normalize o áudio, ex.: ffmpeg loudnorm com alvo I=${round1(
> 250	            target,
> 251	          )}) antes de publicar.`,
> 252	      detected_at,
> 253	    });
> 254	  }
> 255	
> 256	  // 2) True-peak ceiling (independent of the IL check).
> 257	  if (Number.isFinite(m.true_peak_dbtp) && m.true_peak_dbtp > maxTruePeak) {
> 258	    findings.push({
> 259	      id: "loudness-true-peak-clip",
> 260	      flow,
> 261	      severity: "P1",
> 262	      issue_type: "ux",
> 263	      title: "Pico real acima do teto (risco de clipping)",
> 264	      description: `O pico real (true peak) medido é ${round1(m.true_peak_dbtp)} dBTP, acima do teto de ${round1(
> 265	        maxTruePeak,
> 266	      )} dBTP (EBU R128). Isso pode gerar distorção por clipping entre amostras após a recodificação da plataforma.`,
> 267	      repro_steps: [
> 268	        "Medir o pico real (true peak, dBTP) do áudio com ffmpeg loudnorm.",
> 269	        `Comparar com o teto de ${round1(maxTruePeak)} dBTP.`,
> 270	      ],
> 271	      evidence_paths: {},
> 272	      suggested_fix: `Aplique um limitador de pico real com teto em ${round1(
> 273	        maxTruePeak,
> 274	      )} dBTP (ex.: ffmpeg loudnorm com TP=${round1(maxTruePeak)}) para eliminar o risco de clipping.`,
> 275	      detected_at,
> 276	    });
> 277	  }
> 278	
> 279	  return findings;
> 280	}
> 281	
> 282	// ─── Orchestration (impure: spawns ffmpeg) ───────────────────────────────────
> 283	/**
> 284	 * Run the loudness gate over an asset. `assetUrl` MUST already be SSRF-validated
> 285	 * by the caller (contract). Returns Finding[] (empty = on-target OR no audio).
> 286	 * Throws LoudnessError('loudness_probe_failed') when ffmpeg fails for a reason
> 287	 * other than "no audio stream" (fail-closed).
> 288	 *
> 289	 * @param runner injectable ffmpeg runner — defaults to spawning host ffmpeg.
> 290	 */
> 291	export async function loudnessGate(
> 292	  assetUrl: string,
> 293	  opts: LoudnessGateOptions = {},
> 294	  runner: FfmpegRunner = defaultRunner,
> 295	): Promise<Finding[]> {
> 296	  const { stderr, code } = await runner(assetUrl);
> 297	  const measures = parseLoudnormJson(stderr);
> 298	  if (!measures) {
> 299	    // No analysis block: either the asset has no audio (legit no-op) or ffmpeg
> 300	    // failed. Distinguish so silent-video assets don't hard-fail the gate.
> 301	    if (hasNoAudioStream(stderr)) return [];
> 302	    throw new LoudnessError("loudness_probe_failed", `ffmpeg exit ${code}`);
> 303	  }
> 304	  return findingsForLoudness(measures, opts);
> 305	}
> 306	
> ```

## 🤖 Claude *(19:55:54)*

<details>
<summary>💭 Thinking Process</summary>

I'm diving into a security review of an SSRF vulnerability fix, examining the `assertSafeImageUrl` function to understand how it validates URLs and blocks dangerous hostnames like localhost and private IP addresses.

The code also uses `assertTenantSupabaseOrigin` to verify that URLs match the configured Supabase origin and start with `/storage/`, then passes validated URLs to `loudnessGate` which eventually executes ffmpeg with the URL as a command-line argument.

Now I'm working through the first attack vector to see if the userinfo trick with `169.254.169.254@` can bypass the hostname validation. The userinfo in the URL is just treated as basic-auth credentials by ffmpeg and curl, so the actual connection still goes to the legitimate Supabase host—not an SSRF vulnerability. Since `.origin` correctly strips the userinfo and the downstream tools handle it the same way, this isn't a bypass.

I also check the reverse: if I flip it to make `169.254.169.254` the actual host with the Supabase domain as userinfo, the origin check immediately blocks the metadata IP, and the tenant origin validation fails anyway. Now looking at subdomain attacks—if someone tries to register a subdomain like `supabase-host.co.evil.com`, the hostname becomes that full subdomain, which won't match the legitimate Supabase origin.

For path-based tricks, the URL constructor normalizes paths, so something like `/storage/../@evil` gets resolved to its canonical form. is still supabase-host.co, so the pathname `//evil` fails the `/storage/` check anyway. The host is locked in by the origin, so path traversal can't redirect to another host — the origin check handles that, and the pathname check adds a layer of defense by ensuring we're actually accessing storage paths. Now I'm wondering about backslashes: in WHATWG URL parsing, backslashes get treated as forward slashes in special schemes, so something like `https://supabase-host.co\@evil.com/storage/` might be worth examining. abase-host.co becomes the authority, so the path starts with `/@evil.com/storage/x`, which doesn't match the required `/storage/` prefix—rejected. The connection would go to supabase-host.co anyway. The origin exact-match check is robust because the hostname that `new URL` parses is the same one that the actual HTTP client will connect to, so the invariant holds.

There are theoretical parser-differential bugs between Node's WHATWG parser and libcurl, but those are edge cases and not concrete bypasses for this scenario. Now I'm checking whether asset_url reaches ffmpeg only after passing through the origin pin, or if there's a code path that skips the guard.

The guard in `parseSensoryGate` runs first before `loudnessGate` is called, so within that function the protection holds. But I need to verify whether `loudnessGate` is exported and called from elsewhere without the guard, and whether `parseSensoryGate` is the only entry point. I'm also checking `describeImage` — it does validate with `assertSafeImageUrl` but lacks the origin pin, though it passes the image_url to a VLM provider via fetch, not to ffmpeg.

Now I'm considering whether Supabase Storage could redirect to an internal host even when pinned to the Supabase domain, since the pin only locks the first hop.  Supabase Storage endpoints typically return the object bytes directly with a 200 response, but in some configurations backed by S3 or a CDN, they might issue a redirect. However, any redirect would go to Supabase's own CDN or S3 backend, not to an attacker-controlled or internal metadata endpoint, so this doesn't create an exploitable SSRF path. All tenants' assets are stored on the same MCORCH Supabase project, not their own — the container's `SUPABASE_ORIGIN` is pinned to that shared project, so tenants can't control responses from it and can't inject a redirect. This closes off the SSRF vector even more tightly. Now I'm wondering if a tenant could upload a malicious asset that exploits something when fetched. not an input vector. So execFile with the array prevents shell injection, and the argument position prevents flag injection. Closed.

Now looking at command injection through ffmpegLoudnormArgs itself — could the loudness values be manipulated to inject flags? The protocol check also blocks `file://` and other schemes before the pin even matters. Since the URL is passed as a single argument to execFile with no shell expansion, there's no way to inject a second `-i` flag or other options into it — it's treated as one token regardless of what characters it contains. Now I'm checking whether an empty SUPABASE_ORIGIN environment variable could cause a fail-open vulnerability. pass. Now I need to verify there's no other code path into loudnessGate or ffmpeg that bypasses the guard, and confirm the server handler for parse_sensory_gate actually invokes parseSensoryGate with the guard rather than calling loudnessGate directly. I'm also checking that `input.asset_url` is the exact same string passed to both the guard and the actual function — no mutations or re-parsing between them, which would be a classic TOCTOU bypass vector.

There's a subtle parser-differential concern though: the guard validates using the WHATWG URL parser, but ffmpeg gets the raw string and parses it with its own parser (libavformat/libcurl). If these two parsers disagree on what the host is, the guard could see one domain while ffmpeg sees another — a classic SSRF via parser confusion attack. I need to check if there's a concrete divergence that could actually happen here. The pathname requirement acts as a defense layer — for a bypass to work, the attacker would need WHATWG to parse the URL as the legitimate Supabase origin with a `/storage/` path, while ffmpeg connects to a different host from that same URL string. The userinfo approach doesn't help here since there's no userinfo in the legitimate URL structure. info stripped). Passes! And ffmpeg/libcurl: userinfo=user, host=supabase-host. Same host. Connection to supabase-host. Not a bypass (still hits legit host). Fine.

The dangerous differential would be something like `https://<supabase-host> /something@evil` with control chars, or tab/newline injection. WHATWG strips tabs and newlines from URLs. libcurl rejects them. Differences there tend to make libcurl reject, not connect to attacker host. Generally the differential attacks that reach an attacker host require the WHATWG parser to be LENIENT where libcurl is LENIENT differently. Given the exact origin + pathname double-pin, I assess the residual parser-differential risk as low and not a concrete >80% bypass. I'll note it as a residual hardening suggestion (ffmpeg has no `-

protocol_whitelist` here; could add `-protocol_whitelist https,tls,tcp` as defense in depth) but not a confirmed bypass.

Actually, I'm reconsidering whether to recommend `-protocol_whitelist`. The URL is pinned to https Supabase origin, so ffmpeg gets an https URL. But ffmpeg's default could follow protocols within playlists—if a tenant uploads a malicious playlist file like an `.m3u8` or concat file, it might reference `file:///` or `http://169.254...` URLs, which is a real concern I need to think through.

This is actually a known ffmpeg SSRF/LFI vector: a crafted playlist can make ffmpeg fetch arbitrary URLs or read local files, even if the initial asset_url is pinned to Supabase. The host-pin alone doesn't fully protect against this because ffmpeg will follow references embedded in the playlist itself.

The attack works like this: an attacker with `swarm:read` scope uploads a malicious manifest file (like an `.m3u8` playlist or `.ffconcat` script) to their own creative_assets, and when ffmpeg processes it for loudness analysis, it auto-detects the format and follows the internal references using its default protocol whitelist, which typically includes file, http, https, and other protocols that could expose local files or internal services.

The real danger is that even though the loudnorm output isn't directly visible to the attacker, ffmpeg will make requests to those URIs — including potentially to AWS metadata endpoints like `169.254.169.254` — creating a blind SSRF vulnerability that could leak sensitive information through timing differences, error responses, or side-channel effects. The ffmpeg error messages don't leak the actual fetched content back to the user, just exit codes and loudness metrics, so this remains blind SSRF. I'm also considering whether the concat and HLS demuxers have external protocol access enabled by default — historically ffmpeg has restricted some protocols, though the exact defaults around file access and HTTP/HTTPS handling have shifted after various CVE patches.

The real question is whether the proposed fix actually closes the SSRF vector via redirects, or if there are still gaps in the host pinning approach.

The redirect fix handles the 302 case, but there's a separate SSRF risk through ffmpeg's playlist demuxer — a malicious manifest hosted on the pinned Supabase domain could still reference external resources internally. That's a different attack surface the host pin doesn't fully address.

Before I can be confident in my assessment, I need to verify whether tenants can actually upload arbitrary manifest files to the creative_assets bucket that the tool will process, since the asset_url is supposed to be a signed, owner-scoped Supabase Storage URL.

Looking at the ffmpeg configuration, there's no `-protocol_whitelist` or `-safe` flag being passed, so it's relying entirely on ffmpeg's default behavior. The question is what protocols ffmpeg actually allows by default when processing demuxer-initiated requests.

The HLS demuxer in particular has its own whitelist enforcement post-CVE, defaulting to something like `file,crypto,data,http,https,tcp,tls`, but I'm uncertain about the exact version behavior in the container. The blind-SSRF-via-playlist approach is plausible in theory, but it depends on whether the container's ffmpeg version has the necessary permissions and protocol allowances to actually follow those requests.

For the scope of this assessment, I should focus on whether the host-pinning fix actually closes the redirect vector it was designed to address — it does, since the attacker can't force MCORCH's Supabase connection to redirect to an internal address. However, there's a separate residual SSRF risk through ffmpeg's demuxer protocol handling that the host-pin doesn't cover, so I'd recommend adding an explicit protocol whitelist like `-protocol_whitelist https,tls,tcp` to further constrain what ffmpeg can access.

I'm going to verify the ffmpeg invocation doesn't already have these restrictions in place and check the Dockerfile for the ffmpeg version to gauge how plausible the playlist vector actually is.

</details>


## 🤖 Claude *(19:55:54)*

Now let me verify there are no other entry points to `loudnessGate`/ffmpeg that skip the guard, and check the server wiring and the container's ffmpeg setup.

## 🤖 Claude *(19:55:57)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== callers of loudnessGate ===\" && grep -rn \"loudnessGate\" src/ && echo \"\" && echo \"=== callers of parseSensoryGate ===\" && grep -rn \"parseSensoryGate\" src/ && echo \"\" && echo \"=== callers of ffmpegLoudnormArgs / execFile / ffmpeg ===\" && grep -rn \"ffmpegLoudnormArgs\\|execFile\\|spawn\\|\\\"ffmpeg\\\"\\|'ffmpeg'\" src/",
  "description": "Find all callers of loudness gate and ffmpeg invocation"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === callers of loudnessGate ===
> src/tools/parse-sensory-gate.ts:8://   2. loudnessGate(asset_url)              (ffmpeg loudnorm IL/LRA/TP — FR-PSW-004)  → Finding[]
> src/tools/parse-sensory-gate.ts:35:import { loudnessGate, type Finding, type FfmpegRunner } from "../tier1/loudness.js";
> src/tools/parse-sensory-gate.ts:146:    const loudnessFindings = await loudnessGate(input.asset_url, { now }, opts.loudnessRunner);
> src/tier1/loudness.test.ts:9:  loudnessGate,
> src/tier1/loudness.test.ts:189:// ─── loudnessGate (mocked ffmpeg runner) ─────────────────────────────────────
> src/tier1/loudness.test.ts:190:describe("loudnessGate — end to end with mocked ffmpeg", () => {
> src/tier1/loudness.test.ts:201:    expect(await loudnessGate(url, PINNED, mockRunner(ON_TARGET))).toEqual([]);
> src/tier1/loudness.test.ts:205:    const findings = await loudnessGate(url, PINNED, mockRunner(TOO_LOUD));
> src/tier1/loudness.test.ts:211:    expect(await loudnessGate(url, PINNED, mockRunner(NO_AUDIO_STDERR, 1))).toEqual([]);
> src/tier1/loudness.test.ts:216:    await expect(loudnessGate(url, PINNED, brokenRunner)).rejects.toBeInstanceOf(LoudnessError);
> src/tier1/loudness.test.ts:217:    await expect(loudnessGate(url, PINNED, brokenRunner)).rejects.toMatchObject({
> src/tier1/loudness.ts:15:// Tier 1 foothold. If ffmpeg is absent, `loudnessGate` throws
> src/tier1/loudness.ts:160: * analysis block is present (e.g. asset has no audio stream — see loudnessGate).
> src/tier1/loudness.ts:291:export async function loudnessGate(
> 
> === callers of parseSensoryGate ===
> src/tools/parse-sensory-gate.ts:111:export async function parseSensoryGate(
> src/mcp/server.ts:34:import { parseSensoryGate } from "../tools/parse-sensory-gate.js";
> src/mcp/server.ts:371:        const result = await parseSensoryGate(input, sub);
> 
> === callers of ffmpegLoudnormArgs / execFile / ffmpeg ===
> src/tools/parse-sensory-gate.ts:60:  loudnessRunner?: FfmpegRunner; // injectable ffmpeg runner (default: spawn host ffmpeg)
> src/tier1/loudness.test.ts:10:  ffmpegLoudnormArgs,
> src/tier1/loudness.test.ts:194:    const args = ffmpegLoudnormArgs(url);
> src/tier1/loudness.ts:33:import { execFile } from "node:child_process";
> src/tier1/loudness.ts:100:/** Injectable ffmpeg runner (default spawns host ffmpeg). Tests mock this. */
> src/tier1/loudness.ts:116:export function ffmpegLoudnormArgs(assetUrl: string): string[] {
> src/tier1/loudness.ts:133:    execFile(
> src/tier1/loudness.ts:134:      "ffmpeg",
> src/tier1/loudness.ts:135:      ffmpegLoudnormArgs(assetUrl),
> src/tier1/loudness.ts:282:// ─── Orchestration (impure: spawns ffmpeg) ───────────────────────────────────
> src/tier1/loudness.ts:289: * @param runner injectable ffmpeg runner — defaults to spawning host ffmpeg.
> ```

## 🤖 Claude *(19:55:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== server handler wiring for parse_sensory_gate ===\" && grep -rn \"parse_sensory_gate\\|parseSensoryGate\\|asset_url\" src/server.ts src/tools/ 2>/dev/null | grep -iv \"//\" | head -40",
  "description": "Inspect server handler wiring for the tool"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === server handler wiring for parse_sensory_gate ===
> src/tools/parse-sensory-gate.ts:107:    throw new Error("asset_url_not_tenant_storage");
> src/tools/parse-sensory-gate.ts:111:export async function parseSensoryGate(
> src/tools/parse-sensory-gate.ts:128:    assertSafeImageUrl(input.asset_url);
> src/tools/parse-sensory-gate.ts:129:    assertTenantSupabaseOrigin(input.asset_url);
> src/tools/parse-sensory-gate.ts:132:      field: "asset_url",
> src/tools/parse-sensory-gate.ts:146:    const loudnessFindings = await loudnessGate(input.asset_url, { now }, opts.loudnessRunner);
> src/tools/parse-sensory-gate.ts:154:    logHealth("degraded", "tool_error", { tool: "parse_sensory_gate", code, tier: 1 }, SERVICE);
> src/tools/parse-sensory-gate.ts:202:      tool: "parse_sensory_gate",
> ```

## 🤖 Claude *(19:56:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== Dockerfile ffmpeg install / version ===\" && find . -maxdepth 2 -iname \"Dockerfile*\" -exec echo \"--- {} ---\" \\; -exec grep -n \"ffmpeg\\|apk add\\|FROM\\|alpine\\|node:\" {} \\; 2>/dev/null",
  "description": "Find container Dockerfile and ffmpeg version basis"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === Dockerfile ffmpeg install / version ===
> --- ./Dockerfile ---
> 7:FROM --platform=$BUILDPLATFORM node:22-alpine AS builder
> 16:FROM node:22-alpine AS runtime
> 19: && apk add --no-cache tini ffmpeg \
> ```

## 🤖 Claude *(19:56:12)*

<details>
<summary>💭 Thinking Process</summary>

I need to verify how the server handler processes the asset URL at line 371, check what validation constraints exist at the schema level for the sensory gate parser, and confirm the ffmpeg version that comes with the Alpine Node image. Let me also cross-reference the test expectations in loudness.test.ts against the PINNED constant to make sure everything aligns.

</details>


## 🤖 Claude *(19:56:12)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/packages/vision-mcp-core/src/mcp/server.ts",
  "offset": 350,
  "limit": 40
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 350	        .optional(),
> 351	    },
> 352	    async (input: {
> 353	      asset_url: string;
> 354	      question?: string;
> 355	      tier?: 1;
> 356	      layer_colors?: Array<{ foreground: string; background: string; text_kind?: "normal" | "large"; label?: string }>;
> 357	    }) => {
> 358	      const sub = currentSub();
> 359	      const scopeDenied = requireScope("swarm:read");
> 360	      if (scopeDenied) return scopeDenied;
> 361	      // Sentinel over the optional Tier 2 foveal `question` (the Fatia 2 semantic seam), AFTER identity,
> 362	      // BEFORE any work — mirrors describe_image / deepsearch_run (FR-VM-005a).
> 363	      if (input.question) {
> 364	        const verdict = inspectPrompt(input.question, sub);
> 365	        if (!verdict.allow) {
> 366	          logHealth("degraded", "sentinel_block", { code: verdict.code, tool: "parse_sensory_gate" }, "sentinel");
> 367	          return toolError({ error: verdict.code, layer: "sentinel" });
> 368	        }
> 369	      }
> 370	      try {
> 371	        const result = await parseSensoryGate(input, sub);
> 372	        return {
> 373	          content: [{ type: "text" as const, text: JSON.stringify(result, null, 2) }],
> 374	          structuredContent: result as unknown as Record<string, unknown>,
> 375	        };
> 376	      } catch (e) {
> 377	        const code = (e as { code?: string })?.code ?? "parse_sensory_gate_failed";
> 378	        logHealth("degraded", "tool_error", { tool: "parse_sensory_gate", code }, "predictive-swarm");
> 379	        const payload: Record<string, unknown> = { error: code, layer: code === "validation_failed" ? "validation" : "tool" };
> 380	        if (code === "validation_failed") {
> 381	          // FRD §4.4 — field + PT-BR message in the body.
> 382	          payload.field = (e as { field?: string }).field;
> 383	          payload.message = (e as Error).message;
> 384	        }
> 385	        return toolError(payload);
> 386	      }
> 387	    },
> 388	  );
> 389	
> ```

## 🤖 Claude *(19:56:14)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== parse_sensory_gate input schema (asset_url validation) ===\" && grep -rn \"asset_url\\|parse_sensory_gate\\|inputSchema\\|z.string\\|zod\" src/mcp/server.ts | head -30 && echo \"\" && echo \"=== any schema file ===\" && grep -rln \"parse_sensory_gate\\|asset_url\" src/ | grep -i \"schema\\|server\"",
  "description": "Check input schema constraints on asset_url"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === parse_sensory_gate input schema (asset_url validation) ===
> src/mcp/server.ts:19:import { z } from "zod";
> src/mcp/server.ts:78:    { query: z.string().trim().min(1), top_k: z.number().int().min(1).max(50).optional() },
> src/mcp/server.ts:106:      image_url: z.string().url(),
> src/mcp/server.ts:107:      question: z.string().trim().min(1).optional(),
> src/mcp/server.ts:146:      video_url: z.string().url(),
> src/mcp/server.ts:147:      question: z.string().trim().min(1).optional(),
> src/mcp/server.ts:182:    { url: z.string().url() },
> src/mcp/server.ts:208:      name: z.string().trim().min(1),
> src/mcp/server.ts:209:      content: z.string().trim().min(1),
> src/mcp/server.ts:210:      node_type: z.string().trim().min(1).optional(),
> src/mcp/server.ts:214:          source_url: z.string().url().optional(),
> src/mcp/server.ts:215:          license: z.string().optional(),
> src/mcp/server.ts:219:      retention_until: z.string().optional(),
> src/mcp/server.ts:258:      query: z.string().trim().min(1),
> src/mcp/server.ts:260:      source_allowlist: z.array(z.string()).max(20).optional(),
> src/mcp/server.ts:311:    { job_id: z.string().trim().min(1) },
> src/mcp/server.ts:329:  // FR-PSW-002/004/005/012 — vision.parse_sensory_gate (predictive-swarm Fatia 1: Tier 1 objective gate,
> src/mcp/server.ts:334:    "vision_parse_sensory_gate",
> src/mcp/server.ts:337:      asset_url: z.string().url(),
> src/mcp/server.ts:338:      question: z.string().trim().min(1).optional(),
> src/mcp/server.ts:343:            foreground: z.string().trim().min(1),
> src/mcp/server.ts:344:            background: z.string().trim().min(1),
> src/mcp/server.ts:346:            label: z.string().trim().min(1).optional(),
> src/mcp/server.ts:353:      asset_url: string;
> src/mcp/server.ts:366:          logHealth("degraded", "sentinel_block", { code: verdict.code, tool: "parse_sensory_gate" }, "sentinel");
> src/mcp/server.ts:377:        const code = (e as { code?: string })?.code ?? "parse_sensory_gate_failed";
> src/mcp/server.ts:378:        logHealth("degraded", "tool_error", { tool: "parse_sensory_gate", code }, "predictive-swarm");
> src/mcp/server.ts:402:      send(res, 200, { status: "ok", protocol: PROTOCOL_VERSION, tools: ["mesh_search", "vision_describe_image", "vision_analyze_video", "deepsearch_scrape", "mesh_consolidate_reference", "deepsearch_run", "deepsearch_poll", "vision_parse_sensory_gate"] });
> 
> === any schema file ===
> src/mcp/server.ts
> ```

## 🤖 Claude *(19:57:01)*

<details>
<summary>💭 Thinking Process</summary>

I'm tracing the call chain to understand the attack surface: `loudnessGate` is only invoked by `parseSensoryGate` in production, which itself is only called from the server endpoint `vision_parse_sensory_gate` that requires `swarm:read` scope and accepts any valid URL through the `asset_url` parameter—not restricted to HTTPS or Supabase domains.

The input string flows directly through without mutation, so the same URL reaches both the guard and ffmpeg. The container runs Alpine's ffmpeg 6.x without explicit protocol whitelisting in the arguments, so I need to determine whether modern ffmpeg will follow external protocol references embedded in HLS manifests or concat files fetched over HTTPS.

The key question is how ffmpeg's protocol whitelist works by default. When a demuxer like HLS opens nested resources, it checks against the `protocol_whitelist` in the format context. If that's unset, ffmpeg inherits a default whitelist based on the parent protocol—so opening an input over HTTPS should restrict nested protocols accordingly.

The documented behavior is that `file://` is excluded from the default whitelist for network-sourced inputs specifically to prevent SSRF/LFI attacks. This was hardened after CVEs where malicious `.m3u8` or concat files could trick ffmpeg into reading local files. So the exploit vector is largely closed unless someone explicitly enables `file` in the whitelist.

The remaining question is whether nested protocol fetches—like an HLS manifest on Supabase pointing to `http://169.254.169.254/latest/meta-data/`—would work. If the default nested whitelist includes `http` alongside `https` and `tcp`, then yes, this would be a blind SSRF. But if only `https` is allowed for nested protocols, the attacker would need an HTTPS endpoint at that metadata address, which doesn't exist (IMDS only serves HTTP), so the connection would fail at the TLS handshake and the attack wouldn't work.

This is a real gap in the host-pinning defense—it only blocks HTTP 3xx redirects at the top level, not nested references embedded in attacker-controlled files hosted on the pinned origin. However, the exploitability is uncertain because it depends on the exact ffmpeg version's default whitelist, and even if it works, the impact is blind with no clear way to exfiltrate credentials through audio loudness metrics. Given those constraints, I'm below my confidence threshold for reporting this as a confirmed bypass.

Instead, I should flag it as a hardening recommendation—adding protocol whitelisting and demuxer restrictions would close this gap and make the fix's claim more precise. Now I'm moving through the seven specific attack vectors to assess each one. ://concat: protocol at the URL level). Covered. With SUPABASE_ORIGIN empty, the system fails closed and rejects everything. There's one residual risk though — ffmpeg could still be vulnerable to nested-protocol SSRF if an attacker uploads a malicious playlist to the pinned origin, which the pin alone doesn't prevent. That's worth adding `-protocol_whitelist` as defense-in-depth, though it's plausible rather than a confirmed bypass. Let me verify that `new URL` normalizes `..` sequences as expected per the WHATWG spec and trace through what gets passed to the parser.

The server passes `input` directly to `parseSensoryGate`, and both the zod schema validation and `assertSafeImageUrl` independently call `new URL` on the same string, so they'll always produce the same result. The zod `.url()` validator accepts any scheme, but `assertSafeImageUrl` enforces HTTPS, so that guard is solid. Now I need to check what a valid pinned URL looks like in the test constants to finalize my verdict. Now I'll write the report.

</details>


## 🤖 Claude *(19:57:43)*

Tenho o quadro completo. Confirmei os fatos materiais:

- **Único caminho de produção até o ffmpeg:** `server.ts:371` → `parseSensoryGate` → `loudnessGate` (linha 146). O guard (linhas 127-135) roda ANTES, sobre o mesmíssimo `input.asset_url` que depois vai ao ffmpeg (sem mutação, sem re-parse divergente). Não há chamada direta a `loudnessGate`/`ffmpeg` fora desse fluxo (só nos testes).
- **Schema:** `asset_url: z.string().url()` — aceita qualquer esquema; quem restringe é o guard.
- **Container:** `node:22-alpine` + `apk add ffmpeg`. Os args (`ffmpegLoudnormArgs`) NÃO passam `-protocol_whitelist` nem `-f`.

---

## Verificação adversarial — SSRF do predictive-swarm Fatia 1

**Veredito por vetor:**

1. **Userinfo trick** `https://169.254.169.254@<supabase-host>/storage/…` → **NÃO bypassa.** `new URL().origin` descarta o userinfo: retorna `https://<supabase-host>` (== `SUPABASE_ORIGIN`) e o hostname real é `<supabase-host>`. A conexão do ffmpeg/libcurl vai ao host Supabase legítimo, mandando `169.254.169.254` só como usuário de basic-auth. Não alcança rede interna. (O inverso `https://<host>@169.254.169.254/` é barrado: hostname vira `169.254.169.254` → bloqueado por `assertSafeImageUrl` E falha o origin-pin.)

2. **Subdomínio** `https://<supabase-host>.evil.com/storage/…` → **NÃO.** O pin é igualdade EXATA (`u.origin !== SUPABASE_ORIGIN`), não sufixo/substring. `https://abc.supabase.co.evil.com` ≠ `https://abc.supabase.co` → lança.

3. **Path trick** `…/storage/../@evil` ou `//evil` → **NÃO.** `new URL()` normaliza o path ANTES da checagem: `/storage/../@evil` vira `/@evil`, que não passa em `startsWith('/storage/')`. E o host é fixado pelo origin — traversal de path não muda host. Backslash (`\`) em esquema special vira separador de path no WHATWG, o que empurra o payload pro pathname e também reprova o `/storage/`.

4. **asset_url chega ao ffmpeg só depois do pin?** → **SIM (coberto).** Caller único, guard-first, string idêntica. Nenhum caminho pula o guard (o outro consumidor de `assertSafeImageUrl`, `describeImage`, entrega a URL ao provedor VLM remoto — não ao ffmpeg do container). Não há TOCTOU: a string validada É a string executada.

5. **Redirect do Supabase Storage para host interno** → **NÃO (é a raiz que o fix fecha).** O pin não é ao Supabase do tenant — é ao `SUPABASE_URL` do PRÓPRIO container (projeto MCORCH). O objeto é assinado/owner-scoped e o Storage devolve os bytes com 200 (ou, no máximo, 3xx para CDN pública do próprio Supabase — nunca para `169.254.169.254`). O atacante não controla as respostas HTTP do host MCORCH ⇒ não consegue emitir o 302→interno. O pin transforma "Supabase não redireciona pra host interno" de suposição em invariante.

6. **Command/flag injection** → **NÃO.** `execFile("ffmpeg", array, …)` — sem shell, zero splitting. `asset_url` é UM argv, valor do `-i` (ffmpeg o consome como input, não como flag). E o pin exige `https://` + origin Supabase ⇒ a URL não pode começar com `-` nem usar protocolos-armadilha do ffmpeg (`file:`, `concat:`, `subfile:`) no nível da URL, pois `assertSafeImageUrl` já exige `protocol === 'https:'`.

7. **SUPABASE_ORIGIN vazio (env ausente)** → **FAIL-CLOSED.** `if (!SUPABASE_ORIGIN || …)` lança primeiro ⇒ rejeita TUDO. Sem origin configurado, nenhuma URL passa. Correto.

---

## Residual honesto (fora do escopo do redirect, mas o guard NÃO cobre)

**SSRF cega via referência aninhada do ffmpeg (playlist/manifest em asset legítimo).** O pin garante que o RECURSO DE TOPO está no host Supabase MCORCH — mas um tenant com `swarm:read` pode subir um `creative_asset` legítimo (portanto na origem pinada, `/storage/…`) cujo CONTEÚDO seja um manifesto HLS/`.ffconcat`/container com referências externas (`http://169.254.169.254/…`). O demuxer do ffmpeg pode buscar essas referências internas. Os args atuais **não passam `-protocol_whitelist`**, dependendo só dos defaults do ffmpeg do Alpine.

Classificação honesta (Lei 1): **PLAUSÍVEL, abaixo do meu limiar de 80% para "bypass confirmado"** — porque (a) é CEGA (loudnorm devolve só números de loudness; não há canal de exfil dos bytes buscados, então roubo de credencial do IMDS não se materializa), e (b) depende do default whitelist da versão do ffmpeg no container (versões modernas já excluem `file` por default e frequentemente restringem `http` aninhado quando o pai é `https`). Não consegui provar exploração funcional sem sondar o container. É superfície residual, não SSRF-de-redirect.

**Hardening recomendado (defense-in-depth, 1 linha):** adicionar `"-protocol_whitelist", "https,tls,tcp"` (e opcionalmente `-f` forçando o demuxer esperado) em `ffmpegLoudnormArgs`. Fecha o vetor aninhado sem custo. O comentário do fix ("no caller-controlled host ever reaches ffmpeg") está levemente superdimensionado: um FILE controlado pelo caller na origem pinada chega ao ffmpeg — o pin cobre o host, não o conteúdo.

---

## Veredito final

**O SSRF-de-redirect está FECHADO.** O host-pin (`origin === SUPABASE_ORIGIN` exato + `pathname startsWith '/storage/'` + fail-closed quando o env falta), combinado ao `assertSafeImageUrl` (https-only + bloqueio de privado/loopback/link-local) e ao `execFile` sem shell, cobre concretamente os 7 vetores sondados — nenhum bypass do host-pin com >80% de confiança. Os truques de userinfo/subdomínio/path caem no origin-match exato; o redirect malicioso é impossível porque o atacante não controla as respostas do Supabase MCORCH; a injeção de flag é barrada pelo array + pin https.

**Ressalva única:** o pin fecha o host, não o conteúdo do asset — resta a superfície residual (cega, versão-dependente) da referência aninhada do ffmpeg, endereçável com um `-protocol_whitelist https,tls,tcp` como endurecimento. Recomendo aplicá-lo, mas não é um bypass do fix atual.

Arquivos auditados: `/home/gcrUX/htdocs/constellation-orchestra/packages/vision-mcp-core/src/tools/parse-sensory-gate.ts`, `/home/gcrUX/htdocs/constellation-orchestra/packages/vision-mcp-core/src/tools/describe-image.ts`, `/home/gcrUX/htdocs/constellation-orchestra/packages/vision-mcp-core/src/tier1/loudness.ts`, `/home/gcrUX/htdocs/constellation-orchestra/packages/vision-mcp-core/src/mcp/server.ts`, `/home/gcrUX/htdocs/constellation-orchestra/packages/vision-mcp-core/Dockerfile`.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-15 - agent-acdf7ddad1d31fb89]]
> * **Próxima Sessão**: [[2026-07-15 - agent-ad07e409734249e33]]
%% --- TIMELINE END --- %%

# Session agent-a30eb0adeffa481fc
**Date:** 2026-07-21 | **Session ID:** `agent-a30eb0adeffa481fc`

---

## 👤 User *(10:05:16)*

Repo: /home/gcrUX/htdocs/constellation-orchestra (React+Supabase; edge fns em supabase/functions/; UI em src/; SOPs docs/processes/; BoK docs/bok/). READ-ONLY: não modifique nada, no DB só SELECT. TODA afirmação com evidência file:line ou output real (Lei 1). Sua mensagem final é DADO BRUTO p/ um orquestrador — seja exaustivo mas factual; marque UNVERIFIED o que não conseguir provar. User 0 = ada39fae-67e1-4e53-af1c-5a18e1c108e8.

MISSÃO C1 — Cadência de agendamento para VÍDEO (POV/split-screen/cortes).
O gap conhecido: o motor cadence-run Fatia 1 enfileira SÓ o caption (sem mídia) — youtube/tiktok morreriam em *_no_video. Mapeie EXATAMENTE:
1. supabase/functions/cadence-run/index.ts — onde monta a linha scheduled_posts (o dispatch). Confirme que NÃO anexa asset. Qual o shape do metadata.reshape que ele grava?
2. supabase/functions/auto-publish/index.ts — como resolve mídia: já vimos que resolve space_publish_variant_id / channel_variant_id / carousel_render_id owner-scoped e seta content.video_url (auto-publish attachAsset). Então a correção mínima da cadência = fazer o cadence-run gravar um space_publish_variant_id (ou asset id) no metadata.reshape, resolvido owner-scoped do program.source_asset_id.
3. O program do plano de cadência (autopilot_plans.program) carrega source_asset_id (o SUJEITO). Um cadence dispatch de um asset de vídeo → precisa que exista uma space_publish_variant apontando esse asset. Como criar essa variant no arm do plano (cadence-plan) ou no dispatch (cadence-run)? publish-space-asset publish:false cria a variant idempotente — dá para o cadence-run chamar isso internamente, ou criar a variant direto?
4. Proponha a FATIA MÍNIMA (edge fn + smoke) que faz "agendar um corte/POV/split-screen em cadência recorrente, privado-primeiro" funcionar E2E, reusando os trilhos vivos, sem migration se possível. Liste os arquivos exatos a tocar + o gate zero-custo que provaria.
Retorne: diagnóstico file:line + a fatia mínima proposta.

## 🤖 Claude *(10:05:21)*

<details>
<summary>💭 Thinking Process</summary>

I'm diving into the cadence scheduling engine to understand how it orchestrates video content publishing. I need to examine the core functions that handle the scheduling logic, starting with the cadence-run and auto-publish functions, then trace through the related programs and data structures that define how content gets queued and published.

</details>


## 🤖 Claude *(10:05:21)*

I'll investigate the cadence scheduling engine for video content. Let me start by reading the core files mentioned in the mission.

## 🤖 Claude *(10:05:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/ | grep -iE \"cadence|auto-publish|publish-space|publish-channel\"",
  "description": "List cadence/publish edge functions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> drwxrwxr-x   2 gcrUX  gcrUX  4096 Jul 15 15:15 autopilot-cadence-cron
> drwxrwxr-x   2 gcrUX  gcrUX  4096 Jul 20 10:28 auto-publish
> drwxrwxr-x   2 ubuntu ubuntu 4096 Jul 15 15:35 cadence-plan
> drwxrwxr-x   2 ubuntu ubuntu 4096 Jul 15 15:35 cadence-run
> drwxrwxr-x   2 gcrUX  gcrUX  4096 Jun 28 00:19 publish-channel-variant
> drwxrwxr-x   2 ubuntu ubuntu 4096 Jul 20 10:28 publish-space-asset
> drwxrwxr-x   2 ubuntu ubuntu 4096 Jul 14 09:18 publish-space-carousel
> ```

## 🤖 Claude *(10:05:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "find /home/gcrUX/htdocs/constellation-orchestra/supabase/functions -maxdepth 1 -type d -name \"*cadence*\" -o -maxdepth 1 -type d -name \"*publish*\" 2>/dev/null; echo \"---\"; ls /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/ | sort",
  "description": "Find cadence and publish functions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-cadence-cron
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/cadence-plan
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-space-asset
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-channel-variant
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/cadence-run
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/auto-publish
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-space-carousel
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-meta
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-social
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-wordpress
> ---
> admin-manage-user
> aeo-audit
> agent-task-execute
> aios-chat
> aios-chat-gateway
> aios-chat-stream
> aios-live-proxy
> aios-sql-bridge
> analyze-node
> analyze-sem
> analyze-seo
> autopilot-analyze
> autopilot-cadence-cron
> autopilot-collect
> autopilot-run
> auto-publish
> avatar-consent
> avatar-identity-train
> award-mco-coins
> cadence-plan
> cadence-run
> campaign-run
> canvas-execute
> check-post-existence
> check-subscription
> check-video-status
> collect-publication-metrics
> connect-instagram-token
> create-checkout
> create-portal
> data-export
> delete-account
> delete-remote-post
> design-job-enqueue
> detect-viral-moments
> discover-products
> embed-mcorch-node
> erase-avatar-artifacts
> fetch-trends
> generate-audio-script
> generate-carousel
> generate-content
> generate-image
> generate-script-package
> generate-video
> generate-video-script
> generate-voice
> get-infra-status
> handle-ml-postback
> higgsfield-oauth-callback
> higgsfield-oauth-init
> higgsfield-webhook
> ingest-external-asset
> instagram-webhook
> intent-execute
> intent-orchestrate
> lead-score
> list-provider-models
> meta-privacy
> nurture-cron
> nurture-dispatch
> openrouter-swarm
> optimize-schedule
> orchestrate-content
> orchestrate-step
> pinterest-boards
> process-affiliate-link
> publish-channel-variant
> publish-meta
> publish-social
> publish-space-asset
> publish-space-carousel
> publish-wordpress
> refresh-social-token
> rescue-video
> reshape-pillar
> search-constellation
> seed-global-app-creds
> self-heal
> self-optimize
> _shared
> social-auth-callback
> social-auth-init
> stripe-webhook
> submit-lead-webhook
> sync-knowledge-mesh
> sync-meta-ads
> test-api-key
> tiktok-login-callback
> tiktok-login-init
> tiktok-login-session
> trigger-embeddings
> trigger-ingest
> tts-speak
> veo-poll
> video-render
> video-repurpose-run
> whatsapp-templates
> whatsapp-webhook
> youtube-data
> ```

## 🤖 Claude *(10:05:26)*

I'll read the core files. Let me start with cadence-run, auto-publish, cadence-plan, and publish-space-asset in parallel.

## 🤖 Claude *(10:05:27)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/cadence-run/index.ts"
}
```

## 🤖 Claude *(10:05:28)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/cadence-plan/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// cadence-plan — spaces-cadence Fatia 1 arm endpoint (FR-CAD-005 + FR-CAD-007). verify_jwt=false.
> 2	//
> 3	// BoK SSOT (Lei 1 — no invention beyond the sealed suite):
> 4	//   docs/bok/spaces-cadence/05-sdd.md  §2.3/§3.1/§4 (design + API contract for POST /cadence-plan)
> 5	//   docs/bok/spaces-cadence/06-data-model.md §2.1/§3.1 (autopilot_plans columns + tenancy)
> 6	//   docs/bok/spaces-cadence/07-process-flow.md (arm flow + recovery)
> 7	//   docs/bok/spaces-cadence/04-frd.md  FR-CAD-005 (arm) + FR-CAD-007 (generalized UTC re-arm)
> 8	//
> 9	// RESPONSIBILITY (FR-CAD-005): receive a USER JWT, upsert the cadence plan into autopilot_plans
> 10	//   (plan_kind='cadence' + recurrence/program/quiet_hours/channel_allowlist/budget_cap_mco), and ARM
> 11	//   next_run_at in UTC computed from {frequency,days,hours,minutes,tz} (FR-CAD-007 generalized re-arm).
> 12	//   Owner-scoped (auth.uid()). Creating a plan costs 0 mco (the node does not generate — SDD §4;
> 13	//   the G7 quote==charge invariant belongs to the CYCLE begin/finalize, never to the arm).
> 14	//
> 15	// IDENTITY (SDD §5.3): user-facing endpoint. This function is registered verify_jwt=false in config.toml
> 16	//   (the sovereign-orchestration bypass block), so identity is verified IN-FUNCTION via the Supabase auth
> 17	//   server (supabase.auth.getUser with an anon-key client bound to the caller's Authorization header — the
> 18	//   SAME living pattern as canvas-execute:184-211 / autopilot-run:78-83). getUser() validates the JWT
> 19	//   signature server-side (it is NOT a blind atob of the token). user_id is server-trusted from the verified
> 20	//   claim, NEVER from the request body. Cron callers (Bearer SB_SECRET_KEY) are rejected 403 — this endpoint
> 21	//   is arm-only (the drain/dispatch live in cadence-run, invoked by the tick).
> 22	//
> 23	// MANDATE OF INTEGRATION: extends the LIVING rail autopilot_plans (no parallel table, no new pg_cron job).
> 24	//   The live autopilot-cadence-cron tick routes due plans by plan_kind → cadence-run (FR-CAD-004).
> 25	
> 26	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 27	
> 28	const corsHeaders = {
> 29	  "Access-Control-Allow-Origin": "*",
> 30	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 31	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> 32	};
> 33	
> 34	const UUID_RE = /^[0-9a-fA-F-]{36}$/;
> 35	const DEFAULT_TZ = "America/Sao_Paulo";        // final fallback of the fuso cascade (FR-CAD-007)
> 36	const FREQUENCIES = new Set(["daily", "weekly", "monthly"]);
> 37	// Fatia 1 (OTD-CAD-011): X/Twitter is OUT of the cadence allowlist until the pay-per-use probe closes
> 38	// (Post-with-link = 45 mco, a Sovereign-gated Console action). Reject it at the edge with a 422.
> 39	const X_CHANNELS = new Set(["x", "twitter"]);
> 40	
> 41	// ── UTC re-arm calculator (FR-CAD-007 / FM-CAD-06) ───────────────────────────────────────────────────────
> 42	// The cron runs in GMT and NEVER carries a time-of-day preference: the subject's wall-clock time in its IANA
> 43	// timezone is converted to a UTC instant and stored in next_run_at. Deno has no tz library, so DST-correct
> 44	// conversion is done with Intl.DateTimeFormat offsets (the well-known zoned-time → UTC algorithm).
> 45	
> 46	// Offset (ms) such that local = utc + offset, at a given instant, for a timezone.
> 47	function tzOffsetMs(instant: Date, tz: string): number {
> 48	  const dtf = new Intl.DateTimeFormat("en-US", {
> 49	    timeZone: tz, hourCycle: "h23",
> 50	    year: "numeric", month: "2-digit", day: "2-digit",
> 51	    hour: "2-digit", minute: "2-digit", second: "2-digit",
> 52	  });
> 53	  const p: Record<string, string> = {};
> 54	  for (const { type, value } of dtf.formatToParts(instant)) p[type] = value;
> 55	  const asUTC = Date.UTC(+p.year, +p.month - 1, +p.day, +p.hour, +p.minute, +p.second);
> 56	  return asUTC - instant.getTime();
> 57	}
> 58	
> 59	// A wall-clock (y,mo,d,h,mi) in `tz` → the UTC instant it denotes (refined once across DST boundaries).
> 60	function zonedWallToUtc(y: number, mo: number, d: number, h: number, mi: number, tz: string): Date {
> 61	  const wallAsUtc = Date.UTC(y, mo, d, h, mi, 0);
> 62	  const off = tzOffsetMs(new Date(wallAsUtc), tz);
> 63	  let ts = wallAsUtc - off;
> 64	  const off2 = tzOffsetMs(new Date(ts), tz);
> 65	  if (off2 !== off) ts = wallAsUtc - off2;   // DST fold/gap refinement
> 66	  return new Date(ts);
> 67	}
> 68	
> 69	// The caller's local calendar date "today" in `tz`.
> 70	function localYmd(instant: Date, tz: string): { y: number; mo: number; d: number } {
> 71	  const dtf = new Intl.DateTimeFormat("en-US", {
> 72	    timeZone: tz, year: "numeric", month: "2-digit", day: "2-digit",
> 73	  });
> 74	  const p: Record<string, string> = {};
> 75	  for (const { type, value } of dtf.formatToParts(instant)) p[type] = value;
> 76	  return { y: +p.year, mo: +p.month - 1, d: +p.day };
> 77	}
> 78	
> 79	// ISO weekday 1=Mon..7=Sun for a calendar date (tz-independent given Y-M-D).
> 80	function isoDow(y: number, mo: number, d: number): number {
> 81	  const js = new Date(Date.UTC(y, mo, d)).getUTCDay();   // 0=Sun..6=Sat
> 82	  return js === 0 ? 7 : js;
> 83	}
> 84	
> 85	interface Recurrence {
> 86	  frequency: "daily" | "weekly" | "monthly";
> 87	  days: number[];        // weekly: ISO weekdays 1=Mon..7=Sun · monthly: days-of-month 1..31 · daily: ignored
> 88	  hours: number;         // 0..23
> 89	  minutes: number;       // 0..59, multiple of 5 (Knock semantics)
> 90	  tz: string;            // IANA
> 91	}
> 92	
> 93	// Next occurrence strictly after `from`, as a UTC Date. Scans ≤ 430 calendar days (covers monthly day-31).
> 94	function computeNextRunAt(rec: Recurrence, from: Date): Date | null {
> 95	  const { y, mo, d } = localYmd(from, rec.tz);
> 96	  const base = Date.UTC(y, mo, d);   // local "today" midnight as a pure-calendar anchor
> 97	  for (let i = 0; i <= 430; i++) {
> 98	    const cand = new Date(base + i * 86_400_000);
> 99	    const cy = cand.getUTCFullYear(), cmo = cand.getUTCMonth(), cd = cand.getUTCDate();
> 100	    let match = false;
> 101	    if (rec.frequency === "daily") match = true;
> 102	    else if (rec.frequency === "weekly") match = rec.days.includes(isoDow(cy, cmo, cd));
> 103	    else if (rec.frequency === "monthly") match = rec.days.includes(cd);
> 104	    if (!match) continue;
> 105	    const utc = zonedWallToUtc(cy, cmo, cd, rec.hours, rec.minutes, rec.tz);
> 106	    if (utc.getTime() > from.getTime()) return utc;
> 107	  }
> 108	  return null;
> 109	}
> 110	
> 111	function isValidTz(tz: unknown): tz is string {
> 112	  if (typeof tz !== "string" || !tz) return false;
> 113	  try { new Intl.DateTimeFormat("en-US", { timeZone: tz }); return true; } catch { return false; }
> 114	}
> 115	
> 116	Deno.serve(async (req) => {
> 117	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 118	  // Structured errors (PT-BR message for the UI toast; English code/vars per code standards).
> 119	  const json = (b: unknown, s = 200) =>
> 120	    new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 121	  const fail422 = (field: string, message: string) => json({ error: "validation_failed", field, message }, 422);
> 122	
> 123	  const url = Deno.env.get("SUPABASE_URL")!;
> 124	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 125	  const pubKey = (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!;
> 126	  const admin = createClient(url, serviceKey);
> 127	  const logHealth = (status: string, event?: string, metadata?: Record<string, unknown>) =>
> 128	    admin.from("infra_health_logs")
> 129	      .insert({ service: "spaces-cadence", status, ...(event ? { event } : {}), ...(metadata ? { metadata } : {}) })
> 130	      .then(() => {}, () => {});
> 131	
> 132	  try {
> 133	    // ── Identity (SDD §5.3): user JWT only. Cron key is rejected — arm is user-facing. ──────────────────────
> 134	    const authHeader = req.headers.get("Authorization");
> 135	    if (!authHeader?.startsWith("Bearer ")) return json({ error: "Unauthorized" }, 401);
> 136	    if (authHeader === `Bearer ${serviceKey}`) return json({ error: "Forbidden" }, 403); // cron path is cadence-run
> 137	
> 138	    const userClient = createClient(url, pubKey, { global: { headers: { Authorization: authHeader } } });
> 139	    const { data: { user }, error: authErr } = await userClient.auth.getUser();
> 140	    if (authErr || !user) return json({ error: "Unauthorized" }, 401);
> 141	    const userId = user.id;   // server-trusted from the verified claim, never from the body
> 142	
> 143	    const body = await req.json().catch(() => ({}));
> 144	
> 145	    // ── planId (optional): present ⇒ UPDATE (re-arm) an owner-scoped cadence plan; absent ⇒ INSERT a new one. ─
> 146	    const planId = typeof body?.planId === "string" ? body.planId : null;
> 147	    if (planId && !UUID_RE.test(planId)) return fail422("planId", "Identificador de plano inválido.");
> 148	
> 149	    // ── sourceAssetId: cadence subject (creative_assets.id, owner-scoped, existing asset ⇒ 0 mco keyless). ───
> 150	    const sourceAssetId = typeof body?.sourceAssetId === "string" ? body.sourceAssetId : null;
> 151	    if (!sourceAssetId || !UUID_RE.test(sourceAssetId)) {
> 152	      return fail422("sourceAssetId", "Selecione um criativo de origem para a cadência.");
> 153	    }
> 154	    const { data: asset } = await admin
> 155	      .from("creative_assets").select("id").eq("id", sourceAssetId).eq("user_id", userId).maybeSingle();
> 156	    if (!asset) return fail422("sourceAssetId", "Criativo de origem não encontrado.");
> 157	
> 158	    // ── recurrence: required + validated (computed in UTC on the server — FR-CAD-007). ──────────────────────
> 159	    const rec = body?.recurrence;
> 160	    if (!rec || typeof rec !== "object") return fail422("recurrence", "Configure a recorrência da cadência.");
> 161	    if (!FREQUENCIES.has(rec.frequency)) return fail422("recurrence.frequency", "Frequência inválida (diária, semanal ou mensal).");
> 162	    const hours = Number(rec.hours);
> 163	    if (!Number.isInteger(hours) || hours < 0 || hours > 23) return fail422("recurrence.hours", "A hora deve estar entre 0 e 23.");
> 164	    const minutes = Number(rec.minutes);
> 165	    if (!Number.isInteger(minutes) || minutes < 0 || minutes > 59) return fail422("recurrence.minutes", "Os minutos devem estar entre 0 e 59.");
> 166	    if (minutes % 5 !== 0) return fail422("recurrence.minutes", "Os minutos devem ser múltiplos de 5.");
> 167	    const days = Array.isArray(rec.days) ? rec.days.map((n: unknown) => Number(n)) : [];
> 168	    if (rec.frequency === "weekly") {
> 169	      if (days.length === 0 || days.some((d: number) => !Number.isInteger(d) || d < 1 || d > 7)) {
> 170	        return fail422("recurrence.days", "Selecione os dias da semana (1=segunda … 7=domingo).");
> 171	      }
> 172	    } else if (rec.frequency === "monthly") {
> 173	      if (days.length === 0 || days.some((d: number) => !Number.isInteger(d) || d < 1 || d > 31)) {
> 174	        return fail422("recurrence.days", "Selecione os dias do mês (1 a 31).");
> 175	      }
> 176	    }
> 177	
> 178	    // fuso cascade (FR-CAD-007): recurrence.tz → profiles.timezone → America/Sao_Paulo.
> 179	    let tz: string;
> 180	    if (isValidTz(rec.tz)) {
> 181	      tz = rec.tz;
> 182	    } else {
> 183	      let profileTz: string | null = null;
> 184	      try {
> 185	        const { data: prof } = await admin.from("profiles").select("timezone").eq("id", userId).maybeSingle();
> 186	        profileTz = (prof as { timezone?: string | null } | null)?.timezone ?? null;
> 187	      } catch { /* profiles.timezone best-effort — cascade falls through to default */ }
> 188	      tz = isValidTz(profileTz) ? profileTz! : DEFAULT_TZ;
> 189	    }
> 190	
> 191	    const recurrence: Recurrence = { frequency: rec.frequency, days, hours, minutes, tz };
> 192	
> 193	    // ── budget_cap_mco: NOT NULL, in mcoCoins (never USD); cadence requires > 0 (FR-CAD-011). ───────────────
> 194	    // NOTE: the live autopilot_plans column carries a DB CHECK (budget_cap_mco >= 12) from the viral base
> 195	    // migration (20260620120000). We validate > 0 per the FRD literal here; a value in 1..11 would still be
> 196	    // rejected by the DB CHECK and is mapped to a clean 422 on the write below (never a raw 500).
> 197	    const budgetCapMco = Number(body?.budget_cap_mco ?? body?.budgetCapMco);
> 198	    if (!Number.isInteger(budgetCapMco) || budgetCapMco <= 0) {
> 199	      return fail422("budget_cap_mco", "Defina um teto de orçamento em mcoCoins para a cadência (maior que zero).");
> 200	    }
> 201	
> 202	    // ── channel_allowlist: per-plan, non-empty; X excluded in Fatia 1 (OTD-CAD-011). ────────────────────────
> 203	    // TODO(FR-CAD-002 / OTD-CAD-011): the authoritative "auto-publish allowlist MINUS X" is not declared as a
> 204	    // constant in the sealed SDD/data-model (channel_allowlist is per-plan, not a hardcoded set). We enforce
> 205	    // non-empty + X-excluded here; the full channel_profiles-derived membership check is deferred to the
> 206	    // channel_profiles.cadence reader (FR-CAD-008) rather than invented as a literal list.
> 207	    const rawChannels = Array.isArray(body?.channel_allowlist) ? body.channel_allowlist
> 208	      : Array.isArray(body?.channelAllowlist) ? body.channelAllowlist : null;
> 209	    if (!rawChannels || rawChannels.length === 0 || rawChannels.some((c: unknown) => typeof c !== "string" || !c)) {
> 210	      return fail422("channel_allowlist", "Selecione ao menos um canal para a cadência.");
> 211	    }
> 212	    const channels = [...new Set((rawChannels as string[]).map((c) => c.toLowerCase()))];
> 213	    const blockedX = channels.filter((c) => X_CHANNELS.has(c));
> 214	    if (blockedX.length) return fail422("channel_allowlist", "O canal X/Twitter não está disponível nesta cadência.");
> 215	
> 216	    // ── optional fields (defaults mirror the migration column defaults). ────────────────────────────────────
> 217	    const quietHours = body?.quiet_hours ?? body?.quietHours ?? null;
> 218	    if (quietHours !== null && typeof quietHours !== "object") return fail422("quiet_hours", "Horário de silêncio inválido.");
> 219	    const overlapPolicy = body?.overlap_policy === "skip" || body?.overlapPolicy === "skip" ? "skip" : "skip"; // only 'skip' in Fatia 1
> 220	    const catchupWindow = typeof body?.catchup_window === "string" ? body.catchup_window
> 221	      : typeof body?.catchupWindow === "string" ? body.catchupWindow : "6 hours";
> 222	    const jitterRaw = Number(body?.jitter_seconds ?? body?.jitterSeconds ?? 0);
> 223	    const jitterSeconds = Number.isInteger(jitterRaw) && jitterRaw >= 0 ? jitterRaw : 0;
> 224	    const program = Array.isArray(body?.program) ? body.program : null;
> 225	    // Client-computed per-cycle projection (FR-CAD-011 — the inspector owns the per-channel mco projection;
> 226	    // the per-channel mco SSOT is not in this BoK doc). Echoed back for display; TODO move the projection
> 227	    // server-side once a per-channel cost table is declared. Never charged (0 mco at arm).
> 228	    const projectedCostMco = Number.isFinite(Number(body?.projectedCostMco)) ? Number(body.projectedCostMco) : 0;
> 229	
> 230	    // ── ARM next_run_at in UTC (FR-CAD-007). ────────────────────────────────────────────────────────────────
> 231	    const nextRun = computeNextRunAt(recurrence, new Date());
> 232	    if (!nextRun) return fail422("recurrence", "Não foi possível calcular a próxima execução para esta recorrência.");
> 233	    const nextRunAt = nextRun.toISOString();
> 234	
> 235	    // enabled (CadenceData.enabled): arming activates the plan so the live tick picks it up. Default true
> 236	    // (the operator clicked "Armar"); pass enabled:false to arm without activating.
> 237	    const isActive = body?.enabled !== false;
> 238	
> 239	    // Cadence-specific write payload (the columns the task/SDD enumerate).
> 240	    const cadenceCols = {
> 241	      plan_kind: "cadence" as const,
> 242	      recurrence,
> 243	      quiet_hours: quietHours,
> 244	      overlap_policy: overlapPolicy,
> 245	      catchup_window: catchupWindow,
> 246	      jitter_seconds: jitterSeconds,
> 247	      // The cadence SUBJECT lives in `program` — the seam cadence-run reads via extractSourceAssetId
> 248	      // (FR-CAD-005). Wrap the client steps as {source_asset_id, steps} so BOTH the INSERT and the
> 249	      // UPDATE/re-arm persist the subject (this object is used by both branches below).
> 250	      program: { source_asset_id: sourceAssetId, steps: program },
> 251	      channel_allowlist: channels,
> 252	      budget_cap_mco: budgetCapMco,
> 253	      next_run_at: nextRunAt,
> 254	      is_active: isActive,
> 255	    };
> 256	
> 257	    let resultPlanId: string;
> 258	
> 259	    if (planId) {
> 260	      // ── UPDATE path (re-arm): owner-scoped, cadence-only. RLS also enforces user_id = auth.uid(). ──────────
> 261	      const { data: upd, error: updErr } = await admin
> 262	        .from("autopilot_plans")
> 263	        .update(cadenceCols)
> 264	        .eq("id", planId).eq("user_id", userId).eq("plan_kind", "cadence")
> 265	        .select("id").maybeSingle();
> 266	      if (updErr) {
> 267	        if (updErr.code === "23514") return fail422("budget_cap_mco", "O teto de orçamento não atende ao mínimo do plano."); // DB CHECK
> 268	        logHealth("error", "cadence_arm_update_failed", { plan_id: planId, code: updErr.code });
> 269	        return json({ error: "arm_failed", detail: updErr.message }, 500);
> 270	      }
> 271	      if (!upd) return json({ error: "plan_not_found" }, 404);
> 272	      resultPlanId = upd.id;
> 273	    } else {
> 274	      // ── INSERT path: satisfy the legacy NOT NULL columns by REUSING the living rail (module dogma) with a
> 275	      // declared TODO — the sealed suite gives cadence a creative_assets subject but autopilot_plans still
> 276	      // carries viral-era NOT NULL columns that were NOT relaxed by 20260716120000_cadence_recurrence.sql:
> 277	      //   * mode NOT NULL CHECK IN('all_at_once','every_n_days') → 'every_n_days' (recurring) + interval_days=1
> 278	      //     placeholder (the real schedule is recurrence/next_run_at; interval_days is unused by cadence-run).
> 279	      //   * target_product_ids NOT NULL CHECK(len>=1) → [sourceAssetId]: the cadence SUBJECT id reuses this
> 280	      //     array (no source_asset_id column is declared in the SDD/data-model). TODO(FR-CAD-002/005): a
> 281	      //     follow-up migration should add a source_asset_id column OR relax target_product_ids for
> 282	      //     plan_kind='cadence'; until then the subject lives here and cadence-run resolves it owner-scoped.
> 283	      //   * platforms NOT NULL (subset CHECK was dropped by the cadence migration) → the channel_allowlist.
> 284	      // NONE of this is invention beyond the sealed rail: it is the minimal valid filler for pre-existing
> 285	      // NOT NULL columns, and plan_kind='cadence' isolates routing so autopilot-run never reads them.
> 286	      const name = typeof body?.name === "string" && body.name.trim() ? body.name.trim() : `Cadência ${sourceAssetId.slice(0, 8)}`;
> 287	      const { data: ins, error: insErr } = await admin
> 288	        .from("autopilot_plans")
> 289	        .insert({
> 290	          user_id: userId,
> 291	          name,
> 292	          mode: "every_n_days",
> 293	          interval_days: 1,                     // placeholder — cadence re-arm uses recurrence, not interval_days
> 294	          target_product_ids: [sourceAssetId],  // legacy NOT NULL filler; canonical subject is program.source_asset_id (read by cadence-run)
> 295	          platforms: channels,                  // subset CHECK dropped by the cadence migration
> 296	          ...cadenceCols,
> 297	        })
> 298	        .select("id").maybeSingle();
> 299	      if (insErr) {
> 300	        if (insErr.code === "23514") return fail422("budget_cap_mco", "O teto de orçamento não atende ao mínimo do plano."); // DB CHECK
> 301	        logHealth("error", "cadence_arm_insert_failed", { code: insErr.code });
> 302	        return json({ error: "arm_failed", detail: insErr.message }, 500);
> 303	      }
> 304	      if (!ins) return json({ error: "arm_failed" }, 500);
> 305	      resultPlanId = ins.id;
> 306	    }
> 307	
> 308	    // 0 mco at arm — profiles.mco_balance is untouched (FR-CAD-005 material invariant). No deduct_mco_coins.
> 309	    logHealth("healthy", "cadence_armed", { plan_id: resultPlanId, next_run_at: nextRunAt, channels });
> 310	    return json({
> 311	      plan_id: resultPlanId,
> 312	      next_run_at: nextRunAt,            // ISO UTC
> 313	      projected_cost_mco: projectedCostMco,
> 314	    });
> 315	  } catch (e) {
> 316	    logHealth("error", "cadence_arm_unhandled");
> 317	    return json({ error: e instanceof Error ? e.message : "unknown" }, 500);
> 318	  }
> 319	});
> 320	
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// cadence-run — spaces-cadence recurring-sequence executor (FR-CAD-006, the heart). verify_jwt=false.
> 2	// BoK SSOT (Lei 1 — no invention beyond the sealed suite):
> 3	//   docs/bok/spaces-cadence/05-sdd.md §3.2/§4/§5 (data flow + cadence-run contract + STRIDE/RLS)
> 4	//   docs/bok/spaces-cadence/06-data-model.md §2.1/§2.2/§2.4 (autopilot_plans ext · cadence_dispatches · sink)
> 5	//   docs/bok/spaces-cadence/07-process-flow.md PROC-CAD-03 (gate chain + recovery paths)
> 6	//   docs/bok/spaces-cadence/04-frd.md FR-CAD-006/007/008/009/011 (+ material acceptance)
> 7	//   migration 20260716120000_cadence_recurrence.sql (the APPLIED column/idempotency contract)
> 8	//
> 9	// Invoked by the LIVING tick `autopilot-cadence-cron` (NO new pg_cron job — FR-CAD-004) for plan_kind='cadence'.
> 10	// Identity: cron-only. Authorization === `Bearer SB_SECRET_KEY` (else 403). user_id is SERVER-TRUSTED from the
> 11	//   loaded plan ROW (autopilot_plans.user_id) — NEVER from the request body (SOP autopilot-cron-identity.md).
> 12	// Flow (PROC-CAD-03): drain plan FOR-UPDATE-SKIP-LOCKED-equivalent → resolve subject owner-scoped → gate chain
> 13	//   (quiet_hours in subject tz · frequency_cap vs channel_profiles.cadence · budget_cap_mco) → claim idempotency
> 14	//   in cadence_dispatches (ON CONFLICT DO NOTHING) → enqueue scheduled_posts (metadata.reshape sink) → atomic
> 15	//   deduct_mco_coins IF the step spends → re-arm next_run_at in UTC. The nó ENQUEUES; auto-publish drains/publishes.
> 16	//
> 17	// Mandate of integration: Cadence FITS the living rails and does NOT rebuild distribution. The sink is the LIVING
> 18	//   scheduled_posts contract as auto-publish ACTUALLY drains it (status='queued' + scheduled_at) — mirrored from
> 19	//   reshape-pillar's enqueue, NOT the SDD stub's publish_at/pending nomenclature (Lei 1: the sink is what
> 20	//   auto-publish reads). Divergence declared inline where it matters.
> 21	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 22	
> 23	const corsHeaders = {
> 24	  "Access-Control-Allow-Origin": "*",
> 25	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 26	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-autopilot-user-id",
> 27	};
> 28	const UUID_RE = /^[0-9a-fA-F-]{36}$/;
> 29	const DEFAULT_TZ = "America/Sao_Paulo";
> 30	// OTD-CAD-011: X (pay-per-use Post-with-URL = 45 mco) is OUT of Fatia 1. channel_allowlist should already exclude
> 31	// it (enforced at cadence-plan), but we defensively skip+log here so a stale plan can never fan out to X.
> 32	const FATIA1_EXCLUDED = new Set(["twitter", "x"]);
> 33	
> 34	// ── Timezone math (FR-CAD-007 / FM-CAD-06) — the cron runs in GMT; the subject's wall-clock preference is
> 35	// converted to UTC before it ever touches next_run_at. A self-contained calculator (the separately unit-tested
> 36	// FR-CAD-007 helper is a sibling slice; cadence-run needs a working impl now). ────────────────────────────────
> 37	interface TzParts { y: number; mo: number; d: number; h: number; mi: number; isoDow: number }
> 38	function partsInTz(instant: Date, tz: string): TzParts {
> 39	  const dtf = new Intl.DateTimeFormat("en-US", {
> 40	    timeZone: tz, year: "numeric", month: "2-digit", day: "2-digit",
> 41	    hour: "2-digit", minute: "2-digit", second: "2-digit", hour12: false, weekday: "short",
> 42	  });
> 43	  const p: Record<string, string> = {};
> 44	  for (const part of dtf.formatToParts(instant)) if (part.type !== "literal") p[part.type] = part.value;
> 45	  const dowMap: Record<string, number> = { Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6, Sun: 7 };
> 46	  return {
> 47	    y: Number(p.year), mo: Number(p.month), d: Number(p.day),
> 48	    h: Number(p.hour === "24" ? "0" : p.hour), mi: Number(p.minute),
> 49	    isoDow: dowMap[p.weekday] ?? 1,
> 50	  };
> 51	}
> 52	// Convert a wall-clock time in `tz` to the UTC instant (handles DST via the offset at that instant).
> 53	function zonedToUtc(y: number, mo: number, d: number, h: number, mi: number, tz: string): Date {
> 54	  const naiveUtc = Date.UTC(y, mo - 1, d, h, mi, 0);
> 55	  // offset(ms) = (what that wall time reads as if it were UTC) - (the same instant rendered in tz)
> 56	  const asIfUtc = partsInTz(new Date(naiveUtc), tz);
> 57	  const rendered = Date.UTC(asIfUtc.y, asIfUtc.mo - 1, asIfUtc.d, asIfUtc.h, asIfUtc.mi, 0);
> 58	  const offset = rendered - naiveUtc;
> 59	  return new Date(naiveUtc - offset);
> 60	}
> 61	interface Recurrence { frequency?: string; days?: number[]; hours?: number; minutes?: number; tz?: string }
> 62	// Next occurrence strictly AFTER `after`, at hours:minutes in tz, on an allowed day. Returns UTC Date or null.
> 63	function computeNextRunAtUtc(rec: Recurrence, tz: string, after: Date): Date | null {
> 64	  const freq = rec.frequency ?? "daily";
> 65	  const hours = Math.min(23, Math.max(0, Number(rec.hours ?? 9)));
> 66	  const minutes = Math.min(59, Math.max(0, Number(rec.minutes ?? 0)));
> 67	  const days = Array.isArray(rec.days) ? rec.days.map(Number).filter((n) => Number.isFinite(n)) : [];
> 68	  const startLocal = partsInTz(after, tz);
> 69	  // Walk up to ~14 months of candidate calendar days; the first whose UTC instant > after and whose day matches.
> 70	  for (let i = 0; i < 400; i++) {
> 71	    const cand = new Date(Date.UTC(startLocal.y, startLocal.mo - 1, startLocal.d + i, 12, 0, 0));
> 72	    const cp = partsInTz(cand, tz);
> 73	    let match = false;
> 74	    if (freq === "daily") match = true;
> 75	    else if (freq === "weekly") match = days.length === 0 || days.includes(cp.isoDow);
> 76	    else if (freq === "monthly") match = days.length === 0 || days.includes(cp.d);
> 77	    if (!match) continue;
> 78	    const utc = zonedToUtc(cp.y, cp.mo, cp.d, hours, minutes, tz);
> 79	    if (utc.getTime() > after.getTime()) return utc;
> 80	  }
> 81	  return null;
> 82	}
> 83	// Is `now` inside the plan's quiet window (subject tz)? quiet_hours = {start:'HH:MM', end:'HH:MM', days:int[]}.
> 84	function inQuietHours(quiet: unknown, tz: string, now: Date): boolean {
> 85	  const q = (quiet ?? null) as { start?: string; end?: string; days?: number[] } | null;
> 86	  if (!q?.start || !q?.end) return false;
> 87	  const np = partsInTz(now, tz);
> 88	  const qDays = Array.isArray(q.days) ? q.days : [];
> 89	  if (qDays.length > 0 && !qDays.includes(np.isoDow)) return false;
> 90	  const toMin = (s: string) => { const [h, m] = s.split(":").map(Number); return (h || 0) * 60 + (m || 0); };
> 91	  const nowMin = np.h * 60 + np.mi;
> 92	  const s = toMin(q.start), e = toMin(q.end);
> 93	  return s <= e ? (nowMin >= s && nowMin < e) : (nowMin >= s || nowMin < e); // wrap past midnight
> 94	}
> 95	async function sha256Hex(input: string): Promise<string> {
> 96	  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(input));
> 97	  return Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, "0")).join("");
> 98	}
> 99	
> 100	Deno.serve(async (req) => {
> 101	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 102	  const json = (b: unknown, s = 200) =>
> 103	    new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 104	
> 105	  const url = Deno.env.get("SUPABASE_URL")!;
> 106	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 107	  const admin = createClient(url, serviceKey);
> 108	  // Telemetry chokepoint (NFR-CAD-015). `event`/`metadata` allowlisted — never leak per-tenant PII into the
> 109	  // global-read infra_health_logs; plan_id/channel/counts only.
> 110	  const pulse = (status: string, event?: string, metadata?: Record<string, unknown>) =>
> 111	    admin.from("infra_health_logs").insert({ service: "spaces-cadence", status, event: event ?? null, metadata: metadata ?? {} })
> 112	      .then(() => {}, () => {});
> 113	
> 114	  try {
> 115	    // ── Identity: cron-only. NEVER a user-facing path (FR-CAD-006 / STRIDE §5.1). ─────────────────────────────
> 116	    if (req.headers.get("Authorization") !== `Bearer ${serviceKey}`) return json({ error: "Forbidden" }, 403);
> 117	
> 118	    const body = await req.json().catch(() => ({}));
> 119	    const planId = typeof body?.plan_id === "string" ? body.plan_id : null;
> 120	    if (!planId || !UUID_RE.test(planId)) return json({ error: "plan_id (uuid) required" }, 422);
> 121	
> 122	    // ── (1) DRAIN: load the plan (service-role). user_id is SERVER-TRUSTED from THIS ROW, never the body. ──────
> 123	    const { data: plan } = await admin
> 124	      .from("autopilot_plans")
> 125	      .select("id, user_id, project_id, name, plan_kind, is_active, next_run_at, recurrence, quiet_hours, overlap_policy, program, channel_allowlist, budget_cap_mco")
> 126	      .eq("id", planId).maybeSingle();
> 127	    if (!plan) return json({ error: "plan_not_found" }, 404);
> 128	    if (plan.plan_kind !== "cadence") return json({ error: "not_a_cadence_plan", plan_kind: plan.plan_kind }, 409);
> 129	    if (plan.is_active !== true) return json({ ok: false, reason: "inactive" }, 200);
> 130	
> 131	    const userId = plan.user_id as string;                 // ← the only trusted tenant identity (from the row)
> 132	    const rec = (plan.recurrence ?? {}) as Recurrence;
> 133	    const tz = (typeof rec.tz === "string" && rec.tz) ? rec.tz : await resolveSubjectTz(admin, userId);
> 134	    const occurrenceAt = plan.next_run_at ? new Date(plan.next_run_at as string) : new Date();
> 135	    const overlapPolicy = (plan.overlap_policy as string) ?? "skip";
> 136	
> 137	    // ── (2) RESOLVE SUBJECT owner-scoped (Fatia 1 = an existing creative_asset ⇒ 0 mco, keyless — OTD-CAD-002=A).
> 138	    // The subject asset id is carried by the plan's `program` jsonb (the CadenceData.sourceAssetId persisted by
> 139	    // cadence-plan / FR-CAD-005). Tolerant read: {source_asset_id} on the program object, or on step 0 of an array.
> 140	    // No source_asset_id COLUMN exists (migration 20260716120000 added none) — so `program` is the contract seam.
> 141	    const program = plan.program as Record<string, unknown> | Array<Record<string, unknown>> | null;
> 142	    const sourceAssetId = extractSourceAssetId(program);
> 143	    if (!sourceAssetId) {
> 144	      await pulse("degraded", "cadence_no_subject", { plan_id: planId });
> 145	      // Re-arm anyway so a mis-armed plan does not re-fire the same due instant every tick.
> 146	      await reArm(admin, planId, userId, rec, tz, occurrenceAt);
> 147	      // cadence-plan persists source_asset_id into program as {source_asset_id, steps} (FR-CAD-005 —
> 148	      // resolved). This branch stays as defense for a legitimately mis-armed plan (empty/legacy program).
> 149	      return json({ ok: false, reason: "no_subject" }, 200);
> 150	    }
> 151	    const { data: asset } = await admin
> 152	      .from("creative_assets").select("id, user_id")
> 153	      .eq("id", sourceAssetId).eq("user_id", userId).maybeSingle();   // hard tenant bind — a forged id → 0 rows
> 154	    if (!asset) {
> 155	      await pulse("degraded", "cadence_subject_not_owned", { plan_id: planId });
> 156	      await reArm(admin, planId, userId, rec, tz, occurrenceAt);
> 157	      return json({ ok: false, reason: "subject_not_owned" }, 200);
> 158	    }
> 159	
> 160	    // ── Overlap policy (FM-CAD-01): a prior-occurrence dispatch still in flight ⇒ skip THIS occurrence (never
> 161	    // stack), but still re-arm so the plan progresses. Idempotency (below) covers concurrent same-occurrence ticks.
> 162	    if (overlapPolicy === "skip") {
> 163	      const { count: inflight } = await admin
> 164	        .from("cadence_dispatches").select("id", { count: "exact", head: true })
> 165	        .eq("plan_id", planId).eq("user_id", userId)
> 166	        .in("status", ["queued", "publishing"])
> 167	        .lt("occurrence_at", occurrenceAt.toISOString());
> 168	      if ((inflight ?? 0) > 0) {
> 169	        await pulse("degraded", "cadence_overlap_skip", { plan_id: planId, inflight });
> 170	        await reArm(admin, planId, userId, rec, tz, occurrenceAt);
> 171	        return json({ ok: true, reason: "overlap_skip", dispatched: 0 }, 200);
> 172	      }
> 173	    }
> 174	
> 175	    // ── (3) GATE CHAIN — server-side, NEVER an LLM. ────────────────────────────────────────────────────────────
> 176	    const now = new Date();
> 177	    // Gate A — quiet_hours in the subject's timezone ⇒ HALT the whole cycle (suppress, do not reenqueue).
> 178	    if (inQuietHours(plan.quiet_hours, tz, now)) {
> 179	      await pulse("degraded", "cadence_halt_quiet_hours", { plan_id: planId });
> 180	      await reArm(admin, planId, userId, rec, tz, occurrenceAt);
> 181	      return json({ ok: true, reason: "quiet_hours", dispatched: 0 }, 200);
> 182	    }
> 183	
> 184	    // Channels for this cycle (per-plan allowlist MINUS X — OTD-CAD-011).
> 185	    const rawChannels = (Array.isArray(plan.channel_allowlist) ? plan.channel_allowlist : [])
> 186	      .filter((c): c is string => typeof c === "string" && c.length > 0);
> 187	    const channels = rawChannels.filter((c) => {
> 188	      if (FATIA1_EXCLUDED.has(c)) { void pulse("degraded", "cadence_channel_excluded_fatia1", { plan_id: planId, channel: c }); return false; }
> 189	      return true;
> 190	    });
> 191	    if (channels.length === 0) {
> 192	      await reArm(admin, planId, userId, rec, tz, occurrenceAt);
> 193	      return json({ ok: false, reason: "no_channels" }, 200);
> 194	    }
> 195	
> 196	    // Gate C setup — budget_cap_mco (in mcoCoins, never USD). Fatia 1 dispatch of an EXISTING asset costs 0 (keyless,
> 197	    // OTD-CAD-002=A); the debit rail below stays wired (deduct_mco_coins) for a future `generate` step. G7 remains a
> 198	    // CYCLE invariant, not a per-node one. budget_cap_mco is the ceiling for that (future) spend.
> 199	    const budgetCap = Number(plan.budget_cap_mco ?? 0);
> 200	    let spentThisCycle = 0;
> 201	
> 202	    // First-ever dispatch for this plan? (Mesh Connection Mandate — observation node on the first successful cycle.)
> 203	    const { count: priorDispatches } = await admin
> 204	      .from("cadence_dispatches").select("id", { count: "exact", head: true })
> 205	      .eq("plan_id", planId).eq("user_id", userId);
> 206	    const isFirstCycle = (priorDispatches ?? 0) === 0;
> 207	
> 208	    const results: Array<{ channel: string; status: string; dispatch_id?: string; scheduled_post_id?: string }> = [];
> 209	    let dispatched = 0;
> 210	
> 211	    for (let idx = 0; idx < channels.length; idx++) {
> 212	      const channel = channels[idx];
> 213	      try {
> 214	        // Gate B — frequency_cap vs channel_profiles.cadence (authoritative ceiling — OTD-CAD-008). Scope
> 215	        // (user_id, channel) on Fatia 1 (OTD-CAD-017=A). HALT (no reenqueue — Knock semantics).
> 216	        const cap = await frequencyCap(admin, userId, channel);
> 217	        if (cap) {
> 218	          const windowStart = capWindowStart(cap.target_per, tz, now);
> 219	          const { count: usedInWindow } = await admin
> 220	            .from("cadence_dispatches").select("id", { count: "exact", head: true })
> 221	            .eq("user_id", userId).eq("channel", channel)
> 222	            .neq("status", "failed")
> 223	            .gte("occurrence_at", windowStart.toISOString());
> 224	          if ((usedInWindow ?? 0) >= cap.count_max) {
> 225	            await pulse("degraded", "cadence_halt_freq_cap", { plan_id: planId, channel, cap: cap.count_max, target_per: cap.target_per });
> 226	            results.push({ channel, status: "halt_freq_cap" });
> 227	            continue;
> 228	          }
> 229	        }
> 230	
> 231	        // Gate — dedup/digest (user, channel, day): collapse N same-day due instants into 1 publication (FR-CAD-009).
> 232	        const dayStart = capWindowStart("day", tz, occurrenceAt);
> 233	        const { count: sameDay } = await admin
> 234	          .from("cadence_dispatches").select("id", { count: "exact", head: true })
> 235	          .eq("user_id", userId).eq("channel", channel)
> 236	          .neq("status", "failed")
> 237	          .gte("occurrence_at", dayStart.toISOString());
> 238	        if ((sameDay ?? 0) > 0) {
> 239	          results.push({ channel, status: "digest_collapsed" });
> 240	          continue;
> 241	        }
> 242	
> 243	        // Cost of THIS dispatch. Fatia 1 = existing asset ⇒ 0 (keyless). A future `generate` step would set this > 0.
> 244	        const dispatchCostMco = 0;
> 245	        // Gate C — budget_cap_mco. Only meaningful once dispatchCostMco > 0 (future generate step).
> 246	        if (dispatchCostMco > 0 && budgetCap > 0 && spentThisCycle + dispatchCostMco > budgetCap) {
> 247	          await pulse("degraded", "cadence_halt_budget_cap", { plan_id: planId, channel, budget_cap_mco: budgetCap });
> 248	          results.push({ channel, status: "halt_budget_cap" });
> 249	          continue;
> 250	        }
> 251	
> 252	        // ── (5→4 ordering) LEDGER-FIRST claim of the idempotency key, THEN enqueue the sink. Claiming BEFORE the
> 253	        // scheduled_posts INSERT is what makes a concurrent/retry tick a NO-OP instead of a double-post: whoever
> 254	        // loses the ON CONFLICT DO NOTHING never reaches the enqueue. (§5.2 / FM-CAD-01.)
> 255	        const stepIndex = idx;                              // one row per (occurrence, channel); step encodes channel ordinal
> 256	        const idempotencyKey = await sha256Hex(`${planId}:${stepIndex}:${occurrenceAt.toISOString()}:${channel}`);
> 257	        // ON CONFLICT DO NOTHING via the PARTIAL unique index (WHERE status<>'failed'): supabase-js .upsert cannot
> 258	        // target a partial index (Postgres can't infer one without its predicate), so we plain-INSERT and let the
> 259	        // index reject a live duplicate with SQLSTATE 23505 — identical effect, and it is the index (not a promise)
> 260	        // that enforces anti-double-post. A prior FAILED row does NOT block (predicate releases the key = retry).
> 261	        const { data: claim, error: claimErr } = await admin
> 262	          .from("cadence_dispatches")
> 263	          .insert({
> 264	            user_id: userId, plan_id: planId, step_index: stepIndex, occurrence_at: occurrenceAt.toISOString(),
> 265	            idempotency_key: idempotencyKey, channel, status: "queued",
> 266	          })
> 267	          .select("id").maybeSingle();
> 268	        if (claimErr) {
> 269	          if (claimErr.code === "23505") { results.push({ channel, status: "already_dispatched" }); continue; }  // NO-OP
> 270	          throw claimErr;
> 271	        }
> 272	        if (!claim?.id) { results.push({ channel, status: "already_dispatched" }); continue; }
> 273	        const dispatchId = claim.id as string;
> 274	
> 275	        // ── Atomic debit BEFORE the send, fail-closed (NFR-CAD-007 — cobrança só via RPC atômica, nunca client-side).
> 276	        // deduct_mco_coins(p_user_id, p_amount) raises on insufficient balance. Dormant at Fatia 1 (cost 0).
> 277	        if (dispatchCostMco > 0) {
> 278	          const { error: dErr } = await admin.rpc("deduct_mco_coins", { p_user_id: userId, p_amount: dispatchCostMco });
> 279	          if (dErr) {
> 280	            // Debit failed ⇒ release the idempotency key (status='failed') so the next tick may retry this occurrence.
> 281	            await admin.from("cadence_dispatches").update({ status: "failed", error: "insufficient_balance" }).eq("id", dispatchId);
> 282	            await pulse("degraded", "cadence_debit_failed", { plan_id: planId, channel, amount: dispatchCostMco });
> 283	            results.push({ channel, status: "debit_failed", dispatch_id: dispatchId });
> 284	            continue;
> 285	          }
> 286	          spentThisCycle += dispatchCostMco;
> 287	        }
> 288	
> 289	        // ── (4) DISPATCH: enqueue into the LIVING scheduled_posts sink (mirrors reshape-pillar:487 exactly).
> 290	        // auto-publish drains WHERE status='queued' AND scheduled_at<=now() (NOT publish_at/pending — that is the
> 291	        // sealed §7 nomenclature; the applied sink uses scheduled_at/queued). metadata.reshape carries the caption;
> 292	        // the asset image ref is NEVER placed in metadata (FMEA-011 — auto-publish resolves refs owner-scoped).
> 293	        //
> 294	        // TODO(FR-CAD-006 · auto-publish): a bare creative_assets.id has NO owner-scoped resolver branch in
> 295	        // auto-publish (it resolves channel_variant_id / space_publish_variant_id / carousel_render_id). Binding the
> 296	        // subject's IMAGE to the post requires either (a) an auto-publish branch that signs a creative_assets.id
> 297	        // owner-scoped, or (b) minting a space_publish_variant row. Until then this enqueues the CAPTION only.
> 298	        const content: Record<string, unknown> = { text: (plan.name as string) ?? "", channel };
> 299	        const { data: sp, error: spErr } = await admin
> 300	          .from("scheduled_posts")
> 301	          .insert({
> 302	            user_id: userId, content_id: null, campaign_id: null, social_account_id: null,
> 303	            platform: channel, scheduled_at: new Date().toISOString(), status: "queued",
> 304	            metadata: { reshape: { content, source_asset_id: sourceAssetId, channel }, cadence: { plan_id: planId, dispatch_id: dispatchId } },
> 305	          })
> 306	          .select("id").single();
> 307	        if (spErr || !sp?.id) {
> 308	          // Enqueue failed ⇒ release the key (retry next tick). If we debited, the failure is surfaced (a refund of a
> 309	          // generate step is deferred — Fatia 1 cost is 0, so no mint-hole here).
> 310	          await admin.from("cadence_dispatches").update({ status: "failed", error: spErr?.message ?? "enqueue_failed" }).eq("id", dispatchId);
> 311	          await pulse("error", "cadence_enqueue_failed", { plan_id: planId, channel });
> 312	          results.push({ channel, status: "enqueue_failed", dispatch_id: dispatchId });
> 313	          continue;
> 314	        }
> 315	        // Link the ledger row to the sink. status stays 'queued' — it becomes 'sent' ONLY on the status webhook
> 316	        // (PROC-CAD-05 / FM-CAD-05), never from a 202. external_usd_cost/cost_source are written on that reconcile.
> 317	        await admin.from("cadence_dispatches").update({ target_ref: sp.id }).eq("id", dispatchId);
> 318	        await pulse("healthy", "cadence_dispatch", { plan_id: planId, channel });
> 319	        results.push({ channel, status: "dispatched", dispatch_id: dispatchId, scheduled_post_id: sp.id });
> 320	        dispatched++;
> 321	      } catch (chErr) {
> 322	        await pulse("error", "cadence_channel_error", { plan_id: planId, channel });
> 323	        console.warn(`[cadence-run] channel ${channel} error:`, chErr instanceof Error ? chErr.message : chErr);
> 324	        results.push({ channel, status: "error" });
> 325	      }
> 326	    }
> 327	
> 328	    // ── (6) RE-ARM next_run_at in UTC (FR-CAD-007) — or deactivate if no future occurrence exists. ──────────────
> 329	    const armed = await reArm(admin, planId, userId, rec, tz, occurrenceAt);
> 330	
> 331	    // ── Mesh Connection Mandate: observation node on the FIRST successful cycle of the plan (best-effort — a mesh
> 332	    // hiccup NEVER blocks the money/dispatch path; failure is logged to infra_health_logs).
> 333	    if (isFirstCycle && dispatched > 0) {
> 334	      try {
> 335	        const { data: node } = await admin.from("mcorch_nodes").insert({
> 336	          user_id: userId, project_id: plan.project_id ?? null, node_type: "observation",
> 337	          title: `Cadence cycle · plan ${planId} · ${channels.join(",")}`,
> 338	          content: `Cadence ${plan.name ?? ""} dispatched ${dispatched} channel(s): ${channels.join(", ")}. budget_cap_mco=${budgetCap}.`,
> 339	        }).select("id").maybeSingle();
> 340	        if (node?.id) {
> 341	          await fetch(`${url}/functions/v1/embed-mcorch-node`, {
> 342	            method: "POST",
> 343	            headers: { Authorization: `Bearer ${serviceKey}`, "Content-Type": "application/json" },
> 344	            body: JSON.stringify({ node_id: node.id, content: `Cadence ${plan.name ?? ""} ${channels.join(" ")}` }),
> 345	          }).catch(() => {});
> 346	        }
> 347	      } catch (e) {
> 348	        await pulse("degraded", "cadence_mesh_observation_failed", { plan_id: planId });
> 349	        console.warn("[cadence-run] mesh observation skipped:", e instanceof Error ? e.message : e);
> 350	      }
> 351	    }
> 352	
> 353	    return json({ ok: true, plan_id: planId, dispatched, next_run_at: armed, results });
> 354	  } catch (e) {
> 355	    await pulse("error", "cadence_fatal");
> 356	    return json({ error: e instanceof Error ? e.message : "unknown" }, 500);
> 357	  }
> 358	});
> 359	
> 360	// ── helpers ──────────────────────────────────────────────────────────────────────────────────────────────────
> 361	
> 362	// Subject timezone cascade (FR-CAD-007): recurrence.tz (resolved by caller) → profiles.timezone → default.
> 363	// profiles.timezone may not exist yet (no migration adds it) — read defensively; a missing column degrades to
> 364	// the default rather than throwing. TODO(FR-CAD-007): add profiles.timezone (dead-data first-reader per SDD §2.5).
> 365	// deno-lint-ignore no-explicit-any
> 366	async function resolveSubjectTz(admin: any, userId: string): Promise<string> {
> 367	  try {
> 368	    const { data } = await admin.from("profiles").select("timezone").eq("id", userId).maybeSingle();
> 369	    const tz = (data as { timezone?: string } | null)?.timezone;
> 370	    if (typeof tz === "string" && tz.length > 0) return tz;
> 371	  } catch { /* column absent / read error → default */ }
> 372	  return DEFAULT_TZ;
> 373	}
> 374	
> 375	// The subject asset id lives in the plan's `program` jsonb (the seam cadence-plan writes — FR-CAD-005).
> 376	function extractSourceAssetId(program: unknown): string | null {
> 377	  if (!program) return null;
> 378	  const pick = (o: Record<string, unknown> | undefined) => {
> 379	    const v = o?.source_asset_id ?? o?.sourceAssetId;
> 380	    return typeof v === "string" && UUID_RE.test(v) ? v : null;
> 381	  };
> 382	  if (Array.isArray(program)) return pick(program[0] as Record<string, unknown>);
> 383	  return pick(program as Record<string, unknown>);
> 384	}
> 385	
> 386	// channel_profiles.cadence = {target_per: day|week|month, count_min, count_max, note}. Authoritative per-channel
> 387	// ceiling (OTD-CAD-008). Prefer the tenant's own row; fall back to a system row (user_id IS NULL). Multiple
> 388	// surfaces per channel → take the most permissive count_max (channel-level ceiling). Absent ⇒ no cap (allow).
> 389	// deno-lint-ignore no-explicit-any
> 390	async function frequencyCap(admin: any, userId: string, channel: string): Promise<{ count_max: number; target_per: string } | null> {
> 391	  const read = async (scopeOwn: boolean) => {
> 392	    let q = admin.from("channel_profiles").select("cadence").eq("channel", channel);
> 393	    q = scopeOwn ? q.eq("user_id", userId) : q.is("user_id", null);
> 394	    const { data } = await q;
> 395	    return (data ?? []) as Array<{ cadence: { target_per?: string; count_max?: number } | null }>;
> 396	  };
> 397	  let rows = await read(true);
> 398	  if (rows.length === 0) rows = await read(false);
> 399	  let best: { count_max: number; target_per: string } | null = null;
> 400	  for (const r of rows) {
> 401	    const c = r.cadence;
> 402	    if (!c || typeof c.count_max !== "number") continue;
> 403	    if (!best || c.count_max > best.count_max) best = { count_max: c.count_max, target_per: c.target_per ?? "day" };
> 404	  }
> 405	  return best;
> 406	}
> 407	
> 408	// Window start for a frequency-cap window, anchored to the subject timezone. 'day' → start of the local day;
> 409	// 'week'/'month' → rolling 7d/30d (pragmatic; a calendar-week/month refinement is a later slice).
> 410	function capWindowStart(targetPer: string, tz: string, ref: Date): Date {
> 411	  if (targetPer === "week") return new Date(ref.getTime() - 7 * 86_400_000);
> 412	  if (targetPer === "month") return new Date(ref.getTime() - 30 * 86_400_000);
> 413	  const p = partsInTz(ref, tz);
> 414	  return zonedToUtc(p.y, p.mo, p.d, 0, 0, tz); // start of the subject-local day
> 415	}
> 416	
> 417	// Re-arm next_run_at in UTC, or deactivate the plan when no future occurrence exists. Returns the ISO next_run_at
> 418	// (or null when deactivated). NEVER lets the cron carry a wall-clock preference — the subject time is converted.
> 419	// deno-lint-ignore no-explicit-any
> 420	async function reArm(admin: any, planId: string, userId: string, rec: Recurrence, tz: string, after: Date): Promise<string | null> {
> 421	  const next = computeNextRunAtUtc(rec, tz, after);
> 422	  if (next) {
> 423	    await admin.from("autopilot_plans").update({ next_run_at: next.toISOString() }).eq("id", planId).eq("user_id", userId);
> 424	    return next.toISOString();
> 425	  }
> 426	  await admin.from("autopilot_plans").update({ is_active: false }).eq("id", planId).eq("user_id", userId);
> 427	  return null;
> 428	}
> 429	
> ```

## 🤖 Claude *(10:05:40)*

<details>
<summary>💭 Thinking Process</summary>

I'm seeing how the scheduled_posts table gets populated when a plan runs—it creates a record with the user ID, platform, and scheduled timestamp, leaving the content and campaign IDs as null initially.

The metadata structure embeds the reshape data (the plan name and channel) along with cadence tracking info (plan_id and dispatch_id). The TODO comment reveals the actual constraint: without an owner-scoped resolver for creative_assets in auto-publish, the system can only enqueue the caption text, not the associated image. To include media, it would need either a new auto-publish branch that handles owner-scoped asset IDs or a space_publish_variant row to bridge the gap.

I need to check how auto-publish resolves media to understand what's actually happening downstream.

</details>


## 🤖 Claude *(10:05:40)*

Now the critical file — auto-publish, to understand exactly how it resolves media.

## 🤖 Claude *(10:05:40)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/auto-publish/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 2	
> 3	const corsHeaders = {
> 4	  "Access-Control-Allow-Origin": "*",
> 5	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 6	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-user-token",
> 7	};
> 8	
> 9	Deno.serve(async (req) => {
> 10	  if (req.method === "OPTIONS") {
> 11	    return new Response("ok", { headers: corsHeaders });
> 12	  }
> 13	
> 14	  try {
> 15	    const adminClient = createClient(
> 16	      Deno.env.get("SUPABASE_URL")!,
> 17	      (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!
> 18	    );
> 19	
> 20	    // Find all queued posts where scheduled_at <= now
> 21	    const { data: duePosts, error } = await adminClient
> 22	      .from("scheduled_posts")
> 23	      .select("*")
> 24	      .eq("status", "queued")
> 25	      .lte("scheduled_at", new Date().toISOString())
> 26	      .order("scheduled_at")
> 27	      .limit(50);
> 28	
> 29	    if (error) {
> 30	      console.error("Error fetching due posts:", error);
> 31	      return new Response(JSON.stringify({ error: error.message }), {
> 32	        status: 500,
> 33	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 34	      });
> 35	    }
> 36	
> 37	    if (!duePosts || duePosts.length === 0) {
> 38	      return new Response(JSON.stringify({ processed: 0, message: "No posts due" }), {
> 39	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 40	      });
> 41	    }
> 42	
> 43	    const results: Array<{ id: string; status: string; error?: string }> = [];
> 44	
> 45	    for (const post of duePosts) {
> 46	      try {
> 47	        // Mark as publishing
> 48	        await adminClient
> 49	          .from("scheduled_posts")
> 50	          .update({ status: "publishing" })
> 51	          .eq("id", post.id);
> 52	
> 53	        // Get the content body if content_id exists
> 54	        let contentText = "";
> 55	        if (post.content_id) {
> 56	          const { data: content } = await adminClient
> 57	            .from("content_library")
> 58	            .select("body, title")
> 59	            .eq("id", post.content_id)
> 60	            .single();
> 61	          contentText = content?.body || content?.title || "";
> 62	        }
> 63	
> 64	        if (!contentText) {
> 65	          contentText = `Post agendado para ${post.platform}`;
> 66	        }
> 67	
> 68	        // ── FR-PE-011: video transport gap. The scheduled post's content_id points at the TEXT row; the 9:16 render
> 69	        // (video-bridge.ts) lands as a SEPARATE content_library row (type='video', media_url = a path inside the
> 70	        // private `video-studio-assets` bucket — metadata.storage_bucket) sharing this post's campaign_id. Resolve
> 71	        // that sibling and sign it to a LONG-TTL URL so the URL survives Pinterest/IG's async fetch (a 1h signed URL
> 72	        // dies before the publish window). Pass it as content.video_url → publish-social's REELS/TikTok/YouTube/Pin
> 73	        // video branches. Text-only posts keep the plain-string path UNCHANGED (no campaign_id / no video sibling).
> 74	        let videoUrl: string | null = null;
> 75	        if (post.campaign_id) {
> 76	          try {
> 77	            const { data: vid } = await adminClient
> 78	              .from("content_library")
> 79	              .select("media_url, metadata")
> 80	              .eq("campaign_id", post.campaign_id)
> 81	              .eq("type", "video")
> 82	              .eq("status", "approved")
> 83	              .order("created_at", { ascending: false })
> 84	              .limit(1)
> 85	              .maybeSingle();
> 86	            const storageKey = vid?.media_url as string | undefined;
> 87	            if (storageKey) {
> 88	              const bucket = (vid?.metadata as { storage_bucket?: string } | null)?.storage_bucket || "video-studio-assets";
> 89	              if (/^https?:\/\//i.test(storageKey)) {
> 90	                videoUrl = storageKey; // already a public URL — pass through
> 91	              } else {
> 92	                // 6h TTL — outlives the async pull (cover/video fetch) on Pinterest/IG. Private bucket → re-sign on read.
> 93	                const { data: signed } = await adminClient.storage
> 94	                  .from(bucket)
> 95	                  .createSignedUrl(storageKey, 21600);
> 96	                videoUrl = signed?.signedUrl ?? null;
> 97	              }
> 98	            }
> 99	          } catch (e) {
> 100	            console.warn(`[auto-publish] video_url resolve skipped for post ${post.id}:`, e instanceof Error ? e.message : e);
> 101	          }
> 102	        }
> 103	
> 104	        // ── FR-CP-003 — prefer the reshaper's NATIVE variant over the generic derivation. ──
> 105	        // SECURITY (FMEA-011): the asset ref is NEVER trusted from scheduled_posts.metadata (a user can write their
> 106	        // OWN scheduled_posts.metadata, so signing a bucket/key from it with the service key would read ANY tenant's
> 107	        // private object). Instead resolve it from the server-trusted channel_variants row, filtered by the post's
> 108	        // OWNER (post.user_id) — that row is written service-role-only by the reshaper under the correct user_id.
> 109	        // Signing the per-row asset key HERE (fresh 6h URL) also fixes auto-publish's single-video-per-campaign
> 110	        // collision. SSOT: docs/bok/post-engine/13-sdd-reshaper-atomizer.md §5.3. Falls back to legacy when absent.
> 111	        let contentPayload: unknown = videoUrl ? { text: contentText, video_url: videoUrl } : contentText;
> 112	        const reshape = (post.metadata as { reshape?: { content?: Record<string, unknown>; channel_variant_id?: string; space_publish_variant_id?: string; carousel_render_id?: string } } | null)?.reshape;
> 113	        if (reshape?.content) {
> 114	          const c = reshape.content;
> 115	          const native: Record<string, unknown> = { text: typeof c.text === "string" ? c.text : contentText };
> 116	          // FR-SPACES-083 — surface discriminator (plain string, e.g. 'stories'): lets publish-social pick the
> 117	          // right IG media_type. Metadata-borne but INERT (it selects a container type, never an asset ref).
> 118	          if (typeof c.surface === "string") native.surface = c.surface.slice(0, 60);
> 119	          // Publication privacy discriminator (plain string: 'private' | 'unlisted' | 'public'). The SAME
> 120	          // security argument as `surface` above applies verbatim: metadata-borne but INERT — it selects an
> 121	          // enum on the platform API (YouTube status.privacyStatus / TikTok post_info.privacy_level), NEVER
> 122	          // an asset ref. Nothing is signed or read from Storage on its account, so FMEA-011 is untouched.
> 123	          // publish-social re-validates it against a CLOSED allowlist, so an unknown value degrades to the
> 124	          // pre-existing behaviour instead of reaching the Google API.
> 125	          if (typeof c.privacy === "string") native.privacy = c.privacy.slice(0, 20);
> 126	          // Attach the per-row asset ref resolved from an OWNER-SCOPED ledger row (server-trusted), NEVER from metadata.
> 127	          const attachAsset = async (bucket?: string, key?: string, kind?: string) => {
> 128	            if (!bucket || !key) return;
> 129	            let url: string | null = null;
> 130	            if (/^https?:\/\//i.test(key)) url = key;
> 131	            else { const { data: signed } = await adminClient.storage.from(bucket).createSignedUrl(key, 21600); url = signed?.signedUrl ?? null; }
> 132	            if (url) { if (kind === "video") native.video_url = url; else if (kind === "image") native.image_url = url; }
> 133	          };
> 134	          // FR-SPACES-079 (Amendment 22 — closes OTD-SPACES-044): scheduled IG CAROUSEL. carousel_render_id is a
> 135	          // GROUP MARKER, never an asset ref (FMEA-011 preserved): slides are resolved OWNER-SCOPED from
> 136	          // creative_assets with a hard tenant bind (a forged id of another tenant returns 0 rows → structured
> 137	          // failure, zero cross-tenant read), mirroring publish-space-carousel. URLs are signed FRESH here on
> 138	          // EVERY attempt (retries re-sign — an enqueue-time URL would outlive its 6h TTL). <2 resolved/signed
> 139	          // slides throws (→ retry/failed with a clear error) instead of falling into the single-image branch.
> 140	          if (typeof reshape.carousel_render_id === "string" && reshape.carousel_render_id) {
> 141	            const { data: slides } = await adminClient
> 142	              .from("creative_assets")
> 143	              .select("storage_bucket, storage_key")
> 144	              .eq("source_job_id", reshape.carousel_render_id)
> 145	              .eq("user_id", post.user_id)        // hard tenant bind — the marker alone grants nothing
> 146	              .eq("kind", "image")
> 147	              .order("storage_key", { ascending: true })
> 148	              .limit(10);                          // IG max
> 149	            const images: string[] = [];
> 150	            for (const s of slides ?? []) {
> 151	              const { data: signed } = await adminClient.storage
> 152	                .from(s.storage_bucket as string)
> 153	                .createSignedUrl(s.storage_key as string, 21600);
> 154	              if (signed?.signedUrl) images.push(signed.signedUrl);
> 155	            }
> 156	            if (images.length < 2) {
> 157	              throw new Error(`carousel_slides_unavailable (resolved ${slides?.length ?? 0}, signed ${images.length})`);
> 158	            }
> 159	            native.images = images;
> 160	          } else if (reshape.space_publish_variant_id) {
> 161	            // OTD-SPACES-036 — Spaces-origin publish: resolve the asset from space_publish_variants (dedicated table,
> 162	            // money-path/channel_variants untouched). Same tenant hard-bind as the pillar path.
> 163	            const { data: sv } = await adminClient
> 164	              .from("space_publish_variants")
> 165	              .select("asset_bucket, asset_key, asset_kind")
> 166	              .eq("id", reshape.space_publish_variant_id)
> 167	              .eq("user_id", post.user_id)        // hard tenant bind — a forged variant_id of another tenant returns nothing
> 168	              .maybeSingle();
> 169	            await attachAsset(sv?.asset_bucket as string | undefined, sv?.asset_key as string | undefined, sv?.asset_kind as string | undefined);
> 170	          } else if (reshape.channel_variant_id) {
> 171	            // FR-CP-003 pillar path (unchanged).
> 172	            const { data: cv } = await adminClient
> 173	              .from("channel_variants")
> 174	              .select("asset_bucket, asset_key, asset_kind")
> 175	              .eq("id", reshape.channel_variant_id)
> 176	              .eq("user_id", post.user_id)        // hard tenant bind — a forged variant_id of another tenant returns nothing
> 177	              .maybeSingle();
> 178	            await attachAsset(cv?.asset_bucket as string | undefined, cv?.asset_key as string | undefined, cv?.asset_kind as string | undefined);
> 179	          }
> 180	          if (Array.isArray(c.tweets)) native.thread = c.tweets;
> 181	          contentPayload = native;
> 182	        }
> 183	
> 184	        // Call publish-social
> 185	        const publishRes = await fetch(
> 186	          `${Deno.env.get("SUPABASE_URL")}/functions/v1/publish-social`,
> 187	          {
> 188	            method: "POST",
> 189	            headers: {
> 190	              "Content-Type": "application/json",
> 191	              Authorization: `Bearer ${(Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))}`,
> 192	            },
> 193	            body: JSON.stringify({
> 194	              platform: post.platform,
> 195	              content: contentPayload,
> 196	              social_account_id: post.social_account_id,
> 197	              scheduled_post_id: post.id,
> 198	              user_id: post.user_id,
> 199	            }),
> 200	          }
> 201	        );
> 202	
> 203	        if (publishRes.ok) {
> 204	          results.push({ id: post.id, status: "published" });
> 205	        } else {
> 206	          const errBody = await publishRes.json().catch(() => ({ error: "Unknown" }));
> 207	          const retryCount = (post.retry_count || 0) + 1;
> 208	          const maxRetries = post.max_retries || 3;
> 209	
> 210	          await adminClient
> 211	            .from("scheduled_posts")
> 212	            .update({
> 213	              status: retryCount >= maxRetries ? "failed" : "queued",
> 214	              retry_count: retryCount,
> 215	              error_message: errBody.error || "Publish failed",
> 216	            })
> 217	            .eq("id", post.id);
> 218	
> 219	          results.push({ id: post.id, status: "failed", error: errBody.error });
> 220	        }
> 221	      } catch (e) {
> 222	        const retryCount = (post.retry_count || 0) + 1;
> 223	        await adminClient
> 224	          .from("scheduled_posts")
> 225	          .update({
> 226	            status: retryCount >= (post.max_retries || 3) ? "failed" : "queued",
> 227	            retry_count: retryCount,
> 228	            error_message: e instanceof Error ? e.message : String(e),
> 229	          })
> 230	          .eq("id", post.id);
> 231	
> 232	        results.push({ id: post.id, status: "error", error: e instanceof Error ? e.message : String(e) });
> 233	      }
> 234	    }
> 235	
> 236	    return new Response(
> 237	      JSON.stringify({ processed: results.length, results }),
> 238	      { headers: { ...corsHeaders, "Content-Type": "application/json" } }
> 239	    );
> 240	  } catch (err) {
> 241	    console.error("auto-publish error:", err);
> 242	    return new Response(JSON.stringify({ error: err instanceof Error ? err.message : String(err) }), {
> 243	      status: 500,
> 244	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 245	    });
> 246	  }
> 247	});
> 248	
> ```

## 🤖 Claude *(10:05:49)*

<details>
<summary>💭 Thinking Process</summary>

I'm seeing how auto-publish resolves media through a specific sequence using `reshape`: first it handles carousel renders by looking up slides from creative assets using the source job ID to populate image data, then it processes space publish variants by fetching asset details and attaching either video URLs or other media based on the asset kind.

The problem is that cadence-run only writes the `metadata.reshape` object with content and source asset ID, but none of the three resolver IDs (carousel_render_id, space_publish_variant_id, or channel_variant_id) are actually present. This means auto-publish falls back to just setting the caption text with no media attached, which causes downstream failures when publish-social tries to push to YouTube or TikTok since those platforms require video content.

I need to dig into publish-space-asset to understand how to properly create a space_publish_variant, since that's the key to fixing this flow.

</details>


## 🤖 Claude *(10:05:49)*

Now publish-space-asset to understand how the space_publish_variant is minted.

## 🤖 Claude *(10:05:49)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-space-asset/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// publish-space-asset — seam that publishes a Spaces-origin creative asset to a social channel (FR-SPACES-031).
> 2	// ─────────────────────────────────────────────────────────────────────────────
> 3	// Destrava a Fatia B media-social do Spaces (OTD-SPACES-036 option b). Mirrors publish-channel-variant:
> 4	// user-JWT in → getUser (re-verify) → service-role writes to space_publish_variants (which has NO authenticated
> 5	// INSERT/UPDATE policy by design) + optional enqueue into scheduled_posts. The asset ref stored in the variant is
> 6	// resolved SERVER-SIDE from creative_assets bound to the caller (owner-scoped) — NEVER trusted from the client body
> 7	// (FMEA-011 / invariant I2). auto-publish then signs that server-trusted key and drives publish-social.
> 8	// SSOT: docs/processes/space-publish-variants.md + docs/bok/spaces-evolution/16-decision-otd-spaces-036-*.md.
> 9	
> 10	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 11	import { reframeToJpeg } from "../_shared/reframe.ts";
> 12	
> 13	const corsHeaders = {
> 14	  "Access-Control-Allow-Origin": "*",
> 15	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 16	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> 17	};
> 18	
> 19	const PLATFORMS = new Set(["linkedin", "instagram", "facebook", "twitter", "tiktok", "youtube", "pinterest"]);
> 20	
> 21	// Publication privacy levels — YouTube-native enum, reused as the ONE unified vocabulary across the rail.
> 22	// Only YouTube (privacyStatus) and TikTok (privacy_level → SELF_ONLY) honour it; for LinkedIn / Instagram /
> 23	// Pinterest it is a documented NO-OP (those APIs expose no private publish) — see publish-social.
> 24	const PRIVACY_LEVELS = new Set(["private", "unlisted", "public"]);
> 25	
> 26	// Keep only string-valued caption fields (+ string[] tweets). The caption is the caller's OWN content going to the
> 27	// caller's OWN social account — no cross-tenant trust boundary — but we still shape it to avoid storing arbitrary junk.
> 28	function sanitizeNativeText(raw: unknown): Record<string, unknown> {
> 29	  const src = (raw && typeof raw === "object") ? raw as Record<string, unknown> : {};
> 30	  const out: Record<string, unknown> = {};
> 31	  for (const k of ["caption", "title", "description", "body", "link"]) {
> 32	    if (typeof src[k] === "string") out[k] = (src[k] as string).slice(0, 5000);
> 33	  }
> 34	  if (Array.isArray(src.tweets)) {
> 35	    out.tweets = (src.tweets as unknown[]).filter((t) => typeof t === "string").slice(0, 25).map((t) => (t as string).slice(0, 5000));
> 36	  }
> 37	  return out;
> 38	}
> 39	
> 40	Deno.serve(async (req) => {
> 41	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 42	
> 43	  const json = (status: number, body: unknown) =>
> 44	    new Response(JSON.stringify(body), { status, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 45	
> 46	  try {
> 47	    const authHeader = req.headers.get("Authorization");
> 48	    if (!authHeader?.startsWith("Bearer ")) return json(401, { error: "Unauthorized" });
> 49	
> 50	    // Re-verify the caller (gateway already validated the JWT signature).
> 51	    const userClient = createClient(
> 52	      Deno.env.get("SUPABASE_URL")!,
> 53	      (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!,
> 54	      { global: { headers: { Authorization: authHeader } } },
> 55	    );
> 56	    const { data: { user } } = await userClient.auth.getUser();
> 57	    if (!user) return json(401, { error: "Unauthorized" });
> 58	
> 59	    const body = await req.json().catch(() => ({}));
> 60	    const sourceAssetId = typeof body.source_asset_id === "string" ? body.source_asset_id : "";
> 61	    const channel = typeof body.channel === "string" ? body.channel.trim().slice(0, 200) : "";
> 62	    const surface = typeof body.surface === "string" ? body.surface.trim().slice(0, 200) : "";
> 63	    const platform = typeof body.platform === "string" && PLATFORMS.has(body.platform) ? body.platform : null;
> 64	    // Publication privacy — CLOSED allowlist, YouTube-native enum. Inert string forwarded to publish-social
> 65	    // through scheduled_posts.metadata.reshape.content on the same rail as `surface`; an unknown value is
> 66	    // dropped here (null) rather than propagated.
> 67	    const requestedPrivacy = typeof body.privacy === "string" && PRIVACY_LEVELS.has(body.privacy) ? body.privacy : null;
> 68	    if (!sourceAssetId || !channel || !surface) {
> 69	      return json(400, { error: "missing_fields", action: "source_asset_id, channel e surface são obrigatórios." });
> 70	    }
> 71	    const wantPublish = body.publish === true;
> 72	
> 73	    const admin = createClient(
> 74	      Deno.env.get("SUPABASE_URL")!,
> 75	      (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
> 76	    );
> 77	
> 78	    // ── Resolve the source asset OWNER-SCOPED (server-trusted bucket/key; the .eq user_id is the tenant gate). ──
> 79	    const { data: asset } = await admin.from("creative_assets")
> 80	      .select("id, user_id, kind, storage_bucket, storage_key, width, height, file_size_bytes")
> 81	      .eq("id", sourceAssetId).eq("user_id", user.id).maybeSingle();
> 82	    if (!asset) return json(404, { error: "asset_not_found", action: "O asset não existe ou não é seu." });
> 83	    const assetKind = asset.kind === "video" ? "video" : asset.kind === "image" ? "image" : "none";
> 84	
> 85	    const nativeText = sanitizeNativeText(body.native_text);
> 86	    const nodeRunId = typeof body.node_run_id === "string" ? body.node_run_id.slice(0, 200) : null;
> 87	    const spaceId = typeof body.space_id === "string" ? body.space_id : null;
> 88	
> 89	    // ── FR-SPACES-081 (Amendment 23 — closes OTD-SPACES-043 for images): opt-in server-side reframe. ──
> 90	    // Target px come from the SEED channel_profiles row (server-trusted — never client px); the derived JPEG
> 91	    // becomes a lineage-tracked creative_asset (parent_asset_id) and the variant points at IT, so the existing
> 92	    // transport publishes pixel-parity with the preview. Every failure path FAILS OPEN to publish-as-is
> 93	    // (reframed:false + reframe_skip_reason) — the reframe never blocks a publish. Free rail (in-process
> 94	    // imagescript, OTD-CP-009): no mco, only sanity caps (source ≤15MB, target ≤2048px) to bound CPU/RAM.
> 95	    let publishBucket = asset.storage_bucket as string;
> 96	    let publishKey = asset.storage_key as string;
> 97	    let reframed = false;
> 98	    let reframeSkipReason: string | null = null;
> 99	    if (body.reframe === true) {
> 100	      if (assetKind !== "image") {
> 101	        reframeSkipReason = "not_an_image"; // video reframe rides the repurpose rail (OTD-SPACES-045)
> 102	      } else {
> 103	        try {
> 104	          // Tenant override first (lowest priority number), else the system seed row (user_id IS NULL).
> 105	          const { data: profs } = await admin.from("channel_profiles")
> 106	            .select("image, user_id, priority")
> 107	            .eq("channel", channel).eq("surface", surface).eq("is_active", true)
> 108	            .or(`user_id.is.null,user_id.eq.${user.id}`)
> 109	            .order("priority", { ascending: true }).limit(5);
> 110	          const spec = (profs ?? []).map((p) => p.image as { width?: number; height?: number } | null)
> 111	            .find((im) => Number(im?.width) > 0 && Number(im?.height) > 0);
> 112	          const tw = Number(spec?.width) || 0;
> 113	          const th = Number(spec?.height) || 0;
> 114	          if (!tw || !th) {
> 115	            reframeSkipReason = "no_image_spec_for_surface";
> 116	          } else if (tw > 2048 || th > 2048) {
> 117	            reframeSkipReason = "target_too_large";
> 118	          } else if (Number(asset.width) > 0 && Number(asset.height) > 0 && Number(asset.width) * Number(asset.height) > 6_000_000) {
> 119	            // Source-DIMENSION guard (uncatchable WORKER_RESOURCE_LIMIT prevention, witnessed 2026-07-17 on
> 120	            // roadmap-master 2480×8474 = 21MP in a ~1MB PNG): imagescript decodes the FULL source in-process, so a
> 121	            // highly-compressed but huge image passes the ≤15MB file cap yet OOMs the worker on decode — and the
> 122	            // runtime kills the worker BEFORE the try/catch can fail-open. Skip reframe above ~6MP → publish-as-is.
> 123	            reframeSkipReason = "source_dimensions_too_large";
> 124	          } else {
> 125	            const { data: blob } = await admin.storage.from(publishBucket).download(publishKey);
> 126	            if (!blob) throw new Error("source_download_failed");
> 127	            if (blob.size > 15 * 1024 * 1024) {
> 128	              reframeSkipReason = "source_too_large";
> 129	            } else {
> 130	              const jpeg = await reframeToJpeg(new Uint8Array(await blob.arrayBuffer()), tw, th);
> 131	              // channel/surface are client strings — slug-sanitize before they touch a storage PATH (service-role
> 132	              // writes bypass storage policies, so a '../' here could escape the owner prefix; DB usage is
> 133	              // parameterized and safe, the PATH is the boundary). The short hash disambiguates distinct
> 134	              // (channel,surface,target) tuples whose slugs collide (e.g. "a.b" vs "a_b") — same-tenant only,
> 135	              // but a collision would silently overwrite the earlier derived JPEG.
> 136	              const slug = (s: string) => s.toLowerCase().replace(/[^a-z0-9_]/g, "_").slice(0, 40);
> 137	              const rawTuple = new TextEncoder().encode(`${channel}|${surface}|${tw}x${th}`);
> 138	              const digest = new Uint8Array(await crypto.subtle.digest("SHA-256", rawTuple));
> 139	              const tupleHash = Array.from(digest.slice(0, 4)).map((x) => x.toString(16).padStart(2, "0")).join("");
> 140	              const outKey = `${user.id}/publish-reframe/${asset.id}-${slug(channel)}-${slug(surface)}-${tupleHash}.jpg`;
> 141	              const { error: upRfErr } = await admin.storage.from("canvas-assets")
> 142	                .upload(outKey, jpeg, { contentType: "image/jpeg", upsert: true });
> 143	              if (upRfErr) throw new Error(upRfErr.message);
> 144	              // Lineage row — select-first keeps re-calls idempotent. creative_assets HAS a UNIQUE on
> 145	              // (storage_bucket, storage_key) (creative_assets_uq_object), so a concurrent duplicate INSERT
> 146	              // fails 23505 → warn below → publish still proceeds (equivalent, never an overwrite).
> 147	              const { data: existing } = await admin.from("creative_assets")
> 148	                .select("id").eq("user_id", user.id).eq("storage_bucket", "canvas-assets").eq("storage_key", outKey).maybeSingle();
> 149	              if (!existing) {
> 150	                const { error: insErr } = await admin.from("creative_assets").insert({
> 151	                  user_id: user.id, kind: "image", storage_bucket: "canvas-assets", storage_key: outKey,
> 152	                  mime_type: "image/jpeg", file_size_bytes: jpeg.byteLength, width: tw, height: th,
> 153	                  parent_asset_id: asset.id, source_module: "spaces",
> 154	                  title: `reframe ${channel}/${surface}`,
> 155	                  metadata: { reframe: { channel, surface, target: { w: tw, h: th } } },
> 156	                });
> 157	                if (insErr) console.warn("[publish-space-asset] derived lineage insert failed (asset still published):", insErr.message);
> 158	              }
> 159	              publishBucket = "canvas-assets";
> 160	              publishKey = outKey;
> 161	              reframed = true;
> 162	            }
> 163	          }
> 164	        } catch (re) {
> 165	          reframeSkipReason = re instanceof Error ? re.message : String(re);
> 166	          console.warn(`[publish-space-asset] reframe fail-open (${channel}/${surface}):`, reframeSkipReason);
> 167	        }
> 168	      }
> 169	    }
> 170	
> 171	    // ── Upsert the variant (idempotent on user_id, source_asset_id, channel, surface). status/scheduled_post_id are
> 172	    //    NOT in the payload → on conflict they are NOT downgraded (a re-call never un-schedules a scheduled variant). ──
> 173	    const { data: variant, error: upErr } = await admin.from("space_publish_variants")
> 174	      .upsert({
> 175	        user_id: user.id,
> 176	        space_id: spaceId,
> 177	        node_run_id: nodeRunId,
> 178	        source_asset_id: asset.id,
> 179	        channel,
> 180	        surface,
> 181	        platform,
> 182	        native_text: nativeText,
> 183	        asset_kind: assetKind,
> 184	        asset_bucket: publishBucket,   // SERVER-TRUSTED (owner row, or the server-derived reframe of it) — never from the client
> 185	        asset_key: publishKey,
> 186	        asset_status: "ready",
> 187	      }, { onConflict: "user_id,source_asset_id,channel,surface" })
> 188	      .select("id, status, scheduled_post_id, platform").single();
> 189	    if (upErr || !variant) return json(500, { error: "upsert_failed", detail: upErr?.message });
> 190	
> 191	    // ── Draft mode (default): variant created/refreshed, publishable later. ──
> 192	    if (!wantPublish) {
> 193	      return json(200, {
> 194	        ok: true, space_publish_variant_id: variant.id, status: variant.status, platform: variant.platform,
> 195	        reframed, ...(reframeSkipReason ? { reframe_skip_reason: reframeSkipReason } : {}),
> 196	      });
> 197	    }
> 198	
> 199	    // ── Publish mode: enqueue into scheduled_posts (auto-publish resolves the asset owner-scoped from the variant). ──
> 200	    if (!variant.platform) {
> 201	      return json(422, { error: "surface_not_publishable", action: "Este canal/superfície não mapeia para uma rede publicável." });
> 202	    }
> 203	    if (variant.scheduled_post_id || variant.status === "scheduled" || variant.status === "published") {
> 204	      return json(409, { error: "already_enqueued", scheduled_post_id: variant.scheduled_post_id });
> 205	    }
> 206	
> 207	    const text = typeof nativeText.caption === "string" ? nativeText.caption
> 208	      : typeof nativeText.body === "string" ? nativeText.body
> 209	      : typeof nativeText.title === "string" ? nativeText.title : "";
> 210	    // Sovereign default — fail-SAFE, never fail-open: a YouTube publish with nothing wired from the UI goes out
> 211	    // PRIVATE. The last reversible step is taken autonomously; flipping it public stays a Sovereign act. This
> 212	    // makes a public post-by-forgotten-wiring structurally impossible. Other platforms keep the platform default.
> 213	    const privacy = requestedPrivacy ?? (variant.platform === "youtube" ? "private" : null);
> 214	    const content: Record<string, unknown> = { text, surface, channel };
> 215	    if (privacy) content.privacy = privacy;
> 216	    if (Array.isArray(nativeText.tweets)) content.tweets = nativeText.tweets;
> 217	
> 218	    const { data: sp, error: spErr } = await admin.from("scheduled_posts").insert({
> 219	      user_id: user.id, content_id: null, campaign_id: null,
> 220	      social_account_id: typeof body.social_account_id === "string" ? body.social_account_id : null,
> 221	      platform: variant.platform, scheduled_at: new Date().toISOString(), status: "queued",
> 222	      metadata: { reshape: { content, space_publish_variant_id: variant.id, surface, channel } },
> 223	    }).select("id").single();
> 224	    if (spErr || !sp) return json(500, { error: "enqueue_failed", detail: spErr?.message });
> 225	
> 226	    await admin.from("space_publish_variants")
> 227	      .update({ status: "scheduled", scheduled_post_id: sp.id }).eq("id", variant.id);
> 228	
> 229	    // Mesh Connection Mandate + telemetry (best-effort).
> 230	    admin.from("infra_health_logs").insert({ service: "publish-space-asset", status: "healthy" }).then(() => {}, () => {});
> 231	
> 232	    return json(200, {
> 233	      ok: true, space_publish_variant_id: variant.id, scheduled_post_id: sp.id,
> 234	      status: "scheduled", platform: variant.platform,
> 235	      reframed, ...(reframeSkipReason ? { reframe_skip_reason: reframeSkipReason } : {}),
> 236	    });
> 237	  } catch (e) {
> 238	    console.error("publish-space-asset error:", e);
> 239	    return json(500, { error: e instanceof Error ? e.message : "Unknown error" });
> 240	  }
> 241	});
> 242	
> ```

## 🤖 Claude *(10:06:07)*

<details>
<summary>💭 Thinking Process</summary>

So `publish-space-asset` with `publish:false` creates or updates a `space_publish_variant` row through an upsert operation keyed on user, source asset, channel, and surface—it pulls the asset owner info from `creative_assets` and stores the bucket, key, and kind server-side, returning the variant ID. When `publish:true`, it additionally queues the post into `scheduled_posts`...

The real fix for cadence-run is to write the `space_publish_variant_id` into the reshape metadata instead of just the source asset ID. I'm weighing two approaches: either cadence-run calls `publish-space-asset` with `publish:false` (but that needs a user JWT and cadence-run only has a service key), or cadence-run directly creates the `space_publish_variants` row via service-role since it already has admin access and resolves the asset owner. Option 2 is cleaner—cadence-run would just fetch the storage details and upsert the variant row itself, then reference that ID in the metadata.

The variant only needs `asset_bucket`, `asset_key`, and `asset_kind` for auto-publish to resolve the media; the `platform` from the variant isn't actually used by publish-social since cadence-run passes the platform directly from the scheduled post. So the variant's main role is just providing the owner-scoped media source for auto-publish to attach.

Now I need to check the actual `space_publish_variants` schema to see what columns and constraints exist, verify whether cadence-run needs `surface` for the minimal video fix, and confirm what publish-social requires for video handling on YouTube and TikTok. Let me find the migration and also check the `scheduled_posts` schema to see if there's a CHECK constraint on the platform values.

</details>


## 🤖 Claude *(10:06:07)*

Now let me find the `space_publish_variants` schema and the `scheduled_posts` platform constraint, plus how publish-social consumes video for youtube/tiktok.

## 🤖 Claude *(10:06:08)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; grep -rl \"space_publish_variants\" supabase/migrations/ | head; echo \"=== CADENCE MIGRATION ===\"; ls -la supabase/migrations/ | grep -iE \"cadence|space_publish|20260716\"",
  "description": "Find space_publish_variants and cadence migrations"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> supabase/migrations/20260710233000_space_publish_variants.sql
> === CADENCE MIGRATION ===
> -rw-rw-r-- 1 gcrUX  gcrUX   2239 Jun 23 01:24 20260623040000_viral_autopilot_cadence_cron.sql
> -rw-rw-r-- 1 gcrUX  gcrUX   1491 Jul  5 20:46 20260705120000_autopilot_video_cadence.sql
> -rw-rw-r-- 1 ubuntu ubuntu  5883 Jul 10 23:13 20260710233000_space_publish_variants.sql
> -rw-rw-r-- 1 ubuntu ubuntu 10866 Jul 15 15:35 20260716120000_cadence_recurrence.sql
> -rw-rw-r-- 1 ubuntu ubuntu  1854 Jul 16 14:12 20260716190000_pat_allowlist_swarm_read.sql
> -rw-rw-r-- 1 ubuntu ubuntu  9222 Jul 16 18:25 20260716210000_global_app_credentials_admin_tier.sql
> -rw-rw-r-- 1 ubuntu ubuntu  9917 Jul 16 19:04 20260716230000_content_provenance_columns.sql
> ```

## 🤖 Claude *(10:06:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; grep -rln \"space_publish_variants\" supabase/migrations/ | while read f; do echo \"### $f\"; done",
  "description": "List migrations touching space_publish_variants"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ### supabase/migrations/20260710233000_space_publish_variants.sql
> ```

## 🤖 Claude *(10:06:12)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260710233000_space_publish_variants.sql"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	-- Migration: space_publish_variants — media-social publish ledger for Spaces-origin assets (OTD-SPACES-036)
> 2	-- ─────────────────────────────────────────────────────────────────────────────
> 3	-- BoK SSOT: docs/bok/spaces-evolution/16-decision-otd-spaces-036-media-social-schema.md (option (b), GO 2026-07-09)
> 4	--           + docs/bok/spaces-evolution/15-amendment-social-publish-nodes.md (FR-SPACES-031 seam publish-space-asset).
> 5	-- SOP (Lei 2): docs/processes/space-publish-variants.md.
> 6	--
> 7	-- WHY A DEDICATED TABLE (not ALTER channel_variants): channel_variants is `pillar_run_id NOT NULL` (FK-logical to
> 8	-- pipeline_runs — the money-path truth that feeds collective_efficiency_ledger). A Spaces asset has no pillar run.
> 9	-- Option (b) keeps channel_variants/reshaper INTOUCHED (invariant I1) and mirrors its owner-scoped pattern here.
> 10	--
> 11	-- TENANCY (mirrors channel_variants 20260627150000 + creative_assets 20260625120000): SELECT/DELETE own only.
> 12	-- NO INSERT/UPDATE policy for authenticated ⇒ default-deny writes: the seam edge fn `publish-space-asset`
> 13	-- (service-role, bypasses RLS) is the ONLY writer, so user_id + the server-trusted asset ref can never be forged.
> 14	--
> 15	-- IDEMPOTENCY (invariant I3): UNIQUE(user_id, source_asset_id, channel, surface) — "one variant per (owner, source
> 16	-- asset, channel, surface)". Refinement over the ADR §3.1 sketch (which used node_run_id): node_run_id is a
> 17	-- client-supplied CANVAS NODE id (a string, NOT a UUID like pillar_run_id) ⇒ putting it in a GLOBAL unique risks a
> 18	-- cross-tenant collision (two tenants sharing a node id → the 2nd INSERT fails = DoS + leak). The (user_id,...) key
> 19	-- is tenant-scoped by construction and idempotent by the real intent. node_run_id kept only as lineage/audit.
> 20	--
> 21	-- Security posture: HARDENS (new RLS-isolated table, default-deny writes, no client-reachable SECURITY DEFINER).
> 22	-- MANDATORY /security-review before commit (FMEA-011 cross-tenant leak class).
> 23	
> 24	CREATE TABLE IF NOT EXISTS public.space_publish_variants (
> 25	  id                uuid PRIMARY KEY DEFAULT gen_random_uuid(),
> 26	  user_id           uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 27	  space_id          uuid,                          -- vm_canvas_projects.id origin (logical; nullable for loose asset)
> 28	  node_run_id       text,                          -- canvas node id — lineage/audit only, NOT an idempotency anchor
> 29	  source_asset_id   uuid NOT NULL
> 30	                      REFERENCES public.creative_assets(id) ON DELETE CASCADE,  -- owner-scoped source (server-resolved)
> 31	  channel           text NOT NULL,                 -- channel_profiles SPEC naming ('twitter_x' verbatim)
> 32	  surface           text NOT NULL,                 -- 'reels' | 'feed' | 'shorts' | 'video' | 'story' | ...
> 33	  platform          public.social_platform,        -- enum mapped for publishing; NULL = not directly publishable
> 34	  publish_path      text,
> 35	  native_text       jsonb NOT NULL DEFAULT '{}'::jsonb,   -- {caption|title|description|body|tweets[]|link}
> 36	  asset_kind        text,                          -- 'video' | 'image' | 'none'
> 37	  asset_bucket      text,                          -- per-row asset ref, SERVER-TRUSTED (auto-publish signs THIS)
> 38	  asset_key         text,
> 39	  asset_status      text NOT NULL DEFAULT 'ready'  -- Spaces asset already exists (no async render, unlike pillar)
> 40	    CONSTRAINT space_publish_variants_asset_status_chk CHECK (asset_status IN
> 41	      ('pending','ready','reused_master','gap')),
> 42	  status            text NOT NULL DEFAULT 'draft'
> 43	    CONSTRAINT space_publish_variants_status_chk CHECK (status IN
> 44	      ('draft','scheduled','published','skipped','failed')),
> 45	  scheduled_post_id uuid,                          -- set once enqueued (guards double-enqueue)
> 46	  created_at        timestamptz NOT NULL DEFAULT timezone('utc'::text, now()),
> 47	  updated_at        timestamptz NOT NULL DEFAULT timezone('utc'::text, now()),
> 48	  -- Idempotency: one variant per (owner, source asset, channel, surface). publish-space-asset UPSERTs on this.
> 49	  CONSTRAINT space_publish_variants_uq UNIQUE (user_id, source_asset_id, channel, surface)
> 50	);
> 51	
> 52	ALTER TABLE public.space_publish_variants ENABLE ROW LEVEL SECURITY;
> 53	
> 54	-- SELECT own; DELETE own. NO INSERT/UPDATE policy ⇒ writes are service-role-only (publish-space-asset).
> 55	CREATE POLICY "space_publish_variants read own" ON public.space_publish_variants
> 56	  FOR SELECT USING (auth.uid() = user_id);
> 57	CREATE POLICY "space_publish_variants delete own" ON public.space_publish_variants
> 58	  FOR DELETE USING (auth.uid() = user_id);
> 59	
> 60	CREATE TRIGGER tr_update_space_publish_variants_updated_at
> 61	  BEFORE UPDATE ON public.space_publish_variants
> 62	  FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();
> 63	
> 64	CREATE INDEX IF NOT EXISTS idx_space_publish_variants_user
> 65	  ON public.space_publish_variants (user_id, created_at DESC);
> 66	CREATE INDEX IF NOT EXISTS idx_space_publish_variants_draft
> 67	  ON public.space_publish_variants (status) WHERE status = 'draft';
> 68	CREATE INDEX IF NOT EXISTS idx_space_publish_variants_asset
> 69	  ON public.space_publish_variants (source_asset_id);
> 70	CREATE INDEX IF NOT EXISTS idx_space_publish_variants_sched
> 71	  ON public.space_publish_variants (scheduled_post_id) WHERE scheduled_post_id IS NOT NULL;
> 72	
> 73	COMMENT ON TABLE public.space_publish_variants IS
> 74	  'Media-social publish ledger for Spaces-origin assets (OTD-SPACES-036 option b). Mirrors channel_variants '
> 75	  'owner-scoped pattern but keyed by (user_id, source_asset_id, channel, surface) — NOT pillar_run_id, so the '
> 76	  'money-path (channel_variants/reshaper) stays intact (I1). SELECT/DELETE own; writes service-role-only '
> 77	  '(publish-space-asset). auto-publish resolves the asset from asset_bucket/asset_key by user_id (FMEA-011-safe).';
> 78	
> ```

## 🤖 Claude *(10:06:24)*

<details>
<summary>💭 Thinking Process</summary>

Looking at the space_publish_variants schema, I can see the platform field maps to a social_platform enum with NULL values for non-publishable content, the channel field references channel_profiles using their naming convention like 'twitter_x', and there's a surface field covering different content types like reels, feed, shorts, and story. The asset_kind field specifies whether the variant is video, image, or none, with a unique constraint across user_id, source_asset_id, channel, and surface.

For the auto-publish flow, when cadence-run creates a variant, it only needs to provide the asset_bucket, asset_key, and asset_kind fields since auto-publish reads just those three. The channel comes from the channel_allowlist in cadence-plan, which uses lowercase names like "youtube", "tiktok", "instagram", "linkedin", "pinterest", and "facebook". There's a potential naming mismatch here — the channel_profiles SPEC uses names like 'twitter_x' and 'instagram_reels', but cadence-plan's channel_allowlist uses simpler names like "instagram" and "twitter". I need to verify how these map to the platform enum that publish-social expects.

</details>


## 🤖 Claude *(10:06:24)*

Now publish-social — how it handles video for youtube/tiktok/instagram, and what triggers `*_no_video`.

## 🤖 Claude *(10:06:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; grep -nE \"_no_video|no_video|video_url|surface|media_type|reels|shorts|function publish|case \\\"|platform ===|=== \\\"youtube|=== \\\"tiktok|=== \\\"instagram\" supabase/functions/publish-social/index.ts | head -80",
  "description": "Scan publish-social for video/no_video branches"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 38:    // content.surface (FR-SPACES-083): it selects an enum on the platform API and is NEVER an asset ref —
> 47:    // those APIs have no private-publish surface. The UI must NOT offer privacy for those networks; doing
> 146:    if (platform === "linkedin") {
> 214:    } else if (platform === "instagram") {
> 216:      // NOT graph.facebook.com (that base needs a Page token). video_url → REELS (Fatia 2: vídeo do ecossistema
> 224:      // video-repurpose Fatia 3 — a SET of images → a native CAROUSEL post (media_type=CAROUSEL): N child image
> 242:          body: JSON.stringify({ media_type: "CAROUSEL", children: childIds.join(","), caption: content.text || "", access_token: account.access_token }),
> 253:      const videoUrl = content.video_url;
> 254:      // FR-SPACES-083 (Amendment 24) — IG STORIES: same container→publish flow, media_type=STORIES; the surface
> 255:      // discriminator rides content.surface (copied server-side by auto-publish from the reshape row, never a
> 259:      const isStory = (content.surface === "story" || content.surface === "stories") && (videoUrl || content.image_url);
> 267:              ? { media_type: "STORIES", ...(videoUrl ? { video_url: videoUrl } : { image_url: content.image_url }), access_token: account.access_token }
> 269:                ? { media_type: "REELS", video_url: videoUrl, caption: content.text || content, access_token: account.access_token }
> 309:    } else if (platform === "facebook") {
> 310:      // CP-010 — image (link_card surface → Page photo) OR text feed. FB Reels video is deferred (OTD-CP-010).
> 333:    } else if (platform === "twitter") {
> 395:    } else if (platform === "tiktok") {
> 398:      // publishing needs no client_secret. Mirrors the IG REELS create→poll→publish shape. video_url from payload.
> 400:      const videoUrl = content.video_url;
> 402:        pulse("degraded", "tiktok_no_video");
> 528:    } else if (platform === "youtube") {
> 531:      const videoUrl = content.video_url;
> 533:        pulse("degraded", "youtube_no_video");
> 598:        pulse("error", "youtube_no_video_id");
> 625:    } else if (platform === "pinterest") {
> 627:      // pin/board/media REST; the multipart upload itself carries NO Authorization (presigned S3 POST). video_url
> 630:      const videoUrl = content.video_url;
> 673:        body: JSON.stringify({ media_type: "video" }),
> 749:        // CP-010 — standard IMAGE pin (standard_pin surface): Pinterest fetches the public/signed image URL async.
> 783:    const platformLabel = platform === "instagram" ? "Instagram" : platform === "linkedin" ? "LinkedIn" : platform;
> ```

## 🤖 Claude *(10:06:29)*

<details>
<summary>💭 Thinking Process</summary>

I need to check what the TikTok and YouTube branches expect from the content object, specifically whether they require the video_url field, and understand what happens in the no_video path.

</details>


## 🤖 Claude *(10:06:29)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-social/index.ts",
  "offset": 395,
  "limit": 50
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 395	    } else if (platform === "tiktok") {
> 396	      // TikTok Content Posting API — Direct Post, FILE_UPLOAD (the Supabase signed URL does NOT pass the
> 397	      // PULL_FROM_URL domain-ownership check, so we transfer the bytes ourselves). User access_token only —
> 398	      // publishing needs no client_secret. Mirrors the IG REELS create→poll→publish shape. video_url from payload.
> 399	      const TIKTOK_BASE = "https://open.tiktokapis.com";
> 400	      const videoUrl = content.video_url;
> 401	      if (!videoUrl) {
> 402	        pulse("degraded", "tiktok_no_video");
> 403	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 404	      }
> 405	
> 406	      // (1) Pre-flight creator_info — pick a privacy_level that the (possibly unaudited) account actually allows.
> 407	      const ciRes = await fetch(`${TIKTOK_BASE}/v2/post/publish/creator_info/query/`, {
> 408	        method: "POST",
> 409	        headers: {
> 410	          Authorization: `Bearer ${account.access_token}`,
> 411	          "Content-Type": "application/json; charset=UTF-8",
> 412	        },
> 413	      });
> 414	      const creatorInfo = await ciRes.json();
> 415	      if (!ciRes.ok) {
> 416	        console.error("TikTok creator_info error:", ciRes.status, creatorInfo);
> 417	        pulse("error", "tiktok_creator_info_failed", { status: ciRes.status });
> 418	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 419	      }
> 420	      const privacyOptions: string[] = creatorInfo?.data?.privacy_level_options ?? [];
> 421	      // Prefer public when available (post-audit). Otherwise an UNAUDITED client can ONLY post as
> 422	      // SELF_ONLY — TikTok rejects FOLLOWER_OF_CREATOR / MUTUAL_FOLLOW_FRIENDS with
> 423	      // `unaudited_client_can_only_post_to_private_accounts` (proven 2026-06-27). So fall back to
> 424	      // SELF_ONLY explicitly, NOT to privacyOptions[0] (which is FOLLOWER_OF_CREATOR on a private acct).
> 425	      // When the caller asked for `private`, invert the preference (SELF_ONLY first) — the rest of the
> 426	      // negotiation with the options the API actually returned stays byte-identical.
> 427	      const privacyLevel =
> 428	        (privacy === "private"
> 429	          ? privacyOptions.find((p) => p === "SELF_ONLY")
> 430	          : privacyOptions.find((p) => p === "PUBLIC_TO_EVERYONE")) ??
> 431	        privacyOptions.find((p) => p === "SELF_ONLY") ??
> 432	        privacyOptions[0] ??
> 433	        "SELF_ONLY";
> 434	
> 435	      // Fetch the MP4 bytes once (FILE_UPLOAD requires the exact size up-front).
> 436	      const mp4Res = await fetchPublicUrl(videoUrl);
> 437	      if (!mp4Res.ok) {
> 438	        console.error("TikTok video fetch error:", mp4Res.status);
> 439	        pulse("error", "tiktok_video_fetch_failed", { status: mp4Res.status });
> 440	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 441	      }
> 442	      const videoBytes = new Uint8Array(await mp4Res.arrayBuffer());
> 443	      const videoSize = videoBytes.byteLength;
> 444	      // Single-chunk transfer (HyperFrames clips are well under the 64MB chunk ceiling / <128MB final).
> ```

## 🤖 Claude *(10:06:30)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-social/index.ts",
  "offset": 528,
  "limit": 20
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 528	    } else if (platform === "youtube") {
> 529	      // YouTube Data API v3 videos.insert — resumable upload (no remote ingest → fetch the signed bytes, then
> 530	      // PUT). User access_token only (publishing needs no client_secret). Shorts is implicit (9:16 + ≤3min).
> 531	      const videoUrl = content.video_url;
> 532	      if (!videoUrl) {
> 533	        pulse("degraded", "youtube_no_video");
> 534	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 535	      }
> 536	      const mp4Res = await fetchPublicUrl(videoUrl);
> 537	      if (!mp4Res.ok) {
> 538	        console.error("YouTube video fetch error:", mp4Res.status);
> 539	        pulse("error", "youtube_video_fetch_failed", { status: mp4Res.status });
> 540	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 541	      }
> 542	      const videoBytes = new Uint8Array(await mp4Res.arrayBuffer());
> 543	      const videoSize = videoBytes.byteLength;
> 544	
> 545	      // (1) Initiate the resumable session.
> 546	      const initRes = await fetch(
> 547	        "https://www.googleapis.com/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
> ```

## 🤖 Claude *(10:06:45)*

<details>
<summary>💭 Thinking Process</summary>

I see the root cause now—both YouTube and TikTok are checking for `content.video_url`, and when it's missing they trigger the `*_no_video` failure. The solution is to have cadence-run pass the video URL through to publish-social by writing a `space_publish_variant_id` in the metadata reshape step during the auto-publish flow.

When auto-publish resolves that variant owner-scoped and attaches the asset, it sets `native.video_url` since the asset kind is video. For the channel-to-platform mapping, cadence's `channel_allowlist` contains lowercase platform strings (youtube, tiktok, instagram, linkedin, facebook, pinterest), and auto-publish passes these directly as the `platform` field to publish-social, which branches on exact string matches. The minimal fix just needs cadence-run to create the variant with the cadence channel value and a non-null surface—the variant's channel and surface don't need to match the channel_profiles spec naming exactly.

Now I need to verify whether `scheduled_posts.platform` actually accepts these platform strings and check what surface value the Instagram branch requires, plus confirm whether surface is even needed for YouTube and TikTok or if it can just be a sensible default per channel.

</details>


## 🤖 Claude *(10:06:45)*

Let me verify the `scheduled_posts.platform` constraint and the `social_platform` enum values, plus how the autopilot-cadence-cron routes plans.

## 🤖 Claude *(10:06:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"=== scheduled_posts platform constraint ===\"; grep -rniE \"scheduled_posts\" supabase/migrations/*.sql | grep -iE \"platform|CHECK|CREATE TABLE\" | head -20; echo; echo \"=== social_platform enum ===\"; grep -rniE \"type social_platform|social_platform AS ENUM|CREATE TYPE .*social_platform\" supabase/migrations/*.sql | head",
  "description": "Find scheduled_posts platform and social_platform enum"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === scheduled_posts platform constraint ===
> supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql:158:CREATE TABLE public.scheduled_posts (
> supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql:298:CREATE POLICY "Users can create posts" ON public.scheduled_posts FOR INSERT WITH CHECK (auth.uid() = user_id);
> supabase/migrations/20260626130000_publication_metrics.sql:59:CREATE INDEX IF NOT EXISTS scheduled_posts_platform_post_id_idx
> supabase/migrations/20260626130000_publication_metrics.sql:60:  ON public.scheduled_posts (platform_post_id);
> 
> === social_platform enum ===
> supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql:12:CREATE TYPE public.social_platform AS ENUM ('linkedin', 'instagram', 'facebook', 'twitter', 'tiktok', 'youtube', 'pinterest', 'wordpress');
> ```

## 🤖 Claude *(10:06:48)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-cadence-cron/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// autopilot-cadence-cron — Viral Autopilot pg_cron driver (FR-VA-005). verify_jwt=false.
> 2	// SOP: docs/processes/autopilot-cron-identity.md.
> 3	//
> 4	// Service-role driver (mirrors nurture-cron): self-checks Authorization === Bearer SB_SECRET_KEY, scans ACTIVE
> 5	// plans whose next_run_at has passed, and fans out to autopilot-run with the SERVER-TRUSTED user_id taken from
> 6	// the plan row (NEVER a request body). Each plan's spend is gated by begin_autopilot_cycle's caps inside
> 7	// autopilot-run. The pg_cron SCHEDULE that invokes this function is wired at activation time (Sovereign action).
> 8	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 9	
> 10	const corsHeaders = {
> 11	  "Access-Control-Allow-Origin": "*",
> 12	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 13	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> 14	};
> 15	const MAX_PER_RUN = 50;   // cap per tick — no silent unbounded fan-out (logged if hit)
> 16	const CONCURRENCY = 6;    // wall-clock bound (mirrors nurture-cron)
> 17	
> 18	Deno.serve(async (req) => {
> 19	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 20	  const json = (b: unknown, s = 200) =>
> 21	    new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 22	
> 23	  const url = Deno.env.get("SUPABASE_URL")!;
> 24	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 25	  // Only the service-role holder (pg_cron presenting the Vault key) may run the cron.
> 26	  if (req.headers.get("Authorization") !== `Bearer ${serviceKey}`) return json({ error: "Forbidden" }, 403);
> 27	  const admin = createClient(url, serviceKey);
> 28	  const log = (status: string) =>
> 29	    admin.from("infra_health_logs").insert({ service: "autopilot-cadence-cron", status }).then(() => {}, () => {});
> 30	
> 31	  try {
> 32	    // due = active plans whose next_run_at has passed (served by the autopilot_plans_due_idx partial index).
> 33	    // plan_kind routes the dispatch (FR-CAD-004): 'cadence' → cadence-run | else 'viral' → autopilot-run.
> 34	    const { data: due, error } = await admin
> 35	      .from("autopilot_plans")
> 36	      .select("id, user_id, plan_kind")
> 37	      .eq("is_active", true)
> 38	      .not("next_run_at", "is", null)
> 39	      .lte("next_run_at", new Date().toISOString())
> 40	      .order("next_run_at", { ascending: true })
> 41	      .limit(MAX_PER_RUN);
> 42	    if (error) throw error;
> 43	    const list = (due ?? []) as Array<{ id: string; user_id: string; plan_kind: string }>;
> 44	    if (list.length === 0) { log("healthy"); return json({ status: "ok", due: 0, dispatched: 0, aborted: 0, errors: 0 }); }
> 45	
> 46	    const tally = { dispatched: 0, aborted: 0, errors: 0 };
> 47	    const one = async (p: { id: string; user_id: string; plan_kind: string }) => {
> 48	      try {
> 49	        // Route by plan_kind (FR-CAD-004): 'cadence' → cadence-run | 'viral' (default/legacy) → autopilot-run.
> 50	        // Both are cron-only (Bearer SB_SECRET_KEY) and take the server-trusted user_id from the plan row.
> 51	        const target = p.plan_kind === "cadence" ? "cadence-run" : "autopilot-run";
> 52	        const r = await fetch(`${url}/functions/v1/${target}`, {
> 53	          method: "POST",
> 54	          headers: {
> 55	            Authorization: `Bearer ${serviceKey}`,
> 56	            "x-autopilot-user-id": p.user_id,   // server-trusted (from the plan row)
> 57	            "Content-Type": "application/json",
> 58	          },
> 59	          body: JSON.stringify({ plan_id: p.id }),
> 60	        });
> 61	        const d = await r.json().catch(() => ({}));
> 62	        if (d?.ok) tally.dispatched++;
> 63	        else if (d?.reason) tally.aborted++;   // cap/balance abort — expected, not an error
> 64	        else tally.errors++;
> 65	      } catch { tally.errors++; }
> 66	    };
> 67	    for (let i = 0; i < list.length; i += CONCURRENCY) await Promise.all(list.slice(i, i + CONCURRENCY).map(one));
> 68	
> 69	    if (list.length >= MAX_PER_RUN) console.warn(`[autopilot-cadence-cron] hit MAX_PER_RUN=${MAX_PER_RUN} — more plans may be due`);
> 70	    log("healthy");
> 71	    return json({ status: "ok", due: list.length, ...tally });
> 72	  } catch (e) {
> 73	    log("error");
> 74	    return json({ error: e instanceof Error ? e.message : "unknown" }, 500);
> 75	  }
> 76	});
> 77	
> ```

## 🤖 Claude *(10:06:53)*

<details>
<summary>💭 Thinking Process</summary>

I need to verify what type the `platform` column uses in the `scheduled_posts` table—whether it's a `social_platform` enum or text—since the cadence-run service is currently inserting platform values that need to match the column's constraints.

</details>


## 🤖 Claude *(10:06:55)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql",
  "offset": 158,
  "limit": 30
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 158	CREATE TABLE public.scheduled_posts (
> 159	  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> 160	  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 161	  content_id UUID REFERENCES public.content_library(id) ON DELETE SET NULL,
> 162	  campaign_id UUID REFERENCES public.campaigns(id) ON DELETE SET NULL,
> 163	  social_account_id UUID REFERENCES public.social_accounts(id) ON DELETE SET NULL,
> 164	  platform social_platform NOT NULL,
> 165	  scheduled_at TIMESTAMPTZ NOT NULL,
> 166	  published_at TIMESTAMPTZ,
> 167	  status post_status NOT NULL DEFAULT 'queued',
> 168	  platform_post_id TEXT,
> 169	  error_message TEXT,
> 170	  retry_count INTEGER DEFAULT 0,
> 171	  max_retries INTEGER DEFAULT 3,
> 172	  metadata JSONB DEFAULT '{}',
> 173	  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
> 174	  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
> 175	);
> 176	ALTER TABLE public.scheduled_posts ENABLE ROW LEVEL SECURITY;
> 177	
> 178	-- 12. OPTIMIZATION POLICY
> 179	CREATE TABLE public.optimization_policy (
> 180	  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
> 181	  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
> 182	  campaign_id UUID REFERENCES public.campaigns(id) ON DELETE SET NULL,
> 183	  action_type TEXT NOT NULL,
> 184	  action_details JSONB NOT NULL DEFAULT '{}',
> 185	  reward NUMERIC(8,4) DEFAULT 0,
> 186	  context JSONB DEFAULT '{}',
> 187	  applied BOOLEAN DEFAULT FALSE,
> ```

## 🤖 Claude *(10:07:28)*

<details>
<summary>💭 Thinking Process</summary>

The `scheduled_posts.platform` column is a non-nullable enum that accepts 'linkedin', 'instagram', 'facebook', 'twitter', 'tiktok', 'youtube', 'pinterest', and 'wordpress'. When cadence-run inserts records, it needs to map its lowercased channel names to valid enum values, which means for video content the supported platforms are 'youtube', 'tiktok', 'instagram', 'facebook', 'linkedin', and 'pinterest' — excluding X since it's not in the enum.

The current code already handles this constraint at line 302 when it inserts `platform: channel` into `scheduled_posts`, so the enum validation is already built into the existing design. Now for the `space_publish_variants` table, when cadence-run creates a variant record it needs to provide `user_id`, `source_asset_id`, `channel` (reusing the cadence channel string), `surface` (which requires a default value per channel), and the server-trusted asset metadata from `creative_assets`. The auto-publish flow then reads only the asset bucket, key, kind, and user ID from that variant.

There's an idempotency concern though — if cadence-run mints a new variant on every dispatch, it could create duplicates.  Using an upsert on `(user_id, source_asset_id, channel, surface)` would make it idempotent, so recurring cadences for the same asset and channel reuse the same variant row. Cadence-run doesn't actually need to set the variant status to 'scheduled' since it tracks idempotency through its own `cadence_dispatches` ledger; the variant can stay in draft status and auto-publish doesn't check that field anyway.

Now I'm weighing two approaches: either cadence-run mints the variant directly using its admin service role (which already resolves the asset owner-scoped), or it goes through a different path. If it goes direct, cadence-run would need to also fetch the asset's kind, storage bucket, and storage key alongside the existing asset resolution. Option A is the way forward since Option B fails—the service key can't authenticate as a user, so getUser returns nothing and hits a 401. Option A mirrors the existing publish-space-asset logic by inlining the service-role write directly into cadence-run, which is clean and requires no migration. For video assets, the auto-publish resolver correctly sets video_url, while image assets set image_url, which handles the youtube/tiktok constraint properly.

There's a surface complexity though: Instagram's IG branch checks if surface is "story" or "stories" to decide between REELS (video_url) versus STORIES, but cadence-run needs to populate surface in both the internal space_publish_variants table and the metadata.reshape.content object that publish-social actually reads for media_type selection.

Since cadence-run currently only sets `{ text, channel }`, I should define a channel-to-surface mapping (youtube→'shorts', tiktok→'video', instagram→'reels') to satisfy the NOT NULL constraint and maintain idempotency, even though it doesn't directly control media resolution. Let me check if there's an existing smoke test for cadence I can extend and review the current testing patterns.

</details>


## 🤖 Claude *(10:07:28)*

Let me check the cadence_dispatches schema, existing cadence smokes, and the spaces-cadence SOP/BoK to ground the proposal.

## 🤖 Claude *(10:07:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"=== cadence_dispatches DDL (status enum + partial idx) ===\"; sed -n '/cadence_dispatches/,/;/p' supabase/migrations/20260716120000_cadence_recurrence.sql | grep -niE \"status|CHECK|UNIQUE|CREATE TABLE|idempotency|channel|target_ref|occurrence\" | head -40",
  "description": "Inspect cadence_dispatches schema"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === cadence_dispatches DDL (status enum + partial idx) ===
> 2:-- Per-attempt dispatch ledger. NOT append-only pure (OTD-CAD-006): status transitions => service-role UPDATE.
> 3:-- The partial unique index is what ACTUALLY prevents double-post (failure RELEASES the key / success LOCKS it).
> 6:CREATE TABLE IF NOT EXISTS public.cadence_dispatches (
> 13:CREATE UNIQUE INDEX IF NOT EXISTS cadence_dispatches_idem
> 14:  ON public.cadence_dispatches (idempotency_key)
> 15:  WHERE status <> 'failed';
> 16:CREATE INDEX IF NOT EXISTS cadence_dispatches_plan_status_idx
> 17:  ON public.cadence_dispatches (plan_id, status);
> 29:  'spaces-cadence FR-CAD-003: per-attempt dispatch ledger. NOT append-only (OTD-CAD-006) — status transitions '
> 30:  '(queued|publishing|sent|failed) via service-role. Partial UNIQUE(idempotency_key) WHERE status<>''failed'' is '
> ```

## 🤖 Claude *(10:07:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"=== existing cadence smokes ===\"; ls scripts/qa/ | grep -iE \"cadence|space-asset|space-publish\" ; echo; echo \"=== cadence SOPs/BoK ===\"; ls docs/processes/ | grep -iE \"cadence|space-publish\"; echo \"---bok---\"; ls docs/bok/spaces-cadence/ 2>/dev/null",
  "description": "Find existing cadence smokes and docs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === existing cadence smokes ===
> apply-space-publish-variants-migration.sh
> smoke-autopilot-video-cadence.ts
> smoke-cadence-dispatch.ts
> smoke-space-publish-variants.ts
> 
> === cadence SOPs/BoK ===
> cadence-recurrence-engine.md
> content-cadence-strategy.md
> space-publish-format-preview.md
> space-publish-variants.md
> ---bok---
> 00-deepsearch-blueprint.md
> 00-index.md
> 01-mrd.md
> 02-brd.md
> 03-prd.md
> 04-frd.md
> 05-sdd.md
> 06-data-model.md
> 07-process-flow.md
> 08-quality-metrics.md
> 09-pattern-conformance.md
> ```

## 🤖 Claude *(10:07:37)*

<details>
<summary>💭 Thinking Process</summary>

I need to check the existing smoke test files to understand the pattern and see what gap the current cadence test covers—whether it's already asserting variant behavior or just caption-only scenarios.

</details>


## 🤖 Claude *(10:07:37)*

Let me read the existing cadence-dispatch smoke to see what it currently asserts, and the space-publish-variants smoke for the write pattern.

## 🤖 Claude *(10:07:37)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/smoke-cadence-dispatch.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env bun
> 2	/**
> 3	 * smoke-cadence-dispatch — witness E2E de despacho da Cadência (spaces-cadence Fatia 1).
> 4	 * Fecha a ressalva aberta do seal 2026-07-15 ("falta witness E2E de despacho") SEM publicar
> 5	 * nada real: o throwaway não tem credencial social — a linha `scheduled_posts` é provada e
> 6	 * removida no cleanup.
> 7	 *
> 8	 * Gates (SOP docs/processes/cadence-recurrence-engine.md — critérios materiais §Verification):
> 9	 *   W1  setup: throwaway SMOKETEST + creative_asset dele (register_creative_asset RPC)
> 10	 *   W2  cron identity: invoke SEM Bearer SB_SECRET_KEY → 403 (SOP autopilot-cron-identity)
> 11	 *   W3  dispatch: plano cadence vencido → 1 linha cadence_dispatches (uuid) + 1 linha
> 12	 *       scheduled_posts status='queued' (uuid) com metadata.cadence.plan_id correto
> 13	 *   W4  re-arm: next_run_at avançou em UTC (> occurrence consumida)
> 14	 *   W5  idempotência: MESMA occurrence re-tickada → already_dispatched, 0 nova linha no sink
> 15	 *   W6  tenant bind: plano com source_asset_id de OUTRO tenant → no_subject (0 dispatch)
> 16	 *   W7  cleanup total: 0 resíduo (scheduled_posts/cadence_dispatches/plans/asset/user)
> 17	 *
> 18	 * Zero-custo: Fatia 1 dispatch de asset existente = 0 mco (OTD-CAD-002=A).
> 19	 * Run: set -a; source .env; set +a; bun run scripts/qa/smoke-cadence-dispatch.ts
> 20	 */
> 21	import { createClient } from '@supabase/supabase-js';
> 22	
> 23	import { createThrowawayUser, deleteThrowawayUser } from './lib/qa-throwaway';
> 24	
> 25	const URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL!;
> 26	const SVC = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY)!;
> 27	if (!URL || !SVC) { console.error('needs SUPABASE_URL + SB_SECRET_KEY (source .env)'); process.exit(1); }
> 28	
> 29	const admin = createClient(URL, SVC, { auth: { persistSession: false } });
> 30	const FN = `${URL}/functions/v1/cadence-run`;
> 31	
> 32	let pass = 0, fail = 0;
> 33	const gate = (id: string, ok: boolean, detail: string) => {
> 34	  console.log(`${ok ? '✅' : '❌'} ${id} — ${detail}`);
> 35	  if (ok) pass++; else fail++;
> 36	};
> 37	
> 38	const invoke = (planId: string, auth?: string) =>
> 39	  fetch(FN, {
> 40	    method: 'POST',
> 41	    headers: { 'Content-Type': 'application/json', ...(auth ? { Authorization: auth } : {}) },
> 42	    body: JSON.stringify({ plan_id: planId }),
> 43	  });
> 44	
> 45	let uid: string | null = null;
> 46	let otherUid: string | null = null;
> 47	let planId: string | null = null;
> 48	let foreignPlanId: string | null = null;
> 49	
> 50	try {
> 51	  // ── W1 — setup ──────────────────────────────────────────────────────────────
> 52	  const user = await createThrowawayUser(admin, 'cadsmoke');
> 53	  uid = user.uid;
> 54	  const { data: assetId, error: raErr } = await admin.rpc('register_creative_asset', {
> 55	    p_user_id: uid,
> 56	    p_kind: 'image',
> 57	    p_storage_bucket: 'canvas-assets',
> 58	    p_storage_key: `${uid}/smoke-cadence/subject.png`,
> 59	    p_source_module: 'external',
> 60	    p_source_job_id: `smoke-cadence-${Date.now()}`,
> 61	  });
> 62	  gate('W1', !raErr && typeof assetId === 'string', raErr?.message ?? `asset ${String(assetId).slice(0, 8)} do throwaway ${uid.slice(0, 8)}`);
> 63	  if (raErr || !assetId) throw new Error('setup failed');
> 64	
> 65	  const occurrence = new Date(Date.now() - 60_000).toISOString(); // vencido há 1 min
> 66	  const { data: plan, error: planErr } = await admin
> 67	    .from('autopilot_plans')
> 68	    .insert({
> 69	      user_id: uid,
> 70	      name: 'SMOKETEST cadence dispatch',
> 71	      plan_kind: 'cadence',
> 72	      is_active: true,
> 73	      // Legacy NOT NULL fillers — mirrors cadence-plan/index.ts:289-296 exactly
> 74	      mode: 'every_n_days',
> 75	      interval_days: 1,
> 76	      next_run_at: occurrence,
> 77	      recurrence: { frequency: 'daily', hours: 9, minutes: 0, tz: 'America/Sao_Paulo' },
> 78	      quiet_hours: null,
> 79	      program: { source_asset_id: assetId, steps: [] },
> 80	      channel_allowlist: ['instagram'],
> 81	      budget_cap_mco: 12, // CHECK >= 12 (1-cycle kill-switch floor); Fatia 1 dispatch spends 0
> 82	      platforms: ['instagram'],
> 83	      target_product_ids: [assetId], // legacy NOT NULL filler (canonical subject = program.source_asset_id)
> 84	    })
> 85	    .select('id')
> 86	    .single();
> 87	  if (planErr || !plan?.id) throw new Error(`plan insert: ${planErr?.message}`);
> 88	  planId = plan.id as string;
> 89	
> 90	  // ── W2 — cron identity fail-closed ─────────────────────────────────────────
> 91	  const noAuth = await invoke(planId);
> 92	  const badAuth = await invoke(planId, 'Bearer not-the-secret');
> 93	  gate('W2', noAuth.status === 403 && badAuth.status === 403, `sem/errado Bearer → ${noAuth.status}/${badAuth.status} (esperado 403/403)`);
> 94	
> 95	  // ── W3 — dispatch real ──────────────────────────────────────────────────────
> 96	  const r1 = await invoke(planId, `Bearer ${SVC}`);
> 97	  const b1 = await r1.json().catch(() => ({}));
> 98	  const { data: disp } = await admin
> 99	    .from('cadence_dispatches').select('id, status, channel, target_ref')
> 100	    .eq('plan_id', planId).eq('user_id', uid);
> 101	  const { data: sps } = await admin
> 102	    .from('scheduled_posts').select('id, status, platform, metadata')
> 103	    .eq('user_id', uid);
> 104	  const sp0 = sps?.[0];
> 105	  const meta = (sp0?.metadata ?? {}) as { cadence?: { plan_id?: string }; reshape?: { source_asset_id?: string } };
> 106	  const w3 =
> 107	    r1.status === 200 && disp?.length === 1 && disp[0].status === 'queued' &&
> 108	    sps?.length === 1 && sp0?.status === 'queued' && sp0?.platform === 'instagram' &&
> 109	    meta.cadence?.plan_id === planId && meta.reshape?.source_asset_id === assetId &&
> 110	    disp[0].target_ref === sp0?.id;
> 111	  gate('W3', !!w3, w3
> 112	    ? `dispatch ${String(disp![0].id).slice(0, 8)} + scheduled_post ${String(sp0!.id).slice(0, 8)} queued (ledger linkado)`
> 113	    : `http ${r1.status} body=${JSON.stringify(b1).slice(0, 160)} dispatches=${disp?.length} sps=${sps?.length}`);
> 114	
> 115	  // ── W4 — re-arm UTC ─────────────────────────────────────────────────────────
> 116	  const { data: rearmed } = await admin
> 117	    .from('autopilot_plans').select('next_run_at').eq('id', planId).single();
> 118	  const w4 = !!rearmed?.next_run_at && new Date(rearmed.next_run_at as string).getTime() > new Date(occurrence).getTime();
> 119	  gate('W4', w4, `next_run_at ${rearmed?.next_run_at} > occurrence ${occurrence}`);
> 120	
> 121	  // ── W5 — idempotência (mesma occurrence re-tickada) ─────────────────────────
> 122	  await admin.from('autopilot_plans').update({ next_run_at: occurrence }).eq('id', planId);
> 123	  const r2 = await invoke(planId, `Bearer ${SVC}`);
> 124	  const b2 = await r2.json().catch(() => ({}));
> 125	  const { count: dispCount } = await admin
> 126	    .from('cadence_dispatches').select('id', { count: 'exact', head: true })
> 127	    .eq('plan_id', planId).eq('user_id', uid);
> 128	  const { count: spCount } = await admin
> 129	    .from('scheduled_posts').select('id', { count: 'exact', head: true }).eq('user_id', uid);
> 130	  gate('W5', dispCount === 1 && spCount === 1, `2º tick mesma occurrence → dispatches=${dispCount} scheduled=${spCount} (esperado 1/1) body=${JSON.stringify(b2).slice(0, 100)}`);
> 131	
> 132	  // ── W6 — tenant bind (asset de OUTRO tenant → no_subject) ──────────────────
> 133	  const other = await createThrowawayUser(admin, 'cadsmoke-other');
> 134	  otherUid = other.uid;
> 135	  const { data: fplan } = await admin
> 136	    .from('autopilot_plans')
> 137	    .insert({
> 138	      user_id: otherUid, name: 'SMOKETEST foreign subject', plan_kind: 'cadence', is_active: true,
> 139	      mode: 'every_n_days', interval_days: 1,
> 140	      next_run_at: occurrence,
> 141	      recurrence: { frequency: 'daily', hours: 9, minutes: 0, tz: 'America/Sao_Paulo' },
> 142	      program: { source_asset_id: assetId, steps: [] }, // asset do PRIMEIRO tenant
> 143	      channel_allowlist: ['instagram'], budget_cap_mco: 12, platforms: ['instagram'],
> 144	      target_product_ids: [assetId],
> 145	    })
> 146	    .select('id').single();
> 147	  foreignPlanId = fplan?.id as string | null;
> 148	  const r3 = foreignPlanId ? await invoke(foreignPlanId, `Bearer ${SVC}`) : null;
> 149	  const b3 = r3 ? await r3.json().catch(() => ({})) : {};
> 150	  const { count: foreignSp } = await admin
> 151	    .from('scheduled_posts').select('id', { count: 'exact', head: true }).eq('user_id', otherUid);
> 152	  const w6 = !!r3 && foreignSp === 0 && String((b3 as { reason?: string }).reason ?? '').includes('subject');
> 153	  gate('W6', w6, `plano com asset alheio → reason=${(b3 as { reason?: string }).reason} scheduled=${foreignSp} (esperado 0)`);
> 154	} catch (e) {
> 155	  gate('FATAL', false, (e as Error).message);
> 156	} finally {
> 157	  // ── W7 — cleanup total ───────────────────────────────────────────────────────
> 158	  try {
> 159	    for (const u of [uid, otherUid]) {
> 160	      if (!u) continue;
> 161	      await admin.from('scheduled_posts').delete().eq('user_id', u);
> 162	      await admin.from('cadence_dispatches').delete().eq('user_id', u);
> 163	      await admin.from('autopilot_plans').delete().eq('user_id', u);
> 164	      await admin.from('creative_assets').delete().eq('user_id', u);
> 165	    }
> 166	    let residue = 0;
> 167	    for (const u of [uid, otherUid]) {
> 168	      if (!u) continue;
> 169	      for (const t of ['scheduled_posts', 'cadence_dispatches', 'autopilot_plans', 'creative_assets']) {
> 170	        const { count } = await admin.from(t).select('id', { count: 'exact', head: true }).eq('user_id', u);
> 171	        residue += count ?? 0;
> 172	      }
> 173	      await deleteThrowawayUser(admin, u);
> 174	    }
> 175	    gate('W7', residue === 0, `resíduo pós-cleanup = ${residue} rows (esperado 0)`);
> 176	  } catch (e) {
> 177	    gate('W7', false, `cleanup: ${(e as Error).message}`);
> 178	  }
> 179	}
> 180	
> 181	console.log(`\n${pass}/${pass + fail} gates verdes`);
> 182	process.exit(fail === 0 ? 0 : 1);
> 183	
> ```

## 🤖 Claude *(10:08:09)*

<details>
<summary>💭 Thinking Process</summary>

I'm looking at the smoke test that validates the current caption-only behavior by checking that `meta.reshape.source_asset_id` matches the asset ID. For the video fix, I need to extend this test to use a VIDEO asset instead and add an assertion that a `space_publish_variants` row gets created.

The test should verify that `metadata.reshape.space_publish_variant_id` is set and points to that variant, and that the variant is owner-scoped resolvable by querying the asset_bucket/asset_key using the variant_id and user_id — which is exactly what auto-publish's resolver does. I've also confirmed there's no existing `source_asset_id` branch in auto-publish (only carousel_render_id, space_publish_variant_id, and channel_variant_id), so the caption-only gap is definitely real.

Looking at the cadence-run metadata shape, `source_asset_id` is being set but auto-publish completely ignores it — it's a dead field. The `asset_kind` column on space_publish_variants has no CHECK constraint, so it can freely accept 'video', 'image', or 'none'. The variant's `platform` field is nullable and not required for media resolution, though cadence-run could optionally map channel to social_platform for consistency.

For the NOT NULL surface requirement, I need a stable per-channel default since the upsert conflict key includes surface — this keeps idempotency across cadence cycles. Auto-publish doesn't strictly read surface for YouTube/TikTok, but for Instagram Reels it defaults to REELS if surface isn't 'story', so including surface in the cadence content makes sense for completeness even if optional.

The migration is already applied — space_publish_variants table exists from migration 20260710233000, there's an apply script in the QA folder, and the smoke test exists. So this is purely an edge-function code fix in cadence-run without needing a new migration.

I should verify the table is actually applied in production. The mission mentions auto-publish already resolves space_publish_variant_id, which suggests it's live. I have SELECT permission according to the instructions, so let me try querying the database directly to confirm the table exists rather than relying on indirect evidence.

</details>


## 🤖 Claude *(10:08:09)*

Let me verify config.toml (verify_jwt), confirm no `source_asset_id`/`reshape` resolver branch is missing in auto-publish, and materially confirm the `space_publish_variants` table is live via a SELECT.

## 🤖 Claude *(10:08:13)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"=== config.toml cadence/auto-publish/publish-space ===\"; grep -nE \"cadence-run|cadence-plan|auto-publish|publish-space-asset|publish-social\" supabase/config.toml; echo; echo \"=== does auto-publish ever read reshape.source_asset_id ? (expect none) ===\"; grep -nE \"source_asset_id\" supabase/functions/auto-publish/index.ts || echo \"NONE \u2014 confirmed no bare-asset resolver branch\"",
  "description": "Check config.toml and auto-publish for source_asset_id branch"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === config.toml cadence/auto-publish/publish-space ===
> 6:[functions.publish-social]
> 36:[functions.cadence-plan]
> 38:# cadence-run — cron-only (FR-CAD-006). Invoked by autopilot-cadence-cron with Bearer SB_SECRET_KEY, re-checked
> 40:[functions.cadence-run]
> 
> === does auto-publish ever read reshape.source_asset_id ? (expect none) ===
> NONE — confirmed no bare-asset resolver branch
> ```

## 🤖 Claude *(10:08:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; if [ -f .env ]; then set -a; . ./.env 2>/dev/null; set +a; fi; U=\"${SUPABASE_URL:-$VITE_SUPABASE_URL}\"; K=\"${SB_SECRET_KEY:-$SUPABASE_SERVICE_ROLE_KEY}\"; if [ -z \"$U\" ] || [ -z \"$K\" ]; then echo \"NO_ENV_KEYS (cannot run live SELECT)\"; else echo \"=== live HEAD count space_publish_variants (proves table exists) ===\"; curl -s -o /dev/null -w \"HTTP %{http_code}\\n\" -X GET \"$U/rest/v1/space_publish_variants?select=id&limit=1\" -H \"apikey: $K\" -H \"Authorization: Bearer $K\" -H \"Prefer: count=exact\" ; echo \"=== live HEAD count cadence_dispatches ===\"; curl -s -o /dev/null -w \"HTTP %{http_code}\\n\" -X GET \"$U/rest/v1/cadence_dispatches?select=id&limit=1\" -H \"apikey: $K\" -H \"Authorization: Bearer $K\"; fi",
  "description": "Live SELECT to prove space_publish_variants table exists"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === live HEAD count space_publish_variants (proves table exists) ===
> HTTP 206
> === live HEAD count cadence_dispatches ===
> HTTP 200
> ```

## 🤖 Claude *(10:08:23)*

<details>
<summary>💭 Thinking Process</summary>

The SELECT queries confirm both tables are live in production, so no migration is needed for the fix. Now I'm checking the config.toml settings for the JWT verification across cadence-run, cadence-plan, and auto-publish to see how the publish-space-asset entries are configured.

</details>


## 🤖 Claude *(10:08:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; sed -n '1,12p;34,44p' supabase/config.toml; echo \"=== auto-publish + publish-space-asset entries ===\"; grep -nA1 -E \"functions.auto-publish|functions.publish-space-asset\" supabase/config.toml",
  "description": "Show verify_jwt config for relevant functions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> project_id = "bcyvddsykvehvpwstlfa"
> 
> # Configuração de Bypass de JWT para Orquestração Soberana
> # key-migration 2026-06-01: service→service targets are called with the new sb_secret_ key (not a JWT),
> # so the gateway JWT check must be off; each function below enforces its own in-code auth gate.
> [functions.publish-social]
> verify_jwt = false
> [functions.check-post-existence]
> verify_jwt = false
> [functions.delete-remote-post]
> verify_jwt = false
> [functions.refresh-social-token]
> [functions.autopilot-cadence-cron]
> verify_jwt = false
> [functions.cadence-plan]
> verify_jwt = false
> # cadence-run — cron-only (FR-CAD-006). Invoked by autopilot-cadence-cron with Bearer SB_SECRET_KEY, re-checked
> # in-function (403 otherwise); user_id is server-trusted from the plan row, never the body.
> [functions.cadence-run]
> verify_jwt = false
> [functions.autopilot-analyze]
> verify_jwt = false
> [functions.autopilot-collect]
> === auto-publish + publish-space-asset entries ===
> ```

## 🤖 Claude *(10:08:54)*

<details>
<summary>💭 Thinking Process</summary>

I'm realizing there's a potential issue here: auto-publish and publish-space-asset don't have verify_jwt=false configured, so they default to verify_jwt=true. But auto-publish gets triggered by a cron job using the service key—and I need to figure out whether that service key (the sb_secret_ format) would actually pass the JWT verification check at the gateway.

Actually, looking at the note more carefully: service-to-service calls with sb_secret_ need verify_jwt=false because the secret key isn't a JWT. So auto-publish should theoretically need that flag too. But it's already live and working as the drain, so either it's using a different invocation mechanism or this is a pre-existing quirk I shouldn't worry about right now. The actual fix I'm making only touches cadence-run (which already has verify_jwt=false), so I don't need to modify auto-publish at all. The cadence-run change will just mint the variant and reference instead of relying on auto-publish to resolve them.

Now I need to finalize the diagnosis and minimal fix. Let me verify the content object cadence-run passes — currently it's just `{ text: plan.name ?? "", channel }`. For the caption, using plan.name is acceptable for this phase, though ideally it could pull from the plan program later. I should also check what asset.kind values are possible so I can map them correctly to the variant. Looking at the publish-space-asset logic, it maps video to "video", image to "image", and everything else to "none". I'll mirror that mapping.

One more thing to confirm: cadence-run's creative_assets select currently pulls `id, user_id`, but I need to add `kind, storage_bucket, storage_key` to the query so I have what I need to construct the variant.

Now I'm putting together the structured diagnosis with file and line references, covering the dispatch shape, the caption gap confirmed by the TODO, the metadata.reshape shape, how the auto-publish resolver branches don't read source_asset_id, the publish-social video death, the space_publish_variants schema as the actual vehicle, the publish:false pattern in publish-space-asset and why cadence-run can't call it directly due to JWT constraints, and proof that the tables exist. Then I'll lay out the minimal fix: cadence-run mints the variant inline using service-role, with exact files to touch and code changes needed — expanding the select, upserting the variant, swapping the metadata.reshape call — plus the surface default map and no migration required.

I'm checking the register_creative_asset RPC signature to confirm the smoke test can create a video asset by passing kind='video' instead of 'image', which the 26-arg version supports. I'm also verifying that auto-publish's attachAsset expects a storage path rather than a URL, which creative_assets.storage_key provides. One more detail to nail down: the variant upsert in cadence-run needs to work around the fact that space_publish_variants has no INSERT/UPDATE policy for authenticated users, but cadence-run uses service-role so it should bypass that.

For the variant's surface and channel fields, I need to map each social platform to sensible defaults—YouTube to 'shorts', TikTok to 'video', Instagram to 'reels', and so on—though these mostly don't gate anything except Instagram's content.surface check. I'll keep the variant.surface stable and non-null. The key question now is whether cadence-run should also set variant.platform by mapping the channel to the corresponding social_platform enum.

Since cadence loops through channels (line 211) and the variant's idempotency key includes the channel, each channel gets its own variant row. The variant mint should happen inside that loop, right before building the scheduled_posts insert, so each channel's variant is created with the correct surface and platform mapping. I should also double-check whether selecting the asset once before the loop (line 151) creates any issues downstream.

</details>


## 🤖 Claude *(10:08:54)*

I have everything needed, all materially confirmed. Let me compile the exhaustive findings.

## 🤖 Claude *(10:10:18)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "report": "## MISS\u00c3O C1 \u2014 Cad\u00eancia de v\u00eddeo: diagn\u00f3stico + fatia m\u00ednima\n\nTodos os fatos abaixo t\u00eam evid\u00eancia file:line lida nesta sess\u00e3o. Provas de exist\u00eancia de tabela via SELECT/HEAD ao vivo (service key do .env) marcadas [LIVE].\n\n---\n\n### 1. cadence-run \u2014 o dispatch monta `scheduled_posts` SEM anexar m\u00eddia (confirmado)\n\nArquivo: `supabase/functions/cadence-run/index.ts`\n\n**Onde monta a linha `scheduled_posts`:** dentro do loop de canais, linhas **298\u2013306**:\n```ts\nconst content: Record<string, unknown> = { text: (plan.name as string) ?? \"\", channel };\nconst { data: sp, error: spErr } = await admin\n  .from(\"scheduled_posts\")\n  .insert({\n    user_id: userId, content_id: null, campaign_id: null, social_account_id: null,\n    platform: channel, scheduled_at: new Date().toISOString(), status: \"queued\",\n    metadata: { reshape: { content, source_asset_id: sourceAssetId, channel }, cadence: { plan_id: planId, dispatch_id: dispatchId } },\n  })\n```\n\n**Shape exato de `metadata.reshape` gravado hoje:**\n```json\n{\n  \"reshape\": {\n    \"content\":         { \"text\": \"<plan.name>\", \"channel\": \"<channel>\" },\n    \"source_asset_id\": \"<creative_assets.id>\",\n    \"channel\":         \"<channel>\"\n  },\n  \"cadence\": { \"plan_id\": \"<uuid>\", \"dispatch_id\": \"<uuid>\" }\n}\n```\n\n**Confirma\u00e7\u00e3o de que N\u00c3O anexa asset** \u2014 o pr\u00f3prio c\u00f3digo admite o gap num `TODO` expl\u00edcito, linhas **294\u2013297**:\n> `TODO(FR-CAD-006 \u00b7 auto-publish): a bare creative_assets.id has NO owner-scoped resolver branch in auto-publish (it resolves channel_variant_id / space_publish_variant_id / carousel_render_id). Binding the subject's IMAGE to the post requires either (a) an auto-publish branch that signs a creative_assets.id owner-scoped, or (b) minting a space_publish_variant row. Until then this enqueues the CAPTION only.`\n\nO campo `reshape.source_asset_id` \u00e9 **letra morta** para o consumo: auto-publish nunca o l\u00ea (prova no item 2). `content_id`/`campaign_id` s\u00e3o `null`, ent\u00e3o o fallback de v\u00eddeo por campaign_id do auto-publish (linha 75) tamb\u00e9m n\u00e3o dispara.\n\n- `platform: channel` (linha 302) \u2192 `scheduled_posts.platform` \u00e9 `social_platform NOT NULL` (enum), definido em `supabase/migrations/20260402014040_*.sql:164` + enum em `:12` = `('linkedin','instagram','facebook','twitter','tiktok','youtube','pinterest','wordpress')`. cadence-plan j\u00e1 bloqueia x/twitter (`cadence-plan/index.ts:39,213-214`), ent\u00e3o os canais v\u00e1lidos de v\u00eddeo (`youtube`,`tiktok`,`instagram`) casam com o enum \u2014 a inser\u00e7\u00e3o atual j\u00e1 depende disso, n\u00e3o \u00e9 um risco novo.\n\n---\n\n### 2. auto-publish \u2014 como resolve m\u00eddia (e por que a cad\u00eancia morre)\n\nArquivo: `supabase/functions/auto-publish/index.ts`\n\nL\u00ea `post.metadata.reshape` (linha **112**) e resolve o asset **owner-scoped** (`.eq(\"user_id\", post.user_id)` \u2014 FMEA-011) por **exatamente tr\u00eas** discriminadores, nesta ordem:\n\n| Branch | Linhas | Fonte owner-scoped | Seta em `native` |\n|---|---|---|---|\n| `reshape.carousel_render_id` | 140\u2013159 | `creative_assets` por `source_job_id` + `user_id` | `native.images[]` |\n| `reshape.space_publish_variant_id` | 160\u2013169 | `space_publish_variants` (`asset_bucket,asset_key,asset_kind`) por `id`+`user_id` \u2192 `attachAsset` | `native.video_url` **ou** `native.image_url` |\n| `reshape.channel_variant_id` | 170\u2013179 | `channel_variants` por `id`+`user_id` \u2192 `attachAsset` | `native.video_url`/`image_url` |\n\n`attachAsset` (linhas **127\u2013133**) assina URL fresca 6h (`createSignedUrl(key, 21600)`) e, se `kind===\"video\"`, seta `native.video_url`.\n\n**NENHUM branch l\u00ea `reshape.source_asset_id`** \u2014 confirmado por grep: `grep -nE \"source_asset_id\" auto-publish/index.ts` \u2192 **NONE**. Logo, para a linha da cad\u00eancia, `native` fica s\u00f3 `{ text }` (a partir de `reshape.content.text`, linha 115). Sem `video_url`.\n\n**Onde morre** \u2014 `supabase/functions/publish-social/index.ts`:\n- YouTube: linhas **531\u2013535** \u2192 `if (!videoUrl) { pulse(\"degraded\",\"youtube_no_video\"); throw new Error(\"PLATFORM_PUBLISH_FAILED\"); }`\n- TikTok: linhas **400\u2013404** \u2192 `if (!videoUrl) { pulse(\"degraded\",\"tiktok_no_video\"); throw ... }`\n\nOu seja: a corre\u00e7\u00e3o m\u00ednima \u00e9 **fazer cadence-run gravar `metadata.reshape.space_publish_variant_id`** apontando uma variant do asset resolvida owner-scoped. \u00c9 o encaixe do branch 160\u2013169 que **j\u00e1 est\u00e1 vivo**.\n\n---\n\n### 3. Como criar a variant \u2014 publish-space-asset e por que cadence-run N\u00c3O pode cham\u00e1-lo\n\nArquivo: `supabase/functions/publish-space-asset/index.ts`\n\n- `publish:false` (draft, linhas **192\u2013197**) faz **upsert idempotente** em `space_publish_variants` on-conflict `(user_id, source_asset_id, channel, surface)` (linhas 173\u2013188), com `asset_bucket/asset_key/asset_kind` **resolvidos server-side** de `creative_assets` bound ao caller (linhas 79\u201383), e retorna `space_publish_variant_id`.\n- `publish:true` adicionalmente enfileira `scheduled_posts` com `metadata.reshape.space_publish_variant_id` (linhas 218\u2013223) \u2014 que \u00e9 literalmente o formato que auto-publish consome.\n\n**cadence-run N\u00c3O pode invocar publish-space-asset internamente:** publish-space-asset exige **USER JWT** (`userClient.auth.getUser()`, linhas 51\u201357; retorna 401 sem user). cadence-run \u00e9 **cron-only** com `Bearer SB_SECRET_KEY` (`cadence-run/index.ts:116`) \u2014 n\u00e3o tem JWT do user e mintar um seria pesado/fr\u00e1gil. **Rejeitado.**\n\n**Caminho correto (Op\u00e7\u00e3o A):** cadence-run **\u00e9 service-role** (`admin` client, linha 107) e a tabela `space_publish_variants` \u00e9 **writes service-role-only por design** (migration `20260710233000_space_publish_variants.sql:52-58` \u2014 sem policy INSERT/UPDATE para authenticated; publish-space-asset \u00e9 o writer sancionado justamente por bypassar RLS). Logo cadence-run pode **mintar a variant diretamente via upsert**, espelhando publish-space-asset:173-188. Zero HTTP cross-fn, zero JWT.\n\nSchema da vehicle (migration `20260710233000_space_publish_variants.sql`):\n- `channel text NOT NULL` (:31), `surface text NOT NULL` (:32), `platform social_platform` nullable (:33)\n- `asset_kind text` (sem CHECK, :36), `asset_bucket text` (:37), `asset_key text` (:38) \u2014 \"SERVER-TRUSTED (auto-publish signs THIS)\"\n- `UNIQUE (user_id, source_asset_id, channel, surface)` (:49) \u2192 upsert idempotente por ciclo de cad\u00eancia\n- auto-publish s\u00f3 l\u00ea `asset_bucket/asset_key/asset_kind` da variant (n\u00e3o precisa de `platform`/`surface`/`status` corretos para resolver a m\u00eddia).\n\n**Nota de fluxo:** program do plano carrega o sujeito. cadence-plan grava `program: { source_asset_id, steps }` (`cadence-plan/index.ts:250`); cadence-run l\u00ea via `extractSourceAssetId(program)` (`cadence-run/index.ts:142,376-384`). O sujeito j\u00e1 est\u00e1 resolvido owner-scoped em `cadence-run:151-158` \u2014 s\u00f3 falta ENRIQUECER esse SELECT (hoje `.select(\"id, user_id\")`) para trazer `kind, storage_bucket, storage_key`.\n\n---\n\n### PROVA MATERIAL [LIVE] \u2014 tabelas existem em prod, sem migration nova\n\nVia `curl` REST com service key (READ-ONLY, HEAD):\n- `GET /rest/v1/space_publish_variants?select=id&limit=1` \u2192 **HTTP 206** (tabela viva)\n- `GET /rest/v1/cadence_dispatches?select=id&limit=1` \u2192 **HTTP 200** (tabela viva)\n\n`config.toml`: `cadence-run` e `cadence-plan` = `verify_jwt = false` (linhas 36\u201341). O branch consumidor (`space_publish_variant_id`) j\u00e1 est\u00e1 deployado em auto-publish. **Nenhuma migration \u00e9 necess\u00e1ria.**\n\n---\n\n### 4. FATIA M\u00cdNIMA PROPOSTA \u2014 \"agendar corte/POV/split-screen em cad\u00eancia recorrente, privado-primeiro\"\n\n**Estrat\u00e9gia:** cadence-run passa a MINTAR uma `space_publish_variant` por (asset,canal) via service-role e a referenci\u00e1-la em `metadata.reshape.space_publish_variant_id`, reusando 100% o trilho vivo (auto-publish branch 160\u2013169 \u2192 publish-social v\u00eddeo). **Sem migration, sem tabela nova, sem pg_cron novo.** Um \u00fanico arquivo de produ\u00e7\u00e3o tocado.\n\n**Arquivos exatos a tocar:**\n\n1. **`supabase/functions/cadence-run/index.ts`** (\u00fanica mudan\u00e7a de produ\u00e7\u00e3o):\n   - **Linhas 151\u2013153** \u2014 enriquecer o SELECT do sujeito:\n     `.select(\"id, user_id, kind, storage_bucket, storage_key\")` (hoje `\"id, user_id\"`). Manter o hard tenant bind `.eq(\"user_id\", userId)`.\n   - **Dentro do loop de canais (~antes da linha 298)** \u2014 mintar/upsert a variant owner-scoped via `admin`:\n     ```ts\n     const assetKind = asset.kind === \"video\" ? \"video\" : asset.kind === \"image\" ? \"image\" : \"none\";\n     const surface = SURFACE_BY_CHANNEL[channel] ?? \"feed\"; // youtube\u2192shorts, tiktok\u2192video, instagram\u2192reels...\n     const { data: variant } = await admin.from(\"space_publish_variants\").upsert({\n       user_id: userId, source_asset_id: sourceAssetId, channel, surface,\n       platform: PLATFORM_BY_CHANNEL[channel] ?? null,   // social_platform enum ou null (opcional)\n       asset_kind: assetKind, asset_bucket: asset.storage_bucket, asset_key: asset.storage_key,\n       asset_status: \"ready\",\n     }, { onConflict: \"user_id,source_asset_id,channel,surface\" })\n       .select(\"id\").single();\n     ```\n   - **Linhas 298\u2013306** \u2014 trocar o `metadata.reshape` para carregar o `space_publish_variant_id` (e opcionalmente `content.surface` para o IG escolher REELS/STORIES):\n     ```ts\n     const content: Record<string, unknown> = { text: (plan.name as string) ?? \"\", channel, surface };\n     // ... insert scheduled_posts com:\n     metadata: { reshape: { content, space_publish_variant_id: variant.id, channel, surface },\n                 cadence: { plan_id: planId, dispatch_id: dispatchId } }\n     ```\n   - Guard fail-soft: se `variant?.id` faltar \u2192 marcar dispatch `failed` (release da idempotency key, igual ao padr\u00e3o de `spErr` em 307\u2013314) e `continue`, para nunca enfileirar caption \u00f3rf\u00e3 de novo. Custo 0 (asset existente, OTD-CAD-002=A) mantido \u2014 n\u00e3o toca `deduct_mco_coins`.\n   - Adicionar dois mapas constantes no topo: `SURFACE_BY_CHANNEL` e `PLATFORM_BY_CHANNEL`.\n\n   **Privado-primeiro:** para replicar o fail-safe de publish-space-asset:213 (YouTube default `private`), setar `content.privacy = \"private\"` quando `channel===\"youtube\"` (e opcionalmente tiktok\u2192SELF_ONLY j\u00e1 \u00e9 o default do publish-social para conta unaudited, `publish-social:427-433`). auto-publish j\u00e1 propaga `content.privacy` inerte (linhas 119\u2013125) e publish-social o revalida contra allowlist fechada.\n\n2. **`scripts/qa/smoke-cadence-video-dispatch.ts`** (novo \u2014 clona `smoke-cadence-dispatch.ts`, que hoje afirma o gap em `W3: meta.reshape?.source_asset_id === assetId`, linha 109):\n   - **V1** setup: throwaway + `register_creative_asset` com **`p_kind:'video'`** (o existente usa `'image'`), `channel_allowlist:['youtube']`.\n   - **V2** cron identity 403 (sem/errado Bearer) \u2014 reusa W2.\n   - **V3** dispatch: tick vencido \u2192 assert (a) 1 linha `space_publish_variants` com `asset_kind='video'` + `asset_bucket/asset_key` == os do creative_asset; (b) `scheduled_posts.metadata.reshape.space_publish_variant_id` == variant.id (e N\u00c3O mais s\u00f3 `source_asset_id`); (c) `platform='youtube'`, `status='queued'`, `dispatch.target_ref` linkado.\n   - **V4** resolu\u00e7\u00e3o owner-scoped (simula auto-publish sem publicar de verdade): `SELECT asset_bucket,asset_key,asset_kind FROM space_publish_variants WHERE id=<variant> AND user_id=<uid>` retorna a chave \u2192 prova que `native.video_url` seria assinado. Cross-tenant: mesma query com `user_id=<outroUid>` retorna 0 linhas.\n   - **V5** idempot\u00eancia: 2\u00ba tick mesma occurrence \u2192 `already_dispatched`, 0 nova `scheduled_posts`, **1** variant (upsert n\u00e3o duplica).\n   - **V6** privado-primeiro: `metadata.reshape.content.privacy === 'private'` para youtube.\n   - **V7** cleanup total: 0 res\u00edduo em `scheduled_posts/cadence_dispatches/space_publish_variants/autopilot_plans/creative_assets` + delete throwaway.\n\n**Gate zero-custo que prova E2E:** `bun run scripts/qa/smoke-cadence-video-dispatch.ts` \u2192 todos os gates verdes, `exit 0`. \u00c9 zero-custo porque (a) Fatia 1 despacha asset existente = 0 mco; (b) o throwaway n\u00e3o tem credencial social, ent\u00e3o V4 **para na resolu\u00e7\u00e3o da variant** (a join exata que auto-publish faz) sem chamar publish-social/YouTube \u2014 nada \u00e9 publicado de verdade. Prova materialmente que o `no_video` foi eliminado: a m\u00eddia agora chega assin\u00e1vel a partir de uma fonte server-trusted owner-scoped.\n\n**Riscos/limites honestos:**\n- Para YouTube/TikTok o asset-sujeito PRECISA ser v\u00eddeo (`asset_kind='video'`). Um asset imagem num plano youtube ainda cairia em `youtube_no_video` \u2014 comportamento correto (imagem roteia para IG feed/pinterest). A UI/cadence-plan deveria validar kind\u00d7canal, mas isso \u00e9 enhancement, n\u00e3o bloqueia a fatia.\n- `content.text` hoje = `plan.name` (`cadence-run:298`) \u2014 caption fraca; usar `program.steps`/`native_text` \u00e9 enhancement fora do escopo m\u00ednimo.\n- `space_publish_variants.platform` mapeado \u00e9 opcional (auto-publish n\u00e3o o usa para resolver m\u00eddia); inclu\u00ed-lo s\u00f3 deixa a linha auto-descritiva.\n\n**UNVERIFIED:** n\u00e3o executei o smoke novo (n\u00e3o existe ainda) nem a auditoria `/security-review` do diff proposto \u2014 a mudan\u00e7a \u00e9 read-of-owned + write service-role \u00e0 tabela cujo writer sancionado j\u00e1 \u00e9 service-role, ent\u00e3o n\u00e3o abre superf\u00edcie RLS nova, mas o /security-review continua obrigat\u00f3rio por tocar caminho de asset cross-tenant (FMEA-011) antes de qualquer commit.\n\n---\n\n### Arquivos-chave (paths absolutos)\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/cadence-run/index.ts` (dispatch a corrigir: 151\u2013158 SELECT sujeito, 298\u2013306 sink)\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/auto-publish/index.ts` (resolver: 112, 160\u2013169 branch space_publish_variant_id, 127\u2013133 attachAsset)\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-space-asset/index.ts` (padr\u00e3o de upsert a espelhar: 79\u201383, 173\u2013188)\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/publish-social/index.ts` (morte no_video: youtube 531\u2013535, tiktok 400\u2013404)\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260710233000_space_publish_variants.sql` (schema da vehicle, service-role-only writes)\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/cadence-plan/index.ts` (program.source_asset_id seam: 250)\n- `/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/smoke-cadence-dispatch.ts` (base a clonar; W3:109 hoje afirma o caption-only gap)\n- `/home/gcrUX/htdocs/constellation-orchestra/supabase/config.toml` (cadence-run/plan verify_jwt=false: 36\u201341)"
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
> * **Sessão Anterior**: [[2026-07-21 - agent-a07de31c5d167a993]]
> * **Próxima Sessão**: [[2026-07-21 - agent-a6093ec49f09f904f]]
%% --- TIMELINE END --- %%

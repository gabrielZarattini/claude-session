# Diagnosticar falha de render no video-bridge
**Date:** 2026-07-07 | **Session ID:** `f233635b-ad8c-426b-9d4b-068cc9e2712c`

---

## 👤 User *(04:39:06)*

Você é o diagnosticador L2 do laço autonômico MAPE-K do MCORCH (Tier A — DIAGNÓSTICO
APENAS). Um incidente foi aberto pelo guardião mecânico. Sua missão: diagnosticar a
causa-raiz com prova material e propor o fix — SEM executar nenhuma mudança.

REGRAS INEGOCIÁVEIS:
- Você NÃO tem ferramentas de escrita. Não tente editar/commitar/instalar nada.
- Lei 1 (Materialidade): toda afirmação ancorada em evidência que você LEU (arquivo:linha,
  row de tabela, linha de log). Se não conseguir ver algo, diga "não pude verificar X".
- Ferramentas permitidas: Read/Grep/Glob, git read-only, e os scripts de QA re-executáveis
  (`bun run scripts/qa/...`, `bash scripts/qa/guard-sweep.sh --fast`) — todos herméticos.
- Contexto do projeto: /home/gcrUX/htdocs/constellation-orchestra (CLAUDE.md tem a
  arquitetura; docs/processes/ tem os SOPs; o incidente abaixo tem o sintoma).
- Seja eficiente: vá direto ao subsistema apontado pelo sintoma.

TERMINE SUA ÚLTIMA MENSAGEM EXATAMENTE NESTE FORMATO (as 3 linhas finais):
DIAGNOSIS: <causa-raiz em 1-3 frases, com a evidência arquivo:linha/row>
PROPOSED_FIX: <o fix em 1-3 frases, concreto o bastante para a sessão /loop executar>
CONFIDENCE: high|medium|low

INCIDENTE:
{
  "id": "INC-20260707T0432Z-1f2942b6",
  "class": "RED_FINDING",
  "severity": "P1",
  "symptom_hash": "1f2942b65aa102ba3da6f16984b1a20f49524bb6",
  "symptom": "infra error: video-bridge render_failed @ 2026-07-07T02:43:20.080391+00:00",
  "source": "tick",
  "first_seen_at": "2026-07-07T04:32:02.641Z",
  "last_seen_at": "2026-07-07T04:35:02.250Z",
  "count": 6,
  "details": [
    "{\"service\":\"video-bridge\",\"status\":\"error\",\"event\":\"render_failed\",\"last_seen_at\":\"2026-07-07T02:43:20.080391+00:00\"}"
  ],
  "suggested_action": "investigar o serviço video-bridge",
  "status": "open",
  "resolved_at": null,
  "resolution": null,
  "remediation_report": null
}

## 🤖 Claude *(04:39:14)*


## 🤖 Claude *(04:39:14)*

Vou investigar a causa-raiz do `render_failed` no video-bridge, começando pelo worker e pelos logs do sistema.

## 🤖 Claude *(04:39:15)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/video-bridge.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env bun
> 2	/**
> 3	 * scripts/video-bridge.ts
> 4	 *
> 5	 * HyperFrames render bridge — host worker that polls `video_renders` (engine='hyperframes', state='queued'),
> 6	 * atomically claims each, renders the composition → 9:16 1080×1920 MP4 (render-core.ts), uploads to the private
> 7	 * bucket `video-studio-assets`, and closes the render via `finalize_video_render` (the ONLY terminal authority).
> 8	 *
> 9	 * BoK SSOT: docs/bok/video-studio/04-frd.md FR-VS-024/026 + 05-sdd.md §2.3 (drift reconciliation 2026-06-24).
> 10	 * SOP (Lei 2): docs/processes/autopilot-video-9x16.md (gate OTD-VA-009).
> 11	 * Pattern: mirrors scripts/design-bridge.ts (poll + atomic claim) — the proven host↔cloud bridge (Edge fns can't
> 12	 *          reach a host daemon, OTD-VS-... ; the worker pulls). Tenancy: single-tenant Usuário Zero (OTD-VA-011);
> 13	 *          multi-tenant sandbox hardening (FR-VS-025 ephemeral container) is deferred to User 1.
> 14	 *
> 15	 * Supervisor: systemd --user video-bridge.service (Restart=always). Secrets load from ../.env (NOT in the unit).
> 16	 * Usage: bun run scripts/video-bridge.ts   (or `--once` to drain queued renders and exit — used by the smoke).
> 17	 */
> 18	
> 19	import { createClient } from '@supabase/supabase-js';
> 20	import { existsSync, readFileSync, rmSync } from 'fs';
> 21	import { join, dirname } from 'path';
> 22	import { fileURLToPath } from 'url';
> 23	import { renderComposition, renderStudioProject, type RenderSpec, type StudioProjectSpec, type RenderResult } from './hyperframes/render-core.ts';
> 24	
> 25	// ── Env (same loader as design-bridge.ts — no secrets in the systemd unit) ──
> 26	const __dirname = dirname(fileURLToPath(import.meta.url));
> 27	const envPath = join(__dirname, '../.env');
> 28	if (existsSync(envPath)) {
> 29	  for (const line of readFileSync(envPath, 'utf-8').split('\n')) {
> 30	    const m = line.match(/^([^#=\s][^=]*)=(.*)$/);
> 31	    if (m) process.env[m[1].trim()] = m[2].trim().replace(/^["']|["']$/g, '');
> 32	  }
> 33	}
> 34	
> 35	const SUPABASE_URL = process.env.SUPABASE_URL;
> 36	const SERVICE_KEY = process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY;
> 37	if (!SUPABASE_URL || !SERVICE_KEY) {
> 38	  console.error('❌ Missing SUPABASE_URL or SB_SECRET_KEY in .env');
> 39	  process.exit(1);
> 40	}
> 41	const supabase = createClient(SUPABASE_URL, SERVICE_KEY, { auth: { persistSession: false } });
> 42	
> 43	const BUCKET = 'video-studio-assets';
> 44	const POLL_MS = 4000;
> 45	const RUNNING_TIMEOUT_MS = 10 * 60 * 1000; // re-claim a render stuck in 'running' beyond this (dead worker)
> 46	
> 47	function logHealth(status: string, event: string, metadata?: Record<string, unknown>) {
> 48	  return supabase.from('infra_health_logs')
> 49	    .insert({ service: 'video-bridge', status, event, metadata: metadata ?? null })
> 50	    .then(() => {}, () => {});
> 51	}
> 52	
> 53	/** Atomic claim: queued→running for exactly one worker. Returns the claimed row or null. */
> 54	async function claim(renderId: string) {
> 55	  const { data, error } = await supabase
> 56	    .from('video_renders')
> 57	    .update({ state: 'running', updated_at: new Date().toISOString() })
> 58	    .eq('id', renderId)
> 59	    .eq('state', 'queued')
> 60	    .select('id, user_id, engine, charged_mco, composition')
> 61	    .maybeSingle();
> 62	  if (error || !data) return null;
> 63	  return data;
> 64	}
> 65	
> 66	/** Render one claimed row end to end. Never throws — translates failure to finalize(failed, refund). */
> 67	async function processRender(row: {
> 68	  id: string; user_id: string; charged_mco: number; composition: unknown;
> 69	}) {
> 70	  const renderId = row.id;
> 71	  const charged = row.charged_mco ?? 0;
> 72	  let outPath: string | null = null;
> 73	  try {
> 74	    const spec = row.composition as (RenderSpec | StudioProjectSpec) | null;
> 75	    if (!spec || typeof spec !== 'object') {
> 76	      throw new Error('composition_missing_or_invalid');
> 77	    }
> 78	    // Autopilot context — declared UP-FRONT (used by both register_creative_asset below and the FR-VA-025 attach).
> 79	    // Previously declared after the register call → a use-before-declaration TDZ-threw into the fail-soft catch,
> 80	    // silently skipping every video creative_assets registration. Editor (studio-project) renders carry no autopilot.
> 81	    const ap = (spec as { autopilot?: { user_id?: string; campaign_id?: string | null; product_id?: string | null; cycle_id?: string | null; title?: string } }).autopilot;
> 82	
> 83	    outPath = `/tmp/video-render-${renderId}.mp4`;
> 84	    // FR-VS-047: studio-authored projects render via the reference engine (hyperframes render → parity definitional);
> 85	    // template specs (autopilot) render via the bespoke motor. Discriminated by composition.mode.
> 86	    let result: RenderResult;
> 87	    if ((spec as StudioProjectSpec).mode === 'studio-project') {
> 88	      result = await renderStudioProject(spec as StudioProjectSpec, outPath);
> 89	    } else {
> 90	      if (!(spec as RenderSpec).props) throw new Error('composition_missing_or_invalid');
> 91	      result = await renderComposition(spec as RenderSpec, outPath);
> 92	    }
> 93	    // Honest aspect label (FR-CP-004): the engine now renders 9:16 AND 16:9 — derive from the real dimensions.
> 94	    const aspectLabel = result.width >= result.height ? '16:9' : '9:16';
> 95	
> 96	    // Upload to the private bucket under <user_id>/<render_id>.mp4 (path scopes tenant isolation).
> 97	    const storageKey = `${row.user_id}/${renderId}.mp4`;
> 98	    const bytes = readFileSync(outPath);
> 99	    const { error: upErr } = await supabase.storage
> 100	      .from(BUCKET)
> 101	      .upload(storageKey, bytes, { contentType: 'video/mp4', upsert: true });
> 102	    if (upErr) throw new Error(`upload_failed: ${upErr.message}`);
> 103	
> 104	    // Material manifest (the erasure unit, FR-VS-030).
> 105	    await supabase.from('video_assets').insert({
> 106	      user_id: row.user_id, render_id: renderId, kind: 'video',
> 107	      storage_key: storageKey, bytes: result.bytes,
> 108	    }).then(() => {}, () => {});
> 109	
> 110	    // Mesh observation (FR-VS-026) — best-effort; the embed trigger fires on insert.
> 111	    let nodeId: string | null = null;
> 112	    const { data: node } = await supabase.from('mcorch_nodes').insert({
> 113	      user_id: row.user_id, node_type: 'observation',
> 114	      name: `video-render:${renderId}`,
> 115	      content: `HyperFrames ${aspectLabel} render ${result.width}x${result.height} ${result.frames}f @${result.fps}fps (${(result.bytes / 1024).toFixed(0)}KB)`,
> 116	      metadata: { kind: 'video_render', render_id: renderId, storage_key: storageKey, bytes: result.bytes },
> 117	    }).select('id').maybeSingle();
> 118	    nodeId = node?.id ?? null;
> 119	
> 120	    // Terminal: done, refund 0 (prepaid path — the cycle already paid; the motor never self-bills here).
> 121	    const { data: fin } = await supabase.rpc('finalize_video_render', {
> 122	      p_render_id: renderId, p_state: 'done', p_storage_key: storageKey, p_qa: null, p_node_id: nodeId, p_refund: 0,
> 123	    });
> 124	
> 125	    // Dual-write to the canonical asset registry (creative_assets) so Canvas Studio / the HyperFrames editor can
> 126	    // reuse this render bidirectionally (the "power of the outputs" spine). Fail-soft — never break the render.
> 127	    try {
> 128	      await supabase.rpc('register_creative_asset', {
> 129	        p_user_id: row.user_id, p_kind: 'video',
> 130	        p_storage_bucket: BUCKET, p_storage_key: storageKey, p_is_public: false,
> 131	        p_source_module: 'hyperframes', p_source_job_id: renderId,
> 132	        p_mime_type: 'video/mp4', p_file_size_bytes: result.bytes,
> 133	        p_width: result.width, p_height: result.height,
> 134	        p_duration_seconds: result.fps > 0 ? result.frames / result.fps : null,
> 135	        p_mesh_node_id: nodeId,
> 136	        p_title: ap?.title ? `Vídeo ${aspectLabel}: ${ap.title}` : `Vídeo ${aspectLabel} ${renderId}`,
> 137	        p_metadata: { render_id: renderId, format: aspectLabel, fps: result.fps, frames: result.frames },
> 138	      });
> 139	    } catch (e) {
> 140	      console.warn(`[video-bridge] creative_assets register skipped for ${renderId}:`, e instanceof Error ? e.message : e);
> 141	    }
> 142	
> 143	    // FR-VA-025 — autopilot reconciliation (the async asset arrives AFTER the cycle finalized): attach the 9:16
> 144	    // asset to the content library + a creative_metrics row keyed by the new content_variant_id. Gated on the
> 145	    // composition.autopilot context the enqueuer set; generic (editor) renders carry no autopilot block → no attach.
> 146	    if (ap?.user_id) {
> 147	      try {
> 148	        const { data: clib } = await supabase.from('content_library').insert({
> 149	          user_id: ap.user_id, campaign_id: ap.campaign_id ?? null, type: 'video',
> 150	          title: `Vídeo 9:16: ${ap.title ?? renderId}`, media_url: storageKey, status: 'approved',
> 151	          metadata: { source: 'autopilot_video', render_id: renderId, product_id: ap.product_id ?? null, cycle_id: ap.cycle_id ?? null, storage_bucket: BUCKET, format: '9:16' },
> 152	        }).select('id').maybeSingle();
> 153	        if (clib?.id) {
> 154	          // source MUST be one of the CHECK values ('affiliate_click'|'organic'|'postback') — the 9:16 video is an
> 155	          // organic creative (mirrors the article baseline). platform null = not yet bound to a vertical network
> 156	          // (PR-VA-021 deferred). UNIQUE(content_variant_id, source) is safe — the video's content_variant_id is new.
> 157	          await supabase.from('creative_metrics').insert({
> 158	            user_id: ap.user_id, cycle_id: ap.cycle_id ?? null, content_variant_id: clib.id,
> 159	            product_id: ap.product_id ?? null, platform: null, source: 'organic',
> 160	            impressions: 0, engagements: 0, affiliate_clicks: 0, revenue_cents: 0,
> 161	          }).then(() => {}, (e: unknown) => console.warn('[video-bridge] creative_metrics skipped:', e instanceof Error ? e.message : e));
> 162	        }
> 163	        console.log(`   ↳ autopilot attach: content_library video ${clib?.id ?? '(none)'}`);
> 164	      } catch (e) {
> 165	        console.warn(`[video-bridge] autopilot attach skipped for ${renderId}:`, e instanceof Error ? e.message : e);
> 166	      }
> 167	    }
> 168	
> 169	    // ── FR-CP-003 — kick the reshaper for VIDEO surfaces now that the 9:16 master is finalized (out-of-band).
> 170	    // The reshaper reexports THIS master into per-channel native variants (the 7-channel spine, anti cross-post).
> 171	    // Idempotent (channel_variants UNIQUE) + fail-soft — a reshape hiccup never breaks the render.
> 172	    // SSOT: docs/bok/post-engine/13-sdd-reshaper-atomizer.md §4.
> 173	    const pillarRunId = (spec as { pillar_run_id?: string; autopilot?: { pillar_run_id?: string } }).pillar_run_id
> 174	      ?? (spec as { autopilot?: { pillar_run_id?: string } }).autopilot?.pillar_run_id ?? null;
> 175	    if (pillarRunId) {
> 176	      try {
> 177	        await fetch(`${SUPABASE_URL}/functions/v1/reshape-pillar`, {
> 178	          method: 'POST',
> 179	          headers: { Authorization: `Bearer ${SERVICE_KEY}`, 'Content-Type': 'application/json' },
> 180	          body: JSON.stringify({ pillar_run_id: pillarRunId, scope: 'video' }),
> 181	        });
> 182	        console.log(`   ↳ reshape kicked (video) for pillar_run ${pillarRunId}`);
> 183	      } catch (e) {
> 184	        console.warn(`[video-bridge] reshape kick skipped for ${renderId}:`, e instanceof Error ? e.message : e);
> 185	      }
> 186	    }
> 187	
> 188	    console.log(`✅ render ${renderId} done → ${storageKey} (${(result.bytes / 1024).toFixed(0)}KB, ${result.durationMs}ms)`, fin);
> 189	    await logHealth('healthy', 'render_done', { render_id: renderId, bytes: result.bytes });
> 190	  } catch (e) {
> 191	    const msg = e instanceof Error ? e.message : String(e);
> 192	    console.error(`❌ render ${renderId} failed: ${msg}`);
> 193	    // Refund the charge (failed render delivered no value). finalize is idempotent (guard state IN queued/running).
> 194	    await supabase.rpc('finalize_video_render', {
> 195	      p_render_id: renderId, p_state: 'failed', p_storage_key: null, p_qa: null, p_node_id: null, p_refund: charged,
> 196	    }).then(() => {}, () => {});
> 197	    await logHealth('error', 'render_failed', { render_id: renderId, error: msg });
> 198	  } finally {
> 199	    if (outPath) rmSync(outPath, { force: true });
> 200	  }
> 201	}
> 202	
> 203	/** One drain pass: claim + render every queued hyperframes render. Returns count processed. */
> 204	async function drainOnce(): Promise<number> {
> 205	  // Reap renders stuck in 'running' past the timeout (dead worker) → back to queued for re-claim.
> 206	  const cutoff = new Date(Date.now() - RUNNING_TIMEOUT_MS).toISOString();
> 207	  await supabase.from('video_renders')
> 208	    .update({ state: 'queued' })
> 209	    .eq('engine', 'hyperframes').eq('state', 'running').lt('updated_at', cutoff)
> 210	    .then(() => {}, () => {});
> 211	
> 212	  const { data: queued, error } = await supabase
> 213	    .from('video_renders')
> 214	    .select('id')
> 215	    .eq('engine', 'hyperframes').eq('state', 'queued')
> 216	    .order('created_at', { ascending: true })
> 217	    .limit(10);
> 218	  if (error || !queued?.length) return 0;
> 219	
> 220	  let n = 0;
> 221	  for (const q of queued) {
> 222	    const row = await claim(q.id);
> 223	    if (!row) continue; // already claimed by another worker
> 224	    await processRender(row as any);
> 225	    n++;
> 226	  }
> 227	  return n;
> 228	}
> 229	
> 230	async function main() {
> 231	  const once = process.argv.includes('--once');
> 232	  if (once) {
> 233	    const n = await drainOnce();
> 234	    console.log(`drained ${n} render(s)`);
> 235	    process.exit(0);
> 236	  }
> 237	  console.log('🎬 video-bridge running — polling video_renders (engine=hyperframes, queued)...');
> 238	  await logHealth('healthy', 'worker_started');
> 239	  // eslint-disable-next-line no-constant-condition
> 240	  while (true) {
> 241	    try {
> 242	      await drainOnce();
> 243	    } catch (e) {
> 244	      console.error('poll cycle error:', e);
> 245	      await logHealth('degraded', 'poll_error', { error: e instanceof Error ? e.message : String(e) });
> 246	    }
> 247	    await new Promise((r) => setTimeout(r, POLL_MS));
> 248	  }
> 249	}
> 250	
> 251	main();
> 252	
> ```

## 🤖 Claude *(04:39:15)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "systemctl --user status video-bridge.service --no-pager -l 2>&1 | head -50",
  "description": "Check video-bridge systemd service status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ● video-bridge.service - MCORCH HyperFrames Video Bridge (polls video_renders engine=hyperframes, renders HTML→MP4 9:16 via Playwright+FFmpeg)
>      Loaded: loaded (/home/ubuntu/.config/systemd/user/video-bridge.service; enabled; preset: enabled)
>      Active: active (running) since Wed 2026-07-01 18:44:23 -03; 5 days ago
>    Main PID: 3956182 (bun)
>       Tasks: 19 (limit: 28691)
>      Memory: 123.1M (peak: 856.8M swap: 1020.0K swap peak: 1.3M)
>         CPU: 1h 15min 13.033s
>      CGroup: /user.slice/user-1001.slice/user@1001.service/app.slice/video-bridge.service
>              ├─3956182 /home/ubuntu/.bun/bin/bun run scripts/video-bridge.ts
>              └─3956968 /home/gcrUX/htdocs/constellation-orchestra/node_modules/@hyperframes/core/node_modules/esbuild/node_modules/@esbuild/linux-arm64/bin/esbuild --service=0.25.12 --ping
> 
> Jul 01 18:46:52 panel.gcrux.com bun[3956182]: }
> Jul 01 19:01:48 panel.gcrux.com bun[3956182]: ✅ render b25838a0-fca3-4133-b1d5-670d2cb780e8 done → ada39fae-67e1-4e53-af1c-5a18e1c108e8/b25838a0-fca3-4133-b1d5-670d2cb780e8.mp4 (378KB, 127336ms) {
> Jul 01 19:01:48 panel.gcrux.com bun[3956182]:   refunded: 0,
> Jul 01 19:01:48 panel.gcrux.com bun[3956182]:   finalized: true,
> Jul 01 19:01:48 panel.gcrux.com bun[3956182]: }
> Jul 04 00:30:23 panel.gcrux.com bun[3956182]: ✅ render 3d83ed7e-1b7c-4378-8c09-7068fdc467dc done → ada39fae-67e1-4e53-af1c-5a18e1c108e8/3d83ed7e-1b7c-4378-8c09-7068fdc467dc.mp4 (583KB, 119844ms) {
> Jul 04 00:30:23 panel.gcrux.com bun[3956182]:   refunded: 0,
> Jul 04 00:30:23 panel.gcrux.com bun[3956182]:   finalized: true,
> Jul 04 00:30:23 panel.gcrux.com bun[3956182]: }
> Jul 06 23:43:20 panel.gcrux.com bun[3956182]: ❌ render 0537b99d-eab0-410d-9dde-c792beaa1c79 failed: composition_missing_or_invalid
> ```

## 🤖 Claude *(04:39:27)*


## 🤖 Claude *(04:39:29)*

Encontrei a falha exata no log do systemd. Vou confirmar a causa checando a linha de código que lança esse erro e como a composition é populada no enqueue.

## 🤖 Claude *(04:39:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "journalctl --user -u video-bridge.service --since \"2026-07-06 23:40:00\" --until \"2026-07-07 08:00:00\" --no-pager 2>&1 | head -100",
  "description": "Full journal window around the failure"
}
```

## 🤖 Claude *(04:39:31)*


🛠️ **Tool Call**: `Grep`
```json
{
  "pattern": "video_renders.*insert|from\\('video_renders'\\)\\.insert|composition:",
  "path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions",
  "-n": true,
  "output_mode": "content"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Jul 06 23:43:20 panel.gcrux.com bun[3956182]: ❌ render 0537b99d-eab0-410d-9dde-c792beaa1c79 failed: composition_missing_or_invalid
> ```

> **Tool Result (Grep)** - ✅ Success
>
> ```
> supabase/functions/reshape-pillar/index.ts:228:    let renders: Array<{ storage_key: string | null; state: string; composition: unknown }> = [];
> supabase/functions/reshape-pillar/index.ts:266:        await admin.from("video_renders").insert({
> supabase/functions/orchestrate-step/index.ts:527:                const { data: vr, error: vrErr } = await admin.from("video_renders").insert({
> ```

## 🤖 Claude *(04:39:39)*


## 🤖 Claude *(04:39:40)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/reshape-pillar/index.ts",
  "offset": 190,
  "limit": 100
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 190	    const { data: run } = await admin.from("pipeline_runs").select("user_id, metadata").eq("id", pillarRunId).maybeSingle();
> 191	    if (!run?.user_id) {
> 192	      return new Response(JSON.stringify({ error: "run_not_found" }), { status: 404, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 193	    }
> 194	    const userId: string = run.user_id;
> 195	    const campaignId: string | null = (run.metadata as { campaign_id?: string } | null)?.campaign_id ?? null;
> 196	    // Publish opt-in (Sovereign directive 2026-06-28): when the run did NOT opt into auto-publish, the reshaper
> 197	    // still produces every native variant but leaves them as DRAFTS (no scheduled_posts). The user reviews and
> 198	    // publishes via publish-channel-variant. Default false = draft. SSOT: post-engine/13-sdd §5.2.
> 199	    const autoPublish = (run.metadata as { auto_publish?: boolean } | null)?.auto_publish === true;
> 200	    // FR-CP-004 long-form opt-in: a 16:9 YouTube long render is enqueued ONLY when explicitly requested (default
> 201	    // off ⇒ pillar_video_16x9 stays 'gap'). Keeps the autopilot short-form-only; never a silent extra render.
> 202	    const longForm = (run.metadata as { long_form?: boolean } | null)?.long_form === true;
> 203	
> 204	    // ── Load the atomized pillar (latest for this run; reshaper tolerates a heuristic-only row) ──
> 205	    const { data: atomsRow } = await admin.from("pillar_atoms")
> 206	      .select("hook, key_points, stat, quote, cta, pillar_url")
> 207	      .eq("pillar_run_id", pillarRunId).order("created_at", { ascending: false }).limit(1).maybeSingle();
> 208	    if (!atomsRow) {
> 209	      await pulse("reshape-pillar", "degraded", "no_atoms", { scope });
> 210	      return new Response(JSON.stringify({ ok: false, error: "no_pillar_atoms", processed: [] }), { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 211	    }
> 212	    const atoms: Atoms = atomsRow as Atoms;
> 213	
> 214	    // ── Load active channel profiles (system rows + this tenant's overrides), ordered by priority ──
> 215	    const { data: profiles } = await admin.from("channel_profiles")
> 216	      .select("channel, surface, priority, video, image, text, publish_path, voice_prompt_seed, transform_recipe")
> 217	      .eq("is_active", true).or(`user_id.is.null,user_id.eq.${userId}`).order("priority", { ascending: true });
> 218	    if (!profiles?.length) {
> 219	      return new Response(JSON.stringify({ ok: true, processed: [], scheduled: 0, note: "no_active_profiles" }), { headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 220	    }
> 221	
> 222	    // ── Resolve source assets (best-effort; missing master/image ⇒ honest pending_* status, not a crash) ──
> 223	    // Two video masters can exist per run: the 9:16 spine (template viral-short-9x16, from orchestrate-step) and
> 224	    // the 16:9 long-form (template viral-long-16x9, enqueued here on long_form). Distinguish by composition.template.
> 225	    let videoMaster9x16: { bucket: string; key: string } | null = null;
> 226	    let videoMaster16x9: { bucket: string; key: string } | null = null;
> 227	    const needRenders = scope === "video" || scope === "all" || longForm;
> 228	    let renders: Array<{ storage_key: string | null; state: string; composition: unknown }> = [];
> 229	    if (needRenders) {
> 230	      const { data } = await admin.from("video_renders")
> 231	        .select("storage_key, state, composition")
> 232	        .eq("user_id", userId)
> 233	        .order("created_at", { ascending: false }).limit(40);
> 234	      renders = (data ?? []) as typeof renders;
> 235	      const matchesRun = (c: { pillar_run_id?: string; autopilot?: { pillar_run_id?: string } } | null) =>
> 236	        c?.pillar_run_id === pillarRunId || c?.autopilot?.pillar_run_id === pillarRunId;
> 237	      for (const r of renders) {
> 238	        const c = r.composition as { template?: string; pillar_run_id?: string; autopilot?: { pillar_run_id?: string } } | null;
> 239	        if (r.state !== "done" || !r.storage_key || !matchesRun(c)) continue;
> 240	        if (String(c?.template ?? "") === "viral-long-16x9") { if (!videoMaster16x9) videoMaster16x9 = { bucket: "video-studio-assets", key: r.storage_key }; }
> 241	        else if (!videoMaster9x16) videoMaster9x16 = { bucket: "video-studio-assets", key: r.storage_key }; // 9:16 (or legacy untemplated)
> 242	      }
> 243	    }
> 244	
> 245	    // ── FR-CP-004 — enqueue the 16:9 long-form render (opt-in). SINGLE-TENANT charged_mco=0: the reshaper is
> 246	    //    service-role and cannot self-debit (deduct_mco_coins is auth.uid()-self-only); refund-on-fail is therefore
> 247	    //    0 (NO mint). Multi-tenant billing (a service-role debit RPC) is OTD-CP-008-BILLING. Idempotent. ──
> 248	    if ((scope === "static" || scope === "all") && longForm) {
> 249	      const has16x9 = renders.some((r) => {
> 250	        const c = r.composition as { template?: string; pillar_run_id?: string } | null;
> 251	        return String(c?.template ?? "") === "viral-long-16x9" && c?.pillar_run_id === pillarRunId;
> 252	      });
> 253	      if (!has16x9) {
> 254	        const clip = (s: unknown, n: number) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
> 255	        const composition = {
> 256	          template: "viral-long-16x9", width: 1920, height: 1080, duration_s: 8, fps: 24,
> 257	          props: {
> 258	            hook: clip(atoms.hook, 90),
> 259	            caption: clip(atomArray(atoms.key_points).slice(0, 2).join(". "), 160),
> 260	            cta: clip(atoms.cta, 40) || "Inscreva-se",
> 261	            brand: "Gabriel AI",
> 262	            product_image_url: "",
> 263	          },
> 264	          pillar_run_id: pillarRunId,
> 265	        };
> 266	        await admin.from("video_renders").insert({
> 267	          user_id: userId, engine: "hyperframes", state: "queued", topic: clip(atoms.hook, 200),
> 268	          charged_mco: 0, composition,
> 269	        }).then(() => {}, (e: unknown) => console.warn("[reshape-pillar] 16:9 enqueue skipped:", e instanceof Error ? e.message : e));
> 270	      }
> 271	    }
> 272	    let pillarImage: { bucket: string; key: string } | null = null;
> 273	    if (scope === "static" || scope === "all") {
> 274	      // Two-step resolution (SOP channel-reshaper Amendment 2026-07-02): autopilot runs carry campaign_id NULL
> 275	      // (campaigns is a Marketing Hub FK the cycle never mints), so a campaign-only match can never fire for them
> 276	      // — that left every image surface 'gap' on cycle 77e02fca. The run-scoped tag (metadata.pillar_run_id, set
> 277	      // by orchestrate-step at the image insert) is the 1:1 server-set anchor; campaign match stays as the
> 278	      // fallback for Marketing Hub flows and rows older than the tag.
> 279	      let { data: img } = await admin.from("content_library")
> 280	        .select("media_url, metadata")
> 281	        .eq("user_id", userId).eq("type", "image")
> 282	        .eq("metadata->>pillar_run_id", pillarRunId)
> 283	        .order("created_at", { ascending: false }).limit(1).maybeSingle();
> 284	      if (!img && campaignId) {
> 285	        const { data: img2 } = await admin.from("content_library")
> 286	          .select("media_url, metadata")
> 287	          .eq("user_id", userId).eq("type", "image").eq("campaign_id", campaignId)
> 288	          .order("created_at", { ascending: false }).limit(1).maybeSingle();
> 289	        img = img2;
> ```

## 🤖 Claude *(04:39:41)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/orchestrate-step/index.ts",
  "offset": 470,
  "limit": 80
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 470	                body: JSON.stringify({ prompt: imgPrompt, style: "product photography", user_id: run.user_id }),
> 471	              });
> 472	              const imgData = await imgRes.json().catch(() => ({} as any));
> 473	              if (imgRes.ok && imgData?.path) {
> 474	                const { data: imgRow } = await admin.from("content_library").insert({
> 475	                  user_id: run.user_id, campaign_id: campaign_id || null, type: "image",
> 476	                  title: `Imagem: ${articleTitle}`, media_url: imgData.path, status: "approved",
> 477	                  // pillar_run_id = run-scoped anchor the reshaper resolves the pillar image by (autopilot runs
> 478	                  // have campaign_id NULL — SOP channel-reshaper Amendment 2026-07-02).
> 479	                  metadata: { source: "orchestration", products: products.map((p) => p.external_id), product_id: p0.external_id, storage_bucket: "generated-images", pillar_run_id: run_id },
> 480	                }).select("id").single();
> 481	                await addStep("image_generation", "done", { product: p0.name }, { content_id: imgRow?.id ?? null, path: imgData.path });
> 482	              } else {
> 483	                console.warn("[orchestrate-step] image generation skipped (fail-open):", imgData?.error ?? imgRes.status);
> 484	                await addStep("image_generation", "skipped", { product: p0.name }, { reason: imgData?.error ?? `image_http_${imgRes.status}` });
> 485	              }
> 486	            } catch (e: any) {
> 487	              console.warn("[orchestrate-step] image generation fail-open:", e?.message);
> 488	              await addStep("image_generation", "skipped", { product: products[0]?.name }, { reason: e?.message || "image_exception" });
> 489	            }
> 490	
> 491	            // ── Viral Autopilot Fatia VA-V1 — product-aware 9:16 video composition (FR-VA-023/024) ──────────────
> 492	            // FAIL-OPEN (status 'skipped', never 'error'): the video NEVER breaks the run. The cost was pre-debited
> 493	            // in the cycle (OTD-VA-010); we INSERT a queued HyperFrames render with charged_mco=VIDEO_COST as a
> 494	            // MARKER (no deduct here — orchestrate-step never bills) → the host worker (video-bridge.ts) polls,
> 495	            // renders 1080×1920, and on failure finalize_video_render(failed, refund=VIDEO_COST) credits it back.
> 496	            // Props use the actual viral angle (title/description) + the ML product photo (public https). The
> 497	            // template renders all text via textContent (XSS-safe); product name already passed the sentinel
> 498	            // upstream (orchestrate-content). composition.autopilot carries the attach context (FR-VA-025).
> 499	            if (videoEnabled) {
> 500	              const VIDEO_COST = 12; // VIDEO_HYPERFRAMES_RENDER (billing.ts:39) — mirrors autopilot-run projected.
> 501	              let enqueued = false;  // tracks whether a video_renders row was actually created (billing reconciliation).
> 502	              try {
> 503	                const p0 = products[0];
> 504	                const clip = (s: unknown, n: number) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
> 505	                const productImg = typeof (p0 as any)?.image_url === "string" && /^https:\/\//i.test((p0 as any).image_url)
> 506	                  ? (p0 as any).image_url : "";
> 507	                const composition = {
> 508	                  template: "viral-short-9x16",
> 509	                  // 5s × 24fps = 120 frames ≈ 65s render — within NFR-VS-002 (p95 < 90s). The screenshot-per-frame
> 510	                  // capture (~0.5s/frame) is the bottleneck; OTD-VA-013 tracks the CDP-screencast optimization to
> 511	                  // unlock longer/faster clips. 5s is a strong viral-short length.
> 512	                  duration_s: 5,
> 513	                  fps: 24,
> 514	                  props: {
> 515	                    hook: clip(articleTitle, 80) || clip(topic, 80),
> 516	                    caption: clip(args.meta_description, 150) || clip(`${p0.name}`, 150),
> 517	                    cta: "Ver no Mercado Livre",
> 518	                    brand: "MCORCH",
> 519	                    product_image_url: productImg,
> 520	                  },
> 521	                  // Attach context for the worker's reconciliation (FR-VA-025) — NOT rendered, only routing.
> 522	                  // pillar_run_id (FR-CP-003 gap #5): lets video-bridge JOIN the finished master back to pillar_atoms
> 523	                  // so the reshaper can reexport per-channel native variants from THIS run's 9:16 master.
> 524	                  pillar_run_id: run_id,
> 525	                  autopilot: { user_id: run.user_id, campaign_id: campaign_id || null, product_id: p0.external_id, cycle_id: cycleId, title: clip(articleTitle, 120), pillar_run_id: run_id },
> 526	                };
> 527	                const { data: vr, error: vrErr } = await admin.from("video_renders").insert({
> 528	                  user_id: run.user_id, engine: "hyperframes", state: "queued",
> 529	                  product_id: null, // logical product is the ML external_id (text) — kept in composition.autopilot
> 530	                  topic: clip(topic, 200), charged_mco: VIDEO_COST, composition,
> 531	                }).select("id").single();
> 532	                if (vrErr || !vr) throw new Error(vrErr?.message || "video_render_insert_failed");
> 533	                enqueued = true;
> 534	                await addStep("video_generation", "done", { product: p0.name, format: "9:16" }, { render_id: vr.id });
> 535	              } catch (e: any) {
> 536	                console.warn("[orchestrate-step] video enqueue fail-open:", e?.message);
> 537	                await addStep("video_generation", "skipped", { product: products[0]?.name }, { reason: e?.message || "video_exception" });
> 538	                // Billing-accuracy fix (OTD-VA-010 gap): the cycle ALREADY counted VIDEO_COST for this succeeded
> 539	                // sub-run (autopilot-run `actual = succeeded × (ORCH_COST + VIDEO_COST)`, computed BEFORE this async
> 540	                // step ran). If NO render row was created (`!enqueued`), finalize_video_render can never refund it →
> 541	                // the tenant would be charged for a render never queued. Issue the idempotent compensating credit
> 542	                // (anchored on run_id; mirrors the render-fail refund for the no-row case). Only on the cron/cycle
> 543	                // path (cycleId set); user-path renders never reach here. If `enqueued` is true, the row exists and
> 544	                // the render lifecycle / finalize_video_render owns the refund — do NOT double-credit.
> 545	                if (!enqueued && cycleId) {
> 546	                  const { error: refundErr } = await admin.rpc("refund_autopilot_video_enqueue", {
> 547	                    p_run_id: run_id, p_cycle_id: cycleId, p_user_id: run.user_id, p_amount: VIDEO_COST,
> 548	                  });
> 549	                  if (refundErr) {
> ```

## 🤖 Claude *(04:39:49)*


## 🤖 Claude *(04:39:50)*


🛠️ **Tool Call**: `Grep`
```json
{
  "pattern": "mode.*studio-project|studio-project",
  "path": "/home/gcrUX/htdocs/constellation-orchestra/src",
  "-n": true,
  "output_mode": "files_with_matches"
}
```

> **Tool Result (Grep)** - ✅ Success
>
> ```
> No files found
> ```

## 🤖 Claude *(04:39:51)*


🛠️ **Tool Call**: `Glob`
```json
{
  "pattern": "scripts/qa/gen-user-jwt.ts"
}
```

> **Tool Result (Glob)** - ✅ Success
>
> ```
> scripts/qa/gen-user-jwt.ts
> ```

## 🤖 Claude *(04:39:52)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "journalctl --user -u video-bridge.service --since \"2026-07-06 23:00:00\" --until \"2026-07-06 23:45:00\" --no-pager 2>&1 | tail -60",
  "description": "Look for context lines right before the failure"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Jul 06 23:43:20 panel.gcrux.com bun[3956182]: ❌ render 0537b99d-eab0-410d-9dde-c792beaa1c79 failed: composition_missing_or_invalid
> ```

## 🤖 Claude *(04:39:58)*


## 🤖 Claude *(04:40:00)*


🛠️ **Tool Call**: `Grep`
```json
{
  "pattern": "video_renders.*\\.insert\\(|composition:\\s*\\{",
  "path": "/home/gcrUX/htdocs/constellation-orchestra",
  "-n": true,
  "output_mode": "content",
  "glob": "*.{ts,tsx}"
}
```

> **Tool Result (Grep)** - ✅ Success
>
> ```
> scripts/video-studio-host/adapter.ts:133:            composition: { mode: 'studio-project', project_dir: opts.project.dir, fps, resolution },
> supabase/functions/orchestrate-step/index.ts:527:                const { data: vr, error: vrErr } = await admin.from("video_renders").insert({
> supabase/functions/reshape-pillar/index.ts:266:        await admin.from("video_renders").insert({
> ```

## 🤖 Claude *(04:40:03)*


## 🤖 Claude *(04:40:04)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/video-studio-host/adapter.ts",
  "offset": 80,
  "limit": 80
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 80	      const { bundleToSingleHtml } = await import('@hyperframes/core/compiler');
> 81	      return await bundleToSingleHtml(projectDir);
> 82	    } catch (e) {
> 83	      console.error(`[studio-host] bundle failed: ${e instanceof Error ? e.message : e}`);
> 84	      return null;
> 85	    }
> 86	  },
> 87	
> 88	  getProjectSignature: (projectDir: string) => createProjectSignature(projectDir),
> 89	
> 90	  async lint(html: string): Promise<LintResult> {
> 91	    try {
> 92	      const { lintHyperframeHtml } = await import('@hyperframes/core/lint');
> 93	      const r = await lintHyperframeHtml(html);
> 94	      const findings = (r as { findings?: Array<{ severity?: string; message?: string; file?: string; fixHint?: string }> }).findings ?? [];
> 95	      return { findings: findings.map((f) => ({ severity: String(f.severity ?? 'info'), message: String(f.message ?? ''), file: f.file, fixHint: f.fixHint })) };
> 96	    } catch {
> 97	      return { findings: [] }; // lint is advisory — never block the editor on a linter crash
> 98	    }
> 99	  },
> 100	
> 101	  // Same-origin static route (server.ts) — the Apache-2.0 runtime IIFE from the core package, never a CDN.
> 102	  runtimeUrl: '/__hf/runtime.js',
> 103	
> 104	  rendersDir(project: ResolvedProject): string {
> 105	    const dir = join(project.dir, 'renders');
> 106	    mkdirSync(dir, { recursive: true });
> 107	    return dir;
> 108	  },
> 109	
> 110	  /**
> 111	   * FR-VS-048 (A) — the render seam. Returns the job state synchronously and mutates it reactively
> 112	   * (the SSE progress route polls it). The submit goes through `video-render` (charge-at-entry +
> 113	   * refund-on-failure live THERE); the host only observes video_renders and materializes the output.
> 114	   */
> 115	  startRender(opts): RenderJobState {
> 116	    const state: RenderJobState = { id: opts.jobId, status: 'rendering', progress: 0, outputPath: opts.outputPath };
> 117	
> 118	    (async () => {
> 119	      const fps = fpsToInt(opts.fps);
> 120	      const resolution = opts.outputResolution && VALID_RESOLUTIONS.has(String(opts.outputResolution))
> 121	        ? String(opts.outputResolution) : 'portrait';
> 122	
> 123	      // 1) Submit through the billing chokepoint with a real minted User Zero JWT (re-mint once on 401).
> 124	      let res: Response | null = null;
> 125	      for (let attempt = 0; attempt < 2; attempt++) {
> 126	        const jwt = await mintUserZeroJwt(attempt > 0);
> 127	        res = await fetch(`${SUPABASE_URL}/functions/v1/video-render`, {
> 128	          method: 'POST',
> 129	          headers: { Authorization: `Bearer ${jwt}`, 'Content-Type': 'application/json' },
> 130	          body: JSON.stringify({
> 131	            engine: 'hyperframes',
> 132	            topic: `studio:${opts.project.id}`,
> 133	            composition: { mode: 'studio-project', project_dir: opts.project.dir, fps, resolution },
> 134	          }),
> 135	        });
> 136	        if (res.status !== 401) break;
> 137	      }
> 138	      const body = await res!.json().catch(() => ({} as Record<string, unknown>));
> 139	      if (res!.status !== 202) {
> 140	        // Honest surface (PT-BR reaches the studio UI). 503 = billing gate OFF (Fila Sovereign) — no charge happened.
> 141	        state.status = 'failed';
> 142	        state.error = String((body as { detail?: string; error?: string }).detail ?? (body as { error?: string }).error ?? `video-render HTTP ${res!.status}`);
> 143	        return;
> 144	      }
> 145	      const renderId = String((body as { render_id?: string }).render_id ?? '');
> 146	      state.stage = `submetido (render ${renderId.slice(0, 8)})`;
> 147	      state.progress = 0.1;
> 148	
> 149	      // 2) Observe the ledger row until the worker (video-bridge, native FR-VS-050 engine) finishes.
> 150	      const t0 = Date.now();
> 151	      while (Date.now() - t0 < RENDER_TIMEOUT_MS) {
> 152	        await new Promise((r) => setTimeout(r, RENDER_POLL_MS));
> 153	        const { data: row } = await admin.from('video_renders').select('state, user_id').eq('id', renderId).maybeSingle();
> 154	        if (!row) continue;
> 155	        if (row.state === 'running') { state.progress = Math.min(0.8, state.progress + 0.1); state.stage = 'renderizando (nativo)'; continue; }
> 156	        if (row.state === 'failed') { state.status = 'failed'; state.error = 'Render falhou no worker — mcoCoins reembolsados (finalize_video_render).'; return; }
> 157	        if (row.state === 'done') {
> 158	          // 3) Materialize the bucket MP4 at the path the studio routes serve.
> 159	          const key = `${row.user_id}/${renderId}.mp4`;
> ```

## 🤖 Claude *(04:40:14)*


## 🤖 Claude *(04:40:15)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "find /home/gcrUX/htdocs/constellation-orchestra/supabase/functions -iname \"*video-render*\" -o -iname \"*video_render*\" 2>&1",
  "description": "Locate the video-render edge function"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render
> /home/gcrUX/htdocs/constellation-orchestra/supabase/functions/video-render-poll
> ```

## 🤖 Claude *(04:40:18)*


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
> 57	    // HyperFrames render spec (FR-VS-024). The host worker (video-bridge.ts) consumes it. Untrusted props are
> 58	    // sanitized/escaped UPSTREAM (FR-VA-023 / SOP autopilot-video-9x16 G1) and rendered via textContent (XSS-safe);
> 59	    // here the spec is only transported into the queued row.
> 60	    const composition = engine === "hyperframes" && body?.composition && typeof body.composition === "object"
> 61	      ? body.composition : null;
> 62	
> 63	    // Voice-consent gate (FR-VS-032): faceless clones a voice (VoxCPM) → identifiable biometric (LGPD Art. 11).
> 64	    if (engine === "faceless" && !voiceConsent) {
> 65	      return json({ error: "voice_consent_required", action: "Confirme o consentimento de uso de voz para gerar o vídeo faceless." }, 409);
> 66	    }
> 67	
> 68	    // BYOK fail-closed (FR-VS-005/006): faceless needs the tenant's Gemini/Google key (director + vision QA). Per-user
> 69	    // first; NO silent global fallback in a user-facing path (API Tenancy Model). hyperframes is deterministic (no AI leg).
> 70	    // The canonical Vault column is `google_api_key` (NOT `gemini_api_key` — the BoK 06 §2.5 / CLAUDE.md naming is
> 71	    // stale; canvas-execute + the live decrypted view use google_api_key, verified 2026-06-22 via 42703 on gemini_api_key).
> 72	    if (engine === "faceless") {
> 73	      const { data: keys } = await admin
> 74	        .from("decrypted_user_api_keys").select("google_api_key").eq("user_id", userId).maybeSingle();
> 75	      if (!keys?.google_api_key) {
> 76	        return json({ error: "gemini_not_configured", action: "Configure sua chave Gemini/Google em /dashboard/settings para gerar vídeo." }, 402);
> 77	      }
> 78	    }
> 79	
> 80	    const cost = COST[engine];
> 81	
> 82	    // dry_run: cost projection WITHOUT deduct or row (zero-cost proof path; mirrors autopilot-run).
> 83	    if (dryRun) return json({ ok: true, dry_run: true, engine, cost_mco: cost });
> 84	
> 85	    // Engine-availability gate (SLICE 1): the worker webhook is unset until slice 2 wires the render engine.
> 86	    // Returning 503 HERE — before any deduct — guarantees no tenant is charged for a render that cannot complete.
> 87	    const workerWebhook = engine === "faceless"
> 88	      ? Deno.env.get("VIDEO_FACELESS_WEBHOOK")
> 89	      : Deno.env.get("VIDEO_HYPERFRAMES_WEBHOOK");
> 90	    if (!workerWebhook) {
> 91	      return json({
> 92	        error: "render_engine_unavailable",
> 93	        detail: `O motor de render '${engine}' entra na Fatia 2 (faceless: ponte de rede + n8n; hyperframes: sandbox). Nenhum mcoCoin foi debitado.`,
> 94	      }, 503);
> 95	    }
> 96	
> 97	    // ── SLICE 2 prepaid path (activates once the worker webhook env is set) ──────────────────────────────────────
> 98	    // Charge-at-entry (FR-VS-009): atomic deduct BEFORE any leg. 402 if balance < cost (zero rows created).
> 99	    const { error: deductErr } = await admin.rpc("deduct_mco_coins", { p_user_id: userId, p_amount: cost });
> 100	    if (deductErr) {
> 101	      logHealth("degraded", "insufficient_balance");
> 102	      return json({ error: "insufficient_balance", detail: `Saldo insuficiente: render '${engine}' custa ${cost} mcoCoins.`, cost_mco: cost }, 402);
> 103	    }
> 104	
> 105	    // INSERT the queued render (service key — RLS denies tenant writes; this is the only writer). org_id/client_id
> 106	    // NULL = solo creator (§AG agency scoping wires in a later slice).
> 107	    const { data: render, error: insErr } = await admin
> 108	      .from("video_renders")
> 109	      .insert({ user_id: userId, engine, topic, product_id: productId, composition, voice_consent: voiceConsent, charged_mco: cost, state: "queued" })
> 110	      .select("id").single();
> 111	    if (insErr || !render) {
> 112	      // Could not even create the ledger row → refund the just-charged cost (no render_id yet → direct credit).
> 113	      await admin.rpc("add_mco_coins", { p_user_id: userId, p_amount: cost }).then(() => {}, () => {});
> 114	      logHealth("error", "insert_failed");
> 115	      return json({ error: "render_create_failed", detail: insErr?.message }, 500);
> 116	    }
> 117	    const renderId = render.id as string;
> 118	
> 119	    // Trigger the worker. Two transports:
> 120	    //   • poll://  → a HOST worker (video-bridge.ts for hyperframes) POLLS video_renders; the queued row IS the
> 121	    //                trigger (Edge fns can't reach a host daemon — the design-bridge lesson). No kick → 202; the
> 122	    //                poller atomically claims (queued→running) and finalizes via finalize_video_render.
> 123	    //   • http(s)  → a reachable webhook (e.g. a faceless external studio); POST the kick, refund on failure.
> 124	    if (!workerWebhook.startsWith("poll://")) {
> 125	      try {
> 126	        const r = await fetch(workerWebhook, {
> 127	          method: "POST",
> 128	          headers: { Authorization: `Bearer ${serviceKey}`, "Content-Type": "application/json" },
> 129	          body: JSON.stringify({ render_id: renderId, user_id: userId, engine, topic, product_id: productId }),
> 130	        });
> 131	        if (!r.ok) throw new Error(`worker HTTP ${r.status}`);
> 132	      } catch (e) {
> 133	        await admin.rpc("finalize_video_render", {
> 134	          p_render_id: renderId, p_state: "failed", p_storage_key: null, p_qa: null, p_node_id: null, p_refund: cost,
> 135	        }).then(() => {}, () => {});
> 136	        logHealth("error", "worker_trigger_failed");
> 137	        return json({ error: "worker_unavailable", detail: e instanceof Error ? e.message : "trigger failed", render_id: renderId }, 502);
> 138	      }
> 139	    }
> 140	
> 141	    logHealth("healthy", "render_submitted");
> 142	    return json({ ok: true, render_id: renderId, engine, charged_mco: cost, state: "queued" }, 202);
> 143	  } catch (e) {
> 144	    logHealth("error", "exception");
> 145	    return json({ error: e instanceof Error ? e.message : "unknown" }, 500);
> 146	  }
> 147	});
> 148	
> ```

## 🤖 Claude *(04:40:42)*


## 🤖 Claude *(04:40:44)*


🛠️ **Tool Call**: `Grep`
```json
{
  "pattern": "video_renders|composition_missing_or_invalid|composition:\\s*null|composition:\\s*\\{\\}",
  "path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa",
  "-n": true,
  "output_mode": "content"
}
```

## 🤖 Claude *(04:40:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -8 -- supabase/functions/video-render/index.ts scripts/video-studio-host/adapter.ts scripts/video-bridge.ts",
  "description": "Recent history of video-render / adapter / bridge"
}
```

> **Tool Result (Grep)** - ✅ Success
>
> ```
> scripts/qa/smoke-longform-16x9.ts:10: *   G1  reshape scope=static enqueues a 16:9 render (video_renders: template viral-long-16x9, charged_mco=0, run-linked)
> scripts/qa/smoke-longform-16x9.ts:35:  const { data } = await admin.from('video_renders').select('id, composition').eq('user_id', uid);
> scripts/qa/smoke-longform-16x9.ts:57:  const { data: vr } = await admin.from('video_renders').select('charged_mco, composition').eq('user_id', uid).limit(1).maybeSingle();
> scripts/qa/smoke-longform-16x9.ts:69:    const { data } = await admin.from('video_renders').select('state, storage_key, composition').eq('user_id', uid).order('created_at', { ascending: false });
> scripts/qa/smoke-longform-16x9.ts:95:    await admin.from('video_renders').delete().eq('user_id', uid ?? '').then(() => {}, () => {});
> scripts/qa/smoke-autopilot-video-refund.ts:6: * BEFORE the async video enqueues run. A failed video_renders INSERT (fail-open 'skipped') leaves NO row → the
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 4fd9b89 feat(video-studio): Fase B 2b — FR-VS-049 Storage↔volume durability (write-back + materialize)
> 2123a79 feat(video-studio): Fase B 2a — studio host server + McorchAdapter + FR-VS-048 auth-bridge
> 8587573 feat(video-studio): FR-VS-047 studio-project render wiring (worker-side) + TDZ fix
> 2e4c3fb feat(reshaper): 16:9 YouTube long-form render (FR-CP-004, OTD-CP-008 closed)
> 2ed159f feat(reshaper): data-driven channel reshaper + atomizer — 1 pilar -> posts nativos (FR-CP-002/003/006/007/008)
> 1372cc1 feat(creative-assets): dual-write dos produtores (HyperFrames render + Canvas) → registry
> 39f8001 feat(video-studio): motor HyperFrames determinístico 9:16 vivo (Fatia VS-2)
> e3b0716 feat(video-studio): Fatia 1 — contrato edge (video-render submit + poll) + custos
> ```

## 🤖 Claude *(04:40:59)*


## 🤖 Claude *(04:41:00)*


🛠️ **Tool Call**: `Grep`
```json
{
  "pattern": "video-render|functions/v1/video-render",
  "path": "/home/gcrUX/htdocs/constellation-orchestra/src",
  "-n": true,
  "output_mode": "content"
}
```

> **Tool Result (Grep)** - ✅ Success
>
> ```
> src/hooks/useVideoRender.ts:2:// (Harness Engineering). Lists the tenant's renders (RLS own/org) + submits a render to the video-render edge fn
> src/hooks/useVideoRender.ts:24:    queryKey: ['video-renders'],
> src/hooks/useVideoRender.ts:55:      const { data, error } = await supabase.functions.invoke('video-render', {
> src/hooks/useVideoRender.ts:66:    onSuccess: () => qc.invalidateQueries({ queryKey: ['video-renders'] }),
> ```

## 🤖 Claude *(04:41:03)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useVideoRender.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// useVideoRender — video-studio render data harness (Fatia 1b). All server state via TanStack Query
> 2	// (Harness Engineering). Lists the tenant's renders (RLS own/org) + submits a render to the video-render edge fn
> 3	// (dry_run for a zero-cost cost preview; real submit returns 503 until the render engine lands in Fatia 2).
> 4	import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
> 5	import { supabase } from '@/integrations/supabase/client';
> 6	import { useAuth } from '@/hooks/useAuth';
> 7	import { edgeErrorMessage } from '@/lib/edge';
> 8	import type { Tables } from '@/integrations/supabase/types';
> 9	
> 10	export type VideoRender = Tables<'video_renders'>;
> 11	export type VideoEngine = 'faceless' | 'hyperframes';
> 12	
> 13	// Mirror of src/lib/billing.ts COIN_COSTS (provisional — OTD-VS-007, calibrate at the first paid render).
> 14	export const VIDEO_RENDER_COSTS: Record<VideoEngine, number> = { faceless: 125, hyperframes: 12 };
> 15	
> 16	export const VIDEO_ENGINES: { id: VideoEngine; label: string; desc: string }[] = [
> 17	  { id: 'faceless', label: 'Faceless', desc: 'Vídeo vertical sem rosto, narrado — pipeline E2E (Gemini → voz → motion → QA).' },
> 18	  { id: 'hyperframes', label: 'HyperFrames', desc: 'Render programático HTML → MP4, determinístico (sem IA generativa).' },
> 19	];
> 20	
> 21	export function useVideoRenders() {
> 22	  const { user } = useAuth();
> 23	  return useQuery({
> 24	    queryKey: ['video-renders'],
> 25	    enabled: !!user,
> 26	    queryFn: async (): Promise<VideoRender[]> => {
> 27	      const { data, error } = await supabase
> 28	        .from('video_renders').select('*').order('created_at', { ascending: false }).limit(50);
> 29	      if (error) throw error;
> 30	      return (data ?? []) as VideoRender[];
> 31	    },
> 32	  });
> 33	}
> 34	
> 35	export interface VideoRenderInput {
> 36	  engine: VideoEngine;
> 37	  topic?: string | null;
> 38	  voice_consent?: boolean;
> 39	  dry_run?: boolean;
> 40	}
> 41	export interface VideoRenderResult {
> 42	  ok?: boolean;
> 43	  dry_run?: boolean;
> 44	  engine?: string;
> 45	  cost_mco?: number;
> 46	  render_id?: string;
> 47	  charged_mco?: number;
> 48	  state?: string;
> 49	}
> 50	
> 51	export function useSubmitVideoRender() {
> 52	  const qc = useQueryClient();
> 53	  return useMutation({
> 54	    mutationFn: async (input: VideoRenderInput): Promise<VideoRenderResult> => {
> 55	      const { data, error } = await supabase.functions.invoke('video-render', {
> 56	        body: {
> 57	          engine: input.engine,
> 58	          topic: input.topic ?? null,
> 59	          voice_consent: !!input.voice_consent,
> 60	          dry_run: !!input.dry_run,
> 61	        },
> 62	      });
> 63	      if (error) throw new Error(await edgeErrorMessage(error, 'Falha ao gerar vídeo'));
> 64	      return data as VideoRenderResult;
> 65	    },
> 66	    onSuccess: () => qc.invalidateQueries({ queryKey: ['video-renders'] }),
> 67	  });
> 68	}
> 69	
> ```

## 🤖 Claude *(04:41:10)*


## 🤖 Claude *(04:41:10)*


🛠️ **Tool Call**: `Grep`
```json
{
  "pattern": "useSubmitVideoRender",
  "path": "/home/gcrUX/htdocs/constellation-orchestra/src",
  "-n": true,
  "output_mode": "content"
}
```

> **Tool Result (Grep)** - ✅ Success
>
> ```
> src/hooks/useVideoRender.ts:51:export function useSubmitVideoRender() {
> src/pages/VideoStudioPage.tsx:7:  useVideoRenders, useSubmitVideoRender, VIDEO_RENDER_COSTS, VIDEO_ENGINES, type VideoEngine,
> src/pages/VideoStudioPage.tsx:37:  const submit = useSubmitVideoRender();
> ```

## 🤖 Claude *(04:41:13)*


## 🤖 Claude *(04:41:14)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/VideoStudioPage.tsx",
  "offset": 1,
  "limit": 70
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// VideoStudioPage (Fatia 1b) — display-only front door for the video-studio module. All data/logic lives in
> 2	// useVideoRender (Harness Engineering). The render submit validates the full contract (consent, BYOK, cost) end to
> 3	// end; the render ENGINE itself lands in Fatia 2 (faceless = Docker bridge + n8n; hyperframes = sandbox), so a real
> 4	// submit currently returns a friendly 503 and charges nothing.
> 5	import { useState } from 'react';
> 6	import {
> 7	  useVideoRenders, useSubmitVideoRender, VIDEO_RENDER_COSTS, VIDEO_ENGINES, type VideoEngine,
> 8	} from '@/hooks/useVideoRender';
> 9	import { toast } from '@/hooks/use-toast';
> 10	import { Button } from '@/components/ui/button';
> 11	import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
> 12	import { Input } from '@/components/ui/input';
> 13	import { Label } from '@/components/ui/label';
> 14	import { Checkbox } from '@/components/ui/checkbox';
> 15	import { Badge } from '@/components/ui/badge';
> 16	import { Film, Clapperboard, Loader2, Coins, Hammer } from 'lucide-react';
> 17	
> 18	const STATE_BADGE: Record<string, string> = {
> 19	  queued: 'bg-primary/15 text-primary',
> 20	  running: 'bg-primary/15 text-primary',
> 21	  qa_gate: 'bg-accent/15 text-accent',
> 22	  done: 'bg-emerald-500/15 text-emerald-400',
> 23	  qa_failed: 'bg-amber-500/15 text-amber-400',
> 24	  failed: 'bg-red-500/15 text-red-400',
> 25	};
> 26	const STATE_LABEL: Record<string, string> = {
> 27	  queued: 'na fila',
> 28	  running: 'em execução',
> 29	  qa_gate: 'em QA',
> 30	  done: 'concluído',
> 31	  qa_failed: 'reprovado no QA',
> 32	  failed: 'falhou',
> 33	};
> 34	
> 35	export default function VideoStudioPage() {
> 36	  const { data: renders = [], isLoading } = useVideoRenders();
> 37	  const submit = useSubmitVideoRender();
> 38	  const [engine, setEngine] = useState<VideoEngine>('faceless');
> 39	  const [topic, setTopic] = useState('');
> 40	  const [voiceConsent, setVoiceConsent] = useState(false);
> 41	
> 42	  const cost = VIDEO_RENDER_COSTS[engine];
> 43	
> 44	  const onGenerate = async () => {
> 45	    if (engine === 'faceless' && !voiceConsent) {
> 46	      return toast({ title: 'Consentimento de voz necessário', description: 'O vídeo faceless clona uma voz — confirme o consentimento.', variant: 'destructive' });
> 47	    }
> 48	    try {
> 49	      const r = await submit.mutateAsync({ engine, topic: topic.trim() || null, voice_consent: voiceConsent });
> 50	      // In Fatia 2 this returns 202 {render_id}; in Fatia 1 the engine gate returns 503 (handled in catch).
> 51	      toast({ title: 'Render enfileirado', description: `render_id ${r.render_id} · ${r.charged_mco} mcoCoins` });
> 52	    } catch (e) {
> 53	      const msg = (e as Error).message;
> 54	      // Engine-unavailable (Fatia 1) is expected — surface it as info, not an error.
> 55	      const pending = /Fatia 2|render_engine_unavailable|indispon/i.test(msg);
> 56	      toast({
> 57	        title: pending ? 'Motor de render em construção' : 'Não foi possível gerar',
> 58	        description: msg,
> 59	        variant: pending ? 'default' : 'destructive',
> 60	      });
> 61	    }
> 62	  };
> 63	
> 64	  return (
> 65	    <div className="space-y-6 p-6">
> 66	      <div>
> 67	        <h1 className="flex items-center gap-2 text-2xl font-bold">
> 68	          <Film className="h-6 w-6 text-primary" /> Estúdio de Vídeo
> 69	        </h1>
> 70	        <p className="text-sm text-muted-foreground">
> ```

## 🤖 Claude *(04:41:39)*


## 🤖 Claude *(04:41:49)*

**DIAGNOSIS:** O worker `video-bridge.service` (systemd ativo, PID 3956182) processou o render `0537b99d-eab0-410d-9dde-c792beaa1c79` e falhou com `composition_missing_or_invalid` em 06 Jul 23:43:20 -03 (journalctl), erro lançado em `scripts/video-bridge.ts:74-76` quando `row.composition` é `null`/não-objeto. A causa é `supabase/functions/video-render/index.ts:60-61`, que grava `composition = null` sempre que `body.composition` não é um objeto. O caminho de UI reachável que dispara isso é `src/hooks/useVideoRender.ts:51-68` (`useSubmitVideoRender`), cujo `mutationFn` (linhas 56-61) **nunca envia `composition`** — usado por `src/pages/VideoStudioPage.tsx:37,49`, uma página "Fatia 1b" antiga cujo comentário (linha 3-4) presume que o engine `hyperframes` sempre retorna 503 antes de cobrar. Essa premissa ficou stale: o motor HyperFrames está ao vivo desde 01/07 (Fase B, commits `2123a79`/`8587573`), então o gate de disponibilidade (`video-render/index.ts:90`) não bloqueia mais, o `deduct_mco_coins` roda, a linha é inserida com `composition:null`, e o worker garantidamente falha (refund automático via `finalize_video_render`, mas gera o ciclo charge→fail→refund que o guardião está pegando).

**PROPOSED_FIX:** Em `supabase/functions/video-render/index.ts`, antes do `deduct_mco_coins` (linha ~99), adicionar uma validação para `engine === 'hyperframes'`: exigir que `composition` seja um objeto com `props` OU `mode === 'studio-project'`; caso contrário retornar 422 `{error:"composition_required"}` (mesmo padrão do 422 `engine_invalid` já existente na linha 50-52) — nunca cobrar por um render estruturalmente fadado a falhar. Secundariamente, remover/desabilitar a opção `hyperframes` do seletor genérico em `src/pages/VideoStudioPage.tsx` (linhas 16-18/38), já que a autoria real de HyperFrames hoje passa pelo Studio editor (`scripts/video-studio-host/adapter.ts`), que sempre envia `composition` válido.

**CONFIDENCE:** high

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-06 - agent-afda494dc1ce9a2f9]]
> * **Próxima Sessão**: [[2026-07-07 - MCORCH autonomous loop execution com charter e handoff]]
%% --- TIMELINE END --- %%

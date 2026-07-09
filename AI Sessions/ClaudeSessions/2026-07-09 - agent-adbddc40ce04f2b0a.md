# Session agent-adbddc40ce04f2b0a
**Date:** 2026-07-09 | **Session ID:** `agent-adbddc40ce04f2b0a`

---

## 👤 User *(06:32:09)*

Find how the /dashboard/spaces/video route works: grep App.tsx for the route; read VideoStudioEditorPage (src/pages/VideoStudioEditorPage.tsx); the StudioApiAdapter / McorchAdapter seam; nginx/video.mcorch.com.conf. GOAL: the mechanism by which a Spaces node could "open the project directly in /dashboard/spaces/video" — what identifies a video project, how the editor loads/selects one, and what a deep-link (e.g., ?project=<id>) would need to open a specific creative. Report seams, the current project identity model, and unknowns.

## 🤖 Claude *(06:32:15)*


## 🤖 Claude *(06:32:15)*

I'll investigate the `/dashboard/spaces/video` route mechanism. Let me start by examining the key files in parallel.

## 🤖 Claude *(06:32:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"spaces/video\\|canvas/video\\|VideoStudioEditor\\|spaces\" src/App.tsx 2>/dev/null | head -50",
  "description": "Grep App.tsx for video/spaces routes"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 52:const VideoStudioEditorPage = lazy(() => import("./pages/VideoStudioEditorPage.tsx"));
> 60:// FR-SPACES-022 (Amendment 14): legacy /dashboard/canvas/:id deep-links redirect 1:1 to /dashboard/spaces/:id.
> 63:  return <Navigate to={`/dashboard/spaces/${id}`} replace />;
> 145:                <Route path="spaces" element={<CanvasStudioPage />} />
> 146:                <Route path="spaces/design" element={<CanvasDesignPage />} />
> 147:                <Route path="spaces/video" element={<VideoStudioEditorPage />} />
> 148:                <Route path="spaces/assets" element={<CreativeAssetsPage />} />
> 149:                <Route path="spaces/:id" element={<CanvasEditorPage />} />
> 151:                <Route path="canvas" element={<Navigate to="/dashboard/spaces" replace />} />
> 152:                <Route path="canvas/design" element={<Navigate to="/dashboard/spaces/design" replace />} />
> 153:                <Route path="canvas/video" element={<Navigate to="/dashboard/spaces/video" replace />} />
> 154:                <Route path="canvas/assets" element={<Navigate to="/dashboard/spaces/assets" replace />} />
> ```

## 🤖 Claude *(06:32:18)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/VideoStudioEditorPage.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { Helmet } from "react-helmet-async";
> 2	
> 3	// HyperFrames Studio editor — module-container pattern (mirrors CanvasDesignPage / design.mcorch.com).
> 4	// The full multi-layer NLE editor (timeline, tracks/layers, alpha-channel video overlays, effects,
> 5	// transitions) is the official `hyperframes preview` server (systemd video-studio.service, host loopback
> 6	// 127.0.0.1:3210), served behind video.mcorch.com (Cloudflare orange + SSO gate). React 19 lives entirely
> 7	// in that standalone process → no conflict with this React 18 SPA. SDD: video-studio Amendment v0.4 (VS-UI).
> 8	export default function VideoStudioEditorPage() {
> 9	  return (
> 10	    <>
> 11	      <Helmet>
> 12	        <title>Editor de Vídeo — MCORCH</title>
> 13	        <meta name="description" content="Editor HyperFrames — composições 9:16 com cenas, camadas, overlays em alpha, efeitos e transições" />
> 14	      </Helmet>
> 15	
> 16	      <div className="w-full h-full bg-background overflow-hidden relative">
> 17	        <iframe
> 18	          src="https://video.mcorch.com"
> 19	          className="w-full h-full bg-black border-none"
> 20	          title="HyperFrames Video Studio"
> 21	          allow="clipboard-read; clipboard-write; fullscreen"
> 22	        />
> 23	      </div>
> 24	    </>
> 25	  );
> 26	}
> 27	
> ```

## 🤖 Claude *(06:32:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat nginx/video.mcorch.com.conf 2>/dev/null",
  "description": "Read nginx video vhost config"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> # MCORCH HyperFrames Video Studio — public vhost for the `hyperframes preview` NLE editor (iframe target).
> # Mirrors nginx/design.mcorch.com.conf: Cloudflare orange-proxy hides the origin IP; SSL "Full" with a
> # self-signed origin cert; the studio preview server (systemd video-studio.service) listens ONLY on host
> # loopback (127.0.0.1:3210) — this vhost is the single external path. The studio is a Vite SPA with
> # root-relative /assets + /api → it MUST be served at the ROOT of its own host (video.mcorch.com), NOT under
> # a sub-path of login.mcorch.com.
> #
> # ACTIVATION (Sovereign — DNS/cert; same runbook as design.mcorch.com / mcp.mcorch.com):
> #   1. Cloudflare DNS: A video.mcorch.com → origin IP, orange-proxied (proxied=ON).   [✅ já feito pelo Sovereign]
> #   2. Origin cert (self-signed OK behind CF Full):
> #        sudo openssl req -x509 -newkey rsa:2048 -nodes -days 3650 \
> #          -keyout /etc/nginx/ssl-certificates/video.mcorch.com.key \
> #          -out    /etc/nginx/ssl-certificates/video.mcorch.com.crt \
> #          -subj "/CN=video.mcorch.com"
> #   3. Cloudflare SSL/TLS mode: Full (já é zone-wide). WAF: SÓ se o editor (XHR/SSE) for desafiado (403
> #      text/html) — adicione um Skip rule para http.host eq "video.mcorch.com" e DESLIGUE o componente
> #      "Nível de Segurança" (datacenter-IP reputation — o toggle decisivo, ver wordpress-cf-publish-unblock.md).
> #      Para iframe em browser real normalmente NÃO dispara (passa o JS challenge).
> #   4. sudo ln -s /home/gcrUX/htdocs/constellation-orchestra/nginx/video.mcorch.com.conf \
> #        /etc/nginx/sites-enabled/ && sudo nginx -t && sudo systemctl reload nginx
> #   5. (já feito) iframe em src/pages/VideoStudioEditorPage.tsx aponta para https://video.mcorch.com.
> #
> # SECURITY: single-tenant Usuário Zero (OTD-VA-011). The preview server has NO native auth → the SSO gate
> # below (R3, sso-auth-gate :8787) is what restricts it to the logged-in MCORCH session. Multi-tenant
> # hardening (per-user project isolation) deferred to User 1.
> 
> server {
>   listen 80;
>   listen [::]:80;
>   listen 443 ssl;
>   listen [::]:443 ssl;
>   http2 on;
> 
>   ssl_certificate_key /etc/nginx/ssl-certificates/video.mcorch.com.key;
>   ssl_certificate     /etc/nginx/ssl-certificates/video.mcorch.com.crt;
> 
>   server_name video.mcorch.com;
> 
>   # Studio compositions can embed large media (alpha-channel video overlays). Allow generous uploads.
>   client_max_body_size 512m;
> 
>   # ── R3 SSO gate: every request is gated by the MCORCH session (.mcorch.com cookie) ──────────
>   # auth_request → local SSO gate (sso-auth-gate :8787) which verifies the Supabase ES256 JWT in the
>   # sb-mcorch-session cookie. 401 → 302 to login.mcorch.com/auth (the standard MCORCH login). The gate
>   # is host-agnostic (its description already names design/video.mcorch.com) — no per-host change needed.
>   location = /_mcorch_auth {
>     internal;
>     proxy_pass http://127.0.0.1:8787/verify;
>     proxy_pass_request_body off;
>     proxy_set_header Content-Length "";
>     proxy_set_header Cookie $http_cookie;
>   }
>   location @mcorch_login {
>     return 302 https://login.mcorch.com/auth?return_to=$scheme://$host$request_uri;
>   }
> 
>   # hyperframes preview server (node, systemd video-studio.service) on host loopback. SSE-friendly
>   # (render progress stream + live preview reload) over HTTP/1.1 keepalive — mirrors design/mcp
>   # (Connection "" + proxy_buffering off), so NO map $http_upgrade dependency in http{}.
>   location / {
>     auth_request /_mcorch_auth;
>     error_page 401 = @mcorch_login;
> 
>     proxy_pass http://127.0.0.1:3210;
>     proxy_http_version 1.1;
>     proxy_set_header Connection        "";
>     proxy_set_header Host              $host;
>     proxy_set_header X-Real-IP         $remote_addr;
>     proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;
>     proxy_set_header X-Forwarded-Proto $scheme;
>     proxy_buffering        off;          # editor streams (render progress SSE + preview reload) — don't buffer
>     proxy_read_timeout     3600s;
>     proxy_send_timeout     3600s;
> 
>     # ── White-label (Sovereign 2026-06-25): só a identidade visual do MCORCH, sem o logo HeyGen/HyperFrames.
>     #    Injeta CSS no <head> servido — o logo é o 1º <svg> do grupo esquerdo da top-bar; o nome do projeto é
>     #    um irmão e PERMANECE (verificado em browser: logoHidden=true, nameVisible=true). Título rebrandado.
>     #    sub_filter exige HTML do upstream NÃO-gzipado → zera Accept-Encoding pro proxy.
>     proxy_set_header   Accept-Encoding "";
>     sub_filter         '</head>' '<style>.flex.flex-col.h-full > .flex.items-center.justify-between .flex.items-center.gap-3 > svg:first-child{display:none!important}</style></head>';
>     sub_filter         '<title>HyperFrames Studio</title>' '<title>MCORCH Studio</title>';
>     sub_filter_once    off;
>   }
> }
> ```

## 🤖 Claude *(06:32:29)*


## 🤖 Claude *(06:32:29)*

The current editor is a bare iframe with no project selection. Let me investigate the adapter seam, project identity model, and the integration blueprint.

## 🤖 Claude *(06:32:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"=== grep McorchAdapter / StudioApiAdapter across repo ===\"; grep -rn \"McorchAdapter\\|StudioApiAdapter\\|startRender\\|createStudioApi\" --include=\"*.ts\" --include=\"*.tsx\" --include=\"*.md\" . 2>/dev/null | grep -v node_modules | head -40",
  "description": "Search for adapter seam references"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === grep McorchAdapter / StudioApiAdapter across repo ===
> README.md:150:- **Fase B 2a — Studio Host + McorchAdapter + FR-VS-048 (A).** `createStudioApi(mcorchAdapter)` (13 métodos §B.2) + seam `startRender`: minta JWT do Usuário Zero server-side → `video-render` edge fn (chokepoint ÚNICO de billing) → observa `video_renders` → materializa o MP4 do bucket. **E2E PAGO testemunhado** (row `b25838a0`, 12 mco, refund-path intacto) + smoke 6/6 zero-cost + SOP Lei 2. Achado: `VIDEO_HYPERFRAMES_WEBHOOK=poll://` já estava ativo (item da Fila era stale).
> README.md:236:- **Editor HyperFrames VIVO** (`video.mcorch.com`). O servidor oficial `hyperframes preview` (NLE multi-camada: cenas, camadas, overlays em alpha, efeitos, transições) roda como serviço host systemd (`video-studio.service`, node v22, 127.0.0.1:3210) atrás do vhost SSO-gated, integrado no app como módulo iframe `/dashboard/canvas/video` (Canvas Studio → Vídeo). React 19 isolado no processo standalone → zero conflito com o SPA React 18. Contrato `/api` (`StudioApiAdapter`) selado dos `.d.ts` publicados; render-parity resolvido por construção (`@hyperframes/core/runtime` compartilhado). Provado E2E (screenshot Sovereign: projeto 9:16 carregado).
> README.md:756:- **Blueprint de integração do HyperFrames Studio (deepsearch, funda Fatia VS-UI):** material-citado no repo HeyGen `@ ae8b94c5` (Apache-2.0). Achado decisivo — `StudioApp` é **zero-props**, server-backed por um `/api` REST+SSE na mesma origem; a HeyGen expôs um seam de injeção limpo (`StudioApiAdapter` de `@hyperframes/core/studio-api`). Logo **NÃO forkamos a UI**: montamos o `StudioApp` unmodified + implementamos nosso `McorchAdapter` cujo `startRender()` faz bridge pro nosso `video-render` já provado. Composição = HTML+CSS+GSAP → `bundleToSingleHtml` (o que o motor já come). React 19 → container+iframe `studio.mcorch.com`. `.claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md` (6 gates empíricos, render-parity `frame=floor(time*fps)` = maior risco).
> CLAUDE.md:439:| **HyperFrames Studio editor (Fatia VS-UI — Fase A VIVO)** | `~/.config/systemd/user/video-studio.service` (servidor oficial `hyperframes preview` node v22, host loopback `127.0.0.1:3210`, projeto 9:16 em `~/.mcorch/video-studio/projects/mcorch-video`) · `nginx/video.mcorch.com.conf` (vhost SSO-gated, espelha `design.mcorch.com`; cert+symlink = ação Sovereign) · `src/pages/VideoStudioEditorPage.tsx` (iframe `/dashboard/canvas/video`, sub-item "Vídeo" no Canvas Studio) · contrato `/api` (`StudioApiAdapter`) + Fase B (`McorchAdapter.startRender`→`video-render`) em SDD §VS-UI Amendment v0.4 · SOP `docs/processes/video-studio-editor-deploy-and-provision.md` |
> CLAUDE.md:440:| **HyperFrames Studio editor — integration blueprint (Fatia VS-UI, próximo)** | `.claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md` (deepsearch material — `StudioApp` zero-props server-backed; seam = `StudioApiAdapter` de `@hyperframes/core/studio-api`; **montar studio unmodified + nosso `McorchAdapter.startRender`→`video-render`**; composição = HTML+CSS+GSAP `bundleToSingleHtml`; React 19 → container+iframe `studio.mcorch.com`; Apache-2.0; gate #1 render-parity `frame=floor(time*fps)`. Flip OTD-VS-005 A→C) |
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:12:`/api/render/:jobId/progress`). That backend is the Hono app **`createStudioApi(adapter)`** exported from
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:13:**`@hyperframes/core/studio-api`**, parameterized by a single **`StudioApiAdapter`** interface (HeyGen's deliberate
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:17:**`McorchAdapter`** whose `startRender()` bridges to our proven `video-render` edge fn (engine=hyperframes) instead
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:27:    └── Hono: app.route("/api", createStudioApi(McorchAdapter)) + serveStatic(dist)
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:28:         McorchAdapter.startRender(opts) → POST <supabase>/functions/v1/video-render
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:31:         McorchAdapter.{listProjects,resolveProject,files,preview,lint} ← Supabase Storage / container volume
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:54:Export button → `renderQueue.startRender` → `POST /api/projects/:id/render {fps,quality,format,resolution?,composition?}`
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:56:route calls **`adapter.startRender(opts)`** (`opts={project{id,dir,title}, outputPath, format, fps, quality, jobId,
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:58:`vite.adapter.ts startRender` (swap its `@hyperframes/producer` call for our edge-fn fetch + poll). **Studio UI needs
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:63:  **`/studio-api` (Hono factory + adapter interface)**. `hono` is an **optional** peer (only for `createStudioApi`).
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:74:  serveStatic). **If startRender delegates to remote edge fn → NO Chrome/FFmpeg in the container** (lighter than CLI).
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:77:No HeyGen auth on the embedding path (`createStudioApi` is auth-agnostic; CLI's cloud/auth dirs are off-path). Relative
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:86:2. **`createStudioApi` exported from published `@hyperframes/core` dist** (it's in src exports `./studio-api`).
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:100:| R2 | Must implement whole `/api` Hono surface, not just render | **High** | Reuse `createStudioApi`; write only `McorchAdapter`; stub optional methods |
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:108:1. BoK: enumerate the mandatory `/api` route req/resp shapes (`core/studio-api/routes/*.ts`) → amend video-studio SDD with the `McorchAdapter` contract.
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:111:4. Container: React 19 host (`<StudioApp/>`) + Hono `createStudioApi(McorchAdapter)` + Dockerfile → run 127.0.0.1.
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:112:5. `McorchAdapter`: files/preview over Supabase Storage; `startRender` → `video-render` edge fn.
> .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md:117:**Sources:** github.com/heygen-com/hyperframes @ `ae8b94c5` (studio/core/cli package.json, studio/src/{index,main,App}.tsx, useRenderQueue.ts, useServerConnection.ts, vite.adapter.ts, core/src/studio-api/{index,types,createStudioApi}.ts, LICENSE) · registry.npmjs.org/@hyperframes/studio/latest · hyperframes.heygen.com · hyperframes.mintlify.app/quickstart.
> .claude/context/autonomous-loop-charter.md:178:- ✅ **Gate Lei 2 SHIPPED (it.2, 2026-06-30):** emenda BoK `video-studio` SDD **§VS-UI-B (Amendment v0.5)** (FR-VS-047/048/049) — verificação empírica Lei 1 dos pacotes **publicados** @hyperframes/studio@0.7.5 + core@0.7.5 (`npm pack` do dist) + Workflow adversarial `wf_b0a6c005-8c2` (APPROVE_WITH_FIXES). Contrato McorchAdapter completeness **PROVADA** (13 métodos = 13 call-sites reais; rotas de arquivo são FS-based → materialização Storage↔volume mandatória). **Deploy = reuso do `video.mcorch.com`** (swap do `video-studio.service` na mesma porta 3210) → **DNS `studio.mcorch.com` NÃO é mais necessário** (portão Sovereign evitado).
> .claude/context/autonomous-loop-charter.md:183:- ✅ **Sub-fatia 2a SHIPPED (loop 2026-07-01, commit `2123a79`):** `scripts/video-studio-host/` — servidor `createStudioApi(mcorchAdapter)` loopback 3211 (vanilla 3210 intocado até o swap 2c) + **McorchAdapter 13 métodos** (§B.2; FS local canônico v1) + **FR-VS-048 (A) PROVADO E2E PAGO**: startRender minta JWT User 0 → `video-render` (chokepoint) → **202 (12 mco, row `b25838a0`)** → worker **nativo FR-VS-050** → done → MP4 materializado em `renders/` **386.795B sha `c721f8f4` (4º render byte-idêntico em 4 contextos)** → download HTTP 200 → SSE `complete`. Smoke **6/6** zero-cost (`smoke-studio-host.ts`) + SOP Lei 2 (`video-studio-host-fase-b.md`). **ACHADO: `VIDEO_HYPERFRAMES_WEBHOOK=poll://` JÁ ESTÁ ATIVO** (billing do editor-render vivo — item da Fila era stale; débito real testemunhado 4636→4624).
> HANDOFF.md:100:**Pendente (Sovereign-side / próximo arco):** testes LIVE do Sovereign (TikTok login + Higgsfield connect) · `/security-review` formal do `social-auth-callback` mesclado (recomendado) · TikTok app review (vídeo enviado; conta-sandbox P2) · refinamento auto-DCR-per-user do Higgsfield (opcional) · it.4b build (deepsearch HyperFrames `StudioApiAdapter` → emenda SDD → código).
> HANDOFF.md:731:| **Fase B 2a — Studio Host + McorchAdapter + FR-VS-048 (A)** — `createStudioApi(mcorchAdapter)` 13 métodos; seam startRender minta JWT User 0 → `video-render` (chokepoint único de billing) → observa `video_renders` → materializa MP4 | **E2E PAGO testemunhado**: 202 → row `b25838a0` (12 mco, 4636→4624) → worker nativo → done → `renders/*.mp4` 386.795B sha `c721f8f4` (4º byte-idêntico) → download 200 → SSE complete · smoke **6/6** zero-cost · SOP Lei 2 `video-studio-host-fase-b.md` ANTES do código · **Achado: `VIDEO_HYPERFRAMES_WEBHOOK=poll://` já ativo** (Fila stale corrigida) | `2123a79` |
> HANDOFF.md:854:| **BoK §VS-UI-B (Amendment v0.5)** (`docs/bok/video-studio/05-sdd.md`) | ✅ Gate Lei 2: contrato McorchAdapter (13 métodos = 13 call-sites, `npm pack` do dist publicado + Workflow adversarial `wf_b0a6c005-8c2`) + 3 pre-code gates + FR-VS-047/048/049 |
> HANDOFF.md:864:| `06f7601` | docs(bok): §VS-UI-B Amendment v0.5 — McorchAdapter contract + 3 gates |
> HANDOFF.md:1432:**Arco 1 — Editor HyperFrames VIVO (Fatia VS-UI Fase A).** Descoberta material decisiva: o servidor oficial **`hyperframes preview`** (CLI unscoped `hyperframes@0.7.5`, NÃO `@hyperframes/cli` que não existe) **É** o editor NLE completo (StudioApp React 19 + Hono `/api`) — roda como **processo node standalone** → o conflito React 19/18 some **sem Docker**. Implantado como serviço host systemd `video-studio.service` (node v22 EXPLÍCITO — systemd pega `/usr/bin/node` v18 que quebra com `styleText`), projeto 9:16 semeado (`hyperframes init --example warm-grain --resolution portrait`), atrás do vhost `nginx/video.mcorch.com.conf` (SSO-gated, espelha design). Contrato `/api` (`StudioApiAdapter`) selado dos `.d.ts` publicados (Lei 2) — SDD §VS-UI Amendment v0.4 + SOP `video-studio-editor-deploy-and-provision.md`. Frontend `VideoStudioEditorPage` iframe `/dashboard/canvas/video` (rota ANTES de `canvas/:id`). **Sovereign executou os 2 sudo (cert + symlink+reload); provado E2E pela screenshot dele** (projeto 9:16 carregado, SSO redireciona em aba anônima). Render-parity resolvido por construção (`@hyperframes/core/runtime` IIFE compartilhado).
> HANDOFF.md:1467:1. **Blueprint do HyperFrames Studio (deepsearch, `1f770e4`).** Material-citado no repo HeyGen `@ ae8b94c5` (Apache-2.0). Achado decisivo: `StudioApp` é **zero-props**, server-backed por um `/api` REST+SSE na mesma origem; a HeyGen expôs o seam `StudioApiAdapter` (`@hyperframes/core/studio-api`). **Montamos o studio unmodified + nosso `McorchAdapter.startRender()` faz bridge pro `video-render` provado** — não forkamos a UI. Composição = HTML+CSS+GSAP → `bundleToSingleHtml`. React 19 → container+iframe `studio.mcorch.com`. `.claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md` (6 gates empíricos; render-parity `frame=floor(time*fps)` = maior risco; 9 riscos). Flip OTD-VS-005 A→C confirmado pela prova material.
> HANDOFF.md:9554:- **8991 total nodes** (verificado live 2026-06-29 via REST count=exact, product-miner-vision-reliability-async seal: +handoff `1c100e2a-34f4-4b0a-a324-d89cba7ab0a8` embedded 768d — reparo de confiabilidade do Minerador (Vision MCP): Gemini Files API 20-100MB + cover-image fallback (rejeita stub <50KB) + `shouldDownloadVideos:true` vídeo rico em todo vídeo + `:free` 429→pago BYOK + síntese audience-fit/confidence/parser tolerante + extração ASSÍNCRONA timeout-proof [`vm_miner_jobs` RLS-owner/realtime + action `mine-async` EdgeRuntime.waitUntil + hook `useMinerJob` Realtime+polling + barra de progresso + notificação]; 10 commits prod-live; prev 8982 verificado live 2026-06-28 via REST count=exact, privacy-policy-google-oauth-compliance seal: +handoff `d5476bb8-c5ea-4dc4-a3c0-86d1e0895456` embedded 768d — política de privacidade endurecida p/ verificação Google OAuth: cláusula treino-IA Limited Use + §6 revogação/exclusão de tokens + §8 aviso de alterações + §5 segurança concreta [criptografia trânsito/repouso]; grounded na política Google + revisão adversarial 4/4; deployed login.mcorch.com/privacy + render browser-verificado; prev 8973 verificado live 2026-06-27 via REST count=exact, social-connect-tiktok-youtube-pinterest seal: +handoff `311a55b1-fb7b-410f-9582-625fb4721619` embedded 768d — conectar redes TikTok/YouTube/Pinterest: gate BoK post-engine + migration social_app_config Vault-cifrada aplicada/provada + helper fail-closed + 4 edge fns OAuth/publisher [deno 8/8, deployadas, 3×402 live] + UI browser-verified Vision-QA-high; FR-PE-013 video-cadence deferido; prev 8969 gabriel-ai-moodboard-vision-qa seal: +handoff `5501a101-f4fb-4431-a9d8-34f551353c95` embedded 768d — 1º ciclo pago vídeo 9:16 witnessed + billing/CTA fixes + LinkedIn cadence E2E + virada brand-persona Gabriel AI/CCIO + blueprint YT/TikTok + nó mood-board multi-foto + mood board 4 retratos Vision-QA-gated + 2 animações DoP + regra Vision QA + canvas prompt.length hardening; prev 8960 creative-assets-spine-fatia1 seal: +handoff `8eb84bce-f0d5-4463-a79b-9de9ab5892b9` embedded 768d — HyperFrames editor LIVE [video-studio.service + vhost SSO + iframe /dashboard/canvas/video] + auth gating ?devLogin + Canvas hydration-race bug fix + projeto 63d406fe recuperado + creative_assets SPINE [migration+RPC service-role-only, dual-write video-bridge/canvas-execute/generate-image, backfill 73, Biblioteca de Assets UI]; prev 8959 hyperframes-studio-blueprint-and-video-billing-fix seal: +handoff `b42e89f9-3636-4ff0-a86e-674ed479d3c5` embedded 768d via trigger — blueprint de integração do HyperFrames Studio [deepsearch `ae8b94c5`, StudioApp zero-props + seam StudioApiAdapter → módulo-container VS-UI] + fix do gap de billing OTD-VA-010 [crédito compensatório idempotente `refund_autopilot_video_enqueue` migration `20260624140000`, smoke 8/8 net-debit-exclui-12, /security-review SAFE]; prev 8958 video-9x16-motor-and-autopilot seal: +handoff `5e470dff-d7b3-4936-a130-2c34350d56c8` embedded 768d via trigger — vídeo 9:16 autônomo: VS-2 motor HyperFrames determinístico vivo [render-core Playwright+FFmpeg 1080×1920 sha256-idêntico, video-bridge.service, bucket, edge poll://] + VA-V1 integração Autopilot [orchestrate-step enfileira render do ângulo real, custo no pré-débito do ciclo, attach content_library+creative_metrics] + flip editor OTD-VS-005 A→C módulo-container; prev 8954 autopilot-activation-security-hardening seal: +handoff `bc175ac9-e8a8-483b-a32f-4660dd0b90ba` embedded 768d via trigger — 3 arcos: Viral Autopilot ATIVADO [1º ciclo pago `947ef8b5` + pg_cron jobid 3] + FR-VA-018 trend angle hardened + segurança social-auth [state HMAC + webhook IG sig] + paridade pt-BR Cyber-Sentinel OTD-VA-018; prev 8946 alertas-video-fatia1-de-n8n seal: +handoff `bb23b9dc-265e-4338-9709-d320371908b4` embedded 768d — alertas CF/security-drift + Vídeo Fatia 1 [video_renders/video_assets/finalize_video_render + edge video-render/poll] + Fatia 1b UI + emenda BoK SDD v1.2 De-n8n; prev 8935 viral-autopilot-fatia2 seal: +handoff `280e94d7-8de7-43bb-aee7-89d1824042d7` embedded 768d — cadência R2 (cron + begin/finalize_autopilot_cycle atômicos) + loop R3 (analyze→optimization_policy / collect / feedback-inject) + UI (useAutopilot/AutopilotPage); prev 8934 viral-autopilot-fatias-1-1b seal: +handoff `385d3dd5-264f-4e9d-95a6-b50d93ca338c` embedded 768d — Fatias 1 (product-aware + monetização cross-surface + creative_metrics) + 1b (imagem fail-open) + generate-image fix + diagnóstico saída visível; prev 8928 viral-autopilot-bok-seal: +handoff `496ec17c-953e-498c-b18f-e19ef093ad46` embedded 768d + BoK seal `b3398294-aa75-4810-845b-3a15cfe802e7` `documentation_suite` viral-autopilot + DERIVES_FROM edge `05cea16d-b942-409c-9847-1acc693f6ccc` → marketing-hub `d5163fed`; prev 8926 unified-sensorial-canvas-v9 seal: +handoff `5225ff03-5e4d-4599-9c9a-625e2e1806af` embedded 768d + AGI→ASI ref `a576216e` (architecture, edge `INFORMS` `d2827191` → openclaw seal) + AST ingest dos arquivos novos do canvas (CodeNetworkLayer/MemoryNetworkLayer/useUnifiedCanvasStore/useMemoryNetwork); prev 8922 vision-mcp-fatia3-pat-plugin-registry-caps seal: +handoff `c21c53db-cd96-465d-92ba-fc419c0c83e7` embedded 768d — PAT UI + Plugin/Registry + caps; prev 8921 vision-mcp-vhost-live seal: +handoff `0632e1f8-81db-4cc8-bd5e-c5ea8109508d` embedded 768d — OTD-VM-013 fechada; prev 8920 vision-fatia3-pat-erase seal: +handoff `e0695dad-3fc8-4f1e-9973-a40c15aec433` embedded 768d; prev 8918 vision-deepsearch-run-async seal: +handoff `fc0b5efc-9df8-4e03-8544-820caee4ee79` embedded 768d; prev 8917 vision-mcp-fatia2-complete seal: +handoff `7a45d8ef-7f69-4b7d-8ef4-107f4c488c64` embedded 768d; prev 8916 vision-mcp-fatia1-deployed seal: +handoff `98fa83d7-3caa-4d23-9f5d-ed040ced9530` embedded 768d; prev 8915 em vision-mcp-bok-9of9 seal: +handoff `b73d141d` + BoK seal `318862b7` documentation_suite vision-mcp + DERIVES_FROM edge `b4de794c` → mcorch-constellation; prev 8911 em diagnostics-and-continuity +handoff `855e9cdc`; prev 8865 em core-fable-interstellar +handoff `4728b8aa`)
> .claude/context/sprint-priorities.md:33:**Sprint v6.49.0/v6.49.1 — Vídeo viral 9:16 autônomo + motor HyperFrames vivo → Studio blueprint + gap de billing fechado (2026-06-24)** — `/handson` → "fichar o vídeo 9:16 com a UI editor do hyperframer assim como o open design" → sob **ultracode**. **v6.49.0:** decisão Sovereign (AskUserQuestion) = motor HyperFrames + worker single-tenant, alvo Autopilot-primeiro → BoK gate (Amendment v0.2, FR-VA-022..026 + SOP) → **motor HyperFrames VIVO** (`render-core.ts` Playwright+FFmpeg → MP4 9:16 1080×1920 sha256-idêntico NFR-VS-016; worker `video-bridge.ts` systemd active; bucket; edge `poll://`) → integração Autopilot (custo no pré-débito do ciclo OTD-VA-010; E2E real "Roborock S8…" render 9:16, saldo intacto). **v6.49.1:** **(1)** deepsearch do HyperFrames Studio (`ae8b94c5`, Apache-2.0) → flip OTD-VS-005 A→C **módulo-container** (StudioApp zero-props + seam `StudioApiAdapter`; embed in-SPA inviável React 19 vs 18); blueprint `.claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md`. **(2)** gap de billing OTD-VA-010 fechado: crédito compensatório idempotente `refund_autopilot_video_enqueue` (migration `20260624140000`) no fail-open do enqueue (actual otimista contava 12 sem linha → cobrança-sem-valor); smoke **8/8** net-debit-exclui-12. **Prova:** `/security-review` SAFE (motor + billing) · tsc 0 · gitleaks limpo · Phase 5c **SEAL ALLOWED** (10) · mesh **8959** · handoff `b42e89f9`. **Pending (próxima):** **Fatia VS-UI** editor Studio módulo-container (API `/api` → container React 19 → `McorchAdapter` → vhost `studio.mcorch.com` [DNS Sovereign] → render-parity gate) · 1º ciclo pago de vídeo witnessed · Unified Canvas 3.5-3.10 · postback ML real · Security BoK suite (diferida). **Lição:** o achado material (orchestrate-content é async → autopilot-run finaliza ANTES dos enqueues) inviabilizou a Option 1 do diretivo e decidiu o design do fix; o deepsearch pré-código achou o seam zero-props que evita forkar a UI HeyGen.
> docs/bok/spaces-evolution/14-amendment-spaces-v2-consolidation.md:100:  1. **Ponte cross-origin inexistente.** O open-design é um `<iframe>` cru para `design.mcorch.com` sem adapter/postMessage/ref (`src/pages/CanvasDesignPage.tsx:11-17`, arquivo inteiro = 20 linhas). Parent `login.mcorch.com` ≠ iframe `design.mcorch.com` ⇒ same-origin bloqueia `contentWindow`/DOM. Injetar "camadas linkadas a fontes" exige um protocolo de ponte que o open-design **não implementa** (≠ VideoStudio, que tem `StudioApiAdapter`).
> docs/bok/spaces-evolution/14-amendment-spaces-v2-consolidation.md:104:  - **DECISÃO SOVEREIGN 2026-07-08 — editor embutido = HyperFrames Studio (reuso).** Escolhido entre 3 opções (AskUserQuestion): (A) **HyperFrames Studio [ESCOLHIDO]** — reusar o Studio já deployado em `video.mcorch.com` (já tem `StudioApiAdapter` provado no módulo Vídeo — ver [[project_video_studio]] + blueprint `.claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md`), estendendo p/ camadas de arte estática; **sem fork do open-design, sem env hardening OD** (o gate de env vira n-a p/ esta rota). (B) adapter no open-design (rejeitado — fork). (C) editor nativo (rejeitado — build do zero). **Consequência:** o open-design env-hardening SAI do caminho crítico do it.4b (permanece só p/ o card de preview open-design, não p/ a Ponte Designer). 
> docs/bok/spaces-evolution/14-amendment-spaces-v2-consolidation.md:105:  - **Próximo arco (unblock restante):** deepsearch do `StudioApiAdapter`/HyperFrames p/ edição de camadas de IMAGEM estática + link camada→fonte-dinâmica (o `hyperframes-studio-integration-blueprint` cobriu render de vídeo; falta a semântica de layer-source p/ arte estática) → emenda SDD `spaces-evolution` §9/§10 especificando FR-SPACES-030 via HyperFrames → implementação (painel Nodes|Assets no Studio + camadas linkadas + galeria de presets) → /security-review → E2E+Vision. Rebaixa a linha it.4b do §9 (verification gates) a *pendente deste arco*.
> docs/bok/video-studio/05-sdd.md:860:### A.2 Contrato `/api` (Lei 2 — `StudioApiAdapter`, fonte: `@hyperframes/core@0.7.5` `dist/studio-api/types.d.ts`)
> docs/bok/video-studio/05-sdd.md:862:`createStudioApi(adapter: StudioApiAdapter): Hono` monta **todas** as rotas (`/api/projects`, `…/files/*`,
> docs/bok/video-studio/05-sdd.md:872:| **`startRender(opts)`** | retorna `RenderJobState{id,status:rendering\|complete\|failed,progress,stage?,outputPath,error?}` mutável; `opts={project,outputPath,format(mp4\|webm\|mov),fps(rational),quality,jobId,outputResolution?,composition?,distinctId?}` | **o seam**: Fase A = engine local do CLI; **Fase B = `McorchAdapter` → POST `video-render` (engine=hyperframes, composition_html=bundle(dir), 1080×1920, fps) → poll `video-render-poll` → muta o RenderJobState** |
> docs/bok/video-studio/05-sdd.md:881:runtime ao preview. Logo, se o `McorchAdapter` (Fase B) renderiza o output de `bundleToSingleHtml` no nosso
> ```

## 🤖 Claude *(06:32:38)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"=== blueprint context file ===\"; ls -la .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md 2>/dev/null; echo \"=== video-studio SDD files ===\"; ls -la docs/bok/video-studio/ 2>/dev/null; echo \"=== SOP ===\"; ls -la docs/processes/video-studio-editor-deploy-and-provision.md 2>/dev/null",
  "description": "Locate blueprint and SDD files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === blueprint context file ===
> -rw-rw-r-- 1 gcrUX gcrUX 9683 Jun 24 14:10 .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md
> === video-studio SDD files ===
> total 432
> drwxrwxr-x  2 gcrUX gcrUX   4096 Jul  1 18:34 .
> drwxrwxr-x 29 gcrUX gcrUX   4096 Jul  8 23:41 ..
> -rw-rw-r--  1 gcrUX gcrUX  10417 Jul  1 18:34 00-index.md
> -rw-rw-r--  1 gcrUX gcrUX  28062 Jun 21 22:38 01-mrd.md
> -rw-rw-r--  1 gcrUX gcrUX  36035 Jun 21 22:40 02-brd.md
> -rw-rw-r--  1 gcrUX gcrUX  36816 Jun 21 22:39 03-prd.md
> -rw-rw-r--  1 gcrUX gcrUX  45365 Jun 24 12:07 04-frd.md
> -rw-rw-r--  1 gcrUX gcrUX 101693 Jul  1 18:34 05-sdd.md
> -rw-rw-r--  1 gcrUX gcrUX  62010 Jun 21 22:43 06-data-model.md
> -rw-rw-r--  1 gcrUX gcrUX  51151 Jun 21 22:46 07-process-flow.md
> -rw-rw-r--  1 gcrUX gcrUX  46795 Jun 21 22:47 08-quality-metrics.md
> === SOP ===
> -rw-rw-r-- 1 gcrUX gcrUX 5148 Jun 24 20:07 docs/processes/video-studio-editor-deploy-and-provision.md
> ```

## 🤖 Claude *(06:32:45)*


## 🤖 Claude *(06:32:45)*

Let me read the blueprint, the SDD adapter contract, and the studio-host McorchAdapter implementation.

## 🤖 Claude *(06:32:46)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# HyperFrames Studio → MCORCH Integration Blueprint (deepsearch, 2026-06-24)
> 2	
> 3	> **Founds the VS-UI container build** (Fatia VS-UI / FR-VS-021 Amendment v0.3). Deepsearch material-cited
> 4	> against `github.com/heygen-com/hyperframes` @ commit `ae8b94c51841be8c4b53fe861adae9371db5eff3` (files read
> 5	> via GitHub API), npm registry, and docs. **Law 2 artifact** — read this BEFORE writing the container code.
> 6	> Owner: Sovereign. Next gate after this: BoK amendment of the `/api` adapter surface + Dockerfile + vhost.
> 7	
> 8	## TL;DR (decisive finding)
> 9	
> 10	`@hyperframes/studio`'s `StudioApp` takes **ZERO props**. It is a thin React 19 frontend that on mount discovers a
> 11	**same-origin REST + SSE backend** (`/api/projects`, `/api/projects/:id/files/*`, `/preview/*`, `/render`,
> 12	`/api/render/:jobId/progress`). That backend is the Hono app **`createStudioApi(adapter)`** exported from
> 13	**`@hyperframes/core/studio-api`**, parameterized by a single **`StudioApiAdapter`** interface (HeyGen's deliberate
> 14	DI seam: "each host provides its own adapter").
> 15	
> 16	**MCORCH approach:** do NOT fork the studio UI. **Mount the unmodified `StudioApp`** + implement our own
> 17	**`McorchAdapter`** whose `startRender()` bridges to our proven `video-render` edge fn (engine=hyperframes) instead
> 18	of HeyGen's Puppeteer/FFmpeg producer. No HeyGen cloud on the open-source path. **License: Apache-2.0** (self-host +
> 19	adapt OK; retain notice; don't use HeyGen/HyperFrames branding §6).
> 20	
> 21	## Container architecture (mirrors canvas-design→open-design, but ONE origin)
> 22	
> 23	```
> 24	MCORCH SPA (/dashboard/canvas/video, FR-VS-022) ── iframe ──▶ studio.mcorch.com (CF orange → 127.0.0.1:32xx)
> 25	  Docker container mcorch_video_studio (React 19 host + Hono backend, ONE node process, ONE origin):
> 26	    ├── static: vite build of our minimal host that renders <StudioApp/>
> 27	    └── Hono: app.route("/api", createStudioApi(McorchAdapter)) + serveStatic(dist)
> 28	         McorchAdapter.startRender(opts) → POST <supabase>/functions/v1/video-render
> 29	              { engine:"hyperframes", composition_html: bundle(opts.project.dir), width:1080, height:1920, fps }
> 30	            → poll video-render-poll → map to RenderJobState (progress/stage/status) → studio SSE relays to UI
> 31	         McorchAdapter.{listProjects,resolveProject,files,preview,lint} ← Supabase Storage / container volume
> 32	```
> 33	Frontend uses **relative** `fetch("/api/...")` + `new EventSource("/api/render/:id/progress")` → frontend and `/api`
> 34	**must be same-origin** (the container). MCORCH↔container boundary = iframe (`#project=<id>` via URL hash).
> 35	
> 36	## Q1 Mount
> 37	- Exports incl. `StudioApp` (full editor, **no props**), `NLELayout`, `Player`, `Timeline`, `SourceEditor`,
> 38	  `PropertyPanel`, `FileTree`, `usePlayerStore`, etc. (`packages/studio/src/index.ts`).
> 39	- Self-driving: `useServerConnection()` polls `/api/projects` (2s, `StudioSplash` while waiting), reads `projectId`
> 40	  from URL hash `#project=<id>`. No "pass a composition" path — file/server-backed by design.
> 41	- Minimal host (mirror `src/main.tsx`): `createRoot(#root).render(<StrictMode><StudioApp/></StrictMode>)` +
> 42	  `html,body,#root{height:100%}`. CSS import path = **empirical test** (`npm pack` → inspect dist; styling export is
> 43	  `@hyperframes/studio/tailwind-preset`).
> 44	
> 45	## Q2 Composition format (what our motor renders)
> 46	Plain **HTML + inline CSS + paused GSAP timeline** (no JSON, no React). Stored as **files** in a project dir
> 47	(`meta.json`, `index.html`, `compositions/`, `assets/`). Root: `data-composition-id`/`data-width`/`data-height`
> 48	(9:16 = 1080×1920); clips: `class="clip"` + `data-start`/`data-duration`/`data-track-index`; GSAP timeline
> 49	`{paused:true}` on `window.__timelines`. **No `onChange`/`onSave` prop** — editor persists via `PUT /api/.../files`.
> 50	The artifact our motor consumes = **`adapter.bundle(dir)` → `@hyperframes/core/compiler` `bundleToSingleHtml(dir)`**
> 51	(single 1080×1920 HTML string — exactly what our HTML→MP4 worker eats).
> 52	
> 53	## Q3 Render bridge (the seam)
> 54	Export button → `renderQueue.startRender` → `POST /api/projects/:id/render {fps,quality,format,resolution?,composition?}`
> 55	→ `{jobId}` → SSE `/api/render/:jobId/progress` (`{progress,stage,status,error}`, terminal `complete|failed`). That
> 56	route calls **`adapter.startRender(opts)`** (`opts={project{id,dir,title}, outputPath, format, fps, quality, jobId,
> 57	outputResolution?, composition?}`) which "owns async execution + updates RenderJobState reactively". Reference impl =
> 58	`vite.adapter.ts startRender` (swap its `@hyperframes/producer` call for our edge-fn fetch + poll). **Studio UI needs
> 59	zero changes.** Single billing stays our side (cycle prepaid / `prepaid=true`, OTD-VA-010) — studio never sees mcoCoins.
> 60	
> 61	## Q4 core & player
> 62	- `@hyperframes/core`: parsers + linter + **`/compiler` (bundleToSingleHtml)** + **`/runtime` (seekable IIFE)** +
> 63	  **`/studio-api` (Hono factory + adapter interface)**. `hono` is an **optional** peer (only for `createStudioApi`).
> 64	  **core does NOT render to MP4** — `@hyperframes/engine` (Puppeteer+FFmpeg capture) + `@hyperframes/producer`
> 65	  (pipeline) do; same class as our motor. Keep our motor; use core only for studio-api + compiler + runtime.
> 66	- `@hyperframes/player`: `<hyperframes-player>` web component (playback only).
> 67	
> 68	## Q5 React 19 + container
> 69	- npm `@hyperframes/studio@0.7.5` pins `react:"19"` **exactly** (registry-confirmed) → **separate container + iframe**
> 70	  (this is WHY in-SPA embed was rejected; MCORCH SPA = React 18).
> 71	- Tailwind: `presets:[require('@hyperframes/studio/tailwind-preset')]` or editor renders unstyled (Tailwind 3.4).
> 72	- Dockerfile sketch: `node:22-bookworm-slim` (node>=22), `bun install` (react@19/react-dom@19/zustand@5/
> 73	  @hyperframes/studio/@hyperframes/core/hono/@hono/node-server), `vite build`, `node server.js` (Hono route /api +
> 74	  serveStatic). **If startRender delegates to remote edge fn → NO Chrome/FFmpeg in the container** (lighter than CLI).
> 75	
> 76	## Q6 Auth/embedding
> 77	No HeyGen auth on the embedding path (`createStudioApi` is auth-agnostic; CLI's cloud/auth dirs are off-path). Relative
> 78	fetch/SSE → same-origin container. iframe like canvas-design. Adapter resolves `user_id` from JWT/PAT (Vision-MCP
> 79	pattern); scope Storage per user; verify ownership of hash `projectId`. CF orange SSE needs `proxy_buffering off`
> 80	(reuse `mcp.mcorch.com` vhost recipe).
> 81	
> 82	## Q7 License — Apache-2.0 (Copyright 2026 HeyGen, Inc.). Self-host/modify/distribute OK; retain notices; trademark not licensed.
> 83	
> 84	## Empirical gates before declaring it works (Law 1 — not documented)
> 85	1. **CSS import path** for `StudioApp` (`npm pack` → inspect `dist/`).
> 86	2. **`createStudioApi` exported from published `@hyperframes/core` dist** (it's in src exports `./studio-api`).
> 87	3. **Exact composition attribute names** (docs disagree `#stage` vs `data-composition-id`) — confirm from a real
> 88	   `npx hyperframes init` project.
> 89	4. **⚠️ HIGHEST RISK — render parity:** does our HTML→MP4 worker drive `window.__timelines` with
> 90	   `frame=floor(time*fps)` like core's runtime? If not, motion renders wrong. Consider injecting
> 91	   `@hyperframes/core/runtime` into our motor's headless page so seek semantics match. **Gates engine=hyperframes correctness.**
> 92	5. **Full `/api` surface the adapter must satisfy** — read `core/src/studio-api/routes/*.ts`: mandatory
> 93	   `projects`/`files`/`preview`/`render`; optional (stub) `thumbnail`/`waveform`/`fonts`/`registry`/`storyboard`.
> 94	6. React 19 in separate container — confirm no shared-React conflict through the iframe (shouldn't be — separate origin).
> 95	
> 96	## Risk list
> 97	| # | Risk | Sev | Mitigation |
> 98	|---|------|-----|------------|
> 99	| R1 | Render parity (studio preview ≠ our motor output) | **High** | Gate #4; inject core/runtime into motor's headless page |
> 100	| R2 | Must implement whole `/api` Hono surface, not just render | **High** | Reuse `createStudioApi`; write only `McorchAdapter`; stub optional methods |
> 101	| R3 | React 19 vs MCORCH React 18 | Med (mitigated) | Separate container + iframe (chosen) |
> 102	| R4 | Same-origin relative fetch/SSE | Med | Container serves frontend+/api one origin; CF `proxy_buffering off` |
> 103	| R5 | 0.7.x pre-1.0 API churn | Med | Pin 0.7.5; vendor studio-api types; gate upgrades on parity test |
> 104	| R6 | Studio has no native multi-tenant auth | Med | Adapter resolves user from PAT/JWT; scope Storage; verify projectId ownership |
> 105	| R9 | Studio expects real FS (`dir`); Storage is object store | Med | Materialize project to container volume on resolve, sync back on write |
> 106	
> 107	## Build sequence (next session)
> 108	1. BoK: enumerate the mandatory `/api` route req/resp shapes (`core/studio-api/routes/*.ts`) → amend video-studio SDD with the `McorchAdapter` contract.
> 109	2. `npm pack` empirical gates (#1/#2/#3 above).
> 110	3. Render-parity test (#4) — inject core runtime into our motor OR confirm seek convention.
> 111	4. Container: React 19 host (`<StudioApp/>`) + Hono `createStudioApi(McorchAdapter)` + Dockerfile → run 127.0.0.1.
> 112	5. `McorchAdapter`: files/preview over Supabase Storage; `startRender` → `video-render` edge fn.
> 113	6. Frontend: `/dashboard/canvas/video` iframe page (mirror `CanvasDesignPage`) + route before `canvas/:id`.
> 114	7. vhost `studio.mcorch.com` (**DNS+cert = Sovereign action**, OTD-VS-015) + SSE-tuned proxy.
> 115	8. E2E 1920×1080 gate (Lei 1 Canvas).
> 116	
> 117	**Sources:** github.com/heygen-com/hyperframes @ `ae8b94c5` (studio/core/cli package.json, studio/src/{index,main,App}.tsx, useRenderQueue.ts, useServerConnection.ts, vite.adapter.ts, core/src/studio-api/{index,types,createStudioApi}.ts, LICENSE) · registry.npmjs.org/@hyperframes/studio/latest · hyperframes.heygen.com · hyperframes.mintlify.app/quickstart.
> 118	
> ```

## 🤖 Claude *(06:32:47)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md",
  "offset": 855,
  "limit": 70
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 855	(molde `video-bridge.service`/`design-bridge.service`), **sem Docker**. Containerização fica deferida até a
> 856	necessidade multi-tenant (OTD-VA-011). Provas materiais (2026-06-24): `video-studio.service` `active`;
> 857	`curl 127.0.0.1:3210/` → **HTTP 200** `<title>HyperFrames Studio</title>`; `/api/projects` → **200**
> 858	`[{id:"mcorch-demo", dir:…, title:…}]` (projeto 9:16 `--resolution portrait` semeado por `hyperframes init`).
> 859	
> 860	### A.2 Contrato `/api` (Lei 2 — `StudioApiAdapter`, fonte: `@hyperframes/core@0.7.5` `dist/studio-api/types.d.ts`)
> 861	
> 862	`createStudioApi(adapter: StudioApiAdapter): Hono` monta **todas** as rotas (`/api/projects`, `…/files/*`,
> 863	`/preview/*`, `…/render`, `/render/:jobId/progress` SSE) internamente → **o host implementa SÓ o adapter**.
> 864	
> 865	| Método (obrigatório) | Contrato | Realização MCORCH (Fase B) |
> 866	|---|---|---|
> 867	| `listProjects()` / `resolveProject(id)` | `ResolvedProject{id,dir,title?,sessionId?}` | store de projetos (Fase A: FS local; Fase B: Supabase Storage materializado em volume) |
> 868	| `bundle(projectDir)` | `Promise<string\|null>` (HTML único) | `@hyperframes/core/compiler` `bundleToSingleHtml(dir)` |
> 869	| `lint(html, opts?)` | `LintResult` | `@hyperframes/core/lint` |
> 870	| `runtimeUrl: string` | URL do runtime injetado no preview | serve `@hyperframes/core/runtime` (IIFE) estático |
> 871	| `rendersDir(project)` | dir de saída | volume local (Fase A) / tmp + upload (Fase B) |
> 872	| **`startRender(opts)`** | retorna `RenderJobState{id,status:rendering\|complete\|failed,progress,stage?,outputPath,error?}` mutável; `opts={project,outputPath,format(mp4\|webm\|mov),fps(rational),quality,jobId,outputResolution?,composition?,distinctId?}` | **o seam**: Fase A = engine local do CLI; **Fase B = `McorchAdapter` → POST `video-render` (engine=hyperframes, composition_html=bundle(dir), 1080×1920, fps) → poll `video-render-poll` → muta o RenderJobState** |
> 873	
> 874	Opcionais (stub OK): `getProjectSignature` · `transformPreviewHtml` · `generateThumbnail` · `resolveSession`
> 875	· `listRegistryCatalog` · `installRegistryBlock`.
> 876	
> 877	### A.3 Render-parity (R1 — maior risco do blueprint) — resolvido por construção
> 878	
> 879	`@hyperframes/core` exporta **`./runtime`** (IIFE `hyperframe.runtime.iife.js`) e **`./compiler`**
> 880	(`bundleToSingleHtml`, que **embute** esse runtime no HTML final). O `adapter.runtimeUrl` serve **o mesmo**
> 881	runtime ao preview. Logo, se o `McorchAdapter` (Fase B) renderiza o output de `bundleToSingleHtml` no nosso
> 882	motor, **preview e render usam a mesma semântica de seek** (`frame=floor(time*fps)`) — gate empírico #4
> 883	mitigado sem reimplementar timing. (Hoje `render-core.ts` dirige um template fixo via `applyProps/applyFrame`;
> 884	a Fase B adiciona um path `composition_html` que carrega o bundle e dirige o runtime embutido.)
> 885	
> 886	### A.4 OTDs
> 887	
> 888	| OTD | Tema | Decisão |
> 889	|---|---|---|
> 890	| **OTD-VS-005** | HyperFrames Studio mode | **C REALIZADA** (Fase A host service entregue + provada) |
> 891	| **OTD-VS-015** | vhost `video.mcorch.com` | vhost ESCRITO (`nginx/video.mcorch.com.conf`); **cert self-signed + `ln -s`+reload = ação Sovereign** (2 sudo) |
> 892	| **OTD-VS-016** | multi-projeto | `hyperframes preview` é **single-project** (exige `index.html` no DIR). Fase A serve UM projeto canônico (`mcorch-demo`). Switching multi-projeto = follow-up (parent-root não suportado pelo CLI 0.7.5) |
> 893	| **OTD-VS-017** | render bridge (Fase B) | `McorchAdapter.startRender` → `video-render` (substitui engine local) + project store em Supabase Storage + auth JWT/PAT per-user; cobrança ÚNICA no nosso lado (prepaid, OTD-VA-010) — o studio nunca vê mcoCoins |
> 894	
> 895	---
> 896	
> 897	## §VS-UI-B — McorchAdapter contract: verificação empírica + gates pré-código (Amendment v0.5 · 2026-06-30 · FR-VS-047/048/049 · concretiza OTD-VS-017)
> 898	
> 899	> **Gate Lei 2 do build do container Fase B.** Autorada a partir de **verificação empírica material (Lei 1)** dos
> 900	> pacotes npm **publicados** `@hyperframes/studio@0.7.5` + `@hyperframes/core@0.7.5` (pin exato) — `npm pack` +
> 901	> inspeção do `dist/` + fonte das rotas — mais leitura do nosso `render-core.ts`. Supera a §VS-UI v0.4, que deixou
> 902	> os 3 riscos duros (render-parity, auth, FS-sync) como hand-wave "por construção". **Nenhum código de container
> 903	> começa antes destes gates verdes.** Verificação: Workflow adversarial `wf_b0a6c005-8c2` (APPROVE_WITH_FIXES, 3
> 904	> blocking gaps) + gates empíricos re-executados no main-loop (2 subagentes do WF vieram stub — refeitos à mão).
> 905	
> 906	### B.1 Fatos empíricos (Lei 1 — dist publicado, não suposição)
> 907	
> 908	| Fato | Evidência (dist do tarball publicado) |
> 909	|---|---|
> 910	| `@hyperframes/studio@0.7.5` pina `@hyperframes/core@**0.7.5**` (exato) | `npm view @hyperframes/studio@0.7.5 dependencies` |
> 911	| studio é **biblioteca sem `bin`**, pina `react:19`+`react-dom:19` (exato) + `zustand:^4\|\|^5` | `npm view … bin peerDependencies` → **hand-mount `<StudioApp/>` num host React 19; container separado obrigatório** |
> 912	| core exporta `./studio-api` (`createStudioApi`), `./compiler` (`bundleToSingleHtml`), `./runtime` (IIFE 225KB) — **todos presentes no dist publicado** | `package.json` exports + arquivos físicos `dist/studio-api/index.js`, `dist/compiler/index.js`, `dist/hyperframe.runtime.iife.js` |
> 913	| `hono` é **peer OPCIONAL** (só `createStudioApi` precisa) | `peerDependenciesMeta.hono.optional=true` |
> 914	| runtime expõe `window.__hyperframes = { fitTextFontSize, getVariables }` — **seek NÃO é público aqui**; o seek roda via `window.__timelines[…].seek(p)` (GSAP `.seek`/`totalTime`), frame→tempo por `Math.floor(i*n+1e-9)` | grep do `dist/hyperframe.runtime.iife.js` (`.seek(` 20× · `totalTime` 13× · `window.__hyperframes` 2×) |
> 915	
> 916	### B.2 Contrato McorchAdapter — completeness PROVADA (fecha blocking-gap #1 do critic)
> 917	
> 918	Enumeração das **rotas reais** que `createStudioApi` monta (`dist/studio-api/routes/*.js`: `projects` · `files` ·
> 919	`preview` · `lint` · `render` · `thumbnail` · `waveform` · `storyboard` · `fonts` · `registry`) cruzada com as
> 920	**13 chamadas `adapter.X`** reais no dist. **Toda chamada mapeia a um método do contrato — zero rota órfã:**
> 921	
> 922	| adapter.X | call-sites | Mandatório? | McorchAdapter impl |
> 923	|---|---|---|---|
> 924	| `resolveProject(id)` | **15** (todo route project-scoped) | ✅ | materializa Storage→volume `/work/projects/<id>/` (download do prefixo `<user>/<id>/`), retorna `{id,dir,…}`; verifica ownership (User 0) |
> ```

## 🤖 Claude *(06:32:50)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; echo \"=== video-studio-host dir ===\"; ls -la scripts/video-studio-host/ 2>/dev/null; echo; echo \"=== grep listProjects/resolveProject/projectId in host + repo ===\"; grep -rn \"listProjects\\|resolveProject\\|projectId\\|project.dir\\|projects/mcorch-video\\|VIDEO_STUDIO_PROJECT\\|mcorch-video\" scripts/ 2>/dev/null | grep -v node_modules | head -40",
  "description": "List studio-host dir and grep project identity refs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === video-studio-host dir ===
> total 36
> drwxrwxr-x 2 gcrUX gcrUX 4096 Jul  1 19:28 .
> drwxrwxr-x 7 gcrUX gcrUX 4096 Jul  8 06:53 ..
> -rw-rw-r-- 1 gcrUX gcrUX 9402 Jul  1 19:22 adapter.ts
> -rw-rw-r-- 1 gcrUX gcrUX 2700 Jul  1 18:58 auth.ts
> -rw-rw-r-- 1 gcrUX gcrUX 4020 Jul  1 19:21 server.ts
> -rw-rw-r-- 1 gcrUX gcrUX 6240 Jul  1 19:28 sync.ts
> 
> === grep listProjects/resolveProject/projectId in host + repo ===
> scripts/canvas-campaign-build.ts:76:async function findExistingAsset(admin: any, userId: string, projectId: string, nodeId: string) {
> scripts/canvas-campaign-build.ts:81:    .eq("project_id", projectId)
> scripts/canvas-campaign-build.ts:179:async function persistGraph(admin: any, projectId: string, nodes: any[], edges: any[]): Promise<void> {
> scripts/canvas-campaign-build.ts:181:    .from("vm_canvas_projects").select("graph").eq("id", projectId).maybeSingle();
> scripts/canvas-campaign-build.ts:184:  const { error } = await admin.from("vm_canvas_projects").update({ graph }).eq("id", projectId);
> scripts/qa/smoke-studio-host.ts:45:  const previewTarget = list.find((p) => p.id === 'mcorch-video') ?? list[0];
> scripts/qa/smoke-studio-host.ts:50:  gate('G5 traversal guard', traversal.status >= 400, `id '../escape' → HTTP ${traversal.status} (resolveProject nega)`);
> scripts/design-bridge.ts:120:        const projectId = job.od_project_id || 'test_project';
> scripts/design-bridge.ts:129:            const containerFilePath = `/app/.od/projects/${projectId}/${job.od_artifact_id}`;
> scripts/design-bridge.ts:155:              '-e', `OD_PROJECT_ID=${projectId}`,
> scripts/design-bridge.ts:198:            const containerFilePath = `/app/.od/projects/${projectId}/${fileData.name}`;
> scripts/design-bridge.ts:212:                od_project_id: projectId,
> scripts/design-bridge.ts:238:                  od_project_id: projectId,
> scripts/sync-canvas-nodes.ts:15:async function syncProject(projectId: string) {
> scripts/sync-canvas-nodes.ts:16:  console.log(`\nSyncing project: ${projectId}`);
> scripts/sync-canvas-nodes.ts:20:    .eq("id", projectId)
> scripts/sync-canvas-nodes.ts:24:    console.error(`Project not found: ${projectId}`, pErr?.message);
> scripts/sync-canvas-nodes.ts:31:    .eq("project_id", projectId)
> scripts/sync-canvas-nodes.ts:35:    console.error(`Executions not found for project: ${projectId}`, eErr?.message);
> scripts/sync-canvas-nodes.ts:81:      .eq("id", projectId);
> scripts/sync-canvas-nodes.ts:84:      console.error(`Failed to save graph for project ${projectId}:`, saveErr.message);
> scripts/qa/smoke-asset-owner-signing.ts:49:const projectId = crypto.randomUUID();
> scripts/qa/smoke-asset-owner-signing.ts:50:const objectKey = `${projectId}/smoke-${Date.now()}.png`;
> scripts/qa/smoke-asset-owner-signing.ts:58:  const { error: projErr } = await admin.from('vm_canvas_projects').insert({ id: projectId, user_id: owner.uid, name: 'asset-signing-smoke' });
> scripts/qa/smoke-asset-owner-signing.ts:84:  const s3 = await attackerClient.storage.from(BUCKET).list(projectId, { limit: 100 });
> scripts/qa/smoke-asset-owner-signing.ts:89:  const s4 = await attackerClient.from('vm_canvas_projects').insert({ id: projectId, user_id: attacker.uid, name: 'squat' }).select('id').single();
> scripts/qa/smoke-asset-owner-signing.ts:93:    const neutralized = s4.data.id !== projectId;
> scripts/qa/smoke-asset-owner-signing.ts:94:    check('S4 id-squat', neutralized, neutralized ? `trigger regenerated id ${s4.data.id} ≠ victim ${projectId}` : 'LEAK! row kept victim id');
> scripts/qa/smoke-spaces-execution.ts:301:  const projPayload = (projectId: string, extra: Record<string, unknown> = {}) => ({
> scripts/qa/smoke-spaces-execution.ts:302:    project_id: projectId, node_id: 'p_smoke', node_type: 'generate_image',
> scripts/qa/smoke-studio-project-guard.ts:45:await expectThrow('G1 absolute-escape', { mode: 'studio-project', project_dir: '/etc' }, 'project_dir_outside_root');
> scripts/qa/smoke-studio-project-guard.ts:48:await expectThrow('G2 traversal-escape', { mode: 'studio-project', project_dir: `${ROOT}/../../etc` }, 'project_dir_outside_root');
> scripts/qa/smoke-studio-project-guard.ts:50:// G3 — empty/missing project_dir → resolve('') is cwd (outside root) → rejected (no undefined-path crash).
> scripts/qa/smoke-studio-project-guard.ts:51:await expectThrow('G3 empty-dir', { mode: 'studio-project' }, 'project_dir_outside_root');
> scripts/qa/smoke-studio-project-guard.ts:54:await expectThrow('G4 inside-but-missing', { mode: 'studio-project', project_dir: `${ROOT}/ghost-project` }, 'studio_project_not_found');
> scripts/video-studio-host/sync.ts:8: * a project dir from the bucket when the local copy is missing (staging + atomic rename — a partial
> scripts/video-studio-host/sync.ts:79: * Restore a project dir from the bucket (adapter.resolveProject fallback when the local copy is gone).
> scripts/video-studio-host/sync.ts:81: * Returns true iff the project dir exists (materialized) afterwards.
> scripts/hyperframes/render-core.ts:56:  project_dir: string;      // absolute path to the hyperframes project dir (validated under STUDIO_PROJECTS_ROOT)
> scripts/hyperframes/render-core.ts:328: * Security: `project_dir` MUST resolve strictly under STUDIO_PROJECTS_ROOT (no traversal / arbitrary path exec).
> ```

## 🤖 Claude *(06:33:02)*


## 🤖 Claude *(06:33:02)*

Now let me read the Fase B host adapter and server to understand the project identity model and hash-based deep-link.

## 🤖 Claude *(06:33:03)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/video-studio-host/adapter.ts"
}
```

## 🤖 Claude *(06:33:04)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/video-studio-host/server.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	/**
> 2	 * scripts/video-studio-host/adapter.ts — McorchAdapter (SDD §VS-UI-B B.2, contract-complete: 13 call-sites).
> 3	 *
> 4	 * v1 sub-fatia 2a (single-tenant Usuário Zero, OTD-VS-019): the local STUDIO_PROJECTS_ROOT dir is the canonical
> 5	 * project store (the vanilla Fase A editor already works on it); Storage↔volume sync = FR-VS-049 (sub-fatia 2b).
> 6	 * startRender is THE seam (FR-VS-048 option A): mint User Zero JWT → POST `video-render` edge fn (single billing
> 7	 * chokepoint) → poll video_renders → download the bucket MP4 to outputPath. The host NEVER touches mcoCoins.
> 8	 *
> 9	 * Built on @hyperframes/studio-server + @hyperframes/core — Apache-2.0, LICENSE shipped in both tarballs
> 10	 * (© HeyGen, https://github.com/heygen-com/hyperframes; license evidence: SDD §VS-UI-C C.1).
> 11	 */
> 12	import { createClient } from '@supabase/supabase-js';
> 13	import { readdirSync, existsSync, readFileSync, mkdirSync, writeFileSync } from 'fs';
> 14	import { join, resolve } from 'path';
> 15	import type { StudioApiAdapter, ResolvedProject, RenderJobState, LintResult } from '@hyperframes/studio-server';
> 16	import { createProjectSignature } from '@hyperframes/studio-server';
> 17	import { mintUserZeroJwt } from './auth';
> 18	import { materializeProject } from './sync';
> 19	
> 20	// FR-VS-049 materialization: 60s negative cache (id → retry-after epoch-ms).
> 21	const missUntil = new Map<string, number>();
> 22	
> 23	const STUDIO_PROJECTS_ROOT = process.env.STUDIO_PROJECTS_ROOT ?? '/home/ubuntu/.mcorch/video-studio/projects';
> 24	const SUPABASE_URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL ?? '';
> 25	const SVC = process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY ?? '';
> 26	const RENDER_POLL_MS = 5_000;
> 27	const RENDER_TIMEOUT_MS = 15 * 60_000;
> 28	const SAFE_ID = /^[a-zA-Z0-9_-]+$/; // project ids are dir names — never path fragments
> 29	
> 30	const admin = createClient(SUPABASE_URL, SVC, { auth: { persistSession: false } });
> 31	
> 32	function projectTitle(dir: string, id: string): string {
> 33	  try {
> 34	    const meta = JSON.parse(readFileSync(join(dir, 'meta.json'), 'utf8'));
> 35	    return typeof meta.name === 'string' && meta.name ? meta.name : id;
> 36	  } catch {
> 37	    return id;
> 38	  }
> 39	}
> 40	
> 41	/** Map studio fps input (number | {num,den} rational) → integer fps for our composition spec (1..60). */
> 42	function fpsToInt(fps: unknown): number {
> 43	  if (typeof fps === 'number' && Number.isFinite(fps)) return Math.max(1, Math.min(60, Math.round(fps)));
> 44	  if (fps && typeof fps === 'object' && 'num' in (fps as Record<string, unknown>)) {
> 45	    const { num, den } = fps as { num: number; den?: number };
> 46	    return Math.max(1, Math.min(60, Math.round(num / (den || 1))));
> 47	  }
> 48	  return 30;
> 49	}
> 50	
> 51	const VALID_RESOLUTIONS = new Set(['portrait', 'landscape', 'square', 'portrait-4k', 'landscape-4k', 'square-4k']);
> 52	
> 53	export const mcorchAdapter: StudioApiAdapter = {
> 54	  listProjects(): ResolvedProject[] {
> 55	    if (!existsSync(STUDIO_PROJECTS_ROOT)) return [];
> 56	    return readdirSync(STUDIO_PROJECTS_ROOT, { withFileTypes: true })
> 57	      .filter((e) => e.isDirectory() && SAFE_ID.test(e.name) && existsSync(join(STUDIO_PROJECTS_ROOT, e.name, 'index.html')))
> 58	      .map((e) => {
> 59	        const dir = join(STUDIO_PROJECTS_ROOT, e.name);
> 60	        return { id: e.name, dir, title: projectTitle(dir, e.name) };
> 61	      });
> 62	  },
> 63	
> 64	  async resolveProject(id: string): Promise<ResolvedProject | null> {
> 65	    if (!SAFE_ID.test(id)) return null; // blocks traversal — ids are never path fragments
> 66	    const dir = resolve(STUDIO_PROJECTS_ROOT, id);
> 67	    if (!dir.startsWith(resolve(STUDIO_PROJECTS_ROOT) + '/')) return null; // defense-in-depth
> 68	    if (!existsSync(join(dir, 'index.html'))) {
> 69	      // FR-VS-049: local copy gone → try restoring the durable mirror (negative results cached 60s
> 70	      // so garbage ids don't hammer Storage on every route hit).
> 71	      if (missUntil.get(id) && missUntil.get(id)! > Date.now()) return null;
> 72	      const restored = await materializeProject(STUDIO_PROJECTS_ROOT, id);
> 73	      if (!restored) { missUntil.set(id, Date.now() + 60_000); return null; }
> 74	    }
> 75	    return { id, dir, title: projectTitle(dir, id) };
> 76	  },
> 77	
> 78	  async bundle(projectDir: string): Promise<string | null> {
> 79	    try {
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
> 160	          const { data: blob, error: dlErr } = await admin.storage.from('video-studio-assets').download(key);
> 161	          if (dlErr || !blob) { state.status = 'failed'; state.error = `Render concluído mas o download do bucket falhou: ${dlErr?.message ?? 'vazio'}`; return; }
> 162	          writeFileSync(opts.outputPath, Buffer.from(await blob.arrayBuffer()));
> 163	          state.progress = 1;
> 164	          state.status = 'complete';
> 165	          state.stage = 'concluído';
> 166	          return;
> 167	        }
> 168	      }
> 169	      state.status = 'failed';
> 170	      state.error = 'Timeout de 15min aguardando o worker — a linha video_renders segue viva (reaper re-claima).';
> 171	    })().catch((e) => {
> 172	      state.status = 'failed';
> 173	      state.error = e instanceof Error ? e.message : String(e);
> 174	    });
> 175	
> 176	    return state;
> 177	  },
> 178	
> 179	  // Optional surface intentionally omitted in 2a (§B.2): generateThumbnail (degrades gracefully),
> 180	  // resolveSession (SSO vhost is the session authority), registry catalog/install (supply-chain risk
> 181	  // in the render sandbox — MCORCH uses its own allowlist).
> 182	};
> 183	
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env bun
> 2	/**
> 3	 * scripts/video-studio-host/server.ts — Video Studio Host (Fase B sub-fatia 2a, SDD §VS-UI-B/§VS-UI-C).
> 4	 *
> 5	 * Mounts @hyperframes/studio-server `createStudioApi(mcorchAdapter)` under /api (the exact API the
> 6	 * @hyperframes/studio React app consumes) + serves the Apache-2.0 runtime IIFE same-origin at
> 7	 * /__hf/runtime.js (never a CDN). Loopback-only by design: the SSO ES256 vhost is the auth boundary
> 8	 * (mirrors design.mcorch.com / video.mcorch.com pattern) — this process trusts its local caller.
> 9	 *
> 10	 * Run: bun run scripts/video-studio-host/server.ts   (defaults: 127.0.0.1:3211 — the vanilla Fase A
> 11	 * editor keeps owning 3210 until sub-fatia 2c swaps the systemd service with rollback.)
> 12	 * SOP: docs/processes/video-studio-host-fase-b.md
> 13	 */
> 14	import { Hono } from 'hono';
> 15	import { createStudioApi } from '@hyperframes/studio-server';
> 16	import { readFileSync, existsSync } from 'fs';
> 17	import { fileURLToPath } from 'url';
> 18	import { join, resolve, dirname } from 'path';
> 19	import { mcorchAdapter } from './adapter';
> 20	import { startSyncLoop } from './sync';
> 21	
> 22	const PORT = Number(process.env.STUDIO_HOST_PORT ?? 3211);
> 23	const HOSTNAME = process.env.STUDIO_HOST_BIND ?? '127.0.0.1';
> 24	
> 25	// The runtime the preview injects — resolved from the installed @hyperframes/core package (LICENSE ships there).
> 26	const runtimePath = fileURLToPath(import.meta.resolve('@hyperframes/core/runtime'));
> 27	const runtimeJs = readFileSync(runtimePath);
> 28	
> 29	// Prebuilt Studio SPA (Fase B 2c): @hyperframes/studio ships its own built host (React 19 bundled INSIDE the
> 30	// dist assets — the package lives in an ISOLATED carrier package so react@19 never hoists into the SPA root).
> 31	// Apache-2.0, LICENSE in the tarball; telemetry is same-origin /api/events only (no external endpoints).
> 32	const __dir = dirname(fileURLToPath(import.meta.url));
> 33	const UI_DIST = resolve(process.env.STUDIO_UI_DIST
> 34	  ?? join(__dir, '../../packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist'));
> 35	const MIME: Record<string, string> = {
> 36	  '.html': 'text/html', '.js': 'application/javascript', '.css': 'text/css', '.svg': 'image/svg+xml',
> 37	  '.json': 'application/json', '.map': 'application/json', '.woff2': 'font/woff2', '.png': 'image/png',
> 38	};
> 39	
> 40	const app = new Hono();
> 41	app.get('/healthz', (c) => c.json({ ok: true, projects_root: process.env.STUDIO_PROJECTS_ROOT ?? '/home/ubuntu/.mcorch/video-studio/projects', ui: existsSync(join(UI_DIST, 'index.html')) }));
> 42	app.get('/__hf/runtime.js', (c) => c.body(runtimeJs, 200, { 'Content-Type': 'application/javascript', 'Cache-Control': 'public, max-age=3600' }));
> 43	app.route('/api', createStudioApi(mcorchAdapter));
> 44	
> 45	// Static Studio SPA — registered LAST; guard keeps /api|/__hf|/healthz out and jails paths under UI_DIST.
> 46	app.get('*', async (c) => {
> 47	  const path = new URL(c.req.url).pathname;
> 48	  if (path.startsWith('/api') || path.startsWith('/__hf') || path === '/healthz') return c.notFound();
> 49	  const rel = path === '/' ? '/index.html' : path;
> 50	  const fp = resolve(UI_DIST, '.' + rel);
> 51	  if (fp !== UI_DIST && !fp.startsWith(UI_DIST + '/')) return c.notFound(); // traversal jail
> 52	  const target = existsSync(fp) ? fp : join(UI_DIST, 'index.html');        // SPA fallback (hash routing)
> 53	  const ext = target.slice(target.lastIndexOf('.'));
> 54	  return new Response(Bun.file(target), { headers: { 'Content-Type': MIME[ext] ?? 'application/octet-stream' } });
> 55	});
> 56	
> 57	Bun.serve({ hostname: HOSTNAME, port: PORT, fetch: app.fetch, idleTimeout: 120 });
> 58	console.log(`🎬 video-studio-host listening on ${HOSTNAME}:${PORT} (ui=/, api=/api, runtime=/__hf/runtime.js, dist=${UI_DIST})`);
> 59	
> 60	// FR-VS-049 write-back loop (SOP §2b): periodic + final flush on shutdown. Best-effort — never blocks the editor.
> 61	const PROJECTS_ROOT = process.env.STUDIO_PROJECTS_ROOT ?? '/home/ubuntu/.mcorch/video-studio/projects';
> 62	const flushSync = startSyncLoop(PROJECTS_ROOT);
> 63	for (const sig of ['SIGTERM', 'SIGINT'] as const) {
> 64	  process.on(sig, () => { void flushSync().finally(() => process.exit(0)); });
> 65	}
> 66	
> ```

## 🤖 Claude *(06:33:16)*


## 🤖 Claude *(06:33:17)*

Let me confirm what's actually live behind the vhost (port 3210 vanilla vs 3211 Fase B host) and the hash-routing seam.

## 🤖 Claude *(06:33:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== listening ports 3210/3211 ===\"; (ss -ltnp 2>/dev/null || netstat -ltnp 2>/dev/null) | grep -E ':321[01]' || echo \"(no ss/netstat visibility or not listening)\"\necho; echo \"=== systemd unit (ubuntu user) ===\"; cat /home/ubuntu/.config/systemd/user/video-studio.service 2>/dev/null || echo \"(no access to /home/ubuntu unit)\"\necho; echo \"=== live project dirs ===\"; ls -la /home/ubuntu/.mcorch/video-studio/projects/ 2>/dev/null || echo \"(no access to projects dir)\"\necho; echo \"=== grep #project / useServerConnection / hash in repo (npm pkg is external) ===\"; grep -rn \"#project\\|useServerConnection\\|location.hash\\|project=\" src/pages/VideoStudioEditorPage.tsx scripts/video-studio-host/ 2>/dev/null | head",
  "description": "Check live ports, systemd unit, project dirs, hash seam"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === listening ports 3210/3211 ===
> LISTEN 0      512        127.0.0.1:3210       0.0.0.0:*    users:(("bun",pid=4052531,fd=12))            
> 
> === systemd unit (ubuntu user) ===
> [Unit]
> Description=MCORCH Video Studio Host (Fase B — createStudioApi(McorchAdapter) + prebuilt Studio SPA, SDD §VS-UI-B/§VS-UI-C; behind video.mcorch.com)
> After=network-online.target
> Wants=network-online.target
> StartLimitBurst=5
> StartLimitIntervalSec=60
> 
> [Service]
> # Fase B swap (§B.5, 2026-07-01): our host replaces the vanilla `hyperframes preview` on the SAME port 3210.
> # Serves: prebuilt @hyperframes/studio dist (Apache-2.0, isolated carrier package) + /api (McorchAdapter:
> # multi-project, startRender→video-render edge fn = single billing chokepoint) + /__hf/runtime.js.
> # ROLLBACK (Fase A vanilla): swap ExecStart back to:
> #   /home/ubuntu/.local/bin/node /home/ubuntu/.bun/install/global/node_modules/hyperframes/dist/cli.js preview /home/ubuntu/.mcorch/video-studio/projects/mcorch-video --port 3210 --no-open
> # (and WorkingDirectory=/home/ubuntu/.mcorch/video-studio/projects)
> WorkingDirectory=/home/gcrUX/htdocs/constellation-orchestra
> ExecStart=/home/ubuntu/.bun/bin/bun run scripts/video-studio-host/server.ts
> Environment=STUDIO_HOST_PORT=3210
> Restart=always
> RestartSec=5
> TimeoutStopSec=15
> KillMode=control-group
> Environment=HOME=/home/ubuntu
> Environment=TMPDIR=/tmp
> Environment=NODE_EXTRA_CA_CERTS=/etc/ssl/certs/ca-certificates.crt
> Environment=PATH=/home/ubuntu/.local/bin:/home/ubuntu/.nvm/versions/node/v22.22.3/bin:/home/ubuntu/.bun/bin:/usr/local/bin:/usr/bin:/bin
> 
> [Install]
> WantedBy=default.target
> 
> === live project dirs ===
> total 16
> drwxrwxr-x 4 ubuntu ubuntu 4096 Jul  1 19:28 .
> drwxrwxr-x 3 ubuntu ubuntu 4096 Jun 24 19:57 ..
> drwxrwxr-x 4 ubuntu ubuntu 4096 Jul  4 00:30 mcorch-demo
> drwxrwxr-x 6 ubuntu ubuntu 4096 Jul  1 19:01 mcorch-video
> 
> === grep #project / useServerConnection / hash in repo (npm pkg is external) ===
> ```

## 🤖 Claude *(06:33:31)*


## 🤖 Claude *(06:33:32)*

The Fase B swap IS live — the systemd unit runs our `server.ts` (McorchAdapter, multi-project) on port 3210. Two projects exist. Now let me verify the exact deep-link mechanism in the built Studio SPA (the hash param name is the load-bearing fact).

## 🤖 Claude *(06:33:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nDIST=\"packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist\"\necho \"=== dist present? ===\"; ls -la \"$DIST\" 2>/dev/null | head; ls \"$DIST\"/assets 2>/dev/null | head\necho; echo \"=== hash/project deep-link seam in built SPA ===\"\ngrep -roER \"hash|#project|useServerConnection|searchParams|project=|projectId\" \"$DIST\" 2>/dev/null | grep -iE \"project|hash|searchParams\" | head -30\necho; echo \"=== broader: how the SPA picks the active project (grep minified) ===\"\ngrep -roiE \"location\\.(hash|search)|URLSearchParams|get\\(\\\"project|get\\('project|#project=|\\\\?project=\" \"$DIST\" 2>/dev/null | head -30",
  "description": "Grep built Studio SPA dist for hash/project deep-link seam"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === dist present? ===
> total 5152
> drwxrwxr-x 5 gcrUX gcrUX    4096 Jul  1 19:04 .
> drwxrwxr-x 4 gcrUX gcrUX    4096 Jul  1 19:04 ..
> drwxrwxr-x 2 gcrUX gcrUX    4096 Jul  1 19:04 assets
> -rw-rw-r-- 2 gcrUX gcrUX   31389 Jul  1 19:04 chunk-AN2EWWK3.js
> -rw-rw-r-- 2 gcrUX gcrUX   72222 Jul  1 19:04 chunk-AN2EWWK3.js.map
> -rw-rw-r-- 2 gcrUX gcrUX    1080 Jul  1 19:04 domEditingLayers-EK7R7R4G.js
> -rw-rw-r-- 2 gcrUX gcrUX      71 Jul  1 19:04 domEditingLayers-EK7R7R4G.js.map
> -rw-rw-r-- 2 gcrUX gcrUX    1066 Jul  1 19:04 favicon.svg
> drwxrwxr-x 3 gcrUX gcrUX    4096 Jul  1 19:04 icons
> hyperframes-player-DNLS_l47.js
> index-B4h4u7eW.js
> index-B_gDTiNI.js
> index-DmkOvZns.css
> index-gk_X4nXD.js
> 
> === hash/project deep-link seam in built SPA ===
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/chunk-AN2EWWK3.js:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/chunk-AN2EWWK3.js:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/chunk-AN2EWWK3.js:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/chunk-AN2EWWK3.js:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/chunk-AN2EWWK3.js.map:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/chunk-AN2EWWK3.js.map:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/chunk-AN2EWWK3.js.map:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/chunk-AN2EWWK3.js.map:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/chunk-AN2EWWK3.js.map:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.d.ts:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.d.ts:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.d.ts:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.d.ts:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:hash
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:hash
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:#project
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:hash
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:hash
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:hash
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:projectId
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:projectId
> 
> === broader: how the SPA picks the active project (grep minified) ===
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:location.hash
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:URLSearchParams
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:URLSearchParams
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:URLSearchParams
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:URLSearchParams
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:URLSearchParams
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:location.hash
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:URLSearchParams
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:location.hash
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:location.hash
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:location.hash
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:URLSearchParams
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:location.search
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:location.hash
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:location.hash
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:location.hash
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js:location.hash
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/assets/hyperframes-player-DNLS_l47.js:URLSearchParams
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js.map:location.hash
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js.map:URLSearchParams
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js.map:URLSearchParams
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js.map:URLSearchParams
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js.map:URLSearchParams
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js.map:URLSearchParams
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js.map:URLSearchParams
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js.map:URLSearchParams
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js.map:URLSearchParams
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js.map:URLSearchParams
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js.map:location.hash
> packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js.map:location.hash
> ```

## 🤖 Claude *(06:33:42)*


## 🤖 Claude *(06:33:42)*

The `#project` literal is confirmed in the built SPA. Let me extract the exact context to nail down the deep-link format.

## 🤖 Claude *(06:33:45)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nDIST=\"packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist\"\necho \"=== context around #project in built SPA ===\"\ngrep -oE \".{140}#project.{200}\" \"$DIST/index.js\" | head -5\necho; echo \"=== context around location.hash (project selection) ===\"\ngrep -oE \".{80}location\\.hash.{120}\" \"$DIST/index.js\" | head -8",
  "description": "Extract exact deep-link hash parsing context from built SPA"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === context around #project in built SPA ===
> 
> === context around location.hash (project selection) ===
> ```

## 🤖 Claude *(06:33:53)*


## 🤖 Claude *(06:33:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nnode -e '\nconst fs=require(\"fs\");\nconst f=\"packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js\";\nconst s=fs.readFileSync(f,\"utf8\");\nfor(const needle of [\"#project\",\"location.hash\"]){\n  let i=s.indexOf(needle), n=0;\n  console.log(\"\\n===== \"+needle+\" =====\");\n  while(i>=0 && n<4){\n    console.log(\"\u2026\"+s.slice(Math.max(0,i-160), i+180).replace(/\\n/g,\" \")+\"\u2026\");\n    i=s.indexOf(needle,i+1); n++;\n  }\n}\n'",
  "description": "Extract deep-link hash parsing context via node"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== #project =====
> …ight,     viewport_width: window.innerWidth,     viewport_height: window.innerHeight,     user_agent: navigator.userAgent,     url_hash: location.hash.replace(/#project\//, "")   }; } function trackStudioEvent(event, properties = {}) {   if (!isEnabled()) return;   queue.push({     event: `studio:${event}`,     properties: { ...getSession…
> …oks/useFrameCapture.ts import { useState as useState52, useCallback as useCallback72 } from "react";  // src/utils/projectRouting.ts var PROJECT_HASH_PREFIX = "#project/"; function decodeHashProjectId(value) {   try {     return decodeURIComponent(value);   } catch {     return value;   } } function normalizeHashParams(params) {   if (!pa…
> 
> ===== location.hash =====
> …ight: window.screen?.height,     viewport_width: window.innerWidth,     viewport_height: window.innerHeight,     user_agent: navigator.userAgent,     url_hash: location.hash.replace(/#project\//, "")   }; } function trackStudioEvent(event, properties = {}) {   if (!isEnabled()) return;   queue.push({     event: `studio:${event}`,     prop…
> …}; } function readStudioUrlStateFromWindow() {   if (typeof window === "undefined") return defaultStudioUrlState();   return parseStudioUrlStateFromHash(window.location.hash); } function buildStudioHash(projectId, state) {   const params = new URLSearchParams();   params.set("v", "1");   if (state.activeCompPath) params.set("comp", state.…
> … void 0,     selectorIndex: selection.selectorIndex ?? void 0   }; } function replaceHash(nextHash) {   if (typeof window === "undefined") return;   if (window.location.hash === nextHash) return;   window.history.replaceState(null, "", nextHash); } function useStudioUrlState({   projectId,   activeCompPath,   duration,   isPlaying,   comp…
> …ydrated, buildUrlState, projectId]);   useEffect43(() => {     if (!projectId) return;     const onHashChange = () => {       if (parseProjectIdFromHash(window.location.hash) !== projectId) return;       const parsed = parseStudioUrlStateFromHash(window.location.hash);       if (parsed.currentTime != null) {         const clamped = durati…
> ```

## 🤖 Claude *(06:34:01)*


## 🤖 Claude *(06:34:01)*

Let me extract the exact `parseProjectIdFromHash` function to confirm the precise parsing.

## 🤖 Claude *(06:34:05)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nnode -e '\nconst fs=require(\"fs\");\nconst f=\"packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js\";\nconst s=fs.readFileSync(f,\"utf8\");\nfor(const needle of [\"function parseProjectIdFromHash\",\"PROJECT_HASH_PREFIX =\",\"function parseStudioUrlStateFromHash\"]){\n  const i=s.indexOf(needle);\n  if(i>=0) console.log(\"\\n===== \"+needle+\" =====\\n\"+s.slice(i, i+330).replace(/\\n/g,\" \"));\n  else console.log(\"\\n(not found: \"+needle+\")\");\n}\n'",
  "description": "Extract parseProjectIdFromHash implementation"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== function parseProjectIdFromHash =====
> function parseProjectIdFromHash(hash) {   return parseProjectHashRoute(hash)?.projectId ?? null; } function buildProjectApiPath(projectId, suffix = "") {   const normalizedSuffix = suffix && !suffix.startsWith("/") ? `/${suffix}` : suffix;   return `/api/projects/${encodeProjectId(projectId)}${normalizedSuffix}`; }  // src/utils
> 
> ===== PROJECT_HASH_PREFIX = =====
> PROJECT_HASH_PREFIX = "#project/"; function decodeHashProjectId(value) {   try {     return decodeURIComponent(value);   } catch {     return value;   } } function normalizeHashParams(params) {   if (!params) return new URLSearchParams();   if (params instanceof URLSearchParams) return params;   const next = new URLSearchParams(
> 
> ===== function parseStudioUrlStateFromHash =====
> function parseStudioUrlStateFromHash(hash) {   const route = parseProjectHashRoute(hash);   if (!route) return defaultStudioUrlState();   const { params } = route;   return {     activeCompPath: params.get("comp") || null,     currentTime: parseNumber(params.get("t")),     rightPanelTab: normalizeStudioUrlPanelTab(parseTab(param
> ```

## 🤖 Claude *(06:34:37)*


## 🤖 Claude *(06:34:38)*

Let me confirm the materialization contract in sync.ts (the Storage↔dir mirror that a deep-link would rely on to open a not-yet-local creative).

## 🤖 Claude *(06:34:38)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/video-studio-host/sync.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	/**
> 2	 * scripts/video-studio-host/sync.ts — FR-VS-049 (SDD §VS-UI-B B.4 · SOP video-studio-host-fase-b.md §2b):
> 3	 * Storage↔volume durability for Studio-authored projects.
> 4	 *
> 5	 * The studio's files/* routes write straight to the local dir (local FS = canonical, single-tenant v1) —
> 6	 * this module mirrors it: (a) write-back sweep (periodic + on SIGTERM) uploads mtime-changed files to the
> 7	 * private bucket `video-studio-projects` under projects/<id>/<relpath>; (b) materializeProject() restores
> 8	 * a project dir from the bucket when the local copy is missing (staging + atomic rename — a partial
> 9	 * download never leaves a half-dir). Best-effort by design: sync failures log and retry next tick,
> 10	 * NEVER blocking the editor.
> 11	 */
> 12	import { createClient } from '@supabase/supabase-js';
> 13	import { readdirSync, existsSync, statSync, readFileSync, mkdirSync, writeFileSync, renameSync, rmSync } from 'fs';
> 14	import { join, dirname, resolve } from 'path';
> 15	import { walkDir, getMimeType } from '@hyperframes/studio-server';
> 16	
> 17	const SUPABASE_URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL ?? '';
> 18	const SVC = process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY ?? '';
> 19	const BUCKET = 'video-studio-projects';
> 20	const MAX_BYTES = 50 * 1024 * 1024; // skip huge binaries — renders live in video-studio-assets already
> 21	const SAFE_ID = /^[a-zA-Z0-9_-]+$/;
> 22	// Outputs + temp bundles are reproducible noise, not authored state.
> 23	const EXCLUDE = /(^|\/)(renders|node_modules)(\/|$)|(^|\/)\.hf-native-bundle-/;
> 24	
> 25	const admin = createClient(SUPABASE_URL, SVC, { auth: { persistSession: false } });
> 26	
> 27	// relKey (projects/<id>/<relpath>) → last-uploaded mtimeMs. In-memory: first sweep re-upserts everything
> 28	// (idempotent), later sweeps only deltas.
> 29	const lastSync = new Map<string, number>();
> 30	
> 31	/** One write-back pass over every project under root. Best-effort — returns counts, never throws. */
> 32	export async function sweepProjects(root: string): Promise<{ uploaded: number; failed: number; skipped: number }> {
> 33	  let uploaded = 0, failed = 0, skipped = 0;
> 34	  if (!existsSync(root)) return { uploaded, failed, skipped };
> 35	  const ids = readdirSync(root, { withFileTypes: true })
> 36	    .filter((e) => e.isDirectory() && SAFE_ID.test(e.name) && existsSync(join(root, e.name, 'index.html')))
> 37	    .map((e) => e.name);
> 38	
> 39	  for (const id of ids) {
> 40	    const dir = join(root, id);
> 41	    let rels: string[] = [];
> 42	    try { rels = walkDir(dir); } catch { continue; }
> 43	    for (const rel of rels) {
> 44	      if (EXCLUDE.test(rel)) { skipped++; continue; }
> 45	      const abs = join(dir, rel);
> 46	      let st; try { st = statSync(abs); } catch { continue; }
> 47	      if (st.size > MAX_BYTES) { skipped++; continue; }
> 48	      const key = `projects/${id}/${rel}`;
> 49	      if (lastSync.get(key) === st.mtimeMs) continue;
> 50	      try {
> 51	        const { error } = await admin.storage.from(BUCKET)
> 52	          .upload(key, readFileSync(abs), { upsert: true, contentType: getMimeType(rel) });
> 53	        if (error) throw new Error(error.message);
> 54	        lastSync.set(key, st.mtimeMs);
> 55	        uploaded++;
> 56	      } catch (e) {
> 57	        failed++;
> 58	        console.error(`[sync] upload failed ${key}: ${e instanceof Error ? e.message : e}`);
> 59	      }
> 60	    }
> 61	  }
> 62	  if (uploaded || failed) console.log(`[sync] uploaded ${uploaded} files (${failed} failed, ${skipped} skipped)`);
> 63	  return { uploaded, failed, skipped };
> 64	}
> 65	
> 66	/** Recursive bucket listing under a prefix (Storage list() is per-folder — folders come back with id=null). */
> 67	async function listRecursive(prefix: string): Promise<string[]> {
> 68	  const out: string[] = [];
> 69	  const { data, error } = await admin.storage.from(BUCKET).list(prefix, { limit: 1000 });
> 70	  if (error || !data) return out;
> 71	  for (const entry of data) {
> 72	    if (entry.id === null) out.push(...await listRecursive(`${prefix}/${entry.name}`)); // folder
> 73	    else out.push(`${prefix}/${entry.name}`);
> 74	  }
> 75	  return out;
> 76	}
> 77	
> 78	/**
> 79	 * Restore a project dir from the bucket (adapter.resolveProject fallback when the local copy is gone).
> 80	 * Downloads to a staging dir, then atomic-renames into place — failure leaves NO half-materialized dir.
> 81	 * Returns true iff the project dir exists (materialized) afterwards.
> 82	 */
> 83	export async function materializeProject(root: string, id: string): Promise<boolean> {
> 84	  if (!SAFE_ID.test(id)) return false;
> 85	  const dir = resolve(root, id);
> 86	  if (existsSync(dir)) return true;
> 87	
> 88	  const keys = await listRecursive(`projects/${id}`);
> 89	  if (!keys.some((k) => k.endsWith('/index.html'))) return false; // not a mirrored project
> 90	
> 91	  const staging = join(root, `.materialize-${id}-${process.pid}`);
> 92	  try {
> 93	    for (const key of keys) {
> 94	      const rel = key.slice(`projects/${id}/`.length);
> 95	      // Defense-in-depth (security-review 2026-07-01 forward-note): keys are sweep-authored today
> 96	      // (SAFE_ID + walkDir → no '..'), but reject traversal outright before multi-tenant lands.
> 97	      if (!rel || rel.includes('..') || rel.startsWith('/')) continue;
> 98	      const { data, error } = await admin.storage.from(BUCKET).download(key);
> 99	      if (error || !data) throw new Error(`download ${key}: ${error?.message ?? 'empty'}`);
> 100	      const abs = join(staging, rel);
> 101	      mkdirSync(dirname(abs), { recursive: true });
> 102	      writeFileSync(abs, Buffer.from(await data.arrayBuffer()));
> 103	    }
> 104	    renameSync(staging, dir); // atomic — the dir only appears complete
> 105	    console.log(`[sync] materialized ${id} from bucket (${keys.length} files)`);
> 106	    return true;
> 107	  } catch (e) {
> 108	    console.error(`[sync] materialize ${id} failed: ${e instanceof Error ? e.message : e}`);
> 109	    rmSync(staging, { recursive: true, force: true });
> 110	    return false;
> 111	  }
> 112	}
> 113	
> 114	/** Start the periodic write-back loop. Returns a flush fn for the SIGTERM hook. */
> 115	export function startSyncLoop(root: string, intervalS = Number(process.env.STUDIO_SYNC_INTERVAL_S ?? 60)): () => Promise<void> {
> 116	  let running = false;
> 117	  const tick = async () => {
> 118	    if (running) return; // never overlap sweeps
> 119	    running = true;
> 120	    try { await sweepProjects(root); } finally { running = false; }
> 121	  };
> 122	  const timer = setInterval(tick, Math.max(10, intervalS) * 1000);
> 123	  void tick(); // initial sweep at boot
> 124	  return async () => { clearInterval(timer); await tick(); };
> 125	}
> 126	
> ```

## 🤖 Claude *(06:35:25)*


## 🤖 Claude *(06:35:26)*

I have the complete, empirically-grounded picture. Here is my analysis.

## 🤖 Claude *(06:36:28)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "seam": "The deep-link seam is the iframe URL HASH, read client-side by the embedded @hyperframes/studio SPA \u2014 NOT a query string and NOT a MCORCH-side route param. Chain: React route `spaces/video` (App.tsx:147) \u2192 `VideoStudioEditorPage.tsx` renders a single bare `<iframe src=\"https://video.mcorch.com\">` with NO param/hash today \u2192 nginx `video.mcorch.com.conf` SSO-gates every request (auth_request \u2192 sso-auth-gate :8787 verifying the sb-mcorch-session ES256 JWT) and proxies `/` \u2192 `127.0.0.1:3210` \u2192 port 3210 is LIVE-serving the Fase B host `scripts/video-studio-host/server.ts` (running bun pid 4052531; systemd `video-studio.service` ExecStart already swapped to our host, NOT the vanilla single-project CLI). server.ts mounts `createStudioApi(mcorchAdapter)` under `/api`, serves the prebuilt React-19 Studio SPA static (with SPA fallback so hash routing works), and serves the runtime IIFE at `/__hf/runtime.js`.\n\nEMPIRICAL deep-link format (grepped from the built SPA dist `packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js`): the SPA reads the active project from `window.location.hash`. Constants/fns present: `PROJECT_HASH_PREFIX = \"#project/\"`, `parseProjectIdFromHash(hash)` (via `parseProjectHashRoute`), `parseStudioUrlStateFromHash`, `buildStudioHash(projectId,state)`, `replaceHash` (history.replaceState). So the correct deep-link is `https://video.mcorch.com/#project/<projectId>` (path-style after the hash) \u2014 the older blueprint's `#project=<id>` was a hand-wave and is WRONG. Extra editor state rides as URLSearchParams after the id: `#project/<id>?v=1&comp=<compPath>&t=<seconds>&...`. On load the SPA parses the hash \u2192 `<projectId>` \u2192 `buildProjectApiPath` = `/api/projects/<encodeURIComponent(id)>` \u2192 hits `mcorchAdapter.resolveProject(id)`.",
  "integration_points": [
    {
      "file_line": "src/pages/VideoStudioEditorPage.tsx:18",
      "description": "The ONLY MCORCH-side change point. Today `<iframe src=\"https://video.mcorch.com\">` is static with no project selection \u2014 always lands on the SPA default picker. To open a specific creative: read a param (e.g. useSearchParams().get('project') on /dashboard/spaces/video?project=<id>) and set src=`https://video.mcorch.com/#project/${encodeURIComponent(id)}`. The hash is client-only, never reaches nginx/SSO, so no vhost change. Parent\u2192iframe via src is one-way (cross-origin blocks reading it back \u2014 fine for opening)."
    },
    {
      "file_line": "scripts/video-studio-host/adapter.ts:64",
      "description": "resolveProject(id) \u2014 the id-resolution boundary. Validates id against SAFE_ID `/^[a-zA-Z0-9_-]+$/` (so ids are dir-name slugs, never UUIDs-with-dashes work but no path fragments), resolves `<STUDIO_PROJECTS_ROOT>/<id>`, and if the local dir is gone calls materializeProject() to restore from the bucket. This is where a Spaces-UUID\u2192Studio-project mapping would have to be taught, OR extended to look up vm_canvas_projects/creative_assets and materialize on the fly."
    },
    {
      "file_line": "scripts/video-studio-host/adapter.ts:54",
      "description": "listProjects() \u2014 enumerates dirs under STUDIO_PROJECTS_ROOT that contain index.html. This is the project catalog the picker shows. Two exist today (mcorch-demo, mcorch-video, both hyperframes-init seeds)."
    },
    {
      "file_line": "scripts/video-studio-host/sync.ts:83",
      "description": "materializeProject(root,id) \u2014 restores a project dir from the PRIVATE bucket `video-studio-projects` at prefix `projects/<id>/...` (needs an index.html key to count as a project). This is the ONLY path by which a not-yet-local creative could become openable: upload a composition tree to video-studio-projects/projects/<id>/ and resolveProject will hydrate it. Requires SAFE_ID + a real index.html."
    },
    {
      "file_line": "scripts/video-studio-host/adapter.ts:115",
      "description": "startRender(opts) \u2014 the billing seam (mints User-Zero JWT \u2192 POST video-render edge fn \u2192 poll video_renders \u2192 download MP4). Unrelated to opening a project, but it's what the Export button triggers once a project is open; opts.project.id/.dir come from resolveProject."
    },
    {
      "file_line": "nginx/video.mcorch.com.conf:60",
      "description": "SSO gate: every request auth_request\u2192:8787 verifies the .mcorch.com session cookie (ES256). The hash is NOT sent to the server so deep-linking needs no vhost change; but the gate is the ONLY tenant boundary today (single-tenant User Zero \u2014 no per-project ownership check)."
    }
  ],
  "how_to_extend": "To make a Spaces node \"open the project directly in /dashboard/spaces/video\":\n\nSTEP 1 (trivial, frontend): Make VideoStudioEditorPage.tsx param-aware. Read `?project=<id>` (or a route segment) and compose iframe src = `https://video.mcorch.com/#project/${encodeURIComponent(id)}`. That alone makes the Studio SPA select project `<id>` on load via resolveProject. Optionally append `?comp=<compPath>&t=<sec>` inside the hash to jump to a specific composition/time. No nginx, no server change.\n\nSTEP 2 (the real work \u2014 the identity bridge): `<id>` MUST be a Studio project id = a dir name resolvable by resolveProject. Spaces creatives are a DIFFERENT identity space (vm_canvas_projects rows keyed by UUID; assets in canvas-assets/video-studio-assets buckets keyed `<user>/<project>/...`). There is NO existing producer that writes an editable HyperFrames project (index.html + compositions) for a Spaces node \u2014 autopilot/video-bridge only writes finished MP4s to video-studio-assets/<user>/<renderId>.mp4 (outputs, not projects). So you must add ONE of:\n  (a) A deterministic Spaces-UUID \u2192 Studio-slug map + an on-open compiler that builds an index.html composition from the creative and uploads it to bucket `video-studio-projects/projects/<slug>/`, so resolveProject\u2192materializeProject hydrates it; the node links to `?project=<slug>`; OR\n  (b) Extend mcorchAdapter.resolveProject to accept a Supabase-native id (relax SAFE_ID carefully, or use a slug), look up vm_canvas_projects/creative_assets, and materialize a dir at open time.\n\nSTEP 3 (before multi-tenant): resolveProject/materializeProject currently trust the id with NO per-user ownership check (single-tenant User Zero, OTD-VA-011/OTD-VS-019). Any client-supplied id that drives bucket-path materialization must gain an ownership check (verify the id belongs to the SSO-authenticated user) before User 1.",
  "gotchas": "1. WRONG-FORMAT TRAP: the deep-link is `#project/<id>` (hash, path-style), NOT `?project=<id>` and NOT `#project=<id>`. The `?project=<id>` form (if used) belongs on the MCORCH /dashboard/spaces/video URL only; you must translate it into the `#project/<id>` HASH on the iframe src. Confirmed empirically from PROJECT_HASH_PREFIX=\"#project/\" in the built dist.\n2. LIVE server is the Fase B host, not the vanilla CLI: docs/HANDOFF say '3211, vanilla owns 3210 until swap 2c' but the swap already happened \u2014 systemd video-studio.service ExecStart runs scripts/video-studio-host/server.ts with STUDIO_HOST_PORT=3210 (a bun proc is listening on 127.0.0.1:3210). So multi-project resolveProject IS live. Don't trust the stale 'single-project' notes.\n3. IDENTITY MISMATCH is the core blocker: Studio project id = filesystem DIR NAME (slug, SAFE_ID `/^[a-zA-Z0-9_-]+$/`) under /home/ubuntu/.mcorch/video-studio/projects/. Spaces project id = vm_canvas_projects UUID. Raw UUIDs pass SAFE_ID (hex+dashes) but there's no dir/bucket entry named by that UUID, so resolveProject returns null \u2192 SPA falls back to picker. Opening 'the' creative requires materialization, not just a matching string.\n4. THREE DIFFERENT BUCKETS \u2014 don't confuse them: Studio PROJECT source = `video-studio-projects` (prefix projects/<id>/); Studio/render OUTPUT mp4 = `video-studio-assets` (<user>/<renderId>.mp4); Spaces/Canvas assets = `canvas-assets`/`video-studio-assets`. materializeProject reads ONLY video-studio-projects.\n5. Cross-origin: parent login.mcorch.com can SET iframe src (incl. hash) but cannot READ the iframe hash back or postMessage across without a handshake the Studio doesn't expose \u2014 so deep-link is one-way (open), not two-way (no way to know which project the user later switched to inside the iframe).\n6. resolveProject requires index.html to exist (both listProjects filter and materializeProject's `keys.some(endsWith('/index.html'))`) \u2014 a creative with only media assets and no composition html is NOT a valid Studio project.\n7. materializeProject caches misses 60s (missUntil map) \u2014 a just-uploaded project may 404 for up to 60s if a prior miss was cached for that id.",
  "security_review_needed": true,
  "key_files": [
    {
      "path": "src/App.tsx",
      "role": "Route wiring: spaces/video \u2192 VideoStudioEditorPage (line 147); legacy canvas/video \u2192 302 redirect (line 153); spaces/:id \u2192 CanvasEditorPage (the Canvas/Spaces UUID projects, line 149)."
    },
    {
      "path": "src/pages/VideoStudioEditorPage.tsx",
      "role": "The MCORCH-side editor page \u2014 a bare iframe to https://video.mcorch.com with NO project selection today. The single change point to add a `?project=` \u2192 `#project/<id>` deep-link."
    },
    {
      "path": "nginx/video.mcorch.com.conf",
      "role": "SSO-gated vhost proxying / \u2192 127.0.0.1:3210; the only tenant boundary today. Hash never reaches it, so deep-linking needs no vhost change."
    },
    {
      "path": "scripts/video-studio-host/server.ts",
      "role": "LIVE Fase B host on :3210 \u2014 mounts createStudioApi(mcorchAdapter) at /api, serves the prebuilt @hyperframes/studio React-19 SPA (SPA fallback enables hash routing) + runtime IIFE at /__hf/runtime.js."
    },
    {
      "path": "scripts/video-studio-host/adapter.ts",
      "role": "mcorchAdapter (StudioApiAdapter). listProjects/resolveProject define project identity = dir name under STUDIO_PROJECTS_ROOT; startRender is the billing seam to video-render. resolveProject:64 is where a Spaces-id mapping would be taught."
    },
    {
      "path": "scripts/video-studio-host/sync.ts",
      "role": "FR-VS-049 durability mirror: sweeps authored files \u2192 bucket video-studio-projects/projects/<id>/; materializeProject() restores a dir from that bucket \u2014 the only path to make a not-yet-local creative openable."
    },
    {
      "path": "packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/index.js",
      "role": "Built Studio SPA (external Apache-2.0 pkg). Source of the empirical deep-link truth: PROJECT_HASH_PREFIX=\"#project/\", parseProjectIdFromHash, buildStudioHash, buildProjectApiPath \u2192 /api/projects/<id>."
    },
    {
      "path": "docs/bok/video-studio/05-sdd.md",
      "role": "\u00a7A.2/\u00a7VS-UI-B: StudioApiAdapter contract (13 call-sites), OTD-VS-016 (CLI single-project), OTD-VS-011/019 (single-tenant deferral). Reference for the adapter surface."
    }
  ],
  "data_shapes": "Studio ResolvedProject = { id: string (dir-name slug, SAFE_ID /^[a-zA-Z0-9_-]+$/), dir: absolute path under STUDIO_PROJECTS_ROOT=/home/ubuntu/.mcorch/video-studio/projects, title: from <dir>/meta.json .name || id }. A project on disk = a dir containing index.html (+ meta.json, compositions/, assets/). Deep-link hash = `#project/<encodeURIComponent(projectId)>` optionally followed by `?v=1&comp=<compPath>&t=<seconds>&...`. Live catalog today: two dirs, `mcorch-demo` and `mcorch-video` (hyperframes-init seeds). Spaces/Canvas project (the OTHER identity space) = vm_canvas_projects row keyed by UUID with a `graph` jsonb; disjoint from the Studio filesystem/slug model.",
  "unknowns": "1. No producer found that compiles a Spaces creative into an editable HyperFrames project (index.html + compositions) under video-studio-projects \u2014 only finished MP4 outputs exist (video-studio-assets/<user>/<renderId>.mp4). Confirm with the Spaces\u2192video pipeline owner whether any such compiler is planned; if not, STEP 2 above must build it. 2. Exact URLSearchParams keys the SPA honors inside the hash beyond v/comp/t/panel-tab (would need deeper dist read to deep-link to a precise composition+time, not just the project). 3. Whether the running :3210 process is the swapped Fase B host in ALL respects (I confirmed the systemd unit ExecStart + a listening bun proc, but did not curl /api/projects to enumerate live output \u2014 /api is loopback-only and SSO-gated, not reachable from this shell without minting a session). 4. Per-user ownership model for multi-tenant (OTD-VA-011/OTD-VS-019 deferred) \u2014 resolveProject has no ownership check today."
}
```

> **Tool Result (StructuredOutput)** - ✅ Success
>
> ```
> Structured output provided successfully
> ```

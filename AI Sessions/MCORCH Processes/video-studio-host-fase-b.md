# SOP — Video Studio Host (Fase B, sub-fatia 2a: servidor API + auth-bridge)

> Lei 2 (Processo Antecipado) — escrito ANTES do código. BoK SSOT: `docs/bok/video-studio/05-sdd.md`
> §VS-UI-B (contrato McorchAdapter, FR-VS-048/049) + §VS-UI-C (render nativo FR-VS-050).
> Escopo 2a: servidor `createStudioApi(McorchAdapter)` em loopback + seam `startRender`→`video-render`
> (FR-VS-048 opção A — JWT do Usuário Zero mintado server-side; edge fn = chokepoint ÚNICO de billing).
> FORA do escopo 2a: FS sync Storage↔volume (FR-VS-049, sub-fatia 2b) · host React 19 + swap do
> service (sub-fatia 2c) · ativação do billing (`VIDEO_HYPERFRAMES_WEBHOOK` — GO Sovereign, Fila).

## Operator

Hoje: o Sovereign (ou o agente) opera o editor vanilla (`video-studio.service`, porta 3210) e dispara
renders manualmente (insert de `video_renders` via service key OU `hyperframes render` local).
Com 2a: o mesmo operador sobe o host novo em **loopback 3211** (teste, sem tocar o 3210) e usa a API.

## Sequence (com gate de verificação por step)

1. **Env**: `.env` do repo já carrega `VITE_SUPABASE_URL` + `SB_SECRET_KEY` + `SB_PUBLISHABLE_KEY`.
   Extras do host: `STUDIO_PROJECTS_ROOT` (default `/home/ubuntu/.mcorch/video-studio/projects`),
   `STUDIO_HOST_PORT` (default 3211), `USER_ZERO_EMAIL` (default gabrielcall@gmail.com).
   *Gate:* `bun run scripts/video-studio-host/server.ts` imprime `listening on 127.0.0.1:<port>`.
2. **Projects**: `curl 127.0.0.1:3211/api/projects` → JSON com `mcorch-video` (id+title do meta.json).
   *Gate:* HTTP 200 + array não-vazio.
3. **Runtime**: `curl -sI 127.0.0.1:3211/__hf/runtime.js` → 200, `content-length: 230005`
   (o IIFE Apache-2.0 do core, byte-idêntico ao verificado na §VS-UI-C C.1).
4. **Preview**: `curl 127.0.0.1:3211/api/projects/mcorch-video/preview` → 200 HTML contendo
   `data-composition-id="mcorch-viral"`. *Gate:* HTML não-vazio, runtime referenciado.
5. **Render (seam FR-VS-048)**: `curl -X POST 127.0.0.1:3211/api/projects/mcorch-video/render
   -d '{"format":"mp4","fps":30,"quality":"standard"}'` → o adapter minta JWT real do Usuário Zero
   (generateLink→verifyOtp, molde `scripts/qa/gen-user-jwt.ts`) e POSTa `video-render` (edge fn).
   *Gate pré-GO (billing inativo):* job vira `failed` com erro honesto `render_engine_unavailable`
   (503 do edge fn ANTES de qualquer débito — saldo intacto). *Gate pós-GO:* 202 `{render_id}` →
   worker `video-bridge` renderiza NATIVO (FR-VS-050) → job `complete` + MP4 baixável em
   `/api/render/:jobId/download`.
6. **Progress**: `curl 127.0.0.1:3211/api/render/<jobId>/progress` (SSE) reflete o estado do job.

## Verification gates (mecânicos)

- `bun run scripts/qa/smoke-studio-host.ts` → todos os gates acima automatizados, zero-cost
  (o smoke NÃO exige o webhook ativo: prova a fronteira 503-sem-débito + auth 401-sem-JWT).
- `npx tsc --noEmit` → 0 erros.

## Recovery path

- **Step 1 falha (porta ocupada):** `STUDIO_HOST_PORT=3212 bun run …` (loopback livre); NUNCA subir
  no 3210 antes da sub-fatia 2c (swap gated com rollback).
- **Step 5 falha com 401:** mint falhou (SB_SECRET_KEY/URL errados) OU JWT expirou entre mint e uso —
  o adapter re-minta 1× automaticamente; persistindo, rodar `bun run scripts/qa/gen-user-jwt.ts
  <email>` isolado para diagnosticar (generateLink vs verifyOtp).
- **Step 5 falha com 503 `render_engine_unavailable`:** ESPERADO pré-GO (billing inativo). Item da
  Fila Sovereign: setar `VIDEO_HYPERFRAMES_WEBHOOK=poll://` (liga cobrança 12 mco/render).
- **Step 5 falha com 402:** saldo mcoCoins do Usuário Zero insuficiente (12 mco) — decisão Sovereign.
- **Render preso em `rendering` >15min:** o job local expira honesto (failed timeout); a linha
  `video_renders` segue o reaper do worker (RUNNING_TIMEOUT_MS → re-claim). Nunca apagar a linha.

## Success signal

Pré-GO: smoke verde (projects+runtime+preview+503-sem-débito+401-sem-JWT). Pós-GO: POST render →
202 → `video_renders` done → MP4 no bucket → download local 200 → Vision-QA confidence high.

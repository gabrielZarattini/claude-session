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

---

## Sub-fatia 2c — Studio SPA pré-buildado + swap do service (EXECUTADA 2026-07-01)

**Achado decisivo:** `@hyperframes/studio` shipa o app **inteiro pré-buildado** em `dist/` (index.html +
assets; React 19 bundlado DENTRO; Apache-2.0 com LICENSE no tarball; telemetria só same-origin
`/api/events`). Não há build próprio na v1 — o host serve esse dist estático.

### Sequence

1. **Carrier isolado**: `packages/video-studio-host-ui/` (`package.json` com só `@hyperframes/studio`)
   + `bun install` DENTRO desse dir. **NUNCA instalar o studio no root do repo** — react@19 hoistado
   quebraria o SPA React 18. *Gate:* `ls node_modules/@hyperframes/studio/dist/index.html`.
2. **Static-serve**: `server.ts` rota `GET *` (registrada por último; jail sob `UI_DIST`; fallback SPA
   p/ index.html; guard exclui `/api|/__hf|/healthz`). *Gate:* `curl /` = index.html; asset JS 200.
3. **Browser-verify loopback**: `agent-browser open "http://127.0.0.1:<porta>/#project/<id>"`
   (⚠️ formato do hash é **`#project/<id>`**, NÃO `#project=<id>` — verificado no bundle) → editor
   renderiza file-tree + preview 9:16 + timeline com as tracks reais + 0 erros console → **Vision QA
   no print** (upload bucket → signed URL → `vision-qa.ts image`) confidence ≥ high.
4. **Swap do service (§B.5)**: reescrever `~/.config/systemd/user/video-studio.service` —
   `WorkingDirectory=<repo>` (bun auto-carrega `.env`) + `ExecStart=bun run
   scripts/video-studio-host/server.ts` + `Environment=STUDIO_HOST_PORT=3210` (mesma porta = mesmo
   vhost `video.mcorch.com`, zero DNS novo). `daemon-reload` + `restart`. *Gate:* `curl
   127.0.0.1:3210/healthz` → `{ok:true,ui:true}` + `/api/projects` lista multi-projeto + browser-verify
   no 3210.

### Recovery (rollback do swap)

O ExecStart vanilla (Fase A) está **comentado dentro do próprio service file**: restaurar as 2 linhas
(ExecStart + WorkingDirectory), `daemon-reload`, `restart` → editor vanilla volta em <10s.
⚠️ Ao matar servidores de teste, matar por PID da PORTA (`lsof -ti :3211`) — `pkill -f server.ts`
mata o processo do service E o próprio shell (aprendido 2026-07-01; systemd Restart=always ressuscita).

### Success signal (2c)

`systemctl --user is-active video-studio.service` = active · 3210 serve UI+API nossos ·
editor abre `#project/mcorch-video` com timeline real · Vision QA high · Export→render pago provado
(fluxo 2a) — **o editor billável é 100% servido por infra MCORCH** (equity; CLI license-None fora do
caminho de serving; resta só o `hyperframes preview` fora de uso e deletável).

---

## Sub-fatia 2b — FR-VS-049: durabilidade Storage↔volume (write-back + materialização)

**Por quê:** as rotas `files/*`/`file-mutations/*` do studio escrevem DIRETO no dir local (§B.2 achado
crítico) — sem backup, a morte do host perde os projetos autorados. v1 single-tenant (§B.4): FS local
segue canônico; Storage = espelho durável best-effort.

### Operator (manual hoje)

Sovereign copiaria o dir do projeto à mão (`tar` + upload). Com 2b o host espelha sozinho.

### Sequence

1. **Bucket**: migration `20260701*_video_studio_projects_bucket.sql` — bucket privado
   `video-studio-projects` (molde `video-studio-assets`: default-deny, sem policies; host escreve via
   service key). *Gate:* migration aplicada (HTTP/CLI output) + `/security-review` ANTES do commit.
2. **Write-back sweep** (`scripts/video-studio-host/sync.ts`): a cada `STUDIO_SYNC_INTERVAL_S` (default
   60s) + no SIGTERM, varre `walkDir` de cada projeto e sobe (upsert) os arquivos com mtime > último
   sync. Exclui `renders/` (outputs reproduzíveis, já têm bucket próprio), `.hf-native-bundle-*` (temp)
   e arquivos >50MB. Chave: `projects/<id>/<relpath>`. *Gate:* mutar arquivo → aguardar sweep → objeto
   listável no bucket via REST.
3. **Materialização** (adapter `resolveProject`): se o dir local NÃO existe mas o prefixo
   `projects/<id>/` existe no bucket → baixa tudo → recria o dir → resolve normal. *Gate:* apagar
   cópia local de um projeto THROWAWAY → `GET /api/projects/<id>` → dir rematerializado byte-igual.
4. **Smoke** `scripts/qa/smoke-studio-sync.ts`: cria projeto throwaway → sweep → verifica bucket →
   apaga local → materializa → compara sha256 → limpa (local + bucket).

### Recovery

- Sweep falha (rede/bucket): best-effort — loga `[sync]` no journal e re-tenta no próximo tick; NUNCA
  bloqueia o editor (FS local é canônico).
- Materialização parcial (download falha no meio): dir é criado só DEPOIS do download completo em
  staging temp + rename atômico; falha → dir ausente (estado limpo) + erro honesto.
- Restaurar manualmente: baixar prefixo `projects/<id>/` do bucket com service key.

### Success signal

Smoke verde (throwaway round-trip sha-igual) + objeto real de `mcorch-video` visível no bucket após
sweep + journal com `[sync] uploaded N files`.

# SOP — Provisionamento da infra host do Video Repurpose (Lei 2)

> **Por que existe:** o motor de repurpose usa infra que vive **fora do container Supabase e fora do build do frontend** — dois workers systemd + um receiver de upload atrás do nginx. Antes desta SOP, esses artefatos existiam só no host (`~/.config/systemd/user/`, `/etc/nginx`), **não versionados** → risco de perda silenciosa num reprovisionamento. Esta SOP + os arquivos em `infra/systemd/` e `infra/nginx/` fecham o alerta "infra host fora do git".
>
> **ORO:** Operator = Sovereign (host root/user `ubuntu`) · Reviewer = Sovereign · Owner = Sovereign (blast radius = disco do host + porta loopback; rail grátis US$ 0).
> **Materialidade (Lei 1):** as 2 units foram capturadas **verbatim** do host (`~/.config/systemd/user/`). O bloco nginx `/api/host-upload` **não pôde ser lido** no host (rodando como `ubuntu`, `/etc/nginx` é permission-denied; `nginx -T` não permitido) → `infra/nginx/host-upload.location.conf` é a **forma REQUERIDA derivada** de `scripts/host-upload-server.ts`; o provisionamento reconcilia contra o bloco vivo.

## Artefatos versionados (fonte da verdade no git)

| Artefato | Repo (versionado) | Host (deployado) |
|---|---|---|
| Worker de segmentação | `scripts/video-repurpose-bridge.ts` | roda via unit abaixo |
| Receiver de upload | `scripts/host-upload-server.ts` | roda via unit abaixo (`127.0.0.1:3220`) |
| Unit — bridge | `infra/systemd/video-repurpose-bridge.service` | `~/.config/systemd/user/video-repurpose-bridge.service` |
| Unit — upload | `infra/systemd/host-upload.service` | `~/.config/systemd/user/host-upload.service` |
| Location nginx | `infra/nginx/host-upload.location.conf` (derivado) | `/etc/nginx/sites-enabled/*login.mcorch.com*` (não-repo-legível) |
| Inbox no disco | — | `<repo>/repurpose-inbox/<uid>/` (gitignored; dados) |

## Operator — quem executa
O Sovereign no host (usuário `ubuntu` para systemd `--user`; root/sudo para o nginx).

## Sequence — ordem (cada passo com critério material)

1. **Instalar as units** (idempotente — os arquivos já existem no host; este passo re-sincroniza a partir do git):
   ```bash
   cp infra/systemd/host-upload.service infra/systemd/video-repurpose-bridge.service ~/.config/systemd/user/
   systemctl --user daemon-reload
   systemctl --user enable --now host-upload.service video-repurpose-bridge.service
   ```
   ✅ sucesso: `systemctl --user is-active host-upload.service video-repurpose-bridge.service` → `active active`.

2. **Reconciliar o nginx** (root): abrir o server block `server_name login.mcorch.com` e garantir que o `location = /api/host-upload` bate com `infra/nginx/host-upload.location.conf` (mesmos `proxy_pass 127.0.0.1:3220`, `proxy_request_buffering off`, `client_max_body_size 100m`, timeouts 300s). Se divergir, **atualizar o git** (Lei 1 — o repo segue a verdade do host) OU aplicar o bloco versionado ao host, e registrar qual venceu.
   ```bash
   sudo nginx -t && sudo systemctl reload nginx
   ```
   ✅ sucesso: `nginx -t` → `syntax is ok / test is successful`.

3. **Inbox no disco**: `mkdir -p <repo>/repurpose-inbox` (o server cria `<uid>/` sob demanda; realpath-contido).

## Verification gates (o operator confirma cada um materialmente)

| Gate | Comando | Esperado |
|---|---|---|
| G1 units ativas | `systemctl --user is-active host-upload.service video-repurpose-bridge.service` | `active` (×2) |
| G2 porta loopback | `curl -s -o /dev/null -w '%{http_code}' -X POST http://127.0.0.1:3220/api/host-upload` | `401` (sem JWT) — prova que sobe e exige auth |
| G3 admin-gate | POST com JWT de user **não-admin** | `403 admin_only` |
| G4 nginx front-door | `curl -s -o /dev/null -w '%{http_code}' -X POST https://login.mcorch.com/api/host-upload` | `401` (chega no server, exige auth) — **não** 404/502 |
| G5 telemetria | `SELECT count(*) FROM infra_health_logs WHERE service='host-upload' AND created_at > now()-interval '1 day'` | ≥1 no primeiro upload real |

## Recovery — falha no passo N
- **Unit em crash-loop** (`Restart=always` + `StartLimitBurst=5/60s`): `journalctl --user -u host-upload.service -n 50` → causa (falta `.env`? bun no PATH?). O unit já fixa `PATH=/home/ubuntu/.bun/bin:…` e carrega `.env` de `../` (o server faz isso). Corrigir e `systemctl --user restart <unit>`.
- **G4 = 502**: o server loopback caiu → G1/G2 primeiro. **G4 = 404**: o `location` não está no server block → passo 2. **G4 = 403 do Cloudflare** (não do server): challenge de IP datacenter → mesmo playbook `docs/processes/wordpress-cf-publish-unblock.md` (Security Level / WAF Skip).
- **Upload trava em chunk grande**: confirmar `proxy_request_buffering off` + `client_max_body_size 100m` no bloco vivo (sem isso, nginx bufferiza e estoura). CF corta >100MB/request → o cliente DEVE fatiar <100MB (já fatia ~80MB).

## Rota de mídia `/api/host-media` (2026-07-13 — master reproduzível na biblioteca)

**Por quê:** o master host-local é `creative_assets` `storage_bucket='local'` — a biblioteca tentava assinar no Supabase Storage → `Object not found` → player quebrado ("o arquivo corrompeu" — não corrompeu; faltava rota de reprodução).

**Desenho:** `host-upload-server` ganhou `GET /api/host-media?key=<uid>/<file>` — mesmos guards do upload (JWT `admin.getUser` + admin-gate `user_roles` + owner-scope `key.startsWith(uid/)` + containment em `INBOX_BASE` + `..` banido) + **streaming com Range** (HTTP 206 → seek). `<video src>` não envia headers → JWT curto da sessão vai como `?token=` (same-origin TLS, admin-only; o `useDisplayUrl` re-resolve antes de expirar; token em access-log do próprio host = aceito e documentado). Cliente: `src/lib/asset-url.ts` branch `bucket==='local'`. `/security-review` **NO FINDINGS** (traversal/auth/cross-tenant/header-injection verificados).

**Apply (ação Sovereign):** `sudo bash scripts/qa/apply-host-media-nginx.sh` (idempotente: backup → insere a location após o bloco host-upload → `nginx -t` → reload).

**Gates:** G6 local `curl -H 'Range: bytes=0-1023' 'http://127.0.0.1:3220/api/host-media?key=<uid>/<file>&token=<jwt>'` → `206` + `Content-Range` correto (provado 2026-07-13 com o EP01 de 1.336.271.927 bytes; seek em 600MB ok; cross-tenant → 400; sem token → 401; não-admin → 403). G7 público (pós-apply): mesmo curl via `https://login.mcorch.com` → 206; biblioteca reproduz o master.

## Success signal (materialmente observável)
Um upload real (admin, via UI `/dashboard/repurpose`) grava `repurpose-inbox/<uid>/<file>.mp4` no disco (`ls -la` com size ≈ o master) **e** o `ingest-external-asset provider=local` registra o `creative_assets bucket=local`, consumível pelo `video-repurpose-run`. Prova no seal 2026-07-13: EP01 1,3 GB → 5 shorts.

**Cross-links:** [[project_video_repurpose_engine]] · `docs/bok/video-repurpose/00-deepsearch-blueprint.md` (OTD-VR-001 yt-dlp datacenter-block) · `docs/processes/build-deploy-materiality.md`.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

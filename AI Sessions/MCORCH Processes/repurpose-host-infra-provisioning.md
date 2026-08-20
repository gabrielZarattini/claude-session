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

## Rota de saúde `/api/host-probe` (2026-07-20 — selo de integridade do master)

> **Emenda Lei 2** — rota NOVA = automação nova ⇒ este SOP precede o código (`scripts/host-upload-server.ts`).

**Por quê (o buraco material que ela fecha):** o master do EP02 subiu corrompido (chunk perdido no append cego),
o `ffprobe` de cabeçalho passava, o wizard deixou selecioná-lo, e **todo corte FFmpeg falhou** com
`Invalid NAL unit size`. O gate de tamanho (`X-Total-Bytes`) impede a REINCIDÊNCIA, mas **não diz nada sobre os
masters já no acervo** — e **tamanho não prova decodabilidade** (chunks reordenados/duplicados dão tamanho
idêntico). Não existe sinal honesto derivável do banco: `file_size_bytes` é `NULL` nas linhas reais e o
`X-Total-Bytes` declarado nunca foi persistido. **O único sinal honesto exige tocar o arquivo no host.**

**Operator:** o próprio Sovereign, pela UI (`/dashboard/repurpose` → badge amarelo "Não verificado" → clique),
ou manualmente por `curl` no loopback. Hoje, antes desta rota, o equivalente manual era:
`ffprobe <file>` + `ffmpeg -ss <t> -i <file> -frames:v 12 -f null -` em 3 pontos, a olho.

**Sequence (o que a rota executa, na ordem — cada passo com critério material):**

| # | Passo | Critério de sucesso |
|---|---|---|
| 1 | Auth: `authenticate()` (JWT `admin.auth.getUser` + admin-gate `user_roles`) | `userId` resolvido; senão `401`/`403` |
| 2 | Chave: `key.startsWith(uid/)`, sem `..`, `resolve(path)` contido em `INBOX_BASE/` | senão `400 bad_key`/`bad_path` |
| 3 | `existsSync` | senão veredito **`missing`** (`404`) |
| 4 | `statSync().size` | `bytes` real do arquivo em disco |
| 5 | `ffprobe -show_entries format=duration,size + streams` (timeout 30s) | exit 0 + `duration > 0`; senão **`corrupt`** |
| 6 | Spot-decode em 3 offsets (20% / 50% / 90% da duração), cada um `ffmpeg -v error -nostats -progress pipe:1 -ss <t> -i <path> -frames:v 12 -f null -` (timeout 60s) | **os 3 limpos** ⇒ **`ok`**; qualquer sujo ⇒ **`corrupt`** |
| 7 | Persistir em `creative_assets.metadata.health` (service-role, filtro `storage_bucket='local' AND storage_key=<key> AND user_id=<uid>`) | linha atualizada; o filtro por `user_id` é **obrigatório** (owner-scoped — não confiar só na chave) |

**Critério de "spot limpo" — os TRÊS, medidos 2026-07-20 (não afrouxar):**

1. `exit === 0`, **e**
2. `stderr` vazio — *exit code sozinho não basta*: a corrupção tipo EP02 produz stderr sujo com exit 0, **e**
3. **`frame=N` do `-progress` com `N > 0`** — *exit+stderr também não bastam*. Prova material: uma cópia do EP02
   truncada a 300 MB devolveu `exit=0 stderr_bytes=0` nos 3 spots e passaria por íntegra; só o contador de frames
   a denunciou (`frame=0` vs `frame=12` no arquivo real). É por isso que o `-progress pipe:1` existe aqui: mantém
   o stderr limpo para o teste (2) enquanto entrega a contagem para o teste (3).

**Anti-injeção:** `Bun.spawn` **sempre com ARRAY de args**, nunca string de shell — o path vem de dado do usuário.

**Verification gates:**

| Gate | Comando | Esperado |
|---|---|---|
| H1 sem JWT | `curl -s -o /dev/null -w '%{http_code}' 'http://127.0.0.1:3220/api/host-probe?key=<uid>/<file>'` | `401` |
| H2 cross-tenant | `?key=<outro-uid>/<file>` com JWT válido | `400 bad_key` |
| H3 traversal | `?key=<uid>/../../etc/passwd` | `400` |
| H4 arquivo ausente | `?key=<uid>/nao-existe.mp4` | `404` + `status:"missing"` |
| H5 master íntegro | `?key=<uid>/EP02_-_MASTER__YouTube_.mp4` | `200` + `status:"ok"` + `spots:[…]` 3× `frames:12` |
| H6 master corrompido | cópia truncada **no scratchpad, nunca um master de produção** | `status:"corrupt"` + o spot culpado identificado |
| H7 persistência | `SELECT metadata->'health' FROM creative_assets WHERE storage_key=…` | `{status, bytes, duration_seconds, checked_at, spots}` |

**Recovery:**
- `status:"corrupt"` ⇒ **não há conserto** do arquivo montado: re-enviar o master pelo wizard (o gate
  `X-Total-Bytes` agora recusa a montagem divergente antes de publicá-la). O selo vermelho **bloqueia a seleção**
  desse master no wizard — este é exatamente o gate que faltava e que deixou o Sovereign reusar o EP02 quebrado.
- `status:"missing"` ⇒ o registro `creative_assets` está órfão: excluir pela galeria (`/dashboard/spaces/assets`) e re-enviar.
- Probe estourando timeout (arquivo enorme em disco lento) ⇒ veredito permanece o anterior; a UI cai para
  **amarelo "Não verificado"** (fail-soft — nunca pinta de verde o que não mediu).

**Frescor (por que verde não é eterno):** `checked_at` com mais de **7 dias**, ou `health.bytes` divergente de
`file_size_bytes` (quando ambos existirem), rebaixa o selo a amarelo. Master que **não** seja `bucket='local'`
também é amarelo — não há host para sondar, e dizer "íntegro" ali seria fabricar prova (Lei 1).

**nginx (ação Sovereign):** o bloco `location = /api/host-probe` está versionado em
`infra/nginx/host-upload.location.conf`. **Não editar `/etc/nginx` a partir do agente** — aplicar é ação do
Sovereign (`sudo nginx -t && sudo systemctl reload nginx`), mesmo playbook do passo 2.

> ⚠️ **ENQUANTO O BLOCO NÃO FOR APLICADO, O BADGE NÃO VERIFICA NADA.** O vhost vivo
> (`/etc/nginx/sites-enabled/www.mcorch.com.conf`) tem `location = /api/host-upload` e `= /api/host-media`,
> mas **não** `= /api/host-probe`; o `location /` casa e devolve o `index.html` da SPA com **HTTP 200**.
> Medido 2026-07-20: `curl -w '%{http_code} %{content_type}' https://login.mcorch.com/api/host-probe?key=x/y.mp4`
> → `200 text/html` (3649 bytes). Por isso o cliente **valida a FORMA do veredito** (`status ∈ ok|corrupt|missing`)
> antes de acreditar nele: sem essa checagem, um 200-com-HTML virava `{}` → `status` undefined → a UI acusava
> **"arquivo corrompido"** sobre um master saudável — o inverso exato do bug que esta rota existe para corrigir.
> Gate de aceite pós-apply: o mesmo `curl` (com JWT admin) precisa devolver `content_type: application/json`
> e um `status` dos três; qualquer `text/html` = bloco não aplicado, e a UI dirá "verificação não disponível"
> em vez de inventar um veredito.

**Success signal:** um master real devolve `{"status":"ok"}` com 3 spots `frames:12`, o badge vira verde
"Arquivo íntegro" no wizard, e `metadata.health` carrega o veredito datado.

## Success signal (materialmente observável)
Um upload real (admin, via UI `/dashboard/repurpose`) grava `repurpose-inbox/<uid>/<file>.mp4` no disco (`ls -la` com size ≈ o master) **e** o `ingest-external-asset provider=local` registra o `creative_assets bucket=local`, consumível pelo `video-repurpose-run`. Prova no seal 2026-07-13: EP01 1,3 GB → 5 shorts.

**Cross-links:** [[project_video_repurpose_engine]] · `docs/bok/video-repurpose/00-deepsearch-blueprint.md` (OTD-VR-001 yt-dlp datacenter-block) · `docs/processes/build-deploy-materiality.md`.

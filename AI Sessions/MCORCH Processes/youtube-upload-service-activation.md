# SOP — Ativação do `youtube-upload.service` (YouTube Track B — fábrica de upload)

**Status:** ACTIVE · v1.0 · 2026-07-20
**Survival Laws:** Lei 1 (Materialidade) + Lei 2 (Processo Antecipado) + Lei 4 (ORO).
**BoK SSOT:** `docs/bok/youtube-studio/13-amendment-upload-factory.md` (FR-YT-026/027/028).
**Molde:** `docs/processes/video-studio-editor-deploy-and-provision.md` · irmãos vivos `video-bridge.service`,
`crm-media-bridge.service`, `provenance-bridge.service`.

---

## Estado material verificado (2026-07-20)

Levantado nesta sessão. **Nada aqui é presumido.**

```
$ systemctl --user is-enabled youtube-upload.service
not-found
$ systemctl --user is-active youtube-upload.service
inactive
$ ls -la ~/.config/systemd/user/ | grep youtube
(nenhuma linha)
```

O unit existe **apenas no repositório** (`scripts/systemd/youtube-upload.service`) e **nunca foi instalado**
em `~/.config/systemd/user/`. Isso é **deliberado**, não esquecimento — a primeira linha do próprio arquivo diz:

> `# NÃO HABILITADO — nasce desabilitado (gate Sovereign, molde crm-media-bridge/provenance-bridge).`

**Motivo do gate:** o worker faz `videos.insert` **real** no canal YouTube do Sovereign. Habilitá-lo com a
fila já populada publica vídeo (ainda que `private`) e **queima quota diária irreversível** — 1600 unidades
por upload de uma quota default de 10.000 (`13-amendment-upload-factory.md:43`), ou seja **~6 uploads/dia**.
Não há "desfazer" de quota.

**Fatos adjacentes já confirmados materialmente nesta sessão:**

| Fato | Prova |
|------|-------|
| O worker existe e é o alvo do unit | `scripts/youtube-upload-bridge.ts` (17.994 bytes, 2026-07-19 16:40) |
| O master do EP02 **já está no host** | `repurpose-inbox/ada39fae-…/EP02_-_MASTER__YouTube_.mp4`, **529.015.996 bytes** |
| O worker (uid `ubuntu`) **consegue ler** o master do inbox do User 0 | `head -c 16` do arquivo devolveu magic bytes `ftypisom` rodando como `uid=1001(ubuntu)`; `ubuntu` pertence ao grupo `gcrUX` (1011) |
| Os irmãos do mesmo molde estão vivos | `systemctl --user is-enabled video-repurpose-bridge.service crm-media-bridge.service` → `enabled` / `enabled` |

---

## ORO

| Papel | Quem |
|-------|------|
| **Operator** | **Sovereign (Gabriel)** — a ativação publica no canal dele e consome quota dele. O Agent escreve o SOP e verifica gates; **não** habilita o serviço. |
| **Reviewer** | Sovereign (confirma cada pré-condição antes do `enable`) |
| **Owner** | Sovereign — blast radius = canal YouTube em produção (vídeo publicado + quota diária irrecuperável + risco de strike se o conteúdo violar política) |

---

## Arquitetura material

```
UI  /dashboard/youtube/studio-yt → YouTubeUploadPanel  (useEnqueueUpload)
      │ INSERT RLS-owner em youtube_uploads (state='queued', sem video_id)
      ▼
   youtube_uploads  ── begin_youtube_upload(job) ──▶  youtube-upload.service
      │  (RPCs service-role-only)                     scripts/youtube-upload-bridge.ts
      │                                                  │ lê master de repurpose-inbox/<uid>/
      │                                                  │ resumable videos.insert (chunks de 8 MB)
      ◀── finalize_youtube_upload(state,video_id) ───────┘ extras force-ssl fail-soft
```

- **Sem edge function nova** (o projeto está no cap de ~99 funções). O worker é host **porque** uma Edge
  Function não streama 1,3 GB e não alcança o inbox do host.
- **Sem ledger de mcoCoins** — o custo é a **quota do canal**, não a carteira.
- **Token resolvido server-side** de `decrypted_social_accounts` pelo `user_id` **do job** (dono), nunca do
  body (API Tenancy Model).
- **`privacyStatus` default `private`** — nunca público por omissão.
- **Sem policy de UPDATE para `authenticated`**: só o worker (service-role) muda `state`/`progress`/`video_id`.

---

## (a) Pré-condições que o Sovereign precisa confirmar ANTES

**Não habilite nada até as 6 estarem verdes.** Cada uma tem verificação material.

| # | Pré-condição | Como confirmar (material) | Se falhar |
|---|--------------|---------------------------|-----------|
| **P1** | **Migration `youtube_uploads` viva em produção** | `select to_regclass('public.youtube_uploads') is not null as tbl;` **e** os 2 RPCs existem: `select count(*) from pg_proc where proname in ('begin_youtube_upload','finalize_youtube_upload');` → `2`. O `HANDOFF.md` (Record 2026-07-19/20) registra `tbl=1 rpcs=2 policies=3` — **re-confirme**, não confie no texto. | Aplicar via `scripts/qa/apply-youtube-uploads-migration.sh` (gate Sovereign) |
| **P2** | **Canal YouTube conectado** para o User 0 | `select platform, is_active from social_accounts where platform='youtube';` → 1 linha `is_active=true`. Na UI: `/dashboard/youtube/studio-yt` mostra o título do canal. | Conectar em `/dashboard/social` |
| **P3** | **Escopo de upload presente** | `scopes` da linha do YouTube contém **`https://www.googleapis.com/auth/youtube`**. Sem ele o worker devolve `youtube_scope_missing` e o job vira `failed` sem tentar. Opcional para extras: `…/auth/youtube.force-ssl` (thumbnail/legenda) — sem ele os extras viram `warning`, o vídeo sobe igual. | Reconectar com o escopo (`useYouTubeUploadCapability().needsReconnect` acende o CTA na UI) |
| **P4** | **Estado de verificação do app Google (verify / CASA)** — **este é o gate duro** | Console do Google Cloud → OAuth consent screen do app: ou o app está **verificado**, ou o Sovereign está listado como **test user** do app não-verificado. `videos.insert` exige um dos dois (`13-amendment-upload-factory.md:44`). No modo test-user os vídeos ficam travados em `private` e há limites. | **Pare aqui.** Não é contornável por código — é submissão ao Google. Habilitar o serviço sem isso só produz `failed` com 401/403. |
| **P5** | **Quota diária disponível** | Console do Google Cloud → APIs e serviços → YouTube Data API v3 → Quotas: unidades restantes hoje. **1600 por upload**, default 10.000/dia. | Aguardar o reset diário. Não habilite com a fila cheia e a quota curta — os jobs excedentes viram `failed` com `youtube_quota_exceeded`. |
| **P6** | **Master presente e legível no inbox do host** | `ls -la repurpose-inbox/<uid>/` mostra o arquivo, e o `source_key` do job casa `<uid>/<arquivo>` (o CHECK `youtube_uploads_source_owned` já força o prefixo). O master do EP02 **está lá** (529 MB — verificado). | Subir pelo assistente de upload do host (`host-upload.service`) antes de enfileirar |

> **Ordem recomendada de conferência:** P4 primeiro (é o único que pode levar dias), depois P1→P3, P5, P6.

---

## (b) Sequence — instalação, habilitação e start

Comandos exatos. Rodar **como o mesmo usuário dos irmãos** (`ubuntu`, cujos units vivem em
`/home/ubuntu/.config/systemd/user/`).

> 🚨 **`--once` NÃO é um modo dry-run — leia antes do passo 1.** Ele **drena a fila**
> (`scripts/youtube-upload-bridge.ts:363-365`): com jobs em `queued` ele **publica vídeo de verdade e queima
> quota**, antes de P4/P5 terem sido conferidas — exatamente a ordem que este SOP existe para impedir. O ensaio
> do passo 1 só é "a seco" **porque a fila está vazia**; por isso o passo 0 é uma pré-condição verificável, não
> uma observação de rodapé.

| # | Passo | Comando | Critério de sucesso material |
|---|-------|---------|------------------------------|
| **0** | **⚠️ PROVAR QUE A FILA ESTÁ VAZIA — obrigatório antes do passo 1** | `select count(*) as queued from youtube_uploads where state = 'queued';` | **Exatamente `0`.** Se for `> 0`, **PARE** (ver aviso acima). |
| 1 | **Ensaio a seco — ANTES de instalar o unit** (só com o passo 0 = 0) | `cd /home/gcrUX/htdocs/constellation-orchestra && bun run scripts/youtube-upload-bridge.ts --once` | Imprime `drained 0 upload(s)` e sai com código 0. Isso prova env (`SUPABASE_URL`/`SB_SECRET_KEY` do `.env`), conectividade e permissão de RPC **sem publicar nada**. |
| 2 | Instalar o unit | `cp scripts/systemd/youtube-upload.service ~/.config/systemd/user/` | `ls -la ~/.config/systemd/user/youtube-upload.service` retorna a linha |
| 3 | Recarregar o systemd | `systemctl --user daemon-reload` | sem erro |
| 4 | **Habilitar + iniciar** | `systemctl --user enable --now youtube-upload.service` | `systemctl --user is-enabled youtube-upload.service` → `enabled` (era `not-found`) |
| 5 | Conferir estado | `systemctl --user status youtube-upload.service` | `Active: active (running)` **e** o log anuncia `📺 youtube-upload-bridge running — polling youtube_uploads (queued)...` |

> **Persistência entre reboots — VERIFICADO (não presumido).** Units `--user` só sobem sem sessão aberta se o
> *lingering* estiver ligado. Confirmado materialmente nesta sessão:
>
> ```
> $ loginctl show-user ubuntu --property=Linger
> Linger=yes
> ```
>
> Logo, uma vez `enabled`, o serviço **sobe sozinho no boot** — mesmo regime dos irmãos já vivos
> (`video-repurpose-bridge`, `crm-media-bridge`, ambos `enabled`). Re-confirme se o host for reprovisionado.

---

## (c) Verification gates (Lei 1 — nenhum "ativado" sem TODOS verdes)

| Gate | Comando | PASS |
|------|---------|------|
| **G1 — unit instalado** | `systemctl --user is-enabled youtube-upload.service` | `enabled` |
| **G2 — processo vivo** | `systemctl --user is-active youtube-upload.service` | `active` |
| **G3 — worker anunciou o start** | `journalctl --user -u youtube-upload.service -n 30 --no-pager` | contém `polling youtube_uploads (queued)` |
| **G4 — telemetria no banco** (o gate que prova que ele **fala com o Supabase**, não só que o processo subiu) | `select status, event, created_at from infra_health_logs where service='youtube-upload' order by created_at desc limit 5;` | linha `healthy` / `worker_started` com timestamp **posterior** ao `enable` |
| **G5 — consome a fila** | enfileirar 1 job pela UI (`/dashboard/youtube/studio-yt` → painel de upload), `privacyStatus='private'` | `youtube_uploads.state` transita `queued → running` (com `progress` subindo) `→ done`, e `video_id` fica preenchido |
| **G6 — vídeo existe de verdade** | abrir `https://youtu.be/<video_id>` logado no canal | vídeo presente, **privado**, com título/descrição do job |

> **G3 sozinho não prova nada útil.** Um worker com credencial errada sobe, imprime a linha de start e falha
> em silêncio no primeiro ciclo. **G4 é o gate mínimo honesto**; G5/G6 são o gate de valor.

---

## (d) Como parar e reverter

Reversão limpa, em ordem crescente de agressividade:

```bash
# 1. Pausa (mantém instalado; volta com `start`). A fila apenas acumula em 'queued'.
systemctl --user stop youtube-upload.service

# 2. Desabilitar (não sobe mais no boot) — volta ao gate Sovereign.
systemctl --user disable --now youtube-upload.service

# 3. Remoção completa: volta EXATAMENTE ao estado de hoje (is-enabled → not-found).
rm ~/.config/systemd/user/youtube-upload.service
systemctl --user daemon-reload
systemctl --user is-enabled youtube-upload.service   # esperado: not-found
```

**O que a reversão NÃO desfaz:**

- **Vídeos já publicados** — parar o worker não remove nada do YouTube. Excluir é ação manual no
  YouTube Studio (ou pela operação `videos.delete` do painel, que exige `force-ssl`).
- **Quota consumida** — irrecuperável até o reset diário.
- **Jobs em `running` no momento do stop** — ficam pendurados. O worker **se auto-cura**: no próximo start,
  o `drainOnce` devolve para `queued` qualquer `running` parado há mais de **60 minutos**
  (`RUNNING_TIMEOUT_MS`). Antes desses 60 min, o job fica preso — é comportamento esperado, não bug.
  Um upload retomado **não reenvia do zero**: o session URI é retomado via `Range: bytes=*/<size>`.

**Efeito colateral de uma re-fila:** um job devolvido a `queued` que **já havia criado o vídeo** pode gerar
um segundo vídeo se o session URI tiver expirado do lado do Google. Antes de re-enfileirar manualmente,
**confira no YouTube Studio se o vídeo já existe.**

---

## (e) O que observar nas primeiras horas

| Janela | O que olhar | Sinal saudável | Sinal de alarme → ação |
|--------|-------------|----------------|------------------------|
| **Primeiros 5 min** | `journalctl --user -u youtube-upload.service -f` | ciclos de poll silenciosos (poll a cada 5 s, sem ruído com fila vazia) | `poll cycle error` repetido → credencial/rede; **stop** e investigar antes de enfileirar |
| **Primeiro upload** | `progress` da linha em `youtube_uploads` | sobe monotonicamente até 100 | travado no mesmo `progress` por > 10 min → rede ou master corrompido; conferir tamanho do arquivo vs `Content-Range` |
| **Primeira hora** | `select status, event, count(*) from infra_health_logs where service='youtube-upload' and created_at > now() - interval '1 hour' group by 1,2;` | `healthy/worker_started` = 1, `error/upload_failed` = 0 | qualquer `upload_failed` → ler `youtube_uploads.error`; os códigos são estruturados, não crashes: `youtube_not_connected`, `youtube_scope_missing`, `youtube_token_unavailable`, `youtube_quota_exceeded`, `source_not_found`, `insert_init_failed:<status>` |
| **Primeiras 24 h** | quota no console Google | consumo = 1600 × nº de uploads | consumo maior que o esperado ⇒ **retry loop**; `stop` imediato (a quota é o recurso irrecuperável) |
| **Primeiras 24 h** | `warnings` dos jobs `done` | vazio, ou `thumbnail_scope_missing` se `force-ssl` não foi concedido | warnings são **fail-soft por design** — o vídeo já existe; não re-enfileire por causa de warning |
| **Após reboot** | `systemctl --user is-active youtube-upload.service` | `active` | `inactive` ⇒ lingering desligado; ligar ou aceitar start manual |

**Regra de ouro das primeiras horas:** enfileire **um** job, deixe-o chegar a `done`, verifique G6, e só então
enfileire o segundo. A quota não perdoa um loop.

---

## Recovery path

| Sintoma | Causa provável | Fix |
|---------|----------------|-----|
| `youtube_scope_missing` | P3 não satisfeita | reconectar o canal com o escopo `…/auth/youtube`; o job antigo fica `failed` — re-enfileirar |
| `youtube_not_connected` / `youtube_token_unavailable` | linha ausente/inativa em `social_accounts`, ou refresh falhou | reconectar em `/dashboard/social`; conferir `is_active` (não o TTL do token) |
| `youtube_quota_exceeded` | P5 estourada | aguardar o reset diário; re-enfileirar no dia seguinte. **Não** aumente a concorrência do worker |
| `source_not_found` | master ausente ou `source_key` fora de `<uid>/…` | subir o master ao inbox do host; conferir o prefixo (o CHECK `youtube_uploads_source_owned` já força) |
| Job preso em `running` | worker morreu mid-upload | esperar 60 min (auto-reap para `queued`) **ou** `systemctl --user restart` e aguardar; conferir no Studio se o vídeo já existe antes de re-enfileirar |
| Nada acontece, fila cheia, serviço `active` | worker de código velho em memória | `systemctl --user restart youtube-upload.service` — o worker **fica stale até restart** (gotcha conhecido no `video-bridge`, mesmo molde) |
| Vídeo subiu público sem querer | `privacyStatus` errado no job | mudar no YouTube Studio; o default do rail é `private` — investigar quem passou outro valor |

---

## Success signal

**G1–G6 verdes** + o Sovereign vê o vídeo **privado** no canal com os metadados do job + `infra_health_logs`
com `service='youtube-upload'` sem nenhuma linha `error` na primeira hora + quota consumida **exatamente**
1600 × nº de uploads.

Fechamento: registrar no `HANDOFF.md` a data da ativação, o `video_id` do primeiro upload e o gate que o
provou. Isso encerra a pendência "habilitar `youtube-upload.service`" que hoje aparece como item Sovereign no
Record de 2026-07-19/20.

---

## Anti-patterns proibidos

- ❌ `systemctl --user enable --now` **antes** de P4 (verify/CASA). O worker vai só produzir `failed` com 401/403.
- ❌ Habilitar com a fila já populada. Enfileire **depois** dos gates, um job por vez no primeiro dia.
- ❌ Rodar `--once` como se fosse dry-run **sem antes provar que a fila está vazia** (passo 0). Com a fila
  populada, `--once` publica e queima quota — o "ensaio" vira a própria ação que o SOP tenta gatear.
- ❌ Declarar "worker vivo" com base em `is-active`. Um processo vivo que não fala com o Supabase é um
  falso-sucesso — **G4 é o gate mínimo**.
- ❌ Re-enfileirar um job `failed` sem antes ler `youtube_uploads.error`. Os códigos são estruturados de
  propósito; retry cego queima quota.
- ❌ Editar o unit para colocar segredo dentro. O worker carrega `SUPABASE_URL`/`SB_SECRET_KEY` do `.env`
  por design (`youtube-upload-bridge.ts:27-38`); o unit é livre de segredos e deve continuar assim.
- ❌ Rodar mais de uma instância do worker. O claim é atômico (`begin_youtube_upload` com guard
  `state='queued'`), mas concorrência multiplica o risco de quota sem ganho — o gargalo é a rede, não a CPU.

---

## Connection to Survival Laws

**Lei 1:** o serviço só está "ativo" quando a telemetria no banco e o vídeo no canal provam — nunca o
`systemctl status` sozinho. **Lei 2:** este SOP existe **antes** da ativação, com gates de materialidade por
passo, exatamente porque o recurso queimado (quota, vídeo publicado) é irreversível. **Lei 4:** Operator =
Sovereign; o Agent prepara e verifica, não habilita.

## Cross-references

| Recurso | Caminho |
|---------|---------|
| Unit (no repo, não instalado) | `scripts/systemd/youtube-upload.service` |
| Worker | `scripts/youtube-upload-bridge.ts` |
| Migration | `supabase/migrations/20260719170000_youtube_uploads.sql` |
| Aplicador da migration | `scripts/qa/apply-youtube-uploads-migration.sh` |
| BoK SSOT (FR-YT-026/027/028) | `docs/bok/youtube-studio/13-amendment-upload-factory.md` |
| Hooks da UI | `src/hooks/useYouTubeUpload.ts` |
| Painel da UI | `src/components/youtube/YouTubeUploadPanel.tsx` (em `/dashboard/youtube/studio-yt`) |
| Precedente do mesmo molde | `scripts/video-bridge.ts` · `docs/processes/video-repurpose-worker.md` |
| Rotação das credenciais envolvidas | `docs/processes/credential-rotation-runbook.md` |

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

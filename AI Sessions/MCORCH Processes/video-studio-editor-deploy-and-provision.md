# SOP — HyperFrames Video Studio editor: deploy, provision & operate

> **Lei 2 (Processo Antecipado).** Como tornar o editor de vídeo HyperFrames (Fatia VS-UI) funcional E2E:
> servidor preview (systemd host), acesso público (iframe/vhost + SSO), e o caminho de render. BoK:
> `docs/bok/video-studio/` (9/9 selada) + SDD §VS-UI Amendment v0.4. Realiza OTD-VS-005 (C) / OTD-VS-015.

Relacionado: [[project_video_studio]] · `nginx/video.mcorch.com.conf` · `~/.config/systemd/user/video-studio.service`
· precedente direto: `docs/processes/canvas-design-deploy-and-provision.md` (mesmo padrão módulo-container).

---

## ORO

| Papel | Quem |
|-------|------|
| **Operator** | MCORCH Master Execution Agent + Sovereign (passos sudo de cert/symlink) |
| **Reviewer** | Sovereign + `/security-review` (antes de expor o render bridge Fase B) |
| **Owner** | Sovereign — blast radius = preview server sem auth nativa (mitigado pelo SSO gate) + carteira (render Fase B) |

---

## Arquitetura material (verificada 2026-06-24)

```
SPA (/dashboard/canvas/video, React 18) ──iframe──▶ video.mcorch.com (CF orange + SSL Full + SSO gate)
   nginx video.mcorch.com.conf ──proxy 127.0.0.1:3210 (SSE)──▶ video-studio.service (hyperframes preview, node v22)
   render/export Fase A = engine local CLI (Chrome+FFmpeg no host). Fase B = McorchAdapter → video-render.
```

Single-tenant Usuário Zero (OTD-VA-011). O preview server **não tem auth nativa** → o SSO gate do vhost é
o que o restringe à sessão MCORCH logada.

---

## Sequence (deploy do zero)

| # | Passo | Comando / artefato | Critério de sucesso material |
|---|-------|--------------------|------------------------------|
| 1 | Binário global | `bun add -g hyperframes@0.7.5` | `/home/ubuntu/.bun/bin/hyperframes` existe; `node cli.js --version` → `0.7.5` (node **v22**, não v18) |
| 2 | Projeto-semente 9:16 | `hyperframes init mcorch-demo --example warm-grain --resolution portrait --non-interactive --skip-transcribe --skip-skills` em `/home/ubuntu/.mcorch/video-studio/projects/` | `meta.json` + `index.html` + `compositions/*.html` presentes |
| 3 | Serviço systemd | `~/.config/systemd/user/video-studio.service` (ExecStart = **node v22 explícito** + `cli.js preview <projeto> --port 3210 --no-open`) → `systemctl --user enable --now` | `Active: active (running)`; `curl 127.0.0.1:3210/` → 200 `<title>HyperFrames Studio</title>`; `/api/projects` → 200 com o projeto |
| 4 | vhost (Agent escreve) | `nginx/video.mcorch.com.conf` (espelha `design.mcorch.com`: SSO `auth_request` + proxy 3210 + `proxy_buffering off`) | arquivo no repo |
| 5 | **Cert origem (Sovereign, sudo)** | `sudo openssl req -x509 -newkey rsa:2048 -nodes -days 3650 -keyout /etc/nginx/ssl-certificates/video.mcorch.com.key -out /etc/nginx/ssl-certificates/video.mcorch.com.crt -subj "/CN=video.mcorch.com"` | os 2 arquivos existem |
| 6 | **Symlink + reload (Sovereign, sudo)** | `sudo ln -s /home/gcrUX/htdocs/constellation-orchestra/nginx/video.mcorch.com.conf /etc/nginx/sites-enabled/ && sudo nginx -t && sudo systemctl reload nginx` | `nginx -t` OK; reload sem erro |
| 7 | DNS (Sovereign) | A `video.mcorch.com` → IP, CF orange | ✅ já feito |
| 8 | Frontend | `/dashboard/canvas/video` (VideoStudioEditorPage iframe) — rota ANTES de `canvas/:id` | chunk no `dist/` referencia `video.mcorch.com`; nav "Vídeo" sob Canvas Studio |

---

## Verification gates

1. `systemctl --user is-active video-studio.service` → `active`.
2. `curl -s 127.0.0.1:3210/api/projects` → 200 com ≥1 projeto.
3. Pós-cert+symlink: abrir `https://video.mcorch.com` logado → editor carrega (NÃO testar por `curl` do datacenter: CF challenge devolve 403 — usar browser real ou o iframe logado).
4. `/dashboard/canvas/video` no SPA → iframe carrega o editor.

---

## Recovery

| Falha | Causa provável | Fix |
|-------|----------------|-----|
| serviço crash-loop "styleText"/"v18" | systemd pegou `/usr/bin/node` v18 | ExecStart com node v22 EXPLÍCITO (`/home/ubuntu/.local/bin/node …cli.js`) — `env node` do shebang resolve v18 sob systemd |
| "No composition found" | `preview` aponta p/ dir SEM `index.html` (dir-pai) | apontar p/ um **projeto** (tem `index.html`), não o root multi-projeto |
| `video.mcorch.com` → 403 no browser | CF challenge por IP de datacenter | Skip rule CF p/ `http.host eq "video.mcorch.com"` + desligar **"Nível de Segurança"** (ver `wordpress-cf-publish-unblock.md`) |
| 502 atrás do vhost | serviço caiu / porta errada | `systemctl --user restart video-studio.service`; confirmar `:3210` LISTEN |
| `pkill -f hyperframes` mata o próprio shell | o padrão casa a linha de comando do shell | matar por pid da porta (`ss -ltnp \| grep :3210`), nunca `pkill -f hyperframes` |

---

## Success signal

`https://video.mcorch.com` (logado) abre o editor NLE HyperFrames com o projeto 9:16; o Sovereign edita
cenas/camadas/overlays-alpha/efeitos/transições e dá preview ao vivo. **Fase B** (próxima): botão Export →
`McorchAdapter.startRender` → `video-render` (motor MCORCH + mcoCoins prepaid) em vez do engine local.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

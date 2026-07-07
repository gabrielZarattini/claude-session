# SOP — Canvas Design (open-design) deploy, provision & operate

> **Lei 2 (Processo Antecipado).** Como tornar o módulo Canvas Design (sidecar open-design) funcional
> E2E: worker supervisor, provisionamento de provider (BYOK), acesso público (iframe/vhost) e o portão
> LGPD. BoK: `docs/bok/canvas-design/` (9/9 selada). Origem: validação E2E 2026-06-21 que achou o módulo
> scaffolded mas NÃO funcional (worker morto + iframe loopback + provider não configurado).

Relacionado: [[canvas-design-initiative]] · `nginx/design.mcorch.com.conf` · `scripts/design-bridge.ts`.

---

## ORO

| Papel | Quem |
|-------|------|
| **Operator** | MCORCH Master Execution Agent + Sovereign (passos de DNS/cert) |
| **Reviewer** | Sovereign + `/security-review` (antes de expor publicamente) |
| **Owner** | Sovereign — blast radius = credenciais BYOK em arquivo no container + dados de design (LGPD) |

---

## Arquitetura material (verificada 2026-06-21)

```
Browser do user (login.mcorch.com, https)
   │  iframe  →  https://design.mcorch.com  (vhost CF→origin :7456)   ← INTERATIVO (Sovereign-gated: DNS+cert)
   ▼
open-design daemon (container `open-design`, 127.0.0.1:7456, Up healthy)
   ▲  docker exec `od media generate` (CLIENTE FINO → fala HTTP com o daemon)
   │
design-bridge worker (systemd --user `design-bridge.service`)  ← HEADLESS, FUNCIONAL
   ▲  poll/claim
design_jobs (Supabase)  →  complete + design_artifact_refs + nó `design_artifact` na malha
```

**Duas superfícies, dois estados:**
- **Headless (worker → job → asset → mesh):** ✅ FUNCIONAL (provado 2026-06-21, imagem real 1.27MB via OpenRouter).
- **Interativo (iframe do editor):** ⚠️ precisa do vhost público (DNS+cert = ação Sovereign).

---

## ⚠️ OTD-003 REVISADA — isolamento per-user NÃO vale neste deploy (achado material)

A SDD (OTD-003) assumiu que o `od` respeita `OD_MEDIA_CONFIG_DIR` por invocação → BYOK isolado por tenant.
**Falso neste container:** `od media generate` é um **cliente fino** que fala HTTP com o **daemon compartilhado**;
o `-e OD_MEDIA_CONFIG_DIR` vai pro processo-cliente, NÃO pro daemon. O daemon resolve provider do seu
config **global** `/app/.od/media-config.json` (formato `{"providers":{"<id>":{"apiKey":"…"}}}`).
**Consequência:** hoje o Canvas Design é **single-tenant** (uma config de provider compartilhada). Para
multi-tenant real, escolher uma das vias (decisão de engenharia, antes de GA com 2º tenant):
- (a) daemon **per-job** (worker dá spawn de um `od` daemon efêmero com o `OD_DATA_DIR`/config do user) — caro;
- (b) `od media generate` **stateless** que não dependa do daemon compartilhado;
- (c) instância open-design **por tenant** (container por user) — não escala.

---

## Operator — Sequence (com critério material por step)

1. **Worker supervisor.** `~/.config/systemd/user/design-bridge.service` (bun, `Restart=always`, `enable --now`).
   **Sucesso:** `systemctl --user is-active design-bridge.service` = `active`; journal "polling design_jobs".
2. **Provider provisioning (BYOK, single-tenant hoje).** Escrever o config GLOBAL do daemon:
   ```bash
   docker exec -e ODKEY="<openrouter_key>" open-design sh -c \
     'mkdir -p /app/.od && printf "{\"providers\":{\"openrouter\":{\"apiKey\":\"%s\"}}}" "$ODKEY" > /app/.od/media-config.json'
   ```
   (chave do `decrypted_user_api_keys`; providers suportados p/ imagem: `openrouter`, `nanobanana`(google),
   `replicate`, `fal`… ver `media-models.ts`). **Sucesso:** job de imagem real `usedStubFallback:false` + `size` >> 67 (stub).
3. **E2E job (headless).** INSERT em `design_jobs` (`kind=generate`, `od_project_id` VÁLIDO — existe no daemon,
   `params.surface/model`). O worker claima → gera → copia p/ `public/canvas-design/` → `design_artifact_refs`
   + nó `design_artifact` na malha → `status=complete`. **Sucesso:** arquivo PNG/MP4 real no host + nó na malha + `render_url`.
4. **Acesso interativo (Sovereign-gated).** Provisionar `design.mcorch.com` (runbook no topo de `nginx/design.mcorch.com.conf`:
   DNS CF + cert self-signed + Full + WAF skip + symlink + reload). Depois trocar o iframe em
   `src/pages/CanvasDesignPage.tsx` p/ `https://design.mcorch.com` + rebuild. **Sucesso:** editor carrega no
   `/dashboard/canvas/design` logado (sem mixed-content; sem X-Frame-Options bloqueando — confirmado embeddable).
5. **Hardening antes de expor.** `OD_API_TOKEN` forte + `OD_ALLOWED_ORIGINS=https://login.mcorch.com` no env do container.

---

## Verification gates

| Gate | Evidência |
|------|-----------|
| G1 worker ativo | `systemctl --user is-active` = active + journal polling |
| G2 provider real | job `usedStubFallback:false`, `size` real (não 67 bytes) |
| G3 E2E headless | arquivo no host (`ls public/canvas-design/<name>`) + nó `design_artifact` na malha + `design_artifact_refs.mesh_node_id` |
| G4 iframe (Sovereign) | editor renderiza logado, sem mixed-content / X-Frame block |

---

## Recovery path

- **Worker morto:** `systemctl --user restart design-bridge.service` (era esse o estado em 2026-06-21 — 1 job preso 28 dias).
- **Job stub (`usedStubFallback:true`, "no API key"):** config global ausente/errado-schema (precisa do wrapper `providers`)
  OU `OD_MEDIA_ALLOW_STUBS=1` mascarando — corrigir `/app/.od/media-config.json` (step 2) e re-inserir o job.
- **Job 404 "project not found":** `od_project_id` não existe no daemon — usar um projeto válido (`/app/.od/projects/<id>`).
- **iframe em branco/bloqueado:** mixed-content (http em página https) → exige o vhost https; ou WAF challenge da CF → WAF skip.

## Success signal

Job inserido em `design_jobs` → asset real (não stub) em `public/canvas-design/` + nó `design_artifact` na malha,
com o worker sob systemd sobrevivendo a reboot. Editor interativo acessível logado quando o vhost estiver no ar.

---

## ⛔ Launch blocker (OTD-008 / FMEA-007 RPN 240) — LGPD/GDPR

GA do Canvas Design é **gated** numa extensão do `delete-account` para purgar o `OD_DATA_DIR` +
`OD_MEDIA_CONFIG_DIR` (+ a config global de provider, agora que ela carrega a chave BYOK do user) + um
teste de verificação de erasure. NÃO marcar Canvas Design como GA antes disso.

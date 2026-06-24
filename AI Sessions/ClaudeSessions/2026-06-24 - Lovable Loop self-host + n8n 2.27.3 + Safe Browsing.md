---
type: session
date: 2026-06-24
tags:
  - project/agente-lovable-browser
  - infra/n8n
  - infra/cloudflare
  - automation
  - ops
session_id: cowork-2026-06-24-selfhost-migration
---

# Session — Lovable Loop: migração self-host + update n8n + Safe Browsing + roadmap na memória

**Date:** 2026-06-24 | **Tool:** Cowork (desktop) | **Hub:** [[Agente Lovable Browser]] | continua [[2026-06-23 - Lovable Loop (Driver+Critico via n8n)]]

> [!abstract] Resumo
> Migramos o loop do n8n Cloud (consumia o plano de webhook) para o **n8n self-host** em `n8n.gcrux.com`; atualizamos o n8n **2.20.7 → 2.27.3** sem perder dados; tratamos o flag de **Safe Browsing** (falso-positivo de phishing no login do n8n, que está **atrás do Cloudflare**); embutimos o **roadmap na memória dos dois agentes**; e endurecemos o userscript. O loop **fechou a Sprint 13** e a Regra Perene (na memória) detectou um débito → **Sprint 13 sendo reaberta** para fechar os backoffices pendentes antes da 14.

---

## 🖥️ Migração para self-host
- Saímos do `manuelmpires.app.n8n.cloud` (cobrava por execução) para o **self-host `n8n.gcrux.com`** (Docker na Oracle `137.131.243.179`, container `n8n-n8n-1`, imagem custom `n8n-ffmpeg`, Postgres `n8n-postgres-1`, bind `127.0.0.1:5678`).
- Workflow importado via CLI como **`LovableLoopSelf1`** (`n8n import:workflow`), credencial **OpenRouter** já existente linkada (`Uivw3NVCPPRTWvQw`). Driver = `nvidia/nemotron-3-super-120b-a12b:free`, Crítico = `openai/gpt-oss-120b:free`.
- Webhook produção: `https://n8n.gcrux.com/webhook/lovable-loop` (registrado em `webhook_entity`). Userscript atualizado p/ essa URL + `@connect n8n.gcrux.com`.
- Havia um workflow antigo `hwXpmAmyglmoeFzq` ("My workflow") disputando o path `lovable-loop` → **desativado** (não deletado).

## ⬆️ Update n8n 2.20.7 → 2.27.3
- Imagem é build custom: `Dockerfile` = `FROM n8nio/n8n:<versão>` + ffmpeg estático. Atualização = bump no `FROM` + `docker compose build` + `up -d` (migrations rodam no boot).
- **Zero perda**: 36 workflows, 21 credenciais, chave de criptografia preservada (volume `n8n_data`).
- **Rollback** em `/home/ubuntu/n8n/`: imagem `n8n-ffmpeg:rollback-2.20.7`, dump `backup-20260623-1449-n8n-db.sql.gz`, `Dockerfile.bak-2.20.7`.

## 🛑 Safe Browsing (tela vermelha "Site perigoso")
- Só o `n8n.gcrux.com` (não outros subdomínios) → **falso-positivo de phishing na página de login do n8n** (não é malware; varredura no servidor não achou malware real).
- Descoberta-chave: `n8n.gcrux.com` está **atrás do Cloudflare** (`server: cloudflare`). Por isso Basic Auth no origin ficou ruim (pedia senha a cada request) → **revertido**.
- **Solução recomendada (no Cloudflare, conta do usuário):** Cloudflare **Access (Zero Trust)** na app `n8n.gcrux.com` com **policy Allow** (e-mail do dono) + uma app de path `/webhook` com **policy Bypass** (público) → esconde o login do Google na borda, sem prompt por página, webhook aberto. Depois: **Search Console → Solicitar revisão** (só o usuário; remove o flag em ~1–3 dias).
- Arquivo de referência no projeto: `n8n-vhost-cloudpanel.conf` (vhost com Basic Auth, caso opte por origin no futuro).

## 🧠 Modelos & rate limit (aprendizado)
- `openrouter/free` faz **roleta de modelos** (de 1.2B a 120B) → decisões inconsistentes. **Fixar** um modelo capaz no Driver (ex.: nemotron-super-120b).
- Rate limit do free é **por conta** (todos os `:free` somados) — alternar entre free não resolve. Fix durável = **crédito pequeno na OpenRouter**.

## ✍️ Prompts (correções + roadmap)
- Crítico **"corrige, não trava"**: veto só p/ inseguro/destrutivo/loop-sem-saída; senão `verdict=revise` com a action certa (ele tem a palavra final, mascara Driver fraco).
- Driver **pós-aprovação → execução**: plano salvo / "por qual bloco começar" → entra em execução (Bloco 1 migration), nunca re-elabora.
- **ROADMAP DE REFERÊNCIA embutido nos dois prompts** (Sprint 13 itens de fechamento + mapa 14–25 com backoffices). É a "memória" que faltava.

## 🛡️ Userscript (hardening)
- `isBusy` ignora o painel `#llp` (bug do botão "Parar" que travava em "Aguardando ocioso").
- No-progress só conta resposta **após um prompt nosso** (evita falso-positivo de re-leitura).
- Guard p/ `approve_plan` sem plano pendente (para após 3x).
- **Retry com backoff** (60/120/180/240s) quando o n8n falha (rate limit transitório) — antes matava o loop no 1º erro.
- `start()` reseta estado (sem precisar F5).

## ✅ Sprint 13 (status)
- Loop aprovou o plano sozinho e executou: migration → services → hooks → smoke (14 passos OK) → UI `/crm/quotations` (CRUD + cálculo MDC, piso 42%) → backoffice `/admin/quotations` → validação Playwright → **fechamento** (`CURRENT.md` + `HANDOFF-2026-06-24.md`).
- **MAS** a Regra Perene (na memória do agente) pegou um **débito aberto**: faltam `/admin/crm/bundles`, `/admin/crm/discount-rules` e `DealProductsTab` + catálogo `/crm/bundles` (do gerador de cotação a partir de Deal). Tinha sido "aceito p/ destravar a 14"; o agente corretamente **vai reabrir a Sprint 13** para fechá-los.

## ▶️ Próximos passos (retomar aqui)
1. Fechar Sprint 13: `/admin/crm/bundles` → `/admin/crm/discount-rules` → `DealProductsTab` + `/crm/bundles` → re-validação Playwright → reverter `CURRENT.md` p/ 🟡 e ajustar o handoff (remover aceitação do gap).
2. Só então abrir **Sprint 14 (Saved Views)** com `/handson` + `bok-scribe`.
3. **Cloudflare Access** + **Search Console review** p/ tirar o flag.
4. Aplicar (se ainda não) os prompts com roadmap nos nós Driver/Crítico (UI, sem restart) e repastar o userscript com retry/backoff.
5. Considerar crédito na OpenRouter p/ acabar com rate limit.

---
*Breadcrumb Cowork 2026-06-24. Projeto: [[Agente Lovable Browser]].*

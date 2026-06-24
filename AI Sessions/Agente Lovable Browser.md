---
type: hub
tags:
  - project/agente-lovable-browser
  - infra/n8n
  - infra/cloudflare
  - automation
  - index
---

# 🤖 Projeto Agente Lovable Browser

Núcleo do projeto **Agente Lovable Browser**: conduz o builder do **Lovable** pelo roadmap do **OKEAN CRM** de forma autônoma, via userscript (Tampermonkey) + time adversarial no **n8n** (Driver + Crítico) com guardrails determinísticos. O humano é o último recurso.

> [!info] Infra atual (self-host)
> * **n8n:** self-host `https://n8n.gcrux.com` (Docker na Oracle `137.131.243.179`, container `n8n-n8n-1`, imagem custom `n8n-ffmpeg`, **n8n 2.27.3**, Postgres). Atrás do **Cloudflare**.
> * **Workflow:** `LovableLoopSelf1` — `Webhook → Driver → Crítico → Guardrails → Respond`. Webhook prod: `/webhook/lovable-loop`.
> * **Modelos (OpenRouter):** Driver `nemotron-3-super-120b:free` · Crítico `gpt-oss-120b:free`. (free tem rate limit por conta — avaliar crédito.)
> * **Cloud antigo** (`manuelmpires...n8n.cloud`, workflow `fJIbF7ZbTm2CMYUu`): aposentado (cobrava por execução).

---

## 📂 Sessões do Projeto

*   `[[2026-06-24 - Lovable Loop self-host + n8n 2.27.3 + Safe Browsing]]` — migração self-host, update n8n, Cloudflare/Safe Browsing, roadmap na memória, retry/backoff, fechamento da Sprint 13.
*   `[[2026-06-23 - Lovable Loop (Driver+Critico via n8n)]]` — desenho, build e testes ponta a ponta do loop adversarial.

---

## 🗺️ Arquitetura
`Lovable (userscript) → POST estado → n8n Webhook → Driver Agent → Critic Agent → Guardrails (código) → Respond → volta`

## 🛡️ Guardrails
Veto do Crítico (só inseguro/loop sem saída) · teto de iterações (60) · prompt quase-literal repetido (≥90%) · no-progress (Lovable repete resposta ≥2x, só pós-prompt) · approve sem plano (3x) · prompt destrutivo · **retry/backoff** em erro do n8n · botão Parar (kill-switch).

## 🧭 Estado atual (2026-06-24)
- **Sprint 13 sendo reaberta** pela Regra Perene: faltam `/admin/crm/bundles`, `/admin/crm/discount-rules`, `DealProductsTab` + `/crm/bundles`. Depois → **Sprint 14 (Saved Views)**.
- Pendências de ops: **Cloudflare Access** + **Search Console review** (tirar o flag), e aplicar prompts c/ roadmap + userscript c/ retry (repaste).

## 📁 Arquivos (Windows: `C:\Users\gabri\Claude\Projects\Agente Lovable Browser`)
`lovable-loop.user.js` · `n8n-workflow-lovable-loop.json` · `qa-driver-prompt.md` · `qa-critic-prompt.md` · `guardrails-code.js` · `lovable-selectors.js` · `n8n-vhost-cloudpanel.conf` · `README.md`

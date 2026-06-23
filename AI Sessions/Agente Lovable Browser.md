---
type: hub
tags:
  - project/agente-lovable-browser
  - infra/n8n
  - automation
  - index
---

# 🤖 Projeto Agente Lovable Browser

Núcleo do projeto **Agente Lovable Browser**: um sistema que conduz o builder do **Lovable** pelo roadmap do [[Agente Lovable Browser|OKEAN CRM]] de forma autônoma, via userscript (Tampermonkey) + um time adversarial de agentes no **n8n** (Driver + Crítico) com guardrails determinísticos. O humano é o último recurso, não a engrenagem.

> [!info] Stack
> * **Frente:** userscript no Lovable (monitora, extrai estado, injeta prompt, aprova plano)
> * **Cérebro:** n8n `Webhook → Driver (OpenRouter) → Crítico (OpenRouter) → Guardrails → Respond`
> * **n8n:** `manuelmpires.app.n8n.cloud` · workflow `fJIbF7ZbTm2CMYUu` · webhook `/webhook/lovable-loop`
> * **Projeto Lovable:** `YBuilder Oficial` (OKEAN CRM)

---

## 📂 Sessões do Projeto

*   `[[2026-06-23 - Lovable Loop (Driver+Critico via n8n)]]` (ClaudeSessions / Cowork) - *2026-06-23* — desenho, build e testes ponta a ponta do loop adversarial.

---

## 🗺️ Arquitetura

```
Lovable (userscript)  --POST estado-->  n8n Webhook
        ^                                   |
        |                            Driver Agent  (propoe proximo passo)
   injeta prompt / aprova                   |
   (modo autonomo)                   Critic Agent  (aprova / revisa / veta)
        |                                   |
        |                            Guardrails (codigo) - loop/teto/destrutivo/no-progress
        +----- resposta JSON --------  Respond to Webhook
```

## 🛡️ Guardrails (gate automático que substitui o clique humano)

| Gatilho | Resultado |
|---|---|
| Veto do Crítico | `halt` + notificação |
| `iteration >= MAX_ITERATIONS` (60) | `halt` |
| Prompt quase-literal repetido (≥90%) | `halt` (loop) |
| Lovable repete a resposta ≥2x (no-progress) | `halt` (loop real) |
| Prompt destrutivo (drop/delete/reset/force-push/remover auth) | `halt` |
| Botão **Parar** no painel | kill-switch imediato |

## 📁 Arquivos (na máquina Windows: `C:\Users\gabri\Claude\Projects\Agente Lovable Browser`)
- `lovable-loop.user.js` — userscript Monitor + Webhook + loop
- `n8n-workflow-lovable-loop.json` — workflow importável
- `qa-driver-prompt.md` / `qa-critic-prompt.md` — system prompts
- `guardrails-code.js` — nó de guardrails
- `lovable-selectors.js` — mapa de seletores DOM
- `README.md`

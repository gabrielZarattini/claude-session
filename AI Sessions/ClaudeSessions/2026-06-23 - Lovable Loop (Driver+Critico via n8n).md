---
type: session
date: 2026-06-23
tags:
  - project/agente-lovable-browser
  - infra/n8n
  - feat/lovable-loop
  - automation
  - tool/cowork
session_id: cowork-2026-06-23-lovable-loop
---

# Session — Lovable Loop (Driver + Crítico via n8n)

**Date:** 2026-06-23 | **Tool:** Cowork (desktop) | **Hub:** [[Agente Lovable Browser]]

> [!abstract] Resumo
> Construção e teste ponta a ponta de um agente que conduz o builder do **Lovable** pelo roadmap do **OKEAN CRM** sem o joguinho de Q&A. Userscript monitora o Lovable e fala com um time **adversarial** no n8n (Driver propõe, Crítico revisa) protegido por **guardrails determinísticos**. Validado em produção; rodado em dry-run e autônomo.

---

## 🎯 Objetivo
Dado um roadmap já elaborado (Sprints 13→25, com a "Regra Perene" de backoffices `/admin/*` e a malha abertura→execução→fechamento), automatizar a condução do Lovable: o agente decide o próximo passo, aprova planos e avança sprints sozinho — o humano só intervém em último caso.

## 🗺️ Arquitetura
`Lovable (userscript) → POST estado → n8n Webhook → Driver Agent → Critic Agent → Guardrails (código) → Respond to Webhook → volta pro userscript`

- **Driver** (OpenRouter): lê o estado e propõe a próxima ação seguindo a malha.
- **Crítico** (OpenRouter, família diferente de propósito): revisa adversarialmente — ordem da malha, Regra Perene, loop, escopo, segurança, aprovação prematura.
- **Guardrails** (nó Code): gate determinístico que substitui o clique humano.

## 🧩 Infra
- n8n: `manuelmpires.app.n8n.cloud` · workflow `fJIbF7ZbTm2CMYUu` · webhook prod `/webhook/lovable-loop`.
- Modelos via OpenRouter (cred "OpenRouter account"). Testado: Driver `nvidia/nemotron-3-ultra-550b-a55b:free` (lento), Crítico `openai/gpt-oss-120b:free`. Free de 550B tem baixa disponibilidade — preferir modelos menores/confiáveis.
- Projeto Lovable: `7506d5d8-f891-470c-a48f-e0837fb18178` ("YBuilder Oficial").

## 🔎 Seletores DOM do Lovable (validados)
- Input: `div.ProseMirror[contenteditable="true"][role="textbox"]` (TipTap, **não** textarea — injeção via `execCommand`).
- Enviar: `form button[type="submit"]`.
- Mensagens: chat **virtualizado**; texto limpo em `[data-message-copy-text]`; papel no `data-message-id` (`usr`/`ast`/`its`).
- Plano pendente: presença do botão `Approve`. Conteúdo do plano: `.plan-editor-tiptap-content .ProseMirror` (abrir via `button[aria-label="Open plan"]`).

## 🧠 Decisões e descobertas (a jornada)
1. **Sem loop 100% cego:** a segurança vive em **guardrails automáticos**, não num gate de clicar Send. O usuário aceitou ser o último recurso.
2. **Time adversarial** (Driver + Crítico de famílias diferentes) reduz pontos cegos correlacionados — substitui o gate humano.
3. **Loop por texto do prompt é sinal ruim:** dois prompts de sentido idêntico deram só ~0.67 de Jaccard. Trocado para detecção por **falta de progresso** (resposta do Lovable repetindo ≥90%, 2x). Prompt quase-literal (≥90%) ficou só como backstop.
4. **Prompt do agente tem que ser instrução LITERAL ao Lovable** — o Crítico estava vazando meta-comentário ("a proposta indica... corrija a fase"). Corrigido.
5. **Fase:** "abertura" só para sprint nova; sprint com pendências é "execucao"/"fechamento".
6. **Enviar `currentPlan`:** com o plano em mãos o agente avalia em vez de pedir de novo.
7. **Plano pendente = aprovar, não refazer:** mandar prompt de texto com plano pendente faz o Lovable **rejeitar** o plano e pedir ajuste → loop. Regra forçada: plano que cobre o protocolo ⇒ `approve_plan` (clica Approve), nunca "refaça".
8. **Bug do `isBusy`:** ele contava o botão "Parar" do **próprio painel** do userscript como "parar geração" → travava em "Aguardando ocioso". Corrigido (exclui `#llp` + padrão específico).

## ✅ Testes (produção)
- Pipeline completo Driver→Crítico→Guardrails→Respond. ✔
- Crítico pegou **aprovação prematura** e rebaixou para passo concreto. ✔
- HALT por **teto de iterações**. ✔
- HALT por **no-progress** ("Lovable repetiu a resposta 2x"). ✔
- Injeção no ProseMirror ao vivo (dry-run montou prompt de fechamento limpo). ✔
- Com prompts corrigidos: decisão final limpa — `send_prompt` fase `execucao`, Crítico `approve`, ex.: *"Rode o smoke /devtools/quotation-generator-smoke (6 cenários) antes da UI."* ✔

## 📜 Contrato JSON
**Userscript → Webhook:**
```json
{ "project":"OKEAN CRM","currentSprint":"13","lovableLastResponse":"...","lastUserPrompt":"...",
  "planPending":true,"currentPlan":"...","status":"idle","iteration":0,"maxIterations":60,
  "recentPrompts":["..."],"recentResponses":["..."] }
```
**Agente → Userscript:**
```json
{ "action":"approve_plan|send_prompt|wait|halt|stop","prompt":"...","sprint":"13","phase":"execucao",
  "reason":"...","stop":false,"critic":{"verdict":"approve|revise|veto","notes":"..."} }
```

## 🤖 System Prompt — Driver
```text
Você é o "Driver QA", um engenheiro-condutor AUTÔNOMO que guia o builder de IA do Lovable através do roadmap do projeto OKEAN CRM. Você é o procurador do usuário: decide por ele.
Regras-chave: segue a malha (abertura→execução→fechamento) + Regra Perene (/admin/*).
FASE: "abertura" só em sprint nova; sprint com pendências = execucao/fechamento.
PROMPT: texto LITERAL imperativo ao Lovable, nunca meta-comentário.
PLANO PENDENTE: enviar texto com plano pendente REJEITA o plano (loop). Se currentPlan cobre o protocolo ⇒ OBRIGATORIAMENTE approve_plan; nunca "refaça". send_prompt só se faltar item concreto (dizer o que ADICIONAR).
Saída: SOMENTE JSON {action, sprint, phase, prompt, reason, stop}.
```
(versão completa no arquivo `qa-driver-prompt.md` do projeto)

## 🕵️ System Prompt — Crítico
```text
Você é o "Crítico", revisor ADVERSARIAL. Recebe o estado do Lovable + a proposta do Driver. Cético.
Checa: ordem da malha, Regra Perene, risco de loop, escopo, segurança, aprovação prematura.
Veredito: approve / revise / veto.
SAÍDA: o campo "prompt" é SEMPRE instrução limpa ao Lovable (crítica vai em "notes"). Se o Driver errou, gere você o prompt certo.
PLANO PENDENTE: se currentPlan cobre o protocolo, a ÚNICA ação é approve_plan; vete/corrija qualquer "refaça".
Saída: SOMENTE JSON {verdict, action, prompt, notes}.
```
(versão completa em `qa-critic-prompt.md`)

## ⚙️ Guardrails (nó Code do n8n)
```javascript
// Crítico tem a palavra final; fallback no Driver.
let action = critic.action || driver.action || 'wait';
let prompt = (critic.verdict==='revise'||critic.verdict==='veto') ? (critic.prompt||driver.prompt||'') : (driver.prompt||'');
const sim = (a,b)=>{/* Jaccard de tokens */};
if (critic.verdict==='veto') { halt=true; }                                   // veto
if (iteration >= MAX_ITER)  { halt=true; }                                    // teto
if (action==='send_prompt' && recent.some(p=>sim(p,prompt)>=0.9)) halt=true;  // prompt repetido
if (/drop\s+table|delete\s+from|...|remover?\s+auth/i.test(prompt)) halt=true;// destrutivo
const stuck = recentResp.filter(r=>sim(r,lastResp)>=0.9).length;
if (!halt && stuck>=2) halt=true;                                             // no-progress (loop real)
if (halt) action='halt';
```
(versão completa em `guardrails-code.js`)

## ▶️ Próximos passos
- Confirmar caminho `approve_plan` ao vivo no modo autônomo (script clica Approve → plano executa).
- Capturar seletor exato do estado "gerando" do Lovable (hoje usa estabilidade de texto).
- Avaliar Driver num modelo free mais rápido/confiável que o nemotron-550b.

---
*Breadcrumb gerado na sessão Cowork de 2026-06-23. Projeto: [[Agente Lovable Browser]].*

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-22 - agent-afbda1deee15bc84c]]
> * **Próxima Sessão**: [[2026-06-23 - Próximos passos do projeto]]
%% --- TIMELINE END --- %%

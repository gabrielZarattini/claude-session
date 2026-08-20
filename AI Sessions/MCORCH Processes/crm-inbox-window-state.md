# SOP — CRM Inbox: máquina de estado da janela de atendimento (WhatsApp CSW 24h)

> **Lei 2 (Processo Antecipado).** Este SOP documenta o processo humano equivalente ANTES de confiar na automação. O módulo `crm-inbox` (Fatias 1+2, WhatsApp-first) automatiza um fluxo que um atendente humano hoje executaria manualmente no app do WhatsApp Business — persistir a conversa, saber se a janela grátis de 24h está aberta, e escolher entre mensagem livre (grátis) ou template aprovado (pago). Se o humano não consegue executar sem erro, a automação também não.
>
> **BoK SSOT:** [`docs/bok/crm-inbox/05-sdd.md`](../bok/crm-inbox/05-sdd.md) · [`06-data-model.md`](../bok/crm-inbox/06-data-model.md) · [`07-process-flow.md`](../bok/crm-inbox/07-process-flow.md). **Contrato Meta:** janela de atendimento (customer service window) de 24h abre no inbound do cliente; dentro dela, mensagem livre é permitida e grátis; fora, exige template pré-aprovado (blueprint §3.1, fontes primárias Meta).

---

## ORO

| Papel | Quem |
|-------|------|
| **Operator** | MCORCH Master Execution Agent (automação) · humano de plantão = Sovereign/Usuário Zero operando o inbox em `/dashboard/inbox` |
| **Reviewer** | `/security-review` (toda migration/edge fn que toca o rail) + Sovereign (witness E2E) |
| **Owner** | Sovereign — blast radius: envio de mensagem em nome do tenant, custo per-message do WhatsApp em USD real, conversas = PII (LGPD) |

---

## 0. Estado do mundo (o que a máquina persiste)

Por conversa (`public.conversations`), o servidor mantém a verdade da janela — **nunca o cliente**:

| Coluna | Autoridade | Significado |
|--------|-----------|-------------|
| `window_expires_at` | **servidor** (webhook) | `last_inbound_at + 24h`. `NULL` ⇒ nunca houve inbound ⇒ janela fechada. |
| `last_inbound_at` | **servidor** (webhook) | timestamp do último inbound REAL do contato. |
| `status` | cliente (operacional) | `open` / `closed` / `archived` — organização do inbox, **não** é a janela. |

**Regra-mãe (NFR-CRM-004):** o composer da UI é conveniência; a fronteira de decisão free-form-vs-template é **reavaliada server-side no envio** (`whatsapp-templates` action `send`). Um cliente adulterando o DOM não consegue mandar mensagem livre com a janela fechada — o `trigger-guard` (`guard_conversation_server_columns`) impede o cliente de estender `window_expires_at`, e o `send` compara `now()` contra o valor persistido.

---

## 1. Sequence — inbound (o cliente escreve para o número do tenant)

| # | Passo | Executor | Critério de sucesso material |
|---|-------|----------|------------------------------|
| 1 | Cliente envia mensagem do celular para o número WhatsApp do tenant | Humano (cliente) | — |
| 2 | Meta entrega webhook `POST` → `whatsapp-webhook` | Meta Cloud API | HTTP 200 no log do Meta; `infra_health_logs` `service='whatsapp-webhook'` status `healthy` |
| 3 | Verifica HMAC (`X-Hub-Signature-256` vs `META_APP_SECRET`) | Edge fn | Assinatura inválida ⇒ 401, **nada persistido** |
| 4 | Resolve o tenant por `phone_number_id`/`waba_id` (nunca do corpo confiando no cliente) | Edge fn | `meta_config.user_id` encontrado; senão 404 `tenant_not_found` |
| 5 | Dedup por `provider_message_id` (o Meta REENTREGA webhooks) | Edge fn + `messages_provider_dedup_uniq` | reentrega do mesmo `wamid` ⇒ 0 linhas novas em `messages` |
| 6 | Upsert `conversations` (`window_expires_at = ts+24h`, `last_inbound_at=ts`) + insert `messages` (`direction='inbound'`) | Edge fn (service-role) | `SELECT` retorna a conversa com janela ~24h à frente; 1 linha em `messages` |
| 7 | Inbox atualiza (Realtime primário, poll 30s teto) | `useConversations` | conversa aparece no topo da lista em ≤60s (NFR-CRM-001) |

**Success signal:** a mensagem do cliente aparece na thread em `/dashboard/inbox` com o badge de janela **verde** (aberta) e countdown ~24h.

---

## 2. Sequence — outbound (o operador responde)

| # | Passo | Executor | Critério de sucesso material |
|---|-------|----------|------------------------------|
| 1 | Operador seleciona a conversa e vê o **badge de janela** | Humano | verde = aberta (livre grátis) · âmbar = fecha em <2h · cinza = fechada (só template) |
| 2a | **Janela aberta** → digita texto livre → Enviar | Humano | `send` action, `type='text'` → grava outbound `content_type='text'`, **0 mco** |
| 2b | **Janela fechada** → composer trava o livre, força **seletor de template aprovado** (com classe de custo por categoria) | Humano | `send` action, `type='template'`; MARKETING/AUTHENTICATION = pago via `deduct_mco_coins` ANTES do Graph |
| 3 | `send` reavalia a janela server-side | Edge fn | livre fora da janela ⇒ **422 `window_closed`** (nunca vaza para o Graph) |
| 4 | Graph API `POST /{phone_id}/messages` | Edge fn | `messages[0].id` (wamid) retornado |
| 5 | Grava outbound em `messages` + atualiza `last_message_at`/preview da conversa | Edge fn (service-role) | 1 linha outbound com `sent_by = auth.uid()`, `authored_by='human'` |

**Success signal:** a resposta aparece na thread marcada como outbound; se template pago, `profiles.mco_balance` decrementou exatamente o custo da categoria (delta por `SELECT`).

---

## 3. Verification gates (como o operador confirma cada passo)

| Gate | Comando/observação | Output esperado |
|------|--------------------|-----------------|
| Inbound persistido | `SELECT id, window_expires_at FROM conversations WHERE external_thread_key='<phone>'` | 1 linha, janela ~24h à frente |
| Dedup | reenviar o mesmo webhook (mesmo `wamid`) | `SELECT count(*) FROM messages WHERE provider_message_id='<wamid>'` = 1 |
| Cross-tenant = 0 | smoke `scripts/qa/smoke-crm-inbox.ts` (throwaway A tenta ler conversa de B) | 0 linhas / RLS bloqueia |
| Window-gate | `send type=text` numa conversa com `window_expires_at < now()` | HTTP 422 body `{"error":"window_closed"}` |
| Metering livre | enviar texto livre dentro da janela | `mco_balance` inalterado (0 mco) |
| Metering template | enviar template MARKETING | `mco_balance` decrementa o custo; falha do Graph ⇒ refund crédito-positivo |
| Erasure zero-residue | `SELECT erase_lead('<lead>')` | retorna `conversations_removed`/`messages_removed`; re-`SELECT` = 0 |

---

## 4. Recovery path (falha no passo N)

| Falha | Recuperação exata |
|-------|-------------------|
| Webhook 401 (HMAC) após rotação do `META_APP_SECRET` | re-provisionar o secret no vault (`supabase secrets set`) — a rotação do token EAA/app secret está PENDENTE nesta sessão; ver FMEA FM-CRM-15 |
| `tenant_not_found` (404) | conferir `meta_config.whatsapp_phone_number_id` do tenant; reconfigurar em Settings→Meta |
| Reentrega duplicada do Meta | idempotente por design (unique index) — nenhuma ação; se aparecer duplicata, o índice `messages_provider_dedup_uniq` regrediu → investigar |
| `send` 422 `window_closed` | esperado: instruir o operador a usar template; **não** é erro de sistema |
| `send` 402 saldo insuficiente | recarregar mcoCoins; o débito é atômico ANTES do Graph, sem envio sem saldo |
| Graph 5xx no `send` | **NUNCA retry automático** (duplicaria a mensagem ao contato) — refund do mco + erro PT-BR acionável na UI; operador reenvia manualmente |
| `requires_reauth` (token Meta 60d expirou) | CTA de reconexão em Settings→Meta; `send` bloqueia com erro acionável |

---

## 5. Success signal (fluxo completo)

Materialmente observável, ponta-a-ponta:
1. Mensagem enviada do celular do Sovereign para o número `+39…` **aparece** em `/dashboard/inbox` (thread + badge verde) em ≤60s.
2. Resposta livre do operador **chega** no celular do Sovereign, com `profiles.mco_balance` **inalterado** (0 mco — janela aberta).
3. `SELECT` em `conversations`/`messages` confirma as duas linhas (inbound + outbound) com `user_id` do tenant.

Enquanto os três não forem observados juntos (Lei 1), a Fatia não está "pronta" — está "código escrito".

---

## 6. Fora de escopo deste SOP (gated)

- **Agente de reply automatizado** (triagem + rascunho + auto-reply) — Fatia 3, **gate jurídico Sovereign** (AI Act Art.50, exigível 2026-08-02). SOP próprio: `crm-inbox-comment-reply-agent.md` (a escrever quando destravar).
- **Multicanal** (IG/FB DM + comentários, YouTube) — Fatia 3.
- **Pipeline stages configuráveis** — Could pós-MVP (OTD-CRM-007).

---

_Anticorpo permanente (Mandato Obstáculo→Síntese): a armadilha de "confiar no cliente para o estado da janela" foi fechada por design — `window_expires_at` é server-authoritative (trigger-guard) e reavaliada no envio. Nunca mover essa decisão para a UI._

# SOP — Canvas Job Failure Recovery

**Versão:** v1 · **Selada:** 2026-05-16 · **Lei 2 (Processo Antecipado)**

## ORO triplet

- **Operator:** Sovereign (Gabriel) ou engineer agent autorizado
- **Reviewer:** Sovereign
- **Owner:** Sovereign até Phase Commercial; depois Owner do usuário afetado (revenue impact por cliente perdido)

## Contexto

`canvas-execute` cobra credits intencionados antes da inferência. Em sucesso, `deduct_mco_coins` debita; em falha, nada é debitado (atomic on success). Porém o campo `vm_canvas_executions.credits_charged` aparenta cobrança mesmo em falhas — confusão de UI/auditoria.

`higgsfield-webhook` é idempotente (HTTP 409) e só debita após download + validação de bytes (≥100KB + content-type video/*).

## Sequence — execução manual humana

| # | Action | Output esperado | Verification gate |
|---|--------|-----------------|-------------------|
| 1 | Identificar a execução falhada via Canvas Studio UI ou SQL | `vm_canvas_executions.id` (UUID) + `error_message` + `provider`/`model` | UUID match em formato 8-4-4-4-12 |
| 2 | Verificar se houve deduct: query `mcoin_transactions` para o `execution_id` no `context` | Linha negativa OU zero linhas | Se zero linhas E status='failed' → atomic correto; pular step 5 |
| 3 | Identificar causa raiz no `error_message` | Mensagem do provider (e.g., "OpenAI error 429", "no result_url") | Mensagem não-vazia |
| 4 | Decidir retry vs descarte: rate limit → wait + retry; auth/key → fix env; conteúdo → ajustar prompt | Decisão registrada | Documentar no JIRA/issue ou comentário no plan file |
| 5 | (Se houve deduct indevido) Reembolsar via `award_mco_coins`: `npx supabase ...` ou painel Studio | UUID da linha award + balance atualizado | `SELECT mco_balance FROM profiles WHERE id=...` reflete o reembolso |
| 6 | Re-disparar a execução (novo `node_id` ou retry com mesmo) | Nova `vm_canvas_executions.id` | Status='running' inicialmente |
| 7 | Acompanhar status até final | status='success' OU 'failed' | `webhook_received_at` preenchido (para video) |

## Verification gates

Cada step só completa quando o gate material é atendido. Não pular gates "porque pareceu OK".

## Recovery path

- **Step 5 falhou (RPC `award_mco_coins` retornou erro):** verificar `p_amount` ≤ 1000 (limit da RPC). Se válido, fallback: UPDATE manual em `profiles.mco_balance` via Studio + INSERT manual em `mcoin_transactions` com action='manual_refund'.
- **Step 6 segue falhando (3 tentativas):** marcar execução como "abandoned" via UPDATE direto (`status='failed'`, `error_message='abandoned after 3 retries'`). Abrir incident OTD-CM-NNN.

## Success signal

- `vm_canvas_executions.status = 'success'`
- `output_url` preenchido (signed URL acessível por curl HEAD)
- Linha negativa correspondente em `mcoin_transactions` (deduct registrado)
- `infra_health_logs` mostra entry recente com `service='canvas-execute'` ou `'higgsfield-webhook'` e `status='healthy'`

## Anti-patterns

- ❌ "Tentar de novo até funcionar" sem identificar causa
- ❌ Reembolsar antes de confirmar que houve deduct
- ❌ Marcar status='success' manualmente sem `output_url` real

## Referências

- `supabase/functions/canvas-execute/index.ts:232-267`
- `supabase/functions/higgsfield-webhook/index.ts:91-222`
- `.claude/context/survival-audit-v1.md` (5 execuções falhadas documentadas em 2026-05-14/15)

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

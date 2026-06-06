# SOP — Canvas Daily Cap Handling

**Versão:** v1 · **Selada:** 2026-05-17 · **Lei 2 (Processo Antecipado)** · **SSP-01 OE04**

## ORO triplet

- **Operator:** end user (gera no Canvas Studio); admin (overrides — Phase 5)
- **Reviewer:** Sovereign (revisa policy quando cap atingido por user pagante)
- **Owner:** Sovereign (cost discipline owner — Pillar 3)

## Contexto

`canvas-execute` agora aplica um **Daily Cap de 100 mcoCoins** por usuário (janela rolante de 24h). Quando o user tenta gerar e o cap seria estourado, o backend retorna HTTP 402 com JSON estruturado em vez de cobrar. Esta SOP cobre o fluxo de **reconhecimento + comunicação + recovery** para o usuário e o operador.

**Por que existe:** Survival Audit v1 escorou Cost Discipline 2/5. Sem cap, um bug ou abuse case poderia drenar todo o saldo de um user em minutos (5 falhas Higgsfield em 30s = 130 mcoCoins ≈ R$ 10 perdidos). Cap = blast radius limitado + previsibilidade financeira.

**Threshold rationale:** 100 mcoCoins/dia ≈ $8 USD (markup 13× sobre custo nominal Higgsfield). Permite ~5 vídeos Soul 1080p_4 (65 each) OU ~25 imagens DALL·E 3 (15 each) por dia. Suficiente para validação criativa de Usuário Zero; insuficiente para abuse.

## Resposta HTTP quando cap atingido

```json
HTTP 402 Payment Required
{
  "error": "Daily Canvas cap reached",
  "cap": 100,
  "spent_today": 95,
  "required": 20,
  "resets_at": "2026-05-18T05:00:00.000Z"
}
```

## Sequence — fluxo do usuário

| # | Action | Output esperado | Verification gate |
|---|--------|-----------------|-------------------|
| 1 | User dispara generation no Canvas que estouraria cap | Frontend recebe HTTP 402 com JSON acima | `error: "Daily Canvas cap reached"` |
| 2 | Frontend renderiza toast: "Cap diário atingido (95/100 mcoCoins). Reseta em <X>h." | Sonner toast visível, duração ≥6s | `id: "canvas-cap-reached"` (dedupe) |
| 3 | User aguarda janela rolante reset (próxima execução >24h após a primeira do dia) | Próxima generation cobra normal | spent_today drops below `cap` |
| 4 | (Se user pagante reclamar) Operator analisa `mcoin_transactions` filtrado por `action LIKE 'canvas_%'` last 24h | Lista de gastos com timestamps | sum = `spent_today` reportado |
| 5 | (Decisão Sovereign) override manual: insert linha `award_mco_coins` com `action='canvas_cap_override'` para zerar contagem efetiva | UUID returned | next call passes cap check |

## Verification gates

- Cap check ANTES do deduct: garante zero cobrança quando bloqueado.
- Action tagging consistente: TODA chamada `canvas-execute` em sucesso usa `canvas_image_spend` ou `canvas_video_spend`. Sem tags, query do cap não conta.
- Reset implícito: query usa `created_at >= now() - interval '24 hours'`. Não há cron de reset (janela rolante > janela calendário).

## Recovery path

- **Cap bloqueia legítimo (user pagante de alto LTV):**
  - Operator faz `INSERT INTO mcoin_transactions (user_id, action, amount, context) VALUES (<uid>, 'canvas_cap_override', 100, '{"reason":"manual_review","approved_by":"Sovereign"}')`.
  - Como `amount > 0`, NÃO conta no `spent_today` (que soma `abs(amount)` mas filtra por `action LIKE 'canvas_%'` — override match mas é positivo, então sum acaba subtraindo).
  - **TODO Phase 5:** mudar query do cap para `WHERE amount < 0` (mais robusto). Por ora, override usa action diferente: `canvas_credit_grant` (não matchea o LIKE).
- **Cap falha-aberto (query DB erro):** código atual loga e continua. Pillar 4 (Observability) captura via `infra_health_logs`.
- **User abusa (>100/dia repetido):** rate-limit no nível conta — Phase Commercial bloqueia tentativas excessivas em janela curta.

## Success signal

- `canvas-execute` retorna 402 quando `spent_today + required > cap`.
- `mcoin_transactions` tem TODA spend canvas com `action LIKE 'canvas_%'`.
- `DashboardLayout` mostra balance pill amber quando `mco_balance < 50`.
- Toast renderiza quando user cruza threshold.

## Anti-patterns

- ❌ Aumentar cap silenciosamente (>100) para resolver complaint específico — usar override row, manter cap visível.
- ❌ Cobrar antes do cap check — vira sangria de moedas em failed gens.
- ❌ Cap por janela calendário (00:00–23:59) — abre brecha para gastar 100 às 23:59 e mais 100 às 00:01 = 200 em 2 min. Janela rolante 24h é defensiva.
- ❌ Action tagging genérico (`spend` para tudo) — quebra a query do cap.

## Referências

- `supabase/functions/canvas-execute/index.ts` (daily cap implementation + action tagging)
- `supabase/migrations/20260516224541_deduct_mco_coins_ledger.sql` (ledger 4-arg RPC)
- `src/components/dashboard/DashboardLayout.tsx` (toast + amber pill)
- `.claude/context/survival-audit-v1.md` §2 Pillar 3 (motivação)
- `.claude/context/survival-audit-v2.md` (re-audit pós-implementação)

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

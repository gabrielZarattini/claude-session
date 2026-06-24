# SOP — mcoCoins Ledger Reconciliation

**Versão:** v1 · **Selada:** 2026-05-16 · **Lei 2 (Processo Antecipado)**

## ORO triplet

- **Operator:** scientist agent ou Sovereign
- **Reviewer:** Sovereign
- **Owner:** Sovereign até v6.4.x; depois CFO/Finance role quando existir

## Contexto

A partir de `20260516224541_deduct_mco_coins_ledger.sql` (deploy 2026-05-16):
- `award_mco_coins` → INSERT linha positiva em `mcoin_transactions`
- `deduct_mco_coins` → INSERT linha negativa em `mcoin_transactions` + UPDATE `profiles.mco_balance`

Antes desta migration, `deduct` só atualizava balance sem logar. Resultado: histórico pré-2026-05-16 é caixa-preta contábil — balance ≠ Σ ledger.

Audit v1 confirmou: Sovereign user `ada39fae...` tem `mco_balance=5533` e zero linhas em `mcoin_transactions`. Reconciliação retroativa requer decisão Sovereign (backfill sintético vs aceitar opening balance).

## Sequence — execução manual humana

| # | Action | Output esperado | Verification gate |
|---|--------|-----------------|-------------------|
| 1 | Query opening balance por user: `SELECT id, mco_balance FROM profiles` | Lista de UUIDs + balances atuais | Count > 0 |
| 2 | Query ledger sum por user: `SELECT user_id, SUM(amount) FROM mcoin_transactions GROUP BY user_id` | Lista de UUIDs + sum | Pode ser vazio em deploy novo |
| 3 | Computar drift = `mco_balance - SUM(amount)` por user | Tabela `user_id, drift` | Drift = 0 → reconciled; drift ≠ 0 → backfill needed |
| 4 | (Se drift ≠ 0) Decidir: opção A = INSERT linha sintética `action='opening_balance_2026_05_16'` com amount=drift; opção B = aceitar drift como pre-ledger black-box | Decisão registrada em ADR | ADR mergeado em `docs/bok/<slug>/05-sdd.md` |
| 5 | (Se opção A) Executar inserts sintéticos via SQL com prefix `opening_balance_` em action | Linhas inseridas com timestamp '2026-05-16T00:00:00Z' | `SUM(amount) = mco_balance` per user |
| 6 | Re-rodar drift check | Drift = 0 ∀ user | Reconciled |
| 7 | Agendar reconciliação semanal: `scripts/mcoins-reconcile.ts` cron `0 4 * * 0` (domingo 04:00) | Cron line installed | `crontab -l` mostra a linha |

## Verification gates

- Step 3: drift ZERO → reconciled. Drift ≠ 0 sem decisão registrada → STOP.
- Step 5: SUM must equal balance after backfill. Se diferir, rollback (DELETE das linhas sintéticas inseridas).

## Recovery path

- **Backfill quebrou balance**: ROLLBACK transactional não disponível em INSERTs separados. Fix: `DELETE FROM mcoin_transactions WHERE action LIKE 'opening_balance_%' AND created_at = '2026-05-16T00:00:00Z'` + re-rodar do Step 4.
- **Drift descoberto pós-Phase-Commercial**: bloquear novos creditos do user até reconciliar. Notificar Sovereign + Reviewer.

## Success signal

- `SELECT (mco_balance - COALESCE(SUM(amount),0)) AS drift FROM profiles p LEFT JOIN mcoin_transactions t ON t.user_id=p.id GROUP BY p.id, p.mco_balance` retorna `drift=0` ∀ row.
- `infra_health_logs` mostra entry `service='mcoins-reconcile'`, status='healthy' recente.

## Anti-patterns

- ❌ "Vou só ajustar o balance manualmente" — ledger fica de fora, drift volta na próxima query.
- ❌ INSERT sem `action` prefix `opening_balance_*` — vira ruído indistinguível de spend real.
- ❌ Aceitar drift "porque é pouco" — bom é zero ou registrado explicitamente.

## Referências

- `supabase/migrations/20260508100000_mcoin_transactions.sql`
- `supabase/migrations/20260516224541_deduct_mco_coins_ledger.sql`
- `.claude/context/survival-audit-v1.md` §3.B (Discrepância documentada)

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

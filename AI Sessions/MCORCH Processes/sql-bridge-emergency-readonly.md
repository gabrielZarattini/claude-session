# SOP — SQL Bridge Emergency Read-Only Fallback

**Versão:** v1 · **Selada:** 2026-05-16 · **Lei 2 (Processo Antecipado)**

## ORO triplet

- **Operator:** Sovereign (Gabriel) — caminho que NÃO depende da AI nem do bridge funcionando
- **Reviewer:** Sovereign (self)
- **Owner:** Sovereign

## Contexto

Se `aios-sql-bridge` cair (deploy ruim, quota exhausted, admin role revogado, JWT expirado, gateway 5xx), a AI vira "Cérebro sem mãos" para Materiality proofs. Esta SOP é o **caminho manual de emergência** para o Sovereign obter UUIDs reais sem o bridge.

## Sequence — execução manual humana

| # | Action | Como executar | Verification gate |
|---|--------|---------------|-------------------|
| 1 | Abrir Supabase Studio: https://supabase.com/dashboard/project/bcyvddsykvehvpwstlfa/sql/new | Browser | Login válido |
| 2 | Escolher query a partir do menu abaixo (canned queries) | Copy/paste | Query string completa |
| 3 | Executar (Run ou Ctrl+Enter) | Studio | Result panel mostra rows |
| 4 | Copiar UUIDs do result panel | Manual highlight + Ctrl+C | Lista de UUIDs em formato 8-4-4-4-12 |
| 5 | Colar no chat com AI (ou em log file) | Manual | AI usa como Material proof |

## Canned queries (read-only, paste-and-run)

### Q1 — Latest mcoin_transactions (10 UUIDs)
```sql
SELECT id, user_id, action, amount, created_at, context
FROM mcoin_transactions
ORDER BY created_at DESC
LIMIT 10;
```

### Q2 — Sovereign balance + recent activity
```sql
SELECT p.id, p.mco_balance, p.score, p.updated_at,
       (SELECT count(*) FROM mcoin_transactions t WHERE t.user_id=p.id) AS ledger_rows
FROM profiles p
WHERE p.id = 'ada39fae-67e1-4e53-af1c-5a18e1c108e8';
```

### Q3 — Canvas executions com status='failed' (últimas 20)
```sql
SELECT id, user_id, provider, model, status, credits_charged, error_message, created_at
FROM vm_canvas_executions
WHERE status = 'failed'
ORDER BY created_at DESC
LIMIT 20;
```

### Q4 — Infra health timeseries (últimas 50)
```sql
SELECT service, status, last_seen_at
FROM infra_health_logs
ORDER BY last_seen_at DESC
LIMIT 50;
```

### Q5 — Pipeline runs com revenue
```sql
SELECT id, user_id, topic, status, mco_cost, started_at, completed_at
FROM pipeline_runs
ORDER BY started_at DESC
LIMIT 20;
```

### Q6 — Reconciliation drift por user
```sql
SELECT p.id,
       p.mco_balance,
       COALESCE(SUM(t.amount), 0) AS ledger_sum,
       p.mco_balance - COALESCE(SUM(t.amount), 0) AS drift
FROM profiles p
LEFT JOIN mcoin_transactions t ON t.user_id = p.id
GROUP BY p.id, p.mco_balance
ORDER BY ABS(p.mco_balance - COALESCE(SUM(t.amount), 0)) DESC;
```

## Verification gates

- Cada query deve retornar antes de 5s (Studio default timeout).
- Result panel mostra row count exato.
- UUIDs sempre em formato `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`.

## Recovery path

- **Studio retorna timeout:** simplificar query (LIMIT menor, remover JOIN). Se persistir, investigar via psql direto com pooler URL: `psql "$(cat supabase/.temp/pooler-url)"`.
- **Result vazio mas Sovereign esperava dados:** verificar filtros + RLS via `SET ROLE postgres;` no Studio (cuidado, role escalation).
- **Studio inacessível:** fallback ao psql via service-role key. Manual: `psql "postgresql://postgres.bcyvddsykvehvpwstlfa:<password>@aws-0-...supabase.com:5432/postgres"` (password em `.env` ou vault).

## Success signal

- Result panel materializa UUIDs reais
- Sovereign pode copiá-los para validar claims da AI
- AI continua sem precisar do bridge (Lei 1 satisfeita via mão humana)

## Anti-patterns

- ❌ INSERT/UPDATE/DELETE direto no Studio sem migration — quebra a single source of truth do schema
- ❌ Compartilhar queries com PII em chat público
- ❌ Esquecer de fechar a aba Studio com role escalado

## Referências

- `supabase/.temp/pooler-url` (connection string fallback)
- `.env` (SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
- `supabase/functions/aios-sql-bridge/whitelist.ts` (tabelas suportadas pelo bridge equivalente)

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

# SOP — SQL Bridge Admin Bootstrap

**Versão:** v1 · **Selada:** 2026-05-16 · **Lei 2 (Processo Antecipado)**

## ORO triplet

- **Operator:** Sovereign (Gabriel) executando direto via Supabase Studio SQL Editor
- **Reviewer:** Sovereign (self-review — sensível, sem delegação)
- **Owner:** Sovereign (security boundary change)

## Contexto

`aios-sql-bridge` v1 requer admin role (`has_role(auth.uid(),'admin')`). Audit v1 mostrou que `user_roles` só contém roles `viewer` — nenhum admin existe. Sem admin, end-to-end do bridge é inacessível. Esta SOP é o **bootstrap manual seguro** para promover o Sovereign user.

## Pre-conditions

- Sovereign user_id: `ada39fae-67e1-4e53-af1c-5a18e1c108e8` (confirmar em `profiles`)
- Acesso ao Supabase Studio (https://supabase.com/dashboard/project/bcyvddsykvehvpwstlfa)
- `user_roles` tem RLS — service-role bypass apenas via Studio SQL Editor ou via psql com service-role key

## Sequence — execução manual humana

| # | Action | Output esperado | Verification gate |
|---|--------|-----------------|-------------------|
| 1 | Confirmar Sovereign user_id via `SELECT id, mco_balance FROM profiles ORDER BY mco_balance DESC LIMIT 5` | UUID `ada39fae...` no topo (highest balance) | Match string-by-string |
| 2 | Verificar app_role enum: `SELECT unnest(enum_range(NULL::app_role))` | Lista contém `'admin'` | `'admin'` presente |
| 3 | Confirmar que `ada39fae...` ainda não é admin: `SELECT * FROM user_roles WHERE user_id='ada39fae-67e1-4e53-af1c-5a18e1c108e8' AND role='admin'` | Zero rows | Empty result |
| 4 | INSERT do role admin: `INSERT INTO user_roles (user_id, role) VALUES ('ada39fae-67e1-4e53-af1c-5a18e1c108e8','admin') RETURNING id, user_id, role, created_at` | UUID novo, role='admin', timestamp atual | Material proof: UUID returned |
| 5 | Verificar via has_role: `SELECT public.has_role('ada39fae-67e1-4e53-af1c-5a18e1c108e8','admin')` | `true` | Boolean true |
| 6 | Sovereign obtém JWT fresh (login no frontend ou `supabase.auth.signInWithPassword` no Studio) | JWT string ~800 chars | jwt.io decode mostra `sub: ada39fae...` |
| 7 | Smoke test: `curl POST aios-sql-bridge` com `Authorization: Bearer <jwt>` body `{"table":"profiles","limit":1}` | HTTP 200 + 1 row | `rows.length === 1` |

## Verification gates

- Step 4: INSERT RETURNING DEVE retornar o UUID. Se erro de duplicata, rollback (step 3 falhou) — investigar.
- Step 5: `has_role` retorna `true`. Se `false`, RLS pode estar bloqueando OR role não foi inserido. Verificar com `SELECT * FROM user_roles WHERE user_id=...`.
- Step 7: HTTP 200 com row real. Se 403 "Admin role required", role não foi propagado (cache JWT?). Sovereign refresh do JWT (logout/login).

## Recovery path

- **Step 4 falhou (RLS bloqueia INSERT)**: rodar via service-role no SQL Editor (Studio bypasses RLS). Se ainda falhar, ALTER TABLE user_roles DISABLE ROW LEVEL SECURITY temporário (super-risky, reverter imediatamente após insert).
- **Step 7 retorna 401 "Invalid JWT"**: JWT expirou. Re-logar e tentar com token novo. JWT do Supabase tem ~1h de validade.
- **Step 7 retorna 429 "Daily quota exceeded"**: já consumiu 100 queries hoje. Esperar 24h OU `DELETE FROM usage_tracking WHERE user_id=... AND resource_type='sql_bridge_query' AND created_at > NOW() - INTERVAL '24h'` para reset.

## Success signal

- `SELECT * FROM user_roles WHERE user_id='ada39fae...' AND role='admin'` retorna 1 row
- Curl POST com JWT retorna `{"rows":[{...}], "rowCount":1, "queryHash":"...", "executedAt":"..."}`
- `infra_health_logs` mostra entry `service='aios-sql-bridge'`, status='healthy', timestamp ≤ 5s atrás

## Anti-patterns

- ❌ Promover múltiplos users a admin "preventivamente" — apenas Sovereign até Phase Commercial
- ❌ Deixar SQL Editor aberto com admin role após o smoke — fechar imediatamente
- ❌ Compartilhar JWT em chat — JWT é credencial; pode ser revogado mas custa fricção

## Referências

- `supabase/functions/aios-sql-bridge/index.ts:73-89` (admin gate logic)
- `supabase/migrations/20260402014040_b141fb0f-...sql:237-261` (has_role function definition)
- `.claude/context/survival-audit-v1.md` §3.A (No admin findings)

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

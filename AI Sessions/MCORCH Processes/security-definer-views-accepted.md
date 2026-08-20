# SOP — SECURITY DEFINER masked credential views (accepted risk)

> **Status:** Aceito e documentado (2026-07-25). O lint `security_definer_view` do Supabase
> dispara nas views `public.meta_config`, `public.social_accounts`, `public.user_api_keys` — e é
> um **falso-positivo esperado**: essas três são *masked credential views* projetadas
> deliberadamente como `SECURITY DEFINER`. Este SOP registra o racional, as invariantes e o
> gate de re-verificação, para o achado não reaparecer como "bug novo" a cada auditoria.

**ORO** — Operator: engineer / main-loop · Reviewer: Sovereign · Owner: Sovereign (blast radius = camada de credenciais multi-tenant).

---

## 1. O que o lint aponta e por que aqui é aceito

O linter marca qualquer view em `public` que não seja `security_invoker = true`, porque uma view
definer executa com as permissões do **owner** (aqui `postgres`), podendo contornar RLS da tabela-base.
A regra é uma heurística — não enxerga a mitigação embutida.

Estas três views existem para **expor um subconjunto seguro** de tabelas-base que guardam segredos
cifrados (UUID do Vault), sem nunca revelar o segredo. O `SECURITY DEFINER` **não é acidente**: a
migration `20260601000600_secure_definer_views.sql` reverteu deliberadamente de `security_invoker`
para definer, porque o `SELECT` das tabelas-base foi **revogado** de `anon/authenticated` — uma view
`security_invoker` daria *permission denied* na leitura. (Documentado em
`20260601060000_user_api_keys_apify_token.sql:142-144`.)

## 2. Invariantes que tornam o padrão seguro (verificáveis)

| # | Invariante | Onde |
|---|-----------|------|
| I1 | Filtro de tenancy embutido: `WHERE (auth.uid() = user_id OR auth.role() = 'service_role')` nas **três** views | `20260601000600_secure_definer_views.sql:27,45,70` |
| I2 | Toda coluna de token/segredo é mascarada para `'••••••••••••'` via `CASE` — o valor real nunca sai pela view | mesmas linhas + `20260601060000:157-168` |
| I3 | `SELECT` nas tabelas-base revogado de `anon/authenticated` — cliente não toca a base direto | `20260601000600:91-93` |
| I4 | Escrita via `INSTEAD OF` trigger com **guard de tenant** (`auth.role() <> 'service_role' AND NEW.user_id <> auth.uid()` → `RAISE 42501`) + `SET search_path = ''` | `20260602130000` (user_api_keys) · `20260602150000` (meta/social) |
| I5 | Views `decrypted_*` (valor em claro) são `REVOKE ALL FROM anon, authenticated; GRANT SELECT TO service_role` | `20260601000000:625-632` |
| I6 | `anon` **não** tem grant de escrita nas views (least-privilege) | `20260725120100_revoke_anon_credential_view_writes.sql` |

## 3. Correção recomendada (o que fazer) vs Fallback

- **Recomendado (adotado):** MANTER definer + reforçar/auditar as invariantes I1–I6. Não reescrever.
  Suprimir o lint com este racional documentado, não silenciar cego.
- **Fallback (NÃO adotar sem exigência dura):** virar `security_invoker = true` exigiria (a) reabrir
  RLS nas tabelas-base, (b) column-level grants reexpondo só colunas não-sensíveis, e (c) **perder a
  máscara** — grants escondem coluna mas não reescrevem para `••••`. É mais superfície, não menos.

## 4. Verification gates (rodar ao mexer em qualquer coisa desta camada)

Rodar com 3 identidades: `anon`, `authenticated <A>`, `authenticated <B>` (JWTs via
`scripts/qa/gen-user-jwt.ts`) + `service_role`.

1. **Estado deployado** — owner definer + `security_invoker` ausente + base `SELECT` revogado:
   ```sql
   SELECT c.relname, r.rolname AS owner,
          (SELECT option_value FROM pg_options_to_table(c.reloptions)
           WHERE option_name='security_invoker') AS security_invoker
   FROM pg_class c JOIN pg_roles r ON r.oid=c.relowner
   WHERE c.relname IN ('meta_config','social_accounts','user_api_keys');
   ```
2. **Leitura:** anon → 0 linhas · `<A>` → só as próprias, tokens = `••••` · `<A>` pedindo `<B>` → 0 linhas · service_role → tudo.
3. **Escrita:** `<A>` INSERT com `user_id=<B>` → `42501` · `<A>` no próprio → cifra no Vault · anon INSERT → negado (I6).
4. **Máscara:** reenviar `••••` num UPDATE **não** apaga o segredo (`NULLIF(...,'••••')`).
5. Nenhuma coluna (incl. `metadata`/`pages` jsonb) devolve segredo em claro a `authenticated`.

## 5. Recovery / se algo falhar um gate

- Gate 1 falha (view virou invoker ou base voltou a ter SELECT) → **halt**, reverter a mudança que
  causou o drift; a máscara/tenancy só valem sob definer + base revogada.
- Gate 3 falha (injeção cross-tenant passa) → o guard do INSTEAD OF trigger regrediu → reaplicar
  `20260602130000`/`20260602150000`.
- Rodar `scripts/qa/audit-schema-drift.sh` para provar que o deploy bate com as migrations.

## 6. Success signal

Lint documentado como risco-aceito; os 5 gates de §4 verdes contra o banco vivo; `anon` sem grant de
escrita; `/security-review` limpo em qualquer migration futura desta camada (regra do repo).

---

**A verificar no banco vivo (suposições, não fabricar):** owner das views = `postgres`; RLS
`ENABLE`d nas `*_table` como defense-in-depth (não confirmado no grep — recomendado habilitar
default-deny mesmo com SELECT revogado); `user_id` `NOT NULL` nas tabelas-base.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

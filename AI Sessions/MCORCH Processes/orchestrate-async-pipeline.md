# SOP — Orchestrate Async Content Pipeline (recovery + verification)

> **Lei 2 (Processo Antecipado) + Obstáculo→Síntese.** Selado em 2026-06-03 após o 1º run pago E2E expor que o
> flywheel de conteúdo estava **silenciosamente quebrado em 3 lugares** desde o cutover de chaves (2026-06-01).
> Nenhum run de orquestração completava — todos ficavam presos em `pipeline_runs.status='running'`.

---

## Arquitetura (como o pipeline roda)

```
campaign-run (FR-MH-004)            ─┐  (ou invoke direto)
  └→ orchestrate-content  ───────────┤  JWT do user · cobra ORCHESTRATION_RUN(10) · cria pipeline_run
        └→ async_orchestrate_step RPC ┘  (pg_net net.http_post, Bearer = SB_SECRET_KEY)
              └→ orchestrate-step (service-role only; verify_jwt=false; self-checks Bearer===SB_SECRET_KEY)
                    roda 1 passo · grava pipeline_runs.steps[] · chama async_orchestrate_step p/ o PRÓXIMO passo
                    stepsOrder: article_generation → wordpress_publish → linkedin_post → twitter_thread → knowledge_mesh
                    (filtrado por platforms) · knowledge_mesh finaliza: status = done|error
```

Cada passo é **síncrono dentro do orchestrate-step**, mas o **encadeamento entre passos é assíncrono** via a RPC
`async_orchestrate_step` → pg_net → nova invocação do `orchestrate-step`. Se qualquer elo desse encadeamento quebra,
o `pipeline_run` **fica preso em `running` com `steps[]` vazio ou parcial** — e **não há auto-refund** (os mco já saíram).

---

## Os 3 modos de falha (cutover de chaves 2026-06-01) — assinatura material + fix

| # | Sintoma material | Causa raiz | Fix |
|---|---|---|---|
| **1** | run preso `running`, `steps[]` **vazio**; orchestrate-step inalcançável | `orchestrate-step` **faltava** em `config.toml` → default `verify_jwt=true` → o gateway tenta verificar a chave opaca `sb_secret_` como JWT → **401** | adicionar `[functions.orchestrate-step] verify_jwt=false` + `npx supabase functions deploy orchestrate-step` |
| **2** | run preso `running`, `steps[]` vazio/parcial; RPC dá **PGRST202** | drift não-commitado: a RPC em prod tinha o param `p_service_jwt_legacy`, mas os edge fns chamam `p_service_key` → named-arg não resolve → dispatch no-op | migration `20260603190000`: realinha p/ `p_service_key` + `GRANT EXECUTE TO service_role` (dropa overloads) |
| **3** | `wordpress_publish=error` ("Failed"); `wp=None`; `content_mesh_asset=skipped` | `wp_site_url` **não-canônica** (ex.: `mcorch.com` → 301 → `www.mcorch.com`) → `fetch` rebaixa **POST→GET** → WP devolve a **LISTA** de posts (array) → sem `post_url`/`id` | usar a URL **canônica** (`https://www....`) no card WordPress; `publish-wordpress` agora valida `wpData.id` e retorna **502 honesto** (não `success:true` falso) |

**Regra geral (anticorpo):** **toda** edge function invocada por **pg_net** (server-to-server com a chave `sb_secret_`)
DEVE estar `verify_jwt=false` em `config.toml` (ela se auto-autentica no código). E **o nome dos params de uma RPC é
contrato** com os edge fns que a chamam — renomear em prod sem atualizar os callers (e sem migration) quebra o pipeline.

---

## Operator / Sequence / Verification / Recovery / Success

- **Operator** — MCORCH Agent (deploy/migration); **Reviewer/Owner** — Sovereign (mudança outward em prod).
- **Sequence de verificação após qualquer mudança no pipeline ou nas chaves:**
  1. **RPC contrato:** `POST /rest/v1/rpc/async_orchestrate_step` com `p_service_key` (run bogus) → **HTTP 204** (não PGRST202).
  2. **Auto-chain E2E:** `invoke('orchestrate-content', {topic, platforms:['linkedin']})` com JWT real → poll `pipeline_runs` →
     deve chegar a **`status='done'`** com `linkedin_post=done · knowledge_mesh=done` **sem nenhum kick manual**.
  3. **WordPress:** `publish-wordpress` retorna `post_url` (não `{"success":true}` pelado); ou 502 com `code:no_post_returned`
     se a URL não for canônica.
- **Verification gates (materiais):** 204 na RPC · `pipeline_runs.status='done'` autônomo · `post_url` presente.
- **Recovery (run preso `running`):** dirigir os passos manualmente por **kick direto** no `orchestrate-step`
  (`POST /functions/v1/orchestrate-step` com `apikey` + `Authorization: Bearer $SB_SECRET_KEY`, body `{run_id, step}`),
  na ordem `stepsOrder` filtrada por `platforms`. Sem auto-refund → se o run morrer sem produzir, estornar manualmente
  via `mcoin_transactions` (padrão `refund:<run>_<motivo>`) + creditar `profiles.mco_balance`.
- **Success signal:** um `orchestrate-content` fresco se auto-completa a `done` sem intervenção; conteúdo em
  `content_library`; `scheduled_posts` enfileirados; nós `observation`/`content_mesh_asset` na malha.

---

## Gotchas de QA

- **JWT de user p/ chamar edge fns logadas:** `bun run scripts/qa/gen-user-jwt.ts <email>` (admin generateLink → verifyOtp → access_token).
- **`UID` é readonly no bash** — use outra variável (`UZ`) p/ o user_id (senão vira `1001`).
- **`scheduled_posts.status` é enum `post_status`** (não aceita `'draft'`); p/ **segurar** um post sem publicar, adie
  `scheduled_at` p/ o futuro (o cron `auto-publish` só pega `status='queued' AND scheduled_at <= now`).
- Nunca ecoar valores de `SB_SECRET_KEY` no output (use `${v:+SET}`, não `${v:-...}`).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

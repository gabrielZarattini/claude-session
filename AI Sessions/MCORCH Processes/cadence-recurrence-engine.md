# SOP: Spaces Cadence — Motor de Recorrência (Fatia 1) (`cadence-recurrence-engine`)

**Status:** ACTIVE · v1.0 · 2026-07-15
**Owner:** Sovereign (Gabriel Zarattini)
**Survival Law 2 compliance:** Escrito **ANTES** de qualquer linha de código do motor de recorrência da **Fatia 1** do `spaces-cadence`. Abre o gate Lei 2 declarado em toda a suíte BoK (`docs/bok/spaces-cadence/{04-frd,05-sdd,06-data-model,07-process-flow}.md > "SOP Lei 2 (docs/processes/spaces-cadence.md) permanece ABERTO — pré-requisito antes de qualquer código"`). Cobre `cadence-plan` (arm) → tick roteando por `plan_kind` → `cadence-run` (drain + gate chain + dispatch + ledger + re-arm) → `auto-publish` drena.
**SSOT (Lei 1 — Fonte da Verdade):** `docs/bok/spaces-cadence/05-sdd.md` (design/contratos/migration stubs) · `06-data-model.md` (tabelas/RLS/índices) · `07-process-flow.md` (fluxos PROC-CAD-01..05 + recovery) · `04-frd.md` (FR-CAD-001..018 + critérios materiais). **Nada neste SOP inventa coluna/RPC que a SDD/data-model não declara** — onde falta, há `TODO` explícito citando o FR.
**Canonical directive:** `CLAUDE.md > "MCORCH MASTER EXECUTION PROTOCOL"` + `"API Tenancy Model — Per-User Credentials"` · `.claude/rules/survival.md > Law 1 (Materiality) / Law 2 (Anticipated Process) / Law 4 (ORO)`.
**Sibling SOPs (moldes vivos — não reinventar):** `autopilot-cron-identity.md` (gate `Bearer SB_SECRET_KEY` in-function + `user_id` server-trusted da LINHA + pré-débito/refund atômico) · `edge-jwt-identity-verification.md` (`verify_jwt=false` → ES256 JWKS, nunca `atob` cego) · `orchestrate-async-pipeline.md` (`pg_net → verify_jwt=false` + contrato de param-name dos RPCs) · `mcoin-cost-calibration.md` (4×-floor) · `channel-reshaper.md` (contrato do sink `scheduled_posts.metadata.reshape`).

---

## Context

A Fatia 1 do `spaces-cadence` entrega o **motor de cadência de publicação recorrente**: um plano armado pela UI (nó Cadência do Canvas Studio) que, a cada janela, **enfileira** um asset já existente do tenant em `scheduled_posts`, respeitando quiet-hours no fuso do sujeito, frequency-cap por canal e idempotência anti-double-post. O motor é **Postgres-first** (pg_cron + `next_run_at` + índice parcial due) — o mesmo padrão que o MCORCH já roda em produção para o Viral Autopilot e para o `nurture-cron`. A Cadência **encaixa nos trilhos vivos** e **não reconstrói distribuição** (mandato de integração da SDD §1):

- **Estende** `autopilot_plans` (`plan_kind='cadence'`) — não cria tabela de plano paralela (OTD-CAD-003).
- **Reusa** o tick vivo `autopilot-cadence-cron` (`*/15` GMT), que passa a **rotear** por `plan_kind` — **nenhum job pg_cron novo** (FR-CAD-004 · NFR-CAD-012).
- **Enfileira** no sink one-shot `scheduled_posts`; quem publica é o `auto-publish` (que na Fatia 0 migrou para pg_cron + `FOR UPDATE SKIP LOCKED` — FR-CAD-018).

**Riscos materiais que este ritual endereça:**

1. **Double-post / flood (FM-CAD-01/03).** Tick sobreposto ou retry pode enfileirar o mesmo `(plan_id, step_index, occurrence_at)` duas vezes. O único mecanismo que impede isso é o **índice único PARCIAL** `WHERE status <> 'failed'` sobre `cadence_dispatches.idempotency_key` (falha **libera** a chave = retry; sucesso **prende** = anti double-post). É o predicado — e só ele — que garante a idempotência (FR-CAD-003).
2. **Identidade do caminho cron (SEC crítico).** `cadence-run` roda com `verify_jwt=false`; o cron não tem JWT de usuário. Confiar num `user_id` do body deixaria qualquer chamador drenar/publicar na conta de qualquer vítima. O `user_id` **tem** que vir da **LINHA** de `autopilot_plans` drenada, nunca do request (molde `autopilot-cron-identity.md`).
3. **Fuso vira cron expression (FM-CAD-06).** pg_cron roda em **GMT**. Se a preferência de horário do usuário virar uma cron expression, o disparo sai na hora errada em metade do ano (DST). O horário do sujeito é convertido para **UTC** e gravado em `next_run_at`; o cron nunca carrega preferência de horário.
4. **Falso-sucesso "enviado" (FM-CAD-05, Lei 1).** `cadence-run` só **enfileira** (retorna cedo); nunca declara `sent`. A transição para `sent` é responsabilidade da reconciliação por webhook de status (PROC-CAD-05), nunca do 202 de aceite.

**Regra-mãe:** o motor de recorrência é idempotente por construção (índice parcial + `ON CONFLICT DO NOTHING`), com identidade derivada da linha do banco, re-arm computado em UTC, e a cadência **enfileira mas não publica**. Re-rodar o tick sobre o mesmo dado produz o mesmo resultado.

---

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (autoria das migrations `20260716120000/120100` + edges `cadence-plan`/`cadence-run` + roteamento in-place em `autopilot-cadence-cron`) + `pg_cron` apresentando a `SB_SECRET_KEY` (execução por tick) + Edge runtime Deno (gate por request).
- **Reviewer:** Sovereign (Gabriel) — aprova cada migration via `/security-review` independente (mandato `CLAUDE.md`, FMEA-011) + valida os smokes zero-custo re-executáveis (`smoke-cadence-idempotency.ts`, `smoke-cadence-run.ts`, `smoke-cadence-arm-utc.ts` — FRD §6).
- **Owner:** Sovereign — blast radius material: **ban de app Meta/X** (spam de 1 tenant no app global bane todos — OTD-CAD-018) + **sanção ANPD até 2% do faturamento** (LGPD Art. 52) + carteira do tenant gasta em `scheduled_posts` fora de política.

---

## Escopo deste SOP (Fatia 1)

**In scope:** o loop `cadence-plan → tick(plan_kind) → cadence-run → auto-publish`, com sujeito = **asset existente** (`creative_assets.id` owner-scoped, 0 mco, keyless — OTD-CAD-002=A), canais = allowlist do `auto-publish` **MENOS X** (OTD-CAD-011).

**Out of scope (não codar aqui):** FR-CAD-012/013 (inbox IG, `[PROBE-GATED]` — PROC-CAD-07); FR-CAD-014 (Telegram/Resend BYOK, Fatia 3 — PROC-CAD-08); geração de mídia por ciclo (begin/finalize — fatia futura, OTD-CAD-002=A já decidiu asset existente). A **Fatia 0** (FR-CAD-015..018) é **pré-requisito** já coberto pelos seus próprios gates (PROC-CAD-00) — este SOP assume os 6 gates da Fatia 0 verdes antes do primeiro `cadence-plan`.

---

## Operator (equivalente manual — material, Lei 2)

A automação substitui o ritual humano que o Sovereign executaria **hoje, à mão**, a cada janela, para cada plano de cadência ativo. Se o humano não consegue executar sem erro, a IA também não conseguirá — só falhará mais rápido e em escala.

| # | Passo manual (humano) | Comando/UI | Critério de sucesso material |
|---|-----------------------|------------|------------------------------|
| 1 | Abrir o Canvas Studio, configurar recorrência (freq/dias/hora/fuso), canais e `budget_cap_mco` no nó Cadência; ver o custo projetado em mco antes de armar | `/dashboard/spaces` → nó Cadência → CadenceInspector | Custo projetado renderizado em `--gold` **antes** do botão Armar (FR-CAD-011) |
| 2 | Armar o plano | clique **Armar** | `plan_id` (UUID) retornado por `SELECT`; `plan_kind='cadence'`; `next_run_at` em UTC coerente com a recorrência; `mco_balance` **inalterado** (0 débito) |
| 3 | A cada janela, listar os planos cujo `next_run_at` venceu | (o tick faz isso) | Lista de `plan_id` vencidos com `is_active=true` |
| 4 | Para cada plano vencido: conferir fuso/quiet-hours, quantas vezes já publicou hoje no canal (frequency-cap), e se o sujeito ainda pertence ao dono | (gate chain do `cadence-run`) | Fora de quiet-hours; abaixo do teto de `channel_profiles.cadence`; asset owner-scoped |
| 5 | Enfileirar **uma** publicação por ocorrência (não empilhar), gravar no ledger e re-armar a próxima janela | (dispatch + ledger + re-arm) | 1 linha `scheduled_posts` (queued) + 1 linha `cadence_dispatches`; `next_run_at` avança em UTC |
| 6 | O drenador publica os agendamentos vencidos | (o `auto-publish` faz isso) | `scheduled_posts.status` → `published`; webhook de status reconcilia `sent` (nunca o 202) |

---

## Sequence (steps numerados — cada um com critério de sucesso material, Lei 1)

### STEP 0 — Pré-requisitos (gates da Fatia 0 já verdes)

Antes do primeiro `cadence-plan`, os 6 gates de PROC-CAD-00 (FR-CAD-015..018) devem estar verdes: `whatsapp-webhook` alcançável + `timingSafeEqual`; `estimateNodeCost` com `case 'publishSocial'`; `erase_lead()` cascata; `auto-publish` em pg_cron + `FOR UPDATE SKIP LOCKED`. Além disso, a migration `20260716120000_cadence_extend_autopilot_plans.sql` e a `20260716120100_cadence_dispatches.sql` (SDD §7.1/§7.2) aplicadas e com `/security-review` **NO FINDINGS**.

- **Critério material:** `\d autopilot_plans` lista as 9 colunas novas (`plan_kind`, `recurrence`, `quiet_hours`, `overlap_policy`, `catchup_window`, `jitter_seconds`, `program`, `channel_allowlist`, `budget_cap_mco`) com os defaults/CHECK exatos; a constraint `autopilot_plans_platforms_check` **não** existe mais; `pg_indexes` mostra `cadence_dispatches_idem` com predicado `WHERE (status <> 'failed'::text)`; um `INSERT` do cliente (user role) em `cadence_dispatches` é **negado** por RLS (FR-CAD-002/003).

### STEP 1 — Armar o plano (`cadence-plan` — FR-CAD-005, PROC-CAD-01)

Edge fn `cadence-plan` (shape molde `autopilot-cadence-cron`/`canvas-execute`: CORS `OPTIONS`, `verify_jwt=false` no `config.toml`). Sequência in-function:

1. **CORS** — `OPTIONS` → `200 "ok"` com headers.
2. **Identidade** — verificar o JWT do usuário via **ES256 JWKS** (SOP `edge-jwt-identity-verification.md`; teste `scripts/qa/test-es256-jwt-verification.ts`). **NUNCA `atob` cego.** `userId = claims.sub` (server-trusted da claim, nunca do body). Falha → `401`.
3. **Validação** (todas → `422 {error, field, message /* pt-BR */}`): `budget_cap_mco` presente e `> 0`; `recurrence` bem-formada; `recurrence.minutes % 5 === 0` (semântica Knock); cada canal de `channel_allowlist` ⊆ allowlist do `auto-publish` **MENOS X** (Fatia 1); `sourceAssetId` presente.
4. **Resolução do fuso** — cascata `recurrence.tz → profiles.timezone → 'America/Sao_Paulo'` (ressuscita `profiles.timezone` como SSOT — 1º leitor, FR-CAD-007).
5. **Computar `next_run_at` em UTC** a partir de `recurrence {frequency, days, hours, minutes, tz}` (calculador UTC generalizado — STEP 5 abaixo é o mesmo motor).
6. **Upsert** em `autopilot_plans` com `plan_kind='cadence'`, `user_id=userId`, `is_active=true`, `next_run_at`, e as colunas de recorrência/quiet_hours/program/channel_allowlist/budget_cap_mco. RLS owner-scoped **preservada** (nenhuma policy recriada).
7. **Resposta 200** `{ plan_id, next_run_at /* ISO UTC */, projected_cost_mco }`. `projected_cost_mco = Σ(custo mco por canal × ocorrências até o cap)` — **projeção**, obrigação compensatória do quote=0. **0 mco debitado** (G7 é invariante do ciclo, não do nó — nenhum `deduct_mco_coins` aqui).
8. **Telemetria** — `infra_health_logs` `{ service:'spaces-cadence', status:'ok', event:'cadence_plan_armed' }`.

- **Critério material:** POST válido → `plan_id` UUID; `SELECT id, plan_kind, next_run_at FROM autopilot_plans WHERE id=<plan_id>` mostra `plan_kind='cadence'` + `next_run_at` UTC coerente com a recorrência; JWT forjado/ausente → 401; `SELECT mco_balance FROM profiles WHERE id=<user>` **idêntico** antes/depois (0 débito). O inspector faz poll no **molde `useVoiceRenderPoll`** (id no `data` do nó, sobrevive a refresh — nunca `sleep(8s)×25`; NFR-CAD-014).

> **TODO (Lei 1):** o `sourceAssetId` da Fatia 1 é `creative_assets.id`. A SDD (§4 `CadencePlanRequest`) declara o campo; o gate de ownership (o asset pertence ao `userId`) roda no `cadence-run` STEP 3 (resolve subject owner-scoped), não no arm. Se a implementação quiser validar ownership já no arm, é um `SELECT` owner-scoped adicional — **não** inventar coluna nova.

### STEP 2 — Tick roteia por `plan_kind` (`autopilot-cadence-cron` — FR-CAD-004, PROC-CAD-02)

**Extensão in-place** do tick vivo `autopilot-cadence-cron` (`*/15` GMT). **Nenhuma função nova, nenhum job pg_cron novo.**

1. **Gate cron** — `Authorization === Bearer SB_SECRET_KEY` (via `SB_SECRET_KEY ?? SUPABASE_SERVICE_ROLE_KEY`), senão `403`. (Já implementado — linha viva.)
2. **Drain due** — `SELECT id, user_id, plan_kind FROM autopilot_plans WHERE is_active AND next_run_at <= now() ORDER BY next_run_at LIMIT MAX_PER_RUN` (índice parcial `autopilot_plans_due_idx` reusado). **`plan_kind` entra no select** (hoje o select é `id, user_id` — a extensão adiciona `plan_kind`).
3. **Roteamento** — para cada linha, `target = plan.plan_kind === 'cadence' ? 'cadence-run' : 'autopilot-run'`. Fan-out **bounded** (`MAX_PER_RUN=50`, `CONCURRENCY=6` — já constantes vivas). `user_id` **server-trusted da LINHA** repassado via header/body confiável (molde `x-autopilot-user-id`), nunca de um request externo.
4. **Invoke** — `POST ${url}/functions/v1/${target}` com `Authorization: Bearer ${serviceKey}` + `{ plan_id: plan.id }`.

- **Critério material:** `SELECT count(*) FROM cron.job` **inalterado** antes/depois da entrega (0 job novo — NFR-CAD-012); log do tick mostra dispatch a `cadence-run` para linhas `plan_kind='cadence'` e a `autopilot-run` para `'viral'`; POST ao tick sem `Bearer SB_SECRET_KEY` → `403`; regressão do autopilot (`plan_kind='viral'`) permanece verde.

### STEP 3 — `cadence-run` drena, aplica gate chain e enfileira (FR-CAD-006, o coração, PROC-CAD-03)

Edge fn nova `cadence-run` (shape molde `autopilot-run`: CORS, `verify_jwt=false`, cliente service-role). **Auth:** `Authorization === Bearer SB_SECRET_KEY` senão `403`. `user_id` **server-trusted da LINHA** de `autopilot_plans` (nunca do body — SOP `autopilot-cron-identity.md`). Sequência:

1. **DRAIN** — `SELECT ... FROM autopilot_plans WHERE id=<plan_id> AND plan_kind='cadence' AND is_active FOR UPDATE SKIP LOCKED`. Se 0 linhas (outro consumidor pegou / não vencido) → NO-OP. Evita contenção multi-consumer.
2. **OVERLAP** — `overlap_policy='skip'`: se o ciclo anterior deste plano ainda roda, **pula** (não empilha) e re-arma a janela seguinte (FM-CAD-01).
3. **RESOLVE SUBJECT owner-scoped** — `SELECT id FROM creative_assets WHERE id=<sourceAssetId> AND user_id=<row.user_id>`. Se o asset não pertence ao dono da linha → **HALT** + `infra_health_logs`. (Fatia 1 = asset existente ⇒ 0 mco, keyless — OTD-CAD-002=A.)
4. **GATE CHAIN — server-side, NUNCA LLM** (ordem exata da SDD §3.2 / PROC-CAD-03):
   - **quiet_hours** — janela `[start,end]` + weekdays no **fuso do sujeito** (cascata `recurrence.tz → profiles.timezone → 'America/Sao_Paulo'`). Dentro da janela → **HALT** (suprime, **não** reenfileira — semântica Knock) + `infra_health_logs event:'cadence_halt_quiet_hours'` (FR-CAD-008).
   - **frequency_cap** — chave `(user_id, channel)` (OTD-CAD-017=A na Fatia 1) vs teto autoritativo `channel_profiles.cadence` (`target_per`/`count_min`/`count_max` — 1º leitor, OTD-CAD-008=A). Estourou o teto na janela → **HALT** (não reenfileira) + toast pt-BR informativo + `event:'cadence_halt_freq_cap'` (FR-CAD-008).
   - **opt-out** — `withdrawn_at` checado **NO SEND**, independente da base legal → revogado → **HALT** + cascata (G3/G8 · FM-CAD-04).
   - **jurisdição** — lead sem país conhecido ⇒ tratar como **UE (opt-in prévio, fail-closed)**; Brasil = `consent` fail-closed (G11 · OTD-CAD-015).
   - **dedup/digest** — `digestKey = (user, channel, dia)` colapsa N vencimentos do mesmo canal no mesmo dia em **1** publicação (FR-CAD-009 — a diferença estrutural entre cadência e flood).
   - **A/B determinístico** — bucket = `mod(abs(hashtext(subject_ref || ':' || experiment_key)::bigint), 100) < ratio`. **Cast `bigint` ANTES do `abs`** (`abs(int4min)` estoura); **proibido** `hashtext(...) % 100` (integer com sinal enviesa ~50% em silêncio) e **proibido** `random()` (instável entre retries) — FR-CAD-010.
5. **DISPATCH** — `INSERT scheduled_posts` (o nó **enfileira, não publica**) com o contrato do sink `metadata.reshape`. Ver **TODO do contrato do sink** abaixo. Data inválida → 422; double-enqueue → 409.
6. **LEDGER** — `INSERT cadence_dispatches (user_id, plan_id, step_index, occurrence_at, idempotency_key, channel, status='queued', target_ref) ... ON CONFLICT DO NOTHING RETURNING id`, onde `idempotency_key = hash estável de (plan_id, step_index, occurrence_at)` sob o índice único parcial `WHERE status<>'failed'`. Conflito (0 linhas) ⇒ **já despachado neste occurrence: NO-OP anti double-post** (FR-CAD-003 · FM-CAD-01).
7. **RE-ARM** — `next_run_at ← próximo horário em UTC` (calculador `{frequency, days, hours, minutes, tz}` — o mesmo motor do STEP 1.5) **OU** `is_active=false` se fim de `program`. `UPDATE autopilot_plans SET next_run_at=<next> WHERE id=<plan_id> AND user_id=<row.user_id>` (molde `autopilot-run/index.ts:314`).
8. **MESH** — no **1º ciclo bem-sucedido** do plano, `INSERT mcorch_nodes` (`node_type='observation'`) + `embed-mcorch-node` (system key `MESH_EMBED_*`, não BYOK — fluxo de sistema sem `auth.uid()`). Mesh Connection Mandate / Pattern P8.
9. **RECONCILE (assíncrono, desacoplado)** — `cadence_dispatches.status='sent'` + `external_usd_cost` + `cost_source` **só** a partir do webhook de **status** da plataforma (PROC-CAD-05), **NUNCA** do 202 (FM-CAD-05, Lei 1). Fora do escopo desta fn síncrona.

- **Critério material:** 1 plano vencido → **1** linha `cadence_dispatches` + **1** linha `queued` em `scheduled_posts` (UUIDs por `SELECT`); tick sobreposto/retry → **0** 2º dispatch para o mesmo `(plan_id, step_index, occurrence_at)` (smoke `smoke-cadence-idempotency.ts` re-executável); **nenhuma** linha `sent` a partir de 202; `next_run_at` avança em UTC; dispatch em quiet-hours no fuso do sujeito → **0** linha em `scheduled_posts`; dispatch acima do teto de `channel_profiles.cadence` → **HALT** (0 publicação, não reenfileira).

> **TODO (Lei 1 — contrato do sink):** a SDD/FRD descrevem o contrato do sink como `metadata.reshape + schedule:true + publish_at ISO` (Amendment 22). O `scheduled_posts` **vivo** (`reshape-pillar/index.ts:482`) insere `{ user_id, content_id:null, campaign_id, social_account_id:null, platform, scheduled_at: <ISO>, status:'queued', metadata:{ reshape:{...} } }` — usa a coluna **`scheduled_at`** e `status:'queued'`, **não** um campo `publish_at`/`schedule:true`. Na implementação, **confirmar contra Amendment 22 e o schema vivo de `scheduled_posts`** qual é o nome de coluna canônico do horário de publicação (`scheduled_at` vs `publish_at`) e alinhar o INSERT ao shape vivo. Não inventar coluna nova — reusar exatamente o INSERT de `reshape-pillar`/`publish-space-asset`.

> **TODO (Lei 1 — contador de janela do frequency-cap):** a FRD §2.1 (FR-CAD-008) nota que "o contador de janela **não existe hoje** (a SDD deve criá-lo)". O teto vem de `channel_profiles.cadence`, mas a **contagem** de publicações na janela precisa de uma fonte. A implementação deve derivá-la de `cadence_dispatches` (`count WHERE user_id/channel AND occurrence_at na janela AND status<>'failed'`) — **confirmar** que essa é a fonte pretendida pela SDD antes de codar; se a SDD selar outra coluna, seguir a SDD. Não inventar tabela de contador.

### STEP 4 — `auto-publish` drena e publica (FR-CAD-018, PROC-CAD-04)

`auto-publish` (migrado para pg_cron + `FOR UPDATE SKIP LOCKED` na Fatia 0) drena `scheduled_posts` de forma **desacoplada** do `cadence-run`. A cadência **não toca na lógica de publicação** — só a alimenta.

1. `SELECT ... FROM scheduled_posts WHERE status='queued'/'pending' AND scheduled_at <= now() FOR UPDATE SKIP LOCKED LIMIT <batch>` (dois runs concorrentes nunca reivindicam a mesma linha).
2. Resolve o asset owner-scoped **na hora** (`metadata.reshape`) e publica via o seam existente (`reshape-pillar` / `publish-space-asset` / `publish-space-carousel`).
3. Sucesso → `status='published'` (a plataforma emitirá o webhook de status → PROC-CAD-05). Erro → retry por contagem com backoff (molde `auto-publish:200-212`); esgotou → `status='failed'` + `infra_health_logs`.

- **Critério material:** `SELECT jobname FROM cron.job WHERE command ILIKE '%auto-publish%'` ≥1 linha; a claim contém `FOR UPDATE SKIP LOCKED`; smoke de concorrência = **0** double-publish (FM-CAD-01).

### STEP 5 — Calculador de re-arm UTC (`{frequency, days, hours, minutes, tz}` — FR-CAD-007)

Motor compartilhado por STEP 1.5 (arm inicial) e STEP 3.7 (re-arm). Generaliza `autopilot-run:310-314` (`now + interval_days`) para um calculador que: interpreta `days` como weekdays (1=Mon) para `weekly` ou dias do mês para `monthly`; aplica `hours`/`minutes` no fuso `tz`; **converte para UTC** e grava em `next_run_at`. O cron **nunca** carrega preferência de horário.

- **Critério material:** teste unitário `smoke-cadence-arm-utc.ts` — dado `recurrence {frequency:'weekly', days:[1,3,5], hours:9, minutes:0, tz:'America/Sao_Paulo'}`, o `next_run_at` corresponde à próxima 2ª/4ª/6ª 09:00 BRT **convertida para UTC** (12:00Z fora do DST); cobre GMT vs. fuso do usuário (FM-CAD-06); `grep` prova `profiles.timezone` com ≥1 leitor.

---

## Verification gates (consolidado — todos materiais, Lei 1)

| Gate | Verificação | Passa quando |
|------|-------------|--------------|
| **G-ARM** | `POST cadence-plan` válido → `SELECT` da linha | `plan_id` UUID · `plan_kind='cadence'` · `next_run_at` UTC · `mco_balance` inalterado (0 débito) |
| **G-AUTH-PLAN** | JWT forjado/ausente em `cadence-plan` | `401` (ES256 JWKS falha; nunca `atob` cego) |
| **G-AUTH-RUN** | POST a `cadence-run`/tick sem `Bearer SB_SECRET_KEY` | `403` |
| **G-CRON-INVARIANT** | `SELECT count(*) FROM cron.job` antes/depois da entrega | **inalterado** (0 job novo — NFR-CAD-012) |
| **G-ROUTE** | Log do tick por `plan_kind` | `cadence` → `cadence-run` · `viral` → `autopilot-run` |
| **G-IDEMPOTENCY** | `smoke-cadence-idempotency.ts`: 2 ticks sobre o mesmo occurrence | **0** 2º dispatch para `(plan_id, step_index, occurrence_at)`; `ON CONFLICT DO NOTHING` retorna 0 linhas |
| **G-INDEX** | `pg_indexes` de `cadence_dispatches_idem` | predicado `WHERE (status <> 'failed'::text)` presente |
| **G-RLS** | INSERT do cliente (user role) em `cadence_dispatches` | **negado** por default-deny (só SELECT own) |
| **G-QUIET** | Dispatch em quiet-hours no fuso do sujeito | **0** linha em `scheduled_posts`; `event:'cadence_halt_quiet_hours'` |
| **G-FREQCAP** | Dispatch acima do teto `channel_profiles.cadence` | **HALT** (0 publicação, não reenfileira); `channel_profiles.cadence` com ≥1 leitor (grep) |
| **G-UTC** | `smoke-cadence-arm-utc.ts` | `next_run_at` = próxima ocorrência convertida para UTC |
| **G-SENT** | Auditoria de reconcile | **nenhuma** linha `sent` sem webhook de status casado (nunca do 202) |
| **G-SKIPLOCK** | `auto-publish` claim + smoke de concorrência | contém `FOR UPDATE SKIP LOCKED`; **0** double-publish |
| **G-SECREVIEW** | `/security-review` de cada migration | **NO FINDINGS** (FMEA-011) |

---

## Recovery path (falha no step N — nunca "tente de novo" vago)

| Falha | Sintoma | Recuperação exata |
|-------|---------|-------------------|
| **`cadence-plan` 401/422** | Arm rejeitado | Corrigir JWT (ES256) ou o campo apontado no `422` (`budget_cap_mco`, `minutes%5`, canal fora da allowlist); reenviar. Nenhum estado persistido (upsert não ocorreu). |
| **Dispatch transitório (provider 5xx / timeout no `cadence-run`)** | Ciclo não completou | Gravar `cadence_dispatches.status='failed'` ⇒ o índice parcial **libera** a `idempotency_key` ⇒ o próximo tick (`*/15`) **retenta** o mesmo `occurrence_at` (at-least-once — OTD-CAD-006=A). Backoff por contagem (molde `auto-publish:200-212`). |
| **Backlog storm** (queda de N horas) | Muitos vencimentos atrasados de uma vez | `catchup_window` (default `'6 hours'`) **limita** quantos vencimentos atrasados disparam; `jitter_seconds` espalha o fan-out; fan-out bounded (`MAX_PER_RUN=50`/`CONCURRENCY=6`) — FM-CAD-07. |
| **Tick sobreposto** | Risco de double-post | `overlap_policy='skip'` (ciclo anterior rodando ⇒ pula) + `ON CONFLICT DO NOTHING` sob índice parcial ⇒ 0 double-post. pg_cron não sobrepõe a mesma job. |
| **Feedback negativo acima do limiar** | Risco de ban de app | Kill-switch: `is_active=false` no plano (limiar conservador auto-imposto — FM-CAD-14) **para** o drain daquele plano no próximo tick. |
| **`auto-publish` 5xx da plataforma** | Publicação falhou | retry por contagem (`retry_count+1`, backoff); esgotou → `status='failed'` + `infra_health_logs`. |
| **Webhook de status ausente** (`> SLA` do provider) | Dispatch órfão sem reconcile | Reconciliação por **poll** (molde do poll de `video_renders`) reconcilia o órfão; **nunca** declarar `sent` por timeout (isso seria o falso-sucesso do 202 — FM-CAD-05). |
| **Eliminação LGPD chega após enqueue** | Agendamento sobrevive ao erase | `erase_lead()` cascata (Fatia 0, FR-CAD-017) cancela `scheduled_posts` pendentes + marca `cadence_dispatches` `status='failed', error='erased'` **na mesma transação**; `withdrawn_at` checado no send independente da base legal (G9 · FM-CAD-04). |
| **Migration reprovada no `/security-review`** | FINDINGS | Corrigir e re-submeter; **nenhuma** migration commitada com FINDINGS (FMEA-011). |

---

## Success signal (materialmente observável — o flow completo funciona)

O ciclo de cadência está **materialmente** funcionando quando, para um plano `plan_kind='cadence'` armado com `next_run_at` vencido:

1. `SELECT` mostra **1** linha nova em `cadence_dispatches` (`status='queued'`, `idempotency_key` gravada) **e** **1** linha nova `queued` em `scheduled_posts` (`metadata.reshape` presente) — UUIDs reais retornados;
2. re-rodar o tick sobre o mesmo occurrence **não** cria um 2º dispatch (`ON CONFLICT DO NOTHING` → 0 linhas; smoke `smoke-cadence-idempotency.ts` verde);
3. `next_run_at` avançou para a próxima ocorrência **em UTC** coerente com a `recurrence`;
4. o `auto-publish` drenou a linha (`scheduled_posts.status='published'`) e a reconciliação por webhook de status marcou `cadence_dispatches.status='sent'` + `external_usd_cost`/`cost_source` — **nunca** a partir do 202;
5. `SELECT count(*) FROM cron.job` permaneceu **inalterado** (0 job pg_cron novo);
6. um nó de observação foi inserido em `mcorch_nodes` no 1º ciclo bem-sucedido; toda falha registrou `infra_health_logs` (`service='spaces-cadence'`).

---

## Survival Laws Self-check (SOP-time)

- **Lei 1 (Materiality):** cada STEP e cada gate carrega critério material (UUID / HTTP status / `count(*)` / `pg_indexes` predicado / grep / smoke). `sent` só do webhook de status (STEP 3.9 / G-SENT); idempotência pelo índice parcial (G-IDEMPOTENCY). Este SOP **não** declara sucesso — descreve o processo antecipado.
- **Lei 2 (Anticipated Process):** este é o SOP que abre o gate Lei 2 do `spaces-cadence` (Operator/Sequence/Verification/Recovery/Success) — pré-requisito antes de qualquer código do motor de recorrência.
- **Lei 3 (Pruning):** N/A em SOP-time.
- **Lei 4 (ORO):** triplet declarado no cabeçalho.

---

_SOP fiel a `docs/bok/spaces-cadence/{04-frd,05-sdd,06-data-model,07-process-flow}.md` (Lei 1 — SSOT). Nenhuma coluna/RPC inventada além da BoK; dois `TODO` explícitos (contrato do sink `scheduled_posts` vs Amendment 22; fonte do contador de janela do frequency-cap) deixados para a implementação selar contra a SDD/schema vivo. Convenções MCORCH: lógica/vars em inglês, UI/toasts pt-BR; BYOK per-user fail-closed 402/501; cobrança só via `deduct_mco_coins`/`begin`/`finalize` atômico (nunca client-side); `verify_jwt=false` → ES256 JWKS (nunca `atob` cego); RLS default-deny owner-scoped; idempotência por índice único parcial. A Cadência ENCAIXA nos trilhos vivos (autopilot · scheduled_posts · channel_profiles · profiles) — nenhum job pg_cron novo (FR-CAD-004)._

# SOP — Intent Plan Execution (HITL approve / reject / execute + outward dispatch)

> **Lei 2 (Processo Antecipado).** Documenta o processo humano da metade HITL do FR-MH-009 (Intent Orchestrator) **e** o disparo outward real (un-gate v6.27.1) **antes** do código. SSOT: `docs/bok/marketing-hub/04-frd.md` FR-MH-009 + `05-sdd.md` (§intent-execute + STRIDE "ação de alto impacto sem revisão = Tampering → policy engine + HITL obrigatório") + `06-data-model.md` (§intent_plans status machine + bindings + transition guard).

## Contexto

`intent-orchestrate` (FR-MH-009) traduz uma intenção em linguagem natural num **plano de tarefas** e roda um **policy engine**: qualquer tarefa de **alto impacto** (publicar / enviar / cobrar / veicular anúncio / canal outward) força `policy='hitl'` + `status='pending_hitl'`; senão `policy='auto'` + `status='auto_approved'`. O plano fica persistido em `intent_plans` com um `rationale` (XAI auditável). Este SOP cobre o que acontece **depois**: aprovar, rejeitar, executar — e, na execução, **disparar a ação outward real**.

Máquina de estados (`intent_plans.status`):

```
proposed ──▶ auto_approved ─────────────────────────▶ executed ──▶ [outward dispatch]
        └──▶ pending_hitl ──▶ approved ─────────────▶ executed ──▶ [outward dispatch]
                          └──▶ rejected  (terminal)
```

## Operator

Quem executa hoje: o **tenant** (Usuário Zero / operador de marketing) revisando os planos no **Marketing Hub** (`/dashboard/marketing`, painel Intent Orchestrator). A decisão HITL é **humana e consciente** — é a salvaguarda contra uma ação outward disparar sem revisão.

## Sequence (cada passo com critério material de sucesso)

| # | Passo | Ação | Critério de sucesso material |
|---|-------|------|------------------------------|
| 1 | **Orquestrar** | Operator descreve a intenção → `intent-orchestrate` | HTTP 200 `{plan_id, policy, plan_status, tasks, rationale}` + linha em `intent_plans` |
| 2 | **Triagem auto** | Se `policy='auto'` (só tarefas low/medium, nenhum canal outward) | `status='auto_approved'` — não exige humano |
| 3 | **Triagem HITL** | Se `policy='hitl'` (≥1 tarefa de alto impacto) | `status='pending_hitl'` — aparece no painel HITL pendente |
| 4 | **Decidir** | Operator clica **Aprovar** ou **Rejeitar** → `intent-execute {decision}` | `status='approved'` ou `'rejected'` (transição validada server-side) |
| 5 | **Executar** | Operator clica **Executar** → `intent-execute {decision:'execute'}` | `intent-execute` **re-valida** o outward; se passa, `status='executed'` **e dispara o canal real** (manifesto `outward_dispatch` + `dispatch[]`) |

## Roteamento do dispatch outward (un-gate v6.27.1)

Após a governança (`status='executed'`), o executor dispara **uma** ação outward real, por precedência das *bindings* do plano, encaminhando o **JWT do chamador** (a cascata fatura o **mesmo tenant** sob RLS):

| Precedência | Condição | Alvo | Custo (self-bill do alvo) |
|-------------|----------|------|----------------------------|
| 1 | `intent_plans.campaign_id` setado | `campaign-run {campaign_id}` | 10 (fee) + 10×N passos |
| 2 | `intent_plans.enrollment_id` setado | `nurture-dispatch {enrollment_id}` | 2 (consent-gated) |
| 3 | senão, ≥1 canal `content`/`affiliate`/`social` nas tarefas | `orchestrate-content {topic: intent, platforms}` | 10 |
| — | nenhum canal outward (só `none`/`email` sem enrollment) | — | `outward_dispatch='none'` (só governança) |

Mapa canal→plataforma (espelha `campaign-run`): `content`→`[wordpress]` · `affiliate`→`[wordpress]` · `social`→`[linkedin,twitter]` · `email`/`none`/desconhecido → território de `nurture-dispatch` (exige `enrollment_id`), **não** servível via `orchestrate-content`.

**Kill-switch (self-protection / self-healing):** `INTENT_OUTWARD_DISPATCH_ENABLED=false` (secret) reverte o executor para **governança-only** (`outward_dispatch='gated'`) sem redeploy — uso em resposta a incidente. Default = `true` (ativo/un-gated).

## Verification gates (defesa-em-profundidade — a regra de ouro)

1. **Transições válidas server-side.** `intent-execute` recusa transições inválidas (`approve` só de `pending_hitl`; `execute` nunca de `rejected`; `executed` é idempotente — **não re-dispara**). Retorna `409` com mensagem PT-BR.
2. **Re-validação no execute (NÃO confiar em `auto_approved`).** O `execute` **recomputa** o high-impact a partir do `plan` armazenado (mesmo gate do `intent-orchestrate`, via `_shared/intent-policy.ts`). Se o plano contém ação de alto impacto **e** `status !== 'approved'`, recusa com `409 {code:'hitl_required'}` — mesmo que a linha diga `policy='auto'`/`status='auto_approved'` (proteção contra mislabel da IA **ou** adulteração direta do registro via PostgREST RLS). FAIL-CLOSED: plano não-array (jsonb adulterado) é tratado como alto impacto.
3. **Tenant guard.** `intent-execute` carrega o plano por `id` **E** `user_id = auth.uid()` (service role + escopo explícito). Plano de outro tenant → `404`.
4. **OTD-INTENT-TRANSITION-GUARD (DB, defesa-em-profundidade).** Trigger `tr_guard_intent_plan_transition` (BEFORE UPDATE, `SECURITY DEFINER`, `search_path=''`) permite que **só o `service_role`** mova `status` para `approved` ou `executed`. Um tenant que tente `PATCH intent_plans?id=eq.X {status:'approved'}` direto via PostgREST (RLS `update_own`) é **bloqueado** (`RAISE EXCEPTION 42501`) — não consegue se auto-aprovar e cavalgar a re-validação até um dispatch real. Tentativa não-autorizada é logada via `RAISE WARNING` no **log do Postgres** (sobrevive ao rollback que o EXCEPTION causa; um INSERT em `infra_health_logs` aqui faria rollback junto com a statement abortada — por isso o forense vai pro server log, não pra tabela).
5. **Binding tenant-validation (DB).** Trigger `tr_validate_intent_plan_bindings` (BEFORE INSERT/UPDATE) exige que `campaign_id`/`enrollment_id` setados pertençam ao `user_id` do plano (`RAISE EXCEPTION 42501`) — em cima do guard de posse já feito pelos próprios `campaign-run`/`nurture-dispatch` no momento do dispatch (entidade alheia → `404`, dispatch inerte).
6. **Outward dispatch é real, mas billing/consent ficam com o alvo.** O executor **não** cobra (custo 0); cada alvo self-bila e aplica seus próprios gates (`orchestrate-content`/`campaign-run` → `402` sem saldo; `nurture-dispatch` → consent gate). Um `402`/`404`/`blocked` vindo do alvo é prova material de que o dispatch **é real** (código gated nunca produziria erro do alvo) e aparece em `dispatch[].http_status`.

## Recovery path (falha no passo N)

- **Transição inválida (409):** o estado não muda; o Operator corrige (ex.: aprovar antes de executar). Nada a fazer no banco.
- **Re-validação bloqueia (409 `hitl_required`):** o plano permanece `pending_hitl`/`auto_approved`; o Operator deve **Aprovar** explicitamente antes de re-executar. Esse bloqueio é o comportamento correto, não um bug.
- **Transition guard bloqueia (42501):** um tenant tentou mover status para approved/executed direto no banco. Comportamento correto (ataque/erro). O estado não muda; revisar o log do Postgres (`intent_plans transition guard: blocked ...`).
- **Dispatch falha pós-execução (`outward_dispatch='failed'`):** o plano JÁ está `executed` (governança feita — idempotência protege contra dobro de cobrança no retry), mas o alvo retornou non-2xx (ex.: `402` sem saldo, `404` binding alheio). O `dispatch[].detail` traz o motivo. O Operator resolve a causa (saldo / binding / consent) e **re-orquestra** um novo plano para disparar de novo — re-executar o mesmo plano retorna `already=true` (não re-dispara). Nota: o `intent-execute` **não cobra** (custo 0), então não há débito a estornar no nível do executor; o refund-on-failure é responsabilidade de cada alvo charge-at-entry (padrão `refundMco` já adotado em `aeo-audit`/`lead-score`; **OTD-INTENT-DISPATCH-REFUND** = aplicar o mesmo padrão ao gap pós-débito do `orchestrate-content`, follow-up do flywheel).
- **Falha de persistência (500):** `infra_health_logs.service='intent-execute' status='unhealthy'`; o status não avança; retry idempotente seguro (a transição é checada de novo).

## Success signal (materialmente observável)

`intent_plans.status='executed'` para o `plan_id` + `outward_dispatch ∈ {dispatched, none}` (com `dispatch[]` mostrando o alvo + `http_status 2xx` quando houve envio) + um nó `observation` no Knowledge Mesh (`intent-exec-<plan_id>`) + `infra_health_logs.service='intent-execute' status='healthy'`. Um plano de alto impacto **só** chega a `executed` se passou por `approved` (humano) — verificável no `created_at`/`updated_at` e no histórico de status, e agora **garantido no nível do banco** pela transition guard.

## ORO

- **Operator:** tenant (humano) no painel HITL · **Reviewer:** o policy engine + re-validação server-side + transition guard (DB) + `/security-review` da migration · **Owner:** Sovereign (blast radius = ação outward + gasto real de mcoCoins disparados pós-aprovação; mitigado pela re-validação fail-closed, pela transition guard service-role-only, pelo gate HITL humano e pelos billing/consent gates dos alvos).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

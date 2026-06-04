# SOP — Intent Plan Execution (HITL approve / reject / execute)

> **Lei 2 (Processo Antecipado).** Documenta o processo humano da metade HITL do FR-MH-009 (Intent Orchestrator) **antes** do `intent-execute`. SSOT: `docs/bok/marketing-hub/04-frd.md` FR-MH-009 + `05-sdd.md` (§intent-execute + STRIDE "ação de alto impacto sem revisão = Tampering → policy engine + HITL obrigatório") + `06-data-model.md` (§intent_plans status machine).

## Contexto

`intent-orchestrate` (FR-MH-009) traduz uma intenção em linguagem natural num **plano de tarefas** e roda um **policy engine**: qualquer tarefa de **alto impacto** (publicar / enviar / cobrar / veicular anúncio / canal outward) força `policy='hitl'` + `status='pending_hitl'`; senão `policy='auto'` + `status='auto_approved'`. O plano fica persistido em `intent_plans` com um `rationale` (XAI auditável). Este SOP cobre o que acontece **depois**: aprovar, rejeitar ou executar o plano.

Máquina de estados (`intent_plans.status`):

```
proposed ──▶ auto_approved ─────────────────────────▶ executed
        └──▶ pending_hitl ──▶ approved ─────────────▶ executed
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
| 5 | **Executar** | Operator clica **Executar** → `intent-execute {decision:'execute'}` | `intent-execute` **re-valida** o outward; se passa, `status='executed'` |

## Verification gates (defesa-em-profundidade — a regra de ouro)

1. **Transições válidas server-side.** `intent-execute` recusa transições inválidas (`approve` só de `pending_hitl`; `execute` nunca de `rejected`; `executed` é idempotente). Retorna `409` com mensagem PT-BR.
2. **Re-validação no execute (NÃO confiar em `auto_approved`).** O `execute` **recomputa** o high-impact a partir do `plan` armazenado (mesmo gate do `intent-orchestrate`, via `_shared/intent-policy.ts`). Se o plano contém ação de alto impacto **e** `status !== 'approved'`, recusa com `409 {code:'hitl_required'}` — mesmo que a linha diga `policy='auto'`/`status='auto_approved'` (proteção contra mislabel da IA **ou** adulteração direta do registro via PostgREST RLS).
3. **Tenant guard.** `intent-execute` carrega o plano por `id` **E** `user_id = auth.uid()` (service role + escopo explícito). Plano de outro tenant → `404`.
4. **Outward dispatch é gated.** Nesta MVP o `execute` faz a **governança** (re-validação + transição + observação no mesh); o disparo real de canal (`campaign-run`/`orchestrate-content`/`nurture-dispatch`) permanece **gated** (igual à entrega externa de nurturing) — o executor devolve o manifesto das tarefas validadas, sem fabricar envio.

## Recovery path (falha no passo N)

- **Transição inválida (409):** o estado não muda; o Operator corrige (ex.: aprovar antes de executar). Nada a fazer no banco.
- **Re-validação bloqueia (409 `hitl_required`):** o plano permanece `pending_hitl`/`auto_approved`; o Operator deve **Aprovar** explicitamente antes de re-executar. Esse bloqueio é o comportamento correto, não um bug.
- **Falha de persistência (500):** `infra_health_logs.service='intent-execute' status='unhealthy'`; o status não avança; retry idempotente seguro (a transição é checada de novo).

## Success signal (materialmente observável)

`intent_plans.status='executed'` para o `plan_id` + um nó `observation` no Knowledge Mesh (`intent-exec-<plan_id>`) + `infra_health_logs.service='intent-execute' status='healthy'`. Um plano de alto impacto **só** chega a `executed` se passou por `approved` (humano) — verificável no `created_at`/`updated_at` e no histórico de status.

## ORO

- **Operator:** tenant (humano) no painel HITL · **Reviewer:** o próprio policy engine + re-validação server-side · **Owner:** Sovereign (blast radius = ação outward disparada sem revisão; mitigado pelo gate de re-validação).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

# SOP: Constellation Economic Activation (CEA)

**Status:** ACTIVE · v1.1 · 2026-05-30 (UI agora lê dados reais — fim do mock `useSimulation`)
**Owner:** Sovereign (Gabriel Zarattini)
**Survival Law 2 compliance:** SOP retroativa (registrada no seal v6.10.0, promovida a `docs/processes/` no mesmo selo per Phase 5c material proof audit).

---

## Context

A Constelação UI (`/dashboard/constellation`) deploya hoje **137 agentes** (53 Sovereign-owned) com schema rico (`crew_agents.provider`, `model`, `system_prompt`, `squad`, `priority`). Antes da v6.10.0 esses agentes eram **visual demo apenas** — `useSimulation.ts` flipava status aleatoriamente client-side, sem chamadas reais a provedores.

CEA introduz o ciclo **real-cost**: agents executam tarefas, consomem tokens reais, registram custo em USD/mcoCoins, e (para users não-Sovereign) debitam o balance. Sovereign opera em modo admin freebie (analytics-only) por design.

A precificação interna de mcoCoins depende de dados acumulados durante 7d+ via cron diário. A `MARGIN_FACTOR` (hoje 2.0 na RPC `calc_agent_cost_mcoin`) será calibrada após esse período.

---

## Operator

- **Cron daemon (ubuntu user):** dispara `scripts/agent-daily-pulse.sh` diariamente às `0 7 * * *` (sistema BRT = 10:00 UTC)
- **Edge function `agent-task-execute`:** executa cada task em isolamento (1 task = 1 row em `agent_executions`)
- **Sovereign manual via UI** (futuro — wire pendente do `NodeDetailsPanel`): dispara tasks ad-hoc

---

## Pre-conditions

| # | Check | Material proof |
|---|---|---|
| 1 | `user_api_keys.groq_api_key` populado para target user | REST GET retorna SET |
| 2 | `crew_agents` rows ativos com `provider` + `model` válidos | REST GET filtered |
| 3 | `agent_pricing` seedado com par (provider, model) usado | RPC `calc_agent_cost_mcoin` returns sem `pricing_not_found` |
| 4 | Migration `agent_metering_minimal` aplicada | Schema cache lista `agent_executions` |
| 5 | Edge function `agent-task-execute` deployed e ACTIVE | `supabase functions list` confirma |

---

## Sequence (execução por ciclo)

### Step 1 — Trigger (cron OR manual)
Cron diário OR edge function direct invoke.

**Cron path** (`scripts/agent-daily-pulse.sh`):
- Loop por todos Directors Sovereign-owned (1 por squad — ops/content/tech/market)
- Para cada: INSERT pending row + chamar Groq direto + UPDATE done

**Edge path** (`POST /functions/v1/agent-task-execute`):
- Body: `{ agent_id, task_prompt, override_provider?, override_model? }`
- Auth: user JWT (RLS) OR service-role + `x-user-id` header (admin path)

### Step 2 — Fetch agent + key
SELECT `crew_agents` por `id` (RLS enforce ownership). SELECT `user_api_keys` por user. Resolve provider→endpoint→apiKey.

### Step 3 — INSERT execution row (status=running)
```sql
INSERT INTO agent_executions (agent_id, user_id, prompt, provider, model, status='running')
RETURNING id
```

### Step 4 — Call LLM provider
Endpoint conforme provider:
- `groq` → `https://api.groq.com/openai/v1/chat/completions`
- `openrouter` → `https://openrouter.ai/api/v1/chat/completions`
- `openai` → `https://api.openai.com/v1/chat/completions`

Body: OpenAI-compatible chat completions com `max_tokens=500` (cap pilot).

### Step 5 — Capture usage + compute cost
- `tokens_in = response.usage.prompt_tokens`
- `tokens_out = response.usage.completion_tokens`
- RPC `calc_agent_cost_mcoin(tokens_in, tokens_out, provider, model)` → retorna `cost_usd_micro` + `cost_mcoin`

### Step 6 — UPDATE execution row (status=done)
PATCH com response + tokens + cost + latency + completed_at.

### Step 7 — Hybrid billing (CEA-F)
**Se `user.id == SOVEREIGN_USER_ID`**: skip deduct (admin freebie · `sovereign_freebie=true`).
**Se outro user**: `RPC deduct_mco_coins(user_id, cost_mcoin)` → atomic debit.
**Se deduct falha**: log warn, NÃO falha o exec (audit trail preservado · `billed=false`).

### Step 8 — Telemetry pulse
- `scripts/agent-daily-pulse.sh` insere pulse `service=agent-daily-pulse status=healthy` em `infra_health_logs`
- Edge function: log via `console.log` (Supabase function logs)

---

## Verification gates

| Gate | Check | Pass criterion |
|---|---|---|
| G1 | `agent_executions` row final state | `status=done` · `tokens_in > 0` · `tokens_out > 0` · `cost_usd_micro > 0` · `cost_mcoin >= 1` · `completed_at IS NOT NULL` |
| G2 | Pricing applied | `cost_mcoin = CEIL((tokens_in*price_in + tokens_out*price_out)/1M / 100 * 2 * 1000)` ou floor 1 |
| G3 | Latency within budget | `latency_ms < 5000` (Groq target) ou `< 15000` (OpenRouter/OpenAI) |
| G4 | Hybrid billing correct | Sovereign: `mco_balance` unchanged · outros: `mco_balance -= cost_mcoin` |
| G5 | Cron pulse healthy | `infra_health_logs.service=agent-daily-pulse last_seen_at` < 25h (cron `0 7 * * *`) |

---

## Recovery path (failure scenarios)

| Cenário | Detecção | Recovery |
|---|---|---|
| Provider 401/403 | `agent_executions.error_msg ~ provider_\d+` | UPDATE `status=failed` (já feito pelo handler) · investigar `user_api_keys.<provider>_api_key` |
| Provider timeout | `latency_ms > 30s` ou `fetch_error` | UPDATE `status=failed` · re-tentar manualmente |
| pricing_not_found | RPC retorna `{"error":"pricing_not_found"}` | Adicionar row em `agent_pricing` ANTES de re-tentar |
| deduct_mco_coins fails (saldo insuf) | `console.warn` no edge logs · `billed=false` no response | User precisa top-up · exec já completo, sem cobrança · re-tentar quando saldo ok |
| Cron silent failure (sem pulse) | `infra_health_logs` sem `agent-daily-pulse` pulse > 25h | Checar `/var/log/mcorch-agent-daily-pulse.log` · permissões + Groq key |

---

## Success signal (whole protocol)

**Diário**:
- 4+ rows novas em `agent_executions` com `status=done` (1 por Director Sovereign)
- 1 pulse novo em `infra_health_logs.service=agent-daily-pulse status=healthy`
- (Sovereign-only) `mco_balance` permanece — admin freebie operando

**Após 7d**:
- ~28+ executions acumuladas
- Dashboard `/dashboard/agent-economics` mostra KPIs: tokens IN/OUT total, USD, mcoCoins, by_squad breakdown
- `MARGIN_FACTOR` pode ser calibrado com base nos dados (decisão Sovereign + scientist)

---

## Anti-patterns prohibited

- ❌ Cobrar Sovereign em CEA (viola design hybrid billing — Sovereign opera em modo admin freebie)
- ❌ Hardcodar custo fixo em vez de usar `calc_agent_cost_mcoin` RPC (drift entre código e source-of-truth)
- ❌ Esquecer `max_tokens=500` cap no pilot (custo explode rapidamente em tasks longas com gpt-4)
- ❌ Default provider/model `Anthropic/Claude 3.5 Sonnet` no cron diário (66 mcoCoins/exec · 33x Groq) — usar `groq/llama-3.3-70b-versatile` (1 mcoCoin floor)
- ❌ Cancelar/refund `mcoin_transactions` sem registrar `action=refund:<reason>` (auditoria de ledger quebra)
- ❌ UPDATE `agent.status` permanecendo em `thinking`/`running` sem reset back to `idle` (UI fica enganada)

---

## Pricing reference (cents per 1M tokens · seed `agent_pricing` 2026-05-27)

| Provider | Model | IN cents/1M | OUT cents/1M | Notes |
|---|---|---|---|---|
| groq | llama-3.1-8b-instant | 5 | 8 | Ultra-cheap (tasks triviais) |
| openrouter | google/gemini-2.5-flash | 7.5 | 30 | Best perf/cost |
| openai | gpt-4o-mini | 15 | 60 | OpenAI cheap path |
| groq | llama-3.3-70b-versatile | 59 | 79 | **Pilot default** |
| openrouter | meta-llama/llama-3.3-70b-instruct | 80 | 120 | Same model via OR |
| openrouter | anthropic/claude-3.5-sonnet | 300 | 1500 | Premium (Directors em tasks críticas) |
| openai | gpt-4 | 3000 | 6000 | Legacy expensive — avoid |

**Refresh policy:** quando provider anunciar mudança de preço, UPDATE row em `agent_pricing` com `notes` indicando data + fonte. Histórico não-preservado (last-write-wins) porque execuções históricas carregam o cost calculado no momento do exec (snapshot via `agent_executions.cost_usd_micro` + `cost_mcoin`).

---

## Connection to Survival Laws

- **Lei 1 (Materialidade):** todo exec materialmente registrado em `agent_executions` com UUID · cost computed via RPC (não hardcoded) · response preservado para auditoria.
- **Lei 2 (Anticipated Process):** SOP escrita antes da Phase 6 do seal v6.10.0 ser fechada (audit Phase 5c bloqueou e forçou esta criação retroativa — exatamente o caso de uso da skill `mcorch-qa-healing`).
- **Lei 3 (Pruning):** `agent_executions` é write-once, append-only · não carrega histórico em contexto · query window default 7d no dashboard.
- **Lei 4 (ORO):** cron operator = ubuntu daemon · edge operator = function runtime · reviewer = Sovereign (via dashboard) · owner = Sovereign (blast radius = balance Sovereign + custo USD agregado).

---

## v1.1 — UI Wiring (2026-05-30)

A UI da Constelação (`/dashboard/constellation`) deixou de ser teatro: antes `useSimulation.ts` (status aleatório + mensagens hardcoded a cada 3s) alimentava os Live Logs e o status 3D. Agora:

- **`src/hooks/useAgentActivity.ts`** (novo) — lê `agent_executions` reais (poll 12s + invalidate on mutation), projeta cada exec em `store.logs` (Live Logs) e em `updateAgentStatus` por agente (running→thinking · done→idle · failed→error · pending→waiting). Mapeamento `agent_executions.agent_id === crew_agents.id === store Agent.dbId`. Usa `getState()` dentro do efeito (evita React 18 #185).
- **`ConstellationPage.tsx`** — `useSimulation()` → `useAgentActivity()`.
- **`AgentDetail.tsx`** — botão **"Executar tarefa"** (Textarea de prompt) → `useAgentTask` → `agent-task-execute`. Override pilot forçado `groq/llama-3.3-70b-versatile` (guardrail: provider próprio dos agentes seed pode ser `Anthropic`=sem endpoint ou `Llama 3`=sem pricing). Desabilitado se `!agent.dbId`.
- **`useCrewStore`** — novo action `setLogs`.

**Verificação:** `npx tsc --noEmit` zero erros · build OK · Live Logs passam a refletir os 19 execs reais + cron diário; clicar "Executar" gera 1 row real (Groq · ~1 mco · freebie Sovereign) visível em <12s.

**Drift conhecido (follow-up):** seed `crew_agents` usa `provider`/`model` que não casam com `agent_pricing` (Directors=Anthropic sem endpoint no edge; specialists model="Llama 3"). Por isso o override pilot. Corrigir o seed (`enterprise-seed.ts` + `seed_crew_template`) para provider/model válidos é o próximo passo para execução sem override.

---

## Future work (registered as backlog)

- ~~Wire button "Executar tarefa" na UI da Constelação (manual trigger)~~ ✅ DONE v1.1 — `AgentDetail.tsx`
- ~~UI lê execs reais em vez de mock~~ ✅ DONE v1.1 — `useAgentActivity.ts`
- Corrigir seed `crew_agents` (provider/model válidos vs `agent_pricing`) → remover necessidade do override pilot
- Expandir cron daily pulse para incluir specialists além de Directors (108 specialists hoje em IDLE)
- Calibrar `MARGIN_FACTOR` com base em 7d+ data
- Adicionar dimensão `task_category` em `agent_executions.metadata` para análise per-tipo-de-task
- Webhook de provider rate-limit → bloquear cron temporariamente

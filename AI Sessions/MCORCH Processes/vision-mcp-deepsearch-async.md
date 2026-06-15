# SOP — Vision MCP `deepsearch.run` / `deepsearch.poll` (async job + partial-delivery refund)

> **Lei 2 (Processo Antecipado):** este SOP precede o código de `tools/deepsearch-run.ts`. Descreve o processo
> humano equivalente — o que um operador faria à mão para "rodar uma pesquisa fundamentada cobrável, entregar
> o que conseguiu e devolver a diferença" — antes de a máquina automatizá-lo.
>
> **BoK SSOT:** `docs/bok/vision-mcp/04-frd.md` (FR-VM-007 + §4.5) · `05-sdd.md` (§3.3, §5.2, §6 `vision_jobs`).
> **Contrato de billing:** `docs/processes/vision-mcp-billing-credential-resolution.md` (deduct-on-entry + refund).
> **Calibração de classe:** `docs/processes/vision-mcp-cost-calibration.md` (OTD-VM-004 — `deepsearch.run` = 3 mco).

---

## Desvio de engine registrado (OTD-VM-024)

A BoK sela o **Firecrawl** como motor do `deepsearch.*`. Por **diretiva Sovereign (2026-06-15)** — *"não quero
pagar a API Firecrawl agora; para testar usamos as chaves que já temos disponíveis"* — o `deepsearch.run` usa
o provider **`google` já provisionado** (BYOK `google_api_key` → plataforma `GEMINI_API_KEY`/`GOOGLE_API_KEY`)
com a ferramenta de **Google Search grounding** do Gemini: `query` → resposta fundamentada + `groundingChunks`
(fontes web). Cada fonte fundamentada = 1 `delivered_unit`; o `result.references[]` mapeia o shape selado
`{title,url,summary}`. **O contrato de job/refund/estado é 100% fiel à BoK** — só o "leg" do provider muda.
Débito de emenda BoK (deepsearch-blueprint emenda → `/bok-scribe`) registrado em **OTD-VM-024** (SDD §8.2).

---

## ORO

| Papel | Quem |
|-------|------|
| **Operator** | MCORCH Vision MCP container (`mcorch_vision_mcp`) — worker in-process; manualmente, um pesquisador humano |
| **Reviewer** | Sovereign + `/security-review` independente das 2 migrations |
| **Owner** | Sovereign — 1ª tool **assíncrona** que debita mcoCoins + chama provider pago com **refund parcial** |

---

## Operator — quem executa hoje (equivalente manual)

Um analista que recebe um pedido de pesquisa ("pesquise X com até N fontes"), **cobra o pacote inteiro
adiantado** (porque vai gastar tempo/recurso buscando), sai e busca N fontes, e — se só conseguiu M < N —
**devolve a diferença proporcional** ao cliente, entregando o que achou com transparência ("entreguei M de N").

---

## Sequence — passos com critério de sucesso material

### A. `deepsearch.run` (submit — NUNCA bloqueia; p95 < 2s)

| # | Passo | Critério de sucesso material |
|---|-------|------------------------------|
| 1 | Validar `query` (não-vazia) + `planned_units` (`1 ≤ N ≤ MAX_PLANNED_UNITS=25`, provisório DD-VM-003) | fora do range → **422 `validation_failed`** (PT-BR), nada cobrado |
| 2 | Sentinel `inspectPrompt(query)` (FR-VM-005a) — após identidade, antes de custo | injeção → **403 `sentinel_block`**, nada cobrado, log `sentinel` |
| 3 | Resolver chave `google` (BYOK grátis / plataforma cobra / null) | null → **402 `google_not_configured`** (`action` → /dashboard/settings) |
| 4 | `deduct_mco_coins(sub, 3, 'deepsearch.run')` — **débito integral na entrada** (§4.5.1) | saldo < 3 → **402 `insufficient_balance`**, **job não nasce** (zero linha em `vision_jobs`) |
| 5 | `INSERT vision_jobs` (`state='queued'`, `tool='deepsearch.run'`, `planned_units`, `charged_mco`) | retorna `id` (= `job_id`). Falha após débito → **refund integral** + erro |
| 6 | Disparar worker in-process (`void runJobWorker(...)` — fire-and-forget, não-awaited) | resposta retorna imediatamente |
| 7 | Retornar `{ job_id, state:'queued', planned_units, charged_mco }` | cliente recebe `job_id` para `poll` |

### B. Worker (in-process, em background — minutos permitidos, sem teto Edge)

| # | Passo | Critério |
|---|-------|----------|
| 1 | `PATCH vision_jobs state='running'` | linha em `running` |
| 2 | Gemini grounded search (`google_search` tool, model `DEEPSEARCH_MODEL`=gemini-2.5-flash) | `groundingChunks[].web.{uri,title}` extraídos; dedupe por URL; `references.slice(0, planned)` |
| 3 | `delivered = references.length` (cap em `planned`); terminal por `computeTerminal(charged, delivered, planned)` | `done` (d≥p) · `partial` (0<d<p) · `failed` (d=0 ou exceção do leg) |
| 4 | **Refund ANTES do estado terminal** (§4.5.4): `retida = max(1, floor(charged×d/p))`; `refund = charged − retida`; floor **a favor do tenant**; BYOK/Sovereign (charged=0) → refund 0 | `add_mco_coins(sub, refund)` quando `refund>0` (nunca lança) |
| 5 | `PATCH vision_jobs` → `state` terminal + `delivered_units` + `result.references` + (`refunded_mco`+`refunded_at` se houve refund) + `failed_units` se houve | invariante: `retida + refund == charged` |
| 6 | `logHealth` `deepsearch_run_terminal` (event+metadata persistidos pós-migration) | row em `infra_health_logs` com `event`+`metadata` |

### C. `deepsearch.poll(job_id)` (grátis — read-only)

| # | Passo | Critério |
|---|-------|----------|
| 1 | Validar `job_id` como UUID; `SELECT vision_jobs WHERE id=job_id AND user_id=sub` | UUID inválido OU outro tenant OU inexistente → **404 `job_not_found`** |
| 2 | Retornar `{ job_id, state, delivered_units, planned_units, partial:(state==='partial'), failed_units?, refunded_mco?, result? }` | **cost 0** (não está em `COIN_COSTS`); poll-able ≥24h pós-terminal (`expires_at`) |

---

## Verification gates

- **G1** `tools/list` expõe `deepsearch_run` + `deepsearch_poll`.
- **G2 (402-antes-do-job)** saldo 0 + sem BYOK → `deepsearch_run` = 402 `insufficient_balance` **e** `SELECT count(*) vision_jobs WHERE user_id=sub` = **0** (job não nasce).
- **G3 (happy + débito)** saldo ≥3, plataforma → `job_id` retornado; poll converge a `done`/`partial`; `mco_balance` delta = `retida` (= `charged − refund`).
- **G4 (refund parcial §4.5)** cenário `0<delivered<planned` → `state='partial'`, `refunded_mco>0`, `refunded_at` setado, e o delta de saldo bate `retida = max(1, floor(3×d/p))`.
- **G5 (refund total)** `delivered=0` → `state='failed'`, refund integral, **delta líquido de saldo = 0**.
- **G6 (tenant-bound)** poll de `job_id` de outro tenant → 404; poll de UUID inexistente → 404.
- **G7 (sentinel)** `query` de injeção → 403, zero débito, zero job.
- **G8 (BYOK grátis)** `google_api_key` BYOK → `charged_mco=0`, saldo inalterado.
- **G9 (idempotência)** poll repetido NUNCA re-dispara refund (poll é read-only; `refunded_at` é o guard de 1×/job).

Prova material: `scripts/qa/smoke-deepsearch-run.ts` (usuário throwaway, **contra o container servido** — Lei 1).

---

## Recovery path

- **Falha no INSERT do job (passo A5)** após o débito → `refund(sub, charged)` imediato + propaga erro; o tenant
  não fica cobrado por um job que não nasceu.
- **Falha do leg Gemini (worker B2)** → tratado como `delivered=0` → `failed` → **refund integral** (charge-without-value
  fechado). `add_mco_coins` nunca lança; falha de refund vai a `stderr [degraded]` para reconciliação manual.
- **Job órfão em `running`** (container reiniciado no meio do worker) → **RISCO RESIDUAL conhecido**: o tenant
  pagou e o job fica preso em `running` até reconciliação. Mitigação follow-up = sweep periódico
  (`state='running' AND now() > created_at + interval`) → `failed` + refund integral idempotente (guard
  `refunded_at`). Registrado como follow-up; o `expires_at` limita a janela de poll. **NÃO** colocar refund no
  caminho do `poll` (poll é grátis e read-only por contrato §4.5.6).
- **`planned_units` > fontes disponíveis** → entrega `M < N` legítima vira `partial` (refund proporcional) —
  comportamento correto por contrato (cobra-se pelo entregue, floor a favor do tenant).

---

## Success signal

`deepsearch_run` retorna `job_id` em < 2s; um `deepsearch_poll` posterior (≥ alguns segundos) entrega
`state ∈ {done,partial}` com `result.references[]` reais de fontes web fundamentadas, e o saldo `mco_balance`
do tenant reflete exatamente `retida` (cobrança proporcional ao entregue). Smoke `smoke-deepsearch-run.ts`
fecha verde contra o container `mcorch_vision_mcp` servido.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

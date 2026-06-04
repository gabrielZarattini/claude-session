# SOP — AEO Audit (Answer Engine Optimization visibility snapshot)

> **Lei 2 (Processo Antecipado).** Documenta o processo humano do FR-MH-010 **antes** do `aeo-audit`. SSOT: `docs/bok/marketing-hub/04-frd.md` FR-MH-010 + `05-sdd.md` (§aeo-audit + STRIDE "AEO provider call / prompt injection → sanitização; provider isolado; sem secret no prompt") + `06-data-model.md` (§aeo_audits).

## Contexto

**AEO (Answer Engine Optimization)** é o "SEO dos motores de resposta": quando um usuário pergunta algo a um motor de resposta de IA (ChatGPT, Perplexity, Google AI Overviews, Gemini), **a marca aparece citada?** O `aeo-audit` tira um **snapshot de visibilidade**: para um conjunto de queries rastreadas + a marca, mede citação (`cited`/`citation_rate`) e devolve uma **recomendação** de melhoria. Persiste em `aeo_audits` (retenção 12 meses; "stale" após ≤ 7 dias — NFR-MH-010).

### Provider (OTD-MH-003) — modo degradado documentado

Não há, hoje, chave de um motor de resposta dedicado provisionada, **e** o datacenter é bloqueado para scrape de SERP/answer-engine ao vivo (lição provada: ML bloqueia Chromium real do datacenter). Portanto o provider roda em **modo degradado documentado**: o **LLM per-user** (Groq/OpenRouter/Gemini, mesma resolução do `intent-orchestrate`) atua como *answer-engine proxy* — responde a query como um motor de resposta responderia e detecta se a marca seria citada. `aeo_audits.engine='degraded'` marca explicitamente o snapshot como proxy-LLM (não um motor real). Quando uma chave de provider real for provisionada (OTD-MH-003=B), troca-se o provider e `engine` passa a refletir o motor real — sem mudança de contrato.

## Operator

Quem executa hoje: o **tenant** (Usuário Zero / operador de marketing) no Marketing Hub (`/dashboard/marketing`, painel AEO), informando **a marca** + **1–5 queries** rastreadas.

## Sequence (cada passo com critério material)

| # | Passo | Ação | Critério de sucesso material |
|---|-------|------|------------------------------|
| 1 | **Saldo** | `aeo-audit` checa `profiles.mco_balance ≥ 5` | < 5 → HTTP 402 "Saldo insuficiente" (nada cobrado) |
| 2 | **Débito** | `deduct_mco_coins(user, 5)` atômico **na entrada** | saldo −5 (RPC server-side; nunca client-side) |
| 3 | **Sanitização** | trunca brand (≤120) + cada query (≤280), cap 5 queries | input fora de faixa → 422 |
| 4 | **Proxy de motor** | p/ cada query, LLM per-user→sistema responde + detecta citação | resposta JSON `{cited, citation_rate, recommendation}` por query (fail-soft heurístico se IA indisponível) |
| 5 | **Persistir** | INSERT 1 linha `aeo_audits` por query (`engine='degraded'`) | linhas com `0 ≤ citation_rate ≤ 1` |
| 6 | **Agregar** | `citation_rate` agregada = fração de queries citadas | HTTP 200 `{audit_id, citation_rate, findings[]}` |

## Verification gates

1. **Débito antes do trabalho.** 5 mcoCoins deduzidos **antes** da chamada de IA (igual `lead-score`/`campaign-run`). Saldo insuficiente → 402, zero trabalho.
2. **Sanitização (STRIDE — prompt injection).** brand/query truncados e inseridos como *dados* no prompt; **nenhum segredo** entra no prompt; provider isolado.
3. **Faixa válida.** `citation_rate ∈ [0,1]` (CHECK no banco); `query` 1–280 chars (CHECK). Violação → erro do banco, não persiste lixo.
4. **Telemetria.** cada path (success/degraded/error) emite `infra_health_logs.service='aeo-audit'` (NFR-MH-009).
5. **Degradação honesta.** sem IA disponível → recomendação heurística + `engine='degraded'`; nunca fabrica citação "real".

## Recovery path

- **402 (saldo):** Operator compra/recarrega mcoCoins; nada foi cobrado.
- **IA indisponível:** fail-soft — a auditoria ainda persiste com recomendação heurística (`cited=false`, `citation_rate=0`) + `infra_health_logs status='degraded'`; o Operator re-roda quando a IA voltar (novo débito).
- **Falha de persistência (500):** `infra_health_logs status='unhealthy'`; **o débito já ocorreu** → a recovery é re-rodar (custo assumido) OU o Sovereign credita manualmente (registro no handoff). _OTD-AEO-REFUND: avaliar refund automático em falha pós-débito (espelha o débito atômico do `lead-score`)._

## Success signal (materialmente observável)

HTTP 200 `{status:'ok', audit_id, citation_rate, findings[]}` + N linhas em `aeo_audits` (1 por query) com `created_at` recente + nó `observation` `aeo:<brand>:<date>` no mesh + `infra_health_logs.service='aeo-audit' status='healthy'`. Freshness: um audit conta como vigente por ≤ 7 dias (NFR-MH-010).

## ORO

- **Operator:** tenant (humano) · **Reviewer:** `/security-review` da migration `aeo_audits` + policy de débito atômico · **Owner:** Sovereign (blast radius = 5 mcoCoins/run + qualidade da recomendação; provider degradado documentado, sem risco outward).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

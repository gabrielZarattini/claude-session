# Session agent-a0cf0981edfbfb6da
**Date:** 2026-06-20 | **Session ID:** `agent-a0cf0981edfbfb6da`

---

## 👤 User *(17:00:01)*


PROJETO: TradeUX — bot Binance Spot (Beholder/beholder.js = motor hot-path) + agente LLM, mainnet REAL, saldo ~$149.
Repo: /home/gcrux-tradeux/tradeux (leia src do backend, tradeux-agent/src). Memorias estrategicas (LEIA p/ contexto): /home/ubuntu/.claude/projects/-home-gcrux-tradeux/memory/*.md
(em especial: tradeux-farm-funnel-backtest, tradeux-mainnet-go-live, tradeux-strategy-engine, tradeux-bear-capture-research,
tradeux-harvester-experiment, tradeux-vault-guard, tradeux-regime-gate, tradeux-flow-oracle, tradeux-1m-scalping-and-cockpit,
tradeux-earn-autosubscribe-incident). Audit das 12h: /tmp/audit12h/ + a sintese ja feita.

ESTADO ATUAL: mainnet LIVE (floor liberado, halted=false), CANARY Farm-only: so as VENDAS no-loss do Farm armadas
(id10/12/14 ON); compras do Farm (9/11/13), Trend (6/7/15..), Baseline (2/3) OFF por decisao do operador. Posicao real:
0.907 LTC (~$40, custo $39.87) esperando vender a $44.39. BTC = ZERO (concentracao em BTC e a meta, PAUSADA p/ pesquisa).
Equity $149. Proteções: cap diario -5%, teto $25/ordem, teto exposicao Farm $25/simbolo, riskGuard por-ordem, botao de panico,
vault guard (trava SELL-BTC no MCP). Funil shadow baseline $10k (inerte a $149). Paper engine: 16 trilhas [PAPER] virtuais.

INCIDENTE RECENTE (ja resolvido): auto-subscribe do Simple Earn moveu LTC spot -> LDLTC -> (a) HALT falso do cap (LD* sumia
do equity) FIX deployado c6d0853; (b) venda no-loss travou silenciosa as 07:00 + ruido PUSH do [PAPER] FIX deployado 457e25a
(silencia push [PAPER] + alerta Telegram em falha de execucao deduped autofail:<id>).

TAREFA — REVISAO DE RISCO / MONEY-PATH. Onde dinheiro REAL pode ser perdido ou uma protecao falhar? Examine: o vault guard de
SELL-BTC (so no MCP? o grupo Baseline id3 vende o cofre coberto SO por HALT/riskGuard?), os caps (teto $25/ordem, Farm $25/simbolo,
cap diario -5% — buracos?), o riskGuard por-ordem (assertWithinRisk em exchange.js — cobre todos os caminhos? OCO? grid?), o botao
de panico, fail-safes do dailyCap. Modele cenarios adversariais (auto-subscribe religado, stream caindo, baseline do cap errado,
automacao renomeada perdendo prefixo). Severidade + recomendacao. Foque em PERDA REAL, nao cosmetico.

## 🤖 Claude *(17:00:03)*

I'll start by reading the strategic memory files and then dig into the actual code paths where real money moves. Let me begin in parallel.

## 🤖 Claude *(17:00:05)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la /home/gcrux-tradeux/tradeux && echo \"---BACKEND SRC---\" && ls -la /home/gcrux-tradeux/tradeux/src 2>/dev/null && echo \"---AGENT SRC---\" && ls -la /home/gcrux-tradeux/tradeux/tradeux-agent/src 2>/dev/null",
  "description": "List repo layout"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 2
> total 140
> drwxrwxr-x 13 gcrux-tradeux gcrux-tradeux  4096 Jun 19 23:17 .
> drwxrwx--- 11 gcrux-tradeux ubuntu         4096 Jun 19 23:33 ..
> drwxrwxr-x 11 gcrux-tradeux gcrux-tradeux  4096 Jun 19 23:24 backend
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  9970 Jun 15 02:01 CLAUDE.md
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux   954 Jun  2 20:41 docker-compose.supabase.yml
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux  2970 Jun 19 14:34 docker-compose.yml
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux   593 Jun  8 16:22 .dockerignore
> drwxrwxr-x  2 gcrux-tradeux gcrux-tradeux  4096 Jun  9 12:56 docs
> -rw-------  1 gcrux-tradeux gcrux-tradeux  2990 Jun 19 23:17 .env
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux  4077 Jun  2 20:41 .env.example
> drwxrwxr-x  2 gcrux-tradeux gcrux-tradeux  4096 Jun  4 17:16 .firecrawl
> drwxrwxr-x  6 gcrux-tradeux gcrux-tradeux  4096 Jun 19 23:19 frontend
> drwxr-xr-x  4 gcrux-tradeux gcrux-tradeux  4096 Jun 15 01:58 .gemini
> drwxrwxr-x  8 gcrux-tradeux gcrux-tradeux  4096 Jun 20 12:33 .git
> drwxrwxr-x  3 gcrux-tradeux gcrux-tradeux  4096 Jun  2 20:41 .github
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux  1926 Jun 19 14:34 .gitignore
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux  1073 Jun  2 20:41 LICENSE
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux   768 Jun  2 20:41 Makefile
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux  7042 Jun  2 20:41 README.md
> drwxr-xr-x  2 gcrux-tradeux gcrux-tradeux  4096 Jun 15 01:57 scripts
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux  5990 Jun  3 16:22 SECURITY.md
> -rw-r--r--  1 gcrux-tradeux gcrux-tradeux 21861 Jun  2 21:55 setup.log
> -rwxrwxr-x  1 gcrux-tradeux gcrux-tradeux  1558 Jun  3 12:38 setup.sh
> drwxrwxr-x  6 gcrux-tradeux gcrux-tradeux  4096 Jun 16 13:37 tradeux-agent
> drwxrwxr-x  5 gcrux-tradeux gcrux-tradeux  4096 Jun  8 20:14 tradeux-mcp
> drwxrwxr-x  2 gcrux-tradeux gcrux-tradeux  4096 Jun  2 20:41 .vscode
> ---BACKEND SRC---
> ```

## 🤖 Claude *(17:00:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la /home/ubuntu/.claude/projects/-home-gcrux-tradeux/memory/ 2>/dev/null",
  "description": "List memory files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 188
> drwxrwxr-x  2 ubuntu ubuntu  4096 Jun 20 12:34 .
> drwxrwxr-x 26 ubuntu ubuntu  4096 Jun 19 23:48 ..
> -rw-rw-r--  1 ubuntu ubuntu  1387 Jun  2 21:32 github-ssh-key-on-ubuntu.md
> -rw-rw-r--  1 ubuntu ubuntu  3016 Jun 17 15:36 git-ownership-gotcha.md
> -rw-rw-r--  1 ubuntu ubuntu 10964 Jun 20 02:25 MEMORY.md
> -rw-rw-r--  1 ubuntu ubuntu   767 Jun  2 21:34 respond-in-pt-br.md
> -rw-rw-r--  1 ubuntu ubuntu  1796 Jun  3 10:46 shakehands-protocol.md
> -rw-rw-r--  1 ubuntu ubuntu 20393 Jun 17 13:52 tradeux-1m-scalping-and-cockpit.md
> -rw-rw-r--  1 ubuntu ubuntu  5952 Jun  3 19:40 tradeux-agent-500k-validation.md
> -rw-rw-r--  1 ubuntu ubuntu  5381 Jun  8 17:37 tradeux-agent-token-economics.md
> -rw-rw-r--  1 ubuntu ubuntu  3824 Jun  8 23:38 tradeux-bear-capture-research.md
> -rw-rw-r--  1 ubuntu ubuntu  1977 Jun  2 22:03 tradeux-deploy-topology.md
> -rw-rw-r--  1 ubuntu ubuntu  3463 Jun 20 12:34 tradeux-earn-autosubscribe-incident.md
> -rw-rw-r--  1 ubuntu ubuntu  5452 Jun  9 14:29 tradeux-farm-funnel-backtest.md
> -rw-rw-r--  1 ubuntu ubuntu  6051 Jun  8 23:39 tradeux-flow-oracle.md
> -rw-rw-r--  1 ubuntu ubuntu 10652 Jun 19 12:13 tradeux-harvester-experiment.md
> -rw-rw-r--  1 ubuntu ubuntu  1422 Jun  3 17:38 tradeux-logger-per-category-files.md
> -rw-rw-r--  1 ubuntu ubuntu 17556 Jun 19 23:33 tradeux-mainnet-go-live.md
> -rw-rw-r--  1 ubuntu ubuntu  2311 Jun  3 12:26 tradeux-orchestration-model.md
> -rw-rw-r--  1 ubuntu ubuntu  2013 Jun  9 12:10 tradeux-ordertemplate-brain-cache.md
> -rw-rw-r--  1 ubuntu ubuntu  5087 Jun  4 17:59 tradeux-regime-gate.md
> -rw-rw-r--  1 ubuntu ubuntu  2874 Jun  9 12:19 tradeux-settings-password-incident.md
> -rw-rw-r--  1 ubuntu ubuntu 10103 Jun 19 16:35 tradeux-strategy-engine.md
> -rw-rw-r--  1 ubuntu ubuntu  6215 Jun 16 19:00 tradeux-telegram-notifications.md
> -rw-rw-r--  1 ubuntu ubuntu  4916 Jun  4 11:35 tradeux-trend-following.md
> -rw-rw-r--  1 ubuntu ubuntu  2313 Jun  8 20:34 tradeux-vault-guard.md
> ```

## 🤖 Claude *(17:00:10)*

Let me read the key memory files and the core money-path code in parallel.

## 🤖 Claude *(17:00:11)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrux-tradeux/memory/tradeux-vault-guard.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>This memory is 11 days old. Memories are point-in-time observations, not live state — claims about code behavior or file:line citations may be outdated. Verify against current code before asserting as fact.</system-reminder>
> 1	---
> 2	name: tradeux-vault-guard
> 3	description: MCP tem trava determinística FAIL-CLOSED de SELL-BTC no place_order (pré-requisito (a) do flip ALLOW_TRADING); status dos demais pré-requisitos
> 4	metadata: 
> 5	  node_type: memory
> 6	  type: project
> 7	  originSessionId: bfe76003-4642-4a03-a4c1-33da40119d53
> 8	---
> 9	
> 10	Em `tradeux-mcp/src/index.js`, `tradeux_place_order` tem uma trava determinística do COFRE (commit `9898bdf`, gate QA PASS + TL APPROVE): `isBtcVaultSymbol` rejeita `side=SELL` de TODO símbolo que começa com "BTC" (FAIL-CLOSED), exceto os prefixos não-base `BTCUP/BTCDOWN/BTCST`. Vale p/ qualquer `type`, ANTES de qualquer chamada ao backend. Substituiu uma allowlist de quotes que falhava ABERTO (a QA enumerou a Binance ao vivo e achou 5 pares BTC-base escapando: BTCUSDS/BTCUSD1/BTCEURI/BTCIDR/BTCU). Teste de regressão hermético: `tradeux-mcp/test/place-order-vault-guard.mjs` (`npm test`, também no CI).
> 11	
> 12	`automationId` obrigatório nas ordens do agente foi AVALIADO e DESCARTADO: ordens do agente são MANUAIS por design (automationId ausente → bucket 'M'/'Others' em `groupByAutomations`); forçar id falso corromperia o P&L e não é mutex. Vendas legítimas de BTC vêm das automações id3/id7 (que executam in-process no `beholder.js`, NÃO via `POST /orders` → não passam por esta trava).
> 13	
> 14	**Pré-requisitos do flip `TRADEUX_ALLOW_TRADING=true`** (hoje DRY): (a) ✅ trava SELL-BTC = FEITO; (b) ✅ `get_memory_indexes` enxugado (commit `2d01002`, `leanMemoryIndexes`: resumo compacto sem símbolo + detalhe por símbolo) — ainda aberto o mesmo p/ `get_memory`/`get_wallet_full` sem símbolo, e o SYSTEM_PROMPT ainda proíbe a tool (pode reabilitar); (+) follow-ups dos gates: o backend `ordersController.placeOrder` não tem trava equivalente (mover a defesa p/ lá se o modelo de ameaça incluir UI/outros clientes).
> 15	
> 16	CORREÇÃO de premissa recorrente: o agente NÃO é "BTCUSDT-only" — o SYSTEM_PROMPT autoriza FARM de alts (LTC/BNB/ADA) vs USDT. Isso não quebra a trava (alts não começam com "BTC"). O invariante que a sustenta é: BTC=cofre, nenhum SELL de par BTC* é legítimo para o agente.
> 17	
> 18	Relacionada: [[tradeux-agent-token-economics]], [[tradeux-farm-funnel-backtest]], [[tradeux-agent-500k-validation]], [[shakehands-protocol]] (HANDOFF.md item de dívida técnica (a)).
> 19	
> ```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-20 - agent-a0ce568b77a1d7483]]
> * **Próxima Sessão**: [[2026-06-20 - agent-a14f2aab56c8204d1]]
%% --- TIMELINE END --- %%

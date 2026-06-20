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

## 🤖 Claude *(17:00:12)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrux-tradeux/memory/tradeux-mainnet-go-live.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	---
> 2	name: tradeux-mainnet-go-live
> 3	description: Antigravity colocou o sistema em MAINNET (dinheiro real) via feature dual-env; armado mas NÃO seguro p/ fundar — must-fix list
> 4	metadata: 
> 5	  node_type: memory
> 6	  type: project
> 7	  originSessionId: 78499af7-71fd-4dbf-816c-c5996402727d
> 8	---
> 9	
> 10	Em 2026-06-15 (madrugada BRT) a sessão do **Antigravity** (commits `e610f90`..`1fe3364`, autor gabrielcall@gmail.com, NÃO selados no HANDOFF, 5 à frente do seal `a408500`) entregou **ambiente dual + funil live-buy da Fase 4** e o dono **virou `settings.useTestnet=0` → MAINNET REAL** (api.binance.com, chaves mainnet ≠ testnet).
> 11	
> 12	**Por que nenhuma ordem mainnet ainda (CONFIRMADO ao vivo, NÃO é bug):** engine roda live em mainnet; todo módulo está armed-waiting/gateado. Regime=trend nos 4 → farm OFF; trend precisa de golden cross FRESCO (above=true só recarregado); id2 RSI gate aberto mas RSI~45<25; harvester armado (FAIR saudável 66.893; trigger 64.887 vs bestAsk 66.895, precisa −3%); funil dormente (USDT real **$148,84** < baseline $10.000). Ledger mainnet frio: 259 ordens TODAS `isTestnet=1` (o filtro de isolamento de `e610f90` esconde o histórico lucrativo testnet na visão mainnet → "o lucro sumiu"). 0 ordens mainnet, 0 abertas.
> 13	
> 14	**MUST-FIX DE CÓDIGO RESOLVIDOS + DEPLOYADOS** (commit `96915e0`, gate QA PASS-c/ressalvas + TL APPROVE; auditoria wf `wf_b252a2ba-9de`). Estado vivo após deploy (rebuild backend + up -d, boot limpo 17:35): **TRADING_HALT=true (CONGELADO — nada negocia)**, FUNNEL_LIVE_BUY=false (funil em SHADOW), caps no ar, SAPI=mainnet. Sistema espera o GO do dono.
> 15	1. ✅ **Funil live-buy** refeito (`maybeLiveBuy`/`persistFunnelBuy`): usa SÓ o baseline FIXO do env (nunca RUNTIME_BASELINE → mata o dreno-por-depósito da Fase4), TETO obrigatório `FUNNEL_MAX_BUY_USDT` (sem teto = RECUSA), persiste com isTestnet + alerta dono se falhar. + `FUNNEL_LIVE_BUY=false` no .env.
> 16	2. ✅ **AÇÃO DO DONO (Binance) — FEITA 2026-06-17.** Dono editou a chave HMAC "tradeUX" na UI da Binance: desmarcou **Enable Withdrawals** (= "saque off"; NÃO existe botão "saque off" — é só desmarcar Withdrawals) E **Permits Universal Transfer**; restou **Reading + Spot&Margin Trading**; IP **Restrict to trusted IPs = `137.131.243.179`** (= IP de saída do servidor, host==container, confirmado via api.ipify). Verificação read-only minha (login + `GET /exchange/balance/USDT` → HTTP 200, **USDT 148.84** lido, 767 ativos) confirma **Reading+IP OK** com HALT intacto. ⚠️ Saque-OFF NÃO é verificável por leitura (e NÃO se testa saque — nunca mover dinheiro); confiança vem do Save na UI. `exchange.js` ainda expõe `withdraw()` mas a chave agora recusa saque na Binance.
> 17	3. ✅ **`.env` SAPI/API/STREAM → mainnet** (encerra o split-brain de SAPI).
> 18	4. ✅ **`ordersController` morto** corrigido (passa settings plano) → venda manual/emergência volta a funcionar.
> 19	5. ✅ **`insertOrder` ghost** mitigado (honra isTestnet explícito; funil alerta dono na falha de persistência).
> 20	6. ✅ **`getOpenOrdersByAutomation`+`getOpenOcoOrders`** ganham filtro isTestnet (reconcile não cruza ambientes).
> 21	7. ✅ **Scripts backfill** guard `ALLOW_BACKFILL=true` + `isTestnet:true` fixo.
> 22	8. ✅ **Teto de risco no BACKEND** (`exchange.js` chokepoint buy/sell/oco): `TRADING_HALT` kill-switch (cobre TUDO) + `MAX_ORDER_NOTIONAL_USDT=1500` por ordem (calibrado acima do farm $1000). ✅ furo MARKET-por-quantidade **FECHADO** (2026-06-17, commit `e27339a`, QA PASS-c/ressalvas + TL APPROVE): o riskGuard agora deriva o preço (`stopPrice` quando presente, senão `MINI_TICKER.close` via require lazy do beholder) e capa MARKET-por-qty-base (TREND_QTY/HARVEST_QTY/MAX_WALLET; STOP/TP-MARKET). MINI_TICKER frio → passa logado (coberto só pelo HALT; deliberado p/ não bloquear venda protetiva). **Inerte sob HALT** (branch nem é alcançado). Pré-existente e fora deste fix: pares quote≠USDT seguem sem teto.
> 23	
> 24	**PRA IR AO VIVO (flip único `TRADING_HALT=false`):** (a) ✅ saque-off/IP FEITO 2026-06-17 (item 2); (e) ✅ cap −5% + kill-switch QUENTE FEITO 2026-06-18 (item 9); (c) ✅ P&L-BNB FEITO 2026-06-18 (item 10). **🎯 TODOS os pré-reqs de CÓDIGO (a)-(e) FEITOS+DEPLOYADOS → falta só o GO DO DONO pro flip + canary de UM-GRUPO-SÓ.** BNB-fee agora SEGURO de ligar na UI Binance (P&L honesto pós-(c)) — mas é decisão do dono. **FOLLOW-UPS antes de escalar/ligar funil:** plano de aporte vs baseline $10k do funil; **Farm Buy id5/7/9 está em MIN_NOTIONAL×200≈$1000/ordem numa conta de $149 → falha por saldo quando disparar (resizing é decisão do dono)**; re-selar HANDOFF (ainda diz "testnet"). HANDOFF NÃO selado nesta sessão.
> 25	
> 26	9. ✅ **CAP DIÁRIO −5% + KILL-SWITCH QUENTE** (item (e); 2026-06-18, commits `8ef1b69`+`1b639ce`, QA PASS-c/ressalvas + TL APPROVE, plan-mode aprovado pelo dono; smoke ao vivo OK). **`riskState.js` é a FONTE ÚNICA do HALT** — 3 fontes empilháveis: `env` (floor PERMANENTE de `TRADING_HALT=true`; só `.env`+restart o derruba) · `manual` (operador) · `daily-cap` (auto-expira na virada UTC). `exchange.js` agora lê `riskState.isHalted()` POR ORDEM (não mais `const` no load) → **HALT é QUENTE**. **`dailyCapJob`**: snapshota o equity-TRADEABLE (USDT + spot precificado via MINI_TICKER; **Earn/Locked `LD*` e `DAILY_CAP_IGNORE_ASSETS` EXCLUÍDOS** — a conta tem LDGUN/LDBABY) na virada UTC, arma o HALT quando `equity ≤ snapshot×0.95` (block-ALL, inclusive venda protetiva → exige intervenção manual). Fail-safe a preço frio (não dispara no escuro) + alarme Telegram anti-silêncio (15min). Persiste em `logs/risk_state.json` + `logs/daily_cap_snapshot.json` (sobrevive restart; daily-cap auto-expira pós-meia-noite). **🔴 BOTÃO DE PÂNICO QUENTE NOVO:** `POST /system/halt {on:true,reason}` (operator-only, JWT; SEM MCP write tool — agente não flipa) trava sem restart; `POST /system/halt {on:false}` solta o manual (mas NÃO o env floor); `POST /system/daily-cap/reset` re-arma; `GET /system/halt` e `/system/daily-cap` observam. Cockpit/agent leem o estado quente via `/analysis/cockpit` (`env.tradingHalt` boolean preservado + `haltSource`/`haltReason` aditivos). Estado vivo pós-deploy: baseline hoje **$148,84**, piso **$141,40**, `tripped:false`, `halted:true` (source `env`). Inerte sob HALT. **Dívida documentada (não-bloq.):** rollover c/ preço frio fica sem baseline até esquentar (auto-cura); reSnapshot serializado via flag `running`. Knobs env (defaults seguros): `DAILY_CAP_ENABLED=true`, `DAILY_LOSS_CAP_PCT=0.05`, `DAILY_CAP_CHECK_MS=60000`, `DAILY_CAP_COLD_ALERT_MS=900000`, `DAILY_CAP_IGNORE_ASSETS=`.
> 27	
> 28	10. ✅ **P&L-BNB — net fee-inclusive ciente do lado** (item (c); 2026-06-18, commit `854bab5`, QA PASS-c/ressalvas + TL APPROVE, plan-mode aprovado; deploy+migration ao vivo OK). Hoje o `net` só descontava taxa paga no QUOTE (USDT); taxa em **BNB** (o que o desconto BNB-fee −25% liga) passava batido → P&L/painel mentiam OTIMISTA. Fix: **helper único `backend/src/utils/feeCalc.js` `computeNet`** unifica os 3 pontos de cálculo (`calcFillFinancials`, `app-em.processExecutionData`, `ordersController.syncOrder`): **VENDA `net=cummQuote−taxa(USDT-eq)`, COMPRA `net=cummQuote+taxa(USDT-eq)`** (a taxa de COMPRA não some mais do P&L); taxa em quote→direto, base→×avgPrice, **BNB/outro→`beholder.getStableConversion(...,'USDT',...)`** (require LAZY, sem ciclo). **Coluna nova `orders.commissionAsset`** (migration `20260618170000`, idempotente dual-dialect, rodou no boot) persiste o asset → recompute/auditoria via **`POST /orders/:id/sync`**. **Fail-safes:** preço BNB frio → `net=cummQuote` + commissionAsset persistido (recomputa no sync); `side` ausente → sem ajuste (não assume venda); guard `net>0`. Consumidores (getDailyProfit, relatórios, getAveragePrices) ficam mais honestos (P&L p/ baixo), sem quebra. **NÃO** construído (escopo): toggle bnbBurn (dono liga na UI Binance), backfill (0 ordens mainnet), break-even do cockpit (segue 0,20% conservador), Farm no-loss (buffer 1,2% >> fee → já fee-safe). ⚠️ pré-existente (QA P1, fora de escopo): em par NÃO-USDT o `net` fica denominado no quote, não USDT — irrelevante hoje (só pares *USDT negociam).
> 29	
> 30	**REVISÃO DE ESTRATÉGIA p/ $148 reais (wf `wte6rt68t`, 8 agentes + verif. adversarial 3 lentes; dono fundou ~150 USDT mainnet):**
> 31	- **🪦 HARVESTER (id22-25) MORTO no mainnet** (código+dado vivo). FAIR=lastPrice MAINNET hardcoded (`fairPriceService.js:33`, api.binance.com) e o BOOK do bot é SIMULADO do miniTicker (`app-em.js:38-39`; monitor BOOK id2 OFF → bestAsk=bestBid=close). Mesma venue → spread ~$0.01; gatilho `bestAsk<FAIR×0.97` (−3% na MESMA corretora) só dispara em flash-crash raro (pior queda sub-minuto recente <1%) e aí é falling-knife (desgateado de regime). Os "10/10 ciclos" eram **arbitragem testnet-vs-mainnet**. NÃO afrouxar 0.97 nem ligar o monitor BOOK real (vira scalper que sangra fee). Redesign: re-ancorar FAIR a HIGH rolante 24-48h (klines) → MR real; backtestar + gate `REGIME!=bear` antes de fundar. Corrige a tese de [[tradeux-harvester-experiment]] (era testnet-específica).
> 32	- ✅ **BUG P0 (Farm Sell) RESOLVIDO+DEPLOYADO** (commit `c163112`, QA PASS-c/ressalvas + TL APPROVE re-review). Era: `orderTemplates` id6/8/10 = `MAX_WALLET` → vendia a carteira INTEIRA e dumpava a posição do Trend co-localizado. Fix: (1) keyword **`FARM_QTY`** em `beholder.calcQty` (espelho do HARVEST_QTY, vende só `MEMORY['<sym>:FARM_DCA'].qty`); (2) **`getFarmPosition` escopado por automação** (`name LIKE 'Farm %'` → BUYs/lastSell filtrados por automationId; o Trend não infla/re-baseia mais o bucket); (3) **migration `20260615200000`** durável (sobrescreve a `20260614190000` que era o próprio bug): Farm Sell→FARM_QTY, Farm Buy ×200→**×2** (~$10/ordem), Baseline RSI Buy id2→**isActive=0** (era acumulador pelado, compra sem venda). Verificado no DB pós-migrate. **FOLLOW-UP `FARM_SELLING` ✅ FEITO v1 (2026-06-17, commit `baf0f4b`, QA PASS+TL APPROVE+cético money-path PASS):** trava anti-empilhamento via SKIP no place + SET por orderId + RELEASE por **match de orderId** em qualquer terminal (app-em.updateFarmPosition) — **BRAIN-independente** (superior ao HARVEST_SELLING, que perma-trava no stop/start). Sem migration/condition/reload (skip de código, não via condition). **Reconstrução-no-boot (loadFarmSellingLocks) + reconciliação partial→cancel do Farm DEFERIDAS** — gate documentado: NÃO escalar `FARM_SIZE_MULT` até implementá-las (risco bounded: só remistura alt-wallet LTC/BNB/ADA, NUNCA o cofre de BTC, nunca oversell além da carteira). ⚠️ Escopo por `name LIKE 'Farm %'` é frágil a rename — nice-to-have: tag/flag explícita.
> 33	- **TREND (id6/7 BTC, id15-20 alts) = ÚNICO edge real** (same-exchange, golden/death cross 1h), mas minúsculo ($5-15/perna, ~1-3 RT/símbolo/mês). BTC a $5 = no piso do minNotional (frágil). Correlação: 4 golden agora → death cross geral = drawdown único.
> 34	- **EXPECTATIVA REAL: $148 spot ≈ FLAT no mês** (~$0/dia mediano; melhor mês ~+5%=$0.25/dia amortizado só num bull geral). SEM rendimento diário nessa escala. **+3 BTC é impossível (1.350×).** 0 ordens mainnet → nada validado com fill/fee/slippage reais. Win = validação + compor o trend + PACIÊNCIA; maior risco = forçar trade pra ver P&L e sangrar fee. Capital travável: até ~$80/$148 num downtrend (buckets MR sem stop). Plano: P0 fixes (seguros, halted) → redesign harvester+backtest → canary 1 trade → só então descongelar.
> 35	
> 36	**Bom (ruled out / sólido):** agente LLM NÃO coloca ordem real (`ALLOW_TRADING=false` verificado no container; MCP write throws); trava SELL-BTC do cofre vale; migrations portáveis; `secretKey` cifrado em repouso (só `accessKey` plaintext); sem split-brain no caminho SPOT. ⚠️ Se `ALLOW_TRADING` for ligado: guarda SELL-BTC tem buracos (BUY BTCUSDT, SELL alts, BUY ETHBTC). Ver [[tradeux-farm-funnel-backtest]], [[tradeux-harvester-experiment]], [[tradeux-settings-password-incident]], [[tradeux-vault-guard]].
> 37	
> 38	## Painel "Ativação de grupos" em Settings (2026-06-19, commit `771ecf0`, deployado+verificado ao vivo)
> 39	Botão **Ligar/Parar GRUPOS de automação em lote** (Farm/Trend/Baseline/Paper) no card de Settings, ao lado dos botões de HALT — substitui SSH/`automation-ctl.js`. Backend: `GET /automations/groups` + `POST /automations/groups/:group/:action` (atrás do authMiddleware, ANTES de `/:id` no router); grupos por **REGEX de nome**; `applyAutomationActive` extraído de start/stop = **MESMO caminho do botão por-linha** (registra no BRAIN com as ações, via `getAllAutomations` com include). **harvester/grid/scalp EXCLUÍDOS** de propósito (mortos/refutados, não reativáveis por aqui). Frontend: confirm **fail-SAFE ciente do floor** (avisa em trading-liberado E em estado desconhecido; pega HALT fresco antes de ativar grupo real). **Ativar só ARMA — NÃO mexe no HALT** (guard por-ordem do `riskState` segura execução se o floor estiver up). Gate: verify 3/3 ok, QA PASS, TL APPROVE (zero must-fix); smoke vivo stop→start paper 16→0→16 OK; **freeze preservado no deploy** (`halted=true, floor=true`). ⚠️ **CAVEAT money-path:** o grupo `baseline` inclui `Baseline RSI Sell BTCUSDT` (venda do COFRE BTC) — a trava `isBtcVaultSymbol` vive SÓ no caminho MCP, NÃO no beholder/exchange; com floor liberado, ativar Baseline arma uma venda real de BTC coberta só por **HALT+riskGuard**, não pela trava do cofre (já era assim no start por-linha — o botão só agiliza). Ver [[tradeux-vault-guard]]. Nice-to-have deferidos: migrar grupo p/ coluna explícita (regex frágil a rename), teste do regex no CI, re-arm DB↔BRAIN no painel.
> 40	
> 41	## 🔴 GO-LIVE REAL — dono flipou o floor (2026-06-19) — NÃO ESTÁ MAIS CONGELADO
> 42	O dono **destravou o floor pela UI** (botão LIGAR trading real). Estado verificado ao vivo: `GET /system/halt` → **`halted=false, floor=false, manual=false, dailyCap=false, envHard=false`** = trading REAL permitido. **Decisão do dono, deliberada** (a UI exige digitar `LIGAR REAL`); Claude NÃO virou — só verificou e orientou. **Nenhuma ordem real disparou no flip** (orders 252-259 eram testnet de 15/jun; ledger real ainda frio).
> 43	- **Canary escolhido pelo dono (via AskUserQuestion) = FARM-ONLY.** Claude executou `POST /automations/groups/trend/stop` (8 paradas) pelo painel novo → estado: **Farm 6/6 ON (REAL/LIVE)**, Trend 0/8 OFF, Baseline 0/2 OFF, Paper 16/16 (virtual). Farm é **no-loss** (só vende acima do custo), alts LTC/BNB/ADA, **nunca o cofre BTC** → downside limitado (capital pode ficar preso em alts num downtrend, sem perda realizada por desenho).
> 44	- **Proteções vivas mesmo LIVE:** cap diário −5% (baseline novo de hoje UTC; arma HALT no drawdown ≈ −$7,40/$148), teto $300/ordem, riskGuard por-ordem, **pânico** = UI "TRAVAR floor"/"Travar agora" ou `POST /system/halt {on:true}` / `POST /system/floor {on:true}`. Telegram notifica TODA ordem (NEW/FILLED…) → a 1ª ordem real do Farm avisa.
> 45	- **Expectativa honesta (dado do dia):** EV fino/negativo — o único round-trip do paper consistência BTC fechou **+$0,0143 líquido** (taxa comeu 73% do bruto), por sorte (BTC subiu no hold), não por edge; EV BTC −0,17%, pHit 0,40. É **validação da plumbing com dinheiro real**, não rota de lucro. Veredito precisa de 15-30 round-trips (paperReviewJob).
> 46	- ⚠️ Pra re-congelar: `POST /system/floor {on:true}` (ou UI TRAVAR floor). Pra re-armar à prova de clique: `TRADING_HALT_HARD=true` no `.env`+restart.
> 47	
> 48	## Caps recalibrados + 1ª ordem real + 2 GOTCHAS duráveis (2026-06-20, commit `235484c`)
> 49	- **Teto por-ordem $300→$25** (`.env MAX_ORDER_NOTIONAL_USDT=25`+restart): $300 num saldo de ~$148 era DECORATIVO (não dá pra colocar ordem > saldo; Binance recusa). $25 é proporcional (≈17%/ordem).
> 50	- **Teto de EXPOSIÇÃO do Farm por símbolo (`FARM_MAX_NOTIONAL_USDT=25`):** guard novo em `beholder.placeOrder` (hot path, antes do calcQty) — Farm Buy (BUY + `automation.name` ~ `/^Farm Buy /`) é SKIPado se o notional investido no símbolo ≥ teto. Soft-cap, BRAIN-independente (espelha `FARM_SELLING`), `0`=off. Doc em `backend/.env.example`.
> 51	- **🔴 GOTCHA 1 (pego no gate QA/TL — money-path):** `MEMORY['<sym>:FARM_DCA'].cost` é o **PREÇO MÉDIO PONDERADO por unidade** (DCA), **NÃO o USDT investido** (`ordersRepository`: `cost = totalCost/totalQty`; a condition do Farm Sell faz `bestBid > cost*1.012` = preço×preço). O **notional investido = `qty × cost`**. O 1º guard comparava `cost` cru com $25 → bloquearia BNB (~$600/un) já no 1º fill e NUNCA bloquearia ADA (~$0,40/un). FIX = `qty × cost`; unit test 5/5. **Qualquer cálculo de exposição/investido do Farm: use `qty × cost`, nunca `cost` sozinho.**
> 52	- **🔴 GOTCHA 2 (queima fácil):** a tabela `orders` MISTURA testnet + mainnet. Pra posição/P&L REAL **SEMPRE filtre `isTestnet=false`** — senão soma fantasmas (ex.: ordens LTC de 22 LTC/$997 de 15/jun eram TESTNET; davam um falso "$3030 investido").
> 53	- **1ª ordem real + canary refinado:** Farm fez **DCA 3× em LTC** (~$30, avg $43,91; esperado — LTC virou range, RSI<35). Operador parou o Farm (concentração, NÃO perda — equity ~$148,75 intacta, USDT↔LTC). Depois **religou SÓ as VENDAS do Farm** (id10/12/14) → lotes saem no-loss quando LTC bouncar ~$44,4; **compras off** (id9/11/13). Estado canary atual: Farm **3/6** (vendas armadas), Trend/Baseline off.
> 54	
> ```

## 🤖 Claude *(17:00:12)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrux-tradeux/memory/tradeux-earn-autosubscribe-incident.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	---
> 2	name: tradeux-earn-autosubscribe-incident
> 3	description: "Binance Simple Earn auto-subscribe move saldo spot → LDxxx, o que dispara HALT falso do dailyCap E quebra a venda no-loss do Farm"
> 4	metadata: 
> 5	  node_type: memory
> 6	  type: project
> 7	  originSessionId: f441b214-aeeb-4754-b4a6-052611f40093
> 8	---
> 9	
> 10	**Incidente 2026-06-20 (~04:11 UTC): HALT falso do daily-cap.** A Binance **auto-subscreveu** o LTC comprado pelo Farm no **Simple Earn Flexible** → o saldo spot virou **`LDLTC`** (prefixo "LD" = Locked/Earn) e o **spot LTC ficou 0**. Provado via `GET /system/daily-cap` → `LAST.ignored=["LDLTC","LDUSDC","LDGUN","LDBABY"]`, `equity=109.02` (só USDT) e `GET /exchange/balance/USDT` → `LDLTC.available=0.8901`, `LTC.available=0`.
> 11	
> 12	**Dois estragos da mesma causa:**
> 13	1. **HALT falso:** `dailyCapJob.computeEquity` (linha ~108) tem guard `coin.startsWith('LD') && length>3` que EXCLUI qualquer `LD*` do equity (feito pra dust tipo LDGUN/LDBABY). Mas `LDLTC` é valor REAL/resgatável → equity caiu $148,8→$109 → falso −26,76% → cap −5% tripou. Timeline: 02:29 LTC ainda spot (equity $148,79, sem trip) → varrido pro Earn → 04:11 trip.
> 14	2. **Venda no-loss QUEBRADA:** o Farm Sell precisa de LTC **spot** pra vender; com tudo em `LDLTC` o sell falharia (saldo spot 0) quando LTC bouncasse ao alvo.
> 15	
> 16	**RESOLVIDO 2026-06-20:**
> 17	- **Dono:** resgatou `LDLTC`→LTC spot (voltou **0,90709440 = o TOTAL**, provando que os "0,017 LTC sumidos" eram só artefato contábil do Earn, NÃO vazamento) + **desligou o auto-subscribe**.
> 18	- **Código:** fix do `computeEquity` deployado+commitado+pushado (**`c6d0853`**, gate QA PASS + TL APPROVE, zero must-fix): marca `LD*` a mercado pelo subjacente via `TRACKED_BASES` (LDLTC→preço LTC, LDUSDC→stable; dust sem par→ignored; trackado frio→cold/fail-safe). Smoke vivo: equity voltou a ler ~$149 valued, `ignored` sem LDLTC.
> 19	- **HALT limpo** via `POST /system/daily-cap/reset` (re-baseline correto **$149,07**) DEPOIS do resgate. Venda no-loss do Farm re-armada (id10 a $44,39; `MEMORY['LTC:WALLET']=0,907` sincronizada; `calcQty` capa na carteira sozinho).
> 20	
> 21	**FEITO 2026-06-20 (lote `457e25a`, gate QA PASS + TL APPROVE):** (a) **ruído `[PAPER]` era PUSH, NÃO Telegram** (canal = `app-em.sendMessage`→`push.send`, não `telegramNotify`; o audit ESTAVA certo, eu me equivoquei rastreando) → suprimido o push p/ resultados `[PAPER]` (mantém o WS broadcast p/ UI). (b) **falha silenciosa**: `evalDecision` catch (`beholder.js`) agora ALERTA o dono no Telegram quando automação REAL falha na execução (ex.: `no LTC in wallet`), deduped por chave exata `autofail:<id>` (NÃO Jaccard — esse é só do agente), `[PAPER]` excluído.
> 22	
> 23	**DÉBITOS ainda abertos:** (1) `loadWallet`/`calcQty` (`app-em.js:101`/`beholder.js:212`) não enxergam `LD*` → se o auto-subscribe religar, a venda re-falha (mas agora NOTIFICA, via (b)). (2) **bloqueio por HALT/teto segue silencioso no Telegram** — morre em `placeOrder` (`return {type:'error'}`) ANTES do catch do `evalDecision`; cobrir = alertar no return de `placeOrder` com dedup próprio. (3) **doutrina do agente LLM**: ainda re-litiga "baseline/trend inativas" todo ciclo (canary) e não detecta falhas por conta própria — agora menos crítico pois o BACKEND alerta direto via (b); ajuste de prompt em `tradeux-agent` fica p/ depois.
> 24	
> 25	Liga com [[tradeux-mainnet-go-live]] (cap diário −5% / botão de pânico) e [[tradeux-farm-funnel-backtest]].
> 26	
> ```

## 🤖 Claude *(17:00:17)*

Now I have strong context. Let me read the actual money-path code: exchange.js (riskGuard), beholder.js (calcQty/placeOrder), riskState.js, dailyCapJob, and the MCP vault guard.

## 🤖 Claude *(17:00:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "find /home/gcrux-tradeux/tradeux/backend/src -type f -name '*.js' | grep -iE 'exchange|risk|beholder|app-em|order|daily|cap|system|automation' | head -50",
  "description": "Locate money-path source files"
}
```

## 🤖 Claude *(17:00:21)*

API Error: Internal server error

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrux-tradeux/tradeux/backend/src/app-em.js
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js
> /home/gcrux-tradeux/tradeux/backend/src/dailyCapJob.js
> /home/gcrux-tradeux/tradeux/backend/src/dailyProfitJob.js
> /home/gcrux-tradeux/tradeux/backend/src/utils/exchange.js
> /home/gcrux-tradeux/tradeux/backend/src/repositories/ordersRepository.js
> /home/gcrux-tradeux/tradeux/backend/src/repositories/orderTemplatesRepository.js
> /home/gcrux-tradeux/tradeux/backend/src/repositories/automationsRepository.js
> /home/gcrux-tradeux/tradeux/backend/src/models/orderTemplateModel.js
> /home/gcrux-tradeux/tradeux/backend/src/models/paperOrderModel.js
> /home/gcrux-tradeux/tradeux/backend/src/models/orderModel.js
> /home/gcrux-tradeux/tradeux/backend/src/models/automationModel.js
> /home/gcrux-tradeux/tradeux/backend/src/routers/beholderRouter.js
> /home/gcrux-tradeux/tradeux/backend/src/routers/orderTemplatesRouter.js
> /home/gcrux-tradeux/tradeux/backend/src/routers/systemRouter.js
> /home/gcrux-tradeux/tradeux/backend/src/routers/ordersRouter.js
> /home/gcrux-tradeux/tradeux/backend/src/routers/automationsRouter.js
> /home/gcrux-tradeux/tradeux/backend/src/routers/exchangeRouter.js
> /home/gcrux-tradeux/tradeux/backend/src/controllers/systemController.js
> /home/gcrux-tradeux/tradeux/backend/src/controllers/orderTemplatesController.js
> /home/gcrux-tradeux/tradeux/backend/src/controllers/ordersController.js
> /home/gcrux-tradeux/tradeux/backend/src/controllers/exchangeController.js
> /home/gcrux-tradeux/tradeux/backend/src/controllers/beholderController.js
> /home/gcrux-tradeux/tradeux/backend/src/controllers/automationsController.js
> ```

## 🤖 Claude *(17:03:59)*

API Error: 529 Overloaded. This is a server-side issue, usually temporary — try again in a moment. If it persists, check https://status.claude.com.

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

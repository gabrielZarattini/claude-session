# Session agent-a9eceaff0b3d4fecd
**Date:** 2026-06-21 | **Session ID:** `agent-a9eceaff0b3d4fecd`

---

## 👤 User *(15:04:02)*


CONTEXTO DO PROJETO (TradeUX, bot Binance Spot + agente LLM):
- Capital REAL ~$149 USDT, MAINNET LIVE. Spot-only. SEM futuros/alavancagem (refutado + fora de escopo).
- BTC e COFRE (nunca vende a base BTC; trava fail-closed no MCP). Negocia alts vs USDT (LTC/BNB/ADA) + trend BTC.
- Fee Binance taker 0,1% (ou 0,075% com desconto BNB). Owner decidiu: VALIDAR no paper antes de escalar real.
- Claude NUNCA vira o HALT.

JA REFUTADO (NAO re-propor, NAO re-refutar — citar e seguir):
- +3 BTC de alfa absoluto long-only spot = IMPOSSIVEL (~1350x).
- HFT / scalp 1m = MORTO (EV -0,16%/trade medido; fee+whipsaw).
- Frequencia / "verde diario" = REFUTADO (8/8 combos 5m/15m EV liquido < 0).
- Harvester (dislocacao -3%) = MORTO no mainnet (book simulado = FAIR mesma venue); re-ancorado ao HIGH rolante = EV NEGATIVO (17/18 configs).
- Grid simetrico = sangra o cofre (vende por nivel sem rastrear o que comprou).
- Bear-capture via futuros = falso positivo (+88% vs +338% do regime-gating) + futuros fora de escopo.
- Buy&Hold e DIFICILIMO de bater em retorno BRUTO; o edge do trading ativo e RISCO-AJUSTADO (drawdown), nao alfa.
- "Fable 5 / Polymarket 205x" = golpe de referral.

EDGES VALIDADOS (o que FUNCIONA):
- Regime-gating corta drawdown (bear: regime -7% vs B&H -27%).
- Trend (SMA50/200, comprado no bull / caixa no bear) = motor do bull (+22% a +147% em janelas de bull).
- Farm no-loss (DCA na alta de RSI<35, vende a custo*1.012) = alfa marginal, baixo risco.
- %-sizing (reinvestir lucro) = motor do exponencial, MAS so COM edge de EV+ liquido validado.

FONTES PRA LER (use Read/Grep/Glob/Bash):
- Memorias: /home/ubuntu/.claude/projects/-home-gcrux-tradeux/memory/*.md (esp. tradeux-farm-funnel-backtest, tradeux-trend-following, tradeux-bear-capture-research, tradeux-harvester-experiment, tradeux-agent-500k-validation, tradeux-strategy-engine, tradeux-1m-scalping-and-cockpit)
- ~/STRATEGY-3BTC-assessment.md, ~/RESEARCH-bear-capture.md (home do usuario ubuntu: /home/ubuntu/)
- /home/gcrux-tradeux/tradeux/docs/STRATEGY-farm-funnel.md
- /home/gcrux-tradeux/tradeux/backend/backtest-results/ (resultados JSON/CSV)
- /home/gcrux-tradeux/tradeux/backend/scripts/backtest.js e backtest-farm-funnel.js (o que da pra backtestar: klines 1h mainnet, walk-forward, fee 0,1%)


LEDGER consolidado (use como verdade-base; NAO re-proponha refutados):
{"constraints":["Capital REAL ~$148,84 USDT, MAINNET LIVE, spot-only, sem futuros/alavancagem (tradeux-mainnet-go-live.md:12; CLAUDE.md 'Binance Spot'). Escala: +3 BTC e impossivel (~1350x o patrimonio) — tradeux-mainnet-go-live.md:34.","Fee Binance = 0,1%/lado taker em TODO backtest (backtest.js:24 e backtest-farm-funnel.js:28 'FEE = 0.001'); 0,075% com desconto BNB. Em SPOT maker==taker — NAO existe rebate (so Futures/VIP) — tradeux-1m-scalping-and-cockpit.md:14.","COFRE BTC nunca vende a base: trava fail-closed isBtcVaultSymbol vive SO no caminho MCP (place_order), NAO no beholder/exchange — tradeux-vault-guard / tradeux-mainnet-go-live.md:36,39. Grupo 'baseline' inclui venda do cofre coberta so por HALT+riskGuard.","Claude NUNCA vira o HALT — repetido em todas as memorias (tradeux-mainnet-go-live, harvester, strategy-engine). Flip real = .env TRADING_HALT=false + restart (derruba o env floor); POST /system/halt {on:false} so solta o manual.","Agente LLM NAO coloca ordem real: ALLOW_TRADING=false verificado no container + MCP write tools throw (tradeux-mainnet-go-live.md:36). Guardrails de notional sao prompt-level; o cap duro e backend (riskState/exchange.js chokepoint).","Caps de risco DUROS no backend (exchange.js chokepoint por-ordem, QUENTE via riskState.isHalted): teto por-ordem MAX_ORDER_NOTIONAL_USDT=$25 + teto de exposicao do Farm FARM_MAX_NOTIONAL_USDT=$25/simbolo + cap diario -5% (dailyCapJob, Earn LD* excluido) — tradeux-mainnet-go-live.md:26,49,50.","Estado LIVE atual (2026-06-19/20): dono destravou o floor; canary FARM-ONLY (alts LTC/BNB/ADA no-loss, 6 autos), Trend e Baseline PARADOS. Pos-1a ordem real: Farm DCA 3x em LTC, COMPRAS desligadas, so VENDAS armadas (3/6) — tradeux-mainnet-go-live.md:42-53. SEMPRE conferir GET /system/halt no inicio da sessao.","GOTCHA de calculo (money-path): MEMORY['<sym>:FARM_DCA'].cost = PRECO MEDIO/unidade (totalCost/totalQty), NAO USDT investido; investido = qty*cost. Condition do Farm Sell = bestBid > cost*1.012 (preco vs preco) — tradeux-mainnet-go-live.md:51.","GOTCHA de dado: tabela orders MISTURA testnet+mainnet; pra P&L/posicao REAL SEMPRE filtrar isTestnet=false (senao soma fantasmas — ex. 22 LTC/$997 de 15/jun eram testnet) — tradeux-mainnet-go-live.md:52.","No-loss do Farm vende SO acima do custo: backtest minProfit=0,6% (GP.minProfit=0.006, backtest-farm-funnel.js:45); live buffer = cost*1.012 (1,2% >> round-trip de fee). 'No-loss' NAO elimina perda — converte em INVENTARIO PRESO (pior no bear) — STRATEGY-farm-funnel.md:91, backtest-farm-funnel.js:11-12.","BTC nao e farmado (e o cofre); id3 Baseline Sell BTCUSDT pausada (vendia BTC sem gate de lucro = a sangria que motivou o estudo) — STRATEGY-farm-funnel.md:74; id2 Baseline Buy BTC isActive=0 (acumulador pelado sem venda) — tradeux-mainnet-go-live.md:32.","Edge do trading ativo e RISCO-AJUSTADO (drawdown menor), NAO alfa absoluto: em bull o melhor e segurar (B&H domina), em bear todo long-only perde — STRATEGY-3BTC-assessment.md:23-24, backtest-1h-365d.md:130-131."],"refuted":[{"idea":"+3 BTC de alfa absoluto long-only spot","verdict":"IMPOSSIVEL (~1350x)","evidence":"tradeux-mainnet-go-live.md:34 ('+3 BTC e impossivel (1.350x)'); STRATEGY-3BTC-assessment.md:23. $148 spot ~ FLAT no mes; sem rendimento diario nessa escala."},{"idea":"HFT / scalping 1m como motor de P&L","verdict":"MORTO (EV negativo por trade)","evidence":"Backtest fresco em cache real BTCUSDT-1m-60d (86.400 velas): -0,14% a -0,23% liquido POR TRADE em TODAS parametrizacoes (k_ATR 1-2, horiz 10-20, fee 0,075/0,10%); win 35-48% sub-breakeven — tradeux-1m-scalping-and-cockpit.md:13. Move mediano 1m ~0,036-0,15% < custo ~0,15-0,20%. Cockpit reporta EV/trade net -0,16%, pHit 0,6%."},{"idea":"Frequencia / 'verde diario' (5m/15m)","verdict":"REFUTADO (8/8 EV liquido < 0)","evidence":"Workflow paper-frequencia-research, 8 combos 4sym x 5m/15m, mainnet+fee 0,1%/lado: 8/8 EV/trade liquido NEGATIVO (win 52-68% mas EV<0; mais frequencia = pior) — tradeux-strategy-engine.md:31. Verdes so em gate-regime esparso (caixa-no-bear), NAO frequencia."},{"idea":"Harvester de dislocacao -3% (id22-25)","verdict":"MORTO no mainnet (artefato testnet) + EV- no re-design","evidence":"Codigo: FAIR=lastPrice mainnet (fairPriceService.js:33) + book sintetico spread-0 do miniTicker (app-em.js:38) = mesma venue → gatilho bestAsk<FAIR*0.97 estruturalmente inalcancavel. Dado: 0 ordens harvester no mainnet (orders=259 TODAS testnet); +1529 USDT eram 100% testnet. Re-ancorar ao HIGH rolante: backtest dado-real (klines 1h, fee 0,1%/lado, 3sym x 4 regimes) = 17/18 configs P&L NEGATIVO (unica + = +$14,78/~$12k = +0,12%, ruido, 36% maxDD) — tradeux-harvester-experiment.md:32. id22-25 isActive=0; NAO reativar."},{"idea":"Grid simetrico nativo do Beholder (gridEval/generateGrids)","verdict":"REJEITADO (sangra o cofre)","evidence":"id21 operou 26 ordens MAS vende por nivel DIRETO DA CARTEIRA sem rastrear inventario → 24 SELL vs 2 BUY → drenou ~0,0044 BTC do cofre — tradeux-harvester-experiment.md:16. Script com aviso 'NAO-ATIVAR'. Solucao: padrao bucket {qty,cost} (vende so o que comprou)."},{"idea":"Bear-capture via futuros (short / trend bilateral)","verdict":"FALSO POSITIVO no ciclo + fora de escopo","evidence":"Backtest proprio bilateral (backtest-futures-trend.js, custo 0,07%/lado + funding 8h REAL): captura a queda ISOLADA (bear: trendBi NET +5,01% medio vs B&H -34,42%, 3/4 sym — backtest-futures-1h-bear-365d.md:51) MAS no CICLO e dominado pelo regime-gating (ciclo +88% vs +338%); no bull longGated +79,64% vs B&H +338,21% (sacrifica upside) — backtest-futures-1h-bull-end2024-04-01.md:52,54. maxDD -51% a 1x; Sharpe liq 0,31→~0,15 pos-haircut; ADX PIORA (whipsaw). DECISAO: NAO construir modulo de short."},{"idea":"Maker-rebate em Binance SPOT","verdict":"REFUTADO (nao existe)","evidence":"Na Binance SPOT maker==taker (0,075% com BNB nos 2 lados); rebate so em Futures/VIP — tradeux-1m-scalping-and-cockpit.md:14. Verificadores rejeitaram a abordagem."},{"idea":"toxicity/VPIN do flow oracle como forecast direcional","verdict":"REFUTADO 0-3 (rebaixado a nowcasting)","evidence":"Deep research (24 fontes): VPIN-como-forecasting de jumps de BTC refutado 0-3; OFI e nowcasting (~2 price changes/~10s, base equities) — tradeux-bear-capture-research.md:18. toxicity rebaixada a gatilho de timing/execucao (commit c67d6bc)."},{"idea":"Bater Buy&Hold em RETORNO BRUTO num bull","verdict":"DIFICILIMO (B&H domina)","evidence":"Bull 180d: B&H medio +293,61% OOS, melhor ativa (sempre-trend) +146,57%, regime-switch V2 +50,55% — backtest-1h-180d-end2024-04-01.md:103-104. Bate B&H em 0/4 simbolos. Cada saida custa upside + fee."},{"idea":"'Fable 5 / Polymarket 205x' ($11k→$300k)","verdict":"GOLPE de referral","evidence":"Link polymarket.com/profile/...?via=ace-cjyf; narrativa fabricada pra dirigir cadastro/deposito/copy-trade — tradeux-1m-scalping-and-cockpit.md:24. NAO clicar/depositar/copy-tradar."}],"validated_edges":[{"edge":"Regime-gating: ficar em CAIXA no bear corta o drawdown (o maior edge)","magnitude":"BTC 365d-bear OOS: regime-switch V2 +0,61% (agregado 4 sym) vs B&H -23,82%; bate B&H em 4/4 (backtest-1h-365d.md:100,104). BTC isolado: regime-switch ~-7% vs B&H ~-27% OOS (backtest-1h-365d.md:131). Sem-supervisao no farm-funnel: bear 2022 retorno equity -1,7% (farm-so) vs B&H ~-60% nos pares.","evidence":"backtest.js regimeSwitch V2 (histerese, regimeWindowV2:233); backtest-1h-365d.md secao agregada; STRATEGY-3BTC-assessment.md:18."},{"edge":"Trend (SMA50/200, comprado no bull / caixa no bear) = motor do bull","magnitude":"Farm+Trend+funil no bull 2023-24: retorno equity +22,6% (BTC/ano 16x o farm), drivers ETH+52%/SOL+50%/AVAX+49%/LINK+41% (farm-funnel-1h-full-macro500.md:38, tabela:30-36). In-sample 180d SOL trend SMA20/50 +344,93% (backtest-1h-180d:81); sensibilidade 180d trend 50/200 melhor que 20/50. Em janelas de bull a doc cita +22% a +147%.","evidence":"backtest-farm-funnel.js gridTrendFunnel (smaCross:251); farm-funnel-1h-full-macro500.md; tradeux-trend-following.md."},{"edge":"Farm no-loss (DCA em RSI<35, vende a custo*1.012) = alfa marginal, baixo risco","magnitude":"Farm-so + macro (farm-funnel-1h-macro500.md): recente -3,54%, bull +0,89%, bear -1,74% retorno equity; maxDD medio -4,68%/-0,31%/-11,03%; BTC/ano +0,00075 a +0,01057 por $8000 → +3 BTC = 'seculos'. STRATEGY-farm-funnel.md:53: farm-so -3,5%/+0,9%/-1,7%. Drawdown muito menor que o trend.","evidence":"backtest-farm-funnel.js gridFunnel (vendas no-loss:202-212); farm-funnel-1h-macro500.md sintese:60-62; STRATEGY-farm-funnel.md:53."},{"edge":"Menos trades perdem menos (fee+whipsaw punem overtrading)","magnitude":"365d MR: RSI 25/75 -19,34% (~17,5 trades) vs 30/70 -38,59% (~31,8) vs 35/65 -44,01% (~53,5); trend 50/200 -10,90% (~27,5) vs 20/50 -25,46% (~92,8) vs 10/30 -34,44% (~167,3) — backtest-1h-365d.md:113-126. Calibracao recomendada: RSI 25/75 (nao 30/70), SMA 50/200 (nao 20/50).","evidence":"backtest.js runCalibration / secao de sensibilidade; backtest-1h-365d.md:128-133; STRATEGY-3BTC-assessment.md:20,27."},{"edge":"Switch de regime (trend on em bull, farm-so em lateral) e o melhor compromisso sem supervisao","magnitude":"Farm+Trend+Switch (15m, config final): recente -5,5% / bull +14,4% / bear -0,4% (STRATEGY-farm-funnel.md:56). 15m bate o 1h em todos os regimes (granularidade menor = mais farm, menos inventario preso). Switch reduz o whipsaw do trend sem matar o upside.","evidence":"STRATEGY-farm-funnel.md:53-61; backtest-farm-funnel.js (GP.trendSwitch / SC()/tfScale)."},{"edge":"%-sizing (reinvestir lucro) = motor do exponencial — SO com EV+ liquido validado","magnitude":"Condicional, nao medido isolado: alavanca de escala 3→10 = aumento de sizing sobre borda validada (STRATEGY-3BTC-assessment.md:37-41); farm-funnel.md observa 'dobrar capital ~dobra a taxa (ate teto de liquidez/lotes)'. NAO ativar sem edge EV+ liquido por backtest/paper.","evidence":"STRATEGY-3BTC-assessment.md:37-41; farm-funnel-1h-macro500.md leitura:65."}],"backtestable":["backtest.js: long-only spot, klines 1h REAIS da Binance mainnet (HOSTS api.binance.com/data-api.binance.vision/api.binance.us, paginado 1000, cache em backtest-data/ gitignored), ~1 ano, multi-simbolo (default BTC/ETH/BNB/SOL). Flags: --days --interval --symbols --end --calibrate --compareRegime.","Indicadores Wilder self-contained (backtest.js:83-153): RSI(14), ATR(14), DMI completo ADX+pDI/mDI(14), SMA(qualquer), vol realizada anualizada. Sem libs externas (so built-ins Node).","Engine sem lookahead: execucao no OPEN do candle SEGUINTE ao sinal (backtest.js:161-163); net de fee 0,1%/lado nos 2 lados; metricas: netReturn, nTrades, winRate, avgTrade, maxDD, Sharpe anualizado (backtest.js:170-175).","Estrategias prontas: meanReversion(RSI lo/hi), trendFollow(SMA fast/slow), longFlat(SMA200), gatedMeanReversion (RSI gateada por close>SMA200 = modelo da id2 viva). Adicionar estrategia = passar um signalFn(i,inPos)→'BUY'|'SELL'|null (backtest.js:156 — ponto de extensao citado em strategy-engine.md:46).","Regime classifier 3-estados (bear/trend/range/mixed) por ADX+SMA200, com V1 (regimeWindow3:216) e V2 com HISTERESE anti-whipsaw (regimeWindowV2:233; bandas entrada/saida 0.60/0.45, 25/22, 20/23) — mesma logica replicada por-barra em backtest-farm-funnel.js regimeSeries:162.","Walk-forward OUT-OF-SAMPLE: janelas de 30d, regime ex-ante (janela anterior) escolhe a estrategia (bear→caixa/trend→trend/range-mixed→MR); agrega total composto + avg/janela + win% + flips; agregado cross-simbolo (edge vs sorte) — backtest.js:253-278,412-432.","backtest-farm-funnel.js: engine de LOTES (grid no-loss) + funil pra BTC — o backtest.js all-in/all-out NAO serve pra isso. Mede equity TOTAL (caixa + inventario marcado-a-mercado + BTC acumulado), inventario preso no fim, deployedPeak, exposicao, %bear, maxDD — separa farm real de lucro contabil ilusorio (backtest-farm-funnel.js:185-248).","3 regimes de ciclo pre-definidos no farm-funnel (PERIODS:58-62): 'recente ~365d', 'bull 2023-24' (180d end 2024-04-01), 'bear 2022' (365d end 2023-01-01). 8 alts default. Engine 'full' (gridTrendFunnel:262) coordena farm+trend+funil fiel ao runtime (trend sai no death cross = corta no prejuizo; farm pausa em trend/bear).","Knobs do farm-funnel: --capital --lot --maxlots --step --profit --rsibuy --macrosma --macroslope --trendlot --trendadx --switch --full --interval --tfscale (escala periodos por timeframe). Reproducao documentada em STRATEGY-farm-funnel.md:100-106.","Paper/Shadow Engine (NAO e backtest, mas valida ao vivo sob HALT): broker VIRTUAL roteado por prefixo [PAPER] no name → fill ao MINI_TICKER mainnet REAL + fee real (computeNet) + slippage (PAPER_SLIPPAGE_BPS), grava em paperOrders/paperPositions sem tocar Binance. GET /analysis/paper; paperReviewJob notifica nos marcos 5/15/30/60/120 round-trips — tradeux-strategy-engine.md:19-22,50.","LIMITES do harness: (a) timeframe minimo testado e 1m mas o cache 1m so existe pra BTCUSDT (60d); estrategias live id2/id3 usam RSI 1m que o backtest 1h NAO replica exatamente (backtest.js:337 caveat). (b) Sem modelagem de book/profundidade/partial-fills/slippage (so fee fixo; o farm-funnel assume fill ao open/close). (c) Futures (backtest-futures-trend.js) ja existe com funding 8h real, mas futures esta FORA DE ESCOPO e foi refutado. (d) NAO modela impacto de mercado nem MIN_NOTIONAL/stepSize reais (a frag. de calcQty/-1013 so aparece ao vivo)."]}

SEU ANGULO — EXPANSAO CROSS-SIMBOLO: aumentar a CONTAGEM de oportunidades no-loss do Farm via mais pares (scanner cross-simbolo, Bloco C do plano). Quantifique: mais simbolos aumenta o numero de round-trips mas NAO o edge/trade. Quais pares (liquidez/fee/correlacao) e quais riscos (concentracao, capital fragmentado a $149)?

Proponha 1-3 alavancas CONCRETAS e EV-honestas. Cada uma com mecanismo, magnitude esperada honesta, do que depende (capital/edge/simbolos/custo), se e nova vs refutados, e o caminho de validacao (backtest/paper, quanto).

## 🤖 Claude *(15:04:06)*

Vou analisar as fontes para quantificar honestamente a alavanca de expansão cross-símbolo do Farm no-loss. Deixa eu ler o material-chave primeiro.

## 🤖 Claude *(15:04:07)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/scripts/backtest-farm-funnel.js"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env node
> 2	/*
> 3	 * TradeUX — Backtest da estratégia "Farm-and-Funnel" (grid no-loss multi-alt + funil pra BTC).
> 4	 * Self-contained (built-ins do Node). Reusa a infra de dados/indicadores do backtest.js.
> 5	 *
> 6	 * Tese (do dono): farmar USDT com grid "no-loss" nas ALTS (compra dip espaçado, vende SÓ com lucro,
> 7	 * gateado por regime !=bear) e escoar o LUCRO REALIZADO para BTC (funil) → acumular BTC ao longo do tempo.
> 8	 * A meta (+3 BTC) é o tamanho da reserva de BTC acumulada pelo funil.
> 9	 *
> 10	 * Honestidade embutida: o "no-loss" não some com o prejuízo, ele vira INVENTÁRIO preso. Por isso o
> 11	 * relatório mede também o equity TOTAL (caixa + inventário marcado-a-mercado + BTC), o inventário preso
> 12	 * no fim, o pico de capital empregado e o maxDD — pra separar farm real de lucro contábil ilusório.
> 13	 *
> 14	 * Exec no OPEN do candle seguinte ao sinal (sem lookahead). Tudo net de fee. Dados: Binance klines reais.
> 15	 *
> 16	 * Uso: node scripts/backtest-farm-funnel.js [--interval=1h] [--alts=BNBUSDT,ETHUSDT,...]
> 17	 *      [--capital=1000] [--lot=100] [--maxlots=8] [--step=0.015] [--profit=0.006] [--rsibuy=35]
> 18	 */
> 19	'use strict';
> 20	const https = require('https');
> 21	const fs = require('fs');
> 22	const path = require('path');
> 23	
> 24	// ---------- config ----------
> 25	const args = Object.fromEntries(process.argv.slice(2).map(a => {
> 26	  const m = a.match(/^--([^=]+)=?(.*)$/); return m ? [m[1], m[2] || true] : [a, true];
> 27	}));
> 28	const FEE = 0.001;                                    // 0.1%/lado (taker)
> 29	const INTERVAL = args.interval || '1h';
> 30	const ALTS = (args.alts || 'BNBUSDT,ETHUSDT,SOLUSDT,XRPUSDT,ADAUSDT,LINKUSDT,LTCUSDT,AVAXUSDT').split(',');
> 31	const BTC = 'BTCUSDT';
> 32	const HOSTS = ['api.binance.com', 'data-api.binance.vision', 'api.binance.us'];
> 33	const MS_PER = { '1m': 60e3, '5m': 5 * 60e3, '15m': 15 * 60e3, '30m': 30 * 60e3, '1h': 3600e3, '4h': 4 * 3600e3, '1d': 24 * 3600e3 };
> 34	const BAR_MS = MS_PER[INTERVAL] || 3600e3;
> 35	const DATA_DIR = path.join(__dirname, '..', 'backtest-data');
> 36	const OUT_DIR = path.join(__dirname, '..', 'backtest-results');
> 37	
> 38	// grid params (default = ponto de partida sensato, NÃO otimizado; varredura via runSweep)
> 39	const GP = {
> 40	  capital: +args.capital || 1000,    // USDT de trabalho por alt
> 41	  lotUSDT: +args.lot || 100,         // tamanho de cada compra
> 42	  maxLots: +args.maxlots || 8,       // teto de lotes abertos (limita inventário/exposição)
> 43	  gridStep: +args.step || 0.015,     // espaçamento mínimo entre compras (1.5%)
> 44	  minProfit: +args.profit || 0.006,  // lucro líquido alvo por lote (0.6%, já acima do round-trip de fee)
> 45	  rsiBuy: +args.rsibuy || 35,        // timing de compra (RSI abaixo disso)
> 46	  macroSma: args.macrosma !== undefined ? +args.macrosma : 0,  // 0=off; senão filtro macro: SMA longa não-caindo
> 47	  macroSlope: +args.macroslope || 240,                         // lookback do slope da SMA macro
> 48	  trendLot: +args.trendlot || 500,    // tamanho da posição de trend (SMA50/200) por entrada
> 49	  trendAdx: +args.trendadx || 0,      // 0=off; senão exige ADX>=isto no golden cross (confirma força de tendência)
> 50	  trendSwitch: !!args.switch,         // true = switch de regime: trend só entra com filtro macro OK (tendência de fundo subindo)
> 51	  full: !!args.full,                  // true = arquitetura completa (farm + trend coordenados + funil)
> 52	  tfScale: +args.tfscale || 1,        // escala dos períodos de SMA/regime p/ manter horizonte temporal entre timeframes
> 53	};
> 54	const SC = n => Math.max(2, Math.round(n * GP.tfScale));   // período escalado pelo timeframe
> 55	const WARM = Math.max(SC(210), GP.macroSma ? GP.macroSma + GP.macroSlope + 10 : 0);
> 56	
> 57	// janelas de regime (bull/bear/range) — robustez por ciclo
> 58	const PERIODS = [
> 59	  { label: 'recente (~últ. 365d)', days: 365, end: null },
> 60	  { label: 'bull 2023-24', days: 180, end: '2024-04-01' },
> 61	  { label: 'bear 2022', days: 365, end: '2023-01-01' },
> 62	];
> 63	
> 64	// ---------- util ----------
> 65	const mean = a => a.reduce((s, x) => s + x, 0) / (a.length || 1);
> 66	const std = a => { if (a.length < 2) return 0; const m = mean(a); return Math.sqrt(mean(a.map(x => (x - m) ** 2))); };
> 67	const pct = x => (x * 100).toFixed(2) + '%';
> 68	const round = (x, n = 4) => Number.isFinite(x) ? Number(x.toFixed(n)) : null;
> 69	const fmt = (x, n = 2) => Number.isFinite(x) ? x.toFixed(n) : '—';
> 70	
> 71	function httpsGetJSON(host, pathUrl) {
> 72	  return new Promise((res, rej) => {
> 73	    https.get({ host, path: pathUrl, headers: { 'User-Agent': 'tradeux-backtest' } }, r => {
> 74	      let d = ''; r.on('data', c => d += c);
> 75	      r.on('end', () => { try { res({ status: r.statusCode, body: JSON.parse(d) }); } catch (e) { res({ status: r.statusCode, body: d }); } });
> 76	    }).on('error', rej);
> 77	  });
> 78	}
> 79	
> 80	// ---------- data fetch (klines paginados + cache em disco) ----------
> 81	async function fetchAllKlines(symbol, days, end) {
> 82	  const cacheFile = path.join(DATA_DIR, `${symbol}-${INTERVAL}-${days}d${end ? '-end' + end : ''}.json`);
> 83	  if (fs.existsSync(cacheFile)) {
> 84	    const c = JSON.parse(fs.readFileSync(cacheFile, 'utf8'));
> 85	    if (c.length > 100) return c;
> 86	  }
> 87	  const endTime = end ? Date.parse(end + 'T00:00:00Z') : Date.now();
> 88	  const startTime = endTime - days * 24 * 3600e3;
> 89	  let cursor = startTime, all = [], host = null;
> 90	  for (const h of HOSTS) {
> 91	    const r = await httpsGetJSON(h, `/api/v3/klines?symbol=${symbol}&interval=${INTERVAL}&limit=1`).catch(() => null);
> 92	    if (r && r.status === 200 && Array.isArray(r.body)) { host = h; break; }
> 93	  }
> 94	  if (!host) throw new Error(`nenhum host Binance alcançável para ${symbol}`);
> 95	  while (cursor < endTime) {
> 96	    const url = `/api/v3/klines?symbol=${symbol}&interval=${INTERVAL}&startTime=${cursor}&limit=1000`;
> 97	    const r = await httpsGetJSON(host, url);
> 98	    if (r.status !== 200 || !Array.isArray(r.body) || r.body.length === 0) break;
> 99	    const batch = r.body.map(k => ({ t: k[0], open: +k[1], high: +k[2], low: +k[3], close: +k[4], vol: +k[5] }));
> 100	    all.push(...batch);
> 101	    cursor = batch[batch.length - 1].t + BAR_MS;
> 102	    if (batch.length < 1000) break;
> 103	  }
> 104	  const seen = new Set(); const out = [];
> 105	  for (const c of all) { if (!seen.has(c.t)) { seen.add(c.t); out.push(c); } }
> 106	  out.sort((a, b) => a.t - b.t);
> 107	  fs.mkdirSync(DATA_DIR, { recursive: true });
> 108	  fs.writeFileSync(cacheFile, JSON.stringify(out));
> 109	  return out;
> 110	}
> 111	
> 112	// ---------- indicadores (Wilder) ----------
> 113	function rsiSeries(close, period = 14) {
> 114	  const out = Array(close.length).fill(NaN);
> 115	  if (close.length <= period) return out;
> 116	  let gain = 0, loss = 0;
> 117	  for (let i = 1; i <= period; i++) { const d = close[i] - close[i - 1]; if (d >= 0) gain += d; else loss -= d; }
> 118	  let ag = gain / period, al = loss / period;
> 119	  out[period] = al === 0 ? 100 : 100 - 100 / (1 + ag / al);
> 120	  for (let i = period + 1; i < close.length; i++) {
> 121	    const d = close[i] - close[i - 1];
> 122	    ag = (ag * (period - 1) + (d > 0 ? d : 0)) / period;
> 123	    al = (al * (period - 1) + (d < 0 ? -d : 0)) / period;
> 124	    out[i] = al === 0 ? 100 : 100 - 100 / (1 + ag / al);
> 125	  }
> 126	  return out;
> 127	}
> 128	function trueRange(high, low, close, i) {
> 129	  if (i === 0) return high[i] - low[i];
> 130	  return Math.max(high[i] - low[i], Math.abs(high[i] - close[i - 1]), Math.abs(low[i] - close[i - 1]));
> 131	}
> 132	function dmiSeries(high, low, close, period = 14) {
> 133	  const n = close.length;
> 134	  const adx = Array(n).fill(NaN);
> 135	  if (n <= 2 * period) return adx;
> 136	  const plusDM = Array(n).fill(0), minusDM = Array(n).fill(0), tr = Array(n).fill(0);
> 137	  for (let i = 1; i < n; i++) {
> 138	    const up = high[i] - high[i - 1], dn = low[i - 1] - low[i];
> 139	    plusDM[i] = (up > dn && up > 0) ? up : 0;
> 140	    minusDM[i] = (dn > up && dn > 0) ? dn : 0;
> 141	    tr[i] = trueRange(high, low, close, i);
> 142	  }
> 143	  let sTR = 0, sP = 0, sM = 0;
> 144	  for (let i = 1; i <= period; i++) { sTR += tr[i]; sP += plusDM[i]; sM += minusDM[i]; }
> 145	  const dx = Array(n).fill(NaN);
> 146	  const dxAt = (sP, sM, sTR) => { const pdi = sTR === 0 ? 0 : 100 * sP / sTR, mdi = sTR === 0 ? 0 : 100 * sM / sTR; const den = pdi + mdi; return den === 0 ? 0 : 100 * Math.abs(pdi - mdi) / den; };
> 147	  dx[period] = dxAt(sP, sM, sTR);
> 148	  for (let i = period + 1; i < n; i++) { sTR = sTR - sTR / period + tr[i]; sP = sP - sP / period + plusDM[i]; sM = sM - sM / period + minusDM[i]; dx[i] = dxAt(sP, sM, sTR); }
> 149	  let a = 0; for (let i = period + 1; i <= 2 * period; i++) a += dx[i]; a /= period;
> 150	  adx[2 * period] = a;
> 151	  for (let i = 2 * period + 1; i < n; i++) { a = (a * (period - 1) + dx[i]) / period; adx[i] = a; }
> 152	  return adx;
> 153	}
> 154	function smaSeries(close, period) {
> 155	  const out = Array(close.length).fill(NaN); let s = 0;
> 156	  for (let i = 0; i < close.length; i++) { s += close[i]; if (i >= period) s -= close[i - period]; if (i >= period - 1) out[i] = s / period; }
> 157	  return out;
> 158	}
> 159	
> 160	// regime por barra (rolling), réplica do classifier ao vivo: belowFrac das últ. `win` velas vs SMA200
> 161	// + ADX, com histerese anti-whipsaw (mesmos limiares do regimeWindowV2 do backtest.js).
> 162	function regimeSeries(close, sma200, adx, win = 101) {
> 163	  const n = close.length, reg = Array(n).fill('warm');
> 164	  let prev = null;
> 165	  for (let i = 0; i < n; i++) {
> 166	    if (i < win || !Number.isFinite(sma200[i])) { reg[i] = 'warm'; prev = null; continue; }
> 167	    let below = 0, cnt = 0;
> 168	    for (let j = i - win + 1; j <= i; j++) { if (Number.isFinite(sma200[j])) { cnt++; if (close[j] < sma200[j]) below++; } }
> 169	    const bf = cnt ? below / cnt : 0;
> 170	    const a = Number.isFinite(adx[i]) ? adx[i] : 0;
> 171	    const bearTh = prev === 'bear' ? 0.45 : 0.60;
> 172	    const trendTh = prev === 'trend' ? 22 : 25;
> 173	    const rangeTh = prev === 'range' ? 23 : 20;
> 174	    let r;
> 175	    if (bf > bearTh) r = 'bear';
> 176	    else if (a >= trendTh) r = 'trend';
> 177	    else if (a < rangeTh) r = 'range';
> 178	    else r = 'mixed';
> 179	    reg[i] = r; prev = r;
> 180	  }
> 181	  return reg;
> 182	}
> 183	
> 184	// ---------- engine: grid no-loss + funil pra BTC (exec no open de i+1, net de fee) ----------
> 185	function gridFunnel(candles, ind, btcCloseByT, gp) {
> 186	  let cash = gp.capital;
> 187	  const lots = [];                 // {qty, spent, price}
> 188	  let btcAccrued = 0, realizedUSDT = 0, nBuys = 0, nSells = 0;
> 189	  let peakEq = gp.capital, maxDD = 0, deployedPeak = 0, exposedBars = 0, totBars = 0;
> 190	  let lastSell = null, bearBars = 0;
> 191	
> 192	  for (let i = WARM; i < candles.length - 1; i++) {
> 193	    const px = candles[i + 1].open;            // execução sem lookahead
> 194	    const closeNext = candles[i + 1].close;
> 195	    const reg = ind.regime[i];
> 196	    const rsi = ind.rsi[i];
> 197	    const btcPx = btcCloseByT.get(candles[i + 1].t) || btcCloseByT.get(candles[i].t) || null;
> 198	    if (reg === 'bear') bearBars++;
> 199	    totBars++;
> 200	
> 201	    // 1) VENDAS no-loss: realiza cada lote que atingiu o lucro líquido alvo (nunca vende no prejuízo)
> 202	    for (let k = lots.length - 1; k >= 0; k--) {
> 203	      const lot = lots[k];
> 204	      const sellVal = lot.qty * px * (1 - FEE);
> 205	      if (sellVal >= lot.spent * (1 + gp.minProfit)) {
> 206	        cash += lot.spent;                       // principal volta pro caixa de trabalho
> 207	        const profit = sellVal - lot.spent;      // lucro líquido
> 208	        realizedUSDT += profit;
> 209	        if (btcPx) btcAccrued += profit / btcPx; // FUNIL: só o lucro vira BTC
> 210	        lots.splice(k, 1); nSells++; lastSell = px;
> 211	      }
> 212	    }
> 213	
> 214	    // 2) COMPRA grid: dip espaçado, gateado por regime !=bear, com teto de inventário
> 215	    const minLotPrice = lots.length ? Math.min(...lots.map(l => l.price)) : Infinity;
> 216	    const spaced = lots.length === 0 ? true : px <= minLotPrice * (1 - gp.gridStep);
> 217	    const belowLastSell = lastSell === null ? true : px <= lastSell * (1 - gp.gridStep);
> 218	    // filtro macro: não comprar dip quando a tendência de longo prazo está caindo (SMA macro hoje < passado)
> 219	    const macroOk = !gp.macroSma || (Number.isFinite(ind.smaMacro[i]) && Number.isFinite(ind.smaMacro[i - gp.macroSlope]) && ind.smaMacro[i] >= ind.smaMacro[i - gp.macroSlope]);
> 220	    if (reg !== 'bear' && reg !== 'warm' && macroOk && lots.length < gp.maxLots && cash >= gp.lotUSDT
> 221	      && Number.isFinite(rsi) && rsi < gp.rsiBuy && spaced && belowLastSell) {
> 222	      const qty = gp.lotUSDT * (1 - FEE) / px;   // fee na compra
> 223	      lots.push({ qty, spent: gp.lotUSDT, price: px });
> 224	      cash -= gp.lotUSDT; nBuys++;
> 225	    }
> 226	
> 227	    // 3) mark-to-market do equity total (caixa + inventário + BTC acumulado)
> 228	    const invMtM = lots.reduce((s, l) => s + l.qty * closeNext, 0);
> 229	    const eq = cash + invMtM + btcAccrued * (btcPx || 0);
> 230	    if (eq > peakEq) peakEq = eq;
> 231	    const dd = eq / peakEq - 1; if (dd < maxDD) maxDD = dd;
> 232	    const deployed = gp.capital - cash; if (deployed > deployedPeak) deployedPeak = deployed;
> 233	    if (lots.length > 0) exposedBars++;
> 234	  }
> 235	
> 236	  // fim: inventário preso marcado a mercado no último close
> 237	  const lastClose = candles[candles.length - 1].close;
> 238	  const lastBtc = btcCloseByT.get(candles[candles.length - 1].t) || null;
> 239	  const invFinal = lots.reduce((s, l) => s + l.qty * lastClose, 0);
> 240	  const invCost = lots.reduce((s, l) => s + l.spent, 0);
> 241	  const eqFinal = cash + invFinal + btcAccrued * (lastBtc || 0);
> 242	  return {
> 243	    btcAccrued, realizedUSDT, nBuys, nSells, lotsOpen: lots.length,
> 244	    invFinal, invCost, unrealized: invFinal - invCost,
> 245	    cash, eqFinal, capital: gp.capital, totalReturn: eqFinal / gp.capital - 1,
> 246	    maxDD, deployedPeak, exposure: exposedBars / (totBars || 1), bearFrac: bearBars / (totBars || 1),
> 247	  };
> 248	}
> 249	
> 250	// cruzamento SMA 50/200 (sinal do trend-following id6/id7): golden = cruza p/ cima, death = p/ baixo
> 251	function smaCross(sma50, sma200, i) {
> 252	  const f = sma50[i], s = sma200[i], fp = sma50[i - 1], sp = sma200[i - 1];
> 253	  if (![f, s, fp, sp].every(Number.isFinite)) return null;
> 254	  if (fp <= sp && f > s) return 'golden';
> 255	  if (fp >= sp && f < s) return 'death';
> 256	  return null;
> 257	}
> 258	
> 259	// ---------- engine COMPLETO: farm (grid no-loss) + trend (SMA50/200) coordenados + funil ----------
> 260	// Coordenação fiel ao runtime: trend entra no golden cross (se !=bear) e sai no death cross (corta no
> 261	// prejuízo — NÃO é no-loss); farm pausa quando há posição de trend ou regime trend/bear. Ambos → funil.
> 262	function gridTrendFunnel(candles, ind, btcCloseByT, gp) {
> 263	  let cash = gp.capital;
> 264	  const lots = [];
> 265	  let trendPos = null;             // {qty, spent}
> 266	  let btcAccrued = 0, farmRealized = 0, trendRealized = 0;
> 267	  let nFarmBuys = 0, nFarmSells = 0, nTrendTrades = 0, trendWins = 0;
> 268	  let peakEq = gp.capital, maxDD = 0, exposedBars = 0, totBars = 0;
> 269	  let lastSell = null, bearBars = 0;
> 270	
> 271	  for (let i = WARM; i < candles.length - 1; i++) {
> 272	    const px = candles[i + 1].open, closeNext = candles[i + 1].close;
> 273	    const reg = ind.regime[i], rsi = ind.rsi[i];
> 274	    const btcPx = btcCloseByT.get(candles[i + 1].t) || btcCloseByT.get(candles[i].t) || null;
> 275	    if (reg === 'bear') bearBars++; totBars++;
> 276	    const cross = smaCross(ind.sma50, ind.sma200, i);
> 277	    // filtro macro (tendência de fundo não-caindo) — usado pelo farm e, no switch de regime, pela entrada do trend
> 278	    const macroOk = !gp.macroSma || (Number.isFinite(ind.smaMacro[i]) && Number.isFinite(ind.smaMacro[i - gp.macroSlope]) && ind.smaMacro[i] >= ind.smaMacro[i - gp.macroSlope]);
> 279	
> 280	    // TREND: sai no death cross (realiza lucro OU prejuízo — corta a tendência)
> 281	    if (trendPos && cross === 'death') {
> 282	      const val = trendPos.qty * px * (1 - FEE); cash += val;
> 283	      const pnl = val - trendPos.spent; trendRealized += pnl;
> 284	      if (pnl > 0) { if (btcPx) btcAccrued += pnl / btcPx; trendWins++; }   // funil só escoa lucro
> 285	      trendPos = null; nTrendTrades++;
> 286	    }
> 287	    // TREND: entra no golden cross se fora do bear E (opcional) com força de tendência confirmada (ADX)
> 288	    const adxOk = !gp.trendAdx || (Number.isFinite(ind.adx[i]) && ind.adx[i] >= gp.trendAdx);
> 289	    if (!trendPos && cross === 'golden' && reg !== 'bear' && reg !== 'warm' && adxOk && (!gp.trendSwitch || macroOk)) {
> 290	      const spend = Math.min(gp.trendLot, cash);
> 291	      if (spend >= gp.lotUSDT) { trendPos = { qty: spend * (1 - FEE) / px, spent: spend }; cash -= spend; }
> 292	    }
> 293	
> 294	    // FARM: vendas no-loss
> 295	    for (let k = lots.length - 1; k >= 0; k--) {
> 296	      const lot = lots[k]; const sv = lot.qty * px * (1 - FEE);
> 297	      if (sv >= lot.spent * (1 + gp.minProfit)) {
> 298	        cash += lot.spent; const p = sv - lot.spent; farmRealized += p;
> 299	        if (btcPx) btcAccrued += p / btcPx; lots.splice(k, 1); nFarmSells++; lastSell = px;
> 300	      }
> 301	    }
> 302	    // FARM: compra dip — pausa em bear/trend e quando há posição de trend; + filtro macro + espaçamento
> 303	    const minLotPrice = lots.length ? Math.min(...lots.map(l => l.price)) : Infinity;
> 304	    const spaced = lots.length === 0 ? true : px <= minLotPrice * (1 - gp.gridStep);
> 305	    const belowLastSell = lastSell === null ? true : px <= lastSell * (1 - gp.gridStep);
> 306	    if (reg !== 'bear' && reg !== 'trend' && reg !== 'warm' && macroOk && !trendPos
> 307	      && lots.length < gp.maxLots && cash >= gp.lotUSDT && Number.isFinite(rsi) && rsi < gp.rsiBuy && spaced && belowLastSell) {
> 308	      lots.push({ qty: gp.lotUSDT * (1 - FEE) / px, spent: gp.lotUSDT, price: px }); cash -= gp.lotUSDT; nFarmBuys++;
> 309	    }
> 310	
> 311	    const invMtM = lots.reduce((s, l) => s + l.qty * closeNext, 0) + (trendPos ? trendPos.qty * closeNext : 0);
> 312	    const eq = cash + invMtM + btcAccrued * (btcPx || 0);
> 313	    if (eq > peakEq) peakEq = eq; const dd = eq / peakEq - 1; if (dd < maxDD) maxDD = dd;
> 314	    if (lots.length > 0 || trendPos) exposedBars++;
> 315	  }
> 316	
> 317	  const lastClose = candles[candles.length - 1].close;
> 318	  const lastBtc = btcCloseByT.get(candles[candles.length - 1].t) || null;
> 319	  const invFarm = lots.reduce((s, l) => s + l.qty * lastClose, 0), costFarm = lots.reduce((s, l) => s + l.spent, 0);
> 320	  const invTrend = trendPos ? trendPos.qty * lastClose : 0, costTrend = trendPos ? trendPos.spent : 0;
> 321	  const invFinal = invFarm + invTrend, invCost = costFarm + costTrend;
> 322	  const eqFinal = cash + invFinal + btcAccrued * (lastBtc || 0);
> 323	  return {
> 324	    btcAccrued, realizedUSDT: farmRealized + trendRealized, farmRealized, trendRealized,
> 325	    nBuys: nFarmBuys, nSells: nFarmSells, nTrendTrades, trendWins, lotsOpen: lots.length, trendOpen: trendPos ? 1 : 0,
> 326	    invFinal, invCost, unrealized: invFinal - invCost, cash, eqFinal, capital: gp.capital,
> 327	    totalReturn: eqFinal / gp.capital - 1, maxDD, exposure: exposedBars / (totBars || 1), bearFrac: bearBars / (totBars || 1),
> 328	  };
> 329	}
> 330	
> 331	function indicatorsFor(candles) {
> 332	  const close = candles.map(c => c.close), high = candles.map(c => c.high), low = candles.map(c => c.low);
> 333	  const sma200 = smaSeries(close, SC(200));
> 334	  const adx = dmiSeries(high, low, close, 14);
> 335	  const out = { close, rsi: rsiSeries(close, 14), sma200, sma50: smaSeries(close, SC(50)), adx, regime: regimeSeries(close, sma200, adx, SC(101)) };
> 336	  if (GP.macroSma) out.smaMacro = smaSeries(close, GP.macroSma);
> 337	  return out;
> 338	}
> 339	
> 340	// ---------- main ----------
> 341	(async () => {
> 342	  fs.mkdirSync(OUT_DIR, { recursive: true });
> 343	  const lines = [];
> 344	  lines.push(`# TradeUX — Backtest "Farm-and-Funnel" (grid no-loss multi-alt → funil pra BTC)\n`);
> 345	  lines.push(`> ${ALTS.length} alts · ${INTERVAL} · fee ${FEE * 100}%/lado · exec no open seguinte (sem lookahead).`);
> 346	  lines.push(`> Grid: capital ${GP.capital} USDT/alt, lote ${GP.lotUSDT}, máx ${GP.maxLots} lotes, passo ${pct(GP.gridStep)}, lucro-alvo ${pct(GP.minProfit)}, compra RSI<${GP.rsiBuy}, gate regime !=bear${GP.macroSma ? ` + filtro macro SMA${GP.macroSma} não-caindo (slope ${GP.macroSlope})` : ''}.`);
> 347	  if (GP.full) lines.push(`> Trend: SMA 50/200 (id6/id7) — entra no golden cross (se !=bear), sai no death cross (corta no prejuízo). Farm pausa durante trend. Posição ${GP.trendLot} USDT.`);
> 348	  lines.push(`> Funil: o lucro LÍQUIDO de cada venda (farm e trend) vira BTC ao preço do BTC no momento. O principal volta pro caixa de trabalho.\n`);
> 349	  console.log(`Farm-and-Funnel — ${ALTS.length} alts, ${INTERVAL}, params:`, GP);
> 350	
> 351	  const all = {};
> 352	  const PERIODS_RUN = args.only ? PERIODS.filter(p => p.label.includes(args.only)) : PERIODS;
> 353	  for (const P of PERIODS_RUN) {
> 354	    console.log(`\n=== período: ${P.label} (${P.days}d${P.end ? ' end ' + P.end : ''}) ===`);
> 355	    let btc;
> 356	    try { btc = await fetchAllKlines(BTC, P.days, P.end); }
> 357	    catch (e) { console.log(`  ERRO BTC: ${e.message}`); lines.push(`\n## ${P.label}\n\n_falha BTC: ${e.message}_`); continue; }
> 358	    const btcByT = new Map(btc.map(c => [c.t, c.close]));
> 359	
> 360	    const rows = [];
> 361	    for (const sym of ALTS) {
> 362	      let cd;
> 363	      try { cd = await fetchAllKlines(sym, P.days, P.end); }
> 364	      catch (e) { console.log(`  skip ${sym}: ${e.message}`); continue; }
> 365	      if (!cd || cd.length < WARM + 50) { console.log(`  skip ${sym}: dados insuficientes (${cd ? cd.length : 0})`); continue; }
> 366	      const ind = indicatorsFor(cd);
> 367	      const r = (GP.full ? gridTrendFunnel : gridFunnel)(cd, ind, btcByT, GP);
> 368	      r.sym = sym; r.candles = cd.length;
> 369	      rows.push(r);
> 370	      const trendStr = GP.full ? ` | trend ${r.nTrendTrades}t (${r.trendWins}W, $${fmt(r.trendRealized)})` : '';
> 371	      console.log(`  ${sym.padEnd(9)} BTC+${fmt(r.btcAccrued, 5)} | lucro $${fmt(r.realizedUSDT)} | buys ${r.nBuys} sells ${r.nSells}${trendStr} | preso $${fmt(r.invFinal)} (n/r $${fmt(r.unrealized)}) | eqRet ${pct(r.totalReturn)} | DD ${pct(r.maxDD)} | exp ${pct(r.exposure)} | bear ${pct(r.bearFrac)}`);
> 372	    }
> 373	    if (!rows.length) { lines.push(`\n## ${P.label}\n\n_sem dados_`); continue; }
> 374	
> 375	    // agregado do período
> 376	    const sum = k => rows.reduce((s, r) => s + r[k], 0);
> 377	    const years = P.days / 365;
> 378	    const btcTot = sum('btcAccrued'), capTot = sum('capital'), realTot = sum('realizedUSDT');
> 379	    const investedReturn = sum('eqFinal') / capTot - 1;
> 380	    const agg = {
> 381	      period: P.label, alts: rows.length, capital: capTot, btcAccrued: btcTot, btcPerYear: btcTot / years,
> 382	      realizedUSDT: realTot, investedReturn, avgMaxDD: mean(rows.map(r => r.maxDD)),
> 383	      invStuck: sum('invFinal'), unrealized: sum('unrealized'), avgExposure: mean(rows.map(r => r.exposure)),
> 384	      bearFrac: mean(rows.map(r => r.bearFrac)),
> 385	    };
> 386	    all[P.label] = { agg, rows };
> 387	
> 388	    lines.push(`\n## ${P.label} — ${rows.length} alts, capital total ${capTot} USDT\n`);
> 389	    const tcol = GP.full ? ' Trend (trades, PnL) |' : '';
> 390	    const tsep = GP.full ? '---|' : '';
> 391	    lines.push(`| Alt | BTC acumulado | Lucro realiz. (USDT) |${tcol} Buys/Sells | Inventário preso (PnL n/realiz.) | Retorno equity | MaxDD | Exposição | % bear |`);
> 392	    lines.push(`|---|---|---|${tsep}---|---|---|---|---|---|`);
> 393	    for (const r of rows) {
> 394	      const tcell = GP.full ? ` ${r.nTrendTrades}t/${r.trendWins}W ($${fmt(r.trendRealized)}) |` : '';
> 395	      lines.push(`| ${r.sym} | +${fmt(r.btcAccrued, 5)} | ${fmt(r.realizedUSDT)} |${tcell} ${r.nBuys}/${r.nSells} | $${fmt(r.invFinal)} ($${fmt(r.unrealized)}) | ${pct(r.totalReturn)} | ${pct(r.maxDD)} | ${pct(r.exposure)} | ${pct(r.bearFrac)} |`);
> 396	    }
> 397	    lines.push(`\n**Agregado ${P.label}:** BTC acumulado **+${fmt(btcTot, 5)}** (≈ **+${fmt(agg.btcPerYear, 5)} BTC/ano**) · lucro realizado **$${fmt(realTot)}** sobre **$${capTot}** de capital · retorno do equity total **${pct(investedReturn)}** · inventário preso no fim **$${fmt(agg.invStuck)}** (PnL não-realizado **$${fmt(agg.unrealized)}**) · maxDD médio **${pct(agg.avgMaxDD)}** · exposição média **${pct(agg.avgExposure)}** · janela classificada bear **${pct(agg.bearFrac)}** do tempo.\n`);
> 398	  }
> 399	
> 400	  // ---------- síntese / extrapolação rumo a +3 BTC ----------
> 401	  lines.push(`\n## 🎯 Síntese — taxa de acúmulo e o que falta pra +3 BTC\n`);
> 402	  lines.push(`| Período | BTC/ano (por ${GP.capital * ALTS.length} USDT) | Lucro realiz. | Retorno equity | Inventário preso | % bear |`);
> 403	  lines.push(`|---|---|---|---|---|---|`);
> 404	  for (const k of Object.keys(all)) {
> 405	    const a = all[k].agg;
> 406	    lines.push(`| ${a.period} | +${fmt(a.btcPerYear, 5)} | $${fmt(a.realizedUSDT)} | ${pct(a.investedReturn)} | $${fmt(a.invStuck)} | ${pct(a.bearFrac)} |`);
> 407	  }
> 408	  lines.push(`\n**Leitura honesta:**`);
> 409	  lines.push(`- **BTC/ano** é a taxa do funil normalizada pelo capital de trabalho (${ALTS.length}×${GP.capital} = ${GP.capital * ALTS.length} USDT). Pra +3 BTC, escale capital × tempo: dobrar o capital ~dobra a taxa (até o teto de liquidez/lotes).`);
> 410	  lines.push(`- O **inventário preso** é o calcanhar do no-loss: capital que ficou comprado sem fechar no lucro (pior no bear). Se grande, o "lucro realizado" foi em parte financiado por capital imobilizado — por isso o **retorno do equity total** (que inclui esse inventário marcado a mercado) é o juiz, não o lucro realizado isolado.`);
> 411	  lines.push(`- **% bear** mostra quanto do tempo o gate de regime manteve o grid em caixa (sem comprar). Em janelas muito bear, o farm quase não roda — é esperado e é a proteção funcionando.`);
> 412	  lines.push(`\n---\n_Gerado por backend/scripts/backtest-farm-funnel.js. Dados: Binance klines reais (mainnet, cache em backtest-data/). Net de fee. Não é conselho financeiro; validação de estratégia._`);
> 413	
> 414	  const tag = `${GP.full ? '-full' : ''}${GP.macroSma ? '-macro' + GP.macroSma : ''}${GP.trendAdx ? '-adx' + GP.trendAdx : ''}${GP.trendSwitch ? '-switch' : ''}`;
> 415	  const outFile = path.join(OUT_DIR, `farm-funnel-${INTERVAL}${tag}.md`);
> 416	  fs.writeFileSync(outFile, lines.join('\n'));
> 417	  fs.writeFileSync(path.join(OUT_DIR, `farm-funnel-${INTERVAL}${tag}.json`), JSON.stringify(all, null, 2));
> 418	  console.log(`\nRelatório: ${outFile}`);
> 419	})();
> 420	
> ```

## 🤖 Claude *(15:04:07)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrux-tradeux/memory/tradeux-farm-funnel-backtest.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>This memory is 11 days old. Memories are point-in-time observations, not live state — claims about code behavior or file:line citations may be outdated. Verify against current code before asserting as fact.</system-reminder>
> 1	---
> 2	name: tradeux-farm-funnel-backtest
> 3	description: backtest da estratégia do dono (grid no-loss multi-alt + funil pra BTC + trend) — farm = baixo risco/alpha marginal; trend = motor de bull; +3 BTC só capturando ciclos
> 4	metadata: 
> 5	  node_type: memory
> 6	  type: project
> 7	  originSessionId: 410f5676-07a2-443f-b17c-ed9ac8804900
> 8	---
> 9	
> 10	Estratégia "Farm-and-Funnel" (ideia do dono: grid no-loss nas alts → escoar lucro realizado pra BTC).
> 11	Backtestada com candles mainnet reais em 3 regimes (recente/bull-2023-24/bear-2022), 8 alts, 1h, net de fee.
> 12	Harness novo: `backend/scripts/backtest-farm-funnel.js` (engine de LOTES + funil; o backtest.js é all-in/all-out e não serve). Relatórios em `backend/backtest-results/farm-funnel-*.md`.
> 13	
> 14	**Resultados (equity TOTAL agregado — o juiz; "BTC acumulado" sozinho ENGANA: no-loss esconde prejuízo em inventário preso):**
> 15	- **Farm-só + filtro macro**: recente −3.5% · bull +0.9% · bear −1.7%. Baixo risco, mas alpha marginal. +3 BTC = **séculos** (~0.0015 BTC/ano por $8k). No bull o grid fica de FORA do upside.
> 16	- **Farm + Trend (SMA50/200) + funil**: bull **+22.6%** (ETH+52/SOL+50/AVAX+49/LINK+41), BTC/ano **16×** o farm. MAS choppy/recente **−10.5%** (whipsaw do trend-following). bear −2.2%.
> 17	- Confirmar força no golden cross com ADX: ADX≥22 mata o bull (+3.8%); **ADX≥15 = sweet spot** (bull +22.3%, choppy −9.3%). Whipsaw em lateral é INERENTE ao trend, não some.
> 18	
> 19	**Conclusões:** (1) o trend é o motor que torna +3 BTC plausível — mas só **capturando bulls de ciclo**; (2) custo = sangra em lateral; (3) o lever certo é o **regime macro LIGAR/DESLIGAR o trend** (trend on em bull, farm-só em lateral), não um filtro de ADX fino. +3 BTC = horizonte de CICLOS (anos), aposta em capturar altas com gestão de risco nos laterais — não garantido, não rápido.
> 20	
> 21	**Implementado (commit 416d6e9, push master, 2026-06-08):** harness `backtest-farm-funnel.js`; doc `docs/STRATEGY-farm-funnel.md` (estratégia + plano faseado §5); **funnelJob SHADOW AO VIVO** (observa caixa USDT + reserva BTC, loga o que escoaria, NÃO compra — padrão flowJob; rebuild+restart feito, boot limpo); id3 pausada via API.
> 22	**Fase 2a feita (commit 985272f):** `backend/scripts/setup-farm.js` criou o farm no-loss das alts LTC/BNB/ADA — monitor CANDLES (RSI) + templates LIMIT marketável + automações Farm Buy (id 9/11/13) e Farm Sell no-loss (id 10/12/14), TODAS INATIVAS. Venda dispara pelo PREÇO (`bestBid>avgPrice×1.012`), não RSI = regra do dono. Anti-empilhamento (invertCondition exige `.current` na cláusula do index + isLocked + isChecked) e fail-safe (REGIME/LAST_ORDER no index) validados. Conditions devem ser regex-safe (validateConditions: `MEMORY[...]OP valor`, sem espaços/||/guards soltos). v1 = 1 lote (sem trava de posição → DCA leve possível; multi-lote/FARM_QTY = refino).
> 23	**Fase 2b FEITA (farm das alts ATIVO):** as 6 automações (id 9-14, LTC/BNB/ADA) ATIVAS. Wiring validado ao vivo: regimeJob pega a alt sozinho → LTCUSDT:REGIME=bear → gate `!=bear` bloqueia → 0 ordens (proteção em bear). Mercado bear → farm inerte/armado; opera em range. Reversível (`stop` id 9-14). Sem erros, site 200.
> 24	**Fase 3 FEITA (trend das alts ATIVO):** trend SMA50/200 de LTC/BNB/ADA (id 15-20) criado via `setup-trend.js` (3× por TREND_SYMBOL) e ATIVO. ZERO código novo: regimeJob já computa `<alt>:TREND_CROSS_1h` + updateTrendPosition mantém `<alt>:TREND_QTY` (ambos por-símbolo). Coordenação: trend `!=bear`, farm `!=trend`. 15 automações ativas = arquitetura completa do backtest ao vivo. Inerte em bear.
> 25	**Lacunas (Fases 4-5):** Fase 4 = ligar o funil ao vivo (money-path; só rende em mercado não-bear); Fase 5 = calibrar 5m/seleção (SOL ruim) + switch macro FINO (SMA-slope no regimeJob — hoje o "switch" é só a coordenação por REGIME, não o slope do backtest). Ver [[tradeux-agent-500k-validation]] (meta +3 BTC), [[tradeux-regime-gate]] (o switch), [[tradeux-trend-following]] (id6/id7), [[tradeux-flow-oracle]].
> 26	
> 27	**🔔 ARMADOR DA FASE 4 (commit `af22e7a`, 2026-06-09, deployado+smoke-testado):** o farm/trend JÁ retomam sozinhos na saída do bear (gate `REGIME!=bear` é runtime, zero código). O que faltava era NÃO ficar de plantão + capturar o dado pra escrever a Fase 4. Construído: `regimeJob` detecta a borda `bear→não-bear` do macro (`FASE4_MACRO_SYMBOL`, default BTCUSDT) → chama `funnelJob.armFase4Observation()` (hook fire-and-forget + promise-anchored, NUNCA derruba o loop de regime). O armador: (1) NOTIFICA (log+telegram best-effort); (2) pré-arma o funil shadow (snapshot do USDT vira `RUNTIME_BASELINE` → passa a computar o escoamento); (3) abre janela densa de 4h (`FASE4_WINDOW_MS`, captura a cada `FASE4_OBSERVE_MS`=5min, tag `[fase4-observe]` em logs/funnel.log) gravando caixa USDT, reserva BTC, preço, lucro-desde-saída e quanto escoaria; sumário+notify no fim. **SHADOW puro — NÃO compra.** Decisão do dono: opção 1 (notify) + opção 2 (pré-armar shadow) + deixar tudo armado p/ as 1ªs 4h de dados pós-bear bastarem pra ESCREVER a Fase 4. **A Fase 4 (compra de BTC ao vivo) AINDA não existe** — o código de live-buy não foi escrito; depende do dado real (farm só farma pós-bear) + gate QA/TL (o doc §5 manda). Envs `FASE4_*` documentados nos headers de funnelJob/regimeJob. Janela in-memory (snapshots em disco sobrevivem a restart; modo-denso volátil) — v2 = persistir.
> 28	
> ```

## 🤖 Claude *(15:04:11)*

Vou ler as fontes restantes para fundamentar a análise cross-símbolo com números reais.

## 🤖 Claude *(15:04:12)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/docs/STRATEGY-farm-funnel.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Estratégia TradeUX — "Farm-and-Funnel" (rumo a +3 BTC)
> 2	
> 3	> Documento de estratégia validado por backtest com dados reais de mainnet (jun/2026).
> 4	> Substitui o antigo `STRATEGY-3BTC-assessment.md`. Fonte dos números: `backend/scripts/backtest-farm-funnel.js`
> 5	> + relatórios em `backend/backtest-results/farm-funnel-*.md`. Memória: `tradeux-farm-funnel-backtest`.
> 6	
> 7	## 1. Sumário executivo
> 8	
> 9	A meta é denominada **em BTC** (+3 BTC). A estratégia tem três camadas que escoam pra um cofre de BTC:
> 10	
> 11	1. **Farm** — grid "no-loss" (regra do dono: vende só acima do custo, compra só abaixo da última venda) nas
> 12	   **alts**, gateado por regime (`!=bear`) + filtro macro. Gera lucro realizado em USDT nos mercados laterais.
> 13	2. **Trend** — SMA 50/200 (id6/id7) captura os **bull markets** (onde o ganho de BTC realmente acontece).
> 14	3. **Funil** — o **lucro realizado** das duas camadas vira BTC ao preço do momento → reserva que só cresce.
> 15	
> 16	**Por que assim:** vender BTCUSDT no bear *reduz* BTC (o que o sistema fazia — ver §6). Farmar alts e converter
> 17	o lucro em BTC **desacopla "ganhar dinheiro" de "denominar em BTC"** — não exige acertar o timing do próprio BTC.
> 18	
> 19	**Veredito honesto da meta:** +3 BTC **não** é alcançável com o farm sozinho (taxa ~0,5–2%/ano → séculos). É
> 20	plausível **em horizonte de ciclos**, capturando bulls com o trend (no bull 2023-24 a arquitetura fez **+14–22%**
> 21	de equity e **16× o BTC/ano** do farm). Não é garantido nem rápido — é uma aposta em capturar as altas de ciclo
> 22	com gestão de risco nos laterais.
> 23	
> 24	## 2. Arquitetura
> 25	
> 26	```
> 27	        ALTS (BNB, ETH, XRP, ADA, LINK, LTC, AVAX, …)
> 28	   ┌─────────────┴─────────────┐
> 29	   │ FARM (grid no-loss)        │ TREND (SMA 50/200)
> 30	   │ • compra dip RSI<lo         │ • entra no golden cross
> 31	   │   E preço < última venda    │   (gateado por switch de regime:
> 32	   │ • vende só com lucro        │    só em bull macro)
> 33	   │ • gate: !=bear + macro      │ • sai no death cross (corta perda)
> 34	   │ • opera em RANGE            │ • opera em TREND
> 35	   └─────────────┬─────────────┘
> 36	                 │ lucro realizado (USDT)
> 37	                 ▼
> 38	            FUNIL (funnelJob) ──► compra BTC ──► COFRE BTC (não é operado; é a meta)
> 39	```
> 40	
> 41	Coordenação por regime (já existe ao vivo via `regimeJob` → `MEMORY['<sym>:REGIME']`):
> 42	**bear** → tudo em caixa · **range/mixed** → farm · **trend (bull macro)** → trend conduz, farm pausa.
> 43	
> 44	## 3. Resultados do backtest (equity total agregado — net de fee, sem lookahead)
> 45	
> 46	Equity é o **juiz**: o "BTC acumulado" sozinho engana (o no-loss esconde prejuízo em inventário preso).
> 47	
> 48	**1h, 8 alts, 3 regimes:**
> 49	
> 50	| Configuração | Recente (lateral) | Bull 2023-24 | Bear 2022 |
> 51	|---|---|---|---|
> 52	| Farm-só (+ filtro macro) | −3,5% | +0,9% | −1,7% |
> 53	| Farm + Trend (gate `!=bear`) | −10,5% | **+22,6%** | −2,2% |
> 54	| Farm + Trend (switch de regime) | −6,2% | **+13,5%** | −0,9% |
> 55	
> 56	**Config final recomendada (Farm + Trend + Switch, 15m):** recente **−5,5%** · bull **+14,4%** · bear **−0,4%**.
> 57	O 15m bate o 1h em todos os regimes (granularidade menor = mais farm, menos inventário preso).
> 58	
> 59	**Leituras:** (a) o trend é o motor de +3 BTC (sem ele, impossível); (b) o custo do trend é whipsaw em lateral —
> 60	inerente, não some; (c) o switch de regime é o melhor compromisso pra rodar sem supervisão; (d) timeframe curto
> 61	(15m, talvez 5m) é melhor pro farm.
> 62	
> 63	## 4. Decisões de design
> 64	
> 65	- **No-loss** (regra do dono): vender só quando `preço × (1−fee) ≥ custo × (1+lucro_alvo)`. Reusa o **grid nativo
> 66	  do Beholder** (`gridEval`/`generateGrids`) + `MEMORY['<sym>:LAST_ORDER']` pro custo. Lucro-alvo ~0,6% (> round-trip de fee).
> 67	- **Funil**: o lucro realizado vira BTC; o principal volta pro caixa de trabalho. v1 = skimming por saldo (shadow);
> 68	  v2 = rastreio de lucro por trade. Job novo `funnelJob` no padrão `regimeJob`/`flowJob`.
> 69	- **Seleção de alts**: estáveis (LTC/BNB/ADA/ETH) são melhores pro **farm**; voláteis (SOL/AVAX/LINK) afundam o
> 70	  farm mas o **trend** as resgata no bull. SOL é o pior pro farm. Universo diversificado, cada uma na camada certa.
> 71	- **Timeframe**: farm em 15m (ou 5m); regime/trend macro em 1h (como hoje). Períodos de SMA escalam com o timeframe.
> 72	- **Switch de regime**: o trend só entra quando a tendência de fundo (SMA ~21d) está subindo (filtro macro também na entrada do trend).
> 73	- **BTC não é farmado** (é o cofre): a id3 (SELL BTCUSDT) foi **pausada** (vendia BTC sem gate de lucro — a sangria
> 74	  que motivou este estudo). A id2 (BUY BTCUSDT no dip) pode permanecer como DCA direto em BTC.
> 75	
> 76	## 5. Plano de implementação (faseado — cada fase com gate QA+TL antes de ativar; money-path)
> 77	
> 78	- **Fase 0 (feita):** pausar id3; validar a arquitetura por backtest; este doc.
> 79	- **Fase 1 — Funil em SHADOW:** `funnelJob` calcula e loga o que escoaria pra BTC (sem comprar). Zero money-path.
> 80	- **Fase 2 — Farm das alts (inativo→ativo):** `setup-farm.js` cria símbolos + templates + automações no-loss
> 81	  (grid nativo) das alts selecionadas, INATIVAS; ativa com gate, capital pequeno, 1 alt por vez.
> 82	- **Fase 3 — Trend nas alts + switch:** estender id6/id7 (ou análogas) pras alts com o switch de regime macro.
> 83	- **Fase 4 — Funil ao vivo:** ligar a compra de BTC com o lucro realizado (depois de observar o shadow).
> 84	- **Fase 5 — Calibração:** timeframe 5m, seleção de alts, params, por evidência acumulada.
> 85	
> 86	Tudo runtime/idempotente (reaplicar pós-`make nuke`), seguindo `setup-trend.js`/`activate-trend.js`.
> 87	
> 88	## 6. Riscos e honestidade
> 89	
> 90	- **Whipsaw do trend em lateral** (−5 a −10%/ano): inerente; mitigado pelo switch de regime, não eliminado.
> 91	- **Inventário preso (no-loss)**: o "lucro" pode ser financiado por capital imobilizado num bear → o equity total
> 92	  é o juiz, não o lucro realizado isolado.
> 93	- **Testnet sintético**: o preço de execução do testnet **não** valida P&L. A validação de lucro é por **backtest
> 94	  mainnet** (este doc) e, no futuro, operação real. O testnet valida só o *wiring* da lógica.
> 95	- **A meta**: +3 BTC ≈ 3× o patrimônio atual (~$108k). Horizonte de ciclos (anos), dependente de capturar bulls.
> 96	  Calibrar a ambição vs. risco com o dono à medida que os dados reais chegam.
> 97	
> 98	## 7. Reproduzir o backtest
> 99	
> 100	```bash
> 101	cd backend
> 102	node scripts/backtest-farm-funnel.js                                   # farm-só, 1h, 8 alts, 3 regimes
> 103	node scripts/backtest-farm-funnel.js --macrosma=500 --macroslope=240   # + filtro macro
> 104	node scripts/backtest-farm-funnel.js --full --macrosma=500 --switch    # arquitetura completa + switch
> 105	node scripts/backtest-farm-funnel.js --full --switch --interval=15m --tfscale=4 --macrosma=2000 --macroslope=960  # config final
> 106	```
> 107	Relatórios em `backend/backtest-results/farm-funnel-*.md`; cache de klines em `backtest-data/` (gitignored).
> 108	
> ```

## 🤖 Claude *(15:04:13)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la /home/gcrux-tradeux/tradeux/backend/backtest-results/ 2>/dev/null; echo \"---DATA---\"; ls -la /home/gcrux-tradeux/tradeux/backend/backtest-data/ 2>/dev/null | head -60",
  "description": "List backtest results and cached data files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 260
> drwxrwxr-x  2 gcrux-tradeux gcrux-tradeux  4096 Jun 19 12:10 .
> drwxrwxr-x 11 gcrux-tradeux gcrux-tradeux  4096 Jun 19 23:24 ..
> -rw-r--r--  1 gcrux-tradeux gcrux-tradeux  9617 Jun  3 20:40 backtest-1h-180d-end2024-04-01.json
> -rw-r--r--  1 gcrux-tradeux gcrux-tradeux  6919 Jun  3 20:40 backtest-1h-180d-end2024-04-01.md
> -rw-r--r--  1 gcrux-tradeux gcrux-tradeux 10085 Jun  3 20:40 backtest-1h-365d.json
> -rw-r--r--  1 gcrux-tradeux gcrux-tradeux  6992 Jun  3 20:40 backtest-1h-365d.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  3858 Jun  8 23:26 backtest-futures-1h-bear-365d.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  3856 Jun  8 23:28 backtest-futures-1h-bull-end2024-04-01.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 18831 Jun  8 14:30 farm-funnel-15m-full-macro2000-switch.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  6411 Jun  8 14:30 farm-funnel-15m-full-macro2000-switch.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  5253 Jun  8 14:26 farm-funnel-15m-macro2000.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  2991 Jun  8 14:26 farm-funnel-15m-macro2000.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 18930 Jun  8 14:04 farm-funnel-1h-full-macro500-adx15.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  6439 Jun  8 14:04 farm-funnel-1h-full-macro500-adx15.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 18966 Jun  8 14:03 farm-funnel-1h-full-macro500-adx22.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  6416 Jun  8 14:03 farm-funnel-1h-full-macro500-adx22.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 18927 Jun  8 14:01 farm-funnel-1h-full-macro500.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  6444 Jun  8 14:01 farm-funnel-1h-full-macro500.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 18823 Jun  8 14:16 farm-funnel-1h-full-macro500-switch.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  6409 Jun  8 14:16 farm-funnel-1h-full-macro500-switch.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 15509 Jun  8 13:34 farm-funnel-1h.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 15371 Jun  8 13:38 farm-funnel-1h-macro500.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  5705 Jun  8 13:38 farm-funnel-1h-macro500.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  5698 Jun  8 13:34 farm-funnel-1h.md
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux  1916 Jun  3 13:38 README.md
> ---DATA---
> total 158608
> drwxr-xr-x  2 gcrux-tradeux gcrux-tradeux    4096 Jun 19 11:29 .
> drwxrwxr-x 11 gcrux-tradeux gcrux-tradeux    4096 Jun 19 23:24 ..
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 1635009 Jun  8 14:27 ADAUSDT-15m-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 3228064 Jun  8 14:29 ADAUSDT-15m-365d-end2023-01-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 3182473 Jun  8 14:25 ADAUSDT-15m-365d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  457088 Jun  8 13:33 ADAUSDT-1h-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  812447 Jun  8 13:34 ADAUSDT-1h-365d-end2023-01-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  801328 Jun  8 13:33 ADAUSDT-1h-365d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 1548487 Jun  8 14:28 AVAXUSDT-15m-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 3102058 Jun  8 14:30 AVAXUSDT-15m-365d-end2023-01-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 2982373 Jun  8 14:26 AVAXUSDT-15m-365d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  433172 Jun  8 13:33 AVAXUSDT-1h-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  780868 Jun  8 13:34 AVAXUSDT-1h-365d-end2023-01-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  750864 Jun  8 13:33 AVAXUSDT-1h-365d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 1553347 Jun  8 14:27 BNBUSDT-15m-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 3101451 Jun  8 14:28 BNBUSDT-15m-365d-end2023-01-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 3154851 Jun  8 14:24 BNBUSDT-15m-365d.json
> -rw-r--r--  1 gcrux-tradeux gcrux-tradeux  434612 Jun  3 13:36 BNBUSDT-1h-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  781406 Jun  8 13:33 BNBUSDT-1h-365d-end2023-01-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  793655 Jun  3 20:35 BNBUSDT-1h-365d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 7405730 Jun  3 21:34 BNBUSDT-1m-60d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 7642489 Jun  3 21:31 BNBUSDT-1m-60d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux   19236 Jun  8 23:28 BNBUSDT-FUNDING-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux   35172 Jun  8 23:26 BNBUSDT-FUNDING-365d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  390052 Jun  8 23:28 BNBUSDT-FUT-1h-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  792115 Jun  8 23:26 BNBUSDT-FUT-1h-365d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 1758985 Jun  8 14:27 BTCUSDT-15m-180d-end2024-04-01.json
> -rw-r--r--  1 gcrux-tradeux gcrux-tradeux 1686832 Jun 19 11:29 BTCUSDT-15m-180d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 3564030 Jun  8 14:28 BTCUSDT-15m-365d-end2023-01-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 3484584 Jun  8 14:24 BTCUSDT-15m-365d.json
> -rw-r--r--  1 gcrux-tradeux gcrux-tradeux  880675 Jun 19 11:29 BTCUSDT-15m-90d-end2026-03-15.json
> -rw-r--r--  1 gcrux-tradeux gcrux-tradeux  841313 Jun 19 11:29 BTCUSDT-15m-90d.json
> -rw-r--r--  1 gcrux-tradeux gcrux-tradeux  490529 Jun  3 13:36 BTCUSDT-1h-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  894323 Jun  8 13:33 BTCUSDT-1h-365d-end2023-01-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  875768 Jun  3 20:35 BTCUSDT-1h-365d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 8393979 Jun  3 21:33 BTCUSDT-1m-60d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 8347925 Jun  3 21:30 BTCUSDT-1m-60d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux   19453 Jun  8 23:28 BTCUSDT-FUNDING-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux   41174 Jun  8 23:26 BTCUSDT-FUNDING-365d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  403565 Jun  8 23:28 BTCUSDT-FUT-1h-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  832145 Jun  8 23:26 BTCUSDT-FUT-1h-365d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 1704935 Jun  8 14:27 ETHUSDT-15m-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 3421772 Jun  8 14:28 ETHUSDT-15m-365d-end2023-01-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 3324760 Jun  8 14:25 ETHUSDT-15m-365d.json
> -rw-r--r--  1 gcrux-tradeux gcrux-tradeux  475865 Jun  3 13:36 ETHUSDT-1h-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  860288 Jun  8 13:33 ETHUSDT-1h-365d-end2023-01-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  836280 Jun  3 20:35 ETHUSDT-1h-365d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 8134318 Jun  3 21:33 ETHUSDT-1m-60d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 8092304 Jun  3 21:31 ETHUSDT-1m-60d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux   19467 Jun  8 23:28 ETHUSDT-FUNDING-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux   41182 Jun  8 23:26 ETHUSDT-FUNDING-365d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  410635 Jun  8 23:28 ETHUSDT-FUT-1h-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  833382 Jun  8 23:26 ETHUSDT-FUT-1h-365d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 1621658 Jun  8 14:27 LINKUSDT-15m-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 3088716 Jun  8 14:29 LINKUSDT-15m-365d-end2023-01-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 2985646 Jun  8 14:25 LINKUSDT-15m-365d.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  453960 Jun  8 13:33 LINKUSDT-1h-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  778164 Jun  8 13:34 LINKUSDT-1h-365d-end2023-01-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  751774 Jun  8 13:33 LINKUSDT-1h-365d.json
> ```

## 🤖 Claude *(15:04:16)*

I have the per-symbol farm data cached. Let me read the farm-só report to extract per-symbol numbers, which is the core of the cross-symbol expansion question.

## 🤖 Claude *(15:04:17)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/backtest-results/farm-funnel-1h-macro500.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# TradeUX — Backtest "Farm-and-Funnel" (grid no-loss multi-alt → funil pra BTC)
> 2	
> 3	> 8 alts · 1h · fee 0.1%/lado · exec no open seguinte (sem lookahead).
> 4	> Grid: capital 1000 USDT/alt, lote 100, máx 8 lotes, passo 1.50%, lucro-alvo 0.60%, compra RSI<35, gate regime !=bear + filtro macro SMA500 não-caindo (slope 240).
> 5	> Funil: o lucro LÍQUIDO de cada venda vira BTC ao preço do BTC no momento. O principal volta pro caixa de trabalho.
> 6	
> 7	
> 8	## recente (~últ. 365d) — 8 alts, capital total 8000 USDT
> 9	
> 10	| Alt | BTC acumulado | Lucro realiz. (USDT) | Buys/Sells | Inventário preso (PnL n/realiz.) | Retorno equity | MaxDD | Exposição | % bear |
> 11	|---|---|---|---|---|---|---|---|---|
> 12	| BNBUSDT | +0.00004 | 3.32 | 4/4 | $0.00 ($0.00) | 0.25% | -0.13% | 0.29% | 44.20% |
> 13	| ETHUSDT | +0.00010 | 7.32 | 8/8 | $0.00 ($0.00) | 0.62% | -1.14% | 7.45% | 54.25% |
> 14	| SOLUSDT | +0.00013 | 10.60 | 14/11 | $160.29 ($-139.71) | -13.14% | -13.55% | 40.95% | 52.20% |
> 15	| XRPUSDT | +0.00017 | 17.06 | 20/19 | $53.14 ($-46.86) | -4.69% | -6.24% | 54.34% | 61.81% |
> 16	| ADAUSDT | +0.00009 | 8.88 | 9/9 | $0.00 ($0.00) | 0.00% | -1.11% | 2.15% | 62.67% |
> 17	| LINKUSDT | +0.00009 | 7.76 | 11/8 | $186.12 ($-113.88) | -11.39% | -13.87% | 42.24% | 54.43% |
> 18	| LTCUSDT | +0.00004 | 3.22 | 4/4 | $0.00 ($0.00) | 0.00% | -0.70% | 1.62% | 54.80% |
> 19	| AVAXUSDT | +0.00009 | 7.19 | 8/8 | $0.00 ($0.00) | 0.00% | -0.69% | 1.20% | 56.05% |
> 20	
> 21	**Agregado recente (~últ. 365d):** BTC acumulado **+0.00075** (≈ **+0.00075 BTC/ano**) · lucro realizado **$65.34** sobre **$8000** de capital · retorno do equity total **-3.54%** · inventário preso no fim **$399.56** (PnL não-realizado **$-300.44**) · maxDD médio **-4.68%** · exposição média **18.78%** · janela classificada bear **55.05%** do tempo.
> 22	
> 23	
> 24	## bull 2023-24 — 8 alts, capital total 8000 USDT
> 25	
> 26	| Alt | BTC acumulado | Lucro realiz. (USDT) | Buys/Sells | Inventário preso (PnL n/realiz.) | Retorno equity | MaxDD | Exposição | % bear |
> 27	|---|---|---|---|---|---|---|---|---|
> 28	| BNBUSDT | +0.00012 | 4.48 | 5/5 | $0.00 ($0.00) | 0.74% | -0.16% | 0.47% | 33.25% |
> 29	| ETHUSDT | +0.00005 | 1.70 | 1/1 | $0.00 ($0.00) | 0.30% | -0.06% | 0.05% | 32.24% |
> 30	| SOLUSDT | +0.00016 | 5.97 | 4/4 | $0.00 ($0.00) | 1.02% | -0.49% | 0.21% | 37.80% |
> 31	| XRPUSDT | +0.00025 | 9.92 | 10/10 | $0.00 ($0.00) | 1.56% | -0.36% | 4.21% | 51.33% |
> 32	| ADAUSDT | +0.00012 | 4.39 | 2/2 | $0.00 ($0.00) | 0.77% | -0.16% | 0.09% | 40.64% |
> 33	| LINKUSDT | +0.00029 | 10.62 | 10/10 | $0.00 ($0.00) | 1.82% | -0.99% | 1.58% | 42.10% |
> 34	| LTCUSDT | +0.00010 | 3.91 | 4/4 | $0.00 ($0.00) | 0.64% | -0.17% | 0.89% | 41.96% |
> 35	| AVAXUSDT | +0.00004 | 1.49 | 1/1 | $0.00 ($0.00) | 0.26% | -0.06% | 0.02% | 42.53% |
> 36	
> 37	**Agregado bull 2023-24:** BTC acumulado **+0.00114** (≈ **+0.00231 BTC/ano**) · lucro realizado **$42.49** sobre **$8000** de capital · retorno do equity total **0.89%** · inventário preso no fim **$0.00** (PnL não-realizado **$0.00**) · maxDD médio **-0.31%** · exposição média **0.94%** · janela classificada bear **40.23%** do tempo.
> 38	
> 39	
> 40	## bear 2022 — 8 alts, capital total 8000 USDT
> 41	
> 42	| Alt | BTC acumulado | Lucro realiz. (USDT) | Buys/Sells | Inventário preso (PnL n/realiz.) | Retorno equity | MaxDD | Exposição | % bear |
> 43	|---|---|---|---|---|---|---|---|---|
> 44	| BNBUSDT | +0.00039 | 10.30 | 11/11 | $0.00 ($0.00) | 0.68% | -5.37% | 10.81% | 55.05% |
> 45	| ETHUSDT | +0.00012 | 3.69 | 3/3 | $0.00 ($0.00) | 0.20% | -0.20% | 0.25% | 51.63% |
> 46	| SOLUSDT | +0.00165 | 33.08 | 29/21 | $558.89 ($-241.11) | -21.23% | -50.19% | 20.49% | 62.35% |
> 47	| XRPUSDT | +0.00028 | 9.65 | 8/8 | $0.00 ($0.00) | 0.49% | -0.67% | 1.29% | 54.32% |
> 48	| ADAUSDT | +0.00173 | 41.75 | 34/33 | $78.07 ($-21.93) | 0.82% | -4.25% | 33.12% | 63.28% |
> 49	| LINKUSDT | +0.00378 | 81.25 | 52/51 | $86.39 ($-13.61) | 5.23% | -15.20% | 29.62% | 57.05% |
> 50	| LTCUSDT | +0.00065 | 14.32 | 12/12 | $0.00 ($0.00) | 1.14% | -1.56% | 1.94% | 51.70% |
> 51	| AVAXUSDT | +0.00198 | 43.52 | 30/28 | $152.73 ($-47.27) | -1.28% | -10.79% | 20.44% | 61.69% |
> 52	
> 53	**Agregado bear 2022:** BTC acumulado **+0.01057** (≈ **+0.01057 BTC/ano**) · lucro realizado **$237.55** sobre **$8000** de capital · retorno do equity total **-1.74%** · inventário preso no fim **$876.08** (PnL não-realizado **$-323.92**) · maxDD médio **-11.03%** · exposição média **14.74%** · janela classificada bear **57.13%** do tempo.
> 54	
> 55	
> 56	## 🎯 Síntese — taxa de acúmulo e o que falta pra +3 BTC
> 57	
> 58	| Período | BTC/ano (por 8000 USDT) | Lucro realiz. | Retorno equity | Inventário preso | % bear |
> 59	|---|---|---|---|---|---|
> 60	| recente (~últ. 365d) | +0.00075 | $65.34 | -3.54% | $399.56 | 55.05% |
> 61	| bull 2023-24 | +0.00231 | $42.49 | 0.89% | $0.00 | 40.23% |
> 62	| bear 2022 | +0.01057 | $237.55 | -1.74% | $876.08 | 57.13% |
> 63	
> 64	**Leitura honesta:**
> 65	- **BTC/ano** é a taxa do funil normalizada pelo capital de trabalho (8×1000 = 8000 USDT). Pra +3 BTC, escale capital × tempo: dobrar o capital ~dobra a taxa (até o teto de liquidez/lotes).
> 66	- O **inventário preso** é o calcanhar do no-loss: capital que ficou comprado sem fechar no lucro (pior no bear). Se grande, o "lucro realizado" foi em parte financiado por capital imobilizado — por isso o **retorno do equity total** (que inclui esse inventário marcado a mercado) é o juiz, não o lucro realizado isolado.
> 67	- **% bear** mostra quanto do tempo o gate de regime manteve o grid em caixa (sem comprar). Em janelas muito bear, o farm quase não roda — é esperado e é a proteção funcionando.
> 68	
> 69	---
> 70	_Gerado por backend/scripts/backtest-farm-funnel.js. Dados: Binance klines reais (mainnet, cache em backtest-data/). Net de fee. Não é conselho financeiro; validação de estratégia._
> ```

## 🤖 Claude *(15:04:17)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/backtest-results/farm-funnel-15m-macro2000.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# TradeUX — Backtest "Farm-and-Funnel" (grid no-loss multi-alt → funil pra BTC)
> 2	
> 3	> 8 alts · 15m · fee 0.1%/lado · exec no open seguinte (sem lookahead).
> 4	> Grid: capital 1000 USDT/alt, lote 100, máx 8 lotes, passo 1.50%, lucro-alvo 0.60%, compra RSI<35, gate regime !=bear + filtro macro SMA2000 não-caindo (slope 960).
> 5	> Funil: o lucro LÍQUIDO de cada venda (farm e trend) vira BTC ao preço do BTC no momento. O principal volta pro caixa de trabalho.
> 6	
> 7	
> 8	## recente (~últ. 365d) — 8 alts, capital total 8000 USDT
> 9	
> 10	| Alt | BTC acumulado | Lucro realiz. (USDT) | Buys/Sells | Inventário preso (PnL n/realiz.) | Retorno equity | MaxDD | Exposição | % bear |
> 11	|---|---|---|---|---|---|---|---|---|
> 12	| BNBUSDT | +0.00008 | 6.22 | 8/8 | $0.00 ($0.00) | 0.52% | -0.19% | 0.42% | 45.24% |
> 13	| ETHUSDT | +0.00005 | 3.76 | 4/4 | $0.00 ($0.00) | 0.30% | -0.17% | 0.15% | 55.88% |
> 14	| SOLUSDT | +0.00015 | 13.25 | 16/15 | $50.66 ($-49.34) | -3.95% | -5.12% | 42.05% | 53.68% |
> 15	| XRPUSDT | +0.00018 | 14.55 | 16/15 | $53.41 ($-46.59) | -3.53% | -5.00% | 45.52% | 61.62% |
> 16	| ADAUSDT | +0.00005 | 4.20 | 6/6 | $0.00 ($0.00) | 0.29% | -0.22% | 0.93% | 63.11% |
> 17	| LINKUSDT | +0.00016 | 13.47 | 17/16 | $63.19 ($-36.81) | -2.64% | -4.30% | 42.25% | 54.52% |
> 18	| LTCUSDT | +0.00033 | 34.58 | 19/19 | $0.00 ($0.00) | 2.08% | -1.91% | 2.67% | 54.81% |
> 19	| AVAXUSDT | +0.00021 | 16.58 | 21/20 | $75.18 ($-24.82) | -1.17% | -3.33% | 7.17% | 56.03% |
> 20	
> 21	**Agregado recente (~últ. 365d):** BTC acumulado **+0.00120** (≈ **+0.00120 BTC/ano**) · lucro realizado **$106.61** sobre **$8000** de capital · retorno do equity total **-1.01%** · inventário preso no fim **$242.44** (PnL não-realizado **$-157.56**) · maxDD médio **-2.53%** · exposição média **17.64%** · janela classificada bear **55.61%** do tempo.
> 22	
> 23	
> 24	## 🎯 Síntese — taxa de acúmulo e o que falta pra +3 BTC
> 25	
> 26	| Período | BTC/ano (por 8000 USDT) | Lucro realiz. | Retorno equity | Inventário preso | % bear |
> 27	|---|---|---|---|---|---|
> 28	| recente (~últ. 365d) | +0.00120 | $106.61 | -1.01% | $242.44 | 55.61% |
> 29	
> 30	**Leitura honesta:**
> 31	- **BTC/ano** é a taxa do funil normalizada pelo capital de trabalho (8×1000 = 8000 USDT). Pra +3 BTC, escale capital × tempo: dobrar o capital ~dobra a taxa (até o teto de liquidez/lotes).
> 32	- O **inventário preso** é o calcanhar do no-loss: capital que ficou comprado sem fechar no lucro (pior no bear). Se grande, o "lucro realizado" foi em parte financiado por capital imobilizado — por isso o **retorno do equity total** (que inclui esse inventário marcado a mercado) é o juiz, não o lucro realizado isolado.
> 33	- **% bear** mostra quanto do tempo o gate de regime manteve o grid em caixa (sem comprar). Em janelas muito bear, o farm quase não roda — é esperado e é a proteção funcionando.
> 34	
> 35	---
> 36	_Gerado por backend/scripts/backtest-farm-funnel.js. Dados: Binance klines reais (mainnet, cache em backtest-data/). Net de fee. Não é conselho financeiro; validação de estratégia._
> ```

## 🤖 Claude *(15:04:22)*

Now I have rich per-symbol data. The key insight for the cross-symbol expansion question is emerging clearly. Let me analyze the per-symbol economics against the real $149 capital and the $25/symbol Farm exposure cap. Let me check the live setup-farm script to understand which symbols are configured and the exact caps.

## 🤖 Claude *(15:04:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls /home/gcrux-tradeux/tradeux/backend/scripts/ | grep -iE \"farm|trend|scan\" ; echo \"---\"; grep -rn \"FARM_MAX_NOTIONAL\\|MAX_ORDER_NOTIONAL\\|MIN_NOTIONAL\\|minNotional\" /home/gcrux-tradeux/tradeux/backend/src/ 2>/dev/null | head -20",
  "description": "Find farm/scanner scripts and notional cap constants"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> activate-trend.js
> backtest-farm-funnel.js
> backtest-futures-trend.js
> setup-farm.js
> setup-trend.js
> ---
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:26:const FARM_MAX_NOTIONAL_USDT = (() => { const n = parseFloat(process.env.FARM_MAX_NOTIONAL_USDT || '0'); return Number.isFinite(n) && n > 0 ? n : 0; })();
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:228:    else if (orderTemplate.quantity === 'MIN_NOTIONAL') {
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:229:        newQty = (parseFloat(symbol.minNotional) / parseFloat(price)) * (multiplier < 1 ? 1 : multiplier);
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:286:    // (MIN_NOTIONAL) ABAIXO do mínimo da Binance ($5) → ordem rejeitada com -1013 (NOTIONAL) e a automação
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:287:    // NÃO compra (ex.: id6 Trend Buy com mult=1 a ~$66k → $4,65). Só p/ MIN_NOTIONAL: se o resultado floored
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:288:    // não cobre o minNotional, sobe 1 stepSize (menor ordem válida). NÃO afeta posições — TREND_QTY/
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:290:    // um resultado já-válido (mult>=~1.1 ou símbolo que floored acima de $5) não muda. O teto MAX_ORDER_NOTIONAL
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:292:    if (orderTemplate.quantity === 'MIN_NOTIONAL' && parseFloat(price) > 0 && (result * parseFloat(price)) < parseFloat(symbol.minNotional)) {
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:320:    else if (orderTemplate.quantity === 'MIN_NOTIONAL') {
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:321:        return (parseFloat(symbol.minNotional) * (multiplier < 1 ? 1 : multiplier)).toFixed(symbol.quotePrecision);
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:490:    // Teto de EXPOSIÇÃO do Farm por símbolo (FARM_MAX_NOTIONAL_USDT): a COMPRA do Farm NÃO acumula mais que o teto
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:495:    if (order.side === 'BUY' && FARM_MAX_NOTIONAL_USDT > 0 && /^Farm Buy /.test(automation.name || '')) {
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:499:        if (_invested >= FARM_MAX_NOTIONAL_USDT) {
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:500:            const _msg = `[farmCap] ${order.symbol}: $${_invested.toFixed(2)} investido no Farm (teto $${FARM_MAX_NOTIONAL_USDT}) — compra ignorada.`;
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:506:    const isDynamicBuy = order.side === 'BUY' && ['MIN_NOTIONAL', 'MAX_WALLET'].includes(orderTemplate.quantity);
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:508:        && (isDynamicBuy || orderTemplate.quantity === 'MIN_NOTIONAL')) {
> /home/gcrux-tradeux/tradeux/backend/src/repositories/symbolsRepository.js:41:    if (newSymbol.minNotional && newSymbol.minNotional !== currentSymbol.minNotional)
> /home/gcrux-tradeux/tradeux/backend/src/repositories/symbolsRepository.js:42:        currentSymbol.minNotional = newSymbol.minNotional;
> /home/gcrux-tradeux/tradeux/backend/src/utils/exchange.js:16://   MAX_ORDER_NOTIONAL_USDT=<n>  → teto de notional por ordem em USDT (0 = desligado). Cobre MARKET por
> /home/gcrux-tradeux/tradeux/backend/src/utils/exchange.js:30:const _maxNotional = parseFloat(process.env.MAX_ORDER_NOTIONAL_USDT || '0');
> ```

## 🤖 Claude *(15:04:33)*

I have enough to do the honest quantification. The critical constraint is the $25/symbol Farm exposure cap and $25/order cap against $149 total capital. Let me do the capital-fragmentation math to ground the magnitude claims.

The key numbers from the real backtests, normalized per symbol per $1000 working capital:
- Farm-só recente (lateral, the current regime): per-symbol equity return -3.5% to +0.5%, lucro realizado ~$3-17/symbol/year, BTC accrued ~$0.00004-0.00017/symbol/year.
- The "best" farm symbols (low stuck inventory): BNB, ETH, ADA, LTC, AVAX = near-flat, never trap inventory. SOL/XRP/LINK = bleed via trapped inventory (-11% to -13% equity drawdown).
- Crucially: 15m LTC did notably better (+2.08% equity, $34.58 realized) than 1h — granularity helps farm.

Now the capital math at $149 with $25/symbol cap:

## 🤖 Claude *(15:04:46)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "python3 -c \"\ncap_total = 149.0\nfarm_cap_per_sym = 25.0\nmin_notional = 5.0  # Binance floor\n# How many symbols can be funded at the cap simultaneously?\nprint('Max symbols fully funded at \\$25 cap:', cap_total/farm_cap_per_sym, '-> ~5-6 symbols if ALL maxed, but only if all dip at once')\n# Realistic: cap is exposure ceiling not allocation. Real working capital is shared USDT pool.\n# Lote size to be MIN_NOTIONAL-safe with buffer: ~\\$6-7. At \\$25 cap = ~3-4 lots/symbol.\nlote = 6.5\nprint('Lots per symbol at \\$25 cap / \\$%.1f lote:'%lote, farm_cap_per_sym/lote)\n# Per-symbol farm yield (recente/lateral, 1h farm-so) was ~\\$3-17 realized per \\$1000 deployed-capital-equiv\n# But deployed capital per symbol in backtest was up to maxLots*lote = 8*100=\\$800, not \\$1000 nominal.\n# Scale to \\$25: realized profit scales ~linearly with deployed capital.\n# Backtest realized/yr per symbol (recente 1h) avg over non-trapping syms (BNB,ETH,ADA,LTC,AVAX): \nvals=[3.32,7.32,8.88,3.22,7.19]\nprint('avg realized/yr per symbol (good farmers, \\$800-ish deployed peak):', sum(vals)/len(vals))\n# scale to \\$25 exposure (vs ~\\$100-800 deployed): take \\$ realized per \\$ deployed\n# deployed peak in those near-flat cases was small (exposure 0.3-7%) - profit came from few round trips\n# Honest: at \\$25/symbol the realized \\$/yr is roughly profit_per_roundtrip * n_roundtrips, ~\\$0.6%*25*nRT\n# nRT (sells) recente good farmers: 4,8,9,4,8 = avg ~6.6 sells/yr\nnrt=[4,8,9,4,8]\nprint('avg sells/yr:', sum(nrt)/len(nrt))\nprint('Est realized \\$/yr per symbol at \\$25 deployed, 0.6% net/RT, 6.6 RT:', 25*0.006*6.6)\nprint('  -> across 5 symbols:', 5*25*0.006*6.6, 'USDT/yr =', 100*5*25*0.006*6.6/149, '% of \\$149/yr')\n\"\n",
  "description": "Capital fragmentation and yield math at $149 with $25 cap"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Max symbols fully funded at $25 cap: 5.96 -> ~5-6 symbols if ALL maxed, but only if all dip at once
> Lots per symbol at $25 cap / $6.5 lote: 3.8461538461538463
> avg realized/yr per symbol (good farmers, $800-ish deployed peak): 5.986
> avg sells/yr: 6.6
> Est realized $/yr per symbol at $25 deployed, 0.6% net/RT, 6.6 RT: 0.9899999999999999
>   -> across 5 symbols: 4.949999999999999 USDT/yr = 3.3221476510067114 % of $149/yr
> ```

## 🤖 Claude *(15:04:54)*

The math is decisive. I now have everything needed for an EV-honest assessment. Let me verify one more thing — the correlation/diversification angle and which pairs are liquid/farmable vs trapping — by checking the bear-period trapped-inventory pattern across symbols, which is the real risk of adding more pairs.

The pattern across all three regimes is consistent and clear:
- **Trapping symbols** (high volatility): SOL, XRP, LINK, AVAX → bleed equity (-3% to -21%) via stuck inventory, especially in bear/lateral.
- **Clean farmers** (stable, mean-reverting): BNB, ETH, ADA, LTC → near-zero stuck inventory, small positive realized profit.
- Adding MORE symbols multiplies round-trips (good) but the per-trade edge stays ~0.6% gross / fee-fragile, and at $149 the per-symbol cap of $25 makes the absolute $/yr trivial (~$5/yr across 5 symbols = ~3% of capital/yr, before bear drawdown).

I have enough for an honest, grounded answer.

## 🤖 Claude *(15:05:46)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "candidates": [
    {
      "lever": "Curar o universo do Farm por trappabilidade, nao expandir a contagem",
      "mechanism": "O backtest farm-so (1h e 15m, dados reais mainnet, fee 0,1%/lado) mostra que adicionar pares NAO adiciona edge/trade \u2014 adiciona round-trips, e a maioria dos round-trips extras vem dos pares VOLATEIS que prendem inventario. Padrao consistente nos 3 regimes (farm-funnel-1h-macro500.md / farm-funnel-15m-macro2000.md): pares que NUNCA prendem inventario e ficam ~flat-positivos = BNB/ETH/ADA/LTC (inventario preso $0,00, eqRet -0% a +2%); pares que SANGRAM via inventario preso = SOL/XRP/LINK/AVAX (recente: SOL eqRet -13,1%/DD -13,6%, LINK -11,4%/-13,9%, XRP -4,7%; bear: SOL -21,2%/DD -50,2%). O 'no-loss' nao elimina perda, converte em inventario preso marcado-a-mercado \u2014 exatamente o que o equity total penaliza. A alavanca real do Bloco C nao e mais simbolos, e SELECIONAR os mean-reverting liquidos e DESCARTAR os trend-followers (que ja sao cobertos pela camada Trend no bull, nao pelo Farm). LTC e o melhor farmer no 15m ($34,58 realiz., +2,08% eq, 0 preso); BNB/ADA/ETH limpos; manter 3-5 desses, jamais SOL no Farm.",
      "expected_magnitude": "Evita o pior ~3-21% de drawdown por par-volatil sem perder quase nada de upside (os clean farmers ja respondem por ~$3-9 realiz./ano cada por ~$800 de pico empregado). Ganho = RISCO-AJUSTADO (corta cauda de inventario preso), nao alfa. Em USDT absoluto no $149 atual: desprezivel; em maxDD evitado: significativo.",
      "dependency": "Depende de SIMBOLOS (selecao por liquidez+mean-reversion) e de EDGE ja validado; NAO depende de mais capital. Mantem o teto FARM_MAX_NOTIONAL_USDT=$25/simbolo intacto.",
      "is_novel": true,
      "validation_path": "Backtest ja existe e ja roda: rodar backtest-farm-funnel.js farm-so por par individual nos 3 regimes (1h e 15m) e rankear por (inventario preso final, eqRet, maxDD); descartar quem prende. ~10 min de CPU, zero round-trips reais. Confirmar ao vivo no canary FARM-ONLY que ja esta no ar (LTC/BNB/ADA) antes de adicionar qualquer 4o par."
    },
    {
      "lever": "Granularidade 15m no Farm em vez de mais pares (mesmo capital, mais round-trips no-loss limpos)",
      "mechanism": "O caminho honesto pra AUMENTAR a contagem de oportunidades no-loss sem fragmentar os $149 nem adicionar correlacao/concentracao e baixar o timeframe do Farm de 1h pra 15m nos MESMOS pares limpos. Comparando os dois relatorios reais (recente/lateral, o regime atual): 1h farm-so = $65,34 realiz. agregado, +0,00075 BTC/ano, eqRet -3,54%, $399,56 preso; 15m farm-so = $106,61 realiz. (+63%), +0,00120 BTC/ano (+60%), eqRet -1,01% (MELHOR) e inventario preso CAI pra $242,44. Granularidade menor = mais dips capturados e fechados (mais round-trips) E menos inventario preso (sai mais rapido no lucro), exatamente o efeito que adicionar pares NAO da. Isso e o mesmo achado do STRATEGY-farm-funnel ('15m bate o 1h em todos os regimes').",
      "expected_magnitude": "+60% de round-trips e BTC/ano vs 1h, com MENOS drawdown e MENOS inventario preso \u2014 pelo MESMO capital e MESMOS pares (sem custo de fragmentacao/concentracao). Ainda assim alfa marginal em termos absolutos: no $149, +60% de ~$1/ano/simbolo continua ~centavos/dia. O valor e risco-ajustado, nao escala.",
      "dependency": "Depende de CUSTO (15m = mais trades = mais sensivel a fee; ja net 0,1%/lado no backtest e o EV continua positivo nos clean farmers) e de wiring (monitor CANDLES 15m). NAO depende de mais capital nem de mais simbolos.",
      "is_novel": true,
      "validation_path": "Backtest 15m ja existe e os dados 15m ja estao em cache (backtest-data/*-15m-*.json). Validar EV liquido por par no 15m (cuidado com fee: confirmar que cada clean farmer fica EV+ liquido, nao so agregado). Depois paper: rotear os Farm 15m com prefixo [PAPER] no Paper/Shadow Engine que ja existe (fill ao MINI_TICKER mainnet + fee real + slippage), ~30-60 round-trips (~1-2 meses no regime atual) antes de tocar real."
    },
    {
      "lever": "Tratar o cap de $25/simbolo como o veredito de escala: cross-simbolo NAO move a agulha a $149",
      "mechanism": "Quantificacao honesta do angulo pedido: a $149 com FARM_MAX_NOTIONAL_USDT=$25/simbolo e MIN_NOTIONAL ~$5 da Binance, cabem no maximo ~5-6 simbolos custeados ao teto SIMULTANEAMENTE \u2014 e so se todos derem dip ao mesmo tempo (improvavel; o pool de USDT e compartilhado). Com lote ~$6,5 (folga sobre o MIN_NOTIONAL pra nao tomar -1013), sao ~3-4 lotes/simbolo. O edge/round-trip e ~0,6% liquido (lucro-alvo do no-loss, ja acima do round-trip de fee); a ~6,6 vendas/ano por clean farmer, isso da ~$0,99/ano/simbolo a $25 empregado \u2192 ~$5/ano somando 5 simbolos = ~3,3% do capital/ano BRUTO, ANTES do drawdown de bear. Adicionar pares multiplica round-trips mas (a) cada par novo so pode empregar ate $25, (b) os $149 nao sustentam 5 caps cheios de uma vez (fragmentacao), (c) pares novos liquidos sao ALTAMENTE correlacionados ao BTC \u2192 'diversificar' nao reduz risco sistemico, so adiciona base de inventario preso num dump conjunto (concentracao disfarcada). Conclusao EV-honesta: cross-simbolo aumenta a CONTAGEM de no-loss mas o ganho absoluto a $149 e ~ruido; o multiplicador real e CAPITAL \u00d7 TEMPO \u00d7 captura-de-bull-pelo-Trend, nao numero de pares.",
      "expected_magnitude": "~$5/ano (~3% do capital, bruto, sem bear) somando os 5 melhores pares ao teto \u2014 ordem de grandeza de CENTAVOS/dia. Nao e caminho pra +3 BTC (ja refutado como 'seculos' no farm-so). Honestidade: a expansao cross-simbolo e gestao de risco/cobertura de regime, NAO um motor de retorno.",
      "dependency": "Depende criticamente de CAPITAL (a $149 e irrelevante; so vale a pena revisitar a contagem de pares quando o capital crescer o suficiente pra custear varios caps de $25 sem fragmentar). Independe de novo edge.",
      "is_novel": true,
      "validation_path": "Nenhum backtest novo necessario \u2014 e aritmetica de capital sobre os relatorios farm-funnel ja existentes + os caps em beholder.js (FARM_MAX_NOTIONAL_USDT) e exchange.js (MAX_ORDER_NOTIONAL_USDT). Registrar como decisao: NAO expandir a contagem de pares do Farm enquanto capital < ~$300-500; priorizar selecao (alavanca 1) + 15m (alavanca 2) sobre os 3-5 pares atuais."
    }
  ]
}
```

> **Tool Result (StructuredOutput)** - ✅ Success
>
> ```
> Structured output provided successfully
> ```

## 🤖 Claude *(15:06:03)*

Análise concluída. Resumo dos achados (fontes em caminhos absolutos abaixo).

**Veredito central do ângulo cross-símbolo:** a $149 com teto `FARM_MAX_NOTIONAL_USDT=$25/símbolo`, expandir a CONTAGEM de pares aumenta round-trips mas NÃO o edge/trade — e o ganho absoluto é ruído (~$5/ano somando os 5 melhores pares = ~3% do capital/ano bruto, antes do drawdown de bear). O multiplicador real é capital × tempo × captura-de-bull-pelo-Trend, não número de pares.

**3 alavancas EV-honestas (todas novas vs. refutados, todas validáveis no harness/cache já existentes):**

1. **Curar o universo por trappabilidade, não expandir contagem.** Padrão consistente nos 3 regimes: BNB/ETH/ADA/LTC nunca prendem inventário (eqRet -0% a +2%); SOL/XRP/LINK/AVAX sangram via inventário preso (SOL -13% recente / -21% e DD -50% no bear). A alavanca é selecionar mean-reverting líquidos e descartar trend-followers (já cobertos pela camada Trend). Ganho = risco-ajustado, não alfa.

2. **Granularidade 15m nos mesmos pares limpos.** Comparação real: 1h farm-só recente = $65,34 realiz., eqRet -3,54%, $399,56 preso; 15m = $106,61 (+63%), eqRet -1,01% (melhor) e preso cai pra $242,44. Mais round-trips no-loss limpos pelo MESMO capital e MESMOS pares — sem custo de fragmentação/concentração.

3. **O cap de $25/símbolo É o veredito de escala.** Aritmética: ~$0,99/ano/símbolo a $25 empregado × 5 = ~$5/ano. Pares novos líquidos são altamente correlacionados ao BTC → "diversificar" não reduz risco sistêmico, só adiciona base de inventário preso num dump conjunto. Decisão: não expandir contagem enquanto capital < ~$300-500.

**Fontes-chave:**
- `/home/gcrux-tradeux/tradeux/backend/backtest-results/farm-funnel-1h-macro500.md` (per-símbolo farm-só, 3 regimes)
- `/home/gcrux-tradeux/tradeux/backend/backtest-results/farm-funnel-15m-macro2000.md` (15m vence)
- `/home/gcrux-tradeux/tradeux/backend/scripts/backtest-farm-funnel.js` (engine; `--alts=`, `--interval=15m`, `--macrosma`)
- `/home/gcrux-tradeux/tradeux/backend/src/beholder.js:26,490-506` (teto FARM_MAX_NOTIONAL_USDT)
- `/home/gcrux-tradeux/tradeux/docs/STRATEGY-farm-funnel.md` (§3 tabela, §4 seleção de alts)

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-21 - agent-a9cb9f6ee77213f3d]]
> * **Próxima Sessão**: [[2026-06-21 - agent-aaa3db5f0cfb73510]]
%% --- TIMELINE END --- %%

# Session agent-a3c2eabacbaba75bd
**Date:** 2026-06-21 | **Session ID:** `agent-a3c2eabacbaba75bd`

---

## 👤 User *(15:13:00)*


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


LEDGER:
{"constraints":["Capital REAL ~$148,84 USDT, MAINNET LIVE, spot-only, sem futuros/alavancagem (tradeux-mainnet-go-live.md:12; CLAUDE.md 'Binance Spot'). Escala: +3 BTC e impossivel (~1350x o patrimonio) — tradeux-mainnet-go-live.md:34.","Fee Binance = 0,1%/lado taker em TODO backtest (backtest.js:24 e backtest-farm-funnel.js:28 'FEE = 0.001'); 0,075% com desconto BNB. Em SPOT maker==taker — NAO existe rebate (so Futures/VIP) — tradeux-1m-scalping-and-cockpit.md:14.","COFRE BTC nunca vende a base: trava fail-closed isBtcVaultSymbol vive SO no caminho MCP (place_order), NAO no beholder/exchange — tradeux-vault-guard / tradeux-mainnet-go-live.md:36,39. Grupo 'baseline' inclui venda do cofre coberta so por HALT+riskGuard.","Claude NUNCA vira o HALT — repetido em todas as memorias (tradeux-mainnet-go-live, harvester, strategy-engine). Flip real = .env TRADING_HALT=false + restart (derruba o env floor); POST /system/halt {on:false} so solta o manual.","Agente LLM NAO coloca ordem real: ALLOW_TRADING=false verificado no container + MCP write tools throw (tradeux-mainnet-go-live.md:36). Guardrails de notional sao prompt-level; o cap duro e backend (riskState/exchange.js chokepoint).","Caps de risco DUROS no backend (exchange.js chokepoint por-ordem, QUENTE via riskState.isHalted): teto por-ordem MAX_ORDER_NOTIONAL_USDT=$25 + teto de exposicao do Farm FARM_MAX_NOTIONAL_USDT=$25/simbolo + cap diario -5% (dailyCapJob, Earn LD* excluido) — tradeux-mainnet-go-live.md:26,49,50.","Estado LIVE atual (2026-06-19/20): dono destravou o floor; canary FARM-ONLY (alts LTC/BNB/ADA no-loss, 6 autos), Trend e Baseline PARADOS. Pos-1a ordem real: Farm DCA 3x em LTC, COMPRAS desligadas, so VENDAS armadas (3/6) — tradeux-mainnet-go-live.md:42-53. SEMPRE conferir GET /system/halt no inicio da sessao.","GOTCHA de calculo (money-path): MEMORY['<sym>:FARM_DCA'].cost = PRECO MEDIO/unidade (totalCost/totalQty), NAO USDT investido; investido = qty*cost. Condition do Farm Sell = bestBid > cost*1.012 (preco vs preco) — tradeux-mainnet-go-live.md:51.","GOTCHA de dado: tabela orders MISTURA testnet+mainnet; pra P&L/posicao REAL SEMPRE filtrar isTestnet=false (senao soma fantasmas — ex. 22 LTC/$997 de 15/jun eram testnet) — tradeux-mainnet-go-live.md:52.","No-loss do Farm vende SO acima do custo: backtest minProfit=0,6% (GP.minProfit=0.006, backtest-farm-funnel.js:45); live buffer = cost*1.012 (1,2% >> round-trip de fee). 'No-loss' NAO elimina perda — converte em INVENTARIO PRESO (pior no bear) — STRATEGY-farm-funnel.md:91, backtest-farm-funnel.js:11-12.","BTC nao e farmado (e o cofre); id3 Baseline Sell BTCUSDT pausada (vendia BTC sem gate de lucro = a sangria que motivou o estudo) — STRATEGY-farm-funnel.md:74; id2 Baseline Buy BTC isActive=0 (acumulador pelado sem venda) — tradeux-mainnet-go-live.md:32.","Edge do trading ativo e RISCO-AJUSTADO (drawdown menor), NAO alfa absoluto: em bull o melhor e segurar (B&H domina), em bear todo long-only perde — STRATEGY-3BTC-assessment.md:23-24, backtest-1h-365d.md:130-131."],"refuted":[{"idea":"+3 BTC de alfa absoluto long-only spot","verdict":"IMPOSSIVEL (~1350x)","evidence":"tradeux-mainnet-go-live.md:34 ('+3 BTC e impossivel (1.350x)'); STRATEGY-3BTC-assessment.md:23. $148 spot ~ FLAT no mes; sem rendimento diario nessa escala."},{"idea":"HFT / scalping 1m como motor de P&L","verdict":"MORTO (EV negativo por trade)","evidence":"Backtest fresco em cache real BTCUSDT-1m-60d (86.400 velas): -0,14% a -0,23% liquido POR TRADE em TODAS parametrizacoes (k_ATR 1-2, horiz 10-20, fee 0,075/0,10%); win 35-48% sub-breakeven — tradeux-1m-scalping-and-cockpit.md:13. Move mediano 1m ~0,036-0,15% < custo ~0,15-0,20%. Cockpit reporta EV/trade net -0,16%, pHit 0,6%."},{"idea":"Frequencia / 'verde diario' (5m/15m)","verdict":"REFUTADO (8/8 EV liquido < 0)","evidence":"Workflow paper-frequencia-research, 8 combos 4sym x 5m/15m, mainnet+fee 0,1%/lado: 8/8 EV/trade liquido NEGATIVO (win 52-68% mas EV<0; mais frequencia = pior) — tradeux-strategy-engine.md:31. Verdes so em gate-regime esparso (caixa-no-bear), NAO frequencia."},{"idea":"Harvester de dislocacao -3% (id22-25)","verdict":"MORTO no mainnet (artefato testnet) + EV- no re-design","evidence":"Codigo: FAIR=lastPrice mainnet (fairPriceService.js:33) + book sintetico spread-0 do miniTicker (app-em.js:38) = mesma venue → gatilho bestAsk<FAIR*0.97 estruturalmente inalcancavel. Dado: 0 ordens harvester no mainnet (orders=259 TODAS testnet); +1529 USDT eram 100% testnet. Re-ancorar ao HIGH rolante: backtest dado-real (klines 1h, fee 0,1%/lado, 3sym x 4 regimes) = 17/18 configs P&L NEGATIVO (unica + = +$14,78/~$12k = +0,12%, ruido, 36% maxDD) — tradeux-harvester-experiment.md:32. id22-25 isActive=0; NAO reativar."},{"idea":"Grid simetrico nativo do Beholder (gridEval/generateGrids)","verdict":"REJEITADO (sangra o cofre)","evidence":"id21 operou 26 ordens MAS vende por nivel DIRETO DA CARTEIRA sem rastrear inventario → 24 SELL vs 2 BUY → drenou ~0,0044 BTC do cofre — tradeux-harvester-experiment.md:16. Script com aviso 'NAO-ATIVAR'. Solucao: padrao bucket {qty,cost} (vende so o que comprou)."},{"idea":"Bear-capture via futuros (short / trend bilateral)","verdict":"FALSO POSITIVO no ciclo + fora de escopo","evidence":"Backtest proprio bilateral (backtest-futures-trend.js, custo 0,07%/lado + funding 8h REAL): captura a queda ISOLADA (bear: trendBi NET +5,01% medio vs B&H -34,42%, 3/4 sym — backtest-futures-1h-bear-365d.md:51) MAS no CICLO e dominado pelo regime-gating (ciclo +88% vs +338%); no bull longGated +79,64% vs B&H +338,21% (sacrifica upside) — backtest-futures-1h-bull-end2024-04-01.md:52,54. maxDD -51% a 1x; Sharpe liq 0,31→~0,15 pos-haircut; ADX PIORA (whipsaw). DECISAO: NAO construir modulo de short."},{"idea":"Maker-rebate em Binance SPOT","verdict":"REFUTADO (nao existe)","evidence":"Na Binance SPOT maker==taker (0,075% com BNB nos 2 lados); rebate so em Futures/VIP — tradeux-1m-scalping-and-cockpit.md:14. Verificadores rejeitaram a abordagem."},{"idea":"toxicity/VPIN do flow oracle como forecast direcional","verdict":"REFUTADO 0-3 (rebaixado a nowcasting)","evidence":"Deep research (24 fontes): VPIN-como-forecasting de jumps de BTC refutado 0-3; OFI e nowcasting (~2 price changes/~10s, base equities) — tradeux-bear-capture-research.md:18. toxicity rebaixada a gatilho de timing/execucao (commit c67d6bc)."},{"idea":"Bater Buy&Hold em RETORNO BRUTO num bull","verdict":"DIFICILIMO (B&H domina)","evidence":"Bull 180d: B&H medio +293,61% OOS, melhor ativa (sempre-trend) +146,57%, regime-switch V2 +50,55% — backtest-1h-180d-end2024-04-01.md:103-104. Bate B&H em 0/4 simbolos. Cada saida custa upside + fee."},{"idea":"'Fable 5 / Polymarket 205x' ($11k→$300k)","verdict":"GOLPE de referral","evidence":"Link polymarket.com/profile/...?via=ace-cjyf; narrativa fabricada pra dirigir cadastro/deposito/copy-trade — tradeux-1m-scalping-and-cockpit.md:24. NAO clicar/depositar/copy-tradar."}],"validated_edges":[{"edge":"Regime-gating: ficar em CAIXA no bear corta o drawdown (o maior edge)","magnitude":"BTC 365d-bear OOS: regime-switch V2 +0,61% (agregado 4 sym) vs B&H -23,82%; bate B&H em 4/4 (backtest-1h-365d.md:100,104). BTC isolado: regime-switch ~-7% vs B&H ~-27% OOS (backtest-1h-365d.md:131). Sem-supervisao no farm-funnel: bear 2022 retorno equity -1,7% (farm-so) vs B&H ~-60% nos pares.","evidence":"backtest.js regimeSwitch V2 (histerese, regimeWindowV2:233); backtest-1h-365d.md secao agregada; STRATEGY-3BTC-assessment.md:18."},{"edge":"Trend (SMA50/200, comprado no bull / caixa no bear) = motor do bull","magnitude":"Farm+Trend+funil no bull 2023-24: retorno equity +22,6% (BTC/ano 16x o farm), drivers ETH+52%/SOL+50%/AVAX+49%/LINK+41% (farm-funnel-1h-full-macro500.md:38, tabela:30-36). In-sample 180d SOL trend SMA20/50 +344,93% (backtest-1h-180d:81); sensibilidade 180d trend 50/200 melhor que 20/50. Em janelas de bull a doc cita +22% a +147%.","evidence":"backtest-farm-funnel.js gridTrendFunnel (smaCross:251); farm-funnel-1h-full-macro500.md; tradeux-trend-following.md."},{"edge":"Farm no-loss (DCA em RSI<35, vende a custo*1.012) = alfa marginal, baixo risco","magnitude":"Farm-so + macro (farm-funnel-1h-macro500.md): recente -3,54%, bull +0,89%, bear -1,74% retorno equity; maxDD medio -4,68%/-0,31%/-11,03%; BTC/ano +0,00075 a +0,01057 por $8000 → +3 BTC = 'seculos'. STRATEGY-farm-funnel.md:53: farm-so -3,5%/+0,9%/-1,7%. Drawdown muito menor que o trend.","evidence":"backtest-farm-funnel.js gridFunnel (vendas no-loss:202-212); farm-funnel-1h-macro500.md sintese:60-62; STRATEGY-farm-funnel.md:53."},{"edge":"Menos trades perdem menos (fee+whipsaw punem overtrading)","magnitude":"365d MR: RSI 25/75 -19,34% (~17,5 trades) vs 30/70 -38,59% (~31,8) vs 35/65 -44,01% (~53,5); trend 50/200 -10,90% (~27,5) vs 20/50 -25,46% (~92,8) vs 10/30 -34,44% (~167,3) — backtest-1h-365d.md:113-126. Calibracao recomendada: RSI 25/75 (nao 30/70), SMA 50/200 (nao 20/50).","evidence":"backtest.js runCalibration / secao de sensibilidade; backtest-1h-365d.md:128-133; STRATEGY-3BTC-assessment.md:20,27."},{"edge":"Switch de regime (trend on em bull, farm-so em lateral) e o melhor compromisso sem supervisao","magnitude":"Farm+Trend+Switch (15m, config final): recente -5,5% / bull +14,4% / bear -0,4% (STRATEGY-farm-funnel.md:56). 15m bate o 1h em todos os regimes (granularidade menor = mais farm, menos inventario preso). Switch reduz o whipsaw do trend sem matar o upside.","evidence":"STRATEGY-farm-funnel.md:53-61; backtest-farm-funnel.js (GP.trendSwitch / SC()/tfScale)."},{"edge":"%-sizing (reinvestir lucro) = motor do exponencial — SO com EV+ liquido validado","magnitude":"Condicional, nao medido isolado: alavanca de escala 3→10 = aumento de sizing sobre borda validada (STRATEGY-3BTC-assessment.md:37-41); farm-funnel.md observa 'dobrar capital ~dobra a taxa (ate teto de liquidez/lotes)'. NAO ativar sem edge EV+ liquido por backtest/paper.","evidence":"STRATEGY-3BTC-assessment.md:37-41; farm-funnel-1h-macro500.md leitura:65."}],"backtestable":["backtest.js: long-only spot, klines 1h REAIS da Binance mainnet (HOSTS api.binance.com/data-api.binance.vision/api.binance.us, paginado 1000, cache em backtest-data/ gitignored), ~1 ano, multi-simbolo (default BTC/ETH/BNB/SOL). Flags: --days --interval --symbols --end --calibrate --compareRegime.","Indicadores Wilder self-contained (backtest.js:83-153): RSI(14), ATR(14), DMI completo ADX+pDI/mDI(14), SMA(qualquer), vol realizada anualizada. Sem libs externas (so built-ins Node).","Engine sem lookahead: execucao no OPEN do candle SEGUINTE ao sinal (backtest.js:161-163); net de fee 0,1%/lado nos 2 lados; metricas: netReturn, nTrades, winRate, avgTrade, maxDD, Sharpe anualizado (backtest.js:170-175).","Estrategias prontas: meanReversion(RSI lo/hi), trendFollow(SMA fast/slow), longFlat(SMA200), gatedMeanReversion (RSI gateada por close>SMA200 = modelo da id2 viva). Adicionar estrategia = passar um signalFn(i,inPos)→'BUY'|'SELL'|null (backtest.js:156 — ponto de extensao citado em strategy-engine.md:46).","Regime classifier 3-estados (bear/trend/range/mixed) por ADX+SMA200, com V1 (regimeWindow3:216) e V2 com HISTERESE anti-whipsaw (regimeWindowV2:233; bandas entrada/saida 0.60/0.45, 25/22, 20/23) — mesma logica replicada por-barra em backtest-farm-funnel.js regimeSeries:162.","Walk-forward OUT-OF-SAMPLE: janelas de 30d, regime ex-ante (janela anterior) escolhe a estrategia (bear→caixa/trend→trend/range-mixed→MR); agrega total composto + avg/janela + win% + flips; agregado cross-simbolo (edge vs sorte) — backtest.js:253-278,412-432.","backtest-farm-funnel.js: engine de LOTES (grid no-loss) + funil pra BTC — o backtest.js all-in/all-out NAO serve pra isso. Mede equity TOTAL (caixa + inventario marcado-a-mercado + BTC acumulado), inventario preso no fim, deployedPeak, exposicao, %bear, maxDD — separa farm real de lucro contabil ilusorio (backtest-farm-funnel.js:185-248).","3 regimes de ciclo pre-definidos no farm-funnel (PERIODS:58-62): 'recente ~365d', 'bull 2023-24' (180d end 2024-04-01), 'bear 2022' (365d end 2023-01-01). 8 alts default. Engine 'full' (gridTrendFunnel:262) coordena farm+trend+funil fiel ao runtime (trend sai no death cross = corta no prejuizo; farm pausa em trend/bear).","Knobs do farm-funnel: --capital --lot --maxlots --step --profit --rsibuy --macrosma --macroslope --trendlot --trendadx --switch --full --interval --tfscale (escala periodos por timeframe). Reproducao documentada em STRATEGY-farm-funnel.md:100-106.","Paper/Shadow Engine (NAO e backtest, mas valida ao vivo sob HALT): broker VIRTUAL roteado por prefixo [PAPER] no name → fill ao MINI_TICKER mainnet REAL + fee real (computeNet) + slippage (PAPER_SLIPPAGE_BPS), grava em paperOrders/paperPositions sem tocar Binance. GET /analysis/paper; paperReviewJob notifica nos marcos 5/15/30/60/120 round-trips — tradeux-strategy-engine.md:19-22,50.","LIMITES do harness: (a) timeframe minimo testado e 1m mas o cache 1m so existe pra BTCUSDT (60d); estrategias live id2/id3 usam RSI 1m que o backtest 1h NAO replica exatamente (backtest.js:337 caveat). (b) Sem modelagem de book/profundidade/partial-fills/slippage (so fee fixo; o farm-funnel assume fill ao open/close). (c) Futures (backtest-futures-trend.js) ja existe com funding 8h real, mas futures esta FORA DE ESCOPO e foi refutado. (d) NAO modela impacto de mercado nem MIN_NOTIONAL/stepSize reais (a frag. de calcQty/-1013 so aparece ao vivo)."]}

Voce e CETICO ADVERSARIAL. Tente REFUTAR esta alavanca (default REFUTED se incerto). Ancore em: spot-only, ~$149 real, fee 0,1%, B&H dificil de bater em bruto, edge=risco-ajustado, e os ja-refutados (nao deixe re-entrar um refutado disfarcado).

ALAVANCA (angulo cross-symbol):
{"lever":"Granularidade 15m no Farm em vez de mais pares (mesmo capital, mais round-trips no-loss limpos)","mechanism":"O caminho honesto pra AUMENTAR a contagem de oportunidades no-loss sem fragmentar os $149 nem adicionar correlacao/concentracao e baixar o timeframe do Farm de 1h pra 15m nos MESMOS pares limpos. Comparando os dois relatorios reais (recente/lateral, o regime atual): 1h farm-so = $65,34 realiz. agregado, +0,00075 BTC/ano, eqRet -3,54%, $399,56 preso; 15m farm-so = $106,61 realiz. (+63%), +0,00120 BTC/ano (+60%), eqRet -1,01% (MELHOR) e inventario preso CAI pra $242,44. Granularidade menor = mais dips capturados e fechados (mais round-trips) E menos inventario preso (sai mais rapido no lucro), exatamente o efeito que adicionar pares NAO da. Isso e o mesmo achado do STRATEGY-farm-funnel ('15m bate o 1h em todos os regimes').","expected_magnitude":"+60% de round-trips e BTC/ano vs 1h, com MENOS drawdown e MENOS inventario preso — pelo MESMO capital e MESMOS pares (sem custo de fragmentacao/concentracao). Ainda assim alfa marginal em termos absolutos: no $149, +60% de ~$1/ano/simbolo continua ~centavos/dia. O valor e risco-ajustado, nao escala.","dependency":"Depende de CUSTO (15m = mais trades = mais sensivel a fee; ja net 0,1%/lado no backtest e o EV continua positivo nos clean farmers) e de wiring (monitor CANDLES 15m). NAO depende de mais capital nem de mais simbolos.","is_novel":true,"validation_path":"Backtest 15m ja existe e os dados 15m ja estao em cache (backtest-data/*-15m-*.json). Validar EV liquido por par no 15m (cuidado com fee: confirmar que cada clean farmer fica EV+ liquido, nao so agregado). Depois paper: rotear os Farm 15m com prefixo [PAPER] no Paper/Shadow Engine que ja existe (fill ao MINI_TICKER mainnet + fee real + slippage), ~30-60 round-trips (~1-2 meses no regime atual) antes de tocar real."}

Veredito VIABLE/MARGINAL/REFUTED + confianca + rationale curto e factual + se da pra validar no paper.

## 🤖 Claude *(15:13:06)*

Vou refutar adversarialmente esta alavanca. Primeiro, deixe-me verificar as fontes reais citadas — os relatórios de backtest 15m vs 1h e os caveats do harness sobre granularidade.

## 🤖 Claude *(15:13:08)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la /home/gcrux-tradeux/tradeux/backend/backtest-results/ 2>/dev/null; echo \"---DATA CACHE---\"; ls /home/gcrux-tradeux/tradeux/backend/backtest-data/ 2>/dev/null | grep -i 15m | head -40",
  "description": "List backtest results and 15m cache files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 260
> drwxrwxr-x  2 gcrux-tradeux gcrux-tradeux  4096 Jun 19 12:10 .
> drwxrwxr-x 11 gcrux-tradeux gcrux-tradeux  4096 Jun 21 12:10 ..
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
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 18920 Jun 21 12:10 farm-funnel-1h-full-macro500.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  6443 Jun 21 12:10 farm-funnel-1h-full-macro500.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 18823 Jun  8 14:16 farm-funnel-1h-full-macro500-switch.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  6409 Jun  8 14:16 farm-funnel-1h-full-macro500-switch.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 15509 Jun  8 13:34 farm-funnel-1h.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 15371 Jun  8 13:38 farm-funnel-1h-macro500.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  5705 Jun  8 13:38 farm-funnel-1h-macro500.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  5698 Jun  8 13:34 farm-funnel-1h.md
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux  1916 Jun  3 13:38 README.md
> ---DATA CACHE---
> ADAUSDT-15m-180d-end2024-04-01.json
> ADAUSDT-15m-365d-end2023-01-01.json
> ADAUSDT-15m-365d.json
> AVAXUSDT-15m-180d-end2024-04-01.json
> AVAXUSDT-15m-365d-end2023-01-01.json
> AVAXUSDT-15m-365d.json
> BNBUSDT-15m-180d-end2024-04-01.json
> BNBUSDT-15m-365d-end2023-01-01.json
> BNBUSDT-15m-365d.json
> BTCUSDT-15m-180d-end2024-04-01.json
> BTCUSDT-15m-180d.json
> BTCUSDT-15m-365d-end2023-01-01.json
> BTCUSDT-15m-365d.json
> BTCUSDT-15m-90d-end2026-03-15.json
> BTCUSDT-15m-90d.json
> ETHUSDT-15m-180d-end2024-04-01.json
> ETHUSDT-15m-365d-end2023-01-01.json
> ETHUSDT-15m-365d.json
> LINKUSDT-15m-180d-end2024-04-01.json
> LINKUSDT-15m-365d-end2023-01-01.json
> LINKUSDT-15m-365d.json
> LTCUSDT-15m-180d-end2024-04-01.json
> LTCUSDT-15m-365d-end2023-01-01.json
> LTCUSDT-15m-365d.json
> SOLUSDT-15m-180d-end2024-04-01.json
> SOLUSDT-15m-365d-end2023-01-01.json
> SOLUSDT-15m-365d.json
> XRPUSDT-15m-180d-end2024-04-01.json
> XRPUSDT-15m-365d-end2023-01-01.json
> XRPUSDT-15m-365d.json
> ```

## 🤖 Claude *(15:13:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"15m\\|15 min\\|inventario preso\\|242,44\\|242.44\\|106,61\\|106.61\\|65,34\\|65.34\" /home/gcrux-tradeux/tradeux/docs/STRATEGY-farm-funnel.md 2>/dev/null | head -40",
  "description": "Find 15m vs 1h farm comparison in strategy doc"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrux-tradeux/tradeux/docs/STRATEGY-farm-funnel.md:56:**Config final recomendada (Farm + Trend + Switch, 15m):** recente **−5,5%** · bull **+14,4%** · bear **−0,4%**.
> /home/gcrux-tradeux/tradeux/docs/STRATEGY-farm-funnel.md:57:O 15m bate o 1h em todos os regimes (granularidade menor = mais farm, menos inventário preso).
> /home/gcrux-tradeux/tradeux/docs/STRATEGY-farm-funnel.md:61:(15m, talvez 5m) é melhor pro farm.
> /home/gcrux-tradeux/tradeux/docs/STRATEGY-farm-funnel.md:71:- **Timeframe**: farm em 15m (ou 5m); regime/trend macro em 1h (como hoje). Períodos de SMA escalam com o timeframe.
> /home/gcrux-tradeux/tradeux/docs/STRATEGY-farm-funnel.md:105:node scripts/backtest-farm-funnel.js --full --switch --interval=15m --tfscale=4 --macrosma=2000 --macroslope=960  # config final
> ```

## 🤖 Claude *(15:13:14)*

Os dados batem com a alavanca. Vou ler os dois relatórios reais — 15m macro e 1h macro500 — para confirmar os números agregados E, criticamente, checar o EV líquido POR PAR (não só agregado), além do caveat do harness sobre 1m/15m não bater o live.

## 🤖 Claude *(15:13:15)*


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

## 🤖 Claude *(15:13:16)*


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

## 🤖 Claude *(15:13:24)*

Agora tenho os dados POR PAR dos dois relatórios. Vou fazer a verificação adversarial crucial: o EV líquido por par no 15m. A alavanca admite que precisa "confirmar que cada clean farmer fica EV+ líquido, não só agregado". Deixe-me analisar par a par.

Observações críticas dos dados (período "recente", que é o regime atual citado):

**15m por par** — todos os 8 pares têm BTC acumulado POSITIVO e lucro realizado POSITIVO. Os "clean farmers" (inventário=0 no fim): BNB +0.52%, ETH +0.30%, ADA +0.29%, LTC +2.08% retorno equity. Os com inventário preso: SOL -3.95%, XRP -3.53%, LINK -2.64%, AVAX -1.17%.

**1h por par** — os clean farmers: BNB +0.25%, ETH +0.62%, ADA 0.00%, LTC 0.00%, AVAX 0.00%. Com inventário preso: SOL -13.14%, XRP -4.69%, LINK -11.39%.

Deixe-me confirmar o caveat do harness sobre granularidade fina e verificar se há algo no script sobre slippage/MIN_NOTIONAL no 15m.

## 🤖 Claude *(15:13:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"1m\\|15m\\|slippage\\|MIN_NOTIONAL\\|stepSize\\|partial\\|book\\|profundidade\\|impacto\\|caveat\\|337\" /home/gcrux-tradeux/tradeux/backend/scripts/backtest.js 2>/dev/null | head -20; echo \"===FARM-FUNNEL SCRIPT===\"; grep -n \"FEE\\|minProfit\\|0.006\\|0.012\\|slippage\\|MIN_NOTIONAL\\|lote\\|lot\\b\" /home/gcrux-tradeux/tradeux/backend/scripts/backtest-farm-funnel.js 2>/dev/null | head -20",
  "description": "Check harness caveats for fine granularity, slippage, min notional"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 29:const MS_PER = { '1m': 60e3, '5m': 5 * 60e3, '15m': 15 * 60e3, '30m': 30 * 60e3, '1h': 3600e3, '4h': 4 * 3600e3, '1d': 24 * 3600e3 };
> 337:  console.log(`no agregado, SEM piorar materialmente o outro, NAS DUAS janelas (bear+bull). Caveat: aqui é ${INTERVAL}; a id2/id3 ao vivo usa RSI 1m.`);
> ===FARM-FUNNEL SCRIPT===
> 17: *      [--capital=1000] [--lot=100] [--maxlots=8] [--step=0.015] [--profit=0.006] [--rsibuy=35]
> 28:const FEE = 0.001;                                    // 0.1%/lado (taker)
> 41:  lotUSDT: +args.lot || 100,         // tamanho de cada compra
> 42:  maxLots: +args.maxlots || 8,       // teto de lotes abertos (limita inventário/exposição)
> 44:  minProfit: +args.profit || 0.006,  // lucro líquido alvo por lote (0.6%, já acima do round-trip de fee)
> 48:  trendLot: +args.trendlot || 500,    // tamanho da posição de trend (SMA50/200) por entrada
> 201:    // 1) VENDAS no-loss: realiza cada lote que atingiu o lucro líquido alvo (nunca vende no prejuízo)
> 203:      const lot = lots[k];
> 204:      const sellVal = lot.qty * px * (1 - FEE);
> 205:      if (sellVal >= lot.spent * (1 + gp.minProfit)) {
> 206:        cash += lot.spent;                       // principal volta pro caixa de trabalho
> 207:        const profit = sellVal - lot.spent;      // lucro líquido
> 222:      const qty = gp.lotUSDT * (1 - FEE) / px;   // fee na compra
> 282:      const val = trendPos.qty * px * (1 - FEE); cash += val;
> 291:      if (spend >= gp.lotUSDT) { trendPos = { qty: spend * (1 - FEE) / px, spent: spend }; cash -= spend; }
> 296:      const lot = lots[k]; const sv = lot.qty * px * (1 - FEE);
> 297:      if (sv >= lot.spent * (1 + gp.minProfit)) {
> 298:        cash += lot.spent; const p = sv - lot.spent; farmRealized += p;
> 308:      lots.push({ qty: gp.lotUSDT * (1 - FEE) / px, spent: gp.lotUSDT, price: px }); cash -= gp.lotUSDT; nFarmBuys++;
> 345:  lines.push(`> ${ALTS.length} alts · ${INTERVAL} · fee ${FEE * 100}%/lado · exec no open seguinte (sem lookahead).`);
> ```

## 🤖 Claude *(15:13:52)*

Confirmei os pontos-chave do harness e do script. Agora tenho tudo para o veredito adversarial.

A análise crítica que importa:

1. **EV+ por par confirmado no 15m**: no relatório 15m "recente", os 8 pares têm lucro realizado positivo E BTC acumulado positivo. O fee de 0,1%/lado já está embutido (FEE=0.001 nas linhas 204/205/222), e o no-loss vende a `spent*(1+0.006)` que é >> round-trip de 0,2%. Então a dependência de custo está coberta — o backtest com fee real continua EV+ por par. A alavanca passa no teste que ela mesma se impôs.

2. **15m domina 1h no MESMO capital/pares**: +63% lucro realizado ($106,61 vs $65,34), +60% BTC/ano, retorno equity MELHOR (-1,01% vs -3,54%), inventário preso CAI ($242 vs $399). E o efeito é mecanicamente honesto — granularidade fina captura mais dips e sai mais rápido no lucro, exatamente o que adicionar pares NÃO dá (pares fragmentam e correlacionam).

3. **Sem refutado disfarçado**: NÃO é frequência/scalp (refutado 5m/15m era MR all-in/all-out direcional, EV<0; aqui é grid no-loss vende-só-no-lucro, EV+ por par). NÃO é harvester (mecanismo diferente, vende inventário rastreado). É uma calibração de um edge JÁ validado (Farm no-loss), não um motor novo.

Onde a alavanca corretamente se auto-limita (e onde eu a freio):

- **Magnitude é centavos/dia no $149 real.** +60% de ~$1/ano/símbolo no capital de $8000 escala linearmente pra baixo: nos $149 reais (~1,9% do capital backtestado) são centavos/ano. A própria alavanca admite "alfa marginal, não escala". Isso impede VIABLE.
- **Caveats do harness não-modelados que MORDEM mais em 15m**: o backtest não modela slippage real, MIN_NOTIONAL/stepSize, nem partial-fills (caveats (b)/(d) do ledger). Mais round-trips = mais sensível a esses. O live buffer é cost*1.012, mas com lote de ~$25 (teto MAX_ORDER_NOTIONAL) o stepSize/MIN_NOTIONAL pode fragmentar (o -1013 só aparece ao vivo). E o caveat explícito da linha 337: live usa RSI 1m, backtest é por-intervalo.
- **Caminho de validação é limpo e honesto**: paper engine [PAPER] já existe, fill ao MINI_TICKER mainnet + fee real + slippage. É exatamente onde esse tipo de calibração de timeframe deve ser provado antes de tocar real.

Veredito: MARGINAL. O mecanismo é real, sobrevive ao teste de fee POR PAR (não só agregado), domina o 1h no mesmo capital/pares sem fragmentar, e NÃO é um refutado disfarçado. Mas é por construção alfa marginal (centavos no $149), o valor é risco-ajustado e não escala — e os caveats não-modelados (slippage/min-notional/RSI-1m) batem mais forte justamente porque há mais trades. Validável no paper de forma direta.

## 🤖 Claude *(15:14:04)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "lever": "Granularidade 15m no Farm em vez de mais pares (mesmo capital, mais round-trips no-loss limpos)",
  "verdict": "MARGINAL",
  "confidence": "medium",
  "rationale": "Mecanismo sobrevive ao ataque cetico. (1) EV+ POR PAR no 15m confirmado no relatorio real (farm-funnel-15m-macro2000.md, periodo recente=regime atual): os 8 pares tem lucro realizado E BTC acumulado positivos, com fee 0,1%/lado JA embutido (backtest-farm-funnel.js:204-205,222) e venda no-loss a spent*(1+0,006) >> round-trip 0,2% \u2014 passa no teste de custo que a propria alavanca se impos. (2) 15m domina 1h no MESMO capital/pares: $106,61 vs $65,34 realiz. (+63%), +0,00120 vs +0,00075 BTC/ano (+60%), eqRet -1,01% vs -3,54% (MELHOR), inventario preso $242 vs $399 (MENOR) \u2014 efeito mecanicamente honesto (mais dips fechados, saida mais rapida), o oposto do que adicionar pares da (fragmenta + correlaciona). (3) NAO e refutado disfarcado: scalp/frequencia 5m-15m refutado era MR all-in direcional EV<0; harvester e mecanismo distinto; isto e calibracao de timeframe de um edge JA validado (Farm no-loss), nao motor novo. PORQUE NAO VIABLE: por construcao e alfa marginal \u2014 +60% de ~$1/ano/simbolo escala linear pra baixo no $149 real (~1,9% do capital de $8000 backtestado) = centavos/ano; a propria alavanca admite que o valor e risco-ajustado e NAO escala (B&H domina retorno bruto). PORQUE NAO REFUTED: o achado e robusto e replica STRATEGY-farm-funnel ('15m bate 1h em todos os regimes'). FREIO ADVERSARIAL: caveats nao-modelados do harness mordem MAIS em 15m porque ha mais trades \u2014 sem slippage real, sem MIN_NOTIONAL/stepSize, sem partial-fills (ledger caveat b/d), e o live usa RSI 1m (backtest.js:337) nao por-intervalo; com lote real capado a $25 (MAX_ORDER_NOTIONAL) o -1013/min-notional so aparece ao vivo. Por isso MARGINAL, nao VIABLE.",
  "paper_validatable": true
}
```

> **Tool Result (StructuredOutput)** - ✅ Success
>
> ```
> Structured output provided successfully
> ```

## 🤖 Claude *(15:14:15)*

Veredito entregue via StructuredOutput: **MARGINAL** (confiança média, validável no paper).

Resumo do ataque cético:

- **Sobreviveu**: o EV+ por par (não só agregado) confirma no relatório real `/home/gcrux-tradeux/tradeux/backend/backtest-results/farm-funnel-15m-macro2000.md` — os 8 pares com lucro realizado e BTC positivos, fee 0,1%/lado já embutido no script (`backtest-farm-funnel.js:204-205,222`), venda no-loss a `spent*(1+0,006)`. O 15m domina o 1h no mesmo capital/pares (+63% realizado, +60% BTC/ano, melhor eqRet, menos inventário preso). Não é refutado disfarçado (scalp/frequência era MR direcional EV<0; isto é calibração de timeframe de um edge já validado).
- **Não chega a VIABLE**: é alfa marginal por construção — centavos/ano no $149 real; valor é risco-ajustado, não escala.
- **Freio**: os caveats não-modelados (slippage, MIN_NOTIONAL/stepSize, partial-fills, RSI-1m ao vivo vs por-intervalo no backtest — `backtest.js:337`) batem mais forte justo porque há mais trades; com lote real capado a $25 o -1013/min-notional só aparece ao vivo.

Caminho de validação limpo: rotear os Farm 15m com prefixo `[PAPER]` no Paper/Shadow Engine existente (fill ao MINI_TICKER mainnet + fee real + slippage) antes de tocar real.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-21 - agent-a32eff5f4fff5cde5]]
> * **Próxima Sessão**: [[2026-06-21 - agent-a3feaf8b22443361a]]
%% --- TIMELINE END --- %%

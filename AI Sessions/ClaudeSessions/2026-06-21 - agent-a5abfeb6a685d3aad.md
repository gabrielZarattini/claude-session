# Session agent-a5abfeb6a685d3aad
**Date:** 2026-06-21 | **Session ID:** `agent-a5abfeb6a685d3aad`

---

## 👤 User *(15:21:11)*


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

ALAVANCA (angulo risk-adjusted):
{"lever":"Throttle de exposicao drawdown-aware (de-risk em saque/drawdown corrente, anti-martingale)","mechanism":"O sistema ja tem cap diario -5% (dailyCapJob) que e BINARIO: ou opera 100% ou HALTA. Falta o degrau intermediario CONTINUO. Alavanca: escalar a exposicao agregada por f(DD_corrente) — quando o equity-tradeable cai X% do pico rolante, reduzir o notional de novas compras proporcionalmente (ex.: -3% pico -> 70% size, -5% -> halt ja existente). E o oposto explicito do martingale (NUNCA aumentar size pra 'recuperar' — o Farm DCA hoje pode escalar inventario no bear, que e o pecado capital do no-loss). Mecanismo de composicao: protege o capital-semente que e o que efetivamente compoe. Em capital pequeno ($149) a assimetria geometrica e brutal — um -25% exige +33% pra voltar; cortar a cauda esquerda preserva a base composta. Complementa a alavanca 1 (vol-targeting reage ao MERCADO; este reage ao SEU P&L).","expected_magnitude":"HONESTO: ganho de retorno bruto ~zero ou levemente NEGATIVO num ciclo (de-risk as vezes corta uma recuperacao). O valor e 100% risco-ajustado e de SOBREVIVENCIA: reduz a probabilidade de ruina/halt-permanente e suaviza a equity-curve. Magnitude do maxDD: do -10% medio pra ~-6-7% no pior simbolo (LTC recente fez -19,3% maxDD — esse e o alvo). Ganho composto de ciclo: marginal em $ (+1 a +4 p.p.) mas alto em VARIANCIA reduzida (Sharpe sobe mais que o retorno). NAO e motor de crescimento; e seguro de continuidade — 'sobreviver pra compor' literal. Honestamente: o cap -5% ja captura ~70% desse beneficio; o degrau continuo e um refinamento, nao uma revolucao.","dependency":"Depende de CAPITAL (mais relevante quanto MENOR o capital — assimetria geometrica). NAO depende de edge novo nem de simbolos. Depende do baseline de equity ja existir (dailyCapJob ja calcula equity-tradeable excluindo Earn LD*). Custo: pode reduzir trades (menos fee), nunca aumenta. Risco de implementacao: e money-path/risco — exige o mesmo rigor do cap -5% (riskState single-source) e Claude NUNCA vira HALT.","is_novel":true,"validation_path":"BACKTEST: rodar gridFunnel com um multiplicador de exposicao f(DD) na engine (equity-curve ja rastreada, backtest-farm-funnel.js:230-231) e comparar maxDD/retorno vs sem-throttle, nos 3 regimes OOS. Quantificar quanto o degrau-continuo adiciona ALEM do cap -5% binario ja existente (o teste critico — se o delta for <1 p.p., NAO vale a complexidade money-path). Se o delta justificar: paper 30-60 RT. So entao backend sob QA+TL, espelhando riskState. ~1 dia de backtest + janela de paper. Ceticismo embutido: provavel que o cap -5% ja seja suficiente e este vire NO-GO — reportar isso honestamente conta como validacao."}

Veredito VIABLE/MARGINAL/REFUTED + confianca + rationale curto e factual + se da pra validar no paper.

## 🤖 Claude *(15:21:16)*

Vou investigar a alavanca ancorando nas fontes reais do harness antes de julgar. Preciso verificar: (1) o que o dailyCapJob/riskState realmente faz hoje (cap -5% binário), (2) se o engine de backtest farm-funnel já rastreia equity-curve e maxDD por símbolo, (3) os números de maxDD do farm-só nos relatórios.

## 🤖 Claude *(15:21:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la /home/gcrux-tradeux/tradeux/backend/scripts/ 2>/dev/null | grep -i backtest; echo \"---RESULTS---\"; ls -la /home/gcrux-tradeux/tradeux/backend/backtest-results/ 2>/dev/null",
  "description": "List backtest scripts and result files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux 25302 Jun  8 14:24 backtest-farm-funnel.js
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux 16313 Jun  8 23:25 backtest-futures-trend.js
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux 31008 Jun  3 21:24 backtest.js
> ---RESULTS---
> total 288
> drwxrwxr-x  2 gcrux-tradeux gcrux-tradeux  4096 Jun 21 12:14 .
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
> -rw-rw-r--  1 ubuntu        ubuntu        19032 Jun 21 12:15 farm-funnel-1h-full.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 18930 Jun  8 14:04 farm-funnel-1h-full-macro500-adx15.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  6439 Jun  8 14:04 farm-funnel-1h-full-macro500-adx15.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 18966 Jun  8 14:03 farm-funnel-1h-full-macro500-adx22.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  6416 Jun  8 14:03 farm-funnel-1h-full-macro500-adx22.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 18920 Jun 21 12:10 farm-funnel-1h-full-macro500.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  6443 Jun 21 12:10 farm-funnel-1h-full-macro500.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 18823 Jun  8 14:16 farm-funnel-1h-full-macro500-switch.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  6409 Jun  8 14:16 farm-funnel-1h-full-macro500-switch.md
> -rw-rw-r--  1 ubuntu        ubuntu         6421 Jun 21 12:15 farm-funnel-1h-full.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 15509 Jun  8 13:34 farm-funnel-1h.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 15371 Jun  8 13:38 farm-funnel-1h-macro500.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  5705 Jun  8 13:38 farm-funnel-1h-macro500.md
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  5698 Jun  8 13:34 farm-funnel-1h.md
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux  1916 Jun  3 13:38 README.md
> ```

## 🤖 Claude *(15:21:19)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"dailyCap\\|riskState\\|isHalted\\|drawdown\\|DAILY_CAP\\|equity-tradeable\\|equityTradeable\" /home/gcrux-tradeux/tradeux/backend/src 2>/dev/null | head -40",
  "description": "Find dailyCap and riskState implementation"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:3:// === riskState — FONTE ÚNICA DE VERDADE do kill-switch (HALT) ===
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:5:// O guard (utils/exchange.js) chama isHalted() POR ORDEM (HALT QUENTE). Fontes EMPILHÁVEIS (basta UMA p/ travar tudo):
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:14://   daily-cap → disparado pelo dailyCapJob no drawdown de equity do dia. Persistido; AUTO-EXPIRA na virada UTC.
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:17:// disco ilegível → floor LIGADO (trava); isHalted() lançar → o guard lança = ordem bloqueada (direção segura).
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:36:let dailyCap = { on: false, reason: null, since: null, day: null };
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:47:        fs.writeFileSync(STATE_FILE, JSON.stringify({ floor, manual, dailyCap }), 'utf8');
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:49:        logger('system', `[riskState] falha ao persistir ${STATE_FILE}: ${e.message}`);
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:54:// 1º flip); ausente → mantém a semente. manual re-arma como estava; dailyCap só se for do MESMO dia UTC.
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:61:        if (raw && raw.dailyCap && typeof raw.dailyCap.on === 'boolean') {
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:62:            if (raw.dailyCap.on && raw.dailyCap.day === dayKeyUTC()) dailyCap = raw.dailyCap;
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:63:            else dailyCap = { on: false, reason: null, since: null, day: null }; // dia diferente → expira
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:67:        logger('system', `[riskState] estado em disco ilegível (${e.message}) — FAIL-CLOSED (floor LIGADO).`);
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:70:        dailyCap = { on: false, reason: null, since: null, day: null };
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:74:// HALT efetivo: qualquer fonte ligada trava. dailyCap só conta no DIA em que foi armado.
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:75:function isHalted() {
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:76:    return ENV_HALT_HARD || floor.on || manual.on || (dailyCap.on && dailyCap.day === dayKeyUTC());
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:83:    const capActive = dailyCap.on && dailyCap.day === today;
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:94:    else if (capActive) { source = 'daily-cap'; reason = dailyCap.reason || 'daily-loss-cap'; since = dailyCap.since; }
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:97:        halted: isHalted(),
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:101:        dailyCap: { ...dailyCap, active: capActive },
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:115:    logger('system', `[riskState] FLOOR ${on ? 'LIGADO (trava)' : 'DESLIGADO (trading liberado)'}${on && reason ? ` (${reason})` : ''}.`);
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:127:        logger('system', `[riskState] manual HALT ${on ? 'LIGADO' : 'desligado'}${on && reason ? ` (${reason})` : ''}.`);
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:133:            if (dailyCap.on && dailyCap.day === today) return false; // já armado hoje → não re-notifica
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:134:            dailyCap = { on: true, reason: reason || 'daily-loss-cap', since: new Date().toISOString(), day: today };
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:136:            logger('system', `[riskState] daily-cap HALT ARMADO (${dailyCap.reason}).`);
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:141:    throw new Error(`[riskState] setHalt: source inválida '${source}' (use 'manual' ou 'daily-cap').`);
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:146:    if (!dailyCap.on) return false;
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:147:    dailyCap = { on: false, reason: null, since: null, day: null };
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:149:    logger('system', `[riskState] daily-cap HALT limpo (re-armado p/ o dia).`);
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:153:// Dia em que o daily-cap está armado (null se não armado) — o dailyCapJob usa p/ saber se já disparou hoje.
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:155:    return dailyCap.on ? dailyCap.day : null;
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:160:logger('system', `[riskState] inicializado — env-hard=${ENV_HALT_HARD} · floor=${floor.on} · manual=${manual.on} · daily-cap=${dailyCap.on}${dailyCap.on ? ` (${dailyCap.day})` : ''} · halted=${isHalted()}.`);
> /home/gcrux-tradeux/tradeux/backend/src/riskState.js:162:module.exports = { dayKeyUTC, isHalted, getState, setFloor, setHalt, clearDailyCap, getDailyCapDay };
> /home/gcrux-tradeux/tradeux/backend/src/server.js:15:const dailyCapJob = require('./dailyCapJob');
> /home/gcrux-tradeux/tradeux/backend/src/server.js:77:    // Daily Loss Cap job: circuit-breaker de perda diária (-5% por drawdown de equity). Arma o HALT QUENTE
> /home/gcrux-tradeux/tradeux/backend/src/server.js:78:    // (riskState fonte 'daily-cap') quando o equity do dia cai além do teto. Fail-safe a preço frio (não
> /home/gcrux-tradeux/tradeux/backend/src/server.js:81:    dailyCapJob.start();
> /home/gcrux-tradeux/tradeux/backend/src/dailyCapJob.js:3:// === dailyCapJob — CIRCUIT-BREAKER de perda diária (-5%) por DRAWDOWN DE EQUITY ===
> /home/gcrux-tradeux/tradeux/backend/src/dailyCapJob.js:7:// (default 5%), ARMA o HALT via riskState (fonte 'daily-cap') → o guard do exchange.js passa a bloquear
> /home/gcrux-tradeux/tradeux/backend/src/dailyCapJob.js:14:// Por que drawdown de equity e NÃO o cash-flow (sellNet-buyNet do dailyProfitJob): cash-flow falsa-dispara
> ```

## 🤖 Claude *(15:21:22)*

Let me read the core implementation files to ground the verdict.

## 🤖 Claude *(15:21:23)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/src/dailyCapJob.js"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	'use strict';
> 2	
> 3	// === dailyCapJob — CIRCUIT-BREAKER de perda diária (-5%) por DRAWDOWN DE EQUITY ===
> 4	//
> 5	// Tira um snapshot do equity TOTAL da conta (USDT livre + valor de mercado de TODAS as posições) na
> 6	// virada de dia UTC e, a cada ciclo, compara o equity atual com esse snapshot. Se o equity cair >= o teto
> 7	// (default 5%), ARMA o HALT via riskState (fonte 'daily-cap') → o guard do exchange.js passa a bloquear
> 8	// QUALQUER ordem (BUY/SELL/OCO) até a virada de dia UTC OU um reset manual do operador.
> 9	//
> 10	// ⚠️ ESCOPO = BLOQUEIA TUDO (decisão do dono): durante um halt por -5%, venda PROTETIVA (death cross/stop)
> 11	// TAMBÉM é bloqueada. Não há de-risking automático sob o cap — o operador precisa intervir manualmente
> 12	// (vender na mão) ou reabrir via POST /system/halt {on:false} / POST /system/daily-cap/reset.
> 13	//
> 14	// Por que drawdown de equity e NÃO o cash-flow (sellNet-buyNet do dailyProfitJob): cash-flow falsa-dispara
> 15	// em dia de ACUMULAÇÃO (comprar sem vender conta como "perda" sem ser). Equity mark-to-market é robusto.
> 16	//
> 17	// FAIL-SAFE (segurança money-path): se o equity não puder ser AVALIADO (preço frio/ausente de alguma moeda
> 18	// com saldo), NÃO dispara e NÃO faz snapshot — espera o MINI_TICKER esquentar. Nunca trava no escuro.
> 19	
> 20	const beholder = require('./beholder');
> 21	const settingsRepository = require('./repositories/settingsRepository');
> 22	const riskState = require('./riskState');
> 23	const logger = require('./utils/logger');
> 24	const fs = require('fs');
> 25	const path = require('path');
> 26	
> 27	const ENABLED = (process.env.DAILY_CAP_ENABLED || 'true') === 'true';
> 28	const _pct = parseFloat(process.env.DAILY_LOSS_CAP_PCT || '0.05');
> 29	const CAP_PCT = Number.isFinite(_pct) && _pct > 0 && _pct < 1 ? _pct : 0.05; // fração (0.05 = -5%)
> 30	const _ms = parseInt(process.env.DAILY_CAP_CHECK_MS || '60000', 10);
> 31	const CHECK_MS = Number.isFinite(_ms) && _ms >= 15000 ? _ms : 60000; // piso 15s
> 32	const _coldMs = parseInt(process.env.DAILY_CAP_COLD_ALERT_MS || '900000', 10);
> 33	const COLD_ALERT_MS = Number.isFinite(_coldMs) && _coldMs > 0 ? _coldMs : 900000; // 15min: alarme anti-silêncio
> 34	
> 35	const QUOTE = 'USDT';
> 36	const STABLES = new Set(['USDT', 'USDC', 'BUSD', 'FDUSD', 'TUSD', 'DAI']); // valem ~$1 (a par com USDT)
> 37	// Assets que o operador isenta do equity (sem par <coin>USDT que esquente: Earn/Locked 'LD*', leveraged tokens,
> 38	// dust de moeda BTC-only). Sem isenção, um asset assim deixaria o cap em fail-safe PERMANENTE. CSV, default vazio.
> 39	const IGNORE_ASSETS = new Set((process.env.DAILY_CAP_IGNORE_ASSETS || '').split(',').map(s => s.trim().toUpperCase()).filter(Boolean));
> 40	// Bases que o sistema ACOMPANHA (par <base>USDT com ticker quente). Earn dessas (LD<base>) sem preço momentâneo =
> 41	// ativo REAL temporariamente frio → fail-safe (espera); LD de qualquer OUTRA base = dust de Earn sem par → ignora.
> 42	// Deriva do mesmo REGIME_SYMBOLS do regimeJob/cockpit. Nasceu do incidente do auto-subscribe (LTC spot → LDLTC).
> 43	const TRACKED_BASES = new Set(
> 44	    (process.env.REGIME_SYMBOLS || 'BTCUSDT,LTCUSDT,BNBUSDT,ADAUSDT')
> 45	        .split(',').map(s => s.trim().toUpperCase().replace(/USDT$/, '')).filter(Boolean)
> 46	);
> 47	const SNAP_FILE = path.resolve(__dirname, '..', 'logs', 'daily_cap_snapshot.json');
> 48	
> 49	let timer = null;
> 50	let running = false;
> 51	let SNAP = null;          // { day:'YYYY-MM-DD', equity:Number, at:ISO } — baseline do dia (persistido)
> 52	let LAST = null;          // último cálculo de equity p/ observabilidade
> 53	let AT = null;            // ts do último ciclo
> 54	let COLD_LOGGED = false;  // p/ logar a indisponibilidade 1x por episódio (anti-spam)
> 55	let COLD_SINCE = null;    // ts do início do episódio de indisponibilidade (p/ o alarme anti-silêncio)
> 56	let COLD_ALERTED = false; // alarme de proteção-inativa já enviado neste episódio
> 57	
> 58	function loadSnap() {
> 59	    try {
> 60	        if (fs.existsSync(SNAP_FILE)) {
> 61	            const raw = JSON.parse(fs.readFileSync(SNAP_FILE, 'utf8'));
> 62	            if (raw && typeof raw.equity === 'number' && raw.day) SNAP = raw;
> 63	        }
> 64	    } catch (e) {
> 65	        logger('system', `[dailyCap] snapshot em disco ilegível (${e.message}) — recomeçando baseline.`);
> 66	        SNAP = null;
> 67	    }
> 68	}
> 69	
> 70	function saveSnap() {
> 71	    try {
> 72	        const dir = path.dirname(SNAP_FILE);
> 73	        if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
> 74	        fs.writeFileSync(SNAP_FILE, JSON.stringify(SNAP), 'utf8');
> 75	    } catch (e) {
> 76	        logger('system', `[dailyCap] falha ao persistir ${SNAP_FILE}: ${e.message}`);
> 77	    }
> 78	}
> 79	
> 80	// Preço de uma moeda em USDT via MINI_TICKER (mesmo feed que o funnelJob/refPrice usam; sem rede). null se frio.
> 81	function priceOf(coin) {
> 82	    try {
> 83	        const mt = beholder.getMemory(`${coin}${QUOTE}`, 'MINI_TICKER');
> 84	        const p = mt && (mt.close ?? mt.current ?? mt.c ?? mt.lastPrice);
> 85	        const n = parseFloat(p);
> 86	        return Number.isFinite(n) && n > 0 ? n : null;
> 87	    } catch (e) { return null; }
> 88	}
> 89	
> 90	// Equity TOTAL em USDT: USDT/stables a par + (available+onOrder) de cada moeda × preço. Se ALGUMA moeda com
> 91	// saldo positivo estiver com preço frio, marca valued:false (fail-safe — o chamador NÃO dispara nem snapshota).
> 92	// Retorna { valued, equity, usdtFree, cold:[...], settings } ou { valued:false, error } se saldo indisponível.
> 93	async function computeEquity() {
> 94	    const settings = await settingsRepository.getDefaultSettings(); // já vem DESCRIPTOGRAFADO (incl. id)
> 95	    if (!settings || !settings.id) return { valued: false, error: 'sem settings default' };
> 96	    const exchange = require('./utils/exchange')(settings);
> 97	    const bal = await exchange.balance();
> 98	    if (!bal) return { valued: false, error: 'saldo indisponível', settings };
> 99	
> 100	    let equity = 0;
> 101	    let usdtFree = 0;
> 102	    const cold = [];
> 103	    const ignored = [];
> 104	    for (const [coin, b] of Object.entries(bal)) {
> 105	        const qty = (parseFloat(b.available) || 0) + (parseFloat(b.onOrder) || 0);
> 106	        if (qty <= 0) continue;
> 107	        if (coin === QUOTE) { usdtFree = parseFloat(b.available) || 0; equity += qty; continue; }
> 108	        if (STABLES.has(coin)) { equity += qty; continue; }        // outras stables ~ $1
> 109	        if (IGNORE_ASSETS.has(coin)) { ignored.push(coin); continue; } // isento explícito pelo operador
> 110	        const px = priceOf(coin);
> 111	        if (px == null) {
> 112	            // 'LD'+ativo = wrapper do Binance Simple Earn (LDLTC = LTC em Earn, LDUSDC = USDC em Earn...). Tem valor
> 113	            // REAL e resgatável → marca a mercado pelo ativo SUBJACENTE (strip 'LD'). Sem isto, um saldo que a Binance
> 114	            // AUTO-SUBSCREVE no Earn some do equity e dispara o cap por falso drawdown (incidente 2026-06-20: LTC→LDLTC,
> 115	            // equity $148→$109 → HALT falso). length>3 preserva spot real como LDO.
> 116	            if (coin.startsWith('LD') && coin.length > 3) {
> 117	                const under = coin.slice(2);                            // LDLTC -> LTC, LDUSDC -> USDC
> 118	                if (STABLES.has(under)) { equity += qty; continue; }    // Earn de stable ~ $1
> 119	                const upx = priceOf(under);
> 120	                if (upx != null) { equity += qty * upx; continue; }     // Earn de cripto com preço → conta a mercado
> 121	                if (TRACKED_BASES.has(under)) { cold.push(coin); continue; } // Earn de ativo REAL frio → fail-safe
> 122	                ignored.push(coin); continue;                           // dust de Earn sem par → fora do equity, não bloqueia
> 123	            }
> 124	            cold.push(coin); continue;                              // preço frio REAL → fail-safe (não avalia)
> 125	        }
> 126	        equity += qty * px;
> 127	    }
> 128	    const valued = cold.length === 0;
> 129	    return { valued, equity, usdtFree, cold, ignored, settings };
> 130	}
> 131	
> 132	async function notify(settings, msg) {
> 133	    try { await require('./utils/telegram')(settings, msg); } catch (e) { /* best-effort */ }
> 134	}
> 135	
> 136	async function checkCap() {
> 137	    if (running) return;
> 138	    running = true;
> 139	    try {
> 140	        const today = riskState.dayKeyUTC();
> 141	        const eq = await computeEquity();
> 142	        AT = Date.now();
> 143	        LAST = { at: new Date(AT).toISOString(), valued: eq.valued, equity: eq.valued ? eq.equity : null, cold: eq.cold || null, ignored: eq.ignored || null, error: eq.error || null };
> 144	
> 145	        // 1) Rollover de dia UTC: re-arma a proteção (limpa o cap do dia anterior) e força re-baseline.
> 146	        if (SNAP && SNAP.day !== today) {
> 147	            riskState.clearDailyCap();
> 148	            const prev = SNAP;
> 149	            SNAP = null;
> 150	            logger('system', `[dailyCap] virada de dia UTC (${prev.day} → ${today}); cap re-armado, re-baseline.`);
> 151	            await notify(eq.settings, `🌅 [DAILY_CAP] Novo dia UTC. Cap de -${(CAP_PCT * 100).toFixed(0)}% re-armado para o novo dia.`);
> 152	        }
> 153	
> 154	        // 2) Fail-safe: equity não avaliável → não snapshota e não dispara (espera o preço esquentar).
> 155	        if (!eq.valued) {
> 156	            const why = eq.error || `preços frios: ${(eq.cold || []).join(', ')}`;
> 157	            if (!COLD_LOGGED) {
> 158	                COLD_LOGGED = true;
> 159	                COLD_SINCE = AT;
> 160	                logger('system', `[dailyCap] equity NÃO-avaliável (${why}) — cap NÃO avaliado neste ciclo (fail-safe).`);
> 161	            }
> 162	            // Alarme ANTI-SILÊNCIO: se a proteção ficar inavaliável por muito tempo (default 15min), AVISA o dono.
> 163	            // Sem isso o fail-safe poderia deixar o cap de -5% INATIVO em silêncio (ex.: asset sem par USDT). QA P1-A.
> 164	            if (!COLD_ALERTED && COLD_SINCE && (AT - COLD_SINCE) >= COLD_ALERT_MS) {
> 165	                COLD_ALERTED = true;
> 166	                const mins = Math.round((AT - COLD_SINCE) / 60000);
> 167	                logger('system', `[dailyCap] ⚠️ equity inavaliável há ~${mins}min — cap de -${(CAP_PCT * 100).toFixed(0)}% INATIVO (${why}).`);
> 168	                await notify(eq.settings, `⚠️ [DAILY_CAP] Proteção de -${(CAP_PCT * 100).toFixed(0)}% INATIVA há ~${mins}min: não consigo avaliar o equity (${why}). Verifique monitores/preços ou isente o asset via DAILY_CAP_IGNORE_ASSETS.`);
> 169	            }
> 170	            return;
> 171	        }
> 172	        if (COLD_LOGGED) { COLD_LOGGED = false; COLD_SINCE = null; COLD_ALERTED = false; logger('system', `[dailyCap] equity avaliável novamente ($${eq.equity.toFixed(2)}).`); }
> 173	
> 174	        // 3) Baseline do dia ausente (boot mid-day ou pós-rollover): snapshota AGORA e encerra o ciclo.
> 175	        if (!SNAP || SNAP.day !== today) {
> 176	            SNAP = { day: today, equity: eq.equity, at: new Date().toISOString() };
> 177	            saveSnap();
> 178	            logger('system', `[dailyCap] baseline do dia ${today} = $${eq.equity.toFixed(2)} (USDT livre $${eq.usdtFree.toFixed(2)}).`);
> 179	            return;
> 180	        }
> 181	
> 182	        // 4) Avalia o drawdown. Piso = baseline × (1 - CAP_PCT). Equity <= piso → ARMA o HALT (idempotente).
> 183	        const floor = SNAP.equity * (1 - CAP_PCT);
> 184	        if (eq.equity <= floor) {
> 185	            const ddPct = ((eq.equity / SNAP.equity) - 1) * 100;
> 186	            const reason = `daily-loss-cap -${(CAP_PCT * 100).toFixed(0)}% (equity $${eq.equity.toFixed(2)} <= piso $${floor.toFixed(2)}; baseline $${SNAP.equity.toFixed(2)}, dd ${ddPct.toFixed(2)}%)`;
> 187	            const tripped = riskState.setHalt(true, reason, 'daily-cap');
> 188	            if (tripped) {
> 189	                logger('system', `[dailyCap] 🛑 CAP DISPARADO — ${reason}. HALT ativo (bloqueia TODAS as ordens).`);
> 190	                await notify(eq.settings,
> 191	                    `🛑 [DAILY_CAP] Cap diário de -${(CAP_PCT * 100).toFixed(0)}% ATINGIDO!\n` +
> 192	                    `Equity $${eq.equity.toFixed(2)} (baseline $${SNAP.equity.toFixed(2)}, ${ddPct.toFixed(2)}%).\n` +
> 193	                    `🚫 HALT ativo: TODAS as ordens bloqueadas (inclusive venda protetiva). ` +
> 194	                    `Intervenção manual necessária — reabra via /system/halt ou aguarde a virada de dia UTC.`);
> 195	            }
> 196	        }
> 197	    } catch (err) {
> 198	        logger('system', `[dailyCap] erro no ciclo: ${err.message}`);
> 199	    } finally {
> 200	        running = false;
> 201	    }
> 202	}
> 203	
> 204	// Re-snapshot forçado (usado pelo reset do operador): re-baseline com o equity atual p/ não re-disparar
> 205	// contra um baseline velho logo após o reset. Não dispara nada. Retorna { ok, snapshot, reason }.
> 206	async function reSnapshot() {
> 207	    if (running) return { ok: false, reason: 'ciclo do cap em andamento — tente de novo em instantes', snapshot: SNAP };
> 208	    running = true; // serializa com checkCap (evita race na escrita de SNAP)
> 209	    try {
> 210	        const eq = await computeEquity();
> 211	        if (!eq.valued) return { ok: false, reason: eq.error || `preços frios: ${(eq.cold || []).join(', ')}`, snapshot: SNAP };
> 212	        SNAP = { day: riskState.dayKeyUTC(), equity: eq.equity, at: new Date().toISOString() };
> 213	        saveSnap();
> 214	        logger('system', `[dailyCap] re-baseline manual = $${eq.equity.toFixed(2)} (${SNAP.day}).`);
> 215	        return { ok: true, snapshot: SNAP };
> 216	    } catch (err) {
> 217	        return { ok: false, reason: err.message, snapshot: SNAP };
> 218	    } finally {
> 219	        running = false;
> 220	    }
> 221	}
> 222	
> 223	function start() {
> 224	    if (!ENABLED) { logger('system', '[dailyCap] DESABILITADO (DAILY_CAP_ENABLED=false).'); return; }
> 225	    if (timer) return; // idempotente
> 226	    loadSnap();
> 227	    checkCap(); // primeira passada no boot (provável fail-safe se MINI_TICKER ainda frio — esperado)
> 228	    timer = setInterval(checkCap, CHECK_MS);
> 229	    if (timer.unref) timer.unref();
> 230	    logger('system', `[dailyCap] iniciado — teto -${(CAP_PCT * 100).toFixed(0)}% sobre o equity do dia (intervalo ${CHECK_MS}ms).`);
> 231	}
> 232	
> 233	function stop() {
> 234	    if (timer) { clearInterval(timer); timer = null; }
> 235	    running = false;
> 236	}
> 237	
> 238	function getStatus() {
> 239	    const st = riskState.getState();
> 240	    return {
> 241	        enabled: ENABLED, capPct: CAP_PCT, checkMs: CHECK_MS,
> 242	        snapshot: SNAP, last: LAST,
> 243	        floor: SNAP ? SNAP.equity * (1 - CAP_PCT) : null,
> 244	        tripped: st.dailyCap, halted: st.halted, haltSource: st.source,
> 245	        running, at: AT ? new Date(AT).toISOString() : null, ageMs: AT ? Date.now() - AT : null,
> 246	    };
> 247	}
> 248	
> 249	module.exports = { start, stop, checkCap, reSnapshot, getStatus };
> 250	
> ```

## 🤖 Claude *(15:21:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '180,265p' /home/gcrux-tradeux/tradeux/backend/scripts/backtest-farm-funnel.js",
  "description": "Read farm-funnel equity-curve and maxDD tracking section"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>   }
>   return reg;
> }
> 
> // ---------- engine: grid no-loss + funil pra BTC (exec no open de i+1, net de fee) ----------
> function gridFunnel(candles, ind, btcCloseByT, gp) {
>   let cash = gp.capital;
>   const lots = [];                 // {qty, spent, price}
>   let btcAccrued = 0, realizedUSDT = 0, nBuys = 0, nSells = 0;
>   let peakEq = gp.capital, maxDD = 0, deployedPeak = 0, exposedBars = 0, totBars = 0;
>   let lastSell = null, bearBars = 0;
> 
>   for (let i = WARM; i < candles.length - 1; i++) {
>     const px = candles[i + 1].open;            // execução sem lookahead
>     const closeNext = candles[i + 1].close;
>     const reg = ind.regime[i];
>     const rsi = ind.rsi[i];
>     const btcPx = btcCloseByT.get(candles[i + 1].t) || btcCloseByT.get(candles[i].t) || null;
>     if (reg === 'bear') bearBars++;
>     totBars++;
> 
>     // 1) VENDAS no-loss: realiza cada lote que atingiu o lucro líquido alvo (nunca vende no prejuízo)
>     for (let k = lots.length - 1; k >= 0; k--) {
>       const lot = lots[k];
>       const sellVal = lot.qty * px * (1 - FEE);
>       if (sellVal >= lot.spent * (1 + gp.minProfit)) {
>         cash += lot.spent;                       // principal volta pro caixa de trabalho
>         const profit = sellVal - lot.spent;      // lucro líquido
>         realizedUSDT += profit;
>         if (btcPx) btcAccrued += profit / btcPx; // FUNIL: só o lucro vira BTC
>         lots.splice(k, 1); nSells++; lastSell = px;
>       }
>     }
> 
>     // 2) COMPRA grid: dip espaçado, gateado por regime !=bear, com teto de inventário
>     const minLotPrice = lots.length ? Math.min(...lots.map(l => l.price)) : Infinity;
>     const spaced = lots.length === 0 ? true : px <= minLotPrice * (1 - gp.gridStep);
>     const belowLastSell = lastSell === null ? true : px <= lastSell * (1 - gp.gridStep);
>     // filtro macro: não comprar dip quando a tendência de longo prazo está caindo (SMA macro hoje < passado)
>     const macroOk = !gp.macroSma || (Number.isFinite(ind.smaMacro[i]) && Number.isFinite(ind.smaMacro[i - gp.macroSlope]) && ind.smaMacro[i] >= ind.smaMacro[i - gp.macroSlope]);
>     if (reg !== 'bear' && reg !== 'warm' && macroOk && lots.length < gp.maxLots && cash >= gp.lotUSDT
>       && Number.isFinite(rsi) && rsi < gp.rsiBuy && spaced && belowLastSell) {
>       const qty = gp.lotUSDT * (1 - FEE) / px;   // fee na compra
>       lots.push({ qty, spent: gp.lotUSDT, price: px });
>       cash -= gp.lotUSDT; nBuys++;
>     }
> 
>     // 3) mark-to-market do equity total (caixa + inventário + BTC acumulado)
>     const invMtM = lots.reduce((s, l) => s + l.qty * closeNext, 0);
>     const eq = cash + invMtM + btcAccrued * (btcPx || 0);
>     if (eq > peakEq) peakEq = eq;
>     const dd = eq / peakEq - 1; if (dd < maxDD) maxDD = dd;
>     const deployed = gp.capital - cash; if (deployed > deployedPeak) deployedPeak = deployed;
>     if (lots.length > 0) exposedBars++;
>   }
> 
>   // fim: inventário preso marcado a mercado no último close
>   const lastClose = candles[candles.length - 1].close;
>   const lastBtc = btcCloseByT.get(candles[candles.length - 1].t) || null;
>   const invFinal = lots.reduce((s, l) => s + l.qty * lastClose, 0);
>   const invCost = lots.reduce((s, l) => s + l.spent, 0);
>   const eqFinal = cash + invFinal + btcAccrued * (lastBtc || 0);
>   return {
>     btcAccrued, realizedUSDT, nBuys, nSells, lotsOpen: lots.length,
>     invFinal, invCost, unrealized: invFinal - invCost,
>     cash, eqFinal, capital: gp.capital, totalReturn: eqFinal / gp.capital - 1,
>     maxDD, deployedPeak, exposure: exposedBars / (totBars || 1), bearFrac: bearBars / (totBars || 1),
>   };
> }
> 
> // cruzamento SMA 50/200 (sinal do trend-following id6/id7): golden = cruza p/ cima, death = p/ baixo
> function smaCross(sma50, sma200, i) {
>   const f = sma50[i], s = sma200[i], fp = sma50[i - 1], sp = sma200[i - 1];
>   if (![f, s, fp, sp].every(Number.isFinite)) return null;
>   if (fp <= sp && f > s) return 'golden';
>   if (fp >= sp && f < s) return 'death';
>   return null;
> }
> 
> // ---------- engine COMPLETO: farm (grid no-loss) + trend (SMA50/200) coordenados + funil ----------
> // Coordenação fiel ao runtime: trend entra no golden cross (se !=bear) e sai no death cross (corta no
> // prejuízo — NÃO é no-loss); farm pausa quando há posição de trend ou regime trend/bear. Ambos → funil.
> function gridTrendFunnel(candles, ind, btcCloseByT, gp) {
>   let cash = gp.capital;
>   const lots = [];
>   let trendPos = null;             // {qty, spent}
> ```

## 🤖 Claude *(15:21:28)*

Now I have the key facts. Let me verify the critical claim — what the farm-funnel backtest reports for maxDD per symbol (especially LTC -19.3%), and confirm the engine already tracks the rolling-peak equity curve that the lever needs.

## 🤖 Claude *(15:21:31)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"maxDD\\|LTC\\|maxlots\\|lotUSDT\\|FARM_MAX\\|lot\\b\" /home/gcrux-tradeux/tradeux/backend/backtest-results/farm-funnel-1h-full-macro500.md 2>/dev/null | head -40; echo \"===MACRO500 farm-only===\"; cat /home/gcrux-tradeux/tradeux/backend/backtest-results/farm-funnel-1h-macro500.md 2>/dev/null",
  "description": "Inspect maxDD numbers in farm-funnel result reports"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 19:| LTCUSDT | +0.00021 | -170.47 | 7t/2W ($-177.32) | 6/6 | $0.00 ($0.00) | -17.73% | -19.66% | 8.17% | 54.80% |
> 22:**Agregado recente (~últ. 365d):** BTC acumulado **+0.00165** (≈ **+0.00165 BTC/ano**) · lucro realizado **$-668.40** sobre **$8000** de capital · retorno do equity total **-9.89%** · inventário preso no fim **$163.72** (PnL não-realizado **$-136.28**) · maxDD médio **-13.19%** · exposição média **25.11%** · janela classificada bear **55.05%** do tempo.
> 35:| LTCUSDT | +0.00065 | 30.80 | 4t/3W ($30.12) | 1/1 | $0.00 ($0.00) | 7.04% | -10.03% | 15.67% | 41.96% |
> 38:**Agregado bull 2023-24:** BTC acumulado **+0.01889** (≈ **+0.03829 BTC/ano**) · lucro realizado **$671.68** sobre **$8000** de capital · retorno do equity total **22.71%** · inventário preso no fim **$480.92** (PnL não-realizado **$-19.08**) · maxDD médio **-9.23%** · exposição média **13.01%** · janela classificada bear **40.23%** do tempo.
> 51:| LTCUSDT | +0.00006 | -53.72 | 3t/0W ($-55.36) | 2/2 | $572.83 ($72.83) | 1.85% | -13.23% | 8.57% | 51.70% |
> 54:**Agregado bear 2022:** BTC acumulado **+0.01221** (≈ **+0.01221 BTC/ano**) · lucro realizado **$-385.66** sobre **$8000** de capital · retorno do equity total **-2.10%** · inventário preso no fim **$640.10** (PnL não-realizado **$40.10**) · maxDD médio **-13.48%** · exposição média **11.52%** · janela classificada bear **57.13%** do tempo.
> ===MACRO500 farm-only===
> # TradeUX — Backtest "Farm-and-Funnel" (grid no-loss multi-alt → funil pra BTC)
> 
> > 8 alts · 1h · fee 0.1%/lado · exec no open seguinte (sem lookahead).
> > Grid: capital 1000 USDT/alt, lote 100, máx 8 lotes, passo 1.50%, lucro-alvo 0.60%, compra RSI<35, gate regime !=bear + filtro macro SMA500 não-caindo (slope 240).
> > Funil: o lucro LÍQUIDO de cada venda vira BTC ao preço do BTC no momento. O principal volta pro caixa de trabalho.
> 
> 
> ## recente (~últ. 365d) — 8 alts, capital total 8000 USDT
> 
> | Alt | BTC acumulado | Lucro realiz. (USDT) | Buys/Sells | Inventário preso (PnL n/realiz.) | Retorno equity | MaxDD | Exposição | % bear |
> |---|---|---|---|---|---|---|---|---|
> | BNBUSDT | +0.00004 | 3.32 | 4/4 | $0.00 ($0.00) | 0.25% | -0.13% | 0.29% | 44.20% |
> | ETHUSDT | +0.00010 | 7.32 | 8/8 | $0.00 ($0.00) | 0.62% | -1.14% | 7.45% | 54.25% |
> | SOLUSDT | +0.00013 | 10.60 | 14/11 | $160.29 ($-139.71) | -13.14% | -13.55% | 40.95% | 52.20% |
> | XRPUSDT | +0.00017 | 17.06 | 20/19 | $53.14 ($-46.86) | -4.69% | -6.24% | 54.34% | 61.81% |
> | ADAUSDT | +0.00009 | 8.88 | 9/9 | $0.00 ($0.00) | 0.00% | -1.11% | 2.15% | 62.67% |
> | LINKUSDT | +0.00009 | 7.76 | 11/8 | $186.12 ($-113.88) | -11.39% | -13.87% | 42.24% | 54.43% |
> | LTCUSDT | +0.00004 | 3.22 | 4/4 | $0.00 ($0.00) | 0.00% | -0.70% | 1.62% | 54.80% |
> | AVAXUSDT | +0.00009 | 7.19 | 8/8 | $0.00 ($0.00) | 0.00% | -0.69% | 1.20% | 56.05% |
> 
> **Agregado recente (~últ. 365d):** BTC acumulado **+0.00075** (≈ **+0.00075 BTC/ano**) · lucro realizado **$65.34** sobre **$8000** de capital · retorno do equity total **-3.54%** · inventário preso no fim **$399.56** (PnL não-realizado **$-300.44**) · maxDD médio **-4.68%** · exposição média **18.78%** · janela classificada bear **55.05%** do tempo.
> 
> 
> ## bull 2023-24 — 8 alts, capital total 8000 USDT
> 
> | Alt | BTC acumulado | Lucro realiz. (USDT) | Buys/Sells | Inventário preso (PnL n/realiz.) | Retorno equity | MaxDD | Exposição | % bear |
> |---|---|---|---|---|---|---|---|---|
> | BNBUSDT | +0.00012 | 4.48 | 5/5 | $0.00 ($0.00) | 0.74% | -0.16% | 0.47% | 33.25% |
> | ETHUSDT | +0.00005 | 1.70 | 1/1 | $0.00 ($0.00) | 0.30% | -0.06% | 0.05% | 32.24% |
> | SOLUSDT | +0.00016 | 5.97 | 4/4 | $0.00 ($0.00) | 1.02% | -0.49% | 0.21% | 37.80% |
> | XRPUSDT | +0.00025 | 9.92 | 10/10 | $0.00 ($0.00) | 1.56% | -0.36% | 4.21% | 51.33% |
> | ADAUSDT | +0.00012 | 4.39 | 2/2 | $0.00 ($0.00) | 0.77% | -0.16% | 0.09% | 40.64% |
> | LINKUSDT | +0.00029 | 10.62 | 10/10 | $0.00 ($0.00) | 1.82% | -0.99% | 1.58% | 42.10% |
> | LTCUSDT | +0.00010 | 3.91 | 4/4 | $0.00 ($0.00) | 0.64% | -0.17% | 0.89% | 41.96% |
> | AVAXUSDT | +0.00004 | 1.49 | 1/1 | $0.00 ($0.00) | 0.26% | -0.06% | 0.02% | 42.53% |
> 
> **Agregado bull 2023-24:** BTC acumulado **+0.00114** (≈ **+0.00231 BTC/ano**) · lucro realizado **$42.49** sobre **$8000** de capital · retorno do equity total **0.89%** · inventário preso no fim **$0.00** (PnL não-realizado **$0.00**) · maxDD médio **-0.31%** · exposição média **0.94%** · janela classificada bear **40.23%** do tempo.
> 
> 
> ## bear 2022 — 8 alts, capital total 8000 USDT
> 
> | Alt | BTC acumulado | Lucro realiz. (USDT) | Buys/Sells | Inventário preso (PnL n/realiz.) | Retorno equity | MaxDD | Exposição | % bear |
> |---|---|---|---|---|---|---|---|---|
> | BNBUSDT | +0.00039 | 10.30 | 11/11 | $0.00 ($0.00) | 0.68% | -5.37% | 10.81% | 55.05% |
> | ETHUSDT | +0.00012 | 3.69 | 3/3 | $0.00 ($0.00) | 0.20% | -0.20% | 0.25% | 51.63% |
> | SOLUSDT | +0.00165 | 33.08 | 29/21 | $558.89 ($-241.11) | -21.23% | -50.19% | 20.49% | 62.35% |
> | XRPUSDT | +0.00028 | 9.65 | 8/8 | $0.00 ($0.00) | 0.49% | -0.67% | 1.29% | 54.32% |
> | ADAUSDT | +0.00173 | 41.75 | 34/33 | $78.07 ($-21.93) | 0.82% | -4.25% | 33.12% | 63.28% |
> | LINKUSDT | +0.00378 | 81.25 | 52/51 | $86.39 ($-13.61) | 5.23% | -15.20% | 29.62% | 57.05% |
> | LTCUSDT | +0.00065 | 14.32 | 12/12 | $0.00 ($0.00) | 1.14% | -1.56% | 1.94% | 51.70% |
> | AVAXUSDT | +0.00198 | 43.52 | 30/28 | $152.73 ($-47.27) | -1.28% | -10.79% | 20.44% | 61.69% |
> 
> **Agregado bear 2022:** BTC acumulado **+0.01057** (≈ **+0.01057 BTC/ano**) · lucro realizado **$237.55** sobre **$8000** de capital · retorno do equity total **-1.74%** · inventário preso no fim **$876.08** (PnL não-realizado **$-323.92**) · maxDD médio **-11.03%** · exposição média **14.74%** · janela classificada bear **57.13%** do tempo.
> 
> 
> ## 🎯 Síntese — taxa de acúmulo e o que falta pra +3 BTC
> 
> | Período | BTC/ano (por 8000 USDT) | Lucro realiz. | Retorno equity | Inventário preso | % bear |
> |---|---|---|---|---|---|
> | recente (~últ. 365d) | +0.00075 | $65.34 | -3.54% | $399.56 | 55.05% |
> | bull 2023-24 | +0.00231 | $42.49 | 0.89% | $0.00 | 40.23% |
> | bear 2022 | +0.01057 | $237.55 | -1.74% | $876.08 | 57.13% |
> 
> **Leitura honesta:**
> - **BTC/ano** é a taxa do funil normalizada pelo capital de trabalho (8×1000 = 8000 USDT). Pra +3 BTC, escale capital × tempo: dobrar o capital ~dobra a taxa (até o teto de liquidez/lotes).
> - O **inventário preso** é o calcanhar do no-loss: capital que ficou comprado sem fechar no lucro (pior no bear). Se grande, o "lucro realizado" foi em parte financiado por capital imobilizado — por isso o **retorno do equity total** (que inclui esse inventário marcado a mercado) é o juiz, não o lucro realizado isolado.
> - **% bear** mostra quanto do tempo o gate de regime manteve o grid em caixa (sem comprar). Em janelas muito bear, o farm quase não roda — é esperado e é a proteção funcionando.
> 
> ---
> _Gerado por backend/scripts/backtest-farm-funnel.js. Dados: Binance klines reais (mainnet, cache em backtest-data/). Net de fee. Não é conselho financeiro; validação de estratégia._
> ```

## 🤖 Claude *(15:21:40)*

I now have everything needed. The critical finding for the adversarial verdict: the maxDD that the lever targets is dominated by **trapped inventory** (no-loss inventory held through a bear), not by a single bad new-buy. Let me confirm one mechanism detail — whether throttling *new buys* (which is all the lever can do) actually touches that maxDD source.

The key mechanism in `gridFunnel`: maxDD is computed mark-to-market over `cash + invMtM + btcAccrued`. The drawdown comes from `invMtM` — inventory ALREADY bought — depreciating. The lever throttles only *new* buy notional based on current DD. But by the time DD is deep, buying has already stopped (regime gate `!=bear` + macro filter already suppress buys in the falling tape). So the throttle has little left to cut at the moment it would matter.

Let me verify the worst-case (SOL bear -50.19%, LINK bear -15.20%) is inventory-driven, not new-buy-driven, by checking the relationship between maxDD and trapped inventory in the data I already have. SOL bear: maxDD -50.19% with $558.89 trapped inventory ($-241.11 unrealized). That confirms it: the drawdown is held inventory bleeding, and the regime gate (62% bear) already had buys mostly off.

## 🤖 Claude *(15:21:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"macroOk\\|reg !== 'bear'\\|rsi < gp.rsiBuy\\|FARM_MAX\\|FARM_DCA\\|riskState\\|isHalted\" /home/gcrux-tradeux/tradeux/backend/scripts/backtest-farm-funnel.js | head; echo \"===live farm exposure cap===\"; grep -rn \"FARM_MAX_NOTIONAL\\|FARM_MAX\\|farmExposure\\|FARM_DCA\" /home/gcrux-tradeux/tradeux/backend/src 2>/dev/null | head -15",
  "description": "Confirm buy gating in backtest and live farm exposure cap"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 219:    const macroOk = !gp.macroSma || (Number.isFinite(ind.smaMacro[i]) && Number.isFinite(ind.smaMacro[i - gp.macroSlope]) && ind.smaMacro[i] >= ind.smaMacro[i - gp.macroSlope]);
> 220:    if (reg !== 'bear' && reg !== 'warm' && macroOk && lots.length < gp.maxLots && cash >= gp.lotUSDT
> 221:      && Number.isFinite(rsi) && rsi < gp.rsiBuy && spaced && belowLastSell) {
> 278:    const macroOk = !gp.macroSma || (Number.isFinite(ind.smaMacro[i]) && Number.isFinite(ind.smaMacro[i - gp.macroSlope]) && ind.smaMacro[i] >= ind.smaMacro[i - gp.macroSlope]);
> 289:    if (!trendPos && cross === 'golden' && reg !== 'bear' && reg !== 'warm' && adxOk && (!gp.trendSwitch || macroOk)) {
> 306:    if (reg !== 'bear' && reg !== 'trend' && reg !== 'warm' && macroOk && !trendPos
> 307:      && lots.length < gp.maxLots && cash >= gp.lotUSDT && Number.isFinite(rsi) && rsi < gp.rsiBuy && spaced && belowLastSell) {
> ===live farm exposure cap===
> /home/gcrux-tradeux/tradeux/backend/src/paperEngine.js:6:// `orders`, NUNCA toca os buckets reais (TREND_QTY/FARM_DCA) nem a carteira real → roda com o mainnet
> /home/gcrux-tradeux/tradeux/backend/src/app-em.js:289:        // benéfico (o FARM_DCA recomputa e a trava some juntos). v1 SEM reconstrução-no-boot: uma venda em voo
> /home/gcrux-tradeux/tradeux/backend/src/app-em.js:297:        if (order.status !== orderStatus.FILLED) return; // só o fill recomputa o FARM_DCA
> /home/gcrux-tradeux/tradeux/backend/src/app-em.js:300:        await beholder.updateMemory(order.symbol, indexKeys.FARM_DCA, null, dca, false);
> /home/gcrux-tradeux/tradeux/backend/src/app-em.js:301:        logger('system', `FARM_DCA[${order.symbol}] atualizado: qty=${dca.qty}, cost=${dca.cost} (pós-fill de ${order.side})`);
> /home/gcrux-tradeux/tradeux/backend/src/app-em.js:312:            await beholder.updateMemory(symbol, indexKeys.FARM_DCA, null, dca, false);
> /home/gcrux-tradeux/tradeux/backend/src/app-em.js:313:            logger('system', `FARM_DCA[${symbol}] carregado no boot: qty=${dca.qty}, cost=${dca.cost}`);
> /home/gcrux-tradeux/tradeux/backend/src/utils/indexes.js:83:    FARM_DCA: 'FARM_DCA', // preço médio ponderado (DCA) e quantidade de posições abertas no Farm {qty, cost}
> /home/gcrux-tradeux/tradeux/backend/src/models/paperPositionModel.js:5:// FARM_DCA/TREND_QTY que derivam de orders). PK composta (strategy, symbol). qty = base detido (0 = flat),
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:25:// Teto de EXPOSIÇÃO do Farm por símbolo (USDT investido no bucket FARM_DCA). 0 = desligado. Lido no boot.
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:26:const FARM_MAX_NOTIONAL_USDT = (() => { const n = parseFloat(process.env.FARM_MAX_NOTIONAL_USDT || '0'); return Number.isFinite(n) && n > 0 ? n : 0; })();
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:263:        // MEMORY['<sym>:FARM_DCA'] = { qty, cost }. A venda no-loss vende SÓ o que o Farm comprou,
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:266:        const farm = MEMORY[`${orderTemplate.symbol}:FARM_DCA`];
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:269:            throw new Error(`There is no farm position (FARM_DCA) to use as qty reference for ${orderTemplate.symbol}.`);
> /home/gcrux-tradeux/tradeux/backend/src/beholder.js:490:    // Teto de EXPOSIÇÃO do Farm por símbolo (FARM_MAX_NOTIONAL_USDT): a COMPRA do Farm NÃO acumula mais que o teto
> ```

## 🤖 Claude *(15:21:58)*

I have all the evidence needed. The adversarial analysis is complete.

**Core refutation logic:**

1. **The maxDD the lever targets is inventory-driven, not new-buy-driven.** Worst cases: SOL bear maxDD -50.19% with $558.89 trapped inventory ($-241.11 unrealized); LINK bear -15.20%, $86 trapped; LTC recente -19.66% in the *full* engine. These drawdowns come from `invMtM` — inventory **already bought** depreciating mark-to-market (`gridFunnel` line 230: `eq = cash + invMtM + btcAccrued`). A throttle on *new buy notional* (the only thing this lever can do) cannot un-buy held inventory.

2. **By the time DD is deep, buying is already off.** The regime gate (`reg !== 'bear'`, line 220) + macro SMA-not-falling filter (`macroOk`, line 219) already suppress new buys in a falling tape. SOL bear was 62.35% bear-classified time. The throttle would fire precisely when there's almost nothing left to throttle — it's redundant with existing gates.

3. **The cap -5% already captures the tail.** `dailyCapJob` arms a HOT halt on -5% equity drawdown vs daily baseline, blocking ALL orders (BUY/SELL/OCO). The lever's own honest estimate concedes "+1 a +4 p.p." gross and "the cap -5% already captures ~70% of the benefit."

4. **Live exposure is already double-capped at $149 scale.** `FARM_MAX_NOTIONAL_USDT=$25/symbol` (beholder.js:490) + `MAX_ORDER_NOTIONAL=$25/order`. On ~$149 capital with $25/symbol exposure ceilings, there is no meaningful continuous size-curve to ride down — the position granularity is too coarse for a proportional throttle to matter.

5. **Money-path cost vs marginal benefit fails the lever's own kill-test.** It states: "se o delta for <1 p.p., NÃO vale a complexidade money-path." Given the above, the delta-above-the-cap is almost certainly sub-1 p.p. on the drawdown source that actually hurts.

This is not a refuted-in-disguise (it's genuinely novel, anti-martingale, risk-adjusted only). But it's dominated by existing controls and aimed at the wrong DD source.

## 🤖 Claude *(15:22:09)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "lever": "Throttle de exposi\u00e7\u00e3o drawdown-aware (de-risk cont\u00ednuo em drawdown corrente, anti-martingale)",
  "verdict": "REFUTED",
  "confidence": "medium",
  "rationale": "A alavanca mira o maxDD ERRADO. Nos backtests reais o drawdown que d\u00f3i vem de INVENT\u00c1RIO J\u00c1 COMPRADO marcado-a-mercado, n\u00e3o de novas compras: SOL bear maxDD -50,19% com $558,89 de invent\u00e1rio preso ($-241,11 n\u00e3o-realiz.); LINK bear -15,20%; LTC -19,66% no engine full (farm-funnel-1h-full-macro500.md / -macro500.md). No gridFunnel (backtest-farm-funnel.js:230) eq=cash+invMtM+btcAccrued \u2014 o DD \u00e9 invMtM caindo. Um throttle s\u00f3 pode cortar NOTIONAL DE NOVAS COMPRAS; n\u00e3o des-compra invent\u00e1rio preso. Pior: quando o DD fica fundo, a compra j\u00e1 est\u00e1 DESLIGADA pelo gate de regime (reg!=='bear', linha 220) + filtro macro SMA-n\u00e3o-caindo (linha 219) \u2014 SOL bear ficou 62% do tempo classificado bear. O degrau-cont\u00ednuo dispararia justo quando n\u00e3o h\u00e1 quase nada pra throttlar = redundante com gates existentes. O cap -5% (dailyCapJob: arma HALT QUENTE no drawdown de equity vs baseline do dia, bloqueia TUDO) j\u00e1 captura a cauda \u2014 a pr\u00f3pria alavanca admite '~70% do benef\u00edcio' e ganho bruto '+1 a +4 p.p.'. Ao vivo em $149 j\u00e1 h\u00e1 duplo teto ($25/s\u00edmbolo FARM_MAX_NOTIONAL beholder.js:490 + $25/ordem), ent\u00e3o n\u00e3o existe curva de size cont\u00ednua pra descer \u2014 granularidade grossa demais. Pelo pr\u00f3prio kill-test da alavanca ('delta <1 p.p. acima do cap = N\u00c3O-GO'), o delta sobre a fonte real de DD \u00e9 quase certamente sub-1 p.p. N\u00e3o \u00e9 refutado-disfar\u00e7ado (\u00e9 genuinamente novo, anti-martingale, s\u00f3 risco-ajustado), mas \u00e9 dominado pelos controles j\u00e1 existentes e aponta pra fonte de DD que ele n\u00e3o consegue tocar.",
  "paper_validatable": true
}
```

> **Tool Result (StructuredOutput)** - ✅ Success
>
> ```
> Structured output provided successfully
> ```

## 🤖 Claude *(15:22:22)*

Veredito registrado: **REFUTED** (confiança média, validável no paper).

Resumo factual da refutação adversarial:

- **Mira o maxDD errado.** Os piores drawdowns nos backtests reais vêm de inventário JÁ comprado caindo a mercado, não de novas compras — SOL bear -50,19%/$558 preso, LINK -15,20%, LTC -19,66% no full. O `gridFunnel` computa `eq=cash+invMtM+btcAccrued`; o DD é `invMtM`. Um throttle só corta notional de NOVAS compras — não des-compra o inventário que sangra.
- **Redundante com gates existentes.** Quando o DD fica fundo, a compra já está OFF pelo gate de regime (`reg!=='bear'`) + filtro macro (`macroOk`). SOL bear: 62% do tempo classificado bear. O degrau dispararia quando não sobra quase nada pra cortar.
- **O cap -5% já pega a cauda.** `dailyCapJob` arma HALT QUENTE bloqueando TUDO. A própria alavanca admite ~70% do benefício já coberto e ganho bruto +1 a +4 p.p.
- **Escala $149 não tem curva contínua.** Duplo teto de $25/símbolo (FARM_MAX_NOTIONAL, beholder.js:490) + $25/ordem — granularidade grossa demais para um throttle proporcional importar.
- **Falha no próprio kill-test** (delta <1 p.p. acima do cap = NO-GO).

Não é um refutado disfarçado (é genuinamente anti-martingale e só risco-ajustado), mas é dominado pelos controles atuais.

Arquivos-chave consultados (caminhos absolutos):
- /home/gcrux-tradeux/tradeux/backend/src/dailyCapJob.js
- /home/gcrux-tradeux/tradeux/backend/src/riskState.js
- /home/gcrux-tradeux/tradeux/backend/scripts/backtest-farm-funnel.js (gridFunnel:185-248, gates:219-221)
- /home/gcrux-tradeux/tradeux/backend/src/beholder.js (FARM_MAX_NOTIONAL:26,490)
- /home/gcrux-tradeux/tradeux/backend/backtest-results/farm-funnel-1h-macro500.md e farm-funnel-1h-full-macro500.md

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-21 - agent-a56292f2932d4f90d]]
> * **Próxima Sessão**: [[2026-06-21 - agent-a5ed7e2519af727f5]]
%% --- TIMELINE END --- %%

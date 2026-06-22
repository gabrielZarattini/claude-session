# Session agent-aa9fff75dfcffc53a
**Date:** 2026-06-22 | **Session ID:** `agent-aa9fff75dfcffc53a`

---

## 👤 User *(13:55:37)*

TradeUX = bot de trading SPOT Binance (Beholder/Node/Express + Sequelize + agente LLM via MCP). Sistema 🔴 LIVE em MAINNET REAL, equity ~$149, canary FARM-ONLY (so vendas no-loss do Farm armadas). Codigo REAL em /home/gcrux-tradeux/tradeux (backend/, tradeux-agent/, tradeux-mcp/). LEIA o codigo de verdade com Read/Grep/Bash e CITE file:line. Comentarios do repo sao pt-BR.

JA FEITO NESTA SESSAO (NAO re-flagar como bug — esta corrigido+deployado):
- riskGuard (backend/src/utils/exchange.js): %-teto de COMPRA min(MAX_ORDER_NOTIONAL_USDT, MAX_ORDER_PCT_EQUITY x equity) + piso; VENDA isenta do teto de sizing mas com rede anti-runaway MAX_SELL_EQUITY_MULT (3x equity, degrade-open); equity quente publicado pelo dailyCapJob no riskState. getEffectiveCaps() expoe no cockpit (riskCaps).
- FARM_SELLING ganhou reconstrucao-no-boot (app-em.loadFarmSellingLocks + farmSellBootAction).
- P&L fee-em-BNB ja corrigido (utils/feeCalc.computeNet, coluna orders.commissionAsset).
- forwarding do tool MCP tradeux_get_cockpit corrigido (encaminha groups/paper/riskCaps; src/cockpitOut.js).
- suite de simulacao money-path em backend/scripts/sim/ (7 arquivos; calcQty/riskGuard/dailyCap/feeCalc/farmTriggers/integration/farmSellBoot).

3 HIGH conhecidos da revisao PARCIAL anterior (RE-VALIDE se ainda sao reais com EVIDENCIA no codigo, e ache NOVOS):
H1. useTestnet bit-unico mutavel: um unico bit (settings.useTestnet) flipa testnet<->mainnet (modo dinheiro real).
H2. posicao em qty BRUTA: getFarmPosition/getTrendPosition somam buy.quantity BRUTO (nao liquido de fee) -> 0,908 comprado vs 0,907 recebido.
H3. cegueira ao Earn (LD*) no loadWallet/calcQty: saldo auto-subscrito no Simple Earn (LDxxx) some do sizing/calculo.

Seja adversarial mas PRECISO: nao invente; se algo esta OK, diga OK (nao force achado). Foque DESIGN/CORRECAO, nao estilo.

=== VERIFICACAO ADVERSARIAL ===
Verifique este achado da dimensao "resilience-state" contra o codigo REAL (Read/Grep/Bash em /home/gcrux-tradeux/tradeux). TENTE REFUTAR: e problema REAL ou falso-positivo? Confirme/corrija a location (file:line), reproduza a logica no codigo, e de o veredito honesto + severidade FINAL. Default CETICO: se nao conseguir confirmar com evidencia concreta no codigo, confirmed=false. Se confirmar, ajuste a severidade pra realidade (um "qty bruta" que o calcQty mitiga pode ser MEDIUM/LOW, nao HIGH).

ACHADO:
{
 "title": "Equity-quente: janela de staleness assimétrica — EQUITY_MAX_AGE_MS default 10min vs publicação a cada ~60s, sem alarme dedicado de equity-velho desacoplado do cap",
 "severity": "MEDIUM",
 "location": "backend/src/utils/exchange.js:47-48 (EQUITY_MAX_AGE_MS=600000) e :64-69 (freshEquity) ; riskState.js:42-47 (equitySnap não-persistido) ; dailyCapJob.js:178 (única chamada de setEquity)",
 "description": "setEquity só é chamado pelo dailyCapJob em ciclos `valued` (dailyCapJob:178; e no reSnapshot manual). Se o dailyCapJob morrer/travar (running preso, exceção recorrente, ou DAILY_CAP_ENABLED=false), o equity-quente para de ser republicado. freshEquity() aceita o valor por até EQUITY_MAX_AGE_MS=10min após o último `at`; passado isso retorna null e o %-teto de COMPRA cai SILENCIOSAMENTE para o teto absoluto. O alarme anti-silêncio (dailyCapJob:164-169) cobre o caso de equity INAVALIÁVEL (cold), mas NÃO o caso de o próprio job estar morto/parado — nesse cenário não há ciclo, logo não há cold-alert, e o equity-quente apenas expira sem aviso. Como equitySnap não é persistido (riskState.js:40-42), todo restart começa com value:null/at:null (degrade seguro até o 1º ciclo valued, ok). O risco não é a direção (degrada para teto menor = seguro) mas a OBSERVABILIDADE: o operador não é avisado de que o motor do %-teto perdeu a referência de equity.",
 "impact": "Se o dailyCapJob parar, o teto-%-equity de COMPRA silenciosamente vira teto absoluto após 10min sem nenhum alerta; o operador acha que o sizing por %-equity está ativo quando não está. Não é perda de dinheiro direta (degrada conservador), mas é cegueira de risco.",
 "isKnownHigh": false
}

## 🤖 Claude *(13:55:41)*

I'll verify this finding against the real code. Let me start by loading context and examining the specific files cited.

## 🤖 Claude *(13:55:41)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/HANDOFF.md"
}
```

## 🤖 Claude *(13:55:42)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/src/utils/exchange.js",
  "offset": 1,
  "limit": 120
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	const BinanceApi = require('node-binance-api');
> 2	// node-binance-api 1.x (fork ccxt): o build CJS exporta a classe Binance direto (require() já
> 3	// é a classe; .default é undefined). O `|| BinanceApi` é só fallback defensivo p/ builds futuras.
> 4	const Binance = BinanceApi.default || BinanceApi;
> 5	const LOGS = process.env.BINANCE_LOGS === 'true';
> 6	const SAPI_URL = process.env.BINANCE_SAPI_URL;
> 7	const logger = require('./logger');
> 8	const riskState = require('../riskState'); // fonte única do HALT (QUENTE); sem ciclo (riskState não requer o app)
> 9	
> 10	// === Teto de risco global (chokepoint único: TODA ordem real — automação, funil ou manual — passa por
> 11	// buy()/sell()/oco() aqui). Única trava de tamanho do BACKEND (o ALLOW_TRADING é só do agente LLM).
> 12	//   HALT (kill-switch)           → bloqueia QUALQUER ordem (parada de emergência) — cobre TUDO, COMPRA E VENDA.
> 13	//                                  QUENTE: lido por ordem via riskState.isHalted(). TRADING_HALT=true no .env SEEDA
> 14	//                                  o riskState como floor permanente (mexer no .env ainda exige restart); o operador
> 15	//                                  (POST /system/halt) e o cap diário -5% (dailyCapJob) flipam SEM restart.
> 16	//
> 17	//   TETO DE NOTIONAL — aplica-se SÓ A COMPRA. Venda CONVERTE ativo→USDT (reduz exposição) e já é limitada pela
> 18	//   carteira no calcQty → fica ISENTA do teto de compra (segue coberta pelo HALT; o cofre BTC, pela trava do MCP).
> 19	//   Isso conserta o furo histórico em que o teto fixo barrava venda no-loss legítima (ex.: a venda de $40 do LTC vs
> 20	//   teto $25) e dispensa o symbol-aware de BTC (a colheita de BTC_EXCESS é VENDA → isenta).
> 21	//   MAX_SELL_EQUITY_MULT=<n>     → rede anti-runaway na VENDA (defesa-em-profundidade, NÃO sizing): teto FOLGADO =
> 22	//                                  n×equity quente. Barra SÓ venda EGRÉGIA (qty buggado: notional > n×equity), nunca
> 23	//                                  venda legítima (1 posição ≤ equity << n×equity). equity frio/velho → venda PASSA
> 24	//                                  (degrade OPEN — jamais barrar venda protetiva por memória fria). 0/ausente = sem
> 25	//                                  teto de venda. Recomendado folgado (2-3×).
> 26	//   O limite efetivo da compra é:
> 27	//        cap = min( MAX_ORDER_NOTIONAL_USDT , MAX_ORDER_PCT_EQUITY × equityTradeável )  , nunca < MIN_ORDER_NOTIONAL_FLOOR
> 28	//   MAX_ORDER_PCT_EQUITY=<0..1>  → teto da COMPRA como fração do equity tradeable QUENTE (publicado pelo dailyCapJob
> 29	//                                  no riskState a cada ~60s; mark-to-market, conta Earn LD*). É o motor do
> 30	//                                  dimensionamento que ESCALA com o capital. equity ausente/frio/velho
> 31	//                                  (> EQUITY_MAX_AGE_MS) → a % é ignorada e cai-se pro teto absoluto (degrada seguro).
> 32	//                                  0/ausente = %-teto desligado.
> 33	//   MAX_ORDER_NOTIONAL_USDT=<n>  → TETO ABSOLUTO (runaway guard) em USDT — barra uma leitura de equity errada/grande.
> 34	//                                  Deve ficar ACIMA do %-teto típico. 0 = sem teto absoluto.
> 35	//   MIN_ORDER_NOTIONAL_FLOOR=<n> → piso: o %-teto NUNCA derruba o limite abaixo disto (não barra ordem mínima
> 36	//                                  legítima quando o equity é pequeno). 0/ausente = sem piso.
> 37	//   Formas de notional cobertas: quote (quoteOrderQty, ex.: funil), LIMIT/OCO (price×qty) e MARKET-por-QTY sem price
> 38	//   (deriva o preço do MINI_TICKER; STOP/TP-MARKET usa o stopPrice). MINI_TICKER frio → PASSA (logado), coberto só
> 39	//   pelo HALT. Só pares *USDT (notional em USDT); quote ≠ USDT passa.
> 40	// Inerte por padrão; ajustável por env SEM deploy de código (basta reiniciar). Fail-closed (lança). ===
> 41	const _maxNotional = parseFloat(process.env.MAX_ORDER_NOTIONAL_USDT || '0');
> 42	const MAX_ORDER_NOTIONAL_USDT = Number.isFinite(_maxNotional) && _maxNotional > 0 ? _maxNotional : 0;
> 43	const _pctEq = parseFloat(process.env.MAX_ORDER_PCT_EQUITY || '0');
> 44	const MAX_ORDER_PCT_EQUITY = Number.isFinite(_pctEq) && _pctEq > 0 && _pctEq < 1 ? _pctEq : 0;
> 45	const _floorMin = parseFloat(process.env.MIN_ORDER_NOTIONAL_FLOOR || '0');
> 46	const MIN_ORDER_NOTIONAL_FLOOR = Number.isFinite(_floorMin) && _floorMin > 0 ? _floorMin : 0;
> 47	const _eqMaxAge = parseInt(process.env.EQUITY_MAX_AGE_MS || '600000', 10);
> 48	const EQUITY_MAX_AGE_MS = Number.isFinite(_eqMaxAge) && _eqMaxAge > 0 ? _eqMaxAge : 600000; // equity mais velho que isto → cai pro teto absoluto
> 49	const _sellMult = parseFloat(process.env.MAX_SELL_EQUITY_MULT || '0');
> 50	const MAX_SELL_EQUITY_MULT = Number.isFinite(_sellMult) && _sellMult > 0 ? _sellMult : 0; // teto FOLGADO da venda = n×equity (rede anti-runaway). 0 = sem teto de venda.
> 51	
> 52	// Deriva o notional em USDT da ordem (quote do funil, price×qty do LIMIT/OCO, ou MARKET-por-qty via stopPrice/MINI_TICKER).
> 53	// null quando não dá p/ avaliar (MARKET-por-qty com preço de referência frio). Puro/read-only.
> 54	function notionalOf(symbol, quantity, price, o) {
> 55	    if (o.quoteOrderQty != null) return parseFloat(o.quoteOrderQty);                 // MARKET por quote (ex.: funil)
> 56	    if (price != null && quantity != null) return parseFloat(price) * parseFloat(quantity); // LIMIT/OCO
> 57	    if (quantity != null) {                                                          // MARKET por QTY-base sem price (ou STOP/TP-MARKET)
> 58	        const ref = (o.stopPrice != null ? parseFloat(o.stopPrice) : refPrice(symbol)); // STOP/TP-MARKET: stopPrice; senão deriva o spot do MINI_TICKER
> 59	        if (Number.isFinite(ref) && ref > 0) return ref * parseFloat(quantity);
> 60	    }
> 61	    return null;
> 62	}
> 63	
> 64	// Equity tradeável QUENTE e FRESCO (publicado pelo dailyCapJob no riskState), ou null se ausente/frio/velho.
> 65	function freshEquity() {
> 66	    const eq = (riskState.getEquity && riskState.getEquity()) || null;
> 67	    if (eq && Number.isFinite(eq.value) && eq.value > 0 && eq.at && (Date.now() - eq.at) <= EQUITY_MAX_AGE_MS) return eq.value;
> 68	    return null;
> 69	}
> 70	
> 71	function assertWithinRisk(action, symbol, quantity, price, options) {
> 72	    if (riskState.isHalted()) {
> 73	        const st = riskState.getState();
> 74	        const msg = `[riskGuard] HALT ativo (${st.source}: ${st.reason || 'kill-switch'}) — ${action} ${symbol} BLOQUEADA.`;
> 75	        logger('system', msg);
> 76	        throw new Error(msg);
> 77	    }
> 78	
> 79	    if (!/USDT$/i.test(symbol || '')) return; // teto em USDT só vale p/ pares *USDT (compra e venda)
> 80	    const o = options || {};
> 81	
> 82	    // VENDA: isenta do %-teto de COMPRA (reduz risco; já capada na carteira pelo calcQty). Só o HALT e a rede
> 83	    // anti-runaway FOLGADA (opt-in) a cobrem. A rede barra SÓ venda egrégia (notional > n×equity) p/ pegar um qty
> 84	    // buggado, NUNCA venda legítima (1 posição ≤ equity << n×equity). equity frio/velho → venda PASSA (degrade
> 85	    // OPEN: jamais barrar venda protetiva por memória fria — a direção segura na venda é deixar passar).
> 86	    if (/SELL/i.test(action || '')) {
> 87	        if (MAX_SELL_EQUITY_MULT > 0) {
> 88	            const eqv = freshEquity();
> 89	            if (eqv != null) {
> 90	                const sellCap = MAX_SELL_EQUITY_MULT * eqv;
> 91	                const n = notionalOf(symbol, quantity, price, o);
> 92	                if (Number.isFinite(n) && n > sellCap) {
> 93	                    const msg = `[riskGuard] ${action} ${symbol} notional $${n.toFixed(2)} > teto de venda $${sellCap.toFixed(2)} (${MAX_SELL_EQUITY_MULT}× equity) — BLOQUEADA (runaway?).`;
> 94	                    logger('system', msg);
> 95	                    throw new Error(msg);
> 96	                }
> 97	            }
> 98	        }
> 99	        return;
> 100	    }
> 101	
> 102	    // COMPRA: limite efetivo = min(teto absoluto, %×equity), com piso de ordem mínima.
> 103	    let pctCap = Infinity;
> 104	    if (MAX_ORDER_PCT_EQUITY > 0) {
> 105	        const eqv = freshEquity();
> 106	        if (eqv != null) {
> 107	            pctCap = MAX_ORDER_PCT_EQUITY * eqv;
> 108	            if (MIN_ORDER_NOTIONAL_FLOOR > 0 && pctCap < MIN_ORDER_NOTIONAL_FLOOR) pctCap = MIN_ORDER_NOTIONAL_FLOOR;
> 109	        }
> 110	    }
> 111	    const absCeil = MAX_ORDER_NOTIONAL_USDT > 0 ? MAX_ORDER_NOTIONAL_USDT : Infinity;
> 112	    const cap = Math.min(pctCap, absCeil);
> 113	    if (!Number.isFinite(cap)) return; // nem % (equity frio) nem teto absoluto configurado → inerte (só HALT cobre)
> 114	
> 115	    const notional = notionalOf(symbol, quantity, price, o);
> 116	    if (notional == null && quantity != null && price == null && o.quoteOrderQty == null) // MARKET-por-qty c/ ref fria
> 117	        logger('system', `[riskGuard] ${action} ${symbol} MARKET-por-qty sem preço de referência (MINI_TICKER frio) — teto NÃO avaliado (coberto só pelo HALT).`);
> 118	    if (Number.isFinite(notional) && notional > cap) {
> 119	        const basis = (Number.isFinite(pctCap) && pctCap <= absCeil) ? `${(MAX_ORDER_PCT_EQUITY * 100).toFixed(0)}% do equity` : 'teto absoluto';
> 120	        const msg = `[riskGuard] ${action} ${symbol} notional $${notional.toFixed(2)} > teto $${cap.toFixed(2)} (${basis}) — BLOQUEADA.`;
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>[Truncated: PARTIAL view — showing lines 1-239 of 867 total (76999 tokens, cap 25000). Call Read with offset=240 limit=239 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>
> 
> 1	# TradeUX — HANDOFF (single source of truth)
> 2	
> 3	> ShakeHands continuity doc. `/handson` reads this FIRST. Newest record at the bottom.
> 4	> Project: **TradeUX** — Beholder-based multi-coin Binance Spot bot + LLM agent (**mainnet/testnet dual-env**).
> 5	> Updated: **2026-06-21** · Phase: **GO-LIVE MAINNET — 🔴 LIVE (`halted=false`)** · **Canary FARM-ONLY** (vendas no-loss id10/12/14 — **AGORA FUNCIONAM**; compras off) · **SESSÃO 21/jun (maratona): incidente Earn auto-subscribe diagnosticado+resolvido + 4 bugs corrigidos/gated/deployados** → `c6d0853` (dailyCap conta `LD*` do Earn = fim do HALT-falso), `457e25a` (silencia PUSH `[PAPER]` + alerta Telegram em falha real), **`fb932a1` (venda do Farm EDGE→LEVEL-trigger = 1ª saída no-loss do Farm a EXECUTAR no mainnet)** → **LTC vendido +$0,49** (ordem 264 @ $44,54, FARM_DCA→0, equity **$149,39**) · ⚠️ **runtime não-git (reaplicar se reset):** `.env MAX_ORDER_NOTIONAL_USDT=25→50` (band-aid: o teto bloqueava a VENDA de $40), DB `monitors`#2 `*:BOOK isActive=1` · proteções: cap diário −5%, teto **$50/ordem**, Farm $25/símbolo, riskGuard, pânico, painel de grupos · Meta: **realista ≈ flat com ~$149** · Vivo==master==origin==**`fb932a1`**
> 6	
> 7	> 🟢 **ATUALIZAÇÃO 2026-06-21 (cont. — MARATONA 2): suíte de simulação money-path + D3 deployado + paper-validate das 3 alavancas.** Estado segue **🔴 LIVE (`halted=false`), Canary FARM-ONLY**, equity ~$149, HALT intacto o tempo todo. 7 commits (todos gate QA+TL, CI verde, 2 deploys de backend): **(1) SUÍTE DE SIMULAÇÃO** (`backend/scripts/sim/`, 6 arquivos, **90 asserts**, no CI) — achou+corrigiu **3 bugs REAIS latentes**: `getStableConversion` não-exportada (taxa BNB sumia do P&L → `854bab5` estava INERTE), `placeOrder:551` precedência (erro virava `undefined` no Telegram), `placeOrder:573` `order.type` (stopPrice não persistia). **(2) D3 DEPLOYADO** (`5c83c31`): `tradeux_get_cockpit` traz `status.groups` (ATIVO por grupo) + doutrina GATE≠ATIVO (agente para de dizer "aguardando golden cross p/ comprar" com grupo parado; valida no próx. ciclo pós-429). **(3) PAPER-VALIDATE: 3 alavancas LIVE em paper** (grupo paper **40/40**): MR15 (mean-reversion 15m), Slopegate (trend só entra se `TREND_SLOPE_1h!='down'` — sinal novo no regimeJob), Farmnl (Farm no-loss REAL: paperEngine publica `FARMNL_TARGET`=custo×1.012). **Vivo==master==origin==`2c55fe0`.** ⚠️ trilhas paper são RUNTIME — reaplicar pós-`make nuke`: `setup-paper-mr15.js` + `setup-paper-levers.js`.
> 8	
> 9	> 🔴 **ATUALIZAÇÃO 2026-06-20 — NÃO ESTÁ MAIS CONGELADO:** o dono LIBEROU o floor pela UI → trading REAL ON (`halted=false`). Canary **FARM-ONLY** (só as VENDAS do Farm armadas — saída no-loss dos lotes; COMPRAS off). Equity intacta ~$148,75 (USDT↔LTC, sem perda). SEMPRE confira `GET /system/halt` no início da sessão. **O bloco 🛑 abaixo (2026-06-15) é HISTÓRICO** — descreve o estado CONGELADO, já SUPERADO.
> 10	
> 11	> 🛑 **LEIA ANTES DE TUDO (2026-06-15):** o sistema está em **MAINNET REAL** (`settings.useTestnet=0`, ~$150 USDT) e **CONGELADO** (`TRADING_HALT=true` no `.env` → nada negocia; é o kill-switch novo no `exchange.js`). Money-path foi blindado (`96915e0`) e o bug P0 do Farm Sell foi corrigido (`c163112`). **DESCOBERTA CRÍTICA: o harvester está MORTO no mainnet** (o edge de −3% era arbitragem testnet-vs-mainnet; no mainnet o book do bot É o FAIR). O ÚNICO edge real é o **Trend** (pequeno, mensal). **Antes de descongelar:** (1) trava `FARM_SELLING` (follow-up); (2) dono confere saque-OFF+IP da chave Binance; (3) decidir re-design do harvester. Detalhes nos SEALs de 2026-06-15 (fim do doc) + memória `tradeux-mainnet-go-live`. **2026-06-16:** Cockpit Intelligence read-only NO AR (brain computa analytics 1m + agente lê/reporta; commit `1660871`) — a brain reporta **EV −0,16% / pHit 0,6%** (scalp 1m é −EV, dado real). Fix do **−1013** no `calcQty` + template Trend ×3 (commit `2528a5d`). **Auditoria adversarial independente** confirmou 7 achados p/ o descongelamento → ver SEAL 2026-06-16. ⚠️ O "vídeo viral Fable 5/Polymarket 205x" do X é **golpe de referral** — NÃO clicar/depositar.
> 12	
> 13	## ⚡ FIRST ACTION FOR NEXT AGENT
> 14	0. 🏗️ **ARQUITETURA FARM-AND-FUNNEL COMPLETA E NO AR** (sessão 2026-06-08): **15 automações ativas** — Farm no-loss +
> 15	   Trend SMA50/200 nas alts **LTC/BNB/ADA** (id 9-20) + id2/id6/id7 do BTC; **funil em SHADOW**; id3 pausada. Coordenação
> 16	   por regime (farm `!=trend`, trend `!=bear`). Validada por backtest (`backend/scripts/backtest-farm-funnel.js`) **e ao
> 17	   vivo**. Doc: `docs/STRATEGY-farm-funnel.md`. Memória `tradeux-farm-funnel-backtest`. **Hoje MERCADO=BEAR → tudo INERTE/protegido.**
> 18	   ⏰ **GATILHO (pedido do dono): QUANDO O REGIME SAIR DO BEAR / mercado propício → RETOMAR:** Fase 4 = **funil AO VIVO**
> 19	   (ligar a compra de BTC com o lucro real do farm, DEPOIS de observar o farm lucrar e calibrar o baseline com dado real);
> 20	   Fase 5 = **calibração** (5m + seleção de alts, SOL ruim no farm + switch macro fino — SMA-slope no regimeJob). Ver §5 do
> 21	   doc. **Checar o regime no boot:** `GET /analysis/regime-status` ou `logs/regime.log` — se != bear, é a hora.
> 22	   ✅ **ARMADOR DA FASE 4 NO AR** (commit `af22e7a`, 2026-06-09): o farm/trend já retomam sozinhos na saída do bear (gate
> 23	   runtime). O `regimeJob` agora detecta a borda `bear→não-bear` do macro (`FASE4_MACRO_SYMBOL`=BTCUSDT) → dispara
> 24	   `funnelJob.armFase4Observation()` = **notifica (telegram) + pré-arma o funil shadow (baseline) + janela densa de 4h**
> 25	   capturando o dado pra ESCREVER a Fase 4 (caixa USDT, reserva, lucro-desde-saída, escoamento; tag `[fase4-observe]` em
> 26	   `logs/funnel.log`). **NÃO compra** — a Fase 4 live-buy ainda não existe (money-path, gate). Quando o telegram avisar
> 27	   "🔔 [FASE4] Saída do BEAR", as 4h de captura bastam pra calibrar+escrever a compra ao vivo (com gate QA/TL). Memória `tradeux-farm-funnel-backtest`.
> 28	   ✅ **TELEGRAM FUNCIONA DE VERDADE desde 2026-06-10** (a raiz era chatId=username do bot → fix; `c3463ac` notifica TODAS
> 29	   as ordens + canal do agente `tradeux_notify_owner`) — o aviso "[FASE4]" CHEGA no dono. E o **HARVESTER está em size ×4**
> 30	   (`0b94b3a` reconcile-on-boot fechou a última dívida; janela de observação 2-3 dias → ×8). Memória `tradeux-telegram-notifications` + `tradeux-harvester-experiment`.
> 31	   ✅ **AGENTE RECALIBRADO (`12ceabe`)** pós-incidente de spam: doutrina POR MÓDULO (harvester=no-loss; **id7 corta perda
> 32	   POR DESENHO** — não tratar como bug), pt-BR obrigatório, kickoff injeta histórico de notificações (anti-repetição) +
> 33	   cap mecânico 2/ciclo. NÃO reescrever a doutrina sem reler `tradeux-telegram-notifications` (a regra "só vende com lucro"
> 34	   é literal SÓ pro harvester; gate de lucro na id7 = mudança de estratégia REFUTADA pelo backtest — não fazer via prompt).
> 35	1. **Backlog de PRs ZERADO** — modelo **trunk-based** (commit direto no `master` + push via token HTTPS).
> 36	2. 🎯 **META MUDOU: de 500k para +3 BTC (testnet)** — validar uma estratégia que faz +3 BTC; se 3, calibrar p/ 10+.
> 37	   Ver memória `tradeux-agent-500k-validation` (pivot) e `~/STRATEGY-3BTC-assessment.md`.
> 38	3. ✅ **OCO wiring no Beholder COMMITADO E NO AR** (commit `aa3f7f7`): template `type:'OCO'` → SELL protetiva
> 39	   (TP LIMIT_MAKER + SL STOP_LOSS_LIMIT), persiste 2 pernas c/ `orderListId` (migration), `listStatus` reconcile,
> 40	   guard anti-empilhamento, cancel no delete da automação. Gate QA+TL + testnet + CI verde.
> 41	4. ✅ **P&L mensurável + painel** (`d74fac0` net/avgPrice no insert de fills — ~74% das MARKET tinham net NULL;
> 42	   `9a5f989` Reports default USDT + end-date inclusivo + **leitura em BTC** "≈ X BTC"; `1fa6235` **painel
> 43	   Intelligence**: regime de mercado + KPIs do agente no UI). Todos com CI verde + validados no navegador.
> 44	5. ✅ **ENABLER Nº1 ENTREGUE & NO AR** (commit `30e6566`): `regimeJob` grava `MEMORY['<sym>:REGIME']`
> 45	   (string, via `updateMemory(...,executeAutomations=false)` = gate passivo) a cada 5min; `regimeService`
> 46	   compartilha fetch+classify+cache com o endpoint. **id2 (BUY) GATEADA ao vivo** (PATCH): condition
> 47	   `... && MEMORY['BTCUSDT:REGIME']!=='bear'` + `BTCUSDT:REGIME` nos indexes (fail-safe). id3 (SELL) intocada.
> 48	   Hoje BTC=bear → id2 **não compra** (validado). Gate QA+TL + testnet + lógica 9/9. ⚠️ ver "id2 gate" em
> 49	   Technical debt (NÃO é seedado → reaplicar após `make nuke`/reset).
> 50	6. ✅ **Classificador c/ histerese ENTREGUE** (commit `774ae42`): bandas entra/sai (bear >0.60/sai <0.45;
> 51	   trend 25/22; range 20/23), `prev` carregado pelo job. Gate da id2 mais estável e fail-safe (bear pegajoso).
> 52	   ±DI descartado por dados (piorava); MTF desnecessário (histerese já vence). Ganho é risco-ajustado de
> 53	   CARTEIRA, não alfa no BTC (ver task table). Observabilidade do gate ✅ (commit `e6c10dc`, card "Regime Gate" no
> 54	   painel). Calibração RSI ✅ (commit `0b1e949`): **RSI 25/75 aplicado na id2/id3** (domina 30/70 em retorno+drawdown
> 55	   em 1h E 1m). ✅ **Trend Following (SMA 50/200) ATIVADO** (commit `453c7d6`, gate QA PASS + TL APPROVE, CI verde):
> 56	   id6/id7 ativas + coordenação id2/id3 `!=trend` + **LIMIT marketável** (buffer 0.3%) + **persistência de cross** (`regimeStates`).
> 57	   ⏳ **NEXT**: (a) **observar 1 golden→death real** (`logs/A:6.log`/`A:7.log`) antes de calibrar o size (id6=3× MIN_NOTIONAL);
> 58	   (b) observar id2/id3 coordenadas ao longo do tempo; (c) ✅ **risco nº1 RESOLVIDO** (commit `e5ef595`: id7 usa `TREND_QTY`,
> 59	   não mais `LAST_ORDER`) — ⚠️ porém `TREND_QTY` é **volátil** (não persiste) → **persistir ANTES de escalar o size**;
> 60	   (d) opcional: hook de SIGTERM p/ stop().
> 61	7. Sanity no `/handson`: stack up na 8090 (**4 containers: db/backend/frontend/agent**), id2/id3 (coordenadas `!=trend`) + id6/id7 (trend) **ATIVAS**, símbolos
> 62	   synced, `GET /beholder/memory/BTCUSDT/REGIME` => `"bear"`. Trend ATIVO mas **inerte** agora (bear + above=false → sem disparo).
> 63	
> 64	## 🏁 Current state (what's live)
> 65	- **Stack DEPLOYED & healthy**: `tradeux-db/backend/frontend/agent` na 8090 (CloudPanel+Cloudflare).
> 66	  `https://tradeux.gcrux.com` → 200. Backend recriado com deps novas (twilio6/form-data4), boot limpo.
> 67	- **Agente LLM SUPERVISIONADO** (commit `e97a85a`): roda como serviço `agent` no compose (restart:unless-stopped,
> 68	  `user:1011:1013`, DRY/ALLOW_TRADING=false, OpenRouter nemotron `:free`); grava o journal que alimenta os KPIs do card
> 69	  "Agent (LLM)" em `/intelligence`. Antes era CLI manual → parava sem religar (ficou 5 dias parado). Religar/parar:
> 70	  `docker compose up -d agent` / `docker compose stop agent`.
> 71	- **Modelo de trabalho SELADO** (ver memória `tradeux-orchestration-model`): Claude é o ORQUESTRADOR —
> 72	  agentes worker implementam, QA+Tech-Lead são o gate; Claude **aprova OU devolve** e sobe pra prod.
> 73	  Sem PR-por-mudança. Gate proporcional: trivial→direto; hot-path/migration/segredo/dinheiro→gate.
> 74	- **Token GitHub**: em `~/tradeux/.env` como `GITHUB_TOKEN_API` (gitignored). Merge/push via API/HTTPS.
> 75	  ⚠️ é um PAT clássico admin-scope — trocar por fine-grained quando der (hardening).
> 76	- **PRs**: #10 (fix white-screen) e #11 (auto-sync) **MERGEADOS**; #1-7 (dependabot frontend)
> 77	  **fechados** (obsoletos pós-Vite); #9 (BYOK) **superseded** por commit direto; #12-15 (auto-PRs
> 78	  do Dependabot) **fechados como deferidos** (#12/#14 bundlam node-binance-api core → task; #13/#15
> 79	  vite/esbuild dev-only). **0 PRs abertos** — mas o Dependabot REABRE auto-PRs pras 6 moderate
> 80	  deferidas; fechar-como-deferido até o bump do node-binance-api / vite resolver na raiz.
> 81	- **Segurança**: backend runtime **8 → 2 moderate** (0 crit/0 high) após node-binance-api 1.x + `@sendgrid` 6→8
> 82	  (mata o `request`) + remoção do override form-data (commit 063df19). Restam 2 NÃO-exploráveis (`sequelize→uuid@8.3.2`,
> 83	  path `buf` não usado). O Dependabot pode mostrar mais (soma as 2 árvores incl. dev). Ver SECURITY.md.
> 84	- **BYOK**: chaves Binance opcionais no boot (seeder `|| ''` + setup.sh) — commit `9b91416`.
> 85	- **Backtest + regime**: harness walk-forward (`backend/scripts/backtest.js`) + detector
> 86	  (`backend/src/utils/regimeClassifier.js`) + relatórios (`backend/backtest-results/`). Ver Validation.
> 87	- **Baseline**: RSI 30/70 (BTCUSDT) — automations `id2`(buy<30)/`id3`(sell>70) **ACTIVE/armadas**.
> 88	- **Regime gate AO VIVO** (commit `30e6566`): `regimeJob` grava `MEMORY['BTCUSDT:REGIME']` (mainnet 1h, 5min);
> 89	  **id2 (BUY) gateada** `... && MEMORY['BTCUSDT:REGIME']!=='bear'` + `BTCUSDT:REGIME` nos indexes (fail-safe);
> 90	  id3 (SELL) sem gate (saída p/ caixa sempre liberada). Hoje BTC=**bear** → id2 não compra.
> 91	- **LLM agent**: `tradeux-agent`+`tradeux-mcp`, OpenRouter `nemotron-3-super-120b:free`, `ALLOW_TRADING=false`.
> 92	
> 93	## 📋 Task state
> 94	| Item | Status |
> 95	|---|---|
> 96	| Deploy stack / 502 / white-screen / auto-sync symbols | ✅ (mergeados #10/#11) |
> 97	| BYOK chaves opcionais no boot | ✅ (commit direto) |
> 98	| Segurança: critical + 8 high (twilio/form-data) | ✅ (28→6; gate QA+TL) |
> 99	| Backtest robusto walk-forward (1y, 4 símbolos, fee) | ✅ |
> 100	| Detector de regime: módulo + endpoint `/analysis/regime` + MCP `tradeux_get_regime` (Fase 1) | ✅ live (read-only, commit 0a97820) |
> 101	| Modelo de orquestração trunk-based selado | ✅ (memória) |
> 102	| `node-binance-api` 0.13→1.x (mata request via lib+@sendgrid; backend 8→2; OCO no wrapper) | ✅ (commit 063df19; gate+testnet) |
> 103	| OCO wiring no Beholder (template `type:'OCO'`, 2 pernas+`orderListId`, listStatus, anti-stacking) | ✅ (commit `aa3f7f7`; gate+testnet+CI) |
> 104	| P&L: net/avgPrice no insert de fills (~74% das MARKET tinham NULL → P&L furado) | ✅ (commit `d74fac0`; gate+testnet) |
> 105	| Reports: default USDT + end-date inclusivo + **leitura em BTC** (≈ X BTC) | ✅ (commit `9a5f989`; validado browser) |
> 106	| **Painel Intelligence** (regime de mercado + KPIs do agente no UI) — Fase B do dashboard | ✅ (commit `1fa6235`; validado browser) |
> 107	| Trava OCO=SELL no template + UX (E2E fixes) | ✅ (commit `d74fac0`) |
> 108	| **ENABLER Nº1**: regime→`MEMORY['<sym>:REGIME']` (job periódico) + **id2 (BUY) gateada** (`!= bear`) | ✅ (commit `30e6566`; gate QA+TL+testnet+CI; id2 via PATCH runtime) |
> 109	| Classificador de regime c/ **histerese** (anti-whipsaw) | ✅ (commit `774ae42`; gate QA+TL+backtest+testnet+CI). Bear pegajoso (sai só <0.45) = gate fail-safe. ±DI testado e DESCARTADO; MTF desnecessário. Ganho é de CARTEIRA (bear 26→6 flips, -32%→+0.6% agregado), **não alfa no BTC** (no BTC isolado V2 empata/atrasa). |
> 110	| **Calibração RSI/SMA** (backtest, retorno+maxDD agregado) | ✅ (`backtest.js` `--calibrate`, commit `0b1e949`; fix `MS_PER` 1m). **RSI 25/75 aplicado na id2/id3** (runtime/PATCH): domina 30/70 em retorno **E** drawdown em 1h E 1m (1m: 30/70 overtrada ~80 trades, fee corrói; 25/75 ~15-19). **SMA200 mantido** (melhor retorno). SMA-cross 50/200 = roadmap de trend. |
> 111	| **Trend Following (SMA 50/200)** — pipeline + ATIVAÇÃO | ✅ pipeline (commit `49af86a`) + ✅ **ATIVADO** (commit `453c7d6`; gate QA PASS + TL APPROVE; CI verde). Sinal da **MAINNET** (`regimeJob` detecta o cross → `MEMORY['<sym>:TREND_CROSS_1h']`, dispara 1x). **id6/id7 ATIVAS** + coordenação id2/id3 `!=trend` (REGIME nos indexes de ambas, fail-open corrigido) + templates 3/4 **LIMIT marketável** (buffer 0.3% no eval) + **persistência de cross** (`regimeStates`, resiliência a restart) + `validatePrice` no PATCH. Reprodutível: `setup-trend.js`+`activate-trend.js`. ⏳ Observar 1 cross real → calibrar size. |
> 112	
> 113	## 🎯 Validation plan → +3 BTC (testnet) — META NOVA (era 500k)
> 114	- **+3 BTC** = validar uma estratégia que cresce a carteira em 3 BTC (testnet); se valida 3, calibrar p/ 10+.
> 115	  No testnet (preços sintéticos) é **marco de mecânica/disciplina**, não alfa de mercado real.
> 116	- **Verdade dura do backtest (BTCUSDT 1h, net fee, bear 365d + bull 180d):** +3 BTC de **alfa absoluto** com
> 117	  long-only spot **NÃO sai de "trade esperto"** — bull→segurar ganha (B&H +134% vs regime +20%); bear→tudo perde
> 118	  mas o **caixa corta a perda** (regime −8% vs B&H −40%). Edge real = **drawdown menor via regime-gating**, não alfa.
> 119	  Calibração validada: RSI **25/75** (não 30/70), SMA **50/200** (não 20/50), menos trades. HFT é morto (fee+whipsaw).
> 120	  Rota p/ muitos BTC = **comprado no bull/trend, CAIXA no bear** + classificador bom + size pequeno + OCO. Doc:
> 121	  `~/STRATEGY-3BTC-assessment.md`. Painel `/intelligence` mostra o regime ao vivo (hoje BTC=bear/cash).
> 122	- (histórico 500k) = stress/validação, NÃO lucro (testnet fills sintético; reset ~mensal — persistir métricas).
> 123	- **Backtest de ciclo completo** (1h real, fee 0.1%/lado, walk-forward OOS, BTC/ETH/BNB/SOL):
> 124	  - **Bear (365d)**: B&H médio **-24%**; long-only não escapa; o edge é o **estado de CAIXA** (no BTC,
> 125	    regime-switch -7% vs B&H -27%). Regime-switch bate B&H em 1/4.
> 126	  - **Bull (2023-10→2024-04)**: B&H **+294%** ESMAGA tudo (regime +39%, trend +147%); bate B&H em 0/4.
> 127	  - **Lição honesta**: Buy&Hold é dificílimo de bater em retorno BRUTO; o valor do trading ativo é
> 128	    **risco-ajustado** (drawdown), não outperformance. HFT é matematicamente morto (fee+whipsaw).
> 129	- **Próximo edge**: classificador com **histerese** que FICA no bull e SAI no bear (ciclo completo,
> 130	  risco-ajustado) — é o trabalho do agente. Rodar `backtest.js` em mais janelas/símbolos.
> 131	
> 132	## 🧱 Technical debt / gotchas
> 133	- **GIT como gcrux-tradeux SEMPRE** (memória `git-ownership-gotcha`): git como `ubuntu` (mesmo read-only)
> 134	  cria arquivos `ubuntu` em `.git` e depois `gcrux-tradeux` não escreve `.git/objects` → commit falha.
> 135	  Fix: `sudo -n chown -R gcrux-tradeux:gcrux-tradeux .../.git`. Rodar git/docker-que-escreve-repo como gcrux.
> 136	- ✅ **`node-binance-api` 0.13→1.x feito** (063df19): é o **fork ccxt** (reescrita). Gotchas mapeados em
> 137	  `exchange.js`: `test:true` roteia o **ws-api de testnet** p/ o userData (senão autentica no mainnet); ordens
> 138	  via `binance.order(type,side,...)` (buy/sell 1.x quebram STOP via flags); `ohlc()`→`populateOHLC()`;
> 139	  `terminate()` por **URL completa** (1.x indexa subscriptions por url). **Quem matou o `request` foi o
> 140	  `@sendgrid` 6→8**, não só o node-binance (o sendgrid velho sustentava request por conta própria).
> 141	- **Regime classifier**: cru (ADX médio + SMA200 60%) é ruidoso (whipsaw no bull). Melhorar: multi-timeframe,
> 142	  histerese, +DI/-DI. Depois expor como MCP `tradeux_get_regime` + contexto no `SYSTEM_PROMPT` do agente.
> 143	- ✅ **lockfile v3** (regenerado em 063df19; override form-data removido — não há mais o que materializar).
> 144	- **OCO**: `oco()`/`cancelOrderList()` expostos no wrapper (endpoint `v3/orderList/oco`), validados em testnet
> 145	  (place+cancel, `ALL_DONE`). FALTA o **wiring no Beholder** (após buy anexar TP+SL; persistir `orderListId` —
> 146	  `orderModel` precisa de coluna/migration; tratar `listStatus` no userData stream). Task NEXT spawnada.
> 147	- **get_wallet bloated** (~193k tokens, junk testnet) e **free-model 429** seguem pendentes.
> 148	- **Logger por categoria** (memória nova): `logger('M:'+id)`→`logs/M<id>.log`, `logger('A:'+id)`→`logs/A<id>.log`,
> 149	  `'system'`→`system.log`. NÃO grepar só `system.log` p/ debug de monitor/automação (custou tempo no OCO).
> 150	- **OCO — ressalva conhecida (BAIXA, não corrigir já)**: o guard anti-empilhamento é **por automação**; 2 automações
> 151	  distintas no mesmo símbolo podem colocar 1 OCO cada (bounded). Fix futuro: índice único parcial `(automationId,symbol)`.
> 152	- **E2E achados abertos (E2E-REPORT)**: `/api/symbols` baixado 6–8×/página (lista enorme); App WS conecta 4–5×/página
> 153	  (leak por remontagem); gráfico TradingView mostra preço **mainnet** vs backend testnet; ordens MARKET às vezes EXPIRAM
> 154	  no testnet (book fino); `res.json(err.body)` manda corpo vazio em erro de ordem (sem msg na UI). Tudo BAIXA/MÉDIA.
> 155	- **net flip-flop (BAIXA)**: o `executionReport` (3s) reescreve net/avgPrice já gravados no insert (DECIMAL→string vs
> 156	  number no `!==`) → 1 UPDATE + notificação redundantes, inócuo aos dados. Alinhar formato se incomodar.
> 157	- ⚠️ **id2/id3 são RUNTIME (não seedados) — REAPLICAR após `make nuke`/reset do testnet**: NÃO estão nos seeders
> 158	  (só "Example Strategy" inativa é seedada). Estado VIVO atual (gate + RSI 25/75 calibrado):
> 159	  - id2 (BUY): `indexes="BTCUSDT:RSI_14_1m,BTCUSDT:REGIME"` · `conditions="MEMORY['BTCUSDT:RSI_14_1m'].current<25 && MEMORY['BTCUSDT:REGIME']!=='bear'"`
> 160	  - id3 (SELL): `indexes="BTCUSDT:RSI_14_1m"` · `conditions="MEMORY['BTCUSDT:RSI_14_1m'].current>75"`
> 161	  - **Revert do gate** (não da RSI): id2 → `indexes="BTCUSDT:RSI_14_1m"` / `conditions="...current<25"`. **Revert da RSI**: voltar 25→30 / 75→70. Ver memória `tradeux-regime-gate`.
> 162	- **Regime job — dívida diferida (BAIXA)**: (a) sem hook de SIGTERM chamando `regimeJob.stop()` (inócuo: `timer.unref()`).
> 163	  (b) ✅ **RESOLVIDO** (commit `e6c10dc`): `getStatus()` exposto em `GET /analysis/regime-status` + card "Regime Gate"
> 164	  no painel `/intelligence` (regime do gate por símbolo + idade + STALE + auto-refresh 60s) → halt silencioso e
> 165	  divergência display×gate agora visíveis. Env: `REGIME_JOB_ENABLED` (kill-switch), `REGIME_REFRESH_MS` (5min),
> 166	  `REGIME_INTERVAL` (1h), `REGIME_SYMBOLS` (CSV).
> 167	- ✅ **Trend Following — ATIVADO** (commit `453c7d6`, gate QA PASS + TL APPROVE, CI verde) via `node backend/scripts/activate-trend.js`:
> 168	  (1) ✅ **coordenação** id2/id3 `&& MEMORY['BTCUSDT:REGIME']!=='trend'` (REGIME nos indexes de AMBAS; id3 ganhou REGIME → **fail-open
> 169	  corrigido**); (2) ✅ **order type** MARKET→**LIMIT marketável** (buffer 0.3% no eval do `limitPrice` pois `limitPriceMultiplier` é
> 170	  DECIMAL(10,2); + `validatePrice` no `updateOrderTemplate`); (3) ✅ **resiliência a restart**: tabela `regimeStates` (PK=symbol,
> 171	  carregada no boot ANTES do 1º poll → cross não se perde no `make restart`). ⏳ **RESTA**: (a) observar **1 golden→death real**
> 172	  (`A:6.log`/`A:7.log`) antes de calibrar; (b) **sizing** id6=3× MIN_NOTIONAL (pequeno p/ observar) → subir depois; (c) ✅ **risco
> 173	  nº1 RESOLVIDO** (commit `e5ef595`): id7 usa **`TREND_QTY`** (posição acumulada via `app-em.updateTrendPosition` no fill: golden
> 174	  soma, death zera; dedup por orderId + guard NaN; `calcQty` capa na carteira + falha-fechado se 0). ⚠️ **`TREND_QTY` é VOLÁTIL**
> 175	  (só MEMORY, ≠ `regimeStates`) → **persistir ANTES de escalar o size** (restart c/ posição aberta = id7 dá throw, não liquida no
> 176	  death); (d) at-least-once: crash entre fire e upsert pode re-disparar 1 cross no boot (ok p/ size pequeno). Reaplicar após
> 177	  `make nuke` (id2/id3/id6/id7 são runtime): `setup-trend.js` + `activate-trend.js`.
> 178	- **Agente LLM — serviço supervisionado** (commit `e97a85a`; gate QA PASS + TL APPROVE): roda no compose (`agent`,
> 179	  restart:unless-stopped, `user:1011:1013`, mem 384M, journal `/journal` rw; backend lê `:ro`). Religar/parar:
> 180	  `docker compose up -d agent` / `docker compose stop agent`. Dívidas (não-bloqueantes): (a) **429 do modelo `:free`** → o
> 181	  ciclo falha e re-tenta a cada 5min (NÃO é crash-loop; o card marca STALE) — roadmap: backoff/kill-switch
> 182	  `TRADEUX_AGENT_ENABLED` espelhando `REGIME_JOB_ENABLED`; (b) o `agent` precisa de `tradeux-agent/.env` (o `setup.sh` só gera
> 183	  o `.env` raiz) → numa máquina nova ele reinicia até o `.env` existir; (c) `tradeux-agent/journal/` é gitignored → após
> 184	  `make nuke`/máquina nova, garantir o DIR como gcrux antes do 1º `up` (com `user:` os ARQUIVOS já nascem gcrux, mas o Docker
> 185	  cria o DIR ausente como root); (d) threshold STALE do card é fixo (15min = 3× o ciclo de 5min); (e) `npm install` (não `ci`).
> 186	- **Agente — prompt alinhado à Farm-and-Funnel** (commit `a0869c4`; gate QA PASS + TL APPROVE): copiloto OBSERVADOR (BTC=cofre nunca
> 187	  vende; automações executam, ele só aconselha); `MAX_TOOL_ROUNDS` 12→20 (código default + .env). Dívidas/gates de liberação:
> 188	  (a) ✅ **RESOLVIDO (commit `9898bdf`, gate QA PASS + TL APPROVE)** — trava determinística e FAIL-CLOSED de SELL-BTC no
> 189	  `tradeux_place_order` (MCP): `isBtcVaultSymbol` barra SELL de TODO símbolo que começa com "BTC" (exceto prefixos não-base
> 190	  BTCUP/BTCDOWN/BTCST), então pares BTC<quote> NOVOS nascem bloqueados sem manutenção de lista — a allowlist de quotes anterior
> 191	  falhava ABERTO (QA enumerou 5 ao vivo escapando: USDS/USD1/EURI/IDR/U). `automationId` obrigatório foi AVALIADO e DESCARTADO
> 192	  (ordens do agente são manuais por design; forçar id falso corrompe P&L em groupByAutomations e não é mutex — doc no código).
> 193	  Teste de regressão hermético (21 casos) + `npm test` + step no CI. **Follow-ups NÃO-bloqueantes (dos gates):** (i) o backend
> 194	  `ordersController.placeOrder` NÃO tem trava equivalente → ordens de UI/outro cliente MCP não passam por ela; mover a defesa p/ o
> 195	  backend se o modelo de ameaça do flip incluir "qualquer caminho com as chaves da conta"; (ii) a premissa "agente BTCUSDT-only" está
> 196	  ERRADA — o SYSTEM_PROMPT autoriza FARM de alts (LTC/BNB/ADA) vs USDT (NÃO quebra a trava: alts não começam com "BTC"); (iii) resíduo
> 197	  fora de escopo: BUY de par BTC-quote (ex.: BUY ETHBTC) também drena o cofre (agente não negocia pares BTC-quote). (b) ✅ **`get_memory_indexes` RESOLVIDO (commit `2d01002`)** via `leanMemoryIndexes`
> 198	  (SEM símbolo: resumo compacto = variáveis distintas + símbolos, sem eval/example; COM símbolo: chaves detalhadas só do par; cap
> 199	  `MCP_MEMORY_INDEXES_SYMBOL_CAP` default 60) — eliminou o ~192k tok / 400 context-overflow. **Ainda ABERTO** o mesmo enxugamento p/
> 200	  `get_memory` (sem símbolo → MEMORY inteira) e `get_wallet_full`. O SYSTEM_PROMPT ainda proíbe a tool (contorno antigo) → pode
> 201	  reabilitá-la agora. Raiz no MCP, mesma classe do get_wallet bloat.
> 202	
> 203	## 🔑 Key paths & commands
> 204	- Repo: `/home/gcrux-tradeux/tradeux` · shell é `ubuntu`, **agir como `sudo -n -u gcrux-tradeux`** (inclusive git/docker).
> 205	- Token: `GITHUB_TOKEN_API` no `.env`. Push: `git push https://x-access-token:$TOKEN@github.com/gabrielZarattini/tradeux.git HEAD:master` (NÃO persistir em .git/config).
> 206	- Deploy: `cd ~/tradeux && ./setup.sh` (= `make up`); `make logs/ps/restart`; `make nuke` apaga o volume do DB.
> 207	- Backtest: `node backend/scripts/backtest.js --days=365` (bear) · `--days=180 --end=2024-04-01` (bull).
> 208	  Regime ao vivo: `node backend/src/utils/regimeClassifier.js BTCUSDT 1h 20`. (rodar em container node + technicalindicators.)
> 209	- Agent: container na rede `tradeux_tradeux` (ver memória `tradeux-agent-500k-validation`).
> 210	- Memory: `/home/ubuntu/.claude/projects/-home-gcrux-tradeux/memory/`.
> 211	
> 212	---
> 213	
> 214	## 📝 Session Records (newest last)
> 215	
> 216	### Record — 2026-06-03 (Validation phase) — [resumo abreviado]
> 217	Deploy do stack + fix 502, white-screen, auto-sync symbols, agente LLM, RSI baseline, stop-loss/OCO
> 218	validados, backtest v1 (não persistido), ShakeHands + agentes QA/Tech-Lead. (Detalhe nos commits.)
> 219	
> 220	### Record — 2026-06-03 (cont. — merges, segurança, backtest, modelo de trabalho)
> 221	Sessão grande. (1) **Re-rodei o gate** nos 2 PRs e descobri que não eram PRs reais (só branches) —
> 222	**criei+mergeei #10/#11** via API (token novo no `.env`). Triei os 8 PRs restantes: **fechei #1-7**
> 223	(dependabot frontend obsoletos pós-Vite) e **superseded #9** (BYOK) aplicando o equivalente direto no
> 224	master. **Backlog de PRs = 0.** (2) **Selei o modelo trunk-based** (Claude orquestra+aprova/devolve+sobe;
> 225	gate proporcional) — memória `tradeux-orchestration-model`. (3) **Segurança**: Dependabot **28→6**
> 226	(critical+8 high zerados via twilio 3→6 + override form-data), com gate QA+Tech-Lead, backend recriado
> 227	em prod, boot limpo; `node-binance-api` 0.13→1.x deferido (task spawnada, destrava OCO). SECURITY.md
> 228	atualizado. (4) **Backtest de ciclo completo** (bear 365d + bull 2024) + **detector de regime**
> 229	(`regimeClassifier.js`, testado: BTC→bear/cash) — achado honesto: **Buy&Hold é dificílimo de bater em
> 230	retorno bruto; o edge do trading ativo é risco-ajustado (drawdown), não outperformance; HFT é morto.**
> 231	Próximo: classificador com histerese + wiring no agente; bump do node-binance-api.
> 232	
> 233	### Record — 2026-06-03 (cont. — regime wiring + dashboard de agente + /handoff)
> 234	Continuei do "comece". (1) **Regime Fase 1 ✅ live**: endpoint `GET /api/analysis/regime/:symbol` (klines
> 235	mainnet, cache 2min, regime = estado real do mercado) + MCP `tradeux_get_regime`; gate QA+Tech-Lead (ressalva
> 236	MÉDIA do QA corrigida: `limit=300` + guard de dados insuficientes); testado ao vivo (BTC/ETH→bear/cash); commit
> 237	`0a97820`, backend recriado, boot limpo. (2) **E2E no browser** (Claude-in-Chrome): login→dashboard, chart BTC
> 238	vivo + RSI, App WS conectado, **zero console errors**, Orders com 27 ordens BTCUSDT (19 buy / 7 sell — baseline
> 239	acumulando na queda, confirma o backtest). (3) **Carteira testnet** ~US$285k é RUÍDO (445 faucet coins a preço
> ```

## 🤖 Claude *(13:55:44)*

Let me read the rest of exchange.js around the equity logic, plus riskState.js and dailyCapJob.js.

## 🤖 Claude *(13:55:45)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/src/riskState.js"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	'use strict';
> 2	
> 3	// === riskState — FONTE ÚNICA DE VERDADE do kill-switch (HALT) ===
> 4	//
> 5	// O guard (utils/exchange.js) chama isHalted() POR ORDEM (HALT QUENTE). Fontes EMPILHÁVEIS (basta UMA p/ travar tudo):
> 6	//   env-hard  → override ABSOLUTO derivado de process.env.TRADING_HALT_HARD no boot. NÃO é flipável em runtime
> 7	//               (só `.env` + restart). É a trava "à prova de clique" — quando você quer o sistema travado de
> 8	//               verdade, imune ao botão da UI. Default OFF.
> 9	//   floor     → PISO OPERACIONAL de ir-ao-vivo, PERSISTIDO (risk_state.json), controlado pelo OPERADOR via UI
> 10	//               (POST /system/floor), QUENTE (sem restart) e sobrevive a restart. SEED no 1º boot:
> 11	//               process.env.TRADING_HALT (compat com o antigo "env floor"). Depois de persistido o OPERADOR é a
> 12	//               autoridade — o env TRADING_HALT vira só semente (use o botão TRAVAR, ou TRADING_HALT_HARD, p/ travar).
> 13	//   manual    → kill-switch quente do operador / pânico (POST /system/halt). Persistido; sobrevive a restart.
> 14	//   daily-cap → disparado pelo dailyCapJob no drawdown de equity do dia. Persistido; AUTO-EXPIRA na virada UTC.
> 15	//
> 16	// SEM dependência do app (só fs/path/logger) → exchange.js requer este módulo top-level sem ciclo. FAIL-CLOSED:
> 17	// disco ilegível → floor LIGADO (trava); isHalted() lançar → o guard lança = ordem bloqueada (direção segura).
> 18	//
> 19	// ⚠️ MUDANÇA DE POSTURA (2026-06-19): o "env floor" antigo (TRADING_HALT, OR permanente, só .env+restart) virou um
> 20	// PISO PERSISTIDO controlável pela UI (a quente). TRADING_HALT agora só SEMENTE o floor no 1º boot; pra travar
> 21	// "à prova de clique" use TRADING_HALT_HARD=true no .env. Botão de liberar (UI) é bloqueado se env-hard estiver on.
> 22	
> 23	const fs = require('fs');
> 24	const path = require('path');
> 25	const logger = require('./utils/logger');
> 26	
> 27	const STATE_FILE = path.resolve(__dirname, '..', 'logs', 'risk_state.json');
> 28	
> 29	// env-hard: override absoluto (só .env+restart). env-seed: semente do floor no 1º boot (compat com o antigo env floor).
> 30	const ENV_HALT_HARD = process.env.TRADING_HALT_HARD === 'true';
> 31	const ENV_FLOOR_SEED = process.env.TRADING_HALT === 'true';
> 32	
> 33	// Estado mutável das fontes QUENTES (persistidas). env-hard NÃO entra aqui (não é persistido nem flipável).
> 34	let floor = { on: ENV_FLOOR_SEED, reason: ENV_FLOOR_SEED ? 'TRADING_HALT (semente env, 1º boot)' : null, since: null };
> 35	let manual = { on: false, reason: null, since: null };
> 36	let dailyCap = { on: false, reason: null, since: null, day: null };
> 37	
> 38	// Equity tradeable QUENTE — publicado pelo dailyCapJob a cada ciclo `valued` (~60s, mark-to-market, fail-safe).
> 39	// Lido SÍNCRONO pelo guard (utils/exchange.assertWithinRisk) p/ dimensionar o %-teto de COMPRA. NÃO persistido
> 40	// (recomputado em <=60s no boot) e NÃO entra no isHalted() — é só um número p/ o teto. value=null até o 1º cálculo
> 41	// válido; equity ausente/velho faz o guard degradar p/ o teto absoluto (direção segura).
> 42	let equitySnap = { value: null, at: null };
> 43	function setEquity(v) {
> 44	    const n = parseFloat(v);
> 45	    if (Number.isFinite(n) && n > 0) equitySnap = { value: n, at: Date.now() };
> 46	}
> 47	function getEquity() { return { value: equitySnap.value, at: equitySnap.at }; }
> 48	
> 49	// Chave de dia UTC YYYY-MM-DD (NÃO getUTCDate() — evita aliasing dia-do-mês na virada de mês).
> 50	function dayKeyUTC(d) {
> 51	    return (d || new Date()).toISOString().slice(0, 10);
> 52	}
> 53	
> 54	function persist() {
> 55	    try {
> 56	        const dir = path.dirname(STATE_FILE);
> 57	        if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
> 58	        fs.writeFileSync(STATE_FILE, JSON.stringify({ floor, manual, dailyCap }), 'utf8');
> 59	    } catch (e) {
> 60	        logger('system', `[riskState] falha ao persistir ${STATE_FILE}: ${e.message}`);
> 61	    }
> 62	}
> 63	
> 64	// Carrega o estado quente do disco no boot. floor PERSISTIDO vence a semente do env (autoridade do operador após o
> 65	// 1º flip); ausente → mantém a semente. manual re-arma como estava; dailyCap só se for do MESMO dia UTC.
> 66	function loadFromDisk() {
> 67	    try {
> 68	        if (!fs.existsSync(STATE_FILE)) return;
> 69	        const raw = JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
> 70	        if (raw && raw.floor && typeof raw.floor.on === 'boolean') floor = raw.floor;
> 71	        if (raw && raw.manual && typeof raw.manual.on === 'boolean') manual = raw.manual;
> 72	        if (raw && raw.dailyCap && typeof raw.dailyCap.on === 'boolean') {
> 73	            if (raw.dailyCap.on && raw.dailyCap.day === dayKeyUTC()) dailyCap = raw.dailyCap;
> 74	            else dailyCap = { on: false, reason: null, since: null, day: null }; // dia diferente → expira
> 75	        }
> 76	    } catch (e) {
> 77	        // FAIL-CLOSED: disco ilegível → trava pelo floor (não libera no escuro). manual/cap zerados.
> 78	        logger('system', `[riskState] estado em disco ilegível (${e.message}) — FAIL-CLOSED (floor LIGADO).`);
> 79	        floor = { on: true, reason: 'fail-safe (estado em disco ilegível)', since: null };
> 80	        manual = { on: false, reason: null, since: null };
> 81	        dailyCap = { on: false, reason: null, since: null, day: null };
> 82	    }
> 83	}
> 84	
> 85	// HALT efetivo: qualquer fonte ligada trava. dailyCap só conta no DIA em que foi armado.
> 86	function isHalted() {
> 87	    return ENV_HALT_HARD || floor.on || manual.on || (dailyCap.on && dailyCap.day === dayKeyUTC());
> 88	}
> 89	
> 90	// Estado completo p/ reporte (cockpit/agent/endpoint/painel). `source`/`reason` resolvem por PRECEDÊNCIA
> 91	// (env-hard > floor > manual > daily-cap) p/ rotular a causa dominante; `sources` lista TODAS as ativas.
> 92	function getState() {
> 93	    const today = dayKeyUTC();
> 94	    const capActive = dailyCap.on && dailyCap.day === today;
> 95	    const sources = [];
> 96	    if (ENV_HALT_HARD) sources.push('env-hard');
> 97	    if (floor.on) sources.push('floor');
> 98	    if (manual.on) sources.push('manual');
> 99	    if (capActive) sources.push('daily-cap');
> 100	
> 101	    let source = null, reason = null, since = null;
> 102	    if (ENV_HALT_HARD) { source = 'env-hard'; reason = 'TRADING_HALT_HARD (env, absoluto)'; since = null; }
> 103	    else if (floor.on) { source = 'floor'; reason = floor.reason || 'piso operacional'; since = floor.since; }
> 104	    else if (manual.on) { source = 'manual'; reason = manual.reason || 'operador'; since = manual.since; }
> 105	    else if (capActive) { source = 'daily-cap'; reason = dailyCap.reason || 'daily-loss-cap'; since = dailyCap.since; }
> 106	
> 107	    return {
> 108	        halted: isHalted(),
> 109	        envHard: ENV_HALT_HARD,
> 110	        floor: { ...floor },
> 111	        manual: { ...manual },
> 112	        dailyCap: { ...dailyCap, active: capActive },
> 113	        sources, source, reason, since,
> 114	    };
> 115	}
> 116	
> 117	// Liga/desliga o PISO OPERACIONAL (persistido, quente). on=true TRAVA; on=false LIBERA (ir ao vivo c/ dinheiro
> 118	// real). NÃO toca env-hard nem manual/daily-cap. Retorna true se mudou. O bloqueio por env-hard é responsabilidade
> 119	// do chamador (systemController recusa liberar se envHard) — aqui setFloor(false) só mexe na fonte floor.
> 120	function setFloor(on, reason) {
> 121	    on = !!on;
> 122	    if (floor.on === on) return false;
> 123	    floor = on ? { on: true, reason: reason || 'operador', since: new Date().toISOString() }
> 124	               : { on: false, reason: null, since: null };
> 125	    persist();
> 126	    logger('system', `[riskState] FLOOR ${on ? 'LIGADO (trava)' : 'DESLIGADO (trading liberado)'}${on && reason ? ` (${reason})` : ''}.`);
> 127	    return true;
> 128	}
> 129	
> 130	// Liga/desliga uma fonte QUENTE. source ∈ {'manual','daily-cap'}. Retorna `true` se MUDOU. NUNCA toca floor/env.
> 131	function setHalt(on, reason, source) {
> 132	    on = !!on;
> 133	    if (source === 'manual') {
> 134	        if (manual.on === on) return false;
> 135	        manual = on ? { on: true, reason: reason || 'operador', since: new Date().toISOString() }
> 136	                    : { on: false, reason: null, since: null };
> 137	        persist();
> 138	        logger('system', `[riskState] manual HALT ${on ? 'LIGADO' : 'desligado'}${on && reason ? ` (${reason})` : ''}.`);
> 139	        return true;
> 140	    }
> 141	    if (source === 'daily-cap') {
> 142	        const today = dayKeyUTC();
> 143	        if (on) {
> 144	            if (dailyCap.on && dailyCap.day === today) return false; // já armado hoje → não re-notifica
> 145	            dailyCap = { on: true, reason: reason || 'daily-loss-cap', since: new Date().toISOString(), day: today };
> 146	            persist();
> 147	            logger('system', `[riskState] daily-cap HALT ARMADO (${dailyCap.reason}).`);
> 148	            return true;
> 149	        }
> 150	        return clearDailyCap();
> 151	    }
> 152	    throw new Error(`[riskState] setHalt: source inválida '${source}' (use 'manual' ou 'daily-cap').`);
> 153	}
> 154	
> 155	// Zera SÓ a fonte daily-cap (rollover de dia e reset do operador). Nunca toca floor/env/manual.
> 156	function clearDailyCap() {
> 157	    if (!dailyCap.on) return false;
> 158	    dailyCap = { on: false, reason: null, since: null, day: null };
> 159	    persist();
> 160	    logger('system', `[riskState] daily-cap HALT limpo (re-armado p/ o dia).`);
> 161	    return true;
> 162	}
> 163	
> 164	// Dia em que o daily-cap está armado (null se não armado) — o dailyCapJob usa p/ saber se já disparou hoje.
> 165	function getDailyCapDay() {
> 166	    return dailyCap.on ? dailyCap.day : null;
> 167	}
> 168	
> 169	// Seed no LOAD do módulo (try/catch já dentro de loadFromDisk; fail-closed).
> 170	loadFromDisk();
> 171	logger('system', `[riskState] inicializado — env-hard=${ENV_HALT_HARD} · floor=${floor.on} · manual=${manual.on} · daily-cap=${dailyCap.on}${dailyCap.on ? ` (${dailyCap.day})` : ''} · halted=${isHalted()}.`);
> 172	
> 173	module.exports = { dayKeyUTC, isHalted, getState, setFloor, setHalt, clearDailyCap, getDailyCapDay, setEquity, getEquity };
> 174	
> ```

## 🤖 Claude *(13:55:46)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "find /home/gcrux-tradeux/tradeux/backend -name 'dailyCapJob.js' 2>/dev/null",
  "description": "Locate dailyCapJob.js"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrux-tradeux/tradeux/backend/src/dailyCapJob.js
> ```

## 🤖 Claude *(13:55:48)*

Now let me read the full dailyCapJob.js to understand the lifecycle, the alarm logic, and the setEquity call.

## 🤖 Claude *(13:55:49)*


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
> 174	        // Publica o equity QUENTE p/ o %-teto de COMPRA (utils/exchange.assertWithinRisk). Só em ciclo `valued`
> 175	        // (acima já retornamos no fail-safe), então o guard nunca dimensiona a compra por um equity frio.
> 176	        // ⚠️ NÃO mover esta linha p/ ACIMA do early-return do fail-safe (linha ~155): publicaria equity de
> 177	        // cálculo incompleto e o %-teto passaria a dimensionar por lixo.
> 178	        riskState.setEquity(eq.equity);
> 179	
> 180	        // 3) Baseline do dia ausente (boot mid-day ou pós-rollover): snapshota AGORA e encerra o ciclo.
> 181	        if (!SNAP || SNAP.day !== today) {
> 182	            SNAP = { day: today, equity: eq.equity, at: new Date().toISOString() };
> 183	            saveSnap();
> 184	            logger('system', `[dailyCap] baseline do dia ${today} = $${eq.equity.toFixed(2)} (USDT livre $${eq.usdtFree.toFixed(2)}).`);
> 185	            return;
> 186	        }
> 187	
> 188	        // 4) Avalia o drawdown. Piso = baseline × (1 - CAP_PCT). Equity <= piso → ARMA o HALT (idempotente).
> 189	        const floor = SNAP.equity * (1 - CAP_PCT);
> 190	        if (eq.equity <= floor) {
> 191	            const ddPct = ((eq.equity / SNAP.equity) - 1) * 100;
> 192	            const reason = `daily-loss-cap -${(CAP_PCT * 100).toFixed(0)}% (equity $${eq.equity.toFixed(2)} <= piso $${floor.toFixed(2)}; baseline $${SNAP.equity.toFixed(2)}, dd ${ddPct.toFixed(2)}%)`;
> 193	            const tripped = riskState.setHalt(true, reason, 'daily-cap');
> 194	            if (tripped) {
> 195	                logger('system', `[dailyCap] 🛑 CAP DISPARADO — ${reason}. HALT ativo (bloqueia TODAS as ordens).`);
> 196	                await notify(eq.settings,
> 197	                    `🛑 [DAILY_CAP] Cap diário de -${(CAP_PCT * 100).toFixed(0)}% ATINGIDO!\n` +
> 198	                    `Equity $${eq.equity.toFixed(2)} (baseline $${SNAP.equity.toFixed(2)}, ${ddPct.toFixed(2)}%).\n` +
> 199	                    `🚫 HALT ativo: TODAS as ordens bloqueadas (inclusive venda protetiva). ` +
> 200	                    `Intervenção manual necessária — reabra via /system/halt ou aguarde a virada de dia UTC.`);
> 201	            }
> 202	        }
> 203	    } catch (err) {
> 204	        logger('system', `[dailyCap] erro no ciclo: ${err.message}`);
> 205	    } finally {
> 206	        running = false;
> 207	    }
> 208	}
> 209	
> 210	// Re-snapshot forçado (usado pelo reset do operador): re-baseline com o equity atual p/ não re-disparar
> 211	// contra um baseline velho logo após o reset. Não dispara nada. Retorna { ok, snapshot, reason }.
> 212	async function reSnapshot() {
> 213	    if (running) return { ok: false, reason: 'ciclo do cap em andamento — tente de novo em instantes', snapshot: SNAP };
> 214	    running = true; // serializa com checkCap (evita race na escrita de SNAP)
> 215	    try {
> 216	        const eq = await computeEquity();
> 217	        if (!eq.valued) return { ok: false, reason: eq.error || `preços frios: ${(eq.cold || []).join(', ')}`, snapshot: SNAP };
> 218	        riskState.setEquity(eq.equity); // re-baseline manual também atualiza o equity quente do %-teto
> 219	        SNAP = { day: riskState.dayKeyUTC(), equity: eq.equity, at: new Date().toISOString() };
> 220	        saveSnap();
> 221	        logger('system', `[dailyCap] re-baseline manual = $${eq.equity.toFixed(2)} (${SNAP.day}).`);
> 222	        return { ok: true, snapshot: SNAP };
> 223	    } catch (err) {
> 224	        return { ok: false, reason: err.message, snapshot: SNAP };
> 225	    } finally {
> 226	        running = false;
> 227	    }
> 228	}
> 229	
> 230	function start() {
> 231	    if (!ENABLED) { logger('system', '[dailyCap] DESABILITADO (DAILY_CAP_ENABLED=false).'); return; }
> 232	    if (timer) return; // idempotente
> 233	    loadSnap();
> 234	    checkCap(); // primeira passada no boot (provável fail-safe se MINI_TICKER ainda frio — esperado)
> 235	    timer = setInterval(checkCap, CHECK_MS);
> 236	    if (timer.unref) timer.unref();
> 237	    logger('system', `[dailyCap] iniciado — teto -${(CAP_PCT * 100).toFixed(0)}% sobre o equity do dia (intervalo ${CHECK_MS}ms).`);
> 238	}
> 239	
> 240	function stop() {
> 241	    if (timer) { clearInterval(timer); timer = null; }
> 242	    running = false;
> 243	}
> 244	
> 245	function getStatus() {
> 246	    const st = riskState.getState();
> 247	    return {
> 248	        enabled: ENABLED, capPct: CAP_PCT, checkMs: CHECK_MS,
> 249	        snapshot: SNAP, last: LAST,
> 250	        floor: SNAP ? SNAP.equity * (1 - CAP_PCT) : null,
> 251	        tripped: st.dailyCap, halted: st.halted, haltSource: st.source,
> 252	        running, at: AT ? new Date(AT).toISOString() : null, ageMs: AT ? Date.now() - AT : null,
> 253	    };
> 254	}
> 255	
> 256	module.exports = { start, stop, checkCap, reSnapshot, getStatus };
> 257	
> ```

## 🤖 Claude *(13:55:55)*

Now I have the full picture. Let me verify the claims one by one. The finding has several specific claims about line numbers and behavior. Let me check:

1. `EQUITY_MAX_AGE_MS=600000` (10min) — confirmed at exchange.js:47-48.
2. `freshEquity()` returns null after staleness — confirmed at exchange.js:64-69.
3. `setEquity` only called by dailyCapJob:178 (and reSnapshot:218).
4. The cold-alert covers "equity inavaliável" but NOT "job dead/stopped".
5. equitySnap not persisted.

Let me verify the cold-alert logic more carefully and check whether there is any independent staleness alarm. The key claim: if the job dies/hangs, the cold-alert never fires because `checkCap` never runs. Let me also verify the `running` flag deadlock scenario and any SIGTERM/error-recovery.

## 🤖 Claude *(13:55:57)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && grep -rn \"setEquity\\|getEquity\\|freshEquity\\|EQUITY_MAX_AGE\\|equitySnap\" backend/src/ backend/scripts/ 2>/dev/null",
  "description": "Find all setEquity/getEquity/freshEquity references"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> backend/src/riskState.js:42:let equitySnap = { value: null, at: null };
> backend/src/riskState.js:43:function setEquity(v) {
> backend/src/riskState.js:45:    if (Number.isFinite(n) && n > 0) equitySnap = { value: n, at: Date.now() };
> backend/src/riskState.js:47:function getEquity() { return { value: equitySnap.value, at: equitySnap.at }; }
> backend/src/riskState.js:173:module.exports = { dayKeyUTC, isHalted, getState, setFloor, setHalt, clearDailyCap, getDailyCapDay, setEquity, getEquity };
> backend/src/dailyCapJob.js:178:        riskState.setEquity(eq.equity);
> backend/src/dailyCapJob.js:218:        riskState.setEquity(eq.equity); // re-baseline manual também atualiza o equity quente do %-teto
> backend/src/utils/exchange.js:31://                                  (> EQUITY_MAX_AGE_MS) → a % é ignorada e cai-se pro teto absoluto (degrada seguro).
> backend/src/utils/exchange.js:47:const _eqMaxAge = parseInt(process.env.EQUITY_MAX_AGE_MS || '600000', 10);
> backend/src/utils/exchange.js:48:const EQUITY_MAX_AGE_MS = Number.isFinite(_eqMaxAge) && _eqMaxAge > 0 ? _eqMaxAge : 600000; // equity mais velho que isto → cai pro teto absoluto
> backend/src/utils/exchange.js:65:function freshEquity() {
> backend/src/utils/exchange.js:66:    const eq = (riskState.getEquity && riskState.getEquity()) || null;
> backend/src/utils/exchange.js:67:    if (eq && Number.isFinite(eq.value) && eq.value > 0 && eq.at && (Date.now() - eq.at) <= EQUITY_MAX_AGE_MS) return eq.value;
> backend/src/utils/exchange.js:88:            const eqv = freshEquity();
> backend/src/utils/exchange.js:105:        const eqv = freshEquity();
> backend/src/utils/exchange.js:400:    const eqv = freshEquity();
> backend/scripts/sim/riskGuard.test.js:34:    getEquity: () => ({ value: EQUITY.value, at: EQUITY.at }),
> backend/scripts/sim/riskGuard.test.js:40:// equity fresco (agora) e velho (além do EQUITY_MAX_AGE_MS default de 10min).
> backend/scripts/sim/dailyCap.test.js:29:let lastEquityPub = null;     // captura riskState.setEquity(v) — o dailyCapJob publica o equity quente p/ o %-teto
> backend/scripts/sim/dailyCap.test.js:34:    setEquity: (v) => { lastEquityPub = v; },
> backend/scripts/sim/dailyCap.test.js:68:    check('publica o equity QUENTE p/ o %-teto (riskState.setEquity)', lastEquityPub, 100);
> ```

## 🤖 Claude *(13:55:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && grep -rn \"dailyCapJob\\|dailyCap.start\\|dailyCap.stop\\|require.*dailyCap\" backend/src/ 2>/dev/null",
  "description": "Find dailyCapJob wiring (start/stop/require)"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> backend/src/server.js:15:const dailyCapJob = require('./dailyCapJob');
> backend/src/server.js:81:    dailyCapJob.start();
> backend/src/riskState.js:14://   daily-cap → disparado pelo dailyCapJob no drawdown de equity do dia. Persistido; AUTO-EXPIRA na virada UTC.
> backend/src/riskState.js:38:// Equity tradeable QUENTE — publicado pelo dailyCapJob a cada ciclo `valued` (~60s, mark-to-market, fail-safe).
> backend/src/riskState.js:164:// Dia em que o daily-cap está armado (null se não armado) — o dailyCapJob usa p/ saber se já disparou hoje.
> backend/src/utils/exchange.js:15://                                  (POST /system/halt) e o cap diário -5% (dailyCapJob) flipam SEM restart.
> backend/src/utils/exchange.js:28://   MAX_ORDER_PCT_EQUITY=<0..1>  → teto da COMPRA como fração do equity tradeable QUENTE (publicado pelo dailyCapJob
> backend/src/utils/exchange.js:64:// Equity tradeável QUENTE e FRESCO (publicado pelo dailyCapJob no riskState), ou null se ausente/frio/velho.
> backend/src/dailyCapJob.js:3:// === dailyCapJob — CIRCUIT-BREAKER de perda diária (-5%) por DRAWDOWN DE EQUITY ===
> backend/src/controllers/systemController.js:2:const dailyCapJob = require('../dailyCapJob');
> backend/src/controllers/systemController.js:45:    const snap = await dailyCapJob.reSnapshot();     // re-baseline pode falhar a preço frio
> backend/src/controllers/systemController.js:51:    res.json(dailyCapJob.getStatus());
> ```

## 🤖 Claude *(13:56:01)*

Let me check line 400 of exchange.js (the third freshEquity caller) and verify the staleness handling there, plus check whether the cockpit or any endpoint exposes equity age / a STALE indicator to the operator.

## 🤖 Claude *(13:56:03)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/src/utils/exchange.js",
  "offset": 380,
  "limit": 60
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 380	        orderStatus,
> 381	        orderTrade,
> 382	        tickerStream,
> 383	        getCoins,
> 384	        withdraw
> 385	    }
> 386	}
> 387	
> 388	// === Seam de testabilidade (additivo, sem mudança de comportamento) ===
> 389	// assertWithinRisk é o CHOKEPOINT de risco (HALT cobre tudo; teto de notional só na COMPRA, venda isenta) por onde
> 390	// TODA ordem real passa: buy()/sell()/oco() o chamam ANTES de tocar a Binance. Exposto como propriedade da factory
> 391	// (que segue chamável como sempre) p/ a suíte de simulação (scripts/sim/riskGuard.test.js) exercitar "HALT bloqueia
> 392	// tudo", "venda isenta" e o "%-teto de compra" sem rede. refPrice idem (deriva o preço do MINI_TICKER p/ MARKET-por-qty).
> 393	module.exports.assertWithinRisk = assertWithinRisk;
> 394	module.exports.refPrice = refPrice;
> 395	
> 396	// Cap EFETIVO atual p/ OBSERVABILIDADE (cockpit/agente) — usa as MESMAS consts + equity quente que o guard, então
> 397	// reporta exatamente o que o assertWithinRisk imporia AGORA. READ-ONLY (não impõe nada). buyCapUsdt/sellCapUsdt
> 398	// null = sem teto (inerte, ou venda em degrade-open por equity frio). equityUsdt null = equity frio/velho/ausente.
> 399	function getEffectiveCaps() {
> 400	    const eqv = freshEquity();
> 401	    let pctCap = (MAX_ORDER_PCT_EQUITY > 0 && eqv != null) ? MAX_ORDER_PCT_EQUITY * eqv : Infinity;
> 402	    if (Number.isFinite(pctCap) && MIN_ORDER_NOTIONAL_FLOOR > 0 && pctCap < MIN_ORDER_NOTIONAL_FLOOR) pctCap = MIN_ORDER_NOTIONAL_FLOOR;
> 403	    const absCeil = MAX_ORDER_NOTIONAL_USDT > 0 ? MAX_ORDER_NOTIONAL_USDT : Infinity;
> 404	    const buyCap = Math.min(pctCap, absCeil);
> 405	    const sellCap = (MAX_SELL_EQUITY_MULT > 0 && eqv != null) ? MAX_SELL_EQUITY_MULT * eqv : Infinity;
> 406	    return {
> 407	        equityUsdt: eqv,                                          // equity tradeable QUENTE; null = frio/velho/ausente
> 408	        buyCapUsdt: Number.isFinite(buyCap) ? buyCap : null,     // teto de COMPRA por ordem; null = sem teto (inerte)
> 409	        buyCapBasis: !Number.isFinite(buyCap) ? 'none' : (Number.isFinite(pctCap) && pctCap <= absCeil ? 'pct-equity' : 'absolute'),
> 410	        sellCapUsdt: Number.isFinite(sellCap) ? sellCap : null,  // rede anti-runaway de VENDA; null = sem teto (off ou equity frio → degrade-open)
> 411	        params: {
> 412	            pctEquity: MAX_ORDER_PCT_EQUITY || null,
> 413	            absCeilUsdt: MAX_ORDER_NOTIONAL_USDT || null,
> 414	            floorUsdt: MIN_ORDER_NOTIONAL_FLOOR || null,
> 415	            sellEquityMult: MAX_SELL_EQUITY_MULT || null,
> 416	        },
> 417	    };
> 418	}
> 419	module.exports.getEffectiveCaps = getEffectiveCaps;
> 420	
> ```

## 🤖 Claude *(13:56:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && grep -rn \"getEffectiveCaps\\|riskCaps\\|equity.*age\\|ageMs\\|STALE\\|stale\" backend/src/controllers/ backend/src/utils/exchange.js 2>/dev/null | head -40",
  "description": "Find getEffectiveCaps and any equity staleness exposure to cockpit"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> backend/src/controllers/analysisController.js:47:// na MEMORY, histerético), idade da última atualização e flag de STALE; + config do job.
> backend/src/controllers/analysisController.js:97:    // riskCaps: teto EFETIVO por ordem (compra ~%-equity, venda = rede anti-runaway) — o agente lê p/ EXPLICAR um
> backend/src/controllers/analysisController.js:99:    // que o assertWithinRisk impõe (DRY). require lazy (utils/exchange é factory; .getEffectiveCaps é estático).
> backend/src/controllers/analysisController.js:100:    try { status.riskCaps = require('../utils/exchange').getEffectiveCaps(); } catch (_) { status.riskCaps = null; }
> backend/src/utils/exchange.js:399:function getEffectiveCaps() {
> backend/src/utils/exchange.js:419:module.exports.getEffectiveCaps = getEffectiveCaps;
> ```

## 🤖 Claude *(13:56:09)*

Now let me verify the cockpit/riskCaps exposure. The key question is whether the operator gets any signal that equity is stale/old. `getEffectiveCaps` returns `equityUsdt: null` when equity is frozen/old — that is a degraded signal, but does it carry the age, and is there an explicit STALE flag like the regime gate has? Let me check the cockpit output and the `getStatus` returned by dailyCapJob (which has `at`/`ageMs`).

## 🤖 Claude *(13:56:10)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js",
  "offset": 40,
  "limit": 75
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 40	        res.json(data);
> 41	    } catch (err) {
> 42	        next(err);
> 43	    }
> 44	}
> 45	
> 46	// GET /analysis/regime-status — status do job de regime: por símbolo o regime do GATE (valor
> 47	// na MEMORY, histerético), idade da última atualização e flag de STALE; + config do job.
> 48	// Read-only; serve o painel /intelligence p/ tornar visível halt silencioso e a divergência
> 49	// display×gate (o card "Market Regime" mostra o instantâneo; este, a decisão do gate).
> 50	function getRegimeStatus(req, res) {
> 51	    res.json(regimeJob.getStatus());
> 52	}
> 53	
> 54	// GET /analysis/flow/:symbol — desequilíbrio de fluxo do TAKER (imbalance/toxicity) dos aggTrades
> 55	// recentes da MAINNET (ground-truth via isBuyerMaker). Read-only, sem chaves. Cache ~20s. Proxy de
> 56	// toxicidade/seleção adversa (v1 ancorado — não o True VPIN completo). É o estado do Oráculo (v1).
> 57	async function getFlow(req, res, next) {
> 58	    const symbol = String(req.params.symbol || '').toUpperCase();
> 59	    if (!/^[A-Z0-9]{5,20}$/.test(symbol)) return res.status(400).json({ error: 'simbolo invalido' });
> 60	    try {
> 61	        const data = await getFlowData(symbol);
> 62	        if (data.unavailable) return res.status(502).json({ error: data.reason, symbol });
> 63	        res.json(data);
> 64	    } catch (err) {
> 65	        next(err);
> 66	    }
> 67	}
> 68	
> 69	// GET /analysis/flow-status — status do flow job (por símbolo: último fluxo + idade), p/ observabilidade.
> 70	function getFlowStatus(req, res) {
> 71	    res.json(flowJob.getStatus());
> 72	}
> 73	
> 74	// GET /analysis/cockpit — snapshot agregado do Cockpit (por símbolo: distribuição de retornos 1m, EV
> 75	// net-de-fee, tail, banda MC driftless, regime/flow e estado dos gates de compra). READ-ONLY; alimenta
> 76	// o painel /cockpit (single source of truth = brain). Não expõe segredos (só estado de mercado).
> 77	async function getCockpitStatus(req, res) {
> 78	    const status = cockpitJob.getStatus();
> 79	    // AMBIENTE real p/ o painel e o agente: useTestnet (settings, leitura barata sem decrypt) + HALT QUENTE.
> 80	    // tradingHalt agora vem do riskState (env floor | manual | daily-cap), não mais só do .env — chave mantida
> 81	    // p/ o frontend (Cockpit.js) e o agente (agent.js) não quebrarem; haltSource/haltReason são ADITIVOS
> 82	    // (contexto p/ o agente REPORTAR a causa; não é gatilho de notify — ver notifyDedup família 'halt').
> 83	    const st = riskState.getState();
> 84	    try {
> 85	        const s = await settingsRepository.getSettings(process.env.DEFAULT_SETTINGS_ID || 1);
> 86	        status.env = { useTestnet: !!(s && s.useTestnet), tradingHalt: st.halted, haltSource: st.source || null, haltReason: st.reason || null };
> 87	    } catch (e) {
> 88	        status.env = { useTestnet: null, tradingHalt: st.halted, haltSource: st.source || null, haltReason: st.reason || null };
> 89	    }
> 90	    // paper para ANÁLISE: anexa o resumo do Paper Engine (totais + por trilha) ao cockpit que o agente já lê.
> 91	    // READ-ONLY, best-effort (não derruba o cockpit se o ledger estiver vazio/indisponível).
> 92	    try { status.paper = await paperService.summary(); } catch (_) { status.paper = null; }
> 93	    // groups: estado ATIVO por grupo lógico (Farm/Trend/Baseline/Paper) — o agente precisa do estado de ATIVAÇÃO
> 94	    // (não só do gate de regime) p/ NÃO implicar execução de um grupo PARADO ("gate aberto" ≠ "grupo armado").
> 95	    // READ-ONLY, best-effort. require lazy (mesmo dir de controllers; evita ciclo no load).
> 96	    try { status.groups = await require('./automationsController').computeAutomationGroups(); } catch (_) { status.groups = null; }
> 97	    // riskCaps: teto EFETIVO por ordem (compra ~%-equity, venda = rede anti-runaway) — o agente lê p/ EXPLICAR um
> 98	    // capamento ("a compra foi capada em ~$30") em vez de inferir anomalia. READ-ONLY, best-effort, mesmas consts
> 99	    // que o assertWithinRisk impõe (DRY). require lazy (utils/exchange é factory; .getEffectiveCaps é estático).
> 100	    try { status.riskCaps = require('../utils/exchange').getEffectiveCaps(); } catch (_) { status.riskCaps = null; }
> 101	    res.json(status);
> 102	}
> 103	
> 104	// GET /analysis/cockpit/:symbol — o COCKPIT de um símbolo, lido direto da MEMORY do brain (cópia rasa).
> 105	function getCockpit(req, res) {
> 106	    const symbol = String(req.params.symbol || '').toUpperCase();
> 107	    if (!/^[A-Z0-9]{5,20}$/.test(symbol)) return res.status(400).json({ error: 'simbolo invalido' });
> 108	    const snap = beholder.getMemory(symbol, indexKeys.COCKPIT);
> 109	    if (!snap) return res.status(404).json({ error: 'sem snapshot de cockpit', symbol });
> 110	    // freshen: regime/flow/gates SEMPRE no instante da leitura (mata a defasagem de até 60s do snapshot,
> 111	    // que o agente lia como "contradição"); a analítica 1m fica na cadência do job. Ver cockpitJob.freshen.
> 112	    res.json(cockpitJob.freshen(symbol, snap));
> 113	}
> 114	
> ```

## 🤖 Claude *(13:56:22)*

Now I have a comprehensive understanding. Let me analyze the observability question precisely.

Key facts confirmed:
- `getEffectiveCaps()` (exchange.js:399-418) exposes `equityUsdt` (null when frozen/old) and `buyCapBasis` (which becomes `'absolute'` when equity is stale and abs ceiling exists). This is wired into the cockpit at analysisController.js:100 as `status.riskCaps`.
- `dailyCapJob.getStatus()` (dailyCapJob.js:245-254) exposes `running`, `at`, `ageMs`, `halted`, `tripped`, `last`. This is the dailyCap status endpoint (systemController.js:51).

Now the critical claim of the finding: "if dailyCapJob dies/hangs, equity-hot stops being republished, the %-cap silently degrades to absolute after 10min with NO alert, and the operator isn't told the %-cap engine lost its equity reference."

Let me verify whether the cold-alert genuinely does NOT cover the "job dead" scenario, and whether there's a stuck-`running` deadlock risk. Let me look at how `checkCap` handles exceptions — does an exception leave `running=true`?

In `checkCap`, the `finally { running = false; }` block (line 205-207) resets `running` even on exception, so a recurring exception does NOT permanently deadlock `running`. But each exception is caught at line 203-204 and just logged; `setEquity` is NOT called in that path (it's after the try body's normal flow). So a recurring exception in `computeEquity()` (e.g. `exchange.balance()` throwing every cycle) means: the job keeps running every 60s, but never reaches `setEquity` → equity goes stale → %-cap silently degrades. And crucially, that exception path does NOT trigger the cold-alert either (the cold-alert is only inside the `!eq.valued` branch, which requires `computeEquity` to *return* `{valued:false}`, not *throw*).

Let me confirm this distinction precisely — an exception vs a returned `valued:false`.

## 🤖 Claude *(13:56:23)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/src/dailyCapJob.js",
  "offset": 136,
  "limit": 35
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
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
> ```

## 🤖 Claude *(13:56:34)*

My analysis is confirmed. The finding is essentially correct in its core mechanics, but I need to assess severity precisely and refine the location/claims. Let me note an important nuance the finding's title gets slightly wrong: the title says "EQUITY_MAX_AGE_MS default 10min vs publicação a cada ~60s". The asymmetry framing (10min vs 60s) is actually a *safety margin* design — it tolerates up to ~10 missed cycles before degrading. That's not a bug per se; it's intentional slack.

The REAL substance of the finding is the **observability gap**: there is no alarm that fires when the `setEquity` republication stops (whether from job death, or — more realistically — a *recurring exception* in `computeEquity()` which keeps `running` cycling but never reaches `setEquity` and never reaches the cold-alert branch either, because exceptions are caught at line 203 and only logged).

Let me verify the two degradation directions precisely against the impact claim:

1. **Direction is safe**: When equity goes stale, `freshEquity()` returns null → `pctCap` stays `Infinity` → `cap = min(Infinity, absCeil) = absCeil`. With `MAX_ORDER_NOTIONAL_USDT` set (currently $50 per HANDOFF), the buy cap degrades from `min($50, pct×equity)` to just `$50`. Since equity is ~$149 and a typical `MAX_ORDER_PCT_EQUITY` would make pct×equity smaller or comparable, the degraded cap is *larger or equal* (less restrictive). Let me confirm the actual env values to gauge real-world materiality.

## 🤖 Claude *(13:56:38)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && sudo -n -u gcrux-tradeux grep -E \"MAX_ORDER_PCT_EQUITY|MAX_ORDER_NOTIONAL_USDT|MIN_ORDER_NOTIONAL_FLOOR|EQUITY_MAX_AGE_MS|MAX_SELL_EQUITY_MULT|DAILY_CAP_ENABLED|DAILY_CAP_CHECK_MS\" .env 2>/dev/null || echo \"=== cannot read .env as gcrux; trying direct ===\" && grep -E \"MAX_ORDER_PCT_EQUITY|MAX_ORDER_NOTIONAL_USDT|MIN_ORDER_NOTIONAL_FLOOR|EQUITY_MAX_AGE_MS|MAX_SELL_EQUITY_MULT|DAILY_CAP_ENABLED\" /home/gcrux-tradeux/tradeux/.env 2>/dev/null || echo \"no .env readable\"",
  "description": "Read risk-cap env values from .env"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> MAX_ORDER_NOTIONAL_USDT=100
> MAX_ORDER_PCT_EQUITY=0.20
> MIN_ORDER_NOTIONAL_FLOOR=12
> MAX_SELL_EQUITY_MULT=3
> no .env readable
> ```

## 🤖 Claude *(13:56:51)*

This is the key materiality data. Let me compute the real-world impact with these live values:

- `MAX_ORDER_PCT_EQUITY = 0.20`, equity ≈ $149 → pct cap = `0.20 × 149 = ~$29.80`
- `MAX_ORDER_NOTIONAL_USDT = 100` (absolute ceiling)
- Fresh: `cap = min($29.80, $100) = $29.80`
- Stale (equity null): `cap = min(Infinity, $100) = $100`

So when equity goes stale, the per-order BUY cap **degrades from ~$30 to $100** — i.e. it becomes **3.3× larger / LESS restrictive**, not more. This directly **contradicts** the finding's claim that "degrada para teto menor = seguro." With the actual live env values, the staleness degradation makes the cap *looser*, not tighter.

This is an important correction: the finding's premise ("não é perda de dinheiro direta (degrada conservador)") is **wrong** given the live config. The %-equity cap ($30) is *tighter* than the absolute ceiling ($100), so losing the %-equity reference *relaxes* the buy cap to the absolute ceiling. The direction is still bounded (the $100 absolute ceiling still holds and the HALT still covers everything), but it's NOT "conservative degradation" — it's a *loosening*.

Let me double check the relevant note: the canary is currently FARM-ONLY with buys OFF, so in the *current* operational state no buys are happening at all. But the finding is about a latent risk for when buys are re-enabled. Let me also confirm there's genuinely no separate watchdog for the equity republication staleness beyond the cold-alert (which only fires on `valued:false`, not on job-death or recurring exception).

## 🤖 Claude *(13:56:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && grep -rn \"equity.*velho\\|equity.*stale\\|equity.*old\\|republic\\|watchdog\\|heartbeat\\|setEquity\" backend/src/ 2>/dev/null | grep -vi \"test\" | head; echo \"---SIGTERM/stop hooks---\"; grep -rn \"SIGTERM\\|process.on\\|dailyCapJob.stop\" backend/src/server.js 2>/dev/null",
  "description": "Search for any equity-staleness watchdog and SIGTERM/stop hooks"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> backend/src/riskState.js:41:// válido; equity ausente/velho faz o guard degradar p/ o teto absoluto (direção segura).
> backend/src/riskState.js:43:function setEquity(v) {
> backend/src/riskState.js:173:module.exports = { dayKeyUTC, isHalted, getState, setFloor, setHalt, clearDailyCap, getDailyCapDay, setEquity, getEquity };
> backend/src/dailyCapJob.js:92:// Retorna { valued, equity, usdtFree, cold:[...], settings } ou { valued:false, error } se saldo indisponível.
> backend/src/dailyCapJob.js:129:    return { valued, equity, usdtFree, cold, ignored, settings };
> backend/src/dailyCapJob.js:143:        LAST = { at: new Date(AT).toISOString(), valued: eq.valued, equity: eq.valued ? eq.equity : null, cold: eq.cold || null, ignored: eq.ignored || null, error: eq.error || null };
> backend/src/dailyCapJob.js:178:        riskState.setEquity(eq.equity);
> backend/src/dailyCapJob.js:218:        riskState.setEquity(eq.equity); // re-baseline manual também atualiza o equity quente do %-teto
> backend/src/utils/exchange.js:23://                                  venda legítima (1 posição ≤ equity << n×equity). equity frio/velho → venda PASSA
> backend/src/utils/exchange.js:30://                                  dimensionamento que ESCALA com o capital. equity ausente/frio/velho
> ---SIGTERM/stop hooks---
> ```

## 🤖 Claude *(13:57:08)*

Confirmed. There is:
- **No dedicated equity-staleness watchdog/heartbeat** anywhere — the only alarm path is the cold-alert inside `checkCap`'s `!eq.valued` branch.
- **No SIGTERM hook** calling `dailyCapJob.stop()` (consistent with the timer being `unref()`'d).

So the finding's central mechanism is REAL: if the dailyCapJob stops running or recurringly throws in `computeEquity()`, equity stops being republished, `freshEquity()` returns null after `EQUITY_MAX_AGE_MS`, and **no alarm fires** (the cold-alert requires a *returned* `valued:false`, which only happens when the job is actually running and reaches that branch — not when it's dead or throwing).

Now let me finalize the severity assessment. The finding labeled it MEDIUM. My corrections:

1. **The "asymmetric staleness window 10min vs 60s" framing is misleading** — that's intentional slack (tolerate ~10 missed cycles), not a flaw. The real issue is the *observability gap* on republication failure.

2. **The "degrada conservador / não é perda de dinheiro" claim is WRONG** with live config. With `pct=0.20`, equity ~$149, abs=$100: fresh cap ≈ $30, stale cap = $100. Staleness *loosens* the buy cap 3.3×. It's still bounded by the $100 absolute ceiling and the HALT, so it's not unbounded runaway — but it is the opposite direction of what the finding claims.

3. **The exception path is a more realistic trigger than "job dies"** — `computeEquity()` throwing recurrently (e.g. `exchange.balance()` failing) keeps the job cycling but never reaches `setEquity` AND never reaches the cold-alert (caught at line 203, only logged to `system.log`). This is a genuine blind spot.

4. **Mitigations that reduce severity**: (a) the absolute ceiling $100 + HALT still bound exposure; (b) the cockpit `riskCaps.equityUsdt=null` and `buyCapBasis='absolute'` DO surface the degraded state to the operator/agent if they look — but it's passive (no push alert) and not labeled STALE like the regime gate is; (c) `dailyCapJob.getStatus().ageMs/running` is exposed via the system endpoint, giving a way to observe job-staleness, but again passive/pull, no proactive alarm; (d) currently buys are OFF (FARM-ONLY canary), so latent.

Net: the core observability gap is REAL and confirmed in code. Severity MEDIUM is appropriate — possibly even slightly elevated because the finding *understated* the direction (it loosens the cap, not tightens), but the bound (abs ceiling + HALT) and the existence of passive observability (cockpit riskCaps + dailyCap status) keep it at MEDIUM, not HIGH. The location lines are accurate.

Let me produce the verdict.

## 🤖 Claude *(13:57:38)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "title": "Equity-quente: sem alarme dedicado quando a REPUBLICA\u00c7\u00c3O do equity para (job morto OU exce\u00e7\u00e3o recorrente em computeEquity) \u2192 %-teto de COMPRA degrada SILENCIOSAMENTE para o teto absoluto",
  "confirmed": true,
  "severityFinal": "MEDIUM",
  "locationConfirmed": "backend/src/utils/exchange.js:47-48 (EQUITY_MAX_AGE_MS=600000) e :64-69 (freshEquity); backend/src/riskState.js:42-47 (equitySnap n\u00e3o-persistido); backend/src/dailyCapJob.js:178 (\u00fanica chamada de setEquity no hot-path) + :203-204 (catch s\u00f3 LOGA a exce\u00e7\u00e3o) + :164-169 (cold-alert s\u00f3 no ramo valued:false)",
  "evidence": "CONFIRMADO no c\u00f3digo real:\n- exchange.js:47-48: `EQUITY_MAX_AGE_MS = parseInt(process.env.EQUITY_MAX_AGE_MS||'600000')` = 10min.\n- exchange.js:65-68 freshEquity(): retorna o valor s\u00f3 se `(Date.now()-eq.at) <= EQUITY_MAX_AGE_MS`; passado isso \u2192 null.\n- Com equity=null: exchange.js:103-113 \u2192 pctCap fica Infinity \u2192 `cap = min(Infinity, absCeil) = absCeil`. O %-teto some.\n- setEquity() s\u00f3 \u00e9 chamado em dailyCapJob.js:178 (ciclo `valued`) e :218 (reSnapshot manual). grep confirma: nenhum outro publicador.\n- dailyCapJob.js:203-204: `catch(err){ logger('system', ...) }` \u2014 uma exce\u00e7\u00e3o em computeEquity() (ex.: exchange.balance() falhando) N\u00c3O chega no setEquity(:178) NEM no cold-alert(:164-169, que est\u00e1 DENTRO do ramo `if(!eq.valued)` :155, alcan\u00e7ado s\u00f3 quando computeEquity RETORNA valued:false, n\u00e3o quando LAN\u00c7A). `finally{running=false}` evita deadlock mas o ciclo segue sem republicar equity.\n- N\u00e3o existe watchdog/heartbeat de equity-velho (grep por watchdog/heartbeat/republic = nada); n\u00e3o h\u00e1 hook de SIGTERM chamando dailyCapJob.stop() (server.js:81 s\u00f3 .start()).\n\nREFUTA\u00c7\u00c3O PARCIAL do impacto descrito no achado: o achado diz \"degrada para teto menor = seguro / n\u00e3o \u00e9 perda de dinheiro\". Com os valores LIVE do .env (MAX_ORDER_PCT_EQUITY=0.20, MAX_ORDER_NOTIONAL_USDT=100, equity~$149): teto fresco = min(0.20\u00d7149=$29,80, $100) = ~$30; teto com equity velho/null = min(Infinity, $100) = $100. Ou seja a staleness AFROUXA o teto de compra ~3,3\u00d7 (de ~$30 p/ $100), N\u00c3O aperta. Continua LIMITADO (teto absoluto $100 + HALT cobrem), mas a dire\u00e7\u00e3o do achado est\u00e1 invertida.",
  "reasoning": "PROBLEMA REAL \u2014 a mec\u00e2nica central confirma no c\u00f3digo, MAS com duas corre\u00e7\u00f5es importantes ao enunciado:\n\n(1) Dire\u00e7\u00e3o do impacto INVERTIDA pelo achado. Com a config viva (.env: pct=0.20, abs=100, equity~$149), o %-teto fresco (~$30) \u00e9 MAIS APERTADO que o teto absoluto ($100). Perder a refer\u00eancia de equity AFROUXA a compra (~$30 \u2192 $100, ~3,3\u00d7), n\u00e3o aperta. Segue bounded ($100 abs + HALT), ent\u00e3o n\u00e3o \u00e9 runaway, mas \"degrada conservador\" est\u00e1 errado.\n\n(2) Gatilho mais realista que \"job morre\": uma EXCE\u00c7\u00c3O RECORRENTE em computeEquity() (ex.: exchange.balance() falhando em loop) mant\u00e9m o job ciclando a cada 60s mas NUNCA alcan\u00e7a setEquity(:178) e NUNCA alcan\u00e7a o cold-alert(:164-169) \u2014 a exce\u00e7\u00e3o \u00e9 capturada em :203-204 e s\u00f3 vai pro system.log. Esse \u00e9 o blind spot concreto: o cold-alert cobre equity INAVALI\u00c1VEL (computeEquity retorna valued:false), n\u00e3o equity N\u00c3O-REPUBLICADO (job parado ou lan\u00e7ando).\n\n(3) O t\u00edtulo do achado enquadra como \"janela de staleness assim\u00e9trica 10min vs 60s\" \u2014 isso \u00e9 folga INTENCIONAL (tolera ~10 ciclos perdidos), n\u00e3o a falha. A falha \u00e9 a OBSERVABILIDADE: n\u00e3o h\u00e1 alarme push quando a republica\u00e7\u00e3o para.\n\nMITIGANTES que mant\u00eam em MEDIUM (n\u00e3o HIGH): (a) teto absoluto $100 + HALT QUENTE continuam cobrindo \u2014 exposi\u00e7\u00e3o bounded; (b) h\u00e1 observabilidade PASSIVA \u2014 o cockpit exp\u00f5e riskCaps.equityUsdt=null e buyCapBasis='absolute' (getEffectiveCaps, exchange.js:399-418 \u2192 analysisController:100) e dailyCapJob.getStatus() exp\u00f5e running/at/ageMs (systemController:51); o operador/agente V\u00caEM o estado degradado se olharem; (c) canary atual \u00e9 FARM-ONLY com COMPRAS OFF \u2192 latente hoje; (d) equitySnap n\u00e3o-persistido s\u00f3 afeta boot (degrade seguro at\u00e9 o 1\u00ba ciclo, ok).\n\nFaltas reais: nenhum alarme PROATIVO de \"equity-quente parou de ser publicado\" desacoplado do ramo valued:false; nenhuma flag STALE de equity an\u00e1loga \u00e0 do regime gate. Fix sugerido: alarme baseado na idade de getEquity().at (independe do job estar vivo) OU mover a publica\u00e7\u00e3o/heartbeat p/ fora do caminho que a exce\u00e7\u00e3o curto-circuita, e exibir STALE no cockpit quando ageMs > EQUITY_MAX_AGE_MS. Severidade FINAL: MEDIUM (cegueira de risco real + dire\u00e7\u00e3o de afrouxamento sob config viva, por\u00e9m bounded e com observabilidade passiva existente)."
}
```

> **Tool Result (StructuredOutput)** - ✅ Success
>
> ```
> Structured output provided successfully
> ```

## 🤖 Claude *(13:58:02)*

VEREDITO: PASS COM RESSALVAS — achado CONFIRMADO como problema REAL, com duas correções ao enunciado.

A mecânica central confere no código real:
- `EQUITY_MAX_AGE_MS=600000` (10min) em `backend/src/utils/exchange.js:47-48`; `freshEquity()` (`:65-68`) zera o valor passada a idade.
- `setEquity()` só é publicado em `dailyCapJob.js:178` (ciclo `valued`) e `:218` (reSnapshot manual) — confirmado por grep, nenhum outro publicador.
- Não há watchdog/heartbeat de equity-velho nem hook de SIGTERM chamando `dailyCapJob.stop()`.

Correções importantes ao achado:

[MEDIUM] Direção do impacto INVERTIDA. O achado afirma "degrada para teto menor = seguro / não é perda de dinheiro". Com os valores LIVE do `.env` (`MAX_ORDER_PCT_EQUITY=0.20`, `MAX_ORDER_NOTIONAL_USDT=100`, equity ~$149): teto fresco = `min(0.20×149≈$30, $100) = ~$30`; com equity velho/null = `min(Infinity, $100) = $100`. A staleness AFROUXA a compra ~3,3× (de ~$30 p/ $100), não aperta. Segue bounded (teto absoluto $100 + HALT cobrem), mas não é "degradação conservadora".

[MEDIUM] Gatilho mais realista que "job morre" — uma EXCEÇÃO RECORRENTE em `computeEquity()` (ex.: `exchange.balance()` falhando em loop) mantém o job ciclando a cada 60s mas nunca alcança `setEquity` (`:178`) nem o cold-alert (`:164-169`, que vive dentro do ramo `if(!eq.valued)` `:155`). A exceção é capturada em `dailyCapJob.js:203-204` e só vai pro `system.log`. Esse é o blind spot concreto: o cold-alert cobre equity INAVALIÁVEL (retorno `valued:false`), não equity NÃO-REPUBLICADO (job parado/lançando).

[INFO] O título enquadra "janela assimétrica 10min vs 60s" como a falha — na verdade isso é folga intencional (tolera ~10 ciclos perdidos). A falha é OBSERVABILIDADE: sem alarme push quando a republicação para.

Mitigantes que seguram em MEDIUM (não HIGH): teto absoluto $100 + HALT quente = exposição bounded; observabilidade PASSIVA já existe (cockpit `riskCaps.equityUsdt=null`/`buyCapBasis='absolute'` via `getEffectiveCaps` em `exchange.js:399-418` → `analysisController.js:100`; `dailyCapJob.getStatus()` expõe `running`/`at`/`ageMs` via `systemController.js:51`); canary atual é FARM-ONLY com COMPRAS OFF → latente hoje; `equitySnap` não-persistido só afeta boot (degrade seguro, ok).

Testes que eu rodaria:
1. Mockar `riskState.getEquity()` retornando `{value:150, at: Date.now()-700000}` (>10min) e chamar `assertWithinRisk('BUY','BTCUSDT',...)` com notional $80 → deve PASSAR (degradou pro abs $100), provando o afrouxamento de ~$30 p/ $100.
2. Forçar `exchange.balance()` a lançar e rodar `checkCap()` 20×/60s simulado → assertar que `system.log` tem o erro mas Telegram NÃO recebe nada e `getEquity().at` envelhece além de `EQUITY_MAX_AGE_MS` (reproduz o blind spot do catch).
3. Confirmar que o cold-alert (`:164-169`) NÃO dispara nesse cenário de exceção (só dispara em `valued:false`).

Recomendação de merge: não há PR aqui — é um achado de design contra código já vivo. Recomendo abrir follow-up de baixo esforço: (a) alarme proativo baseado na idade de `getEquity().at` (independe do job estar vivo), (b) flag STALE de equity no cockpit quando `ageMs > EQUITY_MAX_AGE_MS`, análoga à do regime gate, e (c) corrigir a doutrina nos comentários que dizem "degrada seguro" (com a config viva ele afrouxa). Não-bloqueante para o canary FARM-ONLY (compras off), mas deve entrar ANTES de re-habilitar compras por %-equity.

Arquivos relevantes:
- `/home/gcrux-tradeux/tradeux/backend/src/utils/exchange.js` (`:47-48`, `:64-69`, `:103-113`, `:399-418`)
- `/home/gcrux-tradeux/tradeux/backend/src/riskState.js` (`:38-47`)
- `/home/gcrux-tradeux/tradeux/backend/src/dailyCapJob.js` (`:155-178`, `:203-207`)
- `/home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js` (`:100`)

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-22 - agent-aa9ba1c078467653c]]
> * **Próxima Sessão**: [[2026-06-22 - agent-aaac9d7e933a6b87b]]
%% --- TIMELINE END --- %%

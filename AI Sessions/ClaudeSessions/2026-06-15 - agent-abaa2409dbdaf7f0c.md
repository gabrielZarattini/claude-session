# Session agent-abaa2409dbdaf7f0c
**Date:** 2026-06-15 | **Session ID:** `agent-abaa2409dbdaf7f0c`

---

## 👤 User *(18:55:42)*

Repo em /home/gcrux-tradeux/tradeux. Mapeie o ENCANAMENTO DE DADOS DE 1 MINUTO disponível para uma estratégia. Leia backend/src/app-em.js, backend/src/beholder.js, backend/src/utils/indexes.js, backend/src/utils/exchange.js. Responda: que streams/klines/miniTicker/aggTrades chegam e em que intervalo; quais MEMORY indexes existem por símbolo (MINI_TICKER, BOOK, FLOW, REGIME, etc.); existe cálculo de indicadores em janela de 1m (RSI/SMA/Bollinger/ATR)? a que granularidade o BRAIN reage; há acesso a book/profundidade real ou simulado. Foque no que habilita/bloqueia decisões a cada vela de 1m.

## 🤖 Claude *(18:55:45)*

I'll map the 1-minute data plumbing. Let me read the four files in parallel.

## 🤖 Claude *(18:55:45)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/src/app-em.js"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	const ordersRepository = require('./repositories/ordersRepository');
> 2	const { orderStatus } = require('./repositories/ordersRepository');
> 3	const harvestPositionsRepository = require('./repositories/harvestPositionsRepository');
> 4	const { monitorTypes, getActiveMonitors } = require('./repositories/monitorsRepository');
> 5	const { execCalc, indexKeys } = require('./utils/indexes');
> 6	const logger = require('./utils/logger');
> 7	const push = require('./utils/push');
> 8	const telegramNotify = require('./utils/telegramNotify');
> 9	const { getDefaultSettings } = require('./repositories/settingsRepository');
> 10	
> 11	let WSS, beholder, exchange;
> 12	
> 13	// Atraso da reconciliação de listStatus da OCO: > 3s do executionReport por-perna, para
> 14	// que o caminho primário (processExecutionData) atualize antes e evitemos REST à toa.
> 15	const OCO_RECONCILE_DELAY_MS = 4000;
> 16	
> 17	function startMiniTickerMonitor(monitorId, broadcastLabel, logs) {
> 18	    if (!exchange) return new Error('Exchange Monitor not initialized yet.');
> 19	    exchange.miniTickerStream(async (markets) => {
> 20	        if (logs) logger('M:' + monitorId, markets);
> 21	
> 22	        try {
> 23	            Object.entries(markets).map(async (mkt) => {
> 24	
> 25	                delete mkt[1].volume;
> 26	                delete mkt[1].quoteVolume;
> 27	                delete mkt[1].eventTime;
> 28	                const converted = {};
> 29	                Object.entries(mkt[1]).map(prop => converted[prop[0]] = parseFloat(prop[1]));
> 30	
> 31	                const results = await beholder.updateMemory(mkt[0], indexKeys.MINI_TICKER, null, converted);
> 32	                if (results) results.map(r => sendMessage({ notification: r }));
> 33	            })
> 34	
> 35	            if (broadcastLabel && WSS) sendMessage({ [broadcastLabel]: markets });
> 36	
> 37	            //simulação de book
> 38	            const books = Object.entries(markets).map(mkt => {
> 39	                const book = { symbol: mkt[0], bestAsk: mkt[1].close, bestBid: mkt[1].close };
> 40	                const currentMemory = beholder.getMemory(mkt[0], indexKeys.BOOK);
> 41	
> 42	                const newMemory = {};
> 43	                newMemory.previous = currentMemory ? currentMemory.current : book;
> 44	                newMemory.current = book;
> 45	
> 46	                beholder.updateMemory(mkt[0], indexKeys.BOOK, null, newMemory)
> 47	                    .then(results => {
> 48	                        if (results)
> 49	                            results.map(r => sendMessage({ notification: r }));
> 50	                    })
> 51	
> 52	                return book;
> 53	            })
> 54	            if (WSS) sendMessage({ book: books });
> 55	            //fim da simulação de book
> 56	
> 57	        } catch (err) {
> 58	            if (logs) logger('M:' + monitorId, err)
> 59	        }
> 60	    })
> 61	    logger('M:' + monitorId, 'Mini Ticker Monitor has started!');
> 62	}
> 63	
> 64	let book = [];
> 65	function startBookMonitor(monitorId, broadcastLabel, logs) {
> 66	    if (!exchange) return new Error('Exchange Monitor not initialized yet.');
> 67	    exchange.bookStream(async (order) => {
> 68	        if (logs) logger('M:' + monitorId, order);
> 69	
> 70	        try {
> 71	            if (book.length === 200) {
> 72	                if (broadcastLabel && WSS) sendMessage({ [broadcastLabel]: book });
> 73	                book = [];
> 74	            }
> 75	            else book.push({ ...order });
> 76	
> 77	            const orderCopy = { ...order };
> 78	            delete orderCopy.symbol;
> 79	            delete orderCopy.updateId;
> 80	            delete orderCopy.bestAskQty;
> 81	            delete orderCopy.bestBidQty;
> 82	
> 83	            const converted = {};
> 84	            Object.entries(orderCopy).map(prop => converted[prop[0]] = parseFloat(prop[1]));
> 85	
> 86	            const currentMemory = beholder.getMemory(order.symbol, indexKeys.BOOK);
> 87	
> 88	            const newMemory = {};
> 89	            newMemory.previous = currentMemory ? currentMemory.current : converted;
> 90	            newMemory.current = converted;
> 91	
> 92	            const results = await beholder.updateMemory(order.symbol, indexKeys.BOOK, null, newMemory);
> 93	            if (results) results.map(r => sendMessage({ notification: r }));
> 94	        } catch (err) {
> 95	            if (logs) logger('M:' + monitorId, err);
> 96	        }
> 97	    })
> 98	    logger('M:' + monitorId, 'Book Monitor has started!');
> 99	}
> 100	
> 101	async function loadWallet() {
> 102	    if (!exchange) throw new Error('Exchange Monitor not initialized yet.');
> 103	
> 104	    try {
> 105	        const info = await exchange.balance();
> 106	        const wallet = Object.entries(info).map(async (item) => {
> 107	            const results = await beholder.updateMemory(item[0], indexKeys.WALLET, null, parseFloat(item[1].available));
> 108	            if (results) results.map(r => sendMessage({ notification: r }));
> 109	
> 110	            return {
> 111	                symbol: item[0],
> 112	                available: item[1].available,
> 113	                onOrder: item[1].onOrder
> 114	            }
> 115	        })
> 116	        return Promise.all(wallet);
> 117	    } catch (err) {
> 118	        throw new Error(err.body ? JSON.stringify(err.body) : err.message);//evita 401 da Binance
> 119	    }
> 120	}
> 121	
> 122	function getLightOrder(order) {
> 123	    const orderCopy = { ...order };
> 124	    delete orderCopy.id;
> 125	    delete orderCopy.symbol;
> 126	    delete orderCopy.automationId;
> 127	    delete orderCopy.orderId;
> 128	    delete orderCopy.clientOrderId;
> 129	    delete orderCopy.transactTime;
> 130	    delete orderCopy.isMaker;
> 131	    delete orderCopy.commission;
> 132	    delete orderCopy.obs;
> 133	    delete orderCopy.automation;
> 134	    delete orderCopy.createdAt;
> 135	    delete orderCopy.updatedAt;
> 136	
> 137	    orderCopy.limitPrice = orderCopy.limitPrice ? parseFloat(orderCopy.limitPrice) : null;
> 138	    orderCopy.stopPrice = orderCopy.stopPrice ? parseFloat(orderCopy.stopPrice) : null;
> 139	    orderCopy.avgPrice = orderCopy.avgPrice ? parseFloat(orderCopy.avgPrice) : null;
> 140	    orderCopy.net = orderCopy.net ? parseFloat(orderCopy.net) : null;
> 141	    orderCopy.quantity = orderCopy.quantity ? parseFloat(orderCopy.quantity) : null;
> 142	    orderCopy.icebergQty = orderCopy.icebergQty ? parseFloat(orderCopy.icebergQty) : null;
> 143	    return orderCopy;
> 144	}
> 145	
> 146	function notifyOrderUpdate(order) {
> 147	    let type = '';
> 148	    switch (order.status) {
> 149	        case 'FILLED': type = 'success'; break;
> 150	        case 'REJECTED':
> 151	        case 'CANCELED':
> 152	        case 'EXPIRED': type = 'error'; break;
> 153	        default: type = 'info'; break;
> 154	    }
> 155	    sendMessage({ notification: { text: `Order #${order.orderId} was updated as ${order.status}`, type } });
> 156	}
> 157	
> 158	// orderIds de fill de trend já contabilizados — dedup contra um executionReport FILLED RE-ENTREGUE
> 159	// (reconexão do userData stream): o BUY é ADITIVO, então um report duplicado somaria 2x e inflaria a
> 160	// posição. Só recebe ordens de trend (raras, dirigidas por cross) → footprint desprezível. Reseta no
> 161	// restart, coerente com o TREND_QTY (que hoje também é volátil — ver nota de persistência abaixo).
> 162	const countedTrendFills = new Set();
> 163	
> 164	// Trend Following — mantém MEMORY['<sym>:TREND_QTY'] (posição em base asset atribuída ao trend),
> 165	// lido pela calcQty do template SELL da id7. Distingue ordem de trend pelas conditions da automação
> 166	// (referenciam TREND_CROSS), lidas do BRAIN em memória (sem ida ao banco). Golden BUY soma a qty
> 167	// FILLED; death SELL zera. Só atua em FILLED (aí order.quantity = qty cheia preenchida). Best-effort:
> 168	// um erro aqui não quebra o fluxo da ordem (o gate de venda da id7 falha fechado se TREND_QTY ausente).
> 169	// PERSISTÊNCIA: TREND_QTY é VOLÁTIL (só MEMORY), ao contrário do cross (regimeStates). Aceitável p/ size
> 170	// pequeno na validação; ANTES DE ESCALAR O SIZE, persistir (senão um restart com posição de trend aberta
> 171	// perde a referência e o death seguinte não liquida). Ver HANDOFF / [[tradeux-trend-following]].
> 172	async function updateTrendPosition(order) {
> 173	    try {
> 174	        if (!order || order.status !== orderStatus.FILLED || !order.automationId) return;
> 175	        if (countedTrendFills.has(order.orderId)) return; // já contabilizado (report FILLED re-entregue)
> 176	        const auto = beholder.getBrain()[order.automationId];
> 177	        const cond = auto && auto.conditions ? auto.conditions : '';
> 178	        if (cond.indexOf('TREND_CROSS') === -1) return; // não é automação de Trend Following
> 179	        const qty = parseFloat(order.quantity);
> 180	        const cur = parseFloat(beholder.getMemory(order.symbol, indexKeys.TREND_QTY)) || 0;
> 181	        let next;
> 182	        if (order.side === 'BUY' && cond.indexOf("'golden'") !== -1) {
> 183	            if (!Number.isFinite(qty) || qty <= 0) return; // guard: qty inválida não corrompe TREND_QTY
> 184	            next = cur + qty;
> 185	        }
> 186	        else if (order.side === 'SELL' && cond.indexOf("'death'") !== -1) next = 0; // vendeu a posição de trend
> 187	        else return;
> 188	        countedTrendFills.add(order.orderId);
> 189	        await beholder.updateMemory(order.symbol, indexKeys.TREND_QTY, null, next, false);
> 190	        logger('A:' + order.automationId, `TREND_QTY[${order.symbol}] ${cur} -> ${next} (fill ${order.side})`);
> 191	    } catch (err) {
> 192	        logger('system', `updateTrendPosition: ${err.message}`);
> 193	    }
> 194	}
> 195	
> 196	// orderIds de fill do Harvester já contabilizados — dedup contra um executionReport RE-ENTREGUE
> 197	// (a compra é ADITIVA na média ponderada; um report duplicado distorceria qty/custo). Também guarda
> 198	// chaves `recon:<orderId>` das reconciliações partial→cancel (subtrair 2x corromperia o bucket).
> 199	// Volátil (reseta no restart) — aceitável: um report re-entregue APÓS restart é raríssimo e o bucket
> 200	// persistido (harvestPositions) já reflete o último estado gravado. Footprint desprezível.
> 201	const countedHarvestFills = new Set();
> 202	
> 203	// Estados TERMINAIS de ordem do harvester (compartilhado entre o caminho vivo e o reconcile-on-boot).
> 204	// EXPIRED/EXPIRED_IN_MATCH são literais (não existem no enum orderStatus); EXPIRED_IN_MATCH (STP da
> 205	// Binance) é raríssimo, mas fora da lista cairia no braço "ainda aberta" e perma-travaria a venda.
> 206	const HARVEST_TERMINAL_STATUSES = [orderStatus.FILLED, orderStatus.CANCELED, orderStatus.REJECTED, 'EXPIRED', 'EXPIRED_IN_MATCH'];
> 207	
> 208	// Harvester de dislocação — mantém MEMORY['<sym>:HARVEST'] = { qty, cost } (posição TÁTICA em base asset +
> 209	// custo MÉDIO ponderado), lido pela calcQty do template SELL (quantity='HARVEST_QTY' → .qty) e pela condition
> 210	// de venda no-loss (bestBid > .cost×(1+lucro)). Distingue a ordem do harvester pelas conditions da automação
> 211	// (a compra referencia ':FAIR'; a venda ':HARVEST'), lidas do BRAIN em memória (sem ida ao banco). Compra
> 212	// FILLED soma e recalcula a média; venda FILLED zera o bucket; venda terminal NÃO-FILLED com fill parcial
> 213	// SUBTRAI o executado (reconciliação abaixo). Bucket SEPARADO do cofre — só rastreia o que o harvester
> 214	// comprou (a calcQty capa a venda na carteira). Best-effort: erro aqui não quebra o fluxo da ordem (o gate
> 215	// de venda falha fechado se HARVEST ausente). PERSISTÊNCIA: harvestPositions (upsert no fill; load no boot).
> 216	async function updateHarvestPosition(order, streamExecutedQty) {
> 217	    try {
> 218	        if (!order || !order.automationId) return;
> 219	        const auto = beholder.getBrain()[order.automationId];
> 220	        const cond = auto && auto.conditions ? auto.conditions : '';
> 221	        const isHarvestBuy = order.side === 'BUY' && cond.indexOf(':FAIR') !== -1;
> 222	        const isHarvestSell = order.side === 'SELL' && cond.indexOf(':HARVEST') !== -1;
> 223	        if (!isHarvestBuy && !isHarvestSell) return; // não é ordem do Harvester
> 224	
> 225	        // Trava de venda (HARVEST_SELLING): liberada em QUALQUER estado TERMINAL da venda do harvester.
> 226	        // FILLED zera o bucket (abaixo); CANCELED/REJECTED/EXPIRED libera p/ retry no próximo tick acima do alvo.
> 227	        // O delay de 3s do processExecutionData é benéfico aqui: o bucket zera e a trava some juntos (sem corrida
> 228	        // entre desarmar a trava e o qty>0 ainda verdadeiro). Idempotente: deleteMemory em chave ausente é no-op.
> 229	        if (isHarvestSell && HARVEST_TERMINAL_STATUSES.includes(order.status))
> 230	            beholder.deleteMemory(order.symbol, indexKeys.HARVEST_SELLING);
> 231	
> 232	        // Reconciliação partial→cancel (dívida do TL, pré-req p/ escalar o size): venda do harvester
> 233	        // que morreu NÃO-FILLED mas com fill PARCIAL já ENTREGOU parte do bucket — sem subtrair, o
> 234	        // bucket fica SUPERESTIMADO e a próxima venda no-loss venderia mais do que o harvester possui
> 235	        // (calcQty capa na CARTEIRA, não no bucket → vazaria o cofre). Usa o `z` cumulativo do
> 236	        // executionReport (streamExecutedQty) — a ordem persistida não guarda executedQty. Dedup
> 237	        // próprio (reports terminais também podem ser RE-ENTREGUES; subtrair 2x corromperia o bucket).
> 238	        if (isHarvestSell && order.status !== orderStatus.FILLED && HARVEST_TERMINAL_STATUSES.includes(order.status)) {
> 239	            const executed = parseFloat(streamExecutedQty);
> 240	            if (!Number.isFinite(executed) || executed <= 0) return; // cancel limpo (sem fill): bucket intacto
> 241	            const reconKey = `recon:${order.orderId}`;
> 242	            if (countedHarvestFills.has(reconKey)) return; // já reconciliado (report terminal re-entregue)
> 243	            const bucket = beholder.getMemory(order.symbol, indexKeys.HARVEST);
> 244	            if (!bucket) return; // sem bucket em memória, nada a reconciliar
> 245	            const bQty = Number(bucket.qty) || 0, bCost = Number(bucket.cost) || 0;
> 246	            const remaining = Number((bQty - executed).toFixed(8));
> 247	            // <= poeira (ou negativo, se o bucket já estava menor) → zera: mesma semântica do FILLED
> 248	            // (qty=0 desarma a venda; fail-closed). Custo médio NÃO muda numa venda parcial.
> 249	            const next = remaining > 1e-8
> 250	                ? { qty: remaining, cost: bCost, atMs: Date.now() }
> 251	                : { qty: 0, cost: 0, atMs: Date.now() };
> 252	            await beholder.updateMemory(order.symbol, indexKeys.HARVEST, null, next, false);
> 253	            // Marca o dedup SÓ após o updateMemory bem-sucedido (gate QA): se falhar, a chave não é
> 254	            // "queimada" e um report re-entregue reconcilia — perder a reconciliação superestima o
> 255	            // bucket, que é exatamente a direção do oversell que este fix mata.
> 256	            countedHarvestFills.add(reconKey);
> 257	            try { await harvestPositionsRepository.upsertPosition(order.symbol, next); }
> 258	            catch (e) { logger('system', `updateHarvestPosition persist: ${e.message}`); }
> 259	            logger('A:' + order.automationId, `HARVEST[${order.symbol}] reconciliado pós-${order.status}: executedQty=${executed}, qty ${bQty}->${next.qty} (cost ${next.cost})`);
> 260	            return;
> 261	        }
> 262	
> 263	        if (order.status !== orderStatus.FILLED) return; // só o fill mexe no bucket/persistência
> 264	        if (countedHarvestFills.has(order.orderId)) return; // já contabilizado (report FILLED re-entregue)
> 265	
> 266	        const cur = beholder.getMemory(order.symbol, indexKeys.HARVEST) || { qty: 0, cost: 0 };
> 267	        const curQty = Number(cur.qty) || 0, curCost = Number(cur.cost) || 0;
> 268	        let next;
> 269	        if (isHarvestBuy) {
> 270	            const qty = parseFloat(order.quantity);
> 271	            const price = parseFloat(order.avgPrice);
> 272	            if (!Number.isFinite(qty) || qty <= 0 || !Number.isFinite(price) || price <= 0) return; // guard: não corrompe o bucket
> 273	            const newQty = curQty + qty;
> 274	            const newCost = (curQty * curCost + qty * price) / newQty; // média ponderada do custo
> 275	            next = { qty: newQty, cost: newCost, atMs: Date.now() };
> 276	        }
> 277	        else { // venda no-loss FILLED → realizou o bucket inteiro → zera (qty=0 desarma a venda; fail-closed)
> 278	            next = { qty: 0, cost: 0, atMs: Date.now() };
> 279	        }
> 280	        countedHarvestFills.add(order.orderId);
> 281	        await beholder.updateMemory(order.symbol, indexKeys.HARVEST, null, next, false);
> 282	        // Persiste o bucket (resiliência a restart — sem isto a posição orfana no boot). Best-effort: falha de
> 283	        // persistência não quebra o tracking em memória; o boot recarrega o último valor efetivamente gravado.
> 284	        try { await harvestPositionsRepository.upsertPosition(order.symbol, next); }
> 285	        catch (e) { logger('system', `updateHarvestPosition persist: ${e.message}`); }
> 286	        logger('A:' + order.automationId, `HARVEST[${order.symbol}] qty ${curQty}->${next.qty} cost ${curCost}->${next.cost} (fill ${order.side})`);
> 287	    } catch (err) {
> 288	        logger('system', `updateHarvestPosition: ${err.message}`);
> 289	    }
> 290	}
> 291	
> 292	// Rastreamento do Preço Médio Ponderado (DCA) do Farm (LTC, BNB, ADA)
> 293	async function updateFarmPosition(order) {
> 294	    try {
> 295	        if (!order || order.status !== orderStatus.FILLED) return;
> 296	        const farmSymbols = ['LTCUSDT', 'BNBUSDT', 'ADAUSDT'];
> 297	        if (!farmSymbols.includes(order.symbol)) return;
> 298	
> 299	        const dca = await ordersRepository.getFarmPosition(order.symbol);
> 300	        await beholder.updateMemory(order.symbol, indexKeys.FARM_DCA, null, dca, false);
> 301	        logger('system', `FARM_DCA[${order.symbol}] atualizado: qty=${dca.qty}, cost=${dca.cost} (pós-fill de ${order.side})`);
> 302	    } catch (err) {
> 303	        logger('system', `updateFarmPosition: ${err.message}`);
> 304	    }
> 305	}
> 306	
> 307	async function loadFarmPositions() {
> 308	    try {
> 309	        const farmSymbols = ['LTCUSDT', 'BNBUSDT', 'ADAUSDT'];
> 310	        for (const symbol of farmSymbols) {
> 311	            const dca = await ordersRepository.getFarmPosition(symbol);
> 312	            await beholder.updateMemory(symbol, indexKeys.FARM_DCA, null, dca, false);
> 313	            logger('system', `FARM_DCA[${symbol}] carregado no boot: qty=${dca.qty}, cost=${dca.cost}`);
> 314	        }
> 315	    } catch (err) {
> 316	        logger('system', `loadFarmPositions: ${err.message}`);
> 317	    }
> 318	}
> 319	
> 320	// Boot-load do Harvester: recarrega os buckets persistidos p/ MEMORY (a posição sobrevive ao restart em vez de
> 321	// orfanar), RECONCILIA contra a corretora as ordens do harvester que viraram TERMINAIS com o backend OFF
> 322	// (o userData stream NÃO tem replay — sem isto o bucket recarrega errado), e RECONSTRÓI a trava HARVEST_SELLING
> 323	// só p/ vendas ainda DE FATO abertas (senão bucket + trava ausente re-disparariam a venda no 1º tick acima do
> 324	// alvo → oversell, já que calcQty capa na carteira e não no bucket). Best-effort: erro aqui não impede o boot.
> 325	// Chamado por init() (exchange já inicializado). Dívida do TL fechada: pré-req p/ escalar o size.
> 326	async function loadHarvestPositions() {
> 327	    try {
> 328	        const brain = beholder.getBrain();
> 329	
> 330	        // 0º) Buckets persistidos num mapa LOCAL primeiro — a reconciliação offline (1º/2º) ajusta o mapa
> 331	        // ANTES de armar a MEMORY, e a trava continua sendo posta antes do bucket aparecer (invariante original).
> 332	        const rows = await harvestPositionsRepository.getAll();
> 333	        const buckets = {};
> 334	        for (const r of rows)
> 335	            buckets[r.symbol] = { qty: Number(r.qty) || 0, cost: Number(r.cost) || 0, atMs: (r.atMs === undefined || r.atMs === null) ? undefined : Number(r.atMs), dirty: false };
> 336	
> 337	        // Aplica um delta de reconciliação ao bucket local (mesma matemática do updateHarvestPosition):
> 338	        // venda FILLED zera; venda parcial subtrai (custo médio intacto); compra soma na média ponderada.
> 339	        function reconBucket(symbol, fn) {
> 340	            const b = buckets[symbol] || (buckets[symbol] = { qty: 0, cost: 0, atMs: undefined, dirty: false });
> 341	            fn(b);
> 342	            b.atMs = Date.now();
> 343	            b.dirty = true;
> 344	        }
> 345	
> 346	        // 1º) VENDAS do harvester abertas no banco (in-flight no restart) — conditions têm ':HARVEST'.
> 347	        // RECONCILE-ON-BOOT: consulta a corretora (autoritativa) p/ cada uma:
> 348	        //   - ainda aberta lá → trava (comportamento original; a venda não re-dispara contra a ordem em voo);
> 349	        //   - TERMINAL offline → atualiza o DB, reconcilia o bucket e NÃO arma a trava (senão a venda ficaria
> 350	        //     silenciada p/ sempre apontando p/ uma ordem morta — era a intervenção manual que este fix mata);
> 351	        //   - REST falhou → trava (FAIL-CLOSED: melhor venda silenciada até o próximo boot do que oversell).
> 352	        const sellAutos = Object.values(brain).filter(a => a && a.conditions && a.conditions.indexOf(':HARVEST') !== -1);
> 353	        for (const a of sellAutos) {
> 354	            const open = await ordersRepository.getOpenOrdersByAutomation(a.id);
> 355	            for (const o of open) {
> 356	                let remote = null;
> 357	                try { remote = await exchange.orderStatus(o.symbol, o.orderId); }
> 358	                catch (e) { logger('system', `loadHarvestPositions: orderStatus #${o.orderId} falhou (${e.body ? JSON.stringify(e.body) : e.message}) — trava mantida (fail-closed).`); }
> 359	
> 360	                if (!remote || !HARVEST_TERMINAL_STATUSES.includes(remote.status)) {
> 361	                    await beholder.updateMemory(o.symbol, indexKeys.HARVEST_SELLING, null, { orderId: o.orderId, at: Date.now() }, false);
> 362	                    continue;
> 363	                }
> 364	
> 365	                // Terminal offline: bucket PRIMEIRO (recon + persist), DB da ordem POR ÚLTIMO (gate QA: se
> 366	                // crashar entre os dois, a ordem segue "aberta" no DB e o próximo boot RE-reconcilia — FILLED
> 367	                // re-zera (idempotente) e parcial re-subtrai (undersell, direção segura); na ordem inversa o
> 368	                // bucket stale nunca mais seria reconciliado = oversell).
> 369	                const executed = parseFloat(remote.executedQty);
> 370	                let reconciled = false;
> 371	                if (remote.status === orderStatus.FILLED) {
> 372	                    reconBucket(o.symbol, b => { b.qty = 0; b.cost = 0; }); // mesma semântica do FILLED ao vivo
> 373	                    countedHarvestFills.add(o.orderId); // um report FILLED tardio do stream não re-zera/duplica
> 374	                    reconciled = true;
> 375	                } else if (Number.isFinite(executed) && executed > 0) {
> 376	                    reconBucket(o.symbol, b => {
> 377	                        const remaining = Number((b.qty - executed).toFixed(8));
> 378	                        if (remaining > 1e-8) b.qty = remaining; else { b.qty = 0; b.cost = 0; }
> 379	                    });
> 380	                    countedHarvestFills.add(`recon:${o.orderId}`); // dedup compartilhado com a recon ao vivo
> 381	                    reconciled = true;
> 382	                }
> 383	                if (reconciled) {
> 384	                    const b = buckets[o.symbol];
> 385	                    try { await harvestPositionsRepository.upsertPosition(o.symbol, { qty: b.qty, cost: b.cost, atMs: b.atMs }); b.dirty = false; }
> 386	                    catch (e) { logger('system', `loadHarvestPositions persist: ${e.message}`); } // dirty=true → passo 3 re-tenta
> 387	                }
> 388	                try { await ordersRepository.updateOrderByOrderId(o.orderId, o.clientOrderId, { status: remote.status, ...ordersRepository.calcFillFinancials(remote, o.symbol) }); }
> 389	                catch (e) { logger('system', `loadHarvestPositions: update DB #${o.orderId}: ${e.message}`); }
> 390	                logger('system', `loadHarvestPositions: [boot-reconcile] venda #${o.orderId} (${o.symbol}) resolvida OFFLINE como ${remote.status} (executedQty=${remote.executedQty}); bucket ${reconciled ? 'reconciliado' : 'intacto (cancel limpo)'}, trava NÃO rearmada.`);
> 391	                telegramNotify.notify(`🔁 [BOOT] Venda do harvester #${o.orderId} (${o.symbol}) resolveu OFFLINE como ${remote.status} (exec=${remote.executedQty}). Bucket ${reconciled ? 'reconciliado' : 'intacto'} no boot.`, `bootrecon:${o.orderId}`).catch(() => { });
> 392	            }
> 393	        }
> 394	
> 395	        // 2º) COMPRAS do harvester abertas no banco — conditions têm ':FAIR'. Compra que FILLOU (ou parcial)
> 396	        // com o backend OFF soma no bucket — senão a posição ORFANA na carteira (foi exatamente o que orfanou
> 397	        // a canary 0,00015 no deploy de 2026-06-09). Direção segura (undersell nunca; só evita órfã).
> 398	        const buyAutos = Object.values(brain).filter(a => a && a.conditions && a.conditions.indexOf(':FAIR') !== -1);
> 399	        for (const a of buyAutos) {
> 400	            const open = await ordersRepository.getOpenOrdersByAutomation(a.id);
> 401	            for (const o of open) {
> 402	                let remote = null;
> 403	                try { remote = await exchange.orderStatus(o.symbol, o.orderId); }
> 404	                catch (e) { logger('system', `loadHarvestPositions: orderStatus #${o.orderId} falhou (${e.body ? JSON.stringify(e.body) : e.message}) — compra fica como está (reconcilia no próximo boot se executou).`); }
> 405	                if (!remote || !HARVEST_TERMINAL_STATUSES.includes(remote.status)) continue; // aberta segue aberta (compra não trava nada)
> 406	
> 407	                // Gate QA: a idempotência da SOMA depende do status terminal ficar gravado no DB (o Set de
> 408	                // dedup não sobrevive a restart) — sem o update confirmado, NÃO soma (re-somar num boot
> 409	                // seguinte superestimaria o bucket = oversell; adiar deixa só uma órfã temporária = seguro).
> 410	                let updated = null;
> 411	                try { updated = await ordersRepository.updateOrderByOrderId(o.orderId, o.clientOrderId, { status: remote.status, ...ordersRepository.calcFillFinancials(remote, o.symbol) }); }
> 412	                catch (e) { logger('system', `loadHarvestPositions: update DB #${o.orderId}: ${e.message}`); }
> 413	                if (!updated) { logger('system', `loadHarvestPositions: compra #${o.orderId} terminal offline mas o DB não confirmou — soma adiada p/ o próximo boot (anti re-soma).`); continue; }
> 414	
> 415	                const executed = parseFloat(remote.executedQty);
> 416	                const cumm = parseFloat(remote.cummulativeQuoteQty);
> 417	                if (!Number.isFinite(executed) || executed <= 0 || !Number.isFinite(cumm) || cumm <= 0) continue; // cancel/expire limpo: nada executou
> 418	                const price = cumm / executed;
> 419	                reconBucket(o.symbol, b => {
> 420	                    const newQty = b.qty + executed;
> 421	                    b.cost = (b.qty * b.cost + executed * price) / newQty; // média ponderada (igual ao vivo)
> 422	                    b.qty = newQty;
> 423	                });
> 424	                countedHarvestFills.add(o.orderId); // FILLED tardio do stream não soma 2x
> 425	                logger('system', `loadHarvestPositions: [boot-reconcile] compra #${o.orderId} (${o.symbol}) executou OFFLINE (${remote.status}, qty=${executed}@${price}); somada ao bucket (anti-órfã).`);
> 426	                telegramNotify.notify(`🔁 [BOOT] Compra do harvester #${o.orderId} (${o.symbol}) executou OFFLINE (qty=${executed} @ ${price.toFixed(2)}). Somada ao bucket no boot.`, `bootrecon:${o.orderId}`).catch(() => { });
> 427	            }
> 428	        }
> 429	
> 430	        // 3º) Arma a MEMORY a partir do mapa reconciliado e persiste o que mudou.
> 431	        const loaded = [];
> 432	        for (const [symbol, b] of Object.entries(buckets)) {
> 433	            // Guard (gate QA [ALTO]): se o handler VIVO já escreveu HARVEST p/ este símbolo durante o boot
> 434	            // (fill chegando enquanto a recon fazia REST), o estado vivo é MAIS FRESCO e já foi persistido por
> 435	            // ele — armar o snapshot do passo 0 aqui ressuscitaria um bucket morto SEM trava (oversell).
> 436	            if (beholder.getMemory(symbol, indexKeys.HARVEST)) {
> 437	                logger('system', `loadHarvestPositions: ${symbol} já tem HARVEST vivo (fill durante o boot) — snapshot do boot descartado.`);
> 438	                continue;
> 439	            }
> 440	            if (b.dirty) {
> 441	                try { await harvestPositionsRepository.upsertPosition(symbol, { qty: b.qty, cost: b.cost, atMs: b.atMs }); }
> 442	                catch (e) { logger('system', `loadHarvestPositions persist: ${e.message}`); }
> 443	            }
> 444	            if (b.qty <= 0) continue; // bucket vazio → HARVEST ausente (mesma semântica do estado fresco; venda não avalia)
> 445	            await beholder.updateMemory(symbol, indexKeys.HARVEST, null, { qty: b.qty, cost: b.cost, atMs: b.atMs }, false);
> 446	            loaded.push(`${symbol}:qty=${b.qty}@${b.cost}`);
> 447	        }
> 448	
> 449	        if (loaded.length) logger('system', `Harvester buckets recarregados: ${loaded.join(', ')}.`);
> 450	    } catch (err) {
> 451	        logger('system', `loadHarvestPositions: ${err.message}`);
> 452	    }
> 453	}
> 454	
> 455	function processExecutionData(monitorId, executionData, broadcastLabel) {
> 456	    if (executionData.x === orderStatus.NEW) return;//ignora as novas, pois podem ter vindo de outras fontes
> 457	
> 458	    const order = {
> 459	        symbol: executionData.s,
> 460	        orderId: executionData.i,
> 461	        clientOrderId: executionData.X === orderStatus.CANCELED ? executionData.C : executionData.c,
> 462	        side: executionData.S,
> 463	        type: executionData.o,
> 464	        status: executionData.X,
> 465	        isMaker: executionData.m,
> 466	        transactTime: executionData.T
> 467	    }
> 468	
> 469	    if (order.status === orderStatus.FILLED) {
> 470	        const quoteAmount = parseFloat(executionData.Z);
> 471	        order.avgPrice = quoteAmount / parseFloat(executionData.z);
> 472	        order.commission = executionData.n;
> 473	        order.quantity = executionData.q;
> 474	        const isQuoteCommission = executionData.N && order.symbol.endsWith(executionData.N);
> 475	        order.net = isQuoteCommission ? quoteAmount - parseFloat(order.commission) : quoteAmount;
> 476	    }
> 477	
> 478	    if (order.status === orderStatus.REJECTED) order.obs = executionData.r;
> 479	
> 480	    setTimeout(async () => {
> 481	        try {
> 482	            const updatedOrder = await ordersRepository.updateOrderByOrderId(order.orderId, order.clientOrderId, order);
> 483	            if (updatedOrder) {
> 484	
> 485	                notifyOrderUpdate(order);
> 486	                // Telegram pro dono (pedido: notificar todas as ordens). Best-effort + dedup interno
> 487	                // por orderId+status (reports re-entregues não duplicam; MARKET já notificada no insert
> 488	                // não re-notifica aqui). Síncrona e não-lançante — não atrasa nem quebra o caminho quente.
> 489	                telegramNotify.notifyOrder(updatedOrder.get({ plain: true }));
> 490	
> 491	                const orderCopy = getLightOrder(updatedOrder.get({ plain: true }));
> 492	                const results = await beholder.updateMemory(order.symbol, indexKeys.LAST_ORDER, null, orderCopy);
> 493	                if (results) results.map(r => sendMessage({ notification: r }));
> 494	
> 495	                await updateTrendPosition(updatedOrder.get({ plain: true }));
> 496	                // z = qty executada CUMULATIVA do executionReport (autoritativa p/ a reconciliação
> 497	                // partial→cancel da venda do harvester; a ordem persistida não guarda executedQty).
> 498	                await updateHarvestPosition(updatedOrder.get({ plain: true }), executionData.z);
> 499	                await updateFarmPosition(updatedOrder.get({ plain: true }));
> 500	
> 501	                if (broadcastLabel) sendMessage({ [broadcastLabel]: order });
> 502	            }
> 503	        } catch (err) {
> 504	            logger('M:' + monitorId, err);
> 505	        }
> 506	    }, 3000)
> 507	}
> 508	
> 509	// Trata o evento cru `listStatus` da OCO (data.e === 'listStatus'). Campos relevantes:
> 510	// g=orderListId, s=symbol, l=listStatusType, L=listOrderStatus, O=[{s,i,c}] (pernas).
> 511	// Quando uma perna executa, a Binance cancela a outra automaticamente; os executionReport
> 512	// por-perna já atualizam cada ordem. Aqui só agimos quando a lista RESOLVE (ALL_DONE/REJECT)
> 513	// e fazemos uma reconciliação de segurança: se alguma perna ainda estiver NEW na base,
> 514	// busca o status real na corretora (autoritativo) e atualiza — cobre um executionReport
> 515	// eventualmente perdido no stream. Idempotente: updateOrder só sai de NEW/PARTIALLY_FILLED.
> 516	function processListStatusData(monitorId, data, broadcastLabel) {
> 517	    const orderListId = data.g;
> 518	    const symbol = data.s;
> 519	    const listOrderStatus = data.L;
> 520	
> 521	    if (listOrderStatus !== 'ALL_DONE' && listOrderStatus !== 'REJECT') return;
> 522	
> 523	    setTimeout(async () => {
> 524	        try {
> 525	            const legs = Array.isArray(data.O) ? data.O : [];
> 526	            await Promise.all(legs.map(async (leg) => {
> 527	                const legOrderId = leg.i;
> 528	                const legClientOrderId = leg.c;
> 529	
> 530	                const current = await ordersRepository.getOrder(legOrderId, legClientOrderId);
> 531	                if (!current) return; // perna não persistida (ex.: OCO criada fora do TradeUX)
> 532	                if (current.status !== orderStatus.NEW && current.status !== orderStatus.PARTIALLY_FILLED)
> 533	                    return; // já terminal: o executionReport por-perna já tratou
> 534	
> 535	                const remote = await exchange.orderStatus(symbol, legOrderId);
> 536	                const updated = await ordersRepository.updateOrderByOrderId(legOrderId, legClientOrderId, { status: remote.status });
> 537	                if (updated) {
> 538	                    notifyOrderUpdate(updated.get({ plain: true }));
> 539	                    telegramNotify.notifyOrder(updated.get({ plain: true })); // dedup cobre o caso do report por-perna já ter notificado
> 540	                    const orderCopy = getLightOrder(updated.get({ plain: true }));
> 541	                    const results = await beholder.updateMemory(symbol, indexKeys.LAST_ORDER, null, orderCopy);
> 542	                    if (results) results.map(r => sendMessage({ notification: r }));
> 543	                }
> 544	            }));
> 545	
> 546	            sendMessage({ notification: { text: `OCO list #${orderListId} resolved (${listOrderStatus}) on ${symbol}`, type: listOrderStatus === 'ALL_DONE' ? 'success' : 'error' } });
> 547	            if (broadcastLabel) sendMessage({ [broadcastLabel]: { orderListId, symbol, listOrderStatus } });
> 548	            logger('M:' + monitorId, `listStatus ${listOrderStatus} for OCO #${orderListId} (${symbol}) reconciled.`);
> 549	        } catch (err) {
> 550	            logger('M:' + monitorId, err);
> 551	        }
> 552	    }, OCO_RECONCILE_DELAY_MS);
> 553	}
> 554	
> 555	async function processBalanceData(monitorId, broadcastLabel, logs, data) {
> 556	    if (logs) logger('M:' + monitorId, data);
> 557	
> 558	    try {
> 559	        const wallet = await loadWallet();
> 560	        if (broadcastLabel && WSS) sendMessage({ [broadcastLabel]: wallet });
> 561	    } catch (err) {
> 562	        if (logs) logger('M:' + monitorId, err);
> 563	    }
> 564	}
> 565	
> 566	async function startUserDataMonitor(monitorId, broadcastLabel, logs) {
> 567	    const [balanceBroadcast, executionBroadcast] = broadcastLabel ? broadcastLabel.split(',') : [null, null];
> 568	
> 569	    try {
> 570	        await loadWallet();
> 571	
> 572	        if (!exchange) return new Error('Exchange Monitor not initialized yet.');
> 573	        exchange.userDataStream(
> 574	            data => {
> 575	                if (data.e === 'executionReport')
> 576	                    processExecutionData(monitorId, data, executionBroadcast);
> 577	                else if (data.e === 'balanceUpdate' || data.e === 'outboundAccountPosition')
> 578	                    processBalanceData(monitorId, balanceBroadcast, logs, data)
> 579	            },
> 580	            // 2º callback dedicado ao listStatus (OCO). O all_updates_callback acima também
> 581	            // recebe o listStatus, mas o tratamos SÓ aqui para não processar em duplicidade.
> 582	            listStatusData => processListStatusData(monitorId, listStatusData, executionBroadcast)
> 583	        )
> 584	
> 585	        logger('M:' + monitorId, 'User Data Monitor has started!');
> 586	    } catch (err) {
> 587	        logger('M:' + monitorId, 'User Data Monitor has NOT started!\n' + err.message);
> 588	    }
> 589	}
> 590	
> 591	async function processChartData(monitorId, symbol, indexes, interval, ohlc, logs) {
> 592	    if (typeof indexes === 'string') indexes = indexes.split(',');
> 593	    if (!indexes || !Array.isArray(indexes) || indexes.length === 0) return false;
> 594	
> 595	    const memoryKeys = [];
> 596	
> 597	    indexes.map(index => {
> 598	        const params = index.split('_');
> 599	        const indexName = params[0];
> 600	        params.splice(0, 1);
> 601	
> 602	        try {
> 603	            const calc = execCalc(indexName, ohlc, ...params);
> 604	            if (logs) logger('M:' + monitorId, `${index}_${interval} calculated: ${JSON.stringify(calc.current ? calc.current : calc)}`);
> 605	            beholder.updateMemory(symbol, index, interval, calc, false);
> 606	
> 607	            memoryKeys.push(beholder.parseMemoryKey(symbol, index, interval));
> 608	        } catch (err) {
> 609	            logger('M:' + monitorId, `Exchange Monitor => Can't calc the index ${index}:`);
> 610	            logger('M:' + monitorId, err);
> 611	        }
> 612	    });
> 613	
> 614	    return Promise.all(memoryKeys.map(async (key) => {
> 615	        return beholder.testAutomations(key);
> 616	    }))
> 617	}
> 618	
> 619	function startChartMonitor(monitorId, symbol, interval, indexes, broadcastLabel, logs) {
> 620	    if (!symbol) return new Error(`Can't start a Chart Monitor without a symbol.`);
> 621	    if (!exchange) return new Error('Exchange Monitor not initialized yet.');
> 622	
> 623	    exchange.chartStream(symbol, interval || '1m', async (ohlc) => {
> 624	        const lastCandle = {
> 625	            open: ohlc.open[ohlc.open.length - 1],
> 626	            close: ohlc.close[ohlc.close.length - 1],
> 627	            high: ohlc.high[ohlc.high.length - 1],
> 628	            low: ohlc.low[ohlc.low.length - 1],
> 629	            volume: ohlc.volume[ohlc.volume.length - 1],
> 630	        };
> 631	
> 632	        const previousCandle = {
> 633	            open: ohlc.open[ohlc.open.length - 2],
> 634	            close: ohlc.close[ohlc.close.length - 2],
> 635	            high: ohlc.high[ohlc.high.length - 2],
> 636	            low: ohlc.low[ohlc.low.length - 2],
> 637	            volume: ohlc.volume[ohlc.volume.length - 2],
> 638	        };
> 639	
> 640	        const previousPreviousCandle = {
> 641	            open: ohlc.open[ohlc.open.length - 3],
> 642	            close: ohlc.close[ohlc.close.length - 3],
> 643	            high: ohlc.high[ohlc.high.length - 3],
> 644	            low: ohlc.low[ohlc.low.length - 3],
> 645	            volume: ohlc.volume[ohlc.volume.length - 3],
> 646	        };
> 647	
> 648	        if (logs) logger('M:' + monitorId, lastCandle);
> 649	
> 650	        try {
> 651	            beholder.updateMemory(symbol, indexKeys.LAST_CANDLE, interval, { current: lastCandle, previous: previousCandle }, false);
> 652	            beholder.updateMemory(symbol, indexKeys.PREVIOUS_CANDLE, interval, { current: previousCandle, previous: previousPreviousCandle }, false);
> 653	
> 654	            if (broadcastLabel && WSS) sendMessage({ [broadcastLabel]: lastCandle });
> 655	
> 656	            let results = await processChartData(monitorId, symbol, indexes, interval, ohlc, logs);
> 657	
> 658	            if (results) {
> 659	                results.push(await beholder.testAutomations(beholder.parseMemoryKey(symbol, indexKeys.LAST_CANDLE, interval)));
> 660	                results.push(await beholder.testAutomations(beholder.parseMemoryKey(symbol, indexKeys.PREVIOUS_CANDLE, interval)));
> 661	
> 662	                if (logs) logger('M:' + monitorId, `chartStream Results: ${results}`);
> 663	                results.flat().map(r => sendMessage({ notification: r }));
> 664	            }
> 665	        } catch (err) {
> 666	            if (logs) logger('M:' + monitorId, err);
> 667	        }
> 668	    })
> 669	    logger('M:' + monitorId, `Chart Monitor has started for ${symbol}_${interval}!`);
> 670	}
> 671	
> 672	function stopChartMonitor(monitorId, symbol, interval, indexes, logs) {
> 673	    if (!symbol) return new Error(`Can't stop a Chart Monitor without a symbol.`);
> 674	    if (!exchange) return new Error('Exchange Monitor not initialized yet.');
> 675	    exchange.terminateChartStream(symbol, interval);
> 676	    if (logs) logger('M:' + monitorId, `Chart Monitor ${symbol}_${interval} stopped!`);
> 677	
> 678	    beholder.deleteMemory(symbol, indexKeys.LAST_CANDLE, interval);
> 679	    beholder.deleteMemory(symbol, indexKeys.PREVIOUS_CANDLE, interval);
> 680	
> 681	    if (indexes && Array.isArray(indexes))
> 682	        indexes.map(ix => beholder.deleteMemory(symbol, ix, interval));
> 683	}
> 684	
> 685	function stopTickerMonitor(monitorId, symbol, logs) {
> 686	    if (!symbol) return new Error(`Can't stop a Ticker Monitor without a symbol.`);
> 687	    if (!exchange) return new Error('Exchange Monitor not initialized yet.');
> 688	
> 689	    exchange.terminateTickerStream(symbol);
> 690	
> 691	    if (logs) logger('M:' + monitorId, `Ticker Monitor ${symbol} stopped!`);
> 692	
> 693	    beholder.deleteMemory(symbol, indexKeys.TICKER);
> 694	}
> 695	
> 696	function getLightTicker(data) {
> 697	    delete data.eventType;
> 698	    delete data.eventTime;
> 699	    delete data.symbol;
> 700	    delete data.openTime;
> 701	    delete data.closeTime;
> 702	    delete data.firstTradeId;
> 703	    delete data.lastTradeId;
> 704	    delete data.numTrades;
> 705	    delete data.closeQty;
> 706	    delete data.bestBidQty;
> 707	    delete data.bestAskQty;
> 708	
> 709	    data.quoteVolume = parseFloat(data.quoteVolume);
> 710	    data.volume = parseFloat(data.volume);
> 711	    data.priceChange = parseFloat(data.priceChange);
> 712	    data.percentChange = parseFloat(data.percentChange);
> 713	    data.averagePrice = parseFloat(data.averagePrice);
> 714	    data.prevClose = parseFloat(data.prevClose);
> 715	    data.high = parseFloat(data.high);
> 716	    data.low = parseFloat(data.low);
> 717	    data.open = parseFloat(data.open);
> 718	    data.close = parseFloat(data.close);
> 719	    data.bestBid = parseFloat(data.bestBid);
> 720	    data.bestAsk = parseFloat(data.bestAsk);
> 721	
> 722	    return data;
> 723	}
> 724	
> 725	async function startTickerMonitor(monitorId, symbol, broadcastLabel, logs) {
> 726	    if (!symbol) return new Error(`Can't start a Ticker Monitor without a symbol.`);
> 727	    if (!exchange) return new Error('Exchange Monitor not initialized yet.');
> 728	
> 729	    exchange.tickerStream(symbol, async (data) => {
> 730	        if (logs) logger('M:' + monitorId, data);
> 731	
> 732	        try {
> 733	            const ticker = getLightTicker({ ...data });
> 734	            const currentMemory = beholder.getMemory(symbol, indexKeys.TICKER);
> 735	
> 736	            const newMemory = {};
> 737	            newMemory.previous = currentMemory ? currentMemory.current : ticker;
> 738	            newMemory.current = ticker;
> 739	
> 740	            const results = await beholder.updateMemory(data.symbol, indexKeys.TICKER, null, newMemory);
> 741	            if (results) results.map(r => sendMessage({ notification: r }));
> 742	
> 743	            if (WSS && broadcastLabel) sendMessage({ [broadcastLabel]: data });
> 744	        }
> 745	        catch (err) {
> 746	            if (logs) logger('M:' + monitorId, err);
> 747	        }
> 748	    })
> 749	    logger('M:' + monitorId, `Ticker Monitor has started for ${symbol}`);
> 750	}
> 751	
> 752	async function sendMessage(json) {
> 753	    try {
> 754	        if (json.notification) {
> 755	            const settings = await getDefaultSettings();
> 756	            push.send(settings, json.notification.text, 'Beholder Notification', json.notification);
> 757	        }
> 758	    } catch (err) { }
> 759	
> 760	    return WSS.broadcast(json);
> 761	}
> 762	
> 763	async function init(settings, wssInstance, beholderInstance) {
> 764	    if (!settings || !beholderInstance) throw new Error(`You can't init the Exchange Monitor App without his settings. Check your database and/or startup code.`);
> 765	
> 766	    WSS = wssInstance;
> 767	    beholder = beholderInstance;
> 768	    exchange = require('./utils/exchange')(settings);
> 769	
> 770	    // Recarrega + RECONCILIA os buckets do Harvester ANTES de subir os monitores (gate TL): com o
> 771	    // userData stream ainda fora do ar, a reconciliação de boot não corre contra fills ao vivo —
> 772	    // o guard do passo 3 vira cinto, não a única defesa. Ver loadHarvestPositions.
> 773	    await loadHarvestPositions();
> 774	    await loadFarmPositions();
> 775	
> 776	    const monitors = await getActiveMonitors();
> 777	    monitors.map(m => {
> 778	        setTimeout(() => {
> 779	            switch (m.type) {
> 780	                case monitorTypes.MINI_TICKER:
> 781	                    return startMiniTickerMonitor(m.id, m.broadcastLabel, m.logs);
> 782	                case monitorTypes.BOOK:
> 783	                    return startBookMonitor(m.id, m.broadcastLabel, m.logs);
> 784	                case monitorTypes.USER_DATA: {
> 785	                    if (!settings.accessKey || !settings.secretKey) return;
> 786	                    return startUserDataMonitor(m.id, m.broadcastLabel, m.logs);
> 787	                }
> 788	                case monitorTypes.CANDLES:
> 789	                    return startChartMonitor(m.id, m.symbol, m.interval, m.indexes ? m.indexes.split(',') : [], m.broadcastLabel, m.logs);
> 790	                case monitorTypes.TICKER:
> 791	                    return startTickerMonitor(m.id, m.symbol, m.broadcastLabel, m.logs);
> 792	            }
> 793	        }, 250)//Binance only permits 5 commands / second
> 794	    })
> 795	
> 796	    const lastOrders = await ordersRepository.getLastFilledOrders();
> 797	    await Promise.all(lastOrders.map(async (order) => {
> 798	        const orderCopy = getLightOrder(order.get({ plain: true }));
> 799	        await beholder.updateMemory(order.symbol, indexKeys.LAST_ORDER, null, orderCopy, false);
> 800	    }))
> 801	
> 802	    logger('system', 'App Exchange Monitor is running!');
> 803	}
> 804	
> 805	module.exports = {
> 806	    init,
> 807	    startChartMonitor,
> 808	    stopChartMonitor,
> 809	    startTickerMonitor,
> 810	    stopTickerMonitor,
> 811	    sendMessage
> 812	}
> 813	
> ```

## 🤖 Claude *(18:55:46)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/src/beholder.js"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	const { getDefaultSettings } = require('./repositories/settingsRepository');
> 2	const { actionTypes } = require('./repositories/actionsRepository');
> 3	const orderTemplatesRepository = require('./repositories/orderTemplatesRepository');
> 4	const automationsRepository = require('./repositories/automationsRepository');
> 5	const withdrawTemplatesRepository = require('./repositories/withdrawTemplatesRepository');
> 6	const gridsRepository = require('./repositories/gridsRepository');
> 7	const { getSymbol } = require('./repositories/symbolsRepository');
> 8	const { STOP_TYPES, LIMIT_TYPES, insertOrder, getOpenOcoOrders, calcFillFinancials } = require('./repositories/ordersRepository');
> 9	const db = require('./db');
> 10	const logger = require('./utils/logger');
> 11	const telegramNotify = require('./utils/telegramNotify');
> 12	
> 13	const MEMORY = {};
> 14	
> 15	let BRAIN = {};
> 16	
> 17	let LOCK_BRAIN = {};
> 18	
> 19	let BRAIN_INDEX = {};
> 20	
> 21	let LOCK_MEMORY = false;
> 22	
> 23	const LOGS = process.env.BEHOLDER_LOGS === 'true';
> 24	const INTERVAL = parseInt(process.env.AUTOMATION_INTERVAL || 0);
> 25	
> 26	function init(automations) {
> 27	
> 28	    try {
> 29	        setLocked(automations.map(a => a.id), true);
> 30	        LOCK_MEMORY = true;
> 31	
> 32	        BRAIN = {};
> 33	        BRAIN_INDEX = {};
> 34	
> 35	        automations.map(auto => {
> 36	            if (auto.isActive && !auto.schedule)
> 37	                updateBrain(auto)
> 38	        });
> 39	    } finally {
> 40	        setLocked(automations.map(a => a.id), false);
> 41	        LOCK_MEMORY = false;
> 42	        logger('beholder', 'Beholder Brain has started!');
> 43	    }
> 44	}
> 45	
> 46	function isLocked(automationId) {
> 47	    if (Array.isArray(automationId))
> 48	        return automationId.some(id => LOCK_BRAIN[id] === true);
> 49	    return LOCK_BRAIN[automationId] === true;
> 50	}
> 51	
> 52	function setLocked(automationId, value) {
> 53	    if (Array.isArray(automationId))
> 54	        return automationId.map(id => LOCK_BRAIN[id] = value);
> 55	    LOCK_BRAIN[automationId] = value;
> 56	}
> 57	
> 58	function updateBrainIndex(index, automationId) {
> 59	    if (!BRAIN_INDEX[index]) BRAIN_INDEX[index] = [];
> 60	    BRAIN_INDEX[index].push(automationId);
> 61	
> 62	    if (index.startsWith('*')) BRAIN_INDEX.hasWildcard = true;
> 63	}
> 64	
> 65	function deleteBrainIndex(indexes, automationId) {
> 66	    if (typeof indexes === 'string') indexes = indexes.split(',');
> 67	    indexes.forEach(ix => {
> 68	        if (!BRAIN_INDEX[ix] || BRAIN_INDEX[ix].length === 0) return;
> 69	        const pos = BRAIN_INDEX[ix].findIndex(id => id === automationId);
> 70	        BRAIN_INDEX[ix].splice(pos, 1);
> 71	    });
> 72	
> 73	    if (BRAIN_INDEX.hasWildcard)
> 74	        BRAIN_INDEX.hasWildcard = Object.entries(BRAIN_INDEX).some(p => p[0].startsWith('*'));
> 75	}
> 76	
> 77	function updateBrain(automation) {
> 78	    if (!automation.isActive || !automation.conditions) return;
> 79	
> 80	    const actions = automation.actions ? automation.actions.map(a => {
> 81	        a = a.toJSON ? a.toJSON() : a;
> 82	        delete a.createdAt;
> 83	        delete a.updatedAt;
> 84	        //delete a.orderTemplate;
> 85	        return a;
> 86	    }) : [];
> 87	
> 88	    const grids = automation.grids ? automation.grids.map(g => {
> 89	        g = g.toJSON ? g.toJSON() : g;
> 90	        delete g.createdAt;
> 91	        delete g.updatedAt;
> 92	        delete g.automationId;
> 93	        if (g.orderTemplate) {
> 94	            delete g.orderTemplate.createdAt;
> 95	            delete g.orderTemplate.updatedAt;
> 96	            delete g.orderTemplate.name;
> 97	        }
> 98	        return g;
> 99	    }) : [];
> 100	
> 101	    if (automation.toJSON)
> 102	        automation = automation.toJSON();
> 103	
> 104	    delete automation.createdAt;
> 105	    delete automation.updatedAt;
> 106	
> 107	    automation.actions = actions;
> 108	    automation.grids = grids;
> 109	
> 110	    BRAIN[automation.id] = automation;
> 111	    automation.indexes.split(',').map(ix => updateBrainIndex(ix, automation.id));
> 112	}
> 113	
> 114	function deleteBrain(automation) {
> 115	    try {
> 116	        setLocked(automation.id, true);
> 117	        delete BRAIN[automation.id];
> 118	        deleteBrainIndex(automation.indexes.split(','), automation.id);
> 119	        if (automation.logs) logger('A:' + automation.id, `Automation removed from BRAIN #${automation.id}`);
> 120	    }
> 121	    finally {
> 122	        setLocked(automation.id, false);
> 123	    }
> 124	}
> 125	
> 126	function findAutomations(indexKey) {
> 127	    let ids = [];
> 128	    if (BRAIN_INDEX.hasWildcard) {
> 129	        const props = Object.entries(BRAIN_INDEX).filter(p => indexKey.endsWith(p[0].replace('*', '')));
> 130	        ids = props.map(p => p[1]).flat();
> 131	    }
> 132	    else
> 133	        ids = BRAIN_INDEX[indexKey];
> 134	
> 135	    if (!ids) return [];
> 136	    return [...new Set(ids)].map(id => BRAIN[id]);
> 137	}
> 138	
> 139	function invertCondition(memoryKey, conditions) {
> 140	    const conds = conditions.split(' && ');
> 141	    const condToInvert = conds.find(c => c.indexOf(memoryKey) !== -1 && c.indexOf('current') !== -1);
> 142	    if (!condToInvert) return false;
> 143	
> 144	    if (condToInvert.indexOf('>=') != -1) return condToInvert.replace('>=', '<').replace(/current/g, 'previous');
> 145	    if (condToInvert.indexOf('<=') != -1) return condToInvert.replace('<=', '>').replace(/current/g, 'previous');
> 146	    if (condToInvert.indexOf('>') != -1) return condToInvert.replace('>', '<').replace(/current/g, 'previous');
> 147	    if (condToInvert.indexOf('<') != -1) return condToInvert.replace('<', '>').replace(/current/g, 'previous');
> 148	    if (condToInvert.indexOf('!') != -1) return condToInvert.replace('!', '=').replace(/current/g, 'previous');
> 149	    if (condToInvert.indexOf('==') != -1) return condToInvert.replace('==', '!==').replace(/current/g, 'previous');
> 150	    return false;
> 151	}
> 152	
> 153	async function sendSms(settings, automation) {
> 154	    await require('./utils/sms')(settings, automation.name + ' has fired!');
> 155	    if (automation.logs) logger('A:' + automation.id, `SMS sent!`);
> 156	    return { text: `SMS sent from automation '${automation.name}'`, type: 'success' };
> 157	}
> 158	
> 159	async function sendEmail(settings, automation) {
> 160	    await require('./utils/email')(settings, automation.name + ' has fired!');
> 161	    if (automation.logs) logger('A:' + automation.id, `E-mail sent!`);
> 162	    return { text: `E-mail sent from automation '${automation.name}'`, type: 'success' };
> 163	}
> 164	
> 165	function calcPrice(orderTemplate, symbol, isStopPrice) {
> 166	    const tickSize = parseFloat(symbol.tickSize);
> 167	    let newPrice, factor;
> 168	
> 169	    // OCO usa preços explícitos (TP em limitPrice, stop em stopPrice), igual aos tipos LIMIT.
> 170	    if (LIMIT_TYPES.includes(orderTemplate.type) || orderTemplate.type === 'OCO') {
> 171	        try {
> 172	            if (!isStopPrice) {
> 173	                if (parseFloat(orderTemplate.limitPrice)) return orderTemplate.limitPrice;
> 174	                newPrice = Function("MEMORY", "return " + getEval(orderTemplate.limitPrice))(MEMORY) * orderTemplate.limitPriceMultiplier;
> 175	            }
> 176	            else {
> 177	                if (parseFloat(orderTemplate.stopPrice)) return orderTemplate.stopPrice;
> 178	                newPrice = Function("MEMORY", "return " + getEval(orderTemplate.stopPrice))(MEMORY) * orderTemplate.stopPriceMultiplier;
> 179	            }
> 180	        }
> 181	        catch (err) {
> 182	            if (isStopPrice)
> 183	                throw new Error(`Error trying to calc Stop Price with params: ${orderTemplate.stopPrice} x ${orderTemplate.stopPriceMultiplier}. Error: ${err.message}`);
> 184	            else
> 185	                throw new Error(`Error trying to calc Limit Price with params: ${orderTemplate.limitPrice} x ${orderTemplate.limitPriceMultiplier}. Error: ${err.message}`);
> 186	        }
> 187	    }
> 188	    else {
> 189	        const memory = MEMORY[`${orderTemplate.symbol}:BOOK`];
> 190	        if (!memory)
> 191	            throw new Error(`Error trying to get market price. OTID: ${orderTemplate.id}, ${isStopPrice}. No Book.`);
> 192	
> 193	        newPrice = orderTemplate.side === 'BUY' ? memory.current.bestAsk : memory.current.bestBid;
> 194	        newPrice = isStopPrice ? newPrice * orderTemplate.stopPriceMultiplier : newPrice * orderTemplate.limitPriceMultiplier;
> 195	    }
> 196	
> 197	    factor = Math.floor(newPrice / tickSize);
> 198	    return (factor * tickSize).toFixed(symbol.quotePrecision);
> 199	}
> 200	
> 201	function calcQty(orderTemplate, price, symbol) {
> 202	    let asset;
> 203	
> 204	    if (orderTemplate.side === 'BUY') {
> 205	        asset = parseFloat(MEMORY[`${symbol.quote}:WALLET`]);
> 206	        if (!asset) throw new Error(`There is no ${symbol.quote} in your wallet to place a buy.`);
> 207	    }
> 208	    else {
> 209	        asset = parseFloat(MEMORY[`${symbol.base}:WALLET`]);
> 210	        if (!asset) throw new Error(`There is no ${symbol.base} in your wallet to place a sell.`);
> 211	    }
> 212	
> 213	    let qty = orderTemplate.quantity.replace(',', '.');
> 214	    if (parseFloat(qty)) return qty;
> 215	
> 216	    const multiplier = orderTemplate.quantityMultiplier;
> 217	    const stepSize = parseFloat(symbol.stepSize);
> 218	
> 219	    let newQty, factor;
> 220	    if (orderTemplate.quantity === 'MAX_WALLET') {
> 221	        if (orderTemplate.side === 'BUY')
> 222	            newQty = (parseFloat(asset) / parseFloat(price)) * (multiplier > 1 ? 1 : multiplier);
> 223	        else
> 224	            newQty = parseFloat(asset) * (multiplier > 1 ? 1 : multiplier);
> 225	    }
> 226	    else if (orderTemplate.quantity === 'MIN_NOTIONAL') {
> 227	        newQty = (parseFloat(symbol.minNotional) / parseFloat(price)) * (multiplier < 1 ? 1 : multiplier);
> 228	    }
> 229	    else if (orderTemplate.quantity === 'LAST_ORDER_QTY') {
> 230	        const lastOrder = MEMORY[`${orderTemplate.symbol}:LAST_ORDER`];
> 231	        if (!lastOrder)
> 232	            throw new Error(`There is no last order to use as qty reference for ${orderTemplate.symbol}.`);
> 233	
> 234	        newQty = parseFloat(lastOrder.quantity) * multiplier;
> 235	        if (orderTemplate.side === 'SELL' && newQty > asset) newQty = asset;
> 236	    }
> 237	    else if (orderTemplate.quantity === 'TREND_QTY') {
> 238	        // Posição acumulada pelo Trend Following (escrita no fill por app-em.updateTrendPosition):
> 239	        // id6 (golden) soma; id7 (death) vende ESTA qty (não a LAST_ORDER, que é compartilhada com a id3).
> 240	        const trendQty = parseFloat(MEMORY[`${orderTemplate.symbol}:TREND_QTY`]);
> 241	        if (!trendQty || trendQty <= 0)
> 242	            throw new Error(`There is no trend position (TREND_QTY) to use as qty reference for ${orderTemplate.symbol}.`);
> 243	
> 244	        newQty = trendQty * multiplier;
> 245	        if (orderTemplate.side === 'SELL' && newQty > asset) newQty = asset; // capa na carteira (fees/saldo)
> 246	    }
> 247	    else if (orderTemplate.quantity === 'HARVEST_QTY') {
> 248	        // Bucket TÁTICO do Harvester de dislocação (escrito no fill por app-em.updateHarvestPosition):
> 249	        // MEMORY['<sym>:HARVEST'] = { qty, cost }. A venda no-loss vende ESTA qty (só o que o harvester
> 250	        // comprou), NUNCA o cofre principal de BTC. Falha-fechado se vazio (sem bucket, não vende).
> 251	        const harvest = MEMORY[`${orderTemplate.symbol}:HARVEST`];
> 252	        const harvestQty = harvest ? parseFloat(harvest.qty) : NaN;
> 253	        if (!harvestQty || harvestQty <= 0)
> 254	            throw new Error(`There is no harvest position (HARVEST) to use as qty reference for ${orderTemplate.symbol}.`);
> 255	
> 256	        newQty = harvestQty * multiplier;
> 257	        if (orderTemplate.side === 'SELL' && newQty > asset) newQty = asset; // capa na carteira (fees/saldo)
> 258	    }
> 259	    else if (orderTemplate.quantity === 'FARM_QTY') {
> 260	        // Bucket DCA do Farm de alts (escrito no fill por app-em.updateFarmPosition):
> 261	        // MEMORY['<sym>:FARM_DCA'] = { qty, cost }. A venda no-loss vende SÓ o que o Farm comprou,
> 262	        // NÃO a carteira inteira do ativo — MAX_WALLET vendia tudo e DUMPAVA junto a posição do Trend
> 263	        // Following co-localizada na mesma carteira (mesmo ativo). Falha-fechado se vazio (sem bucket, não vende).
> 264	        const farm = MEMORY[`${orderTemplate.symbol}:FARM_DCA`];
> 265	        const farmQty = farm ? parseFloat(farm.qty) : NaN;
> 266	        if (!farmQty || farmQty <= 0)
> 267	            throw new Error(`There is no farm position (FARM_DCA) to use as qty reference for ${orderTemplate.symbol}.`);
> 268	
> 269	        newQty = farmQty * multiplier;
> 270	        if (orderTemplate.side === 'SELL' && newQty > asset) newQty = asset; // capa na carteira (fees/saldo)
> 271	    }
> 272	    else if (orderTemplate.quantity === 'BTC_EXCESS') {
> 273	        // Vende o excedente de BTC acima de 1.0 BTC (o cofre).
> 274	        const btcAsset = parseFloat(MEMORY[`${symbol.base}:WALLET`]);
> 275	        if (!btcAsset || btcAsset <= 1.0)
> 276	            throw new Error(`There is no excess BTC (above 1.0 BTC) to sell. Balance: ${btcAsset}`);
> 277	        newQty = (btcAsset - 1.0) * multiplier;
> 278	        if (orderTemplate.side === 'SELL' && newQty > btcAsset) newQty = btcAsset;
> 279	    }
> 280	
> 281	    factor = Math.floor(newQty / stepSize);
> 282	    return (factor * stepSize).toFixed(symbol.basePrecision);
> 283	}
> 284	
> 285	function hasEnoughAssets(symbol, order, price) {
> 286	    const qty = parseFloat(order.quantity);
> 287	    if (order.side === 'BUY')
> 288	        return parseFloat(MEMORY[`${symbol.quote}:WALLET`]) >= (price * qty);
> 289	    else
> 290	        return parseFloat(MEMORY[`${symbol.base}:WALLET`]) >= qty;
> 291	}
> 292	
> 293	function calcQuoteQty(orderTemplate, symbol) {
> 294	    if (orderTemplate.type !== 'MARKET' || parseFloat(orderTemplate.quantity))
> 295	        throw new Error(`Only MARKET orders can cal quote qty.`);
> 296	
> 297	    const multiplier = orderTemplate.quantityMultiplier;
> 298	
> 299	    if (orderTemplate.quantity === 'MAX_WALLET') {
> 300	        if (orderTemplate.side !== 'BUY') throw new Error(`Only MARKET BUY orders can calc quote qty with MAX_WALLET`);
> 301	
> 302	        const asset = MEMORY[`${symbol.quote}:WALLET`];
> 303	        if (!asset) throw new Error(`There is no ${symbol.quote} in your wallet to place a buy.`);
> 304	
> 305	        return (parseFloat(asset) * (multiplier > 1 ? 1 : multiplier)).toFixed(symbol.quotePrecision);
> 306	    }
> 307	    else if (orderTemplate.quantity === 'MIN_NOTIONAL') {
> 308	        return (parseFloat(symbol.minNotional) * (multiplier < 1 ? 1 : multiplier)).toFixed(symbol.quotePrecision);
> 309	    }
> 310	
> 311	    throw new Error(`Invalid order template quantity ${orderTemplate.quantity}`);
> 312	}
> 313	
> 314	// OCO protetiva (One-Cancels-the-Other): TP via LIMIT_MAKER (perna "above") + SL via
> 315	// STOP_LOSS_LIMIT (perna "below"). Quando uma perna executa, a Binance cancela a outra.
> 316	// As 2 pernas são persistidas com o MESMO orderListId. Usa o endpoint novo
> 317	// v3/orderList/oco (ver utils/exchange.oco). v1: só SELL protetivo (TP acima, SL abaixo).
> 318	async function placeOco(settings, automation, orderTemplate, symbol) {
> 319	    const side = orderTemplate.side.toUpperCase();
> 320	    if (side !== 'SELL')
> 321	        throw new Error(`OCO no momento só suporta SELL protetivo (TP+SL). Side recebido: ${side}`);
> 322	
> 323	    // Anti-empilhamento: a proteção é "uma OCO por vez". Se já há uma OCO aberta desta
> 324	    // automação para o símbolo, não coloca outra — a automação re-arma sozinha quando a
> 325	    // anterior resolver (TP/SL) ou for cancelada. Sem isso, uma automação sem índice (que
> 326	    // dispara a cada tick) ou condições oscilando empilhariam OCOs e drenariam o saldo.
> 327	    if (automation.id) {
> 328	        const symbolUpper = orderTemplate.symbol.toUpperCase();
> 329	        const open = await getOpenOcoOrders(automation.id);
> 330	        if (open && open.some(o => o.symbol === symbolUpper)) {
> 331	            if (automation.logs) logger('A:' + automation.id, `OCO já aberta para ${symbolUpper}; re-disparo ignorado.`);
> 332	            return { type: 'success', text: `OCO already open for ${symbolUpper}, skipped.` };
> 333	        }
> 334	    }
> 335	
> 336	    // TP (perna LIMIT_MAKER, acima) = limitPrice × limitPriceMultiplier.
> 337	    const tpPrice = calcPrice(orderTemplate, symbol, false);
> 338	    if (!isFinite(tpPrice) || !parseFloat(tpPrice))
> 339	        throw new Error(`Erro no preço de TP da OCO, OTID ${orderTemplate.id}: ${tpPrice}`);
> 340	
> 341	    // Gatilho do stop (belowStopPrice) = stopPrice × stopPriceMultiplier.
> 342	    const stopTrigger = calcPrice(orderTemplate, symbol, true);
> 343	    if (!isFinite(stopTrigger) || !parseFloat(stopTrigger))
> 344	        throw new Error(`Erro no preço de stop da OCO, OTID ${orderTemplate.id}: ${stopTrigger}`);
> 345	
> 346	    // Preço-limite da perna de stop (belowPrice) = gatilho: para um SELL fica marketável
> 347	    // (limite <= gatilho), garantindo a execução quando o stop dispara.
> 348	    const stopLimit = stopTrigger;
> 349	
> 350	    const quantity = calcQty(orderTemplate, tpPrice, symbol);
> 351	    if (!isFinite(quantity) || !parseFloat(quantity))
> 352	        throw new Error(`Erro na quantidade da OCO, OTID ${orderTemplate.id}: ${quantity}`);
> 353	
> 354	    const order = { symbol: orderTemplate.symbol.toUpperCase(), side, quantity };
> 355	    if (!hasEnoughAssets(symbol, order, tpPrice))
> 356	        throw new Error(`Sem saldo suficiente para a OCO ${side} ${quantity} ${order.symbol}.`);
> 357	
> 358	    const options = {
> 359	        aboveType: 'LIMIT_MAKER',
> 360	        abovePrice: tpPrice,
> 361	        belowType: 'STOP_LOSS_LIMIT',
> 362	        belowPrice: stopLimit,
> 363	        belowStopPrice: stopTrigger,
> 364	        belowTimeInForce: 'GTC'
> 365	    };
> 366	
> 367	    let result;
> 368	    const exchange = require('./utils/exchange')(settings);
> 369	    try {
> 370	        result = await exchange.oco(side, order.symbol, quantity, options);
> 371	    } catch (err) {
> 372	        logger('A:' + automation.id, err.body ? err.body : err);
> 373	        logger('A:' + automation.id, { order, options });
> 374	        return { type: 'error', text: `OCO failed! ` + (err.body ? JSON.stringify(err.body) : err.message) };
> 375	    }
> 376	
> 377	    const orderListId = result.orderListId;
> 378	    const reports = Array.isArray(result.orderReports) ? result.orderReports : [];
> 379	
> 380	    // A OCO já está VIVA na corretora. Se a resposta vier anômala (≠2 pernas), cancela a
> 381	    // lista para não deixar ordem órfã não-rastreável e falha.
> 382	    if (reports.length !== 2) {
> 383	        try { if (orderListId) await exchange.cancelOrderList(order.symbol, orderListId); }
> 384	        catch (e) { logger('A:' + automation.id, e.body ? e.body : e); }
> 385	        return { type: 'error', text: `OCO retornou ${reports.length} pernas (esperado 2); lista #${orderListId} cancelada.` };
> 386	    }
> 387	
> 388	    // Persiste AMBAS as pernas com o mesmo orderListId (consistente com placeOrder). Se a
> 389	    // persistência falhar, a OCO ficaria viva mas órfã (fora do getOpenOcoOrders e do hook
> 390	    // de cancelamento) → cancela na corretora e falha, mantendo DB e exchange coerentes.
> 391	    try {
> 392	        for (const r of reports) {
> 393	            const savedLeg = await insertOrder({
> 394	                automationId: automation.id,
> 395	                symbol: order.symbol,
> 396	                quantity: r.origQty || quantity,
> 397	                type: r.type,
> 398	                side: r.side || side,
> 399	                orderListId,
> 400	                limitPrice: r.price && parseFloat(r.price) ? `${r.price}` : null,
> 401	                stopPrice: r.stopPrice && parseFloat(r.stopPrice) ? `${r.stopPrice}` : null,
> 402	                icebergQty: null,
> 403	                orderId: r.orderId,
> 404	                clientOrderId: r.clientOrderId,
> 405	                transactTime: r.transactTime || result.transactionTime || Date.now(),
> 406	                status: r.status || 'NEW'
> 407	            });
> 408	            telegramNotify.notifyOrder(savedLeg.get({ plain: true })); // uma notificação por perna da OCO
> 409	        }
> 410	    } catch (err) {
> 411	        logger('A:' + automation.id, err);
> 412	        try { if (orderListId) await exchange.cancelOrderList(order.symbol, orderListId); }
> 413	        catch (e) { logger('A:' + automation.id, e.body ? e.body : e); }
> 414	        return { type: 'error', text: `Falha ao persistir a OCO #${orderListId}; lista cancelada na corretora.` };
> 415	    }
> 416	
> 417	    if (automation.logs)
> 418	        logger('A:' + automation.id, `OCO #${orderListId} ${side} ${order.symbol}: TP ${tpPrice} / STOP ${stopTrigger}->${stopLimit}, qty ${quantity}`);
> 419	
> 420	    return { type: 'success', text: `OCO ${side} ${order.symbol} placed (list #${orderListId})` };
> 421	}
> 422	
> 423	async function placeOrder(settings, automation, action) {
> 424	
> 425	    if (!settings || !automation || !action)
> 426	        throw new Error(`All parameters are required to place an order.`);
> 427	
> 428	    if (!action.orderTemplateId)
> 429	        throw new Error(`There is no order template for '${automation.name}', action #${action.id}`);
> 430	
> 431	    const orderTemplate = action.orderTemplate ? { ...action.orderTemplate } : await orderTemplatesRepository.getOrderTemplate(action.orderTemplateId);
> 432	    if (orderTemplate.type === 'TRAILING_STOP') {
> 433	        orderTemplate.type = 'MARKET';
> 434	        orderTemplate.limitPrice = null;
> 435	        orderTemplate.stopPrice = null;
> 436	    }
> 437	
> 438	    const symbol = await getSymbol(orderTemplate.symbol);
> 439	
> 440	    // OCO tem fluxo próprio (2 pernas + orderListId): desvia antes de montar a ordem simples.
> 441	    if (orderTemplate.type.toUpperCase() === 'OCO')
> 442	        return placeOco(settings, automation, orderTemplate, symbol);
> 443	
> 444	    const order = {
> 445	        symbol: orderTemplate.symbol.toUpperCase(),
> 446	        side: orderTemplate.side.toUpperCase(),
> 447	        options: {
> 448	            type: orderTemplate.type.toUpperCase()
> 449	        }
> 450	    }
> 451	
> 452	    const isDynamicBuy = order.side === 'BUY' && ['MIN_NOTIONAL', 'MAX_WALLET'].includes(orderTemplate.quantity);
> 453	    if (order.options.type === 'MARKET'
> 454	        && (isDynamicBuy || orderTemplate.quantity === 'MIN_NOTIONAL')) {
> 455	        order.options.quoteOrderQty = calcQuoteQty(orderTemplate, symbol);
> 456	    } else {
> 457	        const price = calcPrice(orderTemplate, symbol, false);
> 458	
> 459	        if (!isFinite(price) || !price)
> 460	            throw new Error(`Error in calcPrice function, params: OTID ${orderTemplate.id}, $: ${price}, stop: false`);
> 461	
> 462	        if (LIMIT_TYPES.includes(order.options.type))
> 463	            order.limitPrice = price;
> 464	
> 465	        const quantity = calcQty(orderTemplate, price, symbol, false);
> 466	
> 467	        if (!isFinite(quantity) || !quantity)
> 468	            throw new Error(`Error in calcQty function, params: OTID ${orderTemplate.id}, $: ${price}, qty: ${quantity}`);
> 469	
> 470	        order.quantity = quantity;
> 471	
> 472	        if (STOP_TYPES.includes(order.options.type)) {
> 473	            const stopPrice = calcPrice(orderTemplate, symbol, true);
> 474	
> 475	            if (!isFinite(stopPrice) || !stopPrice)
> 476	                throw new Error(`Error in calcPrice function, params: OTID ${orderTemplate.id}, $: ${stopPrice}, stop: true`);
> 477	
> 478	            order.options.stopPrice = stopPrice;
> 479	        }
> 480	
> 481	        if (!hasEnoughAssets(symbol, order, price))
> 482	            throw new Error(`You wanna ${order.side} ${order.quantity} ${order.symbol} but you haven't enough assets.`);
> 483	    }
> 484	
> 485	    let result;
> 486	    const exchange = require('./utils/exchange')(settings);
> 487	
> 488	    try {
> 489	        if (order.side === 'BUY')
> 490	            result = await exchange.buy(order.symbol, order.quantity, order.limitPrice, order.options);
> 491	        else
> 492	            result = await exchange.sell(order.symbol, order.quantity, order.limitPrice, order.options);
> 493	    }
> 494	    catch (err) {
> 495	        logger('A:' + automation.id, err.body ? err.body : err);
> 496	        logger('A:' + automation.id, order);
> 497	        return { type: 'error', text: `Order failed! ` + err.body ? err.body : err.message };
> 498	    }
> 499	
> 500	    // Trava de venda do Harvester: marca HARVEST_SELLING ASSIM QUE a ordem é ACEITA pela corretora (logo após
> 501	    // exchange.sell, ANTES do insertOrder) — se o insertOrder/calcFillFinancials der throw depois, a venda já
> 502	    // está na corretora e a trava JÁ está posta → falha fail-closed (silencia a venda) em vez de re-disparar
> 503	    // uma 2ª venda do MESMO bucket no próximo tick (oversell vazaria o reserve: calcQty capa na carteira, não no
> 504	    // bucket). A venda no-loss é LEVEL-trigger (ver shouldntInvert); a trava é o anti-empilhamento. Liberada no
> 505	    // estado terminal (app-em.updateHarvestPosition). Detecta pela qty='HARVEST_QTY' (assinatura única da venda).
> 506	    if (order.side === 'SELL' && orderTemplate.quantity === 'HARVEST_QTY')
> 507	        await updateMemory(order.symbol, 'HARVEST_SELLING', null, { orderId: result.orderId, at: Date.now() }, false);
> 508	
> 509	    let stopPrice;
> 510	    if (action.orderTemplate && action.orderTemplate.type === 'TRAILING_STOP')
> 511	        stopPrice = action.orderTemplate.stopPrice;
> 512	    else if (STOP_TYPES.includes(order.type))
> 513	        stopPrice = order.options.stopPrice;
> 514	
> 515	    const savedOrder = await insertOrder({
> 516	        automationId: automation.id,
> 517	        symbol: order.symbol,
> 518	        quantity: order.quantity || result.executedQty,
> 519	        type: order.options.type,
> 520	        side: order.side,
> 521	        limitPrice: LIMIT_TYPES.includes(order.options.type) ? order.limitPrice : null,
> 522	        stopPrice,
> 523	        icebergQty: null,
> 524	        orderId: result.orderId,
> 525	        clientOrderId: result.clientOrderId,
> 526	        transactTime: result.transactTime,
> 527	        status: result.status || 'NEW',
> 528	        // net/avgPrice/commission no insert quando já executou (MARKET) — não depende do stream
> 529	        ...calcFillFinancials(result, order.symbol)
> 530	    })
> 531	
> 532	    // Telegram pro dono (pedido: notificar todas as novas ordens). Best-effort, não-lançante;
> 533	    // dedup por orderId+status (a MARKET já-FILLED não re-notifica no executionReport do stream).
> 534	    telegramNotify.notifyOrder(savedOrder.get({ plain: true }));
> 535	
> 536	    if (automation.logs) logger('A:' + automation.id, savedOrder.get({ plain: true }));
> 537	
> 538	    return { type: 'success', text: `Order ${order.side} ${order.symbol} ${result.status}` };
> 539	}
> 540	
> 541	async function gridEval(settings, automation) {
> 542	    automation.grids = automation.grids.sort((a, b) => a.id - b.id);
> 543	
> 544	    if (LOGS)
> 545	        logger('A:' + automation.id, `Beholder is in the GRID zone at ${automation.name}`);
> 546	
> 547	    for (let i = 0; i < automation.grids.length; i++) {
> 548	        const grid = automation.grids[i];
> 549	        if (!Function("MEMORY", "return " + grid.conditions)(MEMORY)) continue;
> 550	
> 551	        if (automation.logs)
> 552	            logger('A:' + automation.id, `Beholder evaluated a condition at ${automation.name} => ${grid.conditions}`);
> 553	
> 554	        automation.actions[0].orderTemplateId = grid.orderTemplateId;
> 555	
> 556	        const book = MEMORY[`${automation.symbol}:BOOK`];
> 557	        if (!book) return { type: 'error', text: `No book info for ${automation.symbol}` };
> 558	
> 559	        const result = await placeOrder(settings, automation, automation.actions[0]);
> 560	        if (automation.logs) await require('./utils/telegram')(settings, result.text);
> 561	        if (result.type === 'error') return result;
> 562	
> 563	        const transaction = await db.transaction();
> 564	        try {
> 565	            const orderTemplate = await orderTemplatesRepository.getOrderTemplate(grid.orderTemplateId);
> 566	            await generateGrids(automation, automation.grids.length + 1, orderTemplate.quantity, transaction);
> 567	            await transaction.commit();
> 568	        } catch (err) {
> 569	            await transaction.rollback();
> 570	            logger('A:' + automation.id, err);
> 571	            return { type: 'error', text: `Beholder can't generate grids for ${automation.name}. ERR: ${err.message}` };
> 572	        }
> 573	
> 574	        automation = await automationsRepository.getAutomation(automation.id);//pega limpo
> 575	        updateBrain(automation);
> 576	        return result;
> 577	    }
> 578	}
> 579	
> 580	async function generateGrids(automation, levels, quantity, transaction) {
> 581	
> 582	    await gridsRepository.deleteGrids(automation.id, transaction);
> 583	
> 584	    const symbol = await getSymbol(automation.symbol);
> 585	    if (!symbol.tickSize) throw new Error(`Tick Size not found for this symbol`);
> 586	
> 587	    const tickSize = parseFloat(symbol.tickSize);
> 588	
> 589	    const conditionSplit = automation.conditions.split(' && ');
> 590	    const lowerLimit = parseFloat(conditionSplit[0].split('>')[1]);
> 591	    const upperLimit = parseFloat(conditionSplit[1].split('<')[1]);
> 592	    levels = parseInt(levels);
> 593	
> 594	    const priceLevel = (upperLimit - lowerLimit) / levels;
> 595	    const grids = [];
> 596	
> 597	    let buyOrderTemplate, sellOrderTemplate;
> 598	    const orderTemplates = await orderTemplatesRepository.getOrderTemplatesByGridName(automation.name);
> 599	
> 600	    if (orderTemplates && orderTemplates.length) {
> 601	        buyOrderTemplate = orderTemplates.find(ot => ot.side === 'BUY');
> 602	        if (buyOrderTemplate && buyOrderTemplate.quantity !== quantity) {
> 603	            buyOrderTemplate.quantity = quantity;
> 604	            await orderTemplatesRepository.updateOrderTemplate(buyOrderTemplate.id, buyOrderTemplate);
> 605	        }
> 606	
> 607	        sellOrderTemplate = orderTemplates.find(ot => ot.side === 'SELL');
> 608	        if (sellOrderTemplate && sellOrderTemplate.quantity !== quantity) {
> 609	            sellOrderTemplate.quantity = quantity;
> 610	            await orderTemplatesRepository.updateOrderTemplate(sellOrderTemplate.id, sellOrderTemplate);
> 611	        }
> 612	    }
> 613	
> 614	    if (!buyOrderTemplate)
> 615	        buyOrderTemplate = await orderTemplatesRepository.insertOrderTemplate({
> 616	            name: automation.name + ' BUY',
> 617	            symbol: automation.symbol,
> 618	            type: 'MARKET',
> 619	            side: 'BUY',
> 620	            limitPrice: null,
> 621	            limitPriceMultiplier: 1,
> 622	            stopPrice: null,
> 623	            stopPriceMultiplier: 1,
> 624	            quantity,
> 625	            quantityMultiplier: 1,
> 626	            icebergQty: null,
> 627	            icebergQtyMultiplier: 1
> 628	        }, transaction)
> 629	
> 630	    if (!sellOrderTemplate)
> 631	        sellOrderTemplate = await orderTemplatesRepository.insertOrderTemplate({
> 632	            name: automation.name + ' SELL',
> 633	            symbol: automation.symbol,
> 634	            type: 'MARKET',
> 635	            side: 'SELL',
> 636	            limitPrice: null,
> 637	            limitPriceMultiplier: 1,
> 638	            stopPrice: null,
> 639	            stopPriceMultiplier: 1,
> 640	            quantity,
> 641	            quantityMultiplier: 1,
> 642	            icebergQty: null,
> 643	            icebergQtyMultiplier: 1
> 644	        }, transaction)
> 645	
> 646	    const book = MEMORY[`${automation.symbol}:BOOK`];
> 647	    if (!book) throw new Error(`There is no book info for ${automation.symbol}`);
> 648	
> 649	    const currentPrice = parseFloat(book.current.bestAsk);
> 650	    const differences = [];
> 651	
> 652	    for (let i = 1; i <= levels; i++) {
> 653	        const priceFactor = Math.floor((lowerLimit + (priceLevel * i)) / tickSize);
> 654	        const targetPrice = priceFactor * tickSize;
> 655	        const targetPriceStr = targetPrice.toFixed(symbol.quotePrecision);
> 656	        differences.push(Math.abs(currentPrice - targetPrice));
> 657	
> 658	        if (targetPrice < currentPrice) { //se está abaixo da cotação, compra
> 659	            const previousLevel = targetPrice - priceLevel;
> 660	            const previousLevelStr = previousLevel.toFixed(symbol.quotePrecision);
> 661	            grids.push({
> 662	                automationId: automation.id,
> 663	                conditions: `MEMORY['${automation.symbol}:BOOK'].current.bestAsk<${targetPriceStr} && MEMORY['${automation.symbol}:BOOK'].previous.bestAsk>=${targetPriceStr} && MEMORY['${automation.symbol}:BOOK'].current.bestAsk>${previousLevelStr}`,
> 664	                orderTemplateId: buyOrderTemplate.id
> 665	            })
> 666	        }
> 667	        else {//se está acima da cotação, vende
> 668	            const nextLevel = targetPrice + priceLevel;
> 669	            const nextLevelStr = nextLevel.toFixed(symbol.quotePrecision);
> 670	            grids.push({
> 671	                automationId: automation.id,
> 672	                conditions: `MEMORY['${automation.symbol}:BOOK'].current.bestBid>${targetPriceStr} && MEMORY['${automation.symbol}:BOOK'].previous.bestBid<=${targetPriceStr} && MEMORY['${automation.symbol}:BOOK'].current.bestBid<${nextLevelStr}`,
> 673	                orderTemplateId: sellOrderTemplate.id
> 674	            })
> 675	        }
> 676	    }
> 677	
> 678	    const nearestGrid = differences.findIndex(d => d === Math.min(...differences));
> 679	    grids.splice(nearestGrid, 1);
> 680	
> 681	    return gridsRepository.insertGrids(grids, transaction);
> 682	}
> 683	
> 684	async function withdrawCrypto(settings, automation, action) {
> 685	    if (!settings || !automation || !action)
> 686	        throw new Error(`All parameters are required to place an order.`);
> 687	
> 688	    if (!action.withdrawTemplateId)
> 689	        throw new Error(`There is no withdraw template for '${automation.name}', action #${action.id}`);
> 690	
> 691	    const withdrawTemplate = await withdrawTemplatesRepository.getWithdrawTemplate(action.withdrawTemplateId);
> 692	
> 693	    let amount = parseFloat(withdrawTemplate.amount);
> 694	    if (!amount) {
> 695	        if (withdrawTemplate.amount === 'MAX_WALLET') {
> 696	            const available = MEMORY[`${withdrawTemplate.coin}:WALLET`];
> 697	            if (!available) throw new Error(`No available funds for this coin.`);
> 698	
> 699	            amount = available * (withdrawTemplate.amountMultiplier > 1 ? 1 : withdrawTemplate.amountMultiplier);
> 700	        }
> 701	        else if (withdrawTemplate.amount === 'LAST_ORDER_QTY') {
> 702	            const keys = searchMemory(new RegExp(`^((${withdrawTemplate.coin}.+|.+${withdrawTemplate.coin}):LAST_ORDER)$`));
> 703	            if (!keys || !keys.length) throw new Error(`No last order for this coin.`);
> 704	
> 705	            amount = keys[keys.length - 1].value.quantity * withdrawTemplate.amountMultiplier;
> 706	        }
> 707	    }
> 708	
> 709	    const exchange = require('./utils/exchange')(settings);
> 710	
> 711	    try {
> 712	        const result = await exchange.withdraw(withdrawTemplate.coin, amount, withdrawTemplate.address, withdrawTemplate.network, withdrawTemplate.addressTag);
> 713	
> 714	        if (automation.logs) logger('A:' + automation.id, `WITHDRAW`, withdrawTemplate);
> 715	
> 716	        return { type: 'success', text: `Withdraw #${result.id} realized successfully for ${withdrawTemplate.coin}` };
> 717	    } catch (err) {
> 718	        throw new Error(err.response ? JSON.stringify(err.response.data) : err.message);
> 719	    }
> 720	}
> 721	
> 722	async function sendTelegram(settings, automation) {
> 723	    await require('./utils/telegram')(settings, automation.name + ' has fired!');
> 724	    if (automation.logs) logger('A:' + automation.id, `Telegram sent!`);
> 725	    return { text: `Telegram sent from automation '${automation.name}'`, type: 'success' };
> 726	}
> 727	
> 728	async function trailingEval(settings, automation, action) {
> 729	    const isBuy = action.orderTemplate.side === 'BUY';
> 730	
> 731	    const book = MEMORY[`${automation.symbol}:BOOK`];
> 732	    if (!book) return { type: 'error', text: `No book info for ${automation.name}` };
> 733	
> 734	    const activationPrice = parseFloat(action.orderTemplate.limitPrice);
> 735	    const stopPrice = parseFloat(action.orderTemplate.stopPrice);
> 736	
> 737	    const currentPrice = isBuy ? book.current.bestAsk : book.current.bestBid;
> 738	    const previousPrice = isBuy ? book.previous.bestAsk : book.previous.bestBid;
> 739	
> 740	    const isPriceActivated = isBuy ? currentPrice <= activationPrice : currentPrice >= activationPrice;
> 741	
> 742	    if (!isPriceActivated) return false;
> 743	
> 744	    if (LOGS)
> 745	        logger('A:' + automation.id, `Beholder is in the Trailing zone at ${automation.name}`);
> 746	
> 747	    const isStopActivated = isBuy ? currentPrice >= stopPrice && previousPrice < stopPrice
> 748	        : currentPrice <= stopPrice && previousPrice > stopPrice;
> 749	
> 750	    if (isStopActivated) {
> 751	        if (automation.logs || LOGS)
> 752	            logger('A:' + automation.id, `Stop price activated at ${automation.name}`);
> 753	
> 754	        const results = await placeOrder(settings, automation, action);
> 755	
> 756	        //para executar apenas uma vez
> 757	        deleteBrain(automation);
> 758	
> 759	        automation.isActive = false;
> 760	        await automationsRepository.updateAutomation(automation.id, automation);
> 761	
> 762	        return results;
> 763	    }
> 764	
> 765	    const newStopPrice = isBuy ? currentPrice * (1 + (parseFloat(action.orderTemplate.stopPriceMultiplier) / 100))
> 766	        : currentPrice * (1 - (parseFloat(action.orderTemplate.stopPriceMultiplier) / 100));
> 767	
> 768	    if (!stopPrice || (isBuy && newStopPrice < stopPrice) || (!isBuy && newStopPrice > stopPrice)) {
> 769	        if (LOGS)
> 770	            logger('A:' + automation.id, `Stop price changed to ${newStopPrice} at ${automation.name}`);
> 771	
> 772	        action.orderTemplate.stopPrice = newStopPrice;
> 773	        await orderTemplatesRepository.updateOrderTemplate(action.orderTemplate.id, action.orderTemplate);
> 774	    }
> 775	}
> 776	
> 777	function doAction(settings, action, automation) {
> 778	
> 779	    try {
> 780	        switch (action.type) {
> 781	            case actionTypes.ALERT_EMAIL: return sendEmail(settings, automation);
> 782	            case actionTypes.ALERT_SMS: return sendSms(settings, automation);
> 783	            case actionTypes.ALERT_TELEGRAM: return sendTelegram(settings, automation);
> 784	            case actionTypes.ORDER: return placeOrder(settings, automation, action);
> 785	            case actionTypes.TRAILING: return trailingEval(settings, automation, action);
> 786	            case actionTypes.WITHDRAW: return withdrawCrypto(settings, automation, action);
> 787	            case actionTypes.GRID: return gridEval(settings, automation);
> 788	        }
> 789	    } catch (err) {
> 790	        if (automation.logs) {
> 791	            logger('A:' + automation.id, `${automation.name}:${action.type}`);
> 792	            logger('A:' + automation.id, err);
> 793	        }
> 794	        return { text: `Error at ${automation.name}: ${err.message}`, type: 'error' };
> 795	    }
> 796	}
> 797	
> 798	function shouldntInvert(automation, memoryKey) {
> 799	    //return true;//descomente para desabilitar 'double check' (teste de condição invertida)
> 800	    return ['GRID', 'TRAILING'].includes(automation.actions[0].type)
> 801	        || automation.schedule
> 802	        // Venda no-loss do Harvester: LEVEL-trigger (dispara enquanto bestBid>alvo), NÃO edge. O 'double check'
> 803	        // invertido re-adicionaria um previous.bestBid<alvo que perde o revert rápido (o bucket nasce 3s após o
> 804	        // fill, já acima do alvo → nunca há cruzamento fresco). O anti-empilhamento vira a trava HARVEST_SELLING
> 805	        // (setada no place, liberada no estado terminal) → 1 venda por bucket, sem oversell.
> 806	        || (automation.conditions && automation.conditions.indexOf('HARVEST_SELLING') !== -1)
> 807	        || memoryKey.indexOf(':LAST_ORDER') !== -1
> 808	        || memoryKey.indexOf(':LAST_CANDLE') !== -1
> 809	        || memoryKey.indexOf(':PREVIOUS_CANDLE') !== -1;
> 810	}
> 811	
> 812	async function evalDecision(memoryKey, automation) {
> 813	    if (!automation) return false;
> 814	
> 815	    try {
> 816	        const indexes = automation.indexes ? automation.indexes.split(',') : [];
> 817	
> 818	        if (indexes.length) {
> 819	            const isChecked = indexes.every(ix => MEMORY[ix] !== null && MEMORY[ix] !== undefined);
> 820	            if (!isChecked) return false;
> 821	
> 822	            const invertedCondition = shouldntInvert(automation, memoryKey) ? '' : invertCondition(memoryKey, automation.conditions);
> 823	            const evalCondition = automation.conditions + (invertedCondition ? ' && ' + invertedCondition : '');
> 824	
> 825	            if (LOGS) logger('A:' + automation.id, `Beholder trying to evaluate:\n${evalCondition}\n at ${automation.name}`);
> 826	
> 827	            const isValid = evalCondition ? Function("MEMORY", "return " + evalCondition)(MEMORY) : true;
> 828	            if (!isValid) return false;
> 829	        }
> 830	
> 831	        if (!automation.actions || !automation.actions.length) {
> 832	            if (LOGS || automation.logs) logger('A:' + automation.id, `No actions defined for automation ${automation.name}`);
> 833	            return false;
> 834	        }
> 835	
> 836	        if ((LOGS || automation.logs) && !['GRID', 'TRAILING'].includes(automation.actions[0].type))
> 837	            logger('A:' + automation.id, `Beholder evaluated a condition at automation: ${automation.name} => ${automation.conditions}`);
> 838	
> 839	        const settings = await getDefaultSettings();
> 840	        const results = [];
> 841	
> 842	        for (let i = 0; i < automation.actions.length; i++) {
> 843	            const action = automation.actions[i];
> 844	            const result = await doAction(settings, action, automation);
> 845	            if (!result || result.type === 'error') break;
> 846	
> 847	            results.push(result);
> 848	        }
> 849	
> 850	        if (automation.logs && results && results.length && results[0])
> 851	            logger('A:' + automation.id, `Automation ${automation.name} finished execution at ${new Date()}\nResults: ${JSON.stringify(results)}`);
> 852	
> 853	        return results.flat();
> 854	    } catch (err) {
> 855	        if (automation.logs) logger('A:' + automation.id, err);
> 856	        return { type: 'error', text: `Error at evalDecision for '${automation.name}': ${err}` };
> 857	    }
> 858	}
> 859	
> 860	async function testAutomations(memoryKey) {
> 861	
> 862	    const automations = findAutomations(memoryKey);
> 863	
> 864	    if (!automations || !automations.length || isLocked(automations.filter(a => a).map(a => a.id))) {
> 865	        if (LOGS) console.log(`Beholder has no automations for memoryKey: ${memoryKey} or the brain is locked!`);
> 866	        return false;
> 867	    }
> 868	
> 869	    setLocked(automations.map(a => a.id), true);
> 870	    let results;
> 871	
> 872	    try {
> 873	        const promises = automations.map(async (automation) => {
> 874	            let auto = { ...automation };
> 875	
> 876	            if (auto.symbol.startsWith('*')) {
> 877	                const symbol = memoryKey.split(':')[0];
> 878	                auto.indexes = auto.indexes.replaceAll(auto.symbol, symbol);
> 879	                auto.conditions = auto.conditions.replaceAll(auto.symbol, symbol);
> 880	                if (auto.actions) {
> 881	                    auto.actions.forEach(action => {
> 882	                        if (action.orderTemplate)
> 883	                            action.orderTemplate.symbol = symbol;
> 884	                    })
> 885	                }
> 886	                auto.symbol = symbol;
> 887	            }
> 888	
> 889	            return evalDecision(memoryKey, auto);
> 890	        });
> 891	
> 892	        results = await Promise.all(promises);
> 893	        if (Array.isArray(results) && results.length)
> 894	            results = results.flat().filter(r => r);
> 895	
> 896	        if (!results || (Array.isArray(results) && !results.length))
> 897	            return false;
> 898	        else
> 899	            return results;
> 900	    }
> 901	    finally {
> 902	        setTimeout(() => {
> 903	            setLocked(automations.map(a => a.id), false);
> 904	        }, results && results.length ? INTERVAL : 0)
> 905	    }
> 906	}
> 907	
> 908	function parseMemoryKey(symbol, index, interval = null) {
> 909	    const indexKey = interval ? `${index}_${interval}` : index;
> 910	    return `${symbol}:${indexKey}`;
> 911	}
> 912	
> 913	async function updateMemory(symbol, index, interval, value, executeAutomations = true) {
> 914	
> 915	    if (value === undefined || value === null) return false;
> 916	    if (value.toJSON) value = value.toJSON();
> 917	    if (value.get) value = value.get({ plain: true });
> 918	
> 919	    if (LOCK_MEMORY) return false;
> 920	
> 921	    const memoryKey = parseMemoryKey(symbol, index, interval);
> 922	    MEMORY[memoryKey] = value;
> 923	
> 924	    if (LOGS) logger('beholder', `Beholder memory updated: ${memoryKey} => ${JSON.stringify(value)}, will exec autos? ${executeAutomations}`);
> 925	
> 926	    if (!executeAutomations) return false;
> 927	
> 928	    return testAutomations(memoryKey);
> 929	}
> 930	
> 931	function deleteMemory(symbol, index, interval) {
> 932	    try {
> 933	        const indexKey = interval ? `${index}_${interval}` : index;
> 934	        const memoryKey = `${symbol}:${indexKey}`;
> 935	        if (MEMORY[memoryKey] === undefined) return;
> 936	
> 937	        LOCK_MEMORY = true;
> 938	        delete MEMORY[memoryKey];
> 939	
> 940	        if (LOGS) logger('beholder', `Beholder memory delete: ${memoryKey}!`);
> 941	    } finally {
> 942	        LOCK_MEMORY = false;
> 943	    }
> 944	}
> 945	
> 946	function getMemory(symbol, index, interval) {
> 947	    if (symbol && index) {
> 948	        const indexKey = interval ? `${index}_${interval}` : index;
> 949	        const memoryKey = `${symbol}:${indexKey}`;
> 950	
> 951	        const result = MEMORY[memoryKey];
> 952	        return typeof result === 'object' ? { ...result } : result;
> 953	    }
> 954	
> 955	    return { ...MEMORY };
> 956	}
> 957	
> 958	function getBrain() {
> 959	    return { ...BRAIN };
> 960	}
> 961	
> 962	function getBrainIndexes() {
> 963	    return { ...BRAIN_INDEX };
> 964	}
> 965	
> 966	function flattenObject(ob) {
> 967	    var toReturn = {};
> 968	
> 969	    for (var i in ob) {
> 970	        if (!ob.hasOwnProperty(i)) continue;
> 971	
> 972	        if ((typeof ob[i]) == 'object' && ob[i] !== null) {
> 973	            var flatObject = flattenObject(ob[i]);
> 974	            for (var x in flatObject) {
> 975	                if (!flatObject.hasOwnProperty(x)) continue;
> 976	
> 977	                toReturn[i + '.' + x] = flatObject[x];
> 978	            }
> 979	        } else {
> 980	            toReturn[i] = ob[i];
> 981	        }
> 982	    }
> 983	    return toReturn;
> 984	}
> 985	
> 986	function getEval(prop) {
> 987	    if (prop.indexOf('MEMORY') !== -1) return prop;
> 988	    if (prop.indexOf('.') === -1) return `MEMORY['${prop}']`;
> 989	
> 990	    const propSplit = prop.split('.');
> 991	    const memKey = propSplit[0];
> 992	    const memProp = prop.replace(memKey, '');
> 993	    return `MEMORY['${memKey}']${memProp}`;
> 994	}
> 995	
> 996	function getMemoryIndexes() {
> 997	    return Object.entries(flattenObject(MEMORY)).map(prop => {
> 998	        if (prop[0].indexOf('previous') !== -1 || prop[0].indexOf(':') === -1) return false;
> 999	        const propSplit = prop[0].split(':');
> 1000	        return {
> 1001	            symbol: propSplit[0],
> 1002	            variable: propSplit[1].replace('.current', ''),
> 1003	            eval: getEval(prop[0]),
> 1004	            example: prop[1]
> 1005	        }
> 1006	    })
> 1007	        .filter(ix => ix)
> 1008	        .sort((a, b) => {
> 1009	            if (a.variable < b.variable) return -1;
> 1010	            if (a.variable > b.variable) return 1;
> 1011	            return 0;
> 1012	        })
> 1013	}
> 1014	
> 1015	const DOLLAR_COINS = ['USD', 'USDT', 'USDC', 'BUSD'];
> 1016	
> 1017	function getStableConversion(baseAsset, quoteAsset, baseQty) {
> 1018	    if (DOLLAR_COINS.includes(baseAsset)) return baseQty;
> 1019	
> 1020	    const book = getMemory(baseAsset + quoteAsset, 'BOOK', null);
> 1021	    if (book) return parseFloat(baseQty) * book.current.bestBid;
> 1022	    return 0;
> 1023	}
> 1024	
> 1025	const FIAT_COINS = ['BRL', 'EUR', 'GBP'];
> 1026	
> 1027	function getFiatConversion(stableCoin, fiatCoin, fiatQty) {
> 1028	    const book = getMemory(stableCoin + fiatCoin, 'BOOK', null);
> 1029	    if (book) return parseFloat(fiatQty) / book.current.bestBid;
> 1030	    return 0;
> 1031	}
> 1032	
> 1033	function tryFiatConversion(baseAsset, baseQty, fiat) {
> 1034	    if (fiat) fiat = fiat.toUpperCase();
> 1035	    if (FIAT_COINS.includes(baseAsset) && baseAsset === fiat) return baseQty;
> 1036	
> 1037	    const usd = tryUSDConversion(baseAsset, baseQty);
> 1038	    if (fiat === 'USD' || !fiat) return usd;
> 1039	
> 1040	    let book = getMemory('USDT' + fiat, 'BOOK');
> 1041	    if (book) return usd * book.current.bestBid;
> 1042	
> 1043	    book = getMemory(fiat + 'USDT', 'BOOK');
> 1044	    if (book) return usd / book.current.bestBid;
> 1045	
> 1046	    return usd;
> 1047	}
> 1048	
> 1049	function tryUSDConversion(baseAsset, baseQty) {
> 1050	    if (DOLLAR_COINS.includes(baseAsset)) return baseQty;
> 1051	    if (FIAT_COINS.includes(baseAsset)) return getFiatConversion('USDT', baseAsset, baseQty);
> 1052	
> 1053	    for (let i = 0; i < DOLLAR_COINS.length; i++) {
> 1054	        const converted = getStableConversion(baseAsset, DOLLAR_COINS[i], baseQty);
> 1055	        if (converted > 0) return converted;
> 1056	    }
> 1057	
> 1058	    return 0;
> 1059	}
> 1060	
> 1061	function searchMemory(regex) {
> 1062	    return Object.entries(getMemory()).filter(prop => regex.test(prop[0])).map(prop => {
> 1063	        return {
> 1064	            key: prop[0], value: prop[1]
> 1065	        }
> 1066	    });
> 1067	}
> 1068	
> 1069	module.exports = {
> 1070	    updateMemory,
> 1071	    getMemory,
> 1072	    getBrain,
> 1073	    init,
> 1074	    deleteMemory,
> 1075	    getMemoryIndexes,
> 1076	    getBrainIndexes,
> 1077	    updateBrain,
> 1078	    deleteBrain,
> 1079	    findAutomations,
> 1080	    placeOrder,
> 1081	    placeOco,
> 1082	    tryFiatConversion,
> 1083	    generateGrids,
> 1084	    evalDecision,
> 1085	    searchMemory,
> 1086	    testAutomations,
> 1087	    parseMemoryKey
> 1088	}
> 1089	
> ```

## 🤖 Claude *(18:55:46)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/src/utils/indexes.js"
}
```

## 🤖 Claude *(18:55:47)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/src/utils/exchange.js"
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
> 8	
> 9	// === Teto de risco global (chokepoint único: TODA ordem real — automação, funil ou manual — passa por
> 10	// buy()/sell()/oco() aqui). Única trava de tamanho do BACKEND (o ALLOW_TRADING é só do agente LLM).
> 11	//   TRADING_HALT=true            → kill-switch: bloqueia QUALQUER ordem (parada de emergência) — cobre TUDO.
> 12	//   MAX_ORDER_NOTIONAL_USDT=<n>  → teto de notional por ordem em USDT (0 = desligado). Cobre o que tem
> 13	//                                  notional CALCULÁVEL: MARKET por quote (quoteOrderQty, ex.: funil) e
> 14	//                                  LIMIT/OCO (price×qty). ⚠️ MARKET por QUANTIDADE-base sem price (ex.: venda
> 15	//                                  MARKET de TREND_QTY/HARVEST_QTY/MAX_WALLET) PASSA sem avaliar o teto —
> 16	//                                  coberta só pelo HALT. FOLLOW-UP: derivar preço do MINI_TICKER antes de
> 17	//                                  subir size. Só pares *USDT (notional em USDT); quote ≠ USDT passa.
> 18	// Inerte por padrão; ajustável por env SEM deploy de código (basta reiniciar). Fail-closed (lança). ===
> 19	const TRADING_HALT = process.env.TRADING_HALT === 'true';
> 20	const _maxNotional = parseFloat(process.env.MAX_ORDER_NOTIONAL_USDT || '0');
> 21	const MAX_ORDER_NOTIONAL_USDT = Number.isFinite(_maxNotional) && _maxNotional > 0 ? _maxNotional : 0;
> 22	
> 23	function assertWithinRisk(action, symbol, quantity, price, options) {
> 24	    if (TRADING_HALT) {
> 25	        const msg = `[riskGuard] TRADING_HALT ativo — ${action} ${symbol} BLOQUEADA (kill-switch).`;
> 26	        logger('system', msg);
> 27	        throw new Error(msg);
> 28	    }
> 29	    if (MAX_ORDER_NOTIONAL_USDT > 0 && /USDT$/i.test(symbol || '')) {
> 30	        const o = options || {};
> 31	        let notional = null;
> 32	        if (o.quoteOrderQty != null) notional = parseFloat(o.quoteOrderQty);            // MARKET por quote (ex.: funil)
> 33	        else if (price != null && quantity != null) notional = parseFloat(price) * parseFloat(quantity); // LIMIT/OCO
> 34	        if (Number.isFinite(notional) && notional > MAX_ORDER_NOTIONAL_USDT) {
> 35	            const msg = `[riskGuard] ${action} ${symbol} notional $${notional.toFixed(2)} > teto $${MAX_ORDER_NOTIONAL_USDT.toFixed(2)} — BLOQUEADA.`;
> 36	            logger('system', msg);
> 37	            throw new Error(msg);
> 38	        }
> 39	    }
> 40	}
> 41	
> 42	module.exports = (settings) => {
> 43	
> 44	    if (!settings) throw new Error(`The settings object is required to connect on exchange!`);
> 45	
> 46	    // testnet x mainnet: na 1.x a WebSocket-API (userData) é roteada por Options.test,
> 47	    // NÃO pelas urls. Sem isso o userData tentaria autenticar no ws-api MAINNET com chave
> 48	    // testnet. Derivamos do apiUrl pra manter o BYOK funcionando nos dois ambientes.
> 49	    const isTestnet = /testnet|binance\.vision/i.test(settings.apiUrl || '');
> 50	
> 51	    const binance = new Binance().options({
> 52	        APIKEY: settings.accessKey,
> 53	        APISECRET: settings.secretKey,
> 54	        recvWindow: 60000,
> 55	        test: isTestnet,
> 56	        reconnect: true,
> 57	        urls: {
> 58	            base: settings.apiUrl.endsWith('/') ? settings.apiUrl : settings.apiUrl + '/',
> 59	            stream: settings.streamUrl.endsWith('/') ? settings.streamUrl : settings.streamUrl + '/'
> 60	        },
> 61	        verbose: LOGS
> 62	    });
> 63	
> 64	    // 1.x: websockets.terminate() indexa as subscriptions pela URL COMPLETA do socket, não
> 65	    // pelo nome curto do endpoint. Guardamos a URL retornada por chart()/prevDay() por stream
> 66	    // p/ conseguir fechá-lo depois (senão terminate vira no-op e o socket vaza/reconecta).
> 67	    const chartStreams = {};
> 68	    const tickerStreams = {};
> 69	
> 70	    function exchangeInfo() {
> 71	        return binance.exchangeInfo();
> 72	    }
> 73	
> 74	    async function balance() {
> 75	        await binance.useServerTime();
> 76	        return binance.balance();
> 77	    }
> 78	
> 79	    // 1.x: buy()/sell() fixam type='LIMIT' posicional e o guard interno de stopPrice dispara
> 80	    // ANTES de params sobrescrever o type -> ordens STOP via flags quebrariam. Por isso chamamos
> 81	    // binance.order(type, side, ...) direto (e marketBuy/marketSell p/ MARKET, que tratam
> 82	    // quoteOrderQty). Cobre MARKET/LIMIT/STOP_LOSS_LIMIT/TAKE_PROFIT_LIMIT/LIMIT_MAKER.
> 83	    function buy(symbol, quantity, price, options) {
> 84	        options = options || {};
> 85	        assertWithinRisk('BUY', symbol, quantity, price, options);
> 86	        const type = options.type || 'MARKET';
> 87	        if (type === 'MARKET')
> 88	            return binance.marketBuy(symbol, quantity, options);
> 89	        return binance.order(type, 'BUY', symbol, quantity, price, options);
> 90	    }
> 91	
> 92	    function sell(symbol, quantity, price, options) {
> 93	        options = options || {};
> 94	        assertWithinRisk('SELL', symbol, quantity, price, options);
> 95	        const type = options.type || 'MARKET';
> 96	        if (type === 'MARKET')
> 97	            return binance.marketSell(symbol, quantity, options);
> 98	        return binance.order(type, 'SELL', symbol, quantity, price, options);
> 99	    }
> 100	
> 101	    // OCO (destravado pelo bump p/ 1.x). ocoOrder usa o endpoint novo POST /api/v3/orderList/oco.
> 102	    // `options` segue o schema novo, p.ex. p/ um SELL protetivo após o buy:
> 103	    //   { aboveType:'LIMIT_MAKER', abovePrice, belowType:'STOP_LOSS_LIMIT',
> 104	    //     belowPrice, belowStopPrice, belowTimeInForce:'GTC' }
> 105	    function oco(side, symbol, quantity, options) {
> 106	        options = options || {};
> 107	        assertWithinRisk(`OCO-${side}`, symbol, quantity, options.abovePrice || options.belowPrice, options);
> 108	        return binance.ocoOrder(side, symbol, quantity, options);
> 109	    }
> 110	
> 111	    function cancel(symbol, orderId) {
> 112	        return binance.cancel(symbol, orderId);
> 113	    }
> 114	
> 115	    // Cancela uma OCO inteira (as 2 pernas) via DELETE /api/v3/orderList.
> 116	    function cancelOrderList(symbol, orderListId) {
> 117	        return binance.privateSpotRequest('v3/orderList', { symbol, orderListId }, 'DELETE');
> 118	    }
> 119	
> 120	    function orderStatus(symbol, orderId) {
> 121	        return binance.orderStatus(symbol, orderId);
> 122	    }
> 123	
> 124	    async function orderTrade(symbol, orderId) {
> 125	        const trades = await binance.trades(symbol);
> 126	        return trades.find(t => t.orderId === orderId);
> 127	    }
> 128	
> 129	    function withdraw(coin, amount, address, network, addressTag) {
> 130	        try {
> 131	            const data = { coin, amount, address };
> 132	            if (addressTag) data.addressTag = addressTag;
> 133	            if (network) data.network = network;
> 134	            return privateCall(SAPI_URL + 'capital/withdraw/apply', data, 'POST');
> 135	        } catch (err) {
> 136	            throw new Error(err.response ? JSON.stringify(err.response.data) : err.message);
> 137	        }
> 138	    }
> 139	
> 140	    async function getCoins() {
> 141	        try {
> 142	            const coins = await privateCall(SAPI_URL + 'capital/config/getall', null, 'GET');
> 143	            return coins.map(c => {
> 144	                return {
> 145	                    coin: c.coin,
> 146	                    networks: c.networkList.map(n => {
> 147	                        return {
> 148	                            network: n.network,
> 149	                            withdrawIntegerMultiple: n.withdrawIntegerMultiple,
> 150	                            isDefault: n.isDefault,
> 151	                            name: n.name,
> 152	                            withdrawFee: n.withdrawFee,
> 153	                            withdrawMin: n.withdrawMin,
> 154	                            minConfirm: n.minConfirm
> 155	                        }
> 156	                    })
> 157	                }
> 158	            })
> 159	        } catch (err) {
> 160	            throw new Error(err.response ? JSON.stringify(err.response.data) : err.message);
> 161	        }
> 162	    }
> 163	
> 164	    async function privateCall(apiUrl, data = {}, method = 'GET') {
> 165	
> 166	        const timestamp = Date.now();
> 167	        const recvWindow = 60000;
> 168	
> 169	        const axios = require('axios');
> 170	        const queryString = new URLSearchParams();
> 171	        Object.entries({ ...data, timestamp, recvWindow }).map(prop => queryString.append(prop[0], `${prop[1]}`));
> 172	
> 173	        const signature = require('crypto')
> 174	            .createHmac('sha256', settings.secretKey)
> 175	            .update(queryString.toString())
> 176	            .digest('hex');
> 177	
> 178	        queryString.append('signature', signature);
> 179	
> 180	        const result = await axios({
> 181	            method,
> 182	            url: `${apiUrl}?${queryString.toString()}`,
> 183	            headers: { 'X-MBX-APIKEY': settings.accessKey }
> 184	        })
> 185	
> 186	        return result.data;
> 187	    }
> 188	
> 189	    function miniTickerStream(callback) {
> 190	        binance.websockets.miniTicker(markets => {
> 191	            callback(markets)
> 192	        });
> 193	    }
> 194	
> 195	    // O monitor BOOK fica inativo por padrão (o book é simulado a partir do miniTicker em
> 196	    // app-em.js). Na 1.x o websockets.bookTickers mudou (perdeu o modo all-symbols e usa
> 197	    // conversor de futures); assinamos o stream cru !bookTicker e remapeamos. Best-effort.
> 198	    function bookStream(callback) {
> 199	        binance.websockets.subscribe('!bookTicker', data => {
> 200	            callback({
> 201	                updateId: data.u,
> 202	                symbol: data.s,
> 203	                bestBid: data.b,
> 204	                bestBidQty: data.B,
> 205	                bestAsk: data.a,
> 206	                bestAskQty: data.A
> 207	            })
> 208	        });
> 209	    }
> 210	
> 211	    function chartStream(symbol, interval, callback) {
> 212	        const streamUrl = binance.websockets.chart(symbol, interval, (symbol, interval, chart) => {
> 213	            const tick = binance.last(chart);
> 214	            const isIncomplete = tick && chart[tick] && chart[tick].isFinal === false;
> 215	            if ((!process.env.INCOMPLETE_CANDLES || process.env.INCOMPLETE_CANDLES === 'false') && isIncomplete)
> 216	                return;
> 217	
> 218	            const ohlc = binance.populateOHLC(chart); // 1.x: binance.ohlc() -> binance.populateOHLC()
> 219	            ohlc.isComplete = !isIncomplete;
> 220	
> 221	            callback(ohlc);
> 222	        });
> 223	        chartStreams[`${symbol.toLowerCase()}@kline_${interval}`] = streamUrl;
> 224	        if (LOGS) logger('system', `Chart Stream connected at ${streamUrl}`);
> 225	    }
> 226	
> 227	    function terminateChartStream(symbol, interval) {
> 228	        const key = `${symbol.toLowerCase()}@kline_${interval}`;
> 229	        const streamUrl = chartStreams[key];
> 230	        if (streamUrl) {
> 231	            binance.websockets.terminate(streamUrl);
> 232	            delete chartStreams[key];
> 233	        }
> 234	        logger('system', `Chart Stream ${key} terminated!`);
> 235	    }
> 236	
> 237	    // 1.x: a assinatura virou (all_updates_callback, balance_callback, execution_callback,
> 238	    // subscribed_callback, list_status_callback). all_updates_callback recebe TODOS os eventos
> 239	    // CRUS (com .e) — exatamente o que app-em.js consome (switch em data.e).
> 240	    function userDataStream(updateCallback, listStatusCallback) {
> 241	        binance.websockets.userData(
> 242	            data => updateCallback(data),
> 243	            undefined,
> 244	            undefined,
> 245	            subscribedData => logger('system', `userDataStream:subscribeEvent: ${JSON.stringify(subscribedData)}`),
> 246	            listStatusData => { if (listStatusCallback) listStatusCallback(listStatusData); });
> 247	    }
> 248	
> 249	    async function tickerStream(symbol, callback) {
> 250	        const streamUrl = binance.websockets.prevDay(symbol, (data, converted) => {
> 251	            callback(converted);
> 252	        })
> 253	        tickerStreams[`${symbol.toLowerCase()}@ticker`] = streamUrl;
> 254	        if (LOGS) logger('system', `Ticker Stream connected at ${streamUrl}`);
> 255	    }
> 256	
> 257	    function terminateTickerStream(symbol) {
> 258	        const key = `${symbol.toLowerCase()}@ticker`;
> 259	        const streamUrl = tickerStreams[key];
> 260	        if (streamUrl) {
> 261	            binance.websockets.terminate(streamUrl);
> 262	            delete tickerStreams[key];
> 263	        }
> 264	        logger('system', `Ticker Stream disconnected at ${key}`);
> 265	    }
> 266	
> 267	    return {
> 268	        exchangeInfo,
> 269	        balance,
> 270	        buy,
> 271	        sell,
> 272	        oco,
> 273	        cancel,
> 274	        cancelOrderList,
> 275	        miniTickerStream,
> 276	        bookStream,
> 277	        chartStream,
> 278	        terminateChartStream,
> 279	        terminateTickerStream,
> 280	        userDataStream,
> 281	        orderStatus,
> 282	        orderTrade,
> 283	        tickerStream,
> 284	        getCoins,
> 285	        withdraw
> 286	    }
> 287	}
> 288	
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	const technicalindicators = require('technicalindicators');
> 2	
> 3	const indexKeys = {
> 4	    //CANDLES PATTERNS
> 5	    INSIDE_CANDLE: 'INSIDE-CANDLE',
> 6	    ABANDONED_BABY: 'ABANDONED-BABY',
> 7	    BEARISH_ENGULFING: 'BEAR-ENGULF',
> 8	    BULLISH_ENGULFING: 'BULL-ENGULF',
> 9	    DARK_CLOUD_COVER: 'DARK-CLOUD-COVER',
> 10	    DOWNSIDE_TASUKI_GAP: 'DOWNSIDE-TASUKI-GAP',
> 11	    DOJI: 'DOJI',
> 12	    DRAGONFLY_DOJI: 'DRAGONFLY-DOJI',
> 13	    GRAVESTONE_DOJI: 'GRAVESTONE-DOJI',
> 14	    BEARISH_HARAMI: 'BEAR-HARAMI',
> 15	    BULLISH_HARAMI: 'BULL-HARAMI',
> 16	    BEARISH_HARAMI_CROSS: 'BEAR-HARAMIX',
> 17	    BULLISH_HARAMI_CROSS: 'BULL-HARAMIX',
> 18	    BULLISH_MARUBOZU: 'BULL-MARUBOZU',
> 19	    BEARISH_MARUBOZU: 'BEAR-MARUBOZU',
> 20	    EVENING_DOJI_STAR: 'EVENING-DOJI-STAR',
> 21	    EVENING_STAR: 'EVENINGSTAR',
> 22	    PIERCING_LINE: 'PIERCING-LINE',
> 23	    BULLISH_SPINNING_TOP: 'BULL-SPINTOP',
> 24	    BEARISH_SPINNING_TOP: 'BEAR-SPINTOP',
> 25	    MORNING_DOJI_STAR: 'MORNING-DOJI-STAR',
> 26	    MORNING_STAR: 'MORNING-STAR',
> 27	    _3BLACK_CROWS: '3BLACK-CROWS',
> 28	    _3WHITE_SOLDIERS: '3WHITE-SOLDIERS',
> 29	    BULLISH_HAMMER: 'BULLHAMMER',
> 30	    BEARISH_HAMMER: 'BEARHAMMER',
> 31	    BULLISH_INVERTED_HAMMER: 'BULL-INVERT-HAMMER',
> 32	    BEARISH_INVERTED_HAMMER: 'BEAR-INVERT-HAMMER',
> 33	    HAMMER: 'HAMMER',
> 34	    HAMMER_UNCONFIRMED: 'HAMMER-UNCONF',
> 35	    HANGING_MAN: 'HANGMAN',
> 36	    HANGING_MAN_UNCONFIRMED: 'HANGMAN-UNCONF',
> 37	    SHOOTING_STAR: 'SHOOTSTAR',
> 38	    SHOOTING_STAR_UNCONFIRMED: 'SHOOTSTAR-UNCONF',
> 39	    TWEEZER_TOP: 'TWEEZER-TOP',
> 40	    TWEEZER_BOTTOM: 'TWEEZER-BOTTOM',
> 41	    //TECHNICAL INDICATORS
> 42	    RSI: 'RSI',
> 43	    MACD: 'MACD',
> 44	    SMA: 'SMA',
> 45	    EMA: 'EMA',
> 46	    STOCH_RSI: 'S-RSI',
> 47	    BOLLINGER_BANDS: 'BB',
> 48	    ADL: 'ADL',
> 49	    ADX: 'ADX',
> 50	    ATR: 'ATR',
> 51	    AWESOME_OSCILLATOR: 'AO',
> 52	    CCI: 'CCI',
> 53	    FORCE_INDEX: 'FI',
> 54	    KST: 'KST',
> 55	    MFI: 'MFI',
> 56	    OBV: 'OBV',
> 57	    PSAR: 'PSAR',
> 58	    ROC: 'ROC',
> 59	    STOCH: 'STOCH',
> 60	    TRIX: 'TRIX',
> 61	    TYPICAL_PRICE: 'TYPICAL',
> 62	    VWAP: 'VWAP',
> 63	    VOLUME_PROFILE: 'VP',
> 64	    WMA: 'WMA',
> 65	    WEMA: 'WEMA',
> 66	    WILLIAMS_R: 'WILLIAMS-R',
> 67	    ICHIMOKU: 'ICHIMOKU',
> 68	    //BEHOLDER INDICATORS
> 69	    MINI_TICKER: 'MINI_TICKER',
> 70	    BOOK: 'BOOK',
> 71	    WALLET: 'WALLET',
> 72	    LAST_ORDER: 'LAST_ORDER',
> 73	    LAST_CANDLE: 'LAST_CANDLE',
> 74	    PREVIOUS_CANDLE: 'PREVIOUS_CANDLE',
> 75	    TICKER: 'TICKER',
> 76	    REGIME: 'REGIME',
> 77	    TREND_CROSS: 'TREND_CROSS',
> 78	    TREND_QTY: 'TREND_QTY', // posição (base asset) acumulada pelo Trend Following — id6 soma no fill golden, id7 zera no death
> 79	    FLOW: 'FLOW', // fluxo do taker da mainnet {imbalance,toxicity} (flowJob) — NOWCASTING/timing, NÃO forecast (ver RESEARCH-bear-capture). imbalance gateia a id2 (não comprar dip sob venda agressora AGORA)
> 80	    FAIR: 'FAIR', // preço de referência da MAINNET {price,at,atMs} (fairPriceJob) — âncora do Harvester de dislocação (compra-limite funda quando o testnet disloca abaixo do FAIR e reverte; sentinel price:0 = fail-safe)
> 81	    HARVEST: 'HARVEST', // bucket TÁTICO do Harvester {qty,cost} (base asset + custo médio; app-em.updateHarvestPosition) — venda no-loss usa quantity='HARVEST_QTY' (lê .qty); SEPARADO do cofre de BTC. PERSISTIDO (tabela harvestPositions, recarregado no boot por app-em.loadHarvestPositions)
> 82	    HARVEST_SELLING: 'HARVEST_SELLING', // trava da venda no-loss do Harvester: setada no place (beholder.placeOrder), liberada no estado TERMINAL da venda (app-em.updateHarvestPosition). Troca o edge-trigger por LEVEL-trigger sem oversell. Ausência = destravado (vende quando há lucro). NÃO persistida (reseta no boot; reconstruída se houver venda aberta)
> 83	    FARM_DCA: 'FARM_DCA' // preço médio ponderado (DCA) e quantidade de posições abertas no Farm {qty, cost}
> 84	}
> 85	
> 86	function getAnalysisIndexes() {
> 87	    return {
> 88	        [indexKeys.RSI]: { params: 'period', name: 'RSI' },
> 89	        [indexKeys.MACD]: { params: 'fast,slow,signal', name: 'MACD' },
> 90	        [indexKeys.SMA]: { params: 'period', name: 'SMA' },
> 91	        [indexKeys.EMA]: { params: 'period', name: 'EMA' },
> 92	        [indexKeys.STOCH_RSI]: { params: 'd,k,rsi,stoch', name: 'Stochastic RSI' },
> 93	        [indexKeys.BOLLINGER_BANDS]: { params: 'period,stdDev', name: 'Bollinger Bands (BB)' },
> 94	        [indexKeys.ADL]: { params: 'none', name: 'ADL' },
> 95	        [indexKeys.ADX]: { params: 'period', name: 'ADX' },
> 96	        [indexKeys.ATR]: { params: 'period', name: 'ATR' },
> 97	        [indexKeys.AWESOME_OSCILLATOR]: { params: 'fast,slow', name: 'Awesome Oscillator' },
> 98	        [indexKeys.CCI]: { params: 'period', name: 'CCI' },
> 99	        [indexKeys.FORCE_INDEX]: { params: 'period', name: 'Force Index' },
> 100	        [indexKeys.KST]: { params: 'roc1,roc2,roc3,roc4,smaroc1,smaroc2,smaroc3,smaroc4,signal', name: 'KST' },
> 101	        [indexKeys.MFI]: { params: 'period', name: 'MFI' },
> 102	        [indexKeys.OBV]: { params: 'none', name: 'OBV' },
> 103	        [indexKeys.PSAR]: { params: 'step,max', name: 'PSAR' },
> 104	        [indexKeys.ROC]: { params: 'period', name: 'ROC' },
> 105	        [indexKeys.STOCH]: { params: 'period,signal', name: 'Stochastic' },
> 106	        [indexKeys.TRIX]: { params: 'period', name: 'TRIX' },
> 107	        [indexKeys.TYPICAL_PRICE]: { params: 'none', name: 'Typical Price' },
> 108	        [indexKeys.VWAP]: { params: 'none', name: 'VWAP' },
> 109	        [indexKeys.VOLUME_PROFILE]: { params: 'bars', name: 'Volume Profile' },
> 110	        [indexKeys.WMA]: { params: 'period', name: 'WMA' },
> 111	        [indexKeys.WEMA]: { params: 'period', name: 'WEMA' },
> 112	        [indexKeys.WILLIAMS_R]: { params: 'period', name: 'Williams R' },
> 113	        [indexKeys.ICHIMOKU]: { params: 'conversion,base,span,displacement', name: 'Ichimoku' },
> 114	        [indexKeys.ABANDONED_BABY]: { params: 'none', name: 'Abandoned Baby' },
> 115	        [indexKeys.BEARISH_ENGULFING]: { params: 'none', name: 'Bearish Engulfing' },
> 116	        [indexKeys.BULLISH_ENGULFING]: { params: 'none', name: 'Bullish Engulfing' },
> 117	        [indexKeys.DARK_CLOUD_COVER]: { params: 'none', name: 'Dark Cloud Cover' },
> 118	        [indexKeys.DOWNSIDE_TASUKI_GAP]: { params: 'none', name: 'Downside Tasuki Gap' },
> 119	        [indexKeys.DOJI]: { params: 'none', name: 'Doji' },
> 120	        [indexKeys.DRAGONFLY_DOJI]: { params: 'none', name: 'DragonFly Doji' },
> 121	        [indexKeys.GRAVESTONE_DOJI]: { params: 'none', name: 'GraveStone Doji' },
> 122	        [indexKeys.BEARISH_HARAMI]: { params: 'none', name: 'Bearish Harami' },
> 123	        [indexKeys.BEARISH_HARAMI_CROSS]: { params: 'none', name: 'Bearish Harami Cross (X)' },
> 124	        [indexKeys.BULLISH_HARAMI]: { params: 'none', name: 'Bullish Harami' },
> 125	        [indexKeys.BULLISH_HARAMI_CROSS]: { params: 'none', name: 'Bullish Harami Cross (X)' },
> 126	        [indexKeys.BULLISH_MARUBOZU]: { params: 'none', name: 'Bullish Marubozu' },
> 127	        [indexKeys.BEARISH_MARUBOZU]: { params: 'none', name: 'Bearish Marubozu' },
> 128	        [indexKeys.EVENING_DOJI_STAR]: { params: 'none', name: 'Evening Doji Star' },
> 129	        [indexKeys.EVENING_STAR]: { params: 'none', name: 'Evening Star' },
> 130	        [indexKeys.PIERCING_LINE]: { params: 'none', name: 'Piercing Line' },
> 131	        [indexKeys.BULLISH_SPINNING_TOP]: { params: 'none', name: 'Bullish Spinning Top' },
> 132	        [indexKeys.BEARISH_SPINNING_TOP]: { params: 'none', name: 'Bearish Spinning Top' },
> 133	        [indexKeys.MORNING_DOJI_STAR]: { params: 'none', name: 'Morning Doji Star' },
> 134	        [indexKeys.MORNING_STAR]: { params: 'none', name: 'Morning Star' },
> 135	        [indexKeys._3BLACK_CROWS]: { params: 'none', name: '3 Black Crows' },
> 136	        [indexKeys._3WHITE_SOLDIERS]: { params: 'none', name: '3 White Soldiers' },
> 137	        [indexKeys.BULLISH_HAMMER]: { params: 'none', name: 'Bullish Hammer' },
> 138	        [indexKeys.BEARISH_HAMMER]: { params: 'none', name: 'Bearish Hammer' },
> 139	        [indexKeys.BULLISH_INVERTED_HAMMER]: { params: 'none', name: 'Bullish Inverted Hammer' },
> 140	        [indexKeys.BEARISH_INVERTED_HAMMER]: { params: 'none', name: 'Bearish Inverted Hammer' },
> 141	        [indexKeys.HAMMER]: { params: 'none', name: 'Hammer' },
> 142	        [indexKeys.HAMMER_UNCONFIRMED]: { params: 'none', name: 'Hammer (Unconf.)' },
> 143	        [indexKeys.HANGING_MAN]: { params: 'none', name: 'Hanging Man' },
> 144	        [indexKeys.HANGING_MAN_UNCONFIRMED]: { params: 'none', name: 'Haning Man (Unconf.)' },
> 145	        [indexKeys.SHOOTING_STAR]: { params: 'none', name: 'Shooting Star' },
> 146	        [indexKeys.SHOOTING_STAR_UNCONFIRMED]: { params: 'none', name: 'Shooting Star (Unconf.)' },
> 147	        [indexKeys.TWEEZER_TOP]: { params: 'none', name: 'Tweezer Top' },
> 148	        [indexKeys.TWEEZER_BOTTOM]: { params: 'none', name: 'Tweezer Bottom' },
> 149	        [indexKeys.INSIDE_CANDLE]: { params: 'bars', name: 'Inside Candle' },
> 150	    }
> 151	}
> 152	
> 153	function execCalc(indexName, ohlc, ...params) {
> 154	    switch (indexName) {
> 155	        case indexKeys.INSIDE_CANDLE: return insideCandle(ohlc, ...params);
> 156	        case indexKeys.ABANDONED_BABY: return abandonedBaby(ohlc);
> 157	        case indexKeys.ADL: return ADL(ohlc);
> 158	        case indexKeys.ADX: return ADX(ohlc, ...params);
> 159	        case indexKeys.ATR: return ATR(ohlc, ...params);
> 160	        case indexKeys.AWESOME_OSCILLATOR: return AO(ohlc, ...params);
> 161	        case indexKeys.BEARISH_ENGULFING: return bearishEngulfing(ohlc);
> 162	        case indexKeys.BEARISH_HARAMI: return bearishHarami(ohlc);
> 163	        case indexKeys.BULLISH_HARAMI: return bullishHarami(ohlc);
> 164	        case indexKeys.BEARISH_HARAMI_CROSS: return bearishHaramiCross(ohlc);
> 165	        case indexKeys.BULLISH_HARAMI_CROSS: return bullishHaramiCross(ohlc);
> 166	        case indexKeys.BULLISH_MARUBOZU: return bullishMarubozu(ohlc);
> 167	        case indexKeys.BEARISH_MARUBOZU: return bearishMarubozu(ohlc);
> 168	        case indexKeys.EVENING_DOJI_STAR: return eveningDojiStar(ohlc);
> 169	        case indexKeys.EVENING_STAR: return eveningStar(ohlc);
> 170	        case indexKeys.PIERCING_LINE: return piercingLine(ohlc);
> 171	        case indexKeys.BULLISH_SPINNING_TOP: return bullishSpinningTop(ohlc);
> 172	        case indexKeys.BEARISH_SPINNING_TOP: return bearishSpinningTop(ohlc);
> 173	        case indexKeys.MORNING_DOJI_STAR: return morningDojiStar(ohlc);
> 174	        case indexKeys.MORNING_STAR: return morningStar(ohlc);
> 175	        case indexKeys._3BLACK_CROWS: return threeBlackCrows(ohlc);
> 176	        case indexKeys._3WHITE_SOLDIERS: return threeWhiteSoldiers(ohlc);
> 177	        case indexKeys.BULLISH_HAMMER: return bullishHammer(ohlc);
> 178	        case indexKeys.BEARISH_HAMMER: return bearishHammer(ohlc);
> 179	        case indexKeys.BULLISH_INVERTED_HAMMER: return bullishInvertedHammer(ohlc);
> 180	        case indexKeys.BEARISH_INVERTED_HAMMER: return bearishInvertedHammer(ohlc);
> 181	        case indexKeys.HAMMER: return hammer(ohlc);
> 182	        case indexKeys.HAMMER_UNCONFIRMED: return hammerUnconfirmed(ohlc);
> 183	        case indexKeys.HANGING_MAN: return hangingMan(ohlc);
> 184	        case indexKeys.HANGING_MAN_UNCONFIRMED: return hangingManUnconfirmed(ohlc);
> 185	        case indexKeys.SHOOTING_STAR: return shootingStar(ohlc);
> 186	        case indexKeys.SHOOTING_STAR_UNCONFIRMED: return shootingStarUnconfirmed(ohlc);
> 187	        case indexKeys.TWEEZER_TOP: return tweezerTop(ohlc);
> 188	        case indexKeys.TWEEZER_BOTTOM: return tweezerBottom(ohlc);
> 189	        case indexKeys.BOLLINGER_BANDS: return bollingerBands(ohlc.close, ...params);
> 190	        case indexKeys.BULLISH_ENGULFING: return bullishEngulfing(ohlc);
> 191	        case indexKeys.CCI: return CCI(ohlc, ...params);
> 192	        case indexKeys.DARK_CLOUD_COVER: return darkCloudCover(ohlc);
> 193	        case indexKeys.DOJI: return doji(ohlc);
> 194	        case indexKeys.DOWNSIDE_TASUKI_GAP: return downsideTasukiGap(ohlc);
> 195	        case indexKeys.DRAGONFLY_DOJI: return dragonflyDoji(ohlc);
> 196	        case indexKeys.EMA: return EMA(ohlc.close, ...params);
> 197	        case indexKeys.FORCE_INDEX: return FI(ohlc, ...params);
> 198	        case indexKeys.GRAVESTONE_DOJI: return graveStoneDoji(ohlc);
> 199	        case indexKeys.ICHIMOKU: return ichimoku(ohlc, ...params);
> 200	        case indexKeys.KST: return KST(ohlc.close, ...params);
> 201	        case indexKeys.MACD: return MACD(ohlc.close, ...params);
> 202	        case indexKeys.MFI: return MFI(ohlc, ...params);
> 203	        case indexKeys.OBV: return OBV(ohlc);
> 204	        case indexKeys.PSAR: return PSAR(ohlc, ...params);
> 205	        case indexKeys.ROC: return ROC(ohlc.close, ...params);
> 206	        case indexKeys.RSI: return RSI(ohlc.close, ...params);
> 207	        case indexKeys.SMA: return SMA(ohlc.close, ...params);
> 208	        case indexKeys.STOCH: return Stochastic(ohlc, ...params);
> 209	        case indexKeys.STOCH_RSI: return StochRSI(ohlc.close, ...params);
> 210	        case indexKeys.TRIX: return TRIX(ohlc.close, ...params);
> 211	        case indexKeys.VOLUME_PROFILE: return VP(ohlc, ...params);
> 212	        case indexKeys.VWAP: return VWAP(ohlc);
> 213	        case indexKeys.WILLIAMS_R: return williamsR(ohlc, ...params);
> 214	        case indexKeys.WEMA: return WEMA(ohlc.close, ...params);
> 215	        case indexKeys.WMA: return WMA(ohlc.close, ...params);
> 216	        default: throw new Error(`Unknown index name: ${indexName}`);
> 217	    }
> 218	}
> 219	
> 220	function getInsideCandle(ohlc, last, bars) {
> 221	    let hasInsideCandle = ohlc.high[last] < ohlc.high[last - 1] && ohlc.low[last] > ohlc.low[last - 1];
> 222	    if (hasInsideCandle && bars > 1) {
> 223	        for (let i = 1; i < bars; i++)
> 224	            hasInsideCandle = hasInsideCandle && ohlc.high[last - i] < ohlc.high[last - i - 1] && ohlc.low[last - i] > ohlc.low[last - i - 1];
> 225	    }
> 226	    return hasInsideCandle;
> 227	}
> 228	
> 229	function insideCandle(ohlc, bars = 1) {
> 230	    const current = getInsideCandle(ohlc, ohlc.high.length - 1, bars);
> 231	    const previous = getInsideCandle(ohlc, ohlc.high.length - 2, bars);
> 232	    return { current, previous };
> 233	}
> 234	
> 235	function abandonedBaby(ohlc) {
> 236	    const input = getThreeCandles(ohlc);
> 237	    return technicalindicators.abandonedbaby(input);
> 238	}
> 239	
> 240	function bullishEngulfing(ohlc) {
> 241	    const input = getTwoCandles(ohlc);
> 242	    return technicalindicators.bullishengulfingpattern(input);
> 243	}
> 244	
> 245	function bearishEngulfing(ohlc) {
> 246	    const input = getTwoCandles(ohlc);
> 247	    return technicalindicators.bearishengulfingpattern(input);
> 248	}
> 249	
> 250	function darkCloudCover(ohlc) {
> 251	    const input = getTwoCandles(ohlc);
> 252	    return technicalindicators.darkcloudcover(input);
> 253	}
> 254	
> 255	function downsideTasukiGap(ohlc) {
> 256	    const input = getThreeCandles(ohlc);
> 257	    return technicalindicators.downsidetasukigap(input);
> 258	}
> 259	
> 260	function doji(ohlc) {
> 261	    const input = getOneCandle(ohlc);
> 262	    return technicalindicators.doji(input);
> 263	}
> 264	
> 265	function dragonflyDoji(ohlc) {
> 266	    const input = getOneCandle(ohlc);
> 267	    return technicalindicators.dragonflydoji(input);
> 268	}
> 269	
> 270	function graveStoneDoji(ohlc) {
> 271	    const input = getOneCandle(ohlc);
> 272	    return technicalindicators.gravestonedoji(input);
> 273	}
> 274	
> 275	function bearishHarami(ohlc) {
> 276	    const input = getTwoCandles(ohlc);
> 277	    return technicalindicators.bearishharami(input);
> 278	}
> 279	
> 280	function bullishHarami(ohlc) {
> 281	    const input = getTwoCandles(ohlc);
> 282	    return technicalindicators.bullishharami(input);
> 283	}
> 284	
> 285	function bullishHaramiCross(ohlc) {
> 286	    const input = getTwoCandles(ohlc);
> 287	    return technicalindicators.bullishharamicross(input);
> 288	}
> 289	
> 290	function bearishHaramiCross(ohlc) {
> 291	    const input = getTwoCandles(ohlc);
> 292	    return technicalindicators.bearishharamicross(input);
> 293	}
> 294	
> 295	function bullishMarubozu(ohlc) {
> 296	    const input = getOneCandle(ohlc);
> 297	    return technicalindicators.bullishmarubozu(input);
> 298	}
> 299	
> 300	function bearishMarubozu(ohlc) {
> 301	    const input = getOneCandle(ohlc);
> 302	    return technicalindicators.bearishmarubozu(input);
> 303	}
> 304	
> 305	function eveningDojiStar(ohlc) {
> 306	    const input = getThreeCandles(ohlc);
> 307	    return technicalindicators.eveningdojistar(input);
> 308	}
> 309	
> 310	function eveningStar(ohlc) {
> 311	    const input = getThreeCandles(ohlc);
> 312	    return technicalindicators.eveningstar(input);
> 313	}
> 314	
> 315	function piercingLine(ohlc) {
> 316	    const input = getTwoCandles(ohlc);
> 317	    return technicalindicators.piercingline(input);
> 318	}
> 319	
> 320	function bullishSpinningTop(ohlc) {
> 321	    const input = getOneCandle(ohlc);
> 322	    return technicalindicators.bullishspinningtop(input);
> 323	}
> 324	
> 325	function bearishSpinningTop(ohlc) {
> 326	    const input = getOneCandle(ohlc);
> 327	    return technicalindicators.bearishspinningtop(input);
> 328	}
> 329	
> 330	function morningDojiStar(ohlc) {
> 331	    const input = getThreeCandles(ohlc);
> 332	    return technicalindicators.morningdojistar(input);
> 333	}
> 334	
> 335	function morningStar(ohlc) {
> 336	    const input = getThreeCandles(ohlc);
> 337	    return technicalindicators.morningstar(input);
> 338	}
> 339	
> 340	function threeBlackCrows(ohlc) {
> 341	    const input = getThreeCandles(ohlc);
> 342	    return technicalindicators.threeblackcrows(input);
> 343	}
> 344	
> 345	function threeWhiteSoldiers(ohlc) {
> 346	    const input = getThreeCandles(ohlc);
> 347	    return technicalindicators.threewhitesoldiers(input);
> 348	}
> 349	
> 350	function bullishHammer(ohlc) {
> 351	    const input = getOneCandle(ohlc);
> 352	    return technicalindicators.bullishhammerstick(input);
> 353	}
> 354	
> 355	function bearishHammer(ohlc) {
> 356	    const input = getOneCandle(ohlc);
> 357	    return technicalindicators.bearishhammerstick(input);
> 358	}
> 359	
> 360	function bearishInvertedHammer(ohlc) {
> 361	    const input = getOneCandle(ohlc);
> 362	    return technicalindicators.bearishinvertedhammerstick(input);
> 363	}
> 364	
> 365	function bullishInvertedHammer(ohlc) {
> 366	    const input = getOneCandle(ohlc);
> 367	    return technicalindicators.bullishinvertedhammerstick(input);
> 368	}
> 369	
> 370	function hammer(ohlc) {
> 371	    const input = getFiveCandles(ohlc);
> 372	    return technicalindicators.hammerpattern(input);
> 373	}
> 374	
> 375	function hammerUnconfirmed(ohlc) {
> 376	    const input = getFiveCandles(ohlc);
> 377	    return technicalindicators.hammerpatternunconfirmed(input);
> 378	}
> 379	
> 380	function hangingMan(ohlc) {
> 381	    const input = getFiveCandles(ohlc);
> 382	    return technicalindicators.hangingman(input);
> 383	}
> 384	
> 385	function hangingManUnconfirmed(ohlc) {
> 386	    const input = getFiveCandles(ohlc);
> 387	    return technicalindicators.hangingmanunconfirmed(input);
> 388	}
> 389	
> 390	function shootingStar(ohlc) {
> 391	    const input = getFiveCandles(ohlc);
> 392	    return technicalindicators.shootingstar(input);
> 393	}
> 394	
> 395	function shootingStarUnconfirmed(ohlc) {
> 396	    const input = getFiveCandles(ohlc);
> 397	    return technicalindicators.shootingstarunconfirmed(input);
> 398	}
> 399	
> 400	function tweezerTop(ohlc) {
> 401	    const input = getFiveCandles(ohlc);
> 402	    return technicalindicators.tweezertop(input);
> 403	}
> 404	
> 405	function tweezerBottom(ohlc) {
> 406	    const input = getFiveCandles(ohlc);
> 407	    return technicalindicators.tweezerbottom(input);
> 408	}
> 409	
> 410	function getFiveCandles(ohlc) {
> 411	    const last = ohlc.high.length - 1;
> 412	    return {
> 413	        open: [ohlc.open[last], ohlc.open[last - 1], ohlc.open[last - 2], ohlc.open[last - 3], ohlc.open[last - 4]],
> 414	        close: [ohlc.close[last], ohlc.close[last - 1], ohlc.close[last - 2], ohlc.close[last - 3], ohlc.close[last - 4]],
> 415	        high: [ohlc.high[last], ohlc.high[last - 1], ohlc.high[last - 2], ohlc.high[last - 3], ohlc.high[last - 4]],
> 416	        low: [ohlc.low[last], ohlc.low[last - 1], ohlc.low[last - 2], ohlc.low[last - 3], ohlc.low[last - 4]],
> 417	        volume: [ohlc.volume[last], ohlc.volume[last - 1], ohlc.volume[last - 2], ohlc.volume[last - 3], ohlc.volume[last - 4]],
> 418	    }
> 419	}
> 420	
> 421	function getThreeCandles(ohlc) {
> 422	    const last = ohlc.high.length - 1;
> 423	    return {
> 424	        open: [ohlc.open[last], ohlc.open[last - 1], ohlc.open[last - 2]],
> 425	        close: [ohlc.close[last], ohlc.close[last - 1], ohlc.close[last - 2]],
> 426	        high: [ohlc.high[last], ohlc.high[last - 1], ohlc.high[last - 2]],
> 427	        low: [ohlc.low[last], ohlc.low[last - 1], ohlc.low[last - 2]],
> 428	        volume: [ohlc.volume[last], ohlc.volume[last - 1], ohlc.volume[last - 2]],
> 429	    }
> 430	}
> 431	
> 432	function getTwoCandles(ohlc) {
> 433	    const last = ohlc.high.length - 1;
> 434	    return {
> 435	        open: [ohlc.open[last], ohlc.open[last - 1]],
> 436	        close: [ohlc.close[last], ohlc.close[last - 1]],
> 437	        high: [ohlc.high[last], ohlc.high[last - 1]],
> 438	        low: [ohlc.low[last], ohlc.low[last - 1]],
> 439	        volume: [ohlc.volume[last], ohlc.volume[last - 1]],
> 440	    }
> 441	}
> 442	
> 443	function getOneCandle(ohlc) {
> 444	    const last = ohlc.high.length - 1;
> 445	    return {
> 446	        open: [ohlc.open[last]],
> 447	        close: [ohlc.close[last]],
> 448	        high: [ohlc.high[last]],
> 449	        low: [ohlc.low[last]],
> 450	        volume: [ohlc.volume[last]],
> 451	    }
> 452	}
> 453	
> 454	function ADL(ohlc) {
> 455	    const adlResult = technicalindicators.adl(ohlc);
> 456	    return {
> 457	        current: adlResult[adlResult.length - 1],
> 458	        previous: adlResult[adlResult.length - 2]
> 459	    }
> 460	}
> 461	
> 462	function ADX(ohlc, period = 14) {
> 463	    period = parseInt(period);
> 464	    if (ohlc.close.length <= period) return { current: false, previous: false };
> 465	
> 466	    const adxResult = technicalindicators.adx({
> 467	        high: ohlc.high,
> 468	        low: ohlc.low,
> 469	        close: ohlc.close,
> 470	        period
> 471	    })
> 472	    return {
> 473	        current: adxResult[adxResult.length - 1],
> 474	        previous: adxResult[adxResult.length - 2]
> 475	    }
> 476	}
> 477	
> 478	function ATR(ohlc, period = 14) {
> 479	    period = parseInt(period);
> 480	    if (ohlc.close.length <= period) return { current: false, previous: false };
> 481	
> 482	    const atrResult = technicalindicators.atr({
> 483	        high: ohlc.high,
> 484	        low: ohlc.low,
> 485	        close: ohlc.close,
> 486	        period
> 487	    })
> 488	    return {
> 489	        current: atrResult[atrResult.length - 1],
> 490	        previous: atrResult[atrResult.length - 2]
> 491	    }
> 492	}
> 493	
> 494	function AO(ohlc, fastPeriod = 5, slowPeriod = 34) {
> 495	    fastPeriod = parseInt(fastPeriod);
> 496	    slowPeriod = parseInt(slowPeriod);
> 497	    if ([fastPeriod, slowPeriod].some(p => p >= ohlc.high.length)) return { current: false, previous: false };
> 498	
> 499	    const aoResult = technicalindicators.awesomeoscillator({
> 500	        high: ohlc.high,
> 501	        low: ohlc.low,
> 502	        fastPeriod,
> 503	        slowPeriod
> 504	    })
> 505	    return {
> 506	        current: aoResult[aoResult.length - 1],
> 507	        previous: aoResult[aoResult.length - 2]
> 508	    }
> 509	}
> 510	
> 511	function CCI(ohlc, period = 20) {
> 512	    period = parseInt(period);
> 513	    if (ohlc.close.length <= period) return { current: false, previous: false };
> 514	
> 515	    const cciResult = technicalindicators.cci({
> 516	        open: ohlc.open,
> 517	        high: ohlc.high,
> 518	        low: ohlc.low,
> 519	        close: ohlc.close,
> 520	        period
> 521	    })
> 522	    return {
> 523	        current: cciResult[cciResult.length - 1],
> 524	        previous: cciResult[cciResult.length - 2]
> 525	    }
> 526	}
> 527	
> 528	function FI(ohlc, period = 1) {
> 529	    period = parseInt(period);
> 530	    if (ohlc.close.length <= period) return { current: false, previous: false };
> 531	
> 532	    const fiResult = technicalindicators.forceindex({
> 533	        open: ohlc.open,
> 534	        high: ohlc.high,
> 535	        low: ohlc.low,
> 536	        close: ohlc.close,
> 537	        volume: ohlc.volume,
> 538	        period
> 539	    })
> 540	    return {
> 541	        current: fiResult[fiResult.length - 1],
> 542	        previous: fiResult[fiResult.length - 2]
> 543	    }
> 544	}
> 545	
> 546	function KST(closes, ROCPer1 = 10, ROCPer2 = 15, ROCPer3 = 20, ROCPer4 = 30, SMAROCPer1 = 10, SMAROCPer2 = 10, SMAROCPer3 = 10, SMAROCPer4 = 15, signal = 3) {
> 547	    ROCPer1 = parseInt(ROCPer1);
> 548	    ROCPer2 = parseInt(ROCPer2);
> 549	    ROCPer3 = parseInt(ROCPer3);
> 550	    ROCPer4 = parseInt(ROCPer4);
> 551	    SMAROCPer1 = parseInt(SMAROCPer1);
> 552	    SMAROCPer2 = parseInt(SMAROCPer2);
> 553	    SMAROCPer3 = parseInt(SMAROCPer3);
> 554	    SMAROCPer4 = parseInt(SMAROCPer4);
> 555	
> 556	    if ([ROCPer1, ROCPer2, ROCPer3, ROCPer4, SMAROCPer1, SMAROCPer2, SMAROCPer3, SMAROCPer4].some(p => p >= closes.length))
> 557	        return { current: false, previous: false };
> 558	
> 559	    const kstResult = technicalindicators.kst({
> 560	        values: closes,
> 561	        ROCPer1,
> 562	        ROCPer2,
> 563	        ROCPer3,
> 564	        ROCPer4,
> 565	        SMAROCPer1,
> 566	        SMAROCPer2,
> 567	        SMAROCPer3,
> 568	        SMAROCPer4,
> 569	        signalPeriod: parseInt(signal),
> 570	    })
> 571	    return {
> 572	        current: kstResult[kstResult.length - 1],
> 573	        previous: kstResult[kstResult.length - 2]
> 574	    }
> 575	}
> 576	
> 577	function MFI(ohlc, period = 14) {
> 578	    period = parseInt(period);
> 579	    if (ohlc.close.length <= period) return { current: false, previous: false };
> 580	
> 581	    const mfiResult = technicalindicators.mfi({
> 582	        high: ohlc.high,
> 583	        low: ohlc.low,
> 584	        close: ohlc.close,
> 585	        volume: ohlc.volume,
> 586	        period
> 587	    })
> 588	    return {
> 589	        current: mfiResult[mfiResult.length - 1],
> 590	        previous: mfiResult[mfiResult.length - 2]
> 591	    }
> 592	}
> 593	
> 594	function OBV(ohlc) {
> 595	    const obvResult = technicalindicators.obv({
> 596	        close: ohlc.close,
> 597	        volume: ohlc.volume
> 598	    })
> 599	    return {
> 600	        current: obvResult[obvResult.length - 1],
> 601	        previous: obvResult[obvResult.length - 2]
> 602	    }
> 603	}
> 604	
> 605	function PSAR(ohlc, step, max) {
> 606	    const psarResult = technicalindicators.psar({
> 607	        high: ohlc.high,
> 608	        low: ohlc.low,
> 609	        step: parseFloat(step) || 0.02,
> 610	        max: parseFloat(max) || 0.2
> 611	    })
> 612	    return {
> 613	        current: psarResult[psarResult.length - 1],
> 614	        previous: psarResult[psarResult.length - 2]
> 615	    }
> 616	}
> 617	
> 618	function ROC(closes, period = 12) {
> 619	    period = parseInt(period);
> 620	    if (closes.length <= period) return { current: false, previous: false };
> 621	
> 622	    const rocResult = technicalindicators.roc({
> 623	        period,
> 624	        values: closes
> 625	    })
> 626	    return {
> 627	        current: rocResult[rocResult.length - 1],
> 628	        previous: rocResult[rocResult.length - 2]
> 629	    }
> 630	}
> 631	
> 632	function Stochastic(ohlc, period = 14, signal = 3) {
> 633	    period = parseInt(period);
> 634	    if (ohlc.close.length <= period) return { current: false, previous: false };
> 635	
> 636	    const stochResult = technicalindicators.stochastic({
> 637	        high: ohlc.high,
> 638	        low: ohlc.low,
> 639	        close: ohlc.close,
> 640	        period,
> 641	        signalPeriod: signal
> 642	    })
> 643	    return {
> 644	        current: stochResult[stochResult.length - 1],
> 645	        previous: stochResult[stochResult.length - 2]
> 646	    }
> 647	}
> 648	
> 649	function TRIX(closes, period = 18) {
> 650	    period = parseInt(period);
> 651	    if (closes.length <= period) return { current: false, previous: false };
> 652	
> 653	    const trixResult = technicalindicators.trix({
> 654	        period,
> 655	        values: closes
> 656	    })
> 657	    return {
> 658	        current: trixResult[trixResult.length - 1],
> 659	        previous: trixResult[trixResult.length - 2]
> 660	    }
> 661	}
> 662	
> 663	function VWAP(ohlc) {
> 664	    const vwapResult = technicalindicators.vwap(ohlc);
> 665	    return {
> 666	        current: vwapResult[vwapResult.length - 1],
> 667	        previous: vwapResult[vwapResult.length - 2]
> 668	    }
> 669	}
> 670	
> 671	function VP(ohlc, bars = 14) {
> 672	    bars = parseInt(bars);
> 673	    if (ohlc.close.length <= bars) return { current: false, previous: false };
> 674	
> 675	    const vpResult = technicalindicators.volumeprofile({
> 676	        open: ohlc.open,
> 677	        high: ohlc.high,
> 678	        low: ohlc.low,
> 679	        close: ohlc.close,
> 680	        volume: ohlc.volume,
> 681	        noOfBars: bars
> 682	    })
> 683	    return {
> 684	        current: vpResult[vpResult.length - 1],
> 685	        previous: vpResult[vpResult.length - 2]
> 686	    }
> 687	}
> 688	
> 689	function williamsR(ohlc, period = 14) {
> 690	    period = parseInt(period);
> 691	    if (ohlc.close.length <= period) return { current: false, previous: false };
> 692	
> 693	    const wrResult = technicalindicators.williamsr({
> 694	        open: ohlc.open,
> 695	        high: ohlc.high,
> 696	        low: ohlc.low,
> 697	        close: ohlc.close,
> 698	        period
> 699	    })
> 700	    return {
> 701	        current: wrResult[wrResult.length - 1],
> 702	        previous: wrResult[wrResult.length - 2]
> 703	    }
> 704	}
> 705	
> 706	function ichimoku(ohlc, conversionPeriod = 9, basePeriod = 26, span = 52, displacement = 26) {
> 707	    conversionPeriod = parseInt(conversionPeriod);
> 708	    basePeriod = parseInt(basePeriod);
> 709	    span = parseInt(span);
> 710	    displacement = parseInt(displacement);
> 711	
> 712	    if ([conversionPeriod, basePeriod, span, displacement].some(p => p >= ohlc.high.length))
> 713	        return { current: false, previous: false };
> 714	
> 715	    const ichimokuResult = technicalindicators.ichimokucloud({
> 716	        high: ohlc.high,
> 717	        low: ohlc.low,
> 718	        conversionPeriod,
> 719	        basePeriod,
> 720	        span,
> 721	        displacement
> 722	    })
> 723	    return {
> 724	        current: ichimokuResult[ichimokuResult.length - 1],
> 725	        previous: ichimokuResult[ichimokuResult.length - 2]
> 726	    }
> 727	}
> 728	
> 729	function WMA(closes, period = 8) {
> 730	    period = parseInt(period);
> 731	    if (closes.length <= period) return { current: false, previous: false };
> 732	
> 733	    const wmaResult = technicalindicators.wma({
> 734	        period,
> 735	        values: closes
> 736	    })
> 737	    return {
> 738	        current: wmaResult[wmaResult.length - 1],
> 739	        previous: wmaResult[wmaResult.length - 2]
> 740	    }
> 741	}
> 742	
> 743	function WEMA(closes, period = 5) {
> 744	    period = parseInt(period);
> 745	    if (closes.length <= period) return { current: false, previous: false };
> 746	
> 747	    const wemaResult = technicalindicators.wema({
> 748	        period,
> 749	        values: closes
> 750	    })
> 751	    return {
> 752	        current: wemaResult[wemaResult.length - 1],
> 753	        previous: wemaResult[wemaResult.length - 2]
> 754	    }
> 755	}
> 756	
> 757	function RSI(closes, period = 14) {
> 758	    period = parseInt(period);
> 759	    if (closes.length <= period) return { current: false, previous: false };
> 760	
> 761	    const rsiResult = technicalindicators.rsi({
> 762	        period,
> 763	        values: closes
> 764	    })
> 765	    return {
> 766	        current: parseFloat(rsiResult[rsiResult.length - 1]),
> 767	        previous: parseFloat(rsiResult[rsiResult.length - 2]),
> 768	    }
> 769	}
> 770	
> 771	function MACD(closes, fastPeriod = 12, slowPeriod = 26, signalPeriod = 9) {
> 772	    fastPeriod = parseInt(fastPeriod);
> 773	    slowPeriod = parseInt(slowPeriod);
> 774	    signalPeriod = parseInt(signalPeriod);
> 775	
> 776	    if ([fastPeriod, slowPeriod, signalPeriod].some(p => p >= closes.length)) return { current: false, previous: false };
> 777	
> 778	    const macdResult = technicalindicators.macd({
> 779	        values: closes,
> 780	        SimpleMAOscillator: false,
> 781	        SimpleMASignal: false,
> 782	        fastPeriod,
> 783	        slowPeriod,
> 784	        signalPeriod
> 785	    });
> 786	    return {
> 787	        current: macdResult[macdResult.length - 1],
> 788	        previous: macdResult[macdResult.length - 2]
> 789	    }
> 790	}
> 791	
> 792	function StochRSI(closes, dPeriod = 3, kPeriod = 3, rsiPeriod = 14, stochasticPeriod = 14) {
> 793	    dPeriod = parseInt(dPeriod);
> 794	    kPeriod = parseInt(kPeriod);
> 795	    rsiPeriod = parseInt(rsiPeriod);
> 796	    stochasticPeriod = parseInt(stochasticPeriod);
> 797	
> 798	    if ([dPeriod, kPeriod, rsiPeriod, stochasticPeriod].some(p => p >= closes.length)) return { current: false, previous: false };
> 799	
> 800	    const stochResult = technicalindicators.stochasticrsi({
> 801	        dPeriod,
> 802	        kPeriod,
> 803	        rsiPeriod,
> 804	        stochasticPeriod,
> 805	        values: closes
> 806	    });
> 807	    return {
> 808	        current: stochResult[stochResult.length - 1],
> 809	        previous: stochResult[stochResult.length - 2]
> 810	    }
> 811	}
> 812	
> 813	function bollingerBands(closes, period = 20, stdDev = 2) {
> 814	    period = parseInt(period);
> 815	    if (closes.length <= period) return { current: false, previous: false };
> 816	
> 817	    const bbResult = technicalindicators.bollingerbands({
> 818	        period,
> 819	        stdDev: parseInt(stdDev),
> 820	        values: closes
> 821	    })
> 822	    return {
> 823	        current: bbResult[bbResult.length - 1],
> 824	        previous: bbResult[bbResult.length - 2]
> 825	    }
> 826	}
> 827	
> 828	function SMA(closes, period = 10) {
> 829	    period = parseInt(period);
> 830	    if (closes.length <= period) return { current: false, previous: false };
> 831	
> 832	    const smaResult = technicalindicators.sma({
> 833	        values: closes,
> 834	        period
> 835	    });
> 836	    return {
> 837	        current: smaResult[smaResult.length - 1],
> 838	        previous: smaResult[smaResult.length - 2],
> 839	    }
> 840	}
> 841	
> 842	function EMA(closes, period = 10) {
> 843	    period = parseInt(period);
> 844	    if (closes.length <= period) return { current: false, previous: false };
> 845	
> 846	    const emaResult = technicalindicators.ema({
> 847	        values: closes,
> 848	        period
> 849	    });
> 850	    return {
> 851	        current: emaResult[emaResult.length - 1],
> 852	        previous: emaResult[emaResult.length - 2],
> 853	    }
> 854	}
> 855	
> 856	module.exports = {
> 857	    indexKeys,
> 858	    execCalc,
> 859	    getAnalysisIndexes
> 860	}
> 861	
> ```

## 🤖 Claude *(18:55:51)*

I have enough from the four files to map the 1-minute data plumbing. Let me verify a couple of load-bearing details about the FAIR/FLOW/REGIME jobs (which symbols, what cadence) since those MEMORY indexes exist but aren't populated in the four files I read.

## 🤖 Claude *(18:55:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux/backend/src && grep -rln \"REGIME\\|:FLOW\\|:FAIR\\|TREND_CROSS\\|aggTrade\\|fairPrice\\|flowJob\\|regimeJob\" --include=*.js | sort",
  "description": "Find files that populate REGIME/FLOW/FAIR/TREND indexes and aggTrades"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> app-em.js
> controllers/analysisController.js
> fairPriceJob.js
> flowJob.js
> funnelJob.js
> models/regimeStateModel.js
> regimeJob.js
> repositories/regimeStatesRepository.js
> server.js
> utils/fairPriceService.js
> utils/flowService.js
> utils/indexes.js
> utils/regimeClassifier.js
> utils/regimeService.js
> ```

## 🤖 Claude *(18:55:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux/backend/src && grep -rn \"interval\\|cron\\|setInterval\\|schedule\\|1m\\|aggTrades\\|klines\\|miniTicker\" jobs/ 2>/dev/null | head -60; echo \"---LS JOBS---\"; ls -la jobs/ 2>/dev/null",
  "description": "Inspect jobs directory cadence and stream usage"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 2
> ---LS JOBS---
> ```

## 🤖 Claude *(18:55:57)*

The jobs are at the root of `src/`. Let me read the three jobs and their cadence to pin down the intervals and which symbols/streams feed REGIME/FLOW/FAIR.

## 🤖 Claude *(18:55:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux/backend/src && for f in regimeJob.js flowJob.js fairPriceJob.js; do echo \"===== $f (head) =====\"; sed -n '1,60p' \"$f\"; done",
  "description": "Read heads of regime/flow/fairPrice jobs for cadence and streams"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== regimeJob.js (head) =====
> 'use strict';
> /*
>  * Regime Job — grava o regime de mercado na MEMORY do Beholder periodicamente, para que as
>  * automações possam GATEAR a entrada (ex.: "não comprar em bear"). É o ENABLER que torna a
>  * estratégia regime-gated (a melhor risco-ajustada no backtest: caixa no bear) deployável ao vivo.
>  *
>  * Escreve uma STRING simples por símbolo:  MEMORY['<symbol>:REGIME'] = 'bear'|'trend'|'range'|'mixed'
>  * para que a condição da automação seja uma igualdade trivial:  MEMORY['<symbol>:REGIME']!=='bear'.
>  *
>  * Decisões de segurança (caminho de dinheiro):
>  *  - executeAutomations=false: a escrita do regime NÃO dispara ordens por si. O regime é um GATE
>  *    PASSIVO, lido quando o tick de preço/RSI dispara a automação — não um gatilho ativo (evita
>  *    comprar sobre um sinal de RSI velho na cadência do poll).
>  *  - skip-on-unknown: se a Binance não responder ou houver poucos dados, NÃO sobrescreve a MEMORY
>  *    (preserva o último regime conhecido e evita derrubar o gate por um soluço de rede). Combinado
>  *    com 'BTCUSDT:REGIME' nos `indexes` da automação, no 1º boot sem regime conhecido a automação
>  *    fica fail-safe (não compra até o regime ser conhecido).
>  *  - kill-switch REGIME_JOB_ENABLED=false: para o job (e, com REGIME nos indexes, pausa as compras
>  *    gateadas — fail-safe).
>  *
>  * Env:
>  *  REGIME_JOB_ENABLED  (default 'true')   — liga/desliga o job
>  *  REGIME_REFRESH_MS   (default 300000)   — intervalo do poll (5 min; regime de velas 1h muda devagar)
>  *  REGIME_INTERVAL     (default '1h')     — timeframe das velas usadas na classificação
>  *  REGIME_SYMBOLS      (CSV, opcional)    — força a lista de símbolos; senão usa os das automações ativas
>  *  FASE4_MACRO_SYMBOL  (default 'BTCUSDT') — símbolo cuja SAÍDA do bear arma a observação da Fase 4 (ver funnelJob)
>  */
> const beholder = require('./beholder');
> const automationsRepository = require('./repositories/automationsRepository');
> const regimeStatesRepository = require('./repositories/regimeStatesRepository');
> const { getRegime } = require('./utils/regimeService');
> const { indexKeys } = require('./utils/indexes');
> const logger = require('./utils/logger');
> 
> const ENABLED = (process.env.REGIME_JOB_ENABLED || 'true') !== 'false';
> // parse defensivo: valor inválido/NaN cairia em setInterval(NaN) (loop quente). Piso de 30s
> // evita isso. Recomendado manter >= TTL do regimeService (~120s) p/ cada poll re-classificar
> // em vez de servir cache; regime de velas 1h muda devagar, default 5 min é folgado.
> const _refresh = parseInt(process.env.REGIME_REFRESH_MS || '300000', 10);
> const REFRESH_MS = Number.isFinite(_refresh) && _refresh >= 30000 ? _refresh : 300000;
> const INTERVAL = process.env.REGIME_INTERVAL || '1h';
> // Símbolo macro cuja SAÍDA do bear arma a observação da Fase 4 no funil (ver funnelJob.armFase4Observation).
> const FASE4_MACRO_SYMBOL = (process.env.FASE4_MACRO_SYMBOL || 'BTCUSDT').toUpperCase();
> 
> let timer = null;
> let running = false;       // trava de re-entrância: nunca roda dois ciclos sobrepostos
> let starting = false;      // trava de boot: cobre a janela do load assíncrono do estado antes do 1º poll
> const LAST = {};           // último regime gravado por símbolo (= valor do gate; também é o `prev`)
> const AT = {};             // timestamp (ms) da última gravação bem-sucedida por símbolo
> const STALE = new Set();   // símbolos em estado "stale" já logados (loga 1x por episódio)
> const ABOVE = {};          // último estado SMA_fast>SMA_slow por símbolo (detecta a transição do cross)
> const SMAVAL = {};         // últimos valores SMA fast/slow por símbolo (observabilidade)
> const CROSS = {};          // último cruzamento por símbolo: { dir: 'golden'|'death', at: ms }
> 
> // Símbolos a monitorar: REGIME_SYMBOLS (CSV) se setado; senão os símbolos não-wildcard das
> // automações ATIVAS (assim novos símbolos entram sozinhos). Wildcard ('*...') é ignorado — não
> // dá p/ saber o símbolo concreto sem a memoryKey; use REGIME_SYMBOLS p/ esses casos.
> async function resolveSymbols() {
>     const fromEnv = (process.env.REGIME_SYMBOLS || '').split(',').map(s => s.trim().toUpperCase()).filter(Boolean);
>     if (fromEnv.length) return [...new Set(fromEnv)];
> ===== flowJob.js (head) =====
> 'use strict';
> /*
>  * Flow Job — grava MEMORY['<sym>:FLOW'] (desequilíbrio de fluxo do TAKER da MAINNET) periodicamente.
>  *
>  * Computa e expõe o sinal (MEMORY + endpoint + MCP) e LOGA os episódios de fluxo unilateral. O JOB é
>  * passivo (escreve a MEMORY, não dispara), mas o sinal JÁ É CONSUMIDO: o `imbalance` gateia a id2
>  * ("não comprar o dip sob venda agressora AGORA" — uso de TIMING/nowcasting, que a evidência suporta).
>  * ⚠️ imbalance/toxicity são NOWCASTING, não forecast (deep-research, ~/RESEARCH-bear-capture.md): nunca
>  * usar como preditor de direção futura (VPIN/toxicidade como sinal forward foi refutado) — só timing.
>  *
>  * Escreve um OBJETO por símbolo:  MEMORY['<sym>:FLOW'] = { imbalance, toxicity, at }
>  * via updateMemory(...,executeAutomations=false) (gate PASSIVO quando ligado: lido no tick, não dispara).
>  * Sinal = MAINNET (estado real), execução = testnet — mesma arquitetura do regimeJob.
>  *
>  * Env:
>  *   FLOW_JOB_ENABLED (default 'true')   — liga/desliga o job
>  *   FLOW_REFRESH_MS  (default 30000)    — intervalo do poll (30s; piso 5s)
>  *   FLOW_SYMBOLS     (CSV, opcional)    — força a lista; senão usa os das automações ativas
>  *   FLOW_LOG_TOXICITY(default '0.6')    — loga quando |imbalance| >= isto (observação dos "quase-vetos")
>  */
> const beholder = require('./beholder');
> const automationsRepository = require('./repositories/automationsRepository');
> const { getFlow } = require('./utils/flowService');
> const { indexKeys } = require('./utils/indexes');
> const logger = require('./utils/logger');
> 
> const ENABLED = (process.env.FLOW_JOB_ENABLED || 'true') !== 'false';
> const _refresh = parseInt(process.env.FLOW_REFRESH_MS || '30000', 10);
> const REFRESH_MS = Number.isFinite(_refresh) && _refresh >= 5000 ? _refresh : 30000;
> const _tox = parseFloat(process.env.FLOW_LOG_TOXICITY || '0.6');
> const LOG_TOXICITY = Number.isFinite(_tox) ? _tox : 0.6;
> 
> let timer = null;
> let running = false;       // trava de re-entrância
> const LAST = {};           // último FLOW por símbolo (observabilidade)
> const AT = {};             // timestamp (ms) da última gravação por símbolo
> const UNAVAIL = new Set();  // símbolos indisponíveis já logados (loga 1x por episódio)
> 
> // Mesma resolução de símbolos do regimeJob: FLOW_SYMBOLS (CSV) OU os das automações ATIVAS (não-wildcard).
> async function resolveSymbols() {
>     const fromEnv = (process.env.FLOW_SYMBOLS || '').split(',').map(s => s.trim().toUpperCase()).filter(Boolean);
>     if (fromEnv.length) return [...new Set(fromEnv)];
>     try {
>         const autos = await automationsRepository.getActiveAutomations();
>         const syms = (autos || [])
>             .map(a => String((a.get ? a.get('symbol') : a.symbol) || '').toUpperCase())
>             .filter(s => s && !s.startsWith('*'));
>         return [...new Set(syms)];
>     } catch (err) {
>         logger('flow', `Falha ao resolver símbolos das automações: ${err.message}`);
>         return [];
>     }
> }
> 
> async function runOnce() {
>     if (running) return;
>     running = true;
>     try {
>         const symbols = await resolveSymbols();
>         if (!symbols.length) return;
> ===== fairPriceJob.js (head) =====
> 'use strict';
> /*
>  * Fair Price Job — grava MEMORY['<sym>:FAIR'] = { price, at, atMs } (preço de referência da MAINNET)
>  * periodicamente, p/ o Harvester de dislocação ancorar as compras-limite fundas (bestAsk testnet vs FAIR).
>  *
>  * PASSIVO (executeAutomations=false): a escrita não dispara ordem; é lida no tick das automações do harvester.
>  * Clona o padrão do flowJob/regimeJob (sinal mainnet → MEMORY → execução testnet).
>  *
>  * FAIL-SAFE de STALENESS (sem Date.now() na condition, que o validateConditions proíbe): após STALE_FAILS
>  * falhas consecutivas de fetch, escreve { price: 0, stale: true } → as conditions de compra
>  * (bestAsk < FAIR.price*0.97) viram bestAsk<0 = sempre falso → COMPRAS DESLIGADAS até o mainnet voltar.
>  * A venda no-loss NÃO usa FAIR (usa HARVEST.cost), então continua liberada p/ sair de posição.
>  *
>  * Env:
>  *   FAIR_PRICE_JOB_ENABLED (default 'true')   — liga/desliga (kill-switch)
>  *   FAIR_REFRESH_MS        (default 10000)    — intervalo do poll (10s; piso 5s)
>  *   FAIR_SYMBOLS           (default 'BTCUSDT') — CSV; senão usa os das automações ativas
>  *   FAIR_STALE_FAILS       (default 3)        — nº de falhas consecutivas antes do sentinel price:0
>  */
> const beholder = require('./beholder');
> const automationsRepository = require('./repositories/automationsRepository');
> const { getFairPrice } = require('./utils/fairPriceService');
> const { indexKeys } = require('./utils/indexes');
> const logger = require('./utils/logger');
> 
> const ENABLED = (process.env.FAIR_PRICE_JOB_ENABLED || 'true') !== 'false';
> const _refresh = parseInt(process.env.FAIR_REFRESH_MS || '10000', 10);
> const REFRESH_MS = Number.isFinite(_refresh) && _refresh >= 5000 ? _refresh : 10000;
> const _staleFails = parseInt(process.env.FAIR_STALE_FAILS || '3', 10);
> const STALE_FAILS = Number.isFinite(_staleFails) && _staleFails >= 1 ? _staleFails : 3;
> 
> let timer = null;
> let running = false;
> const LAST = {};        // último FAIR por símbolo (observabilidade)
> const AT = {};          // timestamp (ms) da última gravação
> const FAILS = {};       // falhas consecutivas de fetch por símbolo
> const STALE = new Set();// símbolos em sentinel price:0 (logados 1x por episódio)
> 
> async function resolveSymbols() {
>     const fromEnv = (process.env.FAIR_SYMBOLS || 'BTCUSDT').split(',').map(s => s.trim().toUpperCase()).filter(Boolean);
>     if (fromEnv.length) return [...new Set(fromEnv)];
>     try {
>         const autos = await automationsRepository.getActiveAutomations();
>         const syms = (autos || [])
>             .map(a => String((a.get ? a.get('symbol') : a.symbol) || '').toUpperCase())
>             .filter(s => s && !s.startsWith('*'));
>         return [...new Set(syms)];
>     } catch (err) {
>         logger('fair', `Falha ao resolver símbolos: ${err.message}`);
>         return [];
>     }
> }
> 
> async function runOnce() {
>     if (running) return;
>     running = true;
>     try {
>         const symbols = await resolveSymbols();
>         if (!symbols.length) return;
> ```

## 🤖 Claude *(18:56:01)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux/backend/src && grep -rn \"INTERVAL\\|setInterval\\|aggTrade\\|klines\\|getKlines\\|interval\\|1m\\|5m\\|15m\\|3600\\|60000\\|miniTicker\" regimeJob.js flowJob.js fairPriceJob.js utils/flowService.js utils/fairPriceService.js utils/regimeService.js 2>/dev/null",
  "description": "Find polling intervals and data source granularity in jobs/services"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> regimeJob.js:23: *  REGIME_REFRESH_MS   (default 300000)   — intervalo do poll (5 min; regime de velas 1h muda devagar)
> regimeJob.js:24: *  REGIME_INTERVAL     (default '1h')     — timeframe das velas usadas na classificação
> regimeJob.js:36:// parse defensivo: valor inválido/NaN cairia em setInterval(NaN) (loop quente). Piso de 30s
> regimeJob.js:41:const INTERVAL = process.env.REGIME_INTERVAL || '1h';
> regimeJob.js:84:                const r = await getRegime(symbol, INTERVAL, LAST[symbol]);
> regimeJob.js:142:                        const results = await beholder.updateMemory(symbol, indexKeys.TREND_CROSS, INTERVAL, dir, true);
> regimeJob.js:146:                        await beholder.updateMemory(symbol, indexKeys.TREND_CROSS, INTERVAL, 'none', false);
> regimeJob.js:207:        runOnce(); // primeira passada imediata no boot (não espera o 1º intervalo)
> regimeJob.js:208:        timer = setInterval(runOnce, REFRESH_MS);
> regimeJob.js:210:        logger('regime', `Regime job iniciado (intervalo ${REFRESH_MS}ms, klines ${INTERVAL}).`);
> regimeJob.js:237:    return { enabled: ENABLED, refreshMs: REFRESH_MS, interval: INTERVAL, running, symbols };
> flowJob.js:17: *   FLOW_REFRESH_MS  (default 30000)    — intervalo do poll (30s; piso 5s)
> flowJob.js:83:                // gatilho técnico da id2 (RSI 1m < 25). Esparso (só em sobrevenda) → I/O baixo; vai p/
> flowJob.js:86:                // então calibra a MECÂNICA/distribuição, NÃO alfa real (p/ isso falta histórico de aggTrades no
> flowJob.js:89:                    const rsi = beholder.getMemory(symbol, 'RSI_14_1m');
> flowJob.js:111:    timer = setInterval(runOnce, REFRESH_MS);
> flowJob.js:113:    logger('flow', `Flow job iniciado SHADOW (intervalo ${REFRESH_MS}ms; log de toxicidade >= ${LOG_TOXICITY}). Ainda NÃO gateia automação.`);
> utils/regimeService.js:13: *   sem klines  -> { ..., regime: 'unknown', unavailable: true }   (endpoint mapeia p/ 502; job preserva MEMORY)
> utils/regimeService.js:42:// re-buscar klines. INDISPONÍVEL (sem klines) não cacheia → re-tenta no próximo ciclo. INSUFICIENTE
> utils/regimeService.js:44:async function getRegime(symbol, interval = '1h', prev = null) {
> utils/regimeService.js:45:    const key = `${symbol}:${interval}`;
> utils/regimeService.js:54:            const r = await getJSON(host, `/api/v3/klines?symbol=${symbol}&interval=${interval}&limit=${BARS}`).catch(() => null);
> utils/regimeService.js:61:            return { symbol, interval, candles: 0, source: null, regime: 'unknown', strategy: 'hold', unavailable: true, reason: 'klines indisponiveis na Binance', signals: {} };
> utils/regimeService.js:66:        return { symbol, interval, candles: candles.length, source: used, regime: 'unknown', strategy: 'hold', insufficient: true, reason: `dados insuficientes (${candles.length} velas; precisa >= ${MIN_BARS})`, signals: {} };
> utils/regimeService.js:71:    return { symbol, interval, candles: candles.length, source: used, cached: fromCache, sma: smaCross(candles), ...classifyRegime(candles, {}, prev) };
> utils/flowService.js:5: * Busca os aggTrades recentes da MAINNET (estado real, independente do testnet sintético) e mede
> utils/flowService.js:10: * Métricas (sobre os últimos LIMIT aggTrades):
> utils/flowService.js:32:const LIMIT = 1000;   // últimos N aggTrades (janela de fluxo; BTCUSDT ~dezenas de segundos)
> utils/flowService.js:52:        const r = await getJSON(host, `/api/v3/aggTrades?symbol=${symbol}&limit=${LIMIT}`).catch(() => null);
> utils/flowService.js:56:        return { symbol, source: null, unavailable: true, reason: 'aggTrades indisponiveis na Binance' };
> fairPriceJob.js:16: *   FAIR_REFRESH_MS        (default 10000)    — intervalo do poll (10s; piso 5s)
> fairPriceJob.js:91:    timer = setInterval(runOnce, REFRESH_MS);
> fairPriceJob.js:93:    logger('fair', `Fair Price job iniciado (intervalo ${REFRESH_MS}ms; sentinel após ${STALE_FAILS} falhas).`);
> ```

## 🤖 Claude *(18:56:09)*

I now have the full picture of the 1-minute data plumbing. Let me confirm the chart stream completeness behavior (the `INCOMPLETE_CANDLES` flag governs whether the BRAIN reacts intra-candle or only on candle close) and check the flowService metrics definition.

## 🤖 Claude *(18:56:09)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/src/utils/flowService.js",
  "limit": 75
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	'use strict';
> 2	/*
> 3	 * Serviço de fluxo de ordens (taker flow) — fonte ÚNICA do desequilíbrio de agressão do mercado.
> 4	 *
> 5	 * Busca os aggTrades recentes da MAINNET (estado real, independente do testnet sintético) e mede
> 6	 * a pressão líquida do TAKER usando o campo `m` (isBuyerMaker) — o ground-truth do agressor:
> 7	 *   m === false  -> comprador é TAKER  -> COMPRA agressora  (acumula buyVol)
> 8	 *   m === true   -> comprador é MAKER  -> VENDA agressora    (acumula sellVol)
> 9	 *
> 10	 * Métricas (sobre os últimos LIMIT aggTrades):
> 11	 *   imbalance = (buyVol - sellVol) / (buyVol + sellVol)   ∈ [-1, 1]   (<0 = taker vendendo)
> 12	 *   toxicity  = |imbalance|                                ∈ [0, 1]    (one-sidedness CONTEMPORÂNEA do fluxo)
> 13	 *
> 14	 * ⚠️ NOWCASTING, não forecasting (deep-research 2026-06-08, ~/RESEARCH-bear-capture.md): order-flow/OFI
> 15	 * descreve o movimento IMEDIATO (~2 price changes / ~10s), NÃO prevê direção futura — e VPIN/toxicidade
> 16	 * como preditor de jumps foi REFUTADO. Usar imbalance/toxicity SÓ como TIMING de execução (ex.: "não
> 17	 * comprar o dip ENQUANTO o taker vende agressivo AGORA"), JAMAIS como forecast direcional autônomo.
> 18	 *
> 19	 * É um proxy de fluxo/toxicidade (NÃO o True VPIN bucketizado com CDF de 30d — ver docs/blueprint;
> 20	 * isto é o v1 ancorado: 1 endpoint REST, sem futures/L2, real mesmo no spot). Consumido por:
> 21	 *   - analysisController.getFlow   (GET /analysis/flow/:symbol — UI/observabilidade + MCP)
> 22	 *   - flowJob                      (job periódico que grava MEMORY['<sym>:FLOW'] — SHADOW, sem gate ainda)
> 23	 *
> 24	 * NUNCA lança: sempre retorna objeto. `unavailable:true` se a Binance não responder (chamador preserva).
> 25	 */
> 26	const https = require('https');
> 27	
> 28	// Só mercado GLOBAL (mesma razão do regimeService: Binance.US tem preços/universo divergentes).
> 29	const HOSTS = ['api.binance.com', 'data-api.binance.vision'];
> 30	const CACHE = new Map();
> 31	const TTL = 20e3;     // 20s (trades mudam rápido; o job poda ~30s, o endpoint compartilha o cache)
> 32	const LIMIT = 1000;   // últimos N aggTrades (janela de fluxo; BTCUSDT ~dezenas de segundos)
> 33	
> 34	function getJSON(host, path) {
> 35	    return new Promise((resolve, reject) => {
> 36	        const req = https.get({ host, path, headers: { 'User-Agent': 'tradeux' }, timeout: 8000 }, r => {
> 37	            let d = '';
> 38	            r.on('data', c => d += c);
> 39	            r.on('end', () => { try { resolve({ status: r.statusCode, body: JSON.parse(d) }); } catch (e) { resolve({ status: r.statusCode, body: null }); } });
> 40	        });
> 41	        req.on('error', reject);
> 42	        req.on('timeout', () => { req.destroy(); reject(new Error('timeout')); });
> 43	    });
> 44	}
> 45	
> 46	async function getFlow(symbol) {
> 47	    const cached = CACHE.get(symbol);
> 48	    if (cached && Date.now() - cached.t < TTL) return { ...cached.data, cached: true };
> 49	
> 50	    let trades = null, used = null;
> 51	    for (const host of HOSTS) {
> 52	        const r = await getJSON(host, `/api/v3/aggTrades?symbol=${symbol}&limit=${LIMIT}`).catch(() => null);
> 53	        if (r && r.status === 200 && Array.isArray(r.body) && r.body.length > 0) { trades = r.body; used = host; break; }
> 54	    }
> 55	    if (!trades)
> 56	        return { symbol, source: null, unavailable: true, reason: 'aggTrades indisponiveis na Binance' };
> 57	
> 58	    let buyVol = 0, sellVol = 0;
> 59	    for (const t of trades) {
> 60	        const q = parseFloat(t.q);
> 61	        if (!Number.isFinite(q)) continue;
> 62	        if (t.m) sellVol += q; else buyVol += q; // m=true => venda agressora; m=false => compra agressora
> 63	    }
> 64	    const tot = buyVol + sellVol;
> 65	    const imbalance = tot > 0 ? (buyVol - sellVol) / tot : 0;
> 66	    const first = trades[0], last = trades[trades.length - 1];
> 67	
> 68	    const data = {
> 69	        symbol, source: used, cached: false,
> 70	        imbalance: +imbalance.toFixed(4),            // [-1,1]: <0 = taker líquido vendendo
> 71	        toxicity: +Math.abs(imbalance).toFixed(4),   // [0,1]: quão unilateral está o fluxo
> 72	        buyVol: +buyVol.toFixed(8), sellVol: +sellVol.toFixed(8),
> 73	        trades: trades.length,
> 74	        spanSec: (first && last && last.T && first.T) ? Math.round((last.T - first.T) / 1000) : 0,
> 75	        at: new Date().toISOString(),
> ```

## 🤖 Claude *(18:56:12)*

I have everything needed to map the complete 1-minute data plumbing. Let me record the structured findings.

## 🤖 Claude *(18:57:30)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "area": "Encanamento de dados de 1 minuto (streams, MEMORY indexes, indicadores e granularidade do BRAIN) no backend TradeUX/Beholder",
  "summary": "O backend \u00e9 um engine Beholder stateful: app-em.js assina streams da Binance via utils/exchange.js (wrapper node-binance-api 1.x) e alimenta um dicion\u00e1rio em mem\u00f3ria MEMORY[`<sym>:<INDEX>`] dentro de beholder.js. Em cada tick, beholder.updateMemory escreve a chave e dispara testAutomations, que avalia conditions compiladas (`Function(\"MEMORY\", ...)`) das automa\u00e7\u00f5es indexadas por aquela memoryKey. Os indicadores t\u00e9cnicos (RSI/SMA/BB/ATR/MACD/etc.) s\u00e3o calculados em utils/indexes.js a partir das klines do chartStream, no timeframe configurado por monitor (tipicamente 1m). O book N\u00c3O \u00e9 real/profundo: o monitor BOOK fica inativo por padr\u00e3o e o BOOK \u00e9 SIMULADO a partir do miniTicker (bestAsk=bestBid=close). Sinais de mercado real (REGIME, FLOW/aggTrades, FAIR) N\u00c3O v\u00eam de stream de 1m: s\u00e3o jobs REST peri\u00f3dicos contra a MAINNET (5min/30s/10s) que gravam a MEMORY de forma passiva. O BRAIN reage por EVENTO de tick (n\u00e3o por rel\u00f3gio de 1m): a cada vela 1m fechada para as klines, a cada update do miniTicker (sub-segundo) para BOOK/MINI_TICKER.",
  "keyFiles": [
    {
      "path": "/home/gcrux-tradeux/tradeux/backend/src/app-em.js",
      "role": "Event monitor: inicia os monitores (miniTicker, book, userData, candles/chart, ticker), converte cada tick e chama beholder.updateMemory; processChartData calcula os indicadores 1m por vela e dispara testAutomations"
    },
    {
      "path": "/home/gcrux-tradeux/tradeux/backend/src/beholder.js",
      "role": "Engine em mem\u00f3ria: MEMORY (estado por s\u00edmbolo/index) + BRAIN (automa\u00e7\u00f5es indexadas); updateMemory/testAutomations/evalDecision avaliam as conditions; calcQty l\u00ea os buckets (TREND_QTY/HARVEST/FARM_DCA/etc.)"
    },
    {
      "path": "/home/gcrux-tradeux/tradeux/backend/src/utils/indexes.js",
      "role": "indexKeys (cat\u00e1logo de chaves de MEMORY) + execCalc/fun\u00e7\u00f5es de indicador (RSI/SMA/EMA/BB/ATR/MACD/ADX/VWAP/Stoch/patterns) sobre o array OHLC da vela"
    },
    {
      "path": "/home/gcrux-tradeux/tradeux/backend/src/utils/exchange.js",
      "role": "Fronteira Binance: chartStream (klines), miniTickerStream, bookStream(!bookTicker, inativo), tickerStream(prevDay), userDataStream; INCOMPLETE_CANDLES controla rea\u00e7\u00e3o intra-vela vs vela-fechada; riskGuard (TRADING_HALT/MAX_ORDER_NOTIONAL_USDT)"
    },
    {
      "path": "/home/gcrux-tradeux/tradeux/backend/src/regimeJob.js",
      "role": "Poll REST mainnet de klines 1h a cada 5min \u2192 MEMORY['<sym>:REGIME'] (string) e TREND_CROSS; gate PASSIVO (executeAutomations=false)"
    },
    {
      "path": "/home/gcrux-tradeux/tradeux/backend/src/flowJob.js",
      "role": "Poll REST mainnet de aggTrades a cada 30s \u2192 MEMORY['<sym>:FLOW']={imbalance,toxicity}; nowcasting/timing, gateia id2 (RSI 1m<25)"
    },
    {
      "path": "/home/gcrux-tradeux/tradeux/backend/src/utils/flowService.js",
      "role": "getFlow: busca \u00faltimos 1000 aggTrades mainnet, deriva imbalance/toxicity pelo campo m (isBuyerMaker); TTL 20s; janela ~dezenas de segundos para BTCUSDT"
    },
    {
      "path": "/home/gcrux-tradeux/tradeux/backend/src/fairPriceJob.js",
      "role": "Poll REST mainnet a cada 10s \u2192 MEMORY['<sym>:FAIR']={price,at,atMs}; \u00e2ncora do Harvester; sentinel price:0 ap\u00f3s 3 falhas (compras off)"
    }
  ],
  "facts": [
    "STREAMS DE WEBSOCKET assinados em app-em.js via exchange.js: (1) miniTickerStream \u2192 !miniTicker all-symbols (exchange.js:189-193); (2) bookStream \u2192 stream cru !bookTicker (exchange.js:198-209), por\u00e9m o monitor BOOK fica INATIVO por padr\u00e3o (coment\u00e1rio exchange.js:195-196); (3) chartStream(symbol, interval||'1m') \u2192 klines/@kline_<interval> (app-em.js:623, exchange.js:211-225); (4) tickerStream \u2192 @ticker prevDay 24h (exchange.js:249-255); (5) userDataStream \u2192 executionReport/balanceUpdate/listStatus (exchange.js:240-247).",
    "CAD\u00caNCIA dos streams: miniTicker da Binance emite ~1x/segundo (all-symbols); !bookTicker emite a cada mudan\u00e7a de topo de livro (sub-segundo) mas est\u00e1 desligado; klines @kline_1m emitem a cada ~1-2s ENQUANTO a vela est\u00e1 aberta e um evento final no fechamento da vela (a cada 60s).",
    "GRANULARIDADE EFETIVA da vela 1m \u00e9 controlada por INCOMPLETE_CANDLES (exchange.js:215-216): se a env N\u00c3O est\u00e1 setada ou \u00e9 'false' (default), chartStream DESCARTA os ticks de vela incompleta (isFinal===false) e s\u00f3 repassa no FECHAMENTO da vela \u2192 o BRAIN reage 1x por vela de 1m fechada. Se INCOMPLETE_CANDLES='true', reage a cada tick intra-vela.",
    "INDICADORES 1m: app-em.processChartData (app-em.js:591-617) recebe o array OHLC completo da vela e, para cada index configurado no monitor (string CSV tipo 'RSI_14,SMA_50'), chama execCalc(indexName, ohlc, ...params) e grava MEMORY['<sym>:<INDEX>_<interval>'] = {current, previous} via updateMemory(...,false). RSI/SMA/EMA/BB/ATR/MACD/ADX/STOCH/VWAP/Williams%R/PSAR/CCI/MFI/OBV + ~40 padr\u00f5es de candle est\u00e3o TODOS implementados em indexes.js (execCalc switch, linhas 153-218); c\u00e1lculo via lib 'technicalindicators'.",
    "Os par\u00e2metros do indicador v\u00eam do NOME do index: o monitor armazena indexes como CSV e processChartData faz index.split('_') \u2192 indexName + params (ex.: 'RSI_14_1m' \u2192 RSI per\u00edodo 14 no intervalo 1m; 'BB_20_2' \u2192 Bollinger 20/2; 'ATR_14'). Defaults em indexes.js: RSI=14, SMA=10, EMA=10, BB=20/2, ATR=14, MACD=12/26/9. Cada calc retorna {current, previous} (pen\u00faltima vela) e devolve {current:false} se faltam velas (ex.: RSI exige close.length>period).",
    "MEMORY INDEXES por s\u00edmbolo (cat\u00e1logo em indexKeys, indexes.js:3-84) que existem em runtime: MINI_TICKER (objeto float do miniTicker, escrito em app-em.js:31), BOOK ({current,previous}={bestAsk,bestBid}), WALLET (saldo dispon\u00edvel por moeda), LAST_ORDER, LAST_CANDLE/PREVIOUS_CANDLE (por interval, {current,previous} OHLC), TICKER (24h prevDay), e os por-job: REGIME (string), TREND_CROSS (string golden/death/none por interval), TREND_QTY, FLOW ({imbalance,toxicity,at}), FAIR ({price,at,atMs}), HARVEST ({qty,cost}), HARVEST_SELLING (trava), FARM_DCA ({qty,cost}). Os INDICADORES viram chaves '<sym>:<INDEX>_<interval>' (ex.: BTCUSDT:RSI_14_1m).",
    "BOOK \u00c9 SIMULADO, n\u00e3o profundidade real: em app-em.js:37-55 cada miniTicker gera book={symbol, bestAsk:close, bestBid:close} (bestAsk==bestBid==close, sem spread nem qty/n\u00edveis). beholder.calcPrice usa MEMORY['<sym>:BOOK'].current.bestAsk/bestBid para ordens MARKET (beholder.js:189-194) e as grids/trailing tamb\u00e9m (beholder.js:556,646,731). N\u00e3o h\u00e1 L2/depth/order-book real em lugar nenhum; bookStream(!bookTicker) daria s\u00f3 o TOPO do livro (best bid/ask + qty) e est\u00e1 desativado.",
    "O BRAIN reage por EVENTO de memoryKey, n\u00e3o por rel\u00f3gio fixo de 1m: beholder.updateMemory(...,executeAutomations=true) chama testAutomations(memoryKey), que busca via BRAIN_INDEX as automa\u00e7\u00f5es cujo `indexes` cont\u00e9m aquela chave e roda evalDecision (beholder.js:812-858). Automa\u00e7\u00f5es com \u00edndice de vela (LAST_CANDLE/RSI/SMA) disparam no fechamento da vela 1m; com \u00edndice MINI_TICKER/BOOK disparam a cada tick sub-segundo do miniTicker.",
    "SINAIS DE MERCADO REAL N\u00c3O s\u00e3o stream-1m, s\u00e3o JOBS REST contra a MAINNET com cad\u00eancia pr\u00f3pria, todos PASSIVOS (updateMemory executeAutomations=false \u2014 escrevem a MEMORY mas N\u00c3O disparam ordem; s\u00e3o lidos quando o tick de pre\u00e7o dispara a automa\u00e7\u00e3o): regimeJob klines 1h a cada REGIME_REFRESH_MS=300000 (5min) \u2192 REGIME + TREND_CROSS (regimeJob.js:38-41,84,142,208); flowJob aggTrades a cada FLOW_REFRESH_MS=30000 (30s) \u2192 FLOW (flowJob.js:24-25,111); fairPriceJob a cada FAIR_REFRESH_MS=10000 (10s) \u2192 FAIR (fairPriceJob.js:25-26,91).",
    "FLOW \u00e9 nowcasting de fluxo do taker (flowService.js): pega os \u00faltimos LIMIT=1000 aggTrades da mainnet (janela ~dezenas de segundos para BTCUSDT), classifica agressor pelo campo m (m=false\u2192compra agressora, m=true\u2192venda), calcula imbalance=(buyVol-sellVol)/(buyVol+sellVol)\u2208[-1,1] e toxicity=|imbalance|. Coment\u00e1rios (flowService.js:14-17) marcam explicitamente como TIMING/nowcasting, N\u00c3O forecast direcional (VPIN refutado). imbalance gateia a id2 (comprar dip s\u00f3 quando RSI 1m<25 e taker n\u00e3o est\u00e1 vendendo agressivo \u2014 flowJob.js:83-89).",
    "O caminho QUENTE \u00e9 guardado por LOCK_MEMORY e LOCK_BRAIN (beholder.js): updateMemory ignora escritas se LOCK_MEMORY; testAutomations trava as automa\u00e7\u00f5es disparadas por INTERVAL (AUTOMATION_INTERVAL, env) ms ap\u00f3s executarem, prevenindo re-disparo no mesmo movimento. processExecutionData (fills) tem delay deliberado de 3000ms (app-em.js:506); listStatus/OCO 4000ms.",
    "Toda ordem real passa por um chokepoint \u00fanico de risco em exchange.js: assertWithinRisk (linhas 23-40) checa TRADING_HALT (kill-switch, bloqueia tudo) e MAX_ORDER_NOTIONAL_USDT (teto por ordem). ATEN\u00c7\u00c3O: vendas MARKET por quantidade-base sem price (TREND_QTY/HARVEST_QTY/MAX_WALLET) PASSAM sem avaliar o teto de notional \u2014 s\u00f3 o HALT as cobre (coment\u00e1rio exchange.js:13-17)."
  ],
  "gapsOrRisks": [
    "N\u00c3O h\u00e1 profundidade de livro real: BOOK \u00e9 sint\u00e9tico (bestAsk=bestBid=close do miniTicker), sem spread, sem tamanho nos n\u00edveis, sem L2. Qualquer estrat\u00e9gia de microestrutura (imbalance de livro, spread capture, queue position, slippage estimate) est\u00e1 BLOQUEADA com o plumbing atual. O !bookTicker (topo do livro real com qty) existe no c\u00f3digo mas o monitor BOOK est\u00e1 desligado por padr\u00e3o.",
    "A rea\u00e7\u00e3o a cada vela 1m s\u00f3 ocorre no FECHAMENTO da vela quando INCOMPLETE_CANDLES \u00e9 false (default): h\u00e1 lat\u00eancia de at\u00e9 ~60s entre o movimento de pre\u00e7o e o disparo de uma automa\u00e7\u00e3o baseada em RSI/SMA/BB/ATR 1m. Para timing intra-vela, ou se liga INCOMPLETE_CANDLES='true' (recalcula o indicador a cada tick parcial, mais ru\u00eddo/CPU) ou se usa MINI_TICKER/BOOK (que tickam sub-segundo mas n\u00e3o t\u00eam indicador t\u00e9cnico associado).",
    "FLOW/REGIME/FAIR t\u00eam cad\u00eancia REST grosseira (30s/5min/10s) e s\u00e3o da MAINNET, descolados do pre\u00e7o de execu\u00e7\u00e3o (testnet sint\u00e9tico). Para decis\u00f5es a cada vela de 1m, FLOW (30s) pode estar at\u00e9 ~30s defasado e REGIME (5min) \u00e9 praticamente est\u00e1tico na escala de 1m \u2014 servem de GATE/contexto, n\u00e3o de gatilho fino.",
    "Os indicadores s\u00e3o calculados sobre a janela de klines que o node-binance-api mant\u00e9m em mem\u00f3ria do chartStream; n\u00e3o vi (nestes arquivos) o tamanho do buffer de klines nem um backfill REST inicial \u2014 se o buffer for curto, indicadores de per\u00edodo longo (SMA_200, BB_20) podem retornar {current:false} por muitas velas ap\u00f3s o boot at\u00e9 acumular hist\u00f3rico suficiente.",
    "fee-awareness N\u00c3O est\u00e1 no plumbing de dados: n\u00e3o h\u00e1 \u00edndice de MEMORY com fee/comiss\u00e3o por s\u00edmbolo; o net/commission s\u00f3 aparece POST-fill em processExecutionData (app-em.js:470-476) e nos buckets de custo (HARVEST.cost, FARM_DCA.cost). Uma estrat\u00e9gia fee-aware a cada vela 1m precisaria injetar a taxa (ex.: 0.1%/0.075%) na pr\u00f3pria condition/c\u00e1lculo de alvo \u2014 hoje isso vive s\u00f3 nos multiplicadores dos orderTemplates, n\u00e3o num \u00edndice consult\u00e1vel."
  ],
  "oneMinuteRelevance": "HABILITA: estrat\u00e9gia em vela de 1m fee-aware \u00e9 vi\u00e1vel usando o chartStream 1m \u2192 indicadores prontos (RSI_14_1m, SMA, EMA, BB_20_2, ATR_14, MACD) j\u00e1 calculados por vela em MEMORY como {current,previous}, com o BRAIN disparando 1x por vela fechada (sinal limpo, sem ru\u00eddo intra-vela, default INCOMPLETE_CANDLES=false). O MINI_TICKER d\u00e1 pre\u00e7o ~1Hz para gatilhos de n\u00edvel e o FLOW (imbalance/toxicity, 30s) e REGIME (5min) servem de GATE de contexto (n\u00e3o comprar dip sob venda agressora / fora de bear). ATR_14_1m est\u00e1 dispon\u00edvel para dimensionar stop/alvo proporcional \u00e0 volatilidade \u2014 chave para uma estrat\u00e9gia fee-aware (alvo > 2\u00d7fee + ru\u00eddo). BLOQUEIA/limita: (1) sem book real/profundidade, nada de microestrutura, spread capture ou estimativa de slippage \u2014 o BOOK simulado for\u00e7a execu\u00e7\u00e3o essencialmente a 'close'; (2) sem \u00edndice de fee na MEMORY, a consci\u00eancia de taxa precisa ser codada na condition/multiplicador, n\u00e3o consultada; (3) FLOW a 30s e REGIME a 5min s\u00e3o contexto grosseiro, n\u00e3o gatilho de 1m; (4) se a estrat\u00e9gia exigir rea\u00e7\u00e3o intra-vela (<60s) baseada em indicador, \u00e9 preciso ligar INCOMPLETE_CANDLES (mais CPU/ru\u00eddo) ou apoiar-se no MINI_TICKER. Recomenda-se ancorar a estrat\u00e9gia em indicadores 1m + ATR para sizing + FLOW/REGIME como filtros, ciente de que alvos precisam superar fees (~0.1%) j\u00e1 que n\u00e3o h\u00e1 otimiza\u00e7\u00e3o de execu\u00e7\u00e3o via livro."
}
```

> **Tool Result (StructuredOutput)** - ✅ Success
>
> ```
> Structured output provided successfully
> ```

## 🤖 Claude *(18:57:42)*

Mapeei o encanamento de dados de 1 minuto. Resumo entregue via StructuredOutput.

Pontos-chave:

- **Streams (app-em.js + exchange.js):** `chartStream` (klines `@kline_1m`), `miniTicker` (~1 Hz, all-symbols), `tickerStream` (24h), `userDataStream` (fills/saldo/OCO). O `bookStream` (`!bookTicker`) existe mas o monitor BOOK está **desligado por padrão**.
- **MEMORY indexes por símbolo:** MINI_TICKER, BOOK (simulado), WALLET, LAST_ORDER, LAST_CANDLE/PREVIOUS_CANDLE, TICKER, mais os de job — REGIME, TREND_CROSS, TREND_QTY, FLOW, FAIR, HARVEST, HARVEST_SELLING, FARM_DCA. Os indicadores viram chaves `<sym>:<INDEX>_<interval>` (ex.: `BTCUSDT:RSI_14_1m`).
- **Indicadores 1m:** RSI/SMA/EMA/BB/ATR/MACD/ADX/STOCH/VWAP/etc. todos calculados por vela em `utils/indexes.js` (lib `technicalindicators`), retornando `{current, previous}`, parametrizados pelo nome do índice.
- **Granularidade do BRAIN:** reage por evento de memoryKey, não por relógio. Com `INCOMPLETE_CANDLES=false` (default) a vela 1m só dispara no **fechamento** (~60s de latência); MINI_TICKER/BOOK tickam sub-segundo mas sem indicador técnico.
- **Book real vs simulado:** **simulado** — `bestAsk=bestBid=close` do miniTicker, sem profundidade/spread/L2. Microestrutura está bloqueada.
- **Sinais de mercado real:** jobs REST contra a MAINNET, passivos — REGIME (klines 1h, 5min), FLOW/aggTrades (30s), FAIR (10s). Servem de **gate/contexto**, não de gatilho fino de 1m.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-15 - agent-ab9c6a8afdcc7f52e]]
> * **Próxima Sessão**: [[2026-06-15 - agent-abbb39f05cfe295a3]]
%% --- TIMELINE END --- %%

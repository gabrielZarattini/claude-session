# Session agent-a0abbdbc6ebf37bc9
**Date:** 2026-06-22 | **Session ID:** `agent-a0abbdbc6ebf37bc9`

---

## 👤 User *(14:08:37)*

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
Verifique este achado da dimensao "security-secrets" contra o codigo REAL (Read/Grep/Bash em /home/gcrux-tradeux/tradeux). TENTE REFUTAR: e problema REAL ou falso-positivo? Confirme/corrija a location (file:line), reproduza a logica no codigo, e de o veredito honesto + severidade FINAL. Default CETICO: se nao conseguir confirmar com evidencia concreta no codigo, confirmed=false. Se confirmar, ajuste a severidade pra realidade (um "qty bruta" que o calcQty mitiga pode ser MEDIUM/LOW, nao HIGH).

ACHADO:
{
 "title": "OK / verificado limpo: hardening de .env, ausencia de HTTP cru no agente, riskState fail-closed, withdraw nao exposto no MCP",
 "severity": "INFO",
 "location": "backend/src/riskState.js:66-88 + tradeux-agent/src/agent.js + tradeux-mcp/src/index.js",
 "description": "Verifiquei e estao OK: (1) .env, tradeux-agent/.env e tradeux-mcp/.env sao 0600 do gcrux-tradeux, gitignored e NAO trackeados no git (git ls-files sem .env). (2) O agente LLM so age via tools MCP — agent.js/mcpClient.js nao tem fetch/axios/HTTP cru, entao o MODELO nao consegue, hoje, chamar POST /system/floor, /exchange/withdraw nem PATCH /settings diretamente. (3) riskState e fail-closed (disco ilegivel -> floor LIGADO; isHalted lanca -> guard bloqueia) e o env-hard TRADING_HALT_HARD nao e flipavel em runtime. (4) O MCP nao registra nenhuma write tool pra /system, /exchange/withdraw ou /settings. (5) crypto.js valida AES_KEY=32 bytes no load (throw se != 32). Ressalva: mcpClient.js:21 passa env:{...process.env} pro filho MCP, herdando TRADEUX_PASSWORD/keys.",
 "impact": "Confirma que os achados HIGH de withdraw/HALT/useTestnet NAO sao exploraveis HOJE por prompt-injection no LLM (falta um vetor de HTTP cru), reduzindo o risco IMEDIATO a um vetor de codigo/credencial — mas continuam sendo falhas de design de defesa-em-profundidade que viram criticas na primeira regressao (novo tool, UI, JWT vazado). Nenhuma acao corretiva necessaria nos itens marcados OK; servem de baseline do que ja esta seguro.",
 "isKnownHigh": false
}

## 🤖 Claude *(14:08:39)*

Vou verificar este achado contra o código real. Começo lendo o contexto e os arquivos-chave citados.

## 🤖 Claude *(14:08:40)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/HANDOFF.md"
}
```

## 🤖 Claude *(14:08:40)*


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

## 🤖 Claude *(14:08:44)*

Este achado é um "OK / verificado limpo" (severidade INFO) afirmando que 5 itens de segurança estão corretos. Meu trabalho é verificar adversarialmente cada afirmação contra o código real. Vou checar cada uma das 5 afirmações + a ressalva.

## 🤖 Claude *(14:08:46)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' ls-files | grep -E '\\.env' ; echo \"---gitignore---\"; grep -n '\\.env' .gitignore tradeux-agent/.gitignore tradeux-mcp/.gitignore 2>/dev/null; echo \"---perms---\"; ls -la .env tradeux-agent/.env tradeux-mcp/.env 2>&1",
  "description": "Check .env tracking, gitignore, and permissions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> .env.example
> backend/.env.example
> frontend/.env.example
> tradeux-agent/.env.example
> tradeux-mcp/.env.example
> ---gitignore---
> .gitignore:71:.env
> .gitignore:72:.env.test
> tradeux-agent/.gitignore:2:.env
> tradeux-mcp/.gitignore:2:.env
> ---perms---
> -rw------- 1 gcrux-tradeux gcrux-tradeux 3068 Jun 22 00:18 .env
> -rw------- 1 gcrux-tradeux gcrux-tradeux  691 Jun  8 17:31 tradeux-agent/.env
> -rw------- 1 gcrux-tradeux gcrux-tradeux  138 Jun  2 22:46 tradeux-mcp/.env
> ```

## 🤖 Claude *(14:08:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && echo \"=== agent.js HTTP raw? ===\"; grep -nE \"require\\(['\\\"](axios|node-fetch|got|http|https|undici)['\\\"]\\)|fetch\\(|axios\\.|https?\\.request|https?\\.get\\(\" tradeux-agent/src/*.js 2>/dev/null; echo \"=== files in agent/src ===\"; ls tradeux-agent/src/",
  "description": "Search for raw HTTP usage in agent source"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === agent.js HTTP raw? ===
> === files in agent/src ===
> agent.js
> index.js
> journal.js
> mcpClient.js
> notifyDedup.js
> providers
> ```

## 🤖 Claude *(14:08:56)*

Item (1) confirmado: os 3 `.env` são 0600 do gcrux-tradeux, gitignored, e não trackeados (só `.env.example`). Item (2) parcialmente confirmado: nenhum HTTP cru em agent.js/mcpClient.js. Mas preciso verificar os `providers/` (que fazem chamadas ao LLM — esperado terem HTTP) e confirmar que o agente realmente só age via tools MCP. Vou verificar os providers e o registro de tools no MCP.

## 🤖 Claude *(14:08:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && echo \"=== providers/ files ===\"; ls tradeux-agent/src/providers/; echo \"=== HTTP in providers (esperado: LLM API) ===\"; grep -rnE \"require\\(['\\\"](axios|node-fetch|got|http|https|undici)['\\\"]\\)|fetch\\(|\\.post\\(|\\.get\\(|baseURL|api\\.openrouter|api\\.anthropic\" tradeux-agent/src/providers/ 2>/dev/null",
  "description": "Inspect providers for HTTP endpoints"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === providers/ files ===
> anthropic.js
> index.js
> openrouter.js
> === HTTP in providers (esperado: LLM API) ===
> tradeux-agent/src/providers/openrouter.js:43:  const res = await fetch(`${BASE}/chat/completions`, {
> ```

## 🤖 Claude *(14:08:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && echo \"=== MCP tools registered (names) ===\"; grep -nE \"name:\\s*['\\\"]tradeux_|registerTool|server\\.tool|addTool|'tradeux_\" tradeux-mcp/src/index.js | head -80",
  "description": "List MCP registered tool names"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === MCP tools registered (names) ===
> 74:  server.tool(name, description, schema, async (args) => {
> 86:  server.tool(name, guarded, schema, async (args) => {
> ```

## 🤖 Claude *(14:09:08)*

The providers do use HTTP, but only to the LLM API endpoint (openrouter `chat/completions`) — that's expected and is NOT a path to the backend. Item (2)'s claim is that the model can't call backend HTTP endpoints directly; the only `fetch` is to the LLM, so the claim holds. Now let me look at how MCP tools are registered (the helpers at lines 74/86) and grep for the actual tool definitions to verify items (4) — no write tools for /system, /exchange/withdraw, /settings.

## 🤖 Claude *(14:09:14)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && echo \"=== how tools are defined (tool/regTool calls) ===\"; grep -nE \"^\\s*(tool|regTool|writeTool|readTool|reg)\\(|defineTool|tools\\.push|^const tools|register\\(\" tradeux-mcp/src/index.js | head -60; echo; echo \"=== grep for endpoint refs: system/withdraw/settings/floor/halt ===\"; grep -niE \"withdraw|/system|/settings|floor|/halt|place_order|cancel|start_automation|stop_automation\" tradeux-mcp/src/index.js | head -60",
  "description": "Find tool definitions and sensitive endpoint references in MCP index"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === how tools are defined (tool/regTool calls) ===
> 104:readTool(
> 111:readTool(
> 118:readTool(
> 125:readTool(
> 132:readTool(
> 139:readTool(
> 146:readTool(
> 158:readTool(
> 169:readTool(
> 186:readTool(
> 193:readTool(
> 200:readTool(
> 207:readTool(
> 214:readTool(
> 227:readTool(
> 237:readTool(
> 244:readTool(
> 257:readTool(
> 264:readTool(
> 271:readTool(
> 278:readTool(
> 337:writeTool(
> 377:writeTool(
> 387:writeTool(
> 398:writeTool(
> 405:writeTool(
> 412:writeTool(
> 419:writeTool(
> 426:writeTool(
> 439:readTool(
> 
> === grep for endpoint refs: system/withdraw/settings/floor/halt ===
> 108:  () => api.get("/settings")
> 338:  "tradeux_place_order",
> 378:  "tradeux_cancel_order",
> 379:  "Cancela uma ordem aberta na Binance.",
> 399:  "tradeux_start_automation",
> 406:  "tradeux_stop_automation",
> ```

## 🤖 Claude *(14:09:17)*

Now I can see the structure. Read tools start around line 104, write tools at 337+. Notably line 108 `api.get("/settings")` is a READ tool (GET only). Let me read the full write-tool block (337-450) to confirm there's NO write tool hitting `/system`, `/exchange/withdraw`, `PATCH /settings`, or `POST /system/floor|halt`.

## 🤖 Claude *(14:09:18)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/tradeux-mcp/src/index.js",
  "offset": 320,
  "limit": 160
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 320	// Sobre EXIGIR automationId nas ordens do agente (defesa vs. execução paralela às automações):
> 321	// NÃO se aplica como obrigatoriedade. O agente é, por design, um operador MANUAL/ad-hoc — suas
> 322	// ordens são legitimamente "manuais" (automationId ausente), iguais às do painel. O backend já
> 323	// distingue a origem: ordens de automação carregam o seu automationId (agrupadas por automação
> 324	// nos relatórios); as manuais caem em 'M'/'Others' (ordersController.groupByAutomations). Forçar
> 325	// um automationId falso corromperia a atribuição de P&L e não seria um mutex (não impede execução
> 326	// concorrente). A defesa de execução que importa é a trava de SELL-BTC abaixo, que barra o caso
> 327	// catastrófico (esvaziar o cofre que id3/id7 gerenciam). A coordenação na COMPRA fica na estratégia
> 328	// (regime-gate; o agente só opera BTCUSDT). Resíduo conhecido (fora de escopo, dívida): (1) gastar
> 329	// BTC via BUY de par BTC-quote (ex.: BUY ETHBTC) também drena o cofre — o agente não negocia esses
> 330	// pares; (2) uma coluna `source`/`origin` (AGENT|UI|AUTOMATION) p/ auditoria fina exige schema no
> 331	// backend. O campo automationId segue OPCIONAL, p/ vincular quando fizer sentido.
> 332	//
> 333	// ----------------------------------------------------------------------------
> 334	// ESCRITA — ordens (gated por TRADEUX_ALLOW_TRADING)
> 335	// ----------------------------------------------------------------------------
> 336	
> 337	writeTool(
> 338	  "tradeux_place_order",
> 339	  "Cria uma ordem na Binance. ATENÇÃO: na mainnet isso usa dinheiro real. TRAVA DE SEGURANÇA: SELL de BTC (qualquer par BTC<quote>, ex. BTCUSDT) é PROIBIDO ao agente — BTC é o cofre (Farm-and-Funnel); só as automações do backend (ex.: id3/id7) vendem BTC.",
> 340	  {
> 341	    symbol: z.string().describe("Par, ex: BTCUSDT"),
> 342	    side: z.enum(["BUY", "SELL"]).describe("Lado da ordem"),
> 343	    quantity: z.union([z.number(), z.string()]).describe("Quantidade (número)"),
> 344	    type: z
> 345	      .string()
> 346	      .default("LIMIT")
> 347	      .describe("MARKET, LIMIT, STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, TRAILING_STOP, ICEBERG"),
> 348	    limitPrice: z
> 349	      .union([z.number(), z.string()])
> 350	      .optional()
> 351	      .describe("Preço limite (obrigatório p/ LIMIT)"),
> 352	    options: z
> 353	      .object({
> 354	        type: z.string().optional(),
> 355	        stopPrice: z.number().optional(),
> 356	        stopPriceMultiplier: z.number().optional(),
> 357	        icebergQty: z.number().optional(),
> 358	      })
> 359	      .optional()
> 360	      .describe("Opções avançadas (stop, iceberg)"),
> 361	    automationId: z.number().int().optional().describe("Vincular a uma automação"),
> 362	  },
> 363	  (body) => {
> 364	    // Trava do cofre: o agente NUNCA vende BTC (ver isBtcVaultSymbol / NON_BTC_BASE_PREFIXES acima).
> 365	    // Vale p/ qualquer type (MARKET/LIMIT/STOP/TRAILING) — basta side=SELL e símbolo do cofre BTC.
> 366	    if (body.side === "SELL" && isBtcVaultSymbol(body.symbol)) {
> 367	      throw new Error(
> 368	        `Venda de BTC BLOQUEADA pela trava do cofre (Farm-and-Funnel): '${body.symbol}' tem BTC como ativo-base — ` +
> 369	          `o agente nunca vende o cofre. Vendas legítimas de BTC são executadas pelas automações do backend ` +
> 370	          `(ex.: id3/id7), não pelo agente.`
> 371	      );
> 372	    }
> 373	    return api.post("/orders", body);
> 374	  }
> 375	);
> 376	
> 377	writeTool(
> 378	  "tradeux_cancel_order",
> 379	  "Cancela uma ordem aberta na Binance.",
> 380	  {
> 381	    symbol: z.string().describe("Par, ex: BTCUSDT"),
> 382	    orderId: z.union([z.number(), z.string()]).describe("orderId da Binance"),
> 383	  },
> 384	  ({ symbol, orderId }) => api.del(`/orders/${symbol.toUpperCase()}/${orderId}`)
> 385	);
> 386	
> 387	writeTool(
> 388	  "tradeux_sync_order",
> 389	  "Sincroniza o status de uma ordem com a Binance.",
> 390	  { id: z.number().int().describe("ID interno da ordem (beholderOrderId)") },
> 391	  ({ id }) => api.post(`/orders/${id}/sync`)
> 392	);
> 393	
> 394	// ----------------------------------------------------------------------------
> 395	// ESCRITA — controle de automações e monitores (gated)
> 396	// ----------------------------------------------------------------------------
> 397	
> 398	writeTool(
> 399	  "tradeux_start_automation",
> 400	  "Ativa uma automação (passa a monitorar condições / agenda).",
> 401	  { id: z.number().int() },
> 402	  ({ id }) => api.post(`/automations/${id}/start`)
> 403	);
> 404	
> 405	writeTool(
> 406	  "tradeux_stop_automation",
> 407	  "Desativa uma automação.",
> 408	  { id: z.number().int() },
> 409	  ({ id }) => api.post(`/automations/${id}/stop`)
> 410	);
> 411	
> 412	writeTool(
> 413	  "tradeux_start_monitor",
> 414	  "Inicia um monitor de mercado (stream).",
> 415	  { id: z.number().int() },
> 416	  ({ id }) => api.post(`/monitors/${id}/start`)
> 417	);
> 418	
> 419	writeTool(
> 420	  "tradeux_stop_monitor",
> 421	  "Para um monitor de mercado (stream).",
> 422	  { id: z.number().int() },
> 423	  ({ id }) => api.post(`/monitors/${id}/stop`)
> 424	);
> 425	
> 426	writeTool(
> 427	  "tradeux_sync_symbols",
> 428	  "Sincroniza a lista de símbolos com a Binance (cadastra novos pares).",
> 429	  {},
> 430	  () => api.post("/symbols/sync")
> 431	);
> 432	
> 433	// ----------------------------------------------------------------------------
> 434	// NOTIFICAÇÃO — canal one-way agente -> dono (Telegram). Registrada como readTool
> 435	// DE PROPÓSITO (não-gated por TRADEUX_ALLOW_TRADING): pedir aprovação/ajuda é mais
> 436	// necessário justamente quando a escrita está travada; não mexe em ordens/automações.
> 437	// ----------------------------------------------------------------------------
> 438	
> 439	readTool(
> 440	  "tradeux_notify_owner",
> 441	  "Envia uma mensagem ao DONO via Telegram (canal ONE-WAY). Use para: solicitar APROVAÇÃO antes de algo sensível, pedir AJUDA quando bloqueado, ou avisar EVENTOS importantes (saída de regime, cross real, anomalia, incoerência). NÃO espere resposta no mesmo ciclo — após solicitar, siga o caminho CONSERVADOR (normalmente: não agir) até haver orientação. Máx. 1500 caracteres.",
> 442	  {
> 443	    message: z
> 444	      .string()
> 445	      .min(1)
> 446	      .max(1500)
> 447	      .describe("Mensagem clara e auto-contida (pt-BR), com contexto e o que você precisa do dono"),
> 448	  },
> 449	  ({ message }) => api.post("/agent/notify", { message })
> 450	);
> 451	
> 452	// ----------------------------------------------------------------------------
> 453	
> 454	async function main() {
> 455	  const transport = new StdioServerTransport();
> 456	  await server.connect(transport);
> 457	  // Log vai para stderr — stdout é reservado ao protocolo MCP.
> 458	  console.error(
> 459	    `tradeux-mcp pronto (API=${api.baseUrl}, trading=${tradingEnabled() ? "ON" : "OFF"})`
> 460	  );
> 461	}
> 462	
> 463	main().catch((e) => {
> 464	  console.error("Falha ao iniciar tradeux-mcp:", e);
> 465	  process.exit(1);
> 466	});
> 467	
> ```

## 🤖 Claude *(14:09:19)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/tradeux-mcp/src/index.js",
  "offset": 60,
  "limit": 45
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 60	  const variables = [...new Set(list.map((ix) => ix && ix.variable).filter(Boolean))].sort();
> 61	  const symbols = [...new Set(list.map((ix) => ix && ix.symbol).filter(Boolean))].sort();
> 62	  const keptSymbols = symbols.slice(0, MEMORY_INDEXES_SYMBOL_CAP);
> 63	  return {
> 64	    totalKeys: list.length,
> 65	    variables,
> 66	    symbols: keptSymbols,
> 67	    _omittedSymbols: symbols.length - keptSymbols.length, // cauda de símbolos suprimida
> 68	    hint: "Resumo compacto. Passe symbol=<PAR> (ex.: BTCUSDT) p/ as chaves detalhadas (eval/example) de um símbolo.",
> 69	  };
> 70	}
> 71	
> 72	// Ferramenta de leitura: sempre disponível.
> 73	function readTool(name, description, schema, handler) {
> 74	  server.tool(name, description, schema, async (args) => {
> 75	    try {
> 76	      return ok(await handler(args ?? {}));
> 77	    } catch (e) {
> 78	      return fail(e.message);
> 79	    }
> 80	  });
> 81	}
> 82	
> 83	// Ferramenta de escrita: travada atrás de TRADEUX_ALLOW_TRADING=true.
> 84	function writeTool(name, description, schema, handler) {
> 85	  const guarded = `${description} [REQUER TRADEUX_ALLOW_TRADING=true]`;
> 86	  server.tool(name, guarded, schema, async (args) => {
> 87	    try {
> 88	      if (!tradingEnabled()) {
> 89	        throw new Error(
> 90	          "Ações de trading desativadas. Defina TRADEUX_ALLOW_TRADING=true para habilitar."
> 91	        );
> 92	      }
> 93	      return ok(await handler(args ?? {}));
> 94	    } catch (e) {
> 95	      return fail(e.message);
> 96	    }
> 97	  });
> 98	}
> 99	
> 100	// ----------------------------------------------------------------------------
> 101	// LEITURA — conta, carteira, mercado
> 102	// ----------------------------------------------------------------------------
> 103	
> 104	readTool(
> ```

## 🤖 Claude *(14:09:25)*

Items (2) and (4) confirmed. The complete list of write tools is: `place_order`, `cancel_order`, `sync_order`, `start/stop_automation`, `start/stop_monitor`, `sync_symbols`. There is NO write tool for `/system/floor`, `/system/halt`, `/exchange/withdraw`, or `PATCH /settings`. The only `/settings` reference is `api.get("/settings")` (read-only, line 108). `tradeux_notify_owner` is a one-way readTool (POST /agent/notify). 

Now let me verify item (3) the fail-closed riskState behaviors and the env-hard non-flippability — already largely confirmed by reading riskState.js (lines 30, 79, 87 confirm: `ENV_HALT_HARD` is a const read once at module load; fail-closed sets `floor.on=true`). And item (5) crypto.js AES_KEY=32 validation. And the ressalva about mcpClient.js:21 passing full env to child. Let me check crypto.js and mcpClient.js.

## 🤖 Claude *(14:09:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && echo \"=== crypto.js AES_KEY validation ===\"; grep -nE \"AES_KEY|length|throw|32|createCipher|createDecipher\" backend/src/utils/crypto.js; echo; echo \"=== mcpClient.js env passing (~line 21) ===\"; grep -nE \"env:|process\\.env|spawn|stdio|TRADEUX_PASSWORD|TRADEUX_EMAIL\" tradeux-agent/src/mcpClient.js | head -30",
  "description": "Verify crypto AES_KEY validation and mcpClient env passing"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === crypto.js AES_KEY validation ===
> 3:const key = aes.utils.utf8.toBytes(process.env.AES_KEY);
> 4:if (key.length !== 32) throw new Error('Invalid key size for AES. Must be 256-bit / 32 bytes.');
> 
> === mcpClient.js env passing (~line 21) ===
> 1:// Cliente MCP que sobe o servidor tradeux-mcp (stdio), lista as ferramentas e
> 5:import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";
> 15:  const serverPath = process.env.TRADEUX_MCP_PATH || DEFAULT_MCP_PATH;
> 21:    env: { ...process.env },
> ```

## 🤖 Claude *(14:09:33)*

All five items confirmed against the real code, and the ressalva (mcpClient.js:21 `env: { ...process.env }` passes the full parent env to the MCP child) is accurate. Let me do one final adversarial check: verify there's genuinely no other way the agent process could issue raw HTTP to the backend — e.g., via the `index.js` CLI or a tool-result that smuggles a URL — and confirm the openrouter `fetch` BASE isn't attacker-controllable to point at the backend. Let me also double-check `tradingEnabled()` and confirm there's no `eval`/dynamic-require vector in the agent.

## 🤖 Claude *(14:09:37)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && echo \"=== openrouter BASE source ===\"; grep -nE \"BASE\\s*=|OPENROUTER|process\\.env\\.(TRADEUX_AGENT_BASE|OPENROUTER)\" tradeux-agent/src/providers/openrouter.js | head; echo; echo \"=== any eval / dynamic require / child_process in agent (excl providers fetch) ===\"; grep -rnE \"\\beval\\(|new Function|child_process|exec\\(|require\\(.*\\$|import\\(\" tradeux-agent/src/ | grep -v node_modules; echo; echo \"=== tradingEnabled def ===\"; grep -nE \"tradingEnabled|TRADEUX_ALLOW_TRADING\" tradeux-mcp/src/index.js | head",
  "description": "Check openrouter BASE controllability and agent dynamic-code vectors"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === openrouter BASE source ===
> 5:const BASE = (process.env.OPENROUTER_BASE_URL || "https://openrouter.ai/api/v1").replace(/\/$/, "");
> 6:const API_KEY = process.env.OPENROUTER_API_KEY;
> 8:// "openai/gpt-4o"). Veja https://openrouter.ai/models. Configure via OPENROUTER_MODEL.
> 9:const MODEL = process.env.OPENROUTER_MODEL || process.env.TRADEUX_AGENT_MODEL || "openai/gpt-4o-mini";
> 33:  if (!API_KEY) throw new Error("OPENROUTER_API_KEY ausente.");
> 40:  if (process.env.OPENROUTER_SITE_URL) headers["HTTP-Referer"] = process.env.OPENROUTER_SITE_URL;
> 41:  if (process.env.OPENROUTER_APP_NAME) headers["X-Title"] = process.env.OPENROUTER_APP_NAME;
> 
> === any eval / dynamic require / child_process in agent (excl providers fetch) ===
> tradeux-agent/src/notifyDedup.js:116:  while ((mm = re.exec(norm)) !== null) trans.add(`${SYNONYMS[mm[1]] || mm[1]}>${SYNONYMS[mm[2]] || mm[2]}`);
> 
> === tradingEnabled def ===
> 8://   TRADEUX_ALLOW_TRADING  "true" para liberar ações que mexem em ordens/automações
> 19:const tradingEnabled = () => process.env.TRADEUX_ALLOW_TRADING === "true";
> 83:// Ferramenta de escrita: travada atrás de TRADEUX_ALLOW_TRADING=true.
> 85:  const guarded = `${description} [REQUER TRADEUX_ALLOW_TRADING=true]`;
> 88:      if (!tradingEnabled()) {
> 90:          "Ações de trading desativadas. Defina TRADEUX_ALLOW_TRADING=true para habilitar."
> 334:// ESCRITA — ordens (gated por TRADEUX_ALLOW_TRADING)
> 435:// DE PROPÓSITO (não-gated por TRADEUX_ALLOW_TRADING): pedir aprovação/ajuda é mais
> 459:    `tradeux-mcp pronto (API=${api.baseUrl}, trading=${tradingEnabled() ? "ON" : "OFF"})`
> ```

## 🤖 Claude *(14:09:43)*

Verification complete. The `re.exec` in notifyDedup.js is a regex match (not code eval) — no dynamic-code vector. The openrouter BASE comes from env, not from model output, so the model cannot redirect HTTP at the backend. All claims hold.

Now I'll synthesize the verdict. This "finding" is a clean-bill-of-health INFO assertion, and my job is to confirm whether the all-clear is justified. It is — every one of the 5 claims is accurate against the code, and the ressalva is correct. The honest framing: this is NOT a bug; it's a correctly-verified baseline. So `confirmed=false` (no real problem exists) at `NOT_AN_ISSUE` severity — but I'll capture the two legitimate defense-in-depth caveats the finding itself raises so they're not lost.

## 🤖 Claude *(14:10:08)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "title": "Hardening de segredos / sem HTTP cru no agente / riskState fail-closed / withdraw fora do MCP \u2014 all-clear CONFIRMADO (baseline, n\u00e3o \u00e9 bug)",
  "confirmed": false,
  "severityFinal": "NOT_AN_ISSUE",
  "locationConfirmed": "backend/src/riskState.js:30,79,87 + tradeux-mcp/src/index.js:337-450 + tradeux-agent/src/mcpClient.js:21 + backend/src/utils/crypto.js:3-4",
  "evidence": "Os 5 itens batem com o c\u00f3digo real:\n(1) Segredos: `git ls-files | grep .env` retorna S\u00d3 `*.env.example`; `.gitignore` ignora `.env` (raiz:71, tradeux-agent:2, tradeux-mcp:2); perms `-rw-------` (0600) gcrux-tradeux nos 3 `.env`.\n(2) Sem HTTP cru no agente: grep por axios/fetch/http.request em tradeux-agent/src/{agent,index,mcpClient,journal,notifyDedup}.js = ZERO. O \u00fanico `fetch` \u00e9 tradeux-agent/src/providers/openrouter.js:43 \u2192 `${BASE}/chat/completions`, com `BASE=process.env.OPENROUTER_BASE_URL||\"https://openrouter.ai/api/v1\"` (linha 5) \u2014 endpoint do LLM, n\u00e3o do backend, e a URL vem do env (n\u00e3o do output do modelo). Logo o MODELO n\u00e3o tem vetor pra POST /system/floor, /exchange/withdraw ou PATCH /settings. Sem `eval`/`new Function`/`child_process`/`import()` din\u00e2mico no agente (o \u00fanico `re.exec` em notifyDedup.js:116 \u00e9 regex, n\u00e3o c\u00f3digo).\n(3) riskState fail-closed CONFIRMADO: `ENV_HALT_HARD = process.env.TRADING_HALT_HARD === 'true'` \u00e9 const lida 1\u00d7 no load (linha 30) \u2192 n\u00e3o-flip\u00e1vel em runtime; `loadFromDisk` catch \u2192 `floor={on:true,...}` (linha 79); `isHalted()` = `ENV_HALT_HARD || floor.on || manual.on || (dailyCap...)` (linha 87) e o guard lan\u00e7a se isHalted lan\u00e7ar (dire\u00e7\u00e3o segura).\n(4) MCP sem write-tool sens\u00edvel CONFIRMADO: a lista COMPLETA de writeTool \u00e9 place_order(POST /orders), cancel_order, sync_order, start/stop_automation, start/stop_monitor, sync_symbols (index.js:337-431). Nenhuma toca /system, /exchange/withdraw nem PATCH /settings. A \u00daNICA ref a /settings \u00e9 `api.get(\"/settings\")` em readTool (linha 108, GET). `tradeux_notify_owner` \u00e9 readTool one-way (POST /agent/notify). place_order tem a trava FAIL-CLOSED de SELL-BTC (`isBtcVaultSymbol`, linhas 366-372).\n(5) crypto.js:3-4 valida `key.length !== 32 \u2192 throw` no load.\nRessalva VERDADEIRA: mcpClient.js:21 `env: { ...process.env }` herda TRADEUX_PASSWORD/keys pro filho MCP (esperado, mas amplo).",
  "reasoning": "Este \"achado\" \u00e9 um atestado de seguran\u00e7a limpo (INFO), n\u00e3o um defeito. Verifiquei adversarialmente as 5 afirma\u00e7\u00f5es + a ressalva contra o c\u00f3digo REAL e TODAS se sustentam com evid\u00eancia concreta \u2014 ent\u00e3o n\u00e3o h\u00e1 problema a confirmar (confirmed=false, NOT_AN_ISSUE). \u00c9 um baseline correto do que j\u00e1 est\u00e1 seguro.\n\nDois pontos honestos que o pr\u00f3prio achado levanta e que valem registrar como d\u00edvida de defesa-em-profundidade (N\u00c3O bugs hoje):\n1. A premissa de n\u00e3o-explora\u00e7\u00e3o depende de o agente s\u00f3 falar MCP-stdio. A barreira N\u00c3O \u00e9 criptogr\u00e1fica nem um sandbox de rede \u2014 \u00e9 simplesmente \"ningu\u00e9m escreveu um fetch/tool pro backend\". A primeira regress\u00e3o que adicione (a) um write-tool no MCP pra /system|/settings|/withdraw, ou (b) qualquer cliente HTTP no agent.js, reabre o vetor instantaneamente. Os HIGH conhecidos (withdraw/HALT/useTestnet sem auth de 2\u00aa camada no backend) continuam latentes; o que falta \u00e9 s\u00f3 o gatilho.\n2. mcpClient.js:21 herda o env inteiro (TRADEUX_PASSWORD, chaves) pro processo MCP. Se um dia o MCP carregar depend\u00eancia comprometida ou logar env, o segredo vaza. Mitiga\u00e7\u00e3o barata: passar s\u00f3 as vars que o MCP precisa (TRADEUX_API_URL/EMAIL/PASSWORD/ALLOW_TRADING), n\u00e3o `{...process.env}`.\n\nNada a corrigir nos itens marcados OK \u2014 eles est\u00e3o de fato OK. Severidade FINAL: NOT_AN_ISSUE (\u00e9 verifica\u00e7\u00e3o-limpa, n\u00e3o achado)."
}
```

> **Tool Result (StructuredOutput)** - ✅ Success
>
> ```
> Structured output provided successfully
> ```

## 🤖 Claude *(14:10:26)*

Verifiquei adversarialmente o achado contra o código real. VEREDITO: PASS — o atestado de segurança está CORRETO; não é bug.

Resumo da verificação (todos os 5 itens + a ressalva CONFIRMADOS com evidência):

1. Segredos OK — `git ls-files | grep .env` só retorna `*.env.example`; `.env` gitignored em 3 lugares; perms `0600` gcrux-tradeux nos três `.env`.
2. Sem HTTP cru no agente OK — zero axios/fetch/http em `tradeux-agent/src/{agent,index,mcpClient,journal,notifyDedup}.js`. O único `fetch` é `providers/openrouter.js:43` para o endpoint do LLM (`BASE` vem do env, não do output do modelo). Sem `eval`/`new Function`/`child_process`/`import()` dinâmico. O modelo não tem vetor para `POST /system/floor`, `/exchange/withdraw` ou `PATCH /settings`.
3. riskState fail-closed OK — `backend/src/riskState.js:30` (`ENV_HALT_HARD` const lida 1× no load, não-flipável em runtime), `:79` (disco ilegível → `floor.on=true`), `:87` (`isHalted` = OR de todas as fontes).
4. MCP sem write-tool sensível OK — lista completa de `writeTool` em `tradeux-mcp/src/index.js:337-431` é place/cancel/sync order, start/stop automation+monitor, sync symbols. Nenhuma toca `/system`, `/exchange/withdraw` nem `PATCH /settings`. A única ref a `/settings` é `api.get` (read, linha 108). place_order tem a trava FAIL-CLOSED de SELL-BTC (`:366-372`).
5. crypto AES_KEY OK — `backend/src/utils/crypto.js:3-4` faz `throw` se `key.length !== 32`.

Ressalva VERDADEIRA: `tradeux-agent/src/mcpClient.js:21` passa `env: { ...process.env }` ao filho MCP, herdando `TRADEUX_PASSWORD`/chaves.

Severidade FINAL: NOT_AN_ISSUE (`confirmed=false`). É uma verificação-limpa, não um defeito — nada a corrigir nos itens marcados OK.

Dívida de defesa-em-profundidade (registro honesto, não-bloqueante):
- A não-exploração depende só de "ninguém escreveu um fetch/write-tool pro backend" — não há sandbox de rede nem 2ª camada de auth no backend. Os HIGH conhecidos (withdraw/HALT/useTestnet) seguem latentes; falta apenas o gatilho (nova tool MCP de `/system`, ou um cliente HTTP no agente).
- `mcpClient.js:21` deveria passar só `TRADEUX_API_URL/EMAIL/PASSWORD/ALLOW_TRADING`, não `{...process.env}`, para reduzir superfície de vazamento de segredo.

Recomendação de merge: nada a mergear (é atestado). Adotar como baseline e abrir as duas dívidas acima como hardening de prioridade baixa.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-22 - agent-a0940db4cb9a271fd]]
> * **Próxima Sessão**: [[2026-06-22 - agent-a0df6aca4064a621c]]
%% --- TIMELINE END --- %%

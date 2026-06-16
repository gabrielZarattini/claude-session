# Session agent-aaeb5a52a6ab8f1cd
**Date:** 2026-06-16 | **Session ID:** `agent-aaeb5a52a6ab8f1cd`

---

## 👤 User *(22:08:17)*

Merge-decision review of an uncommitted change in TradeUX at /home/gcrux-tradeux/tradeux. Diff: `sudo -n -u gcrux-tradeux git -c safe.directory='*' --no-pager diff -- backend/src/cockpitJob.js tradeux-mcp/src/index.js`.

## Context
The read-only cockpit's `deriveGates` applied the BTC-baseline FLOW filter uniformly to all symbols. Ground truth (verified in live DB + setup scripts): only the BTC baseline id2 is flow-gated (setup-flow-gate.js); the alt FARMs (LTC/BNB/ADA, active) gate on RSI+regime only, NO flow (setup-farm.js:131). So the cockpit mislabeled alt gates (e.g. BNB buyAllowed=false "baseline veta o dip" when BNB's farm has no flow gate). The observation agent flagged it. This is the 4th cockpit-VIEW correctness fix this session (after freshen, mixed-label, prompt-consolidation). Read-only, no money impact (HALT on; and even live, the fix makes the VIEW match the automations).

## The change
`deriveGates` becomes symbol-aware: `buyAllowed = flowGated ? baseline : farm`, where flowGated is driven by `COCKPIT_FLOW_GATED_SYMBOLS` env (default BTCUSDT). Alt reason now says "FARM liberado, sem filtro de fluxo" (capitulation noted as informational). New `flowGated` field exposed (+ farm/baseline in MCP buyGate).

## Your job — judge design & whether to merge
- Is symbol-aware gating with an env-driven FLOW_GATED set the right abstraction, or is hardcoding the farm-vs-baseline distinction brittle? Is there a cleaner way (e.g. deriving flow-gatedness from the live automation conditions instead of a config set)? Weigh simplicity vs. coupling-to-config.
- Is the env default 'BTCUSDT' a reasonable single-source assumption given id2 is the only flow-gated baseline? What breaks if a flow-gated baseline is later added for an alt and someone forgets the env? (the comment should make that discoverable — check it does.)
- Meta-question worth your judgment: this is the 4th VIEW-accuracy fix prompted by the agent probing the cockpit. Is chasing per-module gate accuracy in a read-only doctrine panel the right investment, or should the cockpit gates be explicitly labeled "approximate doctrine, see live automation conditions" and stop chasing? Give a recommendation (keep refining vs. declare doctrine-approximate). This is the more important question than the diff itself.
- Convention (pt-BR), no money-path/HALT coupling, doctrine:true preserved.
- Block / must-fix?

Return APPROVE / APPROVE COM SUGESTÕES / REQUEST CHANGES / BLOCK with must-fix vs nice-to-have, and answer the meta-question explicitly. Cite file:line.

## 🤖 Claude *(22:08:20)*

I'll review this change. Let me load context and examine the diff and ground-truth files.

## 🤖 Claude *(22:08:20)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sudo -n -u gcrux-tradeux git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' --no-pager diff -- backend/src/cockpitJob.js tradeux-mcp/src/index.js",
  "description": "Show the uncommitted diff for cockpit and MCP"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> diff --git a/backend/src/cockpitJob.js b/backend/src/cockpitJob.js
> index 2c93a57..97a1b97 100644
> --- a/backend/src/cockpitJob.js
> +++ b/backend/src/cockpitJob.js
> @@ -76,32 +76,42 @@ async function resolveSymbols() {
>  
>  // Estado DERIVADO dos gates de compra POR MÓDULO (view do cockpit, limiares transparentes). NÃO emite ordem.
>  // Espelha a doutrina das automações (ver SYSTEM_PROMPT do agente):
> -//   - FARM/BASELINE ACUMULAM em MEAN-REVERSION (range OU mixed): regime != bear E != trend (baseline ainda
> -//     exige fluxo não-capitulação). 'mixed' tem strategy=mean-reversion no classifier e a condition VIVA da
> -//     farm é MEMORY[REGIME]!=='bear' && !=='trend' (setup-farm.js:131) — então liberar em mixed é CORRETO, não bug.
> -//   - TREND compra no golden cross: gated só por != bear
> -//   - HARVESTER é DESGATEADO do regime (opera em qualquer regime)
> -// `buyAllowed` = gate de ACUMULAÇÃO (farm/baseline), o "padrão"; trend/harvester têm caminhos próprios.
> -function deriveGates(regime, flow) {
> +//   - FARM (alts LTC/BNB/ADA): RSI+regime (mean-reversion, range OU mixed: != bear && != trend), SEM filtro de
> +//     fluxo (condition VIVA = MEMORY[REGIME]!=='bear' && !=='trend', setup-farm.js:131). 'mixed' é mean-reversion
> +//     no classifier → liberar em mixed é CORRETO, não bug.
> +//   - BASELINE (BTC id2): farm + filtro de FLUXO não-capitulação (setup-flow-gate.js) — É O ÚNICO módulo de
> +//     acumulação flow-gated. Aplicar o filtro de fluxo às ALTS MENTE (vetaria entrada que a farm viva FARIA).
> +//   - TREND compra no golden cross: gated só por != bear; HARVESTER é DESGATEADO (opera em qualquer regime).
> +// `buyAllowed` = gate de ACUMULAÇÃO do SÍMBOLO: FARM (alts, sem fluxo) ou BASELINE (BTC, com fluxo), conforme FLOW_GATED.
> +
> +// Símbolos cujo módulo de acumulação gateia por FLUXO: SÓ a baseline BTC (id2). Default BTCUSDT; env sobrescreve.
> +const FLOW_GATED = new Set((process.env.COCKPIT_FLOW_GATED_SYMBOLS || 'BTCUSDT').split(',').map(s => s.trim().toUpperCase()).filter(Boolean));
> +
> +function deriveGates(regime, flow, symbol) {
>      const regimeOk = !!regime && regime !== 'bear' && regime !== 'unknown';
>      const flowFresh = flow && Number.isFinite(flow.imbalance) && flow.atMs && (Date.now() - flow.atMs) < FLOW_STALE_MS;
>      // fail-CLOSED como a id2 (auditoria): fluxo stale/ausente NÃO libera (conservador). Antes era fail-OPEN
>      // (mostrava GO sem fluxo fresco) — direção PERIGOSA/enganosa vs a automação real, que BLOQUEIA o dip.
>      const flowOk = !!flowFresh && flow.imbalance >= FLOW_BUY_MIN;
> -    const farm = regimeOk && regime !== 'trend';        // farm acumula em mean-reversion (range/mixed): != bear && != trend
> -    const baseline = farm && flowOk;                    // baseline = farm + filtro de fluxo (fail-closed)
> +    const farm = regimeOk && regime !== 'trend';        // farm: RSI+regime (mean-reversion range/mixed), SEM fluxo
> +    const baseline = farm && flowOk;                    // baseline (BTC id2): farm + filtro de fluxo (fail-closed)
>      const trend = regimeOk;                             // trend compra no golden cross (!= bear)
> -    const buyAllowed = baseline;
> +    const flowGated = !!symbol && FLOW_GATED.has(String(symbol).toUpperCase());
> +    const buyAllowed = flowGated ? baseline : farm;     // alt: farm (sem fluxo); símbolo flow-gated (BTC): baseline
>      let reason;
>      if (!regimeOk) reason = `regime=${regime || 'unknown'}: acumulação em CAIXA (farm/baseline e trend parados)`;
>      else if (regime === 'trend') reason = 'regime=trend: farm/baseline em CAIXA (correto); trend compra no golden cross';
> -    else if (!flowFresh) reason = 'fluxo stale/ausente → conservador (fail-closed, como a id2): acumulação NÃO liberada';
> -    else if (!flowOk) reason = `fluxo em capitulação (imbalance ${flow.imbalance} < ${FLOW_BUY_MIN}): baseline veta o dip`;
> -    else reason = `regime=${regime} (mean-reversion: range/mixed) + fluxo ok: acumulação (farm/baseline) liberada`;
> +    else if (!flowGated) {
> +        const cap = (flowFresh && !flowOk) ? ` — fluxo em capitulação (imbalance ${flow.imbalance}) é INFORMATIVO, NÃO gateia o farm` : '';
> +        reason = `regime=${regime} (mean-reversion: range/mixed) + RSI: FARM liberado, SEM filtro de fluxo${cap}`;
> +    }
> +    else if (!flowFresh) reason = 'fluxo stale/ausente → conservador (fail-closed, como a id2): baseline BTC NÃO liberada';
> +    else if (!flowOk) reason = `fluxo em capitulação (imbalance ${flow.imbalance} < ${FLOW_BUY_MIN}): baseline BTC veta o dip`;
> +    else reason = `regime=${regime} (mean-reversion: range/mixed) + fluxo ok: baseline BTC liberada`;
>      // doctrine=true (auditoria): estes gates são a DOUTRINA por regime (o que a estratégia FARIA), NÃO confirmam
>      // que a automação correspondente (ex.: baseline id2, hoje isActive=0) está ATIVA — o gate VIVO mora na
>      // condition da automação no banco. O agente/painel deve reportar como doutrina, não como estado vivo.
> -    return { regime, regimeOk, flowOk, flowFresh: !!flowFresh, flowBuyMin: FLOW_BUY_MIN, farm, baseline, trend, harvesterUngated: true, buyAllowed, reason, doctrine: true };
> +    return { regime, regimeOk, flowOk, flowFresh: !!flowFresh, flowBuyMin: FLOW_BUY_MIN, flowGated, farm, baseline, trend, harvesterUngated: true, buyAllowed, reason, doctrine: true };
>  }
>  
>  // Reaplica regime/flow/gates FRESCOS (leituras baratas da MEMORY) sobre um snapshot, preservando a
> @@ -119,7 +129,7 @@ function freshen(symbol, snap) {
>      const flow = flowRaw
>          ? { imbalance: flowRaw.imbalance, toxicity: flowRaw.toxicity, atMs: Number.isFinite(flowRaw.atMs) ? flowRaw.atMs : null, ageMs: flowAgeMs }
>          : null;
> -    const gates = deriveGates(regime, flowRaw);
> +    const gates = deriveGates(regime, flowRaw, symbol);
>      return { ...snap, regime, flow, gates, flowAgeMs };
>  }
>  
> @@ -142,7 +152,7 @@ async function runOnce() {
>                  // snapshot de regime/flow lido da MEMORY (já populada pelos outros jobs) — mesma leitura do flowJob
>                  const regime = beholder.getMemory(symbol, indexKeys.REGIME) || null;
>                  const flow = beholder.getMemory(symbol, indexKeys.FLOW) || null;
> -                const gates = deriveGates(regime, flow);
> +                const gates = deriveGates(regime, flow, symbol);
>  
>                  const snapshot = {
>                      symbol, source: m.source, interval: m.interval,
> diff --git a/tradeux-mcp/src/index.js b/tradeux-mcp/src/index.js
> index 9e0a48a..c30cff9 100644
> --- a/tradeux-mcp/src/index.js
> +++ b/tradeux-mcp/src/index.js
> @@ -225,7 +225,7 @@ readTool(
>          medAbsMovePct: dist.medAbsMovePct, sigmaPct: dist.sigmaPct, pHitBreakevenPct: dist.pHitBreakevenPct,
>          evNetPct: ev.netPct, breakevenPct: ev.breakevenPct,
>          mc: { p10: mc.p10, p50: mc.p50, p90: mc.p90, horizonMin: mc.horizonMin, driftless: true },
> -        buyGate: { allowed: gates.buyAllowed, reason: gates.reason, flowFresh: gates.flowFresh },
> +        buyGate: { allowed: gates.buyAllowed, reason: gates.reason, flowFresh: gates.flowFresh, flowGated: gates.flowGated, farm: gates.farm, baseline: gates.baseline },
>          stale: c.stale,
>        };
>      }
> ```

## 🤖 Claude *(22:08:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sudo -n -u gcrux-tradeux git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' --no-pager status --short",
  "description": "Show working tree status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>  M backend/src/cockpitJob.js
>  M tradeux-mcp/src/index.js
> ```

## 🤖 Claude *(22:08:24)*

Let me verify the ground-truth claims in the setup scripts and check how `flowGated` / new MCP fields are consumed downstream.

## 🤖 Claude *(22:08:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "find . -name 'setup-farm.js' -o -name 'setup-flow-gate.js' 2>/dev/null | grep -v node_modules",
  "description": "Locate setup scripts"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ./backend/scripts/setup-flow-gate.js
> ./backend/scripts/setup-farm.js
> ```

## 🤖 Claude *(22:08:27)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"flowGated\\|buyAllowed\\|deriveGates\\|buyGate\\|COCKPIT_FLOW_GATED_SYMBOLS\\|\\.baseline\\|\\.farm\\b\" --include=*.js --include=*.jsx --include=*.ts -l . | grep -v node_modules",
  "description": "Find consumers of the gate fields"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> frontend/src/private/Cockpit/Cockpit.js
> tradeux-agent/src/agent.js
> tradeux-mcp/src/index.js
> backend/src/cockpitJob.js
> ```

## 🤖 Claude *(22:08:31)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '110,150p' /home/gcrux-tradeux/tradeux/backend/scripts/setup-farm.js; echo \"===== FLOW-GATE =====\"; sed -n '1,200p' /home/gcrux-tradeux/tradeux/backend/scripts/setup-flow-gate.js | grep -n \"flow\\|imbalance\\|FLOW\\|BTCUSDT\\|symbol\\|condition\\|automationId\\|id\\b\" ",
  "description": "Inspect farm and flow-gate setup conditions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> async function setupSymbol(token, symbol) {
>     const K = k => `${symbol}:${k}`;
>     console.log(`\n## ${symbol}`);
>     console.log('- ' + await ensureMonitor(token, symbol));
> 
>     const buyTpl = await ensureTemplate(token, symbol, `Farm Buy ${symbol}`, 'BUY', {
>         type: 'LIMIT', limitPrice: `MEMORY['${K('BOOK')}'].current.bestAsk * ${(1 + BUF).toFixed(4)}`, limitPriceMultiplier: 1,
>         quantity: 'MIN_NOTIONAL', quantityMultiplier: SIZE_MULT,
>     });
>     console.log('- ' + buyTpl.msg);
>     const sellTpl = await ensureTemplate(token, symbol, `Farm Sell ${symbol}`, 'SELL', {
>         type: 'LIMIT', limitPrice: `MEMORY['${K('BOOK')}'].current.bestBid * ${(1 - BUF).toFixed(4)}`, limitPriceMultiplier: 1,
>         quantity: 'LAST_ORDER_QTY', quantityMultiplier: 1, // vende o lote comprado (a última ordem foi a compra)
>     });
>     console.log('- ' + sellTpl.msg);
> 
>     // COMPRA: dip (RSI<lo) fora de bear/trend. Condition regex-safe (validateConditions exige cada cláusula
>     // = MEMORY[...]OP valor, SEM espaços/||/guards soltos). O REGIME vai no INDEX → isChecked é o FAIL-SAFE
>     // (sem regime conhecido a automação NÃO avalia). invertCondition no RSI → dispara só na TRANSIÇÃO p/ baixo
>     // de lo (anti-empilhamento). v1 = 1 lote simples; sem trava de posição → pode haver DCA leve em re-cruzamentos
>     // (a venda realiza a última compra via LAST_ORDER_QTY; rastreio multi-lote/FARM_QTY é refino — §5 do doc).
>     const buyCond = `MEMORY['${K(RSI_KEY_SUFFIX)}'].current<${RSI_LO} && MEMORY['${K('REGIME')}']!=='bear' && MEMORY['${K('REGIME')}']!=='trend'`;
>     console.log('- ' + await ensureAutomation(token, symbol, `Farm Buy ${symbol}`, buyCond, `${K(RSI_KEY_SUFFIX)},${K('REGIME')}`, buyTpl.id));
> 
>     // VENDA no-loss: tem posição (última ordem = compra) E o bestBid já dá lucro sobre o preço de compra.
>     // Index = BOOK,LAST_ORDER → isChecked garante AMBOS presentes (sem guards soltos; até a 1ª compra não avalia).
>     // invertCondition no BOOK → realiza só na TRANSIÇÃO em que o bestBid cruza o alvo (anti-empilhamento), indep. do RSI.
>     const sellCond = `MEMORY['${K('LAST_ORDER')}'].side==='BUY' && MEMORY['${K('BOOK')}'].current.bestBid>MEMORY['${K('LAST_ORDER')}'].avgPrice*${(1 + PROFIT).toFixed(4)}`;
>     console.log('- ' + await ensureAutomation(token, symbol, `Farm Sell ${symbol}`, sellCond, `${K('BOOK')},${K('LAST_ORDER')}`, sellTpl.id));
> }
> 
> (async () => {
>     if (!EM || !PW) { console.error('faltam credenciais (EM/PW ou TRADEUX_EMAIL/TRADEUX_PASSWORD)'); process.exit(1); }
>     const login = await req('POST', '/login', null, { email: EM, password: PW });
>     const token = login.body && login.body.token;
>     if (!token) { console.error('LOGIN_FAIL ' + login.status); process.exit(1); }
> 
>     console.log(`# Setup FARM no-loss — ${SYMBOLS.join(', ')} | RSI<${RSI_LO} compra · lucro-alvo ${(PROFIT * 100).toFixed(1)}% · buffer ${(BUF * 100).toFixed(1)}% · size ${SIZE_MULT}×MIN_NOTIONAL${DRY ? '   [DRY-RUN: nada será aplicado]' : ''}`);
> 
>     for (const symbol of SYMBOLS) await setupSymbol(token, symbol);
> 
> ===== FLOW-GATE =====
> 4: * Pré-requisito: flowJob no ar gravando MEMORY['<sym>:FLOW'] = {imbalance,toxicity,at,atMs} (commit f833032).
> 6: * O que faz: adiciona à condition da id2 um filtro PASSIVO de fluxo do taker (mainnet) — só compra o dip
> 8: * fluxo vendedor exaurir/voltar à neutralidade antes de comprar). Inclui FLOW nos indexes (fail-safe).
> 11: *   (1) FLOW nos `indexes` → se MEMORY['<sym>:FLOW'] for null/ausente (job off, boot, Binance fora) o
> 13: *   (2) STALE: `(Date.now()-MEMORY['<sym>:FLOW'].atMs) < MAX_AGE` — se o dado envelhecer (job preserva o
> 15: *   (3) null-guard `MEMORY['<sym>:FLOW'] && ...` na própria condition (belt-and-suspenders); throw no eval
> 20: * logs/flow-capitulation.log. Re-rodar este script com novo FLOW_GATE_MIN ATUALIZA o gate (idempotente).
> 22: * Uso (no container, server no ar):  node scripts/setup-flow-gate.js   [DRY=true]
> 23: *   env: EM/PW (ou TRADEUX_EMAIL/PASSWORD), PORT (3001), FLOW_SYMBOL (BTCUSDT),
> 24: *        FLOW_GATE_MIN (-0.40 = piso do imbalance p/ permitir compra),
> 25: *        FLOW_GATE_MAX_AGE_MS (180000 = idade máx. do dado de fluxo p/ confiar; senão trava).
> 29:const SYMBOL = (process.env.FLOW_SYMBOL || 'BTCUSDT').toUpperCase();
> 30:const KF = `${SYMBOL}:FLOW`;
> 31:const _min = parseFloat(process.env.FLOW_GATE_MIN || '-0.40');
> 33:const _age = parseInt(process.env.FLOW_GATE_MAX_AGE_MS || '180000', 10);
> 36:const BASE = { host: process.env.FLOW_API_HOST || '127.0.0.1', port: parseInt(process.env.PORT || '3001', 10) };
> 69:// clause do gate de fluxo (sempre o segmento FINAL da condition). Re-tunável: ao re-rodar, o segmento
> 77:    // O stale-check vive AQUI (no consumo, a condition da id2), NÃO no job: o flowJob PRESERVA o último
> 80:    const gate = `MEMORY['${KF}'] && (Date.now()-MEMORY['${KF}'].atMs)<${MAX_AGE} && MEMORY['${KF}'].imbalance>${MIN}`;
> 90:    console.log(`# Gate de Fluxo (Sniper) na id2 — ${SYMBOL}  [imbalance>${MIN}, maxAge=${MAX_AGE}ms]${DRY ? '  [DRY-RUN]' : ''}\n`);
> 95:    const full = await req('GET', `/automations/${a.id}`, token);
> 99:    const newConditions = buildConditions(cur.conditions || '');
> 101:    if (newConditions === cur.conditions && newIndexes === cur.indexes) {
> 102:        console.log(`✓ id2 (id ${a.id}) já com o gate de fluxo idêntico (imbalance>${MIN}). Nada a fazer.`);
> 105:    console.log(`conditions: ${cur.conditions}`);
> 112:    const r = await req('PATCH', `/automations/${a.id}`, token, {
> 113:        name: cur.name, symbol: cur.symbol, indexes: newIndexes, conditions: newConditions,
> 117:    console.log(`\n✏️  id2 (id ${a.id}) GATEADA por fluxo (sniper). Fail-safe: FLOW nos indexes + stale<${MAX_AGE}ms + null-guard.`);
> 118:    console.log(`⚠️  threshold PROVISÓRIO (imbalance>${MIN}) — recalibrar com deep-research + logs/flow-capitulation.log.`);
> 119:    console.log(`Revert: remover o segmento "&& MEMORY['${KF}']..." da condition e tirar ${KF} dos indexes (ou re-rodar com outro FLOW_GATE_MIN).`);
> ```

## 🤖 Claude *(22:08:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"buyGate\\|flowGated\\|buyAllowed\\|\\.farm\\|\\.baseline\\|deriveGates\\|gates\\.\" /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js /home/gcrux-tradeux/tradeux/tradeux-agent/src/agent.js",
  "description": "Check FE and agent consumers of gate fields"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/agent.js:42:  (6) buyGate de acumulação liberado com regime=mixed: CORRETO (range E mixed são mean-reversion; condition viva = regime != bear E != trend) — não sugira "respeitar só range".
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js:411:                <div className="cx-line"><span className="l"><span className="cx-seal real" /> Gate acumulação BTC <span className="cx-flat" style={{ fontSize: '0.66rem' }}>(farm/baseline)</span></span><span className={`v cx-mono ${cpBtc && cpBtc.gates ? (cpBtc.gates.buyAllowed ? 'cx-up' : 'cx-down') : ''}`} title={cpBtc && cpBtc.gates ? cpBtc.gates.reason : ''}>{cpBtc && cpBtc.gates ? (cpBtc.gates.buyAllowed ? 'GO' : 'CAIXA') : '—'}</span></div>
> ```

## 🤖 Claude *(22:08:36)*

The ground-truth claims check out. Let me confirm two things: (1) the FE Cockpit only renders the BTC gate (so alt mislabeling is agent/MCP-surface only, not the panel), and (2) the SYMBOLS set in setup-farm vs the env default.

## 🤖 Claude *(22:08:38)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"SYMBOLS\\|RSI_LO\\|BTCUSDT\\|LTC\\|BNB\\|ADA\" /home/gcrux-tradeux/tradeux/backend/scripts/setup-farm.js | head -20",
  "description": "Confirm farm symbol set"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 25: *        FARM_SYMBOLS (CSV, default LTCUSDT,BNBUSDT,ADAUSDT), FARM_INTERVAL (1m),
> 26: *        FARM_RSI_LO (35), FARM_PROFIT (0.012), FARM_BUFFER (0.003), FARM_SIZE_MULT (2)
> 30:const SYMBOLS = (process.env.FARM_SYMBOLS || 'LTCUSDT,BNBUSDT,ADAUSDT').split(',').map(s => s.trim().toUpperCase()).filter(Boolean);
> 33:const RSI_LO = parseFloat(process.env.FARM_RSI_LO || '35');
> 131:    const buyCond = `MEMORY['${K(RSI_KEY_SUFFIX)}'].current<${RSI_LO} && MEMORY['${K('REGIME')}']!=='bear' && MEMORY['${K('REGIME')}']!=='trend'`;
> 147:    console.log(`# Setup FARM no-loss — ${SYMBOLS.join(', ')} | RSI<${RSI_LO} compra · lucro-alvo ${(PROFIT * 100).toFixed(1)}% · buffer ${(BUF * 100).toFixed(1)}% · size ${SIZE_MULT}×MIN_NOTIONAL${DRY ? '   [DRY-RUN: nada será aplicado]' : ''}`);
> 149:    for (const symbol of SYMBOLS) await setupSymbol(token, symbol);
> 152:    console.log(`Para ATIVAR (1 alt por vez, com gate): garanta o REGIME da alt (REGIME_SYMBOLS ou automação ativa)`);
> ```

## 🤖 Claude *(22:08:39)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"cpBtc\\|cockpit\\|gates\\.\\|buyAllowed\\|flowGated\\|symbol\" /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js | head -40",
  "description": "Check what the cockpit panel renders for gates"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 9:import './cockpit.css';
> 112:  const [gate, setGate] = useState({ symbols: {} });
> 113:  const [flow, setFlow] = useState({ symbols: {} });
> 118:  const [cockpit, setCockpit] = useState({ symbols: {} });
> 131:            if (Array.isArray(mt)) mt.forEach(t => put(t && t.symbol, t && (t.close ?? t.c)));
> 132:            else if (mt.symbol) put(mt.symbol, mt.close ?? mt.c);
> 158:        const r = await fetch(`${host}/api/v3/klines?symbol=${KL_SYMBOL}&interval=1m&limit=120`);
> 184:  // BRAIN snapshot (single source of truth): prefere o cockpitJob; klines client-side = fallback/render.
> 185:  const cp = cockpit || {};
> 187:  const cpBtc = (cp.symbols || {})[KL_SYMBOL] || null;
> 188:  const histB = (cpBtc && cpBtc.dist && cpBtc.dist.hist && Array.isArray(cpBtc.dist.hist.counts))
> 190:        counts: cpBtc.dist.hist.counts,
> 191:        maxc: Math.max(...cpBtc.dist.hist.counts, 1),
> 192:        step: cpBtc.dist.hist.binPct,
> 193:        BINS: cpBtc.dist.hist.counts.length,
> 194:        LIM: cpBtc.dist.hist.lim,
> 195:        n: cpBtc.samples,
> 196:        clearFee: cpBtc.dist.pHitBreakevenPct,
> 197:        medAbs: cpBtc.dist.medAbsMovePct,
> 198:        sd: cpBtc.dist.sigmaPct,
> 202:  const sigmaB = (cpBtc && cpBtc.dist && cpBtc.dist.sigmaPct != null) ? cpBtc.dist.sigmaPct : sigma;
> 203:  const mcBand = (cpBtc && cpBtc.mc) ? cpBtc.mc : null;
> 204:  const evNet = (cpBtc && cpBtc.ev && cpBtc.ev.netPct != null) ? cpBtc.ev.netPct : null;
> 214:  Object.keys(gate.symbols || {}).forEach(s => symset[s] = true);
> 215:  Object.keys(flow.symbols || {}).forEach(s => symset[s] = true);
> 216:  const symbols = Object.keys(symset).sort();
> 225:        <div className="cockpit">
> 228:            <div className="cx-brand"><b>TRADEUX</b><span>fable cockpit</span></div>
> 298:                <div className="cx-panel-title"><span><span className="cx-seal real" /> Tail · retornos 1m vs fee</span><span className="cx-src">{histB && histB.fromBrain ? '/analysis/cockpit (brain)' : 'klines → distribuição'}</span></div>
> 325:                      <div className="cx-note">Zona vermelha = move &lt; fee round-trip ({FEE_RT}%). A maioria das velas de 1m cai aí dentro — prova visual de por que scalping de 1m sangra taxa.{histB.fromBrain ? ' Distribuição computada pelo brain (cockpitJob).' : ''}</div>
> 334:                <div className="cx-panel-title"><span><span className="cx-seal real" /> Probability lattice (Galton)</span><span className="cx-src">{histB && histB.fromBrain ? '/analysis/cockpit (brain)' : 'velas 1m reais'}</span></div>
> 340:                <div className="cx-panel-title"><span><span className="cx-seal real" /> Monte Carlo · median fair</span><span className="cx-src">{mcBand ? '/analysis/cockpit (brain)' : 'σ realizada'}</span></div>
> 351:                  {symbols.length === 0
> 353:                    : symbols.map(s => {
> 354:                        const g = (gate.symbols || {})[s] || {};
> 355:                        const f = (flow.symbols || {})[s] || {};
> 375:                  {symbols.length === 0
> 377:                    : symbols.map(s => {
> 378:                        const g = (gate.symbols || {})[s] || {};
> 379:                        const f = (flow.symbols || {})[s] || {};
> ```

## 🤖 Claude *(22:09:27)*

Confirmed. The FE panel (`Cockpit.js:411`) only renders the BTC gate (`cpBtc.gates.buyAllowed`) and labels it explicitly "Gate acumulação BTC (farm/baseline)" — so the alt-mislabel was never visible in the human panel; it surfaced only through the MCP `buyGate` the agent reads per-symbol. The env default `BTCUSDT` matches the only flow-gated baseline (`setup-flow-gate.js:29` FLOW_SYMBOL default BTCUSDT, id2 only), and the alt FARM condition (`setup-farm.js:131`) has no flow clause. The diff's docstring is now accurate. Let me do a quick sanity check on the new reason-string logic for the stale/capitulation branches.

The logic is sound: for non-flow-gated symbols (alts), `buyAllowed = farm` and the reason short-circuits before the flow branches, noting capitulation as informational only. For BTC, the original baseline path is preserved. `doctrine:true` and `harvesterUngated:true` are intact, no money-path/HALT coupling. Here is my review.

---

**VEREDITO: APPROVE COM SUGESTÕES**

## Racional

A correção está certa e bem fundamentada. Confirmei a ground-truth no repo:

- `setup-farm.js:131` — a condition VIVA das alts (LTC/BNB/ADA, `FARM_SYMBOLS` em `setup-farm.js:30`) é `RSI<lo && REGIME!=='bear' && REGIME!=='trend'`. **Sem cláusula de fluxo.** Aplicar o filtro de fluxo às alts no cockpit MENTE: vetaria um dip que a automação viva FARIA.
- `setup-flow-gate.js:29,80` — o gate de fluxo (`imbalance>MIN` + stale-check) é adicionado **só** à id2, `FLOW_SYMBOL` default `BTCUSDT`. É o único módulo de acumulação flow-gated.
- Logo, o default `COCKPIT_FLOW_GATED_SYMBOLS=BTCUSDT` (`cockpitJob.js:84`) é o single-source correto e bate exatamente com a fonte da verdade.

A mudança é **read-only, zero blast radius**: `deriveGates` não emite ordem, `doctrine:true` e `harvesterUngated:true` preservados (`cockpitJob.js`, linha do `return`), nenhum acoplamento a money-path/`TRADING_HALT`. Mesmo se o HALT virasse, o efeito é alinhar a VIEW à automação real — direção segura. Reversível (1 arquivo de lógica + 3 campos no MCP `buyGate`).

Detalhe que reduz risco de regressão: o painel humano (`Cockpit.js:411`) só renderiza o gate **do BTC** (`cpBtc.gates.buyAllowed`, rótulo "Gate acumulação BTC (farm/baseline)") — o mislabel das alts nunca apareceu na UI; vazava só pelo `buyGate` por-símbolo que o **agente** lê via MCP (`tradeux-mcp/src/index.js:228`). Ou seja, o bug era real mas confinado à superfície do agente, e o fix é exatamente onde dói.

## Resposta às perguntas de design

**1. Abstração env-driven vs. derivar da condition viva.** Para v1, o `Set` env-driven é a escolha pragmática certa. Derivar flow-gatedness lendo a `condition` da automação no banco (parsear `MEMORY[...:FLOW]` na string) seria o "mais correto" porém **mais frágil**: acopla o cockpit ao schema/parsing de conditions, depende de `isActive`, e quebra o princípio de `doctrine:true` (gates = o que a estratégia FARIA, não o estado vivo). Reescrever doutrina a partir de estado vivo contradiz o próprio contrato do campo. O `Set` é simples, testável e desacoplado. Aprovo a abordagem.

**2. Default `BTCUSDT` e o risco de "alguém esquece o env".** Razoável hoje (id2 é o único). O risco real: se no futuro adicionarem um flow-gate a uma alt via `setup-flow-gate.js` (que aceita `FLOW_SYMBOL`) e esquecerem `COCKPIT_FLOW_GATED_SYMBOLS`, o cockpit volta a MENTIR (mostraria a alt como `farm` sem fluxo quando a automação passou a gatear por fluxo). O comentário em `cockpitJob.js:84` documenta o env, mas **não cria a ligação de descoberta no lugar onde o erro nasceria** — quem edita `setup-flow-gate.js` não vê o aviso. Isso é o nice-to-have abaixo.

## Must-fix
Nenhum. Mergeável como está.

## Nice-to-have
- **Discoverability cruzada (o ponto mais valioso):** adicionar 1 linha de comentário em `backend/scripts/setup-flow-gate.js` (perto do `SYMBOL`/`KF`, linha ~29-30) avisando: *"ao gatear fluxo de uma NOVA alt, atualizar também `COCKPIT_FLOW_GATED_SYMBOLS` senão o cockpit/agente reportam a alt como sem-fluxo (doutrina mente)."* É onde o futuro editor olha; o comentário só no cockpit não fecha o loop.
- O `flowGated` no `buyGate` do MCP é redundante com `farm`/`baseline` já expostos (o agente consegue inferir), mas custa nada e deixa a intenção explícita — ok manter.

## Meta-pergunta (a mais importante) — recomendação: PARAR de refinar; declarar doutrina-aproximada

Este é o **4º** fix de acurácia de VIEW nesta sessão (freshen, mixed-label, prompt-consolidation, agora alt-flow), todos disparados pelo agente sondando o cockpit. Isso é um sinal: cada fix torna o painel mais "verdadeiro" módulo-a-módulo, mas o cockpit é por construção `doctrine:true` — uma **aproximação da doutrina**, não o gate vivo (que mora na `condition` no banco, possivelmente `isActive=0`). Perseguir paridade 1:1 com cada condition de automação é reimplementar o motor de regras dentro de uma view read-only — custo crescente, e cada nova automação reabre a divergência.

Recomendo, **depois de mergear este fix** (ele corrige uma mentira direcional concreta, vale a pena):
1. Marcar a superfície de gates explicitamente como **"doutrina aproximada — gate VIVO = condition da automação no banco"** no `reason`/no `buyGate` do MCP e no prompt do agente. O `doctrine:true` já existe no payload; falta o agente/painel **renderizar** esse disclaimer em vez de tratar o gate como verdade.
2. Para acurácia real per-módulo, a fonte deve ser a `condition`/`isActive` da automação (um endpoint que lê o banco), não a doutrina derivada — mas isso é outro produto. Enquanto não existir, declarar a doutrina como aproximada e **parar de caçar divergências** uma a uma.

Em resumo: aprovar este (corrige direção errada), e então **congelar o refino de acurácia da doutrina** atrás de um disclaimer claro, em vez de transformar o cockpit num espelho exato das conditions.

## Decisão de merge
- **APPROVE COM SUGESTÕES** — mergear via PR (não direto-a-master), como `gcrux-tradeux`/root com a chave do `ubuntu` + chown de `.git` de volta.
- Sem condições bloqueantes. O nice-to-have do comentário em `setup-flow-gate.js` pode entrar no mesmo PR (1 linha) ou em follow-up.
- Tratar a recomendação meta (disclaimer "doutrina aproximada" + parar o refino) como item de doutrina/produto separado, não como blocker deste diff.

Arquivos relevantes: `/home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js`, `/home/gcrux-tradeux/tradeux/tradeux-mcp/src/index.js`, `/home/gcrux-tradeux/tradeux/backend/scripts/setup-farm.js`, `/home/gcrux-tradeux/tradeux/backend/scripts/setup-flow-gate.js`, `/home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js`, `/home/gcrux-tradeux/tradeux/tradeux-agent/src/agent.js`.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-16 - agent-aae893e38c8c9d479]]
> * **Próxima Sessão**: [[2026-06-16 - agent-ab2634bc8254c5d31]]
%% --- TIMELINE END --- %%

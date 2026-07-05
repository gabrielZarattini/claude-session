# Session agent-ae6cf60a3b1fcceb1
**Date:** 2026-07-05 | **Session ID:** `agent-ae6cf60a3b1fcceb1`

---

## 👤 User *(17:59:46)*

Revise uma mudança SÓ de frontend (read-only, sem backend/money-path) no cockpit do TradeUX, repo /home/gcrux-tradeux/tradeux. Veja `git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' diff -- frontend/`. Dois arquivos:

1. `frontend/src/private/Cockpit/cockpit.css`: adicionada classe `.cx-row-2` (grid 1fr/1fr + colapso responsivo em 1100px) e estilos do HUD (`.cx-hud-grid/.cx-hud-tile/.cx-hud-k/.cx-hud-v`, `.cx-decision` + variantes buy/sell/hold/wait/ready/halt, `.cx-badge`).
2. `frontend/src/private/Cockpit/Cockpit.js`: (A) os dois painéis "Paper · Estratégias" e "Paper Trilhas (Trend)" foram mesclados numa única `<div className="cx-row-2">` (antes eram dois `<div className="cx-row">` separados) → lado a lado. (B) novo widget "Análise da vela ao vivo (HUD)" (ROW 7) que reusa consts component-level (`cndBig`, `marks`, `klive`, `btcWs`, `cpBtc`, `cp`, `selSym`, `klErr`, `_rsi`, `_buyTh`, `_sellTh`) + helpers (`num`, `fmtPct`, `dirClass`, `simDecision`) pra mostrar candle SVG + decisão simulada + sinais da vela + grid de indicadores (RSI/regime/fluxo/gates/EV) + últimos sinais de `cp.patterns.recent`.

O `vite build` JÁ passou (imagem tradeux-frontend Built). Foque em:
(a) RUNTIME — algum acesso que CRASHA a página do cockpit se um campo vier null/undefined/vazio? Ex.: `cpBtc=null` (símbolo sem dados), `cp.patterns` ausente, `klive` null, `cndBig` null, `sig/g/fl/ev` vazios, `fl.imbalance` null em `fl.imbalance < 0`. Confirme que os guards (`cpBtc || {}`, `sig=s.signals||{}`, `cndBig ? ... : empty`, `snow`/`recent` com defaults) cobrem tudo. Verifique lendo o Cockpit.js atual.
(b) A estrutura JSX ficou BALANCEADA após a mescla dos painéis (as `<div>` de cx-row/cx-panel fecham certo; o `cx-grid` não quebrou)? 
(c) A escala do candle reusado (`sc = 200/cndBig.H`, cndBig tem H=440) desenha certo no viewBox 200?
(d) `simDecision(selSym, cp)` retorna sempre `{act,cls,head,reason}` (sem branch que retorne undefined)?

Veredito PASS / PASS COM RESSALVAS / FAIL com achados por severidade. É o site live — seja rigoroso sobre crash de runtime.

## 🤖 Claude *(17:59:48)*

Vou carregar o contexto e revisar a mudança.

## 🤖 Claude *(17:59:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat /home/gcrux-tradeux/HANDOFF.md 2>/dev/null | head -100; echo \"=== CLAUDE.md ===\"; cat /home/gcrux-tradeux/tradeux/CLAUDE.md 2>/dev/null | head -60",
  "description": "Load HANDOFF and CLAUDE context"
}
```

## 🤖 Claude *(17:59:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' diff --stat -- frontend/; echo \"=== FULL DIFF ===\"; git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' diff -- frontend/",
  "description": "Show frontend diff stat and full diff"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> # TradeUX — HANDOFF (single source of truth)
> 
> > ShakeHands continuity doc. `/handson` reads this FIRST. Newest record at the bottom.
> > Project: **TradeUX** — Beholder-based multi-coin Binance Spot bot + LLM agent (**mainnet/testnet dual-env**).
> > Updated: **2026-06-29** · Phase: **GO-LIVE MAINNET — 🔴 LIVE (`halted=false`) · PARADO-MAS-ARMADO** (capital parqueado como combustível do bull; regime BEAR → supervisor NO-OP) · `Vivo==master==origin==78515ae` · ⚠️ runtime não-git: `.env FLOW_NOTIFY_ENABLED=false` + `AGENT_HEARTBEAT_STALE_MS=2700000` + **`AGENT_HEARTBEAT_ENABLED=false` (agente LLM PAUSADO p/ parar consumo OpenRouter — `docker compose stop agent`; religar no flip)**; `tradeux-agent/.env INTERVAL=900000`+`MAX_ROUNDS=10` · ver SEAL 2026-06-29 no rodapé · *(linha histórica abaixo)* · **Canary FARM-ONLY** (vendas no-loss id10/12/14 — **AGORA FUNCIONAM**; compras off) · **SESSÃO 21/jun (maratona): incidente Earn auto-subscribe diagnosticado+resolvido + 4 bugs corrigidos/gated/deployados** → `c6d0853` (dailyCap conta `LD*` do Earn = fim do HALT-falso), `457e25a` (silencia PUSH `[PAPER]` + alerta Telegram em falha real), **`fb932a1` (venda do Farm EDGE→LEVEL-trigger = 1ª saída no-loss do Farm a EXECUTAR no mainnet)** → **LTC vendido +$0,49** (ordem 264 @ $44,54, FARM_DCA→0, equity **$149,39**) · ⚠️ **runtime não-git (reaplicar se reset):** `.env MAX_ORDER_NOTIONAL_USDT=25→50` (band-aid: o teto bloqueava a VENDA de $40), DB `monitors`#2 `*:BOOK isActive=1` · proteções: cap diário −5%, teto **$50/ordem**, Farm $25/símbolo, riskGuard, pânico, painel de grupos · Meta: **realista ≈ flat com ~$149** · Vivo==master==origin==**`6cec694`** (re-revisão de design 2026-06-22 **100% ZERADA** — só RBAC=DEFER; agente caiu por toggle ZDR do OpenRouter e VOLTOU; ver SEAL 2026-06-24 no rodapé)
> 
> > 🟢 **ATUALIZAÇÃO 2026-06-21 (cont. — MARATONA 2): suíte de simulação money-path + D3 deployado + paper-validate das 3 alavancas.** Estado segue **🔴 LIVE (`halted=false`), Canary FARM-ONLY**, equity ~$149, HALT intacto o tempo todo. 7 commits (todos gate QA+TL, CI verde, 2 deploys de backend): **(1) SUÍTE DE SIMULAÇÃO** (`backend/scripts/sim/`, 6 arquivos, **90 asserts**, no CI) — achou+corrigiu **3 bugs REAIS latentes**: `getStableConversion` não-exportada (taxa BNB sumia do P&L → `854bab5` estava INERTE), `placeOrder:551` precedência (erro virava `undefined` no Telegram), `placeOrder:573` `order.type` (stopPrice não persistia). **(2) D3 DEPLOYADO** (`5c83c31`): `tradeux_get_cockpit` traz `status.groups` (ATIVO por grupo) + doutrina GATE≠ATIVO (agente para de dizer "aguardando golden cross p/ comprar" com grupo parado; valida no próx. ciclo pós-429). **(3) PAPER-VALIDATE: 3 alavancas LIVE em paper** (grupo paper **40/40**): MR15 (mean-reversion 15m), Slopegate (trend só entra se `TREND_SLOPE_1h!='down'` — sinal novo no regimeJob), Farmnl (Farm no-loss REAL: paperEngine publica `FARMNL_TARGET`=custo×1.012). **Vivo==master==origin==`2c55fe0`.** ⚠️ trilhas paper são RUNTIME — reaplicar pós-`make nuke`: `setup-paper-mr15.js` + `setup-paper-levers.js`.
> 
> > 🟢 **ATUALIZAÇÃO 2026-06-22 (MARATONA 3): hardening de risco + Farm + RE-REVISÃO de design (workflow `wyzo1zfr3`, 49 agentes).** **8 commits** (todos gate QA+TL + deploy + smoke; vivo==master==origin==**`5edf856`**), 🔴 LIVE `halted=false` o tempo todo, Canary FARM-ONLY, equity **~$149 intacta**. **Risk-guard:** %-teto de COMPRA 20% (`fe06c74`) + rede anti-runaway na VENDA 3×equity (`d9f0dc5`) + `riskCaps` no cockpit (`6b9b97b` — + FIX do MCP que DROPAVA `groups`/`paper`: a D3 e o paper-no-cockpit estavam **INERTES** pelo caminho do agente!) + harness MCP (`03f6757`). **Farm:** `loadFarmSellingLocks` no boot (`43e8b74`, pré-req de escalar). **RE-REVISÃO:** 3 HIGH conhecidos REBAIXADOS (H1 useTestnet→MEDIUM, H2 qty-bruta→LOW, H3 Earn→HIGH-só-sizing); **2 HIGH reais ATACADOS:** withdraw-lock (`c6f67ef`, HALT+frase+allowlist no BOUNDARY, cobre HTTP **e** automação) + getAveragePrices isTestnet (`39dfa88`) + earnRedeemJob H3 (`5edf856`, **DRY-RUN gated-off — NÃO fixa até `EARN_AUTO_REDEEM=true`**). Relatório: `~/RESEARCH-design-review-2026-06-22.md`. ⚠️ **runtime não-git (reaplicar pós-`make nuke`):** `.env` `MAX_ORDER_NOTIONAL_USDT=100` · `MAX_ORDER_PCT_EQUITY=0.20` · `MIN_ORDER_NOTIONAL_FLOOR=12` · `MAX_SELL_EQUITY_MULT=3` · `WITHDRAW_ADDRESS_ALLOWLIST=` (vazio=fail-closed).
> 
> > 🔴 **ATUALIZAÇÃO 2026-06-20 — NÃO ESTÁ MAIS CONGELADO:** o dono LIBEROU o floor pela UI → trading REAL ON (`halted=false`). Canary **FARM-ONLY** (só as VENDAS do Farm armadas — saída no-loss dos lotes; COMPRAS off). Equity intacta ~$148,75 (USDT↔LTC, sem perda). SEMPRE confira `GET /system/halt` no início da sessão. **O bloco 🛑 abaixo (2026-06-15) é HISTÓRICO** — descreve o estado CONGELADO, já SUPERADO.
> 
> > 🛑 **LEIA ANTES DE TUDO (2026-06-15):** o sistema está em **MAINNET REAL** (`settings.useTestnet=0`, ~$150 USDT) e **CONGELADO** (`TRADING_HALT=true` no `.env` → nada negocia; é o kill-switch novo no `exchange.js`). Money-path foi blindado (`96915e0`) e o bug P0 do Farm Sell foi corrigido (`c163112`). **DESCOBERTA CRÍTICA: o harvester está MORTO no mainnet** (o edge de −3% era arbitragem testnet-vs-mainnet; no mainnet o book do bot É o FAIR). O ÚNICO edge real é o **Trend** (pequeno, mensal). **Antes de descongelar:** (1) trava `FARM_SELLING` (follow-up); (2) dono confere saque-OFF+IP da chave Binance; (3) decidir re-design do harvester. Detalhes nos SEALs de 2026-06-15 (fim do doc) + memória `tradeux-mainnet-go-live`. **2026-06-16:** Cockpit Intelligence read-only NO AR (brain computa analytics 1m + agente lê/reporta; commit `1660871`) — a brain reporta **EV −0,16% / pHit 0,6%** (scalp 1m é −EV, dado real). Fix do **−1013** no `calcQty` + template Trend ×3 (commit `2528a5d`). **Auditoria adversarial independente** confirmou 7 achados p/ o descongelamento → ver SEAL 2026-06-16. ⚠️ O "vídeo viral Fable 5/Polymarket 205x" do X é **golpe de referral** — NÃO clicar/depositar.
> 
> ## ⚡ FIRST ACTION FOR NEXT AGENT
> 0. 🏗️ **ARQUITETURA FARM-AND-FUNNEL COMPLETA E NO AR** (sessão 2026-06-08): **15 automações ativas** — Farm no-loss +
>    Trend SMA50/200 nas alts **LTC/BNB/ADA** (id 9-20) + id2/id6/id7 do BTC; **funil em SHADOW**; id3 pausada. Coordenação
>    por regime (farm `!=trend`, trend `!=bear`). Validada por backtest (`backend/scripts/backtest-farm-funnel.js`) **e ao
>    vivo**. Doc: `docs/STRATEGY-farm-funnel.md`. Memória `tradeux-farm-funnel-backtest`. **Hoje MERCADO=BEAR → tudo INERTE/protegido.**
>    ⏰ **GATILHO (pedido do dono): QUANDO O REGIME SAIR DO BEAR / mercado propício → RETOMAR:** Fase 4 = **funil AO VIVO**
>    (ligar a compra de BTC com o lucro real do farm, DEPOIS de observar o farm lucrar e calibrar o baseline com dado real);
>    Fase 5 = **calibração** (5m + seleção de alts, SOL ruim no farm + switch macro fino — SMA-slope no regimeJob). Ver §5 do
>    doc. **Checar o regime no boot:** `GET /analysis/regime-status` ou `logs/regime.log` — se != bear, é a hora.
>    ✅ **ARMADOR DA FASE 4 NO AR** (commit `af22e7a`, 2026-06-09): o farm/trend já retomam sozinhos na saída do bear (gate
>    runtime). O `regimeJob` agora detecta a borda `bear→não-bear` do macro (`FASE4_MACRO_SYMBOL`=BTCUSDT) → dispara
>    `funnelJob.armFase4Observation()` = **notifica (telegram) + pré-arma o funil shadow (baseline) + janela densa de 4h**
>    capturando o dado pra ESCREVER a Fase 4 (caixa USDT, reserva, lucro-desde-saída, escoamento; tag `[fase4-observe]` em
>    `logs/funnel.log`). **NÃO compra** — a Fase 4 live-buy ainda não existe (money-path, gate). Quando o telegram avisar
>    "🔔 [FASE4] Saída do BEAR", as 4h de captura bastam pra calibrar+escrever a compra ao vivo (com gate QA/TL). Memória `tradeux-farm-funnel-backtest`.
>    ✅ **TELEGRAM FUNCIONA DE VERDADE desde 2026-06-10** (a raiz era chatId=username do bot → fix; `c3463ac` notifica TODAS
>    as ordens + canal do agente `tradeux_notify_owner`) — o aviso "[FASE4]" CHEGA no dono. E o **HARVESTER está em size ×4**
>    (`0b94b3a` reconcile-on-boot fechou a última dívida; janela de observação 2-3 dias → ×8). Memória `tradeux-telegram-notifications` + `tradeux-harvester-experiment`.
>    ✅ **AGENTE RECALIBRADO (`12ceabe`)** pós-incidente de spam: doutrina POR MÓDULO (harvester=no-loss; **id7 corta perda
>    POR DESENHO** — não tratar como bug), pt-BR obrigatório, kickoff injeta histórico de notificações (anti-repetição) +
>    cap mecânico 2/ciclo. NÃO reescrever a doutrina sem reler `tradeux-telegram-notifications` (a regra "só vende com lucro"
>    é literal SÓ pro harvester; gate de lucro na id7 = mudança de estratégia REFUTADA pelo backtest — não fazer via prompt).
> 1. **Backlog de PRs ZERADO** — modelo **trunk-based** (commit direto no `master` + push via token HTTPS).
> 2. 🎯 **META MUDOU: de 500k para +3 BTC (testnet)** — validar uma estratégia que faz +3 BTC; se 3, calibrar p/ 10+.
>    Ver memória `tradeux-agent-500k-validation` (pivot) e `~/STRATEGY-3BTC-assessment.md`.
> 3. ✅ **OCO wiring no Beholder COMMITADO E NO AR** (commit `aa3f7f7`): template `type:'OCO'` → SELL protetiva
>    (TP LIMIT_MAKER + SL STOP_LOSS_LIMIT), persiste 2 pernas c/ `orderListId` (migration), `listStatus` reconcile,
>    guard anti-empilhamento, cancel no delete da automação. Gate QA+TL + testnet + CI verde.
> 4. ✅ **P&L mensurável + painel** (`d74fac0` net/avgPrice no insert de fills — ~74% das MARKET tinham net NULL;
>    `9a5f989` Reports default USDT + end-date inclusivo + **leitura em BTC** "≈ X BTC"; `1fa6235` **painel
>    Intelligence**: regime de mercado + KPIs do agente no UI). Todos com CI verde + validados no navegador.
> 5. ✅ **ENABLER Nº1 ENTREGUE & NO AR** (commit `30e6566`): `regimeJob` grava `MEMORY['<sym>:REGIME']`
>    (string, via `updateMemory(...,executeAutomations=false)` = gate passivo) a cada 5min; `regimeService`
>    compartilha fetch+classify+cache com o endpoint. **id2 (BUY) GATEADA ao vivo** (PATCH): condition
>    `... && MEMORY['BTCUSDT:REGIME']!=='bear'` + `BTCUSDT:REGIME` nos indexes (fail-safe). id3 (SELL) intocada.
>    Hoje BTC=bear → id2 **não compra** (validado). Gate QA+TL + testnet + lógica 9/9. ⚠️ ver "id2 gate" em
>    Technical debt (NÃO é seedado → reaplicar após `make nuke`/reset).
> 6. ✅ **Classificador c/ histerese ENTREGUE** (commit `774ae42`): bandas entra/sai (bear >0.60/sai <0.45;
>    trend 25/22; range 20/23), `prev` carregado pelo job. Gate da id2 mais estável e fail-safe (bear pegajoso).
>    ±DI descartado por dados (piorava); MTF desnecessário (histerese já vence). Ganho é risco-ajustado de
>    CARTEIRA, não alfa no BTC (ver task table). Observabilidade do gate ✅ (commit `e6c10dc`, card "Regime Gate" no
>    painel). Calibração RSI ✅ (commit `0b1e949`): **RSI 25/75 aplicado na id2/id3** (domina 30/70 em retorno+drawdown
>    em 1h E 1m). ✅ **Trend Following (SMA 50/200) ATIVADO** (commit `453c7d6`, gate QA PASS + TL APPROVE, CI verde):
>    id6/id7 ativas + coordenação id2/id3 `!=trend` + **LIMIT marketável** (buffer 0.3%) + **persistência de cross** (`regimeStates`).
>    ⏳ **NEXT**: (a) **observar 1 golden→death real** (`logs/A:6.log`/`A:7.log`) antes de calibrar o size (id6=3× MIN_NOTIONAL);
>    (b) observar id2/id3 coordenadas ao longo do tempo; (c) ✅ **risco nº1 RESOLVIDO** (commit `e5ef595`: id7 usa `TREND_QTY`,
>    não mais `LAST_ORDER`) — ⚠️ porém `TREND_QTY` é **volátil** (não persiste) → **persistir ANTES de escalar o size**;
>    (d) opcional: hook de SIGTERM p/ stop().
> 7. Sanity no `/handson`: stack up na 8090 (**4 containers: db/backend/frontend/agent**), id2/id3 (coordenadas `!=trend`) + id6/id7 (trend) **ATIVAS**, símbolos
>    synced, `GET /beholder/memory/BTCUSDT/REGIME` => `"bear"`. Trend ATIVO mas **inerte** agora (bear + above=false → sem disparo).
> 
> ## 🏁 Current state (what's live)
> - **Stack DEPLOYED & healthy**: `tradeux-db/backend/frontend/agent` na 8090 (CloudPanel+Cloudflare).
>   `https://tradeux.gcrux.com` → 200. Backend recriado com deps novas (twilio6/form-data4), boot limpo.
> - **Agente LLM SUPERVISIONADO** (commit `e97a85a`): roda como serviço `agent` no compose (restart:unless-stopped,
>   `user:1011:1013`, DRY/ALLOW_TRADING=false, OpenRouter nemotron `:free`); grava o journal que alimenta os KPIs do card
>   "Agent (LLM)" em `/intelligence`. Antes era CLI manual → parava sem religar (ficou 5 dias parado). Religar/parar:
>   `docker compose up -d agent` / `docker compose stop agent`.
> - **Modelo de trabalho SELADO** (ver memória `tradeux-orchestration-model`): Claude é o ORQUESTRADOR —
>   agentes worker implementam, QA+Tech-Lead são o gate; Claude **aprova OU devolve** e sobe pra prod.
>   Sem PR-por-mudança. Gate proporcional: trivial→direto; hot-path/migration/segredo/dinheiro→gate.
> - **Token GitHub**: em `~/tradeux/.env` como `GITHUB_TOKEN_API` (gitignored). Merge/push via API/HTTPS.
>   ⚠️ é um PAT clássico admin-scope — trocar por fine-grained quando der (hardening).
> - **PRs**: #10 (fix white-screen) e #11 (auto-sync) **MERGEADOS**; #1-7 (dependabot frontend)
>   **fechados** (obsoletos pós-Vite); #9 (BYOK) **superseded** por commit direto; #12-15 (auto-PRs
>   do Dependabot) **fechados como deferidos** (#12/#14 bundlam node-binance-api core → task; #13/#15
>   vite/esbuild dev-only). **0 PRs abertos** — mas o Dependabot REABRE auto-PRs pras 6 moderate
>   deferidas; fechar-como-deferido até o bump do node-binance-api / vite resolver na raiz.
> - **Segurança**: backend runtime **8 → 2 moderate** (0 crit/0 high) após node-binance-api 1.x + `@sendgrid` 6→8
>   (mata o `request`) + remoção do override form-data (commit 063df19). Restam 2 NÃO-exploráveis (`sequelize→uuid@8.3.2`,
>   path `buf` não usado). O Dependabot pode mostrar mais (soma as 2 árvores incl. dev). Ver SECURITY.md.
> - **BYOK**: chaves Binance opcionais no boot (seeder `|| ''` + setup.sh) — commit `9b91416`.
> - **Backtest + regime**: harness walk-forward (`backend/scripts/backtest.js`) + detector
>   (`backend/src/utils/regimeClassifier.js`) + relatórios (`backend/backtest-results/`). Ver Validation.
> - **Baseline**: RSI 30/70 (BTCUSDT) — automations `id2`(buy<30)/`id3`(sell>70) **ACTIVE/armadas**.
> - **Regime gate AO VIVO** (commit `30e6566`): `regimeJob` grava `MEMORY['BTCUSDT:REGIME']` (mainnet 1h, 5min);
>   **id2 (BUY) gateada** `... && MEMORY['BTCUSDT:REGIME']!=='bear'` + `BTCUSDT:REGIME` nos indexes (fail-safe);
>   id3 (SELL) sem gate (saída p/ caixa sempre liberada). Hoje BTC=**bear** → id2 não compra.
> - **LLM agent**: `tradeux-agent`+`tradeux-mcp`, OpenRouter `nemotron-3-super-120b:free`, `ALLOW_TRADING=false`.
> 
> ## 📋 Task state
> | Item | Status |
> |---|---|
> | Deploy stack / 502 / white-screen / auto-sync symbols | ✅ (mergeados #10/#11) |
> | BYOK chaves opcionais no boot | ✅ (commit direto) |
> | Segurança: critical + 8 high (twilio/form-data) | ✅ (28→6; gate QA+TL) |
> === CLAUDE.md ===
> # CLAUDE.md
> 
> This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
> 
> ## What this is
> 
> TradeUX is a multi-coin trading bot for **Binance Spot** with a web UI. The decision
> core is based on **Beholder 2.1** (LuizTools' course) and is packaged to deploy in one
> command with Docker. Three milestones live in one monorepo:
> 
> - **`backend/`** + **`frontend/`** — the running product (manual operation). Node/Express
>   + Sequelize + WebSocket API, React UI served by nginx.
> - **`tradeux-mcp/`** — an MCP server that exposes the backend's REST API as tools.
> - **`tradeux-agent/`** — an LLM agent (Anthropic or OpenRouter) that drives the bot
>   through `tradeux-mcp`, with guardrails and an evaluation journal.
> 
> ## Architecture (the big picture)
> 
> ### Backend — the Beholder "brain" (`backend/src/`)
> The backend is more than a CRUD API; it runs a stateful trading engine. Entry point is
> `server.js`, which boots everything in order: load default settings → init the Beholder
> brain with active automations → start the scheduler → start Express → attach WebSocket →
> init the exchange/event monitor. The moving parts:
> 
> - **`beholder.js`** — the in-memory engine. Holds `MEMORY` (live market state per
>   symbol/index, e.g. MINI_TICKER, BOOK) and `BRAIN` (compiled automations indexed by the
>   memory keys they react to). `updateMemory()` is called on every market tick and returns
>   the automations whose conditions just fired. This is mutable module-level state guarded
>   by `LOCK_*` flags — treat it carefully; it is the hot path.
> - **`app-em.js`** (event/exchange monitor) — subscribes to Binance streams via
>   `utils/exchange.js`, feeds ticks into `beholder.updateMemory`, and broadcasts results
>   to UI clients. `app-ws.js` is the WebSocket server (JWT-authenticated via `?token=` in
>   the URL). `app.js` is the Express app; `agenda.js` runs scheduled automations.
> - **Layering**: `routers/` → `controllers/` → `repositories/` (Sequelize) → `models/`.
>   Most domain concepts come in this full stack: settings, symbols, orders, monitors,
>   automations, orderTemplates, withdrawTemplates, plus beholder/exchange/logs. When adding
>   a feature, follow this chain end to end.
> - **`utils/`** — `exchange.js` (node-binance-api wrapper, the Binance boundary),
>   `crypto.js` (AES-256 for API-key storage — needs `AES_KEY` exactly 32 chars),
>   `indexes.js` (technical-indicator calc + memory index keys), plus notification channels
>   (email, sms, telegram, push).
> 
> ### MCP server (`tradeux-mcp/src/`)
> A thin **stdio** MCP server. `api.js` is an HTTP client to the backend that logs in once
> (`/login`), caches the JWT, and re-auths on 401. `index.js` registers ~25 tools named
> `tradeux_*` (read: `get_wallet`, `get_price`, `get_analysis`, `get_memory`,
> `list_orders`…; write: `place_order`, `cancel_order`, `start_automation`,
> `stop_automation`…). It needs `TRADEUX_API_URL`, `TRADEUX_EMAIL`, `TRADEUX_PASSWORD`.
> 
> ### Agent (`tradeux-agent/src/`)
> `index.js` is the CLI (`--check` lists MCP tools and exits; `--once` runs one cycle;
> no flag = loop every `TRADEUX_AGENT_INTERVAL`). `mcpClient.js` spawns `tradeux-mcp` over
> stdio (default path `../../tradeux-mcp/src/index.js`) and converts MCP tools to the model
> tool format. `agent.js` runs the decision loop: a stable `SYSTEM_PROMPT` holding the
> trading persona + **guardrails**, then up to `MAX_TOOL_ROUNDS` of tool calls, recording
> everything to the journal. `providers/` abstracts Anthropic vs OpenRouter (selected by
> `TRADEUX_AGENT_PROVIDER`). **Writes are gated by `TRADEUX_ALLOW_TRADING` (default off).**
> 
> ## Deployment model (decided)
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>  frontend/src/private/Cockpit/Cockpit.js  | 94 ++++++++++++++++++++++++++++++--
>  frontend/src/private/Cockpit/cockpit.css | 23 +++++++-
>  2 files changed, 111 insertions(+), 6 deletions(-)
> === FULL DIFF ===
> diff --git a/frontend/src/private/Cockpit/Cockpit.js b/frontend/src/private/Cockpit/Cockpit.js
> index e9a2988..61b9de6 100644
> --- a/frontend/src/private/Cockpit/Cockpit.js
> +++ b/frontend/src/private/Cockpit/Cockpit.js
> @@ -792,8 +792,8 @@ function Cockpit() {
>                </div>
>              </div>
>  
> -            {/* ROW 5 — Paper Engine (research, sem risco) */}
> -            <div className="cx-row">
> +            {/* ROW 5+6 — Paper: Estratégias | Trilhas (Trend) lado a lado (1fr/1fr) */}
> +            <div className="cx-row-2">
>                <div className="cx-panel glow">
>                  <div className="cx-panel-title"><span><span className="cx-seal real" /> Paper · Estratégias (research, sem risco)</span><span className="cx-src">/analysis/cockpit · paper</span></div>
>                  {(() => {
> @@ -818,10 +818,8 @@ function Cockpit() {
>                    );
>                  })()}
>                </div>
> -            </div>
>  
> -            {/* ROW 6 — Paper Trilhas (Trend) — teste ao vivo (pedido do dono) */}
> -            <div className="cx-row">
> +              {/* coluna 2: Paper Trilhas (Trend) — teste ao vivo */}
>                <div className="cx-panel glow">
>                  <div className="cx-panel-title"><span><span className="cx-seal real" /> Paper Trilhas (Trend) — teste ao vivo</span><span className="cx-src">/analysis/cockpit · paper + symbols</span></div>
>                  {(() => {
> @@ -870,6 +868,92 @@ function Cockpit() {
>                </div>
>              </div>
>  
> +            {/* ROW 7 — Análise da vela ao vivo (HUD): os "pensamentos" da vela atual */}
> +            <div className="cx-row">
> +              <div className="cx-panel glow">
> +                <div className="cx-panel-title"><span><span className="cx-seal real" /> Análise da vela ao vivo (HUD) — {selSym.replace('USDT', '')}</span><span className="cx-src">WS preço + /analysis/cockpit · segue o seletor</span></div>
> +                {(() => {
> +                  const s = cpBtc || {};
> +                  const sig = s.signals || {}, g = s.gates || {}, fl = s.flow || {}, ev = s.ev || {};
> +                  const dec = simDecision(selSym, cp);
> +                  const fmtPx = (v) => { const n = num(v); return !isFinite(n) ? '—' : n >= 100 ? n.toFixed(2) : n >= 1 ? n.toFixed(3) : n.toFixed(5); };
> +                  const kl = (klive && klive.length) ? klive[klive.length - 1] : null;
> +                  const liveP = (btcWs != null && !isNaN(btcWs)) ? btcWs : (kl ? kl.c : null);
> +                  const rsi1 = sig.rsi1m != null ? sig.rsi1m : (_rsi.length ? _rsi[_rsi.length - 1] : null);
> +                  const rsi15 = sig.rsi15m;
> +                  const chg = (kl && kl.o) ? ((kl.c - kl.o) / kl.o) * 100 : null;
> +                  const snow = [];
> +                  if (rsi1 != null && rsi1 < _buyTh) snow.push({ t: `RSI 1m ${rsi1.toFixed(0)} < ${_buyTh} · sobrevenda`, cls: 'cx-up' });
> +                  if (rsi1 != null && rsi1 > _sellTh) snow.push({ t: `RSI 1m ${rsi1.toFixed(0)} > ${_sellTh} · sobrecompra`, cls: 'cx-down' });
> +                  if (fl.toxicity != null && fl.toxicity >= 0.6) snow.push({ t: `fluxo extremo · ${fl.imbalance < 0 ? 'venda' : 'compra'} agressora (tox ${fl.toxicity.toFixed(2)})`, cls: fl.imbalance < 0 ? 'cx-down' : 'cx-up' });
> +                  if (sig.trendCross === 'golden') snow.push({ t: 'golden cross · compra de trend', cls: 'cx-up' });
> +                  if (sig.trendCross === 'death') snow.push({ t: 'death cross · venda protetiva', cls: 'cx-down' });
> +                  if (g.regime === 'trend') snow.push({ t: 'regime TREND · TrendState posicionado', cls: 'cx-up' });
> +                  const recent = (cp.patterns && Array.isArray(cp.patterns.recent) ? cp.patterns.recent : []).filter((r) => r.symbol === selSym).slice(0, 5);
> +                  const tile = (k, v, cls) => (<div className="cx-hud-tile" key={k}><span className="cx-hud-k">{k}</span><span className={`cx-hud-v cx-mono ${cls || ''}`}>{v}</span></div>);
> +                  const sc = cndBig ? 200 / cndBig.H : 1;
> +                  return (
> +                    <React.Fragment>
> +                      {cndBig
> +                        ? <svg className="cx-candle" viewBox={`0 0 ${cndBig.W} 200`} preserveAspectRatio="none" aria-label={`Candles 1m do ${selSym} com sinais ao vivo`}>
> +                            {[0.25, 0.5, 0.75].map((gg, i) => <line key={i} className="grid" x1="0" x2={cndBig.W} y1={200 * gg} y2={200 * gg} />)}
> +                            {cndBig.candles.map((cc, i) => {
> +                              const last = i === cndBig.candles.length - 1;
> +                              return (<g key={i}>
> +                                <line className={cc.up ? 'wick-up' : 'wick-down'} x1={cc.wx} x2={cc.wx} y1={cc.wy1 * sc} y2={cc.wy2 * sc} />
> +                                <rect className={cc.up ? 'body-up' : 'body-down'} x={cc.x} y={cc.by * sc} width={cc.bw} height={Math.max(1, cc.bh * sc)} style={last ? { stroke: 'var(--cx-cyan)', strokeWidth: 1 } : null} />
> +                              </g>);
> +                            })}
> +                            {marks.map((m, i) => {
> +                              const c = cndBig.candles[m.i]; if (!c) return null;
> +                              if (m.type === 'buy') { const y = c.wy2 * sc + 6; return <polygon key={'m' + i} className={`cx-mark buy ${m.armed ? 'armed' : 'gated'}`} points={`${c.wx - 4},${y + 6} ${c.wx + 4},${y + 6} ${c.wx},${y}`}><title>{m.title}</title></polygon>; }
> +                              const y = c.wy1 * sc - 6; return <polygon key={'m' + i} className="cx-mark sell" points={`${c.wx - 4},${y - 6} ${c.wx + 4},${y - 6} ${c.wx},${y}`}><title>{m.title}</title></polygon>;
> +                            })}
> +                          </svg>
> +                        : <div className="cx-empty">{klErr ? 'klines indisponíveis (CORS/Binance)' : 'carregando candles…'}</div>}
> +
> +                      <div className={`cx-decision ${dec.cls}`}>
> +                        <span className="cx-dec-act">{dec.act}</span>
> +                        <span className="cx-dec-body"><b>{dec.head}.</b> {dec.reason}</span>
> +                      </div>
> +
> +                      <div className="cx-line">
> +                        <span className="l">Sinal nesta vela</span>
> +                        <span className="v">{snow.length ? snow.map((x, i) => <span key={i} className={`cx-badge ${x.cls}`}>{x.t}</span>) : <span className="cx-flat">nenhum sinal — monitorando</span>}</span>
> +                      </div>
> +
> +                      <div className="cx-hud-grid">
> +                        {tile('preço ao vivo', fmtPx(liveP), chg != null ? dirClass(chg) : '')}
> +                        {tile('vela O/H/L/C', kl ? `${fmtPx(kl.o)}/${fmtPx(kl.h)}/${fmtPx(kl.l)}/${fmtPx(kl.c)}` : '—')}
> +                        {tile('Δ vela', chg != null ? fmtPct(chg) : '—', chg != null ? dirClass(chg) : '')}
> +                        {tile('RSI 1m', rsi1 != null ? rsi1.toFixed(1) : '—', rsi1 != null ? (rsi1 < _buyTh ? 'cx-up' : rsi1 > _sellTh ? 'cx-down' : 'cx-flat') : '')}
> +                        {tile('RSI 15m', rsi15 != null ? rsi15.toFixed(1) : '—')}
> +                        {tile('regime', g.regime || '—', g.regime === 'trend' ? 'cx-up' : g.regime === 'bear' ? 'cx-down' : 'cx-flat')}
> +                        {tile('tendência 1h', `${sig.trendSlope || '—'} · ${sig.trendCross || 'none'}`)}
> +                        {tile('fluxo imb/tox', fl.imbalance != null ? `${fl.imbalance.toFixed(2)} / ${fl.toxicity != null ? fl.toxicity.toFixed(2) : '—'}` : '—', fl.imbalance != null ? (fl.imbalance < 0 ? 'cx-down' : 'cx-up') : '')}
> +                        {tile('compra liberada?', g.buyAllowed ? 'sim' : 'não', g.buyAllowed ? 'cx-up' : 'cx-down')}
> +                        {tile('EV vela gross/net', ev.grossPct != null ? `${fmtPct(ev.grossPct)} / ${fmtPct(ev.netPct)}` : '—', ev.netPct != null ? dirClass(ev.netPct) : '')}
> +                      </div>
> +
> +                      {g.reason && <div className="cx-note" style={{ marginTop: 4 }}><b>Doutrina do gate:</b> {g.reason}</div>}
> +
> +                      {recent.length > 0 && <React.Fragment>
> +                        <div className="cx-line" style={{ fontWeight: 700, marginTop: 6 }}><span className="l">Últimos sinais gravados</span><span className="v cx-flat" style={{ fontSize: '0.66rem' }}>desfecho @10min</span></div>
> +                        {recent.map((r, i) => (
> +                          <div className="cx-line" key={i}>
> +                            <span className="l cx-mono">{r.type} <span className="cx-flat" style={{ fontSize: '0.66rem' }}>RSI {r.ctx && r.ctx.rsi1m != null ? Math.round(r.ctx.rsi1m) : '—'} · reg {r.ctx ? r.ctx.regime : '—'}</span></span>
> +                            <span className={`v cx-mono ${r.ret10 != null ? dirClass(r.ret10) : ''}`}>{r.ret10 != null ? fmtPct(r.ret10) : '—'}</span>
> +                          </div>
> +                        ))}
> +                      </React.Fragment>}
> +
> +                      <div className="cx-note">HUD read-only dos dados REAIS que dirigem as decisões: preço/vela ao vivo (WS), RSI/regime/fluxo/gates do brain (poll 60s) e a decisão simulada (o que o sistema FARIA — sem enviar ordem). Segue o seletor de símbolo acima.</div>
> +                    </React.Fragment>
> +                  );
> +                })()}
> +              </div>
> +            </div>
> +
>            </div>
>  
>            <div className="cx-legend">
> diff --git a/frontend/src/private/Cockpit/cockpit.css b/frontend/src/private/Cockpit/cockpit.css
> index 895a75b..27475be 100644
> --- a/frontend/src/private/Cockpit/cockpit.css
> +++ b/frontend/src/private/Cockpit/cockpit.css
> @@ -72,7 +72,28 @@
>  .cockpit .cx-grid { display: grid; gap: 14px; }
>  .cockpit .cx-row { display: grid; gap: 14px; grid-template-columns: 1.6fr 1fr; }
>  .cockpit .cx-row-3 { display: grid; gap: 14px; grid-template-columns: 1.4fr 1fr; }
> -@media (max-width: 1100px) { .cockpit .cx-row, .cockpit .cx-row-3 { grid-template-columns: 1fr; } }
> +.cockpit .cx-row-2 { display: grid; gap: 14px; grid-template-columns: 1fr 1fr; }
> +@media (max-width: 1100px) { .cockpit .cx-row, .cockpit .cx-row-3, .cockpit .cx-row-2 { grid-template-columns: 1fr; } }
> +
> +.cockpit .cx-hud-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 8px; margin: 8px 0; }
> +.cockpit .cx-hud-tile { padding: 7px 9px; border-radius: 8px; background: rgba(10, 14, 28, 0.5); border: 1px solid var(--cx-border); display: flex; flex-direction: column; gap: 3px; }
> +.cockpit .cx-hud-k { font-size: 0.6rem; letter-spacing: 0.06em; text-transform: uppercase; color: var(--cx-muted); }
> +.cockpit .cx-hud-v { font-size: 0.9rem; font-weight: 600; color: var(--cx-text); }
> +.cockpit .cx-decision { display: flex; align-items: baseline; gap: 10px; padding: 9px 11px; border-radius: 10px; border: 1px solid var(--cx-border); background: rgba(10, 14, 28, 0.5); margin: 6px 0; }
> +.cockpit .cx-decision .cx-dec-act { font-weight: 700; font-size: 0.82rem; letter-spacing: 0.04em; white-space: nowrap; }
> +.cockpit .cx-decision .cx-dec-body { font-size: 0.78rem; color: var(--cx-muted); }
> +.cockpit .cx-decision.buy { border-color: rgba(47, 245, 168, 0.4); background: var(--cx-green-dim); }
> +.cockpit .cx-decision.buy .cx-dec-act { color: var(--cx-green); }
> +.cockpit .cx-decision.sell { border-color: rgba(255, 93, 122, 0.4); background: var(--cx-red-dim); }
> +.cockpit .cx-decision.sell .cx-dec-act, .cockpit .cx-decision.halt .cx-dec-act { color: var(--cx-red); }
> +.cockpit .cx-decision.halt { border-color: rgba(255, 93, 122, 0.5); }
> +.cockpit .cx-decision.hold, .cockpit .cx-decision.wait { border-color: rgba(255, 179, 64, 0.35); }
> +.cockpit .cx-decision.hold .cx-dec-act, .cockpit .cx-decision.wait .cx-dec-act { color: var(--cx-amber); }
> +.cockpit .cx-decision.ready { border-color: rgba(56, 182, 255, 0.35); }
> +.cockpit .cx-decision.ready .cx-dec-act { color: var(--cx-cyan); }
> +.cockpit .cx-badge { display: inline-block; padding: 2px 7px; margin: 2px 4px 2px 0; border-radius: 6px; font-size: 0.68rem; background: rgba(10, 14, 28, 0.6); border: 1px solid var(--cx-border); color: var(--cx-text); }
> +.cockpit .cx-badge.cx-up { color: var(--cx-green); border-color: rgba(47, 245, 168, 0.35); }
> +.cockpit .cx-badge.cx-down { color: var(--cx-red); border-color: rgba(255, 93, 122, 0.35); }
>  
>  .cockpit .cx-panel {
>    position: relative;
> ```

## 🤖 Claude *(18:00:00)*

Agora vou ler o Cockpit.js para verificar os guards, as consts component-level, os helpers e o balanceamento do JSX.

## 🤖 Claude *(18:00:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "wc -l /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js",
  "description": "Count lines of Cockpit.js"
}
```

## 🤖 Claude *(18:00:03)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js",
  "limit": 130
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 976 /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import React, { useState, useEffect } from 'react';
> 2	import useWebSocket from 'react-use-websocket';
> 3	import Menu from '../../components/Menu/Menu';
> 4	import Toast from '../../components/Toast/Toast';
> 5	import { getBalance } from '../../services/ExchangeService';
> 6	import { getOrdersReport } from '../../services/OrdersService';
> 7	import { getRegimeStatus, getFlowStatus, getAgentRuns, getCockpit, postCall } from '../../services/IntelligenceService';
> 8	import { getAutomationGroups } from '../../services/AutomationsService';
> 9	import { AnimatedNumber, GaltonBoard, PathFan } from './CockpitSims';
> 10	import './cockpit.css';
> 11	
> 12	/*
> 13	 * Cockpit — terminal "FABLE" (dark/neon), inspirado na referência viral.
> 14	 * READ-ONLY: só LÊ dados reais (saldo, relatório, regime/flow, KPIs do agente, klines públicas
> 15	 * da Binance, WS de preço). NÃO emite ordem, NÃO toca o TRADING_HALT.
> 16	 * A estética é dos painéis da referência; os DADOS são os reais nossos (sem número fabricado).
> 17	 * Selo: 🟢 dado real (único selo restante — placeholders/estados falsos foram removidos).
> 18	 */
> 19	
> 20	const REPORT_QUOTE = 'USDT';
> 21	const AGENT_STALE_MS = 15 * 60 * 1000;
> 22	const FEE_RT = 0.20;        // round-trip taker spot (%)
> 23	const FEE_RT_BNB = 0.15;    // round-trip com BNB (%)
> 24	const KL_SYMBOL = 'BTCUSDT';
> 25	const KL_HOSTS = ['https://api.binance.com', 'https://data-api.binance.vision'];
> 26	
> 27	function num(v) {
> 28	  if (v === null || v === undefined) return NaN;
> 29	  if (typeof v === 'number') return v;
> 30	  const n = parseFloat(String(v).replace(/[^0-9.\-]/g, ''));
> 31	  return isNaN(n) ? NaN : n;
> 32	}
> 33	function fmtUsd(v, dec = 2) {
> 34	  const n = num(v);
> 35	  if (isNaN(n)) return '—';
> 36	  return '$' + n.toLocaleString('en-US', { minimumFractionDigits: dec, maximumFractionDigits: dec });
> 37	}
> 38	function fmtPct(v) {
> 39	  const n = num(v);
> 40	  if (isNaN(n)) return '—';
> 41	  return (n > 0 ? '+' : '') + n.toFixed(2) + '%';
> 42	}
> 43	function dirClass(v) {
> 44	  const n = num(v);
> 45	  if (isNaN(n) || n === 0) return 'cx-flat';
> 46	  return n > 0 ? 'cx-up' : 'cx-down';
> 47	}
> 48	function fmtAge(ms) {
> 49	  if (ms == null) return '—';
> 50	  const s = Math.round(ms / 1000);
> 51	  if (s < 90) return `${s}s`;
> 52	  const m = Math.round(s / 60);
> 53	  if (m < 90) return `${m}min`;
> 54	  return `${Math.round(m / 60)}h`;
> 55	}
> 56	
> 57	function buildSpark(series) {
> 58	  const pts = (series || []).map(num).filter(n => !isNaN(n));
> 59	  if (pts.length < 2) return null;
> 60	  const W = 600, H = 70, pad = 5;
> 61	  const min = Math.min(...pts), max = Math.max(...pts);
> 62	  const span = max - min || 1;
> 63	  const step = (W - pad * 2) / (pts.length - 1);
> 64	  const c = pts.map((p, i) => [pad + i * step, pad + (H - pad * 2) * (1 - (p - min) / span)]);
> 65	  const line = c.map((p, i) => `${i ? 'L' : 'M'}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' ');
> 66	  return { line, area: `${line} L${c[c.length - 1][0].toFixed(1)},${H} L${c[0][0].toFixed(1)},${H} Z`, up: pts[pts.length - 1] >= pts[0] };
> 67	}
> 68	
> 69	// candlestick a partir das klines [[t,o,h,l,c,...]] -> geometria p/ SVG
> 70	function buildCandles(kl, H = 220) {
> 71	  const data = (kl || []).slice(-60);
> 72	  if (data.length < 2) return null;
> 73	  const W = 600, padT = 8, padB = 8, padL = 4, padR = 40;
> 74	  const max = Math.max(...data.map(d => d.h)), min = Math.min(...data.map(d => d.l));
> 75	  const span = max - min || 1;
> 76	  const cw = (W - padL - padR) / data.length;
> 77	  const bw = Math.max(1.5, cw * 0.62);
> 78	  const y = p => padT + (H - padT - padB) * (1 - (p - min) / span);
> 79	  const candles = data.map((d, i) => {
> 80	    const xc = padL + cw * i + cw / 2;
> 81	    const up = d.c >= d.o;
> 82	    const oy = y(d.o), cy = y(d.c);
> 83	    return { x: xc - bw / 2, bw, by: Math.min(oy, cy), bh: Math.max(1, Math.abs(oy - cy)), wx: xc, wy1: y(d.h), wy2: y(d.l), up };
> 84	  });
> 85	  return { candles, lastY: y(data[data.length - 1].c), last: data[data.length - 1].c, hi: max, lo: min, W, H, padR };
> 86	}
> 87	
> 88	// distribuição de retornos 1m (%) + faixa de fee
> 89	function buildHist(kl) {
> 90	  if (!kl || kl.length < 5) return null;
> 91	  const rets = [];
> 92	  for (let i = 1; i < kl.length; i++) {
> 93	    const r = (kl[i].c - kl[i - 1].c) / kl[i - 1].c * 100;
> 94	    if (isFinite(r)) rets.push(r);
> 95	  }
> 96	  if (!rets.length) return null;
> 97	  const LIM = 0.5, BINS = 25, step = (LIM * 2) / BINS;
> 98	  const counts = new Array(BINS).fill(0);
> 99	  rets.forEach(r => { let b = Math.floor((Math.min(LIM - 1e-9, Math.max(-LIM, r)) + LIM) / step); if (b < 0) b = 0; if (b >= BINS) b = BINS - 1; counts[b]++; });
> 100	  const sorted = rets.map(r => Math.abs(r)).sort((a, b) => a - b);
> 101	  const mean = rets.reduce((a, b) => a + b, 0) / rets.length;
> 102	  const sd = Math.sqrt(rets.reduce((a, b) => a + (b - mean) * (b - mean), 0) / rets.length);
> 103	  return {
> 104	    counts, maxc: Math.max(...counts, 1), step, BINS, LIM, n: rets.length, mean, sd,
> 105	    clearFee: rets.filter(r => Math.abs(r) >= FEE_RT).length / rets.length * 100,
> 106	    medAbs: sorted[Math.floor(sorted.length / 2)],
> 107	  };
> 108	}
> 109	
> 110	// RSI 14 (Wilder) client-side sobre os closes das klines 1m — p/ marcar NA vela onde a condicao de
> 111	// sobrevenda/sobrecompra dispararia (execucao SIMULADA). Mesmo metodo do indicador do beholder.
> 112	function computeRSI(closes, period = 14) {
> 113	  const out = new Array((closes || []).length).fill(NaN);
> 114	  if (!closes || closes.length < period + 1) return out;
> 115	  let g = 0, l = 0;
> 116	  for (let i = 1; i <= period; i++) { const d = closes[i] - closes[i - 1]; if (d >= 0) g += d; else l -= d; }
> 117	  let aG = g / period, aL = l / period;
> 118	  out[period] = aL === 0 ? 100 : 100 - 100 / (1 + aG / aL);
> 119	  for (let i = period + 1; i < closes.length; i++) {
> 120	    const d = closes[i] - closes[i - 1], gg = d > 0 ? d : 0, ll = d < 0 ? -d : 0;
> 121	    aG = (aG * (period - 1) + gg) / period; aL = (aL * (period - 1) + ll) / period;
> 122	    out[i] = aL === 0 ? 100 : 100 - 100 / (1 + aG / aL);
> 123	  }
> 124	  return out;
> 125	}
> 126	
> 127	// Painel de RSI (sub-grafico) alinhado x-a-x com os candles: linha do RSI + faixas de compra(sobrevenda)/
> 128	// venda(sobrecompra). Torna VISIVEL o "porque" de cada marcador (o RSI entra na faixa exatamente na vela).
> 129	function buildRsiPane(vals, buyTh, sellTh) {
> 130	  const W = 600, H = 96, padL = 4, padR = 40, padT = 6, padB = 6;
> ```

## 🤖 Claude *(18:00:06)*

Vou ler as consts component-level, os helpers `simDecision`/`dirClass`/`num`, e a região do JSX modificada com contexto amplo.

## 🤖 Claude *(18:00:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"simDecision\\|cndBig\\|const marks\\|const klive\\|const btcWs\\|const cpBtc\\|const cp \\|const cp=\\|selSym\\|_rsi\\|_buyTh\\|_sellTh\\|const klErr\\|cp.patterns\\|function Cockpit\" /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js",
  "description": "Locate component-level consts and helpers"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 153:function simDecision(sym, cp) {
> 191:function Cockpit() {
> 202:  const [selSym, setSelSym] = useState(KL_SYMBOL);  // simbolo do widget de simulacao (dirige tambem o candle/dist)
> 255:    postCall(selSym, direction, '', token)
> 256:      .then(r => { setNotification({ type: 'success', text: `Previsao registrada: ${selSym.replace('USDT', '')} ${direction === 'down' ? 'CAIR' : 'SUBIR'} @ ${r.price}. Pontuo o desfecho em 5-15min.` }); setTimeout(loadAll, 1500); })
> 266:    loadKlines(selSym);
> 267:    const id = setInterval(() => loadKlines(selSym), 60000);
> 269:  }, [selSym]);
> 273:  const btcWs = prices[selSym];  // preco ao vivo do simbolo selecionado (nome mantido p/ o resto do render)
> 274:  const klive = (klines && btcWs != null && !isNaN(btcWs))
> 278:  const cndBig = buildCandles(klive, 440);   // candle ALTO p/ o widget principal (com marcadores de execucao)
> 282:  const _rsi = computeRSI(_closes, 14);
> 283:  const _isAltSel = selSym !== 'BTCUSDT';
> 284:  const _buyTh = _isAltSel ? 35 : 30, _sellTh = 70;
> 285:  const _cpSel = (cockpit.symbols || {})[selSym] || {};
> 291:  const marks = [];
> 292:  if (cndBig && _rsi.length === _closes.length && _closes.length > 15) {
> 293:    const dispN = cndBig.candles.length, off = _closes.length - dispN;
> 296:      const r = _rsi[ki], rp = _rsi[ki - 1];
> 298:      if (r < _buyTh && rp >= _buyTh) marks.push({ i: j, type: 'buy', armed: _armed, title: `compra simulada · RSI ${r.toFixed(0)} cruzou <${_buyTh} (sobrevenda) -> ${_armed ? 'EXECUTARIA' : 'EM CAIXA (regime ' + _regSel + ')'}` });
> 299:      else if (r > _sellTh && rp <= _sellTh) marks.push({ i: j, type: 'sell', title: `venda/saida simulada · RSI ${r.toFixed(0)} cruzou >${_sellTh} (sobrecompra)` });
> 302:  const _rsiDisp = (cndBig && _closes.length) ? cndBig.candles.map((_, j) => { const ki = (_closes.length - cndBig.candles.length) + j; return (ki >= 0 && ki < _rsi.length) ? _rsi[ki] : NaN; }) : [];
> 303:  const rsiPane = buildRsiPane(_rsiDisp, _buyTh, _sellTh);
> 306:    if (!cndBig) return null;
> 307:    const padT = 8, padB = 8, span = (cndBig.hi - cndBig.lo) || 1;
> 308:    const yOf = v => padT + (cndBig.H - padT - padB) * (1 - (v - cndBig.lo) / span);
> 309:    const dispN = cndBig.candles.length, off = _closes.length - dispN, pts = [];
> 310:    for (let j = 0; j < dispN; j++) { const v = arr[off + j]; if (v != null) pts.push([cndBig.candles[j].wx, yOf(v)]); }
> 319:  const cp = cockpit || {};
> 321:  const cpBtc = (cp.symbols || {})[selSym] || null;  // dados do brain p/ o simbolo selecionado
> 384:                    symbols.map(s => <button key={s} className={`cx-symtab ${s === selSym ? 'on' : ''}`} onClick={() => setSelSym(s)}>{s.replace('USDT', '')}</button>)}
> 386:                    <span className="cl">eu chamo {selSym.replace('USDT', '')}:</span>
> 396:                      {cndBig && <span className="cx-flat cx-mono" style={{ fontSize: '0.72rem' }}>H {fmtUsd(cndBig.hi, cndBig.hi < 5 ? 4 : 0)} · L {fmtUsd(cndBig.lo, cndBig.lo < 5 ? 4 : 0)}</span>}
> 400:                    {cndBig
> 401:                      ? <React.Fragment><svg className="cx-candle tall" viewBox={`0 0 ${cndBig.W} ${cndBig.H}`} preserveAspectRatio="none" aria-label={`Candles 1m do ${selSym} com execucoes simuladas`}>
> 402:                          {[0.25, 0.5, 0.75].map((gg, i) => <line key={i} className="grid" x1="0" x2={cndBig.W} y1={cndBig.H * gg} y2={cndBig.H * gg} />)}
> 403:                          {cndBig.candles.map((cc, i) => (<g key={i}><line className={cc.up ? 'wick-up' : 'wick-down'} x1={cc.wx} x2={cc.wx} y1={cc.wy1} y2={cc.wy2} /><rect className={cc.up ? 'body-up' : 'body-down'} x={cc.x} y={cc.by} width={cc.bw} height={cc.bh} /></g>))}
> 404:                          <line className="lastline" x1="0" x2={cndBig.W - cndBig.padR} y1={cndBig.lastY} y2={cndBig.lastY} />
> 408:                            const c = cndBig.candles[m.i]; if (!c) return null;
> 419:                          <text className="rsi-lbl" x="3" y={rsiPane.yBuy - 3}>RSI &lt;{_buyTh} compra (sobrevenda)</text>
> 420:                          <text className="rsi-lbl" x="3" y={rsiPane.ySell + 10}>RSI &gt;{_sellTh} venda (sobrecompra)</text>
> 427:                      const s = (cp.symbols || {})[selSym] || {};
> 454:                {(() => { const d = simDecision(selSym, cp); return (
> 468:                  const pat = cp.patterns || {};
> 513:                  const oc = (cp.patterns && cp.patterns.opCalls) || {};
> 576:                <div className="cx-panel-title"><span><span className="cx-seal real" /> {selSym} · candles 1m</span><span className="cx-src">binance /api/v3/klines + WS miniTicker</span></div>
> 767:                <div className="cx-line" style={{ marginTop: 10 }}><span className="l"><span className="cx-seal real" /> Moves ≥ break-even ({selSym.replace('USDT','')})</span><span className="v cx-mono">{cpBtc && cpBtc.dist ? Number(cpBtc.dist.pHitBreakevenPct).toFixed(0) + '%' : '—'}</span></div>
> 768:                <div className="cx-line"><span className="l"><span className="cx-seal real" /> Gate acumulação {selSym.replace('USDT','')} <span className="cx-flat" style={{ fontSize: '0.66rem' }}>(farm/baseline)</span></span><span className={`v cx-mono ${cpBtc && cpBtc.gates ? (cpBtc.gates.buyAllowed ? 'cx-up' : 'cx-down') : ''}`} title={cpBtc && cpBtc.gates ? cpBtc.gates.reason : ''}>{cpBtc && cpBtc.gates ? (cpBtc.gates.buyAllowed ? 'GO' : 'CAIXA') : '—'}</span></div>
> 874:                <div className="cx-panel-title"><span><span className="cx-seal real" /> Análise da vela ao vivo (HUD) — {selSym.replace('USDT', '')}</span><span className="cx-src">WS preço + /analysis/cockpit · segue o seletor</span></div>
> 878:                  const dec = simDecision(selSym, cp);
> 882:                  const rsi1 = sig.rsi1m != null ? sig.rsi1m : (_rsi.length ? _rsi[_rsi.length - 1] : null);
> 886:                  if (rsi1 != null && rsi1 < _buyTh) snow.push({ t: `RSI 1m ${rsi1.toFixed(0)} < ${_buyTh} · sobrevenda`, cls: 'cx-up' });
> 887:                  if (rsi1 != null && rsi1 > _sellTh) snow.push({ t: `RSI 1m ${rsi1.toFixed(0)} > ${_sellTh} · sobrecompra`, cls: 'cx-down' });
> 892:                  const recent = (cp.patterns && Array.isArray(cp.patterns.recent) ? cp.patterns.recent : []).filter((r) => r.symbol === selSym).slice(0, 5);
> 894:                  const sc = cndBig ? 200 / cndBig.H : 1;
> 897:                      {cndBig
> 898:                        ? <svg className="cx-candle" viewBox={`0 0 ${cndBig.W} 200`} preserveAspectRatio="none" aria-label={`Candles 1m do ${selSym} com sinais ao vivo`}>
> 899:                            {[0.25, 0.5, 0.75].map((gg, i) => <line key={i} className="grid" x1="0" x2={cndBig.W} y1={200 * gg} y2={200 * gg} />)}
> 900:                            {cndBig.candles.map((cc, i) => {
> 901:                              const last = i === cndBig.candles.length - 1;
> 908:                              const c = cndBig.candles[m.i]; if (!c) return null;
> 929:                        {tile('RSI 1m', rsi1 != null ? rsi1.toFixed(1) : '—', rsi1 != null ? (rsi1 < _buyTh ? 'cx-up' : rsi1 > _sellTh ? 'cx-down' : 'cx-flat') : '')}
> ```

## 🤖 Claude *(18:00:16)*

Vou ler `simDecision` (linhas 153-190), o bloco de consts component-level (191-330), e o novo widget completo (868-965) para verificar guards e balanceamento.

## 🤖 Claude *(18:00:17)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js",
  "offset": 153,
  "limit": 175
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 153	function simDecision(sym, cp) {
> 154	  const s = (cp.symbols || {})[sym] || {};
> 155	  const g = s.gates || {}, sig = s.signals || {}, fl = s.flow || {};
> 156	  const env = cp.env || {};
> 157	  const promoted = (cp.promotions && cp.promotions.promoted) || {};
> 158	  const grand = (cp.promotions && cp.promotions.grandfather) || [];
> 159	  const isAlt = sym !== 'BTCUSDT';
> 160	  const strat = isAlt ? 'farmnl' : 'consistencia';      // trilha do paper que gateia (espelha PROMO_MAP do supervisor)
> 161	  const isPromoted = !!promoted[strat] || grand.indexOf(strat) !== -1;
> 162	  const reg = g.regime || 'unknown';
> 163	  const imb = fl.imbalance, tox = fl.toxicity;
> 164	  const flowSide = imb != null ? (imb < 0 ? 'venda agressora' : 'compra agressora') : null;
> 165	  const dcaQty = (sig.farmDca && sig.farmDca.qty) ? sig.farmDca.qty : 0;
> 166	  const tq = sig.trendQty || 0;
> 167	  const rsi = isAlt ? sig.rsi15m : sig.rsi1m;
> 168	  const trig = isAlt ? 35 : 25;
> 169	  const sx = sym.replace('USDT', '');
> 170	
> 171	  if (env.tradingHalt)
> 172	    return { act: 'BLOQUEADO', cls: 'halt', head: 'HALT ativo', reason: `kill-switch${env.haltSource ? ' (' + env.haltSource + ')' : ''} — nenhuma ordem sai, nem compra nem venda.` };
> 173	  if (dcaQty > 0) {
> 174	    const cost = sig.farmDca.cost, tgt = cost ? cost * 1.012 : null;
> 175	    return { act: 'VENDERIA', cls: 'sell', head: `saida no-loss do Farm ${sx}`, reason: `tenho ${dcaQty} em carteira (custo ${cost ? cost.toFixed(4) : '—'}); a venda dispara quando o bestBid passar de ${tgt ? tgt.toFixed(4) : 'custo x1.012'} (lucro ja pos-fee).` };
> 176	  }
> 177	  if (tq > 0)
> 178	    return { act: 'SEGURO·TREND', cls: 'sell', head: 'posicao de trend aberta', reason: `${tq} em carteira; sairia no death cross (venda protetiva armada).` };
> 179	  if (reg === 'bear' || reg === 'unknown')
> 180	    return { act: 'CAIXA', cls: 'hold', head: 'acumular em caixa', reason: `regime ${reg}: a doutrina e nao comprar no bear. Eu compraria quando ${sx} sair do bear E a trilha "${strat}" provar edge no paper.` };
> 181	  if (!isPromoted)
> 182	    return { act: 'AGUARDANDO PROVA', cls: 'wait', head: `regime ${reg} liberou, falta prova`, reason: `a trilha "${strat}" ainda nao provou edge no paper -> a entrada REAL fica travada (frente D). No paper ela ja operaria. Liberar na hora: PROMOTION_GRANDFATHER=${strat}.` };
> 183	  const flowGated = !!g.flowGated, flowOk = g.flowOk !== false;
> 184	  if (rsi != null && rsi < trig && (!flowGated || flowOk))
> 185	    return { act: 'COMPRARIA AGORA', cls: 'buy', head: `dip em ${sx}`, reason: `RSI ${isAlt ? '15m' : '1m'}=${rsi.toFixed(1)} < ${trig} (gatilho) + regime ${reg} + trilha provada + gate aberto.${tox != null && tox >= 0.6 ? ` AT. ${flowSide} (tox ${tox.toFixed(2)}) — timing apertado.` : ''} (ordem NAO liberada — simulacao.)` };
> 186	  if (flowGated && !flowOk)
> 187	    return { act: 'ESPERANDO TIMING', cls: 'wait', head: 'gate aberto, fluxo veta', reason: `${flowSide} forte (toxicity ${tox != null ? tox.toFixed(2) : '—'}) — nao compro contra a agressao agora.` };
> 188	  return { act: 'PRONTO·AGUARDA DIP', cls: 'ready', head: `armado em ${sx}`, reason: `regime ${reg} + trilha provada + gate aberto. Espero o RSI ${isAlt ? '15m' : '1m'} cair < ${trig} (agora ${rsi != null ? rsi.toFixed(1) : '—'}).` };
> 189	}
> 190	
> 191	function Cockpit() {
> 192	  const [balance, setBalance] = useState({});
> 193	  const [report, setReport] = useState({});
> 194	  const [gate, setGate] = useState({ symbols: {} });
> 195	  const [flow, setFlow] = useState({ symbols: {} });
> 196	  const [agent, setAgent] = useState({ kpis: {}, runs: [] });
> 197	  const [prices, setPrices] = useState({});
> 198	  const [klines, setKlines] = useState(null);
> 199	  const [klErr, setKlErr] = useState(false);
> 200	  const [cockpit, setCockpit] = useState({ symbols: {} });
> 201	  const [groups, setGroups] = useState({ groups: [] });
> 202	  const [selSym, setSelSym] = useState(KL_SYMBOL);  // simbolo do widget de simulacao (dirige tambem o candle/dist)
> 203	  const [notification, setNotification] = useState({});
> 204	
> 205	  const { readyState } = useWebSocket(process.env.REACT_APP_WS_URL, {
> 206	    queryParams: { token: localStorage.getItem('token') },
> 207	    onMessage: (event) => {
> 208	      try {
> 209	        const msg = JSON.parse(event.data);
> 210	        if (msg && msg.miniTicker) {
> 211	          const mt = msg.miniTicker;
> 212	          setPrices(prev => {
> 213	            const next = { ...prev };
> 214	            const put = (sym, c) => { if (sym && c != null && !isNaN(num(c))) next[sym] = num(c); };
> 215	            if (Array.isArray(mt)) mt.forEach(t => put(t && t.symbol, t && (t.close ?? t.c)));
> 216	            else if (mt.symbol) put(mt.symbol, mt.close ?? mt.c);
> 217	            else Object.keys(mt).forEach(k => put(k, mt[k] && (mt[k].close ?? mt[k].c)));
> 218	            return next;
> 219	          });
> 220	        }
> 221	      } catch (e) { /* ignora */ }
> 222	    },
> 223	    shouldReconnect: () => true,
> 224	    reconnectInterval: 3000,
> 225	  });
> 226	
> 227	  function loadAll() {
> 228	    const token = localStorage.getItem('token');
> 229	    getBalance(token).then(setBalance).catch(() => {});
> 230	    getOrdersReport(REPORT_QUOTE, null, null, token, '').then(setReport).catch(err => {
> 231	      setNotification({ type: 'error', text: err.response ? (err.response.data.error || err.response.data) : err.message });
> 232	    });
> 233	    getRegimeStatus(token).then(setGate).catch(() => {});
> 234	    getFlowStatus(token).then(setFlow).catch(() => {});
> 235	    getAgentRuns(50, token).then(setAgent).catch(() => {});
> 236	    getCockpit(token).then(setCockpit).catch(() => {});
> 237	    getAutomationGroups(token).then(setGroups).catch(() => {});
> 238	  }
> 239	
> 240	  async function loadKlines(sym) {
> 241	    for (const host of KL_HOSTS) {
> 242	      try {
> 243	        const r = await fetch(`${host}/api/v3/klines?symbol=${sym}&interval=1m&limit=120`);
> 244	        if (!r.ok) continue;
> 245	        const raw = await r.json();
> 246	        const parsed = raw.map(k => ({ t: k[0], o: +k[1], h: +k[2], l: +k[3], c: +k[4] }));
> 247	        setKlines(parsed); setKlErr(false); return;
> 248	      } catch (e) { /* tenta próximo host */ }
> 249	    }
> 250	    setKlErr(true);
> 251	  }
> 252	
> 253	  function doCall(direction) {
> 254	    const token = localStorage.getItem('token');
> 255	    postCall(selSym, direction, '', token)
> 256	      .then(r => { setNotification({ type: 'success', text: `Previsao registrada: ${selSym.replace('USDT', '')} ${direction === 'down' ? 'CAIR' : 'SUBIR'} @ ${r.price}. Pontuo o desfecho em 5-15min.` }); setTimeout(loadAll, 1500); })
> 257	      .catch(e => setNotification({ type: 'error', text: 'falha ao registrar: ' + (e.response ? (e.response.data.error || e.response.data) : e.message) }));
> 258	  }
> 259	
> 260	  useEffect(() => {
> 261	    loadAll();
> 262	    const id = setInterval(loadAll, 60000);
> 263	    return () => clearInterval(id);
> 264	  }, []);
> 265	  useEffect(() => {
> 266	    loadKlines(selSym);
> 267	    const id = setInterval(() => loadKlines(selSym), 60000);
> 268	    return () => clearInterval(id);
> 269	  }, [selSym]);
> 270	
> 271	  const wsLive = readyState === 1;
> 272	  const hist = buildHist(klines);
> 273	  const btcWs = prices[selSym];  // preco ao vivo do simbolo selecionado (nome mantido p/ o resto do render)
> 274	  const klive = (klines && btcWs != null && !isNaN(btcWs))
> 275	    ? klines.map((k, i) => i === klines.length - 1 ? { ...k, c: btcWs, h: Math.max(k.h, btcWs), l: Math.min(k.l, btcWs) } : k)
> 276	    : klines;
> 277	  const cnd = buildCandles(klive);
> 278	  const cndBig = buildCandles(klive, 440);   // candle ALTO p/ o widget principal (com marcadores de execucao)
> 279	  // EXECUCOES SIMULADAS na vela: marca onde a condicao RSI de sobrevenda(compra)/sobrecompra(venda) dispararia.
> 280	  // "armed" = regime+promocao deixariam EXECUTAR agora (solido); senao "gated" (vazado = sinal, mas em caixa).
> 281	  const _closes = (klines || []).map(k => k.c);
> 282	  const _rsi = computeRSI(_closes, 14);
> 283	  const _isAltSel = selSym !== 'BTCUSDT';
> 284	  const _buyTh = _isAltSel ? 35 : 30, _sellTh = 70;
> 285	  const _cpSel = (cockpit.symbols || {})[selSym] || {};
> 286	  const _regSel = (_cpSel.gates && _cpSel.gates.regime) || 'unknown';
> 287	  const _promoted = (cockpit.promotions && cockpit.promotions.promoted) || {};
> 288	  const _grand = (cockpit.promotions && cockpit.promotions.grandfather) || [];
> 289	  const _stratSel = _isAltSel ? 'farmnl' : 'consistencia';
> 290	  const _armed = (_regSel !== 'bear' && _regSel !== 'unknown') && (!!_promoted[_stratSel] || _grand.indexOf(_stratSel) !== -1);
> 291	  const marks = [];
> 292	  if (cndBig && _rsi.length === _closes.length && _closes.length > 15) {
> 293	    const dispN = cndBig.candles.length, off = _closes.length - dispN;
> 294	    for (let j = 1; j < dispN; j++) {
> 295	      const ki = off + j; if (ki <= 0) continue;
> 296	      const r = _rsi[ki], rp = _rsi[ki - 1];
> 297	      if (!isFinite(r) || !isFinite(rp)) continue;
> 298	      if (r < _buyTh && rp >= _buyTh) marks.push({ i: j, type: 'buy', armed: _armed, title: `compra simulada · RSI ${r.toFixed(0)} cruzou <${_buyTh} (sobrevenda) -> ${_armed ? 'EXECUTARIA' : 'EM CAIXA (regime ' + _regSel + ')'}` });
> 299	      else if (r > _sellTh && rp <= _sellTh) marks.push({ i: j, type: 'sell', title: `venda/saida simulada · RSI ${r.toFixed(0)} cruzou >${_sellTh} (sobrecompra)` });
> 300	    }
> 301	  }
> 302	  const _rsiDisp = (cndBig && _closes.length) ? cndBig.candles.map((_, j) => { const ki = (_closes.length - cndBig.candles.length) + j; return (ki >= 0 && ki < _rsi.length) ? _rsi[ki] : NaN; }) : [];
> 303	  const rsiPane = buildRsiPane(_rsiDisp, _buyTh, _sellTh);
> 304	  const _sma20 = sma(_closes, 20), _sma50 = sma(_closes, 50);
> 305	  function _smaPath(arr) {
> 306	    if (!cndBig) return null;
> 307	    const padT = 8, padB = 8, span = (cndBig.hi - cndBig.lo) || 1;
> 308	    const yOf = v => padT + (cndBig.H - padT - padB) * (1 - (v - cndBig.lo) / span);
> 309	    const dispN = cndBig.candles.length, off = _closes.length - dispN, pts = [];
> 310	    for (let j = 0; j < dispN; j++) { const v = arr[off + j]; if (v != null) pts.push([cndBig.candles[j].wx, yOf(v)]); }
> 311	    if (pts.length < 2) return null;
> 312	    return pts.map((p, i) => `${i ? 'L' : 'M'}${p[0].toFixed(1)},${p[1].toFixed(1)}`).join(' ');
> 313	  }
> 314	  const _sma20Path = _smaPath(_sma20), _sma50Path = _smaPath(_sma50);
> 315	  const btc = (btcWs != null && !isNaN(btcWs)) ? btcWs : (cnd ? cnd.last : null);
> 316	  const sigma = hist ? hist.sd : NaN;
> 317	
> 318	  // BRAIN snapshot (single source of truth): prefere o cockpitJob; klines client-side = fallback/render.
> 319	  const cp = cockpit || {};
> 320	  const env = cp.env || null;
> 321	  const cpBtc = (cp.symbols || {})[selSym] || null;  // dados do brain p/ o simbolo selecionado
> 322	  const histB = (cpBtc && cpBtc.dist && cpBtc.dist.hist && Array.isArray(cpBtc.dist.hist.counts))
> 323	    ? {
> 324	        counts: cpBtc.dist.hist.counts,
> 325	        maxc: Math.max(...cpBtc.dist.hist.counts, 1),
> 326	        step: cpBtc.dist.hist.binPct,
> 327	        BINS: cpBtc.dist.hist.counts.length,
> ```

## 🤖 Claude *(18:00:20)*

Agora vou ler o novo widget completo (linhas 868-965) e verificar o balanceamento das tags ao redor da mescla dos painéis (785-960).

## 🤖 Claude *(18:00:21)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js",
  "offset": 785,
  "limit": 185
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 785	                      return (
> 786	                        <div className="cx-line" key={i}>
> 787	                          <span className="l cx-mono">{name}</span>
> 788	                          <span className={`v cx-mono ${val != null ? dirClass(val) : ''}`}>{val != null ? (num(val) > 0 ? '+' : '') + fmtUsd(val) : '—'}</span>
> 789	                        </div>
> 790	                      );
> 791	                    })}
> 792	              </div>
> 793	            </div>
> 794	
> 795	            {/* ROW 5+6 — Paper: Estratégias | Trilhas (Trend) lado a lado (1fr/1fr) */}
> 796	            <div className="cx-row-2">
> 797	              <div className="cx-panel glow">
> 798	                <div className="cx-panel-title"><span><span className="cx-seal real" /> Paper · Estratégias (research, sem risco)</span><span className="cx-src">/analysis/cockpit · paper</span></div>
> 799	                {(() => {
> 800	                  const pp = cp.paper || null;
> 801	                  const strats = pp && Array.isArray(pp.strategies) ? pp.strategies.slice().sort((a, b) => num(b.totalPnl) - num(a.totalPnl)) : [];
> 802	                  if (!pp || strats.length === 0)
> 803	                    return <div className="cx-empty">sem trades paper ainda — trilhas armadas, aguardando sinal (consistência sai do trend; macro no próximo cross)</div>;
> 804	                  return (
> 805	                    <React.Fragment>
> 806	                      <div className="cx-line" style={{ fontWeight: 700 }}>
> 807	                        <span className="l">Total · {strats.length} trilhas</span>
> 808	                        <span className={`v cx-mono ${dirClass(pp.totals.totalPnl)}`}>{fmtUsd(pp.totals.totalPnl)}</span>
> 809	                      </div>
> 810	                      {strats.map((s, i) => (
> 811	                        <div className="cx-line" key={i} title={`realizado ${fmtUsd(s.realizedPnl)} + não-realizado ${fmtUsd(s.unrealizedPnl)} · fee ${fmtUsd(s.fees)} · ${s.buys}c/${s.sells}v`}>
> 812	                          <span className="l cx-mono">{s.strategy} <span className="cx-flat" style={{ fontSize: '0.66rem' }}>{s.buys}c/{s.sells}v{s.winRate != null ? ` · ${Math.round(s.winRate * 100)}% win` : ''}{s.openPositions ? ` · ${s.openPositions} aberta(s)` : ''}</span></span>
> 813	                          <span className={`v cx-mono ${dirClass(s.totalPnl)}`}>{fmtUsd(s.totalPnl)}</span>
> 814	                        </div>
> 815	                      ))}
> 816	                      <div className="cx-note">P&amp;L simulado com preço+fee <b>REAIS da mainnet</b> (broker virtual, zero dinheiro real; mainnet CONGELADO). Compara qual trilha tem edge antes de arriscar. A trilha de frequência/verde-diário foi refutada por backtest (EV&lt;0) — não listada.</div>
> 817	                    </React.Fragment>
> 818	                  );
> 819	                })()}
> 820	              </div>
> 821	
> 822	              {/* coluna 2: Paper Trilhas (Trend) — teste ao vivo */}
> 823	              <div className="cx-panel glow">
> 824	                <div className="cx-panel-title"><span><span className="cx-seal real" /> Paper Trilhas (Trend) — teste ao vivo</span><span className="cx-src">/analysis/cockpit · paper + symbols</span></div>
> 825	                {(() => {
> 826	                  const symObj = cp.symbols || {};
> 827	                  const regOf = (sym) => (((symObj[sym] || {}).gates) || {}).regime || '—';
> 828	                  const tracked = Object.keys(symObj).length ? Object.keys(symObj) : ['BTCUSDT', 'LTCUSDT', 'BNBUSDT', 'ADAUSDT'];
> 829	                  const breadth = tracked.filter((s) => regOf(s) === 'trend').length;
> 830	                  const byStrat = {};
> 831	                  (cp.paper && Array.isArray(cp.paper.strategies) ? cp.paper.strategies : []).forEach((s) => { byStrat[s.strategy] = s; });
> 832	                  const fmtPx = (v) => { const n = num(v); return n >= 100 ? n.toFixed(2) : n >= 1 ? n.toFixed(3) : n.toFixed(5); };
> 833	                  const tracks = [{ key: 'trendstate', label: 'TrendState · entra em qualquer símbolo em trend' }, { key: 'trendbreadth', label: 'TrendBreadth · só com ≥3 símbolos em trend' }];
> 834	                  return (
> 835	                    <React.Fragment>
> 836	                      <div className="cx-line" style={{ fontWeight: 700 }}>
> 837	                        <span className="l">Regime agora · breadth <span className={breadth >= 3 ? 'cx-up' : 'cx-flat'}>{breadth}/{tracked.length}</span> em trend</span>
> 838	                        <span className="v cx-mono">{tracked.map((s) => `${s.replace('USDT', '')}:${regOf(s)}`).join('  ')}</span>
> 839	                      </div>
> 840	                      {tracks.map((tk, i) => {
> 841	                        const s = byStrat[tk.key];
> 842	                        const syms = (s && s.symbols) || {};
> 843	                        const open = Object.keys(syms).filter((sym) => num(syms[sym].qty) > 0);
> 844	                        return (
> 845	                          <React.Fragment key={i}>
> 846	                            <div className="cx-line" style={{ marginTop: 6 }}>
> 847	                              <span className="l cx-mono">{tk.label} {s ? <span className="cx-flat" style={{ fontSize: '0.66rem' }}>{s.buys}c/{s.sells}v{s.winRate != null ? ` · ${Math.round(s.winRate * 100)}% win` : ''}{s.openPositions ? ` · ${s.openPositions} aberta(s)` : ''}</span> : <span className="cx-flat" style={{ fontSize: '0.66rem' }}>sem trades ainda</span>}</span>
> 848	                              <span className={`v cx-mono ${dirClass(s ? s.totalPnl : 0)}`}>{fmtUsd(s ? s.totalPnl : 0)}</span>
> 849	                            </div>
> 850	                            {open.length === 0
> 851	                              ? <div className="cx-note" style={{ marginTop: 0 }}>{tk.key === 'trendbreadth' && breadth < 3 ? `sem posição — aguardando confirmação ampla (breadth ${breadth}/${tracked.length} < 3, por desenho)` : 'sem posição aberta agora'}</div>
> 852	                              : open.map((sym, j) => {
> 853	                                const info = syms[sym];
> 854	                                return (
> 855	                                  <div className="cx-line" key={j} style={{ paddingLeft: 12 }} title={`entrada ${fmtPx(info.avgCost)} · realizado ${fmtUsd(info.realizedPnl)}`}>
> 856	                                    <span className="l cx-mono">{sym.replace('USDT', '')} <span className="cx-flat" style={{ fontSize: '0.66rem' }}>reg {regOf(sym)} · qty {num(info.qty).toFixed(4)} @ {fmtPx(info.avgCost)}</span></span>
> 857	                                    <span className={`v cx-mono ${dirClass(info.unrealizedPnl)}`}>{fmtUsd(info.unrealizedPnl)}</span>
> 858	                                  </div>
> 859	                                );
> 860	                              })}
> 861	                          </React.Fragment>
> 862	                        );
> 863	                      })}
> 864	                      <div className="cx-note">Teste ao vivo: surfar o regime <b>trend</b> em paper (preço+fee REAIS da mainnet, broker virtual, zero risco). <b>TrendState</b> entra em qualquer símbolo em trend; <b>TrendBreadth</b> só entra com ≥3/4 em trend (anti-whipsaw). O backtest de 900d alerta que trend em chop perde — aqui medimos pra frente, de graça.</div>
> 865	                    </React.Fragment>
> 866	                  );
> 867	                })()}
> 868	              </div>
> 869	            </div>
> 870	
> 871	            {/* ROW 7 — Análise da vela ao vivo (HUD): os "pensamentos" da vela atual */}
> 872	            <div className="cx-row">
> 873	              <div className="cx-panel glow">
> 874	                <div className="cx-panel-title"><span><span className="cx-seal real" /> Análise da vela ao vivo (HUD) — {selSym.replace('USDT', '')}</span><span className="cx-src">WS preço + /analysis/cockpit · segue o seletor</span></div>
> 875	                {(() => {
> 876	                  const s = cpBtc || {};
> 877	                  const sig = s.signals || {}, g = s.gates || {}, fl = s.flow || {}, ev = s.ev || {};
> 878	                  const dec = simDecision(selSym, cp);
> 879	                  const fmtPx = (v) => { const n = num(v); return !isFinite(n) ? '—' : n >= 100 ? n.toFixed(2) : n >= 1 ? n.toFixed(3) : n.toFixed(5); };
> 880	                  const kl = (klive && klive.length) ? klive[klive.length - 1] : null;
> 881	                  const liveP = (btcWs != null && !isNaN(btcWs)) ? btcWs : (kl ? kl.c : null);
> 882	                  const rsi1 = sig.rsi1m != null ? sig.rsi1m : (_rsi.length ? _rsi[_rsi.length - 1] : null);
> 883	                  const rsi15 = sig.rsi15m;
> 884	                  const chg = (kl && kl.o) ? ((kl.c - kl.o) / kl.o) * 100 : null;
> 885	                  const snow = [];
> 886	                  if (rsi1 != null && rsi1 < _buyTh) snow.push({ t: `RSI 1m ${rsi1.toFixed(0)} < ${_buyTh} · sobrevenda`, cls: 'cx-up' });
> 887	                  if (rsi1 != null && rsi1 > _sellTh) snow.push({ t: `RSI 1m ${rsi1.toFixed(0)} > ${_sellTh} · sobrecompra`, cls: 'cx-down' });
> 888	                  if (fl.toxicity != null && fl.toxicity >= 0.6) snow.push({ t: `fluxo extremo · ${fl.imbalance < 0 ? 'venda' : 'compra'} agressora (tox ${fl.toxicity.toFixed(2)})`, cls: fl.imbalance < 0 ? 'cx-down' : 'cx-up' });
> 889	                  if (sig.trendCross === 'golden') snow.push({ t: 'golden cross · compra de trend', cls: 'cx-up' });
> 890	                  if (sig.trendCross === 'death') snow.push({ t: 'death cross · venda protetiva', cls: 'cx-down' });
> 891	                  if (g.regime === 'trend') snow.push({ t: 'regime TREND · TrendState posicionado', cls: 'cx-up' });
> 892	                  const recent = (cp.patterns && Array.isArray(cp.patterns.recent) ? cp.patterns.recent : []).filter((r) => r.symbol === selSym).slice(0, 5);
> 893	                  const tile = (k, v, cls) => (<div className="cx-hud-tile" key={k}><span className="cx-hud-k">{k}</span><span className={`cx-hud-v cx-mono ${cls || ''}`}>{v}</span></div>);
> 894	                  const sc = cndBig ? 200 / cndBig.H : 1;
> 895	                  return (
> 896	                    <React.Fragment>
> 897	                      {cndBig
> 898	                        ? <svg className="cx-candle" viewBox={`0 0 ${cndBig.W} 200`} preserveAspectRatio="none" aria-label={`Candles 1m do ${selSym} com sinais ao vivo`}>
> 899	                            {[0.25, 0.5, 0.75].map((gg, i) => <line key={i} className="grid" x1="0" x2={cndBig.W} y1={200 * gg} y2={200 * gg} />)}
> 900	                            {cndBig.candles.map((cc, i) => {
> 901	                              const last = i === cndBig.candles.length - 1;
> 902	                              return (<g key={i}>
> 903	                                <line className={cc.up ? 'wick-up' : 'wick-down'} x1={cc.wx} x2={cc.wx} y1={cc.wy1 * sc} y2={cc.wy2 * sc} />
> 904	                                <rect className={cc.up ? 'body-up' : 'body-down'} x={cc.x} y={cc.by * sc} width={cc.bw} height={Math.max(1, cc.bh * sc)} style={last ? { stroke: 'var(--cx-cyan)', strokeWidth: 1 } : null} />
> 905	                              </g>);
> 906	                            })}
> 907	                            {marks.map((m, i) => {
> 908	                              const c = cndBig.candles[m.i]; if (!c) return null;
> 909	                              if (m.type === 'buy') { const y = c.wy2 * sc + 6; return <polygon key={'m' + i} className={`cx-mark buy ${m.armed ? 'armed' : 'gated'}`} points={`${c.wx - 4},${y + 6} ${c.wx + 4},${y + 6} ${c.wx},${y}`}><title>{m.title}</title></polygon>; }
> 910	                              const y = c.wy1 * sc - 6; return <polygon key={'m' + i} className="cx-mark sell" points={`${c.wx - 4},${y - 6} ${c.wx + 4},${y - 6} ${c.wx},${y}`}><title>{m.title}</title></polygon>;
> 911	                            })}
> 912	                          </svg>
> 913	                        : <div className="cx-empty">{klErr ? 'klines indisponíveis (CORS/Binance)' : 'carregando candles…'}</div>}
> 914	
> 915	                      <div className={`cx-decision ${dec.cls}`}>
> 916	                        <span className="cx-dec-act">{dec.act}</span>
> 917	                        <span className="cx-dec-body"><b>{dec.head}.</b> {dec.reason}</span>
> 918	                      </div>
> 919	
> 920	                      <div className="cx-line">
> 921	                        <span className="l">Sinal nesta vela</span>
> 922	                        <span className="v">{snow.length ? snow.map((x, i) => <span key={i} className={`cx-badge ${x.cls}`}>{x.t}</span>) : <span className="cx-flat">nenhum sinal — monitorando</span>}</span>
> 923	                      </div>
> 924	
> 925	                      <div className="cx-hud-grid">
> 926	                        {tile('preço ao vivo', fmtPx(liveP), chg != null ? dirClass(chg) : '')}
> 927	                        {tile('vela O/H/L/C', kl ? `${fmtPx(kl.o)}/${fmtPx(kl.h)}/${fmtPx(kl.l)}/${fmtPx(kl.c)}` : '—')}
> 928	                        {tile('Δ vela', chg != null ? fmtPct(chg) : '—', chg != null ? dirClass(chg) : '')}
> 929	                        {tile('RSI 1m', rsi1 != null ? rsi1.toFixed(1) : '—', rsi1 != null ? (rsi1 < _buyTh ? 'cx-up' : rsi1 > _sellTh ? 'cx-down' : 'cx-flat') : '')}
> 930	                        {tile('RSI 15m', rsi15 != null ? rsi15.toFixed(1) : '—')}
> 931	                        {tile('regime', g.regime || '—', g.regime === 'trend' ? 'cx-up' : g.regime === 'bear' ? 'cx-down' : 'cx-flat')}
> 932	                        {tile('tendência 1h', `${sig.trendSlope || '—'} · ${sig.trendCross || 'none'}`)}
> 933	                        {tile('fluxo imb/tox', fl.imbalance != null ? `${fl.imbalance.toFixed(2)} / ${fl.toxicity != null ? fl.toxicity.toFixed(2) : '—'}` : '—', fl.imbalance != null ? (fl.imbalance < 0 ? 'cx-down' : 'cx-up') : '')}
> 934	                        {tile('compra liberada?', g.buyAllowed ? 'sim' : 'não', g.buyAllowed ? 'cx-up' : 'cx-down')}
> 935	                        {tile('EV vela gross/net', ev.grossPct != null ? `${fmtPct(ev.grossPct)} / ${fmtPct(ev.netPct)}` : '—', ev.netPct != null ? dirClass(ev.netPct) : '')}
> 936	                      </div>
> 937	
> 938	                      {g.reason && <div className="cx-note" style={{ marginTop: 4 }}><b>Doutrina do gate:</b> {g.reason}</div>}
> 939	
> 940	                      {recent.length > 0 && <React.Fragment>
> 941	                        <div className="cx-line" style={{ fontWeight: 700, marginTop: 6 }}><span className="l">Últimos sinais gravados</span><span className="v cx-flat" style={{ fontSize: '0.66rem' }}>desfecho @10min</span></div>
> 942	                        {recent.map((r, i) => (
> 943	                          <div className="cx-line" key={i}>
> 944	                            <span className="l cx-mono">{r.type} <span className="cx-flat" style={{ fontSize: '0.66rem' }}>RSI {r.ctx && r.ctx.rsi1m != null ? Math.round(r.ctx.rsi1m) : '—'} · reg {r.ctx ? r.ctx.regime : '—'}</span></span>
> 945	                            <span className={`v cx-mono ${r.ret10 != null ? dirClass(r.ret10) : ''}`}>{r.ret10 != null ? fmtPct(r.ret10) : '—'}</span>
> 946	                          </div>
> 947	                        ))}
> 948	                      </React.Fragment>}
> 949	
> 950	                      <div className="cx-note">HUD read-only dos dados REAIS que dirigem as decisões: preço/vela ao vivo (WS), RSI/regime/fluxo/gates do brain (poll 60s) e a decisão simulada (o que o sistema FARIA — sem enviar ordem). Segue o seletor de símbolo acima.</div>
> 951	                    </React.Fragment>
> 952	                  );
> 953	                })()}
> 954	              </div>
> 955	            </div>
> 956	
> 957	          </div>
> 958	
> 959	          <div className="cx-legend">
> 960	            <span className="li"><span className="cx-seal real" /> dado real agora</span>
> 961	            <span className="li" style={{ marginLeft: 'auto' }}>valores são os REAIS da conta — sem números fabricados.</span>
> 962	          </div>
> 963	
> 964	          <div className="cx-foot">
> 965	            <span>TradeUX · Fable Cockpit · read-only</span>
> 966	            <span>klines: Binance público · sinais: regime/flow jobs (mainnet)</span>
> 967	          </div>
> 968	
> 969	        </div>
> ```

## 🤖 Claude *(18:00:30)*

Agora tenho tudo. Vou verificar dois pontos específicos: (1) a linha 888 tem `fl.imbalance < 0` sem guard de null — preciso confirmar se pode crashar; (2) confirmar o balanceamento das tags com um parse real. Vou rodar uma verificação de balanceamento das divs na região e também confirmar que `fl.imbalance < 0` com null não é crash (é só comparação, retorna false).

## 🤖 Claude *(18:00:38)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrux-tradeux/471cb4d6-e001-49d9-94b4-3b7ebe9b0f00/scratchpad 2>/dev/null || cd /tmp\n# Extrai a se\u00e7\u00e3o JSX modificada (795-955) e conta div de abertura/fechamento pra sanidade\npython3 - <<'PY'\nf='/home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js'\nlines=open(f).read().split('\\n')\nseg='\\n'.join(lines[794:955])  # linhas 795-955 (1-indexed)\nimport re\nopens=len(re.findall(r'<div\\b', seg))\ncloses=len(re.findall(r'</div>', seg))\n# self-closing divs? none expected\nselfclose=len(re.findall(r'<div\\b[^>]*/>', seg))\nprint('div open tags:', opens, '| </div>:', closes, '| self-closing div:', selfclose)\nprint('React.Fragment open:', len(re.findall(r'<React\\.Fragment', seg)), '| close:', len(re.findall(r'</React\\.Fragment>', seg)))\nprint('cx-panel occurrences:', seg.count('cx-panel\"'), 'glow panels:', seg.count('cx-panel glow'))\nPY",
  "description": "Count div balance in modified JSX region"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> div open tags: 26 | </div>: 26 | self-closing div: 0
> React.Fragment open: 5 | close: 5
> cx-panel occurrences: 0 glow panels: 3
> ```

## 🤖 Claude *(18:00:41)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "# Verifica se o null-safety de fl.imbalance<0 (linha 888) \u00e9 problema: em JS null<0 \u00e9 false, undefined<0 \u00e9 false \u2014 sem crash.\nnode -e \"let fl={}; console.log('undefined<0 =', fl.imbalance<0); fl.imbalance=null; console.log('null<0 =', fl.imbalance<0); console.log('(null).toFixed crashes?');\" 2>&1\n# Tamb\u00e9m confirma que grep do vite build passou de fato pela imagem\ndocker images 2>/dev/null | grep -i tradeux-frontend | head -3 || echo \"docker images n/a\"",
  "description": "Verify null comparison safety and docker image"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> undefined<0 = false
> null<0 = false
> (null).toFixed crashes?
> tradeux-frontend:latest                                 5b41484f70ba         69MB             0B
> ```

## 🤖 Claude *(18:01:02)*

Balanceamento confirmado (26/26 divs, 5/5 Fragments, 3 panels glow — dois na row-2 mesclada + um na row-7). Agora vou confirmar os pontos remanescentes: o guard de `fl.imbalance < 0` na linha 888 está dentro de `if (fl.toxicity != null && fl.toxicity >= 0.6)` — mas `fl.imbalance` pode ser null ali. Comparações com null retornam false sem crash (confirmado). Verifico só se há algum `.toFixed()` sem guard e o `cndBig` guard no candle.

Verificação dos acessos críticos remanescentes no widget:

- **Linha 888** `fl.imbalance < 0`: dentro do gate `fl.toxicity != null && fl.toxicity >= 0.6`. Se `imbalance` for null/undefined, a comparação retorna `false` (sem crash) → cai no ramo "compra"/`cx-up`. Cosmético, não crash.
- **Linha 933** `fl.imbalance.toFixed(2)`: guardado por `fl.imbalance != null ? ...` — OK.
- **Linhas 886-887** `rsi1.toFixed(0)`: guardado por `rsi1 != null` — OK.
- **Linha 888** `fl.toxicity.toFixed(2)`: dentro do gate `fl.toxicity != null` — OK.
- **`recent`/`r.ctx`** (944): `r.ctx && r.ctx.rsi1m != null` e `r.ctx ? r.ctx.regime : '—'` — OK.
- **`dec`** sempre objeto: `simDecision` tem `return` em todos os ramos + `return` final incondicional (188) — nunca undefined.
- **`sc = 200/cndBig.H`**: só calculado quando usado dentro do bloco `cndBig ? ...` no SVG; e a const na 894 usa `cndBig ? 200/cndBig.H : 1` — sem divisão por zero (H=440 fixo). viewBox `0 0 W 200`, geometria multiplicada por `sc=200/440≈0.4545` → mapeia [0,440] para [0,200]. Correto.

Vou fazer uma última verificação: confirmar que `cndBig.candles[m.i]` e o guard `if (!c) return null` cobrem o caso de `marks` apontar índice fora de range, e checar rapidamente o `.eslintrc` para no-unused-vars que poderia ter travado o build (mas o build passou).

## 🤖 Claude *(18:01:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "# Confirma que a var `s` (linha 876) e `dec`,`snow`,`recent` etc n\u00e3o colidem com nomes externos do escopo (\u00e9 IIFE, escopo pr\u00f3prio). Tamb\u00e9m checa uso de `ev`/`histB` fora.\ngrep -n \"const ev\\b\\| ev =\\|const env\\b\" /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js | head\necho \"---- confirm React import present ----\"\ngrep -n \"^import React\" /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js\necho \"---- vars marks/klive/cndBig/_rsi/_buyTh/_sellTh referenced in ROW7 all defined at component scope (lines <320) ----\"\ngit -C /home/gcrux-tradeux/tradeux -c safe.directory='*' log --oneline -1 -- frontend/src/private/Cockpit/Cockpit.js",
  "description": "Check scope collisions and imports"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 156:  const env = cp.env || {};
> 320:  const env = cp.env || null;
> 430:                      const ev = (s.ev && s.ev.netPct != null) ? s.ev.netPct : null;
> 877:                  const sig = s.signals || {}, g = s.gates || {}, fl = s.flow || {}, ev = s.ev || {};
> ---- confirm React import present ----
> 1:import React, { useState, useEffect } from 'react';
> ---- vars marks/klive/cndBig/_rsi/_buyTh/_sellTh referenced in ROW7 all defined at component scope (lines <320) ----
> 266d398 feat(cockpit): trilhas [PAPER] de trend por estado + widget ao vivo + MARKET:TREND_BREADTH
> ```

## 🤖 Claude *(18:01:54)*

Tudo confirmado. As consts do ROW7 (`ev` linha 877, `s`, `sig`, `g`, `fl`, `dec`, `snow`, `recent`, `tile`, `sc`) estão todas dentro da IIFE `(() => {...})()` própria (escopo isolado) — nenhuma colisão com o `env`/`ev` de escopos externos. `React` importado. Consts component-level (`marks`, `klive`, `cndBig`, `_rsi`, `_buyTh`, `_sellTh`, `btcWs`, `cpBtc`, `cp`, `selSym`, `klErr`) todas definidas antes da linha 320, no escopo da função `Cockpit()`, acessíveis no JSX. Análise completa.

---

# VEREDITO: PASS

Mudança **read-only** de frontend, sem toque em backend/money-path/beholder. `vite build` passou (imagem `tradeux-frontend:latest` construída). Revisão focada em crash de runtime, balanceamento JSX, escala do candle e totalidade de `simDecision`.

## (a) RUNTIME — sem crash

Todos os acessos potencialmente nulos estão guardados. Arquivo: `/home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js`

- `cpBtc=null` (símbolo sem dados no brain): coberto por `const s = cpBtc || {}` (L876) e desestruturação com defaults `s.signals||{}, s.gates||{}, s.flow||{}, s.ev||{}` (L877). Cada `tile` que acessa `.toFixed` tem guarda `!= null` explícita (L929-935).
- `cp.patterns` ausente: `cp.patterns && Array.isArray(cp.patterns.recent) ? ... : []` (L892) → `recent` sempre array; `recent.length > 0 &&` gateia o bloco (L940).
- `klive` null / vazio: `(klive && klive.length) ? ...[last] : null` (L880); `kl ?` em toda leitura de O/H/L/C (L927,884).
- `cndBig` null: ternário `cndBig ? <svg> : <div cx-empty>` (L897/913), com mensagem distinta por `klErr`.
- `sig/g/fl/ev` vazios: todos default `{}`; ausência renderiza `'—'` via os guards `!= null`.
- **`fl.imbalance < 0` sem guard (L888)** — verificado: dentro do gate `fl.toxicity != null && fl.toxicity >= 0.6`, e `null < 0`/`undefined < 0` retornam `false` em JS (confirmado por execução) → **não crasha**; no pior caso cai no ramo "compra"/verde. Cosmético, não bug de runtime. Já a leitura de valor (L933) usa `fl.imbalance.toFixed` corretamente guardada por `fl.imbalance != null`.
- `marks` apontando índice fora do range de `cndBig.candles`: `const c = cndBig.candles[m.i]; if (!c) return null;` (L908).

## (b) JSX balanceado após a mescla

Confirmado por contagem na região L795-955: **26 `<div>` / 26 `</div>`**, **5 `<React.Fragment>` / 5 `</React.Fragment>`**, **3 painéis `cx-panel glow`** (2 na `cx-row-2` mesclada + 1 na nova `cx-row` do HUD). O fechamento do `cx-grid` (L957) e `cx-legend`/`cx-foot` seguintes estão intactos. A mescla removeu corretamente o `</div>` de fechamento da ROW5 + a abertura `<div className="cx-row">` da ROW6 (o diff mostra as 2 linhas deletadas), mantendo os dois `cx-panel` como irmãos dentro do único `cx-row-2`. CSS `.cx-row-2` (grid `1fr 1fr` + colapso `@1100px`) coerente com `.cx-row`/`.cx-row-3` já existentes.

## (c) Escala do candle reusado

`sc = cndBig ? 200/cndBig.H : 1` (L894), `cndBig.H=440` fixo (L278) → `sc≈0.4545`. Geometria de `buildCandles` (`by`, `bh`, `wy1`, `wy2`, `lastY`) é gerada no domínio `[0,440]`; multiplicar por `sc` mapeia para `[0,200]`, exatamente o `viewBox="0 0 W 200"` (L898). Sem divisão por zero (`H` constante > 0). Marcadores usam `c.wy2*sc`/`c.wy1*sc` com o mesmo fator. **Desenha certo.** `preserveAspectRatio="none"` mantém o comportamento do candle grande.

## (d) `simDecision` sempre retorna objeto completo

`/home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js` L153-189: 7 ramos `return {act,cls,head,reason}` (HALT, farm-DCA, trend-qty, bear/unknown, não-promovido, compra, flow-veta) **+ `return` final incondicional** (L188). Nenhum caminho retorna `undefined`. `dec.cls` sempre casa com uma variante CSS existente (`halt/sell/hold/wait/buy/wait/ready`) — todas definidas no `cockpit.css` novo.

## Achados

- **[LOW / cosmético]** L888: `fl.imbalance < 0` sem guarda de `null` decide o texto "venda/compra agressora" e a cor. Se `toxicity>=0.6` mas `imbalance` vier `null`, mostra "compra agressora"/verde por padrão (comparação `null<0=false`). Não crasha; só pode rotular o lado errado num caso de borda de dados parciais. Alinhar com o guard de L933 (`imbalance != null`) seria mais correto, mas é não-bloqueante.
- **[INFO]** `dec.reason` da variante HALT interpola `env.haltSource` de `cp.env` (via `simDecision`), coerente com o resto do cockpit; sem risco.

## Testes que eu rodaria

1. **Símbolo sem dados no brain**: selecionar um símbolo cujo `cockpit.symbols[sym]` não exista → `cpBtc=null`. Esperado: HUD renderiza com `'—'` nos tiles, decisão via `simDecision` (cai em CAIXA/bear-unknown), zero exceção no console.
2. **`cp.patterns` ausente** (resposta antiga/parcial de `/analysis/cockpit`): mockar `cockpit` sem `patterns` → bloco "Últimos sinais" some, sem crash.
3. **klines indisponíveis** (bloquear `api.binance.com`/`data-api.binance.vision` no devtools): `cndBig=null` → placeholder `cx-empty` com texto de `klErr`; HUD continua renderizando decisão/tiles.
4. **WS preço null** (`btcWs` indefinido antes do primeiro tick): `liveP` cai no `kl.c`; `klive` volta a `klines` cru — verificar candle desenha e "preço ao vivo" não fica `NaN` (fmtPx trata `!isFinite`).
5. **Responsivo**: viewport < 1100px → `cx-row-2` colapsa para 1 coluna (os dois painéis Paper empilham); ≥1100px lado a lado 1fr/1fr.
6. **`toxicity>=0.6` com `imbalance=null`**: confirmar o rótulo do badge (achado LOW) — sanity visual.
7. **Troca de seletor de símbolo** (BTC→LTC→ADA): HUD segue `selSym`, candle/RSI/decisão recomputam, sem stale nem exceção.

## Recomendação de merge

**PODE MERGEAR.** Mudança puramente cosmética/read-only, guards completos, JSX balanceado, escala do candle e `simDecision` corretos. Único item aberto é o LOW cosmético de L888 (rótulo do lado do fluxo quando `imbalance=null`) — opcional endurecer para `fl.imbalance != null && fl.imbalance < 0` num follow-up, não bloqueia. Recomendo um smoke visual pós-deploy nos 4 símbolos (BTC/LTC/BNB/ADA) e com klines bloqueadas, dado que é o site live.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-05 - agent-adfd61319aeaf80ac]]
> * **Próxima Sessão**: [[2026-07-05 - agent-aed41526b2d0082ee]]
%% --- TIMELINE END --- %%

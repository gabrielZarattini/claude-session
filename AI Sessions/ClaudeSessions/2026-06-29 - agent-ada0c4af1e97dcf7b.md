# Session agent-ada0c4af1e97dcf7b
**Date:** 2026-06-29 | **Session ID:** `agent-ada0c4af1e97dcf7b`

---

## 👤 User *(19:20:46)*

Revise como GATE DE APROVAÇÃO (merge) o novo "laboratório de padrões" do TradeUX — 5 arquivos NOVOS, nenhum existente modificado. É pesquisa pura sobre klines públicas (fase de descoberta de padrões → simulação OOS), ZERO money-path/DB/ordens/live. O dono pediu "construir o lab primeiro, trazer pra aprovar".

Arquivos (em backend/scripts/):
- lib/labkit.js (fetch+indicadores+estatística+split+forwardReturn)
- lib/patterns.js (~40 padrões pré-registrados, compartilhado pelas 2 fases)
- pattern-discover.js (Fase 1: descoberta in-sample, FDR no gross, holdout trancado)
- pattern-validate.js (Fase 2: valida no holdout, bootstrap CI, gross=direção/net=acionável)
- sim/labkit.test.js (45 asserts; suíte completa 20/20 OK)

Avalie:
1. **Design/manutenibilidade**: a fronteira labkit (kit) + patterns (universo compartilhado) + 2 scripts de fase é sã? O fato de patterns.js ser compartilhado pelas 2 fases (evita drift entre os lados da parede) é o desenho certo?
2. **Aderência à convenção** do repo: segue o estilo de scripts/backtest.js (self-contained-ish, indicadores Wilder, exec no open seguinte, saída em backtest-results/, comentários pt-BR)? Reusa o que devia ou duplica indelevelmente? (Nota: backtest.js roda um IIFE no require → não dá pra reusar fácil; por isso labkit re-implementa.)
3. **Risco**: algo aqui pode tocar o sistema vivo (fetch bate em api.binance.com — tudo bem? rate-limit? grava só em backtest-data[gitignored]/backtest-results)? algum efeito colateral inesperado?
4. **Honestidade metodológica** como código: a parede (split trancado), a correção de múltiplos testes e a separação gross/net são suficientes pra NÃO entregar falso-positivo? Falta algo crítico (ex.: o overlap já é tratado por thin; o p-valor é aprox normal)?
5. **must-fix vs nice-to-have** antes de eu apresentar ao dono e (talvez) commitar.

Veredito: APPROVE / APPROVE COM SUGESTÕES / REQUEST CHANGES / BLOCK, com racional e a lista must-fix vs nice-to-have. Cite file:line.

## 🤖 Claude *(19:20:48)*

Vou carregar o contexto e revisar os 5 arquivos novos.

## 🤖 Claude *(19:20:50)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat /home/gcrux-tradeux/HANDOFF.md 2>/dev/null | head -100; echo \"=====CLAUDE.md=====\"; cat /home/gcrux-tradeux/tradeux/CLAUDE.md 2>/dev/null | head -120",
  "description": "Read HANDOFF and CLAUDE context files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> # TradeUX — HANDOFF (single source of truth)
> 
> > ShakeHands continuity doc. `/handson` reads this FIRST. Newest record at the bottom.
> > Project: **TradeUX** — Beholder-based multi-coin Binance Spot bot + LLM agent (**mainnet/testnet dual-env**).
> > Updated: **2026-06-26** · Phase: **GO-LIVE MAINNET — 🔴 LIVE (`halted=false`) · PARADO-MAS-ARMADO** (capital parqueado como combustível do bull; regime BEAR → supervisor NO-OP) · `Vivo==master==origin==701b7e7` · ⚠️ runtime não-git desta sessão: `.env FLOW_NOTIFY_ENABLED=false` + `AGENT_HEARTBEAT_STALE_MS=2700000`; `tradeux-agent/.env INTERVAL=900000`+`MAX_ROUNDS=10` · ver SEAL 2026-06-26 no rodapé · *(linha histórica abaixo)* · **Canary FARM-ONLY** (vendas no-loss id10/12/14 — **AGORA FUNCIONAM**; compras off) · **SESSÃO 21/jun (maratona): incidente Earn auto-subscribe diagnosticado+resolvido + 4 bugs corrigidos/gated/deployados** → `c6d0853` (dailyCap conta `LD*` do Earn = fim do HALT-falso), `457e25a` (silencia PUSH `[PAPER]` + alerta Telegram em falha real), **`fb932a1` (venda do Farm EDGE→LEVEL-trigger = 1ª saída no-loss do Farm a EXECUTAR no mainnet)** → **LTC vendido +$0,49** (ordem 264 @ $44,54, FARM_DCA→0, equity **$149,39**) · ⚠️ **runtime não-git (reaplicar se reset):** `.env MAX_ORDER_NOTIONAL_USDT=25→50` (band-aid: o teto bloqueava a VENDA de $40), DB `monitors`#2 `*:BOOK isActive=1` · proteções: cap diário −5%, teto **$50/ordem**, Farm $25/símbolo, riskGuard, pânico, painel de grupos · Meta: **realista ≈ flat com ~$149** · Vivo==master==origin==**`6cec694`** (re-revisão de design 2026-06-22 **100% ZERADA** — só RBAC=DEFER; agente caiu por toggle ZDR do OpenRouter e VOLTOU; ver SEAL 2026-06-24 no rodapé)
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
> =====CLAUDE.md=====
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
> 
> - **Operational DB = MySQL in the bundled Docker stack** (source of truth for orders,
>   settings, automations). Self-contained — `./setup.sh` brings up `db` + `backend` +
>   `frontend` on an isolated network/volume. This is the default and the validated path.
> - **Memory / RAG = Supabase pgvector**, in a dedicated `tradeux_memory` database — kept
>   separate from the operational DB. (Agent memory layer is a later milestone.)
> - The backend uses Sequelize and speaks **both MySQL and Postgres**; migrations are
>   portable (CI proves migrate+seed on both). The Supabase override
>   (`docker-compose.supabase.yml`) exists for running the operational DB on Postgres
>   instead, but the chosen setup keeps operational on the bundled MySQL.
> - **Production fronting**: behind CloudPanel/Cloudflare set `WEB_BIND=127.0.0.1` and a
>   free `WEB_PORT` (e.g. 8090), and the reverse proxy **must enable WebSocket upgrade**
>   (the `/ws` endpoint depends on it). Run as the site's own system user (e.g.
>   `gcrux-tradeux`), not root. `REACT_APP_*` URLs are baked into the React build, so they
>   must be set correctly **before** building the frontend image.
> 
> > The backend **must be able to reach Binance** — run it where Binance's API is not
> > geo-blocked. Switching the DB to Supabase does not change this.
> 
> ## Commands
> 
> ### Full stack (Docker)
> ```bash
> ./setup.sh            # one-command bootstrap: create .env, generate secrets, validate, up
> make up               # = ./setup.sh
> make logs / ps / restart / down
> make backup-state     # backup CIFRADO do estado (DB + logs + .env) — read-only
> make reset-db CONFIRM=RESET-DB  # backup + apaga SO o banco (preserva backend_logs/risk_state)
> make restore-state    # restaura risk_state/daily_cap de um backup cifrado
> make migrate / seed   # run sequelize migrate / seed inside the backend container
> 
> # Supabase/Postgres as the operational DB (no local MySQL):
> docker compose -f docker-compose.yml -f docker-compose.supabase.yml up -d --build backend frontend
> ```
> `setup.sh` auto-generates `JWT_SECRET` (32 bytes hex) and `AES_KEY` (16 bytes = 32 chars).
> On first run it stops if required `.env` fields (DB passwords, panel login, Binance keys)
> are blank — fill them and re-run. The backend container's `docker-entrypoint.sh` runs
> `db:migrate` + `db:seed:all` (idempotent) on every boot.
> 
> ### Backend (host dev, `backend/`)
> ```bash
> npm run dev           # nodemon + dotenv
> npm start             # node -r dotenv/config ./src/server
> npm run migratedb     # npx sequelize-cli db:migrate
> npm run seeddb        # npx sequelize-cli db:seed:all
> # Run a single migration: npx sequelize-cli db:migrate --to <YYYYMMDD-name.js>
> # Undo last:             npx sequelize-cli db:migrate:undo
> ```
> Sequelize config is `backend/config/` and reads `DB_*` from env. Seeders use
> `seederStorage: 'sequelize'` so `db:seed:all` is idempotent. There are no unit tests; the
> CI's "tests" are migrate+seed (both dialects) and the agent `--check` integration.
> 
> ### Frontend (`frontend/`) — Vite/React
> ```bash
> npm run dev           # vite dev server
> npm run build         # production bundle (what CI and the Docker image run)
> npm run preview
> ```
> 
> ### MCP + agent
> ```bash
> ```

## 🤖 Claude *(19:20:52)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && ls -la backend/scripts/lib/labkit.js backend/scripts/lib/patterns.js backend/scripts/pattern-discover.js backend/scripts/pattern-validate.js backend/scripts/sim/labkit.test.js 2>&1; echo \"=====wc=====\"; wc -l backend/scripts/lib/labkit.js backend/scripts/lib/patterns.js backend/scripts/pattern-discover.js backend/scripts/pattern-validate.js backend/scripts/sim/labkit.test.js 2>&1",
  "description": "List and count the 5 new files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> -rw-rw-r-- 1 gcrux-tradeux gcrux-tradeux 19794 Jun 29 16:17 backend/scripts/lib/labkit.js
> -rw-rw-r-- 1 gcrux-tradeux gcrux-tradeux  7102 Jun 29 16:11 backend/scripts/lib/patterns.js
> -rw-rw-r-- 1 gcrux-tradeux gcrux-tradeux 12629 Jun 29 16:17 backend/scripts/pattern-discover.js
> -rw-rw-r-- 1 gcrux-tradeux gcrux-tradeux  9807 Jun 29 16:17 backend/scripts/pattern-validate.js
> -rw-rw-r-- 1 gcrux-tradeux gcrux-tradeux  7016 Jun 29 16:17 backend/scripts/sim/labkit.test.js
> =====wc=====
>   359 backend/scripts/lib/labkit.js
>    70 backend/scripts/lib/patterns.js
>   156 backend/scripts/pattern-discover.js
>   131 backend/scripts/pattern-validate.js
>   104 backend/scripts/sim/labkit.test.js
>   820 total
> ```

## 🤖 Claude *(19:20:54)*

Vou ler os 5 arquivos completos.

## 🤖 Claude *(19:20:55)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/scripts/lib/labkit.js"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env node
> 2	'use strict';
> 3	/*
> 4	 * TradeUX — labkit: kit compartilhado do LABORATÓRIO DE PADRÕES.
> 5	 * Self-contained (só built-ins do Node), no mesmo espírito de scripts/backtest.js.
> 6	 *
> 7	 * Fornece, em um só lugar, as peças que tanto a DESCOBERTA (pattern-discover.js, Fase 1)
> 8	 * quanto a VALIDAÇÃO (pattern-validate.js, Fase 2) precisam — e que têm que ser IDÊNTICAS
> 9	 * nas duas pontas pra a "parede" entre amostra e holdout fazer sentido:
> 10	 *
> 11	 *   1) FETCH de klines estendido (mantém o taker-buy-volume p/ um PROXY de fluxo histórico),
> 12	 *      com cache em disco SEM colidir com os caches do backtest.js (sufixo -ext).
> 13	 *   2) INDICADORES (Wilder) — RSI, SMA, EMA, ATR, ADX/±DI, Bollinger, MACD, ROC, vol realizada,
> 14	 *      máx/mín rolantes — todos alinhados ao índice, NaN no warmup (sem lookahead).
> 15	 *   3) RETORNO FUTURO net-de-fee SEM LOOKAHEAD — entrada no OPEN do candle seguinte ao sinal.
> 16	 *   4) ESTATÍSTICA HONESTA — t-stat de 1 amostra, p-valor (aprox. normal), correção de
> 17	 *      múltiplos testes Benjamini-Hochberg (FDR) e Bonferroni, "barra de ruído" sqrt(2 ln N),
> 18	 *      e bootstrap por BLOCOS (preserva autocorrelação) com RNG SEMEADO (reprodutível).
> 19	 *   5) SPLIT train/test TRANCADO POR TEMPO — a parede anti-overfitting.
> 20	 *
> 21	 * NADA aqui toca o money-path: é pesquisa pura sobre dados públicos. Zero deps do backend.
> 22	 */
> 23	const https = require('https');
> 24	const fs = require('fs');
> 25	const path = require('path');
> 26	
> 27	// ---------- diretórios / constantes ----------
> 28	const DATA_DIR = path.join(__dirname, '..', '..', 'backtest-data');
> 29	const OUT_DIR = path.join(__dirname, '..', '..', 'backtest-results');
> 30	const HOSTS = ['api.binance.com', 'data-api.binance.vision', 'api.binance.us'];
> 31	const MS_PER = { '1m': 60e3, '5m': 5 * 60e3, '15m': 15 * 60e3, '30m': 30 * 60e3, '1h': 3600e3, '2h': 2 * 3600e3, '4h': 4 * 3600e3, '1d': 24 * 3600e3 };
> 32	const FEE_DEFAULT = 0.001; // 0.1% por lado (taker spot) — mesma do backtest.js
> 33	
> 34	// ---------- estatística básica ----------
> 35	const sum = a => a.reduce((s, x) => s + x, 0);
> 36	const mean = a => (a.length ? sum(a) / a.length : 0);
> 37	function variance(a) { if (a.length < 2) return 0; const m = mean(a); return sum(a.map(x => (x - m) ** 2)) / (a.length - 1); } // amostral (n-1)
> 38	const std = a => Math.sqrt(variance(a));
> 39	function stdPop(a) { if (a.length < 1) return 0; const m = mean(a); return Math.sqrt(sum(a.map(x => (x - m) ** 2)) / a.length); } // populacional (Bollinger)
> 40	function median(a) { if (!a.length) return 0; const s = [...a].sort((x, y) => x - y); const m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; }
> 41	function quantile(a, q) { if (!a.length) return 0; const s = [...a].sort((x, y) => x - y); const pos = (s.length - 1) * q; const lo = Math.floor(pos), hi = Math.ceil(pos); return lo === hi ? s[lo] : s[lo] + (s[hi] - s[lo]) * (pos - lo); }
> 42	
> 43	// erf (Abramowitz-Stegun 7.1.26) → Phi (CDF normal) → p-valor bicaudal.
> 44	function erf(x) {
> 45	  const s = x < 0 ? -1 : 1; x = Math.abs(x);
> 46	  const t = 1 / (1 + 0.3275911 * x);
> 47	  const y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
> 48	  return s * y;
> 49	}
> 50	const normCdf = z => 0.5 * (1 + erf(z / Math.SQRT2));
> 51	// Teste t de 1 amostra contra 0. Aprox. NORMAL no p-valor (válida p/ n grande; n<30 é anti-conservador → flag amostra-pequena no relatório).
> 52	function tTest(arr) {
> 53	  const n = arr.length;
> 54	  if (n < 2) return { n, mean: n ? arr[0] : 0, std: 0, se: 0, t: 0, p: 1 };
> 55	  const m = mean(arr), s = std(arr), se = s / Math.sqrt(n);
> 56	  const t = se > 0 ? m / se : 0;
> 57	  const p = 2 * (1 - normCdf(Math.abs(t)));
> 58	  return { n, mean: m, std: s, se, t, p };
> 59	}
> 60	
> 61	// Benjamini-Hochberg: controla a FALSE DISCOVERY RATE em q. Recebe [{key,p}], devolve o limiar
> 62	// de p, o conjunto rejeitado (descobertas) e o ranking. É O anticorpo contra "achei 50 padrões
> 63	// significativos" quando 1000 foram testados (≈50 são falsos a p<0.05 só por acaso).
> 64	function benjaminiHochberg(tests, q = 0.05) {
> 65	  const m = tests.length;
> 66	  if (!m) return { q, m, pThreshold: 0, rejected: new Set(), ranked: [] };
> 67	  const ranked = [...tests].sort((a, b) => a.p - b.p).map((t, i) => ({ ...t, rank: i + 1, crit: ((i + 1) / m) * q }));
> 68	  let kMax = 0;
> 69	  for (const r of ranked) if (r.p <= r.crit) kMax = r.rank;
> 70	  const pThreshold = kMax ? (kMax / m) * q : 0;
> 71	  const rejected = new Set(ranked.filter(r => r.rank <= kMax).map(r => r.key));
> 72	  return { q, m, kMax, pThreshold, rejected, ranked };
> 73	}
> 74	const bonferroniThreshold = (m, alpha = 0.05) => (m ? alpha / m : 0);
> 75	// Barra de ruído: |t| esperado do MELHOR de N testes puramente aleatórios ~ sqrt(2 ln N).
> 76	// Um padrão só "vence o acaso de N tentativas" se |t| superar isto. Intuição, não teste formal.
> 77	const noiseBarT = m => (m > 1 ? Math.sqrt(2 * Math.log(m)) : 0);
> 78	
> 79	// RNG semeado (mulberry32) — bootstrap reprodutível (a suíte de sim e o relatório têm que bater byte-a-byte).
> 80	function mulberry32(seed) {
> 81	  let a = seed >>> 0;
> 82	  return function () { a |= 0; a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
> 83	}
> 84	// Bootstrap por BLOCOS móveis: reamostra blocos contíguos (preserva autocorrelação dos retornos)
> 85	// e devolve o IC percentil da MÉDIA. blockLen ~ sqrt(n) é um default razoável.
> 86	function blockBootstrapMeanCI(returns, { blockLen, nResamples = 2000, seed = 12345, ci = 0.95 } = {}) {
> 87	  const n = returns.length;
> 88	  if (n < 2) return { mean: mean(returns), lo: NaN, hi: NaN, n, pPos: NaN };
> 89	  const L = Math.max(1, blockLen || Math.round(Math.sqrt(n)));
> 90	  const rng = mulberry32(seed);
> 91	  const means = [];
> 92	  for (let r = 0; r < nResamples; r++) {
> 93	    let acc = 0, cnt = 0;
> 94	    while (cnt < n) {
> 95	      const start = Math.floor(rng() * Math.max(1, n - L + 1));
> 96	      for (let j = 0; j < L && cnt < n; j++) { acc += returns[start + j]; cnt++; }
> 97	    }
> 98	    means.push(acc / n);
> 99	  }
> 100	  means.sort((a, b) => a - b);
> 101	  const a = (1 - ci) / 2;
> 102	  return { mean: mean(returns), lo: quantile(means, a), hi: quantile(means, 1 - a), n, pPos: means.filter(x => x > 0).length / means.length };
> 103	}
> 104	
> 105	// ---------- indicadores (Wilder; arrays alinhados ao índice, NaN no warmup) ----------
> 106	function rsiSeries(close, period = 14) {
> 107	  const out = Array(close.length).fill(NaN);
> 108	  if (close.length <= period) return out;
> 109	  let gain = 0, loss = 0;
> 110	  for (let i = 1; i <= period; i++) { const d = close[i] - close[i - 1]; if (d >= 0) gain += d; else loss -= d; }
> 111	  let ag = gain / period, al = loss / period;
> 112	  out[period] = al === 0 ? 100 : 100 - 100 / (1 + ag / al);
> 113	  for (let i = period + 1; i < close.length; i++) {
> 114	    const d = close[i] - close[i - 1];
> 115	    ag = (ag * (period - 1) + (d > 0 ? d : 0)) / period;
> 116	    al = (al * (period - 1) + (d < 0 ? -d : 0)) / period;
> 117	    out[i] = al === 0 ? 100 : 100 - 100 / (1 + ag / al);
> 118	  }
> 119	  return out;
> 120	}
> 121	function smaSeries(values, period) {
> 122	  const out = Array(values.length).fill(NaN); let s = 0;
> 123	  for (let i = 0; i < values.length; i++) { s += values[i]; if (i >= period) s -= values[i - period]; if (i >= period - 1) out[i] = s / period; }
> 124	  return out;
> 125	}
> 126	function emaSeries(values, period) {
> 127	  const out = Array(values.length).fill(NaN); const k = 2 / (period + 1); let ema = 0, s = 0;
> 128	  for (let i = 0; i < values.length; i++) {
> 129	    if (i < period) { s += values[i]; if (i === period - 1) { ema = s / period; out[i] = ema; } continue; }
> 130	    ema = values[i] * k + ema * (1 - k); out[i] = ema;
> 131	  }
> 132	  return out;
> 133	}
> 134	function trueRange(high, low, close, i) {
> 135	  if (i === 0) return high[i] - low[i];
> 136	  return Math.max(high[i] - low[i], Math.abs(high[i] - close[i - 1]), Math.abs(low[i] - close[i - 1]));
> 137	}
> 138	function atrSeries(high, low, close, period = 14) {
> 139	  const out = Array(close.length).fill(NaN);
> 140	  if (close.length <= period) return out;
> 141	  let tr = 0; for (let i = 1; i <= period; i++) tr += trueRange(high, low, close, i);
> 142	  let atr = tr / period; out[period] = atr;
> 143	  for (let i = period + 1; i < close.length; i++) { atr = (atr * (period - 1) + trueRange(high, low, close, i)) / period; out[i] = atr; }
> 144	  return out;
> 145	}
> 146	function dmiSeries(high, low, close, period = 14) {
> 147	  const n = close.length;
> 148	  const adx = Array(n).fill(NaN), pdiArr = Array(n).fill(NaN), mdiArr = Array(n).fill(NaN);
> 149	  if (n <= 2 * period) return { adx, pdi: pdiArr, mdi: mdiArr };
> 150	  const plusDM = Array(n).fill(0), minusDM = Array(n).fill(0), tr = Array(n).fill(0);
> 151	  for (let i = 1; i < n; i++) {
> 152	    const up = high[i] - high[i - 1], dn = low[i - 1] - low[i];
> 153	    plusDM[i] = (up > dn && up > 0) ? up : 0;
> 154	    minusDM[i] = (dn > up && dn > 0) ? dn : 0;
> 155	    tr[i] = trueRange(high, low, close, i);
> 156	  }
> 157	  let sTR = 0, sP = 0, sM = 0;
> 158	  for (let i = 1; i <= period; i++) { sTR += tr[i]; sP += plusDM[i]; sM += minusDM[i]; }
> 159	  const dx = Array(n).fill(NaN);
> 160	  const dxAt = (i, sP, sM, sTR) => {
> 161	    const pdi = sTR === 0 ? 0 : 100 * sP / sTR, mdi = sTR === 0 ? 0 : 100 * sM / sTR;
> 162	    pdiArr[i] = pdi; mdiArr[i] = mdi;
> 163	    const den = pdi + mdi; return den === 0 ? 0 : 100 * Math.abs(pdi - mdi) / den;
> 164	  };
> 165	  dx[period] = dxAt(period, sP, sM, sTR);
> 166	  for (let i = period + 1; i < n; i++) {
> 167	    sTR = sTR - sTR / period + tr[i]; sP = sP - sP / period + plusDM[i]; sM = sM - sM / period + minusDM[i];
> 168	    dx[i] = dxAt(i, sP, sM, sTR);
> 169	  }
> 170	  let a = 0; for (let i = period + 1; i <= 2 * period; i++) a += dx[i]; a /= period;
> 171	  adx[2 * period] = a;
> 172	  for (let i = 2 * period + 1; i < n; i++) { a = (a * (period - 1) + dx[i]) / period; adx[i] = a; }
> 173	  return { adx, pdi: pdiArr, mdi: mdiArr };
> 174	}
> 175	// Bollinger: std POPULACIONAL (convenção). pctB = (close-lower)/(upper-lower); bw = (upper-lower)/mid.
> 176	function bollingerSeries(close, period = 20, k = 2) {
> 177	  const n = close.length;
> 178	  const mid = Array(n).fill(NaN), upper = Array(n).fill(NaN), lower = Array(n).fill(NaN), pctB = Array(n).fill(NaN), bw = Array(n).fill(NaN);
> 179	  for (let i = period - 1; i < n; i++) {
> 180	    const w = close.slice(i - period + 1, i + 1);
> 181	    const m = mean(w), sd = stdPop(w);
> 182	    mid[i] = m; upper[i] = m + k * sd; lower[i] = m - k * sd;
> 183	    const den = upper[i] - lower[i];
> 184	    pctB[i] = den > 0 ? (close[i] - lower[i]) / den : NaN;
> 185	    bw[i] = m > 0 ? den / m : NaN;
> 186	  }
> 187	  return { mid, upper, lower, pctB, bw };
> 188	}
> 189	function macdSeries(close, fast = 12, slow = 26, signalP = 9) {
> 190	  const ef = emaSeries(close, fast), es = emaSeries(close, slow);
> 191	  const macd = close.map((_, i) => (Number.isFinite(ef[i]) && Number.isFinite(es[i])) ? ef[i] - es[i] : NaN);
> 192	  // EMA do macd começando no 1º índice finito (evita contaminar com NaN do warmup).
> 193	  const signal = Array(close.length).fill(NaN); const k = 2 / (signalP + 1);
> 194	  let first = macd.findIndex(Number.isFinite), ema = 0, s = 0, c = 0;
> 195	  if (first >= 0) {
> 196	    for (let i = first; i < close.length; i++) {
> 197	      if (c < signalP) { s += macd[i]; c++; if (c === signalP) { ema = s / signalP; signal[i] = ema; } continue; }
> 198	      ema = macd[i] * k + ema * (1 - k); signal[i] = ema;
> 199	    }
> 200	  }
> 201	  const hist = macd.map((v, i) => (Number.isFinite(v) && Number.isFinite(signal[i])) ? v - signal[i] : NaN);
> 202	  return { macd, signal, hist };
> 203	}
> 204	function rocSeries(close, period = 10) {
> 205	  const out = Array(close.length).fill(NaN);
> 206	  for (let i = period; i < close.length; i++) out[i] = close[i - period] !== 0 ? close[i] / close[i - period] - 1 : NaN;
> 207	  return out;
> 208	}
> 209	// máx/mín dos ÚLTIMOS `period` candles ATÉ i-1 (exclui i) — p/ detectar rompimento causal: close[i] > priorHigh.
> 210	function rollingPriorHigh(arr, period) {
> 211	  const out = Array(arr.length).fill(NaN);
> 212	  for (let i = period; i < arr.length; i++) { let mx = -Infinity; for (let j = i - period; j < i; j++) if (arr[j] > mx) mx = arr[j]; out[i] = mx; }
> 213	  return out;
> 214	}
> 215	function rollingPriorLow(arr, period) {
> 216	  const out = Array(arr.length).fill(NaN);
> 217	  for (let i = period; i < arr.length; i++) { let mn = Infinity; for (let j = i - period; j < i; j++) if (arr[j] < mn) mn = arr[j]; out[i] = mn; }
> 218	  return out;
> 219	}
> 220	function realizedVolSeries(close, window, barsPerYear) {
> 221	  const out = Array(close.length).fill(NaN);
> 222	  const lr = close.map((c, i) => (i ? Math.log(c / close[i - 1]) : 0));
> 223	  for (let i = window; i < close.length; i++) out[i] = std(lr.slice(i - window + 1, i + 1)) * Math.sqrt(barsPerYear);
> 224	  return out;
> 225	}
> 226	// percentil rolante de um valor dentro da própria janela passada (0..1) — p/ "ATR baixo/alto" relativo.
> 227	function rollingPercentile(arr, window) {
> 228	  const out = Array(arr.length).fill(NaN);
> 229	  for (let i = 0; i < arr.length; i++) {
> 230	    if (i < window || !Number.isFinite(arr[i])) continue;
> 231	    const w = []; for (let j = i - window + 1; j <= i; j++) if (Number.isFinite(arr[j])) w.push(arr[j]);
> 232	    if (w.length < 2) continue;
> 233	    out[i] = w.filter(x => x <= arr[i]).length / w.length;
> 234	  }
> 235	  return out;
> 236	}
> 237	
> 238	// ---------- retorno futuro long, SEM lookahead — GROSS (direção) + NET (acionabilidade) ----------
> 239	// Sinal observado em i (indicadores usam closes[0..i]). Entrada no OPEN de i+1, saída no OPEN de i+1+h.
> 240	//   gross = open(i+1+h)/open(i+1) - 1            → mede se o PREÇO se move (predição direcional).
> 241	//   net   = open(i+1+h)*(1-fee)/(open(i+1)*(1+fee)) - 1  → desconta a fee round-trip (acionável no spot long).
> 242	// A distinção é crítica: em horizonte curto net ≈ -fee p/ QUALQUER sinal (o move médio é ~0), então
> 243	// usar net p/ "direção" confunde fee-drag com edge. Direção testa-se no GROSS; acionabilidade no NET.
> 244	function forwardReturn(candles, i, h, fee = FEE_DEFAULT) {
> 245	  const e = i + 1, x = i + 1 + h;
> 246	  if (x >= candles.length || e >= candles.length) return null;
> 247	  const eo = candles[e].open, xo = candles[x].open;
> 248	  if (!(eo > 0)) return null;
> 249	  return { gross: xo / eo - 1, net: (xo * (1 - fee)) / (eo * (1 + fee)) - 1 };
> 250	}
> 251	// compat: só o net long (usado por testes e por chamadas que só querem acionabilidade).
> 252	function forwardNetLong(candles, i, h, fee = FEE_DEFAULT) { const r = forwardReturn(candles, i, h, fee); return r ? r.net : null; }
> 253	
> 254	// ---------- split train/test TRANCADO por tempo (a parede) ----------
> 255	// Divide por ÍNDICE temporal: os primeiros (1-holdoutFrac) viram amostra de DESCOBERTA; o resto é HOLDOUT
> 256	// trancado (a Fase 1 NUNCA o lê). Devolve o timestamp de corte p/ a Fase 2 usar a MESMA fronteira.
> 257	function splitByTime(candles, holdoutFrac = 0.3) {
> 258	  const n = candles.length;
> 259	  const k = Math.max(1, Math.min(n - 1, Math.floor(n * (1 - holdoutFrac))));
> 260	  return { kIndex: k, cutMs: candles[k].t, inSample: candles.slice(0, k), holdout: candles.slice(k), nTotal: n };
> 261	}
> 262	
> 263	// ---------- fetch de klines estendido (com taker-buy-volume) + cache -ext ----------
> 264	function httpsGetJSON(host, pathUrl) {
> 265	  return new Promise((res, rej) => {
> 266	    https.get({ host, path: pathUrl, headers: { 'User-Agent': 'tradeux-labkit' } }, r => {
> 267	      let d = ''; r.on('data', c => d += c);
> 268	      r.on('end', () => { try { res({ status: r.statusCode, body: JSON.parse(d) }); } catch (e) { res({ status: r.statusCode, body: d }); } });
> 269	    }).on('error', rej);
> 270	  });
> 271	}
> 272	async function fetchKlinesExt(symbol, interval, days, end) {
> 273	  const barMs = MS_PER[interval] || 3600e3;
> 274	  const cacheFile = path.join(DATA_DIR, `${symbol}-${interval}-${days}d${end ? '-end' + end : ''}-ext.json`);
> 275	  if (fs.existsSync(cacheFile)) {
> 276	    const c = JSON.parse(fs.readFileSync(cacheFile, 'utf8'));
> 277	    if (c.length > 100) { console.log(`  [cache] ${symbol} ${interval}: ${c.length} candles`); return c; }
> 278	  }
> 279	  const endTime = end ? Date.parse(end + 'T00:00:00Z') : Date.now();
> 280	  const startTime = endTime - days * 24 * 3600e3;
> 281	  let cursor = startTime, all = [], host = null;
> 282	  for (const h of HOSTS) {
> 283	    const r = await httpsGetJSON(h, `/api/v3/klines?symbol=${symbol}&interval=${interval}&limit=1`).catch(() => null);
> 284	    if (r && r.status === 200 && Array.isArray(r.body)) { host = h; break; }
> 285	  }
> 286	  if (!host) throw new Error(`nenhum host Binance alcançável para ${symbol} (tentei ${HOSTS.join(', ')})`);
> 287	  while (cursor < endTime) {
> 288	    const url = `/api/v3/klines?symbol=${symbol}&interval=${interval}&startTime=${cursor}&limit=1000`;
> 289	    const r = await httpsGetJSON(host, url);
> 290	    if (r.status !== 200 || !Array.isArray(r.body) || r.body.length === 0) break;
> 291	    // k[5]=volume base, k[9]=taker buy base volume → fração compradora agressiva (proxy de fluxo histórico).
> 292	    const batch = r.body.map(k => ({ t: k[0], open: +k[1], high: +k[2], low: +k[3], close: +k[4], vol: +k[5], takerBuy: +k[9] }));
> 293	    all.push(...batch);
> 294	    cursor = batch[batch.length - 1].t + barMs;
> 295	    if (batch.length < 1000) break;
> 296	  }
> 297	  const seen = new Set(); const out = [];
> 298	  for (const c of all) { if (!seen.has(c.t)) { seen.add(c.t); out.push(c); } }
> 299	  out.sort((a, b) => a.t - b.t);
> 300	  fs.mkdirSync(DATA_DIR, { recursive: true });
> 301	  fs.writeFileSync(cacheFile, JSON.stringify(out));
> 302	  console.log(`  [fetch ${host}] ${symbol} ${interval}: ${out.length} candles`);
> 303	  return out;
> 304	}
> 305	
> 306	// ---------- catálogo de indicadores computados de uma vez (todos causais) ----------
> 307	// regimeBar: regime causal por barra usando as últimas `regimeWin` barras ATÉ i (bear se >60% < SMA200; senão
> 308	// trend se ADX>=25, range se <20, mixed). Espelha a lógica do regimeClassifier ao vivo, mas por-barra.
> 309	function computeIndicators(candles, interval) {
> 310	  const barMs = MS_PER[interval] || 3600e3;
> 311	  const barsPerYear = (365 * 24 * 3600e3) / barMs;
> 312	  const close = candles.map(c => c.close), high = candles.map(c => c.high), low = candles.map(c => c.low);
> 313	  const vol = candles.map(c => c.vol), takerBuy = candles.map(c => (Number.isFinite(c.takerBuy) ? c.takerBuy : NaN));
> 314	  const dmi = dmiSeries(high, low, close, 14);
> 315	  const atr = atrSeries(high, low, close, 14);
> 316	  const sma200 = smaSeries(close, 200);
> 317	  const boll = bollingerSeries(close, 20, 2);
> 318	  const macd = macdSeries(close, 12, 26, 9);
> 319	  const ind = {
> 320	    candles, interval, barMs, barsPerYear, close, high, low, vol,
> 321	    takerBuyFrac: vol.map((v, i) => (v > 0 && Number.isFinite(takerBuy[i]) ? takerBuy[i] / v : NaN)),
> 322	    rsi14: rsiSeries(close, 14),
> 323	    sma20: smaSeries(close, 20), sma50: smaSeries(close, 50), sma100: smaSeries(close, 100), sma200,
> 324	    adx: dmi.adx, pdi: dmi.pdi, mdi: dmi.mdi, atr,
> 325	    atrPct: atr.map((a, i) => (a > 0 && close[i] > 0 ? a / close[i] : NaN)),
> 326	    boll, macd, roc10: rocSeries(close, 10), roc20: rocSeries(close, 20),
> 327	    priorHigh20: rollingPriorHigh(high, 20), priorLow20: rollingPriorLow(low, 20),
> 328	    rvol: realizedVolSeries(close, 24, barsPerYear),
> 329	  };
> 330	  ind.atrPctPctile = rollingPercentile(ind.atrPct, 200);
> 331	  // regime causal por barra
> 332	  const regimeWin = 200;
> 333	  ind.regimeBar = Array(candles.length).fill('unknown');
> 334	  for (let i = 0; i < candles.length; i++) {
> 335	    if (i < regimeWin) continue;
> 336	    let below = 0, n = 0; const adxs = [];
> 337	    for (let j = i - regimeWin + 1; j <= i; j++) {
> 338	      if (Number.isFinite(sma200[j])) { n++; if (close[j] < sma200[j]) below++; }
> 339	      if (Number.isFinite(ind.adx[j])) adxs.push(ind.adx[j]);
> 340	    }
> 341	    if (n && below / n > 0.6) { ind.regimeBar[i] = 'bear'; continue; }
> 342	    const m = adxs.length ? mean(adxs) : 0;
> 343	    ind.regimeBar[i] = m >= 25 ? 'trend' : (m < 20 ? 'range' : 'mixed');
> 344	  }
> 345	  return ind;
> 346	}
> 347	
> 348	module.exports = {
> 349	  // dirs / const
> 350	  DATA_DIR, OUT_DIR, MS_PER, FEE_DEFAULT,
> 351	  // stats
> 352	  sum, mean, variance, std, stdPop, median, quantile, erf, normCdf, tTest,
> 353	  benjaminiHochberg, bonferroniThreshold, noiseBarT, mulberry32, blockBootstrapMeanCI,
> 354	  // indicadores
> 355	  rsiSeries, smaSeries, emaSeries, atrSeries, dmiSeries, bollingerSeries, macdSeries,
> 356	  rocSeries, rollingPriorHigh, rollingPriorLow, realizedVolSeries, rollingPercentile,
> 357	  // retorno / split / fetch / catálogo
> 358	  forwardReturn, forwardNetLong, splitByTime, httpsGetJSON, fetchKlinesExt, computeIndicators,
> 359	};
> 360	
> ```

## 🤖 Claude *(19:20:56)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/scripts/lib/patterns.js"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	'use strict';
> 2	/*
> 3	 * TradeUX — universo PRÉ-REGISTRADO de padrões do laboratório.
> 4	 * Compartilhado por pattern-discover.js (Fase 1) e pattern-validate.js (Fase 2): a definição
> 5	 * TEM que ser idêntica dos dois lados da parede, senão a validação no holdout não significa nada.
> 6	 *
> 7	 * Cada padrão: { name, family, dir, fn(d,i)->bool }, onde d = catálogo de indicadores (labkit.computeIndicators
> 8	 * + d.bwPctile) e i = índice da barra. fn é CAUSAL (só usa índices <= i). dir = direção esperada (rótulo):
> 9	 *   bull = sinal de COMPRA (acionável no spot); bear = sinal de SAÍDA/evitar (gate; no spot não vira short);
> 10	 *   flat = regime/contexto (sem direção forte).
> 11	 */
> 12	const fin = Number.isFinite;
> 13	
> 14	const PATTERNS = [
> 15	  // --- RSI (mean-reversion) ---
> 16	  { name: 'rsi_lt_25', family: 'rsi', dir: 'bull', fn: (d, i) => fin(d.rsi14[i]) && d.rsi14[i] < 25 },
> 17	  { name: 'rsi_lt_30', family: 'rsi', dir: 'bull', fn: (d, i) => fin(d.rsi14[i]) && d.rsi14[i] < 30 },
> 18	  { name: 'rsi_lt_35', family: 'rsi', dir: 'bull', fn: (d, i) => fin(d.rsi14[i]) && d.rsi14[i] < 35 },
> 19	  { name: 'rsi_gt_70', family: 'rsi', dir: 'bear', fn: (d, i) => fin(d.rsi14[i]) && d.rsi14[i] > 70 },
> 20	  { name: 'rsi_gt_75', family: 'rsi', dir: 'bear', fn: (d, i) => fin(d.rsi14[i]) && d.rsi14[i] > 75 },
> 21	  // --- tendência / SMA ---
> 22	  { name: 'above_sma200', family: 'trend', dir: 'bull', fn: (d, i) => fin(d.sma200[i]) && d.close[i] > d.sma200[i] },
> 23	  { name: 'below_sma200', family: 'trend', dir: 'bear', fn: (d, i) => fin(d.sma200[i]) && d.close[i] < d.sma200[i] },
> 24	  { name: 'sma_aligned_up', family: 'trend', dir: 'bull', fn: (d, i) => fin(d.sma20[i]) && fin(d.sma50[i]) && fin(d.sma200[i]) && d.close[i] > d.sma20[i] && d.sma20[i] > d.sma50[i] && d.sma50[i] > d.sma200[i] },
> 25	  { name: 'golden_cross_50_200', family: 'trend', dir: 'bull', fn: (d, i) => i > 0 && fin(d.sma50[i]) && fin(d.sma200[i]) && fin(d.sma50[i - 1]) && fin(d.sma200[i - 1]) && d.sma50[i - 1] <= d.sma200[i - 1] && d.sma50[i] > d.sma200[i] },
> 26	  { name: 'death_cross_50_200', family: 'trend', dir: 'bear', fn: (d, i) => i > 0 && fin(d.sma50[i]) && fin(d.sma200[i]) && fin(d.sma50[i - 1]) && fin(d.sma200[i - 1]) && d.sma50[i - 1] >= d.sma200[i - 1] && d.sma50[i] < d.sma200[i] },
> 27	  // --- ADX / DMI ---
> 28	  { name: 'adx_strong_up', family: 'adx', dir: 'bull', fn: (d, i) => fin(d.adx[i]) && d.adx[i] > 25 && d.pdi[i] > d.mdi[i] },
> 29	  { name: 'adx_strong_down', family: 'adx', dir: 'bear', fn: (d, i) => fin(d.adx[i]) && d.adx[i] > 25 && d.mdi[i] > d.pdi[i] },
> 30	  { name: 'adx_range_low', family: 'adx', dir: 'flat', fn: (d, i) => fin(d.adx[i]) && d.adx[i] < 20 },
> 31	  // --- Bollinger ---
> 32	  { name: 'boll_lower_break', family: 'boll', dir: 'bull', fn: (d, i) => fin(d.boll.lower[i]) && d.close[i] < d.boll.lower[i] },
> 33	  { name: 'boll_upper_break', family: 'boll', dir: 'bear', fn: (d, i) => fin(d.boll.upper[i]) && d.close[i] > d.boll.upper[i] },
> 34	  { name: 'boll_pctb_low', family: 'boll', dir: 'bull', fn: (d, i) => fin(d.boll.pctB[i]) && d.boll.pctB[i] < 0.05 },
> 35	  { name: 'boll_squeeze', family: 'boll', dir: 'flat', fn: (d, i) => fin(d.bwPctile[i]) && d.bwPctile[i] < 0.10 },
> 36	  // --- MACD ---
> 37	  { name: 'macd_cross_up', family: 'macd', dir: 'bull', fn: (d, i) => i > 0 && fin(d.macd.hist[i]) && fin(d.macd.hist[i - 1]) && d.macd.hist[i - 1] <= 0 && d.macd.hist[i] > 0 },
> 38	  { name: 'macd_cross_down', family: 'macd', dir: 'bear', fn: (d, i) => i > 0 && fin(d.macd.hist[i]) && fin(d.macd.hist[i - 1]) && d.macd.hist[i - 1] >= 0 && d.macd.hist[i] < 0 },
> 39	  { name: 'macd_pos', family: 'macd', dir: 'bull', fn: (d, i) => fin(d.macd.macd[i]) && d.macd.macd[i] > 0 },
> 40	  // --- momentum / breakout ---
> 41	  { name: 'roc10_pos', family: 'mom', dir: 'bull', fn: (d, i) => fin(d.roc10[i]) && d.roc10[i] > 0 },
> 42	  { name: 'roc10_neg', family: 'mom', dir: 'bear', fn: (d, i) => fin(d.roc10[i]) && d.roc10[i] < 0 },
> 43	  { name: 'breakout_high20', family: 'mom', dir: 'bull', fn: (d, i) => fin(d.priorHigh20[i]) && d.close[i] > d.priorHigh20[i] },
> 44	  { name: 'breakdown_low20', family: 'mom', dir: 'bear', fn: (d, i) => fin(d.priorLow20[i]) && d.close[i] < d.priorLow20[i] },
> 45	  // --- volatilidade ---
> 46	  { name: 'atr_low', family: 'vol', dir: 'flat', fn: (d, i) => fin(d.atrPctPctile[i]) && d.atrPctPctile[i] < 0.2 },
> 47	  { name: 'atr_high', family: 'vol', dir: 'flat', fn: (d, i) => fin(d.atrPctPctile[i]) && d.atrPctPctile[i] > 0.8 },
> 48	  // --- fluxo (proxy histórico: taker-buy-fraction da própria vela) ---
> 49	  { name: 'flow_buy', family: 'flow', dir: 'bull', fn: (d, i) => fin(d.takerBuyFrac[i]) && d.takerBuyFrac[i] > 0.55 },
> 50	  { name: 'flow_sell', family: 'flow', dir: 'bear', fn: (d, i) => fin(d.takerBuyFrac[i]) && d.takerBuyFrac[i] < 0.45 },
> 51	  // --- regime causal por barra ---
> 52	  { name: 'regime_trend', family: 'regime', dir: 'bull', fn: (d, i) => d.regimeBar[i] === 'trend' },
> 53	  { name: 'regime_range', family: 'regime', dir: 'flat', fn: (d, i) => d.regimeBar[i] === 'range' },
> 54	  { name: 'regime_not_bear', family: 'regime', dir: 'bull', fn: (d, i) => d.regimeBar[i] !== 'bear' && d.regimeBar[i] !== 'unknown' },
> 55	  // --- CONJUNÇÕES (teses combinadas) ---
> 56	  { name: 'rsi30_AND_not_bear', family: 'conj', dir: 'bull', fn: (d, i) => fin(d.rsi14[i]) && d.rsi14[i] < 30 && d.regimeBar[i] !== 'bear' && d.regimeBar[i] !== 'unknown' }, // a tese da id2 ao vivo
> 57	  { name: 'rsi30_AND_above_sma200', family: 'conj', dir: 'bull', fn: (d, i) => fin(d.rsi14[i]) && d.rsi14[i] < 30 && fin(d.sma200[i]) && d.close[i] > d.sma200[i] },
> 58	  { name: 'rsi30_AND_range', family: 'conj', dir: 'bull', fn: (d, i) => fin(d.rsi14[i]) && d.rsi14[i] < 30 && d.regimeBar[i] === 'range' },
> 59	  { name: 'boll_lower_AND_range', family: 'conj', dir: 'bull', fn: (d, i) => fin(d.boll.lower[i]) && d.close[i] < d.boll.lower[i] && fin(d.adx[i]) && d.adx[i] < 20 },
> 60	  { name: 'golden_AND_adx', family: 'conj', dir: 'bull', fn: (d, i) => i > 0 && fin(d.sma50[i]) && fin(d.sma200[i]) && fin(d.sma50[i - 1]) && fin(d.sma200[i - 1]) && d.sma50[i - 1] <= d.sma200[i - 1] && d.sma50[i] > d.sma200[i] && fin(d.adx[i]) && d.adx[i] > 25 },
> 61	  { name: 'macd_up_AND_above_sma200', family: 'conj', dir: 'bull', fn: (d, i) => i > 0 && fin(d.macd.hist[i]) && fin(d.macd.hist[i - 1]) && d.macd.hist[i - 1] <= 0 && d.macd.hist[i] > 0 && fin(d.sma200[i]) && d.close[i] > d.sma200[i] },
> 62	  { name: 'breakout_AND_adx', family: 'conj', dir: 'bull', fn: (d, i) => fin(d.priorHigh20[i]) && d.close[i] > d.priorHigh20[i] && fin(d.adx[i]) && d.adx[i] > 25 },
> 63	  { name: 'rsi30_AND_flow_buy', family: 'conj', dir: 'bull', fn: (d, i) => fin(d.rsi14[i]) && d.rsi14[i] < 30 && fin(d.takerBuyFrac[i]) && d.takerBuyFrac[i] > 0.5 },
> 64	  { name: 'above_sma200_AND_roc_pos', family: 'conj', dir: 'bull', fn: (d, i) => fin(d.sma200[i]) && d.close[i] > d.sma200[i] && fin(d.roc10[i]) && d.roc10[i] > 0 },
> 65	];
> 66	
> 67	// afina sinais p/ não-sobrepostos no horizonte h (espaçamento >= h) → retornos ~independentes (t-stat honesto).
> 68	function thin(indices, gap) { const out = []; let last = -Infinity; for (const idx of indices) { if (idx - last >= gap) { out.push(idx); last = idx; } } return out; }
> 69	
> 70	module.exports = { PATTERNS, thin, fin };
> 71	
> ```

## 🤖 Claude *(19:20:57)*

Agora os dois scripts de fase e o teste.

## 🤖 Claude *(19:20:58)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/scripts/pattern-discover.js"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env node
> 2	'use strict';
> 3	/*
> 4	 * TradeUX — FASE 1: DESCOBERTA DE PADRÕES (só na amostra de descoberta; holdout TRANCADO).
> 5	 *
> 6	 * Mede, p/ um universo PRÉ-REGISTRADO de padrões (clássicos + conjunções), o retorno futuro
> 7	 * NET-DE-FEE em múltiplos horizontes — e ranqueia por ROBUSTEZ, não por retorno bruto:
> 8	 *   - parede: split por tempo; a Fase 1 só enxerga os primeiros (1-holdout) — o resto nem é lido.
> 9	 *   - sem lookahead: sinal em i, entrada no OPEN de i+1, saída no OPEN de i+1+h, net de fee.
> 10	 *   - anti-overlap: p/ cada horizonte h, AFINA os sinais (espaçados >= h) → retornos ~independentes
> 11	 *     (senão o t-stat mente: janelas sobrepostas são autocorrelacionadas).
> 12	 *   - múltiplos testes: Benjamini-Hochberg (FDR) + Bonferroni + barra-de-ruído sqrt(2 ln N).
> 13	 *   - estabilidade: consistência de SINAL por símbolo e por sub-período (3 terços da amostra).
> 14	 *
> 15	 * Saída: backtest-results/pattern-discovery-<int>-<days>d[-end].md/json
> 16	 *        backtest-results/pattern-survivors-<int>-<days>d[-end].json  (manifesto p/ a Fase 2)
> 17	 *
> 18	 * Uso: node scripts/pattern-discover.js [--interval=1h] [--days=900]
> 19	 *        [--symbols=BTCUSDT,ETHUSDT,LTCUSDT,BNBUSDT,ADAUSDT] [--holdout=0.3]
> 20	 *        [--horizons=1,5,10,20] [--fdr=0.10] [--warm=250] [--end=YYYY-MM-DD]
> 21	 *
> 22	 * NÃO toca money-path/DB/ordens. Pesquisa pura sobre klines públicas.
> 23	 */
> 24	const fs = require('fs');
> 25	const path = require('path');
> 26	const lab = require('./lib/labkit');
> 27	
> 28	const args = Object.fromEntries(process.argv.slice(2).map(a => { const m = a.match(/^--([^=]+)=?(.*)$/); return m ? [m[1], m[2] || true] : [a, true]; }));
> 29	const INTERVAL = args.interval || '1h';
> 30	const DAYS = parseInt(args.days || '900', 10);
> 31	const SYMBOLS = (args.symbols || 'BTCUSDT,ETHUSDT,LTCUSDT,BNBUSDT,ADAUSDT').split(',');
> 32	const HOLDOUT = parseFloat(args.holdout || '0.3');
> 33	const HORIZONS = (args.horizons || '1,5,10,20').split(',').map(x => parseInt(x, 10)).filter(Boolean);
> 34	const FDR_Q = parseFloat(args.fdr || '0.10');
> 35	const WARM = parseInt(args.warm || '250', 10);
> 36	const FEE = args.fee ? parseFloat(args.fee) : lab.FEE_DEFAULT;
> 37	const END = args.end || null;
> 38	const fin = Number.isFinite;
> 39	const pct = x => (x * 100).toFixed(3) + '%';
> 40	
> 41	// universo PRÉ-REGISTRADO de padrões + afinamento anti-overlap (compartilhado com a Fase 2 → idêntico dos 2 lados da parede)
> 42	const { PATTERNS, thin } = require('./lib/patterns');
> 43	
> 44	(async () => {
> 45	  fs.mkdirSync(lab.OUT_DIR, { recursive: true });
> 46	  console.log(`pattern-discover — ${INTERVAL}, ${DAYS}d${END ? ' end ' + END : ''}, holdout ${pct(HOLDOUT)}, horizontes [${HORIZONS.join(',')}], fee ${FEE * 100}%/lado`);
> 47	  console.log(`símbolos: ${SYMBOLS.join(', ')} · ${PATTERNS.length} padrões × ${HORIZONS.length} horizontes = ${PATTERNS.length * HORIZONS.length} testes`);
> 48	
> 49	  // por símbolo: fetch → SPLIT (tranca holdout) → indicadores SÓ na amostra de descoberta.
> 50	  const perSym = {}; const splitInfo = {};
> 51	  for (const sym of SYMBOLS) {
> 52	    let candles;
> 53	    try { candles = await lab.fetchKlinesExt(sym, INTERVAL, DAYS, END); }
> 54	    catch (e) { console.log(`  skip ${sym}: ${e.message}`); continue; }
> 55	    if (!candles || candles.length < WARM + 400) { console.log(`  skip ${sym}: dados insuficientes (${candles ? candles.length : 0})`); continue; }
> 56	    const sp = lab.splitByTime(candles, HOLDOUT);
> 57	    const ind = lab.computeIndicators(sp.inSample, INTERVAL); // ⚠️ só a amostra de descoberta entra aqui
> 58	    ind.bwPctile = lab.rollingPercentile(ind.boll.bw, 200);
> 59	    perSym[sym] = { candles: sp.inSample, ind, n: sp.inSample.length };
> 60	    splitInfo[sym] = { totalCandles: candles.length, inSampleCandles: sp.inSample.length, holdoutCandles: sp.holdout.length, cutMs: sp.cutMs, kIndex: sp.kIndex };
> 61	    console.log(`  ${sym}: ${candles.length} candles → descoberta ${sp.inSample.length} | holdout TRANCADO ${sp.holdout.length} (corte ${new Date(sp.cutMs).toISOString().slice(0, 10)})`);
> 62	  }
> 63	  const syms = Object.keys(perSym);
> 64	  if (!syms.length) { console.log('sem dados — abortando.'); process.exit(1); }
> 65	
> 66	  // coleta: por (padrão × horizonte) acumula retornos AFINADOS, pooled entre símbolos + por símbolo + por terço.
> 67	  const results = [];
> 68	  for (const p of PATTERNS) {
> 69	    // pré-computa índices de sinal por símbolo (independem do horizonte)
> 70	    const sigBySym = {};
> 71	    for (const s of syms) {
> 72	      const d = perSym[s].ind; const idx = [];
> 73	      for (let i = WARM; i < perSym[s].n; i++) { try { if (p.fn(d, i)) idx.push(i); } catch (e) { /* NaN/edge → ignora */ } }
> 74	      sigBySym[s] = idx;
> 75	    }
> 76	    for (const h of HORIZONS) {
> 77	      const pooledG = [], pooledN = []; const perSymMeanG = {}; const thirds = [[], [], []];
> 78	      for (const s of syms) {
> 79	        const cd = perSym[s].candles; const n = perSym[s].n;
> 80	        const thinned = thin(sigBySym[s], h);
> 81	        const gs = [];
> 82	        for (const i of thinned) {
> 83	          const r = lab.forwardReturn(cd, i, h, FEE);
> 84	          if (r) { gs.push(r.gross); pooledG.push(r.gross); pooledN.push(r.net); const t = Math.min(2, Math.floor(3 * i / n)); thirds[t].push(r.gross); }
> 85	        }
> 86	        perSymMeanG[s] = gs.length ? lab.mean(gs) : null;
> 87	      }
> 88	      const ttG = lab.tTest(pooledG);                         // teste DIRECIONAL = gross (fee-drag não contamina)
> 89	      const meanNet = pooledN.length ? lab.mean(pooledN) : 0;  // acionabilidade long = net
> 90	      const winRateNet = pooledN.length ? pooledN.filter(r => r > 0).length / pooledN.length : 0;
> 91	      const signsSym = Object.values(perSymMeanG).filter(v => v !== null);
> 92	      const sameSignSym = signsSym.length ? signsSym.filter(v => Math.sign(v) === Math.sign(ttG.mean)).length : 0;
> 93	      const thirdMeans = thirds.map(t => (t.length ? lab.mean(t) : null));
> 94	      const sameSignThird = thirdMeans.filter(v => v !== null && Math.sign(v) === Math.sign(ttG.mean)).length;
> 95	      results.push({
> 96	        key: `${p.name}@${h}`, pattern: p.name, family: p.family, dir: p.dir, horizon: h,
> 97	        n: ttG.n, meanGross: ttG.mean, t: ttG.t, p: ttG.p, meanNet, winRateNet, tradeableLong: meanNet > 0, medianGross: lab.median(pooledG),
> 98	        symCovered: signsSym.length, symSameSign: sameSignSym, thirdSameSign: sameSignThird, thirdMeans, perSymMeanG,
> 99	      });
> 100	    }
> 101	  }
> 102	
> 103	  // correção de múltiplos testes sobre TODOS os (padrão × horizonte)
> 104	  const bh = lab.benjaminiHochberg(results.map(r => ({ key: r.key, p: r.p })), FDR_Q);
> 105	  const bonf = lab.bonferroniThreshold(results.length, 0.05);
> 106	  const noiseT = lab.noiseBarT(results.length);
> 107	  for (const r of results) { r.fdrPass = bh.rejected.has(r.key); r.bonfPass = r.p <= bonf; r.beatsNoise = Math.abs(r.t) >= noiseT; }
> 108	
> 109	  // ---------- relatório ----------
> 110	  const sorted = [...results].sort((a, b) => Math.abs(b.t) - Math.abs(a.t));
> 111	  const survivors = results.filter(r => r.fdrPass).sort((a, b) => Math.abs(b.t) - Math.abs(a.t));
> 112	  const L = [];
> 113	  L.push(`# TradeUX — Descoberta de padrões (Fase 1) · ${INTERVAL}, ${DAYS}d${END ? ', end ' + END : ''}\n`);
> 114	  L.push(`> Amostra de DESCOBERTA apenas (holdout ${pct(HOLDOUT)} trancado p/ a Fase 2). Sem lookahead (entrada no open seguinte). Retorno **net de fee** (${FEE * 100}%/lado, round-trip ${(2 * FEE * 100).toFixed(1)}%). Sinais AFINADOS por horizonte (não-sobrepostos) → t-stat honesto.`);
> 115	  L.push(`> Símbolos: ${syms.join(', ')}. ${PATTERNS.length} padrões × ${HORIZONS.length} horizontes = **${results.length} testes**. Correção FDR Benjamini-Hochberg q=${FDR_Q}.\n`);
> 116	  L.push(`## Parede (split por tempo)\n`);
> 117	  L.push(`| Símbolo | candles totais | descoberta | holdout (trancado) | corte |`); L.push(`|---|---|---|---|---|`);
> 118	  for (const s of syms) { const si = splitInfo[s]; L.push(`| ${s} | ${si.totalCandles} | ${si.inSampleCandles} | ${si.holdoutCandles} | ${new Date(si.cutMs).toISOString().slice(0, 10)} |`); }
> 119	
> 120	  const nTradeable = survivors.filter(r => r.tradeableLong).length;
> 121	  L.push(`\n> ⚖️ **Direção vs acionabilidade:** o t-stat/FDR testa **direção** no retorno GROSS (sem fee — senão o fee-drag de ~${(2 * FEE * 100).toFixed(1)}% finge ser "edge" em horizonte curto). A coluna **net** (com fee) diz se dá pra LUCRAR comprando: só \`tradeável long\` (net>0) é acionável no spot. dir=bear/flat com gross<0 = sinal de SAÍDA/evitar (no spot não vira short).\n`);
> 122	  L.push(`## 🎯 Sobreviventes da FDR (q=${FDR_Q}) — ${survivors.length} de ${results.length} · ${nTradeable} tradeáveis long (net>0)\n`);
> 123	  if (!survivors.length) {
> 124	    L.push(`**Nenhum padrão sobreviveu à correção de múltiplos testes.** Resultado HONESTO e esperado (taxa-base). Limiar de p da FDR: ${bh.pThreshold.toExponential(2)}.`);
> 125	  } else {
> 126	    L.push(`| Padrão@h | dir | n | gross/trade | net/trade | tradeável long | win%(net) | t(gross) | p | Bonf | sym | terços |`);
> 127	    L.push(`|---|---|---|---|---|---|---|---|---|---|---|---|`);
> 128	    for (const r of survivors) L.push(`| \`${r.key}\` | ${r.dir} | ${r.n} | ${pct(r.meanGross)} | ${pct(r.meanNet)} | ${r.tradeableLong ? '✅' : '·'} | ${(r.winRateNet * 100).toFixed(1)}% | ${r.t.toFixed(2)} | ${r.p.toExponential(2)} | ${r.bonfPass ? '✓' : '·'} | ${r.symSameSign}/${r.symCovered} | ${r.thirdSameSign}/3 |`);
> 129	    L.push(`\n**Leitura:** um sobrevivente é forte se, ALÉM do FDR: passa Bonferroni (✓), tem mesmo sinal nos ${syms.length} símbolos e nos 3 terços (estável no tempo). Mas só vira COMPRA se \`tradeável long\`=✅. A Fase 2 (holdout) é o juiz final.`);
> 130	  }
> 131	
> 132	  L.push(`\n## Ranking completo (por |t| do gross)\n`);
> 133	  L.push(`Barra de ruído |t| do melhor-de-${results.length}-aleatórios ≈ **${noiseT.toFixed(2)}**. Bonferroni p<${bonf.toExponential(2)}.\n`);
> 134	  L.push(`| Padrão@h | família | dir | n | gross/trade | net/trade | tradeável | win%(net) | t(gross) | p | FDR | Bonf | ruído | sym | terços |`);
> 135	  L.push(`|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|`);
> 136	  for (const r of sorted) L.push(`| \`${r.key}\` | ${r.family} | ${r.dir} | ${r.n} | ${pct(r.meanGross)} | ${pct(r.meanNet)} | ${r.tradeableLong ? '✅' : '·'} | ${(r.winRateNet * 100).toFixed(1)}% | ${r.t.toFixed(2)} | ${r.p.toExponential(2)} | ${r.fdrPass ? '✅' : '·'} | ${r.bonfPass ? '✓' : '·'} | ${r.beatsNoise ? '✓' : '·'} | ${r.symSameSign}/${r.symCovered} | ${r.thirdSameSign}/3 |`);
> 137	
> 138	  L.push(`\n## Conclusão (honesta)\n`);
> 139	  L.push(`1. Testados **${results.length}** padrões×horizontes; **${survivors.length}** sobreviveram à FDR de DIREÇÃO (gross) q=${FDR_Q}, **${results.filter(r => r.bonfPass).length}** ao Bonferroni. Destes, só **${nTradeable}** são tradeáveis long (net>0 após fee) — o resto é direção real mas que NÃO paga a fee, ou sinal de queda/saída.`);
> 140	  L.push(`2. Sobreviver à FDR é NECESSÁRIO mas NÃO suficiente: o veredito real vem da **Fase 2** (holdout trancado + bootstrap por blocos). Um sobrevivente que muda de sinal entre símbolos/terços é frágil.`);
> 141	  L.push(`3. Lembre da taxa-base: a maioria dos padrões NÃO passa — e isso é o sistema funcionando, não falhando. O prêmio é mapear COM confiança onde (se em algum lugar) sobra edge.`);
> 142	  L.push(`\n---\n_Gerado por backend/scripts/pattern-discover.js. Dados Binance reais (cache -ext, gitignored). Net de fee. Holdout NÃO foi lido nesta fase._`);
> 143	
> 144	  const tag = `${INTERVAL}-${DAYS}d${END ? '-end' + END : ''}`;
> 145	  const report = { config: { interval: INTERVAL, days: DAYS, end: END, symbols: syms, holdout: HOLDOUT, horizons: HORIZONS, fdrQ: FDR_Q, warm: WARM, fee: FEE }, nTests: results.length, fdr: { q: FDR_Q, pThreshold: bh.pThreshold, kMax: bh.kMax }, bonferroni: bonf, noiseBarT: noiseT, splitInfo, results: sorted };
> 146	  fs.writeFileSync(path.join(lab.OUT_DIR, `pattern-discovery-${tag}.md`), L.join('\n'));
> 147	  fs.writeFileSync(path.join(lab.OUT_DIR, `pattern-discovery-${tag}.json`), JSON.stringify(report, null, 2));
> 148	  // manifesto de sobreviventes p/ a Fase 2 (inclui a fronteira do split p/ reuso EXATO)
> 149	  const manifest = {
> 150	    config: report.config, generatedFor: tag,
> 151	    splitInfo, // a Fase 2 usa o MESMO cutMs por símbolo
> 152	    survivors: survivors.map(r => ({ pattern: r.pattern, horizon: r.horizon, dir: r.dir, family: r.family, inSample: { n: r.n, meanGross: r.meanGross, meanNet: r.meanNet, t: r.t, p: r.p, winRateNet: r.winRateNet, tradeableLong: r.tradeableLong, symSameSign: r.symSameSign, thirdSameSign: r.thirdSameSign } })),
> 153	  };
> 154	  fs.writeFileSync(path.join(lab.OUT_DIR, `pattern-survivors-${tag}.json`), JSON.stringify(manifest, null, 2));
> 155	  console.log(`\nSobreviventes FDR: ${survivors.length}/${results.length}. Relatório: backend/backtest-results/pattern-discovery-${tag}.md`);
> 156	})();
> 157	
> ```

## 🤖 Claude *(19:20:59)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/scripts/pattern-validate.js"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env node
> 2	'use strict';
> 3	/*
> 4	 * TradeUX — FASE 2: VALIDAÇÃO dos sobreviventes no HOLDOUT TRANCADO.
> 5	 *
> 6	 * Pega o manifesto `pattern-survivors-<tag>.json` (gerado pela Fase 1, SEM olhar o holdout) e testa
> 7	 * cada sobrevivente EXCLUSIVAMENTE nos dados que a descoberta NUNCA viu (t >= cutMs por símbolo).
> 8	 *   - mesma definição de padrão (lib/patterns.js), mesmo fee, mesmo afinamento anti-overlap.
> 9	 *   - retorno net-de-fee, sem lookahead; pooled entre símbolos.
> 10	 *   - IC da média por BOOTSTRAP DE BLOCOS (preserva autocorrelação) com RNG semeado.
> 11	 *   - VEREDITO por sobrevivente:
> 12	 *       CONFIRMA    — mesmo sinal da amostra E o IC do holdout exclui o zero na direção esperada.
> 13	 *       REFUTA      — sinal sumiu/inverteu, ou IC cruza o zero (o "edge" não replica fora da amostra).
> 14	 *       INCONCLUSIVO— amostra de holdout pequena demais (n < minN) p/ decidir.
> 15	 *
> 16	 * Saída: backtest-results/pattern-validation-<tag>.md/json
> 17	 * Uso:   node scripts/pattern-validate.js --tag=1h-900d [--minN=20] [--bootstrap=2000] [--ci=0.95] [--seed=12345]
> 18	 *        (ou derive o tag de --interval/--days/--end, igual à Fase 1)
> 19	 *
> 20	 * NÃO toca money-path. Lê só klines públicas (cache -ext) + o manifesto da Fase 1.
> 21	 */
> 22	const fs = require('fs');
> 23	const path = require('path');
> 24	const lab = require('./lib/labkit');
> 25	const { PATTERNS, thin } = require('./lib/patterns');
> 26	
> 27	const args = Object.fromEntries(process.argv.slice(2).map(a => { const m = a.match(/^--([^=]+)=?(.*)$/); return m ? [m[1], m[2] || true] : [a, true]; }));
> 28	const fin = Number.isFinite;
> 29	const pct = x => (fin(x) ? (x * 100).toFixed(3) + '%' : 'n/a');
> 30	const MIN_N = parseInt(args.minN || '20', 10);
> 31	const NBOOT = parseInt(args.bootstrap || '2000', 10);
> 32	const CI = parseFloat(args.ci || '0.95');
> 33	const SEED = parseInt(args.seed || '12345', 10);
> 34	
> 35	let TAG = args.tag;
> 36	if (!TAG) { const I = args.interval || '1h', D = parseInt(args.days || '900', 10), E = args.end || null; TAG = `${I}-${D}d${E ? '-end' + E : ''}`; }
> 37	
> 38	(async () => {
> 39	  const manifestPath = path.join(lab.OUT_DIR, `pattern-survivors-${TAG}.json`);
> 40	  if (!fs.existsSync(manifestPath)) { console.error(`manifesto não encontrado: ${manifestPath}\nrode a Fase 1 primeiro (pattern-discover.js).`); process.exit(1); }
> 41	  const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'));
> 42	  const cfg = manifest.config;
> 43	  const FEE = cfg.fee || lab.FEE_DEFAULT;
> 44	  const patByName = Object.fromEntries(PATTERNS.map(p => [p.name, p]));
> 45	  console.log(`pattern-validate — tag ${TAG} · ${manifest.survivors.length} sobreviventes · holdout trancado · fee ${FEE * 100}%/lado`);
> 46	
> 47	  if (!manifest.survivors.length) {
> 48	    const L = [`# TradeUX — Validação Fase 2 · ${TAG}\n`, `Nenhum sobrevivente na Fase 1 → nada a validar. (Resultado honesto: a descoberta não achou edge que passe da correção de múltiplos testes.)`];
> 49	    fs.writeFileSync(path.join(lab.OUT_DIR, `pattern-validation-${TAG}.md`), L.join('\n'));
> 50	    console.log('Nenhum sobrevivente — relatório vazio escrito.'); return;
> 51	  }
> 52	
> 53	  // por símbolo: re-fetch (cache hit) → indicadores no SÉRIE COMPLETA → marca o início do holdout por cutMs.
> 54	  const syms = Object.keys(manifest.splitInfo);
> 55	  const perSym = {};
> 56	  for (const sym of syms) {
> 57	    let candles;
> 58	    try { candles = await lab.fetchKlinesExt(sym, cfg.interval, cfg.days, cfg.end); }
> 59	    catch (e) { console.log(`  skip ${sym}: ${e.message}`); continue; }
> 60	    const cutMs = manifest.splitInfo[sym].cutMs;
> 61	    const ind = lab.computeIndicators(candles, cfg.interval); // série completa: indicadores nas barras do holdout têm warmup causal
> 62	    ind.bwPctile = lab.rollingPercentile(ind.boll.bw, 200);
> 63	    let hStart = candles.findIndex(c => c.t >= cutMs);
> 64	    if (hStart < 0) hStart = candles.length;
> 65	    perSym[sym] = { candles, ind, hStart, n: candles.length };
> 66	    console.log(`  ${sym}: ${candles.length} candles, holdout começa em idx ${hStart} (${new Date(cutMs).toISOString().slice(0, 10)}) → ${candles.length - hStart} barras OOS`);
> 67	  }
> 68	  const liveSyms = Object.keys(perSym);
> 69	
> 70	  const rows = [];
> 71	  for (const sv of manifest.survivors) {
> 72	    const p = patByName[sv.pattern]; if (!p) { rows.push({ ...sv, verdict: 'ERRO', note: 'padrão não encontrado em lib/patterns.js' }); continue; }
> 73	    const h = sv.horizon; const gross = [], net = []; const perSymN = {};
> 74	    for (const s of liveSyms) {
> 75	      const { candles, ind, hStart, n } = perSym[s];
> 76	      const idx = [];
> 77	      for (let i = Math.max(hStart, 250); i < n; i++) { try { if (p.fn(ind, i)) idx.push(i); } catch (e) { } }
> 78	      const thinned = thin(idx, h); let c = 0;
> 79	      for (const i of thinned) { const r = lab.forwardReturn(candles, i, h, FEE); if (r) { gross.push(r.gross); net.push(r.net); c++; } }
> 80	      perSymN[s] = c;
> 81	    }
> 82	    const ttG = lab.tTest(gross);
> 83	    const bootG = lab.blockBootstrapMeanCI(gross, { blockLen: Math.max(1, h), nResamples: NBOOT, seed: SEED, ci: CI });
> 84	    const bootN = lab.blockBootstrapMeanCI(net, { blockLen: Math.max(1, h), nResamples: NBOOT, seed: SEED, ci: CI });
> 85	    const meanNet = net.length ? lab.mean(net) : 0;
> 86	    const winRateNet = net.length ? net.filter(r => r > 0).length / net.length : 0;
> 87	    const inSampleGross = sv.inSample.meanGross;
> 88	    let verdict, note, actionable = false;
> 89	    if (ttG.n < MIN_N) { verdict = 'INCONCLUSIVO'; note = `n=${ttG.n} < ${MIN_N} no holdout`; }
> 90	    else {
> 91	      const sameSign = Math.sign(ttG.mean) === Math.sign(inSampleGross);
> 92	      const grossCIexcl = ttG.mean > 0 ? bootG.lo > 0 : bootG.hi < 0;   // direção replica c/ IC fora do zero
> 93	      if (sameSign && grossCIexcl) {
> 94	        actionable = bootN.lo > 0;                                       // tradeável long só se o NET (com fee) tb tem IC>0
> 95	        verdict = 'CONFIRMA';
> 96	        note = actionable ? `direção replica E net paga a fee [${pct(bootN.lo)}, ${pct(bootN.hi)}] → TRADEÁVEL LONG` : `direção replica (gross [${pct(bootG.lo)}, ${pct(bootG.hi)}]) mas net NÃO paga a fee → sinal de SAÍDA/gate, não compra`;
> 97	      } else {
> 98	        verdict = 'REFUTA';
> 99	        note = sameSign ? `direção mesma mas gross IC cruza 0 [${pct(bootG.lo)}, ${pct(bootG.hi)}]` : `direção inverteu (amostra gross ${pct(inSampleGross)} → holdout ${pct(ttG.mean)})`;
> 100	      }
> 101	    }
> 102	    rows.push({ pattern: sv.pattern, horizon: h, dir: sv.dir, family: sv.family, inSampleGross, holdoutN: ttG.n, holdoutGross: ttG.mean, holdoutNet: meanNet, grossLo: bootG.lo, grossHi: bootG.hi, netLo: bootN.lo, netHi: bootN.hi, holdoutT: ttG.t, winRateNet, perSymN, verdict, actionable, note });
> 103	  }
> 104	
> 105	  const order = { CONFIRMA: 0, REFUTA: 1, INCONCLUSIVO: 2, ERRO: 3 };
> 106	  rows.sort((a, b) => (order[a.verdict] - order[b.verdict]) || ((b.actionable ? 1 : 0) - (a.actionable ? 1 : 0)) || (Math.abs(b.holdoutT) - Math.abs(a.holdoutT)));
> 107	  const nConf = rows.filter(r => r.verdict === 'CONFIRMA').length;
> 108	  const nAction = rows.filter(r => r.actionable).length;
> 109	
> 110	  const L = [];
> 111	  L.push(`# TradeUX — Validação Fase 2 (holdout trancado) · ${TAG}\n`);
> 112	  L.push(`> ${manifest.survivors.length} sobreviventes da Fase 1 testados SÓ no holdout (t >= cutMs, que a descoberta nunca viu). IC por bootstrap de blocos (${NBOOT} reamostras, seed ${SEED}). minN=${MIN_N}. fee ${FEE * 100}%/lado.`);
> 113	  L.push(`> **Direção** = IC do retorno GROSS exclui o zero replicando o sinal da amostra. **Tradeável long** = ALÉM disso o NET (com fee) tem IC>0 → dá pra LUCRAR comprando. CONFIRMA sem tradeável = direção real porém net não paga a fee (serve de gate/saída, não de compra no spot).\n`);
> 114	  L.push(`## Veredito: ${nConf}/${rows.length} confirmam a DIREÇÃO · **${nAction} TRADEÁVEIS long** (net paga a fee)\n`);
> 115	  L.push(`| Padrão@h | dir | veredito | tradeável | amostra(gross) | holdout n | holdout gross | holdout net | win%(net) | gross IC${CI * 100} | t | obs |`);
> 116	  L.push(`|---|---|---|---|---|---|---|---|---|---|---|---|`);
> 117	  for (const r of rows) {
> 118	    const badge = r.verdict === 'CONFIRMA' ? '✅ CONFIRMA' : r.verdict === 'REFUTA' ? '❌ REFUTA' : r.verdict === 'INCONCLUSIVO' ? '🟡 INCONC.' : '⚠️ ERRO';
> 119	    L.push(`| \`${r.pattern}@${r.horizon}\` | ${r.dir} | ${badge} | ${r.actionable ? '💰 SIM' : '·'} | ${pct(r.inSampleGross)} | ${r.holdoutN} | ${pct(r.holdoutGross)} | ${pct(r.holdoutNet)} | ${(r.winRateNet * 100).toFixed(1)}% | [${pct(r.grossLo)}, ${pct(r.grossHi)}] | ${fin(r.holdoutT) ? r.holdoutT.toFixed(2) : 'n/a'} | ${r.note} |`);
> 120	  }
> 121	  L.push(`\n## Leitura\n`);
> 122	  L.push(`- **💰 TRADEÁVEL long** = os ÚNICOS candidatos a virar regra de COMPRA — direção replicou no holdout E o net paga a fee. Mesmo assim entram em PAPER antes de qualquer real.`);
> 123	  L.push(`- **CONFIRMA sem tradeável** = a direção é real, mas o movimento não cobre a fee no spot long (ex.: sinais de queda → só servem de GATE/saída, não viram short).`);
> 124	  L.push(`- **REFUTA** = era overfitting da amostra (o caso comum, esperado). **INCONCLUSIVO** = holdout com poucos sinais; junte mais dados (símbolos/tempo) e re-rode.`);
> 125	  L.push(`- Próximo passo dos tradeáveis: encodar no motor de paper ([PAPER]) e medir round-trips reais antes do flip. Nada vira real sem essa ponte.`);
> 126	  L.push(`\n---\n_Gerado por backend/scripts/pattern-validate.js. Holdout = dados pós-corte que a Fase 1 não leu. Net de fee._`);
> 127	
> 128	  fs.writeFileSync(path.join(lab.OUT_DIR, `pattern-validation-${TAG}.md`), L.join('\n'));
> 129	  fs.writeFileSync(path.join(lab.OUT_DIR, `pattern-validation-${TAG}.json`), JSON.stringify({ tag: TAG, config: cfg, minN: MIN_N, bootstrap: NBOOT, ci: CI, seed: SEED, nConfirm: nConf, nActionable: nAction, rows }, null, 2));
> 130	  console.log(`\nVeredito: ${nConf}/${rows.length} confirmam direção · ${nAction} tradeáveis long. Relatório: backend/backtest-results/pattern-validation-${TAG}.md`);
> 131	})();
> 132	
> ```

## 🤖 Claude *(19:20:59)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/scripts/sim/labkit.test.js"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	'use strict';
> 2	/*
> 3	 * Suíte de SIMULAÇÃO — labkit (fundação do laboratório de padrões). Node puro, zero deps do backend.
> 4	 * Trava as propriedades de CORREÇÃO que, se quebrarem, viciam toda a pesquisa em silêncio:
> 5	 *   - retorno futuro SEM lookahead (usa open de i+1 e i+1+h; null fora do range);
> 6	 *   - t-test bate valor conhecido; FDR Benjamini-Hochberg bate o exemplo canônico;
> 7	 *   - split por tempo é disjunto e cobre tudo; RNG semeado + bootstrap são REPRODUTÍVEIS;
> 8	 *   - indicadores produzem arrays alinhados e o catálogo de padrões carrega íntegro.
> 9	 */
> 10	const lab = require('../lib/labkit');
> 11	const { PATTERNS, thin } = require('../lib/patterns');
> 12	
> 13	let passed = 0, failed = 0;
> 14	function check(name, cond) { if (cond) passed++; else { failed++; console.error(`  ✗ ${name}`); } }
> 15	function approx(a, b, eps = 1e-9) { return Math.abs(a - b) <= eps; }
> 16	
> 17	// ---------- (1) forwardNetLong: SEM lookahead ----------
> 18	const cs = [{ open: 100 }, { open: 110 }, { open: 120 }, { open: 130 }, { open: 140 }];
> 19	check('fwd fee0 usa open de i+1 e i+1+h', approx(lab.forwardNetLong(cs, 0, 1, 0), 120 / 110 - 1));
> 20	check('fwd fee0 horizonte 2', approx(lab.forwardNetLong(cs, 0, 2, 0), 130 / 110 - 1));
> 21	check('fwd null fora do range (saída além do fim)', lab.forwardNetLong(cs, 3, 2, 0) === null);
> 22	check('fwd null quando i+1 não existe', lab.forwardNetLong(cs, 4, 1, 0) === null);
> 23	{ const g = lab.forwardNetLong(cs, 0, 1, 0); const f = lab.forwardNetLong(cs, 0, 1, 0.001); check('fee reduz o retorno vs bruto', f < g); }
> 24	{ const r = lab.forwardReturn(cs, 0, 1, 0.001); check('forwardReturn gross independe da fee', approx(r.gross, 120 / 110 - 1)); check('forwardReturn net < gross', r.net < r.gross); check('forwardReturn null fora do range', lab.forwardReturn(cs, 3, 2, 0) === null); }
> 25	// independência de tudo em i (lookahead): mexer em candles[i] não muda o retorno (só i+1 e i+1+h importam)
> 26	{ const c2 = cs.map(c => ({ ...c })); c2[0].open = 999999; check('fwd independe de candles[i] (sem lookahead)', approx(lab.forwardNetLong(c2, 0, 1, 0), 120 / 110 - 1)); }
> 27	
> 28	// ---------- (2) estatística: t-test ----------
> 29	{ const r = lab.tTest([2, 4, 6, 8, 10]); check('tTest mean', approx(r.mean, 6)); check('tTest t≈4.2426', approx(r.t, 4.242640687, 1e-6)); }
> 30	{ const r = lab.tTest([-3, -1, 1, 3]); check('tTest média 0 → t=0', approx(r.t, 0)); check('tTest média 0 → p≈1 (erf aprox ~1e-7)', approx(r.p, 1, 1e-6)); }
> 31	check('normCdf(0)=0.5', approx(lab.normCdf(0), 0.5, 1e-9));
> 32	check('normCdf(+grande)≈1', lab.normCdf(8) > 0.999999);
> 33	check('normCdf simétrico', approx(lab.normCdf(1.5) + lab.normCdf(-1.5), 1, 1e-6));
> 34	
> 35	// ---------- (3) FDR Benjamini-Hochberg: exemplo canônico (BH 1995, m=15, q=0.05 → rejeita 4) ----------
> 36	{
> 37	  const pv = [0.0001, 0.0004, 0.0019, 0.0095, 0.0201, 0.0278, 0.0298, 0.0344, 0.0459, 0.3240, 0.4262, 0.5719, 0.6528, 0.7590, 1.000];
> 38	  const tests = pv.map((p, i) => ({ key: 'k' + i, p }));
> 39	  const bh = lab.benjaminiHochberg(tests, 0.05);
> 40	  check('BH kMax=4', bh.kMax === 4);
> 41	  check('BH rejeita exatamente 4', bh.rejected.size === 4);
> 42	  check('BH rejeita os 4 menores', ['k0', 'k1', 'k2', 'k3'].every(k => bh.rejected.has(k)));
> 43	  check('BH NÃO rejeita o 5º', !bh.rejected.has('k4'));
> 44	}
> 45	check('Bonferroni threshold = alpha/m', approx(lab.bonferroniThreshold(20, 0.05), 0.0025));
> 46	check('noiseBarT(1000) ≈ 3.717', approx(lab.noiseBarT(1000), Math.sqrt(2 * Math.log(1000)), 1e-9));
> 47	
> 48	// ---------- (4) split por tempo: disjunto + cobre tudo ----------
> 49	{
> 50	  const candles = Array.from({ length: 10 }, (_, i) => ({ t: 1000 + i, open: 1, high: 1, low: 1, close: 1, vol: 1 }));
> 51	  const sp = lab.splitByTime(candles, 0.3);
> 52	  check('split kIndex=7', sp.kIndex === 7);
> 53	  check('split soma cobre tudo', sp.inSample.length + sp.holdout.length === 10);
> 54	  check('split disjunto (in < holdout)', sp.inSample[sp.inSample.length - 1].t < sp.holdout[0].t);
> 55	  check('split cutMs = candles[k].t', sp.cutMs === candles[7].t);
> 56	}
> 57	
> 58	// ---------- (5) RNG semeado + bootstrap REPRODUTÍVEIS ----------
> 59	{
> 60	  const a = lab.mulberry32(42), b = lab.mulberry32(42);
> 61	  check('mulberry32 determinístico (mesma seed)', a() === b() && a() === b() && a() === b());
> 62	  const c = lab.mulberry32(43);
> 63	  check('mulberry32 muda com a seed', lab.mulberry32(42)() !== c());
> 64	  const data = Array.from({ length: 200 }, (_, i) => Math.sin(i) * 0.01);
> 65	  const r1 = lab.blockBootstrapMeanCI(data, { blockLen: 10, nResamples: 500, seed: 7 });
> 66	  const r2 = lab.blockBootstrapMeanCI(data, { blockLen: 10, nResamples: 500, seed: 7 });
> 67	  check('bootstrap reprodutível (lo)', approx(r1.lo, r2.lo, 1e-12));
> 68	  check('bootstrap reprodutível (hi)', approx(r1.hi, r2.hi, 1e-12));
> 69	  check('bootstrap mean = lab.mean', approx(r1.mean, lab.mean(data), 1e-12));
> 70	  check('bootstrap lo <= mean <= hi', r1.lo <= r1.mean + 1e-9 && r1.mean <= r1.hi + 1e-9);
> 71	}
> 72	
> 73	// ---------- (6) indicadores: arrays alinhados + sanidade ----------
> 74	{
> 75	  const n = 400;
> 76	  const candles = Array.from({ length: n }, (_, i) => {
> 77	    const base = 100 + i * 0.05 + 10 * Math.sin(i / 15);
> 78	    const open = base, close = base + Math.sin(i / 7) * 0.5;
> 79	    const high = Math.max(open, close) + 1, low = Math.min(open, close) - 1;
> 80	    const vol = 1000 + (i % 13) * 10, takerBuy = vol * (0.4 + 0.2 * ((i % 5) / 5));
> 81	    return { t: 1700000000000 + i * 3600000, open, high, low, close, vol, takerBuy };
> 82	  });
> 83	  const d = lab.computeIndicators(candles, '1h');
> 84	  check('ind arrays no tamanho da série', d.rsi14.length === n && d.sma200.length === n && d.adx.length === n);
> 85	  check('rsi no range [0,100] onde finito', d.rsi14.every(x => !Number.isFinite(x) || (x >= 0 && x <= 100)));
> 86	  check('sma200 finita no fim', Number.isFinite(d.sma200[n - 1]));
> 87	  check('regimeBar válido no fim', ['bear', 'trend', 'range', 'mixed', 'unknown'].includes(d.regimeBar[n - 1]));
> 88	  check('takerBuyFrac em (0,1) onde finito', d.takerBuyFrac.every(x => !Number.isFinite(x) || (x > 0 && x < 1)));
> 89	  check('boll.pctB e bw presentes', Array.isArray(d.boll.pctB) && Array.isArray(d.boll.bw));
> 90	  check('macd tem macd/signal/hist', Array.isArray(d.macd.macd) && Array.isArray(d.macd.signal) && Array.isArray(d.macd.hist));
> 91	  // warmup: índice 0 não pode ter SMA200 finita (sem lookahead de janela)
> 92	  check('sma200 NaN no warmup (idx 0)', !Number.isFinite(d.sma200[0]));
> 93	}
> 94	
> 95	// ---------- (7) catálogo de padrões íntegro ----------
> 96	check('PATTERNS não-vazio', Array.isArray(PATTERNS) && PATTERNS.length >= 30);
> 97	check('todo padrão tem name/family/dir/fn', PATTERNS.every(p => p.name && p.family && p.dir && typeof p.fn === 'function'));
> 98	check('names únicos', new Set(PATTERNS.map(p => p.name)).size === PATTERNS.length);
> 99	check('dir ∈ {bull,bear,flat}', PATTERNS.every(p => ['bull', 'bear', 'flat'].includes(p.dir)));
> 100	// thin: afina respeitando o gap
> 101	{ const t = thin([0, 1, 2, 5, 6, 12], 5); check('thin respeita gap>=5', t.length === 3 && t[0] === 0 && t[1] === 5 && t[2] === 12); }
> 102	
> 103	console.log(`\nlabkit.test.js: ${passed} passed, ${failed} failed`);
> 104	process.exit(failed ? 1 : 0);
> 105	
> ```

## 🤖 Claude *(19:21:06)*

Agora vou verificar a aderência à convenção (backtest.js), gitignore, integração com a suíte de sim/CI, e rodar a suíte de teste.

## 🤖 Claude *(19:21:08)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && echo \"===== backtest.js head (cache/fetch/fee/dirs) =====\" && grep -nE \"FEE|backtest-data|backtest-results|fetchKlines|HOSTS|api.binance|cache|require\\(\" backend/scripts/backtest.js | head -50",
  "description": "Inspect backtest.js conventions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== backtest.js head (cache/fetch/fee/dirs) =====
> 16:const https = require('https');
> 17:const fs = require('fs');
> 18:const path = require('path');
> 24:const FEE = 0.001;                       // 0.1% por lado (taker)
> 28:const HOSTS = ['api.binance.com', 'data-api.binance.vision', 'api.binance.us'];
> 32:const DATA_DIR = path.join(__dirname, '..', 'backtest-data');
> 33:const OUT_DIR = path.join(__dirname, '..', 'backtest-results');
> 50:// ---------- data fetch (klines paginados + cache em disco) ----------
> 52:  const cacheFile = path.join(DATA_DIR, `${symbol}-${INTERVAL}-${DAYS}d${args.end ? '-end' + args.end : ''}.json`);
> 53:  if (fs.existsSync(cacheFile)) {
> 54:    const c = JSON.parse(fs.readFileSync(cacheFile, 'utf8'));
> 55:    if (c.length > 100) { console.log(`  [cache] ${symbol}: ${c.length} candles`); return c; }
> 60:  for (const h of HOSTS) {
> 64:  if (!host) throw new Error(`nenhum host Binance alcançável para ${symbol} (tentei ${HOSTS.join(', ')})`);
> 78:  fs.writeFileSync(cacheFile, JSON.stringify(out));
> 162:    if (sig === 'BUY' && !inPos && nextOpen) { entry = nextOpen * (1 + FEE); inPos = true; }
> 163:    else if (sig === 'SELL' && inPos && nextOpen) { const exit = nextOpen * (1 - FEE); const r = exit / entry - 1; trades.push(r); equity *= (1 + r); inPos = false; }
> 169:  if (inPos) { const exit = candles[endIdx - 1].close * (1 - FEE); const r = exit / entry - 1; trades.push(r); equity *= (1 + r); }
> 178:  const e = candles[startIdx].open * (1 + FEE), x = candles[endIdx - 1].close * (1 - FEE);
> 302:  const bh = syms.map(s => { const cd = IND[s].cd; const e = cd[warm].open * (1 + FEE), x = cd[cd.length - 1].close * (1 - FEE); return { netReturn: x / e - 1, maxDD: 0 }; });
> 344:  console.log(`TradeUX backtest — ${INTERVAL}, ${DAYS}d, fee ${FEE * 100}%/lado, símbolos: ${SYMBOLS.join(', ')}`);
> 345:  const report = { generatedDays: DAYS, interval: INTERVAL, fee: FEE, symbols: {}, params: {} };
> 347:  lines.push(`# TradeUX — Backtest robusto + regime (${INTERVAL}, ${DAYS}d, fee ${FEE * 100}%/lado)\n`);
> 475:  lines.push(`\n---\n_Gerado pelo harness de backtest do TradeUX (backend/scripts/backtest.js). Dados: Binance klines reais (cache em backtest-data/, gitignored). Net de fee. Não é conselho financeiro; fase de validação em testnet._`);
> 479:  console.log(`\nRelatório: backend/backtest-results/backtest-${INTERVAL}-${DAYS}d${outTag}.md`);
> ```

## 🤖 Claude *(19:21:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && echo \"===== .gitignore (backtest-data / results) =====\" && grep -nE \"backtest|results|data\" .gitignore backend/.gitignore 2>/dev/null; echo \"===== existing dirs =====\" && ls -la backend/backtest-data 2>/dev/null | head -5; ls -la backend/backtest-results 2>/dev/null | head -5; echo \"===== sim runner / package.json test:sim =====\" && grep -nE \"test:sim|sim/\" backend/package.json; echo \"===== how sim tests are invoked =====\" && ls backend/scripts/sim/ && cat backend/scripts/sim/run-all.js 2>/dev/null | head -40",
  "description": "Check gitignore, dirs, sim runner integration"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== .gitignore (backtest-data / results) =====
> .gitignore:11:# Runtime data
> .gitignore:104:# backtest raw kline cache (reprodutivel via scripts/backtest.js)
> .gitignore:105:backend/backtest-data/
> ===== existing dirs =====
> total 160640
> drwxr-xr-x  2 gcrux-tradeux gcrux-tradeux    4096 Jun 29 16:12 .
> drwxrwxr-x 11 gcrux-tradeux gcrux-tradeux    4096 Jun 22 12:22 ..
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 1635009 Jun  8 14:27 ADAUSDT-15m-180d-end2024-04-01.json
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux 3228064 Jun  8 14:29 ADAUSDT-15m-365d-end2023-01-01.json
> total 288
> drwxrwxr-x  2 gcrux-tradeux gcrux-tradeux  4096 Jun 29 16:19 .
> drwxrwxr-x 11 gcrux-tradeux gcrux-tradeux  4096 Jun 22 12:22 ..
> -rw-r--r--  1 gcrux-tradeux gcrux-tradeux  9617 Jun  3 20:40 backtest-1h-180d-end2024-04-01.json
> -rw-r--r--  1 gcrux-tradeux gcrux-tradeux  6919 Jun  3 20:40 backtest-1h-180d-end2024-04-01.md
> ===== sim runner / package.json test:sim =====
> 14:    "test:sim": "node scripts/sim/run.js"
> ===== how sim tests are invoked =====
> calcQty.test.js
> crypto.test.js
> dailyCapResumeFlow.test.js
> dailyCapResume.test.js
> dailyCap.test.js
> earnRedeemDryRun.test.js
> earnRedeem.test.js
> eventNotify.test.js
> farmSellBoot.test.js
> farmTriggers.test.js
> feeCalc.test.js
> groupSupervisorReconcile.test.js
> groupSupervisor.test.js
> integration.test.js
> labkit.test.js
> promotion.test.js
> riskGuard.test.js
> run.js
> signalRecorder.test.js
> stepUpGuard.test.js
> withdrawGuard.test.js
> ```

## 🤖 Claude *(19:21:15)*

Vou ver como `run.js` descobre os testes (a labkit.test.js precisa estar incluída na suíte e no CI), e checar se backtest-results está gitignored.

## 🤖 Claude *(19:21:15)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/scripts/sim/run.js"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	'use strict';
> 2	/*
> 3	 * Runner da SUÍTE DE SIMULAÇÃO (scripts/sim/*.test.js). Puro Node, zero deps.
> 4	 * Descobre cada *.test.js do diretório, roda em processo separado (isolamento de MEMORY/env) e agrega.
> 5	 * Sai 1 se QUALQUER arquivo falhar. Usado por `npm run test:sim`, pelo ci-preflight e pelo CI.
> 6	 */
> 7	const fs = require('fs');
> 8	const path = require('path');
> 9	const { spawnSync } = require('child_process');
> 10	
> 11	process.env.AES_KEY = process.env.AES_KEY || '01234567890123456789012345678901';
> 12	
> 13	const DIR = __dirname;
> 14	const files = fs.readdirSync(DIR).filter(f => f.endsWith('.test.js')).sort();
> 15	
> 16	if (!files.length) { console.error('sim/run.js: nenhum *.test.js encontrado'); process.exit(1); }
> 17	
> 18	let failures = 0;
> 19	for (const f of files) {
> 20	    console.log(`\n=== sim/${f} ===`);
> 21	    const r = spawnSync(process.execPath, [path.join(DIR, f)], { stdio: 'inherit', env: process.env });
> 22	    if (r.status !== 0) failures++;
> 23	}
> 24	
> 25	console.log(`\nsim suite: ${files.length - failures}/${files.length} arquivos OK${failures ? ` — ${failures} FALHARAM` : ''}.`);
> 26	process.exit(failures ? 1 : 0);
> 27	
> ```

## 🤖 Claude *(19:21:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && echo \"===== backtest-results in gitignore? =====\" && grep -nE \"backtest-results\" .gitignore backend/.gitignore 2>/dev/null; echo \"(se vazio: N\u00c3O est\u00e1 gitignored)\"; echo \"===== git status dos novos arquivos + results =====\" && git -c safe.directory='*' -C /home/gcrux-tradeux/tradeux status --short 2>&1 | head -30; echo \"===== run the labkit sim test standalone =====\"; cd backend && node scripts/sim/labkit.test.js 2>&1 | tail -15",
  "description": "Check backtest-results gitignore, git status, run labkit test"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== backtest-results in gitignore? =====
> (se vazio: NÃO está gitignored)
> ===== git status dos novos arquivos + results =====
> backups/.gitignore: Permission denied
> warning: could not open directory 'backups/': Permission denied
>  M backend/backtest-results/farm-funnel-1h-full-macro500.json
>  M backend/backtest-results/farm-funnel-1h-full-macro500.md
> ?? backend/backtest-results/farm-funnel-1h-full.json
> ?? backend/backtest-results/farm-funnel-1h-full.md
> ?? backend/scripts/lib/labkit.js
> ?? backend/scripts/lib/patterns.js
> ?? backend/scripts/pattern-discover.js
> ?? backend/scripts/pattern-validate.js
> ?? backend/scripts/sim/labkit.test.js
> ===== run the labkit sim test standalone =====
> 
> labkit.test.js: 45 passed, 0 failed
> ```

## 🤖 Claude *(19:21:23)*

O teste passa 45/45. Importante: `backtest-results/` NÃO está gitignored (só `backtest-data/`). O `run.js` auto-descobre `*.test.js`, então `labkit.test.js` já entra na suíte e no CI automaticamente. Vou confirmar a contagem da suíte completa e verificar um detalhe metodológico crítico: a Fase 2 usa `Math.max(hStart, 250)` mas o warmup dos indicadores na série completa — confirmo se há vazamento de fronteira (overlap entre in-sample e holdout via thinning).

## 🤖 Claude *(19:21:25)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"===== su\u00edte completa (deve incluir labkit) =====\" && node scripts/sim/run.js 2>&1 | tail -6",
  "description": "Run full sim suite to confirm labkit included"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== suíte completa (deve incluir labkit) =====
> 
> === sim/withdrawGuard.test.js ===
> 
> withdrawGuard.test.js: 13 passed, 0 failed
> 
> sim suite: 20/20 arquivos OK.
> ```

## 🤖 Claude *(19:22:31)*

Suíte 20/20 OK, labkit incluída. Tenho tudo que preciso. Vou analisar os pontos metodológicos finos e fechar o veredito.

Pontos que verifiquei nos arquivos:

1. **Fronteira do split na Fase 2** (`pattern-validate.js:77`): `i = Math.max(hStart, 250)` — começa o holdout no índice de corte ou no warmup-250, o que for maior. Não há vazamento: a Fase 1 computa indicadores **só na inSample** (`pattern-discover.js:57`), e a Fase 2 recomputa na série completa mas só **lê** sinais a partir de `hStart`. Correto.

2. **Edge case do thinning na fronteira**: na Fase 2, o thin começa a contar `last=-Infinity` dentro do holdout. Bom — não puxa sinais de antes do corte.

3. **Bug latente leve**: `forwardReturn` na Fase 2 usa `candles` (série completa), e os sinais do holdout próximos ao fim podem ter `i+1+h >= length` → retorna `null`, tratado. OK.

---

# Revisão — Laboratório de Padrões (5 arquivos novos)

**Contexto confirmado:** repo `gcrux-tradeux`-owned; HALT vivo (`halted=false`, parado-mas-armado); convenção pt-BR + camada routers→…→models. Os 5 arquivos vivem 100% em `backend/scripts/` (research), **zero import do backend** (`src/`), zero money-path/DB/ordens. Suíte de sim **20/20 OK** com `labkit.test.js` já auto-descoberta pelo `run.js` (entra no CI sem mexer em nada). Standalone: **45/45**.

## VEREDITO: APPROVE COM SUGESTÕES

Mergeável. Mudança nova, bem-escopada, reversível (deletar 5 arquivos = rollback total), blast radius nulo sobre o sistema vivo. As sugestões abaixo são todas nice-to-have — nenhuma bloqueia.

### Racional por eixo de avaliação

**1. Design/manutenibilidade — sólido.** A fronteira labkit(kit) + patterns(universo) + 2 scripts-de-fase é a decomposição certa. O ponto-chave que você levantou — `patterns.js` ser **compartilhado** pelas duas fases — é exatamente o desenho correto e o que dá integridade à parede: se descoberta e validação tivessem cópias separadas da `fn`, qualquer drift silencioso invalidaria o holdout sem erro visível. Centralizar `forwardReturn`, `splitByTime`, `thin` e a estatística no kit garante que os dois lados usam bit-a-bit a mesma régua. `pattern-validate.js:72` ainda valida `patByName[sv.pattern]` e emite `ERRO` se um padrão sumiu do catálogo — guard explícito contra o drift. Bem feito.

**2. Aderência à convenção — alta.** Espelha `backtest.js` fielmente: mesmos `HOSTS`, `FEE=0.001`, `DATA_DIR`/`OUT_DIR` via `path.join(__dirname,...)`, cache em disco, indicadores Wilder, exec no open seguinte (sem lookahead), saída `.md`+`.json` em `backtest-results/`, comentários pt-BR, rodapé "Gerado por…". A re-implementação dos indicadores em vez de reusar `backtest.js` é **justificada** — `backtest.js` roda um IIFE no `require` (`(async()=>{…})()`), não exporta nada; reusá-lo dispararia um backtest. A duplicação aqui é inevitável e o labkit pelo menos a concentra num único módulo testado. O sufixo `-ext` no cache (`labkit.js:274`) evita colisão com os caches do `backtest.js` (que não têm `takerBuy`). Correto.

**3. Risco — baixo, conforme alegado.** Fetch bate em `api.binance.com` (read-only, klines públicas, sem auth/chave) — mesmíssimo padrão já em produção no `backtest.js`. Sem chamada autenticada, sem `exchange.js`, sem tocar `MEMORY`/`BRAIN`. Escreve só em `backtest-data/` (gitignored) e `backtest-results/`. **Não há efeito colateral sobre o processo vivo** (scripts standalone, rodados à mão). Único respingo operacional: rodar a Fase 1 com 5 símbolos × 900d em 1h pagina ~22 req/símbolo de uma vez — bem dentro do rate-limit da Binance, mas ver nice-to-have #2.

**4. Honestidade metodológica — esse é o ponto forte.** A defesa anti-falso-positivo é genuinamente em camadas e cada uma está testada:
- **Parede temporal trancada** (`splitByTime`): Fase 1 computa indicadores **só na inSample** (`pattern-discover.js:57`), holdout nunca é lido; Fase 2 reusa o **mesmo `cutMs` por símbolo** via manifesto. Sem vazamento de fronteira.
- **Anti-overlap** (`thin`, gap≥h): mata a autocorrelação de janelas sobrepostas que mentiria no t-stat. Crítico e presente nas duas fases.
- **Múltiplos testes**: BH-FDR + Bonferroni + barra-de-ruído `sqrt(2 ln N)`, sobre **todos** os (padrão×horizonte). O exemplo canônico BH-1995 (m=15→rejeita 4) está travado no teste.
- **Gross vs net separados** (`forwardReturn`): direção testada no gross (fee-drag não finge edge), acionabilidade exigida no net — distinção metodológica que muita gente erra. Excelente.
- **Holdout com bootstrap de blocos** + RNG semeado (reprodutível, travado no teste) e veredito que exige `sameSign && IC-exclui-zero`, e `actionable` só se `bootN.lo>0`.

Está **suficiente** para não entregar falso-positivo no nível de research. As aproximações declaradas (p-valor normal vs t-Student; overlap tratado por thin) estão honestamente comentadas em `labkit.js:51` e `:17`.

---

### Must-fix (antes de commitar)
**Nenhum.** Não há bug, segredo, nem toque no hot-path/money-path. Não bloqueia apresentar ao dono nem o commit.

### Nice-to-have (follow-up, não-bloqueante)
1. **`backtest-results/` NÃO está gitignored** (só `backtest-data/`, `.gitignore:105`). Hoje já há `.md`/`.json` commitados ali (e dois `farm-funnel-*` aparecem como `??`/`M` no `git status`). Decisão consciente: ou (a) commitar os relatórios do lab como artefato versionado (consistente com o que já existe), ou (b) ignorar `backtest-results/*pattern-*`. **Recomendo (a)** — relatório de research versionado tem valor de auditoria. Só esteja ciente de que `git add backend/scripts` não arrasta os outputs; adicione-os explicitamente se quiser versioná-los.

2. **Sem throttle entre páginas no `fetchKlinesExt`** (`labkit.js:287-296`): o loop pagina sem `sleep`. Para 900d/1h é trivial, mas se alguém rodar 1m/900d × 5 símbolos são ~6k requests em rajada e pode bater 418/429. Um `await sleep(120)` por página, ou um comentário "para intervalos finos, espere rate-limit", fecha o risco. (`backtest.js` tem a mesma característica, então não é regressão — é o teto conhecido.)

3. **`emaSeries` no warmup** (`labkit.js:126-132`): inicia a EMA com SMA do primeiro bloco — convenção válida e igual à do `macdSeries`. Só não bate 1:1 com a EMA do `indexes.js`/Beholder ao vivo. Para **research** é irrelevante (o lab é auto-consistente), mas se algum padrão "tradeável long" for promovido para o motor, vale conferir que o sinal sobrevive à definição de EMA de produção antes do paper. Anotar como pré-req da ponte, não do merge.

4. **`p-valor normal vs t-Student** já flagado em código (`labkit.js:51`): para `n<30` é anti-conservador. O `MIN_N=20` da Fase 2 é o backstop, mas considerar elevar o piso de `n` para os horizontes longos (h=20 afina muito a amostra) — é o caso mais provável de `INCONCLUSIVO` legítimo. Comportamento já correto; só calibração.

### Decisão de merge
- **Aprovar e commitar os 5 arquivos** como um único commit (research-only, scope-clean). Sugiro incluir os relatórios gerados **só depois** de rodar a Fase 1+2 uma vez e revisar a saída com o dono — não commitar outputs vazios/parciais.
- **Condição única**: decidir conscientemente o item nice-to-have #1 (versionar ou ignorar `backtest-results/*pattern-*`) **antes** do `git add`, para não vazar/omitir artefato por acidente. Cuidado de rotina com ownership: `git -C … -c safe.directory='*'`, commit/push via chave do `ubuntu` + chown back, e **via PR, não direto no master** (a árvore está com `farm-funnel-*` não-commitados de outra origem — `git status` em `backend/backtest-results/` — não arraste-os no mesmo commit; ver memória de cross-session contamination).

Arquivos revisados:
- `/home/gcrux-tradeux/tradeux/backend/scripts/lib/labkit.js`
- `/home/gcrux-tradeux/tradeux/backend/scripts/lib/patterns.js`
- `/home/gcrux-tradeux/tradeux/backend/scripts/pattern-discover.js`
- `/home/gcrux-tradeux/tradeux/backend/scripts/pattern-validate.js`
- `/home/gcrux-tradeux/tradeux/backend/scripts/sim/labkit.test.js`

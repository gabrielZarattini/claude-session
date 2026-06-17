# Session agent-a4eb89cfabd5df68c
**Date:** 2026-06-17 | **Session ID:** `agent-a4eb89cfabd5df68c`

---

## 👤 User *(16:47:06)*

Decisão de merge sobre um fix backend+MCP NÃO-COMMITADO no TradeUX. Veredito: APPROVE / APPROVE COM SUGESTÕES / REQUEST CHANGES / BLOCK, com must-fix vs nice-to-have.

## Contexto e a tensão que quero que você julgue
O agente LLM notificou o dono no Telegram: "baseline liberado para BNBUSDT apesar de RSI ~53 > 25 = incoerência". É falso-flag da classe GATE≠TRIGGER. Numa sessão ANTERIOR, um TL revisou esta MESMA área e deu o veredito: **"a fase de ENUMERAÇÃO REATIVA de coerência do cockpit está DONE; PARAR de perseguir paridade 1:1 no VIEW; corrigir só mentiras DIRECIONAIS, não nuances."** 

Então a pergunta central pra você: **este fix é uma mentira DIRECIONAL legítima de corrigir, ou é mais perseguição-de-view que o TL anterior pediu pra parar?**

Meu argumento p/ ser direcional (e não nuance): o cockpit expõe `baseline=true` pra uma ALT (BNBUSDT) que **não tem módulo baseline** — pra alts o gate de acumulação operativo é o FARM (`buyAllowed=farm`). Expor um estado de gate de um módulo inexistente afirma algo falso sobre o símbolo, e é a RAIZ ESTRUTURAL de uma notificação recorrente ao dono (3ª/4ª vez). O fix mata na fonte (não no prompt): pra não-flow-gated, `baseline=null` (n/a).

## Diff
```diff
# backend/src/cockpitJob.js — deriveGates
-    const baseline = farm && flowOk;
+    const baselineRaw = farm && flowOk;                 // módulo baseline (só BTC)
+    const baseline = flowGated ? baselineRaw : null;    // alt: null (n/a) — não expor gate-fantasma
     const buyAllowed = flowGated ? baselineRaw : farm;  // INALTERADO (BTC usa baselineRaw == antigo baseline)
# tradeux-mcp/src/index.js — +1 frase na descrição do tool: baseline=null p/ alts, gate != gatilho.
```

## Avalie
1. **Direcional vs nuance** (acima) — é a decisão central. Concorda que expor gate de módulo inexistente é direcional e merece fix estrutural, OU isso é re-litigar o que o TL anterior fechou e deveria ficar no prompt/ignorado?
2. **buyAllowed inalterado** — confirme que o gate OPERATIVO não muda (risco zero de mudar decisão de compra). `baselineRaw` preserva o BTC; alt segue `farm`.
3. **null como sentinela** vs omitir o campo vs false — escolha certa? Algum consumidor (MCP `index.js:228`, frontend `Cockpit.js`) quebra ou interpreta mal `null`?
4. **Convenção/manutenção** — o comentário e a nota do MCP ficaram claros e honestos? Escopo mínimo?
5. Esta mudança REDUZ a superfície de falso-flag de forma durável (estrutural) em vez de empilhar regra no prompt — alinhado à filosofia "consertar a fonte, não a interpretação"?

Leia o necessário (deriveGates, callers, frontend Cockpit.js, MCP). Retorne veredito + must-fix vs nice-to-have com justificativa.

## 🤖 Claude *(16:47:08)*

Vou carregar o contexto e inspecionar o código relevante antes de julgar.

## 🤖 Claude *(16:47:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat /home/gcrux-tradeux/HANDOFF.md 2>/dev/null | head -100; echo \"=====CLAUDE.md=====\"; cat /home/gcrux-tradeux/tradeux/CLAUDE.md 2>/dev/null | head -120",
  "description": "Load HANDOFF and CLAUDE context"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> # TradeUX — HANDOFF (single source of truth)
> 
> > ShakeHands continuity doc. `/handson` reads this FIRST. Newest record at the bottom.
> > Project: **TradeUX** — Beholder-based multi-coin Binance Spot bot + LLM agent (**mainnet/testnet dual-env**).
> > Updated: **2026-06-16** · Phase: **GO-LIVE MAINNET — CONGELADO (`TRADING_HALT=true`)** · Meta: **realista ≈ flat com ~$150** (o +3 BTC era do testnet) · Vivo==master==origin==**`0b1554d`**
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
> | Backtest robusto walk-forward (1y, 4 símbolos, fee) | ✅ |
> | Detector de regime: módulo + endpoint `/analysis/regime` + MCP `tradeux_get_regime` (Fase 1) | ✅ live (read-only, commit 0a97820) |
> | Modelo de orquestração trunk-based selado | ✅ (memória) |
> | `node-binance-api` 0.13→1.x (mata request via lib+@sendgrid; backend 8→2; OCO no wrapper) | ✅ (commit 063df19; gate+testnet) |
> | OCO wiring no Beholder (template `type:'OCO'`, 2 pernas+`orderListId`, listStatus, anti-stacking) | ✅ (commit `aa3f7f7`; gate+testnet+CI) |
> | P&L: net/avgPrice no insert de fills (~74% das MARKET tinham NULL → P&L furado) | ✅ (commit `d74fac0`; gate+testnet) |
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
> make nuke             # down -v — DELETES the database volume
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
> # tradeux-mcp/  — usually launched by the agent, not directly
> npm start
> ```

## 🤖 Claude *(16:47:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' status 2>&1 | head -40; echo \"=====DIFF=====\"; git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' diff 2>&1 | head -200",
  "description": "Show git status and uncommitted diff"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> On branch master
> Your branch is ahead of 'origin/master' by 1 commit.
>   (use "git push" to publish your local commits)
> 
> Changes not staged for commit:
>   (use "git add <file>..." to update what will be committed)
>   (use "git restore <file>..." to discard changes in working directory)
> 	modified:   backend/src/cockpitJob.js
> 	modified:   tradeux-mcp/src/index.js
> 
> no changes added to commit (use "git add" and/or "git commit -a")
> =====DIFF=====
> diff --git a/backend/src/cockpitJob.js b/backend/src/cockpitJob.js
> index 97a1b97..46defd2 100644
> --- a/backend/src/cockpitJob.js
> +++ b/backend/src/cockpitJob.js
> @@ -94,10 +94,14 @@ function deriveGates(regime, flow, symbol) {
>      // (mostrava GO sem fluxo fresco) — direção PERIGOSA/enganosa vs a automação real, que BLOQUEIA o dip.
>      const flowOk = !!flowFresh && flow.imbalance >= FLOW_BUY_MIN;
>      const farm = regimeOk && regime !== 'trend';        // farm: RSI+regime (mean-reversion range/mixed), SEM fluxo
> -    const baseline = farm && flowOk;                    // baseline (BTC id2): farm + filtro de fluxo (fail-closed)
>      const trend = regimeOk;                             // trend compra no golden cross (!= bear)
>      const flowGated = !!symbol && FLOW_GATED.has(String(symbol).toUpperCase());
> -    const buyAllowed = flowGated ? baseline : farm;     // alt: farm (sem fluxo); símbolo flow-gated (BTC): baseline
> +    const baselineRaw = farm && flowOk;                 // módulo baseline (BTC id2): farm + filtro de fluxo (fail-closed)
> +    // baseline SÓ existe p/ símbolo flow-gated (BTC). Pra ALT não há módulo baseline (o gate de acumulação é o FARM):
> +    // expor baseline=true p/ alt é um gate-FANTASMA que o agente lê como "incoerência" (baseline aberto c/ RSI>25).
> +    // → baseline=null (n/a) p/ não-flow-gated; buyAllowed e farm ficam INTACTOS (buyAllowed usa baselineRaw p/ BTC).
> +    const baseline = flowGated ? baselineRaw : null;
> +    const buyAllowed = flowGated ? baselineRaw : farm;  // alt: farm (sem fluxo); símbolo flow-gated (BTC): baseline
>      let reason;
>      if (!regimeOk) reason = `regime=${regime || 'unknown'}: acumulação em CAIXA (farm/baseline e trend parados)`;
>      else if (regime === 'trend') reason = 'regime=trend: farm/baseline em CAIXA (correto); trend compra no golden cross';
> diff --git a/tradeux-mcp/src/index.js b/tradeux-mcp/src/index.js
> index c30cff9..8dedbc3 100644
> --- a/tradeux-mcp/src/index.js
> +++ b/tradeux-mcp/src/index.js
> @@ -212,7 +212,7 @@ readTool(
>  
>  readTool(
>    "tradeux_get_cockpit",
> -  "Cockpit Intelligence (READ-ONLY): snapshot que a brain computa por simbolo a partir de klines 1m REAIS da mainnet — distribuicao de retornos (mediana |move|, sigma, % de moves >= break-even de fee), EV/trade NET de fee (mecanica da distribuicao 1m; costuma ser <=0 = por que scalping de 1m sangra taxa), banda Monte Carlo DRIFTLESS (p50 == preco, NAO previsao) e o snapshot regime/fluxo + estado dos gates de COMPRA por simbolo. Tambem informa o AMBIENTE real (env.useTestnet) e se o trading esta congelado (env.tradingHalt). Use para REPORTAR ao operador o estado MECANICO do mercado e a coerencia dos gates; NAO e sinal de trade nem forecast. ATENCAO: os gates (buyGate/farm/baseline/trend, doctrine=true) sao a DOUTRINA por regime (o que a estrategia FARIA), NAO confirmam que a automacao correspondente esta ATIVA/ligada (ex.: a baseline id2 esta isActive=0) — o gate VIVO mora na condition da automacao no banco. Reporte como doutrina, nao como estado vivo, e o fluxo e fail-closed (stale/ausente => CAIXA). O regime/fluxo do cockpit sao lidos das MESMAS chaves MEMORY['REGIME']/['FLOW'] que os oraculos vivos (tradeux_get_regime/tradeux_get_oracle_state) — NAO uma fonte paralela; o fluxo carrega flow.ageSec (idade em segundos). Por isso NAO trate diferenca cockpit×oraculo-vivo como contradicao: compare pela idade (um imbalance velho mais negativo que o vivo e o MESMO sinal em instantes diferentes) e, no regime, use o gate.regime histeretico.",
> +  "Cockpit Intelligence (READ-ONLY): snapshot que a brain computa por simbolo a partir de klines 1m REAIS da mainnet — distribuicao de retornos (mediana |move|, sigma, % de moves >= break-even de fee), EV/trade NET de fee (mecanica da distribuicao 1m; costuma ser <=0 = por que scalping de 1m sangra taxa), banda Monte Carlo DRIFTLESS (p50 == preco, NAO previsao) e o snapshot regime/fluxo + estado dos gates de COMPRA por simbolo. Tambem informa o AMBIENTE real (env.useTestnet) e se o trading esta congelado (env.tradingHalt). Use para REPORTAR ao operador o estado MECANICO do mercado e a coerencia dos gates; NAO e sinal de trade nem forecast. ATENCAO: os gates (buyGate/farm/baseline/trend, doctrine=true) sao a DOUTRINA por regime (o que a estrategia FARIA), NAO confirmam que a automacao correspondente esta ATIVA/ligada (ex.: a baseline id2 esta isActive=0) — o gate VIVO mora na condition da automacao no banco. Reporte como doutrina, nao como estado vivo, e o fluxo e fail-closed (stale/ausente => CAIXA). O campo baseline SO se aplica a simbolo flow-gated (BTC); para ALTS vem null (n/a) — o gate de acumulacao da alt e o farm, entao NAO trate baseline=null (nem farm aberto com RSI>35/25) como incoerencia: o gate e a DOUTRINA de regime/fluxo, o RSI e o GATILHO (gate != gatilho). O regime/fluxo do cockpit sao lidos das MESMAS chaves MEMORY['REGIME']/['FLOW'] que os oraculos vivos (tradeux_get_regime/tradeux_get_oracle_state) — NAO uma fonte paralela; o fluxo carrega flow.ageSec (idade em segundos). Por isso NAO trate diferenca cockpit×oraculo-vivo como contradicao: compare pela idade (um imbalance velho mais negativo que o vivo e o MESMO sinal em instantes diferentes) e, no regime, use o gate.regime histeretico.",
>    {},
>    async () => {
>      const d = await api.get(`/analysis/cockpit`);
> ```

## 🤖 Claude *(16:47:14)*

Vou ler o `deriveGates` completo, os callers no backend, o consumo no frontend e no MCP para validar o sentinela `null`.

## 🤖 Claude *(16:47:15)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	'use strict';
> 2	/*
> 3	 * Cockpit Job — grava MEMORY['<sym>:COCKPIT'] (analytics READ-ONLY que o brain segura e o agente LÊ/REPORTA).
> 4	 *
> 5	 * Clona o padrão do fairPriceJob/flowJob/regimeJob: sinal/dado da MAINNET → MEMORY (passivo). Compõe:
> 6	 *   - bloco de MERCADO (distribuição de retornos 1m, EV net-de-fee, tail, banda MC driftless) do cockpitService
> 7	 *   - SNAPSHOT de regime/flow LIDO da MEMORY (já populada por regimeJob/flowJob)
> 8	 *   - estado DERIVADO dos gates de COMPRA (view do cockpit; limiares transparentes no payload)
> 9	 *
> 10	 * PASSIVO e READ-ONLY: updateMemory(...,executeAutomations=FALSE) — NUNCA dispara automação, NUNCA chama
> 11	 * buy/sell/oco. COCKPIT é informativo (o agente lê via MCP/MEMORY); diferente de REGIME/FAIR, NÃO gateia nada,
> 12	 * então desligar o job (kill-switch) não tem efeito colateral no money-path.
> 13	 *
> 14	 * ⚠️ honestidade: EV/distribuição/MC são MECÂNICA da distribuição de 1m do mercado REAL (mainnet), NÃO previsão;
> 15	 * a banda MC é DRIFTLESS (p50 ≡ preço). `gates.buyAllowed` é a VIEW do cockpit (limiar COCKPIT_FLOW_BUY_MIN
> 16	 * exposto no payload) — NÃO é o gate exato da id2 ao vivo (esse vive na condition da automação no banco); por
> 17	 * isso o payload carrega `flowBuyMin` p/ ser transparente. A defasagem de SNAPSHOT (flow/regime/gates velhos no
> 18	 * tick de 60s) foi RESOLVIDA pelo `freshen` (read-path recomputa do MEMORY vivo + expõe `flow.ageMs`); FOLLOW-UP
> 19	 * remanescente = reconciliar SÓ os limiares (`flowBuyMin`/`FLOW_STALE_MS`) com a condition viva da id2.
> 20	 *
> 21	 * Env:
> 22	 *   COCKPIT_JOB_ENABLED  (default 'true')   — kill-switch
> 23	 *   COCKPIT_REFRESH_MS   (default 60000)    — intervalo do poll (60s; piso 5s)
> 24	 *   COCKPIT_SYMBOLS      (CSV, opcional)    — força a lista; senão automações ativas; BTCUSDT sempre incluído
> 25	 *   COCKPIT_LOOKBACK     (default 500)      — nº de velas 1m p/ a distribuição
> 26	 *   COCKPIT_BREAKEVEN_PCT(default 0.20)     — round-trip de fee (%) p/ pHit/EV (0.15 com BNB)
> 27	 *   COCKPIT_TAIL_K       (default 3)        — k de |r| >= k·σ p/ tail mass
> 28	 *   COCKPIT_MC_HORIZON   (default 60)       — horizonte (min) da banda MC driftless
> 29	 *   COCKPIT_FLOW_BUY_MIN (default -0.4)     — imbalance mínimo p/ a VIEW "fluxo não-capitulação" do gate
> 30	 */
> 31	const beholder = require('./beholder');
> 32	const automationsRepository = require('./repositories/automationsRepository');
> 33	const { getCockpit } = require('./utils/cockpitService');
> 34	const { indexKeys } = require('./utils/indexes');
> 35	const logger = require('./utils/logger');
> 36	
> 37	const ENABLED = (process.env.COCKPIT_JOB_ENABLED || 'true') !== 'false';
> 38	const _refresh = parseInt(process.env.COCKPIT_REFRESH_MS || '60000', 10);
> 39	const REFRESH_MS = Number.isFinite(_refresh) && _refresh >= 5000 ? _refresh : 60000;
> 40	const _lookback = parseInt(process.env.COCKPIT_LOOKBACK || '500', 10);
> 41	const LOOKBACK = Number.isFinite(_lookback) && _lookback >= 30 ? _lookback : 500;
> 42	const _be = parseFloat(process.env.COCKPIT_BREAKEVEN_PCT || '0.20');
> 43	const BREAKEVEN_PCT = Number.isFinite(_be) && _be > 0 ? _be : 0.20;
> 44	const _tk = parseFloat(process.env.COCKPIT_TAIL_K || '3');
> 45	const TAIL_K = Number.isFinite(_tk) && _tk > 0 ? _tk : 3;
> 46	const _mc = parseInt(process.env.COCKPIT_MC_HORIZON || '60', 10);
> 47	const MC_HORIZON = Number.isFinite(_mc) && _mc > 0 ? _mc : 60;
> 48	const _fbm = parseFloat(process.env.COCKPIT_FLOW_BUY_MIN || '-0.4');
> 49	const FLOW_BUY_MIN = Number.isFinite(_fbm) ? _fbm : -0.4;
> 50	const FLOW_STALE_MS = 5 * 60 * 1000; // fluxo mais velho que isto não conta p/ a view do gate (fail-safe)
> 51	
> 52	let timer = null;
> 53	let running = false;       // trava de re-entrância
> 54	const LAST = {};           // último COCKPIT por símbolo (observabilidade/endpoint)
> 55	const AT = {};             // timestamp (ms) da última gravação
> 56	const UNAVAIL = new Set();  // símbolos indisponíveis já logados (1x por episódio)
> 57	
> 58	async function resolveSymbols() {
> 59	    const fromEnv = (process.env.COCKPIT_SYMBOLS || '').split(',').map(s => s.trim().toUpperCase()).filter(Boolean);
> 60	    let syms = [];
> 61	    if (fromEnv.length) syms = fromEnv;
> 62	    else {
> 63	        try {
> 64	            const autos = await automationsRepository.getActiveAutomations();
> 65	            syms = (autos || [])
> 66	                .map(a => String((a.get ? a.get('symbol') : a.symbol) || '').toUpperCase())
> 67	                .filter(s => s && !s.startsWith('*'));
> 68	        } catch (err) {
> 69	            logger('cockpit', `Falha ao resolver símbolos: ${err.message}`);
> 70	            syms = [];
> 71	        }
> 72	    }
> 73	    syms.push('BTCUSDT'); // BTC sempre presente (âncora do painel), mesmo sem automação ativa
> 74	    return [...new Set(syms)];
> 75	}
> 76	
> 77	// Estado DERIVADO dos gates de compra POR MÓDULO (view do cockpit, limiares transparentes). NÃO emite ordem.
> 78	// Espelha a doutrina das automações (ver SYSTEM_PROMPT do agente):
> 79	//   - FARM (alts LTC/BNB/ADA): RSI+regime (mean-reversion, range OU mixed: != bear && != trend), SEM filtro de
> 80	//     fluxo (condition VIVA = MEMORY[REGIME]!=='bear' && !=='trend', setup-farm.js:131). 'mixed' é mean-reversion
> 81	//     no classifier → liberar em mixed é CORRETO, não bug.
> 82	//   - BASELINE (BTC id2): farm + filtro de FLUXO não-capitulação (setup-flow-gate.js) — É O ÚNICO módulo de
> 83	//     acumulação flow-gated. Aplicar o filtro de fluxo às ALTS MENTE (vetaria entrada que a farm viva FARIA).
> 84	//   - TREND compra no golden cross: gated só por != bear; HARVESTER é DESGATEADO (opera em qualquer regime).
> 85	// `buyAllowed` = gate de ACUMULAÇÃO do SÍMBOLO: FARM (alts, sem fluxo) ou BASELINE (BTC, com fluxo), conforme FLOW_GATED.
> 86	
> 87	// Símbolos cujo módulo de acumulação gateia por FLUXO: SÓ a baseline BTC (id2). Default BTCUSDT; env sobrescreve.
> 88	const FLOW_GATED = new Set((process.env.COCKPIT_FLOW_GATED_SYMBOLS || 'BTCUSDT').split(',').map(s => s.trim().toUpperCase()).filter(Boolean));
> 89	
> 90	function deriveGates(regime, flow, symbol) {
> 91	    const regimeOk = !!regime && regime !== 'bear' && regime !== 'unknown';
> 92	    const flowFresh = flow && Number.isFinite(flow.imbalance) && flow.atMs && (Date.now() - flow.atMs) < FLOW_STALE_MS;
> 93	    // fail-CLOSED como a id2 (auditoria): fluxo stale/ausente NÃO libera (conservador). Antes era fail-OPEN
> 94	    // (mostrava GO sem fluxo fresco) — direção PERIGOSA/enganosa vs a automação real, que BLOQUEIA o dip.
> 95	    const flowOk = !!flowFresh && flow.imbalance >= FLOW_BUY_MIN;
> 96	    const farm = regimeOk && regime !== 'trend';        // farm: RSI+regime (mean-reversion range/mixed), SEM fluxo
> 97	    const trend = regimeOk;                             // trend compra no golden cross (!= bear)
> 98	    const flowGated = !!symbol && FLOW_GATED.has(String(symbol).toUpperCase());
> 99	    const baselineRaw = farm && flowOk;                 // módulo baseline (BTC id2): farm + filtro de fluxo (fail-closed)
> 100	    // baseline SÓ existe p/ símbolo flow-gated (BTC). Pra ALT não há módulo baseline (o gate de acumulação é o FARM):
> 101	    // expor baseline=true p/ alt é um gate-FANTASMA que o agente lê como "incoerência" (baseline aberto c/ RSI>25).
> 102	    // → baseline=null (n/a) p/ não-flow-gated; buyAllowed e farm ficam INTACTOS (buyAllowed usa baselineRaw p/ BTC).
> 103	    const baseline = flowGated ? baselineRaw : null;
> 104	    const buyAllowed = flowGated ? baselineRaw : farm;  // alt: farm (sem fluxo); símbolo flow-gated (BTC): baseline
> 105	    let reason;
> 106	    if (!regimeOk) reason = `regime=${regime || 'unknown'}: acumulação em CAIXA (farm/baseline e trend parados)`;
> 107	    else if (regime === 'trend') reason = 'regime=trend: farm/baseline em CAIXA (correto); trend compra no golden cross';
> 108	    else if (!flowGated) {
> 109	        const cap = (flowFresh && !flowOk) ? ` — fluxo em capitulação (imbalance ${flow.imbalance}) é INFORMATIVO, NÃO gateia o farm` : '';
> 110	        reason = `regime=${regime} (mean-reversion: range/mixed) + RSI: FARM liberado, SEM filtro de fluxo${cap}`;
> 111	    }
> 112	    else if (!flowFresh) reason = 'fluxo stale/ausente → conservador (fail-closed, como a id2): baseline BTC NÃO liberada';
> 113	    else if (!flowOk) reason = `fluxo em capitulação (imbalance ${flow.imbalance} < ${FLOW_BUY_MIN}): baseline BTC veta o dip`;
> 114	    else reason = `regime=${regime} (mean-reversion: range/mixed) + fluxo ok: baseline BTC liberada`;
> 115	    // doctrine=true (auditoria): estes gates são a DOUTRINA por regime (o que a estratégia FARIA), NÃO confirmam
> 116	    // que a automação correspondente (ex.: baseline id2, hoje isActive=0) está ATIVA — o gate VIVO mora na
> 117	    // condition da automação no banco. O agente/painel deve reportar como doutrina, não como estado vivo.
> 118	    return { regime, regimeOk, flowOk, flowFresh: !!flowFresh, flowBuyMin: FLOW_BUY_MIN, flowGated, farm, baseline, trend, harvesterUngated: true, buyAllowed, reason, doctrine: true };
> 119	}
> 120	
> 121	// Reaplica regime/flow/gates FRESCOS (leituras baratas da MEMORY) sobre um snapshot, preservando a
> 122	// analítica CARA de 1m (price/dist/ev/tail/mc) na cadência do job. Motivo: o snapshot CONGELA regime/flow
> 123	// no tick de REFRESH_MS (60s); como o FLOW oscila em segundos (janela ~1000 aggTrades) e o REGIME é
> 124	// histerético, o agente lia o número VELHO do snapshot e o reportava como "contradição" vs o oráculo vivo.
> 125	// Aqui flow/regime/gates do payload SEMPRE refletem a MEMORY no instante da LEITURA, e expõe a idade do
> 126	// fluxo (flowAgeMs / flow.ageMs) p/ transparência. NÃO recomputa a analítica (custa klines; 60s de cache
> 127	// nela é aceitável e desejado). Usado pelos read-paths (endpoint agregado e por-símbolo) — read-only.
> 128	function freshen(symbol, snap) {
> 129	    if (!snap) return snap;
> 130	    const regime = beholder.getMemory(symbol, indexKeys.REGIME) || null;
> 131	    const flowRaw = beholder.getMemory(symbol, indexKeys.FLOW) || null;
> 132	    const flowAgeMs = flowRaw && Number.isFinite(flowRaw.atMs) ? Date.now() - flowRaw.atMs : null;
> 133	    const flow = flowRaw
> 134	        ? { imbalance: flowRaw.imbalance, toxicity: flowRaw.toxicity, atMs: Number.isFinite(flowRaw.atMs) ? flowRaw.atMs : null, ageMs: flowAgeMs }
> 135	        : null;
> 136	    const gates = deriveGates(regime, flowRaw, symbol);
> 137	    return { ...snap, regime, flow, gates, flowAgeMs };
> 138	}
> 139	
> 140	async function runOnce() {
> 141	    if (running) return;
> 142	    running = true;
> 143	    try {
> 144	        const symbols = await resolveSymbols();
> 145	        if (!symbols.length) return;
> 146	
> 147	        for (const symbol of symbols) {
> 148	            try {
> 149	                const m = await getCockpit(symbol, { lookback: LOOKBACK, breakevenPct: BREAKEVEN_PCT, tailK: TAIL_K, mcHorizonMin: MC_HORIZON });
> 150	                if (!m || m.unavailable) {
> 151	                    if (!UNAVAIL.has(symbol)) { UNAVAIL.add(symbol); logger('cockpit', `${symbol}: klines indisponíveis (${m ? m.reason : 'sem resposta'}); MEMORY preservada.`); }
> 152	                    continue;
> 153	                }
> 154	                if (UNAVAIL.delete(symbol)) logger('cockpit', `${symbol}: klines recuperadas.`);
> 155	
> 156	                // snapshot de regime/flow lido da MEMORY (já populada pelos outros jobs) — mesma leitura do flowJob
> 157	                const regime = beholder.getMemory(symbol, indexKeys.REGIME) || null;
> 158	                const flow = beholder.getMemory(symbol, indexKeys.FLOW) || null;
> 159	                const gates = deriveGates(regime, flow, symbol);
> 160	
> 161	                const snapshot = {
> 162	                    symbol, source: m.source, interval: m.interval,
> 163	                    price: m.price, samples: m.samples,
> 164	                    dist: m.dist, ev: m.ev, tail: m.tail, mc: m.mc,
> 165	                    regime,
> 166	                    flow: flow ? { imbalance: flow.imbalance, toxicity: flow.toxicity, atMs: flow.atMs || null } : null,
> 167	                    gates,
> 168	                    at: m.at, atMs: Date.now(),
> 169	                };
> 170	
> 171	                // PASSIVO/READ-ONLY: executeAutomations=FALSE — escreve a MEMORY, NUNCA dispara ordem.
> 172	                await beholder.updateMemory(symbol, indexKeys.COCKPIT, null, snapshot, false);
> 173	                LAST[symbol] = snapshot; AT[symbol] = Date.now();
> 174	            } catch (err) {
> 175	                logger('cockpit', `${symbol}: erro ao atualizar COCKPIT: ${err.message}`);
> 176	            }
> 177	        }
> 178	    } finally {
> 179	        running = false;
> 180	    }
> 181	}
> 182	
> 183	function start() {
> 184	    if (!ENABLED) { logger('cockpit', 'Cockpit job DESABILITADO (COCKPIT_JOB_ENABLED=false).'); return; }
> 185	    if (timer) return; // idempotente
> 186	    runOnce(); // primeira passada imediata no boot
> 187	    timer = setInterval(runOnce, REFRESH_MS);
> 188	    if (timer.unref) timer.unref(); // não segura o processo no shutdown
> 189	    logger('cockpit', `Cockpit job iniciado READ-ONLY (intervalo ${REFRESH_MS}ms; lookback ${LOOKBACK}; break-even ${BREAKEVEN_PCT}%). Informativo — não gateia automação.`);
> 190	}
> 191	
> 192	function stop() {
> 193	    if (timer) { clearInterval(timer); timer = null; }
> 194	    running = false;
> 195	}
> 196	
> 197	// Status/snapshot agregado p/ o endpoint e observabilidade (por símbolo o último COCKPIT + idade).
> 198	function getStatus() {
> 199	    const now = Date.now();
> 200	    const symbols = {};
> 201	    for (const s of Object.keys(LAST)) {
> 202	        // freshen: regime/flow/gates no instante da leitura (mata a defasagem de até REFRESH_MS do snapshot);
> 203	        // ageMs aqui é a idade da ANALÍTICA (snapshot), distinta de flow.ageMs (idade do fluxo) que o freshen anexa.
> 204	        symbols[s] = { ...freshen(s, LAST[s]), ageMs: AT[s] ? now - AT[s] : null, stale: AT[s] ? (now - AT[s]) > REFRESH_MS * 3 : true, unavailable: UNAVAIL.has(s) };
> 205	    }
> 206	    return { enabled: ENABLED, refreshMs: REFRESH_MS, lookback: LOOKBACK, breakevenPct: BREAKEVEN_PCT, flowBuyMin: FLOW_BUY_MIN, running, symbols };
> 207	}
> 208	
> 209	module.exports = { start, stop, runOnce, getStatus, freshen };
> 210	
> ```

## 🤖 Claude *(16:47:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"baseline\" /home/gcrux-tradeux/tradeux/frontend/src 2>/dev/null; echo \"=====MCP index.js 220-245=====\"; sed -n '220,245p' /home/gcrux-tradeux/tradeux/tradeux-mcp/src/index.js",
  "description": "Find baseline usage in frontend and MCP cockpit tool"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/cockpit.css:49:.cockpit .cx-brand { display: flex; align-items: baseline; gap: 12px; }
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/cockpit.css:99:.cockpit .cx-sub { display: flex; align-items: baseline; gap: 14px; margin-top: 6px; flex-wrap: wrap; }
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/cockpit.css:164:.cockpit .cx-candle-head { display: flex; align-items: baseline; gap: 12px; margin-bottom: 8px; }
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js:379:                        // só a baseline BTC (flowGated=true) é bloqueada por fluxo; o FARM das alts NÃO gateia por
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js:386:                        // trend o farm/baseline ficam em CAIXA). Usa cpg.farm (backend); fallback exclui os 3.
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js:395:                          ? `fluxo ${flowOk ? 'ok' : 'capitulação'} (imbalance ${imb != null ? imb.toFixed(2) : '—'}) — gateia a baseline BTC`
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js:412:                <div className="cx-note">Cada ponte acende quando o gate de COMPRA do símbolo abre: <b>BTC (baseline)</b> = regime ≠ bear/trend <b>E</b> fluxo não-capitulação; <b>alts (farm)</b> = só regime ≠ bear/trend (o fluxo é <b>informativo·i</b>, não gateia). "go" = condições prontas; a ordem em si segue gateada e sob HALT.</div>
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js:425:                <div className="cx-line"><span className="l"><span className="cx-seal real" /> Gate acumulação BTC <span className="cx-flat" style={{ fontSize: '0.66rem' }}>(farm/baseline)</span></span><span className={`v cx-mono ${cpBtc && cpBtc.gates ? (cpBtc.gates.buyAllowed ? 'cx-up' : 'cx-down') : ''}`} title={cpBtc && cpBtc.gates ? cpBtc.gates.reason : ''}>{cpBtc && cpBtc.gates ? (cpBtc.gates.buyAllowed ? 'GO' : 'CAIXA') : '—'}</span></div>
> =====MCP index.js 220-245=====
>     for (const [sym, c] of Object.entries(d.symbols || {})) {
>       const dist = c.dist || {}, ev = c.ev || {}, mc = c.mc || {}, gates = c.gates || {};
>       out.symbols[sym] = {
>         price: c.price, regime: c.regime,
>         flow: c.flow ? { imbalance: c.flow.imbalance, toxicity: c.flow.toxicity, ageSec: Number.isFinite(c.flow.ageMs) ? Math.round(c.flow.ageMs / 1000) : null } : null,
>         medAbsMovePct: dist.medAbsMovePct, sigmaPct: dist.sigmaPct, pHitBreakevenPct: dist.pHitBreakevenPct,
>         evNetPct: ev.netPct, breakevenPct: ev.breakevenPct,
>         mc: { p10: mc.p10, p50: mc.p50, p90: mc.p90, horizonMin: mc.horizonMin, driftless: true },
>         buyGate: { allowed: gates.buyAllowed, reason: gates.reason, flowFresh: gates.flowFresh, flowGated: gates.flowGated, farm: gates.farm, baseline: gates.baseline },
>         stale: c.stale,
>       };
>     }
>     return out;
>   }
> );
> 
> // ----------------------------------------------------------------------------
> // LEITURA — ordens, automações, monitores, templates
> // ----------------------------------------------------------------------------
> 
> readTool(
>   "tradeux_list_orders",
>   "Histórico de ordens (paginado). Pode filtrar por símbolo.",
>   {
>     symbol: z.string().optional().describe("Par, ex: BTCUSDT"),
>     page: z.number().int().positive().optional().describe("Página (default 1)"),
> ```

## 🤖 Claude *(16:47:23)*

Vou ler o resto do `Cockpit.js` (a seção de "pontes" / bridges que monta os badges das alts) para confirmar como o frontend interpreta `gates.baseline` e `gates.farm`, já que essa é a peça que pode quebrar com `null`.

## 🤖 Claude *(16:47:25)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js",
  "offset": 360,
  "limit": 70
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 360	                            <span className="cx-sym cx-mono">{s}</span>
> 361	                            <span className={`cx-reg ${reg}`}>{reg}{g.stale ? '·s' : ''}</span>
> 362	                            <span className="cx-flowbar"><span className="mid" />{imb != null && <span className={`fill ${imb >= 0 ? 'buy' : 'sell'}`} style={{ width: w + '%' }} />}</span>
> 363	                            <span className={`cx-imb cx-mono ${imb == null ? 'cx-flat' : imb < -0.05 ? 'cx-down' : imb > 0.05 ? 'cx-up' : 'cx-flat'}`}>{imb != null ? imb.toFixed(2) : '—'}</span>
> 364	                            <span className={`cx-tox cx-mono ${tox != null && tox >= 0.6 ? 'hot' : ''}`}>{tox != null ? tox.toFixed(2) : '—'}</span>
> 365	                          </div>
> 366	                        );
> 367	                      })}
> 368	                </div>
> 369	                <div className="cx-note">Colunas: regime do gate · barra de <b>imbalance</b> do taker (verde compra/vermelho vende) · valor · <b>toxicity</b> (|imbalance|). Nowcasting de timing — não previsão.</div>
> 370	              </div>
> 371	
> 372	              <div className="cx-panel">
> 373	                <div className="cx-panel-title"><span><span className="cx-seal real" /> Trade bridges (gates de compra)</span></div>
> 374	                <div className="cx-bridges">
> 375	                  {symbols.length === 0
> 376	                    ? <div className="cx-empty">sem sinais ainda</div>
> 377	                    : symbols.map(s => {
> 378	                        // Fonte de verdade = gate SYMBOL-AWARE do cockpit (cp.symbols[s].gates, commit 8884bd3):
> 379	                        // só a baseline BTC (flowGated=true) é bloqueada por fluxo; o FARM das alts NÃO gateia por
> 380	                        // fluxo → p/ alts a ponte de fluxo é INFORMATIVA, não bloqueante. Fallback regime/flow-status.
> 381	                        const cps = (cp.symbols || {})[s] || {};
> 382	                        const cpg = cps.gates || {};
> 383	                        const g = (gate.symbols || {})[s] || {};
> 384	                        const f = (flow.symbols || {})[s] || {};
> 385	                        // nó "regime" = gate de regime da ACUMULAÇÃO (farm) → exclui bear/unknown E trend (em
> 386	                        // trend o farm/baseline ficam em CAIXA). Usa cpg.farm (backend); fallback exclui os 3.
> 387	                        const regOpen = cpg.farm != null ? cpg.farm : !!(g.regime && g.regime !== 'bear' && g.regime !== 'unknown' && g.regime !== 'trend');
> 388	                        const flowGated = !!cpg.flowGated;
> 389	                        const imb = (cps.flow && cps.flow.imbalance != null) ? cps.flow.imbalance : f.imbalance;
> 390	                        const flowMin = cpg.flowBuyMin != null ? cpg.flowBuyMin : -0.4;
> 391	                        const flowOk = imb != null && imb >= flowMin; // não-capitulação (>= piso, igual ao backend)
> 392	                        const ready = cpg.buyAllowed != null ? cpg.buyAllowed : (regOpen && (!flowGated || flowOk));
> 393	                        const flowDot = flowGated ? (flowOk ? 'on' : 'off') : 'info'; // alt: informativo (não gateia)
> 394	                        const flowTitle = flowGated
> 395	                          ? `fluxo ${flowOk ? 'ok' : 'capitulação'} (imbalance ${imb != null ? imb.toFixed(2) : '—'}) — gateia a baseline BTC`
> 396	                          : `fluxo INFORMATIVO (imbalance ${imb != null ? imb.toFixed(2) : '—'}) — o FARM desta alt NÃO gateia por fluxo`;
> 397	                        return (
> 398	                          <div className="cx-bridge" key={s}>
> 399	                            <span className="bsym cx-mono">{s}</span>
> 400	                            <span className="cx-chain">
> 401	                              <span className="cx-node"><span className={`dot ${regOpen ? 'on' : 'off'}`} /><span className="nl">regime</span></span>
> 402	                              <span className={`cx-link ${regOpen ? 'on' : ''}`} />
> 403	                              <span className="cx-node" title={flowTitle}><span className={`dot ${flowDot}`} /><span className="nl">fluxo{flowGated ? '' : '·i'}</span></span>
> 404	                              <span className={`cx-link ${ready ? 'on' : ''}`} />
> 405	                              <span className="cx-node"><span className={`dot ${ready ? 'on' : 'off'}`} /><span className="nl">pronto</span></span>
> 406	                            </span>
> 407	                            <span className={`cx-ready ${ready ? 'go' : 'no'}`}>{ready ? 'go' : 'wait'}</span>
> 408	                          </div>
> 409	                        );
> 410	                      })}
> 411	                </div>
> 412	                <div className="cx-note">Cada ponte acende quando o gate de COMPRA do símbolo abre: <b>BTC (baseline)</b> = regime ≠ bear/trend <b>E</b> fluxo não-capitulação; <b>alts (farm)</b> = só regime ≠ bear/trend (o fluxo é <b>informativo·i</b>, não gateia). "go" = condições prontas; a ordem em si segue gateada e sob HALT.</div>
> 413	              </div>
> 414	            </div>
> 415	
> 416	            {/* ROW 4 — edge/agent + positions */}
> 417	            <div className="cx-row-3">
> 418	              <div className="cx-panel">
> 419	                <div className="cx-panel-title"><span><span className="cx-seal real" /> Edge vs fee · agente</span><span className="cx-src">/analysis/cockpit · /agent/runs</span></div>
> 420	                <div className="cx-edge">
> 421	                  <div className="e"><div className="el">EV/trade net (1m)</div><div className={`ev cx-mono ${cpBtc && evNet != null ? dirClass(evNet) : ''}`}>{cpBtc && evNet != null ? (evNet > 0 ? '+' : '') + Number(evNet).toFixed(3) + '%' : '—'}</div></div>
> 422	                  <div className="e"><div className="el">Break-even fee</div><div className="ev cx-mono">{FEE_RT.toFixed(2)}% <span className="cx-flat" style={{ fontSize: '0.7rem' }}>· {FEE_RT_BNB.toFixed(2)}% BNB</span></div></div>
> 423	                </div>
> 424	                <div className="cx-line" style={{ marginTop: 10 }}><span className="l"><span className="cx-seal real" /> Moves ≥ break-even (BTC)</span><span className="v cx-mono">{cpBtc && cpBtc.dist ? Number(cpBtc.dist.pHitBreakevenPct).toFixed(0) + '%' : '—'}</span></div>
> 425	                <div className="cx-line"><span className="l"><span className="cx-seal real" /> Gate acumulação BTC <span className="cx-flat" style={{ fontSize: '0.66rem' }}>(farm/baseline)</span></span><span className={`v cx-mono ${cpBtc && cpBtc.gates ? (cpBtc.gates.buyAllowed ? 'cx-up' : 'cx-down') : ''}`} title={cpBtc && cpBtc.gates ? cpBtc.gates.reason : ''}>{cpBtc && cpBtc.gates ? (cpBtc.gates.buyAllowed ? 'GO' : 'CAIXA') : '—'}</span></div>
> 426	                <div className="cx-line"><span className="l"><span className="cx-seal todo" /> Shadow 1m — P(cont. ≥ custo)</span><span className="v cx-flat">medindo… (Fase 3)</span></div>
> 427	                {agent.available === false
> 428	                  ? <div className="cx-empty">agente ainda não rodou (journal ausente)</div>
> 429	                  : <React.Fragment>
> ```

## 🤖 Claude *(16:47:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"\\.baseline\\|gates\\.baseline\\|cpg\\.baseline\\|buyGate\\|\\.farm\" /home/gcrux-tradeux/tradeux/frontend/src /home/gcrux-tradeux/tradeux/tradeux-agent/src 2>/dev/null",
  "description": "Find all consumers of gates.baseline/farm across frontend and agent"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/agent.js:42:  (6) buyGate de acumulação liberado com regime=mixed: CORRETO (range E mixed são mean-reversion; condition viva = regime != bear E != trend) — não sugira "respeitar só range".
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js:386:                        // trend o farm/baseline ficam em CAIXA). Usa cpg.farm (backend); fallback exclui os 3.
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js:387:                        const regOpen = cpg.farm != null ? cpg.farm : !!(g.regime && g.regime !== 'bear' && g.regime !== 'unknown' && g.regime !== 'trend');
> ```

## 🤖 Claude *(16:48:11)*

Tenho tudo que preciso. Vou confirmar o último ponto: como o frontend lê `gates.baseline` do BTC (linha 425 usa `buyAllowed`, não `baseline`), e checar se há algum lugar que renderize `gates.baseline` diretamente como booleano (que com `null` mostraria vazio).

O frontend nunca lê `cpg.baseline` diretamente — usa `cpg.farm`, `cpg.buyAllowed`, `cpg.flowGated`, `cpg.flowBuyMin`. O MCP repassa `baseline: gates.baseline` cru no `buyGate`. Tenho o quadro completo.

---

# Review — fix de gate-fantasma `baseline` no cockpit (NÃO-COMMITADO)

**Arquivos:** `/home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js` (`deriveGates`, L96-118) e `/home/gcrux-tradeux/tradeux/tradeux-mcp/src/index.js` (descrição do tool `tradeux_get_cockpit`, L215).

## VEREDITO: APPROVE

Mudança pequena, cirúrgica, reversível, read-only fora do money-path. Aprovo o merge. As sugestões abaixo são todas nice-to-have.

## 1. Direcional vs nuance — concordo: é direcional, fix estrutural legítimo

Não é re-litígio do que o TL anterior fechou. O TL anterior pediu pra parar de perseguir **paridade 1:1 do VIEW** (nuances de número/idade do flow, "cockpit vs oráculo vivo", interpolação de `reason`). Aqui o caso é categoricamente diferente: o payload afirma a **existência de um estado de gate de um módulo que não existe para aquele símbolo**. `baseline` é definido na própria doutrina do código (L82-83, L88) como "o ÚNICO módulo de acumulação flow-gated" = só BTC. Expor `baseline=true` para BNBUSDT não é uma nuance de precisão — é um campo logicamente **mal-tipado para a alt** (`true`/`false` ambos mentem; o valor honesto é "não se aplica").

Isso é uma mentira **estrutural e direcional**: faz o consumidor (agente) afirmar coisa falsa sobre o símbolo, e é a raiz provada de uma notificação recorrente (3ª/4ª vez). A regra de ouro "consertar a fonte, não a interpretação" se aplica perfeitamente — e é o **oposto** de empilhar regra no prompt. `baseline = flowGated ? baselineRaw : null` remove o campo-fantasma na origem (resposta à sua pergunta 5: sim, reduz a superfície de falso-flag de forma durável).

## 2. `buyAllowed` inalterado — CONFIRMADO, risco zero no money-path

`buyAllowed = flowGated ? baselineRaw : farm` é byte-idêntico ao anterior, agora apoiado em `baselineRaw` (que é o antigo `baseline`: `farm && flowOk`). BTC → `baselineRaw`; alt → `farm`. O gate OPERATIVO não muda. Reforçando o óbvio mas importante: este job é `executeAutomations=false` (L172) e **não gateia nada** (L11) — o gate vivo mora na `condition` da automação no banco. Blast radius real é só a VIEW/agente. Nada toca `beholder.js` hot-path nem order flow.

## 3. `null` como sentinela — escolha certa; nenhum consumidor quebra

Validei os três consumidores:

- **Frontend `Cockpit.js`** — nunca lê `cpg.baseline`. As bridges usam `cpg.farm`, `cpg.buyAllowed`, `cpg.flowGated`, `cpg.flowBuyMin` (todos com guards `!= null`, L387/390/392). O card "Gate acumulação BTC" (L425) usa `gates.buyAllowed`. `baseline=null` é simplesmente ignorado. Zero impacto visual.
- **MCP `index.js:228`** — repassa cru: `baseline: gates.baseline`. `null` serializa em JSON limpo (vira `null`, não some, não vira `NaN`). É exatamente a semântica n/a desejada, e o agente lê o tool-text atualizado que explica o `null`.
- **Agente** — só consome via MCP; `agent.js:42` fala de "buyGate de acumulação liberado", não de `baseline` por nome.

`null` é melhor que `false` (que mentiria "gate fechado") e melhor que omitir o campo (a forma do objeto fica estável entre BTC e alts — bom para o agente diffar símbolos sem `undefined`). Escolha correta.

## 4. Convenção/manutenção — boa, pt-BR, escopo mínimo

Comentário pt-BR claro e honesto, nomeia o problema ("gate-FANTASMA"), explica por que `null` e afirma o invariante ("buyAllowed e farm ficam INTACTOS"). A nota do MCP é coerente e amarra na doutrina GATE≠GATILHO já vigente. Escopo mínimo: 1 linha de lógica + 1 frase de doc. Sem bikeshedding.

## Must-fix
Nenhum.

## Nice-to-have (não bloqueiam)
- **Inconsistência interna pequena no tool-text do MCP:** a frase nova diz "nem farm aberto com **RSI>35/25**" e a antiga parte da descrição não menciona limiar; o `reason` do backend (L110) fala "RSI" sem número. É cosmético — o agente entende GATE≠GATILHO. Só registro pra não virar dívida: padronizar o jargão de RSI num lugar só depois.
- **Comentário L101 cita "RSI>25"** como exemplo do que o agente lia como incoerência; o falso-flag relatado foi "RSI ~53 > 25". Coerente, mas se quiser, alinhar o exemplo do comentário com o threshold real da farm evita confusão futura.

## Decisão de merge

**MERGE — APPROVE, sem condições.** Subir os dois arquivos juntos (são um par lógico: o backend para de emitir o campo-fantasma, o MCP documenta o `null` para o leitor). Sem migration, sem mudança de money-path, CI deve passar trivialmente (frontend build não toca; backend migrate/seed inalterado; agent `--check` não depende deste campo).

Recomendo rodar o pre-flight mínimo antes do push para fechar o gate de processo:
- `bash /home/gcrux-tradeux/tradeux/scripts/ci-preflight.sh --only-lint` (não há migration aqui, mas é barato)
- após deploy, um `GET /analysis/cockpit` conferindo `symbols.BNBUSDT.gates.baseline === null` e `symbols.BTCUSDT.gates.baseline` ainda booleano — validação ao vivo de 10s que fecha o loop.

Ordem/ops: commit em branch + push via a chave do `ubuntu` rodando como root + chown do `.git` de volta para `gcrux-tradeux` (gotcha conhecido). Não direto-no-master sem o push-helper habitual.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-17 - agent-a1a351de1820e4318]]
> * **Próxima Sessão**: [[2026-06-17 - agent-aa1d4a413cde4ecbc]]
%% --- TIMELINE END --- %%

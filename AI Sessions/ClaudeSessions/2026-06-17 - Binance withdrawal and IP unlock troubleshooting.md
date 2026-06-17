# Binance withdrawal and IP unlock troubleshooting
**Date:** 2026-06-17 | **Session ID:** `ffaf623b-aacb-40b8-9160-28ef147ccb48`

---

## 👤 User *(02:31:30)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(02:31:30)*

# ShakeHands — /handson (TradeUX session pick-up)

Execute the ShakeHands `/handson` ritual. Load full context in <10s — trust
`HANDOFF.md`, do not re-discover the file tree. (See skill `shake-hands`.)

## PRE-FLIGHT (run in parallel)
```bash
cat /home/gcrux-tradeux/HANDOFF.md
git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' log --oneline -7
git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' status --short
sudo -n -u gcrux-tradeux bash -lc 'cd /home/gcrux-tradeux/tradeux && docker compose ps' 2>/dev/null || docker ps --filter name=tradeux --format "table {{.Names}}\t{{.Status}}"
curl -s -m5 -o /dev/null -w "site https://tradeux.gcrux.com -> %{http_code}\n" https://tradeux.gcrux.com/
```
Read in parallel: `HANDOFF.md`, repo `CLAUDE.md`, `/home/ubuntu/.claude/projects/-home-gcrux-tradeux/memory/MEMORY.md`.

## BRIEF OUTPUT (pt-BR)
```
═══════════════════════════════════════════════════
  HANDSON — <fase> (<data do último seal>)
═══════════════════════════════════════════════════
🏁 ESTADO     : <fase atual + 1 linha>
🧾 COMMITS    : <3 últimos hash — msg>
🐳 STACK      : db/backend/frontend <status> · site <HTTP>
📈 BASELINE   : automações <ativas?> · símbolos <synced?> · ordens <n>
🔀 PRs ABERTOS: <lista — lembrete de merge>
📂 PENDENTE   : <dirty files, ou "worktree limpo">
⚡ PRÓXIMO    : <1º item dos Next Steps do HANDOFF.md>
⚠️ ALERTAS    : <stack unhealthy / dirty conflitante / PRs sem merge / ou "nenhum">
═══════════════════════════════════════════════════
  Pronto pra trabalhar. Aguardando direção.
═══════════════════════════════════════════════════
```

## Rules
- Trust HANDOFF.md; do NOT auto-restart unhealthy containers.
- Dirty files → describe as "trabalho não-commitado da sessão anterior"; do NOT commit.
- Always surface open PRs as a merge reminder (we can't merge — no gh/token).


## 🤖 Claude *(02:31:35)*


## 🤖 Claude *(02:31:35)*

I'll run the pre-flight checks and read context files in parallel.

## 🤖 Claude *(02:31:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat /home/gcrux-tradeux/HANDOFF.md",
  "description": "Read HANDOFF.md state file"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> <persisted-output>
> Output too large (112.3KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrux-tradeux/ffaf623b-aacb-40b8-9160-28ef147ccb48/tool-results/btcx58g3e.txt
> 
> Preview (first 2KB):
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
> ...
> </persisted-output>
> ```

## 🤖 Claude *(02:31:37)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' log --oneline -7",
  "description": "Show last 7 commits"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 0b1554d docs(agent): doutrina GATE != TRIGGER no SYSTEM_PROMPT (fecha a classe gate-aberto-mas-condicao)
> 2c8655c fix(cockpit-ui): painel "Trade bridges" consome o gate symbol-aware (alt = fluxo informativo)
> 8884bd3 fix(cockpit): gate de acumulacao symbol-aware (alt FARM nao gateia por fluxo)
> 37ed4b1 refactor(agent): consolida doutrina anti-ruido do SYSTEM_PROMPT num bloco "DIVERGENCIAS ESPERADAS"
> bf254a0 fix(cockpit): reason do gate reflete o regime real (mixed != "range" hardcoded)
> 64752f0 feat(agent): dedup de notificacao por assunto em codigo (anti-spam defesa em profundidade)
> 6042bd9 fix(cockpit): freshen no read-path (flow/regime/gates vivos + idade) + anti-spam do agente
> ```

## 🤖 Claude *(02:31:38)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' status --short",
  "description": "Show working tree status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> (Bash completed with no output)
> ```

## 🤖 Claude *(02:31:39)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sudo -n -u gcrux-tradeux bash -lc 'cd /home/gcrux-tradeux/tradeux && docker compose ps' 2>/dev/null || docker ps --filter name=tradeux --format \"table {{.Names}}\\t{{.Status}}\"",
  "description": "Show docker stack status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> NAME                 IMAGE              COMMAND                  SERVICE    CREATED       STATUS                  PORTS
> tradeux-agent-1      tradeux-agent      "docker-entrypoint.s…"   agent      4 hours ago   Up 4 hours              
> tradeux-backend-1    tradeux-backend    "docker-entrypoint.s…"   backend    4 hours ago   Up 4 hours              3001/tcp
> tradeux-db-1         mysql:8.0          "docker-entrypoint.s…"   db         2 weeks ago   Up 34 hours (healthy)   3306/tcp, 33060/tcp
> tradeux-frontend-1   tradeux-frontend   "/docker-entrypoint.…"   frontend   4 hours ago   Up 4 hours              127.0.0.1:8090->80/tcp
> ```

## 🤖 Claude *(02:31:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "curl -s -m5 -o /dev/null -w \"site https://tradeux.gcrux.com -> %{http_code}\\n\" https://tradeux.gcrux.com/",
  "description": "Check site HTTP status"
}
```

## 🤖 Claude *(02:31:40)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/CLAUDE.md"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> site https://tradeux.gcrux.com -> 200
> ```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# CLAUDE.md
> 2	
> 3	This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
> 4	
> 5	## What this is
> 6	
> 7	TradeUX is a multi-coin trading bot for **Binance Spot** with a web UI. The decision
> 8	core is based on **Beholder 2.1** (LuizTools' course) and is packaged to deploy in one
> 9	command with Docker. Three milestones live in one monorepo:
> 10	
> 11	- **`backend/`** + **`frontend/`** — the running product (manual operation). Node/Express
> 12	  + Sequelize + WebSocket API, React UI served by nginx.
> 13	- **`tradeux-mcp/`** — an MCP server that exposes the backend's REST API as tools.
> 14	- **`tradeux-agent/`** — an LLM agent (Anthropic or OpenRouter) that drives the bot
> 15	  through `tradeux-mcp`, with guardrails and an evaluation journal.
> 16	
> 17	## Architecture (the big picture)
> 18	
> 19	### Backend — the Beholder "brain" (`backend/src/`)
> 20	The backend is more than a CRUD API; it runs a stateful trading engine. Entry point is
> 21	`server.js`, which boots everything in order: load default settings → init the Beholder
> 22	brain with active automations → start the scheduler → start Express → attach WebSocket →
> 23	init the exchange/event monitor. The moving parts:
> 24	
> 25	- **`beholder.js`** — the in-memory engine. Holds `MEMORY` (live market state per
> 26	  symbol/index, e.g. MINI_TICKER, BOOK) and `BRAIN` (compiled automations indexed by the
> 27	  memory keys they react to). `updateMemory()` is called on every market tick and returns
> 28	  the automations whose conditions just fired. This is mutable module-level state guarded
> 29	  by `LOCK_*` flags — treat it carefully; it is the hot path.
> 30	- **`app-em.js`** (event/exchange monitor) — subscribes to Binance streams via
> 31	  `utils/exchange.js`, feeds ticks into `beholder.updateMemory`, and broadcasts results
> 32	  to UI clients. `app-ws.js` is the WebSocket server (JWT-authenticated via `?token=` in
> 33	  the URL). `app.js` is the Express app; `agenda.js` runs scheduled automations.
> 34	- **Layering**: `routers/` → `controllers/` → `repositories/` (Sequelize) → `models/`.
> 35	  Most domain concepts come in this full stack: settings, symbols, orders, monitors,
> 36	  automations, orderTemplates, withdrawTemplates, plus beholder/exchange/logs. When adding
> 37	  a feature, follow this chain end to end.
> 38	- **`utils/`** — `exchange.js` (node-binance-api wrapper, the Binance boundary),
> 39	  `crypto.js` (AES-256 for API-key storage — needs `AES_KEY` exactly 32 chars),
> 40	  `indexes.js` (technical-indicator calc + memory index keys), plus notification channels
> 41	  (email, sms, telegram, push).
> 42	
> 43	### MCP server (`tradeux-mcp/src/`)
> 44	A thin **stdio** MCP server. `api.js` is an HTTP client to the backend that logs in once
> 45	(`/login`), caches the JWT, and re-auths on 401. `index.js` registers ~25 tools named
> 46	`tradeux_*` (read: `get_wallet`, `get_price`, `get_analysis`, `get_memory`,
> 47	`list_orders`…; write: `place_order`, `cancel_order`, `start_automation`,
> 48	`stop_automation`…). It needs `TRADEUX_API_URL`, `TRADEUX_EMAIL`, `TRADEUX_PASSWORD`.
> 49	
> 50	### Agent (`tradeux-agent/src/`)
> 51	`index.js` is the CLI (`--check` lists MCP tools and exits; `--once` runs one cycle;
> 52	no flag = loop every `TRADEUX_AGENT_INTERVAL`). `mcpClient.js` spawns `tradeux-mcp` over
> 53	stdio (default path `../../tradeux-mcp/src/index.js`) and converts MCP tools to the model
> 54	tool format. `agent.js` runs the decision loop: a stable `SYSTEM_PROMPT` holding the
> 55	trading persona + **guardrails**, then up to `MAX_TOOL_ROUNDS` of tool calls, recording
> 56	everything to the journal. `providers/` abstracts Anthropic vs OpenRouter (selected by
> 57	`TRADEUX_AGENT_PROVIDER`). **Writes are gated by `TRADEUX_ALLOW_TRADING` (default off).**
> 58	
> 59	## Deployment model (decided)
> 60	
> 61	- **Operational DB = MySQL in the bundled Docker stack** (source of truth for orders,
> 62	  settings, automations). Self-contained — `./setup.sh` brings up `db` + `backend` +
> 63	  `frontend` on an isolated network/volume. This is the default and the validated path.
> 64	- **Memory / RAG = Supabase pgvector**, in a dedicated `tradeux_memory` database — kept
> 65	  separate from the operational DB. (Agent memory layer is a later milestone.)
> 66	- The backend uses Sequelize and speaks **both MySQL and Postgres**; migrations are
> 67	  portable (CI proves migrate+seed on both). The Supabase override
> 68	  (`docker-compose.supabase.yml`) exists for running the operational DB on Postgres
> 69	  instead, but the chosen setup keeps operational on the bundled MySQL.
> 70	- **Production fronting**: behind CloudPanel/Cloudflare set `WEB_BIND=127.0.0.1` and a
> 71	  free `WEB_PORT` (e.g. 8090), and the reverse proxy **must enable WebSocket upgrade**
> 72	  (the `/ws` endpoint depends on it). Run as the site's own system user (e.g.
> 73	  `gcrux-tradeux`), not root. `REACT_APP_*` URLs are baked into the React build, so they
> 74	  must be set correctly **before** building the frontend image.
> 75	
> 76	> The backend **must be able to reach Binance** — run it where Binance's API is not
> 77	> geo-blocked. Switching the DB to Supabase does not change this.
> 78	
> 79	## Commands
> 80	
> 81	### Full stack (Docker)
> 82	```bash
> 83	./setup.sh            # one-command bootstrap: create .env, generate secrets, validate, up
> 84	make up               # = ./setup.sh
> 85	make logs / ps / restart / down
> 86	make nuke             # down -v — DELETES the database volume
> 87	make migrate / seed   # run sequelize migrate / seed inside the backend container
> 88	
> 89	# Supabase/Postgres as the operational DB (no local MySQL):
> 90	docker compose -f docker-compose.yml -f docker-compose.supabase.yml up -d --build backend frontend
> 91	```
> 92	`setup.sh` auto-generates `JWT_SECRET` (32 bytes hex) and `AES_KEY` (16 bytes = 32 chars).
> 93	On first run it stops if required `.env` fields (DB passwords, panel login, Binance keys)
> 94	are blank — fill them and re-run. The backend container's `docker-entrypoint.sh` runs
> 95	`db:migrate` + `db:seed:all` (idempotent) on every boot.
> 96	
> 97	### Backend (host dev, `backend/`)
> 98	```bash
> 99	npm run dev           # nodemon + dotenv
> 100	npm start             # node -r dotenv/config ./src/server
> 101	npm run migratedb     # npx sequelize-cli db:migrate
> 102	npm run seeddb        # npx sequelize-cli db:seed:all
> 103	# Run a single migration: npx sequelize-cli db:migrate --to <YYYYMMDD-name.js>
> 104	# Undo last:             npx sequelize-cli db:migrate:undo
> 105	```
> 106	Sequelize config is `backend/config/` and reads `DB_*` from env. Seeders use
> 107	`seederStorage: 'sequelize'` so `db:seed:all` is idempotent. There are no unit tests; the
> 108	CI's "tests" are migrate+seed (both dialects) and the agent `--check` integration.
> 109	
> 110	### Frontend (`frontend/`) — Vite/React
> 111	```bash
> 112	npm run dev           # vite dev server
> 113	npm run build         # production bundle (what CI and the Docker image run)
> 114	npm run preview
> 115	```
> 116	
> 117	### MCP + agent
> 118	```bash
> 119	# tradeux-mcp/  — usually launched by the agent, not directly
> 120	npm start
> 121	
> 122	# tradeux-agent/
> 123	node src/index.js --check   # connect MCP, list tools, exit (no model key needed)
> 124	node src/index.js --once    # one decision cycle
> 125	node src/index.js           # loop
> 126	```
> 127	
> 128	## CI (`.github/workflows/ci.yml`)
> 129	Three jobs, all on Node 22, triggered on PRs and pushes to `main`/`master`:
> 130	1. **frontend** — `vite build` must compile.
> 131	2. **backend** — matrix `[mysql, postgres]`: `db:migrate` + `db:seed:all`, then re-run to
> 132	   prove idempotency. Keep migrations/seeds portable across **both** dialects.
> 133	3. **integration** — installs `tradeux-mcp` + `tradeux-agent` and runs the agent
> 134	   `--check` (validates the MCP bridge end to end, no backend or model key).
> 135	
> 136	### CI Pre-flight (rodar ANTES de todo push)
> 137	```bash
> 138	# Lint rápido de migrations (< 1s) — detecta camelCase sem quoting, backticks
> 139	# hardcoded, e outros padrões que quebram no Postgres
> 140	bash scripts/ci-lint-migrations.sh
> 141	
> 142	# CI completo local (~2min) — espelha o GitHub Actions:
> 143	# lint + frontend build + MySQL migrate+seed + Postgres efêmero + agent --check
> 144	bash scripts/ci-preflight.sh
> 145	
> 146	# Só lint, sem containers nem build
> 147	bash scripts/ci-preflight.sh --only-lint
> 148	
> 149	# Pular etapas específicas
> 150	bash scripts/ci-preflight.sh --skip-frontend     # só mexeu no backend
> 151	bash scripts/ci-preflight.sh --skip-postgres      # sem Docker disponível
> 152	bash scripts/ci-preflight.sh --skip-agent         # sem deps do agent instaladas
> 153	```
> 154	
> 155	**Regra de ouro para migrations dual-dialect:** nunca escreva SQL raw com
> 156	identificadores camelCase sem `queryInterface.quoteIdentifier()`. MySQL usa
> 157	backticks, Postgres usa aspas duplas — o `quoteIdentifier()` abstrai isso.
> 158	```javascript
> 159	// ✅ Portável (ambos dialetos)
> 160	const qi = queryInterface.quoteIdentifier.bind(queryInterface);
> 161	await queryInterface.sequelize.query(
> 162	  `UPDATE ${qi('settings')} SET ${qi('testnetApiUrl')} = ${qi('apiUrl')} WHERE id = 1`
> 163	);
> 164	```
> 165	Skill completo: `.gemini/skills/tradeux-ci-guard/SKILL.md`
> 166	Workflow agente: `.gemini/workflows/ci-preflight.md`
> 167	
> 168	## Conventions & gotchas
> 169	- **Secrets**: `AES_KEY` must be exactly 32 chars (AES-256) — `setup.sh` enforces it; do
> 170	  not hand-edit it to another length. API keys are AES-encrypted at rest via `crypto.js`.
> 171	- **Testnet first**: default `.env` points at Binance **mainnet (real money)**. For
> 172	  testing use `testnet.binance.vision` for the API and **`stream.testnet.binance.vision`**
> 173	  (note the `stream.` host) for the stream, and keep `TRADEUX_ALLOW_TRADING` off.
> 174	- **Frontend env is build-time**: `REACT_APP_API_URL`, `REACT_APP_WS_URL`,
> 175	  `REACT_APP_BWS_URL` are compiled into the bundle (passed as Docker build args). Changing
> 176	  them requires a frontend rebuild, not just a restart.
> 177	- **Two databases, one engine each**: backend talks to one operational DB (MySQL by
> 178	  default); when on Postgres set `DB_DIALECT=postgres` and `DB_SSL=true` for managed
> 179	  Postgres (Supabase). Do not point the backend at the `tradeux_memory` RAG database.
> 180	- **Comments and docs in this repo are in Portuguese (pt-BR)** — match that when editing.
> 181	- See `SECURITY.md` for the dependency/vulnerability posture before bumping deps.
> 182	
> 183	## Branching
> 184	Active development branch for the current task: `claude/github-project-review-setup-k2ELV`.
> 185	CI runs on `main`/`master`.
> 186	
> ```

## 🤖 Claude *(02:31:45)*


## 🤖 Claude *(02:31:45)*

Let me read the latest SEAL and Next Steps from the bottom of HANDOFF.md.

## 🤖 Claude *(02:31:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "tail -c 9000 /home/gcrux-tradeux/HANDOFF.md",
  "description": "Read newest SEAL records at bottom of HANDOFF.md"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> tasia de edge-impossível que nossa pesquisa refuta. Entregue (QA-PASS/TL-APPROVE Fase A e B+C; deployado+verificado): `cockpitJob`+`utils/cockpitService.js` (klines 1m MAINNET → distribuição de retornos, EV net-de-fee, tail, histograma, banda MC **driftless**, snapshot regime/flow/gates → `MEMORY['<sym>:COCKPIT']`, passivo `executeAutomations=false`); `GET /analysis/cockpit` (+env `useTestnet`/`tradingHalt`); tool MCP **read-only** `tradeux_get_cockpit`; **fix do BLOQUEADOR do prompt** (`agent.js` afirmava "conta é TESTNET/equity é ruído" em MAINNET → agora **env-aware** deferindo ao cockpit); frontend `/cockpit` (neon, consome o snapshot do brain, fallback klines). Verificado ao vivo: o agente chamou `tradeux_get_cockpit` e reportou coerente (mainnet real + halt). **A brain reporta EV/trade −0,16% / só 0,6% dos moves limpam a fee** — a própria máquina mostra que scalp 1m é −EV (o oposto honesto do golpe). Memória `tradeux-1m-scalping-and-cockpit`. Screenshots via Playwright headless (`/tmp/cockpit-shot.js`, login pelo `tradeux-mcp/.env`).
> 
> **(2) 🔧 Fix do −1013 no Trend (commit `2528a5d`, QA-PASS/TL-APPROVE).** orderTemplate **id3** (usado pela automação **id6 ATIVA** Trend Buy BTC) sofreu drift p/ `quantityMultiplier=1.00` → em `beholder.calcQty` o `Math.floor(qty/stepSize)*stepSize` empurrava o MIN_NOTIONAL **abaixo de $5** → quando um golden cross disparasse, a Binance rejeitaria **-1013** e a id6 NÃO compraria (repro: $4,65 BTC / $4,94 ETH / $4,80 BNB / $4,99 ADA). Fix 2 camadas: **backstop de piso** em `calcQty` (cirúrgico, **só MIN_NOTIONAL**, idempotente, NÃO toca posições TREND/HARVEST/FARM/MAX_WALLET — cobre farm/harvester de quebra) + template id3 → **×3** (~$15, intenção documentada do `setup-trend.js`). DB UPDATE aplicado ANTES do boot; BRAIN re-init com ×3 verificado via `/beholder/brain`. HALT intacto.
> 
> **(3) 🔍 Auditoria adversarial INDEPENDENTE de descongelamento (wf `wew1texdp`, 4 auditores + verif. anti-falso-positivo).** Segurança do diff do cockpit: **SEM_PROBLEMA_REAL** (read-only confirmado: writeTool 9→9, env só 2 booleanos, sem money-path). CONFIRMOU 7 achados que pesam contra descongelar AGORA: (1) **pré-reqs não resolvidos** (saque-OFF/IP **não confirmado**; trava **`FARM_SELLING` AUSENTE** — grep=0, nunca implementada); (2) **harvester morto** (id22-25 ainda ATIVAS); (3) **0 ordens mainnet** (descongelar = 1º trade real, fill/fee/slippage não validados); (4) **gap `MAX_ORDER_NOTIONAL`** (SELL MARKET por qty-base NÃO é capado — só o HALT); (5) **bug P&L com BNB** (net não desconta a taxa em BNB → painel mente otimista); (6) **sem cap diário/posição**; (7) **1m refutado** (−0,14% a −0,23%/trade no cache real). Também pegou 3 bugs do cockpit que eu subestimei → **CORRIGIDOS** no `1660871`: gate fluxo **fail-OPEN→fail-CLOSED** (mostrava GO sem fluxo fresco; id2 real bloqueia); gate como **DOUTRINA** (`doctrine=true` + disclaimer no MCP — a baseline id2 está `isActive=0`, não é estado vivo); `.toFixed(2)` colapsava a banda MC de alts (ADA 0,18/0,18/0,18) → **precisão dinâmica**.
> 
> **Estado vivo:** 4 containers up, **MAINNET CONGELADO** (`TRADING_HALT=true`), ~$150 USDT, 0 ordens mainnet. `.git` intacto (gcrux-tradeux). Memórias: `tradeux-1m-scalping-and-cockpit` (atualizada) + índice.
> **NEXT (descongelamento RESPONSÁVEL — recomendação FUNDAMENTADA NA AUDITORIA, não flip cego):** pré-reqs antes de QUALQUER ordem real: **(a)** dono confirma chave Binance **saque-OFF + IP travado**; **(b)** **desativar harvester** (id22-25 → isActive=0, morto+falling-knife); **(c)** **fix do P&L com BNB** (senão o painel mente); **(d)** **fechar o gap do teto** p/ SELL-by-base (ou restringir a LIMIT/OCO); **(e)** **cap diário de perda** OU size minúsculo + 1 trade. Aí canary: **só a Trend id6 ativa** (resto parado), ×3 (~$15), observar **1 ciclo golden→death real**, medir fill/fee/slippage; **persistir `TREND_QTY`** antes de escalar. **Claude NÃO vira o `TRADING_HALT`** — é GO do dono + (a)-(e). Ofereci fazer **(b)(c)(d) com QA/TL** como próximo passo. **PRs: 0** (trunk-based direct-to-master; commits já no origin, CI rodando).
> 
> ### 🤝 SEAL — 2026-06-16 (Coerência do Cockpit + anti-spam do agente — 7 commits, QA/TL em cada, HALT intacto)
> **Sessão dirigida pelas mensagens do agente no Telegram: o dono encaminhou observações, eu diagnostiquei cada uma e corrigi as REAIS. Vivo==master==origin==`0b1554d` (7 commits, trunk-based; CI rodando). 4 containers up, site 200, `TRADING_HALT=true` intocado o tempo todo, 0 ordens mainnet.**
> 
> **O gatilho:** o agente vinha flagando "divergências" cockpit×oráculo no Telegram. Investigação (wf `wf_8cc8b47b-22c`, 6 agentes + verif. adversarial `synthesis-holds`) provou que o cockpit **lê as MESMAS chaves** `MEMORY['REGIME']/['FLOW']` dos oráculos vivos — não é fonte paralela. A maioria era ESPERADA (histerese, idade de snapshot); algumas eram bugs REAIS de VIEW/honestidade. Corrigi em camadas:
> 
> 1. **`6042bd9` fix(cockpit): freshen no read-path + anti-spam (prompt).** O cockpit congelava flow/regime no tick de 60s; o agente comparava o número velho com o vivo e chamava de "contradição". `cockpitJob.freshen()` recomputa regime/flow/gates da MEMORY no instante da LEITURA (analítica 1m segue em cache) + expõe `flow.ageMs`/`ageSec`. `getRegime` anexa `data.gate` (regime HISTERÉTICO operativo) sem mudar `data.regime` (instantâneo, card UI). QA-PASS+TL-APPROVE.
> 2. **`64752f0` feat(agent): dedup de notificação POR ASSUNTO em código.** Defesa em profundidade independente do prompt (`tradeux-agent/src/notifyDedup.js`, puro/testável): normaliza+canoniza sinônimos PT/EN, chave de tópico = vocabulário de domínio ∪ tickers ∪ transições direcionais, **Jaccard ≥ 0.6**; guards anti-falso-positivo (símbolo distinto / transição inversa / marcador de evento inédito). Roda ANTES do cap 2/ciclo (suprimido não consome o cap). **Self-test com mensagens REAIS do Telegram (15 casos) wired no CI.** Red-team pegou B6 CRÍTICO (ticker por sufixo p/ alts novas) → corrigido. QA-PASS+TL-APPROVE.
> 3. **`bf254a0` fix(cockpit): reason reflete o regime real** — mostrava "range + fluxo ok" com regime `mixed` (auto-contradição); agora interpola o regime. Decisão do gate intocada (mixed é mean-reversion = correto). QA-PASS+TL-APPROVE.
> 4. **`37ed4b1` refactor(agent): consolida doutrina anti-ruído num bloco `DIVERGÊNCIAS ESPERADAS`** — 3 regras anti-ruído repetidas → 1 bloco rotulado (6→7 itens) + ponteiros. Zero regra perdida. QA-PASS+TL-APPROVE.
> 5. **`8884bd3` fix(cockpit): gate de acumulação SYMBOL-AWARE (BUG REAL).** `deriveGates` aplicava o filtro de fluxo da baseline BTC a TODOS os símbolos; mas só a id2 (BTC) é flow-gated (`setup-flow-gate.js`), o FARM das alts gateia só RSI+regime (`setup-farm.js:131`). Mostrava alt em capitulação como `buyAllowed=false "baseline veta"`, vetando entrada que a farm VIVA faria. Fix: `deriveGates(regime,flow,symbol)` + `FLOW_GATED` (env, default BTCUSDT) → `buyAllowed = flowGated ? baseline : farm`. QA-PASS (truth-table 24 células)+TL-APPROVE.
> 6. **`2c8655c` fix(cockpit-ui): painel "Trade bridges" consome o gate symbol-aware** — o frontend tinha o MESMO hardcode (`imbalance>-0.4` p/ toda alt); agora consome `cp.symbols[s].gates` (alts: fluxo informativo `.info`/"fluxo·i", não bloqueia). Frontend-only. QA-PASS+TL-APPROVE.
> 7. **`0b1554d` docs(agent): doutrina GATE ≠ TRIGGER (item 7 do bloco).** O agente flagou `farm=true` com RSI 79/66/62 (>35) como incoerência. NÃO é bug: o gate é DOUTRINA de regime/fluxo (`doctrine:true`), NÃO lê RSI; o FARM dispara só no dip RSI<35. Fix agent-side (não cockpit). QA-PASS+TL-APPROVE.
> 
> **Aprendizados duráveis (na memória `tradeux-1m-scalping-and-cockpit`):** (a) o **dedup ESTÁ funcionando** — as ~8 notificações eram TÓPICOS DISTINTOS ao longo de ~10h, não repetição (rodei pelo módulo p/ provar); journal persistido em volume. (b) **VERDICT do TL: a fase de ENUMERAÇÃO REATIVA de coerência do cockpit está DONE** — os 2 sub-eixos de "gate aberto mas X não atendido" cobertos (fluxo `8884bd3` = bug real; RSI/trigger `0b1554d` = leitura). Próximo eixo plausível = notional/saldo; NÃO pré-emptar — o catch-all do prompt ("só sinalize se a fonte VIVA por si só mostrar anomalia") já segura; se aparecer é +1 item incremental.
> 
> **Tech debt / follow-ups (chips abertos, fora do escopo):** (1) notify-dedup por assunto em código foi FEITO (`64752f0`); (2) painel "Trade bridges" FEITO (`2c8655c`); **(3) baseline id2 (RSI<25) é runtime/PATCH, NÃO seedada** (QA flagou — pós-`make nuke` reaplicar manual; dívida já conhecida em `tradeux-regime-gate`). **Descongelamento:** pré-reqs (a)-(e) do SEAL anterior SEGUEM PENDENTES (saque-OFF/IP, desativar harvester, fix P&L BNB, gap teto SELL-by-base, cap diário). **PRs: 0** (trunk-based; tudo já no origin).
> ```

## 🤖 Claude *(02:31:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && git -c safe.directory='*' branch --show-current 2>/dev/null; echo \"---PRs via gh---\"; gh pr list --state open 2>/dev/null || echo \"gh indispon\u00edvel (sem token/cli)\"",
  "description": "Current branch and open PRs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> master
> ---PRs via gh---
> gh indisponível (sem token/cli)
> ```

## 🤖 Claude *(02:31:50)*


## 🤖 Claude *(02:32:04)*

═══════════════════════════════════════════════════
  HANDSON — GO-LIVE MAINNET · CONGELADO (seal 2026-06-16)
═══════════════════════════════════════════════════
🏁 ESTADO     : MAINNET REAL **CONGELADO** (`TRADING_HALT=true`), ~$150 USDT, **0 ordens mainnet**. Fase reativa de coerência do Cockpit ENCERRADA (verdict do TL).
🧾 COMMITS    : `0b1554d` docs: doutrina GATE≠TRIGGER · `2c8655c` fix(cockpit-ui): bridges symbol-aware · `8884bd3` fix(cockpit): gate de acumulação symbol-aware
🐳 STACK      : db healthy · backend/frontend/agent up (4h) · site **200**
📈 BASELINE   : 15 automações Farm-and-Funnel (mas **nada negocia** — HALT global no `exchange.js`) · agent supervisionado no ar · harvester id22-25 ainda ATIVAS (mortas no mainnet)
🔀 PRs ABERTOS: **0** (trunk-based direct-to-master; tudo já no origin, CI rodando) — `gh` indisponível, sem lembrete de merge
📂 PENDENTE   : **worktree limpo** (master == origin == `0b1554d`)
⚡ PRÓXIMO    : descongelamento RESPONSÁVEL — pré-reqs **(a)–(e)** ainda PENDENTES: (a) dono confirma chave Binance saque-OFF + IP travado · (b) desativar harvester (id22-25→isActive=0) · (c) fix P&L com BNB · (d) fechar gap do teto SELL-by-base · (e) cap diário de perda. Ofereci fazer (b)(c)(d) com QA/TL.
⚠️ ALERTAS    : 🛑 **Claude NÃO vira o `TRADING_HALT`** — é GO do dono + (a)-(e) · harvester é falling-knife no mainnet (edge era arbitragem testnet) · baseline id2 é runtime/PATCH não-seedada (reaplicar pós-`make nuke`) · golpe "Fable 5/Polymarket 205x" = referral scam, NÃO engajar
═══════════════════════════════════════════════════
  Pronto pra trabalhar. Aguardando direção.
═══════════════════════════════════════════════════

Contexto carregado. Stack saudável, worktree limpo, **HALT intacto** — nada negociou desde o último seal.

O caminho natural daqui é o **descongelamento responsável**: posso atacar os pré-reqs de código **(b) desativar harvester**, **(c) fix P&L com BNB** e **(d) gap do teto SELL-by-base** com QA/TL, já que (a) e (e) dependem de decisão tua. Quer que eu comece por algum desses, ou tens outra direção?

## 👤 User *(02:40:16)*

Binance saque-OFF + IP travado como posso dazer isso?

## 🤖 Claude *(02:40:29)*


## 🤖 Claude *(02:40:32)*

Boa — esse é o pré-req (a), e é coisa que **só tu fazes** no site da Binance (eu não toco em chave nem em saque). Te guio. Antes, deixa eu descobrir **qual IP** tu precisas liberar — é o IP de saída que a Binance enxerga quando o backend chama a API, não o IP do teu notebook.

## 🤖 Claude *(02:40:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"== IP de sa\u00edda do HOST ==\"; curl -s -m8 https://api.ipify.org; echo; echo \"== IP de sa\u00edda de DENTRO do container backend (o que a Binance realmente v\u00ea) ==\"; sudo -n -u gcrux-tradeux bash -lc 'cd /home/gcrux-tradeux/tradeux && docker compose exec -T backend sh -lc \"command -v curl >/dev/null 2>&1 && curl -s -m8 https://api.ipify.org || (command -v wget >/dev/null 2>&1 && wget -qO- -T8 https://api.ipify.org)\"' 2>/dev/null; echo",
  "description": "Descobrir IP de sa\u00edda do host e do container backend"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> == IP de saída do HOST ==
> 137.131.243.179
> == IP de saída de DENTRO do container backend (o que a Binance realmente vê) ==
> 137.131.243.179
> ```

## 🤖 Claude *(02:40:42)*


## 🤖 Claude *(02:40:58)*

O IP de saída — tanto do host quanto de dentro do container backend — é o mesmo:

## 🔑 IP a liberar na Binance
```
137.131.243.179
```
É esse que a Binance vê quando o backend chama a API. (⚠️ é uma instância **Oracle Cloud** — confirma no painel da Oracle que esse IP público é **reservado/estático**, não efêmero; se for efêmero ele muda num reboot e a chave para de funcionar.)

---

## Passo a passo no site da Binance

**1. Abrir o gerenciador de chaves**
Login → ícone do perfil → **Account** → **API Management** (ou direto em `binance.com/en/my/settings/api-management`). Acha a chave que o TradeUX usa.

**2. Editar a chave** → botão **Edit restrictions**.

**3. Saque-OFF (permissões) — o crítico**
Deixa marcado **só** o que o bot precisa pra spot:
- ✅ **Enable Reading**
- ✅ **Enable Spot & Margin Trading**
- ❌ **Enable Withdrawals** → **DESMARCADO** (essa é a trava "saque-OFF"; nem aparece sem 2FA, e a gente nunca liga)
- ❌ Enable Futures / Margin / Internal Transfer / Universal Transfer → todos **off**

**4. IP travado (restrição de IP)**
Na seção **IP access restrictions**, escolhe:
- **Restrict access to trusted IPs only** (NÃO "Unrestricted")
- Cola `137.131.243.179` na caixa → **Confirm**

**5. Salvar** — vai pedir 2FA (Google Auth / e-mail / SMS).

---

## Por que isso importa (além do óbvio)
- **Saque-OFF** = mesmo que a chave vaze, ninguém saca teus fundos; o pior caso vira "alguém faz trades ruins", não "alguém esvazia a conta".
- **IP travado** = a chave só funciona a partir de `137.131.243.179`. Some o risco de uso remoto **e** a Binance deixa de expirar a chave (chaves sem IP restrito **expiram sozinhas em 90 dias** — isso derrubaria o bot do nada).

---

## Depois de salvar — me avisa que eu valido
Eu **não** mexo na chave, mas posso confirmar do lado de cá que ela ainda autentica e lê a carteira com o novo IP travado (sem destravar nada — o `TRADING_HALT` continua de pé). Algo como um `get_wallet` read-only pelo backend. Quando salvares, me diz e eu rodo a verificação.

Quer que eu já confirme no painel da **Oracle Cloud** se esse IP é reservado antes de tu travar? (evita o pé-na-jaca de travar num IP efêmero)

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-16 - agent-afe8189a8d120151e]]
> * **Próxima Sessão**: [[2026-06-17 - Implement OAuth 2.1 browser-flow and vision-mcp roadmap tasks]]
%% --- TIMELINE END --- %%

# Implement shake-hands endpoint
**Date:** 2026-06-19 | **Session ID:** `2b2f6508-34d7-4007-b556-91b1cc19927e`

---

## 👤 User *(03:13:43)*

<command-message>shake-hands</command-message>
<command-name>/shake-hands</command-name>

## 👤 User *(03:13:43)*

Base directory for this skill: /home/gcrux-tradeux/.claude/skills/shake-hands

# ShakeHands — TradeUX Continuity Protocol

Two symmetric commands — `handson` (enter) and `handoff` (exit) — that make every
session stateless from the agent's perspective: all durable state lives in
`HANDOFF.md` + the memory files.

## Context anchors (TradeUX)
- **App / repo:** `/home/gcrux-tradeux/tradeux` — Docker stack `db + backend + frontend`,
  published on `127.0.0.1:8090`, fronted by CloudPanel nginx (TLS) → Cloudflare →
  `tradeux.gcrux.com`.
- **Source of truth:** `/home/gcrux-tradeux/HANDOFF.md` (what `/handson` reads first).
- **Memory:** `/home/ubuntu/.claude/projects/-home-gcrux-tradeux/memory/`.
- **Identity:** the shell runs as `ubuntu`; act as the site user with `sudo -n -u gcrux-tradeux`.
- **Git push:** the repo is `gcrux-tradeux`-owned, but only `ubuntu`'s SSH key reaches
  GitHub. Push as root with that key, then chown back (see `/handoff` Phase 5).
- **NOT applicable here** (constellation-orchestra only): Supabase Knowledge Mesh,
  BoK gates, Chroma, TypeScript/edge-functions, mcorch/mega-brain containers.

## /handson — enter (load context in <10s, don't re-discover)
1. `cat /home/gcrux-tradeux/HANDOFF.md`
2. `git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' log --oneline -7`
3. `git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' status --short`
4. `sudo -n -u gcrux-tradeux bash -lc 'cd /home/gcrux-tradeux/tradeux && docker compose ps'`
5. site check: `curl -s -m5 -o /dev/null -w "%{http_code}" https://tradeux.gcrux.com/`
6. Read repo `CLAUDE.md` + memory `MEMORY.md`.
Then emit the HANDSON brief (pt-BR). Trust HANDOFF.md — do not walk the file tree.
Surface dirty files + open PRs; do NOT auto-restart containers or auto-commit.

## /handoff — seal (commit → HANDOFF.md → memory → push; zero orphaned state)
1. **Audit:** `git status --short` + `git diff HEAD --stat` (in the repo).
2. **Secret scan (BLOCKS the seal):** grep the diff for `sk-…`, `eyJ…`, `SECRET_KEY`,
   `ACCESS_KEY`, Binance/OpenRouter keys. `.env` must stay gitignored — keys NEVER committed.
3. **Commit by layer**, each group separately (branch + PR):
   | Layer | Pattern | Prefix |
   |---|---|---|
   | Backend (Beholder core — careful) | `backend/**` | `feat(backend):` / `fix(backend):` |
   | Frontend | `frontend/**` | `feat(frontend):` / `fix(frontend):` |
   | Agent / MCP | `tradeux-agent/**`, `tradeux-mcp/**` | `feat(agent):` |
   | Deploy | `docker-compose*.yml`, `setup.sh`, `Makefile` | `chore(deploy):` |
   | Docs | `*.md` | `docs:` |
   Append `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
4. **Update `HANDOFF.md`:** task table ✅/pending, Next Steps, new tech debt, open PRs,
   append a dated Session Record.
5. **Update memory files** under `/home/ubuntu/.claude/projects/-home-gcrux-tradeux/memory/`
   (+ `MEMORY.md` index).
6. **Push (mandatory final act):**
   `sudo env GIT_SSH_COMMAND='ssh -i /home/ubuntu/.ssh/id_ed25519' git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' push -u origin <branch>`
   then `sudo chown -R gcrux-tradeux:gcrux-tradeux /home/gcrux-tradeux/tradeux`.
   Open the PR via the printed `pull/new/<branch>` URL (no `gh`/token on this box).
Emit the HANDOFF seal box. The seal is complete only when `origin` reflects the work.

## Error handling
- `git: nothing to commit` → skip commit, still update HANDOFF.md + memory.
- push auth fails → confirm you used ubuntu's key as root (`github-ssh-key-on-ubuntu` memory).
- secret found in diff → STOP, scrub it, do not push.


## 🤖 Claude *(03:13:56)*


## 🤖 Claude *(03:13:56)*

I'll run the ShakeHands `/handson` entry protocol to load the session state.

## 🤖 Claude *(03:13:57)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/HANDOFF.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>[Truncated: PARTIAL view — showing lines 1-266 of 767 total (61145 tokens, cap 25000). Call Read with offset=267 limit=266 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>
> 
> 1	# TradeUX — HANDOFF (single source of truth)
> 2	
> 3	> ShakeHands continuity doc. `/handson` reads this FIRST. Newest record at the bottom.
> 4	> Project: **TradeUX** — Beholder-based multi-coin Binance Spot bot + LLM agent (**mainnet/testnet dual-env**).
> 5	> Updated: **2026-06-18** · Phase: **GO-LIVE MAINNET — CONGELADO (`TRADING_HALT=true`) · 🎯 TODOS pré-reqs de CÓDIGO (a)-(e) FEITOS → falta só GO do dono pro flip + canary de um-grupo-só** · Meta: **realista ≈ flat com ~$150** (o +3 BTC era do testnet) · Vivo==master==origin==**`854bab5`**
> 6	
> 7	> 🛑 **LEIA ANTES DE TUDO (2026-06-15):** o sistema está em **MAINNET REAL** (`settings.useTestnet=0`, ~$150 USDT) e **CONGELADO** (`TRADING_HALT=true` no `.env` → nada negocia; é o kill-switch novo no `exchange.js`). Money-path foi blindado (`96915e0`) e o bug P0 do Farm Sell foi corrigido (`c163112`). **DESCOBERTA CRÍTICA: o harvester está MORTO no mainnet** (o edge de −3% era arbitragem testnet-vs-mainnet; no mainnet o book do bot É o FAIR). O ÚNICO edge real é o **Trend** (pequeno, mensal). **Antes de descongelar:** (1) trava `FARM_SELLING` (follow-up); (2) dono confere saque-OFF+IP da chave Binance; (3) decidir re-design do harvester. Detalhes nos SEALs de 2026-06-15 (fim do doc) + memória `tradeux-mainnet-go-live`. **2026-06-16:** Cockpit Intelligence read-only NO AR (brain computa analytics 1m + agente lê/reporta; commit `1660871`) — a brain reporta **EV −0,16% / pHit 0,6%** (scalp 1m é −EV, dado real). Fix do **−1013** no `calcQty` + template Trend ×3 (commit `2528a5d`). **Auditoria adversarial independente** confirmou 7 achados p/ o descongelamento → ver SEAL 2026-06-16. ⚠️ O "vídeo viral Fable 5/Polymarket 205x" do X é **golpe de referral** — NÃO clicar/depositar.
> 8	
> 9	## ⚡ FIRST ACTION FOR NEXT AGENT
> 10	0. 🏗️ **ARQUITETURA FARM-AND-FUNNEL COMPLETA E NO AR** (sessão 2026-06-08): **15 automações ativas** — Farm no-loss +
> 11	   Trend SMA50/200 nas alts **LTC/BNB/ADA** (id 9-20) + id2/id6/id7 do BTC; **funil em SHADOW**; id3 pausada. Coordenação
> 12	   por regime (farm `!=trend`, trend `!=bear`). Validada por backtest (`backend/scripts/backtest-farm-funnel.js`) **e ao
> 13	   vivo**. Doc: `docs/STRATEGY-farm-funnel.md`. Memória `tradeux-farm-funnel-backtest`. **Hoje MERCADO=BEAR → tudo INERTE/protegido.**
> 14	   ⏰ **GATILHO (pedido do dono): QUANDO O REGIME SAIR DO BEAR / mercado propício → RETOMAR:** Fase 4 = **funil AO VIVO**
> 15	   (ligar a compra de BTC com o lucro real do farm, DEPOIS de observar o farm lucrar e calibrar o baseline com dado real);
> 16	   Fase 5 = **calibração** (5m + seleção de alts, SOL ruim no farm + switch macro fino — SMA-slope no regimeJob). Ver §5 do
> 17	   doc. **Checar o regime no boot:** `GET /analysis/regime-status` ou `logs/regime.log` — se != bear, é a hora.
> 18	   ✅ **ARMADOR DA FASE 4 NO AR** (commit `af22e7a`, 2026-06-09): o farm/trend já retomam sozinhos na saída do bear (gate
> 19	   runtime). O `regimeJob` agora detecta a borda `bear→não-bear` do macro (`FASE4_MACRO_SYMBOL`=BTCUSDT) → dispara
> 20	   `funnelJob.armFase4Observation()` = **notifica (telegram) + pré-arma o funil shadow (baseline) + janela densa de 4h**
> 21	   capturando o dado pra ESCREVER a Fase 4 (caixa USDT, reserva, lucro-desde-saída, escoamento; tag `[fase4-observe]` em
> 22	   `logs/funnel.log`). **NÃO compra** — a Fase 4 live-buy ainda não existe (money-path, gate). Quando o telegram avisar
> 23	   "🔔 [FASE4] Saída do BEAR", as 4h de captura bastam pra calibrar+escrever a compra ao vivo (com gate QA/TL). Memória `tradeux-farm-funnel-backtest`.
> 24	   ✅ **TELEGRAM FUNCIONA DE VERDADE desde 2026-06-10** (a raiz era chatId=username do bot → fix; `c3463ac` notifica TODAS
> 25	   as ordens + canal do agente `tradeux_notify_owner`) — o aviso "[FASE4]" CHEGA no dono. E o **HARVESTER está em size ×4**
> 26	   (`0b94b3a` reconcile-on-boot fechou a última dívida; janela de observação 2-3 dias → ×8). Memória `tradeux-telegram-notifications` + `tradeux-harvester-experiment`.
> 27	   ✅ **AGENTE RECALIBRADO (`12ceabe`)** pós-incidente de spam: doutrina POR MÓDULO (harvester=no-loss; **id7 corta perda
> 28	   POR DESENHO** — não tratar como bug), pt-BR obrigatório, kickoff injeta histórico de notificações (anti-repetição) +
> 29	   cap mecânico 2/ciclo. NÃO reescrever a doutrina sem reler `tradeux-telegram-notifications` (a regra "só vende com lucro"
> 30	   é literal SÓ pro harvester; gate de lucro na id7 = mudança de estratégia REFUTADA pelo backtest — não fazer via prompt).
> 31	1. **Backlog de PRs ZERADO** — modelo **trunk-based** (commit direto no `master` + push via token HTTPS).
> 32	2. 🎯 **META MUDOU: de 500k para +3 BTC (testnet)** — validar uma estratégia que faz +3 BTC; se 3, calibrar p/ 10+.
> 33	   Ver memória `tradeux-agent-500k-validation` (pivot) e `~/STRATEGY-3BTC-assessment.md`.
> 34	3. ✅ **OCO wiring no Beholder COMMITADO E NO AR** (commit `aa3f7f7`): template `type:'OCO'` → SELL protetiva
> 35	   (TP LIMIT_MAKER + SL STOP_LOSS_LIMIT), persiste 2 pernas c/ `orderListId` (migration), `listStatus` reconcile,
> 36	   guard anti-empilhamento, cancel no delete da automação. Gate QA+TL + testnet + CI verde.
> 37	4. ✅ **P&L mensurável + painel** (`d74fac0` net/avgPrice no insert de fills — ~74% das MARKET tinham net NULL;
> 38	   `9a5f989` Reports default USDT + end-date inclusivo + **leitura em BTC** "≈ X BTC"; `1fa6235` **painel
> 39	   Intelligence**: regime de mercado + KPIs do agente no UI). Todos com CI verde + validados no navegador.
> 40	5. ✅ **ENABLER Nº1 ENTREGUE & NO AR** (commit `30e6566`): `regimeJob` grava `MEMORY['<sym>:REGIME']`
> 41	   (string, via `updateMemory(...,executeAutomations=false)` = gate passivo) a cada 5min; `regimeService`
> 42	   compartilha fetch+classify+cache com o endpoint. **id2 (BUY) GATEADA ao vivo** (PATCH): condition
> 43	   `... && MEMORY['BTCUSDT:REGIME']!=='bear'` + `BTCUSDT:REGIME` nos indexes (fail-safe). id3 (SELL) intocada.
> 44	   Hoje BTC=bear → id2 **não compra** (validado). Gate QA+TL + testnet + lógica 9/9. ⚠️ ver "id2 gate" em
> 45	   Technical debt (NÃO é seedado → reaplicar após `make nuke`/reset).
> 46	6. ✅ **Classificador c/ histerese ENTREGUE** (commit `774ae42`): bandas entra/sai (bear >0.60/sai <0.45;
> 47	   trend 25/22; range 20/23), `prev` carregado pelo job. Gate da id2 mais estável e fail-safe (bear pegajoso).
> 48	   ±DI descartado por dados (piorava); MTF desnecessário (histerese já vence). Ganho é risco-ajustado de
> 49	   CARTEIRA, não alfa no BTC (ver task table). Observabilidade do gate ✅ (commit `e6c10dc`, card "Regime Gate" no
> 50	   painel). Calibração RSI ✅ (commit `0b1e949`): **RSI 25/75 aplicado na id2/id3** (domina 30/70 em retorno+drawdown
> 51	   em 1h E 1m). ✅ **Trend Following (SMA 50/200) ATIVADO** (commit `453c7d6`, gate QA PASS + TL APPROVE, CI verde):
> 52	   id6/id7 ativas + coordenação id2/id3 `!=trend` + **LIMIT marketável** (buffer 0.3%) + **persistência de cross** (`regimeStates`).
> 53	   ⏳ **NEXT**: (a) **observar 1 golden→death real** (`logs/A:6.log`/`A:7.log`) antes de calibrar o size (id6=3× MIN_NOTIONAL);
> 54	   (b) observar id2/id3 coordenadas ao longo do tempo; (c) ✅ **risco nº1 RESOLVIDO** (commit `e5ef595`: id7 usa `TREND_QTY`,
> 55	   não mais `LAST_ORDER`) — ⚠️ porém `TREND_QTY` é **volátil** (não persiste) → **persistir ANTES de escalar o size**;
> 56	   (d) opcional: hook de SIGTERM p/ stop().
> 57	7. Sanity no `/handson`: stack up na 8090 (**4 containers: db/backend/frontend/agent**), id2/id3 (coordenadas `!=trend`) + id6/id7 (trend) **ATIVAS**, símbolos
> 58	   synced, `GET /beholder/memory/BTCUSDT/REGIME` => `"bear"`. Trend ATIVO mas **inerte** agora (bear + above=false → sem disparo).
> 59	
> 60	## 🏁 Current state (what's live)
> 61	- **Stack DEPLOYED & healthy**: `tradeux-db/backend/frontend/agent` na 8090 (CloudPanel+Cloudflare).
> 62	  `https://tradeux.gcrux.com` → 200. Backend recriado com deps novas (twilio6/form-data4), boot limpo.
> 63	- **Agente LLM SUPERVISIONADO** (commit `e97a85a`): roda como serviço `agent` no compose (restart:unless-stopped,
> 64	  `user:1011:1013`, DRY/ALLOW_TRADING=false, OpenRouter nemotron `:free`); grava o journal que alimenta os KPIs do card
> 65	  "Agent (LLM)" em `/intelligence`. Antes era CLI manual → parava sem religar (ficou 5 dias parado). Religar/parar:
> 66	  `docker compose up -d agent` / `docker compose stop agent`.
> 67	- **Modelo de trabalho SELADO** (ver memória `tradeux-orchestration-model`): Claude é o ORQUESTRADOR —
> 68	  agentes worker implementam, QA+Tech-Lead são o gate; Claude **aprova OU devolve** e sobe pra prod.
> 69	  Sem PR-por-mudança. Gate proporcional: trivial→direto; hot-path/migration/segredo/dinheiro→gate.
> 70	- **Token GitHub**: em `~/tradeux/.env` como `GITHUB_TOKEN_API` (gitignored). Merge/push via API/HTTPS.
> 71	  ⚠️ é um PAT clássico admin-scope — trocar por fine-grained quando der (hardening).
> 72	- **PRs**: #10 (fix white-screen) e #11 (auto-sync) **MERGEADOS**; #1-7 (dependabot frontend)
> 73	  **fechados** (obsoletos pós-Vite); #9 (BYOK) **superseded** por commit direto; #12-15 (auto-PRs
> 74	  do Dependabot) **fechados como deferidos** (#12/#14 bundlam node-binance-api core → task; #13/#15
> 75	  vite/esbuild dev-only). **0 PRs abertos** — mas o Dependabot REABRE auto-PRs pras 6 moderate
> 76	  deferidas; fechar-como-deferido até o bump do node-binance-api / vite resolver na raiz.
> 77	- **Segurança**: backend runtime **8 → 2 moderate** (0 crit/0 high) após node-binance-api 1.x + `@sendgrid` 6→8
> 78	  (mata o `request`) + remoção do override form-data (commit 063df19). Restam 2 NÃO-exploráveis (`sequelize→uuid@8.3.2`,
> 79	  path `buf` não usado). O Dependabot pode mostrar mais (soma as 2 árvores incl. dev). Ver SECURITY.md.
> 80	- **BYOK**: chaves Binance opcionais no boot (seeder `|| ''` + setup.sh) — commit `9b91416`.
> 81	- **Backtest + regime**: harness walk-forward (`backend/scripts/backtest.js`) + detector
> 82	  (`backend/src/utils/regimeClassifier.js`) + relatórios (`backend/backtest-results/`). Ver Validation.
> 83	- **Baseline**: RSI 30/70 (BTCUSDT) — automations `id2`(buy<30)/`id3`(sell>70) **ACTIVE/armadas**.
> 84	- **Regime gate AO VIVO** (commit `30e6566`): `regimeJob` grava `MEMORY['BTCUSDT:REGIME']` (mainnet 1h, 5min);
> 85	  **id2 (BUY) gateada** `... && MEMORY['BTCUSDT:REGIME']!=='bear'` + `BTCUSDT:REGIME` nos indexes (fail-safe);
> 86	  id3 (SELL) sem gate (saída p/ caixa sempre liberada). Hoje BTC=**bear** → id2 não compra.
> 87	- **LLM agent**: `tradeux-agent`+`tradeux-mcp`, OpenRouter `nemotron-3-super-120b:free`, `ALLOW_TRADING=false`.
> 88	
> 89	## 📋 Task state
> 90	| Item | Status |
> 91	|---|---|
> 92	| Deploy stack / 502 / white-screen / auto-sync symbols | ✅ (mergeados #10/#11) |
> 93	| BYOK chaves opcionais no boot | ✅ (commit direto) |
> 94	| Segurança: critical + 8 high (twilio/form-data) | ✅ (28→6; gate QA+TL) |
> 95	| Backtest robusto walk-forward (1y, 4 símbolos, fee) | ✅ |
> 96	| Detector de regime: módulo + endpoint `/analysis/regime` + MCP `tradeux_get_regime` (Fase 1) | ✅ live (read-only, commit 0a97820) |
> 97	| Modelo de orquestração trunk-based selado | ✅ (memória) |
> 98	| `node-binance-api` 0.13→1.x (mata request via lib+@sendgrid; backend 8→2; OCO no wrapper) | ✅ (commit 063df19; gate+testnet) |
> 99	| OCO wiring no Beholder (template `type:'OCO'`, 2 pernas+`orderListId`, listStatus, anti-stacking) | ✅ (commit `aa3f7f7`; gate+testnet+CI) |
> 100	| P&L: net/avgPrice no insert de fills (~74% das MARKET tinham NULL → P&L furado) | ✅ (commit `d74fac0`; gate+testnet) |
> 101	| Reports: default USDT + end-date inclusivo + **leitura em BTC** (≈ X BTC) | ✅ (commit `9a5f989`; validado browser) |
> 102	| **Painel Intelligence** (regime de mercado + KPIs do agente no UI) — Fase B do dashboard | ✅ (commit `1fa6235`; validado browser) |
> 103	| Trava OCO=SELL no template + UX (E2E fixes) | ✅ (commit `d74fac0`) |
> 104	| **ENABLER Nº1**: regime→`MEMORY['<sym>:REGIME']` (job periódico) + **id2 (BUY) gateada** (`!= bear`) | ✅ (commit `30e6566`; gate QA+TL+testnet+CI; id2 via PATCH runtime) |
> 105	| Classificador de regime c/ **histerese** (anti-whipsaw) | ✅ (commit `774ae42`; gate QA+TL+backtest+testnet+CI). Bear pegajoso (sai só <0.45) = gate fail-safe. ±DI testado e DESCARTADO; MTF desnecessário. Ganho é de CARTEIRA (bear 26→6 flips, -32%→+0.6% agregado), **não alfa no BTC** (no BTC isolado V2 empata/atrasa). |
> 106	| **Calibração RSI/SMA** (backtest, retorno+maxDD agregado) | ✅ (`backtest.js` `--calibrate`, commit `0b1e949`; fix `MS_PER` 1m). **RSI 25/75 aplicado na id2/id3** (runtime/PATCH): domina 30/70 em retorno **E** drawdown em 1h E 1m (1m: 30/70 overtrada ~80 trades, fee corrói; 25/75 ~15-19). **SMA200 mantido** (melhor retorno). SMA-cross 50/200 = roadmap de trend. |
> 107	| **Trend Following (SMA 50/200)** — pipeline + ATIVAÇÃO | ✅ pipeline (commit `49af86a`) + ✅ **ATIVADO** (commit `453c7d6`; gate QA PASS + TL APPROVE; CI verde). Sinal da **MAINNET** (`regimeJob` detecta o cross → `MEMORY['<sym>:TREND_CROSS_1h']`, dispara 1x). **id6/id7 ATIVAS** + coordenação id2/id3 `!=trend` (REGIME nos indexes de ambas, fail-open corrigido) + templates 3/4 **LIMIT marketável** (buffer 0.3% no eval) + **persistência de cross** (`regimeStates`, resiliência a restart) + `validatePrice` no PATCH. Reprodutível: `setup-trend.js`+`activate-trend.js`. ⏳ Observar 1 cross real → calibrar size. |
> 108	
> 109	## 🎯 Validation plan → +3 BTC (testnet) — META NOVA (era 500k)
> 110	- **+3 BTC** = validar uma estratégia que cresce a carteira em 3 BTC (testnet); se valida 3, calibrar p/ 10+.
> 111	  No testnet (preços sintéticos) é **marco de mecânica/disciplina**, não alfa de mercado real.
> 112	- **Verdade dura do backtest (BTCUSDT 1h, net fee, bear 365d + bull 180d):** +3 BTC de **alfa absoluto** com
> 113	  long-only spot **NÃO sai de "trade esperto"** — bull→segurar ganha (B&H +134% vs regime +20%); bear→tudo perde
> 114	  mas o **caixa corta a perda** (regime −8% vs B&H −40%). Edge real = **drawdown menor via regime-gating**, não alfa.
> 115	  Calibração validada: RSI **25/75** (não 30/70), SMA **50/200** (não 20/50), menos trades. HFT é morto (fee+whipsaw).
> 116	  Rota p/ muitos BTC = **comprado no bull/trend, CAIXA no bear** + classificador bom + size pequeno + OCO. Doc:
> 117	  `~/STRATEGY-3BTC-assessment.md`. Painel `/intelligence` mostra o regime ao vivo (hoje BTC=bear/cash).
> 118	- (histórico 500k) = stress/validação, NÃO lucro (testnet fills sintético; reset ~mensal — persistir métricas).
> 119	- **Backtest de ciclo completo** (1h real, fee 0.1%/lado, walk-forward OOS, BTC/ETH/BNB/SOL):
> 120	  - **Bear (365d)**: B&H médio **-24%**; long-only não escapa; o edge é o **estado de CAIXA** (no BTC,
> 121	    regime-switch -7% vs B&H -27%). Regime-switch bate B&H em 1/4.
> 122	  - **Bull (2023-10→2024-04)**: B&H **+294%** ESMAGA tudo (regime +39%, trend +147%); bate B&H em 0/4.
> 123	  - **Lição honesta**: Buy&Hold é dificílimo de bater em retorno BRUTO; o valor do trading ativo é
> 124	    **risco-ajustado** (drawdown), não outperformance. HFT é matematicamente morto (fee+whipsaw).
> 125	- **Próximo edge**: classificador com **histerese** que FICA no bull e SAI no bear (ciclo completo,
> 126	  risco-ajustado) — é o trabalho do agente. Rodar `backtest.js` em mais janelas/símbolos.
> 127	
> 128	## 🧱 Technical debt / gotchas
> 129	- **GIT como gcrux-tradeux SEMPRE** (memória `git-ownership-gotcha`): git como `ubuntu` (mesmo read-only)
> 130	  cria arquivos `ubuntu` em `.git` e depois `gcrux-tradeux` não escreve `.git/objects` → commit falha.
> 131	  Fix: `sudo -n chown -R gcrux-tradeux:gcrux-tradeux .../.git`. Rodar git/docker-que-escreve-repo como gcrux.
> 132	- ✅ **`node-binance-api` 0.13→1.x feito** (063df19): é o **fork ccxt** (reescrita). Gotchas mapeados em
> 133	  `exchange.js`: `test:true` roteia o **ws-api de testnet** p/ o userData (senão autentica no mainnet); ordens
> 134	  via `binance.order(type,side,...)` (buy/sell 1.x quebram STOP via flags); `ohlc()`→`populateOHLC()`;
> 135	  `terminate()` por **URL completa** (1.x indexa subscriptions por url). **Quem matou o `request` foi o
> 136	  `@sendgrid` 6→8**, não só o node-binance (o sendgrid velho sustentava request por conta própria).
> 137	- **Regime classifier**: cru (ADX médio + SMA200 60%) é ruidoso (whipsaw no bull). Melhorar: multi-timeframe,
> 138	  histerese, +DI/-DI. Depois expor como MCP `tradeux_get_regime` + contexto no `SYSTEM_PROMPT` do agente.
> 139	- ✅ **lockfile v3** (regenerado em 063df19; override form-data removido — não há mais o que materializar).
> 140	- **OCO**: `oco()`/`cancelOrderList()` expostos no wrapper (endpoint `v3/orderList/oco`), validados em testnet
> 141	  (place+cancel, `ALL_DONE`). FALTA o **wiring no Beholder** (após buy anexar TP+SL; persistir `orderListId` —
> 142	  `orderModel` precisa de coluna/migration; tratar `listStatus` no userData stream). Task NEXT spawnada.
> 143	- **get_wallet bloated** (~193k tokens, junk testnet) e **free-model 429** seguem pendentes.
> 144	- **Logger por categoria** (memória nova): `logger('M:'+id)`→`logs/M<id>.log`, `logger('A:'+id)`→`logs/A<id>.log`,
> 145	  `'system'`→`system.log`. NÃO grepar só `system.log` p/ debug de monitor/automação (custou tempo no OCO).
> 146	- **OCO — ressalva conhecida (BAIXA, não corrigir já)**: o guard anti-empilhamento é **por automação**; 2 automações
> 147	  distintas no mesmo símbolo podem colocar 1 OCO cada (bounded). Fix futuro: índice único parcial `(automationId,symbol)`.
> 148	- **E2E achados abertos (E2E-REPORT)**: `/api/symbols` baixado 6–8×/página (lista enorme); App WS conecta 4–5×/página
> 149	  (leak por remontagem); gráfico TradingView mostra preço **mainnet** vs backend testnet; ordens MARKET às vezes EXPIRAM
> 150	  no testnet (book fino); `res.json(err.body)` manda corpo vazio em erro de ordem (sem msg na UI). Tudo BAIXA/MÉDIA.
> 151	- **net flip-flop (BAIXA)**: o `executionReport` (3s) reescreve net/avgPrice já gravados no insert (DECIMAL→string vs
> 152	  number no `!==`) → 1 UPDATE + notificação redundantes, inócuo aos dados. Alinhar formato se incomodar.
> 153	- ⚠️ **id2/id3 são RUNTIME (não seedados) — REAPLICAR após `make nuke`/reset do testnet**: NÃO estão nos seeders
> 154	  (só "Example Strategy" inativa é seedada). Estado VIVO atual (gate + RSI 25/75 calibrado):
> 155	  - id2 (BUY): `indexes="BTCUSDT:RSI_14_1m,BTCUSDT:REGIME"` · `conditions="MEMORY['BTCUSDT:RSI_14_1m'].current<25 && MEMORY['BTCUSDT:REGIME']!=='bear'"`
> 156	  - id3 (SELL): `indexes="BTCUSDT:RSI_14_1m"` · `conditions="MEMORY['BTCUSDT:RSI_14_1m'].current>75"`
> 157	  - **Revert do gate** (não da RSI): id2 → `indexes="BTCUSDT:RSI_14_1m"` / `conditions="...current<25"`. **Revert da RSI**: voltar 25→30 / 75→70. Ver memória `tradeux-regime-gate`.
> 158	- **Regime job — dívida diferida (BAIXA)**: (a) sem hook de SIGTERM chamando `regimeJob.stop()` (inócuo: `timer.unref()`).
> 159	  (b) ✅ **RESOLVIDO** (commit `e6c10dc`): `getStatus()` exposto em `GET /analysis/regime-status` + card "Regime Gate"
> 160	  no painel `/intelligence` (regime do gate por símbolo + idade + STALE + auto-refresh 60s) → halt silencioso e
> 161	  divergência display×gate agora visíveis. Env: `REGIME_JOB_ENABLED` (kill-switch), `REGIME_REFRESH_MS` (5min),
> 162	  `REGIME_INTERVAL` (1h), `REGIME_SYMBOLS` (CSV).
> 163	- ✅ **Trend Following — ATIVADO** (commit `453c7d6`, gate QA PASS + TL APPROVE, CI verde) via `node backend/scripts/activate-trend.js`:
> 164	  (1) ✅ **coordenação** id2/id3 `&& MEMORY['BTCUSDT:REGIME']!=='trend'` (REGIME nos indexes de AMBAS; id3 ganhou REGIME → **fail-open
> 165	  corrigido**); (2) ✅ **order type** MARKET→**LIMIT marketável** (buffer 0.3% no eval do `limitPrice` pois `limitPriceMultiplier` é
> 166	  DECIMAL(10,2); + `validatePrice` no `updateOrderTemplate`); (3) ✅ **resiliência a restart**: tabela `regimeStates` (PK=symbol,
> 167	  carregada no boot ANTES do 1º poll → cross não se perde no `make restart`). ⏳ **RESTA**: (a) observar **1 golden→death real**
> 168	  (`A:6.log`/`A:7.log`) antes de calibrar; (b) **sizing** id6=3× MIN_NOTIONAL (pequeno p/ observar) → subir depois; (c) ✅ **risco
> 169	  nº1 RESOLVIDO** (commit `e5ef595`): id7 usa **`TREND_QTY`** (posição acumulada via `app-em.updateTrendPosition` no fill: golden
> 170	  soma, death zera; dedup por orderId + guard NaN; `calcQty` capa na carteira + falha-fechado se 0). ⚠️ **`TREND_QTY` é VOLÁTIL**
> 171	  (só MEMORY, ≠ `regimeStates`) → **persistir ANTES de escalar o size** (restart c/ posição aberta = id7 dá throw, não liquida no
> 172	  death); (d) at-least-once: crash entre fire e upsert pode re-disparar 1 cross no boot (ok p/ size pequeno). Reaplicar após
> 173	  `make nuke` (id2/id3/id6/id7 são runtime): `setup-trend.js` + `activate-trend.js`.
> 174	- **Agente LLM — serviço supervisionado** (commit `e97a85a`; gate QA PASS + TL APPROVE): roda no compose (`agent`,
> 175	  restart:unless-stopped, `user:1011:1013`, mem 384M, journal `/journal` rw; backend lê `:ro`). Religar/parar:
> 176	  `docker compose up -d agent` / `docker compose stop agent`. Dívidas (não-bloqueantes): (a) **429 do modelo `:free`** → o
> 177	  ciclo falha e re-tenta a cada 5min (NÃO é crash-loop; o card marca STALE) — roadmap: backoff/kill-switch
> 178	  `TRADEUX_AGENT_ENABLED` espelhando `REGIME_JOB_ENABLED`; (b) o `agent` precisa de `tradeux-agent/.env` (o `setup.sh` só gera
> 179	  o `.env` raiz) → numa máquina nova ele reinicia até o `.env` existir; (c) `tradeux-agent/journal/` é gitignored → após
> 180	  `make nuke`/máquina nova, garantir o DIR como gcrux antes do 1º `up` (com `user:` os ARQUIVOS já nascem gcrux, mas o Docker
> 181	  cria o DIR ausente como root); (d) threshold STALE do card é fixo (15min = 3× o ciclo de 5min); (e) `npm install` (não `ci`).
> 182	- **Agente — prompt alinhado à Farm-and-Funnel** (commit `a0869c4`; gate QA PASS + TL APPROVE): copiloto OBSERVADOR (BTC=cofre nunca
> 183	  vende; automações executam, ele só aconselha); `MAX_TOOL_ROUNDS` 12→20 (código default + .env). Dívidas/gates de liberação:
> 184	  (a) ✅ **RESOLVIDO (commit `9898bdf`, gate QA PASS + TL APPROVE)** — trava determinística e FAIL-CLOSED de SELL-BTC no
> 185	  `tradeux_place_order` (MCP): `isBtcVaultSymbol` barra SELL de TODO símbolo que começa com "BTC" (exceto prefixos não-base
> 186	  BTCUP/BTCDOWN/BTCST), então pares BTC<quote> NOVOS nascem bloqueados sem manutenção de lista — a allowlist de quotes anterior
> 187	  falhava ABERTO (QA enumerou 5 ao vivo escapando: USDS/USD1/EURI/IDR/U). `automationId` obrigatório foi AVALIADO e DESCARTADO
> 188	  (ordens do agente são manuais por design; forçar id falso corrompe P&L em groupByAutomations e não é mutex — doc no código).
> 189	  Teste de regressão hermético (21 casos) + `npm test` + step no CI. **Follow-ups NÃO-bloqueantes (dos gates):** (i) o backend
> 190	  `ordersController.placeOrder` NÃO tem trava equivalente → ordens de UI/outro cliente MCP não passam por ela; mover a defesa p/ o
> 191	  backend se o modelo de ameaça do flip incluir "qualquer caminho com as chaves da conta"; (ii) a premissa "agente BTCUSDT-only" está
> 192	  ERRADA — o SYSTEM_PROMPT autoriza FARM de alts (LTC/BNB/ADA) vs USDT (NÃO quebra a trava: alts não começam com "BTC"); (iii) resíduo
> 193	  fora de escopo: BUY de par BTC-quote (ex.: BUY ETHBTC) também drena o cofre (agente não negocia pares BTC-quote). (b) ✅ **`get_memory_indexes` RESOLVIDO (commit `2d01002`)** via `leanMemoryIndexes`
> 194	  (SEM símbolo: resumo compacto = variáveis distintas + símbolos, sem eval/example; COM símbolo: chaves detalhadas só do par; cap
> 195	  `MCP_MEMORY_INDEXES_SYMBOL_CAP` default 60) — eliminou o ~192k tok / 400 context-overflow. **Ainda ABERTO** o mesmo enxugamento p/
> 196	  `get_memory` (sem símbolo → MEMORY inteira) e `get_wallet_full`. O SYSTEM_PROMPT ainda proíbe a tool (contorno antigo) → pode
> 197	  reabilitá-la agora. Raiz no MCP, mesma classe do get_wallet bloat.
> 198	
> 199	## 🔑 Key paths & commands
> 200	- Repo: `/home/gcrux-tradeux/tradeux` · shell é `ubuntu`, **agir como `sudo -n -u gcrux-tradeux`** (inclusive git/docker).
> 201	- Token: `GITHUB_TOKEN_API` no `.env`. Push: `git push https://x-access-token:$TOKEN@github.com/gabrielZarattini/tradeux.git HEAD:master` (NÃO persistir em .git/config).
> 202	- Deploy: `cd ~/tradeux && ./setup.sh` (= `make up`); `make logs/ps/restart`; `make nuke` apaga o volume do DB.
> 203	- Backtest: `node backend/scripts/backtest.js --days=365` (bear) · `--days=180 --end=2024-04-01` (bull).
> 204	  Regime ao vivo: `node backend/src/utils/regimeClassifier.js BTCUSDT 1h 20`. (rodar em container node + technicalindicators.)
> 205	- Agent: container na rede `tradeux_tradeux` (ver memória `tradeux-agent-500k-validation`).
> 206	- Memory: `/home/ubuntu/.claude/projects/-home-gcrux-tradeux/memory/`.
> 207	
> 208	---
> 209	
> 210	## 📝 Session Records (newest last)
> 211	
> 212	### Record — 2026-06-03 (Validation phase) — [resumo abreviado]
> 213	Deploy do stack + fix 502, white-screen, auto-sync symbols, agente LLM, RSI baseline, stop-loss/OCO
> 214	validados, backtest v1 (não persistido), ShakeHands + agentes QA/Tech-Lead. (Detalhe nos commits.)
> 215	
> 216	### Record — 2026-06-03 (cont. — merges, segurança, backtest, modelo de trabalho)
> 217	Sessão grande. (1) **Re-rodei o gate** nos 2 PRs e descobri que não eram PRs reais (só branches) —
> 218	**criei+mergeei #10/#11** via API (token novo no `.env`). Triei os 8 PRs restantes: **fechei #1-7**
> 219	(dependabot frontend obsoletos pós-Vite) e **superseded #9** (BYOK) aplicando o equivalente direto no
> 220	master. **Backlog de PRs = 0.** (2) **Selei o modelo trunk-based** (Claude orquestra+aprova/devolve+sobe;
> 221	gate proporcional) — memória `tradeux-orchestration-model`. (3) **Segurança**: Dependabot **28→6**
> 222	(critical+8 high zerados via twilio 3→6 + override form-data), com gate QA+Tech-Lead, backend recriado
> 223	em prod, boot limpo; `node-binance-api` 0.13→1.x deferido (task spawnada, destrava OCO). SECURITY.md
> 224	atualizado. (4) **Backtest de ciclo completo** (bear 365d + bull 2024) + **detector de regime**
> 225	(`regimeClassifier.js`, testado: BTC→bear/cash) — achado honesto: **Buy&Hold é dificílimo de bater em
> 226	retorno bruto; o edge do trading ativo é risco-ajustado (drawdown), não outperformance; HFT é morto.**
> 227	Próximo: classificador com histerese + wiring no agente; bump do node-binance-api.
> 228	
> 229	### Record — 2026-06-03 (cont. — regime wiring + dashboard de agente + /handoff)
> 230	Continuei do "comece". (1) **Regime Fase 1 ✅ live**: endpoint `GET /api/analysis/regime/:symbol` (klines
> 231	mainnet, cache 2min, regime = estado real do mercado) + MCP `tradeux_get_regime`; gate QA+Tech-Lead (ressalva
> 232	MÉDIA do QA corrigida: `limit=300` + guard de dados insuficientes); testado ao vivo (BTC/ETH→bear/cash); commit
> 233	`0a97820`, backend recriado, boot limpo. (2) **E2E no browser** (Claude-in-Chrome): login→dashboard, chart BTC
> 234	vivo + RSI, App WS conectado, **zero console errors**, Orders com 27 ordens BTCUSDT (19 buy / 7 sell — baseline
> 235	acumulando na queda, confirma o backtest). (3) **Carteira testnet** ~US$285k é RUÍDO (445 faucet coins a preço
> 236	sintético); sinal real = acumulação de BTC na baixa. (4) **Dashboard de agente Fase A** ✅ commit `40b5a18`:
> 237	`GET /api/agent/runs` lê o journal e devolve KPIs reais — validação = **366k tokens, 91.5k/ciclo, 99% input**
> 238	(o `get_wallet` bloat é a otimização nº1). **NÃO-live ainda** (build travado pelo WIP). (5) **Descoberta**: a task
> 239	`node-binance-api` 0.13→1.x ficou ATIVA no working tree (package.json/lock/exchange.js em 1.x) — deixei intocada;
> 240	validar testnet (ordem/OCO) + gate antes de subir. (6) **/handoff** selado (secret-scan limpo; só os 4 arquivos do
> 241	dashboard commitados, WIP do node-binance-api preservado). NEXT: concluir/validar/subir node-binance-api (destrava
> 242	dashboard + OCO + zera as 6 moderate) · **regime Fase 2** (gate id2/id3: não comprar em bear) · **dashboard Fase B**
> 243	(página visual). Memória: novo `tradeux-agent-token-economics`.
> 244	
> 245	### Record — 2026-06-03 (cont. — node-binance-api 0.13→1.x + segurança, COMMITADO)
> 246	Fechei o gap prod≠master do node-binance-api. (1) **Investigação profunda da API 1.x** (fork **ccxt**, reescrita
> 247	ESM+CJS): instalei a 1.0.27 num scratch e li typings/source — confirmei (não adivinhei) cada adaptação. (2)
> 248	**Reescrevi `exchange.js`**: `test:true` (roteia ws-api testnet p/ userData), ordens via `binance.order()`
> 249	(buy/sell 1.x quebram STOP via flags), `ohlc()`→`populateOHLC()`, userData callbacks reordenados, `terminate()`
> 250	por **URL completa** (regressão que o QA pegou: 1.x indexa subscriptions por url, não nome curto → era no-op +
> 251	vazava socket), `bookStream` via `subscribe('!bookTicker')` (BOOK inativo), e expus `oco()`/`cancelOrderList()`.
> 252	(3) **DESCOBERTA**: node-binance-api NÃO era a única fonte das 8 — o `@sendgrid/mail@6.5.5` sustentava
> 253	`request@2.88` sozinho. Remover só o override re-exporia 2 CRÍTICOS. Decisão do dono: **bumpar `@sendgrid` 6→8**
> 254	(drop-in, usa axios). Resultado medido: **backend 8→2 moderate** (0 crit/high; restam sequelize→uuid não-exploráveis),
> 255	override removido, lockfile→v3. (4) **Validação testnet** (lib smoke + E2E backend): exchangeInfo, streams,
> 256	**userData ws-api entregou executionReport**, MARKET fill no MIN_NOTIONAL, LIMIT/STOP_LOSS_LIMIT/OCO place+cancel,
> 257	boot limpo, id2/id3 re-armadas, site 200. (5) **Gate QA (PASS c/ ressalvas) + Tech-Lead (APPROVE c/ sugestões)** —
> 258	corrigi as 2 ressalvas (terminate por URL + lockfile v3) e re-validei. (6) **Commit `063df19` + push master**.
> 259	GOTCHA reforçado: `npm install` como ubuntu também polui o `.git` (npm chama git p/ gitHead) → `chown .git` p/ gcrux.
> 260	NEXT: **OCO wiring no Beholder** (task spawnada) · regime Fase 2 · dashboard Fase B.
> 261	
> 262	### Record — 2026-06-03 (cont. — OCO wiring + E2E + painel P&L/BTC + Intelligence + pivô 3 BTC)
> 263	Sessão grande, **5 commits no master, todos CI verde + validados em testnet/navegador**. (1) **OCO wiring no
> 264	Beholder ✅** (`aa3f7f7`): migration `orderListId` (BIGINT nullable, portável MySQL+PG, idempotente), `placeOco`
> 265	(template `type:'OCO'`→SELL protetiva TP LIMIT_MAKER + SL STOP_LOSS_LIMIT, persiste 2 pernas), `processListStatusData`
> 266	(reconcilia `ALL_DONE`/`REJECT`, idempotente), endpoint `DELETE /orders/oco/:symbol/:orderListId`, cancel no delete
> ```

## 🤖 Claude *(03:13:57)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' log --oneline -7",
  "description": "Show recent git log"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 854bab5 feat(pnl): net fee-inclusive ciente do lado — taxa em BNB/qualquer asset -> USDT (item (c))
> 1b639ce fix(safety): cap diario exclui Earn/Locked (LD*) do equity-tradeable
> 8ef1b69 feat(safety): cap diario -5% (drawdown de equity) + kill-switch QUENTE (item (e))
> baf0f4b feat(safety): 3 pre-reqs de descongelamento — FARM_SELLING, TREND_QTY persist, teto
> 7ec6e75 fix(cockpit): baseline=null p/ simbolos nao-flow-gated (mata gate-fantasma da alt)
> e27339a fix(exchange): teto MAX_ORDER_NOTIONAL cobre MARKET-por-qty (deriva preco do MINI_TICKER)
> 0b1554d docs(agent): doutrina GATE != TRIGGER no SYSTEM_PROMPT (fecha a classe gate-aberto-mas-condicao)
> ```

## 🤖 Claude *(03:13:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' status --short",
  "description": "Show git working tree status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> (Bash completed with no output)
> ```

## 🤖 Claude *(03:13:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sudo -n -u gcrux-tradeux bash -lc 'cd /home/gcrux-tradeux/tradeux && docker compose ps' 2>&1",
  "description": "Show docker compose container status"
}
```

## 🤖 Claude *(03:13:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "curl -s -m5 -o /dev/null -w \"%{http_code}\" https://tradeux.gcrux.com/",
  "description": "Check live site HTTP status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> NAME                 IMAGE              COMMAND                  SERVICE    CREATED        STATUS                PORTS
> tradeux-agent-1      tradeux-agent      "docker-entrypoint.s…"   agent      33 hours ago   Up 33 hours           
> tradeux-backend-1    tradeux-backend    "docker-entrypoint.s…"   backend    12 hours ago   Up 12 hours           3001/tcp
> tradeux-db-1         mysql:8.0          "docker-entrypoint.s…"   db         2 weeks ago    Up 3 days (healthy)   3306/tcp, 33060/tcp
> tradeux-frontend-1   tradeux-frontend   "/docker-entrypoint.…"   frontend   2 days ago     Up 2 days             127.0.0.1:8090->80/tcp
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 200
> ```

## 🤖 Claude *(03:14:05)*


## 🤖 Claude *(03:14:06)*

Stack está saudável (4 containers up, site 200). Vou ler os registros mais recentes do HANDOFF para fechar o brief.

## 🤖 Claude *(03:14:07)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/HANDOFF.md",
  "offset": 640,
  "limit": 130
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 640	
> 641	### 🤝 SEAL — 2026-06-10 (cont. — agente recalibrado pós-incidente de spam no Telegram)
> 642	**1 commit gated no master/origin (`vivo==master==origin==12ceabe`).** O canal novo de notificações expôs na 1ª noite um incidente REAL do agente: **6 alertas falso-positivos parafraseados** sobre a venda do harvester id25 em bear ("viola a regra do cofre!") + **2 em inglês**. O dono respondeu com a doutrina canônica (verbatim): *"só pode vender btc se obtiver lucro... Trade com base em lucros. Mas sim com certeza burrico de acumular (não somente) mas acumular 3 BTC"* + *"Ajustar para sempre enviar em português brasileiro. Somente termos técnicos em inglês."* Causa raiz DUPLA: (a) SYSTEM_PROMPT desatualizado (não conhecia o harvester; doutrina absoluta "BTC nunca é vendido"); (b) **zero memória entre ciclos** — a regra "não repita" era impossível de cumprir (cada ciclo nasce zerado; o modelo re-descobria a mesma "incoerência" e re-alarmava parafraseado).
> 643	**Fix (`12ceabe`, tradeux-agent apenas):** (1) doutrina POR MÓDULO no SYSTEM_PROMPT — cofre nunca é vendido; harvester id25 = NO-LOSS garantido (fill < custo = bug, aí sim alarma; só alarmar prejuízo/oversell); **trend id7 zera TREND_QTY no death cross INDEPENDENTE do P&L — corte de perda é DESENHADO** (whipsaw no prejuízo é correto); baseline id3 mencionada (pausada); ordens manuais = dono/operador; (2) guardrail 6: **pt-BR obrigatório** em diário E notificações; (3) `buildKickoff()` injeta as últimas 5 notificações já enviadas (de `journal.recentOwnerNotifications`, varre o journal inteiro, trunca 300 chars normalizados) — memória anti-repetição; SYSTEM_PROMPT segue estável (cache de prefixo); (4) cap mecânico `MAX_NOTIFY_PER_CYCLE=2` no runCycle (3ª chamada volta como erro pro modelo; bloqueios não entram no dedupe).
> 644	**⚠️ Gates pegaram um erro MEU (lição):** a 1ª versão dizia "id7 sempre com lucro" — FALSO (QA e TL verificaram `setup-trend.js`: sellCond = death cross puro, sem gate de lucro; doc §"corta perda") → teria plantado o PRÓXIMO falso-positivo (whipsaw). Corrigido pré-commit. **Decisão de produto registrada:** gate de lucro na id7 NÃO será feito (segurar trend perdedor em queda = refutado pelo backtest); a regra do dono é literal só pro harvester.
> 645	**Regressão ao vivo:** ciclo `--once` com o journal real (os 6 alertas do incidente injetados no kickoff) = **0 re-notificações + resumo pt-BR**; a única notificação nova do período (ordem manual LTC, tom calmo "nenhuma ação requerida") veio do CONTAINER ANTIGO ainda no ar — substituído no deploy.
> 646	**Estado vivo:** 4 containers up (agent recriado), site 200, bear nos 4, harvester ×4 com bucket {0,0} aguardando dislocação, 1 rung ×2 antiga aberta. **0 PRs.** Memórias `tradeux-telegram-notifications` (incidente+fix+decisão id7) e índice atualizados. **NEXT inalterado:** observar o ×4 (2-3 dias; conferir também o comportamento do agente recalibrado nos próximos ciclos — pt-BR, sem spam, eventos novos ainda passam) → ×8; Fase 4 no aviso "[FASE4]"; dívidas menores (TREND_QTY persistir, rate-limit /agent/notify, two-way).
> 647	
> 648	### 🤝 SEAL — 2026-06-14 (Auditoria de desempenho do Harvester v2 + Validação de Regime-Gating)
> 649	**Resumo da sessão ad-hoc de diagnósticos e continuidade (zero alterações de código):**
> 650	1. **Harvester v2 (BTC/USDT):** Confirmamos via consultas diretas ao banco de dados MySQL (`harvestPositions` e `orders`) que o Harvester obteve lucro em 100% dos 5 wicks seguidos de dislocação capturados com size ×4, com retornos entre +1.88% e +3.90%. O bucket tático foi zerado e persistido corretamente (`qty=0, cost=0` em `harvestPositions`), provando a eficácia da trava LEVEL-trigger contra double-selling e resiliência a reinicializações. Nova compra armada em `$61.414,10` (id 163).
> 651	2. **Regime-Gating (BNBUSDT):** Validamos que o SMA Golden Cross (50/200) de BNBUSDT ocorrido em 12/06 01:03Z foi devidamente interceptado pelo gate passivo de regime (`BNBUSDT:REGIME !== 'bear'`), protegendo o caixa contra falsos-sinais em tendência macro de baixa.
> 652	3. **Mapeamento de Infraestrutura:** Verificamos a saúde dos containers no compose (4 no ar, sem crash loops), logs e conectividade com a API do Chroma (heartbeat ativo).
> 653	
> 654	**NEXT:** (a) Seguir monitorando o Harvester no size ×4 por mais 1-2 dias antes de escalar para ×8; (b) calibrar o Sniper Flow Gate na id 2 via z-score de volume com base no log `flow-capitulation.log` (>230 KB acumulados); (c) integrar/persistir a variável `TREND_QTY` no banco antes de escalar o sizing do Trend Following.
> 655	
> 656	### 🤝 SEAL — 2026-06-14 (cont. — Correção crítica de migração no Postgres/MySQL + CI verde)
> 657	**Resolução do bug das migrações do banco de dados e estabilização do CI (1 commit, trunk-based, master/origin; `vivo==master==origin==a408500`).**
> 658	
> 659	1. **Causa-raiz identificada:** 
> 660	   - O CI falhava no PostgreSQL com `relation "ordertemplates" does not exist` porque o Postgres força identificadores sem aspas para letras minúsculas. Como a tabela foi criada em camelCase como `orderTemplates`, as queries brutas no banco precisam ser delimitadas com aspas duplas (`"orderTemplates"`) para preservar as maiúsculas no Postgres.
> 661	   - A tentativa anterior de corrigir isso usando `queryInterface.quoteTable('orderTemplates')` quebrou tanto no MySQL quanto no Postgres no CI porque `quoteTable` não é uma função válida no objeto `queryInterface` no Sequelize v6.
> 662	
> 663	2. **Fix implementado (`a408500`):**
> 664	   - No arquivo `backend/migrations/20260614180000-btc-scalping-excess.js`, adicionamos uma verificação dinâmica de dialeto:
> 665	     ```javascript
> 666	     const dialect = queryInterface.sequelize.options.dialect;
> 667	     const orderTemplatesTable = dialect === 'mysql' ? '`orderTemplates`' : '"orderTemplates"';
> 668	     ```
> 669	   - Isso garante que a query direta seja gerada com crases no MySQL (`` `orderTemplates` ``) e com aspas duplas no Postgres (`"orderTemplates"`), garantindo portabilidade perfeita em ambos os dialetos.
> 670	   - Executamos `git add` e `git commit` com o usuário correto `gcrux-tradeux` (para evitar problemas de ownership de arquivos em `.git`) e efetuamos o push utilizando o token do GitHub disponível no `.env` do diretório raiz.
> 671	   - As migrações locais no MySQL rodaram e completaram com sucesso via `make migrate`.
> 672	
> 673	**Estado vivo:** 4 containers ativos, site 200, banco sincronizado e migrações locais atualizadas. O push engatilhou o CI e agora a esteira do GitHub Actions deverá passar de forma limpa em ambas as matrizes de dialeto (MySQL e Postgres).
> 674	
> 675	**0 PRs** (modelo trunk-based).
> 676	
> 677	### 🤝 SEAL — 2026-06-15 (GO-LIVE MAINNET: auditoria + blindagem money-path + revisão de estratégia $148 + fix P0 do Farm; CONGELADO)
> 678	**Contexto:** a sessão paralela do **Antigravity** (commits `e610f90`..`1fe3364`, madrugada 2026-06-15) entregou **ambiente dual (testnet/mainnet) + isolation filter** e o dono **virou pra MAINNET REAL** (`settings.useTestnet=0`, api.binance.com) e **fundou ~150 USDT**. Isso entrou **SEM gate QA/TL**. Esta sessão (Claude) auditou, blindou e corrigiu. **Vivo==master==origin==`c163112`** (2 commits meus, trunk-based; CI roda no push).
> 679	
> 680	**(1) 🔍 Auditoria de go-live mainnet (wf `wf_b252a2ba-9de`, 13 agentes + verif. adversarial).** Diagnóstico do "nenhuma ordem real ainda": **ESPERADO** (modules armed-waiting + gating + ledger frio + ~$148 USDT; engine comprovadamente em mainnet — `userDataStream` OK). Mas achou riscos de money-path.
> 681	
> 682	**(2) 🛡️ Blindagem money-path (commit `96915e0`, QA PASS-c/ressalvas + TL APPROVE; deployado+verificado).**
> 683	- **Teto de risco no BACKEND** (`exchange.js`, chokepoint buy/sell/oco): `TRADING_HALT` (kill-switch global, cobre TUDO) + `MAX_ORDER_NOTIONAL_USDT=1500` (teto por ordem; ⚠️ NÃO cobre MARKET-por-quantidade — só o HALT — FOLLOW-UP). É a ÚNICA trava de tamanho do backend (o `ALLOW_TRADING` é só do agente).
> 684	- **Funil live-buy** refeito (`funnelJob.maybeLiveBuy`/`persistFunnelBuy`): usa SÓ o baseline FIXO do env (nunca o `RUNTIME_BASELINE` da Fase4 → mata o dreno-por-depósito), teto obrigatório por compra (sem teto = RECUSA), alerta o dono na falha de persistência. + `FUNNEL_LIVE_BUY=false` (shadow).
> 685	- `ordersController.placeOrder` corrigido (passava `.get()` num objeto plano → 500; matava venda manual de emergência). `insertOrder` honra isTestnet explícito (anti-ghost). `getOpenOrdersByAutomation`/`getOpenOcoOrders` filtram ambiente (reconcile não cruza testnet↔mainnet). Scripts backfill com guard `ALLOW_BACKFILL`+`isTestnet:true`.
> 686	- **`.env`** (host, não versionado): `FUNNEL_LIVE_BUY=false`, `FUNNEL_MAX_BUY_USDT=100`, `MAX_ORDER_NOTIONAL_USDT=1500`, `TRADING_HALT=true`, e **SAPI/API/STREAM → mainnet** (encerra o split-brain de SAPI que ainda batia em testnet). **Ruled out:** agente LLM NÃO coloca ordem real (`ALLOW_TRADING=false` verificado no container); trava SELL-BTC do cofre vale.
> 687	
> 688	**(3) 📉 Revisão de estratégia p/ $148 reais (wf `wte6rt68t`, 8 agentes + verif. adversarial 3 lentes). DESCOBERTA CRÍTICA:**
> 689	- **🪦 HARVESTER (id22-25) MORTO no mainnet.** `getFairPrice` (`fairPriceService.js:33`) busca SEMPRE o lastPrice MAINNET hardcoded; o BOOK do bot é simulado do miniTicker (monitor BOOK off). No mainnet, book=FAIR (mesma venue, spread ~$0.01) → o gatilho `bestAsk<FAIR×0.97` (−3%) nunca dispara. Os "10/10 ciclos lucrativos" eram **arbitragem testnet-vs-mainnet** (artefato). Redesign: re-ancorar FAIR a HIGH rolante 24-48h (klines) + backtest + gate de regime. **NÃO afrouxar 0.97 nem ligar o monitor BOOK real** (vira scalper que sangra fee).
> 690	- **TREND (id6/7,15-20) = ÚNICO edge real** (same-exchange, golden/death cross), mas minúsculo ($5-15/perna, ~1-3 RT/símbolo/mês). **EXPECTATIVA REAL: $148 spot ≈ FLAT no mês** (~$0/dia mediano). **+3 BTC é impossível (1.350×).** 0 ordens mainnet → nada validado com fill/fee/slippage reais. Win = validação + paciência; maior risco = forçar trade e sangrar fee.
> 691	
> 692	**(4) 🔧 Fix P0 do Farm (commit `c163112`, QA PASS-c/ressalvas + TL APPROVE re-review; deployado+verificado).** Bug: Farm Sell (`orderTemplates` id6/8/10) = `MAX_WALLET` → vendia a carteira INTEIRA e dumpava a posição do Trend co-localizado nos mesmos alts. Fix em 3 frentes: (a) keyword **`FARM_QTY`** em `beholder.calcQty` (espelho do HARVEST_QTY); (b) **`getFarmPosition` escopado por automação** (`name LIKE 'Farm %'` → o Trend não infla/re-baseia mais o bucket — era o 2º must-fix que o TL pegou); (c) **migration `20260615200000`** durável (sobrescreve a `20260614190000` que era o próprio bug): Farm Sell→FARM_QTY, Farm Buy ×200→×2 (~$10), Baseline RSI Buy id2→isActive=0 (acumulador pelado, compra sem venda). Verificado no DB pós-migrate; 18 autos ativas (id2 saiu); boot limpo; **TRADING_HALT=true mantido**.
> 693	
> 694	**Estado vivo:** 4 containers up, site 200, **MAINNET CONGELADO** (`TRADING_HALT=true`), funil shadow, ~$150 USDT, 0 ordens mainnet (tudo testnet). `.git` intacto (gcrux-tradeux). Memórias: **`tradeux-mainnet-go-live` (nova)**, `tradeux-harvester-experiment` (caveat: edge era testnet) + índice. Secret scan: limpo (`ci-key`/`ci-secret` são fixtures do CI, não chaves).
> 695	**NEXT (antes de descongelar — sem pressa, congelado é o estado seguro):** (a) trava `FARM_SELLING` anti-empilhamento (análoga a HARVEST_SELLING); (b) dono confere **saque-OFF + IP travado** na chave mainnet (o `withdraw()` fica fora do HALT); (c) decidir o **re-design do harvester** (re-ancorar FAIR + backtest) OU rodar só o Trend; (d) plano de canary (1 trade mínimo com log de fill/fee/slippage) antes de escalar. **FOLLOW-UPS menores:** fechar o furo MARKET-by-quantity no riskGuard; teto diário/posição; escopo do Farm por flag/tag (em vez de `name LIKE`). **0 PRs** (trunk-based).
> 696	**NEXT:** Seguir o monitoramento do Harvester no size ×4 por mais 1-2 dias antes de escalar para ×8.
> 697	
> 698	### 🤝 SEAL — 2026-06-16 (Cockpit Intelligence brain-integrado + fix −1013 do Trend + auditoria adversarial de descongelamento)
> 699	**Sessão grande. Vivo==master==origin==`1660871` (2 commits: `2528a5d` beholder isolado + `1660871` cockpit, JÁ no origin). 4 containers up, HALT=true intacto, 0 ordens mainnet.**
> 700	
> 701	**(1) 🎛️ Cockpit Intelligence — feature READ-ONLY (brain computa / agente lê+reporta / front consome).** O pedido "dashboard estilo vídeo viral do Fable" evoluiu p/ feature de DADO REAL brain-integrada. ⚠️ **GOLPE:** o "vídeo viral Fable 5 / Polymarket / 205x / export-controlled" do X é **referral scam** (link `?via=ace-cjyf`) — orientado dono a NÃO clicar/depositar/copy-tradar; mesma fantasia de edge-impossível que nossa pesquisa refuta. Entregue (QA-PASS/TL-APPROVE Fase A e B+C; deployado+verificado): `cockpitJob`+`utils/cockpitService.js` (klines 1m MAINNET → distribuição de retornos, EV net-de-fee, tail, histograma, banda MC **driftless**, snapshot regime/flow/gates → `MEMORY['<sym>:COCKPIT']`, passivo `executeAutomations=false`); `GET /analysis/cockpit` (+env `useTestnet`/`tradingHalt`); tool MCP **read-only** `tradeux_get_cockpit`; **fix do BLOQUEADOR do prompt** (`agent.js` afirmava "conta é TESTNET/equity é ruído" em MAINNET → agora **env-aware** deferindo ao cockpit); frontend `/cockpit` (neon, consome o snapshot do brain, fallback klines). Verificado ao vivo: o agente chamou `tradeux_get_cockpit` e reportou coerente (mainnet real + halt). **A brain reporta EV/trade −0,16% / só 0,6% dos moves limpam a fee** — a própria máquina mostra que scalp 1m é −EV (o oposto honesto do golpe). Memória `tradeux-1m-scalping-and-cockpit`. Screenshots via Playwright headless (`/tmp/cockpit-shot.js`, login pelo `tradeux-mcp/.env`).
> 702	
> 703	**(2) 🔧 Fix do −1013 no Trend (commit `2528a5d`, QA-PASS/TL-APPROVE).** orderTemplate **id3** (usado pela automação **id6 ATIVA** Trend Buy BTC) sofreu drift p/ `quantityMultiplier=1.00` → em `beholder.calcQty` o `Math.floor(qty/stepSize)*stepSize` empurrava o MIN_NOTIONAL **abaixo de $5** → quando um golden cross disparasse, a Binance rejeitaria **-1013** e a id6 NÃO compraria (repro: $4,65 BTC / $4,94 ETH / $4,80 BNB / $4,99 ADA). Fix 2 camadas: **backstop de piso** em `calcQty` (cirúrgico, **só MIN_NOTIONAL**, idempotente, NÃO toca posições TREND/HARVEST/FARM/MAX_WALLET — cobre farm/harvester de quebra) + template id3 → **×3** (~$15, intenção documentada do `setup-trend.js`). DB UPDATE aplicado ANTES do boot; BRAIN re-init com ×3 verificado via `/beholder/brain`. HALT intacto.
> 704	
> 705	**(3) 🔍 Auditoria adversarial INDEPENDENTE de descongelamento (wf `wew1texdp`, 4 auditores + verif. anti-falso-positivo).** Segurança do diff do cockpit: **SEM_PROBLEMA_REAL** (read-only confirmado: writeTool 9→9, env só 2 booleanos, sem money-path). CONFIRMOU 7 achados que pesam contra descongelar AGORA: (1) **pré-reqs não resolvidos** (saque-OFF/IP **não confirmado**; trava **`FARM_SELLING` AUSENTE** — grep=0, nunca implementada); (2) **harvester morto** (id22-25 ainda ATIVAS); (3) **0 ordens mainnet** (descongelar = 1º trade real, fill/fee/slippage não validados); (4) **gap `MAX_ORDER_NOTIONAL`** (SELL MARKET por qty-base NÃO é capado — só o HALT); (5) **bug P&L com BNB** (net não desconta a taxa em BNB → painel mente otimista); (6) **sem cap diário/posição**; (7) **1m refutado** (−0,14% a −0,23%/trade no cache real). Também pegou 3 bugs do cockpit que eu subestimei → **CORRIGIDOS** no `1660871`: gate fluxo **fail-OPEN→fail-CLOSED** (mostrava GO sem fluxo fresco; id2 real bloqueia); gate como **DOUTRINA** (`doctrine=true` + disclaimer no MCP — a baseline id2 está `isActive=0`, não é estado vivo); `.toFixed(2)` colapsava a banda MC de alts (ADA 0,18/0,18/0,18) → **precisão dinâmica**.
> 706	
> 707	**Estado vivo:** 4 containers up, **MAINNET CONGELADO** (`TRADING_HALT=true`), ~$150 USDT, 0 ordens mainnet. `.git` intacto (gcrux-tradeux). Memórias: `tradeux-1m-scalping-and-cockpit` (atualizada) + índice.
> 708	**NEXT (descongelamento RESPONSÁVEL — recomendação FUNDAMENTADA NA AUDITORIA, não flip cego):** pré-reqs antes de QUALQUER ordem real: **(a)** dono confirma chave Binance **saque-OFF + IP travado**; **(b)** **desativar harvester** (id22-25 → isActive=0, morto+falling-knife); **(c)** **fix do P&L com BNB** (senão o painel mente); **(d)** **fechar o gap do teto** p/ SELL-by-base (ou restringir a LIMIT/OCO); **(e)** **cap diário de perda** OU size minúsculo + 1 trade. Aí canary: **só a Trend id6 ativa** (resto parado), ×3 (~$15), observar **1 ciclo golden→death real**, medir fill/fee/slippage; **persistir `TREND_QTY`** antes de escalar. **Claude NÃO vira o `TRADING_HALT`** — é GO do dono + (a)-(e). Ofereci fazer **(b)(c)(d) com QA/TL** como próximo passo. **PRs: 0** (trunk-based direct-to-master; commits já no origin, CI rodando).
> 709	
> 710	### 🤝 SEAL — 2026-06-16 (Coerência do Cockpit + anti-spam do agente — 7 commits, QA/TL em cada, HALT intacto)
> 711	**Sessão dirigida pelas mensagens do agente no Telegram: o dono encaminhou observações, eu diagnostiquei cada uma e corrigi as REAIS. Vivo==master==origin==`0b1554d` (7 commits, trunk-based; CI rodando). 4 containers up, site 200, `TRADING_HALT=true` intocado o tempo todo, 0 ordens mainnet.**
> 712	
> 713	**O gatilho:** o agente vinha flagando "divergências" cockpit×oráculo no Telegram. Investigação (wf `wf_8cc8b47b-22c`, 6 agentes + verif. adversarial `synthesis-holds`) provou que o cockpit **lê as MESMAS chaves** `MEMORY['REGIME']/['FLOW']` dos oráculos vivos — não é fonte paralela. A maioria era ESPERADA (histerese, idade de snapshot); algumas eram bugs REAIS de VIEW/honestidade. Corrigi em camadas:
> 714	
> 715	1. **`6042bd9` fix(cockpit): freshen no read-path + anti-spam (prompt).** O cockpit congelava flow/regime no tick de 60s; o agente comparava o número velho com o vivo e chamava de "contradição". `cockpitJob.freshen()` recomputa regime/flow/gates da MEMORY no instante da LEITURA (analítica 1m segue em cache) + expõe `flow.ageMs`/`ageSec`. `getRegime` anexa `data.gate` (regime HISTERÉTICO operativo) sem mudar `data.regime` (instantâneo, card UI). QA-PASS+TL-APPROVE.
> 716	2. **`64752f0` feat(agent): dedup de notificação POR ASSUNTO em código.** Defesa em profundidade independente do prompt (`tradeux-agent/src/notifyDedup.js`, puro/testável): normaliza+canoniza sinônimos PT/EN, chave de tópico = vocabulário de domínio ∪ tickers ∪ transições direcionais, **Jaccard ≥ 0.6**; guards anti-falso-positivo (símbolo distinto / transição inversa / marcador de evento inédito). Roda ANTES do cap 2/ciclo (suprimido não consome o cap). **Self-test com mensagens REAIS do Telegram (15 casos) wired no CI.** Red-team pegou B6 CRÍTICO (ticker por sufixo p/ alts novas) → corrigido. QA-PASS+TL-APPROVE.
> 717	3. **`bf254a0` fix(cockpit): reason reflete o regime real** — mostrava "range + fluxo ok" com regime `mixed` (auto-contradição); agora interpola o regime. Decisão do gate intocada (mixed é mean-reversion = correto). QA-PASS+TL-APPROVE.
> 718	4. **`37ed4b1` refactor(agent): consolida doutrina anti-ruído num bloco `DIVERGÊNCIAS ESPERADAS`** — 3 regras anti-ruído repetidas → 1 bloco rotulado (6→7 itens) + ponteiros. Zero regra perdida. QA-PASS+TL-APPROVE.
> 719	5. **`8884bd3` fix(cockpit): gate de acumulação SYMBOL-AWARE (BUG REAL).** `deriveGates` aplicava o filtro de fluxo da baseline BTC a TODOS os símbolos; mas só a id2 (BTC) é flow-gated (`setup-flow-gate.js`), o FARM das alts gateia só RSI+regime (`setup-farm.js:131`). Mostrava alt em capitulação como `buyAllowed=false "baseline veta"`, vetando entrada que a farm VIVA faria. Fix: `deriveGates(regime,flow,symbol)` + `FLOW_GATED` (env, default BTCUSDT) → `buyAllowed = flowGated ? baseline : farm`. QA-PASS (truth-table 24 células)+TL-APPROVE.
> 720	6. **`2c8655c` fix(cockpit-ui): painel "Trade bridges" consome o gate symbol-aware** — o frontend tinha o MESMO hardcode (`imbalance>-0.4` p/ toda alt); agora consome `cp.symbols[s].gates` (alts: fluxo informativo `.info`/"fluxo·i", não bloqueia). Frontend-only. QA-PASS+TL-APPROVE.
> 721	7. **`0b1554d` docs(agent): doutrina GATE ≠ TRIGGER (item 7 do bloco).** O agente flagou `farm=true` com RSI 79/66/62 (>35) como incoerência. NÃO é bug: o gate é DOUTRINA de regime/fluxo (`doctrine:true`), NÃO lê RSI; o FARM dispara só no dip RSI<35. Fix agent-side (não cockpit). QA-PASS+TL-APPROVE.
> 722	
> 723	**Aprendizados duráveis (na memória `tradeux-1m-scalping-and-cockpit`):** (a) o **dedup ESTÁ funcionando** — as ~8 notificações eram TÓPICOS DISTINTOS ao longo de ~10h, não repetição (rodei pelo módulo p/ provar); journal persistido em volume. (b) **VERDICT do TL: a fase de ENUMERAÇÃO REATIVA de coerência do cockpit está DONE** — os 2 sub-eixos de "gate aberto mas X não atendido" cobertos (fluxo `8884bd3` = bug real; RSI/trigger `0b1554d` = leitura). Próximo eixo plausível = notional/saldo; NÃO pré-emptar — o catch-all do prompt ("só sinalize se a fonte VIVA por si só mostrar anomalia") já segura; se aparecer é +1 item incremental.
> 724	
> 725	**Tech debt / follow-ups (chips abertos, fora do escopo):** (1) notify-dedup por assunto em código foi FEITO (`64752f0`); (2) painel "Trade bridges" FEITO (`2c8655c`); **(3) baseline id2 (RSI<25) é runtime/PATCH, NÃO seedada** (QA flagou — pós-`make nuke` reaplicar manual; dívida já conhecida em `tradeux-regime-gate`). **Descongelamento:** pré-reqs (a)-(e) do SEAL anterior SEGUEM PENDENTES (saque-OFF/IP, desativar harvester, fix P&L BNB, gap teto SELL-by-base, cap diário). **PRs: 0** (trunk-based; tudo já no origin).
> 726	
> 727	### 🤝 SEAL — 2026-06-17 (Descongelamento EM CURSO: pré-reqs (a)(b)(d) + cockpit gate-fantasma + 3 BLOQUEADORES — 3 commits, todos QA+TL, 2 workflows adversariais, HALT intacto)
> 728	**Sessão de descongelamento responsável dirigida pelo dono. Vivo==master==origin==`baf0f4b`. 4 containers up, `TRADING_HALT=true` intocado, 0 ordens mainnet, ~$148,84 USDT. PRs: 0 (trunk-based direct-to-master; tudo no origin).**
> 729	
> 730	**Pré-reqs de descongelamento FECHADOS esta sessão:**
> 731	- **(a) chave Binance saque-OFF + IP travado — FEITO+VERIFICADO.** Dono desmarcou na UI **Enable Withdrawals** (= "saque off"; não existe botão "saque off", é desmarcar Withdrawals) + **Permits Universal Transfer**; restou Reading + Spot Trading; IP **`137.131.243.179`** (= IP de saída do servidor, host==container, via api.ipify). Verifiquei read-only: login + `GET /exchange/balance/USDT` → 200, **USDT 148,84** lido. Saque-OFF NÃO é verificável por leitura (e NÃO se testa saque); confiança = Save na UI. Ver memória `tradeux-mainnet-go-live` item 2.
> 732	- **(b) harvester id22-25 DESATIVADO** (`isActive=0` via `POST /automations/:id/stop`; bucket vazio, BRAIN só 6,7,9-20). `setup-harvester.js` já cria default-OFF → durável até `make nuke`. MORTO no mainnet (edge era artefato testnet).
> 733	- **(d) furo SELL-by-base do riskGuard FECHADO** (`e27339a`): `assertWithinRisk` agora deriva preço (stopPrice senão MINI_TICKER.close via require lazy do beholder) e capa MARKET-por-qty-base. Inerte sob HALT.
> 734	
> 735	**Cockpit — gate-FANTASMA da alt ELIMINADO** (`7ec6e75`, QA+TL+verif. adversarial, deployado+verificado): o agente notificava "baseline liberado p/ BNBUSDT c/ RSI>25 = incoerência". Raiz estrutural: `deriveGates` expunha `baseline=true` pra ALTS, que NÃO têm módulo baseline (gate de acumulação da alt = FARM). Fix: `baseline = flowGated ? baselineRaw : null` (só BTC expõe baseline; alt = null/n-a). `buyAllowed`/`farm` byte-idênticos (QA: tabela-verdade 60 casos). Verificado ao vivo: BTC `baseline=true`, BNB/LTC/ADA `null`. **TL: é direcional (payload afirmava gate de módulo inexistente), não perseguição-de-view.**
> 736	
> 737	**3 BLOQUEADORES do flip (`baf0f4b`, QA PASS + TL APPROVE + cético money-path PASS; design→verify e review→verify via workflow adversarial):**
> 738	1. **Teto:** `MAX_ORDER_NOTIONAL_USDT` 1500→**300** no `.env` (~2× a conta) + doutrina no exchange.js. ⚠️ verificador pegou que reativar **BTC Scalp Excess id38** (hoje `isActive=0`, vende BTC>1.0 a MARKET p/ +3 BTC) exige teto **symbol-aware** — caveat documentado.
> 739	2. **FARM_SELLING v1** (anti-empilhamento da venda no-loss do Farm): SKIP no place + SET por orderId + RELEASE por **match de orderId** em qualquer terminal — **BRAIN-independente** (mata a perma-trava do stop/start, superior ao HARVEST_SELLING). Sem migration/condition/reload. **Reconstrução-no-boot (loadFarmSellingLocks) + reconciliação partial→cancel DEFERIDAS** — gate: NÃO escalar `FARM_SIZE_MULT` (risco bounded: só remistura alt-wallet, NUNCA o cofre de BTC, nunca oversell além da carteira).
> 740	3. **TREND_QTY persistido via DERIVE-FROM-ORDERS** (não tabela nova — evitou o double-count): `getTrendPosition` espelha `getFarmPosition` (name LIKE 'Trend %'); `updateTrendPosition` recomputa (removeu accumulator + countedTrendFills → idempotente); `loadTrendPosition` no boot. Sem migration. Posição do golden não orfana num restart.
> 741	
> 742	**Parecer de READINESS (data-founded, 2 agentes: readiness + modos-de-falha) p/ o dono decidir o flip:** GO-CONDICIONADO, não GO cego. Money-path de ENTRADA + teto/reconcile sólidos; os 2 HIGH eram FARM_SELLING ausente + TREND_QTY não-persistido (AGORA FEITOS). Expectativa REAL = **≈ flat** (canary valida MECÂNICA — fill/fee/slippage reais nunca exercitados, 0 ordens mainnet —, NÃO lucro rápido). Canary recomendado: **um grupo só** (Farm alts id9-14 valida a mecânica em horas; OU Trend id6/7 valida o edge mas pode ficar inerte), NÃO os dois.
> 743	
> 744	**Estratégia BNB (pedido do dono):** a alavanca real NÃO é especular — é o **desconto de taxa BNB** (0,10%→0,075%, −25% em TODO par → abre margem no edge fino). MAS ligar BNB-fee **acorda o pré-req (c)** (P&L `net` para de descontar fee em BNB → painel mente otimista). ACOPLADOS: fix (c) ANTES de ligar BNB-fee. (O "no-loss" do Farm hoje também não é líquido — irmão do (c).)
> 745	
> 746	**Gotchas operacionais (DURÁVEIS):** (1) **`TRADING_HALT` e `MAX_ORDER_NOTIONAL` são lidos em `const` no LOAD do exchange.js → NÃO são kill-switch QUENTE.** Botão de pânico real = **`docker compose stop backend`**, não editar `.env`. O cap diário (e) precisa de refactor do guard p/ ler runtime — fecha os dois. (2) **Edit/Write do harness ENVENENA o dono do arquivo** (vira `ubuntu`); `.env` (600) ficou ilegível p/ gcrux → push + docker compose quebrariam. Detectei, `chown` de volta, gravei em `git-ownership-gotcha`. **SEMPRE `chown gcrux-tradeux` após editar arquivos do repo (esp. `.env`) antes de git/docker como gcrux.**
> 747	
> 748	**⚡ NEXT (falta p/ um flip responsável):** **(e) cap diário −5%** (dono APROVOU o valor) **+ refactor do guard p/ kill-switch quente** (resolve o HALT-frio junto) — É O PRÓXIMO ITEM, é só desenhar/implementar com QA/TL; depois **(c) P&L-BNB + BNB-fee** (acoplados, dono disse "ver depois"); aí **GO do dono** pro flip + canary de um-grupo-só. **Claude NÃO vira o `TRADING_HALT`.** Memórias atualizadas: `tradeux-mainnet-go-live`, `tradeux-harvester-experiment`, `tradeux-1m-scalping-and-cockpit`, `tradeux-trend-following`, `git-ownership-gotcha` + índice.
> 749	
> 750	### 🤝 SEAL — 2026-06-18 (Pré-reqs (e) e (c) ENTREGUES+DEPLOYADOS — fecha a fila de CÓDIGO do descongelamento)
> 751	**Sessão de descongelamento dirigida pelo dono (`/handson`→`/handoff`). `Vivo==master==origin==854bab5`. 4 containers up, `TRADING_HALT=true` intocado, 0 ordens mainnet, ~$148,84 USDT. PRs: 0 (trunk-based direct-to-master, com GO explícito do dono em cada pouso). Plan-mode + QA(qa-engineer)+TL(tech-lead) em cada item; secret-scan limpo.**
> 752	
> 753	**🎯 MARCO: TODOS os pré-reqs de CÓDIGO (a)-(e) do descongelamento estão FEITOS+DEPLOYADOS. Falta SÓ o GO do dono pro flip `TRADING_HALT=false` + canary de um-grupo-só.**
> 754	
> 755	**(e) CAP DIÁRIO −5% + KILL-SWITCH QUENTE** (`8ef1b69` + `1b639ce`; QA PASS-c/ressalvas + TL APPROVE):
> 756	- **`riskState.js` = fonte ÚNICA do HALT**, 3 fontes empilháveis: `env` (floor permanente de `TRADING_HALT`, só `.env`+restart derruba) · `manual` (operador) · `daily-cap` (auto-expira na virada UTC). Persiste `logs/risk_state.json`, fail-closed.
> 757	- **Guard do `exchange.js` lê `riskState.isHalted()` POR ORDEM** → o HALT deixou de ser `const` no load = **agora é QUENTE** (resolve o "HALT-frio"). 🔴 **GOTCHA ATUALIZADO: o botão de pânico quente NÃO é mais só `docker compose stop backend`** — agora `POST /system/halt {on:true,reason}` (operator-only, JWT; SEM MCP write tool — agente não flipa) trava sem restart; `POST /system/halt {on:false}` solta o manual (NÃO o env floor); `POST /system/daily-cap/reset` re-arma.
> 758	- **`dailyCapJob`** snapshota o **equity-TRADEABLE** na virada UTC e arma o HALT quando o drawdown bate −5% (block-ALL, inclusive venda protetiva → exige intervenção manual). Fail-safe a preço frio + alarme anti-silêncio (15min). **Earn/Locked `LD*` auto-excluído** (descoberto ao vivo: conta tem **LDGUN/LDBABY** — sem par USDT, deixavam o cap inerte). Knobs: `DAILY_CAP_ENABLED/DAILY_LOSS_CAP_PCT(0.05)/DAILY_CAP_CHECK_MS(60000)/DAILY_CAP_COLD_ALERT_MS/DAILY_CAP_IGNORE_ASSETS`. Vivo: baseline $148,84, piso $141,40, `tripped:false`.
> 759	- Cockpit/agent leem o estado quente via `/analysis/cockpit` (`env.tradingHalt` boolean preservado + `haltSource`/`haltReason` aditivos).
> 760	
> 761	**(c) P&L-BNB — net fee-inclusive ciente do lado** (`854bab5`; QA PASS-c/ressalvas + TL APPROVE):
> 762	- Helper único **`utils/feeCalc.computeNet`** unifica os 3 pontos de cálculo (`calcFillFinancials`, `app-em.processExecutionData`, `ordersController.syncOrder`): **VENDA `net=cummQuote−taxa(USDT-eq)`, COMPRA `net=cummQuote+taxa(USDT-eq)`**; taxa em quote→direto, base→×avgPrice, **BNB/outro→`getStableConversion`** (require LAZY, sem ciclo). Coluna nova **`orders.commissionAsset`** (migration `20260618170000`, idempotente dual-dialect, rodou no boot) → recompute/auditoria via `POST /orders/:id/sync`. Fail-safes: preço frio + `side` ausente → sem ajuste; guard `net>0`. Fecha o furo da taxa-em-BNB invisível no P&L → **BNB-fee agora SEGURO de ligar na UI Binance** (decisão do dono).
> 763	
> 764	**Gotchas/dívida (DURÁVEIS):** (1) Edit/Write do harness ENVENENA dono p/ `ubuntu` → `chown gcrux-tradeux` antes de git/docker (feito; repo limpo). (2) push via `GITHUB_TOKEN_API` (HTTPS) como gcrux — funciona sem a chave SSH do ubuntu e sem envenenar `.git`. (3) `ci-preflight.sh` rodado via `sudo bash -lc` dá FAIL falso em frontend/postgres por **`npx` fora do PATH** do shell — os passos que importam (lint de migration, MySQL migrate+seed idempotente, agent `--check`) PASSARAM; portabilidade da migration garantida por lint + padrão idêntico à `20260603170000`. (4) Dívida não-bloqueante: cap rollover c/ preço frio fica sem baseline até esquentar (auto-cura); cockpit break-even segue 0,20% (conservador com BNB-fee real ~0,15%); em par NÃO-USDT o `net` ficaria denominado no quote (irrelevante — só *USDT negocia).
> 765	
> 766	**⚡ NEXT:** acabou a fila de CÓDIGO. O próximo passo é **decisão/operação do DONO**: (1) ligar (ou não) o BNB-fee na UI da Binance; (2) dar o **GO pro flip `TRADING_HALT=false`** e rodar um **canary de um-grupo-só** (Farm alts id9-14 valida a mecânica em horas; Trend id6/7 valida o edge mas pode ficar inerte) — NÃO os dois. Expectativa REAL = **≈ flat** (canary valida fill/fee/slippage reais, nunca exercitados; 0 ordens mainnet — NÃO lucro rápido). **Claude NÃO vira o `TRADING_HALT`.** Memórias atualizadas: `tradeux-mainnet-go-live` (itens 9-10 + readiness) + índice `MEMORY.md`.
> 767	
> ```

## 🤖 Claude *(03:14:07)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/CLAUDE.md"
}
```

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

## 🤖 Claude *(03:14:18)*


## 🤖 Claude *(03:14:33)*

Contexto carregado. Aqui está o brief de entrada.

## 🤝 HANDSON — TradeUX (2026-06-19)

**Estado geral: 🟢 saudável / 🧊 MAINNET CONGELADO**

| Check | Resultado |
|---|---|
| Stack (compose) | ✅ 4 containers up — `db` (healthy, 3d), `backend` (12h), `frontend` (2d), `agent` (33h) |
| Site | ✅ `https://tradeux.gcrux.com` → **200** |
| Working tree | ✅ limpo (`git status` vazio) |
| Vivo == master == origin | ✅ **`854bab5`** (bate com o HANDOFF) |
| PRs abertos | **0** (trunk-based direct-to-master) |
| Trading | 🧊 **`TRADING_HALT=true`** · 0 ordens mainnet · ~**$148,84 USDT** |

### 🎯 Onde paramos (SEAL 2026-06-18)
**MARCO: TODOS os pré-reqs de CÓDIGO (a)–(e) do descongelamento estão FEITOS + DEPLOYADOS.** Os dois últimos a cair:
- **(e) Cap diário −5% + kill-switch QUENTE** (`8ef1b69`+`1b639ce`): `riskState.js` é a fonte única do HALT (env floor / manual / daily-cap); o guard lê `isHalted()` **por ordem** → o HALT agora é **quente**. Baseline vivo $148,84 / piso $141,40, `tripped:false`.
  - 🔴 **Gotcha novo:** o botão de pânico **não é mais** `docker compose stop backend` — agora é **`POST /system/halt {on:true}`** (operator-only, JWT, sem MCP write tool).
- **(c) P&L-BNB fee-inclusive** (`854bab5`): helper `feeCalc.computeNet` nos 3 pontos + coluna `orders.commissionAsset` → fecha o furo da taxa-em-BNB invisível. **BNB-fee agora seguro de ligar na UI Binance.**

### ⚡ O próximo passo é do DONO, não meu
Acabou a fila de código. Falta decisão/operação:
1. Ligar (ou não) o **BNB-fee** na UI da Binance.
2. Dar o **GO pro flip `TRADING_HALT=false`** + **canary de um-grupo-só** — Farm alts (id9-14) valida a mecânica em horas, **OU** Trend (id6/7) valida o edge mas pode ficar inerte. **Não os dois.**

**Expectativa REAL = ≈ flat.** O canary valida fill/fee/slippage reais (nunca exercitados — 0 ordens mainnet), **não** lucro rápido. **Claude NÃO vira o `TRADING_HALT`** — isso é GO explícito do dono.

### ⚠️ Lembretes de operação
- Git/docker **sempre** como `gcrux-tradeux`; Edit/Write do harness envenena o dono do arquivo → `chown gcrux-tradeux` antes de git/docker (esp. `.env`).
- id2/id3/id6/id7 são **runtime** (não seedadas) → reaplicar após `make nuke`.

Estou pronto. O que vamos atacar nesta sessão? Se for o canary/flip, lembro que preciso do **GO explícito** seu — eu não viro o HALT sozinho.

## 👤 User *(03:18:26)*

consegue analisar o mercado desde as ultimas alteracoes ate agora se tivesse virado a chave para comecar a criar ordens com o dinheiro real qual seria o resultado?

## 🤖 Claude *(03:18:53)*


## 🤖 Claude *(03:18:55)*

Boa pergunta — é uma análise contrafactual ("e se a chave tivesse sido virada em 18/06?") e é 100% read-only, então posso fazer sem tocar no `TRADING_HALT`. Vou reconstruir: (1) qual regime/mercado rolou desde o deploy do `854bab5`, (2) quais automações teriam disparado, (3) a que preços, e (4) estimar o P&L.

Deixa eu mapear onde estão os logs e o estado atual.

## 🤖 Claude *(03:18:56)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "An\u00e1lise contrafactual do flip",
  "summary": "E se TRADING_HALT=false em 18/06: que ordens teriam sa\u00eddo e qual o P&L"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Análise contrafactual do flip". Continue your current work.'}]
> ```

## 🤖 Claude *(03:18:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && sudo -n -u gcrux-tradeux bash -lc 'docker compose exec -T backend sh -lc \"ls -la logs/ 2>/dev/null | head -50\"' 2>&1 | head -60",
  "description": "List backend log files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 148
> drwxrwxr-x    1 root     root          4096 Jun 19 02:02 .
> drwxr-xr-x    1 root     root          4096 Jun 15 17:35 ..
> -rw-r--r--    1 root     root           716 Jun 19 02:02 A7.log
> -rw-r--r--    1 root     root            66 Jun 18 15:07 M1.log
> -rw-r--r--    1 root     root            75 Jun 18 15:07 M10.log
> -rw-r--r--    1 root     root            64 Jun 18 15:07 M3.log
> -rw-r--r--    1 root     root            75 Jun 18 15:07 M4.log
> -rw-r--r--    1 root     root            75 Jun 18 15:07 M8.log
> -rw-r--r--    1 root     root            75 Jun 18 15:07 M9.log
> -rw-r--r--    1 root     root            61 Jun 18 15:07 beholder.log
> -rw-r--r--    1 root     root           157 Jun 18 15:07 cockpit.log
> -rw-r--r--    1 root     root            74 Jun 19 00:00 daily_cap_snapshot.json
> -rw-r--r--    1 root     root           103 Jun 18 15:07 fair.log
> -rw-r--r--    1 root     root         19127 Jun 19 03:18 flow-capitulation.log
> -rw-r--r--    1 root     root         26140 Jun 19 03:18 flow.log
> -rw-r--r--    1 root     root          1883 Jun 19 03:07 funnel.log
> -rw-r--r--    1 root     root          1019 Jun 19 02:02 regime.log
> -rw-rw-r--    1 root     root         17908 Jun 19 03:17 system.log
> ```

## 🤖 Claude *(03:19:00)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sudo -n -u gcrux-tradeux bash -lc 'curl -s -m8 http://127.0.0.1:8090/ >/dev/null; echo \"---regime via backend---\"; docker compose exec -T backend sh -lc \"wget -qO- http://localhost:3001/api/analysis/regime-status 2>/dev/null || echo nofetch\"' 2>&1 | head -40",
  "description": "Probe regime-status endpoint"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ---regime via backend---
> nofetch
> ```

## 🤖 Claude *(03:19:12)*


## 🤖 Claude *(03:19:13)*

Logs ficam dentro do container. O backend bootou em 18/06 15:07 UTC (deploy do `854bab5`) e agora são ~03:18 de 19/06 — então a janela é de ~12h. Já vejo que a **A7.log** (Trend Sell BTC) teve evento. Vou ler os logs-chave.

## 🤖 Claude *(03:19:15)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sudo -n -u gcrux-tradeux bash -lc 'docker compose exec -T backend sh -lc \"echo \\\"==== regime.log ====\\\"; cat logs/regime.log; echo; echo \\\"==== A7.log ====\\\"; cat logs/A7.log; echo; echo \\\"==== funnel.log ====\\\"; cat logs/funnel.log\"' 2>&1 | head -120",
  "description": "Read regime, A7, funnel logs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ==== regime.log ====
> info: 2026-06-18T15:07:14.392Z - Estado de cross recarregado: ADAUSDT:above=false, BNBUSDT:above=false, BTCUSDT:above=true, LTCUSDT:above=true.
> info: 2026-06-18T15:07:14.393Z - Regime job iniciado (intervalo 300000ms, klines 1h).
> info: 2026-06-18T15:07:14.837Z - BTCUSDT:REGIME => mixed (ADX 23.2 intermediário, sem viés claro)
> info: 2026-06-18T15:07:15.151Z - LTCUSDT:REGIME => trend (ADX 33.8 >= 25 (tendência forte))
> info: 2026-06-18T15:07:15.438Z - BNBUSDT:REGIME => trend (ADX 32.4 >= 25 (tendência forte))
> info: 2026-06-18T15:07:15.716Z - ADAUSDT:REGIME => trend (ADX 40.3 >= 25 (tendência forte))
> info: 2026-06-18T16:02:14.682Z - BTCUSDT:REGIME => trend (ADX 26.8 >= 25 (tendência forte) [histerese: prev=mixed])
> info: 2026-06-19T02:02:14.771Z - BTCUSDT: SMA DEATH cross (50/200) — disparando automação de trend
> info: 2026-06-19T02:02:14.779Z - BTCUSDT: trend => {"type":"error","text":"Error at evalDecision for 'Trend Sell BTCUSDT SMA50/200': Error: There is no BTC in your wallet to place a sell."}
> 
> ==== A7.log ====
> info: 2026-06-19T02:02:14.774Z - Beholder evaluated a condition at automation: Trend Sell BTCUSDT SMA50/200 => MEMORY['BTCUSDT:TREND_CROSS_1h']==='death'
> info: 2026-06-19T02:02:14.778Z
> error: There is no BTC in your wallet to place a sell. {"stack":"Error: There is no BTC in your wallet to place a sell.\n    at calcQty (/app/src/beholder.js:210:27)\n    at placeOrder (/app/src/beholder.js:485:26)\n    at process.processTicksAndRejections (node:internal/process/task_queues:103:5)\n    at async evalDecision (/app/src/beholder.js:871:28)\n    at async Promise.all (index 1)\n    at async testAutomations (/app/src/beholder.js:919:19)\n    at async Timeout.runOnce [as _onTimeout] (/app/src/regimeJob.js:142:41)"}
> 
> ==== funnel.log ====
> info: 2026-06-18T15:07:14.328Z - Funnel job iniciado em modo SHADOW (OBSERVAÇÃO) (intervalo 3600000ms; baseline $10000).
> info: 2026-06-18T15:07:15.101Z - [shadow] USDT=148.84 | reserva BTC=0.000000 (preço n/d) | sem excedente (baseline $10000.00).
> info: 2026-06-18T16:07:14.880Z - [shadow] USDT=148.84 | reserva BTC=0.000000 (~$0.00) @ $62596.16 | sem excedente (baseline $10000.00).
> info: 2026-06-18T17:07:14.916Z - [shadow] USDT=148.84 | reserva BTC=0.000000 (~$0.00) @ $62528.59 | sem excedente (baseline $10000.00).
> info: 2026-06-18T18:07:14.899Z - [shadow] USDT=148.84 | reserva BTC=0.000000 (~$0.00) @ $62686.00 | sem excedente (baseline $10000.00).
> info: 2026-06-18T19:07:14.877Z - [shadow] USDT=148.84 | reserva BTC=0.000000 (~$0.00) @ $62697.66 | sem excedente (baseline $10000.00).
> info: 2026-06-18T20:07:14.879Z - [shadow] USDT=148.84 | reserva BTC=0.000000 (~$0.00) @ $63147.99 | sem excedente (baseline $10000.00).
> info: 2026-06-18T21:07:14.881Z - [shadow] USDT=148.84 | reserva BTC=0.000000 (~$0.00) @ $63094.88 | sem excedente (baseline $10000.00).
> info: 2026-06-18T22:07:14.876Z - [shadow] USDT=148.84 | reserva BTC=0.000000 (~$0.00) @ $62922.00 | sem excedente (baseline $10000.00).
> info: 2026-06-18T23:07:14.872Z - [shadow] USDT=148.84 | reserva BTC=0.000000 (~$0.00) @ $62835.99 | sem excedente (baseline $10000.00).
> info: 2026-06-19T00:07:14.877Z - [shadow] USDT=148.84 | reserva BTC=0.000000 (~$0.00) @ $62909.05 | sem excedente (baseline $10000.00).
> info: 2026-06-19T01:07:14.881Z - [shadow] USDT=148.84 | reserva BTC=0.000000 (~$0.00) @ $63059.53 | sem excedente (baseline $10000.00).
> info: 2026-06-19T02:07:14.881Z - [shadow] USDT=148.84 | reserva BTC=0.000000 (~$0.00) @ $63056.14 | sem excedente (baseline $10000.00).
> info: 2026-06-19T03:07:14.884Z - [shadow] USDT=148.84 | reserva BTC=0.000000 (~$0.00) @ $62952.01 | sem excedente (baseline $10000.00).
> ```

## 🤖 Claude *(03:19:47)*


## 🤖 Claude *(03:19:48)*

O quadro está ficando claro. Deixa eu confirmar no `system.log` se houve QUALQUER tentativa de ordem (farm das alts, dip de RSI) bloqueada pelo HALT, e checar o flow.

## 🤖 Claude *(03:19:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sudo -n -u gcrux-tradeux bash -lc 'docker compose exec -T backend sh -lc \"\necho \\\"==== grep ordens/HALT/place/calcQty/sell/buy no system.log ====\\\";\ngrep -iE \\\"halt|placeorder|calcqty|sell|buy|fill|order placed|MAX_ORDER|notional|reject|-2010|-1013|cross|farm|trend\\\" logs/system.log | tail -40;\necho;\necho \\\"==== contagem de linhas por nivel no system.log ====\\\";\ngrep -ciE \\\"error\\\" logs/system.log; \necho \\\"--- todas as automa\u00e7\u00f5es que logaram (A*.log) ---\\\";\nls -la logs/ | grep -E \\\"A[0-9]+\\.log\\\";\n\"' 2>&1 | head -80",
  "description": "Grep system.log for order attempts and HALT blocks"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ==== grep ordens/HALT/place/calcQty/sell/buy no system.log ====
> info: 2026-06-18T13:47:05.779Z - [riskState] inicializado — env floor=true · manual=false · daily-cap=false · halted=true.
> info: 2026-06-18T13:50:02.136Z - [riskState] inicializado — env floor=true · manual=false · daily-cap=false · halted=true.
> info: 2026-06-18T13:50:11.142Z - [riskState] inicializado — env floor=false · manual=false · daily-cap=false · halted=false.
> info: 2026-06-18T13:55:43.299Z - [riskState] inicializado — env floor=true · manual=false · daily-cap=false · halted=true.
> info: 2026-06-18T15:07:14.085Z - [riskState] inicializado — env floor=true · manual=false · daily-cap=false · halted=true.
> info: 2026-06-18T15:07:14.538Z - FARM_DCA[LTCUSDT] carregado no boot: qty=0, cost=0
> info: 2026-06-18T15:07:14.554Z - FARM_DCA[BNBUSDT] carregado no boot: qty=0, cost=0
> info: 2026-06-18T15:07:14.560Z - FARM_DCA[ADAUSDT] carregado no boot: qty=0, cost=0
> 
> ==== contagem de linhas por nivel no system.log ====
> 0
> --- todas as automações que logaram (A*.log) ---
> -rw-r--r--    1 root     root           716 Jun 19 02:02 A7.log
> ```

## 🤖 Claude *(03:20:33)*


## 🤖 Claude *(03:20:51)*

Análise completa. O resultado é definitivo e, honestamente, **um pouco anticlimático** — mas é exatamente o que a tese do HANDOFF previa.

## 📊 Contrafactual: e se `TRADING_HALT=false` em 18/06?

**Janela analisada:** deploy do `854bab5` (18/06 15:07 UTC) → agora (~19/06 03:18 UTC) ≈ **12h**.

### Resultado: **FLAT. $148,84 → $148,84. Zero ordens executadas.**

Mesmo com a chave virada, **nenhuma ordem real teria saído.** Não por bug — por ausência de gatilho de entrada num mercado de lado.

### O que o mercado fez (BTC, via snapshots do funil)
| Hora (UTC) | BTC |
|---|---|
| 16:07 | $62.596 |
| 20:07 | **$63.148** (topo) |
| 00:07 | $62.909 |
| 03:07 | $62.952 |

BTC andou de lado num range de **~1%** ($62.528–$63.148). Regime virou `mixed`→`trend` às 16:02, mas **sem golden cross novo**.

### Por que zero ordens (item por item)
1. **Trend Buy BTC (id6)** — dispara em *golden cross*. No boot já estávamos `above=true` (sem cross novo) → **não disparou**. Sem compra = sem posição.
2. **Trend Sell BTC (id7 / A7)** — 🎯 **único evento da janela**: **DEATH cross 50/200 às 02:02**. Tentou vender, mas a conta é 100% USDT → `"There is no BTC in your wallet to place a sell"`. **No-op mesmo com HALT off.**
3. **Farm alts (id9-14)** — compram em dip `RSI<35`. LTC/BNB/ADA estavam em `trend` (gate aberto), mas **nenhuma alt furou RSI<35** → nenhum `A9-A14.log` → não disparou. Buckets `FARM_DCA` carregados vazios (`qty=0`).
4. **Trend alts (id15-20)** — sem cross SMA novo nas alts na janela → inertes.
5. Funil em **shadow**, baseline id2 e harvester (id22-25) **desativados**.

`system.log`: **0 erros**, `riskState` `halted=true` o tempo todo. Só **A7.log** registrou evento.

### A leitura honesta pro dono
Isto **valida a tese**: expectativa = **≈ flat**. O ponto não-óbvio é *por que* seria flat — **a conta começa em caixa (USDT) e o módulo que ABRE posição não recebeu gatilho**. Num período de lado, o sistema corretamente **não força trade** (que é o maior risco — sangrar fee à toa).

Consequência prática pro **canary**: virar a chave num mercado parado pode te deixar **horas/dias sem nenhuma ordem** — não dá pra exercitar fill/fee/slippage sem um sinal. As duas saídas:
- **Esperar um gatilho de entrada** (golden cross do BTC ou dip RSI<35 numa alt) — passivo, pode demorar.
- Escolher o grupo **Farm-alts** como canary (entra em dips menores, mais provável de disparar) em vez do Trend-BTC (que neste período ficaria 100% inerte).

Quer que eu monte um **monitor** (ex.: `/loop`) que me acorda quando aparecer o primeiro gatilho real de entrada — pra você decidir o flip *no momento* em que o canary teria algo pra fazer, e não no escuro? (Continuo sem virar o HALT — isso é GO seu.)

## 👤 User *(03:28:33)*

nao eu quero que voce crie um sistema de geracao e ativacao de estrategias e metodos de trade para operar em todos os periodos e principalmente no que estamos e nos que vamos ou temos a tendencia de entrar a curto prazo. ensei tambem em guardar em base de conhecimento todos os tipos de padores e sinais do mercaod trade. E por fim verificar e usar o poder total do beholder que é ver simultaneamente todos as criptos monitoradas, ou seja todos os monitores sendo processados com inteligencia artifical de baixa latencia para decidir ordens e obter lucros diarios

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-18 - d7c8c9da-f4e1-4286-b1f5-5d9a47531010]]
%% --- TIMELINE END --- %%

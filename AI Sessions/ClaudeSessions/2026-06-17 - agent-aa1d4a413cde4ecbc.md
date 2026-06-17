# Session agent-aa1d4a413cde4ecbc
**Date:** 2026-06-17 | **Session ID:** `agent-aa1d4a413cde4ecbc`

---

## 👤 User *(16:46:48)*

Revise um fix de backend+MCP NÃO-COMMITADO no working tree do TradeUX. Veredito: PASS / PASS COM RESSALVAS / FAIL, com achados severizados e testes concretos.

## Contexto
O agente LLM notificou o dono no Telegram alegando "incoerência": `buyGate de baseline liberado para BNBUSDT apesar do RSI_1m ~53 > 25". Isso é falso-flag da classe GATE≠TRIGGER (o gate é doutrina de regime/fluxo, NÃO lê RSI; RSI é o GATILHO) — JÁ documentada. PIOR: pra uma ALT (BNBUSDT) o módulo `baseline` **nem é o operativo** — o gate de acumulação da alt é o FARM (`buyAllowed=farm`). O cockpit calculava e expunha um `baseline=true` pra alts (gate-FANTASMA de um módulo que a alt não tem), que o agente lia como gate vivo e flagava.

**Fix:** em `deriveGates` (`backend/src/cockpitJob.js`), expor `baseline` SÓ pra símbolo flow-gated (BTC); pra não-flow-gated (alts) `baseline=null` (n/a). `buyAllowed` e `farm` ficam INTACTOS (buyAllowed usa um `baselineRaw` interno pro BTC). Mais uma nota na descrição do tool MCP `tradeux_get_cockpit` explicando o null.

## Diff
```diff
# backend/src/cockpitJob.js — deriveGates
     const farm = regimeOk && regime !== 'trend';
-    const baseline = farm && flowOk;
     const trend = regimeOk;
     const flowGated = !!symbol && FLOW_GATED.has(String(symbol).toUpperCase());
-    const buyAllowed = flowGated ? baseline : farm;
+    const baselineRaw = farm && flowOk;
+    // baseline SÓ p/ flow-gated (BTC); alt não tem módulo baseline → null (n/a); buyAllowed/farm intactos
+    const baseline = flowGated ? baselineRaw : null;
+    const buyAllowed = flowGated ? baselineRaw : farm;
# return { ...farm, baseline, trend, ..., buyAllowed, reason, doctrine:true }  (inalterado)

# tradeux-mcp/src/index.js:215 — só adiciona à descrição do tool uma frase sobre baseline=null p/ alts.
```

## Verifique (não exaustivo)
1. **`buyAllowed` permanece idêntico** ao comportamento anterior pra TODOS os casos (BTC flow-gated usa baselineRaw==antigo baseline; alt usa farm). Prove com tabela: {BTC, alt} × {regime range/mixed/trend/bear} × {flowOk t/f}.
2. **Nenhum consumidor quebra com `baseline=null`**: rastreie quem lê `gates.baseline` — MCP (`index.js:228` projeta no buyGate), frontend (`frontend/src/private/Cockpit/Cockpit.js` — confirme se LÊ o valor `baseline` ou só usa farm/buyAllowed/labels), e o snapshot gravado em `MEMORY['<sym>:COCKPIT'].gates` por `cockpitJob.runOnce` (algum leitor de get_memory que faça `if (gates.baseline)`?). null deve ser tratado como n/a, sem virar `false`-falso-positivo nem quebrar render.
3. **`freshen` e `runOnce`** ambos chamam `deriveGates` — confirme que a mudança vale nos dois caminhos (read-path freshened e snapshot do job).
4. **`reason`** das alts continua coerente (linha "FARM liberado, SEM filtro de fluxo")? As linhas 102-103 ("farm/baseline em CAIXA" genérico) ficaram inconsistentes com baseline=null? (provável nice-to-have, avalie severidade.)
5. Símbolos flow-gated extras via env `COCKPIT_FLOW_GATED_SYMBOLS` mantêm baseline. 

Leia os arquivos. Retorne veredito + achados + testes concretos (incl. como simular deriveGates com BTC vs alt).

## 🤖 Claude *(16:46:51)*

Vou carregar o contexto e revisar o fix.

## 🤖 Claude *(16:46:52)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/HANDOFF.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>[Truncated: PARTIAL view — showing lines 1-275 of 726 total (56096 tokens, cap 25000). Call Read with offset=276 limit=275 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>
> 
> 1	# TradeUX — HANDOFF (single source of truth)
> 2	
> 3	> ShakeHands continuity doc. `/handson` reads this FIRST. Newest record at the bottom.
> 4	> Project: **TradeUX** — Beholder-based multi-coin Binance Spot bot + LLM agent (**mainnet/testnet dual-env**).
> 5	> Updated: **2026-06-16** · Phase: **GO-LIVE MAINNET — CONGELADO (`TRADING_HALT=true`)** · Meta: **realista ≈ flat com ~$150** (o +3 BTC era do testnet) · Vivo==master==origin==**`0b1554d`**
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
> 267	da automação. **Descoberta-chave (custou tempo):** logs de monitor vão p/ `logs/M<id>.log`, NÃO `system.log` (logger
> 268	por categoria) → memória nova `tradeux-logger-per-category-files`. Gate QA+TL devolveu 4 achados de dinheiro (empilhamento
> 269	de OCO, órfã em falha de persist, match cancel, semântica do stop) → **corrigi todos** (guard anti-empilhamento, auto-cancel,
> 270	`origClientOrderId`, cancel só no delete) e re-validei → PASS/APPROVE. (2) **E2E pelo navegador** (Claude-in-Chrome, no
> 271	Chrome do Gabriel) → relatório `~/E2E-REPORT-TradeUX.md`. Achado nº1: **~74% das ordens MARKET com `net`/`avgPrice` NULL**
> 272	(P&L/custo-base furados; Reports mostrava 0 mesmo lucrando). (3) **Fix P&L ✅** (`d74fac0`): `calcFillFinancials` computa
> 273	net/avgPrice/commission **no insert** do fill (não depende do stream) + trava OCO=SELL no template. (4) **Painel P&L ✅**
> 274	(`9a5f989`): Reports default **USDT** (consertou Reports=0 E Market 24h do Dashboard) + end-date inclusivo + **leitura em
> 275	BTC** ("≈ X BTC", `profitBtc` no backend). (5) **Painel Intelligence ✅** (`1fa6235`): `/intelligence` mostra regime de
> ```

## 🤖 Claude *(16:46:52)*


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

## 🤖 Claude *(16:46:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' status && echo \"---DIFF---\" && git -C /home/gcrux-tradeux/tradeux -c safe.directory='*' diff",
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
> ---DIFF---
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

## 🤖 Claude *(16:46:56)*

Vou ler os arquivos relevantes para rastrear todos os consumidores de `gates.baseline`.

## 🤖 Claude *(16:46:56)*


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

## 🤖 Claude *(16:46:59)*

Agora vou rastrear os consumidores: MCP `index.js` (projeção do buyGate), frontend `Cockpit.js`, e qualquer leitor de `gates.baseline`.

## 🤖 Claude *(16:47:00)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/tradeux-mcp/src/index.js",
  "offset": 216,
  "limit": 40
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 216	  {},
> 217	  async () => {
> 218	    const d = await api.get(`/analysis/cockpit`);
> 219	    const out = { env: d.env || null, enabled: d.enabled, symbols: {} };
> 220	    for (const [sym, c] of Object.entries(d.symbols || {})) {
> 221	      const dist = c.dist || {}, ev = c.ev || {}, mc = c.mc || {}, gates = c.gates || {};
> 222	      out.symbols[sym] = {
> 223	        price: c.price, regime: c.regime,
> 224	        flow: c.flow ? { imbalance: c.flow.imbalance, toxicity: c.flow.toxicity, ageSec: Number.isFinite(c.flow.ageMs) ? Math.round(c.flow.ageMs / 1000) : null } : null,
> 225	        medAbsMovePct: dist.medAbsMovePct, sigmaPct: dist.sigmaPct, pHitBreakevenPct: dist.pHitBreakevenPct,
> 226	        evNetPct: ev.netPct, breakevenPct: ev.breakevenPct,
> 227	        mc: { p10: mc.p10, p50: mc.p50, p90: mc.p90, horizonMin: mc.horizonMin, driftless: true },
> 228	        buyGate: { allowed: gates.buyAllowed, reason: gates.reason, flowFresh: gates.flowFresh, flowGated: gates.flowGated, farm: gates.farm, baseline: gates.baseline },
> 229	        stale: c.stale,
> 230	      };
> 231	    }
> 232	    return out;
> 233	  }
> 234	);
> 235	
> 236	// ----------------------------------------------------------------------------
> 237	// LEITURA — ordens, automações, monitores, templates
> 238	// ----------------------------------------------------------------------------
> 239	
> 240	readTool(
> 241	  "tradeux_list_orders",
> 242	  "Histórico de ordens (paginado). Pode filtrar por símbolo.",
> 243	  {
> 244	    symbol: z.string().optional().describe("Par, ex: BTCUSDT"),
> 245	    page: z.number().int().positive().optional().describe("Página (default 1)"),
> 246	  },
> 247	  ({ symbol, page }) => api.get(symbol ? `/orders/${symbol.toUpperCase()}` : "/orders", { page })
> 248	);
> 249	
> 250	readTool(
> 251	  "tradeux_get_last_orders",
> 252	  "As últimas 10 ordens preenchidas (FILLED).",
> 253	  {},
> 254	  () => api.get("/orders/last")
> 255	);
> ```

## 🤖 Claude *(16:47:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"\\.baseline\\|baseline\" /home/gcrux-tradeux/tradeux/tradeux-mcp/src/ /home/gcrux-tradeux/tradeux/frontend/src/ /home/gcrux-tradeux/tradeux/backend/src/ 2>/dev/null | grep -iv \"node_modules\" | grep -i baseline",
  "description": "Find all references to baseline across MCP, frontend, backend"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrux-tradeux/tradeux/tradeux-mcp/src/index.js:215:  "Cockpit Intelligence (READ-ONLY): snapshot que a brain computa por simbolo a partir de klines 1m REAIS da mainnet — distribuicao de retornos (mediana |move|, sigma, % de moves >= break-even de fee), EV/trade NET de fee (mecanica da distribuicao 1m; costuma ser <=0 = por que scalping de 1m sangra taxa), banda Monte Carlo DRIFTLESS (p50 == preco, NAO previsao) e o snapshot regime/fluxo + estado dos gates de COMPRA por simbolo. Tambem informa o AMBIENTE real (env.useTestnet) e se o trading esta congelado (env.tradingHalt). Use para REPORTAR ao operador o estado MECANICO do mercado e a coerencia dos gates; NAO e sinal de trade nem forecast. ATENCAO: os gates (buyGate/farm/baseline/trend, doctrine=true) sao a DOUTRINA por regime (o que a estrategia FARIA), NAO confirmam que a automacao correspondente esta ATIVA/ligada (ex.: a baseline id2 esta isActive=0) — o gate VIVO mora na condition da automacao no banco. Reporte como doutrina, nao como estado vivo, e o fluxo e fail-closed (stale/ausente => CAIXA). O campo baseline SO se aplica a simbolo flow-gated (BTC); para ALTS vem null (n/a) — o gate de acumulacao da alt e o farm, entao NAO trate baseline=null (nem farm aberto com RSI>35/25) como incoerencia: o gate e a DOUTRINA de regime/fluxo, o RSI e o GATILHO (gate != gatilho). O regime/fluxo do cockpit sao lidos das MESMAS chaves MEMORY['REGIME']/['FLOW'] que os oraculos vivos (tradeux_get_regime/tradeux_get_oracle_state) — NAO uma fonte paralela; o fluxo carrega flow.ageSec (idade em segundos). Por isso NAO trate diferenca cockpit×oraculo-vivo como contradicao: compare pela idade (um imbalance velho mais negativo que o vivo e o MESMO sinal em instantes diferentes) e, no regime, use o gate.regime histeretico.",
> /home/gcrux-tradeux/tradeux/tradeux-mcp/src/index.js:228:        buyGate: { allowed: gates.buyAllowed, reason: gates.reason, flowFresh: gates.flowFresh, flowGated: gates.flowGated, farm: gates.farm, baseline: gates.baseline },
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/cockpit.css:49:.cockpit .cx-brand { display: flex; align-items: baseline; gap: 12px; }
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/cockpit.css:99:.cockpit .cx-sub { display: flex; align-items: baseline; gap: 14px; margin-top: 6px; flex-wrap: wrap; }
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/cockpit.css:164:.cockpit .cx-candle-head { display: flex; align-items: baseline; gap: 12px; margin-bottom: 8px; }
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js:379:                        // só a baseline BTC (flowGated=true) é bloqueada por fluxo; o FARM das alts NÃO gateia por
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js:386:                        // trend o farm/baseline ficam em CAIXA). Usa cpg.farm (backend); fallback exclui os 3.
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js:395:                          ? `fluxo ${flowOk ? 'ok' : 'capitulação'} (imbalance ${imb != null ? imb.toFixed(2) : '—'}) — gateia a baseline BTC`
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js:412:                <div className="cx-note">Cada ponte acende quando o gate de COMPRA do símbolo abre: <b>BTC (baseline)</b> = regime ≠ bear/trend <b>E</b> fluxo não-capitulação; <b>alts (farm)</b> = só regime ≠ bear/trend (o fluxo é <b>informativo·i</b>, não gateia). "go" = condições prontas; a ordem em si segue gateada e sob HALT.</div>
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js:425:                <div className="cx-line"><span className="l"><span className="cx-seal real" /> Gate acumulação BTC <span className="cx-flat" style={{ fontSize: '0.66rem' }}>(farm/baseline)</span></span><span className={`v cx-mono ${cpBtc && cpBtc.gates ? (cpBtc.gates.buyAllowed ? 'cx-up' : 'cx-down') : ''}`} title={cpBtc && cpBtc.gates ? cpBtc.gates.reason : ''}>{cpBtc && cpBtc.gates ? (cpBtc.gates.buyAllowed ? 'GO' : 'CAIXA') : '—'}</span></div>
> /home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js:87:// Símbolos cujo módulo de acumulação gateia por FLUXO: SÓ a baseline BTC (id2). Default BTCUSDT; env sobrescreve.
> /home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js:99:    const baselineRaw = farm && flowOk;                 // módulo baseline (BTC id2): farm + filtro de fluxo (fail-closed)
> /home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js:100:    // baseline SÓ existe p/ símbolo flow-gated (BTC). Pra ALT não há módulo baseline (o gate de acumulação é o FARM):
> /home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js:101:    // expor baseline=true p/ alt é um gate-FANTASMA que o agente lê como "incoerência" (baseline aberto c/ RSI>25).
> /home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js:102:    // → baseline=null (n/a) p/ não-flow-gated; buyAllowed e farm ficam INTACTOS (buyAllowed usa baselineRaw p/ BTC).
> /home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js:103:    const baseline = flowGated ? baselineRaw : null;
> /home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js:104:    const buyAllowed = flowGated ? baselineRaw : farm;  // alt: farm (sem fluxo); símbolo flow-gated (BTC): baseline
> /home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js:106:    if (!regimeOk) reason = `regime=${regime || 'unknown'}: acumulação em CAIXA (farm/baseline e trend parados)`;
> /home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js:107:    else if (regime === 'trend') reason = 'regime=trend: farm/baseline em CAIXA (correto); trend compra no golden cross';
> /home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js:112:    else if (!flowFresh) reason = 'fluxo stale/ausente → conservador (fail-closed, como a id2): baseline BTC NÃO liberada';
> /home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js:113:    else if (!flowOk) reason = `fluxo em capitulação (imbalance ${flow.imbalance} < ${FLOW_BUY_MIN}): baseline BTC veta o dip`;
> /home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js:114:    else reason = `regime=${regime} (mean-reversion: range/mixed) + fluxo ok: baseline BTC liberada`;
> /home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js:116:    // que a automação correspondente (ex.: baseline id2, hoje isActive=0) está ATIVA — o gate VIVO mora na
> /home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js:118:    return { regime, regimeOk, flowOk, flowFresh: !!flowFresh, flowBuyMin: FLOW_BUY_MIN, flowGated, farm, baseline, trend, harvesterUngated: true, buyAllowed, reason, doctrine: true };
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:11: * baseline de capital de trabalho for configurado — o EXCEDENTE de USDT que escoaria pra BTC ao preço
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:65:let RUNTIME_BASELINE = null; // baseline de USDT setado em runtime na saída do bear (sobrepõe BASELINE_USDT no shadow)
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:111:        // baseline efetivo: o setado em runtime na saída do bear (armador da Fase 4) tem precedência sobre o env.
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:112:        const baseline = RUNTIME_BASELINE != null ? RUNTIME_BASELINE : BASELINE_USDT;
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:114:        // excedente a escoar (só se um baseline foi configurado; senão v1 apenas observa)
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:116:        if (baseline > 0) {
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:117:            excessUsdt = Math.max(0, usdtFree - baseline);
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:121:        LAST = { usdtFree, btcReserve, btcReserveUsd, price, baseline, excessUsdt, btcWouldBuy };
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:126:        if (baseline > 0 && btcWouldBuy > 0) {
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:128:            else logger('funnel', `[shadow] ${base} → escoaria $${excessUsdt.toFixed(2)} acima do baseline → +${btcWouldBuy.toFixed(6)} ${BASE_ASSET} (NÃO comprado: shadow).`);
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:131:            logger('funnel', `[shadow] ${base}${baseline > 0 ? ` | sem excedente (baseline $${baseline.toFixed(2)})` : ' | observando (sem baseline)'}.`);
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:140://  (1) usa SÓ o baseline FIXO do env (BASELINE_USDT), NUNCA o RUNTIME_BASELINE auto-armado pela Fase 4 — senão
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:141://      um depósito DURANTE a janela de observação viraria "excedente" e seria drenado mesmo abaixo do baseline;
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:147:        logger('funnel', '[LIVE] compra RECUSADA: FUNNEL_BASELINE_USDT (baseline FIXO) não configurado.');
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:152:        logger('funnel', `[LIVE] sem excedente sobre o baseline fixo $${BASELINE_USDT.toFixed(2)} (USDT=$${usdtFree.toFixed(2)}); nada a escoar.`);
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:162:        logger('funnel', `[LIVE] Escoando $${buyUsdt.toFixed(2)} (excedente $${liveExcess.toFixed(2)} sobre baseline $${BASELINE_USDT.toFixed(2)}; teto $${MAX_BUY_USDT.toFixed(2)}) p/ ${BASE_ASSET}...`);
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:203:// Combina: (1) NOTIFICA a transição; (2) pré-arma o funil SHADOW (snapshot do USDT vira o baseline runtime → o
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:206:// USDT, reserva BTC, preço, lucro desde a saída do bear (USDT−baseline) e quanto escoaria. NÃO compra nada (shadow).
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:230:        await notify(snap ? snap.settings : null, `🔔 [FASE4] Saída do BEAR (${reason}). Farm/trend RETOMAM (gate de regime liberado). Janela de observação de ${hrs}h ARMADA · baseline USDT=$${usdt.toFixed(2)} · reserva ${BASE_ASSET}=${(snap ? snap.btcReserve : 0).toFixed(6)}. Capturando os dados pra calibrar a Fase 4 (funil ao vivo). NÃO compra ainda (shadow).`);
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:280:    logger('funnel', `Funnel job iniciado em modo ${isLive ? 'LIVE (COMPRAS REAIS)' : 'SHADOW (OBSERVAÇÃO)'} (intervalo ${REFRESH_MS}ms; baseline $${BASELINE_USDT || '—'}).`);
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:292:        maxBuyUsdt: MAX_BUY_USDT, baselineUsdt: BASELINE_USDT,
> /home/gcrux-tradeux/tradeux/backend/src/funnelJob.js:301:            baseline: obsBaseline,
> /home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js:32:            source: `MEMORY['${symbol}:REGIME'] (histerético; valor OPERATIVO que farm/trend/baseline gateiam)`,
> ```

## 🤖 Claude *(16:47:07)*

The `funnelJob.js` references to `baseline` are a different variable (USDT working-capital baseline), unrelated. Now let me read the frontend `Cockpit.js` around the bridge-rendering logic and the lines that consume `gates`, to confirm whether it reads `gates.baseline` directly.

## 🤖 Claude *(16:47:08)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js",
  "offset": 360,
  "limit": 75
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
> 430	                      <div className="cx-line"><span className="l"><span className="cx-seal real" /> Ciclos do agente</span><span className="v cx-mono">{agent.kpis.cycles != null ? agent.kpis.cycles : '—'}{agentLastMs != null ? `  ·  ${fmtAge(agentLastMs)}${agentStale ? ' STALE' : ''}` : ''}</span></div>
> 431	                      <div className="cx-line"><span className="l"><span className="cx-seal real" /> Tokens (total)</span><span className="v cx-mono">{agent.kpis.tokens && agent.kpis.tokens.total != null ? num(agent.kpis.tokens.total).toLocaleString() : '—'}</span></div>
> 432	                      <div className="cx-line"><span className="l"><span className="cx-seal real" /> Custo estimado</span><span className="v cx-mono">{agent.kpis.estCostUSD != null ? '$' + agent.kpis.estCostUSD : '—'}</span></div>
> 433	                    </React.Fragment>}
> 434	              </div>
> ```

## 🤖 Claude *(16:47:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"gates\\.\\|\\.gates\\b\\|COCKPIT\\|:COCKPIT\" /home/gcrux-tradeux/tradeux/backend/src/ /home/gcrux-tradeux/tradeux/tradeux-agent/src/ /home/gcrux-tradeux/tradeux/frontend/src/ 2>/dev/null | grep -iv node_modules | grep -i \"baseline\\|gates\" ",
  "description": "Find all gates.* reads across backend, agent, frontend"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js:15: * a banda MC é DRIFTLESS (p50 ≡ preço). `gates.buyAllowed` é a VIEW do cockpit (limiar COCKPIT_FLOW_BUY_MIN
> /home/gcrux-tradeux/tradeux/backend/src/utils/indexes.js:84:    COCKPIT: 'COCKPIT' // analytics READ-ONLY por símbolo (cockpitJob): distribuição de retornos 1m, EV net-de-fee, tail, banda MC driftless, snapshot regime/flow + estado dos gates de compra. NÃO gateia nada — o agente LÊ/REPORTA via MEMORY/MCP. Fonte = klines mainnet (mercado real), independe de useTestnet.
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js:378:                        // Fonte de verdade = gate SYMBOL-AWARE do cockpit (cp.symbols[s].gates, commit 8884bd3):
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js:382:                        const cpg = cps.gates || {};
> /home/gcrux-tradeux/tradeux/frontend/src/private/Cockpit/Cockpit.js:425:                <div className="cx-line"><span className="l"><span className="cx-seal real" /> Gate acumulação BTC <span className="cx-flat" style={{ fontSize: '0.66rem' }}>(farm/baseline)</span></span><span className={`v cx-mono ${cpBtc && cpBtc.gates ? (cpBtc.gates.buyAllowed ? 'cx-up' : 'cx-down') : ''}`} title={cpBtc && cpBtc.gates ? cpBtc.gates.reason : ''}>{cpBtc && cpBtc.gates ? (cpBtc.gates.buyAllowed ? 'GO' : 'CAIXA') : '—'}</span></div>
> ```

## 🤖 Claude *(16:47:14)*

The frontend (`Cockpit.js`) reads `cpg.farm`, `cpg.flowGated`, `cpg.flowBuyMin`, `cpg.buyAllowed` — but never `cpg.baseline`. So the frontend is unaffected. Now let me check the agent's SYSTEM_PROMPT for any literal reference to `baseline` in cockpit reporting, and confirm there's no consumer reading the COCKPIT snapshot via `get_memory` that does `if (gates.baseline)`.

## 🤖 Claude *(16:47:15)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"baseline\\|COCKPIT\\|cockpit\\|gates\" /home/gcrux-tradeux/tradeux/tradeux-agent/src/ 2>/dev/null | grep -iv node_modules | grep -i \"baseline\\|cockpit\"",
  "description": "Search agent src for baseline/cockpit references"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/agent.js:20:- BASELINE (BTC): reversão à média (RSI<25 compra / RSI>75 vende), gateada por != bear, != trend e por um filtro de fluxo do taker (não compra dip sob capitulação vendedora). A venda da baseline é a automação id3 — HOJE PAUSADA; se um dia reativada, é venda tática legítima (RSI>75), não venda do cofre.
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/agent.js:22:- REGIME-GATING é o coração: em BEAR, as COMPRAS de farm/trend/baseline ficam em CAIXA (protegido); o HARVESTER é a exceção desenhada (acima). O edge validado é DRAWDOWN MENOR por não pescar faca caindo — NÃO é alpha. Farm/trend parados em bear é o comportamento CORRETO e desejado, não uma oportunidade perdida.
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/agent.js:25:AMBIENTE (crucial — confirme a cada ciclo com tradeux_get_cockpit; NÃO assuma)
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/agent.js:26:- O ambiente REAL e o estado de trading vêm de tradeux_get_cockpit: env.useTestnet (mainnet vs testnet) e env.tradingHalt (kill-switch). É a FONTE DE VERDADE — confie nela, não no que este prompt assume.
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/agent.js:33:- 1× tradeux_get_cockpit por ciclo: confirma o AMBIENTE (env.useTestnet/env.tradingHalt) e traz, por símbolo, a MECÂNICA da distribuição de 1m — mediana |move|, σ, % de moves ≥ break-even, EV/trade NET de fee (costuma ser ≤0), a banda Monte Carlo DRIFTLESS (p50≡preço, NÃO previsão) e o estado dos gates de COMPRA. REPORTE no diário o estado mecânico e a coerência dos gates (EV≤0 a 1m é esperado — ver DIVERGÊNCIAS ESPERADAS).
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/agent.js:35:- Avaliar COERÊNCIA com a tese: o regime está sendo respeitado? alguma automação deveria ter disparado e não disparou (ou o contrário)? há venda de BTC INDEVIDA — isto é, FORA dos módulos táticos (trend id7 / harvester id25), vendendo MAIS que a posição tática (TREND_QTY/HARVEST), ou um fill do HARVESTER abaixo do custo médio (o no-loss é garantia SÓ do harvester; o trend corta perda por desenho)? Ordens manuais (sem automationId) costumam ser do dono/operador (testes, ajustes) — registre no diário; só alarme se drenarem o cofre de forma recorrente. NUNCA compare o RSI ou preço atual da memória com o momento de execução de uma ordem passada para alegar incoerência, pois o mercado se moveu e o Beholder não guarda histórico de RSI no momento do preenchimento. A memória do Beholder reflete apenas o estado real-time atual (no segundo da sua leitura). Para divergências cockpit×oráculo (regime/fluxo/gates), consulte DIVERGÊNCIAS ESPERADAS (abaixo) ANTES de chamar de incoerência.
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/agent.js:36:- DIVERGÊNCIAS ESPERADAS (NÃO são incoerência/anomalia — NÃO reporte como achado NEM notifique o dono): o cockpit lê as MESMAS chaves MEMORY['REGIME']/['FLOW'] que os oráculos vivos; tradeux_get_regime/tradeux_get_oracle_state são leituras VIVAS separadas → delta pequeno cockpit×vivo é TIMING, não fonte paralela. Itens:
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/agent.js:38:  (2) FLUXO eixo IDADE: compare pela IDADE (cockpit flow.ageSec) — imbalance velho mais negativo que o vivo é o MESMO sinal em instantes diferentes.
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/agent.js:43:  (7) GATE ≠ TRIGGER: buyAllowed/farm/baseline = o GATE de regime/fluxo (DOUTRINA: o que a estratégia PERMITE naquele regime), NÃO o gatilho de entrada nem confirmação de ordem. O FARM só compra no dip RSI_1m<35 (baseline RSI<25); o cockpit NÃO lê RSI de propósito. Gate ABERTO (farm=true) com RSI ACIMA do gatilho é ESPERADO (o gate permite, aguardando o dip) — NÃO é incoerência nem "RSI errado/threshold diferente".
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/agent.js:51:2. NUNCA coloque ordens que dupliquem/concorram com as automações (farm, trend, baseline). Seu produto é OBSERVAÇÃO e CONSELHO, não execução paralela.
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/agent.js:62:  "verifique se o sistema (farm/trend/baseline/harvester + regime-gating) está coerente com a " +
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/notifyDedup.js:7:// HALT e divergência cockpit×oráculo repetidos). Esta camada compara o ASSUNTO da notificação
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/notifyDedup.js:37:  'cockpit', 'snapshot', 'divergencia', 'divergente', 'diverge', 'contradicao', 'incoerencia', 'coerencia',
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/notifyDedup.js:42:  'harvester', 'harvest', 'farm', 'baseline', 'funil', 'funnel',
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/notifyDedup.js:54:  desequilibrio: 'imbalance', painel: 'cockpit',
> ```

## 🤖 Claude *(16:47:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"if.*gates\\.baseline\\|gates\\.baseline\\b\\|c\\.gates\\|\\.gates\\.baseline\\|=== true\\|=== false\" /home/gcrux-tradeux/tradeux/backend/src/ /home/gcrux-tradeux/tradeux/tradeux-mcp/src/ 2>/dev/null | grep -iv node_modules | grep -i baseline; echo \"---node version check for ?? operator---\"; node --version",
  "description": "Search for direct truthy/strict consumers of gates.baseline; check node version"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrux-tradeux/tradeux/tradeux-mcp/src/index.js:228:        buyGate: { allowed: gates.buyAllowed, reason: gates.reason, flowFresh: gates.flowFresh, flowGated: gates.flowGated, farm: gates.farm, baseline: gates.baseline },
> ---node version check for ?? operator---
> v22.22.3
> ```

## 🤖 Claude *(16:47:22)*

The agent consumes `gates.baseline` only as free-text via the MCP `buyGate.baseline` field (it reasons over it, doesn't do `if (gates.baseline)`). The `(7) GATE ≠ TRIGGER` doctrine block already exists. Now let me verify the analysisController endpoint that serves `/analysis/cockpit` — to confirm `getStatus()` (which calls `freshen` → `deriveGates`) is the path the MCP/frontend hit, and there's no JSON serialization issue with `null` (there isn't, but let me confirm the endpoint shape).

## 🤖 Claude *(16:47:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"cockpit\\|getStatus\\|freshen\\|deriveGates\" /home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js /home/gcrux-tradeux/tradeux/backend/src/routers/*.js 2>/dev/null",
  "description": "Locate the /analysis/cockpit endpoint wiring"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrux-tradeux/tradeux/backend/src/routers/analysisRouter.js:13:router.get('/cockpit', analysisController.getCockpitStatus);
> /home/gcrux-tradeux/tradeux/backend/src/routers/analysisRouter.js:15:router.get('/cockpit/:symbol', analysisController.getCockpit);
> /home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js:5:const cockpitJob = require('../cockpitJob');
> /home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js:25:        // da UI ("Market Regime" = instantâneo). As automações e o cockpit gateiam pelo regime HISTERÉTICO
> /home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js:27:        // histerese evita que o agente compare o instantâneo com o cockpit (=gate) e chame de "contradição":
> /home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js:48:    res.json(regimeJob.getStatus());
> /home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js:68:    res.json(flowJob.getStatus());
> /home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js:71:// GET /analysis/cockpit — snapshot agregado do Cockpit (por símbolo: distribuição de retornos 1m, EV
> /home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js:73:// o painel /cockpit (single source of truth = brain). Não expõe segredos (só estado de mercado).
> /home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js:75:    const status = cockpitJob.getStatus();
> /home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js:87:// GET /analysis/cockpit/:symbol — o COCKPIT de um símbolo, lido direto da MEMORY do brain (cópia rasa).
> /home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js:92:    if (!snap) return res.status(404).json({ error: 'sem snapshot de cockpit', symbol });
> /home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js:93:    // freshen: regime/flow/gates SEMPRE no instante da leitura (mata a defasagem de até 60s do snapshot,
> /home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js:94:    // que o agente lia como "contradição"); a analítica 1m fica na cadência do job. Ver cockpitJob.freshen.
> /home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js:95:    res.json(cockpitJob.freshen(symbol, snap));
> ```

## 🤖 Claude *(16:47:27)*

Both endpoints (`/cockpit` aggregated via `getStatus()→freshen→deriveGates`, and `/cockpit/:symbol` via `freshen→deriveGates`) go through `deriveGates`, plus the `runOnce` snapshot path. The change is in `deriveGates` itself, so it applies to all three. JSON serializes `null` fine.

Now let me write a quick adversarial simulation of `deriveGates` to prove the `buyAllowed` truth table is byte-identical pre/post for the full matrix, and that `baseline` is `null` only for non-flow-gated.

## 🤖 Claude *(16:47:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat > /tmp/derive_test.js <<'EOF'\nconst FLOW_BUY_MIN = -0.4;\nconst FLOW_STALE_MS = 5*60*1000;\nconst FLOW_GATED = new Set(['BTCUSDT']);\n\n// OLD behavior\nfunction deriveOld(regime, flow, symbol) {\n  const regimeOk = !!regime && regime !== 'bear' && regime !== 'unknown';\n  const flowFresh = flow && Number.isFinite(flow.imbalance) && flow.atMs && (Date.now()-flow.atMs) < FLOW_STALE_MS;\n  const flowOk = !!flowFresh && flow.imbalance >= FLOW_BUY_MIN;\n  const farm = regimeOk && regime !== 'trend';\n  const baseline = farm && flowOk;\n  const trend = regimeOk;\n  const flowGated = !!symbol && FLOW_GATED.has(String(symbol).toUpperCase());\n  const buyAllowed = flowGated ? baseline : farm;\n  return { farm, baseline, trend, buyAllowed, flowGated };\n}\n// NEW behavior\nfunction deriveNew(regime, flow, symbol) {\n  const regimeOk = !!regime && regime !== 'bear' && regime !== 'unknown';\n  const flowFresh = flow && Number.isFinite(flow.imbalance) && flow.atMs && (Date.now()-flow.atMs) < FLOW_STALE_MS;\n  const flowOk = !!flowFresh && flow.imbalance >= FLOW_BUY_MIN;\n  const farm = regimeOk && regime !== 'trend';\n  const trend = regimeOk;\n  const flowGated = !!symbol && FLOW_GATED.has(String(symbol).toUpperCase());\n  const baselineRaw = farm && flowOk;\n  const baseline = flowGated ? baselineRaw : null;\n  const buyAllowed = flowGated ? baselineRaw : farm;\n  return { farm, baseline, trend, buyAllowed, flowGated };\n}\n\nconst now = Date.now();\nconst regimes = ['range','mixed','trend','bear','unknown', null];\nconst flows = [\n  {name:'fresh+ok', flow:{imbalance:0.1, atMs:now}},\n  {name:'fresh+capit', flow:{imbalance:-0.9, atMs:now}},\n  {name:'stale', flow:{imbalance:0.1, atMs:now-10*60*1000}},\n  {name:'absent', flow:null},\n  {name:'NaN', flow:{imbalance:NaN, atMs:now}},\n];\nconst symbols = ['BTCUSDT','BNBUSDT'];\n\nlet buyMismatch=0, total=0;\nconsole.log('SYM      | REGIME  | FLOW        | farm  | buyAllowed | baseline(old->new)');\nfor (const sym of symbols) for (const r of regimes) for (const f of flows) {\n  total++;\n  const o = deriveOld(r, f.flow, sym);\n  const n = deriveNew(r, f.flow, sym);\n  const buyEq = o.buyAllowed === n.buyAllowed;\n  const farmEq = o.farm === n.farm;\n  if (!buyEq) buyMismatch++;\n  const flag = (!buyEq||!farmEq) ? '  <== MISMATCH' : '';\n  console.log(`${sym.padEnd(8)} | ${String(r).padEnd(7)} | ${f.name.padEnd(11)} | ${String(o.farm).padEnd(5)} | ${String(n.buyAllowed).padEnd(10)} | ${String(o.baseline)} -> ${String(n.baseline)}${flag}`);\n}\nconsole.log(`\\nTotal casos: ${total} | buyAllowed mismatches: ${buyMismatch}`);\n\n// extra symbol via env-like\nconst FLOW_GATED2 = new Set(['BTCUSDT','ETHUSDT']);\nfunction deriveNewEnv(regime, flow, symbol) {\n  const regimeOk = !!regime && regime !== 'bear' && regime !== 'unknown';\n  const flowFresh = flow && Number.isFinite(flow.imbalance) && flow.atMs && (Date.now()-flow.atMs) < FLOW_STALE_MS;\n  const flowOk = !!flowFresh && flow.imbalance >= FLOW_BUY_MIN;\n  const farm = regimeOk && regime !== 'trend';\n  const flowGated = !!symbol && FLOW_GATED2.has(String(symbol).toUpperCase());\n  const baselineRaw = farm && flowOk;\n  const baseline = flowGated ? baselineRaw : null;\n  return { baseline, flowGated };\n}\nconst eth = deriveNewEnv('range', {imbalance:0.1, atMs:now}, 'ETHUSDT');\nconsole.log(`\\nENV extra flow-gated ETHUSDT (range,fresh+ok): baseline=${eth.baseline} flowGated=${eth.flowGated}  (esperado: true/true)`);\nEOF\nnode /tmp/derive_test.js",
  "description": "Run adversarial truth-table simulation comparing old vs new deriveGates"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> SYM      | REGIME  | FLOW        | farm  | buyAllowed | baseline(old->new)
> BTCUSDT  | range   | fresh+ok    | true  | true       | true -> true
> BTCUSDT  | range   | fresh+capit | true  | false      | false -> false
> BTCUSDT  | range   | stale       | true  | false      | false -> false
> BTCUSDT  | range   | absent      | true  | false      | false -> false
> BTCUSDT  | range   | NaN         | true  | false      | false -> false
> BTCUSDT  | mixed   | fresh+ok    | true  | true       | true -> true
> BTCUSDT  | mixed   | fresh+capit | true  | false      | false -> false
> BTCUSDT  | mixed   | stale       | true  | false      | false -> false
> BTCUSDT  | mixed   | absent      | true  | false      | false -> false
> BTCUSDT  | mixed   | NaN         | true  | false      | false -> false
> BTCUSDT  | trend   | fresh+ok    | false | false      | false -> false
> BTCUSDT  | trend   | fresh+capit | false | false      | false -> false
> BTCUSDT  | trend   | stale       | false | false      | false -> false
> BTCUSDT  | trend   | absent      | false | false      | false -> false
> BTCUSDT  | trend   | NaN         | false | false      | false -> false
> BTCUSDT  | bear    | fresh+ok    | false | false      | false -> false
> BTCUSDT  | bear    | fresh+capit | false | false      | false -> false
> BTCUSDT  | bear    | stale       | false | false      | false -> false
> BTCUSDT  | bear    | absent      | false | false      | false -> false
> BTCUSDT  | bear    | NaN         | false | false      | false -> false
> BTCUSDT  | unknown | fresh+ok    | false | false      | false -> false
> BTCUSDT  | unknown | fresh+capit | false | false      | false -> false
> BTCUSDT  | unknown | stale       | false | false      | false -> false
> BTCUSDT  | unknown | absent      | false | false      | false -> false
> BTCUSDT  | unknown | NaN         | false | false      | false -> false
> BTCUSDT  | null    | fresh+ok    | false | false      | false -> false
> BTCUSDT  | null    | fresh+capit | false | false      | false -> false
> BTCUSDT  | null    | stale       | false | false      | false -> false
> BTCUSDT  | null    | absent      | false | false      | false -> false
> BTCUSDT  | null    | NaN         | false | false      | false -> false
> BNBUSDT  | range   | fresh+ok    | true  | true       | true -> null
> BNBUSDT  | range   | fresh+capit | true  | true       | false -> null
> BNBUSDT  | range   | stale       | true  | true       | false -> null
> BNBUSDT  | range   | absent      | true  | true       | false -> null
> BNBUSDT  | range   | NaN         | true  | true       | false -> null
> BNBUSDT  | mixed   | fresh+ok    | true  | true       | true -> null
> BNBUSDT  | mixed   | fresh+capit | true  | true       | false -> null
> BNBUSDT  | mixed   | stale       | true  | true       | false -> null
> BNBUSDT  | mixed   | absent      | true  | true       | false -> null
> BNBUSDT  | mixed   | NaN         | true  | true       | false -> null
> BNBUSDT  | trend   | fresh+ok    | false | false      | false -> null
> BNBUSDT  | trend   | fresh+capit | false | false      | false -> null
> BNBUSDT  | trend   | stale       | false | false      | false -> null
> BNBUSDT  | trend   | absent      | false | false      | false -> null
> BNBUSDT  | trend   | NaN         | false | false      | false -> null
> BNBUSDT  | bear    | fresh+ok    | false | false      | false -> null
> BNBUSDT  | bear    | fresh+capit | false | false      | false -> null
> BNBUSDT  | bear    | stale       | false | false      | false -> null
> BNBUSDT  | bear    | absent      | false | false      | false -> null
> BNBUSDT  | bear    | NaN         | false | false      | false -> null
> BNBUSDT  | unknown | fresh+ok    | false | false      | false -> null
> BNBUSDT  | unknown | fresh+capit | false | false      | false -> null
> BNBUSDT  | unknown | stale       | false | false      | false -> null
> BNBUSDT  | unknown | absent      | false | false      | false -> null
> BNBUSDT  | unknown | NaN         | false | false      | false -> null
> BNBUSDT  | null    | fresh+ok    | false | false      | false -> null
> BNBUSDT  | null    | fresh+capit | false | false      | false -> null
> BNBUSDT  | null    | stale       | false | false      | false -> null
> BNBUSDT  | null    | absent      | false | false      | false -> null
> BNBUSDT  | null    | NaN         | false | false      | false -> null
> 
> Total casos: 60 | buyAllowed mismatches: 0
> 
> ENV extra flow-gated ETHUSDT (range,fresh+ok): baseline=true flowGated=true  (esperado: true/true)
> ```

## 🤖 Claude *(16:47:49)*

The simulation proves: 60 cases, **zero `buyAllowed` mismatches**, `farm` intact, `baseline` becomes `null` only for non-flow-gated alts (and notice the prior bug it exposes: old `baseline` for BNB was a phantom `true` in range/mixed regardless of flow — exactly the gate-fantasma the agent flagged). ENV-extra flow-gated symbol keeps `baseline=true`.

Now let me verify the MCP description string is well-formed (no broken escaping) and run the agent `--check` syntax/CI-relevant sanity, plus confirm the notifyDedup self-test still passes.

## 🤖 Claude *(16:47:52)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp && node -e \"require('/home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js'); console.log('cockpitJob.js: syntax OK, exports:', Object.keys(require('/home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js')).join(','));\" 2>&1 | head -20",
  "description": "Syntax-load cockpitJob.js to confirm it parses and exports cleanly"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrux-tradeux/tradeux/backend/src/utils/crypto.js:4
> if (key.length !== 32) throw new Error('Invalid key size for AES. Must be 256-bit / 32 bytes.');
>                        ^
> 
> Error: Invalid key size for AES. Must be 256-bit / 32 bytes.
>     at Object.<anonymous> (/home/gcrux-tradeux/tradeux/backend/src/utils/crypto.js:4:30)
>     at Module._compile (node:internal/modules/cjs/loader:1781:14)
>     at Object..js (node:internal/modules/cjs/loader:1913:10)
>     at Module.load (node:internal/modules/cjs/loader:1505:32)
>     at Function._load (node:internal/modules/cjs/loader:1309:12)
>     at wrapModuleLoad (node:internal/modules/cjs/loader:254:19)
>     at Module.require (node:internal/modules/cjs/loader:1527:12)
>     at require (node:internal/modules/helpers:147:16)
>     at Object.<anonymous> (/home/gcrux-tradeux/tradeux/backend/src/repositories/settingsRepository.js:3:16)
>     at Module._compile (node:internal/modules/cjs/loader:1781:14)
> 
> Node.js v22.22.3
> ```

## 🤖 Claude *(16:47:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux/tradeux-mcp && node --check src/index.js 2>&1 | head -20 && echo \"MCP index.js: --check OK\"",
  "description": "Syntax-check MCP index.js after description edit"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> MCP index.js: --check OK
> ```

## 🤖 Claude *(16:47:56)*

The full `require` fails only because `AES_KEY` isn't set in this bare shell (transitive load of beholder→exchange→crypto) — not a syntax problem in the changed file. Let me confirm `cockpitJob.js` parses with a pure `--check`, and run the notifyDedup self-test that the CI runs.

## 🤖 Claude *(16:47:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "node --check /home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js && echo \"cockpitJob.js: --check OK (syntax valid)\"; echo \"---notifyDedup self-test (CI step)---\"; grep -rn \"selfTest\\|self-test\\|require.main\\|node.*notifyDedup\" /home/gcrux-tradeux/tradeux/tradeux-agent/src/notifyDedup.js /home/gcrux-tradeux/tradeux/.github/workflows/*.yml 2>/dev/null | head",
  "description": "Syntax-check cockpitJob; locate notifyDedup CI self-test"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> cockpitJob.js: --check OK (syntax valid)
> ---notifyDedup self-test (CI step)---
> /home/gcrux-tradeux/tradeux/tradeux-agent/src/notifyDedup.js:154:// Exportado p/ o self-test/observabilidade.
> /home/gcrux-tradeux/tradeux/.github/workflows/ci.yml:120:      - name: Dedup de notificacoes por assunto (self-test)
> ```

## 🤖 Claude *(16:48:04)*

Both files parse. The notifyDedup self-test is unrelated to this change (no notifyDedup file was touched). The CI "tests" (migrate+seed on mysql+postgres + agent `--check`) don't exercise `deriveGates` logic — this is a runtime-pure JS change with no DB/migration footprint, so CI staying green tells us nothing about correctness; my simulation is the real proof.

Let me do one final check: confirm there's no other backend reader of `MEMORY['<sym>:COCKPIT'].gates.baseline` (e.g., a separate job or controller doing `if (gates.baseline)`), which would be the one place `null` could silently become a false-negative.

## 🤖 Claude *(16:48:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"COCKPIT\\|getMemory.*COCKPIT\\|\\.gates\" /home/gcrux-tradeux/tradeux/backend/src/ 2>/dev/null | grep -iv node_modules | grep -v \"cockpitJob.js\\|indexes.js\\|// \" | grep -i \"cockpit\\|gates\"",
  "description": "Find any other backend consumer of COCKPIT.gates"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js:91:    const snap = beholder.getMemory(symbol, indexKeys.COCKPIT);
> ```

## 🤖 Claude *(16:48:47)*

The only other reader (`analysisController.js:91`) just passes the snapshot through `freshen` (which re-derives gates) and serializes to JSON — it does not branch on `gates.baseline`. No backend consumer does `if (gates.baseline)`.

---

# REVISÃO — fix `baseline` gate-fantasma (cockpit), working tree NÃO-commitado

**Arquivos:** `/home/gcrux-tradeux/tradeux/backend/src/cockpitJob.js` (`deriveGates`) · `/home/gcrux-tradeux/tradeux/tradeux-mcp/src/index.js:215` (descrição do tool `tradeux_get_cockpit`).

## VEREDITO: PASS

O fix faz exatamente o que diz: torna `baseline` symbol-aware (`null`=n/a para alt não-flow-gated), preserva `buyAllowed` e `farm` byte-a-byte, e a mudança vale nos 3 caminhos que passam por `deriveGates`. Nenhum consumidor quebra com `null`. Prova abaixo.

## Achados

**[INFO] `buyAllowed` idêntico — provado por tabela-verdade exaustiva.** Simulei old vs new em `{BTCUSDT, BNBUSDT} × {range, mixed, trend, bear, unknown, null} × {fresh+ok, fresh+capit, stale, absent, NaN}` = 60 casos: **0 mismatches** em `buyAllowed` e `farm`. BTC usa `baselineRaw` (≡ antigo `baseline`); alt usa `farm`. Confirma o claim 1.

**[INFO] O fix de fato mata o falso-flag — e a simulação exibe o bug antigo.** No caminho antigo, BNBUSDT em range/mixed expunha `baseline=true` MESMO com fluxo capitulação/stale/absent/NaN (porque `flowGated?baseline:farm` só usava `baseline` no `buyAllowed`, mas o campo `baseline` cru ia pro payload). Era um `true`-fantasma de um módulo que a alt não tem. Agora vai `null`. Causa-raiz correta.

**[INFO] Nenhum consumidor quebra com `null` (claim 2):**
- MCP `index.js:228` projeta `baseline: gates.baseline` cru no `buyGate` → `null` serializa OK em JSON; é texto que o agente raciocina, não há `if(gates.baseline)`.
- Frontend `Cockpit.js` (bridges + card "Gate acumulação BTC", linhas 378-412, 425): lê `cpg.farm`, `cpg.flowGated`, `cpg.flowBuyMin`, `cpg.buyAllowed`, `cpg.reason` — **nunca** `cpg.baseline`. Imune. O card de BTC usa `buyAllowed` (intacto).
- Snapshot `MEMORY['<sym>:COCKPIT'].gates` (gravado em `runOnce`): o único outro leitor é `analysisController.js:91`, que re-deriva via `freshen` e serializa — não ramifica em `gates.baseline`. Nenhum `if (gates.baseline)` em backend/agent/frontend. `null` nunca vira `false`-falso-positivo.

**[INFO] `freshen` e `runOnce` cobertos (claim 3):** ambos chamam `deriveGates(regime, flow, symbol)` (linhas 136 e 159); o endpoint agregado `/analysis/cockpit` (via `getStatus→freshen`) e o por-símbolo `/analysis/cockpit/:symbol` (via `freshen`) re-derivam na leitura. Como a mudança está DENTRO de `deriveGates`, vale nos 3.

**[INFO] Env `COCKPIT_FLOW_GATED_SYMBOLS` mantém baseline (claim 5):** simulei ETHUSDT como flow-gated extra → `baseline=true, flowGated=true`. A lógica é `flowGated ? baselineRaw : null`, então qualquer símbolo no set ganha `baseline` real. OK.

**[BAIXA — nice-to-have, claim 4] `reason` das alts coerente, mas os textos genéricos seguem dizendo "farm/baseline".** A linha da alt (`Cockpit.js:110` / `cockpitJob.js:110`) é específica e correta ("FARM liberado, SEM filtro de fluxo"). Porém os ramos genéricos `!regimeOk` (l.106) e `regime==='trend'` (l.107) ainda escrevem "farm/baseline em CAIXA" / "farm/baseline e trend parados" — para uma ALT, `baseline` é n/a, então mencioná-lo no `reason` é levemente inconsistente com `baseline=null` no mesmo payload. É puramente cosmético (não muda gate nem `buyAllowed`); o agente já tem a doutrina GATE≠TRIGGER + a nota de `baseline=null` na descrição do tool. Severidade BAIXA — não bloqueia. Se for polir: trocar "farm/baseline" por "acumulação (farm)" nas l.106-107, ou interpolar condicional ao `flowGated`.

**[INFO] Descrição MCP correta e bem-formada.** `node --check` passa; a frase nova explica `baseline=null` para alts + reforça GATE≠TRIGGER (e menciona `RSI>35/25`, coerente com farm RSI_1m<35 / baseline RSI<25). Alinhada com o bloco `(7) GATE ≠ TRIGGER` já no `agent.js:43`.

## Testes que eu rodaria

1. **Tabela-verdade old-vs-new (FEITO):** `/tmp/derive_test.js` — 60 casos, 0 mismatch em `buyAllowed`/`farm`; `baseline` null só p/ alt; ETHUSDT-via-env mantém `true`. Reproduzível extraindo `deriveGates` puro.
2. **`node --check` (FEITO):** `cockpitJob.js` e `tradeux-mcp/src/index.js` parseiam OK (o erro de `require` cheio é só `AES_KEY` ausente no shell, transitivo via crypto.js — não é do diff).
3. **Smoke ao vivo:** `GET /analysis/cockpit` e `GET /analysis/cockpit/BNBUSDT` no stack 8090 → confirmar `gates.baseline:null` p/ BNB/LTC/ADA e `true|false` p/ BTC; `buyAllowed`/`farm`/`reason` inalterados vs antes. (BTC=bear hoje → BTC `baseline:false`, alts `null`.)
4. **MCP regression:** `tradeux_get_cockpit` → `buyGate.baseline` deve vir `null` p/ alts, sem throw na projeção (l.228).
5. **Frontend visual:** `/cockpit` no browser → bridges das alts acendem por regime (farm), card "Gate acumulação BTC" segue lendo `buyAllowed` → sem `undefined`/crash no render.
6. **Agente:** rodar 1 ciclo (`--once`) e confirmar que NÃO emite mais o falso-flag de "baseline liberado p/ BNBUSDT apesar de RSI". (CI `--check` não exercita `deriveGates`; é só bridge-smoke.)

## Recomendação de merge

**MERGE — PASS.** Mudança runtime-pura, sem footprint de DB/migration/money-path; `buyAllowed` provadamente intacto em 60 casos; corrige um falso-positivo real de observabilidade (gate-fantasma) sem mexer em execução. CI permanece verde mas é irrelevante aqui (não cobre essa lógica) — a prova é a tabela-verdade. Único follow-up é o cosmético BAIXA dos `reason` genéricos l.106-107 (`cockpitJob.js`), opcional e pós-merge.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-17 - agent-a5a3922b86c4d255c]]
> * **Próxima Sessão**: [[2026-06-17 - agent-ac71eb815829bc61b]]
%% --- TIMELINE END --- %%

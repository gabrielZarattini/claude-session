# Fix farm buy order notional filter failures
**Date:** 2026-06-09 | **Session ID:** `95ad4b6a-ec2f-4341-80cc-9bb1087b5149`

---

## 👤 User *(14:56:19)*

As automações de COMPRA do FARM (id 9/11/13 = Farm Buy LTCUSDT/BNBUSDT/ADAUSDT) no TradeUX usam orderTemplate com quantity='MIN_NOTIONAL' e quantityMultiplier=1. Foi validado AO VIVO em 2026-06-09 que MIN_NOTIONAL×1 arredonda pra baixo (Math.floor no calcQty em backend/src/beholder.js) e fica ABAIXO do filtro NOTIONAL de $5 (~$4.4 no BTC), falhando com o erro Binance -1013 "Filter failure: NOTIONAL" quando a ordem dispara. O farm NUNCA disparou (gateado por regime=bear), então o bug é latente — quando o mercado sair do bear e o farm tentar comprar, vai falhar silenciosamente.

Tarefa: corrigir o size das compras do farm pra limpar $5 com margem. (1) Editar backend/scripts/setup-farm.js: mudar o default de FARM_SIZE_MULT de 1 para 2 (igual foi feito no setup-harvester.js, commit 7aebc26). (2) Corrigir os templates JÁ VIVOS no banco: rodar dentro do container db `UPDATE orderTemplates SET quantityMultiplier=2 WHERE name LIKE 'Farm Buy%'` (são 3: LTC/BNB/ADA). (3) Verificar que MIN_NOTIONAL×2 × preço > $5 em todas as alts (LTC ~$42, BNB ~$600, ADA ~$0.16 — atenção à ADA, que com preço baixo pode precisar de mult maior; cheque o minNotional de cada par na tabela symbols). Rodar git/docker como gcrux-tradeux. Ver o SEAL 2026-06-09 em ~/HANDOFF.md e a memória tradeux-harvester-experiment.

## 🤖 Claude *(14:56:37)*


## 🤖 Claude *(14:56:38)*

Vou começar reunindo o contexto necessário: o estado do HANDOFF.md, a memória do harvester, e a estrutura do repositório. Deixa eu fazer o reconhecimento inicial.

## 🤖 Claude *(14:56:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "whoami; echo \"---HOME---\"; echo $HOME; echo \"---PWD---\"; pwd; echo \"---LS /home/gcrux-tradeux---\"; ls -la /home/gcrux-tradeux 2>/dev/null | head -40; echo \"---HANDOFF locations---\"; ls -la /home/gcrux-tradeux/HANDOFF.md /home/ubuntu/HANDOFF.md 2>/dev/null",
  "description": "Check identity, home, and locate HANDOFF.md and repo"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 2
> ubuntu
> ---HOME---
> /home/ubuntu
> ---PWD---
> /home/gcrux-tradeux
> ---LS /home/gcrux-tradeux---
> total 152
> drwxrwx--- 11 gcrux-tradeux ubuntu         4096 Jun  9 10:19 .
> drwxr-xr-x 15 ubuntu        ubuntu         4096 Jun  2 18:34 ..
> drwxrwx---  3 gcrux-tradeux ubuntu         4096 Aug 21  2025 backups
> -rw-------  1 gcrux-tradeux ubuntu          135 Jun  2 19:52 .bash_history
> -rwxrwx---  1 gcrux-tradeux ubuntu          182 Aug 21  2025 .bashrc
> drwxrwxr-x  5 ubuntu        ubuntu         4096 Jun  3 10:27 .claude
> drwx------  3 gcrux-tradeux gcrux-tradeux  4096 Jun  2 21:54 .docker
> drwxrwxr-x  2 ubuntu        ubuntu         4096 Jun  4 18:30 .firecrawl
> -rw-rw-r--  1 ubuntu        ubuntu        70823 Jun  9 10:19 HANDOFF.md
> drwxrwx---  3 gcrux-tradeux ubuntu         4096 Jun  2 18:34 htdocs
> drwxrwx---  4 gcrux-tradeux ubuntu         4096 Aug 21  2025 logs
> -rwxrwx---  1 gcrux-tradeux ubuntu          675 Aug 21  2025 .profile
> -rw-rw-r--  1 ubuntu        ubuntu        10742 Jun  8 23:06 RESEARCH-bear-capture.md
> -rw-rw-r--  1 ubuntu        ubuntu         9133 Jun  8 11:29 RESEARCH-flow-and-margin.md
> drwx------  2 gcrux-tradeux ubuntu         4096 Jun  2 20:39 .ssh
> drwxrwx---  2 gcrux-tradeux ubuntu         4096 Aug 21  2025 tmp
> drwxrwxr-x 11 gcrux-tradeux gcrux-tradeux  4096 Jun  9 00:45 tradeux
> ---HANDOFF locations---
> -rw-rw-r-- 1 ubuntu ubuntu 70823 Jun  9 10:19 /home/gcrux-tradeux/HANDOFF.md
> ```

## 🤖 Claude *(14:56:47)*


## 🤖 Claude *(14:56:49)*

Entendi o layout: sou `ubuntu`, o repo está em `/home/gcrux-tradeux/tradeux` (dono gcrux-tradeux), e o HANDOFF.md está em `/home/gcrux-tradeux/HANDOFF.md`. Vou ler o SEAL mais recente, a memória do harvester e os arquivos-alvo em paralelo.

## 🤖 Claude *(14:56:49)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrux-tradeux/memory/tradeux-harvester-experiment.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	---
> 2	name: tradeux-harvester-experiment
> 3	description: "Harvester de dislocação (vault-safe, ATIVO id22-25) vs grid nativo (REJEITADO: drena cofre); bug do MIN_NOTIONAL×1 < $5"
> 4	metadata: 
> 5	  node_type: memory
> 6	  type: project
> 7	  originSessionId: 60395cbe-5bcd-4389-a706-1cc57b403b01
> 8	---
> 9	
> 10	Experimento ousado no testnet (2026-06-09, commit `7aebc26`) pra colher o chop/dislocação do BTCUSDT. Análise das 4h: ER~0.08 = chop puro; o **testnet disloca ABAIXO do mainnet em wicks e REVERTE** (corr 0.89 nos closes) = alfa testnet-específico; BTC testnet é o único feed limpo (alts descoladas/RSI travado).
> 11	
> 12	**GRID nativo do Beholder = REJEITADO.** `gridEval`/`generateGrids` (setup-grid.js, id21) operou 26 ordens MAS **vende por nível DIRETO DA CARTEIRA, sem rastrear inventário** → 24 SELL vs 2 BUY → **drenou ~0.0044 BTC do cofre** (mesma sangria do pivô). id21 PARADO; script com aviso ⛔NÃO-ATIVAR. **Não usar o grid nativo p/ nada que toque o cofre.**
> 13	
> 14	**HARVESTER = o que sobrevive (vault-safe, VALIDADO ao vivo).** Vende **só o próprio bucket** `MEMORY['<sym>:HARVEST']={qty,cost}` (custo médio ponderado, OBJETO pq o `validateConditions` exige `.cost*1.012`; clone do [[tradeux-trend-following]] `TREND_QTY`), via `app-em.updateHarvestPosition`; `calcQty` ganhou `HARVEST_QTY`. `fairPriceJob` grava `MEMORY['<sym>:FAIR']`=preço mainnet (sentinel `{price:0}` após N falhas = fail-safe de staleness sem `Date.now()`). 3 rungs de compra-limite funda (−3/−5/−7% do FAIR, **desgateadas do regime**) + venda no-loss. id22/23/24+id25 ATIVAS.
> 15	
> 16	**Why:** o cofre de BTC nunca pode ser drenado (origem do pivô [[tradeux-farm-funnel-backtest]]); o harvester garante isso por construção (vende só o que comprou, com lucro); o grid nativo NÃO garante.
> 17	
> 18	**How to apply:** p/ qualquer estratégia que venda BTC, use o padrão do bucket (rastreia o que comprou) — NÃO o grid nativo. Reaplicar pós-`make nuke`: `setup-harvester.js` (cria inativo) → `scripts/automation-ctl.js ACTION=start IDS=22,23,24,25`.
> 19	
> 20	**🐛 Bug do MIN_NOTIONAL (validado ao vivo, -1013):** `MIN_NOTIONAL×1` arredonda pra baixo (~$4.4 no BTC) e **FALHA o filtro NOTIONAL ($5)** ao disparar. Harvester usa `×2` (~$9). **O FARM (id9-14) tem o mesmo `MIN_NOTIONAL×1` → falharia ao operar (nunca testado, travado em bear); bumpar `FARM_SIZE_MULT`≥1.5 antes do farm rodar.** Ver [[tradeux-settings-password-incident]] (outro achado da mesma sessão).
> 21	
> ```

## 🤖 Claude *(14:56:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"SEAL 2026-06-09\\|^## SEAL\\|^# SEAL\\|SEAL \u2014\\|farm\\|Farm\\|FARM_SIZE_MULT\\|MIN_NOTIONAL\" /home/gcrux-tradeux/HANDOFF.md | head -60",
  "description": "Find SEAL 2026-06-09 and farm references in HANDOFF.md"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 8:0. 🏗️ **ARQUITETURA FARM-AND-FUNNEL COMPLETA E NO AR** (sessão 2026-06-08): **15 automações ativas** — Farm no-loss +
> 10:   por regime (farm `!=trend`, trend `!=bear`). Validada por backtest (`backend/scripts/backtest-farm-funnel.js`) **e ao
> 11:   vivo**. Doc: `docs/STRATEGY-farm-funnel.md`. Memória `tradeux-farm-funnel-backtest`. **Hoje MERCADO=BEAR → tudo INERTE/protegido.**
> 13:   (ligar a compra de BTC com o lucro real do farm, DEPOIS de observar o farm lucrar e calibrar o baseline com dado real);
> 14:   Fase 5 = **calibração** (5m + seleção de alts, SOL ruim no farm + switch macro fino — SMA-slope no regimeJob). Ver §5 do
> 38:   ⏳ **NEXT**: (a) **observar 1 golden→death real** (`logs/A:6.log`/`A:7.log`) antes de calibrar o size (id6=3× MIN_NOTIONAL);
> 153:  (`A:6.log`/`A:7.log`) antes de calibrar; (b) **sizing** id6=3× MIN_NOTIONAL (pequeno p/ observar) → subir depois; (c) ✅ **risco
> 167:- **Agente — prompt alinhado à Farm-and-Funnel** (commit `a0869c4`; gate QA PASS + TL APPROVE): copiloto OBSERVADOR (BTC=cofre nunca
> 241:**userData ws-api entregou executionReport**, MARKET fill no MIN_NOTIONAL, LIMIT/STOP_LOSS_LIMIT/OCO place+cancel,
> 357:O dono escolheu a **ativação correta**. **Decisões** (via AskUserQuestion): LIMIT marketável + buffer 0.3% · size pequeno (3× MIN_NOTIONAL,
> 434:### 🤝 SEAL — 2026-06-04 (fim de sessão grande: Trend + Oráculo de Fluxo + agente + pesquisa)
> 444:### 🤝 SEAL — 2026-06-08 (Pivô de estratégia: Farm-and-Funnel validado + funil shadow no ar)
> 450:Backtest novo `backend/scripts/backtest-farm-funnel.js` (engine de LOTES; candles mainnet; 3 regimes; 7 rodadas): farm =
> 453:não garantido, horizonte de anos. Config final (Farm+Trend+Switch, 15m): bull **+14.4%** / bear **−0.4%** / lateral **−5.5%**.
> 454:**Entregue (commit `416d6e9`, push master, CI rodando):** harness + relatórios `backtest-results/farm-funnel-*.md` + doc
> 455:**`docs/STRATEGY-farm-funnel.md`** (estratégia + plano faseado §5) + **`funnelJob` SHADOW AO VIVO** (rebuild+restart, boot
> 457:**NEXT = Fases 2-5 do doc (money-path, gate QA+TL, 1 passo/vez):** (2) `setup-farm` das alts via **grid NATIVO do Beholder**
> 459:(4) ligar o funil (money-path); (5) calibrar 5m + seleção de alts (SOL ruim no farm; LTC/BNB/ADA bons). Memória nova
> 460:**`tradeux-farm-funnel-backtest`**. ⚠️ Estado vivo: id3 PAUSADA · funil SHADOW (não compra) · id2/id6/id7 intocadas · stack 8090 / site 200.
> 462:**Fase 2a (commit `985272f`, push master):** `setup-farm.js` criou o farm no-loss das alts **LTC/BNB/ADA** — monitores
> 463:CANDLES ATIVOS (RSI) + templates LIMIT marketável + automações **Farm Buy** (id 9/11/13) e **Farm Sell no-loss** (id 10/12/14),
> 466:(REGIME/LAST_ORDER no index), regex-safe (validateConditions). **Fase 2b FEITA — farm das alts ATIVO:** as 6 automações (id 9-14, LTC/BNB/ADA) estão **ATIVAS**. Wiring validado AO VIVO na LTC:
> 468:(proteção em bear, igual a id2). Mercado bear ⇒ farm **inerte/armado**; opera quando virar range (compra RSI<35; vende no-loss
> 469:`bestBid>avgPrice×1.012`). Size 1×MIN_NOTIONAL (~$5-10). Reversível (`stop` id 9-14). Sem erros, site 200.
> 474:farm `!=trend` (igual id2/id3↔id6/id7 do BTC). **15 automações ativas = a arquitetura completa do backtest AO VIVO** (Farm+Trend+
> 476:realizado — money-path; só rende quando o farm lucrar, i.e. mercado não-bear); **Fase 5** = calibração 5m/seleção (SOL ruim) +
> 479:### 🤝 SEAL — 2026-06-08 (sessão grande: Farm-and-Funnel do diagnóstico ao deploy completo)
> 480:**De "só vende BTC, sangrando" → estratégia Farm-and-Funnel inteira validada e NO AR.** Arco: (1) **diagnóstico** do
> 482:backtest** (`backtest-farm-funnel.js`, candles mainnet, 3 regimes) → farm=baixo risco/marginal, **trend=motor de bull
> 484:(`docs/STRATEGY-farm-funnel.md`); (4) **Fase 1** funil SHADOW ao vivo; (5) **Fase 2** farm no-loss das alts (id 9-14, ativo,
> 488:do bear** (ver FIRST ACTION ⏰). Memória nova `tradeux-farm-funnel-backtest`. Stack 8090 / site 200. **0 PRs** (trunk-based).
> 490:### 🤝 SEAL — 2026-06-08 (cont. — agente LLM virou serviço supervisionado + STALE no card de KPIs)
> 508:site 200. **NEXT (Farm-and-Funnel) inalterado:** Fases 4-5 GUARDADAS até o regime sair do bear (regime confirmado BEAR nos 4 hoje).
> 512:### 🤝 SEAL — 2026-06-08 (cont. — prompt do agente alinhado à Farm-and-Funnel)
> 516:ele observa/aconselha, não opera em paralelo); tese explicada (farm/trend/baseline + regime-gating); BTC nunca vende (cofre × posição
> 528:### 🤝 SEAL — 2026-06-08 (cont. — trava determinística do cofre no MCP + get_memory_indexes enxuto)
> 541:"qualquer caminho com as chaves"; (ii) premissa "agente BTCUSDT-only" ERRADA — o prompt farma alts (LTC/BNB/ADA), não quebra a trava;
> 549:### 🤝 SEAL — 2026-06-08 (cont. — rebuild do agente: vivo == master + próxima frente)
> 559:### 🤝 SEAL — 2026-06-08 (cont. — deep research + backtest CRÍTICO de futures (FALSO POSITIVO) + toxicity nowcasting)
> 569:flips). **NÃO construir módulo de Futures de short** — a farm-and-funnel (caixa em bear, captura do bull) continua o melhor.
> 576:### 🤝 SEAL — 2026-06-09 (Harvester de dislocação vault-safe ATIVO + grid nativo REJEITADO + incidente de senha)
> 580:**🐛 Fix de size (validado ao vivo):** `MIN_NOTIONAL×1` (~$4.4) **FALHA o filtro NOTIONAL ($5)** → `-1013` (canary inicial falhou). Harvester agora `MIN_NOTIONAL×2` (~$9). **⚠️ O FARM (id9-14) tem o MESMO `MIN_NOTIONAL×1` → falharia ao disparar (nunca testado, travado em bear) — FOLLOW-UP: bumpar `FARM_SIZE_MULT`/`setup-farm.js` p/ ≥1.5 antes do farm operar.**
> 582:**Estado vivo:** grid21 PARADO · harvester 22-25 ATIVO (vault-safe, size ok) · baseline id2/id3(pausada)/trend id6-20/farm intactos e INERTES (bear nos 4) · fairPriceJob no ar (`FAIR`=mainnet) · agente recuperado · 4 containers, site 200, **vivo==master** (`7aebc26`). **0 PRs.** Helpers reutilizáveis: `scripts/automation-ctl.js` (start/stop por id), reaplicar pós-`make nuke`: `setup-harvester.js` (cria inativo) → `automation-ctl ACTION=start IDS=22,23,24,25`. **NEXT:** observar a venda no-loss disparar no revert (fecha o ciclo compra→venda ao vivo); fix do size do FARM; investigar o frontend de Settings; Farm-and-Funnel Fases 4-5 seguem PARADAS até sair do bear.
> ```

## 🤖 Claude *(14:56:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && echo \"---TOP LEVEL---\" && ls -la && echo \"---backend/scripts---\" && ls -la backend/scripts/ 2>/dev/null | grep -i \"farm\\|harvester\" && echo \"---git remote/status (as gcrux)---\" && sudo -u gcrux-tradeux git -C /home/gcrux-tradeux/tradeux status -sb 2>&1 | head -20",
  "description": "Explore repo top-level and farm/harvester scripts"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ---TOP LEVEL---
> total 132
> drwxrwxr-x 11 gcrux-tradeux gcrux-tradeux  4096 Jun  9 00:45 .
> drwxrwx--- 11 gcrux-tradeux ubuntu         4096 Jun  9 10:19 ..
> drwxrwxr-x 11 gcrux-tradeux gcrux-tradeux  4096 Jun  3 16:57 backend
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  8652 Jun  3 10:31 CLAUDE.md
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux   954 Jun  2 20:41 docker-compose.supabase.yml
> -rw-rw-r--  1 ubuntu        ubuntu         2612 Jun  8 16:33 docker-compose.yml
> -rw-rw-r--  1 ubuntu        ubuntu          593 Jun  8 16:22 .dockerignore
> drwxrwxr-x  2 ubuntu        ubuntu         4096 Jun  8 14:38 docs
> -rw-rw----  1 gcrux-tradeux gcrux-tradeux  1987 Jun  3 22:04 .env
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux  4077 Jun  2 20:41 .env.example
> drwxrwxr-x  2 ubuntu        ubuntu         4096 Jun  4 17:16 .firecrawl
> drwxrwxr-x  4 gcrux-tradeux gcrux-tradeux  4096 Jun  2 20:41 frontend
> drwxrwxr-x  8 gcrux-tradeux gcrux-tradeux  4096 Jun  9 10:18 .git
> drwxrwxr-x  3 gcrux-tradeux gcrux-tradeux  4096 Jun  2 20:41 .github
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux  1690 Jun  3 13:33 .gitignore
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux  1073 Jun  2 20:41 LICENSE
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux   768 Jun  2 20:41 Makefile
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux  7042 Jun  2 20:41 README.md
> -rw-rw-r--  1 gcrux-tradeux gcrux-tradeux  5990 Jun  3 16:22 SECURITY.md
> -rw-r--r--  1 gcrux-tradeux gcrux-tradeux 21861 Jun  2 21:55 setup.log
> -rwxrwxr-x  1 gcrux-tradeux gcrux-tradeux  1558 Jun  3 12:38 setup.sh
> drwxrwxr-x  5 gcrux-tradeux gcrux-tradeux  4096 Jun  8 17:31 tradeux-agent
> drwxrwxr-x  5 gcrux-tradeux gcrux-tradeux  4096 Jun  8 20:14 tradeux-mcp
> drwxrwxr-x  2 gcrux-tradeux gcrux-tradeux  4096 Jun  2 20:41 .vscode
> ---backend/scripts---
> -rw-rw-r--  1 ubuntu        ubuntu        25302 Jun  8 14:24 backtest-farm-funnel.js
> -rw-rw-r--  1 ubuntu        ubuntu        10404 Jun  8 15:28 setup-farm.js
> -rw-rw-r--  1 ubuntu        ubuntu         9055 Jun  9 10:15 setup-harvester.js
> ---git remote/status (as gcrux)---
> ## master...origin/master
> ?? "docs/Engenharia Preditiva para Criptoativos.md"
> ```

## 🤖 Claude *(14:57:02)*


## 🤖 Claude *(14:57:04)*

O contexto está claro — o SEAL 2026-06-09 confirma exatamente esse follow-up. Agora vou ler os três arquivos-chave: `setup-farm.js`, `setup-harvester.js` (o padrão a seguir) e o `calcQty` no beholder.

## 🤖 Claude *(14:57:04)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/scripts/setup-farm.js"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	'use strict';
> 2	/*
> 3	 * Setup IDEMPOTENTE do FARM no-loss das ALTS (Fase 2 da estratégia Farm-and-Funnel) — config pura,
> 4	 * sem código novo no engine. Ver docs/STRATEGY-farm-funnel.md e memória tradeux-farm-funnel-backtest.
> 5	 *
> 6	 * A regra do dono ("vende só por mais caro que comprou"): a venda dispara pelo PREÇO (no-loss), não
> 7	 * pelo RSI — vende a posição quando o bestBid supera o preço de compra (LAST_ORDER.avgPrice) + margem.
> 8	 * A compra entra no dip (RSI baixo) só fora de bear/trend (mean-reversion vive em range). Fiel ao
> 9	 * engine do backtest (compra RSI<lo; vende lote com lucro). 1 lote por vez no v1 (grid multi-nível = refino).
> 10	 *
> 11	 * Cria, por alt (se ausentes; INATIVAS por segurança):
> 12	 *   - monitor CANDLES (RSI_14) ATIVO — alimenta MEMORY['<sym>:RSI_14_<interval>'] (gatilho da compra).
> 13	 *     MINI_TICKER/BOOK já vêm do monitor system '*' (preço/bestBid de todas as alts, sem monitor próprio).
> 14	 *   - templates LIMIT marketável: BUY = bestAsk×(1+buf) MIN_NOTIONAL ; SELL = bestBid×(1−buf) LAST_ORDER_QTY.
> 15	 *   - automação "Farm Buy <sym>"  (RSI<lo + regime!=bear/trend + sem posição), INATIVA.
> 16	 *   - automação "Farm Sell <sym>" no-loss (tem posição + bestBid > avgPrice×(1+lucro)), INATIVA.
> 17	 *
> 18	 * Por que INATIVAS: é money-path. Ativar (1 alt por vez, com gate) é um passo SEPARADO — garantir antes
> 19	 * que o regimeJob computa o REGIME da alt (resolveSymbols pega símbolos de automações ATIVAS; até o 1º
> 20	 * poll a compra fica fail-safe pelo guard de REGIME na condition) e o sizing. Ver §5 do doc.
> 21	 *
> 22	 * Reproduz o setup após `make nuke` (dado runtime, não seeders).
> 23	 * Uso (dentro do container, server no ar):  node scripts/setup-farm.js   [DRY=true p/ preview]
> 24	 *   env: EM/PW (ou TRADEUX_EMAIL/TRADEUX_PASSWORD), PORT (3001),
> 25	 *        FARM_SYMBOLS (CSV, default LTCUSDT,BNBUSDT,ADAUSDT), FARM_INTERVAL (1m),
> 26	 *        FARM_RSI_LO (35), FARM_PROFIT (0.012), FARM_BUFFER (0.003), FARM_SIZE_MULT (1)
> 27	 */
> 28	const http = require('http');
> 29	
> 30	const SYMBOLS = (process.env.FARM_SYMBOLS || 'LTCUSDT,BNBUSDT,ADAUSDT').split(',').map(s => s.trim().toUpperCase()).filter(Boolean);
> 31	const INTERVAL = process.env.FARM_INTERVAL || '1m';
> 32	const RSI_KEY_SUFFIX = `RSI_14_${INTERVAL}`;
> 33	const RSI_LO = parseFloat(process.env.FARM_RSI_LO || '35');
> 34	const PROFIT = parseFloat(process.env.FARM_PROFIT || '0.012');   // lucro-alvo sobre o avgPrice (cobre buffer+fees no testnet)
> 35	const BUF = parseFloat(process.env.FARM_BUFFER || '0.003');      // buffer do LIMIT marketável (atravessa o book fino do testnet)
> 36	const SIZE_MULT = parseFloat(process.env.FARM_SIZE_MULT || '1'); // MIN_NOTIONAL × isto (size pequeno p/ validar)
> 37	const DRY = String(process.env.DRY || '').toLowerCase() === 'true';
> 38	const BASE = { host: process.env.FARM_API_HOST || '127.0.0.1', port: parseInt(process.env.PORT || '3001', 10) };
> 39	const EM = process.env.EM || process.env.TRADEUX_EMAIL;
> 40	const PW = process.env.PW || process.env.TRADEUX_PASSWORD;
> 41	
> 42	function req(method, path, token, body) {
> 43	    return new Promise((resolve) => {
> 44	        const data = body ? JSON.stringify(body) : null;
> 45	        const headers = { 'Content-Type': 'application/json' };
> 46	        if (token) headers['authorization'] = token; // middleware usa o token CRU (sem Bearer)
> 47	        if (data) headers['Content-Length'] = Buffer.byteLength(data);
> 48	        const r = http.request({ ...BASE, method, path, headers, timeout: 15000 }, res => {
> 49	            let d = ''; res.on('data', c => d += c);
> 50	            res.on('end', () => { let j; try { j = JSON.parse(d); } catch { j = d; } resolve({ status: res.statusCode, body: j }); });
> 51	        });
> 52	        r.on('error', e => resolve({ status: 0, body: String(e.message) }));
> 53	        r.on('timeout', () => { r.destroy(); resolve({ status: 0, body: 'timeout' }); });
> 54	        if (data) r.write(data); r.end();
> 55	    });
> 56	}
> 57	
> 58	// monitor CANDLES (RSI) ATIVO — alimenta o RSI da alt. Idempotente: insertMonitor responde 409 se já existe.
> 59	async function ensureMonitor(token, symbol) {
> 60	    if (DRY) return `[DRY] POST monitor CANDLES ${symbol} ${INTERVAL} RSI_14 (ativo)`;
> 61	    const r = await req('POST', '/monitors', token, {
> 62	        type: 'CANDLES', symbol, interval: INTERVAL, indexes: 'RSI_14',
> 63	        isActive: true, isSystemMon: false, broadcastLabel: null, logs: false,
> 64	    });
> 65	    if (r.status === 201) return `monitor CANDLES ${symbol} ${INTERVAL} criado (id ${r.body.id}, ATIVO → ${symbol}:${RSI_KEY_SUFFIX})`;
> 66	    if (r.status === 409) return `monitor CANDLES ${symbol} ${INTERVAL} já existe`;
> 67	    throw new Error(`falha ao criar monitor ${symbol}: ${r.status} ${JSON.stringify(r.body)}`);
> 68	}
> 69	
> 70	async function ensureTemplate(token, symbol, name, side, opts) {
> 71	    const all = await req('GET', `/ordertemplates/all/${symbol}`, token);
> 72	    const found = Array.isArray(all.body) ? all.body.find(t => t.name === name) : null;
> 73	    if (found) return { id: found.id, msg: `template "${name}" já existe (id ${found.id})` };
> 74	    if (DRY) return { id: 0, msg: `[DRY] POST template "${name}" (${opts.type} ${side} qty ${opts.quantity}×${opts.quantityMultiplier})` };
> 75	    const r = await req('POST', '/ordertemplates', token, {
> 76	        name, symbol, type: opts.type, side,
> 77	        limitPrice: opts.limitPrice || null, limitPriceMultiplier: opts.limitPriceMultiplier || 1,
> 78	        stopPrice: null, stopPriceMultiplier: 1,
> 79	        quantity: opts.quantity, quantityMultiplier: opts.quantityMultiplier || 1,
> 80	        icebergQty: null, icebergQtyMultiplier: 1,
> 81	    });
> 82	    if (r.status !== 201) throw new Error(`falha ao criar template ${name}: ${r.status} ${JSON.stringify(r.body)}`);
> 83	    return { id: r.body.id, msg: `template "${name}" criado (id ${r.body.id}, ${opts.type})` };
> 84	}
> 85	
> 86	async function findAutomationByName(token, name) {
> 87	    for (let page = 1; page <= 40; page++) {
> 88	        const r = await req('GET', `/automations?page=${page}`, token);
> 89	        const rows = r.body && r.body.rows;
> 90	        if (!Array.isArray(rows) || rows.length === 0) break;
> 91	        const hit = rows.find(a => a.name === name);
> 92	        if (hit) return hit;
> 93	        if (rows.length < 10) break; // page size do backend = 10
> 94	    }
> 95	    return null;
> 96	}
> 97	
> 98	async function ensureAutomation(token, symbol, name, conditions, indexes, orderTemplateId) {
> 99	    const existing = await findAutomationByName(token, name);
> 100	    if (existing) return `automação "${name}" já existe (id ${existing.id}, isActive=${existing.isActive})`;
> 101	    if (DRY) return `[DRY] POST automação "${name}" INATIVA\n      cond: ${conditions}\n      idx:  ${indexes}`;
> 102	    const r = await req('POST', '/automations', token, {
> 103	        name, symbol, indexes, conditions, isActive: false, logs: true, schedule: null,
> 104	        actions: [{ type: 'ORDER', orderTemplateId }],
> 105	    });
> 106	    if (r.status !== 201) throw new Error(`falha ao criar automação ${name}: ${r.status} ${JSON.stringify(r.body)}`);
> 107	    return `automação "${name}" criada (id ${r.body.id}, INATIVA)`;
> 108	}
> 109	
> 110	async function setupSymbol(token, symbol) {
> 111	    const K = k => `${symbol}:${k}`;
> 112	    console.log(`\n## ${symbol}`);
> 113	    console.log('- ' + await ensureMonitor(token, symbol));
> 114	
> 115	    const buyTpl = await ensureTemplate(token, symbol, `Farm Buy ${symbol}`, 'BUY', {
> 116	        type: 'LIMIT', limitPrice: `MEMORY['${K('BOOK')}'].current.bestAsk * ${(1 + BUF).toFixed(4)}`, limitPriceMultiplier: 1,
> 117	        quantity: 'MIN_NOTIONAL', quantityMultiplier: SIZE_MULT,
> 118	    });
> 119	    console.log('- ' + buyTpl.msg);
> 120	    const sellTpl = await ensureTemplate(token, symbol, `Farm Sell ${symbol}`, 'SELL', {
> 121	        type: 'LIMIT', limitPrice: `MEMORY['${K('BOOK')}'].current.bestBid * ${(1 - BUF).toFixed(4)}`, limitPriceMultiplier: 1,
> 122	        quantity: 'LAST_ORDER_QTY', quantityMultiplier: 1, // vende o lote comprado (a última ordem foi a compra)
> 123	    });
> 124	    console.log('- ' + sellTpl.msg);
> 125	
> 126	    // COMPRA: dip (RSI<lo) fora de bear/trend. Condition regex-safe (validateConditions exige cada cláusula
> 127	    // = MEMORY[...]OP valor, SEM espaços/||/guards soltos). O REGIME vai no INDEX → isChecked é o FAIL-SAFE
> 128	    // (sem regime conhecido a automação NÃO avalia). invertCondition no RSI → dispara só na TRANSIÇÃO p/ baixo
> 129	    // de lo (anti-empilhamento). v1 = 1 lote simples; sem trava de posição → pode haver DCA leve em re-cruzamentos
> 130	    // (a venda realiza a última compra via LAST_ORDER_QTY; rastreio multi-lote/FARM_QTY é refino — §5 do doc).
> 131	    const buyCond = `MEMORY['${K(RSI_KEY_SUFFIX)}'].current<${RSI_LO} && MEMORY['${K('REGIME')}']!=='bear' && MEMORY['${K('REGIME')}']!=='trend'`;
> 132	    console.log('- ' + await ensureAutomation(token, symbol, `Farm Buy ${symbol}`, buyCond, `${K(RSI_KEY_SUFFIX)},${K('REGIME')}`, buyTpl.id));
> 133	
> 134	    // VENDA no-loss: tem posição (última ordem = compra) E o bestBid já dá lucro sobre o preço de compra.
> 135	    // Index = BOOK,LAST_ORDER → isChecked garante AMBOS presentes (sem guards soltos; até a 1ª compra não avalia).
> 136	    // invertCondition no BOOK → realiza só na TRANSIÇÃO em que o bestBid cruza o alvo (anti-empilhamento), indep. do RSI.
> 137	    const sellCond = `MEMORY['${K('LAST_ORDER')}'].side==='BUY' && MEMORY['${K('BOOK')}'].current.bestBid>MEMORY['${K('LAST_ORDER')}'].avgPrice*${(1 + PROFIT).toFixed(4)}`;
> 138	    console.log('- ' + await ensureAutomation(token, symbol, `Farm Sell ${symbol}`, sellCond, `${K('BOOK')},${K('LAST_ORDER')}`, sellTpl.id));
> 139	}
> 140	
> 141	(async () => {
> 142	    if (!EM || !PW) { console.error('faltam credenciais (EM/PW ou TRADEUX_EMAIL/TRADEUX_PASSWORD)'); process.exit(1); }
> 143	    const login = await req('POST', '/login', null, { email: EM, password: PW });
> 144	    const token = login.body && login.body.token;
> 145	    if (!token) { console.error('LOGIN_FAIL ' + login.status); process.exit(1); }
> 146	
> 147	    console.log(`# Setup FARM no-loss — ${SYMBOLS.join(', ')} | RSI<${RSI_LO} compra · lucro-alvo ${(PROFIT * 100).toFixed(1)}% · buffer ${(BUF * 100).toFixed(1)}% · size ${SIZE_MULT}×MIN_NOTIONAL${DRY ? '   [DRY-RUN: nada será aplicado]' : ''}`);
> 148	
> 149	    for (const symbol of SYMBOLS) await setupSymbol(token, symbol);
> 150	
> 151	    console.log(`\n${DRY ? 'DRY-RUN OK (nada aplicado).' : 'PRONTO — monitores ATIVOS, automações de farm INATIVAS.'}`);
> 152	    console.log(`Para ATIVAR (1 alt por vez, com gate): garanta o REGIME da alt (REGIME_SYMBOLS ou automação ativa)`);
> 153	    console.log(`e dê start nas automações "Farm Buy/Sell <sym>". A venda é no-loss (só realiza com lucro real).`);
> 154	})();
> 155	
> ```

## 🤖 Claude *(14:57:08)*


## 🤖 Claude *(14:57:09)*

Agora vou ler o `setup-harvester.js` (o padrão `×2` do commit 7aebc26) e o `calcQty` no beholder, mais como o `MIN_NOTIONAL` é resolvido.

## 🤖 Claude *(14:57:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"===== HARVESTER: SIZE_MULT lines =====\" && grep -n \"SIZE_MULT\\|MIN_NOTIONAL\\|quantityMultiplier\\|HARVEST_SIZE\" backend/scripts/setup-harvester.js && echo \"\" && echo \"===== beholder calcQty + MIN_NOTIONAL =====\" && grep -n \"calcQty\\|MIN_NOTIONAL\\|Math.floor\\|minNotional\\|NOTIONAL\\|stepSize\\|quantityMultiplier\" backend/src/beholder.js",
  "description": "Grep harvester SIZE_MULT and beholder calcQty/MIN_NOTIONAL"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== HARVESTER: SIZE_MULT lines =====
> 14: *   - template "Harvest Buy <sym>"  LIMIT marketável (bestAsk×(1+buf)) MIN_NOTIONAL×size — compartilhado pelas rungs.
> 24: *        HARVEST_BUFFER (0.003), HARVEST_SIZE_MULT (2 = MIN_NOTIONAL×2 ~$9; ×1 falha o filtro NOTIONAL $5)
> 32:const SIZE_MULT = parseFloat(process.env.HARVEST_SIZE_MULT || '2'); // MIN_NOTIONAL×2 (~$9 a 62k): ×1 dá ~$4,4 e FALHA o filtro NOTIONAL ($5) ao disparar (validado ao vivo: -1013)
> 59:    if (DRY) return { id: 0, msg: `[DRY] POST template "${name}" (${opts.type} ${side} qty ${opts.quantity}×${opts.quantityMultiplier || 1})` };
> 64:        quantity: opts.quantity, quantityMultiplier: opts.quantityMultiplier || 1,
> 102:    console.log(`# Setup HARVESTER de dislocação — ${SYMBOL} | rungs ${RUNGS.map(r => '-' + (r * 100).toFixed(0) + '%').join(', ')} abaixo do FAIR (mainnet) · lucro-alvo ${(PROFIT * 100).toFixed(1)}% · buffer ${(BUF * 100).toFixed(1)}% · size ${SIZE_MULT}×MIN_NOTIONAL${DRY ? '   [DRY-RUN: nada será aplicado]' : ''}`);
> 106:        quantity: 'MIN_NOTIONAL', quantityMultiplier: SIZE_MULT,
> 111:        quantity: 'HARVEST_QTY', quantityMultiplier: 1, // vende o bucket tático inteiro (capa na carteira em calcQty)
> 
> ===== beholder calcQty + MIN_NOTIONAL =====
> 196:    factor = Math.floor(newPrice / tickSize);
> 200:function calcQty(orderTemplate, price, symbol) {
> 215:    const multiplier = orderTemplate.quantityMultiplier;
> 216:    const stepSize = parseFloat(symbol.stepSize);
> 225:    else if (orderTemplate.quantity === 'MIN_NOTIONAL') {
> 226:        newQty = (parseFloat(symbol.minNotional) / parseFloat(price)) * (multiplier < 1 ? 1 : multiplier);
> 259:    factor = Math.floor(newQty / stepSize);
> 260:    return (factor * stepSize).toFixed(symbol.basePrecision);
> 275:    const multiplier = orderTemplate.quantityMultiplier;
> 285:    else if (orderTemplate.quantity === 'MIN_NOTIONAL') {
> 286:        return (parseFloat(symbol.minNotional) * (multiplier < 1 ? 1 : multiplier)).toFixed(symbol.quotePrecision);
> 328:    const quantity = calcQty(orderTemplate, tpPrice, symbol);
> 429:    const isDynamicBuy = order.side === 'BUY' && ['MIN_NOTIONAL', 'MAX_WALLET'].includes(orderTemplate.quantity);
> 431:        && (isDynamicBuy || orderTemplate.quantity === 'MIN_NOTIONAL')) {
> 442:        const quantity = calcQty(orderTemplate, price, symbol, false);
> 445:            throw new Error(`Error in calcQty function, params: OTID ${orderTemplate.id}, $: ${price}, qty: ${quantity}`);
> 589:            quantityMultiplier: 1,
> 605:            quantityMultiplier: 1,
> 617:        const priceFactor = Math.floor((lowerLimit + (priceLevel * i)) / tickSize);
> ```

## 🤖 Claude *(14:57:15)*


## 🤖 Claude *(14:57:16)*

Vou ler o `calcQty` completo (linhas 196–290) pra entender exatamente como o `Math.floor` por `stepSize` interage com o `minNotional` e o multiplicador.

## 🤖 Claude *(14:57:16)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/src/beholder.js",
  "offset": 196,
  "limit": 95
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 196	    factor = Math.floor(newPrice / tickSize);
> 197	    return (factor * tickSize).toFixed(symbol.quotePrecision);
> 198	}
> 199	
> 200	function calcQty(orderTemplate, price, symbol) {
> 201	    let asset;
> 202	
> 203	    if (orderTemplate.side === 'BUY') {
> 204	        asset = parseFloat(MEMORY[`${symbol.quote}:WALLET`]);
> 205	        if (!asset) throw new Error(`There is no ${symbol.quote} in your wallet to place a buy.`);
> 206	    }
> 207	    else {
> 208	        asset = parseFloat(MEMORY[`${symbol.base}:WALLET`]);
> 209	        if (!asset) throw new Error(`There is no ${symbol.base} in your wallet to place a sell.`);
> 210	    }
> 211	
> 212	    let qty = orderTemplate.quantity.replace(',', '.');
> 213	    if (parseFloat(qty)) return qty;
> 214	
> 215	    const multiplier = orderTemplate.quantityMultiplier;
> 216	    const stepSize = parseFloat(symbol.stepSize);
> 217	
> 218	    let newQty, factor;
> 219	    if (orderTemplate.quantity === 'MAX_WALLET') {
> 220	        if (orderTemplate.side === 'BUY')
> 221	            newQty = (parseFloat(asset) / parseFloat(price)) * (multiplier > 1 ? 1 : multiplier);
> 222	        else
> 223	            newQty = parseFloat(asset) * (multiplier > 1 ? 1 : multiplier);
> 224	    }
> 225	    else if (orderTemplate.quantity === 'MIN_NOTIONAL') {
> 226	        newQty = (parseFloat(symbol.minNotional) / parseFloat(price)) * (multiplier < 1 ? 1 : multiplier);
> 227	    }
> 228	    else if (orderTemplate.quantity === 'LAST_ORDER_QTY') {
> 229	        const lastOrder = MEMORY[`${orderTemplate.symbol}:LAST_ORDER`];
> 230	        if (!lastOrder)
> 231	            throw new Error(`There is no last order to use as qty reference for ${orderTemplate.symbol}.`);
> 232	
> 233	        newQty = parseFloat(lastOrder.quantity) * multiplier;
> 234	        if (orderTemplate.side === 'SELL' && newQty > asset) newQty = asset;
> 235	    }
> 236	    else if (orderTemplate.quantity === 'TREND_QTY') {
> 237	        // Posição acumulada pelo Trend Following (escrita no fill por app-em.updateTrendPosition):
> 238	        // id6 (golden) soma; id7 (death) vende ESTA qty (não a LAST_ORDER, que é compartilhada com a id3).
> 239	        const trendQty = parseFloat(MEMORY[`${orderTemplate.symbol}:TREND_QTY`]);
> 240	        if (!trendQty || trendQty <= 0)
> 241	            throw new Error(`There is no trend position (TREND_QTY) to use as qty reference for ${orderTemplate.symbol}.`);
> 242	
> 243	        newQty = trendQty * multiplier;
> 244	        if (orderTemplate.side === 'SELL' && newQty > asset) newQty = asset; // capa na carteira (fees/saldo)
> 245	    }
> 246	    else if (orderTemplate.quantity === 'HARVEST_QTY') {
> 247	        // Bucket TÁTICO do Harvester de dislocação (escrito no fill por app-em.updateHarvestPosition):
> 248	        // MEMORY['<sym>:HARVEST'] = { qty, cost }. A venda no-loss vende ESTA qty (só o que o harvester
> 249	        // comprou), NUNCA o cofre principal de BTC. Falha-fechado se vazio (sem bucket, não vende).
> 250	        const harvest = MEMORY[`${orderTemplate.symbol}:HARVEST`];
> 251	        const harvestQty = harvest ? parseFloat(harvest.qty) : NaN;
> 252	        if (!harvestQty || harvestQty <= 0)
> 253	            throw new Error(`There is no harvest position (HARVEST) to use as qty reference for ${orderTemplate.symbol}.`);
> 254	
> 255	        newQty = harvestQty * multiplier;
> 256	        if (orderTemplate.side === 'SELL' && newQty > asset) newQty = asset; // capa na carteira (fees/saldo)
> 257	    }
> 258	
> 259	    factor = Math.floor(newQty / stepSize);
> 260	    return (factor * stepSize).toFixed(symbol.basePrecision);
> 261	}
> 262	
> 263	function hasEnoughAssets(symbol, order, price) {
> 264	    const qty = parseFloat(order.quantity);
> 265	    if (order.side === 'BUY')
> 266	        return parseFloat(MEMORY[`${symbol.quote}:WALLET`]) >= (price * qty);
> 267	    else
> 268	        return parseFloat(MEMORY[`${symbol.base}:WALLET`]) >= qty;
> 269	}
> 270	
> 271	function calcQuoteQty(orderTemplate, symbol) {
> 272	    if (orderTemplate.type !== 'MARKET' || parseFloat(orderTemplate.quantity))
> 273	        throw new Error(`Only MARKET orders can cal quote qty.`);
> 274	
> 275	    const multiplier = orderTemplate.quantityMultiplier;
> 276	
> 277	    if (orderTemplate.quantity === 'MAX_WALLET') {
> 278	        if (orderTemplate.side !== 'BUY') throw new Error(`Only MARKET BUY orders can calc quote qty with MAX_WALLET`);
> 279	
> 280	        const asset = MEMORY[`${symbol.quote}:WALLET`];
> 281	        if (!asset) throw new Error(`There is no ${symbol.quote} in your wallet to place a buy.`);
> 282	
> 283	        return (parseFloat(asset) * (multiplier > 1 ? 1 : multiplier)).toFixed(symbol.quotePrecision);
> 284	    }
> 285	    else if (orderTemplate.quantity === 'MIN_NOTIONAL') {
> 286	        return (parseFloat(symbol.minNotional) * (multiplier < 1 ? 1 : multiplier)).toFixed(symbol.quotePrecision);
> 287	    }
> 288	
> 289	    throw new Error(`Invalid order template quantity ${orderTemplate.quantity}`);
> 290	}
> ```

## 🤖 Claude *(14:57:51)*


## 🤖 Claude *(14:57:54)*

Agora entendo a matemática exatamente. O `calcQty` faz `newQty = (minNotional/price) * mult`, depois `Math.floor(newQty/stepSize)*stepSize`. O flooring por `stepSize` derruba o notional abaixo de `minNotional` — daí o `-1013`. Com `×2`, sobra margem suficiente desde que `minNotional > stepSize×price`. Preciso dos valores reais por par. Vou inspecionar o compose/.env e a tabela `symbols`.

## 🤖 Claude *(14:57:56)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"===== DB service in compose =====\" && grep -nA15 \"db:\" docker-compose.yml | head -40 && echo \"\" && echo \"===== DB_* / MYSQL_* in .env =====\" && grep -nE \"DB_|MYSQL_\" .env | sed -E 's/(PASS[A-Z_]*=).*/\\1***REDACTED***/' && echo \"\" && echo \"===== containers (as gcrux) =====\" && sudo -u gcrux-tradeux docker ps --format '{{.Names}}\\t{{.Image}}\\t{{.Status}}' 2>&1 | head",
  "description": "Inspect DB service, env, and running containers"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== DB service in compose =====
> 7:  db:
> 8-    image: mysql:8.0
> 9-    restart: unless-stopped
> 10-    environment:
> 11-      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PWD}
> 12-      MYSQL_DATABASE: ${DB_NAME}
> 13-      MYSQL_USER: ${DB_USER}
> 14-      MYSQL_PASSWORD: ${DB_PWD}
> 15-    volumes:
> 16-      - db_data:/var/lib/mysql
> 17-    healthcheck:
> 18-      test: ["CMD", "mysqladmin", "ping", "-h", "127.0.0.1"]
> 19-      interval: 10s
> 20-      timeout: 5s
> 21-      retries: 12
> 22-    deploy:
> --
> 35:      db:
> 36-        condition: service_healthy
> 37-    deploy:
> 38-      resources:
> 39-        limits:
> 40-          memory: 384M
> 41-    networks: [tradeux]
> 42-
> 43-  agent:
> 44-    build:
> 45-      context: .
> 46-      dockerfile: tradeux-agent/Dockerfile
> 47-    restart: unless-stopped
> 48-    # Roda como o dono do bind-mount do journal (gcrux-tradeux = 1011:1013 nesta máquina) p/ que
> 49-    # os arquivos do journal nasçam como gcrux (não root) e a escrita funcione sem sudo — evita a
> 50-    # reincidência do gotcha de ownership (mesma classe do .git). Overridável por AGENT_UID/GID.
> 
> ===== DB_* / MYSQL_* in .env =====
> 23:DB_NAME=tradeux
> 24:DB_USER=tradeux
> 25:DB_PWD=2e462b7cdff790fb6d6290a0f5a6b25b
> 26:DB_ROOT_PWD=c6a84c146bad3dcb878b251528481fc5
> 27:DB_HOST=db
> 28:DB_PORT=3306
> 29:DB_DIALECT=mysql
> 30:DB_LOGS=false
> 31:DB_SSL=false
> 
> ===== containers (as gcrux) =====
> tradeux-backend-1	tradeux-backend	Up 11 hours
> tradeux-agent-1	tradeux-agent	Up 12 hours
> tradeux-frontend-1	tradeux-frontend	Up 12 hours
> tradeux-db-1	mysql:8.0	Up 6 days (healthy)
> open-design	vanjayak/open-design:latest	Up 2 weeks (healthy)
> supabase_studio_engineer	public.ecr.aws/supabase/studio:2026.04.28-sha-89d08a2	Up 2 weeks (healthy)
> supabase_pg_meta_engineer	public.ecr.aws/supabase/postgres-meta:v0.96.4	Up 2 weeks (healthy)
> supabase_storage_engineer	public.ecr.aws/supabase/storage-api:v1.54.1	Up 2 weeks (healthy)
> supabase_rest_engineer	public.ecr.aws/supabase/postgrest:v14.10	Up 2 weeks
> supabase_realtime_engineer	public.ecr.aws/supabase/realtime:v2.86.3	Up 2 weeks (healthy)
> ```

## 🤖 Claude *(14:58:33)*


## 🤖 Claude *(14:58:35)*

DB é `tradeux-db-1` (MySQL 8). A verificação se reduz a um ponto preciso: o notional no pior caso (após o `Math.floor`) = `2×minNotional − stepSize×preço`. Ou seja, o que importa por par é a granularidade `stepSize×preço` vs `minNotional` — e isso na verdade pesa mais em moeda CARA com step grosso (BNB) do que na ADA barata. Vou puxar os valores reais da tabela `symbols` e os templates atuais.

## 🤖 Claude *(14:58:38)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sudo -u gcrux-tradeux docker exec -e MYSQL_PWD=2e462b7cdff790fb6d6290a0f5a6b25b tradeux-db-1 mysql -u tradeux tradeux -t -e \"\nSELECT symbol, base, quote, minNotional, stepSize, tickSize, basePrecision, quotePrecision\nFROM symbols\nWHERE symbol IN ('BTCUSDT','LTCUSDT','BNBUSDT','ADAUSDT')\nORDER BY symbol;\n\" 2>&1 | grep -v \"Using a password\"",
  "description": "Query symbols filters for BTC/LTC/BNB/ADA"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> +---------+------+-------+-------------+------------+------------+---------------+----------------+
> | symbol  | base | quote | minNotional | stepSize   | tickSize   | basePrecision | quotePrecision |
> +---------+------+-------+-------------+------------+------------+---------------+----------------+
> | ADAUSDT | ADA  | USDT  | 5.00000000  | 0.10000000 | 0.00010000 |             8 |              8 |
> | BNBUSDT | BNB  | USDT  | 5.00000000  | 0.00100000 | 0.01000000 |             8 |              8 |
> | BTCUSDT | BTC  | USDT  | 5.00000000  | 0.00001000 | 0.01000000 |             8 |              8 |
> | LTCUSDT | LTC  | USDT  | 5.00000000  | 0.00100000 | 0.01000000 |             8 |              8 |
> +---------+------+-------+-------------+------------+------------+---------------+----------------+
> ```

## 🤖 Claude *(14:58:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sudo -u gcrux-tradeux docker exec -e MYSQL_PWD=2e462b7cdff790fb6d6290a0f5a6b25b tradeux-db-1 mysql -u tradeux tradeux -t -e \"\nSELECT id, name, symbol, side, type, quantity, quantityMultiplier, limitPrice\nFROM orderTemplates\nWHERE name LIKE 'Farm Buy%' OR name LIKE 'Farm Sell%'\nORDER BY name;\n\" 2>&1 | grep -v \"Using a password\"",
  "description": "Query current Farm order templates"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> +----+-------------------+---------+------+-------+----------------+--------------------+-------------------------------------------------+
> | id | name              | symbol  | side | type  | quantity       | quantityMultiplier | limitPrice                                      |
> +----+-------------------+---------+------+-------+----------------+--------------------+-------------------------------------------------+
> |  9 | Farm Buy ADAUSDT  | ADAUSDT | BUY  | LIMIT | MIN_NOTIONAL   |               1.00 | MEMORY['ADAUSDT:BOOK'].current.bestAsk * 1.0030 |
> |  7 | Farm Buy BNBUSDT  | BNBUSDT | BUY  | LIMIT | MIN_NOTIONAL   |               1.00 | MEMORY['BNBUSDT:BOOK'].current.bestAsk * 1.0030 |
> |  5 | Farm Buy LTCUSDT  | LTCUSDT | BUY  | LIMIT | MIN_NOTIONAL   |               1.00 | MEMORY['LTCUSDT:BOOK'].current.bestAsk * 1.0030 |
> | 10 | Farm Sell ADAUSDT | ADAUSDT | SELL | LIMIT | LAST_ORDER_QTY |               1.00 | MEMORY['ADAUSDT:BOOK'].current.bestBid * 0.9970 |
> |  8 | Farm Sell BNBUSDT | BNBUSDT | SELL | LIMIT | LAST_ORDER_QTY |               1.00 | MEMORY['BNBUSDT:BOOK'].current.bestBid * 0.9970 |
> |  6 | Farm Sell LTCUSDT | LTCUSDT | SELL | LIMIT | LAST_ORDER_QTY |               1.00 | MEMORY['LTCUSDT:BOOK'].current.bestBid * 0.9970 |
> +----+-------------------+---------+------+-------+----------------+--------------------+-------------------------------------------------+
> ```

## 🤖 Claude *(14:59:23)*


## 🤖 Claude *(14:59:28)*

Dados reais obtidos. Dois pontos importantes:

1. **Os IDs do template são 5/7/9** (Farm Buy LTC/BNB/ADA), não 9/11/13 — esses são os IDs das *automações*. O `WHERE name LIKE 'Farm Buy%'` que a tarefa especificou acerta os 3 templates BUY corretos (5/7/9) e evita essa confusão. Há exatamente 3.

2. Todos têm `minNotional=$5`. A granularidade `stepSize×preço` (a perda do flooring) é: LTC=0,042 · BNB=0,60 · ADA=0,016. Ou seja, a **ADA é na verdade a MAIS segura** (step×preço minúsculo), ao contrário do que o aviso da tarefa sugeria — o risco residual seria em moeda cara/step grosso, e o BNB já está folgado.

Vou confirmar com **preços ao vivo** (a fonte exata que a ordem usaria) pra fechar a verificação numérica. Deixa eu ver pra qual ambiente o backend aponta e puxar os preços.

## 🤖 Claude *(14:59:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"===== Binance endpoint (.env) =====\" && grep -nE \"BINANCE|API_URL|STREAM|TESTNET\" .env | sed -E 's/(KEY[A-Z_]*=|SECRET[A-Z_]*=).*/\\1***REDACTED***/' && echo \"\" && echo \"===== live prices from backend container =====\" && for S in LTCUSDT BNBUSDT ADAUSDT BTCUSDT; do P=$(sudo -u gcrux-tradeux docker exec tradeux-backend-1 node -e \"fetch('https://testnet.binance.vision/api/v3/ticker/price?symbol=$S').then(r=>r.json()).then(j=>console.log(j.price)).catch(e=>console.log('ERR',e.message))\" 2>/dev/null); echo \"$S = $P\"; done",
  "description": "Check Binance env and fetch live testnet prices"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===== Binance endpoint (.env) =====
> 9:REACT_APP_API_URL=https://tradeux.gcrux.com/api
> 11:# Stream publico Binance — TESTNET (inicial; troque p/ mainnet no painel)
> 38:# ---------- Binance — TESTNET (inicial) ----------
> 39:BINANCE_API_URL=https://testnet.binance.vision/api
> 40:BINANCE_STREAM_URL=wss://stream.testnet.binance.vision/ws
> 41:BINANCE_SAPI_URL=https://testnet.binance.vision/sapi/v1/
> 50:BINANCE_BLVT=false
> 51:BINANCE_LOGS=false
> 
> ===== live prices from backend container =====
> LTCUSDT = 42.20000000
> BNBUSDT = 588.57000000
> ADAUSDT = 0.16590000
> BTCUSDT = 62100.87000000
> ```

## 🤖 Claude *(14:59:47)*


## 🤖 Claude *(14:59:48)*

Preços ao vivo confirmados (testnet, a fonte exata da ordem): LTC=$42,20 · BNB=$588,57 · ADA=$0,1659. Vou replicar o `calcQty` exato (incluindo o buffer de +0,3% do limit marketável) pra ×1 e ×2, e ver o notional resultante de cada par.

## 🤖 Claude *(14:59:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sudo -u gcrux-tradeux docker exec tradeux-backend-1 node -e '\nconst syms = [\n  {s:\"LTCUSDT\", step:0.001,  px:42.20},\n  {s:\"BNBUSDT\", step:0.001,  px:588.57},\n  {s:\"ADAUSDT\", step:0.1,    px:0.16590},\n  {s:\"BTCUSDT\", step:0.00001,px:62100.87},\n];\nconst MN = 5, BUF = 1.003;\nconst f = n => n.toFixed(4);\nconsole.log(\"sym       mult  limitPx      qty           notional   verdict\");\nfor (const {s,step,px} of syms){\n  const lp = px*BUF;\n  for (const mult of [1,2]){\n    const raw = (MN/lp)*(mult<1?1:mult);\n    const qty = Math.floor(raw/step)*step;\n    const notional = qty*lp;\n    const ok = notional >= MN ? \"PASS (>=$5)\" : \"FAIL (<$5) -1013\";\n    console.log(`${s.padEnd(9)} x${mult}   ${f(lp).padStart(9)}   ${qty.toFixed(8).padStart(12)}   $${f(notional).padStart(7)}  ${ok}`);\n  }\n}\n' 2>/dev/null",
  "description": "Replicate calcQty exactly for x1 and x2 across symbols"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> sym       mult  limitPx      qty           notional   verdict
> LTCUSDT   x1     42.3266     0.11800000   $ 4.9945  FAIL (<$5) -1013
> LTCUSDT   x2     42.3266     0.23600000   $ 9.9891  PASS (>=$5)
> BNBUSDT   x1    590.3357     0.00800000   $ 4.7227  FAIL (<$5) -1013
> BNBUSDT   x2    590.3357     0.01600000   $ 9.4454  PASS (>=$5)
> ADAUSDT   x1      0.1664    30.00000000   $ 4.9919  FAIL (<$5) -1013
> ADAUSDT   x2      0.1664    60.00000000   $ 9.9839  PASS (>=$5)
> BTCUSDT   x1   62287.1726     0.00008000   $ 4.9830  FAIL (<$5) -1013
> BTCUSDT   x2   62287.1726     0.00016000   $ 9.9659  PASS (>=$5)
> ```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-09 - Audit trading bot order status and agent KPI updates]]
> * **Próxima Sessão**: [[2026-06-09 - Fix settings password overwrite bug preventing logins]]
%% --- TIMELINE END --- %%

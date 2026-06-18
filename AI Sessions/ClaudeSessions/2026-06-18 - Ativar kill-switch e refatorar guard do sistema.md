# Ativar kill-switch e refatorar guard do sistema
**Date:** 2026-06-18 | **Session ID:** `d7c8c9da-f4e1-4286-b1f5-5d9a47531010`

---

## 👤 User *(12:48:10)*

<command-message>handson</command-message>
<command-name>/handson</command-name>

## 👤 User *(12:48:10)*

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


## 🤖 Claude *(12:48:13)*


## 🤖 Claude *(12:48:14)*


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
> Output too large (117.8KB). Full output saved to: /home/ubuntu/.claude/projects/-home-gcrux-tradeux/d7c8c9da-f4e1-4286-b1f5-5d9a47531010/tool-results/b4ez7v40g.txt
> 
> Preview (first 2KB):
> # TradeUX — HANDOFF (single source of truth)
> 
> > ShakeHands continuity doc. `/handson` reads this FIRST. Newest record at the bottom.
> > Project: **TradeUX** — Beholder-based multi-coin Binance Spot bot + LLM agent (**mainnet/testnet dual-env**).
> > Updated: **2026-06-17** · Phase: **GO-LIVE MAINNET — CONGELADO (`TRADING_HALT=true`) · descongelamento EM CURSO** · Meta: **realista ≈ flat com ~$150** (o +3 BTC era do testnet) · Vivo==master==origin==**`baf0f4b`**
> 
> > 🛑 **LEIA ANTES DE TUDO (2026-06-15):** o sistema está em **MAINNET REAL** (`settings.useTestnet=0`, ~$150 USDT) e **CONGELADO** (`TRADING_HALT=true` no `.env` → nada negocia; é o kill-switch novo no `exchange.js`). Money-path foi blindado (`96915e0`) e o bug P0 do Farm Sell foi corrigido (`c163112`). **DESCOBERTA CRÍTICA: o harvester está MORTO no mainnet** (o edge de −3% era arbitragem testnet-vs-mainnet; no mainnet o book do bot É o FAIR). O ÚNICO edge real é o **Trend** (pequeno, mensal). **Antes de descongelar:** (1) trava `FARM_SELLING` (follow-up); (2) dono confere saque-OFF+IP da chave Binance; (3) decidir re-design do harvester. Detalhes nos SEALs de 2026-06-15 (fim do doc) + memória `tradeux-mainnet-go-live`. **2026-06-16:** Cockpit Intelligence read-only NO AR (brain computa analytics 1m + agente lê/reporta; commit `1660871`) — a brain reporta **EV −0,16% / pHit 0,6%** (scalp 1m é −EV, dado real). Fix do **−1013** no `calcQty` + template Trend ×3 (commit `2528a5d`). **Auditoria adversarial independente** confirmou 7 achados p/ o descongelamento → ver SEAL 2026-06-16. ⚠️ O "vídeo viral Fable 5/Polymarket 205x" do X é **golpe de referral** — NÃO clicar/depositar.
> 
> ## ⚡ FIRST ACTION FOR NEXT AGENT
> 0. 🏗️ **ARQUITETURA FARM-AND-FUNNEL COMPLETA E NO AR** (sessão 2026-06-08): **15 automações ativas** — Farm no-loss +
>    Trend SMA50/200 nas alts **LTC/BNB/ADA** (id 9-20) + id2/id6/id7 do BTC; **funil em SHADOW**; id3 pausada. Coordenação
> ...
> </persisted-output>
> ```

## 🤖 Claude *(12:48:15)*


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
> baf0f4b feat(safety): 3 pre-reqs de descongelamento — FARM_SELLING, TREND_QTY persist, teto
> 7ec6e75 fix(cockpit): baseline=null p/ simbolos nao-flow-gated (mata gate-fantasma da alt)
> e27339a fix(exchange): teto MAX_ORDER_NOTIONAL cobre MARKET-por-qty (deriva preco do MINI_TICKER)
> 0b1554d docs(agent): doutrina GATE != TRIGGER no SYSTEM_PROMPT (fecha a classe gate-aberto-mas-condicao)
> 2c8655c fix(cockpit-ui): painel "Trade bridges" consome o gate symbol-aware (alt = fluxo informativo)
> 8884bd3 fix(cockpit): gate de acumulacao symbol-aware (alt FARM nao gateia por fluxo)
> 37ed4b1 refactor(agent): consolida doutrina anti-ruido do SYSTEM_PROMPT num bloco "DIVERGENCIAS ESPERADAS"
> ```

## 🤖 Claude *(12:48:15)*


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

## 🤖 Claude *(12:48:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sudo -n -u gcrux-tradeux bash -lc 'cd /home/gcrux-tradeux/tradeux && docker compose ps' 2>/dev/null || docker ps --filter name=tradeux --format \"table {{.Names}}\\t{{.Status}}\"",
  "description": "Check Docker stack status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> NAME                 IMAGE              COMMAND                  SERVICE    CREATED        STATUS                PORTS
> tradeux-agent-1      tradeux-agent      "docker-entrypoint.s…"   agent      18 hours ago   Up 18 hours           
> tradeux-backend-1    tradeux-backend    "docker-entrypoint.s…"   backend    18 hours ago   Up 18 hours           3001/tcp
> tradeux-db-1         mysql:8.0          "docker-entrypoint.s…"   db         2 weeks ago    Up 2 days (healthy)   3306/tcp, 33060/tcp
> tradeux-frontend-1   tradeux-frontend   "/docker-entrypoint.…"   frontend   38 hours ago   Up 38 hours           127.0.0.1:8090->80/tcp
> ```

## 🤖 Claude *(12:48:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "curl -s -m5 -o /dev/null -w \"site https://tradeux.gcrux.com -> %{http_code}\\n\" https://tradeux.gcrux.com/",
  "description": "Check site HTTP status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> site https://tradeux.gcrux.com -> 200
> ```

## 🤖 Claude *(12:48:22)*


## 🤖 Claude *(12:48:22)*

Working tree is clean. Let me read the tail of HANDOFF.md (newest record) to get the latest seal and Next Steps.

## 🤖 Claude *(12:48:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "tail -c 9000 /home/gcrux-tradeux/HANDOFF.md",
  "description": "Read tail of HANDOFF.md for newest seal and next steps"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> * Defesa em profundidade independente do prompt (`tradeux-agent/src/notifyDedup.js`, puro/testável): normaliza+canoniza sinônimos PT/EN, chave de tópico = vocabulário de domínio ∪ tickers ∪ transições direcionais, **Jaccard ≥ 0.6**; guards anti-falso-positivo (símbolo distinto / transição inversa / marcador de evento inédito). Roda ANTES do cap 2/ciclo (suprimido não consome o cap). **Self-test com mensagens REAIS do Telegram (15 casos) wired no CI.** Red-team pegou B6 CRÍTICO (ticker por sufixo p/ alts novas) → corrigido. QA-PASS+TL-APPROVE.
> 3. **`bf254a0` fix(cockpit): reason reflete o regime real** — mostrava "range + fluxo ok" com regime `mixed` (auto-contradição); agora interpola o regime. Decisão do gate intocada (mixed é mean-reversion = correto). QA-PASS+TL-APPROVE.
> 4. **`37ed4b1` refactor(agent): consolida doutrina anti-ruído num bloco `DIVERGÊNCIAS ESPERADAS`** — 3 regras anti-ruído repetidas → 1 bloco rotulado (6→7 itens) + ponteiros. Zero regra perdida. QA-PASS+TL-APPROVE.
> 5. **`8884bd3` fix(cockpit): gate de acumulação SYMBOL-AWARE (BUG REAL).** `deriveGates` aplicava o filtro de fluxo da baseline BTC a TODOS os símbolos; mas só a id2 (BTC) é flow-gated (`setup-flow-gate.js`), o FARM das alts gateia só RSI+regime (`setup-farm.js:131`). Mostrava alt em capitulação como `buyAllowed=false "baseline veta"`, vetando entrada que a farm VIVA faria. Fix: `deriveGates(regime,flow,symbol)` + `FLOW_GATED` (env, default BTCUSDT) → `buyAllowed = flowGated ? baseline : farm`. QA-PASS (truth-table 24 células)+TL-APPROVE.
> 6. **`2c8655c` fix(cockpit-ui): painel "Trade bridges" consome o gate symbol-aware** — o frontend tinha o MESMO hardcode (`imbalance>-0.4` p/ toda alt); agora consome `cp.symbols[s].gates` (alts: fluxo informativo `.info`/"fluxo·i", não bloqueia). Frontend-only. QA-PASS+TL-APPROVE.
> 7. **`0b1554d` docs(agent): doutrina GATE ≠ TRIGGER (item 7 do bloco).** O agente flagou `farm=true` com RSI 79/66/62 (>35) como incoerência. NÃO é bug: o gate é DOUTRINA de regime/fluxo (`doctrine:true`), NÃO lê RSI; o FARM dispara só no dip RSI<35. Fix agent-side (não cockpit). QA-PASS+TL-APPROVE.
> 
> **Aprendizados duráveis (na memória `tradeux-1m-scalping-and-cockpit`):** (a) o **dedup ESTÁ funcionando** — as ~8 notificações eram TÓPICOS DISTINTOS ao longo de ~10h, não repetição (rodei pelo módulo p/ provar); journal persistido em volume. (b) **VERDICT do TL: a fase de ENUMERAÇÃO REATIVA de coerência do cockpit está DONE** — os 2 sub-eixos de "gate aberto mas X não atendido" cobertos (fluxo `8884bd3` = bug real; RSI/trigger `0b1554d` = leitura). Próximo eixo plausível = notional/saldo; NÃO pré-emptar — o catch-all do prompt ("só sinalize se a fonte VIVA por si só mostrar anomalia") já segura; se aparecer é +1 item incremental.
> 
> **Tech debt / follow-ups (chips abertos, fora do escopo):** (1) notify-dedup por assunto em código foi FEITO (`64752f0`); (2) painel "Trade bridges" FEITO (`2c8655c`); **(3) baseline id2 (RSI<25) é runtime/PATCH, NÃO seedada** (QA flagou — pós-`make nuke` reaplicar manual; dívida já conhecida em `tradeux-regime-gate`). **Descongelamento:** pré-reqs (a)-(e) do SEAL anterior SEGUEM PENDENTES (saque-OFF/IP, desativar harvester, fix P&L BNB, gap teto SELL-by-base, cap diário). **PRs: 0** (trunk-based; tudo já no origin).
> 
> ### 🤝 SEAL — 2026-06-17 (Descongelamento EM CURSO: pré-reqs (a)(b)(d) + cockpit gate-fantasma + 3 BLOQUEADORES — 3 commits, todos QA+TL, 2 workflows adversariais, HALT intacto)
> **Sessão de descongelamento responsável dirigida pelo dono. Vivo==master==origin==`baf0f4b`. 4 containers up, `TRADING_HALT=true` intocado, 0 ordens mainnet, ~$148,84 USDT. PRs: 0 (trunk-based direct-to-master; tudo no origin).**
> 
> **Pré-reqs de descongelamento FECHADOS esta sessão:**
> - **(a) chave Binance saque-OFF + IP travado — FEITO+VERIFICADO.** Dono desmarcou na UI **Enable Withdrawals** (= "saque off"; não existe botão "saque off", é desmarcar Withdrawals) + **Permits Universal Transfer**; restou Reading + Spot Trading; IP **`137.131.243.179`** (= IP de saída do servidor, host==container, via api.ipify). Verifiquei read-only: login + `GET /exchange/balance/USDT` → 200, **USDT 148,84** lido. Saque-OFF NÃO é verificável por leitura (e NÃO se testa saque); confiança = Save na UI. Ver memória `tradeux-mainnet-go-live` item 2.
> - **(b) harvester id22-25 DESATIVADO** (`isActive=0` via `POST /automations/:id/stop`; bucket vazio, BRAIN só 6,7,9-20). `setup-harvester.js` já cria default-OFF → durável até `make nuke`. MORTO no mainnet (edge era artefato testnet).
> - **(d) furo SELL-by-base do riskGuard FECHADO** (`e27339a`): `assertWithinRisk` agora deriva preço (stopPrice senão MINI_TICKER.close via require lazy do beholder) e capa MARKET-por-qty-base. Inerte sob HALT.
> 
> **Cockpit — gate-FANTASMA da alt ELIMINADO** (`7ec6e75`, QA+TL+verif. adversarial, deployado+verificado): o agente notificava "baseline liberado p/ BNBUSDT c/ RSI>25 = incoerência". Raiz estrutural: `deriveGates` expunha `baseline=true` pra ALTS, que NÃO têm módulo baseline (gate de acumulação da alt = FARM). Fix: `baseline = flowGated ? baselineRaw : null` (só BTC expõe baseline; alt = null/n-a). `buyAllowed`/`farm` byte-idênticos (QA: tabela-verdade 60 casos). Verificado ao vivo: BTC `baseline=true`, BNB/LTC/ADA `null`. **TL: é direcional (payload afirmava gate de módulo inexistente), não perseguição-de-view.**
> 
> **3 BLOQUEADORES do flip (`baf0f4b`, QA PASS + TL APPROVE + cético money-path PASS; design→verify e review→verify via workflow adversarial):**
> 1. **Teto:** `MAX_ORDER_NOTIONAL_USDT` 1500→**300** no `.env` (~2× a conta) + doutrina no exchange.js. ⚠️ verificador pegou que reativar **BTC Scalp Excess id38** (hoje `isActive=0`, vende BTC>1.0 a MARKET p/ +3 BTC) exige teto **symbol-aware** — caveat documentado.
> 2. **FARM_SELLING v1** (anti-empilhamento da venda no-loss do Farm): SKIP no place + SET por orderId + RELEASE por **match de orderId** em qualquer terminal — **BRAIN-independente** (mata a perma-trava do stop/start, superior ao HARVEST_SELLING). Sem migration/condition/reload. **Reconstrução-no-boot (loadFarmSellingLocks) + reconciliação partial→cancel DEFERIDAS** — gate: NÃO escalar `FARM_SIZE_MULT` (risco bounded: só remistura alt-wallet, NUNCA o cofre de BTC, nunca oversell além da carteira).
> 3. **TREND_QTY persistido via DERIVE-FROM-ORDERS** (não tabela nova — evitou o double-count): `getTrendPosition` espelha `getFarmPosition` (name LIKE 'Trend %'); `updateTrendPosition` recomputa (removeu accumulator + countedTrendFills → idempotente); `loadTrendPosition` no boot. Sem migration. Posição do golden não orfana num restart.
> 
> **Parecer de READINESS (data-founded, 2 agentes: readiness + modos-de-falha) p/ o dono decidir o flip:** GO-CONDICIONADO, não GO cego. Money-path de ENTRADA + teto/reconcile sólidos; os 2 HIGH eram FARM_SELLING ausente + TREND_QTY não-persistido (AGORA FEITOS). Expectativa REAL = **≈ flat** (canary valida MECÂNICA — fill/fee/slippage reais nunca exercitados, 0 ordens mainnet —, NÃO lucro rápido). Canary recomendado: **um grupo só** (Farm alts id9-14 valida a mecânica em horas; OU Trend id6/7 valida o edge mas pode ficar inerte), NÃO os dois.
> 
> **Estratégia BNB (pedido do dono):** a alavanca real NÃO é especular — é o **desconto de taxa BNB** (0,10%→0,075%, −25% em TODO par → abre margem no edge fino). MAS ligar BNB-fee **acorda o pré-req (c)** (P&L `net` para de descontar fee em BNB → painel mente otimista). ACOPLADOS: fix (c) ANTES de ligar BNB-fee. (O "no-loss" do Farm hoje também não é líquido — irmão do (c).)
> 
> **Gotchas operacionais (DURÁVEIS):** (1) **`TRADING_HALT` e `MAX_ORDER_NOTIONAL` são lidos em `const` no LOAD do exchange.js → NÃO são kill-switch QUENTE.** Botão de pânico real = **`docker compose stop backend`**, não editar `.env`. O cap diário (e) precisa de refactor do guard p/ ler runtime — fecha os dois. (2) **Edit/Write do harness ENVENENA o dono do arquivo** (vira `ubuntu`); `.env` (600) ficou ilegível p/ gcrux → push + docker compose quebrariam. Detectei, `chown` de volta, gravei em `git-ownership-gotcha`. **SEMPRE `chown gcrux-tradeux` após editar arquivos do repo (esp. `.env`) antes de git/docker como gcrux.**
> 
> **⚡ NEXT (falta p/ um flip responsável):** **(e) cap diário −5%** (dono APROVOU o valor) **+ refactor do guard p/ kill-switch quente** (resolve o HALT-frio junto) — É O PRÓXIMO ITEM, é só desenhar/implementar com QA/TL; depois **(c) P&L-BNB + BNB-fee** (acoplados, dono disse "ver depois"); aí **GO do dono** pro flip + canary de um-grupo-só. **Claude NÃO vira o `TRADING_HALT`.** Memórias atualizadas: `tradeux-mainnet-go-live`, `tradeux-harvester-experiment`, `tradeux-1m-scalping-and-cockpit`, `tradeux-trend-following`, `git-ownership-gotcha` + índice.
> ```

## 🤖 Claude *(12:48:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && curl -s -m5 http://127.0.0.1:8090/ -o /dev/null -w \"local frontend -> %{http_code}\\n\" 2>/dev/null; grep -iE 'TRADING_HALT|ALLOW_TRADING|useTestnet' /home/gcrux-tradeux/tradeux/.env 2>/dev/null | sed 's/=.*KEY.*/=<redacted>/' || echo \".env not readable as ubuntu\"",
  "description": "Check local frontend and key env flags"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> local frontend -> 200
> ```

## 🤖 Claude *(12:48:34)*


## 🤖 Claude *(12:48:34)*


🛠️ **Tool Call**: `mcp__ccd_session__mark_chapter`
```json
{
  "title": "Handson pick-up",
  "summary": "Load TradeUX session state via ShakeHands /handson"
}
```

> **Tool Result (mcp__ccd_session__mark_chapter)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Chapter marked: "Handson pick-up". Continue your current work.'}]
> ```

## 🤖 Claude *(12:48:51)*

```
═══════════════════════════════════════════════════
  HANDSON — GO-LIVE MAINNET · CONGELADO (seal 2026-06-17)
═══════════════════════════════════════════════════
🏁 ESTADO     : Mainnet real (~$148,84 USDT) · TRADING_HALT=true · descongelamento EM CURSO
🧾 COMMITS    : baf0f4b feat(safety) 3 pré-reqs (FARM_SELLING/TREND_QTY/teto)
                7ec6e75 fix(cockpit) baseline=null mata gate-fantasma
                e27339a fix(exchange) teto cobre MARKET-por-qty
🐳 STACK      : db healthy · backend up 18h · frontend up 38h · agent up 18h · site 200
📈 BASELINE   : 15 automações ativas (Farm+Trend alts + id2/6/7 BTC) · funil em SHADOW · 0 ordens mainnet (HALT)
🔀 PRs ABERTOS: 0 (trunk-based direct-to-master; tudo no origin)
📂 PENDENTE   : worktree limpo (Vivo==master==origin==baf0f4b)
⚡ PRÓXIMO    : (e) cap diário −5% + refactor do guard → kill-switch QUENTE (resolve o HALT-frio junto)
⚠️ ALERTAS    : TRADING_HALT é const no load (NÃO é kill-switch quente — pânico real = docker compose stop backend);
                Edit/Write do harness envenena dono do .env → chown gcrux-tradeux antes de git/docker
═══════════════════════════════════════════════════
  Pronto pra trabalhar. Aguardando direção.
═══════════════════════════════════════════════════
```

**Contexto rápido do que ficou na mesa** (do último seal, 2026-06-17):

- **Descongelamento em curso, responsável.** Pré-reqs **(a)** saque-OFF+IP, **(b)** harvester desativado e **(d)** furo SELL-by-base do riskGuard — todos **FECHADOS**. Mais o cockpit gate-fantasma das alts eliminado (`7ec6e75`) e os **3 bloqueadores** do flip entregues (`baf0f4b`: teto 1500→300, FARM_SELLING v1, TREND_QTY persistido).
- **Falta p/ um flip responsável:** **(e)** cap diário −5% + refactor do guard p/ kill-switch quente ← **este é o próximo item**, é só desenhar/implementar com QA/TL. Depois **(c)** P&L-BNB + BNB-fee (acoplados, dono disse "ver depois"), aí **GO do dono** + canary de **um-grupo-só**.
- **Expectativa real do flip: ≈ flat** — o canary valida MECÂNICA (fill/fee/slippage reais nunca exercitados, 0 ordens mainnet), não lucro rápido. O +3 BTC era do testnet.
- 🛑 **Claude NÃO vira o `TRADING_HALT`.** Isso é decisão e ação do dono.

Qual a direção? O caminho natural é atacar o item (e) — desenhar o cap diário com o refactor do guard pra virar kill-switch quente.

## 👤 User *(13:18:00)*

Ultimas mensagens recebidas no telegram.: 

🤖 [AGENTE] Observação: O regime de ADAUSDT mudou para 'trend' (antes provavelmente 'range'). Isso habilita a automação de tendência (compra no golden cross, venda no death cross). Nenhuma cruz detectada atualmente (TREND_CROSS_1h = 'none', TREND_QTY = null). O sistema permanece coerente com a estratégia Farm-and-Funnel; as portas de compra estão abertas conforme regime/fluxo, porém os gatilhos de RSI (farm <35, baseline <25) não estão satisfeitos, então nenhuma ordem de farm ou baseline foi esperada. O kill-switch (tradingHalt=true) está ativo, impedindo novas ordens.
🤖 [AGENTE] Observação: O sistema está com tradingHalt=true (kill‑switch ativado). Nenhuma ordem real está sendo enviada; as automações (farm, trend, baseline, harvester) estão congeladas. O regimegate indica trend para BTCUSDT, LTCUSDT, BNBUSDT e ADAUSDT, com farm e baseline em CAIXA (correto). Não há posições de trend abertas (TREND_CROSS_1h = none, TREND_QTY = null) e o harvester não executa devido ao halt. Tudo coerente com a estratégia Farm‑and‑Funnel.

---

⚡ PRÓXIMO    : (e) cap diário −5% + refactor do guard → kill-switch QUENTE (resolve o HALT-frio junto)

## 🤖 Claude *(13:18:26)*


## 🤖 Claude *(13:18:28)*

Recebido. As duas mensagens do Telegram são **informativas e coerentes** — o agente confirmando que sob `tradingHalt=true` tudo está em CAIXA, regimes em `trend`, sem cruzes, sem ordens. Nada pra corrigir ali; é o comportamento esperado (e o dedup/doutrina anti-ruído segurando o tom certo).

Direção entendida: **atacar o item (e)** — cap diário −5% + refactor do guard pra kill-switch QUENTE. Antes de desenhar, preciso ler o código real do guard (não confiar de memória num path money-critical). Deixa eu mapear.

## 🤖 Claude *(13:18:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrux-tradeux/tradeux && ls && echo \"---BACKEND SRC---\" && find . -path ./node_modules -prune -o -name '*.js' -print 2>/dev/null | grep -iE 'exchange|riskGuard|risk' | grep -v node_modules | head -40",
  "description": "List repo root and find exchange/risk files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> backend
> CLAUDE.md
> docker-compose.supabase.yml
> docker-compose.yml
> docs
> frontend
> LICENSE
> Makefile
> README.md
> scripts
> SECURITY.md
> setup.log
> setup.sh
> tradeux-agent
> tradeux-mcp
> ---BACKEND SRC---
> ./frontend/src/services/ExchangeService.js
> ./backend/src/utils/exchange.js
> ./backend/src/routers/exchangeRouter.js
> ./backend/src/controllers/exchangeController.js
> ```

## 🤖 Claude *(13:18:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn -iE 'TRADING_HALT|tradingHalt|MAX_ORDER_NOTIONAL|assertWithinRisk|riskGuard|DAILY|daily.*cap|cap.*daily|MAX_DAILY' backend/src tradeux-agent/src tradeux-mcp 2>/dev/null | grep -v node_modules | head -60",
  "description": "Grep for guard/halt/daily-cap references"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> backend/src/agenda.js:24:    return /^(@(annually|yearly|monthly|weekly|daily|hourly|reboot))|(@every (\d+(ns|us|µs|ms|s|m|h))+)|((((\d+,)+\d+|(\d+(\/|-)\d+)|\d+|\*) ?){5,7})$/.test(schedule);
> backend/src/beholder.js:288:    // um resultado já-válido (mult>=~1.1 ou símbolo que floored acima de $5) não muda. O teto MAX_ORDER_NOTIONAL
> tradeux-agent/src/agent.js:26:- O ambiente REAL e o estado de trading vêm de tradeux_get_cockpit: env.useTestnet (mainnet vs testnet) e env.tradingHalt (kill-switch). É a FONTE DE VERDADE — confie nela, não no que este prompt assume.
> tradeux-agent/src/agent.js:29:- Se env.tradingHalt=TRUE: o sistema está CONGELADO (kill-switch) — nenhuma ordem real sai; trate tudo como observação, não aja. HALT é estado CONHECIDO do operador — ver DIVERGÊNCIAS ESPERADAS (não reportar a cada ciclo).
> tradeux-agent/src/agent.js:33:- 1× tradeux_get_cockpit por ciclo: confirma o AMBIENTE (env.useTestnet/env.tradingHalt) e traz, por símbolo, a MECÂNICA da distribuição de 1m — mediana |move|, σ, % de moves ≥ break-even, EV/trade NET de fee (costuma ser ≤0), a banda Monte Carlo DRIFTLESS (p50≡preço, NÃO previsão) e o estado dos gates de COMPRA. REPORTE no diário o estado mecânico e a coerência dos gates (EV≤0 a 1m é esperado — ver DIVERGÊNCIAS ESPERADAS).
> tradeux-agent/src/agent.js:41:  (5) HALT inalterado (tradingHalt=TRUE estável): estado conhecido do operador — reporte 1× ou só quando MUDAR.
> backend/src/dailyProfitJob.js:12:const TARGET_PROFIT = parseFloat(process.env.DAILY_PROFIT_TARGET || '500');
> backend/src/dailyProfitJob.js:13:const CHECK_INTERVAL_MS = parseInt(process.env.DAILY_PROFIT_CHECK_MS || '300000', 10);
> backend/src/dailyProfitJob.js:45:async function getDailyProfit() {
> backend/src/dailyProfitJob.js:86:                    await telegram(settings, `🌅 [DAILY_TARGET] Novo dia UTC iniciado. Reativando as grades do Farm de alts para buscar nova meta diária!`);
> backend/src/dailyProfitJob.js:93:        const dailyProfit = await getDailyProfit();
> backend/src/dailyProfitJob.js:94:        logger('system', `Monitoramento de Lucro Diário: $${dailyProfit.toFixed(2)} USDT (Meta: $${TARGET_PROFIT.toFixed(2)} USDT)`);
> backend/src/dailyProfitJob.js:97:        if (dailyProfit >= TARGET_PROFIT) {
> backend/src/dailyProfitJob.js:116:                        await telegram(settings, `🎉 [DAILY_TARGET] Meta diária de $${TARGET_PROFIT.toFixed(2)} USDT alcançada! Lucro atual: $${dailyProfit.toFixed(2)} USDT.\n🚫 Farm de alts PAUSADO até a virada do dia para garantir o ganho.`);
> backend/src/dailyProfitJob.js:122:        logger('system', `Erro no dailyProfitJob: ${err.message}`);
> backend/src/dailyProfitJob.js:131:    logger('system', `Daily Profit target job iniciado. Meta: $${TARGET_PROFIT.toFixed(2)} USDT.`);
> backend/src/utils/exchange.js:11://   TRADING_HALT=true            → kill-switch: bloqueia QUALQUER ordem (parada de emergência) — cobre TUDO.
> backend/src/utils/exchange.js:12://   MAX_ORDER_NOTIONAL_USDT=<n>  → teto de notional por ordem em USDT (0 = desligado). Cobre MARKET por
> backend/src/utils/exchange.js:26:const TRADING_HALT = process.env.TRADING_HALT === 'true';
> backend/src/utils/exchange.js:27:const _maxNotional = parseFloat(process.env.MAX_ORDER_NOTIONAL_USDT || '0');
> backend/src/utils/exchange.js:28:const MAX_ORDER_NOTIONAL_USDT = Number.isFinite(_maxNotional) && _maxNotional > 0 ? _maxNotional : 0;
> backend/src/utils/exchange.js:30:function assertWithinRisk(action, symbol, quantity, price, options) {
> backend/src/utils/exchange.js:31:    if (TRADING_HALT) {
> backend/src/utils/exchange.js:32:        const msg = `[riskGuard] TRADING_HALT ativo — ${action} ${symbol} BLOQUEADA (kill-switch).`;
> backend/src/utils/exchange.js:36:    if (MAX_ORDER_NOTIONAL_USDT > 0 && /USDT$/i.test(symbol || '')) {
> backend/src/utils/exchange.js:44:            else logger('system', `[riskGuard] ${action} ${symbol} MARKET-por-qty sem preço de referência (MINI_TICKER frio) — teto NÃO avaliado (coberto só pelo HALT).`);
> backend/src/utils/exchange.js:46:        if (Number.isFinite(notional) && notional > MAX_ORDER_NOTIONAL_USDT) {
> backend/src/utils/exchange.js:47:            const msg = `[riskGuard] ${action} ${symbol} notional $${notional.toFixed(2)} > teto $${MAX_ORDER_NOTIONAL_USDT.toFixed(2)} — BLOQUEADA.`;
> backend/src/utils/exchange.js:112:        assertWithinRisk('BUY', symbol, quantity, price, options);
> backend/src/utils/exchange.js:121:        assertWithinRisk('SELL', symbol, quantity, price, options);
> backend/src/utils/exchange.js:134:        assertWithinRisk(`OCO-${side}`, symbol, quantity, options.abovePrice || options.belowPrice, options);
> tradeux-agent/src/notifyDedup.js:36:  'tradinghalt', 'halt', 'kill', 'switch', 'congelado', 'congelamento', 'freeze',
> tradeux-agent/src/notifyDedup.js:55:  // família HALT (o spam #1 é "tradingHalt=TRUE" reformulado — unifica todas as variantes em 'halt')
> tradeux-agent/src/notifyDedup.js:56:  tradinghalt: 'halt', congelado: 'halt', congelamento: 'halt', freeze: 'halt',
> backend/src/controllers/analysisController.js:77:    // TRADING_HALT (env). Read-only; não expõe segredo (só os dois booleanos).
> backend/src/controllers/analysisController.js:80:        status.env = { useTestnet: !!(s && s.useTestnet), tradingHalt: process.env.TRADING_HALT === 'true' };
> backend/src/controllers/analysisController.js:82:        status.env = { useTestnet: null, tradingHalt: process.env.TRADING_HALT === 'true' };
> tradeux-mcp/src/index.js:215:  "Cockpit Intelligence (READ-ONLY): snapshot que a brain computa por simbolo a partir de klines 1m REAIS da mainnet — distribuicao de retornos (mediana |move|, sigma, % de moves >= break-even de fee), EV/trade NET de fee (mecanica da distribuicao 1m; costuma ser <=0 = por que scalping de 1m sangra taxa), banda Monte Carlo DRIFTLESS (p50 == preco, NAO previsao) e o snapshot regime/fluxo + estado dos gates de COMPRA por simbolo. Tambem informa o AMBIENTE real (env.useTestnet) e se o trading esta congelado (env.tradingHalt). Use para REPORTAR ao operador o estado MECANICO do mercado e a coerencia dos gates; NAO e sinal de trade nem forecast. ATENCAO: os gates (buyGate/farm/baseline/trend, doctrine=true) sao a DOUTRINA por regime (o que a estrategia FARIA), NAO confirmam que a automacao correspondente esta ATIVA/ligada (ex.: a baseline id2 esta isActive=0) — o gate VIVO mora na condition da automacao no banco. Reporte como doutrina, nao como estado vivo, e o fluxo e fail-closed (stale/ausente => CAIXA). O campo baseline SO se aplica a simbolo flow-gated (BTC); para ALTS vem null (n/a) — o gate de acumulacao da alt e o farm, entao NAO trate baseline=null (nem farm aberto com RSI>35/25) como incoerencia: o gate e a DOUTRINA de regime/fluxo, o RSI e o GATILHO (gate != gatilho). O regime/fluxo do cockpit sao lidos das MESMAS chaves MEMORY['REGIME']/['FLOW'] que os oraculos vivos (tradeux_get_regime/tradeux_get_oracle_state) — NAO uma fonte paralela; o fluxo carrega flow.ageSec (idade em segundos). Por isso NAO trate diferenca cockpit×oraculo-vivo como contradicao: compare pela idade (um imbalance velho mais negativo que o vivo e o MESMO sinal em instantes diferentes) e, no regime, use o gate.regime histeretico.",
> backend/src/server.js:14:const dailyProfitJob = require('./dailyProfitJob');
> backend/src/server.js:71:    // Daily Profit target job: monitora meta diária e controla o estado de ativação do farm de alts.
> backend/src/server.js:72:    logger('system', `Starting the Daily Profit Target Job...`);
> backend/src/server.js:73:    dailyProfitJob.start();
> ```

## 🤖 Claude *(13:18:39)*


## 🤖 Claude *(13:18:40)*

Vou ler o guard inteiro e o `dailyProfitJob` (que já computa P&L diário — pode ser a fonte do cap).

## 🤖 Claude *(13:18:41)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/src/utils/exchange.js",
  "limit": 160
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
> 12	//   MAX_ORDER_NOTIONAL_USDT=<n>  → teto de notional por ordem em USDT (0 = desligado). Cobre MARKET por
> 13	//                                  quote (quoteOrderQty, ex.: funil), LIMIT/OCO (price×qty) e — desde o fix
> 14	//                                  do furo MARKET-por-quantidade — MARKET por QTY-base sem price (venda de
> 15	//                                  TREND_QTY/HARVEST_QTY/MAX_WALLET): deriva o preço do MINI_TICKER p/ estimar
> 16	//                                  o notional. Se o MINI_TICKER estiver frio (sem preço de referência), a
> 17	//                                  ordem PASSA (logada) e fica coberta só pelo HALT — escolha deliberada p/
> 18	//                                  NÃO bloquear venda protetiva (ex.: death cross) por memória fria.
> 19	//                                  Só pares *USDT (notional em USDT); quote ≠ USDT passa.
> 20	//   DIMENSIONAMENTO: o teto deve ficar logo ACIMA do maior pedido LEGÍTIMO (venda de posição/bucket por símbolo,
> 21	//   capada na carteira pelo calcQty) e MUITO ABAIXO de um runaway. ~2× o saldo total da conta é a régua; reajuste
> 22	//   ao aportar. ⚠️ vendas de EXCEDENTE de BTC (BTC_EXCESS, meta +3 BTC) têm notional ALTO → se reativar a 'BTC
> 23	//   Scalp Excess' (id38), tornar o teto symbol-aware (isentar/segregar BTCUSDT SELL): um teto fixo a MARKET
> 24	//   bloquearia a colheita de BTC. Hoje id38 está isActive=0, então o teto fixo é seguro.
> 25	// Inerte por padrão; ajustável por env SEM deploy de código (basta reiniciar). Fail-closed (lança). ===
> 26	const TRADING_HALT = process.env.TRADING_HALT === 'true';
> 27	const _maxNotional = parseFloat(process.env.MAX_ORDER_NOTIONAL_USDT || '0');
> 28	const MAX_ORDER_NOTIONAL_USDT = Number.isFinite(_maxNotional) && _maxNotional > 0 ? _maxNotional : 0;
> 29	
> 30	function assertWithinRisk(action, symbol, quantity, price, options) {
> 31	    if (TRADING_HALT) {
> 32	        const msg = `[riskGuard] TRADING_HALT ativo — ${action} ${symbol} BLOQUEADA (kill-switch).`;
> 33	        logger('system', msg);
> 34	        throw new Error(msg);
> 35	    }
> 36	    if (MAX_ORDER_NOTIONAL_USDT > 0 && /USDT$/i.test(symbol || '')) {
> 37	        const o = options || {};
> 38	        let notional = null;
> 39	        if (o.quoteOrderQty != null) notional = parseFloat(o.quoteOrderQty);            // MARKET por quote (ex.: funil)
> 40	        else if (price != null && quantity != null) notional = parseFloat(price) * parseFloat(quantity); // LIMIT/OCO
> 41	        else if (quantity != null) {                                                    // MARKET por QTY-base sem price (venda TREND_QTY/HARVEST_QTY/MAX_WALLET; ou STOP/TP-MARKET)
> 42	            const ref = (o.stopPrice != null ? parseFloat(o.stopPrice) : refPrice(symbol)); // STOP/TP-MARKET: usa o stopPrice (preço-alvo real); senão deriva o spot do MINI_TICKER
> 43	            if (Number.isFinite(ref) && ref > 0) notional = ref * parseFloat(quantity);
> 44	            else logger('system', `[riskGuard] ${action} ${symbol} MARKET-por-qty sem preço de referência (MINI_TICKER frio) — teto NÃO avaliado (coberto só pelo HALT).`);
> 45	        }
> 46	        if (Number.isFinite(notional) && notional > MAX_ORDER_NOTIONAL_USDT) {
> 47	            const msg = `[riskGuard] ${action} ${symbol} notional $${notional.toFixed(2)} > teto $${MAX_ORDER_NOTIONAL_USDT.toFixed(2)} — BLOQUEADA.`;
> 48	            logger('system', msg);
> 49	            throw new Error(msg);
> 50	        }
> 51	    }
> 52	}
> 53	
> 54	// Preço de referência p/ estimar o notional de uma MARKET-por-quantidade (sem price): MINI_TICKER.close da
> 55	// MEMORY do beholder. require LAZY de propósito — exchange é boundary de baixo nível e beholder é a engine;
> 56	// o require no corpo (não no topo) evita ciclo no load, e em runtime (na hora da ordem) o beholder já está
> 57	// inicializado. Read-only: só lê a memória p/ avaliar o teto de risco, nunca escreve.
> 58	function refPrice(symbol) {
> 59	    try {
> 60	        const beholder = require('../beholder');
> 61	        const mt = beholder.getMemory(symbol, 'MINI_TICKER'); // chave === indexKeys.MINI_TICKER; interval falsy
> 62	        const px = mt && parseFloat(mt.close);
> 63	        return Number.isFinite(px) && px > 0 ? px : null;
> 64	    } catch (_) {
> 65	        return null;
> 66	    }
> 67	}
> 68	
> 69	module.exports = (settings) => {
> 70	
> 71	    if (!settings) throw new Error(`The settings object is required to connect on exchange!`);
> 72	
> 73	    // testnet x mainnet: na 1.x a WebSocket-API (userData) é roteada por Options.test,
> 74	    // NÃO pelas urls. Sem isso o userData tentaria autenticar no ws-api MAINNET com chave
> 75	    // testnet. Derivamos do apiUrl pra manter o BYOK funcionando nos dois ambientes.
> 76	    const isTestnet = /testnet|binance\.vision/i.test(settings.apiUrl || '');
> 77	
> 78	    const binance = new Binance().options({
> 79	        APIKEY: settings.accessKey,
> 80	        APISECRET: settings.secretKey,
> 81	        recvWindow: 60000,
> 82	        test: isTestnet,
> 83	        reconnect: true,
> 84	        urls: {
> 85	            base: settings.apiUrl.endsWith('/') ? settings.apiUrl : settings.apiUrl + '/',
> 86	            stream: settings.streamUrl.endsWith('/') ? settings.streamUrl : settings.streamUrl + '/'
> 87	        },
> 88	        verbose: LOGS
> 89	    });
> 90	
> 91	    // 1.x: websockets.terminate() indexa as subscriptions pela URL COMPLETA do socket, não
> 92	    // pelo nome curto do endpoint. Guardamos a URL retornada por chart()/prevDay() por stream
> 93	    // p/ conseguir fechá-lo depois (senão terminate vira no-op e o socket vaza/reconecta).
> 94	    const chartStreams = {};
> 95	    const tickerStreams = {};
> 96	
> 97	    function exchangeInfo() {
> 98	        return binance.exchangeInfo();
> 99	    }
> 100	
> 101	    async function balance() {
> 102	        await binance.useServerTime();
> 103	        return binance.balance();
> 104	    }
> 105	
> 106	    // 1.x: buy()/sell() fixam type='LIMIT' posicional e o guard interno de stopPrice dispara
> 107	    // ANTES de params sobrescrever o type -> ordens STOP via flags quebrariam. Por isso chamamos
> 108	    // binance.order(type, side, ...) direto (e marketBuy/marketSell p/ MARKET, que tratam
> 109	    // quoteOrderQty). Cobre MARKET/LIMIT/STOP_LOSS_LIMIT/TAKE_PROFIT_LIMIT/LIMIT_MAKER.
> 110	    function buy(symbol, quantity, price, options) {
> 111	        options = options || {};
> 112	        assertWithinRisk('BUY', symbol, quantity, price, options);
> 113	        const type = options.type || 'MARKET';
> 114	        if (type === 'MARKET')
> 115	            return binance.marketBuy(symbol, quantity, options);
> 116	        return binance.order(type, 'BUY', symbol, quantity, price, options);
> 117	    }
> 118	
> 119	    function sell(symbol, quantity, price, options) {
> 120	        options = options || {};
> 121	        assertWithinRisk('SELL', symbol, quantity, price, options);
> 122	        const type = options.type || 'MARKET';
> 123	        if (type === 'MARKET')
> 124	            return binance.marketSell(symbol, quantity, options);
> 125	        return binance.order(type, 'SELL', symbol, quantity, price, options);
> 126	    }
> 127	
> 128	    // OCO (destravado pelo bump p/ 1.x). ocoOrder usa o endpoint novo POST /api/v3/orderList/oco.
> 129	    // `options` segue o schema novo, p.ex. p/ um SELL protetivo após o buy:
> 130	    //   { aboveType:'LIMIT_MAKER', abovePrice, belowType:'STOP_LOSS_LIMIT',
> 131	    //     belowPrice, belowStopPrice, belowTimeInForce:'GTC' }
> 132	    function oco(side, symbol, quantity, options) {
> 133	        options = options || {};
> 134	        assertWithinRisk(`OCO-${side}`, symbol, quantity, options.abovePrice || options.belowPrice, options);
> 135	        return binance.ocoOrder(side, symbol, quantity, options);
> 136	    }
> 137	
> 138	    function cancel(symbol, orderId) {
> 139	        return binance.cancel(symbol, orderId);
> 140	    }
> 141	
> 142	    // Cancela uma OCO inteira (as 2 pernas) via DELETE /api/v3/orderList.
> 143	    function cancelOrderList(symbol, orderListId) {
> 144	        return binance.privateSpotRequest('v3/orderList', { symbol, orderListId }, 'DELETE');
> 145	    }
> 146	
> 147	    function orderStatus(symbol, orderId) {
> 148	        return binance.orderStatus(symbol, orderId);
> 149	    }
> 150	
> 151	    async function orderTrade(symbol, orderId) {
> 152	        const trades = await binance.trades(symbol);
> 153	        return trades.find(t => t.orderId === orderId);
> 154	    }
> 155	
> 156	    function withdraw(coin, amount, address, network, addressTag) {
> 157	        try {
> 158	            const data = { coin, amount, address };
> 159	            if (addressTag) data.addressTag = addressTag;
> 160	            if (network) data.network = network;
> ```

## 🤖 Claude *(13:18:41)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrux-tradeux/tradeux/backend/src/dailyProfitJob.js"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	'use strict';
> 2	
> 3	const fs = require('fs');
> 4	const path = require('path');
> 5	const ordersRepository = require('./repositories/ordersRepository');
> 6	const automationsRepository = require('./repositories/automationsRepository');
> 7	const settingsRepository = require('./repositories/settingsRepository');
> 8	const beholder = require('./beholder');
> 9	const logger = require('./utils/logger');
> 10	const telegram = require('./utils/telegram');
> 11	
> 12	const TARGET_PROFIT = parseFloat(process.env.DAILY_PROFIT_TARGET || '500');
> 13	const CHECK_INTERVAL_MS = parseInt(process.env.DAILY_PROFIT_CHECK_MS || '300000', 10);
> 14	const PAUSED_FILE = path.resolve(__dirname, '..', 'logs', 'paused_automations.json');
> 15	
> 16	let timer = null;
> 17	let lastCheckDay = new Date().getUTCDate();
> 18	
> 19	// Carrega os IDs das automações pausadas anteriormente pela meta diária
> 20	function getPausedIds() {
> 21	    try {
> 22	        if (fs.existsSync(PAUSED_FILE)) {
> 23	            const data = fs.readFileSync(PAUSED_FILE, 'utf8');
> 24	            return JSON.parse(data) || [];
> 25	        }
> 26	    } catch (e) {
> 27	        logger('system', `Falha ao ler ${PAUSED_FILE}: ${e.message}`);
> 28	    }
> 29	    return [];
> 30	}
> 31	
> 32	// Salva os IDs das automações pausadas
> 33	function savePausedIds(ids) {
> 34	    try {
> 35	        const dir = path.dirname(PAUSED_FILE);
> 36	        if (!fs.existsSync(dir)) {
> 37	            fs.mkdirSync(dir, { recursive: true });
> 38	        }
> 39	        fs.writeFileSync(PAUSED_FILE, JSON.stringify(ids), 'utf8');
> 40	    } catch (e) {
> 41	        logger('system', `Falha ao salvar ${PAUSED_FILE}: ${e.message}`);
> 42	    }
> 43	}
> 44	
> 45	async function getDailyProfit() {
> 46	    const startOfDay = new Date();
> 47	    startOfDay.setUTCHours(0, 0, 0, 0);
> 48	    const startMs = startOfDay.getTime();
> 49	
> 50	    const endOfDay = new Date();
> 51	    endOfDay.setUTCHours(23, 59, 59, 999);
> 52	    const endMs = endOfDay.getTime();
> 53	
> 54	    const orders = await ordersRepository.getReportOrders('USDT', startMs, endMs);
> 55	    if (!orders || !orders.length) return 0;
> 56	
> 57	    const buyVolume = orders.filter(o => o.side === 'BUY').reduce((acc, o) => acc + parseFloat(o.net), 0);
> 58	    const sellVolume = orders.filter(o => o.side === 'SELL').reduce((acc, o) => acc + parseFloat(o.net), 0);
> 59	
> 60	    return sellVolume - buyVolume;
> 61	}
> 62	
> 63	async function checkProfitAndControl() {
> 64	    try {
> 65	        const today = new Date().getUTCDate();
> 66	        const ds = await settingsRepository.getDefaultSettings();
> 67	        if (!ds) return;
> 68	        const settings = await settingsRepository.getSettingsDecrypted(ds.id);
> 69	
> 70	        // 1. Virada do Dia: Reativação se houver pausados
> 71	        if (today !== lastCheckDay) {
> 72	            logger('system', `Mudança de dia detectada (Dia ${lastCheckDay} -> ${today}). Iniciando reativação...`);
> 73	            const pausedIds = getPausedIds();
> 74	            if (pausedIds.length > 0) {
> 75	                logger('system', `Reativando ${pausedIds.length} automações pausadas pela meta ontem...`);
> 76	                for (const id of pausedIds) {
> 77	                    const auto = await automationsRepository.getAutomation(id);
> 78	                    if (auto) {
> 79	                        auto.isActive = true;
> 80	                        await auto.save();
> 81	                        beholder.updateBrain(auto.get({ plain: true }));
> 82	                    }
> 83	                }
> 84	                savePausedIds([]);
> 85	                try {
> 86	                    await telegram(settings, `🌅 [DAILY_TARGET] Novo dia UTC iniciado. Reativando as grades do Farm de alts para buscar nova meta diária!`);
> 87	                } catch (e) {}
> 88	            }
> 89	            lastCheckDay = today;
> 90	        }
> 91	
> 92	        // 2. Calcula Lucro Diário
> 93	        const dailyProfit = await getDailyProfit();
> 94	        logger('system', `Monitoramento de Lucro Diário: $${dailyProfit.toFixed(2)} USDT (Meta: $${TARGET_PROFIT.toFixed(2)} USDT)`);
> 95	
> 96	        // 3. Trava de Lucro Diário atingido
> 97	        if (dailyProfit >= TARGET_PROFIT) {
> 98	            const pausedIds = getPausedIds();
> 99	            if (pausedIds.length === 0) {
> 100	                // Seleciona automações de altcoins ativas para pausar (Farm de alts)
> 101	                const activeAutos = await automationsRepository.getActiveAutomations();
> 102	                const altsToPause = activeAutos.filter(a => a.symbol !== 'BTCUSDT' && a.name.startsWith('Farm'));
> 103	
> 104	                if (altsToPause.length > 0) {
> 105	                    const idsToSave = [];
> 106	                    logger('system', `META DIÁRIA ATINGIDA! Pausando ${altsToPause.length} automações de alts...`);
> 107	                    for (const auto of altsToPause) {
> 108	                        auto.isActive = false;
> 109	                        await auto.save();
> 110	                        beholder.deleteBrain(auto.get({ plain: true }));
> 111	                        idsToSave.push(auto.id);
> 112	                    }
> 113	                    savePausedIds(idsToSave);
> 114	
> 115	                    try {
> 116	                        await telegram(settings, `🎉 [DAILY_TARGET] Meta diária de $${TARGET_PROFIT.toFixed(2)} USDT alcançada! Lucro atual: $${dailyProfit.toFixed(2)} USDT.\n🚫 Farm de alts PAUSADO até a virada do dia para garantir o ganho.`);
> 117	                    } catch (e) {}
> 118	                }
> 119	            }
> 120	        }
> 121	    } catch (err) {
> 122	        logger('system', `Erro no dailyProfitJob: ${err.message}`);
> 123	    }
> 124	}
> 125	
> 126	function start() {
> 127	    if (timer) return;
> 128	    checkProfitAndControl();
> 129	    timer = setInterval(checkProfitAndControl, CHECK_INTERVAL_MS);
> 130	    if (timer.unref) timer.unref();
> 131	    logger('system', `Daily Profit target job iniciado. Meta: $${TARGET_PROFIT.toFixed(2)} USDT.`);
> 132	}
> 133	
> 134	function stop() {
> 135	    if (timer) {
> 136	        clearInterval(timer);
> 137	        timer = null;
> 138	    }
> 139	}
> 140	
> 141	module.exports = { start, stop };
> 142	
> ```

## 🤖 Claude *(13:19:29)*


## 🤖 Claude *(13:19:32)*

Já tenho o quadro do guard e do P&L diário. Antes de desenhar, preciso checar duas coisas que mudam o design: (1) se existe uma fonte de **equity total** (USDT + valor das posições) ou só o cash-flow do `getDailyProfit`, e (2) onde a UI/agent lê o `tradingHalt` (pra fazer o switch quente coerente ponta-a-ponta).

## 🤖 Claude *(13:19:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== getReportOrders / net ===\" && grep -rn \"getReportOrders\\|\\.net\\b\" backend/src/repositories/ordersRepository.js | head; echo \"=== equity / wallet value / USD valuation ===\" && grep -rn -iE \"equity|walletValue|totalUsdt|getWallet|estimateValue|getBalance|valuation|netWorth\" backend/src tradeux-mcp/src | grep -v node_modules | head -30",
  "description": "Find PnL source and any equity/wallet valuation"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === getReportOrders / net ===
> backend/src/repositories/ordersRepository.js:52:            net: parseFloat(r.net),
> backend/src/repositories/ordersRepository.js:54:            avg: parseFloat(r.net) / parseFloat(r.qty)
> backend/src/repositories/ordersRepository.js:132:    if (newOrder.net !== null && newOrder.net !== undefined
> backend/src/repositories/ordersRepository.js:133:        && newOrder.net !== currentOrder.net)
> backend/src/repositories/ordersRepository.js:134:        currentOrder.net = newOrder.net;
> backend/src/repositories/ordersRepository.js:200:async function getReportOrders(quoteAsset, startDate, endDate, isTestnet = null) {
> backend/src/repositories/ordersRepository.js:239:        if (commAsset && symbol.endsWith(commAsset)) out.net = cummQuote - commission; // comissão no quote
> backend/src/repositories/ordersRepository.js:377:    getReportOrders,
> === equity / wallet value / USD valuation ===
> backend/src/funnelJob.js:250:        const equity = snap.price ? (snap.usdtFree + snap.btcReserve * snap.price) : null;
> backend/src/funnelJob.js:251:        logger('funnel', `[fase4-observe] t+${tMin}min · USDT=$${snap.usdtFree.toFixed(2)} · reserva ${BASE_ASSET}=${snap.btcReserve.toFixed(6)}${snap.price ? ` @ $${snap.price.toFixed(2)}` : ''}${equity != null ? ` · equity~$${equity.toFixed(2)}` : ''} · lucro_desde_saída=$${profit.toFixed(2)} · escoaria=+${drainBtc.toFixed(6)} ${BASE_ASSET}`);
> backend/src/routers/exchangeRouter.js:7:router.get('/balance/:fiat', exchangeController.getBalance);
> backend/src/controllers/exchangeController.js:32:async function getBalance(req, res, next) {
> backend/src/controllers/exchangeController.js:133:    getBalance,
> ```

## 🤖 Claude *(13:19:37)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== where tradingHalt is read (UI/agent/cockpit) ===\" && grep -rn -iE \"tradingHalt|TRADING_HALT\" backend/src tradeux-mcp/src frontend/src | grep -v node_modules | head -30; echo; echo \"=== analysisController status/cockpit ===\" && grep -rn -iE \"cockpit|getStatus|status\\.env\" backend/src/controllers/analysisController.js | head",
  "description": "Find all tradingHalt read sites end-to-end"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === where tradingHalt is read (UI/agent/cockpit) ===
> backend/src/controllers/analysisController.js:77:    // TRADING_HALT (env). Read-only; não expõe segredo (só os dois booleanos).
> backend/src/controllers/analysisController.js:80:        status.env = { useTestnet: !!(s && s.useTestnet), tradingHalt: process.env.TRADING_HALT === 'true' };
> backend/src/controllers/analysisController.js:82:        status.env = { useTestnet: null, tradingHalt: process.env.TRADING_HALT === 'true' };
> tradeux-mcp/src/index.js:215:  "Cockpit Intelligence (READ-ONLY): snapshot que a brain computa por simbolo a partir de klines 1m REAIS da mainnet — distribuicao de retornos (mediana |move|, sigma, % de moves >= break-even de fee), EV/trade NET de fee (mecanica da distribuicao 1m; costuma ser <=0 = por que scalping de 1m sangra taxa), banda Monte Carlo DRIFTLESS (p50 == preco, NAO previsao) e o snapshot regime/fluxo + estado dos gates de COMPRA por simbolo. Tambem informa o AMBIENTE real (env.useTestnet) e se o trading esta congelado (env.tradingHalt). Use para REPORTAR ao operador o estado MECANICO do mercado e a coerencia dos gates; NAO e sinal de trade nem forecast. ATENCAO: os gates (buyGate/farm/baseline/trend, doctrine=true) sao a DOUTRINA por regime (o que a estrategia FARIA), NAO confirmam que a automacao correspondente esta ATIVA/ligada (ex.: a baseline id2 esta isActive=0) — o gate VIVO mora na condition da automacao no banco. Reporte como doutrina, nao como estado vivo, e o fluxo e fail-closed (stale/ausente => CAIXA). O campo baseline SO se aplica a simbolo flow-gated (BTC); para ALTS vem null (n/a) — o gate de acumulacao da alt e o farm, entao NAO trate baseline=null (nem farm aberto com RSI>35/25) como incoerencia: o gate e a DOUTRINA de regime/fluxo, o RSI e o GATILHO (gate != gatilho). O regime/fluxo do cockpit sao lidos das MESMAS chaves MEMORY['REGIME']/['FLOW'] que os oraculos vivos (tradeux_get_regime/tradeux_get_oracle_state) — NAO uma fonte paralela; o fluxo carrega flow.ageSec (idade em segundos). Por isso NAO trate diferenca cockpit×oraculo-vivo como contradicao: compare pela idade (um imbalance velho mais negativo que o vivo e o MESMO sinal em instantes diferentes) e, no regime, use o gate.regime histeretico.",
> backend/src/utils/exchange.js:11://   TRADING_HALT=true            → kill-switch: bloqueia QUALQUER ordem (parada de emergência) — cobre TUDO.
> backend/src/utils/exchange.js:26:const TRADING_HALT = process.env.TRADING_HALT === 'true';
> backend/src/utils/exchange.js:31:    if (TRADING_HALT) {
> backend/src/utils/exchange.js:32:        const msg = `[riskGuard] TRADING_HALT ativo — ${action} ${symbol} BLOQUEADA (kill-switch).`;
> frontend/src/private/Cockpit/Cockpit.js:14: * da Binance, WS de preço). NÃO emite ordem, NÃO toca o TRADING_HALT.
> frontend/src/private/Cockpit/Cockpit.js:235:              {env && env.tradingHalt && <span className="cx-pill halt"><span className="cx-dot" />halt</span>}
> frontend/src/private/Cockpit/Cockpit.js:439:                  ? <div className="cx-empty">nenhuma posição/automação no período — feed ao vivo liga ao descongelar (<code>TRADING_HALT=false</code>)</div>
> frontend/src/services/IntelligenceService.js:44:// tradingHalt). Single source of truth do painel /cockpit — alimenta as métricas vindas do brain.
> 
> === analysisController status/cockpit ===
> backend/src/controllers/analysisController.js:5:const cockpitJob = require('../cockpitJob');
> backend/src/controllers/analysisController.js:25:        // da UI ("Market Regime" = instantâneo). As automações e o cockpit gateiam pelo regime HISTERÉTICO
> backend/src/controllers/analysisController.js:27:        // histerese evita que o agente compare o instantâneo com o cockpit (=gate) e chame de "contradição":
> backend/src/controllers/analysisController.js:48:    res.json(regimeJob.getStatus());
> backend/src/controllers/analysisController.js:68:    res.json(flowJob.getStatus());
> backend/src/controllers/analysisController.js:71:// GET /analysis/cockpit — snapshot agregado do Cockpit (por símbolo: distribuição de retornos 1m, EV
> backend/src/controllers/analysisController.js:73:// o painel /cockpit (single source of truth = brain). Não expõe segredos (só estado de mercado).
> backend/src/controllers/analysisController.js:74:async function getCockpitStatus(req, res) {
> backend/src/controllers/analysisController.js:75:    const status = cockpitJob.getStatus();
> backend/src/controllers/analysisController.js:80:        status.env = { useTestnet: !!(s && s.useTestnet), tradingHalt: process.env.TRADING_HALT === 'true' };
> ```

## 🤖 Claude *(13:20:18)*


## 🤖 Claude *(13:20:22)*

O quadro está claro. Tenho os três pontos onde `tradingHalt` é lido (guard em `exchange.js:26/31`, `analysisController:80` que alimenta UI+agente, e o frontend), a fonte de P&L diário (`getDailyProfit` = cash-flow sellNet−buyNet) e que já existe padrão de **equity** (`funnelJob.js:250`: `usdtFree + btcReserve*price`).

Há duas decisões de **política de risco** que mudam o desenho e são suas (não dá pra derivar do código). Vou entrar em plan mode e alinhar elas antes de escrever qualquer linha no money-path.

## 🤖 Claude *(13:20:22)*


🛠️ **Tool Call**: `ToolSearch`
```json
{
  "query": "select:EnterPlanMode,ExitPlanMode",
  "max_results": 5
}
```

> **Tool Result (ToolSearch)** - ✅ Success
>
> ```
> [{'type': 'tool_reference', 'tool_name': 'EnterPlanMode'}, {'type': 'tool_reference', 'tool_name': 'ExitPlanMode'}]
> ```

## 🤖 Claude *(13:20:28)*


🛠️ **Tool Call**: `EnterPlanMode`
```json
{}
```

> **Tool Result (EnterPlanMode)** - ✅ Success
>
> ```
> Entered plan mode. You should now focus on exploring the codebase and designing an implementation approach.
> 
> In plan mode, you should:
> 1. Thoroughly explore the codebase to understand existing patterns
> 2. Identify similar features and architectural approaches
> 3. Consider multiple approaches and their trade-offs
> 4. Use AskUserQuestion if you need to clarify the approach
> 5. Design a concrete implementation strategy
> 6. When ready, use ExitPlanMode to present your plan for approval
> 
> Remember: DO NOT write or edit any files yet. This is a read-only exploration and planning phase.
> ```

## 🤖 Claude *(13:20:49)*


## 🤖 Claude *(13:20:52)*

Já explorei o guard, os pontos de leitura do `tradingHalt`, a fonte de P&L diário e o padrão de equity. Vou disparar **um Explore focado** pra fechar os detalhes que faltam pro plano (cômputo de equity total, rollover/persistência do job diário, lifecycle do `net`, e onde plugar um monitor novo no boot) — em paralelo eu já vou destrinchar as decisões de política pra você.

## 🤖 Claude *(13:21:14)*


🛠️ **Tool Call**: `Agent`
```json
{
  "description": "Map daily-cap integration points",
  "subagent_type": "Explore",
  "prompt": "Repo: /home/gcrux-tradeux/tradeux (Node/Express trading bot \"TradeUX\"). I'm designing a **daily loss cap (\u22125%)** plus a **hot kill-switch refactor** of the risk guard. I need precise file:line facts to write an implementation plan. Do NOT edit anything \u2014 read-only. Be thorough across backend/src.\n\nAnswer these concretely with file:line references and short code excerpts:\n\n1. **Total account equity computation.** I want to compute total account equity in USDT (USDT free + value of all coin holdings at current price) and also just USDT balance.\n   - Read `backend/src/controllers/exchangeController.js` getBalance and `backend/src/repositories`/exchange util: what shape does the balance object have? Does it return ALL assets with free/locked, or just one fiat?\n   - Read `backend/src/funnelJob.js` around line 240-260: how does it build its equity snapshot (usdtFree, btcReserve, price)? Where does `price` come from (beholder MEMORY MINI_TICKER)?\n   - Is there any existing helper that values the whole wallet in USDT (sum over assets \u00d7 price)? Look in beholder.js, exchangeController, funnelJob, cockpitJob. If not, what's the cleanest existing primitive to build it from?\n\n2. **Daily PnL / realized vs cash-flow.** \n   - Read `backend/src/dailyProfitJob.js` fully and `backend/src/repositories/ordersRepository.js` getReportOrders (line ~200-250): what exactly is `net` per order, how is the UTC day window computed, and is sellNet\u2212buyNet a true realized PnL or just cash flow (i.e. does buying without selling show as a loss)?\n   - Does any code compute realized PnL accounting for cost basis / open positions? (grep for costBasis, avgPrice, realized, pnl, getFarmPosition, getTrendPosition)\n\n3. **Day rollover & restart persistence.**\n   - In dailyProfitJob, how is the UTC day-rollover detected (`lastCheckDay`) and what persists across a container restart (the paused_automations.json file)? What would happen to a daily-cap flag on restart mid-day?\n\n4. **Where to wire a new monitor job + getStatus pattern.**\n   - Read `backend/src/server.js` boot sequence: how are jobs like dailyProfitJob, regimeJob, flowJob, funnelJob, cockpitJob started? Show the start() calls and order.\n   - How do these jobs expose state to controllers (e.g. regimeJob.getStatus, flowJob.getStatus, cockpitJob.getStatus used in analysisController.js)? I want the same pattern for a riskState/dailyCap getStatus.\n\n5. **tradingHalt read sites (for hot-switch coherence).**\n   - Confirm every place that reads TRADING_HALT / process.env.TRADING_HALT / exposes tradingHalt: `backend/src/utils/exchange.js` (the guard), `backend/src/controllers/analysisController.js` (status.env), and any others in backend/src, tradeux-mcp/src, frontend/src. I need to make a runtime halt flag coherent across the guard (enforcement) and the cockpit/agent (reporting).\n   - Is exchange.js's assertWithinRisk the SINGLE chokepoint for all real orders (buy/sell/oco)? Confirm no other code path places orders bypassing buy()/sell()/oco().\n\n6. **Settings model & runtime control surfaces.**\n   - Is there a `settings` table/model with arbitrary fields, or a MEMORY mechanism in beholder, that could hold a persisted runtime flag (so a manual hot-halt survives restart)? Look at backend/src/models/settings.js and beholder.js getMemory/updateMemory/setMemory.\n   - Are there existing API endpoints + MCP tools for control actions (e.g. start_automation/stop_automation) I could mirror for a \"set halt\" operator surface? Check backend/src/routers + tradeux-mcp/src/index.js.\n\nReturn a structured findings list with exact file:line refs and minimal excerpts. Flag any gotcha that would make a daily-loss cap false-trip (especially the cash-flow vs realized-PnL issue) or make the hot switch incoherent."
}
```

> **Tool Result (Agent)** - ✅ Success
>
> ```
> [{'type': 'text', 'text': 'Perfect! Now I have all the information I need. Let me compile a comprehensive findings document:\n\n---\n\n## COMPREHENSIVE FINDINGS: TRADEUX DAILY LOSS CAP + HOT KILL-SWITCH REFACTOR\n\n### 1. TOTAL ACCOUNT EQUITY COMPUTATION\n\n**Question:** Shape of balance object, USDT free + all holdings in USDT, existing helpers?\n\n#### 1.1 Balance Object Structure\n**File:** `backend/src/controllers/exchangeController.js:10-30`\n\n**How it works:**\n- `exchange.balance()` returns an object keyed by coin symbol (e.g. `info[\'USDT\']`, `info[\'BTC\']`)\n- Each coin has structure: `{ available, onOrder }` (both floats)\n- Per-coin fiat conversion: line 19-24 calls `beholder.tryFiatConversion(coin, available, fiat)`\n- **NOT a single-asset return** — returns ALL assets with free/locked\n\n**Relevant excerpt:**\n```javascript\n// Line 12-26: balance() returns info keyed by coin\nconst coins = Object.entries(info).map(p => p[0]);\nlet total = 0;\nawait Promise.all(coins.map(async (coin) => {\n    let available = parseFloat(info[coin].available);\n    beholder.updateMemory(coin, `WALLET`, null, available);\n    if (available > 0) available = beholder.tryFiatConversion(coin, available, fiat);\n    let onOrder = parseFloat(info[coin].onOrder);\n    if (onOrder > 0) onOrder = beholder.tryFiatConversion(coin, onOrder, fiat);\n    info[coin].fiatEstimate = available + onOrder;\n    total += available + onOrder;\n}))\n```\n\n#### 1.2 Equity Snapshot in funnelJob\n**File:** `backend/src/funnelJob.js:85-96` (readBalances), **240-250** (captureFase4)\n\n**How it computes:**\n- Line 92: `usdtFree = parseFloat(bal[QUOTE].available)` (USDT free only, not on-order)\n- Line 93: `btcReserve = parseFloat((bal[BASE_ASSET] || {}).available)` (BTC free)\n- Line 94: `price = btcPrice()` — **pulls BTC price from MEMORY**\n\n**Price source (line 73-80):**\n```javascript\nfunction btcPrice() {\n    try {\n        const mt = beholder.getMemory(BTC, \'MINI_TICKER\');  // BTC:MINI_TICKER from MEMORY\n        const p = mt && (mt.close ?? mt.current ?? mt.c ?? mt.lastPrice);\n        const n = parseFloat(p);\n        return Number.isFinite(n) && n > 0 ? n : null;\n    } catch (e) { return null; }\n}\n```\n\n**Equity calculation (line 250):**\n```javascript\nconst equity = snap.price ? (snap.usdtFree + snap.btcReserve * snap.price) : null;\n```\n\n**GOTCHA:** The funnelJob reads `usdtFree` (available only), not including on-order holdings. For daily-cap purposes, this is **intentional** (working capital, not locked). But a true "account value" for a −5% cap should include both.\n\n#### 1.3 Existing Equity Helper?\n- **No dedicated helper exists** to compute total account equity (fiat free + all coin holdings × current price).\n- **Nearest patterns:**\n  - `exchangeController.loadBalance()` (line 7-30): computes per-coin fiat estimates, sums to `total` but does **NOT expose it in the response** (only logs as `fiatEstimate: "~USDT 123.45"` string).\n  - `funnelJob.readBalances()`: returns `{ usdtFree, btcReserve, price }` + computes equity for logging only.\n  - `beholder.tryFiatConversion()`: converts one coin to fiat via order history (call required).\n\n**Cleanest primitive to build from:**\n1. Call `exchange.balance()` → get all assets with free/onOrder.\n2. For each coin > 0, price = `beholder.getMemory(symbol, \'MINI_TICKER\').close` or fallback to last-order avg price.\n3. Sum: `totalEquity = usdtFree + sum(otherCoin.available × price)`.\n\n**Recommendation:** Create a helper in `utils/` or `beholder.js`:\n```javascript\nasync function getAccountEquity(fiat=\'USDT\') {\n  const bal = await exchange.balance();\n  const usdtFree = parseFloat(bal[fiat]?.available || 0);\n  let equity = usdtFree;\n  for (const [coin, balance] of Object.entries(bal)) {\n    if (coin === fiat) continue;\n    const available = parseFloat(balance.available || 0);\n    if (available <= 0) continue;\n    const price = beholder.getMemory(`${coin}${fiat}`, \'MINI_TICKER\')?.close \n                  || beholder.getMemory(coin, \'MINI_TICKER\')?.close;\n    if (price) equity += available * price;\n  }\n  return { usdtFree, equity };\n}\n```\n\n---\n\n### 2. DAILY PnL / REALIZED VS CASH-FLOW\n\n**Question:** What is `net` per order, realized PnL vs cash flow, day window computation?\n\n#### 2.1 Daily Profit Calculation\n**File:** `backend/src/dailyProfitJob.js:45-61`\n\n**How it computes (line 45-61):**\n```javascript\nasync function getDailyProfit() {\n    const startOfDay = new Date();\n    startOfDay.setUTCHours(0, 0, 0, 0);     // UTC midnight\n    const startMs = startOfDay.getTime();\n    \n    const endOfDay = new Date();\n    endOfDay.setUTCHours(23, 59, 59, 999);  // UTC 23:59:59.999\n    const endMs = endOfDay.getTime();\n    \n    const orders = await ordersRepository.getReportOrders(\'USDT\', startMs, endMs);\n    if (!orders || !orders.length) return 0;\n    \n    const buyVolume = orders.filter(o => o.side === \'BUY\').reduce((acc, o) => acc + parseFloat(o.net), 0);\n    const sellVolume = orders.filter(o => o.side === \'SELL\').reduce((acc, o) => acc + parseFloat(o.net), 0);\n    \n    return sellVolume - buyVolume;  // CASH FLOW, NOT REALIZED PnL\n}\n```\n\n#### 2.2 What is `net`?\n**File:** `backend/src/repositories/ordersRepository.js:227-242` (calcFillFinancials)\n\n**Definition (line 227-241):**\n```javascript\nfunction calcFillFinancials(result, symbol) {\n    if (!result) return {};\n    const executedQty = parseFloat(result.executedQty);\n    const cummQuote = parseFloat(result.cummulativeQuoteQty);\n    if (!executedQty || !cummQuote || isNaN(executedQty) || isNaN(cummQuote)) return {};\n    \n    const out = { avgPrice: cummQuote / executedQty, net: cummQuote };\n    if (Array.isArray(result.fills) && result.fills.length) {\n        const commission = result.fills.reduce((a, f) => a + parseFloat(f.commission || 0), 0);\n        out.commission = `${commission}`;\n        out.isMaker = result.fills.every(f => f.isMaker === true);\n        const commAsset = result.fills[0].commissionAsset;\n        if (commAsset && symbol.endsWith(commAsset)) out.net = cummQuote - commission; // commission in quote\n    }\n    return out;\n}\n```\n\n**Key points:**\n- **BUY:** `net = cumulativeQuoteQty` (USDT spent), minus commission if paid in USDT.\n- **SELL:** `net = cumulativeQuoteQty` (USDT received), minus commission if paid in USDT.\n- **sellVolume − buyVolume = cash flow, NOT realized PnL.**\n\n#### 2.3 CRITICAL GOTCHA: CASH FLOW VS. REALIZED PnL\n\n**This is FALSE for detecting loss:**\n- Buying 1 BTC without selling = `buyVolume = +5000 USDT`, `sellVolume = 0`, daily profit = −5000 USDT (looks like a loss).\n- **This is actually a capital allocation, not a loss.** If the BTC is worth $5100 now, equity is +$100, not −$5000.\n\n**The problem with `dailyProfitJob.getDailyProfit()` logic (line 57-60):**\n```javascript\nconst buyVolume = orders.filter(o => o.side === \'BUY\').reduce(...);  // total spent on buys\nconst sellVolume = orders.filter(o => o.side === \'SELL\').reduce(...);  // total received from sells\nreturn sellVolume - buyVolume;  // only true PnL if ALL buys are sold same day\n```\n\n**Why it works in practice here:** The daily-profit job **pauses the farm at +$500 profit**, meaning it only pauses after real sells exceed buys — so the cash-flow approximation holds for the use case (farm scalping, high turnover). But **for a daily-loss cap (−5% of account)**, you CANNOT use this metric.\n\n#### 2.4 Realized PnL with Cost Basis\n**File:** `backend/src/repositories/ordersRepository.js:244-300` (getFarmPosition + getTrendPosition)\n\n**These DO compute cost basis:**\n```javascript\n// Line 289-298 (getFarmPosition)\nlet totalQty = 0;\nlet totalCost = 0;\nfor (const buy of buys) {\n    const qty = parseFloat(buy.quantity);\n    const avgPrice = parseFloat(buy.avgPrice);\n    if (Number.isFinite(qty) && qty > 0 && Number.isFinite(avgPrice) && avgPrice > 0) {\n        totalQty += qty;\n        totalCost += qty * avgPrice;\n    }\n}\nconst cost = totalQty > 0 ? (totalCost / totalQty) : 0;\nreturn { qty: totalQty, cost };\n```\n\n**To compute realized PnL:**\n```javascript\n// For each SELL order in the day, match against cost basis of buys, compute gain/loss\n// This is NOT currently implemented — there\'s no getRealized() method\n```\n\n#### 2.5 Recommendation for Daily-Loss Cap\n**Do NOT use `dailyProfitJob.getDailyProfit()`** (cash flow only). Instead:\n1. **Snapshot account equity at UTC midnight** (or when cap is armed).\n2. **Compare current equity to snapshot.**\n3. **If current < snapshot × 0.95, trigger halt.**\n\nThis is **equity-based** and correct (accounts for open positions with unrealized gains/losses).\n\n---\n\n### 3. DAY ROLLOVER & RESTART PERSISTENCE\n\n**Question:** How UTC day-rollover detected, what persists, daily-cap flag on restart mid-day?\n\n#### 3.1 Day-Rollover Detection\n**File:** `backend/src/dailyProfitJob.js:17, 63-90`\n\n**Detection (line 17, 65, 71):**\n```javascript\nlet lastCheckDay = new Date().getUTCDate();  // line 17: initialized at module load\n\n// line 65-71: in checkProfitAndControl()\nconst today = new Date().getUTCDate();\nif (today !== lastCheckDay) {\n    logger(\'system\', `Mudança de dia detectada (Dia ${lastCheckDay} -> ${today}). Iniciando reativação...`);\n    // reactivate paused automations\n    lastCheckDay = today;\n}\n```\n\n**PROBLEM:** `getUTCDate()` is just the day-of-month (1–31), **not globally unique**. At UTC midnight 2026-06-30 → 2026-07-01, `getUTCDate()` flips from 30 to 1. But if the server is running in a timezone-aware context and restarted mid-day, the comparison still works (e.g. restarts on June 15 midday, `getUTCDate()=15`, checks against `lastCheckDay=15` → no rollover fired).\n\n**True gotcha:** On **month boundary** (June 30 → July 1), UTC date resets. This is handled correctly by the module-level `lastCheckDay`.\n\n#### 3.2 What Persists Across Restart\n**File:** `backend/src/dailyProfitJob.js:14, 20-43`\n\n**Persistence mechanism:**\n```javascript\nconst PAUSED_FILE = path.resolve(__dirname, \'..\', \'logs\', \'paused_automations.json\');\n\nfunction getPausedIds() {\n    if (fs.existsSync(PAUSED_FILE)) {\n        const data = fs.readFileSync(PAUSED_FILE, \'utf8\');\n        return JSON.parse(data) || [];\n    }\n    return [];\n}\n\nfunction savePausedIds(ids) {\n    const dir = path.dirname(PAUSED_FILE);\n    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });\n    fs.writeFileSync(PAUSED_FILE, JSON.stringify(ids), \'utf8\');\n}\n```\n\n**What survives restart:**\n- `paused_automations.json` ← list of automation IDs paused by daily target (saved to disk).\n- **At boot, the job re-reads this file and reactivates automations if a new day is detected** (line 71-88).\n\n#### 3.3 Daily-Cap Flag on Restart Mid-Day\n**Current behavior:**\n- If the server restarts **mid-day after hitting the daily target**, the `paused_automations.json` file persists.\n- On boot, the job calls `checkProfitAndControl()` which reads `lastCheckDay = new Date().getUTCDate()`.\n- If the day hasn\'t changed, **the paused automations stay paused** (they won\'t reactivate).\n- The `getPausedIds()` file is only cleared when a new day is detected (line 84: `savePausedIds([])`).\n\n**Implication for daily-loss cap:**\n- A **runtime flag for halt** (e.g. `DAILY_LOSS_CAP_TRIGGERED = true`) stored only in memory is **NOT recovered on restart**.\n- To persist a halt across restart, you **must write to disk** (like `paused_automations.json`).\n\n**Recommendation:** For a daily-loss cap:\n```javascript\nconst DAILY_CAP_FILE = path.resolve(__dirname, \'..\', \'logs\', \'daily_cap_state.json\');\n// Save at boot: { triggeredAt: ms, equityAtTrigger, halt: true }\n// On restart, read and re-arm the halt if the day hasn\'t changed\n```\n\n---\n\n### 4. WHERE TO WIRE A NEW MONITOR JOB + getStatus PATTERN\n\n**Question:** How are jobs started in server.js, how do they expose state to controllers?\n\n#### 4.1 Job Boot Sequence\n**File:** `backend/src/server.js:17-74`\n\n**Order of start() calls (line 48-73):**\n```javascript\n// Line 48: regimeJob (market regime gate)\nlogger(\'system\', `Starting the Regime Job...`);\nregimeJob.start();\n\n// Line 52: flowJob (taker flow / oracle state)\nlogger(\'system\', `Starting the Flow Job (shadow)...`);\nflowJob.start();\n\n// Line 58: fairPriceJob\nlogger(\'system\', `Starting the Fair Price Job...`);\nfairPriceJob.start();\n\n// Line 64: cockpitJob (read-only analytics)\nlogger(\'system\', `Starting the Cockpit Job (read-only analytics)...`);\ncockpitJob.start();\n\n// Line 69: funnelJob (Farm-and-Funnel shadow)\nlogger(\'system\', `Starting the Funnel Job (shadow)...`);\nfunnelJob.start();\n\n// Line 73: dailyProfitJob (daily target)\nlogger(\'system\', `Starting the Daily Profit Target Job...`);\ndailyProfitJob.start();\n```\n\n#### 4.2 How Jobs Expose State: getStatus() Pattern\n**File:** `backend/src/regimeJob.js`, `backend/src/flowJob.js`, `backend/src/cockpitJob.js`, `backend/src/funnelJob.js:288-300`\n\n**Pattern (funnelJob example, line 289-300):**\n```javascript\nfunction getStatus() {\n    return {\n        enabled: ENABLED, refreshMs: REFRESH_MS, mode: LIVE_BUY ? \'live\' : \'shadow\',\n        maxBuyUsdt: MAX_BUY_USDT, baselineUsdt: BASELINE_USDT,\n        runtimeBaselineUsdt: RUNTIME_BASELINE, minUsdt: MIN_USDT, symbol: BTC, running,\n        at: AT ? new Date(AT).toISOString() : null, ageMs: AT ? Date.now() - AT : null,\n        last: LAST,\n        fase4: {\n            enabled: FASE4_ENABLED, windowMs: FASE4_WINDOW_MS, observeMs: FASE4_OBSERVE_MS,\n            observing: !!obsTimer,\n            startedAt: obsStartAt ? new Date(obsStartAt).toISOString() : null,\n            until: obsUntil ? new Date(obsUntil).toISOString() : null,\n            // ...\n        }\n    };\n}\n\nmodule.exports = { start, stop, getStatus };  // exports the function\n```\n\n**How controllers consume it:**\n**File:** `backend/src/controllers/analysisController.js:47-49`\n```javascript\nfunction getRegimeStatus(req, res) {\n    res.json(regimeJob.getStatus());\n}\n\nfunction getFlowStatus(req, res) {\n    res.json(flowJob.getStatus());\n}\n\n// GET /analysis/regime-status calls getRegimeStatus()\n// GET /analysis/cockpit calls cockpitJob.getStatus()\n```\n\n**Router wiring:**\n**File:** `backend/src/routers/analysisRouter.js` (implied; routes are in app.js or a main router)\n\n#### 4.3 Template for Daily-Loss-Cap Job\n```javascript\n// backend/src/dailyCapJob.js\n\nlet timer = null;\nlet DAILY_CAP_STATE = {\n    enabled: ENABLED,\n    triggered: false,\n    equityAtArm: null,\n    threshold: DAILY_CAP_PERCENT,\n    triggeredAt: null,\n    ageMs: null,\n};\n\nasync function checkDailyCap() {\n    // read equity, compare to last snapshot, write halt if needed\n}\n\nfunction start() {\n    if (timer) return;\n    checkDailyCap();\n    timer = setInterval(checkDailyCap, CAP_CHECK_MS);\n    if (timer.unref) timer.unref();\n}\n\nfunction stop() {\n    if (timer) { clearInterval(timer); timer = null; }\n}\n\nfunction getStatus() {\n    return { ...DAILY_CAP_STATE };\n}\n\nfunction resetDaily() {\n    DAILY_CAP_STATE.triggered = false;\n    DAILY_CAP_STATE.equityAtArm = null;\n    DAILY_CAP_STATE.triggeredAt = null;\n}\n\nmodule.exports = { start, stop, getStatus, resetDaily };\n```\n\n**Integration in server.js (after line 73):**\n```javascript\nconst dailyCapJob = require(\'./dailyCapJob\');\n// ...\nlogger(\'system\', `Starting the Daily Cap Job...`);\ndailyCapJob.start();\n```\n\n**Exposure in controller (analysisController.js):**\n```javascript\nconst dailyCapJob = require(\'../dailyCapJob\');\n\nfunction getDailyCapStatus(req, res) {\n    res.json(dailyCapJob.getStatus());\n}\n\n// router: GET /analysis/daily-cap\n```\n\n---\n\n### 5. TRADING_HALT READ SITES (HOT-SWITCH COHERENCE)\n\n**Question:** Every place that reads TRADING_HALT, single chokepoint for orders?\n\n#### 5.1 TRADING_HALT Read Sites\n**File searches:**\n```\n/home/gcrux-tradeux/tradeux/backend/src/utils/exchange.js:26, 31-32\n/home/gcrux-tradeux/tradeux/backend/src/controllers/analysisController.js:80, 82\n```\n\n**Complete list:**\n\n1. **`backend/src/utils/exchange.js:26, 31-34`** (THE ENFORCEMENT CHOKEPOINT)\n```javascript\nconst TRADING_HALT = process.env.TRADING_HALT === \'true\';\n\nfunction assertWithinRisk(action, symbol, quantity, price, options) {\n    if (TRADING_HALT) {\n        const msg = `[riskGuard] TRADING_HALT ativo — ${action} ${symbol} BLOQUEADA (kill-switch).`;\n        logger(\'system\', msg);\n        throw new Error(msg);\n    }\n    // ... rest of notional check\n}\n```\n\n2. **`backend/src/controllers/analysisController.js:74-84`** (STATUS REPORTING)\n```javascript\nasync function getCockpitStatus(req, res) {\n    const status = cockpitJob.getStatus();\n    try {\n        const s = await settingsRepository.getSettings(process.env.DEFAULT_SETTINGS_ID || 1);\n        status.env = { useTestnet: !!(s && s.useTestnet), tradingHalt: process.env.TRADING_HALT === \'true\' };\n    } catch (e) {\n        status.env = { useTestnet: null, tradingHalt: process.env.TRADING_HALT === \'true\' };\n    }\n    res.json(status);\n}\n```\n\n**NOT found in:**\n- `tradeux-mcp/src/index.js` — MCP tools do NOT read `TRADING_HALT` directly; they call the backend API which enforces it.\n- `frontend/src` — frontend reads from `/analysis/cockpit` endpoint (reports `env.tradingHalt`).\n\n#### 5.2 Is exchange.js the SINGLE Chokepoint?\n**YES.** All order execution goes through one of these (lines 110-136):**\n\n```javascript\nfunction buy(symbol, quantity, price, options) {\n    options = options || {};\n    assertWithinRisk(\'BUY\', symbol, quantity, price, options);  // ← CHOKE\n    const type = options.type || \'MARKET\';\n    if (type === \'MARKET\')\n        return binance.marketBuy(symbol, quantity, options);\n    return binance.order(type, \'BUY\', symbol, quantity, price, options);\n}\n\nfunction sell(symbol, quantity, price, options) {\n    options = options || {};\n    assertWithinRisk(\'SELL\', symbol, quantity, price, options);  // ← CHOKE\n    const type = options.type || \'MARKET\';\n    if (type === \'MARKET\')\n        return binance.marketSell(symbol, quantity, options);\n    return binance.order(type, \'SELL\', symbol, quantity, price, options);\n}\n\nfunction oco(side, symbol, quantity, options) {\n    options = options || {};\n    assertWithinRisk(`OCO-${side}`, symbol, quantity, options.abovePrice || options.belowPrice, options);  // ← CHOKE\n    return binance.ocoOrder(side, symbol, quantity, options);\n}\n```\n\n**No other code path places orders.** All automations, manual UI, funnelJob, agent all call `exchange.buy()/sell()/oco()`.\n\n#### 5.3 Runtime Halt Coherence\n\n**Current state:**\n- `TRADING_HALT = process.env.TRADING_HALT === \'true\'` — **loaded once at module init, not live**.\n- To change halt status, must restart the backend (or modify `/proc/self/environ` in exotic scenarios).\n- UI and cockpit report the static value via `analysisController.getCockpitStatus()`.\n\n**To make it a true hot-switch:**\n1. **Move `TRADING_HALT` to a mutable location** (Beholder MEMORY, database, a file polled by all jobs).\n2. **Refactor `assertWithinRisk()` to read dynamically**:\n```javascript\nfunction assertWithinRisk(action, symbol, quantity, price, options) {\n    const HALT = (process.env.TRADING_HALT === \'true\') || beholder.getMemory(\'SYSTEM\', \'TRADING_HALT\');\n    if (HALT) {\n        const msg = `[riskGuard] TRADING_HALT ativo — ${action} ${symbol} BLOQUEADA (kill-switch).`;\n        logger(\'system\', msg);\n        throw new Error(msg);\n    }\n    // ...\n}\n```\n\n3. **Expose a setHalt API endpoint:**\n```javascript\n// POST /system/halt { halt: true|false }\n// → sets beholder.updateMemory(\'SYSTEM\', \'TRADING_HALT\', null, true|false, false)\n```\n\n**Recommendation:** Separate task — refactor to read `TRADING_HALT` from MEMORY at request time, not process.env at load time.\n\n---\n\n### 6. SETTINGS MODEL & RUNTIME CONTROL SURFACES\n\n**Question:** Settings table/model, MEMORY mechanism for persisted runtime flags, existing API endpoints + MCP tools?\n\n#### 6.1 Settings Model Structure\n**File:** `backend/src/models/settingsModel.js`\n\n**Existing schema** (inferred from `settingsRepository.js:45-100`):\n- `id` (PK)\n- `email` (unique, user login)\n- `password` (bcrypt hash)\n- `phone`, `pushToken` (notifications)\n- `apiUrl`, `streamUrl`, `accessKey`, `secretKey` (mainnet)\n- `testnetApiUrl`, `testnetStreamUrl`, `testnetAccessKey`, `testnetSecretKey`\n- `useTestnet` (boolean switch)\n- `sendGridKey` (email integration)\n\n**No arbitrary-field table exists.** Settings are strongly typed per above columns.\n\n#### 6.2 Beholder MEMORY for Runtime State\n**File:** `backend/src/beholder.js:13, 940-956, 973-983`\n\n**How MEMORY works:**\n```javascript\nconst MEMORY = {};  // line 13: module-level mutable state\n\nasync function updateMemory(symbol, index, interval, value, executeAutomations = true) {\n    // line 940-956\n    const memoryKey = parseMemoryKey(symbol, index, interval);\n    MEMORY[memoryKey] = value;\n    // optionally trigger automations\n}\n\nfunction getMemory(symbol, index, interval) {\n    // line 973-983\n    if (symbol && index) {\n        const memoryKey = `${symbol}:${index}`;  // "BTC:MINI_TICKER", "SYSTEM:TRADING_HALT"\n        return MEMORY[memoryKey];\n    }\n    return { ...MEMORY };  // all keys\n}\n```\n\n**Key properties:**\n- **Volatile:** Lost on restart. Designed for live market data (MINI_TICKER, BOOK, REGIME, FLOW, COCKPIT).\n- **Not persisted:** No disk flush (unlike `paused_automations.json`).\n- **Symbol-indexed:** Keys are `"${symbol}:${index}"` (e.g. `"BTCUSDT:MINI_TICKER"`, `"SYSTEM:TRADING_HALT"`).\n\n**For a persistent runtime flag (daily-cap state):**\n- **DO use MEMORY for the HOT state** (e.g. `MEMORY[\'SYSTEM:DAILY_CAP_TRIGGERED\'] = true`).\n- **DO persist to disk** (`logs/daily_cap_state.json`) for recovery on restart.\n- **Polling pattern:** dailyCapJob reads MEMORY state; if restart happens mid-day, re-read from disk.\n\n#### 6.3 Existing API Endpoints + MCP Tools\n\n**Automation control endpoints:**\n**File:** `backend/src/routers/automationsRouter.js:15-17`\n```javascript\nrouter.post(\'/:id/start\', automationsController.startAutomation);\nrouter.post(\'/:id/stop\', automationsController.stopAutomation);\n```\n\n**Implementation (automationsController.js:50-94):**\n```javascript\nasync function startAutomation(req, res, next) {\n    // set isActive=true, update brain or agenda, save\n}\n\nasync function stopAutomation(req, res, next) {\n    // set isActive=false, remove from brain or agenda, save\n}\n```\n\n**MCP tools for control:**\n**File:** `tradeux-mcp/src/index.js:400-450+`\n\n```javascript\nwriteTool(\n  "tradeux_start_automation",\n  "Inicia uma automação.",\n  { id: z.number().int().describe("ID da automação") },\n  ({ id }) => api.post(`/automations/${id}/start`)\n);\n\nwriteTool(\n  "tradeux_stop_automation",\n  "Para uma automação.",\n  { id: z.number().int().describe("ID da automação") },\n  ({ id }) => api.post(`/automations/${id}/stop`)\n);\n```\n\n#### 6.4 Template for Daily-Cap Control Surface\n\n**API endpoint:**\n```javascript\n// POST /system/daily-cap-reset { force: true }\n// → resets DAILY_CAP_STATE, clears halt flag\n\n// GET /system/daily-cap-status (or via /analysis/daily-cap)\n// → returns { enabled, triggered, equityAtArm, threshold, ... }\n\n// PATCH /system/daily-cap { enabled: true|false, percent: 5 }\n// → updates config (env-like but live-editable)\n```\n\n**MCP tool template:**\n```javascript\nreadTool(\n  "tradeux_get_daily_cap_status",\n  "Status do daily-loss-cap: se disparado, equity base, limite %.",\n  {},\n  () => api.get("/analysis/daily-cap")\n);\n\nwriteTool(\n  "tradeux_reset_daily_cap",\n  "Reset do daily-loss-cap (manualmente re-arma a proteção).",\n  {},\n  () => api.post("/system/daily-cap-reset")\n);\n\nwriteTool(\n  "tradeux_set_daily_cap_halt",\n  "Força a parada de emergência via daily-cap (hot kill-switch).",\n  { enabled: z.boolean().describe("true to halt, false to resume") },\n  ({ enabled }) => api.patch("/system/daily-cap", { halt: enabled })\n);\n```\n\n---\n\n## SUMMARY TABLE: KEY FILE:LINE REFERENCES\n\n| Question | File | Line | Key Insight |\n|----------|------|------|------------|\n| 1. Balance object shape | `exchangeController.js` | 7–30 | ALL coins returned; per-coin fiat conversion |\n| 1. Equity in funnelJob | `funnelJob.js` | 85–96, 250 | `usdtFree + btcReserve × price` from MINI_TICKER |\n| 1. Equity helper | (none exist) | — | Must build custom from balance() + MEMORY prices |\n| 2. Daily profit calc | `dailyProfitJob.js` | 45–61 | **CASH FLOW not realized PnL** (buy−sell) |\n| 2. `net` definition | `ordersRepository.js` | 227–242 | cumulative quote qty, minus commission in quote |\n| 2. Cost basis | `ordersRepository.js` | 244–300 | `getFarmPosition()`, `getTrendPosition()` exist but NOT used for PnL |\n| 3. Day rollover | `dailyProfitJob.js` | 17, 65–71 | `getUTCDate()` comparison; resets on new day |\n| 3. Persist across restart | `dailyProfitJob.js` | 14, 20–43 | `paused_automations.json` survives restart |\n| 3. Mid-day restart gotcha | `dailyProfitJob.js` | 71–88 | Paused automations stay paused if day hasn\'t changed |\n| 4. Job boot order | `server.js` | 48–73 | regime → flow → fair → cockpit → funnel → daily profit |\n| 4. getStatus() pattern | `funnelJob.js`, `regimeJob.js` | 289–300, (similar) | Module exports `{ start, stop, getStatus }` |\n| 4. Controller consumption | `analysisController.js` | 47–49, 74–85 | `regimeJob.getStatus()`, `cockpitJob.getStatus()` in response |\n| 5. TRADING_HALT reads | `exchange.js` | 26, 31–34 | Loaded once at module init in `assertWithinRisk()` |\n| 5. Status reporting | `analysisController.js` | 80, 82 | `process.env.TRADING_HALT === \'true\'` in `/analysis/cockpit` |\n| 5. Single chokepoint? | `exchange.js` | 110–136 | YES — all orders via `buy()`, `sell()`, `oco()` call `assertWithinRisk()` |\n| 6. Settings model | `settingsRepository.js` | 45–100 | Strongly typed; no arbitrary-field mechanism |\n| 6. MEMORY for runtime state | `beholder.js` | 13, 940–956, 973–983 | Volatile, symbol-indexed (`"SYS:KEY"`), not persisted |\n| 6. Automation control | `automationsRouter.js` | 15–17 | `POST /automations/:id/start`, `:id/stop` |\n| 6. MCP tools | `tradeux-mcp/src/index.js` | 400+, (lines vary) | `tradeux_start_automation`, `tradeux_stop_automation` + ~25 others |\n\n---\n\n## FLAGGED GOTCHAS FOR IMPLEMENTATION\n\n1. **Daily-profit job uses cash flow, not realized PnL.** A daily-loss cap CANNOT use the same logic. Must snapshot equity at UTC midnight and compare current equity.\n\n2. **TRADING_HALT is loaded once at module init.** To make it a true hot-switch, refactor to read from MEMORY or a polled file at request time, not `process.env` at load.\n\n3. **Mid-day restart preserves halt state via disk file, but only clears on next UTC rollover.** If the cap triggers at noon and the server restarts at 1pm, the flag stays until UTC midnight (day boundary). Plan for this in the UX (manual reset endpoint).\n\n4. **Beholder MEMORY is volatile.** Persist daily-cap state to disk (`logs/daily_cap_state.json`) to recover on restart.\n\n5. **getUTCDate() is day-of-month only (1–31).** Month boundaries work (30 → 1), but the string `"lastCheckDay"` pattern is not timezone-safe for systems running non-UTC. Use `new Date().toISOString().split(\'T\')[0]` (YYYY-MM-DD) for global safety.\n\n6. **No realized-PnL helper exists.** To compute true PnL for audits, iterate orders by cost-basis (getFarmPosition + getTrendPosition give you the scaffold, but you must compute matching buys→sells).\n\n7. **Exchange.js is the chokepoint, but MCP tools are gated at the tool level** (`tradingEnabled()` check, `TRADEUX_ALLOW_TRADING` env). The hot-halt in exchange.js is backend-only; if the MCP gate is open but exchange.js halts, the agent sees an error (good fail-closed behavior, but coherence for the operator depends on both being in sync).\n\n---\n\nThis completes the comprehensive read-only analysis. All findings are grounded in exact file:line references with minimal code excerpts. The implementation plan can now be written with confidence in the actual mechanics.'}]
> ```

## 🤖 Claude *(13:24:14)*


## 🤖 Claude *(13:24:18)*

A exploração fechou o desenho. Dois achados decisivos:

1. **`getDailyProfit()` é cash-flow (`sellNet − buyNet`), não P&L realizado** → num dia de acumulação (comprar sem vender) ele marca "perda" que não é perda. Pra um cap de −5% isso falsa-dispara. O caminho correto é **drawdown de equity** (snapshot do equity total na virada UTC, compara com o atual).
2. **`assertWithinRisk` é o chokepoint único** de toda ordem real (buy/sell/oco) — confirmado, nada desvia dele. E `TRADING_HALT` é `const` no load → o refactor pra ler runtime resolve o "HALT-frio" e dá o gancho pro cap auto-halt.

Duas decisões de **política de risco** são suas — mudam o que vou implementar no money-path:

## 🤖 Claude *(13:24:26)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "Como medir a perda di\u00e1ria que dispara o cap de \u22125%? (o valor \u22125% voc\u00ea j\u00e1 aprovou; aqui \u00e9 a M\u00c9TRICA)",
      "header": "M\u00e9trica do cap",
      "multiSelect": false,
      "options": [
        {
          "label": "Drawdown de equity (recomendado)",
          "description": "Snapshot do equity TOTAL (USDT + valor das posi\u00e7\u00f5es a pre\u00e7o de mercado) na virada UTC; dispara se o equity atual cair \u22655% vs o snapshot. Robusto: acumula\u00e7\u00e3o (comprar sem vender) N\u00c3O falsa-dispara. Custo: precisa precificar a carteira via MINI_TICKER e tratar pre\u00e7o frio fail-safe (n\u00e3o dispara no escuro)."
        },
        {
          "label": "Cash-flow realizado (reusa dailyProfitJob)",
          "description": "sellNet \u2212 buyNet do dia (c\u00f3digo que j\u00e1 existe). Simples e m\u00ednimo. MAS falsa-dispara em dia de acumula\u00e7\u00e3o e ignora o valor da posi\u00e7\u00e3o aberta \u2014 pode travar o sistema por uma 'perda' que \u00e9 s\u00f3 capital alocado."
        }
      ]
    },
    {
      "question": "Quando o cap de \u22125% disparar, o que o guard deve bloquear?",
      "header": "Escopo do bloqueio",
      "multiSelect": false,
      "options": [
        {
          "label": "Tudo, igual ao HALT (recomendado)",
          "description": "Bloqueia BUY/SELL/OCO \u2014 circuit-breaker total at\u00e9 a virada UTC ou reset manual do operador. Mais simples, menos l\u00f3gica nova no money-path, sem\u00e2ntica id\u00eantica ao kill-switch. Contra: trava tamb\u00e9m venda protetiva."
        },
        {
          "label": "S\u00f3 entradas (BUY); deixa passar venda/sa\u00edda",
          "description": "Permite o sistema/dono REDUZIR risco (death cross, stop, venda no-loss) mesmo com o cap batido; s\u00f3 barra abrir risco novo. Mais 'correto' p/ loss-cap, por\u00e9m mais l\u00f3gica condicional no guard (e OCO tem 2 pernas)."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "Como medir a perda diária que dispara o cap de −5%? (o valor −5% você já aprovou; aqui é a MÉTRICA)"="Drawdown de equity (recomendado)", "Quando o cap de −5% disparar, o que o guard deve bloquear?"="Tudo, igual ao HALT (recomendado)". You can now continue with these answers in mind.
> ```

## 🤖 Claude *(13:27:02)*


## 🤖 Claude *(13:27:03)*

Decisões travadas: **drawdown de equity** + **bloqueia tudo (circuit-breaker total)**. Vou rodar um agente de design (Plan) pra validar a arquitetura que tenho em mente contra esses requisitos e cravar os edge-cases do money-path antes de escrever o plano final.

## 🤖 Claude *(13:27:49)*


🛠️ **Tool Call**: `Agent`
```json
{
  "description": "Design daily-cap + hot kill-switch",
  "subagent_type": "Plan",
  "prompt": "Design the implementation plan for a safety feature in the TradeUX trading bot at /home/gcrux-tradeux/tradeux (Node/Express + Sequelize, comments in pt-BR). READ-ONLY \u2014 produce a concrete plan, do not edit.\n\n# Goal (item \"(e)\" of the mainnet de-freeze checklist)\nAdd a **daily loss cap of \u22125%** AND refactor the risk guard into a **HOT kill-switch** (today TRADING_HALT is read as a `const` at module load \u2192 not hot; resolving the cap forces the refactor, closing both).\n\n# Decisions already made by the owner (do NOT revisit)\n1. Metric = **equity drawdown**: snapshot TOTAL account equity (USDT free + value of all coin holdings at market price) at the UTC day boundary; trip when current equity \u2264 snapshot \u00d7 0.95.\n2. When tripped, **block ALL orders** (BUY/SELL/OCO) \u2014 full circuit breaker, identical semantics to TRADING_HALT \u2014 until UTC day rollover or an operator manual reset.\n\n# Established facts from codebase exploration (file:line)\n- **Guard chokepoint**: `backend/src/utils/exchange.js:26-52`. `const TRADING_HALT = process.env.TRADING_HALT==='true'` (line 26, load-time). `assertWithinRisk()` (30) throws if TRADING_HALT, then checks MAX_ORDER_NOTIONAL_USDT. All real orders pass through `buy()/sell()/oco()` (110-136) which call assertWithinRisk \u2014 CONFIRMED single chokepoint, nothing bypasses it. `refPrice(symbol)` (58-67) lazy-requires beholder to read MINI_TICKER.close.\n- **Halt reporting**: `backend/src/controllers/analysisController.js:74-84` getCockpitStatus sets `status.env.tradingHalt = process.env.TRADING_HALT==='true'`. This feeds the /cockpit UI (`frontend/src/private/Cockpit/Cockpit.js:235`) and the agent (MCP tradeux_get_cockpit). MCP/frontend do NOT read the env directly \u2014 only via this endpoint.\n- **Equity primitives**: no existing total-equity helper. `exchange.balance()` returns an object keyed by coin \u2192 `{available, onOrder}` (all assets). `beholder.tryFiatConversion(coin, amount, fiat)` exists. `beholder.getMemory(symbol,'MINI_TICKER').close` gives live price. funnelJob.js:73-96,250 shows the pattern: `equity = usdtFree + btcReserve*price`, price from MINI_TICKER, fail-safe to null when price cold.\n- **Daily PnL (do NOT use for the cap)**: `dailyProfitJob.js:45-61` getDailyProfit = sellNet\u2212buyNet (cash flow, false-trips on accumulation). `ordersRepository.js:227-242` defines `net`. `getFarmPosition/getTrendPosition` (244-300) compute cost basis but no realized-PnL helper.\n- **Job pattern**: jobs are `backend/src/*Job.js` exposing `{start, stop, getStatus}`, started in `server.js:48-73` (regimeJob, flowJob, fairPriceJob, cockpitJob, funnelJob, dailyProfitJob \u2014 each `logger(...)` + `.start()`). Controllers expose state via `regimeJob.getStatus()` etc in analysisController. Timers use `setInterval` + `timer.unref()`.\n- **Day rollover + persistence pattern**: dailyProfitJob uses module-level `lastCheckDay = new Date().getUTCDate()` (line 17) and persists paused IDs to `logs/paused_automations.json` via fs (14,20-43). Beholder MEMORY is volatile (lost on restart).\n- **Control surfaces**: automations have `POST /automations/:id/start|stop` (automationsRouter.js:15-17) + MCP write tools `tradeux_start_automation/stop_automation`. Settings model is strongly-typed columns (no arbitrary JSON field).\n- **Gotcha (from project memory)**: editing files via the harness poisons file ownership to `ubuntu`; the repo runs as user `gcrux-tradeux`; `.env` is 600. TRADING_HALT/MAX_ORDER_NOTIONAL are NOT hot today; the real panic button is `docker compose stop backend`. The doctrine: \"Claude does NOT flip TRADING_HALT\".\n\n# What I need from you \u2014 a concrete, minimal, money-path-safe plan covering:\n\n1. **A new `riskState` module** (`backend/src/riskState.js`) as the single source of halt truth: module-level mutable flag(s) with reason/source/timestamp; `isHalted()`, `getState()`, `setHalt(on, reason, source)`. Seeded at boot by env `TRADING_HALT=true` (env halt is a permanent floor \u2014 can't be cleared by reset), plus a manual operator halt and a daily-cap halt as separate sources. Persisted to disk (`logs/risk_state.json`) so a tripped cap / manual halt survives a container restart; on load, re-arm if still same UTC day, auto-expire the daily-cap source on UTC rollover. Pure/testable, no require cycle (it must NOT depend on exchange.js; exchange.js will require IT). Decide: top-level require vs lazy.\n\n2. **Guard refactor** in `exchange.js`: replace the load-time `const TRADING_HALT` with a call to `riskState.isHalted()` inside `assertWithinRisk()` at order time, preserving the exact throw/log behavior and the existing MAX_ORDER_NOTIONAL check. Keep env `TRADING_HALT` working (via riskState seed). Confirm no behavior change when nothing trips.\n\n3. **A new `dailyCapJob`** (`backend/src/dailyCapJob.js`): on boot/first-run snapshot equity for the current UTC day (persisted), poll every N ms, compute current total equity (build the equity helper \u2014 where should it live? a util? reuse tryFiatConversion or MINI_TICKER?), trip `riskState.setHalt(true,'daily-loss-cap -5%','daily-cap')` + Telegram notify when equity \u2264 snapshot\u00d70.95. Fail-safe: if equity can't be valued (cold prices), DO NOT trip and log. On UTC rollover: re-snapshot, clear the daily-cap halt source (but never the env/manual halt). Env knobs (DAILY_LOSS_CAP_PCT default 0.05, check interval, enable flag). getStatus() for the controller.\n\n4. **Reporting coherence**: update analysisController getCockpitStatus to report `riskState.getState()` (hot) instead of `process.env.TRADING_HALT`, so /cockpit + agent see the live halt + reason/source. Consider whether the cockpit env payload should carry the reason/source (so the agent can report \"halt by daily-cap \u22125%\" vs operator halt) \u2014 and whether the agent's notifyDedup 'halt' family still de-dups correctly.\n\n5. **Operator hot-switch surface**: a backend endpoint to manually flip the hot halt (POST /system/halt {on,reason}?) and a daily-cap reset/re-arm. IMPORTANT doctrine: the LLM agent must NOT be able to flip halt (operator-only) \u2014 so do NOT add an MCP write tool for it; read-only exposure only. Decide router placement (new systemRouter? extend analysisRouter?) and auth (same JWT middleware as other routers).\n\n6. **Edge cases / failure modes to address explicitly**: stale/cold MINI_TICKER for a held alt (don't trip blind); equity snapshot missing on a fresh boot mid-day (snapshot now, accept that intra-day-before-boot drawdown is lost \u2014 or persist); the env-halt-vs-reset precedence; double-trip idempotency (don't re-notify every poll); the MAX_ORDER_NOTIONAL symbol-aware caveat is out of scope but note interactions; UTC `getUTCDate()` month-boundary safety (prefer YYYY-MM-DD key); ensuring `timer.unref()`; how a SELL-side protective order interacts (owner chose block-all, so note the consequence). Also: is there any startup-order issue (dailyCapJob needs exchange + beholder ready)?\n7. **Test/verification plan**: no unit-test harness exists (CI = migrate+seed+agent --check). Propose how to verify: a small node self-test for riskState (pure logic: seed/set/reset/rollover/persist), manual curl against the running backend for the endpoint + /cockpit, and how to exercise the cap trip safely WITHOUT real orders (the system is in HALT). Note CI preflight `bash scripts/ci-preflight.sh`.\n\nDeliver: a step-by-step plan listing exact files to create/modify, the key function signatures, the env knobs, the data shape persisted to disk, and a risk/rollback note. Keep it minimal and idiomatic to this codebase (match the existing *Job.js + repository patterns, pt-BR comments). Call out anything you'd push back on as over-engineering."
}
```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-17 - agent-aff65e0ac55826d37]]
> * **Próxima Sessão**: [[2026-06-18 - agent-a14dd3dd37735a84e]]
%% --- TIMELINE END --- %%

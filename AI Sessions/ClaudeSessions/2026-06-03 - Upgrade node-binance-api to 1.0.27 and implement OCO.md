---
type: session-stub
archived: true
original_size_bytes: 521113
original_size: 509 KB
date: 2026-06-03
session_id: 9b8145ac-8e22-490e-8799-cba80ba967e4
full_path: _full-sessions/ClaudeSessions/2026-06-03 - Upgrade node-binance-api to 1.0.27 and implement OCO.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-03%20-%20Upgrade%20node-binance-api%20to%201.0.27%20and%20implement%20OCO.md
---

# Upgrade node-binance-api to 1.0.27 and implement OCO

> [!abstract] Sessao arquivada
> O conteudo completo (**509 KB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-03%20-%20Upgrade%20node-binance-api%20to%201.0.27%20and%20implement%20OCO.md)**

- **Data:** 2026-06-03
- **Session ID:** `9b8145ac-8e22-490e-8799-cba80ba967e4`
- **Tamanho original:** 509 KB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-06-03 - Upgrade node-binance-api to 1.0.27 and implement OCO.md`

## Roteiro da sessao

- Contexto: TradeUX (Beholder-based Binance Spot bot), repo em /home/gcrux-tradeux/tradeux, branch master, model

## Previa

> # Upgrade node-binance-api to 1.0.27 and implement OCO
> **Date:** 2026-06-03 | **Session ID:** `9b8145ac-8e22-490e-8799-cba80ba967e4`
> 
> ---
> 
> ## 👤 User *(17:24:55)*
> 
> Contexto: TradeUX (Beholder-based Binance Spot bot), repo em /home/gcrux-tradeux/tradeux, branch master, modelo trunk-based (commit direto no master + push). Token do GitHub está em ~/tradeux/.env como GITHUB_TOKEN_API (gitignored). Shell roda como ubuntu; atue no repo como gcrux-tradeux via `sudo -n -u gcrux-tradeux`. Containers via `docker compose` (rodar como gcrux-tradeux, que lê o .env).
> 
> Tarefa: bumpar `node-binance-api` de ^0.13.1 para ^1.0.27 no backend e revalidar em testnet. Por quê:
> 1. SEGURANÇA: é a única fonte das 8 vulnerabilidades moderate transitivas restantes do backend (`request`@2.88 deprecated/no-fix, `qs`, `tough-cookie`, `uuid`). Ver SECURITY.md (roadmap item 1). As deps diretas já são modernas; só falta esse core.
> 2. Hoje existe um workaround em backend/package.json: `"overrides": { "form-data": ">=2.5.4" }` que neutraliza a crítica do form-data que o node-binance-api@0.13 trazia. APÓS o bump, REMOVER esse override e reconferir `npm audit` (a árvore nova do node-binance-api 1.x deve trazer form-data moderno sozinha).
> 3. node-binance-api 1.x reestrutura a API usada em backend/src/utils/exchange.js (a fronteira Binance — HOT-PATH do trading). É preciso adaptar exchange.js ao novo API (assinaturas de exchangeInfo, order, candles, streams mudaram entre 0.13 e 1.x).
> 4. BÔNUS: a 1.x reporta suporte a OCO (a 0.13.5 não tinha — HANDOFF registrou isso como deferido). Aproveitar para implementar OCO (POST /api/v3/order/oco; cancel via orderList) e fechar esse débito, com wiring no Beholder após o buy.
> 
> Como validar (testnet, ALLOW_TRADING controlado): smoke de exchangeInfo/symbols, um stream de candle, e UMA ordem de teste (MIN_NOTIONAL) — confirmar fill e que o Beholder não quebrou no hot-path. Idealmente smoke de um OCO. Rodar o gate QA+Tech-Lead (agentes em .claude/agents) ANTES de subir, porque é hot-path de trading. Só commitar/pushar trunk-based depois de aprovado + boot limpo (docker compose up -d backend, sem erro de require, site 200, automações id2/id3 re-armadas).
> 
> Risco: mudança de API no core de ordens. Fazer com cuidado, testar bem em testnet antes de qualquer cogitação de mainnet.
> 
> ## 🤖 Claude *(17:25:32)*
> 
> 
> ## 🤖 Claude *(17:25:33)*
> 
> Vou começar entendendo o estado atual antes de tocar em qualquer coisa — é hot-path de trading, então reconhecimento primeiro. Deixa eu carregar o contexto de continuidade (HANDOFF) e os arquivos-chave em paralelo.
> 
> ## 🤖 Claude *(17:25:35)*
> 
> 
> 🛠️ **Tool Call**: `Bash`
> ```json
> {
>   "command": "sudo -n -u gcrux-tradeux git -C /home/gcrux-tradeux/tradeux status 2>&1 | head -30; echo \"---BRANCH---\"; sudo -n -u gcrux-tradeux git -C /home/gcrux-tradeux/tradeux branch -vv 2>&1 | head -10; echo \"---LAST COMMITS---\"; sudo -n -u gcrux-tradeux git -C /home/gcrux-tradeux/tradeux log --oneline -8 2>&1",
>   "description": "Check repo git status, branch, recent commits"
> }

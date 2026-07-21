---
type: session-stub
archived: true
original_size_bytes: 1961178
original_size: 1.9 MB
date: 2026-06-03
session_id: cba664a2-9bab-474e-ae2c-a43a7cdabd93
full_path: _full-sessions/ClaudeSessions/2026-06-03 - Wire OCO orders into Beholder automation engine.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-03%20-%20Wire%20OCO%20orders%20into%20Beholder%20automation%20engine.md
---

# Wire OCO orders into Beholder automation engine

> [!abstract] Sessao arquivada
> O conteudo completo (**1.9 MB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-03%20-%20Wire%20OCO%20orders%20into%20Beholder%20automation%20engine.md)**

- **Data:** 2026-06-03
- **Session ID:** `cba664a2-9bab-474e-ae2c-a43a7cdabd93`
- **Tamanho original:** 1.9 MB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-06-03 - Wire OCO orders into Beholder automation engine.md`

## Roteiro da sessao

- Wire OCO (One-Cancels-the-Other) into the Beholder automation engine of TradeUX (repo: /home/gcrux-tradeux/tra

## Previa

> # Wire OCO orders into Beholder automation engine
> **Date:** 2026-06-03 | **Session ID:** `cba664a2-9bab-474e-ae2c-a43a7cdabd93`
> 
> ---
> 
> ## 👤 User *(19:40:07)*
> 
> Wire OCO (One-Cancels-the-Other) into the Beholder automation engine of TradeUX (repo: /home/gcrux-tradeux/tradeux). The exchange-boundary plumbing is DONE (committed in 063df19); this task is the Beholder/persistence/userData wiring that was deliberately deferred.
> 
> ## Context / what already exists
> - `backend/src/utils/exchange.js` already exposes (validated on testnet, place+cancel OK):
>   - `oco(side, symbol, quantity, options)` → `binance.ocoOrder(...)` → POST `v3/orderList/oco` (NEW OCO endpoint, ccxt fork node-binance-api@1.x).
>   - `cancelOrderList(symbol, orderListId)` → DELETE `v3/orderList`.
>   - OCO params schema (NEW endpoint) for a protective SELL after a BUY: `{ aboveType:'LIMIT_MAKER', abovePrice:<TP>, belowType:'STOP_LOSS_LIMIT', belowPrice:<stop limit>, belowStopPrice:<stop trigger>, belowTimeInForce:'GTC' }`. Response has `orderListId` + `orderReports[]` (2 legs) + `listStatusType`/`listOrderStatus`.
> - The userData wrapper forwards a `listStatusCallback` (5th arg of `binance.websockets.userData`), but `backend/src/app-em.js` `startUserDataMonitor` currently passes only ONE callback (no listStatus handling). Raw `listStatus` event has `data.e === 'listStatus'`.
> 
> ## Scope of THIS task
> 1. **Order model / persistence**: `backend/src/models/orderModel.js` has no `orderListId`. Add a nullable `orderListId` (BIGINT) column via a Sequelize migration **portable across mysql AND postgres** (CI runs migrate+seed on both — see `backend/config/`). Persist `orderListId` on both OCO legs.
> 2. **Beholder action flow**: decide the trigger — likely a new order-template `type:'OCO'` (see `STOP_TYPES`/`LIMIT_TYPES` in `backend/src/beholder.js` and `ordersRepository.js`) OR a post-BUY hook placing a protective OCO SELL (TP+SL) computed from the template (reuse `calcPrice`/`calcQty`, `beholder.js` ~lines 170-320). Persist both legs, consistent with current `placeOrder` (`beholder.js` ~269-366).
> 3. **userData listStatus**: in `app-em.js` `startUserDataMonitor`, pass a second callback to `exchange.userDataStream(updateCb, listStatusCb)` and handle `listStatus` → when one leg fills, mark the list resolved + update orders/beholder memory (Binance auto-cancels the other leg).
> 4. **Cancel path**: surface `exchange.cancelOrderList(symbol, orderListId)` from controller/automation (e.g. when an automation stops).
> 5. (Optional) Frontend OCO order template in `frontend/`.
> 
> ## Validation (MANDATORY — trading hot-path)
> - TESTNET only. Stack via Docker at /home/gcrux-tradeux/tradeux on port 8090; `.env` is testnet. Panel login in `.env` (`DEFAULT_SETTINGS_EMAIL`/`DEFAULT_SETTINGS_PWD`).
> - Smoke: a BUY that triggers an OCO SELL → confirm 2 legs persisted with `orderListId`; let a leg fill or cancel via `cancelOrderList` → confirm `listStatus` handled + DB/beholder consistent. Rebuild backend image, confirm clean boot (logs are FILE-only in prod: `docker compose exec backend cat /app/logs/system.log`; NODE_ENV=production disables console transport).
> - Run the **qa-engineer + tech-lead** gate on the diff BEFORE committing.
> 
> ## Box gotchas (read memories `git-ownership-gotcha`, `tradeux-deploy-topology`, `tradeux-orchestration-model`)
> - Shell runs as `ubuntu`; do ALL git/docker as `sudo -n -u gcrux-tradeux`. `npm install` as ubuntu poisons `.git` (npm calls git for gitHead) → `sudo -n chown -R gcrux-tradeux:gcrux-tradeux .git` after + chown regenerated `package-lock.json` before committing as gcrux. node/npm live under ubuntu's nvm (gcrux can't exec them) → run npm as ubuntu, then chown.
> - Trunk-based: commit direct to master + push via `GITHUB_TOKEN_API` from `.env` inline in an HTTPS URL (`git push https://x-access-token:$TOKEN@github.com/gabrielZarattini/tradeux.git HEAD:master`) — `origin` is SSH and gcrux has no key. Only commit/push after testnet validation + gate + clean boot. Migrations idempotent + portable; pt-BR comments.
> 
> ## 🤖 Claude *(19:40:19)*
> 
> 

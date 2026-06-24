# SOP — Nightly Circadian Cycle v1.0

**Versão:** v1 · **Selada:** 2026-05-17 · **Lei 2 (Processo Antecipado)** · **SSP-01 OE03**

## ORO triplet

- **Operator:** cron daemon (system); manual fallback é Sovereign via shell direto
- **Reviewer:** Sovereign (revisa briefing matinal entregue ao Telegram diariamente — é o "review acceptance" implícito)
- **Owner:** Sovereign (até v6.4.x); depois engineer agent (infra ownership)

## Contexto

Rotinas noturnas autonômicas modeladas em arquitetura humana de sono. 3 estágios espaçados 2h em horário BRT (`America/Sao_Paulo`) para isolamento de CPU/IO, thermal recovery do servidor e separação clara de responsabilidades. Refator de `30 2 * * * nightly-bridge-refresh.sh` + `30 3 * * * morning-briefing.sh` (sequenciais, sobrepostos) → 3 stages independentes (03:00 / 05:00 / 07:00 BRT).

| Stage | Hora BRT | Script | Foco | Falha → próximo? |
|-------|----------|--------|------|------------------|
| 1 — Light Sleep | 03:00 | `nightly-stage1-light-sleep.sh` | IO (cleanup, log rotation, health spot check) | Sim — estágios são independentes |
| 2 — Deep Sleep | 05:00 | `nightly-stage2-deep-sleep.sh` | Integridade (mesh reindex, VACUUM, ledger drift watch) | Sim |
| 3 — REM Cycle | 07:00 | `nightly-stage3-rem.sh` | Inteligência (news pulse + briefing) | N/A (último estágio) |

OpenClaw native cron `Memory Dreaming Promotion` (em `~/.openclaw/cron/jobs.json` schedule `0 3 * * *`) **sobrepõe Stage 1** — daemon próprio, IO próprio, sem race condition.

## Pre-conditions

- Server timezone = `America/Sao_Paulo` (-03). Verificar com `timedatectl | grep "Time zone"`. Se UTC, converter horários: 03→06, 05→08, 07→10.
- `/var/log/mcorch-*.log` existe (criado pelos cron handlers em primeira execução; pre-touch opcional).
- `~/.openclaw/secrets.json` chmod 600 (Telegram bot token).
- `mcorch_chroma` healthy + Chroma API v2 acessível (`http://localhost:8001/api/v2/heartbeat`).

## Sequence — execução manual humana (fallback)

| # | Action | Output esperado | Verification gate |
|---|--------|-----------------|-------------------|
| 1 | `bash scripts/nightly-stage1-light-sleep.sh` | Log apêndice em `/var/log/mcorch-stage1.log` com `STAGE1 DONE (zero failures)` | tail mostra final OK + zero incidents em `/tmp/openclaw-incidents/` |
| 2 | `bash scripts/nightly-stage2-deep-sleep.sh` | Log em `/var/log/mcorch-stage2.log` com bridge + drift report + VACUUM line | `STAGE2 DONE`; se drift > 0, linha WARN com lista de user_ids |
| 3 | `bash scripts/nightly-stage3-rem.sh` | Briefing entregue ao Telegram chat 5835174772 + 1 nó `news_pulse` novo em `mcorch_nodes` | HTTP 200 do Telegram + nó recuperável via REST |
| 4 | `crontab -l \| grep nightly-stage` | 3 linhas: 03:00, 05:00, 07:00 | exato match |

## Verification gates

- **Stage 1:** `/var/log/mcorch-stage1.log` última linha = `STAGE1 DONE` E `infra_health_logs` tem entrada `service='nightly-stage1'`, `status='healthy'` ≤5min atrás.
- **Stage 2:** bridge refresh OK (`/var/log/mcorch-nightly-bridge.log` última linha "DONE"); drift query retorna explicitamente (vazio ou lista). VACUUM se rodou, log mostra "VACUUM completed in Xs".
- **Stage 3:** Telegram API retornou HTTP 200 (em `/tmp/morning-briefing-tg-response.json`); 1 nó novo `node_type='news_pulse'` criado nas últimas 30min.

## Recovery path

- **Stage 1 falhou (cleanup quebrou):** `find` pode falhar se `/tmp/openclaw-incidents/` não existe. Criar com `mkdir -p`. Logrotate pode falhar se `/var/log/mcorch-*.log` sem write perm — `chmod 664` necessário (gcrUX user owner).
- **Stage 2 falhou (bridge):** verificar `mcorch_chroma` healthy. Se down: `docker compose up -d mcorch-vector-engine`. Re-rodar `nightly-bridge-refresh.sh` manualmente.
- **Stage 2 falhou (VACUUM timeout):** se VACUUM `mcorch_nodes` levou >5min, comentar a linha de VACUUM no script. Promover para weekly cron separado (`0 5 * * 0`).
- **Stage 3 falhou (Firecrawl/OpenRouter):** Stage 3 é best-effort para news pulse — briefing roda sem News Pulse section. Verificar `~/.openclaw/secrets.json` se Telegram falhou; rotacionar token via BotFather se comprometido.
- **Ledger drift detectado:** SOP `mcoins-ledger-reconciliation.md` para decisão Sovereign. Stage 2 NÃO auto-backfill.

## Success signal

- Diariamente: Telegram bot @claw_gcrux envia briefing antes das 07:30 BRT.
- `infra_health_logs` tem 3 entradas por dia: `service IN ('nightly-stage1', 'nightly-stage2', 'nightly-stage3')`, todas `status='healthy'`.
- `mcorch_nodes` ganha 1 nó `news_pulse` por dia (verificar: `SELECT count(*) FROM mcorch_nodes WHERE node_type='news_pulse' AND created_at > now() - interval '24h'`).
- Zero incidentes em `/tmp/openclaw-incidents/` por 7 dias = ciclo saudável.

## Anti-patterns

- ❌ Empilhar mais estágios sem espaçamento (vira sequencial denso, perde isolamento de CPU/IO).
- ❌ Stages que assumem ordem estrita (são independentes — Stage 3 NÃO pode depender de output do Stage 2 fora do banco).
- ❌ Promover briefing para horário diferente sem avisar Sovereign (07:00 BRT é o cliente-facing handshake).
- ❌ Auto-backfill de ledger drift sem decisão humana (Stage 2 só ALERTA).

## Referências

- `scripts/nightly-stage1-light-sleep.sh`
- `scripts/nightly-stage2-deep-sleep.sh`
- `scripts/nightly-stage3-rem.sh`
- `scripts/nightly-bridge-refresh.sh` (encapsulado em Stage 2)
- `scripts/morning-briefing.sh` (encapsulado em Stage 3)
- `scripts/news-impact-analyzer.ts` (chamado em Stage 3)
- `scripts/watchdog-mcorch.sh` (continua `*/5 * * * *`, paralelo aos stages)
- `~/.openclaw/cron/jobs.json` (OpenClaw native `Memory Dreaming Promotion` 03:00)
- `.claude/context/survival-audit-v1.md` §2 Pillar 4 (Observability gap que motiva infra_health_logs writes)
- SSP-01 OE03 diretiva Sovereign (2026-05-17)

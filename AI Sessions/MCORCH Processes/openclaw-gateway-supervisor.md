# SOP — OpenClaw Gateway Supervisor (Single-Owner Lifecycle) v1.0

**Versão:** v1 · **Selada:** 2026-05-29 · **Lei 2 (Processo Antecipado)** · Trigger: qualquer operação que reinicie / recarregue / diagnostique o OpenClaw Gateway (porta 18789), OU recarregar `openclaw.json` / `cron/jobs.json` (não fazem hot-reload).

> **Esta SOP CORRIGE e SUPERSEDE a lição operacional selada em v6.8.1 (HANDOFF.md:817-859) que mandava usar `pm2 restart maestro`.** Aquela conclusão estava certa para o setup de 2026-05-21, mas o upgrade do OpenClaw para v2026.5.14 migrou o supervisor para systemd. Ver §Histórico.

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (eu) ou engineer agent; manual fallback é Sovereign via shell direto.
- **Reviewer:** Sovereign (Gabriel Zarattini) — confirma painel `claw.gcrux.com` responsivo + Telegram bot `@MCORCH_Clawbot` reconectado após reload.
- **Owner:** Sovereign — blast radius = disponibilidade do Gateway (cron circadiano, briefing Telegram, Control UI, agentes Pantheon) + custo de CPU desperdiçado por crash-loop.

## Contexto — O supervisor canônico é o systemd, NÃO o PM2

O OpenClaw Gateway (porta **18789**, `bind: loopback`) é gerenciado por **UM único supervisor canônico**:

```
systemd user service: openclaw-gateway.service
  Arquivo:   ~/.config/systemd/user/openclaw-gateway.service
  ExecStart: /home/ubuntu/.nvm/versions/node/v22.22.3/bin/node \
             /home/ubuntu/openclaw/dist/index.js gateway --port 18789
  Restart:   always (RestartSec=5)
  Estado:    enabled + active
```

**Por que `dist/index.js` direto e NÃO `openclaw.mjs`:** o wrapper `openclaw.mjs` tenta `import('./dist/warning-filter.js')` e `import('./dist/entry.js')` — nomes canônicos sem hash. O bundler do build (`scripts/build-all.mjs` via Bun) emite artefatos **hasheados** (`warning-filter-BGICq60U.js`, etc.), então o wrapper **quebra** com `Cannot find module './dist/warning-filter.js'`. O systemd contorna isso invocando `dist/index.js` diretamente, que é o entry-point real (`package.json` → `"main": "dist/index.js"`).

### ⛔ Anti-pattern proibido — DOIS supervisores na mesma porta

Historicamente existiu também um app **PM2 `maestro`** rodando `bash -c "bun run openclaw.mjs gateway"`. Como o wrapper quebra, o maestro entra em **crash-loop infinito** (a cada `RestartSec`) tentando bindar a 18789 que o systemd já possui → `EADDRINUSE` → contador de restarts explode (chegou a **3.5 milhões**). Custo: CPU desperdiçada + confusão de "qual processo é o gateway".

**Regra de ferro:** o Gateway tem **exatamente um** supervisor. Hoje = systemd. PM2 `maestro` foi **deletado** em 2026-05-29 (`pm2 delete maestro && pm2 save --force`). NUNCA recriar.

## Pre-conditions

- `systemctl --user status openclaw-gateway.service` retorna `enabled` + `active`.
- `pm2 list` NÃO contém `maestro` (e `~/.pm2/dump.pm2` está vazio — não ressuscita no reboot).
- Node target real do `ExecStart` existe: `/home/ubuntu/.nvm/versions/node/v22.22.3/bin/node`.
- Token do gateway lido de `openclaw.json` → `gateway.auth.token`.

## Sequence A — Recarregar config (`openclaw.json` / `cron/jobs.json`)

`openclaw.json` e `cron/jobs.json` são lidos **apenas no boot do gateway** — não há hot-reload. Após editar:

| # | Action | Output esperado | Verification gate |
|---|--------|-----------------|-------------------|
| 1 | Validar JSON: `python3 -c "import json; json.load(open('/home/ubuntu/.openclaw/openclaw.json'))"` | `(sem erro)` | Exit 0. JSON quebrado = gateway não sobe |
| 2 | Backup: `cp <arquivo> <arquivo>.bak-$(date +%s)` | arquivo .bak criado | `ls -la` mostra o backup |
| 3 | **Reload canônico:** `systemctl --user restart openclaw-gateway.service` | retorna em ~1s | comando sai com 0 |
| 4 | Aguardar ready: `sleep 8` | — | — |
| 5 | Health: `curl -s -o /dev/null -w "%{http_code}" -H "Authorization: Bearer <token>" http://127.0.0.1:18789/healthz` | `200` | HTTP 200 |
| 6 | Single-owner: ver §Sequence C (no-orphan check) | 1 node pid, ppid=systemd | exatamente 1 |
| 7 | Config aplicada: `node /home/ubuntu/openclaw/openclaw.mjs models list \| head` (CLI usa wrapper p/ subcomandos — OK, não é o gateway) | tag `default` no modelo esperado | bate com a edição |

> **`systemctl --user restart` é limpo e NÃO desgarra órfão** — validado material em 2026-05-29 (1.0s, MainPID trocou, 1 listener, ppid=1264 systemd). É o substituto seguro do antigo `pm2 restart maestro`.

## Sequence B — Aplicar config via kill (quando systemctl não disponível no shell)

Como `Restart=always`, matar o pid faz o systemd respawnar com a config nova:

| # | Action | Verification gate |
|---|--------|-------------------|
| 1 | `MAIN=$(systemctl --user show openclaw-gateway.service -p MainPID --value)` | pid numérico |
| 2 | `kill $MAIN` | — |
| 3 | `sleep 8` então health (Seq A passo 5) | HTTP 200 com pid NOVO |
| 4 | No-orphan check (§Sequence C) | 1 node pid systemd-owned |

## Sequence C — No-orphan / single-owner check (sempre rodar pós-reload)

O grande risco histórico: um segundo processo segurando a 18789. Verificação determinística:

```bash
# 1. Exatamente 1 listener na 18789, e é o MainPID do systemd:
ss -tlnp 2>/dev/null | grep 18789 | grep -oE "pid=[0-9]+" | sort -u
systemctl --user show openclaw-gateway.service -p MainPID --value

# 2. Todo processo NODE rodando o gateway tem ppid=1264 (systemd --user):
#    (filtrar comm=node evita self-match do próprio bash -c que contém a string)
for p in $(pgrep -f "node.*dist/index.js gateway"); do
  [ "$(ps -o comm= -p $p)" = "node" ] && echo "pid=$p ppid=$(ps -o ppid= -p $p | tr -d ' ')"
done
# Esperado: 1 linha, ppid=1264. Qualquer ppid≠1264 = ÓRFÃO → kill.
```

**Gate de sucesso:** count de node-gateway == 1, ppid == 1264, listener == MainPID.

## Recovery path — Gateway down ou crash-loop

| Sintoma | Causa provável | Fix |
|---------|----------------|-----|
| `healthz` != 200, porta livre | service parado | `systemctl --user start openclaw-gateway.service` |
| `EADDRINUSE` no log + restarts subindo | segundo supervisor (PM2 maestro ressuscitado) ou órfão | `pm2 delete maestro; pm2 save --force` + `kill <órfão não-systemd>` (§C) |
| `Cannot find module './dist/warning-filter.js'` | alguém rodando o wrapper `openclaw.mjs` como serviço (errado) | Não use o wrapper como serviço. ExecStart deve ser `dist/index.js`. Defensivo: `ln -sf warning-filter-*.js dist/warning-filter.js` |
| service falha após upgrade Node/NVM | `ExecStart` aponta p/ binário Node removido | atualizar path no `.service` → `daemon-reload` → `restart` |
| `agentId is not allowed for sessions_spawn` | `allowAgents` restritivo | editar `agents.defaults.subagents.allowAgents` em `openclaw.json` + Seq A |

**Nunca usar `openclaw gateway restart`** — em 2026-05-21 esse comando desgarrou um processo órfão (PPID 1) que roubou a 18789, criando o crash-loop original. Use `systemctl --user restart` (Seq A) ou kill+respawn (Seq B).

## Success signal

- `curl .../healthz` → **HTTP 200**
- `ss ... 18789` → **exatamente 1** listener, == systemd MainPID, ppid 1264
- `pm2 list` → **sem `maestro`**
- Telegram bot reconecta (log `[telegram] starting provider (@MCORCH_Clawbot)`)
- Cron `jobs-state.json` → próxima execução agendada, `lastRunStatus` sem `skipped/error` por config

## Histórico — por que a lição mudou

| Data | Estado | Lição vigente |
|------|--------|---------------|
| 2026-05-21 | OpenClaw pré-v2026.5.14; systemd `disabled/failed`; PM2 maestro era o supervisor de fato | "use `pm2 restart maestro`" (correta à época) — selada em memory + HANDOFF v6.8.1 |
| ~2026-05-22..28 | Upgrade p/ v2026.5.14 **re-habilitou** `openclaw-gateway.service`; passaram a existir 2 supervisores brigando | (não detectado — maestro crash-loopou de 716 → 3.5M restarts) |
| 2026-05-29 | PM2 maestro **deletado**; systemd é supervisor único | **"use `systemctl --user restart openclaw-gateway.service`"** (esta SOP) |

## Findings adjacentes registrados (não-bloqueantes desta SOP)

- **OTD-OCGW-001** — OpenClaw `memory-core` falha embeddings com `403 text-embedding-3-small project access revoked` (OpenAI key do OpenClaw, não a do mcorch que usa OpenRouter). `memory_search` degradado nas execuções de cron. SLA: próxima sessão OpenClaw dedicada.
- **OTD-OCGW-002** — build artifacts duplicados/hasheados em `dist/` (`task-registry.maintenance` 2 hashes, `status.summary` 2 hashes) sugerem build incremental sujo. Rebuild limpo (`bun run build` em `~/openclaw`) recomendado quando houver upgrade.

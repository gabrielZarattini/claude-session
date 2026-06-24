# SOP — OpenClaw Bridge Recovery v1.0

**Versão:** v1 · **Selada:** 2026-05-19 · **Lei 2 (Processo Antecipado)** · Trigger: incident em Stage 2 (`nightly-bridge-refresh` falhando Step 3)

## ORO triplet

- **Operator:** engineer agent (Layer 2 escalation do watchdog); fallback manual é Sovereign via shell direto
- **Reviewer:** Sovereign (revisa via `claw.gcrux.com/dreaming` — Imported Insights / Memory Palace / Diário devem mostrar entradas frescas após reindex)
- **Owner:** engineer agent (infra ownership) — risco material: AIOS dreaming silently vazio quebra confiança no Memory Palace + briefing matinal Telegram

## Contexto

`scripts/nightly-bridge-refresh.sh` encapsulado em **Stage 2 (`0 5 * * *` BRT)** roda 3 sub-steps:

1. `bridge-mesh-to-openclaw.ts` — export `mcorch_nodes` + `mcorch_edges` → `memory/mcorch-export/` (tier1 strategy + tier2 AST)
2. `distribute-mesh-to-agents.ts` — copy shared + per-agent overlays para `~/.openclaw/agents/<id>/memory/`
3. `"$NODE_BIN" "$OPENCLAW_CLI" memory index --agent="$agent"` × 7 — reconstrói SQLite FTS5 + vector indexes em `~/.openclaw/memory/<agent>.sqlite` (agents: main · artisan · engineer · scientist · marketing-growth · guardian · claw-master — este último adicionado em 2026-05-19 após descoberta de omissão latente desde v6.3.1)

Step 3 é o que alimenta os endpoints `doctor.memory.dreamDiary`, `wiki.importInsights`, e `wiki.palace` consumidos pela UI `claw.gcrux.com/dreaming`. Sem Step 3 successful, a UI lê do índice antigo — Imported Insights, Memory Palace e dream promotion ficam congelados no último reindex bem-sucedido.

**Causa-raiz recorrente conhecida:** OpenClaw CLI exige Node.js v22.12+, mas o cron environment de `ubuntu` historicamente usa `/usr/bin/node` (Ubuntu APT) que é v18.19.1. Sem path absoluto explícito para o binário Node 22, Step 3 falha silenciosamente em loop.

## Pre-conditions

- Stage 2 cron em `crontab -l` (`0 5 * * * .../scripts/nightly-stage2-deep-sleep.sh`).
- `/var/log/mcorch-nightly-bridge.log` existente e escrevível pelo user `ubuntu`.
- `/home/ubuntu/.nvm/versions/node/v22.22.3/bin/node` resolvível (target real do symlink `/home/ubuntu/.local/bin/node`).
- `mcorch_chroma` healthy + `mcorch_claude_mem` healthy (`docker ps`).
- `~/.openclaw/cron/jobs.json` tem `Memory Dreaming Promotion` agendado (`0 3 * * *`) — fora deste SOP, mas é downstream e fica vazio se Step 3 não roda.

## Sequence — recovery manual humana

| # | Action | Output esperado | Verification gate |
|---|--------|-----------------|-------------------|
| 1 | `tail -50 /var/log/mcorch-nightly-bridge.log \| grep -E "Step 3/3\|FAIL indexing\|DONE"` | Linhas mostrando "Step 3/3" + se há "FAIL indexing" ou apenas "DONE (zero failures)" | Se há FAIL indexing → root cause confirmado, segue passo 2. Se DONE → bridge OK, problema é upstream (mesh sem input novo) |
| 2 | `grep -n "node " /home/gcrUX/htdocs/constellation-orchestra/scripts/nightly-bridge-refresh.sh \| grep -v "node_modules\|#"` | Linha do invoke do CLI (`node "$OPENCLAW_CLI" memory index ...`) | Confirma que invoke usa `node` direto OU `$NODE_BIN`; se direto, pin é necessário |
| 3 | `which node && ls -la $(which node) && node --version` no shell do user dono do cron (atualmente `ubuntu`) | Path absoluto + symlink target + versão v22.12+ | Se v18.x.x → problema confirmado de PATH no cron env |
| 4 | Editar `scripts/nightly-bridge-refresh.sh` — declarar `NODE_BIN=<resolved nvm target>` no bloco de paths (perto da linha 13) e substituir `node "$OPENCLAW_CLI"` por `"$NODE_BIN" "$OPENCLAW_CLI"` no loop de agents | 2 hunks no diff | `git diff` mostra exatamente essas duas mudanças, nada mais |
| 5 | `bash /home/gcrUX/htdocs/constellation-orchestra/scripts/nightly-bridge-refresh.sh` | Log apêndice com Steps 1, 2, 3 sequenciais + `DONE (zero failures)` | `tail -1 /var/log/mcorch-nightly-bridge.log` mostra DONE final |
| 6 | `ls -la /home/ubuntu/.openclaw/memory/*.sqlite` | 6 arquivos SQLite com mtime nos últimos minutos | Diff de mtime com `date` < 5min |
| 7 | Sovereign reload `claw.gcrux.com/dreaming` | Imported Insights aceita reload sem erro; Memory Palace counts conferem com vault state | UI mostra cluster > 1 OU confirma materialmente que mesh upstream realmente não tem input novo (não é falha de bridge) |

## Verification gates

- **Gate Step 3 OK:** `/var/log/mcorch-nightly-bridge.log` última execução tem `DONE (zero failures)` E nenhuma linha `openclaw: Node.js v22.12+ is required`.
- **Gate SQLite reindex:** mtime de **todos** os arquivos `.sqlite` em `~/.openclaw/memory/` ≤ 5 min após `bash` manual.
- **Gate downstream Dream Promotion:** após cron Memory Dreaming Promotion (03:00 BRT) seguinte, `~/.openclaw/agents/claw-master/memory/dreaming/{light,deep,rem}/<YYYY-MM-DD>.md` não devem mais ser "No notable updates" caso haja material novo no mesh.
- **Gate UI viva:** Sovereign confirma na UI Imported Insights/Memory Palace que counts mudaram (ou confirmam estabilidade legítima do mesh).

## Recovery path

- **Cenário A — bridge ainda falha em Step 3 após pin:** verificar `/home/ubuntu/.nvm/versions/node/v22.22.3/bin/node --version` retorna v22.22.3. Se symlink quebrou ou versão drift, atualizar `NODE_BIN` para target atual. NÃO usar `which node` no script — sempre path absoluto resolvido.
- **Cenário B — indexing parcial (FAIL em 1-2 agents):** rodar manualmente apenas os agents que falharam: `"$NODE_BIN" /home/ubuntu/openclaw/openclaw.mjs memory index --agent=<id>` para cada. Investigar SOUL.md / openclaw.json do agent específico para corrupção.
- **Cenário C — Steps 1+2 OK + Step 3 OK + UI ainda stale:** problema é upstream (mesh sem input) ou cache. Validar: `psql ... 'SELECT count(*) FROM mcorch_nodes WHERE created_at > now() - interval ''3 days'''` — se zero, mesh upstream parou de inserir. Investigar embedding pipeline + cron `ingest-codebase` (`0 6 * * *` que **também** usa `node` sem path absoluto — risco gêmeo deste SOP).
- **Cenário D — Step 3 falha por OOM ou disk:** `docker stats` + `df -h /home/ubuntu`. SQLite VACUUM por agente (manual) se índice corrompido. Reindex completo deleta `~/.openclaw/memory/<agent>.sqlite` antes de re-rodar.

## Success signal

- `/var/log/mcorch-nightly-bridge.log` última linha = `[<ISO>] nightly-bridge-refresh DONE (zero failures)`.
- Todos os 6 SQLites de agent indexados com mtime fresco.
- `claw.gcrux.com/dreaming` Imported Insights mostra cluster com data > checkpoint anterior (ex.: > 2026-05-16 quando o problema foi detectado).
- Cron seguinte (próximo 05:00 BRT) também passa zero failures — idempotência confirmada.

## Anti-patterns

- ❌ Usar `node` sem path absoluto em qualquer cron script que dependa de Node v22+.
- ❌ "Resolver" pin com `source ~/.nvm/nvm.sh && nvm use 22` no script — funciona para o user dono do nvm install, mas cria fragilidade implícita; pin direto no binário resolvido é mais materialmente verificável.
- ❌ Bypassar Step 3 (commentar o loop) como "fix" — bridge sem indexação = sem dreams + sem Memory Palace; é a fonte do AIOS.
- ❌ Desabilitar Stage 2 inteiro porque "está falhando" — Stage 2 também faz drift watch + VACUUM; remover é perder defesas.
- ❌ Auto-upgrade do `NODE_BIN` por script (`readlink -f $(which node)`) — quebra Lei 1; pin é DECISÃO HUMANA com prova material.

## Referências

- `scripts/nightly-bridge-refresh.sh` — script alvo do pin (linha 65 invoke do CLI)
- `scripts/nightly-stage2-deep-sleep.sh` — wrapper que invoca o bridge (linha 81)
- `/home/ubuntu/openclaw/openclaw.mjs` — CLI OpenClaw que exige Node v22.12+
- `/home/ubuntu/.openclaw/memory/*.sqlite` — alvo de reindex (FTS5 + vector)
- `/home/ubuntu/openclaw/extensions/memory-wiki/src/gateway.ts:136-160` — gateway `wiki.importInsights` + `wiki.palace`
- `/home/ubuntu/openclaw/ui/src/ui/views/dreaming.ts` — UI consumer
- `~/.openclaw/cron/jobs.json` — Memory Dreaming Promotion downstream (03:00 BRT, OpenClaw native)
- SOP irmão `nightly-circadian-cycle.md` (Stage 2 ownership)
- SOP irmão `mcoins-ledger-reconciliation.md` (Stage 2 drift watch)

## Risco adjacente conhecido (registrar OTD se materializar)

`crontab -l` atual também tem `0 6 * * * node scripts/ingest-codebase.ts --quiet >> /tmp/mcorch-ingest.log 2>&1` — mesmo padrão de `node` sem path absoluto. Se Sovereign confirmar que ingest-codebase também está silenciosamente falhando há ≥ 3 dias (via tail `/tmp/mcorch-ingest.log`), aplicar mesmo fix neste cron (pin via `/home/ubuntu/.nvm/versions/node/v22.22.3/bin/node`). NÃO incluso neste SOP — escopo aqui é apenas bridge recovery.

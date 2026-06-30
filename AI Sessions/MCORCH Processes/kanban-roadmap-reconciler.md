# SOP — Kanban Roadmap Reconciler (board vivo, não-destrutivo)

> **Lei 2 (Processo Antecipado).** Automação que mantém o board Kanban "🎭 Gabriel AI — Programa"
> sincronizado com a realidade do sistema **sem apagar os cards manuais do Sovereign**.
> Anti-corpo do incidente: o board virava snapshot mockado e mostrava `RUNNING` falso (2026-06-30).

## Operator
Quem executa hoje (manualmente): o agente MCORCH roda `bun run scripts/reconcile-kanban-roadmap.ts`
sempre que conclui uma fatia. **Automatizado por:** cron `*/15 * * * *` (crontab `gcrUX`).

## Princípio de segurança (UNBREAKABLE)
- **Proveniência:** `aios_kanban_tasks.source`. `NULL` = card **manual** (criado/arrastado pelo user) →
  o reconciliador **nunca** o atualiza nem deleta. `'roadmap-reconciler'` = card **gerenciado**.
- **Chave estável:** `external_key` (ex. `fatia-1`) → upsert por chave, **rename-safe** (não por título).
- **Status derivado da realidade**, não hardcode: cards signal-driven (`fatia-1`, `bok-seal`) calculam o
  status de sinais ao vivo (coluna `user_api_keys.hedra_api_key` existe? nó de selo na malha existe?).
- **Adoção one-time:** no 1º run, cards legados `source IS NULL` com o MESMO título de um card gerenciado
  são **adotados** (recebem `source`/`external_key`) — zero duplicata.
- **Sem delete+recreate do board.** Nunca apaga coluna nem o board.

## Sequence (cada run, idempotente)
1. Lê sinais reais: `fatia1DbLive` (coluna BYOK existe) · `bokSealed` (nó de selo existe).
2. Garante board + 4 colunas (cria se faltar; nunca deleta).
3. Carrega tasks existentes; separa **gerenciadas** (`source='roadmap-reconciler'`) das **manuais** (`source IS NULL`).
4. Para cada card gerenciado do conjunto: upsert por `external_key` (ou adota legado por título); UPDATE só se algo mudou.
5. Cleanup: deleta **apenas** cards gerenciados cuja `external_key` saiu do roadmap (jamais manuais).
6. Cards manuais ficam intocados.

## Verification gates
- **G1 (não-destrutivo):** após um run, todo card com `source IS NULL` continua presente e na mesma coluna.
  Prova: `SELECT count(*) FROM aios_kanban_tasks WHERE source IS NULL AND <board>` antes == depois.
- **G2 (sem duplicata):** `SELECT external_key, count(*) FROM aios_kanban_tasks WHERE source='roadmap-reconciler' GROUP BY external_key HAVING count(*)>1` → **0 linhas**.
- **G3 (signal-derived):** o card `fatia-1` está em "Concluído" **sse** `user_api_keys.hedra_api_key` existe.
- **G4 (output):** o script imprime `signals:` + `adopted/created/updated/unchanged/deleted` e
  `manual cards ... were NOT touched`.

## Recovery path
- **Run falhou (rede/credencial):** o cron loga em `~/.mcorch/logs/kanban-reconcile.log`. Re-rodar é seguro (idempotente).
- **Duplicata apareceu (bug):** rodar a query G2; deletar a duplicata gerenciada mais nova por `id`. Nunca delete `source IS NULL`.
- **Reconciliador apagou algo errado:** desativar o cron (`crontab -e`, comentar a linha), investigar; o `source` guard impede tocar manuais por design.
- **Sinal mudou e o card não atualizou:** rodar o script à mão; checar o nome da coluna/sinal.

## Success signal
Board reflete a realidade ≤15 min após uma mudança de sinal (ex.: aplicar a migration da Fatia 2 →
o card sobe pra Concluído sozinho), **e** todo card que o Sovereign arrastou/criou continua exatamente onde ele deixou.

## Infra
- Script: `scripts/reconcile-kanban-roadmap.ts` (bun; `.env` auto-load → `SB_SECRET_KEY`).
- Migration: `20260630010000_kanban_task_source_external_key.sql` (`source` + `external_key` + index parcial).
- Cron: `*/15 * * * * cd <repo> && /usr/bin/env bun run scripts/reconcile-kanban-roadmap.ts >> ~/.mcorch/logs/kanban-reconcile.log 2>&1` (crontab `gcrUX`).
- Single-tenant Usuário Zero (`USER_ID` fixo). Multi-tenant = evolução futura (iterar sobre boards por user).

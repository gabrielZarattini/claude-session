# SOP — Gate de entrega da auditoria 4Cs (Lei 1 · Lei 3)

> **Status:** ativo desde 2026-07-29 · **Gate mecânico:** o próprio `scripts/audit-4cs.sh` (bloco de entrega + verificação)
> **Irmão:** [`handoff-pruning-gate.md`](handoff-pruning-gate.md) — mesma classe de falha, superfície diferente

---

## O obstáculo que gerou este SOP

Em **2026-07-29** descobriu-se que a rotina de auditoria 4Cs **nunca esteve quebrada**: ela rodava,
diagnosticava corretamente — inclusive **diagnosticava a própria falha** — e o resultado não chegava
a lugar nenhum. Duas metades independentes do mesmo defeito:

| Mecanismo | Rodava? | Por que não chegava |
|---|---|---|
| **Rotina remota** (auditoria pontuada) | sim | commitava numa branch de sessão (`claude/adoring-mendel-*`) que ninguém mergeava. **6 auditorias órfãs** recuperadas no PR #11 |
| **Cron do host** (`audit-4cs.sh`, snapshot objetivo) | **não** | o redirect `>> /var/log/mcorch-audit.log` falhava (arquivo de `gcrUX` modo 644, cron roda como `ubuntu`) → o comando nunca executava. E, quando executado à mão, fazia `git commit` **dentro do checkout de produção** e **sem `git push`** → o commit nascia na branch que o repo de produção tivesse no HEAD e morria ali |

Prova material da segunda metade: `git log --all --grep="4Cs weekly snapshot"` devolvia **1 único
commit** (`1107cf4`, 2026-05-04) — para ~12 execuções semanais esperadas entre maio e julho.

**A lição, que é a doutrina deste SOP:** *rodar não é entregar.* Uma rotina de diagnóstico que não
publica o diagnóstico é indistinguível de uma rotina morta — e é pior, porque consome recurso e
gera a ilusão de cobertura. **A entrega é parte da rotina, não um pós-passo opcional.**

---

## Operator — quem executa

- **Automático:** cron do host `0 12 * * 1` (segunda 09:00 BRT = 12:00 UTC) → `scripts/audit-4cs.sh`.
- **Rotina remota (pontuada):** o agente que roda a skill `/audit` em ambiente remoto.
- **Manual:** qualquer agente rodando `bash scripts/audit-4cs.sh`.

---

## Sequence — em que ordem

| # | Passo | Critério de sucesso material |
|---|-------|------------------------------|
| 1 | Coletar métricas objetivas do host (`COMPOSE_DIR` = repo de produção) | valores preenchidos; o que não pôde ser medido vira `n/a`, **nunca `0`** |
| 2 | Preparar o **worktree de entrega** (`/home/ubuntu/.mcorch/audit-delivery`, DETACHED em `origin/main`) | `git -C <wt> rev-parse HEAD` == `origin/main` |
| 3 | Append da entrada no `audit-log.md` **do worktree** (nunca no checkout de produção) | entrada `## <DATA>` presente no arquivo do worktree |
| 4 | `commit --no-verify` + `push origin HEAD:main` | push aceito |
| 5 | **Se rejeitado:** `fetch` + `rebase origin/main` + push de novo | push aceito na 2ª tentativa |
| 6 | **GATE DE ENTREGA:** `git show origin/main:.claude/context/audit-log.md \| grep "^## <DATA>"` | ≥ 1 ocorrência |
| 7 | Falha em qualquer passo → linha em `infra_health_logs` (`service='audit-4cs'`, `event='delivery_failed'`) | linha visível na tabela |

### Por que um worktree detached, e não o checkout de produção

O repo de produção (`/home/gcrUX/htdocs/constellation-orchestra`) é um **ambiente vivo**: o nginx
serve o `dist/` dele e o HEAD dele pode estar em qualquer branch de trabalho. Commitar ali acopla a
entrega ao estado acidental do checkout — foi exatamente o que enterrou a série histórica. O
worktree detached preso a `origin/main` torna a entrega **independente** do que produção esteja
fazendo, e o push é sempre para o alvo certo.

---

## Verification gates

| Gate | Comando | Esperado |
|------|---------|----------|
| **G1 — a rotina roda** | `tail -3 /home/ubuntu/logs/mcorch-audit.log` | linha `Audit snapshot ENTREGUE em origin/main (<sha>)` |
| **G2 — chegou na main** | `git fetch origin main && git show origin/main:.claude/context/audit-log.md \| grep -c "^## $(date +%F)"` | `≥ 1` |
| **G3 — série sem buraco** | `grep -cE "^## (Audit — )?20[0-9]{2}-" .claude/context/audit-log.md` | cresce 1 por semana (2 formatos de cabeçalho vivos: `## <data>` do cron e `## Audit — <data>` da rotina pontuada) |
| **G4 — log gravável** | `ls -la /home/ubuntu/logs/mcorch-audit.log` | dono `ubuntu`, tamanho crescendo |

**G4 é o gate que não existia.** Todo cron do host que redireciona saída **deve** escrever num
diretório do próprio usuário do cron (`/home/ubuntu/logs/`), **nunca** em `/var/log/` — o
`logrotate` de `/etc/logrotate.d/mcorch-host-workers` recria `/var/log/mcorch-*.log` como
`create 0644 gcrUX gcrUX`, e o cron roda como `ubuntu`: o redirect falha e **o comando não executa**.
Em 2026-07-27 02:55 UTC isso matou em silêncio o `watchdog-mcorch.sh`, o `canvas-video-watchdog.sh`
e o `affiliate-enrich-cron.sh` além do audit (telemetria de `mcorch_chroma`/`mcorch_claude_mem`
parou por ~3 dias). Scripts agora usam `${MCORCH_LOG_DIR:-/home/ubuntu/logs}`.

---

## Recovery path — falha no passo N

| Falha | Recuperação exata |
|-------|-------------------|
| Passo 2 (worktree não cria) | `git -C <repo> worktree prune && git -C <repo> worktree add --detach /home/ubuntu/.mcorch/audit-delivery origin/main` |
| Passo 4/5 (push rejeitado 2×) | rodar à mão: `cd /home/ubuntu/.mcorch/audit-delivery && git fetch origin main && git rebase origin/main && git push origin HEAD:main` |
| Passo 6 (gate falha após push) | conferir se o push foi para outro ref: `git -C <wt> log -1 --format=%H` vs `git ls-remote origin main`; nunca declarar entregue sem o `grep` verde |
| Snapshot de semana perdida | rodar `bash scripts/audit-4cs.sh` à mão; a data será a de hoje — registrar no corpo da entrada que ela cobre a semana anterior (data errada corrompe a série que o log existe para medir) |
| Entrada órfã em branch de sessão | `git show <branch>:.claude/context/audit-log.md` → recuperar o bloco → append na main preservando a **data original** da execução |

---

## Success signal

`git show origin/main:.claude/context/audit-log.md | grep -c "^## 20"` **aumenta em 1 por semana**,
sem buraco, e cada entrada carrega a data real de execução. Nenhuma auditoria vive só em branch.

---

## Conexão com as Leis

- **Lei 1 (Materialidade):** "auditoria rodou" só é verdade se o resultado está em `origin/main`.
  Commit local, branch de sessão ou log em `/var/log` ilegível **não são entrega**. O passo 6 é a prova.
- **Lei 3 (Pruning):** a série histórica é o instrumento que mede a saúde ao longo do tempo — perdê-la
  é perder a capacidade de detectar deriva. Ver o irmão [`handoff-pruning-gate.md`](handoff-pruning-gate.md).
- **CLAUDE.md §5 (Obstacle → Synthesis):** *se o mesmo erro pode reincidir, ele ainda não foi resolvido
  — só adiado.* O bloco de entrega + o gate G4 são o anticorpo.

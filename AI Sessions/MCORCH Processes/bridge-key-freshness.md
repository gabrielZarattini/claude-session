# SOP — Frescor de chave nas pontes: o worker VERDE que segura a chave MORTA (Lei 1 · Lei 2)

**Status:** ACTIVE · v1.0 · 2026-08-11
**Anticorpo:** `scripts/qa/self-heal-bridge-keys.sh` (cron `*/5`)
**Irmãos:** `scripts/qa/rotate-supabase-secret.sh` (a rotação) · `scripts/qa/sync-edge-secret.sh` (o vault)
**Memórias:** `reference_supabase_secret_key_rotation_silent_kill` · `reference_hyperframes_worker_restart`

## O incidente que este SOP existe para nunca mais permitir

**2026-08-08 17:18 → 2026-08-10 23:00 (53h40m).** A secret key do Supabase foi revogada e derrubou **em
silêncio** as pontes de render, as Edge Functions e todo script CLI. Durante as 53 horas:

- `systemctl --user status` reportou **`active (running)` para todas as pontes**. Elas estavam vivas — só
  o crédito na mão delas é que tinha morrido.
- O cron do host acumulou **634 ticks HTTP 401 `Unregistered API key`** sem **um único alarme**.
- O app seguiu de pé (usa a publishable), então nenhum sintoma visível chegou ao Sovereign.

**2026-08-11 — a reincidência, encontrada por auditoria.** A rotação reiniciou 8 pontes às 22:08, mas
**`youtube-upload` rodava desde 06/08 15:35** e atravessou a revogação segurando a chave morta. Estava
`active (running)` havia 5 dias. Ninguém teria notado até alguém tentar subir um vídeo.

**Terceira ocorrência da mesma família:** a cláusula de gate stale (`provenance-bridge`, `subtitle-bridge`,
motion MONTAR) que declarava um serviço "NÃO habilitado" meses depois de ele estar no ar.

## A regra

> **`active (running)` NÃO é prova de saúde.**
> Um worker lê o `.env` **uma vez**, no start. Depois disso ele carrega uma cópia em memória que nenhuma
> mudança de arquivo alcança. A prova de saúde é dupla:
> **(a)** o processo iniciou **depois** da última modificação do `.env` — `ExecMainStartTimestamp`, nunca
> "acho que reiniciei"; e **(b)** a chave desse `.env` autentica **agora** — um `curl` de verdade.

## Operator

Hoje, sem o anticorpo: um humano teria de lembrar de comparar, ponte por ponte, o timestamp de start com o
mtime do `.env` — depois de toda rotação, todo deploy e toda edição do `.env`. Ninguém lembra. Foi por isso
que falhou duas vezes.

Com o anticorpo: o cron `*/5` faz isso e **cura sozinho** o que é curável.

## Sequence

| # | Passo | Critério de sucesso material |
|---|-------|------------------------------|
| 1 | **Gate da chave** — `curl REST /profiles?limit=1` com a `SB_SECRET_KEY` do `.env` | HTTP **200**. Qualquer outro código ⇒ pare no passo 1 |
| 2 | **Gate do frescor** — para cada ponte, `systemctl --user show <b> -p ExecMainStartTimestamp` × `stat -c %Y .env` | `start_epoch >= env_epoch` ⇒ fresca |
| 3 | **Cura** — reinicia SÓ as stale | o `ExecMainStartTimestamp` **mudou** E `ActiveState=active` |
| 4 | **Telemetria** — grava em `infra_health_logs` (`service='bridge-key-guard'`) | linha nova com `event` ∈ `all_fresh` \| `stale_bridges_healed` \| `secret_key_dead` |

## Verification gates

- **G1 — a chave morta NÃO é auto-curável.** Se o passo 1 falhar, o script **recusa reiniciar qualquer
  coisa** e sai com código 2. Reiniciar ali trocaria um worker com chave morta por outro worker com a
  **mesma** chave morta, e ainda mataria o job em voo. Só o Sovereign gera chave nova.
- **G2 — o restart é provado, não presumido.** Comparar `ExecMainStartTimestamp` antes × depois. Um
  `systemctl restart` que retorna 0 **não prova** que o processo trocou — é o falso-sucesso que o gate da
  rotação já tinha aprendido a recusar (`ac7e29c`: *"o gate do restart mediu janela de tempo e acusou
  ponte limpa"*).
- **G3 — convergência.** Rodar duas vezes seguidas: a segunda tem de dar `all_fresh`. Se continuar
  acusando stale, o restart não está pegando (unit com `Environment` fixo? bun fora do PATH?).
- **G4 — o log tem de ser gravável.** Cron com redirect para arquivo não-gravável **não executa o comando**
  (memória `reference_cron_log_permission_trap`). Logs vivem em `/home/ubuntu/logs/`.

## Recovery path

| Sintoma | Diagnóstico | Conserto |
|---|---|---|
| `secret_key_dead` (exit 2) | a chave do `.env` foi revogada | Sovereign gera nova → `bash scripts/qa/rotate-supabase-secret.sh` → depois `bash scripts/qa/sync-edge-secret.sh` para o **vault** (que NÃO lê o `.env`) |
| ponte acusada stale toda rodada | o restart não troca o processo | `systemctl --user cat <b>` — unit com `env bun` dá exit 127 sob systemd; use o caminho cheio `/home/ubuntu/.bun/bin/bun` + `Environment=PATH=...` |
| ponte sem unidade systemd | worker novo não versionado | criar a unit em `scripts/systemd/` e adicionar o nome ao array `BRIDGES` do script |
| tudo verde mas job não anda | não é chave — é fila ou código stale | `journalctl --user -u <b> --since -1h`; compare `ExecMainStartTimestamp` com o **mtime do .ts** (memória `reference_hyperframes_worker_restart`) |

## Success signal

`bash scripts/qa/self-heal-bridge-keys.sh` sai **0** com `✅ N ponte(s) com env fresco`, e
`infra_health_logs` recebe `service='bridge-key-guard'` `event='all_fresh'` a cada 5 minutos. Qualquer
janela de silêncio maior que ~10 minutos nessa série É o alarme — a ausência do batimento é o sinal.

## A CHAVE VIVE EM TRÊS LUGARES (descoberto em 2026-08-11)

Esta é a lição mais cara da investigação, e a razão pela qual o incidente teve uma cauda de 3 dias que
ninguém viu: **rotacionar a chave em um lugar não rotaciona nos outros dois.**

| # | Onde | Quem lê | Como sincronizar | Sintoma quando fica para trás |
|---|------|---------|------------------|-------------------------------|
| 1 | `.env` do repo | as 9 pontes systemd · todo script CLI | `rotate-supabase-secret.sh` | worker `active (running)` sem pegar job |
| 2 | **Vault das Edge Functions** (Supabase) | as ~103 edge fns via `Deno.env.get` | `sync-edge-secret.sh` (precisa de PAT) | `get-infra-status` devolve 500 **com a chave certa no header** — o erro nasce DENTRO da função |
| 3 | **Vault do POSTGRES** — `vault.decrypted_secrets` name=`sb_secret_key` | os jobs do **`pg_cron`** via `pg_net` | `vault.update_secret(<id>, <chave>, 'sb_secret_key')` | jobs seguem `active=true`, disparam no horário, tomam **401**, e a edge function **nunca loga** |

O terceiro é o mais traiçoeiro: `cron.job.active = true` continua verdadeiro o tempo todo. Em
2026-08-08 20:15 `autopilot-cadence` e `nurture-advance` morreram assim e ficaram **55 horas** sem um
único alarme — só apareceram porque um crítico adversarial foi conferir a série do `infra_health_logs`.

**Regra:** `cron.job.active` NÃO é sinal de saúde. O sinal é a **série de batimentos** em
`infra_health_logs` — e o alarme é a **ausência** dela.

Onde os jobs leem o cofre (para achar de novo):
`supabase/migrations/20260623040000_viral_autopilot_cadence_cron.sql:34` ·
`supabase/migrations/20260603230000_nurture_advance_cron.sql:26`

## O que este SOP NÃO cobre (escopo honesto)

- **Código stale.** O guarda compara o start da ponte com o `.env`, não com o `.ts`. Um worker rodando
  código velho passa por aqui como saudável (memória `reference_hyperframes_worker_restart`).
- **O vault das Edge Functions não é auto-curável.** O guarda não o consulta (exige PAT). Quem fecha é o
  passo 5 do `rotate-supabase-secret.sh` + o `sync-edge-secret.sh`.
- **O Vault do Postgres é detectado, não curado.** O GATE 3 acusa o silêncio e nomeia a causa provável,
  mas não escreve no cofre sozinho — escrever segredo em produção fica com quem tem a chave na mão.
- **Outros crons do host.** O `auto-publish` acumulou 634 ticks 401 no mesmo incidente e continua sem
  sentinela própria: ele loga em arquivo, não em `infra_health_logs`.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

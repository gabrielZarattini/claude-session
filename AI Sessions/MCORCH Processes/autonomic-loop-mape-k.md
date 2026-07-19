# SOP — Loop Autonômico MAPE-K (Monitor · Analyze · Plan · Execute sobre Knowledge)

> Lei 2 (Processo Antecipado) — escrito ANTES do código. Plano aprovado: `~/.claude/plans/dinovo-agora-foi-para-snazzy-crescent.md`.
>
> **Nasceu de:** o `/loop` de sessão com pacing improvisado pelo LLM (ScheduleWakeup 270s→3300s ad-hoc), o falso
> alarme 21:07 (check inline leu objeto de erro PostgREST como "4 erros") e a fragilidade sessão-morta =
> vigilância-morta. Referência: IBM Autonomic Computing (MAPE-K) — **M+A mecânicos e perpétuos (cron);
> LLM só em P+E**; monitor quebrado é sintoma de primeira classe; todo estado em Knowledge auditável.

## ORO
- **Operator (humano):** Sovereign — instala/valida crontab, recebe Telegram, arma/desarma L2 (`--arm`/`--disarm`), abre a sessão /loop v3 (L3).
- **Operator (máquina):** cron `guardian-tick-cron.sh` (*/5) + `guardian-sweep-runner.sh` (6h via exit 10) + `watchdog-mcorch.sh` (monitor do monitor) + `ux-explorer-cron.sh` (nightly) — M+A. `guardian-remediate.sh` (L2) e sessão /loop v3 (L3) — P+E.
- **Reviewer:** Sovereign; `/security-review` na fatia L2 (LLM com shell).
- **Owner:** Sovereign (blast radius: alertas falsos/perdidos, tokens do L2).

## Componentes e contratos

| Componente | Papel MAPE-K | Contrato |
|------------|--------------|----------|
| `scripts/qa/guardian-tick.ts` | **M+A** (cérebro) | exit **0**=GREEN · **1**=RED · **10**=SWEEP_DUE. Flag `--cron` habilita efeitos (heartbeat, incidentes, Telegram); sem ela é read-only (uso interativo/charter). Subcomandos: `--record-sweep <verdict> [--fails N]` · `--list-incidents` · `--resolve <id> --note "<prova>"` · `--consume-remediation-budget` · `--arm` / `--disarm` |
| `scripts/guardian-tick-cron.sh` | **M** (driver) | flock `/tmp/mcorch-guardian-tick.lock` + `timeout 180` + env do `.env`; exit 10 → dispara runner destacado; exit∉{0,1,10} → row `tick_crash` (NÃO é heartbeat) |
| `scripts/qa/guardian-sweep-runner.sh` | **M** (bateria 6h) | flock próprio + `timeout 1800`; roda `guard-sweep.sh`; SEMPRE grava verdict via `--record-sweep ... --fails N` (mesmo RED — o RED persiste como incidente, não como re-disparo a cada 5min) |
| `scripts/watchdog-mcorch.sh` (extensão aditiva) | **auto-correção** | heartbeat `service='guardian' event='tick'` ausente/velho >900s → Telegram (stamp-file cooldown 6h) + `INC-guardian-heartbeat.json` fixo (dedup por nome) + row `heartbeat_missing` |
| `scripts/lib/notify-telegram.sh` | **E nível 1** | `notify-telegram.sh "<msg>"`; token `jq -r '.keys.telegramBotToken' ~/.openclaw/secrets.json`; chat default `5835174772`; truncagem 4000; token ausente → **exit 2** (nunca silencioso — Lei 1); exit = resultado material do POST |
| `scripts/guardian-remediate.sh` | **E nível 2 (toggle)** | gates encadeados (ordem endurecida pelo /security-review M3): `mode==auto-remediate` → classe ∈ {RED_FINDING, SWEEP_RED, UX_FINDING:P1} → **flock (G4) ANTES do budget (G2)** → budget diário. `claude -p` **Tier A diagnose-only** com allowlist **estritamente read-only**: `Read/Grep/Glob + git status/log/show` — **ZERO execução de script** (H1: `bun run scripts/qa/*` expunha cunhagem de credencial [gen-user-jwt/mint-vision-pat], DDL de prod [apply-*.sh via shebang do bun] e o control-plane do loop [--resolve/--disarm] a um LLM injetável; `git diff:*` removido [M2: `--output=` escreve arquivo arbitrário]). O diagnosticador LÊ o fonte dos scripts, nunca os executa. `--max-turns 30`, `timeout 1200`, transcript em `~/logs/mcorch-remediate/`; NUNCA dispara para HEARTBEAT_MISSING. Tier B (fix+commit) = **GO futuro** |
| `scripts/qa/ux-explorer-cron.sh` | **M (gerador de backlog)** | nightly: e2e-user-zero flows + Vision QA com lente designer UX/UI sênior → achados no finding-schema → incidentes `UX_FINDING` P1/P2/P3; P1 → Telegram imediato + elegível L2; P2/P3 → digest diário |
| Sessão `/loop` v3 | **P+E nível 3** | início: `--list-incidents`; incidentes = itens EXECUTOR (diagnóstico→fix→prova→commit) fechados com `--resolve`; NUNCA faz polling de monitoramento próprio |

## Knowledge (K) — schemas

### `guardian-state.json` v2 (UNTRACKED — `git rm --cached` + `.gitignore`; escritor único = subcomandos do tick; exceção documentada: `remediation_report` é escrito pelo remediate no arquivo do incidente)
```json
{ "schema_version": 2,
  "mode": "observe | auto-remediate",
  "last_tick_at": "…", "last_tick_verdict": "GREEN|RED|SWEEP_DUE", "last_tick_exit": 0,
  "last_sweep_at": "…", "last_sweep_verdict": "…", "sweep_consecutive_red": 0,
  "open_incidents": ["INC-…"],
  "notified": { "<symptom_hash>": "<iso-ts>" },
  "remediate": { "day": "YYYY-MM-DD", "daily_count": 0, "max_per_day": 4 } }
```
State ilegível/corrompido → tick trata como `{}` e reconstrói (fail-safe já existente).

### Incidente `.claude/context/incidents/INC-<utcstamp>-<hash8>.json` (dir gitignored; resolvidos → `archive/`)
```json
{ "id": "INC-20260707T0100Z-a1b2c3d4", "class": "RED_FINDING|SWEEP_RED|NEW_STATE|UX_FINDING|HEARTBEAT_MISSING",
  "severity": "P1|P2|P3", "symptom_hash": "sha1(class+stable_key)",
  "symptom": "…", "source": "tick|sweep|watchdog|ux-explorer",
  "first_seen_at": "…", "last_seen_at": "…", "count": 1,
  "details": ["linhas cruas do achado"], "suggested_action": "…",
  "status": "open|resolved", "resolved_at": null, "resolution": null, "remediation_report": null }
```
`symptom_hash` usa chave ESTÁVEL (sem timestamps) — ex.: `T2:vision-mcp:job_failed`. Dedup: hash igual → `count++` + `last_seen_at`, sem novo arquivo/alerta dentro do cooldown.

### Telemetria (`infra_health_logs`) — REGRAS LOAD-BEARING
1. **Tudo do subsistema guardião usa `service='guardian'`** e o **T2 filtra `service=neq.guardian`** (sem isso o guardião come os próprios erros → RED permanente).
2. **Heartbeat é sempre `status='healthy'`, `event='tick'`** — afirma "monitor vivo"; o veredito vai em `metadata.verdict`. Crash rows usam `event='tick_crash'` (não contam como heartbeat → crash persistente ainda dispara o alarme de ausência).
3. Eventos: `tick` · `tick_crash` · `sweep` · `incident_open` · `incident_resolved` · `heartbeat_missing` · `remediation` · `ux_explorer_run`.

## Sequence (fluxo normal)
1. Cron */5 → wrapper (flock, timeout, env) → `guardian-tick.ts --cron`.
2. Tick: T1 git sync · T2 erros infra 3h (`last_seen_at`, `neq.guardian`) · T3 `autopilot_cycles` (`started_at`) · T4 cadência sweep · T5 frescor da telemetria do watchdog (>20min = RED).
3. Tick grava heartbeat; classifica sintomas; abre/refresca/auto-resolve incidentes (dedup+cooldown); alerta L1; se `mode=auto-remediate` e gates ok → dispara L2 destacado.
4. Exit 10 → wrapper dispara `guardian-sweep-runner.sh` destacado (heartbeats continuam durante o sweep).
5. Nightly → UX-Explorer gera achados → mesmo pipeline de incidentes.
6. Sovereign (Telegram) ou sessão /loop v3 trabalham incidentes → `--resolve <id> --note "<prova>"`.

## Escalação e anti-spam
| Nível | Gatilho | Cooldown/limite |
|-------|---------|-----------------|
| L1 Telegram | incidente NOVO (hash fora do cooldown) | 6h (RED/SWEEP_RED/UX P1) · 12h (NEW_STATE, dedup por sha do origin) · re-ping 1×/dia se aberto >24h · `sweep_consecutive_red≥3` escala o texto |
| L2 headless | incidente novo elegível + `mode=auto-remediate` | budget atômico **4/dia** · 1 tentativa por sintoma/dia · NUNCA para HEARTBEAT_MISSING |
| L3 sessão | humano abre /loop | n/a |

## Verification gates (prova material — Lei 1)
- **G1** wrapper manual → heartbeat row fresco no REST (GET confirma).
- **G2** execução concorrente → 2º processo sai 0 imediato (flock).
- **G3** `SUPABASE_URL` inválida → sem heartbeat falso; crash row apenas.
- **G4** row fake `service='qa-simulated-red'` → 1 incidente + espelho + **exatamente 1** Telegram; repetição no cooldown → `count++` sem Telegram.
- **G5** remover a fake → tick auto-resolve → `archive/` + row `incident_resolved`.
- **G6** `last_sweep_at` −7h → exit 10 → runner → verdict gravado por **merge** (demais chaves intactas = clobber-fix provado).
- **G7** cron comentado 25min → Telegram do watchdog ≤20min + `INC-guardian-heartbeat.json`; restaurar → auto-resolve; sem 2º alerta em 6h.
- **G8** `--disarm` → remediate "gated", zero invocação; `--arm` → transcript existe, `git status` LIMPO (read-only provado), budget=1.
- **G9** UX-Explorer manual → achados no finding-schema; P1 → Telegram; digest gerado.
- **G10** soak 24h → ~288 heartbeats, zero alertas de ausência, zero Telegram espúrio.

## Recovery paths (runbooks)
- **HEARTBEAT MISSING (alerta do watchdog):** `crontab -l | grep guardian` (linha existe/ativa?) → `tail -50 ~/logs/mcorch-guardian.log` → rodar wrapper manual e observar exit → se o tick quebrou, o traceback está no log; corrigir e o próximo tick auto-resolve o incidente.
- **Sweep RED repetido:** cada RED refresca o incidente (count++); consertar a guarda apontada; próximo sweep verde zera `sweep_consecutive_red` e auto-resolve.
- **State corrompido:** tick reconstrói de `{}`; incidentes órfãos re-listados por `--list-incidents` (fonte = dir, não o state).
- **Telegram fora:** notify exit≠0 fica no log do cron; incidentes/telemetria continuam (alerta é degradado, não perdido — inbox durável).
- **Ambos crons mortos (tick+watchdog):** risco residual aceito; backstop humano = silêncio do morning-briefing 03:30. Futuro: systemd timer.

## Success signal
`infra_health_logs` com `service='guardian' event='tick'` a cada 5min por 24h, **zero** alertas de ausência, **zero** Telegram espúrio, e **um** RED simulado produzindo **exatamente um** Telegram com incidente rastreável ponta-a-ponta (open → notified → resolved → archive).

### Endurecimentos do /security-review (BLOCK → SAFE, 2026-07-07)
- **H1**: allowlist do L2 sem NENHUMA execução de script (era `bun run scripts/qa/*` — vetor de mint/DDL/control-plane via prompt injection de campos de incidente).
- **M2**: `git diff:*` removido (`--output=<path>` = escrita arbitrária).
- **M3**: flock de remediação (G4) adquirido ANTES do consumo de budget (G2) — mata o budget-drain por corrida de remediates destacados.
- **M4**: locks/stamps/scratch movidos de `/tmp` (nomes previsíveis → symlink attack em host multi-user) para `~/.mcorch/run` (0700).
- Residual aceito e documentado: `writeState` do tick é read-merge-write sem file-lock — corrida tick×remediate em CHAVES diferentes pode perder um timestamp de `notified` (pior caso: 1 Telegram duplicado pós-cooldown). Não-explorável para mint/bypass.

## Anti-patterns proibidos
- ❌ LLM decidindo pacing de monitoramento (ScheduleWakeup como monitor).
- ❌ Check de vigilância inline/improvisado fora do `guardian-tick.ts` (lição 21:07).
- ❌ Heartbeat com `status='error'` ou verdict no status (quebra a semântica de ausência e realimenta o T2).
- ❌ Escrita no state/incidentes fora dos subcomandos do tick (exceção única: `remediation_report`).
- ❌ L2 disparando para monitor-morto ou sem budget/flock.
- ❌ `git`-trackear state/incidentes (árvore perpetuamente suja).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

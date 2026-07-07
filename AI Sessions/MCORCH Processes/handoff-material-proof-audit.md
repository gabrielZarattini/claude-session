# SOP — Handoff Material Proof Audit v1.0

**Versão:** v1 · **Selada:** 2026-05-19 · **Lei 2 (Processo Antecipado)** · Trigger: `/handoff` Fase 5c, OU auditoria on-demand de um selo via `bun run scripts/qa/run-audit.ts`

> Esta SOP documenta o **processo humano** de verificação de prova material de um selo `/handoff`.
> O skill `mcorch-qa-healing` (`scripts/qa/run-audit.ts`) **automatiza exatamente esta sequência**.
> Se um humano não consegue executá-la sem erro, o script também não conseguirá — Lei 2.

## ORO triplet

- **Operator:** o agente que executa `/handoff` (MCORCH Master Execution Agent). Fallback manual = o Sovereign rodando a Sequence à mão no shell. Após o v1 do `mcorch-qa-healing`, o Operator usa o script; esta SOP é a referência manual de quando o script não está disponível ou precisa ser auditado.
- **Reviewer:** Sovereign (Gabriel) — revê o Proof Manifest no relatório da Fase 8.
- **Owner:** Sovereign até v6.4.x; migra para o `engineer` agent depois. Risco material: um selo com claim de SUCCESS falsa (commit inexistente, UUID que não resolve, teste que não passou) chega ao `origin/main` e corrompe o ledger de handoff — exatamente a morte por dívida invisível que a SSP-01 Lei 1 existe para prevenir.

## Contexto

O ritual `/handoff` (`.claude/commands/handoff.md`) sela cada sessão em 8 fases e encerra com o bloco **Survival Laws Self-audit** (`.claude/rules/survival.md`, "Self-audit cadence"). O item de Lei 1 — *"Toda claim de SUCCESS desta sessão tem prova citada?"* — é hoje **auto-declarado**: o próprio agente que fez o trabalho marca o checkbox da própria prova. Um check de materialidade auto-avaliado é, ele mesmo, uma claim não verificada.

A **Fase 5c — Material Proof Audit** fecha esse buraco: entre a Fase 5b (secret scan do `HANDOFF.md`) e a Fase 6 (BoK seal status), um passo **independente** extrai cada claim de prova material do selo e a confronta com o artefato físico real. Se qualquer claim é contradita, o selo é **bloqueado** — consistente com as Fases 1 e 5b, que já bloqueiam.

## Pre-conditions

- `.env` na raiz do repo com `SUPABASE_URL` (ou `VITE_SUPABASE_URL`) e `SUPABASE_SERVICE_ROLE_KEY`.
- `git`, `bun` e `npx tsc` disponíveis no ambiente do selo.
- `HANDOFF.md` já atualizado pela Fase 5 — contém o bloco `## <Fase> Record` mais recente + a tabela `Commit`.
- Fase 2 (commits granulares) já concluída — os hashes citados já existem no repo local.
- A Fase 3 (Knowledge Mesh Milestone) já rodou — o nó de handoff e seu UUID existem (ou falharam de forma logada).

## Sequence — verificação manual humana

> Cada passo abaixo é o equivalente humano de um verifier do `run-audit.ts`. `${SB}` = `SUPABASE_URL`; `${KEY}` = `SUPABASE_SERVICE_ROLE_KEY` (ler do `.env`, NUNCA colar o valor em doc/commit).

| # | Action | Output esperado | Verification gate |
|---|--------|-----------------|-------------------|
| 1 | Ler o bloco `## <Fase> Record` mais recente do `HANDOFF.md` e listar cada claim material: hashes de commit, UUIDs Supabase, frases de `tsc`, contagens de teste (`N passed`), tamanhos de deploy (`NN.N kB`), paths de arquivo | Uma lista enumerada de claims, cada uma com seu `kind` | A lista cobre TODA claim de SUCCESS do Record; nada citado fica de fora |
| 2 | Para cada hash de commit: `git cat-file -e <hash>^{commit}; echo "exit=$?"` | `exit=0` para hash válido | `exit=0` → `pass`; `exit≠0` → `fail` (commit não existe) |
| 3 | Para cada UUID de nó: `curl -s "${SB}/rest/v1/mcorch_nodes?id=eq.<uuid>&select=id" -H "apikey: ${KEY}" -H "Authorization: Bearer ${KEY}"` | Array JSON com 1 elemento | 1 elemento → `pass`; `[]` → `fail`; erro de rede → `skip` |
| 4 | Para cada UUID de aresta: idem passo 3 contra `mcorch_edges` | Array JSON com 1 elemento | 1 elemento → `pass`; `[]` → `fail`; erro de rede → `skip` |
| 5 | Para a claim de `tsc`: `npx tsc --noEmit; echo "exit=$?"` | `exit=0` (zero erros) | `exit=0` → `pass`; caso contrário → `fail` |
| 6 | Para a claim de testes: `bun run test 2>&1 \| tail -5` | Linha `N passed` com `N ≥` valor citado no Record | `N ≥` citado E exit 0 → `pass`; senão → `fail` |
| 7 | Para cada edge function citada como deployed: `curl -s -o /dev/null -w "%{http_code}" "${SB}/functions/v1/<fn>"` | HTTP status ≠ 404 | `≠404` → `pass` (alcançável); claim só de tamanho (`NN.N kB`) sem nome de fn → `skip`; erro de rede → `skip` |
| 8 | Para cada path de arquivo afirmado: `test -f <path>; echo "exit=$?"` | `exit=0` | `exit=0` → `pass`; senão → `fail` |
| 9 | Tabular o Proof Manifest: `Claim \| Kind \| Expected \| Actual \| Verdict` + linha de veredito | Tabela markdown + `QA VERDICT: …` | Qualquer `fail` → veredito `SEAL BLOCKED`; senão `SEAL ALLOWED` |

## Verification gates

- **Gate commit:** `git cat-file -e <hash>^{commit}` retorna exit 0 para todo hash citado.
- **Gate mesh:** todo UUID citado retorna exatamente 1 linha em `mcorch_nodes`/`mcorch_edges`; ausência (`[]`) é `fail`, indisponibilidade de rede é `skip`.
- **Gate tsc:** `npx tsc --noEmit` exit 0 — zero erros — quando o Record afirma "tsc zero erros".
- **Gate testes:** `bun run test` exit 0 E `N passed` ≥ contagem citada.
- **Gate edge fn:** GET em `/functions/v1/<fn>` retorna status ≠ 404.
- **Gate veredito:** o selo só prossegue para a Fase 6 se NENHUMA claim está em `fail`.

## Recovery path

- **Cenário A — claim contradita (`fail`):** NÃO fabricar a prova. Corrigir a causa real — se o hash está errado no `HANDOFF.md`, corrigir o texto; se o commit não foi feito, voltar à Fase 2 e commitar; se o teste não passou, consertar o código. Re-rodar a Sequence inteira. O selo permanece bloqueado até veredito `ALLOWED`.
- **Cenário B — Supabase inalcançável:** os passos 3, 4 e 7 retornam `skip`, não `fail`. Registrar pulse `degraded` em `infra_health_logs` (`service='qa-healing'`). O selo **prossegue** — flakiness de infra nunca pode produzir um falso bloqueio (NFR-002 / FMEA-003).
- **Cenário C — uma claim do Record não foi capturada na extração:** adicionar a claim manualmente à lista do passo 1 e verificá-la. Se o `run-audit.ts` a perdeu, registrar o padrão faltante como caso de teste de `extract-manifest.ts` (FMEA-001) — a regex precisa ser endurecida.
- **Cenário D — UUID do nó de handoff do próprio selo não resolve:** re-tentar o INSERT da Fase 3 **uma única vez** (`POST mcorch_nodes`), capturar o UUID **real** retornado e reportá-lo. Isto cria um registro verdadeiro — NUNCA editar o `HANDOFF.md` para fazer um UUID falso parecer válido. Se o re-INSERT falha, a claim permanece `fail`.

## Success signal

- Proof Manifest renderizado com **toda** claim em `pass` ou `skip` explícito — zero `fail`.
- Linha de veredito = `QA VERDICT: <N> verified · <M> skipped · 0 failed → SEAL ALLOWED`.
- Uma linha em `infra_health_logs` com `service='qa-healing'`, `status='healthy'` (ou `degraded` se houve `skip`).
- A Fase 5c do `/handoff` libera a passagem para a Fase 6; o selo segue para push.

## Anti-patterns

- ❌ Marcar uma claim como `pass` sem rodar o comando de verificação correspondente — é auto-avaliação, exatamente o vício que a Fase 5c existe para matar.
- ❌ Fabricar um UUID, hash ou contagem de teste para fazer uma claim contradita "passar" — violação direta de Lei 1; halt imediato.
- ❌ Tratar erro de rede / ferramenta ausente como `fail` — bloqueio falso; o correto é `skip` + pulse `degraded`.
- ❌ Rodar `/handoff` pulando a Fase 5c — o gate é silenciosamente burlado (FMEA-007); a Fase 5c está na lista de Invariants do `handoff.md` justamente por isso.
- ❌ Auto-corrigir o texto do `HANDOFF.md` para um claim bater — verificação NÃO é edição; a única cura permitida no v1 é o re-INSERT do nó de handoff (Cenário D).

## Referências

- `.claude/commands/handoff.md` — ritual alvo; a Fase 5c é inserida entre 5b e 6
- `.claude/rules/survival.md` — Lei 1 (Materiality) + bloco "Self-audit cadence" que esta SOP torna mecânico
- `docs/bok/mcorch-qa-healing/` — suíte BoK 9/9 que governa este módulo (FRD §2 define os 7 `kind` de claim)
- `scripts/qa/run-audit.ts` — entrypoint que automatiza esta Sequence (a construir na Stage C)
- `scripts/audit-mesh-edges.ts` — padrão de acesso Supabase REST por service-role reutilizado pelos verifiers
- `scripts/watchdog-mcorch.sh` — helper `write_health()` reutilizado pelo pulse `qa-healing`
- SOP irmã `mcoins-ledger-reconciliation.md` — alvo da verificação de ledger no v3 (PR-020)

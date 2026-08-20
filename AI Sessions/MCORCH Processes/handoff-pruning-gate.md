# SOP — Gate de poda do HANDOFF.md (Lei 3)

> **Status:** ativo desde 2026-07-29 · **Lei:** 3 (Pruning) · **Gate mecânico:** `scripts/qa/check-handoff-size.sh`
> **Wired em:** `/handoff` PHASE 5b-2 (antes do commit do HANDOFF.md)

---

## O obstáculo que gerou este SOP

Em **2026-07-29**, a auditoria 4Cs semanal encontrou o `HANDOFF.md` com **28.756 tokens** — acima do cap de 25k da ferramenta de leitura.

A consequência não era teórica. **O arquivo estava materialmente ilegível:** a própria auditoria não conseguiu ler as 80 primeiras linhas do arquivo que deveria auditar, e qualquer agente entrando por `/handson` perderia o **Task State** — exatamente a seção que existe para dar o pickup de contexto.

O `HANDOFF.md` é o arquivo que carrega o estado da sessão. Ele ficar ilegível é uma falha silenciosa: nada quebra, nenhum teste falha, e o agente seguinte simplesmente arranca **sem contexto**, achando que tem.

A poda daquele dia resolveu o sintoma. Mas o arquivo cresce **~1,7k tokens por record selado** — sem um gate recorrente, ele reencosta no cap em ~4 sessões. Pelo **CLAUDE.md §5 (Obstacle → Synthesis Mandate)**: *se o mesmo erro pode reincidir, ele ainda não foi resolvido — só adiado.* Este SOP é o anticorpo.

---

## Operator — quem executa

**Hoje (manual):** o agente que roda `/handoff`, na PHASE 5b-2, imediatamente antes de commitar o `HANDOFF.md`.
**Comando:** `bash scripts/qa/check-handoff-size.sh`

Não exige host de produção, credenciais nem rede — é leitura de arquivo local. Roda em qualquer ambiente, inclusive container efêmero.

---

## Sequence — em que ordem

| # | Passo | Critério de sucesso material |
|---|-------|------------------------------|
| 1 | Rodar `bash scripts/qa/check-handoff-size.sh` | Imprime linhas/bytes/tokens estimados + veredito |
| 2 | **exit 0 + `✅ OK`** → nada a fazer | Segue para PHASE 5c |
| 3 | **exit 0 + `🟡 WARN`** → pode selar, mas agenda a poda | Registrar no Pendente do record: "podar HANDOFF na próxima sessão" |
| 4 | **exit 1 + `🔴 FAIL`** → **PODAR ANTES DE SELAR** | O script imprime a linha de corte sugerida |
| 5 | Criar o arquivo de archive com cabeçalho + corpo | `docs/handoff-archive/HANDOFF-archive-<AAAA-MM-DD>-and-earlier.md` existe |
| 6 | Truncar o `HANDOFF.md` e reescrever o rodapé | Tabela faixa→arquivo aponta para TODOS os archives |
| 7 | **Verificação de integridade (passo 8)** — obrigatório | Ver gates abaixo |
| 8 | Re-rodar o gate | exit 0 |

### Convenção de nomes e corte

- **Corte sempre num cabeçalho de record** (`^## .*Record (`) — nunca no meio de um bloco.
- **Um arquivo de archive por faixa**, imutável: `HANDOFF-archive-<data-do-record-mais-novo-arquivado>-and-earlier.md`.
- **Newest-first** dentro do archive (mesma ordem do HANDOFF).
- O cabeçalho do archive **aponta para o archive anterior** (cadeia navegável).
- O rodapé `## 📦 Records arquivados` no HANDOFF lista **todas** as faixas.

---

## Verification gates — como confirmar que funcionou

Estes gates são **obrigatórios**. A poda move conteúdo histórico: perder um record é perder a trilha de uma sessão inteira, e o erro é silencioso.

| Gate | Comando | Esperado |
|------|---------|----------|
| **G1 — nenhum record perdido** | comparar os cabeçalhos `^## .*Record (` do original vs (novo HANDOFF + novo archive) | `diff` vazio |
| **G2 — porção mantida intacta** | `diff <(sed -n '1,<CUT-1>p' original) <(sed -n '1,<CUT-1>p' HANDOFF.md)` | byte-idêntico |
| **G3 — porção arquivada intacta** | `diff <(sed -n '<CUT>,<FIM>p' original) <(tail -n +<N> archive)` | byte-idêntico |
| **G4 — gate verde** | `bash scripts/qa/check-handoff-size.sh` | exit 0 |
| **G5 — legibilidade real** | ler as ~40 primeiras linhas do `HANDOFF.md` com a ferramenta de leitura | retorna conteúdo, **não** erro de cap |

> **G5 é o gate que importa.** G1-G4 são estruturais; G5 é o único que prova o objetivo — que o Task State voltou a ser legível. Um arquivo pode passar em G1-G4 e ainda estar quebrado para o próximo agente.

**Antes de podar, sempre:** `cp HANDOFF.md <scratchpad>/HANDOFF.orig.md` — G1/G2/G3 dependem do original.

---

## Recovery path — falha no passo N

| Falha | Recuperação exata |
|-------|-------------------|
| G1 acusa record faltando | `git checkout HANDOFF.md` (se não commitado) OU restaurar do backup em scratchpad e refazer o corte na fronteira correta de cabeçalho |
| G2/G3 acusam drift | O corte pegou no meio de um bloco. Restaurar do backup, recalcular a linha de corte com `grep -n '^## .*Record ('` e refazer |
| G4 ainda FAIL após podar | Corte não foi fundo o bastante — rodar o script de novo e usar a NOVA linha sugerida |
| Nenhum corte deixa sob o alvo | Cabeçalho + Task State já passam do alvo sozinhos → condensar o Task State (1 linha por fase; o detalhe já vive nos records) |
| Já commitado e errado | `git revert` do commit de poda; refazer com backup do original recuperado via `git show <sha>^:HANDOFF.md` |

---

## Success signal — sinal materialmente observável

**O fluxo completo está correto quando, simultaneamente:**

1. `bash scripts/qa/check-handoff-size.sh` → **exit 0**;
2. os 5 gates G1-G5 passam, com **G5 provado por leitura real** do arquivo;
3. `docs/handoff-archive/` contém a cadeia completa de archives, cada um alcançável pelo rodapé do `HANDOFF.md`;
4. `grep -c '^## .*Record (' HANDOFF.md` + `... archives` = contagem do original (**zero perdidos**).

---

## Anti-patterns proibidos

- ❌ **Deletar records** em vez de arquivar. Nada se perde — o histórico explica o PORQUÊ das decisões atuais.
- ❌ Podar **sem backup** do original (mata G1/G2/G3 — a verificação vira palpite).
- ❌ Cortar no meio de um bloco de record (quebra o markdown e perde contexto pela metade).
- ❌ Declarar "podado ✅" **sem rodar G5** — o objetivo é legibilidade, não contagem de linhas (Lei 1).
- ❌ Arquivar e **não atualizar o rodapé** → archive órfão, trilha quebrada.
- ❌ Tratar o `🟡 WARN` como verde permanente — WARN é dívida agendada, não isenção.

---

## Referências

- Lei 3 (Pruning) — `.claude/rules/survival.md`
- Obstacle → Synthesis Mandate — `CLAUDE.md` §5
- Precedente de archive — `docs/handoff-archive/HANDOFF-archive-2026-07-12-and-earlier.md`
- Auditoria que gerou este SOP — `.claude/context/audit-log.md` (entrada 2026-07-29)
- Skill homônima (gatilho automático) — `.claude/skills/handoff-pruning-gate/SKILL.md`

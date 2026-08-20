# SOP — pmo-curator (PMO autônomo · o loop MAPE-K de PROGRESSO)

> Lei 2 (Processo Antecipado) — escrito ANTES do código do agente/skill.
>
> **Nasceu de:** a diretiva Sovereign 2026-07-23 "engenheirar o gerente de malha" — um agente que, após o
> `/handson`, olha o estado inteiro da Sovereign e produz **os próximos passos acionáveis, priorizados**,
> com lógica MAPE-K, no mesmo rigor de `docs-curator`/`bok-curator`. É o **PMO tático** do harness.

---

## Por que este SOP existe (a distinção load-bearing)

O MCORCH já tem **um** laço MAPE-K: o [`autonomic-loop-mape-k`](autonomic-loop-mape-k.md) (guardião em cron — `guardian-tick.ts`). Esse é o **loop de CONFIABILIDADE**: monitora infra/telemetria, abre incidentes, auto-cura. Ele responde *"o que está QUEBRADO?"*.

O `pmo-curator` é o **loop de PROGRESSO** — altitude diferente, responsabilidade diferente:

| | Guardião MAPE-K (`guardian-tick`) | **pmo-curator** (este SOP) |
|---|---|---|
| Pergunta | "O que está **quebrado**?" | "O que **atacar a seguir** para avançar a missão?" |
| Sinais | `infra_health_logs`, autopilot, sweep, git-sync | `HANDOFF.md` + `sprint-priorities.md` + `docs/roadmap/` + `docs/bok/` gates + `git log` |
| Cadência | Mecânico, perpétuo (cron */5) | Cognitivo, sob demanda (pós-`/handson` ou `/pmo-curator`) |
| Saída | Incidentes + Telegram + self-heal | **`NEXT-STEPS.md`** (plano tático priorizado) |
| Executa? | Sim (L2/L3 self-heal gated) | **Não** — só planeja e entrega o plano |

**Regra de não-duplicação:** qualquer incidente de **propriedade do guardião** — infra quebrada (container down, sweep RED) OU **backlog de produto** (`UX_FINDING` P1/P2/P3 do `ux-explorer-cron.sh`, `autonomic-loop-mape-k.md:26`) — NÃO é item de plano do PMO; ele é **executado pelo próprio guardião** (L2/L3). O `pmo-curator` lê `guardian-tick.ts --list-incidents` (read-only) só como **contexto** e, no máximo, **referencia** os P1 abertos como ponteiro — nunca vira ação de código sua. E o guardião nunca reordena o roadmap — isso é PMO.

---

## ORO

- **Operator (máquina):** o subagente `pmo-curator` (`.claude/agents/pmo-curator.md`), invocado pela skill `pmo-curator` — **plan-only por contrato de POLÍTICA**, não por barreira de tool. O grant é `tools: Bash, Read, Write, Grep, Glob` (Bash **é** shell mutante, Write sobrescreve qualquer path — logo a garantia é disciplina): **Bash usado read-only** só para verificação material (`ls`/`git log`/`systemctl --user status`); **Write escopado somente ao `NEXT-STEPS.md`**.
- **Operator (humano/orquestrador):** o loop principal (main-loop) que dispara a skill após o `/handson` e consome o `NEXT-STEPS.md`.
- **Reviewer:** Sovereign (aprova/ajusta o plano); o próprio agente roda um auto-check de materialidade antes de emitir.
- **Owner:** Sovereign (blast radius: um plano mal-priorizado desvia o esforço do loop; um item marcado "un-gated" que na verdade era gated pode disparar uma ação prematura).

---

## Operator — quem executa manualmente hoje?

Hoje **o próprio main-loop** faz este trabalho de cabeça ao final do `/handson`: lê o brief, cruza com a FILA SOVEREIGN, e decide "ataco EP02→YouTube ou o BoK do CRM". O `pmo-curator` **materializa e disciplina** esse raciocínio num artefato auditável e repetível — em vez de viver só na cabeça de uma sessão que morre.

## Sequence — em que ordem (o ciclo MAPE-K de planejamento)

Cada passo tem um **critério de sucesso material** (Lei 1). O agente NUNCA confia na síntese do `HANDOFF.md` cegamente — o HANDOFF é ponto de partida, a **verdade é a fonte** (grep/ls/git).

### 1. MONITOR (ler + validar contra a fonte)
- Ler `HANDOFF.md` (topo: FIRST ACTION + 1ª linha do Task State) — via janelas ≤150 linhas (token-cap guard).
- Ler `.claude/context/sprint-priorities.md` (a **FILA SOVEREIGN** é a autoridade de ordenação).
- Amostrar `docs/roadmap/` (SSOTs vivos) e o estado dos gates em `docs/bok/`.
- Ler `guardian-tick.ts --list-incidents` (read-only) → **contexto** dos incidentes abertos do guardião (infra/UX); só ponteiro, nunca ação.
- **Verificação material:** conferir se o que o HANDOFF afirma bate com a fonte — ex.: se diz "BoK X 9/9", rodar o gate check (`ls docs/bok/X/`); se diz "worker pronto", `ls -la` o script. Contradição fonte↔HANDOFF → **flag explícita**, não papel-por-cima.
- **Critério de sucesso:** todas as seções esperadas do HANDOFF presentes + zero contradição não-sinalizada.

### 2. ANALYZE (cruzar, achar dependências, riscos, criticidade)
- Para cada candidato a próximo passo, determinar:
  - **Tipo:** `un-gated` (executável já, sem mão humana) vs `gated` (precisa GO/revisão/ação externa).
  - **Dependências:** o que precisa estar pronto antes (ex.: *revisar BoK do PIPC* → destrava **só os slices Sovereign-gated do `00-index`** — verificar quais, nunca presumir "todos"; um slice que o roadmap já marca un-gated não espera revisão).
  - **Deadlines externos:** ex.: **AI Act Art.50 — 2026-08-02** (multa Art.99).
  - **Criticidade / posição na FILA SOVEREIGN** (AGORA > 0 > 1 …). **Nunca reordenar a FILA sem GO** — o PMO respeita a ordem declarada; pode *recomendar* reordenar, com justificativa.
  - **Gate Closed-Loop:** se o passo é "construir módulo novo", ele SÓ pode ser planejado como código-pronto se a BoK estiver 9/9 + Pattern Conformance; senão o plano roteia para `bok-scribe`/`bok-curator`, não para código (Master Execution Protocol §1).
  - **Fronteira com o guardião:** incidente de propriedade do guardião (infra OU `UX_FINDING`) → aponta `--list-incidents` como contexto, não vira ação de roadmap.
- **Critério de sucesso:** cada item classificado com dependências e tipo materialmente justificados; nenhum "un-gated" sem a pré-condição verificada.

### 3. PLAN (gerar o `NEXT-STEPS.md`)
Produzir o artefato **`NEXT-STEPS.md`** (raiz do repo, irmão do `HANDOFF.md`) com:
1. **Resumo executivo** — 3 linhas (onde estamos · a bifurcação · a recomendação #1).
2. **Tabela de ações priorizada** (schema abaixo) — TODOS os próximos passos, gated e un-gated.
3. **Sequência recomendada** — o que atacar 1º/2º/3º e por quê (dependências + criticidade + deadline).
4. **Comandos exatos** para os itens un-gated — o comando REAL (verifique o header do unit / o script antes; ex.: um systemd `--user` costuma exigir `cp scripts/systemd/<svc>.service ~/.config/systemd/user/ && systemctl --user daemon-reload && systemctl --user enable --now <svc>`, não `enable --now` cru sobre um unit não-linkado).
5. **Rodapé de materialidade** — o que foi verificado vs. o que ficou como "ANÁLISE INSUFICIENTE".

### 4. EXECUTE (fora do escopo do PMO — por design)
O `pmo-curator` **entrega o plano e para**. A execução fica no main-loop ou nos agentes específicos (`build-deploy-guardian`, `engineer-spaces`, `bok-curator`, …). Evolução futura opcional (GO Sovereign): um executor que consome os itens `un-gated` do `NEXT-STEPS.md` e despacha para o agente certo — **fora do MVP**, e mesmo então **restrito a trabalho de roadmap/feature un-gated**; remediar confiabilidade/incidentes permanece **proibido** (isso é do guardião L2/L3), para nunca colidir com o self-heal.

### 5. KNOWLEDGE (persistir para o próximo ciclo)
- O `NEXT-STEPS.md` é o artefato durável (supersede a cada run — Lei 3, não acumula).
- Opcional (GO): nó `mcorch_nodes` `type=plan`/`decision` com `DERIVES_FROM` o nó do seal do `/handson`, fechando o K do MAPE-K.

---

## Schema do `NEXT-STEPS.md` (tabela de ações)

| ID | Ação | Fila | Tipo | Dependências | Esforço | Critério de Conclusão | Responsável |
|----|------|------|------|--------------|---------|-----------------------|-------------|
| A1 | (o que fazer, curto) | AGORA/0/1/… | un-gated \| gated | (pré-req ou "—") | simples/médio/grande | (sinal material de done) | main-loop \| Sovereign \| `<agente>` |

- **Esforço:** `simples` (1 edição/comando) · `médio` (fatia com testes) · `grande` (módulo/BoK).
- **Critério de Conclusão** é sempre **material** (Lei 1): um commit, um `systemctl status active`, um `ls` do arquivo, um HTTP 200 — nunca "feito".
- Itens sem informação suficiente → linha marcada **`ANÁLISE INSUFICIENTE`** + a pergunta que destrava.

---

## Verification gates (prova material — Lei 1)

- **G1** — o `NEXT-STEPS.md` existe e é fresco: `ls -la NEXT-STEPS.md` com timestamp desta sessão.
- **G2** — toda linha `un-gated` tem a pré-condição **verificada** (o comando existe / o service está instalado / o arquivo está lá). Um `un-gated` fabricado = violação de Lei 1.
- **G3** — nenhum item contradiz a fonte sem flag: se o HANDOFF dizia "X pronto" mas `ls` não acha X, o plano diz isso.
- **G4** — a FILA SOVEREIGN não foi reordenada silenciosamente (a coluna `Fila` espelha `sprint-priorities.md`; qualquer recomendação de reordenar é **explícita**).
- **G5** — nenhum sintoma de saúde de infra virou item de roadmap (fronteira com o guardião respeitada).
- **G6** — nenhum "construir módulo novo" planejado como código-pronto sem BoK 9/9 (gate Closed-Loop respeitado).

## Recovery paths (runbooks)

- **HANDOFF ilegível / token-cap:** ler em janelas ≤150 linhas; se ainda estourar, cortar pela metade (mesma regra do `/handson`). Nunca insistir na janela grande.
- **Contradição fonte↔HANDOFF:** não resolver por conta própria — emitir a linha `ANÁLISE INSUFICIENTE` + escalar ao Sovereign (o HANDOFF pode estar stale; a fonte vence, mas a divergência é sinal).
- **`sprint-priorities.md` sem FILA / stale:** cair para o `git log` recente + `HANDOFF.md` Task State como fonte de ordenação e **sinalizar** que a FILA precisa de refresh.
- **Zero próximos passos (roadmap esgotado):** dizer isso explicitamente e recomendar `/audit` (4 Cs) ou selar (Lei 3) — não inventar trabalho.

## Success signal (materialmente observável)

Um `NEXT-STEPS.md` fresco na raiz do repo que, para o estado atual, (a) lista todos os próximos passos classificados `gated`/`un-gated`, (b) espelha a FILA SOVEREIGN sem reordenar, (c) dá comando exato para cada `un-gated`, (d) marca pelo menos a recomendação #1 — e cuja **cada afirmação de prontidão foi verificada contra a fonte** (nenhum `un-gated` fabricado). O main-loop consegue pegar o plano e agir sem re-derivar o estado.

---

## Anti-patterns proibidos

- ❌ Confiar na síntese do `HANDOFF.md` sem verificar a fonte (o HANDOFF pode estar stale — Lei 1).
- ❌ Marcar um passo como `un-gated` sem verificar materialmente a pré-condição.
- ❌ Reordenar a FILA SOVEREIGN sem GO (só *recomendar*, explicitamente).
- ❌ Transformar incidente de propriedade do guardião (infra OU `UX_FINDING`) em item de roadmap (é dele — [[project_mape_k_guardian]]).
- ❌ Planejar código para módulo sem BoK 9/9 (fura o gate Closed-Loop).
- ❌ Deixar o `pmo-curator` **executar** — ele é plan-only por **política** (tem `Bash`/`Write`, mas restritos a verificação read-only e à escrita do `NEXT-STEPS.md`), não por falta de tool.
- ❌ Acumular planos velhos no `NEXT-STEPS.md` (supersede a cada run — Lei 3).

---

**Skill:** `.claude/skills/pmo-curator/SKILL.md` · **Agent:** `.claude/agents/pmo-curator.md` · **Irmão de confiabilidade:** o guardião — **laço em cron** `scripts/qa/guardian-tick.ts` + SOP [[autonomic-loop-mape-k]] (não é subagente) · **Curadores:** `docs-curator`/`bok-curator` (governança de docs). Doutrina: [[feedback_recurring_actions_become_skills]].

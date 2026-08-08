# SOP — Gerar PELO NÓ, não pelo CLI (Lei 2)

> **Status:** ativo desde 2026-08-04 · **Origem:** diretiva Sovereign, verbatim:
> *"nas próximas gerações que você fizer direto é melhor que seja pelo nó já no Spaces, para depois
> não ter que ficar sintetizando algo que você já fez."*

---

## O obstáculo que gerou este SOP

Em 2026-08-04 gerei as 15 narrações do EP06 por um runner CLI (`scripts/ep06/gen-narration.ts`).
Funcionou: 3:24 de narração na voz IVC, verificada por whisper.

E aí veio o custo escondido. Os arquivos estavam **no disco do host** — não no projeto. Para o
trabalho valer alguma coisa dentro do produto, foi preciso um SEGUNDO runner
(`push-narration-to-spaces.ts`) só para: subir cada arquivo, registrar na spine com `project_id`,
criar os nós de voz, conectar nas cenas e ajustar as durações.

**Metade do trabalho foi reconciliação** — trabalho que não existiria se a geração tivesse nascido
dentro do nó. E reconciliação é o tipo de tarefa que erra em silêncio: um arquivo que não sobe, um
`project_id` que não entra, um nó que fica sem conexão. Ninguém percebe até faltar.

Isto é o [[feedback_cli_actions_must_become_ui]] levado um passo adiante: não basta o CLI virar UI
depois — **a geração precisa nascer na UI**.

## Operator — quem executa

O agente (eu) ao produzir qualquer mídia para um projeto do Spaces.

## Sequence — a ordem correta

| # | Passo | Critério material |
|---|-------|-------------------|
| 1 | O nó existe no canvas para aquele tipo de mídia? | consta em `canvas-node-registry.ts` |
| 2 | **Não existe** → construir o nó ANTES de gerar (SOP `engineer-spaces-node-authoring`) | nó no editor VIVO com inspector e motor |
| 3 | **Existe** → gerar pelo nó (UI ou invocando a MESMA edge fn que o nó invoca, com `project_id` e `node_id`) | linha na fila/ledger com `project_id` |
| 4 | O asset nasce na spine com `metadata.project_id` | aparece filtrado por projeto na Biblioteca |
| 5 | O nó reflete o resultado (preview/`output`) sem passo manual | card mostra a mídia |

## Quando o CLI ainda é legítimo

Não é proibição cega — é sobre **onde o resultado precisa viver**:

- ✅ **Exploração/probe**: medir custo por frame, sondar contrato de API, testar um filtro. O
  resultado é conhecimento, não asset.
- ✅ **Lote grande e repetitivo** (frota de 19 takes): aceitável **se** o runner já gravar
  `project_id`/`node_id` e registrar na spine — ou seja, se ele fizer o que o nó faria.
- ✅ **Motor que ainda não tem nó**: aí o CLI é a ponte, e a dívida é construir o nó (Amendment 34).
- ❌ **Gerar mídia final de um projeto que TEM nó** e reconciliar depois. Isso é retrabalho.

## Verification gate

Antes de rodar um runner que gera mídia, uma pergunta: **"o resultado disto precisa aparecer no
projeto do usuário?"** Se sim e existir nó → use o nó. Se sim e não existir nó → construa o nó.

## Recovery path

Se já gerou fora (o caso do EP06): escreva o runner de reconciliação **na mesma sessão**, subindo
com `project_id`, registrando na spine, criando os nós e conectando. Precedente:
`scripts/ep06/push-narration-to-spaces.ts`. Não deixe a reconciliação para depois — arquivo em
`/tmp` morre no reboot ([[feedback_scratchpad_harvest_continuity]]).

## Success signal

O usuário abre o projeto no Spaces e **vê a mídia no nó** — sem que ninguém tenha rodado um segundo
script para colocá-la lá.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

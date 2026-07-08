# SOP — Spaces Canvas: criação, edição e persistência (Fase 1a)

> **Lei 2 (Processo Antecipado).** SOP do fluxo humano que a Fase 1a do Spaces automatiza —
> detalha os processos `PROC-SPACES-001/002/006` da BoK (`docs/bok/spaces-evolution/07-process-flow.md`)
> no nível de operação. Execução/ledger (PROC-SPACES-003) é a Fase 1b — fora deste SOP.
> Criada 2026-07-02, antes do código (loop autônomo it.3).

## Operator

**Sovereign (Gabriel)** como Usuário Zero — abre `/dashboard/spaces`, cria/edita canvases.

## Sequence

1. `/dashboard/spaces` → lista os Spaces do tenant (RLS-own) com nome, nº de nós e updated_at;
   empty-state pt-BR canônico (*"Nenhum Space ainda…"*, FR-SPACES-001).
2. **Criar** → dialog de nome → INSERT em `spaces` (graph vazio) → navega para `/dashboard/spaces/:id`.
3. **Canvas** (`SpaceCanvasPage`): hidrata o grafo de `spaces.graph` (jsonb) no `useSpacesStore`
   — nós/edges passam pelos guards zod ANTES de entrar no store (`FMEA-SPACES-007`); linha de
   outro tenant → RLS devolve vazio → tela "Space não encontrado" (404-like, `FR-SPACES-007`).
4. **Inserir nó**: Spotlight (`N` ou `/`) → busca nos 26 tipos canônicos → `⏎` insere no centro
   da viewport, auto-selecionado, título auto-numerado (`PROC-SPACES-001`).
5. **Conectar**: arrastar porta→porta → `canConnect` (única fonte de verdade) valida os 6 tipos;
   incompatível → toast pt-BR *"Tipos incompatíveis: {a} → {b}"* e a edge NÃO entra (`PROC-SPACES-002`).
6. **Editar parâmetros**: HUD direito 72/28 (nó selecionado → schema de `useParamRegistry`).
7. **Persistir**: toda mutação → debounce 800 ms → UPDATE de `spaces.graph`
   (`PROC-SPACES-006`) com **guard empty-over-nonempty** (nunca sobrescrever grafo cheio com
   vazio — anticorpo do incidente Canvas 2026-06-25 / `FMEA-SPACES-006`).

## Verification gates

| Gate | Critério material |
|---|---|
| G1 — persistência real | Criar space + 2 nós + 1 edge → reload → grafo volta; provado pela ROW no DB (`spaces.graph` jsonb com os ids), não pelo DOM. |
| G2 — porta tipada | Conexão `image→text` rejeitada com toast; `text→text` aceita (smoke de store + browser). |
| G3 — anti-perda | Save com store vazio ANTES da hidratação não sobrescreve grafo cheio (guard provado por teste/verificação). |
| G4 — tenant | `spaces` RLS-own 4 policies; abrir id de outro tenant → "não encontrado" (sem vazamento). |
| G5 — zero débito | Fase 1a não toca ledger: nenhuma chamada a `deduct_mco_coins`/`canvas-execute`. |

## Recovery path

- Falha no UPDATE → toast pt-BR + estado local preservado (zundo buffer); retry no próximo debounce.
- Grafo corrompido no DB → guards zod dropam apenas os itens inválidos (console.warn) e o canvas abre
  com o resto — nunca white-screen (`FMEA-SPACES-005`: lookups sempre com fallback).

## Success signal

Sovereign cria um Space, monta um grafo tipado via Spotlight, recarrega a página e o grafo está lá —
com a linha correspondente em `spaces` (UUID citável) e Vision-QA APROVADO no print 1920×1080.

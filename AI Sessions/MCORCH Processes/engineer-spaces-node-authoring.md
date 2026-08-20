# SOP — Autoria de Nós do Spaces / Infinite Canvas (engineer-spaces)

> Lei 2 (Processo Antecipado). Como um humano adiciona/altera um tipo de nó do Spaces **corretamente**,
> ponta-a-ponta, contra o sistema VIVO. Skill/agente irmãos: `engineer-spaces`.
> Recon de suporte: `.claude/context/spaces-loop-recon-2026-07-21.md` (mapa VIVO com file:line).

## Operator
O especialista **engineer-spaces** (L2 sob `engineer`), ou o MCORCH Master Agent operando a skill.
Ferramentas: editor de código (`src/`), `bun run build`, `npx tsc -p tsconfig.app.json`,
`agent-browser` / auditoria E2E do Canvas, Vision QA.

## Sequence (cada passo com critério de sucesso material)

| # | Passo | Critério de sucesso material |
|---|-------|------------------------------|
| 0 | **Confirmar VIVO vs MIRROR** | `grep -n "spaces/:id" src/App.tsx` → `CanvasEditorPage`. NUNCA editar `node-registry.ts`/`useSpacesStore` (mirror não-roteado). |
| 1 | **Tipo + factory** em `src/types/canvas.ts` | `<kind>` na união `CanvasNode` + `makeDefault<Kind>` compila. |
| 2 | **Catálogo** em `src/lib/canvas-node-registry.ts` | entrada com `category ∈ NodeCategory`; `factory` referenciada. |
| 3 | **Inspector** + dispatcher `RightPanel/index.tsx` + card `canvas/nodes/` | o nó abre o inspector ao ser selecionado. |
| 4 | **Despacho** (ledger `node_run_id` / edge-fn / fila `video_renders`) | dispatch retorna 2xx (não 422); job real produz output. |
| 5 | **Custo** server-side (`CREDIT_COSTS` ou `charged_mco:0`) | débito real = valor declarado (witness saldo −exato) OU grátis. |
| 6 | **Assets** assinados owner-scoped (`asset-url.ts`) | mídia renderiza (URL assinada 200), não 400. |

## Verification gates (output esperado)

- `bun run build` → exit 0 (bundla; NÃO typa).
- `npx tsc -p tsconfig.app.json --noEmit` → **contagem de erros ≤ baseline**, **nenhum erro novo em arquivo tocado** (o app tem backlog pré-existente — compare com `tsc-baseline.txt`, não exija limpo). Categoria fora do union aparece como `TS2322`.
- Migration (se houver): `/security-review` **NO FINDINGS** antes do commit.
- Auditoria E2E do Canvas 1920×1080: nó aparece no Spotlight/palette, conecta e despacha (screenshot).
- Vision QA ocular de toda mídia gerada (Lei 1 — o detector honesto).

## Recovery path (falha por passo)

- **Nó não aparece no editor** → você editou o MIRROR. Reaplique nos arquivos VIVOS (passo 0).
- **Dispatch 422** → falta `node_run_id` no payload (ledger) OU `<kind>` fora de `EXECUTABLE_TYPES`/branch. Adicione o `node_run_id` (`useGenerationLedger`) ou roteie por edge-fn/fila.
- **`tsc` acusa erro novo** → conserte antes de commitar (não confie no `build`, que ignora tipos).
- **Mídia 400** → assinar owner-scoped (`toDisplayUrl`), nunca `getPublicUrl` em bucket privado.
- **Motor material sem BoK** → parar; abrir Amendment BoK + Pattern Conformance (Closed-Loop Step 3.5).

## Success signal

O nó novo: (a) aparece e conecta no Canvas vivo (E2E 1920×1080), (b) despacha e produz output real
(job UUID / render MP4 ≥100KB / asset assinado 200), (c) cobra o valor exato server-side (ou grátis),
(d) `tsc` sem erro novo e `build` verde, (e) Vision QA ocular aprovado. Só então "pronto".

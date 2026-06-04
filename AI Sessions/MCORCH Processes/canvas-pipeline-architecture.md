# Canvas Pipeline Architecture - C1 Foundation

**Version:** 1.0
**Selada:** 2026-05-28 07:00 BRT
**Lei 2:** (Anticipated Process) All UI and backend schema modifications must be governed by this document. Standard handle conventions must be fully updated in the frontend nodes before deploying compilation checks, and backfills must be run in `--dry-run` mode first to inspect and confirm all edge mappings.

---

## ORO Triplet

- **Operator:** MCORCH Master Execution Agent
- **Reviewer:** Sovereign (Gabriel Zarattini)
- **Owner:** Sovereign — blast radius = Canvas Studio project integrity, historical project graphs, connection logic

---

## Context

This document outlines the foundational architecture for the Canvas pipeline, focusing on the new handle convention and edge port routing. The goal is to standardize how nodes connect and exchange data, moving towards a more robust and predictable graph structure. This refactor is crucial for enhancing the stability, debuggability, and extensibility of the Canvas module, ensuring consistent data flow and easier integration of new node types. The handle convention defines explicit input and output ports on each node, enabling precise routing of data edges and preventing ambiguous connections within the canvas graph.

---

## Handle ID Convention

| Node Kind           | Output Handle (ID) | Input Handles (IDs)                               |
|---------------------|--------------------|---------------------------------------------------|
| `characterReference`| `output`           | `input_image`, `input_text`                       |
| `generateImage`     | `output_image`     | `input_prompt`, `input_style`                     |
| `imageToVideo`      | `output_video`     | `input_image`, `input_audio`                      |
| `sceneCompose`      | `output_scene`     | `input_image_1`, `input_image_2`, `input_layout`  |
| `styleTransfer`     | `output_styled`    | `input_content_image`, `input_style_image`        |

---

## Verification Gates

1. **Semantic Match verification**: All new nodes render Handles with exact `id` matching the `Handle ID Convention` table.
2. **Backward Compatibility**: `scripts/canvas-backfill-edge-handles.ts` successfully maps existing graph edges to these semantic IDs.
3. **DAG compatibility**: Kahn's topological sort handles nodes with these semantic inputs/outputs correctly.
4. **Validation checks**: The UI's `onConnect` event enforces that target handles and source handles use these explicit identifiers.
5. **Phase 5c verify**: Compilation completes without TypeScript errors (`tsc --noEmit`), and all 189+ tests pass.

---

## Recovery Path

If any issues arise during or after implementation:
1. **Frontend Rollback**: Revert to the prior checkout version where `GenerateImageNode` etc., used anonymous (null ID) handles.
2. **Database Rollback**: `scripts/canvas-backfill-edge-handles.ts` saves a JSON backup of the project graphs in `.claude/context/backups/canvas-edge-handles-pre-c1-<date>/` before executing mutations. In case of database graph corruption, run the restore subcommand or execute a SQL script to restore the graphs from these backups.

---

## Anti-patterns Proibidos

- **Anonymous Handles**: Creating a `Handle` component without an explicit `id` property or using empty/null string.
- **Implicit Mapping assumptions**: Hardcoding index-based lookups in DAG sorting instead of using the node kind mapping defined in `src/lib/canvas-handles.ts`.
- **Bypassing the schema validation**: Mutating `graph` rows in `vm_canvas_projects` directly without validating them against the handle ID convention.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

# Veo 3.1 · Refs → 8s Guard (SOP Lei 2)

**Escopo:** Google Veo 3.1 rejeita qualquer duração ≠ 8s quando o payload carrega `instances[0].referenceImages` (feature `reference_to_video`). Este SOP documenta o processo humano equivalente ao clamp UI + guard server pré-débito.

**Referência:** memória `[[reference_veo_refs_require_8s]]` · witness `gen 256b8876` (2026-08-02, char ref + 5s → charged 167 → refunded 167 ANTES desta guarda).

## Operator
- **Humano:** Sovereign (ou operador do MCORCH) clica **Run** num nó `image_to_video` do Spaces que tem 1..3 imagens upstream conectadas como referência de identidade (char ref, sem toggle **First frame**).
- **UI:** `/dashboard/spaces/<slug>` → seleciona nó → RightPanel `ImageToVideoInspector`.

## Sequence
1. UI resolve refs upstream via `findUpstreamImages(node.id, nodes, edges).slice(0, VEO_MAX_REFERENCES)` (`ImageToVideoInspector.tsx:171-173`).
2. UI computa `allowedDurations = veoAllowedDurations({ hasReferences, useFirstFrame })` (helper puro em `src/lib/veo.ts:38-45`): `[8]` quando há refs e NÃO há first-frame; senão `VEO_DURATIONS = [4,5,6,7,8]`.
3. UI auto-clampa `veoDuration → 8` via `useEffect` (`ImageToVideoInspector.tsx:188-198`) e renderiza SÓ o botão 8s (`:594`).
4. Payload sai com `duration = 8` e `reference_image_urls: [...]` (`:251`).
5. Server `canvas-execute` valida PRÉ-DÉBITO em `supabase/functions/canvas-execute/index.ts:1367-1378`: se `hasRefs = !body.input_asset_url && refs.some(non-empty)` e `duration !== 8`, retorna `HTTP 422 {error:"veo_refs_require_8s"}`.
6. Só após passar todos os guards `/1337-1409` o request debita mcoCoins.

## Verification gates
- **G1 · UI:** com char ref conectada e `veoUseFirstFrame=false`, o seletor de duração renderiza apenas o botão **8s** e o helper text explica a trava.
- **G2 · Server:** `curl` do `canvas-execute` com `reference_image_urls:["https://..."]` + `duration:5` + sem `input_asset_url` → `HTTP 422 veo_refs_require_8s` (nenhuma linha em `mco_coins_ledger`).
- **G3 · Test:** `bun run test src/test/veo-refs-guard.test.ts` → 6/6 verde (4 combos de `hasReferences × useFirstFrame` + sanity + drift-gate contra `VEO_DURATIONS`).

## Recovery path
- **Payload adulterado (cliente fora da UI, refs + duração<8):** server retorna 422 ANTES do débito → operador vê toast PT-BR e ajusta.
- **Prova de que a guarda é necessária:** witness `gen 256b8876` — SEM esta guarda o pipeline cobrou 167 mco e refundou 167 (saldo intacto, mas ledger poluído + latência do Google). Lei 1: charge+refund não é equivalente a 422 pré-débito.

## Success signal
- Nó `image_to_video` com char ref e sem first-frame só permite gerar em 8s (UI trava · server 422 se burlar).
- `src/test/veo-refs-guard.test.ts` verde no CI.
- Zero linhas `mco_coins_ledger` para combinações inválidas (`refs && dur≠8 && !firstFrame`).

# SOP — Sinapses por Similaridade de Embedding (OTD-SYNAPSE-EMBEDDING, Fase B)

> Lei 2 (Processo Antecipado). Feature = enriquecer a fusão "Universo" do Unified Sensorial
> Canvas (`/dashboard/universe`, superfície PRIMÁRIA de constelação pós-cutover 3.9) com
> **sinapses semânticas**: linhas código↔memória derivadas de similaridade de cosseno 768d,
> rotuladas HONESTAMENTE como *similaridade* — nunca uma relação de malha fabricada (Lei 1).
>
> Contexto: as sinapses Fase A (`useSynapses`, FR-046) desenham só as **7 arestas
> cross-partition reais** de `mcorch_edges` (`DERIVES_FROM`/`observes`) → a fusão fica
> visualmente vazia. A riqueza real vive na vizinhança semântica entre os 224 nós de
> memória (system knowledge) e os 8402 nós de código (AST), ambos 100% embedded.

## ORO
- **Operator:** MCORCH Master Execution Agent (loop autônomo).
- **Reviewer:** Sovereign + `/security-review` independente sobre a migration.
- **Owner:** Sovereign (superfície visual; custo USD = 0, computação server-side sobre índice HNSW existente).

## Precondições materiais (provadas Lei 1 — loop 2026-07-05)
| Fato | Valor | Fonte |
|------|-------|-------|
| Nós de código (AST) | 8402, **todos `user_id NULL`** (system-shared), 100% embedded | REST count=exact |
| Nós de memória (system knowledge) | 224 `project_id NULL AND user_id NULL`, 100% embedded | REST count=exact |
| Veredito de segurança | RPC que retorna `(memory_id, code_id, similarity)` de partições system-shared **não vaza cross-tenant** (FMEA-011) | ambas partições `user_id NULL` |
| Custo cliente proibitivo | baixar embeddings de 8626 nós ≈ 25MB + cosseno no main thread = inviável | 768d × 4B × 8626 |

⇒ A similaridade DEVE ser computada **server-side** (pgvector HNSW), nunca no cliente.

## Operator — quem executa hoje (manual equivalente)
Um engenheiro rodaria, para cada nó de memória, um `SELECT ... ORDER BY embedding <=> :mem_embedding LIMIT k`
contra os nós de código, coletaria os pares acima de um threshold, e desenharia uma linha
tracejada distinta (visual ≠ das arestas reais) rotulada "similaridade". A automação é
exatamente isso, batido em UMA RPC `LATERAL`.

## Sequence (cada step com critério material)
1. **Migration — RPC `match_memory_code_synapses(match_count, match_threshold)`**
   `SECURITY DEFINER` **com filtros `user_id IS NULL` HARDCODED nas duas partições** (mesmo padrão do
   `match_mcorch_nodes`) — escolhido não por escalada, mas para **garantir o plano do índice HNSW**
   (sob INVOKER, o wrapper de RLS pode empurrar o `LATERAL` p/ seq-scan × 224 iterações). É
   *provably* leak-free por construção: ambos endpoints são nós de sistema (`user_id NULL`), o retorno
   é só `(uuid, uuid, float)` sem conteúdo, e nenhum parâmetro do caller cruza fronteira de tenant.
   `SET search_path = public` (fixo, não-mutável), `STABLE`. `CROSS JOIN LATERAL` top-K vizinhos de
   código por `embedding <=>` (HNSW), filtrando as duas partições system-shared e `similarity > threshold`.
   Caps duros: `match_count` clampeado a [1,5]; retorna só UUIDs + float (zero conteúdo). REVOKE de
   `anon`/`PUBLIC`, GRANT só `authenticated`/`service_role`.
   - ✅ Sucesso: `supabase db push` aplica; ledger registra; `SELECT` de amostra retorna pares plausíveis.
2. **`/security-review`** da migration ANTES do commit (FMEA-011 gate — obrigatório p/ toda migration).
   - ✅ Sucesso: veredito SAFE/CLOSED (sem P0/HIGH cross-tenant).
3. **Regen de tipos** `npx supabase gen types` → `tsc --noEmit` 0.
   - ✅ Sucesso: assinatura da RPC no `types.ts`; tsc 0.
4. **Hook `useSemanticSynapses(graph, memoryNodes)`** — chama a RPC (TanStack, staleTime 5min),
   mapeia pares → segmentos de linha código↔memória usando os MESMOS layouts de `universe-layout.ts`
   que a Fase A usa (âncora por membership dos sets renderizados; par sem endpoint renderizado = descartado).
   - ✅ Sucesso: `count > 0`; toda linha ancorada em 2 nós renderizados.
5. **`SynapseLayer` — camada visual distinta** para similaridade (cor/opacidade/tracejado ≠ das
   sinapses reais) + legenda/contador honesto ("N semânticas · K reais"). Nunca misturar os dois
   registros num contador só.
   - ✅ Sucesso: build 0; badge distingue os dois tipos.
6. **E2E + Vision QA** — `scripts/qa/audit-universe-ui.ts` (magic-link → 1920×1080 → Vision gate).
   - ✅ Sucesso: gate APROVADO; contador de sinapses semânticas > 0 no Terminal Tático.

## Verification gates
- **G1 (segurança):** `/security-review` SAFE — RPC não retorna conteúdo nem linhas de outro tenant.
- **G2 (honestidade Lei 1):** a UI rotula as linhas semânticas como *similaridade*, visualmente
  distintas das arestas reais; contadores separados. Uma linha semântica NUNCA é apresentada como
  aresta de malha.
- **G3 (âncora):** toda sinapse renderizada tem os 2 endpoints nos sets renderizados (código+memória);
  pares órfãos são descartados (idêntico à disciplina da Fase A).
- **G4 (perf):** a RPC roda sobre o índice HNSW; medir latência real (deve ser sub-segundo). Não
  regride o load do Universo (2,5s real-browser baseline it.7).
- **G5 (cap):** `match_count` clampeado server-side a ≤5; total de sinapses ≤ 224×5 = 1120 (bounded).

## Recovery path
- RPC lenta / regride perf → baixar `match_count` p/ 1 e subir `match_threshold` (menos linhas); se
  ainda lenta, materializar em tabela via cron (fora de escopo desta fatia — vira OTD).
- Migration falha ao aplicar → `supabase db push` mostra o erro; corrigir e reaplicar (idempotente
  via `CREATE OR REPLACE`).
- Vision REPROVА → não é regressão de dados; inspecionar screenshot; a Fase A + código + memória
  continuam renderizando (a camada semântica é aditiva, fail-soft: RPC erro → count 0, zero linhas).

## Success signal (materialmente observável)
Gate E2E `audit-universe-ui.ts` **APROVADO** com o contador "Sinapses semânticas > 0" no Terminal
Tático, sobre a superfície primária, e `/security-review` SAFE na migration. As linhas semânticas
aparecem visualmente distintas das 7 arestas reais.

## Anti-patterns proibidos
- ❌ Apresentar linha de similaridade como aresta de `mcorch_edges` (relação fabricada — viola Lei 1).
- ❌ Computar cosseno no cliente (25MB de embeddings no main thread).
- ❌ RPC `SECURITY DEFINER` que aceite `user_id`/partição do caller (aqui os filtros system-shared são
  HARDCODED — o DEFINER só existe p/ garantir o plano HNSW, nunca p/ ampliar escopo).
- ❌ Contador único somando reais + semânticas (esconde a distinção honesta).

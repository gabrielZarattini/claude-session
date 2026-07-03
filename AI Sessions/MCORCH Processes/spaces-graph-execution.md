# SOP — Spaces: execução do grafo com ledger (Fase 1b)

> **Lei 2 (Processo Antecipado).** SOP do fluxo humano que a Fase 1b do Spaces automatiza —
> detalha `PROC-SPACES-003/007/008` da BoK (`docs/bok/spaces-evolution/07-process-flow.md`) no nível
> de operação, e SELA as resoluções das contradições BoK↔código-vivo encontradas no mapeamento
> (workflow `wf_b4abf175-410`, 2026-07-02). Criada ANTES do código (loop autônomo).
> Sibling: `spaces-canvas-persistence.md` (Fase 1a — gates G1-G5 permanecem válidos e invioláveis).

## Operator

**Sovereign (Gabriel)** como Usuário Zero — monta um grafo em `/dashboard/spaces/:id`, estima o
custo (dry-run), roda (▶) e colhe as gerações no cluster do nó, com débito/estorno corretos de mcoCoins.

## Decisões seladas (resoluções de contradição — fonte: síntese `wf_b4abf175-410`)

| # | Decisão | Racional |
|---|---------|----------|
| S1 | **Ordem de débito = ledger-first**: `begin_space_generation` INSERE a row `generations` `status='running'` **e** debita (`deduct_mco_coins`, action `spaces.node.run`) **na MESMA transação**; falha do deduct → rollback da row (nunca órfã). | Resolve a contradição interna da BoK (BPMN insere após provider vs sweep precisa de row `running`); espelha `begin_autopilot_cycle`. |
| S2 | **Idempotência** vive em `generations.node_run_id UNIQUE` + `ON CONFLICT DO NOTHING` no begin (0 rows → retorna estado prévio, **zero segundo débito**) — NÃO no `deduct_mco_coins` (que não tem chave de idempotência). | C3/C5 da síntese. |
| S3 | **`node_run_id` é cunhado no cliente 1× por nó por tentativa de run** (`crypto.randomUUID()`); retry client-side da MESMA tentativa REUSA o id; re-run iniciado pelo usuário cunha id novo. | Retry que cunha id novo derrota a idempotência (C23). |
| S4 | **Reuso do `canvas-execute` (zero tool novo, Pattern #5)** via **extensão aditiva**: presença de `space_id` + `node_run_id` no payload ativa o "Spaces ledger mode" (branch exclusivo). O caminho legado (deduct-after-success do Canvas Studio) fica INTOCADO; os dois branches são mutuamente exclusivos — sem double-charge. | C1/C4. |
| S5 | **Teto diário**: a query do cap passa de `LIKE 'canvas_%spend'` para lista explícita `IN ('canvas_magic_prompt_spend','canvas_image_spend','canvas_video_spend','spaces.node.run')` — senão o gasto Spaces bypassa o teto silenciosamente. Modelo por-role (100/1000/10000) mantido; teto por-plano = débito OPEN (BR-SPACES-003). | C7. |
| S6 | **Refund = crédito positivo** via `finalize_space_generation` (claim `status IN ('pending','running')` — primeiro finalizador vence, idempotente), clamp `0 ≤ refund ≤ mco_charged`, `add_mco_coins` + **row simétrica** em `mcoin_transactions` (action `spaces.node.refund`) com `node_run_id` no context (chave da reconciliação KPI-SPACES-004). uid SEMPRE da row reclamada, nunca do caller. | D5/D7/C15. |
| S7 | **Escopo executável 1b**: `image-generator` → `generate_image` e `prompt-generator` → `magic_prompt`. **`image-upscaler` CORTADO da 1b** (o server não tem caminho real de upscale — `upscale-2x/4x` são cost-keys inalcançáveis); declarado no seal. Demais tipos: fontes/decorativos = no-op (nunca cobrados); geradores fora do slice (vídeo/áudio/svg/designer) → toast pt-BR "não suportado na Fase 1" + status `idle` (nunca `error`, nunca cobrado). | C12 + NA-SPACES-008. |
| S8 | **Mapa de modelos**: os 38 `IMAGE_MODELS` do Spaces são chaves Magnific SEM roteamento server. 1b resolve por `SPACES_MODEL_MAP` client-side: `auto` → `openrouter`/`google/gemini-2.5-flash-image` (10 mco); `flux.1.1` → `openrouter`/`black-forest-labs/flux-1.1-pro` (12 mco). Chave fora do mapa → resolve como `auto` (Pattern #2 Routing mínimo) e o `estimateCost` do HUD usa o preço do `auto` como fallback (estimativa = cobrança). A row `generations.model_key` grava a chave **resolvida** (`provider/model` — verdade do server). | C11. |
| S9 | **Status transitório não persiste**: o serializer da Fase 1a passa a resetar `pending/running` → `idle` ao persistir `spaces.graph` (reload nunca hidrata run fantasma). `done/error/blocked` podem persistir (sinal histórico). | C14 — sem isso viola G1 da SOP 1a. |
| S10 | **Batch N = N execuções independentes** do mesmo nó (cada uma com `node_run_id` e row próprios, sequenciais). Estimativa `base × batch` = cobrança real. NUNCA reusar o batch nativo do provider (hazard Soul paga-4-entrega-1, C18). | C18. |
| S11 | **Threading de inputs (convenção single-output 1b)**: edge chegando no handle `prompt` + upstream com geração `done` de texto → o texto vira o prompt do filho (fallback: prompt próprio); edge no handle `reference` + upstream `done` de imagem → `reference_image_urls=[url]`. A saída de texto mora em `generations.result` (jsonb — divergência aditiva D8 do stub, precedente `vision_jobs.result`); imagem mora em `creative_assets`/URL. Multi-output = diferido com os nós de vídeo. | C20. |
| S12 | **Billing segue o precedente vivo**: cobra `CREDIT_COSTS` mesmo com chave BYOK do tenant (todo canvas-execute já é per-user BYOK e cobra — mcoCoins é cobrança de valor de plataforma). "BYOK isenta débito" (BR-SPACES-006) contradiz o precedente do ecossistema inteiro → registrado como errata/OPEN de BoK no seal; `data.byok` fica dormant. | C17. |
| S13 | Colunas mco em `numeric` (semântica BoK); todos os custos atuais são inteiros — o cast `::integer` do ledger é latente-only (comentado na migration). | D6. |

## Sequence

1. **Montar o grafo** (Fase 1a): nós `prompt-generator` e/ou `image-generator` conectados por portas
   tipadas; parâmetros no HUD (modelo, prompt, proporção, batch).
2. **Dry-run (estimar)**: botão "Estimar" → `projectGraphCost()` client-side → toast
   *"Simulação — {n} mcoCoins projetados (sem débito)."* → **zero chamadas de servidor** (BR-SPACES-005).
3. **Run ▶**: `useSpaceSession.ensureFresh()` (sessão expirada → 1 refresh; falha → toast + aborta);
   `getTopologicalLayers(nodes, edges)` (Kahn — ciclo → erro pt-BR); por camada, nós executáveis em
   paralelo (`Promise.allSettled`); por nó gerador: status `pending`→`running` → invoke
   `canvas-execute` `{...payload legado, space_id, node_run_id}` → `done|error` →
   `invalidateQueries(['generations', nodeId])`.
4. **Servidor (branch Spaces)**: JWT → guards 422 (prompt) → 402 saldo/teto (strings canônicas) →
   `begin_space_generation` (S1/S2) → provider (1 retry, backoff fixo 5s) → sucesso:
   `finalize_space_generation('done', refund=0, asset_id, result, usd, latency)` +
   `register_creative_asset` fail-soft; falha: `finalize_space_generation('error', refund=mco_charged)`
   + `infra_health_logs{event:'spaces_run_failure'}`.
5. **Falha parcial**: nó `error` → descendentes `blocked` (BFS pelas edges de saída); ramos
   independentes continuam; `runState` final = `partial|done`.
6. **Cluster**: `useInfiniteQuery(['generations', nodeId])` — ≤24 cards/página, cursor `created_at`
   DESC, `staleTime` 60s; card mostra preview, modelo, `mco_charged`, `refunded_mco` (se estorno),
   status, timestamp. Re-run ADICIONA, nunca sobrescreve (FR-SPACES-012).
7. **Primeira geração `done` de um Space** → nó `observation` `spaces-first-run-<spaceId>` na
   Knowledge Mesh, **fail-open** (nunca bloqueia o run — PROC-SPACES-008).

## Verification gates

| Gate | Critério material |
|---|---|
| G1 — ledger-first atômico | `begin_space_generation` com saldo insuficiente → EXCEPTION do deduct → **zero row** em `generations` (rollback provado); com saldo → row `running` + débito na mesma tx (row de `mcoin_transactions` action `spaces.node.run` com `node_run_id` no context). |
| G2 — idempotência | 2ª chamada com o MESMO `node_run_id` → `duplicate:true`, **zero segundo débito** (saldo intacto entre as duas chamadas — provado por SELECT). |
| G3 — refund idempotente | `finalize('error', refund)` → saldo restaurado + row simétrica `spaces.node.refund`; 2ª chamada de finalize na mesma row → no-op (`finalized:false`), sem double-refund. CHECK `mco_refunded ≤ mco_charged` no schema (anti-mint). |
| G4 — guards zero-custo | 401 sem JWT · 402 saldo · 402 teto · 422 prompt-guard → **nenhuma** row nova em `generations` e saldo intacto. |
| G5 — tenant | `generations` RLS SELECT-own only (sem policy de INSERT/UPDATE/DELETE p/ authenticated); FK composta `(space_id, owner_id)` → geração nunca aponta pro space de outro tenant; RESTRICTIVE no-delete. `/security-review` obrigatório na migration. |
| G6 — smoke antes de run pago | O smoke zero-cost (G1-G5) passa ANTES de qualquer run pago real (FMEA-SPACES-001, 08:153). |
| G7 — UI honesta | Estimativa do HUD = cobrança real p/ o conjunto executável (mirror-parity dos keys do S8); nó não-suportado nunca cobra nem vira `error`. |

## Recovery path

- **Provider falhou (após retry)**: finalize `error` + refund total automático (S6) — nunca "tente de novo" sem estorno.
- **Run travado** (`running` > 30 min — crash do edge fn entre begin e finalize):
  `scripts/self-heal-spaces.sh` (on-demand, SEM cron novo — 07:182) marca `error` + refund
  idempotente via `finalize_space_generation`. NUNCA re-cobrar. **Guard do sweep
  (/security-review 2026-07-02):** só estorna rows SEM valor entregue (`result IS NULL AND
  asset_id IS NULL`) — row entregue-mas-finalize-falhou é materializada pelo done-fallback do
  edge fn e nunca é estornada. O edge fn reporta `refund_pending:true` (não `refunded`) quando
  o estorno não confirmou commit — a resposta nunca mente sobre o ledger (Lei 1).
- **Duplicidade suspeita**: reconciliar `mcoin_transactions` (actions `spaces.node.run`/`spaces.node.refund`,
  join por `context->>'node_run_id'`) × `generations` — invariante KPI-SPACES-004: Σ débitos = Σ `mco_charged`
  de rows não-estornadas; violação = P0 freeze.
- **Sessão expirada no meio do run**: nó atual → `error` (com refund server-side se já debitado);
  cliente tenta `refreshSession()` 1×; camadas seguintes abortam com toast.

## Success signal

Sovereign roda ▶ num grafo `prompt-generator → image-generator`; débito visível no HUD de mcoCoins;
cluster do nó mostra o card com a imagem + `mco_charged`; row em `generations` (UUID citável) com
`status='done'` e `mcoin_transactions` batendo; Vision-QA APROVADO no print 1920×1080.

---

## Amendment Fase 2a — vídeo async no slice (2026-07-02, ANTES do código)

> Estende o slice executável com `image_to_video` (Fase 2 "breadth" — SDD §10.3). O ciclo de vida
> async exige decisões novas porque o finalizador NÃO é a request do submit — é o webhook.

| # | Decisão | Racional |
|---|---------|----------|
| S14 | **Vídeo async é ledger-first no SUBMIT**: `begin_space_generation` (débito, `output_type='video'`, `status='running'`) roda ANTES do submit ao Higgsfield. Submit falhou (rede/4xx/5xx/sem request_id) → `finalize_space_generation(error, refund total)` na MESMA request + resposta honesta 502 (`refund_pending` se o estorno não confirmar). Submit ok → resposta `202 {generation_id, status:'queued'}`; quem finaliza é o webhook. | Espelha S1; o débito nunca fica sem row e a row nunca fica sem débito. |
| S15 | **Correlação webhook tenant-safe = HASH do token na row**: colunas novas `generations.webhook_token_hash text` (UNIQUE parcial, nullable — só runs async mintam) + `generations.operation_id text`. O submit minta o token server-side (CSPRNG), guarda **só o SHA-256** na row e baked o plaintext na URL (`?spaces_token=`). O webhook hasheia o token recebido e resolve a row pelo hash (single-row lookup no índice UNIQUE); NUNCA aceita `node_run_id`/ids vindos de URL/corpo — anti cross-tenant injection. **Hash (não plaintext) porque a RLS SELECT-own exporia o token ao próprio dono**, que poderia forjar failure-callback do próprio run (refund + vídeo tardio de graça) — precedente PAT vision-mcp. Replay-guard = claim do finalize (`status IN ('pending','running')`): 2º POST → no-op. `vm_canvas_executions` NÃO é usada (FK `project_id NOT NULL → vm_canvas_projects` a torna estruturalmente inutilizável p/ Spaces). | Mesma razão do `webhook_token` legado, sem herdar a tabela errada nem vazar segredo via RLS. |
| S16 | **Supressão do dinheiro legado no webhook**: o branch Spaces do `higgsfield-webhook` NÃO chama `deduct_mco_coins` (débito já ocorreu no begin — chamar de novo = double-charge, o P0 da OTD-VA-010) e NÃO escreve `vm_canvas_assets`/`updateProjectGraph` (grafo Spaces vive em `spaces.graph`). Sucesso pós-upload → `finalize(done, refund 0, result={video_url, storage_path})`; vídeo no bucket privado `canvas-assets` (mesmo path-shape legado, prefixo = space_id). Falha/NSFW/cancel → `finalize(error, refund total)`. `asset_id → creative_assets` = follow-up declarado (spine), não bloqueia a 2a. | Anti double-charge estrutural. |
| S17 | **Sweep cobre async**: `running` > 30 min sem webhook → refund pelo sweep (S6/guard de valor). Webhook TARDIO pós-sweep → claim falha → no-op (vídeo entregue com refund mantido = generosidade limitada e logada; NUNCA re-cobrança). DoP real ~2-6 min ≪ 30 min. | First-finalizer-wins já selado (S6). |
| S18 | **Guards 422 do vídeo (pré-débito)**: `provider === 'higgsfield'` + modelo ∈ allowlist 1:1 com os `ALLOWED_VIDEO_MODELS` legados (dop-lite/turbo/standard, kling-2.1-pro, seedance-v1-pro) + `input_asset_url` obrigatório (sem ele o submit falharia DEPOIS do débito) + `duration ∈ {5,10}` default 5. Custo = `CREDIT_COSTS["higgsfield/<model>-<duration>s"]` (chaves 10s ausentes hoje ⇒ fallback 10 do lookup legado NÃO se aplica ao Spaces: duration sem chave de custo → 422, estimativa=cobrança G7). | C12 lição: nunca cobrar caminho sem preço declarado. |

**Gates novos (verification):**
- **G8** submit-fail → row `error` + refund total + `mcoin_transactions` simétrica (zero cobrança líquida).
- **G9** webhook failure/NSFW → finalize(error, refund total) idempotente.
- **G10** webhook success (payload com `result_url` real) → download+validação (≥100KB, `video/*`) → upload bucket → `done` + `result.video_url` + **zero** `deduct_mco_coins` novo no ledger (a única txn é a do begin).
- **G11** replay do webhook (2º POST mesmo token) → `{finalized:false}` no-op, zero mutação de saldo.
- **G12** token inválido/ausente → 400 (malformado)/404 (desconhecido) sem vazamento de existência.

**Recovery path (delta):** webhook perdido → sweep 30min refund (S17). Webhook com payload sem
`result_url` → trata como falha (refund) — nunca `done` sem vídeo material (Lei 1).

**Success signal (2a-server):** smoke zero-cost prova G8-G12 com webhook simulado (payload forjado +
vídeo fake hospedado) SEM nenhuma chamada Higgsfield; E2E pago real (~30 mco + ~$0.13 BYOK) fica
para a fatia 2a-cliente com nota de GO.

### Amendment 2a-cliente (2026-07-02, ANTES do código do cliente)

| # | Decisão | Racional |
|---|---------|----------|
| S19 | **Semântica de run async no cliente**: `runState` do grafo = *dispatch completo* (o Run button libera quando todas as camadas dispararam). Nó de vídeo fica `running` após o 202/queued; um **poller** (5s, teto 12min — FR-SPACES-013 padrão polling) lê a própria row `generations` (RLS own) e flipa o nó p/ `done`/`error` + invalida o cluster. Timeout do poller → nó permanece `running` com toast honesto ("processando — o cluster atualiza ao concluir"); o sweep S17 cobre o caso travado. | Não bloquear o run inteiro por um render de minutos; a verdade continua server-side. |
| S20 | **Threading imagem→vídeo (extensão S11)**: edge chegando no handle **`first-frame`** do `video-generator` + upstream com geração `done` de imagem → vira `input_asset_url`. Vídeo SEM first-frame conectado (ou upstream sem imagem done) → nó pulado como no-op com toast específico (nunca cobrado — o guard 422 do server é o backstop). Prompt continua obrigatório (motion prompt). | O handle first-frame é semanticamente o frame inicial do image_to_video (DoP). |
| S21 | **Batch de vídeo = 1 no slice 2a** (estimativa e execução ignoram `batch` p/ video-generator; S10 continua valendo p/ imagem). Vídeo custa 30-160 mco/run — batch acidental de 8 seria um débito de até 1.280 mco. Batch de vídeo volta com a Fase 2 breadth se houver demanda. | Proteção de débito acidental > conveniência. |
| S22 | **Custo do vídeo no HUD = espelho 1:1 do server** (`SPACES_VIDEO_COSTS` client = `CREDIT_COSTS['higgsfield/<model>-5s']`), coberto pelo teste mecânico de mirror-parity que parseia o fonte do edge fn (mesmo padrão SOL-SPACES-001 da 1b). Estimativa = cobrança (G7). | Zero drift silencioso de preço. |

**Gate novo:** **G13** — vitest prova: classify(video-generator)=executable · estimate 1:1 com CREDIT_COSTS · payload com `input_asset_url` do first-frame · skip sem first-frame · batch ignorado p/ vídeo.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

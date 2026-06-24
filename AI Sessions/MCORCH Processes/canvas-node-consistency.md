# SOP — Canvas Node Consistency (Reference Threading + Seed Lock)

**Versão:** v1.1 · **Selada:** 2026-05-29 · **Atualizada:** 2026-05-30 · **Lei 2 (Processo Antecipado)** · **Canvas Studio Phase 4.3**
**Validação técnica:** `.claude/context/canvas-consistency-validation-2026-05-29.md`

> **v1.1 (2026-05-30) — Graph seeding:** `scripts/canvas-campaign-build.ts` agora **persiste o grafo do projeto** (`vm_canvas_projects.graph`) além de gerar os assets. Antes o builder criava `vm_canvas_assets` mas deixava `graph.nodes=[]` → o projeto abria **em branco** no painel apesar de ter creatives (assets órfãos do grafo). Agora `buildCampaignGraph()` monta `base → variação → vídeo` (`generateImage` + `imageToVideo`) com as imagens/vídeo já gerados anexados via `data.output.{imageUrl,videoUrl}` e handles corretos (`output_image`/`input_prompt`/`input_image`); `persistGraph()` faz UPDATE preservando lanes/styleSettings (`pipelineMode=false`). Idempotente (reusa assets via `findExistingAsset` → zero gasto). Backfill executado nas 3 campanhas existentes (Roborock/Samsung/Family Hub → 3 nós · 2 edges cada). **Verificação:** os 3 projetos abrem no painel mostrando o pipeline com os creatives reais.

## ORO triplet
- **Operator:** end user no Canvas Studio (conecta nós e executa Run); admin (validação/campanhas)
- **Reviewer:** Sovereign (aprova consumo de crédito pago + valida fidelidade visual)
- **Owner:** Sovereign (dono dos créditos Higgsfield/OpenRouter + qualidade do conteúdo monetizável)

## Contexto

O propósito do Canvas Studio é produzir **conteúdo visualmente consistente** ao longo de uma
cadeia de nós conectados: o mesmo personagem/produto/estilo deve persistir de uma geração à
seguinte. Hoje a saída de imagem do nó upstream **não é enviada como referência** ao gerador do
nó downstream — cada geração parte só do texto. Esta SOP define como a imagem upstream e um
**seed travado** fluem pela cadeia para garantir identidade visual.

**Por que existe:** sem consistência, os criativos de uma campanha (imagem do produto → variações →
vídeo) divergem visualmente → inutilizáveis para monetização afiliada séria. Consistência é o
diferencial do módulo.

## Operador humano equivalente (o que automatizamos)

Um designer hoje: gera a imagem-mãe do produto; baixa-a; ao gerar a próxima variação, **anexa a
imagem-mãe como referência** no modelo (Nano Banana/edits) e mantém o mesmo seed; repete; ao final
usa a melhor imagem como frame inicial do vídeo. Automatizamos exatamente esse "anexar referência +
travar seed" ao longo das conexões do grafo.

## Sequence — fluxo de consistência

| # | Action | Output esperado | Verification gate |
|---|--------|-----------------|-------------------|
| 1 | Nó A (GenerateImage) gera com seed S; asset salvo em `vm_canvas_assets` (`node_id`, `public_url`) | URL pública + `vm_canvas_assets.id` | `SELECT public_url, node_id FROM vm_canvas_assets WHERE node_id='A'` |
| 2 | Nó B conectado downstream de A: o pipeline coleta `public_url` do(s) upstream conectado(s) → `reference_image_urls[]` + propaga seed S | payload de B contém `reference_image_urls` não-vazio + `seed=S` | log do request / `input_asset_id` em B |
| 3 | Backend roteia a referência ao dialeto do provider (Gemini `image_url` parts · Replicate `image`+`seed` · Soul compose `image_1`) | request ao provider inclui a imagem de referência | resposta do provider = imagem (não texto) |
| 4 | Asset de B salvo com `input_asset_id = A.asset.id` (linhagem C3) | linhagem pai→filho | `SELECT input_asset_id FROM vm_canvas_assets WHERE node_id='B'` = A.asset.id |
| 5 | Avaliação de fidelidade: comparar B vs A (mesmo sujeito/identidade) | identidade preservada | inspeção visual do Reviewer OU score heurístico |

## Mecanismo por provider (alavanca A — reference threading)

| Provider/modelo | Como a referência entra | Seed |
|-----------------|--------------------------|------|
| OpenRouter / Gemini Nano Banana | `image_url` parts no `content` (até 4 p/ personagem) | n/a (multi-turn / referência) |
| Replicate / FLUX·SDXL | `input.image` (img2img) + `prompt_strength` | `input.seed` (int) |
| Higgsfield / Soul compose | `image_1_url` (upstream = identidade) | n/a |
| Higgsfield / Soul standard | sem suporte público → **fail-open** (gera só por texto + aviso) | n/a |
| OpenAI / gpt-image-1 | `/images/edits` + `input_fidelity:"high"` (**DEFERIDO** — OTD-CONS-004) | n/a |

**Invariante fail-open:** sem `reference_image_urls` → comportamento idêntico ao atual (zero regressão).

## Verification gates (Lei 1)

```bash
# Gate 1/4 — asset + linhagem
curl -s "$SUPABASE_URL/rest/v1/vm_canvas_assets?node_id=eq.<B>&select=id,public_url,node_id,input_asset_id" \
  -H "apikey: $KEY" -H "Authorization: Bearer $KEY"
# input_asset_id deve == id do asset do nó A

# Gate 3 — provider devolveu imagem (não texto)
# canvas-execute retorna { status:'done', asset_url } e NÃO { error:'...sem image_url' }
```

## Recovery path

| Falha | Detecção | Ação |
|-------|----------|------|
| Provider devolve texto em vez de imagem (prompt instrucional) | erro "resposta multimodal sem image_url" | Magic Prompt + guard de prompt (já existe v6.8.6) |
| Referência `data:` URI estoura payload | erro 413/timeout | usar sempre `https` URL do bucket `canvas-assets` (OTD-CONS-003) |
| Soul standard ignora referência | imagem diverge | trocar nó para Nano Banana (OpenRouter) ou Soul **compose** |
| Reference URL expirada (signed 7d) | 403 no fetch da referência | re-gerar signed URL antes de enviar |

## Success signal

Cadeia A→B→…→Vídeo produz assets com `input_asset_id` encadeado E identidade visual preservada,
confirmada pelo Reviewer. Crédito pago só consumido em geração `completed` + upload OK (invariante
herdado de `canvas-video-async-execution.md`).

## Budget de crédito (diretiva Sovereign 2026-05-29)

160 créditos Higgsfield disponíveis. **~30-50% (≈48-80 cr) reservados para testes**; resto para
monetização real após validação. Estratégia: imagens consistentes via **Nano Banana (OpenRouter,
centavos)**; Higgsfield DoP (9 cr) só no passo de **vídeo**. Alvo de teste: 3 produtos × 1 vídeo DoP
= 27 cr, preservando margem.

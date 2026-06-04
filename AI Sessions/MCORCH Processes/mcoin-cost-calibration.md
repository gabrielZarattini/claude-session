# SOP — mcoCoins Cost Calibration (OTD-MCOIN-CALIBRATION)

> **Lei 2 (Processo Antecipado).** Como precificar uma operação em mcoCoins a partir do custo $ real,
> em vez de um número redondo. Selado em 2026-06-03 (decisão Sovereign: "modelo 4×, fix IMAGE_GENERATION").
> SSOT dos valores: [`src/lib/billing.ts`](../../src/lib/billing.ts) → `COIN_COSTS`.

---

## O modelo

```
mco(op) = ceil( real_cost_usd(op) / USD_PER_MCO_FLOOR × MARGIN )
```

| Lever | Valor (2026-06-03) | Quem decide | Por quê |
|-------|--------------------|-------------|---------|
| `USD_PER_MCO_FLOOR` | **$0.018/mco** | Sovereign (pricing) | A **venda mais barata** do mcoCoin = pior caso de margem. Enterprise R$997 / 10000 mco ÷ R$5.5/USD. |
| `MARGIN` | **4×** | Sovereign (Owner) | Markup bruto alvo no preço de venda mais baixo. |
| `FX` | **R$5.5/USD** | Sovereign | Premissa de câmbio; revisar se BRL sair de R$5–7. |

**Por que o piso é o Enterprise, não o Starter:** o desconto de volume é íngreme —
Starter R$147/500 = **R$0.294/mco** ($0.053) · Pro R$397/2000 = **R$0.199/mco** ($0.036) ·
Enterprise R$997/10000 = **R$0.0997/mco** ($0.018). Calibrar no piso garante margem em **todos** os planos.
(Preços de plano: [`src/pages/BillingPage.tsx`](../../src/pages/BillingPage.tsx).)

---

## Custos reais medidos (2026-06-03)

| Componente | Provider / modelo | Custo $ real | Fonte |
|------------|-------------------|--------------|-------|
| Texto (artigo/post/thread) | llama-3.3-70b (Groq ~free / OpenRouter $0.10·$0.32/M) | **~$0.001** por geração | OpenRouter `/api/v1/models` live |
| Imagem | DALL·E 3 1024² standard | **$0.04** | OpenAI pricing · `generate-image:82` model `dall-e-3` |
| Orchestrate run | 3 textos + 1 imagem | **~$0.04** | soma (imagem domina) |
| Vídeo | Higgsfield DoP 5s (9 hf credits) | **$0.56** | `canvas-execute:34` + smoke pago |

---

## COIN_COSTS calibrado + markup no piso Enterprise

| Operação | mco | Custo $ | Markup @ floor | Nota |
|----------|-----|---------|----------------|------|
| `ORCHESTRATION_RUN` | 10 | $0.04 | **4.4×** ✓ | flat (bundle: 3×CONTENT + IMAGE = 15, vendido a 10) |
| `CONTENT_GENERATION` | 2 | ~$0.0006 | enorme | piso conservador (estrito = 1) — **era 5** |
| `IMAGE_GENERATION` | **9** | $0.04 | **4.4×** ✓ | **era 3 = 1.36× (sub-margem) → corrigido** |
| `EMBED_NODE` | 1 | ~$0.000002 | enorme | piso mínimo |
| `LEAD_SCORE` | 1 | ~$0.0005 | enorme | 1 call de scoring |
| `CAMPAIGN_RUN` | 10 | $0 direto | n/a | **fee** de orquestração (valor/coordenação), não custo de provider |
| `NURTURE_DISPATCH` | 2 | ~$0.0006 | enorme | 1 geração de mensagem |
| `canvas_video_spend` | 125 | $0.56 | **4.0×** ✓ | `canvas-execute` (validado, sem mudança) |
| `canvas_image_spend` | 12 | $0.04 | **5.4×** ✓ | `canvas-execute` (validado, sem mudança) |

**Achado-chave:** o `10` e o `125` que pareciam arbitrários já eram **~4×** sobre o custo real no piso.
A OTD fechou validando-os; o único furo genuíno era `IMAGE_GENERATION` (3 → 9).

---

## Operator / Sequence / Verification / Recovery / Success

- **Operator** — MCORCH Agent mede o custo $ real; **Sovereign** (Owner) fixa `MARGIN` + `FX` + `USD_PER_MCO_FLOOR`.
- **Sequence** (ao adicionar/recalibrar uma op):
  1. Medir `real_cost_usd(op)` material — preço por-token do provider (OpenRouter `/models`) × tokens, ou preço fixo (imagem/vídeo).
  2. Aplicar a fórmula com o piso/margem/FX vigentes → `ceil`.
  3. Editar `COIN_COSTS` em `src/lib/billing.ts` **E** o mirror hardcoded no edge fn correspondente (Deno não importa src/lib).
  4. Atualizar `src/test/billing.test.ts` (asserts dos valores).
- **Verification gates:** `npx tsc --noEmit` exit 0 · `bun run test src/test/billing.test.ts` verde · markup ≥ `MARGIN` no piso recomputado.
- **Recovery (margem afunda):** se um provider subir de preço OU o FX passar de R$7, recomputar a op afetada e subir o mco;
  nunca deixar uma op < 1× no piso (venderia no prejuízo no Enterprise).
- **Success signal:** todo `COIN_COSTS[op]` ≥ `ceil(custo_usd/floor × 1)` (nunca no prejuízo) e o alvo é `× MARGIN`;
  edge fn mirrors em sincronia; suíte verde.

---

## Mirrors hardcoded (manter em sincronia — Deno não importa `src/lib`)

| Constante | Edge fn | Linha |
|-----------|---------|-------|
| `CAMPAIGN_RUN` (10) | `supabase/functions/campaign-run/index.ts` | `CAMPAIGN_RUN_COST` |
| `ORCHESTRATION_RUN` (10) | `supabase/functions/orchestrate-content/index.ts` | `ORCHESTRATION_COST` |
| `NURTURE_DISPATCH` (2) | `supabase/functions/nurture-dispatch/index.ts` | `DISPATCH_COST` |
| `LEAD_SCORE` (1) | `supabase/functions/lead-score/index.ts` | (inline) |

> `IMAGE_GENERATION`/`CONTENT_GENERATION` **não** têm caminho de cobrança em produção hoje (orchestrate cobra flat 10) —
> são catálogo/teste. Se forem ligados a uma cobrança, criar o mirror no edge fn na mesma hora.

---

## Decisões abertas (pricing — Sovereign)

- **Desconto de volume** (Enterprise a 1/3 do Starter) é o que comprime a margem para o piso de $0.018 — revisar se quiser
  mais folga em todos os planos. Fora do escopo da calibração de custo (é decisão de pricing de plano).
- **FX dinâmico:** hoje premissa fixa R$5.5; se quiser, ancorar num oracle de câmbio e recomputar `USD_PER_MCO_FLOOR`.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

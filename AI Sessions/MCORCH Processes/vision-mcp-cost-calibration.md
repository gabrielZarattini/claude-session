# SOP — Vision MCP Cost Calibration (mcoCoins por tool)

> **Lei 2 (Processo Antecipado) + OTD-VM-004 (FECHÁVEL 2026-06-15).** Espelha `docs/processes/mcoin-cost-calibration.md`.
> Sela a unit economics das tools do `vision-mcp` no modelo **4×-floor** com custo real **fonteado por provider** (deepsearch verificado adversarialmente). Calibrar **antes** de rodar a 1ª transação econômica (a lição do flywheel: nunca cobrar a preço inventado).

## Modelo (idêntico ao [[mcoin-cost-calibration|mcoin-cost-calibration]])

```
mco(tool) = ceil( custo_usd_real(tool) / $0.018 × 4 ) = ceil( custo_usd_real / $0.0045 )
```
`$0.018/mco` = piso Enterprise (R$997 / 10000 mco). Margem **4×**. Floor absoluto = **1 mco** (nada cobra 0 exceto poll/scan grátis por design).

## Operator
MCORCH Agent (Engineering) calibra; Sovereign aprova qualquer mudança de classe. Owner: Sovereign.

## Tabela de unit economics — datada 2026-06-15 (fonte por linha)

| Tool | Custo USD real | Fonte | mco atual | mco 4×-floor | Veredito |
|------|----------------|-------|-----------|--------------|----------|
| `deepsearch.scrape` (Firecrawl) | $0.0006/pág (Growth) – $0.0032 (Hobby) | firecrawl.dev/pricing | 1 | 1 | NO-PISO (markup ~7.5× no Growth) — OK |
| `vision.ocr` (Mistral OCR 3) | $0.002/pág (standard $2/1k) · $0.001 (Batch) · PaddleOCR $0 API | mistral.ai/news/mistral-ocr-3 | 1/pág | 1 | NO-PISO (ceil(0.44)=1). Conflito $1-vs-$2 resolvido: standard vs Batch |
| `vision.describe_image` (VLM) | $0.0001 (Qwen3-VL-8B) – $0.0004 (Gemini Flash) – $0.007 (Claude Opus 4.7) /img 1024² | blog.roboflow.com/image-token-cost-vlm | 2 | 1 (barato) – 2 (premium) | NO-PISO p/ premium; manter 2 = mínimo conservador + hedge |
| `vision.detect` (Gemini boxes) | $0.0004–0.002 (= custo de 1 imagem, sem tarifa extra) | ai.google.dev/gemini-api/docs/image-understanding | 2 | 1 | OVER-MARGINED (headroom defensável; baixar p/1 opcional) |
| `vision.segment` (SAM) | $0.005/req (fal.ai SAM3) · $0.017/run (Replicate SAM2) | fal.ai/models/fal-ai/sam-3 · replicate.com/meta/sam-2 | 2–5 | 2 (fal) – 4 (Replicate) | **COST-AWARE obrigatório** (abaixo) |
| `vision.analyze_video` (Gemini) | $0.0054/min (Flash @1FPS) · $0.0018 (Flash-Lite) | ai.google.dev/gemini-api/docs/video-understanding | 2/min | 2 | NO-PISO (Flash ceil(1.2)=2) — OK |
| `mesh.search` / `deepsearch.poll` | ~$0 (RPC/leitura) | — | 0–1 / 0 | — | grátis por design |

**Veredito global (OTD-VM-004 CLOSEABLE):** a grade ATUAL sobrevive à auditoria — **nenhuma classe sub-margem**.

## Verification gates

| Gate | Critério |
|------|----------|
| G1 — sem under-floor | toda tool cobra ≥ ceil(custo/$0.0045) (tabela acima) |
| G2 — **segment cost-aware** (MUDANÇA OBRIGATÓRIA) | o edge fn cobra **2 mco só se backend=fal.ai SAM3**; **4-5 se Replicate SAM2**. **Anti-pattern banido:** cobrar 2 rodando Replicate = sub-margem 1.18× |
| G3 — espelhamento triplo | classes em `src/lib/billing.ts` (ou análogo do serviço) + constante hardcoded no container + asserção em `src/test/billing.test.ts` |
| G4 — medição em produção | no 1º run pago E2E, medir 1 chamada real de cada tool (padrão Higgsfield DoP 4×-validado) antes de cravar a constante final |

## Recovery / pendências (Lei 1 — só fonte, falta produção)
- Tokenização exata por imagem do VLM **default** (não selado no SDD — estimado 1.3-1.5k tokens p/ 1024² via tiles Gemini).
- Custo real de `detect` com N boxes (assumido = custo de 1 imagem pela doc Gemini; não medido).
- Infra amortizada/página do PaddleOCR self-host (API=$0; $/hora por throughput não calculado).
- Qwen3-VL-32B $0.104/M (confiança média — WebSearch, não fetch direto; o 8B $0.08/M confirmado).

## Success signal
Tabela datada no SDD §4.2/§5.1 + este SOP + `segment` cost-aware implementado + medição de produção registrada no 1º run pago. OTD-VM-004 fecha de CLOSEABLE→DONE quando G4 materializar.

---
_Anticorpo de OTD-VM-004. Espelha `mcoin-cost-calibration.md`. Gate research 2026-06-15 (workflow `wf_0040a939-232`)._

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

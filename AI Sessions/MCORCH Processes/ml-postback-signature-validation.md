# SOP — ML/Mercado Pago Postback Signature Validation

**Versão:** v1 · **Selada:** 2026-05-31 · **Lei 2 (Processo Antecipado)** · **FMEA-ML-003 / FMEA-ML-004**

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (gate na Edge Function `handle-ml-postback`)
- **Reviewer:** Sovereign (Gabriel)
- **Owner:** Sovereign (Gabriel) — blast radius = integridade financeira (receita forjada envenena o grafo de ROI que dirige gasto autônomo de anúncio).

## Contexto

`handle-ml-postback` roda com `verify_jwt = false` (Mercado Pago / painel de redirect não apresentam JWT Supabase). Sem validação, o endpoint é um gravador de dinheiro **público e forjável**: qualquer `POST` com `status=approved` + `commission` cria `revenue_cents`, soma `revenue_impact` e injeta a aresta `ATTRIBUTES_REVENUE_TO`. A autenticação passa a ser a assinatura **HMAC-SHA256 `x-signature`** do Mercado Pago (esquema oficial), com **fail-closed** + **idempotência por `order_id`**.

## Sequence — Validação de origem do postback

| # | Action | Output esperado | Verification gate |
|---|--------|-----------------|-------------------|
| 1 | Resolver o secret `MP_WEBHOOK_SECRET` do vault (global no piloto; per-user via `mercado_pago_config` — ver OTD-ML-MP-PER-USER) | string não-vazia | Secret ausente → `501 mp_webhook_secret_not_configured` (não processa) |
| 2 | Ler `data.id` da **query string**, `x-request-id` do header, `ts`/`v1` do header `x-signature` (`ts=<unix>,v1=<hex>`) | valores extraídos | `ts` ou `v1` vazio → `401 invalid_signature` |
| 3 | Montar manifest `id:<data.id minúsculo>;request-id:<x-request-id>;ts:<ts>;` (segmentos ausentes omitidos) | string canônica do MP | Bate com o doc oficial (mercadopago → Webhooks) |
| 4 | `HMAC-SHA256(manifest, secret)` em hex, comparação **constant-time** com `v1` | match exato | Divergência → `401 invalid_signature` + pulse `degraded` |
| 5 | Idempotência: se já existe observation com `metadata->>order_id == order_id` e `event=ml_conversion` | — | Duplicado → `200 idempotent_skip` (não re-credita — FMEA-ML-004) |
| 6 | Processar receita (update `affiliate_links`, soma `revenue_impact`, observation + aresta `ATTRIBUTES_REVENUE_TO`) | `200 ok` + pulse `healthy` | `infra_health_logs` healthy |

## Verification gates (Lei 1 — Materiality)

Vetor reproduzível (assina e testa o endpoint vivo):

```bash
SECRET="<MP_WEBHOOK_SECRET>"
TS="1730000000"; DATAID="123456789"; RID="test-req-id-001"
MANIFEST="id:${DATAID};request-id:${RID};ts:${TS};"
V1=$(printf '%s' "$MANIFEST" | openssl dgst -sha256 -hmac "$SECRET" | sed 's/^.*= *//')
URL="https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/handle-ml-postback?data.id=${DATAID}"
# Válido → 200 (status=cancelled = skipped, sem efeito colateral):
curl -s -w "\nHTTP:%{http_code}" -X POST "$URL" -H "x-signature: ts=${TS},v1=${V1}" -H "x-request-id: ${RID}" -H "Content-Type: application/json" -d '{"status":"cancelled"}'
# Adulterado / ausente → 401 invalid_signature
```

Resultado esperado: válido `HTTP 200`; v1 adulterado `HTTP 401`; sem assinatura `HTTP 401`.

## Recovery path

| Falha | Detecção | Ação | Resultado |
|-------|----------|------|-----------|
| Secret não configurado | `501` em todo postback | `npx supabase secrets set MP_WEBHOOK_SECRET=<segredo real do MP> --project-ref bcyvddsykvehvpwstlfa` | gate volta a validar |
| Todo postback legítimo dá `401` | secret do edge ≠ secret do MP dashboard | Alinhar o secret do vault com **Mercado Pago → Suas Integrações → Assinatura** e re-assinar a origem | assinaturas batem |
| Replay / double-credit | mesma `order_id` reincide | Idempotência (passo 5) responde `200 idempotent_skip` | receita não duplica |

## Success signal

- Assinatura válida → `HTTP 200`; adulterada/ausente → `HTTP 401`.
- `infra_health_logs` com `service='handle-ml-postback'` `healthy` no caminho feliz, `degraded` em rejeição.
- Aresta `ATTRIBUTES_REVENUE_TO` criada só para postbacks autenticados.

## Débito registrado

- **OTD-ML-MP-PER-USER** — migrar `MP_WEBHOOK_SECRET` global → `mercado_pago_config` per-user (`auth.uid()`, RESTRICTIVE no-delete) antes de Usuário 1 (API Tenancy Model). Bypass global autorizado para o piloto Usuário Zero.
- E2E do caminho resolvido (link real + assinatura real do MP) pendente — validar quando o piloto enviar o primeiro postback verdadeiro.

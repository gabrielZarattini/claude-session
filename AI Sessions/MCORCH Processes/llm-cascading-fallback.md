# SOP — LLM Cascading Fallback

**Versão:** v1 · **Selada:** 2026-05-31 · **Lei 2 (Processo Antecipado)** · **OTD-LLM-FALLBACK**

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (executa nas Edge Functions de completions)
- **Reviewer:** Sovereign (Gabriel)
- **Owner:** Sovereign (Gabriel) - Blast radius de custos e confiabilidade da geração de conteúdo.

## Contexto

A orquestração do Constellation Orchestra depende de completions confiáveis de LLM para gerar artigos, scripts, posts e planos. Se a conta do OpenRouter ficar sem saldo (retornando HTTP 402) ou sofrer com limites severos de requisição (retornando HTTP 429), o sistema deve migrar dinamicamente para o Gemini Free (via endpoint oficial do Google compatível com a API da OpenAI) e, em último caso, para modelos gratuitos do OpenRouter (OpenRouter Free).

## Sequence — Fluxo de Fallback de Completions

| # | Action | Output esperado | Verification gate |
|---|--------|-----------------|-------------------|
| 1 | Edge function intercepta chamada de completion e chama o helper `fetchLLMWithFallback` | Retorna Response com dados da API ou stream | Helper executa fetch primário |
| 2 | Chamada primária ao OpenRouter Pago falha com HTTP `402`, `429` ou erro de rede | Helper captura a falha e registra aviso no console | Console logs: "OpenRouter primary call failed. Falling back to Gemini Free." |
| 3 | Helper mapeia o modelo para Gemini correspondente (Heavy vs Light/Medium) | Modelo definido: `gemini-2.5-pro` / `gemini-1.5-pro` ou `gemini-2.5-flash` / `gemini-1.5-flash` | Mapeamento no log de depuração do Deno |
| 4 | Helper faz chamada secundária ao Gemini OpenAI-Compatible Endpoint com a chave de API resolvida | Retorna HTTP 200 com a resposta do Gemini em formato compatível com OpenAI (incluindo streams) | `Authorization` header contém `Bearer <GEMINI_API_KEY>`; corpo da resposta tem formato OpenAI |
| 5 | Se chamada ao Gemini falhar (HTTP diferente de 2xx ou rede offline) | Helper intercepta e loga falha secundária | Console logs: "Gemini fallback failed. Attempting OpenRouter Free fallback." |
| 6 | Helper faz chamada de último recurso ao OpenRouter usando o modelo gratuito `google/gemma-2-9b-it:free` | Retorna HTTP 200 com resposta do modelo gratuito | Modelo no payload alterado para `google/gemma-2-9b-it:free` |
| 7 | Se todas as tentativas falharem | Helper propaga o erro final estruturado HTTP 502 / 500 | Resposta JSON com `{ error: "All LLM providers failed in cascade" }` |

## Verification gates (Lei 1 — Materiality)

Comandos reproduzíveis e verificações de integridade:

```bash
# Verificar se o Gemini OpenAI-Compatible Endpoint está respondendo de forma saudável
curl https://generativelanguage.googleapis.com/v1beta/openai/chat/completions \
  -H "Authorization: Bearer $GEMINI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gemini-2.5-flash",
    "messages": [{"role": "user", "content": "Hello"}],
    "stream": false
  }'
```

## Recovery path

| Falha | Detecção | Ação | Resultado |
|-------|----------|------|-----------|
| **Gemini API Key Ausente** | `geminiKey` é nulo/indefinido | Helper pula direto para a tentativa de OpenRouter Free | Execução não quebra por falta de chave Gemini |
| **Timeout upstream** | Requisição fica travada > 30s | AbortController cancela a tentativa e aciona o próximo provedor na cascata | Resiliência contra travamento do OpenRouter ou Gemini |
| **Stream corrompida** | Erro de leitura de stream no meio da geração | Interrompe e lança erro ao cliente (não há como fazer fallback no meio de uma stream já iniciada) | Retorna erro HTTP parcial ao cliente de forma limpa |

## Success signal

- Chamada da Edge Function retorna HTTP 200 com resposta completa ou stream de texto.
- Telemetria de depuração no console do Deno detalhando qual etapa da cascata foi utilizada.
- Registros saudáveis em `infra_health_logs` para as funções correspondentes.

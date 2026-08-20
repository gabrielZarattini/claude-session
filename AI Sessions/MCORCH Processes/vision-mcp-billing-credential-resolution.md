# SOP — Vision MCP Fatia 2: Billing + Per-User Credential Resolution (container)

> **Lei 2 (Processo Antecipado) + API Tenancy Model + FR-VM-006.** Precede QUALQUER código das tools billable
> (`vision.describe_image`/`analyze_video`/`ocr`/`segment`/`detect`, `deepsearch.*`, `mesh.consolidate_reference`).
> O `vision-mcp` é um **container Node/TS** (não edge Deno) — não pode importar `_shared/agent-metering.ts`;
> reimplementa o MESMO contrato (cost-on-entry · BYOK-free · Sovereign-exempt · refund-on-failure). Espelha
> `docs/processes/affiliate-credential-resolution.md` + `docs/processes/vision-mcp-cost-calibration.md` (grade selada).

## ORO
- **Operator:** MCORCH Agent (Engineering) — implementa a camada `src/infra/billing.ts` + `src/auth/credentials.ts`.
- **Reviewer:** Sovereign + `/security-review` independente em qualquer migration nova (ex.: `firecrawl_api_key`).
- **Owner:** Sovereign — 1º serviço tenant-facing que **debita mcoCoins** + chama provider pago.

## Operator (quem executa hoje, manual)
Hoje o débito de mcoCoins é feito pelos edge fns (`orchestrate-content`, `lead-score`, `aeo-audit`) via
`deduct_mco_coins` com o JWT do user (auth.uid()=sub). O `vision-mcp` move esse papel para o container, que
**verifica o JWT ES256 ele mesmo** (FR-VM-002) e então atua com `SB_SECRET_KEY` (service-role) contra o `sub` verificado.

## Sequence (ordem materialmente verificada — probe `scripts/qa/probe-vision-mcp-fatia2-foundation.ts`)

1. **Identidade** — o `sub` SÓ vem do JWT ES256 verificado (AsyncLocalStorage). NUNCA do input do tool.
2. **Resolução de credencial de provider** (`resolveProviderKey(sub, provider)`):
   - Ler `decrypted_user_api_keys?user_id=eq.<sub>&select=<col>` com `SB_SECRET_KEY` (service-role — **probado READABLE 200**).
     Colunas vivas: `openrouter_api_key` (VLM/describe_image), `google_api_key` (Gemini video/grounding), `replicate_api_key`.
   - **BYOK** — se a coluna do user é não-nula → `{ key: <user>, isUserCustomKey: true }`. **Custo da tool = 0** (o user paga o provider direto). FR-VM-006: "BYOK anda de graça".
   - **Plataforma (default cobrado documentado)** — senão, usar a env global do container (`OPENROUTER_API_KEY`/`GEMINI_API_KEY`, injetadas via compose a partir do `.env`, NUNCA baked) → `{ key: <platform>, isUserCustomKey: false }`. Custo = classe mco da tool. (Este é o modelo mcoCoins-gatekeeper idêntico ao `orchestrate-content`: a env global é o **default compartilhado documentado** permitido pela API Tenancy, não o caminho primário escondido.)
   - **Hard failure** — se nem BYOK nem plataforma resolvem → **HTTP 402** estruturado `{ error: "<provider>_not_configured", action: "Configure sua chave em /dashboard/settings" }`. NUNCA seguir sem chave.
3. **Decisão de custo** (`costFor(tool, sub, isUserCustomKey)`):
   - `sub === SOVEREIGN_USER_ID` (`ada39fae-67e1-4e53-af1c-5a18e1c108e8`) → **0** (exempção).
   - `isUserCustomKey` → **0** (BYOK).
   - senão → `COIN_COSTS[tool]` (grade selada: describe_image 2 · ocr 1 · scrape 1 · run 3 · poll 0 · analyze_video 2/min · detect 2 · segment 2|4 cost-aware · consolidate_reference 1).
4. **Sentinel** — `inspectPrompt` sobre args textuais (question/query) DEPOIS da identidade, ANTES do débito (FR-VM-005a).
5. **Débito na entrada** (se custo > 0) — `deduct_mco_coins(sub, cost, 'vision.<tool>', {context})` (4-arg, service-role; **probado OK**). Saldo insuficiente → **HTTP 402** `insufficient_balance` ANTES de qualquer leg de provider.
6. **Leg de provider** — chamar o provider (OpenRouter VLM / Gemini / Firecrawl) com a chave resolvida.
7. **Refund-on-failure** — em QUALQUER falha pós-débito (provider erro, parse, persistência) → `add_mco_coins(sub, cost)` (service-role; **probado OK**; nunca lança). Espelha `_shared/billing.ts refundMco`.
8. **Metering/telemetria** — pulse `infra_health_logs service='vision-mcp'` (healthy/degraded). Detalhe rico → stderr (a tabela viva não tem `metadata` — follow-up migration).

## Verification gates (material)

| Gate | Critério |
|------|----------|
| G-CRED-1 | sem chave (per-user nem plataforma) → 402 `<provider>_not_configured` (nunca chama provider) |
| G-COST-1 | BYOK → cost 0, sem deduct; Sovereign → cost 0; plataforma → deduct da classe selada |
| G-402   | saldo < classe → 402 `insufficient_balance` ANTES do leg (nada debitado, nenhuma chamada de provider) |
| G-SENT  | injeção no arg textual → 403 sentinel, sem débito, sem leg |
| G-REFUND| falha forçada pós-débito (ex.: image_url inválida) → saldo restaurado (deduct N → refund N, net 0) |
| G-TENANT| qualquer escrita na malha (consolidate_reference) carrega `user_id = sub` verificado (nunca cross-tenant) |

## Recovery path
- Deduct OK mas leg falha → refund automático (G-REFUND). Se o refund em si falhar (RPC down), logar `degraded`
  em `infra_health_logs` + stderr com `sub`+`amount` para reconciliação manual; NUNCA mascarar como sucesso.
- Provider 429/5xx → erro estruturado + refund; o cliente MCP recebe `isError` in-band (não HTTP 500).
- Migration nova (ex.: `firecrawl_api_key`) → `/security-review` independente ANTES do commit (FMEA-011).

## Success signal
- Smoke zero-custo verde (G-CRED-1·G-COST-1·G-402·G-SENT·G-REFUND) + 1 leg real medido (sub-cent) provando
  débito atômico da classe + output estruturado + (consolidate) node `user_id=sub`. Tudo contra o CONTAINER servido (Lei 1).

## Anti-patterns proibidos
- ❌ Chamar provider antes do débito (cobra sem valor / valor sem cobrança).
- ❌ Usar env global de provider em fluxo user-facing **sem** tentar BYOK primeiro (viola resolução 2→1).
- ❌ Confiar em `user_id` do input em vez do `sub` verificado.
- ❌ Reportar sucesso com refund silenciosamente falho.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

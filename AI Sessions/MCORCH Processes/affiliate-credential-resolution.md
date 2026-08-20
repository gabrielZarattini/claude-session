# SOP: ML Affiliate Credential Resolution (Per-User)

**Status:** ACTIVE · v1.0 · 2026-05-30
**Owner:** Sovereign (Gabriel Zarattini)
**Survival Law 2 compliance:** Escrita ANTES do refactor fail-closed em `supabase/functions/process-affiliate-link/index.ts` (fecha OTD-OE661-PER-USER · RPN 120 · SLA 2026-06-02).
**Canonical directive:** `CLAUDE.md > Architecture > "API Tenancy Model — Per-User Credentials"`

---

## Context

A monetização via Mercado Livre resolve um **affiliate_id** (`affiliate_config.app_id`) para anexar a links de produto. Antes deste SOP, dois caminhos vazavam atribuição de receita para uma credencial **global compartilhada**:

1. **GET redirect** (`handleGetRedirect`, público no-JWT) — inicializava `affiliateToken` com `Deno.env.get("GCRUX_ML_AFFILIATE_TOKEN")` e só fazia fail-closed quando o token era o literal placeholder `"GCRUX_DEFAULT_TOKEN"`. Se o env global estivesse provisionado (foi, em v6.6.7), um asset SEM config per-user redirecionava usando o token global → **receita do clique creditada à conta afiliada errada**.
2. **POST monetize** (`ContentLibraryPage → "Monetizar Links ML"`, JWT-authed) — `affiliateId = config?.app_id ?? Deno.env.get("ML_AFFILIATE_ID") ?? null`, e seguia construindo o link mesmo com `null` (sem `partner_id`, atribuição perdida).

`scripts/link-forge.ts` **já** resolve per-user (carrega `affiliate_config` por `user_id`, pula com observation node quando falta) — fora de escopo deste fix.

**Por que importa (multi-tenant readiness):** atribuição de receita correta por tenant · isolamento de risco financeiro · LGPD (cada user controla/revoga sua credencial) · anti-fraude (um user não monetiza pela credencial de outro).

---

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (refactor) + Cron/Edge runtime (execução)
- **Reviewer:** Sovereign (Gabriel) — aprova o diff + valida o smoke
- **Owner:** Sovereign — blast radius = atribuição de receita ML por tenant + risco financeiro isolado

---

## Operator (quem executa manualmente hoje)

- **Usuário Zero / cliente:** configura suas credenciais ML em `/dashboard/affiliates` (hook `useAffiliateConfig` → INSERT `affiliate_config` `platform='mercadolivre'`, `is_active=true`, `app_id=<seu affiliate id>`).
- **Edge function `process-affiliate-link`:** resolve a credencial por request (GET click-through OU POST monetize) e atribui a receita ao dono do conteúdo.

---

## Resolution order (canonical — espelha API Tenancy Model)

| # | Camada | Fonte | Permitido em |
|---|--------|-------|--------------|
| 1 | **Per-user** | `affiliate_config` WHERE `user_id = <owner>` AND `platform='mercadolivre'` AND `is_active=true` → `app_id` | SEMPRE (caminho primário) |
| 2 | **Global vault fallback** | `Deno.env.get('GCRUX_ML_AFFILIATE_TOKEN')` / `ML_AFFILIATE_ID` | **PROIBIDO** em atribuição de receita user-facing. Reservado a cron/system/onboarding default explícito documentado. |
| 3 | **Hard failure** | — | GET → 302 `Location: /dashboard/settings?no_config=1` · POST → HTTP 402 `{ error: "mercadolivre_not_configured", action: "Configure your Mercado Livre credentials at /dashboard/affiliates" }` |

**Owner resolution (GET branch):** `contentVariantId` (= `mcorch_nodes.id`) → `node.user_id` → `affiliate_config` desse user. O redirect é público mas a receita pertence ao **dono do conteúdo**, não a quem clica.

---

## Sequence

### GET branch (`handleGetRedirect`)
1. Validar `product_id` + `content_variant_id` (400 se faltar).
2. SELECT `mcorch_nodes.user_id` WHERE `id = content_variant_id`.
3. Se `user_id` existe → SELECT `affiliate_config.affiliate_tag, metadata` per-user (camada 1).
4. Resolução **híbrida** (OTD-ML-001): (a) se `metadata.shortlinks[product_id]` for um short link `meli.la`/`/sec/` → 302 direto (atribuição cravada); (b) senão, com `affiliate_tag` → 302 para o `product_url` REAL (lookup `vm_affiliate_products`) + `matt_word=<affiliate_tag>` + UTMs + pulse `status=healthy`. **Nunca** `panel.gcrux.com`, **nunca** `app_id` como affiliate id.
5. Se NÃO resolveu (sem tag e sem short link) → 302 para `/dashboard/settings?no_config=1` + pulse `status=degraded reason=no_config` (camada 3). **Nunca** usar env global.

### POST branch (monetize)
1. JWT obrigatório → `user.id`.
2. SELECT `affiliate_config.affiliate_tag, metadata` WHERE `user_id = user.id` (camada 1).
3. Se NÃO resolveu (sem tag e sem short link p/ o produto) → HTTP 402 estruturado (camada 3). **Não** cair em `ML_AFFILIATE_ID` nem usar `app_id`.
4. Se resolveu → (short link cravado bypassa probe) ou probe + self-heal + `matt_word=<affiliate_tag>` → INSERT `affiliate_links` (`metadata.attribution = shortlink|matt_word`) + pulse `status=healthy`.

---

## Verification gates

| Gate | Check | Pass criterion |
|------|-------|----------------|
| G1 | User COM config → POST monetize | HTTP 200 · `affiliate_url` contém `partner_id=<app_id>` · row em `affiliate_links` |
| G2 | User SEM config → POST monetize | HTTP 402 · body `mercadolivre_not_configured` · ZERO row em `affiliate_links` |
| G3 | Asset COM config → GET redirect | 302 `Location` contém `affiliate_id=<app_id>` (≠ token global) |
| G4 | Asset SEM config → GET redirect | 302 `Location=/dashboard/settings?no_config=1` |
| G5 | Telemetria | `infra_health_logs.service='affiliate-link-resolution'` recebe pulse em cada path (healthy/degraded) |
| G6 | Zero global em path user-facing | `grep GCRUX_ML_AFFILIATE_TOKEN\|ML_AFFILIATE_ID` em `process-affiliate-link` → 0 refs em branch de atribuição |

---

## Recovery path

| Cenário | Detecção | Recovery |
|---------|----------|----------|
| User reclama "link sem comissão" | `affiliate_links.metadata.affiliate_id` null | Verificar `affiliate_config` ativo do user; reprocessar após configurar |
| GET 302 loop para settings | pulse `degraded reason=no_config` repetido | Confirmar que o asset tem `user_id` setado + config ativa do dono |
| Regressão (global reintroduzido) | G6 falha em CI/grep | Reverter; global só em cron/system documentado |
| `affiliate_config` lookup erro DB | `console.error` no edge log + pulse `status=error` | Fail-closed (camada 3), nunca fallback silencioso |

---

## Success signal (whole protocol)

- G1–G6 verdes no smoke.
- `process-affiliate-link` redeployado (script size + ACTIVE em `supabase functions list`).
- `infra_health_logs.service='affiliate-link-resolution'` com pulses recentes (`last_seen_at` < 1h pós-smoke).
- OTD-OE661-PER-USER fechada antes de 2026-06-02.

---

## Anti-patterns prohibited

- ❌ `Deno.env.get('GCRUX_ML_AFFILIATE_TOKEN')` / `ML_AFFILIATE_ID` em branch de atribuição user-facing.
- ❌ Construir affiliate URL com `affiliate_id=null` silenciosamente (atribuição perdida sem erro).
- ❌ Fail-closed só quando token == placeholder literal (deixa o env global setado vazar).
- ❌ Compartilhar receita/quota de um user com outro via credencial global (fraude por design).

---

## Connection to Survival Laws

- **Lei 1 (Materialidade):** cada gate produz prova material (HTTP status + body + `affiliate_links` row + pulse UUID).
- **Lei 2 (Anticipated Process):** este SOP escrito ANTES do refactor (requisito explícito da diretiva API Tenancy item 5).
- **Lei 3 (Pruning):** resolução stateless por request; nada acumulado em contexto.
- **Lei 4 (ORO):** triplet declarado acima; Reviewer = Sovereign aprova o diff antes do deploy.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

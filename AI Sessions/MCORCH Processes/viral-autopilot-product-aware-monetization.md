# SOP — Viral Autopilot: Product-Aware Generation + Cross-Surface Monetization (Fatia 1)

> **Lei 2 (Processo Antecipado).** Escrito ANTES do código. Cobre o caminho **user-JWT (sem cron)** —
> a geração disparada manualmente pelo "gerar agora" do Visual Orchestrator. O caminho de cadência/cron
> (FR-VA-005/007) é gated por um SOP irmão (`autopilot-cron-identity.md` — OTD-VA-008), fora desta fatia.
>
> **BoK SSOT:** `docs/bok/viral-autopilot/04-frd.md` (FR-VA-003 · FR-VA-004 · FR-VA-016 metade-produto ·
> FR-VA-009 · FR-VA-012) · `06-data-model.md` (creative_metrics). **Closes:** os buracos R1/R4 da auditoria
> de seal (monetização só no artigo via 3 SKUs hardcoded por regex; `affiliate_url`/produto da UI dropado;
> `content_id` sempre null; sem writer de métricas por criativo).

---

## O que esta fatia entrega (e o que NÃO entrega)

**Entrega:** o gerador de conteúdo (`orchestrate-content` → `orchestrate-step`) passa a, **quando o operador
escolhe produtos**, (a) gerar conteúdo viral de consumo focado no produto em destaque em **todas as 3
superfícies de texto** (artigo WP, post LinkedIn, thread X) em vez dos 3 prompts B2B genéricos; (b) monetizar
**todas** as superfícies com link rastreável per-owner do Mercado Livre (não só o artigo); (c) gravar
`affiliate_links.content_id = content_library.id` daquele criativo (antes `null`) habilitando atribuição por
peça; (d) escrever uma linha-baseline em `creative_metrics` por criativo (semente do loop R3).

**NÃO entrega (fatias seguintes):** imagem product-referenced (FR-VA-013 — não há passo de imagem no
pipeline hoje), cadência/cron (FR-VA-001/002/005/006/007/021), loop auto-melhorável que LÊ
`optimization_policy` (FR-VA-010/011), coletor real de engajamento (FR-VA-008), dashboard
(FR-VA-014/015), atribuição de compra (FR-VA-017).

---

## Operator — quem executa manualmente hoje

O **Usuário (tenant)** no Visual Orchestrator Canvas (`/dashboard/orchestrate`), nó **Trigger**:
1. Digita o tópico da campanha.
2. **Escolhe 1+ produtos** do catálogo verificado (`vm_affiliate_products`, gate `isListableProduct` =
   ativo + preço + `availability='available'`). O 1º selecionado é o **produto em destaque**.
3. Seleciona plataformas (WP/LinkedIn/X) e rascunho/publicar.
4. Clica **Executar Pipeline** (10 mcoCoins — bundle plano existente, sem novo débito).

Pré-requisito de monetização: o tenant tem `affiliate_config` (Mercado Livre) ativo com `affiliate_tag`.
Sem isso, a geração roda normalmente, **sem** links (fail-open — a monetização nunca quebra o pipeline).

## Sequence — ordem (cada step tem critério de sucesso material)

| # | Step | Sucesso material |
|---|------|------------------|
| 1 | UI envia `product_ids[]` (external_ids) para `orchestrate-content` | network body contém `product_ids` |
| 2 | `orchestrate-content` resolve produtos do `vm_affiliate_products` (`is_active`), **sanitiza cada nome pelo sentinel** (dado externo/Apify → injeção; nome bloqueado = produto pulado), preserva ordem da UI | `SELECT metadata->'products' FROM pipeline_runs WHERE id=<run>` mostra o set resolvido e sanitizado |
| 3 | Cada step de `orchestrate-step` (artigo/LinkedIn/X) lê `metadata.products`; se presente, usa prompt **product-aware viral** (gancho→valor→CTA, citando o produto em destaque) | `content_library.body` menciona o produto |
| 4 | Cada criativo é inserido em `content_library` (id capturado), monetizado por `monetizeForProduct` (link rastreável per-owner; `affiliate_links.content_id = content_library.id`), e o body atualizado | 3 linhas `affiliate_links` com `content_id` NÃO-null, uma por criativo |
| 5 | Por criativo, linha-baseline em `creative_metrics` (source `organic`, zeros) keyed por `content_variant_id` | 3 linhas `creative_metrics` keyed pelos `content_library.id` dos criativos |

## Verification gates

- `SELECT count(*) FROM content_library WHERE ...` = 3 criativos do run, cada um citando o produto.
- `SELECT content_id, product_id, short_url FROM affiliate_links WHERE user_id=<tenant> ORDER BY created_at DESC LIMIT 3`
  → 3 linhas, **`content_id` non-null** (o defeito-núcleo fechado), `short_url` é URL ML válida com `matt_word`.
- `SELECT content_variant_id, source, platform FROM creative_metrics WHERE user_id=<tenant>` → 3 linhas baseline.
- `mco_balance` delta do run = **exatamente 10** (sem cobrança extra pela monetização cross-surface).

## Recovery path — falha no step N

- **Produto não resolve / catálogo vazio:** geração cai no prompt B2B legado (sem produto). Pipeline sobrevive.
  Operator: verificar `vm_affiliate_products.is_active` e o picker.
- **Sem `affiliate_config`:** geração roda, monetização pulada (fail-open). Operator: configurar credencial ML em
  `/dashboard/affiliates`. Não há rollback — o run gera conteúdo não-monetizado (recuperável re-rodando após config).
- **`affiliate_links` insert falha:** o link cai no destino ML direto (fail-open de `monetizeForProduct`); `content_id`
  não grava. Operator: checar `infra`/logs; o criativo existe, re-monetizável.
- **`creative_metrics` insert falha:** fail-soft (`.then(ok, warn)`) — nunca quebra a geração; baseline pode faltar.
- **Nome de produto bloqueado pelo sentinel:** produto pulado (fail-closed por produto, não por run); log de aviso.
  Operator: revisar o nome enriquecido (Apify) do produto; pode ser falso-positivo de injeção.

## Success signal — materialmente observável

Um run "gerar agora" com 1+ produtos produz, para Usuário Zero:
**3 criativos** (artigo+LinkedIn+X), cada um (i) citando o produto OU com CTA de compra anexado, (ii) carregando
um **link ML rastreável** (redirect `?link_id=` per-owner), (iii) com `affiliate_links.content_id` = o
`content_library.id` daquele criativo, e **3 linhas `creative_metrics`** keyed por esses `content_variant_id`,
com **delta de carteira = 10 mcoCoins**.

---

## ORO

- **Operator:** MCORCH Master Execution Agent (código) · Tenant (dispara o run).
- **Reviewer:** Sovereign (Gabriel) + `/security-review` (migration `creative_metrics`) + revisão adversarial.
- **Owner:** Sovereign — blast radius = mudança de comportamento de geração + gasto de carteira no E2E +
  links monetizados publicados sob a conta do tenant.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

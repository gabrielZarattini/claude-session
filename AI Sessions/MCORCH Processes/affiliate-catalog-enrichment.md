# SOP — Affiliate Catalog Enrichment (Mercado Livre via Apify)

> **Anticorpo / Lei 2 (Processo Antecipado).** Sintetizado 2026-06-01 após provar materialmente que
> o ML bloqueia TODO acesso server-side (API 403/401, página → `/gz/account-verification`, headless
> "Hubo un error") — tanto da nossa IP quanto da IP da Supabase Edge. Logo, foto/preço/disponibilidade
> só vêm via um scraper com proxy residencial. Apify (`karamelo~mercadolivre-scraper-brasil-portugues`)
> furou o anti-bot e devolveu preço+imagem+SKU reais (Roborock `MLB27834876` → R$17770).

## Verdade material (validada 2026-06-01)
- `api.mercadolibre.com/{items,products,sites/MLB/search,sites/MLB/categories}` → **403/401** (PolicyAgent, IP-block).
- Página do produto (curl UA-browser) → **302 `/gz/account-verification`**; headless → "Hubo un error".
- Apify actor keyword-based devolve `eTituloProduto`, `novoPreco`, `imagemLink`, `zProdutoLink`, **`SKU`** (= MLB id), `Moeda`. **NÃO** devolve estoque/quantidade/status pausado.
- Disponibilidade ⇒ **proxy**: "o `SKU` ainda aparece na busca pelo nome?" Sim ⇒ `available`; não ⇒ `unavailable`. Não é contagem de estoque; é detecção de delisting/desativação. Toggle manual cobre bordas.

## Resolução de credencial (API Tenancy — em camadas)
1. **Per-user** (`user_api_keys.apify_token`, `auth.uid()`) — quando um tenant enriquece os próprios produtos (quota/custo isolados).
2. **Sistema/global** (`Deno.env.get('APIFY_TOKENS')` / `.env`) — fallback para o **catálogo compartilhado** (`vm_affiliate_products`) e crons (sem `auth.uid()`). Permitido pela exceção cron/system do API Tenancy Model.
3. **Hard failure** — sem nenhum dos dois → não enriquece; pulse `degraded`; mantém dados anteriores.

## SOP operacional

| Pergunta | Conteúdo |
|----------|----------|
| **Operator** | MCORCH Agent (cron/system) ou o tenant (UI Settings, BYOK). |
| **Sequence** | 1) Ler produtos `is_active` de `vm_affiliate_products`; 2) p/ cada um, rodar a actor Apify com `keyword = name` (`run-sync-get-dataset-items`); 3) casar `item.SKU === external_id`; 4) extrair `novoPreco`→`price`, `imagemLink`→`image_url`, `Moeda`→`currency` (normaliza "BRL R$"→"BRL"); 5) `UPDATE` + `metadata.availability` (`available` se SKU casou, senão `unavailable`) + `last_checked_at` + `enriched_by`; 6) pulse `infra_health_logs service='affiliate-catalog-enrichment'`. |
| **Verification gates** | (a) actor run `status=SUCCEEDED`; (b) `SELECT` mostra `price IS NOT NULL` + `image_url` começa com `https://http2.mlstatic.com/`; (c) `metadata.availability='available'`; (d) a página `/dashboard/affiliate-products` mostra foto+preço após hard-refresh. |
| **Recovery** | Run `FAILED` (anti-bot/selectors) → manter dados anteriores, `metadata.availability` inalterado, pulse `degraded`, **não** zerar foto/preço. SKU não casou em N execuções seguidas → marca `unavailable` (sai da listagem pelo gate). Actor sumir/quebrar → fallback manual (Settings) ou trocar de actor. |
| **Success signal** | `vm_affiliate_products.price`/`image_url` populados + `availability='available'` + card renderiza foto+preço; e em re-checks, delisting vira `unavailable` automaticamente. |

## Gate de listagem (verificação antes de listar como oportunidade)
A página/hook lista **só** produtos `is_active=true` **E** `price IS NOT NULL` **E** `metadata.availability='available'`. Produto não-verificado/indisponível **não** aparece como oportunidade (requisito Sovereign 2026-06-01).

## Anti-patterns proibidos
- ❌ Tentar `api.mercadolibre.com` direto de qualquer servidor nosso (IP-blocked — provado).
- ❌ Zerar `price`/`image_url` num run que falhou (perde dado bom por causa de anti-bot transitório).
- ❌ Afirmar "estoque verificado" — a actor não dá estoque; é proxy de presença em busca.
- ❌ Hardcodar token Apify per-user em cron sem JOIN; ou usar token de um tenant p/ enriquecer produto de outro.

---
_Ref: actor `karamelo~mercadolivre-scraper-brasil-portugues` · `scripts/enrich-affiliate-products.ts` · OTD-ML-001 · seal v6.20.x_

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

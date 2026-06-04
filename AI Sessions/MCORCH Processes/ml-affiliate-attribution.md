# SOP — Mercado Livre Affiliate Attribution (no public link API)

> **Anticorpo** (CLAUDE.md §5 Obstacle→Synthesis). Sintetizado em 2026-05-30 a partir do
> falso-sucesso da seal v6.14.1, que afirmou *"OTD-ML-001 resolvido / shortlinks meli.la"*
> enquanto `link-forge.ts` ainda roteava por `panel.gcrux.com/api/ml-redirect` →
> `302 → /login` (login wall, zero atribuição). Materialidade (Lei 1) refutou a claim.

## Verdade material (OTD-ML-001, validada 2026-05-30)

**O Mercado Livre NÃO tem API pública de geração de link de afiliado.** Confirmado por:
- `api.mercadolibre.com/items/{id}` → 403 (exige OAuth user-token).
- Páginas oficiais de afiliados → 403/login (auth-gated).
- `grant_type=client_credentials` com `affiliate_config` → `invalid_client` (ML não habilita esse grant).
- Múltiplas fontes (incl. Reclame Aqui) convergem: geração de link é **só via painel/Barra de Afiliados** (per-user, canal aprovado), produzindo short links `meli.la`/`mercadolivre.com/sec`.

**Logo:** não existe endpoint para "minerar" `meli.la` programaticamente. Quem afirmar o contrário deve **colar a doc oficial** (Lei 1) antes de codar.

## Mecanismo correto de atribuição

| Camada | Como | Confiança |
|--------|------|-----------|
| Programática (automatizável) | URL real do produto + `?matt_word=<tag>` (param de atribuição do ML) | Best-effort — atribui se o `matt_word`/canal estiver vinculado à conta |
| Definitiva | Short link `meli.la` gerado no painel do afiliado (per-user) | Garantida — embute conta + canal |

- A **tag** (ex.: `caga6077534`) mora em `affiliate_config.affiliate_tag` (per-user, `auth.uid()`). **NÃO** é o `app_id` OAuth (erro corrigido em `eebea0a`).
- Build correto: `https://www.mercadolivre.com.br/MLB-{numeric}?matt_word={tag}&utm_*` (ver `scripts/link-forge.ts:buildAffiliateUrl`).

## Anti-patterns proibidos (gates de recusa)

- ❌ Rotear afiliado via `panel.gcrux.com/api/ml-redirect` (proxy morto → login wall).
- ❌ Passar `app_id` OAuth como "affiliate id" (não atribui; vaza entre tenants se compartilhado).
- ❌ Afirmar "shortlinks meli.la gerados via API" sem a doc oficial do endpoint (não existe).
- ❌ Fechar OTD/seal de afiliado com audit `--bypass` (pula a prova — Lei 1).

## SOP operacional

| Pergunta | Conteúdo |
|----------|----------|
| **Operator** | MCORCH Agent (ou Sovereign no painel ML para gerar o `meli.la` per-user). |
| **Sequence** | 1) Confirmar `affiliate_config.affiliate_tag` do user (`auth.uid()`); 2) resolver produto real; 3) build URL com `matt_word` OU usar o `meli.la` colado do painel; 4) persistir em `affiliate_links`; 5) pulse `infra_health_logs`. |
| **Verification gates** | (a) `grep -c panel.gcrux.com scripts/link-forge.ts` em código = 0; (b) link gerado começa com `mercadolivre.com.br`/`meli.la` (nunca `panel.gcrux.com`); (c) **browser real (`agent-browser`) confirma que o MLB resolve no produto** — curl é bot-bloqueado (403), não serve de prova; (d) `revenue_cents > 0` no tenant correto após conversão real. |
| **Recovery** | Link 404/login → reabrir o produto no painel, regenerar `meli.la`, atualizar `affiliate_links`. Tag ausente → user sem `affiliate_tag` é fail-closed (skip), não emitir link sem atribuição. |
| **Success signal** | Clique → produto ML real → conversão atribuída ao tenant dono (postback `handle-ml-postback` → `ATTRIBUTES_REVENUE_TO` → ROIWidget). |

## Verificação de IDs de produto (não pular)

curl a `/items` e à URL pública retorna **403** (OAuth + bot-block). Para afirmar que um `MLB...`
é real/ativo: usar `agent-browser` (browser real) OU OAuth user-token válido. **Nunca** declarar
"verificado" sem um desses — foi a lacuna não-fechada da v6.14.1.

> ⚠️ **Nota de materialidade (2026-06-01):** o `agent-browser` headless em IP de datacenter também
> é bot-bloqueado pelo ML ("Hubo un error accediendo a esta pagina…") — tanto na URL crua quanto na
> `matt_word`. Controle: a URL crua que o Sovereign confirma abrir no browser real dele mostra o MESMO
> erro headless → isola o bloqueio como anti-bot (não o link). Prova de resolução = browser real do
> Sovereign (residencial) + experimento de controle isolando a variável. Prova das mecânicas = 302s
> reais da edge function + composição (a `matt_word` é o `product_url` verificado + query params).

## Implementação híbrida (v6.20.0 — 2026-06-01)

Resolução em camadas, **per-user e fail-closed**, compartilhada por frontend + edge:

1. **Definitiva (`shortlink`)** — short link `meli.la`/`/sec/` do painel ML, guardado **per-user** em
   `affiliate_config.metadata.shortlinks[<MLB external_id>]`. **NUNCA** no catálogo compartilhado
   `vm_affiliate_products` (vazaria a atribuição de um tenant para outro — o short link embute a conta).
2. **Best-effort (`matt_word`)** — `product_url` real (do catálogo) + `?matt_word=<affiliate_config.affiliate_tag>`.
3. **Fail-closed** — sem tag e sem short link → não emite link (UI manda pra `/dashboard/affiliates`;
   edge GET 302 → `/dashboard/settings?no_config=1`; POST → HTTP 402).

| Superfície | Arquivo | Papel |
|------------|---------|-------|
| Resolver puro (browser/Node) | `src/lib/affiliate.ts` | `resolveAffiliateLink` · `buildMattWordUrl` · `isMlShortLink` · `readShortlinks` (testes em `affiliate.test.ts`) |
| Catálogo (página) | `src/pages/AffiliateProductsPage.tsx` + `useAffiliateConfig.ts` | copia o link resolvido · editor per-produto grava `metadata.shortlinks` via `setProductShortlink` |
| Clique do leitor | `supabase/functions/process-affiliate-link/index.ts` | GET + POST resolvem hybrid (cópia Deno do builder) |
| Catálogo (dados) | `vm_affiliate_products.affiliate_template_url` | **NULL** (templates `panel.gcrux.com` removidos 2026-06-01); link montado por tenant |

**Gate (a) reforçado:** nenhum arquivo de código/script **emite** `panel.gcrux.com` (só comentários/anti-pattern
e o trilho de auditoria README/BoK/HANDOFF o citam). `grep -c panel.gcrux.com scripts/link-forge.ts` = 0.

---
_Ref: docs/bok/mercado-livre-api/ (OTD-ML-001/002) · commit eebea0a · seal 45bc299b · hybrid v6.20.0_

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

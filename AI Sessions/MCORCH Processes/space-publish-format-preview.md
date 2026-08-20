# SOP — Pré-visualização de formato de publicação (Spaces / Biblioteca de Assets)

> **Lei 2 (Processo Antecipado).** Feature **display-only** sobre um trilho JÁ documentado. Este SOP cobre a
> camada de UX (seletor de formato + preview) que antecede o passo de publicação; o **dono da automação de
> publicação** é [`space-publish-variants.md`](./space-publish-variants.md) — este SOP NÃO o duplica.
> BoK: [`docs/bok/spaces-evolution/21-amendment-publication-format-preview.md`](../bok/spaces-evolution/21-amendment-publication-format-preview.md).

## Contexto

O social media manager, hoje, escolhe `channel`/`surface` no nó "Publicar em Rede Social" **sem ver** como o
criativo vai aparecer — imagina mentalmente o crop 9:16, a safe-zone da legenda, o teto de 10 slides. Este
processo materializa essa imaginação num preview fiel client-side, ANTES de gravar a variante ou publicar.

**Invariante honesto (Lei 1):** o preview é uma **prévia aproximada**. O Spaces publica o asset **como-está**
(`publish-space-asset` não reframa). O reframe real por formato só ocorre no fluxo pago (reshaper). A UI declara isso.

| Pergunta | Conteúdo |
|---|---|
| **Operator** | Social media manager / Usuário Zero — na Biblioteca de Assets (`/dashboard/spaces/assets`), abre um asset, escolhe o formato de publicação e confere o preview antes de agir. |
| **Sequence** | 1. Selecionar um asset (imagem/vídeo) na biblioteca → abre o modal. 2. Na seção "Publicar", escolher um formato (chips filtrados por tipo de asset: p/ imagem → Feed/Carrossel/Stories/Pin/Link; p/ vídeo → Reels/Short/TikTok/Stories). 3. O `PublicationPreview` renderiza client-side no aspect/px exatos + safe-zones + chrome da rede. 4. Escrever a legenda (contador respeita o `caption.max` do formato). 5. **Salvar rascunho** (grava `space_publish_variants` via `publish-space-asset {publish:false}`) OU **Publicar** (só habilitado quando o formato tem trilho real; `{publish:true}` enfileira `scheduled_posts`). |
| **Verification gates** | (G1) o aspect do preview bate com `format.aspect` do catálogo `src/lib/format-specs.ts` (que espelha o seed `channel_profiles`). (G2) zero rede além da signed-URL owner-scoped já resolvida — nenhum mcoCoin debitado (preview é display-only). (G3) badge de disponibilidade honesto: `Publicável` / `Privado até auditoria` / `Em breve` (derivado de `publishable`). (G4) rascunho salvo aparece em `space_publish_variants` (UNIQUE user+asset+channel+surface). |
| **Recovery path** | Signed-URL expirada → o preview re-resolve via `resolveAssetUrl` (normalizador owner-scoped) ao reabrir o modal. Formato sem trilho ("Em breve") → botão publicar desabilitado + tooltip; o rascunho ainda pode ser salvo. Falha do `publish-space-asset` → toast pt-BR com `edgeErrorMessage` (o trilho documentado trata idempotência/tenant). |
| **Success signal** | O preview renderiza no formato escolhido (materialmente: aspect correto + safe-zones desenhadas), o contador de legenda reflete o limite do formato, e "Salvar rascunho" incrementa a contagem de `space_publish_variants` do usuário (SELECT real). |

## O que este processo NÃO faz (fronteiras)

- **Não reframa bytes.** Nenhuma chamada a `reshape-pillar` / money-path. O preview é CSS-crop; o publicado é as-is.
- **Não cria tabela/edge.** Reusa `publish-space-asset` + `space_publish_variants` (Amendment 15).
- **Não promete alcance.** Trilhos com transporte real mas alcance gated (IG/TikTok/YT/Pinterest, app-audit/Trial)
  aparecem como `Privado até auditoria`; formatos sem trilho algum (Stories, YT Comunidade, LinkedIn/X com mídia)
  aparecem como `Em breve` com publicar desabilitado — a UI nunca mente sobre o que vai ao ar.

## Anticorpo

Se um futuro requisito pedir que "o preview seja pixel-exato ao publicado", isso implica reframe server-side por
formato (OTD-SPACES-043) — é money-path (compute), exige BoK/gate de custo e NÃO pode ser embutido no preview
display-only sob pena de virar cobrança-sem-declaração. Preview permanece aproximação até esse OTD ser resolvido.

## Apêndice (2026-07-14) — Carrossel IG agendado (OTD-SPACES-044 → Amendment 22)

O transporte agendado do carrossel vive em `docs/bok/spaces-evolution/22-amendment-scheduled-carousel.md`
(FR-SPACES-079/080 + gates G1-G6). Resumo operacional: `publish-space-carousel {render_id, caption, schedule:true, publish_at?}`
enfileira `scheduled_posts` com o marcador `metadata.reshape.carousel_render_id`; o cron `auto-publish` resolve os
slides OWNER-SCOPED de `creative_assets` no momento do publish (assinatura fresca 6h por tentativa) e entrega
`content.images[]` ao ramo CAROUSEL do `publish-social`. FMEA-011 preservado: o marcador nunca é uma ref de asset.
Smoke: `scripts/qa/smoke-scheduled-carousel.ts`. UI de agendamento + flip do catálogo = fatia seguinte.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

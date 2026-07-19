# Estratégia de cadência de conteúdo — MCORCH × GabrielAI (v1, gerada pelo ecossistema)

> **Origem:** Diretiva Sovereign 2026-07-13 ("preciso de uma estratégia válida gerada também pelo ecossistema mcorch para a cadência e próximos vídeos… já temos o roadmap e pipeline definidos"). Este doc é **plano, não execução** — nenhuma recorrência (cron) é armada sem GO explícito do Sovereign (Lei 4).
> **Fundamentação (Lei 1):** cada trilho abaixo foi verificado materialmente em 2026-07-13 (inventário `scratchpad/rails-inventory.ts`). Onde um trilho está frio ou gated, está dito sem maquiagem.
> **ORO:** Operator = MCORCH (autopilot + workers) · Reviewer = Sovereign · Owner = Sovereign (marca + contas reais).

---

## 1. Inventário material — o que existe HOJE

| Capacidade | Estado real (verificado) | Implicação p/ cadência |
|---|---|---|
| **Produção de cortes** | Detector viral 1-clique + motor motion-graphic (US$ 0) — **3 shorts EP01 prontos** (abertura 9.0 · finale 9.5 · conspiração 8.5) na Biblioteca | O EP01 já tem estoque para uma **semana** de posts |
| **Distribuição** | `publish-space-asset` VIVO (probe 400) + botão "Distribuir" na UI → `scheduled_posts` → `auto-publish` (cron) | ⚠️ `scheduled_posts` = **0**: o motor nunca rodou p/ o User 0. A 1ª publicação é o marco de tração. |
| **Canais** | `channel_profiles` 7 canais + `social_accounts` IG/LinkedIn/FB/YouTube/X/TikTok todos `is_active` | Multi-canal pronto; **gates externos** mandam (abaixo) |
| **Roteiro/masters** | GabrielAI: ep01 footage (host) + SRT gerado; **ep02-04 têm SRT mas SEM footage no host**; roteiros no GitHub (via MCP) | Produção dos próximos exige subir/gerar footage dos ep02-04 |
| **Mineração (novos vídeos)** | Pool multi-key BYOK (Amendment 20) pronto p/ 3 Gmails × créditos free-tier Google | Habilita produção ep05+ via pipeline GabrielAI (Veo) a custo ~US$ 0 |
| **Métrica de loop** | `creative_metrics.hook_rate` existe; `viral-autopilot` (cadência recorrente, default OFF); `autopilot_plans` ausente | Fechamento de loop possível quando houver dados reais |

### Gates externos honestos (mandam na cadência — ação Sovereign, não código)
- **TikTok**: `SELF_ONLY` (privado) até a auditoria do app aprovar → serve p/ testar pipeline, **não** p/ alcance.
- **Instagram**: publicação gated no App Review da Meta.
- **YouTube**: conectado (`social_accounts` on), mas **Analytics API não habilitada** → sem métrica de retenção ainda.
- **Conclusão**: o **único canal com alcance público imediato e métrica é o YouTube (Shorts + Data API)** + **WordPress** (blog próprio). A v1 da cadência **ancora nesses dois** e trata IG/TikTok como "ensaia agora, alcança quando o gate abrir".

---

## 2. Dois loops (produção ≠ distribuição)

### Loop A — PRODUÇÃO (semanal, gated na mineração)
```
roteiro GabrielAI (GitHub) → Veo via pool multi-key (créditos Gmail#1→#2→#3) → master 16:9 + SRT
  → ingest host-local (/dashboard/repurpose) → detector 1-clique → 3-5 shorts motion-graphic
```
- **Ritmo proposto:** **1 episódio novo / semana** (o pipeline GabrielAI já produziu 4; o gargalo é crédito, resolvido pelo pool).
- **Estoque atual:** EP01 pronto; ep02-04 = só precisam do footage (SRT já existe) → **3 episódios a um upload de distância**.
- **Custo:** rail de corte US$ 0; geração Veo consome créditos free-tier (por isso o pool prioriza os 3 Gmails).

### Loop B — DISTRIBUIÇÃO (por episódio, escalonada)
Regra: **1 master → N shorts espaçados** (não despejar tudo no D0 — o algoritmo pune e você queima o estoque). Proposta por episódio:

| Dia | Ativo | Canal (v1, alcance real) | Depois do gate |
|---|---|---|---|
| **D0** | Short **abertura** ("o fim da programação") + **post WordPress** (vídeo embedado + fontes) | YouTube Shorts + WP | +IG Reels |
| **D+2** | Short **conspiração** ("Coincidência?") | YouTube Shorts | +TikTok, +IG |
| **D+4** | Short **finale** ("nova forma de inteligência?") | YouTube Shorts | +TikTok, +IG |
| **D+5** | Carrossel IG (key-frames dos capítulos) | — (gated App Review) | IG |

- **Horários:** derivados do `channel_profiles` (cada canal tem sua janela); o `auto-publish` já respeita `scheduled_at`.
- **Mecânica:** botão "Distribuir" (hoje manual, 1 clique/short) → quando a v1 validar, o `viral-autopilot` assume o agendamento (recorrência = decisão Sovereign).

---

## 3. Fechamento de loop (o que torna a cadência *inteligente*)
```
short publicado → creative_metrics (hook_rate, impressions, engagements)
   ⤷ YouTube Data/Analytics (quando habilitada) alimenta impressions/retenção reais
short com hook_rate alto → sinal p/ o detector (OTD-VR-008b, padrão agêntico 9 "Learning")
   ⤷ os próximos cortes priorizam o TIPO de momento que performou
```
- **v1 (agora):** métrica manual/observacional (o Sovereign vê o que pegou).
- **v2 (pós-Analytics):** `creative_metrics.hook_rate` real realimenta o scoring do detector — hoje é OTD aberto, honesto.

---

## 4. Sequência de ativação proposta (o que eu recomendo, em ordem)
1. **Agora (0 gate):** publicar os **3 shorts EP01 no YouTube** (D0/D+2/D+4) + **post WordPress** do EP01. → primeira tração real, métrica via YouTube.
2. **Esta semana:** subir footage de **ep02** (SRT já existe) → detector → distribuir. Prova o pipeline com 2 episódios.
3. **Habilitar YouTube Analytics API** (ação Sovereign) → liga a métrica de retenção.
4. **Mineração ep05+:** aplicar migration do pool + cadastrar os 3 Gmails → produzir via créditos.
5. **Só então** armar recorrência (`viral-autopilot` / cron) — com dados reais para calibrar, não no escuro.

---

## 5. O que NÃO fazer (anti-cadência)
- ❌ Armar cron de recorrência **antes** de 1 ciclo manual provado (sem baseline, o autopilot amplifica erro).
- ❌ Publicar os 3 shorts no mesmo dia (canibaliza alcance + queima estoque).
- ❌ Tratar TikTok/IG como alcance antes dos gates de auditoria (hoje só ensaio).
- ❌ Minerar vídeo novo com chave paga enquanto houver crédito free no pool (o pool existe justamente p/ isso).

---

## 6. Decisão pendente do Sovereign (antes de qualquer recorrência)
- [ ] Aprovar esta v1 (ou ajustar canais/dias/ritmo).
- [ ] GO para publicar os 3 shorts EP01 no YouTube agora (eu enfileiro via botão Distribuir / `publish-space-asset`).
- [ ] Ordem de produção dos próximos: ep02 → ep03 → ep04 (footage) ou minerar ep05 novo?

**Cross-links:** `docs/bok/video-repurpose/10-frd-sdd-viral-quality.md` · `docs/bok/spaces-evolution/20-amendment-multikey-byok-vertex.md` · `docs/processes/autopilot-cron-identity.md` (recorrência) · [[project_viral_autopilot]] · [[project_revenue_funnel_repair]].

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

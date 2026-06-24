# SOP: Viral Autopilot — Vídeo Vertical 9:16 via HyperFrames (`autopilot-video-9x16`)

**Status:** ACTIVE · v1.0 · 2026-06-24
**Owner:** Sovereign (Gabriel Zarattini)
**Survival Law 2 compliance:** Escrito **ANTES** de qualquer código da Fatia VA-V1 (integração 9:16 no pipeline do Autopilot). Abre o gate **OTD-VA-009** (`docs/bok/viral-autopilot/05-sdd.md` — *"Gate Lei 2 — Amendment v0.2: exige SOP `docs/processes/autopilot-video-9x16.md` ANTES de qualquer código de vídeo"*) e cobre FR-VA-022..026 + a extensão de custo de FR-VA-007.
**Canonical directive:** `CLAUDE.md > MCORCH Master Execution Protocol` (Closed-Loop) · `.claude/rules/survival.md > Law 1/Law 2` · `docs/bok/viral-autopilot/{03-prd,04-frd,05-sdd}.md` (Amendment v0.2) · `docs/bok/video-studio/{04-frd,05-sdd}.md` (FR-VS-024/025 motor + sandbox).
**Sibling SOPs:** `autopilot-cron-identity.md` (identidade cron + pré-débito/refund — **base financeira deste**) · `orchestrate-async-pipeline.md` (`verify_jwt=false` + pg_net + contrato de RPC) · `build-deploy-materiality.md` (worker host ≠ worktree) · `canvas-video-async-execution.md` (precedente de render async + reconciliação).

---

## Context

A Amendment v0.2 do `viral-autopilot` adiciona **um asset de vídeo vertical 9:16** a cada sub-run product-aware, quando o plano opta (`video_enabled`). O vídeo é renderizado pelo **motor determinístico HyperFrames** do `video-studio` (HTML→MP4 1080×1920 via Chrome headless + FFmpeg — FR-VS-024/025), **não** por IA (OTD-VA-009 escolha A). Três riscos materiais nascem disso:

1. **Render de HTML não-confiável (FMEA-VS-001 RPN 200 / FR-VS-025).** A composição 9:16 mistura 3 fontes não-confiáveis (nome/descrição de produto ML, texto de trend `vm_trends`, `optimization_policy` reinjetado) dentro de um HTML que um Chrome headless executa. Se o HTML escapar do template e injetar `<script>`/`fetch`, um render pode exfiltrar segredos do ambiente ou bater na rede interna. **Mitigação desta fase:** (a) Cyber-Sentinel fail-closed + escape das 3 fontes ANTES de entrarem no HTML (espelha `orchestrate-content:92`); (b) o motor roda **single-tenant Usuário Zero** (OTD-VA-011), renderizando **templates do próprio tenant 0** — o hardening multi-tenant (container efêmero selado, egress-only, zero credencial no env, `cap_drop=ALL`) é **diferido** para o Usuário 1, mas o `/security-review` do worker é **obrigatório** já agora.

2. **Dupla cobrança (OTD-VA-010 / TOCTOU financeiro).** O motor `video-render` deduz `VIDEO_HYPERFRAMES_RENDER` na entrada (FR-VS-010). O ciclo do Autopilot **já pré-debitou** o custo de vídeo no `begin_autopilot_cycle` (FR-VA-007 estendido). Se o enqueue não sinalizar `prepaid=true`, o tenant é cobrado **duas vezes**. **Regra:** o caminho Autopilot→motor é **`prepaid`** (motor NÃO self-bill — espelha `orchestrate-content` FR-VA-016); o ÚNICO débito de vídeo é o do pré-débito do ciclo.

3. **Asset assíncrono que chega depois do `finalize` (FR-VA-025).** O render é fire-and-forget; o `finalize_autopilot_cycle` (refund) roda quando os sub-runs de **texto/imagem** terminam — o MP4 pode aterrissar **minutos depois**. Se o ciclo fechar sem reconciliar, o asset some. **Regra:** um poller de reconciliação (estilo `autopilot-collect`/`rescue-video`) anexa o asset por `content_variant_id` **após** o `done`, e a falha de render é **fail-open `skipped`** — nunca derruba o ciclo de texto/imagem.

**Regra-mãe:** o vídeo é uma **camada aditiva fail-open** sobre o ciclo já existente. Nenhuma falha de render, sanitização ou reconciliação pode (a) cobrar o tenant a mais, (b) derrubar a geração de texto/imagem, ou (c) publicar HTML não-escapado. O custo de vídeo é contabilizado **uma vez**, no pré-débito do ciclo.

---

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (autoria da migration `video_enabled`/`video_format`, do bloco de composição em `orchestrate-step`, do enqueue prepaid, do poller de reconciliação) + worker host HyperFrames (render por job) + Edge runtime (enqueue + reconcile).
- **Reviewer:** Sovereign (Gabriel) — aprova a migration + o `/security-review` **obrigatório** do worker de render (sandbox) + valida os smokes zero-cost · `/security-review` independente na migration de schema.
- **Owner:** Sovereign — blast radius = **carteira do tenant 0 gasta autonomamente** (dupla cobrança se o prepaid falhar) + **superfície de execução de HTML** (escape de sandbox se a sanitização falhar) + **asset órfão** (custo pago sem entrega se a reconciliação falhar).

---

## Operator (equivalente manual — material)

O ritual humano que a automação substitui, a cada sub-run de um plano com vídeo ligado:

| # | Passo manual | Critério de sucesso material |
|---|--------------|------------------------------|
| 1 | Abrir o produto-alvo do ciclo (imagem, nome, preço, comissão) + o gancho viral do ângulo | Dados do produto + hook conferidos |
| 2 | Compor um short 9:16 (1080×1920): imagem do produto + texto do gancho + caption + CTA + branding, num template fixo | Composição visual aprovada, sem texto não-escapado |
| 3 | Renderizar a composição em MP4 (determinístico) | MP4 ≥ 100KB, 1080×1920, ratio 9:16 conferido |
| 4 | Conferir que o custo do render saiu **uma vez** (não cobrar de novo se já pré-pago) | Saldo debitado 1×, igual ao projetado |
| 5 | Anexar o MP4 ao criativo daquele produto/rede (biblioteca + post agendado) | `content_library type=video` + `scheduled_posts.content_id` setados |
| 6 | Se o render falhar, **publicar o texto/imagem mesmo assim** (não bloquear o ciclo) | Ciclo de texto/imagem intacto; vídeo marcado `skipped` |

O passo 4 (cobrança única) e o passo 6 (fail-open) são exatamente o que o gate Lei 2 protege.

---

## Topologia (alvo)

```
autopilot-run (begin_autopilot_cycle: projected += N_video × VIDEO_HYPERFRAMES_RENDER, pré-débito atômico)
  │  fan-out sub-runs (Bearer SB_SECRET_KEY + x-autopilot-user-id server-trusted)
  ▼
orchestrate-content → orchestrate-step  (prepaid=true)
  │  ① gera texto + imagem product-aware (Fatia 1/1b)
  │  ② SE video_enabled:
  │     ├─ sanitiza 3 fontes (Cyber-Sentinel fail-closed + escape HTML)   ◀── FR-VA-023
  │     ├─ monta composição HTML 1080×1920 (template + imagem do produto)
  │     └─ enqueue video_render(engine='hyperframes', prepaid=true,        ◀── FR-VA-024
  │           product_id, user_id da linha, content_variant_id)
  │        (fail-open: erro → marca 'skipped', segue o ciclo de texto/imagem)
  ▼
[worker host HyperFrames] ── claim atômico video_renders (engine=hyperframes, state=queued)
  │  render no container efêmero (Chrome headless + FFmpeg) → MP4 1080×1920
  │  upload bucket privado video-studio-assets → finalize_video_render(refund=0 no prepaid)
  ▼
autopilot-video-reconcile (poller service-role, user_id da linha)            ◀── FR-VA-025
  │  detecta video_renders.state='done' do ciclo
  │  content_library(type='video', media_url=storage_key) + creative_metrics + scheduled_posts.content_id
  ▼
finalize_autopilot_cycle (refund crédito-positivo idempotente — inalterado; absorve N_video no actual)
```

---

## Cost & atomicity contract (resumo executável)

| Regra | Implementação |
|-------|---------------|
| Custo de vídeo no projetado | `projected = N_runs×10 + N_video×VIDEO_HYPERFRAMES_RENDER(12) + ANALYZE_COST(2)`, `N_video = N_runs` se `video_enabled` senão 0 (FR-VA-007 estendido) |
| Débito único | Pré-débito do ciclo cobre o vídeo; o enqueue usa **`prepaid=true`** → o motor `video-render` **suprime** o `deduct_mco_coins` (espelha `orchestrate-content` FR-VA-016) |
| Refund | `finalize_autopilot_cycle(cycle_id, actual)` — `actual` inclui os renders que **de fato** entregaram; o não-usado volta como **crédito positivo idempotente** (NUNCA `deduct` negativo — `migration 20260603220000:45`) |
| Cap diário | `N_video×12` entra no `acumulado + projetado` do cap diário (FR-VA-021); o plano (default 200) e o cap diário devem comportar +12/sub-run (OTD-VA-010) |
| Identidade | service-role + `user_id` server-trusted da linha (`autopilot_cycles`/`autopilot_plans`/`video_renders`), **nunca do body** (OTD-VA-008, herdado de `autopilot-cron-identity`) |

---

## Verification gates

| Gate | Comando/observação material | Esperado |
|------|------------------------------|----------|
| G1 — sanitização | Smoke com produto/trend contendo `<script>`, `</template>`, `${...}`, aspas, URL → inspecionar o HTML gerado | Zero tag/script não-escapado; Cyber-Sentinel 403 em injeção (espelha sentinel pt-BR/en) |
| G2 — prepaid (sem dupla cobrança) | Smoke zero-cost: ciclo `video_enabled` em `dry_run`/saldo controlado → `SELECT` no ledger | **1** débito de vídeo (no pré-débito do ciclo); `video_renders` do sub-run com `charged_mco=0` (prepaid) |
| G3 — ratio 9:16 | Render real (1 sub-run) → `ffprobe` no MP4 do bucket | `width=1080 height=1920` (ratio 9:16); arquivo ≥ 100KB; `Content-Type: video/mp4` |
| G4 — determinismo | 2 renders do mesmo input → `sha256sum` (NFR-VS-016) | Hashes idênticos |
| G5 — fail-open | Forçar erro de render (template inválido) → conferir o ciclo | Texto/imagem publicam; `video_render.state='failed'`/`skipped`; ciclo NÃO aborta; saldo de vídeo refundado |
| G6 — reconciliação async | Render que termina **depois** do `finalize` → rodar o poller | `content_library type=video` + `creative_metrics` + `scheduled_posts.content_id` populados; sem asset órfão |
| G7 — sandbox | `/security-review` do worker host + inspeção do container de render | Sem credencial de tenant no env de render; HTML não alcança rede interna; `/security-review` SAFE |
| G8 — tenancy | Smoke: enqueue com `user_id` de outro tenant no body → conferir | Ignorado; `user_id` resolvido **da linha** (OTD-VA-008); RLS `video_renders` SELECT-own |

---

## Recovery path

| Falha no passo | Rollback/retry exato |
|----------------|----------------------|
| Sanitização rejeita (G1) | Sub-run gera texto/imagem normalmente; vídeo `skipped`; log `infra_health_logs` `service='autopilot-video' event='sanitize_blocked'`. Sem deduct extra. |
| Enqueue falha (motor 503/erro) | **fail-open**: `skipped`; o pré-débito de vídeo daquele sub-run vira refund no `finalize` (`actual` não conta o vídeo não-entregue). Nunca derruba o ciclo. |
| Render trava (worker morto) | O poller `autopilot-video-reconcile` reaproveita o padrão `rescue-video`: re-claim de `video_renders` em `running` há > timeout → `failed` + refund; ou re-render manual via `video-render-poll`. |
| Asset chega após `finalize` | É o caso **normal** — o poller anexa por `content_variant_id` depois do `done`. Idempotente (não re-anexa se `content_library` já tem a linha do `content_variant_id`). |
| Dupla cobrança detectada | Bug de contrato: o enqueue não passou `prepaid=true`. Halt, corrigir o flag, refund manual via `finalize_autopilot_cycle` reconciliando `actual`. |

---

## Success signal

Materialmente observável que o flow 9:16 está completo e seguro:

1. **`ffprobe`** de um asset real do ciclo → `1080×1920` (9:16), ≥ 100KB, `video/mp4` no bucket privado `video-studio-assets`.
2. **Ledger:** saldo do tenant caiu exatamente `N_runs×10 + N_video×12 + 2` (− refund do não-entregue); **nenhum** `video_renders.charged_mco > 0` no caminho prepaid.
3. **`content_library`** tem a linha `type='video'` + **`creative_metrics`** tem a linha do `content_variant_id` + **`scheduled_posts.content_id`** aponta para o criativo.
4. **Smoke G5 (fail-open):** um ciclo com render forçado a falhar publica texto/imagem e fecha sem abortar, com refund do vídeo.
5. **`/security-review` SAFE** do worker de render + da migration de schema.

---

## Anti-patterns proibidos

- ❌ Enqueue do render **sem** `prepaid=true` → dupla cobrança (motor self-bill + pré-débito do ciclo).
- ❌ `user_id` do vídeo vindo do **body/header** do request em vez da linha confiável → injeção cross-tenant (viola OTD-VA-008).
- ❌ Falha de render **derrubando** o ciclo de texto/imagem (deve ser fail-open `skipped`).
- ❌ Interpolar nome de produto / texto de trend / `optimization_policy` **direto** no HTML sem escape + Cyber-Sentinel → XSS/escape de sandbox no Chrome headless.
- ❌ Render **multi-tenant** antes do hardening do sandbox selado (`/security-review` + container efêmero egress-only) — Usuário Zero single-tenant é o limite desta fase (OTD-VA-011).
- ❌ Fechar o ciclo (`finalize`) **sem** reconciliar o asset assíncrono → custo pago, asset órfão.
- ❌ Refund de vídeo como `deduct` negativo → viola o guard anti-mint `p_amount<=0` (`migration 20260603220000:45`).

---

## Sibling reference

Esta SOP é a **camada de vídeo** sobre a base financeira de `autopilot-cron-identity.md` (que já cobre identidade do cron + pré-débito/refund + cap diário). Reusa o motor de `video-studio` (FR-VS-024/025) e o padrão de render async + reconciliação de `canvas-video-async-execution.md`. O worker host segue o molde de `scripts/design-bridge.ts` (claim atômico + execução em container) descrito na reconciliação de drift do `video-studio` SDD §2.3.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

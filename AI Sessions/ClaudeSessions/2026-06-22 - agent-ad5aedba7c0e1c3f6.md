# Session agent-ad5aedba7c0e1c3f6
**Date:** 2026-06-22 | **Session ID:** `agent-ad5aedba7c0e1c3f6`

---

## 👤 User *(01:26:13)*

STRATEGIC LENS = "AGENCY LEVERAGE" in the MCORCH ecosystem: MCORCH is a B2B2C platform whose multiplier is enabling AGENCIES and power-creators to PRODUCE and MONETIZE faceless video + design at SCALE across MANY clients/brands — using their own keys (BYOK), reselling/white-labeling the output, with mcoCoins as the margin/leverage lever and ML affiliate as revenue. "Usuário Zero" (Sovereign) is the pilot; the real TAM is agencies running content ops for portfolios of clients. Review whether the BoK PERFECTLY captures this leverage — not just a single-creator tool.

ADVERSARIAL VERIFICATION for dimension "monetization-leverage" of the BoK in docs/bok/video-studio/. A reviewer claimed these GAPS:
1. CRITICAL: Zero explicit Agency/Enterprise plan-tier pricing specification—no feature gates (seats, quotas, API limits) tied to plan tier; mcoCoins table shows volumes but no plan_tier.features mapping
2. CRITICAL: NO wholesale mcoCoins or resale margin model—agencies cannot buy in bulk at discount and resale to clients; no revenue split between MCORCH and agency; no margin transparency
3. CRITICAL: Affiliate revenue split undefined—BR-VS-007 says 'atribuição per-tenant' but not how much % goes to tenant/agency vs MCORCH; blocks agency business case
4. CRITICAL: NO agency ROI model distinct from single-creator—BRD §5.3 states '18% ROI depends on agency segment activation' but this is MCORCH's ROI; zero agency unit economics (cost-per-client, revenue-per-client, payback)
5. HIGH: No seat-based or role-based access control (RBAC)—agency with 5 editors cannot provision team seats; Stakeholder SH-VS-003 exists but no FRD/PRD specs for roles (owner/billing-admin/editor)
6. HIGH: Multi-client rollup dashboard missing—no feature for agencies to visualize per-client cost, revenue, affiliate split, or team usage; cost attribution exists at render level but no agency aggregation layer
7. HIGH: Affiliate ledger reconciliation undefined—no transaction schema for tracking click-source attribution, revenue settlement, or monthly reconciliation between MCORCH and agency
8. MEDIUM: OTD-VS-002 (Per-user BYOK open-design) is a hard gate for multi-client agencies—open status with no decision timeline blocks v1.0 agency onboarding; risks 'single-tenant EXPLICIT until closed' (BRD line 122)
9. MEDIUM: No agency activation KPI—BRD §2 lists BO-VS-001..005 but zero business objective for agency segment health (attach rate, volume, retention); quality-metrics §2 has 18 KPIs but no KPI-VS-XXX for agency leverage

Re-read the BoK docs (Read/Grep, read-only) and DEFAULT TO SKEPTICISM: for EACH claimed gap, determine if it is GENUINELY ABSENT or actually covered somewhere (a reviewer may have missed it). Return gaps_confirmed (truly absent) vs false_positives (already covered — cite the doc+ID where). Be precise.

## 🤖 Claude *(01:26:15)*

I'll systematically review the BoK for the "monetization-leverage" dimension to verify each gap claim. Let me start by exploring the document structure.

## 🤖 Claude *(01:26:15)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "find /home/gcrUX/htdocs/constellation-orchestra/docs/bok -type f -name \"*.md\" | head -20"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/canvas-design/01-mrd.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/canvas-design/00-index.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/canvas-design/05-sdd.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/canvas-design/04-frd.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/canvas-design/07-process-flow.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/canvas-design/03-prd.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/canvas-design/02-brd.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/canvas-design/08-quality-metrics.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/canvas-design/06-data-model.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/agentic-workspace/01-mrd.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/agentic-workspace/00-index.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/agentic-workspace/05-sdd.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/agentic-workspace/04-frd.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/agentic-workspace/07-process-flow.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/agentic-workspace/03-prd.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/agentic-workspace/02-brd.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/agentic-workspace/08-quality-metrics.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/agentic-workspace/06-data-model.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/01-mrd.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/marketing-hub/00-index.md
> ```

## 🤖 Claude *(01:26:22)*

Now let me find the video-studio BoK documents:

## 🤖 Claude *(01:26:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "find /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio -type f -name \"*.md\" | sort"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/00-index.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/03-prd.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/06-data-model.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/08-quality-metrics.md
> ```

## 🤖 Claude *(01:26:25)*

Let me read the key documents to evaluate each gap. I'll start with the BRD, PRD, and FRD:

## 🤖 Claude *(01:26:25)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# BRD — Business Requirements Document
> 2	
> 3	**Project:** video-studio
> 4	**Version:** v0.1 | **Date:** 2026-06-21
> 5	**BoK Applied:** BABOK v3 (Requirements Analysis & Design Definition)
> 6	**Status:** Draft
> 7	**Source of Truth (upstream):** `01-mrd.md` (MR-VS-001..014) — todo BR-VS deste documento rastreia ≥1 MR-VS.
> 8	**Market segment:** B2B2C · **Monetization:** híbrida (mcoCoins por render + afiliado Mercado Livre) · **Regulatory:** LGPD · **Integration surface:** extends-mcorch
> 9	
> 10	---
> 11	
> 12	## 1. Executive Summary
> 13	
> 14	O `video-studio` converte as Market Requirements em compromissos de negócio executáveis sob as **cinco regras inquebráveis MCORCH** (Diretiva Sovereign 2026-06-21): **R1 BYOK per-user**, **R2 mcoCoins gatekeeper atômico**, **R3 auth MCORCH nos apps isolados**, **R4 conexão à malha**, **R5 ponte de rede Docker**. O módulo entrega dois motores — **Faceless Studio** (geração autônoma E2E sobre o workflow n8n existente) e **HyperFrames Editor** (edição programática HTML→MP4 embedada nativamente em `/dashboard/canvas/video`) — ambos como apps isolados governados pelo cockpit soberano. O modelo econômico é híbrido: débito de mcoCoins por render (operação cara, calibrada 4×-floor) **mais** monetização via afiliado Mercado Livre embutido no conteúdo. Cada render bem-sucedido vira observação na malha; cada falha vira telemetria. A viabilidade depende de destravar três blocos materiais hoje abertos — **ponte de rede Docker (R5)**, **BYOK per-user no open-design de daemon compartilhado (OTD-VS-002)** e **provisionamento de identidade/entrega (PAT/JWT do studio + Telegram OTD-VS-003)** — sem os quais a fiação vision-QA/chroma/entrega é prosa, não engenharia.
> 15	
> 16	---
> 17	
> 18	## 2. Business Objectives (SMART)
> 19	
> 20	| ID | Objective | Specific | Measurable | Achievable | Relevant | Time-bound |
> 21	|----|-----------|----------|------------|------------|----------|------------|
> 22	| BO-VS-001 | Ativar produção autônoma de vídeo faceless E2E sob auth + billing MCORCH | Faceless Studio produz vídeo vertical completo (roteiro→voz→movimento→QA→entrega) a partir de tema/produto, gateado por JWT e debitado em mcoCoins | ≥ 1 render `success` com asset ≥100KB no bucket + observação na malha + débito atômico registrado, por tenant pagante | Workflow n8n já existe (id `e7e3beeb58f7411a`); falta auth/billing/ponte de rede | Núcleo do segmento primário (MR-VS-001) | MVP — após ponte de rede (R5) + BYOK (R1) destravados |
> 23	| BO-VS-002 | Embedar o editor programático HyperFrames no cockpit, multi-tenant e sandboxed | Rota nativa `/dashboard/canvas/video` (React embed, não iframe a dev server) renderiza HTML→MP4 determinístico com render isolado per-tenant | ≥ 1 MP4 determinístico renderizado por tenant via sandbox sem credencial compartilhada no ambiente de render | Pacote `@hyperframes/studio` exporta componentes React p/ embed nativo; porta 3002 livre no host | Núcleo do segmento secundário/agência (MR-VS-002) | v1.0 — após sandbox per-render (OTD-VS-006) selado |
> 24	| BO-VS-003 | Garantir disciplina econômica: zero gasto de crédito caro sem QA + consistência, margem ≥4× | Portão VLM (olho criativo) + consistência entre frames precede todo render caro de vídeo; custo calibrado 4×-floor | ≥ 90% dos renders de vídeo precedidos de gate VLM aprovado (12m); 100% das classes mco ≥ ceil(usd/$0.0045) | BYOK torna o QA grátis; SOP `creative-qa-vision-gate.md` já documenta o fluxo | Sustentabilidade + diferencial (MR-VS-005/006) | Contínuo desde o MVP; medição em produção no 1º render pago |
> 25	| BO-VS-004 | Monetizar o conteúdo gerado com afiliado ML e atribuição per-tenant | Link de afiliado Mercado Livre embutido no conteúdo do vídeo + atribuição de receita/clique por tenant | Attach-rate ≥ 65% de vídeos com link afiliado + ≥1 clique atribuído (12m) | Arquitetura afiliado ML + click ledger in-system já existem no MCORCH | Receita híbrida; diferencial vs SaaS de avatar (MR-VS-007) | v1.0 |
> 26	| BO-VS-005 | Selar compliance LGPD: erasure em cascata dos artefatos de vídeo/voz/config BYOK | Extensão do `delete-account` purga artefatos de vídeo, áudio clonado, config BYOK e dados de design; teste de zero-resíduo | 100% dos artefatos de vídeo/áudio/config de um tenant removidos ≤24h da chamada, provado por `SELECT` count antes/depois | Precedente Canvas Design (OTD-008) e `erase_lead()`/`erase_vision_artifacts` existem | Gate de GA — sem isso não há 2º tenant (MR-VS-014) | Gate de GA (antes do 2º tenant externo) |
> 27	
> 28	---
> 29	
> 30	## 3. Stakeholder Register
> 31	
> 32	| ID | Role | Interest | Influence | Communication Cadence | Contact |
> 33	|----|------|----------|-----------|----------------------|---------|
> 34	| SH-VS-001 | Sovereign / Maestro (Gabriel) | High | High | Continuous | gabrielcall@gmail.com |
> 35	| SH-VS-002 | Criador faceless (Usuário Zero → Usuário 1+, segmento primário) | High | Medium | Monthly NPS survey | Conta Gmail em produção (Usuário Zero) |
> 36	| SH-VS-003 | Operador de agência (segmento secundário) | High | Medium | Bi-weekly onboarding multi-tenant | Pipeline comercial v6.5.0+ |
> 37	| SH-VS-004 | Engineering (MCORCH Master Execution Agent + L1 engineer) | High | High | Per-session handoff | OpenClaw `engineer` / `.claude/agents/` |
> 38	| SH-VS-005 | Marketing-Growth (afiliado ML + atribuição de receita) | Medium | Medium | Sprint cadence (OE-661-ROADMAP) | OpenClaw `marketing-growth` |
> 39	| SH-VS-006 | Encarregado LGPD / Security (`/security-review`) | High | High | Per-migration gate | Engineering + Sovereign |
> 40	| SH-VS-007 | Providers externos (Gemini, Pollinations, LTX HF, VoxCPM, Mercado Livre) | Low | Medium | On license/quota change | Termos/dashboards de cada provider |
> 41	
> 42	---
> 43	
> 44	## 4. Business Requirements
> 45	
> 46	> Each BR traces to at least one MR. mcoCoins cost defined if AI-powered. **R1–R5 honored across all BRs.**
> 47	
> 48	| ID | Requirement | MR Traced | Priority | mcoCoins Cost | Acceptance Criteria |
> 49	|----|-------------|-----------|----------|---------------|---------------------|
> 50	| BR-VS-001 | Faceless Studio gera vídeo vertical E2E (Gemini director/QA → Pollinations → VoxCPM → Remotion overlays → LTX i2v + Ken-Burns fallback → FFmpeg composite → Gemini-vision QA → entrega) a partir de tema/produto | MR-VS-001 | Critical | `VIDEO_FACELESS_RENDER` (calibrado 4×-floor — multi-leg; OTD-VS-007) | Render `success` com MP4 ≥100KB no bucket + observação na malha + débito atômico |
> 51	| BR-VS-002 | HyperFrames Editor embedado nativamente (React embed) em `/dashboard/canvas/video`, rota declarada ANTES de `canvas/:id` no App.tsx; botão "Video" ao lado de Pipeline na TopBar | MR-VS-002 | Critical | `VIDEO_HYPERFRAMES_RENDER` (Chrome+FFmpeg local; calibrado — barato vs leg de IA) | Rota carrega editor logado; render produz MP4 determinístico; `:id="video"` não sombreia |
> 52	| BR-VS-003 | Toda superfície de vídeo (faceless trigger, editor, design.mcorch.com) gateada por sessão/JWT MCORCH; nunca anônima; identidade do studio via PAT/JWT emitido | MR-VS-003 | Critical | — | 401 em request sem identidade verificada; smoke prova rejeição anônima |
> 53	| BR-VS-004 | Gemini e todo provider externo resolvidos per-user via `decrypted_user_api_keys` (`auth.uid()`); env global SÓ em cron/service-role; hard-fail 402 estruturado se não configurado | MR-VS-004 | Critical | — | Zero env-key global em path user-facing; 402 `{error, action}` quando falta config |
> 54	| BR-VS-005 | Débito de render via `deduct_mco_coins(p_user_id,p_amount,...)` RPC atômico; 402 em saldo insuficiente; refund-on-failure; nunca client-side | MR-VS-005 | Critical | conforme tabela §6 | Delta `mco_balance` por `SELECT` real; 402 antes de qualquer leg de provider; refund em falha |
> 55	| BR-VS-006 | Portão de QA por olho criativo VLM (`vision.describe_image`/`analyze_video` via BYOK, custo 0) + consistência entre frames ANTES de gastar crédito caro de vídeo | MR-VS-006 | High | 0 (QA BYOK grátis) | `compare` aprova atributos-chave dos frames antes do render de vídeo (G3 do SOP) |
> 56	| BR-VS-007 | Link de afiliado Mercado Livre embutido no conteúdo do vídeo + UTM + atribuição de receita/clique por tenant | MR-VS-007 | High | — (atribuição, não geração) | `affiliate_links.content_id` NON-NULL + ≥1 clique no ledger in-system |
> 57	| BR-VS-008 | Cada render `success` insere nó `observation` na malha (`user_id+project_id`, embed-on-insert); cada falha → `infra_health_logs` | MR-VS-008 | High | EMBED grátis (assíncrono via trigger) | Nó com BR/FR ID rastreável na malha; log de falha com `service='video-studio'` |
> 58	| BR-VS-009 | Persistir o asset real (vídeo/imagem/áudio) em bucket privado soberano com row de asset; nunca confiar em URL efêmera do provider | MR-VS-009 | High | — | Objeto no bucket + row de asset (`public_url`/`storage_key`); prova = objeto, não API |
> 59	| BR-VS-010 | Execução de HTML/JS de tenant em sandbox per-render isolado (sem credenciais compartilhadas no ambiente de render Chrome headless) | MR-VS-010 | High | (incluído no custo de render HyperFrames) | Render roda em container/contexto isolado; nenhuma credencial de tenant vazada no env de render |
> 60	| BR-VS-011 | Memória semântica de roteiro/vídeo persistida (ChromaDB API v2 / malha com embed) para busca e reuso | MR-VS-013 | Medium | EMBED grátis | Roteiro/verdict pesquisável via `mesh.search`/Chroma após render |
> 61	| BR-VS-012 | Entrega do vídeo ao tenant com canal opcional/configurável (Telegram per-user ou sistema, ou apenas link soberano) — entrega não pode ser bloqueador único | MR-VS-011 | Medium | — | Vídeo acessível ao tenant via link soberano mesmo sem Telegram configurado (OTD-VS-003) |
> 62	| BR-VS-013 | Ponte de rede Docker entre `n8n_default` (faceless/remotion) e `mcorch-sovereign-net` (vision_mcp/chroma) + PAT/JWT do studio, destravando vision-QA + chroma-memory | MR-VS-008, MR-VS-013 | Critical | — | DNS de container resolve entre redes + handshake MCP+PAT do studio (OTD-VS-001) |
> 63	| BR-VS-014 | BYOK per-user real no open-design (daemon compartilhado): escolher via (a) daemon per-job efêmero / (b) `od` stateless / (c) container por tenant; fechar single-tenant atual | MR-VS-004 | High | — | 2 tenants com providers distintos isolados; nenhum config global compartilhado (OTD-VS-002) |
> 64	| BR-VS-015 | Hardening do design.mcorch.com: `OD_API_TOKEN` forte (não `development_token`), `OD_ALLOWED_ORIGINS=https://login.mcorch.com`, CF WAF Skip rule p/ requests não-browser | MR-VS-003 | High | — | Editor carrega logado sem CF challenge; token de dev substituído; origins restritos |
> 65	| BR-VS-016 | Erasure LGPD em cascata no `delete-account`: artefatos de vídeo/áudio + config BYOK + `OD_DATA_DIR`/`OD_MEDIA_CONFIG_DIR` + nós/embeddings; teste de zero-resíduo | MR-VS-014 | High | — | `SELECT` count antes/depois = zero resíduo ≤24h; migration passa `/security-review` |
> 66	
> 67	---
> 68	
> 69	## 5. ROI Model
> 70	
> 71	### 5.1 Cost Estimates
> 72	
> 73	| Cost Item | Type | Monthly Estimate | Annual Estimate |
> 74	|-----------|------|-----------------|----------------|
> 75	| Infraestrutura (Supabase + Docker mesh: remotion-render, studio-dashboard, open-design, vision_mcp, chroma) | OpEx | R$ ~600/mês | R$ ~7.200 |
> 76	| Chamadas de IA (Gemini director/QA per-user BYOK; LTX HF ZeroGPU grátis ~5 GPU-min/dia; Pollinations/VoxCPM free) | Variable | R$ ~250/mês (paths sistema; BYOK = $0 ao MCORCH) | R$ ~3.000 |
> 77	| Desenvolvimento inicial (ponte de rede, BYOK open-design, sandbox render, embed HyperFrames, billing legs, erasure) | CapEx | — | R$ ~95.000 (estimativa de esforço, 1 sprint-equivalente por sub-sistema + gates) |
> 78	| GPU/crédito de vídeo premium (fallback além do LTX grátis, ex.: leg paga eventual) | Variable | R$ ~150/mês | R$ ~1.800 |
> 79	
> 80	### 5.2 Revenue Streams
> 81	
> 82	| Stream | Model | Monthly Potential | Notes |
> 83	|--------|-------|-----------------|-------|
> 84	| mcoCoins por render de vídeo | Consumo (débito atômico, 4×-floor) | R$ ~4.000/mês (SOM ramp) | Faceless render + HyperFrames render; margem ≥4× sobre custo medido |
> 85	| Afiliado Mercado Livre | Comissão sobre conversão atribuída | R$ ~1.200/mês | Attach-rate crescente; receita per-tenant atribuída (click ledger) |
> 86	| Upsell de plano (volume de render puxa Pro/Enterprise) | Assinatura | R$ ~3.500/mês | Vídeo é operação cara → consome mcoCoins → puxa upgrade Starter→Pro→Enterprise |
> 87	
> 88	### 5.3 Payback Analysis
> 89	
> 90	| Metric | Value |
> 91	|--------|-------|
> 92	| Break-even (months) | ~11 meses (CapEx amortizado contra receita combinada de render + afiliado + upsell no ramp do SOM) |
> 93	| 12-month ROI | ~ +18% (conservador; depende da ativação do segmento agência em v1.0) |
> 94	| IRR (estimated) | ~22% a/a (sensível à attach-rate de afiliado e ao mix Pro/Enterprise) |
> 95	
> 96	---
> 97	
> 98	## 6. mcoCoins Economics
> 99	
> 100	> Modelo 4×-floor: `mco = ceil(custo_usd_real / $0.018 × 4) = ceil(custo_usd / $0.0045)`. Floor = piso Enterprise R$997/10000 mco. Espelhamento triplo (`src/lib/billing.ts` + constante do serviço + `billing.test.ts`). Classe final SÓ após medição material no 1º render pago (OTD-VS-007).
> 101	
> 102	| Operation | Coins/Run | Plan Tier Mapping | Monthly Volume (est.) | Monthly Revenue (est.) |
> 103	|-----------|-----------|-------------------|-----------------------|----------------------|
> 104	| `VIDEO_FACELESS_RENDER` (multi-leg: Gemini + LTX + Remotion + FFmpeg) | ~125 (provisório, paridade com canvas video DoP; recalibrar pós-medição — OTD-VS-007) | Starter(500)≈4 vídeos / Pro(2000)≈16 / Ent(10k)≈80 | ~320 renders | R$ ~3.200 |
> 105	| `VIDEO_HYPERFRAMES_RENDER` (Chrome headless + FFmpeg, sem leg de IA pesada) | ~12 (provisório — render local barato; análogo a IMAGE_GENERATION; OTD-VS-007) | Starter≈41 / Pro≈166 / Ent≈833 | ~600 renders | R$ ~700 |
> 106	| `VIDEO_QA_VLM` (olho criativo describe/analyze) | 0 (BYOK per-user) / 2 (path plataforma) | qualquer | ~1.500 chamadas | ~R$ 0 (BYOK domina; QA grátis incentiva o gate) |
> 107	| `MESH_CONSOLIDATE_REFERENCE` (verdict de QA na malha) | 1 | qualquer | ~300 | R$ ~75 |
> 108	
> 109	---
> 110	
> 111	## 7. Constraints & Assumptions
> 112	
> 113	### Constraints
> 114	
> 115	- **R5 — ponte de rede Docker (bloqueador material):** `n8n`/`remotion-render` vivem em `n8n_default`; `mcorch_vision_mcp` (127.0.0.1:3200) e `mcorch_chroma` (127.0.0.1:8001, API v2) vivem em `constellation-orchestra_mcorch-sovereign-net` — redes **isoladas**. A fiação vision-QA + chroma-memory do README é **prosa** até as redes serem pontadas e um PAT/JWT ser emitido p/ a identidade do studio.
> 116	- **R3 — design.mcorch.com:** LIVE via Cloudflare (origin `137.131.243.179`, cert self-signed, vhost provado HTTP 200 via loopback), mas CF **bot-challenge** bloqueia requests não-browser (403) → exige WAF Skip rule + `OD_API_TOKEN` forte (hoje `development_token`) + `OD_ALLOWED_ORIGINS`.
> 117	- **OTD-VS-002 — open-design single-tenant:** o `od` é cliente fino de um **daemon compartilhado**; `OD_MEDIA_CONFIG_DIR` por invocação NÃO isola — BYOK per-user exige re-arquitetura (daemon per-job / `od` stateless / container por tenant).
> 118	- **OTD-VS-003 — Telegram ausente:** `TELEGRAM_BOT_TOKEN` não existe em lugar nenhum; `GEMINI_API_KEY` existe só no `.env` da constellation. Entrega Telegram deve ser opcional ou provisionada per-user/sistema.
> 119	- **OTD-VS-006 — HTML não-confiável:** HyperFrames executa HTML/JS arbitrário de tenant via Chrome headless (Puppeteer) → sandbox multi-tenant obrigatório (container per-render, sem credenciais compartilhadas no env de render).
> 120	- Faceless workflow n8n está `active:false` hoje; helper scripts (`ltx.js`, `composite.sh`) precisam ser copiados para `/home/node/.n8n/assets/` no container `n8n-n8n-1`; SFX via `docker exec` lavfi.
> 121	- `docker compose up -d --build` recria os 2 containers ad-hoc do studio (downtime breve) e NÃO toca `login.mcorch.com` (nginx/CloudPanel do host, fora do Docker).
> 122	- Toda migration nova passa `/security-review` antes do commit (FMEA-011).
> 123	- Harness Engineering: lógica de negócio em hooks; componentes display-only; ops sensíveis em Edge Functions; RLS default-deny.
> 124	
> 125	### Assumptions
> 126	
> 127	- O workflow n8n existente (`e7e3beeb58f7411a`) é a base do cérebro faceless e será ativado/instrumentado, não reescrito do zero.
> 128	- LTX HF ZeroGPU (~5 GPU-min/dia grátis) cobre o volume MVP; fallback Ken-Burns cobre overflow sem custo de GPU.
> 129	- O Usuário Zero possui chaves BYOK (Gemini/OpenRouter/Google) → QA VLM custa 0 mco no piloto.
> 130	- HyperFrames (Apache-2.0) exporta componentes React (`StudioApp`, `NLELayout`, `NLEPreview`, `Player`, `Timeline`, `SourceEditor`, `PropertyPanel`) estáveis o suficiente p/ embed nativo (não iframe a dev server).
> 131	- O click ledger in-system de afiliado ML (OTD-ML-CLICKS, fechado) já reflete cliques no ROIWidget.
> 132	- FX R$5,5/USD; conclusões de margem sustentam-se em R$5–7.
> 133	
> 134	---
> 135	
> 136	## 8. Business Risk Register
> 137	
> 138	| Risk ID | Description | Probability | Impact | RPN | Mitigation |
> 139	|---------|-------------|-------------|--------|-----|------------|
> 140	| BR-VS-RISK-001 | Ponte de rede Docker (R5) não selada → vision-QA + chroma-memory permanecem prosa; portão de consistência inoperante | 4 | 5 | 20 | Tratar R5 (OTD-VS-001) como bloqueador de MVP; decidir attach-to-sovereign-net vs proxy dedicado ANTES de qualquer leg de QA; PAT/JWT do studio emitido |
> 141	| BR-VS-RISK-002 | HTML/JS de tenant executado sem sandbox → RCE / vazamento de credencial cross-tenant via Chrome headless | 3 | 5 | 15 | Container per-render isolado (OTD-VS-006); zero credencial no env de render; `/security-review` obrigatório; bloquear render multi-tenant até sandbox selado |
> 142	| BR-VS-RISK-003 | BYOK não isolado no open-design (daemon compartilhado) → quota/receita/risco de um tenant vazam p/ outro; fraude por design | 4 | 4 | 16 | OTD-VS-002 selada antes do 2º tenant; manter single-tenant explícito até lá; gate de GA |
> 143	| BR-VS-RISK-004 | Crédito caro de vídeo gasto sobre frames inconsistentes (sem portão VLM) → desperdício irreversível | 3 | 4 | 12 | Portão G3 obrigatório (SOP `creative-qa-vision-gate.md`); QA grátis via BYOK remove fricção; bloquear leg de vídeo se gate não passou |
> 144	| BR-VS-RISK-005 | Erasure LGPD incompleto (vídeo/voz clonada/config BYOK residual) → não-conformidade + bloqueio de 2º tenant | 3 | 5 | 15 | BR-VS-016 como gate de GA; teste de zero-resíduo; precedente `erase_vision_artifacts`/Canvas Design OTD-008 |
> 145	| BR-VS-RISK-006 | Custo de render mal calibrado (multi-leg sub-margem) → operação cara vendida abaixo de 4×-floor | 3 | 4 | 12 | OTD-VS-007: medição material no 1º render pago antes de cravar a constante; espelhamento triplo |
> 146	| BR-VS-RISK-007 | Entrega Telegram como bloqueador único (token ausente) → vídeo gerado mas não entregue ao tenant | 3 | 3 | 9 | OTD-VS-003: link soberano sempre disponível; Telegram opcional/per-user; entrega nunca depende só do bot |
> 147	| BR-VS-RISK-008 | CF bot-challenge bloqueia clientes não-browser no design.mcorch.com → editor/automação quebrados | 3 | 3 | 9 | BR-VS-015: WAF Skip rule + token forte + origins restritos; confirmar via origin `--resolve` ou handshake, nunca curl cru |
> 148	| BR-VS-RISK-009 | Licença de provider (modelo/asset) restritiva ou voz clonada sem consentimento → exposição legal LGPD Art. 11 | 2 | 5 | 10 | Tag de proveniência/licença por asset; consentimento explícito p/ clonagem de voz; recusar clonagem não autorizada |
> 149	
> 150	> Probability & Impact: 1=Low, 5=High. RPN = Probability × Impact.
> 151	
> 152	---
> 153	
> 154	## 9. Business Acceptance Criteria
> 155	
> 156	| ID | Criterion | Verification Method |
> 157	|----|-----------|-------------------|
> 158	| BAC-VS-001 | Faceless render E2E produz MP4 ≥100KB no bucket + observação na malha + débito atômico, gateado por JWT | `ls`/`SELECT` do asset + nó na malha + delta `mco_balance`; smoke do render |
> 159	| BAC-VS-002 | HyperFrames editor carrega logado em `/dashboard/canvas/video` e renderiza MP4 determinístico em sandbox | E2E logado 1920×1080 + 2 renders idênticos byte-comparáveis; container de render isolado |
> 160	| BAC-VS-003 | Toda superfície de vídeo rejeita request anônima (401) | Smoke 401 sem token nas 3 superfícies |
> 161	| BAC-VS-004 | Provider resolvido per-user; 402 estruturado quando não configurado; zero env-key global em path user-facing | Smoke 402 `{error, action}` + grep de env global em paths user-facing = 0 |
> 162	| BAC-VS-005 | Débito por render atômico via RPC; refund-on-failure; 402 antes de leg de provider | Delta `mco_balance` por `SELECT` antes/depois (sucesso e falha) |
> 163	| BAC-VS-006 | Portão VLM + consistência precede 100% dos renders pagos de vídeo | Verdict `compare` aprovado registrado antes de cada leg de vídeo |
> 164	| BAC-VS-007 | Link afiliado ML embutido + ≥1 clique atribuído por tenant | `affiliate_links.content_id` NON-NULL + click ledger |
> 165	| BAC-VS-008 | Erasure em cascata remove artefatos de vídeo/áudio/config BYOK com zero resíduo ≤24h | `SELECT` count antes/depois = 0; `/security-review` SAFE da migration |
> 166	| BAC-VS-009 | Ponte de rede Docker resolve DNS de container vision_mcp/chroma a partir do studio + handshake PAT/JWT | `docker exec` ping/handshake MCP entre redes |
> 167	
> 168	---
> 169	
> 170	## 10. Traceability Matrix
> 171	
> 172	| MR ID | BR ID | PR ID (stub) |
> 173	|-------|-------|--------------|
> 174	| MR-VS-001 | BR-VS-001 | _to be linked in PRD_ |
> 175	| MR-VS-002 | BR-VS-002, BR-VS-010 | _to be linked in PRD_ |
> 176	| MR-VS-003 | BR-VS-003, BR-VS-015 | _to be linked in PRD_ |
> 177	| MR-VS-004 | BR-VS-004, BR-VS-014 | _to be linked in PRD_ |
> 178	| MR-VS-005 | BR-VS-005 | _to be linked in PRD_ |
> 179	| MR-VS-006 | BR-VS-006 | _to be linked in PRD_ |
> 180	| MR-VS-007 | BR-VS-007 | _to be linked in PRD_ |
> 181	| MR-VS-008 | BR-VS-008, BR-VS-013 | _to be linked in PRD_ |
> 182	| MR-VS-009 | BR-VS-009 | _to be linked in PRD_ |
> 183	| MR-VS-010 | BR-VS-010 | _to be linked in PRD_ |
> 184	| MR-VS-011 | BR-VS-012 | _to be linked in PRD_ |
> 185	| MR-VS-012 | (UX — PRD §6) | _to be linked in PRD_ |
> 186	| MR-VS-013 | BR-VS-011, BR-VS-013 | _to be linked in PRD_ |
> 187	| MR-VS-014 | BR-VS-016 | _to be linked in PRD_ |
> 188	
> 189	---
> 190	
> 191	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 192	
> ```

## 🤖 Claude *(01:26:26)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/03-prd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# PRD — Product Requirements Document
> 2	
> 3	**Project:** video-studio
> 4	**Version:** v0.1 | **Date:** 2026-06-21
> 5	**BoK Applied:** ProdBOK + CXBOK
> 6	**Status:** Draft
> 7	**Source of Truth (upstream):** `01-mrd.md` (MR-VS-001..014) + `02-brd.md` (BR-VS-001..016) — todo PR-VS rastreia ≥1 BR-VS.
> 8	**Market segment:** B2B2C · **Monetization:** híbrida (mcoCoins por render + afiliado Mercado Livre) · **Regulatory:** LGPD · **Integration surface:** extends-mcorch
> 9	
> 10	---
> 11	
> 12	## 1. Product Vision Statement
> 13	
> 14	> _Format: "For [target user] who [need], [Product Name] is a [category] that [key benefit]. Unlike [alternative], our product [differentiator]."_
> 15	
> 16	Para o **criador faceless e o operador de agência brasileiros** que precisam produzir vídeo vertical em volume, consistente e monetizado sem montar um pipeline manual nem pagar SaaS em dólar, o **MCORCH Video Studio** é um **estúdio de vídeo soberano de dois motores** — geração autônoma E2E (Faceless Studio) + edição programática determinística (HyperFrames Editor) — que entrega vídeo pronto-para-publicar com voz clonada, movimento real, QA por olho criativo e link de afiliado embutido, tudo dentro do cockpit MCORCH. Diferente de HeyGen/Synthesia/Argil (USD, jardim murado, criador não monetiza) e da pilha manual CapCut+ElevenLabs (lenta, sem consistência, sem aprendizado), nosso produto cobra em mcoCoins (R$), resolve credenciais per-user, gateia o gasto caro por um portão de consistência, persiste assets reais e conecta cada render à malha de conhecimento e ao programa de afiliados Mercado Livre.
> 17	
> 18	---
> 19	
> 20	## 2. User Personas
> 21	
> 22	### Persona 1 — Léo, o Criador Faceless (Primary)
> 23	
> 24	| Attribute | Detail |
> 25	|-----------|--------|
> 26	| Role | Criador solo de canais faceless (Shorts/Reels/TikTok) em nicho de produto/curiosidades; quer volume e renda de afiliado |
> 27	| Goals | Produzir 5–10 vídeos verticais/semana, consistentes e monetizados, sem virar editor de vídeo profissional |
> 28	| Frustrations | Pipeline manual de 1–3h por vídeo; cota ElevenLabs em USD; frames inconsistentes; zero atribuição de receita; nada do trabalho acumula |
> 29	| Tech-savviness | 2/5 (sabe usar ferramentas no-code, não programa) |
> 30	| MCORCH usage pattern | Loga em `login.mcorch.com`, escolhe um produto no picker, aciona o Faceless Studio num clique, recebe o vídeo pronto + link afiliado |
> 31	| Quote | _"Eu só quero escolher um produto, apertar um botão e ter um vídeo bom o suficiente pra postar — e ganhar comissão quando alguém compra."_ |
> 32	
> 33	### Persona 2 — Marina, a Operadora de Agência (Secondary)
> 34	
> 35	| Attribute | Detail |
> 36	|-----------|--------|
> 37	| Role | Operadora/editora numa micro-agência que produz vídeo data-driven para vários clientes |
> 38	| Goals | Montar vídeos programáticos determinísticos (reutilizáveis por template), versionáveis, com custo atribuído por cliente, sem rodar servidor local |
> 39	| Frustrations | Remotion exige dev + servidor; SaaS de avatar não dá controle de layout; sem isolamento de credencial por cliente; sem determinismo (cada export sai diferente) |
> 40	| Tech-savviness | 4/5 (lê/edita HTML/CSS/JS, entende timeline e props) |
> 41	| MCORCH usage pattern | Abre `/dashboard/canvas/video`, edita HTML/props na timeline com preview ao vivo, renderiza MP4 determinístico por cliente, debita do plano da agência |
> 42	| Quote | _"Eu preciso que o mesmo template gere o mesmo vídeo, byte a byte, pra cada cliente — e que a chave de um cliente nunca toque a do outro."_ |
> 43	
> 44	---
> 45	
> 46	## 3. User Journey Maps
> 47	
> 48	### Journey: "Do produto ao vídeo monetizado" (Léo, Happy Path)
> 49	
> 50	| Stage | Action | Touchpoint | Emotion | Opportunity |
> 51	|-------|--------|-----------|---------|-------------|
> 52	| Awareness | Vê um vídeo gerado pelo próprio MCORCH e descobre que dá pra automatizar | Conteúdo orgânico / dashboard | 😐 Neutral | CTA "Gerar meu primeiro vídeo" no dashboard |
> 53	| Consideration | Abre o Faceless Studio, vê o picker de produto e o custo em mcoCoins | `/dashboard/canvas/video` (aba Faceless) | 🤔 Curious | Preço transparente + preview de pipeline (roteiro→voz→vídeo→QA) |
> 54	| Activation | Escolhe um produto, aciona o render, acompanha as legs (script→imagem→voz→movimento→QA) | Trigger + status timeline | 😊 Excited | Status ao vivo das legs com microcopy de luxo; QA VLM visível |
> 55	| Value | Recebe o MP4 pronto (≥100KB no bucket) com link afiliado ML embutido + observação na malha | Player + link de download/entrega | 🚀 Delighted | Botão "Publicar" + atribuição de receita visível no ROIWidget |
> 56	| Retention | Volta para gerar lote; reaproveita roteiros via memória semântica; vê comissões acumularem | Histórico + Chroma/mesh search | ❤️ Loyal | Recomendação de próximos produtos/temas baseada na malha; upsell de plano |
> 57	
> 58	#### Edge Case 1: Saldo insuficiente de mcoCoins
> 59	> Léo aciona o render mas não tem mcoCoins suficientes para a operação cara de vídeo. O sistema retorna **HTTP 402** ANTES de qualquer leg de provider, com mensagem PT-BR acionável ("Saldo insuficiente — faça upgrade ou compre mcoCoins") e CTA de upgrade. Nenhum débito parcial, nenhum crédito gasto.
> 60	
> 61	#### Edge Case 2: Frames inconsistentes reprovam no portão VLM
> 62	> O frame-inicial e o frame-final descrevem produtos/cores divergentes. O olho criativo (`compare`) reprova no gate G3. O sistema **NÃO prossegue** para a leg cara de vídeo; oferece regenerar o frame-final com mesmo seed + reference threading mais forte. Custo do gate = 0 (BYOK); o gate evita o desperdício do render caro.
> 63	
> 64	### Journey: "Template determinístico multi-cliente" (Marina, Happy Path)
> 65	
> 66	| Stage | Action | Touchpoint | Emotion | Opportunity |
> 67	|-------|--------|-----------|---------|-------------|
> 68	| Awareness | Procura editor programático que não exija servidor local | `/dashboard/canvas` (botão Video na TopBar) | 😐 Neutral | Botão "Video" ao lado de Pipeline; "edição como código, sem servidor" |
> 69	| Consideration | Abre o editor embedado, vê timeline + preview ao vivo + CodeMirror | `/dashboard/canvas/video` (HyperFrames embed) | 🤔 Curious | Hot reload + preview determinístico; templates iniciais |
> 70	| Activation | Edita HTML/props por cliente, renderiza MP4 determinístico em sandbox | NLE embed + render isolado | 😊 Excited | Render per-tenant sandboxed; status + custo em mcoCoins |
> 71	| Value | Recebe MP4 byte-determinístico, com credencial do cliente isolada e custo atribuído | Player + ledger por cliente | 🚀 Delighted | Atribuição de custo per-cliente; reuso de template |
> 72	| Retention | Versiona templates, gera lotes por cliente, escala a agência sem caos de credencial | Biblioteca de templates + BYOK per-tenant | ❤️ Loyal | Plano Enterprise; isolamento provado vira argumento de venda |
> 73	
> 74	#### Edge Case 1: HTML de tenant tenta acessar credenciais/rede
> 75	> O HTML/JS do tenant tenta ler variáveis de ambiente ou alcançar serviços internos durante o render no Chrome headless. O **sandbox per-render** (container isolado, sem credenciais no env de render, rede restrita) bloqueia o acesso; o render falha de forma segura e gera telemetria, sem vazar nada cross-tenant.
> 76	
> 77	#### Edge Case 2: design.mcorch.com bloqueado por CF bot-challenge
> 78	> Uma automação não-browser tenta alcançar a superfície e recebe **403** do Cloudflare. A mitigação (WAF Skip rule + `OD_API_TOKEN` forte + `OD_ALLOWED_ORIGINS`) permite o tráfego legítimo; a verificação de deploy usa origin `--resolve`/handshake, nunca curl cru (que retorna o challenge HTML).
> 79	
> 80	---
> 81	
> 82	## 4. Feature Inventory (MoSCoW)
> 83	
> 84	> Effort: S=hours, M=days, L=week, XL=sprint. mcoCoins finais SÓ após medição material (OTD-VS-007).
> 85	
> 86	### Must Have (MVP)
> 87	
> 88	| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |
> 89	|----|---------|---------|-----------|--------|-------------|-------|
> 90	| PR-VS-001 | Ponte de rede Docker (`n8n_default` ↔ `mcorch-sovereign-net`) + PAT/JWT do studio destravando vision_mcp + chroma | Léo (infra) | BR-VS-013 | L | — | **Gating do MVP** (R5); OTD-VS-001; sem isso QA/chroma são prosa |
> 91	| PR-VS-002 | Auth MCORCH em todas as superfícies de vídeo (faceless trigger, editor, design.mcorch.com) — 401 anônimo | Léo, Marina | BR-VS-003 | M | — | R3; smoke 401 |
> 92	| PR-VS-003 | Resolução de provider per-user (Gemini + todos) via `decrypted_user_api_keys`; 402 estruturado se não configurado | Léo, Marina | BR-VS-004 | M | — | **Gating do MVP** (R1); API Tenancy fail-closed |
> 93	| PR-VS-004 | Débito atômico por render via `deduct_mco_coins` RPC; 402 antes da leg; refund-on-failure | Léo, Marina | BR-VS-005 | M | conforme op | R2; nunca client-side; delta por `SELECT` |
> 94	| PR-VS-005 | Faceless Studio render E2E (Gemini director/QA → Pollinations → VoxCPM → Remotion → LTX i2v + Ken-Burns fallback → FFmpeg → Gemini-vision QA) | Léo | BR-VS-001 | XL | ~125 (provisório — OTD-VS-007) | Sobre workflow n8n `e7e3beeb58f7411a` (ativar + instrumentar) |
> 95	| PR-VS-006 | Portão de QA por olho criativo VLM + consistência entre frames antes do render caro | Léo | BR-VS-006 | M | 0 (BYOK) | SOP `creative-qa-vision-gate.md` (gate G3); QA grátis via BYOK |
> 96	| PR-VS-007 | Persistência de asset real (vídeo/imagem/áudio) em bucket privado + row de asset | Léo, Marina | BR-VS-009 | M | — | Lei 1; nunca URL efêmera; prova = objeto no bucket |
> 97	| PR-VS-008 | Mesh observation por render `success` + `infra_health_logs` por falha | Léo, Marina | BR-VS-008 | S | EMBED grátis | R4; nó com BR/FR ID rastreável |
> 98	| PR-VS-009 | HyperFrames Editor embedado nativamente (React) em `/dashboard/canvas/video`; rota ANTES de `canvas/:id`; botão "Video" na TopBar | Marina | BR-VS-002 | L | — | Embed nativo (não iframe a dev server); `:id="video"` não sombreia |
> 99	| PR-VS-010 | Sandbox per-render para HTML/JS de tenant (container isolado, sem credencial no env de render) | Marina | BR-VS-010 | L | (incl. no render) | **Gating do render multi-tenant** (OTD-VS-006); `/security-review` |
> 100	
> 101	### Should Have (v1.0)
> 102	
> 103	| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |
> 104	|----|---------|---------|-----------|--------|-------------|-------|
> 105	| PR-VS-011 | HyperFrames render → MP4 determinístico (Chrome headless + FFmpeg) com custo atômico | Marina | BR-VS-002, BR-VS-005 | M | ~12 (provisório — OTD-VS-007) | 2 renders byte-idênticos; débito atômico |
> 106	| PR-VS-012 | Link afiliado Mercado Livre embutido + UTM + atribuição de receita/clique per-tenant | Léo | BR-VS-007 | M | — | `affiliate_links.content_id` NON-NULL + click ledger |
> 107	| PR-VS-013 | BYOK per-user real no open-design (fechar single-tenant): daemon per-job / `od` stateless / container por tenant | Marina | BR-VS-014 | L | — | OTD-VS-002; gate antes do 2º tenant |
> 108	| PR-VS-014 | Hardening design.mcorch.com (`OD_API_TOKEN` forte + `OD_ALLOWED_ORIGINS` + CF WAF Skip rule) | Marina | BR-VS-015 | M | — | Substitui `development_token`; editor logado sem CF challenge |
> 109	| PR-VS-015 | Memória semântica de roteiro/vídeo (ChromaDB API v2 / malha com embed) pesquisável e reutilizável | Léo | BR-VS-011 | M | EMBED grátis | Reuso de roteiro; base de recomendação |
> 110	| PR-VS-016 | Erasure LGPD em cascata no `delete-account` (vídeo/áudio/config BYOK/`OD_DATA_DIR`) + teste zero-resíduo | Léo, Marina | BR-VS-016 | L | — | **Gate de GA**; precedente `erase_vision_artifacts` / Canvas Design OTD-008 |
> 111	| PR-VS-017 | Entrega configurável (link soberano sempre; Telegram opcional per-user/sistema) | Léo | BR-VS-012 | M | — | OTD-VS-003; entrega nunca depende só do bot |
> 112	
> 113	### Could Have (Future)
> 114	
> 115	| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |
> 116	|----|---------|---------|-----------|--------|-------------|-------|
> 117	| PR-VS-020 | Render em lote (campanha de N vídeos por lista de produtos) com pré-débito atômico | Léo | BR-VS-001, BR-VS-005 | L | N × custo de render | Análogo a campaign-run; pré-débito + refund |
> 118	| PR-VS-021 | Recomendação de próximo tema/produto via malha (GraphRAG sobre roteiros passados) | Léo | BR-VS-011 | M | 1 (mesh.search) | Acúmulo de aprendizado vira sugestão |
> 119	| PR-VS-022 | Biblioteca de templates HyperFrames versionados reutilizáveis entre clientes | Marina | BR-VS-002 | M | — | Reuso determinístico; argumento Enterprise |
> 120	| PR-VS-023 | Publicação direta nas redes (auto-publish) a partir do vídeo gerado, gateada por credencial social per-user | Léo | BR-VS-007, BR-VS-012 | L | — | Reusa `publish-social`/`publish-meta`; ToS de plataforma |
> 121	
> 122	### Won't Have (This Cycle)
> 123	
> 124	- Avatar fotorrealista / talking-head (o módulo é **faceless** por definição — fora de escopo).
> 125	- Reescrita do workflow n8n do zero (instrumentamos o existente `e7e3beeb58f7411a`, não recriamos).
> 126	- Edição colaborativa multi-usuário em tempo real no HyperFrames Editor.
> 127	- Treinamento de modelo próprio de voz/imagem (usamos providers via BYOK).
> 128	- Exposição pública/anônima de qualquer superfície de vídeo (viola R3).
> 129	
> 130	---
> 131	
> 132	## 5. Release Phasing
> 133	
> 134	### MVP Scope
> 135	**Target date:** após destravar os 2 gates de infra
> 136	**Included:** PR-VS-001, PR-VS-002, PR-VS-003, PR-VS-004, PR-VS-005, PR-VS-006, PR-VS-007, PR-VS-008
> 137	**Success gate:** Faceless render E2E `success` (MP4 ≥100KB no bucket) gateado por JWT, debitado atomicamente, precedido de portão VLM, com observação na malha — **condicionado a (1) PR-VS-001 ponte de rede Docker (R5) e (2) PR-VS-003 BYOK per-user (R1) selados primeiro**. Sem esses dois, o MVP NÃO arranca: a fiação vision-QA/chroma é prosa e o billing não atribui por tenant.
> 138	
> 139	### v1.0 Scope
> 140	**Target date:** após o MVP estabilizar
> 141	**Adds:** PR-VS-009, PR-VS-010, PR-VS-011, PR-VS-012, PR-VS-013, PR-VS-014, PR-VS-015, PR-VS-016, PR-VS-017
> 142	**Success gate:** HyperFrames Editor embedado renderiza MP4 determinístico em sandbox per-render (OTD-VS-006); BYOK per-user no open-design fechado (OTD-VS-002); link afiliado atribuído; **erasure LGPD em cascata (PR-VS-016) selada como gate de GA antes do 2º tenant externo**.
> 143	
> 144	### Future Scope
> 145	**Items:** PR-VS-020, PR-VS-021, PR-VS-022, PR-VS-023
> 146	**Condition:** segmento agência ativado em escala + demanda de lote/publicação direta comprovada; cada item entra após métrica de uso do v1.0.
> 147	
> 148	---
> 149	
> 150	## 6. Luxury UX Specifications
> 151	
> 152	### 6.1 Color & Visual Identity
> 153	
> 154	| Token | Value | Usage |
> 155	|-------|-------|-------|
> 156	| `--bg-deep` | `#0A0A0F` | Canvas background do editor e do studio |
> 157	| `--accent-violet` | `#7C3AED` | CTA primário (Gerar vídeo / Render), estados ativos da timeline |
> 158	| `--accent-cyan` | `#06B6D4` | Highlights de dados (custo mcoCoins, status das legs, QA pass) |
> 159	| `--glass-surface` | `rgba(255,255,255,0.04)` | Cards de status de render, painel de propriedades |
> 160	| `--border-subtle` | `rgba(255,255,255,0.08)` | Bordas de card, divisores da timeline |
> 161	
> 162	### 6.2 Animation Guidelines
> 163	
> 164	| Element | Library | Duration | Easing |
> 165	|---------|---------|----------|--------|
> 166	| Transição de aba (Faceless ↔ Editor) | Framer Motion | 300ms | `easeInOut` |
> 167	| Entrada de card de leg de pipeline | Framer Motion | 500ms | `spring(stiffness:80)` |
> 168	| Pulso de status "rendering" | CSS keyframes | 2s | `ease-in-out infinite` |
> 169	| Micro-interações (hover botão Render, scrub da timeline) | Framer Motion | 150ms | `easeOut` |
> 170	
> 171	### 6.3 Interaction Patterns
> 172	
> 173	- **Cards de status de render:** glass morphism — `backdrop-blur-sm`, borda sutil, sombra `0 4px 24px rgba(0,0,0,0.4)`; cada leg (script/imagem/voz/movimento/QA) com seu próprio chip de estado.
> 174	- **Botões:** gradiente na borda em hover; nunca fill chapado para o CTA primário "Gerar vídeo"/"Render".
> 175	- **Loading de render:** skeleton shimmer + status timeline das legs (nunca spinner cru para a área de conteúdo).
> 176	- **Preview do editor:** preview ao vivo determinístico com hot reload; scrub suave na timeline.
> 177	- **Toasts:** `sonner`; sucesso = violeta, erro = vermelho (mensagem PT-BR acionável), info = ciano.
> 178	- **Custo:** chip de mcoCoins sempre visível antes do render (transparência de preço) + estado 402 com CTA de upgrade.
> 179	
> 180	### 6.4 Accessibility (WCAG 2.1 AA)
> 181	
> 182	- Contraste ≥ 4.5:1 para todo texto sobre glass surfaces.
> 183	- Timeline e player totalmente navegáveis por teclado; controles com ARIA labels.
> 184	- Labels ARIA em botões icon-only (play, render, add scene).
> 185	- Indicadores de foco visíveis ≥ 2px; legendas/captions do vídeo respeitam contraste.
> 186	
> 187	---
> 188	
> 189	## 7. Acceptance Criteria (Gherkin)
> 190	
> 191	```gherkin
> 192	Feature: MCORCH Video Studio — geração autônoma e edição programática
> 193	
> 194	  Scenario: Faceless render E2E gateado, debitado e QA-aprovado (PR-VS-005, PR-VS-004, PR-VS-006)
> 195	    Given um tenant autenticado com JWT MCORCH válido e provider Gemini configurado per-user
> 196	    And saldo de mcoCoins suficiente para a operação de vídeo
> 197	    When ele aciona o Faceless Studio para um produto escolhido
> 198	    Then o sistema debita o custo via deduct_mco_coins RPC de forma atômica
> 199	    And o pipeline roda script -> imagem -> voz -> movimento -> overlays -> composite
> 200	    And o portão VLM aprova a consistência dos frames antes da leg cara de vídeo
> 201	    And o vídeo final (MP4 >= 100KB) é persistido no bucket privado com row de asset
> 202	    And uma observação é inserida na malha com BR/FR ID rastreável
> 203	
> 204	  Scenario: Saldo insuficiente bloqueia antes de qualquer leg (PR-VS-004)
> 205	    Given um tenant autenticado sem mcoCoins suficientes
> 206	    When ele aciona o render de vídeo
> 207	    Then o sistema retorna HTTP 402 antes de qualquer chamada de provider
> 208	    And nenhum mcoCoin é debitado
> 209	    And a UI mostra mensagem PT-BR acionável com CTA de upgrade
> 210	
> 211	  Scenario: Frames inconsistentes reprovam no portão e poupam crédito (PR-VS-006)
> 212	    Given um frame-inicial e um frame-final gerados
> 213	    When o olho criativo executa compare nos dois frames
> 214	    And os atributos-chave (produto, cores, identidade) divergem
> 215	    Then o sistema NÃO prossegue para a leg cara de vídeo
> 216	    And oferece regenerar o frame-final com mesmo seed e reference threading
> 217	    And o custo do gate VLM é 0 (BYOK)
> 218	
> 219	  Scenario: HyperFrames render é determinístico e sandboxed (PR-VS-009, PR-VS-010, PR-VS-011)
> 220	    Given uma operadora autenticada em /dashboard/canvas/video
> 221	    When ela renderiza o mesmo template HTML duas vezes
> 222	    Then os dois MP4 são byte-idênticos (determinístico)
> 223	    And cada render roda em sandbox isolado sem credenciais compartilhadas no env
> 224	    And o HTML do tenant não alcança rede interna nem variáveis de ambiente
> 225	
> 226	  Scenario: Request anônima é rejeitada em toda superfície (PR-VS-002)
> 227	    Given uma request sem JWT/sessão MCORCH
> 228	    When ela atinge o trigger faceless, o editor ou design.mcorch.com
> 229	    Then o sistema responde HTTP 401
> 230	    And nenhuma operação é executada
> 231	
> 232	  Scenario: Provider não configurado falha fechado com ação (PR-VS-003)
> 233	    Given um tenant autenticado sem chave de provider per-user
> 234	    When ele aciona uma leg que exige o provider
> 235	    Then o sistema retorna HTTP 402 estruturado { error, action }
> 236	    And nenhuma chave global é usada no path user-facing
> 237	```
> 238	
> 239	---
> 240	
> 241	## 8. Traceability Matrix
> 242	
> 243	| MR ID | BR ID | PR ID |
> 244	|-------|-------|-------|
> 245	| MR-VS-001 | BR-VS-001 | PR-VS-005, PR-VS-020 |
> 246	| MR-VS-002 | BR-VS-002, BR-VS-010 | PR-VS-009, PR-VS-010, PR-VS-011, PR-VS-022 |
> 247	| MR-VS-003 | BR-VS-003, BR-VS-015 | PR-VS-002, PR-VS-014 |
> 248	| MR-VS-004 | BR-VS-004, BR-VS-014 | PR-VS-003, PR-VS-013 |
> 249	| MR-VS-005 | BR-VS-005 | PR-VS-004, PR-VS-011 |
> 250	| MR-VS-006 | BR-VS-006 | PR-VS-006 |
> 251	| MR-VS-007 | BR-VS-007 | PR-VS-012, PR-VS-023 |
> 252	| MR-VS-008 | BR-VS-008, BR-VS-013 | PR-VS-001, PR-VS-008 |
> 253	| MR-VS-009 | BR-VS-009 | PR-VS-007 |
> 254	| MR-VS-010 | BR-VS-010 | PR-VS-010 |
> 255	| MR-VS-011 | BR-VS-012 | PR-VS-017 |
> 256	| MR-VS-012 | (UX house style) | §6 (todas as superfícies humanas) |
> 257	| MR-VS-013 | BR-VS-011, BR-VS-013 | PR-VS-001, PR-VS-015, PR-VS-021 |
> 258	| MR-VS-014 | BR-VS-016 | PR-VS-016 |
> 259	
> 260	---
> 261	
> 262	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 263	
> ```

## 🤖 Claude *(01:26:26)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# FRD — Functional Requirements Document
> 2	
> 3	**Project:** video-studio
> 4	**Version:** v0.1 | **Date:** 2026-06-21
> 5	**BoK Applied:** SWEBOK v4 (Software Requirements) + CISSP CBK 2024 (Security Requirements)
> 6	**Status:** Draft
> 7	**Source of Truth (upstream):** `01-mrd.md` (MR-VS-001..014) + `02-brd.md` (BR-VS-001..016) + `03-prd.md` (PR-VS-001..023) — todo FR-VS/NFR-VS rastreia ≥1 PR-VS; ambiguidade vira OTD-VS, nunca improvisação.
> 8	**Market segment:** B2B2C · **Monetization:** híbrida (mcoCoins por render + afiliado Mercado Livre) · **Regulatory:** LGPD (voz clonada = biométrico potencial, Art. 11) · **Integration surface:** extends-mcorch.
> 9	**Five Unbreakable Rules (Sovereign 2026-06-21) honored across this document:** R1 BYOK per-user · R2 mcoCoins gatekeeper atômico · R3 auth MCORCH nos apps isolados · R4 conexão à malha · R5 ponte de rede Docker.
> 10	
> 11	---
> 12	
> 13	## 1. Scope Statement
> 14	
> 15	Este documento especifica os requisitos funcionais e não-funcionais do `video-studio` — o módulo de produção de vídeo do MCORCH entregue como **dois sub-sistemas criativos isolados** governados pelo cockpit soberano: **(A) FACELESS STUDIO** (geração autônoma E2E sobre o workflow n8n existente `e7e3beeb58f7411a`) e **(B) HYPERFRAMES EDITOR** (edição programática HTML→MP4 determinística, embedada nativamente em `/dashboard/canvas/video`). Deriva do PRD `03-prd.md` e alimenta diretamente o SDD `05-sdd.md`.
> 16	
> 17	**In scope:**
> 18	- Auth MCORCH (JWT/sessão) gating de TODA superfície de vídeo — faceless trigger, editor HyperFrames, `design.mcorch.com` (R3 · PR-VS-002).
> 19	- Resolução de provider per-user (Gemini e todos) via `decrypted_user_api_keys`, fail-closed (R1 · PR-VS-003).
> 20	- Débito atômico por render via `deduct_mco_coins` RPC, 402 antes da leg, refund-on-failure (R2 · PR-VS-004).
> 21	- Pipeline faceless E2E instrumentado (Gemini director/QA → Pollinations → VoxCPM → Remotion → LTX i2v + Ken-Burns fallback → FFmpeg composite → Gemini-vision QA → entrega · PR-VS-005).
> 22	- Portão de QA por olho criativo VLM + consistência entre frames antes do gasto caro (PR-VS-006).
> 23	- Persistência de asset real em bucket privado + row de asset (Lei 1 · PR-VS-007).
> 24	- Mesh observation por `success` + `infra_health_logs` por falha + memória semântica Chroma/malha (R4 · PR-VS-008, PR-VS-015).
> 25	- HyperFrames embedado nativamente (React) com botão "Video" na TopBar e rota declarada ANTES de `canvas/:id` (PR-VS-009); render determinístico (PR-VS-011); sandbox per-render de HTML não-confiável (PR-VS-010).
> 26	- Ponte de rede Docker `n8n_default` ↔ `mcorch-sovereign-net` + PAT/JWT do studio (R5 · PR-VS-001).
> 27	- Monetização afiliada ML + atribuição (PR-VS-012); BYOK per-user no open-design (PR-VS-013); hardening `design.mcorch.com` (PR-VS-014); erasure LGPD em cascata (PR-VS-016); entrega configurável/Telegram opcional (PR-VS-017).
> 28	
> 29	**Out of scope:** avatar fotorrealista/talking-head (módulo é faceless por definição); reescrita do workflow n8n do zero (instrumenta-se o existente); edição colaborativa multi-usuário em tempo real; treinamento de modelo próprio de voz/imagem; exposição pública/anônima de qualquer superfície (viola R3); render em lote (PR-VS-020, Future); publicação direta nas redes (PR-VS-023, Future).
> 30	
> 31	---
> 32	
> 33	## 2. Functional Requirements
> 34	
> 35	> Priority: `Critical` | `High` | `Medium` · Category: `UI` | `Hook` | `EdgeFunction` | `DB` | `Cron` | `Container`
> 36	> Cada FR rastreia ≥1 PR-VS. Test IDs (AT-VS-NNN) materializam no §6.
> 37	
> 38	### 2.1 Auth & Identity (R3)
> 39	
> 40	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 41	|----|-------|-------------|----------|-----------|----------|---------|
> 42	| FR-VS-001 | Auth gate — faceless trigger | A edge function `video-faceless-render` valida JWT MCORCH (`supabase.auth.getUser`) ANTES de qualquer lógica; request sem `Authorization` → 401; token inválido/expirado → 401. Nenhuma operação executa anonimamente. | Critical | PR-VS-002 | EdgeFunction | AT-VS-001 |
> 43	| FR-VS-002 | Auth gate — HyperFrames editor | A rota `/dashboard/canvas/video` é protegida por `DashboardLayout`/`ProtectedRoute`; sessão ausente redireciona para `/auth`; a edge function `video-hyperframes-render` valida JWT antes do render. | Critical | PR-VS-002, PR-VS-009 | UI/EdgeFunction | AT-VS-002 |
> 44	| FR-VS-003 | Auth gate — design.mcorch.com | O acesso ao editor open-design via `design.mcorch.com` exige `OD_API_TOKEN` forte (não `development_token`), `OD_ALLOWED_ORIGINS=https://login.mcorch.com`, e CF WAF Skip rule p/ requests não-browser legítimos; request sem origem permitida/token → 401/403. | Critical | PR-VS-002, PR-VS-014 | Container | AT-VS-003 |
> 45	| FR-VS-004 | Studio service identity (PAT/JWT) | A identidade do Faceless Studio (n8n/worker) para chamar `mcorch_vision_mcp` é um PAT MCORCH emitido (`mcp_access_tokens`, scopes `vision:read`/`mesh:write`) OU JWT de service-identity; handshake MCP+PAT prova a conexão. Sem PAT/JWT → 401 no vision_mcp. | Critical | PR-VS-001 | Container | AT-VS-004 |
> 46	
> 47	### 2.2 Per-User Credentials / BYOK (R1)
> 48	
> 49	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 50	|----|-------|-------------|----------|-----------|----------|---------|
> 51	| FR-VS-005 | Per-user provider resolution (fail-closed) | Toda leg que usa provider externo (Gemini director/QA, OCR, VLM, image) resolve a credencial por `user_id = auth.uid()` em `decrypted_user_api_keys` (VIEW Vault mascarada); se ausente → HTTP 402 estruturado `{ error: "<service>_not_configured", action: "Configure suas credenciais em /dashboard/settings" }`. Zero `Deno.env.get('<SERVICE>_API_KEY')` em path user-facing. | Critical | PR-VS-003 | EdgeFunction/Container | AT-VS-005 |
> 52	| FR-VS-006 | Env-global fallback restrito | `Deno.env.get` de chave global SÓ é permitido em cron/service-role (sem `auth.uid()`), onboarding default explícito, ou paths de trigger sem JWT; nunca como caminho primário user-facing. Auditável por grep = 0 menções globais em paths user-facing. | Critical | PR-VS-003 | EdgeFunction | AT-VS-005 |
> 53	| FR-VS-007 | BYOK isolation — open-design (re-arquitetura) | O open-design (`od` cliente fino → daemon compartilhado) DEVE isolar provider por tenant por uma das vias OTD-VS-002 (daemon per-job efêmero / `od` stateless / container por tenant); fechar o single-tenant `/app/.od/media-config.json` global. 2 tenants com providers distintos não compartilham config. | High | PR-VS-013 | Container | AT-VS-013 |
> 54	| FR-VS-008 | BYOK write pattern (VIEW Vault) | Escrita de credencial de provider de vídeo segue o padrão Vault: `.insert` (NUNCA `.upsert`), null não limpa (clear via RPC dedicado), teste de chave server-side (a UI só vê o mask `••••`). | High | PR-VS-003 | Hook/DB | AT-VS-005 |
> 55	
> 56	### 2.3 Economics / mcoCoins Gatekeeper (R2)
> 57	
> 58	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 59	|----|-------|-------------|----------|-----------|----------|---------|
> 60	| FR-VS-009 | Atomic deduct — faceless render | `video-faceless-render` debita `VIDEO_FACELESS_RENDER` mco via `deduct_mco_coins(p_user_id, p_amount, ...)` RPC ANTES de qualquer leg de provider; saldo insuficiente → HTTP 402 (nenhuma leg roda, nada debitado). Nunca client-side. | Critical | PR-VS-004, PR-VS-005 | EdgeFunction | AT-VS-009 |
> 61	| FR-VS-010 | Atomic deduct — HyperFrames render | `video-hyperframes-render` debita `VIDEO_HYPERFRAMES_RENDER` mco via RPC antes do render Chrome+FFmpeg; 402 em saldo insuficiente. | Critical | PR-VS-004, PR-VS-011 | EdgeFunction | AT-VS-010 |
> 62	| FR-VS-011 | Refund-on-failure (idempotente) | Falha de qualquer leg APÓS o débito → refund crédito-positivo idempotente (guard por `render_id`/`job_id`, espelha `finalize_vision_job`/`refundMco`); a função de refund nunca lança. Delta `mco_balance` por `SELECT` prova o crédito. | Critical | PR-VS-004 | EdgeFunction/DB | AT-VS-011 |
> 63	| FR-VS-012 | QA via BYOK = custo 0 | O portão de QA (`vision.describe_image`/`analyze_video`/`compare` via vision_mcp) resolve a chave per-user → custo 0 mco no path BYOK; path plataforma (sem BYOK) debita `VIDEO_QA_VLM` (2 mco). QA grátis remove fricção do gate de consistência. | High | PR-VS-006 | Container | AT-VS-006 |
> 64	| FR-VS-013 | Cost calibration (4×-floor) | As classes `VIDEO_FACELESS_RENDER` (~125 provisório) e `VIDEO_HYPERFRAMES_RENDER` (~12 provisório) seguem o modelo `mco = ceil(usd/$0.018×4)`; espelhamento triplo (`src/lib/billing.ts` + constante do serviço + `billing.test.ts`); classe final SÓ após medição material no 1º render pago (OTD-VS-007). | Critical | PR-VS-004 | DB/Container | AT-VS-013 |
> 65	
> 66	### 2.4 Faceless Studio pipeline (núcleo segmento primário)
> 67	
> 68	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 69	|----|-------|-------------|----------|-----------|----------|---------|
> 70	| FR-VS-014 | Faceless render orchestration | `video-faceless-render` aciona o workflow n8n `e7e3beeb58f7411a` (ativá-lo + instrumentá-lo) com o tema/produto + identidade do tenant; o cérebro loopa por cena: Gemini director → Pollinations (imagem) → VoxCPM (TTS voz clonada) → Remotion (HUD/captions) → LTX HF i2v (Ken-Burns fallback) → FFmpeg composite → Gemini-vision QA → entrega. | Critical | PR-VS-005 | EdgeFunction/Container | AT-VS-014 |
> 71	| FR-VS-015 | n8n asset bootstrap | Os helper scripts `n8n/scripts/ltx.js` + `composite.sh` são copiados para `/home/node/.n8n/assets/` no container `n8n-n8n-1`; `scripts/gen-sfx.sh` constrói a biblioteca de SFX procedural via `docker exec n8n-n8n-1` ffmpeg lavfi. Render falha-cedo com erro claro se os assets faltam. | High | PR-VS-005 | Container | AT-VS-015 |
> 72	| FR-VS-016 | LTX i2v + Ken-Burns fallback | A leg de movimento usa o HF Space `lightricks-ltx-video-distilled` (ZeroGPU ~5 GPU-min/dia grátis); ao exceder a cota/timeout, faz fallback determinístico para Ken-Burns (pan/zoom FFmpeg) sem custo de GPU. O render nunca trava por cota de GPU. | High | PR-VS-005 | Container | AT-VS-016 |
> 73	| FR-VS-017 | Product-aware script + monetização | O director Gemini gera roteiro product-aware (quando há produto escolhido); as 3 superfícies de texto/entrega recebem link afiliado ML + UTM; `affiliate_links.content_id` NON-NULL liga o link ao asset gerado. | High | PR-VS-012 | EdgeFunction | AT-VS-012 |
> 74	| FR-VS-018 | Delivery (sovereign-first, Telegram opcional) | A entrega do vídeo é SEMPRE via link soberano (signed URL do bucket privado); Telegram é canal OPCIONAL (per-user ou sistema, OTD-VS-003); ausência de `TELEGRAM_BOT_TOKEN` nunca bloqueia a entrega. | Medium | PR-VS-017 | EdgeFunction/Container | AT-VS-017 |
> 75	
> 76	### 2.5 Quality Gate (olho criativo VLM)
> 77	
> 78	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 79	|----|-------|-------------|----------|-----------|----------|---------|
> 80	| FR-VS-019 | Consistency gate (G3) pré-render caro | Antes da leg cara de vídeo (LTX i2v / DoP), o olho criativo executa `compare` (`vision.describe_image` nos frames inicial+final); atributos-chave divergentes (produto/cores/identidade) → o sistema NÃO prossegue; oferece regenerar o frame-final com mesmo seed + reference threading. Custo do gate = 0 (BYOK). | High | PR-VS-006 | Container | AT-VS-006 |
> 81	| FR-VS-020 | Post-render video QA | Após o render, `vision.analyze_video` descreve a cena; `confidence ≥ medium` + coerência com os frames sela o sucesso de qualidade; verdict registrável na malha (1 mco, opcional). | Medium | PR-VS-006 | Container | AT-VS-006 |
> 82	
> 83	### 2.6 HyperFrames Editor (núcleo segmento secundário)
> 84	
> 85	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 86	|----|-------|-------------|----------|-----------|----------|---------|
> 87	| FR-VS-021 | Native React embed | O editor HyperFrames é embedado NATIVAMENTE via os componentes React exportados pelo `@hyperframes/studio` (`StudioApp`, `NLELayout`, `NLEPreview`, `Player`, `Timeline`, `SourceEditor`, `PropertyPanel`) — NÃO um iframe a um dev server `npx hyperframes preview`. Renderiza timeline + preview ao vivo + CodeMirror + hot reload dentro do cockpit. | Critical | PR-VS-009 | UI | AT-VS-021 |
> 88	| FR-VS-022 | Route ordering — canvas/video before canvas/:id | A rota `canvas/video` é declarada ANTES de `canvas/:id` em `src/App.tsx` (senão `:id="video"` sombreia a nova rota). O componente da rota é lazy-loaded. | Critical | PR-VS-009 | UI | AT-VS-022 |
> 89	| FR-VS-023 | "Video" button na TopBar | Um botão "Video" senta ao lado do botão "Pipeline" em `src/components/canvas/TopBar.tsx`; clicar navega para `/dashboard/canvas/video`. | High | PR-VS-009 | UI | AT-VS-023 |
> 90	| FR-VS-024 | Deterministic MP4 render | `video-hyperframes-render` produz MP4 via Chrome headless (Puppeteer) + FFmpeg de forma DETERMINÍSTICA: o mesmo template HTML/CSS/JS + media + props renderiza dois MP4 byte-idênticos. | High | PR-VS-011 | EdgeFunction/Container | AT-VS-024 |
> 91	| FR-VS-025 | Per-render sandbox (untrusted HTML) | O render de HTML/JS de tenant roda em sandbox isolado per-render (container efêmero, rede restrita, ZERO credencial de tenant no env de render); o HTML do tenant não alcança rede interna nem variáveis de ambiente (OTD-VS-006). Gate de `/security-review` obrigatório. | High | PR-VS-010 | Container | AT-VS-025 |
> 92	
> 93	### 2.7 Mesh & Memory (R4)
> 94	
> 95	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 96	|----|-------|-------------|----------|-----------|----------|---------|
> 97	| FR-VS-026 | Observation node on success | Cada render `success` insere um nó `observation` em `mcorch_nodes` (`user_id + project_id`, embed-on-insert via trigger `embed-mcorch-node`), com `metadata` carregando `fr_id`/`br_id` rastreável + `cost_mco` + `render_id`. NUNCA system node (`user_id IS NULL`) para conteúdo de tenant. | High | PR-VS-008 | DB/Container | AT-VS-008 |
> 98	| FR-VS-027 | infra_health_logs on failure | Cada falha de leg/render insere uma row em `infra_health_logs` com `service='video-studio'`, `event`, `metadata` (allowlist — sem PII per-tenant na tabela global-read), em todo path success/degraded/error. | High | PR-VS-008 | DB/Container | AT-VS-008 |
> 99	| FR-VS-028 | Semantic script/video memory | Roteiro + verdict de QA são persistidos para busca semântica via ChromaDB API v2 (`127.0.0.1:8001`) e/ou `mcorch_nodes` com embed; pesquisável por `mesh.search`/Chroma após o render, base para reuso/recomendação. | Medium | PR-VS-015 | Container | AT-VS-015b |
> 100	
> 101	### 2.8 Infra Bridge & Assets (R5 + Lei 1)
> 102	
> 103	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 104	|----|-------|-------------|----------|-----------|----------|---------|
> 105	| FR-VS-029 | Docker network bridge | O studio (n8n/remotion em `n8n_default`) alcança `mcorch_vision_mcp` (`127.0.0.1:3200`) e `mcorch_chroma` (`127.0.0.1:8001`) em `constellation-orchestra_mcorch-sovereign-net` via a estratégia de bridge escolhida (OTD-VS-001: attach-to-sovereign-net vs proxy dedicado). DNS de container resolve entre redes. | Critical | PR-VS-001 | Container | AT-VS-004 |
> 106	| FR-VS-030 | Real asset persistence | Todo vídeo/imagem/áudio gerado termina como objeto material em bucket privado (`generated-videos`/`video-studio-assets`) com row de asset (`storage_key`/`public_url`); nunca confiar em URL efêmera do provider. Prova = objeto no bucket (≥100KB p/ vídeo), não a resposta da API. | High | PR-VS-007 | DB/Container | AT-VS-007 |
> 107	
> 108	### 2.9 LGPD / Compliance
> 109	
> 110	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 111	|----|-------|-------------|----------|-----------|----------|---------|
> 112	| FR-VS-031 | Cascade erasure (delete-account) | O `delete-account` purga em cascata: artefatos de vídeo/imagem/áudio (bucket + rows), config BYOK de vídeo, `OD_DATA_DIR`/`OD_MEDIA_CONFIG_DIR` do open-design, e nós/embeddings de roteiro na malha; teste de zero-resíduo (`SELECT` count antes/depois = 0) ≤24h. Gate de GA. | High | PR-VS-016 | EdgeFunction/DB | AT-VS-016b |
> 113	| FR-VS-032 | Cloned-voice consent | A leg VoxCPM (clonagem de voz) exige consentimento explícito quando a amostra deriva de pessoa identificável (LGPD Art. 11); o sistema recusa clonagem não autorizada e nunca expõe/treina template biométrico de terceiros sem consentimento. | High | PR-VS-016 | EdgeFunction/Container | AT-VS-016c |
> 114	
> 115	---
> 116	
> 117	## 3. Non-Functional Requirements
> 118	
> 119	| ID | Category | Requirement | Target | Measurement |
> 120	|----|----------|-------------|--------|-------------|
> 121	| NFR-VS-001 | Performance | Faceless render trigger ACK (job aceito, débito feito, worker disparado) | p95 < 3s (submit; o render é async) | Edge logs + smoke do submit |
> 122	| NFR-VS-002 | Performance | HyperFrames render wall-clock (clip curto ≤30s, 1080×1920) | p95 < 90s | Container timing logs |
> 123	| NFR-VS-003 | Performance | Editor embed first interaction (timeline/preview navegável) | LCP < 2.5s | Lighthouse CI |
> 124	| NFR-VS-004 | Performance | Vision QA gate (`compare` 2 frames via BYOK) | p95 < 6s | vision_mcp telemetry |
> 125	| NFR-VS-005 | Scalability | Renders faceless concorrentes sem degradação (single-replica n8n/remotion) | ≥ 3 jobs em fila estável; LTX cota ~5 GPU-min/dia respeitada via fallback | Load test + queue depth |
> 126	| NFR-VS-006 | Scalability | Renders HyperFrames concorrentes (sandbox per-render) | ≥ 5 containers efêmeros sem contenção de host | Load test |
> 127	| NFR-VS-007 | Availability | Uptime SLO das superfícies de vídeo (studio + editor + vision_mcp bridge) | 99.0%/mês | Watchdog `infra_health_logs` |
> 128	| NFR-VS-008 | Security | Toda edge function valida JWT antes de lógica de negócio | 100% | `/security-review` + grep de entrypoints |
> 129	| NFR-VS-009 | Security | Zero credencial de tenant no env do sandbox de render HTML | 0 vazamentos | `/security-review` + inspeção de env do container de render |
> 130	| NFR-VS-010 | Security | Zero `Deno.env.get('<SERVICE>_API_KEY')` em path user-facing | 0 | grep auditável (`scripts/qa/`) |
> 131	| NFR-VS-011 | Security | RLS default-deny em toda tabela nova; financeiras com RESTRICTIVE no-delete | 100% | `/security-review` da migration |
> 132	| NFR-VS-012 | Security | `design.mcorch.com`: token forte + origins restritos + WAF Skip (não `development_token`) | token rotacionado; origins = `https://login.mcorch.com` | Handshake via origin `--resolve` |
> 133	| NFR-VS-013 | Maintainability | Lógica de negócio em hooks (`src/hooks/`); componentes display-only; complexidade ciclomática/hook | ≤ 10 | ESLint |
> 134	| NFR-VS-014 | Maintainability | Cost classes espelhadas em 3 lugares (billing.ts + serviço + test) | drift = 0 | `billing.test.ts` |
> 135	| NFR-VS-015 | Compliance | Erasure em cascata completa ≤24h da chamada `delete-account` | zero resíduo | `SELECT` count antes/depois |
> 136	| NFR-VS-016 | Determinism | HyperFrames: 2 renders do mesmo input → byte-idênticos | hash igual | `sha256sum` comparado |
> 137	| NFR-VS-017 | Accessibility | Superfícies humanas (picker, timeline, player) WCAG 2.1 AA; contraste ≥ 4.5:1; teclado-navegável | AA | Auditoria axe + E2E 1920×1080 |
> 138	
> 139	---
> 140	
> 141	## 4. Interface Requirements
> 142	
> 143	### 4.1 UI → Hook → Edge Function / Container Contract
> 144	
> 145	```
> 146	[Component: VideoStudioPage / FacelessStudioPanel]   (display-only)
> 147	  ↓ calls
> 148	[Hook: useFacelessRender]                            (TanStack Query mutation)
> 149	  ↓ POST + JWT
> 150	[Edge Function: video-faceless-render]               (JWT gate → BYOK resolve → deduct_mco_coins → enqueue)
> 151	  ↓ trigger (PAT/JWT do studio, via bridge R5)
> 152	[Container: n8n e7e3beeb58f7411a + remotion-render]  (Gemini/Pollinations/VoxCPM/Remotion/LTX/FFmpeg)
> 153	  ↓ vision QA (PAT) + mesh write
> 154	[Container: mcorch_vision_mcp + mcorch_chroma]       (QA gate + semantic memory)
> 155	  ↓ writes
> 156	[Storage bucket: video-studio-assets] + [DB: video_renders, mcorch_nodes, infra_health_logs]
> 157	```
> 158	
> 159	```
> 160	[Component: HyperFramesEditor (native embed)]        (StudioApp/NLELayout/Timeline/SourceEditor)
> 161	  ↓ calls
> 162	[Hook: useHyperframesRender]                         (TanStack Query mutation)
> 163	  ↓ POST + JWT
> 164	[Edge Function: video-hyperframes-render]            (JWT gate → deduct_mco_coins → spawn sandbox)
> 165	  ↓ spawn (per-render isolated container — OTD-VS-006)
> 166	[Container: hyperframes-render (ephemeral)]          (headless Chrome/Puppeteer + FFmpeg, no creds in env)
> 167	  ↓ writes
> 168	[Storage bucket: video-studio-assets] + [DB: video_renders]
> 169	```
> 170	
> 171	### 4.2 External API Contracts
> 172	
> 173	#### `POST /functions/v1/video-faceless-render`
> 174	
> 175	**Auth:** Bearer JWT (user scope). **Sequência:** JWT → BYOK resolve (R1) → `deduct_mco_coins` (R2) → enqueue → ACK async.
> 176	**Request:**
> 177	```typescript
> 178	{
> 179	  product_id?: string,       // produto escolhido no picker (product-aware); opcional → tema livre
> 180	  topic?: string,            // tema livre quando sem produto
> 181	  project_id?: string,       // tenant project scope (mesh isolation)
> 182	  scenes?: number,           // nº de cenas (default workflow), cap por plano
> 183	  voice_consent?: boolean,   // obrigatório se clonagem de voz de pessoa identificável (FR-VS-032)
> 184	  delivery?: { telegram?: boolean }  // entrega opcional; link soberano sempre
> 185	}
> 186	```
> 187	**Response (202 Accepted):**
> 188	```typescript
> 189	{
> 190	  status: 'queued',
> 191	  render_id: string,         // uuid — poll-able
> 192	  charged_mco: number,       // VIDEO_FACELESS_RENDER debitado
> 193	  estimated_legs: number
> 194	}
> 195	```
> 196	**Error codes:**
> 197	| Code | Condition |
> 198	|------|-----------|
> 199	| 401 | JWT ausente/inválido (FR-VS-001) |
> 200	| 402 | Saldo mco insuficiente (antes da leg) OU `<service>_not_configured` (BYOK ausente, FR-VS-005) |
> 201	| 409 | `voice_consent` exigido e não fornecido (FR-VS-032) |
> 202	| 422 | Validação (campo + mensagem PT-BR no body) |
> 203	| 500 | Erro interno (logado em `infra_health_logs`) |
> 204	
> 205	#### `POST /functions/v1/video-hyperframes-render`
> 206	
> 207	**Auth:** Bearer JWT (user scope). **Sequência:** JWT → `deduct_mco_coins` → spawn sandbox per-render.
> 208	**Request:**
> 209	```typescript
> 210	{
> 211	  template_id?: string,      // template versionado (reuso); OU
> 212	  html: string,              // HTML/CSS/JS inline (untrusted → sandbox)
> 213	  props?: Record<string, unknown>,  // data-driven props
> 214	  media_refs?: string[],     // assets do bucket do tenant
> 215	  fps?: number, width?: number, height?: number, duration_s?: number
> 216	}
> 217	```
> 218	**Response (202 Accepted):**
> 219	```typescript
> 220	{ status: 'queued', render_id: string, charged_mco: number }
> 221	```
> 222	**Error codes:** 401 (FR-VS-002) · 402 (saldo) · 422 (validação/HTML malformado) · 500 (sandbox falhou → refund FR-VS-011).
> 223	
> 224	#### `POST /functions/v1/video-render-poll`
> 225	
> 226	**Auth:** Bearer JWT. **Tenant-bound:** `render_id` de outro tenant → 404.
> 227	**Response (200):**
> 228	```typescript
> 229	{
> 230	  render_id: string,
> 231	  state: 'queued' | 'running' | 'qa_gate' | 'done' | 'qa_failed' | 'failed',
> 232	  legs?: Array<{ name: 'script'|'image'|'voice'|'motion'|'overlay'|'composite'|'qa', status: string }>,
> 233	  qa?: { consistent: boolean, confidence?: 'high'|'medium'|'low' },
> 234	  video_url?: string,        // signed URL (sovereign delivery); presente em 'done'
> 235	  refunded_mco?: number,     // presente em 'failed'
> 236	  node_id?: string           // observação na malha (FR-VS-026)
> 237	}
> 238	```
> 239	
> 240	#### External provider/service contracts (per-user BYOK · resolved by `auth.uid()`)
> 241	
> 242	| Provider / Service | Used by leg | Auth resolution | Contract surface |
> 243	|--------------------|-------------|-----------------|------------------|
> 244	| Gemini API (director + vision QA) | script, QA gate | `decrypted_user_api_keys.gemini_api_key` (per-user); env só em cron | text/vision; boxes `[ymin,xmin,ymax,xmax]`; video @1FPS |
> 245	| Pollinations | image | free/no-key (system path documentado) | image-from-prompt |
> 246	| VoxCPM | voice (TTS clonado) | in-container; consentimento gate (FR-VS-032) | text→audio (voz clonada) |
> 247	| Remotion `remotion-render:8088` | overlays (HUD/captions) | container-local (network `n8n_default`); **NÃO** host-published (OTD-VS-004) | `POST /render` → composição React→frames |
> 248	| LTX HF Space `lightricks-ltx-video-distilled` | motion (i2v) | HF ZeroGPU (~5 GPU-min/dia); Ken-Burns fallback | image→video |
> 249	| `mcorch_vision_mcp` (`127.0.0.1:3200`) | QA gate + mesh | Bearer PAT do studio (R5 bridge); Streamable-HTTP MCP, Origin gate | `vision.describe_image`/`analyze_video`/`mesh.consolidate_reference` |
> 250	| `mcorch_chroma` (`127.0.0.1:8001`, API v2) | semantic memory | bridge R5; loopback | upsert/query embeddings |
> 251	| Telegram Bot API | delivery (opcional) | `TELEGRAM_BOT_TOKEN` per-user OU sistema (OTD-VS-003); ausência ≠ bloqueio | `sendVideo` |
> 252	| Mercado Livre affiliate | monetização | `affiliate_config` per-user (`app_id`/`affiliate_tag` por `user_id`) | link + UTM; `affiliate_links.content_id` |
> 253	
> 254	> **Billing point (todas as legs pagas):** o débito ocorre via `deduct_mco_coins` RPC no entrypoint da edge function, ANTES da 1ª leg de provider. Refund idempotente em falha pós-débito (FR-VS-011). QA via BYOK = 0 mco (FR-VS-012).
> 255	
> 256	---
> 257	
> 258	## 5. Data Requirements
> 259	
> 260	| Field | Type | Nullable | Validation Rule | Error Message (PT-BR) |
> 261	|-------|------|----------|-----------------|----------------------|
> 262	| `video_renders.user_id` | uuid | No | `= auth.uid()` (RLS) | "Sessão inválida." |
> 263	| `video_renders.engine` | text | No | `IN ('faceless','hyperframes')` | "Motor de render inválido." |
> 264	| `video_renders.state` | text | No | `IN ('queued','running','qa_gate','done','qa_failed','failed')` | — |
> 265	| `video_renders.charged_mco` | integer | No | `>= 0` | "Custo inválido." |
> 266	| `video_renders.refunded_mco` | integer | No (default 0) | `>= 0` e `<= charged_mco` | — |
> 267	| `video_renders.storage_key` | text | Yes (até `done`) | objeto existe no bucket; vídeo ≥ 100KB | "Asset de vídeo não persistido." |
> 268	| `video_renders.product_id` | uuid | Yes | FK product do tenant (se product-aware) | "Produto não encontrado." |
> 269	| `video_renders.voice_consent` | boolean | No (default false) | `true` exigido se clonagem de voz identificável | "Consentimento de voz obrigatório para clonagem." |
> 270	| `video_templates.html` | text | No | tamanho ≤ cap; sanitizado p/ sandbox | "Template HTML inválido ou grande demais." |
> 271	| `affiliate_links.content_id` | uuid | No (no link de vídeo) | NON-NULL (liga link↔asset) | "Link de afiliado sem conteúdo associado." |
> 272	| `mco_balance` (profiles) | integer | No | `>= 0` após deduct (RPC atômico) | "Saldo de mcoCoins insuficiente." |
> 273	
> 274	---
> 275	
> 276	## 6. Test Strategy Matrix
> 277	
> 278	| FR ID | Unit Test | Integration Test | E2E Test | Notes |
> 279	|-------|-----------|-----------------|----------|-------|
> 280	| FR-VS-001/002/003/004 | ✅ | ✅ | ✅ | AT-VS-001..004 — smoke 401 nas 3 superfícies + handshake PAT do studio (zero-cost) |
> 281	| FR-VS-005/006/008 | ✅ | ✅ | — | AT-VS-005 — 402 `{error,action}` + grep env global = 0 |
> 282	| FR-VS-007 | ✅ | ✅ | — | AT-VS-013 — 2 tenants providers distintos isolados (OTD-VS-002 selada) |
> 283	| FR-VS-009/010/011 | ✅ | ✅ | ✅ | AT-VS-009/010/011 — delta `mco_balance` por `SELECT` (sucesso + falha+refund) |
> 284	| FR-VS-012/019/020 | ✅ | ✅ | — | AT-VS-006 — `compare` aprova/reprova; QA custo 0 (BYOK) |
> 285	| FR-VS-013 | ✅ | — | — | AT-VS-013 — espelhamento triplo + medição material 1º render (OTD-VS-007) |
> 286	| FR-VS-014/015/016/017/018 | ✅ | ✅ | ✅ | AT-VS-014..017 — render `success` MP4 ≥100KB + Ken-Burns fallback + link afiliado |
> 287	| FR-VS-021/022/023 | ✅ | ✅ | ✅ | AT-VS-021..023 — embed nativo carrega; rota não sombreada; botão Video navega (E2E 1920×1080) |
> 288	| FR-VS-024 | ✅ | ✅ | ✅ | AT-VS-024 — 2 renders byte-idênticos (`sha256sum`) |
> 289	| FR-VS-025 | ✅ | ✅ | — | AT-VS-025 — `/security-review`; HTML não alcança rede/env; zero cred no sandbox |
> 290	| FR-VS-026/027/028 | ✅ | ✅ | — | AT-VS-008/015b — nó na malha com fr_id; log de falha; busca semântica |
> 291	| FR-VS-029/030 | ✅ | ✅ | ✅ | AT-VS-004/007 — bridge DNS resolve + handshake; asset material no bucket |
> 292	| FR-VS-031/032 | ✅ | ✅ | — | AT-VS-016b/c — zero-resíduo ≤24h; recusa de clonagem sem consentimento |
> 293	
> 294	**Test files location:**
> 295	- Unit: `src/hooks/__tests__/useFacelessRender.test.ts`, `src/hooks/__tests__/useHyperframesRender.test.ts`
> 296	- Integration / smoke (zero-cost gates): `scripts/qa/smoke-video-faceless.ts`, `scripts/qa/smoke-video-hyperframes.ts`, `scripts/qa/smoke-video-auth.ts`, `scripts/qa/smoke-video-byok.ts`
> 297	- E2E (logado, 1920×1080): `scripts/qa/e2e-user-zero/flows/video-studio.json` + `e2e/video-studio.spec.ts`
> 298	
> 299	---
> 300	
> 301	## 7. Traceability Matrix
> 302	
> 303	| PR ID | FR ID | NFR ID |
> 304	|-------|-------|--------|
> 305	| PR-VS-001 | FR-VS-004, FR-VS-029 | NFR-VS-007 |
> 306	| PR-VS-002 | FR-VS-001, FR-VS-002, FR-VS-003 | NFR-VS-008, NFR-VS-012 |
> 307	| PR-VS-003 | FR-VS-005, FR-VS-006, FR-VS-008 | NFR-VS-010 |
> 308	| PR-VS-004 | FR-VS-009, FR-VS-010, FR-VS-011, FR-VS-013 | NFR-VS-014 |
> 309	| PR-VS-005 | FR-VS-014, FR-VS-015, FR-VS-016, FR-VS-018 | NFR-VS-001, NFR-VS-005 |
> 310	| PR-VS-006 | FR-VS-012, FR-VS-019, FR-VS-020 | NFR-VS-004 |
> 311	| PR-VS-007 | FR-VS-030 | NFR-VS-016 |
> 312	| PR-VS-008 | FR-VS-026, FR-VS-027 | NFR-VS-007 |
> 313	| PR-VS-009 | FR-VS-021, FR-VS-022, FR-VS-023 | NFR-VS-003, NFR-VS-017 |
> 314	| PR-VS-010 | FR-VS-025 | NFR-VS-009 |
> 315	| PR-VS-011 | FR-VS-010, FR-VS-024 | NFR-VS-002, NFR-VS-006, NFR-VS-016 |
> 316	| PR-VS-012 | FR-VS-017 | — |
> 317	| PR-VS-013 | FR-VS-007 | NFR-VS-011 |
> 318	| PR-VS-014 | FR-VS-003 | NFR-VS-012 |
> 319	| PR-VS-015 | FR-VS-028 | — |
> 320	| PR-VS-016 | FR-VS-031, FR-VS-032 | NFR-VS-015 |
> 321	| PR-VS-017 | FR-VS-018 | — |
> 322	| (UX house style) | FR-VS-021, FR-VS-023 | NFR-VS-017 |
> 323	
> 324	---
> 325	
> 326	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 327	
> ```

## 🤖 Claude *(01:26:28)*

Now let me check the data model and quality metrics documents:

## 🤖 Claude *(01:26:29)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/06-data-model.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Data Model — Data & Knowledge Model
> 2	
> 3	**Project:** video-studio
> 4	**Version:** v0.1 | **Date:** 2026-06-21
> 5	**BoK Applied:** DMBOK v2 (Data Modeling & Design · Data Quality · Reference & Master Data · Metadata)
> 6	**Status:** Draft
> 7	**Source of Truth:** `01-mrd.md` (MR-VS-001..014) + `02-brd.md` (BR-VS-001..016) + `03-prd.md` (PR-VS-001..023) + `04-frd.md` (FR-VS-001..032, NFR-VS-001..017) + `05-sdd.md` (§2.6 New DB Objects, §5.2 RLS, §5.5 Erasure, §7 Migration Stubs, §8 OTD-VS-001..007) — todo objeto de dados rastreia ≥1 FR-VS; os stubs físicos do SDD §7 são autoridade (aqui referenciados, não duplicados verbatim).
> 8	**Regulatory:** LGPD **ELEVADO** — voz clonada (VoxCPM) = dado biométrico potencial (Art. 11); HTML/dados arbitrários do editor; config BYOK por tenant; erasure em cascata (Art. 18) e retention (Art. 16) tratados como Critical.
> 9	**Market segment:** B2B2C · **Monetization:** híbrida (mcoCoins por render + afiliado Mercado Livre) · **Integration surface:** extends-mcorch.
> 10	**Five Unbreakable Rules (Sovereign 2026-06-21) honored:** R1 BYOK per-user · R2 mcoCoins gatekeeper atômico · R3 auth MCORCH nos apps isolados · R4 conexão à malha · R5 ponte de rede Docker.
> 11	
> 12	---
> 13	
> 14	## 1. Conceptual Data Model
> 15	
> 16	### 1.1 Entity inventory
> 17	
> 18	| Entity | Kind | New? | Purpose | FR traced |
> 19	|--------|------|------|---------|-----------|
> 20	| `tenant` (≡ `auth.users` + `profiles`) | Reference | reuse | Dono de renders, templates, assets, config BYOK e nós; carteira `mco_balance` (ledger de cobrança) | — |
> 21	| `video_render` (≡ render/job) | Transactional | **new** | Máquina de estados de um render (faceless OU hyperframes); ledger atômico charged/refunded; poll-able | FR-VS-009/010/011/014/024/026 |
> 22	| `video_template` | Master | **new** | Template HyperFrames versionado reutilizável (HTML/props), tenant-scoped — habilita PR-VS-022 | FR-VS-021/024 |
> 23	| `video_asset` (≡ render_asset) | Transactional | **new** | Manifest de artefatos materiais (vídeo/imagem/áudio em Storage + node_ids) — unidade atômica de erasure | FR-VS-030/031 |
> 24	| `video_scene` | Transactional | **new** | Cena individual do loop faceless (script + image + voice + motion + QA por cena) — granularidade do pipeline n8n | FR-VS-014/016/019 |
> 25	| `script` (≡ roteiro) | Knowledge | typed | Roteiro product-aware do director Gemini + verdict de QA → memória semântica (`mcorch_nodes` tipado + Chroma) | FR-VS-017/028 |
> 26	| `user_api_key` (VIEW Vault) | Master | extend | + coluna BYOK de provider de vídeo (família trigger Vault); `gemini_api_key` reusado | FR-VS-005/008 |
> 27	| `affiliate_link` (≡ mcoin/monetização link) | Transactional | reuse | Link afiliado ML + UTM ligado ao asset gerado (`content_id` NON-NULL) | FR-VS-017 |
> 28	| `mco_transaction` / `profiles.mco_balance` | Operational | reuse | Ledger de débito/refund atômico via `deduct_mco_coins`/refund | FR-VS-009/010/011 |
> 29	| `observation` (≡ `mcorch_nodes` tipado) | Knowledge | reuse+typed | Nó de observação por render `success` (embed-on-insert) + nó de roteiro/verdict | FR-VS-026/028 |
> 30	| `mesh_edge` (≡ `mcorch_edges`) | Knowledge | reuse | Edge observation→render/produto (instrumenta KPI) + `DERIVES_FROM` | FR-VS-026 |
> 31	| `infra_health_log` | Operational | reuse | Telemetria de todo path (success/degraded/error) — `service='video-studio'` | FR-VS-027 |
> 32	| `design_artifact` (≡ open-design link) | Knowledge | reuse | Artefato de design do open-design (sidecar) ligado à malha (`design_artifact_refs`) — alvo de erasure | FR-VS-007/031 |
> 33	| `video-studio-assets` (Storage bucket) | Binary | **new** | Vídeo/imagem/áudio privados (signed URL curto · entrega soberana) | FR-VS-030 |
> 34	
> 35	### 1.2 Text ERD (relacionamentos)
> 36	
> 37	```
> 38	auth.users (tenant) ──1:N──▶ video_renders            (user_id, ON DELETE CASCADE; id = PK poll-able)
> 39	                   ──1:N──▶ video_templates           (user_id; HyperFrames reuse)
> 40	                   ──1:N──▶ video_assets              (user_id; manifest de erasure)
> 41	                   ──1:1──▶ user_api_keys (VIEW)       (BYOK gemini/<video_provider> — Vault)
> 42	                   ──1:N──▶ mcorch_nodes (vídeo)       (user_id NOT NULL p/ tenant — NUNCA system node)
> 43	                   ──1:N──▶ affiliate_links           (monetização; content_id liga ao asset)
> 44	                   ──1:1──▶ profiles (mco_balance)     (ledger via deduct_mco_coins/refund)
> 45	
> 46	video_renders   ──1:N──▶ video_scenes                (render_id, ON DELETE CASCADE; loop faceless)
> 47	                ──1:N──▶ video_assets                (render_id → manifest dos artefatos materiais)
> 48	                ──1:1──▶ mcorch_nodes (observation)  (node_id; observação na malha por success)
> 49	                ──1:N──▶ affiliate_links             (content_id NON-NULL p/ link de vídeo)
> 50	video_assets    ──N:M──▶ mcorch_nodes                (node_id — alvo do cascade de erasure)
> 51	                ──1:N──▶ storage.objects             (storage_key no bucket video-studio-assets)
> 52	video_templates ──1:N──▶ video_renders              (template_id; reuso determinístico HyperFrames)
> 53	mcorch_nodes (observation) ──edge──▶ mcorch_nodes (produto/roteiro)  (instrumenta KPI de receita)
> 54	mcorch_nodes (roteiro/verdict) ──upsert──▶ mcorch_chroma            (memória semântica API v2)
> 55	```
> 56	
> 57	**Cardinalidade-chave:** um `video_render` é a raiz do ledger financeiro (charged/refunded atômico) e a raiz da cascata de artefatos. Um `video_asset` agrega o objeto de Storage + os `node_ids` derivados — apagar o tenant (ou chamar `erase_video_artifacts`) derruba renders → scenes → assets → objetos de Storage → nós/embeddings de roteiro em cascata (FR-VS-031). O `video_template` é a única entidade Master per-tenant (reuso determinístico — argumento Enterprise PR-VS-022).
> 58	
> 59	---
> 60	
> 61	## 2. Logical Data Model
> 62	
> 63	> Tipos/constraints físicos selados no SDD §7 (autoridade copy-ready). Aqui: contrato lógico + chaves + nullability + isolamento. As tabelas espelham as canônicas existentes (`vm_canvas_*`, `creative_metrics`, `autopilot_cycles`) para consistência de família.
> 64	
> 65	### 2.1 `video_renders` (FR-VS-009/010/011/014/024/026 — ledger + máquina de estados)
> 66	
> 67	| Column | Type | Null | Key / Constraint | Notes |
> 68	|--------|------|------|------------------|-------|
> 69	| `id` (= `render_id`) | uuid | NO | PK | retornado no 202; poll-able (`video-render-poll`) |
> 70	| `user_id` | uuid | NO | FK → `auth.users(id)` CASCADE | tenant; poll alheio → 404 |
> 71	| `project_id` | uuid | YES | FK → `projects(id)` CASCADE | isolamento de malha |
> 72	| `engine` | text | NO | CHECK ∈ {`faceless`,`hyperframes`} | qual motor produziu o render |
> 73	| `state` | text | NO | CHECK ∈ {queued,running,qa_gate,done,qa_failed,failed} DEFAULT `queued` | máquina de estados (FRD §4.3) |
> 74	| `product_id` | uuid | YES | (lógico → produto do tenant) | product-aware (FR-VS-017); sem FK físico (produto pode ser podado) |
> 75	| `topic` | text | YES | — | tema livre quando sem produto |
> 76	| `template_id` | uuid | YES | FK → `video_templates(id)` | reuso HyperFrames (FR-VS-024) |
> 77	| `legs` | jsonb | NO | DEFAULT `'[]'` | status por leg (script/image/voice/motion/overlay/composite/qa) |
> 78	| `qa` | jsonb | YES | — | `{ consistent, confidence }` do portão VLM (FR-VS-019/020) |
> 79	| `charged_mco` | int | NO | CHECK ≥0 DEFAULT 0 | débito integral na entrada (R2) |
> 80	| `refunded_mco` | int | NO | CHECK ≥0 e `≤ charged_mco` DEFAULT 0 | crédito de refund (floor a favor do tenant) |
> 81	| `refunded_at` | timestamptz | YES | — | **guard de idempotência** (refund 1×/render) |
> 82	| `storage_key` | text | YES (até `done`) | objeto existe no bucket; vídeo ≥100KB | prova material (Lei 1) |
> 83	| `voice_consent` | boolean | NO | DEFAULT false | exigido p/ clonagem de voz identificável (FR-VS-032) |
> 84	| `node_id` | uuid | YES | (lógico → `mcorch_nodes.id`) | observação na malha (FR-VS-026) |
> 85	| `expires_at` | timestamptz | NO | DEFAULT now()+24h | retenção de poll ≥24h |
> 86	| `created_at`/`updated_at` | timestamptz | NO | DEFAULT now() | audit |
> 87	
> 88	### 2.2 `video_scenes` (FR-VS-014/016/019 — granularidade do loop faceless)
> 89	
> 90	| Column | Type | Null | Key / Constraint | Notes |
> 91	|--------|------|------|------------------|-------|
> 92	| `id` | uuid | NO | PK | — |
> 93	| `render_id` | uuid | NO | FK → `video_renders(id)` CASCADE | cena pertence ao render |
> 94	| `user_id` | uuid | NO | FK → `auth.users(id)` CASCADE | redundância de tenant p/ RLS direto |
> 95	| `scene_index` | int | NO | CHECK ≥0; UNIQUE `(render_id, scene_index)` | ordem no loop |
> 96	| `script_text` | text | YES | — | roteiro da cena (director Gemini) |
> 97	| `image_storage_key` | text | YES | — | frame da cena (Pollinations) |
> 98	| `voice_storage_key` | text | YES | — | TTS da cena (VoxCPM) |
> 99	| `motion_storage_key` | text | YES | — | clipe i2v (LTX) ou Ken-Burns fallback |
> 100	| `motion_fallback` | boolean | NO | DEFAULT false | true = Ken-Burns (cota LTX excedida — FR-VS-016) |
> 101	| `qa_consistent` | boolean | YES | — | gate G3 por cena (frames inicial/final) |
> 102	| `created_at` | timestamptz | NO | DEFAULT now() | — |
> 103	
> 104	### 2.3 `video_templates` (FR-VS-021/024 — Master HyperFrames reuse)
> 105	
> 106	| Column | Type | Null | Key / Constraint | Notes |
> 107	|--------|------|------|------------------|-------|
> 108	| `id` | uuid | NO | PK | — |
> 109	| `user_id` | uuid | NO | FK → `auth.users(id)` CASCADE | tenant-scoped CRUD |
> 110	| `project_id` | uuid | YES | FK → `projects(id)` CASCADE | — |
> 111	| `name` | text | NO | — | rótulo do template |
> 112	| `html` | text | NO | tamanho ≤ cap; sanitizado p/ sandbox (OTD-VS-006) | HTML/CSS/JS UNTRUSTED |
> 113	| `props` | jsonb | NO | DEFAULT `'{}'` | props data-driven |
> 114	| `version` | int | NO | DEFAULT 1 | versionamento determinístico (PR-VS-022) |
> 115	| `created_at`/`updated_at` | timestamptz | NO | DEFAULT now() | — |
> 116	
> 117	### 2.4 `video_assets` (FR-VS-030/031 — manifest de erasure)
> 118	
> 119	| Column | Type | Null | Key / Constraint | Notes |
> 120	|--------|------|------|------------------|-------|
> 121	| `id` | uuid | NO | PK | — |
> 122	| `user_id` | uuid | NO | FK → `auth.users(id)` CASCADE | dono |
> 123	| `render_id` | uuid | NO | FK → `video_renders(id)` CASCADE | render que produziu |
> 124	| `kind` | text | NO | CHECK ∈ {`video`,`image`,`audio`} | tipo de artefato |
> 125	| `storage_key` | text | NO | objeto no bucket `video-studio-assets` | chave de Storage (deletada via Storage API — OTD-VM-026 lição) |
> 126	| `node_id` | uuid | YES | (lógico → `mcorch_nodes.id`) | nó derivado (roteiro/observação) |
> 127	| `bytes` | bigint | YES | CHECK ≥0 | tamanho material (vídeo ≥100KB) |
> 128	| `retention_until` | timestamptz | YES | > now() quando setado; teto = política §7 | clock de retenção LGPD (Art. 16) |
> 129	| `created_at` | timestamptz | NO | DEFAULT now() | — |
> 130	
> 131	### 2.5 `user_api_keys` extension — BYOK de provider de vídeo (FR-VS-005/008 · família Vault)
> 132	
> 133	VIEW Vault-mascarada (família de trigger `vault_upsert_secret` idempotente — precedente `20260602140000`). `gemini_api_key` é **reusado** (director + vision QA); coluna nova apenas se um provider de vídeo dedicado exigir chave separada:
> 134	
> 135	| Column | Type | Null | Write rule | Lookup |
> 136	|--------|------|------|-----------|--------|
> 137	| `gemini_api_key` (reuso) | text (Vault) | YES | `.insert` na VIEW (NUNCA `.upsert`); null não limpa (clear via RPC) | `decrypted_user_api_keys` (service-role only) |
> 138	| `<video_provider>_api_key` (condicional) | text (Vault) | YES | idem | idem — só se OTD-VS-002 exigir provider de vídeo dedicado |
> 139	
> 140	### 2.6 Reuse — sem alteração de schema
> 141	
> 142	`affiliate_config` (BYOK ML per-user · `app_id`/`affiliate_tag`), `affiliate_links` (`content_id` NON-NULL no link de vídeo — FR-VS-017), `profiles.mco_balance` (carteira via `deduct_mco_coins`/refund), `mcorch_nodes`/`mcorch_edges` (malha, §4), `infra_health_logs` (telemetria, novo `service='video-studio'` + `event` types — sem DDL), `design_artifact_refs` (open-design — alvo de erasure FR-VS-031).
> 143	
> 144	---
> 145	
> 146	## 3. Supabase Physical Schema Stubs
> 147	
> 148	Os `CREATE TABLE`/RLS/índices/RPC físicos estão selados no **SDD §7 (Migration Stubs)** e **§5.2 (RLS Policies)** — autoridade única copy-ready para os arquivos de migration. Resumo das migrations (ordem de aplicação):
> 149	
> 150	| # | Migration file (stub) | Cria | RLS | Índices |
> 151	|---|----------------------|------|-----|---------|
> 152	| 1 | `<ts>_video_studio_renders.sql` | `video_renders` (+CHECK engine/state, `refunded_mco ≤ charged_mco`) | default-deny; SELECT/INSERT own; UPDATE service-role; **RESTRICTIVE no client delete** (ledger financeiro) | `(user_id, state)`, `(user_id, created_at DESC)`, `expires_at` |
> 153	| 2 | `<ts>_video_studio_scenes.sql` | `video_scenes` | default-deny; SELECT own; writes service-role | `(render_id, scene_index)` UNIQUE, `user_id` |
> 154	| 3 | `<ts>_video_studio_templates.sql` | `video_templates` | default-deny; ALL own (CRUD tenant-scoped) | `user_id`, `project_id` |
> 155	| 4 | `<ts>_video_studio_assets.sql` | `video_assets` | default-deny; SELECT own; writes service-role | `render_id`, `user_id`, `retention_until` |
> 156	| 5 | `<ts>_video_studio_byok.sql` | coluna BYOK condicional + re-create da família trigger/VIEW Vault | herdada (VIEW Vault mascarada) | — |
> 157	| 6 | `<ts>_video_studio_erase_rpc.sql` | `erase_video_artifacts(p_user_id)` SECURITY DEFINER `search_path=''` | EXECUTE revogado de PUBLIC/anon; GRANT authenticated (own via guard) + service_role (sweep) | — |
> 158	
> 159	**Padrão de cobrança:** nenhuma das tabelas tem coluna de embedding própria — roteiro/verdict embedam em `mcorch_nodes`/Chroma (§4). Tabelas financeiras (`video_renders`) seguem a família **RESTRICTIVE no-delete** de `creative_metrics`/`autopilot_cycles` (clientes nunca apagam o ledger). **Gate house:** cada migration passa `/security-review` independente ANTES do commit (FMEA-011 + NFR-VS-011). Bucket `video-studio-assets` privado (config + policy de Storage).
> 160	
> 161	### 3.1 RPC de erasure — `erase_video_artifacts(p_user_id)` (FR-VS-031 · espelha `erase_vision_artifacts`/`erase_lead`)
> 162	
> 163	```sql
> 164	-- Migration: <ts>_video_studio_erase_rpc.sql (FR-VS-031 — LGPD cascade · gate de GA).
> 165	-- Espelha erase_vision_artifacts (20260615200000) + erase_lead: SECURITY DEFINER + search_path='' +
> 166	-- guard de tenant em CADA cascade DELETE (um node_ids[] envenenado nunca vira primitiva cross-tenant).
> 167	-- Storage: NÃO deletado em SQL (storage.objects é do storage-admin → 42501); RETURN storage_keys p/ o
> 168	-- CALLER (container erase-broker / delete-account, service-role) remover via Storage API (lição OTD-VM-026).
> 169	CREATE OR REPLACE FUNCTION public.erase_video_artifacts(p_user_id uuid)
> 170	RETURNS jsonb
> 171	LANGUAGE plpgsql SECURITY DEFINER SET search_path = ''
> 172	AS $$
> 173	DECLARE
> 174	  v_keys text[];
> 175	  v_node_ids uuid[];
> 176	  v_nodes int; v_renders int;
> 177	BEGIN
> 178	  -- Guard de tenant (ledger-RPC rule): só o próprio tenant OU service-role pode disparar o cascade.
> 179	  IF NOT (p_user_id = auth.uid() OR auth.role() = 'service_role') THEN
> 180	    RAISE EXCEPTION 'forbidden' USING errcode = '42501';
> 181	  END IF;
> 182	
> 183	  SELECT array_agg(storage_key), array_agg(node_id)
> 184	    INTO v_keys, v_node_ids
> 185	    FROM public.video_assets WHERE user_id = p_user_id;
> 186	
> 187	  -- Cada DELETE re-escopado por user_id (defense-in-depth — SECURITY DEFINER bypassa RLS).
> 188	  DELETE FROM public.mcorch_edges
> 189	   WHERE (source_id = ANY(COALESCE(v_node_ids,'{}')) OR target_id = ANY(COALESCE(v_node_ids,'{}')))
> 190	     AND user_id = p_user_id;
> 191	  DELETE FROM public.mcorch_nodes
> 192	   WHERE id = ANY(COALESCE(v_node_ids,'{}')) AND user_id = p_user_id;   -- leva o embedding junto
> 193	  GET DIAGNOSTICS v_nodes = ROW_COUNT;
> 194	  DELETE FROM public.video_assets    WHERE user_id = p_user_id;
> 195	  DELETE FROM public.video_scenes    WHERE user_id = p_user_id;
> 196	  DELETE FROM public.video_renders   WHERE user_id = p_user_id;          -- CASCADE leva scenes/assets remanescentes
> 197	  GET DIAGNOSTICS v_renders = ROW_COUNT;
> 198	  DELETE FROM public.video_templates WHERE user_id = p_user_id;
> 199	
> 200	  RETURN jsonb_build_object(
> 201	    'erased', true, 'renders', v_renders, 'nodes', v_nodes,
> 202	    'storage_keys', to_jsonb(COALESCE(v_keys,'{}'))   -- caller remove via Storage API + purga Chroma + OD_DATA_DIR
> 203	  );
> 204	END $$;
> 205	
> 206	REVOKE EXECUTE ON FUNCTION public.erase_video_artifacts(uuid) FROM PUBLIC, anon;
> 207	GRANT  EXECUTE ON FUNCTION public.erase_video_artifacts(uuid) TO authenticated, service_role;
> 208	```
> 209	
> 210	> O `delete-account` (edge fn, service-role) chama esta RPC e ADICIONALMENTE: remove os objetos de Storage (`storage_keys` retornados via Storage API), faz purge das coleções do ChromaDB do tenant (§4.5), e dispara a limpeza do `OD_DATA_DIR`/`OD_MEDIA_CONFIG_DIR` + config global de provider do open-design que carrega a chave BYOK (precedente Canvas Design OTD-008).
> 211	
> 212	---
> 213	
> 214	## 4. GraphRAG Knowledge Nodes
> 215	
> 216	### 4.1 Node types introduzidos / tipados
> 217	
> 218	| node_type | Origem | Regime | stability_score inicial | revenue_impact |
> 219	|-----------|--------|--------|------------------------|----------------|
> 220	| `observation` | render `success` (FR-VS-026) — um nó por render | **decai** (FSRS-6) | 1.0 | 0 (enabler interno); recalculado quando o link afiliado do vídeo converte (FR-VS-017) |
> 221	| `video_script` | roteiro product-aware do director (FR-VS-028) — base de reuso/recomendação | **decai** | 0.6 | 0 (corpus); upsell quando vira venda |
> 222	| `video_qa_verdict` | verdict do olho criativo (FR-VS-020) persistido na malha (1 mco, opcional) | **decai** | 0.6 | 0 |
> 223	
> 224	> Conteúdo de tenant **NUNCA** é system node (`user_id IS NULL`) — guard server-side (precedente vision-mcp NFR-VM-009). `revenue_impact` do nó `observation` é atualizado a cada conversão atribuída do link afiliado ML ligado ao asset (`affiliate_links.content_id`).
> 225	
> 226	### 4.2 Edge types
> 227	
> 228	| relation_type | Source → Target | Significado |
> 229	|---------------|-----------------|-------------|
> 230	| (edge ao render) | nó `observation` → nó do produto/roteiro | instrumenta KPI de receita por render (R4) |
> 231	| `DERIVES_FROM` | nó `video_qa_verdict` → nó `observation` do render | lineage do verdict (padrão da casa) |
> 232	| `DERIVES_FROM` | nó `video_script` reusado → roteiro original | recomendação de próximo tema (PR-VS-021) |
> 233	
> 234	### 4.3 Embedding fields
> 235	
> 236	Conteúdo textual do nó (`content` + `title` = roteiro + verdict) → `embed-mcorch-node` (Edge Fn existente, **reuso** — sem encanamento novo): OpenRouter `text-embedding-3-small` → fallback Gemini `text-embedding-004`, **768 dims**, HNSW cosine. Embed-on-insert **grátis** via o trigger existente (pg_net async — nunca bloqueia o insert). Espelhamento Chroma (§4.5) para busca semântica adicional.
> 237	
> 238	### 4.4 Metadata shape de um nó de observação de render
> 239	
> 240	```json
> 241	{
> 242	  "fr_id": "FR-VS-026",
> 243	  "br_id": "BR-VS-008",
> 244	  "render_id": "<uuid>",
> 245	  "engine": "faceless | hyperframes",
> 246	  "cost_mco": 125,
> 247	  "qa_confidence": "high | medium | low",
> 248	  "product_id": "<external_id ML | null>",
> 249	  "scenes": 5,
> 250	  "provenance": { "origin": "tenant" },
> 251	  "retention_until": "<ISO; > now(); ≤ teto §7>"
> 252	}
> 253	```
> 254	
> 255	### 4.5 ChromaDB memória semântica (FR-VS-028 · via bridge R5)
> 256	
> 257	Roteiro + verdict de QA também são `upsert`ados no `mcorch_chroma` (API v2, `127.0.0.1:8001`) — id = `render_id`, document = roteiro+verdict, metadata tenant-scoped (`user_id`/`project_id`). Pesquisável por `mesh.search`/Chroma após o render (base de reuso/recomendação). **Bloqueador material:** o `upsert` Chroma SÓ resolve após a ponte de rede R5 (OTD-VS-001) — antes disso é prosa. A coleção do tenant é purgada no cascade de erasure (§3.1 caller).
> 258	
> 259	---
> 260	
> 261	## 5. Tenant Isolation Map
> 262	
> 263	| Table / Object | Scope | Policy resumo | System-node caveat |
> 264	|----------------|-------|---------------|--------------------|
> 265	| `video_renders` | `user_id = auth.uid()` + `project_id` | SELECT/INSERT own; UPDATE service-role; **RESTRICTIVE no client delete** | poll alheio → 404 (FR-VS-026) |
> 266	| `video_scenes` | `user_id = auth.uid()` | SELECT own; writes service-role | — |
> 267	| `video_templates` | `user_id = auth.uid()` + `project_id` | ALL own (CRUD tenant-scoped) | — |
> 268	| `video_assets` | `user_id = auth.uid()` | SELECT own; DELETE só via `erase_video_artifacts`/cascade | — |
> 269	| `user_api_keys` (VIEW) | `user_id = auth.uid()` | máscara; reais no Vault; decrypted view service-role only | — |
> 270	| `affiliate_links` / `affiliate_config` | `user_id = auth.uid()` | RLS-own; RESTRICTIVE no-delete (financeiro) | — |
> 271	| `mcorch_nodes` (vídeo) | `user_id + project_id` | conteúdo de tenant **NUNCA** `user_id IS NULL` | **proibido** system node p/ tenant — guard server-side; violação = bug crítico |
> 272	| `mcorch_edges` | mesmo par do nó | herda isolamento | — |
> 273	| `open-design` config/`OD_DATA_DIR` | **single-tenant hoje** (config GLOBAL) | ⚠️ OTD-VS-002 — daemon compartilhado NÃO isola per-user; gate de GA antes do 2º tenant | risco cross-tenant aberto até OTD-VS-002 selar |
> 274	
> 275	> ⚠️ **Buraco de isolamento conhecido (OTD-VS-002 · BR-VS-RISK-003):** o open-design resolve provider do config GLOBAL `/app/.od/media-config.json` — o `od` é cliente fino de um daemon **compartilhado**, então `OD_MEDIA_CONFIG_DIR` por invocação NÃO isola. Hoje single-tenant EXPLÍCITO; multi-tenant exige re-arquitetura (daemon per-job / `od` stateless / container por tenant) ANTES do 2º tenant.
> 276	
> 277	---
> 278	
> 279	## 6. Data Quality Rules
> 280	
> 281	> Validações de input de request seladas no FRD §5 (mensagens PT-BR). Aqui: regras de qualidade dos dados persistidos.
> 282	
> 283	| Table | Column / Rule | Validação | Null policy | Violation (PT-BR) | Source |
> 284	|-------|---------------|-----------|-------------|-------------------|--------|
> 285	| `video_renders` | `engine` | CHECK ∈ {faceless,hyperframes} | NOT NULL | "Motor de render inválido." | FR-VS-014/024 |
> 286	| `video_renders` | `state` | CHECK ∈ máquina de estados | NOT NULL | — | FRD §4.3 |
> 287	| `video_renders` | `charged_mco` | ≥ 0 | NOT NULL | "Custo inválido." | FR-VS-009 |
> 288	| `video_renders` | `refunded_mco` | ≥0 e `≤ charged_mco` (CHECK) | NOT NULL DEFAULT 0 | — (anti negative-refund mint) | FR-VS-011 |
> 289	| `video_renders` | `refunded_at` | set 1×; guard de idempotência do refund | YES (até o refund) | — | FR-VS-011 |
> 290	| `video_renders` | `storage_key` em `done` | objeto existe no bucket; vídeo ≥100KB | NOT NULL em `done` | "Asset de vídeo não persistido." | FR-VS-030 / Lei 1 |
> 291	| `video_renders` | `voice_consent` | `true` exigido p/ clonagem de voz identificável | NOT NULL DEFAULT false | "Consentimento de voz obrigatório para clonagem." | FR-VS-032 |
> 292	| `video_scenes` | `(render_id, scene_index)` | UNIQUE | NOT NULL | — | FR-VS-014 |
> 293	| `video_templates` | `html` | tamanho ≤ cap; sanitizado p/ sandbox | NOT NULL | "Template HTML inválido ou grande demais." | FR-VS-025 |
> 294	| `video_assets` | `storage_key` | objeto existe no bucket | NOT NULL | "Asset não persistido." | FR-VS-030 |
> 295	| `video_assets` | `bytes` (vídeo) | ≥ 100KB (rejeita stub JSON) | YES | "Vídeo abaixo do tamanho mínimo (stub)." | Lei 1 / SOP creative-qa-vision-gate |
> 296	| `affiliate_links` | `content_id` (link de vídeo) | NON-NULL (liga link↔asset) | NOT NULL no link de vídeo | "Link de afiliado sem conteúdo associado." | FR-VS-017 |
> 297	| `mcorch_nodes` (vídeo) | `user_id` | NOT NULL **sempre** (zero system node p/ tenant) | NOT NULL | (bug crítico) | NFR-VS / R4 |
> 298	| `mcorch_nodes` (vídeo) | `metadata.fr_id`/`br_id` | rastreável (≥1 ID da suíte) | NOT NULL | — | R4 mandate |
> 299	| `profiles.mco_balance` | saldo pós-deduct | ≥ 0 (RPC atômico) | NOT NULL | "Saldo de mcoCoins insuficiente." | FR-VS-009 |
> 300	| voz clonada (VoxCPM) | amostra de pessoa identificável | consentimento explícito; nunca treinar/expor template sem | — | "Clonagem de voz não autorizada." | FR-VS-032 / LGPD Art. 11 |
> 301	
> 302	---
> 303	
> 304	## 7. Retention & Archival Policy (LGPD Art. 16 / 18 · gate de GA)
> 305	
> 306	| Classe de dado | Retenção | Mecanismo de expiração | Erasure sob demanda |
> 307	|----------------|----------|------------------------|---------------------|
> 308	| `video_renders` (ledger) | indefinida enquanto a conta existe (auditável); `expires_at` é só TTL de poll | poll TTL ≥24h; sem auto-delete do ledger | cascade via `delete-account` → `erase_video_artifacts` |
> 309	| `video_assets` + objetos (Storage `video-studio-assets`) | `retention_until` (tenant pode encurtar, nunca exceder o teto) | sweep diário in-container (`jobs/video-retention-sweep.ts`, espelha vision-mcp PROC-VM-008) | `erase_video_artifacts` + Storage API remove |
> 310	| `video_scenes` | acompanha o `video_render` | cascade do render | mesmo cascade |
> 311	| Nó de roteiro/observação/verdict + embeddings (`mcorch_nodes`) | acompanha o asset (`retention_until` no metadata) | sweep diário (mesmo cascade) | cascade `erase_video_artifacts` |
> 312	| Memória semântica (ChromaDB) | espelha o nó de roteiro | sweep + purge da coleção | purge no cascade (caller, §3.1) |
> 313	| Voz clonada (template biométrico, se persistido) | só com consentimento; deletada no cascade | — | cascade + revogação de consentimento (LGPD Art. 11) |
> 314	| Config BYOK de vídeo + open-design (`OD_DATA_DIR`/`OD_MEDIA_CONFIG_DIR` + config global de provider) | enquanto a conta existe | — | purgada no cascade (precedente Canvas Design OTD-008) |
> 315	| `infra_health_logs` (vídeo) | 90 dias (política global; allowlist sem PII per-tenant) | cron purge global | — |
> 316	
> 317	**Cascade de erasure (prova material NFR-VS-015 · gate de GA):** `SELECT count(*)` de renders/scenes/assets/nós/edges/embeddings/objetos de Storage **antes e depois** de `delete-account` = **zero resíduo em ≤24h**. Precedentes: `erase_vision_artifacts()` (vision-mcp) + `erase_lead()` (marketing-hub) + Canvas Design OTD-008. **Limite honesto:** a chave BYOK do open-design no config global é purgada explicitamente; cópias eventuais já transmitidas a providers externos dependem do DPA do provider (registro auditável, como em vision-mcp `provider_copies`).
> 318	
> 319	---
> 320	
> 321	## 8. Traceability (Data → FR)
> 322	
> 323	| Objeto | FR Traced | OTD / Risco relacionado |
> 324	|--------|-----------|-------------------------|
> 325	| `video_renders` | FR-VS-009/010/011/014/024/026 | OTD-VS-007 (cost); BR-VS-RISK-006 |
> 326	| `video_scenes` | FR-VS-014/016/019 | OTD-VS-004 (render engine) |
> 327	| `video_templates` | FR-VS-021/024 (+PR-VS-022) | OTD-VS-005 (embed) |
> 328	| `video_assets` + `erase_video_artifacts` | FR-VS-030/031 | BR-VS-RISK-005; Canvas Design OTD-008 |
> 329	| `user_api_keys` (BYOK vídeo) | FR-VS-005/008 | OTD-VS-002 (open-design isolation); BR-VS-RISK-003 |
> 330	| `affiliate_links` (content_id) | FR-VS-017 | — |
> 331	| `mcorch_nodes`/`edges` (tipados) + Chroma | FR-VS-026/028 | OTD-VS-001 (bridge R5); BR-VS-RISK-001 |
> 332	| `video-studio-assets` bucket | FR-VS-030 | Lei 1 |
> 333	| voz clonada / consentimento | FR-VS-032 | BR-VS-RISK-009; LGPD Art. 11 |
> 334	| `infra_health_logs` (reuse) | FR-VS-027 | — |
> 335	
> 336	Toda tabela nova aparece no `07-process-flow.md` em ≥1 processo ✅ · consolidação na malha presente nos nós de observação/roteiro ✅ · cascade de erasure cobre 100% das classes de dado pessoal ✅.
> 337	
> 338	---
> 339	
> 340	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 341	
> ```

## 🤖 Claude *(01:26:30)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/08-quality-metrics.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Quality & Self-Optimization Specification
> 2	
> 3	**Project:** video-studio
> 4	**Version:** v0.1 | **Date:** 2026-06-21
> 5	**BoK Applied:** CMQ/OE BOK (Process Management + Organizational Excellence)
> 6	**Status:** Draft
> 7	**Source of Truth (upstream):** `01-mrd.md` (MR-VS-001..014) · `02-brd.md` (BO-VS-001..005, BR-VS-001..016, Risk Register) · `03-prd.md` (PR-VS-001..023) · `04-frd.md` (FR-VS-001..032, NFR-VS-001..017) · `05-sdd.md` (OTD-VS-001..007) · `06-data-model.md` · `07-process-flow.md` (PROC-VS-001..007). Todo KPI/FMEA deste documento rastreia ≥1 FR-VS/BO-VS; ambiguidade vira OTD-VS, nunca improvisação.
> 8	**Market segment:** B2B2C · **Monetization:** híbrida (mcoCoins por render + afiliado Mercado Livre) · **Regulatory:** LGPD (voz clonada VoxCPM = biométrico potencial, Art. 11) · **Integration surface:** extends-mcorch.
> 9	**Five Unbreakable Rules (Sovereign 2026-06-21) honored:** R1 BYOK per-user · R2 mcoCoins gatekeeper atômico · R3 auth MCORCH nos apps isolados · R4 conexão à malha · R5 ponte de rede Docker.
> 10	
> 11	> **Filosofia de qualidade (CMQ/OE):** "MATE A POESIA. ENTREGUE ENGENHARIA." A qualidade do `video-studio` é a disciplina de **não queimar crédito caro sem prova** — portão VLM antes do render (G3), refund atômico em falha, sandbox antes de executar HTML de terceiro, e erasure provada antes do 2º tenant. Todo número abaixo é **medível por `SELECT`/log real** (Lei 1 — Materialidade); nenhuma classe de custo final crava-se antes da medição no 1º render pago (OTD-VS-007).
> 12	
> 13	---
> 14	
> 15	## 1. Quality Objectives
> 16	
> 17	> Cada QO ancora um Business Objective (BRD §2) e fecha a malha PDCA (§7). Alvos provisórios marcados — recalibrados no 1º render pago.
> 18	
> 19	| QO ID | Objective | Linked Business Objective | Target | Review Cadence |
> 20	|-------|-----------|--------------------------|--------|---------------|
> 21	| QO-VS-001 | **Render confiável** — produção faceless E2E termina em asset material sem queda silenciosa | BO-VS-001 | Render success rate ≥ 95% (faceless) / ≥ 98% (HyperFrames) sobre jobs aceitos | Weekly |
> 22	| QO-VS-002 | **Disciplina de QA** — zero crédito caro de vídeo gasto sobre frames inconsistentes | BO-VS-003 | ≥ 90% dos renders de vídeo precedidos de gate VLM aprovado; QA pass rate ≥ 80% pós-render | Weekly |
> 23	| QO-VS-003 | **Margem sustentável** — custo-por-vídeo dentro do modelo 4×-floor | BO-VS-001, BO-VS-003 | 100% das classes mco ≥ `ceil(usd/$0.0045)`; nenhuma op sub-1× no piso Enterprise | Monthly (revisão de calibração) |
> 24	| QO-VS-004 | **Confiança financeira** — débito atômico, sem cobrança dupla, refund íntegro em falha | BO-VS-001 | mcoCoins double-charge rate = 0; refund correctness = 100% (delta `mco_balance` provado) | Monthly |
> 25	| QO-VS-005 | **Isolamento multi-tenant** — credencial/quota/asset de um tenant nunca vaza para outro | BO-VS-002, BO-VS-005 | 0 incidentes de cross-tenant; BYOK isolation provada (2 tenants distintos) antes de GA | Quarterly (gate de GA) |
> 26	| QO-VS-006 | **Adoção monetizada** — vídeos com afiliado ML e atribuição de clique por tenant | BO-VS-004 | BYOK-configured rate ≥ 70%; affiliate attach-rate ≥ 65%; ≥1 clique atribuído | Monthly |
> 27	| QO-VS-007 | **Conformidade LGPD** — erasure em cascata e consentimento de voz provados | BO-VS-005 | Zero-resíduo de erasure em 100% dos testes ≤24h; 0 clonagens de voz sem consentimento | Quarterly (gate de GA) |
> 28	
> 29	---
> 30	
> 31	## 2. KPI Dashboard Definition
> 32	
> 33	> Data source: tabelas/views Supabase + telemetria de container. KPIs alimentam o Neural HUD (`get-infra-status`) e o ROIWidget. Janela de agregação default = 7 dias móveis salvo nota. Alvos provisórios (∼) recalibrados pós-medição (OTD-VS-007).
> 34	
> 35	| KPI ID | Name | Formula | Target | Warn Threshold | Critical Threshold | Data Source |
> 36	|--------|------|---------|--------|---------------|-------------------|-------------|
> 37	| KPI-VS-001 | Render success rate (faceless) | `COUNT(state='done' AND engine='faceless') / COUNT(state IN ('done','qa_failed','failed') AND engine='faceless')` | ≥ 95% | < 95% | < 85% | `video_renders` |
> 38	| KPI-VS-002 | Render success rate (HyperFrames) | `COUNT(state='done' AND engine='hyperframes') / COUNT(terminal AND engine='hyperframes')` | ≥ 98% | < 98% | < 90% | `video_renders` |
> 39	| KPI-VS-003 | Cost-per-video (mco) | `SUM(charged_mco - refunded_mco) / COUNT(state='done')` por engine | ≈ 125 (faceless) / ≈ 12 (HyperFrames), ±10% | desvio > 15% | desvio > 30% (sub-margem) | `video_renders` |
> 40	| KPI-VS-004 | QA pass rate (vision_mcp) | `COUNT(qa.consistent=true AND qa.confidence IN ('high','medium')) / COUNT(qa_evaluated)` | ≥ 80% | < 80% | < 60% | `video_renders.qa` + vision_mcp telemetry |
> 41	| KPI-VS-005 | QA gate coverage (pré-render caro) | `COUNT(renders com gate G3 executado) / COUNT(renders com leg i2v/DoP)` | 100% | < 98% | < 90% | `video_renders` + `infra_health_logs` |
> 42	| KPI-VS-006 | Time-to-render (faceless, E2E wall-clock) | `PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY done_at - queued_at)` (5 cenas) | p95 ≤ 12 min | > 12 min | > 20 min (SLA breach) | `video_renders` timestamps |
> 43	| KPI-VS-007 | Time-to-render (HyperFrames render) | `PERCENTILE_CONT(0.95) (done_at - running_at)` (clip ≤30s) | p95 ≤ 90s | > 90s | > 180s | `video_renders` timestamps |
> 44	| KPI-VS-008 | Submit ACK latency | `PERCENTILE_CONT(0.95) OVER (JWT+BYOK+deduct+enqueue)` | p95 < 3s | > 3s | > 5s | Edge Fn logs |
> 45	| KPI-VS-009 | BYOK-configured rate | `COUNT(DISTINCT user_id com gemini_api_key ativa em user_api_keys) / COUNT(DISTINCT tenant ativo)` | ≥ 70% | < 70% | < 40% | `user_api_keys` (mask-safe) + `profiles` |
> 46	| KPI-VS-010 | Refund rate | `COUNT(refunded_mco > 0) / COUNT(charged_mco > 0)` | ≤ 5% | > 8% | > 15% | `video_renders` |
> 47	| KPI-VS-011 | Refund correctness (double-charge guard) | `COUNT(refunded_mco > charged_mco) ` (deve ser 0) + reconciliação delta `mco_balance` | = 0 | ≥ 1 | ≥ 1 (qualquer ocorrência é crítica) | `video_renders` + `profiles.mco_balance` |
> 48	| KPI-VS-012 | Affiliate attach-rate | `COUNT(renders done com affiliate_links.content_id NON-NULL) / COUNT(renders done product-aware)` | ≥ 65% | < 65% | < 40% | `affiliate_links` + `video_renders` |
> 49	| KPI-VS-013 | Real-asset persistence rate | `COUNT(state='done' AND storage_key NOT NULL AND bytes ≥ 100KB) / COUNT(state='done')` | 100% | < 99% | < 95% (stubs vazando) | `video_assets` |
> 50	| KPI-VS-014 | Mesh observation coverage | `COUNT(renders done com node_id NOT NULL) / COUNT(state='done')` | ≥ 99% | < 95% | < 80% | `video_renders` + `mcorch_nodes` |
> 51	| KPI-VS-015 | Edge Fn error rate | `COUNT(5xx) / COUNT(total requests)` por função de render | < 1% | > 1% | > 5% | Supabase logs + `infra_health_logs` |
> 52	| KPI-VS-016 | mcoCoins burn rate | `SUM(charged_mco - refunded_mco) / active_users` (semanal) | dentro da quota do plano | aproxima do teto do plano | esgota quota global | `profiles` + `video_renders` |
> 53	| KPI-VS-017 | Erasure zero-residue rate | `COUNT(erasures com count_after = 0) / COUNT(erasures executadas)` | 100% | < 100% | < 100% (qualquer resíduo é gate de GA bloqueado) | `delete-account` audit + `SELECT` antes/depois |
> 54	| KPI-VS-018 | LTX fallback rate (Ken-Burns) | `COUNT(legs motion via Ken-Burns fallback) / COUNT(legs motion)` | informativo (≤ 40% saudável) | > 60% (cota GPU estrangulando) | > 85% (LTX efetivamente indisponível) | `infra_health_logs` `event='ltx_quota_fallback'` |
> 55	
> 56	---
> 57	
> 58	## 3. FMEA Table
> 59	
> 60	> Severity (S), Occurrence (O), Detection (D): 1 (best) → 10 (worst). **RPN = S × O × D**. **Todo RPN > 100 exige ação recomendada (coluna obrigatória).** Cada FMEA mapeia um FR-VS crítico (FRD §2) e/ou risco de negócio (BRD §8). Os 4 OTD-VS estruturais (untrusted-HTML, shared-daemon, bridge, calibração) concentram o RPN mais alto.
> 61	
> 62	| ID | Function (FR/PROC) | Failure Mode | Effect | S | O | D | RPN | Recommended Action |
> 63	|----|--------------------|--------------|--------|---|---|---|-----|--------------------|
> 64	| FMEA-VS-001 | `hyperframes-render` — untrusted HTML/JS via Puppeteer (FR-VS-025 · OTD-VS-006) | HTML/JS de tenant escapa do sandbox → RCE / SSRF / leitura de env / pivô de rede / vazamento de credencial cross-tenant | Comprometimento do host de render + roubo de segredos de outros tenants (catastrófico) | 10 | 4 | 5 | **200** | **Container per-render efêmero** (`cap_drop=ALL`, `no-new-privileges`, rede egress-only, **ZERO** credencial de tenant no env de render); `/security-review` obrigatório; **bloquear render multi-tenant até selado**; smoke AT-VS-025 (HTML não alcança rede/env) |
> 65	| FMEA-VS-002 | `open-design` daemon compartilhado — BYOK per-user (FR-VS-007 · OTD-VS-002) | Provider BYOK resolvido do config GLOBAL `/app/.od/media-config.json`; `OD_MEDIA_CONFIG_DIR` por invocação NÃO isola (daemon shared) | Chave/quota/receita/risco de um tenant vazam para outro — **fraude por design**; viola R1 + LGPD | 9 | 5 | 4 | **180** | **Re-arquitetura per-user (OTD-VS-002):** daemon per-job efêmero (B preferido) / `od` stateless / container por tenant; manter **single-tenant EXPLÍCITO** até selar; **gate de GA** antes do 2º tenant; AT-VS-013 prova 2 tenants isolados |
> 66	| FMEA-VS-003 | Docker network bridge `n8n_default` ⇄ `mcorch-sovereign-net` (FR-VS-029 · OTD-VS-001) — exposição da ponte | Bridge mal-escopada expõe `vision_mcp`/`chroma` (loopback-only hoje) a tráfego não-autenticado; OU bridge ausente → QA/Chroma são prosa | Superfície de ataque interna ampliada (vision_mcp sem Origin/PAT gate) OU gate de consistência inoperante (crédito caro sem QA) | 8 | 3 | 5 | **120** | **Multi-network attach mínimo (opção A OTD-VS-001)** preservando loopback-only do vision_mcp + **PAT do studio obrigatório** (`VIDEO_STUDIO_PAT`, scopes `vision:read`/`mesh:write`); Origin gate mantido; selar ANTES de qualquer leg de QA; AT-VS-004 handshake |
> 67	| FMEA-VS-004 | `deduct_mco_coins` + refund (FR-VS-011 · PROC-VS-004) | RPC timeout/retry sem idempotência → débito duplo OU refund duplo (double-credit) | Tenant sobrecarregado (perda de confiança) ou MCORCH drenado (perda financeira) | 9 | 3 | 4 | **108** | **Idempotência por `render_id`/`job_id`** em deduct e refund (espelha `finalize_vision_job`/`refundMco`); refund crédito-positivo nunca lança; floor a favor do tenant; CHECK `refunded_mco ≤ charged_mco`; KPI-VS-011 = 0; reconciliação delta `mco_balance` (Lei 1) |
> 68	| FMEA-VS-005 | LTX HF Space i2v — cota ZeroGPU ~5 GPU-min/dia (FR-VS-016) | Cota esgota e o fallback Ken-Burns dispara silenciosamente sem sinal → degradação de qualidade invisível ao tenant | Vídeos entregues com movimento inferior sem aviso; QA pode reprovar tarde; insatisfação | 5 | 6 | 4 | **120** | **Telemetria explícita** `infra_health_logs event='ltx_quota_fallback'` + flag `motion_mode` no `video_renders`; KPI-VS-018 alerta em > 60%; expor "modo movimento" no poll/UI; SOL-VS-004 sinaliza Sovereign em fallback ≥85% |
> 69	| FMEA-VS-006 | `design.mcorch.com` — CF + auth exposure (FR-VS-003 · BR-VS-015) | `OD_API_TOKEN='development_token'` (fraco) + origins abertos + CF bot-challenge bloqueia clientes legítimos não-browser (403) | Acesso não-autorizado ao editor OU editor/automação quebrados (403) — superfície R3 comprometida | 7 | 4 | 4 | **112** | **Token forte rotacionado** (não `development_token`) + `OD_ALLOWED_ORIGINS=https://login.mcorch.com` + **CF WAF Skip rule** p/ requests legítimos; verificar via origin `--resolve`/handshake (nunca curl cru); AT-VS-003; NFR-VS-012 |
> 70	| FMEA-VS-007 | Cascade erasure — `delete-account`/`erase_video_artifacts` (FR-VS-031 · PROC-VS-006) | Erasure incompleta: vídeo/voz clonada/config BYOK/objeto de Storage/embedding residual após delete | Não-conformidade LGPD (Art. 18) + voz biométrica residual (Art. 11); **bloqueio do 2º tenant** | 9 | 3 | 4 | **108** | **Cascade tenant-guarded** (`erase_video_artifacts`) + Storage API remove (lição OTD-VM-026: storage via API, não SQL) + purga explícita do config BYOK open-design; **teste de zero-resíduo** `SELECT` count antes/depois = 0 ≤24h (KPI-VS-017); `/security-review` SAFE; gate de GA |
> 71	| FMEA-VS-008 | VoxCPM — clonagem de voz (FR-VS-032) | Voz de pessoa identificável clonada sem consentimento (`voice_consent=false`) | Exposição legal LGPD Art. 11 (biométrico); template de voz de terceiro vazado/treinado | 8 | 3 | 5 | **120** | **Consent gate HTTP 409** quando `voice_consent` exigido e ausente; recusar clonagem não-autorizada na leg VoxCPM; nunca expor/treinar template biométrico sem consentimento; AT-VS-016c; registro auditável de consentimento |
> 72	| FMEA-VS-009 | `infra_health_logs` (global-read) — telemetria de vídeo (FR-VS-027) | PII per-tenant (topic, produto, prompt, voz) escrita na tabela de leitura global | Vazamento de dados de tenant via tabela global-read (Information Disclosure) | 7 | 3 | 5 | **105** | **Telemetry allowlist no chokepoint** (apenas `service`/`event`/`render_id`/contadores — **sem** topic/prompt/PII per-tenant); precedente vision-mcp; `/security-review` da migration; auditoria de payload |
> 73	| FMEA-VS-010 | Real-asset persistence (FR-VS-030 · Lei 1) | Provider retorna stub JSON/erro mas o pipeline marca `done` confiando na URL efêmera; vídeo < 100KB | Tenant cobrado por um "vídeo" que é um stub de erro; falso-sucesso (viola Lei 1) | 8 | 3 | 3 | 72 | Validar **bytes ≥ 100KB** antes de `state=done` (rejeita stub — precedente `rescue-video`); persistir objeto material no bucket + row `video_assets`; KPI-VS-013 = 100%; prova = objeto, não resposta da API |
> 74	| FMEA-VS-011 | Auth gate — faceless trigger / editor / poll (FR-VS-001/002 · R3) | JWT ausente/inválido não rejeitado no entrypoint → operação anônima OU leitura de render de outro tenant no poll | Acesso não-autenticado a render caro; vazamento cross-tenant via poll | 9 | 2 | 2 | 36 | Hard-fail 401 ANTES de qualquer lógica (`auth.getUser`); poll **tenant-bound** (`render_id` alheio → 404, RLS-scoped); smoke AT-VS-001/002; grep de entrypoints (NFR-VS-008) |
> 75	| FMEA-VS-012 | Per-user provider resolution (FR-VS-005/006 · R1) | Edge fn cai em `Deno.env.get('GEMINI_API_KEY')` global em path user-facing (em vez de 402) | Quota/receita de um tenant consome chave global compartilhada; viola R1; atribuição de receita corrompida | 7 | 3 | 4 | 84 | Resolver por `auth.uid()` em `decrypted_user_api_keys`; **HTTP 402 estruturado** `{error,action}` se ausente; **grep auditável = 0** menções globais em path user-facing (NFR-VS-010); AT-VS-005 |
> 76	| FMEA-VS-013 | n8n asset bootstrap (FR-VS-015) | Helper scripts (`ltx.js`/`composite.sh`/SFX) ausentes em `/home/node/.n8n/assets/` no container | Render faceless falha mid-flight ou produz output corrompido | 5 | 4 | 3 | 60 | **Falha-cedo com erro claro** se assets faltam (preflight check); copiar scripts no provisioning; `docker compose up --build` recria containers ad-hoc; documentar no SOP de deploy |
> 77	| FMEA-VS-014 | Render engine canônico — host `:8088` (OTD-VS-004) | Tanto o container `remotion-render` quanto um node process stray escutam `:8088` → leg de overlay mira o engine errado/conflito de porta | Overlays renderizam em engine não-hardened/ambíguo; resultado não-reproduzível | 4 | 4 | 4 | 64 | **Container `remotion-render` é o engine canônico** (network `n8n_default`, hardened); **matar o stray host process** (remove ambiguidade/conflito de porta); OTD-VS-004 fechada |
> 78	| FMEA-VS-015 | Cost calibration multi-leg (FR-VS-013 · OTD-VS-007) | Constante `VIDEO_FACELESS_RENDER` cravada sem medição real → render multi-leg vendido sub-margem (< 4×-floor) | Operação cara vendida no prejuízo no piso Enterprise; erosão de margem | 6 | 4 | 4 | 96 | **Medir 1 render real no 1º run pago** (G4 `mcoin-cost-calibration.md`) antes de cravar; espelhamento triplo (`billing.ts`+serviço+test, drift=0); nenhuma op < 1× no piso; KPI-VS-003 monitora desvio |
> 79	| FMEA-VS-016 | Telegram delivery — `TELEGRAM_BOT_TOKEN` ausente (FR-VS-018 · OTD-VS-003) | Entrega depende de Telegram como bloqueador único; token ausente everywhere → vídeo gerado mas não entregue | Tenant não recebe o vídeo que pagou; trabalho/crédito perdido na percepção | 6 | 3 | 2 | 36 | **Entrega soberana (signed URL) é o default garantido** (FR-VS-018); Telegram **opcional** per-user/sistema; ausência ≠ bloqueio; entrega NUNCA depende só do bot; OTD-VS-003 |
> 80	| FMEA-VS-017 | Route ordering — `canvas/video` vs `canvas/:id` (FR-VS-022) | Rota `canvas/video` declarada DEPOIS de `canvas/:id` → `:id="video"` sombreia o editor | Botão "Video" abre a rota errada; editor inacessível | 4 | 3 | 2 | 24 | Declarar `canvas/video` **ANTES** de `canvas/:id` em `App.tsx`; componente lazy-loaded; AT-VS-022; E2E 1920×1080 confirma navegação |
> 81	| FMEA-VS-018 | embed-mcorch-node — observação na malha (FR-VS-026) | Embedding API timeout → nó de observação armazenado sem vetor; KPI de receita por render fica cego | Memória semântica/recomendação degradada; busca de roteiro incompleta | 4 | 3 | 4 | 48 | Async retry queue; **backfill** via `scripts/backfill-embeddings.ts`; nó persiste mesmo sem vetor (embed assíncrono); KPI-VS-014 monitora cobertura |
> 82	| FMEA-VS-019 | Deterministic render (FR-VS-024 · NFR-VS-016) | Render HyperFrames não-determinístico (fonte/timing/seed variável) → 2 renders do mesmo input divergem | Quebra a promessa de reprodutibilidade; cache/diff inválido | 4 | 3 | 3 | 36 | Pinnar fonte/seed/timing no contexto de render; 2 renders byte-idênticos (`sha256sum`, AT-VS-024); container de render versionado |
> 83	
> 84	> **FMEA com RPN > 100 (8 itens — ação recomendada obrigatória, preenchida acima):** FMEA-VS-001 (200) · FMEA-VS-002 (180) · FMEA-VS-003 (120) · FMEA-VS-005 (120) · FMEA-VS-008 (120) · FMEA-VS-006 (112) · FMEA-VS-004 (108) · FMEA-VS-007 (108) · FMEA-VS-009 (105). *(9 itens contados — os dois Critical estruturais de execução não-confiável e daemon compartilhado dominam o topo.)*
> 85	
> 86	---
> 87	
> 88	## 4. Self-Optimization Loops
> 89	
> 90	> Loops fecham a malha autonômica: KPI fora de alvo → resposta autônoma (mega-brain-daemon / cron) → escalação humana se persistir. Espelham o padrão do watchdog + `autopilot-analyze`.
> 91	
> 92	| Loop ID | Trigger Condition | KPI Source | Autonomous Response | Escalation (human) |
> 93	|---------|------------------|------------|--------------------|--------------------|
> 94	| SOL-VS-001 | KPI-VS-001/002 render success rate < warn por 2 janelas consecutivas | `video_renders` | `mega-brain-daemon`: health-check dos containers `n8n-n8n-1`/`remotion-render`; restart do container unhealthy; re-bootstrap de assets (FR-VS-015) | Alerta Sovereign se < critical (< 85% faceless) |
> 95	| SOL-VS-002 | KPI-VS-004 QA pass rate < 60% (critical) | `video_renders.qa` + vision_mcp | Auto-ajuste de threshold do gate G3 + injeção de feedback no director Gemini (espelha `orchestrate-step` feedback injection); marcar `qa_failed` mais cedo | Alerta se persistir 7 dias (modelo/prompt drift) |
> 96	| SOL-VS-003 | KPI-VS-003 cost-per-video desvio > 30% (sub-margem) | `video_renders` | Disparar rotina de re-calibração (medir 1 render real, OTD-VS-007); congelar a classe de custo até recalibrar | Alerta Sovereign (decisão de pricing — Owner) |
> 97	| SOL-VS-004 | KPI-VS-018 LTX fallback rate > 85% (LTX indisponível) | `infra_health_logs` `ltx_quota_fallback` | Forçar modo Ken-Burns global temporário + sinalizar "movimento reduzido" no poll/UI; throttle de novos jobs faceless | Alerta Sovereign (cota GPU / provider de vídeo pago) |
> 98	| SOL-VS-005 | KPI-VS-010 refund rate > 15% (critical) | `video_renders` | Análise automática do `<leg>_failed` dominante em `infra_health_logs`; auto-heal da leg falha (restart container / retry); pausar enqueue se a leg estiver morta | Alerta Sovereign + abrir OTD se a causa for arquitetural |
> 99	| SOL-VS-006 | KPI-VS-011 double-charge guard ≥ 1 (qualquer ocorrência) | `video_renders` + `profiles` | **HALT** de novos renders pagos; reconciliação automática do delta `mco_balance`; refund corretivo idempotente | Alerta Sovereign IMEDIATO (incidente financeiro — Lei 1) |
> 100	| SOL-VS-007 | KPI-VS-016 burn rate aproxima do teto do plano do tenant | `profiles` + `video_renders` | Notificação in-app (PT-BR) ao tenant (< 10% da quota); sugerir upgrade Starter→Pro→Enterprise | — (sem auto-ação financeira) |
> 101	| SOL-VS-008 | KPI-VS-009 BYOK-configured rate < 40% (critical) | `user_api_keys` + `profiles` | Nudge in-app de onboarding BYOK (QA grátis via BYOK); destacar `/dashboard/settings` | — (decisão do tenant) |
> 102	
> 103	---
> 104	
> 105	## 5. Self-Healing Specifications
> 106	
> 107	### 5.1 Watchdog Telemetry Events
> 108	
> 109	Novos `event` types escritos em `infra_health_logs` por este módulo (sempre `service='video-studio'`; payload sob **allowlist** — sem PII per-tenant na tabela global-read, FMEA-VS-009):
> 110	
> 111	| Event Type | Trigger | Severity | Payload (allowlist) |
> 112	|------------|---------|----------|---------------------|
> 113	| `render_submitted` | Job aceito (JWT+BYOK+deduct+enqueue OK) | info | `{render_id, engine, charged_mco, estimated_legs}` |
> 114	| `<leg>_failed` (`script`/`image`/`voice`/`motion`/`overlay`/`composite`/`qa`) | Leg falha após retries (PROC-VS-001) | error | `{render_id, leg, retry_count, error_code}` |
> 115	| `render_failed` | Render terminal `failed` após refund | error | `{render_id, engine, failed_leg, refunded_mco}` |
> 116	| `qa_gate_blocked` | Gate G3 reprova consistência (FR-VS-019) | warn | `{render_id, qa_confidence, divergent_attrs_count}` |
> 117	| `ltx_quota_fallback` | LTX ZeroGPU cota/timeout → Ken-Burns (FR-VS-016) | warn | `{render_id, motion_mode:'ken_burns'}` |
> 118	| `refund_applied` | Refund idempotente crédito-positivo aplicado | info | `{render_id, refunded_mco, already_refunded}` |
> 119	| `double_charge_detected` | `refunded_mco > charged_mco` OU delta inconsistente | error | `{render_id, charged_mco, refunded_mco}` |
> 120	| `asset_stub_rejected` | Vídeo < 100KB / stub JSON rejeitado (FR-VS-030) | warn | `{render_id, bytes}` |
> 121	| `byok_missing` | Provider per-user ausente → 402 (FR-VS-005) | warn | `{user_id_hash, service}` |
> 122	| `studio_pat_handshake_failed` | Handshake MCP+PAT do studio falha (R5 · FR-VS-004) | error | `{component:'vision_mcp', http_status}` |
> 123	| `bridge_dns_unresolved` | DNS de container vision_mcp/chroma não resolve (R5) | error | `{target_container}` |
> 124	| `sandbox_spawn_failed` | Container per-render efêmero não sobe (FR-VS-025) | error | `{render_id}` |
> 125	| `voice_consent_blocked` | Clonagem sem consentimento recusada (FR-VS-032) | warn | `{render_id}` |
> 126	| `retention_sweep` | Sweep diário de retenção (PROC-VS-007) | info | `{swept_count, errors_count}` |
> 127	| `erasure_residue_detected` | `delete-account` deixou resíduo (FR-VS-031) | error | `{user_id_hash, residual_table, count}` |
> 128	| `recovery_ok` | Health-check passa após self-heal | info | `{component, action}` |
> 129	
> 130	### 5.2 Auto-Recovery Script Stubs
> 131	
> 132	```bash
> 133	#!/bin/bash
> 134	# scripts/self-heal-video-studio.sh
> 135	# Triggered by mega-brain-daemon when render_failed / <leg>_failed rate spikes
> 136	# (SOL-VS-001 / SOL-VS-005). Targets the Docker render mesh — NOT host nginx.
> 137	
> 138	set -euo pipefail
> 139	TS() { date -u +%Y-%m-%dT%H:%M:%SZ; }
> 140	LOG_TABLE="infra_health_logs"
> 141	SERVICE="video-studio"
> 142	
> 143	echo "[$(TS)] Self-heal triggered for $SERVICE"
> 144	
> 145	# Step 1 — health of the render containers (engine canônico = container, OTD-VS-004)
> 146	for C in n8n-n8n-1 remotion-render mcorch_vision_mcp mcorch_chroma; do
> 147	  STATE=$(docker inspect -f '{{.State.Health.Status}}{{.State.Status}}' "$C" 2>/dev/null || echo "absent")
> 148	  echo "[$(TS)] $C -> $STATE"
> 149	  case "$STATE" in
> 150	    *unhealthy*|absent|*exited*)
> 151	      echo "[WARN] $C degraded ($STATE). Restarting..."
> 152	      docker restart "$C" || echo "[ERR] restart failed for $C"
> 153	      ;;
> 154	  esac
> 155	done
> 156	
> 157	# Step 2 — re-bootstrap n8n helper assets if missing (FR-VS-015 / FMEA-VS-013)
> 158	if ! docker exec n8n-n8n-1 test -f /home/node/.n8n/assets/ltx.js; then
> 159	  echo "[WARN] n8n render assets missing. Re-bootstrapping..."
> 160	  docker cp ./n8n/scripts/ltx.js        n8n-n8n-1:/home/node/.n8n/assets/ltx.js
> 161	  docker cp ./n8n/scripts/composite.sh  n8n-n8n-1:/home/node/.n8n/assets/composite.sh
> 162	  bash ./scripts/gen-sfx.sh   # docker exec ffmpeg lavfi SFX library
> 163	fi
> 164	
> 165	# Step 3 — verify the studio identity bridge (R5 · FR-VS-004 · FMEA-VS-003)
> 166	#   handshake MCP+PAT against vision_mcp via the bridged network (loopback-only origin gate preserved)
> 167	HS=$(curl -s -o /dev/null -w "%{http_code}" \
> 168	  -H "Authorization: Bearer $VIDEO_STUDIO_PAT" \
> 169	  -H "Origin: https://login.mcorch.com" \
> 170	  http://mcorch_vision_mcp:3200/healthz || echo "000")
> 171	[ "$HS" = "200" ] || echo "[ERR] studio PAT handshake to vision_mcp failed (status=$HS)"
> 172	
> 173	# Step 4 — log recovery attempt (allowlist payload; via Supabase REST + SB_SECRET_KEY)
> 174	echo "[$(TS)] Self-heal pass complete for $SERVICE (handshake=$HS)"
> 175	# → INSERT infra_health_logs { service:'video-studio', event:'recovery_ok', metadata:{...allowlist} }
> 176	```
> 177	
> 178	> **Idempotência e blast radius:** o stub atua APENAS sobre containers da malha de render (Docker) — **nunca** toca `login.mcorch.com` (nginx/CloudPanel do host, fora do Docker). `docker restart` é idempotente; re-bootstrap de assets é no-op se já presentes. Refund nunca é acionado pelo self-heal (separação de responsabilidade financeira — só a edge fn refunda, por `render_id`).
> 179	
> 180	### 5.3 mega-brain-daemon Integration Points
> 181	
> 182	| Daemon Event | Condition | Action |
> 183	|-------------|-----------|--------|
> 184	| `health_check` | Cada 5 min (`scripts/watchdog-mcorch.sh`) | Inspecionar `n8n-n8n-1`/`remotion-render`/`mcorch_vision_mcp`/`mcorch_chroma` + `video_renders` queue depth vs baseline; pulse ao Neural HUD via `get-infra-status` |
> 185	| `anomaly_detected` | `infra_health_logs` error rate (`<leg>_failed`/`render_failed`) > 5/hora (SOL-VS-005) | Executar `self-heal-video-studio.sh`; identificar a leg dominante; throttle de enqueue se a leg estiver morta |
> 186	| `quota_pressure` | `ltx_quota_fallback` > 85% por 1h (SOL-VS-004) | Forçar modo Ken-Burns global temporário; sinalizar Sovereign (cota GPU) |
> 187	| `financial_anomaly` | `double_charge_detected` ≥ 1 (SOL-VS-006) | **HALT** de renders pagos + reconciliação delta `mco_balance` + alerta Sovereign IMEDIATO |
> 188	| `bridge_down` | `bridge_dns_unresolved`/`studio_pat_handshake_failed` (R5) | Re-attach de rede / re-emitir/recarregar `VIDEO_STUDIO_PAT`; bloquear leg de QA até handshake OK |
> 189	| `recovery_confirmed` | Health-check passa após self-heal | INSERT `recovery_ok` em `infra_health_logs` + limpar flag de anomalia |
> 190	
> 191	---
> 192	
> 193	## 6. SLA / SLO / SLI Definitions
> 194	
> 195	| Service | SLI (o que medimos) | SLO (nosso alvo) | SLA (consequência contratual) |
> 196	|---------|----------------------|------------------|-------------------------------|
> 197	| `video-faceless-render` submit API | p95 ACK latency (JWT+BYOK+deduct+enqueue) | ≤ 3s | Crédito de mcoCoins emitido se > 5s para > 1% das chamadas/mês |
> 198	| Faceless render pipeline (E2E) | p95 wall-clock (5 cenas, queued→done) | ≤ 12 min | Incident report + refund se > 20 min (SLA breach) e o render não concluir |
> 199	| `video-hyperframes-render` | p95 render wall-clock (clip ≤30s) | ≤ 90s | Refund se > 180s sem entrega |
> 200	| Vision QA gate (`compare` BYOK) | p95 latência do gate G3 | ≤ 6s | Não bloqueia entrega; degradação loga em `infra_health_logs` |
> 201	| mcoCoins deduct/refund | % renders com débito atômico correto + refund íntegro | 100% (double-charge = 0) | Reconciliação + crédito corretivo; incidente financeiro se ≥ 1 |
> 202	| Asset persistence | % renders `done` com objeto material ≥ 100KB no bucket | ≥ 99% | Auto-rejeição de stub + refund; nenhum cobrado por stub |
> 203	| Erasure cascade (LGPD) | % erasures com zero-resíduo ≤ 24h | 100% | Gate de GA bloqueado; remediação obrigatória antes do 2º tenant |
> 204	| Uptime das superfícies de vídeo (studio + editor + vision_mcp bridge) | % minutos disponível/mês (watchdog `*/5`) | ≥ 99.0% | Por contrato enterprise; incident report se < 99.0% |
> 205	| Knowledge Mesh embedding (observação de render) | % nós com embedding ≤ 5 min do insert | ≥ 95% | Auto-backfill via `scripts/backfill-embeddings.ts` |
> 206	
> 207	---
> 208	
> 209	## 7. PDCA Improvement Cadence
> 210	
> 211	| Cycle | Phase | Activity | Owner | Frequency |
> 212	|-------|-------|----------|-------|-----------|
> 213	| video-studio Quality | **Plan** | Revisar FMEA-VS (RPNs) + alvos de KPI-VS; confirmar fechamento de OTD-VS-001..007 antes de cada Fatia | Sovereign | Quarterly (e ao abrir cada Fatia) |
> 214	| video-studio Quality | **Do** | Implementar a ação de RPN mais alto aberta (top: FMEA-VS-001 sandbox, FMEA-VS-002 BYOK open-design); medir 1 render real (OTD-VS-007) | Engineering | Per sprint |
> 215	| video-studio Quality | **Check** | Comparar KPI-VS vs alvo; recalibrar RPNs (sandbox/daemon selados ↓ Occurrence); recalibrar cost classes pós-medição | AIOS / `mega-brain-daemon` | Monthly |
> 216	| video-studio Quality | **Act** | Fechar a malha: atualizar este doc + Risk Register (BRD §8); registrar OTD-VS fechada; promover lição a `docs/processes/` (Lei 2 — Anticorpo) | Sovereign | Monthly |
> 217	
> 218	**Improvement backlog location:** `.claude/context/sprint-priorities.md` (OE-661-ROADMAP) + tasks `video-studio` (#2..#7).
> 219	**Gates de GA (não-negociáveis antes do 2º tenant externo):** FMEA-VS-001 (sandbox per-render selado) · FMEA-VS-002 (BYOK open-design isolado) · FMEA-VS-007 (erasure zero-resíduo provada). Sem os três, GA bloqueado.
> 220	
> 221	---
> 222	
> 223	## 8. Observability Checklist
> 224	
> 225	### 8.1 Logging Events
> 226	
> 227	| Event | Location | Level | Fields logged (allowlist) |
> 228	|-------|----------|-------|---------------------------|
> 229	| Function entry | `video-faceless-render`/`video-hyperframes-render`/`video-render-poll` `index.ts` ~L10 | INFO | `{user_id, request_id, timestamp}` |
> 230	| BYOK resolve | Após `auth.getUser`, antes da leg | INFO | `{user_id_hash, service, resolved:boolean}` (sem a chave) |
> 231	| mcoCoins deduction | Após `deduct_mco_coins` RPC | INFO | `{user_id, render_id, amount, new_balance}` |
> 232	| Leg transition | Worker n8n / sandbox, por leg | INFO | `{render_id, leg, status, elapsed_ms}` |
> 233	| QA gate verdict | Após `vision.compare` (G3) | INFO | `{render_id, consistent, confidence}` |
> 234	| Business logic error | Catch block de cada leg | ERROR | `{render_id, leg, error_code, stack}` (sem PII/prompt) |
> 235	| Refund applied | Após refund idempotente | WARN | `{render_id, refunded_mco, already_refunded}` |
> 236	| SLA breach | Timeout guard (submit / E2E / render) | WARN | `{render_id, process_id, elapsed_ms, threshold_ms}` |
> 237	
> 238	### 8.2 Alerting Rules
> 239	
> 240	| Condition | Channel | Escalation |
> 241	|-----------|---------|------------|
> 242	| `<leg>_failed`/`render_failed` rate > 5/hora | `infra_health_logs` insert | `mega-brain-daemon` `anomaly_detected` → self-heal |
> 243	| `double_charge_detected` ≥ 1 | `infra_health_logs` insert | HALT renders pagos + alerta Sovereign IMEDIATO (Lei 1) |
> 244	| p95 submit ACK > 5s OU render E2E > 20 min | `infra_health_logs` insert + Neural HUD | Sovereign notification (SLA breach) |
> 245	| `ltx_quota_fallback` > 85% por 1h | `infra_health_logs` insert | Sovereign (cota GPU / provider de vídeo pago) |
> 246	| `bridge_dns_unresolved`/`studio_pat_handshake_failed` | `infra_health_logs` insert | `mega-brain-daemon` `bridge_down` → re-attach/re-PAT |
> 247	| `erasure_residue_detected` ≥ 1 | `infra_health_logs` insert | Gate de GA bloqueado + Sovereign + remediação obrigatória |
> 248	| KPI-VS-009 BYOK-configured < 40% | Scheduled check | AIOS nudge de onboarding (SOL-VS-008) |
> 249	
> 250	### 8.3 Distributed Tracing Touchpoints
> 251	
> 252	| Span | Start | End | Tags |
> 253	|------|-------|-----|------|
> 254	| `video-faceless-render.submit` | Request recebido | 202 enviado | `user_id`, `render_id`, `status_code` |
> 255	| `*.byok_resolve` | Antes do lookup `decrypted_user_api_keys` | Após resolve | `service`, `resolved` |
> 256	| `*.mco_deduct` | Antes do RPC `deduct_mco_coins` | Após RPC | `render_id`, `amount`, `balance_after` |
> 257	| `faceless.pipeline` | Worker n8n dispara | Render terminal (`done`/`failed`/`qa_failed`) | `render_id`, `engine`, `terminal_state` |
> 258	| `faceless.leg.<name>` | Início da leg (script/image/voice/motion/overlay/composite/qa) | Fim da leg | `render_id`, `leg`, `status`, `motion_mode` |
> 259	| `*.qa_gate` | Antes de `vision.compare` (PAT do studio) | Após verdict | `render_id`, `consistent`, `confidence` |
> 260	| `hyperframes.sandbox` | Spawn do container per-render | Teardown | `render_id`, `isolated:true` |
> 261	| `*.mesh_observe` | Antes do INSERT `mcorch_nodes` + embed | Após embed | `render_id`, `node_id`, `embed_ok` |
> 262	| `*.asset_persist` | Antes do upload ao bucket | Após row `video_assets` | `render_id`, `bytes`, `≥100KB:boolean` |
> 263	
> 264	---
> 265	
> 266	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 267	
> ```

## 🤖 Claude *(01:26:32)*

Now let me search for specific content related to agency/enterprise plans, pricing, team seats, RBAC, and agency dashboards:

## 🤖 Claude *(01:26:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -r \"agency\\|Enterprise\\|Pro\\|Starter\\|plan.*tier\\|seat\\|role\\|RBAC\\|resale\\|wholesale\\|margin\" /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/ --include=\"*.md\" | head -60"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:**Project:** video-studio
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:## 2. Market Problem Statement
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:- **Process gap:** não há SOP que una "gerar barato → QA com olho criativo (VLM) → portão de consistência → só então gastar crédito caro". O criador gasta crédito de vídeo em frames inconsistentes porque não há gate antes do gasto.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:| SOM (Serviceable Obtainable Market) | R$ ~6,8 mi/ano (24m) | Captura realista 2% do SAM em 24 meses, ancorada na conversão Starter/Pro/Enterprise existente do MCORCH e no crescimento orgânico via o próprio conteúdo gerado (loop viral) |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:| Pilha manual CapCut + ElevenLabs (+ ChatGPT) | "Do it yourself" — ferramentas avulsas | Baratíssimo/grátis, controle total, ubíquo | 1–3h por vídeo; zero acúmulo de aprendizado; sem consistência entre frames; cota ElevenLabs em USD; republicação manual; nenhuma atribuição de custo/receita | Autonomia E2E (roteiro→voz→vídeo→QA→entrega) num clique, com voz clonada VoxCPM livre, consistência travada por seed/reference + portão VLM, e monetização embutida |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:| NPS | Net Promoter Score do módulo de vídeo | ≥ 35 | ≥ 50 | Survey mensal in-app aos tenants ativos |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:**Project:** video-studio
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:| FR-VS-002 | Auth gate — HyperFrames editor | A rota `/dashboard/canvas/video` é protegida por `DashboardLayout`/`ProtectedRoute`; sessão ausente redireciona para `/auth`; a edge function `video-hyperframes-render` valida JWT antes do render. | Critical | PR-VS-002, PR-VS-009 | UI/EdgeFunction | AT-VS-002 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:| FR-VS-006 | Env-global fallback restrito | `Deno.env.get` de chave global SÓ é permitido em cron/service-role (sem `auth.uid()`), onboarding default explícito, ou paths de trigger sem JWT; nunca como caminho primário user-facing. Auditável por grep = 0 menções globais em paths user-facing. | Critical | PR-VS-003 | EdgeFunction | AT-VS-005 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:| FR-VS-017 | Product-aware script + monetização | O director Gemini gera roteiro product-aware (quando há produto escolhido); as 3 superfícies de texto/entrega recebem link afiliado ML + UTM; `affiliate_links.content_id` NON-NULL liga o link ao asset gerado. | High | PR-VS-012 | EdgeFunction | AT-VS-012 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:| FR-VS-021 | Native React embed | O editor HyperFrames é embedado NATIVAMENTE via os componentes React exportados pelo `@hyperframes/studio` (`StudioApp`, `NLELayout`, `NLEPreview`, `Player`, `Timeline`, `SourceEditor`, `PropertyPanel`) — NÃO um iframe a um dev server `npx hyperframes preview`. Renderiza timeline + preview ao vivo + CodeMirror + hot reload dentro do cockpit. | Critical | PR-VS-009 | UI | AT-VS-021 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:| FR-VS-030 | Real asset persistence | Todo vídeo/imagem/áudio gerado termina como objeto material em bucket privado (`generated-videos`/`video-studio-assets`) com row de asset (`storage_key`/`public_url`); nunca confiar em URL efêmera do provider. Prova = objeto no bucket (≥100KB p/ vídeo), não a resposta da API. | High | PR-VS-007 | DB/Container | AT-VS-007 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:| Provider / Service | Used by leg | Auth resolution | Contract surface |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:| `video_renders.product_id` | uuid | Yes | FK product do tenant (se product-aware) | "Produto não encontrado." |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:**Project:** video-studio
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:**Decisão:** o editor é embedado consumindo os componentes React exportados pelo `@hyperframes/studio` (`StudioApp`, `NLELayout`, `NLEPreview`, `Player`, `Timeline`, `SourceEditor`, `PropertyPanel`) — **não** um iframe a `npx hyperframes preview` (localhost:3002, dev server sem modo produção/auth documentado — OTD-VS-005). O embed nativo herda a sessão MCORCH (R3) sem postMessage cross-origin, e o render acontece server-side numa edge function + sandbox (não no dev server local).
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:| Component | File | Props | Hook consumed |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:| `erase_video_artifacts(p_user_id)` | RPC (SECURITY DEFINER, service-role) | Cascade LGPD: rows + Storage + nós/embeddings + config BYOK (espelha `erase_vision_artifacts`/`erase_lead`) | `<ts>_video_studio_erase_rpc.sql` |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md: │  (ProtectedRoute → /auth se sem sessão)    │ embed nativo @hyperframes/studio                 │
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md: │   env global SÓ em cron/service-role/onboarding default (sem auth.uid())
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:-- UPDATE de estado/refund é server-side (service-role) — sem policy de UPDATE p/ authenticated.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:`erase_video_artifacts(p_user_id)` (SECURITY DEFINER, service-role, `search_path=''`) — espelha `erase_vision_artifacts`/`erase_lead`:
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:Ordem obrigatória (API Tenancy Model): (1) per-user `decrypted_user_api_keys` por `auth.uid()`; (2) env global SÓ em cron/service-role/onboarding default sem `auth.uid()`; (3) hard-fail 402 `{error, action}` se nenhum resolve. Anti-pattern banido: `Deno.env.get('<SERVICE>_API_KEY')` em path user-facing sem fallback per-user (grep = 0 · NFR-VS-010).
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:| OTD-VS-001 | **Docker network bridge** p/ vision_mcp QA + chroma memory (R5 · bloqueador MVP) | Attach `n8n`/`remotion` containers à `constellation-orchestra_mcorch-sovereign-net` (multi-network) | Proxy dedicado (sidecar) que ponteia loopback ↔ rede sovereign | Expor vision_mcp/chroma na `n8n_default` também (dual-attach do lado sovereign) | **A** — multi-network attach é o menos invasivo (DNS de container resolve direto), preserva o loopback-only do vision_mcp; emitir `VIDEO_STUDIO_PAT` p/ a identidade do studio. Selar ANTES de qualquer leg de QA | Sovereign |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:| OTD-VS-003 | **Telegram delivery** (`TELEGRAM_BOT_TOKEN` ausente everywhere; `GEMINI_API_KEY` só no `.env` da constellation) | Provisionar bot **per-user** (cada tenant conecta seu bot) | Bot **de sistema** único (entrega via 1 bot compartilhado) | Telegram **opcional** (link soberano sempre; Telegram off por default) | **C + A** — entrega soberana (signed URL) é o caminho garantido (FR-VS-018); Telegram per-user como opt-in. Entrega NUNCA depende só do bot | Sovereign |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/08-quality-metrics.md:**Project:** video-studio
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/08-quality-metrics.md:**BoK Applied:** CMQ/OE BOK (Process Management + Organizational Excellence)
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/08-quality-metrics.md:| QO-VS-003 | **Margem sustentável** — custo-por-vídeo dentro do modelo 4×-floor | BO-VS-001, BO-VS-003 | 100% das classes mco ≥ `ceil(usd/$0.0045)`; nenhuma op sub-1× no piso Enterprise | Monthly (revisão de calibração) |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/08-quality-metrics.md:| FMEA-VS-002 | `open-design` daemon compartilhado — BYOK per-user (FR-VS-007 · OTD-VS-002) | Provider BYOK resolvido do config GLOBAL `/app/.od/media-config.json`; `OD_MEDIA_CONFIG_DIR` por invocação NÃO isola (daemon shared) | Chave/quota/receita/risco de um tenant vazam para outro — **fraude por design**; viola R1 + LGPD | 9 | 5 | 4 | **180** | **Re-arquitetura per-user (OTD-VS-002):** daemon per-job efêmero (B preferido) / `od` stateless / container por tenant; manter **single-tenant EXPLÍCITO** até selar; **gate de GA** antes do 2º tenant; AT-VS-013 prova 2 tenants isolados |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/08-quality-metrics.md:| FMEA-VS-010 | Real-asset persistence (FR-VS-030 · Lei 1) | Provider retorna stub JSON/erro mas o pipeline marca `done` confiando na URL efêmera; vídeo < 100KB | Tenant cobrado por um "vídeo" que é um stub de erro; falso-sucesso (viola Lei 1) | 8 | 3 | 3 | 72 | Validar **bytes ≥ 100KB** antes de `state=done` (rejeita stub — precedente `rescue-video`); persistir objeto material no bucket + row `video_assets`; KPI-VS-013 = 100%; prova = objeto, não resposta da API |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/08-quality-metrics.md:| FMEA-VS-015 | Cost calibration multi-leg (FR-VS-013 · OTD-VS-007) | Constante `VIDEO_FACELESS_RENDER` cravada sem medição real → render multi-leg vendido sub-margem (< 4×-floor) | Operação cara vendida no prejuízo no piso Enterprise; erosão de margem | 6 | 4 | 4 | 96 | **Medir 1 render real no 1º run pago** (G4 `mcoin-cost-calibration.md`) antes de cravar; espelhamento triplo (`billing.ts`+serviço+test, drift=0); nenhuma op < 1× no piso; KPI-VS-003 monitora desvio |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/08-quality-metrics.md:| SOL-VS-007 | KPI-VS-016 burn rate aproxima do teto do plano do tenant | `profiles` + `video_renders` | Notificação in-app (PT-BR) ao tenant (< 10% da quota); sugerir upgrade Starter→Pro→Enterprise | — (sem auto-ação financeira) |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/08-quality-metrics.md:| `byok_missing` | Provider per-user ausente → 402 (FR-VS-005) | warn | `{user_id_hash, service}` |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/00-index.md:## Project Metadata
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/00-index.md:| Regulatory Profile | LGPD (elevado — voz clonada Art. 11 + dados de mídia + erasure Art. 16/18) |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/00-index.md:| Project Slug | `video-studio` |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/00-index.md:| 0 | `00-index.md` | Project Manifest | — | [x] complete |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/00-index.md:| 3 | `03-prd.md` | Product Requirements Document | ProdBOK + CXBOK | [x] complete |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/00-index.md:| 7 | `07-process-flow.md` | Process & Automation Blueprint | BPM CBOK v4 | [x] complete |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/00-index.md:| 0 | Project Bootstrap | 2026-06-21 | slug video-studio |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/00-index.md:| 2 | Product Definition | 2026-06-21 | PR-VS + 2 personas + Gherkin |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/00-index.md:| 4 | Data & Process Engineering | 2026-06-21 | 4 tabelas + RPC erasure + 8 PROC-VS |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:# Process Flow — Process & Automation Blueprint
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:**Project:** video-studio
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:**BoK Applied:** BPM CBOK v4 (Process Modeling · Analysis · Design · Performance Management)
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:## 1. Process Inventory
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:| Process ID | Name | Type | Trigger | Owner | FR traced | Tabelas tocadas | SLA |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:| PROC-VS-008 | n8n asset bootstrap (helper scripts + SFX) | `human-in-loop` (setup 1×) | Provisão do studio | Operator (Engineering) | FR-VS-015 | (filesystem do container `n8n-n8n-1`) | setup único |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:## 2. BPMN-lite Process Maps
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md: /dashboard/canvas/video ───────────────────▶ (rota ANTES de canvas/:id — FR-VS-022; ProtectedRoute → /auth se sem sessão R3)
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md: │   env global SÓ em cron/service-role/onboarding default (sem auth.uid())
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:> **Regra-mãe (charge-at-entry + refund-on-failure):** todo path billable cobra na entrada e estorna em qualquer falha pós-débito — herdada de `_shared/billing.ts`/`finalize_vision_job` (service-role-only, idempotente por `refunded_at`, nunca lança). Retry de poll nunca dobra cobrança nem dispatch. 401/402/409 nunca debitam.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:  ▶ video-delete-account / delete-account (service-role) chama erase_video_artifacts(p_user_id)
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:  ▶ guard de tenant (p_user_id = auth.uid() OR service_role) ─ não ─▶ 42501 forbidden ⛔
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:  ▶ CALLER (service-role) remove objetos de Storage (bucket video-studio-assets) via Storage API (OTD-VM-026)
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:| Process | Step | Error Type | Max Retries | Backoff | Failure Action |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:| Process | Step | Duração esperada | Timeout / Threshold | Alert se exceder | NFR |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:## 7. Traceability (Process → FR → Tabela)
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md:**Project:** video-studio
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md:| SH-VS-007 | Providers externos (Gemini, Pollinations, LTX HF, VoxCPM, Mercado Livre) | Low | Medium | On license/quota change | Termos/dashboards de cada provider |
> ```

## 🤖 Claude *(01:26:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -r \"affiliate.*split\\|revenue.*split\\|margin\\|agency ROI\\|unit economics\" /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/ --include=\"*.md\""
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> (Bash completed with no output)
> ```

## 🤖 Claude *(01:26:37)*

Let me search more specifically for agency-related content and plan tier definitions:

## 🤖 Claude *(01:26:38)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"ag\u00eancia\\|operador de ag\u00eancia\\|Marina\\|segmento secund\u00e1rio\\|SH-VS-003\" /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md | head -20"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 23:| BO-VS-002 | Embedar o editor programático HyperFrames no cockpit, multi-tenant e sandboxed | Rota nativa `/dashboard/canvas/video` (React embed, não iframe a dev server) renderiza HTML→MP4 determinístico com render isolado per-tenant | ≥ 1 MP4 determinístico renderizado por tenant via sandbox sem credencial compartilhada no ambiente de render | Pacote `@hyperframes/studio` exporta componentes React p/ embed nativo; porta 3002 livre no host | Núcleo do segmento secundário/agência (MR-VS-002) | v1.0 — após sandbox per-render (OTD-VS-006) selado |
> 36:| SH-VS-003 | Operador de agência (segmento secundário) | High | Medium | Bi-weekly onboarding multi-tenant | Pipeline comercial v6.5.0+ |
> 93:| 12-month ROI | ~ +18% (conservador; depende da ativação do segmento agência em v1.0) |
> ```

## 🤖 Claude *(01:26:39)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"plan\\|Starter\\|Pro\\|Enterprise\\|mcoCoins.*table\" /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 3:**Project:** video-studio
> 40:| SH-VS-007 | Providers externos (Gemini, Pollinations, LTX HF, VoxCPM, Mercado Livre) | Low | Medium | On license/quota change | Termos/dashboards de cada provider |
> 86:| Upsell de plano (volume de render puxa Pro/Enterprise) | Assinatura | R$ ~3.500/mês | Vídeo é operação cara → consome mcoCoins → puxa upgrade Starter→Pro→Enterprise |
> 94:| IRR (estimated) | ~22% a/a (sensível à attach-rate de afiliado e ao mix Pro/Enterprise) |
> 100:> Modelo 4×-floor: `mco = ceil(custo_usd_real / $0.018 × 4) = ceil(custo_usd / $0.0045)`. Floor = piso Enterprise R$997/10000 mco. Espelhamento triplo (`src/lib/billing.ts` + constante do serviço + `billing.test.ts`). Classe final SÓ após medição material no 1º render pago (OTD-VS-007).
> 104:| `VIDEO_FACELESS_RENDER` (multi-leg: Gemini + LTX + Remotion + FFmpeg) | ~125 (provisório, paridade com canvas video DoP; recalibrar pós-medição — OTD-VS-007) | Starter(500)≈4 vídeos / Pro(2000)≈16 / Ent(10k)≈80 | ~320 renders | R$ ~3.200 |
> 105:| `VIDEO_HYPERFRAMES_RENDER` (Chrome headless + FFmpeg, sem leg de IA pesada) | ~12 (provisório — render local barato; análogo a IMAGE_GENERATION; OTD-VS-007) | Starter≈41 / Pro≈166 / Ent≈833 | ~600 renders | R$ ~700 |
> 130:- HyperFrames (Apache-2.0) exporta componentes React (`StudioApp`, `NLELayout`, `NLEPreview`, `Player`, `Timeline`, `SourceEditor`, `PropertyPanel`) estáveis o suficiente p/ embed nativo (não iframe a dev server).
> 138:| Risk ID | Description | Probability | Impact | RPN | Mitigation |
> 150:> Probability & Impact: 1=Low, 5=High. RPN = Probability × Impact.
> 161:| BAC-VS-004 | Provider resolvido per-user; 402 estruturado quando não configurado; zero env-key global em path user-facing | Smoke 402 `{error, action}` + grep de env global em paths user-facing = 0 |
> ```

## 🤖 Claude *(01:26:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"agency\\|ag\u00eancia\\|segmento ag\u00eancia\\|multi-tenant\" /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/03-prd.md"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 16:Para o **criador faceless e o operador de agência brasileiros** que precisam produzir vídeo vertical em volume, consistente e monetizado sem montar um pipeline manual nem pagar SaaS em dólar, o **MCORCH Video Studio** é um **estúdio de vídeo soberano de dois motores** — geração autônoma E2E (Faceless Studio) + edição programática determinística (HyperFrames Editor) — que entrega vídeo pronto-para-publicar com voz clonada, movimento real, QA por olho criativo e link de afiliado embutido, tudo dentro do cockpit MCORCH. Diferente de HeyGen/Synthesia/Argil (USD, jardim murado, criador não monetiza) e da pilha manual CapCut+ElevenLabs (lenta, sem consistência, sem aprendizado), nosso produto cobra em mcoCoins (R$), resolve credenciais per-user, gateia o gasto caro por um portão de consistência, persiste assets reais e conecta cada render à malha de conhecimento e ao programa de afiliados Mercado Livre.
> 37:| Role | Operadora/editora numa micro-agência que produz vídeo data-driven para vários clientes |
> 41:| MCORCH usage pattern | Abre `/dashboard/canvas/video`, edita HTML/props na timeline com preview ao vivo, renderiza MP4 determinístico por cliente, debita do plano da agência |
> 72:| Retention | Versiona templates, gera lotes por cliente, escala a agência sem caos de credencial | Biblioteca de templates + BYOK per-tenant | ❤️ Loyal | Plano Enterprise; isolamento provado vira argumento de venda |
> 99:| PR-VS-010 | Sandbox per-render para HTML/JS de tenant (container isolado, sem credencial no env de render) | Marina | BR-VS-010 | L | (incl. no render) | **Gating do render multi-tenant** (OTD-VS-006); `/security-review` |
> 146:**Condition:** segmento agência ativado em escala + demanda de lote/publicação direta comprovada; cada item entra após métrica de uso do v1.0.
> ```

## 🤖 Claude *(01:26:42)*

Now let me search for information about team roles, RBAC, multi-client features, and ledger/reconciliation:

## 🤖 Claude *(01:26:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"owner\\|billing-admin\\|editor\\|role\\|RBAC\\|SH-VS-003\" /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/ --include=\"*.md\" | grep -v \"^Binary\""
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/00-index.md:14:| Business Idea | Módulo Vídeo do MCORCH — estúdio faceless 100% automático (n8n + Remotion + LTX + Gemini) **e** editor HyperFrames (HTML→MP4), entregues como **apps isolados** dentro do MCORCH |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/00-index.md:63:MR-VS-001..014  (mercado: faceless viral, editor próprio, app isolado)
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:66:| Pilha manual CapCut + ElevenLabs (+ ChatGPT) | "Do it yourself" — ferramentas avulsas | Baratíssimo/grátis, controle total, ubíquo | 1–3h por vídeo; zero acúmulo de aprendizado; sem consistência entre frames; cota ElevenLabs em USD; republicação manual; nenhuma atribuição de custo/receita | Autonomia E2E (roteiro→voz→vídeo→QA→entrega) num clique, com voz clonada VoxCPM livre, consistência travada por seed/reference + portão VLM, e monetização embutida |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:75:O momento converge três maturidades. **(1) Tecnológica:** modelos image-to-video livres/baratos (LTX-Video distilled no HF ZeroGPU, ~5 GPU-min/dia grátis), TTS de voz clonada open (VoxCPM), VLMs de QA baratos via BYOK (Gemini Flash), e editores de vídeo-como-código Apache-2.0 (HyperFrames) chegaram a um patamar utilizável — o que antes exigia GPU dedicada agora roda CPU-only com fallback Ken-Burns. **(2) Comportamental:** o vídeo vertical curto é o formato dominante de descoberta (Shorts/Reels/TikTok), e o "faceless content" virou categoria econômica madura no BR, mas a produção segue manual e não-monetizada. **(3) Regulatória/comercial:** a fase Commercial multi-tenant do MCORCH exige integrações **per-user BYOK** (atribuição de receita por tenant, isolamento de quota e risco, compliance LGPD) — e vídeo é a operação criativa de maior valor a destravar nesse modelo. O MCORCH já possui o cockpit (auth, mcoCoins, malha, afiliado ML, Canvas Studio, Vision MCP como olho criativo) — falta apenas **costurar os motores de vídeo** sob esse modelo. A janela é agora: os blocos livres existem, o formato domina, e o diferencial soberano (R$ + afiliado + malha + LGPD) não tem concorrente direto no BR.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:87:| MR-VS-003 | Toda operação de vídeo gateada por sessão/JWT MCORCH — nunca anônima — incluindo as superfícies isoladas (design.mcorch.com / editor de vídeo) | Critical | Apps isolados são extensão do MCORCH, não produtos abertos; risco de abuso/custo se anônimo | R3 (diretiva Sovereign 2026-06-21) |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:96:| MR-VS-012 | UX de luxo MCORCH coerente nas superfícies humanas (picker de produto/tema, timeline/preview do editor, estados de render) | Medium | Diferenciação experiencial; o módulo é vitrine do cockpit soberano | CXBOK; PRD §6 house style |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:119:| LGPD | Alta — vídeo carrega imagem/voz (voz clonada VoxCPM é dado biométrico potencial), config BYOK do tenant, e HTML/dados arbitrários do editor | Erasure em cascata de artefatos de vídeo/áudio + config BYOK + `OD_DATA_DIR`/`OD_MEDIA_CONFIG_DIR` no `delete-account`; provenance/retention por artefato; consentimento p/ voz clonada; isolamento per-tenant de credencial (Art. 6 finalidade/segurança) | Engineering |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:8:**Regulatory elevation:** LGPD **ELEVADO** — voz clonada (VoxCPM) = dado biométrico potencial (Art. 11); HTML/dados arbitrários do editor; config BYOK por tenant. Erasure (§5.5) e consentimento de voz tratados como Critical.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:82:**Decisão:** o editor é embedado consumindo os componentes React exportados pelo `@hyperframes/studio` (`StudioApp`, `NLELayout`, `NLEPreview`, `Player`, `Timeline`, `SourceEditor`, `PropertyPanel`) — **não** um iframe a `npx hyperframes preview` (localhost:3002, dev server sem modo produção/auth documentado — OTD-VS-005). O embed nativo herda a sessão MCORCH (R3) sem postMessage cross-origin, e o render acontece server-side numa edge function + sandbox (não no dev server local).
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:84:**Gotcha de roteamento (FR-VS-022):** a rota `canvas/video` DEVE ser declarada ANTES de `canvas/:id` em `src/App.tsx` — senão `:id="video"` sombreia a rota nova e o editor nunca carrega.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:86:> ⚠️ `npx skills add heygen-com/hyperframes` instala um **agent skill** (SKILL.md), NÃO a UI do editor. A UI vem do pacote `@hyperframes/studio` (Apache-2.0).
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:155:| `erase_video_artifacts(p_user_id)` | RPC (SECURITY DEFINER, service-role) | Cascade LGPD: rows + Storage + nós/embeddings + config BYOK (espelha `erase_vision_artifacts`/`erase_lead`) | `<ts>_video_studio_erase_rpc.sql` |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:194:### 3.2 Open the HyperFrames editor + deterministic render (FR-VS-021/024/025)
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:226: │   env global SÓ em cron/service-role/onboarding default (sem auth.uid())
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:348:| `design.mcorch.com` (CF→origin) | Superfície exposta com `OD_API_TOKEN=development_token` + origins abertos → acesso não-autenticado ao editor | Spoofing | High | `OD_API_TOKEN` forte rotacionado + `OD_ALLOWED_ORIGINS=https://login.mcorch.com` + CF WAF Skip rule (libera não-browser legítimo sem abrir geral); confirmar via origin `--resolve` (curl cru retorna challenge) (FR-VS-003 · NFR-VS-012) |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:372:-- UPDATE de estado/refund é server-side (service-role) — sem policy de UPDATE p/ authenticated.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:420:`erase_video_artifacts(p_user_id)` (SECURITY DEFINER, service-role, `search_path=''`) — espelha `erase_vision_artifacts`/`erase_lead`:
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:429:Ordem obrigatória (API Tenancy Model): (1) per-user `decrypted_user_api_keys` por `auth.uid()`; (2) env global SÓ em cron/service-role/onboarding default sem `auth.uid()`; (3) hard-fail 402 `{error, action}` se nenhum resolve. Anti-pattern banido: `Deno.env.get('<SERVICE>_API_KEY')` em path user-facing sem fallback per-user (grep = 0 · NFR-VS-010).
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:18:- Auth MCORCH (JWT/sessão) gating de TODA superfície de vídeo — faceless trigger, editor HyperFrames, `design.mcorch.com` (R3 · PR-VS-002).
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:43:| FR-VS-002 | Auth gate — HyperFrames editor | A rota `/dashboard/canvas/video` é protegida por `DashboardLayout`/`ProtectedRoute`; sessão ausente redireciona para `/auth`; a edge function `video-hyperframes-render` valida JWT antes do render. | Critical | PR-VS-002, PR-VS-009 | UI/EdgeFunction | AT-VS-002 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:44:| FR-VS-003 | Auth gate — design.mcorch.com | O acesso ao editor open-design via `design.mcorch.com` exige `OD_API_TOKEN` forte (não `development_token`), `OD_ALLOWED_ORIGINS=https://login.mcorch.com`, e CF WAF Skip rule p/ requests não-browser legítimos; request sem origem permitida/token → 401/403. | Critical | PR-VS-002, PR-VS-014 | Container | AT-VS-003 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:52:| FR-VS-006 | Env-global fallback restrito | `Deno.env.get` de chave global SÓ é permitido em cron/service-role (sem `auth.uid()`), onboarding default explícito, ou paths de trigger sem JWT; nunca como caminho primário user-facing. Auditável por grep = 0 menções globais em paths user-facing. | Critical | PR-VS-003 | EdgeFunction | AT-VS-005 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:87:| FR-VS-021 | Native React embed | O editor HyperFrames é embedado NATIVAMENTE via os componentes React exportados pelo `@hyperframes/studio` (`StudioApp`, `NLELayout`, `NLEPreview`, `Player`, `Timeline`, `SourceEditor`, `PropertyPanel`) — NÃO um iframe a um dev server `npx hyperframes preview`. Renderiza timeline + preview ao vivo + CodeMirror + hot reload dentro do cockpit. | Critical | PR-VS-009 | UI | AT-VS-021 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:127:| NFR-VS-007 | Availability | Uptime SLO das superfícies de vídeo (studio + editor + vision_mcp bridge) | 99.0%/mês | Watchdog `infra_health_logs` |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:127: │   env global SÓ em cron/service-role/onboarding default (sem auth.uid())
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:148:> **Regra-mãe (charge-at-entry + refund-on-failure):** todo path billable cobra na entrada e estorna em qualquer falha pós-débito — herdada de `_shared/billing.ts`/`finalize_vision_job` (service-role-only, idempotente por `refunded_at`, nunca lança). Retry de poll nunca dobra cobrança nem dispatch. 401/402/409 nunca debitam.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:172:  ▶ video-delete-account / delete-account (service-role) chama erase_video_artifacts(p_user_id)
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:173:  ▶ guard de tenant (p_user_id = auth.uid() OR service_role) ─ não ─▶ 42501 forbidden ⛔
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:178:  ▶ CALLER (service-role) remove objetos de Storage (bucket video-studio-assets) via Storage API (OTD-VM-026)
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:274:| Canvas (Visual Orchestrator) | botão "Video" na TopBar + rota `/dashboard/canvas/video` | O editor HyperFrames vive como uma aba do Canvas (FR-VS-022/023); reusa o layout do cockpit sem novo Zustand store (SDD §2.5). |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:308:| PROC-VS-002 | editor embed first interaction | LCP < 2.5s | — | Não | NFR-VS-003 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:312:| Todas | uptime das superfícies de vídeo (studio+editor+bridge) | 99.0%/mês | — | watchdog `*/5` | NFR-VS-007 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md:23:| BO-VS-002 | Embedar o editor programático HyperFrames no cockpit, multi-tenant e sandboxed | Rota nativa `/dashboard/canvas/video` (React embed, não iframe a dev server) renderiza HTML→MP4 determinístico com render isolado per-tenant | ≥ 1 MP4 determinístico renderizado por tenant via sandbox sem credencial compartilhada no ambiente de render | Pacote `@hyperframes/studio` exporta componentes React p/ embed nativo; porta 3002 livre no host | Núcleo do segmento secundário/agência (MR-VS-002) | v1.0 — após sandbox per-render (OTD-VS-006) selado |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md:36:| SH-VS-003 | Operador de agência (segmento secundário) | High | Medium | Bi-weekly onboarding multi-tenant | Pipeline comercial v6.5.0+ |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md:51:| BR-VS-002 | HyperFrames Editor embedado nativamente (React embed) em `/dashboard/canvas/video`, rota declarada ANTES de `canvas/:id` no App.tsx; botão "Video" ao lado de Pipeline na TopBar | MR-VS-002 | Critical | `VIDEO_HYPERFRAMES_RENDER` (Chrome+FFmpeg local; calibrado — barato vs leg de IA) | Rota carrega editor logado; render produz MP4 determinístico; `:id="video"` não sombreia |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md:52:| BR-VS-003 | Toda superfície de vídeo (faceless trigger, editor, design.mcorch.com) gateada por sessão/JWT MCORCH; nunca anônima; identidade do studio via PAT/JWT emitido | MR-VS-003 | Critical | — | 401 em request sem identidade verificada; smoke prova rejeição anônima |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md:53:| BR-VS-004 | Gemini e todo provider externo resolvidos per-user via `decrypted_user_api_keys` (`auth.uid()`); env global SÓ em cron/service-role; hard-fail 402 estruturado se não configurado | MR-VS-004 | Critical | — | Zero env-key global em path user-facing; 402 `{error, action}` quando falta config |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md:147:| BR-VS-RISK-008 | CF bot-challenge bloqueia clientes não-browser no design.mcorch.com → editor/automação quebrados | 3 | 3 | 9 | BR-VS-015: WAF Skip rule + token forte + origins restritos; confirmar via origin `--resolve` ou handshake, nunca curl cru |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md:159:| BAC-VS-002 | HyperFrames editor carrega logado em `/dashboard/canvas/video` e renderiza MP4 determinístico em sandbox | E2E logado 1920×1080 + 2 renders idênticos byte-comparáveis; container de render isolado |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/03-prd.md:27:| Goals | Produzir 5–10 vídeos verticais/semana, consistentes e monetizados, sem virar editor de vídeo profissional |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/03-prd.md:37:| Role | Operadora/editora numa micro-agência que produz vídeo data-driven para vários clientes |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/03-prd.md:39:| Frustrations | Remotion exige dev + servidor; SaaS de avatar não dá controle de layout; sem isolamento de credencial por cliente; sem determinismo (cada export sai diferente) |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/03-prd.md:68:| Awareness | Procura editor programático que não exija servidor local | `/dashboard/canvas` (botão Video na TopBar) | 😐 Neutral | Botão "Video" ao lado de Pipeline; "edição como código, sem servidor" |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/03-prd.md:69:| Consideration | Abre o editor embedado, vê timeline + preview ao vivo + CodeMirror | `/dashboard/canvas/video` (HyperFrames embed) | 🤔 Curious | Hot reload + preview determinístico; templates iniciais |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/03-prd.md:91:| PR-VS-002 | Auth MCORCH em todas as superfícies de vídeo (faceless trigger, editor, design.mcorch.com) — 401 anônimo | Léo, Marina | BR-VS-003 | M | — | R3; smoke 401 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/03-prd.md:108:| PR-VS-014 | Hardening design.mcorch.com (`OD_API_TOKEN` forte + `OD_ALLOWED_ORIGINS` + CF WAF Skip rule) | Marina | BR-VS-015 | M | — | Substitui `development_token`; editor logado sem CF challenge |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/03-prd.md:156:| `--bg-deep` | `#0A0A0F` | Canvas background do editor e do studio |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/03-prd.md:176:- **Preview do editor:** preview ao vivo determinístico com hot reload; scrub suave na timeline.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/03-prd.md:183:- Timeline e player totalmente navegáveis por teclado; controles com ARIA labels.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/03-prd.md:228:    When ela atinge o trigger faceless, o editor ou design.mcorch.com
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/08-quality-metrics.md:69:| FMEA-VS-006 | `design.mcorch.com` — CF + auth exposure (FR-VS-003 · BR-VS-015) | `OD_API_TOKEN='development_token'` (fraco) + origins abertos + CF bot-challenge bloqueia clientes legítimos não-browser (403) | Acesso não-autorizado ao editor OU editor/automação quebrados (403) — superfície R3 comprometida | 7 | 4 | 4 | **112** | **Token forte rotacionado** (não `development_token`) + `OD_ALLOWED_ORIGINS=https://login.mcorch.com` + **CF WAF Skip rule** p/ requests legítimos; verificar via origin `--resolve`/handshake (nunca curl cru); AT-VS-003; NFR-VS-012 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/08-quality-metrics.md:74:| FMEA-VS-011 | Auth gate — faceless trigger / editor / poll (FR-VS-001/002 · R3) | JWT ausente/inválido não rejeitado no entrypoint → operação anônima OU leitura de render de outro tenant no poll | Acesso não-autenticado a render caro; vazamento cross-tenant via poll | 9 | 2 | 2 | 36 | Hard-fail 401 ANTES de qualquer lógica (`auth.getUser`); poll **tenant-bound** (`render_id` alheio → 404, RLS-scoped); smoke AT-VS-001/002; grep de entrypoints (NFR-VS-008) |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/08-quality-metrics.md:80:| FMEA-VS-017 | Route ordering — `canvas/video` vs `canvas/:id` (FR-VS-022) | Rota `canvas/video` declarada DEPOIS de `canvas/:id` → `:id="video"` sombreia o editor | Botão "Video" abre a rota errada; editor inacessível | 4 | 3 | 2 | 24 | Declarar `canvas/video` **ANTES** de `canvas/:id` em `App.tsx`; componente lazy-loaded; AT-VS-022; E2E 1920×1080 confirma navegação |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/08-quality-metrics.md:204:| Uptime das superfícies de vídeo (studio + editor + vision_mcp bridge) | % minutos disponível/mês (watchdog `*/5`) | ≥ 99.0% | Por contrato enterprise; incident report se < 99.0% |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/06-data-model.md:8:**Regulatory:** LGPD **ELEVADO** — voz clonada (VoxCPM) = dado biométrico potencial (Art. 11); HTML/dados arbitrários do editor; config BYOK por tenant; erasure em cascata (Art. 18) e retention (Art. 16) tratados como Critical.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/06-data-model.md:137:| `gemini_api_key` (reuso) | text (Vault) | YES | `.insert` na VIEW (NUNCA `.upsert`); null não limpa (clear via RPC) | `decrypted_user_api_keys` (service-role only) |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/06-data-model.md:152:| 1 | `<ts>_video_studio_renders.sql` | `video_renders` (+CHECK engine/state, `refunded_mco ≤ charged_mco`) | default-deny; SELECT/INSERT own; UPDATE service-role; **RESTRICTIVE no client delete** (ledger financeiro) | `(user_id, state)`, `(user_id, created_at DESC)`, `expires_at` |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/06-data-model.md:153:| 2 | `<ts>_video_studio_scenes.sql` | `video_scenes` | default-deny; SELECT own; writes service-role | `(render_id, scene_index)` UNIQUE, `user_id` |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/06-data-model.md:155:| 4 | `<ts>_video_studio_assets.sql` | `video_assets` | default-deny; SELECT own; writes service-role | `render_id`, `user_id`, `retention_until` |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/06-data-model.md:157:| 6 | `<ts>_video_studio_erase_rpc.sql` | `erase_video_artifacts(p_user_id)` SECURITY DEFINER `search_path=''` | EXECUTE revogado de PUBLIC/anon; GRANT authenticated (own via guard) + service_role (sweep) | — |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/06-data-model.md:168:-- CALLER (container erase-broker / delete-account, service-role) remover via Storage API (lição OTD-VM-026).
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/06-data-model.md:178:  -- Guard de tenant (ledger-RPC rule): só o próprio tenant OU service-role pode disparar o cascade.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/06-data-model.md:179:  IF NOT (p_user_id = auth.uid() OR auth.role() = 'service_role') THEN
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/06-data-model.md:207:GRANT  EXECUTE ON FUNCTION public.erase_video_artifacts(uuid) TO authenticated, service_role;
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/06-data-model.md:210:> O `delete-account` (edge fn, service-role) chama esta RPC e ADICIONALMENTE: remove os objetos de Storage (`storage_keys` retornados via Storage API), faz purge das coleções do ChromaDB do tenant (§4.5), e dispara a limpeza do `OD_DATA_DIR`/`OD_MEDIA_CONFIG_DIR` + config global de provider do open-design que carrega a chave BYOK (precedente Canvas Design OTD-008).
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/06-data-model.md:265:| `video_renders` | `user_id = auth.uid()` + `project_id` | SELECT/INSERT own; UPDATE service-role; **RESTRICTIVE no client delete** | poll alheio → 404 (FR-VS-026) |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/06-data-model.md:266:| `video_scenes` | `user_id = auth.uid()` | SELECT own; writes service-role | — |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/06-data-model.md:269:| `user_api_keys` (VIEW) | `user_id = auth.uid()` | máscara; reais no Vault; decrypted view service-role only | — |
> ```

## 🤖 Claude *(01:26:46)*

Let me search for cost attribution, multi-client dashboards, and affiliate/revenue sharing mechanisms:

## 🤖 Claude *(01:26:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"cost.*per\\|attribution\\|dashboard\\|client\\|multi-client\\|ledger\\|reconcile\\|per-tenant cost\" /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/ --include=\"*.md\" | head -40"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:15:O `video-studio` é o módulo de produção de vídeo do MCORCH, entregue como **dois sub-sistemas criativos isolados ("apps dentro do app")**, ambos gateados por sessão/JWT MCORCH, débito atômico de mcoCoins e credenciais BYOK per-user: **(A) FACELESS STUDIO** — uma fábrica autônoma de vídeos verticais sem rosto (cérebro = workflow n8n existente: Gemini director/QA → Pollinations → VoxCPM TTS clonado → Remotion HUD/captions → LTX image-to-video → FFmpeg composite → QA Gemini-vision → entrega) — e **(B) HYPERFRAMES EDITOR** — um NLE agent-first (HeyGen HyperFrames, Apache-2.0) que renderiza HTML/CSS/JS em MP4 determinístico via Chrome headless + FFmpeg, embedado nativamente em `/dashboard/canvas/video`. O problema de mercado é agudo: criadores e agências brasileiras gastam horas em CapCut + ElevenLabs + ferramentas avulsas para montar um único Short/Reel, enquanto plataformas SaaS de avatar (HeyGen/Synthesia) custam em USD, não monetizam o criador e não conectam a uma malha de conhecimento ou a um programa de afiliados. O `video-studio` une **geração autônoma barata (CPU-only, free tools)** + **edição programática determinística** dentro de um cockpit soberano que já carrega auth, billing per-render, persistência de assets reais e monetização via afiliado ML — transformando vídeo em um ativo econômico rastreável, não um custo afundado.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:25:O criador faceless brasileiro (canais de curiosidades, finanças, motivação, nichos de produto) opera hoje um **pipeline manual fragmentado**: rascunha roteiro no ChatGPT, gera imagens em uma ferramenta, narra em ElevenLabs (cota em USD), monta legendas e cortes no CapCut, exporta, e republica manualmente em TikTok/Reels/Shorts. Cada vídeo consome 1–3 horas de trabalho operacional repetitivo e **não acumula nenhum aprendizado** — o próximo vídeo recomeça do zero. A agência/operador que serve vários clientes multiplica esse caos por N contas, com credenciais misturadas, sem atribuição de custo por cliente e sem consistência visual entre frames. Ferramentas de avatar (HeyGen/Synthesia) resolvem parte do problema mas cobram em dólar, travam o criador num jardim murado, e não há caminho para **monetizar o conteúdo gerado** (nenhum link de afiliado nativo, nenhuma atribuição de receita). Editar vídeo "como código" (Remotion/HyperFrames) é poderoso e determinístico, mas exige um dev rodando um servidor local — inacessível ao criador e inseguro para multi-tenant (HTML arbitrário no Chrome headless).
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:31:- **Technology gap:** as peças baratas/livres (LTX no HF ZeroGPU, Pollinations, VoxCPM, Remotion, FFmpeg, HyperFrames) existem mas vivem **isoladas em redes Docker e portas diferentes** (faceless studio em `n8n_default`; vision-QA/chroma do MCORCH em `constellation-orchestra_mcorch-sovereign-net`), sem ponte, sem auth unificada e sem billing. Ninguém as costurou num produto soberano com identidade per-tenant.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:39:Um criador logado no MCORCH escolhe um produto (ou tema), aciona o **Faceless Studio**, e em minutos recebe um vídeo vertical pronto — roteiro dirigido por IA, voz clonada, legendas/HUD, movimento real (image-to-video), QA aprovado por um olho criativo VLM e link de afiliado ML embutido — tudo debitado de forma transparente em mcoCoins do seu plano, com o vídeo persistido como asset real e uma observação inserida na malha de conhecimento. O operador de agência abre o **HyperFrames Editor** embedado em `/dashboard/canvas/video`, monta um vídeo data-driven com timeline/preview ao vivo, e renderiza um MP4 determinístico — sem rodar servidor, sem expor credenciais, com cada render sandboxed. Sucesso de mercado = o criador produz **mais vídeos, mais consistentes, mais baratos, e monetizados**, e a agência atribui custo e receita por cliente — algo que nenhum SaaS de avatar entrega.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:48:| Secondary | Operadores/agências de social media que produzem vídeo para múltiplos clientes e precisam de edição programática determinística + atribuição de custo per-cliente | ~50k micro-agências/freelancers BR | Medium | Média — exige onboarding multi-tenant (BYOK por cliente) + isolamento de render |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:89:| MR-VS-005 | Cobrança por render via mcoCoins atômico (RPC), 402 em saldo insuficiente, custo calibrado pelo modelo 4×-floor | Critical | Sustentabilidade econômica; vídeo é a operação cara; sem mint/drain client-side | R2 (mcoCoins gatekeeper) |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:107:| Render Activation | Vídeos renderizados com sucesso por tenant ativo / mês | ≥ 8 vídeos | ≥ 20 vídeos | `mcorch_nodes` observation nodes de render + ledger de débito |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:109:| Monetization Attach-rate | % de vídeos com link afiliado ML embutido + ≥1 clique atribuído | ≥ 40% | ≥ 65% | `affiliate_links.content_id` + click ledger in-system |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:21:│  src/pages/VideoStudioPage.tsx          (rota /dashboard/canvas/video)          │
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:46:└──────────────────────────────────┘        │  studio-dashboard (127.0.0.1:8095 ops)  │
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:71:**Decisão:** o cérebro do Faceless Studio é o workflow n8n **já existente** `e7e3beeb58f7411a` (container `n8n-n8n-1`, imagem `n8n-ffmpeg`), hoje `active:false`. Ele é **ativado e instrumentado**, não reescrito (PRD §4 Won't Have; assumption do BRD §7). O `docker-compose.yml` do studio sobe apenas `remotion-render` + `studio-dashboard`, **attachando a recursos n8n EXTERNOS** (network `n8n_default` + volume `n8n_n8n_assets`).
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:75:2. **Timeouts matam a rota Edge.** O render faceless é trabalho de minutos (multi-leg). Repetindo a lição do orchestrate-async (`docs/processes/orchestrate-async-pipeline.md`): a edge function NÃO faz o render — ela valida JWT, resolve BYOK, debita, enfileira (`video_renders` em `queued`) e retorna 202; o worker n8n executa async; o cliente faz poll (`video-render-poll`). Zero wall-clock de Edge no caminho quente.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:136:| Studio ops UI | `studio-dashboard` (`127.0.0.1:8095`) | Operação/observabilidade headless do studio | (ops) |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:199: │──/dashboard/canvas/video──────────────────▶│ (rota ANTES de canvas/:id — FR-VS-022)           │
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:224: │                            action:'Configure suas credenciais em /dashboard/settings' }
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:350:| mcoCoins deduction | Bypass client-side / mint / drain | Tampering | **Critical** | `deduct_mco_coins` RPC server-side ONLY; nunca client-side; refund crédito-positivo idempotente (R2 · FR-VS-009/011) |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:373:-- RESTRICTIVE no-delete (financeiro/auditável): clientes não apagam render (refund/ledger).
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:374:CREATE POLICY "video_renders_no_client_delete"
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:442:| `studio-dashboard` (`127.0.0.1:8095`) | Ops/observabilidade headless | Sobe via `docker compose up -d --build` (recria 2 containers ad-hoc — downtime breve) |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:478:-- (RLS policies de §5.2: select_own · insert_own · RESTRICTIVE no_client_delete)
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:523:| OTD-VS-005 | **HyperFrames Studio mode** (dev server `npx preview` sem modo produção/host/auth documentado) | **Native React embed** (`@hyperframes/studio` componentes — herda sessão MCORCH) | Served build endurecido (build estático servido com auth proxy) | iframe ao dev server (rejeitado) | **A (escolhido)** — embed nativo em `/dashboard/canvas/video` herda auth R3 sem postMessage cross-origin; rota ANTES de `canvas/:id` (FR-VS-022) | Sovereign |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/05-sdd.md:525:| OTD-VS-007 | **mcoCoins cost calibration** do faceless render (multi-leg: Gemini + LTX + Remotion + FFmpeg) | Cravar ~125 provisório agora (paridade canvas video DoP) | Medir 1 render real no 1º run pago e calibrar 4×-floor antes de cravar | — | **B** — provisório ~125 (faceless) / ~12 (HyperFrames) no espelhamento triplo; medir custo real (BYOK Gemini ~free + LTX ZeroGPU ~free + compute Remotion/FFmpeg) no 1º render pago e fechar a constante (G4 do `mcoin-cost-calibration.md`) | Engineering + Sovereign |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:15:Este documento especifica os requisitos funcionais e não-funcionais do `video-studio` — o módulo de produção de vídeo do MCORCH entregue como **dois sub-sistemas criativos isolados** governados pelo cockpit soberano: **(A) FACELESS STUDIO** (geração autônoma E2E sobre o workflow n8n existente `e7e3beeb58f7411a`) e **(B) HYPERFRAMES EDITOR** (edição programática HTML→MP4 determinística, embedada nativamente em `/dashboard/canvas/video`). Deriva do PRD `03-prd.md` e alimenta diretamente o SDD `05-sdd.md`.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:43:| FR-VS-002 | Auth gate — HyperFrames editor | A rota `/dashboard/canvas/video` é protegida por `DashboardLayout`/`ProtectedRoute`; sessão ausente redireciona para `/auth`; a edge function `video-hyperframes-render` valida JWT antes do render. | Critical | PR-VS-002, PR-VS-009 | UI/EdgeFunction | AT-VS-002 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:51:| FR-VS-005 | Per-user provider resolution (fail-closed) | Toda leg que usa provider externo (Gemini director/QA, OCR, VLM, image) resolve a credencial por `user_id = auth.uid()` em `decrypted_user_api_keys` (VIEW Vault mascarada); se ausente → HTTP 402 estruturado `{ error: "<service>_not_configured", action: "Configure suas credenciais em /dashboard/settings" }`. Zero `Deno.env.get('<SERVICE>_API_KEY')` em path user-facing. | Critical | PR-VS-003 | EdgeFunction/Container | AT-VS-005 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:53:| FR-VS-007 | BYOK isolation — open-design (re-arquitetura) | O open-design (`od` cliente fino → daemon compartilhado) DEVE isolar provider por tenant por uma das vias OTD-VS-002 (daemon per-job efêmero / `od` stateless / container por tenant); fechar o single-tenant `/app/.od/media-config.json` global. 2 tenants com providers distintos não compartilham config. | High | PR-VS-013 | Container | AT-VS-013 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:60:| FR-VS-009 | Atomic deduct — faceless render | `video-faceless-render` debita `VIDEO_FACELESS_RENDER` mco via `deduct_mco_coins(p_user_id, p_amount, ...)` RPC ANTES de qualquer leg de provider; saldo insuficiente → HTTP 402 (nenhuma leg roda, nada debitado). Nunca client-side. | Critical | PR-VS-004, PR-VS-005 | EdgeFunction | AT-VS-009 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:89:| FR-VS-023 | "Video" button na TopBar | Um botão "Video" senta ao lado do botão "Pipeline" em `src/components/canvas/TopBar.tsx`; clicar navega para `/dashboard/canvas/video`. | High | PR-VS-009 | UI | AT-VS-023 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/04-frd.md:296:- Integration / smoke (zero-cost gates): `scripts/qa/smoke-video-faceless.ts`, `scripts/qa/smoke-video-hyperframes.ts`, `scripts/qa/smoke-video-auth.ts`, `scripts/qa/smoke-video-byok.ts`
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:18:| PROC-VS-002 | Editar no HyperFrames + render determinístico | `human-in-loop` | Abrir `/dashboard/canvas/video` + clicar "Render" | User (Marina) | FR-VS-021/022/023/024/025/010 | `video_templates`, `video_renders`, `video_assets` | render wall-clock p95 <90s |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:89: /dashboard/canvas/video ───────────────────▶ (rota ANTES de canvas/:id — FR-VS-022; ProtectedRoute → /auth se sem sessão R3)
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:125: │                           action:'Configure suas credenciais em /dashboard/settings' } ⛔
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:243:| `user_id` | Webhook body (server-trusted, nunca do body do cliente) | → | `p_user_id` | refund RPC + nó da malha |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:253:| Sequência | (1) copiar `n8n/scripts/ltx.js` + `composite.sh` para `/home/node/.n8n/assets/` no container `n8n-n8n-1`; (2) `bash scripts/gen-sfx.sh` → roda `docker exec n8n-n8n-1` ffmpeg lavfi p/ construir a biblioteca de SFX procedural; (3) `docker compose up -d --build` sobe `remotion-render` + `studio-dashboard` (recria os 2 containers ad-hoc — downtime breve; NÃO toca `login.mcorch.com`, fora do Docker) |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:274:| Canvas (Visual Orchestrator) | botão "Video" na TopBar + rota `/dashboard/canvas/video` | O editor HyperFrames vive como uma aba do Canvas (FR-VS-022/023); reusa o layout do cockpit sem novo Zustand store (SDD §2.5). |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/07-process-flow.md:276:| `deduct_mco_coins` / refund | reuso (billing SSOT) | nenhuma dedução client-side; ponto único de cobrança no entrypoint da edge fn. |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md:14:O `video-studio` converte as Market Requirements em compromissos de negócio executáveis sob as **cinco regras inquebráveis MCORCH** (Diretiva Sovereign 2026-06-21): **R1 BYOK per-user**, **R2 mcoCoins gatekeeper atômico**, **R3 auth MCORCH nos apps isolados**, **R4 conexão à malha**, **R5 ponte de rede Docker**. O módulo entrega dois motores — **Faceless Studio** (geração autônoma E2E sobre o workflow n8n existente) e **HyperFrames Editor** (edição programática HTML→MP4 embedada nativamente em `/dashboard/canvas/video`) — ambos como apps isolados governados pelo cockpit soberano. O modelo econômico é híbrido: débito de mcoCoins por render (operação cara, calibrada 4×-floor) **mais** monetização via afiliado Mercado Livre embutido no conteúdo. Cada render bem-sucedido vira observação na malha; cada falha vira telemetria. A viabilidade depende de destravar três blocos materiais hoje abertos — **ponte de rede Docker (R5)**, **BYOK per-user no open-design de daemon compartilhado (OTD-VS-002)** e **provisionamento de identidade/entrega (PAT/JWT do studio + Telegram OTD-VS-003)** — sem os quais a fiação vision-QA/chroma/entrega é prosa, não engenharia.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md:23:| BO-VS-002 | Embedar o editor programático HyperFrames no cockpit, multi-tenant e sandboxed | Rota nativa `/dashboard/canvas/video` (React embed, não iframe a dev server) renderiza HTML→MP4 determinístico com render isolado per-tenant | ≥ 1 MP4 determinístico renderizado por tenant via sandbox sem credencial compartilhada no ambiente de render | Pacote `@hyperframes/studio` exporta componentes React p/ embed nativo; porta 3002 livre no host | Núcleo do segmento secundário/agência (MR-VS-002) | v1.0 — após sandbox per-render (OTD-VS-006) selado |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md:25:| BO-VS-004 | Monetizar o conteúdo gerado com afiliado ML e atribuição per-tenant | Link de afiliado Mercado Livre embutido no conteúdo do vídeo + atribuição de receita/clique por tenant | Attach-rate ≥ 65% de vídeos com link afiliado + ≥1 clique atribuído (12m) | Arquitetura afiliado ML + click ledger in-system já existem no MCORCH | Receita híbrida; diferencial vs SaaS de avatar (MR-VS-007) | v1.0 |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md:40:| SH-VS-007 | Providers externos (Gemini, Pollinations, LTX HF, VoxCPM, Mercado Livre) | Low | Medium | On license/quota change | Termos/dashboards de cada provider |
> ```

## 🤖 Claude *(01:26:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"KPI-VS.*agency\\|activat.*agency\\|segmento ag\u00eancia\" /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/ --include=\"*.md\""
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/01-mrd.md:131:| MR-VS-002 | BR-??? | Editor programático embedado → objetivo do segmento agência |
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/03-prd.md:146:**Condition:** segmento agência ativado em escala + demanda de lote/publicação direta comprovada; cada item entra após métrica de uso do v1.0.
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-studio/02-brd.md:93:| 12-month ROI | ~ +18% (conservador; depende da ativação do segmento agência em v1.0) |
> ```

## 🤖 Claude *(01:26:52)*

Based on my thorough review of the BoK documents, I can now provide my final analysis. Let me call StructuredOutput with my findings:

## 🤖 Claude *(01:27:20)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "dimension": "monetization-leverage",
  "gaps_confirmed": [
    "Agency/Enterprise plan-tier pricing specification undefined \u2014 no feature gates (seats, quotas, API limits) tied to plan tier; mcoCoins table shows plan-volume mappings (Starter/Pro/Ent) but no plan_tier.features access control matrix",
    "Wholesale mcoCoins and resale margin model absent \u2014 no bulk discount mechanism for agencies to resale to clients; no revenue split percentage defined between MCORCH and agency tenant; no margin transparency or agency ROI calculation",
    "Affiliate revenue split undefined at contract level \u2014 BR-VS-007 states 'atribui\u00e7\u00e3o per-tenant' (click ledger in-system) but neither affiliate_links schema nor FRD/PRD specifies % split between tenant/agency vs MCORCH; blocking agency business case math",
    "Agency ROI model and unit economics missing \u2014 BRD \u00a75.3 shows MCORCH's 18% ROI depending on 'ativa\u00e7\u00e3o do segmento ag\u00eancia em v1.0' but zero agency-side cost-per-client or revenue-per-client calculation; agency payback/margin undefined",
    "Seat-based and role-based access control (RBAC) not specified \u2014 Stakeholder SH-VS-003 (agency operator) exists but FRD has no FR for team seats, roles (owner/billing-admin/editor), or permission scopes; PR-VS-013 mentions BYOK per-user open-design isolation but not team access patterns",
    "Multi-client rollup dashboard absent \u2014 PRD/FRD define per-tenant/per-render cost tracking but no feature for agencies to visualize aggregate per-client cost, revenue, affiliate split, or team usage; cost attribution exists at render level (video_renders.charged_mco) but no aggregation layer",
    "Affiliate ledger reconciliation schema undefined \u2014 no transaction schema for tracking click-source attribution, revenue settlement frequency, or monthly reconciliation between MCORCH and agency; affiliate_links table exists (content_id) but no reconciliation audit trail or settlement model",
    "OTD-VS-002 (Per-user BYOK open-design) blocks multi-client agency onboarding \u2014 explicitly marked 'open status with no decision timeline' in BRD line 117; prevents v1.0 agency activation; documented as 'single-tenant EXPLICIT until closed' (BRD line 143)",
    "Agency activation KPI missing \u2014 BRD \u00a72 lists BO-VS-001..005 business objectives but zero KPI for agency segment health (attach rate, volume, retention, multi-client adoption); Quality Metrics \u00a72 has 18 KPIs (KPI-VS-001..018) but no KPI-VS-XXX specifically for agency leverage or multi-tenant health"
  ],
  "false_positives": [
    "Claim: 'NO wholesale mcoCoins or resale margin model' \u2014 PARTIALLY MITIGATED: BRD \u00a76 shows mcoCoins pricing with plan-tier mappings (Starter 500/~4 vids, Pro 2000/~16, Ent 10k/~80 faceless renders); however this is consumption-based (tenant quota in plan), not a wholesale/resale discount model for agencies buying in bulk \u2014 gap persists as framed",
    "Claim: 'NO affiliate revenue split defined' \u2014 CONFIRMED but SCOPED: Data model \u00a72.6 and FRD \u00a74.2 detail affiliate_links table with content_id NON-NULL (ligado ao asset), and click ledger in-system already exist (reuse per BRD Assumptions); however the ledger tracks clicks, NOT revenue % split \u2014 gap is accurate",
    "Claim: 'Affiliate ledger reconciliation undefined' \u2014 CORRECT but QUALIFIED: BRD \u00a75.2 revenue stream shows 'Afiliado Mercado Livre \u00b7 Comiss\u00e3o sobre convers\u00e3o atribu\u00edda \u00b7 ~R$1.2k/m\u00eas' and BRD line 131 Assumption states 'click ledger in-system de afiliado ML (OTD-ML-CLICKS, fechado)'; the click ledger EXISTS but affiliate reconciliation (settlement to agency, % split) is NOT in the BoK \u2014 gap confirmed",
    "Claim: 'Zero agency activation KPI' \u2014 CONFIRMED but SCOPED: BRD \u00a75.3 explicitly says 'depende da ativa\u00e7\u00e3o do segmento ag\u00eancia em v1.0' and lists BO-VS-001..005 as business objectives; Quality Metrics \u00a72 defines 18 KPIs for product quality but KPI-VS-009 'BYOK-configured rate' is closest to adoption (not agency-specific); no KPI-VS-agency-attach or KPI-VS-agency-volume \u2014 gap is real"
  ],
  "note": "STRATEGIC FINDING: The BoK is **MCORCH-centric** (single-creator + platform economics) NOT **AGENCY-CENTRIC** (multi-client portfolio economics). Gaps 1\u20139 cluster into three blocks: (A) **Commercial tiers** \u2014 plan features/seats undefined, wholesale/resale opaque (gaps 1\u20132); (B) **Agency operations** \u2014 no team RBAC, no multi-client dashboard, no agency ROI math (gaps 5\u20136, 9); (C) **Financial transparency** \u2014 affiliate split %, settlement model, agency unit economics missing (gaps 3\u20134, 7). Gap 8 (OTD-VS-002) is architectural blocker, not a doc gap \u2014 it's open for decision. **Verdict per adversarial brief:** The BoK captures L\u00e9o (primary, faceless) and Marina (secondary, editor) PERSONAS but NOT the **BUSINESS MODEL** by which Marina's agency (or a portfolio agency) makes money, allocates costs, or integrates with MCORCH financially. This is load-bearing for \"AGENCY LEVERAGE\" claim in strategic lens. Recommend: Defer agency monetization (gaps 1\u20137) to v1.0+ or explicitly scope as \"single-creator-first, agency playbook follows.\""
}
```

> **Tool Result (StructuredOutput)** - ✅ Success
>
> ```
> Structured output provided successfully
> ```

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-22 - agent-ad463d72ad94664fa]]
> * **Próxima Sessão**: [[2026-06-22 - agent-ad6f57e218901236b]]
%% --- TIMELINE END --- %%

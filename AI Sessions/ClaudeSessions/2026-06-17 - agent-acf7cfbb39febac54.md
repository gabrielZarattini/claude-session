# Session agent-acf7cfbb39febac54
**Date:** 2026-06-17 | **Session ID:** `agent-acf7cfbb39febac54`

---

## 👤 User *(21:09:01)*

Você é um crítico ADVERSARIAL da suíte BoK viral-autopilot em /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot (9 docs: 00-index,01-mrd,02-brd,03-prd,04-frd,05-sdd,06-data-model,07-process-flow,08-quality-metrics). Leia os arquivos relevantes (Read/Grep) e CACE INCONSISTÊNCIAS — seu trabalho é reprovar, não elogiar. Reporte findings com severidade e fix concreto (doc + seção). Default cético: se algo está ambíguo ou falta, é finding. Não invente conteúdo; cite o que leu.

DIMENSÃO: Rastreabilidade. Construa a cadeia MR-VA-NNN → BR-VA-NNN → PR-VA-NNN → FR-VA-NNN → (tabela|edge fn|cron|processo). Assert:
- Todo MR (8) rastreia ≥1 BR; todo BR (8) ≥1 PR; todo PR ≥1 FR; todo FR (18) ≥1 PR e ≥1 artefato no SDD/data-model/process-flow.
- Sem ID órfão (aparece numa matriz mas nunca definido, ou definido mas nunca rastreado downstream).
- As matrizes de rastreabilidade nos 4 docs (01,02,03,04) são MUTUAMENTE CONSISTENTES (ex.: PR-VA-008 image aparece como Must no PRD e tem FR? FR-VA-013 marcado 'Should (MVP)' — é coerente com MVP=texto+imagem?).
- Os 5 PROC do 07 cobrem todos os FR críticos; os 2 crons existem no SDD e no process-flow.
Liste cada quebra de cadeia como finding.

## 🤖 Claude *(21:09:04)*

I'll start by reading all the relevant BoK docs to build the traceability chains and hunt for inconsistencies.

## 🤖 Claude *(21:09:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/",
  "description": "List viral-autopilot BoK docs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 140
> drwxrwxr-x  2 ubuntu ubuntu  4096 Jun 17 18:07 .
> drwxrwxr-x 23 ubuntu ubuntu  4096 Jun 17 17:57 ..
> -rw-rw-r--  1 ubuntu ubuntu  7205 Jun 17 17:58 00-index.md
> -rw-rw-r--  1 ubuntu ubuntu 10695 Jun 17 17:59 01-mrd.md
> -rw-rw-r--  1 ubuntu ubuntu 12631 Jun 17 18:00 02-brd.md
> -rw-rw-r--  1 ubuntu ubuntu 12506 Jun 17 18:01 03-prd.md
> -rw-rw-r--  1 ubuntu ubuntu 13570 Jun 17 18:03 04-frd.md
> -rw-rw-r--  1 ubuntu ubuntu 21154 Jun 17 18:04 05-sdd.md
> -rw-rw-r--  1 ubuntu ubuntu 11703 Jun 17 18:05 06-data-model.md
> -rw-rw-r--  1 ubuntu ubuntu  9953 Jun 17 18:06 07-process-flow.md
> -rw-rw-r--  1 ubuntu ubuntu 12334 Jun 17 18:07 08-quality-metrics.md
> ```

## 🤖 Claude *(21:09:09)*

Let me read all the docs in parallel to build the traceability chains.

## 🤖 Claude *(21:09:10)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/01-mrd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# MRD — Market Requirements Document
> 2	
> 3	**Project:** viral-autopilot  
> 4	**Version:** v0.1 | **Date:** 2026-06-17  
> 5	**BoK Applied:** BABOK v3 (Strategy Analysis + Elicitation & Collaboration)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Executive Summary
> 11	
> 12	Criadores e afiliados que monetizam via Mercado Livre enfrentam um trabalho braçal insustentável: para cada produto precisam pesquisar tendência, escrever copy, formatar por rede, agendar, publicar e — quase nunca — medir o que funcionou para ajustar o próximo post. O resultado é volume baixo, inconsistência e cegueira de desempenho. O **viral-autopilot** é o piloto-automático de conteúdo viral monetizado do MCORCH: a partir de um produto-alvo, gera criativos prontos para publicação em múltiplas redes, agenda-os (tudo de uma vez ou em lotes recorrentes a cada N dias) e — o diferencial central — **fecha o loop**: a cada ciclo ingere o desempenho real do ciclo anterior (cliques de afiliado, engajamento orgânico, receita confirmada) e realimenta os próximos criativos. A janela é agora: o custo marginal de gerar texto via LLM caiu a quase zero, as APIs de publicação social estão maduras, e o MCORCH já tem a infraestrutura de receita ML per-user pronta — falta apenas o cérebro que orquestra o ciclo e aprende.
> 13	
> 14	---
> 15	
> 16	## 2. Market Problem Statement
> 17	
> 18	### 2.1 Current State
> 19	
> 20	O afiliado/criador faz hoje, **manualmente e sem memória de desempenho**:
> 21	1. Escolhe um produto (intuição, não dado de comissão/tendência).
> 22	2. Escreve a copy à mão ou pede a um LLM genérico — sem ângulo viral, sem amarração ao produto.
> 23	3. Adapta para cada rede, cola o link de afiliado manualmente, agenda um por um.
> 24	4. Publica e **não mede** — não há leitura de qual criativo converteu para ajustar o próximo.
> 25	
> 26	Mesmo dentro do MCORCH, a auditoria material de 2026-06-17 provou que o pipeline atual: gera só **texto** (mídia órfã, `generate-image`/`generate-video` com zero callers), monetiza **só o artigo** com catálogo **hardcoded de 3 SKUs por regex** (`_shared/affiliate.ts`), **não tem recorrência** (só 2 pg_cron, nenhum re-gera conteúdo) e tem o loop de melhoria **aberto em 3 quebras** (`campaign_metrics` sem writer, `optimization_policy` nunca lida por gerador, `self-optimize` sem cron).
> 27	
> 28	### 2.2 Root Cause Analysis
> 29	
> 30	- **Gap de processo:** ninguém desenhou o ciclo fechado geração→publicação→análise→re-geração — cada peça existe isolada (ilhas: `fetch-trends`, `self-optimize`, `vm_affiliate_products`).
> 31	- **Gap de tecnologia:** não há entidade de "cadência" nem coletor de desempenho por criativo; o agendamento é offset fixo hardcoded.
> 32	- **Gap de mercado:** ferramentas de agendamento (Buffer, Hootsuite) publicam mas não geram nem aprendem; geradores de IA (Jasper, Copy.ai) geram mas não agendam, não monetizam ML e não fecham loop. Ninguém une os quatro no mercado BR de afiliados ML.
> 33	
> 34	### 2.3 Desired State
> 35	
> 36	Um operador define um **plano de autopilot** (produtos-alvo, redes, modo: tudo-de-uma-vez ou a-cada-N-dias) e o sistema, sozinho e dentro de um teto de custo, **gera criativos virais product-aware monetizados, publica, mede e melhora a cada ciclo** — com ROI visível por peça de conteúdo e tudo escopado por tenant (credenciais e carteira do próprio operador).
> 37	
> 38	---
> 39	
> 40	## 3. Target Market Segments
> 41	
> 42	| Segment | Description | Size Estimate | Urgency | Accessibility |
> 43	|---------|-------------|---------------|---------|---------------|
> 44	| Primary | Afiliados/criadores BR do Mercado Livre que querem escalar conteúdo monetizado sem equipe | ~centenas de milhares de afiliados ML BR ativos | High | Alta — Usuário Zero (Gabriel) é o piloto; onboarding via plano + BYOK |
> 45	| Secondary | Pequenas agências/lojistas que gerenciam várias contas de produto e precisam de cadência + ROI | dezenas de milhares de PMEs/agências | Medium | Média — exige multi-conta e relatório de ROI |
> 46	
> 47	### 3.1 TAM / SAM / SOM
> 48	
> 49	| Metric | Value | Basis |
> 50	|--------|-------|-------|
> 51	| TAM | ~R$ 50–80 M/ano (estimado) | Programa de afiliados ML no Brasil + criadores que monetizam links; proxy: ferramentas de social scheduling + AI copy no segmento BR |
> 52	| SAM | ~R$ 8–12 M/ano (estimado) | Afiliados/criadores que pagariam por automação de conteúdo+ROI (plano Pro/Enterprise MCORCH) |
> 53	| SOM (12m) | ~R$ 0,5–1,5 M/ano (estimado) | Usuário Zero + primeiros 50–200 tenants pagantes na fase Commercial |
> 54	
> 55	> Estimativas de ordem-de-grandeza para priorização (BABOK Strategy Analysis), não pesquisa de mercado primária. Refinar quando o 1º tenant externo for onboardado.
> 56	
> 57	---
> 58	
> 59	## 4. Competitive Landscape
> 60	
> 61	| Competitor | Positioning | Strengths | Weaknesses | Our Differentiation |
> 62	|------------|-------------|-----------|------------|---------------------|
> 63	| Buffer / Hootsuite / Metricool | Agendamento e analytics de social | Maduros, multi-rede, analytics ricos | Não geram conteúdo, não monetizam afiliado, não fecham loop de melhoria | Geramos + monetizamos ML + **loop auto-melhorável**, não só agendamos |
> 64	| Jasper / Copy.ai / ChatGPT | Geração de copy por IA | Boa qualidade de texto | Sem agendamento, sem ML, sem medição/aprendizado, product-unaware | Product-aware + cadência + atribuição de receita por criativo |
> 65	| Linktree / Beacons + planilha manual | Bio-link + tracking manual de cliques | Simples, barato | Zero geração/automação; medição manual; sem aprendizado | Click ledger automático + ROI por peça + re-geração informada |
> 66	
> 67	---
> 68	
> 69	## 5. Market Opportunity & Timing
> 70	
> 71	- **Custo marginal de geração ≈ 0:** LLMs de texto (Groq/OpenRouter, BYOK) tornam viável gerar dezenas de criativos por ciclo a custo desprezível.
> 72	- **APIs de publicação maduras:** LinkedIn publica hoje no MCORCH; WordPress e X já no pipeline; Meta/IG já tem `publish-meta`.
> 73	- **Infra de receita ML pronta:** `affiliate_config` per-user, click ledger atômico, `handle-ml-postback` HMAC idempotente — já construídos e provados na auditoria. O diferencial só precisa do **orquestrador do ciclo + loop de aprendizado**.
> 74	- **Vácuo competitivo:** nenhuma ferramenta une geração+agendamento+monetização-ML+aprendizado para o afiliado BR.
> 75	
> 76	---
> 77	
> 78	## 6. Market Requirements
> 79	
> 80	> Priority: **Critical** (must have at launch) | **High** | **Medium** | **Low**
> 81	
> 82	| ID | Market Requirement | Priority | Rationale | Source |
> 83	|----|-------------------|----------|-----------|--------|
> 84	| MR-VA-001 | Geração automática de conteúdo viral para redes sociais a partir de um produto-alvo, sem operação manual por post | Critical | R1 — núcleo do valor; hoje pipeline gera texto genérico product-unaware | Diretiva Sovereign R1 |
> 85	| MR-VA-002 | Cadência configurável: disparo único ("tudo de uma vez") OU recorrente a cada N dias (default 3), por tenant/plano | Critical | R2 — recorrência inexistente hoje; é o que torna "autônomo" | Diretiva Sovereign R2 |
> 86	| MR-VA-003 | Loop auto-melhorável: o desempenho do ciclo anterior realimenta materialmente a geração do próximo | Critical | R3 — requisito mais valorizado e mais ausente (loop aberto em 3 quebras) | Diretiva Sovereign R3 |
> 87	| MR-VA-004 | Monetização nativa: todo criativo amarrado a produto ML com link de afiliado per-user em TODO formato | Critical | R4 — hoje monetiza só o artigo, por regex, 3 SKUs hardcoded | Diretiva Sovereign R4 |
> 88	| MR-VA-005 | Atribuição de receita e desempenho por criativo (ROI por peça de conteúdo) | High | Sem ROI por peça não há aprendizado nem prova de valor | Auditoria (R3 signal) |
> 89	| MR-VA-006 | Controle de custo do loop autônomo: teto de gasto por ciclo + kill-switch quando saldo baixo | Critical | Loop autônomo recorrente pode drenar mcoCoins silenciosamente | Restrição Sovereign (custo) |
> 90	| MR-VA-007 | Multi-tenancy estrita: cada operador usa suas próprias credenciais (BYOK) e carteira | High | API Tenancy Model per-user (diretiva 2026-05-19); isolamento de receita/quota | CLAUDE.md API Tenancy |
> 91	| MR-VA-008 | Seleção de produto e ângulo a partir de sinal viral real (trends + métricas de comissão) | Medium | `fetch-trends`/`vm_affiliate_products` existem mas estão desconectados da geração | Auditoria (R4) |
> 92	
> 93	---
> 94	
> 95	## 7. Success Metrics (Market-Level KPIs)
> 96	
> 97	| KPI | Definition | Target (6-month) | Target (12-month) | Measurement |
> 98	|-----|-----------|------------------|-------------------|-------------|
> 99	| Conteúdo autônomo publicado | nº de criativos publicados por autopilot sem ação manual | ≥ 90% dos posts do tenant | ≥ 95% | `scheduled_posts` com `cycle_id` not null |
> 100	| Lift viral ciclo-a-ciclo | engajamento médio do ciclo N+1 ÷ ciclo N | ≥ 1.10× após 3 ciclos | ≥ 1.25× | `creative_metrics` agregado por `cycle_id` |
> 101	| Receita ML atribuída | R$ de comissão creditada e atribuída a criativos do autopilot | > R$ 0 (Usuário Zero) | crescente MoM | `affiliate_links.revenue_cents` por `content_variant_id` |
> 102	| % criativos monetizados | criativos com link ML válido ÷ criativos gerados | 100% (todo formato) | 100% | `creative_metrics` ∩ `affiliate_links` |
> 103	| NPS | Net Promoter Score dos operadores | ≥ 40 | ≥ 55 | Survey in-app |
> 104	
> 105	---
> 106	
> 107	## 8. Regulatory & Compliance Context
> 108	
> 109	| Regulation | Applicability | Key Constraint | Compliance Owner |
> 110	|------------|---------------|----------------|-----------------|
> 111	| LGPD | Sim | PII residual em métricas de engajamento (não coletar dados pessoais de quem engaja além de agregados); direito ao apagamento por tenant | Engineering |
> 112	| ToS Mercado Livre / Mercado Pago | Sim | Disclosure de afiliado; uso correto de `matt_word`/`matt_tool`; postback de comissão | Engineering + Sovereign |
> 113	| ToS Redes Sociais (LinkedIn/X/Meta) | Sim | Limites de automação/rate, rotulagem de conteúdo, sem spam; respeitar quotas de API tier | Engineering |
> 114	| Publicidade (CONAR/identificação de publi) | Sim | Conteúdo monetizado deve sinalizar caráter publicitário/afiliado | Sovereign |
> 115	
> 116	---
> 117	
> 118	## 9. Traceability Matrix Stub
> 119	
> 120	| MR ID | → BR ID | Rationale |
> 121	|-------|---------|-----------|
> 122	| MR-VA-001 | BR-VA-001 | Geração product-aware multi-formato |
> 123	| MR-VA-002 | BR-VA-002 | Plano de cadência + cron por-tenant |
> 124	| MR-VA-003 | BR-VA-003 | Coletor + analisador + reinjeção |
> 125	| MR-VA-004 | BR-VA-004 | Monetização em todo formato com `content_variant_id` |
> 126	| MR-VA-005 | BR-VA-005 | Métricas por criativo + atribuição postback |
> 127	| MR-VA-006 | BR-VA-006 | Orçamento de ciclo + kill-switch atômico |
> 128	| MR-VA-007 | BR-VA-007 | Resolução per-user (affiliate_config, BYOK) |
> 129	| MR-VA-008 | BR-VA-008 | Seleção por comissão+trend (3 SKUs semente) |
> 130	
> 131	---
> 132	
> 133	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 134	
> ```

## 🤖 Claude *(21:09:10)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/02-brd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# BRD — Business Requirements Document
> 2	
> 3	**Project:** viral-autopilot  
> 4	**Version:** v0.1 | **Date:** 2026-06-17  
> 5	**BoK Applied:** BABOK v3 (Requirements Analysis & Design Definition)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Executive Summary
> 11	
> 12	O `viral-autopilot` converte a infraestrutura de geração e de receita ML já existente no MCORCH em um **motor de receita autônomo e auto-melhorável**. O objetivo de negócio é triplo: (1) **escalar volume** de conteúdo monetizado sem trabalho humano por post; (2) **aumentar a conversão** ao tornar cada criativo product-aware e informado pelo desempenho passado; (3) **proteger a margem** com tetos de custo e atribuição de ROI por peça. O retorno é direto — comissão de afiliado ML — mas protegido por um modelo de custo em mcoCoins que garante que o loop autônomo nunca opere no prejuízo silencioso.
> 13	
> 14	---
> 15	
> 16	## 2. Business Objectives (SMART)
> 17	
> 18	| ID | Objective | Specific | Measurable | Achievable | Relevant | Time-bound |
> 19	|----|-----------|----------|------------|------------|----------|------------|
> 20	| BO-001 | Automatizar a geração+publicação monetizada | Operador define 1 plano e o sistema produz/publica criativos product-aware sem ação por post | ≥ 90% dos posts via autopilot (sem toque manual) | Pipeline de texto já vivo; falta orquestrador | Escala receita sem escalar trabalho | MVP até 2026-07-31 |
> 21	| BO-002 | Fechar o loop de melhoria por desempenho | Cada ciclo lê o desempenho do anterior e ajusta os próximos criativos | Lift de engajamento ciclo-a-ciclo ≥ 1.10× após 3 ciclos | `self-optimize` já existe (esqueleto); fechar 3 quebras | É o diferencial do produto | v1.0 até 2026-08-31 |
> 22	| BO-003 | Garantir margem positiva e custo controlado | Todo ciclo respeita teto de mcoCoins e atribui ROI por criativo | 100% dos ciclos com `spend_mco ≤ budget_cap`; ROI por peça visível | Débito atômico `deduct_mco_coins` já existe | Evita o autopilot virar buraco de carteira | MVP até 2026-07-31 |
> 23	| BO-004 | Monetizar todo formato gerado | Artigo + LinkedIn + X saem com link ML válido per-user | 100% dos criativos com `content_variant_id` + link rastreável | `monetizeContent` + `affiliate_config` já existem (só no artigo hoje) | Sem monetização universal não há atribuição nem receita | MVP até 2026-07-31 |
> 24	
> 25	---
> 26	
> 27	## 3. Stakeholder Register
> 28	
> 29	| ID | Role | Interest | Influence | Communication Cadence | Contact |
> 30	|----|------|----------|-----------|----------------------|---------|
> 31	| SH-001 | Sovereign / Maestro | High | High | Continuous | Gabriel Zarattini |
> 32	| SH-002 | Operador/Afiliado (Primary) — Usuário Zero | High | Medium | Por ciclo (dashboard) + NPS mensal | gabrielcall@gmail.com |
> 33	| SH-003 | Mercado Livre / Mercado Pago | Medium | High | Via postback + ToS (assíncrono) | Plataforma externa |
> 34	| SH-004 | Redes sociais (LinkedIn/X/Meta) | Medium | High | Via API + ToS/quotas | Plataformas externas |
> 35	| SH-005 | MCORCH Master Execution Agent (Operator) | High | Medium | Por sessão (handoff) | AIOS |
> 36	
> 37	---
> 38	
> 39	## 4. Business Requirements
> 40	
> 41	> Cada BR rastreia ≥ 1 MR. Custo mcoCoins definido para BR com geração via IA.
> 42	
> 43	| ID | Requirement | MR Traced | Priority | mcoCoins Cost | Acceptance Criteria |
> 44	|----|-------------|-----------|----------|---------------|---------------------|
> 45	| BR-VA-001 | Geração product-aware multi-formato: artigo+post+thread com copy de venda construída em torno de um produto-alvo (id+nome+imagem ML), substituindo os prompts B2B hardcoded por framework de gancho viral | MR-VA-001 | Critical | herda `orchestrate-content` (10 mco/run + sub-steps) | Dado um produto-alvo, os 3 formatos mencionam o produto e contêm link ML válido |
> 46	| BR-VA-002 | Plano de cadência persistido (modo all-at-once vs lote-a-cada-N-dias, default 3) + cron por-tenant que dispara o ciclo sem ação humana | MR-VA-002 | Critical | 0 (orquestração) | Plano com `interval_days=3` dispara automaticamente a cada 3 dias; modo all-at-once gera lote único |
> 47	| BR-VA-003 | Loop fechado: coletar desempenho do ciclo → analisar → reinjetar aprendizados (top hooks/produtos/horários) na geração do próximo ciclo | MR-VA-003 | Critical | 5 mco/análise (LLM, herda `self-optimize`) | Ciclo N+1 recebe no prompt o resumo estruturado do desempenho do ciclo N |
> 48	| BR-VA-004 | Monetização em TODO formato com `content_variant_id` por criativo, honrando o produto-alvo (corrigir param `affiliate_url` dropado) | MR-VA-004 | Critical | 0 (parte da geração) | LinkedIn e Twitter, não só o artigo, saem com link ML rastreável + `content_variant_id` |
> 49	| BR-VA-005 | Métricas por criativo unificadas (cliques afiliado + engajamento orgânico + receita postback) + atribuição de ROI por peça | MR-VA-005 | High | 0 (ingestão) | `creative_metrics` populada por ≥ 1 fonte real; ROIWidget mostra ROI por `content_variant_id` |
> 50	| BR-VA-006 | Orçamento de ciclo (teto mcoCoins) + kill-switch que pausa o plano quando saldo < limiar, ANTES de qualquer deduct | MR-VA-006 | Critical | 0 (guarda) | Ciclo aborta sem cobrar quando `spend projetado > budget_cap` ou `saldo < min`; plano pausado + notificação |
> 51	| BR-VA-007 | Toda credencial externa (ML, redes, LLM) resolvida per-user via `auth.uid()`; sem chave global em fluxo user-facing | MR-VA-007 | High | 0 | Tenant A nunca usa credencial/quota de Tenant B; fail-closed quando não configurado |
> 52	| BR-VA-008 | Seleção de produto por comissão+trend a partir do catálogo (3 SKUs semente agora; caminho de auto-descoberta documentado) | MR-VA-008 | Medium | 0 (seleção) | Plano referencia produtos do catálogo `vm_affiliate_products`; ranking por `commission_value`+`trend_score` disponível |
> 53	
> 54	---
> 55	
> 56	## 5. ROI Model
> 57	
> 58	### 5.1 Cost Estimates
> 59	
> 60	| Cost Item | Type | Monthly Estimate | Annual Estimate |
> 61	|-----------|------|-----------------|----------------|
> 62	| Infraestrutura (Supabase, Docker mesh, pg_cron) | OpEx | ~R$ 0 incremental (reusa stack existente) | ~R$ 0 incremental |
> 63	| Chamadas LLM (texto, BYOK por tenant) | Variable | ~R$ 0–20/tenant (texto é quase free; custo no tenant via BYOK) | — |
> 64	| Geração de imagem (DALL·E/Nano Banana) | Variable | ~$0.04/imagem × volume do ciclo | escala com nº de criativos |
> 65	| Desenvolvimento (inicial — MVP+v1.0) | CapEx | — | ~2–3 sprints de engenharia (interno) |
> 66	
> 67	### 5.2 Revenue Streams
> 68	
> 69	| Stream | Model | Monthly Potential | Notes |
> 70	|--------|-------|-----------------|-------|
> 71	| Comissão de afiliado ML | Transaction (revenue share) | variável — função de volume × CTR × taxa de conversão × comissão | Receita direta; atribuída por `content_variant_id` via postback |
> 72	| Consumo de mcoCoins | Subscription/consumption | 10 mco/run + 5 mco/análise × ciclos | Receita indireta da plataforma; alinha custo ao uso |
> 73	
> 74	### 5.3 Payback Analysis
> 75	
> 76	| Metric | Value |
> 77	|--------|-------|
> 78	| Break-even (months) | Indeterminado até 1º postback real de conversão ML (OTD-VA-007 / OTD-ML-MP-PER-USER) — depende de CTR×conversão observados |
> 79	| 12-month ROI | A medir; meta é receita ML atribuída > custo de mcoCoins do loop por tenant |
> 80	| IRR (estimated) | N/A nesta fase (Usuário Zero pré-Commercial) |
> 81	
> 82	> **Honestidade material (Lei 1):** o payback real só pode ser afirmado após um postback de conversão ML chegar em produção. Hoje a receita atribuível é R$ 0 provados. O ROI Model é projeção, não fato.
> 83	
> 84	---
> 85	
> 86	## 6. mcoCoins Economics
> 87	
> 88	| Operation | Coins/Run | Plan Tier Mapping | Monthly Volume (est.) | Monthly Revenue (est.) |
> 89	|-----------|-----------|-------------------|-----------------------|----------------------|
> 90	| Ciclo de geração (autopilot) | 10 mco/run (herda `orchestrate-content`) + sub-steps | Starter(500) / Pro(2000) / Ent(10k) | função de `interval_days` × nº produtos × redes | consumo de plano |
> 91	| Análise de ciclo (self-optimize) | 5 mco/análise | idem | 1 por ciclo por plano | consumo de plano |
> 92	| Geração de imagem | calibrar via SOP `mcoin-cost-calibration` (modelo 4×-floor) | idem | 1+ por criativo | consumo de plano |
> 93	
> 94	> **Teto obrigatório (BR-VA-006):** cada plano carrega `budget_cap_mco` por ciclo. O ciclo soma o custo projetado (10 + 5 + imagem × nº criativos) e **aborta antes de deduzir** se exceder o teto ou se o saldo cair abaixo do mínimo. Espelha o modelo de caps do `vision-mcp` (per-plano + safety diário).
> 95	
> 96	---
> 97	
> 98	## 7. Constraints & Assumptions
> 99	
> 100	### Constraints
> 101	- **API Tenancy per-user (UNBREAKABLE):** toda credencial externa resolvida via `auth.uid()`; env global só em cron/service-role sem JWT, nunca como caminho primário user-facing.
> 102	- **mcoCoins atômico:** dedução só via `deduct_mco_coins` RPC; nunca client-side; sempre depois do gate de teto.
> 103	- **RLS default-deny** em toda nova tabela; multi-tenant `user_id (+ project_id)`.
> 104	- **MVP = texto + imagem nas redes atuais** (WordPress/LinkedIn/Twitter-X). Vídeo + TikTok/IG/YT são fase 2.
> 105	- **Cyber-Sentinel gate** no tópico e no conteúdo gerado antes de publicar (brand-safety + anti-prompt-injection).
> 106	- Toda migration nova passa `/security-review` antes do commit.
> 107	
> 108	### Assumptions
> 109	- O click ledger ML (`record_affiliate_click`) já conta cada clique que passa pelo nosso redirect (provado na auditoria).
> 110	- LinkedIn publica hoje; Twitter depende de tier Basic; Meta/IG via `publish-meta` (dev mode).
> 111	- O postback de conversão ML (`handle-ml-postback`) é infra pronta mas **não provado em produção** — atribuição de receita real depende de fechar OTD-ML-MP-PER-USER.
> 112	- Engajamento orgânico por post depende da disponibilidade de insights na API de cada rede (tier-dependente) — cliques de afiliado são o sinal sempre-disponível.
> 113	
> 114	---
> 115	
> 116	## 8. Business Risk Register
> 117	
> 118	| Risk ID | Description | Probability | Impact | RPN | Mitigation |
> 119	|---------|-------------|-------------|--------|-----|------------|
> 120	| BR-RISK-001 | Loop autônomo drena mcoCoins silenciosamente (cron × produtos × redes) | 4 | 5 | 20 | Teto por ciclo + kill-switch + safety diário (BR-VA-006 / FR-VA-007); notificação saldo baixo |
> 121	| BR-RISK-002 | "Auto-melhoria teatral": loop roda sem dado real e o LLM cai em recomendações genéricas | 4 | 4 | 16 | Bloquear análise quando `creative_metrics` vazia; usar cliques de afiliado (sempre disponível) como sinal mínimo (OTD-VA-003) |
> 122	| BR-RISK-003 | Postback ML nunca chega → receita atribuída = 0 mesmo com vendas | 3 | 5 | 15 | Fechar OTD-ML-MP-PER-USER; provar 1 postback real; ROI usa cliques como proxy enquanto isso |
> 123	| BR-RISK-004 | Conteúdo autônomo viola ToS de rede/ML ou publica algo off-brand | 3 | 5 | 15 | Cyber-Sentinel gate pré-publicação; disclosure de afiliado; rate/quota por tier; HITL opcional no plano |
> 124	| BR-RISK-005 | Volume alto de conteúdo que não converte (custo sobe, comissão não vem) | 3 | 4 | 12 | ROI por criativo + kill-switch por margem; loop poda ângulos de baixa conversão |
> 125	| BR-RISK-006 | Conteúdo só em texto em WP/LinkedIn/X (baixa viralização orgânica) | 4 | 3 | 12 | Imagem no MVP; vídeo+TikTok/IG/YT priorizados na fase 2 |
> 126	
> 127	> Probability & Impact: 1=Low, 5=High. RPN = Probability × Impact.
> 128	
> 129	---
> 130	
> 131	## 9. Business Acceptance Criteria
> 132	
> 133	| ID | Criterion | Verification Method |
> 134	|----|-----------|-------------------|
> 135	| BAC-001 | Um plano de autopilot com `interval_days=3` dispara um ciclo automaticamente sem ação humana | SELECT em `autopilot_cycles` mostrando ciclos sequenciais com `started_at` espaçados ~3d |
> 136	| BAC-002 | Todo criativo gerado (artigo+LinkedIn+X) contém link ML válido com `content_variant_id` | SELECT `creative_metrics`/`affiliate_links` por `cycle_id`; 100% com link |
> 137	| BAC-003 | Nenhum ciclo cobra mcoCoins acima do `budget_cap_mco`; ciclo aborta limpo quando excede | Smoke zero-cost: plano com cap baixo → ciclo aborta, saldo intacto |
> 138	| BAC-004 | O ciclo N+1 recebe no prompt o resumo de desempenho do ciclo N | Log/trace do prompt do gerador contendo features do `optimization_policy` do ciclo anterior |
> 139	| BAC-005 | ROI por criativo visível no dashboard (cliques + receita atribuída por peça) | UI `AutopilotPage` exibindo `creative_metrics` por `content_variant_id` |
> 140	
> 141	---
> 142	
> 143	## 10. Traceability Matrix
> 144	
> 145	| MR ID | BR ID | PR ID (stub) |
> 146	|-------|-------|--------------|
> 147	| MR-VA-001 | BR-VA-001 | PR-VA-002, PR-VA-008 |
> 148	| MR-VA-002 | BR-VA-002 | PR-VA-001, PR-VA-003 |
> 149	| MR-VA-003 | BR-VA-003 | PR-VA-004, PR-VA-005 |
> 150	| MR-VA-004 | BR-VA-004 | PR-VA-002 |
> 151	| MR-VA-005 | BR-VA-005 | PR-VA-007 |
> 152	| MR-VA-006 | BR-VA-006 | PR-VA-006 |
> 153	| MR-VA-007 | BR-VA-007 | PR-VA-001 |
> 154	| MR-VA-008 | BR-VA-008 | PR-VA-010, PR-VA-011 |
> 155	
> 156	---
> 157	
> 158	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 159	
> ```

## 🤖 Claude *(21:09:13)*

The BRD traceability matrix already shows interesting things. Let me note: BRD §10 references PR-VA-010 and PR-VA-011 for MR-VA-008. Let me read the PRD and FRD now.

## 🤖 Claude *(21:09:14)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/03-prd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# PRD — Product Requirements Document
> 2	
> 3	**Project:** viral-autopilot  
> 4	**Version:** v0.1 | **Date:** 2026-06-17  
> 5	**BoK Applied:** ProdBOK + CXBOK  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Product Vision Statement
> 11	
> 12	> Para **afiliados e criadores do Mercado Livre** que **não têm tempo nem equipe para produzir, agendar e otimizar conteúdo viral monetizado**, o **viral-autopilot** é um **piloto-automático de conteúdo** que **gera criativos product-aware, publica em cadência configurável e melhora a cada ciclo lendo o desempenho real**. Diferente de **ferramentas de agendamento (que só publicam) ou geradores de IA (que só escrevem)**, nosso produto **fecha o loop geração→publicação→atribuição→re-geração com receita de comissão ML rastreável por peça**.
> 13	
> 14	---
> 15	
> 16	## 2. User Personas
> 17	
> 18	### Persona 1 — Rafael, o Afiliado-Solo (Primary)
> 19	
> 20	| Attribute | Detail |
> 21	|-----------|--------|
> 22	| Role | Afiliado ML / criador de conteúdo que monetiza links (perfil do Usuário Zero) |
> 23	| Goals | Escalar volume de conteúdo monetizado sem virar refém da produção manual; saber o que converte |
> 24	| Frustrations | Escrever copy à mão para cada produto/rede; colar links manualmente; não saber qual post deu venda |
> 25	| Tech-savviness | 3 (confortável com ferramentas, não-programador) |
> 26	| MCORCH usage pattern | Define plano(s) de autopilot, confere o dashboard de ROI por ciclo, ajusta produtos-alvo |
> 27	| Quote | _"Eu quero ligar isso numa sexta e na segunda ter conteúdo no ar, com link certo, e ver o que vendeu."_ |
> 28	
> 29	### Persona 2 — Marina, a Gestora de Múltiplas Contas (Secondary)
> 30	
> 31	| Attribute | Detail |
> 32	|-----------|--------|
> 33	| Role | Gestora de PME/agência operando várias contas/produtos de afiliado |
> 34	| Goals | Cadência consistente em várias contas; relatório de ROI por produto/criativo para decidir investimento |
> 35	| Frustrations | Gerenciar credenciais e calendário de N contas; sem visão consolidada de qual criativo performa |
> 36	| Tech-savviness | 4 |
> 37	| MCORCH usage pattern | Vários planos (um por produto/conta), BYOK por tenant, foco no relatório ciclo-a-ciclo |
> 38	| Quote | _"Preciso de cadência previsível e um número de ROI por peça que eu possa mostrar ao cliente."_ |
> 39	
> 40	---
> 41	
> 42	## 3. User Journey Maps
> 43	
> 44	### Journey: Ligar o Autopilot (Rafael, Happy Path)
> 45	
> 46	| Stage | Action | Touchpoint | Emotion | Opportunity |
> 47	|-------|--------|-----------|---------|-------------|
> 48	| Awareness | Descobre o Autopilot no dashboard | `AutopilotPage` (nav) | 😐 Neutral | Empty-state explicando o ciclo + custo |
> 49	| Consideration | Cria um plano: escolhe produtos-alvo + redes + modo | Plan editor | 🤔 Curious | Pré-visualizar custo projetado por ciclo (mcoCoins) |
> 50	| Activation | Salva o plano e dispara "tudo de uma vez" (ou ativa cadência) | Run/Activate button | 😊 Excited | Confirmar teto de custo antes de disparar |
> 51	| Value | Vê criativos publicados e o primeiro ROI por peça | Cycle timeline + ROI cards | 🚀 Delighted | Destacar o "vencedor" do ciclo |
> 52	| Retention | Ciclo seguinte melhora sozinho; ajusta produtos | Auto-improve insight card | ❤️ Loyal | Mostrar o lift ciclo-a-ciclo |
> 53	
> 54	#### Edge Case 1: Saldo insuficiente / teto estourado
> 55	> No disparo, o custo projetado excede `budget_cap_mco` ou o saldo está abaixo do mínimo → ciclo **não inicia**, plano não cobra, toast PT-BR "Saldo/teto insuficiente para este ciclo" + plano marcado `paused`.
> 56	
> 57	#### Edge Case 2: Métricas ainda não chegaram (ciclo 1)
> 58	> No primeiro ciclo não há desempenho anterior → o analisador usa baseline (sem dado) e o gerador roda com framework viral padrão + sinal de trends; o insight card sinaliza "coletando desempenho — melhoria a partir do ciclo 2".
> 59	
> 60	---
> 61	
> 62	## 4. Feature Inventory (MoSCoW)
> 63	
> 64	> Effort: S=hours, M=days, L=week, XL=sprint
> 65	
> 66	### Must Have (MVP — texto + imagem nas redes atuais)
> 67	
> 68	| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |
> 69	|----|---------|---------|-----------|--------|-------------|-------|
> 70	| PR-VA-001 | **Autopilot Plan** — criar/editar plano (produtos-alvo, redes, modo all-at-once vs cada-N-dias, teto) | P1, P2 | BR-VA-002, BR-VA-007, BR-VA-008 | L | 0 | Entidade `autopilot_plans` per-user; default `interval_days=3` |
> 71	| PR-VA-002 | **Product-aware generation** — texto monetizado (artigo+LinkedIn+X) com copy de venda em torno do produto-alvo, link ML em todo formato | P1 | BR-VA-001, BR-VA-004 | L | herda 10 + sub-steps | Substitui prompts B2B; corrige `affiliate_url` dropado |
> 72	| PR-VA-003 | **Cadence scheduler** — cron por-tenant que dispara o ciclo a cada N dias (auto-refill) | P1, P2 | BR-VA-002 | L | 0 | Generaliza primitiva nurture (`next_run_at` + pg_cron) |
> 73	| PR-VA-004 | **Performance collector** — cliques afiliado + engajamento orgânico + receita → `creative_metrics` | P1, P2 | BR-VA-005, BR-VA-003 | L | 0 | Combo (Decisão 3); cliques primeiro, orgânico best-effort |
> 74	| PR-VA-005 | **Self-improvement feedback** — analisar lote anterior → injetar features no prompt do próximo | P1 | BR-VA-003 | M | 5 (análise) | Fecha as 3 quebras do `self-optimize` |
> 75	| PR-VA-006 | **Cost guardrail** — teto por ciclo + kill-switch + alerta de saldo baixo (antes do deduct) | P1, P2 | BR-VA-006 | M | 0 | `budget_cap_mco` no plano; espelha caps vision-mcp |
> 76	| PR-VA-007 | **Autopilot dashboard** — timeline de ciclos + criativos + ROI por peça | P1, P2 | BR-VA-005 | M | 0 | Hook `useAutopilot`; reusa ROIWidget |
> 77	| PR-VA-008 | **Image creative** — imagem por criativo, produto ML como referência, formato por plataforma | P1 | BR-VA-001 | M | ~img cost | MVP (Decisão 2); plugar `generate-image` (hoje órfã) ao ciclo |
> 78	
> 79	### Should Have (v1.0)
> 80	
> 81	| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |
> 82	|----|---------|---------|-----------|--------|-------------|-------|
> 83	| PR-VA-010 | **Auto product selection** — selecionar produto do catálogo por `commission_value`+`trend_score` (além dos 3 semente) | P1, P2 | BR-VA-008 | M | 0 | OTD-VA-006: auto-score em v1.0 |
> 84	| PR-VA-011 | **Trend-informed angle** — `fetch-trends`/`vm_trends` pautam o ângulo viral | P1 | BR-VA-008 | M | 0 | Reconecta a ilha de trends ao gerador |
> 85	| PR-VA-012 | **A/B variant generation** — N variações por criativo por ciclo, escolhe vencedora pelo desempenho | P1 | BR-VA-003 | M | herda geração | Acelera o aprendizado do loop |
> 86	| PR-VA-013 | **HITL gate opcional** — aprovação humana antes de publicar (plano configura) | P2 | BR-VA-004 | S | 0 | Reusa policy-engine do `intent-execute` |
> 87	
> 88	### Could Have (Future / Fase 2)
> 89	
> 90	| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |
> 91	|----|---------|---------|-----------|--------|-------------|-------|
> 92	| PR-VA-020 | **Video creative 9:16** (TikTok/Reels/Shorts) | P1 | BR-VA-001 | XL | vídeo cost | Fase 2 (Decisão 2); `generate-video` hoje órfã |
> 93	| PR-VA-021 | **TikTok/Instagram/YouTube publishing** | P1 | BR-VA-001 | XL | 0 | Fase 2; OAuth + publish novos destinos |
> 94	| PR-VA-022 | **Catalog auto-discovery cron** — produtiza `discover-affiliate-products.ts` (hoje CLI manual) | P2 | BR-VA-008 | L | 0 | Score por comissão/trend real, não só log10(preço) |
> 95	
> 96	### Won't Have (This Cycle)
> 97	
> 98	- Gestão de anúncios pagos (Meta Ads) dentro do autopilot — `sync-meta-ads` permanece separado.
> 99	- Deduplicação de atribuição cross-network (multi-touch) — atribuição é por clique/postback no MVP.
> 100	- Outreach a influenciadores / parcerias.
> 101	
> 102	---
> 103	
> 104	## 5. Release Phasing
> 105	
> 106	### MVP Scope
> 107	**Target date:** 2026-07-31  
> 108	**Included:** PR-VA-001, PR-VA-002, PR-VA-003, PR-VA-004, PR-VA-005, PR-VA-006, PR-VA-007, PR-VA-008  
> 109	**Success gate:** um plano dispara ciclos a cada 3 dias, gera texto+imagem monetizados em WP/LinkedIn/X, coleta cliques de afiliado, e o ciclo 2 demonstra reinjeção do desempenho do ciclo 1 — tudo dentro do teto de custo (smoke zero-cost provando o kill-switch).
> 110	
> 111	### v1.0 Scope
> 112	**Target date:** 2026-08-31  
> 113	**Adds:** PR-VA-010, PR-VA-011, PR-VA-012, PR-VA-013  
> 114	**Success gate:** seleção automática de produto por comissão+trend + ângulo informado por trends + A/B + HITL opcional; lift de engajamento ciclo-a-ciclo ≥ 1.10× medido.
> 115	
> 116	### Future Scope
> 117	**Items:** PR-VA-020, PR-VA-021, PR-VA-022  
> 118	**Condition:** após MVP validado e decisão Sovereign de priorizar mídia viral (vídeo 9:16 + redes virais) — gate de esforço XL.
> 119	
> 120	---
> 121	
> 122	## 6. Luxury UX Specifications
> 123	
> 124	### 6.1 Color & Visual Identity
> 125	
> 126	| Token | Value | Usage |
> 127	|-------|-------|-------|
> 128	| `--bg-deep` | `#0A0A0F` | Canvas background da AutopilotPage |
> 129	| `--accent-violet` | `#7C3AED` | CTA "Ativar Autopilot", estado ativo do plano |
> 130	| `--accent-cyan` | `#06B6D4` | Métricas de ROI, gráficos de lift ciclo-a-ciclo |
> 131	| `--glass-surface` | `rgba(255,255,255,0.04)` | Cards de ciclo e de criativo |
> 132	| `--border-subtle` | `rgba(255,255,255,0.08)` | Bordas de card |
> 133	
> 134	### 6.2 Animation Guidelines
> 135	
> 136	| Element | Library | Duration | Easing |
> 137	|---------|---------|----------|--------|
> 138	| Transição de página | Framer Motion | 300ms | `easeInOut` |
> 139	| Entrada de card de ciclo | Framer Motion | 300ms | `easeOut` |
> 140	| Pulse de status "ciclo rodando" | CSS keyframes | 2s | `ease-in-out infinite` |
> 141	| Highlight do criativo "vencedor" | Framer Motion | 150ms | `easeOut` |
> 142	
> 143	### 6.3 Interaction Patterns
> 144	
> 145	- **Cards:** glass morphism — `backdrop-blur-sm`, borda sutil, sombra `0 4px 24px rgba(0,0,0,0.4)`.
> 146	- **Botão "Ativar Autopilot":** gradiente no hover; confirmação de teto de custo (mcoCoins) antes do disparo.
> 147	- **Loading:** skeleton shimmer nos cards de ciclo (nunca spinner em área de conteúdo).
> 148	- **Toasts:** `sonner` — sucesso=violeta, erro=vermelho, info=ciano. Saldo/teto insuficiente = toast PT-BR explícito.
> 149	
> 150	### 6.4 Accessibility (WCAG 2.1 AA)
> 151	
> 152	- Contraste ≥ 4.5:1 para texto sobre vidro.
> 153	- Todos os controles do plano navegáveis por teclado.
> 154	- ARIA labels nos botões ícone (ativar/pausar/editar plano).
> 155	- Foco visível ≥ 2px.
> 156	
> 157	---
> 158	
> 159	## 7. Acceptance Criteria (Gherkin)
> 160	
> 161	```gherkin
> 162	Feature: Viral Autopilot — ciclo autônomo monetizado e auto-melhorável
> 163	
> 164	  Scenario: Ativar plano com cadência de 3 dias (PR-VA-001, PR-VA-003)
> 165	    Given um operador autenticado com saldo de mcoCoins suficiente
> 166	    And um plano com produtos-alvo [Roborock S8], redes [wordpress, linkedin, twitter], modo "every_n_days", interval_days 3
> 167	    When o operador ativa o plano
> 168	    Then o sistema agenda next_run_at para now
> 169	    And o cron dispara o primeiro ciclo sem ação humana
> 170	    And cria uma linha em autopilot_cycles com status "running"
> 171	
> 172	  Scenario: Geração product-aware monetizada em todo formato (PR-VA-002, PR-VA-008)
> 173	    Given um ciclo em execução com produto-alvo "Roborock S8"
> 174	    When o gerador produz artigo, post de LinkedIn, thread de X e imagem
> 175	    Then cada formato menciona o produto e contém um link de afiliado ML válido com content_variant_id
> 176	    And a imagem usa a image_url do produto como referência
> 177	
> 178	  Scenario: Kill-switch de custo antes do deduct (PR-VA-006)
> 179	    Given um plano com budget_cap_mco 5 e custo de ciclo projetado 15
> 180	    When o cron tenta disparar o ciclo
> 181	    Then o ciclo aborta com status "aborted_budget"
> 182	    And nenhum mcoCoin é deduzido
> 183	    And o plano é marcado "paused" com notificação PT-BR "Teto de custo insuficiente para este ciclo"
> 184	
> 185	  Scenario: Loop auto-melhorável realimenta o ciclo seguinte (PR-VA-004, PR-VA-005)
> 186	    Given o ciclo 1 publicou criativos e o coletor gravou cliques de afiliado em creative_metrics
> 187	    When o ciclo 2 é disparado
> 188	    Then o analisador produz um optimization_policy a partir do desempenho do ciclo 1
> 189	    And o prompt de geração do ciclo 2 inclui as features de melhor desempenho (top hook/produto/horário)
> 190	
> 191	  Scenario: ROI por criativo visível (PR-VA-007)
> 192	    Given criativos publicados com cliques e/ou receita atribuída
> 193	    When o operador abre a AutopilotPage
> 194	    Then vê, por content_variant_id, cliques, receita atribuída e o criativo vencedor do ciclo
> 195	```
> 196	
> 197	---
> 198	
> 199	## 8. Traceability Matrix
> 200	
> 201	| MR ID | BR ID | PR ID |
> 202	|-------|-------|-------|
> 203	| MR-VA-001 | BR-VA-001 | PR-VA-002, PR-VA-008 |
> 204	| MR-VA-002 | BR-VA-002 | PR-VA-001, PR-VA-003 |
> 205	| MR-VA-003 | BR-VA-003 | PR-VA-004, PR-VA-005, PR-VA-012 |
> 206	| MR-VA-004 | BR-VA-004 | PR-VA-002, PR-VA-013 |
> 207	| MR-VA-005 | BR-VA-005 | PR-VA-007 |
> 208	| MR-VA-006 | BR-VA-006 | PR-VA-006 |
> 209	| MR-VA-007 | BR-VA-007 | PR-VA-001 |
> 210	| MR-VA-008 | BR-VA-008 | PR-VA-010, PR-VA-011, PR-VA-022 |
> 211	
> 212	---
> 213	
> 214	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 215	
> ```

## 🤖 Claude *(21:09:14)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/04-frd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# FRD — Functional Requirements Document
> 2	
> 3	**Project:** viral-autopilot  
> 4	**Version:** v0.1 | **Date:** 2026-06-17  
> 5	**BoK Applied:** SWEBOK v4 (Software Requirements)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Scope Statement
> 11	
> 12	Este documento especifica os requisitos funcionais e não-funcionais do `viral-autopilot`. Deriva do PRD `03-prd.md` e alimenta o SDD `05-sdd.md`.
> 13	
> 14	**In scope (MVP+v1.0):** entidade de plano de cadência; cron de disparo recorrente por-tenant; geração product-aware monetizada em todo formato (texto+imagem); coletor de desempenho unificado (cliques+orgânico+receita); analisador de ciclo + reinjeção de aprendizado; guarda de custo (teto + kill-switch); dashboard de ROI por criativo; seleção de produto por comissão+trend; ângulo informado por trends.
> 15	
> 16	**Out of scope (Fase 2 / Won't):** geração de vídeo 9:16; publicação em TikTok/Instagram/YouTube; gestão de anúncios pagos; atribuição multi-touch cross-network; auto-descoberta de catálogo (CLI manual permanece até PR-VA-022).
> 17	
> 18	---
> 19	
> 20	## 2. Functional Requirements
> 21	
> 22	> Category: `UI` | `Hook` | `EdgeFunction` | `DB` | `Cron` | `Lib`
> 23	
> 24	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 25	|----|-------|-------------|----------|-----------|----------|---------|
> 26	| FR-VA-001 | Autopilot plan entity | Tabela `autopilot_plans` (per-user RLS): mode (`all_at_once`\|`every_n_days`), interval_days (default 3), target_product_ids[], platforms[], budget_cap_mco, is_active, next_run_at. CRUD via hook. | Critical | PR-VA-001 | DB | AT-VA-001 |
> 27	| FR-VA-002 | Cycle dispatcher | Edge fn `autopilot-run` (JWT): valida plano, aplica gate de custo (FR-VA-007), seleciona produto(s), abre `autopilot_cycles`, e faz fan-out product-aware para `orchestrate-content` (1 dispatch por produto×rede). Reusa o padrão de `campaign-run`. | Critical | PR-VA-002, PR-VA-001 | EdgeFunction | AT-VA-002 |
> 28	| FR-VA-003 | Product-aware generation | Em `orchestrate-step`, o prompt recebe o produto-alvo (id+nome+imagem+preço+comissão) e usa framework de gancho viral de consumo (hook/valor/CTA) — substitui os system prompts B2B hardcoded (`:138`,`:290`). | Critical | PR-VA-002 | Lib/EdgeFunction | AT-VA-003 |
> 29	| FR-VA-004 | Monetize all formats | `monetizeContent` (`_shared/affiliate.ts`) roda em artigo **+ LinkedIn + Twitter**, embutindo link ML per-user com `content_variant_id` por criativo (não só no artigo, não por regex de 3 SKUs). | Critical | PR-VA-002 | Lib | AT-VA-004 |
> 30	| FR-VA-005 | Cadence cron | pg_cron `autopilot-cadence` (*/15) → fn `autopilot-cadence-cron` (service-role): encontra planos `is_active AND next_run_at <= now`, dispara `autopilot-run`, e re-agenda `next_run_at = now + interval_days` (auto-refill, ao contrário do drip finito do nurture). | Critical | PR-VA-003 | Cron | AT-VA-005 |
> 31	| FR-VA-006 | Cycle ledger | Tabela `autopilot_cycles`: plan_id, cycle_number, status (`running`\|`completed`\|`aborted_budget`\|`failed`), spend_mco, planned_units, analysis_node_id, started_at, completed_at. Idempotência por (plan_id, cycle_number). | Critical | PR-VA-003, PR-VA-006 | DB | AT-VA-006 |
> 32	| FR-VA-007 | Cost guardrail (kill-switch) | ANTES de qualquer `deduct_mco_coins`: soma custo projetado (10 + 5 + img × nº criativos). Se `> budget_cap_mco` OU `saldo < min_balance` → aborta ciclo (`aborted_budget`), pausa o plano, notifica. Espelha caps do `vision-mcp`. | Critical | PR-VA-006 | EdgeFunction | AT-VA-007 |
> 33	| FR-VA-008 | Engagement collector | Cron `autopilot-collect` → fn que, dado o `post_id` retornado por `publish-social`/`publish-meta`, busca insights reais (best-effort por API tier) e grava em `creative_metrics`. | High | PR-VA-004 | Cron/EdgeFunction | AT-VA-008 |
> 34	| FR-VA-009 | Unified creative metrics | Tabela `creative_metrics` keyed por `content_variant_id`: affiliate_clicks, impressions, engagements, revenue_cents, source, collected_at. Unifica os 3 sinais (Decisão 3). | High | PR-VA-004 | DB | AT-VA-009 |
> 35	| FR-VA-010 | Cycle analyzer | Edge fn `autopilot-analyze` (service-role, 5 mco): lê `creative_metrics` do ciclo anterior do tenant; se vazio, usa baseline (NÃO inventa); produz `optimization_policy` estruturado (top hook/produto/horário/formato). Generaliza `self-optimize`, agora agendado. | High | PR-VA-005 | EdgeFunction | AT-VA-010 |
> 36	| FR-VA-011 | Feedback injection | A geração (`orchestrate-step`/`autopilot-run`) LÊ o `optimization_policy` mais recente do tenant e injeta as features no system prompt do próximo ciclo. Fecha a quebra "saída sem consumo". | Critical | PR-VA-005 | Lib/EdgeFunction | AT-VA-011 |
> 37	| FR-VA-012 | Product selection by score | Seleção do produto-alvo do `vm_affiliate_products` por `commission_value`+`trend_score`+`profitability_score` (auto em v1.0). No MVP: 3 SKUs semente referenciados no plano. | High | PR-VA-010, PR-VA-001 | EdgeFunction | AT-VA-012 |
> 38	| FR-VA-013 | Image creative (product-referenced) | Plugar `generate-image` (hoje órfã) ao ciclo: usa `image_url` do produto ML como referência; formato por plataforma (quadrado MVP; 9:16 fase 2). Anexa asset a `scheduled_posts`. | Should (MVP) | PR-VA-008 | EdgeFunction | AT-VA-013 |
> 39	| FR-VA-014 | Autopilot hook | `useAutopilot` (TanStack Query): CRUD de plano, status de ciclos, ROI por criativo. Toda lógica de dados no hook (Harness Engineering). | High | PR-VA-001, PR-VA-007 | Hook | AT-VA-014 |
> 40	| FR-VA-015 | Autopilot dashboard | `AutopilotPage` (display-only): editor de plano, timeline de ciclos, cards de criativo com ROI, criativo "vencedor", insight de lift ciclo-a-ciclo. | High | PR-VA-007 | UI | AT-VA-015 |
> 41	| FR-VA-016 | Honor product/affiliate param | `orchestrate-content` passa a desestruturar e honrar o produto-alvo/`affiliate_url` (hoje dropado em `:79`), propagando ao `orchestrate-step`. | Medium | PR-VA-002 | EdgeFunction | AT-VA-016 |
> 42	| FR-VA-017 | Revenue attribution per creative | `handle-ml-postback` credita `revenue_cents` na `affiliate_links` correta e o coletor (FR-VA-008) reflete em `creative_metrics` por `content_variant_id`. Depende de OTD-VA-007. | High | PR-VA-007 | EdgeFunction | AT-VA-017 |
> 43	| FR-VA-018 | Trend-informed angle | `autopilot-run` lê `vm_trends` (de `fetch-trends`) para pautar o ângulo viral do ciclo (reconecta a ilha de trends). | Should (v1.0) | PR-VA-011 | EdgeFunction | AT-VA-018 |
> 44	
> 45	---
> 46	
> 47	## 3. Non-Functional Requirements
> 48	
> 49	| ID | Category | Requirement | Target | Measurement |
> 50	|----|----------|-------------|--------|-------------|
> 51	| NFR-VA-001 | Performance | Dispatch do ciclo (fan-out) p95 | < 5min para N ≤ 8 criativos | Supabase logs + `autopilot_cycles.completed_at − started_at` |
> 52	| NFR-VA-002 | Cost-safety | Gate de teto aplicado ANTES de qualquer deduct mcoCoins | 100% dos ciclos (zero deduct em ciclo abortado) | Smoke zero-cost; saldo intacto pós-abort |
> 53	| NFR-VA-003 | Idempotency | Re-fire do cron sobre o mesmo ciclo não dobra cobrança nem post | 0 duplicatas | Idempotência por (plan_id, cycle_number); guarda em `scheduled_posts` |
> 54	| NFR-VA-004 | Tenancy | Toda credencial externa resolvida per-user (`auth.uid()`); zero chave global em path user-facing | 100% | Code review + grep de `Deno.env` em fluxo user-facing |
> 55	| NFR-VA-005 | Security | Edge fns user-facing exigem JWT; crons usam service-role; RLS default-deny em toda tabela | 100% | `/security-review` |
> 56	| NFR-VA-006 | Availability/Self-heal | Cron reconcilia janelas perdidas (catch-up) sem disparar ciclos duplicados | recupera em ≤ 1 tick (15min) | Teste de janela perdida |
> 57	| NFR-VA-007 | Auditability | Todo post autônomo rastreável a `cycle_id`+`plan_id`+`product`+`content_variant_id` | 100% | SELECT join `scheduled_posts`↔`autopilot_cycles` |
> 58	| NFR-VA-008 | Brand-safety | Cyber-Sentinel no tópico e no conteúdo gerado antes de publicar; disclosure de afiliado | 100% dos criativos | Gate pré-publicação + revisão |
> 59	
> 60	---
> 61	
> 62	## 4. Interface Requirements
> 63	
> 64	### 4.1 UI → Hook → Edge Function Contract
> 65	
> 66	```
> 67	[Component: AutopilotPage.tsx]
> 68	  ↓ calls
> 69	[Hook: useAutopilot.ts]   (CRUD plano · status ciclos · ROI por criativo)
> 70	  ↓ calls (sensitive ops)
> 71	[Edge Function: autopilot-run]   (gate custo → seleção produto → fan-out)
> 72	  ↓ dispatch (forward JWT, self-bill)
> 73	[Edge Function: orchestrate-content → orchestrate-step]   (geração product-aware + monetize)
> 74	  ↓ reads/writes
> 75	[Tables: autopilot_plans · autopilot_cycles · creative_metrics · scheduled_posts · affiliate_links]
> 76	```
> 77	
> 78	### 4.2 External API Contracts
> 79	
> 80	#### `POST /functions/v1/autopilot-run`
> 81	
> 82	**Auth:** Bearer JWT (user scope) — OU service-role quando chamado pelo cron (`X-Cron-Trigger`).  
> 83	**Request:**
> 84	```typescript
> 85	{
> 86	  plan_id: string,          // uuid do autopilot_plans (RLS-own)
> 87	  mode_override?: "all_at_once" | "every_n_days",  // opcional; default = plano
> 88	  dry_run?: boolean,        // se true, retorna custo projetado SEM deduzir nem publicar
> 89	}
> 90	```
> 91	**Response (200):**
> 92	```typescript
> 93	{
> 94	  status: "ok",
> 95	  cycle_id: string,
> 96	  cycle_number: number,
> 97	  projected_cost_mco: number,
> 98	  dispatched: { product_id: string, platform: string, run_id: string }[],
> 99	}
> 100	```
> 101	**Error codes:**
> 102	| Code | Condition |
> 103	|------|-----------|
> 104	| 401 | JWT ausente/inválido |
> 105	| 402 | Saldo de mcoCoins insuficiente (`insufficient_balance`) |
> 106	| 409 | Teto de custo do ciclo excedido (`aborted_budget`) — plano pausado |
> 107	| 422 | Validação: plano sem produtos/redes, `interval_days` inválido (campo+mensagem PT-BR) |
> 108	| 500 | Erro interno (logado em `infra_health_logs`) |
> 109	
> 110	#### `POST /functions/v1/autopilot-analyze`
> 111	
> 112	**Auth:** service-role (chamado pós-ciclo / pelo cron).  
> 113	**Request:** `{ tenant_id: string, plan_id: string, previous_cycle_id: string }`  
> 114	**Response (200):** `{ status: "ok", optimization_policy_id: string, has_real_data: boolean, top_features: {...} }`  
> 115	> `has_real_data=false` quando `creative_metrics` do ciclo anterior está vazia → usa baseline, NÃO inventa.
> 116	
> 117	---
> 118	
> 119	## 5. Data Requirements
> 120	
> 121	| Field | Type | Nullable | Validation Rule | Error Message (PT-BR) |
> 122	|-------|------|----------|-----------------|----------------------|
> 123	| `autopilot_plans.mode` | `text` | NOT NULL | ∈ {`all_at_once`,`every_n_days`} | "Modo de cadência inválido." |
> 124	| `autopilot_plans.interval_days` | `int` | NULL (req. se `every_n_days`) | 1 ≤ n ≤ 30; default 3 | "Intervalo deve ser entre 1 e 30 dias." |
> 125	| `autopilot_plans.target_product_ids` | `text[]` | NOT NULL | tamanho ≥ 1; ids ∈ `vm_affiliate_products` | "Selecione ao menos um produto-alvo." |
> 126	| `autopilot_plans.platforms` | `text[]` | NOT NULL | ⊆ {`wordpress`,`linkedin`,`twitter`} (MVP) | "Selecione ao menos uma rede suportada." |
> 127	| `autopilot_plans.budget_cap_mco` | `int` | NOT NULL | ≥ custo mínimo de 1 criativo | "Teto de custo abaixo do mínimo de um ciclo." |
> 128	| `creative_metrics.content_variant_id` | `uuid` | NOT NULL | FK → criativo/`content_library` | — |
> 129	| `creative_metrics.source` | `text` | NOT NULL | ∈ {`affiliate_click`,`organic`,`postback`} | — |
> 130	| `creative_metrics.revenue_cents` | `int` | NOT NULL DEFAULT 0 | ≥ 0 | — |
> 131	
> 132	---
> 133	
> 134	## 6. Test Strategy Matrix
> 135	
> 136	| FR ID | Unit Test | Integration Test | E2E Test | Notes |
> 137	|-------|-----------|-----------------|----------|-------|
> 138	| FR-VA-001 | ✅ | ✅ | — | RLS own-row; validação de campos |
> 139	| FR-VA-002 | ✅ | ✅ | ✅ | fan-out + forward JWT (smoke zero-cost com `dry_run`) |
> 140	| FR-VA-003 | ✅ | ✅ | — | prompt contém produto + framework viral |
> 141	| FR-VA-004 | ✅ | ✅ | ✅ | link ML + `content_variant_id` em TODO formato |
> 142	| FR-VA-005 | ✅ | ✅ | — | auto-refill `next_run_at`; janela perdida (catch-up) |
> 143	| FR-VA-006 | ✅ | ✅ | — | idempotência (plan_id, cycle_number) |
> 144	| FR-VA-007 | ✅ | ✅ | ✅ | **kill-switch smoke zero-cost** (saldo intacto pós-abort) |
> 145	| FR-VA-008 | ✅ | ✅ | — | coletor best-effort por tier; cliques sempre |
> 146	| FR-VA-009 | ✅ | — | — | unicidade por `content_variant_id`+`source` |
> 147	| FR-VA-010 | ✅ | ✅ | — | baseline quando vazio (`has_real_data=false`) |
> 148	| FR-VA-011 | ✅ | ✅ | ✅ | prova de reinjeção: prompt ciclo N+1 contém features do ciclo N |
> 149	| FR-VA-012 | ✅ | ✅ | — | ranking comissão+trend |
> 150	| FR-VA-013 | ✅ | ✅ | — | imagem product-referenced anexada a `scheduled_posts` |
> 151	| FR-VA-014 | ✅ | — | — | hook CRUD + queries |
> 152	| FR-VA-015 | — | — | ✅ | E2E UI 1920×1080 (gate Canvas/UI) |
> 153	| FR-VA-016 | ✅ | ✅ | — | param honrado (regressão do drop em `:79`) |
> 154	| FR-VA-017 | ✅ | ✅ | — | atribuição por `content_variant_id` (gated em OTD-VA-007) |
> 155	| FR-VA-018 | ✅ | ✅ | — | ângulo lê `vm_trends` |
> 156	
> 157	**Test files location:**
> 158	- Unit: `src/hooks/__tests__/useAutopilot.test.ts`
> 159	- Integration / smokes: `scripts/qa/smoke-autopilot-run.ts`, `scripts/qa/smoke-autopilot-budget.ts` (zero-cost)
> 160	- E2E: `e2e/viral-autopilot.spec.ts` + gate `/e2e-audit` 1920×1080 para `AutopilotPage`
> 161	
> 162	---
> 163	
> 164	## 7. Traceability Matrix
> 165	
> 166	| PR ID | FR ID | NFR ID |
> 167	|-------|-------|--------|
> 168	| PR-VA-001 | FR-VA-001, FR-VA-014, FR-VA-016 | NFR-VA-004, NFR-VA-005 |
> 169	| PR-VA-002 | FR-VA-002, FR-VA-003, FR-VA-004, FR-VA-016 | NFR-VA-001, NFR-VA-008 |
> 170	| PR-VA-003 | FR-VA-005, FR-VA-006 | NFR-VA-003, NFR-VA-006 |
> 171	| PR-VA-004 | FR-VA-008, FR-VA-009, FR-VA-017 | NFR-VA-007 |
> 172	| PR-VA-005 | FR-VA-010, FR-VA-011 | NFR-VA-007 |
> 173	| PR-VA-006 | FR-VA-007 | NFR-VA-002 |
> 174	| PR-VA-007 | FR-VA-014, FR-VA-015, FR-VA-017 | NFR-VA-007 |
> 175	| PR-VA-008 | FR-VA-013 | NFR-VA-008 |
> 176	| PR-VA-010 | FR-VA-012 | — |
> 177	| PR-VA-011 | FR-VA-018 | — |
> 178	
> 179	---
> 180	
> 181	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 182	
> ```

## 🤖 Claude *(21:09:18)*

I now have the four traceability docs. Let me read the SDD, data-model, process-flow, and index to verify downstream artifacts (tables, edge fns, crons, processes).

## 🤖 Claude *(21:09:19)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/05-sdd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# SDD — System Design Document
> 2	
> 3	**Project:** viral-autopilot  
> 4	**Version:** v0.1 | **Date:** 2026-06-17  
> 5	**BoK Applied:** SWEBOK v4 (Software Design) + CISSP CBK 2024 (Software Development Security)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Architecture Overview
> 11	
> 12	O `viral-autopilot` é o **orquestrador de ciclo** que costura peças já existentes do MCORCH num loop fechado. Não reinventa geração nem receita — adiciona a cabeça que planeja, dispara, mede e aprende.
> 13	
> 14	```
> 15	┌──────────────────────────────────────────────────────────────┐
> 16	│  PRESENTATION LAYER (display-only)                            │
> 17	│  src/pages/AutopilotPage.tsx                                  │
> 18	│  src/components/autopilot/{PlanEditor,CycleTimeline,RoiCard}  │
> 19	└───────────────────────┬──────────────────────────────────────┘
> 20	                        │ calls
> 21	┌───────────────────────▼──────────────────────────────────────┐
> 22	│  LOGIC LAYER (Harness Engineering)                            │
> 23	│  src/hooks/useAutopilot.ts  (TanStack Query — plano/ciclo/ROI)│
> 24	└───────────────────────┬──────────────────────────────────────┘
> 25	                        │ HTTP + JWT
> 26	┌───────────────────────▼──────────────────────────────────────┐
> 27	│  EDGE LAYER (Deno / Supabase Functions)                       │
> 28	│  autopilot-run ─────────────┐   autopilot-analyze (5 mco)     │
> 29	│  autopilot-cadence-cron ◀───┤   autopilot-collect             │
> 30	│  (service-role, pg_cron)    │                                 │
> 31	│      │ fan-out (forward JWT) │ reuse                          │
> 32	│      ▼                       ▼                                 │
> 33	│  orchestrate-content → orchestrate-step (product-aware gen)   │
> 34	│  _shared/affiliate.ts (monetize ALL formats)                  │
> 35	└──────────┬───────────────────────────────┬───────────────────┘
> 36	           │ Supabase RLS                  │ External APIs
> 37	┌──────────▼────────────────┐  ┌───────────▼────────────────────┐
> 38	│  DB LAYER                  │  │  EXTERNAL SERVICES              │
> 39	│  autopilot_plans (new)     │  │  OpenRouter/Groq (LLM, BYOK)    │
> 40	│  autopilot_cycles (new)    │  │  DALL·E/Nano Banana (image)     │
> 41	│  creative_metrics (new)    │  │  LinkedIn/X/WordPress (publish) │
> 42	│  scheduled_posts (reuse)   │  │  Mercado Livre/Pago (postback)  │
> 43	│  affiliate_links (reuse)   │  │  Apify (fetch-trends, v1.0)     │
> 44	│  optimization_policy(reuse)│  └─────────────────────────────────┘
> 45	│  vm_affiliate_products     │
> 46	│  mcorch_nodes/_edges       │
> 47	└────────────────────────────┘
> 48	```
> 49	
> 50	---
> 51	
> 52	## 2. Component Catalog
> 53	
> 54	### 2.1 New Custom Hooks (`src/hooks/`)
> 55	
> 56	| Hook | File | Responsibility | TanStack Query keys |
> 57	|------|------|---------------|---------------------|
> 58	| `useAutopilot` | `useAutopilot.ts` | CRUD de `autopilot_plans`; lista ciclos; ROI por criativo; activate/pause | `['autopilot-plans']`, `['autopilot-cycles', planId]`, `['creative-metrics', cycleId]` |
> 59	
> 60	### 2.2 New Display Components (`src/components/autopilot/`)
> 61	
> 62	| Component | File | Props | Hook consumed |
> 63	|-----------|------|-------|--------------|
> 64	| `AutopilotPage` | `src/pages/AutopilotPage.tsx` | — (route) | `useAutopilot` |
> 65	| `PlanEditor` | `src/components/autopilot/PlanEditor.tsx` | `plan?, onSave` | `useAutopilot` |
> 66	| `CycleTimeline` | `src/components/autopilot/CycleTimeline.tsx` | `planId` | `useAutopilot` |
> 67	| `RoiCard` | `src/components/autopilot/RoiCard.tsx` | `creativeMetric` | — (display) |
> 68	
> 69	### 2.3 New Edge Functions (`supabase/functions/`)
> 70	
> 71	| Function | Path | Auth | mcoCoins | Secrets needed |
> 72	|----------|------|------|----------|----------------|
> 73	| `autopilot-run` | `supabase/functions/autopilot-run/index.ts` | JWT (user) OR service-role (cron) | gate só; deduct ocorre nos sub-runs | — (resolve per-user) |
> 74	| `autopilot-cadence-cron` | `supabase/functions/autopilot-cadence-cron/index.ts` | service-role (`verify_jwt=false`, pg_net) | 0 | `SB_SECRET_KEY` (service) |
> 75	| `autopilot-analyze` | `supabase/functions/autopilot-analyze/index.ts` | service-role | 5 mco (análise) | LLM key (per-user→sistema fallback) |
> 76	| `autopilot-collect` | `supabase/functions/autopilot-collect/index.ts` | service-role (cron) | 0 | social/meta tokens per-user |
> 77	
> 78	> **Reuso (modificadas, não novas):** `orchestrate-content` (FR-VA-016 honra produto), `orchestrate-step` (FR-VA-003 product-aware + FR-VA-011 feedback inject), `_shared/affiliate.ts` (FR-VA-004 monetiza todo formato), `generate-image` (FR-VA-013 plugado ao ciclo).
> 79	
> 80	### 2.4 Zustand Store Slices (if applicable)
> 81	
> 82	| Slice | Store file | State shape | Actions |
> 83	|-------|------------|-------------|---------|
> 84	| — | — | Nenhum store novo; estado de servidor via TanStack Query (Harness). UI local mínima no editor. | — |
> 85	
> 86	### 2.5 New DB Objects
> 87	
> 88	| Object | Type | Purpose | Migration file |
> 89	|--------|------|---------|---------------|
> 90	| `autopilot_plans` | Table | Config de cadência per-user (FR-VA-001) | `<ts>_viral_autopilot_plans.sql` |
> 91	| `autopilot_cycles` | Table | Ledger de ciclo + spend + status (FR-VA-006) | `<ts>_viral_autopilot_cycles.sql` |
> 92	| `creative_metrics` | Table | Métricas unificadas por criativo (FR-VA-009) | `<ts>_viral_autopilot_creative_metrics.sql` |
> 93	| `scheduled_posts.cycle_id` | Column | Liga post ao ciclo (NFR-VA-007 auditabilidade) | `<ts>_scheduled_posts_cycle_id.sql` |
> 94	| `autopilot-cadence` | pg_cron | Disparo recorrente */15 (FR-VA-005) | dentro da migration de cron |
> 95	| `autopilot-collect` | pg_cron | Coleta de métricas (FR-VA-008) | dentro da migration de cron |
> 96	
> 97	---
> 98	
> 99	## 3. Data Flow Diagrams
> 100	
> 101	### Use Case: Ciclo autônomo a cada N dias (FR-VA-005 → FR-VA-011)
> 102	
> 103	```
> 104	pg_cron        cadence-cron        autopilot-run        orchestrate-*        DB / External
> 105	 │ (*/15)          │                    │                    │                   │
> 106	 │──[tick]────────▶│                    │                    │                   │
> 107	 │                 │──[plans due?]──────────────────────────────────────────────▶│ SELECT is_active AND next_run_at<=now
> 108	 │                 │◀──[plan X]──────────────────────────────────────────────────│
> 109	 │                 │──[POST X-Cron]────▶│                    │                   │
> 110	 │                 │                    │──[cost gate]──────────────────────────▶│ project cost vs budget_cap + balance
> 111	 │                 │                    │  (abort if over → aborted_budget, pause)│
> 112	 │                 │                    │──[read policy]────────────────────────▶│ optimization_policy (ciclo N-1)
> 113	 │                 │                    │──[select product]─────────────────────▶│ vm_affiliate_products (comm+trend)
> 114	 │                 │                    │──[open cycle]─────────────────────────▶│ autopilot_cycles (running)
> 115	 │                 │                    │──[fan-out/product×rede]─▶│              │
> 116	 │                 │                    │                    │──[gen product-aware + feedback]─▶ LLM (BYOK)
> 117	 │                 │                    │                    │──[monetize all formats]────────▶ affiliate_links + content_variant_id
> 118	 │                 │                    │                    │──[schedule]────────────────────▶ scheduled_posts (cycle_id)
> 119	 │                 │◀──[re-arm next_run_at = now + interval]──────────────────────│
> 120	 │                 │                    │                    │   (auto-publish cron drains scheduled_posts → publish-*)
> 121	 │                 │ (later) autopilot-collect: post_id → insights → creative_metrics
> 122	 │                 │ (post-cycle) autopilot-analyze: creative_metrics(N) → optimization_policy(N) [feeds cycle N+1]
> 123	```
> 124	
> 125	---
> 126	
> 127	## 4. API Contract Definitions
> 128	
> 129	> Toda Edge Function user-facing valida JWT antes de qualquer lógica. Crons usam service-role com `verify_jwt=false` (padrão pg_net do projeto — ver SOP `orchestrate-async-pipeline`).
> 130	
> 131	### `POST /functions/v1/autopilot-run`
> 132	
> 133	```typescript
> 134	// Request
> 135	interface AutopilotRunRequest {
> 136	  plan_id: string
> 137	  mode_override?: 'all_at_once' | 'every_n_days'
> 138	  dry_run?: boolean   // true → retorna projected_cost_mco sem deduzir/publicar
> 139	}
> 140	
> 141	// Response (HTTP 200)
> 142	interface AutopilotRunResponse {
> 143	  status: 'ok'
> 144	  cycle_id: string
> 145	  cycle_number: number
> 146	  projected_cost_mco: number
> 147	  dispatched: { product_id: string; platform: string; run_id: string }[]
> 148	}
> 149	
> 150	// Cost gate (FR-VA-007) — BEFORE any deduction:
> 151	// → project = 10 (orchestrate) + 5 (analyze) + IMAGE_COST * creatives
> 152	// → if project > plan.budget_cap_mco → 409 aborted_budget + pause plan
> 153	// → balance check via profiles.mco_balance; if < min_balance → 402
> 154	// mcoCoins deduction happens inside each orchestrate-content sub-run (self-bill), never here.
> 155	```
> 156	
> 157	### `POST /functions/v1/autopilot-analyze`
> 158	
> 159	```typescript
> 160	interface AutopilotAnalyzeRequest { tenant_id: string; plan_id: string; previous_cycle_id: string }
> 161	interface AutopilotAnalyzeResponse {
> 162	  status: 'ok'
> 163	  optimization_policy_id: string
> 164	  has_real_data: boolean        // false → baseline used, NÃO fabrica recomendação
> 165	  top_features: { hook?: string; product_id?: string; best_hour?: number; format?: string }
> 166	}
> 167	// Deduct 5 mco (deduct_mco_coins) only when has_real_data OR explicitly configured; logged.
> 168	```
> 169	
> 170	---
> 171	
> 172	## 5. Security Design
> 173	
> 174	### 5.1 Threat Model (STRIDE)
> 175	
> 176	| Component | Threat | Type | Severity | Mitigation |
> 177	|-----------|--------|------|----------|------------|
> 178	| `autopilot-run` | Acesso não autenticado / disparo por terceiro | Spoofing | High | JWT no path user; `X-Cron-Trigger` + service-role no path cron; valida `plan.user_id = auth.uid()` |
> 179	| `autopilot-cadence-cron` | Falsificação de trigger de cron (disparo forçado) | Spoofing/Elevation | High | `verify_jwt=false` + service-role key; sem path público que dispare ciclo arbitrário; rate por plano via `next_run_at` |
> 180	| `autopilot_plans`/`_cycles`/`creative_metrics` | Leitura/escrita cross-tenant | Information Disclosure | Critical | RLS `user_id = auth.uid()`; crons usam service-role com filtro explícito por tenant |
> 181	| Cost gate | Bypass do teto (disparo paralelo p/ exceder) | Tampering | Critical | Gate atômico server-side ANTES do deduct; idempotência (plan_id, cycle_number); lock otimista no ciclo |
> 182	| Gerador product-aware | Prompt injection via nome/desc de produto ou trend | Tampering/Elevation | High | Cyber-Sentinel no input + no output; sanitização do produto antes do prompt |
> 183	| `affiliate_links` | Injeção de link malicioso / open-redirect | Tampering | High | Guarda de domínio ML já existente em `process-affiliate-link`; `content_variant_id` assinado por ciclo |
> 184	| Conteúdo autônomo | Publicação off-brand / viola ToS | Repudiation/Reputation | High | Cyber-Sentinel gate pré-publicação; HITL opcional (PR-VA-013); disclosure de afiliado |
> 185	| `autopilot-collect` | Vazamento de PII de engajamento na tabela global-read | Information Disclosure | Medium | Só agregados em `creative_metrics`; sem PII de terceiros; RLS own |
> 186	
> 187	### 5.2 RLS Policy Definitions
> 188	
> 189	```sql
> 190	-- autopilot_plans RLS (espelhar em autopilot_cycles, creative_metrics)
> 191	ALTER TABLE public.autopilot_plans ENABLE ROW LEVEL SECURITY;
> 192	
> 193	CREATE POLICY "autopilot_plans_select_own"
> 194	  ON public.autopilot_plans FOR SELECT
> 195	  USING (user_id = auth.uid());
> 196	
> 197	CREATE POLICY "autopilot_plans_insert_own"
> 198	  ON public.autopilot_plans FOR INSERT
> 199	  WITH CHECK (user_id = auth.uid());
> 200	
> 201	CREATE POLICY "autopilot_plans_update_own"
> 202	  ON public.autopilot_plans FOR UPDATE
> 203	  USING (user_id = auth.uid())
> 204	  WITH CHECK (user_id = auth.uid());
> 205	
> 206	-- DELETE bloqueado para authenticated (RESTRICTIVE); só service_role gerencia ciclos/spend.
> 207	```
> 208	
> 209	### 5.3 JWT Validation Points
> 210	
> 211	```typescript
> 212	// autopilot-run (user path):
> 213	const authHeader = req.headers.get('Authorization')
> 214	if (!authHeader) return new Response('Unauthorized', { status: 401 })
> 215	const { data: { user }, error } = await supabase.auth.getUser(authHeader.replace('Bearer ', ''))
> 216	if (error || !user) return new Response('Unauthorized', { status: 401 })
> 217	// then: assert plan.user_id === user.id  (cross-tenant guard)
> 218	
> 219	// cron path: header X-Cron-Trigger + SB_SECRET_KEY (service-role client); verify_jwt=false in config.toml
> 220	```
> 221	
> 222	### 5.4 Secrets Inventory
> 223	
> 224	| Secret Name | Used In | Vault Location | Rotation Policy |
> 225	|-------------|---------|----------------|----------------|
> 226	| `SB_SECRET_KEY` | crons (service-role) | Supabase Vault | per incident (legada `SUPABASE_SERVICE_ROLE_KEY` REVOGADA) |
> 227	| LLM key (Groq/OpenRouter/Gemini) | `orchestrate-step`, `autopilot-analyze` | `user_api_keys` (per-user) → vault fallback | per-user controlado |
> 228	| ML `affiliate_tag`/`matt_tool` | `_shared/affiliate.ts`, `process-affiliate-link` | `affiliate_config` (per-user) | per-user |
> 229	| Social tokens (LinkedIn/X/Meta) | `publish-*`, `autopilot-collect` | `social_credentials`/`meta_config` (per-user) | OAuth refresh |
> 230	| `MP_WEBHOOK_SECRET` | `handle-ml-postback` | Vault (global hoje → per-user em OTD-VA-007) | OTD-ML-MP-PER-USER |
> 231	
> 232	> ⚠️ NUNCA commitar valores de segredo. Só nomes de chave aparecem na documentação. Usar `SB_SECRET_KEY` (legada revogada — ver `reference_supabase_keys_migrated`).
> 233	
> 234	---
> 235	
> 236	## 6. Infrastructure Touchpoints
> 237	
> 238	| Infrastructure | Usage | Impact |
> 239	|----------------|-------|--------|
> 240	| `pg_cron` | 2 novos jobs (`autopilot-cadence` */15, `autopilot-collect`) | Soma a `memory_decay_fsrs` + `nurture-advance`; preservar os existentes |
> 241	| `mega-brain-daemon` | Consome eventos `viral_autopilot_*` de `infra_health_logs` p/ self-heal | Watchdog telemetry |
> 242	| `infra_health_logs` | Novos `event`: `viral_autopilot_cycle_started/completed/aborted_budget/collect_failure/analyze_empty` | Telemetria allowlist (não vazar per-tenant na tabela global-read) |
> 243	| `mcorch_nodes`/`_edges` | Observation node por ciclo + edge `OPTIMIZES_FROM` (ciclo N+1 → N) | GraphRAG memória de campanhas |
> 244	| ChromaDB (`mcorch_chroma`) | Não usado diretamente nesta fase | — |
> 245	
> 246	---
> 247	
> 248	## 7. Migration Stubs
> 249	
> 250	```sql
> 251	-- Migration: <ts>_viral_autopilot_plans.sql
> 252	CREATE TABLE public.autopilot_plans (
> 253	  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,
> 254	  user_id         uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
> 255	  project_id      uuid,                                  -- tenant scope opcional
> 256	  name            text NOT NULL,
> 257	  mode            text NOT NULL CHECK (mode IN ('all_at_once','every_n_days')),
> 258	  interval_days   int CHECK (interval_days BETWEEN 1 AND 30),  -- req. se every_n_days
> 259	  target_product_ids text[] NOT NULL CHECK (cardinality(target_product_ids) >= 1),
> 260	  platforms       text[] NOT NULL CHECK (cardinality(platforms) >= 1),
> 261	  budget_cap_mco  int NOT NULL CHECK (budget_cap_mco > 0),
> 262	  min_balance_mco int NOT NULL DEFAULT 10,
> 263	  is_active       boolean NOT NULL DEFAULT false,
> 264	  next_run_at     timestamptz,
> 265	  created_at      timestamptz NOT NULL DEFAULT now(),
> 266	  updated_at      timestamptz NOT NULL DEFAULT now()
> 267	);
> 268	ALTER TABLE public.autopilot_plans ENABLE ROW LEVEL SECURITY;
> 269	-- (RLS policies from §5.2)
> 270	CREATE INDEX autopilot_plans_user_idx ON public.autopilot_plans (user_id);
> 271	CREATE INDEX autopilot_plans_due_idx  ON public.autopilot_plans (next_run_at) WHERE is_active;
> 272	
> 273	-- Migration: <ts>_viral_autopilot_cycles.sql
> 274	CREATE TABLE public.autopilot_cycles (
> 275	  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,
> 276	  plan_id         uuid REFERENCES public.autopilot_plans(id) ON DELETE CASCADE NOT NULL,
> 277	  user_id         uuid NOT NULL,                         -- denormalized for RLS
> 278	  cycle_number    int NOT NULL,
> 279	  status          text NOT NULL DEFAULT 'running'
> 280	                    CHECK (status IN ('running','completed','aborted_budget','failed')),
> 281	  spend_mco       int NOT NULL DEFAULT 0,
> 282	  planned_units   int NOT NULL DEFAULT 0,
> 283	  analysis_node_id uuid,                                 -- mcorch_nodes observation
> 284	  started_at      timestamptz NOT NULL DEFAULT now(),
> 285	  completed_at    timestamptz,
> 286	  UNIQUE (plan_id, cycle_number)                         -- idempotência (NFR-VA-003)
> 287	);
> 288	ALTER TABLE public.autopilot_cycles ENABLE ROW LEVEL SECURITY;
> 289	-- SELECT own; INSERT/UPDATE service-role only.
> 290	
> 291	-- Migration: <ts>_viral_autopilot_creative_metrics.sql
> 292	CREATE TABLE public.creative_metrics (
> 293	  id                 uuid DEFAULT gen_random_uuid() PRIMARY KEY,
> 294	  user_id            uuid NOT NULL,
> 295	  cycle_id           uuid REFERENCES public.autopilot_cycles(id) ON DELETE CASCADE,
> 296	  content_variant_id uuid NOT NULL,
> 297	  product_id         text,
> 298	  platform           text,
> 299	  source             text NOT NULL CHECK (source IN ('affiliate_click','organic','postback')),
> 300	  impressions        int NOT NULL DEFAULT 0,
> 301	  engagements        int NOT NULL DEFAULT 0,
> 302	  affiliate_clicks   int NOT NULL DEFAULT 0,
> 303	  revenue_cents      int NOT NULL DEFAULT 0,
> 304	  collected_at       timestamptz NOT NULL DEFAULT now(),
> 305	  UNIQUE (content_variant_id, source)                    -- upsert idempotente por fonte
> 306	);
> 307	ALTER TABLE public.creative_metrics ENABLE ROW LEVEL SECURITY;
> 308	-- SELECT own; INSERT/UPDATE service-role only (coletor).
> 309	
> 310	-- Migration: <ts>_scheduled_posts_cycle_id.sql
> 311	ALTER TABLE public.scheduled_posts ADD COLUMN IF NOT EXISTS cycle_id uuid
> 312	  REFERENCES public.autopilot_cycles(id) ON DELETE SET NULL;
> 313	CREATE INDEX scheduled_posts_cycle_idx ON public.scheduled_posts (cycle_id);
> 314	```
> 315	
> 316	> Nenhuma tabela aqui carrega `embedding` (não são nós de conhecimento diretos). A memória GraphRAG entra via `mcorch_nodes` observation por ciclo (ver `06-data-model.md` §4). Toda migration passa `/security-review` antes do commit (FMEA-011).
> 317	
> 318	---
> 319	
> 320	## 8. Open Technical Decisions
> 321	
> 322	| ID | Description | Option A | Option B | Recommendation | Owner |
> 323	|----|-------------|----------|----------|----------------|-------|
> 324	| OTD-VA-001 | Tabela de métricas | Estender `campaign_metrics` (campaign-level) | Nova `creative_metrics` (por content_variant_id) | **B** — granularidade por criativo é pré-req de R3; ETL agrega p/ campaign_metrics | Sovereign |
> 325	| OTD-VA-002 | Infra de cron | pg_cron (como `nurture-advance`) | OS crontab (como `auto-publish`) | **A** — pg_cron service-role, consistente com o cron de cadência existente | Sovereign |
> 326	| OTD-VA-003 | Fonte de engajamento orgânico | Só cliques de afiliado (sempre disponível) | + insights de API por rede (tier-dependente) | **Ambos faseado** — cliques no MVP; orgânico best-effort gated por tier (Twitter Basic, LinkedIn, Meta) | Sovereign |
> 327	| OTD-VA-004 | Unidade do teto de custo | Por ciclo (no plano) | Diário global por tenant | **Ambos** — cap por ciclo (plano) + safety diário global espelhando `vision-mcp` | Sovereign |
> 328	| OTD-VA-005 | Reinjeção de feedback | Texto cru do `optimization_policy` no prompt | Features estruturadas (top hook/produto/horário/formato) | **B** — estruturado mantém o prompt enxuto e auditável | Sovereign |
> 329	| OTD-VA-006 | Autonomia de seleção de produto | Auto-score por comissão+trend | Shortlist curada pelo Sovereign | **Shortlist (3 SKUs) no MVP** (Decisão 4); auto-score em v1.0 (PR-VA-010) | Decidido |
> 330	| OTD-VA-007 | Secret de postback per-user (herdada `OTD-ML-MP-PER-USER`) | Manter secret global (Usuário Zero) | Per-user `meta`/MP config | **B antes de multi-tenant** — atribuição de receita por tenant exige secret per-user | Sovereign |
> 331	
> 332	---
> 333	
> 334	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 335	
> ```

## 🤖 Claude *(21:09:20)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/07-process-flow.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Process & Automation Blueprint
> 2	
> 3	**Project:** viral-autopilot  
> 4	**Version:** v0.1 | **Date:** 2026-06-17  
> 5	**BoK Applied:** BPM CBOK v4 (Process Modeling + Process Design)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Process Inventory
> 11	
> 12	| Process ID | Name | Type | Trigger | Owner | SLA |
> 13	|------------|------|------|---------|-------|-----|
> 14	| PROC-VA-001 | Ciclo autônomo de cadência | cron | pg_cron `autopilot-cadence` */15 → plano due | System | ciclo dispara em ≤ 15min após `next_run_at` |
> 15	| PROC-VA-002 | Disparo "tudo de uma vez" | human-in-loop | Operador clica "Gerar agora" na UI | User | resposta < 5min p95 (fan-out) |
> 16	| PROC-VA-003 | Coleta de desempenho | cron | pg_cron `autopilot-collect` (horário) | System | métrica coletada ≤ 24h após publicação |
> 17	| PROC-VA-004 | Kill-switch de custo | event-driven | custo projetado > teto OU saldo < piso | System | aborta antes de qualquer deduct |
> 18	| PROC-VA-005 | Análise + reinjeção de aprendizado | automated | pós-ciclo (encadeado a PROC-VA-001) | System | `optimization_policy` pronto antes do próximo ciclo |
> 19	
> 20	---
> 21	
> 22	## 2. BPMN-lite Process Maps
> 23	
> 24	### PROC-VA-001: Ciclo autônomo de cadência
> 25	
> 26	```
> 27	START (cron tick */15)
> 28	   │
> 29	[autopilot-cadence-cron: SELECT plans is_active AND next_run_at<=now]
> 30	   │
> 31	<Gateway: há plano due?>
> 32	   │ NO ──▶ END (no-op)
> 33	   │ YES
> 34	[autopilot-run(plan, X-Cron-Trigger)]
> 35	   │
> 36	[Cost gate: projetar 10 + 5 + img×criativos]
> 37	   │
> 38	<Gateway: custo ≤ budget_cap AND saldo ≥ min_balance?>
> 39	   │ NO ──▶ [status=aborted_budget] ──▶ [pause plan] ──▶ [infra_health_logs: viral_autopilot_aborted_budget] ──▶ [notify PT-BR] ──▶ END
> 40	   │ YES
> 41	[read optimization_policy (ciclo N-1)]  →  [select product (comm+trend / seed)]  →  [open autopilot_cycles (running)]
> 42	   │
> 43	[fan-out por produto×rede → orchestrate-content (forward JWT, self-bill)]
> 44	   │
> 45	   ├──[orchestrate-step: gerar product-aware + injetar feedback]
> 46	   ├──[monetize ALL formats → affiliate_links + content_variant_id]
> 47	   ├──[generate-image product-referenced → asset]
> 48	   └──[insert scheduled_posts (cycle_id)]
> 49	   │
> 50	[re-arm: next_run_at = now + interval_days]   (auto-refill)
> 51	   │
> 52	[Insert mcorch_node observation + edge OPTIMIZES_FROM → ciclo N-1]
> 53	   │
> 54	END  (auto-publish cron drena scheduled_posts → publish-*; PROC-VA-003 coleta depois)
> 55	```
> 56	
> 57	**Swimlanes:**
> 58	
> 59	| Swimlane | Participant | Tasks |
> 60	|----------|-------------|-------|
> 61	| Scheduler | pg_cron + `autopilot-cadence-cron` | tick, encontrar planos due, re-armar next_run_at |
> 62	| Edge Function | `autopilot-run` | cost gate, seleção de produto, abrir ciclo, fan-out |
> 63	| Generation | `orchestrate-content`→`orchestrate-step` + `_shared/affiliate.ts` + `generate-image` | gerar product-aware, monetizar, agendar |
> 64	| External API | LLM (BYOK), DALL·E/Nano Banana, redes (via auto-publish) | gerar texto/imagem, publicar |
> 65	| DB | Supabase | autopilot_cycles, scheduled_posts, affiliate_links, mcorch_nodes |
> 66	
> 67	---
> 68	
> 69	### PROC-VA-002: Disparo "tudo de uma vez" (HITL)
> 70	
> 71	```
> 72	[User Action: clica "Gerar agora" (mode=all_at_once)]
> 73	  │
> 74	  ▼
> 75	[Hook: useAutopilot → invoke autopilot-run { plan_id, dry_run:true }]
> 76	  │
> 77	  ▼
> 78	[Edge Fn: autopilot-run]
> 79	  ├── Validate JWT ──(fail)──▶ HTTP 401
> 80	  ├── assert plan.user_id == auth.uid() ──(fail)──▶ HTTP 403
> 81	  ├── Cost gate (projeção) ──(over)──▶ HTTP 409 → Toast: "Teto de custo insuficiente para este ciclo"
> 82	  ├── return projected_cost_mco  (dry_run)
> 83	  │
> 84	  ▼
> 85	[UI mostra custo projetado + confirmação]
> 86	  │
> 87	  ▼ (usuário confirma)
> 88	[invoke autopilot-run { plan_id, dry_run:false }]
> 89	  ├── deduct ocorre nos sub-runs (self-bill via orchestrate-content)
> 90	  ├── fan-out todos os criativos AGORA (Promise.allSettled)
> 91	  ├── Embed observation node via embed-mcorch-node
> 92	  └── HTTP 200 → React Query invalida ['autopilot-cycles'] → UI refresh
> 93	```
> 94	
> 95	---
> 96	
> 97	### PROC-VA-003: Coleta de desempenho
> 98	
> 99	```
> 100	START (cron autopilot-collect, horário)
> 101	  │
> 102	[SELECT scheduled_posts status='published' AND cycle_id NOT NULL AND metrics_pending]
> 103	  │
> 104	[para cada post: resolve post_id + plataforma]
> 105	  │
> 106	<Gateway: API de insights disponível p/ a rede/tier?>
> 107	  │ NO  ──▶ [registrar só affiliate_clicks do click ledger] (sinal sempre disponível)
> 108	  │ YES ──▶ [fetch insights (likes/views/shares) best-effort]
> 109	  │
> 110	[UPSERT creative_metrics (content_variant_id, source) — idempotente]
> 111	  │
> 112	[merge revenue: handle-ml-postback já creditou affiliate_links → refletir revenue_cents]
> 113	  │
> 114	END  (alimenta PROC-VA-005)
> 115	```
> 116	
> 117	---
> 118	
> 119	## 3. n8n Workflow Blueprints
> 120	
> 121	> O `viral-autopilot` usa **pg_cron + Edge Functions** como motor primário (consistente com `nurture-advance`). n8n é opcional como camada de notificação/observação externa.
> 122	
> 123	### Workflow: Autopilot Cycle Alert (opcional)
> 124	
> 125	**Trigger:** Supabase webhook em `infra_health_logs` (event `viral_autopilot_aborted_budget` ou `_collect_failure`)  
> 126	**Idempotency key:** `infra_health_logs.id`
> 127	
> 128	```
> 129	[Trigger: webhook infra_health_logs (autopilot event)]
> 130	  │
> 131	  ▼
> 132	[Node: Filter event_type IN (aborted_budget, collect_failure, analyze_empty)]
> 133	  │
> 134	  ├── (aborted_budget) ──▶ [Node: Telegram @claw_gcrux "Plano <x> pausado — teto de custo"]
> 135	  │
> 136	  └── (collect_failure) ──▶ [Node: Set retry; (count>3) → infra_health_logs {n8n_alert}]
> 137	```
> 138	
> 139	**Data Mapping:**
> 140	
> 141	| Input Field | Source | → | Output Field | Destination |
> 142	|-------------|--------|---|--------------|-------------|
> 143	| `event` | infra_health_logs row | → | message | Telegram body |
> 144	| `metadata.plan_id` | infra_health_logs row | → | context | Telegram body |
> 145	
> 146	---
> 147	
> 148	## 4. Orchestration Integration Points
> 149	
> 150	> O `viral-autopilot` é um **wrapper sobre `orchestrate-content`**, não um novo passo dentro dele. O ciclo dispara N execuções de `orchestrate-content` (uma por produto×rede), cada uma com `product_target` injetado.
> 151	
> 152	| Pipeline Step | Step ID | Position | Description | mcoCoins Trigger |
> 153	|---------------|---------|----------|-------------|-----------------|
> 154	| `product_target` injection | n/a (param) | entrada do orchestrate-content | `autopilot-run` passa `{ product_id, product_meta, feedback_features }` que hoje é dropado (FR-VA-016) | — |
> 155	| `monetize_all_formats` | dentro de orchestrate-step | após cada formato (article/linkedin/twitter) | `_shared/affiliate.ts` embute link ML + content_variant_id (FR-VA-004) | 0 |
> 156	| `feedback_inject` | dentro de orchestrate-step | antes da chamada LLM | injeta features do `optimization_policy` no system prompt (FR-VA-011) | 0 |
> 157	
> 158	**Integration code stub (dentro de `autopilot-run/index.ts`):**
> 159	```typescript
> 160	// Para cada produto-alvo × rede do plano:
> 161	for (const product of selectedProducts) {
> 162	  for (const platform of plan.platforms) {
> 163	    await updateCycleStatus(cycleId, 'running')
> 164	    const run = await supabase.functions.invoke('orchestrate-content', {
> 165	      headers: { Authorization: userJwt },     // self-bill no tenant
> 166	      body: {
> 167	        topic: buildViralAngle(product, trends),   // FR-VA-018
> 168	        product_target: { id: product.external_id, meta: product, feedback: policyFeatures }, // FR-VA-016
> 169	        platforms: [platform],
> 170	        cycle_id: cycleId,                          // NFR-VA-007 auditabilidade
> 171	      },
> 172	    })
> 173	    if (!run.data?.ok) await logHealth('viral_autopilot_cycle_failed', { cycleId, platform })
> 174	  }
> 175	}
> 176	```
> 177	
> 178	---
> 179	
> 180	## 5. Error Handling & Retry Strategy
> 181	
> 182	| Process | Step | Error Type | Max Retries | Backoff | Failure Action |
> 183	|---------|------|-----------|-------------|---------|----------------|
> 184	| PROC-VA-001 | cost gate | saldo/teto insuficiente | 0 | — | `aborted_budget` + pause plan + notify (sem cobrar) |
> 185	| PROC-VA-001 | fan-out orchestrate-content | sub-run 5xx | 2 | Fixo 5s | marcar criativo failed; ciclo segue (Promise.allSettled) |
> 186	| PROC-VA-001 | re-arm next_run_at | DB error | 3 | Exp (2s,4s,8s) | infra_health_logs; cron retenta no próximo tick (idempotente por cycle_number) |
> 187	| PROC-VA-003 | fetch insights | API tier/timeout | 1 | Fixo | fallback p/ só affiliate_clicks; log `collect_failure` |
> 188	| PROC-VA-005 | analyze | LLM timeout / métricas vazias | 1 | — | se vazio: baseline (`has_real_data=false`), NÃO inventa; log `analyze_empty` |
> 189	| Qualquer | JWT validation | token inválido | 0 | — | HTTP 401 imediato |
> 190	
> 191	---
> 192	
> 193	## 6. SLA Definitions
> 194	
> 195	| Process | Step | Expected Duration | Timeout Threshold | Alert if exceeded |
> 196	|---------|------|------------------|-------------------|-------------------|
> 197	| PROC-VA-001 | ciclo end-to-end (N≤8 criativos) | < 5min | 15min | Sim → infra_health_logs `sla_breach` |
> 198	| PROC-VA-001 | cost gate | < 1s | 5s | Não |
> 199	| PROC-VA-002 | autopilot-run (dry_run) | < 2s | 5s | Sim |
> 200	| PROC-VA-003 | coleta por post | < 3s | 30s | Não (best-effort) |
> 201	| PROC-VA-005 | analyze | < 10s | 60s | Sim |
> 202	
> 203	---
> 204	
> 205	## 7. Cron Jobs
> 206	
> 207	| Job Name | Schedule (cron) | Function | Idempotency | Failure Alerting |
> 208	|----------|----------------|----------|-------------|-----------------|
> 209	| `autopilot-cadence` | `*/15 * * * *` | `autopilot-cadence-cron` | re-arm de `next_run_at` + UNIQUE (plan_id, cycle_number) ⇒ re-fire não duplica | `infra_health_logs` + Telegram (n8n opcional) |
> 210	| `autopilot-collect` | `0 */6 * * *` (6/6h) | `autopilot-collect` | UPSERT (content_variant_id, source) | `infra_health_logs` `collect_failure` |
> 211	
> 212	> **Preservar crons existentes:** `memory_decay_fsrs`, `nurture-advance` (*/15), `watchdog-mcorch` (*/5), `auto-publish` (*/5), `audit-4cs`, `affiliate-enrich-cron` (6/6h). Os 2 novos jobs são adicionais.
> 213	> **Idempotência (NFR-VA-003):** re-rodar o cron sobre o mesmo `next_run_at`/ciclo produz o mesmo resultado — o ciclo já aberto (UNIQUE plan_id+cycle_number) bloqueia duplicata; janela perdida faz catch-up no próximo tick sem dobrar.
> 214	
> 215	---
> 216	
> 217	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 218	
> ```

## 🤖 Claude *(21:09:24)*

Now let me read the data-model and index to complete the artifact verification.

## 🤖 Claude *(21:09:24)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/06-data-model.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Data & Knowledge Model
> 2	
> 3	**Project:** viral-autopilot  
> 4	**Version:** v0.1 | **Date:** 2026-06-17  
> 5	**BoK Applied:** DMBOK v2 (Data Modeling & Design + Data Quality)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Conceptual Data Model
> 11	
> 12	```
> 13	[autopilot_plans] ──(1:N)──▶ [autopilot_cycles] ──(1:N)──▶ [creative_metrics]
> 14	       │                            │                              │
> 15	       │ (references)               │ (cycle_id on)                │ (content_variant_id)
> 16	       ▼                            ▼                              ▼
> 17	[vm_affiliate_products]      [scheduled_posts] ──(N:1)──▶ [content_library]
> 18	       │                            │                              │
> 19	       └──(promotes)──▶ [affiliate_links] ◀──(revenue)── [handle-ml-postback]
> 20	                                    │
> 21	                                    └──(1:1 observation)──▶ [mcorch_nodes] ──OPTIMIZES_FROM──▶ [mcorch_nodes]
> 22	```
> 23	
> 24	**Entities:**
> 25	- **autopilot_plans:** configuração de cadência per-user (modo, intervalo, produtos-alvo, redes, teto de custo). Fonte da verdade do "o quê e quando".
> 26	- **autopilot_cycles:** instância de execução de um plano (ledger: status, spend, planned_units, ponteiro p/ análise). Idempotente por (plan_id, cycle_number).
> 27	- **creative_metrics:** desempenho por criativo (`content_variant_id`), unificando cliques de afiliado + engajamento orgânico + receita de postback (Decisão 3).
> 28	- **vm_affiliate_products (reuse):** catálogo ML com `commission_value`/`trend_score`/`profitability_score`/`image_url` — fonte do produto-alvo.
> 29	- **scheduled_posts (reuse + `cycle_id`):** fila de publicação; agora rastreável ao ciclo.
> 30	- **affiliate_links / optimization_policy / content_library / mcorch_nodes (reuse):** receita, política de melhoria, conteúdo, memória.
> 31	
> 32	---
> 33	
> 34	## 2. Logical Data Model
> 35	
> 36	### Table: `autopilot_plans`
> 37	
> 38	| Column | Type | Nullable | Default | FK | Description |
> 39	|--------|------|----------|---------|-----|------------|
> 40	| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | — | PK |
> 41	| `user_id` | `uuid` | NOT NULL | — | `auth.users.id` | Tenant isolation |
> 42	| `project_id` | `uuid` | NULL | — | — | Project scope opcional |
> 43	| `name` | `text` | NOT NULL | — | — | Nome do plano |
> 44	| `mode` | `text` | NOT NULL | — | — | `all_at_once` \| `every_n_days` |
> 45	| `interval_days` | `int` | NULL | `3` | — | Req. se `every_n_days`; 1–30 |
> 46	| `target_product_ids` | `text[]` | NOT NULL | — | → `vm_affiliate_products.external_id` | ≥ 1 produto |
> 47	| `platforms` | `text[]` | NOT NULL | — | — | ⊆ {wordpress,linkedin,twitter} (MVP) |
> 48	| `budget_cap_mco` | `int` | NOT NULL | — | — | Teto de custo por ciclo |
> 49	| `min_balance_mco` | `int` | NOT NULL | `10` | — | Piso de saldo p/ disparar |
> 50	| `is_active` | `boolean` | NOT NULL | `false` | — | Cadência ligada |
> 51	| `next_run_at` | `timestamptz` | NULL | — | — | Próximo disparo (cron) |
> 52	| `created_at` | `timestamptz` | NOT NULL | `now()` | — | Audit |
> 53	| `updated_at` | `timestamptz` | NOT NULL | `now()` | — | Audit |
> 54	
> 55	### Table: `autopilot_cycles`
> 56	
> 57	| Column | Type | Nullable | Default | FK | Description |
> 58	|--------|------|----------|---------|-----|------------|
> 59	| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | — | PK |
> 60	| `plan_id` | `uuid` | NOT NULL | — | `autopilot_plans.id` | Plano pai |
> 61	| `user_id` | `uuid` | NOT NULL | — | — | Denormalizado p/ RLS |
> 62	| `cycle_number` | `int` | NOT NULL | — | — | Sequencial por plano |
> 63	| `status` | `text` | NOT NULL | `running` | — | running\|completed\|aborted_budget\|failed |
> 64	| `spend_mco` | `int` | NOT NULL | `0` | — | mcoCoins gastos no ciclo |
> 65	| `planned_units` | `int` | NOT NULL | `0` | — | nº criativos planejados |
> 66	| `analysis_node_id` | `uuid` | NULL | — | `mcorch_nodes.id` | Nó de observação do ciclo |
> 67	| `started_at` | `timestamptz` | NOT NULL | `now()` | — | — |
> 68	| `completed_at` | `timestamptz` | NULL | — | — | — |
> 69	| — | — | — | — | — | **UNIQUE (plan_id, cycle_number)** |
> 70	
> 71	### Table: `creative_metrics`
> 72	
> 73	| Column | Type | Nullable | Default | FK | Description |
> 74	|--------|------|----------|---------|-----|------------|
> 75	| `id` | `uuid` | NOT NULL | `gen_random_uuid()` | — | PK |
> 76	| `user_id` | `uuid` | NOT NULL | — | — | Tenant isolation |
> 77	| `cycle_id` | `uuid` | NULL | — | `autopilot_cycles.id` | Ciclo de origem |
> 78	| `content_variant_id` | `uuid` | NOT NULL | — | → criativo/`content_library` | Criativo medido |
> 79	| `product_id` | `text` | NULL | — | → `vm_affiliate_products` | Produto promovido |
> 80	| `platform` | `text` | NULL | — | — | Rede |
> 81	| `source` | `text` | NOT NULL | — | — | affiliate_click\|organic\|postback |
> 82	| `impressions` | `int` | NOT NULL | `0` | — | — |
> 83	| `engagements` | `int` | NOT NULL | `0` | — | likes/shares/comments |
> 84	| `affiliate_clicks` | `int` | NOT NULL | `0` | — | do click ledger |
> 85	| `revenue_cents` | `int` | NOT NULL | `0` | — | do postback |
> 86	| `collected_at` | `timestamptz` | NOT NULL | `now()` | — | — |
> 87	| — | — | — | — | — | **UNIQUE (content_variant_id, source)** |
> 88	
> 89	> Nenhuma das 3 tabelas carrega `embedding`/`stability_score` — não são nós de conhecimento diretos. A memória semântica entra via `mcorch_nodes` (§4).
> 90	
> 91	---
> 92	
> 93	## 3. Supabase Physical Schema Stubs
> 94	
> 95	```sql
> 96	-- ============================================================
> 97	-- MIGRATION: <ts>_viral_autopilot_schema.sql  (split em 4 arquivos — ver 05-sdd §7)
> 98	-- ============================================================
> 99	-- autopilot_plans / autopilot_cycles / creative_metrics + ALTER scheduled_posts
> 100	-- (stubs CREATE TABLE completos em 05-sdd.md §7)
> 101	
> 102	-- RLS (default-deny → own-row)
> 103	ALTER TABLE public.autopilot_plans     ENABLE ROW LEVEL SECURITY;
> 104	ALTER TABLE public.autopilot_cycles    ENABLE ROW LEVEL SECURITY;
> 105	ALTER TABLE public.creative_metrics    ENABLE ROW LEVEL SECURITY;
> 106	
> 107	CREATE POLICY "autopilot_plans: users read own"    ON public.autopilot_plans  FOR SELECT USING (user_id = auth.uid());
> 108	CREATE POLICY "autopilot_plans: users write own"   ON public.autopilot_plans  FOR INSERT WITH CHECK (user_id = auth.uid());
> 109	CREATE POLICY "autopilot_plans: users update own"  ON public.autopilot_plans  FOR UPDATE USING (user_id = auth.uid()) WITH CHECK (user_id = auth.uid());
> 110	
> 111	CREATE POLICY "autopilot_cycles: users read own"   ON public.autopilot_cycles FOR SELECT USING (user_id = auth.uid());
> 112	-- INSERT/UPDATE de cycles e creative_metrics: service_role only (coletor/runner).
> 113	CREATE POLICY "creative_metrics: users read own"   ON public.creative_metrics FOR SELECT USING (user_id = auth.uid());
> 114	
> 115	-- Índices
> 116	CREATE INDEX autopilot_plans_due_idx     ON public.autopilot_plans (next_run_at) WHERE is_active;
> 117	CREATE INDEX autopilot_cycles_plan_idx   ON public.autopilot_cycles (plan_id);
> 118	CREATE INDEX creative_metrics_cycle_idx  ON public.creative_metrics (cycle_id);
> 119	CREATE INDEX creative_metrics_variant_idx ON public.creative_metrics (content_variant_id);
> 120	
> 121	-- Updated-at trigger (reusa update_updated_at_column existente)
> 122	CREATE TRIGGER set_autopilot_plans_updated_at
> 123	  BEFORE UPDATE ON public.autopilot_plans
> 124	  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
> 125	```
> 126	
> 127	---
> 128	
> 129	## 4. GraphRAG Knowledge Nodes
> 130	
> 131	### Node Types Introduced
> 132	
> 133	| node_type | Title Pattern | Content Fields | Embedding Source |
> 134	|-----------|--------------|----------------|-----------------|
> 135	| `observation` (reuse) | `autopilot-cycle-<plan>-<n>-<date>` | resumo do ciclo: produto, redes, desempenho agregado, política aplicada | `${title} ${content}` via `embed-mcorch-node` |
> 136	
> 137	> Não introduz `node_type` novo — reusa `observation`. A novidade é o **edge** que liga ciclos para a memória de aprendizado ser navegável.
> 138	
> 139	### Edge Types Introduced
> 140	
> 141	| Edge relationship | Source node_type | Target node_type | Metadata |
> 142	|-------------------|-----------------|-----------------|----------|
> 143	| `OPTIMIZES_FROM` (new) | `observation` (ciclo N+1) | `observation` (ciclo N) | `{ lift, applied_features }` — o ciclo N+1 derivou aprendizado do ciclo N |
> 144	| `ATTRIBUTES_REVENUE_TO` (reuse) | `revenue` event | `content_mesh_asset`/criativo | `{ revenue_cents, order_id }` — atribuição por criativo |
> 145	| `PROMOTES` (new, optional) | `observation` (ciclo) | product node | `{ product_id, commission_value }` |
> 146	
> 147	### Embedding Trigger
> 148	
> 149	```typescript
> 150	// Após fechar o ciclo (autopilot-run / autopilot-analyze), insere observation node:
> 151	await supabase.functions.invoke('embed-mcorch-node', {
> 152	  body: { node_id: cycleNode.id, content: `${title} ${cycleSummary}` }
> 153	})
> 154	// O trigger trg_mcorch_embed_on_insert (pg_net) também dispara automaticamente.
> 155	```
> 156	
> 157	### FSRS-6 Parameters
> 158	
> 159	| Field | Initial Value | Decay Rule |
> 160	|-------|--------------|------------|
> 161	| `stability_score` (no `mcorch_nodes` do ciclo) | `0.7` (observação operacional relevante) | Decai por `decay_mcorch_stability()` (migration `20260425190000`) |
> 162	| `revenue_impact` (no nó do ciclo) | `SUM(creative_metrics.revenue_cents)/100` do ciclo | Atualizado quando postback credita receita atribuída ao ciclo |
> 163	
> 164	---
> 165	
> 166	## 5. Tenant Isolation Map
> 167	
> 168	| Table | `user_id` scope | `project_id` scope | System rows (user_id IS NULL) |
> 169	|-------|----------------|-------------------|-------------------------------|
> 170	| `autopilot_plans` | ✅ Required | Optional | No |
> 171	| `autopilot_cycles` | ✅ Required (denorm) | via plano | No |
> 172	| `creative_metrics` | ✅ Required | via ciclo | No |
> 173	| `scheduled_posts` (reuse) | ✅ Required (existente) | — | No |
> 174	| `vm_affiliate_products` (reuse) | catálogo compartilhado (read `USING(true)`) | — | Sim (shared) |
> 175	| `mcorch_nodes` (reuse) | Optional | Optional | Sim (system nodes) |
> 176	
> 177	---
> 178	
> 179	## 6. Data Quality Rules
> 180	
> 181	| Table | Column | Rule | Violation Message (PT-BR) |
> 182	|-------|--------|------|--------------------------|
> 183	| `autopilot_plans` | `mode` | ∈ {all_at_once, every_n_days} | "Modo de cadência inválido." |
> 184	| `autopilot_plans` | `interval_days` | 1–30; obrigatório se `every_n_days` | "Intervalo deve ser entre 1 e 30 dias." |
> 185	| `autopilot_plans` | `target_product_ids` | cardinalidade ≥ 1; ids existem no catálogo | "Selecione ao menos um produto-alvo válido." |
> 186	| `autopilot_plans` | `platforms` | ⊆ redes suportadas (MVP); ≥ 1 | "Selecione ao menos uma rede suportada." |
> 187	| `autopilot_plans` | `budget_cap_mco` | ≥ custo mínimo de 1 ciclo | "Teto de custo abaixo do mínimo de um ciclo." |
> 188	| `autopilot_cycles` | `(plan_id, cycle_number)` | UNIQUE (idempotência) | "Ciclo já existente para este plano." |
> 189	| `creative_metrics` | `(content_variant_id, source)` | UNIQUE (upsert por fonte) | — |
> 190	| `creative_metrics` | `revenue_cents`/`affiliate_clicks` | ≥ 0 | "Métrica não pode ser negativa." |
> 191	
> 192	---
> 193	
> 194	## 7. Retention & Archival Policy
> 195	
> 196	| Data | Retention Period | Archival Strategy | Deletion Trigger |
> 197	|------|-----------------|-------------------|-----------------|
> 198	| `autopilot_plans` | enquanto ativo + 1 ano | nenhum | CASCADE no delete do user (LGPD) |
> 199	| `autopilot_cycles` | 18 meses | sumário agregado em `mcorch_nodes` (observation) | CASCADE no delete do plano |
> 200	| `creative_metrics` | 18 meses | agregado por ciclo preservado no nó | CASCADE no delete do ciclo |
> 201	| `mcorch_nodes` (observation de ciclo) | Indefinido (memória) | FSRS-6 decay de stability | LGPD erase por tenant |
> 202	| `infra_health_logs` (eventos autopilot) | 90 dias | sem archival | Cron purge |
> 203	
> 204	> **LGPD:** o delete do tenant (`auth.users`) cascateia plans→cycles→creative_metrics. Métricas guardam só agregados (sem PII de terceiros que engajaram).
> 205	
> 206	---
> 207	
> 208	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 209	
> ```

## 🤖 Claude *(21:09:25)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/00-index.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# BoK Documentation Suite — viral-autopilot
> 2	
> 3	**Generated:** 2026-06-17  
> 4	**Version:** v0.1  
> 5	**Agent:** MCORCH BoK Scribe Agent v1.0.0  
> 6	**Sovereign:** Gabriel Zarattini (gabrielcall@gmail.com)
> 7	
> 8	---
> 9	
> 10	## Project Metadata
> 11	
> 12	| Field | Value |
> 13	|-------|-------|
> 14	| Business Idea | Motor de conteúdo viral autônomo: alimentar contas de redes sociais com conteúdo gerado automaticamente, agendado (tudo de uma vez OU lote a cada N dias, default 3), que a cada ciclo analisa o desempenho anterior para melhorar os próximos criativos — tudo monetizado com afiliado do Mercado Livre. |
> 15	| Market Segment | B2B2C (plataforma SaaS multi-tenant para criadores/afiliados [B2B] cujo conteúdo viral atinge consumidores [B2C]) |
> 16	| Monetization Model | hybrid (consumo de mcoCoins por ciclo/criativo + receita de comissão de afiliado ML compartilhada) |
> 17	| Regulatory Profile | LGPD (publicação de conteúdo + PII residual de engajamento + ToS de redes sociais e do Mercado Livre) |
> 18	| Integration Surface | extends-mcorch |
> 19	| Project Slug | `viral-autopilot` |
> 20	
> 21	---
> 22	
> 23	## Sovereign Directive (Source of Truth Parameters — 2026-06-17)
> 24	
> 25	Quatro requisitos-núcleo, derivados da diretiva verbal do Sovereign e travados por 4 decisões formais:
> 26	
> 27	| Req | Descrição | Estado pré-suite (auditoria 2026-06-17) |
> 28	|-----|-----------|------------------------------------------|
> 29	| **R1** | Geração automática de conteúdo para redes sociais | 🟡 parcial — pipeline de TEXTO vivo; mídia órfã |
> 30	| **R2** | Agendamento: tudo de uma vez OU lote a cada N dias (default 3) | 🟡 parcial — "tudo de uma vez" existe; recorrência NÃO existe |
> 31	| **R3** | Loop auto-melhorável: analisar o ciclo anterior → melhorar o próximo | 🔴 ausente — loop aberto em 3 quebras |
> 32	| **R4** | Conteúdo viral monetizado com comissão de afiliado do Mercado Livre | 🟡 parcial — receita ML madura, mas conteúdo product-unaware |
> 33	
> 34	**Decisões Soberanas (parâmetros fixos):**
> 35	1. **BoK Gate:** suite-mãe NOVO `viral-autopilot` que UNIFICA R1-R4 e é dono explícito do orquestrador do ciclo. Referencia/promove (sem re-documentar): `mercado-livre-api` (FR-ML-001..012), `post-engine` (FR-PE-001..004), `viral-daily-canvas` (FR-VDC-001..004), `viralmind` (FR-024..026), `marketing-hub` (FR-MH-004).
> 36	2. **MVP:** TEXTO + IMAGEM nas redes ATUAIS (WordPress/LinkedIn/Twitter-X). Vídeo 9:16 + TikTok/Instagram/YouTube = FASE 2 explícita.
> 37	3. **Sinal R3:** combo completo — (a) cliques de afiliado (click ledger já existe), (b) engajamento orgânico por post (coletor novo), (c) receita por postback ML.
> 38	4. **Produtos ML:** 3 SKUs semente (Roborock S8, Samsung Neo QLED 8K, Family Hub), com caminho de expansão de catálogo documentado.
> 39	
> 40	> **Origem:** auditoria material de 7 agentes (2026-06-17) — `project_viral_autopilot` (memória). Cada gap citado abaixo carrega prova `path:linha`. Ver `01-mrd.md` §2 e `05-sdd.md` §8 (OTDs).
> 41	
> 42	---
> 43	
> 44	## Document Registry
> 45	
> 46	| # | File | Document | BoK Applied | Status |
> 47	|---|------|----------|-------------|--------|
> 48	| 0 | `00-index.md` | Project Manifest | — | [x] complete |
> 49	| 1 | `01-mrd.md` | Market Requirements Document | BABOK v3 | [x] complete |
> 50	| 2 | `02-brd.md` | Business Requirements Document | BABOK v3 | [x] complete |
> 51	| 3 | `03-prd.md` | Product Requirements Document | ProdBOK + CXBOK | [x] complete |
> 52	| 4 | `04-frd.md` | Functional Requirements Document | SWEBOK v4 | [x] complete |
> 53	| 5 | `05-sdd.md` | System Design Document | SWEBOK v4 + CISSP CBK | [x] complete |
> 54	| 6 | `06-data-model.md` | Data & Knowledge Model | DMBOK v2 | [x] complete |
> 55	| 7 | `07-process-flow.md` | Process & Automation Blueprint | BPM CBOK v4 | [x] complete |
> 56	| 8 | `08-quality-metrics.md` | Self-Optimization Specification | CMQ/OE BOK | [x] complete |
> 57	
> 58	---
> 59	
> 60	## Traceability Chain (summary — full matrices in each doc)
> 61	
> 62	```
> 63	MR-VA-001 (geração auto) ──▶ BR-VA-001 ──▶ PR-VA-002 ──▶ FR-VA-003, FR-VA-013 ──▶ orchestrate-step (lib) | generate-image
> 64	MR-VA-002 (cadência)     ──▶ BR-VA-002 ──▶ PR-VA-001, PR-VA-003 ──▶ FR-VA-001, FR-VA-005, FR-VA-006 ──▶ autopilot_plans | autopilot-cadence-cron
> 65	MR-VA-003 (loop melhoria)──▶ BR-VA-003 ──▶ PR-VA-004, PR-VA-005 ──▶ FR-VA-008..011 ──▶ creative_metrics | cycle-analyzer | feedback-inject
> 66	MR-VA-004 (afiliado ML)  ──▶ BR-VA-004 ──▶ PR-VA-002 ──▶ FR-VA-004, FR-VA-016 ──▶ _shared/affiliate.ts | process-affiliate-link
> 67	MR-VA-005 (ROI/criativo) ──▶ BR-VA-005 ──▶ PR-VA-007 ──▶ FR-VA-009, FR-VA-017 ──▶ creative_metrics | handle-ml-postback
> 68	MR-VA-006 (custo)        ──▶ BR-VA-006 ──▶ PR-VA-006 ──▶ FR-VA-007 ──▶ autopilot_cycles | deduct_mco_coins
> 69	MR-VA-007 (multi-tenant) ──▶ BR-VA-007 ──▶ PR-VA-001 ──▶ FR-VA-001, NFR-VA-004 ──▶ affiliate_config (RLS auth.uid())
> 70	MR-VA-008 (sinal viral)  ──▶ BR-VA-008 ──▶ PR-VA-010, PR-VA-011 ──▶ FR-VA-012, FR-VA-018 ──▶ vm_affiliate_products | fetch-trends
> 71	```
> 72	
> 73	---
> 74	
> 75	## Phase Completion Log
> 76	
> 77	| Phase | Name | Completed | Notes |
> 78	|-------|------|-----------|-------|
> 79	| 0 | Project Bootstrap | 2026-06-17 | Slug `viral-autopilot`; inputs derived from Sovereign directive |
> 80	| 1 | Market & Business Intelligence | 2026-06-17 | MRD + BRD — 8 MR, 8 BR, ROI model |
> 81	| 2 | Product Definition | 2026-06-17 | PRD — 2 personas, MoSCoW (MVP=texto+imagem) |
> 82	| 3 | Technical Specification | 2026-06-17 | FRD (18 FR + 8 NFR) + SDD (STRIDE, RLS, 7 OTD) |
> 83	| 4 | Data & Process Engineering | 2026-06-17 | 3 novas tabelas + 4 processos + 2 crons |
> 84	| 5 | Quality & Autonomic Engineering | 2026-06-17 | 12 FMEA (4 RPN>100), kill-switch self-heal |
> 85	| 6 | Traceability Validation | 2026-06-17 | Adversarial workflow — ver seal report |
> 86	| 7 | Knowledge Mesh Injection | [ ] | `scripts/seed-viral-autopilot-bok-seal.ts` (pendente exec sob aprovação) |
> 87	
> 88	---
> 89	
> 90	## Open Technical Decisions (consolidated — detail in `05-sdd.md` §8)
> 91	
> 92	| OTD ID | Description | Recommendation | Status |
> 93	|--------|-------------|----------------|--------|
> 94	| OTD-VA-001 | `campaign_metrics` (campaign-level) vs `creative_metrics` (por content_variant_id) | Nova `creative_metrics`; ETL agrega p/ campaign_metrics | Open |
> 95	| OTD-VA-002 | Cron infra: pg_cron (nurture-advance) vs OS crontab (auto-publish) | pg_cron service-role por consistência | Open |
> 96	| OTD-VA-003 | Fonte de engajamento orgânico (LinkedIn/Twitter API tier) | Cliques de afiliado primeiro (já temos); orgânico best-effort gated por tier | Open |
> 97	| OTD-VA-004 | Unidade do teto de custo: por ciclo vs diário | Cap por ciclo no plano + safety diário global (espelha vision-mcp) | Open |
> 98	| OTD-VA-005 | Mecanismo de reinjeção do feedback (texto cru vs features estruturadas) | Features estruturadas (top hooks/produtos/horários) | Open |
> 99	| OTD-VA-006 | Autonomia de seleção de produto (auto-score vs shortlist) | 3 SKUs semente agora (Decisão 4); auto-score em v1.0 | Decided (seeds) |
> 100	| OTD-VA-007 | `OTD-ML-MP-PER-USER` — secret de postback per-user | Fechar antes da atribuição de receita multi-tenant | Open (herdada) |
> 101	
> 102	---
> 103	
> 104	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 105	
> ```

## 🤖 Claude *(21:09:28)*

I now have all the data. Let me read the quality-metrics doc (08) to complete the picture, then do my cross-matrix analysis.

## 🤖 Claude *(21:09:28)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/08-quality-metrics.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Quality & Self-Optimization Specification
> 2	
> 3	**Project:** viral-autopilot  
> 4	**Version:** v0.1 | **Date:** 2026-06-17  
> 5	**BoK Applied:** CMQ/OE BOK (Process Management + Organizational Excellence)  
> 6	**Status:** Draft
> 7	
> 8	---
> 9	
> 10	## 1. Quality Objectives
> 11	
> 12	| QO ID | Objective | Linked Business Objective | Target | Review Cadence |
> 13	|-------|-----------|--------------------------|--------|---------------|
> 14	| QO-001 | Autonomia sem intervenção por post | BO-001 | ≥ 90% posts via autopilot | Weekly |
> 15	| QO-002 | Loop de melhoria com dado real (não teatral) | BO-002 | ≥ 80% das análises com `has_real_data=true` após ciclo 2 | Monthly |
> 16	| QO-003 | Margem protegida: zero overspend | BO-003 | 100% ciclos com `spend_mco ≤ budget_cap`; 0 deduct em ciclo abortado | Weekly |
> 17	| QO-004 | Monetização universal | BO-004 | 100% criativos com link ML + `content_variant_id` | Weekly |
> 18	
> 19	---
> 20	
> 21	## 2. KPI Dashboard Definition
> 22	
> 23	> Data source: tabelas/views Supabase por KPI.
> 24	
> 25	| KPI ID | Name | Formula | Target | Warn Threshold | Critical Threshold | Data Source |
> 26	|--------|------|---------|--------|---------------|-------------------|-------------|
> 27	| KPI-VA-001 | Custo por ciclo | `SUM(spend_mco) per cycle` | ≤ `budget_cap_mco` | > 80% do cap | > cap | `autopilot_cycles` |
> 28	| KPI-VA-002 | Lift viral ciclo-a-ciclo | `avg_engagement(N+1) / avg_engagement(N)` | ≥ 1.10× após 3 ciclos | < 1.0× | < 0.8× (regressão) | `creative_metrics` por `cycle_id` |
> 29	| KPI-VA-003 | Receita ML atribuída por ciclo | `SUM(revenue_cents) per cycle / 100` | crescente MoM | estagnado 3 ciclos | 0 com cliques > 0 (postback morto) | `creative_metrics` + `affiliate_links` |
> 30	| KPI-VA-004 | % criativos monetizados | `monetized_creatives / total_creatives` | 100% | < 100% | < 90% | `creative_metrics` ∩ `affiliate_links` |
> 31	| KPI-VA-005 | CTR de afiliado | `affiliate_clicks / impressions` | benchmark por produto | < baseline | 0 com impressões > 0 | `creative_metrics` |
> 32	| KPI-VA-006 | mcoCoins Burn Rate | `SUM(deductions) / active_plans` | < `budget_cap` médio | 80% | > cap | `profiles` + `mco_transactions` |
> 33	| KPI-VA-007 | Edge Fn p95 Latency (`autopilot-run`) | `PERCENTILE_CONT(0.95)` | < 800ms (dry_run) | 1000ms | 2000ms | Supabase logs |
> 34	| KPI-VA-008 | Cadência cumprida | `cycles_on_time / cycles_due` | ≥ 98% | < 95% | < 90% | `autopilot_cycles` vs `next_run_at` |
> 35	
> 36	---
> 37	
> 38	## 3. FMEA Table
> 39	
> 40	> S, O, D: 1 (melhor) → 10 (pior). RPN = S × O × D. RPN > 100 exige ação.
> 41	
> 42	| ID | Function | Failure Mode | Effect | S | O | D | RPN | Recommended Action |
> 43	|----|---------|--------------|--------|---|---|---|-----|--------------------|
> 44	| FMEA-VA-001 | Cost guardrail (FR-VA-007) | Bypass do teto / overspend autônomo (disparo paralelo, gate fraco) | Drena mcoCoins do tenant silenciosamente | 8 | 4 | 4 | **128** | Gate atômico server-side ANTES do deduct + idempotência (plan_id, cycle_number) + safety cap diário global (espelha vision-mcp); lock otimista no ciclo |
> 45	| FMEA-VA-002 | Cycle analyzer (FR-VA-010) | "Auto-melhoria teatral": analisa `creative_metrics` vazia, LLM gera recomendação genérica | Loop aparenta aprender mas não aprende; decisões com base em ruído | 6 | 6 | 5 | **180** | Bloquear deduct/aplicação quando vazio (`has_real_data=false`); usar `affiliate_clicks` (sempre disponível) como sinal mínimo; expor flag no dashboard |
> 46	| FMEA-VA-003 | Cadence cron (FR-VA-005) | Re-fire do cron dobra post/cobrança | Conteúdo duplicado nas redes + cobrança dupla | 7 | 3 | 4 | 84 | UNIQUE (plan_id, cycle_number) + guarda em `scheduled_posts`; catch-up idempotente |
> 47	| FMEA-VA-004 | Geração autônoma (FR-VA-003) | Conteúdo off-brand / viola ToS de rede ou ML publicado sem revisão | Suspensão de conta, dano de marca, queda de receita | 9 | 3 | 5 | **135** | Cyber-Sentinel gate pré-publicação (input+output) + disclosure de afiliado + HITL opcional (PR-VA-013) |
> 48	| FMEA-VA-005 | Product-aware prompt (FR-VA-003) | Prompt injection via nome/desc de produto ou texto de trend | Geração desviada / vazamento de instrução | 8 | 3 | 5 | **120** | Sanitizar produto/trend antes do prompt; Cyber-Sentinel no input; validar output antes de publicar |
> 49	| FMEA-VA-006 | Revenue attribution (FR-VA-017) | Postback ML nunca chega (secret global, OTD-ML-MP-PER-USER) | Receita atribuída = 0 mesmo com vendas; KPI-VA-003 cego | 6 | 5 | 3 | 90 | Fechar OTD-VA-007; provar 1 postback real; usar cliques de afiliado como proxy de ROI enquanto isso |
> 50	| FMEA-VA-007 | mcoCoins deduction | RPC timeout → cobrança dupla | Tenant cobrado em excesso | 9 | 2 | 3 | 54 | Idempotency key por sub-run; `deduct_mco_coins` atômico |
> 51	| FMEA-VA-008 | JWT validation (autopilot-run) | Header ausente/inválido | Acesso não autenticado | 10 | 2 | 1 | 20 | Hard fail no entrypoint; log `infra_health_logs` |
> 52	| FMEA-VA-009 | embed-mcorch-node (observation) | Timeout de embedding | Nó de ciclo sem vetor (memória não pesquisável) | 6 | 3 | 4 | 72 | Retry assíncrono; `scripts/backfill-embeddings.ts` |
> 53	| FMEA-VA-010 | Credential resolution (NFR-VA-004) | Resolução errada → tenant A usa credencial de B | Vazamento de credencial/quota cross-tenant | 9 | 2 | 4 | 72 | Resolução per-user `auth.uid()` + RLS + teste de isolamento; fail-closed |
> 54	| FMEA-VA-011 | Honor product param (FR-VA-016) | Regressão do drop de `affiliate_url`/produto em `:79` | Conteúdo gerado não monetizado | 7 | 3 | 3 | 63 | Teste de integração de regressão; assert link presente em todo formato |
> 55	| FMEA-VA-012 | Cadence availability (NFR-VA-006) | Cron caiu → janela perdida, plano trava | Cadência interrompida silenciosamente | 4 | 3 | 4 | 48 | Reconcile-on-run (catch-up no próximo tick); KPI-VA-008 alerta |
> 56	
> 57	**Itens com RPN > 100 (ação obrigatória):** FMEA-VA-002 (180), FMEA-VA-004 (135), FMEA-VA-001 (128), FMEA-VA-005 (120) — todos com ação recomendada acima.
> 58	
> 59	---
> 60	
> 61	## 4. Self-Optimization Loops
> 62	
> 63	| Loop ID | Trigger Condition | KPI Source | Autonomous Response | Escalation (human) |
> 64	|---------|------------------|------------|--------------------|--------------------|
> 65	| SOL-VA-001 | Ciclo N+1 disparado com `creative_metrics(N)` populada | `creative_metrics` | `autopilot-analyze` produz `optimization_policy`; geração N+1 injeta top features (FR-VA-011) | — (é o core loop) |
> 66	| SOL-VA-002 | KPI-VA-002 lift < 0.8× por 2 ciclos (regressão) | `creative_metrics` | Reverter para baseline de prompt + sinalizar produto/ângulo de baixa conversão p/ poda | Alertar Sovereign |
> 67	| SOL-VA-003 | KPI-VA-006 burn > 80% do cap | `mco_transactions` | Reduzir `planned_units` do próximo ciclo (menos variações) | Alertar se > cap |
> 68	| SOL-VA-004 | Saldo < `min_balance_mco` | `profiles` | Pausar plano (kill-switch) + notificação PT-BR; NÃO disparar ciclo | — (sem auto-recarga) |
> 69	| SOL-VA-005 | KPI-VA-005 CTR de um produto < baseline por 3 ciclos | `creative_metrics` | Despriorizar o produto na seleção (comm+trend) do próximo ciclo | — |
> 70	
> 71	---
> 72	
> 73	## 5. Self-Healing Specifications
> 74	
> 75	### 5.1 Watchdog Telemetry Events
> 76	
> 77	Novos `event` em `infra_health_logs` (com `metadata` allowlist — não vazar per-tenant na tabela global-read):
> 78	
> 79	| Event Type | Trigger | Severity | Payload (allowlisted) |
> 80	|------------|---------|----------|---------|
> 81	| `viral_autopilot_cycle_started` | ciclo aberto | info | `{plan_id, cycle_number, planned_units}` |
> 82	| `viral_autopilot_cycle_completed` | ciclo fechado | info | `{cycle_id, spend_mco, creatives}` |
> 83	| `viral_autopilot_aborted_budget` | kill-switch disparado | warn | `{plan_id, projected_mco, budget_cap}` |
> 84	| `viral_autopilot_collect_failure` | coletor falhou após retry | warn | `{cycle_id, platform}` |
> 85	| `viral_autopilot_analyze_empty` | análise sem dado real | warn | `{plan_id, cycle_id}` |
> 86	| `viral_autopilot_cycle_failed` | sub-run de geração 5xx | error | `{cycle_id, platform}` |
> 87	
> 88	### 5.2 Auto-Recovery Script Stubs
> 89	
> 90	```bash
> 91	#!/bin/bash
> 92	# scripts/self-heal-viral-autopilot.sh
> 93	# Triggered by mega-brain-daemon when viral_autopilot_cycle_failed/analyze_empty detected
> 94	LOG_TABLE="infra_health_logs"
> 95	echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] Self-heal viral-autopilot"
> 96	
> 97	# 1. Reconcile stuck cycles: cycles 'running' > 30min → mark 'failed', NÃO re-cobrar
> 98	# 2. Re-arm planos com next_run_at no passado mas is_active (janela perdida)
> 99	# 3. Re-disparar autopilot-collect para posts published sem creative_metrics há > 24h
> 100	# (todas as ações idempotentes; service-role; logam recovery_ok em infra_health_logs)
> 101	echo "[OK] Self-heal viral-autopilot complete"
> 102	```
> 103	
> 104	### 5.3 mega-brain-daemon Integration Points
> 105	
> 106	| Daemon Event | Condition | Action |
> 107	|-------------|-----------|--------|
> 108	| `health_check` | A cada 5 min (watchdog) | Checar ciclos `running` órfãos (> 30min) e planos due não disparados |
> 109	| `anomaly_detected` | `viral_autopilot_*` error rate > 5/h | Executar `self-heal-viral-autopilot.sh` |
> 110	| `budget_anomaly` | `aborted_budget` > 3× p/ o mesmo plano em 24h | Manter pausado + alertar Sovereign (plano mal-configurado) |
> 111	| `recovery_confirmed` | Ciclo subsequente completa OK | Inserir `recovery_ok` em `infra_health_logs` |
> 112	
> 113	---
> 114	
> 115	## 6. SLA / SLO / SLI Definitions
> 116	
> 117	| Service | SLI (what we measure) | SLO (our target) | SLA (consequence) |
> 118	|---------|----------------------|------------------|-------------------|
> 119	| `autopilot-run` (dry_run) | p95 response latency | ≤ 800ms | Investigar se > 2s por > 1% das chamadas/mês |
> 120	| Cadência | % ciclos disparados em ≤ 15min do `next_run_at` | ≥ 98% | Self-heal + alerta se < 90% |
> 121	| Cost guardrail | % ciclos com `spend ≤ cap` e 0 deduct em abortados | 100% | Incident report obrigatório se violado (dinheiro do tenant) |
> 122	| Coleta de métricas | % posts com ≥ 1 sinal em `creative_metrics` ≤ 24h | ≥ 95% (cliques sempre; orgânico best-effort) | Auto-retry; cair p/ só cliques |
> 123	| Monetização | % criativos com link ML válido | 100% | Bloquear publicação de criativo sem link |
> 124	
> 125	---
> 126	
> 127	## 7. PDCA Improvement Cadence
> 128	
> 129	| Cycle | Phase | Activity | Owner | Frequency |
> 130	|-------|-------|----------|-------|-----------|
> 131	| viral-autopilot Quality | Plan | Revisar FMEA (RPN>100) + alvos de KPI | Sovereign | Quarterly |
> 132	| viral-autopilot Quality | Do | Implementar top ação (ex.: fechar OTD-ML-MP-PER-USER) | Engineering | Per sprint |
> 133	| viral-autopilot Quality | Check | Comparar KPI-VA-002 (lift) e KPI-VA-003 (receita) vs alvo; atualizar RPNs | AIOS | Monthly |
> 134	| viral-autopilot Quality | Act | Fechar loop; podar produtos/ângulos de baixa conversão; atualizar este doc | Sovereign | Monthly |
> 135	
> 136	**Improvement backlog location:** `.claude/context/sprint-priorities.md`
> 137	
> 138	---
> 139	
> 140	## 8. Observability Checklist
> 141	
> 142	### 8.1 Logging Events
> 143	
> 144	| Event | Location | Level | Fields logged |
> 145	|-------|----------|-------|--------------|
> 146	| Entrada de função | `autopilot-run/index.ts` ~linha 10 | INFO | `{user_id, plan_id, request_id}` |
> 147	| Cost gate decision | após projeção | INFO | `{projected_mco, budget_cap, decision}` |
> 148	| mcoCoins deduction (sub-run) | após RPC | INFO | `{user_id, amount, new_balance, cycle_id}` |
> 149	| Feedback inject | antes da chamada LLM | INFO | `{cycle_id, has_real_data, features_count}` |
> 150	| Erro de lógica | catch block | ERROR | `{cycle_id, error_message}` |
> 151	| SLA breach | timeout guard | WARN | `{process_id, elapsed_ms}` |
> 152	
> 153	### 8.2 Alerting Rules
> 154	
> 155	| Condition | Channel | Escalation |
> 156	|-----------|---------|------------|
> 157	| `aborted_budget` para 1 plano | `infra_health_logs` + Telegram | Sovereign se > 3× em 24h |
> 158	| `analyze_empty` após ciclo 2 | `infra_health_logs` | AIOS (loop teatral — FMEA-VA-002) |
> 159	| KPI-VA-003 = 0 com cliques > 0 | scheduled check | Sovereign (postback morto — FMEA-VA-006) |
> 160	| p95 `autopilot-run` > 2s | `infra_health_logs` | mega-brain-daemon self-heal |
> 161	
> 162	### 8.3 Distributed Tracing Touchpoints
> 163	
> 164	| Span | Start | End | Tags |
> 165	|------|-------|-----|------|
> 166	| `autopilot-run.total` | request recebido | response enviado | `user_id`, `plan_id`, `cycle_id`, `status` |
> 167	| `autopilot-run.cost_gate` | antes da projeção | após decisão | `projected_mco`, `decision` |
> 168	| `autopilot-run.fanout` | início fan-out | fim Promise.allSettled | `creatives`, `failures` |
> 169	| `autopilot-analyze.total` | leitura de métricas | policy gravada | `cycle_id`, `has_real_data` |
> 170	
> 171	---
> 172	
> 173	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 174	
> ```

## 🤖 Claude *(21:09:38)*

I now have all 9 docs. Let me build the full traceability chains and cross-check the four matrices systematically. Let me construct the data carefully.

**Building the chains across the 4 matrices:**

MR→BR (consistent across MRD §9, BRD §10): all 8 MR→BR are 1:1, consistent.

MR→PR mappings — comparing BRD §10 (PR stub) vs PRD §8:
- MR-VA-001: both → PR-VA-002, PR-VA-008 ✓
- MR-VA-002: both → PR-VA-001, PR-VA-003 ✓
- MR-VA-003: BRD→ PR-VA-004, PR-VA-005 | PRD→ PR-VA-004, PR-VA-005, **PR-VA-012** (PRD adds PR-VA-012)
- MR-VA-004: BRD→ PR-VA-002 | PRD→ PR-VA-002, **PR-VA-013** (PRD adds PR-VA-013)
- MR-VA-005: both → PR-VA-007 ✓
- MR-VA-006: both → PR-VA-006 ✓
- MR-VA-007: both → PR-VA-001 ✓
- MR-VA-008: BRD→ PR-VA-010, PR-VA-011 | PRD→ PR-VA-010, PR-VA-011, **PR-VA-022** (PRD adds PR-VA-022)

Now let me check PR definitions vs traceability. PRD §4 defines: PR-VA-001..008 (Must), PR-VA-010..013 (Should), PR-VA-020..022 (Could). Let me verify each PR's "BR Traced" against the matrices and check the FRD.

Let me verify a few critical cross-references with grep to be precise.

## 🤖 Claude *(21:09:41)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot && echo \"=== PR-VA-009 anywhere? ===\" && grep -rn \"PR-VA-009\" . ; echo \"=== PR-VA-020 / 021 in FRD? ===\" && grep -rn \"PR-VA-020\\|PR-VA-021\" 04-frd.md ; echo \"=== FR-VA traced PRs in FRD matrix \u00a77 ===\" && grep -n \"PR-VA-022\\|PR-VA-020\\|PR-VA-021\\|PR-VA-012\\|PR-VA-013\" 04-frd.md",
  "description": "Check for orphan/missing PR IDs across docs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === PR-VA-009 anywhere? ===
> === PR-VA-020 / 021 in FRD? ===
> === FR-VA traced PRs in FRD matrix §7 ===
> 16:**Out of scope (Fase 2 / Won't):** geração de vídeo 9:16; publicação em TikTok/Instagram/YouTube; gestão de anúncios pagos; atribuição multi-touch cross-network; auto-descoberta de catálogo (CLI manual permanece até PR-VA-022).
> ```

## 🤖 Claude *(21:09:44)*

Confirmed. Now let me check downstream FR coverage: which PRs have FRs in the FRD §7 matrix, and which FRs trace which PRs. Let me also check the PROC coverage and cron consistency.

## 🤖 Claude *(21:09:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot && echo \"=== PR-VA-012 / 013 / 022 in FRD \u00a77 matrix ===\" && grep -nE \"^\\| PR-VA-(012|013|022)\" 04-frd.md ; echo \"\" ; echo \"=== All PR rows in FRD \u00a77 ===\" && grep -nE \"^\\| PR-VA-[0-9]+ \\|\" 04-frd.md ; echo \"\" ; echo \"=== FR-VA-016 PR Traced in FR table ===\" && grep -n \"FR-VA-016\" 04-frd.md",
  "description": "Check FRD PR-to-FR matrix completeness"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === PR-VA-012 / 013 / 022 in FRD §7 matrix ===
> 
> === All PR rows in FRD §7 ===
> 168:| PR-VA-001 | FR-VA-001, FR-VA-014, FR-VA-016 | NFR-VA-004, NFR-VA-005 |
> 169:| PR-VA-002 | FR-VA-002, FR-VA-003, FR-VA-004, FR-VA-016 | NFR-VA-001, NFR-VA-008 |
> 170:| PR-VA-003 | FR-VA-005, FR-VA-006 | NFR-VA-003, NFR-VA-006 |
> 171:| PR-VA-004 | FR-VA-008, FR-VA-009, FR-VA-017 | NFR-VA-007 |
> 172:| PR-VA-005 | FR-VA-010, FR-VA-011 | NFR-VA-007 |
> 173:| PR-VA-006 | FR-VA-007 | NFR-VA-002 |
> 174:| PR-VA-007 | FR-VA-014, FR-VA-015, FR-VA-017 | NFR-VA-007 |
> 175:| PR-VA-008 | FR-VA-013 | NFR-VA-008 |
> 176:| PR-VA-010 | FR-VA-012 | — |
> 177:| PR-VA-011 | FR-VA-018 | — |
> 
> === FR-VA-016 PR Traced in FR table ===
> 41:| FR-VA-016 | Honor product/affiliate param | `orchestrate-content` passa a desestruturar e honrar o produto-alvo/`affiliate_url` (hoje dropado em `:79`), propagando ao `orchestrate-step`. | Medium | PR-VA-002 | EdgeFunction | AT-VA-016 |
> 153:| FR-VA-016 | ✅ | ✅ | — | param honrado (regressão do drop em `:79`) |
> 168:| PR-VA-001 | FR-VA-001, FR-VA-014, FR-VA-016 | NFR-VA-004, NFR-VA-005 |
> 169:| PR-VA-002 | FR-VA-002, FR-VA-003, FR-VA-004, FR-VA-016 | NFR-VA-001, NFR-VA-008 |
> ```

## 🤖 Claude *(21:09:51)*

Key findings emerging. Now let me verify the FR-level PR-Traced field (FR table §2) against the §7 reverse matrix, to spot the FR-VA-016 PR-Traced discrepancy and check FR-VA-006/FR-VA-017 multi-PR claims.

## 🤖 Claude *(21:09:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot && echo \"=== FR table \u00a72 PR Traced column (FR-VA-001..018) ===\" && grep -nE \"^\\| FR-VA-[0-9]+ \\|\" 04-frd.md | sed -E 's/\\|[^|]*\\|[^|]*\\|[^|]*\\|[^|]*\\| ([^|]*) \\|[^|]*\\|[^|]*\\|/  >>PR: \\1/'",
  "description": "Extract PR Traced per FR from FR table"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === FR table §2 PR Traced column (FR-VA-001..018) ===
> 26:  >>PR: Critical AT-VA-001 |
> 27:  >>PR: PR-VA-002, PR-VA-001
> 28:  >>PR: PR-VA-002
> 29:  >>PR: PR-VA-002
> 30:  >>PR: PR-VA-003
> 31:| FR-VA-006 | Cycle ledger   >>PR: Critical AT-VA-006 |
> 32:  >>PR: PR-VA-006
> 33:  >>PR: PR-VA-004
> 34:  >>PR: PR-VA-004
> 35:  >>PR: PR-VA-005
> 36:  >>PR: PR-VA-005
> 37:  >>PR: PR-VA-010, PR-VA-001
> 38:  >>PR: PR-VA-008
> 39:  >>PR: PR-VA-001, PR-VA-007
> 40:  >>PR: PR-VA-007
> 41:  >>PR: PR-VA-002
> 42:  >>PR: PR-VA-007
> 43:  >>PR: PR-VA-011
> 138:| FR-VA-001 | ✅ | ✅ | — | RLS own-row; validação de campos |
> 139:| FR-VA-002 | ✅ | ✅ | ✅ | fan-out + forward JWT (smoke zero-cost com `dry_run`) |
> 140:| FR-VA-003 | ✅ | ✅ | — | prompt contém produto + framework viral |
> 141:| FR-VA-004 | ✅ | ✅ | ✅ | link ML + `content_variant_id` em TODO formato |
> 142:| FR-VA-005 | ✅ | ✅ | — | auto-refill `next_run_at`; janela perdida (catch-up) |
> 143:| FR-VA-006 | ✅ | ✅ | — | idempotência (plan_id, cycle_number) |
> 144:| FR-VA-007 | ✅ | ✅ | ✅ | **kill-switch smoke zero-cost** (saldo intacto pós-abort) |
> 145:| FR-VA-008 | ✅ | ✅ | — | coletor best-effort por tier; cliques sempre |
> 146:| FR-VA-009 | ✅ | — | — | unicidade por `content_variant_id`+`source` |
> 147:| FR-VA-010 | ✅ | ✅ | — | baseline quando vazio (`has_real_data=false`) |
> 148:| FR-VA-011 | ✅ | ✅ | ✅ | prova de reinjeção: prompt ciclo N+1 contém features do ciclo N |
> 149:| FR-VA-012 | ✅ | ✅ | — | ranking comissão+trend |
> 150:| FR-VA-013 | ✅ | ✅ | — | imagem product-referenced anexada a `scheduled_posts` |
> 151:| FR-VA-014 | ✅ | — | — | hook CRUD + queries |
> 152:| FR-VA-015 | — | — | ✅ | E2E UI 1920×1080 (gate Canvas/UI) |
> 153:| FR-VA-016 | ✅ | ✅ | — | param honrado (regressão do drop em `:79`) |
> 154:| FR-VA-017 | ✅ | ✅ | — | atribuição por `content_variant_id` (gated em OTD-VA-007) |
> 155:| FR-VA-018 | ✅ | ✅ | — | ângulo lê `vm_trends` |
> ```

## 🤖 Claude *(21:10:04)*

I have everything I need. Let me consolidate the analysis. I'll record key per-FR PR-Traced values from the FR table §2 explicitly:

- FR-VA-006 (Cycle ledger): PR-Traced = **PR-VA-003, PR-VA-006** (from the table row I read earlier: "PR-VA-003, PR-VA-006")
- FR-VA-012: PR-VA-010, PR-VA-001
- FR-VA-014: PR-VA-001, PR-VA-007
- FR-VA-017: PR-VA-007

Now let me cross-check the index summary chain (00-index §"Traceability Chain") against the actual matrices — this is a known place for drift.

**Index chain claims:**
- MR-VA-001 → BR-VA-001 → **PR-VA-002** → FR-VA-003, FR-VA-013. But PRD/BRD map MR-VA-001→ PR-VA-002 **and PR-VA-008**. Index drops PR-VA-008. Also FR-VA-013 traces PR-VA-008 (not PR-VA-002). So the index chain conflates: it shows PR-VA-002 → FR-VA-013, but FR-VA-013 actually traces PR-VA-008.
- MR-VA-002 → ... → FR-VA-001, FR-VA-005, FR-VA-006. OK-ish.
- MR-VA-007 → BR-VA-007 → PR-VA-001 → FR-VA-001, NFR-VA-004 → **affiliate_config**. But BR-VA-007/NFR-VA-004 is about per-user credential resolution. FR-VA-001 is the plan entity. The actual per-user-credential FR is not clearly its own FR.

Let me now nail down the most important structural findings and verify the "MVP coherence" question raised in the prompt (FR-VA-013 'Should (MVP)' vs MVP=texto+imagem).

Let me verify one more thing: whether BR-VA-003 traces a PR that actually covers "performance collector" — there's a notable BR-Traced anomaly in the PRD feature inventory.

## 🤖 Claude *(21:10:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot && echo \"=== PRD \u00a74 BR Traced per PR ===\" && grep -nE \"^\\| PR-VA-[0-9]+ \\|\" 03-prd.md | sed -E 's/^([0-9]+):\\| (PR-VA-[0-9]+) \\|[^|]*\\|[^|]*\\| ([^|]*) \\|.*/\\1 \\2 -> BR: \\3/' ; echo \"\" ; echo \"=== PR-VA-004 BR Traced (collector) ===\" && grep -n \"PR-VA-004\" 03-prd.md",
  "description": "Extract BR Traced per PR from PRD feature inventory"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === PRD §4 BR Traced per PR ===
> 70 PR-VA-001 -> BR: BR-VA-002, BR-VA-007, BR-VA-008
> 71 PR-VA-002 -> BR: BR-VA-001, BR-VA-004
> 72 PR-VA-003 -> BR: BR-VA-002
> 73 PR-VA-004 -> BR: BR-VA-005, BR-VA-003
> 74 PR-VA-005 -> BR: BR-VA-003
> 75 PR-VA-006 -> BR: BR-VA-006
> 76 PR-VA-007 -> BR: BR-VA-005
> 77 PR-VA-008 -> BR: BR-VA-001
> 83 PR-VA-010 -> BR: BR-VA-008
> 84 PR-VA-011 -> BR: BR-VA-008
> 85 PR-VA-012 -> BR: BR-VA-003
> 86 PR-VA-013 -> BR: BR-VA-004
> 92 PR-VA-020 -> BR: BR-VA-001
> 93 PR-VA-021 -> BR: BR-VA-001
> 94 PR-VA-022 -> BR: BR-VA-008
> 
> === PR-VA-004 BR Traced (collector) ===
> 73:| PR-VA-004 | **Performance collector** — cliques afiliado + engajamento orgânico + receita → `creative_metrics` | P1, P2 | BR-VA-005, BR-VA-003 | L | 0 | Combo (Decisão 3); cliques primeiro, orgânico best-effort |
> 108:**Included:** PR-VA-001, PR-VA-002, PR-VA-003, PR-VA-004, PR-VA-005, PR-VA-006, PR-VA-007, PR-VA-008  
> 185:  Scenario: Loop auto-melhorável realimenta o ciclo seguinte (PR-VA-004, PR-VA-005)
> 205:| MR-VA-003 | BR-VA-003 | PR-VA-004, PR-VA-005, PR-VA-012 |
> ```

## 🤖 Claude *(21:10:13)*

Now I have the complete picture. There's a notable inconsistency: PR-VA-004's BR-Traced (in PRD §4) is `BR-VA-005, BR-VA-003`, but PR-VA-004 traces to MR-VA-003/BR-VA-003 in the matrices. Meanwhile BR-VA-005 (metrics+ROI) in the PRD §4 feature-level traces shows PR-VA-004 and PR-VA-007 both claiming BR-VA-005 — but the matrices (BRD §10, PRD §8) map MR-VA-005/BR-VA-005 → **only PR-VA-007**, dropping PR-VA-004. This is a real cross-matrix inconsistency.

Let me do one final verification on the cron consistency and the "5 PROC cover all critical FRs" claim. Critical FRs are: FR-VA-001, 002, 003, 004, 005, 006, 007, 011. Let me confirm FR-VA-016's priority and check whether the data-model FK for `creative_metrics.content_variant_id` is consistently typed (uuid) vs `content_variant_id` source.

## 🤖 Claude *(21:10:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot && echo \"=== Critical FRs (priority) ===\" && grep -nE \"Critical\" 04-frd.md | grep -E \"FR-VA\" ; echo \"\" ; echo \"=== autopilot-analyze cron? (FR-VA-010 is service-role 'agendado' but which cron?) ===\" && grep -rn \"autopilot-analyze\" 05-sdd.md 07-process-flow.md | grep -i \"cron\\|pg_cron\\|schedule\" ; echo \"\" ; echo \"=== Crons declared (SDD \u00a72.5 + process \u00a77) ===\" && grep -rn \"autopilot-cadence\\|autopilot-collect\\|autopilot-analyze\" 05-sdd.md | grep -i cron",
  "description": "Verify critical FR priorities and analyze-cron coverage"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === Critical FRs (priority) ===
> 26:| FR-VA-001 | Autopilot plan entity | Tabela `autopilot_plans` (per-user RLS): mode (`all_at_once`\|`every_n_days`), interval_days (default 3), target_product_ids[], platforms[], budget_cap_mco, is_active, next_run_at. CRUD via hook. | Critical | PR-VA-001 | DB | AT-VA-001 |
> 27:| FR-VA-002 | Cycle dispatcher | Edge fn `autopilot-run` (JWT): valida plano, aplica gate de custo (FR-VA-007), seleciona produto(s), abre `autopilot_cycles`, e faz fan-out product-aware para `orchestrate-content` (1 dispatch por produto×rede). Reusa o padrão de `campaign-run`. | Critical | PR-VA-002, PR-VA-001 | EdgeFunction | AT-VA-002 |
> 28:| FR-VA-003 | Product-aware generation | Em `orchestrate-step`, o prompt recebe o produto-alvo (id+nome+imagem+preço+comissão) e usa framework de gancho viral de consumo (hook/valor/CTA) — substitui os system prompts B2B hardcoded (`:138`,`:290`). | Critical | PR-VA-002 | Lib/EdgeFunction | AT-VA-003 |
> 29:| FR-VA-004 | Monetize all formats | `monetizeContent` (`_shared/affiliate.ts`) roda em artigo **+ LinkedIn + Twitter**, embutindo link ML per-user com `content_variant_id` por criativo (não só no artigo, não por regex de 3 SKUs). | Critical | PR-VA-002 | Lib | AT-VA-004 |
> 30:| FR-VA-005 | Cadence cron | pg_cron `autopilot-cadence` (*/15) → fn `autopilot-cadence-cron` (service-role): encontra planos `is_active AND next_run_at <= now`, dispara `autopilot-run`, e re-agenda `next_run_at = now + interval_days` (auto-refill, ao contrário do drip finito do nurture). | Critical | PR-VA-003 | Cron | AT-VA-005 |
> 31:| FR-VA-006 | Cycle ledger | Tabela `autopilot_cycles`: plan_id, cycle_number, status (`running`\|`completed`\|`aborted_budget`\|`failed`), spend_mco, planned_units, analysis_node_id, started_at, completed_at. Idempotência por (plan_id, cycle_number). | Critical | PR-VA-003, PR-VA-006 | DB | AT-VA-006 |
> 32:| FR-VA-007 | Cost guardrail (kill-switch) | ANTES de qualquer `deduct_mco_coins`: soma custo projetado (10 + 5 + img × nº criativos). Se `> budget_cap_mco` OU `saldo < min_balance` → aborta ciclo (`aborted_budget`), pausa o plano, notifica. Espelha caps do `vision-mcp`. | Critical | PR-VA-006 | EdgeFunction | AT-VA-007 |
> 36:| FR-VA-011 | Feedback injection | A geração (`orchestrate-step`/`autopilot-run`) LÊ o `optimization_policy` mais recente do tenant e injeta as features no system prompt do próximo ciclo. Fecha a quebra "saída sem consumo". | Critical | PR-VA-005 | Lib/EdgeFunction | AT-VA-011 |
> 
> === autopilot-analyze cron? (FR-VA-010 is service-role 'agendado' but which cron?) ===
> 
> === Crons declared (SDD §2.5 + process §7) ===
> 05-sdd.md:29:│  autopilot-cadence-cron ◀───┤   autopilot-collect             │
> 05-sdd.md:74:| `autopilot-cadence-cron` | `supabase/functions/autopilot-cadence-cron/index.ts` | service-role (`verify_jwt=false`, pg_net) | 0 | `SB_SECRET_KEY` (service) |
> 05-sdd.md:76:| `autopilot-collect` | `supabase/functions/autopilot-collect/index.ts` | service-role (cron) | 0 | social/meta tokens per-user |
> 05-sdd.md:94:| `autopilot-cadence` | pg_cron | Disparo recorrente */15 (FR-VA-005) | dentro da migration de cron |
> 05-sdd.md:95:| `autopilot-collect` | pg_cron | Coleta de métricas (FR-VA-008) | dentro da migration de cron |
> 05-sdd.md:179:| `autopilot-cadence-cron` | Falsificação de trigger de cron (disparo forçado) | Spoofing/Elevation | High | `verify_jwt=false` + service-role key; sem path público que dispare ciclo arbitrário; rate por plano via `next_run_at` |
> 05-sdd.md:240:| `pg_cron` | 2 novos jobs (`autopilot-cadence` */15, `autopilot-collect`) | Soma a `memory_decay_fsrs` + `nurture-advance`; preservar os existentes |
> ```

## 🤖 Claude *(21:10:25)*

This surfaces a significant finding: **FR-VA-010 (Cycle analyzer / `autopilot-analyze`)** is described as "agora agendado" (now scheduled) and is the engine of the auto-improvement loop (R3, the core differentiator). But there is **no cron** for it anywhere. The SDD §2.5 declares only 2 crons (`autopilot-cadence`, `autopilot-collect`), and the process-flow §7 also lists only those 2. The process-flow PROC-VA-005 (Análise + reinjeção) is typed "automated / pós-ciclo (encadeado a PROC-VA-001)" — i.e. chained inside the cadence cycle, not its own cron. Yet FR-VA-010 explicitly says "Generaliza `self-optimize`, agora **agendado**" implying a scheduler. The "2 crons" claim is consistent across SDD/process-flow, but it contradicts FR-VA-010's "agendado" wording — the analyzer's trigger mechanism is ambiguous/contradictory.

Let me verify how `autopilot-analyze` is actually triggered in the process-flow and SDD data-flow to confirm this is genuinely unspecified vs chained.

## 🤖 Claude *(21:10:28)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot && echo \"=== autopilot-analyze trigger mentions ALL docs ===\" && grep -rn \"autopilot-analyze\" *.md ; echo \"\" ; echo \"=== PROC-VA-005 trigger ===\" && grep -n \"PROC-VA-005\" 07-process-flow.md",
  "description": "Trace how autopilot-analyze is triggered across docs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === autopilot-analyze trigger mentions ALL docs ===
> 04-frd.md:35:| FR-VA-010 | Cycle analyzer | Edge fn `autopilot-analyze` (service-role, 5 mco): lê `creative_metrics` do ciclo anterior do tenant; se vazio, usa baseline (NÃO inventa); produz `optimization_policy` estruturado (top hook/produto/horário/formato). Generaliza `self-optimize`, agora agendado. | High | PR-VA-005 | EdgeFunction | AT-VA-010 |
> 04-frd.md:110:#### `POST /functions/v1/autopilot-analyze`
> 05-sdd.md:28:│  autopilot-run ─────────────┐   autopilot-analyze (5 mco)     │
> 05-sdd.md:75:| `autopilot-analyze` | `supabase/functions/autopilot-analyze/index.ts` | service-role | 5 mco (análise) | LLM key (per-user→sistema fallback) |
> 05-sdd.md:122: │                 │ (post-cycle) autopilot-analyze: creative_metrics(N) → optimization_policy(N) [feeds cycle N+1]
> 05-sdd.md:157:### `POST /functions/v1/autopilot-analyze`
> 05-sdd.md:227:| LLM key (Groq/OpenRouter/Gemini) | `orchestrate-step`, `autopilot-analyze` | `user_api_keys` (per-user) → vault fallback | per-user controlado |
> 06-data-model.md:150:// Após fechar o ciclo (autopilot-run / autopilot-analyze), insere observation node:
> 08-quality-metrics.md:65:| SOL-VA-001 | Ciclo N+1 disparado com `creative_metrics(N)` populada | `creative_metrics` | `autopilot-analyze` produz `optimization_policy`; geração N+1 injeta top features (FR-VA-011) | — (é o core loop) |
> 08-quality-metrics.md:169:| `autopilot-analyze.total` | leitura de métricas | policy gravada | `cycle_id`, `has_real_data` |
> 
> === PROC-VA-005 trigger ===
> 18:| PROC-VA-005 | Análise + reinjeção de aprendizado | automated | pós-ciclo (encadeado a PROC-VA-001) | System | `optimization_policy` pronto antes do próximo ciclo |
> 114:END  (alimenta PROC-VA-005)
> 188:| PROC-VA-005 | analyze | LLM timeout / métricas vazias | 1 | — | se vazio: baseline (`has_real_data=false`), NÃO inventa; log `analyze_empty` |
> 201:| PROC-VA-005 | analyze | < 10s | 60s | Sim |
> ```

## 🤖 Claude *(21:10:33)*

Confirmed the ambiguity. Now I have a comprehensive, verified set of findings. Let me also double-check the `content_variant_id` FK target consistency (FRD §5 says "FK → criativo/`content_library`" but `content_variant_id` is the keyword across docs) — and whether `content_variant_id` is ever defined as a real column on a real table (it's the join key for monetization/metrics but I don't see it defined on any reuse table).

## 🤖 Claude *(21:10:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot && echo \"=== content_variant_id as a DEFINED column/source (not just FK ref) ===\" && grep -rn \"content_variant_id\" *.md | grep -iE \"content_library|column|coluna|ALTER|CREATE|source|origem|gerado por|produzido\" ; echo \"\" ; echo \"=== optimization_policy: is it reuse? where defined? ===\" && grep -rn \"optimization_policy\" 05-sdd.md 06-data-model.md | head",
  "description": "Check content_variant_id provenance and optimization_policy reuse"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === content_variant_id as a DEFINED column/source (not just FK ref) ===
> 04-frd.md:34:| FR-VA-009 | Unified creative metrics | Tabela `creative_metrics` keyed por `content_variant_id`: affiliate_clicks, impressions, engagements, revenue_cents, source, collected_at. Unifica os 3 sinais (Decisão 3). | High | PR-VA-004 | DB | AT-VA-009 |
> 04-frd.md:128:| `creative_metrics.content_variant_id` | `uuid` | NOT NULL | FK → criativo/`content_library` | — |
> 04-frd.md:146:| FR-VA-009 | ✅ | — | — | unicidade por `content_variant_id`+`source` |
> 05-sdd.md:305:  UNIQUE (content_variant_id, source)                    -- upsert idempotente por fonte
> 06-data-model.md:78:| `content_variant_id` | `uuid` | NOT NULL | — | → criativo/`content_library` | Criativo medido |
> 06-data-model.md:87:| — | — | — | — | — | **UNIQUE (content_variant_id, source)** |
> 06-data-model.md:119:CREATE INDEX creative_metrics_variant_idx ON public.creative_metrics (content_variant_id);
> 06-data-model.md:189:| `creative_metrics` | `(content_variant_id, source)` | UNIQUE (upsert por fonte) | — |
> 07-process-flow.md:110:[UPSERT creative_metrics (content_variant_id, source) — idempotente]
> 07-process-flow.md:210:| `autopilot-collect` | `0 */6 * * *` (6/6h) | `autopilot-collect` | UPSERT (content_variant_id, source) | `infra_health_logs` `collect_failure` |
> 
> === optimization_policy: is it reuse? where defined? ===
> 05-sdd.md:44:│  optimization_policy(reuse)│  └─────────────────────────────────┘
> 05-sdd.md:112: │                 │                    │──[read policy]────────────────────────▶│ optimization_policy (ciclo N-1)
> 05-sdd.md:122: │                 │ (post-cycle) autopilot-analyze: creative_metrics(N) → optimization_policy(N) [feeds cycle N+1]
> 05-sdd.md:163:  optimization_policy_id: string
> 05-sdd.md:328:| OTD-VA-005 | Reinjeção de feedback | Texto cru do `optimization_policy` no prompt | Features estruturadas (top hook/produto/horário/formato) | **B** — estruturado mantém o prompt enxuto e auditável | Sovereign |
> 06-data-model.md:30:- **affiliate_links / optimization_policy / content_library / mcorch_nodes (reuse):** receita, política de melhoria, conteúdo, memória.
> ```

## 🤖 Claude *(21:10:51)*

I now have a thorough, verified analysis. Let me compile the findings.

**Summary of verified traceability/consistency breaks:**

1. **MR→PR matrices diverge between BRD §10 and PRD §8** (MR-VA-003, MR-VA-004, MR-VA-008 each get extra PRs in the PRD that the BRD omits). Cross-matrix inconsistency.

2. **00-index "Traceability Chain summary" contradicts the downstream matrices** — drops PR-VA-008 from MR-VA-001 chain and mis-attributes FR-VA-013 to PR-VA-002 when FR-VA-013 actually traces PR-VA-008.

3. **FR-VA-010 (`autopilot-analyze`) trigger is contradictory/orphaned** — FRD says "agora agendado" (scheduled), but no cron exists for it (SDD/process declare only 2 crons); process-flow types it as chained post-cycle. The R3 core-loop engine has no defined, consistent trigger.

4. **BR-VA-005 → PR mapping inconsistent**: PR-VA-004 claims BR-VA-005 in PRD §4 feature inventory, but the MR→BR→PR matrices map BR-VA-005 only to PR-VA-007. PR-VA-004's matrix lineage is BR-VA-003 (MR-VA-003), yet its feature row lists BR-VA-005 first.

5. **FR-VA-016 PR-Traced inconsistency**: FR table §2 lists FR-VA-016 → PR-VA-002 only; §7 reverse matrix lists it under BOTH PR-VA-001 and PR-VA-002.

6. **PR-VA-012, PR-VA-013, PR-VA-022 are orphaned downstream-of-FR**: they appear in PRD §8 matrix (and PRD §4) but are entirely absent from FRD §7's PR→FR matrix. PR-VA-012/013 are v1.0 Should-haves that the index claims FR coverage doesn't exist for; PR-VA-022 (Could) has no FR — acceptable as Future, but it's listed in PRD §8 traceability without any FR, making the chain dead-end.

7. **`content_variant_id` is a load-bearing join key with no defined origin** — every monetization/metrics FR keys on it, FRD/data-model say "FK → criativo/`content_library`", but no doc defines where/how `content_library` gets a `content_variant_id` column (no ALTER, no source). The chain FR-VA-004/009/017 → artifact has a missing table column.

8. **PR-VA-020 / PR-VA-021 (Could/Fase 2) appear in PRD §4 with BR-Traced=BR-VA-001 but never in any traceability matrix** (not in PRD §8, not in FRD §7) — defined but never traced downstream (acceptable as Won't/Future, but inconsistent with PR-VA-022 which IS in PRD §8).

Let me verify finding 7 more strictly and finding 3's MVP-criticality, then finalize.

## 🤖 Claude *(21:10:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot && echo \"=== Does ANY doc add content_variant_id column to content_library / scheduled_posts? ===\" && grep -rn \"ADD COLUMN\\|ALTER TABLE\" *.md ; echo \"\" ; echo \"=== FR-VA-013 priority restated (Should MVP) vs MVP scope ===\" && grep -n \"Should (MVP)\\|MVP = texto\\|MVP \u2014 texto\\|texto + imagem\\|TEXTO + IMAGEM\" *.md",
  "description": "Verify missing column + FR-VA-013 MVP coherence"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === Does ANY doc add content_variant_id column to content_library / scheduled_posts? ===
> 05-sdd.md:191:ALTER TABLE public.autopilot_plans ENABLE ROW LEVEL SECURITY;
> 05-sdd.md:268:ALTER TABLE public.autopilot_plans ENABLE ROW LEVEL SECURITY;
> 05-sdd.md:288:ALTER TABLE public.autopilot_cycles ENABLE ROW LEVEL SECURITY;
> 05-sdd.md:307:ALTER TABLE public.creative_metrics ENABLE ROW LEVEL SECURITY;
> 05-sdd.md:311:ALTER TABLE public.scheduled_posts ADD COLUMN IF NOT EXISTS cycle_id uuid
> 06-data-model.md:103:ALTER TABLE public.autopilot_plans     ENABLE ROW LEVEL SECURITY;
> 06-data-model.md:104:ALTER TABLE public.autopilot_cycles    ENABLE ROW LEVEL SECURITY;
> 06-data-model.md:105:ALTER TABLE public.creative_metrics    ENABLE ROW LEVEL SECURITY;
> 
> === FR-VA-013 priority restated (Should MVP) vs MVP scope ===
> 00-index.md:36:2. **MVP:** TEXTO + IMAGEM nas redes ATUAIS (WordPress/LinkedIn/Twitter-X). Vídeo 9:16 + TikTok/Instagram/YouTube = FASE 2 explícita.
> 04-frd.md:38:| FR-VA-013 | Image creative (product-referenced) | Plugar `generate-image` (hoje órfã) ao ciclo: usa `image_url` do produto ML como referência; formato por plataforma (quadrado MVP; 9:16 fase 2). Anexa asset a `scheduled_posts`. | Should (MVP) | PR-VA-008 | EdgeFunction | AT-VA-013 |
> 02-brd.md:104:- **MVP = texto + imagem nas redes atuais** (WordPress/LinkedIn/Twitter-X). Vídeo + TikTok/IG/YT são fase 2.
> 03-prd.md:66:### Must Have (MVP — texto + imagem nas redes atuais)
> ```

## 🤖 Claude *(21:11:01)*

Both confirmed. Finding 7 verified: no `ADD COLUMN content_variant_id` anywhere — only `scheduled_posts.cycle_id` is added; `content_variant_id` is keyed/FK'd but never provisioned. Finding on FR-VA-013: it's `Should (MVP)` while PRD §4 lists PR-VA-008 (its parent) as **Must Have (MVP)** and §5 MVP scope explicitly INCLUDES PR-VA-008 — so the FR is a downgraded "Should" under a "Must" PR, while the index/BRD/PRD all assert MVP = texto+imagem (i.e. image is a Must). That's an internal priority contradiction on the very feature that makes the MVP "texto + imagem".

I have a complete, verified set of findings. Compiling the structured output.

## 🤖 Claude *(21:11:58)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "dimension": "Rastreabilidade (MR-VA \u2192 BR-VA \u2192 PR-VA \u2192 FR-VA \u2192 artefato)",
  "verdict": "fail",
  "findings": [
    {
      "id": "TRACE-01",
      "severity": "high",
      "doc": "03-prd.md \u00a78 vs 02-brd.md \u00a710 (matrizes MR\u2192PR)",
      "issue": "As matrizes MR\u2192PR dos dois docs N\u00c3O s\u00e3o mutuamente consistentes. BRD \u00a710 mapeia MR-VA-003\u2192{PR-VA-004,PR-VA-005}, MR-VA-004\u2192{PR-VA-002}, MR-VA-008\u2192{PR-VA-010,PR-VA-011}. O PRD \u00a78 adiciona silenciosamente PR-VA-012 a MR-VA-003, PR-VA-013 a MR-VA-004 e PR-VA-022 a MR-VA-008. Mesma cadeia, tr\u00eas c\u00e9lulas divergentes \u2014 n\u00e3o d\u00e1 pra saber qual matriz \u00e9 a fonte da verdade.",
      "fix": "Reconciliar as duas matrizes para serem id\u00eanticas. Como PR-VA-012/013/022 s\u00e3o features Should/Could que de fato rastreiam essas MRs (ver PRD \u00a74 BR-Traced), atualizar a BRD \u00a710 para inclu\u00ed-las, OU anotar explicitamente que a BRD \u00a710 lista s\u00f3 o escopo MVP e o PRD \u00a78 o escopo completo."
    },
    {
      "id": "TRACE-02",
      "severity": "high",
      "doc": "00-index.md \u00a7'Traceability Chain (summary)'",
      "issue": "O resumo de cadeia do \u00edndice contradiz as matrizes downstream. (a) Linha MR-VA-001 mostra 'BR-VA-001 \u2500\u2500\u25b6 PR-VA-002 \u2500\u2500\u25b6 FR-VA-003, FR-VA-013', omitindo PR-VA-008 que BRD \u00a710 e PRD \u00a78 listam para MR-VA-001. (b) Atribui FR-VA-013 a PR-VA-002, mas FR-VA-013 rastreia PR-VA-008 (FRD \u00a72 e \u00a77). O \u00edndice cria uma liga\u00e7\u00e3o PR-VA-002\u2192FR-VA-013 que n\u00e3o existe em nenhuma outra matriz.",
      "fix": "Corrigir a cadeia do \u00edndice: MR-VA-001 \u2192 BR-VA-001 \u2192 PR-VA-002, PR-VA-008 \u2192 (PR-VA-002\u2192FR-VA-003) e (PR-VA-008\u2192FR-VA-013). Tratar o \u00edndice como vis\u00e3o derivada e regener\u00e1-lo das matrizes autoritativas, n\u00e3o escrev\u00ea-lo \u00e0 m\u00e3o."
    },
    {
      "id": "TRACE-03",
      "severity": "high",
      "doc": "04-frd.md (FR-VA-010) vs 05-sdd.md \u00a72.5 + 07-process-flow.md \u00a71/\u00a77",
      "issue": "O acionador do FR-VA-010 (autopilot-analyze) \u2014 motor do loop R3, o diferencial central do produto \u2014 \u00e9 contradit\u00f3rio e sem artefato. A FRD diz 'Generaliza self-optimize, agora AGENDADO', implicando cron pr\u00f3prio. Mas SDD \u00a72.5 e process-flow \u00a77 declaram APENAS 2 crons (autopilot-cadence, autopilot-collect); n\u00e3o h\u00e1 cron de an\u00e1lise. Process-flow PROC-VA-005 tipa a an\u00e1lise como 'automated / p\u00f3s-ciclo (encadeado a PROC-VA-001)', n\u00e3o agendada. SDD \u00a73 tamb\u00e9m a desenha como '(post-cycle)' inline. FR cr\u00edtico-de-valor sem trigger consistente nem artefato cron.",
      "fix": "Decidir e cravar o acionador em UM lugar: ou (a) autopilot-analyze \u00e9 chamado in-line ao fim de cada ciclo do autopilot-cadence-cron \u2014 ent\u00e3o corrigir a FRD FR-VA-010 para remover 'agendado' e dizer 'encadeado p\u00f3s-ciclo'; ou (b) \u00e9 um 3\u00ba cron \u2014 ent\u00e3o adicion\u00e1-lo a SDD \u00a72.5, \u00a76 e process-flow \u00a77 (hoje a doc afirma '2 crons' em 3 lugares)."
    },
    {
      "id": "TRACE-04",
      "severity": "medium",
      "doc": "03-prd.md \u00a74 (PR-VA-004) vs \u00a78/02-brd.md \u00a710 (matrizes MR-VA-005/BR-VA-005)",
      "issue": "Inconsist\u00eancia de rastreio de BR-VA-005. No PRD \u00a74 o feature PR-VA-004 (Performance collector) declara BR-Traced='BR-VA-005, BR-VA-003'. Por\u00e9m todas as matrizes MR\u2192BR\u2192PR mapeiam BR-VA-005 (MR-VA-005) S\u00d3 para PR-VA-007 \u2014 PR-VA-004 n\u00e3o aparece sob MR-VA-005 em lugar nenhum. Ou PR-VA-004 rastreia BR-VA-005 (e a matriz MR-VA-005 deveria list\u00e1-lo) ou n\u00e3o rastreia (e o BR-Traced do feature est\u00e1 errado).",
      "fix": "Decidir: se o coletor (PR-VA-004) serve BR-VA-005 (m\u00e9tricas por criativo), adicionar PR-VA-004 \u00e0 c\u00e9lula MR-VA-005 nas matrizes BRD \u00a710 e PRD \u00a78. Caso contr\u00e1rio, remover BR-VA-005 do BR-Traced de PR-VA-004 em PRD \u00a74 (deixando s\u00f3 BR-VA-003)."
    },
    {
      "id": "TRACE-05",
      "severity": "medium",
      "doc": "04-frd.md \u00a72 (linha FR-VA-016) vs \u00a77 (matriz PR\u2192FR)",
      "issue": "FR-VA-016 (honor product/affiliate param) tem PR-Traced inconsistente entre as duas tabelas do pr\u00f3prio FRD: a tabela \u00a72 lista FR-VA-016 \u2192 'PR-VA-002' (apenas); a matriz reversa \u00a77 lista FR-VA-016 sob AMBOS PR-VA-001 e PR-VA-002. Um FR n\u00e3o pode rastrear 1 PR numa tabela e 2 na outra dentro do mesmo documento.",
      "fix": "Alinhar: se FR-VA-016 atende tanto a entidade de plano (PR-VA-001) quanto a gera\u00e7\u00e3o product-aware (PR-VA-002), atualizar a coluna PR Traced da \u00a72 para 'PR-VA-001, PR-VA-002'. Sen\u00e3o, remover FR-VA-016 da linha PR-VA-001 em \u00a77."
    },
    {
      "id": "TRACE-06",
      "severity": "high",
      "doc": "03-prd.md \u00a78 vs 04-frd.md \u00a77 (PR-VA-012, PR-VA-013)",
      "issue": "IDs de PR \u00f3rf\u00e3os a jusante. PR-VA-012 (A/B variant) e PR-VA-013 (HITL gate) s\u00e3o v1.0 'Should Have', aparecem na matriz PRD \u00a78 (sob MR-VA-003 e MR-VA-004 respectivamente) e em PRD \u00a74, MAS est\u00e3o totalmente ausentes da matriz PR\u2192FR da FRD \u00a77 e nenhum FR os rastreia (grep confirma 0 ocorr\u00eancias em 04-frd.md). A cadeia MR-VA-003\u2192...\u2192PR-VA-012 e MR-VA-004\u2192...\u2192PR-VA-013 termina em beco sem FR. Como o escopo v1.0 est\u00e1 In-scope na FRD \u00a71, esses PRs deveriam ter FR.",
      "fix": "Ou criar FRs para PR-VA-012 (ex.: FR de gera\u00e7\u00e3o de N variantes + sele\u00e7\u00e3o por desempenho) e PR-VA-013 (FR de gate HITL reusando policy-engine do intent-execute) e adicion\u00e1-los \u00e0 matriz \u00a77; ou, se forem deferidos para al\u00e9m do v1.0 documentado, remov\u00ea-los das c\u00e9lulas de rastreio MR-VA-003/004 do PRD \u00a78 e marc\u00e1-los Future."
    },
    {
      "id": "TRACE-07",
      "severity": "medium",
      "doc": "03-prd.md \u00a78 vs 04-frd.md \u00a77 (PR-VA-022 e PR-VA-020/021)",
      "issue": "Tratamento inconsistente dos PRs 'Could/Fase 2'. PR-VA-022 aparece na matriz autoritativa PRD \u00a78 (c\u00e9lula MR-VA-008) por\u00e9m sem nenhum FR em FRD \u00a77 \u2014 cadeia que morre num PR sem artefato. J\u00e1 PR-VA-020 e PR-VA-021 (mesma categoria Could) N\u00c3O aparecem em PRD \u00a78 nem em FRD \u00a77, apesar de definidos em PRD \u00a74 com BR-Traced=BR-VA-001. Logo, 3 PRs Fase-2 recebem tratamento de rastreio divergente entre si.",
      "fix": "Uniformizar: ou os 3 PRs de Fase 2 (020/021/022) ficam fora de todas as matrizes de rastreio (s\u00e3o Could/Won't) com nota expl\u00edcita, ou todos entram com FR-stubs Fase-2. Remover PR-VA-022 da c\u00e9lula MR-VA-008 do PRD \u00a78 se a decis\u00e3o for mant\u00ea-lo s\u00f3 como Future."
    },
    {
      "id": "TRACE-08",
      "severity": "high",
      "doc": "06-data-model.md \u00a72/\u00a73 + 04-frd.md \u00a75 + 05-sdd.md \u00a77",
      "issue": "Chave de jun\u00e7\u00e3o load-bearing 'content_variant_id' sem artefato de origem. FR-VA-004/009/017 (monetiza\u00e7\u00e3o, m\u00e9tricas, atribui\u00e7\u00e3o de receita) todos chaveiam em content_variant_id; FRD \u00a75 e data-model \u00a72 declaram 'FK \u2192 criativo/content_library'. Por\u00e9m NENHUM doc define onde esse content_variant_id \u00e9 criado: grep de 'ADD COLUMN'/'ALTER TABLE' mostra que s\u00f3 scheduled_posts.cycle_id \u00e9 adicionado \u2014 content_library nunca recebe a coluna content_variant_id, e nenhuma tabela nova a produz. A cadeia FR-VA-004/009/017 \u2192 tabela tem o alvo da FK inexistente.",
      "fix": "Documentar a origem de content_variant_id: ou ALTER TABLE content_library ADD COLUMN content_variant_id uuid (+ onde a gera\u00e7\u00e3o o popula por criativo), ou definir que \u00e9 o pr\u00f3prio id de content_library e renomear o FK accordingly. Adicionar o stub na SDD \u00a77 e a coluna no data-model \u00a72."
    },
    {
      "id": "TRACE-09",
      "severity": "medium",
      "doc": "04-frd.md \u00a72 (FR-VA-013 'Should (MVP)') vs 03-prd.md \u00a74/\u00a75 e 00-index.md \u00a7Decis\u00e3o 2",
      "issue": "Contradi\u00e7\u00e3o de prioridade na feature que DEFINE o MVP. Index/BRD/PRD afirmam em tr\u00eas lugares 'MVP = TEXTO + IMAGEM'. PR-VA-008 (Image creative), pai de FR-VA-013, est\u00e1 em 'Must Have (MVP)' no PRD \u00a74 e inclu\u00eddo no escopo MVP do PRD \u00a75. Mas o FR que o realiza, FR-VA-013, \u00e9 marcado 'Should (MVP)' (e prioridade textual divergente das demais que usam Critical/High). Um FR 'Should' sob um PR 'Must' que \u00e9 a metade 'imagem' do MVP \u00e9 incoerente.",
      "fix": "Elevar FR-VA-013 para 'High' ou 'Critical' (consistente com o PR Must PR-VA-008 e com 'MVP=texto+imagem'), ou rebaixar PR-VA-008 e o claim de MVP. Padronizar a coluna Priority do FRD (usar a mesma escala Critical/High/Medium das outras FRs, n\u00e3o 'Should (MVP)')."
    }
  ],
  "notes": "Verifiquei as 4 matrizes (01 \u00a79, 02 \u00a710, 03 \u00a78, 04 \u00a77) + \u00edndice (00) + downstream (05 SDD, 06 data-model, 07 process-flow, 08 quality). Cobertura base OK: os 8 MR rastreiam BR 1:1; cada BR tem \u22651 PR; cada PR Must/Should tem PR-Traced; FR-VA-001..018 todos rastreiam \u22651 PR na tabela \u00a72 e t\u00eam artefato (tabela/edge fn/cron) no SDD/data-model. Os 5 PROC do 07 cobrem os FRs cr\u00edticos de gera\u00e7\u00e3o/cad\u00eancia/custo (FR-VA-002/005/007), MAS o FR cr\u00edtico-de-valor FR-VA-010/011 (loop R3) tem trigger contradit\u00f3rio (TRACE-03). Os 2 crons (autopilot-cadence, autopilot-collect) s\u00e3o consistentes entre SDD \u00a72.5/\u00a76 e process \u00a77 \u2014 por\u00e9m s\u00f3 2, o que colide com 'autopilot-analyze agendado' da FRD. PR-VA-009 n\u00e3o existe em lugar nenhum (numera\u00e7\u00e3o pula 008\u2192010, intencional). Quebras de cadeia reais e acion\u00e1veis: 9 findings (4 high, 5 medium). Veredito FAIL por inconsist\u00eancia m\u00fatua entre matrizes (TRACE-01/02/05), IDs \u00f3rf\u00e3os downstream (TRACE-06) e FK sem origem (TRACE-08). Nada fabricado: cada finding cita doc+se\u00e7\u00e3o lida nesta sess\u00e3o."
}
```

> **Tool Result (StructuredOutput)** - ✅ Success
>
> ```
> Structured output provided successfully
> ```

## 🤖 Claude *(21:12:13)*

Reprovei a suíte na dimensão Rastreabilidade (verdict: **fail**). Resumo das quebras de cadeia, todas verificadas contra os arquivos em `/home/gcrUX/htdocs/constellation-orchestra/docs/bok/viral-autopilot/`:

**Quebras estruturais (high):**
- **TRACE-01** — Matrizes MR→PR do BRD §10 e PRD §8 divergem: PRD adiciona PR-VA-012/013/022 a MR-VA-003/004/008 que o BRD não tem.
- **TRACE-02** — Resumo de cadeia do `00-index` contradiz as matrizes: omite PR-VA-008 de MR-VA-001 e atribui FR-VA-013 a PR-VA-002 (FR-VA-013 rastreia PR-VA-008).
- **TRACE-03** — FR-VA-010 (`autopilot-analyze`, motor do loop R3) tem trigger contraditório: FRD diz "agendado", mas só existem 2 crons em SDD/process-flow; PROC-VA-005 o trata como encadeado. O diferencial central do produto sem trigger/artefato consistente.
- **TRACE-06** — PR-VA-012 e PR-VA-013 (v1.0 Should, in-scope na FRD §1) aparecem na matriz PRD §8 mas têm ZERO FRs na FRD §7 — cadeia morre sem artefato.
- **TRACE-08** — `content_variant_id`, chave de junção de FR-VA-004/009/017, é declarada FK→`content_library` mas nenhum doc adiciona essa coluna (só `scheduled_posts.cycle_id` é provisionado). Alvo de FK inexistente.

**Inconsistências (medium):**
- **TRACE-04** — PR-VA-004 declara BR-VA-005 no PRD §4, mas as matrizes mapeiam BR-VA-005 só a PR-VA-007.
- **TRACE-05** — FR-VA-016 rastreia PR-VA-002 na tabela §2 mas PR-VA-001+PR-VA-002 na matriz §7 (contradição intra-doc).
- **TRACE-07** — PR-VA-022 está na matriz PRD §8 sem FR; PR-VA-020/021 (mesma categoria) não estão — tratamento divergente.
- **TRACE-09** — FR-VA-013 marcado "Should (MVP)" sob PR-VA-008 que é "Must (MVP)" e é a metade "imagem" do MVP declarado — prioridade incoerente + escala fora do padrão das demais FRs.

A cobertura-base passou (8 MR→BR 1:1, cada BR≥1 PR, FR-VA-001..018 todos com PR e artefato), mas a inconsistência mútua entre matrizes, os PRs órfãos a jusante e o FK sem origem reprovam a dimensão.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-17 - agent-acd33ce41f767d7ab]]
> * **Próxima Sessão**: [[2026-06-17 - agent-ad0c209a581d78aca]]
%% --- TIMELINE END --- %%

# Session agent-ae9dbcb4ac4d7fbaa
**Date:** 2026-07-16 | **Session ID:** `agent-ae9dbcb4ac4d7fbaa`

---

## 👤 User *(15:53:35)*


Você escreve documentação BoK RETROATIVA para o MCORCH (repo /home/gcrUX/htdocs/constellation-orchestra). REGRAS INEGOCIÁVEIS:
- Ground truth = /home/gcrUX/htdocs/constellation-orchestra/.claude/context/bok-readiness-audit-2026-07-16.json (auditoria adversarialmente verificada 2026-07-16: readers[].{blueprint_summary,shipped_state,drifts,doc_gaps,key_pointers} + verification[].{verified,refuted,missed}). LEIA-O PRIMEIRO.
- Lei 1 (Materialidade): a suíte documenta o ESTADO REAL DO CÓDIGO, não o blueprint. TODO drift listado no audit deve aparecer CORRIGIDO (documenta a realidade) — NUNCA copie claims do blueprint que o audit marcou como stale/divergente. Pointers file:line: use os key_pointers do audit e VERIFIQUE por leitura própria antes de citar.
- Idioma: prosa em PT-BR; termos técnicos/código em inglês. Formato: markdown com frontmatter '# <título>' + data 2026-07-16 + banner '> Suíte retroativa — consolida módulo JÁ SHIPADO; ground truth = código vivo + auditoria wf_2998d4c7'.
- Molde de forma: leia 2-3 docs equivalentes de /home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/ (suíte 9/9 recém-selada) para calibrar estrutura/tamanho. Templates em /home/gcrUX/htdocs/constellation-orchestra/.claude/agents/bok-scribe/templates/ se precisar.
- FRs/OTDs ganham tabela de STATUS REAL (vivo/gated/manual/não-shipado/fechada) com evidência.
- Escreva os arquivos com o Write tool nos paths indicados. Retorne APENAS JSON {files_written:[...], notes:'...'}.
MÓDULO video-repurpose (1 master externo → N shorts 9:16 + carrossel IG). Docs existentes que PERMANECEM na família: 00-deepsearch-blueprint.md (semente histórica) e 10-frd-sdd-viral-quality.md (FRD/SDD da fatia Viral Quality). Código: Fatias 1-3 + front-door host + Viral Quality VIVOS; Fatia 4 (mapeador FR-VR-008) NÃO shipada; FR-VR-013 (loop Vision) = processo MANUAL. Correções obrigatórias do audit: derivados são source_module='hyperframes' (só master='external'); carrossel NÃO passa por channel_profiles (OTD-VR-003 aberta, arquitetura real = publish-space-carousel→publish-social + marcador carousel_render_id); slides = FFmpeg puro (render-core diferido OTD-VR-007); legenda = drawtext byte-pad (não subtitles=); erro real 'ai_not_configured'; rail IG tem 3 superfícies (REELS/CAROUSEL/STORIES); commit 955117d na traceabilidade; smoke-carousel.ts é do POST-ENGINE (carousel-core IG não tem smoke próprio — registrar gap honesto). REPARO DE HOJE (2026-07-16, commit a729f83): gate BYOK do detect-viral-moments agora aceita Gemini-only (contrato FR-VR-010 cumprido — documentar como FECHADO).
SUA TAREFA: escrever /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-repurpose/01-mrd.md (Market Requirements — por que o módulo existe: mercado, Usuário Zero/brand-persona, doutrina USD-0/open-source-first, MRs numerados MR-XX), 02-brd.md (Business Requirements — BRs numerados com rastreio a MRs, modelo econômico mcoCoins real, riscos de negócio) e 03-prd.md (Product Requirements — PRs/jornadas de usuário reais das superfícies shipadas, UI existente). Grounde o racional de negócio no que a intro do blueprint + HANDOFF.md registram (grep pelo slug).

## 🤖 Claude *(15:53:44)*


## 🤖 Claude *(15:53:45)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/bok-readiness-audit-2026-07-16.json"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	{
> 2	  "summary": "Auditar prontidão dos módulos video-repurpose e youtube-studio para a suíte BoK 9/9 (drifts blueprint↔código)",
> 3	  "agentCount": 4,
> 4	  "logs": [],
> 5	  "result": {
> 6	    "readers": [
> 7	      {
> 8	        "module": "video-repurpose",
> 9	        "blueprint_summary": "Dois docs existem em docs/bok/video-repurpose/: (1) `00-deepsearch-blueprint.md` (2026-07-12, semente Closed-Loop Step 0) — tese \"o MCORCH distribui mas não produz cortes\", 5 Pilares (I Ingest externo · II Worker segment/reframe/caption · III Carrossel IG · IV Mapeador de metadados · V Fiar na distribuição), FR-VR-001..009, OTD-VR-001..007, FM-VR-01..05, Pattern Conformance 21 padrões, decisão de schema `source_module='external'` aditivo (§5), reuse-map (§6) e ordem de fatias com gates (§8). Referência externa = repo GabrielAI (pipeline INVERSO N→1, fonte do master + schema `episodios/epNN.json`). (2) `10-frd-sdd-viral-quality.md` (2026-07-13, FRD/SDD da Fatia 6 \"Viral Quality\") — FR-VR-010..015 (detector Hormozi, overlay motion-graphic alpha, template sem-botão, loop Vision-gated, caption_mode por clipe, UI 1-clique), extensão do `composition` jsonb (ClipSpec/TextBeat), Pattern Conformance própria, OTD-VR-008..013 e FM-VR-Q1..Q5. NÃO existem 00-index/01-mrd/02-brd/03-prd/04-frd/05-sdd/06-data-model/07-process-flow/08-quality-metrics — a suíte 9/9 é integralmente retroativa.",
> 10	        "shipped_state": "Módulo majoritariamente VIVO (Fatias 1-3 + front-door + Viral Quality; commits f703cc8→0e4393c→439d064→831f5cc→9f561c0→681002f→d4972c7→67dc54d). Verificado arquivo a arquivo: MIGRATIONS `supabase/migrations/20260712120000_creative_assets_external_source.sql` (CHECK + register_creative_asset union +'external') e `20260712130000_video_renders_repurpose_engine.sql` (engine +'repurpose'). EDGE FNS: `supabase/functions/ingest-external-asset/index.ts` (sign_upload owner-forced :61-80; YouTube gated 501 OTD-VR-001 :85-91; bucket 'local' ADMIN-only :95-104; registra master source_module='external' + metadata.{episode,srt} :131-144); `video-repurpose-run/index.ts` (sanitiza clips/slides/beats :33-74; resolve fonte owner-scoped :117-133; local admin-only :123-127; enfileira video_renders engine='repurpose' charged_mco=0 :139-141); `detect-viral-moments/index.ts` (FR-VR-010: parse SRT, sentinel pré-débito :106-110, BYOK per-user fail-closed 402 :113-119, DETECT_COST=3 débito+refund :21,125,250, LLM só escolhe índices de cues — beats verbatim do SRT :186-233, expansão de janela OTD-VR-013 :196-210, observação na malha :240-245); `publish-space-carousel/index.ts` (slides owner-scoped por source_job_id :57-60, modo agendado FR-SPACES-080 c/ marcador carousel_render_id :64-91, publish imediato via publish-social); branch CAROUSEL no `publish-social/index.ts:202-229` (children is_carousel_item→parent→media_publish). WORKERS HOST: `scripts/video-repurpose-bridge.ts` (claim atômico+reaper :50-56,157-159; guarda OTD-VR-006 no READ incl. realpath-containment do inbox local :72-93; registra derivados via register_creative_asset com parent_asset_id=master :103-127; finalize_video_render :140-143); cores `scripts/video-repurpose/segment-core.ts` (trim -ss/-t input-0 c/ anticorpo multi-input :88-90; reframe center-safe expression-crop :62-67; beats→renderAlphaFrames+overlay :79-103; drawtext UTF-8 byte-pad :110-115) e `carousel-core.ts` (slides 1080×1350 4:5, wrap MAX_CHARS=16 OTD-VR-007 :23-26,49-61) + `reconcile-srt-roteiro.py`; `scripts/host-upload-server.ts` (loopback 3220, upload chunked 80MB anti-cap CF, admin-gate, rota GET /api/host-media com Range) + infra versionada `infra/systemd/{video-repurpose-bridge,host-upload}.service` e `infra/nginx/host-upload.location.conf`. TEMPLATE `scripts/hyperframes/templates/viral-caption-overlay-9x16.html` (fundo transparente, Montserrat, textContent XSS-safe) + `renderAlphaFrames` em `scripts/hyperframes/render-core.ts:359,392` (omitBackground:true). UI: `src/pages/VideoRepurposePage.tsx` (602 linhas — upload .srt :366-376, \"Gerar cortes virais\" 1-clique FR-VR-015 c/ progresso ancorado em sinais reais :142-160,394-424, badge SRT :400-407, Distribuir→publish-space-asset :585) + `src/hooks/useVideoRepurpose.ts` (+useMasterSrtStatus :200-210). SOPs Lei 2: docs/processes/{external-video-ingest,video-repurpose-worker,repurpose-host-infra-provisioning,asr-master-to-srt}.md (ASR = whisper.cpp em /home/ubuntu/.mcorch/asr-engine/, US$0). Smokes re-executáveis: scripts/qa/{smoke-external-ingest,smoke-video-repurpose,smoke-carousel,smoke-scheduled-carousel}.ts. NÃO SHIPADO: FR-VR-008/Fatia 4 (mapeador metadado→legenda nativa+WordPress — zero refs em código) e FR-VR-013 como código (loop Vision automatizado — zero hits de MAX_VIRAL_ITERS/vision_score no repo; Vision QA foi manual por sessão). FR-VR-002 (YouTube) shipado como gate 501. Fatia 5 parcial: reuso do sink VIVO; alcance externo real gated em auditoria de app (ação Sovereign).",
> 11	        "drifts": [
> 12	          {
> 13	            "claim": "Blueprint §Pilar II afirma que os clipes derivados são registrados com source_module='external'; o código shipado registra os DERIVADOS (clipes e slides) como source_module='hyperframes' — só o MASTER é 'external'. Se o bok-scribe copiar o blueprint, o 06-data-model documentaria a proveniência errada.",
> 14	            "evidence": "Blueprint 00-deepsearch-blueprint.md:45 'clipes MP4 9:16 registrados creative_assets kind=video source_module=external (derivado, parent_asset_id=master)' vs scripts/video-repurpose-bridge.ts:106 e :123 'p_source_module: \\'hyperframes\\'' (register_creative_asset dos slides e clipes); master 'external' só em ingest-external-asset/index.ts:136",
> 15	            "severity": "material"
> 16	          },
> 17	          {
> 18	            "claim": "FR-VR-013 (loop Vision-gated com vision_score por short, limiar, iteração e cap MAX_VIRAL_ITERS=2) está especificado como requisito com critério de aceite no 10-frd, mas NÃO existe como código — o Vision QA foi executado manualmente por sessão. O 04-frd/08-quality-metrics retroativos devem registrá-lo como processo manual/aberto, não como implementado.",
> 19	            "evidence": "10-frd-sdd-viral-quality.md:35 (FR-VR-013) e :97 (§3.6 'Cap MAX_VIRAL_ITERS=2'); grep -rn 'MAX_VIRAL_ITERS|vision_score' em scripts/, supabase/functions/ e src/ → zero resultados",
> 20	            "severity": "material"
> 21	          },
> 22	          {
> 23	            "claim": "Blueprint §Pilar III diz que o carrossel 'Reusa a superfície carousel do channel_profiles' (OTD-VR-003); o caminho shipado NÃO passa por channel_profiles — publica direto via publish-space-carousel→publish-social, e o agendado usa marcador scheduled_posts.metadata.reshape.carousel_render_id (Amendment 22 do spaces). A migration de carousel do channel_profiles segue só LinkedIn/PDF (sem instagram). OTD-VR-003 continua aberta e a arquitetura real diverge do blueprint.",
> 24	            "evidence": "00-deepsearch-blueprint.md:48 vs supabase/functions/publish-space-carousel/index.ts:85 (metadata.reshape.carousel_render_id, channel 'instagram', surface 'carousel' — direto em scheduled_posts) e :101-109 (fetch direto publish-social); grep 'instagram' em migrations/20260628120000_channel_profiles_carousel.sql → zero matches",
> 25	            "severity": "material"
> 26	          },
> 27	          {
> 28	            "claim": "Blueprint §Pilar III afirma que os slides do carrossel são compostos 'via render-core.ts (HTML→PNG)'; o shipado é FFmpeg puro (drawtext/drawbox, sem Playwright) — a tipografia via render-core foi explicitamente diferida (OTD-VR-007). O próprio blueprint se contradiz internamente (§Pilar III vs tabela OTD-VR-007).",
> 29	            "evidence": "00-deepsearch-blueprint.md:48 'compõe slides via render-core.ts (HTML→PNG existente)' vs scripts/video-repurpose/carousel-core.ts:12 'Same deterministic FFmpeg family as segment-core; no Playwright' e :23-25 (MAX_CHARS=16, 'render-core HTML→PNG is deferred (OTD-VR-007)')",
> 30	            "severity": "minor"
> 31	          },
> 32	          {
> 33	            "claim": "Blueprint §Pilar II especifica queima de legenda via filtro FFmpeg 'subtitles=<srt>'; o shipado usa drawtext textfile por clipe (com anticorpo de padding UTF-8) + overlay de beats — o filtro subtitles nunca foi usado.",
> 34	            "evidence": "00-deepsearch-blueprint.md:44 'queima de legenda: subtitles=<srt>' vs scripts/video-repurpose/segment-core.ts:107-118 (drawtext textfile + byte-pad) e :79-97 (beats overlay)",
> 35	            "severity": "minor"
> 36	          },
> 37	          {
> 38	            "claim": "Claims-snapshot do blueprint §2 estão datados vs o código atual: 'publish-social IG só Reels... sem CAROUSEL' — a branch CAROUSEL foi shipada na Fatia 3. O bok-scribe não pode copiar a tabela §2 como estado atual; ela descreve o estado PRÉ-implementação (2026-07-12).",
> 39	            "evidence": "00-deepsearch-blueprint.md:25 'publish-social/index.ts:167 media_type REELS apenas; sem CAROUSEL' vs supabase/functions/publish-social/index.ts:202-229 (branch CAROUSEL completa: children is_carousel_item → parent media_type=CAROUSEL → media_publish)",
> 40	            "severity": "minor"
> 41	          },
> 42	          {
> 43	            "claim": "OTD-VR-012 no 10-frd carrega pendências já resolvidas: 'Ingest precisa aceitar SRT-file no upload (hoje metadata.srt só via API)' — a UI já sobe arquivo .srt; e o ASR self-host (whisper.cpp) saiu do 'opção futura' para motor vivo com SOP (commit 67dc54d). A suíte deve refletir o fechamento.",
> 44	            "evidence": "10-frd-sdd-viral-quality.md:142 vs src/pages/VideoRepurposePage.tsx:366-376 (input accept='.srt,.vtt' → setSrtPt) e docs/processes/asr-master-to-srt.md (engine /home/ubuntu/.mcorch/asr-engine/whisper.cpp, modelo large-v3-turbo-q5_0)",
> 45	            "severity": "minor"
> 46	          },
> 47	          {
> 48	            "claim": "Código de erro do detector diverge do FRD: FR-VR-010 promete 402 '<provider>_not_configured'; o código retorna 'ai_not_configured'. Cosmético, mas o 04-frd retroativo deve fixar o contrato real.",
> 49	            "evidence": "10-frd-sdd-viral-quality.md:32 vs supabase/functions/detect-viral-moments/index.ts:119 'return json({ error: \"ai_not_configured\", ... }, 402)'",
> 50	            "severity": "minor"
> 51	          },
> 52	          {
> 53	            "claim": "Referências de linha do 10-frd ao segment-core drifted após as edições da fatia beats: 'drawtext... :71-82' — hoje o drawtext legado está em ~:107-118 (a :71-82 atual é o renderClip/beats). Snapshot cosmético; a suíte deve re-derivar pointers.",
> 54	            "evidence": "10-frd-sdd-viral-quality.md:15 'segment-core.ts:71-82 (drawtext textfile...)' vs scripts/video-repurpose/segment-core.ts:107-118 (bloco drawtext atual)",
> 55	            "severity": "minor"
> 56	          }
> 57	        ],
> 58	        "doc_gaps": [
> 59	          "01-mrd/02-brd/03-prd inexistentes: o racional de mercado/negócio (por que repurpose de documentário, GabrielAI como fonte do master, estratégia Usuário Zero/brand-persona, rail 100% grátis US$0 como decisão de negócio) vive só na intro do blueprint e na memória — precisa de consolidação formal.",
> 60	          "06-data-model inexistente: schema consolidado de (a) creative_assets com source_module='external' (master) vs 'hyperframes' (derivados) + parent_asset_id + source_job_id como modelo de proveniência; (b) video_renders.composition jsonb (ClipSpec {in_sec,out_sec,reframe,caption,caption_mode,text_beats[]} e SlideIn {t_sec,caption} + handle + fps — contratos hoje só em código); (c) metadata.{episode,srt} do master (schema epNN.json); (d) marcador scheduled_posts.metadata.reshape.carousel_render_id do caminho agendado.",
> 61	          "07-process-flow inexistente: o fluxo E2E real está espalhado em 4 SOPs + HANDOFF — precisa do fluxo unificado: upload chunked 80MB → host-upload-server 3220 → repurpose-inbox/<uid>/ (admin-only) OU sign_upload→bucket privado → ingest-external-asset → (ASR whisper.cpp se sem SRT) → detect-viral-moments → video-repurpose-run → video-repurpose-bridge (segment-core/carousel-core) → register_creative_asset → publish-space-asset / publish-space-carousel (imediato ou agendado) → auto-publish → publish-social.",
> 62	          "08-quality-metrics inexistente: rubrica Vision viral (hook-2s/legibilidade som-off/ritmo/reenquadre), scores reais provados (EP01: 9.0/9.5/8.5, Vision 7-8/10), status HONESTO do FR-VR-013 (loop automatizado NÃO shipado — Vision manual por sessão), anticorpos como métricas de regressão (drawtext UTF-8 byte-pad, -t multi-input do FFmpeg, OTD-VR-013 tuning de janela) e os 4 smokes re-executáveis como gates.",
> 63	          "Registro consolidado de FRs com status real: FR-VR-001..015 estão em DOIS docs com numeração contínua — a suíte precisa da tabela única com status (001 vivo · 002 gated 501 · 003-007 vivos · 008 NÃO shipado · 009 parcial-gated · 010-012 vivos · 013 manual/aberto · 014-015 vivos) + o vínculo FR-CP-012 (post-engine) destravado.",
> 64	          "Ledger de OTDs com status atual: VR-001 aberta(gated) · VR-002 aberta · VR-003 aberta E caminho shipado divergiu do plano · VR-005 fechada (FR-VR-010) · VR-006 fechada · VR-007 aberta · VR-008 fechada por decisão · VR-009 aberta (prova no smoke) · VR-010 aberta (DETECT_COST=3 não calibrado 4×-floor formal) · VR-012 majoritariamente fechada (SRT UI + ASR vivo) · VR-013 parcialmente fechada em código (expansão de janela no detector).",
> 65	          "Modelo de segurança consolidado: duplo admin-gate do source local (ingest + run), guarda OTD-VR-006 no READ com realpath-containment, sentinel pré-débito no detector, BYOK per-user fail-closed, textContent XSS-safe, disclosure sintética preservada — hoje espalhado em comentários de código e SOPs.",
> 66	          "Superfície de infra host não-containerizada: os 2 systemd units + nginx location agora versionados em infra/ + a nota de materialidade do SOP de provisionamento (bloco nginx é forma DERIVADA, não capturada do host) — a suíte deve apontar isso como caveat Lei 1.",
> 67	          "Fatias 4/5 como roadmap honesto: mapeador de metadados (FR-VR-008, OTD-VR-004 decisão adaptar-reshape-vs-mapper NUNCA tomada) e E2E de alcance externo real (gated auditoria de app IG/TikTok — ação Sovereign, não código)."
> 68	        ],
> 69	        "readiness_verdict": "ready_with_corrections",
> 70	        "key_pointers": [
> 71	          "docs/bok/video-repurpose/00-deepsearch-blueprint.md (semente — §2 é snapshot PRÉ-implementação, não copiar como estado atual)",
> 72	          "docs/bok/video-repurpose/10-frd-sdd-viral-quality.md (FRD/SDD Fatia 6 — FR-VR-010..015 + OTD-VR-008..013)",
> 73	          "supabase/migrations/20260712120000_creative_assets_external_source.sql (source_module +'external' + register_creative_asset union)",
> 74	          "supabase/migrations/20260712130000_video_renders_repurpose_engine.sql (engine +'repurpose', charged_mco=0)",
> 75	          "supabase/functions/ingest-external-asset/index.ts:61-80,85-91,95-111,131-144 (sign_upload owner-forced · YouTube 501 gated · local admin-only · master external + metadata.{episode,srt})",
> 76	          "supabase/functions/video-repurpose-run/index.ts:33-74,117-141 (sanitização clips/slides/beats · resolve owner-scoped · enqueue)",
> 77	          "supabase/functions/detect-viral-moments/index.ts:21,106-127,186-233 (DETECT_COST=3 · sentinel pré-débito · BYOK fail-closed · beats verbatim do SRT + expansão de janela OTD-VR-013)",
> 78	          "supabase/functions/publish-space-carousel/index.ts:57-91,101-109 (slides owner-scoped · modo agendado carousel_render_id · publish imediato)",
> 79	          "supabase/functions/publish-social/index.ts:202-229 (branch IG CAROUSEL — children→parent→media_publish)",
> 80	          "scripts/video-repurpose-bridge.ts:72-93 (guarda OTD-VR-006 no READ + realpath containment do inbox local) e :103-127 (derivados p_source_module='hyperframes' + parent_asset_id=master — a proveniência REAL)",
> 81	          "scripts/video-repurpose/segment-core.ts:62-67,79-103,107-118 (reframe expression-crop · beats overlay + anticorpo -ss/-t multi-input · drawtext UTF-8 byte-pad)",
> 82	          "scripts/video-repurpose/carousel-core.ts:20-27,49-61 (1080×1350 4:5 · wrapCaption MAX_CHARS=16 — OTD-VR-007)",
> 83	          "scripts/hyperframes/render-core.ts:359,392 (renderAlphaFrames omitBackground:true) + scripts/hyperframes/templates/viral-caption-overlay-9x16.html (transparente, Montserrat, XSS-safe)",
> 84	          "scripts/host-upload-server.ts (3220 · chunked 80MB anti-cap CF · admin-gate · GET /api/host-media Range) + infra/systemd/{video-repurpose-bridge,host-upload}.service + infra/nginx/host-upload.location.conf",
> 85	          "src/pages/VideoRepurposePage.tsx:142-160,366-376,394-424,585 (1-clique FR-VR-015 · upload .srt · badge SRT · Distribuir) + src/hooks/useVideoRepurpose.ts:200-210 (useMasterSrtStatus)",
> 86	          "docs/processes/external-video-ingest.md · video-repurpose-worker.md · repurpose-host-infra-provisioning.md · asr-master-to-srt.md (as 4 SOPs Lei 2 do módulo)",
> 87	          "scripts/qa/smoke-external-ingest.ts · smoke-video-repurpose.ts · smoke-carousel.ts · smoke-scheduled-carousel.ts (anticorpos re-executáveis)",
> 88	          "docs/bok/post-engine/12-amendment-channel-format-intelligence.md:83 + 13-sdd-reshaper-atomizer.md:196 (FR-CP-012 — o gap que este motor destrava)",
> 89	          "Commits: f703cc8 (blueprint) · 0e4393c (F1 ingest) · 439d064 (F2 worker) · 831f5cc (F3 carrossel) · 9f561c0 (front-door host) · 681002f (fix UTF-8) · d4972c7 (Viral Quality) · 67dc54d (ASR)"
> 90	        ]
> 91	      },
> 92	      {
> 93	        "module": "youtube-studio",
> 94	        "blueprint_summary": "Três docs coexistem sob o slug com DUAS visões distintas: (A) `00-deepsearch-blueprint.md` (v0.1.0, 2026-07-09, 53KB) define o youtube-studio como FÁBRICA DE VÍDEO LONG-FORM 16:9 da persona CCIO — 6 pilares (assembler FFmpeg normalize-then-concat, lipsync MuseTalk/SadTalker/OmniHuman, YouTube Data API avançada, legendas ASS, thumbnail, render 16:9), 14 OTDs (YTS-001..014), FMEA-seed FM-YTS-01..11, fatias 0-5 (Fatia 1 = destravar engine='faceless' 503-gated do video-render), gates de monetização (inauthentic-content channel-wide + containsSyntheticMedia disclosure) como requisito FRD mandatório, doutrina USD-0/licenças verificadas (Remotion REJECT, Wav2Lip bloqueado, Hedra API Terms proíbem integração). (B) `11-api-surface-map.md` (2026-07-12) + `youtube-api-registry.json` definem o PAINEL de gestão de canal: matriz de 10 escopos OAuth, 13 recursos Data API v3 (175 props), 52 métricas + 32 dimensões Analytics v2, registro de 33 ações write/destrutivas com TIER de risco, custos de quota (§5.1: refresh ≈4 unidades), Pattern Conformance 21 padrões (yes 12 · deferred 6 · n-a 5), fatias próprias (1=read, 2=write, 3=destrutivo com dry-run+confirmação dupla). (C) `12-amendment-write-ops-and-monetary.md` (2026-07-14) = FR-YT-020..025: update_video/delete_video gated force-ssl + revenue_metrics gated yt-analytics-monetary.readonly + os 4 escopos demonstráveis p/ verificação Google + gates Y1-Y6. Amendment 12 é o spec efetivamente shipado.",
> 95	        "shipped_state": "SHIPADO E VERIFICADO NO CÓDIGO: (1) `supabase/functions/youtube-data/index.ts` (330 linhas) — 7 actions (channel_summary, list_videos, video_metrics, video_categories, revenue_metrics, update_video, delete_video); token per-user server-side via `decrypted_social_accounts` com filtro `user_id` load-bearing (:119-125), refresh auto via `refresh-social-token` (:44-70), gate fail-closed de escopo ANTES do Google (:137-164, retorna 403 `youtube_scope_missing` + CTA), read-modify-write do snippet no update preservando categoryId (:294-307), delete 204-tolerante (:314-322), revenue fail-soft `{monetized:false}` em 403 (:273-284), telemetria `infra_health_logs service='youtube-studio'` (:100-101). (2) `social-auth-init/index.ts:151-156` — os 4 escopos do Amendment 12 (youtube.readonly, youtube, youtube.force-ssl, yt-analytics-monetary.readonly) com `access_type=offline&prompt=consent` (:157); callback persiste `scopes` concedidos (:88,114,320-337 de social-auth-callback). (3) UI: rota `/dashboard/youtube` (App.tsx:131), `useYouTubeStudio.ts` deriva hasReadScope/hasAnalyticsScope (monetário=superset :110-113)/hasWriteScope da view mascarada; `YouTubeStudioPage.tsx` (589 linhas) — card Receita gated hasMonetaryScope (:579), botões Editar/Excluir gated canWrite (:303-311), AlertDialog destrutivo (:402-421), CTA \"Reconectar com permissões ampliadas\" (:512). (4) Publish YouTube já vivo em `publish-social/index.ts:502-587` — videos.insert resumable com `selfDeclaredMadeForKids:false` (:538) e `containsSyntheticMedia:true` (:539) hardcoded (os 2 gates de disclosure do blueprint JÁ no publish path). (5) Smoke `scripts/qa/smoke-youtube-write-ops.ts` 9 gates zero-custo (401/400/409/403×3/400×2). (6) SOPs Lei 2: `docs/processes/youtube-studio-panel.md` + `youtube-publish-credential-resolution.md`. NÃO SHIPADO (proposta-apenas do blueprint): assembler multi-cena, youtube-lipsync (zero código MuseTalk/SadTalker no repo — grep confirma; só `fal_api_key` OmniHuman do módulo avatar-clone-ai, migration 20260630000000), thumbnails.set, playlists.insert; `engine='faceless'` segue 503-gated (`video-render/index.ts` header + bloco `render_engine_unavailable` quando VIDEO_FACELESS_WEBHOOK unset; COST faceless:125 na linha 23); template `viral-long-16x9` existe na allowlist (`render-core.ts:90`) e no disco.",
> 96	        "drifts": [
> 97	          {
> 98	            "claim": "Cisma de escopo do módulo: o 00-blueprint define youtube-studio como fábrica long-form (Fatia 1 = faceless assembler), enquanto 11+12 e o código shipado definem um painel de gestão de canal (Fatia 1 = read-only, Fatia 2 = write). A numeração de Fatias colide entre os docs da mesma família — se o bok-scribe não reconciliar, a suíte nasce com dois roadmaps contraditórios sob os mesmos labels.",
> 99	            "evidence": "00-deepsearch-blueprint.md §9 'Fatia 1 — Faceless assembler (destrava o engine já codado)' vs 11-api-surface-map.md §7 'Fatia 1 — Tabela CRUD read-only de vídeos'; shipado = youtube-data/index.ts (painel), nenhum assembler existe",
> 100	            "severity": "blocker"
> 101	          },
> 102	          {
> 103	            "claim": "O 'GAP CRÍTICO' do surface-map §1 e o registry json afirmam que a conexão concede APENAS youtube.upload — STALE: social-auth-init pede os 4 escopos do Amendment 12 (e youtube.upload nem está mais no pedido; videos.insert é coberto pelo escopo `youtube`). Se o registry for tratado como estado atual, contamina a suíte.",
> 104	            "evidence": "youtube-api-registry.json: \"currentConnectionGap\": {\"grantedScopes\": [\"youtube.upload\"]...} (gerado 2026-07-12) vs social-auth-init/index.ts:151-156 (youtube.readonly + youtube + youtube.force-ssl + yt-analytics-monetary.readonly)",
> 105	            "severity": "material"
> 106	          },
> 107	          {
> 108	            "claim": "11-api-surface-map §7 Fatia 2 afirma 'Toda ação debita mcoCoins e emite infra_health_logs' — o débito mcoCoins NÃO existe no código: youtube-data não tem nenhuma chamada a deduct_mco_coins, e billing.ts não tem chave para o painel. Amendment 12 (o spec shipado) omite billing. A suíte precisa selar a postura real: ações do painel são gratuitas hoje.",
> 109	            "evidence": "grep 'deduct_mco' em supabase/functions/youtube-data/index.ts = 0 hits; grep 'youtube' em src/lib/billing.ts = 0 hits; vs 11-api-surface-map.md:443 'Toda ação debita mcoCoins e emite infra_health_logs'",
> 110	            "severity": "material"
> 111	          },
> 112	          {
> 113	            "claim": "Pattern Conformance #8 (Memory Management) declarado 'yes' com 'Nós de observação na Knowledge Mesh (mcorch_nodes) por sync bem-sucedido' e o SOP tem seção Mesh Connection Mandate idêntica — NÃO implementado: youtube-data só pulsa infra_health_logs; não há INSERT em mcorch_nodes em nenhum path da função (arquivo inteiro lido). Mesh Connection Mandate (CLAUDE.md §3) descoberto pelo código shipado.",
> 114	            "evidence": "youtube-data/index.ts:100-101 (único sink = infra_health_logs); 11-api-surface-map.md §6 linha do pattern #8 'yes — Nós de observação na Knowledge Mesh (mcorch_nodes) por sync bem-sucedido'; docs/processes/youtube-studio-panel.md §Mesh Connection Mandate",
> 115	            "severity": "material"
> 116	          },
> 117	          {
> 118	            "claim": "Fatia 3 do surface-map especifica delete com dry-run (leitura prévia do que será removido) + confirmação dupla 'digitar o ID ou EXCLUIR' + trilha de auditoria na mesh por delete — o shipado (Amendment 12, Fatia 2) puxou o delete_video antecipadamente com UM AlertDialog simples, sem dry-run e sem nó de mesh. Amendment 12 §3 é o contrato real; a suíte deve superseder o §7 Fatia 3 do map ou re-escopar o restante como futuro.",
> 119	            "evidence": "11-api-surface-map.md:450-452 ('(1) dry-run... (2) confirmação dupla (digitar o ID ou \"EXCLUIR\")... registrar... nó de observação na mesh todo delete') vs youtube-data/index.ts:314-322 (delete direto pós-gate) + YouTubeStudioPage.tsx:402-421 (AlertDialog único)",
> 120	            "severity": "material"
> 121	          },
> 122	          {
> 123	            "claim": "SOP youtube-studio-panel.md fixa o pedido OAuth em 5 escopos (youtube.readonly + youtube.upload + youtube.force-ssl + yt-analytics.readonly + yt-analytics-monetary.readonly) — o código pede 4 diferentes (adiciona `youtube` amplo, remove youtube.upload e yt-analytics.readonly; monetário é superset do não-monetário, FR-YT-023). SOP stale vs Amendment 12/código.",
> 124	            "evidence": "docs/processes/youtube-studio-panel.md §Pré-condição item 1 ('conjunto completo... youtube.readonly, youtube.upload, youtube.force-ssl, yt-analytics.readonly, yt-analytics-monetary.readonly') vs social-auth-init/index.ts:151-156",
> 125	            "severity": "minor"
> 126	          },
> 127	          {
> 128	            "claim": "Blueprint cita 'scope youtube.upload + refresh offline (social-auth-init/index.ts:139-140)' como estado do OAuth — superseded: essas linhas hoje carregam o comentário do prompt=consent e o bloco de 4 escopos do Amendment 12. Era verdade em 2026-07-09; não copiar como estado atual.",
> 129	            "evidence": "00-deepsearch-blueprint.md §1 item 2 vs social-auth-init/index.ts:139-157 (lido nesta sessão)",
> 130	            "severity": "minor"
> 131	          },
> 132	          {
> 133	            "claim": "Realidade operacional ≠ docs: o gate material da própria Fatia 1 (reports.query com ≥1 linha) ainda não é provável — a YouTube Analytics API não foi habilitada no Cloud project e o Sovereign ainda não reconectou (test-user) com os 4 escopos novos; verificação data-access do Google pendente. A suíte deve registrar como OTDs abertas com owner Sovereign, nunca como done.",
> 134	            "evidence": "HANDOFF.md:178 ('reconectar YouTube (test-user) p/ os 4 escopos novos' + 'Data-access verification'), :252 ('habilitar YouTube Analytics API'), :287; sprint-priorities.md:22 ('analytics adiado até habilitar a YouTube Analytics API')",
> 135	            "severity": "material"
> 136	          },
> 137	          {
> 138	            "claim": "Tensão cross-módulo em lipsync: o blueprint youtube-studio manda default self-host MuseTalk USD-0 e proíbe codificar sobre Hedra sem deal (OTD-YTS-002, API Terms proíbem integração verbatim), mas o módulo irmão avatar-clone-ai já selou 'Hedra Character-3 default ~$35/ciclo' e só tem BYOK fal/OmniHuman cabeado. Nenhum código MuseTalk/SadTalker existe. A suíte precisa reconciliar qual doutrina vale para o modo avatar-clone do YouTube.",
> 139	            "evidence": "00-deepsearch-blueprint.md OTD-YTS-002 ('Não codificar avatar-clone sobre Hedra sem GO') vs scripts/reconcile-kanban-roadmap.ts:69 ('Economics fechado — Hedra ~$35/mês (default)') + migration 20260630000000_user_api_keys_avatar_byok.sql (fal_api_key OmniHuman); grep musetalk/sadtalker no repo = 0 hits de código",
> 140	            "severity": "minor"
> 141	          }
> 142	        ],
> 143	        "doc_gaps": [
> 144	          "Os 9 docs canônicos não existem: docs/bok/youtube-studio/ tem só 00, 11, 12, _apimap/ e o registry json (ls verificado) — 00-index, 01-mrd, 02-brd, 03-prd, 04-frd, 05-sdd, 06-data-model, 07-process-flow, 08-quality-metrics são todos green-field.",
> 145	          "Decisão de escopo do módulo (a mais importante): o slug abriga painel-de-canal (shipado) E fábrica long-form (blueprint, unbuilt). A suíte precisa declarar a arquitetura guarda-chuva com dois tracks — Track A painel (FR-YT-0xx, shipado, retroativo) e Track B fábrica (FR-YTS-0xx, roadmap) — e renumerar as Fatias colidentes.",
> 146	          "06-data-model: nenhum doc descreve a superfície de dados real do módulo — não há tabela dedicada; tudo reusa social_accounts (scopes[], tokens Vault via decrypted_social_accounts), social_app_config (app creds BYOK), infra_health_logs service='youtube-studio'. O data model é 100% reuso e isso precisa ser dito explicitamente (inclusive a decisão de NÃO ter cache de metadados de canal, contradizendo o Pattern #8).",
> 147	          "Postura de billing selada: ações do painel custam 0 mco hoje (só quota do Google, USD-0 direto). A suíte deve documentar isso como decisão (ou criar chave COIN_COSTS) — hoje o 11 afirma débito que não existe.",
> 148	          "Mesh Connection Mandate: plano de implementação do observation node no primeiro sync bem-sucedido (ou OTD honesta de deferimento) — o código shipado viola o mandate do CLAUDE.md §3 e a Pattern Conformance declara 'yes' indevidamente.",
> 149	          "OTDs de lifecycle Google com owner Sovereign: (a) reconectar test-user com os 4 escopos; (b) habilitar YouTube Analytics API no Cloud project; (c) publicar branding no console (expira em 7 dias, HANDOFF:178); (d) data-access verification (review do vídeo demo dos 4 escopos); (e) classificação sensitive/restricted + CASA segue '(não verificado)' — a página oauth2/scopes truncou em toda captura (11 §8).",
> 150	          "08-quality-metrics: aproveitar o orçamento de quota do §5.1 (refresh ≈4 un, ~2.500 refreshes/dia, evitar search.list 100 un) + smoke-youtube-write-ops 9/9 como gate de regressão + os gates Y1-Y6 do Amendment 12 (Y3/Y4 ainda abertos — dependem da reconexão).",
> 151	          "07-process-flow: os 2 SOPs existentes (youtube-studio-panel.md, youtube-publish-credential-resolution.md) cobrem painel-read e publish; falta o flow de write/destrutivo (Amendment 12) e a correção do conjunto de escopos no SOP do painel.",
> 152	          "09-pattern-conformance: promover a tabela 21-padrões do 11 §6 + delta do 12 §4, CORRIGINDO #8 (Memory Management yes→deferred até o observation node existir) e registrando #13 como shipado (AlertDialog) em vez do dry-run+type-to-confirm nunca construído.",
> 153	          "Carry-over honesto dos pilares unbuilt do blueprint como FRs deferidas com OTDs vivas: assembler (FR-YTS-001/002), lipsync (FR-YTS-004/005 + reconciliação com avatar-clone-ai/Hedra), thumbnails.set (FR-YTS-007), playlists/Shorts (FR-YTS-008), destravamento do engine='faceless' 503-gated (OTD-VS-001) — nada disso virou código e não pode ser descrito como shipado.",
> 154	          "Registrar que os 2 gates de disclosure do blueprint JÁ estão parcialmente shipados no publish path (publish-social:538-539 hardcoda selfDeclaredMadeForKids:false + containsSyntheticMedia:true) — mas como constantes, não como input por-upload computado de classificação de realismo como o blueprint §2 Pilar III exige; o FRD deve capturar o delta."
> 155	        ],
> 156	        "readiness_verdict": "ready_with_corrections",
> 157	        "key_pointers": [
> 158	          "supabase/functions/youtube-data/index.ts:1-330 — chokepoint único do painel; scope-gate fail-closed :137-164; update read-modify-write :288-311; delete :314-322; revenue fail-soft :264-285; telemetria :100-101; SEM deduct_mco e SEM mcorch_nodes",
> 159	          "supabase/functions/social-auth-init/index.ts:125-157 — os 4 escopos reais (:151-156) + access_type=offline&prompt=consent (:157); youtube.upload NÃO está mais no pedido",
> 160	          "supabase/functions/social-auth-callback/index.ts:88,114,320-337 — scopes concedidos persistidos em social_accounts.scopes (sinal de verdade do gap)",
> 161	          "supabase/functions/publish-social/index.ts:502-587 — videos.insert resumable; selfDeclaredMadeForKids:false (:538) e containsSyntheticMedia:true (:539) hardcoded",
> 162	          "src/hooks/useYouTubeStudio.ts:12-13,102-122,188-203 — derivação de escopos da view mascarada; monetário=superset; mutations update/delete",
> 163	          "src/pages/YouTubeStudioPage.tsx:303-311,402-421,512,579-586 — Editar/Excluir gated force-ssl; AlertDialog destrutivo; card Receita gated monetário; CTA reconexão",
> 164	          "src/App.tsx:30,131 — rota lazy /dashboard/youtube",
> 165	          "scripts/qa/smoke-youtube-write-ops.ts — 9 gates zero-custo do contrato fail-closed (regressão re-executável)",
> 166	          "supabase/functions/video-render/index.ts:23 (COST faceless:125/hyperframes:12) + bloco render_engine_unavailable 503 — engine='faceless' segue NÃO wired (confirma blueprint §6)",
> 167	          "scripts/hyperframes/render-core.ts:90 — VALID_TEMPLATES inclui viral-long-16x9; template presente em scripts/hyperframes/templates/",
> 168	          "docs/bok/youtube-studio/{00-deepsearch-blueprint.md,11-api-surface-map.md,12-amendment-write-ops-and-monetary.md} + youtube-api-registry.json (currentConnectionGap STALE) + _apimap/ (11 mapas-fonte)",
> 169	          "docs/processes/youtube-studio-panel.md (SOP Fatia 1; conjunto de escopos STALE) + docs/processes/youtube-publish-credential-resolution.md (SOP publish per-user)",
> 170	          "HANDOFF.md:178,252,287 — pendências honestas: reconectar test-user 4 escopos · habilitar YouTube Analytics API · branding console (7d) · data-access verification",
> 171	          "supabase/migrations/20260630000000_user_api_keys_avatar_byok.sql — fal_api_key OmniHuman (único BYOK de lipsync existente; MuseTalk/SadTalker = zero código)"
> 172	        ]
> 173	      }
> 174	    ],
> 175	    "verification": [
> 176	      {
> 177	        "module": "video-repurpose",
> 178	        "verified": [
> 179	          "DRIFT 1 (proveniência dos derivados) CONFIRMADO com leitura própria: blueprint 00-deepsearch-blueprint.md:45 afirma clipes derivados 'source_module=external'; scripts/video-repurpose-bridge.ts registra slides (:106) e clipes (:123) com p_source_module:'hyperframes'; só o MASTER é 'external' (ingest-external-asset/index.ts:136 literal p_source_module:\"external\"). Um 06-data-model copiado do blueprint documentaria a proveniência errada.",
> 180	          "DRIFT 2 (FR-VR-013 não é código) CONFIRMADO por grep próprio: 'MAX_VIRAL_ITERS|vision_score' em scripts/, supabase/functions/ e src/ = ZERO hits; únicas ocorrências são no próprio 10-frd-sdd-viral-quality.md (:35,:97,:118,:141,:151). O loop Vision-gated existe só como requisito e processo manual por sessão.",
> 181	          "DRIFT 3 (carrossel não passa por channel_profiles; OTD-VR-003 aberta) CONFIRMADO: publish-space-carousel/index.ts:85 grava marcador metadata.reshape.carousel_render_id (channel 'instagram', surface 'carousel') DIRETO em scheduled_posts; :101-109 publica imediato via fetch direto ao publish-social; auto-publish/index.ts:133-141 resolve o marcador owner-bound (.eq user_id) sem tocar channel_profiles; grep 'instagram' em 20260628120000_channel_profiles_carousel.sql = exit 1 (migration é só linkedin/PDF, comentário ':7' diz 'IG/TikTok photo-carousel ... later slice'). Arquitetura real diverge do blueprint:48.",
> 182	          "DRIFT 4 (slides = FFmpeg puro; contradição interna do blueprint) CONFIRMADO: carousel-core.ts:12 'Same deterministic FFmpeg family as segment-core; no Playwright' + :23-25 MAX_CHARS=16 e 'render-core HTML→PNG is deferred (OTD-VR-007)'; blueprint §Pilar III (:48) diz render-core enquanto a própria tabela OTD (:77) descreve drawtext/MAX_CHARS — contradição interna real (o §Pilar III não foi atualizado quando OTD-VR-007 foi acrescida pós-implementação).",
> 183	          "DRIFT 5 (filtro subtitles= nunca usado) CONFIRMADO: blueprint:44 'queima de legenda: subtitles=<srt>' vs segment-core.ts — drawtext textfile com anticorpo de padding UTF-8 byte-vs-char (:107-118, pad :110-115) + overlay de beats via renderAlphaFrames (:79-103). Zero ocorrência de 'subtitles=' no core.",
> 184	          "DRIFT 6 (claims-snapshot §2 datado) CONFIRMADO: blueprint:25 'media_type REELS apenas; sem CAROUSEL' vs branch CAROUSEL completa e viva em publish-social/index.ts (~:203-231: children is_carousel_item → parent media_type=CAROUSEL → media_publish). A tabela §2 descreve o estado PRÉ-implementação (2026-07-12) e não pode ser copiada como estado atual.",
> 185	          "DRIFT 7 (OTD-VR-012 carrega pendências resolvidas) CONFIRMADO: FRD:142 diz 'Ingest precisa aceitar SRT-file no upload' e 'ASR ... opção futura', mas VideoRepurposePage.tsx:366-376 tem input accept='.srt,.vtt,text/plain' → setSrtPt, e docs/processes/asr-master-to-srt.md documenta motor VIVO (whisper.cpp em /home/ubuntu/.mcorch/asr-engine/, modelo ggml-large-v3-turbo-q5_0, US$0); commit 67dc54d existe (git log 2026-07-14 'feat(video-repurpose): ASR self-host (whisper.cpp) + reconciliação roteiro-autoritativa').",
> 186	          "DRIFT 8 (código de erro do detector) CONFIRMADO: detect-viral-moments/index.ts:119 retorna literal { error: \"ai_not_configured\" } 402 vs FRD:32 que promete '402 <provider>_not_configured'.",
> 187	          "DRIFT 9 (pointers do FRD ao segment-core drifted) CONFIRMADO: FRD:15 cita 'segment-core.ts:71-82 (drawtext textfile...)'; hoje :71-82 é o início do renderClip + branch beats (FR-VR-011); o bloco drawtext legado está em :107-118.",
> 188	          "SHIPPED núcleo CONFIRMADO arquivo a arquivo com leitura própria: migrations 20260712120000 (CHECK creative_assets + RPC register_creative_asset union +'external'; NENHUMA migration posterior redefine a RPC — 'external' preservado na definição vigente) e 20260712130000 (engine CHECK +'repurpose'); ingest-external-asset (sign_upload key server-forced ${uid}/ :61-80 · YouTube 501 OTD-VR-001 :85-91 · bucket 'local' admin-only via user_roles :95-104 · registra master external + metadata.{episode,srt} :131-144); video-repurpose-run (sanitize clips/slides/beats :33-74 · fonte owner-scoped :117-133 · local admin-only :123-127 · enqueue engine='repurpose' charged_mco=0 :139-141); detect-viral-moments (sentinel PRÉ-débito :104-110 · BYOK fail-closed 402 :113-119 · DETECT_COST=3 débito+refund :21/:125/:250 · LLM só escolhe índices, beats verbatim do SRT :186-233 · expansão de janela OTD-VR-013 :196-210 · observação na malha :240-245); bridge (claim atômico :50-56 · reaper :157-159 · OTD-VR-006 no READ incl. realpath-containment do inbox :72-93 · finalize_video_render :140-143).",
> 189	          "SHIPPED superfície host/UI CONFIRMADO: host-upload-server.ts (loopback 3220, admin-gate user_roles :75-77, GET /api/host-media com Range/206 :81-101; chunk do cliente = CHUNK_BYTES 80MB em useVideoRepurpose.ts:68, sob o cap CF de 100MB/request); infra/systemd/{video-repurpose-bridge,host-upload}.service + infra/nginx/host-upload.location.conf versionados (com caveat Lei 1 no SOP repurpose-host-infra-provisioning.md: bloco nginx é forma DERIVADA, não capturada); template viral-caption-overlay-9x16.html (background:transparent, Montserrat, textContent XSS-safe) + renderAlphaFrames em render-core.ts:359 com omitBackground:true :392; VideoRepurposePage.tsx = 602 linhas exatas (FR-VR-015 doViralCuts :142-165 com progresso ancorado em sinais reais, painel :394-425, badge SRT :400-407, Distribuir :583 → doPublish → publish-space-asset em useVideoRepurpose.ts:187); useMasterSrtStatus :200-210; SOPs external-video-ingest/video-repurpose-worker/repurpose-host-infra-provisioning/asr-master-to-srt presentes; os 8 commits f703cc8→67dc54d TODOS existem no git log com datas e mensagens compatíveis.",
> 190	          "NÃO-SHIPADO CONFIRMADO: FR-VR-008/Fatia 4 (mapeador) — grep 'FR-VR-008' em código (*.ts/*.tsx) = exit 1, só existe no blueprint:67; FR-VR-002 shipado apenas como gate 501; smokes do módulo que existem e cobrem os seams: smoke-external-ingest (G1-G5), smoke-video-repurpose (G1-G5 enqueue), smoke-scheduled-carousel (S1-S8 publish-space-carousel)."
> 191	        ],
> 192	        "refuted": [
> 193	          "'Smokes re-executáveis: scripts/qa/{...,smoke-carousel,...}.ts' — PARCIALMENTE REFUTADO: smoke-carousel.ts NÃO é deste módulo. Seu header declara 'PDF carousel generation (FR-CP-009, CP-011)' — é o smoke do POST-ENGINE (reshaper/pillar_atoms → carrossel PDF LinkedIn via generate-carousel), não do video-repurpose. O caminho de render do carousel-core (slides IG 1080×1350) NÃO tem smoke re-executável próprio — a prova material é o witness Vision QA 2026-07-12 + o smoke-scheduled-carousel cobre só o seam publish-space-carousel. O 08-quality-metrics retroativo deve contar 3 smokes do módulo (não 4) e registrar o gap de smoke do carousel-core honestamente."
> 194	        ],
> 195	        "missed": [
> 196	          "Gate BYOK do detector diverge do contrato do FRD (o leitor pegou só o nome do erro): FR-VR-010/§3.5 prometem provider per-user 'openrouter/gemini/groq', mas o código exige `aiKey = openRouterKey || groqKey` (detect-viral-moments/index.ts:117) — tenant com SÓ google_api_key (Gemini) toma 402 ai_not_configured apesar de Gemini constar no contrato; geminiKey só entra como fallback da cascata quando já há chave primária (:170). O 04-frd retroativo deve fixar: gemini-only NÃO destrava o detector.",
> 197	          "§Pilar II tem MAIS spec-drift FFmpeg além da legenda: (a) corte — blueprint:42 especifica '-ss <in> -to <out> (stream-accurate)'; o shipado é '-ss'+'-t <dur>' como opções de INPUT 0 com re-encode frame-accurate + o anticorpo multi-input documentado (segment-core.ts:14, :88-90, :123); (b) reframe — blueprint:43 crava a fórmula 9:16 'crop=ih*9/16:ih:...'; o shipado é expression-crop source-agnóstico 'min(iw,ih*ar)' + force_original_aspect_ratio=increase (:62-67). Um 05-sdd retro que copie os filtros do blueprint especificaria flags errados.",
> 198	          "FRD §1 linha 19 tem pointer E claim stale (mesma classe do drift 9, não citado pelo leitor): 'cut-spec é 100% caller-authored (VideoRepurposePage.tsx:289)' — hoje :289 é o Card '1. Enviar o master' (drift de pointer após as edições do front-door), e o claim em si foi superado pela própria fatia: doViralCuts alimenta os clips a partir do DETECTOR (FR-VR-010), não mais 100% caller-authored.",
> 199	          "O bloco instagram do publish-social também ganhou a branch STORIES (FR-SPACES-083 / Amendment 24, discriminador content.surface, logo abaixo da branch CAROUSEL) — o 07-process-flow retroativo deve registrar que o rail IG hoje tem 3 superfícies (REELS/CAROUSEL/STORIES); a tabela §2 do blueprint está stale além do exemplo CAROUSEL que o leitor citou.",
> 200	          "A lista de commits do leitor termina em 67dc54d, mas a rota host-media (streaming Range) e a infra host versionada (infra/systemd + infra/nginx) — que ele mesmo lista como shipped — nasceram no commit 955117d 'feat(repurpose): rota host-media (Range) + infra host versionada' (HANDOFF.md:238). O registro retroativo de traceabilidade (FR↔commit) deve incluí-lo."
> 201	        ]
> 202	      },
> 203	      {
> 204	        "module": "youtube-studio",
> 205	        "verified": [
> 206	          "DRIFT 1 (blocker) CONFIRMADO — cisma de escopo: 00-deepsearch-blueprint.md:313 = '### Fatia 1 — Faceless assembler (destrava o engine já codado)' vs 11-api-surface-map.md:433 = '### Fatia 1 — Tabela CRUD read-only de vídeos'; 12-amendment define Fatia 2 = write ops. Shipado = painel (youtube-data/index.ts existe, 331 linhas; assembler = zero código, engine faceless segue atrás do gate 503 VIDEO_FACELESS_WEBHOOK em video-render/index.ts:104-113). Colisão de numeração provada nos dois arquivos da mesma família.",
> 207	          "DRIFT 2 (material) CONFIRMADO E AMPLIFICADO — youtube-api-registry.json:10-14 'currentConnectionGap.grantedScopes: [youtube.upload]' está DUPLAMENTE stale: (a) social-auth-init pede os 4 escopos do Amendment 12 (bloco scopes ~:152-157, sem youtube.upload, com access_type=offline&prompt=consent); (b) PROVA VIVA própria: SELECT em social_accounts (REST, service key) retorna scopes = [yt-analytics-monetary.readonly, youtube, youtube.readonly, youtube.force-ssl], is_active=true, updated_at=2026-07-15T18:00:05Z — a conexão real JÁ tem os 4. Também 11 §1 (linha 41 'Fatia 1 BLOQUEADA até re-consent') e SOP youtube-studio-panel.md:19 carregam o mesmo gap stale.",
> 208	          "DRIFT 3 (material) CONFIRMADO — 11-api-surface-map.md:443 'Toda ação debita mcoCoins' E TAMBÉM :420 (pattern #16 'débito mcoCoins por ação' — segunda ocorrência que o leitor não citou) vs grep 'deduct_mco' em youtube-data/index.ts = 0 hits e grep 'youtube' em src/lib/billing.ts = 0 hits. Amendment 12 lido inteiro (56 linhas): zero menção a billing/mcoCoins. Ações do painel são gratuitas hoje.",
> 209	          "DRIFT 4 (material) CONFIRMADO — 11:412 pattern #8 = 'yes — Nós de observação na Knowledge Mesh (mcorch_nodes) por sync bem-sucedido; cache de metadados por project_id'; SOP youtube-studio-panel.md:60-62 tem seção 'Mesh Connection Mandate' prescrevendo o nó; youtube-data/index.ts lido INTEIRO: único sink é infra_health_logs (:100-101, service='youtube-studio') — zero INSERT em mcorch_nodes e zero cache. Declaração 'yes' indevida.",
> 210	          "DRIFT 5 (material) CONFIRMADO — 11 §7 Fatia 3 (linhas ~450-452): '(1) dry-run… (2) confirmação dupla (digitar o ID ou EXCLUIR)… nó de observação na mesh todo delete'. Shipado: delete direto pós-gate (youtube-data:314-322, DELETE 204-tolerante) + UM AlertDialog (YouTubeStudioPage.tsx:404-425, botão 'Excluir permanentemente'). Amendment 12 §3 sanciona 'videoId explícito + confirmação na UI' (única) — 12 é o contrato real e supersede o §7 Fatia 3 do map.",
> 211	          "DRIFT 6 (minor) CONFIRMADO — SOP youtube-studio-panel.md:21 fixa 5 escopos ('youtube.readonly, youtube.upload, youtube.force-ssl, yt-analytics.readonly, yt-analytics-monetary.readonly') vs código pede 4 diferentes (sem upload, sem yt-analytics.readonly; `youtube` amplo adicionado). Superset monetário confirmado no código: youtube-data:144-148 aceita ANALYTICS OU MONETARY p/ video_metrics (FR-YT-023) e useYouTubeStudio.ts:110-113 espelha.",
> 212	          "DRIFT 7 (minor) CONFIRMADO — 00-deepsearch-blueprint.md:28 e :234 citam 'scope youtube.upload + refresh offline (social-auth-init/index.ts:139-140)'; hoje essas linhas carregam o comentário prompt=consent + bloco de 4 escopos (lido :130-170). Superseded — snapshot de 2026-07-09.",
> 213	          "DRIFT 9 (minor) CONFIRMADO — blueprint OTD-YTS-002 (:270 'Não codificar avatar-clone sobre Hedra sem GO', API Terms proíbem integração verbatim :79) + default MuseTalk MIT (:84,:94) vs reconcile-kanban-roadmap.ts:69 'Economics fechado — Hedra ~$35/mês (default)' + migration 20260630000000 (hedra_api_key:14 + fal_api_key:16 no user_api_keys_table). grep musetalk/sadtalker em src/+supabase/+scripts/ (*.ts/tsx) = 0 hits de código. Tensão cross-módulo real.",
> 214	          "SHIPPED (tudo verificado materialmente): youtube-data/index.ts 331 linhas, 7 actions confirmadas; filtro user_id load-bearing :119-125; ensureFreshToken via refresh-social-token :44-70; gate fail-closed de escopo :137-164 (403 youtube_scope_missing + CTA); read-modify-write preservando categoryId :294-307; delete 204-tolerante :314-322; revenue fail-soft {monetized:false} :276-284; telemetria :100-101. social-auth-init 4 escopos + offline+consent. social-auth-callback persiste scopes (:88,:114,:320,:337 — upsert E insert-fallback). App.tsx:131 rota youtube. useYouTubeStudio deriva hasRead/hasAnalytics(superset)/hasWrite/needsReconnect. YouTubeStudioPage.tsx 589 linhas: canWrite gating :300-315, AlertDialog :404-425, CTA 'Reconectar com permissões ampliadas' :511, Receita gated hasMonetaryScope :579. publish-social branch youtube :502+ com selfDeclaredMadeForKids:false + containsSyntheticMedia:true hardcoded :537-539 (via fetchPublicUrl anti-SSRF). smoke-youtube-write-ops.ts = exatamente 9 gates S1-S9 (401/400/409/403×3/400×2/400). SOPs existem (youtube-studio-panel.md 62 linhas; youtube-publish-credential-resolution.md 222). COST faceless:125 em video-render:23; gate 503 render_engine_unavailable :104-113. render-core.ts:90 VALID_TEMPLATES inclui viral-long-16x9; template no disco (6341 bytes). NÃO-SHIPADO confirmado: 0 código assembler/lipsync; docs/bok/youtube-studio/ = só 00+11+12+_apimap+registry (ls) — os 9 canônicos são green-field."
> 215	        ],
> 216	        "refuted": [
> 217	          "DRIFT 8 (material) REFUTADO NO NÚCLEO OPERACIONAL — o leitor afirma que o gate da Fatia 1 'ainda não é provável' porque 'a YouTube Analytics API não foi habilitada' e 'o Sovereign ainda não reconectou'. As citações de HANDOFF.md/sprint-priorities.md existem MAS estão STALE: prova material própria desta sessão (2026-07-16): (a) social_accounts vivo tem os 4 escopos novos concedidos, updated_at=2026-07-15T18:00:05Z — a reconexão JÁ ACONTECEU depois do seal do HANDOFF; (b) refresh-social-token respondeu {success:true}; (c) curl real com o token vivo: channels.list HTTP 200 (canal UChCsERxOu9f8lh5bYVrGbOA, 2871 views, 55 subs) E reports.query HTTP 200 com rows=[[61]] — a YouTube Analytics API ESTÁ habilitada e retorna ≥1 linha. O gate de materialidade da Fatia 1 (curl videos.list + reports.query ≥1 linha) está SATISFEITO no lado API neste exato momento; falta só o screenshot Vision QA. O drift real é o INVERSO do reportado: HANDOFF:~252, sprint-priorities.md:22, registry e 11 §1 é que estão stale contra a realidade. Ressalva honesta: os subitens Google-side (data-access verification, publicação do branding, classificação CASA) não são verificáveis daqui e podem seguir abertos — mas os 2 bloqueadores nomeados (reconexão + Analytics API) estão materialmente resolvidos, e a recomendação 'registrar como OTDs abertas, nunca como done' cristalizaria estado morto."
> 218	        ],
> 219	        "missed": [
> 220	          "REALIDADE VIVA NÃO CAPTURADA (o maior): a reconexão de 4 escopos + Analytics API habilitada + reports.query com dados reais (rows=[[61]]) tornam o gate Y3 do Amendment 12 satisfeito e a Fatia 1 provável AGORA — a suíte retroativa deve selar isso como estado atual (com prova datada), não como OTD aberta; senão nasce stale no dia 1, repetindo o erro do registry.",
> 221	          "SEGUNDO trilho YouTube vivo ignorado pela auditoria: Channel Format Intelligence produz variantes NATIVAS de YouTube — channel_profiles seeda 2 perfis youtube (short weight 10 :132 e long_video weight 50 :169, migration 20260627140000) e smoke-longform-16x9.ts prova E2E o reshaper enfileirando render 16:9 determinístico (template viral-long-16x9, charged_mco=0) → variante youtube long_video 'reused_master'. Isso significa que o Track B ('fábrica long-form') NÃO é 100% green-field: o trilho de master 16:9 já renderiza; o que falta é o assembler multi-cena. A suíte deve baseline-ar isso.",
> 222	          "publication_metrics (migration 20260626130000) inclui platform youtube — série temporal de outcome por post publicado (FR-VA-027, coletor never-fabricate). É uma SEGUNDA fonte de métricas YouTube, distinta dos reads on-demand da Analytics API do painel; o 06-data-model precisa reconciliar as duas (panel=Analytics v2 on-demand vs collector=snapshot por publicação).",
> 223	          "format-specs.ts define youtube_short (:110) e youtube_video (:116) — SSOT client-side de formatos/chromes de preview YouTube (Amendment 21). Superfície de dados cross-módulo que o 06-data-model do leitor não lista.",
> 224	          "guard-sweep.sh:33 JÁ integra o smoke-youtube-write-ops na bateria consolidada de regressão ('youtube-write-ops (force-ssl gate, 9)') — o 08-quality-metrics pode citar o guarda existente em vez de propor wiring novo.",
> 225	          "Micro-drift interno do Amendment 12 que estende o Drift 1: a tabela §1 rotula o escopo `youtube` (videos.insert via publish-social) como '✅ Fatia 1' — mas publish nunca foi Fatia 1 em doc nenhum (11 §7 Fatia 1 é read-only; publish shipou antes, pelo post-engine). A confusão de numeração contamina até o amendment mais novo.",
> 226	          "Micro-drift de pointer no blueprint: :10 cita 'VALID_TEMPLATES linha 71 = viral-short-9x16+viral-long-16x9' — hoje é a linha 90 e a allowlist tem 4 templates (+cinematic-9x16, +viral-caption-overlay-9x16). Sintoma de que TODOS os file:line do blueprint (2026-07-09) precisam de re-verificação no seal retroativo.",
> 227	          "delete_video não emite telemetria distinguível: pulse('healthy') genérico (youtube-data:320) sem event/metadata — mesmo sem o nó de mesh (Drift 4), o infra_health_logs suporta event+metadata (migration 20260615170000) e um delete permanente deveria no mínimo logar videoId+ação para trilha de auditoria mínima; hoje um delete é indistinguível de um list bem-sucedido no HUD."
> 228	        ]
> 229	      }
> 230	    ]
> 231	  },
> 232	  "workflowProgress": [
> 233	    {
> 234	      "type": "workflow_phase",
> 235	      "index": 1,
> 236	      "title": "Ler"
> 237	    },
> 238	    {
> 239	      "type": "workflow_phase",
> 240	      "index": 2,
> 241	      "title": "Verificar"
> 242	    },
> 243	    {
> 244	      "type": "workflow_agent",
> 245	      "index": 1,
> 246	      "label": "read:video-repurpose",
> 247	      "phaseIndex": 1,
> 248	      "phaseTitle": "Ler",
> 249	      "agentId": "abfa2108037f4d175",
> 250	      "model": "claude-opus-4-8",
> 251	      "state": "done",
> 252	      "startedAt": 1784211835082,
> 253	      "queuedAt": 1784211828888,
> 254	      "attempt": 1,
> 255	      "lastToolName": "StructuredOutput",
> 256	      "lastToolSummary": "video-repurpose",
> 257	      "promptPreview": "Contexto: repo /home/gcrUX/htdocs/constellation-orchestra (MCORCH). O Sovereign quer selar a suíte BoK canônica 9/9 (00-index, 01-mrd, 02-brd, 03-prd, 04-frd, 05-sdd, 06-data-model, 07-process-flow, 08-quality-metrics) RETROATIVA para um módulo que já tem código shipado. Sua tarefa: auditar se o material existente é suficiente e fiel para o /bok-scribe começar, ou se há drifts que contaminariam a …",
> 258	      "lastProgressAt": 1784212179363,
> 259	      "tokens": 158935,
> 260	      "toolCalls": 22,
> 261	      "durationMs": 344280,
> 262	      "resultPreview": "{\"module\":\"video-repurpose\",\"blueprint_summary\":\"Dois docs existem em docs/bok/video-repurpose/: (1) `00-deepsearch-blueprint.md` (2026-07-12, semente Closed-Loop Step 0) — tese \\\"o MCORCH distribui mas não produz cortes\\\", 5 Pilares (I Ingest externo · II Worker segment/reframe/caption · III Carrossel IG · IV Mapeador de metadados · V Fiar na distribuição), FR-VR-001..009, OTD-VR-001..007, FM-VR-…"
> ```

## 🤖 Claude *(15:53:46)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-repurpose/ /home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/ 2>&1",
  "description": "List video-repurpose and spaces-cadence BoK dirs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/:
> 00-deepsearch-blueprint.md
> 00-index.md
> 01-mrd.md
> 02-brd.md
> 03-prd.md
> 04-frd.md
> 05-sdd.md
> 06-data-model.md
> 07-process-flow.md
> 08-quality-metrics.md
> 09-pattern-conformance.md
> 
> /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-repurpose/:
> 00-deepsearch-blueprint.md
> 10-frd-sdd-viral-quality.md
> ```

## 🤖 Claude *(15:53:56)*


## 🤖 Claude *(15:53:57)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/01-mrd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# MRD — Market Requirements Document
> 2	
> 3	**Project:** spaces-cadence
> 4	**Version:** v0.1 | **Date:** 2026-07-15
> 5	**BoK Applied:** BABOK v3 (Strategy Analysis + Elicitation & Collaboration)
> 6	**Status:** Draft
> 7	**Source of truth:** [`00-deepsearch-blueprint.md`](00-deepsearch-blueprint.md) (verificação externa 2026-07-14). Toda afirmação externa deste MRD é ancorada no blueprint; nada é inventado além dele (Lei 1).
> 8	
> 9	> **ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign · Owner = Sovereign (blast radius: ban de app Meta/X + sanção ANPD até 2% do faturamento — LGPD Art. 52).
> 10	> **Closed-Loop gate:** este é o **primeiro** documento da suíte. Os gates permanecem ABERTOS: BoK 02-brd→05-sdd, `09-pattern-conformance.md`, SOP Lei 2 (`docs/processes/spaces-cadence.md`), `/security-review` de toda migration. **Nenhuma linha de código antes disso.**
> 11	
> 12	---
> 13	
> 14	## 1. Executive Summary
> 15	
> 16	O MCORCH já executa a metade cara do funil de conteúdo — **gerar** (pilar → `pillar_atoms`), **reformatar por canal** (`reshape-pillar` → `channel_variants`), **publicar** (`scheduled_posts` + `auto-publish`) e **medir receita** (UTM + afiliado + `creative_metrics` + `collective_efficiency_ledger`). Faltam duas capacidades que nenhum concorrente de "bot de DM" entrega junto: (a) **recorrência com hora-do-dia / weekday / timezone / quiet-hours / frequency-cap / digest / A-B / idempotência** — que hoje **não existe** (`grep rrule|recurrence|recurring` = 0; `profiles.timezone` tem 0 consumidores; `channel_profiles.cadence` é dado morto), e (b) — **PROBE-GATED, não prometida** — o fechamento do laço inbound (comentário/DM) que o post provoca. O módulo entrega isso como um `kind:cadence` novo no Canvas Studio + um motor de sequência **Postgres-first** que **estende** o trilho de recorrência já vivo (`autopilot_plans` + tick `autopilot-cadence-cron`) em vez de construir um terceiro driver. O "ir além do ManyChat" não é "mais um bot": é o bot ser alimentado pelo mesmo motor que criou o post e pelo mesmo ledger que mede o retorno. **Timing:** o AI Act Art. 50(1) entra em vigência **2026-08-02**, exigindo disclosure de IA server-side por construção — quem não nascer compliant não pode operar automação de mensagem na UE.
> 17	
> 18	---
> 19	
> 20	## 2. Market Problem Statement
> 21	
> 22	### 2.1 Current State
> 23	
> 24	O Usuário Zero (Gabriel — dono do app Meta **global** do MCORCH, Standard Access) e os tenants BYOK futuros conseguem gerar, atomizar, reformatar e publicar conteúdo, mas:
> 25	
> 26	- **Não há recorrência com semântica de calendário.** A única recorrência do sistema é `autopilot_plans.next_run_at + interval_days` — sem hora-do-dia, sem weekday, sem timezone (`profiles.timezone` existe desde `20260402014040` e tem **zero leitores**). `campaign_steps` não tem noção de tempo; `campaign-run` dispara tudo em paralelo.
> 27	- **Não há teto declarativo por canal em uso.** `channel_profiles.cadence` (`{target_per, count_min, count_max}`) é **dado morto** (grep de leitores = 0).
> 28	- **O laço inbound morre.** `instagram-webhook` itera só `entry.changes`; um DM real seria descartado com **200 OK** (falso-sucesso perfeito). Não existe tabela de thread/mensagem social, nem outbound de mensagem em canal nenhum.
> 29	- **Infra de ingestão quebrada (P0).** `whatsapp-webhook` está **inalcançável** (sem bloco `[functions.whatsapp-webhook]` em `config.toml` ⇒ `verify_jwt` default true ⇒ Meta leva 401 no gateway) e valida HMAC com `===` (não timing-safe).
> 30	
> 31	### 2.2 Root Cause Analysis
> 32	
> 33	- **Gap de tecnologia:** o motor de recorrência existente (`autopilot_plans` + 2 drivers gêmeos `autopilot-cadence-cron`/`nurture-advance`) nunca precisou de hora/weekday/tz porque nasceu para o ciclo viral. As lacunas são `ALTER TABLE`, não fundamento para uma tabela paralela.
> 34	- **Gap de processo:** não há SOP (Lei 2) nem BoK de cadência/inbox; `auto-publish` roda em **crontab de SO de um host** (classe de confiabilidade inferior ao pg_cron, sem lock).
> 35	- **Gap de mercado (honesto):** o inbound (comentário/DM) sob Standard Access pode **não entregar nada** de quem não tem role no app (FM-CAD-02, RPN 486 — o maior deste doc). Enquanto o probe (DM real de terceiro sem role) não fechar, o laço inbound é **hipótese gated por App Review**, não capacidade.
> 36	
> 37	### 2.3 Desired State
> 38	
> 39	Um `kind:cadence` no Canvas Studio que arma um plano recorrente e — sem app review, para o Usuário Zero **e qualquer tenant** — publica com **hora-do-dia + weekday + timezone + quiet-hours + frequency-cap + digest + A/B determinístico + overlap/catchup/jitter + idempotência por índice único** que ninguém mais tem. Sobre esse chão, e **só depois** de o probe fechar, o laço inbound alimenta o **mesmo** `lead_events`/`creative_metrics` que já mede receita. Compliance (LGPD / Meta / AI Act) é **estrutural por construção** — nunca via prompt/LLM.
> 40	
> 41	---
> 42	
> 43	## 3. Target Market Segments
> 44	
> 45	| Segment | Description | Size Estimate | Urgency | Accessibility |
> 46	|---------|-------------|---------------|---------|---------------|
> 47	| Primary | **Usuário Zero** — Gabriel, dono do app Meta global (Standard Access); comment→DM e code-only apenas para as contas IG próprias | 1 tenant (piloto enterprise interno) | High | **Imediata** — Fatia 1 (publicação) não exige review externo |
> 48	| Secondary | **Tenants BYOK** — trazem o próprio app Meta + WABA + System User token + método de pagamento | Multi-tenant (pós-Usuário 1) | Medium | **Gated** — IG multi-tenant exige App Review + Business Verification; WhatsApp BYOK sem review (tenant é developer direto) |
> 49	
> 50	### 3.1 TAM / SAM / SOM
> 51	
> 52	| Metric | Value | Basis |
> 53	|--------|-------|-------|
> 54	| TAM (Total Addressable Market) | **Não quantificado neste MRD** — decisão aberta | O blueprint não fornece números de mercado externos verificados; §3 carrega **SELO DE NÃO-VERIFICAÇÃO**. Quantificar TAM/SAM/SOM exigiria pricing/docs datados de concorrentes (ManyChat et al.), que o blueprint removeu por falta de âncora (Lei 1). **Marcado como decisão aberta, não improvisado.** |
> 55	| SAM (Serviceable Addressable Market) | **Beachhead qualitativo:** todo tenant que já usa o funil de conteúdo do MCORCH e precisa de recorrência de publicação | Fatia 1 serve **qualquer** tenant sem gate externo (asset existente, 0 mco, keyless) | Base instalada do MCORCH (produtores de conteúdo de afiliados / marca) |
> 56	| SOM (Serviceable Obtainable Market) | **1 tenant (Usuário Zero)** na largada; expansão gated por probes Sovereign | O único entregável sem gate externo é a Fatia 1; inbound multi-tenant depende de FM-CAD-02 + App Review | Estratégia Usuário Zero (piloto enterprise) |
> 57	
> 58	> **Nota de fidelidade (Lei 1):** os campos TAM/SAM/SOM não são preenchidos com estimativas numéricas porque o blueprint não as fornece com âncora datada. Preenchê-los seria fabricar mercado. Ficam como **decisão aberta** para o Sovereign prover fonte externa verificada, se necessário à BRD.
> 59	
> 60	---
> 61	
> 62	## 4. Competitive Landscape
> 63	
> 64	> 🚫 **SELO DE NÃO-VERIFICAÇÃO (§3 do blueprint, Lei 1).** A comparação com o ManyChat foi **removida** do blueprint por fazer ~12 afirmações factuais sobre produto de terceiro **sem uma única URL**. **Este MRD NÃO pode citar §3 como fato.** Só a **coluna MCORCH** (verificável no repo, §2.1 do blueprint) é reutilizável. Para reabilitar a comparação, ancorar cada linha em pricing/docs datados do concorrente.
> 65	
> 66	| Competitor | Positioning | Strengths | Weaknesses | Our Differentiation |
> 67	|------------|-------------|-----------|------------|---------------------|
> 68	| ManyChat (categoria "respondedor de DM") | **NÃO VERIFICADO** — descrito no blueprint apenas como categoria (bot de DM com fluxos visuais), sem âncora | **NÃO VERIFICADO** (proibido afirmar) | **NÃO VERIFICADO** (proibido afirmar; a linha removida mais perigosa alegava "broadcast por DM no IG", que §4/§10 declaram **impossível na plataforma**) | **Fosso verificável no repo:** geração do conteúdo agendado (pilar→atomiza→reshape→carrossel/vídeo 9:16) + atribuição de receita ao post (UTM+afiliado+`creative_metrics`+`collective_efficiency_ledger`) + ledger de custo por ação (mcoCoins 4×-floor + begin/finalize atômico). O bot é **alimentado pelo mesmo motor que criou o post e medido pelo mesmo ledger que mede o retorno** |
> 69	
> 70	**Diferenciação defensável (só o que o repo prova — §2.1/§3 do blueprint):**
> 71	
> 72	| Capacidade | MCORCH hoje (verificado no repo) | Veredito |
> 73	|---|---|---|
> 74	| Geração do conteúdo agendado | pilar → `pillar_atoms` → `reshape-pillar` → `channel_variants` → carrossel/vídeo 9:16 | **Fosso** |
> 75	| Atribuição de receita ao post/DM | UTM + afiliado + `creative_metrics` + `collective_efficiency_ledger` | **Fosso** |
> 76	| Ledger de custo por ação | mcoCoins 4×-floor + begin/finalize atômico | **Fosso** |
> 77	| Agendamento de posts | `scheduled_posts` + `auto-publish` + 3 seams (`metadata.reshape` + `schedule:true`/`publish_at`, Amendment 22) | **Temos** (o `kind:cadence` falta) |
> 78	| Drip/sequência com espera | `sequences`+`sequence_enrollments` (`nurture-dispatch`, gated, e-mail) | **Temos o motor**; falta canal + flip |
> 79	| Recorrência com hora/weekday/timezone | 0 | **Novo — o produto** (Fatia 1) |
> 80	| Comment→DM / keyword auto-reply | 0 (webhook descarta) | **Novo — PROBE-GATED** (FM-CAD-02) |
> 81	| Broadcast/newsletter por DM no IG | 0 | **Impossível no IG** (§4/§10 — Meta não oferece OTN/News/Sponsored no IG) |
> 82	
> 83	---
> 84	
> 85	## 5. Market Opportunity & Timing
> 86	
> 87	- **Regulatório (janela dura):** **EU AI Act Art. 50(1)** entra em vigência **2026-08-02** — informar que se interage com IA. O módulo nasce com disclosure server-side (G12) por construção; quem não nascer compliant não opera automação de mensagem na UE. (AI Act Art. 50(2), marcação machine-readable de conteúdo sintético, é **módulo próprio maior que este** — OTD-CAD-014.)
> 88	- **Maturidade técnica:** o MCORCH já roda **dois** motores de recorrência idênticos em produção (`autopilot-cadence-cron` + `nurture-advance`). O motor de cadência **estende** um deles — infra nova = zero. Débito/estorno atômico (`begin`/`finalize`), consent gate (`marketing_consents` + `erase_lead()`), pool BYOK (`resolveProviderKey`) e `notify()` já existem para reuso.
> 89	- **Ativos mortos a ressuscitar:** `profiles.timezone` (dado morto → SSOT de fuso) e `channel_profiles.cadence` (dado morto → teto autoritativo por canal, primeiro leitor do repo).
> 90	- **Comportamental:** o valor do WhatsApp deixou de ser "disparar volume" e passou a ser **abrir e manter janelas** (não existe franquia de 1.000 conversas grátis — §10.8); o desenho aposta na janela, não no broadcast.
> 91	
> 92	---
> 93	
> 94	## 6. Market Requirements
> 95	
> 96	> Priority: **Critical** (must have at launch) | **High** | **Medium** | **Low**
> 97	> Fidelidade (Lei 1): o blueprint **não** define `FR-CAD-xxx` — declara zero FR de inbound antes do payload cru. Os FRs abaixo são **candidatos** derivados 1:1 de §5/§7; a numeração é **proposta**, a ser selada pela FRD.
> 98	
> 99	| ID | Market Requirement | Priority | Rationale | Source (blueprint) |
> 100	|----|-------------------|----------|-----------|--------|
> 101	| MR-CAD-001 | Nó `cadence` no Canvas Studio (categoria Publish), keyless, que arma um plano recorrente sem gastar mco na criação | Critical | Entregável visível ao Usuário Zero e a qualquer tenant sem review externo | §5.1 · Fatia 1 → FR-CAD-001, FR-CAD-005 |
> 102	| MR-CAD-002 | Recorrência com **hora-do-dia + weekday + timezone**, computada em **UTC** e gravada em `next_run_at` | Critical | Capacidade inexistente hoje; cron em GMT nunca carrega preferência de horário (FM-CAD-06) | §5.2 · §5.3 → FR-CAD-002, FR-CAD-007 |
> 103	| MR-CAD-003 | **Quiet-hours** no fuso do sujeito + **frequency-cap** lendo `channel_profiles.cadence` (HALT, não reenfileira) | High | Diferença entre cadência e flood; ressuscita `channel_profiles.cadence` | §5.3 · G4 → FR-CAD-008 |
> 104	| MR-CAD-004 | **Dedup/digest** por `(user, channel, dia)` colapsando N vencimentos em 1 publicação/carrossel | High | Anti-flood estrutural | §5.3 → FR-CAD-009 |
> 105	| MR-CAD-005 | **A/B determinístico** estável entre retries (`mod(abs(hashtext(subject‖:‖exp)::bigint),100) < ratio`, cast bigint **antes** do abs) | High | Sem o cast correto ~50% cairia no bucket A e o experimento mentiria em silêncio | §5.3 → FR-CAD-010 |
> 106	| MR-CAD-006 | **Overlap/catchup/jitter + idempotência** por índice único parcial (`WHERE status <> 'failed'`) | Critical | Impede double-post (FM-CAD-01) e backlog storm (FM-CAD-07) | §5.2 · §5.3 → FR-CAD-003, FR-CAD-006 |
> 107	| MR-CAD-007 | **Custo projetado por ciclo em mco** exibido no inspector antes de armar; `budget_cap_mco` NOT NULL em mcoCoins | Critical | O nó cota 0, mas um plano diário de 30d com X-post-com-link projeta 1.350 mco — o Sovereign precisa ver a magnitude antes | §5.1 · §5.5 → FR-CAD-011 |
> 108	| MR-CAD-008 | Motor **Postgres-first sem infra nova**: estender `autopilot_plans` + roteamento por `plan_kind` no tick existente; **nenhum job pg_cron novo** | Critical | Um 3º driver triplica índice due/kill-switch/cap/identidade cron (2 idênticos já custam em prod) | §5.2 · OTD-CAD-003 → FR-CAD-002, FR-CAD-004 |
> 109	| MR-CAD-009 | **Sink = trilhos vivos**: enfileirar via `scheduled_posts` (contrato `metadata.reshape` + `schedule:true` + `publish_at`); `auto-publish` drena sem tocar | Critical | Mandato de integração: encaixar, não reconstruir distribuição | §5.4 · Fatia 1 → FR-CAD-006 |
> 110	| MR-CAD-010 | **BYOK per-user fail-closed** para todo provider; cobrança só via RPC atômica `begin`/`finalize`; custo externo do tenant **registrado** em `external_usd_cost` mesmo com mco=0 | Critical | API Tenancy Model; "não cobrar" ≠ "não medir" (senão a `collective_efficiency_ledger` mente — Lei 1) | §5.5 · G7 → FR-CAD-011, FR-CAD-014 |
> 111	| MR-CAD-011 | **Compliance estrutural**: cold DM impossível de representar (FK NOT NULL p/ inbound), UNIQUE(comment_id), opt-out no send, rodapé/disclosure IA server-side, caps NOT NULL, IoC anti-browser-automation | Critical | 14 guardrails de §6 impostos por construção, nunca via LLM | §6 (G1–G14) → FR-CAD-012, FR-CAD-013 |
> 112	| MR-CAD-012 | **Laço inbound IG** (comentário/DM → `lead_events`/`social_threads` → private reply ≤7d / resposta in-window ≤24h) | High · **PROBE-GATED** | Só destrava por DM real de terceiro sem role (FM-CAD-02, RPN 486); nasce `delivery:'gated'` | §5.4 · Fatia 2 → FR-CAD-012, FR-CAD-013 |
> 113	| MR-CAD-013 | **Canais desimpedidos BYOK**: Telegram (US$0, opt-in `/start`) + Email Resend (flip `nurture-dispatch` com rodapé server-side) | Medium | Sem review de plataforma; caminho mais barato | §5.5 · Fatia 3 → FR-CAD-014 |
> 114	| MR-CAD-014 | **Pré-requisitos P0 (Fatia 0)** fechados antes de qualquer código de cadência | Critical | Sem eles tudo é falso-sucesso | §7 Fatia 0 → OTD-CAD-001/004/006/007 |
> 115	
> 116	---
> 117	
> 118	## 7. Success Metrics (Market-Level KPIs)
> 119	
> 120	| KPI | Definition | Target (6-month) | Target (12-month) | Measurement |
> 121	|-----|-----------|------------------|-------------------|-------------|
> 122	| Ativação da cadência | Planos `plan_kind='cadence'` ativos (`is_active=true`) | ≥1 (Usuário Zero) | Multi-tenant (pós-Usuário 1) | `SELECT count(*) FROM autopilot_plans WHERE plan_kind='cadence' AND is_active` |
> 123	| Idempotência provada (Lei 1) | Double-post por tick sobreposto/retry | **0** | **0** | Índice único parcial `WHERE status <> 'failed'` + smoke re-executável |
> 124	| Fidelidade de reconciliação | `sent` reportado a partir do webhook de status (nunca do 202) | **100%** | **100%** | `cadence_dispatches.status` transiciona só no reconcile (FM-CAD-05) |
> 125	| Ressurreição de ativos mortos | Consumidores de `profiles.timezone` e `channel_profiles.cadence` | ≥1 cada (o motor) | ≥1 cada | grep de leitores no repo (era 0) |
> 126	| Custo visível | Inspector projeta mco/ciclo antes de armar; `budget_cap_mco` NOT NULL | 100% dos planos | 100% dos planos | Coluna NOT NULL + UI |
> 127	| Probe inbound fechado | DM real de terceiro sem role aparece no banco (FM-CAD-02) | Sim/Não (gate) | — | Payload cru + linha em `lead_events` |
> 128	
> 129	> **Nota:** KPIs clássicos de mercado (Market Penetration % de SAM, NPS) ficam como **decisão aberta** — dependem do TAM/SAM numérico que o blueprint não fornece (§3.1). Métricas acima são **materialmente verificáveis** no repo (Lei 1).
> 130	
> 131	---
> 132	
> 133	## 8. Regulatory & Compliance Context
> 134	
> 135	| Regulation | Applicability | Key Constraint | Compliance Owner |
> 136	|------------|---------------|----------------|-----------------|
> 137	| LGPD (Lei 13.709) | Todo lead brasileiro | Art. 8 §2/§4/§5 (ônus da prova, autorização genérica nula, revogação gratuita); Art. 16/18 VI (eliminação ⇒ `erase_lead()` **deve** cancelar agendamentos em cascata — OTD-CAD-006/G9); `basis='consent'` fail-closed até confirmar Guia de Legítimo Interesse (OTD-CAD-015) | Engineering (estrutural, migration) |
> 138	| EU AI Act Art. 50(1) | Leads UE / jurisdição desconhecida (fail-closed = UE) | Disclosure de IA server-side na 1ª mensagem de toda thread automatizada; vigência **2026-08-02** (G12) | Engineering |
> 139	| EU AI Act Art. 50(2) | Conteúdo sintético (Nano Banana/HyperFrames/Qwen3-TTS) | Marcação machine-readable — **módulo próprio, fora deste** (OTD-CAD-014) | Sovereign (escopo) |
> 140	| ePrivacy 13 + GDPR Art. 21 | Leads UE | Oposição a marketing direto é absoluta; aviso na 1ª comunicação, "clearly and separately"; lead sem país ⇒ tratar como UE (G11) | Engineering |
> 141	| CAN-SPAM | E-mail (Resend) | Rodapé + endereço postal + opt-out ≤10 dias úteis, montado **server-side** e concatenado — jamais delegado ao prompt (G10/FM-CAD-12) | Engineering |
> 142	| Meta Platform Policy §5 | IG/Messenger/WhatsApp | Consentimento suficiente + opt-out contínuo + sem feedback negativo excessivo (limiar auto-imposto conservador — sem número oficial, §10.4/FM-CAD-14); Human Agent tag inalcançável do caminho automático (G5) | Engineering + Sovereign (App Review) |
> 143	| WhatsApp Business Policy | WhatsApp Cloud BYOK | Opt-in explícito com número + `source_proof`; 422 `whatsapp_opt_in_missing` fail-closed (G7/FM-CAD-15); enquadramento **AI Provider** no Brasil pode cobrar cada msg não-template (OTD-CAD-009 — bloqueante econômico do auto-reply) | Sovereign (consulta Meta) + Engineering |
> 144	| Meta Platform Terms (Tech Provider) | Tenants BYOK | Armazenar System User token de terceiro pode caracterizar Tech Provider — revisão jurídica antes do Usuário 1 (OTD-CAD-010) | Sovereign (jurídico) |
> 145	| Instagram inauthentic-activity | Todos os canais Meta | Proibição perene de automação de mensagem/engajamento via browser headless; IoC falha se script fora de `scripts/qa/` tocar instagram.com/facebook.com (G13) | Engineering |
> 146	
> 147	---
> 148	
> 149	## 9. Traceability Matrix Stub
> 150	
> 151	| MR ID | → BR ID | → FR candidato | → OTD/FM | Rationale |
> 152	|-------|---------|----------------|----------|-----------|
> 153	| MR-CAD-001 | BR-??? | FR-CAD-001, FR-CAD-005 | OTD-CAD-002, OTD-CAD-007 | Nó `cadence` + edge `cadence-plan` |
> 154	| MR-CAD-002 | BR-??? | FR-CAD-002, FR-CAD-007 | FM-CAD-06 | Recorrência UTC hora/weekday/tz |
> 155	| MR-CAD-003 | BR-??? | FR-CAD-008 | OTD-CAD-008, OTD-CAD-017 | Quiet-hours + frequency-cap |
> 156	| MR-CAD-004 | BR-??? | FR-CAD-009 | — | Dedup/digest |
> 157	| MR-CAD-005 | BR-??? | FR-CAD-010 | OTD-CAD-016 | A/B determinístico |
> 158	| MR-CAD-006 | BR-??? | FR-CAD-003, FR-CAD-006 | FM-CAD-01, FM-CAD-07 | Idempotência + overlap/catchup/jitter |
> 159	| MR-CAD-007 | BR-??? | FR-CAD-011 | OTD-CAD-011 | Custo projetado + `budget_cap_mco` |
> 160	| MR-CAD-008 | BR-??? | FR-CAD-002, FR-CAD-004 | OTD-CAD-003 | Estender `autopilot_plans` + roteamento `plan_kind` |
> 161	| MR-CAD-009 | BR-??? | FR-CAD-006 | OTD-CAD-004, OTD-CAD-005 | Sink `scheduled_posts` |
> 162	| MR-CAD-010 | BR-??? | FR-CAD-011, FR-CAD-014 | OTD-CAD-009, OTD-CAD-010 | BYOK fail-closed + custo externo registrado |
> 163	| MR-CAD-011 | BR-??? | FR-CAD-012, FR-CAD-013 | FM-CAD-03/04/12/15 | Guardrails estruturais (§6) |
> 164	| MR-CAD-012 | BR-??? | FR-CAD-012, FR-CAD-013 | FM-CAD-02 (RPN 486), FM-CAD-13, OTD-CAD-018 | Laço inbound IG (PROBE-GATED) |
> 165	| MR-CAD-013 | BR-??? | FR-CAD-014 | — | Telegram + Email Resend |
> 166	| MR-CAD-014 | BR-??? | (Fatia 0) | OTD-CAD-001, OTD-CAD-004, OTD-CAD-006, OTD-CAD-007 | Pré-requisitos P0 |
> 167	
> 168	> **Decisões abertas (bloqueiam BRD→SDD — §11 do blueprint):** (1) sujeito da cadência (asset existente vs geração); (2) estender `autopilot_plans` vs tabela nova; (3) `channel_profiles.cadence` autoritativo vs sugestão; (4) escopo de canal da Fatia 1; (5) jurisdição default sem país; (6) semântica `cadence_dispatches` (retry via índice parcial vs append-only puro); (7) IG/Messenger no app Meta global vs BYOK-de-app. **Provisões Sovereign:** probe X Console (OTD-CAD-011) · probe TikTok autenticado (OTD-CAD-013) · consulta Meta AI Provider Brasil (OTD-CAD-009) · DM real de terceiro sem role + payload cru (FM-CAD-02/13) · domínio Resend verificado + flip `nurture-dispatch` · escopo AI Act 50(2) (OTD-CAD-014).
> 169	
> 170	---
> 171	
> 172	_Generated by MCORCH BoK Scribe Agent v1.0.0 — fiel a `00-deepsearch-blueprint.md` (Lei 1: nenhum FR/OTD/FM/entidade inventado além do blueprint; §3 sob selo de não-verificação; TAM/SAM numérico marcado como decisão aberta, não improvisado)._
> 173	
> ```

## 🤖 Claude *(15:53:58)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/02-brd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# BRD — Business Requirements Document
> 2	
> 3	**Project:** spaces-cadence
> 4	**Version:** v0.1 | **Date:** 2026-07-15
> 5	**BoK Applied:** BABOK v3 (Requirements Analysis & Design Definition)
> 6	**Status:** Draft
> 7	**Source of truth:** [`00-deepsearch-blueprint.md`](00-deepsearch-blueprint.md) (verificação externa 2026-07-14) + [`01-mrd.md`](01-mrd.md). Toda BR abaixo deriva 1:1 de uma MR-CAD-xxx e das seções §5/§6/§7/§8 do blueprint; nada é inventado além dele (Lei 1).
> 8	
> 9	> **ORO triplet desta task:**
> 10	> - **Operator:** MCORCH Master Execution Agent
> 11	> - **Reviewer:** Sovereign (Gabriel)
> 12	> - **Owner:** Sovereign — blast radius material: **ban de app Meta/X** (spam de 1 tenant no app global bane todos — OTD-CAD-018) + **sanção ANPD até 2% do faturamento** (LGPD Art. 52).
> 13	>
> 14	> **Closed-Loop gate:** este é o **2º** documento da suíte. Permanecem ABERTOS: 03-prd → 05-sdd, `09-pattern-conformance.md`, SOP Lei 2 (`docs/processes/spaces-cadence.md`), `/security-review` de toda migration. **Nenhuma linha de código antes disso.**
> 15	>
> 16	> **Nota de fidelidade (Lei 1):** o blueprint declara **zero FR de inbound** antes do payload cru de DM real. Os `FR-CAD-xxx` citados são **candidatos** derivados de §5/§7 — numeração proposta, a ser selada pela FRD. `§3` (posicionamento vs. ManyChat) carrega **SELO DE NÃO-VERIFICAÇÃO**: nenhuma BR/ROI cita §3 como fato; só a coluna MCORCH (verificável no repo) alimenta a diferenciação.
> 17	
> 18	---
> 19	
> 20	## 1. Executive Summary
> 21	
> 22	O MCORCH já paga a metade cara do funil — **gera** (pilar → `pillar_atoms`), **reformata** (`reshape-pillar` → `channel_variants`), **publica** (`scheduled_posts` + `auto-publish`) e **mede receita** (UTM + afiliado + `creative_metrics` + `collective_efficiency_ledger`). O módulo **spaces-cadence** adiciona a única peça que fecha o loop de recorrência sem reconstruir distribuição: um `kind:cadence` no Canvas Studio + um motor de sequência **Postgres-first** que **estende** o trilho de recorrência já vivo (`autopilot_plans` + tick `autopilot-cadence-cron`), roteando por `plan_kind`, **sem um terceiro driver e sem job pg_cron novo**.
> 23	
> 24	O valor de negócio da **Fatia 1** (Cadência de Publicação) é entregável ao Usuário Zero **e a qualquer tenant sem review externo**: hora-do-dia + weekday + **timezone** + quiet-hours + frequency-cap + digest + A/B determinístico + overlap/catchup/jitter + idempotência por índice único — capacidades que **hoje não existem** (`grep rrule|recurrence` = 0; `profiles.timezone` = 0 leitores; `channel_profiles.cadence` = dado morto). O laço inbound (comentário/DM) é **PROBE-GATED** (FM-CAD-02, RPN 486 — o maior do doc) e **não é prometido como capacidade** até o probe fechar.
> 25	
> 26	**Janela regulatória dura:** EU AI Act Art. 50(1) entra em vigência **2026-08-02** — quem não nascer com disclosure de IA server-side não opera automação de mensagem na UE. O módulo nasce compliant por construção (G12), não por prompt.
> 27	
> 28	---
> 29	
> 30	## 2. Business Objectives (SMART)
> 31	
> 32	| ID | Objective | Specific | Measurable | Achievable | Relevant | Time-bound |
> 33	|----|-----------|----------|------------|------------|----------|------------|
> 34	| BO-CAD-001 | Entregar Cadência de Publicação (Fatia 1) sem review externo | `kind:cadence` no canvas + `autopilot_plans` estendido + `cadence_dispatches` + `cadence-run`; sujeito = asset existente (0 mco) | ≥1 plano `plan_kind='cadence'` ativo para o Usuário Zero | Reusa trilho vivo; só `ALTER TABLE` + 2 edge fns + 6 edições de canvas | É o único entregável sem gate de plataforma (Fatia 1) | Primeira release após Fatia 0 (P0) fechada |
> 35	| BO-CAD-002 | Zero infra nova de recorrência | Estender `autopilot_plans` (OTD-CAD-003) + roteamento `plan_kind` no tick existente; **nenhum** 3º driver, **nenhum** job pg_cron novo | Contagem de drivers de recorrência permanece = 2 (não 3); jobs pg_cron sem incremento | Já há 2 motores idênticos em prod para copiar o padrão | Um 3º driver triplica índice due/kill-switch/cap/identidade cron | Junto com BO-CAD-001 |
> 36	| BO-CAD-003 | Provar idempotência (anti double-post) | Índice **único parcial** `(idempotency_key) WHERE status<>'failed'` + `ON CONFLICT DO NOTHING RETURNING` + `overlap_policy=skip` | **0** double-posts sob tick sobreposto/retry (smoke re-executável) | Mesmo truque de `begin_space_generation` | Double-post = FM-CAD-01 (RPN 224) + ban de plataforma | Antes de armar qualquer plano em prod |
> 37	| BO-CAD-004 | Ressuscitar 2 ativos mortos | `profiles.timezone` vira SSOT de fuso; `channel_profiles.cadence` vira teto autoritativo por canal | ≥1 leitor de cada no repo (era 0 em ambos) | Ambas as colunas já existem, só faltam consumidores | Fuso correto (FM-CAD-06) + teto anti-flood (G4) | Fatia 1 |
> 38	| BO-CAD-005 | Nascer compliant antes do AI Act | Disclosure de IA + rodapé/opt-out montados **server-side** e concatenados; nunca no prompt (G10/G12) | 100% das threads automatizadas com disclosure server-side | Molde `nurture-dispatch` gated já existe | Vigência AI Act Art. 50(1) = **2026-08-02** | Antes de flipar qualquer canal para `sent` |
> 39	| BO-CAD-006 | Tornar o custo visível antes de armar | Inspector projeta `Σ(canal×ocorrências até cap)` em mco; `budget_cap_mco` NOT NULL em mcoCoins | 100% dos planos exibem custo/ciclo antes do arm | Cálculo puro no cliente + coluna NOT NULL | Plano diário de 30d com X-post-com-link = **1.350 mco** (magnitude oculta) | Fatia 1 (obrigação compensatória do quote=0 do nó) |
> 40	
> 41	---
> 42	
> 43	## 3. Stakeholder Register
> 44	
> 45	| ID | Role | Interest | Influence | Communication Cadence | Contact |
> 46	|----|------|----------|-----------|----------------------|---------|
> 47	| SH-001 | Sovereign / Maestro (Reviewer + Owner) | High | High | Continuous | Gabriel Zarattini |
> 48	| SH-002 | Usuário Zero (Primary tenant, dono do app Meta global) | High | High | Contínua (é o próprio Sovereign nesta fase) | Gabriel Zarattini |
> 49	| SH-003 | Tenants BYOK (Secondary, pós-Usuário 1) | High | Low | Gated por App Review + Business Verification | — (futuro) |
> 50	| SH-004 | Engineering (Operator) | High | Medium | Por sessão `/handoff` | MCORCH Master Execution Agent |
> 51	| SH-005 | Compliance/Jurídico (LGPD/Meta Terms) | High | Medium | Por gate regulatório (OTD-CAD-009/010/014/015) | Sovereign (aciona consulta) |
> 52	| SH-006 | Plataformas externas (Meta/X/Telegram/Resend) | Medium | High (podem banir o app) | Reativa (webhooks de status + rate limits) | n/a |
> 53	
> 54	---
> 55	
> 56	## 4. Business Requirements
> 57	
> 58	> Cada BR traça ≥1 MR-CAD e ≥1 FR-CAD candidato. mcoCoins: a **unidade de cobrança é o CICLO** (par `begin`/`finalize`), **não o nó** — criar plano custa **0** (G7 = invariante do ciclo, não do nó). Custo externo BYOK que o tenant absorve é **registrado** (`external_usd_cost`) mesmo com cobrança mco = 0.
> 59	
> 60	| ID | Requirement | MR Traced | Priority | mcoCoins Cost | Acceptance Criteria |
> 61	|----|-------------|-----------|----------|---------------|---------------------|
> 62	| BR-CAD-001 | Nó `cadence` no Canvas Studio (categoria **Publish**), keyless, excluído do gate "runnable"; `resolveExecutePayload→null`, `estimateNodeCost→0` | MR-CAD-001 | Critical | **0** (criar plano não gera) | Nó adicionável via registry (aliases pt-BR: cadência/agendar/recorrente/cron/calendário); 6 edições de canvas feitas; não quebra `runAllCost` (FR-CAD-001) |
> 63	| BR-CAD-002 | **Estender `autopilot_plans`** (`plan_kind`, `recurrence jsonb`, `quiet_hours`, `overlap_policy`, `catchup_window`, `jitter_seconds`, `program jsonb`, `channel_allowlist`, `budget_cap_mco NOT NULL`; DROP CHECK `platforms`) — **não** tabela nova | MR-CAD-008 | Critical | 0 (migration) | Migration única aprovada em `/security-review`; `plan_kind IN ('viral','cadence')`; RLS owner-scoped preservada (FR-CAD-002) |
> 64	| BR-CAD-003 | Ledger `cadence_dispatches` com **índice único parcial** `(idempotency_key) WHERE status<>'failed'`; RLS = select_own + insert/update **service-role** (cliente nunca escreve) | MR-CAD-006 | Critical | 0 | `/security-review` sem findings; transição de `status` só service-role; retry libera / sucesso prende (FR-CAD-003) |
> 65	| BR-CAD-004 | Roteamento por `plan_kind` no tick **vivo** `autopilot-cadence-cron` (viral→`autopilot-run`, cadence→`cadence-run`) + edge `cadence-plan` (upsert + arm `next_run_at` UTC) | MR-CAD-002, MR-CAD-008 | Critical | 0 | **Nenhum** job pg_cron novo; `user_id` server-trusted da linha; gate `Bearer SB_SECRET_KEY`→403 (FR-CAD-004, FR-CAD-005) |
> 66	| BR-CAD-005 | Re-arm UTC generalizado `{frequency, days, hours, minutes, tz}` a partir de `autopilot-run:310-314`; cron **nunca** carrega preferência de horário | MR-CAD-002 | Critical | 0 | `next_run_at` computado em UTC; cadência multi-tenant correta por fuso (FR-CAD-007; fecha FM-CAD-06) |
> 67	| BR-CAD-006 | Quiet-hours no fuso do sujeito (cascata `recurrence.tz→profiles.timezone→America/Sao_Paulo`) + frequency-cap com **HALT** lendo `channel_profiles.cadence` | MR-CAD-003 | High | 0 | `profiles.timezone` e `channel_profiles.cadence` ganham 1º leitor; cap não reenfileira, HALT (FR-CAD-008) |
> 68	| BR-CAD-007 | Dedup/digest `(user, channel, dia)` colapsa N vencimentos em 1 publicação/carrossel | MR-CAD-004 | High | 0 | N vencimentos do mesmo canal/dia → 1 dispatch (FR-CAD-009) |
> 69	| BR-CAD-008 | A/B determinístico `mod(abs(hashtext(subject‖:‖exp)::bigint),100) < ratio` (cast bigint **antes** do abs) | MR-CAD-005 | High | 0 | Estável entre retries; bucket não enviesado (nunca `% 100` sobre int com sinal) (FR-CAD-010; fecha viés silencioso) |
> 70	| BR-CAD-009 | Overlap (`skip`) + catchup (6h) + jitter + fan-out bounded (`MAX_PER_RUN=50`/`CONCURRENCY=6`) | MR-CAD-006 | Critical | 0 | Queda de N horas não dispara backlog inteiro (FR-CAD-006; fecha FM-CAD-07) |
> 71	| BR-CAD-010 | Inspector exibe **custo projetado por ciclo em mco** antes de armar; `budget_cap_mco` NOT NULL, expresso em mcoCoins (nunca USD) | MR-CAD-007 | Critical | 0 (exibição) | Plano diário 30d com X-post-com-link projeta 1.350 mco visível antes do arm (FR-CAD-011) |
> 72	| BR-CAD-011 | Sink = `scheduled_posts` via contrato `metadata.reshape` + `schedule:true` + `publish_at` ISO (422/409 do Amendment 22); `auto-publish` drena **sem tocar** | MR-CAD-009 | Critical | Custo do canal no dispatch (não na criação) | Nó **enfileira**, não publica; 409 anti double-enqueue; 422 em data inválida (FR-CAD-006) |
> 73	| BR-CAD-012 | BYOK per-user fail-closed (`resolveProviderKey`, nunca `Deno.env.get`); cobrança só via RPC atômica `begin`/`finalize`; `external_usd_cost` + `cost_source` gravados **no reconcile** mesmo com mco=0 | MR-CAD-010 | Critical | Variável (por canal) | 402/501 estruturado quando provider não configurado; custo externo do tenant medido no `collective_efficiency_ledger` (FR-CAD-011, FR-CAD-014) |
> 74	| BR-CAD-013 | Reconciliação: `sent` só do **webhook de status**, nunca do 202 da API (molde poll `video_renders`) | MR-CAD-010, MR-CAD-011 | Critical | 0 | 100% dos `sent` originados de webhook de status (FR-CAD-006; fecha FM-CAD-05, Lei 1) |
> 75	| BR-CAD-014 | 14 guardrails de compliance **estruturais**: FK NOT NULL p/ inbound, UNIQUE(comment_id), opt-out no send, rodapé/disclosure IA server-side, caps NOT NULL, IoC anti-browser-automation | MR-CAD-011 | Critical | 0 | Cold DM impossível de representar; disclosure nunca via LLM; IoC falha se script fora de `scripts/qa/` tocar instagram.com/facebook.com (FR-CAD-012, FR-CAD-013) |
> 76	| BR-CAD-015 | **Laço inbound IG** (comentário/DM → `lead_events`/`social_threads` → private reply ≤7d UNIQUE / resposta in-window ≤24h) — **PROBE-GATED**, nasce `delivery:'gated'` | MR-CAD-012 | High · **PROBE-GATED** | Variável (in-window US$0) | **Só após** DM real de terceiro sem role no banco + payload cru fixar `entry.messaging` (FR-CAD-012, FR-CAD-013; gate FM-CAD-02/13) |
> 77	| BR-CAD-016 | Canais desimpedidos BYOK: Telegram (US$0, opt-in `/start`) + Email Resend (flip `nurture-dispatch` com rodapé server-side) | MR-CAD-013 | Medium | Telegram 0 / Resend 0 mco (custo externo BYOK) | `telegram_not_configured` fail-closed; flip para `sent` só com GO Sovereign (FR-CAD-014) |
> 78	| BR-CAD-017 | **Fatia 0 (P0)** fechada antes de qualquer código de cadência | MR-CAD-014 | Critical | 0 | `whatsapp-webhook` alcançável (config.toml `verify_jwt=false`) + `timingSafeEqual`; `estimateNodeCost` com case `publishSocial`; `erase_lead()` cascata; `auto-publish` em pg_cron + `FOR UPDATE SKIP LOCKED` (OTD-CAD-001/004/006/007) |
> 79	
> 80	---
> 81	
> 82	## 5. ROI Model
> 83	
> 84	> **Selo de honestidade (Lei 1):** o blueprint **não fornece números de mercado externos verificados** (§3.1 do MRD marca TAM/SAM/SOM numérico como decisão aberta). As linhas monetárias abaixo que dependem de mercado ficam **não quantificadas**; o que é quantificável é o **custo interno** (reuso de infra) e o **custo por ação em mco** (4×-floor, verificável no repo).
> 85	
> 86	### 5.1 Cost Estimates
> 87	
> 88	| Cost Item | Type | Monthly Estimate | Annual Estimate |
> 89	|-----------|------|-----------------|----------------|
> 90	| Infra de recorrência (pg_cron + `autopilot_plans` + tick existente) | OpEx | **US$0 incremental** — estende trilho vivo; zero container/serviço novo | US$0 incremental |
> 91	| Storage `cadence_dispatches` / `social_threads` (Supabase Postgres) | OpEx | Desprezível (ledger append + 20 msgs/thread; Meta não é banco de histórico) | Desprezível |
> 92	| Custo externo por canal (BYOK — absorvido pelo **tenant**, registrado em `external_usd_cost`) | Variable | Telegram US$0 · Resend free 3k/mês · IG in-window US$0 · X pay-per-use (DM US$0,015 / post-com-URL US$0,200) | Depende de volume do tenant |
> 93	| Desenvolvimento (Fatia 0 + Fatia 1) | CapEx | — | Escopo contido: `ALTER TABLE` + `cadence_dispatches` + 2 edge fns + 6 edições de canvas + Fatia 0 (5 itens P0) |
> 94	
> 95	### 5.2 Revenue Streams
> 96	
> 97	| Stream | Model | Monthly Potential | Notes |
> 98	|--------|-------|-----------------|-------|
> 99	| Consumo de mcoCoins por ciclo de cadência | mcoCoins 4×-floor via `begin`/`finalize` | **Não quantificado** (depende de volume/tenant — decisão aberta) | Cadência de publicação incrementa consumo de coins existente; X-post-com-link = 45 mco/post é o item de maior magnitude |
> 100	| Retenção/expansão do funil de conteúdo (fosso) | Plano (Starter/Pro/Enterprise) | **Não quantificado** | Recorrência com hora/weekday/tz é capacidade que "nenhum concorrente de bot de DM entrega junto ao motor de geração + ledger de receita" (só a coluna MCORCH, verificável) |
> 101	| Inbound → atribuição de receita (comentário/DM → afiliado/UTM) | mcoCoins + attribution | **PROBE-GATED** — não contabilizar até FM-CAD-02 fechar | Defensável só se alimentar o mesmo `lead_events`/`creative_metrics` |
> 102	
> 103	### 5.3 Payback Analysis
> 104	
> 105	| Metric | Value |
> 106	|--------|-------|
> 107	| Break-even (months) | **Qualitativo** — CapEx contido (reuso de infra; sem OpEx incremental) ⇒ payback dominado por custo de desenvolvimento, não por infra recorrente |
> 108	| 12-month ROI | **Não quantificado** (sem TAM/SAM numérico ancorado — §3.1 do MRD). Ganho estratégico: fecha o loop conteúdo→distribuição→**recorrência**→receita sem novo custo fixo |
> 109	| Risco de retorno negativo | Concentrado em **compliance** (ban de app Meta/X + ANPD até 2% do faturamento) — ver §8; mitigado por guardrails estruturais (BR-CAD-014) |
> 110	
> 111	---
> 112	
> 113	## 6. mcoCoins Economics
> 114	
> 115	> Modelo 4×-floor: `mco = ceil(usd / 0.018 × 4)`. Fonte dos valores: §4/§5.5 do blueprint (X pricing datado 2026-07-14). **Criar plano = 0**; cobrança no ciclo.
> 116	
> 117	| Operation | Coins/Run | Plan Tier Mapping | Monthly Volume (est.) | Monthly Revenue (est.) |
> 118	|-----------|-----------|-------------------|-----------------------|----------------------|
> 119	| Criar/armar plano `cadence` (`cadence-plan`) | **0** | Starter(500)/Pro(2000)/Ent(10k) | Não quantificado | 0 (criar plano não gera) |
> 120	| Dispatch publicação (WordPress/LinkedIn/IG/TikTok/YouTube/Pinterest via `scheduled_posts`) | Custo de publicação existente do canal (não recobrado pela cadência) | idem | Não quantificado | Herda economia do `auto-publish` |
> 121	| Dispatch **X DM Create** (US$0,015) | **4 mco** | idem | Não quantificado | Fora da Fatia 1 (X gated por OTD-CAD-011) |
> 122	| Dispatch **X Post com URL** (US$0,200) | **45 mco** (4,5× um `orchestrate-content`) | idem | Não quantificado | **X FORA da allowlist da Fatia 1** até probe de créditos fechar (OTD-CAD-011/FM-CAD-10) |
> 123	| Dispatch Telegram / Resend / IG in-window (BYOK) | **0 mco** — custo externo absorvido pelo tenant, **registrado** em `external_usd_cost` | idem | Não quantificado | "Não cobrar" ≠ "não medir": entra no `collective_efficiency_ledger` |
> 124	
> 125	---
> 126	
> 127	## 7. Constraints & Assumptions
> 128	
> 129	### Constraints
> 130	- **Mandato de integração (duro):** a Cadência **encaixa nos trilhos vivos** (`autopilot_plans` + `autopilot-cadence-cron` + `sequences`/`nurture-dispatch` + `scheduled_posts`) — **NÃO reconstrói distribuição**. Um 3º driver de recorrência é proibido (OTD-CAD-003).
> 131	- **BYOK per-user fail-closed:** toda credencial de provider resolve por `auth.uid()` via `resolveProviderKey`; `Deno.env.get(<provider>)` proibido em fluxo user-facing; sem credencial ⇒ 402/501 estruturado.
> 132	- **Cobrança só via RPC atômica** `begin`/`finalize` (nunca client-side); G7 (quote==charge) é invariante do **ciclo**, não do nó.
> 133	- **Edge fn com `verify_jwt=false`** (webhooks) ⇒ verificação ES256 JWKS ou HMAC `timingSafeEqual` — **nunca `atob` cego** nem `===` (bug atual do `whatsapp-webhook`, OTD-CAD-001).
> 134	- **RLS default-deny owner-scoped** em toda tabela; `cadence_dispatches` não é append-only puro (precisa `UPDATE` service-role de `status`).
> 135	- **Compliance é estrutural, nunca via prompt/LLM** (rodapé, disclosure de IA, gate de janela, opt-out).
> 136	- **Standard Access do app Meta global:** o webhook pode não entregar inbound de terceiro sem role ⇒ Fatia 2 é **PROBE-GATED**; **zero FR de inbound** no BoK antes do payload cru.
> 137	- **IG/Messenger no app Meta GLOBAL** (não BYOK-de-app): blast radius compartilhado ⇒ cap de fan-out **por-APP** + kill-switch **global** obrigatórios (OTD-CAD-018).
> 138	
> 139	### Assumptions
> 140	- O Sovereign fornecerá as **provisões** que só ele executa: probe X Console (OTD-CAD-011), probe TikTok autenticado (OTD-CAD-013), consulta Meta AI Provider Brasil (OTD-CAD-009), DM real de terceiro sem role + payload cru (FM-CAD-02/13), domínio Resend verificado, escopo AI Act 50(2) (OTD-CAD-014).
> 141	- **Sujeito da Fatia 1 = asset existente** (`creative_assets.id`, owner-scoped) ⇒ 0 mco, keyless, sem ledger de geração (OTD-CAD-002, recomendação do blueprint).
> 142	- **`channel_profiles.cadence` é teto autoritativo** por canal (OTD-CAD-008, recomendação).
> 143	- **Semântica `cadence_dispatches` = retry via índice parcial** (`WHERE status<>'failed'` + UPDATE service-role), não append-only puro (OTD-CAD-006 do §11, recomendação).
> 144	- **Jurisdição default = UE (opt-in prévio)** quando o lead não tem país (fail-closed, G11).
> 145	- Os 2 motores de recorrência em prod (`autopilot-cadence-cron`, `nurture-advance`) permanecem estáveis como padrão a copiar.
> 146	
> 147	---
> 148	
> 149	## 8. Business Risk Register
> 150	
> 151	> Probability & Impact: 1=Low, 5=High. RPN = Probability × Impact. Deriva da FMEA técnica (§8 do blueprint, escala 1–10) traduzida para risco de **negócio** (blast radius: ban de app / sanção ANPD / custo invisível).
> 152	
> 153	| Risk ID | Description | Probability | Impact | RPN | Mitigation |
> 154	|---------|-------------|-------------|--------|-----|------------|
> 155	| BR-RISK-CAD-001 | **Inbox nasce vazio em prod** sob Standard Access (webhook só entrega role users); time declara "funciona" testando com conta própria ⇒ Fatia 2 shipa morta | 4 | 5 | **20** | Gate Lei 1: DM real de **terceiro sem role** antes de qualquer FR de inbound; senão App Review vira pré-requisito da Fatia 2 (FM-CAD-02, RPN técnico 486) |
> 156	| BR-RISK-CAD-002 | **Cold DM / janela expirada** enfileirado ⇒ violação de política ⇒ **ban do app Meta** (não erro HTTP) — atinge TODOS os tenants (app global) | 3 | 5 | **15** | FK NOT NULL p/ inbound (cold DM impossível de representar); gate de janela no send; 2 relógios (24h CSW × 7d private reply); cap por-APP + kill-switch global (FM-CAD-03/OTD-CAD-018) |
> 157	| BR-RISK-CAD-003 | **Opt-out ignorado** (revogação chega depois do enqueue) ⇒ **sanção ANPD** (LGPD Art. 8 §5) | 3 | 5 | **15** | `withdrawn_at` checado **no send**, independente da base legal; cascata no `erase_lead()` (FM-CAD-04; OTD-CAD-006) |
> 158	| BR-RISK-CAD-004 | **Custo X invisível**: publish-com-URL a US$0,200/req sangra o tenant sem entrar no ledger ⇒ `collective_efficiency_ledger` mente (Lei 1) | 4 | 4 | **16** | X FORA da allowlist da Fatia 1; precificar 45 mco (4×-floor) + probe de créditos; `external_usd_cost` no reconcile (FM-CAD-10/OTD-CAD-011) |
> 159	| BR-RISK-CAD-005 | **Double-post** por tick sobreposto/retry ⇒ flood + feedback negativo ⇒ risco de ban | 3 | 4 | **12** | Índice único parcial + `ON CONFLICT DO NOTHING RETURNING` + `overlap_policy=skip`; pg_cron não sobrepõe a mesma job (FM-CAD-01) |
> 160	| BR-RISK-CAD-006 | **Falso-sucesso do 202**: reporta "enviado" sem webhook de status ⇒ métrica e cobrança mentem (Lei 1) | 4 | 3 | **12** | `sent` só do webhook de status; reconciliação obrigatória (FM-CAD-05) |
> 161	| BR-RISK-CAD-007 | **AI Provider Brasil**: Meta cobra cada msg não-template ⇒ auto-reply "grátis" pode não valer no mercado do Usuário Zero | 3 | 4 | **12** | Consultar Meta/rate cards **antes** de flipar auto-reply para `sent`; registrar `external_usd_cost` (OTD-CAD-009, bloqueante econômico) |
> 162	| BR-RISK-CAD-008 | **Rodapé/disclosure delegado ao LLM** ⇒ alucinação omite endereço/opt-out/disclosure de IA ⇒ CAN-SPAM + AI Act | 3 | 4 | **12** | Montagem **server-side** concatenada, nunca no prompt (G10/G12/FM-CAD-12) |
> 163	| BR-RISK-CAD-009 | **Cron em GMT vira "toda segunda 9h"** (horário do user como cron expression) ⇒ cadência multi-tenant errada por fuso | 3 | 3 | **9** | `next_run_at` computado em UTC no re-arm; cron nunca carrega preferência de horário (FM-CAD-06) |
> 164	| BR-RISK-CAD-010 | **Legitimidade contratual BYOK**: armazenar System User token de terceiro pode caracterizar Tech Provider (Meta Platform Terms) | 2 | 4 | **8** | Revisão jurídica antes do Usuário 1 (OTD-CAD-010) |
> 165	| BR-RISK-CAD-011 | **AI Act Art. 50(1)** entra em vigência 2026-08-02 sem disclosure server-side ⇒ não pode operar na UE | 2 | 4 | **8** | Disclosure server-side por construção (G12); gate de jurisdição fail-closed = UE (G11/OTD-CAD-015) |
> 166	| BR-RISK-CAD-012 | **`estimateNodeCost` NaN** por kind faltando no switch (`strict:false` esconde) ⇒ `runAllCost` quebra silenciosamente | 4 | 2 | **8** | Corrigir `publishSocial` de quebra (Fatia 0); checklist manual de 6 edições (FM-CAD-16/OTD-CAD-007) |
> 167	
> 168	---
> 169	
> 170	## 9. Business Acceptance Criteria
> 171	
> 172	| ID | Criterion | Verification Method |
> 173	|----|-----------|-------------------|
> 174	| BAC-CAD-001 | Fatia 0 (P0) fechada: `whatsapp-webhook` alcançável (bloco `config.toml`) + `timingSafeEqual`; `estimateNodeCost` com `publishSocial`; `erase_lead()` cascata; `auto-publish` em pg_cron + `FOR UPDATE SKIP LOCKED` | `curl` do webhook (não-401) + diff das 4 correções + `/security-review` da migration |
> 175	| BAC-CAD-002 | ≥1 plano `plan_kind='cadence'` ativo para o Usuário Zero, armado com hora/weekday/timezone | `SELECT count(*) FROM autopilot_plans WHERE plan_kind='cadence' AND is_active` (UUID real) |
> 176	| BAC-CAD-003 | Zero double-post sob tick sobreposto/retry | Smoke re-executável provando índice único parcial (`WHERE status<>'failed'`) |
> 177	| BAC-CAD-004 | 100% dos `sent` originados do webhook de status (nunca do 202) | Inspeção de `cadence_dispatches.status` + trace de reconcile |
> 178	| BAC-CAD-005 | `profiles.timezone` e `channel_profiles.cadence` com ≥1 leitor cada (eram 0) | `grep` de leitores no repo após a Fatia 1 |
> 179	| BAC-CAD-006 | Inspector projeta mco/ciclo antes de armar; `budget_cap_mco` NOT NULL | Screenshot do inspector + DDL da coluna |
> 180	| BAC-CAD-007 | Nenhuma migration mergeada sem `/security-review` sem findings | Output do `/security-review` por migration |
> 181	| BAC-CAD-008 | Probe FM-CAD-02 fechado (DM real de terceiro sem role no banco + payload cru) **antes** de qualquer FR de inbound | Linha real em `lead_events` + payload cru arquivado |
> 182	| BAC-CAD-009 | IoC falha se script fora de `scripts/qa/` importar o driver de browser e tocar instagram.com/facebook.com | Smoke/IoC executável (exit 1 no toque proibido) |
> 183	| BAC-CAD-010 | Custo externo BYOK registrado em `external_usd_cost` mesmo com cobrança mco=0 | `SELECT external_usd_cost, cost_source FROM cadence_dispatches` após reconcile |
> 184	
> 185	---
> 186	
> 187	## 10. Traceability Matrix
> 188	
> 189	| MR ID | BR ID | FR candidato | OTD / FM | PR ID (stub) |
> 190	|-------|-------|--------------|----------|--------------|
> 191	| MR-CAD-001 | BR-CAD-001, BR-CAD-004 | FR-CAD-001, FR-CAD-005 | OTD-CAD-002, OTD-CAD-007 | _to be linked in PRD_ |
> 192	| MR-CAD-002 | BR-CAD-004, BR-CAD-005 | FR-CAD-002, FR-CAD-007 | FM-CAD-06 | _PRD_ |
> 193	| MR-CAD-003 | BR-CAD-006 | FR-CAD-008 | OTD-CAD-008, OTD-CAD-017 | _PRD_ |
> 194	| MR-CAD-004 | BR-CAD-007 | FR-CAD-009 | — | _PRD_ |
> 195	| MR-CAD-005 | BR-CAD-008 | FR-CAD-010 | OTD-CAD-016 | _PRD_ |
> 196	| MR-CAD-006 | BR-CAD-003, BR-CAD-009 | FR-CAD-003, FR-CAD-006 | FM-CAD-01, FM-CAD-07 | _PRD_ |
> 197	| MR-CAD-007 | BR-CAD-010 | FR-CAD-011 | OTD-CAD-011 | _PRD_ |
> 198	| MR-CAD-008 | BR-CAD-002, BR-CAD-004 | FR-CAD-002, FR-CAD-004 | OTD-CAD-003 | _PRD_ |
> 199	| MR-CAD-009 | BR-CAD-011 | FR-CAD-006 | OTD-CAD-004, OTD-CAD-005 | _PRD_ |
> 200	| MR-CAD-010 | BR-CAD-012, BR-CAD-013 | FR-CAD-011, FR-CAD-014 | OTD-CAD-009, OTD-CAD-010 | _PRD_ |
> 201	| MR-CAD-011 | BR-CAD-014, BR-CAD-013 | FR-CAD-012, FR-CAD-013 | FM-CAD-03/04/05/12/15 | _PRD_ |
> 202	| MR-CAD-012 | BR-CAD-015 | FR-CAD-012, FR-CAD-013 | FM-CAD-02 (RPN 486), FM-CAD-13, OTD-CAD-018 | _PRD_ |
> 203	| MR-CAD-013 | BR-CAD-016 | FR-CAD-014 | — | _PRD_ |
> 204	| MR-CAD-014 | BR-CAD-017 | (Fatia 0) | OTD-CAD-001, OTD-CAD-004, OTD-CAD-006, OTD-CAD-007 | _PRD_ |
> 205	
> 206	> **Decisões abertas (§11 do blueprint) que a PRD/SDD deve resolver:** (1) sujeito da cadência; (2) estender `autopilot_plans` vs tabela nova; (3) `channel_profiles.cadence` autoritativo vs sugestão; (4) escopo de canal da Fatia 1; (5) jurisdição default sem país; (6) semântica `cadence_dispatches`; (7) IG/Messenger no app global vs BYOK-de-app. Recomendações do blueprint adotadas como **Assumptions** (§7). **`/bok-scribe` deve selar a numeração `FR-CAD-xxx` na FRD** — aqui são candidatos.
> 207	
> 208	---
> 209	
> 210	_Generated by MCORCH BoK Scribe Agent v1.0.0 — fiel a `00-deepsearch-blueprint.md` + `01-mrd.md` (Lei 1: nenhum FR/OTD/FM/entidade inventado além do blueprint; §3 sob selo de não-verificação; ROI/TAM numérico marcado como não quantificado, não improvisado). Convenções MCORCH: lógica/vars em inglês, UI/toasts pt-BR; BYOK per-user fail-closed 402/501; cobrança via RPC atômica begin/finalize; verify_jwt=false → ES256 JWKS / HMAC timingSafeEqual; RLS default-deny owner-scoped._
> 211	
> ```

## 🤖 Claude *(15:53:58)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-repurpose/00-deepsearch-blueprint.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# video-repurpose — Deepsearch Blueprint (semente de BoK)
> 2	
> 3	> **Tipo:** Blueprint-semente fundamentado (deepsearch) — o motor que FALTA: o MCORCH **distribui** mas não **produz cortes**. Constrói a metade que falta reusando a metade que já existe.
> 4	> **Status:** ✅ Blueprint autorado 2026-07-12 (Closed-Loop Step 0). Abre o BoK gate para a **Fatia 1 (ingest)**. FRD/SDD por-fatia antes das fatias pesadas (worker/carrossel).
> 5	> **Diretiva Sovereign 2026-07-12:** motor de REPURPOSE de vídeo externo — 1 documentário longo (16:9, ~7-8 min, "Gabriel AI") + metadados estruturados + SRT → N Shorts 9:16 (reenquadrados, legenda queimada) + carrosséis IG + post WordPress, **escoando pelos trilhos que já existem**.
> 6	> **ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = `/security-review` por seam + Sovereign · Owner = Sovereign (alcance público depende de auditoria de app — ação dele, não código).
> 7	> **Referência externa (o "mapa dos nós"):** repo público `gabrielZarattini/GabrielAI` (ref `da5b53b`) — pipeline HÍBRIDO VALIDADO (4 episódios 6+ min: N takes Veo 8s → 1 master via ponte Premiere). **Fundamental:** esse pipeline é o **INVERSO** deste (montagem N→1); ele é a **FONTE do master**, o **schema de metadados** e a **filosofia data-driven**, não o molde do segmenter.
> 8	
> 9	---
> 10	
> 11	## 1. Tese (uma frase)
> 12	
> 13	O MCORCH já tem a **saída** (publish-social/publish-wordpress/reshape-pillar/channel_profiles/scheduled_posts+auto-publish + o sink `publish-space-asset`→`space_publish_variants`) e o **motor de render determinístico** (HyperFrames `render-core.ts` + o worker `video-bridge.ts` sobre a fila `video_renders`); falta a **entrada e a transformação de vídeo** — ingerir um MP4 externo, cortá-lo em N shorts, reenquadrar 16:9→9:16, queimar legenda, e extrair carrosséis — e **fiar** o resultado nos trilhos existentes.
> 14	
> 15	## 2. Fundamentação material (Lei 1 — cada pointer verificado neste turno)
> 16	
> 17	| Claim (snapshot Sovereign) | Realidade verificada (file:line) |
> 18	|---|---|
> 19	| creative_assets rejeita origem externa (CHECK sem 'external') | ✅ `supabase/migrations/20260710170000_creative_assets_source_module_reunion.sql:15,55` — `source_module IN ('canvas-studio','hyperframes','open-design','content-pipeline','generate-image','faceless','spaces','avatar-studio')` — **sem 'external'**. `kind` inclui `'video'` (`20260625120000:24`). |
> 20	| channel-format "1 longo→N shorts" (dito OTD-CP-011, deferred) | ✅ é **FR-CP-012** (`12-amendment-channel-format-intelligence.md:83`) "Auto-segmentação 1 fonte longa → N shorts (Hormozi), owner HyperFrames, worker=segmenter, *slice posterior*". SDD `13-sdd-reshaper-atomizer.md:196`: **"N/A hoje: não há vídeo-fonte LONGO no pipeline para segmentar (geramos clipes curtos). Aplicável quando entrar INPUT de vídeo longo."** ⇒ **este motor É o gatilho que destrava FR-CP-012.** |
> 21	| reframe de vídeo (OTD-CP-009 cobre só imagem) | ✅ nuance: **OTD-CP-009 está FECHADA** (`13-…:190`) — reframe de **imagem** in-process (imagescript WASM). Reframe de **vídeo** é gap **não coberto** por nenhuma OTD. |
> 22	| youtube-studio §Pilar I (falta camada FFmpeg de montagem/segmentação) | ✅ `youtube-studio/00-…:53-59` — Pilar I = **assembler multi-cena (concat N→1)**, "a cola que falta". ⚠️ **Pilar I é MONTAGEM; a SEGMENTAÇÃO (1→N) deste motor é o inverso — gap distinto** (embora reuse o mesmo worker-shape FFmpeg). O render 16:9 já existe (`render-core.ts:71` template `viral-long-16x9`). |
> 23	| video-bridge.ts pattern (poll→claim→heartbeat→render→finalize→dual-write) | ✅ `scripts/video-bridge.ts:5-6,53-60,121,128,205` — fila `video_renders` engine='hyperframes', claim atômico queued→running + reaper `RUNNING_TIMEOUT_MS`, `finalize_video_render` (única autoridade terminal), `register_creative_asset` dual-write. **Molde exato do worker de segmentação.** |
> 24	| render-core.ts HTML→PNG | ✅ `scripts/hyperframes/render-core.ts:10-13` — Playwright headless → `page.screenshot(PNG)` por frame → FFmpeg PNG→MP4 bitexact. Aceita `images[]` pré-gerados (`:108`). **Reusável para slides de carrossel.** |
> 25	| publish-social IG só Reels | ✅ `supabase/functions/publish-social/index.ts:167` — `media_type: "REELS"` apenas; **sem CAROUSEL**. |
> 26	| channel_profiles surface carousel | ✅ existe mas **só LinkedIn/PDF** (`20260628120000_channel_profiles_carousel.sql:12-18`) e o comentário `:7` diz explicitamente **"IG/TikTok photo-carousel are image-set variants for a later slice."** `generate-carousel` (fn) existe mas emite **PDF** (pdf-lib, 1080×1350, LinkedIn). |
> 27	| disclosure sintética hard-coded | ✅ `publish-social/index.ts:325` `is_aigc: true` (TikTok), `:429` `containsSyntheticMedia: true` (YouTube), `:297` TikTok `SELF_ONLY` forçado pré-audit. **Preservar.** |
> 28	| sink que consome os clipes | ✅ `space_publish_variants` + `publish-space-asset` (landados 2026-07-12) — `asset_kind` video/image, resolve owner-scoped de `creative_assets`. **Os clipes/carrosséis registrados como creative_assets já são publicáveis por ele.** |
> 29	| IG CAROUSEL API contract | ✅ Meta docs (developers.facebook.com/docs/instagram-platform/content-publishing): child `POST /<IG_ID>/media` `image_url`+`is_carousel_item=true` → parent `media_type=CAROUSEL`+`children` (CSV ≤10) → `POST /<IG_ID>/media_publish` `creation_id`. Host `graph.instagram.com` (= o branch IG atual). |
> 30	
> 31	**Lição-âncora do GabrielAI (BoK §4, verbatim):** *"O DOM é CEGO para o que a transição DESENHA"* — o Premiere reporta "aplicada, ok" e o render mostra banner de erro. No FFmpeg/HyperFrames o pixel é controlado direto (o "DOM cego" some), **mas o gate "olhe o render" (Vision QA) é obrigatório** em cada clipe/carrossel. Lei 1 aplicada a mídia.
> 32	
> 33	## 3. Os 5 Pilares (mapeiam os passos 1-5 da diretiva)
> 34	
> 35	### Pilar I — INGEST de ativo externo (porta de 1ª classe) · Fatia 1
> 36	**Gap:** `creative_assets` rejeita origem externa. **Decisão de schema (§5):** adicionar `source_module='external'` (aditivo, espelha a reunion `20260710170000`) — **não** tabela dedicada, porque o spine `creative_assets` é lido por TODOS os consumidores (sink, workers, biblioteca); fragmentar em tabela nova quebraria a interop. O master externo vira `creative_assets` `kind='video'`, `source_module='external'`, `provider='upload'|'youtube'`, com os **metadados estruturados** (schema espelhando `episodios/epNN.json`: `titulo/subtitulo/atos[]=capítulos/creditos.blocos[]=fontes/teaser/tags`) + a **ref do SRT** (pt-BR/en) no `metadata` jsonb.
> 37	- **DEFAULT:** upload do MP4 (client→bucket privado→seam `ingest-external-asset` registra owner-scoped). Melhor qualidade, funciona.
> 38	- **FALLBACK:** link YouTube (recompressão = perda dupla; conveniência). ⚠️ **OTD-VR-001:** download server-side do YouTube é **bloqueado por IP de datacenter** ([[reference_youtube_datacenter_workarounds]]) — a fatia registra o intent mas o download real fica gated (host worker / ação Sovereign). Não-preferido por design.
> 39	
> 40	### Pilar II — Worker de SEGMENTAÇÃO / REFRAME / CAPTION · Fatia 2 (destrava FR-CP-012)
> 41	Espelha `video-bridge.ts` (poll `video_renders` + claim atômico + heartbeat + `finalize_video_render` + dual-write `register_creative_asset`), **engine novo** `video_renders.engine += 'repurpose'` (aditivo, molde `qwen3-voice` `20260709234000:34`). Rail **grátis** (FFmpeg, `charged_mco=0`). O `composition` jsonb carrega a **cut-spec data-driven** (lista `{in, out, reframe, caption_source}` por clipe — **não cravada**, filosofia `mapa_transicoes.py` do GabrielAI: cortes de dado, não de texto). Operações FFmpeg (canônicas, cf. `ffmpeg.org/ffmpeg-filters.html` já citado no youtube-studio blueprint):
> 42	- **corte** 1 longo → N: `-ss <in> -to <out>` por clipe (stream-accurate);
> 43	- **reframe 16:9→9:16 subject-safe:** `crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920` (center default; **OTD-VR-002:** crop dinâmico subject-aware = fatia posterior, MVP=center-safe);
> 44	- **queima de legenda:** `subtitles=<srt>` (filtro `subtitles`, do SRT ingerido ou texto por clipe) — ≠ GabrielAI (que envia SRT como faixa no MASTER; aqui os SHORTS queimam, contexto social distinto);
> 45	- **saída:** clipes MP4 9:16 registrados `creative_assets` `kind='video'` `source_module='external'` (derivado, `parent_asset_id`=master) → **o sink `publish-space-asset` já sabe consumir**.
> 46	
> 47	### Pilar III — CARROSSEL de Instagram · Fatia 3
> 48	Extrai key-frames do master (`ffmpeg -ss <t> -frames:v 1`) em timestamps (dos `atos[]`/capítulos), compõe slides via **`render-core.ts`** (HTML→PNG existente, aceita `images[]`): quadro + citação/legenda, **1080×1350** (4:5). Estende a branch IG do `publish-social` para **`media_type=CAROUSEL`** (children `image_url`+`is_carousel_item=true`, ≤10 → parent → `media_publish`). Reusa a superfície `carousel` do `channel_profiles` (hoje LinkedIn/PDF; **OTD-VR-003:** adicionar surface IG-carousel image-set, que o próprio migration `20260628120000:7` já marcou "later slice").
> 49	
> 50	### Pilar IV — MAPEADOR de metadados · Fatia 4
> 51	Lê os metadados estruturados do episódio (schema `episodios/epNN.json`) e emite: (a) a **legenda nativa por plataforma** e (b) o **corpo HTML do WordPress** (vídeo embedado + **fontes creditadas** de `creditos.blocos[]` — não perder capítulos/fontes). **OTD-VR-004:** o `reshape-pillar` é pillar-coupled (`pillar_run_id`+`pillar_atoms`); o mapeador reusa a **gramática `field_map` / voicing** do `channel_profiles.transform_recipe` mas alimentada pelo metadado do episódio (não por um pillar_run) — a decisão exata (adaptar reshape-pillar vs. mapper leve dedicado) é FRD da Fatia 4.
> 52	
> 53	### Pilar V — FIAR na distribuição existente · Fatia 5
> 54	Clipes/carrosséis/post escoam por: **`publish-space-asset`→`space_publish_variants`→`auto-publish`→`publish-social`** (TikTok/YT/IG) + **`publish-wordpress`**. Disclosure sintética (is_aigc/containsSyntheticMedia) **hard-coded preservada**. **Gate externo honesto (não código):** alcance público depende de auditoria de app — TikTok força `SELF_ONLY`, YouTube pode forçar privado pré-audit (`publish-social:290-297,388`). Ação do Sovereign.
> 55	
> 56	## 4. FR / OTD / FM (semente — refinar por FRD de fatia)
> 57	
> 58	| FR | Descrição | Fatia |
> 59	|---|---|---|
> 60	| FR-VR-001 | Ingest de MP4 externo owner-scoped (`source_module='external'`) + metadados + SRT | 1 |
> 61	| FR-VR-002 | Fallback link YouTube (best-effort, gated datacenter-IP) | 1 |
> 62	| FR-VR-003 | Worker de segmentação data-driven (cut-spec `{in,out}` → N clipes) — destrava FR-CP-012 | 2 |
> 63	| FR-VR-004 | Reframe 16:9→9:16 (+ opção 1:1) center-safe | 2 |
> 64	| FR-VR-005 | Queima de legenda (SRT/texto por clipe) nos shorts | 2 |
> 65	| FR-VR-006 | Key-frames → slides carrossel via render-core (1080×1350) | 3 |
> 66	| FR-VR-007 | Branch IG `media_type=CAROUSEL` no publish-social | 3 |
> 67	| FR-VR-008 | Mapeador metadado→legenda nativa + corpo HTML WordPress (fontes preservadas) | 4 |
> 68	| FR-VR-009 | Fiar em publish-space-asset/publish-wordpress (reuso puro) | 5 |
> 69	
> 70	| OTD | Débito |
> 71	|---|---|
> 72	| OTD-VR-001 | YouTube download bloqueado por IP datacenter — fallback gated |
> 73	| OTD-VR-002 | Reframe subject-aware (crop dinâmico) diferido; MVP center-safe |
> 74	| OTD-VR-003 | Surface IG-carousel image-set no channel_profiles (o migration já previu "later") |
> 75	| OTD-VR-004 | Mapeador: adaptar reshape-pillar vs mapper dedicado (decisão FRD Fatia 4) |
> 76	| OTD-VR-005 | Cut-spec: fonte do `{in,out}` (capítulos/atos → manual → Hormozi hook-detector futuro) |
> 77	| OTD-VR-007 | **Caption-fit do slide de carrossel (FFmpeg drawtext):** o wrap é por contagem de chars (sem medir a largura real da fonte) → legendas MUITO longas com palavras largas podem clipar ~1 char na última linha. Mitigado conservador (`MAX_CHARS=16`, left-align, ≤6 linhas) — legendas curtas (nomes de capítulo/hooks) saem limpas (Vision QA 2026-07-12). Typografia pixel-perfect = via render-core HTML→PNG (auto-wrap CSS), diferido. |
> 78	| OTD-VR-006 | **Fatia 2 read-time guard (do /security-review da Fatia 1):** o worker de segmentação (service-role) fará `download`/sign de `(storage_bucket, storage_key)` da linha `creative_assets` — DEVE (a) allowlist `storage_bucket` e (b) re-validar o prefixo `${user.id}/` + rejeitar `..` no READ, não confiar na linha armazenada. A Fatia 1 já allowlista o bucket + rejeita `..` no INGEST (defense-in-depth na fonte), mas o worker não pode assumir isso. |
> 79	
> 80	| FM (FMEA) | Vetor | Mitigação |
> 81	|---|---|---|
> 82	| FM-VR-01 | Ingest de asset alheio (cross-tenant) | seam owner-scoped (key-prefix `${uid}/` OU resolve por user_id), register service-role-only |
> 83	| FM-VR-02 | Worker assina bucket/objeto de outro tenant | claim por `user_id` da linha `video_renders` (server-trusted), como video-bridge; **+ re-validar `(bucket allowlist, key prefix ${uid}/, no `..`)` no READ (OTD-VR-006)** — não confiar na linha armazenada |
> 84	| FM-VR-03 | Carrossel publica asset alheio | mesmo hard-bind `.eq user_id=post.user_id` do sink (FMEA-011) |
> 85	| FM-VR-04 | Master externo enorme estoura memória/custo | piso/teto de tamanho + timeout no worker (não no edge) |
> 86	| FM-VR-05 | Publicar sem disclosure sintética | is_aigc/containsSyntheticMedia hard-coded (não removível) |
> 87	
> 88	## 5. Decisão de schema do Pilar I (com prova — a única decisão da Fatia 1)
> 89	
> 90	**`source_module='external'` aditivo** (não tabela dedicada). Prova/razão: `creative_assets` é o spine canônico lido por sink+workers+biblioteca (`UNIQUE(bucket,key)`, RLS own-or-org, `register_creative_asset` service-role-only). Adicionar 'external' ao CHECK+RPC é o padrão **já usado 2×** (spaces `20260707230000`, avatar-studio `20260710170000`) e mantém a interop. Tabela dedicada fragmentaria o spine (todo consumidor teria que ler 2 fontes). Metadados ricos → `metadata` jsonb (sem tabela nova na Fatia 1); a fila do worker (Fatia 2) reusa `video_renders.composition` + engine 'repurpose'. **Money-path (`channel_variants`/reshaper/`pipeline_runs`) intocado.**
> 91	
> 92	## 6. Reuse map — NÃO reconstruir (diretiva explícita)
> 93	
> 94	Reusar sem tocar: `publish-social`, `publish-wordpress`, `reshape-pillar`, `channel_profiles`, `render-core.ts`, `video-bridge.ts` (molde), `finalize_video_render`, `register_creative_asset`, `space_publish_variants`+`publish-space-asset` (o sink), `scheduled_posts`+`auto-publish`. **Não** escoar por viral-autopilot (product-centric ML, caminho errado p/ documentário). **Não** ingerir via browser (arquivo/API oficial).
> 95	
> 96	## 7. Pattern Conformance Declaration (21 padrões · `docs/architecture/agentic-vision.md`)
> 97	
> 98	| Pattern | Impl? | Como / porquê-deferido |
> 99	|---|---|---|
> 100	| 1 Prompt Chaining | yes | ingest→segment→reframe→caption→carousel→publish é uma cadeia de estágios |
> 101	| 2 Routing | yes | cut-spec dirige N clipes; channel_profiles roteia por canal/superfície |
> 102	| 3 Parallelization | yes | N clipes / N slides renderizam em paralelo (fila video_renders) |
> 103	| 4 Reflection | yes | gate Vision QA ("olhe o render") por clipe/carrossel — herdado do GabrielAI |
> 104	| 5 Tool Use | yes | FFmpeg/Playwright/IG API/WordPress REST |
> 105	| 6 Planning | yes | cut-spec data-driven = o plano de cortes |
> 106	| 7 Multi-Agent | n-a | worker single-tenant Usuário Zero (multi-tenant = hardening posterior) |
> 107	| 8 Memory | deferred | provenance via `parent_asset_id` (master→clipes) cobre linhagem; mesh node OTD |
> 108	| 9 Learning/Adaptation | deferred | hook-detector Hormozi (OTD-VR-005) aprenderia melhores cortes — fatia futura |
> 109	| 10 Goal Setting | yes | objetivo por episódio nos metadados (atos/teaser) |
> 110	| 11 Exception/Recovery | yes | worker fail→finalize(failed)+refund (charged 0); reaper de dead-worker |
> 111	| 12 HITL | yes | rascunho default no sink (opt-in publish), gate Sovereign de alcance |
> 112	| 13 Guardrails | yes | owner-scoping (FM-VR-01..03), disclosure sintética, piso/teto de tamanho |
> 113	| 14 Prioritization | yes | channel_profiles.priority já ordena canais |
> 114	| 15 Resource-Aware | yes | rail grátis (charged 0); teto de tamanho/timeout |
> 115	| 16 Reasoning (CoT) | n-a | pipeline determinístico, não raciocínio LLM no core |
> 116	| 17 Eval/Monitoring | yes | Vision QA gate + infra_health_logs telemetry |
> 117	| 18 Orchestration | yes | fila video_renders + auto-publish cron |
> 118	| 19 Knowledge Retrieval | yes | metadados/fontes creditadas preservados no mapeador |
> 119	| 20 Inter-Agent Comm | n-a | sem múltiplos agentes no runtime |
> 120	| 21 Self-Improvement | deferred | métricas de creative → melhores cut-specs (junto do padrão 9) |
> 121	
> 122	## 8. Ordem de fatias & gates (parar no gate natural, molde space_publish_variants)
> 123	
> 124	1. **Fatia 1 — Ingest:** SOP Lei 2 + migration `source_module='external'` + seam `ingest-external-asset` + /security-review → **PARA no apply-gate** (comando pronto). ← **1º GATE (este arco).**
> 125	2. **Fatia 2 — Worker segment/reframe/caption:** FRD/SDD de fatia + engine 'repurpose' + worker + smoke + **1 clipe 9:16 renderizado e INSPECIONADO** (Vision QA).
> 126	3. **Fatia 3 — Carrossel IG:** slides via render-core + branch CAROUSEL + **1 carrossel VISTO**.
> 127	4. **Fatia 4 — Mapeador:** legenda nativa + corpo WP com fontes.
> 128	5. **Fatia 5 — Fiar:** E2E ingest→short→publicado (gated no alcance externo = Sovereign).
> 129	
> 130	**Cross-links:** [[project_lora_witness_and_otd_spaces_036]] (o sink) · post-engine FR-CP-012 (destravado) · youtube-studio Pilar I (irmão de montagem) · OTD-CP-009 (reframe de imagem, fechado; vídeo é este motor).
> 131	
> ```

## 🤖 Claude *(15:54:07)*


## 🤖 Claude *(15:54:09)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/spaces-cadence/03-prd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# PRD — Product Requirements Document
> 2	
> 3	**Project:** spaces-cadence
> 4	**Version:** v0.1 | **Date:** 2026-07-15
> 5	**BoK Applied:** ProdBOK + CXBOK
> 6	**Status:** Draft
> 7	**Source of truth:** [`00-deepsearch-blueprint.md`](00-deepsearch-blueprint.md) (verificação externa 2026-07-14) + [`01-mrd.md`](01-mrd.md) + [`02-brd.md`](02-brd.md). Todo item de produto abaixo deriva 1:1 de uma BR-CAD-xxx / MR-CAD-xxx e das seções §5/§6/§7 do blueprint; nada é inventado além dele (Lei 1).
> 8	
> 9	> **ORO triplet desta task:**
> 10	> - **Operator:** MCORCH Master Execution Agent
> 11	> - **Reviewer:** Sovereign (Gabriel)
> 12	> - **Owner:** Sovereign — blast radius material: **ban de app Meta/X** (spam de 1 tenant no app global bane todos — OTD-CAD-018) + **sanção ANPD até 2% do faturamento** (LGPD Art. 52).
> 13	>
> 14	> **Closed-Loop gate:** este é o **3º** documento da suíte. Permanecem ABERTOS: 04-frd → 05-sdd, `09-pattern-conformance.md`, SOP Lei 2 (`docs/processes/spaces-cadence.md`), `/security-review` de toda migration. **Nenhuma linha de código antes disso.**
> 15	>
> 16	> **Nota de fidelidade (Lei 1):** o blueprint declara **zero FR de inbound** antes do payload cru de DM real. Os `FR-CAD-xxx` citados são **candidatos** derivados de §5/§7 — a numeração `FR-CAD-xxx` será **selada pela FRD**; aqui são propostos e rastreados. Os `PR-CAD-xxx` deste doc são **itens de produto** (features MoSCoW), distintos dos FRs. §3 (posicionamento vs. ManyChat) carrega **SELO DE NÃO-VERIFICAÇÃO**: nenhum item de produto cita §3 como fato; só a coluna MCORCH (verificável no repo) alimenta a diferenciação.
> 17	
> 18	---
> 19	
> 20	## 1. Product Vision Statement
> 21	
> 22	> Para **produtores de conteúdo de afiliados/marca** (Usuário Zero e tenants BYOK) que precisam de **recorrência de publicação com semântica de calendário** e — probe-gated — do fechamento do laço inbound, o **nó Cadência do Spaces** é um **motor de sequência Postgres-first embutido no Canvas Studio** que agenda com hora-do-dia + weekday + timezone + quiet-hours + frequency-cap + digest + A/B + idempotência e enfileira nos trilhos vivos de distribuição. Diferente de um respondedor de DM avulso, o nó é **alimentado pelo mesmo motor que criou o post e medido pelo mesmo ledger que mede a receita** — sem reconstruir distribuição e sem um terceiro driver de recorrência.
> 23	
> 24	---
> 25	
> 26	## 2. User Personas
> 27	
> 28	### Persona 1 — Usuário Zero (Gabriel) (Primary)
> 29	
> 30	| Attribute | Detail |
> 31	|-----------|--------|
> 32	| Role | Sovereign / dono do app Meta **global** do MCORCH (Standard Access); opera como piloto enterprise interno |
> 33	| Goals | Armar uma cadência de publicação recorrente (hora/weekday/timezone) sobre um asset já produzido, ver o custo projetado em mco **antes** de armar, sem gastar mco na criação do plano |
> 34	| Frustrations | Só existe `next_run_at + interval_days` (sem hora/weekday/tz); `profiles.timezone` e `channel_profiles.cadence` são dados mortos; o post gera comentário/DM mas o laço inbound morre (webhook descarta com 200 OK) |
> 35	| Tech-savviness | 5 (expert — Lead Architect) |
> 36	| MCORCH usage pattern | Canvas Studio (Spaces) → nó `cadence` categoria Publish; sujeito = `creative_assets.id` owner-scoped; inspector com poll molde `useVoiceRenderPoll` |
> 37	| Quote | _"Quero armar a cadência uma vez, ver quanto vai custar por ciclo, e nunca postar duas vezes o mesmo dispatch."_ |
> 38	
> 39	### Persona 2 — Tenant BYOK (Secondary, pós-Usuário 1)
> 40	
> 41	| Attribute | Detail |
> 42	|-----------|--------|
> 43	| Role | Cliente multi-tenant que traz o próprio app Meta + WABA + System User token + método de pagamento |
> 44	| Goals | Cadência de publicação keyless imediata (Fatia 1, sem review); canais BYOK desimpedidos (Telegram/Email); WhatsApp Cloud com o próprio app |
> 45	| Frustrations | IG multi-tenant é gated por App Review + Business Verification; auto-reply WhatsApp pode custar por mensagem (enquadramento AI Provider Brasil — OTD-CAD-009); System User token de terceiro pode caracterizar Tech Provider (OTD-CAD-010) |
> 46	| Tech-savviness | 3–4 (developer direto do próprio app) |
> 47	| MCORCH usage pattern | BYOK per-user fail-closed (`resolveProviderKey`); custo externo absorvido pelo tenant, **registrado** em `external_usd_cost` mesmo com cobrança mco=0 |
> 48	| Quote | _"Trago meu próprio app e minha própria conta; o MCORCH orquestra e mede, mas quem paga a plataforma sou eu."_ |
> 49	
> 50	---
> 51	
> 52	## 3. User Journey Maps
> 53	
> 54	### Journey 1: Armar Cadência de Publicação (Usuário Zero, Happy Path — Fatia 1)
> 55	
> 56	| Stage | Action | Touchpoint | Emotion | Opportunity |
> 57	|-------|--------|-----------|---------|-------------|
> 58	| Awareness | Percebe que precisa publicar um asset toda 2ª/4ª/6ª às 09h BRT | Canvas Studio (Spaces) | 😐 Neutral | Aliases pt-BR no registry: cadência/agendar/recorrente/cron/calendário |
> 59	| Consideration | Adiciona nó `cadence` (categoria Publish), liga o asset via handle `input_asset` | `CadenceNode` + `RightPanel` | 🤔 Curious | Nó keyless, sem gate "runnable" (não exige `prompt`) |
> 60	| Activation | Define recurrence {frequency, days, hours, minutes, tz}, quiet-hours, `channel_allowlist`, `budget_cap_mco` | `CadenceInspector` → `cadence-plan` | 😊 Excited | Inspector projeta **custo por ciclo em mco** (Σ canal × ocorrências até cap) **antes** de armar |
> 61	| Value | Plano armado (`plan_kind='cadence'`, `next_run_at` UTC); tick `autopilot-cadence-cron` dispara no fuso certo → `scheduled_posts` → `auto-publish` publica | `autopilot_plans` + `cadence_dispatches` + inspector poll | 🚀 Delighted | Ressuscita `profiles.timezone` (fuso) + `channel_profiles.cadence` (teto); idempotência impede double-post |
> 62	| Retention | Vê as últimas N dispatches + `next_run_at` no inspector; ajusta cap/quiet-hours; kill-switch `is_active=false` a qualquer momento | Inspector + `notify()` + sino | ❤️ Loyal | Custo agregado no `collective_efficiency_ledger`; overlap/catchup/jitter mantêm a cadência sã após quedas |
> 63	
> 64	#### Edge Case 1: Frequency cap / quiet-hours atingido
> 65	> No dispatch, se o `channel_profiles.cadence` (teto autoritativo por canal) já foi atingido na janela, o gate faz **HALT** (não reenfileira — semântica Knock); se o horário cai em quiet-hours no fuso do sujeito (cascata `recurrence.tz → profiles.timezone → America/Sao_Paulo`), o dispatch é suprimido. Diferença estrutural entre **cadência** e **flood** (G4). Toast pt-BR informativo; nenhuma publicação.
> 66	
> 67	#### Edge Case 2: Backlog storm após queda de N horas
> 68	> Ao voltar, o tick não dispara todos os planos atrasados de uma vez: `catchup_window` (default 6h) descarta vencimentos antigos e `jitter_seconds` + fan-out bounded (`MAX_PER_RUN=50`/`CONCURRENCY=6`) espalham a carga (FM-CAD-07). Tick sobreposto/retry **não** produz double-post: índice único parcial `(idempotency_key) WHERE status<>'failed'` + `ON CONFLICT DO NOTHING RETURNING` + `overlap_policy=skip` (FM-CAD-01).
> 69	
> 70	#### Edge Case 3: `budget_cap_mco` atingido no ciclo
> 71	> A cobrança acontece no **ciclo** (par `begin`/`finalize`, invariante G7 = quote==charge do ciclo, não do nó); atingir o `budget_cap_mco` (NOT NULL, em mcoCoins) yielda o ciclo sem estourar. O Usuário Zero já viu a magnitude no inspector antes de armar (ex.: plano diário 30d com X-post-com-link = **1.350 mco**).
> 72	
> 73	### Journey 2: Laço Inbound IG (comentário/DM) — **PROBE-GATED** (Fatia 2, hipótese até o probe fechar)
> 74	
> 75	> ⚠️ **Todo este journey é PROBE-GATED** (FM-CAD-02, RPN 486): sob Standard Access o webhook pode não entregar DM de terceiro sem role. Nasce `delivery:'gated'`; **zero FR de inbound no BoK antes do payload cru**. Não é capacidade prometida do roadmap até o probe fechar.
> 76	
> 77	| Stage | Action | Touchpoint | Emotion | Opportunity |
> 78	|-------|--------|-----------|---------|-------------|
> 79	| Awareness | Post publicado provoca comentário/DM de terceiro | `instagram-webhook` (`entry.changes` comentário \| `entry.messaging` DM) | 😐 Neutral | Reusa esqueleto do webhook (HMAC `timingSafeEqual` + `hub.challenge`), troca o sink |
> 80	| Consideration | Inbound vira `lead_events(message_received)` + `leads` + `notify()` → `social_threads`/`social_messages` | Ledger + sino | 🤔 Curious | Meta só devolve as 20 últimas msgs ⇒ histórico **tem** que morar em `social_threads` |
> 81	| Activation | Gate chain (janela in/out, opt-out, jurisdição, consent) roda **server-side** | `social_threads` (relógios `csw_expires_at` 24h × `private_reply_deadline` 7d) | 😊 Excited | Private reply 1× (≤7d, `UNIQUE(comment_id)`) ou resposta in-window (≤24h) |
> 82	| Value | Resposta com link afiliado + UTM → `creative_metrics` → `collective_efficiency_ledger` | Ledger de receita | 🚀 Delighted | Inbound alimenta o **mesmo** ledger que já mede receita (o fosso) |
> 83	| Retention | Reconciliação `sent` só do webhook de status (nunca do 202); kill-switch global por feedback negativo | `cadence_dispatches` + `infra_health_logs` | ❤️ Loyal | Custo externo BYOK registrado em `external_usd_cost` mesmo com mco=0 |
> 84	
> 85	#### Edge Case 1 (bloqueante): Inbox nasce vazio
> 86	> Se o DM real de terceiro sem role **não** aparecer no banco no probe, **App Review vira pré-requisito** e a Fatia 2 inteira está bloqueada (FM-CAD-02). O time não pode declarar "funciona" testando com a própria conta (role user).
> 87	
> 88	#### Edge Case 2: Cold DM / janela expirada
> 89	> Enfileirar DM para o futuro e a janela fechar = violação de política (ban do app, não erro HTTP). Estruturalmente impossível: a fila tem **FK NOT NULL** para um inbound (`lead_events.event_type='message_received'` do mesmo `user_id`); sem inbound, a linha não existe (G1/FM-CAD-03). Gate de janela **no send**.
> 90	
> 91	---
> 92	
> 93	## 4. Feature Inventory (MoSCoW)
> 94	
> 95	> Effort: S=hours, M=days, L=week, XL=sprint. `mcoCoins/run` = custo do **nó/ação**; a unidade de cobrança real é o **ciclo** (par `begin`/`finalize`) — criar plano custa 0 (G7 = invariante do ciclo, não do nó). Custo externo BYOK que o tenant absorve é **registrado** (`external_usd_cost`), mesmo com cobrança mco=0.
> 96	
> 97	### Must Have (MVP — Fatia 0 + Fatia 1)
> 98	
> 99	| ID | Feature | Persona | BR Traced | FR cand. | Effort | mcoCoins/run | Notes |
> 100	|----|---------|---------|-----------|----------|--------|-------------|-------|
> 101	| PR-CAD-001 | Nó `cadence` no Canvas Studio (categoria Publish), keyless, excluído do gate "runnable"; `resolveExecutePayload→null`, `estimateNodeCost→0` | P1, P2 | BR-CAD-001 | FR-CAD-001 | M | **0** | 6 edições de canvas (types/registry/node/nodeTypes/RightPanel/inspector); aliases pt-BR; não quebra `runAllCost` |
> 102	| PR-CAD-002 | Edge `cadence-plan` (upsert do plano + arm `next_run_at` UTC) + inspector com poll molde `useVoiceRenderPoll` | P1, P2 | BR-CAD-004 | FR-CAD-005 | M | 0 | Gate `Bearer SB_SECRET_KEY`→403; `user_id` server-trusted; poll sobrevive a refresh |
> 103	| PR-CAD-003 | Estender `autopilot_plans` (`plan_kind`, `recurrence jsonb`, `quiet_hours`, `overlap_policy`, `catchup_window`, `jitter_seconds`, `program jsonb`, `channel_allowlist`, `budget_cap_mco NOT NULL`; DROP CHECK `platforms`) + roteamento por `plan_kind` no tick vivo | P1, P2 | BR-CAD-002, BR-CAD-004 | FR-CAD-002, FR-CAD-004 | M | 0 | **Nenhum** job pg_cron novo; migration única em `/security-review`; RLS owner-scoped preservada (OTD-CAD-003) |
> 104	| PR-CAD-004 | Ledger `cadence_dispatches` (índice único parcial `(idempotency_key) WHERE status<>'failed'`; RLS select_own + insert/update service-role) | P1, P2 | BR-CAD-003 | FR-CAD-003 | M | 0 | Cliente nunca escreve; retry **libera** / sucesso **prende**; não append-only puro (OTD-CAD-006 §11) |
> 105	| PR-CAD-005 | Edge `cadence-run` (drain `FOR UPDATE SKIP LOCKED`, gate chain server-side, dispatch → `scheduled_posts`, ledger, re-arm) | P1, P2 | BR-CAD-009, BR-CAD-011, BR-CAD-013 | FR-CAD-006 | L | Custo do canal no dispatch | Nó **enfileira**, não publica; reconciliação `sent` só do webhook de status (FM-CAD-05) |
> 106	| PR-CAD-006 | Re-arm UTC generalizado `{frequency, days, hours, minutes, tz}` a partir de `autopilot-run:310-314` | P1, P2 | BR-CAD-005 | FR-CAD-007 | S | 0 | Cron **nunca** carrega preferência de horário; ressuscita `profiles.timezone` (FM-CAD-06) |
> 107	| PR-CAD-007 | Quiet-hours no fuso do sujeito (cascata `recurrence.tz→profiles.timezone→America/Sao_Paulo`) + frequency-cap **HALT** lendo `channel_profiles.cadence` | P1, P2 | BR-CAD-006 | FR-CAD-008 | M | 0 | 1º leitor de `channel_profiles.cadence` (teto autoritativo); HALT, não reenfileira (OTD-CAD-008/017) |
> 108	| PR-CAD-008 | Dedup/digest `(user, channel, dia)` colapsa N vencimentos em 1 publicação/carrossel | P1, P2 | BR-CAD-007 | FR-CAD-009 | M | 0 | Diferença entre cadência e flood |
> 109	| PR-CAD-009 | A/B determinístico `mod(abs(hashtext(subject‖:‖exp)::bigint),100) < ratio` (cast bigint **antes** do abs) | P1, P2 | BR-CAD-008 | FR-CAD-010 | S | 0 | Estável entre retries; nunca `% 100` sobre int com sinal (viés silencioso) |
> 110	| PR-CAD-010 | Inspector projeta **custo por ciclo em mco** antes de armar; `budget_cap_mco` NOT NULL em mcoCoins; BYOK fail-closed + `external_usd_cost`/`cost_source` no reconcile | P1, P2 | BR-CAD-010, BR-CAD-012 | FR-CAD-011, FR-CAD-014 | M | 0 (exibição) | Obrigação compensatória do quote=0; "não cobrar" ≠ "não medir" (OTD-CAD-011) |
> 111	| PR-CAD-011 | Guardrails de compliance **estruturais** (FK NOT NULL p/ inbound, UNIQUE(comment_id), opt-out no send, rodapé/disclosure IA server-side, caps NOT NULL, IoC anti-browser-automation) | P1, P2 | BR-CAD-014 | FR-CAD-012, FR-CAD-013 | L | 0 | 14 guardrails de §6, nunca via LLM; cold DM impossível de representar |
> 112	| PR-CAD-012 | **Fatia 0 (P0)**: `whatsapp-webhook` alcançável (`config.toml` `verify_jwt=false`) + `timingSafeEqual`; `estimateNodeCost` case `publishSocial`; `erase_lead()` cascata; `auto-publish` → pg_cron + `FOR UPDATE SKIP LOCKED` | P1, P2 | BR-CAD-017 | (Fatia 0) | M | 0 | Sem eles tudo é falso-sucesso (OTD-CAD-001/004/006/007) |
> 113	
> 114	### Should Have (v1.0 — Fatia 3, BYOK sem review de plataforma)
> 115	
> 116	| ID | Feature | Persona | BR Traced | FR cand. | Effort | mcoCoins/run | Notes |
> 117	|----|---------|---------|-----------|----------|--------|-------------|-------|
> 118	| PR-CAD-020 | Canal **Telegram** BYOK (bot token per-user no pool cifrado; opt-in estrutural via `/start`) | P2 | BR-CAD-016 | FR-CAD-014 | M | **0** (US$0 Meta-free) | Fail-closed `telegram_not_configured`; bot não fala com quem nunca deu `/start` |
> 119	| PR-CAD-021 | Canal **Email (Resend)** — flip do `nurture-dispatch` de `gated`→`sent` com rodapé/opt-out server-side (G10) | P2 | BR-CAD-016 | FR-CAD-014 | M | 0 (custo externo BYOK) | Domínio verificado do tenant + GO Sovereign; rodapé montado server-side, nunca no prompt (FM-CAD-12) |
> 120	
> 121	### Could Have (Future — Fatia 2 PROBE-GATED + Fatia 4 GATED)
> 122	
> 123	| ID | Feature | Persona | BR Traced | FR cand. | Effort | mcoCoins/run | Notes |
> 124	|----|---------|---------|-----------|----------|--------|-------------|-------|
> 125	| PR-CAD-030 | **Laço inbound IG** (comentário/DM → `lead_events`/`social_threads` → private reply ≤7d UNIQUE / resposta in-window ≤24h) | P1 | BR-CAD-015 | FR-CAD-012, FR-CAD-013 | XL | Variável (in-window US$0) | **PROBE-GATED** por FM-CAD-02 (RPN 486); nasce `delivery:'gated'`; prova de shape `entry.messaging` com payload cru (FM-CAD-13) |
> 126	| PR-CAD-031 | Canal **WhatsApp Cloud BYOK** (tenant traz app + WABA + número + pagamento) | P2 | BR-CAD-016 | — | XL | 0 mco (tenant paga Meta) | **GATED**: apagar conta WhatsApp do número; `422 whatsapp_opt_in_missing` fail-closed; HMAC por-tenant via `phone_number_id` (FM-CAD-09/15); enquadramento AI Provider Brasil bloqueia auto-reply (OTD-CAD-009) |
> 127	| PR-CAD-032 | Canal **X** na `channel_allowlist` (DM Create = 4 mco; **Post com URL = 45 mco**) | P2 | BR-CAD-012 | — | M | 4 / **45** mco | **GATED por OTD-CAD-011**: X FORA da allowlist da Fatia 1 até probe de créditos no Developer Console (conta pode estar sangrando agora — FM-CAD-10) |
> 128	| PR-CAD-033 | Canal **Messenger** (`pages_messaging`, Page access token) | P2 | BR-CAD-016 | — | XL | 0 mco (in-window) | **GATED**: outra integração (outro token/host/objeto de webhook) |
> 129	| PR-CAD-034 | **Instagram multi-tenant** (inbound para tenants terceiros) | P2 | BR-CAD-015 | — | XL | Variável | **GATED**: App Review + Business Verification; `ig_advanced_access_required` fail-closed (OTD-CAD-018) |
> 130	| PR-CAD-035 | **LinkedIn comment reply** (`socialActions/{urn}/comments`) | P2 | BR-CAD-016 | — | XL | 0 | **GATED**: Community Management API (revisão da LinkedIn) + reconexão OAuth |
> 131	
> 132	### Won't Have (This Cycle)
> 133	
> 134	- **Cold DM em qualquer canal** — proibido em toda plataforma verificada (§1/§4 do blueprint).
> 135	- **Broadcast/newsletter por DM no Instagram** — a Meta não oferece OTN/News/Sponsored no IG; impossível na plataforma (§4/§10.8).
> 136	- **SMS (Twilio BR)** — provisionamento de semanas (short code) + janela horária legal (09h–22h, sem domingo) — deferido (§7).
> 137	- **Discord DM de marketing** — a política da plataforma proíbe (§4/§10.13).
> 138	- **LinkedIn DM automatizada** — sem caminho legítimo ("Member actions do not include an automated or scheduled event") (§4/§10).
> 139	- **TikTok DM/comment** — hipótese não confirmada; **zero FR até probe autenticado** (OTD-CAD-013).
> 140	- **Marcação C2PA/machine-readable de conteúdo sintético (AI Act Art. 50(2))** — módulo próprio, maior que este (OTD-CAD-014, vigência 2026-08-02).
> 141	- **Carrossel dentro da cadência** — até fechar OTD-CAD-005 (retry duplica children, amplificado pela recorrência — FM-CAD-08).
> 142	
> 143	---
> 144	
> 145	## 5. Release Phasing
> 146	
> 147	### MVP Scope — Fatia 0 + Fatia 1 ("Cadência de Publicação", ZERO app review)
> 148	**Target date:** primeira release após a Fatia 0 (P0) fechada e verificada
> 149	**Included:** PR-CAD-012 (Fatia 0 P0) → PR-CAD-001..011 (nó, edges, motor, gates, custo, guardrails estruturais)
> 150	**Canais:** allowlist de `auto-publish` **MENOS X** (WordPress, LinkedIn, IG, TikTok, YouTube, Pinterest via seams existentes). **Nenhuma mensagem privada.**
> 151	**Success gate:** ≥1 plano `plan_kind='cadence'` ativo para o Usuário Zero (UUID real), armado com hora/weekday/timezone; **0** double-post sob tick sobreposto/retry (smoke re-executável); 100% dos `sent` do webhook de status; `profiles.timezone` e `channel_profiles.cadence` com ≥1 leitor cada; inspector projeta mco/ciclo; `/security-review` sem findings em toda migration.
> 152	
> 153	### v1.0 Scope — Fatia 3 ("Canais desimpedidos" BYOK)
> 154	**Target date:** após MVP estável + domínio Resend verificado + GO Sovereign
> 155	**Adds:** PR-CAD-020 (Telegram), PR-CAD-021 (Email Resend flip)
> 156	**Success gate:** Telegram fail-closed (`telegram_not_configured`); flip `nurture-dispatch`→`sent` só com rodapé/disclosure server-side (G10/G12) e GO Sovereign; custo externo BYOK registrado em `external_usd_cost`.
> 157	
> 158	### Future Scope — Fatia 2 (PROBE-GATED) + Fatia 4 (GATED)
> 159	**Items:** PR-CAD-030 (inbound IG), PR-CAD-031..035 (WhatsApp/X/Messenger/IG multi-tenant/LinkedIn comment)
> 160	**Condition:** cada item destrava por uma **provisão Sovereign** específica:
> 161	- PR-CAD-030: **DM real de terceiro sem role** aparece no banco + payload cru fixa `entry.messaging` (FM-CAD-02/13). Senão App Review vira pré-requisito.
> 162	- PR-CAD-032: probe de créditos no **X Developer Console** + confirmar Post-com-URL = US$0,200 (OTD-CAD-011).
> 163	- PR-CAD-031: consulta Meta sobre enquadramento **AI Provider Brasil** antes de flipar auto-reply para `sent` (OTD-CAD-009); revisão jurídica Tech Provider (OTD-CAD-010).
> 164	- PR-CAD-034: **App Review + Business Verification** (OTD-CAD-018).
> 165	
> 166	---
> 167	
> 168	## 6. Luxury UX Specifications
> 169	
> 170	> Marca MIV (rebrand): fundo `void`, acento `cyan` (dual-role bg+text), `gold` reservado a **valor/mcoCoins**, `nebula` a **memória**; CTA usa glow (nunca fill flat). Tokens abaixo espelham o MIV — o motor real é o Canvas Studio (ReactFlow), não uma tela nova.
> 171	
> 172	### 6.1 Color & Visual Identity
> 173	
> 174	| Token | Value | Usage |
> 175	|-------|-------|-------|
> 176	| `--bg-void` | `#0A0A0F` | Canvas background do Spaces |
> 177	| `--accent-cyan` | `#06B6D4` | Nó `cadence` ativo, handles, `next_run_at`, status de dispatch |
> 178	| `--gold` | `#F5C451` | **Custo projetado em mco** e `budget_cap_mco` (semântica de valor) |
> 179	| `--glass-surface` | `rgba(255,255,255,0.04)` | Card do inspector |
> 180	| `--border-subtle` | `rgba(255,255,255,0.08)` | Bordas de card |
> 181	| `--danger` | `#EF4444` | Kill-switch (`is_active=false`), fail-closed (402/422), quiet-hours HALT |
> 182	
> 183	### 6.2 Animation Guidelines
> 184	
> 185	| Element | Library | Duration | Easing |
> 186	|---------|---------|----------|--------|
> 187	| Entrada do nó no canvas | R3F / Framer Motion | 300ms | `easeInOut` |
> 188	| Status pulse do dispatch (queued/publishing) | CSS keyframes | 2s | `ease-in-out infinite` |
> 189	| Micro-interações do inspector | Framer Motion | 150ms | `easeOut` |
> 190	| Skeleton do poll (últimas N dispatches) | shimmer | — | — (nunca spinner) |
> 191	
> 192	### 6.3 Interaction Patterns
> 193	
> 194	- **Nó `cadence`:** único `<Handle>` target `input_asset` (id inline, molde `PublishSocialNode`); categoria Publish no registry; aliases pt-BR **cadência/agendar/recorrente/cron/calendário**.
> 195	- **Inspector:** exibe recurrence {frequency, days, hours, minutes, tz}, quiet-hours, `channel_allowlist`, `budget_cap_mco` e — **obrigatório** — o **custo projetado por ciclo em mco** (`Σ canal × ocorrências até cap`) em `--gold`, **antes** do botão Armar. Mostra `next_run_at` + últimas N dispatches (poll molde `useVoiceRenderPoll`, id no `data` do nó, sobrevive a refresh — **nunca** o loop `sleep(8s)×25`).
> 196	- **Toasts (`sonner`, pt-BR):** sucesso = cyan, erro = danger, info = cyan. Mensagens fail-closed pt-BR: `telegram_not_configured`, `whatsapp_opt_in_missing`, `ig_advanced_access_required`, `<provider>_not_configured` (402/501 estruturado com `action` de configuração).
> 197	- **Loading states:** skeleton shimmer para as dispatches; nunca spinner em área de conteúdo.
> 198	
> 199	### 6.4 Accessibility (WCAG 2.1 AA)
> 200	
> 201	- Contraste ≥ 4.5:1 para todo texto sobre glass (o custo em `--gold` deve passar o teste sobre `--bg-void`).
> 202	- Handles e botão Armar keyboard-navegáveis; foco visível ≥ 2px.
> 203	- ARIA labels nos botões icon-only do inspector (kill-switch, editar recurrence).
> 204	
> 205	---
> 206	
> 207	## 7. Acceptance Criteria (Gherkin)
> 208	
> 209	```gherkin
> 210	Feature: Cadência de Publicação (Fatia 1)
> 211	
> 212	  Scenario: Armar plano de cadência sobre asset existente (PR-CAD-001, PR-CAD-002, PR-CAD-003)
> 213	    Given um asset owner-scoped em creative_assets e um nó "cadence" no Canvas Studio
> 214	    When o Usuário Zero define recurrence {frequency:"weekly", days:[1,3,5], hours:9, minutes:0, tz:"America/Sao_Paulo"}, channel_allowlist e budget_cap_mco, e clica em Armar
> 215	    Then a edge cadence-plan faz upsert em autopilot_plans com plan_kind='cadence' e next_run_at computado em UTC
> 216	    And criar o plano custa 0 mco (nenhuma cobrança na criação)
> 217	    And o inspector exibiu o custo projetado por ciclo em mco antes do Armar
> 218	
> 219	  Scenario: Tick dispara no fuso correto sem double-post (PR-CAD-004, PR-CAD-005, PR-CAD-006)
> 220	    Given um plano cadence com next_run_at vencido
> 221	    When o tick autopilot-cadence-cron roteia por plan_kind='cadence' para cadence-run
> 222	    Then o drain usa FOR UPDATE SKIP LOCKED e enfileira em scheduled_posts (metadata.reshape + schedule:true + publish_at)
> 223	    And uma linha em cadence_dispatches é criada via INSERT ON CONFLICT DO NOTHING RETURNING sob o índice único parcial (idempotency_key) WHERE status<>'failed'
> 224	    And um tick sobreposto ou retry não cria um segundo dispatch para a mesma (plan_id, step_index, occurrence_at)
> 225	    And next_run_at é re-armado em UTC
> 226	
> 227	  Scenario: Quiet-hours e frequency cap fazem HALT (PR-CAD-007)
> 228	    Given um dispatch cujo horário cai em quiet-hours no fuso do sujeito OU cujo canal atingiu o teto de channel_profiles.cadence na janela
> 229	    When cadence-run avalia a gate chain server-side
> 230	    Then o dispatch é suprimido com HALT (não reenfileira)
> 231	    And nada é publicado
> 232	
> 233	  Scenario: Custo externo BYOK é medido mesmo com cobrança mco=0 (PR-CAD-010, PR-CAD-020)
> 234	    Given um dispatch por um canal BYOK (Telegram/Email/IG in-window)
> 235	    When o reconcile recebe o webhook de status
> 236	    Then external_usd_cost e cost_source são gravados em cadence_dispatches (nunca no 202)
> 237	    And a cobrança em mco é 0
> 238	    And o custo entra no collective_efficiency_ledger
> 239	
> 240	  Scenario: Reconciliação nunca reporta enviado a partir do 202 (PR-CAD-005)
> 241	    Given um dispatch despachado à API do canal
> 242	    When a API responde 202 (accepted) sem confirmação de entrega
> 243	    Then o status permanece diferente de 'sent'
> 244	    And 'sent' só é gravado ao chegar o webhook de status (Lei 1)
> 245	
> 246	  Scenario: Fatia 0 fechada antes de qualquer código de cadência (PR-CAD-012)
> 247	    Given o estado atual do repositório
> 248	    When a Fatia 0 é aplicada
> 249	    Then whatsapp-webhook responde não-401 (bloco [functions.whatsapp-webhook] verify_jwt=false em config.toml)
> 250	    And o HMAC usa timingSafeEqual (não ===)
> 251	    And estimateNodeCost tem case para publishSocial (runAllCost não vira NaN)
> 252	    And erase_lead() cancela agendamentos futuros em cascata na mesma transação
> 253	    And auto-publish roda em pg_cron com FOR UPDATE SKIP LOCKED
> 254	
> 255	Feature: Laço Inbound IG (Fatia 2 — PROBE-GATED)
> 256	
> 257	  Scenario: Probe FM-CAD-02 antes de qualquer FR de inbound (PR-CAD-030)
> 258	    Given o app Meta global do MCORCH em Standard Access
> 259	    When um terceiro SEM role no app envia um DM real para uma conta IG própria
> 260	    Then a linha aparece em lead_events(event_type='message_received') e o payload cru é arquivado
> 261	    And somente então o branch entry.messaging pode ser codado (shape fixado, FM-CAD-13)
> 262	    And se o DM não chegar, App Review vira pré-requisito e a Fatia 2 está bloqueada
> 263	
> 264	  Scenario: Cold DM é impossível de representar (PR-CAD-011, G1)
> 265	    Given a fila de DM com FK NOT NULL para um inbound do mesmo user_id
> 266	    When se tenta enfileirar um DM sem inbound correspondente
> 267	    Then a linha não pode existir (FK viola)
> 268	    And a resposta nasce delivery:'gated', flip para 'sent' só com GO Sovereign
> 269	```
> 270	
> 271	---
> 272	
> 273	## 8. Traceability Matrix
> 274	
> 275	| MR ID | BR ID | PR ID | FR cand. | OTD / FM |
> 276	|-------|-------|-------|----------|----------|
> 277	| MR-CAD-001 | BR-CAD-001, BR-CAD-004 | PR-CAD-001, PR-CAD-002 | FR-CAD-001, FR-CAD-005 | OTD-CAD-002, OTD-CAD-007 |
> 278	| MR-CAD-002 | BR-CAD-004, BR-CAD-005 | PR-CAD-003, PR-CAD-006 | FR-CAD-002, FR-CAD-007 | FM-CAD-06 |
> 279	| MR-CAD-003 | BR-CAD-006 | PR-CAD-007 | FR-CAD-008 | OTD-CAD-008, OTD-CAD-017 |
> 280	| MR-CAD-004 | BR-CAD-007 | PR-CAD-008 | FR-CAD-009 | — |
> 281	| MR-CAD-005 | BR-CAD-008 | PR-CAD-009 | FR-CAD-010 | OTD-CAD-016 |
> 282	| MR-CAD-006 | BR-CAD-003, BR-CAD-009 | PR-CAD-004, PR-CAD-005 | FR-CAD-003, FR-CAD-006 | FM-CAD-01, FM-CAD-07 |
> 283	| MR-CAD-007 | BR-CAD-010 | PR-CAD-010 | FR-CAD-011 | OTD-CAD-011 |
> 284	| MR-CAD-008 | BR-CAD-002, BR-CAD-004 | PR-CAD-003 | FR-CAD-002, FR-CAD-004 | OTD-CAD-003 |
> 285	| MR-CAD-009 | BR-CAD-011 | PR-CAD-005 | FR-CAD-006 | OTD-CAD-004, OTD-CAD-005 |
> 286	| MR-CAD-010 | BR-CAD-012, BR-CAD-013 | PR-CAD-010, PR-CAD-005 | FR-CAD-011, FR-CAD-014 | OTD-CAD-009, OTD-CAD-010 |
> 287	| MR-CAD-011 | BR-CAD-014, BR-CAD-013 | PR-CAD-011 | FR-CAD-012, FR-CAD-013 | FM-CAD-03/04/05/12/15 |
> 288	| MR-CAD-012 | BR-CAD-015 | PR-CAD-030, PR-CAD-034 | FR-CAD-012, FR-CAD-013 | FM-CAD-02 (RPN 486), FM-CAD-13, OTD-CAD-018 |
> 289	| MR-CAD-013 | BR-CAD-016 | PR-CAD-020, PR-CAD-021 | FR-CAD-014 | — |
> 290	| MR-CAD-014 | BR-CAD-017 | PR-CAD-012 | (Fatia 0) | OTD-CAD-001, OTD-CAD-004, OTD-CAD-006, OTD-CAD-007 |
> 291	| — (Fatia 4 GATED) | BR-CAD-012, BR-CAD-016 | PR-CAD-031, PR-CAD-032, PR-CAD-033, PR-CAD-035 | — | OTD-CAD-009/010/011/013/018, FM-CAD-09/10/11/14 |
> 292	
> 293	> **Decisões abertas (§11 do blueprint) que a FRD/SDD deve selar:** (1) sujeito da cadência — PRD assume **asset existente** (OTD-CAD-002); (2) estender `autopilot_plans` vs tabela nova — PRD assume **estender** (OTD-CAD-003); (3) `channel_profiles.cadence` **autoritativo** (OTD-CAD-008); (4) escopo de canal da Fatia 1 = **só publicação, X fora** (OTD-CAD-011); (5) jurisdição default = **UE fail-closed** (G11); (6) semântica `cadence_dispatches` = **retry via índice parcial** (OTD-CAD-006 §11); (7) IG/Messenger no app **global** com caps por-app (OTD-CAD-018). **A FRD sela a numeração `FR-CAD-xxx`** — aqui são candidatos rastreados; PR-CAD-xxx são itens de produto.
> 294	
> 295	---
> 296	
> 297	_Generated by MCORCH BoK Scribe Agent v1.0.0 — fiel a `00-deepsearch-blueprint.md` + `01-mrd.md` + `02-brd.md` (Lei 1: nenhum FR/OTD/FM/entidade inventado além do blueprint; §3 sob selo de não-verificação; TAM/ROI numérico marcado como não quantificado). Convenções MCORCH: lógica/vars em inglês, UI/toasts pt-BR; BYOK per-user fail-closed 402/501; cobrança via RPC atômica begin/finalize; verify_jwt=false → ES256 JWKS / HMAC timingSafeEqual; RLS default-deny owner-scoped; a Cadência ENCAIXA nos trilhos vivos (autopilot · sequences/nurture-dispatch · scheduled_posts), não reconstrói distribuição._
> 298	
> ```

## 🤖 Claude *(15:54:09)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-repurpose/10-frd-sdd-viral-quality.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# video-repurpose — Fatia "Viral Quality" (FRD + SDD de fatia)
> 2	
> 3	> **Tipo:** FRD/SDD por-fatia (o blueprint `00-deepsearch-blueprint.md` §8 manda "FRD/SDD de fatia antes das fatias pesadas"). Esta é a **Fatia 6 — Viral Quality**, além das 5 fatias do blueprint.
> 4	> **Status:** ✅ Autorada 2026-07-13 (Closed-Loop Step 3/3.5). **Abre o gate de código** para o motor de qualidade viral. Fecha o alerta de doc-gate (`video-repurpose` deixa de ser blueprint-only para esta capacidade).
> 5	> **Diretiva Sovereign 2026-07-13:** "templates sofisticados e sem botão… verifique se realmente precisa de legenda; se não, legendas pontuais grandes como motion-graphic… entender os melhores momentos dos cortes, envolver o Vision para calibrar para viralizar — foco 100% em viral."
> 6	> **ORO triplet:** Operator = MCORCH Master Execution Agent (loop autônomo) · Reviewer = `/security-review` por seam + **Vision ocular por criativo** (Lei 1) + Sovereign nos gates · Owner = Sovereign (alcance público gated na auditoria de app = ação dele; rail de render 100% grátis US$ 0; detector LLM metered per-user BYOK).
> 7	> **Traceabilidade:** destrava **FR-CP-012** (auto-segmentação 1→N) · fecha **OTD-VR-005** (fonte do cut-spec: Hormozi hook-detector) · herda **OTD-VR-002/006** · consome o sink `publish-space-asset`→`space_publish_variants` ([[project_lora_witness_and_otd_spaces_036]]).
> 8	
> 9	---
> 10	
> 11	## 1. Fundamentação material (Lei 1 — verificado neste turno)
> 12	
> 13	| Claim | Prova (file:line / veredito) |
> 14	|---|---|
> 15	| Legenda hoje = barra drawtext tradicional (embaixo) | ✅ `scripts/video-repurpose/segment-core.ts:71-82` (drawtext textfile, box preta, y=h-th-8%). **Vision QA 2026-07-13** no `clip_000`: "legendas em barra tradicional… não maximiza impacto no modo som-desligado". |
> 16	| Estilo premium desejado = motion-graphic palavra-por-palavra | ✅ **Vision QA** na referência `33bebbce` (asset `84aefb3a`): "tipografia grande em motion-graphic… palavra por palavra, animações suaves; NÃO legendas tradicionais". |
> 17	| "sem botão" = a própria referência tem CTA a remover | ✅ **Vision QA** na referência: "botão 'Ativar'… HUD com timer e frame-counter" (leak de dev) → **dropar** no template novo. |
> 18	| Motor motion-graphic já existe (rail separado) | ✅ `scripts/hyperframes/render-core.ts` (Playwright HTML→PNG bitexact) + `scripts/hyperframes/templates/cinematic-9x16.html` (kinético per-word, MIV). Roda em `engine='hyperframes'`, **desacoplado** do `engine='repurpose'`. |
> 19	| NÃO existe detector de momento viral | ✅ cut-spec é 100% caller-authored (`VideoRepurposePage.tsx:289`); zero scenedetect/scoring no repurpose. Único `viral_score` do repo é de **trends** (`fetch-trends`), não de vídeo. |
> 20	| Master carrega SRT inline | ✅ `ingest-external-asset/index.ts:143` grava `metadata.srt` (pt/en) — matéria-prima do detector, hoje **não lida** por ninguém. |
> 21	| composition é jsonb livre (sem migration p/ novos campos) | ✅ `video-repurpose-run/index.ts:114-116` monta `composition` jsonb; `video_renders.composition` é jsonb (`20260624120000`). Novos campos (`text_beats`) **não exigem migration**. |
> 22	| render-core faz screenshot PNG por frame | ✅ `render-core.ts` (`page.screenshot` `animations:'disabled'`, frame por índice). **Falta modo alpha** (`omitBackground:true`) → detalhe de implementação FR-VR-011. |
> 23	
> 24	**Lei-âncora (do blueprint §2):** "o gate 'olhe o render' (Vision QA) é obrigatório em cada clipe." Reforçado: **nunca fabricar frase de legenda** — o texto na tela deriva do SRT falado (Lei 1); o LLM SELECIONA/APARA, não INVENTA citação.
> 25	
> 26	---
> 27	
> 28	## 2. FRD — Requisitos funcionais (continuam a numeração do blueprint FR-VR-001..009)
> 29	
> 30	| FR | Requisito | Critério de aceite material |
> 31	|---|---|---|
> 32	| **FR-VR-010** | **Detector de momento viral** (`detect-viral-moments` edge fn): lê `metadata.srt` do master owner-scoped → segmenta em janelas → pontua cada janela por potencial viral (framework Hormozi: hook/retenção/recompensa + auto-suficiência sem contexto) via LLM **per-user BYOK fail-closed** → retorna cut-spec ranqueado `{in_sec,out_sec,hook_phrase,score,reason,text_beats[]}` e **auto-seleciona top-N** (default 3). | JWT válido; sem SRT → `422 no_transcript`; sem chave LLM → `402 <provider>_not_configured`; retorna ≥1 candidato ranqueado com `score∈[0,1]` e `in_sec<out_sec`; observação na malha. |
> 33	| **FR-VR-011** | **Compositing motion-graphic** no `segment-core`: render-core em **modo alpha** produz PNG-seq transparente dos `text_beats[]` → FFmpeg `overlay` pts-sync sobre o clipe reenquadrado. Substitui a barra drawtext como caminho premium (drawtext vira fallback FR-VR-014). | 1 clipe com ≥1 text-beat → MP4 9:16 com texto grande animado sobre o footage, **Vision QA confirma "motion-graphic, não barra"**; determinismo preservado (PNG bitexact + overlay puro). |
> 34	| **FR-VR-012** | **Template sofisticado "sem botão"** `viral-caption-overlay-9x16.html`: fundo **transparente**, tipografia MIV kinética **palavra-por-palavra** (void/cyan/gold, Playfair/JetBrains), reveal blur→sharp + glow; **sem CTA/pílula, sem HUD/frame-counter**. Texto via `textContent` (XSS-safe). | Render alpha do template → PNG com canal alpha (fundo transparente); Vision QA: "texto grande motion-graphic, sem botão, sem HUD". |
> 35	| **FR-VR-013** | **Loop Vision-gated de qualidade**: cada short gerado é pontuado pelo Vision (rubrica viral: hook 2s, legibilidade som-off, ritmo, reenquadre) antes de "pronto"; abaixo do limiar → itera (ajusta beats/janela), **cap de iterações** (anti-runaway). | Report material com `vision_score` por short; short final ≥ limiar OU cap atingido com motivo registrado. |
> 36	| **FR-VR-014** | **Decisão legenda-vs-motion por clipe**: clipes com fala densa/sem frase-gancho forte mantêm legenda (drawtext) OU karaokê leve; clipes com hook claro usam text-beats pontuais grandes. Default = pontual motion-graphic (diretiva Sovereign). | Cada clipe declara `caption_mode ∈ {beats, drawtext, none}`; escolha registrada no manifest. |
> 37	| **FR-VR-015** | **UI "Gerar cortes virais" (Diretiva 2026-07-13)**: 1 clique no front-door admin roda ingest(se preciso)→detector→enqueue beats-clips, com **barra de progresso + tail de log de linha única** durante todo o run (~15 min). Progresso ancorado em sinais REAIS: resposta do detector → estado `video_renders` (queued/running/done) → contagem de filhos `creative_assets` registrados por clipe (nunca % fabricado — Lei 1). | Botão em `/dashboard/repurpose`; barra avança por evento material; log mostra o último estágio; done → toast + Resultados. |
> 38	
> 39	---
> 40	
> 41	## 3. SDD — Arquitetura de implementação
> 42	
> 43	### 3.1 Fluxo (fundido nos dois rails existentes)
> 44	```
> 45	master (creative_assets source_module=external, metadata.srt)
> 46	  → detect-viral-moments (edge fn, JWT, per-user LLM BYOK)     [FR-VR-010]
> 47	      SRT → janelas → Hormozi scoring → top-N cut-spec {in,out,hook_phrase,text_beats[]}
> 48	  → video-repurpose-run (valida + enfileira, JÁ EXISTE)         [composition += text_beats]
> 49	  → video-repurpose-bridge worker (engine='repurpose')
> 50	      → segment-core:
> 51	          (a) trim -ss/-t + reframe 16:9→9:16 center-safe (JÁ EXISTE)
> 52	          (b) render-core ALPHA(viral-caption-overlay-9x16, text_beats) → PNG-seq transparente  [FR-VR-011/012]
> 53	          (c) FFmpeg overlay PNG-seq sobre o clipe reenquadrado (pts-sync)
> 54	      → upload + register_creative_asset (parent=master, JÁ EXISTE)
> 55	  → Vision QA loop (rubrica viral) → score/iterate                [FR-VR-013]
> 56	  → sink publish-space-asset → space_publish_variants (JÁ EXISTE, reuso puro)
> 57	```
> 58	
> 59	### 3.2 `composition` jsonb — extensão (sem migration; jsonb livre)
> 60	```ts
> 61	interface ClipSpec {
> 62	  in_sec: number; out_sec: number; reframe: "9:16" | "1:1";
> 63	  caption?: string;                       // legado (drawtext fallback)
> 64	  caption_mode?: "beats" | "drawtext" | "none";   // FR-VR-014, default "beats"
> 65	  text_beats?: Array<{                    // FR-VR-011 — legendas pontuais grandes
> 66	    t_start: number; t_end: number;       // relativo ao clipe (0 = início do corte)
> 67	    phrase: string;                       // DERIVADA do SRT (Lei 1 — não inventada)
> 68	    emphasis?: "hook" | "punch" | "normal";
> 69	  }>;
> 70	}
> 71	```
> 72	Guarda: `text_beats` validado no `video-repurpose-run` (≤12 beats/clipe, `phrase ≤120 chars`, `0 ≤ t_start < t_end ≤ (out-in)`), espelhando a sanitização existente (`video-repurpose-run:28-40`).
> 73	
> 74	### 3.3 render-core — modo alpha (novo)
> 75	- Adicionar `renderCompositionAlpha(spec, outDir)` OU flag `spec.alpha=true`: `page.screenshot({ omitBackground: true })` + template com `html,body{background:transparent}` → PNG-seq com canal alpha em `outDir/frame_%05d.png`. Mantém determinismo (índice-driven, `animations:'disabled'`, flags srgb). **Não** encoda MP4 — devolve o dir de PNGs (o segment-core faz o overlay).
> 76	- Gate Lei 1 herdado: ≥1 frame e cada PNG > 0 bytes.
> 77	
> 78	### 3.4 segment-core — overlay (novo branch)
> 79	- Se `clip.caption_mode==='beats'` e `text_beats?.length`: computa `fps`, chama render-core alpha (duração = out-in, mesmos fps), depois:
> 80	  ```
> 81	  ffmpeg -i <reframed_clip.mp4> -framerate <fps> -i <alpha>/frame_%05d.png \
> 82	    -filter_complex "[0][1]overlay=0:0:format=auto:eof_action=pass" \
> 83	    -c:a copy -pix_fmt yuv420p <out.mp4>
> 84	  ```
> 85	  (footage full-frame por baixo; texto animado por cima). PNG-count = fps×dur (casa com o clipe).
> 86	  **Anticorpo (bug 2026-07-13):** `-ss`+`-t` do master são opções de **INPUT 0** e DEVEM preceder o `-i` dele; num comando multi-input, `-t` depois do `-i` liga ao **próximo** input (os PNGs) e o master roda até o EOF → output de ~500s / 300MB / encode de 43min (pego por ffprobe do tamanho, não pelo "6s" reportado). `eof_action=pass` fica inócuo quando os dois inputs têm a mesma duração.
> 87	- Se `drawtext` → caminho legado atual (`:71-82`). Se `none` → sem texto.
> 88	- **Anti-XSS**: `phrase` chega ao template só via `textContent` (render-core já garante).
> 89	
> 90	### 3.5 detect-viral-moments — edge fn (novo)
> 91	- JWT obrigatório; resolve master owner-scoped (`.eq id .eq user_id`, molde `video-repurpose-run:96-98`); lê `metadata.srt`.
> 92	- LLM **per-user** (API Tenancy Model): `user_api_keys` → `<provider>` (openrouter/gemini/groq) fail-closed 402; **sem** `Deno.env.get` user-facing. Prompt Hormozi (hook/retain/reward + standalone). Saída JSON estrita (score, reason, hook_phrase, text_beats derivados do SRT). Débito mcoCoins atômico (calibração 4×-floor) via `deduct_mco_coins`.
> 93	- Telemetria `infra_health_logs` `service='detect-viral-moments'` (success/degraded/error). Observação na malha (padrão 8).
> 94	- **NÃO** enfileira render — devolve cut-spec p/ o cliente/`video-repurpose-run` (separação de responsabilidades, como `ingest-external-asset`).
> 95	
> 96	### 3.6 Vision QA loop (FR-VR-013)
> 97	- Reusa `scripts/qa/vision-qa.ts` (`vision_analyze_video`, custo 0 User Zero). Rubrica: hook-2s / legibilidade-som-off / ritmo / reenquadre-sem-corte-de-sujeito. Cap `MAX_VIRAL_ITERS=2` (anti-runaway, custo). Score < limiar → registra motivo e ajusta (ex.: encurtar janela, promover beat a "hook"). Determinístico o suficiente p/ ser re-executável.
> 98	
> 99	### 3.7 O que é REUSO puro (não reconstruir — blueprint §Tese)
> 100	`video-repurpose-run` (enqueue+guards), `video-repurpose-bridge` (claim/heartbeat/finalize/OTD-VR-006 read-guard), `register_creative_asset`, reframe center-safe, `render-core` (motor bitexact), o sink `publish-space-asset`. Disclosure sintética hard-coded (is_aigc/SELF_ONLY) **preservada**.
> 101	
> 102	---
> 103	
> 104	## 4. Pattern Conformance Declaration (21 padrões — `docs/architecture/agentic-vision.md`)
> 105	
> 106	| # | Pattern | Implemented? | How / Why-deferred |
> 107	|---|---------|:---:|---|
> 108	| 1 | Prompt Chaining | yes | detector→enqueue→segment→overlay→Vision-QA encadeados (cut-spec é o contrato entre steps). |
> 109	| 2 | Routing | yes | LLM do detector via cascata per-user (openrouter→…); Vision-QA como gate de dispatch (itera vs. aprova). |
> 110	| 3 | Parallelization | yes | Vision-QA dos N shorts em paralelo (Workflow `parallel()`); render-core dos beats concorrente por clipe. |
> 111	| 4 | Reflection | yes | **Generator-Critic explícito**: gera short → Vision critica (rubrica viral) → itera (FR-VR-013). É o coração da fatia. |
> 112	| 5 | Tool Use | yes | Vision MCP (`vision_analyze_video`), FFmpeg (overlay/reframe), render-core (HTML→PNG alpha). |
> 113	| 6 | Planning | yes | cut-spec ranqueado = plano de produção; top-N select antes de renderizar. |
> 114	| 7 | Multi-Agent | deferred | subagentes de loop (creative-director/Vision) coordenados pelo main; sem protocolo A2A formal — sem benefício neste escopo. |
> 115	| 8 | Memory Management | yes | observação na malha por run (detector + cada short); consome SRT do asset. |
> 116	| 9 | Learning & Adaptation | deferred | **OTD-VR-008b**: métricas de creative (hook_rate/retenção reais) → melhores cut-specs é loop futuro (espelha o padrão 9 `deferred` do MCORCH). Sem RL agora = evita reward de métrica única (Goodhart). |
> 117	| 10 | Model Context Protocol | yes | Vision QA via Vision MCP público (spec Anthropic). |
> 118	| 11 | Goal Setting & Monitoring | yes | goal = `vision_score ≥ limiar`; monitor = report material + `infra_health_logs`. |
> 119	| 12 | Exception Handling & Recovery | yes | detector 402/422 fail-closed; overlay falha → fallback drawtext (FR-VR-014); worker heartbeat/reaper herdado; cap de iterações. |
> 120	| 13 | Human-in-the-Loop | yes | auto-seleção top-N **com veto do Sovereign** (ORO); GO nos gates materiais. |
> 121	| 14 | Knowledge Retrieval (RAG) | n-a | fatia não recupera da malha p/ decidir corte (fonte = SRT do próprio master). |
> 122	| 15 | Inter-Agent Comm. (A2A) | n-a | sem troca inter-agente formal nesta fatia. |
> 123	| 16 | Resource-Aware Optimization | yes | render/overlay rail **grátis** (charged 0); detector LLM metered per-user (4×-floor, `deduct_mco_coins`); cap de iterações Vision (teto de custo). |
> 124	| 17 | Reasoning Techniques | yes | scoring Hormozi (hook/retain/reward + standalone) sobre o SRT = raciocínio estruturado do detector. |
> 125	| 18 | Guardrails / Safety | yes | **Lei 1: nunca fabricar frase** (beats derivam do SRT); per-user BYOK fail-closed (API Tenancy); OTD-VR-006 read-guard herdado; disclosure sintética preservada; XSS-safe `textContent`; `/security-review` por seam. |
> 126	| 19 | Evaluation & Monitoring | yes | rubrica Vision viral (score multi-dimensão) = eval por criativo; re-executável. |
> 127	| 20 | Prioritization | yes | ranquear janelas + top-N select = priorização explícita dos melhores momentos. |
> 128	| 21 | Exploration & Discovery | yes | detector explora o espaço de janelas do master (candidatos > selecionados); descobre hooks não-óbvios no SRT. |
> 129	
> 130	**Deferidos com justificativa material:** 7 (sem A2A neste escopo), 9 (loop de métricas→cut-spec = fatia futura, anti-Goodhart), 14/15 (n-a). Nenhum "deferido por preguiça".
> 131	
> 132	---
> 133	
> 134	## 5. OTD / FMEA (continuam do blueprint OTD-VR-001..007)
> 135	
> 136	| OTD | Débito | SLA/Decisão |
> 137	|---|---|---|
> 138	| **OTD-VR-008** | Fonte do text-beat: SRT verbatim vs LLM-rewrite. **Decisão:** derivar do SRT (Lei 1); LLM só seleciona/apara/timeia. Rewrite "punchy" = fatia futura gated (risco de citação inventada). | Fechado por decisão |
> 139	| **OTD-VR-009** | Determinismo do overlay: PNG-seq alpha + FFmpeg `overlay` pts-sync. Spec em §3.4; smoke deve provar count PNG = fps×dur. | Aberto (prova no smoke) |
> 140	| **OTD-VR-008b** | Loop métricas de creative → melhores cut-specs (padrão 9). | Deferido pós-1ª-métrica-real |
> 141	| **OTD-VR-010** | Custo do detector LLM + iterações Vision. Cap `MAX_VIRAL_ITERS=2`; detector metered per-user; surface do custo. | Aberto (calibrar 4×-floor) |
> 142	| **OTD-VR-012** | **Transcript-gate do detector.** ~~ASR vs user-SRT~~ **RESOLVIDO 2026-07-13 (Sovereign):** via **SRT fornecido pelo usuário** — Sovereign subiu `video-studio/GabrielAI/legendas/ep0{2,3,4}-{pt-BR,en}.srt` (SRTs reais timed, 58+ cues, 6,5min). ASR self-host (whisper.cpp) fica como opção futura p/ masters sem SRT, não bloqueia. **Novo gap (pareamento):** footage no disco = **EP01** (sem SRT); SRTs = ep02/03/04 (sem footage). Full-E2E precisa de 1 par casado (footage+SRT do mesmo episódio) — pedido ao Sovereign. Ingest precisa aceitar SRT-file no upload (hoje `metadata.srt` só via API). | ~~Aberto~~ Resolvido (user-SRT); pareamento pendente |
> 143	| **OTD-VR-013** | **Tuning de janela do detector (prova ep02 2026-07-13):** o LLM devolveu janelas **curtas demais** (2–6s, = 1 cue) apesar do "ideal 12-45s"; e às vezes o beat de punch cai **fora** de [in,out] (o fn corretamente o descarta, mas o clipe perde o punch). **Fix:** endurecer o prompt (janela 15–45s obrigatória, agrupar cues consecutivas numa micro-história; in/out DEVE conter os beats escolhidos) + no build, EXPANDIR [in,out] para conter os beats selecionados (clamp aos limites das cues). | Aberto — refino de prompt/build |
> 144	| herda **OTD-VR-002** | reframe subject-aware (crop dinâmico) diferido; MVP center-safe (Vision confirmou OK no `clip_000`). | Deferido |
> 145	| herda **OTD-VR-006** | worker re-valida `(bucket,key)` no READ (allowlist + prefixo `${uid}/` + no `..`). | Fechado (Fatia 2) |
> 146	
> 147	| FM | Vetor | Mitigação |
> 148	|---|---|---|
> 149	| FM-VR-Q1 | Beat fabricado (citação que o vídeo não fala) | beats derivam do SRT; guard de origem; Vision confere no loop |
> 150	| FM-VR-Q2 | Overlay dessincronizado (texto fora do tempo da fala) | pts-sync fps×dur; smoke de contagem; Vision confere |
> 151	| FM-VR-Q3 | Runaway de iterações Vision (custo) | `MAX_VIRAL_ITERS=2` + motivo registrado |
> 152	| FM-VR-Q4 | Cross-tenant no detector (SRT de outro user) | resolve master owner-scoped `.eq user_id`; per-user LLM key |
> 153	| FM-VR-Q5 | Template com fundo opaco → overlay tampa o footage | template `background:transparent` + `omitBackground:true`; smoke checa alpha |
> 154	
> 155	---
> 156	
> 157	## 6. Gates da fatia (parar no gate natural)
> 158	1. **Este doc** (FRD/SDD + Pattern Conformance) — fecha Closed-Loop 3.5. ✅
> 159	2. Template `viral-caption-overlay-9x16.html` + render-core modo alpha → **1 PNG-seq alpha inspecionado** (magic bytes RGBA).
> 160	3. `detect-viral-moments` edge fn + `/security-review` → **top-N cut-spec real do EP01 SRT**.
> 161	4. segment-core overlay branch → **1 short com motion-graphic VISTO pelo Vision** (score ≥ limiar).
> 162	5. E2E: EP01 master → detector → N shorts motion-graphic → Vision before/after nos 5 → sink. `/security-review` em toda edge fn/migration.
> 163	
> 164	**Cross-links:** [[project_video_repurpose_engine]] · [[project_creative_ecosystem_program]] · blueprint §8 · post-engine FR-CP-012.
> 165	
> ```

## 🤖 Claude *(15:54:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n -i \"video-repurpose\\|repurpose\" /home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md | head -60",
  "description": "Grep HANDOFF.md for video-repurpose slug"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 19:| **YouTube Fatia 2 + débito eslint ZERADO + roadmap não-gated + branding OAuth Google (2026-07-14)** | ✅ Sessão-maratona pós-v6.100.0 (loop autônomo GO'd + Sovereign ao vivo na verificação Google). **(A) Roadmap não-gated drenado:** carrossel IG pelo caminho AGENDADO (Amendment 22, fecha OTD-SPACES-044 — marcador de grupo `carousel_render_id` resolvido owner-scoped, FMEA-011 por construção; smoke 9/9) · reframe server-side no publish (Amendment 23, fecha OTD-SPACES-043 imagem — motor `reframeToJpeg` extraído p/ `supabase/functions/_shared/reframe.ts`, px do seed channel_profiles, fail-open; smoke 8/8 geometria 1080×1350 por decode SOF real) · trilhos de mídia LinkedIn imagem + IG Stories + X media (Amendment 24, FR-SPACES-082..085) + hardening `supabase/functions/_shared/public-url.ts` `assertPublicHttpUrl` (fecha classe SSRF pré-existente nos 5 fetch de mídia caller-controlada) · UI dos trilhos (toggle reframe no AssetDetailDialog + "Agendar carrossel" no VideoRepurposePage). **(B) Débito eslint ZERADO 448→0** (`bun run lint` exit 0; 26 warnings restantes): fan-out 1-agente-por-arquivo (122 arqs) types-only, tipos reais (Tables<>, interfaces por SELECT, catch narrowing, remoção de casts `as any` supérfluos), tsc+test verdes por lote, 6 commits + ignore de vendored/worktrees. **(C) YouTube Studio Fatia 2** (Amendment 12): editar (videos.update) + excluir permanentemente (videos.delete) vídeo via `force-ssl` + receita (revenue_metrics) via `yt-analytics-monetary.readonly` → os **4 escopos ficam demonstráveis** p/ a verificação Google (não aprova uso futuro); `social-auth-init` +escopo monetário; UI card Receita + Editar/Excluir por vídeo gated; smoke 9/9 fail-closed sem tocar canal; `/security-review` NO FINDINGS. **(D) Branding OAuth Google FIXADO** (marca verificada ✅): home era iframe-only (DOM do pai vazio) → verificador sem-JS não via nome/info → home crawlável login-free (HTML estático no `#root` do index.html + header React visível "MCORCH" + descrição + links Entrar/Privacidade/Termos; provado por curl do HTML cru servido). **21 commits** `1c59da5..08f49c5` · 2 `/security-review` NO FINDINGS · smokes 9/9+8/8+9/9 · guard-sweep +2 anticorpos · malha **9108** · nó `5f75a568`. |
> 23:| **Motor Viral Quality + ASR self-host + pool multi-key BYOK (2026-07-14)** | ✅ sessão-maratona interativa (Sovereign testando ao vivo, GO'ing deploys). **(1) Motor Viral Quality** (video-repurpose, BoK `10-frd-sdd-viral-quality.md` selada c/ Pattern Conformance): detector `detect-viral-moments` (Hormozi sobre o SRT, janelas 15-45s, `text_beats` = cues VERBATIM, LLM só escolhe índices — zero fabricação Lei 1, JSON-mode + parse defensivo) + overlay motion-graphic (`viral-caption-overlay-9x16.html` Montserrat premium sem botão + `renderAlphaFrames` RGBA + FFmpeg overlay sobre footage reenquadrado; anticorpo do `-t` multi-input). UI "Gerar cortes virais" 1-clique (barra ancorada em sinais reais) + botão Distribuir (`publish-space-asset`) + badge SRT. **3 shorts EP01 provados E2E em prod** (abertura 9.0/finale 9.5/conspiração 8.5, Vision 7-8/10). **(2) ASR self-host** whisper.cpp US$0 + reconciliação roteiro-autoritativa (o áudio da IA erra nomes: Austin→Boston Dynamics; roteiro do GitHub GabrielAI via MCP é a verdade). **(3) Rota host-media** streaming Range (206 seek) — master 1,3GB abre na biblioteca; infra host versionada. **(4) Pool multi-key BYOK** (Amendment 20): `user_provider_keys` Vault-cifrada + `resolveProviderKey` (explícita→prioridade→legado→402) + Settings card + seletor Spaces — 3 Gmails × créditos free-tier. **6 commits** `d4972c7..23f6e65` · `/security-review` **NO FINDINGS ×4** · malha **9105** · nó `d98767ea`. **Gated Sovereign:** aplicar migration `user_provider_keys` + deploy `canvas-execute` + cadastrar 3 chaves + aprovar cadência. |
> 25:| **YouTube Studio (Fatia 1) + front-door host-local do Repurpose (2026-07-13)** | ✅ sessão interativa "colocar a ferramenta pra funcionar" (Usuário Zero). **(1) Painel YouTube** `/dashboard/youtube` — edge fn `youtube-data` lê vídeos+métricas (Data v3 + Analytics v2) com token per-user de `social_accounts` server-side; escopos alinhados aos 3 registrados no Google (analytics adiado até habilitar a YouTube Analytics API); mapa exaustivo da API (`docs/bok/youtube-studio/11-api-surface-map.md`: 13 recursos·175 props·52 métricas·33 ações + Pattern Conformance 21 padrões) + SOP. **(2) Front-door host-local do Repurpose (admin-only)** `/dashboard/repurpose` — o Sovereign sobe o master pela UI e gera cortes; cap de 50MB do Supabase free → master (1,3GB) vai pro **disco do host** via `host-upload-server` (loopback 3220 atrás de nginx `/api/host-upload`, **upload chunked** 80MB/pedaço furando o cap de 100MB do CF, JWT+admin-gate, streaming); `ingest-external-asset` +sign_upload +provider `local` ADMIN-ONLY; `video-repurpose-run` +source `local` ADMIN-ONLY; worker lê `bucket=local` realpath-contido **sem copiar 1,3GB**. yt-dlp do host CONFIRMADO bloqueado pelo YouTube (bot-check). **(3)** fix legenda drawtext (truncagem por bytes-extra UTF-8 → padding). **EP01 real 1,3GB → 5 shorts 9:16** (1080×1920) provados por Vision QA (reframe centralizado + legenda completa). 5 commits `e174988..f10fba4` (+README `adcab9a`) · `/security-review` **NO FINDINGS ×3** · malha **9102** · nó `9f7b191a` |
> 26:| **Motor de repurpose de vídeo — Fatias 1-3 (1 master → N shorts + carrossel IG) + OTD-SPACES-036 + witness LoRA (2026-07-12)** | ✅ sessão-maratona interativa (Sovereign aplicou 3 migrations ao vivo + testou cada gate). **A metade que faltava: o MCORCH agora PRODUZ cortes, não só distribui.** BoK-first (Closed-Loop): blueprint `docs/bok/video-repurpose/00-deepsearch-blueprint.md` fundamentado em 10 pointers verificados file:line + no mapa do pipeline validado do repo `gabrielZarattini/GabrielAI` (o INVERSO — N takes Veo→1 master; fonte do master + schema de metadados `episodios/epNN.json` + filosofia cut-spec data-driven). **Correções ao snapshot:** segmenter é **FR-CP-012** (não OTD-CP-011; SDD já o gateava em "quando entrar INPUT de vídeo longo" → esta capacidade é o gatilho); OTD-CP-009 FECHADA (imagem, vídeo é gap); youtube Pilar I=montagem (concat), segmentação=inverso; carrossel existente=PDF/LinkedIn (IG image-children=gap, contrato Meta confirmado). **(Fatia 1 VIVA)** `source_module='external'` no spine `creative_assets` (migration aditiva aplicada) + seam `ingest-external-asset` (owner-scoped `${uid}/` + bucket allowlist + no-`..`; upload MP4 + metadados episódio + SRT inline; YouTube gated OTD-VR-001) · smoke 5/5 · `/security-review` NO FINDINGS. **(Fatia 2 VIVA E2E)** worker host `video-repurpose-bridge` (fila `video_renders` engine `repurpose` aditivo, rail FFmpeg **grátis** charged 0) → `segment-core` (trim `-ss/-t` frame-accurate + reframe 16:9→9:16/1:1 center-safe expression-crop + legenda queimada drawtext-textfile) · guarda **OTD-VR-006** re-valida source no READ (o controle decisivo tenant-safe) · **provado E2E na produção**: master→3 clipes reais (Vision QA: CENTRO preservado, ESQ/DIR cortados, **timestamp 00:00:04.000 prova o trim**, legenda queimada) · `/security-review` NO FINDINGS. **(Fatia 3 E2E provada)** `carousel-core` (key-frames dos capítulos → slides 1080×1350 4:5 + legenda wrapped + handle; **OTD-VR-007** wrap conservador, legendas curtas limpas, pixel-perfect via render-core diferido) + worker branch `mode='carousel'` + enqueue `slides[{t_sec,caption}]`≤10 + branch **media_type=CAROUSEL** no `publish-social` (contrato Meta) + seam `publish-space-carousel` (resolve slides owner-scoped→assina→publica) · **provado E2E**: master→3 slides 1080×1350 image assets + Vision QA no slide real · `/security-review` NO FINDINGS. **Distribuição reusada (não reconstruída):** cortes/slides nascem `creative_assets` que o nó **"Publicar em Rede Social"** (`publish-space-asset`/`space_publish_variants` — **OTD-SPACES-036** decisão (b) landada nesta sessão: tabela dedicada owner-scoped, money-path intocado, migration aplicada + smoke) já consome. **Witness LoRA:** treino real→402 Insufficient credit na conta Replicate BYOK do User 0 (plumbing 100% provado até o passo pago; bloqueado só em crédito — não código; inferência-com-LoRA é fatia futura inexistente). **Gates externos honestos:** publish real na IG/TikTok gated na auditoria de app (ação Sovereign). 6 commits `ac5ca86..831f5cc` · 3 migrations aplicadas · rail 100% grátis US$ 0 · Malha **9097** · nó `f050959c` |
> 222:Sessão que **completou a metade que faltava do repurpose** (o MCORCH agora ELEGE e VESTE os momentos, não só corta) e destravou a **mineração de vídeo a custo ~US$ 0**. A cadeia produzir→distribuir fechou de ponta a ponta: master → ASR/roteiro → detector → shorts motion-graphic → botão Distribuir → fila. Vários bugs viraram anticorpos: o `-t` do FFmpeg multi-input (302MB/43min → ffprobe pegou), o JSON malformado da cascata LLM (guard estornou os mco), a fonte com `-webkit-text-stroke` grosso "comendo" as letras (paint-order fix), e o cron `sync_sessions.sh` empilhando sem flock (estrangulava o whisper).
> 228:| `segment-core` branch beats + `video-repurpose-run` wire-through | ✅ `caption_mode`/`text_beats` validados e fiados até o worker |
> 229:| UI `VideoRepurposePage` (Gerar cortes + Distribuir + badge SRT) | ✅ 1-clique com barra real; distribui via `publish-space-asset` |
> 236:| `d4972c7` | feat(video-repurpose): motor Viral Quality — detector + overlay motion-graphic |
> 237:| `67dc54d` | feat(video-repurpose): ASR self-host + reconciliação roteiro-autoritativa |
> 238:| `955117d` | feat(repurpose): rota host-media (Range) + infra host versionada |
> 247:  → video-repurpose-run (valida beats) → worker → segment-core (reframe 9:16 + renderAlphaFrames overlay)
> 255:## YouTube Studio (Fatia 1) + front-door host-local do Repurpose Record (2026-07-13)
> 259:Sessão que **colocou a ferramenta para funcionar** com o Usuário Zero, resolvendo bloqueios reais ao vivo: (1) o **painel completo da API do YouTube** que o Sovereign pediu; (2) o **front-door do repurpose** que transformou o **EP01 real (1,3 GB)** em 5 shorts 9:16. Dois caps de plataforma furados: o de **50 MB do Supabase free** (solução: master no disco do host — `yt-dlp` do host **confirmado bloqueado** pelo YouTube por bot-check no IP de datacenter, então upload direto via UI) e o de **100 MB por request do Cloudflare** (upload **chunked** de 80 MB). Vision QA em mídia real pegou uma **legenda truncada** (bug drawtext UTF-8) — reproduzido, corrigido com padding, e re-provado no corte real.
> 264:| Front-door host-local (admin-only) | ✅ `/dashboard/repurpose` — dropzone chunked (80MB) → `host-upload-server` (3220, nginx `/api/host-upload`, JWT `admin.auth.getUser` + admin-gate `user_roles`, streaming) → worker lê `bucket=local` realpath-contido. yt-dlp bloqueado confirmado por probe |
> 271:| `9f561c0` | feat(video-repurpose): front-door host-local (drag-drop + ingest/worker fonte local admin-only) |
> 272:| `681002f` | fix(video-repurpose): legenda drawtext UTF-8 → padding |
> 273:| `65167eb` | feat(nav): rotas + nav YouTube Studio & Repurpose (admin-only) |
> 280:  → host-upload-server (3220; JWT admin.getUser + admin-gate user_roles) → streaming → repurpose-inbox/<uid>/<file>
> 281:ingest-external-asset (provider=local, ADMIN) → creative_assets (bucket=local) → video-repurpose-run (ADMIN)
> 282:  → video_renders (engine=repurpose) → worker lê o master do disco (realpath-contido, SEM copiar 1,3GB)
> 284:Infra host (FORA do git): systemd host-upload.service + video-repurpose-bridge.service; nginx location /api/host-upload
> 289:## Motor de repurpose de vídeo — Fatias 1-3 + OTD-SPACES-036 + witness LoRA Record (2026-07-12)
> 297:| BoK blueprint `video-repurpose` (Closed-Loop step 0) | ✅ 5 Pilares · FR-VR-001..009 · OTD-VR-001..007 · FMEA · Pattern Conformance 21 padrões · reuse-map. 10 pointers do Sovereign verificados file:line (o repo andou: segmenter=FR-CP-012, OTD-CP-009 fechada, etc.) |
> 299:| Fatia 2 — cortes 9:16/1:1 + legenda | ✅ **VIVO E2E** — worker `video-repurpose-bridge` + `segment-core` (trim frame-accurate + reframe center-safe + caption). 3 clipes reais provados por Vision QA (timestamp confirma o trim). OTD-VR-006 guard |
> 308:| `f703cc8` | blueprint BoK video-repurpose (Closed-Loop step 0) |
> 313:### Arquitetura do motor de repurpose
> 317:  → video-repurpose-run    → video_renders (engine='repurpose', mode='repurpose'|'carousel', charged 0)
> 318:  → video-repurpose-bridge (host, FFmpeg grátis; OTD-VR-006 re-valida source no READ)
> 319:       repurpose: segment-core → N clipes 9:16/1:1 (trim + reframe + legenda queimada)
> 9911:- **9102 total nodes** (verificado live 2026-07-13 via REST count=exact, youtube-panel-repurpose-frontdoor seal: +handoff `9f7b191a-ec4a-45ef-9906-7a1f4e0b2c01` embedded 768d — Painel YouTube Studio Fatia 1 [`youtube-data` read Data v3+Analytics v2 token per-user server-side + escopos alinhados + mapa API 13rec/175props/52metrics/33ações + Pattern Conformance] + front-door host-local do Repurpose admin-only [drag-drop chunked 80MB furando o cap 100MB do CF → `host-upload-server` 3220 nginx `/api/host-upload` JWT+admin → ingest/run/worker fonte-local realpath-contido; **EP01 real 1,3GB → 5 shorts 9:16 Vision-QA-provados**] + fix legenda drawtext UTF-8→padding; 5 commits `e174988..f10fba4` +README `adcab9a`; /security-review NO FINDINGS ×3; prev 9097 do video-repurpose-engine seal `f050959c`)
> 9912:- **9097 total nodes** (verificado live 2026-07-12 via REST count=exact, video-repurpose-engine seal: +handoff `f050959c-5b05-4518-9142-2cf62ece1816` embedded 768d — Motor de repurpose de vídeo Fatias 1-3 [ingest externo `source_module='external'` VIVO + cortes 9:16/1:1 worker FFmpeg VIVO E2E + carrossel IG provado E2E, reusando a distribuição existente; 3 migrations aplicadas pelo Sovereign; cortes+carrossel provados por Vision QA em mídia real de produção] + OTD-SPACES-036 `space_publish_variants`/nó Publicar-em-Rede-Social + witness LoRA bloqueado em crédito Replicate BYOK; 6 commits `ac5ca86..831f5cc`; /security-review NO FINDINGS ×3; prev 9094 do voice-rail seal `8c1f0e7b`)
> ```

## 🤖 Claude *(15:54:19)*


## 🤖 Claude *(15:54:19)*

Now let me verify the key code pointers I'll cite, especially today's fix (commit a729f83) on the detect-viral-moments BYOK gate.

## 🤖 Claude *(15:54:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -5 && git show a729f83 --stat | head -20",
  "description": "Check recent commits and a729f83 diff stat"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> a729f83 fix(edge): micro-reparos pré-BoK 9/9 — mesh mandate youtube-data + gate Gemini-only do detector
> 7a00511 fix(ui): ReactFlow Controls no tema MIV via --xy-* vars (INC-8cba901a)
> 50bd550 fix(qa): UX-Explorer enxerga pela 1ª vez — 4 causas empilhadas do INC-39626fcd
> 5534eda chore(sprint): landing-factory na Fila Sovereign (item 5) — BoK 9/9 selada, Fatia 1 = landing-bundler
> 29a8b06 docs(handoff): seal landing-factory BoK 9/9 + fix imagem + fix egress (malha 9122)
> commit a729f833a0f33de4b4bb2e2c528e38a06ca76f51
> Author: Gabriel Zarattini <gabrielcall@gmail.com>
> Date:   Thu Jul 16 12:51:27 2026 -0300
> 
>     fix(edge): micro-reparos pré-BoK 9/9 — mesh mandate youtube-data + gate Gemini-only do detector
>     
>     Preparação GO'd das suítes retroativas (auditoria wf_2998d4c7): a Fonte da
>     Verdade nasce documentando o estado REPARADO.
>     
>     youtube-data:
>     - Mesh Connection Mandate (CLAUDE.md §3): observation node no PRIMEIRO
>       channel_summary bem-sucedido (dedup por nome determinístico, best-effort)
>       — Pattern #8 declarado 'yes' no 11-api-surface-map era indevido até aqui
>     - delete_video ganha telemetria distinguível: event 'video_deleted' no
>       infra_health_logs (SEM payload per-tenant — tabela global-read) + trilha
>       de auditoria com videoId na mesh (RLS-scoped)
>     
>     detect-viral-moments:
>     - Gate BYOK honra o contrato FR-VR-010 (openrouter OU gemini OU groq):
>       tenant Gemini-only era rejeitado 402 antes da cascata que JÁ fala Gemini;
> ```

## 🤖 Claude *(15:54:21)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/detect-viral-moments/index.ts",
  "offset": 100,
  "limit": 90
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 100	    const cues = parseSrt(rawSrt);
> 101	    if (cues.length < 2) return json({ error: "no_transcript", detail: "SRT não parseável em cues." }, 422);
> 102	    const sent = cues.slice(0, MAX_CUES_SENT);
> 103	
> 104	    // Cyber-Sentinel: the transcript reaches the LLM verbatim — inspect a bounded slice BEFORE the debit
> 105	    // (never bill a blocked request). It's the tenant's own content, but defense-in-depth against smuggled injection.
> 106	    const sentinelVerdict = inspectPrompt(sent.map((c) => c.text).join(" ").slice(0, 4000), user.id, { rateLimit: false });
> 107	    if (!sentinelVerdict.allow) {
> 108	      await logSentinelBlock(admin, "detect-viral-moments", sentinelVerdict, user.id);
> 109	      return verdictResponse(sentinelVerdict, corsHeaders);
> 110	    }
> 111	
> 112	    // per-user AI key (API Tenancy Model) — FAIL-CLOSED (no Deno.env provider fallback in a user-facing fn).
> 113	    const { data: userKeys } = await admin.from("decrypted_user_api_keys").select("*").eq("user_id", user.id).maybeSingle();
> 114	    const openRouterKey = userKeys?.openrouter_api_key as string | undefined;
> 115	    const groqKey = userKeys?.groq_api_key as string | undefined;
> 116	    const geminiKey = userKeys?.google_api_key as string | undefined;
> 117	    // FR-VR-010 contract: openrouter OR gemini OR groq — a Gemini-only tenant is
> 118	    // valid (the cascade in fetchLLMWithFallback already speaks Gemini; the gate
> 119	    // must not reject what the dispatcher supports).
> 120	    const aiKey = openRouterKey || groqKey || geminiKey;
> 121	    if (!aiKey) {
> 122	      return json({ error: "ai_not_configured", action: "Configure sua chave de IA em /dashboard/settings" }, 402);
> 123	    }
> 124	
> 125	    // mcoCoins gatekeeper: pre-check, then atomic deduction (never client-side).
> 126	    const { data: bal } = await admin.from("profiles").select("mco_balance").eq("id", user.id).maybeSingle();
> 127	    if ((bal?.mco_balance ?? 0) < DETECT_COST) return json({ error: "Saldo insuficiente de mcoCoins" }, 402);
> 128	    const { error: deductErr } = await admin.rpc("deduct_mco_coins", { p_user_id: user.id, p_amount: DETECT_COST });
> 129	    if (deductErr) return json({ error: "Saldo insuficiente de mcoCoins" }, 402);
> 130	    charged = true; chargedUser = user.id;
> 131	
> 132	    const usingGroq = !openRouterKey && !!groqKey;
> 133	    const usingGemini = !openRouterKey && !groqKey && !!geminiKey;
> 134	    const endpoint = usingGemini
> 135	      ? "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
> 136	      : usingGroq
> 137	      ? "https://api.groq.com/openai/v1/chat/completions"
> 138	      : "https://openrouter.ai/api/v1/chat/completions";
> 139	    const model = usingGemini
> 140	      ? "gemini-2.5-flash"
> 141	      : usingGroq
> 142	      ? "llama-3.3-70b-versatile"
> 143	      : "meta-llama/llama-3.3-70b-instruct";
> 144	
> 145	    const sys =
> 146	      "Você é um editor viral especialista (estilo Alex Hormozi). Recebe a transcrição legendada (cues numeradas " +
> 147	      "com tempo em segundos). Selecione os TOP " + topN + " momentos que viralizam como Shorts verticais " +
> 148	      "INDEPENDENTES. CADA clipe DEVE durar 15 a 45 segundos e AGRUPAR VÁRIAS cues CONSECUTIVAS numa micro-história " +
> 149	      "completa: gancho (2s) → desenvolvimento/tensão → payoff. NÃO selecione um único trecho de 2-6s — isso não é " +
> 150	      "um Short. in_sec = início da PRIMEIRA cue do arco; out_sec = fim da ÚLTIMA cue do arco (15-45s de span). " +
> 151	      "beats = índices de cues a destacar como TEXTO GRANDE na tela (o gancho + 1 a 3 punchlines), TODOS dentro de " +
> 152	      "[in_sec,out_sec], cada um com emphasis 'hook'|'punch'|'normal'. Critérios de escolha: gancho forte, " +
> 153	      "curiosidade, frase citável, compreensível SEM contexto externo, payoff. NUNCA invente texto — só selecione " +
> 154	      'cues existentes pelo índice. Responda APENAS JSON válido: {"clips":[{"in_sec":<n>,"out_sec":<n>,"score":<0..1>,' +
> 155	      '"reason":"<pt-BR>","beats":[{"cue":<índice>,"emphasis":"hook"}]}]}';
> 156	    const userMsg = "Transcrição (cues):\n" +
> 157	      sent.map((c) => `#${c.i} [${c.start.toFixed(1)}-${c.end.toFixed(1)}] ${c.text}`).join("\n") +
> 158	      `\n\nRetorne os ${topN} melhores clipes.`;
> 159	
> 160	    const aiResp = await fetchLLMWithFallback(
> 161	      endpoint,
> 162	      {
> 163	        method: "POST",
> 164	        headers: {
> 165	          Authorization: `Bearer ${aiKey}`,
> 166	          "Content-Type": "application/json",
> 167	          // OpenRouter-specific attribution headers — the Gemini OpenAI-compat
> 168	          // endpoint rejects unknown headers (mirrors the cascade's deletes).
> 169	          ...(usingGemini ? {} : {
> 170	            "HTTP-Referer": "https://mcorch.com",
> 171	            "X-Title": "GCRUX Constellation",
> 172	          }),
> 173	        },
> 174	        body: JSON.stringify({
> 175	          model,
> 176	          messages: [{ role: "system", content: sys }, { role: "user", content: userMsg }],
> 177	          stream: false,
> 178	          temperature: 0.3,
> 179	          // strict JSON mode — fallback models in the cascade otherwise emit single-quoted keys /
> 180	          // trailing commas that broke JSON.parse in prod (witnessed 2026-07-13: 500 → refund).
> 181	          response_format: { type: "json_object" },
> 182	        }),
> 183	      },
> 184	      { openRouterKey, geminiKey, groqKey, functionName: "detect-viral-moments" },
> 185	    );
> 186	    if (!aiResp.ok) throw new Error(`llm_http_${aiResp.status}`);
> 187	    const data = await aiResp.json();
> 188	    await logLlmUsage("detect-viral-moments", model, data?.usage);
> 189	    const content: string = data?.choices?.[0]?.message?.content ?? "";
> ```

## 🤖 Claude *(15:54:38)*


## 🤖 Claude *(15:54:38)*


## 🤖 Claude *(15:54:41)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '18,24p' supabase/functions/detect-viral-moments/index.ts && echo \"---run enqueue---\" && sed -n '117,145p' supabase/functions/video-repurpose-run/index.ts && echo \"---ingest master---\" && sed -n '85,91p;95,104p;131,144p' supabase/functions/ingest-external-asset/index.ts",
  "description": "Verify DETECT_COST, enqueue charged_mco=0, ingest gates"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>   "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
> };
> 
> const DETECT_COST = 3;            // 4×-floor calibratable (OTD-VR-010); one analytical LLM pass over the transcript.
> const MIN_CLIP_S = 12;            // OTD-VR-013: a viral short needs a full micro-story, not one 3s cue.
> const MAX_CLIP_S = 90;
> const MAX_CUES_SENT = 500;        // bound tokens for very long masters.
> ---run enqueue---
>     const { data: asset } = await admin.from("creative_assets")
>       .select("id, user_id, kind, storage_bucket, storage_key")
>       .eq("id", sourceAssetId).eq("user_id", user.id).maybeSingle();
>     if (!asset) return json(404, { error: "source_not_found", action: "O vídeo-fonte não existe ou não é seu." });
>     if (asset.kind !== "video") return json(422, { error: "source_not_video" });
>     const bucket = asset.storage_bucket as string, key = asset.storage_key as string;
>     if (bucket === "local") {
>       // Host-local master → ADMIN-ONLY (Sovereign directive 2026-07-12). The worker reads it from
>       // repurpose-inbox/<uid>/ with a real-path containment guard; free-plan Supabase can't hold the master.
>       const { data: adminRow } = await admin.from("user_roles").select("role").eq("user_id", user.id).eq("role", "admin").maybeSingle();
>       if (!adminRow) return json(403, { error: "admin_only", action: "Repurpose de arquivo do host é restrito a administradores." });
>     } else if (!ALLOWED_BUCKETS.has(bucket)) {
>       return json(400, { error: "source_ref_invalid" });   // defense-in-depth; the worker re-checks (OTD-VR-006)
>     }
>     if (!key.startsWith(`${user.id}/`) || key.includes("..")) {
>       return json(400, { error: "source_ref_invalid" });
>     }
> 
>     const composition = mode === "carousel"
>       ? { mode, source: { bucket, key }, source_asset_id: asset.id, slides, handle }
>       : { mode, source: { bucket, key }, source_asset_id: asset.id, clips, fps };
> 
>     const { data: render, error: insErr } = await admin.from("video_renders").insert({
>       user_id: user.id, engine: "repurpose", charged_mco: 0, composition,
>     }).select("id").single();
>     if (insErr || !render) return json(500, { error: "enqueue_failed", detail: insErr?.message });
> 
>     return json(202, {
>       ok: true, render_id: render.id, mode,
> ---ingest master---
>     if (provider === "youtube") {
>       return json(501, {
>         error: "youtube_ingest_gated",
>         action: "O download server-side do YouTube é bloqueado por IP de datacenter (OTD-VR-001). " +
>           "Faça upload do arquivo MP4 do master (default, melhor qualidade).",
>       });
>     }
>     if (storageBucket === "local") {
>       // Host-local master (uploaded via CloudPanel) — the host-FS-source capability is ADMIN-ONLY (Sovereign
>       // directive 2026-07-12). Free-plan Supabase caps uploads at 50MB, so a full documentary lives on host disk;
>       // the worker reads repurpose-inbox/<uid>/<key> with a real-path containment guard.
>       const svc = createClient(
>         Deno.env.get("SUPABASE_URL")!,
>         (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!,
>       );
>       const { data: adminRow } = await svc.from("user_roles").select("role").eq("user_id", user.id).eq("role", "admin").maybeSingle();
>       if (!adminRow) return json(403, { error: "admin_only", action: "Ingestão de arquivo do host é restrita a administradores." });
>     const { data: assetId, error: regErr } = await admin.rpc("register_creative_asset", {
>       p_user_id: user.id,
>       p_kind: "video",
>       p_storage_bucket: storageBucket,
>       p_storage_key: storageKey,
>       p_source_module: "external",
>       p_provider: "upload",
>       p_mime_type: mimeType,
>       p_duration_seconds: durationSeconds,
>       p_width: width,
>       p_height: height,
>       p_title: title,
>       p_metadata: { provider: "upload", ingested_at: new Date().toISOString(), episode, srt },
>     });
> ```

## 🤖 Claude *(15:54:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '55,95p;98,112p' supabase/functions/publish-space-carousel/index.ts",
  "description": "Verify publish-space-carousel scheduled marker and immediate publish"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>     // Resolve the carousel's slides OWNER-SCOPED (the .eq user_id is the tenant gate; kind='image' = the slides).
>     const { data: slides } = await admin.from("creative_assets")
>       .select("storage_bucket, storage_key")
>       .eq("source_job_id", renderId).eq("user_id", user.id).eq("kind", "image")
>       .order("storage_key", { ascending: true });
>     if (!slides || slides.length < 2) return json(422, { error: "carousel_needs_2_slides", have: slides?.length ?? 0 });
>     if (slides.length > 10) slides.length = 10; // IG max
> 
>     // ── FR-SPACES-080 — scheduled mode: enqueue the GROUP MARKER; auto-publish resolves + signs at publish time
>     // (fresh 6h URLs per attempt — FR-SPACES-079). Slides were validated ABOVE (≥2 owner-scoped) before any INSERT.
>     if (schedule) {
>       // Anti double-enqueue (G4): one queued carousel per render per user.
>       const { data: dup } = await admin.from("scheduled_posts")
>         .select("id")
>         .eq("user_id", user.id)
>         .eq("status", "queued")
>         .eq("metadata->reshape->>carousel_render_id", renderId)
>         .limit(1)
>         .maybeSingle();
>       if (dup) return json(409, { error: "already_queued", scheduled_post_id: dup.id });
> 
>       const { data: sp, error: spErr } = await admin.from("scheduled_posts").insert({
>         user_id: user.id,
>         content_id: null,
>         campaign_id: null,
>         social_account_id: socialAccountId,
>         platform: "instagram",
>         scheduled_at: publishAt ?? new Date().toISOString(),
>         status: "queued",
>         metadata: { reshape: { content: { text: caption }, carousel_render_id: renderId, channel: "instagram", surface: "carousel" } },
>       }).select("id, scheduled_at").single();
>       if (spErr || !sp) return json(500, { error: "enqueue_failed", detail: spErr?.message });
> 
>       admin.from("infra_health_logs").insert({ service: "publish-space-carousel", status: "healthy" }).then(() => {}, () => {});
>       return json(200, { ok: true, scheduled: true, scheduled_post_id: sp.id, scheduled_at: sp.scheduled_at, slides: slides.length });
>     }
> 
>     const images: string[] = [];
>     for (const s of slides) {
>       const { data: signed } = await admin.storage.from(s.storage_bucket as string).createSignedUrl(s.storage_key as string, 21600);
>     if (images.length < 2) return json(500, { error: "slide_sign_failed" });
> 
>     // Drive publish-social (service-role; user_id server-trusted from the verified token).
>     const pubRes = await fetch(`${Deno.env.get("SUPABASE_URL")}/functions/v1/publish-social`, {
>       method: "POST",
>       headers: { "Content-Type": "application/json", Authorization: `Bearer ${(Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))}` },
>       body: JSON.stringify({
>         platform: "instagram",
>         content: { images, text: caption },
>         social_account_id: socialAccountId,
>         user_id: user.id,
>       }),
>     });
>     const pub = await pubRes.json().catch(() => ({}));
>     if (!pubRes.ok) return json(502, { error: "publish_failed", detail: pub?.error ?? pub });
> ```

## 🤖 Claude *(15:54:49)*


## 🤖 Claude *(15:54:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n '140,165p;364,378p' src/pages/VideoRepurposePage.tsx && echo \"=== useVideoRepurpose ===\" && sed -n '60,72p;183,212p' src/hooks/useVideoRepurpose.ts && echo \"=== route ===\" && grep -n \"repurpose\" src/App.tsx",
  "description": "Verify UI pointers in VideoRepurposePage and hook"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>   }, [viral?.done, viral?.total, renderId, renderState, clipsReady]); // eslint-disable-line react-hooks/exhaustive-deps
> 
>   // FR-VR-015 — one click: ingest (if needed) → detector (SRT→Hormozi) → enqueue beats-clips → progress.
>   const doViralCuts = async () => {
>     if (!user || (!assetId && !hostFilename.trim())) return;
>     try {
>       setViral({ pct: 4, log: '📦 Preparando o master…', total: 0, done: false });
>       let aid = assetId;
>       if (!aid) {
>         setViral((v) => v && { ...v, pct: 8, log: '📦 Registrando o master (ingest)…' });
>         const ing = await ingest.mutateAsync({
>           storage_bucket: 'local',
>           storage_key: `${user.id}/${hostFilename.trim()}`,
>           title: title || hostFilename.trim(),
>           mime_type: 'video/mp4',
>           srt_pt: srtPt || undefined,
>         });
>         aid = ing.asset_id;
>         setAssetId(aid);
>       }
>       setViral((v) => v && { ...v, pct: 16, log: '🧠 Detectando momentos virais (Hormozi sobre o SRT)…' });
>       const det = await detect.mutateAsync({ master_asset_id: aid!, top_n: 3 });
>       const detClips: ClipSpecInput[] = det.clips.map((c) => ({
>         in_sec: c.in_sec, out_sec: c.out_sec, reframe: '9:16', caption: '',
>         caption_mode: 'beats', text_beats: c.text_beats,
>       }));
>             <div className="flex items-center justify-between">
>               <label className="text-xs text-muted-foreground">Legenda SRT pt-BR (opcional)</label>
>               {/* FR-VR: upload the .srt file instead of pasting — reads into the same field. */}
>               <label className="text-xs text-primary cursor-pointer hover:underline">
>                 Subir arquivo .srt
>                 <input
>                   type="file"
>                   accept=".srt,.vtt,text/plain"
>                   className="hidden"
>                   onChange={(e) => {
>                     const f = e.target.files?.[0];
>                     if (!f) return;
>                     f.text().then((t) => setSrtPt(t)).catch(() => toast.error('Falha ao ler o arquivo SRT'));
>                     e.target.value = '';
>                   }}
> === useVideoRepurpose ===
>   });
> }
> 
> // Drag-and-drop upload of a LARGE master straight to the host disk (repurpose-inbox/<uid>/) via the
> // nginx-fronted host-upload service — the free-plan Supabase 50MB cap makes Storage impossible for a full
> // documentary. XHR (not fetch) so we get upload progress. The Supabase JWT authenticates + admin-gates server-side.
> // Cloudflare (free plan) caps each request body at 100MB → slice the master into <100MB chunks; each passes CF
> // and the host appends them (renaming on the last chunk). Small files go as a single request. XHR gives progress.
> const CHUNK_BYTES = 80 * 1024 * 1024;
> 
> interface UploadResp { ok?: boolean; done?: boolean; filename?: string; bytes?: number }
> 
> function xhrPost(body: Blob, headers: Record<string, string>, onLoaded: (loaded: number) => void): Promise<UploadResp> {
>     Error,
>     { source_asset_id: string; platform: string; caption?: string }
>   >({
>     mutationFn: async ({ source_asset_id, platform, caption }) => {
>       const { data, error } = await supabase.functions.invoke('publish-space-asset', {
>         body: {
>           source_asset_id, platform, channel: platform, surface: 'video', publish: true,
>           native_text: caption ? { caption } : {},
>         },
>       });
>       if (error) throw new Error(await edgeErrorMessage(error, 'Falha ao enviar para distribuição.'));
>       return data ?? {};
>     },
>   });
> }
> 
> // S1 UX: honest SRT badge — server truth from the ingested master's metadata (RLS own).
> export function useMasterSrtStatus(assetId: string | null) {
>   return useQuery({
>     queryKey: ['master_srt', assetId],
>     enabled: !!assetId,
>     queryFn: async () => {
>       const { data, error } = await supabase
>         .from('creative_assets').select('metadata').eq('id', assetId!).maybeSingle();
>       if (error) throw error;
>       const srt = (data?.metadata as { srt?: { pt?: string; en?: string } } | null)?.srt;
>       const len = (srt?.pt ?? srt?.en ?? '').length;
>       return { hasSrt: len > 100, chars: len };
>     },
>   });
> === route ===
> 132:                <Route path="repurpose" element={<VideoRepurposePage />} />
> ```

## 🤖 Claude *(15:55:00)*


## 🤖 Claude *(15:55:02)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"p_source_module\" scripts/video-repurpose-bridge.ts && grep -n \"MAX_CHARS\\|1080\\|1350\" scripts/video-repurpose/carousel-core.ts | head -8 && grep -rn \"video-repurpose\\|repurpose\" src/components/dashboard/DashboardSidebar.tsx 2>/dev/null | head -5",
  "description": "Verify derived provenance hyperframes, carousel dims, sidebar nav"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 106:          p_source_module: 'hyperframes', p_source_job_id: renderId, p_parent_asset_id: comp.source_asset_id ?? null,
> 123:          p_source_module: 'hyperframes', p_source_job_id: renderId, p_parent_asset_id: comp.source_asset_id ?? null,
> 6: * (key-frame timestamps + captions, e.g. one per chapter/ato) → N still slides (1080×1350, 4:5) — key-frame
> 20:const W = 1080, H = 1350;            // 4:5 carousel page (IG feed / carousel)
> 23:const MAX_CHARS = 16;                // very conservative: DejaVu Bold wide words (documentário/constelação) at 40px
> 48:/** Greedy word-wrap to lines of ≤ MAX_CHARS; a single over-long word is hard-split. */
> 49:export function wrapCaption(text: string, maxChars = MAX_CHARS): string[] {
> src/components/dashboard/DashboardSidebar.tsx:83:      { title: 'Repurpose de Vídeo', url: '/dashboard/repurpose', icon: Scissors, adminOnly: true },
> ```

## 🤖 Claude *(15:56:31)*


## 🤖 Claude *(15:56:31)*

All pointers verified by own reading. Now I'll write the three documents.

## 🤖 Claude *(15:58:08)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-repurpose/01-mrd.md",
  "content": "# MRD \u2014 Market Requirements Document\n\n**Project:** video-repurpose (1 master externo \u2192 N shorts 9:16 + carrossel IG)\n**Version:** v1.0 (retroativa) | **Date:** 2026-07-16\n**BoK Applied:** BABOK v3 (Strategy Analysis) sobre estado shipado\n**Status:** Selada \u2014 retroativa\n\n> Su\u00edte retroativa \u2014 consolida m\u00f3dulo J\u00c1 SHIPADO; ground truth = c\u00f3digo vivo + auditoria wf_2998d4c7\n>\n> Este MRD documenta o **estado real do c\u00f3digo** (Fatias 1-3 + front-door host + Viral Quality VIVOS; Fatia 4 n\u00e3o-shipada; FR-VR-013 processo manual), n\u00e3o o blueprint. Onde o blueprint `00-deepsearch-blueprint.md` (2026-07-12) divergiu do que foi constru\u00eddo, **vale o c\u00f3digo** \u2014 os drifts est\u00e3o corrigidos aqui por escrito. A semente hist\u00f3rica permanece na fam\u00edlia como registro do Closed-Loop Step 0.\n\n> **ORO triplet:** Operator = MCORCH Master Execution Agent \u00b7 Reviewer = Sovereign + `/security-review` por seam + Vision QA ocular por criativo (Lei 1) \u00b7 Owner = Sovereign (blast radius: alcance p\u00fablico gated em auditoria de app IG/TikTok \u2014 a\u00e7\u00e3o dele, n\u00e3o c\u00f3digo; rail de render 100% gr\u00e1tis US$ 0).\n\n---\n\n## 1. Executive Summary\n\nAt\u00e9 2026-07-12 o MCORCH **distribu\u00eda** conte\u00fado (publish-social/publish-wordpress/reshape-pillar/`scheduled_posts`+`auto-publish`) mas **n\u00e3o produzia cortes**: n\u00e3o havia como ingerir um v\u00eddeo longo externo, segment\u00e1-lo em N shorts verticais e extrair carross\u00e9is. O gap era reconhecido formalmente \u2014 o SDD do post-engine gateava a auto-segmenta\u00e7\u00e3o (**FR-CP-012**) em *\"aplic\u00e1vel quando entrar INPUT de v\u00eddeo longo\"* (`docs/bok/post-engine/13-sdd-reshaper-atomizer.md:196`).\n\nO m\u00f3dulo **video-repurpose** fechou essa metade: **1 master externo** (document\u00e1rio \"Gabriel AI\", 16:9, ~7-8 min, produzido pelo pipeline inverso do repo `gabrielZarattini/GabrielAI`) **\u2192 N shorts 9:16** (reenquadrados center-safe, legenda queimada ou motion-graphic palavra-por-palavra) **+ carrossel IG** (slides 1080\u00d71350 dos key-frames), tudo escoando pelos trilhos de distribui\u00e7\u00e3o **j\u00e1 existentes** (sink `publish-space-asset`/`publish-space-carousel` \u2192 `publish-social`). O rail de transforma\u00e7\u00e3o \u00e9 **100% gr\u00e1tis** (FFmpeg + whisper.cpp self-host, `charged_mco=0`); o \u00fanico passo metered \u00e9 o detector de momentos virais (3 mcoCoins, LLM per-user BYOK).\n\n**Estado shipado provado em produ\u00e7\u00e3o (Lei 1):** EP01 real de 1,3 GB \u2192 5 shorts 9:16 Vision-QA-provados (2026-07-13); 3 shorts virais motion-graphic E2E com scores 9.0/9.5/8.5 e Vision 7-8/10 (2026-07-14); 1 carrossel IG E2E (2026-07-12). Commits `f703cc8`\u2192`a729f83` (traceabilidade completa no \u00a79).\n\n---\n\n## 2. Market Problem Statement\n\n### 2.1 Estado hist\u00f3rico (snapshot PR\u00c9-implementa\u00e7\u00e3o, 2026-07-12 \u2014 n\u00e3o \u00e9 o estado atual)\n\n> \u26a0\ufe0f A tabela \u00a72 do blueprint descreve este estado hist\u00f3rico. **N\u00e3o copi\u00e1-la como estado atual** \u2014 tudo abaixo foi resolvido pelo m\u00f3dulo.\n\n- `creative_assets` **rejeitava origem externa** \u2014 o CHECK de `source_module` n\u00e3o tinha `'external'`.\n- **Zero segmenta\u00e7\u00e3o de v\u00eddeo** no repo: nenhum worker cortava, reenquadrava ou queimava legenda em v\u00eddeo-fonte.\n- `publish-social` IG publicava **s\u00f3 REELS** \u2014 sem `media_type=CAROUSEL`.\n- FR-CP-012 (1 longa \u2192 N shorts) formalmente **gated** por aus\u00eancia de input longo.\n- O acervo de masters (epis\u00f3dios GabrielAI validados, 4 epis\u00f3dios 6+ min) morria sem repurpose \u2014 cada epis\u00f3dio gerava 1 publica\u00e7\u00e3o em vez de N.\n\n### 2.2 Root Cause\n\n- **Gap de capacidade, n\u00e3o de distribui\u00e7\u00e3o:** a sa\u00edda (canais, agendamento, disclosure sint\u00e9tica, ledger de receita) j\u00e1 existia. Faltava a **entrada** (ingest de MP4 externo) e a **transforma\u00e7\u00e3o** (corte/reframe/caption/carrossel).\n- **Caps de plataforma reais** bloqueavam o caminho ing\u00eanuo: Supabase free capa upload em 50 MB (o master tem 1,3 GB) e o Cloudflare free capa cada request em 100 MB \u2014 resolvidos pelo front-door host-local com upload chunked de 80 MB (`useVideoRepurpose.ts:68`).\n- **YouTube bloqueia IP de datacenter** (probe yt-dlp confirmado 2026-07-13) \u2014 o fallback \"cole um link do YouTube\" \u00e9 estruturalmente invi\u00e1vel server-side (OTD-VR-001, gate 501 vivo).\n\n### 2.3 Estado entregue (o c\u00f3digo vivo)\n\nUpload do master (host-local admin-only para arquivos grandes; bucket privado owner-scoped para pequenos) \u2192 SRT por arquivo na UI ou ASR self-host (whisper.cpp, US$ 0) \u2192 detector Hormozi seleciona os melhores momentos **sem fabricar cita\u00e7\u00e3o** (beats = cues verbatim do SRT; o LLM s\u00f3 escolhe \u00edndices) \u2192 worker FFmpeg corta/reenquadra/veste (motion-graphic alpha ou drawtext byte-pad) \u2192 derivados nascem `creative_assets` e s\u00e3o distribu\u00edveis com 1 clique pelos trilhos existentes. Rail IG hoje tem **3 superf\u00edcies** (REELS / CAROUSEL / STORIES).\n\n---\n\n## 3. Target Market Segments\n\n| Segment | Description | Size | Urgency | Accessibility |\n|---------|-------------|------|---------|---------------|\n| Primary | **Usu\u00e1rio Zero** (Gabriel, admin) operando a **persona de marca Gabriel AI / CCIO** \u2014 o document\u00e1rio \u00e9 o ativo-m\u00e3e; os shorts/carross\u00e9is s\u00e3o a m\u00e1quina de volume da marca ([[project_brand_persona_ccio]]) | 1 tenant (piloto enterprise interno) | High | **Imediata e VIVA** \u2014 `/dashboard/repurpose` operacional; alcance externo gated em auditoria de app (a\u00e7\u00e3o Sovereign) |\n| Secondary | **Tenants futuros** com acervo de v\u00eddeo longo pr\u00f3prio (masters \u226450 MB via bucket privado owner-scoped; masters grandes exigem hardening multi-tenant do front-door host, hoje admin-only) | P\u00f3s-Usu\u00e1rio 1 | Medium | Parcial \u2014 seams owner-scoped existem; fonte `local` \u00e9 admin-only por diretiva Sovereign 2026-07-12 |\n\n### 3.1 TAM / SAM / SOM\n\n**N\u00e3o quantificado nesta su\u00edte retroativa (Lei 1).** Nenhuma fonte externa datada de mercado foi verificada para este m\u00f3dulo; preencher TAM/SAM/SOM seria fabricar mercado. O racional de mercado \u00e9 **estrat\u00e9gico e interno**: o m\u00f3dulo multiplica o rendimento de um ativo j\u00e1 pago (1 epis\u00f3dio \u2192 N criativos) dentro do motor de conte\u00fado de duas m\u00e1quinas do MCORCH \u2014 a **m\u00e1quina de volume** (audi\u00eancia) \u00e9 alimentada a custo marginal ~US$ 0 ([[project_content_engine_two_machines]]).\n\n---\n\n## 4. Posicionamento estrat\u00e9gico & doutrina\n\n### 4.1 Doutrina USD-0 / open-source-first (decis\u00e3o de neg\u00f3cio, n\u00e3o detalhe t\u00e9cnico)\n\nO rail inteiro de transforma\u00e7\u00e3o foi constru\u00eddo para custar **US$ 0 externo** ([[feedback_opensource_first_zero_cost_equity]], [[feedback_paid_byok_post_revenue]]):\n\n| Componente | Motor | Custo externo | Evid\u00eancia |\n|---|---|---|---|\n| Corte/reframe/caption/overlay | FFmpeg (host worker `video-repurpose-bridge`) | US$ 0 | `video-repurpose-run/index.ts:139-141` \u2014 enqueue `engine='repurpose'`, `charged_mco: 0` |\n| Slides de carrossel | FFmpeg puro (`carousel-core.ts`, sem Playwright) | US$ 0 | `carousel-core.ts:20-23` \u2014 1080\u00d71350, `MAX_CHARS=16` (OTD-VR-007) |\n| Transcri\u00e7\u00e3o (masters sem SRT) | whisper.cpp self-host (`/home/ubuntu/.mcorch/asr-engine/`) | US$ 0 | SOP `docs/processes/asr-master-to-srt.md` (commit `67dc54d`) |\n| Overlay motion-graphic | Playwright headless local (`renderAlphaFrames`) | US$ 0 | `render-core.ts:359,392` (`omitBackground:true`) |\n| Detector viral (\u00fanico metered) | LLM **per-user BYOK** fail-closed (openrouter OU gemini OU groq) | Do tenant (free-tier vi\u00e1vel) | `detect-viral-moments/index.ts:117-122` \u2014 `DETECT_COST=3` mco |\n| Vision QA | Vision MCP (custo 0 Usu\u00e1rio Zero) | US$ 0 | `scripts/qa/vision-qa.ts` |\n\n### 4.2 Diferencia\u00e7\u00e3o defens\u00e1vel (verific\u00e1vel no repo)\n\nA categoria \"repurpose de v\u00eddeo\" externa (ferramentas de clipping) entrega o corte, mas n\u00e3o entrega o que vem **depois** do corte. No MCORCH, o derivado nasce `creative_assets` e \u00e9 imediatamente consum\u00edvel pela distribui\u00e7\u00e3o que j\u00e1 mede receita:\n\n| Capacidade | MCORCH (verificado) | Veredito |\n|---|---|---|\n| Corte data-driven 1\u2192N + reframe + caption | `segment-core.ts` vivo E2E | **Novo \u2014 este m\u00f3dulo** |\n| Sele\u00e7\u00e3o viral sem fabrica\u00e7\u00e3o (beats verbatim do SRT) | `detect-viral-moments` (Lei 1 estrutural) | **Novo \u2014 este m\u00f3dulo** |\n| Distribui\u00e7\u00e3o multi-canal + agendamento | `publish-space-asset`/`publish-space-carousel` \u2192 `auto-publish` \u2192 `publish-social` (reuso puro) | **Fosso preexistente** |\n| Disclosure sint\u00e9tica estrutural | `is_aigc`/`containsSyntheticMedia` hard-coded preservados | **Fosso preexistente** |\n| Ledger de custo por a\u00e7\u00e3o (mcoCoins) + telemetria | d\u00e9bito+refund at\u00f4mico no detector; `infra_health_logs` | **Fosso preexistente** |\n\n### 4.3 Rela\u00e7\u00e3o com o repo GabrielAI (a fonte, n\u00e3o o molde)\n\nO pipeline `gabrielZarattini/GabrielAI` \u00e9 o **INVERSO** deste m\u00f3dulo (N takes Veo 8s \u2192 1 master via ponte Premiere). Ele fornece: (a) o **master** de entrada; (b) o **schema de metadados** `episodios/epNN.json` (`titulo/atos[]/creditos.blocos[]/teaser/tags`), gravado em `creative_assets.metadata.episode` no ingest; (c) a filosofia **cut-spec data-driven** (cortes de dado, n\u00e3o de texto); (d) o **roteiro-autoritativo** para reconciliar erros do ASR (o \u00e1udio de IA erra nomes \u2014 witness Austin\u2192Boston Dynamics, 2026-07-14). **N\u00e3o reconstruir os trilhos dele** ([[project_video_repurpose_engine]]).\n\n---\n\n## 5. Market Opportunity & Timing\n\n- **Multiplicador de acervo:** 4 epis\u00f3dios validados de 6+ min j\u00e1 existiam sem repurpose; cada master agora rende N shorts + 1 carrossel + (futuro, Fatia 4) 1 post WordPress \u2014 a custo marginal ~US$ 0. \"Minera\u00e7\u00e3o de v\u00eddeo a custo ~US$ 0\" (HANDOFF 2026-07-14).\n- **Virada brand-first:** a persona Gabriel AI/CCIO evangeliza o MCORCH; o produto \u00e9 subproduto da marca. O volume de shorts \u00e9 o combust\u00edvel da persona ([[project_brand_persona_ccio]]).\n- **Destravamento interno:** este m\u00f3dulo \u00e9 o gatilho declarado de **FR-CP-012** do post-engine (auto-segmenta\u00e7\u00e3o) \u2014 o input longo que faltava agora existe.\n- **Timing honesto:** o alcance externo real (IG/TikTok p\u00fablicos) segue **gated em auditoria de app** (TikTok for\u00e7a `SELF_ONLY` pr\u00e9-audit) \u2014 a a\u00e7\u00e3o \u00e9 do Sovereign, n\u00e3o c\u00f3digo. O m\u00f3dulo produz e enfileira; o \"ir a p\u00fablico\" tem gate externo declarado.\n\n---\n\n## 6. Market Requirements (status REAL \u2014 retroativo)\n\n> Conven\u00e7\u00e3o de status: **VIVO** (c\u00f3digo em produ\u00e7\u00e3o, prova material) \u00b7 **GATED** (c\u00f3digo existe, gate externo/501) \u00b7 **MANUAL** (capacidade exercida por processo humano, sem c\u00f3digo) \u00b7 **N\u00c3O-SHIPADO** (zero c\u00f3digo).\n\n| ID | Market Requirement | Priority | Status REAL | Evid\u00eancia |\n|----|-------------------|----------|-------------|-----------|\n| MR-VR-001 | Ingerir master de v\u00eddeo externo owner-scoped com metadados de epis\u00f3dio + SRT, no spine `creative_assets` (`source_module='external'` \u2014 **s\u00f3 o master**; derivados nascem `'hyperframes'`) | Critical | **VIVO** | migration `20260712120000` + `ingest-external-asset/index.ts:131-144`; derivados: `video-repurpose-bridge.ts:106,123` (`p_source_module:'hyperframes'`, `parent_asset_id`=master) |\n| MR-VR-002 | Masters gigantes (1,3 GB) precisam entrar apesar dos caps de plataforma (Supabase 50 MB, CF 100 MB/request) | Critical | **VIVO** (admin-only) | `host-upload-server.ts` (loopback 3220) + upload chunked 80 MB (`useVideoRepurpose.ts:68`); infra versionada `infra/systemd/` + `infra/nginx/` (commit `955117d`) |\n| MR-VR-003 | 1 master \u2192 N shorts 9:16 (reframe center-safe + legenda queimada), custo de render US$ 0 | Critical | **VIVO** | `segment-core.ts` (reframe `:62-67`, drawtext byte-pad `:107-118`); EP01 \u2192 5 shorts Vision-QA (2026-07-13) |\n| MR-VR-004 | Sele\u00e7\u00e3o dos MELHORES momentos (framework Hormozi) **sem fabricar cita\u00e7\u00e3o** \u2014 texto na tela deriva do SRT falado | Critical | **VIVO** | `detect-viral-moments/index.ts:186-233` (LLM escolhe \u00edndices de cues; beats verbatim); contrato BYOK openrouter/gemini/groq **fechado** em `a729f83` (2026-07-16, `:117-122`) |\n| MR-VR-005 | Est\u00e9tica premium som-off: motion-graphic palavra-por-palavra, sem bot\u00e3o/HUD | High | **VIVO** | template `viral-caption-overlay-9x16.html` (transparente, XSS-safe) + `renderAlphaFrames` (`render-core.ts:359,392`) + overlay FFmpeg (`segment-core.ts:79-103`) |\n| MR-VR-006 | Carrossel IG do mesmo master (key-frames + captions dos cap\u00edtulos) | High | **VIVO** | `carousel-core.ts` (FFmpeg puro, 1080\u00d71350) + branch CAROUSEL `publish-social/index.ts:202-229` + seam `publish-space-carousel` (imediato E agendado via marcador `carousel_render_id`) \u2014 **n\u00e3o passa por `channel_profiles`** (OTD-VR-003 aberta) |\n| MR-VR-007 | Escoar pela distribui\u00e7\u00e3o existente sem reconstruir (rail IG = 3 superf\u00edcies REELS/CAROUSEL/STORIES) | Critical | **VIVO** | bot\u00e3o Distribuir \u2192 `publish-space-asset` (`useVideoRepurpose.ts:187`); STORIES = FR-SPACES-083 (Amendment 24) |\n| MR-VR-008 | Legenda nativa por plataforma + corpo HTML WordPress com fontes creditadas (mapeador de metadados) | Medium | **N\u00c3O-SHIPADO** | Fatia 4 \u2014 zero refs de FR-VR-008 em c\u00f3digo; decis\u00e3o OTD-VR-004 (adaptar reshape vs mapper) nunca tomada |\n| MR-VR-009 | Qualidade verificada por olhar (rubrica viral: hook-2s, legibilidade som-off, ritmo, reenquadre) | High | **MANUAL** | Vision QA por sess\u00e3o (witnesses 2026-07-12/13/14); loop automatizado FR-VR-013 = zero c\u00f3digo (`grep MAX_VIRAL_ITERS\\|vision_score` = 0 hits) |\n| MR-VR-010 | Transcri\u00e7\u00e3o a custo zero para masters sem SRT | High | **VIVO** (host-side, SOP) | whisper.cpp self-host + reconcilia\u00e7\u00e3o roteiro-autoritativa \u2014 SOP `docs/processes/asr-master-to-srt.md` (commit `67dc54d`) |\n| MR-VR-011 | Alcance externo p\u00fablico real (IG/TikTok fora de SELF_ONLY) | High | **GATED** (a\u00e7\u00e3o Sovereign) | auditoria de app pendente; disclosure sint\u00e9tica hard-coded preservada no publish path |\n\n---\n\n## 7. Success Metrics (provadas \u2014 Lei 1)\n\n| KPI | Definition | Resultado material | Evid\u00eancia |\n|-----|-----------|--------------------|-----------|\n| Master real processado | EP01 (1,3 GB) \u2192 shorts 9:16 1080\u00d71920 | **5 shorts** provados | Vision QA 2026-07-13 (reframe centralizado + legenda completa); malha 9102, n\u00f3 `9f7b191a` |\n| Shorts virais E2E | detector \u2192 motion-graphic \u2192 prod | **3 shorts** (abertura 9.0 / finale 9.5 / conspira\u00e7\u00e3o 8.5; Vision 7-8/10) | HANDOFF 2026-07-14; malha 9105, n\u00f3 `d98767ea` |\n| Carrossel IG E2E | master \u2192 slides \u2192 asset registrado | **3 slides 1080\u00d71350** + Vision QA no slide real | HANDOFF 2026-07-12; malha 9097, n\u00f3 `f050959c` |\n| Custo externo do rail | USD por render | **US$ 0** | `charged_mco=0` + FFmpeg/whisper.cpp self-host |\n| Seguran\u00e7a | `/security-review` por seam | **NO FINDINGS** \u00d73 (F1-F3) + \u00d73 (front-door) + \u00d74 (Viral Quality) | HANDOFF seals 2026-07-12/13/14 |\n| Anticorpos re-execut\u00e1veis | smokes do m\u00f3dulo | **3 smokes** (`smoke-external-ingest`, `smoke-video-repurpose`, `smoke-scheduled-carousel`) | \u26a0\ufe0f gap honesto: `smoke-carousel.ts` \u00e9 do POST-ENGINE (PDF/LinkedIn), n\u00e3o deste m\u00f3dulo; o render do `carousel-core` n\u00e3o tem smoke pr\u00f3prio \u2014 prova \u00e9 o witness Vision 2026-07-12 |\n\n---\n\n## 8. Regulatory & Compliance Context\n\n| Constraint | Applicability | Estado real |\n|------------|---------------|-------------|\n| Disclosure de conte\u00fado sint\u00e9tico | Todo publish de derivado | **Estrutural, preservado**: `is_aigc:true` (TikTok) e `containsSyntheticMedia:true` (YouTube) hard-coded no `publish-social` \u2014 n\u00e3o remov\u00edveis pelo caller |\n| Auditoria de app (TikTok/IG) | Alcance p\u00fablico | **GATED** \u2014 TikTok `SELF_ONLY` for\u00e7ado pr\u00e9-audit; a\u00e7\u00e3o Sovereign, registrada como gate honesto (MR-VR-011) |\n| Lei 1 anti-fabrica\u00e7\u00e3o de cita\u00e7\u00e3o | Texto na tela dos shorts | **Estrutural**: beats = cues verbatim do SRT; o LLM s\u00f3 seleciona \u00edndices (`detect-viral-moments:186-233`); ASR reconciliado contra o roteiro-autoritativo do GitHub |\n| Tenancy / cross-tenant | Ingest, worker, publish | Owner-scoping em todos os seams (key-prefix `${uid}/`, resolve `.eq user_id`, guarda OTD-VR-006 no READ com realpath-containment \u2014 `video-repurpose-bridge.ts:72-93`); fonte `local` duplo admin-gate |\n| Cyber-Sentinel | Transcript \u2192 LLM | Inspe\u00e7\u00e3o pr\u00e9-d\u00e9bito do SRT (nunca cobrar request bloqueada) \u2014 `detect-viral-moments:106-110` |\n\n---\n\n## 9. Traceability (MR \u2192 commits \u2192 docs)\n\n| Commit | Entrega | MRs |\n|--------|---------|-----|\n| `f703cc8` | Blueprint (Closed-Loop Step 0 \u2014 semente hist\u00f3rica) | todos |\n| `0e4393c` | Fatia 1 \u2014 ingest externo (`source_module='external'`) | MR-VR-001 |\n| `439d064` | Fatia 2 \u2014 worker segment/reframe/caption | MR-VR-003 |\n| `831f5cc` | Fatia 3 \u2014 carrossel IG (carousel-core + branch CAROUSEL + seam) | MR-VR-006 |\n| `9f561c0` | Front-door host-local admin-only (chunked 80 MB) | MR-VR-002 |\n| `681002f` | Fix legenda drawtext UTF-8 \u2192 byte-pad | MR-VR-003 |\n| `65167eb` | Rotas + nav (YouTube Studio & Repurpose admin-only) | MR-VR-002 |\n| `d4972c7` | Fatia 6 \u2014 Viral Quality (detector + overlay motion-graphic + UI 1-clique) | MR-VR-004/005 |\n| `67dc54d` | ASR self-host + reconcilia\u00e7\u00e3o roteiro-autoritativa | MR-VR-010 |\n| `955117d` | Rota host-media (Range 206) + infra host versionada | MR-VR-002 |\n| `a729f83` | Gate BYOK do detector aceita Gemini-only (contrato FR-VR-010 cumprido) | MR-VR-004 |\n\n**Stub MR \u2192 BR (selado na BRD):** MR-VR-001\u2192BR-VR-001/002 \u00b7 MR-VR-002\u2192BR-VR-003 \u00b7 MR-VR-003\u2192BR-VR-004 \u00b7 MR-VR-004\u2192BR-VR-005 \u00b7 MR-VR-005\u2192BR-VR-006 \u00b7 MR-VR-006\u2192BR-VR-007 \u00b7 MR-VR-007\u2192BR-VR-008 \u00b7 MR-VR-008\u2192BR-VR-011 (roadmap) \u00b7 MR-VR-009\u2192BR-VR-009 \u00b7 MR-VR-010\u2192BR-VR-010 \u00b7 MR-VR-011\u2192BR-VR-012 (gate).\n\n---\n\n_Generated by MCORCH BoK Scribe Agent \u2014 su\u00edte retroativa fiel ao c\u00f3digo vivo (Lei 1: todo pointer file:line re-verificado por leitura pr\u00f3pria em 2026-07-16; drifts do blueprint corrigidos: derivados=`hyperframes`, carrossel fora de `channel_profiles`, slides=FFmpeg puro, legenda=drawtext byte-pad, erro=`ai_not_configured`, rail IG 3 superf\u00edcies, commit `955117d` inclu\u00eddo, 3 smokes n\u00e3o 4)._\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-repurpose/01-mrd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:00:16)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-repurpose/02-brd.md",
  "content": "# BRD \u2014 Business Requirements Document\n\n**Project:** video-repurpose (1 master externo \u2192 N shorts 9:16 + carrossel IG)\n**Version:** v1.0 (retroativa) | **Date:** 2026-07-16\n**BoK Applied:** BABOK v3 (Requirements Analysis & Design Definition) sobre estado shipado\n**Status:** Selada \u2014 retroativa\n**Source of truth:** c\u00f3digo vivo + [`01-mrd.md`](01-mrd.md); semente hist\u00f3rica em [`00-deepsearch-blueprint.md`](00-deepsearch-blueprint.md) (n\u00e3o copiar \u00a72/\u00a7Pilar II-III como estado atual); FRD/SDD da Fatia 6 em [`10-frd-sdd-viral-quality.md`](10-frd-sdd-viral-quality.md).\n\n> Su\u00edte retroativa \u2014 consolida m\u00f3dulo J\u00c1 SHIPADO; ground truth = c\u00f3digo vivo + auditoria wf_2998d4c7\n\n> **ORO triplet:**\n> - **Operator:** MCORCH Master Execution Agent\n> - **Reviewer:** Sovereign + `/security-review` por seam + Vision QA ocular por criativo\n> - **Owner:** Sovereign \u2014 blast radius material: alcance p\u00fablico depende de auditoria de app (IG/TikTok); custo externo do rail = US$ 0 (FFmpeg/whisper.cpp self-host); \u00fanico metered = detector (3 mco, BYOK do tenant).\n\n---\n\n## 1. Executive Summary\n\nO m\u00f3dulo transformou o MCORCH de distribuidor em **produtor de cortes**: 1 master externo (document\u00e1rio Gabriel AI) vira N shorts 9:16 vestidos (motion-graphic ou legenda queimada) + carrossel IG, escoando pelos trilhos vivos sem reconstruir distribui\u00e7\u00e3o. O valor de neg\u00f3cio \u00e9 o **multiplicador de acervo a custo marginal ~US$ 0** para a m\u00e1quina de volume da marca ([[project_content_engine_two_machines]], [[project_brand_persona_ccio]]): cada epis\u00f3dio j\u00e1 pago rende N criativos distribu\u00edveis, e o \u00fanico custo vari\u00e1vel \u00e9 o detector viral (3 mcoCoins/an\u00e1lise, LLM na chave BYOK do pr\u00f3prio tenant).\n\n**O que est\u00e1 VIVO** (prova material no \u00a79 do MRD): ingest externo + front-door host para masters de 1,3 GB + worker FFmpeg de segmenta\u00e7\u00e3o + carrossel IG (imediato e agendado) + detector Hormozi anti-fabrica\u00e7\u00e3o + overlay motion-graphic + UI 1-clique + ASR self-host. **O que N\u00c3O est\u00e1:** o mapeador de metadados (Fatia 4 / FR-VR-008, zero c\u00f3digo) e o loop Vision automatizado (FR-VR-013 \u2014 a rubrica \u00e9 exercida **manualmente** por sess\u00e3o). **Gate externo honesto:** alcance p\u00fablico IG/TikTok depende de auditoria de app (a\u00e7\u00e3o Sovereign).\n\n---\n\n## 2. Business Objectives (SMART \u2014 retroativos, com resultado)\n\n| ID | Objective | Measurable | Resultado REAL | Evid\u00eancia |\n|----|-----------|------------|----------------|-----------|\n| BO-VR-001 | Ingerir master externo no spine `creative_assets` sem fragmentar a interop | migration aditiva + seam owner-scoped | \u2705 **Atingido** | migration `20260712120000` (CHECK + RPC union `'external'`); `ingest-external-asset` vivo; smoke 5/5 (commit `0e4393c`) |\n| BO-VR-002 | Produzir shorts 9:16 reais de master real a custo US$ 0 | \u22651 clipe renderizado e inspecionado | \u2705 **Superado** \u2014 EP01 1,3 GB \u2192 5 shorts Vision-QA; +3 shorts virais E2E | HANDOFF 2026-07-13/14; `charged_mco=0` (`video-repurpose-run:139-141`) |\n| BO-VR-003 | Carrossel IG E2E do mesmo master | \u22651 carrossel visto | \u2705 **Atingido** \u2014 3 slides 1080\u00d71350 + Vision QA no slide real | HANDOFF 2026-07-12 (commit `831f5cc`) |\n| BO-VR-004 | Sele\u00e7\u00e3o viral sem fabrica\u00e7\u00e3o de cita\u00e7\u00e3o (Lei 1 estrutural) | beats verbatim do SRT; LLM s\u00f3 escolhe \u00edndices | \u2705 **Atingido** (com contrato BYOK fechado em 2026-07-16) | `detect-viral-moments:186-233`; fix Gemini-only `a729f83` |\n| BO-VR-005 | Reusar a distribui\u00e7\u00e3o, n\u00e3o reconstru\u00ed-la | zero fn de publish nova por canal | \u2705 **Atingido** \u2014 sink `publish-space-asset`/`publish-space-carousel` reusados; \u00fanica extens\u00e3o foi a branch CAROUSEL dentro do `publish-social` existente | `publish-social:202-229` |\n| BO-VR-006 | Furar os caps de plataforma para o master grande | 1,3 GB entra pela UI | \u2705 **Atingido** \u2014 chunked 80 MB (CF 100 MB cap) + disco do host (Supabase 50 MB cap); streaming Range p/ a biblioteca | `useVideoRepurpose.ts:68`; `host-upload-server.ts`; commit `955117d` |\n| BO-VR-007 | Fechar o loop com post WordPress + legendas nativas (mapeador) | Fatia 4 shipada | \u274c **N\u00e3o atingido** \u2014 roadmap honesto (FR-VR-008 zero c\u00f3digo; OTD-VR-004 decis\u00e3o aberta) | grep FR-VR-008 em c\u00f3digo = 0 hits |\n\n---\n\n## 3. Stakeholder Register\n\n| ID | Role | Interest | Influence | Notes |\n|----|------|----------|-----------|-------|\n| SH-001 | Sovereign / Maestro (Reviewer + Owner) | High | High | Aplicou 3 migrations ao vivo e testou cada gate (2026-07-12); GO'd deploys |\n| SH-002 | Usu\u00e1rio Zero / persona Gabriel AI (Primary) | High | High | \u00danico operador do front-door (admin-only); dono do acervo GabrielAI |\n| SH-003 | Tenants futuros | Medium | Low | Seams owner-scoped prontos; fonte `local` exige hardening multi-tenant (hoje admin-only) |\n| SH-004 | Engineering (Operator) | High | Medium | 4 SOPs Lei 2 vivas (`external-video-ingest`, `video-repurpose-worker`, `repurpose-host-infra-provisioning`, `asr-master-to-srt`) |\n| SH-005 | Plataformas externas (Meta/TikTok/YouTube) | Medium | High | Auditoria de app gateia alcance; disclosure sint\u00e9tica hard-coded protege o app |\n\n---\n\n## 4. Business Requirements (status REAL)\n\n> Conven\u00e7\u00e3o: **VIVO** \u00b7 **GATED** \u00b7 **MANUAL** \u00b7 **N\u00c3O-SHIPADO**. Cada BR tra\u00e7a \u22651 MR do MRD e os FRs reais (tabela consolidada no \u00a77).\n\n| ID | Requirement | MR Traced | Priority | Status | Acceptance (real) |\n|----|-------------|-----------|----------|--------|-------------------|\n| BR-VR-001 | Master externo entra no spine `creative_assets` via CHECK aditivo `source_module='external'` \u2014 **s\u00f3 o master**; derivados (clipes/slides) registram `'hyperframes'` com `parent_asset_id`=master como modelo de proveni\u00eancia | MR-VR-001 | Critical | **VIVO** | `ingest-external-asset:131-144` (master) vs `video-repurpose-bridge.ts:106,123` (derivados). \u26a0\ufe0f corrige o blueprint \u00a7Pilar II, que afirmava derivados `'external'` |\n| BR-VR-002 | Ingest owner-scoped fail-closed: `sign_upload` com key server-forced `${uid}/`, bucket allowlist, rejei\u00e7\u00e3o de `..`; YouTube = gate **501** (`youtube_ingest_gated`, OTD-VR-001); fonte `local` = admin-only | MR-VR-001 | Critical | **VIVO** (YouTube **GATED**) | `ingest-external-asset:61-80,85-91,95-104`; smoke-external-ingest G1-G5 |\n| BR-VR-003 | Front-door host para masters grandes: upload chunked 80 MB \u2192 `host-upload-server` (loopback 3220, JWT + admin-gate `user_roles`) \u2192 `repurpose-inbox/<uid>/`; leitura com realpath-containment; streaming Range para a biblioteca | MR-VR-002 | Critical | **VIVO** (admin-only) | `host-upload-server.ts`; infra versionada `infra/systemd/{video-repurpose-bridge,host-upload}.service` + `infra/nginx/host-upload.location.conf` (caveat Lei 1: bloco nginx \u00e9 forma DERIVADA, n\u00e3o capturada do host \u2014 SOP de provisionamento) |\n| BR-VR-004 | Worker de segmenta\u00e7\u00e3o no molde `video-bridge`: claim at\u00f4mico + reaper + `finalize_video_render` + dual-write `register_creative_asset`; engine aditivo `'repurpose'` na fila `video_renders`, rail gr\u00e1tis `charged_mco=0`; guarda OTD-VR-006 no READ (bucket allowlist + prefixo `${uid}/` + no-`..` + realpath p/ inbox) | MR-VR-003 | Critical | **VIVO** | migration `20260712130000`; `video-repurpose-bridge.ts:50-56,72-93,157-159`; smoke-video-repurpose G1-G5 |\n| BR-VR-005 | Detector viral metered: 3 mco d\u00e9bito at\u00f4mico + refund em falha; sentinel pr\u00e9-d\u00e9bito; BYOK per-user fail-closed **openrouter OU gemini OU groq** (402 `ai_not_configured` s\u00f3 quando NENHUMA existe); beats verbatim do SRT | MR-VR-004 | Critical | **VIVO** | `detect-viral-moments:21,106-130` (gate `:117-122` fechado em `a729f83`); erro real = `ai_not_configured` (n\u00e3o `<provider>_not_configured` como o FRD da Fatia 6 prometia) |\n| BR-VR-006 | Vestimenta premium som-off: template alpha sem bot\u00e3o/HUD + overlay pts-sync sobre o footage reenquadrado; fallback = drawtext **byte-pad UTF-8** (nunca o filtro `subtitles=` do blueprint); `caption_mode` por clipe | MR-VR-005 | High | **VIVO** | `viral-caption-overlay-9x16.html` + `render-core.ts:359,392` + `segment-core.ts:79-118` (anticorpo `-ss/-t` multi-input `:88-90`) |\n| BR-VR-007 | Carrossel IG: slides FFmpeg puro 1080\u00d71350 (`carousel-core`, tipografia render-core **diferida** OTD-VR-007) + publica\u00e7\u00e3o **direta** `publish-space-carousel`\u2192`publish-social` (imediata) OU **agendada** via marcador `scheduled_posts.metadata.reshape.carousel_render_id` resolvido owner-scoped pelo `auto-publish` \u2014 **N\u00c3O passa por `channel_profiles`** (OTD-VR-003 segue aberta; a migration de carousel do channel_profiles \u00e9 s\u00f3 LinkedIn/PDF) | MR-VR-006 | High | **VIVO** | `carousel-core.ts:20-27,49-61`; `publish-space-carousel:57-91` (schedule) `:101-109` (imediato); `publish-social:202-229` (children\u2192parent\u2192media_publish); smoke-scheduled-carousel S1-S8 |\n| BR-VR-008 | Distribui\u00e7\u00e3o = reuso puro: derivados distribu\u00edveis pelo sink `publish-space-asset`/`space_publish_variants`; rail IG com 3 superf\u00edcies (REELS/CAROUSEL/STORIES); disclosure sint\u00e9tica hard-coded preservada | MR-VR-007 | Critical | **VIVO** | bot\u00e3o Distribuir (`VideoRepurposePage:583` \u2192 `useVideoRepurpose:187`); STORIES = Amendment 24 |\n| BR-VR-009 | Qualidade por olhar (rubrica viral) em cada criativo antes de \"pronto\" | MR-VR-009 | High | **MANUAL** | Vision QA exercido por sess\u00e3o (witnesses 12/13/14-07); loop automatizado com `vision_score`/`MAX_VIRAL_ITERS` = **zero c\u00f3digo** \u2014 FR-VR-013 permanece requisito aberto, n\u00e3o capacidade |\n| BR-VR-010 | Transcri\u00e7\u00e3o US$ 0 para master sem SRT + reconcilia\u00e7\u00e3o roteiro-autoritativa (o roteiro do GitHub \u00e9 a verdade; o \u00e1udio de IA erra nomes) | MR-VR-010 | High | **VIVO** (host-side, SOP) | whisper.cpp em `/home/ubuntu/.mcorch/asr-engine/`; SOP `asr-master-to-srt.md`; UI aceita `.srt/.vtt` por arquivo (`VideoRepurposePage:366-376`) |\n| BR-VR-011 | Mapeador metadado\u2192legenda nativa por plataforma + corpo HTML WordPress com fontes creditadas | MR-VR-008 | Medium | **N\u00c3O-SHIPADO** | Fatia 4; OTD-VR-004 (adaptar `reshape-pillar` vs mapper dedicado) decis\u00e3o nunca tomada \u2014 roadmap |\n| BR-VR-012 | Alcance p\u00fablico real nos canais | MR-VR-011 | High | **GATED** (Sovereign) | auditoria de app IG/TikTok; TikTok `SELF_ONLY` for\u00e7ado pr\u00e9-audit no publish path |\n\n---\n\n## 5. Modelo econ\u00f4mico mcoCoins (REAL \u2014 verificado no c\u00f3digo)\n\n> A doutrina do m\u00f3dulo \u00e9 **rail gr\u00e1tis** ([[feedback_opensource_first_zero_cost_equity]]): transforma\u00e7\u00e3o a US$ 0, cobran\u00e7a apenas onde h\u00e1 LLM metered. Nenhum custo abaixo \u00e9 proje\u00e7\u00e3o \u2014 todos verificados por leitura.\n\n| Operation | Coins/Run | Mec\u00e2nica | Evid\u00eancia |\n|-----------|-----------|----------|-----------|\n| Ingest do master (`ingest-external-asset`) | **0** | registro no spine, sem gera\u00e7\u00e3o | fn n\u00e3o chama `deduct_mco_coins` |\n| Enfileirar render (`video-repurpose-run`) | **0** | `charged_mco: 0` gravado na fila | `video-repurpose-run:139-141` |\n| Render de clipes/slides (worker FFmpeg) | **0** | rail gr\u00e1tis; `finalize_video_render` sem cobran\u00e7a | `video-repurpose-bridge:140-143` |\n| **Detector viral** (`detect-viral-moments`) | **3** (`DETECT_COST`) | pr\u00e9-check saldo \u2192 d\u00e9bito at\u00f4mico `deduct_mco_coins` \u2192 **refund em falha** (witnessed: JSON malformado da cascata estornou) | `detect-viral-moments:21,125-130,~250` \u00b7 \u26a0\ufe0f OTD-VR-010 **aberta**: 3 mco ainda n\u00e3o calibrado formalmente pelo modelo 4\u00d7-floor (`docs/processes/mcoin-cost-calibration.md`) |\n| ASR (whisper.cpp) | **0** (n\u00e3o bilhetado) | processo host-side por SOP, fora do ledger | `asr-master-to-srt.md` |\n| Distribuir (publish) | herda custo do canal | `publish-space-asset`/`auto-publish` \u2014 economia preexistente, n\u00e3o recobrada | reuso puro |\n| Vision QA | **0** | Vision MCP custo 0 Usu\u00e1rio Zero | `scripts/qa/vision-qa.ts` |\n\n**Custo externo (USD):** US$ 0 no rail; o detector consome a **chave BYOK do tenant** (free-tier vi\u00e1vel \u2014 Gemini/Groq/OpenRouter free models). Consistente com [[feedback_paid_byok_post_revenue]]: nenhum provider pago ativado em sil\u00eancio.\n\n---\n\n## 6. Business Risk Register\n\n| Risk ID | Description | Prob | Impact | RPN | Mitigation (real) |\n|---------|-------------|------|--------|-----|-------------------|\n| BR-RISK-VR-001 | **Alcance morto**: produzir N shorts que s\u00f3 publicam `SELF_ONLY`/privado (auditoria de app pendente) \u21d2 m\u00e1quina de volume sem audi\u00eancia | 4 | 4 | **16** | Gate declarado (MR-VR-011, a\u00e7\u00e3o Sovereign na Fila); enquanto isso o valor \u00e9 acervo pronto + prova E2E interna |\n| BR-RISK-VR-002 | **Falso-sucesso de render**: worker host stale renderiza no template errado com `done` no ledger (ffprobe/state mentem) | 3 | 4 | **12** | Anticorpo operacional: `systemctl --user restart video-bridge.service` ap\u00f3s mudar render-core/templates ([[reference_hyperframes_worker_restart]]); gate Vision \"olhe o render\" |\n| BR-RISK-VR-003 | **Cita\u00e7\u00e3o fabricada** no short (dano de marca da persona) | 2 | 5 | **10** | Estrutural: beats = \u00edndices de cues do SRT (LLM n\u00e3o escreve texto); ASR reconciliado contra roteiro-autoritativo; Vision confere |\n| BR-RISK-VR-004 | **Gap de regress\u00e3o do carrossel**: o render do `carousel-core` N\u00c3O tem smoke pr\u00f3prio (o `smoke-carousel.ts` \u00e9 do post-engine/PDF) \u2014 regress\u00e3o de slide s\u00f3 seria pega por witness manual | 3 | 3 | **9** | Registrado como gap honesto; candidato a anticorpo na 08-quality-metrics; `smoke-scheduled-carousel` cobre o seam de publish |\n| BR-RISK-VR-005 | **Single-tenant de fato**: fonte `local` + front-door admin-only; multi-tenant do caminho grande exige hardening n\u00e3o feito | 3 | 3 | **9** | Deliberado (diretiva Sovereign 2026-07-12); seams bucket-privado j\u00e1 owner-scoped p/ masters \u226450 MB |\n| BR-RISK-VR-006 | **Custo LLM runaway** no detector (master muito longo) | 2 | 3 | **6** | `MAX_CUES_SENT=500` limita tokens; d\u00e9bito fixo 3 mco; refund em falha; sentinel pr\u00e9-d\u00e9bito nunca cobra request bloqueada |\n| BR-RISK-VR-007 | **Diverg\u00eancia doc\u2194c\u00f3digo** (blueprint stale contamina decis\u00f5es futuras) | 3 | 2 | **6** | Esta su\u00edte retroativa fixa o estado real; blueprint \u00a72/\u00a7Pilar II-III rotulados como snapshot hist\u00f3rico |\n| BR-RISK-VR-008 | **Infra host fora do mesh Docker** (2 systemd units + nginx location no host) \u2014 provisionamento n\u00e3o reproduz\u00edvel por container | 2 | 3 | **6** | Infra versionada em `infra/` (commit `955117d`) + SOP `repurpose-host-infra-provisioning.md` com nota de materialidade (bloco nginx = forma derivada) |\n\n### 6.1 Ledger de OTDs (status de neg\u00f3cio)\n\n| OTD | D\u00e9bito | Status |\n|-----|--------|--------|\n| OTD-VR-001 | YouTube ingest bloqueado por IP datacenter | **Aberta (gated 501)** \u2014 probe yt-dlp confirmou o bloqueio |\n| OTD-VR-002 | Reframe subject-aware (crop din\u00e2mico) | **Aberta (deferida)** \u2014 MVP center-safe aprovado por Vision |\n| OTD-VR-003 | Surface IG-carousel no `channel_profiles` | **Aberta** \u2014 E a arquitetura shipada divergiu do plano: caminho real = `publish-space-carousel` direto (marcador `carousel_render_id`), sem `channel_profiles` |\n| OTD-VR-004 | Mapeador: adaptar reshape vs dedicado | **Aberta** \u2014 decis\u00e3o nunca tomada (Fatia 4 n\u00e3o-shipada) |\n| OTD-VR-005 | Fonte do cut-spec | **Fechada** \u2014 FR-VR-010 (detector Hormozi) |\n| OTD-VR-006 | Read-guard do worker | **Fechada** \u2014 Fatia 2 |\n| OTD-VR-007 | Tipografia pixel-perfect do slide | **Aberta** \u2014 FFmpeg drawtext conservador (`MAX_CHARS=16`); render-core HTML\u2192PNG diferido |\n| OTD-VR-008 | Beat: SRT verbatim vs rewrite | **Fechada por decis\u00e3o** \u2014 verbatim (Lei 1) |\n| OTD-VR-008b | M\u00e9tricas de creative \u2192 cut-specs | **Deferida** (p\u00f3s-1\u00aa-m\u00e9trica-real, anti-Goodhart) |\n| OTD-VR-009 | Determinismo do overlay (prova por smoke) | **Aberta** \u2014 count PNG = fps\u00d7dur sem smoke dedicado |\n| OTD-VR-010 | Calibra\u00e7\u00e3o 4\u00d7-floor do `DETECT_COST=3` | **Aberta** |\n| OTD-VR-012 | Transcript-gate (SRT no upload + ASR) | **Majoritariamente fechada** \u2014 UI sobe `.srt` + ASR vivo (o 10-frd carrega o texto stale) |\n| OTD-VR-013 | Tuning de janela do detector | **Parcialmente fechada em c\u00f3digo** \u2014 prompt endurecido 15-45s + clamp `MIN_CLIP_S=12`/`MAX_CLIP_S=90` + expans\u00e3o de janela p/ conter beats (`detect-viral-moments:196-210`) |\n\n---\n\n## 7. Registro consolidado de FRs (status REAL \u2014 a tabela \u00fanica que faltava)\n\n> FR-VR-001..009 nasceram no blueprint; FR-VR-010..015 no `10-frd-sdd-viral-quality.md`. Esta \u00e9 a vis\u00e3o consolidada com status verificado.\n\n| FR | Descri\u00e7\u00e3o | Status | Evid\u00eancia |\n|----|-----------|--------|-----------|\n| FR-VR-001 | Ingest MP4 externo owner-scoped + metadados + SRT | **VIVO** | `ingest-external-asset` + migration `20260712120000` (commit `0e4393c`) |\n| FR-VR-002 | Fallback link YouTube | **GATED (501)** | `ingest-external-asset:85-91` (OTD-VR-001) |\n| FR-VR-003 | Worker de segmenta\u00e7\u00e3o data-driven (destrava FR-CP-012) | **VIVO** | `video-repurpose-bridge` + `segment-core` (commit `439d064`) |\n| FR-VR-004 | Reframe 16:9\u21929:16 (+1:1) center-safe | **VIVO** | `segment-core.ts:62-67` (expression-crop source-agn\u00f3stico) |\n| FR-VR-005 | Queima de legenda nos shorts | **VIVO** | drawtext textfile **byte-pad UTF-8** (`segment-core:107-118`; fix `681002f`) \u2014 nunca `subtitles=` |\n| FR-VR-006 | Key-frames \u2192 slides carrossel 1080\u00d71350 | **VIVO** | `carousel-core.ts` \u2014 **FFmpeg puro** (render-core diferido OTD-VR-007); commit `831f5cc` |\n| FR-VR-007 | Branch IG `media_type=CAROUSEL` | **VIVO** | `publish-social:202-229` |\n| FR-VR-008 | Mapeador metadado\u2192legenda nativa + WordPress | **N\u00c3O-SHIPADO** | zero refs em c\u00f3digo (Fatia 4) |\n| FR-VR-009 | Fiar em publish-space-asset/publish-wordpress | **PARCIAL** | sink vivo e usado (Distribuir); alcance externo GATED (auditoria de app) |\n| FR-VR-010 | Detector de momento viral (Hormozi, BYOK fail-closed) | **VIVO \u2014 contrato FECHADO** | `detect-viral-moments`; gate aceita openrouter/gemini/groq desde `a729f83` (2026-07-16); erro real `ai_not_configured` 402 |\n| FR-VR-011 | Compositing motion-graphic alpha | **VIVO** | `renderAlphaFrames` (`render-core:359,392`) + overlay (`segment-core:79-103`) |\n| FR-VR-012 | Template sofisticado \"sem bot\u00e3o\" | **VIVO** | `viral-caption-overlay-9x16.html` (transparente, Montserrat, textContent XSS-safe) |\n| FR-VR-013 | Loop Vision-gated de qualidade | **MANUAL** | zero c\u00f3digo (`MAX_VIRAL_ITERS`/`vision_score` = 0 hits); rubrica exercida por sess\u00e3o |\n| FR-VR-014 | `caption_mode` por clipe (beats/drawtext/none) | **VIVO** | ClipSpec sanitizado em `video-repurpose-run:33-74` |\n| FR-VR-015 | UI \"Gerar cortes virais\" 1-clique | **VIVO** | `VideoRepurposePage:142-165` (progresso ancorado em sinais reais) |\n\n---\n\n## 8. Business Acceptance Criteria (verificados)\n\n| ID | Criterion | Verification (real) |\n|----|-----------|---------------------|\n| BAC-VR-001 | Master real de produ\u00e7\u00e3o processado E2E | EP01 1,3 GB \u2192 5 shorts 9:16 (Vision QA 2026-07-13, n\u00f3 `9f7b191a`) |\n| BAC-VR-002 | Shorts virais E2E com scores | 3 shorts (9.0/9.5/8.5; Vision 7-8/10, n\u00f3 `d98767ea`) |\n| BAC-VR-003 | Carrossel E2E | 3 slides 1080\u00d71350 registrados + Vision no slide real (n\u00f3 `f050959c`) |\n| BAC-VR-004 | Rail a custo 0 | `charged_mco=0` na fila; FFmpeg/whisper self-host |\n| BAC-VR-005 | Nenhuma migration sem `/security-review` | NO FINDINGS \u00d710 acumulado nas 3 sess\u00f5es (HANDOFF seals) |\n| BAC-VR-006 | Anticorpos re-execut\u00e1veis | 3 smokes do m\u00f3dulo (`smoke-external-ingest`, `smoke-video-repurpose`, `smoke-scheduled-carousel`); gap declarado: sem smoke do render do carousel-core |\n| BAC-VR-007 | Tenant nunca bloqueado indevidamente no detector | Gemini-only destrava desde `a729f83` (gate = `openRouterKey || groqKey || geminiKey`) |\n\n---\n\n## 9. Traceability Matrix\n\n| MR ID | BR ID | FR real | OTD / FM | Status |\n|-------|-------|---------|----------|--------|\n| MR-VR-001 | BR-VR-001, BR-VR-002 | FR-VR-001, FR-VR-002 | OTD-VR-001; FM-VR-01 | VIVO (YouTube gated) |\n| MR-VR-002 | BR-VR-003 | (front-door \u2014 FRs de infra, sela na FRD) | FM-VR-04 | VIVO admin-only |\n| MR-VR-003 | BR-VR-004, BR-VR-006 | FR-VR-003, FR-VR-004, FR-VR-005 | OTD-VR-002/006; FM-VR-02 | VIVO |\n| MR-VR-004 | BR-VR-005 | FR-VR-010 | OTD-VR-005 (fechada), OTD-VR-010/013; FM-VR-Q1/Q4 | VIVO (contrato fechado `a729f83`) |\n| MR-VR-005 | BR-VR-006 | FR-VR-011, FR-VR-012, FR-VR-014 | OTD-VR-008 (fechada), OTD-VR-009; FM-VR-Q2/Q5 | VIVO |\n| MR-VR-006 | BR-VR-007 | FR-VR-006, FR-VR-007 | OTD-VR-003 (aberta \u2014 caminho real diverge), OTD-VR-007; FM-VR-03 | VIVO |\n| MR-VR-007 | BR-VR-008 | FR-VR-009 (parcial), FR-VR-015 | FM-VR-05 | VIVO / gate externo |\n| MR-VR-008 | BR-VR-011 | FR-VR-008 | OTD-VR-004 | N\u00c3O-SHIPADO |\n| MR-VR-009 | BR-VR-009 | FR-VR-013 | FM-VR-Q3 | MANUAL |\n| MR-VR-010 | BR-VR-010 | (ASR \u2014 SOP-driven) | OTD-VR-012 (maj. fechada) | VIVO |\n| MR-VR-011 | BR-VR-012 | FR-VR-009 (gate) | \u2014 | GATED Sovereign |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent \u2014 su\u00edte retroativa fiel ao c\u00f3digo vivo (Lei 1: pointers re-verificados por leitura pr\u00f3pria 2026-07-16; economia mcoCoins lida do c\u00f3digo, n\u00e3o projetada; drifts do blueprint corrigidos por escrito nos BRs; FR-VR-010 registrado como FECHADO pelo commit `a729f83`)._\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-repurpose/02-brd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:00:27)*


## 🤖 Claude *(16:00:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"Agendar\\|carrossel\\|Carrossel\\|Distribuir\\|Gerar cortes\" src/pages/VideoRepurposePage.tsx | head -20 && grep -n \"publish-space-carousel\\|schedule\" src/hooks/useVideoRepurpose.ts | head",
  "description": "Verify carousel/distribute UI labels in VideoRepurposePage"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 105:      if (error) throw new Error(await edgeErrorMessage(error, 'Falha ao agendar carrossel'));
> 108:      toast.success(`Carrossel agendado (${data?.slides ?? slides.length} slides) — o auto-publish cuida do resto.`);
> 281:            1 master 16:9 → N shorts verticais legendados + carrossel. Rail FFmpeg grátis (US$ 0).
> 358:              <label className="text-xs text-muted-foreground">@handle (carrossel IG, opcional)</label>
> 399:                  <Sparkles className="h-4 w-4 text-primary" /> Gerar cortes virais (IA)
> 424:                {viral && !viral.done ? 'Gerando…' : 'Gerar cortes'}
> 448:              <Images className="h-4 w-4" /> Carrossel IG
> 522:            Registrar & gerar {mode === 'carousel' ? 'carrossel' : 'cortes'}
> 542:              {/* OTD-SPACES-044 — carrossel publica como UM post IG (todos os slides), não por-slide. */}
> 546:                    Carrossel Instagram · {(results.data ?? []).length} slides
> 553:                      Agendar carrossel
> 559:                  (Modo carrossel: os slides individuais ficam ocultos — o post é o conjunto.) */}
> 585:                        Distribuir
> 179:// publish-space-asset resolves the asset SERVER-SIDE owner-scoped and enqueues scheduled_posts (auto-publish drives it).
> 182:    { ok?: boolean; variant_id?: string; scheduled_post_id?: string },
> ```

## 🤖 Claude *(16:00:36)*


## 🤖 Claude *(16:02:10)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-repurpose/03-prd.md",
  "content": "# PRD \u2014 Product Requirements Document\n\n**Project:** video-repurpose (1 master externo \u2192 N shorts 9:16 + carrossel IG)\n**Version:** v1.0 (retroativa) | **Date:** 2026-07-16\n**BoK Applied:** ProdBOK + CXBOK sobre estado shipado\n**Status:** Selada \u2014 retroativa\n**Source of truth:** c\u00f3digo vivo + [`01-mrd.md`](01-mrd.md) + [`02-brd.md`](02-brd.md).\n\n> Su\u00edte retroativa \u2014 consolida m\u00f3dulo J\u00c1 SHIPADO; ground truth = c\u00f3digo vivo + auditoria wf_2998d4c7\n>\n> As jornadas abaixo descrevem **superf\u00edcies que existem e foram operadas** (Usu\u00e1rio Zero, produ\u00e7\u00e3o real), n\u00e3o fluxos planejados. Onde a UI diverge do blueprint/FRD hist\u00f3rico, vale a UI \u2014 cada label citado foi verificado por leitura de `src/pages/VideoRepurposePage.tsx` em 2026-07-16.\n\n> **ORO triplet:** Operator = MCORCH Master Execution Agent \u00b7 Reviewer = Sovereign + Vision QA ocular \u00b7 Owner = Sovereign (alcance p\u00fablico gated em auditoria de app).\n\n---\n\n## 1. Product Vision Statement\n\n> Para o **Usu\u00e1rio Zero operando a persona Gabriel AI/CCIO** (e futuros tenants com acervo de v\u00eddeo longo), o **Repurpose de V\u00eddeo** \u00e9 a superf\u00edcie `/dashboard/repurpose` que transforma **1 document\u00e1rio master** em **N shorts verticais virais + 1 carrossel IG** com **1 clique**, a **custo de render US$ 0** \u2014 selecionando os melhores momentos pelo SRT falado (sem fabricar cita\u00e7\u00e3o), vestindo-os com motion-graphic premium e entregando derivados prontos para a distribui\u00e7\u00e3o que o MCORCH j\u00e1 opera. Diferente de ferramentas de clipping avulsas, o derivado nasce `creative_assets` e \u00e9 distribu\u00edvel/agend\u00e1vel pelos mesmos trilhos que medem receita.\n\n---\n\n## 2. User Personas\n\n### Persona 1 \u2014 Usu\u00e1rio Zero / Sovereign (Primary \u2014 \u00fanico operador real hoje)\n\n| Attribute | Detail |\n|-----------|--------|\n| Role | Admin do MCORCH; dono do acervo GabrielAI; rosto da persona de marca Gabriel AI/CCIO |\n| Goals | Subir o master (1,3 GB) pela UI, gerar cortes virais com 1 clique, ver progresso real (n\u00e3o % fabricado), distribuir/agendar sem sair da p\u00e1gina |\n| Frustrations resolvidas | Cap de 50 MB do Supabase free e 100 MB/request do Cloudflare (resolvidos: host-disk + chunked 80 MB); yt-dlp bloqueado (aceito: upload direto); legenda truncada UTF-8 (corrigida: byte-pad); tenant Gemini-only rejeitado no detector (corrigido `a729f83`) |\n| Tech-savviness | 5 (Lead Architect) |\n| Acesso | Rota `adminOnly` \u2014 item \"Repurpose de V\u00eddeo\" (\u00edcone Scissors) em `DashboardSidebar.tsx:83`; rota `/dashboard/repurpose` (`App.tsx:132`) |\n| Quote | _\"Quero que o epis\u00f3dio j\u00e1 pago vire a semana inteira de conte\u00fado \u2014 e quero VER cada corte antes de ir a p\u00fablico.\"_ |\n\n### Persona 2 \u2014 Tenant futuro (Secondary \u2014 parcialmente servido)\n\n| Attribute | Detail |\n|-----------|--------|\n| Role | Criador com acervo de v\u00eddeo longo pr\u00f3prio |\n| O que j\u00e1 funciona para ele | Seams owner-scoped (`ingest-external-asset` via `sign_upload` key-forced `${uid}/`, detector com a pr\u00f3pria chave BYOK, worker tenant-safe via OTD-VR-006) para masters \u226450 MB em bucket privado |\n| O que N\u00c3O funciona ainda | Fonte `local` (masters grandes) \u00e9 admin-only por diretiva Sovereign 2026-07-12; a p\u00e1gina inteira \u00e9 nav `adminOnly` \u2014 abrir a superf\u00edcie para tenants \u00e9 hardening futuro, n\u00e3o promessa desta su\u00edte |\n\n---\n\n## 3. User Journeys (superf\u00edcies REAIS shipadas)\n\n### Journey 1 \u2014 \"Gerar cortes virais\" com 1 clique (FR-VR-015, o caminho principal)\n\n| Stage | Action | Touchpoint real | Emotion | Notes |\n|-------|--------|-----------------|---------|-------|\n| Preparo | Arrasta o master MP4 (at\u00e9 1,3 GB provado) no dropzone; XHR chunked 80 MB com progresso de upload | Card \"1. Enviar o master\" \u2192 `host-upload-server` (3220) \u2192 `repurpose-inbox/<uid>/` | \ud83d\ude10\u2192\ud83d\ude0a | Fura o cap de 100 MB do CF por chunk (`useVideoRepurpose.ts:68`); JWT + admin-gate server-side |\n| Transcri\u00e7\u00e3o | Clica \"Subir arquivo .srt\" (aceita `.srt/.vtt`) OU \u2014 sem SRT \u2014 roda o ASR whisper.cpp pelo SOP host-side | input file (`VideoRepurposePage:366-376`); badge SRT honesto (verdade do servidor via `useMasterSrtStatus`) | \ud83e\udd14 | Badge l\u00ea `metadata.srt` do master ingerido (RLS own) \u2014 nunca estado local fingido |\n| 1 clique | Clica **\"Gerar cortes virais (IA)\"** \u2014 ingest (se preciso) \u2192 detector \u2192 enqueue dos beats-clips | bot\u00e3o `:399`; `doViralCuts` (`:142-165`) | \ud83d\ude0a | Custo vis\u00edvel: s\u00f3 o detector cobra (3 mco); render gr\u00e1tis |\n| Progresso | Barra + tail de log de linha \u00fanica avan\u00e7am por **sinais reais**: resposta do detector \u2192 estado `video_renders` (queued/running/done) \u2192 contagem de `creative_assets` filhos por clipe | painel de progresso (`:394-425`) | \ud83d\ude80 | Lei 1 na UI: nunca % fabricado |\n| Resultado | Shorts 9:16 aparecem em Resultados; cada um com bot\u00e3o **\"Distribuir\"** | `:585` \u2192 `publish-space-asset` (surface `video`) | \u2764\ufe0f | Derivado nasce `creative_assets` (`source_module='hyperframes'`, `parent_asset_id`=master) |\n\n#### Edge cases reais (comportamento verificado)\n- **Sem SRT no master** \u2192 detector responde `422 no_transcript` (toast pt-BR); o badge SRT j\u00e1 avisava antes do clique.\n- **Sem chave de IA** \u2192 `402 ai_not_configured` + action \"Configure sua chave de IA em /dashboard/settings\". Desde `a729f83` (2026-07-16), tenant com **apenas** `google_api_key` (Gemini) **destrava** \u2014 o gate \u00e9 `openrouter OU groq OU gemini`, honrando o contrato FR-VR-010 (antes, Gemini-only tomava 402 indevido).\n- **Saldo < 3 mco** \u2192 `402 Saldo insuficiente de mcoCoins` (pr\u00e9-check antes do d\u00e9bito at\u00f4mico).\n- **LLM devolve JSON malformado** \u2192 guard de parse **estorna os 3 mco** (witnessed em prod 2026-07-13).\n- **N\u00e3o-admin com fonte host** \u2192 `403 admin_only` (duplo gate: ingest E run).\n- **Link YouTube** \u2192 `501 youtube_ingest_gated` com instru\u00e7\u00e3o de upload (OTD-VR-001).\n\n### Journey 2 \u2014 Carrossel IG (modo `carousel`)\n\n| Stage | Action | Touchpoint real | Notes |\n|-------|--------|-----------------|-------|\n| Configura | Alterna para o modo \"Carrossel IG\" (`:448`); opcional: `@handle` (`:358`) e captions por slide `{t_sec, caption}` | UI do card de composi\u00e7\u00e3o | Slides = key-frames dos cap\u00edtulos/atos do epis\u00f3dio |\n| Gera | Clica **\"Registrar & gerar carrossel\"** (`:522`) \u2192 `video-repurpose-run` (mode `carousel`) \u2192 worker `carousel-core` | fila `video_renders` engine `repurpose`, `charged_mco=0` | Slides **FFmpeg puro** 1080\u00d71350 4:5; wrap conservador `MAX_CHARS=16` (OTD-VR-007 \u2014 tipografia render-core diferida) |\n| Publica J\u00c1 | (caminho imediato) `publish-space-carousel` resolve os slides **owner-scoped por `source_job_id`**, assina URLs 6h e chama `publish-social` direto | `publish-space-carousel:101-109` \u2192 branch CAROUSEL (`publish-social:202-229`: children `is_carousel_item` \u2192 parent `media_type=CAROUSEL` \u2192 `media_publish`) | O post \u00e9 **UM** post IG com todos os slides (OTD-SPACES-044) \u2014 os slides individuais ficam ocultos nos Resultados (`:542-559`) |\n| OU Agenda | Clica **\"Agendar carrossel\"** (`:553`) \u2192 enfileira em `scheduled_posts` o **marcador de grupo** `metadata.reshape.carousel_render_id` (channel `instagram`, surface `carousel`); o `auto-publish` resolve + re-assina na hora do publish | `publish-space-carousel:57-91`; toast \"Carrossel agendado (N slides) \u2014 o auto-publish cuida do resto.\" | Anti double-enqueue: `409 already_queued` por render/user; `422 carousel_needs_2_slides` se <2 |\n\n> \u26a0\ufe0f **Arquitetura real (corrige o blueprint):** o carrossel **n\u00e3o passa por `channel_profiles`** \u2014 OTD-VR-003 segue aberta. O caminho vivo \u00e9 `publish-space-carousel` \u2192 `publish-social`, com o modo agendado via marcador `carousel_render_id` (Amendment 22 do spaces). A migration de carousel do `channel_profiles` (`20260628120000`) permanece s\u00f3 LinkedIn/PDF.\n\n### Journey 3 \u2014 Cut-spec manual (modo `repurpose` sem detector)\n\nO operador pode autorar os clipes \u00e0 m\u00e3o (`{in_sec, out_sec, reframe 9:16|1:1, caption}`) e clicar \"Registrar & gerar cortes\" \u2014 o caminho original das Fatias 1-2, ainda vivo, com legenda drawtext byte-pad. O detector (Journey 1) \u00e9 a evolu\u00e7\u00e3o, n\u00e3o a substitui\u00e7\u00e3o: `caption_mode` por clipe (`beats`/`drawtext`/`none`) decide a vestimenta (FR-VR-014).\n\n### Journey 4 \u2014 Qualidade por olhar (processo MANUAL \u2014 n\u00e3o \u00e9 feature de UI)\n\nO gate \"olhe o render\" \u00e9 exercido **por sess\u00e3o** com Vision QA (rubrica viral: hook-2s, legibilidade som-off, ritmo, reenquadre) \u2014 [[feedback_vision_qa_always]]. **N\u00e3o existe** loop automatizado com `vision_score`/limiar/itera\u00e7\u00e3o na UI ou no worker (FR-VR-013 = zero c\u00f3digo). Um bot\u00e3o \"avaliar com Vision\" \u00e9 candidato de roadmap, n\u00e3o capacidade atual.\n\n---\n\n## 4. Feature Inventory (MoSCoW retroativo \u2014 com status REAL)\n\n### Shipped (o MVP que j\u00e1 existe)\n\n| ID | Feature | Persona | BR Traced | FR | Status | Evid\u00eancia |\n|----|---------|---------|-----------|-----|--------|-----------|\n| PR-VR-001 | P\u00e1gina `/dashboard/repurpose` (nav adminOnly, \u00edcone Scissors) | P1 | BR-VR-003 | FR-VR-015 | **VIVO** | `App.tsx:132`; `DashboardSidebar.tsx:83`; `VideoRepurposePage.tsx` (602 linhas) |\n| PR-VR-002 | Dropzone chunked 80 MB \u2192 disco do host (masters grandes) + streaming Range p/ a biblioteca | P1 | BR-VR-003 | \u2014 (infra) | **VIVO** (admin) | `useVideoRepurpose.ts:68`; `host-upload-server.ts` GET `/api/host-media` (206); commit `955117d` |\n| PR-VR-003 | Upload de SRT por arquivo + badge SRT honesto (server-truth) | P1, P2 | BR-VR-010 | FR-VR-001 | **VIVO** | `VideoRepurposePage:366-376`; `useMasterSrtStatus` (`useVideoRepurpose:200-210`) |\n| PR-VR-004 | Bot\u00e3o \"Gerar cortes virais (IA)\" 1-clique com progresso ancorado em sinais reais | P1 | BR-VR-005 | FR-VR-015, FR-VR-010 | **VIVO** | `doViralCuts` (`:142-165`); janela-alvo 15-45s no prompt, clamp 12-90s na valida\u00e7\u00e3o |\n| PR-VR-005 | Shorts motion-graphic sem bot\u00e3o (beats verbatim) com fallback drawtext | P1 | BR-VR-006 | FR-VR-011/012/014 | **VIVO** | template alpha + overlay; 3 shorts E2E provados |\n| PR-VR-006 | Modo Carrossel IG (gerar + publicar j\u00e1 + agendar) | P1 | BR-VR-007 | FR-VR-006/007 | **VIVO** | Journey 2; smoke-scheduled-carousel S1-S8 |\n| PR-VR-007 | Bot\u00e3o \"Distribuir\" por short \u2192 fila de distribui\u00e7\u00e3o existente | P1 | BR-VR-008 | FR-VR-009 | **VIVO** | `:585` \u2192 `publish-space-asset` |\n| PR-VR-008 | Cut-spec manual (clipes \u00e0 m\u00e3o) | P1, P2 | BR-VR-004 | FR-VR-003/004/005 | **VIVO** | Journey 3 |\n\n### Not shipped / gated (roadmap honesto \u2014 nada abaixo \u00e9 capacidade)\n\n| ID | Feature | Status | Gate |\n|----|---------|--------|------|\n| PR-VR-020 | Mapeador metadado\u2192legenda nativa + post WordPress com fontes creditadas | **N\u00c3O-SHIPADO** | Fatia 4; decis\u00e3o OTD-VR-004 pendente |\n| PR-VR-021 | Loop Vision automatizado (score/limiar/itera\u00e7\u00e3o na UI ou worker) | **N\u00c3O-SHIPADO** (processo manual vivo) | FR-VR-013 aberto |\n| PR-VR-022 | Ingest por link YouTube | **GATED (501)** | OTD-VR-001 (IP datacenter) |\n| PR-VR-023 | Alcance p\u00fablico IG/TikTok | **GATED** | Auditoria de app \u2014 a\u00e7\u00e3o Sovereign |\n| PR-VR-024 | Superf\u00edcie para tenants n\u00e3o-admin (masters grandes) | **N\u00c3O-SHIPADO** | Hardening multi-tenant do front-door host |\n| PR-VR-025 | Reframe subject-aware (crop din\u00e2mico) | **N\u00c3O-SHIPADO** | OTD-VR-002 (center-safe aprovado por Vision) |\n\n---\n\n## 5. UX real (o que est\u00e1 na tela)\n\n- **Marca MIV:** a p\u00e1gina segue os tokens do dashboard (void/cyan; custo em contexto de valor). Header: \"1 master 16:9 \u2192 N shorts verticais legendados + carrossel. Rail FFmpeg gr\u00e1tis (US$ 0).\" (`:281`) \u2014 o custo zero \u00e9 comunicado na pr\u00f3pria superf\u00edcie.\n- **Toasts (`sonner`, pt-BR):** \"Carrossel agendado (N slides) \u2014 o auto-publish cuida do resto.\" \u00b7 \"Falha ao agendar carrossel\" \u00b7 \"Falha ao ler o arquivo SRT\" \u00b7 erros de edge fn extra\u00eddos por `edgeErrorMessage` (`src/lib/edge.ts`).\n- **Progresso Lei 1:** a barra do run viral s\u00f3 avan\u00e7a em evento material (detector respondeu / render mudou de estado / filho registrado) \u2014 nunca timer decorativo.\n- **Resultados por modo:** modo carrossel mostra o **conjunto** (\"Carrossel Instagram \u00b7 N slides\") com a\u00e7\u00f5es \"Publicar j\u00e1\"/\"Agendar carrossel\"; modo cortes lista cada short com \"Distribuir\".\n- **Acessibilidade/idioma:** UI 100% pt-BR (c\u00f3digo/logs em ingl\u00eas, conven\u00e7\u00e3o MCORCH).\n\n---\n\n## 6. Acceptance Criteria (Gherkin \u2014 comportamento real verificado)\n\n```gherkin\nFeature: Gerar cortes virais (Journey 1)\n\n  Scenario: 1 clique do master ao short motion-graphic\n    Given um master ingerido com metadata.srt (badge SRT ativo)\n    When o admin clica \"Gerar cortes virais (IA)\"\n    Then detect-viral-moments debita 3 mcoCoins atomicamente e retorna top-3 clipes com beats = cues verbatim do SRT\n    And video-repurpose-run enfileira video_renders engine='repurpose' com charged_mco=0\n    And o worker registra cada short como creative_assets source_module='hyperframes' com parent_asset_id = master\n    And a barra de progresso avan\u00e7a apenas por sinais reais (detector \u2192 estado do render \u2192 filhos registrados)\n\n  Scenario: Tenant Gemini-only destrava o detector (contrato FR-VR-010 \u2014 fechado em a729f83)\n    Given um tenant cujo decrypted_user_api_keys tem APENAS google_api_key\n    When ele dispara o detector\n    Then o gate aceita a chave (openrouter OU groq OU gemini) e o dispatch usa o endpoint OpenAI-compat do Gemini\n    And nenhum 402 ai_not_configured \u00e9 retornado\n\n  Scenario: Falha do LLM n\u00e3o custa nada ao tenant\n    Given o d\u00e9bito de 3 mco j\u00e1 efetuado\n    When a cascata LLM devolve JSON malformado ou HTTP de erro\n    Then o refund credita os 3 mco de volta (witnessed 2026-07-13)\n\nFeature: Carrossel IG (Journey 2)\n\n  Scenario: Agendar carrossel como UM post\n    Given um render de carrossel done com \u22652 slides owner-scoped\n    When o admin clica \"Agendar carrossel\"\n    Then scheduled_posts recebe o marcador metadata.reshape.carousel_render_id (channel instagram, surface carousel)\n    And um segundo clique retorna 409 already_queued\n    And o auto-publish resolve os slides owner-scoped e publica via a branch CAROUSEL do publish-social\n    And o fluxo N\u00c3O consulta channel_profiles (OTD-VR-003 permanece aberta)\n\n  Scenario: Carrossel com menos de 2 slides\n    When publish-space-carousel resolve <2 slides para o render\n    Then retorna 422 carousel_needs_2_slides\n\nFeature: Gates fail-closed do ingest\n\n  Scenario: Link YouTube\n    When o caller pede provider=youtube\n    Then 501 youtube_ingest_gated com instru\u00e7\u00e3o de upload (OTD-VR-001)\n\n  Scenario: N\u00e3o-admin com fonte do host\n    When um user sem role admin tenta ingerir/rodar bucket local\n    Then 403 admin_only (gate duplo: ingest E run)\n\n  Scenario: Key adulterada\n    When storage_key n\u00e3o come\u00e7a com ${uid}/ ou cont\u00e9m \"..\"\n    Then 400 source_ref_invalid (e o worker re-valida no READ \u2014 OTD-VR-006)\n```\n\n---\n\n## 7. Traceability Matrix\n\n| MR ID | BR ID | PR ID | FR real | Status |\n|-------|-------|-------|---------|--------|\n| MR-VR-001 | BR-VR-001/002 | PR-VR-003 | FR-VR-001, FR-VR-002 | VIVO (YouTube gated) |\n| MR-VR-002 | BR-VR-003 | PR-VR-001/002 | \u2014 (infra) | VIVO admin-only |\n| MR-VR-003 | BR-VR-004/006 | PR-VR-005/008 | FR-VR-003/004/005/011/012/014 | VIVO |\n| MR-VR-004 | BR-VR-005 | PR-VR-004 | FR-VR-010 | VIVO (contrato fechado `a729f83`) |\n| MR-VR-006 | BR-VR-007 | PR-VR-006 | FR-VR-006/007 | VIVO |\n| MR-VR-007 | BR-VR-008 | PR-VR-007 | FR-VR-009 (parcial), FR-VR-015 | VIVO / alcance gated |\n| MR-VR-008 | BR-VR-011 | PR-VR-020 | FR-VR-008 | N\u00c3O-SHIPADO |\n| MR-VR-009 | BR-VR-009 | PR-VR-021 | FR-VR-013 | MANUAL |\n| MR-VR-010 | BR-VR-010 | PR-VR-003 | (ASR SOP) | VIVO |\n| MR-VR-011 | BR-VR-012 | PR-VR-023 | \u2014 | GATED Sovereign |\n\n---\n\n_Generated by MCORCH BoK Scribe Agent \u2014 su\u00edte retroativa fiel ao c\u00f3digo vivo (Lei 1: labels de UI e comportamentos citados verificados por leitura de `VideoRepurposePage.tsx`/`useVideoRepurpose.ts` em 2026-07-16; jornadas descrevem produ\u00e7\u00e3o real, n\u00e3o prot\u00f3tipo; roadmap segregado explicitamente do shipado)._\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-repurpose/03-prd.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:02:31)*


## 🤖 Claude *(16:02:31)*


## 🤖 Claude *(16:02:42)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "files_written": [
    "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-repurpose/01-mrd.md",
    "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-repurpose/02-brd.md",
    "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/video-repurpose/03-prd.md"
  ],
  "notes": "Su\u00edte retroativa 01-03 do video-repurpose escrita fiel ao c\u00f3digo vivo (auditoria wf_2998d4c7). Todos os pointers file:line re-verificados por leitura pr\u00f3pria em 2026-07-16 (ingest-external-asset, video-repurpose-run, detect-viral-moments, publish-space-carousel, video-repurpose-bridge, carousel-core, VideoRepurposePage, useVideoRepurpose, App.tsx, DashboardSidebar). Corre\u00e7\u00f5es obrigat\u00f3rias do audit incorporadas: derivados='hyperframes' (s\u00f3 master='external'); carrossel fora de channel_profiles (OTD-VR-003 aberta, caminho real publish-space-carousel\u2192publish-social + carousel_render_id); slides FFmpeg puro (OTD-VR-007); drawtext byte-pad (n\u00e3o subtitles=); erro real ai_not_configured; rail IG 3 superf\u00edcies; commit 955117d na traceabilidade; gap honesto do smoke do carousel-core (3 smokes, n\u00e3o 4); FR-VR-010 Gemini-only documentado como FECHADO por a729f83 (verificado vivo: gate = openRouterKey||groqKey||geminiKey). Status REAL selado: MRs/BRs/PRs com vivo/gated/manual/n\u00e3o-shipado + tabela consolidada FR-VR-001..015 (02-brd \u00a77) + ledger OTD-VR (02-brd \u00a76.1) + economia mcoCoins lida do c\u00f3digo (DETECT_COST=3, charged_mco=0, OTD-VR-010 calibra\u00e7\u00e3o aberta). Forma calibrada pela su\u00edte spaces-cadence 9/9. Racional de neg\u00f3cio ancorado na intro do blueprint + HANDOFF (persona Gabriel AI/CCIO, motor 2 m\u00e1quinas, doutrina USD-0, GabrielAI como fonte do master). Nota menor: detectei MIN_CLIP_S=12/MAX_CLIP_S=90 no c\u00f3digo vs \"15-45s\" do prompt \u2014 registrado como janela-alvo 15-45s com clamp 12-90 no PRD (OTD-VR-013 parcialmente fechada)."
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
> * **Sessão Anterior**: [[2026-07-16 - agent-ae88d67e696ff8fd7]]
> * **Próxima Sessão**: [[2026-07-16 - agent-aec44318bddbe695f]]
%% --- TIMELINE END --- %%

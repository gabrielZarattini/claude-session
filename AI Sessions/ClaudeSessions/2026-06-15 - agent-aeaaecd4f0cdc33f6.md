# Session agent-aeaaecd4f0cdc33f6
**Date:** 2026-06-15 | **Session ID:** `agent-aeaaecd4f0cdc33f6`

---

## 👤 User *(18:49:45)*

You are determining WHAT `deepsearch.run` actually DOES — the "google/gemini grounded research half" of the Vision MCP deepsearch surface (distinct from `deepsearch.scrape` which is Firecrawl single-URL). Be rigorous: report only what the sealed BoK specifies; flag everything underspecified as a candidate OTD (Lei 2 — never improvise).

Read:
- /home/gcrUX/htdocs/constellation-orchestra/docs/bok/vision-mcp/00-deepsearch-blueprint.md — the "Cognitive"/deepsearch pillar; what grounded research means here; any provider named (Gemini grounding / Google Search grounding / google CSE).
- /home/gcrUX/htdocs/constellation-orchestra/docs/bok/vision-mcp/03-prd.md — PR-VM-013 (and neighbors) for the deepsearch.run product behavior.
- /home/gcrUX/htdocs/constellation-orchestra/docs/bok/vision-mcp/01-mrd.md — the market/job-to-be-done for deepsearch.run.
- /home/gcrUX/htdocs/constellation-orchestra/docs/bok/vision-mcp/04-frd.md — re-read FR-VM-007 + the tool spec for what a "unit" is (planned_units) and the result shape.
- Cross-check how the EXISTING repo does grounded deep research: /home/gcrUX/htdocs/constellation-orchestra/docs/processes/deepsearch-blueprint.md and any deep-research skill, to see what "units" naturally map to (search fronts? sources? sub-queries?).

Determine, with sources:
1. The provider + API for the grounded-research leg (Gemini with Google Search grounding? raw Google API? Is the key 'gemini_api_key' per-user — confirm it's a column in user_api_keys).
2. What ONE `unit` is (so planned_units + partial-delivery has concrete meaning).
3. The result payload contents (citations? synthesized report? per the FRD poll `result` field).
4. How partial delivery physically happens (some units fail → partial).

Return the structured map. open_questions = every place the provider/unit/result is NOT pinned by the BoK (these become OTDs for the design, not guesses).

## 🤖 Claude *(18:49:49)*

I'll research the Vision MCP deepsearch surface, focusing on `deepsearch.run`. Let me read the relevant BoK documents.

## 🤖 Claude *(18:49:50)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/vision-mcp/00-deepsearch-blueprint.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> <system-reminder>[Truncated: PARTIAL view — showing lines 1-257 of 533 total (44045 tokens, cap 25000). Call Read with offset=258 limit=257 for the next page, or Grep to find a specific section. Do NOT answer from this page alone if the answer may be further in the file.]</system-reminder>
> 
> 1	# 🧠 MCORCH Vision MCP — Percepção de Essência Humana
> 2	
> 3	**Blueprint DeepSearch · SEED / Fonte da Verdade para `/bok-scribe`**
> 4	`docs/bok/vision-mcp/00-deepsearch-blueprint.md` · slug `vision-mcp` · v0.2.0 (2026-06-11)
> 5	> **Changelog v0.2.0** — adiciona Pilar V Computação Cognitiva + vertical Tecnologia Assistiva; Computação Neuromórfica confirmada já coberta no Pilar III.
> 6	
> 7	> **Natureza deste documento.** Este é o artefato-semente (precedente: `docs/bok/security/00-deepsearch-blueprint.md`, que sedimentou a suíte Cyber-Sentinel de 4 docs). Ele NÃO é código nem especificação final — é a **Fonte da Verdade fundamentada em deepsearch** que destrava o **Closed-Loop Protocol** do MCORCH Master Execution Protocol (CLAUDE.md §1): com este blueprint consolidado e revisado, o Sovereign pode rodar `/bok-scribe vision-mcp` para gerar MRD → BRD → PRD → FRD → SDD. Nenhuma linha de código de `vision-mcp` deve ser escrita antes dessa suíte existir.
> 8	>
> 9	> **ORO triplet deste blueprint** — Operator: MCORCH Master Execution Agent (autoria do seed) · Reviewer: Sovereign (Gabriel) · Owner: Sovereign até v6.4.0 (blast radius = primeiro serviço tenant-facing fora do gateway Supabase + corpus de referências redistribuído).
> 10	>
> 11	> **Materialidade (Lei 1).** Toda afirmação externa carrega sua URL-fonte da pesquisa. Afirmações refutadas pela verificação adversarial NÃO aparecem como fato (usa-se a versão corrigida); afirmações não-verificáveis são marcadas como tal (`⚠️ não-verificado`). Referências de repositório foram materialmente confirmadas nesta sessão (`packages/gitnexus-core/src/mcp/server.ts`, `docker-compose.yml`, `docs/processes/mcoin-cost-calibration.md`, `docs/processes/edge-jwt-identity-verification.md`, `supabase/functions/_shared/sentinel.ts`, `supabase/migrations/20260603000000_marketing_hub_lead_core.sql`).
> 12	
> 13	---
> 14	
> 15	## 1. Sumário Executivo
> 16	
> 17	### O que é
> 18	
> 19	O **Vision MCP** é um servidor **Model Context Protocol nativo do MCORCH** que expõe uma camada de **percepção visual + deepsearch fundamentado** tanto para os agentes internos (Pantheon: engineer/scientist/artisan/marketing-growth) quanto para **ecossistemas externos** (Claude Desktop/Code, VS Code, ChatGPT/connector, Claude API), via um endpoint remoto **Streamable HTTP + OAuth 2.1**. Ele transforma imagem, vídeo, captura de tela e páginas web em (a) descrições/detecções/segmentações/OCR estruturados e (b) **referências de mercado consolidadas** extraídas por deepsearch e gravadas na Knowledge Mesh.
> 20	
> 21	A arquitetura de produto é desenhada sobre uma metáfora biológica defensável — a **"Essência Humana"**: uma periferia barata, always-on, inspirada em princípios neuromórficos emulados em software (detecção de mudança/saliência) que **dispara** uma análise foveal cara e profunda apenas quando há sinal — exatamente como a retina humana concentra ~5% de cones de alta acuidade em uma fóvea minúscula e usa ~95% de bastões para vigilância periférica de baixa resolução ([NCBI Webvision](https://www.ncbi.nlm.nih.gov/books/NBK554706/); [StatPearls Retina](https://www.ncbi.nlm.nih.gov/books/NBK545310/)).
> 22	
> 23	### Por que agora
> 24	
> 25	1. **A especificação MCP amadureceu.** A revisão corrente é **2025-11-25** (marcada "Current"), define exatamente dois transportes — stdio e **Streamable HTTP** (o antigo HTTP+SSE está deprecado) — e formaliza OAuth 2.1 com RFC 9728 Protected Resource Metadata para servidores remotos protegidos ([MCP Transports 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports); [MCP Authorization 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)). O Claude API MCP connector (`mcp-client-2025-11-20`) consome servidores remotos HTTPS com bearer token ([Claude MCP connector](https://platform.claude.com/docs/en/agents-and-tools/mcp-connector)).
> 26	2. **O MCORCH já roda um servidor MCP in-house.** `mcorch_gitnexus` usa `StreamableHTTPServerTransport` em `127.0.0.1:3100` dentro do Sovereign Mesh hardened — confirmado materialmente em `packages/gitnexus-core/src/mcp/server.ts:16,97` e `docker-compose.yml:89-119`. O runtime recomendado é uma extensão de infraestrutura provada, não terreno novo.
> 27	3. **Toda a cadeia de billing/tenancy/sentinel/mesh já existe** e é reutilizável (Seção 5).
> 28	
> 29	### O diferencial — sendo honesto sobre o que a recon do sandcastles.ai estabeleceu
> 30	
> 31	A recon do **sandcastles.ai** foi **materialmente verificada (alta confiança)** por probes diretos (curl, 2026-06-10/11), e **confirmada por re-probe adversarial independente**:
> 32	
> 33	- O MCP deles é **remoto, Streamable HTTP, OAuth-protegido** em `https://mcp.sandcastles.ai/`: `POST initialize` retorna `HTTP 401` com `WWW-Authenticate: Bearer ... resource_metadata="https://mcp.sandcastles.ai/.well-known/oauth-protected-resource"` (RFC 9728), servido por "Google Frontend" ([probe + verdict confirmado](https://mcp.sandcastles.ai/)). O authorization server (`signin.sandcastles.ai`) anuncia DCR, PKCE S256, device-code e refresh tokens — o que faz "cole 1 URL → login no browser → conectado" funcionar com zero config ([metadata chain confirmada](https://signin.sandcastles.ai/.well-known/openid-configuration)).
> 34	- O **diferencial de distribuição** (confirmado verbatim por render headless do doc oficial): eles não enviam só o servidor MCP — enviam um **"Plugin Zip" versionado** baixado de Settings → Connectors, que empacota o connector remoto (URL pré-preenchida) **+ um conjunto curado de Skills nomeadas** (slash-commands tipo `/analyze`, `/rules`) que envelopam as ferramentas cruas em workflows guiados ([setup doc confirmado](https://help.sandcastles.ai/mcp)). É um **triângulo de paridade de três superfícies** (UI web = REST API = MCP tools) + **skills-as-distribution**.
> 35	
> 36	**O que a recon NÃO estabeleceu (e portanto não é diferencial nosso):**
> 37	
> 38	- O provedor de auth é **inferido** como WorkOS AuthKit (path `/user_management/`, `client_id` ULID), **não declarado** — confiança média, citar como "consistente com", nunca como fato.
> 39	- Receita ~$1.6M / 22.000 creators vem de **uma única fonte secundária (Medium)** — confiança baixa, usar como anedota no MRD, jamais como evidência de mercado ([Medium, não-verificado](https://anirudhchundawat.medium.com/how-1-6m-app-started-with-a-one-day-experiment-without-coding-a70ec0d31441)).
> 40	- **Crucial:** sandcastles valida o **padrão de distribuição** (remote MCP + plugin + skills), **não o mercado de vision-deepsearch**. A varredura competitiva ao vivo do registry oficial (2026-06-11) provou que as duas metades do nosso "diferencial" já são servidas por incumbentes first-party:
> 41	  - **Vision sobre MCP já está tomado:** `com.roboflow/roboflow-mcp` (v1.0.3, "Roboflow Official", hosted em `mcp.roboflow.com/mcp`) expõe ~70 ferramentas de CV e **já executa o mesmíssimo padrão "remote MCP + Apps + Skills"** ([registry probe](https://registry.modelcontextprotocol.io/v0/servers?search=roboflow&limit=20); [llms.txt](https://mcp.roboflow.com/llms.txt)).
> 42	  - **Deepsearch sobre MCP já está tomado:** `ai.exa/exa`, `io.github.firecrawl/firecrawl-mcp-server` (6.5k★, MIT, self-hostable) e `io.github.tavily-ai/tavily-mcp` têm demanda comprovada — npm downloads no último mês: firecrawl-mcp **376.976**, tavily-mcp **165.112**, exa-mcp-server **67.928** ([npm stats](https://api.npmjs.org/downloads/point/last-month/firecrawl-mcp)).
> 43	
> 44	**Logo, o diferencial defensável do Vision MCP se sustenta por mérito próprio em quatro eixos, não na cópia do sandcastles:**
> 45	
> 46	1. **O produto cruzado** — saída de visão **fundamentada/verificada por evidência de deepsearch** numa única superfície de ferramenta. Busca direta não encontrou nenhum servidor MCP combinando computer vision com agentes de deep-research (whitespace genuíno) — **mas ausência de competidor é também ausência de validação de demanda**: o MRD deve tratar isso como **hipótese a validar**, não mercado provado.
> 47	2. **Soberania / self-host** vs o servidor hosted-only da Roboflow (cujo repo GitHub retorna 404 — provável closed-source) — deploy on-prem no Sovereign Mesh é uma cunha real.
> 48	3. **Credencial per-tenant + billing mcoCoins atômico** que o MCORCH já tem nativo (Seção 5).
> 49	4. **A filosofia "Essência Humana"** — arquitetura de percepção em dois níveis (Seção 3) como princípio de custo/eficiência, fundamentada em biologia e já validada como paradigma de engenharia em XR.
> 50	
> 51	---
> 52	
> 53	## 2. Os 4 Pilares
> 54	
> 55	> Para cada pilar: fundamentos consolidados + **veredictos da verificação adversarial**. Refutados aparecem corrigidos; não-verificáveis são marcados `⚠️`.
> 56	
> 57	### Pilar I — Computer Vision (CV)
> 58	
> 59	**Fundamento.** Para um SaaS server-side sem GPU garantida, a CV de produção se divide em quatro pistas: VLM-via-API (default sem GPU), foundation models de segmentação/open-vocab (GPU/hosted), stacks clássicos/treináveis (CPU), e OCR/embeddings.
> 60	
> 61	| Afirmação | Veredicto adversarial | Fonte |
> 62	|---|---|---|
> 63	| **SAM 3** é a geração corrente do Segment Anything (lançada **2025-11-19**); **SAM 3.1** "Object Multiplex" em **2026-03-27**. Adiciona prompts de conceito por **texto/exemplar** (detect+segment+track de todas as instâncias). | ✅ **Confirmado** (Meta newsroom + Roboflow + Ultralytics + Voxel51). Citar "SAM 2 como último" está uma geração atrás. | [github.com/facebookresearch/sam3](https://github.com/facebookresearch/sam3) · [ai.meta.com/blog/segment-anything-model-3](https://ai.meta.com/blog/segment-anything-model-3/) |
> 64	| SAM 3 exige **CUDA ≥12.6 / PyTorch ≥2.7 / Python ≥3.12** — **não é opção CPU-only**. | ✅ Confirmado (guias de deploy Spheron/StableLearn). Para SaaS sem GPU: consumir via host (fal.ai $0.005/req, Replicate). | [Verdict](https://github.com/facebookresearch/sam3) |
> 65	| SAM 3 sob **"SAM License" bespoke** (não Apache); SAM 2 é **Apache-2.0**. | ✅ Confirmado — **regressão de licença entre gerações**. SAM 2 é o fallback de licença limpa. | [SAM 2 LICENSE](https://github.com/facebookresearch/sam2/blob/main/LICENSE) · [SAM License raw](https://raw.githubusercontent.com/facebookresearch/sam3/main/LICENSE) |
> 66	| **DINOv3** (ago/2025): backbone self-supervised SOTA, porém **licença comercial gated** (não Apache como DINOv2). | ✅ Confirmado; impõe **atribuição "Built with DINOv3"** + direito de terminação Meta. DINOv2 permanece a opção permissiva. | [DINOv3 License](https://ai.meta.com/resources/models-and-libraries/dinov3-license/) |
> 67	| **Ultralytics (YOLO)** é **AGPL-3.0 OU Enterprise paga** — a maior armadilha de licença do ecossistema para SaaS closed-source. | ✅ Confirmado **diretamente** (dual-licensing). ⚠️ **"YOLO26 lançado jan/2026" NÃO foi verificado** (veio de síntese de busca, não fetch direto). Tratar o nome/data YOLO26 como não-confirmado; a armadilha AGPL é fato. | [github.com/ultralytics/ultralytics](https://github.com/ultralytics/ultralytics) |
> 68	| **RF-DETR** (Roboflow, ICLR 2026): detecção+segmentação real-time, **Apache-2.0** nos tamanhos core (Nano..Large); só XL/2XL "Plus" sob PML 1.0. | ✅ Confirmado — alternativa de licença limpa ao YOLO/AGPL. | [github.com/roboflow/rf-detr](https://github.com/roboflow/rf-detr) |
> 69	| **Gemini API** detecta objetos nativamente, retornando boxes `[ymin,xmin,ymax,xmax]` normalizados 0–1000. | ✅ Alta confiança (doc oficial). Único VLM-API com box detection treinado-in. | [ai.google.dev/.../image-understanding](https://ai.google.dev/gemini-api/docs/image-understanding) |
> 70	| Segmentação (máscaras) **não suportada** em Gemini 3 Pro/Flash; rotear para Gemini 2.5 Flash. | ⚠️ **Confiança média** — vem de snippet; a página fetchada apenas **omite** segmentação, não declara a limitação. Validar antes de fixar no SDD. | [ai.google.dev/.../gemini-3](https://ai.google.dev/gemini-api/docs/gemini-3) |
> 71	| **OpenCV 5.0** (jun/2026): primeiro major desde 2018; C API legado removido, DNN reescrita (ONNX >80%). | ⚠️ **Contradição interna sinalizada pela crítica:** rotulado "consolidado" sendo de dias atrás; **licença do 5.0 não re-verificada**. O SDD precisa de **decisão explícita pin-4.x-vs-5.0**. | [opencv.org/opencv-5](https://opencv.org/opencv-5/) |
> 72	| **PaddleOCR 3.x** Apache-2.0, **CPU-viável**, 100+ idiomas (PP-OCRv5) + doc→Markdown/JSON. | ✅ Confirmado — escolha OCR consolidada/permissiva quando não há GPU. | [github.com/PaddlePaddle/PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) |
> 73	| **Mistral OCR 3** — pricing era conflitante. | ✅ **Resolvido (fetch ao vivo):** **$2/1.000 páginas** (extração) + **$3/1.000** (annotations) no tier standard; **$1/1.000** é o Batch API; os $0.50 eram a geração anterior. **Não está no OpenRouter** → exige integração direta Mistral (chave per-user). | [mistral.ai/pricing](https://mistral.ai/pricing) · [OCR 3 launch](https://mistral.ai/news/mistral-ocr-3/) |
> 74	| Pista permissiva leve: **Florence-2** (MIT, 230M/770M, caption/detect/ground/OCR), **Moondream** (Apache-2.0 0.5B/2B, roda em CPU/RPi), **SigLIP 2** e **CLIP** (MIT) para embeddings. | ✅ Consolidado. Florence-2 é o modelo mais denso em MIT pequeno o suficiente para CPU. | [Florence-2](https://huggingface.co/microsoft/Florence-2-large) · [Moondream](https://moondream.ai/blog/introducing-moondream-0-5b) · [SigLIP 2](https://huggingface.co/blog/siglip2) |
> 75	| **Qwen3-VL** (8B→235B) via OpenRouter; instruct weights **Apache-2.0** confirmados no card HF. | ✅ Confirmado — VLM frontier na pista Apache sem propagação de licença. | [Qwen3-VL-8B-Instruct](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct) |
> 76	
> 77	**Veredicto de hype-vs-consolidado:** consolidados = VLM via OpenRouter, OpenCV (com pin), PaddleOCR, transformers/timm, SigLIP2/CLIP, Grounding DINO, SAM 2. Jovens-mas-reais = SAM 3/3.1, RF-DETR, DeepSeek-OCR-2, Perception Encoder. Emergentes = wrappers "agentic CV", SAM 3D — adotar atrás de interfaces.
> 78	
> 79	### Pilar II — Análise de Movimento (Motion)
> 80	
> 81	| Afirmação | Veredicto adversarial | Fonte |
> 82	|---|---|---|
> 83	| Fluxo óptico é linhagem **RAFT**: RAFT (BSD-3, ECCV 2020) → **SEA-RAFT** (BSD-3, ECCV 2024, ≥2.3× mais rápido, SOTA Spring 3.69 EPE) → **MEMFOF** (ICCV 2025, multi-frame em 2.09 GB a 1080p). | ✅ Confirmado. **Gap fechado:** a licença do MEMFOF — antes "não-verificada" — é **BSD-3-Clause** (verdict). | [RAFT](https://github.com/princeton-vl/RAFT) · [SEA-RAFT](https://github.com/princeton-vl/SEA-RAFT) · [MEMFOF](https://github.com/msu-video-group/memfof) |
> 84	| **RTMPose-m**: 75.8 AP COCO a **90+ FPS em CPU Intel i7-11700** (Apache-2.0, ONNX/ncnn/OpenVINO); **MediaPipe Pose** (33 landmarks, Apache-2.0). | ✅ Confirmado — pose multi-pessoa vira workload **CPU-barato**. ⚠️ **Crítica:** todos os números CPU são **x86**; o host-alvo é **Oracle ARM64** — **faltam benchmarks aarch64** (ONNX/ncnn ARM). | [MMPose/RTMPose](https://github.com/open-mmlab/mmpose/tree/main/projects/rtmpose) · [MediaPipe](https://github.com/google-ai-edge/mediapipe) |
> 85	| Tracking consolidado tracking-by-detection: **ByteTrack** (MIT) e **BoT-SORT** (MIT, default na Ultralytics YOLO). | ✅ Confirmado — camada de associação MOT barata sobre qualquer detector. | [ByteTrack](https://github.com/ifzhang/ByteTrack) · [BoT-SORT](https://github.com/NirAharon/BoT-SORT) · [Ultralytics Track](https://docs.ultralytics.com/modes/track/) |
> 86	| **VideoMAE V2** (action recognition self-host, repo **MIT**); **InternVideo2** (92.1% K400) — licença antes não-verificada. | ✅ **Gap fechado:** repo InternVideo **Apache-2.0**, weights **InternVideo2-Stage2_6B tagged MIT** — pista permissiva, mas **fixar o checkpoint exato** (licenças variam por variante). | [VideoMAE V2 LICENSE](https://github.com/OpenGVLab/VideoMAEv2/blob/master/LICENSE) · [InternVideo LICENSE](https://raw.githubusercontent.com/OpenGVLab/InternVideo/main/LICENSE) · [Stage2_6B](https://huggingface.co/OpenGVLab/InternVideo2-Stage2_6B) |
> 87	| **Gemini é o único LLM-API geral com input nativo de vídeo**: 1 FPS default, **~300 tokens/seg** (default res), até 1h (3h low-res). **OpenAI NÃO tem input nativo de vídeo** (mar/2026, workaround ffmpeg→frames perde sinal temporal). | ✅ Confirmado (doc Gemini + issue OpenAI). Alternativa video-nativa: **TwelveLabs** (Marengo/Pegasus) via Amazon Bedrock. | [Gemini video](https://ai.google.dev/gemini-api/docs/video-understanding) · [OpenAI issue #1778](https://github.com/openai/openai-node/issues/1778) |
> 88	| **OpenCV MOG2/KNN** (background subtraction): máscara de foreground por frame para câmera estática — gate quase-grátis em CPU **antes** de estágios caros. | ✅ Confirmado — o nicho durável dos clássicos: câmera fixa, CPU-only, objetos sub-detector, pré-filtro para cortar gasto GPU/API. | [OpenCV BGS tutorial](https://docs.opencv.org/4.x/d1/dc5/tutorial_background_subtraction.html) |
> 89	
> 90	**Stack consolidado de pipeline:** MOG2/frame-diff gate (CPU) → RTMPose/MediaPipe pose (CPU) → YOLO+BoT-SORT/ByteTrack tracking (GPU) → VideoMAE V2 fine-tune para ações fechadas (GPU) → Gemini video API para perguntas temporais abertas (API), com SAM 2/3 reservado para tracking promptável pixel-accurate.
> 91	
> 92	### Pilar III — Sensores & Computação Neuromórfica (Neuromorphic)
> 93	
> 94	> Este pilar cobre **dois lados** do paradigma neuromórfico: a **captação** (sensores event-based/DVS da Sony/Prophesee) **e a computação** propriamente dita — processadores (Loihi 2, BrainChip Akida), redes spiking (SNN: snnTorch/Norse/SpikingJelly) e sua **emulação em software** (v2e/OpenEB) sobre vídeo/tela. A diretiva Sovereign "Computação Neuromórfica" cai inteiramente aqui (já coberta), por isso v0.2.0 não cria pilar novo para ela.
> 95	
> 96	| Afirmação | Veredicto adversarial | Fonte |
> 97	|---|---|---|
> 98	| Sensores event-based são **produto comercial real**: Sony vende 4 EVS (IMX636/646/637/647, 4.86µm, 1.06 Geps, latência µs), co-dev Prophesee. | ✅ Confirmado (Sony + FRAMOS + IDS + Lucid). | [Sony EVS](https://www.sony-semicon.com/en/products/is/industry/evs.html) |
> 99	| **O mercado é financeiramente frágil:** Prophesee entrou em **redressement judiciaire** (recuperação judicial FR) fim de 2024; reestruturou em 2025 (novo CEO, pivô para defesa/industrial). | ✅ Confirmado (Sifted + VIPress). ⚠️ **Desfecho legal formal (plano de continuação vs venda) não-verificado.** | [Insolvency](http://image-sensors-world.blogspot.com/2025/01/prophesee-files-for-insolvency.html) · [Recap 2025](https://www.prophesee.ai/2026/01/07/prophesee-recap-2025/) |
> 100	| **Intel arquivou TODO o framework Lava em 2026-05-13** — sem manutenção. Loihi 2/Hala Point é research-only (INRC). | ✅ Confirmado — **diretiva de engenharia: NÃO adotar Lava em 2026.** | [github.com/lava-nc/lava](https://github.com/lava-nc/lava) |
> 101	| **BrainChip Akida Cloud** (ago/2025): inferência neuromórfica como serviço cloud (free tier + usage-based) — **o único processador neuromórfico consumível como API sem hardware**. | ✅ Confirmado. AKD1500 só atinge volume Q3'26. | [Akida Cloud](https://brainchip.com/brainchip-launches-akida-cloud-for-instant-access-to-latest-akida-neuromorphic-technology/) |
> 102	| **Os PRINCÍPIOS neuromórficos são software-emuláveis** sobre vídeo/screenshots: **v2e** (MIT) converte vídeo em event streams DVS realistas; **rpg_vid2e/ESIM** (GPL-3.0) idem; **OpenEB/Metavision** (Apache-2.0) traz simulador Video-to-Event de primeira classe; **CARLA** tem sensor DVS embutido. Stack SNN completo é PyTorch puro: **snnTorch** (MIT), Norse, SpikingJelly, Tonic. | ✅ Confirmado — a própria Prophesee trata síntese frame→evento como ferramenta de produção. | [v2e](https://github.com/SensorsINI/v2e) · [OpenEB](https://github.com/prophesee-ai/openeb) · [snnTorch](https://github.com/jeshraghian/snntorch) |
> 103	| **Onde o hardware é insubstituível (honestidade):** (a) resolução temporal µs verdadeira — eventos sintéticos herdam o frame-rate da fonte; interpolação **fabrica** timestamps inter-frame, não os **observa** (a própria framing do v2e: "higher EFFECTIVE timing precision"); (b) HDR >140dB e ausência de motion blur na captura; (c) economia de potência/banda no sensor (GenX320 a 36µW). | ✅ Confirmado — qualquer claim de produto deve dizer **"event-like processing"**, jamais "microsecond sensing". | [v2e paper](https://arxiv.org/pdf/2006.07722) · [GenX320](https://www.prophesee.ai/2023/10/16/prophesee-launches-genx320/) |
> 104	| O gap sim-to-real (modelos treinados em eventos sintéticos degradam em sensores reais) **se dissolve quando o domínio de deploy É vídeo/tela renderizada** (train-domain == inference-domain). | ⚠️ **Raciocínio plausível, NÃO evidência** — nenhuma fonte testou pipelines de evento sintético em conteúdo de tela especificamente. **Marcar como HIPÓTESE no SDD**, não como achado. | [Sim-to-real study](https://arxiv.org/abs/2506.13722) |
> 105	
> 106	**Receita pragmática 2026 para SaaS sem sensor:** síntese de eventos estilo OpenEB/v2e (ou frame-differencing log-intensity barato) → representações voxel-grid/time-surface → modelos GPU convencionais ou SNNs snnTorch/SpikingJelly, com Akida Cloud opcional se inferência neuromórfica genuína for desejada.
> 107	
> 108	### Pilar IV — Visão Periférica / Foveada (Peripheral/Foveated)
> 109	
> 110	| Afirmação | Veredicto adversarial | Fonte |
> 111	|---|---|---|
> 112	| A retina é radicalmente não-uniforme: cones foveais ~170–200k/mm² vs periferia <20k/mm²; **~95% dos fotorreceptores são bastões** (vigilância ampla), ~5% cones (acuidade central esparsa). | ✅ Confirmado (Curcio/AOSLO; Nature; Webvision). Justifica gastar compute hi-res num crop minúsculo e lo-res no campo amplo. | [Webvision Fovea](https://www.ncbi.nlm.nih.gov/books/NBK554706/) · [Retina](https://www.ncbi.nlm.nih.gov/books/NBK545310/) |
> 113	| A periferia é **detector de movimento/mudança**: o stream dorsal "where/how" recebe **~90%** do input do sistema magnocelular (alto ganho de contraste, baixa freq. espacial, rápido), projeta a V5/MT e córtex parietal, dirige atenção e movimentos oculares. | ✅ Confirmado **com nuance**: "~90%" é aproximação de livro-texto ("dominado por/grande maioria"), não valor exato pinado. Substância correta. | [Magnocellular/dorsal](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4186266/) |
> 114	| **Two-streams hypothesis** (Goodale & Milner 1992): ventral "what" (identidade) vs dorsal "where/how" (localização/ação) — paciente D.F. Mapeia direto no design de dois níveis. **Feature Integration Theory** (Treisman 1980): features básicas pré-atentivas em paralelo ("pop-out" em tempo constante); conjunções exigem busca serial atencional. | ✅ Ambas confirmadas (Frontiers; Wikipedia; CUNY). Blueprint biológico direto do nível barato (pop-out paralelo) vs caro (binding serial). | [Two-streams](https://en.wikipedia.org/wiki/Two-streams_hypothesis) · [FIT](https://en.wikipedia.org/wiki/Feature_integration_theory) |
> 115	| **Foveated rendering eye-tracked é paradigma de engenharia EM PRODUÇÃO** em XR: Apple Vision Pro, Quest Pro, PSVR2, Vive Pro Eye. No Quest Pro, ETFR economiza **33–45% GPU** (default), limitado por **~50ms** de latência de eye-tracking. | ✅ Confirmado (Meta dev docs + UploadVR). A latência do trigger limita o ganho do tier caro-sob-demanda — **lição de sistemas para o loop saliência→fóvea**. ⚠️ A figura visionOS "72%" é **não-verificada** (blog secundário). | [Quest Pro ETFR](https://www.uploadvr.com/quest-pro-foveated-rendering-performance/) · [Meta ETFR](https://developers.meta.com/horizon/blog/save-gpu-with-eye-tracked-foveated-rendering/) |
> 116	| Componentes ML maduros: **saliência** consolidada (DeepGaze IIE ICCV 2021, DeepGaze III 2022, SALICON); **glimpse/hard-attention** (RAM, Mnih 2014); arquiteturas peripheral-inspired (**PerViT** NeurIPS 2022; modelo foveal-peripheral Frontiers 2021 ~10× mais rápido, 0.39% perda); o loop "passe barato amplo → análise focada cara" é dominante em VLMs hi-res (**V*/SEAL**, Chain-of-Focus, CropVLM). | ✅ Confirmados individualmente. ⚠️→✅ **[CORRIGIDO 2026-06-15 — gate research OTD-VM-001 FECHADA]** As 2 afirmações originais foram **refutadas materialmente** (a regra de Materialidade manda usar a versão corrigida): (a) datasets de UI-saliency **EXISTEM** — **UEyes** (CHI 2023, 1.980 screenshots eye-tracked) e **Imp1k** (1.000 designs incl. UI) públicos (WebSaliency segue não-confirmado); (b) o SOTA de UI-saliency **NÃO é DeepGaze** (free-viewing natural — confirmado que NÃO transfere) — é **SUM** (WACV 2025 Oral, **MIT, self-hostável**; CC 0.731 vs 0.696 em U-EYE) / UniAR. O "maior buraco técnico" vira **engenharia com benchmark de domínio + SOTA self-hostável + recall≥0.95 fundamentado** (SDD §3.4 / FR-VM-010). Resta hipótese: latência ARM64 do SUM. | [DeepGaze IIE](https://arxiv.org/abs/2105.12441) · [PerViT](https://proceedings.neurips.cc/paper_files/paper/2022/hash/cf78a15772ec1a6aee9bbee2d2b382c3-Abstract-Conference.html) · [V*/SEAL](https://arxiv.org/abs/2312.14135) |
> 117	| O análogo de sistemas — estágio barato de alto-recall rejeitando a maioria, reservando o estágio caro/preciso para casos ambíguos (linhagem **Viola-Jones**; probes antes de classificadores LLM caros) — é padrão de eficiência de produção. | ✅ Confirmado (cascatas reportam ~3× redução de latência) — valida a arquitetura proposta independentemente de visão. ⚠️ Figuras de speedup de robótica foveada (94%/7×/3×) **não-verificadas**. | [Cascaded pipelines](https://www.emergentmind.com/topics/cascaded-detection-pipelines) |
> 118	
> 119	### Pilar V — Computação Cognitiva
> 120	
> 121	**Fundamento (e a armadilha de nomenclatura).** "Computação Cognitiva" como **rótulo de produto** é marketing legado da era Watson (IBM, 2011–2017): o ponto-final material foi a venda dos ativos de dados/analytics da Watson Health à Francisco Partners (~US$1B, 2022) → empresa autônoma **Merative**, e o pivô da IBM para a marca **watsonx** ("AI for business", Think 2023-05-09) — ambos abandonando explicitamente o moniker "cognitive computing". O termo sobrevive apenas como verbete educacional/definicional. O vocabulário da indústria migrou para **"agentic AI" / "AI agents"** — que carrega o **mesmo risco de hype** (Gartner 2025: AI agents no Pico de Expectativas Infladas + previsão de >40% dos projetos agentic cancelados até fim de 2027 + cunhagem do termo "agent washing"). **Diretiva de posicionamento: nunca brandar o produto como "cognitive computing" nem como "cérebro digital"; ancorar a arquitetura na camada de pesquisa consolidada (CoALA/V*/GraphRAG), não no rótulo.**
> 122	
> 123	> O substantivo aproveitável de "computação cognitiva" para o Vision MCP **não** é a marca — é a **arquitetura cognitiva de agentes** (memória modular + espaço de ação estruturado + loop de decisão), da qual a percepção visual é um **órgão**. E o MCORCH já tem quase toda a arquitetura (Seção 3).
> 124	
> 125	| Afirmação | Veredicto adversarial | Fonte |
> 126	|---|---|---|
> 127	| "Cognitive computing" é marketing legado: IBM vendeu os ativos da Watson Health à Francisco Partners (~US$1B, 2022) → **Merative**, afastando-se do moniker; pivotou para **watsonx** ("AI for business", 2023-05-09). | ✅ **Confirmado** (IBM Newsroom + Francisco Partners + STAT/HealthExec/Fierce). | [STAT/Merative](https://www.statnews.com/2022/07/06/ibm-watson-health-merative-data/) · [watsonx](https://newsroom.ibm.com/2023-05-09-IBM-Unveils-the-Watsonx-Platform-to-Power-Next-Generation-Foundation-Models-for-Business) |
> 128	| O termo sobrevive só como verbete **dormente-definicional** (TechTarget o associa a IBM Watson, "assiste decisão humana"), não foi formalmente aposentado. | ✅ Confirmado (fetch ao vivo 2026-06-11). Usar como rótulo de produto sinaliza marketing de 2015. | [TechTarget](https://www.techtarget.com/searchenterpriseai/definition/cognitive-computing) |
> 129	| A indústria migrou para **"agentic AI"**; Gartner 2025 põe AI agents no Pico de Expectativas Infladas, prevê **>40% de cancelamento** de projetos agentic até fim de 2027 e cunhou **"agent washing"**. | ✅ Confirmado (BusinessWire/MarTech/Search Engine Land/HPCwire). O novo rótulo herda o risco de hype do antigo. | [Gartner Hype Cycle 2025](https://www.gartner.com/en/newsroom/press-releases/2025-08-05-gartner-hype-cycle-identifies-top-ai-innovations-in-2025) · [40% cancel](https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027) |
> 130	| Arquiteturas cognitivas clássicas estão vivas como **pesquisa, não stack de produção**: ACT-R (CMU, workshop 2026) e Soar (OSS release 9.6.5, fixes EpMem/SMem, pacote `soar_ros`) pioneiraram o split memória episódica/semântica/procedural que os frameworks de agente LLM hoje copiam. | ✅ Confirmado (releases GitHub SoarGroup + homepage CMU). Citar como **linhagem** da memória da malha, não construir sobre. | [Soar](https://soar.eecs.umich.edu/) · [ACT-R](http://act-r.psy.cmu.edu/) |
> 131	| **CoALA** (Sumers/Yao/Narasimhan/Griffiths; **TMLR 2024**) é a ponte consolidada e peer-reviewed entre arquiteturas cognitivas clássicas e agentes LLM: memória modular (working = janela de contexto; episódica; semântica; procedural) + espaço de ação estruturado (interno/externo) + loop de decisão. | ✅ **Confirmado e consolidado** — a doc oficial do **LangGraph cita CoALA verbatim** e implementa a taxonomia em framework de produção. É engenharia, não especulação. | [CoALA TMLR](https://arxiv.org/abs/2309.02427) · [LangGraph Memory](https://docs.langchain.com/oss/python/langgraph/memory) |
> 132	| O mercado de memória de agente convergiu na taxonomia episódica/semântica/procedural: **Letta** (contexto como memória virtual paginada), **Zep** (temporal knowledge graph), **Mem0**; **Microsoft GraphRAG** consolida o híbrido vector+graph. | ✅ Confiança média (landscape secundário + docs primárias). **Valida o híbrido pgvector+`mcorch_edges` da malha** como padrão de indústria. | [GraphRAG](https://github.com/microsoft/graphrag) · [Survey memória](https://arxiv.org/abs/2404.13501) |
> 133	| O **computer-use da Anthropic** é um loop de produção (beta) percepção→raciocínio→ação: screenshot → mouse/teclado, gated por beta-headers. | ✅ Confirmado (doc oficial). Um Vision MCP fatora o **mesmo primitivo de percepção** como capability MCP, não como ferramenta monolítica fechada. | [computer-use](https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/computer-use-tool) |
> 134	| **GWT-para-IA** é thread de pesquisa ativo (Goldstein & Kirk-Giannini 2024; "Theater of Mind"/Global Workspace Agents 2026) — fornece um **padrão de broadcast** (percepção publicada num workspace compartilhado legível por todos os agentes = a malha) usável **como metáfora de engenharia apenas**. | ⚠️ Research-grade (preprints recentes, single-author/sem replicação). **Claims de consciência NÃO são engenharia acionável** — fora de escopo. | [GWT/consciousness](https://arxiv.org/abs/2410.11407) · [Global Workspace Agents](https://arxiv.org/abs/2604.08206) |
> 135	| **Active inference** (Friston): VERSES lançou Genius comercialmente (2025-04-30); **AXIOM** (arXiv 2505.24784) é agente object-centric gradient-free que aprende jogos em ~10k passos; PR alega bater o DreamerV3. | ⚠️ **Benchmark é vendor-controlado, sem replicação independente.** Citar o **paper** (a ideia: atenção gated por ganho de informação esperado), nunca o press release "digital brain beats Google". `pymdp` é a implementação OSS peer-reviewed (JOSS 2022). | [AXIOM](https://arxiv.org/abs/2505.24784) · [pymdp](https://github.com/infer-actively/pymdp) |
> 136	| Pesquisa pós-CoALA (arXiv 2604.11364) argumenta que stacks CoALA precisam de uma **camada de Conhecimento distinta**: **fatos suplantam** (supersession, sem decaimento); **memórias decaem** (Ebbinghaus/FSRS). Aplicar decaimento cognitivo a fato factual é um **"category error"**. | ✅ Confiança alta (preprint 2026 com implementação). **Regra de design citável** para o `stability_score`/FSRS-6 da malha: decair relevância de **observações**, deixar **fatos** suplantarem. | [Missing Knowledge Layer](https://arxiv.org/abs/2604.11364) |
> 137	
> 138	**Receita pragmática 2026 (quatro âncoras defensáveis, cada uma mapeada num primitivo MCORCH existente):** (1) **CoALA como mapa de memória** — working = janela de contexto; episódica = nós `observation` em `mcorch_nodes`; semântica = grafo + pgvector; procedural = skills/SOPs; a percepção escreve em episódica e promove a semântica, exatamente como a malha já faz. (2) **O pipeline de dois níveis É busca visual guiada V\*/SEAL** (CVPR 2024) — passe periférico barato → política decide se a fóvea cara vale o custo (a citação mais forte da arquitetura, Pilar IV). (3) **GWT como padrão de broadcast** — resultado de percepção publicado no workspace compartilhado (a malha) legível por todo o Pantheon, **só como metáfora**. (4) **Active inference → metering** — disparar a passada foveal cara apenas quando o ganho de informação esperado justifica o custo, mapeando direto no metering mcoCoins de chamadas hi-res. **Fluff a evitar:** brandar "cognitive computing"; claims de consciência GWT; "cérebro digital" sem benchmark independente; decaimento aplicado a fatos semânticos (o category error de 2604.11364).
> 139	
> 140	---
> 141	
> 142	## 3. Arquitetura "Essência Humana"
> 143	
> 144	### O design unificador: percepção em dois níveis
> 145	
> 146	```
> 147	                          ┌──────────────────────────────────────────────────────┐
> 148	                          │  TIER 1 — PERIFERIA (barata, always-on, alto-recall)  │
> 149	   input (imagem/         │  "dorsal / where-how": princípios neuromórficos        │
> 150	    vídeo/screen/         │   EMULADOS EM SOFTWARE                                  │
> 151	    stream/URL)  ───────▶ │   • frame-diff / MOG2 (OpenCV, CPU)                     │
> 152	                          │   • síntese de eventos v2e/OpenEB → voxel-grid          │
> 153	                          │   • saliência DeepGaze (cheap "where to look")          │
> 154	                          │   • pop-out de feature única (FIT, paralelo)            │
> 155	                          └───────────────┬──────────────────────────────────────┘
> 156	                                          │  SALIENCY / EVENT TRIGGER
> 157	                                          │  (só dispara se há sinal — gate)
> 158	                                          ▼
> 159	                          ┌──────────────────────────────────────────────────────┐
> 160	                          │  TIER 2 — FÓVEA (cara, profunda, sob-demanda)          │
> 161	                          │  "ventral / what": identidade & semântica              │
> 162	                          │   • crop foveal → VLM (Gemini/Qwen/Claude/GPT-5.x)     │
> 163	                          │   • SAM 2/3 segmentação promptável                     │
> 164	                          │   • OCR (Mistral/PaddleOCR)                            │
> 165	                          │   • Gemini video API (temporal aberto)                 │
> 166	                          └───────────────┬──────────────────────────────────────┘
> 167	                                          │  extração estruturada
> 168	                                          ▼
> 169	                          ┌──────────────────────────────────────────────────────┐
> 170	                          │  DEEPSEARCH GROUNDING (Firecrawl, per-user)            │
> 171	                          │   query ▶ scrape/search ▶ "referências consolidadas"  │
> 172	                          └───────────────┬──────────────────────────────────────┘
> 173	                                          ▼
> 174	                          ┌──────────────────────────────────────────────────────┐
> 175	                          │  KNOWLEDGE MESH (mcorch_nodes/edges, user+project)    │
> 176	                          │   nó observation + content_mesh_asset                 │
> 177	                          │   ▶ embed-mcorch-node → pgvector(768) (grátis)        │
> 178	                          │   ▶ provenance/license/retention metadata             │
> 179	                          └──────────────────────────────────────────────────────┘
> 180	```
> 181	
> 182	**Por que dois níveis (fundamento + economia).** A biologia (Pilar IV) e o XR de produção provam que concentrar compute caro onde há sinal economiza 33–52% de GPU com perda de acurácia negligenciável (Quest Pro ETFR; modelo foveal-peripheral Frontiers 2021 ~10× mais rápido a 0.39% de perda). No nosso domínio econômico isso é literal: o **Tier 1 roda em CPU quase-grátis** (1 mco ou 0), e o **Tier 2 só queima mcoCoins quando o gate dispara** — a periferia neuromórfica emulada é o que mantém o custo por chamada baixo.
> 183	
> 184	**Honestidade do limite.** O Tier 1 NÃO entrega resolução temporal µs (eventos sintéticos são interpolados, não observados — Pilar III). E a saliência DeepGaze **ainda não tem transferência comprovada para telas/UIs** (Pilar IV, gap aberto). Portanto o gate periférico é especificado como **alto-recall com custo de falso-negativo explícito** (o que o Tier 1 não disparar, o Tier 2 nunca vê) — uma decisão de design que o FRD precisa calibrar com um alvo de recall medido (Seção 8).
> 185	
> 186	### Como o deepsearch fundamentado alimenta a Knowledge Mesh
> 187	
> 188	Cada extração de deepsearch ("referência de mercado consolidada") vira um nó na malha seguindo o shape `content_mesh_asset` (precedente `orchestrate-step/index.ts:445-462`), com `user_id + project_id` (isolamento tenant, migration `20260425210000`), e é **embeddada de graça** pelo pipeline `embed-mcorch-node` (OpenRouter text-embedding-3-small → fallback Gemini text-embedding-004, 768 dims). Isso casa o diferencial de produto (referências consolidadas) com o GraphRAG existente: cada referência ganha edges para o nó de query/run, fica buscável por `match_mcorch_nodes`, e é submetida ao decaimento FSRS/`stability_score`. **Regra de soberania de dados:** conteúdo scrapeado NUNCA entra em system nodes (`user_id IS NULL` — visível a todos os tenants) e carrega metadata de proveniência/licença/retenção (Seções 7–8).
> 189	
> 190	### O dois-níveis é o órgão de percepção de uma arquitetura cognitiva (CoALA)
> 191	
> 192	A percepção em dois níveis não é um endpoint de OCR solto — ela é o **órgão de percepção** de uma **arquitetura cognitiva de agentes que o MCORCH já possui em quase toda a sua extensão**. Mapeando contra o loop CoALA (Pilar V; [CoALA TMLR 2024](https://arxiv.org/abs/2309.02427), citado verbatim pela doc do [LangGraph](https://docs.langchain.com/oss/python/langgraph/memory)):
> 193	
> 194	```
> 195	percepção            atenção                memória                          raciocínio/ação
> 196	(vision-mcp)   →     (Tier 1 gate     →     (Knowledge Mesh)          →      (Pantheon agents)
> 197	                      periférico)            • working = janela de contexto
> 198	 imagem/vídeo/        saliência/             • episódica = nós observation
> 199	 screen/URL           evento decide          • semântica/long-term = grafo + pgvector(768)
> 200	                      onde "olhar"           • procedural = skills/SOPs
> 201	```
> 202	
> 203	- **Percepção → atenção.** O Tier 1 (frame-diff/MOG2/saliência) é a função de **atenção** que decide onde gastar a fóvea — exatamente o mecanismo de **busca visual guiada** validado por [V\*/SEAL (CVPR 2024)](https://arxiv.org/abs/2312.14135): passe amplo barato → política → crop hi-res caro.
> 204	- **Memória.** A saída foveal **escreve em memória episódica** (nó `observation` em `mcorch_nodes`) e **promove a semântica** (grafo `mcorch_edges` + pgvector via `embed-mcorch-node`) — o híbrido vector+graph que [Microsoft GraphRAG](https://github.com/microsoft/graphrag) e Zep validam como padrão de indústria. A **janela de contexto** do agente é a working memory; **skills/SOPs** são a procedural memory.
> 205	- **Broadcast (GWT, só metáfora).** Publicar o resultado de percepção na malha legível por todo o Pantheon espelha o padrão de **broadcast hub** do Global Workspace ([2604.08206](https://arxiv.org/abs/2604.08206)) — adotado como engenharia, **sem nenhum claim de consciência** ([2410.11407](https://arxiv.org/abs/2410.11407), explicitamente fora de escopo).
> 206	- **Regra de persistência (anti-category-error).** Observações de visão **decaem** pela FSRS-6/`stability_score` (relevância episódica envelhece); **fatos** derivados (ex.: "este produto é X") devem **suplantar** versões antigas, não decair — a regra citável de [arXiv 2604.11364](https://arxiv.org/abs/2604.11364). O SDD deve separar esses dois regimes ao tipar nós originados de visão.
> 207	
> 208	**Por que isto importa para o BoK:** o diferencial não é "mais uma ferramenta de visão" — é a percepção fatorada como capability MCP **dentro de uma arquitetura cognitiva já montada** (malha GraphRAG + pgvector + FSRS + Pantheon), com âncoras peer-reviewed (CoALA/V\*/GraphRAG) em vez do rótulo morto "cognitive computing".
> 209	
> 210	---
> 211	
> 212	## 4. Catálogo de Referências Consolidadas
> 213	
> 214	> Apenas referências com URL real da pesquisa. `Como consumir`: API · self-host CPU · self-host GPU · emulável.
> 215	
> 216	| Nome | Pilar | Tipo | Maturidade | Licença | Como consumir | URL |
> 217	|---|---|---|---|---|---|---|
> 218	| SAM 3 / 3.1 (Meta) | CV/Motion | model | emergente/prod | SAM License (bespoke, gated) | self-host GPU; hosted (fal.ai $0.005/req) | https://github.com/facebookresearch/sam3 |
> 219	| SAM 2 (Meta) | CV/Motion | model | consolidado | Apache-2.0 | self-host GPU; Replicate $0.019/run | https://github.com/facebookresearch/sam2 |
> 220	| Grounding DINO | CV | model | consolidado | Apache-2.0 | self-host GPU/CPU | https://github.com/IDEA-Research/GroundingDINO |
> 221	| RF-DETR (Roboflow) | CV | model | produção | Apache-2.0 (core) / PML 1.0 (XL) | self-host CPU/GPU; Roboflow hosted | https://github.com/roboflow/rf-detr |
> 222	| DINOv3 (Meta) | CV | model | produção | DINOv3 License (gated, atribuição) | self-host GPU | https://ai.meta.com/resources/models-and-libraries/dinov3-license/ |
> 223	| OpenCV 5.0 | CV/Motion | library | consolidado (⚠️ pin) | Apache-2.0 (5.0 não re-verif.) | self-host CPU | https://opencv.org/opencv-5/ |
> 224	| PaddleOCR 3.x | CV | library | consolidado | Apache-2.0 | self-host CPU | https://github.com/PaddlePaddle/PaddleOCR |
> 225	| Mistral OCR 3 | CV | API | produção | proprietária | API (direta, não OpenRouter) | https://mistral.ai/pricing |
> 226	| Florence-2 (MS) | CV | model | produção | MIT | self-host CPU | https://huggingface.co/microsoft/Florence-2-large |
> 227	| Moondream | CV | model | emergente | Apache-2.0 | self-host CPU; API | https://moondream.ai/blog/introducing-moondream-0-5b |
> 228	| SigLIP 2 (Google) | CV | model | produção | Apache-2.0 (verif. por checkpoint) | self-host CPU/GPU | https://huggingface.co/blog/siglip2 |
> 229	| Qwen3-VL | CV | model | produção | Apache-2.0 (instruct) | API (OpenRouter); self-host GPU | https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct |
> 230	| Gemini API (vision/detect) | CV/Motion | API | consolidado | proprietária | API (também OpenRouter) | https://ai.google.dev/gemini-api/docs/image-understanding |
> 231	| Claude vision | CV | API | consolidado | proprietária | API (OpenRouter/Bedrock/Vertex) | https://platform.claude.com/docs/en/build-with-claude/vision |
> 232	| RAFT / SEA-RAFT / MEMFOF | Motion | model | consolidado/emergente | BSD-3-Clause | self-host GPU | https://github.com/princeton-vl/SEA-RAFT |
> 233	| MediaPipe Pose | Motion | SDK | produção | Apache-2.0 | self-host CPU | https://github.com/google-ai-edge/mediapipe |
> 234	| RTMPose (MMPose) | Motion | model | produção | Apache-2.0 | self-host CPU | https://github.com/open-mmlab/mmpose/tree/main/projects/rtmpose |
> 235	| ByteTrack / BoT-SORT | Motion | model | consolidado | MIT | self-host GPU | https://github.com/NirAharon/BoT-SORT |
> 236	| VideoMAE V2 | Motion | model | consolidado | MIT | self-host GPU | https://github.com/OpenGVLab/VideoMAEv2 |
> 237	| InternVideo2-Stage2_6B | Motion | model | produção | MIT (weight) / Apache-2.0 (repo) | self-host GPU | https://huggingface.co/OpenGVLab/InternVideo2-Stage2_6B |
> 238	| Gemini video understanding | Motion | API | produção | proprietária | API | https://ai.google.dev/gemini-api/docs/video-understanding |
> 239	| TwelveLabs (Bedrock) | Motion | API | produção | proprietária | API | https://aws.amazon.com/blogs/aws/twelvelabs-video-understanding-models-are-now-available-in-amazon-bedrock/ |
> 240	| Sony EVS sensors | Neuromorphic | hardware | consolidado | comercial | hardware-only | https://www.sony-semicon.com/en/products/is/industry/evs.html |
> 241	| BrainChip Akida Cloud | Neuromorphic | API | emergente | comercial (free+usage) | API | https://brainchip.com/brainchip-launches-akida-cloud-for-instant-access-to-latest-akida-neuromorphic-technology/ |
> 242	| OpenEB (Metavision core) | Neuromorphic | SDK | produção | Apache-2.0 | emulável / self-host CPU+GPU | https://github.com/prophesee-ai/openeb |
> 243	| v2e | Neuromorphic | library | produção | MIT | emulável / self-host GPU | https://github.com/SensorsINI/v2e |
> 244	| rpg_vid2e / ESIM | Neuromorphic | library | research | GPL-3.0 | emulável / self-host GPU | https://github.com/uzh-rpg/rpg_vid2e |
> 245	| snnTorch | Neuromorphic | library | produção | MIT | self-host CPU/GPU | https://github.com/jeshraghian/snntorch |
> 246	| Tonic (event transforms) | Neuromorphic | library | produção | GPL-3.0 (verif.) | self-host CPU | https://github.com/neuromorphs/tonic |
> 247	| DeepGaze IIE / III | Foveated | model | consolidado | research | self-host GPU | https://arxiv.org/abs/2105.12441 |
> 248	| RAM (glimpse) | Foveated | paper | research | — | self-host GPU | https://www.emergentmind.com/papers/1406.6247 |
> 249	| PerViT | Foveated | model | research | open source | self-host GPU | https://proceedings.neurips.cc/paper_files/paper/2022/hash/cf78a15772ec1a6aee9bbee2d2b382c3-Abstract-Conference.html |
> 250	| V*/SEAL (+V*Bench) | Foveated | paper | emergente | research | self-host GPU / API | https://arxiv.org/abs/2312.14135 |
> 251	| Foveal-Peripheral model (Frontiers 2021) | Foveated | paper | research | CC BY | self-host GPU | https://www.frontiersin.org/journals/computational-neuroscience/articles/10.3389/fncom.2021.746204/full |
> 252	| **MCP Spec 2025-11-25 — Transports** | (infra) | spec | consolidado | aberta | referência | https://modelcontextprotocol.io/specification/2025-11-25/basic/transports |
> 253	| **MCP Spec 2025-11-25 — Authorization** | (infra) | spec | consolidado | aberta | referência | https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization |
> 254	| **MCP TypeScript SDK** | (infra) | SDK | produção (v1.x) | MIT / Apache-2.0 | self-host (Node/Bun/Deno) | https://github.com/modelcontextprotocol/typescript-sdk |
> 255	| **MCP Registry** | (infra) | spec | preview | aberta | API (mcp-publisher) | https://modelcontextprotocol.io/registry/about |
> 256	| Supabase Edge BYO-MCP | (infra) | product | emergente | — | self-host (Deno edge) | https://supabase.com/docs/guides/ai-tools/byo-mcp |
> 257	| Cloudflare remote MCP | (infra) | SDK | produção | — | self-host (Workers) | https://developers.cloudflare.com/agents/guides/remote-mcp-server/ |
> ```

## 🤖 Claude *(18:49:51)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/vision-mcp/03-prd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# PRD — Product Requirements Document
> 2	
> 3	**Project:** vision-mcp  
> 4	**Version:** v0.1 | **Date:** 2026-06-11  
> 5	**BoK Applied:** ProdBOK + CXBOK  
> 6	**Status:** Complete  
> 7	**Source of Truth:** `docs/bok/vision-mcp/00-deepsearch-blueprint.md` (v0.2.0) + `docs/bok/vision-mcp/01-mrd.md` (MR-VM-001..016) + `docs/bok/vision-mcp/02-brd.md` (BR-VM-001..012) — todo PR-VM deste documento rastreia ≥1 BR-VM; ambiguidades viram OTD, nunca improvisação.  
> 8	**Market segment:** B2B2C · **Monetization:** híbrida (mcoCoins por tool call + planos Starter/Pro/Enterprise) · **Regulatory:** LGPD ELEVADO (biométrico art. 11) · **Integration surface:** extends-mcorch
> 9	
> 10	---
> 11	
> 12	## 1. Product Vision Statement
> 13	
> 14	> Para **agentes de IA, desenvolvedores MCP e empresas sob compulsão de acessibilidade (LBI Art. 63 / EAA / NBR 17225)** que **precisam de percepção visual confiável, fundamentada e auditável como capability componível**, o **Vision MCP** é um **servidor Model Context Protocol soberano de percepção visual + deepsearch fundamentado** que **transforma imagem, vídeo, tela e web em descrições/OCR/detecções estruturadas e referências de mercado consolidadas na Knowledge Mesh — com economia "Essência Humana" (Tier 1 periférico quase-grátis gateando o Tier 2 foveal billable) e dever de cuidado assistivo embarcado**. Diferente do **Roboflow MCP (hosted-only, sem grounding) e dos apps assistivos fechados (Be My AI/Seeing AI/Lookout)**, o nosso é **self-host no Sovereign Mesh, BYOK per-tenant fail-closed, billing mcoCoins atômico com refund-on-failure, e percepção fatorada como órgão de uma arquitetura cognitiva (CoALA) já montada**.
> 15	
> 16	---
> 17	
> 18	## 2. User Personas
> 19	
> 20	### Persona 1 — Gabriel / "Usuário Zero" (Primary, interno)
> 21	
> 22	| Attribute | Detail |
> 23	|-----------|--------|
> 24	| Role | Sovereign/Maestro do MCORCH; primeiro tenant em produção real; operador de dogfooding (SH-VM-001/002) |
> 25	| Goals | Dar olhos ao Pantheon (percepção como capability, não scripts ad-hoc); referências de mercado consolidadas na malha; validar o cruzado vision×deepsearch com dados (KPI-VM-003); manter margem 4×-floor |
> 26	| Frustrations | Pantheon raciocina sobre texto/AST mas não enxerga; deepsearch hoje depende de chave Firecrawl global (anti-pattern FM-VM-05); análise foveal cara sem gate barato |
> 27	| Tech-savviness | 5 (expert — arquiteto do sistema) |
> 28	| MCORCH usage pattern | Power user: opera a constelação, Canvas Studio e malha; consumirá as tools via Pantheon e Claude Code; audita ledger e telemetria |
> 29	| Quote | _"Não quero mais um endpoint de OCR solto — quero a percepção escrevendo na malha que os agentes já leem, com cada mcoCoin rastreável."_ |
> 30	
> 31	### Persona 2 — Otávio / MCP Developer (Secondary, externo)
> 32	
> 33	| Attribute | Detail |
> 34	|-----------|--------|
> 35	| Role | Desenvolvedor/operador de agentes em ecossistemas MCP externos (Claude Desktop/Code, VS Code, ChatGPT, Claude API) — SH-VM-004 |
> 36	| Goals | Conectar percepção visual + grounding ao seu agente com onboarding "cole 1 URL → login → conectado"; jobs de deepsearch que sobrevivem a janelas de wall-clock; billing previsível e confiável |
> 37	| Frustrations | Roboflow é hosted-only sem grounding; Firecrawl/Tavily/Exa não têm visão; sessions JWT de ~1h são inúteis para configs de client long-lived; medo de cobrança opaca sem refund |
> 38	| Tech-savviness | 4 (proficiente em agentes; não quer ler spec OAuth) |
> 39	| MCORCH usage pattern | Self-serve: descobre via MCP Registry (`com.mcorch/*`), conecta via OAuth 2.1, gera PAT para clients headless, baixa o Plugin Zip em Connectors |
> 40	| Quote | _"Se eu colar a URL e em dois minutos a tool responder — e devolver meus créditos quando falhar — eu fico."_ |
> 41	
> 42	### Persona 3 — Helena / Compliance & Accessibility Lead (Secondary, pagadora B2B2C)
> 43	
> 44	| Attribute | Detail |
> 45	|-----------|--------|
> 46	| Role | Líder de acessibilidade/compliance num e-commerce brasileiro sob LBI Art. 63 + EAA (vende à UE) — SH-VM-003; o pagador primário do beachhead |
> 47	| Goals | Alt-text WCAG 2.2 SC 1.1.1 / NBR 17225 em escala (catálogo com milhares de imagens); trilha de auditoria com revisão humana; nunca um claim de conformidade falso (FM-VM-17) |
> 48	| Frustrations | ~99% dos sites BR não-conformes e o dela é um deles; alt-text manual não escala; IA genérica alucina com confiança e não embarca dever de cuidado; MPF e notificações EAA aumentando a pressão |
> 49	| Tech-savviness | 3 (gestora técnica; consome via API/integrador, não escreve código de agente) |
> 50	| MCORCH usage pattern | Batch assistivo via API/MCP + fila de revisão humana; relatórios de conformidade; BYOK configurado pelo time de engenharia dela |
> 51	| Quote | _"Eu não preciso de uma IA que jura que está conforme — preciso de alt-text bom, sinalização honesta de incerteza e um humano aprovando o que vai para o ar."_ |
> 52	
> 53	### Persona 4 — Pantheon Agent (machine persona, interno)
> 54	
> 55	| Attribute | Detail |
> 56	|-----------|--------|
> 57	| Role | Agente L1/L2 do Pantheon (engineer/scientist/artisan/marketing-growth) consumindo percepção via mesh interno — SH-VM-006 |
> 58	| Goals | Invocar `vision.*`/`deepsearch.*` com identidade verificada; gravar observações episódicas na malha (embed-on-insert); promover fatos por supersession (anti-category-error FM-VM-16) |
> 59	| Frustrations | Sem capability de percepção fatorada; conteúdo scrapeado sem proveniência envenenaria o corpus que ele mesmo lê (FM-VM-03) |
> 60	| Tech-savviness | n/a (máquina — consome contratos de tool, não UI) |
> 61	| MCORCH usage pattern | Tool calls server-to-server com JWT ES256; toda percepção bem-sucedida vira nó `observation` + `content_mesh_asset`; falhas vão a `infra_health_logs service='vision-mcp'` |
> 62	| Quote | _(log)_ `tool=vision.describe_image status=ok cost_mco=2 node_id=<uuid> provenance=tenant` |
> 63	
> 64	---
> 65	
> 66	## 3. User Journey Maps
> 67	
> 68	### Journey 1: "Dar olhos ao Pantheon" (Gabriel, Happy Path)
> 69	
> 70	| Stage | Action | Touchpoint | Emotion | Opportunity |
> 71	|-------|--------|-----------|---------|-------------|
> 72	| Awareness | Percebe que as referências consolidadas dependem de scripts ad-hoc com chave global | Malha + scripts QA | 😐 Neutral | FM-VM-05 nomeado: per-user BYOK fail-closed |
> 73	| Consideration | Sobe a Fatia 1: container autenticado + `mesh.search` read-only | `docker ps` healthy + `curl` 401/200 | 🤔 Curious | Padrão auth/transport provado antes de qualquer tool billable |
> 74	| Activation | Configura BYOK (firecrawl/openrouter/gemini/mistral) no Settings card | `/dashboard/settings` (hook-first) | 😊 Excited | Mesma família Vault de credenciais já existente |
> 75	| Value | `vision.describe_image` + `deepsearch.scrape` + `mesh.consolidate_reference` num run pago — nó com UUID na malha, débito atômico no ledger | Tool calls + `agent_executions` + `SELECT` do nó | 🚀 Delighted | O cruzado mínimo (vision+grounding) monetizado e instrumentado (KPI-VM-003) |
> 76	| Retention | Pantheon consome o corpus de percepção; dashboard de uso mostra custo por tool com margem 4×-floor | Usage/ledger view + Neural HUD | ❤️ Loyal | Dogfooding alimenta a decisão GO/NO-GO do upsell |
> 77	
> 78	#### Edge Case 1: Saldo de mcoCoins insuficiente (402 no-balance)
> 79	> O saldo cai abaixo da classe da tool. O container retorna **HTTP 402 estruturado antes de qualquer leg de provider** — débito é na entrada, então **nenhuma cobrança parcial** ocorre. Em superfícies UI, toast PT-BR "Saldo insuficiente — recarregue para continuar"; em clients MCP, erro estruturado com `action`. O run não inicia; nenhum refund é necessário porque nada foi debitado.
> 80	
> 81	#### Edge Case 2: Sentinel bloqueia args hostis (bloqueio não cobra)
> 82	> Args de tool contêm payload de injeção. `inspectPrompt` L1/L2/L3 roda **após** a identidade ES256 e **antes** do débito: a chamada é bloqueada, `logSentinelBlock` grava em `infra_health_logs service='sentinel'`, e **zero mcoCoins são debitados** do tenant. O bloqueio nunca custa ao cliente.
> 83	
> 84	### Journey 2: "Cole 1 URL → login → conectado" (Otávio, Happy Path — OAuth 2.1)
> 85	
> 86	| Stage | Action | Touchpoint | Emotion | Opportunity |
> 87	|-------|--------|-----------|---------|-------------|
> 88	| Awareness | Descobre `com.mcorch/vision-mcp` no MCP Registry buscando "vision + grounding" | MCP Registry (`server.json`) | 😐 Neutral | Whitespace do cruzado visível na descrição honesta |
> 89	| Consideration | Cola `https://mcp.mcorch.com` no Claude Desktop; recebe `401` + `WWW-Authenticate … resource_metadata` (RFC 9728) | Client MCP → endpoint Streamable HTTP | 🤔 Curious | Zero config manual: o client resolve o AS sozinho |
> 90	| Activation | Browser abre, faz login (PKCE S256), autoriza scopes — **conectado** | OAuth 2.1 flow → consent screen | 😊 Excited | O padrão sandcastles/Roboflow validado, agora soberano |
> 91	| Value | Chama `vision.describe_image` de dentro do agente; cobrança atômica aparece no ledger; em falha de provider, refund automático restaura o saldo | Tool call + `agent_executions` + `refundMco` | 🚀 Delighted | Confiança de billing = pré-requisito de adoção (BO-VM-004) |
> 92	| Retention | Gera PAT em Connectors para o client headless de CI; baixa o Plugin Zip com skills PT-BR | `/dashboard/settings → Connectors` | ❤️ Loyal | Distribuição self-serve (Plugin + skills + registry) |
> 93	
> 94	#### Edge Case 1: Tenant sem credencial Firecrawl (402 no-credential, fail-closed)
> 95	> Otávio chama `deepsearch.scrape` sem ter configurado BYOK. O container **não cai em chave global silenciosa** (anti-pattern proibido): retorna `402 {error:"firecrawl_not_configured", action:"Configure your Firecrawl credentials at /dashboard/settings"}` — body literal verificável por `curl` (BAC-VM-002). Zero mcoCoins debitados; a quota de nenhum outro tenant é tocada.
> 96	
> 97	#### Edge Case 2: Job de minutos num client sem suporte a progress
> 98	> `deepsearch.run` num host que não consome notifications (ex.: Claude API connector, tools-only). A tool retorna `job_id` imediatamente; o client chama `deepsearch.poll` (custo 0) até o resultado — sobrevivendo a disconnects SSE, ao idle ~100s do Cloudflare (OTD-VM-013) e a janelas de wall-clock. Entrega parcial segue a regra de **partial-delivery refund** selada no FRD (FM-VM-07); nunca chamada bloqueante.
> 99	
> 100	### Journey 3: "Catálogo conforme sem claim falso" (Helena, Happy Path — fase Could/assistiva)
> 101	
> 102	| Stage | Action | Touchpoint | Emotion | Opportunity |
> 103	|-------|--------|-----------|---------|-------------|
> 104	| Awareness | Auditoria interna + pressão EAA/MPF: milhares de imagens de catálogo sem alt-text | Relatório de auditoria NBR 17225 | 😟 Anxious | ~99% de não-conformidade BR = greenfield (MR-VM-001) |
> 105	| Consideration | Avalia a matriz de paridade (§4.5) e a política de claims controlados — ninguém promete "conformidade automática" | Docs page + matriz de paridade | 🤔 Curious | Honestidade como diferencial vs vendors over-claim (FM-VM-17) |
> 106	| Activation | Engenharia dela conecta via MCP/API; roda batch de `vision.alt_text` (curto + longo + detecção de decorativa) | Batch assistivo + BYOK | 😊 Excited | Custo por imagem previsível (classe 2 mco) |
> 107	| Value | Saídas de baixa certeza chegam com confidence flag e caem na fila de revisão humana; o relatório de conformidade só sela o que foi revisado | Fila de revisão + relatório | 🚀 Delighted | "Propósito equivalente" WCAG 2.2 SC 1.1.1 com trilha de auditoria |
> 108	| Retention | Novas imagens do catálogo passam pelo mesmo pipeline; consumo recorrente de mcoCoins financia o plano | Pipeline contínuo + plano Pro/Enterprise | ❤️ Loyal | Pagador B2B sob compulsão legal; usuário BLV final nunca paga premium (BR-VM-010) |
> 109	
> 110	#### Edge Case 1: Imagem red-line (medicação/alérgeno/mobilidade/emergência)
> 111	> Uma imagem de rótulo de medicamento entra no batch com pergunta de dosagem. O **duty-of-care gate recusa categoricamente** (template ToS Be My Eyes), registra a recusa em `infra_health_logs service='vision-mcp'` e direciona à verificação humana. 100% de recusa em queries red-line é critério de aceite (KPI-VM-005, BAC-VM-003).
> 112	
> 113	#### Edge Case 2: Baixa confiança bloqueia o claim
> 114	> A descrição de uma imagem complexa sai com confidence baixa. A saída carrega linguagem hedge + flag explícita (ASSETS 2024 — anti-overtrust), **não entra** no relatório de conformidade sem aprovação humana, e o gancho de escalonamento (padrão híbrido Aira) é exposto. Nenhuma copy do produto afirma "NBR 17225-conformante" sem mapeamento requisito-a-requisito + revisão humana (OTD-VM-019).
> 115	
> 116	### Journey 4: Pantheon Agent (machine persona, compact flow)
> 117	
> 118	| Stage | Action | Material proof |
> 119	|-------|--------|----------------|
> 120	| Invoke | `scientist` chama `deepsearch.run` (JWT ES256 verificado, sub confiável) | Identity log; sentinel pass |
> 121	| Ground | Resultado de scrape passa por sentinel L2 sobre **texto extraído** antes de qualquer insert (FM-VM-03) | `infra_health_logs` em bloqueio |
> 122	| Persist | `mesh.consolidate_reference` grava nó com tag `scraped` + proveniência/licença/retenção — **nunca** em system nodes (`user_id IS NULL`) | UUID por `SELECT`; query prova zero scraped em system nodes |
> 123	| Learn | Observações decaem (FSRS-6/`stability_score`); fatos derivados suplantam versões antigas (supersession) | Regimes distinguíveis no schema do nó (FM-VM-16) |
> 124	
> 125	#### Edge Case: Conteúdo scrapeado hostil (injeção persistente)
> 126	> Página web contém instruções de injeção destinadas aos agentes que lerão o corpus. O sentinel L2 (lexicalScore/control-chars) bloqueia o insert; o conteúdo nunca vira nó; o evento é registrado. Trust por proveniência: mesmo conteúdo aprovado carrega tag `scraped` para que consumidores downstream ponderem a origem (BR-RISK-VM-007).
> 127	
> 128	---
> 129	
> 130	## 4. Feature Inventory (MoSCoW)
> 131	
> 132	> Effort: S=hours, M=days, L=week, XL=sprint. mcoCoins = classes da Seção 6 do blueprint (fórmula `ceil(usd/$0.018×4)`); **calibração inicial — medição material do $ real antes do fix** em `COIN_COSTS` + constante espelhada no serviço + asserção em `src/test/billing.test.ts` (OTD-VM-004). House constraints transversais a TODA feature: débito só via `deduct_mco_coins` RPC atômico + `refundMco` on-failure; sentinel `inspectPrompt` após identidade e antes de cobrar; ES256 JWKS antes de confiar no `sub`; credencial per-user fail-closed; RLS default-deny + `user_id`(+`project_id`); embed-on-insert na malha; UI nova nasce hook-first.
> 133	
> 134	### Must Have (MVP → v1.0 — Fatias 1–2)
> 135	
> 136	| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |
> 137	|----|---------|---------|-----------|--------|-------------|-------|
> 138	| PR-VM-001 | Container MCP soberano `mcorch_vision_mcp` (Streamable HTTP `127.0.0.1`, hardening anchor gitnexus: cap_drop/read_only/UID 1001/pids_limit, healthcheck, telemetria watchdog → Neural HUD) | P1, P4 | BR-VM-005, BR-VM-012 | L | n/a | Fatia 1; rede `mcorch-sovereign-net`; NUNCA campo `name:` no compose |
> 139	| PR-VM-002 | Gate de identidade ES256 JWKS **fail-closed** (jose `jwtVerify` + `createRemoteJWSet`; nunca `atob` cego no `sub`; anti-confused-deputy) | Todas | BR-VM-001 | M | n/a | SOP `docs/processes/edge-jwt-identity-verification.md`; 401 sem token / 200 com JWT user (mint via `scripts/qa/gen-user-jwt.ts`) |
> 140	| PR-VM-003 | `mesh.search` — busca semântica RLS-scoped na malha do tenant (`match_mcorch_nodes`) | P1, P4 | BR-VM-012 | S | 0–1 | 1ª tool (read-only, Fatia 1); prova o padrão auth/transport |
> 141	| PR-VM-004 | `vision.describe_image` — VLM QA sobre 1 imagem (Gemini/Qwen/Claude/GPT-5.x via BYOK) → texto/structuredContent | P1, P2, P4 | BR-VM-003, BR-VM-001 | M | 2 | Tool de entrada (lane imagem única $0.0006–0.0107); URL/host allowlist |
> 142	| PR-VM-005 | `vision.ocr` — documento → markdown/JSON (Mistral OCR 3 direta / PaddleOCR CPU) | P1, P2, P3 | BR-VM-003 | M | 1 / página | Mistral não está no OpenRouter → integração direta per-user; provenance tag |
> 143	| PR-VM-006 | `deepsearch.scrape` — 1 URL pública via Firecrawl BYOK (robots.txt + login-wall block + provenance) | P1, P2, P4 | BR-VM-002, BR-VM-005 | M | 1 | Logged-out only; allowlist de fontes permissivas; CDSM Art. 4 opt-out |
> 144	| PR-VM-007 | BYOK Settings card — migration coluna `user_api_keys.firecrawl_api_key` (Vault-encrypted, família existente) + UI hook-first + fail-closed `402 firecrawl_not_configured` | P1, P2, P3 | BR-VM-002 | M | 0 | `/security-review` na migration; VIEW mascarada → write `.insert` (nunca `.upsert`), teste server-side |
> 145	| PR-VM-008 | Billing atômico — débito na entrada via `deduct_mco_coins` (PostgREST + secret name `SB_SECRET_KEY`), `refundMco` em toda falha billable, metering por leg em `agent_executions`, **BYOK anda de graça** (`isUserCustomKey → 0`), HTTP 402 em saldo insuficiente, exempção `SOVEREIGN_USER_ID` | Todas | BR-VM-003, BR-VM-001 | M | transversal | Delta de `mco_balance` por `SELECT` before/after é o gate material (BAC-VM-001) |
> 146	| PR-VM-009 | Sentinel duplo — `inspectPrompt` L1/L2/L3 nos args (inbound) + L2 sobre **texto extraído** de scrape/OCR/VLM antes de insert na malha (FM-VM-02/03/04) | Todas | BR-VM-003, BR-VM-006 | S | 0 (bloqueio não cobra) | `logSentinelBlock → infra_health_logs service='sentinel'`; estender SOP a outputs de vision-tool (OWASP LLM01) |
> 147	| PR-VM-010 | `mesh.consolidate_reference` — grava referência consolidada como nó `observation` + `content_mesh_asset` (PII-strip, proveniência/licença/retenção, embed-on-insert grátis, BR/FR ID no metadata) com **dois regimes de persistência**: observações decaem (FSRS-6), fatos suplantam | P1, P4 | BR-VM-012, BR-VM-004, BR-VM-010 | M | 1 | Instrumenta o gate do cruzado (KPI-VM-003); scraped NUNCA em system nodes |
> 148	
> 149	### Should Have (Fatia 3 — exposição externa)
> 150	
> 151	| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |
> 152	|----|---------|---------|-----------|--------|-------------|-------|
> 153	| PR-VM-011 | Endpoint público `mcp.mcorch.com` — nginx vhost (proxy loopback, SSE `proxy_buffering off` + heartbeat) + OAuth 2.1 + RFC 9728 PRM (`/.well-known/oauth-protected-resource`), Origin 403, `MCP-Protocol-Version`, audience validation, token passthrough proibido | P2 | BR-VM-007 | XL | n/a | Decisão do AS (Supabase Auth fronteado vs vendor) é do SDD; vhost exige root + DNS Cloudflare (OTD-VM-013) |
> 154	| PR-VM-012 | PAT para clients long-lived — tabela `mcp_access_tokens` (hash SHA-256, nunca plaintext; scopes que EXCLUEM gestão de credencial; `expires_at`/`revoked_at`; RLS default-deny `auth.uid()=user_id`) + UI de gestão/revogação hook-first | P2 | BR-VM-006 | M | 0 | `/security-review` obrigatório na migration (FM-VM-06: PAT leak = dreno da carteira) |
> 155	| PR-VM-013 | `deepsearch.run` + `deepsearch.poll` — job semantics assíncrona dentro do container (submit → `job_id` + progress; poll grátis) com **partial-delivery refund** conforme regra selada no FRD | P2, P4 | BR-VM-003, BR-VM-006 | L | 3 / 0 | Nunca chamada bloqueante; sobrevive a Cloudflare/wall-clock (OTD-VM-003/013) |
> 156	| PR-VM-014 | Connectors UI + Plugin Zip versionado (connector URL pré-preenchida + skills PT-BR workflow-named `/vision-essence`, `/reference-brief`, `/competitive-vision`) baixável de `/dashboard/settings → Connectors` | P2, P3 | BR-VM-007 | M | 0 | Hook-first; tools workflow-named, não CRUD cru (lição Roboflow/sandcastles) |
> 157	| PR-VM-015 | Publicação no MCP Registry — `server.json` via `mcp-publisher` sob namespace verificado `com.mcorch/*` (challenge DNS/HTTP) | P2 | BR-VM-007 | S | 0 | Registry em preview → version-pinning + deprecation-watch no SDD |
> 158	| PR-VM-016 | RPC `erase_vision_artifacts(content_ref)` — cascade nó + edges + embedding + frames Storage + cópias provider, espelhando `erase_lead()` + retention clock (art. 16) | P3 | BR-VM-004 | M | 0 | Gate da Fatia 3 (antes do 1º tenant externo); prova zero resíduo por `SELECT` antes/depois |
> 159	| PR-VM-017 | Dashboard usage/ledger view — consumo mcoCoins por tool/tenant (hook-first sobre `agent_executions` + ledger), margem por tool visível ao Sovereign | P1, P2 | BR-VM-001, BR-VM-003 | M | 0 | Alimenta recalibração contínua (KPI-VM-004) |
> 160	
> 161	### Could Have (Future — expansão assistiva + loop cognitivo)
> 162	
> 163	| ID | Feature | Persona | BR Traced | Effort | mcoCoins/run | Notes |
> 164	|----|---------|---------|-----------|--------|-------------|-------|
> 165	| PR-VM-020 | `vision.alt_text` — alt-text curto + longo + detecção de imagem decorativa, "propósito equivalente" WCAG 2.2 SC 1.1.1 / NBR 17225, com duty-of-care gate + confidence flag | P3 | BR-VM-008 | L | 2 | Beachhead GTM (BO-VM-001, 6–12m pós-v1.0); claim de conformidade só com revisão humana + mapeamento NBR (OTD-VM-019) |
> 166	| PR-VM-021 | `vision.describe_screen` — descrição de screenshot/UI (padrão JAWS PictureSmart / NVDA Content Describer) com sinalização de incerteza | P3 | BR-VM-008 | M | 2 | Dual-backend OpenAI+Anthropic validado por terceiros; BYOK provider-agnóstico |
> 167	| PR-VM-022 | Batch assistivo — alt-text de catálogo em escala + fila de revisão humana + relatório de conformidade auditável | P3 | BR-VM-008, BR-VM-010 | XL | 2 / imagem | Monetização recai no B2B/compliance; usuário BLV final nunca paga premium |
> 168	| PR-VM-023 | `motion.peripheral_scan` — Tier 1 periférico (frame-diff/MOG2 + síntese de eventos + saliência → regiões salientes, `resource_link` p/ crops) | P1, P4 | BR-VM-011 | L | 0–1 | **Gated por OTD-VM-001**: alvo de recall medido em domínio screen/UI + custo de falso-negativo explícito ANTES de GA; bypass billable direto ao Tier 2 sempre disponível |
> 169	| PR-VM-024 | Tools foveais adicionais — `vision.detect_objects` (Gemini boxes), `vision.segment` (SAM-3 fal / SAM-2 Replicate), `vision.analyze_video` (Gemini video), `motion.track` (RTMPose + ByteTrack/BoT-SORT) | P1, P2 | BR-VM-003 | L | 2 / 2–5 / 2·min / 1 | Pista Apache default (FM-VM-08); keep-warm/batch contra cold start GPU (FM-VM-12) |
> 170	| PR-VM-025 | Loop cognitivo completo — prompts `/vision-essence` (pipeline Essência Humana E2E) + resources `mesh://nodes/{id}`, `mesh://references?pillar=…`, `vision://artifacts/{ref}` (signed URLs curtos) | P1, P4 | BR-VM-010, BR-VM-012 | M | herda classes | Resources/prompts = progressive enhancement (Claude API connector consome só tools); âncoras CoALA/V*/GraphRAG, nunca "cognitive computing" |
> 171	
> 172	### Won't Have (This Cycle)
> 173	
> 174	- **Reconhecimento facial / template biométrico / classificação biométrica — EXPLICITAMENTE Won't (LGPD art. 5º II + art. 11; FM-VM-09).** O escopo de visão é detecção/descrição; legítimo interesse NÃO se aplica a biométrico; qualquer exceção futura exige base art. 11 documentada + revisão da regulação ANPD 2026 (OTD-VM-007/008). Nenhuma tool de recognition na superfície publicada (BAC-VM — BRD).
> 175	- **Hardware neuromórfico** (sensores DVS Sony/Prophesee, Loihi 2, Akida on-prem) — o Tier 1 é **emulação em software** de princípios neuromórficos (v2e/OpenEB/frame-diff); comunicação sempre "event-like processing", jamais "microsecond sensing" (Pilar III; MR-VM-009).
> 176	- **LIBRAS / língua de sinais** — linha vermelha WFD+WASLI (avatar/MT ≠ intérprete humano); SignGemma é ASL→inglês não-GA (FM-VM-18; OTD-VM-018). Zero claim no v1.
> 177	- **Branding "cognitive computing" / "cérebro digital" / claims de consciência** — proibição BR-VM-009 (FM-VM-15); GWT só como metáfora de engenharia.
> 178	- **Authorization server proprietário construído do zero** — a decisão AS (Supabase Auth fronteado vs vendor WorkOS/Auth0) pertence ao SDD; o PRD só exige a conformidade RFC 9728/OAuth 2.1 observável.
> 179	
> 180	### 4.5 Assistive Baseline Parity Matrix (mandato BR-VM-010)
> 181	
> 182	> As tools assistivas devem **igualar o baseline grátis de big tech** antes de qualquer cobrança B2B — impossível cobrar do usuário BLV o que Seeing AI/Lookout dão de graça (MR-VM-015).
> 183	
> 184	| Capability | Seeing AI (free) | Google Lookout (free) | Vision MCP |
> 185	|------------|-----------------|----------------------|------------|
> 186	| Descrição rica de cena | ✅ | ✅ | `vision.describe_image` / `vision.describe_screen` (paridade exigida) |
> 187	| OCR de documento + estrutura | ✅ (chat-com-documento) | ✅ | `vision.ocr` (markdown/JSON estruturado) |
> 188	| Q&A sobre imagem | ✅ | ✅ (Gemini) | `vision.describe_image` em modo QA |
> 189	| Alt-text de conformidade (curto+longo, WCAG 2.2 SC 1.1.1 / NBR 17225) | ❌ (não é produto de compliance) | ❌ | `vision.alt_text` — **diferencial B2B** |
> 190	| Detecção de imagem decorativa | ❌ | ❌ | `vision.alt_text` |
> 191	| Dever de cuidado auditável (recusas red-line + confidence + escalonamento humano) | parcial (ToS) | parcial | Duty-of-care gate explícito + log + fila de revisão (FM-VM-14) |
> 192	| Capability componível (API/MCP, multi-host) | ❌ (app fechado) | ❌ (app fechado) | Toda a superfície MCP — **diferencial estrutural** |
> 193	| Self-host / soberania de dados | ❌ | ❌ | Container Sovereign Mesh + erasure LGPD em cascata |
> 194	| Grounding por deepsearch + malha de conhecimento | ❌ | ❌ | `mesh.consolidate_reference` (upsell gated KPI-VM-003) |
> 195	
> 196	**Leitura de pricing:** onde há ✅✅ na big tech, a tool MCORCH iguala e não cobra premium do usuário final BLV; o valor pago (B2B/compliance) vem das linhas ❌❌ — conformidade auditável, componibilidade e soberania.
> 197	
> 198	---
> 199	
> 200	## 5. Release Phasing
> 201	
> 202	> Fases = fatias do blueprint §9, cada uma com gate material (Lei 1). **Zero novas Edge Functions em todo o ciclo** — o runtime é container (timeouts matam a rota Edge; blueprint §5.1); reusa `embed-mcorch-node` (embed-on-insert), `get-infra-status` (Neural HUD) e o RPC `deduct_mco_coins` existente.
> 203	
> 204	### MVP Scope (= Fatia 1 — esqueleto autenticado, read-only, internal-only)
> 205	**Target date:** sprint dedicada pós-seal BoK (Fatia 0 = esta suíte + SOP `docs/processes/vision-mcp-credential-resolution.md`)  
> 206	**Included:** PR-VM-001, PR-VM-002, PR-VM-003  
> 207	**Success gate:** `docker ps`/`docker inspect` healthy com envelope hardened; `curl` interno → `200 /health`, `401` fail-closed sem token, `200` com JWT user (mint `scripts/qa/gen-user-jwt.ts`); nó da malha inserido com UUID retornado por `SELECT`.  
> 208	**NEW infra needed:** container `mcorch_vision_mcp` (Docker, fork do skeleton gitnexus). Nenhuma migration; nenhuma edge function nova.
> 209	
> 210	### v1.0 Scope (= Fatia 2 — Tier 2 foveal billable + per-user creds + refund)
> 211	**Target date:** após MVP validado com Usuário Zero  
> 212	**Adds:** PR-VM-004, PR-VM-005, PR-VM-006, PR-VM-007, PR-VM-008, PR-VM-009, PR-VM-010  
> 213	**Success gate:** run pago E2E com ledger `agent_executions` + delta de `mco_balance` por `SELECT` before/after; `402` literal em saldo insuficiente; `402 firecrawl_not_configured` sem credencial; refund material em falha forçada (saldo restaurado por `SELECT`); `/security-review` SAFE na migration da coluna (BAC-VM-001/002).  
> 214	**NEW infra needed:** migration `user_api_keys.firecrawl_api_key` (Vault trigger family + `/security-review`); Settings BYOK card hook-first. Nenhuma edge function nova.
> 215	
> 216	### Future Scope (= Fatia 3+ — exposição externa + expansão assistiva/cognitiva)
> 217	**Items:** PR-VM-011..017 (Fatia 3), depois PR-VM-020..025 (expansão gated)  
> 218	**Condition:** Fatia 3 só após BO-VM-006 (gate LGPD: `erase_vision_artifacts` + escopo biométrico selado) — pré-requisito do 1º tenant externo. PR-VM-020..022 (assistivas) só após duty-of-care suite adversarial 100% verde (KPI-VM-005) + mapeamento NBR 17225 (OTD-VM-019). PR-VM-023 só após benchmark de recall do Tier 1 (OTD-VM-001). Investimento GTM no cruzado só após GO no gate KPI-VM-003 (OTD-VM-002).  
> 219	**NEW infra needed (Fatia 3):** nginx vhost `mcp.mcorch.com` + DNS Cloudflare (root — OTD-VM-013); migration `mcp_access_tokens` (`/security-review`); migration RPC `erase_vision_artifacts`; Plugin Zip pipeline; entry `server.json` no registry. Nenhuma edge function nova.
> 220	
> 221	---
> 222	
> 223	## 6. Luxury UX Specifications
> 224	
> 225	> **O módulo é majoritariamente headless** — o produto é a superfície MCP. A UX visível ao humano se concentra em **4 superfícies**, todas nascendo **hook-first** (lógica no hook, componente display-only):
> 226	
> 227	| Surface | Backing hook (nasce primeiro) | Data source | PR |
> 228	|---------|------------------------------|-------------|-----|
> 229	| Settings → Vision/Deepsearch BYOK card | `useUserApiKeys` (estende família existente com `firecrawl_api_key`) | `user_api_keys` (VIEW mascarada — write `.insert`, nunca `.upsert`; teste de chave server-side) | PR-VM-007 |
> 230	| Settings → Connectors (URL MCP + PAT + Plugin Zip) | `useMcpTokens` (novo — TanStack Query) | `mcp_access_tokens` (RLS `auth.uid()=user_id`) | PR-VM-012, PR-VM-014 |
> 231	| Dashboard usage/ledger view | `useVisionUsage` (novo — TanStack Query) | `agent_executions` + ledger mcoCoins | PR-VM-017 |
> 232	| Docs page pública (onboarding + claims controlados) | estática (sem hook) | docs versionadas com o Plugin | PR-VM-014 |
> 233	
> 234	### 6.1 Color & Visual Identity
> 235	
> 236	| Token | Value | Usage |
> 237	|-------|-------|-------|
> 238	| `--bg-deep` | `#0A0A0F` | Canvas background (dark mesh) |
> 239	| `--accent-violet` | `#7C3AED` | Primary CTA, estado conectado, badges de tool ativa |
> 240	| `--accent-cyan` | `#06B6D4` | Ledger/uso, gráficos de consumo por tool |
> 241	| `--glass-surface` | `rgba(255,255,255,0.04)` | Cards de credencial/PAT/uso |
> 242	| `--border-subtle` | `rgba(255,255,255,0.08)` | Bordas de card |
> 243	
> 244	### 6.2 Animation Guidelines
> 245	
> 246	| Element | Library | Duration | Easing |
> 247	|---------|---------|----------|--------|
> 248	| Card de conexão (estado conectado/erro) | Framer Motion | 300ms | `easeInOut` |
> 249	| Entrada de PAT recém-gerado (reveal único) | Framer Motion | 300ms | `spring(stiffness:80)` |
> 250	| Pulso de uso live (ledger atualizando) | CSS keyframes | 2s | `ease-in-out infinite` |
> 251	| Micro-interactions (copy URL, revogar token) | Framer Motion | 150ms | `easeOut` |
> 252	| `prefers-reduced-motion` | — | todas as animações reduzidas a fade ≤100ms | respeitado globalmente |
> 253	
> 254	### 6.3 Interaction Patterns
> 255	
> 256	- **Cards:** glass morphism — `backdrop-blur-sm`, borda sutil, shadow `0 4px 24px rgba(0,0,0,0.4)`.
> 257	- **PAT reveal:** o token é exibido UMA vez na geração (depois só hash/prefixo); botão copiar com confirmação acessível; revogação com confirm dialog navegável por teclado.
> 258	- **Estados de credencial:** conectado (violet) / não-configurado (neutro + CTA "Configurar") / erro de teste server-side (red + mensagem PT-BR acionável). Nunca exibir valor de secret — apenas máscara + nome.
> 259	- **Erros de billing:** 402 vira toast PT-BR acionável ("Saldo insuficiente — recarregue para continuar" / "Configure sua credencial Firecrawl em Configurações") via `sonner`; sucesso = violet, erro = red, info = cyan.
> 260	- **Loading:** skeleton shimmer com `aria-busy="true"` (nunca spinner em área de conteúdo).
> 261	
> 262	### 6.4 Accessibility — WCAG 2.2 AA exemplar (este módulo VENDE acessibilidade)
> 263	
> 264	> Padrão de régua: a própria UI do módulo que vende alt-text de conformidade é **vitrine** — auditada contra WCAG 2.2 AA completo, incluindo os SCs novos da 2.2, antes de cada release.
> 265	
> 266	- **Contraste ≥ 4.5:1** para todo texto sobre superfícies de vidro (verificado por tooling, não a olho).
> 267	- **100% navegável por teclado** — geração/revogação de PAT, copy de URL, formulários BYOK; ordem de foco lógica; indicador de foco visível ≥ 2px e **nunca obscurecido** (SC 2.4.11 Focus Not Obscured).
> 268	- **Alvos de toque ≥ 24×24px** (SC 2.5.8 Target Size — Minimum) em todos os controles, inclusive ícones de revogar/copiar.
> 269	- **Zero interação dependente de arrastar** (SC 2.5.7 Dragging Movements) — todas as ações têm alternativa de clique simples.
> 270	- **Ajuda consistente** (SC 3.2.6 Consistent Help): link de docs/suporte na mesma posição em todas as superfícies do módulo.
> 271	- **Sem reentrada redundante** (SC 3.3.7 Redundant Entry): onboarding de credencial nunca pede o mesmo dado duas vezes.
> 272	- **Autenticação acessível** (SC 3.3.8 Accessible Authentication): fluxo OAuth/PAT sem teste cognitivo (sem transcrição manual de token quando copy/paste está disponível).
> 273	- **ARIA completo:** labels em botões icon-only; `role="status"` em toasts; live regions para mudanças de estado de conexão; tabelas de ledger com headers associados.
> 274	- **Dogfooding obrigatório:** toda imagem da docs page usa alt-text gerado por `vision.alt_text` **e revisado por humano** (claim controlado — FM-VM-17); leitura real com NVDA/JAWS no checklist de release; auditoria axe/Lighthouse + E2E UI audit 1920×1080 quando houver UI nova (gate Lei 1).
> 275	
> 276	---
> 277	
> 278	## 7. Acceptance Criteria (Gherkin)
> 279	
> 280	```gherkin
> 281	Feature: Percepção visual + deepsearch fundamentado como capability MCP soberana e billable
> 282	
> 283	  Scenario: Run pago interno com consolidação na malha (PR-VM-004, PR-VM-008, PR-VM-010)
> 284	    Given um tenant autenticado com JWT ES256 verificado via JWKS e saldo suficiente
> 285	    When ele chama vision.describe_image e em seguida mesh.consolidate_reference
> 286	    Then 2 mcoCoins e 1 mcoCoin são debitados atomicamente via deduct_mco_coins RPC
> 287	    And cada execução aparece em agent_executions ligada ao user_id verificado
> 288	    And um nó observation com content_mesh_asset é inserido com user_id+project_id e embeddado
> 289	    And o UUID do nó é retornável por SELECT (prova material)
> 290	
> 291	  Scenario: Falha de provider restaura o saldo (PR-VM-008)
> 292	    Given um run billable em andamento já debitado na entrada
> 293	    When a leg de provider falha de forma irrecuperável
> 294	    Then refundMco credita o valor integral de volta
> 295	    And o delta de mco_balance por SELECT before/after é zero
> 296	    And a falha é registrada em infra_health_logs com service='vision-mcp'
> 297	
> 298	  Scenario: Saldo insuficiente retorna 402 sem cobrança parcial (Edge Case J1.1)
> 299	    Given um tenant cujo saldo é menor que a classe da tool chamada
> 300	    When a tool é invocada
> 301	    Then a resposta é HTTP 402 estruturado antes de qualquer leg de provider
> 302	    And nenhum mcoCoin é debitado
> 303	    And em superfície UI um toast PT-BR "Saldo insuficiente" é exibido
> 304	
> 305	  Scenario: Credencial Firecrawl ausente falha fechado (PR-VM-007, Edge Case J2.1)
> 306	    Given um tenant sem firecrawl_api_key configurada em user_api_keys
> 307	    When ele chama deepsearch.scrape
> 308	    Then a resposta é 402 {error:"firecrawl_not_configured", action:"Configure your Firecrawl credentials at /dashboard/settings"}
> 309	    And nenhuma chave global de ambiente é usada no caminho user-facing
> 310	    And zero mcoCoins são debitados
> 311	
> 312	  Scenario: Sentinel bloqueia antes de cobrar (PR-VM-009)
> 313	    Given args de tool contendo payload de injeção detectável (L1/L2/L3)
> 314	    When a tool é invocada por identidade válida
> 315	    Then inspectPrompt bloqueia a chamada após a identidade e antes do débito
> 316	    And zero mcoCoins são debitados do tenant
> 317	    And o bloqueio é registrado em infra_health_logs com service='sentinel'
> 318	
> 319	  Scenario: Cole 1 URL, login, conectado — e cobrado corretamente (PR-VM-011, PR-VM-012)
> 320	    Given um client MCP externo (Claude Desktop) apontado para https://mcp.mcorch.com
> 321	    When o client envia POST initialize sem credencial
> 322	    Then a resposta é 401 com WWW-Authenticate contendo resource_metadata (RFC 9728)
> 323	    When o usuário completa o fluxo OAuth 2.1 com PKCE S256 no browser
> 324	    Then o client conecta e lista as tools
> 325	    And uma tool call subsequente debita mcoCoins contra o user_id do token verificado
> 326	
> 327	  Scenario: Job de deepsearch de minutos sobrevive ao client (PR-VM-013, Edge Case J2.2)
> 328	    Given um job deepsearch.run submetido por um client tools-only
> 329	    When o client desconecta e chama deepsearch.poll com o job_id mais de 150 segundos depois
> 330	    Then o resultado completo é entregue pelo poll (custo 0)
> 331	    And em caso de entrega parcial o refund segue a regra de partial-delivery selada no FRD
> 332	
> 333	  Scenario: Recusa categórica red-line assistiva (PR-VM-020/021, Edge Case J3.1)
> 334	    Given uma imagem de rótulo de medicamento e uma query de dosagem em tool assistiva
> 335	    When o duty-of-care gate avalia a chamada
> 336	    Then a resposta é uma recusa categórica com direcionamento à verificação humana
> 337	    And a recusa é registrada em infra_health_logs (cobertura 100% — KPI-VM-005)
> 338	    And nenhuma descrição de dosagem é gerada
> 339	
> 340	  Scenario: Erasure LGPD cascateia sem resíduo (PR-VM-016)
> 341	    Given artefatos de visão persistidos (nó + edges + embedding + frames em Storage)
> 342	    When erase_vision_artifacts(content_ref) é executada
> 343	    Then a contagem por SELECT em todas as superfícies antes/depois prova zero resíduo
> 344	
> 345	  Scenario: BYOK anda de graça (PR-VM-008)
> 346	    Given um tenant com chave própria de provider resolvida (isUserCustomKey)
> 347	    When uma leg LLM executa com essa chave
> 348	    Then o custo de metering registrado é 0
> 349	    And a receita do tenant vem do plano, não de markup sobre a API dele
> 350	```
> 351	
> 352	---
> 353	
> 354	## 8. Traceability Matrix
> 355	
> 356	> Sela os stubs do MRD §9 e do BRD §10 (coluna PR). MR → BR → PR completo.
> 357	
> 358	| MR ID | BR ID | PR ID |
> 359	|-------|-------|-------|
> 360	| MR-VM-001 | BR-VM-008 | PR-VM-020, PR-VM-021, PR-VM-022 |
> 361	| MR-VM-002 | BR-VM-008 | PR-VM-020, PR-VM-021 |
> 362	| MR-VM-003 | BR-VM-008, BR-VM-006 | PR-VM-020, PR-VM-022 (claims controlados — relatório só com revisão humana) |
> 363	| MR-VM-004 | BR-VM-010 | PR-VM-010, PR-VM-025 (cruzado instrumentado, gate KPI-VM-003) |
> 364	| MR-VM-005 | BR-VM-006, BR-VM-007 | PR-VM-011, PR-VM-012, PR-VM-015 |
> 365	| MR-VM-006 | BR-VM-005 | PR-VM-001 |
> 366	| MR-VM-007 | BR-VM-001, BR-VM-002 | PR-VM-002, PR-VM-007 |
> 367	| MR-VM-008 | BR-VM-003 | PR-VM-008, PR-VM-009, PR-VM-017 |
> 368	| MR-VM-009 | BR-VM-011, BR-VM-009 | PR-VM-023 (+ Won't Have: hardware neuromórfico / "microsecond sensing") |
> 369	| MR-VM-010 | BR-VM-004, BR-VM-005 | PR-VM-001, PR-VM-010, PR-VM-016 |
> 370	| MR-VM-011 | BR-VM-003, BR-VM-006 | PR-VM-013 |
> 371	| MR-VM-012 | BR-VM-007 | PR-VM-014, PR-VM-015 |
> 372	| MR-VM-013 | BR-VM-009 | Transversal — checklist anti-hype de copy por release (BAC-VM-009; sem PR de feature) |
> 373	| MR-VM-014 | BR-VM-012 | PR-VM-003, PR-VM-010 |
> 374	| MR-VM-015 | BR-VM-010, BR-VM-003 | PR-VM-020, PR-VM-021, PR-VM-022 + matriz de paridade §4.5 |
> 375	| MR-VM-016 | BR-VM-006 | Won't Have — LIBRAS/sign language excluído explicitamente (FM-VM-18) |
> 376	
> 377	---
> 378	
> 379	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 380	
> ```

## 🤖 Claude *(18:49:51)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/vision-mcp/04-frd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# FRD — Functional Requirements Document
> 2	
> 3	**Project:** vision-mcp  
> 4	**Version:** v0.1 | **Date:** 2026-06-11  
> 5	**BoK Applied:** SWEBOK v4 (Software Requirements)  
> 6	**Status:** Complete  
> 7	**Source of Truth:** `docs/bok/vision-mcp/00-deepsearch-blueprint.md` (v0.2.0) + `01-mrd.md` (MR-VM-001..016) + `02-brd.md` (BR-VM-001..012) + `03-prd.md` (PR-VM-001..025) — todo FR-VM deste documento rastreia ≥1 PR-VM; IDs do blueprint (FM-VM-01..18, OTD-VM-001..019) preservados verbatim; ambiguidades viram OTD, nunca improvisação.  
> 8	**Market segment:** B2B2C · **Monetization:** híbrida (mcoCoins por tool call + planos Starter/Pro/Enterprise) · **Regulatory:** LGPD ELEVADO (biométrico art. 11) · **Integration surface:** extends-mcorch
> 9	
> 10	---
> 11	
> 12	## 1. Scope Statement
> 13	
> 14	This document specifies the functional and non-functional requirements for `vision-mcp`.
> 15	It is derived from PRD `03-prd.md` and feeds directly into SDD `05-sdd.md`.
> 16	
> 17	**In scope:** servidor MCP soberano de percepção visual + deepsearch fundamentado em container `mcorch_vision_mcp` (Sovereign Mesh, precedente gitnexus) — transporte Streamable HTTP 2025-11-25; identidade ES256 JWKS fail-closed + OAuth 2.1/RFC 9728 + PAT `mcp_access_tokens`; resolução de credencial per-user fail-closed (coluna `user_api_keys.firecrawl_api_key`); sentinel duplo (inbound + texto extraído); superfície de tools com classes mcoCoin (débito atômico + refund-on-failure + **regra de partial-delivery refund selada neste documento**, §4.5); Mesh Connection Mandate com dois regimes de persistência; erasure LGPD em cascata + retention clock; gate periférico Tier 1 com alvo de recall; distribuição Plugin Zip + skills + MCP Registry; expansão assistiva (`vision.alt_text`/`vision.describe_screen` + duty-of-care) e cognitiva (resources/prompts) gated.
> 18	
> 19	**Out of scope (this cycle):** reconhecimento facial/template biométrico/classificação biométrica (LGPD art. 11 — FM-VM-09); hardware neuromórfico (Tier 1 é emulação em software — "event-like processing", nunca "microsecond sensing"); LIBRAS/língua de sinais (FM-VM-18, OTD-VM-018); branding "cognitive computing"/"cérebro digital"/claims de consciência (BR-VM-009); authorization server proprietário do zero (decisão AS = SDD); **zero novas Edge Functions** — o runtime é container (timeouts matam a rota Edge; blueprint §5.1), reusando `embed-mcorch-node`, `get-infra-status` e o RPC `deduct_mco_coins` existentes.
> 20	
> 21	---
> 22	
> 23	## 2. Functional Requirements
> 24	
> 25	> Category: `Container service` | `EdgeFunction` (reuso apenas — zero novas) | `Hook` | `UI` | `DB` | `Cron`.  
> 26	> House constraints transversais a TODO FR: débito **só** via `deduct_mco_coins` RPC atômico + `refundMco` on-failure; sentinel `inspectPrompt` **após** identidade e **antes** de cobrar; ES256 JWKS verify antes de confiar no `sub` (SOP `docs/processes/edge-jwt-identity-verification.md` — nunca `atob` cego); credencial per-user fail-closed (API Tenancy Model); toda tabela nova RLS default-deny + `user_id` (+`project_id` na malha); embed-on-insert em todo fluxo `mcorch_nodes`; UI nova nasce hook-first; nomes de secrets apenas (ex.: `SB_SECRET_KEY`), nunca valores.
> 27	
> 28	### 2.1 Transport, Identity & Access (Fatias 1 e 3)
> 29	
> 30	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 31	|----|-------|-------------|----------|-----------|----------|---------|
> 32	| FR-VM-001 | Streamable HTTP Transport (spec 2025-11-25) | Endpoint MCP único Streamable HTTP: POST → `application/json` ou `text/event-stream`; GET → SSE server-initiated. Validar header `Origin` contra allowlist — inválido → **HTTP 403** (anti DNS-rebinding). Honrar `MCP-Protocol-Version` por request (mismatch → 400 estruturado). Semântica de disconnect/resume do SSE para sobreviver a wall-clock/Cloudflare (heartbeat ≤25s — OTD-VM-013). Loopback-only (`127.0.0.1:<porta>`) atrás do nginx vhost `mcp.mcorch.com` (`proxy_buffering off`) | Critical | PR-VM-001, PR-VM-011 | Container service | AT-VM-001 |
> 33	| FR-VM-002 | Identity ES256 JWKS fail-closed + OAuth 2.1/RFC 9728 | Toda request autenticada: verificar JWT via `jose` `jwtVerify` + `createRemoteJWKSet` contra `…/auth/v1/.well-known/jwks.json` **antes** de confiar no `sub` (anti-confused-deputy). Sem token/inválido/expirado → **401** com `WWW-Authenticate … resource_metadata="https://mcp.mcorch.com/.well-known/oauth-protected-resource"` (RFC 9728 PRM). JWKS inalcançável → fail-closed (rejeita; nunca processa). OAuth 2.1: PKCE S256, audience validation, token passthrough proibido, bearer só em header `Authorization` (nunca query string) | Critical | PR-VM-002, PR-VM-011 | Container service | AT-VM-002 |
> 34	| FR-VM-003 | PAT `mcp_access_tokens` | Tabela `mcp_access_tokens` (`user_id`, `token_hash` SHA-256 — nunca plaintext/Vault-reversível, `token_prefix` p/ exibição, `scopes text[]`, `expires_at`, `revoked_at`, `last_used_at`) com RLS default-deny `auth.uid()=user_id`. Scopes EXCLUEM gestão de credencial e billing (FM-VM-06). Lookup por hash em O(1); token revogado/expirado → 401. UI de geração/revogação hook-first (`useMcpTokens`); token exibido UMA vez na geração. Migration passa `/security-review` antes do commit | Critical | PR-VM-012 | DB + Hook + UI | AT-VM-003 |
> 35	| FR-VM-004 | Per-user credential resolution fail-closed | Ordem mandatória: (1) `decrypted_user_api_keys` por `user_id` verificado (firecrawl/openrouter/gemini/mistral); (2) env vault SÓ cron/service-role; (3) hard-fail **402 estruturado** `{error:"<service>_not_configured", action:"Configure your <service> credentials at /dashboard/settings"}`. Nova coluna `user_api_keys.firecrawl_api_key` (Vault-encrypted, família trigger existente; padrão 1-linha da migration `20260601060000`). Zero env-key global em path user-facing; quota de um tenant nunca esgota a de outro | Critical | PR-VM-007 | DB + Container service | AT-VM-004 |
> 36	| FR-VM-016 | Container runtime hardened + watchdog | Container `mcorch_vision_mcp` na rede `mcorch-sovereign-net` com hardening anchor gitnexus (`cap_drop`/`read_only`/UID 1001/`pids_limit`), healthcheck node, NUNCA campo `name:` no compose. Telemetria de health → `infra_health_logs` via `scripts/watchdog-mcorch.sh` (cron */5) → Neural HUD via `get-infra-status` | Critical | PR-VM-001 | Container service + Cron | AT-VM-016 |
> 37	
> 38	### 2.2 Billing & Safety (transversal — Fatia 2)
> 39	
> 40	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 41	|----|-------|-------------|----------|-----------|----------|---------|
> 42	| FR-VM-005 | Sentinel duplo (inbound + extracted) | (a) `inspectPrompt` L1/L2/L3 (`_shared/sentinel.ts`, portado a Node) sobre args de TODA tool, **após** identidade e **antes** do débito — bloqueio → **403 estruturado**, zero mcoCoins debitados, `logSentinelBlock → infra_health_logs service='sentinel'`. (b) Sentinel L2 (lexicalScore/control-chars) sobre **texto extraído** de scrape/OCR/VLM antes de qualquer insert na malha (FM-VM-03/04 — injeção persistente; OWASP LLM01); conteúdo bloqueado nunca vira nó | Critical | PR-VM-009 | Container service | AT-VM-005 |
> 43	| FR-VM-006 | Tool surface billable (classes mcoCoin) | Registro de tools com classe mco por tool (BRD §6: describe_image 2, ocr 1/página, scrape 1, run 3, poll 0, mesh.search 0–1, consolidate_reference 1, alt_text/describe_screen 2, peripheral_scan 0–1, track 1, detect 2, segment 2/5, video 2/min). Débito **na entrada** via `deduct_mco_coins(p_user_id, p_amount, p_action, p_context)` (PostgREST + secret name `SB_SECRET_KEY`) contra `sub` verificado; saldo insuficiente → **402** antes de qualquer leg de provider. `refundMco` em TODA falha billable (credit service-role-only, nunca lança). Metering por leg em `agent_executions`; **BYOK anda de graça** (`isUserCustomKey → cost 0`); exempção `SOVEREIGN_USER_ID`. Classes espelhadas em `src/lib/billing.ts → COIN_COSTS` + constante hardcoded no serviço + asserção em `src/test/billing.test.ts`; fix de preço só após medição material do $ (OTD-VM-004) | Critical | PR-VM-008 | Container service + DB | AT-VM-006 |
> 44	| FR-VM-007 | Async job semantics + partial-delivery refund | `deepsearch.run` → débito integral na entrada → retorna `job_id` imediato (p95 <2s) + progress notifications quando o host suporta; `deepsearch.poll(job_id)` custo 0 entrega estado/resultado (tools-only hosts — OTD-VM-003). Máquina de estados `queued→running→done|partial|failed`; jobs tenant-scoped (poll exige mesma identidade verificada); resultado disponível p/ poll ≥24h pós-terminal; nunca chamada bloqueante. **Regra de partial-delivery refund selada em §4.5** (FM-VM-07): 0 unidades entregues → refund integral; entrega parcial → cobrança proporcional arredondada A FAVOR do tenant, resultado com `partial:true` | Critical | PR-VM-013 | Container service | AT-VM-007 |
> 45	
> 46	### 2.3 Tool Surface — Fatia 1–2 (interno, cruzado mínimo)
> 47	
> 48	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 49	|----|-------|-------------|----------|-----------|----------|---------|
> 50	| FR-VM-017 | `mesh.search` (read-only, 1ª tool) | Busca semântica RLS-scoped na malha do tenant via RPC `match_mcorch_nodes` (pgvector 768). Custo 0–1; prova o padrão auth/transport da Fatia 1 antes de qualquer tool billable | Critical | PR-VM-003 | Container service | AT-VM-017 |
> 51	| FR-VM-018 | `vision.describe_image` | VLM QA sobre 1 imagem (Gemini/Qwen/Claude/GPT-5.x via BYOK per-user) → texto + `structuredContent`. Input gate: URL https + host allowlist + content-type/size cap (§5). Classe 2 mco (lane imagem única $0.0006–0.0107) | Critical | PR-VM-004 | Container service | AT-VM-018 |
> 52	| FR-VM-019 | `vision.ocr` | Documento → markdown/JSON estruturado. Backend Mistral OCR 3 (integração direta per-user — não está no OpenRouter) ou PaddleOCR CPU. Classe 1 mco/página; provenance tag obrigatória na saída; texto extraído passa sentinel L2 antes de qualquer insert (FR-VM-005b) | Critical | PR-VM-005 | Container service | AT-VM-019 |
> 53	| FR-VM-020 | `deepsearch.scrape` | Scrape de 1 URL pública via Firecrawl BYOK (fail-closed FR-VM-004), logged-out only. Gates: robots.txt honrado, login-wall block, allowlist de fontes permissivas, CDSM Art. 4 opt-out. Saída markdown + metadata de proveniência/licença. Classe 1 mco | Critical | PR-VM-006 | Container service | AT-VM-020 |
> 54	| FR-VM-021 | `mesh.consolidate_reference` | Grava referência consolidada (saída de visão fundamentada por deepsearch) como nó `observation` + `content_mesh_asset` (template `orchestrate-step`): PII-strip antes do insert, tag `scraped` + proveniência/licença/`retention_until`, `metadata.cost_mco`, BR/FR ID de traceabilidade, embed-on-insert grátis via `embed-mcorch-node`. **NUNCA em system nodes** (`user_id IS NULL`). Edge ao nó do run instrumenta o gate do cruzado (KPI-VM-003). Classe 1 mco | Critical | PR-VM-010 | Container service + DB | AT-VM-021 |
> 55	| FR-VM-008 | Mesh Connection Mandate | Toda percepção bem-sucedida insere nó `observation` na malha (`user_id+project_id`, `stability_score 1.0`, embed-on-insert); toda falha → `infra_health_logs service='vision-mcp'` (fire-and-forget); cada nó/log carrega o BR/FR ID rastreável. Health do container no Neural HUD (FR-VM-016) | Critical | PR-VM-010 | Container service + DB | AT-VM-008 |
> 56	| FR-VM-015 | Regimes de persistência de memória | Nós originados de visão tipados em dois regimes distinguíveis no schema: **observações decaem** (FSRS-6/`stability_score`); **fatos derivados suplantam** versões antigas (supersession, sem decay) — anti-category-error arXiv 2604.11364 (FM-VM-16). `mesh.consolidate_reference` exige declaração do regime no insert | High | PR-VM-010, PR-VM-025 | DB + Container service | AT-VM-015 |
> 57	
> 58	### 2.4 LGPD & Data Sovereignty (gate da Fatia 3)
> 59	
> 60	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 61	|----|-------|-------------|----------|-----------|----------|---------|
> 62	| FR-VM-009 | `erase_vision_artifacts` + retention clock | RPC `erase_vision_artifacts(content_ref)` SECURITY DEFINER espelhando `erase_lead()`: cascade nó + edges + embedding + frames/crops em Storage + registro de cópias provider; prova zero resíduo por `SELECT` count antes/depois (BAC-VM-005). Retention clock (art. 16): todo nó de visão carrega `retention_until`; sweep periódico expira artefatos vencidos. Migration passa `/security-review`. Pré-requisito do 1º tenant externo (BO-VM-006) | Critical | PR-VM-016 | DB + Cron | AT-VM-009 |
> 63	
> 64	### 2.5 Peripheral Tier & Foveal Expansion (gated)
> 65	
> 66	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 67	|----|-------|-------------|----------|-----------|----------|---------|
> 68	| FR-VM-010 | Tier-1 peripheral gate com alvo de recall | `motion.peripheral_scan`: frame-diff/MOG2 + síntese de eventos (v2e/OpenEB-style) + saliência → regiões salientes (`resource_link` p/ crops), CPU, classe 0–1 mco. **Modelo de saliência: SUM** (WACV 2025, MIT, self-hostável — OTD-VM-001 FECHADA; DeepGaze NÃO transfere p/ UI). **Condição de GA:** recall medido em **benchmark de domínio UEyes (CHI 2023) + Imp1k** (V*Bench/SEAL = PoC do padrão, não métrica de domínio) ≥ **0.95** via AUC-Judd/sAUC com threshold calibrado. **Justificativa da assimetria (recall≫precisão):** falso-negativo do Tier 1 = região que o Tier 2 NUNCA examina = cegueira permanente irrecuperável; falso-positivo só gasta compute foveal (recuperável) — calibração de cascata estilo Viola-Jones. Antes do GA: tool `experimental`, fallback frame-diff/MOG2 sem ML é GA-safe, bypass billable direto ao Tier 2 SEMPRE disponível. Comunicação "event-like processing", nunca "microsecond sensing" | High | PR-VM-023 | Container service | AT-VM-010 |
> 69	| FR-VM-024 | Tools foveais adicionais | `vision.detect_objects` (Gemini native boxes `[ymin,xmin,ymax,xmax]`, 2 mco); `vision.segment` (SAM-3 fal 2 mco / SAM-2 Replicate 5 mco — pista Apache default FM-VM-08); `vision.analyze_video` (Gemini video 1 FPS, cap de duração, 2 mco/min); `motion.track` (RTMPose/MediaPipe + ByteTrack/BoT-SORT, GPU ≤8s, 1 mco; keep-warm/batch contra cold start FM-VM-12) | Medium | PR-VM-024 | Container service | AT-VM-024 |
> 70	
> 71	### 2.6 Distribution & Human Surfaces (Fatia 3 — hook-first)
> 72	
> 73	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 74	|----|-------|-------------|----------|-----------|----------|---------|
> 75	| FR-VM-011 | Plugin Zip + skills + MCP Registry | Plugin Zip versionado (connector URL pré-preenchida + skills PT-BR workflow-named `/vision-essence`, `/reference-brief`, `/competitive-vision`) baixável de `/dashboard/settings → Connectors` (UI display-only sobre `useMcpTokens`/hook de Connectors). Publicação `server.json` via `mcp-publisher` sob namespace verificado `com.mcorch/*` (challenge DNS/HTTP); registry em preview → version-pinning + deprecation-watch no SDD | Medium | PR-VM-014, PR-VM-015 | UI + Hook | AT-VM-011 |
> 76	| FR-VM-022 | BYOK Settings card | Card Vision/Deepsearch em `/dashboard/settings` estendendo `useUserApiKeys` com `firecrawl_api_key`. `user_api_keys` é VIEW mascarada → write via `.insert` (NUNCA `.upsert`); null não limpa (clear via RPC); teste de chave server-side (cliente só vê máscara). Estados: conectado / não-configurado + CTA / erro com mensagem PT-BR acionável | Critical | PR-VM-007 | UI + Hook + DB | AT-VM-022 |
> 77	| FR-VM-023 | Usage/ledger dashboard | View de consumo mcoCoins por tool/tenant via hook novo `useVisionUsage` (TanStack Query sobre `agent_executions` + ledger); margem por tool visível ao Sovereign; alimenta recalibração KPI-VM-004 | Medium | PR-VM-017 | UI + Hook | AT-VM-023 |
> 78	
> 79	### 2.7 Assistive Expansion (Could — gated por KPI-VM-005 + OTD-VM-019)
> 80	
> 81	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 82	|----|-------|-------------|----------|-----------|----------|---------|
> 83	| FR-VM-012 | `vision.alt_text` | Alt-text curto + longo + detecção de imagem decorativa servindo "propósito equivalente" (WCAG 2.2 SC 1.1.1 / NBR 17225). Saída inclui confidence flag; claim "conformante" SÓ com caminho de revisão humana + mapeamento requisito-a-requisito da NBR (OTD-VM-019, FM-VM-17). Classe 2 mco; duty-of-care gate (FR-VM-014) obrigatório | Medium (Could) | PR-VM-020 | Container service | AT-VM-012 |
> 84	| FR-VM-013 | `vision.describe_screen` | Descrição de screenshot/UI (padrão JAWS PictureSmart / NVDA AI Content Describer) com sinalização de incerteza; dual-backend BYOK provider-agnóstico (precedente validado por terceiros). Classe 2 mco; duty-of-care gate obrigatório | Medium (Could) | PR-VM-021 | Container service | AT-VM-013 |
> 85	| FR-VM-014 | Duty-of-care layer assistivo | Camada transversal a `vision.alt_text`/`describe_screen`/`describe_image`/`ocr`/`analyze_video` em uso assistivo (FM-VM-14): (a) **recusas categóricas duras** — medicação/dosagem, alérgeno, mobilidade, emergência (template ToS Be My Eyes), 100% de recusa red-line (KPI-VM-005); (b) **confidence flag/linguagem hedge** em baixa certeza (anti-overtrust ASSETS 2024); (c) **gancho de escalonamento a verificação humana** (híbrido Aira). Toda recusa registrada em `infra_health_logs service='vision-mcp'`; recusa não cobra mcoCoins | Critical (quando assistivas existirem) | PR-VM-020, PR-VM-021, PR-VM-022 | Container service | AT-VM-014 |
> 86	| FR-VM-026 | Batch assistivo + fila de revisão humana | Processamento em lote de catálogo via `vision.alt_text` (2 mco/imagem) com fila de revisão humana: saídas de baixa confiança NÃO entram no relatório de conformidade sem aprovação; relatório auditável sela apenas itens revisados. Monetização B2B/compliance — usuário BLV final nunca paga premium (BR-VM-010) | Medium (Could) | PR-VM-022 | Container service + UI + Hook | AT-VM-026 |
> 87	
> 88	### 2.8 Cognitive Enhancement (Could)
> 89	
> 90	| ID | Title | Description | Priority | PR Traced | Category | Test ID |
> 91	|----|-------|-------------|----------|-----------|----------|---------|
> 92	| FR-VM-025 | Resources + Prompts (progressive enhancement) | Resources `mesh://nodes/{node_id}`, `mesh://references?pillar={cv\|motion\|neuromorphic\|foveated}`, `vision://artifacts/{content_ref}` (Storage privado, signed URL curto) e prompts `/vision-essence`/`/reference-brief`/`/competitive-vision` para hosts completos. Toda capability alcançável por ecossistemas externos mantém **porta tool** (Claude API connector consome só tools). Âncoras CoALA/V*/GraphRAG; proibido rótulo "cognitive computing" | Low (Could) | PR-VM-025 | Container service | AT-VM-025 |
> 93	
> 94	---
> 95	
> 96	## 3. Non-Functional Requirements
> 97	
> 98	> Targets de latência/custo são **calibração inicial** — medição material antes do fix (OTD-VM-004); números CPU coletados são x86, benchmarks ARM64 pendentes (OTD-VM-010).
> 99	
> 100	| ID | Category | Requirement | Target | Measurement |
> 101	|----|----------|-------------|--------|-------------|
> 102	| NFR-VM-001 | Performance (Tier 1) | `motion.peripheral_scan` latência por imagem/frame-batch em CPU ARM64 (sem GPU) | p95 ≤ 2s (provisório — OTD-VM-010) | Telemetria do container + bench aarch64 |
> 103	| NFR-VM-002 | Performance (Tier 2) | Overhead do serviço por tool call (identidade + sentinel + billing + mesh), excluída a leg de provider | p95 < 800ms | Logs do container / `agent_executions` |
> 104	| NFR-VM-003 | Performance (async) | `deepsearch.run` submit→`job_id`; SSE heartbeat anti-idle Cloudflare (~100s — OTD-VM-013); resultado poll-able pós-terminal | submit p95 < 2s; heartbeat ≤ 25s; retenção ≥ 24h | Teste de job >150s + curl do poll |
> 105	| NFR-VM-004 | Scalability | Single-replica por design (sentinel L3 token bucket per-process — OTD-VM-014); scaling horizontal BLOQUEADO até rate limiter compartilhado | 1 réplica; ≥50 tool calls concorrentes sem degradação | Load test no container |
> 106	| NFR-VM-005 | Availability | Uptime SLO do serviço (healthcheck + watchdog cron */5) | 99.5%/mês | `infra_health_logs` / Neural HUD |
> 107	| NFR-VM-006 | Maintainability | Complexidade ciclomática por hook ≤10; TS strict; contratos de tool versionados com o Plugin Zip | 100% | ESLint + revisão |
> 108	| NFR-VM-007 | Security (identity) | 100% das requests com identidade verificada (ES256 JWKS ou PAT hash) ANTES de qualquer efeito; Origin 403; fail-closed se JWKS inalcançável; `SB_SECRET_KEY` jamais em path client-reachable; migrations (`mcp_access_tokens`, `firecrawl_api_key`, `erase_vision_artifacts`) passam `/security-review` | 100% / SAFE | `/security-review` + smoke 401/403 |
> 109	| NFR-VM-008 | Security (billing) | 0 dedução client-side; 100% dos paths billable com refund-on-failure; integridade de refund (KPI-VM-007); sentinel-block e duty-of-care refusal nunca cobram | 100% | Material proof: delta `mco_balance` por `SELECT` |
> 110	| NFR-VM-009 | Privacy (LGPD) | Erasure cascateia com zero resíduo em ≤24h da chamada; 100% dos nós de visão com metadata proveniência/licença/`retention_until`; PII-strip antes de insert; zero nó scraped em system nodes; zero tool de recognition publicada | 100% / zero resíduo | `SELECT` count antes/depois + query de system nodes |
> 111	| NFR-VM-010 | Observability | Cada path (success/degraded/error/block/refusal) emite `infra_health_logs` (`service='vision-mcp'` ou `'sentinel'`); container no watchdog | 100% dos paths | Telemetry audit |
> 112	| NFR-VM-011 | Cost discipline | Margem por tool ≥4× floor sobre custo medido (`mco=ceil(usd/$0.018×4)`); classes só fixadas após medição material; espelhamento triplo (COIN_COSTS + constante do serviço + teste) | 100% das tools lançadas (KPI-VM-004) | SOP `mcoin-cost-calibration.md` + `billing.test.ts` |
> 113	| NFR-VM-012 | Accessibility | Superfícies humanas do módulo (Settings BYOK, Connectors, usage view, docs) WCAG 2.2 AA exemplar (PRD §6.4 — o módulo VENDE acessibilidade) | AA completo | axe/Lighthouse + NVDA/JAWS + E2E 1920×1080 |
> 114	| NFR-VM-013 | Compatibility | Conformidade MCP spec 2025-11-25 ("Current"); version-pinning + deprecation-watch (RC 2026-07-28; registry preview) | 100% por release | Checklist de release no SDD |
> 115	
> 116	---
> 117	
> 118	## 4. Interface Requirements
> 119	
> 120	### 4.1 Surface → Hook → Service Contract
> 121	
> 122	```
> 123	[UI: SettingsByokCard / ConnectorsCard / VisionUsageView]
> 124	  ↓ calls (hook-first)
> 125	[Hooks: useUserApiKeys(+firecrawl) / useMcpTokens / useVisionUsage]
> 126	  ↓ reads/writes (RLS-gated)
> 127	[Supabase: user_api_keys (VIEW) / mcp_access_tokens / agent_executions]
> 128	
> 129	[MCP clients (Pantheon · Claude Desktop/Code · VS Code · ChatGPT · Claude API)]
> 130	  ↓ Streamable HTTP + OAuth 2.1/PAT (mcp.mcorch.com → nginx → 127.0.0.1)
> 131	[Container: mcorch_vision_mcp — identity → sentinel → debit → tool → mesh]
> 132	  ↓ PostgREST/RPC (SB_SECRET_KEY, server-side only)
> 133	[Supabase: deduct_mco_coins / refundMco / match_mcorch_nodes / mcorch_nodes+edges /
> 134	 erase_vision_artifacts / infra_health_logs]  + [Edge reuse: embed-mcorch-node]
> 135	```
> 136	
> 137	### 4.2 Transport & Auth Contract (FR-VM-001/002)
> 138	
> 139	#### `POST https://mcp.mcorch.com/` (MCP Streamable HTTP)
> 140	
> 141	**Headers obrigatórios:** `Authorization: Bearer <jwt|pat>` · `Origin` (validado) · `MCP-Protocol-Version` = **qualquer rev suportada pelo SDK MCP** (`SUPPORTED_PROTOCOL_VERSIONS`; `2025-11-25` é a LATEST anunciada, mas `2025-06-18`/`2025-03-26`/… também são aceitas — ausência tolerada, pois é negociada no `initialize`). Pinning a uma única rev 400-aria clientes 3rd-party legítimos que negociam uma rev mais antiga (interop FR-VM-001).  
> 142	**Unauthenticated `initialize`:**
> 143	```
> 144	HTTP/1.1 401 Unauthorized
> 145	WWW-Authenticate: Bearer resource_metadata="https://mcp.mcorch.com/.well-known/oauth-protected-resource"
> 146	```
> 147	**Discovery:** `GET /.well-known/oauth-protected-resource` → RFC 9728 PRM (aponta o AS; decisão Supabase-Auth-fronteado vs vendor = SDD). `GET /health` → 200 (loopback/watchdog).
> 148	
> 149	### 4.3 MCP Tool Contracts (representativos — shape completo por tool no SDD)
> 150	
> 151	#### `vision.describe_image` (FR-VM-018 · 2 mco)
> 152	**Input:**
> 153	```typescript
> 154	{
> 155	  image_url: string,        // https only; host allowlist; ≤20MB
> 156	  question?: string,        // QA opcional (sentinel-inspected)
> 157	  assistive?: boolean,      // ativa duty-of-care gate (FR-VM-014)
> 158	}
> 159	```
> 160	**Output (structuredContent):**
> 161	```typescript
> 162	{
> 163	  description: string,
> 164	  confidence: 'high' | 'medium' | 'low',   // hedge obrigatório se 'low'
> 165	  cost_mco: number,
> 166	  node_id?: string,         // uuid se consolidado na malha
> 167	}
> 168	```
> 169	
> 170	#### `deepsearch.run` / `deepsearch.poll` (FR-VM-007 · 3 / 0 mco)
> 171	**Input run:** `{ query: string, planned_units?: number, source_allowlist?: string[] }`  
> 172	**Output run:** `{ job_id: string, state: 'queued', planned_units: number, charged_mco: number }`  
> 173	**Output poll:** `{ job_id, state: 'queued'|'running'|'done'|'partial'|'failed', delivered_units, planned_units, partial: boolean, failed_units?: string[], refunded_mco?: number, result?: {...} }`
> 174	
> 175	#### `mesh.consolidate_reference` (FR-VM-021 · 1 mco)
> 176	**Input:** `{ content: {...}, regime: 'observation_decay' | 'fact_supersede', provenance: { source_url: string, license: string, origin: 'tenant'|'scraped' }, retention_until: string /* ISO */ }`  
> 177	**Output:** `{ node_id: string /* uuid por SELECT */, embedded: boolean, cost_mco: number }`
> 178	
> 179	#### `vision.alt_text` (FR-VM-012 · 2 mco — assistiva)
> 180	**Output:** `{ alt_short: string, alt_long: string, decorative: boolean, confidence: 'high'|'medium'|'low', human_review_required: boolean, escalation_hint?: string }` — recusa red-line retorna erro 403 estruturado `assistive_redline_refusal` (sem descrição gerada, sem cobrança).
> 181	
> 182	### 4.4 Error Model (uniforme — HTTP no transporte, espelhado em `structuredContent` no tool result)
> 183	
> 184	| Code | Identifier | Condition |
> 185	|------|-----------|-----------|
> 186	| 400 | `protocol_version_mismatch` | `MCP-Protocol-Version` **presente e fora do conjunto suportado pelo SDK** (ausente é tolerado — negociado no `initialize`). Body lista `supported`. |
> 187	| 401 | `identity_unverified` | Token ausente/inválido/expirado/revogado; JWKS inalcançável (fail-closed) |
> 188	| 402 | `insufficient_balance` | Saldo mcoCoins < classe da tool (antes de qualquer leg; nada debitado) |
> 189	| 402 | `<service>_not_configured` | Credencial per-user ausente (ex.: `firecrawl_not_configured`) + `action` apontando `/dashboard/settings` |
> 190	| 403 | `origin_invalid` | Header Origin fora da allowlist (anti DNS-rebinding) |
> 191	| 403 | `sentinel_blocked` | `inspectPrompt` L1/L2/L3 bloqueou args ou texto extraído (não cobra; logado) |
> 192	| 403 | `scope_insufficient` | PAT sem scope para a tool (scopes nunca incluem credencial/billing) |
> 193	| 403 | `assistive_redline_refusal` | Duty-of-care: medicação/alérgeno/mobilidade/emergência (não cobra; logado) |
> 194	| 404 | `job_not_found` | `job_id` inexistente ou de outro tenant |
> 195	| 422 | `validation_failed` | Campo + mensagem PT-BR no body (§5) |
> 196	| 429 | `rate_limited` | Sentinel L3 token bucket (single-replica — OTD-VM-014) |
> 197	| 500 | `internal_error` | Erro interno (logado em `infra_health_logs`; refund se já debitado) |
> 198	
> 199	### 4.5 Async Job & Partial-Delivery Refund Contract (sela FM-VM-07 / BR-VM-003 / BAC-VM-007)
> 200	
> 201	> Regra definida AQUI, antes de qualquer código — exigência do BRD ("regra selada no FRD antes da Fatia 3").
> 202	
> 203	1. **Débito integral na entrada:** `deepsearch.run` debita a classe inteira (3 mco) via `deduct_mco_coins` antes do enqueue. Saldo insuficiente → 402, job não nasce.
> 204	2. **Unidades entregáveis:** todo job declara `planned_units` (páginas/queries) no aceite; o estado terminal reporta `delivered_units`.
> 205	3. **Falha total (`delivered_units = 0`):** estado `failed`; `refundMco` credita o valor integral; delta líquido de `mco_balance` = 0 (prova por `SELECT` before/after).
> 206	4. **Entrega parcial (`0 < delivered < planned`):** estado `partial`; cobrança retida = `max(1, floor(class_mco × delivered_units / planned_units))`; refund = `class_mco − retida`, executado via `refundMco` ANTES de o job ir a terminal. Arredondamento sempre A FAVOR do tenant (floor na cobrança).
> 207	5. **Transparência:** resultado parcial entregue com `partial: true` + `failed_units[]` + `refunded_mco` explícito no payload do poll.
> 208	6. **Idempotência:** refund por job é executado no máximo uma vez (guard por `job_id` no contexto do RPC); retries de poll nunca re-disparam refund.
> 209	
> 210	### 4.6 Internal RPC/REST Contracts (reuso — nenhum novo encanamento client-side)
> 211	
> 212	| Contract | Direction | Notes |
> 213	|----------|-----------|-------|
> 214	| `deduct_mco_coins(p_user_id, p_amount, p_action, p_context)` | container → PostgREST (service key name `SB_SECRET_KEY`) | Atômico; só após identidade verificada; HTTP 402 propagado |
> 215	| `refundMco` (padrão `_shared/billing.ts`) | container → PostgREST | Credit service-role-only; nunca lança; fire-and-forget com log |
> 216	| `match_mcorch_nodes(query_embedding, …)` | container → RPC | `mesh.search`; RLS-scoped ao tenant |
> 217	| `embed-mcorch-node` | insert em `mcorch_nodes` → Edge Fn existente | Embed-on-insert grátis (OpenRouter → fallback Gemini, 768 dims) |
> 218	| `erase_vision_artifacts(content_ref)` | RPC SECURITY DEFINER | Cascade nó+edges+embedding+Storage; espelha `erase_lead()` |
> 219	| `infra_health_logs` insert | container → PostgREST | `service='vision-mcp'`/`'sentinel'`; todo path de falha/block/refusal |
> 220	
> 221	---
> 222	
> 223	## 5. Data Requirements
> 224	
> 225	| Field | Type | Nullable | Validation Rule | Error Message (PT-BR) |
> 226	|-------|------|----------|-----------------|----------------------|
> 227	| `mcp_access_tokens.token_hash` | `char(64)` | NOT NULL | SHA-256 hex; nunca plaintext; UNIQUE | "Token inválido ou expirado" |
> 228	| `mcp_access_tokens.scopes` | `text[]` | NOT NULL | ⊆ vocabulário de tools; NUNCA `credentials:*`/`billing:*` | "Escopo inválido para token de acesso" |
> 229	| `mcp_access_tokens.expires_at` | `timestamptz` | NOT NULL | > `now()` na criação (validade máxima selada no SDD) | "Data de expiração deve ser futura" |
> 230	| `user_api_keys.firecrawl_api_key` | `text` (Vault via VIEW) | NULL | Não-vazia quando fornecida; write `.insert` (nunca `.upsert`); teste server-side | "Chave Firecrawl inválida — verifique e tente novamente" |
> 231	| `image_url` (tool input) | `string` | NOT NULL (tools de imagem) | `https://` only; host allowlist; content-type imagem; ≤ 20MB | "URL de imagem inválida ou não permitida" |
> 232	| `video` (tool input) | `string`/ref | NOT NULL (`analyze_video`) | Duração ≤ cap (60 min default res — Gemini); cap cobrado por minuto | "Vídeo excede a duração máxima suportada" |
> 233	| `planned_units` (`deepsearch.run`) | `int` | NOT NULL (default 1) | 1 ≤ N ≤ cap do plano (valor selado no SDD) | "Número de unidades do job fora do limite" |
> 234	| `job_id` | `uuid` | NOT NULL (`poll`) | UUID v4 existente e pertencente ao tenant | "Job não encontrado" |
> 235	| `regime` (consolidate) | `enum` | NOT NULL | ∈ {observation_decay, fact_supersede} (FR-VM-015) | "Regime de persistência obrigatório" |
> 236	| `provenance.source_url` | `text` | NOT NULL (nós scraped) | URL válida; obrigatória com `origin='scraped'` | "Proveniência obrigatória para conteúdo coletado" |
> 237	| `provenance.license` | `text` | NOT NULL (nós scraped) | Não-vazia; allowlist de fontes permissivas aplicada no scrape | "Licença da fonte é obrigatória" |
> 238	| `retention_until` | `timestamptz` | NOT NULL (nós de visão) | > `now()`; ≤ teto de retenção (art. 16; teto no SDD) | "Prazo de retenção inválido" |
> 239	| `mcorch_nodes.user_id` (nós de visão/scrape) | `uuid` | NOT NULL | NUNCA NULL para conteúdo scraped (system nodes proibidos) | — (guard server-side; violação = bug crítico) |
> 240	| `content_ref` (`erase_vision_artifacts`) | `text` | NOT NULL | Existe e pertence ao tenant chamador | "Artefato não encontrado" |
> 241	
> 242	---
> 243	
> 244	## 6. Test Strategy Matrix
> 245	
> 246	> **Padrão house de smoke zero-cost:** todos os guards são prováveis SEM gasto de provider — 401 (sem token), 403 origin/sentinel/red-line, 402 saldo (user descartável zerado), 402 `firecrawl_not_configured`, 422 validação — à la `scripts/qa/smoke-campaign-run.ts` (throwaway users + cleanup). Runs pagos E2E ficam gated em GO Sovereign. JWT de user para QA: `scripts/qa/gen-user-jwt.ts`.
> 247	
> 248	| FR ID | Unit Test | Integration Test | E2E Test | Notes |
> 249	|-------|-----------|-----------------|----------|-------|
> 250	| FR-VM-001 | ✅ Required | ✅ Required | ✅ Required | Origin 403 + protocol-version + SSE heartbeat (zero-cost) |
> 251	| FR-VM-002 | ✅ Required | ✅ Required | ✅ Required | 401 + `WWW-Authenticate` literal; fail-closed com JWKS off; `test-es256-jwt-verification.ts` G1/G2 |
> 252	| FR-VM-003 | ✅ Required | ✅ Required | — | Hash-only no DB; revogação → 401; scope negativo → 403; RLS isolation |
> 253	| FR-VM-004 | ✅ Required | ✅ Required | ✅ Required | `402 firecrawl_not_configured` body literal; zero env-key em path user-facing (grep material) |
> 254	| FR-VM-005 | ✅ Required | ✅ Required | — | Bloqueio não cobra (delta saldo = 0); L2 sobre texto extraído bloqueia insert |
> 255	| FR-VM-006 | ✅ Required | ✅ Required | ✅ Required | Débito atômico + 402 + BYOK custo 0 + espelhamento triplo (`billing.test.ts`) |
> 256	| FR-VM-007 | ✅ Required | ✅ Required | ✅ Required | Job >150s via poll; refund parcial bate §4.5 (floor a favor do tenant); idempotência |
> 257	| FR-VM-008 | ✅ Required | ✅ Required | — | UUID por `SELECT`; `infra_health_logs` em falha forçada; BR/FR ID no metadata |
> 258	| FR-VM-009 | ✅ Required | ✅ Required | ✅ Required | Erasure zero-residue count antes/depois (crítico LGPD); retention sweep |
> 259	| FR-VM-010 | ✅ Required | ✅ Required | — | Benchmark de recall (gate de GA); bypass Tier 2 sempre disponível |
> 260	| FR-VM-011 | ✅ Required | — | ✅ Required | Plugin Zip baixável; conexão OAuth real de client externo (log/screenshot) |
> 261	| FR-VM-012 | ✅ Required | ✅ Required | — | "Propósito equivalente" + decorative detection + confidence flag |
> 262	| FR-VM-013 | ✅ Required | ✅ Required | — | Screenshot/UI description + incerteza sinalizada |
> 263	| FR-VM-014 | ✅ Required | ✅ Required | ✅ Required | Suite adversarial red-line 100% recusa (KPI-VM-005) — zero-cost por design (recusa não chama provider) |
> 264	| FR-VM-015 | ✅ Required | ✅ Required | — | Regimes distinguíveis no schema; fato suplanta, observação decai |
> 265	| FR-VM-016 | ✅ Required | ✅ Required | — | `docker ps`/`inspect` healthy; hardening anchor; watchdog → HUD |
> 266	| FR-VM-017 | ✅ Required | ✅ Required | ✅ Required | 1ª tool da Fatia 1 — prova auth/transport; RLS scoping |
> 267	| FR-VM-018 | ✅ Required | ✅ Required | ✅ Required | Run pago E2E (gated GO) + allowlist de host (zero-cost) |
> 268	| FR-VM-019 | ✅ Required | ✅ Required | — | Billing por página; provenance tag; sentinel L2 no texto |
> 269	| FR-VM-020 | ✅ Required | ✅ Required | — | robots.txt + login-wall block + allowlist (zero-cost guards) |
> 270	| FR-VM-021 | ✅ Required | ✅ Required | ✅ Required | Nó + embed + edge KPI-VM-003; zero scraped em system nodes (query material) |
> 271	| FR-VM-022 | ✅ Required | ✅ Required | — | `.insert` na VIEW mascarada; teste server-side; estados do card |
> 272	| FR-VM-023 | ✅ Required | — | — | Agregação ledger por tool/tenant |
> 273	| FR-VM-024 | ✅ Required | ✅ Required | — | Classes por tool; caps de duração; keep-warm documentado |
> 274	| FR-VM-025 | ✅ Required | — | — | Resources RLS-scoped; signed URLs curtos; porta tool preservada |
> 275	| FR-VM-026 | ✅ Required | ✅ Required | — | Low-confidence nunca sela relatório sem revisão humana |
> 276	
> 277	**Test files location:**
> 278	- Unit (serviço): pacote do container `mcorch_vision_mcp` (path final selado no SDD — precedente `packages/gitnexus-core`)
> 279	- Unit (hooks): `src/hooks/__tests__/useMcpTokens.test.ts`, `useVisionUsage.test.ts`, extensão de `useUserApiKeys`
> 280	- Billing assertions: `src/test/billing.test.ts` (espelhamento triplo das classes)
> 281	- Smokes zero-cost: `scripts/qa/smoke-vision-mcp.ts` (throwaway users + cleanup; guards 401/402/403/422/red-line)
> 282	- E2E: `e2e/vision-mcp.spec.ts` + conexão OAuth real (Fatia 3) + E2E UI audit 1920×1080 quando houver UI nova (gate Lei 1)
> 283	
> 284	---
> 285	
> 286	## 7. Traceability Matrix
> 287	
> 288	> Sela a coluna FR sobre o PRD §8 (MR → BR → PR → FR → NFR completo).
> 289	
> 290	| PR ID | FR ID | NFR ID |
> 291	|-------|-------|--------|
> 292	| PR-VM-001 | FR-VM-001, FR-VM-016 | NFR-VM-004, NFR-VM-005, NFR-VM-010 |
> 293	| PR-VM-002 | FR-VM-002 | NFR-VM-007 |
> 294	| PR-VM-003 | FR-VM-017 | NFR-VM-002 |
> 295	| PR-VM-004 | FR-VM-018 | NFR-VM-002, NFR-VM-011 |
> 296	| PR-VM-005 | FR-VM-019 | NFR-VM-002, NFR-VM-011 |
> 297	| PR-VM-006 | FR-VM-020 | NFR-VM-002, NFR-VM-009 |
> 298	| PR-VM-007 | FR-VM-004, FR-VM-022 | NFR-VM-006, NFR-VM-007 |
> 299	| PR-VM-008 | FR-VM-006 | NFR-VM-008, NFR-VM-011 |
> 300	| PR-VM-009 | FR-VM-005 | NFR-VM-007, NFR-VM-010 |
> 301	| PR-VM-010 | FR-VM-008, FR-VM-015, FR-VM-021 | NFR-VM-009, NFR-VM-010 |
> 302	| PR-VM-011 | FR-VM-001, FR-VM-002 | NFR-VM-003, NFR-VM-007, NFR-VM-013 |
> 303	| PR-VM-012 | FR-VM-003 | NFR-VM-007 |
> 304	| PR-VM-013 | FR-VM-007 | NFR-VM-003, NFR-VM-008 |
> 305	| PR-VM-014 | FR-VM-011 | NFR-VM-012, NFR-VM-013 |
> 306	| PR-VM-015 | FR-VM-011 | NFR-VM-013 |
> 307	| PR-VM-016 | FR-VM-009 | NFR-VM-009 |
> 308	| PR-VM-017 | FR-VM-023 | NFR-VM-006, NFR-VM-011 |
> 309	| PR-VM-020 | FR-VM-012, FR-VM-014 | NFR-VM-012 |
> 310	| PR-VM-021 | FR-VM-013, FR-VM-014 | NFR-VM-012 |
> 311	| PR-VM-022 | FR-VM-026, FR-VM-014 | NFR-VM-009, NFR-VM-012 |
> 312	| PR-VM-023 | FR-VM-010 | NFR-VM-001, NFR-VM-011 |
> 313	| PR-VM-024 | FR-VM-024 | NFR-VM-002, NFR-VM-011 |
> 314	| PR-VM-025 | FR-VM-025 | NFR-VM-013 |
> 315	
> 316	---
> 317	
> 318	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 319	
> ```

## 🤖 Claude *(18:49:52)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/vision-mcp/01-mrd.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# MRD — Market Requirements Document
> 2	
> 3	**Project:** vision-mcp  
> 4	**Version:** v0.1 | **Date:** 2026-06-11  
> 5	**BoK Applied:** BABOK v3 (Strategy Analysis + Elicitation & Collaboration)  
> 6	**Status:** Complete  
> 7	**Source of Truth:** `docs/bok/vision-mcp/00-deepsearch-blueprint.md` (v0.2.0, 2026-06-11) — todo requisito deste MRD deriva do blueprint; ambiguidades viram OTD, nunca improvisação.  
> 8	**Market segment:** B2B2C · **Monetization:** híbrida (mcoCoins por tool call + planos Starter/Pro/Enterprise) · **Regulatory:** LGPD ELEVADO (biométrico art. 11) · **Integration surface:** extends-mcorch
> 9	
> 10	---
> 11	
> 12	## 1. Executive Summary
> 13	
> 14	O **Vision MCP** é um servidor Model Context Protocol nativo do MCORCH que expõe **percepção visual + deepsearch fundamentado** — imagem, vídeo, captura de tela e páginas web convertidos em descrições/detecções/OCR estruturados e em **referências de mercado consolidadas** gravadas na Knowledge Mesh — para agentes internos (Pantheon) **e** ecossistemas externos (Claude Desktop/Code, VS Code, ChatGPT, Claude API) via Streamable HTTP + OAuth 2.1 em `mcp.mcorch.com` (container Sovereign Mesh). A arquitetura de produto segue a metáfora biológica **"Essência Humana"**: uma periferia barata always-on com princípios neuromórficos emulados em software (Tier 1, CPU quase-grátis) dispara a análise foveal profunda e billable (Tier 2) apenas quando há sinal de saliência — o que mantém o custo por chamada baixo por design.
> 15	
> 16	**A tese de mercado deste MRD é deliberadamente bifurcada (OTD-VM-002 emendada):**
> 17	
> 18	> **(a) Beachhead demand-PROVADO — descrição visual assistiva / alt-text de conformidade.** A demanda é validada em **três eixos independentes e multi-fonteados**: (1) **uso real** — Be My Eyes com 1M de usuários cegos/baixa-visão e 43M requests de IA+vídeo/ano; (2) **convergência de capability** — JAWS PictureSmart e NVDA AI Content Describer já chamam OpenAI/Anthropic para exatamente a tool `describe_screen`; (3) **compulsão regulatória** — WCAG 2.2 SC 1.1.1, EAA exigível desde 28/06/2025, LBI Art. 63 e ABNT NBR 17225:2025, com ~99% dos sites brasileiros não-conformes.
> 19	>
> 20	> **(b) Aposta de diferenciação NÃO-validada — o produto cruzado vision×deepsearch.** A varredura do registry oficial MCP (2026-06-11) provou que nenhum servidor combina computer vision com deep-research (whitespace genuíno), **mas ausência de competidor é também ausência de validação de demanda**. O cruzado é tratado como **upsell a provar**, com gate de validação explícito — nunca como mercado estabelecido.
> 21	
> 22	O GTM ancora no vertical assistivo (entrada de menor risco, regulatoriamente compelida) e monta o cruzado por cima da infraestrutura que o MCORCH já tem provada em produção: billing mcoCoins atômico, credenciais per-tenant, sentinel, malha GraphRAG e o precedente de container MCP (`mcorch_gitnexus`).
> 23	
> 24	---
> 25	
> 26	## 2. Market Problem Statement
> 27	
> 28	### 2.1 Current State
> 29	
> 30	**No mercado assistivo/compliance:** empresas brasileiras e europeias estão sob obrigação legal de acessibilidade digital (LBI Art. 63 — todas as empresas com sede ou representação comercial no Brasil; EAA — exigível desde 06/2025 inclusive para empresas não-UE que vendem ao consumidor europeu), mas **menos de 1–3% dos sites brasileiros são acessíveis** (0,74% plenamente — BigDataCorp/Movimento Web para Todos), e a novíssima ABNT NBR 17225:2025 acaba de dar ao Art. 63 uma régua técnica objetiva (~150 requisitos mapeados a WCAG 2.2). Gerar alt-text conformante em escala é hoje trabalho manual caro ou saída de IA sem dever de cuidado. Do lado do usuário final BLV, as soluções dominantes são apps fechados (Be My AI, Seeing AI, Lookout) ou serviço humano caro (Aira, US$26–1.160/mês) — nenhuma é uma capability componível que desenvolvedores e agentes possam invocar via protocolo aberto.
> 31	
> 32	**No mercado de agentes/MCP:** as duas metades isoladas já têm donos. Vision sobre MCP está tomado pela Roboflow (`com.roboflow/roboflow-mcp`, ~70 tools, hosted-only); deepsearch sobre MCP está tomado por Firecrawl/Tavily/Exa (376.976 / 165.112 / 67.928 downloads npm/mês respectivamente). Porém nenhum oferece: saída de visão **fundamentada por evidência de deepsearch** numa única superfície; **self-host soberano**; **credencial per-tenant com billing atômico**; ou **dever de cuidado assistivo** embarcado.
> 33	
> 34	**No MCORCH (estado interno):** o Pantheon raciocina sobre texto e AST, mas **não enxerga** — não há capability de percepção visual fatorada, e as "referências consolidadas" de mercado que alimentariam a malha dependem de scripts ad-hoc com chave Firecrawl global (anti-pattern de tenancy — FM-VM-05).
> 35	
> 36	### 2.2 Root Cause Analysis
> 37	
> 38	| Gap | Tipo | Por que persiste |
> 39	|-----|------|------------------|
> 40	| Alt-text/descrição conformante não escala | Technology + process gap | IA genérica não embarca dever de cuidado (recusas, confiança, escalonamento humano); revisão humana pura não escala; norma técnica objetiva (NBR 17225) só existe desde 03/2025 |
> 41	| ~99% de não-conformidade BR apesar da lei | Enforcement gap | LBI Art. 63 vigente desde 2015 sem régua técnica; aplicação imatura — mas MPF já recomendou regulamentação e o EAA criou precedente de notificação em dias |
> 42	| Percepção visual não-componível para agentes | Market gap | Incumbentes assistivos são apps B2C fechados; Roboflow MCP é hosted-only/closed (repo 404); ninguém expõe percepção como capability MCP soberana |
> 43	| Visão sem fundamentação (alucinação) | Technology gap | VLMs descrevem com confiança sem ground truth; usuários BLV **super-confiam** por não terem como verificar (ASSETS 2024); nenhum competidor cruza visão com evidência de deepsearch |
> 44	| Custo de visão profunda em escala | Economic gap | Análise foveal (VLM/segmentação/vídeo) é cara por chamada; sem um gate periférico barato, o custo por percepção contínua é proibitivo |
> 45	
> 46	### 2.3 Desired State
> 47	
> 48	Um agente (interno ou externo) ou uma aplicação cliente invoca tools de percepção (`vision.alt_text`, `vision.describe_screen`, `vision.describe_image`, `deepsearch.run`…) via endpoint MCP padrão, com identidade verificada (ES256 JWKS / OAuth 2.1), credenciais resolvidas per-tenant (BYOK fail-closed), cobrança atômica em mcoCoins com refund-on-failure, e dever de cuidado embarcado nas tools assistivas. A saída de visão é fundamentada por deepsearch quando o caso de uso exige, e consolidada como nó na Knowledge Mesh do tenant (observation embeddado, com proveniência/licença/retenção) — percepção como **órgão de uma arquitetura cognitiva (CoALA)** que o MCORCH já possui, não mais uma ferramenta de visão solta.
> 49	
> 50	### 2.4 Demand Bifurcation (OTD-VM-002 emendada — framing estrutural deste MRD)
> 51	
> 52	| Fatia | Status de demanda | Evidência | Tratamento neste MRD |
> 53	|-------|-------------------|-----------|----------------------|
> 54	| **Descrição/alt-text assistivo** | **Demand-provado** (3 eixos independentes) | Uso: Be My Eyes 1M usuários BLV + 43M requests/ano; Seeing AI/Lookout grátis em escala; disposição a pagar Aira US$26–1.160/mês; hardware US$399–4.250. Capability: JAWS/NVDA já chamam OpenAI/Anthropic. Regulação: WCAG 2.2 + EAA + LBI Art. 63 + NBR 17225 com ~99% não-conformidade BR | **Beachhead** — requisitos Critical, GTM primário |
> 55	| **Vision×deepsearch cruzado** | **Hipótese não-validada** (whitespace sem demanda comprovada) | Zero competidores no registry MCP combinam as metades; zero evidência de demanda específica para a combinação | **Upsell bet** — requisito High com **gate de validação explícito** (KPI-VM-003); nunca apresentado como mercado provado |
> 56	
> 57	---
> 58	
> 59	## 3. Target Market Segments
> 60	
> 61	> Modelo **B2B2C**: o pagador primário é a empresa/desenvolvedor sob compulsão de conformidade ou construindo agentes; o beneficiário final é o usuário BLV (padrão Be My Eyes: grátis ao usuário final, financiado por B2B).
> 62	
> 63	| Segment | Description | Size Estimate | Urgency | Accessibility |
> 64	|---------|-------------|---------------|---------|---------------|
> 65	| Primary | Empresas BR/UE sob compulsão de acessibilidade (e-commerce, bancos, SaaS, gov) + vendors de tecnologia assistiva/screen-readers que precisam de descrição visual compliance-grade via API/MCP | ~99% dos sites BR não-conformes = greenfield de milhões de CNPJs com presença web (⚠️ estimativa de ordem de grandeza) | High — EAA exigível, NBR 17225 publicada, MPF pressionando Art. 63 | Média — exige distribuição self-serve (Plugin/registry) + prova de conformidade |
> 66	| Secondary | Desenvolvedores e operadores de agentes nos ecossistemas MCP (Claude Desktop/Code, VS Code, ChatGPT, Claude API) que precisam de percepção visual + grounding como capability componível | Proxy de demanda: 376.976 + 165.112 + 67.928 downloads npm/mês dos MCPs de deepsearch (⚠️ proxy, não contagem de pagantes) | Medium | Alta — endpoint remoto padrão 2025-11-25 + registry `com.mcorch/*` |
> 67	| Internal/Tertiary | Pantheon (engineer/scientist/artisan/marketing-growth) e tenants MCORCH existentes consumindo referências consolidadas na malha | Base de tenants MCORCH atual (Usuário Zero → multi-tenant) | High — dogfooding é o validador do cruzado | Imediata — extends-mcorch |
> 68	
> 69	### 3.1 TAM / SAM / SOM
> 70	
> 71	> ⚠️ **Honestidade de sizing:** o blueprint só tem números fonteados para o vertical assistivo (uso/população/preço), **não** para o tamanho em $ de nenhum dos dois mercados. Tudo que está marcado ⚠️ é estimativa de ordem de grandeza a refinar antes de decisão de investimento — registrado como **OTD-VM-021** (novo neste MRD): *dimensionamento bottom-up em $ do mercado de acessibilidade digital BR/UE e do mercado de tooling MCP de percepção; refinar com fontes primárias antes do BRD fixar metas de receita.*
> 72	
> 73	| Metric | Value | Basis |
> 74	|--------|-------|-------|
> 75	| TAM (Total Addressable Market) | **2,2 bilhões** de pessoas com deficiência visual (top-down, população — não receita); perda de produtividade global ≈ **US$411 bi/ano** (proxy macro, NÃO mercado endereçável) | WHO fact sheet 02/2026 (fonteado no blueprint §4-A). ⚠️ Valor em $ do mercado de acessibilidade digital: não fonteado — OTD-VM-021 |
> 76	| SAM (Serviceable Addressable Market) | Empresas BR sob LBI Art. 63 com web não-conforme (~99% do universo BR) + empresas vendendo à UE sob EAA + desenvolvedores de agentes MCP | BigDataCorp/Movimento Web para Todos (<1–3% acessíveis; 0,74% plenamente); npm stats como proxy do lado MCP. ⚠️ Sem $ fonteado — OTD-VM-021 |
> 77	| SOM (Serviceable Obtainable Market, 24m) | Tenants MCORCH + early adopters externos via registry MCP; receita ancorada ao Million-BRL Roadmap | ⚠️ Estimativa interna; primeiro marco material = primeira receita mcoCoins de tool call externo |
> 78	
> 79	---
> 80	
> 81	## 4. Competitive Landscape
> 82	
> 83	> Todos os competidores abaixo foram **verificados na pesquisa do blueprint com URL-fonte**. Posicionamento honesto: **não reivindicamos "vision sobre MCP" nem "deepsearch sobre MCP" como diferencial — ambos já estão tomados.** O diferencial se sustenta em 4 eixos próprios: (i) produto cruzado (hipótese), (ii) self-host soberano, (iii) credencial per-tenant + mcoCoins atômico, (iv) Essência Humana / percepção como órgão de arquitetura cognitiva CoALA já montada.
> 84	
> 85	### 4.1 Superfície MCP (perception & deepsearch)
> 86	
> 87	| Competitor | Positioning | Strengths | Weaknesses | Our Differentiation |
> 88	|------------|-------------|-----------|------------|---------------------|
> 89	| **Roboflow MCP** (`com.roboflow/roboflow-mcp` v1.0.3, [mcp.roboflow.com](https://mcp.roboflow.com/llms.txt)) | Vision-sobre-MCP first-party, "Roboflow Official", hosted em `mcp.roboflow.com/mcp` | ~70 tools de CV; já executa o padrão "remote MCP + Apps + Skills" completo | **Hosted-only** (repo GitHub 404 — provável closed-source); sem self-host; sem grounding deepsearch; sem camada assistiva/dever de cuidado | Self-host soberano no Sovereign Mesh; cruzado vision+grounding; billing per-tenant; duty-of-care |
> 90	| **Firecrawl MCP** ([github.com/firecrawl/firecrawl-mcp-server](https://github.com/firecrawl/firecrawl-mcp-server)) | Deepsearch/scrape sobre MCP, líder de adoção | **376.976 downloads npm/mês**; 6.5k★; MIT; self-hostable | Só deepsearch — zero visão; sem billing per-tenant nativo | **Co-opetição:** Firecrawl é nosso engine de scrape per-user BYOK; nosso valor é o cruzado + malha + billing |
> 91	| **Tavily MCP** ([github.com/tavily-ai/tavily-mcp](https://github.com/tavily-ai/tavily-mcp)) | Search-for-agents sobre MCP | **165.112 downloads npm/mês**; MIT wrapper | Só search; sem visão; sem soberania de dados | Idem — cruzado + consolidação na malha do tenant com proveniência |
> 92	| **Exa MCP** ([github.com/exa-labs/exa-mcp-server](https://github.com/exa-labs/exa-mcp-server)) | Neural search sobre MCP | **67.928 downloads npm/mês**; MIT wrapper | Só search | Idem |
> 93	| **x402** ([docs.cdp.coinbase.com/x402/mcp-server](https://docs.cdp.coinbase.com/x402/mcp-server)) | Spec de micropagamento por tool call MCP | Valida o modelo "pagar por chamada" | Emergente, não é produto de percepção | Observação de modelo de monetização — mcoCoins já implementa credit-metering equivalente |
> 94	
> 95	**Nota sandcastles.ai (validador de padrão, não competidor):** a recon materialmente verificada do sandcastles estabeleceu que o padrão de distribuição **remote MCP + OAuth 2.1 (RFC 9728) + Plugin Zip versionado + skills nomeadas** funciona em produção com onboarding "cole 1 URL → login → conectado". A anedota de receita (~$1.6M / 22.000 creators) vem de fonte secundária única (Medium, não-verificada) e **não é usada como evidência de mercado** — só o padrão técnico é importado (MR-VM-012).
> 96	
> 97	### 4.2 Vertical Tecnologia Assistiva (beachhead)
> 98	
> 99	| Competitor | Positioning | Strengths | Weaknesses | Our Differentiation |
> 100	|------------|-------------|-----------|------------|---------------------|
> 101	| **Be My Eyes / Be My AI** ([bemyeyes.com](https://www.bemyeyes.com/news/be-my-eyes-reaches-1-million-blind-and-low-vision-users-and-10-million-volunteers/)) | App de descrição visual líder, grátis ao usuário, B2B-funded | **1M usuários BLV + 10M voluntários** (CSUN 2026); **43M requests IA+vídeo/ano**; crescimento de receita >300%; 97% satisfação; enterprise (Google, Microsoft, Hilton…) | App fechado B2C — não é capability componível para desenvolvedores/agentes; modelo atual por trás do Be My AI não-divulgado (OTD-VM-015) | Percepção como tool MCP aberta a qualquer host/agente; self-host; malha de conhecimento do tenant |
> 102	| **Microsoft Seeing AI** ([blogs.microsoft.com/accessibility](https://blogs.microsoft.com/accessibility/seeing-ai-app-launches-on-android-including-new-and-updated-features-and-new-languages/)) | App grátis iOS/Android, 36 idiomas, rich descriptions + chat-com-documento | Baseline de feature de big tech, grátis | App fechado; sem API/MCP; sem compliance BR (NBR 17225) | **Define o baseline que nossas tools devem igualar** (MR-VM-015); monetizamos o B2B/compliance, não o usuário final |
> 103	| **Google Lookout** | App grátis Android, Q&A de imagem via Gemini | Grátis, distribução Android | Idem Seeing AI | Idem |
> 104	| **Aira** ([aira.io/subscriptions](https://aira.io/subscriptions/)) | Interpretação visual humana on-demand + Access AI grátis | Prova **disposição a pagar**: US$26–1.160/mês pelo tier humano; padrão híbrido IA-grátis + humano-pago-para-verificar | Custo humano não escala; não é API | Importamos o **padrão híbrido** como gancho de escalonamento humano (MR-VM-002), não competimos no serviço humano |
> 105	| **JAWS PictureSmart AI** ([vispero.com](https://vispero.com/news/freedom-scientific-unveils-revolutionary-picturesmart-ai-for-jaws/)) | Descrição de tela embarcada no screen reader líder | Usa OpenAI **e** Anthropic (valida dual-backend); distribuição JAWS | Preso à licença JAWS; não-componível | Mesma capability como tool MCP provider-agnóstica BYOK |
> 106	| **NVDA AI Content Describer** ([github.com/cartertemm/AI-content-describer](https://github.com/cartertemm/AI-content-describer)) | Add-on OSS provider-agnóstico (GPT/Gemini/Claude/Grok) | OSS; **valida o padrão multi-modelo BYOK** que o MCORCH já tem nativo | Add-on de nicho NVDA; sem billing/governança | Mesmo padrão, com governança, billing, dever de cuidado e malha |
> 107	
> 108	---
> 109	
> 110	## 5. Market Opportunity & Timing
> 111	
> 112	**Por que agora (5 vetores, todos fonteados no blueprint):**
> 113	
> 114	1. **Maturidade do protocolo MCP.** A revisão **2025-11-25** é "Current": dois transportes (stdio + Streamable HTTP; HTTP+SSE deprecado), OAuth 2.1 formalizado com RFC 9728 Protected Resource Metadata para servidores remotos. O Claude API MCP connector (`mcp-client-2025-11-20`) consome servidores remotos com bearer token. A janela de publicar cedo no MCP Registry (preview) sob namespace verificado `com.mcorch/*` está aberta.
> 115	2. **Compulsão regulatória em cascata (a metade legal da demanda assistiva).** EAA exigível desde **28/06/2025** (notificações de advocacy em dias após o prazo; aplica-se a empresas não-UE vendendo à UE); **LBI Art. 63** obriga TODAS as empresas com sede/representação no Brasil; **ABNT NBR 17225:2025** (03/2025) finalmente dá régua técnica objetiva (~150 requisitos WCAG 2.2-mapeados); MPF recomendou regulamentação do Art. 63. Com ~99% de não-conformidade BR, o mercado de remediação é greenfield.
> 116	3. **Convergência de capability provada.** Os screen readers dominantes **já chamam OpenAI/Anthropic** para exatamente esta capability (JAWS PictureSmart, NVDA Content Describer) — o formato da tool e o padrão multi-modelo BYOK estão validados por terceiros independentes.
> 117	4. **Prontidão da infraestrutura MCORCH (extends-mcorch).** O precedente `mcorch_gitnexus` prova MCP server in-house com `StreamableHTTPServerTransport` no Sovereign Mesh hardened; billing mcoCoins atômico (4×-floor), credenciais per-tenant cifradas (Vault), sentinel, ES256 JWKS, agent-metering e malha GraphRAG+pgvector já existem em produção — o Vision MCP capitaliza, não constrói do zero.
> 118	5. **Economia de percepção viável.** O paradigma foveado é engenharia em produção (Quest Pro ETFR economiza 33–45% de GPU); a emulação software de princípios neuromórficos (v2e/OpenEB, MIT/Apache-2.0) permite um Tier 1 CPU quase-grátis que protege a margem do Tier 2 billable.
> 119	
> 120	**Contrapeso honesto (riscos de timing):** as duas metades isoladas já têm incumbentes first-party com distribuição superior; a demanda do produto cruzado é hipótese (OTD-VM-002); a saliência DeepGaze não tem transferência comprovada para telas/UIs (OTD-VM-001 — maior risco técnico do diferencial); e a regulação biométrica ANPD 2026 é alvo móvel (OTD-VM-007). O MRD responde a isso ancorando o caso de mercado no beachhead provado e exigindo gates de validação para a aposta.
> 121	
> 122	---
> 123	
> 124	## 6. Market Requirements
> 125	
> 126	> Priority: **Critical** (must have at launch) | **High** | **Medium** | **Low**  
> 127	> Source cita a seção do blueprint / FM-VM / OTD-VM de origem. House constraints (CLAUDE.md) já embutidas: credencial per-user (API Tenancy), mcoCoins só via `deduct_mco_coins` atômico + `refundMco`, sentinel `inspectPrompt` antes de cobrar, ES256 JWKS antes de confiar no `sub`, RLS default-deny + isolamento `user_id`(+`project_id`), embed-on-insert na malha.
> 128	
> 129	| ID | Market Requirement | Priority | Rationale | Source |
> 130	|----|-------------------|----------|-----------|--------|
> 131	| MR-VM-001 | **Beachhead assistivo:** tools de alt-text e descrição de tela por IA (`vision.alt_text`, `vision.describe_screen`) alinhadas a WCAG 2.2 SC 1.1.1 / NBR 17225, servindo "propósito equivalente" | Critical | Única fatia com demanda provada em 3 eixos independentes (uso + capability + regulação); entrada de menor risco | Blueprint §4-A, §6; OTD-VM-002 emendada |
> 132	| MR-VM-002 | **Dever de cuidado assistivo embarcado:** recusas categóricas duras (medicação/dosagem, alérgeno, mobilidade, emergência — template ToS Be My Eyes), sinalização de confiança/hedge em baixa certeza, gancho de escalonamento a verificação humana (padrão híbrido Aira) | Critical | Para usuário BLV dependente, descrição errada = dano físico real; usuários super-confiam em IA confiante (ASSETS 2024) | Blueprint §4-A; FM-VM-14 |
> 133	| MR-VM-003 | **Claims de conformidade controlados:** nunca afirmar "WCAG/NBR 17225-conformante" sem caminho de revisão humana e sem mapeamento requisito-a-requisito da norma | High | Claim falso de conformidade = exposição regulatória sob EAA/LBI Art. 63 | FM-VM-17; OTD-VM-019 |
> 134	| MR-VM-004 | **Produto cruzado vision×deepsearch como upsell hipótese-a-validar:** saída de visão fundamentada por evidência de deepsearch + consolidação na malha (`mesh.consolidate_reference`), com **gate de validação de demanda explícito** antes de investimento GTM dedicado | High | Whitespace genuíno sem competidor, mas sem validação de demanda — tratar como aposta mensurada, não mercado provado | Blueprint §1, §10; OTD-VM-002 |
> 135	| MR-VM-005 | **Acesso remoto MCP padrão:** endpoint único Streamable HTTP (spec 2025-11-25) + OAuth 2.1/RFC 9728 + PAT (`mcp_access_tokens`, hash SHA-256, scopes, RLS default-deny) em `mcp.mcorch.com`, consumível por Claude Desktop/Code, VS Code, ChatGPT e Claude API | Critical | Sem porta padrão não há ecossistema externo — a meta da Diretiva Sovereign; toda capability externa precisa de porta tool (connector Claude API só consome tools) | Blueprint §5.5, §6; FM-VM-01, FM-VM-06; OTD-VM-003 |
> 136	| MR-VM-006 | **Soberania/self-host:** deploy on-prem no Sovereign Mesh (container hardened, precedente gitnexus) como cunha contra o hosted-only da Roboflow | High | Único eixo de diferenciação estrutural contra o incumbente de vision-MCP | Blueprint §1, §5.1 |
> 137	| MR-VM-007 | **Credencial per-tenant BYOK fail-closed:** resolução per-user (`user_api_keys` — incluindo nova coluna `firecrawl_api_key`), env global só para cron/service-role, hard-fail 402 estruturado; segregação de quota e atribuição de receita por tenant | Critical | API Tenancy Model é UNBREAKABLE RULE; chave compartilhada = exaustão de quota + fraude por design | CLAUDE.md API Tenancy; Blueprint §5.2; FM-VM-05 |
> 138	| MR-VM-008 | **Billing metered transparente:** mcoCoins por tool call exclusivamente via RPC atômico `deduct_mco_coins` + `refundMco` on-failure; sentinel `inspectPrompt` **após** identidade e **antes** de cobrar; fórmula 4×-floor com medição material antes de fixar preço; BYOK anda de graça; planos híbridos Starter/Pro/Enterprise | Critical | Modelo credit-metered é o padrão observado nos comps (Roboflow/Exa/Firecrawl/Tavily); confiança de billing = pré-requisito de adoção externa | Blueprint §5.3, §6; FM-VM-06, FM-VM-07 |
> 139	| MR-VM-009 | **Economia de percepção em dois níveis ("Essência Humana"):** Tier 1 periférico barato/always-on (CPU, 0–1 mco, neuromórfico emulado) gateando o Tier 2 foveal billable; comunicar sempre como "event-like processing", jamais "microsecond sensing"; alvo de recall do gate medido e custo de falso-negativo explícito | High | Mantém custo por chamada baixo por design (análogo XR: 33–45% GPU economizada); honestidade técnica protege credibilidade | Blueprint §3; FM-VM-12; OTD-VM-001, OTD-VM-012 |
> 140	| MR-VM-010 | **Conformidade LGPD elevada + soberania de dados:** visão escopada a detecção/descrição (NUNCA template biométrico/recognition sem base art. 11 documentada); PII-strip antes de insert; conteúdo scrapeado NUNCA em system nodes; metadata de proveniência/licença/retenção; RPC `erase_vision_artifacts` (cascade nó+edges+embedding+frames); salvaguardas de transferência internacional | Critical | Faces/gait = dado sensível (art. 5º II / art. 11); legítimo interesse NÃO se aplica; precedente hiQ alcança corpus derivado | FM-VM-09, FM-VM-10, FM-VM-11; OTD-VM-007, OTD-VM-008 |
> 141	| MR-VM-011 | **Job semantics para deepsearch de minutos:** tool `start` → `job_id` + `poll`/progress notifications (semântica dentro do container, nunca chamada bloqueante); regra de **partial-delivery refund** definida antes do código | High | Deepsearch é trabalho de minutos; clients externos precisam de submit→poll que sobrevive a janelas de wall-clock e Cloudflare | Blueprint §5.1, §6; FM-VM-07; OTD-VM-003, OTD-VM-013 |
> 142	| MR-VM-012 | **Distribuição self-serve:** Plugin Zip versionado (connector URL pré-preenchida + skills PT-BR workflow-named) baixável de `/dashboard/settings → Connectors` + publicação no MCP Registry sob `com.mcorch/*` | Medium | Padrão de distribuição validado em produção (sandcastles, Roboflow); tools workflow-named, não CRUD cru | Blueprint §1, §6; BR-VM-007 hint |
> 143	| MR-VM-013 | **Anti-hype positioning:** proibido brandar "cognitive computing", "cérebro digital" ou claims de consciência; ancorar marketing/arquitetura em citações peer-reviewed (CoALA TMLR, V*/SEAL CVPR, GraphRAG); benchmark só com replicação independente | Medium | "Cognitive computing" é marca morta (Watson→Merative/watsonx); "agentic" carrega risco análogo (Gartner: agent washing, >40% cancelamento até 2027) | Blueprint §Pilar V; FM-VM-15; OTD-VM-017 |
> 144	| MR-VM-014 | **Percepção como órgão da arquitetura cognitiva existente:** toda percepção bem-sucedida escreve na Knowledge Mesh (nó observation + `content_mesh_asset`, embed-on-insert grátis, `user_id+project_id`); dois regimes de persistência — **observações decaem** (FSRS-6/`stability_score`), **fatos suplantam** (supersession) | Medium | O diferencial é a malha CoALA já montada, não a tool isolada; category error de persistência corrompe a malha | Blueprint §3, §Pilar V; FM-VM-16; Mesh Connection Mandate |
> 145	| MR-VM-015 | **Paridade de baseline + monetização B2B2C:** as tools assistivas devem igualar o baseline de feature das ofertas grátis de big tech (Seeing AI/Lookout); monetização recai sobre o B2B/compliance (padrão Be My Eyes: grátis ao usuário final, financiado por B2B; híbrido Aira) | Medium | Impossível cobrar do usuário BLV o que a big tech dá de graça; o pagador é a empresa sob compulsão legal | Blueprint §4-A, §10 |
> 146	| MR-VM-016 | **Língua de sinais explicitamente fora de escopo v1:** nenhum claim de suporte LIBRAS/sign language via avatar/MT | Low | Linha vermelha WFD+WASLI (avatar/MT ≠ intérprete); SignGemma é ASL→inglês não-GA | FM-VM-18; OTD-VM-018 |
> 147	
> 148	---
> 149	
> 150	## 7. Success Metrics (Market-Level KPIs)
> 151	
> 152	| KPI | Definition | Target (6-month) | Target (12-month) | Measurement |
> 153	|-----|-----------|------------------|-------------------|-------------|
> 154	| KPI-VM-001 — External MCP Connections | Tenants distintos com PAT/OAuth ativos consumindo `mcp.mcorch.com` | 1 interno (Usuário Zero/Pantheon) + ≥2 clients externos beta (Claude Desktop/Code) | ≥25 tenants ativos | `mcp_access_tokens` ativos + `agent_executions` por `user_id` distinto |
> 155	| KPI-VM-002 — Assistive Tool Adoption | Chamadas/mês de `vision.alt_text` + `vision.describe_screen` | ≥500 (dogfooding + beta) | ≥10.000 | Ledger `agent_executions` por tool |
> 156	| KPI-VM-003 — Cross-Product Validation Rate (**gate da hipótese OTD-VM-002**) | % de runs de visão que disparam grounding deepsearch + `mesh.consolidate_reference` | Baseline medido (sem meta — coleta honesta) | ≥15% OU decisão GO/NO-GO documentada sobre o upsell | `mcorch_nodes` observation com edge para nó de run |
> 157	| KPI-VM-004 — Unit Margin per Tool | Margem mcoCoin por tool ≥ 4× floor (fórmula `ceil(usd/$0.018×4)`) sobre custo medido materialmente | 100% das tools lançadas | 100% (recalibração contínua via SOP) | `docs/processes/mcoin-cost-calibration.md` + `agent_executions` custo real |
> 158	| KPI-VM-005 — Duty-of-Care Efficacy | Cobertura de recusa categórica em queries red-line (medicação/alérgeno/mobilidade/emergência) + incidentes de dano reportados | 100% recusa / 0 incidentes | 100% / 0 | Suite de teste adversarial + `infra_health_logs service='vision-mcp'` |
> 159	| KPI-VM-006 — Tier 1 Gate Recall | Recall do gate periférico (o que o Tier 1 não dispara, o Tier 2 nunca vê) | Baseline medido em domínio screen/UI (OTD-VM-001) | ≥ alvo fixado no FRD | Benchmark interno (V*Bench/UEyes candidatos) |
> 160	| KPI-VM-007 — Refund Integrity | % de falhas billable com refund automático material | 100% | 100% | `refundMco` + delta `mco_balance` por `SELECT` |
> 161	| KPI-VM-008 — NPS | Net Promoter Score de operadores B2B (compliance) e desenvolvedores MCP | ≥30 | ≥50 | Pesquisa in-app / canal Connectors |
> 162	
> 163	---
> 164	
> 165	## 8. Regulatory & Compliance Context
> 166	
> 167	> **Regulatory posture: LGPD ELEVADO** — faces e modo de andar (gait) são dado biométrico **sensível** (art. 5º II); o vertical assistivo adiciona dever de cuidado a população dependente.
> 168	
> 169	| Regulation | Applicability | Key Constraint | Compliance Owner |
> 170	|------------|---------------|----------------|-----------------|
> 171	| LGPD — biométrico (art. 5º II, art. 11) | **Crítica** — qualquer imagem/vídeo com pessoas | Só consentimento específico-destacado (art. 11 I) ou lista fechada art. 11 II; **legítimo interesse NÃO se aplica**; escopo do produto = detecção/descrição, NUNCA template/recognition/classificação biométrica; regulação ANPD 2026 é alvo móvel (OTD-VM-007, OTD-VM-008) | Engineering (Cyber-Sentinel) + Sovereign |
> 172	| LGPD — transferência internacional (art. 33) | Alta — VLM APIs US (OpenAI/Google/OpenRouter) | Não há adequação p/ EUA (só UE via Res. 32/2026); SCCs ANPD (Res. 19/2024) no DPA do provider, roteamento a território adequado, ou consentimento destacado; auditar DPAs para inputs de imagem (OTD-VM-005) | Engineering |
> 173	| LGPD — eliminação & retenção (art. 16) | Alta — nós persistentes/embeddados/bridgeados | RPC `erase_vision_artifacts` em cascata (nó+edges+embedding+frames+cópias provider); retention clock; precedente hiQ×LinkedIn alcança corpus derivado (FM-VM-11) | Engineering |
> 174	| WCAG 2.2 — SC 1.1.1 Non-text Content (Nível A) | Alta — âncora normativa de `vision.alt_text` | Alternativa textual deve servir "propósito equivalente"; claim de conformidade só com revisão humana (FM-VM-17) | Engineering + Sovereign |
> 175	| ABNT NBR 17225:2025 | Alta — régua técnica do Art. 63 no BR | ~150 requisitos WCAG 2.2-mapeados, dois níveis (Regular/Plena); mapeamento requisito-a-requisito pendente antes de claim de produto (OTD-VM-019) | Engineering |
> 176	| LBI Lei 13.146/2015 — Art. 63 | Alta — mercado primário BR | Acessibilidade web obrigatória para TODAS as empresas com sede/representação no BR + governo; enforcement imaturo mas crescente (MPF) | Sovereign (GTM) + Engineering |
> 177	| European Accessibility Act (Dir. 2019/882) | Média-Alta — clientes vendendo à UE | Exigível desde 28/06/2025; alcança empresas não-UE; multas variam por Estado-membro — não fixar número único (OTD-VM-016); transição de serviços existentes até 2030 | Engineering |
> 178	| Direitos autorais / scraping (CDSM Art. 4, robots.txt, ToS) | Média — deepsearch | Honrar robots.txt + opt-out CDSM; allowlist de fontes permissivas; bloquear login-wall; pinar wording de ToS na implementação (OTD-VM-009) | Engineering |
> 179	| Licenciamento OSS (AGPL/bespoke) | Média — stack de modelos | Pista Apache default (SAM 2, RF-DETR, Qwen3-VL, OpenEB); Ultralytics AGPL e SAM-3/DINOv3 gated só com termos documentados (FM-VM-08; OTD-VM-006) | Engineering |
> 180	
> 181	---
> 182	
> 183	## 9. Traceability Matrix Stub
> 184	
> 185	> BR-VM-001..009 derivam dos hints do blueprint §10; BRs marcados **(novo)** são lacunas que o BRD deve criar. Vínculo completo selado no `02-brd.md`.
> 186	
> 187	| MR ID | → BR ID | Rationale |
> 188	|-------|---------|-----------|
> 189	| MR-VM-001 | BR-VM-008 | Beachhead assistivo = conformidade de acessibilidade (WCAG/EAA/LBI/NBR) |
> 190	| MR-VM-002 | BR-VM-008 | Dever de cuidado assistivo (recusas + confiança + escalonamento) |
> 191	| MR-VM-003 | BR-VM-008 + BR-VM-006 | Claim de conformidade controlado entra no Risk Ledger |
> 192	| MR-VM-004 | BR-VM-010 _(novo — gate de validação do produto cruzado)_ | Hipótese OTD-VM-002 precisa de BR próprio com critério GO/NO-GO |
> 193	| MR-VM-005 | BR-VM-006 + BR-VM-007 | Superfície externa segura (PAT no Risk Ledger) + distribuição |
> 194	| MR-VM-006 | BR-VM-005 | Soberania de dados/deploy |
> 195	| MR-VM-007 | BR-VM-001 + BR-VM-002 | Atribuição de receita por tenant + segregação de quota |
> 196	| MR-VM-008 | BR-VM-003 | Billing mcoCoins atômico com refund-on-failure |
> 197	| MR-VM-009 | BR-VM-011 _(novo — economia de percepção dois-níveis com alvo de recall)_ | Tier 1/Tier 2 é decisão de negócio de custo, não só design |
> 198	| MR-VM-010 | BR-VM-004 + BR-VM-005 | LGPD (biométrico/transferência/erasure) + scraped nunca em system nodes |
> 199	| MR-VM-011 | BR-VM-003 + BR-VM-006 | Partial-delivery refund (billing) + job semantics (risco OTD-VM-003) |
> 200	| MR-VM-012 | BR-VM-007 | Distribuição self-serve (Plugin + skills + registry) |
> 201	| MR-VM-013 | BR-VM-009 | Anti-hype/positioning |
> 202	| MR-VM-014 | BR-VM-012 _(novo — Mesh Connection Mandate + regimes de persistência)_ | Percepção→malha com anti-category-error (FM-VM-16) |
> 203	| MR-VM-015 | BR-VM-010 _(novo)_ + BR-VM-003 | Baseline grátis vs monetização B2B2C define o pricing do beachhead |
> 204	| MR-VM-016 | BR-VM-006 | Exclusão de escopo registrada no Risk Ledger (FM-VM-18) |
> 205	
> 206	---
> 207	
> 208	_Generated by MCORCH BoK Scribe Agent v1.0.0_
> 209	
> ```

## 🤖 Claude *(18:49:59)*

I have most of what I need from the four BoK docs. The blueprint's deepsearch/Cognitive pillar detail and the existing repo's deep-research process are still needed. Let me read the rest of the blueprint and cross-check the existing grounded-research process.

## 🤖 Claude *(18:50:00)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/vision-mcp/00-deepsearch-blueprint.md",
  "offset": 258,
  "limit": 276
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 258	| Roboflow MCP (competidor) | (mercado) | product | produção | proprietária (hosted) | API | https://mcp.roboflow.com/llms.txt |
> 259	| Firecrawl MCP (deepsearch) | (mercado) | product | consolidado | MIT | API / self-host CPU | https://github.com/firecrawl/firecrawl-mcp-server |
> 260	| Exa MCP (deepsearch) | (mercado) | product | consolidado | MIT (wrapper) | API | https://github.com/exa-labs/exa-mcp-server |
> 261	| Tavily MCP (deepsearch) | (mercado) | product | consolidado | MIT (wrapper) | API | https://github.com/tavily-ai/tavily-mcp |
> 262	| x402 (micropagamento MCP) | (mercado) | spec | emergente | Apache-2.0 (a verif.) | API | https://docs.cdp.coinbase.com/x402/mcp-server |
> 263	| **CoALA — Cognitive Architectures for Language Agents** | Cognitive | paper | consolidado (TMLR 2024) | research | referência (mapa de memória) | https://arxiv.org/abs/2309.02427 |
> 264	| LangGraph Memory docs (cita CoALA verbatim) | Cognitive | doc | produção | — | referência | https://docs.langchain.com/oss/python/langgraph/memory |
> 265	| Microsoft GraphRAG | Cognitive | library | produção (demo OSS) | MIT (a verif.) | self-host CPU/GPU | https://github.com/microsoft/graphrag |
> 266	| Anthropic computer-use tool | Cognitive | API | produção (beta) | proprietária | API | https://platform.claude.com/docs/en/docs/agents-and-tools/tool-use/computer-use-tool |
> 267	| Survey: Memory Mechanism of LLM Agents (Zhang et al.) | Cognitive | survey | consolidado | research | referência | https://arxiv.org/abs/2404.13501 |
> 268	| The Missing Knowledge Layer (persistência: fatos suplantam, memórias decaem) | Cognitive | paper | emergente (2026) | research | referência (regra FSRS) | https://arxiv.org/abs/2604.11364 |
> 269	| Soar (EpMem/SMem, 9.6.5) | Cognitive | library | consolidado (linhagem) | BSD-3 (a verif.) | self-host CPU/GPU | https://soar.eecs.umich.edu/ |
> 270	| ACT-R (CMU) | Cognitive | research | ativo (modelagem) | research | referência (teoria de decay) | http://act-r.psy.cmu.edu/ |
> 271	| Global Workspace Agents ("Theater of Mind") | Cognitive | paper | research (preprint 2026) | research | referência (broadcast metáfora) | https://arxiv.org/abs/2604.08206 |
> 272	| GWT × Language Agents (consciência — fora de escopo) | Cognitive | paper | research | research | referência (delimitar escopo) | https://arxiv.org/abs/2410.11407 |
> 273	| pymdp (active inference, JOSS 2022) | Cognitive | library | peer-reviewed OSS | research | self-host CPU/GPU | https://github.com/infer-actively/pymdp |
> 274	| AXIOM (active inference, Verses) | Cognitive | paper | research (benchmark vendor) | research | referência | https://arxiv.org/abs/2505.24784 |
> 275	| Gartner Hype Cycle AI 2025 (agent washing) | Cognitive | analyst | sinal de indústria | — | referência | https://www.gartner.com/en/newsroom/press-releases/2025-08-05-gartner-hype-cycle-identifies-top-ai-innovations-in-2025 |
> 276	| **Be My Eyes — 1M usuários BLV / 10M voluntários** | Assistive | product | produção (GA 2015, AI 2023) | proprietária | API (B2B-funded) | https://www.bemyeyes.com/news/be-my-eyes-reaches-1-million-blind-and-low-vision-users-and-10-million-volunteers/ |
> 277	| Microsoft Seeing AI | Assistive | product | produção (free) | proprietária | app (iOS/Android) | https://blogs.microsoft.com/accessibility/seeing-ai-app-launches-on-android-including-new-and-updated-features-and-new-languages/ |
> 278	| Aira (humano-on-demand + Access AI grátis) | Assistive | product | produção (hybrid) | proprietária | API/serviço | https://aira.io/subscriptions/ |
> 279	| JAWS PictureSmart AI (OpenAI + Anthropic Claude) | Assistive | product | produção (JAWS 2024) | proprietária | embed (screen reader) | https://vispero.com/news/freedom-scientific-unveils-revolutionary-picturesmart-ai-for-jaws/ |
> 280	| NVDA AI Content Describer | Assistive | add-on | produção (OSS) | ver repo | self-host CPU; multi-provider | https://github.com/cartertemm/AI-content-describer |
> 281	| WHO — Blindness & visual impairment (2.2B) | Assistive | stats | autoritativo (02/2026) | público | referência (TAM) | https://www.who.int/news-room/fact-sheets/detail/blindness-and-visual-impairment |
> 282	| W3C WCAG 2.2 — SC 1.1.1 Non-text Content | Assistive | standard | W3C Rec | aberta | normativo (alt text) | https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html |
> 283	| European Accessibility Act (Dir. 2019/882) | Assistive | lei | em vigor (28/06/2025) | — | conformidade | https://accessible-eu-centre.ec.europa.eu/content-corner/news/eaa-comes-effect-june-2025-are-you-ready-2025-01-31_en |
> 284	| LBI Lei 13.146/2015 — Art. 63 | Assistive | lei | em vigor (BR) | — | conformidade | https://www2.camara.leg.br/legin/fed/lei/2015/lei-13146-6-julho-2015-781174-publicacaooriginal-147468-pl.html |
> 285	| ABNT NBR 17225:2025 (Acessibilidade Digital) | Assistive | norma | publicada (03/2025) | — | conformidade (WCAG 2.2-mapeada) | https://www.gov.br/mdh/pt-br/assuntos/noticias/2025/marco/com-apoio-do-governo-federal-nova-norma-tecnica-da-abnt-e-instituida-para-impulsionar-acessibilidade-digital-no-brasil |
> 286	| eMAG v3.1 (modelo gov federal) | Assistive | standard | legado (2014) | — | conformidade (gov) | https://emag.governoeletronico.gov.br/ |
> 287	| Be My Eyes — Terms of Service (duty-of-care) | Assistive | legal | em vigor | — | referência (guardrails) | https://www.bemyeyes.com/terms-of-service/ |
> 288	| ASSETS 2024 — Misfitting With AI (overtrust BLV) | Assistive | paper | peer-reviewed | research | referência (uncertainty) | https://dl.acm.org/doi/10.1145/3663548.3675659 |
> 289	| WFD + WASLI — Statement on Signing Avatars | Assistive | position | autoritativo (comunidade) | — | referência (red line LIBRAS) | https://wfdeaf.org/resources/statement-on-use-of-signing-avatars/ |
> 290	
> 291	---
> 292	
> 293	## 4-A. Tecnologia Assistiva — vertical de aplicação e evidência de demanda
> 294	
> 295	> **Por que esta seção existe.** A recon original (Seção 1) foi honesta: o produto cruzado vision+deepsearch é **whitespace sem validação de demanda** (OTD-VM-002). A pesquisa de Tecnologia Assistiva fecha parte desse buraco — ela fornece a **evidência de demanda mais forte que existe hoje** para um serviço de descrição visual por IA, em três eixos independentes (uso, convergência de capability, regulação). Isto **muda a hipótese**: a descrição/alt-text assistiva é um **beachhead demand-provado**, enquanto o grounding vision+deepsearch permanece hipótese (ver OTD-VM-002 emendada na Seção 8).
> 296	
> 297	### Evidência de demanda (com números fonteados)
> 298	
> 299	- **Be My Eyes** atingiu **1 milhão de usuários cegos/baixa-visão (BLV) e 10 milhões de voluntários** (anúncio 2026-03-12 no CSUN), em **150+ países e 180+ idiomas**, e lançou a Be My Eyes Foundation ([fonte](https://www.bemyeyes.com/news/be-my-eyes-reaches-1-million-blind-and-low-vision-users-and-10-million-volunteers/)). No 10º aniversário (jan/2025) reportou **43 milhões de requests de IA+vídeo/ano**, crescimento de receita **>300%**, 97% de satisfação e clientes enterprise (Google, Microsoft, Hilton, Spotify, P&G, Unilever) — modelo **gratuito ao usuário final, financiado por B2B** ([10 anos](https://www.bemyeyes.com/blog/be-my-eyes-celebrates-10-years-and-a-decade-of-accessibility-innovation/)). **Be My AI** lançou sobre o GPT-4 da OpenAI em 2023.
> 300	- **Taxa de substituição IA-vs-humano:** no deployment do Microsoft Disability Answer Desk, **~10%** dos usuários escolheram escalar para humano após a IA, com **~4 min** (IA) vs **12 min** (humano) por chamada ([PYMNTS/BusinessWire](https://openai.com/index/be-my-eyes/)) — input direto de unit-economics para um serviço de descrição.
> 301	- **Disposição a pagar:** **Aira** cobra **US$26–US$1.160/mês** por interpretação visual humana, enquanto o tier **Access AI é grátis com verificação humana opcional** — o **padrão híbrido** IA-grátis + humano-pago-para-verificar ([Aira pricing](https://aira.io/subscriptions/)). Hardware vai de **US$399** (Envision Ally Solos, pré-venda) a **~US$4.250** (OrCam MyEye 3 Pro, offline).
> 302	- **Big tech já oferece de graça:** **Microsoft Seeing AI** (iOS/Android, 18→36 idiomas, rich descriptions + chat-com-documento) e **Google Lookout** (Q&A de imagem via Gemini) — definem o **baseline de feature** que qualquer tool MCP de visão precisa igualar ([Seeing AI](https://blogs.microsoft.com/accessibility/seeing-ai-app-launches-on-android-including-new-and-updated-features-and-new-languages/)).
> 303	- **Tamanho top-down:** a OMS conta **2,2 bilhões de pessoas** com deficiência visual (fact sheet 02/2026), com perda de produtividade global ≈ **US$411 bilhões/ano** ([WHO](https://www.who.int/news-room/fact-sheets/detail/blindness-and-visual-impairment)).
> 304	
> 305	### Ângulo regulatório (a outra metade da demanda — compulsão legal)
> 306	
> 307	- **WCAG 2.2 SC 1.1.1 (Nível A)** exige alternativa textual para **todo conteúdo não-textual**, servindo "o propósito equivalente" ([W3C](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html)) — a âncora normativa de uma tool `vision.alt_text`.
> 308	- **European Accessibility Act** (Dir. 2019/882) é **exigível desde 28/06/2025** (e-commerce, bancos, transporte, telecom, dispositivos de consumo), **aplica-se a empresas não-UE que vendem ao consumidor da UE**; isenção de microempresa cobre **serviços apenas**; serviços existentes têm transição até **2030**. Notificações legais de advocacy francês saíram **dias** após o prazo ([AccessibleEU](https://accessible-eu-centre.ec.europa.eu/content-corner/news/eaa-comes-effect-june-2025-are-you-ready-2025-01-31_en)).
> 309	- **Brasil (mercado de origem do projeto) — escopo mais amplo que o EAA:** a **LBI (Lei 13.146/2015), Art. 63** torna acessibilidade web **obrigatória para TODAS as empresas com sede ou representação comercial no Brasil** + governo (sem lista setorial) ([Câmara](https://www2.camara.leg.br/legin/fed/lei/2015/lei-13146-6-julho-2015-781174-publicacaooriginal-147468-pl.html)). A novíssima **ABNT NBR 17225:2025** (publicada 03/2025; ~150 requisitos mapeados a WCAG 2.2; dois níveis — Conformidade **Regular** e **Plena**) finalmente dá ao Art. 63 um **régua técnica objetiva** ([Gov.br/MDH](https://www.gov.br/mdh/pt-br/assuntos/noticias/2025/marco/com-apoio-do-governo-federal-nova-norma-tecnica-da-abnt-e-instituida-para-impulsionar-acessibilidade-digital-no-brasil)); o **eMAG v3.1 (2014)** é o modelo federal obrigatório-mas-defasado. Aplicação ainda imatura mas crescente: **<1–3%** dos sites brasileiros são acessíveis (0,74% plenamente — BigDataCorp/Movimento Web para Todos) e o **MPF** recomendou regulamentação do Art. 63.
> 310	
> 311	### Quais tools MCP servem o vertical (mapeamento 1:1 a produtos provados)
> 312	
> 313	| Tool MCP (Seção 6) | Produto-espelho provado | Norma/citação |
> 314	|---|---|---|
> 315	| `vision.alt_text` | Meta AAT, alt-text de compliance | WCAG 2.2 SC 1.1.1 / NBR 17225 |
> 316	| `vision.describe_screen` | JAWS PictureSmart AI; NVDA AI Content Describer | [JAWS](https://vispero.com/news/freedom-scientific-unveils-revolutionary-picturesmart-ai-for-jaws/) · [NVDA](https://github.com/cartertemm/AI-content-describer) |
> 317	| `vision.ocr` (já existe) + `vision.describe_image` | Seeing AI (OCR+chat); Be My AI (scene Q&A) | [Seeing AI](https://blogs.microsoft.com/accessibility/seeing-ai-app-launches-on-android-including-new-and-updated-features-and-new-languages/) |
> 318	| `vision.analyze_video` (human-in-loop) | AI audio description (research-mature, **não** autônoma) | — |
> 319	
> 320	Os screen readers dominantes **já chamam OpenAI/Anthropic** para essa exata capability — JAWS PictureSmart usa "ChatGPT da OpenAI **e** Claude da Anthropic"; o NVDA AI Content Describer é provider-agnóstico (GPT/Gemini/Claude/Grok). Isto **valida o formato da tool e o padrão multi-modelo** que o MCORCH já tem nativo (per-user BYOK).
> 321	
> 322	### Dever de cuidado — descrição errada = dano real (sourced)
> 323	
> 324	Para usuários **dependentes**, uma descrição incorreta é dano no mundo físico, não um bug cosmético. Os **Termos de Serviço da própria Be My Eyes** proíbem confiar no serviço para **identificação/dosagem de medicamento, checagem de alérgenos, mobilidade e emergências** ([ToS](https://www.bemyeyes.com/terms-of-service/)). Pesquisa peer-reviewed (ASSETS 2024) mostra que usuários BLV **super-confiam** em saída de IA confiante porque **não têm ground truth** para detectar alucinações — o tom "humanístico" e seguro **encoraja** o overtrust ([Misfitting With AI](https://dl.acm.org/doi/10.1145/3663548.3675659)). Logo, **toda tool assistiva DEVE** embarcar: (1) **sinalização de confiança / linguagem hedge** para conteúdo de baixa certeza; (2) **recusas categóricas duras** em queries de medicação/alérgeno/navegação/emergência (template Be My Eyes); (3) **gancho de escalonamento para verificação humana** (padrão híbrido Aira). **Língua de sinais está fora de escopo do v1:** SignGemma (2025) é ASL→inglês, em teste; WFD+WASLI traçam linha vermelha contra avatares/MT como substitutos de intérprete humano ([WFD/WASLI](https://wfdeaf.org/resources/statement-on-use-of-signing-avatars/)).
> 325	
> 326	---
> 327	
> 328	## 5. Arquitetura MCORCH-nativa
> 329	
> 330	> Cada escolha aterrada em referência concreta de repo que o agente de mapeamento estabeleceu (e que confirmei materialmente nesta sessão).
> 331	
> 332	### 5.1 Runtime recomendado — Container no Sovereign Mesh
> 333	
> 334	**Decisão: Docker container `mcorch_vision_mcp`** no Sovereign Mesh, **Node/Bun + `@modelcontextprotocol/sdk` `StreamableHTTPServerTransport`**, publicado **loopback-only** (`127.0.0.1:<porta>`) e proxiado pelo nginx do host sob um novo vhost **`mcp.mcorch.com`**.
> 335	
> 336	**Por quê (3 razões aterradas):**
> 337	1. **Precedente direto.** `mcorch_gitnexus` já roda um MCP server in-house com `StreamableHTTPServerTransport` em `127.0.0.1:3100` dentro do mesh hardened — confirmado em `packages/gitnexus-core/src/mcp/server.ts:16,97` + `docker-compose.yml:89-119`. O envelope de hardening (`x-hardening` anchor em `docker-compose.yml:8`: `cap_drop`/`read_only`/UID 1001/`pids_limit`), o healthcheck node (`docker-compose.yml:113`) e a telemetria watchdog são reutilizáveis as-is. `mcorch_vision_mcp` entra na rede `mcorch-sovereign-net`.
> 338	2. **Timeouts matam a rota Edge.** O histórico do próprio repo prova que limites de wall-clock do Supabase Edge forçaram o pipeline orchestrate a virar passos async encadeados por pg_net (`docs/processes/orchestrate-async-pipeline.md`; RPC `async_orchestrate_step`). Deepsearch é, por definição, trabalho de minutos — não pode bloquear num isolate Edge. Um container long-lived não tem teto de execução (nginx `proxy_read_timeout` + `proxy_buffering off` tratam SSE) e zero cold-start.
> 339	3. **systemd (opção c) regrediria o BoK de segurança.** O FM-10 foi corrigido movendo o gitnexus para um container hardened não-root (`docker-compose.yml:2-3`); um serviço tenant-facing/billable merece o mesmo envelope `cap_drop`/`no-new-privileges`/`mem_limit`, não um processo bare no host.
> 340	
> 341	**Caveat material:** NÃO adicionar campo `name:` ao `docker-compose.yml` (o projeto deve permanecer `constellation-orchestra` ou containers rodando viram órfãos). Para deepsearch: implementar **semântica de job dentro do container** (tool `start` retorna `job_id` + progress notifications / tool `poll`), não chamada bloqueante.
> 342	
> 343	### 5.2 Auth — API Tenancy per-user (fail-closed)
> 344	
> 345	O container **não** fica atrás do Kong, então a verificação de identidade é 100% in-app. O repo já resolveu exatamente isso para edge functions `verify_jwt=false`: **verificação ES256 via JWKS** (`docs/processes/edge-jwt-identity-verification.md:47-79` — `jose` `jwtVerify` + `createRemoteJWKSet` contra `…/auth/v1/.well-known/jwks.json`). O mesmo código roda em Node.
> 346	
> 347	- **Ordem de resolução de credencial (mandatória, CLAUDE.md §API Tenancy):** (1) tabela per-user (`decrypted_user_api_keys` por `user_id`, padrão `orchestrate-content/index.ts:60-66`) → (2) env vault fallback só para cron/service-role → (3) hard-fail HTTP 402/501 estruturado.
> 348	- **Gap conhecido:** **não existe coluna `firecrawl_api_key`** em `user_api_keys` hoje (firecrawl só aparece em scripts QA com env key). Adicionar a coluna + UI Settings + fail-closed `firecrawl_not_configured` (padrão de 1 linha: migration `20260601060000_user_api_keys_apify_token.sql:12`; encryption pelo Vault trigger family).
> 349	- **Anti-pattern proibido:** `Deno.env.get('FIRECRAWL_API_KEY')` em fluxo user-facing sem fallback per-user → exaustão de quota por um tenant, sem atribuição de receita, blast radius financeiro compartilhado.
> 350	- **Regra anti-confused-deputy:** o `deduct_mco_coins` tem grant service_role (`20260603220000`); o container só pode deduzir contra `user_id` **verificado por ele mesmo** (sub do token assinado), nunca de campo não-verificado. NUNCA `atob` cego no sub (`edge-jwt-identity-verification.md:118-124`).
> 351	
> 352	### 5.3 Billing — mcoCoins atômico (modelo 4×-floor)
> 353	
> 354	- **Dedução atômica:** RPC `deduct_mco_coins(p_user_id, p_amount, p_action, p_context)` (assinatura `20260603220000:37-74`), chamada via PostgREST com `SB_SECRET_KEY` **após** verificar identidade. Saldo insuficiente → **HTTP 402**.
> 355	- **Cobrança na entrada + refund-on-failure:** `refundMco` (`_shared/billing.ts:20-38`, credit service-role-only, nunca lança); padrão catch `orchestrate-content/index.ts:207-221`.
> 356	- **Metering por leg LLM:** `_shared/agent-metering.ts:69-127` (`calc_agent_cost_mcoin` + ledger `agent_executions` + `deduct_mco_coins`); **BYOK anda de graça** (`isUserCustomKey → cost 0`); exempção `SOVEREIGN_USER_ID`.
> 357	- **Fórmula de preço (SSOT `docs/processes/mcoin-cost-calibration.md`, confirmada):**
> 358	  `mco(op) = ceil( real_cost_usd(op) / USD_PER_MCO_FLOOR ($0.018) × MARGIN (4) )`.
> 359	  **Classes de preço (derivadas dos custos medidos ao vivo 2026-06-11 — Seção 6).** Regra do SOP: medir o $ real materialmente antes de fixar; espelhar em `src/lib/billing.ts → COIN_COSTS` **e** numa constante hardcoded no serviço (ele não importa `src/lib`); asserir em `src/test/billing.test.ts`.
> 360	
> 361	### 5.4 Mesh Connection Mandate
> 362	
> 363	Template `orchestrate-step/index.ts:424-462`: em todo run bem-sucedido, inserir nó `observation` em `mcorch_nodes` (`metadata.cost_mco`, `stability_score 1.0`) + `content_mesh_asset` com `project_id`. Toda falha → `infra_health_logs` com `service='vision-mcp'` (padrão fire-and-forget `_shared/llm-fallback.ts:19-35`). Traceabilidade: cada nó/log carrega o BR/FR ID da suíte BoK (Seção 10). Health do container → Neural HUD via `scripts/watchdog-mcorch.sh` + `get-infra-status` (zero novo encanamento depois que o watchdog aprende o nome do container).
> 364	
> 365	### 5.5 Exposição externa — Streamable HTTP + OAuth 2.1
> 366	
> 367	Conformidade mínima 2025-11-25 (servidor remoto protegido):
> 368	- **Transporte:** endpoint único Streamable HTTP (POST → `application/json` ou `text/event-stream`; GET → SSE server-initiated). Validar header **Origin** (403 em inválido, anti DNS-rebinding). Honrar `MCP-Protocol-Version` por request. Usar a semântica de disconnect/poll do SSE para sobreviver a janelas de wall-clock e limites do Cloudflare ([transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)).
> 369	- **Auth:** RFC 9728 Protected Resource Metadata (`/.well-known/oauth-protected-resource`) apontando ao AS; bearer no header **Authorization** em todo request (nunca query string); validar **audience** do token; **token passthrough proibido**; PKCE S256; preferir **Client ID Metadata Documents** sobre DCR ([authorization](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)). O AS pode ser o Supabase Auth fronteado, ou um vendor (WorkOS/Auth0) — decisão do SDD.
> 370	- **PAT para clients MCP externos:** sessions JWT do Supabase expiram em ~1h, inúteis para configs de client long-lived. **Não existe** tabela de PAT no repo. **Novo design obrigatório:** tabela `mcp_access_tokens` (`user_id`, **hash SHA-256 do token** — nunca plaintext/Vault-reversível, `scopes`, `expires_at`, `revoked_at`, RLS `auth.uid()=user_id`, default-deny) + `/security-review` na migration (mandato FMEA-011). Scopes DEVEM excluir gestão de credencial (vazamento de PAT = dreno direto da carteira mcoCoins).
> 371	- **Descoberta:** publicar `server.json` via `mcp-publisher` sob namespace verificado `com.mcorch/*` (challenge DNS/HTTP) no MCP Registry (preview) ([registry](https://modelcontextprotocol.io/registry/about)).
> 372	- **Sentinel:** `_shared/sentinel.ts` (TS puro, portável a Node) — `inspectPrompt` L1/L2/L3 **após** identidade, **antes** de cobrar; `logSentinelBlock → infra_health_logs service='sentinel'`.
> 373	
> 374	---
> 375	
> 376	## 6. Superfície MCP proposta
> 377	
> 378	> Rascunho de tools/resources/prompts. Custo em classes mcoCoins derivadas dos preços medidos ao vivo (2026-06-11), fórmula `ceil(usd/$0.018×4)`. **Toda tool: gate sentinel `inspectPrompt` nos args + verificação de identidade antes de cobrar.** Números são **calibração inicial** — o SOP exige medição material antes do fix em `COIN_COSTS`.
> 379	
> 380	### Tools (model-controlled — front-door para ecossistemas externos)
> 381	
> 382	| Tool | Contrato (1 linha) | Input gate (sentinel) | Classe mcoCoin |
> 383	|---|---|---|---|
> 384	| `vision.describe_image` | VLM QA sobre 1 imagem (Gemini/Qwen/Claude/GPT-5.x) → texto/structuredContent | inspect prompt + URL/host allowlist | **2** (cobre lane premium: img única $0.0006–0.0107) |
> 385	| `vision.detect_objects` | Detecção de objetos via Gemini native boxes `[ymin,xmin,ymax,xmax]` | inspect prompt | **2** |
> 386	| `vision.segment` | Segmentação promptável (texto/box/point) via SAM-3 (fal) / SAM-2 (Replicate) | inspect prompt | **2** (fal $0.005) / **5** (Replicate $0.019) |
> 387	| `vision.ocr` | OCR documento → markdown/JSON (Mistral OCR 3 direta / PaddleOCR CPU) | inspect + provenance tag | **1 / página** ($0.002→margem 9×) |
> 388	| `vision.analyze_video` | QA temporal sobre vídeo (Gemini video, 1 FPS default) | inspect + duração cap | **2 / minuto** (default res; low-res ~0.7/min) |
> 389	| `motion.peripheral_scan` | **Tier 1** — gate barato: frame-diff/MOG2 + saliência → regiões salientes (retorna `resource_link` p/ crops) | inspect | **1** ou **0** (CPU) |
> 390	| `motion.track` | Pose (RTMPose/MediaPipe) + tracking (ByteTrack/BoT-SORT) sobre vídeo curto | inspect | **1** (hot GPU ≤8s L40S) |
> 391	| `deepsearch.scrape` | Scrape de 1 URL pública (Firecrawl, logged-out) → markdown + provenance | inspect + robots.txt + login-wall block | **1** ($0.00083/página) |
> 392	| `deepsearch.run` | Job de deepsearch (N searches + scrapes) → `job_id`; conclui via progress/poll | inspect + allowlist de fontes | **3** (bundle ~$0.013) |
> 393	| `deepsearch.poll` | Recupera resultado de job assíncrono por `job_id` | scope check | **0** |
> 394	| `mesh.search` | Busca semântica na Knowledge Mesh do tenant (`match_mcorch_nodes`) | scope `auth.uid()` | **0–1** |
> 395	| `mesh.consolidate_reference` | Grava referência consolidada (vision+deepsearch) como nó observation + embed | inspect + LGPD/PII strip + provenance | **1** (embed grátis) |
> 396	| `vision.alt_text` | **(Assistiva)** alt-text WCAG 2.2 SC 1.1.1 / NBR 17225-conformante (curto + longo) + detecção de imagem decorativa → texto que serve "propósito equivalente" | inspect + **duty-of-care gate** (recusa medicação/alérgeno/navegação/emergência) + confidence flag | **2** (lane img única) |
> 397	| `vision.describe_screen` | **(Assistiva)** descrição de screenshot/UI (padrão JAWS PictureSmart / NVDA Content Describer) com sinalização de incerteza | inspect + **duty-of-care gate** + confidence flag | **2** (lane img única) |
> 398	
> 399	> **Camada de dever de cuidado (obrigatória nas tools assistivas — Seção 4-A + FM-VM-14):** as tools `vision.alt_text`/`vision.describe_screen` (e `vision.describe_image`/`vision.ocr`/`vision.analyze_video` quando em uso assistivo) DEVEM (a) recusar categoricamente queries de medicação/dosagem, alérgeno, mobilidade e emergência (template ToS Be My Eyes); (b) emitir **confidence/hedge** em conteúdo de baixa certeza (ASSETS 2024); (c) expor gancho de **escalonamento a verificação humana** (padrão Aira). "Conformante a WCAG/NBR" é claim controlado — só com caminho de revisão humana (ver FM-VM-17). Custo na classe **2** (mesma lane de imagem única do `vision.describe_image`, fórmula `ceil(usd/$0.018×4)`).
> 400	
> 401	### Resources (application-driven — progressive enhancement p/ hosts completos)
> 402	
> 403	| Resource (URI template) | Conteúdo |
> 404	|---|---|
> 405	| `mesh://nodes/{node_id}` | Nó da malha (referência/observation) do tenant, RLS-scoped |
> 406	| `mesh://references?pillar={cv\|motion\|neuromorphic\|foveated}` | Corpus de referências consolidadas por pilar |
> 407	| `vision://artifacts/{content_ref}` | Frames/crops cacheados (Storage privado, signed URL curto) |
> 408	
> 409	> ⚠️ O Claude API MCP connector consome **só tools** — resources/prompts são enhancement para hosts completos (Claude Desktop/Code, VS Code). Toda capability que precisa ser alcançável por ecossistemas externos precisa de uma **porta tool**.
> 410	
> 411	### Prompts (user-controlled — workflows empacotados, estilo skills/slash)
> 412	
> 413	| Prompt | Workflow |
> 414	|---|---|
> 415	| `/vision-essence` | Pipeline completo Essência Humana: peripheral_scan → foveal analysis → grounding → consolidação na malha |
> 416	| `/reference-brief` | "Faça um brief de referências consolidadas sobre {tópico} contra a visão {pilar}" |
> 417	| `/competitive-vision` | Análise de criativo/produto (imagem/vídeo) fundamentada por deepsearch de mercado |
> 418	
> 419	**Distribuição (lição do sandcastles, aplicada):** empacotar connector + skills PT-BR num **Plugin Zip versionado** baixável de `/dashboard/settings → Connectors` (com API-key + URL MCP + instruções), replicando do formato público de plugins/skills da Anthropic — **não** reverse-engineering do artefato deles.
> 420	
> 421	---
> 422	
> 423	## 7. Riscos & FMEA-seed
> 424	
> 425	| # | Vetor | Modo de falha | Severidade | Mitigação (gate) |
> 426	|---|---|---|---|---|
> 427	| FM-VM-01 | **Security — superfície pública** | `mcp.mcorch.com` é o 1º serviço tenant-facing fora do gateway Supabase; bug fail-open = impersonação cross-tenant (a classe que o SOP ES256 corrigiu) | Crítica | JWKS-verify antes de confiar no `sub`; **fail-closed** se JWKS inalcançável; nunca expor `SB_SECRET_KEY` em path client-reachable |
> 428	| FM-VM-02 | **Prompt-injection (inbound)** | Args de tool hostis manipulam o agente | Alta | `_shared/sentinel.ts` `inspectPrompt` L1/L2/L3 nos args, antes de cobrar |
> 429	| FM-VM-03 | **Indirect prompt-injection (scraped)** | Conteúdo web hostil scrapeado vira nó da malha consumido por agentes internos (corpus Pantheon) — vetor de injeção **persistente** | Alta | Rodar sentinel L2 (`lexicalScore`/control-chars) sobre texto **extraído** antes do insert; tag de origem `scraped` no metadata p/ trust por proveniência |
> 430	| FM-VM-04 | **Image-borne injection** | Instruções do atacante renderizadas **dentro** da imagem/tela, lavadas via OCR/VLM para o loop do agente | Média-Alta | ⚠️ Não pesquisado a fundo — sentinel cobre texto; **estender SOP a outputs de vision-tool** (citar OWASP LLM01 / MCP tool-poisoning) |
> 431	| FM-VM-05 | **Tenancy — firecrawl env key** | Shared `FIRECRAWL_API_KEY` em fluxo user-facing → exaustão de quota, sem atribuição de receita, blast radius compartilhado | Alta | Coluna `firecrawl_api_key` per-user + UI + 402 `firecrawl_not_configured` antes de exposição externa |
> 432	| FM-VM-06 | **Billing — PAT leak** | Vazamento de PAT = dreno direto da carteira mcoCoins via tool calls billable | Crítica | `mcp_access_tokens` com hash SHA-256, scopes (sem gestão de credencial), `expires_at`/`revoked_at`, RLS default-deny, `/security-review` |
> 433	| FM-VM-07 | **Billing — job parcial** | Job de minutos que sucede parcialmente (5 de 12 páginas) tem semântica de refund ambígua | Média | Definir regra de **partial-delivery refund** no FRD antes do código; cobrança contra identidade verificada pelo container |
> 434	| FM-VM-08 | **Licensing — AGPL/bespoke** | Ultralytics AGPL servido em rede sem licença Enterprise = violação; SAM/DINOv3 propagam termos de redistribuição | Alta | SDD escolhe pista Apache (SAM 2, RF-DETR, Qwen3-VL, OpenEB); se SAM 3/DINOv3, importar atribuição + propagação + gated-distribution; fetch dos LICENSE files |
> 435	| FM-VM-09 | **LGPD — dado biométrico** | Faces/gait são **dado sensível** (LGPD art. 5º II); só consentimento específico-destacado (art. 11 I) ou lista fechada art. 11 II — **legítimo interesse NÃO se aplica**; ANPD lista "modo de andar" como biométrico | Crítica | Escopar vision **para detecção/descrição, NÃO geração de template/recognition/classificação** sem base art. 11 documentada; watch da regulação ANPD 2026 |
> 436	| FM-VM-10 | **LGPD — PII de terceiros / transferência internacional** | Screenshots/scraping capturam PII; envio a APIs US (OpenAI/Google/OpenRouter) é transferência internacional; **não há adequação p/ EUA** (só UE via Res. 32/2026) | Alta | PII-strip antes do insert; SCCs ANPD (Res. 19/2024) no DPA do provider, ou roteamento p/ território adequado, ou consentimento art. 33 VIII destacado |
> 437	| FM-VM-11 | **LGPD/IP — erasure & corpus** | Nós persistentes/embeddados/bridgeados p/ memória OpenClaw sem path de apagamento; precedente hiQ×LinkedIn alcançou o **corpus derivado** ($500k + deleção) | Alta | RPC `erase_vision_artifacts(content_ref)` espelhando `erase_lead()` (cascade: nó + edges + embedding + frames Storage + cópias provider); retention clock (art. 16); allowlist de fontes permissivas (Wikipedia/PLOS/Frontiers/SEC EDGAR/IPFS); honrar robots.txt + CDSM Art. 4 opt-out |
> 438	| FM-VM-12 | **Custo — cold start** | Inferência GPU sub-segundo a 1 mco só fecha com container **warm**; cold start (10–60s) estoura o budget | Média | Keep-warm ou batch semantics; medir $ real antes de fixar mco |
> 439	| FM-VM-13 | **Process — BoK gate** | Código escrito sem `docs/bok/vision-mcp/{01-mrd..05-sdd}` viola Closed-Loop Protocol; sem BR/FR IDs não há traceabilidade de mesh-mandate | Bloqueante | `/bok-scribe vision-mcp` antes de qualquer código; Lei 2 — SOP `docs/processes/vision-mcp-*.md` antes da automação |
> 440	| FM-VM-14 | **Assistive — dever de cuidado / acurácia** | Para usuário BLV **dependente**, descrição errada = dano físico real (medicação/alérgeno/mobilidade/emergência); usuários **super-confiam** em IA confiante por falta de ground truth (ASSETS 2024) | Crítica | Recusas categóricas (template ToS Be My Eyes); **confidence/hedge** em baixa certeza; gancho de **escalonamento humano** (híbrido Aira); disclaimer "as is"; gate nas tools `vision.alt_text`/`vision.describe_screen` |
> 441	| FM-VM-15 | **Marketing — cognitive/agent-washing** | Brandar o produto como "cognitive computing" (termo Watson morto) / "cérebro digital" / claims de consciência GWT cria expectativa não-falsificável + crítica de "agent washing" (Gartner, >40% cancel) + risco reputacional | Média | Ancorar a arquitetura em citações peer-reviewed (CoALA/V\*/GraphRAG); nunca brandar "cognitive computing"; zero claim de consciência; benchmark só com replicação independente |
> 442	| FM-VM-16 | **Memory — category error de persistência** | Aplicar decaimento FSRS/Ebbinghaus a **fatos semânticos** derivados de visão (em vez de deixá-los suplantar versões antigas) corrompe a malha — o category error de arXiv 2604.11364 | Média | Tipar nós de visão em dois regimes: **observações decaem** (`stability_score`/FSRS-6), **fatos suplantam** (supersession, sem decay) |
> 443	| FM-VM-17 | **Compliance — claim de conformidade falso** | Marketing "alt-text NBR 17225/WCAG 1.1.1-conformante" quando a saída não serve "propósito equivalente" → exposição regulatória sob EAA/LBI Art. 63 | Alta | Alinhar à letra normativa SC 1.1.1 ("equivalent purpose"); caminho de revisão humana antes de afirmar conformidade; não over-claim |
> 444	| FM-VM-18 | **Scope — overreach de língua de sinais** | Marketing "suporte a LIBRAS/sign language" via avatar/MT enfrenta linha vermelha WFD+WASLI (avatar/MT ≠ intérprete humano) | Média | Excluir do v1 OU escopar explicitamente como experimental; SignGemma é ASL→inglês em teste, não-GA |
> 445	
> 446	---
> 447	
> 448	## 8. OTDs e Questões Abertas
> 449	
> 450	> Toda lacuna crítica que a crítica levantou e **não** foi preenchida, mais itens `could_not_verify` que importam. Cada uma vira candidata a OTD com RPN/SLA no FMEA do BoK.
> 451	
> 452	- **OTD-VM-001 — Validação de domínio da saliência (Tier 1). ✅ FECHADA 2026-06-15 (gate research).** Corrigido: DeepGaze (free-viewing natural) **não transfere** para UI — mas datasets de UI-saliency **EXISTEM** (UEyes CHI 2023, 1.980 screenshots; Imp1k 1.000 designs) e o SOTA é **SUM** (WACV 2025, **MIT, self-hostável**), não DeepGaze. Gate selado: SUM treinado/avaliado em UEyes+Imp1k, métrica AUC-Judd/sAUC, **recall≥0.95** (assimetria: falso-negativo = cegueira permanente do Tier 2). Resta hipótese (could_not_verify): latência ARM64 do SUM + transferência zero-shot exata. Detalhe: SDD §8.2 OTD-VM-001 + FR-VM-010 + KPI-VM-008.
> 453	- **OTD-VM-002 — Demanda do produto cruzado (EMENDADA v0.2.0).** Nenhum competidor combina vision+deepsearch sobre MCP (whitespace), e **para esse produto cruzado a evidência de demanda permanece zero** — segue hipótese a validar. **O que a pesquisa de Tecnologia Assistiva (Seção 4-A) mudou:** ela **NÃO** valida o produto cruzado, mas valida fortemente uma **fatia adjacente** — a **descrição/alt-text visual por IA** — em três eixos independentes e multi-fonteados: (1) **uso** (Be My Eyes 1M usuários BLV + 43M requests/ano; Seeing AI/Lookout grátis; hardware US$399–US$4.250; humano US$26–US$1.160/mês); (2) **convergência de capability** (JAWS PictureSmart e NVDA já chamam OpenAI/Anthropic para a exata tool `describe_screen`); (3) **compulsão regulatória** (WCAG 2.2 SC 1.1.1 + EAA exigível 06/2025 + LBI Art. 63 + ABNT NBR 17225:2025 com ~99% dos sites BR não-conformes). **Mudança de hipótese:** o MRD deve **bifurcar** — a **descrição/alt-text assistiva é um beachhead demand-provado e regulatoriamente compelido** (entrada de mercado de menor risco), enquanto o **grounding vision+deepsearch consolidado** continua sendo a aposta de diferenciação **não-validada**. Recomendação: ancorar o GTM no vertical assistivo e tratar o cruzado como upsell a provar.
> 454	- **OTD-VM-003 — Long-running jobs sobre MCP para clients externos.** `tasks` é **experimental** em 2025-11-25; o Claude API connector consome só tools (sem tasks/elicitation/resources); **zero exemplos coletados** de como servidores remotos de produção entregam jobs de minutos (submit→job_id+poll, resource_link, SSE keep-alive, webhooks). Falta **matriz de capabilities por host** (Claude Desktop/Code, VS Code, ChatGPT, Claude API).
> 455	- **OTD-VM-004 — Unit economics medido.** A calibração da Seção 6 é inicial; faltam: custo de inferência GPU por-tool medido (RTMPose/RF-DETR throughput não verificado independentemente); semântica de partial-delivery refund; tokenização exata de imagem GPT-5.x (estimada). SOP exige medição material antes do fix.
> 456	- **OTD-VM-005 — DPAs/SCCs dos providers.** Opções zero-retention/no-training e prontidão de SCC ANPD dos DPAs de OpenAI/Google/OpenRouter para **inputs de imagem** não foram pesquisadas — auditar antes de o SDD nomear provider default.
> 457	- **OTD-VM-006 — Licenças não-fetchadas que importam.** ⚠️ Texto da "SAM License" para distribuição comercial (field-of-use); termos exatos do gate HF de `facebook/sam3`/`dinov3`; ToS de leaderboards de benchmark quanto a redistribuição. Fetch dos LICENSE antes da tabela de dependências do SDD.
> 458	- **OTD-VM-007 — Regulação biométrica ANPD 2026.** A tomada de subsídios fechou 02/07/2025; ANPD espera concluir regras em 2026; **nenhuma regra final publicada** verificada. Contribuições convergem: uso de biométrico para treinar IA exige consentimento específico + regras claras de deleção. Tratar o capítulo biométrico como alvo móvel com item de watch.
> 459	- **OTD-VM-008 — Pose/gait sem identificação.** ANPD lista "modo de andar" como biométrico, mas **não há orientação** sobre se análise de movimento **não-identificadora** (ex: qualidade ergonômica) escapa do art. 11. Risco legal aberto pendente da regulação 2026.
> 460	- **OTD-VM-009 — Notion/Medium ToS.** Cláusula exata de scraping da Notion não-fetchável (JS-rendered); a frase histórica de crawling da Medium **não confirmada** no texto vivo atual. Pinar wording na hora da implementação; não citar fontes scrapeadas via quotes secundários.
> 461	- **OTD-VM-010 — Pin OpenCV & ARM64.** Decisão explícita 4.x-vs-5.0 (licença 5.0 não re-verificada); **faltam benchmarks aarch64** (ONNX/ncnn ARM) para o tier periférico no host Oracle ARM64 — todos os números CPU coletados são x86.
> 462	- **OTD-VM-011 — Gemini 3.x segmentação.** A limitação "sem segmentation em Gemini 3 Pro/Flash" vem de snippet (a página apenas omite). Re-fetch antes de fixar a matriz de modelos.
> 463	- **OTD-VM-012 — Sim-to-real screen-domain.** O argumento "gap se dissolve para SaaS de tela" é raciocínio, não evidência. Marcar como hipótese no SDD.
> 464	- **OTD-VM-013 — Nginx vhost + Cloudflare SSE.** Criação de vhost exige root (sites-enabled root-only) + DNS Cloudflare; SSE por trás do Cloudflare precisa de buffering off + heartbeat (limite idle ~100s do free-tier em conexões longas de deepsearch).
> 465	- **OTD-VM-014 — Sentinel L3 single-replica.** Token bucket per-process (`sentinel.ts:48-50`) nunca reseta no container long-lived (bom) mas é estado single-replica; scaling horizontal futuro precisa de rate limiter compartilhado antes de réplicas.
> 466	- **OTD-VM-015 — Modelo atual por trás do Be My AI.** O Be My AI **lançou** sobre GPT-4 (2023), mas nem a página de marco (03/2026) nem o update Winter '25 **nomeiam o modelo atual** (`could_not_verify`). Não assumir "GPT-4V" como atual; irrelevante para o nosso provider matrix (somos BYOK per-user), mas relevante para benchmarking competitivo no MRD.
> 467	- **OTD-VM-016 — Penalidades EAA / aplicação BR.** Os valores de multa do EAA **variam por Estado-membro** (citados €100k vs €3M) — exigem a lei de transposição nacional; não fixar número único. A alegação de multas brasileiras >R$1M em 2025 (EqualWeb) vem de **fonte comercial única** (`confidence baixa`) — verificar contra registros judiciais/MPF antes de citar no MRD/BRD como evidência de enforcement financeiro.
> 468	- **OTD-VM-017 — Active inference: replicação independente.** O resultado AXIOM "bate DreamerV3" tem **auditoria contratada pelo vendor** (Soothsayer) e **nenhuma replicação independente** encontrada; a condição financeira da VERSES é auto-reportada (`could_not_verify`). Tratar active inference como **research-grade** — citar `pymdp`/paper para a ideia (atenção gated por ganho de informação → metering mcoCoins), nunca a stack Verses como dependência.
> 469	- **OTD-VM-018 — Língua de sinais (escopo).** SignGemma é ASL→inglês, "esperado até fim de 2025", status GA **não-verificado** em 2026 (`could_not_verify`); WFD+WASLI vetam avatar/MT como substituto de intérprete. **Manter fora do v1**; se algum dia entrar, scope experimental explícito + revisão da comunidade Surda.
> 470	- **OTD-VM-019 — Mapeamento requisito-a-requisito da NBR 17225.** A norma é **confirmada real** (publicada 03/2025, ~150 requisitos, dois níveis), mas o **texto requisito-a-requisito não foi parseado** nesta sessão (só PDF-mirror/sumários). Antes de afirmar "alt-text NBR 17225-conformante" como claim de produto (FM-VM-17), mapear os requisitos de alternativa textual da norma contra a saída da tool `vision.alt_text`. Idem: números do estudo VideoA11y (AI ≈ humano treinado) vêm de guia de vendor — buscar o paper CHI primário antes de qualquer marketing de audio description.
> 471	
> 472	---
> 473	
> 474	## 9. Fatiamento MVP
> 475	
> 476	> 4 fatias, cada uma com gate de verificação material (Lei 1) e o que destrava.
> 477	
> 478	### Fatia 0 — BoK Gate + SOP (pré-código, bloqueante)
> 479	- **Entrega:** `/bok-scribe vision-mcp` → `docs/bok/vision-mcp/{01-mrd..05-sdd}.md`; SOP `docs/processes/vision-mcp-credential-resolution.md` (Operator/Sequence/Gates/Recovery/Success).
> 480	- **Gate material (Lei 1):** `ls -la docs/bok/vision-mcp/` mostra 5 docs com size byte-exato; `git log -1 --format=%H` do commit do seal.
> 481	- **Destrava:** permissão para escrever qualquer código de `vision-mcp` (Closed-Loop Protocol).
> 482	
> 483	### Fatia 1 — Esqueleto MCP autenticado, read-only, internal-only
> 484	- **Entrega:** container `mcorch_vision_mcp` (fork do skeleton gitnexus) com `StreamableHTTPServerTransport` em `127.0.0.1`, healthcheck node, hardening anchor; gate ES256 JWKS fail-closed; 1 tool read-only `mesh.search` (custo 0); telemetria `infra_health_logs service='vision-mcp'`.
> 485	- **Gate material:** `docker ps`/`docker inspect` do container healthy; `curl` interno retorna `200` no `/health` + **`401` fail-closed** sem token e **`200` com token user válido** (mint via `scripts/qa/gen-user-jwt.ts`); nó da malha inserido com UUID retornado por `SELECT`.
> 486	- **Destrava:** padrão de auth/transport provado para todas as tools subsequentes.
> 487	
> 488	### Fatia 2 — Tier 2 foveal billable + per-user creds + refund
> 489	- **Entrega:** `vision.describe_image` + `vision.ocr` + `deepsearch.scrape`; coluna `firecrawl_api_key` per-user + UI Settings; sentinel `inspectPrompt`; cobrança `deduct_mco_coins` + `refundMco`; `mesh.consolidate_reference` com PII-strip + provenance tag.
> 490	- **Gate material:** run pago E2E com `agent_executions` ledger + delta de `mco_balance` por `SELECT`; `402` em saldo insuficiente (body literal); `402 firecrawl_not_configured` sem credencial; refund material em falha forçada (saldo restaurado por `SELECT`); `/security-review` SAFE na migration da coluna.
> 491	- **Destrava:** o produto cruzado mínimo (vision + grounding) na malha, monetizado.
> 492	
> 493	### Fatia 3 — Exposição externa: PAT + OAuth + Plugin + jobs async
> 494	- **Entrega:** vhost `mcp.mcorch.com` (proxy loopback, SSE buffering off); RFC 9728 PRM + OAuth 2.1; tabela `mcp_access_tokens` (hash, scopes, RLS, `/security-review`); `deepsearch.run`/`poll` com job semantics + partial-delivery refund; Plugin Zip + skills PT-BR em `/dashboard/settings`; `erase_vision_artifacts()` RPC.
> 495	- **Gate material:** `curl -i POST initialize` externo retorna `401` + `WWW-Authenticate resource_metadata`; conexão real de Claude Desktop/Code via OAuth (screenshot/log); `deepsearch.run` retorna `job_id` e `poll` entrega resultado >150s depois; `erase_vision_artifacts` apaga nó+edges+embedding+frames (contagem por `SELECT` antes/depois); E2E UI audit 1920×1080 se houver UI nova.
> 496	- **Destrava:** ecossistemas externos (a meta da Diretiva Sovereign) + soberania de apagamento LGPD.
> 497	
> 498	---
> 499	
> 500	## 10. Apontadores para o BoK
> 501	
> 502	> O que `/bok-scribe vision-mcp` deve transformar em MRD/BRD/PRD/FRD/SDD. Hints de traceabilidade `BR-VM-xxx` / `FR-VM-xxx`.
> 503	
> 504	### MRD (01) — Market Requirements
> 505	- Categoria: content/perception-intelligence MCP; comps diretos **Roboflow MCP** (vision), **Exa/Firecrawl/Tavily MCP** (deepsearch) — posicionar contra eles, **não** reivindicar "vision sobre MCP" ou "deepsearch sobre MCP" como diferencial (ambos perdidos).
> 506	- Diferenciais defensáveis: (i) produto cruzado vision+deepsearch (whitespace, **hipótese a validar** — OTD-VM-002), (ii) self-host soberano vs Roboflow hosted-only, (iii) credencial per-tenant + mcoCoins atômico, (iv) filosofia Essência Humana, (v) **percepção como órgão de uma arquitetura cognitiva (CoALA)** já montada (malha GraphRAG + pgvector + FSRS + Pantheon) — Pilar V / Seção 3.
> 507	- **Vertical Tecnologia Assistiva (beachhead demand-provado — Seção 4-A + OTD-VM-002 emendada):** alt-text/descrição visual por IA para usuários BLV e para **conformidade WCAG 2.2 / EAA / LBI Art. 63 / ABNT NBR 17225:2025**. Comps deste vertical: **Be My Eyes / Be My AI** (1M usuários, modelo B2B-funded), **Microsoft Seeing AI**, **Google Lookout**, **Aira** (híbrido IA-grátis + humano-pago), **JAWS PictureSmart AI**, **NVDA AI Content Describer**. Demanda multi-fonteada (uso + convergência de capability + compulsão regulatória); o cruzado vision+deepsearch permanece upsell a validar.
> 508	- Modelos de monetização observados: BYOK credit-metered (Roboflow/Exa/Firecrawl/Tavily) e x402 micropagamento — mcoCoins mapeia no primeiro. No vertical assistivo: free-ao-usuário-financiado-por-B2B (Be My Eyes) e híbrido IA-grátis/humano-pago (Aira) são templates observados.
> 509	
> 510	### BRD (02) — Business Requirements (`BR-VM-001..0xx`)
> 511	- BR-VM-001 Atribuição de receita correta por tenant (API Tenancy). BR-VM-002 Segregação de quota/rate-limit per-user. BR-VM-003 Billing mcoCoins atômico com refund-on-failure. BR-VM-004 Conformidade LGPD (biométrico art. 11, transferência internacional, erasure). BR-VM-005 Soberania de dados (scraped nunca em system nodes). BR-VM-006 Risk Ledger (PAT leak, AGPL, prompt-injection persistente, hiQ-style corpus deletion). BR-VM-007 Distribuição self-serve (Plugin + skills). **BR-VM-008 Dever de cuidado assistivo + conformidade de acessibilidade** (recusas categóricas medicação/alérgeno/mobilidade/emergência, sinalização de confiança, escalonamento humano — FM-VM-14/17; alinhamento WCAG 2.2 SC 1.1.1 / EAA / LBI Art. 63 / NBR 17225). **BR-VM-009 Anti-hype/positioning** — proibição de brandar "cognitive computing"/consciência/"cérebro digital" sem benchmark independente (FM-VM-15).
> 512	
> 513	### PRD (03) — Product Requirements
> 514	- Empty-state/onboarding de credenciais (firecrawl/openrouter/gemini/mistral BYOK). Página Connectors em `/dashboard/settings` (API-key + URL MCP + Plugin Zip + instruções PT-BR). UX de tools workflow-named (não CRUD cru — lição Roboflow/sandcastles). Permission guidance por-tool.
> 515	
> 516	### FRD (04) — Functional Requirements (`FR-VM-001..0xx`)
> 517	- FR-VM-001 Transporte Streamable HTTP 2025-11-25 (Origin 403, MCP-Protocol-Version). FR-VM-002 Auth ES256 JWKS fail-closed + RFC 9728 PRM + OAuth 2.1. FR-VM-003 `mcp_access_tokens` (hash/scopes/RLS). FR-VM-004 Resolução de credencial per-user fail-closed (402 estruturado). FR-VM-005 Sentinel inbound + sobre texto extraído. FR-VM-006 Tools (Seção 6) com classes mcoCoin. FR-VM-007 Job semantics async + partial-delivery refund. FR-VM-008 Mesh Connection Mandate (observation node + content_mesh_asset + embed). FR-VM-009 `erase_vision_artifacts()` + retention clock. FR-VM-010 Tier-1 peripheral gate (alvo de recall — OTD-VM-001). FR-VM-011 Plugin Zip + skills distribution.
> 518	- **FR-VM-012 `vision.alt_text`** — alt-text WCAG 2.2 SC 1.1.1 / NBR 17225-conformante (curto + longo) + detecção de imagem decorativa; saída serve "propósito equivalente"; caminho de revisão humana antes de afirmar conformidade (FM-VM-17). **FR-VM-013 `vision.describe_screen`** — descrição de screenshot/UI (padrão JAWS/NVDA) com sinalização de incerteza. **FR-VM-014 Camada de dever de cuidado assistivo** — recusas categóricas (medicação/dosagem/alérgeno/mobilidade/emergência, template ToS Be My Eyes), confidence/hedge em baixa certeza (ASSETS 2024), gancho de escalonamento a verificação humana (híbrido Aira); aplicável a `vision.alt_text`/`describe_screen`/`describe_image`/`ocr`/`analyze_video` em uso assistivo (FM-VM-14). **FR-VM-015 Regime de persistência de memória** — tipar nós originados de visão: observações decaem (FSRS-6/`stability_score`), fatos suplantam (supersession, sem decay) — anti-category-error arXiv 2604.11364 (FM-VM-16).
> 519	
> 520	### SDD (05) — Software Design
> 521	- Runtime: container Sovereign Mesh (Seção 5.1), decisão pin OpenCV 4.x-vs-5.0 + benchmarks ARM64. Matriz de modelos (pista Apache default: SAM 2/RF-DETR/Qwen3-VL/OpenEB; SAM 3/DINOv3 só com propagação de licença documentada). Tabela de dependências com LICENSE fetchados (OTD-VM-006). Pipeline Essência Humana (Tier 1 emulação neuromórfica → trigger → Tier 2). Esquema `mcp_access_tokens`, `erase_vision_artifacts`, coluna `firecrawl_api_key`. Estratégia de version-pinning MCP + deprecation-watch (RC 2026-07-28 existe; registry em preview).
> 522	- **Loop cognitivo (CoALA — Pilar V / Seção 3):** especificar a percepção como **órgão de uma arquitetura cognitiva** — mapear working memory = janela de contexto, episódica = nós `observation`, semântica/long-term = grafo `mcorch_edges` + pgvector, procedural = skills/SOPs; broadcast GWT (metáfora, sem consciência); active inference → metering (disparar fóvea só quando o ganho de informação esperado justifica o custo mcoCoins). **Regime de persistência (FR-VM-015):** observações decaem, fatos suplantam (arXiv 2604.11364). Âncoras de design citáveis: CoALA (TMLR), V\*/SEAL (CVPR), GraphRAG; **proibido** ancorar no rótulo "cognitive computing".
> 523	- **Provider matrix assistivo (FR-VM-012/013/014):** precedente dual-backend OpenAI + Anthropic (JAWS PictureSmart) e provider-agnóstico (NVDA Content Describer) — casa com o BYOK per-user do MCORCH; especificar gate de dever de cuidado (recusas categóricas + confidence + escalonamento humano) e mapeamento requisito-a-requisito da NBR 17225 antes de claim de conformidade (OTD-VM-019).
> 524	- **FMEA (seed Seção 7 + OTDs Seção 8):** calcular RPN para FM-VM-01..18 (inclui os novos FM-VM-14 dever-de-cuidado assistivo, FM-VM-15 cognitive/agent-washing, FM-VM-16 category-error de persistência, FM-VM-17 claim-de-conformidade falso, FM-VM-18 overreach de língua de sinais); promover OTD-VM-001..019 com SLA.
> 525	
> 526	### Data Model / Process Flow / Quality Metrics
> 527	- Data model: `mcorch_nodes`/`mcorch_edges` (user+project), `mcp_access_tokens`, coluna `user_api_keys.firecrawl_api_key`, retention metadata em reference nodes.
> 528	- Process flow: o loop de dois níveis + grounding + consolidação na malha (Seção 3).
> 529	- Quality metrics (CMQ/OE): recall do gate periférico, margem mcoCoin por-tool ≥1× floor, taxa de refund, fail-closed coverage do auth, zero scraped-em-system-nodes.
> 530	
> 531	---
> 532	
> 533	> **"MATE A POESIA. ENTREGUE ENGENHARIA."** — Selo do seed `vision-mcp` · próximo passo: `/bok-scribe vision-mcp` para sedimentar a Fonte da Verdade em MRD→BRD→PRD→FRD→SDD.
> ```

## 🤖 Claude *(18:50:01)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/deepsearch-blueprint.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# SOP — Deepsearch Blueprint (semente de BoK fundamentada em pesquisa)
> 2	
> 3	> **Lei 2 (Processo Antecipado).** Este SOP documenta o processo que já rodou manualmente 2×
> 4	> com sucesso antes de virar skill/agent: `docs/bok/security/00-deepsearch-blueprint.md`
> 5	> (Cyber-Sentinel, 2026-06-09) e `docs/bok/vision-mcp/00-deepsearch-blueprint.md`
> 6	> (Vision MCP v0.1.0→v0.2.0, 2026-06-10/11).
> 7	>
> 8	> **Quando usar:** o Sovereign emite uma diretiva de **módulo novo** ancorada em referência
> 9	> externa desconhecida ("a referência é <produto/URL>") ou em temas que exigem fundamento de
> 10	> mercado. O Closed-Loop Protocol exige BoK antes de código — e o blueprint é a **semente
> 11	> verificada** que alimenta o `/bok-scribe` sem improviso.
> 12	
> 13	---
> 14	
> 15	## Operator
> 16	
> 17	Hoje: **MCORCH Master Execution Agent** (main loop com a tool `Workflow`), sob GO do Sovereign.
> 18	Reviewer: Sovereign (revisa o blueprint antes do `/bok-scribe`). Owner: Sovereign.
> 19	Forma delegável: subagent `.claude/agents/deepsearch-blueprint.md` (sem `Workflow` — executa as
> 20	frentes sequencialmente com WebSearch/WebFetch).
> 21	
> 22	## Sequence
> 23	
> 24	1. **ORO + gate declarado.** Declarar o triplet e afirmar explicitamente: "nenhum código antes
> 25	   da BoK" (FM de processo). Critério: o ORO aparece na resposta antes de qualquer tool call.
> 26	2. **Workflow de pesquisa (ultracode).** Estrutura provada:
> 27	   - **N frentes web** (4-6) em `pipeline()`: cada uma com prompt de domínio + regras duras de
> 28	     materialidade (toda claim com URL consultada; sem fonte → `could_not_verify`; NUNCA
> 29	     fabricar nome/versão/número).
> 30	   - **Verify adversarial por frente** (2º estágio do pipeline): fact-checker independente
> 31	     tenta REFUTAR as top ~6 claims com fontes que não sejam a original
> 32	     (`confirmed`/`refuted`/`unverifiable`).
> 33	   - **Mapeamento do repo em paralelo** (read-only): como o módulo integra ao MCORCH
> 34	     (runtime/auth/billing/mesh + assets a reusar), com referências `path:line` concretas.
> 35	   - **Completeness critic** (barreira): o que falta para uma BoK honesta? → `critical_gaps`
> 36	     (≤6, cada um com `suggested_search`).
> 37	   - **Gap-fill** (≤4 em paralelo) → gaps não preenchidos viram OTDs, nunca silêncio.
> 38	   - **Síntese**: documento completo PT-BR (termos técnicos em inglês), 10 seções no precedente
> 39	     (Sumário honesto · Pilares com veredictos · Arquitetura unificadora · Catálogo de
> 40	     referências com URL · Arquitetura MCORCH-nativa · Superfície proposta · FMEA-seed ·
> 41	     OTDs · Fatiamento MVP com gates Lei 1 · Apontadores para o BoK).
> 42	3. **Escrita em main loop.** O markdown retorna pelo workflow; o main loop grava
> 43	   `docs/bok/<slug>/00-deepsearch-blueprint.md` (controle de qualidade fica fora do subagente).
> 44	4. **Emendas (v0.x+1)** — quando o Sovereign acrescenta temas: pesquisa só das frentes novas +
> 45	   merge agent que **lê o arquivo atual e devolve o documento COMPLETO como superset**.
> 46	   Nunca aplicar "patches cegos".
> 47	
> 48	## Verification gates (cada step)
> 49	
> 50	| Gate | Comando/critério | Esperado |
> 51	|---|---|---|
> 52	| G1 claims verificadas | stats do workflow | `refuted` tratadas (corrigidas/excluídas); 0 claims refutadas no doc final |
> 53	| G2 artefato em disco | `ls -la` + `wc -l` + `md5sum` do arquivo | tamanho/linhas citados literais |
> 54	| G3 escapes | `grep -c '&gt;\|&lt;\|&amp;'` no markdown extraído | 0 (artefato de notificação ≠ arquivo) |
> 55	| G4 superset (emendas) | script python: headers v_old ⊆ v_new (renames intencionais à parte) · 0 OTD/FM IDs perdidos · 0 URLs perdidas · bytes crescem | tudo zero-perda |
> 56	| G5 gaps honestos | grep dos `critical_gaps` não preenchidos | todos presentes na seção OTDs |
> 57	
> 58	## Recovery path
> 59	
> 60	- **Session-limit mata o workflow** (sintoma: `failures: [...] session limit · resets HH:MM`):
> 61	  NÃO recomece. `Workflow({scriptPath, resumeFromRunId})` — agentes completos voltam do journal
> 62	  em cache; só os mortos re-rodam. Provado 2× (2026-06-10 23:58 e 2026-06-11 09:57). Genérico
> 63	  para QUALQUER workflow, não só este.
> 64	- **Merge agent morreu no meio de edição no arquivo:** SEMPRE faça `cp` + `md5sum` de backup
> 65	  ANTES de lançar merge (arquivo não commitado = sem rede git). Ao retomar: `diff` arquivo vs
> 66	  backup; se houver edição parcial (ex.: só bump de header), **restaurar o backup limpo** antes
> 67	  do resume — o merge agent precisa ler estado honesto.
> 68	- **Frente de pesquisa retorna vazio/baixa confiança:** registrar como finding honesto
> 69	  ("could not establish") — nunca fabricar perfil do produto-referência.
> 70	
> 71	## Success signal
> 72	
> 73	`docs/bok/<slug>/00-deepsearch-blueprint.md` em disco com md5/linhas citados + gates G1-G5
> 74	verdes + resumo ao Sovereign com os vereditos que mudam decisão (ex.: bifurcação de demanda)
> 75	+ oferta explícita do próximo passo: `/bok-scribe <slug>`.
> 76	
> 77	---
> 78	
> 79	_Anticorpo do padrão repetido 2× (Obstacle→Synthesis Mandate). Skill: `.claude/skills/deepsearch-blueprint/SKILL.md` · Agent: `.claude/agents/deepsearch-blueprint.md`._
> 80	
> ```

## 🤖 Claude *(18:50:08)*

I now have all four BoK docs fully read plus the deepsearch-blueprint SOP. I have a critical finding to verify: the blueprint and FRD describe `deepsearch.run` as a job of "N searches + scrapes" via Firecrawl — but the task framing asks whether it's the "google/gemini grounded research half." Let me cross-check what provider the BoK actually pins, and whether `gemini_api_key` is confirmed as a `user_api_keys` column, by checking the SDD (05) if it exists, plus the actual schema reference for the user_api_keys columns.

## 🤖 Claude *(18:50:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la /home/gcrUX/htdocs/constellation-orchestra/docs/bok/vision-mcp/ 2>/dev/null; echo \"---SDD CHECK---\"; test -f /home/gcrUX/htdocs/constellation-orchestra/docs/bok/vision-mcp/05-sdd.md && echo \"SDD EXISTS\" || echo \"NO 05-sdd.md\"",
  "description": "List vision-mcp BoK files and check for SDD"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 436
> drwxrwxr-x  2 ubuntu ubuntu  4096 Jun 15 13:52 .
> drwxrwxr-x 22 ubuntu ubuntu  4096 Jun 11 00:36 ..
> -rw-rw-r--  1 ubuntu ubuntu 98802 Jun 15 12:42 00-deepsearch-blueprint.md
> -rw-rw-r--  1 ubuntu ubuntu  7690 Jun 15 10:20 00-index.md
> -rw-rw-r--  1 ubuntu ubuntu 33673 Jun 15 10:17 01-mrd.md
> -rw-rw-r--  1 ubuntu ubuntu 34554 Jun 15 10:17 02-brd.md
> -rw-rw-r--  1 ubuntu ubuntu 38286 Jun 11 11:45 03-prd.md
> -rw-rw-r--  1 ubuntu ubuntu 37579 Jun 15 13:52 04-frd.md
> -rw-rw-r--  1 ubuntu ubuntu 77910 Jun 15 12:58 05-sdd.md
> -rw-rw-r--  1 ubuntu ubuntu 16089 Jun 15 10:05 06-data-model.md
> -rw-rw-r--  1 ubuntu ubuntu 16899 Jun 15 09:35 07-process-flow.md
> -rw-rw-r--  1 ubuntu ubuntu 16188 Jun 15 12:41 08-quality-metrics.md
> -rw-rw-r--  1 ubuntu ubuntu 35968 Jun 15 09:42 09-agent-system.md
> ---SDD CHECK---
> SDD EXISTS
> ```

## 🤖 Claude *(18:50:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -rn \"gemini_api_key\\|firecrawl_api_key\\|openrouter_api_key\" supabase/migrations/ 2>/dev/null | head -40",
  "description": "Find user_api_keys credential columns in migrations"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> supabase/migrations/20260601000000_credential_encryption.sql:109:  -- openrouter_api_key
> supabase/migrations/20260601000000_credential_encryption.sql:110:  IF NEW.openrouter_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openrouter_api_key IS DISTINCT FROM OLD.openrouter_api_key) THEN
> supabase/migrations/20260601000000_credential_encryption.sql:111:    IF NEW.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> supabase/migrations/20260601000000_credential_encryption.sql:114:      v_id := vault.create_secret(NEW.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || NEW.user_id::text, 'OpenRouter API Key');
> supabase/migrations/20260601000000_credential_encryption.sql:115:      NEW.openrouter_api_key = v_id::text;
> supabase/migrations/20260601000000_credential_encryption.sql:294:    IF r.openrouter_api_key IS NOT NULL AND r.openrouter_api_key !~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> supabase/migrations/20260601000000_credential_encryption.sql:295:      v_or := vault.create_secret(r.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || r.user_id::text, 'OpenRouter API Key');
> supabase/migrations/20260601000000_credential_encryption.sql:329:        openrouter_api_key = COALESCE(v_or::text, openrouter_api_key),
> supabase/migrations/20260601000000_credential_encryption.sql:399:  CASE WHEN openrouter_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS openrouter_api_key,
> supabase/migrations/20260601000000_credential_encryption.sql:504:      user_id, groq_api_key, openrouter_api_key, openai_api_key, pref_audio_provider, pref_image_provider, pref_video_provider, elevenlabs_api_key, google_api_key, nanobana_api_key, seedance_api_key, wp_site_url, wp_username, wp_app_password, pref_ai_model, replicate_api_key, higgsfield_api_key, higgsfield_api_key_secret
> supabase/migrations/20260601000000_credential_encryption.sql:506:      NEW.user_id, NEW.groq_api_key, NEW.openrouter_api_key, NEW.openai_api_key, NEW.pref_audio_provider, NEW.pref_image_provider, NEW.pref_video_provider, NEW.elevenlabs_api_key, NEW.google_api_key, NEW.nanobana_api_key, NEW.seedance_api_key, NEW.wp_site_url, NEW.wp_username, NEW.wp_app_password, NEW.pref_ai_model, NEW.replicate_api_key, NEW.higgsfield_api_key, NEW.higgsfield_api_key_secret
> supabase/migrations/20260601000000_credential_encryption.sql:510:      openrouter_api_key = COALESCE(NULLIF(NEW.openrouter_api_key, '••••••••••••'), public.user_api_keys_table.openrouter_api_key),
> supabase/migrations/20260601000000_credential_encryption.sql:588:  COALESCE(s_openrouter.decrypted_secret, uak.openrouter_api_key) AS openrouter_api_key,
> supabase/migrations/20260601000000_credential_encryption.sql:608:LEFT JOIN vault.decrypted_secrets s_openrouter ON uak.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_openrouter.id = uak.openrouter_api_key::uuid
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:121:  -- openrouter_api_key
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:122:  IF NEW.openrouter_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openrouter_api_key IS DISTINCT FROM OLD.openrouter_api_key) THEN
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:123:    IF NEW.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:126:      v_id := public.vault_upsert_secret(NEW.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || NEW.user_id::text, 'OpenRouter API Key');
> supabase/migrations/20260602140000_vault_upsert_secret_idempotent_encrypt.sql:127:      NEW.openrouter_api_key = v_id::text;
> supabase/migrations/20260601060000_user_api_keys_apify_token.sql:34:  -- openrouter_api_key
> supabase/migrations/20260601060000_user_api_keys_apify_token.sql:35:  IF NEW.openrouter_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openrouter_api_key IS DISTINCT FROM OLD.openrouter_api_key) THEN
> supabase/migrations/20260601060000_user_api_keys_apify_token.sql:36:    IF NEW.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN
> supabase/migrations/20260601060000_user_api_keys_apify_token.sql:38:      v_id := vault.create_secret(NEW.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || NEW.user_id::text, 'OpenRouter API Key');
> supabase/migrations/20260601060000_user_api_keys_apify_token.sql:39:      NEW.openrouter_api_key = v_id::text;
> supabase/migrations/20260601060000_user_api_keys_apify_token.sql:158:  CASE WHEN openrouter_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS openrouter_api_key,
> supabase/migrations/20260601060000_user_api_keys_apify_token.sql:186:      user_id, groq_api_key, openrouter_api_key, openai_api_key, pref_audio_provider, pref_image_provider, pref_video_provider, elevenlabs_api_key, google_api_key, nanobana_api_key, seedance_api_key, wp_site_url, wp_username, wp_app_password, pref_ai_model, replicate_api_key, higgsfield_api_key, higgsfield_api_key_secret, apify_token
> supabase/migrations/20260601060000_user_api_keys_apify_token.sql:188:      NEW.user_id, NEW.groq_api_key, NEW.openrouter_api_key, NEW.openai_api_key, NEW.pref_audio_provider, NEW.pref_image_provider, NEW.pref_video_provider, NEW.elevenlabs_api_key, NEW.google_api_key, NEW.nanobana_api_key, NEW.seedance_api_key, NEW.wp_site_url, NEW.wp_username, NEW.wp_app_password, NEW.pref_ai_model, NEW.replicate_api_key, NEW.higgsfield_api_key, NEW.higgsfield_api_key_secret, NEW.apify_token
> supabase/migrations/20260601060000_user_api_keys_apify_token.sql:192:      openrouter_api_key = COALESCE(NULLIF(NEW.openrouter_api_key, '••••••••••••'), public.user_api_keys_table.openrouter_api_key),
> supabase/migrations/20260601060000_user_api_keys_apify_token.sql:223:  COALESCE(s_openrouter.decrypted_secret, uak.openrouter_api_key) AS openrouter_api_key,
> supabase/migrations/20260601060000_user_api_keys_apify_token.sql:244:LEFT JOIN vault.decrypted_secrets s_openrouter ON uak.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' AND s_openrouter.id = uak.openrouter_api_key::uuid
> supabase/migrations/20260421000000_create_user_api_keys.sql:4:    openrouter_api_key TEXT,
> supabase/migrations/20260602130000_fix_user_api_keys_instead_of_double_fire.sql:53:      openrouter_api_key        = COALESCE(NULLIF(NEW.openrouter_api_key, '••••••••••••'), public.user_api_keys_table.openrouter_api_key),
> supabase/migrations/20260602130000_fix_user_api_keys_instead_of_double_fire.sql:76:        user_id, groq_api_key, openrouter_api_key, openai_api_key, pref_audio_provider, pref_image_provider, pref_video_provider, elevenlabs_api_key, google_api_key, nanobana_api_key, seedance_api_key, wp_site_url, wp_username, wp_app_password, pref_ai_model, replicate_api_key, higgsfield_api_key, higgsfield_api_key_secret, apify_token
> supabase/migrations/20260602130000_fix_user_api_keys_instead_of_double_fire.sql:78:        NEW.user_id, NEW.groq_api_key, NEW.openrouter_api_key, NEW.openai_api_key, NEW.pref_audio_provider, NEW.pref_image_provider, NEW.pref_video_provider, NEW.elevenlabs_api_key, NEW.google_api_key, NEW.nanobana_api_key, NEW.seedance_api_key, NEW.wp_site_url, NEW.wp_username, NEW.wp_app_password, NEW.pref_ai_model, NEW.replicate_api_key, NEW.higgsfield_api_key, NEW.higgsfield_api_key_secret, NEW.apify_token
> supabase/migrations/20260601000600_secure_definer_views.sql:59:  CASE WHEN openrouter_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS openrouter_api_key,
> supabase/migrations/20260603240000_user_api_keys_resend_channel.sql:34:  IF NEW.openrouter_api_key IS NOT NULL AND (TG_OP = 'INSERT' OR NEW.openrouter_api_key IS DISTINCT FROM OLD.openrouter_api_key) THEN
> supabase/migrations/20260603240000_user_api_keys_resend_channel.sql:35:    IF NEW.openrouter_api_key ~ '^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$' THEN ELSE
> supabase/migrations/20260603240000_user_api_keys_resend_channel.sql:36:      v_id := public.vault_upsert_secret(NEW.openrouter_api_key, 'user_api_keys_openrouter_api_key_' || NEW.user_id::text, 'OpenRouter API Key'); NEW.openrouter_api_key = v_id::text;
> supabase/migrations/20260603240000_user_api_keys_resend_channel.sql:105:  CASE WHEN openrouter_api_key IS NOT NULL THEN '••••••••••••' ELSE NULL END AS openrouter_api_key,
> supabase/migrations/20260603240000_user_api_keys_resend_channel.sql:138:      openrouter_api_key        = COALESCE(NULLIF(NEW.openrouter_api_key, '••••••••••••'), public.user_api_keys_table.openrouter_api_key),
> ```

## 🤖 Claude *(18:50:20)*

The SDD (05) exists — it's the authoritative design layer and will pin the provider for `deepsearch.run`. The critical question (Firecrawl vs Gemini/Google grounding) must be answered there. Let me check the SDD and the actual `user_api_keys` table columns to confirm whether `gemini_api_key` exists.

## 🤖 Claude *(18:50:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"deepsearch.run\\|deepsearch\\.run\\|planned_units\\|gemini_api_key\\|google_api_key\\|Google Search\\|grounding\\|Gemini grounding\\|CSE\\|google CSE\\|Firecrawl\\|firecrawl\\|/v1/search\\|deep.research\\|/search\\b\\|partial_units\\|delivered_units\\|unit\" /home/gcrUX/htdocs/constellation-orchestra/docs/bok/vision-mcp/05-sdd.md | head -80",
  "description": "Search SDD for deepsearch.run provider, units, gemini key"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 27:│  useUserApiKeys (+firecrawl/mistral) · useMcpTokens · useVisionMcp ·        │
> 61:│  SUPABASE (reuso — zero      │  │  Firecrawl (deepsearch, BYOK) ·            │
> 113:│ DEEPSEARCH GROUNDING — Firecrawl BYOK per-user (fail-closed)  │
> 154:| Credentials | `auth/credentials.ts` | Resolução per-user fail-closed via `decrypted_user_api_keys` (firecrawl/openrouter/google/mistral/openai); 402 `<service>_not_configured` | FR-VM-004 |
> 162:| Deepsearch | `tools/deepsearch/` | `deepsearch.scrape` (robots/login-wall/allowlist) + `deepsearch.run`/`poll` (máquina de estados em `vision_jobs`) | FR-VM-020, FR-VM-007 |
> 206:| `useUserApiKeys` (extensão) | `useUserApiKeys.ts` | + `firecrawl_api_key`, `mistral_api_key` — write `.insert` (NUNCA `.upsert` — VIEW Vault), null não limpa (clear via RPC), teste server-side | `['user-api-keys', userId]` (existente) |
> 231:| `user_api_keys.firecrawl_api_key` / `.mistral_api_key` | Columns (VIEW family) | BYOK deepsearch + OCR direto (padrão Vault da `20260601060000`) | `<ts>_user_api_keys_vision_byok.sql` |
> 281:### 3.3 Deepsearch async job + partial refund (`deepsearch.run`/`poll` — FR-VM-007)
> 284:Client                  mcorch_vision_mcp                       Supabase / Firecrawl
> 285: │──deepsearch.run──────▶│ identity → sentinel                     │
> 286: │  {query,planned_units}│──deduct_mco_coins(sub, 3, 'deepsearch.run')▶│ (402 → job não nasce)
> 289: │   (submit p95 <2s)    │──scrape×N (robots/allowlist/login-wall)─▶│ Firecrawl BYOK
> 299: │◀─{state,delivered_units,partial,failed_units[],refunded_mco,result}
> 365:| `deepsearch.scrape` | 1 | `deepsearch:run` | robots.txt + login-wall block + allowlist + CDSM Art.4 |
> 366:| `deepsearch.run` | 3 | `deepsearch:run` | job async; débito integral na entrada |
> 367:| `deepsearch.poll` | 0 | `deepsearch:run` | tenant-bound (`job_id` alheio → 404) |
> 372:**Vocabulário de scopes (fechado):** `vision:read`, `deepsearch:run`, `mesh:read`, `mesh:write`. **NUNCA** existem scopes `credentials:*`/`billing:*` (FM-VM-06 — vazamento de PAT não pode alcançar gestão de credencial nem carteira além do consumo de tools).
> 415:#### `deepsearch.run` / `deepsearch.poll` (FR-VM-007 · 3 / 0 mco)
> 418:interface DeepsearchRunInput  { query: string; planned_units?: number; source_allowlist?: string[] }
> 419:interface DeepsearchRunOutput { job_id: string; state: 'queued'; planned_units: number; charged_mco: number }
> 424:  delivered_units: number; planned_units: number
> 425:  partial: boolean; failed_units?: string[]; refunded_mco?: number
> 428:// Débito integral (3) na entrada — 402 → job não nasce. planned_units ≤ cap do plano (DD-VM-003).
> 504:| Credentials (`auth/credentials.ts`) | FM-VM-05 | `FIRECRAWL_API_KEY` compartilhada em fluxo user-facing → exaustão de quota + blast radius financeiro cross-tenant | DoS / Repudiation | Alta | Coluna `firecrawl_api_key` per-user + UI + 402 `firecrawl_not_configured` fail-closed; zero env-key global em path user-facing (grep material no gate de teste) |
> 591:| `user_api_keys.firecrawl_api_key` (per-user) | `deepsearch.*` | Vault via `decrypted_user_api_keys` (service-role only view) | Primário; ausente → 402 `firecrawl_not_configured` |
> 592:| `user_api_keys.openrouter_api_key` / `google_api_key` / `openai_api_key` (per-user) | `vision.*` VLM legs | idem | Primário (BYOK → metering custo 0) |
> 644:    scopes <@ ARRAY['vision:read','deepsearch:run','mesh:read','mesh:write']
> 662:  ADD COLUMN IF NOT EXISTS firecrawl_api_key text,
> 664:COMMENT ON COLUMN public.user_api_keys_table.firecrawl_api_key
> 665:  IS 'Per-user Firecrawl key (BYOK) for vision-mcp deepsearch. Vault-encrypted. Ausente = 402 firecrawl_not_configured (fail-closed — sem fallback global user-facing).';
> 678:  tool            text NOT NULL,                                -- 'deepsearch.run'
> 681:  planned_units   int NOT NULL DEFAULT 1 CHECK (planned_units >= 1),  -- cap por plano: app-side (DD-VM-003)
> 682:  delivered_units int NOT NULL DEFAULT 0,
> 686:  failed_units    jsonb,
> 755:| DD-VM-003 | Cap de `planned_units` por plano | Starter 10 · Pro 25 · Enterprise 50 (provisório — recalibra com OTD-VM-004) | Proporcional aos saldos 500/2000/10000 mco; enforced app-side no aceite do job |
> ```

## 🤖 Claude *(18:50:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n \"gemini_api_key\\|google_api_key\\|^    [a-z_]*_api_key\\|TEXT,\" /home/gcrUX/htdocs/constellation-orchestra/supabase/migrations/20260421000000_create_user_api_keys.sql",
  "description": "Show original user_api_keys table column definitions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 3:    groq_api_key TEXT,
> 4:    openrouter_api_key TEXT,
> 5:    openai_api_key TEXT,
> ```

## 🤖 Claude *(18:50:29)*

This is the decisive finding. The SDD definitively pins `deepsearch.run` to **Firecrawl BYOK** (the SAME engine as `deepsearch.scrape`) — NOT Gemini/Google Search grounding. The premise of the task ("google/gemini grounded research half") is **not what the sealed BoK specifies**. Let me read the exact SDD sections 3.3 and the deepsearch tool section, plus confirm the `vision_jobs` table and the unit/result definitions precisely.

## 🤖 Claude *(18:50:31)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/vision-mcp/05-sdd.md",
  "offset": 281,
  "limit": 100
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 281	### 3.3 Deepsearch async job + partial refund (`deepsearch.run`/`poll` — FR-VM-007)
> 282	
> 283	```
> 284	Client                  mcorch_vision_mcp                       Supabase / Firecrawl
> 285	 │──deepsearch.run──────▶│ identity → sentinel                     │
> 286	 │  {query,planned_units}│──deduct_mco_coins(sub, 3, 'deepsearch.run')▶│ (402 → job não nasce)
> 287	 │◀─{job_id,state:queued,│──INSERT vision_jobs (tenant-scoped)─────▶│
> 288	 │   charged_mco:3}      │ … worker in-process (sem teto Edge) …    │
> 289	 │   (submit p95 <2s)    │──scrape×N (robots/allowlist/login-wall)─▶│ Firecrawl BYOK
> 290	 │                       │──sentinel L2 por página → nós na malha──▶│
> 291	 │  [SSE heartbeat ≤25s] │──estado terminal:                        │
> 292	 │                       │   delivered=planned → done               │
> 293	 │                       │   0<delivered<planned → partial:         │
> 294	 │                       │     retida=max(1,floor(3×del/planned))   │
> 295	 │                       │     refundMco(3−retida) UMA vez (guard   │
> 296	 │                       │     por job_id — idempotente)            │
> 297	 │                       │   delivered=0 → failed + refund integral │
> 298	 │──deepsearch.poll─────▶│ mesma identidade (outro tenant → 404)    │
> 299	 │◀─{state,delivered_units,partial,failed_units[],refunded_mco,result}
> 300	 │   (resultado poll-able ≥24h pós-terminal — vision_jobs.expires_at)
> 301	```
> 302	
> 303	### 3.4 Tier 1 → Tier 2 trigger (Essência Humana — FR-VM-010)
> 304	
> 305	```
> 306	Client/agent            Tier 1 (CPU)                       Tier 2 (billable)
> 307	 │──motion.peripheral_scan▶ frame-diff/MOG2 + event-synth     │
> 308	 │   (0–1 mco)            │ + saliência → regiões salientes   │
> 309	 │◀─{regions[], resource_link vision://artifacts/{ref}}       │
> 310	 │   (crops em Storage privado, signed URL curto)             │
> 311	 │── decisão do agente (active-inference: vale o custo?) ────▶│
> 312	 │──vision.describe_image{image_url: <crop signed URL>}──────▶│ fluxo §3.1 (2 mco)
> 313	 │   [bypass: client pode chamar Tier 2 direto SEMPRE —       │
> 314	 │    gate experimental não é gargalo obrigatório]            │
> 315	```
> 316	
> 317	### 3.5 Mesh consolidation (`mesh.consolidate_reference` — FR-VM-021/015)
> 318	
> 319	```
> 320	Tool output (vision+deepsearch)
> 321	  → PII-strip (server-side, pré-insert — FM-VM-10)
> 322	  → sentinel L2 sobre conteúdo (FM-VM-03 — injeção persistente nunca vira nó)
> 323	  → INSERT mcorch_nodes { node_type:'observation'|'fact', user_id (NUNCA NULL p/ scraped),
> 324	      project_id, metadata: { regime, provenance:{source_url,license,origin}, retention_until,
> 325	      cost_mco, fr_id:'FR-VM-021', origin_tag:'scraped'|'tenant' }, stability_score: 1.0 }
> 326	  → regime='fact_supersede' → edge SUPERSEDES → versão anterior (sem decay)
> 327	    regime='observation_decay' → FSRS-6/stability_score normal
> 328	  → trigger/invoke embed-mcorch-node → pgvector(768) (grátis)
> 329	  → INSERT mcorch_edges (nó → nó do run/query — instrumenta KPI do cruzado)
> 330	  → INSERT vision_artifacts manifest (p/ erasure cascade)
> 331	```
> 332	
> 333	---
> 334	
> 335	## 4. API Contract Definitions
> 336	
> 337	> Todo request passa, nesta ordem: **identity (ES256 JWKS | PAT hash) → sentinel.inspectPrompt → débito mcoCoins → handler**. Bloqueio de sentinel, recusa red-line e 402 nunca debitam. Erros espelham o modelo do FRD §4.4 (HTTP no transporte + `structuredContent` no tool result).
> 338	
> 339	### 4.1 Transport & Discovery Endpoints
> 340	
> 341	| Endpoint | Method | Auth | Contract |
> 342	|----------|--------|------|----------|
> 343	| `https://mcp.mcorch.com/` | POST/GET | Bearer (JWT\|PAT) | MCP Streamable HTTP 2025-11-25; headers `Authorization`, `Origin` (allowlist → 403 `origin_invalid`), `MCP-Protocol-Version: 2025-11-25` (mismatch → 400) |
> 344	| `/.well-known/oauth-protected-resource` | GET | público | RFC 9728 PRM (aponta o AS — OTD-VM-020) |
> 345	| `/health` | GET | loopback/watchdog | `200 {status:'ok', uptime_s, tools_registered}` |
> 346	
> 347	Unauthenticated `initialize` (literal — gate de teste AT-VM-002):
> 348	```
> 349	HTTP/1.1 401 Unauthorized
> 350	WWW-Authenticate: Bearer resource_metadata="https://mcp.mcorch.com/.well-known/oauth-protected-resource"
> 351	```
> 352	
> 353	### 4.2 Tool Registry (superfície completa — classes mco do FRD/BRD; fix só após medição material, OTD-VM-004)
> 354	
> 355	| Tool | mco | Scope (PAT) | Gates específicos |
> 356	|------|-----|-------------|-------------------|
> 357	| `mesh.search` | 0–1 | `mesh:read` | RLS-scoped ao tenant via `match_mcorch_nodes` |
> 358	| `vision.describe_image` | 2 | `vision:read` | https-only + host allowlist + ≤20MB + content-type |
> 359	| `vision.detect_objects` | 2 | `vision:read` | idem (Gemini native boxes 0–1000) |
> 360	| `vision.segment` | 2 (fal) / 5 (Replicate) | `vision:read` | pista Apache default (SAM 2); SAM 3 gated FM-VM-08 |
> 361	| `vision.ocr` | 1/página | `vision:read` | provenance tag + sentinel L2 no texto |
> 362	| `vision.analyze_video` | 2/min | `vision:read` | cap duração ≤60min default res |
> 363	| `motion.peripheral_scan` | 0–1 | `vision:read` | `experimental` até GA (recall — OTD-VM-001) |
> 364	| `motion.track` | 1 | `vision:read` | vídeo curto ≤8s GPU; keep-warm (FM-VM-12) |
> 365	| `deepsearch.scrape` | 1 | `deepsearch:run` | robots.txt + login-wall block + allowlist + CDSM Art.4 |
> 366	| `deepsearch.run` | 3 | `deepsearch:run` | job async; débito integral na entrada |
> 367	| `deepsearch.poll` | 0 | `deepsearch:run` | tenant-bound (`job_id` alheio → 404) |
> 368	| `mesh.consolidate_reference` | 1 | `mesh:write` | PII-strip + provenance + regime + NUNCA system node |
> 369	| `vision.alt_text` | 2 | `vision:read` | duty-of-care gate + confidence flag (FR-VM-012/014) |
> 370	| `vision.describe_screen` | 2 | `vision:read` | duty-of-care gate + incerteza sinalizada (FR-VM-013/014) |
> 371	
> 372	**Vocabulário de scopes (fechado):** `vision:read`, `deepsearch:run`, `mesh:read`, `mesh:write`. **NUNCA** existem scopes `credentials:*`/`billing:*` (FM-VM-06 — vazamento de PAT não pode alcançar gestão de credencial nem carteira além do consumo de tools).
> 373	
> 374	### 4.3 Tool Contracts (completos — billing point explícito)
> 375	
> 376	#### `vision.describe_image` (FR-VM-018 · 2 mco)
> 377	
> 378	```typescript
> 379	// Input (sentinel-inspected)
> 380	interface DescribeImageInput {
> ```

## 🤖 Claude *(18:50:31)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/vision-mcp/05-sdd.md",
  "offset": 408,
  "limit": 40
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 408	interface OcrOutput { content: string; pages_processed: number; provenance: { source_url: string }; cost_mco: number }
> 409	// Backend: Mistral OCR 3 (chave per-user mistral_api_key — integração direta; NÃO está no
> 410	// OpenRouter) OU PaddleOCR CPU in-container (sem leg externa).
> 411	// Débito = pages × 1 na entrada (pages declarado); texto extraído passa sentinel L2 antes
> 412	// de qualquer insert (FR-VM-005b). Falha em página → refund proporcional (regra §4.5 FRD).
> 413	```
> 414	
> 415	#### `deepsearch.run` / `deepsearch.poll` (FR-VM-007 · 3 / 0 mco)
> 416	
> 417	```typescript
> 418	interface DeepsearchRunInput  { query: string; planned_units?: number; source_allowlist?: string[] }
> 419	interface DeepsearchRunOutput { job_id: string; state: 'queued'; planned_units: number; charged_mco: number }
> 420	interface DeepsearchPollInput  { job_id: string }
> 421	interface DeepsearchPollOutput {
> 422	  job_id: string
> 423	  state: 'queued' | 'running' | 'done' | 'partial' | 'failed'
> 424	  delivered_units: number; planned_units: number
> 425	  partial: boolean; failed_units?: string[]; refunded_mco?: number
> 426	  result?: { references: Array<{ title: string; url: string; license?: string; summary: string; node_id?: string }> }
> 427	}
> 428	// Débito integral (3) na entrada — 402 → job não nasce. planned_units ≤ cap do plano (DD-VM-003).
> 429	// Partial-delivery refund EXATAMENTE como selado no FRD §4.5: retida = max(1, floor(3×delivered/planned)),
> 430	// refund = 3−retida via refundMco ANTES do estado terminal, floor sempre A FAVOR do tenant,
> 431	// refund no máximo 1× por job_id (guard em vision_jobs.refunded_at). Poll de outro tenant → 404.
> 432	```
> 433	
> 434	#### `mesh.consolidate_reference` (FR-VM-021/015 · 1 mco)
> 435	
> 436	```typescript
> 437	interface ConsolidateInput {
> 438	  content: Record<string, unknown>
> 439	  regime: 'observation_decay' | 'fact_supersede'           // obrigatório (FR-VM-015)
> 440	  provenance: { source_url: string; license: string; origin: 'tenant' | 'scraped' }
> 441	  retention_until: string                                   // ISO; > now(); ≤ teto (DD-VM-004)
> 442	  supersedes_node_id?: string                               // exigido se fact_supersede
> 443	}
> 444	interface ConsolidateOutput { node_id: string; embedded: boolean; cost_mco: number }
> 445	// Débito 1 na entrada. PII-strip + sentinel L2 ANTES do insert; origin='scraped' exige
> 446	// source_url+license e NUNCA system node (user_id NOT NULL — guard server-side, violação = bug crítico).
> 447	// Embed-on-insert via embed-mcorch-node (grátis). Edge ao nó do run sela a traceabilidade.
> ```

## 🤖 Claude *(18:50:38)*

I now have the complete, authoritative picture from all sealed BoK layers. Let me read the `vision_jobs` table schema and the credential resolution row precisely to finalize the unit/result/provider mapping.

## 🤖 Claude *(18:50:40)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/vision-mcp/05-sdd.md",
  "offset": 670,
  "limit": 100
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 670	```
> 671	
> 672	```sql
> 673	-- Migration 3: <ts>_vision_mcp_jobs.sql  (FR-VM-007 · FM-VM-07)
> 674	CREATE TABLE public.vision_jobs (
> 675	  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,   -- = job_id do contrato
> 676	  user_id         uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
> 677	  project_id      uuid,
> 678	  tool            text NOT NULL,                                -- 'deepsearch.run'
> 679	  state           text NOT NULL DEFAULT 'queued'
> 680	                    CHECK (state IN ('queued','running','done','partial','failed')),
> 681	  planned_units   int NOT NULL DEFAULT 1 CHECK (planned_units >= 1),  -- cap por plano: app-side (DD-VM-003)
> 682	  delivered_units int NOT NULL DEFAULT 0,
> 683	  charged_mco     int NOT NULL,
> 684	  refunded_mco    int,
> 685	  refunded_at     timestamptz,                                  -- guard de idempotência (refund 1×/job)
> 686	  failed_units    jsonb,
> 687	  result          jsonb,
> 688	  expires_at      timestamptz NOT NULL,                         -- terminal + 24h (retenção de poll)
> 689	  created_at      timestamptz NOT NULL DEFAULT now(),
> 690	  updated_at      timestamptz NOT NULL DEFAULT now()
> 691	);
> 692	ALTER TABLE public.vision_jobs ENABLE ROW LEVEL SECURITY;
> 693	-- (SELECT own apenas — §5.2; writes via service key do container)
> 694	CREATE INDEX vision_jobs_user_state_idx ON public.vision_jobs (user_id, state);
> 695	```
> 696	
> 697	```sql
> 698	-- Migration 4: <ts>_vision_mcp_artifacts.sql  (FR-VM-009 · FM-VM-11)
> 699	CREATE TABLE public.vision_artifacts (
> 700	  id              uuid DEFAULT gen_random_uuid() PRIMARY KEY,
> 701	  content_ref     text NOT NULL UNIQUE,                 -- chave do cascade de erasure
> 702	  user_id         uuid REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
> 703	  project_id      uuid,
> 704	  node_ids        uuid[] NOT NULL DEFAULT '{}',         -- nós mcorch_nodes derivados
> 705	  storage_paths   text[] NOT NULL DEFAULT '{}',         -- objetos no bucket vision-artifacts
> 706	  provider_copies jsonb NOT NULL DEFAULT '[]'::jsonb,   -- registro de cópias enviadas a providers (FM-VM-11)
> 707	  retention_until timestamptz NOT NULL,                 -- > now(); ≤ teto DD-VM-004 (sweep diário)
> 708	  created_at      timestamptz NOT NULL DEFAULT now()
> 709	);
> 710	ALTER TABLE public.vision_artifacts ENABLE ROW LEVEL SECURITY;
> 711	-- (SELECT own apenas — §5.2)
> 712	CREATE INDEX vision_artifacts_retention_idx ON public.vision_artifacts (retention_until);
> 713	CREATE INDEX vision_artifacts_user_idx ON public.vision_artifacts (user_id);
> 714	```
> 715	
> 716	```sql
> 717	-- Migration 5: <ts>_vision_mcp_erase_rpc.sql  (FR-VM-009 — espelha erase_lead())
> 718	CREATE OR REPLACE FUNCTION public.erase_vision_artifacts(p_content_ref text)
> 719	RETURNS jsonb
> 720	LANGUAGE plpgsql SECURITY DEFINER SET search_path = ''
> 721	AS $$
> 722	DECLARE v_artifact public.vision_artifacts%ROWTYPE;
> 723	BEGIN
> 724	  SELECT * INTO v_artifact FROM public.vision_artifacts
> 725	   WHERE content_ref = p_content_ref
> 726	     AND (user_id = auth.uid() OR auth.role() = 'service_role');  -- auth.uid()-guard (regra ledger-RPC)
> 727	  IF NOT FOUND THEN RAISE EXCEPTION 'artifact_not_found'; END IF;
> 728	  -- Defense-in-depth tenant guard em CADA cascade DELETE (espelha erase_lead() linhas 154/163):
> 729	  -- SECURITY DEFINER bypassa RLS, então re-escopar por user_id impede que um node_ids[] poisoned
> 730	  -- vire primitiva de deleção cross-tenant na malha (NFR-VM-009 / QO-VM-005 — isolamento estrito).
> 731	  DELETE FROM public.mcorch_edges  WHERE (source_id = ANY(v_artifact.node_ids) OR target_id = ANY(v_artifact.node_ids))
> 732	                                     AND user_id = v_artifact.user_id;
> 733	  DELETE FROM public.mcorch_nodes  WHERE id = ANY(v_artifact.node_ids)
> 734	                                     AND user_id = v_artifact.user_id;          -- leva o embedding junto
> 735	  DELETE FROM storage.objects      WHERE bucket_id = 'vision-artifacts' AND name = ANY(v_artifact.storage_paths);
> 736	  DELETE FROM public.vision_artifacts WHERE id = v_artifact.id;
> 737	  RETURN jsonb_build_object('erased', true, 'nodes', array_length(v_artifact.node_ids,1),
> 738	                            'storage_objects', array_length(v_artifact.storage_paths,1),
> 739	                            'provider_copies_registered', v_artifact.provider_copies);
> 740	END $$;
> 741	REVOKE EXECUTE ON FUNCTION public.erase_vision_artifacts(text) FROM PUBLIC, anon;
> 742	GRANT  EXECUTE ON FUNCTION public.erase_vision_artifacts(text) TO authenticated, service_role;
> 743	```
> 744	
> 745	---
> 746	
> 747	## 8. Open Technical Decisions
> 748	
> 749	### 8.1 Decisions sealed by this SDD (deferidas pelo FRD para cá)
> 750	
> 751	| ID | Decision | Sealed value | Rationale |
> 752	|----|----------|--------------|-----------|
> 753	| DD-VM-001 | Path do pacote + porta do serviço | `packages/vision-mcp-core/` · `127.0.0.1:3200` | Precedente `packages/gitnexus-core/` (:3100); loopback-only |
> 754	| DD-VM-002 | Validade do PAT | Default 90 dias; máximo **365 dias** (CHECK + validação no hook) | Limita janela de dreno FM-VM-06 sem matar configs long-lived |
> 755	| DD-VM-003 | Cap de `planned_units` por plano | Starter 10 · Pro 25 · Enterprise 50 (provisório — recalibra com OTD-VM-004) | Proporcional aos saldos 500/2000/10000 mco; enforced app-side no aceite do job |
> 756	| DD-VM-004 | Retention clock (art. 16) | `retention_until` default **90 dias**; teto **365 dias**; sweep diário | Conservador até regulação ANPD 2026 (OTD-VM-007); tenant pode encurtar, nunca exceder o teto |
> 757	| DD-VM-005 | Pin OpenCV | **4.x** (Apache-2.0 verificada); 5.0 só após re-verificação de licença + bench ARM64 | Resolve a metade decidível de OTD-VM-010 |
> 758	| DD-VM-006 | Acesso externo v1 | **PAT-first** (bearer — atende Claude API connector e hosts completos); OAuth 2.1 flow completo entra com OTD-VM-020 | PRM RFC 9728 já publicado desde o dia 1 (401 aponta o caminho); reduz o blast radius da Fatia 3 |
> 759	
> 760	### 8.2 OTD Register (absorve OTD-VM-001..019 verbatim do blueprint §8 + OTD-VM-020 surfaced pelo FRD + OTD-VM-021/022 surfaced pelo MRD/FMEA)
> 761	
> 762	| ID | Description (verbatim-condensada do blueprint) | Option A | Option B | Recommendation | Owner |
> 763	|----|-----------------------------------------------|----------|----------|----------------|-------|
> 764	| OTD-VM-001 | Validação de domínio da saliência (Tier 1). **[CLOSEABLE 2026-06-15 — gate research]** O probe FECHOU e corrigiu 2 erros factuais do blueprint: (a) datasets de UI-saliency EXISTEM — **UEyes** (CHI 2023, 1.980 screenshots eye-tracked) + **Imp1k** (1.000 designs); (b) o SOTA de UI-saliency NÃO é DeepGaze (free-viewing natural, não transfere) — é **SUM** (WACV 2025 Oral, **MIT, self-hostável** → alinha soberania; CC 0.731 vs 0.696 DeepGaze em U-EYE) / UniAR (Google). | Gate Tier 1 sobre SUM (MIT) treinado/avaliado em UEyes+Imp1k; métrica AUC-Judd/sAUC alvo **recall≥0.95** (fundamentado, não palpite); V*Bench/SEAL = PoC do padrão, não métrica de domínio | Fallback frame-diff/MOG2 GA-safe; gate ML `experimental` até recall medido em ARM64 | **A — FECHÁVEL**: SUM+UEyes/Imp1k+recall≥0.95 selados (FR-VM-010/KPI-VM-008). Resta (could_not_verify): latência ARM64 do SUM + transferência zero-shot exata | Engineering |
> 765	| OTD-VM-002 | Demanda do produto cruzado vision+deepsearch = whitespace SEM validação (emendada: assistivo é beachhead demand-provado; cruzado segue hipótese) | GTM ancorado no assistivo, cruzado como upsell | GTM no cruzado direto | **A** (conforme MRD bifurcado) | Sovereign |
> 766	| OTD-VM-003 | Long-running jobs sobre MCP p/ clients externos: `tasks` experimental; Claude API connector consome só tools; zero exemplos de produção coletados | submit→job_id + poll tool (tools-only universal) | MCP tasks/elicitation quando estabilizar | **A** (já selado em FR-VM-007); montar matriz de capabilities por host na Fatia 3 | Engineering |
> 767	| OTD-VM-004 | Unit economics medido. **[CLOSEABLE 2026-06-15 — gate research]** Custo real fonteado para as 6 classes (5 oficiais provider + segment cross-check 2 backends); o modelo 4×-floor confirma a grade ATUAL **sem nenhuma classe sub-margem** (scrape/ocr/video no-piso; describe_image/detect no-piso ou acima). SOP `docs/processes/vision-mcp-cost-calibration.md` (tabela datada). | Manter classes (validadas) + **MUDANÇA OBRIGATÓRIA**: `vision.segment` COST-AWARE (2 mco fal.ai SAM3 $0.005 / 4-5 Replicate SAM2 $0.017 — banir "cobrar 2 rodando Replicate") | Fixar classes pela estimativa | **A — FECHÁVEL** por fonte; resta APENAS medição em produção do 1º run pago (tokenização VLM default + detection N-boxes + infra PaddleOCR) | Engineering |
> 768	| OTD-VM-005 | DPAs/SCCs dos providers p/ inputs de imagem. **[PARTIAL 2026-06-15 — gate research]** Postura BYOK CONFIRMADA correta. Fato decisivo: todos têm zero-retention + EU SCCs, mas a **ANPD NÃO reconhece EU SCCs** como equivalentes (Res. 19/2024) e os EUA seguem **sem adequação** → DPA c/ EU SCCs NÃO basta sob LGPD. **Res. 32/2026 (26-jan) tornou a UE adequada.** A mitigação "SCCs ANPD no DPA" (FM-VM-10) é **INVIÁVEL hoje** — corrigida em §5.5.5. | BYOK-only sem default; mitigação real = roteamento UE adequado (Res.32/2026) OU PII-strip robusto pré-leg OU consentimento art.33 VIII; **Mistral = candidato default** (100% UE, adequação direta) | Fixar provider US default | **PARTIAL by design** — sub-OTD: validar Vertex/Bedrock EU via BYOK; provider default só com PII-strip OU rota UE OU SCC-ANPD assinada | Sovereign + Engineering |
> 769	| OTD-VM-006 | Licenças self-host. **[CLOSEABLE 2026-06-15 — gate research]** LICENSE fetchado verbatim: **14 verdes** (Apache/MIT/BSD — SAM2/RF-DETR-core/Qwen3-VL/SigLIP2/OWLv2/V-JEPA2/InternVideo2/OpenCV4.5+/PaddleOCR/SEA-RAFT/OpenEB/snnTorch/Tonic/v2e), **3 minas banidas** (rpg_vid2e GPL-3.0 · VideoMAEv2 CC-BY-NC · Ultralytics AGPL), **6 condicionais** (SpikingJelly AITISA **não-MIT** · Norse LGPL · SAM3/DINOv3 bespoke+ITAR · RF-DETR-Plus PML1.0 · Mistral OCR proprietária). Allowlist/denylist gravada no §2.2. | Pista Apache default CONFIRMADA (§2.2); gated só com termos lidos | Excluir gated do v1 | **A — FECHÁVEL**: allowlist verificada (FMEA-VM-008 occurrence↓). Resta: PML 1.0 integral + Mistral self-host terms quando entrarem em escopo | Engineering |
> ```

## 🤖 Claude *(18:50:44)*

I have everything I need. The sealed BoK is unambiguous and the task's premise is materially contradicted by the SDD. Let me confirm the SDD section 5.5.x deepsearch credential / provider naming and the §2.2 module map once more for precision, then deliver.

## 🤖 Claude *(18:50:46)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/vision-mcp/05-sdd.md",
  "offset": 580,
  "limit": 15
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 580	// service-role SELECT: revoked_at IS NULL AND expires_at > now() — senão 401
> 581	```
> 582	
> 583	**Anti-patterns proibidos (herdados do SOP):** `atob(token.split('.')[1])` cego para extrair `sub`; confiar em `user_id` vindo de body/header não-verificado; processar request com JWKS inalcançável ("fail-open"); aceitar bearer em query string; token passthrough para providers downstream (proibição explícita da spec MCP 2025-11-25).
> 584	
> 585	### 5.4 Secrets Inventory (NOMES apenas — valores jamais em doc/código/commit)
> 586	
> 587	| Secret Name | Used In | Location | Scope rule |
> 588	|-------------|---------|----------|------------|
> 589	| `SB_SECRET_KEY` | container (PostgREST/RPC: deduct/refund/mesh/jobs/logs) | env do container (compose, sem valor no repo) | **Server-side only**; jamais em path client-reachable; legadas `SUPABASE_SERVICE_ROLE_KEY`/`ANON_KEY` REVOGADAS |
> 590	| `OPENROUTER_API_KEY` | fallback de embed/system flows | Supabase Vault | **Fallback-restricted**: SÓ cron/service-role/system; nunca caminho primário user-facing (API Tenancy) |
> 591	| `user_api_keys.firecrawl_api_key` (per-user) | `deepsearch.*` | Vault via `decrypted_user_api_keys` (service-role only view) | Primário; ausente → 402 `firecrawl_not_configured` |
> 592	| `user_api_keys.openrouter_api_key` / `google_api_key` / `openai_api_key` (per-user) | `vision.*` VLM legs | idem | Primário (BYOK → metering custo 0) |
> 593	| `user_api_keys.mistral_api_key` (per-user, nova) | `vision.ocr` (Mistral OCR 3 direto) | idem | Primário; ausente → 402 `mistral_not_configured` (PaddleOCR CPU é o caminho sem chave) |
> 594	| PAT do tenant (`mcp_access_tokens.token_hash`) | clients MCP externos | DB (hash SHA-256 apenas) | Plaintext exibido 1× no client; nunca armazenado |
> ```

## 🤖 Claude *(18:50:50)*

I have complete, materially-sourced answers across all five sealed BoK layers (blueprint, MRD, PRD, FRD, SDD) plus the live migration schema. The findings are decisive and the task's premise is contradicted by the sealed BoK. Delivering the structured map.

## 🤖 Claude *(18:52:01)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "summary": "CRITICAL CORRECTION TO THE TASK PREMISE: the sealed Vision MCP BoK does NOT specify a \"google/gemini grounded research half\" for deepsearch.run. Both deepsearch.scrape AND deepsearch.run are pinned to the SAME engine \u2014 Firecrawl, per-user BYOK, fail-closed. The SDD (the authoritative design layer, sealed 2026-06-15) is explicit: 05-sdd.md:113 \"DEEPSEARCH GROUNDING \u2014 Firecrawl BYOK per-user (fail-closed)\", 05-sdd.md:284-289 shows the deepsearch.run worker doing \"scrape\u00d7N (robots/allowlist/login-wall) \u2192 Firecrawl BYOK\", and 05-sdd.md:591 binds user_api_keys.firecrawl_api_key as the credential for deepsearch.* (ausente \u2192 402 firecrawl_not_configured). There is NO Gemini grounding, NO Google Search grounding, NO Google CSE anywhere in the deepsearch surface. deepsearch.run is the ASYNC, multi-unit sibling of deepsearch.scrape (which is single-URL synchronous): same provider, same scope (deepsearch:run), differing only in job semantics. A \"unit\" = one source/page scraped+consolidated (planned_units = N pages/queries the job will fetch). The result payload = an array of consolidated references {title, url, license?, summary, node_id?}. Partial delivery is physical: a long-lived in-container worker scrapes N pages; pages that fail (robots/login-wall/error) reduce delivered_units below planned_units \u2192 state 'partial' \u2192 proportional refund floored in the tenant's favor. gemini_api_key is NOT confirmed as a user_api_keys column \u2014 the actual column is google_api_key (used for vision.* VLM legs, NOT for deepsearch).",
  "findings": [
    {
      "topic": "Provider for deepsearch.run grounded-research leg = Firecrawl, NOT Gemini/Google",
      "detail": "The task premise (\"google/gemini grounded research half\") is materially contradicted by the sealed BoK. The SDD architecture diagram labels the grounding box verbatim: 'DEEPSEARCH GROUNDING \u2014 Firecrawl BYOK per-user (fail-closed)'. The deepsearch.run sequence diagram shows the in-process worker doing 'scrape\u00d7N (robots/allowlist/login-wall)' against 'Firecrawl BYOK'. No Gemini grounding, Google Search grounding, or Google CSE appears anywhere in the deepsearch tool family. deepsearch.run and deepsearch.scrape share provider (Firecrawl), credential (firecrawl_api_key), and PAT scope (deepsearch:run); they differ ONLY in sync-single-URL (scrape, 1 mco) vs async-multi-unit-job (run, 3 mco).",
      "source": "docs/bok/vision-mcp/05-sdd.md:113 + 05-sdd.md:284-289 (sequence diagram) + 05-sdd.md:365-367 (tool registry)"
    },
    {
      "topic": "Credential is firecrawl_api_key per-user, fail-closed \u2014 NOT gemini_api_key",
      "detail": "Secrets Inventory binds 'user_api_keys.firecrawl_api_key (per-user)' to 'deepsearch.*' with rule 'Prim\u00e1rio; ausente \u2192 402 firecrawl_not_configured'. The column does not yet exist (it is a NEW migration: PR-VM-007 / FR-VM-004; SDD migration `<ts>_user_api_keys_vision_byok.sql` adds `firecrawl_api_key text` + `mistral_api_key text` via the Vault trigger family, pattern of migration 20260601060000). The grounding leg has NO Gemini/Google dependency at all.",
      "source": "docs/bok/vision-mcp/05-sdd.md:591 + 05-sdd.md:231 + 05-sdd.md:662-665 (ADD COLUMN firecrawl_api_key)"
    },
    {
      "topic": "gemini_api_key is NOT a user_api_keys column \u2014 the real column is google_api_key",
      "detail": "Live schema check: the original table 20260421000000_create_user_api_keys.sql defines groq_api_key, openrouter_api_key, openai_api_key. The encryption migration 20260601000000 enumerates the full live column set including google_api_key, nanobana_api_key, seedance_api_key, replicate_api_key, higgsfield_api_key, elevenlabs_api_key \u2014 there is NO 'gemini_api_key'. The SDD assigns user_api_keys.google_api_key (+ openrouter_api_key, openai_api_key) to vision.* VLM legs (describe_image etc.), explicitly NOT to deepsearch. So even the Gemini-family key in the system serves vision tools, not the deepsearch grounding leg.",
      "source": "supabase/migrations/20260421000000_create_user_api_keys.sql:3-5 + 20260601000000_credential_encryption.sql:504 + docs/bok/vision-mcp/05-sdd.md:592"
    },
    {
      "topic": "Definition of ONE unit",
      "detail": "A 'unit' = one source/page that the job scrapes-and-consolidates. planned_units is the declared number of pages/queries the job will fetch (FRD \u00a74.5.2: 'todo job declara planned_units (p\u00e1ginas/queries) no aceite'). DB CHECK: planned_units int NOT NULL DEFAULT 1 CHECK (planned_units >= 1). Caps per plan (DD-VM-003, provisional): Starter 10 \u00b7 Pro 25 \u00b7 Enterprise 50, enforced app-side at job acceptance, proportional to mco balances 500/2000/10000. The terminal state reports delivered_units (how many actually succeeded).",
      "source": "docs/bok/vision-mcp/04-frd.md:204 (\u00a74.5.2) + 05-sdd.md:681-682 + 05-sdd.md:755 (DD-VM-003)"
    },
    {
      "topic": "Result payload contents (poll `result` field)",
      "detail": "DeepsearchPollOutput.result is typed exactly: `result?: { references: Array<{ title: string; url: string; license?: string; summary: string; node_id?: string }> }`. So the deliverable is an array of consolidated references \u2014 each a scraped source with title, URL, optional license, a synthesized summary, and an optional mesh node_id (set when the reference was written to the Knowledge Mesh via consolidation). It is NOT a single synthesized prose report and NOT a citations-only list \u2014 it is structured per-source reference objects. Each reference page also passes sentinel L2 and becomes a mesh node (observation/fact) during the run (sequence diagram: 'sentinel L2 por p\u00e1gina \u2192 n\u00f3s na malha').",
      "source": "docs/bok/vision-mcp/05-sdd.md:421-427 (DeepsearchPollOutput) + 05-sdd.md:290"
    },
    {
      "topic": "How partial delivery physically happens",
      "detail": "deepsearch.run charges the full class (3 mco) at entry via deduct_mco_coins BEFORE enqueue (402 \u2192 job never born). An in-container long-lived worker (no Edge wall-clock ceiling \u2014 blueprint \u00a75.1 rationale) then scrapes the N planned pages via Firecrawl BYOK. Pages that fail (blocked by robots.txt / login-wall / source not in allowlist / scrape error) are counted in failed_units and lower delivered_units below planned_units. Terminal states: delivered=planned \u2192 'done'; 0<delivered<planned \u2192 'partial'; delivered=0 \u2192 'failed'. The worker writes state to vision_jobs and exposes it via deepsearch.poll (cost 0, tenant-bound, poll-able \u226524h post-terminal via vision_jobs.expires_at).",
      "source": "docs/bok/vision-mcp/05-sdd.md:284-301 (sequence) + 05-sdd.md:674-695 (vision_jobs table)"
    },
    {
      "topic": "Partial-delivery refund formula (sealed, exact)",
      "detail": "Sealed in FRD \u00a74.5 and re-stated verbatim in SDD: retained charge = max(1, floor(3 \u00d7 delivered_units / planned_units)); refund = 3 \u2212 retained, executed via refundMco BEFORE the job reaches terminal state. Rounding ALWAYS favors the tenant (floor on the charge). Full failure (delivered=0) \u2192 full 3 mco refund, net mco_balance delta = 0. Idempotency: refund executed at most once per job_id, guarded by vision_jobs.refunded_at. Poll retries never re-fire refund. Poll from another tenant \u2192 404 (tenant-bound by user_id).",
      "source": "docs/bok/vision-mcp/04-frd.md:199-208 (\u00a74.5) + 05-sdd.md:428-431 + 05-sdd.md:685 (refunded_at guard)"
    },
    {
      "topic": "deepsearch.run vs deepsearch.scrape relationship",
      "detail": "deepsearch.scrape (FR-VM-020, PR-VM-006, 1 mco, Fatia 2): synchronous scrape of 1 public URL via Firecrawl BYOK, logged-out only, gates robots.txt + login-wall block + permissive-source allowlist + CDSM Art.4 opt-out, output markdown + provenance/license metadata. deepsearch.run (FR-VM-007/FR-VM-013-PR, 3 mco, Fatia 3): the ASYNC multi-unit job that runs scrape\u00d7N over the same Firecrawl engine with job semantics (run\u2192job_id\u2192poll). They are the same provider/leg at different cardinality and sync model \u2014 there is no second 'Google/Gemini half'. The two-tool deepsearch surface is scrape(sync,1-URL) + run/poll(async,N-URL).",
      "source": "docs/bok/vision-mcp/04-frd.md:53 (FR-VM-020) + 04-frd.md:44 (FR-VM-007) + 05-sdd.md:365-367"
    },
    {
      "topic": "Tool I/O contract for deepsearch.run / poll",
      "detail": "Input run: { query: string, planned_units?: number, source_allowlist?: string[] }. Output run: { job_id: string, state: 'queued', planned_units: number, charged_mco: number } (submit p95 <2s, NEVER blocking). Input poll: { job_id: string }. Output poll: { job_id, state: 'queued'|'running'|'done'|'partial'|'failed', delivered_units, planned_units, partial: boolean, failed_units?: string[], refunded_mco?: number, result?: {references[...]} }. PAT scope required: deepsearch:run for both run and poll. Sentinel inspectPrompt runs on args after identity, before debit; source_allowlist gate applies.",
      "source": "docs/bok/vision-mcp/05-sdd.md:417-432 + 04-frd.md:170-173 + 05-sdd.md:366-367"
    },
    {
      "topic": "Runtime location of the grounded-research execution",
      "detail": "deepsearch.run runs INSIDE the container mcorch_vision_mcp (packages/vision-mcp-core/, 127.0.0.1:3200, DD-VM-001) as an in-process worker \u2014 explicitly NOT an Edge Function (blueprint \u00a75.1: 'Timeouts matam a rota Edge ... Deepsearch \u00e9, por defini\u00e7\u00e3o, trabalho de minutos \u2014 n\u00e3o pode bloquear num isolate Edge'). The whole cycle is ZERO new Edge Functions (reuses embed-mcorch-node, get-infra-status, deduct_mco_coins). Job state persisted in new table public.vision_jobs (RLS, SELECT-own; writes via container service key).",
      "source": "docs/bok/vision-mcp/00-deepsearch-blueprint.md:338 (\u00a75.1) + 05-sdd.md:753 (DD-VM-001) + 05-sdd.md:674-695"
    },
    {
      "topic": "Demand status of deepsearch.run is HYPOTHESIS, not proven market",
      "detail": "deepsearch.run is part of the vision\u00d7deepsearch cross-product, which the MRD classifies as 'Aposta de diferencia\u00e7\u00e3o N\u00c3O-validada' / 'Hip\u00f3tese n\u00e3o-validada (whitespace sem demanda comprovada)' \u2014 gated by KPI-VM-003 (cross-product validation rate) and OTD-VM-002. It is Fatia 3 (Should Have, PR-VM-013), AFTER the assistive beachhead. This matters for build sequencing: deepsearch.run is not on the MVP/v1.0 critical path (Fatias 1-2); only deepsearch.scrape is.",
      "source": "docs/bok/vision-mcp/01-mrd.md:20 + 03-prd.md:155 (PR-VM-013 Should Have) + 03-prd.md:217-218"
    }
  ],
  "open_questions": [
    "PROVIDER PINNED BUT GROUNDING MECHANISM UNDERSPECIFIED: The BoK pins Firecrawl as the deepsearch.run engine, but Firecrawl's own surface includes BOTH /scrape (single URL) AND /search (query\u2192ranked results\u2192optional content). The SDD sequence diagram shows deepsearch.run doing 'scrape\u00d7N' \u2014 but a query\u2192N-sources job needs a discovery/search step FIRST to turn the free-text `query` into N URLs to scrape. The BoK never specifies HOW the query becomes the N scrape targets: Firecrawl /search? a separate search provider (Tavily/Exa appear only as competitors)? source_allowlist as the literal URL list? This is the real OTD \u2014 candidate: OTD-DEEPSEARCH-RUN-DISCOVERY (how a free-text query is decomposed into planned_units scrape targets).",
    "Is there ANY Gemini/Google grounded-research leg intended at all? The task framing assumed one; the sealed BoK has none. If the Sovereign actually wants Google/Gemini Search-grounding (distinct from Firecrawl scrape) as a SECOND deepsearch leg, that is a NET-NEW requirement NOT in the sealed BoK \u2014 it would require a BoK amendment (deepsearch-blueprint emenda v0.x+1 \u2192 re-run /bok-scribe), not improvisation. Flag to Sovereign before building.",
    "When does a scraped reference become a mesh node during deepsearch.run, and does that consume additional mco? The sequence diagram shows 'sentinel L2 por p\u00e1gina \u2192 n\u00f3s na malha' inside the run (implying auto-consolidation), but mesh.consolidate_reference is a SEPARATE billable tool (1 mco). Whether deepsearch.run auto-writes nodes for free as part of its 3-mco class, or whether consolidation is a separate explicit call, is not reconciled between \u00a73.3 and \u00a73.5 / the run result's node_id field.",
    "Exact definition of a 'failed' unit for partial-refund accounting: does a page blocked by robots.txt/login-wall count as a failed_unit (reducing delivered_units, triggering refund) or as a successfully-completed-but-empty unit (no refund)? The refund formula floor(3\u00d7delivered/planned) is exact, but the boolean of what increments delivered_units vs failed_units for non-error skips (robots/allowlist) is not pinned.",
    "planned_units semantics when query yields fewer discoverable sources than planned_units: if the user requests planned_units=10 but the query only surfaces 4 valid sources, is that 'partial' (4/10, refund) or 'done' (4/4 of what existed)? The BoK ties delivered vs planned to refund but does not address the case where planned_units exceeds available sources.",
    "OAuth/external-reachability of deepsearch.run: DD-VM-006 seals external access as 'PAT-first', full OAuth 2.1 flow deferred to OTD-VM-020. Since deepsearch.run is the Fatia-3 external job tool, the exact AS decision (Supabase Auth fronted vs WorkOS/Auth0 vendor) remains an open SDD/OTD item that gates external consumption of this tool.",
    "Source allowlist for deepsearch.run: deepsearch.scrape enforces a 'permissive-source allowlist' (Wikipedia/PLOS/Frontiers/SEC EDGAR/IPFS per FM-VM-11) but the run input takes an optional source_allowlist[]. The interaction between the tenant-supplied source_allowlist and the system permissive allowlist (intersection? override? CDSM opt-out precedence) is not pinned."
  ]
}
```

> **Tool Result (StructuredOutput)** - ✅ Success
>
> ```
> Structured output provided successfully
> ```

## 🤖 Claude *(18:52:12)*

I've completed the rigorous map of `deepsearch.run`. The headline finding overturns the task's premise: the sealed Vision MCP BoK does **not** specify any "google/gemini grounded research half" — both `deepsearch.scrape` and `deepsearch.run` are pinned to **Firecrawl BYOK, per-user, fail-closed**, sharing credential (`firecrawl_api_key`) and PAT scope (`deepsearch:run`), differing only in sync-single-URL vs async-multi-unit-job semantics. `gemini_api_key` is not a `user_api_keys` column (the real column is `google_api_key`, and it serves `vision.*` VLM legs, not deepsearch).

All four requested determinations are answered with file:line sources from the authoritative SDD layer plus the live migration schema, and every place the BoK leaves the provider/unit/result mechanism unpinned is flagged as an open question (candidate OTD) rather than improvised — most notably the real gap: how a free-text `query` is decomposed into `planned_units` scrape targets (Firecrawl `/search` vs a separate discovery step is never specified).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-15 - agent-ae3ca456c3895778f]]
> * **Próxima Sessão**: [[2026-06-15 - agent-aee5f968c94e55954]]
%% --- TIMELINE END --- %%

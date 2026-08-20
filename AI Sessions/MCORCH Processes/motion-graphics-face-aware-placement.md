# SOP — Fuga de rosto no motion graphics (`detectFaceRegions` → `pickCalmestZone`) (Lei 2)

> **Feature:** pré-passe **server-side, offline, US$ 0** de detecção de rosto sobre o FOOTAGE que produz uma **região PROIBIDA** para o cartão de motion graphics (`caption_style='motion-graphics-hero-9x16'`). A escolha de zona (`pickCalmestZone`, Fatia 1) passa a **excluir** as zonas que caem sobre o rosto **antes** de eleger a mais calma — o texto foge do sujeito mesmo quando a zona estatisticamente mais calma coincide com ele. É a **Fatia 2 / Opção C** (MediaPipe FaceDetector WASM in-Chromium), que **enriquece** a Fatia 1, não a substitui.
> **BoK SSOT:** `docs/bok/video-repurpose/12-amendment-motion-graphics.md` (Amendment 12 — **OTD-VR-016** era a Fatia 2 DEFERIDA; este SOP + o código a **fecham**). SOP irmão (Fatia 1): `docs/processes/motion-graphics-zone-saliency.md` — cujo "Limite conhecido" (saliência mede CALMA, não ROSTO) é exatamente o que esta fatia resolve.
> **Motor:** `scripts/video-repurpose/face-detect.ts` → `detectFaceRegions(sourcePath, times, opts)`. **Runtime vendorizado:** `scripts/video-repurpose/face-assets/` (bundle MediaPipe + WASM SIMD + modelo `.tflite` + `detector.html`). **Consumidor:** `scripts/video-repurpose/segment-core.ts` (`renderClip`, caminho `caption_mode==='beats'`) — o pré-passe roda **só** para `MOTION_GRAPHICS_STYLE`; os 7 estilos karaokê ancorados no rodapé **nunca** entram aqui. **Exclusão de zona:** `scripts/video-repurpose/zone-saliency.ts` (`pickCalmestZone` aceita `forbidden?`).

## ORO triplet
- **Operator:** MCORCH Master Execution Agent (constrói/prova); na operação, o worker `video-repurpose-bridge` executa sozinho ao renderizar um corte `motion-graphics-hero-9x16`.
- **Reviewer:** Sovereign + Vision QA **OCULAR por render** (Lei 1 para mídia — a bbox geométrica NÃO substitui o olho; a prova é: o rosto foi detectado SOBRE o rosto **e** o texto pousou fora dele) + `/security-review` (o motor recebe caminho de arquivo → todo `spawn` de FFmpeg recebe **array** de args, nunca string de shell; a expressão de reframe carrega só frações fixas de aspecto, zero dado do caller; o runtime é **air-gapped** — a rota do browser aborta todo http/https).
- **Owner:** Sovereign. **Custo mcoCoins = 0** (rail FFmpeg + WASM 100% local; nenhuma API externa). Custo = CPU: **~2,3 s por corte** de 3 instantes (medido: `detectFaceRegions(final.mp4,[8,11,14]) → 2327 ms`, incluindo o launch do Chromium na 1ª chamada; **amortizado** — o browser é cacheado no processo e reusado entre clips). Risco = **qualidade percebida do criativo**, não financeiro.

## Operator — manual equivalente

Hoje, para não cobrir o rosto, o **editor humano** olha o corte reenquadrado 9:16, vê **de que lado está a cara do sujeito**, e ancora o cartão no canto oposto — mesmo que o outro canto pareça "mais bonito/calmo". O motor automatiza exatamente esse juízo de *"onde está o rosto? evite-o"*. Para achar **um** rosto à mão (aqui em `t=8 s`, canvas 9:16 608×1080), o operador roda:

```bash
# 1) Reenquadra 9:16 (MESMO center-crop do segment-core) → 1 frame PNG.
ffmpeg -v error -y -ss 8 -i master.mp4 -frames:v 1 \
  -vf "crop=min(iw\,ih*0.5625):min(ih\,iw/0.5625):(iw-ow)/2:(ih-oh)/2,scale=608:1080:force_original_aspect_ratio=increase,crop=608:1080,setsar=1" frame.png
# 2) Roda o FaceDetector (blaze_face_short_range) sobre frame.png no Chromium headless — offline, US$0.
#    A bbox em pixels / (608,1080) = fração do canvas. Repete para start/mid/end e UNE as caixas (rosto que se move).
# 3) Desenha a bbox e OLHA: a caixa caiu sobre olho/nariz/boca? Então é rosto. Escolha a zona do LADO OPOSTO.
```

O motor faz os 3 instantes num Chromium cacheado, normaliza cada bbox por `workW/workH`, **une** todas as detecções (pega o rosto em movimento) e entrega a lista à `pickCalmestZone`, que remove as zonas sobrepostas e elege a mais calma entre as sobreviventes. O **aceite estético** (o cartão está legível e bonito?) continua sendo o olho (Vision QA), não a estatística.

## Achados materiais que definem o veredito (não re-derivar)

| # | Achado | Consequência de design |
|---|--------|------------------------|
| B1 | **MediaPipe FaceDetector (`blaze_face_short_range`) WASM in-Chromium é o único runtime de visão já no host** (Candidato A). OpenCV (B) e onnxruntime (C) foram REJEITADOS: `import cv2`/`import onnxruntime` = `ModuleNotFoundError` (não instalados). A é a MESMA arquitetura headless-Chromium do `render-core`. | Reusar o Chromium do Playwright + o pipeline WASM. Nenhuma dependência de runtime nova; só o modelo `.tflite` (230 KB) baixado uma vez em design-time. |
| B2 | **`executablePath: chromium.executablePath()` é LOAD-BEARING, não cosmético.** Sem pinar o binário (resolução default), o loader emscripten do WASM falha o `fetch()` do `.wasm` `file://` com **"Failed to fetch"**. Provado por isolamento: o ÚNICO toggle que vira a detecção entre OK e falha é o `executablePath`. `render-core` nunca sofreu isso porque render **não** faz `fetch()` de wasm. | `face-detect.ts` pina `executablePath: chromium.executablePath()` no `chromium.launch`. **Anticorpo:** se um dia a detecção "parar de achar rosto" com "Failed to fetch" no log, é o `executablePath` — não o modelo. |
| B3 | **Chromium bloqueia `fetch()` de `file://` por padrão**; `--allow-file-access-from-files` cobre XHR/subresource, **não** `fetch()`. A rota `page.route('**/*')` que **continua** `file://`/`data:`/`blob:` (e **aborta** todo o resto) resolve o wasm PELA camada de rede do Playwright. | `face-detect.ts` instala essa rota. Duplo propósito: (a) destrava o `fetch()` do wasm; (b) **air-gap por construção** — em PRODUÇÃO nenhum http/https é sequer emitido (`getBlockedNetworkRequests() === []`), não só sob o smoke. |
| B4 | **`@mediapipe/tasks-vision` NÃO está declarado no `package.json`** (só `camera_utils`/`drawing_utils`/`hands` estão). Está só transitivamente presente. Um `npm ci` limpo NÃO o restauraria → o detector falharia-aberto pra Fatia 1 **para sempre, em silêncio**. | Vendorizamos o runtime INTEIRO (bundle 140 KB + WASM SIMD 9,7 MB + `.tflite` 230 KB + `detector.html`) em `face-assets/`, não só o `.tflite`. Custo ~10 MB no git = preço de um runtime de visão self-hosted, version-independent, air-gapped. Ver `face-assets/README.md`. |
| B5 | **A região proibida vive no MESMO espaço de canvas das zonas.** O `reframeChain(9/16, workW, workH)` do detector **espelha** o do `segment-core`/`zone-saliency`; a bbox é normalizada por `workW/workH` → fração 0..1. | Sem esse espelho, a bbox pontuaria pixels que o render não sobrepõe. A UNIÃO das detecções ao longo de start/mid/end = a região proibida. |
| B6 | **Exclusão por sobreposição de ÁREA, não por centro.** Uma zona é removida quando a fração dela coberta pela união dos rostos passa de `EXCLUDE_FRAC=0.12`. Overlap medido por grid-sample 24×24 (união correta de rects sobrepostos, determinístico). | `pickCalmestZone` remove as zonas sobrepostas, escolhe a mais calma entre as sobreviventes (desempate `PREFERENCE`). Se **todas** as zonas legíveis forem cobertas (rosto enorme/central, raro), cai na **menos coberta** (calma como desempate) e marca `faceExcludedAll:true` — **nunca** retorna vazio. |
| B7 | **Fail-open, best-effort — NUNCA derruba um render.** Detecção é refinamento de qualidade, não gate. | `detectFaceRegions` é contratualmente **no-throw**: assets ausentes / fonte ilegível / falha de browser/WASM / zero detecções → `{ forbidden:[], degraded:true }` (ou `degraded:false` com `forbidden:[]` quando o frame simplesmente não tinha rosto). O `segment-core` embrulha em `try/catch` **e** loga. Sem `forbidden`, `pickCalmestZone` é **idêntica** à Fatia 1. |
| B8 | **`blaze_face_short_range` é frontal/near-frontal best-effort.** Perfil duro, oclusão pesada, rosto minúsculo/distante podem ser **perdidos** — provado no próprio witness: `t=8/11 s` detectaram (score ~0,6), `t=14 s` (perfil mais fechado) **não** detectou. | Honestidade material (Lei 1): a fuga de rosto é *best-effort*, não garantia. Um rosto perdido num instante → sem região para aquele instante → aquele instante volta ao comportamento Fatia 1. A UNIÃO sobre start/mid/end mitiga (basta 1 instante achar). |

## Sequence — os passos (cada um com critério material)

| # | Passo | Executor | Sucesso material |
|---|-------|----------|------------------|
| 0 | O `segment-core` só chama o pré-passe quando `resolveCaptionStyle(clip.caption_style) === MOTION_GRAPHICS_STYLE`. Outros estilos não pagam. | `segment-core.ts` | estilo karaokê → nenhum `spawn`/browser de face-detect (0 custo). |
| 1 | **Instantes:** `sampleTimes(clip.in_sec, clip.out_sec, 3)` (exportada de `zone-saliency`) → os **MESMOS** start/mid/end que a saliência amostra. | `sampleTimes` | 1..3 instantes finitos dentro de `[in,out]`. |
| 2 | **Guardas fail-open:** fonte inexistente **ou** assets do runtime ausentes → `degraded:true`, `forbidden:[]`, **sem browser**. | `detectFaceRegions` | `existsSync(source)` **e** `assetsPresent()`, senão degrada cedo. |
| 3 | **Browser cacheado (lazy):** launch do Chromium do Playwright (`executablePath()` pinado, `--allow-file-access-from-files`) + rota air-gap (continua `file://`/`data:`/`blob:`, aborta o resto) + `goto(detector.html)` + `waitFor(window.__ready)`. Reusado entre clips. | `ensureDetectorPage` | página pronta OU `null` (fail-open → degraded). |
| 4 | **Por instante:** `ffmpeg -ss t -frames:v 1 -vf <reframe 9:16 workW×workH>` (array de args) → PNG → `page.evaluate(__runFaceDetect(file://png))`. Fail-soft por instante (`exit≠0`/eval throw → pula; os outros ainda contam). | `extractReframedFrame` + eval | ≥1 frame processado, senão `degraded:true`. |
| 5 | **Filtro + normalização + união:** descarta score < `minConfidence` (default 0.4); normaliza `bbox/(workW,workH)`; clampa a [0,1]; **une** todas as detecções. | `detectFaceRegions` | `forbidden: NormRect[]` (fração) + `merged` (bbox da união) + `sampled` (frames que passaram). |
| 6 | **Exclusão de zona:** `pickCalmestZone(source, in, out, { forbidden })` remove zonas com overlap > `EXCLUDE_FRAC` e elege a mais calma sobrevivente; `faceExcludedAll` se todas caíram. | `pickCalmestZone` | `zone`/`rect` da zona escolhida, `faceExcludedAll` correto. |
| 7 | **Injeção no beat:** `beatProps = beats.map(b => ({...b, zone}))`. O template lê `b.zone` e ancora o cartão. | `segment-core.ts` | props do render carregam a zona escolhida; PNG RGBA no canto certo. |

## Verification gates

Anticorpo re-executável: **`scripts/qa/smoke-face-aware-zone.ts`** — **RODAR antes de mexer** no detector, na exclusão de zona, no `EXCLUDE_FRAC`, ou nos assets vendorizados.

| Gate | O que prova | Custo |
|------|-------------|-------|
| **G1 — rosto à DIREITA vence a calma.** Footage busy-ESQ/calm-DIR: saliência sozinha → DIREITA; com `forbidden` da metade direita → **ESQUERDA**. | A exclusão de rosto **sobrepõe** a calma. Hermético (fixtures `ffmpeg lavfi`). | 0 |
| **G2 — espelho** (busy-DIR/calm-ESQ; `forbidden` esquerda → DIREITA). | A escolha **segue o rosto**, não um viés fixo. | 0 |
| **G3 — Fatia 1 intacta.** Sem `forbidden` → comportamento idêntico ao de hoje (`scores.length===6`, `!degraded`, `!faceExcludedAll`). | Zero regressão da Fatia 1 (compat de assinatura). | 0 |
| **G4 — fallback rosto-ocupa-tudo.** `forbidden` = canvas inteiro → retorna zona não-vazia, `faceExcludedAll:true`, sem lançar. | Nunca retorna vazio; degradação sinalizada. | 0 |
| **G5 — detector fail-open.** Fonte inexistente → `degraded:true`, `[]`, sem lançar. | Cosmético nunca derruba render (B7). | 0 |
| **G6 — rosto REAL offline.** Se `final.mp4`/`FACE_SMOKE_SRC` presente: detecta o rosto num lado (offline, `blockedNetworkRequests===[]`), reporta a bbox ocular, e prova que a zona escolhida tem overlap com o rosto **≤ EXCLUDE_FRAC**. Pula alto se ausente (não fabricamos rosto — Lei 1). | Prova ponta-a-ponta com rosto real + air-gap. | 0 |

**Witness deste ciclo (2026-07-20):** G1..G6 **verdes**. G6 sobre `/home/ubuntu/final.mp4` (mulher de perfil, telas holográficas): detecção `sampled=3 degraded=false regions=2`, `merged frac(x=0.630,y=0.294,w=0.370,h=0.228)` → `faceCenterX=0.815` (DIREITA), `blockedNetworkRequests=[]` (offline); zona escolhida `upper-left` (cx=0.232, ESQUERDA), `faceOverlap=0.000`. **Prova ocular** (`f2-proof-face-vs-zone.png`): a caixa verde caiu **sobre olho/nariz/boca** da mulher à direita; a caixa ciano "TEXTO vai AQUI" ficou no vazio escuro à esquerda — o texto foge do rosto.

## Recovery path

| Falha | Diagnóstico | Ação exata |
|-------|-------------|------------|
| **"Failed to fetch"** no log de eval / detector nunca acha rosto. | O `executablePath` deixou de pinar o binário certo (B2), ou o Chromium do Playwright mudou de build. | Confirmar `chromium.executablePath()` aponta para um build válido; garantir `executablePath: chromium.executablePath()` no `launch` de `face-detect.ts`. Rodar o smoke — G6 deve voltar verde. **Nunca** trocar o modelo por causa disso. |
| `face-detect degraded` num corte (log `[repurpose] face-detect degraded for clip N`). | Assets ausentes (`face-assets/` incompleto), master ilegível na janela, ou browser não subiu. **O render prosseguiu** (Fatia 1). | `ls scripts/video-repurpose/face-assets/{detector.html,vision_bundle.mjs,blaze_face_short_range.tflite,wasm/vision_wasm_internal.wasm}` + `xxd -s4 -l4 …tflite` (=`TFL3`). Restaurar via `face-assets/README.md`. Rodar o smoke. |
| `face fills every readable zone` (log `faceExcludedAll`). | Rosto enorme/central cobre todas as 6 zonas. Colocou-se na menos-pior. | Aceite (raro); o corte é candidato a re-autorar `zone` explícita ou trocar `caption_style`. Registrar como evidência. |
| Cartão **sobre o rosto** apesar de `degraded:false` e `!faceExcludedAll`. | **Limite conhecido, não bug (B8):** o rosto foi **perdido** naquele instante (perfil/oclusão/pequeno) → sem região → Fatia 1 escolheu a zona calma que calhou no rosto. | Aceite best-effort. Baixar `minConfidence` (mais recall) **ou** re-autorar `zone` explícita **ou** trocar `caption_style`. Não é regressão do motor. |
| `getBlockedNetworkRequests()` ≠ `[]`. | Algo tentou http/https (foi abortado, mas tentou). | Investigar — o runtime deve ser 100% `file://`. Provavelmente um asset movido fez o loader tentar CDN. Restaurar `face-assets/` e re-vendorizar (README). |

## Success signal

**O texto pousa fora do rosto — provado OCULARMENTE por render** (Lei 1 para mídia; "detectou sem erro" não é prova). O sinal de vida é triplo: (a) o smoke `scripts/qa/smoke-face-aware-zone.ts` sai **G1..G6 verdes** com o `blockedNetworkRequests===[]` real; (b) o log operacional mostra `face-detect clip N: R region(s) … merged=(…)` quando há rosto e `degraded` quando não mediu; e (c) — o que a geometria **não** garante — o **olho** confirma, por render, que o cartão não cobre a cara. Se a geometria passar mas o olho reprovar (rosto perdido, B8), o olho vence e o corte vira evidência para calibrar `minConfidence`.

## Limite conhecido (Lei 1 — honestidade material)

- **Detecção é best-effort frontal/near-frontal (B8).** Perfil duro, oclusão, ou rosto muito pequeno/distante podem ser perdidos; a fuga de rosto é *refinamento*, não *garantia*. A união sobre 3 instantes mitiga, não elimina. Quando perde, degrada silenciosamente para a Fatia 1 (que já era o estado anterior) — nunca piora.
- **Uma zona por clipe, não por beat.** O cartão não pula de canto entre beats. A janela inteira governa por uma zona face-aware (herda a decisão da Fatia 1).
- **Rostos múltiplos:** a união de todas as caixas é proibida; se dois rostos ocupam lados opostos e sobram só zonas centrais (que não existem — a grade não tem coluna central), cai no `faceExcludedAll` (menos-pior). Cenário raro no formato talking-head 9:16.
- **Custo ~2,3 s/corte** (1ª chamada inclui launch ~1,1 s; amortizado depois). Aceitável ante os minutos de re-encode que decora; roda síncrono antes do render do corte.

## Rastreabilidade

- **BoK:** BR-VR-006 (shorts motion-graphic) · FR-VR-023 (zona por saliência) · **OTD-VR-016 FECHADA** (Fatia 2 — fuga de rosto via MediaPipe WASM in-Chromium) — `docs/bok/video-repurpose/12-amendment-motion-graphics.md`.
- **Padrões agênticos implementados** (`docs/architecture/agentic-vision.md`): #5 Tool Use (MediaPipe WASM + FFmpeg) · #11 Goal Setting & Monitoring (objetivo "o cartão foge do rosto" + smoke que mede a bbox e o overlap) · #12 Exception Handling (fail-open `degraded` + `faceExcludedAll` + telemetria) · #16 Resource-Aware (self-host US$ 0, browser cacheado/amortizado, air-gapped) · #20 Prioritization (enriquece a Fatia 1 já shipada, aditivo/reversível).
- **SOP irmão:** `docs/processes/motion-graphics-zone-saliency.md` (Fatia 1 — a base que esta fatia enriquece).
- **Runtime vendorizado:** `scripts/video-repurpose/face-assets/README.md` (proveniência + refresh).
- **Sem migration:** `zone` continua dentro do jsonb `video_renders.composition` (migration `20260624120000`) — nenhuma alteração de schema. `/security-review` incide sobre o **motor** (spawn com array; filtergraph sem dado do caller; runtime air-gapped).

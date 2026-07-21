# SOP — Zona por saliência para o motion graphics (`pickCalmestZone`) (Lei 2)

> **Feature:** eleição **server-side** da zona-âncora do cartão de motion graphics (`caption_style='motion-graphics-hero-9x16'`) — escolhe o canto/lateral **mais CALMO** do quadro 9:16 reenquadrado para que o pôster de palavra-chave aterrisse no **espaço negativo**, não sobre o sujeito. É a Opção B (single-pass, US$ 0) da decisão de design: um scorer de densidade de borda semeado por um prior determinístico, **não** composição consciente de rosto (Opção C, deferida à Fatia 2).
> **BoK SSOT:** `docs/bok/video-repurpose/12-amendment-motion-graphics.md` (Amendment 12 — FR-VR-023 §3 + Gramática de zona §4.1/§4.3 + OTD-VR-016 §5 + Pattern Conformance §7). A saliência é a **única** extensão do `segment-core` que a Amendment 12 abriu (aditiva, fail-open, reversível) — este SOP é o processo antecipado que faltava para essa automação nova (`zone-saliency.ts:33` reconhece que ele "não estava escrito ainda; não citar como se estivesse").
> **Motor:** `scripts/video-repurpose/zone-saliency.ts` → `pickCalmestZone(sourcePath, inSec, outSec)`. **Consumidor:** `scripts/video-repurpose/segment-core.ts` (`renderClip`, caminho `caption_mode==='beats'`) — a saliência roda **só** para `MOTION_GRAPHICS_STYLE`; os 7 estilos karaokê ancorados no rodapé ignoram `zone` e **nunca** pagam a sonda.

## ORO triplet
- **Operator:** MCORCH Master Execution Agent (constrói/prova); na operação, o worker `video-repurpose-bridge` executa sozinho ao renderizar um corte `motion-graphics-hero-9x16`.
- **Reviewer:** Sovereign + Vision QA **ocular por render** (Lei 1 — a medição geométrica de "calma" NÃO substitui o olho) + `/security-review` (o motor recebe caminho de arquivo → todo `spawn` recebe **array** de args, nunca string de shell; as expressões de `crop` carregam só frações fixas de zona, zero dado do caller).
- **Owner:** Sovereign. **Custo mcoCoins = 0** (`charged_mco=0` inalterado); o custo é CPU: **~0,20 s por passe de 6 zonas**, logo **~0,6 s por corte** de 3 instantes (medido neste ciclo: `elapsedMs=923 ms` num corte de 3 s a 540×960) — desprezível ante os minutos de re-encode que ele decora. O risco é **qualidade percebida do criativo publicado**, não financeiro (rail FFmpeg 100% grátis).

## Operator — manual equivalente

Hoje, para pôr o texto no vazio, o **editor humano** olha o corte reenquadrado 9:16, identifica de que lado vive o sujeito/ação e ancora o cartão no canto de **espaço negativo** oposto. O motor automatiza exatamente esse juízo de *"onde está o vazio?"* — e **só** ele: o aceite estético (o cartão está bonito e legível?) continua sendo o olho (Vision QA), não a estatística.

Para pontuar **uma** zona à mão (aqui `lower-left`, no instante `t=2.0 s`), o operador roda:

```bash
# Reenquadra 9:16 (center-crop) → recorta a zona lower-left (fração 0.375×0.24 @ 0.045,0.63)
# → edgedetect → signalstats → lê a luma média do MAPA DE BORDAS (YAVG) = proxy de AGITAÇÃO.
ffmpeg -v error -ss 2.0 -i master.mp4 \
  -vf "crop=min(iw\,ih*0.5625):min(ih\,iw/0.5625):(iw-ow)/2:(ih-oh)/2,scale=540:960:force_original_aspect_ratio=increase,crop=540:960,setsar=1,crop=iw*0.375:ih*0.24:iw*0.045:ih*0.63,edgedetect,signalstats,metadata=print" \
  -f null -
# Lê YAVG: quanto MENOR, mais CALMA a zona. Repete para as 6 zonas seguras; a de menor
# max-YAVG (sobre start/mid/end) vence. Empate (dentro de ~0.5) → cai na PREFERENCE (banda de baixo primeiro).
```

O motor faz as 6 zonas × até 3 instantes num único `filter_complex` por instante (`split=6` + 6 cadeias `crop→edgedetect→signalstats→metadata`), lê o `YAVG` de cada arquivo e escolhe — determinístico, sem IA, sem download de modelo.

## Achados materiais que definem o veredito (não re-derivar)

| # | Achado | Consequência de design |
|---|--------|------------------------|
| A1 | **Densidade de borda (`edgedetect`→`YAVG`) é o proxy escolhido de agitação**, medido barato (`~0,20 s` por passe de 6 zonas). Zona lisa/uniforme → `YAVG≈0`; zona com detalhe/movimento → `YAVG` alto. | Escolher a zona de **menor** `YAVG` = mais espaço negativo. Prova ocular deste ciclo: sujeito (barras `testsrc2`) à direita → `pick.zone=lower-left`; espelhado → `lower-right`; cartão pousou no vazio nas duas. |
| A2 | **O PIOR instante governa (temporal MAX).** A footage fica ocupada de forma intermitente; amostrar só um frame elegeria uma zona que fica calma **por um átimo**. | `pickCalmestZone` amostra `start / mid / end` (`sampleTimes`, até 3, clamp 1..3) e toma o **MAX** do `YAVG` por zona (`maxAgitation`). Um cartão nunca pousa onde a footage é brevemente calma mas depois enche. |
| A3 | **Coluna central é estruturalmente excluída.** O sujeito vive quase sempre na faixa central 9:16. | A grade é **2 colunas** com um **CENTER GUTTER largo `[0.42,0.58]`** (`COL_LEFT_X=0.045`, `COL_RIGHT_X=0.58`) — a "banda vertical". `center-stack` existe no template como superset, mas **NÃO é elegível por saliência** (§4.1 da Amendment 12). |
| A4 | **Empate por float é ruído sub-perceptual.** Duas zonas com `YAVG` quase idêntico não têm diferença visível de calma. | `CALM_EPS=0.5` **bucketiza** o score; zonas na mesma faixa deferem à `PREFERENCE` (transitivo). Sem isso, o motor "caçaria" flutuação de decoder e a zona pularia entre renders equivalentes. |
| A5 | **A saliência é COSMÉTICA — nunca pode derrubar um render.** Um cartão num canto um pouco mais ocupado é uma falha muito mais barata que um re-encode multi-minuto abortado. | Contrato **fail-open** (`zone-saliency.ts:246` — "NEVER throws"): fonte ausente / FFmpeg ausente / zona sem leitura → `defaultPick` = `lower-left`, `degraded:true`. O `segment-core` embrulha a chamada em `try/catch` **e** loga o `degraded` — falha silenciosa é a classe de falso-sucesso que este projeto já levou (`segment-core.ts:133-146`). |
| A6 | **Viés de banda deliberado.** A ordem de desempate não é arbitrária. | `PREFERENCE = [lower-*, mid-*, upper-*]` (banda de baixo primeiro): é o terço convencional de legenda e o **menos** provável de cobrir um rosto (que costuma sentar no terço superior/central). `DEFAULT_ZONE = lower-left` é também o fail-open. |

## Sequence — os passos de `pickCalmestZone` (cada um com critério material)

| # | Passo | Executor | Sucesso material |
|---|-------|----------|------------------|
| 0 | O `segment-core` só chama a sonda quando `resolveCaptionStyle(clip.caption_style) === MOTION_GRAPHICS_STYLE`. Os outros estilos mantêm os `beats` sem `zone` e **não** pagam a sonda. | `segment-core.ts:128` | estilo karaokê → nenhum `spawn` de saliência (0 custo). |
| 1 | **Existência da fonte:** `existsSync(sourcePath)` falso → `defaultPick` imediato (fail-open A5). | `pickCalmestZone` | caminho existe em disco, senão `degraded:true` sem `spawn`. |
| 2 | **Instantes de amostra:** `sampleTimes(inSec, outSec, count)` → `start / mid / end` (fim empurrado `nudge` para dentro da janela), dedupe de instantes < 0,02 s (janela minúscula colapsa mid/end nas pontas). | `sampleTimes` | 1..3 instantes finitos dentro de `[inSec, outSec]`. |
| 3 | **Grade de 6 zonas candidatas:** 2 colunas × 3 linhas dentro da safe-area (laterais ~4,5%, topo ~7%, base ~13%), center gutter `[0.42,0.58]`. Cada célula 0,375×0,24 do canvas (405×461 px @ 1080×1920 — acima do `MIN_ZONE_*`, logo o cartão de 2 níveis sempre cabe). | `ZONE_RECTS` | 6 rects fixos; nenhuma na coluna central. |
| 4 | **Passe FFmpeg por instante:** `[0:v] reframe 9:16 → select=eq(n\,0) → split=6 → (por zona) crop→edgedetect→signalstats→metadata=print:file=<zona>`. Reframe **espelha** o `reframeChain` do `segment-core` (as zonas alinham com os pixels que o render vai sobrepor). | `buildPassArgs` + `runFfmpeg` | `exit 0`; um arquivo `YAVG` por zona escrito no `metaDir` (tmp). Fail-soft por instante: `exit≠0` → pula o instante, outros ainda contam. |
| 5 | **Leitura + agregação temporal:** `readYavg` parseia o `YAVG` (MAX-robusto) de cada arquivo; `maxAgitation[zone] = max(anteriores, atual)` — o **PIOR instante governa** (A2). | `readYavg` | cada zona lida ganha um `YAVG` finito ≥ 0. |
| 6 | **Filtro de elegibilidade:** só zonas que (a) tiveram leitura **e** (b) cabem o cartão (`zoneFits` ≥ `MIN_ZONE_W_FRAC`/`_H_FRAC`) entram. Nenhuma elegível → `defaultPick` (A5). | `pickCalmestZone` | `selectable.length > 0`, senão `degraded:true`. |
| 7 | **Escolha da mais calma + viés de banda:** ordena por `round(YAVG/CALM_EPS)` asc; empate na mesma faixa → `PREF_INDEX` (banda de baixo primeiro, A6). `scores[0]` é a escolhida. | `pickCalmestZone` | `zone`/`rect`/`scores[]` ranqueados, `degraded:false`, `elapsedMs` medido. |
| 8 | **Injeção no beat:** o `segment-core` carimba `zone` em **cada** beat (`beatProps = beats.map(b => ({...b, zone}))`) + carrega o `zone` de topo. Uma zona calma governa a janela inteira do clipe (Fatia 1 — zoneamento por-beat/face-aware é a Fatia 2). O template lê `b.zone` e coerça zona inválida para `'lower-left'` (allowlist fechada no template). | `segment-core.ts:150` | props do render carregam a zona eleita; `renderAlphaFrames` produz o PNG RGBA no canto certo. |

## Verification gates

Anticorpo re-executável: **`scripts/qa/smoke-zone-saliency.ts`** (zero-custo, hermético, offline — sintetiza fixtures com `ffmpeg lavfi`: uma metade `color=gray` calma + uma metade `testsrc` ocupada, resposta correta conhecida a priori; **nunca** toca um master real, a rede ou o DB). **Rodar antes de mexer na grade de zonas, na métrica de agitação ou nas partições de amostra.**

| Gate | O que prova |
|------|-------------|
| **G1 — sujeito à DIREITA → zona à ESQUERDA.** | Detalhe (`testsrc`) na metade direita sobre metade esquerda lisa ⇒ `!degraded && centerX(rect) < 0.5 && scores.length === 6`. A métrica de agitação de fato encontra o lado calmo. (Prova ocular deste ciclo: `pick.zone=lower-left`, cartão "O PONTO É [FOCO]" pousou sobre o vazio à esquerda.) |
| **G2 — sujeito à ESQUERDA → zona à DIREITA.** | O espelho de G1: `centerX(rect) > 0.5`. Prova que a escolha **segue o sujeito**, não um viés fixo de lado. (Ocular: `pick.zone=lower-right`, cartão à direita, `FOCO` sobre o vazio.) |
| **G3 — fail-open em fonte inexistente.** | Caminho para arquivo inexistente ⇒ `degraded===true && zone===DEFAULT_ZONE` (`lower-left`) **e NÃO lança**. Prova o contrato A5: a escolha cosmética nunca derruba um render. |
| **G4 — custo por corte medido (< ~2 s).** | Lê o `elapsedMs` **real** dos picks de G1/G2 (Lei 1 — o custo verdadeiro, não estimado) e afirma `< 2000 ms`. Prova que a sonda fica dentro do orçamento 0,3–0,9 s/corte que justifica rodá-la síncrona antes de cada render. |

**Custo material:** rail grátis preservado — `charged_mco=0`, US$ 0. Nenhuma migration, nenhum `/security-review` de banco (`zone` é campo dentro do jsonb `video_renders.composition` já existente — migration `20260624120000`); o `/security-review` incide sobre o **motor** (spawn com array, filtergraph sem dado do caller).

## Recovery path

| Falha | Diagnóstico | Ação exata |
|-------|-------------|------------|
| `degraded:true` num corte (log `[repurpose] zone-saliency degraded for clip N — probe did not measure, using default zone 'lower-left'`). | FFmpeg/`edgedetect` ausente no host, master ilegível na janela, ou nenhuma zona rendeu leitura. **O render prosseguiu** (fail-open) — a única perda é a inteligência de posição. | `which ffmpeg` + `ffmpeg -filters | grep edgedetect` no host do worker. Rodar `smoke-zone-saliency.ts` — se ele passar, o host está são e o problema é a fonte daquele corte (checar a janela do clipe com o decode-probe: `docs/processes/video-repurpose-source-probe.md`). **Nunca** tratar `degraded` como erro de render — é telemetria de qualidade, não caminho de falha. |
| `pickCalmestZone threw` (log `[repurpose] zone-saliency threw for clip N (kept default 'lower-left')`). | Falha **inesperada** — o contrato é no-throw; chegar aqui é bug do motor, não da fonte. O `try/catch` do `segment-core` manteve o `DEFAULT_ZONE`. | Reproduzir com o master + janela reais num driver de scratchpad (molde: importar `pickCalmestZone` e olhar `pick`); corrigir o motor; re-rodar o smoke. O render **não** precisa esperar o fix (fail-open já cobriu). |
| Cartão pousou **sobre o sujeito** apesar de `degraded:false`. | **Limite conhecido, não bug** (ver abaixo): a zona estatisticamente mais calma coincidiu com o rosto porque o fundo atrás do rosto era liso/claro (baixa densidade de borda). A saliência mede calma, não rosto. | Aceite Fatia 1: re-autorar o cut-spec com `zone` explícita (superset), **ou** trocar o `caption_style` do corte, **ou** escalar para o gatilho da Fatia 2 (OTD-VR-016). Registrar o corte como evidência para o gatilho volume/qualidade. |

## Success signal

**O texto pousa no vazio — provado OCULARMENTE por render** (Lei 1 para mídia; "renderizou sem erro" não é prova). Neste ciclo, dois renders compostos (cartão alpha `motion-graphics-hero-9x16` sobre footage 9:16 com sujeito num lado):

- **Sujeito à DIREITA** → `pick.zone=lower-left`, `degraded=false`, `elapsedMs=923` → cartão "O PONTO É [FOCO]" (kicker branco + hero ciano `#22D3EE` + colchetes arquiteturais) pousou **inteiro sobre a metade escura calma à esquerda**, sem colidir com as barras de cor à direita.
- **Sujeito à ESQUERDA** → `pick.zone=lower-right`, `degraded=false` → cartão espelhado (alinhado à direita) com `FOCO` sobre **o vazio escuro à direita**, o sujeito à esquerda intacto.

O sinal de que o SOP está vivo é duplo: (a) o smoke `scripts/qa/smoke-zone-saliency.ts` sai **G1..G4 verdes** com o `elapsedMs` real reportado; e (b) — o que a estatística **não** garante — o **olho** confirma, por render, que o cartão não cobre o sujeito. Se algum dia a métrica passar mas o olho reprovar, o olho vence (é a Fatia 2 batendo à porta).

## Notas de design

- **Por que Opção B (saliência US$ 0) e não Opção C (MediaPipe face-aware) agora:** shipar o zero-custo primeiro (Padrão 20 Prioritization) e só pagar a complexidade do face-detection quando a aproximação da Fatia 1 **provar-se insuficiente** por evidência (não por suposição). A Opção C está registrada como OTD-VR-016, não descartada.
- **Uma zona por clipe, não por beat:** o cartão **não** pula de canto entre beats — pular seria ruído visual. A janela inteira do corte governa por uma zona (Fatia 1). Re-eleger por janela de beat é refinamento possível, fora do escopo.
- **Reframe do motor ESPELHA o do `segment-core`** (`reframeChain` idêntico) — sem isso, as zonas pontuariam pixels que o render não sobrepõe, e a escolha seria contra o quadro errado.
- **`stderr`/`exit` por instante é fail-soft, não fail-hard:** um instante que falha é pulado; os outros ainda votam. Só a ausência **total** de leitura cai no default. Diferente do decode-probe (`source-probe.md`), onde `stderr` não-vazio é veredito de **falha** — lá a integridade é load-bearing; aqui a posição é cosmética.

## Limite conhecido (Lei 1 — honestidade material)

**Saliência mede CALMA, não ROSTO.** `edgedetect→YAVG` é um *proxy* de espaço negativo por densidade de borda. Um fundo liso e claro atrás de um rosto lê como **"calmo"** mesmo com o rosto ali; um cartão pode aterrissar sobre um rosto se essa for a zona estatisticamente mais calma. A Fatia 1 aceita conscientemente essa aproximação zero-custo. A **prova de fuga-de-rosto** — bounding box real do rosto → cartão na metade oposta — é a **Fatia 2 (OTD-VR-016)**: MediaPipe FaceDetection WASM rodando **dentro do Chromium** do render, self-hosted US$ 0 (NÃO Vision MCP, NÃO Adobe pago), **DEFERIDA e gated**. Ela acopla ao rail frames-in-browser (OTD-VR-014 Saída b) — é mudança de rail, não ajuste de motor — e só volta à mesa quando Vision QA (ou métrica de criativo) constatar que a zona calma da Fatia 1 aterrissa texto sobre rostos numa taxa que fere a qualidade percebida, OU quando o volume tornar a inspeção ocular por corte inviável. Enquanto DEFERIDA, `pickCalmestZone` **não** injeta frames no browser, **não** roda MediaPipe e **não** faz composição dividida — ele posiciona por zona calma e ponto.

## Rastreabilidade

- **BoK:** BR-VR-006 (shorts motion-graphic) · FR-VR-023 (zona por saliência, Opção B US$ 0) · Gramática §4.1/§4.3 · Amendment 12 §7 (Pattern Conformance) — `docs/bok/video-repurpose/12-amendment-motion-graphics.md`.
- **Padrões agênticos implementados:** #5 Tool Use (reusa `signalstats`/`edgedetect` FFmpeg) · #11 Goal Setting & Monitoring (objetivo "o cartão pousa na zona mais calma" + smoke que mede) · #12 Exception Handling (fail-open `lower-left` + telemetria `degraded`) · #16 Resource-Aware (Opção B US$ 0 sobre a Opção C paga) · #20 Prioritization (Fatia 1 antes da Fatia 2) — `docs/architecture/agentic-vision.md`.
- **OTD aberta:** **OTD-VR-016** (Fatia 2 — composição dividida consciente do rosto via MediaPipe WASM in-Chromium; DEFERIDA, gated).
- **OTDs relacionadas:** OTD-VR-014 (frames-in-browser — o veículo técnico da Fatia 2) · OTD-VR-015 (legibilidade adaptativa ao fundo).
- **Sem migration:** `zone` é campo dentro do jsonb existente `video_renders.composition` (migration `20260624120000`) — nenhuma alteração de schema disparada por esta feature.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

# SOP — Cena Motion com camadas raster ("MONTAR, não desenhar")

> **Lei 2 (Processo Antecipado).** Fonte da Verdade: `docs/bok/spaces-evolution/43-amendment-motion-montar-camadas.md`
> (FR-SPACES-164..175). Este SOP descreve o processo HUMANO de produzir uma cena montada — o mesmo
> que o motor executa. Se o operador não consegue fazer isto à mão sem errar, o motor também não.

**ORO** — Operator: diretor de arte / creative-director (ou o Sovereign) · Reviewer: Sovereign ·
Owner: engineer-spaces (o rail) + creative-director (a peça).

---

## 0. O que este processo entrega

Um MP4 1920×1080 (ou 1080×1920) em que **peças prontas** — screenshot, arte gerada, recorte com
alpha — são **montadas** num espaço 3D com câmera, parallax por geometria e profundidade de campo.
Custo: **0 mco de render, US$ 0** (Chromium + FFmpeg no host). O que custa são as **peças**, que
nascem em outros nós (`generateImage` = 20 mco) ou vêm de fora (upload/screenshot = 0).

Não substitui o Veo: Veo entrega fotorrealismo generativo; MONTAR entrega dado, UI, marca e ritmo,
de forma **determinística** (mesma spec ⇒ mesmo pixel) e dirigível quadro a quadro.

## 1. Operator — quem executa manualmente hoje

| Papel | Ferramenta |
|---|---|
| Diretor de arte | `/dashboard/spaces/<id>` → nó **Cena Motion** → seção "Camadas de imagem" |
| Engenheiro (QA/depuração) | `bun run scripts/qa/preview-motion-scene.ts <project> <node> <t...>` |
| Worker (automação) | `motion-bridge.service` (systemd --user), engine `motion` da fila `video_renders` |

## 2. Sequence — a ordem, com critério material de sucesso em cada passo

1. **Ter a peça no acervo.** A camada aponta para um asset de `creative_assets` com `kind='image'`,
   do próprio dono. Se a peça não existe: gerar (nó de imagem), subir (Biblioteca) ou recortar
   (passo 2). *Sucesso:* o asset aparece no seletor "Adicionar imagem".
2. **(Opcional) Recortar com alpha.** `python3 scripts/motion/layered/matte.py <modelo.onnx> <in> <out.png> [--stroke 4]`
   com os modelos em `/home/ubuntu/.mcorch/motion-models/`. *Sucesso:* o log imprime
   `semi=<n>` > 0 e o PNG abre em modo `RGBA`. **Limite honesto:** o grafo do u2net infere em
   320×320 fixo ⇒ franja de 5–8 px em qualquer resolução. O `--stroke` (contorno branco de papel)
   **encobre** essa franja — é o que o próprio `matte.py:56-58` documenta ("hides matting fuzz by
   design"), e é a estética da referência do Sovereign. Não é enfeite, é curativo assumido.
3. **Declarar cada camada** no inspector, em vocabulário FECHADO:
   `plano` ∈ {fundo, meio, frente} · `lado` ∈ {esq, centro, dir} · `tratamento` ∈ {laje, recorte} ·
   `tamanho` ∈ [0,40 … 1,80]. Máximo **4 camadas** (o render é serial no host).
   *Sucesso:* cada linha mostra a miniatura REAL da peça (não um uuid).
4. **Escolher a câmera** — `aproxima` (dolly in, padrão) · `afasta` · `fixa`. Uma curva monótona
   consumida por TODOS os planos: o parallax é consequência da geometria, nunca N translações.
5. **Ver antes de enfileirar.** `preview-motion-scene.ts` baixa as MESMAS peças e usa o MESMO motor.
   *Sucesso:* o PNG do preview mostra as camadas montadas. **Este passo é o que pega o que teste
   nenhum pega** (enquadramento, colisão, foco).
6. **Renderizar.** Botão "Renderizar animação" → `motion-render` → 202 `queued` → worker.
   *Sucesso:* `video_renders.state='done'` com `qa.layers = <nº de camadas>` e `storage_key` sob
   `<uid>/motion/`.
7. **Olhar o arquivo.** Extrair 2-3 frames (`ffmpeg -ss <t> -frames:v 1`) e **ver com os olhos**.
   Nenhuma cena é declarada pronta sem Vision QA ocular.

## 3. Verification gates

| Gate | Como se prova | Falha significa |
|---|---|---|
| **G1 — a peça é do dono** | 422 `layer_not_found` para asset de outro tenant | vazamento cross-tenant |
| **G2 — a peça é imagem** | 422 `layer_not_found` para asset `kind='video'` | o worker baixaria um MP4 como `<img>` |
| **G3 — camada sem id** | 422 `layer_invalid` | camada fantasma renderizando vazio |
| **G4 — teto de 4** | 422 `too_many_layers` | orçamento de relógio do worker estourado |
| **G5 — o download falhou** | o render termina `failed` com "camada N não baixou" | frames furados com job `done` |
| **G6 — a imagem não decodificou** | `window.__fatal` no template → `render-frames.mjs` aborta | idem, pelo lado do browser |
| **G7 — a perspectiva é real** | razão borda-esq/borda-dir ≠ 1,0000 no DOM | `transform-style` achatado (retângulo) |
| **G8 — determinismo** | `buildSceneHtml(spec)` byte-idêntico entre chamadas | `Math.random` infiltrado |

Automatizados em `src/test/motion-raster-layers.test.ts` (G7/G8 + a invariante de câmera) e no
witness E2E (G1-G6). **G7 tem uma armadilha específica:** `getComputedStyle().transformStyle`
reporta o valor *especificado* e continua dizendo `preserve-3d` mesmo quando o valor *usado* é
`flat`. A única prova é **medir a caixa projetada** — marcadores 0×0 nos cantos e comparar as
alturas das bordas.

## 4. Recovery path — falha no passo N

| Sintoma | Causa provável | Ação exata |
|---|---|---|
| 422 `layer_not_found` | asset apagado / de outro tenant / `kind≠image` | reescolher a peça no seletor |
| `failed`: "camada N não baixou" | objeto sumiu do Storage entre o enfileiramento e o claim | re-selecionar a peça e renderizar de novo |
| `failed`: "não é uma imagem reconhecida" | arquivo corrompido ou formato exótico (SVG/AVIF) | converter para PNG/JPEG e re-registrar |
| `failed`: "cena inválida: camada nao carregou" | o arquivo baixou mas não decodifica | mesmo caminho acima |
| render passa do orçamento | camadas grandes demais / cena longa | reduzir `tamanho`, cortar camadas, encurtar a cena |
| peça fora do quadro | `lado` extremo num plano `frente` (que magnifica ~1,2×) | mudar para `centro` ou reduzir `tamanho` |

Timeout do passo de frames: `FRAME_BUDGET_MS` em `scripts/motion-bridge.ts` (2,5× o ms/frame
MEDIDO). Depois do teto, o job morre e o reaper devolve à fila — **não** reprocessa em silêncio.

## 5. Success signal (materialmente observável)

`video_renders.state='done'` **E** `qa.layers = <nº declarado>` **E** um asset novo em
`creative_assets` com `metadata.motion.layers = <nº>` **E** o frame extraído mostrando as peças
montadas em profundidade. Os quatro juntos; três não bastam (o quarto é o único que prova o pixel).

## 6. Custos medidos (nesta máquina, 2026-08-06)

| Item | Medida |
|---|---|
| Cena SEM camadas | 453 ms/frame (1920×1080, jpeg q100) |
| Cena com **3 camadas** | 497 ms/frame (**+10%**) |
| Render de 9 s / 270 frames | 2 min 59 s de relógio, MP4 4,4 MB |
| Custo em mco | **0** (o rail `motion` é `charged_mco:0`) |
| Custo das peças | `generateImage` = 20 mco cada · upload/screenshot/matte = 0 |

A lei de custo do motor é **ÁREA de superfície composta**, não "efeito": 3 camadas custam +44 ms/f
porque somam superfície, e não porque têm blur (todos os blurs somados dão ±30 ms).

## 7. Limites que este processo NÃO resolve (declarados, não escondidos)

- **Franja do matte** — 320×320 fixo no grafo do u2net. O `isnet-general-use` aceitaria 1024×1024
  se o grafo for dinâmico (`matte.py:26`): **NÃO VERIFICADO**, e a prova custa 30 s.
- **Proveniência das peças do spike** — os assets em `repurpose-inbox/ada39fae-motion-spike/assets/`
  e os `.onnx` não têm fonte/licença registrada. Peça sem procedência não vai para peça publicada.
- **Sem legenda/scrim próprio das camadas** — com texto do HUD sobre uma laje clara, o contraste é
  responsabilidade da composição (mudar `lado`/`tamanho`), não do motor.
- **O agente de chat ainda não escolhe peças** — `spaces-agent-chat` pode ajustar `camera` via
  `data_patch`, mas não tem ferramenta para LISTAR assets, então não monta camadas sozinho.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

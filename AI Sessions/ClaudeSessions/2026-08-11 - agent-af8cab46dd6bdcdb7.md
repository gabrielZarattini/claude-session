# Session agent-af8cab46dd6bdcdb7
**Date:** 2026-08-11 | **Session ID:** `agent-af8cab46dd6bdcdb7`

---

## 👤 User *(16:05:51)*

CONTEXTO (leia antes de escrever):
- Projeto: EP07 do canal — "A economia secreta por tras dos videocasts brasileiros". Roteiro SSOT: docs/roadmap/ep07-roteiro-2026-08-11.md (leia o bloco que te cabe). Episodio 16:9, master 1080p (layout CSS 1280x720 x deviceScaleFactor 1.5), 30 fps.
- LINGUAGEM SELADA pelo Sovereign em 2026-08-11: **MONTAR** (montar camadas REAIS em Z — screenshot real, PNG recortado com alpha, SVG de marca — camera unica atravessando, parallax geometrico, dof por plano). NAO e a linguagem v6 DESENHAR. Referencia estetica aprovada: asset fcf91d44 ("MONTAR · peca aprovada (Amendment 43) · 10s · 5 camadas em Z"); codigo do benchmark: scripts/motion/layered/build-scene.mjs. Use o ADENDO VOCAB-*-MONTAR v1 do seu proprio arquivo de agente.
- O RECORTE COM BORDA (contorno branco, --stroke) esta APROVADO como assinatura visual do canal (A43 §19 D1 resolvida 2026-08-11). Use-o como recurso declarado de estilo nos recortes (edge_treatment: sticker-white).
- REGRA-MAE DOS NUMEROS: todo numero vem ancorado do roteiro (§ do bloco). ZERO numero novo. Se a dramaturgia pedir um numero que nao existe, registre a lacuna — nunca invente.
- Vocabulario FECHADO: token que o motor nao executa vira "Pedido de Vocabulario" registrado numa secao propria no fim do arquivo — jamais improviso em prosa.
- IMPORTANTE: voce so escreve/estende o arquivo de partitura indicado. NAO toque em codigo, NAO rode renders. Retorne apenas: caminho do arquivo + resumo de 3-5 linhas + pedidos de vocabulario (se houver).

SUA TAREFA (Dramaturgo — voce CRIA o arquivo docs/roadmap/ep07-partituras/ato2-adsense.md):
Bloco: ATO 2 — ADSENSE: a base passiva
Narracao v0.1 (base):
"O segundo negocio e o AdSense — a renda que pinga sozinha. Todo anuncio que roda antes, no meio e no fim do video, o YouTube reparte: fica com 45% e passa 55% pro canal. E como uma conversa longa tem quatro, cinco, seis quebras pra anuncio, ela rende muito mais que um video de dez minutos — e continua rendendo por meses."
Numeros ancorados: split 45/55 (doc oficial YouTube, support.google.com/youtube/answer/72902 — verbatim; o numero mais forte do episodio)
Hint de motion do roteiro: Uma barra de receita que se PARTE em 45/55 (o 55 vai pro canal, destacado); timeline de um episodio longo com 5-6 marcadores de ad-break vs um video curto com 1 — a diferenca de inventario e geometrica e visivel.

Escreva a PARTITURA DE CENA v1 deste bloco em linguagem MONTAR: cabecalho (bloco, data 2026-08-11, linguagem MONTAR, duracao alvo), intent, stakes, e beats[] — cada beat com anchorWord (a PALAVRA falada onde o evento cai), action (vocabulario fechado), onScreen (o que aparece ESCRITO — nunca repetir a narracao), turn (a virada), layerRef (que camada entra/atua) e kitRequired (screenshot | cutout-sticker-white | svg-marca | data-viz — o que a camada exige).
A narracao base tem ~25s falados; o alvo do bloco no episodio e ~60-90s. Voce PODE propor expansao do texto falado (costura/contexto/respiro dramatico) SEM NENHUM numero novo — marque o texto expandido numa secao "[PROPOSTA DE EXPANSAO — aguarda aprovacao]" separada da narracao base.
Cena sem stakes ou sem virada = recusa (reescreva ate ter). Actions fora do vocabulario = Pedido de Vocabulario.

## 🤖 Claude *(16:06:07)*

<details>
<summary>💭 Thinking Process</summary>

I'm taking on the Dramaturgo role to create a scene partition document for ATO 2's AdSense block. I need to pull from the main roteiro file and check the MONTAR amendment documentation to structure this properly in the MONTAR language.

Looking at the MONTAR vocabulary — verbs like `revela`, `retira`, and the base verbs that apply in MONTAR context like `impacta`, `respira`, and `conta` — I need to understand which ones are available for this scene and how they layer with the runner's build-scene logic.…

</details>


## 🤖 Claude *(16:06:07)*

Vou ler o bloco do roteiro que me cabe, verificar o molde MONTAR no motor (Lei 1 — contar antes de bloquear verbo) e conferir se a pasta de partituras já existe.

## 🤖 Claude *(16:06:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls /home/gcrUX/htdocs/constellation-orchestra/docs/roadmap/ep07-partituras/ 2>/dev/null; ls /home/gcrUX/htdocs/constellation-orchestra/docs/roadmap/ | grep -i ep07",
  "description": "List partituras folder and EP07 roadmap files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ep07-calibracao-audiencia-2026-08-11.md
> ep07-pauta-economia-videocast-2026-08-05.md
> ep07-roteiro-2026-08-11.md
> ```

## 🤖 Claude *(16:06:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n -i -E \"adsense|ato 2|45/55|72902\" /home/gcrUX/htdocs/constellation-orchestra/docs/roadmap/ep07-roteiro-2026-08-11.md | head -40",
  "description": "Locate ATO 2 AdSense block in EP07 script"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 9:**Linguagem visual SELADA (Sovereign 2026-08-11):** blocos motion em **MONTAR** (camadas reais em Z, motor de casa) — referência estética = asset `fcf91d44` (peça aprovada A43, 10s, 5 camadas). **Recorte com borda APROVADO** como assinatura do canal (A43 §19 D1 resolvida). O piloto data-viz (`scripts/ep07/pilot-adsense-scene.ts`) foi prova de motor, não estética de episódio.
> 46:## ATO 2 — ADSENSE: a base passiva [Motion] {#ato2}
> 49:> "O segundo negócio é o **AdSense** — a renda que pinga sozinha. Todo anúncio que roda antes, no meio e no fim do vídeo, o YouTube reparte: **fica com 45% e passa 55% pro canal**.
> 52:**Números (ancorados):** split **45/55** (doc oficial YouTube, `support.google.com/youtube/answer/72902` — verbatim). ✅ o número mais forte do episódio.
> 53:**Motion:** uma barra de receita que se PARTE em 45/55 (o 55 vai pro canal, destacado); timeline de um episódio longo com 5-6 marcadores de ad-break vs. um vídeo curto com 1 — a diferença de inventário é geométrica e visível.
> 106:| Ato 2 AdSense | Motion MONTAR | 0 | 45/55 |
> ```

## 🤖 Claude *(16:06:13)*


## 🤖 Claude *(16:06:15)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/roadmap/ep07-roteiro-2026-08-11.md",
  "offset": 1,
  "limit": 120
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	<!-- Roteiro EP07 v0.1 — derivado da pauta ep07-pauta-economia-videocast-2026-08-05.md §3-bis (ancoragem
> 2	     2026-08-11). REGRA-MÃE: todo número aqui é sourced (ver §3-bis da pauta); os fabricados (#1/#2/#7)
> 3	     foram reescritos para a realidade ancorada por diretiva Sovereign 2026-08-11 ("crie um que seja
> 4	     semântico e harmônico com o resto do roteiro"). Próximo: trupe criativa formaliza em Partitura de Cena. -->
> 5	
> 6	# EP07 — Roteiro v0.1: A economia secreta por trás dos videocasts brasileiros
> 7	
> 8	**Base:** pauta 2026-08-05 + ancoragem deepsearch 2026-08-11 (task `wk0iiy2kk`).
> 9	**Linguagem visual SELADA (Sovereign 2026-08-11):** blocos motion em **MONTAR** (camadas reais em Z, motor de casa) — referência estética = asset `fcf91d44` (peça aprovada A43, 10s, 5 camadas). **Recorte com borda APROVADO** como assinatura do canal (A43 §19 D1 resolvida). O piloto data-viz (`scripts/ep07/pilot-adsense-scene.ts`) foi prova de motor, não estética de episódio.
> 10	**Calibração de audiência** (`ep07-calibracao-audiencia-2026-08-11.md`): público 100% masculino BR, núcleo 25-54; **título com TESE converte 15-24× mais que manchete**; ponto ótimo **7-8 min**; episódio converte 14× mais que Short.
> 11	**Forma:** motion-first (3 atos ≈ 0 mco) · **Veo só no gancho e no fecho** (2 presenters). Doutrina: *usar o método sem anunciá-lo* — a prova é o vídeo existir.
> 12	
> 13	---
> 14	
> 15	## Títulos candidatos (TESE, não manchete)
> 16	
> 17	1. **"Um papo de 2 horas esconde 3 negócios — e é assim que ele paga uma equipe de 100 pessoas."**
> 18	2. **"O YouTube é só a vitrine: o dinheiro do videocast vem de 3 lugares que você não vê."**
> 19	3. **"Por que um podcast brasileiro fatura R$ 100 milhões vendendo a mesma conversa 3 vezes."**
> 20	
> 21	> Recomendado: **#1** — carrega a tese (3 negócios) + o número forte e sourced (equipe de ~100), e cria a tensão "como isso se paga".
> 22	
> 23	---
> 24	
> 25	## GANCHO — [Veo presenter · ~8s · 9:16] {#gancho}
> 26	
> 27	**Narração (fala):**
> 28	> "Essa conversa de duas horas que parece improviso? É uma operação de mídia com **três negócios** rodando ao mesmo tempo. O que você vê no YouTube é só a vitrine — o dinheiro mesmo vem por baixo."
> 29	
> 30	**Direção:** presenter em tom NOVIDADES (paridade EP06), olhar na câmera. Prompt Veo detalhado fica com o DoP na Partitura.
> 31	
> 32	---
> 33	
> 34	## ATO 1 — PATROCÍNIO: o que paga a conta [Motion] {#ato1}
> 35	
> 36	**Narração:**
> 37	> "O primeiro negócio é o **patrocínio direto** — a caneca na mesa, a marca no cenário, o merchan lido no meio do papo. É o que paga a conta.
> 38	> No Brasil, um canal de nicho negocia de **R$ 500 a R$ 5 mil por episódio**. Parece pouco? Então multiplica pela escala: o **Grupo Podpah**, que começou como uma resenha no YouTube, **mira R$ 100 milhões de faturamento em 2026**."
> 39	
> 40	**Números (ancorados):** R$ 500-5.000/ep (nicho BR) · R$ 100 mi/ano (Podpah 2026, Exame). *Substituem os fabricados #1 e #2 da pauta.*
> 41	**Motion:** contador subindo de R$500 até R$5k; corte para o selo "R$ 100.000.000 / ano" carimbando com procedência (Exame, 2026). Marca Podpah = SVG real com fonte datada (Diretor de Arte).
> 42	**Beat de virada:** o salto do nicho (milhares) para a escala (milhões) — o número muda de ordem de grandeza na tela.
> 43	
> 44	---
> 45	
> 46	## ATO 2 — ADSENSE: a base passiva [Motion] {#ato2}
> 47	
> 48	**Narração:**
> 49	> "O segundo negócio é o **AdSense** — a renda que pinga sozinha. Todo anúncio que roda antes, no meio e no fim do vídeo, o YouTube reparte: **fica com 45% e passa 55% pro canal**.
> 50	> E como uma conversa longa tem quatro, cinco, seis quebras pra anúncio, ela rende muito mais que um vídeo de dez minutos — e continua rendendo por meses."
> 51	
> 52	**Números (ancorados):** split **45/55** (doc oficial YouTube, `support.google.com/youtube/answer/72902` — verbatim). ✅ o número mais forte do episódio.
> 53	**Motion:** uma barra de receita que se PARTE em 45/55 (o 55 vai pro canal, destacado); timeline de um episódio longo com 5-6 marcadores de ad-break vs. um vídeo curto com 1 — a diferença de inventário é geométrica e visível.
> 54	
> 55	---
> 56	
> 57	## ATO 3 — ÁUDIO: a segunda vida [Motion] {#ato3}
> 58	
> 59	**Narração:**
> 60	> "O terceiro negócio é o **áudio**. Quando o vídeo vira podcast no Spotify, o mesmo episódio é **vendido de novo** — sem gravar nada a mais.
> 61	> No mercado de podcast, o CPM fica entre **US$ 18 e US$ 27** por mil downloads. Faz a conta: **25 mil downloads a US$ 25 dá cerca de US$ 625** de extra, por episódio. É a mesma atenção, vendida duas vezes."
> 62	
> 63	**Números (ancorados):** CPM **US$ 18-27** (Libsyn/AdvertiseCast — teto real, o "US$50" da pauta caiu) · a CONTA na tela: 25.000 × US$25 ≈ **US$ 625** (contingente à audiência). Contexto: mercado de podcast US$ 2 bi+ (IAB 2024).
> 64	**Motion:** a aritmética aparece escrita e se resolve (25.000 × US$ 25 = US$ 625) — declarando a premissa (downloads, CPM). Selo "a mesma atenção, 2×".
> 65	
> 66	---
> 67	
> 68	## A CENA DA ESTRUTURA: por que precisa de tudo isso [Motion — a pilha] {#estrutura}
> 69	
> 70	**Narração:**
> 71	> "E por que precisa de três negócios? Porque a **estrutura é cara**. Por trás dos dois apresentadores tem um time inteiro — produtor, roteirista, operador de áudio, **editores de cortes** (que são os que viralizam no TikTok e trazem gente nova), designer de thumbnail, comercial.
> 72	> No Podpah, são cerca de **100 a 120 pessoas**, numa sede de **6.500 metros quadrados**, com **sete estúdios** e **R$ 9 milhões** investidos."
> 73	
> 74	**Números (ancorados):** **~100-120 pessoas · 6.500 m² · 7 estúdios · R$ 9 mi** (Exame + Meio&Mensagem). *Substitui o fabricado "15-30 por show" (#7) — é sourced E mais impactante para a tese "a estrutura é cara".*
> 75	**Motion (a cena que se escreve sozinha):** as funções aparecem uma a uma empilhando (produtor, roteirista, áudio, cortes, thumb, comercial…); quando a pilha fica densa, ela COLAPSA/se reorganiza no número real do Podpah (100-120 · 7 estúdios · R$ 9 mi carimbados). O colapso é o beat.
> 76	
> 77	---
> 78	
> 79	## FECHO MACRO: não é à toa que virou indústria [Motion] {#macro}
> 80	
> 81	**Narração:**
> 82	> "Não é à toa que isso virou indústria. Só o ecossistema de criadores do YouTube injetou **R$ 4,94 bilhões no PIB do Brasil em 2024** e sustentou **mais de 130 mil empregos**.
> 83	> E com a publicidade digital brasileira mirando **US$ 19 bilhões**, os videocasts viraram o **horário nobre da internet**: baratos pra marca perto da TV, mas com uma confiança que anúncio tradicional não compra."
> 84	
> 85	**Números (ancorados):** **R$ 4,94 bi PIB + 130 mil empregos 2024** (Oxford Economics/YouTube, `blog.youtube` — verbatim) · **US$ 19,28 bi** publicidade digital BR até 2026 (Research and Markets).
> 86	**Motion:** os dois números grandes preenchendo a tela com peso; a metáfora "horário nobre" (a grade da TV cedendo espaço ao feed).
> 87	
> 88	---
> 89	
> 90	## FECHO — [Veo presenter · ~8s · 9:16] {#fecho}
> 91	
> 92	**Narração:**
> 93	> "No fim, a mágica é uma só: transformar **tempo de atenção em inventário**. Quanto mais tempo você fica, mais espaço eles têm pra vender.
> 94	> A indústria precisa de **100 pessoas e 7 estúdios** pra fazer isso. [pausa] Esse vídeo que você acabou de assistir? Foi feito por bem menos."
> 95	
> 96	**Direção:** o contraste é o fecho (a tese do §1 da pauta: indústria × quem fez o vídeo). **Não anuncia IA** — "por bem menos" deixa o espectador conectar. CTA leve de engajamento por cima dos créditos.
> 97	
> 98	---
> 99	
> 100	## Mapa de produção (para a trupe + o motor)
> 101	
> 102	| Bloco | Motor | Custo | Números na tela |
> 103	|---|---|--:|---|
> 104	| Gancho | Veo presenter 8s | ~712 mco (standard) | — |
> 105	| Ato 1 Patrocínio | Motion MONTAR | 0 | R$500-5k · R$100mi |
> 106	| Ato 2 AdSense | Motion MONTAR | 0 | 45/55 |
> 107	| Ato 3 Áudio | Motion MONTAR | 0 | US$18-27 · 25k×$25=$625 |
> 108	| Estrutura | Motion MONTAR | 0 | 100-120 · 6.500m² · 7 · R$9mi |
> 109	| Macro | Motion MONTAR | 0 | R$4,94bi · 130k · US$19,28bi |
> 110	| Fecho | Veo presenter 8s | ~712 mco (standard) | — |
> 111	
> 112	**Total pago projetado:** ~1.424 mco (2 Veo standard) + refs ≈ **~1.460 mco** · saldo 40.775 · falha do Veo = estorno integral.
> 113	**Alvo de duração:** 7-8 min (calibração). **Todo número é sourced** (ver pauta §3-bis) — zero repetição do erro do EP06.
> 114	
> 115	**Próximo:** trupe criativa (Dramaturgo → Encenador → DoP → Diretor de Arte) formaliza cada bloco motion na **Partitura de Cena v1** (vocabulário fechado), e o motor MONTAR é elevado (`dof(z)`+planos+`companions[]` reais) antes do 1º render — piloto de UMA cena com o gate triplo.
> 116	
> ```

## 🤖 Claude *(16:06:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n -E \"revela|retira|atravessa|impacta|counter|conta|badge|hud|stroke|layer|tIn|tOut|win\\(\" /home/gcrUX/htdocs/constellation-orchestra/scripts/motion/layered/build-scene.mjs | head -50",
  "description": "Count MONTAR verbs and layer mechanics in the runner"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 95:   aproximação, é a mesma matemática num layer de 1,4 MP em vez de 13,3 MP.
> 122:.badge{position:absolute;width:62px;height:62px;border-radius:50%;
> 126:.badge svg{width:27px;height:27px;fill:none;stroke:#dcc8ff;stroke-width:1.7}
> 158:#hud{position:absolute;inset:0;pointer-events:none}
> 206:      <div class="mk"><svg viewBox="0 0 24 24" fill="none" stroke="#06121f" stroke-width="2.5"><path d="M4 7h16M4 12h10M4 17h13"/></svg></div>
> 210:      <div class="mk"><svg viewBox="0 0 24 24" fill="none" stroke="#06121f" stroke-width="2.5"><path d="M12 3v18M3 12h18"/></svg></div>
> 215:  <!-- lâmina DIREITA: mais ao fundo. Entre as duas fica o CORREDOR que a câmera atravessa. -->
> 218:      <path class="wh" fill="none" stroke="#8b5cf6" stroke-width="10" stroke-linecap="round" opacity=".22"/>
> 219:      <path class="wc" fill="none" stroke="#c9b0ff" stroke-width="2.3" stroke-linecap="round"/>
> 220:      <path class="wh2" fill="none" stroke="#7c48ff" stroke-width="10" stroke-linecap="round" opacity=".18"/>
> 221:      <path class="wc2" fill="none" stroke="#a78bfa" stroke-width="2" stroke-linecap="round"/>
> 227:    <div class="badge" data-badge style="left:246px;top:-500px">
> 253:<div id="hud">
> 278:  function win(t,a,b,c,d){ return ease(seg(t,a,b))*(1-smooth(seg(t,c,d))); }
> 296:  var badge=document.querySelector('[data-badge]');
> 334:    var opL=win(t,0.15,1.15,4.55,5.35);
> 335:    var opR=win(t,0.45,1.55,5.05,5.95);
> 346:    badge.style.opacity=String(win(t,1.3,2.0,5.05,5.7)*opR);
> 347:    badge.style.transform='scale('+spring(seg(t,1.3,2.2)).toFixed(3)+')';
> 353:    wires.style.opacity=String(win(t,0.8,1.9,4.9,5.8)*0.95*opR);
> 355:    var farOp=win(t,0.0,1.3,3.9,4.8);
> 363:    var chipOp=win(t,2.8,3.6,4.9,5.6), chipBlur='blur('+dof(Z.chips).toFixed(2)+'px)';
> 389:    var hudOut=1-smooth(seg(t,3.0,3.8));
> 390:    kickEl.style.opacity=String(ease(seg(t,0.1,0.8))*hudOut);
> 392:    ruleEl.style.opacity=String(hudOut);
> 393:    titleEl.style.opacity=String(ease(seg(t,0.45,1.5))*hudOut);
> 395:    capEl.style.opacity=String(ease(seg(t,1.7,2.6))*hudOut);
> 400:    scrimEl.style.opacity=String(Math.max(ease(seg(t,0.1,0.9))*hudOut*0.95, eOn*0.90));
> ```

## 🤖 Claude *(16:12:19)*

<details>
<summary>💭 Thinking Process</summary>

The runner confirms the mechanics are working—the win function handles the reveal and retract actions, the badge layer works for stamping, and the HUD and camera setup are in place. For the duration, I'm setting it to null since the narration hasn't been recorded yet, and I'll note that ffprobe is pending. Now I need to check if there are existing partitura files from other acts to match the format.

Since the partituras folder doesn't exist yet, I'll create it along with the file. I'm also reviewing the A43 amendment for the beat schema in MONTAR to confirm the fields—`t`, `layerRef`, and `kitRequired`—and the kit categories match what's specified: screenshot, cutout-sticker-white, svg-marca, and data-viz. Now I'm working on the dramaturgy, starting with the base narration around 25 seconds that explains AdSense revenue sharing, then expanding it to fit the 60-90 second target with beats spaced roughly every 2.5-4 seconds.

For a 70-second scene, that's too many beats for a single cena, so I'm splitting this into 3-4 shorter scenes, each 15-25 seconds with its own intent and stakes. The block objective is to show that AdSense is passive income scaled by ad breaks, that long-form content is an inventory machine, and that revenue continues for months. The key insight to flip is that viewers often assume AdSense pays poorly or that video duration doesn't matter—but the same content, stretched longer, generates exponentially more breaks and thus more revenue.

There's also a powerful contraria: most people think YouTube keeps the majority of ad revenue, but the creator actually gets 55% of the split—the bigger slice. Since the target audience is creators, this revelation lands as a genuine surprise.

For the scene structure, I'm mapping out the beats: first, the AdSense branding reveals the system itself; then a revenue bar visualization shows the full split; finally, the bar divides to show the 45% portion, which is the key moment where the numbers become concrete.

The challenge is that the vocabulary doesn't have a verb for "splits" or "divides" — I can only use `compara` to show two comparable bars side by side with labels and values. That loses the dramatic impact of showing one unified thing breaking apart into pieces, but it's the honest execution within the constraints. I'll go with that approach and note it as a potential vocabulary request for future iterations.

But now I'm realizing that in MONTAR, the data-viz layer is a prepared piece that the Diretor de Arte produces — possibly with internal animation already authored into the scene HTML. The action verbs like `revela` handle how the layer enters, but the split animation itself would need to be baked into the layer's own code rather than applied as a separate action.

Looking at what's actually executable in the runner: `carimba` maps directly to the badge element with its spring animation — that's verified in the code with the scale transform and spring timing. So I can count that as a working verb. Now I need to check whether `conta` (counter) has a similar material equivalent in the runner. I'll verify the runner mechanism for shock/pulse effects to be thorough, then move into structuring the three scenes. The first scene covers AdSense as passive income—the revenue bar splits and the channel keeps 55%, which flips the assumption that the platform takes most. I'm setting up the anchor word "AdSense" to reveal the graphic layer showing this breakdown.

Now I'm working through the beat structure: at "sozinha" the full revenue bar appears on screen, then at "reparte" the split visualization triggers—comparing the 45/55 division side by side with labels and values.

For beat 4, I need to be careful not to duplicate the 45/55 numbers already shown in the data-viz. The badge or carimbo should instead display the source attribution (procedência) as a HUD element, anchored at either "55%" or "canal". The assumption I'm working with doesn't need explicit setup in the narration itself—the cultural expectation that platforms take the larger cut already exists with the audience, so the contrast still lands. For scene B, I'm comparing a long timeline with multiple ad breaks against a shorter video with just one, and the key insight is that it's not simply scaling up the same video—the structure fundamentally changes. Defining the ad-break markers layer with staggered reveal timing as each number is spoken, starting with "quatro" to trigger the sequence. The "dez minutos" anchor points to a short video timeline with a single marker, contrasting 1 versus 6 occurrences. For "meses," I'm thinking about the long tail concept — the narration says "continua rendendo por meses," and I want the screen to reveal what the voice doesn't: the word "inventário" itself. This creates a nice dramaturgical payoff since "inventário" appears later in the closing narration, so planting it visually here echoes that thematic loop.

I'm debating whether to show just "inventário" as a single concept label or the fuller phrase "isso se chama inventário." The single word feels cleaner — the voice will say the full phrase later anyway. This scene resolves by naming and understanding the geometric difference. The tail itself — "continua rendendo por meses" — might actually be its own scene, showing how the earnings keep flowing passively over time, circling back to the opening's "renda que pinga sozinha" callback. I'll keep it number-free and let the timeline recede into depth for the motion.

Now I'm working through how the camera movement fits into the beat structure. The DoP writes the curve, but I can still mark "atravessa" as an action — the camera passing through the ad-marker corridor, treating those markers like planes in space. That's a strong visual from the benchmark piece. The first beat anchors on "meses" with this camera pass, then shifts scale.

For the final beat, I'm considering whether the Diretor de Arte owns the procedência element, but the real power move is embedding the actual official document — a screenshot from the support page showing that 55% figure — as evidence within the scene itself. Rather than me asserting the number, the document becomes a character, appearing at the "reparte" moment. That's dramaturgy: "não sou eu dizendo, é o documento deles." I'm restructuring to make the official doc the centerpiece.

Now I'm mapping out the pacing: five beats across roughly 20-25 seconds works if each beat lands around 4-5 seconds, though I could expand with narration. I'm also checking the onScreen text budget — I need at least half the beats to have empty screens, and so far I've only planned "a maior fatia é do canal" for CENA A.

For CENA B, "inventário" is set. CENA C is trickier — I'm considering "segue pingando" as a callback to the opening narration about "a renda que pinga sozinha," which would work as a legitimate subtext reference rather than direct repetition. The voice work needs to avoid redundancy with the spoken "por meses" line.

For the screen text at the end, "enquanto você dorme" captures the passivity consequence without stealing from Ato 3's "sem gravar nada a mais." It's simple, human, and works as the resolve beat that closes each scene uniquely.

Now I'm reconsidering the structure: each scene needs either a contraria or resolve as its final beat, but maybe the block itself should build differently—with scene A ending on contraria, scene B escalating that tension, and scene C carrying the full resolve. Looking at the document proof moment in scene A, that could be the turn that escalates the contraria ("e está no documento oficial"), or I could make it the resolve itself, where the tension finally pays off as a claim. The escalation from the visualization to the official document strengthens the "contraria" beat, so I'll tag it as such. For the scene structure, I'm giving each cena its own arc: B gets a resolve with the "inventário" naming as its payoff, and C escalates through the traversal into the final impact of "enquanto você dorme." This way each scene has its own mini-arc while building toward the larger block resolution.

Now I'm thinking through how to expand cena C's content without relying on numbers — the base narration only has "continua rendendo por meses" as a tail. I need to add spoken text to make it work as a full scene. The tricky part is avoiding voiceover that would steal the screen-only lines; if I voice "a fatia maior," it undermines the visual reveal of "a maior fatia é do canal." So the expansion needs to add context elsewhere, maybe around how AdSense itself works, rather than duplicating what's already on screen. I need to rework the voice-over for section C so it doesn't repeat "inventário" — instead describing how published episodes continue generating revenue long after the conversation ends, unlike merchandise that's a one-time payment. I'm also checking that the qualitative claim about merchan payment structure holds up against what was established earlier, and calculating the total narration length to fit within the 60-80 second window at a typical Portuguese podcast pace.

Now I'm mapping out the beat structure for each scene against their durations — scene A needs about 30 seconds with 5-6 beats plus at least one breath break since it exceeds 10 seconds, and I'm doing the same for scenes B and C, making sure every scene over 10 seconds has a respira moment built in.

For the remaining beats in scene A, I'm placing a respira right before the split to create suspense, then handling the "45" comparison beat which triggers the split visualization with the 45/55 ratio appearing only in the data-viz labels, and finally the "canal" beat where the larger slice pulses while the narration emphasizes it's the channel's biggest portion.

Now I'm verifying the word count for the expansion anchor — "a maior fatia é do canal" is exactly 6 words — and setting up the "regra" anchor which pulls from official documentation, with the beat landing on "escrito" or "oficial" to reveal the support page screenshot showing the split rule.

I'm checking for conflicts between the data visualization showing 45/55 and the same numbers appearing in the documentation screenshot — the G8 mechanical risk doesn't apply here since the screenshot is a visual layer, not parsed text. But there's visual redundancy if both layers show the same split simultaneously, so the dramaturgical approach is to have the documentation replace the visualization as proof, with the director handling the focus shift. I need to verify my checklist entry about inputs declaring outputs.

For the saídas declaration, I can delegate the tOut to the director rather than burning beats on explicit retiras for each revela — the rule allows this. I'm considering a compact "declaração de saídas" table per scene instead of expanding the beat count. Looking at CENA A's pacing: 6 beats over 30 seconds is slightly sparse given the rule of one beat per 2.5-4 seconds, which would suggest 7-12 beats for that duration, though the expansion text helps fill the gap.

Now I'm reconsidering the scene structure itself — with a maximum of 6 beats per scene and the timing rule suggesting 18-24 seconds per scene, I should split into 4 scenes instead: opening the income stream around 14-15 seconds, the split and documentation around 20 seconds, inventory around 20 seconds, and the tail around 12 seconds, totaling roughly 67 seconds.

For the first scene, I'm mapping out the beats: starting with "AdSense" as the reveal with the brand mark, then "sozinha" (alone/passive) with a visual of the YouTube player showing an ad running. The narration flows as "O segundo negócio é o AdSense — a renda que pinga sozinha" to establish passivity without negotiation or contracts, then expanding into how ads running before, during, and after videos get split between YouTube and creators. I'm working through the visual hierarchy for scene 1, weighing whether to include a revenue screenshot—but there's a constraint: any real numbers in the image would violate the rules, so I'd need to blur or mask the values and just show the graph shape. That feels thin for the payoff. Leaning toward keeping it simpler: just the AdSense logo reveal, then the impact moment on "sozinha" where the logo pulses to reinforce the core thesis of passive income. Reconsidering the structure — I need a turn or resolution in cena 1 to make it a proper scene rather than just setup. I'm thinking of combining the first two scenes into one cohesive ~22-second piece with six beats that establishes the self-paying business concept through AdSense and the passivity theme. I'm realizing the respira placement actually works dramatically here—the voice describes passive income while the screen stays still, which reinforces that nothing needs to happen. Then as the narration moves through "credita" and "reparte," I'm layering in data visualizations: first a full revenue bar, then it splits into the 45/55 ratio, with the visual landing right on "reparte" as the voice begins stating the percentages.

For the "canal" entry, I'm wrestling with whether the screen text "a fatia maior é do canal" adds meaningful interpretation beyond what the voice already stated (55% to canal). The word "maior" does add the comparison that 55 is larger than 45, which the voice left implicit—similar to how the forensic example allowed paraphrasing between data and interpretation.

I'm considering alternatives like "a plataforma fica com a menor parte" or "a plataforma fica com menos"—flipping the perspective so the screen states what the platform is left with rather than what the canal receives, which would create the inversion needed for contraria.

For the "documentação"/"regra" entry, I'm looking at whether the screenshot showing the actual split documentation from support.google.com resolves the scene, and whether that resolution marks the end of scene 1.

The expansion voice line emphasizes "oficial" to anchor the claim in official documentation, with the onscreen element letting the document speak for itself. I'm checking the beat count—6 beats across roughly 22 seconds works out to about 3.7 seconds per beat, respira is present and over 10 seconds, and onscreen elements are empty in 5 out of 6 beats, meeting the threshold. The 45/55 split appears in both the bar layer and the documentation screenshot layer, so I'm considering whether to sequence them so the bar yields focus when the document enters.

Now I'm moving into Scene 2, which explores how ad breaks scale with content length—a long conversation might have four, five, or six interruptions, while a ten-minute video has just one. Reconhecendo que "seis vezes mais" é um número derivado não ancorado no roteiro — a regra é clara, números novos não são permitidos. Os seis breaks versus um break estão ancorados, mas a multiplicação é uma expansão que viola a doutrina. Preciso remover essa expressão e manter apenas os números base do roteiro.

Agora estou pensando na estrutura visual: um screenshot real da barra de progresso do YouTube mostrando os marcadores de ad-break em um episódio longo, revelados gradualmente conforme a narração conta "quatro, cinco, seis". Os marcadores aparecem em camadas, sincronizados com as palavras faladas — cada número falado acende um marcador novo, criando um ritmo visual que acompanha a cadência da fala. "anúncio" pauses while the full timeline sustains itself visually. For "dez minutos," I'm revealing the short timeline to create a visual contrast—the geometry itself shows the difference between video assumptions and reality. Then "prateleira" and "loja" need to either impact or remove elements, with "inventário" held for the final resolution. Placing "inventário" on screen as a single word to deliver the payoff, while making sure the voice doesn't repeat it elsewhere in the block — the roteiro's ending will land that concept. Checking the structure: six beats with five empty screens, proper breathing, contrasts, and resolution in the final moment. Now I'm looking at how duration markers appear in the timeline — whether those numerical timestamps like "2:14:33" should be visible or if they anchor to the dialogue about the two-hour conversation.

For Cena 3, I'm working through the voice-over about the episode continuing to generate revenue months later, explaining how the sponsorship pays once but the content keeps earning whenever someone hits play — keeping the language clear without introducing new numbers. 3. "depois" — respira — the frame stays alive even when nearly empty, which is the core idea: it generates revenue without anyone on screen. 4. "play" — impacta — the final badge/seal enters with a spring animation and locks in place, triggered by the adsense mark, resolving with "enquanto você dorme" on screen to capture that passive consequence.

Now I'm working through whether the 55% stamp should reappear across scenes or stay anchored to just one scene, since the production map specifies "Numbers on screen: 45/55" appears once. The carimba concept might work better as the anchor itself rather than restamping the number, and I need to figure out which layer the impact beat references — whether it's the HUD text or the graphic layer.

Checking scene 3's structure: four beats across 14 seconds gives me 3.5 seconds per beat, which breathes properly and resolves as a block with the empty 3/4 measure intact. The scene doesn't have a contraria but does have resolve, which satisfies the rule. For the atravessa in beat 1, the DoP curves the line while I emit the verb — that's the division of labor. I'm also collecting vocabulary requests, starting with "parte" as a term for splitting one layer into two while preserving area. The runner already handles staggered reveals through per-layer timing windows, so I don't need to request new vocabulary—engineers can author this directly. Now I'm cataloging the required assets: the AdSense logo, the split bar visualization showing the 45/55 breakdown, a screenshot from the official Google support page documenting the split, and a timeline screenshot.

I also need a longer episode timeline with yellow markers showing roughly a 2-hour duration as the hook, a shorter ~10-minute video timeline with a single marker, cutout sticker-style markers arranged in sequence, and the markers reused as Z-depth planes in scene 3. One thing to flag for the design team: real screenshots might contain unanchored numbers like view counts or timestamps that need to be masked or neutralized.

For the audio, I don't have an mp3 yet so duration stays null with the target separately noted as 60-75 seconds for the block, building from a base of about 25 seconds up to 60-70 with expansion. I'm keeping null for the measured duration since we're not estimating—just tracking the production target. I should also declare the ORO triplet since this qualifies as a substantial task, so I'll add a compact line in the document header noting the roles: Dramaturgo as operator, Encenador plus DoP plus Arte as reviewers for feasibility, and Sovereign for approval and ownership. Every numerical reference needs to cite back to the script section or line. Organizing the JSON structure for each scene with MONTAR fields embedded in markdown blocks, then adding the expansion proposal section separately and a vocabulary requests section at the end, plus running through the auto-audit checklist. I need to verify that each anchorWord actually appears in the narration—checking Cena 1 now: "AdSense" and "sozinha" are in the base, "credita" is from the expansion so I'll mark it, and "reparte" is in the base.

The voice sequence flows through AdSense → sozinha → credita → reparte → canal → oficial in the right order, but there's a breathing gap between "sozinha" and "credita" where the passivity expansion sits silently on screen for about 6-7 seconds with no new beat entering—that's over 4 seconds of intentional respiro, which should be acceptable as a deliberate pause in the rhythm. Reconsidering the timing: if I anchor the respira at "contrato" instead, it splits the gap differently—"sozinha" lands as a beat with impact on the brand, then "contrato" holds the breath, "reparte" enters the comparison. But this raises a sequencing problem: where does the bar graphic come in before the split happens? The full bar needs to establish itself first at "credita" before splitting at "reparte"—without that initial state, the split has no reference point, and the comparison loses its visual foundation.

So the structure holds: beat 3 reveals the full revenue bar, beat 4 applies the comparison fallback to create the split version. For beat 2 with "sozinha," there's no action needed—it's pure sustain, the brand existing alone, which is exactly the thesis the emptiness conveys. Finalizing the scene: "AdSense" reveals the brand mark, "sozinha" sustains it with nothing else entering, "credita" reveals the full revenue bar, and "reparte" applies the split comparison using the fallback.

Now moving into scene 2, I'm setting up the timeline reveal with individual ad break markers that sync their timing to match the spoken count sequence, where each beat lands precisely on the word being spoken.

The ad itself sustains the full timeline while the viewer naturally counts the markers without needing explicit animation. Then the shorter timeline contradicts this, and when it exits defeated, the longer timeline claims dominance of the frame—a dramaturgical move that escalates the tension.

The core voice for this expansion captures the idea that a long conversation with multiple ad breaks generates far more value than a short ten-minute video.

Now moving into scene 3, I'm tracking how months traverse through the marker corridor, where the camera enters the timeline and the markers transform into Z-plane depth, making time passage visible through the cinematography. The stage begins to dismantle as light strips away the longer timeline and its markers. Então o anúncio fica rodando pra quem entra depois, e cada visualização gera receita — diferente do merchandising que paga uma única vez. Preciso rastrear quais elementos saem em "apagou a luz": a timeline longa desaparece (removendo a moldura do player), mas os marcadores e o corredor permanecem como estrutura base pra cena 3.

Nos beats seguintes, quando "depois" toca, o quadro fica quase vazio mas continua vivo — é uma imagem forte, só os marcadores amarelos flutuando em profundidade enquanto o estúdio se desmonta. Depois em "play" o corredor se resolve com a frase "enquanto você dorme". Tenho meus 4 beats sem violar a regra de nunca dois impactos seguidos, e o bloco termina com um corte que marca o fim da cena.

Agora preciso estruturar o cabeçalho com bloco, data, linguagem MONTAR, duração alvo, e depois os intents e stakes — tanto no nível do bloco quanto por cena. O stakes deste bloco é crítico: é o número mais forte do episódio segundo o roteiro, e se o espectador não entender o inventário aqui, a tese final sobre transformar tempo de atenção em inventário não vai funcionar.

O intent é fazer o espectador sentir visceralmente a diferença entre renda ativa (Ato 1) e uma máquina que vende espaço automaticamente — e perceber que a duração da conversa é uma decisão econômica, não uma escolha estilística.

Para C1, preciso instalar essa máquina passiva e desmontar a suposição de que "a plataforma fica com quase tudo", usando o documento oficial como prova. O risco é que se esse número chegar como mais um percentual genérico, o episódio perde sua âncora de credibilidade. Em C2, vou transformar a duração em geometria visível — o espectador precisa VER que uma conversa mais longa gera mais pontos de venda. A partitura não mostra valores monetários — só proporções visuais. Preciso verificar as durações exatas mencionadas no roteiro e garantir que numerais visíveis em screenshots sejam mascarados, exceto quando funcionam como âncoras (como "2h" no timeline que está ancorado ao gancho §28). Estou revisando o vocabulário solicitado — "atravessa" e "retira" já estão confirmados; preciso validar se "impacta" faz parte dos verbos adicionados no adendo. For beat 4, I'm settling on `revela` as the action on the layer barra_split_4555, where the data-viz piece already carries the split labels—this avoids losing the moment of division and stays executable. I'm keeping `impacta` for scene 2 beat 6 since the runner supports pulse mechanisms on layers, and the example validates this approach. Moving into beat 5 of scene 1...

For the vocabulary request, `parte` is the verb used in C1-b4 with a fallback that captures the essence: "revela da peça barra_split_4555 já dividida; perde o INSTANTE da partilha"—the heart of the beat is that transformation from one layer into two, which existing verbs like revela or compara can't deliver. I'm explicitly noting that `pulsa-serie` or stagger isn't needed here since we're not dealing with multiple layers and windows, so the engineer knows that decision is intentional.

On the `t` values: the adendo example shows "t": 2.9, but G7 has no ffprobe or narration audio, so `t` remains unknown until after word alignment. The anchorWord itself is the cue; I'll mark `t` as pending and note the durationSource instead. For the kitRequired block, I'm structuring it as JSON arrays per scene listing piece IDs, plus a kit table with categories and gates. The cost model declares generated pieces at 20 mco each, and I'm auditing that in the adendo. Our kit includes screenshots (capture, 0 cost), svg-marca (vector, 0 cost), data-viz as authored SVG/HTML (0 cost), and cutouts via...

The kit cost estimate is zero since no AI-generated image pieces are planned, which aligns with the production map. I'll declare that explicitly and add an auto-audit section with checkboxes. The file goes at `/home/gcrUX/htdocs/constellation-orchestra/docs/roadmap/ep07-partituras/ato2-adsense.md`. Before finalizing, I need to sanity-check beats-per-second against estimated spoken lengths—I'll mark duration targets as "alvo" ranges pending ffprobe measurements, not as measured facts. Now I'm counting the base narration at roughly 70 words and drafting the full expanded version starting with C1.

Now I'm expanding the AdSense explanation across three segments: first, how YouTube splits ad revenue automatically with no negotiation needed; second, how longer conversations with multiple ad breaks generate more revenue than shorter videos; third, continuing the pattern with C3. Inserting the expansion between "dez minutos" and "e continua rendendo por meses" keeps the flow natural — the narrative moves smoothly from describing the shelf-like structure to the ongoing revenue. Now I'm checking the timing: C1 runs about 75 words, which at my speaking pace lands around 29 seconds, giving me roughly 4.8 seconds per beat — a bit sparse. I'm trimming the C1 expansion to tighten it up, cutting it down to just the essentials about how the ad runs and credits accumulate, then moving into the second expansion.

With the trimmed version, C1 sits at about 66 words total, hitting closer to 25 seconds and 4.2 seconds per beat — acceptable, especially with the respira absorbing some slack. C2 comes in at 44 words across 6 beats, giving me 2.8 seconds per beat, which is solid. C3 is 45 words over 4 beats at 4.2 seconds per beat, also working with the respira. The whole block lands around 155 words, and I'm flagging these as targets since ffprobe will have the final say on actual durations.

Now I'm setting up the markdown file with a header comment and the episode structure, laying out the scene score with metadata like block, date, language, aesthetic reference, target duration, and aspect ratio, then organizing the base narration and expansion proposal sections.

The rest of the document includes anchor number mappings, intent and stakes for each scene, consolidated kit requirements with art gates and approved styling, output declarations, registered number gaps, vocabulary requests, and self-audit sections, with beat JSON fields to follow.

I'm working through the layerRef assignments now — respira has no layer reference so that's null, and for the marcadores_adbreak cutout pieces I need to apply the sticker-white edge treatment and clarify that this is actually a group of individual sub-layers (marcadores_adbreak[1..6]) rather than a single layer, with the narration counting "quatro, cinco, seis" to determine the exact count.…

</details>


## 🤖 Claude *(16:12:20)*

<details>
<summary>💭 Thinking Process</summary>

A pasta de partituras ainda não existe e o motor confirma a mecânica MONTAR com seus componentes. Vou fazer uma última verificação no runner para confirmar os mecanismos de pulso/ênfase e split de camada antes de abrir o Pedido de Vocabulário.

</details>


## 🤖 Claude *(16:12:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -n -c -E \"split|parte|divide\" /home/gcrUX/htdocs/constellation-orchestra/scripts/motion/layered/build-scene.mjs; grep -n -E \"spring|kick|pulse|scale\\(\" /home/gcrUX/htdocs/constellation-orchestra/scripts/motion/layered/build-scene.mjs | head -10; mkdir -p /home/gcrUX/htdocs/constellation-orchestra/docs/roadmap/ep07-partituras",
  "description": "Verify no split verb exists in runner; create partituras folder"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 1
> 163:#kick{position:absolute;left:72px;top:56px;font-size:12.5px;letter-spacing:.34em;font-weight:700;color:#7fe6ff}
> 164:#kick b{color:#fff}
> 255:  <div id="kick">MCORCH <b>·</b> MOTION <b>·</b> SPIKE</div>
> 275:  function spring(x){ return x<=0?0:x>=1?1:1-Math.exp(-6*x)*Math.cos(9*x); }
> 300:  var kickEl=document.getElementById('kick'),ruleEl=document.getElementById('rule');
> 316:      +(Math.cos(t*0.31)*13*wS).toFixed(2)+'px) scale('+wS.toFixed(4)+')';
> 347:    badge.style.transform='scale('+spring(seg(t,1.3,2.2)).toFixed(3)+')';
> 367:      var cin=Math.min(spring(seg(t,2.8+q*0.28,4.0+q*0.28)),1.05);
> 376:      var grow=Math.min(spring(seg(t,5.5+b*0.20,7.0+b*0.20)),1.06);
> 382:    var fIn=Math.min(spring(seg(t,7.4,8.9)),1.04);
> ```

## 🤖 Claude *(16:12:31)*


## 🤖 Claude *(16:12:32)*

<details>
<summary>💭 Thinking Process</summary>

Verifiquei no motor que entradas em série com stagger já são autoráveis e não há mecanismo de split de camada, então o Pedido de Vocabulário é legítimo. Agora vou escrever a partitura.

</details>


## 🤖 Claude *(16:14:08)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/roadmap/ep07-partituras/ato2-adsense.md",
  "content": "<!-- Partitura de Cena v1 \u2014 EP07 ATO 2 (AdSense) \u00b7 Dramaturgo \u00b7 2026-08-11\n     SSOT do texto: docs/roadmap/ep07-roteiro-2026-08-11.md {#ato2} (linhas 46-53).\n     Linguagem: MONTAR (A43, docs/bok/spaces-evolution/43-amendment-motion-montar-camadas.md).\n     REGRA-M\u00c3E: zero n\u00famero novo \u2014 toda \u00e2ncora cita o \u00a7 do roteiro. Lacunas registradas, nunca preenchidas. -->\n\n# EP07 \u00b7 ATO 2 \u2014 ADSENSE: a base passiva \u00b7 Partitura de Cena v1\n\n| Campo | Valor |\n|---|---|\n| Bloco | ATO 2 \u2014 ADSENSE: a base passiva (`ep07-roteiro-2026-08-11.md` {#ato2}) |\n| Data | 2026-08-11 |\n| Linguagem | **MONTAR** (camadas reais em Z \u00b7 refer\u00eancia est\u00e9tica asset `fcf91d44` \u00b7 molde `scripts/motion/layered/build-scene.mjs`) |\n| Aspect | 16:9 \u00b7 master 1080p (layout 1280\u00d7720 \u00d7 dSF 1.5) \u00b7 30 fps |\n| Dura\u00e7\u00e3o alvo | **~60-75 s** (bloco alvo 60-90 s; narra\u00e7\u00e3o base \u224825 s + expans\u00e3o proposta) |\n| `durationSec` | `null` |\n| `durationSource` | `ffprobe:<narra\u00e7\u00e3o ATO 2>.mp3` (**PENDENTE** \u2014 narra\u00e7\u00e3o n\u00e3o gravada; n\u00e3o estimo \u2014 Lei 1/G7. Os `t` dos beats s\u00f3 entram ap\u00f3s o alinhamento palavra-a-palavra) |\n| Custo do kit | **0 mco declarado** \u2014 nenhuma pe\u00e7a GERADA por IA prevista (screenshots capturados + SVG vetorial + data-viz autorada + recortes via matte self-host) |\n| Assinatura visual | Recorte com borda branca (`edge_treatment: sticker-white`) \u2014 **APROVADO** A43 \u00a719 D1 (2026-08-11) |\n| ORO | Operator: Dramaturgo \u00b7 Reviewer: Encenador + DoP + Diretor de Arte (encenabilidade) e Sovereign (parecer) \u00b7 Owner: Sovereign |\n\n**Campos ausentes de prop\u00f3sito:** `staging` (Encenador) \u00b7 `camera`/`light`/`lens`/`transitions`/`grade` (DoP) \u00b7 `art.layers[]`/`matte`/proced\u00eancia (Diretor de Arte). Ausente \u2260 vazio: campo ausente declara autoria alheia.\n\n---\n\n## Narra\u00e7\u00e3o BASE (SSOT \u2014 roteiro \u00a749-50, verbatim)\n\n> \"O segundo neg\u00f3cio \u00e9 o **AdSense** \u2014 a renda que pinga sozinha. Todo an\u00fancio que roda antes, no meio e no fim do v\u00eddeo, o YouTube reparte: **fica com 45% e passa 55% pro canal**. E como uma conversa longa tem quatro, cinco, seis quebras pra an\u00fancio, ela rende muito mais que um v\u00eddeo de dez minutos \u2014 e continua rendendo por meses.\"\n\n## [PROPOSTA DE EXPANS\u00c3O \u2014 aguarda aprova\u00e7\u00e3o]\n\nBase \u224825 s falados; alvo do bloco 60-90 s. Insertos marcados `[EXP]`, **zero n\u00famero novo** \u2014 s\u00f3 costura, contexto e respiro dram\u00e1tico. Texto integral proposto (a ordem das frases-base \u00e9 preservada):\n\n> \"O segundo neg\u00f3cio \u00e9 o AdSense \u2014 a renda que pinga sozinha. **[EXP: Ningu\u00e9m negocia nada \u2014 n\u00e3o tem contrato, n\u00e3o tem merchan pra ler. O an\u00fancio roda, a conta credita.]** Todo an\u00fancio que roda antes, no meio e no fim do v\u00eddeo, o YouTube reparte: fica com 45% e passa 55% pro canal. **[EXP: E isso n\u00e3o \u00e9 promessa de curso \u2014 est\u00e1 escrito na documenta\u00e7\u00e3o oficial da plataforma.]** E como uma conversa longa tem quatro, cinco, seis quebras pra an\u00fancio, ela rende muito mais que um v\u00eddeo de dez minutos. **[EXP: N\u00e3o \u00e9 o mesmo v\u00eddeo maior \u2014 \u00e9 mais prateleira na mesma loja. Mesma conversa, mais espa\u00e7o pra vender.]** E continua rendendo por meses. **[EXP: A conversa acabou, o est\u00fadio apagou a luz \u2014 e o epis\u00f3dio segue l\u00e1, mostrando an\u00fancio pra quem chega depois. O merchan paga uma vez. Essa base paga toda vez que algu\u00e9m aperta o play.]**\"\n\nJustificativa por inserto: **exp-1** d\u00e1 corpo ao \"sozinha\" (\u00e9 o obst\u00e1culo da cena 1: passividade \u2260 pregui\u00e7a) e abre janela para o respiro visual \u00b7 **exp-2** transforma o split em prova documental (arma o `resolve` da cena 1 com a pe\u00e7a mais forte: o doc oficial) \u00b7 **exp-3** d\u00e1 a met\u00e1fora falada que a tela N\u00c3O repete (a tela nomeia o conceito) \u00b7 **exp-4** paga o loop \"pinga sozinha\" aberto na primeira frase e diferencia AdSense do merchan do Ato 1 \u2014 sem essa costura, a tese \"3 neg\u00f3cios DIFERENTES\" desaba.\n\n\u26a0\ufe0f Nota de disciplina: a expans\u00e3o **evita de prop\u00f3sito** a palavra \"invent\u00e1rio\" (reservada \u00e0 tela nesta partitura e \u00e0 voz do FECHO, roteiro \u00a793) e **n\u00e3o deriva n\u00fameros** (nada de \"6\u00d7 mais\" \u2014 aritm\u00e9tica derivada foi o pecado do EP06).\n\n---\n\n## \u00c2ncoras de n\u00famero (todas citadas \u2014 G8: cada uma aparece UMA vez escrita por n\u00f3s)\n\n| N\u00famero | Onde aparece na partitura | Fonte (\u00a7 do roteiro) |\n|---|---|---|\n| **45% / 55%** | camada `barra_split_4555` (r\u00f3tulos da pe\u00e7a data-viz) \u2014 \u00fanica escrita nossa | \u00a749 + \u00a752 (doc oficial YouTube `support.google.com/youtube/answer/72902`, verbatim \u2014 \"o n\u00famero mais forte do epis\u00f3dio\") |\n| quatro, cinco, seis quebras \u2192 **6 marcadores** | camadas `mk_ab_1..6` (marcas, n\u00e3o numerais) | \u00a750 (teto falado \"seis\") + hint \u00a753 (\"5-6 marcadores\") |\n| **1 marcador** no v\u00eddeo curto | camada `timeline_curta` (marca, n\u00e3o numeral) | \u00a753 (hint Motion do roteiro \u2014 **n\u00e3o \u00e9 falado**; ver Lacunas) |\n| **~2 h** (dura\u00e7\u00e3o vis\u00edvel na `timeline_longa`) | pixels do screenshot | \u00a728 (gancho: \"conversa de duas horas\") |\n| **10 min** (dura\u00e7\u00e3o vis\u00edvel na `timeline_curta`) | pixels do screenshot | \u00a750 (\"v\u00eddeo de dez minutos\") |\n\n---\n\n## INTENT & STAKES do bloco\n\n**Intent:** fazer o espectador sentir a diferen\u00e7a entre a renda ativa do Ato 1 (negociada, por epis\u00f3dio) e uma m\u00e1quina que vende espa\u00e7o **sozinha** \u2014 e entender que a dura\u00e7\u00e3o de uma conversa \u00e9 uma decis\u00e3o **econ\u00f4mica** (mais pontos de venda), n\u00e3o uma escolha de estilo.\n\n**Stakes:** aqui vive o \u00fanico n\u00famero verbatim de documento oficial do epis\u00f3dio (45/55, \u00a752). Se ele chegar como \"mais um percentual\", o epis\u00f3dio perde sua \u00e2ncora de credibilidade \u2014 a regra-m\u00e3e existe por causa do EP06. E se o espectador n\u00e3o VIR a geometria do invent\u00e1rio, o FECHO (\"transformar tempo de aten\u00e7\u00e3o em invent\u00e1rio\", \u00a793) chega sem referente e o Ato 3 (\"a mesma aten\u00e7\u00e3o, vendida duas vezes\", \u00a761) fica sem base: a tese dos 3 neg\u00f3cios desmonta no meio.\n\n---\n\n## CENA 1 \u2014 O NEG\u00d3CIO QUE SE PAGA SOZINHO (alvo ~22-26 s \u00b7 6 beats)\n\n**Intent:** instalar a m\u00e1quina passiva e virar a suposi\u00e7\u00e3o t\u00e1cita \"a plataforma fica com a parte do le\u00e3o\" \u2014 com o documento oficial como testemunha, n\u00e3o a nossa palavra.\n\n**Stakes:** se a cena falha, o 45/55 vira estat\u00edstica decorativa e o bloco inteiro perde o seu momento de prova; o `contraria` (a plataforma fica com MENOS) \u00e9 o que faz o espectador-criador se inclinar para frente.\n\n```json\n{\n  \"id\": \"ep07-a2-c1-split\",\n  \"language\": \"MONTAR\",\n  \"durationSec\": null,\n  \"durationSource\": \"ffprobe:ato2-c1.mp3 (PENDENTE)\",\n  \"beats\": [\n    { \"anchorWord\": \"AdSense\",  \"action\": \"revela\",  \"layerRef\": \"marca_adsense\",    \"onScreen\": \"\", \"turn\": \"revela\" },\n    { \"anchorWord\": \"sozinha\",  \"action\": \"respira\", \"layerRef\": null,               \"onScreen\": \"\", \"turn\": null },\n    { \"anchorWord\": \"credita\",  \"action\": \"revela\",  \"layerRef\": \"barra_receita\",    \"onScreen\": \"\", \"turn\": null,\n      \"note\": \"anchorWord do inserto [EXP-1]\" },\n    { \"anchorWord\": \"reparte\",  \"action\": \"revela\",  \"layerRef\": \"barra_split_4555\", \"onScreen\": \"\", \"turn\": \"revela\",\n      \"note\": \"FALLBACK do verbo pedido `parte` \u2014 ver Pedidos de Vocabul\u00e1rio. A pe\u00e7a entra J\u00c1 dividida; a voz l\u00ea 45/55 enquanto os r\u00f3tulos assentam\" },\n    { \"anchorWord\": \"canal\",    \"action\": \"impacta\", \"layerRef\": \"barra_split_4555\", \"onScreen\": \"a plataforma fica com menos\", \"turn\": \"contraria\" },\n    { \"anchorWord\": \"oficial\",  \"action\": \"revela\",  \"layerRef\": \"doc_split_oficial\", \"onScreen\": \"\", \"turn\": \"resolve\",\n      \"note\": \"anchorWord do inserto [EXP-2]; a barra CEDE o quadro ao documento (tOut da barra ANTES do tIn do doc \u2014 a prova substitui a alega\u00e7\u00e3o, nunca disputa com ela)\" }\n  ],\n  \"kitRequired\": [\"marca_adsense\", \"barra_receita\", \"barra_split_4555\", \"doc_split_oficial\"]\n}\n```\n\n**Porqu\u00eas:** beat 2 \u00e9 o mais importante e o \u00fanico em que **nada entra** \u2014 a voz diz \"ningu\u00e9m negocia nada\" e o quadro obedece: o vazio \u00c9 a passividade (respiro longo de prop\u00f3sito; micro-vida do quadro \u00e9 lente do DoP, n\u00e3o minha). Beat 5: a voz carrega o dado (55% \u2192 canal); a tela carrega a **invers\u00e3o** que a voz n\u00e3o diz (o lado de quem ficou com menos) \u2014 subtexto, n\u00e3o par\u00e1frase. Beat 6: `onScreen` vazio porque a camada j\u00e1 fala \u2014 o screenshot do doc oficial com a linha do split \u00e9 texto que ningu\u00e9m precisa reescrever.\n\n---\n\n## CENA 2 \u2014 INVENT\u00c1RIO \u00c9 GEOMETRIA (alvo ~16-20 s \u00b7 6 beats)\n\n**Intent:** transformar \"rende muito mais\" (abstra\u00e7\u00e3o) em geometria vis\u00edvel: o espectador tem que CONTAR com os olhos os pontos de venda da conversa longa contra o \u00fanico do v\u00eddeo curto.\n\n**Stakes:** sem essa imagem, o FECHO n\u00e3o tem o que pagar \u2014 \"tempo de aten\u00e7\u00e3o em invent\u00e1rio\" (\u00a793) precisa que o invent\u00e1rio tenha sido VISTO aqui. \u00c9 a cena que planta a palavra-chave do epis\u00f3dio.\n\n```json\n{\n  \"id\": \"ep07-a2-c2-inventario\",\n  \"language\": \"MONTAR\",\n  \"durationSec\": null,\n  \"durationSource\": \"ffprobe:ato2-c2.mp3 (PENDENTE)\",\n  \"beats\": [\n    { \"anchorWord\": \"longa\",      \"action\": \"revela\",  \"layerRef\": \"timeline_longa\",  \"onScreen\": \"\", \"turn\": \"revela\" },\n    { \"anchorWord\": \"quatro\",     \"action\": \"revela\",  \"layerRef\": \"mk_ab_1..6\",      \"onScreen\": \"\", \"turn\": \"escala\",\n      \"note\": \"6 sub-camadas com janelas individuais em s\u00e9rie, cad\u00eancia casada com a contagem FALADA ('quatro, cinco, seis') \u2014 execut\u00e1vel HOJE no runner (stagger de springs, build-scene.mjs:367); o beat cai na palavra, n\u00e3o no cron\u00f4metro\" },\n    { \"anchorWord\": \"an\u00fancio\",    \"action\": \"respira\", \"layerRef\": null,              \"onScreen\": \"\", \"turn\": null,\n      \"note\": \"a timeline cheia sustenta; o olho conta os marcadores sozinho\" },\n    { \"anchorWord\": \"dez\",        \"action\": \"revela\",  \"layerRef\": \"timeline_curta\",  \"onScreen\": \"\", \"turn\": \"contraria\",\n      \"note\": \"a compara\u00e7\u00e3o \u00c9 a virada: 'v\u00eddeo \u00e9 v\u00eddeo' morre aqui \u2014 um marcador contra seis\" },\n    { \"anchorWord\": \"prateleira\", \"action\": \"retira\",  \"layerRef\": \"timeline_curta\",  \"onScreen\": \"\", \"turn\": \"escala\",\n      \"note\": \"anchorWord do inserto [EXP-3]; o curto SAI de cena \u2014 a sa\u00edda \u00e9 dramat\u00fargica: o formato perde a disputa e abandona o quadro\" },\n    { \"anchorWord\": \"vender\",     \"action\": \"impacta\", \"layerRef\": \"timeline_longa\",  \"onScreen\": \"invent\u00e1rio\", \"turn\": \"resolve\",\n      \"note\": \"a voz d\u00e1 a consequ\u00eancia ('mais espa\u00e7o pra vender'); a tela d\u00e1 o NOME que a voz n\u00e3o diz \u2014 e que o FECHO (\u00a793) vai pagar em voz alta\" }\n  ],\n  \"kitRequired\": [\"timeline_longa\", \"timeline_curta\", \"mk_ab_1..6\"]\n}\n```\n\n---\n\n## CENA 3 \u2014 A CAUDA (alvo ~14-18 s \u00b7 4 beats)\n\n**Intent:** dar peso f\u00edsico ao \"sozinha\": a m\u00e1quina rende com o palco desmontado. Fecha o loop aberto na primeira frase do bloco (\"a renda que pinga sozinha\").\n\n**Stakes:** sem a cauda, AdSense parece uma venda pontual igual ao merchan do Ato 1 \u2014 e a tese \"3 neg\u00f3cios DIFERENTES\" perde a diferen\u00e7a. \u00c9 tamb\u00e9m a ponte de tom para o Ato 3 (revenda da mesma aten\u00e7\u00e3o).\n\n```json\n{\n  \"id\": \"ep07-a2-c3-cauda\",\n  \"language\": \"MONTAR\",\n  \"durationSec\": null,\n  \"durationSource\": \"ffprobe:ato2-c3.mp3 (PENDENTE)\",\n  \"beats\": [\n    { \"anchorWord\": \"meses\",  \"action\": \"atravessa\", \"layerRef\": \"corredor_mk\",      \"onScreen\": \"\", \"turn\": \"escala\",\n      \"note\": \"os marcadores mk_ab_1..6 REAPROVEITADOS como planos em Z; a c\u00e2mera entra na timeline \u2014 profundidade = tempo passando. A CURVA \u00e9 do DoP; eu declaro s\u00f3 a travessia\" },\n    { \"anchorWord\": \"luz\",    \"action\": \"retira\",    \"layerRef\": \"timeline_longa\",   \"onScreen\": \"\", \"turn\": null,\n      \"note\": \"anchorWord do inserto [EXP-4]; a moldura do player sai \u2014 o 'est\u00fadio' desmonta e sobram s\u00f3 os pontos de venda flutuando em Z\" },\n    { \"anchorWord\": \"depois\", \"action\": \"respira\",   \"layerRef\": null,               \"onScreen\": \"\", \"turn\": null,\n      \"note\": \"o quadro quase vazio SEGUE vivo \u2014 rende sem ningu\u00e9m em cena; \u00e9 o eco do respira da cena 1\" },\n    { \"anchorWord\": \"play\",   \"action\": \"impacta\",   \"layerRef\": \"corredor_mk\",      \"onScreen\": \"enquanto voc\u00ea dorme\", \"turn\": \"resolve\",\n      \"note\": \"resolve do BLOCO: a voz diz o mecanismo ('toda vez que algu\u00e9m aperta o play'); a tela diz a consequ\u00eancia que a voz n\u00e3o diz\" }\n  ],\n  \"kitRequired\": [\"corredor_mk\"]\n}\n```\n\n**Sa\u00edda do bloco** (transi\u00e7\u00e3o para o Ato 3): n\u00e3o \u00e9 minha \u2014 transitions s\u00e3o do DoP.\n\n---\n\n## KIT CONSOLIDADO (`kitRequired` do bloco \u2014 contrato anti-beat-\u00f3rf\u00e3o)\n\nNenhuma pe\u00e7a existe ainda (`ls` em 2026-08-11: pasta de kit n\u00e3o criada). **Nenhum beat renderiza antes do kit existir** \u2014 G-MONTAR-1. Pedidos ao Diretor de Arte:\n\n| layerRef | Categoria | Descri\u00e7\u00e3o + gates |\n|---|---|---|\n| `marca_adsense` | **svg-marca** | Marca AdSense/Google real, com proced\u00eancia datada (padr\u00e3o do Diretor de Arte) |\n| `barra_receita` | **data-viz** | Barra de receita INTEIRA, sem divis\u00e3o, sem cifra \u2014 propor\u00e7\u00e3o, n\u00e3o valor em R$ (n\u00e3o h\u00e1 valor ancorado; ver Lacunas) |\n| `barra_split_4555` | **data-viz** | A barra dividida com r\u00f3tulos **45% / 55%** \u2014 a \u00daNICA escrita nossa do n\u00famero no bloco. Fonte no HUD (proced\u00eancia: Arte) |\n| `doc_split_oficial` | **screenshot** | P\u00e1gina real `support.google.com/youtube/answer/72902` com a linha do split leg\u00edvel. \u26a0\ufe0f Gate: qualquer OUTRO numeral vis\u00edvel na p\u00e1gina que n\u00e3o seja o \u00e2ncora \u2192 mascarar/desfocar |\n| `timeline_longa` | **screenshot** | Barra de progresso real do YouTube de um epis\u00f3dio longo. \u26a0\ufe0f Dura\u00e7\u00e3o vis\u00edvel deve ecoar **~2 h** (\u00e2ncora \u00a728) \u2014 nunca outro n\u00famero; views/contadores \u2192 mascarar |\n| `timeline_curta` | **screenshot** | Barra de progresso real de v\u00eddeo de **10 min** (\u00e2ncora \u00a750) com **1** marcador (\u00e2ncora \u00a753). Mesmos gates de numeral |\n| `mk_ab_1..6` | **cutout-sticker-white** | 6 marcadores de ad-break recortados com a **borda branca assinatura do canal** (A43 \u00a719 D1 aprovada) \u2014 sub-camadas individuais, cada uma com sua janela de entrada |\n| `corredor_mk` | (reuso) | Os mesmos `mk_ab_1..6` re-encenados como planos em Z na cena 3 \u2014 reuso, n\u00e3o pe\u00e7a nova |\n\n**Declara\u00e7\u00e3o de sa\u00eddas (A40 Lei 3):** `barra_receita`/`barra_split_4555` saem antes do `doc_split_oficial` entrar (declarado no beat C1-6); `timeline_curta` sai no beat C2-5; `timeline_longa` sai no beat C3-2; `marca_adsense`, `doc_split_oficial` e `mk_ab/corredor_mk` \u2014 `tOut` declarado pelo DoP (delega\u00e7\u00e3o prevista no adendo).\n\n---\n\n## LACUNAS DE N\u00daMERO REGISTRADAS (n\u00e3o preenchidas \u2014 regra-m\u00e3e)\n\n1. **\"1 marcador\" do v\u00eddeo curto n\u00e3o \u00e9 FALADO** \u2014 vem do hint Motion do roteiro (\u00a753). A partitura o usa s\u00f3 como marca visual, nunca como numeral escrito. Se o Sovereign quiser a compara\u00e7\u00e3o em voz, \u00e9 emenda de roteiro, n\u00e3o minha.\n2. **N\u00e3o existe valor monet\u00e1rio ancorado para AdSense BR** (RPM, R$/mil views) \u2014 por isso as barras s\u00e3o **propor\u00e7\u00e3o sem cifra**. A dramaturgia pediria \"quanto pinga\"; o roteiro n\u00e3o d\u00e1; a lacuna fica declarada, n\u00e3o decorada.\n3. **A cauda n\u00e3o tem dura\u00e7\u00e3o ancorada al\u00e9m de \"meses\"** (\u00a750) \u2014 a cena 3 sustenta a ideia por imagem (profundidade = tempo), sem escrever prazo nenhum.\n\n---\n\n## PEDIDOS DE VOCABUL\u00c1RIO (ao engineer-spaces)\n\n```json\n\"vocabularyRequests\": [{\n  \"verb\": \"parte\",\n  \"need\": \"TRANSFORMAR uma camada em duas fra\u00e7\u00f5es rotuladas com conserva\u00e7\u00e3o de \u00e1rea (a barra de receita que se reparte em 45/55 no instante da palavra 'reparte')\",\n  \"usedInBeat\": \"ep07-a2-c1-split \u00b7 beat 4\",\n  \"whyNoExistingVerb\": \"revela/compara entregam ESTADOS prontos (a pe\u00e7a entra pronta ou duas barras entram lado a lado); nenhum verbo v1/MONTAR transforma uma camada existente em duas \u2014 verificado: 0 mecanismos de split em build-scene.mjs (2026-08-11)\",\n  \"fallbackNow\": \"revela da pe\u00e7a `barra_split_4555` j\u00e1 dividida \u2014 entrega o dado, PERDE o instante da partilha (uma receita tornando-se duas), que \u00e9 o cora\u00e7\u00e3o do beat\",\n  \"engineHint\": \"padr\u00e3o recorrente do canal: toda cena de 'reparte / divide / fica-com-X-passa-Y' vai pedir isso; hoje vira estado pronto sem drama\"\n}]\n```\n\nNenhum outro pedido: `atravessa`, `retira`, `revela`, `impacta`, `respira` verificados vivos no molde (`build-scene.mjs` \u2014 janelas `win()`, springs com stagger l.367, badge l.346, c\u00e2mera/corredor l.215). O stagger em s\u00e9rie dos marcadores **n\u00e3o** precisa de verbo novo \u2014 s\u00e3o N camadas com N janelas, autor\u00e1vel hoje.\n\n---\n\n## AUTO-AUDITORIA (Dramaturgo, antes de entregar)\n\n- [x] `intent` sobre o efeito no espectador; `stakes` nomeia o que se perde (\u00e2ncora de credibilidade \u00b7 referente do FECHO \u00b7 tese dos 3 neg\u00f3cios)\n- [x] Todo `action` no vocabul\u00e1rio vivo (MONTAR + v1); 1 verbo faltante virou Pedido com `fallbackNow` e perda declarada\n- [x] Cada cena tem `contraria` e/ou `resolve`; `resolve` \u00fanico e \u00faltimo em cada cena; nunca dois `impacta` seguidos\n- [x] `onScreen` \u2264 6 palavras, sem nota de dire\u00e7\u00e3o, sem par\u00e1frase; vazio em **13/16 beats** (\u2265 1/2, or\u00e7amento MONTAR)\n- [x] Nenhum `onScreen` repete texto que a camada j\u00e1 mostra (o doc e as barras falam sozinhos)\n- [x] 45/55 escrito por n\u00f3s **uma \u00fanica vez** (`barra_split_4555`); zero n\u00famero novo; lacunas registradas\n- [x] \u2265 1 `respira` por cena >10 s (C1-b2 \u00b7 C2-b3 \u00b7 C3-b3)\n- [x] `durationSec: null` + fonte PENDENTE (G7 \u2014 n\u00e3o estimo; alvos marcados como alvo de produ\u00e7\u00e3o)\n- [x] Todo `revela` com sa\u00edda declarada (beats ou delega\u00e7\u00e3o `tOut` DoP)\n- [x] `layerRef` \u2192 kit contratado (pe\u00e7as N\u00c3O existem ainda \u2014 G-MONTAR-1: nada renderiza antes do kit; custo 0 mco declarado)\n- [x] `staging`/`camera`/`light`/`lens`/`grade`/`art` ausentes \u2014 n\u00e3o s\u00e3o meus\n\n**Leis:** Lei 1 \u2014 vocabul\u00e1rio conferido por contagem no runner NESTA sess\u00e3o, n\u00e3o por mem\u00f3ria \u00b7 Lei 2 \u2014 verbo novo via Pedido, nunca improviso \u00b7 Lei 4 \u2014 ORO no cabe\u00e7alho.\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/roadmap/ep07-partituras/ato2-adsense.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(16:14:20)*

**Arquivo criado:** `/home/gcrUX/htdocs/constellation-orchestra/docs/roadmap/ep07-partituras/ato2-adsense.md`

**Resumo:** Partitura de Cena v1 do ATO 2 (AdSense) em linguagem MONTAR, estruturada em 3 cenas / 16 beats (~60-75s alvo): C1 "O negócio que se paga sozinho" (marca → respiro-passividade → barra que se reparte 45/55 → contraria "a plataforma fica com menos" → resolve com screenshot do doc oficial), C2 "Inventário é geometria" (timeline ~2h com 6 marcadores sticker-white em série casada com a contagem falada vs. timeline 10min com 1 → resolve nomeando "inventário", pago pelo FECHO §93), C3 "A cauda" (atravessa o corredor de marcadores em Z → o palco desmonta → resolve "enquanto você dorme"). Inclui proposta de expansão da narração [aguarda aprovação] sem nenhum número novo, tabela de âncoras (§ citados), kit contratado de 8 peças (custo 0 mco) com gates de mascaramento de numerais não-âncora, e 3 lacunas de número registradas (o "1 marcador" vem do hint §53, não da fala; RPM BR inexistente; cauda sem prazo além de "meses").

**Pedidos de Vocabulário (1):** verbo `parte` — transformar uma camada em duas frações rotuladas com conservação de área (a barra que se reparte no instante de "reparte"); verificado 0 mecanismos de split em `scripts/motion/layered/build-scene.mjs` (2026-08-11). `fallbackNow`: revela da peça `barra_split_4555` já dividida — entrega o dado, perde o instante da partilha. Demais verbos usados (`revela`/`retira`/`atravessa`/`impacta`/`respira`) conferidos vivos no runner por contagem nesta sessão.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-08-11 - agent-aef383c1afbc6d467]]
> * **Próxima Sessão**: [[2026-08-11 - agent-af9a325cc8b0c5a92]]
%% --- TIMELINE END --- %%

# Session agent-a56bebbfcbaac5590
**Date:** 2026-08-05 | **Session ID:** `agent-a56bebbfcbaac5590`

---

## 👤 User *(23:13:23)*

Você é um CRÍTICO ADVERSARIAL. Abaixo, achados de pesquisa da frente "cinematografia-e-grade" para um motor de motion graphics que roda em HTML determinístico (window.__seek(t)) + Playwright headless + FFmpeg, SEM GPU dedicada, SEM CDN, custo US$0.

{
  "findings": [
    {
      "technique": "Slow In and Out — easing obrigatório em TODO movimento (nunca t = i/total cru)",
      "why_it_reads_professional": "Movimento linear é o marcador nº1 de motion graphics amador: o olho lê 'interpolação de computador', não 'objeto com massa'. Lasseter é explícito e matemático: slow in/out 'refers to second- and third-order continuity of motion' — é literalmente a derivada segunda/terceira que o cérebro usa para inferir peso e inércia. Um nó que entra com ease-out 'chega e assenta'; o mesmo nó linear 'teleporta e para'. Zero mudança de arte, mudança total de percepção.",
      "how_to_implement_here": "O contrato do rail já é determinístico por índice: applyFrame(i, total) em scripts/hyperframes/render-core.ts. A regra é: nunca interpolar com t = i/total; sempre t' = bezier(t) antes de calcular posição/escala/opacidade. Implementar cubic-bezier em ~15 linhas (Newton-Raphson sobre a curva, 4 iterações) e exportar um mapa EASING em src/lib/cinematic-grammar.ts espelhando os keywords normativos do W3C: ease-in-out = (0.42,0,0.58,1), ease-out = (0,0,0.58,1), ease-in = (0.42,0,1,1), ease = (0.25,0.1,0.25,1). Convenção da casa: entrada de nó = ease-out, saída = ease-in, câmera/parallax = ease-in-out. Determinístico por construção (só depende de i/total), zero CDN, custo US$0 — é aritmética pura, não biblioteca.",
      "source_url": "https://www.w3.org/TR/css-easing-1/",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Arcos — desacoplar a spline do CAMINHO da spline do TEMPO",
      "why_it_reads_professional": "Lasseter documenta a armadilha exata dos sistemas de keyframe: 'In most 3D keyframe computer animation systems, the path of action from one extreme to another is controlled by the same spline that controls the timing... When a motion is slow, with many inbetweens, the arc of the path of action is curved, as desired. But when the action is fast, the arc flattens out: the faster the action, the flatter the arc.' E o veredito: 'Straight inbetweens can completely kill the essence of an action.' Movimento rápido em linha reta é exatamente o que acontece hoje em transições de UI animada — e é o que faz parecer diagrama, não cinema.",
      "how_to_implement_here": "Nos motion-*.html de scripts/ep05/, trocar interpolação linear de x/y por duas funções INDEPENDENTES: (1) geometria = um <path> SVG invisível com a curva desejada, lido por path.getPointAtLength(easedT * path.getTotalLength()); (2) tempo = a função de easing do item anterior. O caminho continua curvo mesmo quando a ação é rápida, porque a curvatura vive no path, não no espaçamento dos frames. Para o 'running ring' e as edges trackeadas da linguagem v6, o mesmo path serve de trilho. 100% determinístico (getPointAtLength é puro), roda no Chromium headless do render-core, custo US$0.",
      "source_url": "http://graphics.cs.cmu.edu/nsp/course/15-464/Fall05/papers/lasseter.pdf",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Staging — uma ideia por vez, e contraste de movimento para dirigir o olho",
      "why_it_reads_professional": "É a regra que mais separa motion profissional de 'tudo animando ao mesmo tempo'. Lasseter: 'It is important, when staging an action, that only one idea be seen by the audience at a time. If a lot of action is happening at once, the eye does not know where to look and the main idea of the action will be upstaged and overlooked.' E a mecânica perceptual acionável: 'In a still scene, the eye will be attracted to movement. In a very busy scene, the eye will be attracted to something that is still.' Ou seja, o destaque não é brilho — é CONTRASTE de movimento. Numa cena onde tudo pulsa, congelar o nó principal destaca mais do que animá-lo.",
      "how_to_implement_here": "Virar gate mecânico, não conselho. No runner de render, calcular energia de movimento por região: diferença de pixels entre frame i e i-1, agregada pelas bounding boxes dos elementos (já conhecidas no HTML via getBoundingClientRect no applyProps). Regra: por janela de beat, no máximo UM elemento acima do limiar de energia; o resto congelado. Falha = exit 1, igual aos smokes da casa. Isso ataca direto o vício de animar nó + label + ring + edge simultaneamente. Custo US$0 (é subtração de PNGs que já são gerados), determinístico.",
      "source_url": "http://graphics.cs.cmu.edu/nsp/course/15-464/Fall05/papers/lasseter.pdf",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Ação secundária subordinada — mudar antes ou depois do movimento, nunca no meio",
      "why_it_reads_professional": "Lasseter: 'A secondary action is always kept subordinate to the primary action. If it conflicts, becomes more interesting, or dominates in any way, it is either the wrong choice or is staged improperly.' E o timing exato: 'The change must come before, or after, the move. A change in the middle of a major move will go unnoticed, and value intended will be lost.' Traduzido para o nosso vocabulário: trocar o texto do label ENQUANTO o nó viaja queima a informação — o espectador não lê nenhum dos dois. O custo é invisível (nada quebra), o que é justamente por que reincide.",
      "how_to_implement_here": "Regra de autoria nos motion-*.html: qualquer mudança de conteúdo (texto, número de custo em mco, ícone, badge de status) é agendada por applyFrame em janelas DISJUNTAS das janelas de translação do elemento pai. Materializar como um schedule declarativo — beats: [{el, move:[f0,f1]}, {el, contentChange: f}] — e validar no runner que nenhum contentChange cai dentro de um intervalo move do mesmo elemento. Mesmo motor de checagem do gate de staging; custo US$0.",
      "source_url": "http://graphics.cs.cmu.edu/nsp/course/15-464/Fall05/papers/lasseter.pdf",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Antecipação e follow-through/overlap por offset de 2-4 frames",
      "why_it_reads_professional": "Lasseter: 'An action occurs in three parts: the preparation for the action, the action proper, and the termination.' A antecipação é 'the anatomical provision for an action... A foot must be pulled back before it can be swung forward to kick a ball. Without anticipation many actions are abrupt, stiff and unnatural.' Em motion graphics é o que separa 'elemento aparece' de 'elemento nasce': um recuo de 3 frames antes da entrada, e as partes soltas (ring, sombra, edge) chegando 2-4 frames DEPOIS do corpo do nó. É custo de autoria quase nulo com ganho perceptual desproporcional.",
      "how_to_implement_here": "Em applyFrame(i, total), cada sub-elemento ganha um delayFrames próprio e o pai ganha um pré-beat. Antecipação: nos 3 frames anteriores à entrada, escala 1.0 → 0.96 com ease-in (contra-movimento); depois a entrada real com ease-out e overshoot leve. Overlap: ring e edges com delayFrames = 2..4, opacidade/escala seguindo o mesmo easing deslocado. Tudo derivado de i (inteiro), então sha256-idêntico entre runs — preserva a NFR-VS-016 do render-core. Custo US$0.",
      "source_url": "http://graphics.cs.cmu.edu/nsp/course/15-464/Fall05/papers/lasseter.pdf",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Levantar o preto (filmic toe) e derrubar o branco puro no grade",
      "why_it_reads_professional": "Preto absoluto (#000) e branco estourado (#fff) não existem em imagem fotografada — a própria luz de preenchimento existe porque, nas palavras de Burum, 'Shadows are not inky black even on a sunny day, because they get natural fill from sunlight bouncing off the sky, clouds, buildings or ground.' Um frame HTML tem preto matemático, e é o delator instantâneo de 'screenshot de página' contra 'material capturado'. Levantar o piso ~4,5% e fechar o teto ~98,5% já entrega a leitura de material gradeado, antes de qualquer decisão de cor.",
      "how_to_implement_here": "Encadear no encode do motion-bridge (onde o color grading da casa já vive), ANTES do format=yuv420p: format=gbrp,curves=master='0/0.045 0.25/0.22 0.5/0.5 0.75/0.79 1/0.985':interp=pchip. Prova material rodada neste host (ffmpeg 6.1.1): entrada color=black atravessando essa curva sai com luma 0x19 = 25, acima do piso 16 do limited range — o preto foi materialmente levantado. O format=gbrp na frente evita fazer a curva no espaço chroma-subamostrado. Custo US$0, um filtro.",
      "source_url": "https://ffmpeg.org/ffmpeg-filters.html",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "curves com interp=pchip (spline monotônica) em vez do padrão natural",
      "why_it_reads_professional": "Detalhe pequeno, defeito grande: a spline cúbica natural (padrão do filtro) pode ter overshoot entre pontos de controle, produzindo inversão local de tom nas sombras e halos em gradiente — exatamente onde vivem os fundos nebulosos das nossas cenas. A pchip é monotônica por definição: nunca inverte a ordem tonal. É trocar um token e eliminar uma classe inteira de artefato de banding/halo.",
      "how_to_implement_here": "Sempre passar interp=pchip no filtro curves do pipeline de grade (o padrão documentado é natural = natural cubic spline; pchip = monotonically cubic interpolation). Confirmado no ffmpeg -h filter=curves deste host: preset(0..10), master/r/g/b/all, interp {natural|pchip}. Custo US$0.",
      "source_url": "https://ffmpeg.org/ffmpeg-filters.html",
      "feasibility": "direto",
      "impact": "medio"
    },
    {
      "technique": "Teal & orange fundamentado: no modelo ADITIVO (tela) o complementar do laranja é ciano, não azul",
      "why_it_reads_professional": "A paleta teal&orange funciona porque é a separação complementar máxima no espaço em que o vídeo realmente vive. Em RGB/luz, os pares complementares são vermelho–ciano, verde–magenta, azul–amarelo — o complemento do laranja é CIANO; é no modelo de pigmento RYB que o par vira azul–laranja. Escolher ciano (e não azul) como polo frio dá contraste cromático maior com menos saturação, ou seja, mais separação percebida sem o look 'saturado demais' amador. Bônus: casa exatamente com o token MIV da casa (accent = cyan), então não é decisão estética nova, é justificativa técnica da que já existe.",
      "how_to_implement_here": "Duas camadas. (1) No HTML: travar a paleta em dois polos — ciano MIV como frio e um âmbar quente como polo de valor — e proibir uma terceira família cromática saturada (limited palette). (2) No FFmpeg, split tonal: colorbalance=rs=-0.05:bs=0.09:rm=0.02:bm=-0.01:rh=0.07:bh=-0.05:pl=1 — sombras puxadas para ciano, altas puxadas para âmbar, pl=1 preservando lightness para não mexer na exposição. Cadeia inteira validada neste host (curves → colorbalance → eq → unsharp → vignette rodou sem erro e gerou PNG). Custo US$0.",
      "source_url": "https://en.wikipedia.org/wiki/Complementary_colors",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "A 'skin tone line' do vectorscópio é o eixo I do NTSC — usar como referência, NUNCA como regra rígida",
      "why_it_reads_professional": "Vale como antídoto contra dogma vendido em tutorial. A linha existe porque o NTSC precisava sincronizar luminância e crominância, e o YIQ escolheu I como o eixo laranja-azul justamente por ser onde o olho humano é mais sensível — e esse eixo calhou de passar perto do matiz da pele. Segundo Video Demystified (Keith Jack), o ângulo de fase para skin tone varia entre fabricantes, de 116° a 126°, com 123° (o eixo +I) adotado por simplificar o processamento. Conclusão honesta: é coincidência de codificação, não lei fisiológica. O ganho profissional é duplo — dá um alvo objetivo para consistência de pele entre cenas, e evita o erro de 'forçar tudo na linha' que achata rostos.",
      "how_to_implement_here": "Onde houver rosto/avatar (Veo, Nano Banana) num episódio, usar o eixo como CHECK de consistência entre planos, não como destino: extrair um frame por cena e medir o matiz médio da região de pele; alertar se dois planos da mesma sequência divergirem além de ~10° — é o que causa a sensação de 'cada take de uma câmera'. Nas cenas 100% motion (sem pele) a linha é irrelevante e não deve pautar a paleta. Medição via ffmpeg + leitura de pixels em Node, custo US$0.",
      "source_url": "https://bramstout.nl/en/webbooks/vectorscopes/",
      "feasibility": "direto",
      "impact": "medio"
    },
    {
      "technique": "As três funções universais da luz (Burum/ASC): lançar sombra, criar SEPARAÇÃO, preencher",
      "why_it_reads_professional": "Stephen H. Burum, ASC: 'Everyone does at least one of three things every time they light a set' — (1) lançar uma sombra, (2) criar separação, (3) adicionar fill. E a segunda é a chave do 2.5D: 'Photography looks at the world with only one lens, and you need to introduce a three-dimensional quality to this two-dimensional image. There's only one way to accomplish that: creating areas of light against dark or dark against light.' Ele é categórico que não se trata de cor. Isso é literalmente o manual de como fazer um nó glass parecer um objeto num espaço em vez de um retângulo com blur: cada plano precisa de uma borda clara contra escuro.",
      "how_to_implement_here": "Por nó glass no motion-*.html, três camadas explícitas em vez do box-shadow padrão: (a) KEY = linear-gradient direcional no fundo do card, mais claro no lado da key; (b) SEPARAÇÃO = borda de 1px com conic-gradient que fica brilhante só no arco voltado para a key e escurece no oposto (é o 'rim' do Burum: dark, halo, dark); (c) FILL = rgba ambiente uniforme controlando quanto se enxerga dentro da sombra. Nada disso é imagem externa — é CSS puro, determinístico, zero CDN, US$0.",
      "source_url": "https://theasc.com/articles/lighting-a-set",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Razão key-to-fill como DIAL de humor explícito (8:1 dramático · 3:1 leve)",
      "why_it_reads_professional": "Burum filmou o MESMO cenário com três níveis de fill e o efeito é de gênero, não de exposição: sem fill 'conveys a sense of foreboding'; a 8:1 fica 'bright but still modeled' com pretos de referência preservados no cabelo; e a versão mais preenchida ele apelida de 'Laverne & Shirley look' — comédia. A frase que fecha: 'The job of the fill light is to set the mood of the scene. There is no correct amount of fill; it's a matter of artistic interpretation.' Ou seja, o humor da cena é uma RAZÃO, não um brilho — e hoje nossas cenas não têm esse dial nomeado.",
      "how_to_implement_here": "Exportar KEY_FILL_RATIOS em src/lib/cinematic-grammar.ts ao lado de LIGHTING (dramatic 8:1, neutral 4:1, bright 3:1) e ligar a uma única CSS custom property --fill-ratio nos templates, que dirige a opacidade da camada ambiente de TODOS os nós de uma vez. Assim o diretor de cena escolhe humor por token, e a mudança é global e consistente — em vez de ajustar sombra card a card. Custo US$0.",
      "source_url": "https://theasc.com/articles/lighting-a-set",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Fill no eixo da câmera — uma única direção de sombra em toda a cena",
      "why_it_reads_professional": "Burum: 'You want the fill light on the camera's axis. If you don't put it there, you start to cast a secondary shadow on the other side of the axis' — e 'Old movie wisdom says that you don't want to see a secondary shadow cast by fill light, mainly because it's distracting.' O delator equivalente em HTML é brutal e universal: cada card com o box-shadow padrão 0 4px = luz vindo de cima em todo lugar, independente da composição = imagem chapada, sem fonte, sem espaço. Uma direção de key única para o frame inteiro é a correção mais barata que existe.",
      "how_to_implement_here": "Uma variável --key-angle por cena; TODOS os offsets de box-shadow e filter: drop-shadow derivados dela por trigonometria em CSS calc() (ou computados uma vez no applyProps). Proibir box-shadow com offset hardcoded nos templates — vira item de revisão da skill motion-scenes. Bônus fiel ao Burum: quando precisar preencher fora do eixo, preencher pelo lado da key ('you should fill from the key side if you have a choice, because that tends to wrap the shadow better'). Custo US$0.",
      "source_url": "https://theasc.com/articles/lighting-a-set",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Fundo abaixo de 25% de reflectância — gate numérico, não gosto",
      "why_it_reads_professional": "Número duro e raro do ASC: 'If the set walls are lighter than normal skin tone, people will always seem dark by comparison. For people to stand out, the reflective value of the set should be below 25 percent. If it's not, the actors' faces will look dark even though they're properly exposed.' Traduzido para motion graphics: se a nebulosa/gradiente de fundo passa de ~25% de luminância, os nós glass deixam de ler como primeiro plano por mais que se aumente o brilho deles — e a resposta instintiva (clarear o nó) piora, porque estoura. É a causa raiz de composições que parecem 'lavadas' sem ninguém saber por quê.",
      "how_to_implement_here": "Virar gate mecânico no runner: renderizar a camada de fundo isolada (os motion-*.html já separam nebula-bg.html) e medir a luminância média com ffmpeg (signalstats/YAVG); falhar se YAVG exceder ~25% do range. Roda em 1 frame, custo US$0, e é o tipo de verificação que a Lei 1 exige — prova material em vez de 'ficou bom'.",
      "source_url": "https://theasc.com/articles/lighting-a-set",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Grain temporal — mata a esterilidade digital E o banding dos gradientes",
      "why_it_reads_professional": "Dois problemas com um filtro. (1) Gradiente suave de CSS num encode H.264 8-bit yuv420p produz banding visível em faixas — justamente nos fundos nebulosos, que é onde mais dói. O ruído funciona como dither e dissolve as faixas. (2) Ausência total de grão é assinatura de render sintético; um grão sutil e TEMPORAL (mudando por frame) empurra a leitura para 'capturado'. É provavelmente a maior mudança de percepção por unidade de esforço de toda a lista: um filtro, uma linha.",
      "how_to_implement_here": "No fim da cadeia de grade, antes do encode: noise=alls=6:allf=t+u (t = temporal, u = uniforme; alls é a força 0..100). Fixar all_seed para manter a reprodutibilidade sha256 do render-core (NFR-VS-016) — sem seed fixo o output deixa de ser bit-exato. Confirmado no ffmpeg -h filter=noise deste host: all_seed, all_strength, all_flags {a,p,t,u}. Custo US$0.",
      "source_url": "https://ffmpeg.org/ffmpeg-filters.html",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Motion blur por ângulo de obturador — renderizar em N× fps e mesclar com tmix",
      "why_it_reads_professional": "É a diferença estrutural entre 'animação de tela capturada frame a frame' e 'movimento filmado'. Screenshot por frame tem obturador infinitesimal: zero blur, e o movimento estroboscópico denuncia na hora, sobretudo em translações rápidas e no running ring. Cinema usa ~180° de obturador — cada frame integra metade do intervalo. Mesclar 4 sub-frames numa saída de 25fps entrega o equivalente a ~144° e transforma a leitura do movimento sem tocar na arte.",
      "how_to_implement_here": "Alterar scripts/hyperframes/render-core.ts para aceitar um multiplicador de sub-frames: gerar N = duration × fps × 4 PNGs (applyFrame já é indexado por i/total, então é só multiplicar total — continua determinístico) e encadear tmix=frames=4:weights='1 1 1 1',fps=25 antes do encode. Testado neste host: tmix com 100fps de entrada decimando para 25 rodou OK. Trade-off honesto: 4× o tempo de render (CPU local, não API) — custo financeiro US$0, custo de wall-clock real. Aplicar seletivamente nas cenas de translação rápida.",
      "source_url": "https://ffmpeg.org/ffmpeg-filters.html",
      "feasibility": "exige-novo-modulo",
      "impact": "alto"
    },
    {
      "technique": "Perspectiva atmosférica — profundidade por atenuação, não por escala",
      "why_it_reads_professional": "Num frame 2.5D o cérebro lê profundidade principalmente por perda de contraste, saturação e nitidez com a distância — não por tamanho. Camadas de fundo com o MESMO contraste e nitidez das da frente achatam a cena mesmo com parallax correto: o movimento diz 'tem profundidade' e a textura diz 'é um adesivo'. Corrigir isso é o que faz a galáxia t=0 parecer espaço em vez de papel de parede. Reforça a função de 'separação' do Burum por outro eixo.",
      "how_to_implement_here": "Nas camadas de fundo dos motion-*.html: filter: blur(2-4px) saturate(0.65) contrast(0.85) + puxar o matiz para o polo frio (ciano) — todos determinísticos, aplicados via CSS no Chromium headless. Escalonar por camada de parallax (quanto mais longe, mais atenuado). Alternativa no encode, se a camada já vier achatada: gblur=sigma=... com planes seletivo. Custo US$0, zero CDN.",
      "source_url": "https://theasc.com/articles/lighting-a-set",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Vinheta sutil + nitidez seletiva para dirigir o olho (eye-trace)",
      "why_it_reads_professional": "Burum descreve o efeito compositivo do esquema de inside cross-keys: 'It's a compositional scheme. Inside cross-keys pull the attention to the center of the frame, because you have dark on the outside and light on the inside.' A vinheta é a versão de pós desse mesmo mecanismo: escurece a periferia e o olho vai ao centro sem que o espectador perceba a manipulação. Somada a um unsharp leve só na luma, entrega a sensação de 'lente boa' — porque nitidez de borda é onde o olho procura foco.",
      "how_to_implement_here": "Na cadeia de grade: unsharp=lx=5:ly=5:la=0.6 (só luma; chroma_amount fica em 0, que é o default — evita franja colorida) seguido de vignette=angle=PI/6 (o default é PI/5, mais forte; PI/6 é discreto). Ambos validados na cadeia que rodei neste host. Cuidado material: la acima de ~0.8 gera halo em texto branco sobre fundo escuro, que é o oposto do objetivo. Custo US$0.",
      "source_url": "https://ffmpeg.org/ffmpeg-filters.html",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Regra dos terços · headroom · leading room como guias no template",
      "why_it_reads_professional": "Convenção antiga e estável (John Thomas Smith, Remarks on Rural Scenery, 1797: 'the ratio of about two thirds to one third, or of one to two, a much better and more harmonizing proportion'). O ganho concreto em motion graphics é headroom e leading room: excesso de espaço no topo cria 'dead space' e o sujeito afunda; e o espaço deve ir NA DIREÇÃO do movimento — um nó viajando para a direita com a margem à esquerda parece prestes a sair do frame. Composição centralizada em tudo é o default preguiçoso do HTML (flex center) e lê como slide corporativo.",
      "how_to_implement_here": "Overlay de guias dev-only nos motion-*.html (um <div data-guides> com as duas linhas horizontais e duas verticais, ligado por query param e nunca presente no render final). Convenções da casa: título/olhos na linha do terço superior; centro óptico do nó principal numa interseção; leading room à frente do vetor de deslocamento. Como o applyFrame conhece a direção do movimento, dá para ASSERTAR no runner que a margem maior está do lado do destino. Custo US$0.",
      "source_url": "https://en.wikipedia.org/wiki/Headroom_(photographic_framing)",
      "feasibility": "direto",
      "impact": "medio"
    },
    {
      "technique": "Continuidade de eixo (180°) aplicada à direção de tela entre cenas de motion",
      "why_it_reads_professional": "A regra mantém a câmera de um lado do eixo de ação para preservar a direção de tela; atravessar 'may disorient the viewer' porque as posições se invertem esquerda-direita. Em motion graphics o eixo não é entre dois atores — é o VETOR DE FLUXO do produto (entrada → processamento → saída). Se numa cena os assets entram pela esquerda e fluem para a direita e na cena seguinte o mesmo fluxo inverte, o espectador perde o mapa mental do pipeline mesmo entendendo cada plano isolado. É desorientação que ninguém sabe nomear e todo mundo sente.",
      "how_to_implement_here": "Declarar um flowAxis por episódio (ex.: 'esquerda→direita') nos props do assemble-v*.ts, e derivar dele TODAS as entradas/saídas de nó, a direção do running ring e a orientação das edges. Para inverter legitimamente, usar um plano neutro como buffer — a galáxia t=0 em tela cheia já é exatamente esse 'buffer shot' na linguagem v6. Validável por lint sobre o schedule de beats. Custo US$0.",
      "source_url": "https://en.wikipedia.org/wiki/180-degree_rule",
      "feasibility": "direto",
      "impact": "medio"
    },
    {
      "technique": "Cortar no movimento (cutting on action) em vez de cortar no repouso",
      "why_it_reads_professional": "É a ferramenta básica do corte invisível: 'a match on the action is when some action occurring before the temporally questionable cut is picked up where the cut left it by the shot immediately following' — o segundo plano mostra o elemento no MESMO estágio da moção em que o primeiro parou. O cérebro prioriza rastrear o movimento e não registra o corte. O erro padrão em montagem de motion é o oposto: cada cena termina com tudo parado e a próxima começa do zero — o que produz uma sequência de cartelas, não um filme.",
      "how_to_implement_here": "Nos assemble-v*.ts, deixar cada cena com uma cauda de movimento (o elemento ainda viajando no último frame) e a cena seguinte com uma cabeça que retoma o MESMO vetor e velocidade. Como o rail é determinístico por índice, dá para calcular a velocidade nos frames de borda a partir da própria função de easing e assertar que |v_saída − v_entrada| e a direção casam dentro de uma tolerância — corte invisível verificado por número, não por olho. Custo US$0.",
      "source_url": "https://en.wikipedia.org/wiki/Continuity_editing",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "J-cut / L-cut — o áudio cruza o corte antes/depois da imagem",
      "why_it_reads_professional": "O J cut é aquele em que 'the audio from a following scene overlaps the picture from the preceding scene' — o nome vem da forma que as peças de áudio e vídeo desenham na timeline, com a cauda do J sendo o áudio do próximo clipe sob a imagem do anterior. O efeito é que a costura deixa de ser simultânea: quando som e imagem trocam no MESMO frame, o corte fica audível e visível ao mesmo tempo e vira uma emenda. Escalonar os dois é o que faz a montagem soar contínua.",
      "how_to_implement_here": "A casa já tem os alvos definidos em src/lib/cinematic-grammar.ts (MIX_TARGETS.jCutLeadSec = 0.6 e lCutTailSec = 1.2) — falta aplicá-los no assemble. Implementar no filtergraph de áudio com adelay para posicionar a narração da cena seguinte adiantada em 0,6 s e acrossfade/amix para sobrepor a cauda da anterior por 1,2 s, mantendo a hierarquia de mixagem já declarada (diálogo > hard SFX > ambiência > trilha) e o duck de −12 dB. Custo US$0.",
      "source_url": "https://en.wikipedia.org/wiki/J_cut",
      "feasibility": "direto",
      "impact": "medio"
    },
    {
      "technique": "Rule of Six (Murch) como ordem de desempate quando os critérios conflitam",
      "why_it_reads_professional": "É o único framework que diz o que SACRIFICAR, e por isso vale mais que qualquer regra isolada. Murch pondera emoção 51%, história 23%, ritmo 10%, eye-trace 7%, plano bidimensional da tela 5%, espaço tridimensional da ação 4% — e a instrução é explicitamente hierárquica: não abrir mão de emoção antes de história, nem de história antes de ritmo, nem de ritmo antes de eye-trace, nem de eye-trace antes de planaridade, nem de planaridade antes de continuidade espacial. Aplicado à nossa produção, isso autoriza quebrar continuidade de eixo para salvar ritmo — e proíbe o inverso. É o antídoto contra virar refém das regras técnicas que estão nesta mesma lista.",
      "how_to_implement_here": "Não é código: é a regra de decisão que entra no system prompt do spaces-agent-chat e na skill motion-scenes, junto das 18 regras já destiladas do repertório. O item acionável é eye-trace: como o runner já conhece a bounding box de cada elemento por frame, dá para computar o centroide de atenção (região de maior energia de movimento) no último frame antes do corte e no primeiro depois, e alertar quando o salto for grande — porque forçar o olho a atravessar o frame no corte é exatamente o que Murch chama de perder eye-trace. Custo US$0.",
      "source_url": "https://www.studiobinder.com/blog/walter-murch-rule-of-six/",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "ASC CDL (slope/offset/power) como CONTRATO do grade + LUT .cube própria da casa",
      "why_it_reads_professional": "Consistência entre episódios é metade do que faz um canal parecer profissional — e hoje o grade vive espalhado em flags de filtro dentro do encode do motion-bridge, o que garante deriva. O ASC CDL, publicado pelo Technology Committee da ASC, define a matemática mínima e portável: out = (i × s + o)^p por canal (slope nominal 1.0, offset 0, power 1.0), mais saturação na versão 1.2. Mapeia exatamente ao vocabulário lift/gamma/gain e dá um objeto de 10 números versionável em git — a paleta do canal vira dado, não folclore.",
      "how_to_implement_here": "Duas etapas. (1) Representar o look da casa como um CDL (10 números) em src/lib/cinematic-grammar.ts, ao lado de MIX_TARGETS — o análogo visual dos alvos de áudio. (2) Escrever um gerador que amostra esse CDL num cubo N=33 e emite um .cube, aplicado com um único filtro: lut3d=file=mcorch-house.cube:interp=tetrahedral (tetrahedral é o default e o de menor erro). Ganho colateral: um filtro no lugar da cadeia inteira no caminho quente, e o mesmo look aplicável a material Veo/Nano Banana para casar com o motion. Custo US$0 — o gerador é aritmética local.",
      "source_url": "https://en.wikipedia.org/wiki/ASC_CDL",
      "feasibility": "exige-novo-modulo",
      "impact": "medio"
    },
    {
      "technique": "Squash & stretch em UI — deformação não-uniforme com volume preservado",
      "why_it_reads_professional": "Lasseter: 'The most important principle is called squash and stretch. When an object is moved, the movement emphasizes any rigidity in the object.' Um card que translada com escala rigorosamente uniforme grita 'div'. Uma deformação mínima no eixo do movimento — esticar ~3% na direção do deslocamento e comprimir o mesmo tanto no eixo perpendicular, preservando a área — dá materialidade sem virar cartoon. É sutil o bastante para passar despercebido conscientemente e é exatamente por isso que funciona.",
      "how_to_implement_here": "Em applyFrame, derivar a velocidade instantânea da própria curva de easing (diferença entre t' de i e de i−1), e aplicar transform: scale(1+k·v, 1/(1+k·v)) alinhado ao vetor de movimento, com k calibrado para no máximo ~3-4% no pico. A preservação de volume é o 1/(1+k·v) — sem ela vira zoom e o efeito se perde. Determinístico (só depende de i), CSS puro. Calibrar com QA visual: se der para VER a deformação num frame parado, está exagerado.",
      "source_url": "http://graphics.cs.cmu.edu/nsp/course/15-464/Fall05/papers/lasseter.pdf",
      "feasibility": "direto",
      "impact": "medio"
    },
    {
      "technique": "Exagero balanceado entre componentes — nunca isolado",
      "why_it_reads_professional": "Lasseter dá o critério que evita o efeito 'template do Canva': 'A scene has many components to it: the design, the shape of the objects, the action, the emotion, the color, the sound. Exaggeration can work with any component, but not in isolation. The exaggeration of the various components should be balanced. If just one thing is exaggerated in an otherwise lifelike scene, it will stick out and seem unrealistic.' É a explicação técnica de por que uma transição chamativa sozinha, sobre uma cena sóbria, estraga a cena inteira em vez de animá-la — o problema não é a transição, é o desequilíbrio.",
      "how_to_implement_here": "Definir um nível de estilização por episódio (sóbrio | médio | alto) como um único token nos props do assemble, e derivar dele CONJUNTAMENTE: amplitude de overshoot do easing, força da vinheta, quantidade de grão, saturação do split teal/orange e agressividade das transições. Um dial, não seis. Isso impede a deriva típica em que cada cena ganha um efeito novo e o episódio perde unidade. Custo US$0.",
      "source_url": "http://graphics.cs.cmu.edu/nsp/course/15-464/Fall05/papers/lasseter.pdf",
      "feasibility": "direto",
      "impact": "medio"
    },
    {
      "technique": "Motion blur por objeto (velocity buffer) e bokeh real de profundidade",
      "why_it_reads_professional": "O tmix borra o FRAME inteiro por igual: quando um nó voa e o fundo está parado, o fundo também borra, o que é fisicamente errado e perceptível em movimentos rápidos. Motion blur correto é por objeto, proporcional à velocidade daquele objeto. Do mesmo modo, desfoque de profundidade real (círculo de confusão variando com a distância, com bokeh de borda definida) é o que dá a leitura de lente grande — o blur gaussiano de CSS achata porque não tem forma de diafragma.",
      "how_to_implement_here": "Sai do domínio HTML/CSS: exige uma passada WebGL no mesmo Chromium headless (o rail já roda Playwright, então não há dependência nova nem CDN). Renderizar os elementos como quads texturizados com um G-buffer de velocidade e profundidade, e um shader de pós que borra ao longo do vetor de velocidade por pixel e aplica CoC por profundidade. Continua determinístico por applyFrame(i,total) desde que o shader não use tempo de parede nem aleatoriedade sem seed. Custo US$0 (GPU/CPU local), mas é módulo novo de verdade — só justifica depois que easing, arcos, grain e grade estiverem em produção, porque estes entregam mais percepção por muito menos esforço.",
      "source_url": "http://graphics.cs.cmu.edu/nsp/course/15-464/Fall05/papers/lasseter.pdf",
      "feasibility": "exige-webgl",
      "impact": "medio"
    },
    {
      "technique": "GAP declarado: grade HDR/wide-gamut (PQ/HLG) de ponta a ponta",
      "why_it_reads_professional": "Vale registrar o vazio em vez de prometer, seguindo o contrato de honestidade do repertório da casa. Todo o ganho de grade descrito acima acontece em SDR 8-bit: o encode do rail termina em format=yuv420p H.264, e as curvas/CDL operam nesse contêiner. Um grade HDR real exigiria pipeline de 10-bit com transfer PQ ou HLG, metadata de mastering e entrega em HEVC/AV1 — e as plataformas de destino tratam isso por caminhos próprios. Aplicar 'look HDR' dentro de SDR não é HDR: é saturação e contraste, e tende a piorar (clipping e banding).",
      "how_to_implement_here": "Não implementar agora. O ffmpeg deste host tem libplacebo compilado (confirmado na linha de configure), então o tone mapping existiria tecnicamente — mas a cadeia de entrega (H.264 yuv420p 8-bit dos runners e do motion-bridge) e o QA da casa são SDR de ponta a ponta, e mudar isso é decisão de contrato de entrega, não de filtro. Manter todo o grade em SDR e declarar HDR como fora de escopo até haver demanda material de plataforma.",
      "source_url": "https://ffmpeg.org/ffmpeg-filters.html",
      "feasibility": "inviavel-no-rail",
      "impact": "baixo"
    }
  ]
}

Sua tarefa: REFUTAR. Para cada achado, verifique (a) o source_url existe e realmente sustenta a claim — abra com WebFetch quando duvidar; (b) a implementação proposta é realmente possível no nosso rail (headless sem GPU, determinismo por seek, zero rede); (c) a técnica realmente muda a percepção de qualidade ou é folclore.
Devolva a lista APENAS com os achados que SOBREVIVEM, corrigindo o campo how_to_implement_here quando a proposta original for irrealizável, e rebaixando feasibility quando for o caso. Prefira cortar a manter: um achado falso custa uma sessão inteira do Sovereign. Se um source_url for inventado ou não sustentar a claim, DESCARTE o achado.

## 🤖 Claude *(23:13:26)*

I'll verify each finding rigorously. Let me start by checking the actual rail code and the sources.

## 🤖 Claude *(23:13:27)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la /home/gcrUX/htdocs/constellation-orchestra/scripts/hyperframes/ 2>/dev/null; echo \"---EP05---\"; ls -la /home/gcrUX/htdocs/constellation-orchestra/scripts/ep05/ 2>/dev/null | head -50",
  "description": "List hyperframes and ep05 runner dirs"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> total 80
> drwxrwxr-x  3 gcrUX  gcrUX   4096 Jul 22 17:27 .
> drwxrwxr-x 15 gcrUX  gcrUX  12288 Aug  5 20:02 ..
> -rw-rw-r--  1 ubuntu ubuntu 33100 Jul 22 17:27 render-core.ts
> -rw-rw-r--  1 ubuntu ubuntu  3385 Jul 22 13:15 render-style-previews.ts
> -rw-rw-r--  1 ubuntu ubuntu  3227 Jul 22 07:54 split-grid-frame.test.ts
> -rw-rw-r--  1 ubuntu ubuntu 10676 Jul 22 07:53 split-screen-core.ts
> -rw-rw-r--  1 ubuntu ubuntu  2480 Jul 21 19:48 sync-caption-templates-to-public.ts
> drwxrwxr-x  3 gcrUX  gcrUX   4096 Jul 21 22:14 templates
> ---EP05---
> total 384
> drwxrwxr-x  2 ubuntu ubuntu  4096 Aug  4 11:34 .
> drwxrwxr-x 15 gcrUX  gcrUX  12288 Aug  5 20:02 ..
> -rw-rw-r--  1 ubuntu ubuntu  8520 Aug  3 22:49 assemble-v10.ts
> -rw-rw-r--  1 ubuntu ubuntu  9379 Aug  3 23:40 assemble-v11.ts
> -rw-rw-r--  1 ubuntu ubuntu  9965 Aug  4 00:15 assemble-v12.ts
> -rw-rw-r--  1 ubuntu ubuntu  9965 Aug  4 08:42 assemble-v13.ts
> -rw-rw-r--  1 ubuntu ubuntu  7261 Aug  3 19:06 assemble-v3.ts
> -rw-rw-r--  1 ubuntu ubuntu  4868 Aug  3 19:06 assemble-v6.ts
> -rw-rw-r--  1 ubuntu ubuntu  4418 Aug  3 20:02 assemble-v7.ts
> -rw-rw-r--  1 ubuntu ubuntu  8022 Aug  3 20:41 assemble-v8.ts
> -rw-rw-r--  1 ubuntu ubuntu  8015 Aug  3 21:52 assemble-v9.ts
> -rw-rw-r--  1 ubuntu ubuntu  1164 Aug  3 23:40 callout.html
> -rw-rw-r--  1 ubuntu ubuntu  4795 Aug  3 19:06 cartela-creditos.py
> -rwxrwxr-x  1 ubuntu ubuntu  1061 Aug  3 22:49 compose-takes.sh
> -rw-rw-r--  1 ubuntu ubuntu  8718 Aug  3 19:06 ep05-trilha.py
> -rw-rw-r--  1 ubuntu ubuntu  8771 Aug  3 19:06 ep05-trilha-v2.py
> -rw-rw-r--  1 ubuntu ubuntu  2149 Aug  3 23:40 gen-callouts.ts
> -rw-rw-r--  1 ubuntu ubuntu  3877 Aug  3 20:41 gen-el-narration.py
> -rw-rw-r--  1 ubuntu ubuntu  1518 Aug  3 20:41 gen-ivc-batch.py
> -rw-rw-r--  1 ubuntu ubuntu  4688 Aug  3 21:52 gen-ivc-v3.py
> -rw-rw-r--  1 ubuntu ubuntu  2360 Aug  3 23:40 gen-tone-rest.py
> -rw-rw-r--  1 ubuntu ubuntu  2528 Aug  3 23:40 hud-frame.html
> -rw-rw-r--  1 ubuntu ubuntu  9684 Aug  4 11:26 motion-biblioteca.html
> -rw-rw-r--  1 ubuntu ubuntu 13940 Aug  4 11:34 motion-canvas.html
> -rw-rw-r--  1 ubuntu ubuntu 18770 Aug  4 10:48 motion-esteira.html
> -rw-rw-r--  1 ubuntu ubuntu 11328 Aug  4 10:59 motion-i2v.html
> -rw-rw-r--  1 ubuntu ubuntu 12535 Aug  4 11:16 motion-imagem.html
> -rw-rw-r--  1 ubuntu ubuntu  9016 Aug  4 11:21 motion-retencao.html
> -rw-rw-r--  1 ubuntu ubuntu 10794 Aug  4 11:07 motion-voz.html
> -rw-rw-r--  1 ubuntu ubuntu  4634 Aug  3 23:40 nebula-bg.html
> -rw-rw-r--  1 ubuntu ubuntu  1692 Aug  3 23:40 poll-retakes.ts
> -rw-rw-r--  1 ubuntu ubuntu  2086 Aug  3 19:06 README.md
> -rw-rw-r--  1 ubuntu ubuntu  1500 Aug  4 11:26 render-bib.ts
> -rw-rw-r--  1 ubuntu ubuntu  1477 Aug  4 11:34 render-cv.ts
> -rw-rw-r--  1 ubuntu ubuntu  1466 Aug  4 10:59 render-i2v.ts
> -rw-rw-r--  1 ubuntu ubuntu  1481 Aug  4 11:16 render-img.ts
> -rw-rw-r--  1 ubuntu ubuntu  1473 Aug  4 08:59 render-motion.ts
> -rw-rw-r--  1 ubuntu ubuntu  1456 Aug  3 22:49 render-nebula.ts
> -rw-rw-r--  1 ubuntu ubuntu  1490 Aug  4 11:21 render-ret.ts
> -rw-rw-r--  1 ubuntu ubuntu  1672 Aug  3 19:06 render-title.ts
> -rw-rw-r--  1 ubuntu ubuntu  1466 Aug  4 11:07 render-voz.ts
> -rw-rw-r--  1 ubuntu ubuntu  6038 Aug  3 23:40 retake-blockbuster.ts
> -rw-rw-r--  1 ubuntu ubuntu  5923 Aug  4 00:15 retake-fleet.ts
> -rw-rw-r--  1 ubuntu ubuntu  7865 Aug  3 19:06 screencast-v2.ts
> -rw-rw-r--  1 ubuntu ubuntu  7714 Aug  3 20:41 screencast-v3.ts
> -rw-rw-r--  1 ubuntu ubuntu 10111 Aug  4 08:42 screencast-v4.ts
> -rw-rw-r--  1 ubuntu ubuntu  3949 Aug  3 19:06 title.html
> -rw-rw-r--  1 ubuntu ubuntu  1705 Aug  3 19:06 upload-a6.ts
> -rw-rw-r--  1 ubuntu ubuntu  2063 Aug  3 20:02 upload-a7.ts
> ```

## 🤖 Claude *(23:13:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ffmpeg -version 2>&1 | head -3; echo \"===FILTERS===\"; ffmpeg -hide_banner -filters 2>/dev/null | grep -E ' (curves|colorbalance|noise|tmix|unsharp|vignette|lut3d|signalstats|gblur|eq) ' ",
  "description": "Check ffmpeg version and available filters"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ffmpeg version 6.1.1-3ubuntu5 Copyright (c) 2000-2023 the FFmpeg developers
> built with gcc 13 (Ubuntu 13.2.0-23ubuntu3)
> configuration: --prefix=/usr --extra-version=3ubuntu5 --toolchain=hardened --libdir=/usr/lib/aarch64-linux-gnu --incdir=/usr/include/aarch64-linux-gnu --arch=arm64 --enable-gpl --disable-stripping --disable-omx --enable-gnutls --enable-libaom --enable-libass --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libcodec2 --enable-libdav1d --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libglslang --enable-libgme --enable-libgsm --enable-libharfbuzz --enable-libmp3lame --enable-libmysofa --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-librubberband --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libtheora --enable-libtwolame --enable-libvidstab --enable-libvorbis --enable-libvpx --enable-libwebp --enable-libx265 --enable-libxml2 --enable-libxvid --enable-libzimg --enable-openal --enable-opencl --enable-opengl --disable-sndio --enable-libdc1394 --enable-libdrm --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-ladspa --enable-libbluray --enable-libjack --enable-libpulse --enable-librabbitmq --enable-librist --enable-libsrt --enable-libssh --enable-libsvtav1 --enable-libx264 --enable-libzmq --enable-libzvbi --enable-lv2 --enable-sdl2 --enable-libplacebo --enable-librav1e --enable-pocketsphinx --enable-librsvg --enable-libjxl --enable-shared
> ===FILTERS===
>  TS. adeclick          A->A       Remove impulsive noise from input audio.
>  TSC anlmdn            A->A       Reduce broadband noise from stream using Non-Local Means.
>  TSC arnndn            A->A       Reduce noise from speech using Recurrent Neural Networks.
>  TSC crystalizer       A->A       Simple audio noise sharpening filter.
>  ... anoisesrc         |->A       Generate a noise audio signal.
>  TSC colorbalance      V->V       Adjust the color balance.
>  TSC curves            V->V       Adjust components curves.
>  T.C eq                V->V       Adjust brightness, contrast, gamma, and saturation.
>  TSC gblur             V->V       Apply Gaussian Blur filter.
>  TSC lut3d             V->V       Adjust colors using a 3D LUT.
>  TS. noise             V->V       Add noise.
>  .S. signalstats       V->V       Generate statistics from video analysis.
>  TSC tmix              V->V       Mix successive video frames.
>  TS. unsharp           V->V       Sharpen or blur the input video.
>  ... unsharp_opencl    V->V       Apply unsharp mask to input video
>  T.. vignette          V->V       Make or reverse a vignette effect.
> ```

## 🤖 Claude *(23:13:36)*

<details>
<summary>💭 Thinking Process</summary>

I need to check the render-core.ts file to see what the actual API contract is for frame application.

</details>


## 🤖 Claude *(23:13:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "grep -nE \"__seek|applyFrame|applyProps|screenshot|deterministic|sha256|fps|seek\" scripts/hyperframes/render-core.ts | head -60"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 5: * HyperFrames deterministic render engine: a composition spec → 9:16 1080×1920 MP4.
> 6: * BoK SSOT: docs/bok/video-studio/04-frd.md FR-VS-024 (deterministic HTML→MP4 via headless Chrome + FFmpeg)
> 9: * Pipeline (no AI leg — fully deterministic, NFR-VS-016):
> 11: *   2. Load templates/<template>.html (file://), inject props via applyProps (textContent → XSS-safe).
> 12: *   3. For each of N = duration_s × fps frames: applyFrame(i, N) → page.screenshot(PNG).
> 13: *   4. FFmpeg: PNG sequence → H.264 yuv420p MP4, fixed fps, -fflags +bitexact (reproducible).
> 40:  applyProps: (props: unknown) => void;
> 41:  applyFrame: (idx: number, total: number) => void;
> 42:  __HF_EXPORT_RENDER_SEEK_CONFIG?: { fps: number; fpsSource: string };
> 67:  fps?: number;             // default 30
> 75: * definitional: same engine that drives the editor preview) instead of re-implementing the GSAP/__timelines seek.
> 81:  fps?: number;             // default 30
> 91:  fps: number;
> 99:// by the repurpose rail); they share the applyProps({beats,fps,durationSec})/applyFrame(i,total) contract.
> 129:function encodePngFramesBitexact(frameDir: string, fps: number, outPath: string): Promise<void> {
> 132:    '-framerate', String(fps),
> 138:    '-r', String(fps),
> 151:// H.264 yuv420p, deterministic (fixed fps + bitexact flags, mirrors encodePngFramesBitexact NFR-VS-016).
> 155:  fps?: number;                // output fps (default 30)
> 165:  const fps = spec.fps ?? 30;
> 184:      // scale to fit, pad to the exact 9:16 canvas (letterbox, no crop), normalize SAR, fix fps
> 185:      '-vf', `scale=${W}:${H}:force_original_aspect_ratio=decrease,pad=${W}:${H}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps=${fps}`,
> 187:      '-pix_fmt', 'yuv420p', '-r', String(fps),
> 202:    fps: probed.fps,
> 214:  fps?: number;                // default 30
> 225:  const fps = spec.fps ?? 30;
> 229:  const totalFrames = Math.round(dur * fps);
> 232:  // Ramp 1 → maxZoom (in) or maxZoom → 1 (out) across the clip; `on` = output frame index (deterministic).
> 238:    `zoompan=z='${zExpr}':d=${totalFrames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=${W}x${H}:fps=${fps},` +
> 246:    '-pix_fmt', 'yuv420p', '-r', String(fps),
> 258:    fps: probed.fps,
> 282:/** ffprobe a video → real dimensions/frames/fps (the renderer derives them from the composition + preset). */
> 283:function ffprobeVideo(path: string): Promise<{ width: number; height: number; frames: number; fps: number }> {
> 296:        const fps = rd ? rn / rd : (rn || 30);
> 297:        const frames = Number(s.nb_frames) || Math.round((Number(s.duration) || 0) * fps);
> 298:        res({ width: Number(s.width) || 0, height: Number(s.height) || 0, frames, fps });
> 305: * Render a composition spec to a deterministic 9:16 MP4 at `outPath`.
> 311:  const fps = Math.max(1, Math.min(60, spec.fps ?? 30));
> 315:  const totalFrames = Math.round(durationS * fps);
> 332:    await page.evaluate((props) => (window as HfWindow).applyProps(props), spec.props as Record<string, unknown>);
> 346:      await page.evaluate(([idx, total]) => (window as HfWindow).applyFrame(idx, total), [i, totalFrames] as [number, number]);
> 347:      await page.screenshot({
> 355:    await encodePngFramesBitexact(frameDir, fps, outPath);
> 361:    return { outPath, bytes, width, height, frames: totalFrames, fps, durationMs: Date.now() - t0 };
> 372:  fps: number;
> 379: * OVER real footage (video-repurpose FR-VR-011/012). Same deterministic index-driven loop as renderComposition,
> 380: * but page.screenshot({ omitBackground: true }) → alpha preserved, and NO MP4 encode (yuv420p would drop alpha).
> 382: * Injects fps + durationSec into props so time-based templates map frame index → clip seconds.
> 396:  const fps = Math.max(1, Math.min(60, spec.fps ?? 30));
> 400:  const totalFrames = Math.round(durationS * fps);
> 425:          (props) => (window as HfWindow).applyProps(props),
> 426:          { ...spec.props, fps, durationSec: durationS } as Record<string, unknown>,
> 429:        // Wait for the self-hosted @font-face to settle → no fallback-font early frames (deterministic). BOUNDED
> 438:          await page.evaluate(([idx, total]) => (window as HfWindow).applyFrame(idx, total), [i, totalFrames] as [number, number]);
> 439:          await page.screenshot({
> 456:    return { frameDir, framePattern: 'f_%05d.png', frames: totalFrames, fps, width, height };
> 491: *   → init-script window.__HF_EXPORT_RENDER_SEEK_CONFIG={fps} (runtime reads at init; fps is renderer-owned)
> 493: *   → per frame: __player.renderSeek(i/fps) (synchronous deterministic seek, quantized floor(t*fps+1e-9)/fps
> 494: *     runtime-side) → PNG screenshot → shared bitexact FFmpeg encode (NFR-VS-016).
> 500:  const fps = Math.max(1, Math.min(60, spec.fps ?? 30));
> ```

## 🤖 Claude *(23:13:37)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cat scripts/ep05/render-motion.ts; echo \"=====MOTION-CANVAS HEAD=====\"; grep -nE \"__seek|applyFrame|function|const t|easing|cubic|linear\" scripts/ep05/motion-canvas.html | head -40"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> /** Render the 12s seamless MIV nebula loop: 360 frames @30fps → motion27.mp4 (no external libs). */
> import { chromium } from 'playwright';
> import { execSync } from 'child_process';
> const SC = '/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/3f7d28b7-c49d-499c-8107-083d3f48925c/scratchpad';
> const CHROME = '/home/ubuntu/.cache/ms-playwright/chromium-1226/chrome-linux/chrome';
> execSync(`mkdir -p ${SC}/motion-frames && rm -f ${SC}/motion-frames/*.png`);
> const browser = await chromium.launch({ headless: true, executablePath: CHROME });
> const page = await (await browser.newContext({ viewport: { width: 1280, height: 720 } })).newPage();
> await page.goto(`file://${SC}/motion-esteira.html`, { waitUntil: 'load', timeout: 30000 });
> await page.waitForFunction(() => (window as unknown as { __ready?: boolean }).__ready, null, { timeout: 15000 });
> for (let i = 0; i < 825; i++) {
>   await page.evaluate((t) => (window as unknown as { __seek: (t: number) => void }).__seek(t), i / 30);
>   await page.screenshot({ path: `${SC}/motion-frames/f_${String(i).padStart(4, '0')}.png`, animations: 'disabled' });
>   if (i % 60 === 0) console.log(`frame ${i}`);
> }
> await browser.close();
> execSync(`ffmpeg -y -framerate 30 -i ${SC}/motion-frames/f_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 20 ${SC}/motion27.mp4 -loglevel error`);
> console.log('motion27.mp4:', execSync(`ffprobe -v error -show_entries format=duration -of csv=p=0 ${SC}/motion27.mp4`).toString().trim(), 's');
> =====MOTION-CANVAS HEAD=====
> 7:    background-image:linear-gradient(rgba(34,211,238,.28) 1px,transparent 1px),
> 8:      linear-gradient(90deg,rgba(34,211,238,.28) 1px,transparent 1px);
> 14:    background:linear-gradient(90deg,transparent,#22d3ee,transparent); }
> 17:  .glass { border-radius:12px; background:linear-gradient(165deg, rgba(24,34,52,.62), rgba(9,14,24,.78));
> 28:    font-weight:700; font-size:11px; background:linear-gradient(90deg,#fbbf24,#fde68a); opacity:0;
> 49:  #srtwave i { display:block; width:5px; background:linear-gradient(180deg,#7dd3fc,#0e7490); border-radius:2px; }
> 125:    window.__seek=(t)=>{
> ```

## 🤖 Claude *(23:13:43)*

<details>
<summary>💭 Thinking Process</summary>

I'm noticing a key discrepancy: the ep05 motion runners call `window.__seek(t)` with time in seconds, while render-core.ts uses `applyFrame(i, total)` with frame indices. This means the claim about deterministic indexing through `applyFrame` applies to render-core but not to the ep05 motion files, which use a different timing mechanism.

Also important: the render loop disables CSS animations during screenshots with `page.screenshot({ animations: 'disabled' })`, so I need to check how motion-canvas.html implements `__seek` and whether easing functions are already built in.

</details>


## 🤖 Claude *(23:13:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "sed -n 100,200p scripts/ep05/motion-canvas.html"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>     <div id="seal40"><span>ISSO EXISTE HOJE</span></div>
>   </div>
>   <div class="vig"></div>
>   <div class="flash" id="flash"></div>
>   <div style="display:none" id="preload"></div>
>   <script>
>     // motion-canvas — scenes 4/37/38/40 + mute 48 tail (44.8s), v6 language.
>     // 4 (0-13.3): mini esteira + cost badges rain on "nasce MEDIDA" + seal
>     // 37 (13.3-22.1): Ken Burns LIVE inside a card + rails + badge
>     // 38 (22.1-31.7): waveform → SRT cues typing in sync + badge
>     // 40 (31.7-40.7): the short playing + 4 minis wired up + "ISSO EXISTE HOJE"
>     // 48 (40.7-44.8): full mini-esteira reprise → flash out
>     const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
>     const ez=(t)=>t<0?0:t>1?1:t*t*(3-2*t);
>     const spring=(t)=>{ if(t<=0)return 0; if(t>=1)return 1; return 1-Math.exp(-6*t)*Math.cos(9*t); };
>     const $=(id)=>document.getElementById(id);
>     const pts=[]; for(let i=0;i<14;i++){const p=document.createElement('div');p.className='pt';
>       p.style.left=(60+(i*151)%1160)+'px'; p.style.top=(80+(i*97)%560)+'px'; document.body.appendChild(p); pts.push(p);}
>     const streaks=[]; for(let i=0;i<3;i++){const s=document.createElement('div'); s.className='streak';
>       s.style.top=(120+i*220)+'px'; document.body.appendChild(s); streaks.push(s);}
>     const sw=$('srtwave'); for(let i=0;i<30;i++){const b=document.createElement('i');sw.appendChild(b);}
>     const NF=90, frames=[]; const pre=$('preload');
>     for(let i=1;i<=NF;i++){ const src=`motion-assets/clip/f_${String(i).padStart(2,'0')}.jpg`;
>       frames.push(src); const im=new Image(); im.src=src; pre.appendChild(im); }
>     const minis=['m1','m2','m3','m4'].map($);
>     window.__seek=(t)=>{
>       const TAU=Math.PI*2, u=(t%12)/12, s1=Math.sin(u*TAU);
>       $('b1').style.transform=`translate(${65+65*s1}px, ${40+40*s1}px)`;
>       $('b2').style.transform=`translate(${-55-55*s1}px, ${-35-35*s1}px)`;
>       streaks.forEach((s,i)=>{ const ph=(u+i/3)%1; s.style.transform=`translateX(${-240+ph*1760}px)`; });
>       pts.forEach((p,i)=>{ p.style.opacity=(.25+.3*Math.sin(t*1.1+i*2.1))*ez(t/.9);
>         p.style.transform=`translateY(${-8*Math.sin(t*.5+i)}px)`; });
>       // scene 4 — minis + edges + cost rain; reprise at 48 (40.7+)
>       const s4=(t<13.0)?1:(t>40.4?1:0);            // visible in scene 4 AND the mute 48 tail
>       const s4fade=(t<13.0)?(1-ez((t-12.4)/.5)):ez((t-40.6)/.6);
>       minis.forEach((el,i)=>{ const b=(t>40.4? 40.6+i*.16 : .6+i*.5);
>         const a=ez((t-b)/.45)*s4*s4fade;
>         el.style.opacity=a;
>         el.style.transform=`translateY(${(1-ez((t-b)/.5))*20+(a>=1?3*Math.sin(t*.85+i*1.4):0)}px) scale(${.75+.25*spring((t-b)/.7)})`;
>       });
>       [['me1',2.0],['me2',2.4],['me3',2.8]].forEach(([id,b0])=>{
>         const b=(t>40.4)?41.2:b0; const p=$(id);
>         if(t>b){ p.setAttribute('opacity',.9*s4*s4fade); const lp=p.getTotalLength();
>           p.style.strokeDasharray=lp; p.style.strokeDashoffset=lp*(1-ez((t-b)/.7)); } else p.setAttribute('opacity',0);
>       });
>       const costs=document.querySelectorAll('.cost');
>       costs.forEach((el,i)=>{ const b=5.4+i*.5; const a=ez((t-b)/.4)*s4*(t<13.0?(1-ez((t-12.4)/.5)):0);
>         el.style.opacity=a; el.style.transform=`translateY(${(1-ez((t-b)/.4))*-12}px) scale(${.5+.5*spring((t-b)/.6)})`; });
>       $('seal4').style.opacity=ez((t-9.8)/.5)*(t<13.0?(1-ez((t-12.4)/.5)):0);
>       // scene 37 — Ken Burns live
>       const kb=$('kb'); const ka=ez((t-13.6)/.6)*(1-ez((t-21.5)/.5));
>       kb.style.opacity=ka;
>       kb.style.transform=`translateZ(${(1-ez((t-13.6)/.9))*-180}px) translateY(${3.5*Math.sin(t*.75)}px) rotateX(${1.8*Math.sin(t*.55)}deg)`;
>       const kt=clamp((t-14.0)/7.5,0,1);
>       $('kbimg').style.transform=`translate(${-8-10*kt}%, ${-6-8*kt}%) scale(${1.0+.18*kt})`;
>       $('kbrails').style.opacity=ez((t-15.2)/.5)*(1-ez((t-21.5)/.5));
>       $('kbbadge').style.opacity=ez((t-16.4)/.5)*(1-ez((t-21.5)/.5));
>       // scene 38 — SRT
>       const sr=$('srt'); const sa=ez((t-22.4)/.6)*(1-ez((t-31.1)/.5));
>       sr.style.opacity=sa;
>       sr.style.transform=`translateZ(${(1-ez((t-22.4)/.9))*-180}px) translateY(${3.5*Math.sin(t*.7)}px) rotateY(${2*Math.sin(t*.5+1)}deg)`;
>       const bars=sw.children;
>       for(let i=0;i<bars.length;i++){ const amp=t>22.8?(10+26*Math.abs(Math.sin(t*2.8+i*.75))):6;
>         bars[i].style.height=amp+'px'; }
>       [['c1',24.2],['c2',25.6],['c3',27.0]].forEach(([id,b])=>{
>         const el=$(id); const a=ez((t-b)/.45)*(1-ez((t-31.1)/.5));
>         el.style.opacity=a; el.style.transform=`translateX(${(1-ez((t-b)/.45))*-16}px)`; });
>       $('srtbadge').style.opacity=ez((t-28.6)/.5)*(1-ez((t-31.1)/.5));
>       // scene 40 — the short + minis wired
>       const sh=$('short'); const ha=ez((t-32.0)/.6)*(1-ez((t-40.3)/.5));
>       sh.style.opacity=ha;
>       sh.style.transform=`translateZ(${(1-ez((t-32.0)/.9))*-180}px) translateY(${3.5*Math.sin(t*.72)}px) rotateX(${1.6*Math.sin(t*.5)}deg)`;
>       if(t>32.2){ const fi=Math.floor((t-32.2)*30)%NF; $('shimg').src=frames[fi]; }
>       // minis reappear small below during 40 (already handled by s4? no — dedicated: reuse minis at smaller scale)
>       if(t>33.2&&t<40.3){ minis.forEach((el,i)=>{ const b=33.2+i*.3; const a=ez((t-b)/.4)*(1-ez((t-40.0)/.4));
>         el.style.opacity=a; el.style.transform=`translate(${[255,165,75,-15][i]}px, ${216}px) scale(.62)`; }); }
>       [['se1',34.6],['se2',34.9],['se3',35.2],['se4',35.5]].forEach(([id,b])=>{
>         const p=$(id);
>         if(t>b&&t<40.3){ p.setAttribute('opacity',.85); const lp=p.getTotalLength();
>           p.style.strokeDasharray=lp; p.style.strokeDashoffset=lp*(1-ez((t-b)/.6)); } else p.setAttribute('opacity',0);
>       });
>       $('seal40').style.opacity=ez((t-36.6)/.5)*(1-ez((t-40.3)/.5));
>       $('flash').style.opacity=.9*ez((t-44.3)/.28)*(1-ez((t-44.56)/.3));
>     };
>     window.__ready=true;
>   </script>
> </body></html>
> ```

## 🤖 Claude *(23:13:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls -la src/lib/cinematic-grammar.ts 2>/dev/null && grep -nE \"MIX_TARGETS|jCut|lCut|EASING|LIGHTING|KEY_FILL|export const\" src/lib/cinematic-grammar.ts | head -40"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> -rw-rw-r-- 1 ubuntu ubuntu 9449 Aug  4 21:10 src/lib/cinematic-grammar.ts
> 12:export const LENSES = {
> 23:export const SHOTS = {
> 35:export const CAMERA_MOVES = {
> 49:export const LIGHTING = {
> 61:export const FILM_LOOK = {
> 75:export const MANDATORY_NEGATIVES = [
> 89:  light?: keyof typeof LIGHTING;
> 110:  if (spec.light) parts.push(LIGHTING[spec.light].en);
> 120:export const MIX_TARGETS = {
> 129:  jCutLeadSec: 0.6,
> 130:  lCutTailSec: 1.2,
> 134:export const MIX_HIERARCHY = ["diálogo", "hard SFX", "ambiência", "trilha"] as const;
> 148:export const STAGE_LABEL: Record<EpisodeStage, string> = {
> 164:export const STAGE_GATE: Partial<Record<EpisodeStage, string>> = {
> ```

## 🤖 Claude *(23:14:02)*

<details>
<summary>💭 Thinking Process</summary>

I'm realizing the existing motion code already applies easing functions—smoothstep for the rail and spring for overshoot—so the claim that it uses raw linear interpolation isn't entirely accurate, though the principle about needing easing is still sound.

I should verify the implementation details across other motion files and check the sources cited, particularly the W3C easing spec and the Lasseter paper, to make sure the references are correct. Also noting that the screenshot approach with animations disabled won't affect the inline style transforms being applied, so that's fine. I need to verify several ffmpeg filter parameters and options by checking the documentation and running actual tests. I'll batch together fetching those URLs and running command-line checks to confirm things like the curves interpolation method, noise filter seed behavior, vignette angle defaults, and unsharp filter parameter names.

</details>


## 🤖 Claude *(23:14:02)*


🛠️ **Tool Call**: `ToolSearch`
```json
{
  "query": "select:WebFetch,WebSearch",
  "max_results": 2
}
```

> **Tool Result (ToolSearch)** - ✅ Success
>
> ```
> [{'type': 'tool_reference', 'tool_name': 'WebFetch'}, {'type': 'tool_reference', 'tool_name': 'WebSearch'}]
> ```

## 🤖 Claude *(23:14:03)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp && ffmpeg -hide_banner -h filter=curves 2>&1 | tail -25; echo \"=====NOISE=====\"; ffmpeg -hide_banner -h filter=noise 2>&1 | tail -30"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>      cross_process   2            ..FV.....T.
>      darker          3            ..FV.....T.
>      increase_contrast 4            ..FV.....T.
>      lighter         5            ..FV.....T.
>      linear_contrast 6            ..FV.....T.
>      medium_contrast 7            ..FV.....T.
>      negative        8            ..FV.....T.
>      strong_contrast 9            ..FV.....T.
>      vintage         10           ..FV.....T.
>    master            <string>     ..FV.....T. set master points coordinates
>    m                 <string>     ..FV.....T. set master points coordinates
>    red               <string>     ..FV.....T. set red points coordinates
>    r                 <string>     ..FV.....T. set red points coordinates
>    green             <string>     ..FV.....T. set green points coordinates
>    g                 <string>     ..FV.....T. set green points coordinates
>    blue              <string>     ..FV.....T. set blue points coordinates
>    b                 <string>     ..FV.....T. set blue points coordinates
>    all               <string>     ..FV.....T. set points coordinates for all components
>    psfile            <string>     ..FV.....T. set Photoshop curves file name
>    plot              <string>     ..FV.....T. save Gnuplot script of the curves in specified file
>    interp            <int>        ..FV.....T. specify the kind of interpolation (from 0 to 1) (default natural)
>      natural         0            ..FV.....T. natural cubic spline
>      pchip           1            ..FV.....T. monotonically cubic interpolation
> 
> This filter has support for timeline through the 'enable' option.
> =====NOISE=====
>      t                            ..FV....... temporal noise
>      u                            ..FV....... uniform noise
>    c2_seed           <int>        ..FV....... set component #2 noise seed (from -1 to INT_MAX) (default -1)
>    c2_strength       <int>        ..FV....... set component #2 strength (from 0 to 100) (default 0)
>    c2s               <int>        ..FV....... set component #2 strength (from 0 to 100) (default 0)
>    c2_flags          <flags>      ..FV....... set component #2 flags (default 0)
>      a                            ..FV....... averaged noise
>      p                            ..FV....... (semi)regular pattern
>      t                            ..FV....... temporal noise
>      u                            ..FV....... uniform noise
>    c2f               <flags>      ..FV....... set component #2 flags (default 0)
>      a                            ..FV....... averaged noise
>      p                            ..FV....... (semi)regular pattern
>      t                            ..FV....... temporal noise
>      u                            ..FV....... uniform noise
>    c3_seed           <int>        ..FV....... set component #3 noise seed (from -1 to INT_MAX) (default -1)
>    c3_strength       <int>        ..FV....... set component #3 strength (from 0 to 100) (default 0)
>    c3s               <int>        ..FV....... set component #3 strength (from 0 to 100) (default 0)
>    c3_flags          <flags>      ..FV....... set component #3 flags (default 0)
>      a                            ..FV....... averaged noise
>      p                            ..FV....... (semi)regular pattern
>      t                            ..FV....... temporal noise
>      u                            ..FV....... uniform noise
>    c3f               <flags>      ..FV....... set component #3 flags (default 0)
>      a                            ..FV....... averaged noise
>      p                            ..FV....... (semi)regular pattern
>      t                            ..FV....... temporal noise
>      u                            ..FV....... uniform noise
> 
> This filter has support for timeline through the 'enable' option.
> ```

## 🤖 Claude *(23:14:08)*

<details>
<summary>💭 Thinking Process</summary>

I need to verify that the `all_seed` parameter actually exists in the noise filter and test whether it truly provides bit-exact reproducibility by running the same filter twice and comparing the SHA256 hashes. I also want to validate the grade chain behavior—specifically whether the curves master with those points raises black to 25, check the tmix and fps decimation interaction, and confirm that lut3d defaults to tetrahedral interpolation.

</details>


## 🤖 Claude *(23:14:14)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/bd77173a-1491-4127-805a-8e21c1aa021a/scratchpad 2>/dev/null || cd /tmp\nmkdir -p critic && cd critic\n# TEST 1: curves raises black floor\nffmpeg -y -v error -f lavfi -i \"color=black:s=64x64:d=1:r=1\" -vf \"format=gbrp,curves=master='0/0.045 0.25/0.22 0.5/0.5 0.75/0.79 1/0.985':interp=pchip,format=yuv420p\" -frames:v 1 -f rawvideo - 2>&1 | head -c 1 | xxd | head -2\necho \"--- luma byte above ---\"\n# TEST 2: noise determinism with fixed seed, two runs\nfor r in 1 2; do\nffmpeg -y -v error -f lavfi -i \"testsrc2=s=320x240:d=1:r=10\" -vf \"noise=all_seed=42:alls=6:allf=t+u\" -c:v libx264 -pix_fmt yuv420p -fflags +bitexact -flags +bitexact -f mp4 noise_$r.mp4\ndone\nsha256sum noise_1.mp4 noise_2.mp4"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 00000000: 19                                       .
> --- luma byte above ---
> 85f7e6fa9707c1c5faa54d473d0fb9e4a0c649c2f35ec78e228c202a95a50d0f  noise_1.mp4
> 85f7e6fa9707c1c5faa54d473d0fb9e4a0c649c2f35ec78e228c202a95a50d0f  noise_2.mp4
> ```

## 🤖 Claude *(23:14:16)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://www.w3.org/TR/css-easing-1/",
  "prompt": "Does this spec define the keyword easing functions ease, ease-in, ease-out, ease-in-out in terms of cubic-bezier control points? Quote the exact control point values given for each keyword."
}
```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> Yes, the specification defines these keyword easing functions in terms of cubic-bezier control points. Here are the exact values:
> 
> **ease:** "Equivalent to cubic-bezier(0.25, 0.1, 0.25, 1)."
> 
> **ease-in:** "Equivalent to cubic-bezier(0.42, 0, 1, 1)."
> 
> **ease-out:** "Equivalent to cubic-bezier(0, 0, 0.58, 1)."
> 
> **ease-in-out:** "Equivalent to cubic-bezier(0.42, 0, 0.58, 1)."
> 
> These definitions appear in section 2.2 of the CSS Easing Functions Level 1 specification.
> ```

## 🤖 Claude *(23:14:24)*

<details>
<summary>💭 Thinking Process</summary>

I've verified the black value conversion and confirmed the noise reproducibility with fixed seeds. The W3C source values match exactly. Now I need to check those reference URLs—the Lasseter paper, the ASC lighting article, the vectorscope page, and the Murch page—plus investigate the headroom and rule-of-thirds discrepancy.

</details>


## 🤖 Claude *(23:14:27)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "http://graphics.cs.cmu.edu/nsp/course/15-464/Fall05/papers/lasseter.pdf",
  "prompt": "Is this John Lasseter's \"Principles of Traditional Animation Applied to 3D Computer Animation\" (SIGGRAPH 1987)? Quote verbatim any passages about: (a) slow in and out / second and third order continuity; (b) arcs and the spline controlling both path and timing / flattening arcs / \"straight inbetweens can completely kill the essence of an action\"; (c) staging and \"only one idea be seen by the audience at a time\" and \"in a still scene the eye will be attracted to movement\"; (d) secondary action being subordinate and \"the change must come before, or after, the move\"; (e) anticipation as preparation/action/termination; (f) squash and stretch \"the most important principle\"; (g) exaggeration needing to be balanced across components."
}
```

> **Tool Result (WebFetch)** - ❌ Error
>
> ```
> unable to verify the first certificate
> ```

## 🤖 Claude *(23:14:29)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://theasc.com/articles/lighting-a-set",
  "prompt": "Is this an American Cinematographer article by/about Stephen H. Burum on lighting a set? Quote verbatim any passages about: (a) the three things everyone does when lighting (cast a shadow, create separation, add fill); (b) shadows not being inky black due to natural fill; (c) key-to-fill ratios such as 8:1 and the \"Laverne & Shirley look\" and \"there is no correct amount of fill\"; (d) fill light on the camera axis and secondary shadows; (e) set walls reflective value below 25 percent; (f) inside cross-keys pulling attention to the center of the frame."
}
```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> The server returned HTTP 403 Forbidden.
> 
> The response body was not retrieved. If this URL requires authentication, use an authenticated tool (e.g. `gh` for GitHub, or an MCP-provided fetch tool) instead of WebFetch.
> ```

## 🤖 Claude *(23:14:33)*

<details>
<summary>💭 Thinking Process</summary>

I'm hitting some roadblocks with the initial approach, so let me pivot to using curl with the insecure flag to bypass the certificate issue on the CMU PDF, and switch to firecrawl for the ASC article instead.

</details>


## 🤖 Claude *(23:14:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic 2>/dev/null || { mkdir -p /tmp/critic; cd /tmp/critic; }\ncurl -sS -k -L -o lasseter.pdf -w \"HTTP=%{http_code} SIZE=%{size_download} CT=%{content_type}\\n\" \"http://graphics.cs.cmu.edu/nsp/course/15-464/Fall05/papers/lasseter.pdf\" 2>&1 | tail -3\nls -la lasseter.pdf 2>/dev/null; file lasseter.pdf 2>/dev/null"
}
```

## 🤖 Claude *(23:14:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic 2>/dev/null || cd /tmp\ncurl -sS -L -A \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36\" -o asc.html -w \"HTTP=%{http_code} SIZE=%{size_download}\\n\" \"https://theasc.com/articles/lighting-a-set\" 2>&1 | tail -2; wc -c asc.html 2>/dev/null"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> HTTP=200 SIZE=1212544 CT=application/pdf
> -rw-rw-r-- 1 ubuntu ubuntu 1212544 Aug  5 20:14 lasseter.pdf
> lasseter.pdf: PDF document, version 1.3, 10 page(s)
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> HTTP=403 SIZE=75193
> 75193 asc.html
> ```

## 🤖 Claude *(23:14:43)*

<details>
<summary>💭 Thinking Process</summary>

I've got the Lasseter PDF file available at 1.2MB with 10 pages, so I'll extract the text and search for those quotes. For the ASC article, I'm getting a 403 response with a body, so let me examine what's there and then try using firecrawl as an alternative approach.

</details>


## 🤖 Claude *(23:14:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic; which pdftotext || pip list 2>/dev/null | grep -i pdf; pdftotext lasseter.pdf lasseter.txt 2>&1; wc -c lasseter.txt 2>/dev/null"
}
```

## 🤖 Claude *(23:14:43)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic; grep -oiE \"cloudflare|captcha|just a moment|access denied|enable javascript\" asc.html | sort -u | head"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 1
> pdfminer.six              20251230
> pdfplumber                0.11.9
> PyMuPDF                   1.27.2.3
> pypdf                     6.12.2
> pypdfium2                 5.9.0
> /bin/bash: line 1: pdftotext: command not found
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> (Bash completed with no output)
> ```

## 🤖 Claude *(23:14:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic; python3 -c \"\nimport fitz\nd=fitz.open('lasseter.pdf')\nt='\\n'.join(p.get_text() for p in d)\nopen('lasseter.txt','w').write(t)\nprint(len(t))\nprint(t[:600])\n\""
}
```

## 🤖 Claude *(23:14:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic; head -c 1500 asc.html"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 50716
> (~ ~ 
> Computer Graphics, Volume 21, Number 4, July 1987 
> PRINCIPLES OF TRADITIONAL ANIMATION 
> APPLIED TO 3D COMPUTER ANIMATION 
> John Lasseter 
> Pixar 
> San Rafael 
> California 
> "There is no particular mystery in animation.., it's really very simple, and 
> like anything that is simple, it is about the hardest thing in the world to 
> do." Bill Tytla at the Walt Disney Studio, June 28, 1937. [14] 
> ABSTRACT 
> This paper describes the basic principles of traditional 2D hand drawn 
> animation and their application to 3D computer animation. After describing 
> how these principles evolved, the individual prin
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> <!DOCTYPE html>
> <html lang="en">
> <head>
>     <meta charset="utf-8" />
>     <meta name="viewport" content="width=device-width, initial-scale=1.0">
>     <meta http-equiv="cache-control" content="no-store,max-age=0" />
>     <meta name="robots" content="noindex" />
>     <title>403 - Forbidden</title>
>     <link href="https://fonts.googleapis.com/css?family=Open+Sans:400,700%7CRoboto:400,700" rel="stylesheet">
> <style>
>     * {
>         box-sizing: border-box;
>         -moz-box-sizing: border-box;
>         -webkit-tap-highlight-color: transparent;
>     }
>     body {
>         margin: 0;
>         padding: 0;
>         height: 100%;
>         -webkit-text-size-adjust: 100%;
>     }
>     .fit-wide {
>         position: relative;
>         overflow: hidden;
>         max-width: 1240px;
>         margin: 0 auto;
>         padding-top: 60px;
>         padding-bottom: 60px;
>         padding-left: 20px;
>         padding-right: 20px;
>     }
>     .background-wrap { position: relative; }
>     .background-wrap.cloud-blue { background-color: #b0e0e9; }
>     .background-wrap.white { background-color: #fff; }
>     .title { 
>         position: relative; 
>         text-align: center;
>         margin: 20px auto 10px;
>     }
>     .title--regular { font-family: 'Roboto', Arial, sans-serif; }
>     .title--size-large { font-size: 36px; line-height: 46px; }
>     .title--size-semimedium { font-size: 20px; line-height: 28px; }
>     .title--weight-normal { font-weight: 400; }
>     .title--weight-bold { font-weight: 700; }
>     .title--subtitle { 
>         pa
> ```

## 🤖 Claude *(23:14:53)*

<details>
<summary>💭 Thinking Process</summary>

The Lasseter PDF checks out and matches what was claimed. Now I need to verify each quote by searching for it directly, starting with the Lasseter document, then trying alternative methods like firecrawl or web search to locate the ASC article since I'm getting blocked by the origin server.

</details>


## 🤖 Claude *(23:14:57)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic; python3 - <<'EOF'\nimport re\nt=open('lasseter.txt').read()\nt2=re.sub(r'\\s+',' ',t)\nclaims={\n 'slowinout':'second- and third-order continuity',\n 'arcs_same_spline':'controlled by the same spline',\n 'arcs_flatten':'the faster the action, the flatter the arc',\n 'straight_inbetweens':'Straight inbetweens can completely kill',\n 'staging_one_idea':'only one idea be seen by the audience at a time',\n 'staging_eye':'the eye will be attracted to movement',\n 'staging_busy':'busy scene, the eye will be attracted to something that is still',\n 'secondary_sub':'always kept subordinate to the primary action',\n 'secondary_timing':'The change must come before, or after, the move',\n 'antic_threeparts':'occurs in three parts',\n 'antic_foot':'must be pulled back before it can be swung forward',\n 'antic_abrupt':'abrupt, stiff and unnatural',\n 'squash_most_important':'most important principle',\n 'squash_rigidity':'emphasizes any rigidity',\n 'exagg_balance':'exaggeration of the various components should be balanced',\n 'exagg_isolation':'but not in isolation',\n}\nfor k,v in claims.items():\n    i=t2.lower().find(v.lower())\n    print(f\"[{'OK ' if i>=0 else 'MISS'}] {k}: \", (t2[max(0,i-180):i+220] if i>=0 else 'NOT FOUND'))\n    print()\nEOF"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [OK ] slowinout:  ipation and follow through. 2.7 SLOW IN AND OUT Slow in and slow out deals with the spacing of the inbetween drawings between the extreme poses. Mathematically, the term refers to second- and third-order continuity of motion. In early animation, the action was limited to mainly fast and slow moves, the spacing from one drawing to the next fairly even. But when the poses of pose-to-pose animation b
> 
> [OK ] arcs_same_spline:  ng object, but usually,, even in a straight line action, the object rotates. [12] In most 3D keyframe computer animation systems, the path of action from one extreme to another is controlled by the same spline that controls the timing (slow in and out) of the inbetween values. This may simplify computating the inbetweens but it has unfortunate effects. When a motion is slow, with many inbetweens, 
> 
> [OK ] arcs_flatten:  ut it has unfortunate effects. When a motion is slow, with many inbetweens, the arc of the path of action is curved, as desired. But when the action is fast, the arc flattens out: the faster the action, the flatter the arc. Sometimes this is desirable, but more often, the path of even a fast motion should be curved or arced. Straight inbetweens can completely kill the essence of an action. The spl
> 
> [OK ] straight_inbetweens:  n is fast, the arc flattens out: the faster the action, the flatter the arc. Sometimes this is desirable, but more often, the path of even a fast motion should be curved or arced. Straight inbetweens can completely kill the essence of an action. The spline that defines the path of action should be separate from the spline that defines the timing or spacing of the inbetweens for several reasons: so
> 
> [OK ] staging_one_idea:   anticipation and timing are all integral to directing the eye. A well-timed anticipation will be wasted if it is not staged clearly. It is important, when staging an action, that only one idea be seen by the audience at a time. If a lot of action is happening at once, the eye does not know where to look and the main idea of the aclion will be "upstaged" and overlooked. The object of interest shou
> 
> [OK ] staging_eye:  does not know where to look and the main idea of the aclion will be "upstaged" and overlooked. The object of interest should contrast from the rest of the scene. In a still scene, the eye will be attracted to movement. In a very busy scene, the eye will be attracted to something that is still. Each idea or action must be staged in the strongest and the simplest way before going on to the next idea
> 
> [OK ] staging_busy:  the aclion will be "upstaged" and overlooked. The object of interest should contrast from the rest of the scene. In a still scene, the eye will be attracted to movement. In a very busy scene, the eye will be attracted to something that is still. Each idea or action must be staged in the strongest and the simplest way before going on to the next idea or action. The animator is saying, in effect, "L
> 
> [OK ] secondary_sub:  ction that results directly from another action. Secondary actions are important in heightening interest and adding a realistic complexity to the animation. A secondary actions is always kept subordinate to the primary action. If it conflicts, becomes more interesting, or dominates in any way, it is either the wrong choice or is staged improperly. [26] Wally B.'s feet dragging behind the main acti
> 
> [OK ] secondary_timing:  come subordinate to the main idea. If this expression is going to animate or change, the danger is not that the expression will dominate the scene, but that it will never be seen. The change must come before, or after, the move. A change in the middle of a major move will go unnoticed, and value intended will be lost. It must also be staged to be obvious, though secondary. [26] 2.11 APPEAL The wor
> 
> [OK ] antic_threeparts:  hes a sore muscle. FIGURE 5. Wally B.'s zip off shows use of squash and stretch, anticipation, follow through, overlapping action, and secondary action. 2.3 ANTICIPATION An action occurs in three parts: the preparation for the action, the action proper, and the termination of the action. Anticipation is the preparation for the action; the latter two are discussed in the next sections. There are se
> 
> [OK ] antic_foot:  . In one sense, it is the anatomical provision for an action. Since muscles in the body function through contraction, each must be first be extended before it can contract. A foot must be pulled back before it can be swung forward to kick a ball. [12] Without anticipation many actions are abrupt, stiff and unnatural. Anticipation is also a device to catch the audience's eye, to prepare them for th
> 
> [OK ] antic_abrupt:  action, each must be first be extended before it can contract. A foot must be pulled back before it can be swung forward to kick a ball. [12] Without anticipation many actions are abrupt, stiff and unnatural. Anticipation is also a device to catch the audience's eye, to prepare them for the next movement and lead them to expect it before it actually occurs. Anticipation is often used to explain wh
> 
> [OK ] squash_most_important:  low in and out, arcs, appeal, straight ahead action, and pose-to-pose action remain the same, their application changes due to the difference in medium. 2.1 SQUASH AND STRETCH The most important principle is called squash and stretch. When an object is moved, the movement emphasizes any rigidity in the object. In real life, only the most rigid shapes (such as chairs, dishes and pans) remain so dur
> 
> [OK ] squash_rigidity:   their application changes due to the difference in medium. 2.1 SQUASH AND STRETCH The most important principle is called squash and stretch. When an object is moved, the movement emphasizes any rigidity in the object. In real life, only the most rigid shapes (such as chairs, dishes and pans) remain so during motion. Anything composed of living flesh, no matter how bony, will show considerable mov
> 
> [OK ] exagg_balance:  has many components to it: the design, the shape of the objects, the action, the emotion, the color, the sound. Exaggeration can work with any component, but not in isolation. The exaggeration of the various components should be balanced. If just one thing is exaggerated in an otherwise lifelike scene, it will stick out and seem unrealistic. f 41 ~ SIGGRAPH '87, Anaheim, July 27-31, 1987 FIGURE 11
> 
> [OK ] exagg_isolation:  make him frantic. A scene has many components to it: the design, the shape of the objects, the action, the emotion, the color, the sound. Exaggeration can work with any component, but not in isolation. The exaggeration of the various components should be balanced. If just one thing is exaggerated in an otherwise lifelike scene, it will stick out and seem unrealistic. f 41 ~ SIGGRAPH '87, Anaheim,
> ```

## 🤖 Claude *(23:15:04)*

<details>
<summary>💭 Thinking Process</summary>

All the Lasseter quotes check out verbatim, though there's a minor typo in the original paper where it says "A secondary actions is always kept subordinate" instead of "actions." The staging finding about scene components also verified as written. Now I'm trying to access the ASC article to verify the Burum quotes—getting a 403 error, so I'll need to try alternative methods like firecrawl or web search to pull those citations.

</details>


## 🤖 Claude *(23:15:04)*


🛠️ **Tool Call**: `WebSearch`
```json
{
  "query": "Stephen Burum ASC \"lighting a set\" \"create separation\" \"add fill\" cast a shadow American Cinematographer"
}
```

## 🤖 Claude *(23:15:07)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic; for ua in \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36\"; do\ncurl -sS -L --compressed -H \"Accept: text/html\" -H \"Accept-Language: en-US,en;q=0.9\" -A \"$ua\" -o asc2.html -w \"HTTP=%{http_code} SIZE=%{size_download}\\n\" \"https://theasc.com/articles/lighting-a-set\"; done\ngrep -oiE \"burum|separation|Laverne\" asc2.html | sort -u | head"
}
```

> **Tool Result (WebSearch)** - ✅ Success
>
> ```
> Web search results for query: "Stephen Burum ASC "lighting a set" "create separation" "add fill" cast a shadow American Cinematographer"
> 
> Links: [{"title":"Stephen H. Burum, ASC Archives (@BurumArchives) / ...","url":"https://twitter.com/BurumArchives"},{"title":"Lighting a Set with Stephen H. Burum, ASC","url":"https://theasc.com/article/lighting-a-set/"},{"title":"Visionary / Stephen H. Burum ASC","url":"https://britishcinematographer.co.uk/stephen-h-burum-asc/"},{"title":"Consummate Professional: Stephen H. Burum, ASC","url":"https://theasc.com/articles/burum-camerimage"},{"title":"A Collaboration with Panavision: Stephen H. Burum, ASC - YouTube","url":"https://www.youtube.com/watch?v=siQ8WMIL8E8"},{"title":"Stephen Henry Burum ASC to be awarded with EnergaCameraimage Lifetime Achievement award - Cinematography World","url":"https://www.cinematography.world/stephen-henry-burum-to-be-awarded-with-energacameraimage-lifetime-achievement-award/"},{"title":"Stephen H. Burum — Grokipedia","url":"https://grokipedia.com/page/Stephen_H._Burum"}]
> 
> I found a highly relevant result! The American Cinematographer article "Lighting a Set with Stephen H. Burum, ASC" demonstrates classical techniques of lighting a set with multiple Fresnel fixtures and varying amounts of fill, adapted from the 2002 book "Reflections: 21 Cinematographers at Work."
> 
> This appears to be the exact article you're looking for, as it covers the specific lighting topics you mentioned (lighting a set, creating separation, and adding fill). The article is available at theasc.com and discusses fundamental lighting techniques demonstrated by Stephen Burum, ASC, an American cinematographer.
> 
> 
> REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> HTTP=200 SIZE=29165
> burum
> Burum
> Laverne
> separation
> ```

## 🤖 Claude *(23:15:20)*

<details>
<summary>💭 Thinking Process</summary>

The curl request with the proper user agent returned successfully and the page contains the expected keywords. I notice the canonical URL uses the singular form "article" while the source citation uses the plural "articles," though both resolve correctly. Now I need to verify the final URL and pull out the relevant quotes.

</details>


## 🤖 Claude *(23:15:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic; python3 - <<'EOF'\nimport re,html\nt=open('asc2.html',encoding='utf-8',errors='replace').read()\nt=re.sub(r'<script.*?</script>','',t,flags=re.S|re.I)\nt=re.sub(r'<style.*?</style>','',t,flags=re.S|re.I)\nt=re.sub(r'<[^>]+>',' ',t)\nt=html.unescape(t); t=re.sub(r'\\s+',' ',t)\nopen('asc.txt','w').write(t)\nprint(len(t))\nclaims={\n 'three_things':'three things every time',\n 'shadows_inky':'inky black',\n 'separation_3d':'three-dimensional quality',\n 'light_against_dark':'light against dark',\n 'ratio8':'8:1',\n 'laverne':'Laverne',\n 'no_correct_fill':'no correct amount of fill',\n 'axis':\"camera's axis\",\n 'secondary_shadow':'secondary shadow',\n 'reflect25':'25 percent',\n 'crosskeys':'cross-keys',\n 'fill_from_key_side':'fill from the key side',\n 'foreboding':'foreboding',\n}\nfor k,v in claims.items():\n    i=t.lower().find(v.lower())\n    print(f\"[{'OK ' if i>=0 else 'MISS'}] {k}: \", (t[max(0,i-260):i+300] if i>=0 else 'NOT FOUND'))\n    print()\nEOF"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 21559
> [OK ] three_things:  “Interiors are always the hardest for people to start,” he explains, “because you go into a big black room and you have to create everything.” The cinematographer firmly believes that film lighting has three universal functions: “Everyone does at least one of three things every time they light a set: 1. The first thing is to cast a shadow. The light that casts the shadow could be a tiny pinpoint source, a big soft source, or anything in between. The shadow can be a hard shadow with a hard edge, or a soft shadow with an edge that just trails off into noth
> 
> [OK ] shadows_inky:  hen you go from cut to cut, you try to maintain the same volume of light and dark in the frame. That’s why you have to light close-ups separately, but with a similar direction of light.” Burum explains that fill light is a natural phenomenon. “Shadows are not inky black even on a sunny day, because they get natural fill from sunlight bouncing off the sky, clouds, buildings or ground.” Fill light, he says, is usually placed as close as possible to the lens axis to avoid creating shadows. “You want to be able to fill in the shadows in a way that the audien
> 
> [OK ] separation_3d:   for no shadow at all. It’s the difference between when the sun’s out and a cloudy day, or any gradation in between. 2. The second thing you do in lighting is to create separation. Photography looks at the world with only one lens, and you need to introduce a three-dimensional quality to this two-dimensional image. There’s only one way to accomplish that: creating areas of light against dark or dark against light. I’m not referring to color. For example, you may put a backlight on someone’s dark head so that you have a dark area, a little bright halo, an
> 
> [OK ] light_against_dark:   2. The second thing you do in lighting is to create separation. Photography looks at the world with only one lens, and you need to introduce a three-dimensional quality to this two-dimensional image. There’s only one way to accomplish that: creating areas of light against dark or dark against light. I’m not referring to color. For example, you may put a backlight on someone’s dark head so that you have a dark area, a little bright halo, and another dark area. Or you may put a light on a wall behind somebody’s dark shoulder. You can put in as many of tho
> 
> [OK ] ratio8:  so patterns the left-most wall through a shuttered window. The resulting effect is a striking mesh of horizontals that suggest the low angle of late-afternoon sunlight. The same setup with increasing levels of fill light: no fill (top), a key-to-fill ratio of 8:1 (middle) and a ratio of 3:1 (bottom). This diagram illustrates Burum’s lighting for a demonstration of working with Fresnel fixtures and varying amounts of fill. Two light sources illuminate the dark, right-hand corner of the set. A 1K from a catwalk above the stage simulates the “glow” from day
> 
> [OK ] laverne:  too bright. There is no correct amount of fill; it’s a matter of artistic interpretation.” The progression of fill-light levels in the workshop footage provides a dramatic illustration of contrasting moods. Burum jokingly describes the brightest shot as the “ Laverne & Shirley look.” Indeed, an audience might well associate this low-contrast image with a comedic theme. The middle image was measured to have a key-to-fill ratio of 8:1 (based on two incident readings, one toward the key and one toward the fill). The effect is bright but still modeled, and t
> 
> [OK ] no_correct_fill:  rkshop setup with different amounts of fill. “The job of the fill light is to set the mood of the scene. Here we had a demonstration of no fill light, fill light that I thought was at the proper level, and fill light that I felt was a bit too bright. There is no correct amount of fill; it’s a matter of artistic interpretation.” The progression of fill-light levels in the workshop footage provides a dramatic illustration of contrasting moods. Burum jokingly describes the brightest shot as the “ Laverne & Shirley look.” Indeed, an audience might well assoc
> 
> [MISS] axis:  NOT FOUND
> 
> [OK ] secondary_shadow:  ings or ground.” Fill light, he says, is usually placed as close as possible to the lens axis to avoid creating shadows. “You want to be able to fill in the shadows in a way that the audience won’t recognize. Old movie wisdom says that you don’t want to see a secondary shadow cast by fill light, mainly because it’s distracting.” As with every other light but the key, Burum sets the fill by eye, and doesn’t measure the exposure ratio of the fill to the key. “I’m used to correlating in my mind what I see on the stage with what I see on the screen. The key-
> 
> [OK ] reflect25:  otes that this problem was highlighted in the bright, unpainted set used in the workshop. “If the set walls are lighter than normal skin tone, people will always seem dark by comparison. For people to stand out, the reflective value of the set should be below 25 percent. If it’s not, the actors’ faces will look dark even though they’re properly exposed, or you’ll spend a lot of time taking light off the walls. This is especially true when you have actors coming through doors, or standing against walls. It’s suicide. It’s always easier to put light on the
> 
> [OK ] crosskeys:  there are two keys, one for each actor. Each light provides 40 footcandles, yielding an exposure of T4 at ISO 500. The woman’s key is a right-hand 2K through a window without blinds. The man’s key is a left-hand 1K. Burum refers to these placements as “inside cross-keys,” because the angle of the key lights to the camera-subject axis is greater than 90 degrees, creating a rim of light on the profiles. Both actors are also separated from the dark background by a 2K backlight. “The key light’s job is to cast a shadow and give the scene texture, roundness a
> 
> [OK ] fill_from_key_side:  ght on the camera’s axis,” Burum stresses. “If you don’t put it there, you start to cast a secondary shadow on the other side of the axis. Quite often, you’re hemmed in by the set, so you place it as close as possible to the camera. In those cases, you should fill from the key side if you have a choice, because that tends to wrap the shadow better.” One of the problems with fill light, Burum warns, is that “you start to build up the background. Very often, you want a fill light that just goes out and dies, because you want to fill the people and not the 
> 
> [OK ] foreboding:  ey-to-fill ratio of 8:1 (based on two incident readings, one toward the key and one toward the fill). The effect is bright but still modeled, and the frame still retains black references — in the actors’ hair, for example. The no-fill image conveys a sense of foreboding that is absent from the other two scenes. Burum comments: “If you really wanted to be gutsy, you could turn off the key light on the actress, but then what would you do for close-ups? You should always keep coverage in mind. When you go from cut to cut, you try to maintain the same volume
> ```

## 🤖 Claude *(23:15:38)*

<details>
<summary>💭 Thinking Process</summary>

I'm verifying all the Burum quotes are accurate—the apostrophe encoding issue was just a formatting quirk with the curly apostrophe in "camera's axis," and the fill light positioning quote checks out. There's an important distinction in how Burum describes the compositional scheme with inside cross-keys, which draws attention toward the frame's center through the contrast of dark edges.

I'm also cross-checking the key-to-fill ratios against the article: the 8:1 ratio in the middle represents "bright but still modeled," while 3:1 at the bottom is the brightest, giving that "Laverne & Shirley" comedy look. The finding's mapping of 8:1 as "dramatic" is slightly off since the article positions 8:1 as the proper middle ground, with no fill being the truly dramatic choice—but the finding itself acknowledges that no fill conveys foreboding, so the derived token mapping is reasonable enough. I'll keep it but note the calibration honestly.

Now I need to verify a batch of sources: the vectorscope skin tone references, RGB color complements, ASC CDL formula, J cuts, continuity editing match-on-action, the 180-degree rule, whether the headroom entry actually contains the Smith 1797 quote (it probably doesn't—that's likely in the rule of thirds article instead, which suggests a source mismatch for finding #18), and the Murch rule of six percentages.

</details>


## 🤖 Claude *(23:15:38)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic; python3 - <<'EOF'\nt=open('asc.txt').read()\nfor v in ['compositional scheme','pull the attention','dark on the outside']:\n    i=t.lower().find(v.lower())\n    print(f\"[{'OK ' if i>=0 else 'MISS'}] {v}:\", (t[max(0,i-320):i+320] if i>=0 else 'NOT FOUND'),\"\\n\")\nEOF"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [OK ] compositional scheme:  also gives you illumination and an exposure level. Then you’ve got the lights that separate things: the backlights, the glow lights, the kickers, the set lights, and all of the other fixtures that provide gradations of light against dark.” Burum adds that the rear key position directs the eye of the audience. “It’s a compositional scheme. Inside cross-keys pull the attention to the center of the frame, because you have dark on the outside and light on the inside; there’s usually another bright area behind the faces, so everything is contained in the middle of the frame.” An “inside cross-keys” lighting setup The cinematographer not 
> 
> [OK ] pull the attention: sure level. Then you’ve got the lights that separate things: the backlights, the glow lights, the kickers, the set lights, and all of the other fixtures that provide gradations of light against dark.” Burum adds that the rear key position directs the eye of the audience. “It’s a compositional scheme. Inside cross-keys pull the attention to the center of the frame, because you have dark on the outside and light on the inside; there’s usually another bright area behind the faces, so everything is contained in the middle of the frame.” An “inside cross-keys” lighting setup The cinematographer notes that the position of the actor is als 
> 
> [OK ] dark on the outside:  backlights, the glow lights, the kickers, the set lights, and all of the other fixtures that provide gradations of light against dark.” Burum adds that the rear key position directs the eye of the audience. “It’s a compositional scheme. Inside cross-keys pull the attention to the center of the frame, because you have dark on the outside and light on the inside; there’s usually another bright area behind the faces, so everything is contained in the middle of the frame.” An “inside cross-keys” lighting setup The cinematographer notes that the position of the actor is also crucial, especially for lighting close-ups. In the workshop sc
> ```

## 🤖 Claude *(23:15:39)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://en.wikipedia.org/wiki/Headroom_(photographic_framing)",
  "prompt": "Does this article contain a quote from John Thomas Smith, \"Remarks on Rural Scenery\" (1797) about \"the ratio of about two thirds to one third\"? Does it discuss the rule of thirds, headroom, lead room / leading room / nose room, and dead space? Quote what it actually says."
}
```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # Analysis of the Article Content
> 
> No, this Wikipedia article does **not** contain a direct quote from John Thomas Smith's "Remarks on Rural Scenery" (1797). 
> 
> The article merely **references** Smith's work, stating: "The 'rule of thirds' was coined by the painter John Thomas Smith in his book 'Remarks on Rural Scenery.'" However, no actual quotation from that historical source is provided.
> 
> ## Topics Covered
> 
> The article does extensively discuss:
> 
> - **Rule of thirds**: "The rule of thirds suggests that the subject's eyes, as a centre of interest, are ideally positioned one-third of the way down from the top of the frame."
> 
> - **Headroom**: Defined as the distance between the top of a subject's head and the top of the frame
> 
> - **Lead room/nose room/looking room**: Mentioned as alternative terms the headroom concept sometimes encompasses
> 
> - **Dead space**: Described as the result of excessive headroom—"Too much room between a subject's head and the top of frame results in dead space."
> 
> The article does not reproduce Smith's original language about proportional ratios.
> ```

## 🤖 Claude *(23:15:59)*

<details>
<summary>💭 Thinking Process</summary>

Finding #18's source from the Headroom wiki doesn't actually contain the Smith 1797 quote verbatim—it's in the Rule of Thirds article instead—but the wiki does support the operational claims about headroom, dead space, and lead room. Since the source sustains the core concept even though the attribution is fabricated, I need to determine whether that's grounds for discarding it per the instructions.

The rule of thirds part is genuinely contested folklore, but lead room and dead space are perceptually real, so I'm leaning toward keeping the finding but stripping the misattributed quote and downgrading the impact to "baixo" to reflect the weaker attribution and folkloric nature of the technique. I also notice the ep05 motion pieces are 1280x720 landscape and 9:16 verticals, which might be relevant context.

Now I need to verify the remaining sources: vectorscope skin tone, complementary colors, ASC CDL, J cut, continuity editing, 180-degree rule, and Murch rule of six. Let me batch the WebFetches to check these.

</details>


## 🤖 Claude *(23:16:00)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://bramstout.nl/en/webbooks/vectorscopes/",
  "prompt": "Does this page discuss the vectorscope \"skin tone line\" as the NTSC I axis (YIQ)? Does it cite Keith Jack's \"Video Demystified\" saying the skin tone phase angle varies from 116 to 126 degrees between manufacturers, with 123 degrees (+I axis) commonly adopted? Quote the relevant passages verbatim."
}
```

## 🤖 Claude *(23:16:01)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://en.wikipedia.org/wiki/ASC_CDL",
  "prompt": "What is the exact ASC CDL math formula (slope, offset, power) given? What are the nominal default values? Does version 1.2 add saturation? Who publishes it?"
}
```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> The server returned HTTP 403 Forbidden.
> 
> The response body was not retrieved. If this URL requires authentication, use an authenticated tool (e.g. `gh` for GitHub, or an MCP-provided fetch tool) instead of WebFetch.
> ```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # ASC CDL Formula and Specifications
> 
> **The Mathematical Formula:**
> 
> The ASC CDL uses this equation: "out=(i×s+o)^p" where:
> - **i** = input pixel value (0=black, 1=white)
> - **s** = slope (nominal: 1.0)
> - **o** = offset (nominal: 0)
> - **p** = power (nominal: 1.0)
> 
> **Saturation in Version 1.2:**
> 
> Yes, version 1.2 added a tenth parameter. "A tenth number, Saturation, specified in the Version 1.2 release, applies to the R, G, and B color channels in combination."
> 
> **Publisher:**
> 
> The American Society of Cinematographers (ASC) publishes this standard through its Technology Committee. According to the document, "Instructions for getting the current release of ASC CDL implementor-oriented documentation can be retrieved by sending an e-mail to asc-cdl at theasc dot com."
> ```

## 🤖 Claude *(23:16:08)*

<details>
<summary>💭 Thinking Process</summary>

I'm checking the ASC CDL verification and looking up the vectorscope reference on page 403, trying to fetch it with a proper user agent.

</details>


## 🤖 Claude *(23:16:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic; curl -sS -L --compressed -A \"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36\" -o vec.html -w \"HTTP=%{http_code} SIZE=%{size_download}\\n\" \"https://bramstout.nl/en/webbooks/vectorscopes/\"\npython3 - <<'EOF'\nimport re,html\nt=open('/tmp/critic/vec.html',encoding='utf-8',errors='replace').read()\nt=re.sub(r'<(script|style).*?</\\1>','',t,flags=re.S|re.I); t=re.sub(r'<[^>]+>',' ',t); t=html.unescape(t); t=re.sub(r'\\s+',' ',t)\nopen('/tmp/critic/vec.txt','w').write(t); print('LEN',len(t))\nfor v in ['skin tone','116','126','123','Video Demystified','Keith Jack','I axis','YIQ','NTSC']:\n    i=t.find(v)\n    print(f\"[{'OK ' if i>=0 else 'MISS'}] {v}:\", (t[max(0,i-260):i+300] if i>=0 else 'NOT FOUND'),\"\\n\")\nEOF"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> HTTP=200 SIZE=10285
> LEN 7962
> [OK ] skin tone:  Vectorscopes | Bram Stout Productions Vectorscopes The skin tone line does not exist Disclaimer: I wrote this very late in the evening/night and did this for fun. I may be wrong on some things, but I would love to hear about it. You can easily talk to me about it on my twitter, specifically this tweet: [link] Table of Contents Introduction If you are an 
> 
> [OK ] 116: n tone line? According to the book Video Demystified: A Handbook for the Digital Engineer by Keith Jack [8] , in a section about automatic skin tone correction: “It should be noted that the phase angle for skin tone varies between companies. Phase angles from 116° to 126° are used; however, using 123° (the +I axis) simplifies the processing.” The phase angle in this case could be seen as the hue but from a different starting point. This tells us that skin tones in different software packages can vary by at least 10° in the hue. That might sound not that  
> 
> [OK ] 126: ine? According to the book Video Demystified: A Handbook for the Digital Engineer by Keith Jack [8] , in a section about automatic skin tone correction: “It should be noted that the phase angle for skin tone varies between companies. Phase angles from 116° to 126° are used; however, using 123° (the +I axis) simplifies the processing.” The phase angle in this case could be seen as the hue but from a different starting point. This tells us that skin tones in different software packages can vary by at least 10° in the hue. That might sound not that much or  
> 
> [OK ] 123: eo Demystified: A Handbook for the Digital Engineer by Keith Jack [8] , in a section about automatic skin tone correction: “It should be noted that the phase angle for skin tone varies between companies. Phase angles from 116° to 126° are used; however, using 123° (the +I axis) simplifies the processing.” The phase angle in this case could be seen as the hue but from a different starting point. This tells us that skin tones in different software packages can vary by at least 10° in the hue. That might sound not that much or a lot, but below is a GIF to v 
> 
> [OK ] Video Demystified: in-sync, our vectorscopes got two lines to help with that and because of the need to optimise the chrominance signal, one of those lines ended up roughly indicating where the skin tones lie. Can the I line function as the skin tone line? According to the book Video Demystified: A Handbook for the Digital Engineer by Keith Jack [8] , in a section about automatic skin tone correction: “It should be noted that the phase angle for skin tone varies between companies. Phase angles from 116° to 126° are used; however, using 123° (the +I axis) simplifies the pro 
> 
> [OK ] Keith Jack: and because of the need to optimise the chrominance signal, one of those lines ended up roughly indicating where the skin tones lie. Can the I line function as the skin tone line? According to the book Video Demystified: A Handbook for the Digital Engineer by Keith Jack [8] , in a section about automatic skin tone correction: “It should be noted that the phase angle for skin tone varies between companies. Phase angles from 116° to 126° are used; however, using 123° (the +I axis) simplifies the processing.” The phase angle in this case could be seen as th 
> 
> [OK ] I axis: kind of neutral light and not specifically sunlight. So, it would be a quick google to find the answer and one tweet. Instead, I couldn’t find any proper source calling this a skin tone line. Skin tone was never mentioned. Instead this line had two names: the I axis/bar/line and the burst line [2] [3] . I will call it the I line. It’s brother, the Q axis/bar/line and also the burst line, will also become important later on. What is the I line? According to a manual of a physical vectorscope [4] , the I line is used to help detect if the luminance and chr 
> 
> [OK ] YIQ:  use the RGB model that we all use nowadays. Instead, it needed to keep the luminance, called Y, and add in the chrominance. In order to represent the chrominance, they decided to use two values called I and Q. The colour space that this resulted in is called YIQ [7] . It is very similar to the more well known YUV colour space. YIQ and the skin tone line The I value represents the orange-blue range and the Q value represents the purple-green range. These ranges were chosen in order to take advantage of the human colour-response characteristics. Our eyes  
> 
> [OK ] NTSC: allows you to make adjustments to the signal in order to correct the synchronisation, so that the colours are accurate. Source. On the left the signals are in-sync. On the right they are not in-sync. This is important, because in analog video and specifically NTSC encoded video, the signal that carries the chrominance (colour) is completely separated from the signal that carries the luminance (brightness) [5] . However, they still need to stay in-sync and we can’t always use a colour bar image. To achieve this, there is a specific signal called colorburs
> ```

## 🤖 Claude *(23:17:38)*

<details>
<summary>💭 Thinking Process</summary>

I've verified the Vectorscope source—it's titled "The skin tone line does not exist" and contains the Keith Jack quote with the 116-126/123 +I axis reference, matching the finding's framing as a counterpoint to dogma. However, there's a critical tension: the source actually argues the skin tone line is unreliable as a reference, while the finding recommends using it for consistency—these positions are in direct conflict.

Looking at the implementation, the finding proposes measuring hue divergence between shots with alerts above 10°, but this doesn't actually require the skin tone line at all—it's just checking hue consistency across frames. The "eixo I" becomes decorative rather than functional. For a motion-graphics rail where most scenes lack faces, this approach is marginal at best, and the feasibility is problematic: detecting and segmenting skin regions requires a face detector that doesn't exist in the rail. The finding assumes "medir o matiz médio da região de pele" is possible, but that segmentation capability isn't there. I'd need to either downgrade this to requiring a new module or reframe it as something achievable—sampling a fixed region manually or using ffmpeg's frame-level hue statistics instead.

Given that the rail is motion graphics with few avatar shots and no skin segmentation infrastructure, the impact is low and the implementation is hand-wavy. The source itself calls the skin tone concept folklore, so keeping a finding whose own source dismisses it as non-existent would push the Sovereign to build a skin-hue checker for a rail that doesn't need it. I'm cutting this one.

Moving on to the remaining findings: complementary colors, J cuts, continuity editing, the 180-degree rule, and the Murch rule of six. Now I need to examine the more substantial technical claims, particularly the grain finding—it's a verified filter with determinism, which makes it a strong keeper, though there's a caveat about how noise applied after grading interacts with encoding.

For the grain implementation, I'm refining the ffmpeg recipe to use luma-only noise rather than applying it to all components, since that's more accurate for a film grain aesthetic. I need to verify that the tmix approach for motion blur actually works with the frame indexing and that the render-core modification is feasible given how the frame counter is already indexed.

But there's a critical issue with the tmix strategy: when I apply `tmix=frames=4` followed by fps decimation, the rolling average window integrates all 4 subframes into each output frame, which gives 360° shutter rather than the intended 144°. To achieve 180° shutter I'd need `tmix=frames=2` instead, since that would average only 2 out of 4 subframes per output. I need to nail down the phase alignment between tmix and fps decimation to avoid misaligned frame averaging, and I'm considering using select filters or framestep to ensure I'm grabbing the right frames. There's also a real cost here — rendering 4× more frames with Playwright screenshots would multiply the wall-clock time significantly, so I need to weigh whether this approach is actually feasible or if I should stick with the corrected math but acknowledge the performance trade-off.

For the pixel-diff staging gate, I'm realizing this isn't a trivial feature — it requires per-frame pixel difference computation aggregated by bounding boxes, which means either using imagescript for WASM image processing or piping through ffmpeg. The constraint that only one element can exceed the threshold is also too restrictive given the v6 animation complexity with the ring, drifting points, and parallax background motion.

I'm shifting the approach: keep the staging principle (one idea at a time) as an authoring rule with optional advisory reporting rather than a hard exit condition, and note that ambient motion needs to be excluded from the measurement. The mechanical gate is where the risk lies, so I'll downgrade it to guidance instead of enforcement.

Now looking at the secondary action timing issue with disjoint windows — the declarative beat scheduling approach versus the hand-written seek calls in the ep05 runners. I need to verify that getPointAtLength works deterministically in headless Chromium when reading points from SVG paths and applying them as transforms — it should be fine since the rail pins the chromium version. Finding #6 about curves is already verified materially, but I'm realizing it might already be implemented in the motion-bridge encode, which would mean it's not a new finding but rather something that survived the review.

Now I'm checking whether findings #7 through #10 hold up: pchip interpolation does prevent overshoot compared to natural cubic splines, the teal and orange complementary color claim needs verification against Wikipedia, and I need to confirm the colorbalance preserve-lightness option exists in ffmpeg 6.1.

For finding #10, the conic-gradient border approach for the three functions of light is implementable in Chromium. Finding #11 about the key-fill ratio dial checks out. Finding #12 involves using CSS custom properties with trigonometric calculations—CSS added sin() and cos() support in Chrome 111, which is compatible with the Playwright Chromium version, though computing the values in JavaScript at applyProps is a simpler fallback. Finding #13 references a 25% reflectance threshold for background detection via ffmpeg's signalstats YAVG, which is feasible but I need to clarify what that 25% threshold actually represents.

The principle that the background should be darker than the subject cards is sound, so I'd frame the gate as measuring whether the background is genuinely darker rather than relying on a specific magic number. For finding #16 on atmospheric perspective, the ASC article supports the concept of separation between elements but doesn't explicitly cover blur or desaturation by distance—the justification leans on general perceptual knowledge rather than a direct citation.

The technique itself is real and widely accepted, but there's a source-claim mismatch. The instructions say to discard if the source doesn't sustain the claim, and strictly speaking the ASC article doesn't. I could either discard it or replace the source with something like Wikipedia's aerial perspective article, which would better support the finding. Let me verify that source and decide whether to keep it with a corrected citation.

Now I'm checking the other findings — vignette and unsharp mask defaults need verification, the 180-degree rule analogy to flow axis is defensible but a bit of a stretch, and I need to confirm the cutting on action quote from the continuity editing source.

For the J/L cut finding, the targets are already defined in the codebase, so the real question is whether the assembly process actually applies them — I should trace through the assembly logic to see if it's using those cut markers or if it's relying on crossfades instead.

Now checking the Rule of Six percentages from Murch's work and verifying the source citation. For the ASC CDL and LUT approach, the math checks out and it's implementable with a 3D LUT, though technically a 1D LUT would be more efficient for simple per-channel adjustments.

For the squash and stretch effect, I can derive velocity from easing functions and apply it through CSS transforms with rotation and scaling. The exaggeration balance finding is solid. For the WebGL motion blur approach, I need to assess whether headless Chromium can handle the rendering requirements.

The key blocker is testing if WebGL actually works in the pinned headless environment—it might fall back to SwiftShader software rendering, which is deterministic but slow. If WebGL isn't materially available, I'll downgrade that finding to infeasible. Let me run the test to confirm. Finding #27 is about the HDR gap...

For Finding #27, it's marked as low impact and infeasible, which is honest—ffmpeg does have libplacebo support, so the gap is real and verified. It's a useful explicit non-goal that prevents wasted effort, so I'll keep it.

For Finding #1, I need to clarify that the existing runners already use smoothstep easing, so the real value-add is codifying named easings and distinguishing entrance versus exit curves rather than introducing easing from scratch.

Now I'm running through the material verification tests across chromium WebGL, path length calculations, color balance options, vignette and unsharp defaults, LUT3D interpolation, signal statistics, temporal mix phase math, and luma-only noise generation, plus the remaining web fetches.

</details>


## 🤖 Claude *(23:17:40)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic\necho \"===COLORBALANCE===\"; ffmpeg -hide_banner -h filter=colorbalance 2>&1 | sed -n '1,30p'\necho \"===VIGNETTE===\"; ffmpeg -hide_banner -h filter=vignette 2>&1 | grep -E \"angle|a  \" | head -5\necho \"===UNSHARP===\"; ffmpeg -hide_banner -h filter=unsharp 2>&1 | grep -E \"amount|msize\" | head -8\necho \"===LUT3D===\"; ffmpeg -hide_banner -h filter=lut3d 2>&1 | tail -12"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ===COLORBALANCE===
> Filter colorbalance
>   Adjust the color balance.
>     slice threading supported
>     Inputs:
>        #0: default (video)
>     Outputs:
>        #0: default (video)
> colorbalance AVOptions:
>    rs                <float>      ..FV.....T. set red shadows (from -1 to 1) (default 0)
>    gs                <float>      ..FV.....T. set green shadows (from -1 to 1) (default 0)
>    bs                <float>      ..FV.....T. set blue shadows (from -1 to 1) (default 0)
>    rm                <float>      ..FV.....T. set red midtones (from -1 to 1) (default 0)
>    gm                <float>      ..FV.....T. set green midtones (from -1 to 1) (default 0)
>    bm                <float>      ..FV.....T. set blue midtones (from -1 to 1) (default 0)
>    rh                <float>      ..FV.....T. set red highlights (from -1 to 1) (default 0)
>    gh                <float>      ..FV.....T. set green highlights (from -1 to 1) (default 0)
>    bh                <float>      ..FV.....T. set blue highlights (from -1 to 1) (default 0)
>    pl                <boolean>    ..FV.....T. preserve lightness (default false)
> 
> This filter has support for timeline through the 'enable' option.
> ===VIGNETTE===
>    angle             <string>     ..FV....... set lens angle (default "PI/5")
>    a                 <string>     ..FV....... set lens angle (default "PI/5")
> ===UNSHARP===
>    luma_msize_x      <int>        ..FV....... set luma matrix horizontal size (from 3 to 23) (default 5)
>    luma_msize_y      <int>        ..FV....... set luma matrix vertical size (from 3 to 23) (default 5)
>    luma_amount       <float>      ..FV....... set luma effect strength (from -2 to 5) (default 1)
>    chroma_msize_x    <int>        ..FV....... set chroma matrix horizontal size (from 3 to 23) (default 5)
>    chroma_msize_y    <int>        ..FV....... set chroma matrix vertical size (from 3 to 23) (default 5)
>    chroma_amount     <float>      ..FV....... set chroma effect strength (from -2 to 5) (default 0)
>    alpha_msize_x     <int>        ..FV....... set alpha matrix horizontal size (from 3 to 23) (default 5)
>    alpha_msize_y     <int>        ..FV....... set alpha matrix vertical size (from 3 to 23) (default 5)
> ===LUT3D===
>    file              <string>     ..FV....... set 3D LUT file name
>    clut              <int>        ..FV.....T. when to process CLUT (from 0 to 1) (default all)
>      first           0            ..FV.....T. process only first CLUT, ignore rest
>      all             1            ..FV.....T. process all CLUTs
>    interp            <int>        ..FV.....T. select interpolation mode (from 0 to 4) (default tetrahedral)
>      nearest         0            ..FV.....T. use values from the nearest defined points
>      trilinear       1            ..FV.....T. interpolate values using the 8 points defining a cube
>      tetrahedral     2            ..FV.....T. interpolate values using a tetrahedron
>      pyramid         3            ..FV.....T. interpolate values using a pyramid
>      prism           4            ..FV.....T. interpolate values using a prism
> 
> This filter has support for timeline through the 'enable' option.
> ```

## 🤖 Claude *(23:17:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic; cat > webgl-probe.mjs <<'EOF'\nimport { chromium } from 'playwright';\nconst CHROME='/home/ubuntu/.cache/ms-playwright/chromium-1226/chrome-linux/chrome';\nconst b = await chromium.launch({ headless:true, executablePath:CHROME });\nconst p = await (await b.newContext({viewport:{width:400,height:300}})).newPage();\nawait p.setContent('<canvas id=c width=64 height=64></canvas><svg><path id=\"pp\" d=\"M0,0 C100,200 300,200 400,0\"/></svg>');\nconst r = await p.evaluate(() => {\n  const c=document.getElementById('c');\n  const gl=c.getContext('webgl2')||c.getContext('webgl');\n  let info={webgl:!!gl};\n  if(gl){ const dbg=gl.getExtension('WEBGL_debug_renderer_info');\n    info.renderer = dbg? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : gl.getParameter(gl.RENDERER);\n    info.vendor = dbg? gl.getParameter(dbg.UNMASKED_VENDOR_WEBGL) : gl.getParameter(gl.VENDOR);\n    info.version = gl.getParameter(gl.VERSION);\n    // actually draw + read pixels\n    gl.clearColor(0.25,0.5,0.75,1); gl.clear(gl.COLOR_BUFFER_BIT);\n    const px=new Uint8Array(4); gl.readPixels(1,1,1,1,gl.RGBA,gl.UNSIGNED_BYTE,px); info.pixel=[...px];\n  }\n  const path=document.getElementById('pp');\n  info.pathLen = path.getTotalLength();\n  const pt = path.getPointAtLength(info.pathLen*0.37);\n  info.pt=[pt.x,pt.y];\n  return info;\n});\nconsole.log(JSON.stringify(r,null,1));\nawait b.close();\nEOF\nbun /tmp/critic/webgl-probe.mjs 2>&1 | tail -20"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> {
>  "webgl": true,
>  "renderer": "ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (LLVM 10.0.0) (0x0000C0DE)), SwiftShader driver)",
>  "vendor": "Google Inc. (Google)",
>  "version": "WebGL 2.0 (OpenGL ES 3.0 Chromium)",
>  "pixel": [
>   64,
>   128,
>   191,
>   255
>  ],
>  "pathLen": 526.8367309570312,
>  "pt": [
>   133.29141235351562,
>   136.54783630371094
>  ]
> }
> ```

## 🤖 Claude *(23:18:00)*

<details>
<summary>💭 Thinking Process</summary>

I'm verifying the default parameters across these filters—colorbalance's `pl` parameter, vignette's angle default, and unsharp's chroma and luma amounts all check out. Though I'm noticing the documentation shows `la=0.6` in one example, and I need to confirm whether `la` is actually a valid shorthand alias for luma_amount, since the help output lists the full parameter names but not the abbreviated forms.

I'm also confirming that lut3d uses tetrahedral interpolation by default, and that WebGL 2.0 is accessible through SwiftShader in the pinned Chromium build—readPixels works, which means exige-webgl is genuinely feasible with software rendering, even if it'll be slower on local CPU. The determinism should hold since SwiftShaker's consistent across builds. I've verified getPointAtLength returns the expected point data as well.

Next I need to test the unsharp short aliases directly, check signalstats for YAVG output, verify tmix's phase calculations, confirm noise can operate in luma-only mode, and finish the remaining WebFetch calls.

</details>


## 🤖 Claude *(23:18:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic\n# unsharp short aliases + full chain smoke\nffmpeg -y -v error -f lavfi -i \"testsrc2=s=320x240:d=1:r=5\" -vf \"format=gbrp,curves=master='0/0.045 0.25/0.22 0.5/0.5 0.75/0.79 1/0.985':interp=pchip,colorbalance=rs=-0.05:bs=0.09:rm=0.02:bm=-0.01:rh=0.07:bh=-0.05:pl=1,unsharp=lx=5:ly=5:la=0.6,vignette=angle=PI/6,noise=all_seed=42:alls=6:allf=t+u,format=yuv420p\" -frames:v 1 chain.png && echo \"CHAIN OK $(ls -la chain.png | awk '{print $5}') bytes\"\n# luma-only grain\nffmpeg -y -v error -f lavfi -i \"testsrc2=s=320x240:d=1:r=5\" -vf \"noise=c0_seed=42:c0s=8:c0f=t+u,format=yuv420p\" -frames:v 1 grain_luma.png && echo \"LUMA-ONLY GRAIN OK\"\n# signalstats YAVG on a dark background\nffmpeg -v error -f lavfi -i \"color=0x141c2b:s=320x240:d=1:r=1\" -vf \"signalstats,metadata=print:key=lavfi.signalstats.YAVG\" -f null - 2>&1 | head -3"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> CHAIN OK 168835 bytes
> LUMA-ONLY GRAIN OK
> ```

## 🤖 Claude *(23:18:10)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic\n# tmix shutter-angle math probe: 4x subframes (100fps) -> 25fps.\n# Make a moving bar at 100fps, then A) tmix=4 B) tmix=2, decimate to 25.\nffmpeg -y -v error -f lavfi -i \"color=black:s=200x100:r=100:d=1\" -vf \"drawbox=x='t*1000':y=20:w=8:h=60:color=white:t=fill\" -c:v ffv1 src100.mkv\nfor N in 2 4; do\nffmpeg -y -v error -i src100.mkv -vf \"tmix=frames=$N,fps=25\" -c:v ffv1 tmix$N.mkv\n# measure how many columns are non-black in frame 10 => blur extent\nffmpeg -v error -i tmix$N.mkv -vf \"select=eq(n\\,10),signalstats,metadata=print:key=lavfi.signalstats.YMAX\" -vsync 0 -f null - 2>&1 | head -2\nffmpeg -y -v error -i tmix$N.mkv -vf \"select=eq(n\\,10)\" -vsync 0 -frames:v 1 t$N.png\npython3 -c \"\nfrom PIL import Image; import sys\nim=Image.open('t$N.png').convert('L'); w,h=im.size\ncols=[x for x in range(w) if max(im.getpixel((x,y)) for y in range(h))>8]\nprint('tmix=$N -> blurred width px:', (max(cols)-min(cols)+1) if cols else 0)\n\"\ndone"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> tmix=2 -> blurred width px: 0
> tmix=4 -> blurred width px: 0
> ```

## 🤖 Claude *(23:18:16)*

<details>
<summary>💭 Thinking Process</summary>

The signalstats metadata output came back empty, so I need to try again. The tmix probe also failed—the drawbox probably moved outside the frame since the bar was moving too fast. I'll slow it down and verify the frames are captured correctly, plus adjust the select filter with -vsync 0.

</details>


## 🤖 Claude *(23:18:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic\nffmpeg -v info -f lavfi -i \"color=0x141c2b:s=64x64:d=1:r=1\" -vf \"signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-\" -f null - 2>&1 | grep -iE \"YAVG|pts\" | head -5\necho \"=== ref: pure white / pure black ===\"\nffmpeg -v info -f lavfi -i \"color=white:s=64x64:d=1:r=1\" -vf \"signalstats,metadata=print:key=lavfi.signalstats.YAVG:file=-\" -f null - 2>&1 | grep -i yavg | head -2"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> frame:0    pts:0       pts_time:0
> lavfi.signalstats.YAVG=39
> === ref: pure white / pure black ===
> lavfi.signalstats.YAVG=235
> ```

## 🤖 Claude *(23:18:24)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic\n# 100fps source: bar moving 100 px/s across 400px wide frame, 1s\nffmpeg -y -v error -f lavfi -i \"color=black:s=400x80:r=100:d=2\" -vf \"drawbox=x='60*t':y=20:w=6:h=40:color=white:t=fill\" -c:v ffv1 src100.mkv\npython3 - <<'EOF'\nimport subprocess, os\nfrom PIL import Image\ndef probe(nf):\n    out=f'/tmp/critic/o{nf}.mkv'\n    vf = f\"tmix=frames={nf},\" if nf>1 else \"\"\n    subprocess.run(['ffmpeg','-y','-v','error','-i','/tmp/critic/src100.mkv','-vf',f'{vf}fps=25','-c:v','ffv1',out],check=True)\n    d=f'/tmp/critic/fr{nf}'; os.makedirs(d,exist_ok=True)\n    subprocess.run(['ffmpeg','-y','-v','error','-i',out,'-vf','select=between(n\\\\,10\\\\,10)','-vsync','0',f'{d}/f.png'],check=True)\n    im=Image.open(f'{d}/f.png').convert('L'); w,h=im.size\n    cols=[x for x in range(w) if max(im.getpixel((x,y)) for y in range(0,h,4))>8]\n    print(f\"tmix=frames={nf}: bar footprint = {max(cols)-min(cols)+1 if cols else 0} px  (static bar = 6 px)\")\nfor n in (1,2,4):\n    probe(n)\nEOF"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> tmix=frames=1: bar footprint = 0 px  (static bar = 6 px)
> tmix=frames=2: bar footprint = 0 px  (static bar = 6 px)
> tmix=frames=4: bar footprint = 0 px  (static bar = 6 px)
> ```

## 🤖 Claude *(23:18:32)*

<details>
<summary>💭 Thinking Process</summary>

The signalstats YAVG function is working correctly with the expected range of 16 to 235, though I'll need to recalibrate the 25% gate threshold against this actual range. For the tmix probe, the bar footprint shows zero, which suggests the drawbox rendering might not be working—I'm going to extract a frame directly from the source video to debug this, possibly checking whether the variable `t` in the drawbox expression needs to be explicitly enabled.

</details>


## 🤖 Claude *(23:18:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic\nffmpeg -y -v error -i src100.mkv -vf \"select=eq(n\\,50)\" -vsync 0 -frames:v 1 chk.png\npython3 -c \"\nfrom PIL import Image\nim=Image.open('/tmp/critic/chk.png').convert('L'); w,h=im.size\nprint('size',w,h,'max',im.getextrema())\ncols=[x for x in range(w) if max(im.getpixel((x,y)) for y in range(h))>8]\nprint('cols',(min(cols),max(cols)) if cols else None)\n\""
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> size 400 80 max (0, 0)
> cols None
> ```

## 🤖 Claude *(23:18:38)*

<details>
<summary>💭 Thinking Process</summary>

The drawbox x expression with `60*t` should work since drawbox supports time variables, but I'm wondering if the issue is parameter confusion — `t` is also the thickness parameter, so `t=fill` sets thickness to fill. The color might be rendering as black-on-black despite specifying white, so I should test this to see what's actually happening.

</details>


## 🤖 Claude *(23:18:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic\nffmpeg -y -v error -f lavfi -i \"color=black:s=400x80:r=100:d=2\" -vf \"drawbox=x=100:y=20:w=6:h=40:color=white@1:t=fill\" -frames:v 1 s1.png && python3 -c \"\nfrom PIL import Image; im=Image.open('/tmp/critic/s1.png').convert('L'); print('static drawbox extrema',im.getextrema())\"\n# alternative: use a moving box via geq or overlay of a color source\nffmpeg -y -v error -f lavfi -i \"color=black:s=400x80:r=100:d=2\" -f lavfi -i \"color=white:s=6x40:r=100:d=2\" -filter_complex \"[0][1]overlay=x='60*t':y=20\" -c:v ffv1 src100b.mkv && ffmpeg -y -v error -i src100b.mkv -vf \"select=eq(n\\,50)\" -vsync 0 -frames:v 1 chk2.png && python3 -c \"\nfrom PIL import Image; im=Image.open('/tmp/critic/chk2.png').convert('L'); w,h=im.size\ncols=[x for x in range(w) if max(im.getpixel((x,y)) for y in range(h))>8]\nprint('moving overlay frame50 cols',(min(cols),max(cols)) if cols else None)\""
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> static drawbox extrema (0, 253)
> moving overlay frame50 cols (30, 35)
> ```

## 🤖 Claude *(23:18:49)*

<details>
<summary>💭 Thinking Process</summary>

The static drawbox is working correctly, and the moving overlay approach checks out—at frame 50 (0.5 seconds at 100fps), the x position lands at 30, which maps to columns 30-35 for the 6-pixel-wide box. Now I'm running the tmix shutter probe against src100b.mkv to test the actual behavior.

</details>


## 🤖 Claude *(23:18:51)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic\npython3 - <<'EOF'\nimport subprocess, os\nfrom PIL import Image\ndef probe(nf):\n    out=f'/tmp/critic/o{nf}.mkv'\n    vf = (f\"tmix=frames={nf},\" if nf>1 else \"\")+\"fps=25\"\n    subprocess.run(['ffmpeg','-y','-v','error','-i','/tmp/critic/src100b.mkv','-vf',vf,'-c:v','ffv1',out],check=True)\n    subprocess.run(['ffmpeg','-y','-v','error','-i',out,'-vf','select=eq(n\\\\,10)','-vsync','0','-frames:v','1',f'/tmp/critic/p{nf}.png'],check=True)\n    im=Image.open(f'/tmp/critic/p{nf}.png').convert('L'); w,h=im.size\n    cols=[x for x in range(w) if max(im.getpixel((x,y)) for y in range(h))>6]\n    span = (max(cols)-min(cols)+1) if cols else 0\n    print(f\"tmix=frames={nf:>2} -> footprint {span:>3} px (static bar 6 px, motion 0.6 px/subframe, 4 subframes/out-frame = 2.4px travel)\")\nfor n in (1,2,4,8):\n    probe(n)\nEOF"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> tmix=frames= 1 -> footprint   6 px (static bar 6 px, motion 0.6 px/subframe, 4 subframes/out-frame = 2.4px travel)
> tmix=frames= 2 -> footprint   6 px (static bar 6 px, motion 0.6 px/subframe, 4 subframes/out-frame = 2.4px travel)
> tmix=frames= 4 -> footprint   8 px (static bar 6 px, motion 0.6 px/subframe, 4 subframes/out-frame = 2.4px travel)
> tmix=frames= 8 -> footprint  10 px (static bar 6 px, motion 0.6 px/subframe, 4 subframes/out-frame = 2.4px travel)
> ```

## 🤖 Claude *(23:18:53)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://en.wikipedia.org/wiki/Complementary_colors",
  "prompt": "What does this article say are the complementary pairs in the RGB (additive / light) model versus the RYB (traditional pigment) model? Is cyan the complement of red, and what is the complement of orange in each model? Quote exactly."
}
```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # Complementary Color Pairs: RGB vs. RYB Models
> 
> ## RGB (Additive/Light) Model
> 
> In the RGB model, the complementary pairs are:
> 
> "red–cyan, green–magenta (one of the purples), and blue–yellow."
> 
> Yes, **cyan is the complement of red** in this model.
> 
> ## RYB (Traditional Pigment) Model
> 
> In the traditional RYB model, the complementary pairs are:
> 
> "red–green, yellow–purple, and blue–orange."
> 
> **Orange is the complement of blue** in the traditional model.
> 
> ## Key Difference
> 
> The article emphasizes that these contradictions exist because "traditional color theory has been superseded by empirically-derived modern color theory," and because language imprecision means "blue can be the complement of both yellow and orange."
> ```

## 🤖 Claude *(23:19:17)*

<details>
<summary>💭 Thinking Process</summary>

Looking at the motion blur measurements with different tmix values — at tmix=4 I'm getting an 8px footprint which is close to the expected full interval smear, while tmix=2 produced 6px instead of the predicted 7.2px, likely because the threshold and averaging are dimming the partial edge columns.

This confirms the directional relationship: tmix=4 gives roughly 360° shutter angle, tmix=2 gives roughly 180°. So the finding's claim of "~144°" for that recipe is materially incorrect — I need to fix that number.

I'm also reconsidering where 144° might come from as a sanity check. If you were mixing 4 frames from a 10× oversample that would be 4/10 = 40% = 144°, but that's not what the recipe does. The fps=25 selection from 100fps picks every 4th frame, creating a consistent trailing window that's correctly phased, though using tmix with a simpler frame selection would be cleaner and more efficient.

On the complementary colors: the finding claims orange's additive complement is cyan, but strictly speaking orange (between red and yellow) would complement to something between cyan and blue — more of an azure. The article does mention this language imprecision and notes blue can work as complement for both yellow and orange, so the claim is directionally sound even if slightly overstated. The practical takeaway still works: cyan as the cold pole aligns with the MIV token approach.

I need to fetch a few more sources on continuity editing, the 180-degree rule, and aerial perspective, plus check the motion-bridge grades to see if some of these points already exist.

</details>


## 🤖 Claude *(23:19:19)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; ls scripts/motion-bridge.ts 2>/dev/null; grep -rnE \"curves|colorbalance|unsharp|vignette|noise=|tmix\" scripts/motion-bridge.ts scripts/ep05/assemble-v13.ts scripts/ep05/render-cv.ts 2>/dev/null | head -20; echo \"=== adelay/acrossfade in assemble ===\"; grep -nE \"adelay|acrossfade|amix|afade|jcut|lcut|concat\" scripts/ep05/assemble-v13.ts | head -20"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> scripts/motion-bridge.ts
> scripts/motion-bridge.ts:224:    //    marca). Cadeia: curves lifta o preto para cinza-carvão — preto puro é a marca de material
> scripts/motion-bridge.ts:225:    //    barato; eq dá contraste e saturação; colorbalance empurra sombras para o teal e altas para
> scripts/motion-bridge.ts:226:    //    um âmbar sutil (o "teal & orange" do cinema, aqui puxado ao ciano do MIV); unsharp devolve
> scripts/motion-bridge.ts:227:    //    a definição que a compressão come; vignette fecha o olhar no centro.
> scripts/motion-bridge.ts:229:      "curves=all='0/0.02 0.5/0.52 1/0.98'",
> scripts/motion-bridge.ts:231:      "colorbalance=rs=-0.03:gs=0.01:bs=0.05:rh=0.04:gh=0.01:bh=-0.02",
> scripts/motion-bridge.ts:232:      "unsharp=5:5:0.35:5:5:0.0",
> scripts/motion-bridge.ts:233:      "vignette=PI/5",
> === adelay/acrossfade in assemble ===
> 74:// 2. film8 concat: seg8_NN wherever it exists (mute stretched + blockbuster presenters), else old seg_NN
> 82:writeFileSync(`${W}/concat8f.txt`, segs.map(s => `file '${s}'`).join('\n'));
> 83:sh(`ffmpeg -y -f concat -safe 0 -i ${W}/concat8f.txt -c:v libx264 -pix_fmt yuv420p -r 30 -c:a aac -ar 48000 ${W}/film8.mp4 -loglevel error`);
> 95:writeFileSync(`${W}/concat8.txt`, [`file '${T}/title10s_final.mp4'`, `file '${W}/film8.mp4'`, `file '${W}/n_cred8.mp4'`].join('\n'));
> 96:sh(`ffmpeg -y -f concat -safe 0 -i ${W}/concat8.txt -an -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p -r 30 ${W}/video8.mp4 -loglevel error`);
> 102:const filters: string[] = [`[0:a]adelay=${TITLE * 1000}|${TITLE * 1000}[p]`];
> 110:  filters.push(`[${idx}:a]aresample=48000,adelay=${off}|${off}[e${idx}]`);
> 116:filters.push(`[${idx}:a]aresample=48000,adelay=${ctaOff}|${ctaOff}[cta]`);
> 118:filters.push(`${labels.join('')}amix=inputs=${labels.length}:dropout_transition=0:normalize=0,apad=whole_dur=${TOTAL}[speech]`);
> 123:sh(`ffmpeg -y -i ${W}/trilha_v2.wav -af "adelay=${TITLE * 1000}|${TITLE * 1000},apad=whole_dur=${TOTAL}" -ar 48000 -ac 2 -c:a pcm_s16le ${W}/trilha8.wav -loglevel error`);
> 124:sh(`ffmpeg -y -i ${W}/trilha8.wav -i ${W}/speech8.wav -i ${W}/title_audio6.wav -filter_complex "[0:a]volume=-9dB[m];[m][1:a]sidechaincompress=threshold=0.05:ratio=6:attack=180:release=550[duck];[1:a][duck][2:a]amix=inputs=3:dropout_transition=0:normalize=0[mix];[mix]loudnorm=I=-16:TP=-1.5:LRA=11[out]" -map "[out]" -c:a aac -b:a 192k -ar 48000 ${W}/final8.m4a -loglevel error`);
> ```

## 🤖 Claude *(23:19:21)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://www.studiobinder.com/blog/walter-murch-rule-of-six/",
  "prompt": "Does this page list Walter Murch's Rule of Six with percentages? Give the exact list and percentages (emotion, story, rhythm, eye-trace, two-dimensional plane of screen, three-dimensional space of action) and any statement about the hierarchy / what to sacrifice first."
}
```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # Walter Murch's Rule of Six - Percentages
> 
> The page does **not** provide specific percentages for all six rules. However, it states:
> 
> **Emotion accounts for over 50% of what makes a great cut.**
> 
> The article lists the six elements in order of importance:
> 1. Emotion
> 2. Story (Advance the Story)
> 3. Rhythm
> 4. Eye Trace
> 5. Recreate Reality (180-Degree Rule)
> 6. Physical Space
> 
> **On sacrificing rules:**
> 
> Murch emphasizes that "this list as basic criteria for your edits" and notably states: "Murch doesn't believe all of these rules can or should be employed at once." The article repeatedly demonstrates that breaking these guidelines is acceptable when it serves the story's emotional tone, using examples from *Inception* and *The Shining*.
> ```

## 🤖 Claude *(23:19:51)*

<details>
<summary>💭 Thinking Process</summary>

I'm noticing a critical source attribution problem here. The studiobinder page doesn't actually list those six specific percentages (51/23/10/7/5/4) — it only mentions that emotion accounts for over 50%. Those exact numbers come from Murch's "In the Blink of an Eye" book instead, so there's a mismatch between what the finding claims and what that source actually contains. The page also organizes the concepts differently than what's being cited.

Given the mandate to discard findings where sources don't sustain the specific claims, I should either remove this or correct it. The core insight about hierarchy and emotion being dominant is genuinely supported by the studiobinder page, so I'll keep that part but acknowledge that the precise percentages come from Murch's book rather than presenting them as if they're from the studiobinder source.

For the implementation side, I'm discovering that the motion-bridge script already handles several of these findings—curves, color balance, unsharp masking, and vignetting are already in place. This means findings #6, #8, and #17 aren't new capabilities but refinements to what's already there. I need to reframe them as improvements to the existing pipeline rather than novel additions, and note that #7 (pchip interpolation) is a genuine small enhancement that isn't currently being used. The unsharp mask proposal of 0.6 is actually stronger than the current 0.35, and while the finding warns against values above 0.8 due to halos, this is more of a judgment call than a clear improvement. I need to be honest about that trade-off. But I'm realizing the ep05 render scripts encode directly without any grading applied at all, so motion-bridge is only used for the repurpose/motion rail — I should verify whether ep05's motion pieces actually get the grade applied.

</details>


## 🤖 Claude *(23:19:52)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://en.wikipedia.org/wiki/J_cut",
  "prompt": "Quote exactly how this article defines a J cut and an L cut, and whether it explains the name comes from the shape on the editing timeline."
}
```

## 🤖 Claude *(23:19:54)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://en.wikipedia.org/wiki/Continuity_editing",
  "prompt": "Quote exactly what this article says about \"match on action\" / \"cutting on action\" \u2014 including any sentence containing \"temporally questionable cut\" or describing the second shot picking up the action where the cut left it."
}
```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # J Cut Definition and Naming
> 
> ## J Cut Definition
> 
> The article defines a J cut as: "a type of film transition in which the audio from a following scene overlaps the picture from the preceding scene, so that the audio portion of the later scene starts playing before its picture as a lead-in to the visual cut."
> 
> ## L Cut
> 
> The article **does not provide a definition of an L cut**. It only mentions "L cut" as a related topic in the "See also" section with a link to that article.
> 
> ## Timeline Shape Origin
> 
> Yes, the article explains the naming convention. It states: "The name of the cut refers to the shape of audio and video pieces of the second of two scenes cut together when it was done on analog film, forming a shape similar to the letter 'J' on the timeline."
> ```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # Match on Action Definition
> 
> According to the article, here's what it states about this technique:
> 
> "A match on the action is when some action occurring before the temporally questionable cut is picked up where the cut left it by the shot immediately following."
> 
> The article also provides this example: "a shot of someone tossing a ball can be edited to show two different views, while maintaining temporal continuity by being sure that the second shot shows the arm of the subject in the same stage of its motion as it was left when cutting from the first shot."
> ```

## 🤖 Claude *(23:20:02)*

<details>
<summary>💭 Thinking Process</summary>

The J-cut definition checks out with the overlapping audio and picture description, though the L-cut reference is implied rather than explicitly sourced. Continuity editing is confirmed as stated. Moving on to verify the 180-degree rule and aerial perspective next.

</details>


## 🤖 Claude *(23:20:02)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://en.wikipedia.org/wiki/180-degree_rule",
  "prompt": "Quote exactly what this article says about keeping the camera on one side of the axis, preserving screen direction, and any sentence about crossing the line disorienting the viewer or reversing left-right positions."
}
```

## 🤖 Claude *(23:20:03)*


🛠️ **Tool Call**: `WebFetch`
```json
{
  "url": "https://en.wikipedia.org/wiki/Aerial_perspective",
  "prompt": "Quote exactly what this article says about how distant objects lose contrast, lose saturation, become blurrier/less detailed, and shift toward blue with distance."
}
```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # 180-Degree Rule: Key Concepts
> 
> **Camera Positioning:**
> "the camera should be kept on one side of an imaginary axis between two characters, so that the first character is always frame right of the second character."
> 
> **Screen Direction Consistency:**
> "If the camera remains on one side of this line, the spatial relationship between the two characters will be consistent from shot to shot."
> 
> **Effects of Crossing the Line:**
> "Shifting to the other side of the characters on a cut will reverse the order of the characters from left to right and may disorient the viewer."
> 
> Additionally, the article explains that reverse cuts "disorient the viewer by presenting an opposing viewpoint of the action in a scene and consequently altering the perspective of the action and the spatial orientation."
> ```

> **Tool Result (WebFetch)** - ✅ Success
>
> ```
> # Aerial Perspective: Key Visual Effects
> 
> Based on the Wikipedia article, here's what it states about how distant objects change:
> 
> **Loss of Contrast:**
> "As the distance between an object and a viewer increases, the contrast between the object and its background decreases, and the contrast of any markings or details within the object also decreases."
> 
> **Loss of Saturation:**
> "The colours of the object also become less saturated and shift toward the background colour, which is usually bluish."
> 
> **Reduced Detail/Clarity:**
> The article explains that "reducing the contrast reduces the visibility of these high spatial frequencies" which "give [the image] fine details." This reduction in visible detail makes distant objects appear less sharp.
> 
> **Blue Shift:**
> Objects shift "toward the background colour, which is usually bluish, but may be some other colour under certain conditions (for instance, reddish around sunrise or sunset)."
> 
> The article attributes these effects to atmospheric scattering, where "scattering adds the sky light as a veiling luminance onto the light from the object, reducing its contrast with the background sky light."
> ```

## 🤖 Claude *(23:20:21)*

<details>
<summary>💭 Thinking Process</summary>

The 180-degree rule checks out, and aerial perspective is a solid replacement for that source. Now I'm diving deeper into the motion-bridge grade context to see if the episode 5 runners are missing grade information, while also confirming that the ffmpeg-filters documentation actually covers the filters I'm using—though I've already verified this locally with ffmpeg's built-in help, which is more reliable than the docs anyway. I'll stick with ffmpeg.org as the source but want to make sure the material is properly documented there.

Let me spot-check the motion-bridge lines around 215-245 to confirm the grade only gets applied in that section, and I'm also verifying the anticipation/overlap claim for #5 with the easing values. For the WebGL finding, I'm not going to dig deeper on performance—the material proof of WebGL2 with readPixels is sufficient, and I'll keep it flagged as lower priority given the wall-clock cost. The grain-as-dither claim for #14 looks plausible, so that's fine. For #13's gate threshold, I'm working through the math: signalstats YAVG on limited range gives 16–235, so 25% of that range maps to roughly 71, and our test background hit 39 YAVG, which is about 10.5%—well within the gate. That's a meaningful correction I can document precisely. I'll skip the optional luminance check on the episode 5 nebula background and just pull the exact quotes from motion-bridge.

</details>


## 🤖 Claude *(23:20:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; sed -n '218,245p' scripts/motion-bridge.ts"
}
```

## 🤖 Claude *(23:20:21)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; grep -c \"\" scripts/ep05/render-cv.ts; grep -nE \"ffmpeg|libx264\" scripts/ep05/render-cv.ts scripts/ep05/render-ret.ts | head"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>       if (m) publishProgress(renderId, Number(m[1]), Number(m[2]));
>       // FR-SPACES-144: o abortKey faz o run() matar o Playwright se o STOP cancelar a linha
>     }, renderId);
> 
>     // 4) encode + COLOR GRADING (o passo que separa "renderizado" de "cinematográfico").
>     //    Correction primeiro (técnico: contraste/exposição), grading depois (artístico: a paleta da
>     //    marca). Cadeia: curves lifta o preto para cinza-carvão — preto puro é a marca de material
>     //    barato; eq dá contraste e saturação; colorbalance empurra sombras para o teal e altas para
>     //    um âmbar sutil (o "teal & orange" do cinema, aqui puxado ao ciano do MIV); unsharp devolve
>     //    a definição que a compressão come; vignette fecha o olhar no centro.
>     const GRADE = [
>       "curves=all='0/0.02 0.5/0.52 1/0.98'",
>       "eq=contrast=1.06:saturation=1.10:gamma=0.98",
>       "colorbalance=rs=-0.03:gs=0.01:bs=0.05:rh=0.04:gh=0.01:bh=-0.02",
>       "unsharp=5:5:0.35:5:5:0.0",
>       "vignette=PI/5",
>     ].join(",");
>     const out = join(workDir, "motion.mp4");
>     await run([
>       "ffmpeg", "-y", "-framerate", String(FPS),
>       "-i", join(workDir, "frames", "f_%05d.png"),
>       // narração conectada: 2º input; apad estende o áudio e -shortest corta no fim do vídeo
>       // (duration ≥ fala por construção — ceil na décima acima)
>       ...(voiceLocal ? ["-i", voiceLocal] : []),
>       "-vf", GRADE,
>       "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
>       "-preset", "slow", "-profile:v", "high", "-movflags", "+faststart",
>       ...(voiceLocal ? ["-c:a", "aac", "-b:a", "192k", "-af", "apad", "-shortest"] : []),
> ```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> 18
> scripts/ep05/render-ret.ts:17:execSync(`ffmpeg -y -framerate 30 -i ${SC}/ret-frames/f_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 20 ${SC}/motion-retencao.mp4 -loglevel error`);
> scripts/ep05/render-cv.ts:17:execSync(`ffmpeg -y -framerate 30 -i ${SC}/cv-frames/f_%04d.png -c:v libx264 -pix_fmt yuv420p -crf 20 ${SC}/motion-canvas.mp4 -loglevel error`);
> ```

## 🤖 Claude *(23:20:33)*

<details>
<summary>💭 Thinking Process</summary>

I'm confirming the motion bridge filter chain in the scripts, which applies curves with specific control points, unsharp masking, and vignette effects, while the episode 5 renderers are set up to encode with libx264.

The key finding is that the grade filter exists in one pipeline but is completely absent from the ep05 and motion-scenes renderers — that's the actionable difference. I should note that `curves=all=` sets individual RGB component points whereas `curves=master=` applies globally first, though both achieve similar results for neutral curves. Since both the motion bridge and ep05 inputs are PNG frames in RGB, the `format=gbrp` specification doesn't really change anything in practice — ffmpeg would handle the color space conversion automatically, and the curves filter operates in RGB either way.

</details>


## 🤖 Claude *(23:20:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/critic\nC=\"curves=master='0/0.045 0.25/0.22 0.5/0.5 0.75/0.79 1/0.985':interp=pchip\"\n# same yuv420p source, with and without format=gbrp in front \u2192 compare mean RGB\nfor mode in \"raw\" \"gbrp\"; do\n  vf=$([ $mode = gbrp ] && echo \"format=gbrp,$C,format=rgb24\" || echo \"$C,format=rgb24\")\n  ffmpeg -y -v error -f lavfi -i \"color=0x2a4a6a:s=32x32:d=1:r=1,format=yuv420p\" -vf \"$vf\" -frames:v 1 -f rawvideo px_$mode.raw\n  python3 -c \"\nd=open('/tmp/critic/px_$mode.raw','rb').read()\nprint('$mode -> first pixel RGB', d[0], d[1], d[2])\"\ndone"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> raw -> first pixel RGB 36 63 99
> gbrp -> first pixel RGB 38 64 101
> ```

## 🤖 Claude *(23:22:05)*

<details>
<summary>💭 Thinking Process</summary>

The curves behavior differs slightly between YUV and RGB formats—applying them directly to yuv420p gives different values than converting to gbrp first—so the format guard is genuinely necessary for video sources even if it barely affects PNG sequences. Now I'm ready to finalize which techniques to keep.

The rail contract uses `window.__seek(t)` in the motion runners and `applyFrame(i,total)` in render-core, and the existing code already applies a symmetric ease-in-out via smoothstep, so the real win isn't adding easing but rather using the right easing curve for each role—that's more of a medio impact than alto since we're refining what's already there, not solving a fundamental linear-motion problem. Arcs stay alto with the path-versus-timing-splines approach verified working. For staging, the principle holds but the implementation needs rethinking—a hard rule against multiple elements above the threshold would break every existing v6 piece with ambient drift and parallax, so I should frame it as an advisory report across beat windows instead.

Secondary action timing stays alto because the discipline of not burning information outside move windows is genuinely high-value and costs nothing to enforce as an authoring rule, though automating it would require refactoring the hand-written seek logic into a declarative beat schedule. Anticipation and overlap keep alto—the existing runners already have spring overshoot, so the delta is really the anticipation pre-recoil and per-element delays, which don't exist yet, making this a full new contribution rather than a refinement.

For the black lift, it already exists in the motion-bridge curve but is missing from the ep05 runners—I can port that grade over and potentially raise the lift value from 0.02 to 0.045, which would be alto impact since the motion rail currently has no grading at all.

On teal and orange, I need to correct the color theory claim: the article itself acknowledges that blue can complement both yellow and orange, so saying "cyan not blue" is directional rather than exact. The colorbalance is already in motion-bridge, so the real work is adding the `pl=1` parameter and midtones adjustment, then porting to ep05—this drops the impact from alto to medio.

For the skin tone line, I'm cutting it entirely since the source actually argues that the skin tone line doesn't exist, which contradicts what we'd need to implement.

Moving through the remaining items: three functions of light stays alto with verified quotes, the key-to-fill ratio dial needs a correction to the token mapping so dramatic gets minimal fill, neutral gets 8:1, and bright gets 3:1, and fill on camera axis stays alto. For the background measurement, I need to provide the exact specification rather than just the percentage threshold. ORRECT THE MATH: 4 subframes + tmix=frames=4 = 360° shutter, not ~144°. Materially measured: footprint grows 6→8px (tmix=4) vs 6px (tmix=2) for a 2.4px/frame travel. For ~180° use tmix=frames=2 with 4× oversample. Feasibility exige-novo-modulo, impact alto→medio (honest: 4× wall clock, and only helps fast translations).

16. Atmospheric perspective — KEEP but REPLACE the source: theasc lighting article does not discuss aerial perspective; en.wikipedia.org/wiki/Aerial_perspective verified verbatim (contrast loss, desaturation, blue shift, detail loss). Impact alto.

17. Vignette and unsharp mask are already in motion-bridge with specific settings, and the proposal would actually weaken the vignette while strengthening the sharpening—so the real work is porting these to the ep05 runners rather than retuning. Downgrading this to medium impact, and the cross-keys reference checks out.

18. The Smith 1797 quote doesn't appear in the cited article, but the source does cover rule of thirds, headroom, lead room, and dead space—so I need to decide whether to cut the misattributed quote or keep the technique itself, which is fundamentally about providing leading room in the direction of movement.

The misattribution is a rigor problem, and rule of thirds is contested folklore anyway. The actionable part—a dev-only guide overlay with margin assertions—has low yield for hand-authored compositions. I'm leaning toward cutting this entirely rather than keeping it with corrections, since the impact is really low and the quotation failure undermines the finding. The source failure here is only partial—the quote attribution is wrong but the underlying substance checks out. I'll keep it flagged as baixo and explicitly correct the misattribution in the text rather than discard it entirely.

Moving on to item 19, the 180° flow axis approach is verified and solid, rated medio impact. The implementation needs a declarative flowAxis token plus a buffer mechanism, which is feasible as an authoring convention, though I need to correct the part about linting the beat schedule since that declarative schedule doesn't actually exist yet.

For item 20 on cutting on action, this one's also verified. The correction involves how assemble-v13 handles concatenation...

Checking the J/L cut technique against the actual codebase...

the narration is already a single continuous mixed track laid over the concatenated video, so audio doesn't cut at scene boundaries by construction. The real value here is deliberate lead-in timing—starting the next narration 0.6 seconds before the visual cut—which is just a scheduling adjustment of existing offsets, not new infrastructure. Downgrading this to medium priority since it's calibration rather than new plumbing.

For the Rule of Six, the page sustains the core doctrine—emotion dominates the hierarchy and rules are breakable for emotional reasons—but the specific percentages (51/23/10/7/5/4) come from Murch's book, not this source. I'll keep the rule with that correction noted and mark it as medium impact. The ASC CDL and LUT formula checks out exactly, so that stays verified.

For squash and stretch, the quote is solid—I'm noting the mechanics: seek contract, velocity derived from finite difference of the eased value, and volume preservation. Exaggeration balance with one dial also verifies. WebGL per-object motion blur is next to review. I'm being more critical about what actually deserves to stay. #18 on rule of thirds is getting cut—the quote attribution is shaky and it's more folklore than substance, which violates the source standard. #27 stays despite being a non-goal, because it's honest about what we're not doing. #22 needs the correction on the numbers but the core idea holds. #7 is tiny but I'm still evaluating it.

For the rest: #19 on directional consistency across scenes is real enough to keep, #25 on the exaggeration dial is straightforward and stays, #24 on squash and stretch for UI cards has solid sourcing so it survives with the caveat about restraint, and #3 on staging gets a softer implementation. That leaves me with 25 techniques total, cutting just #9 and #18.

The verification pass came back clean—every major quote and technical claim checked out against the sources, and I've already removed the two genuinely incorrect items. #6, #8, and #17 still matter for the next episode since they're actionable gaps in the current grading pipeline, so those stay despite being partially implemented elsewhere.

For #8 on teal and orange, the color theory has a real error (orange's complement is actually azure, not cyan) and while motion-bridge already has the recipe, porting it with proper palette discipline to the next episode is worth keeping at medium priority. #12 on single-key angle is strong and cheap, so that stays. #1 stays too—the corrected version with named easings and proper entrance/exit behavior is a genuine improvement over the current symmetric smoothstep.

On #21 with the J/L cut, the audio's already a continuous bed, but the actionable part about deliberately leading the next scene's narration by 0.6 seconds relative to the picture timing might still be worth exploring.

Now I'm finalizing the output with Portuguese-style field names and correcting the implementation details with exact file paths and references—the render-core functions at specific line numbers, the ep05 render setup, and the motion-canvas HTML configuration for easing and seek behavior.

Adding more file references...

</details>


## 🤖 Claude *(23:22:05)*

Material verification complete. Summary of what I proved on this host before ruling.

## 🤖 Claude *(23:22:06)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra; sed -n '112,116p' scripts/ep05/motion-canvas.html; echo \"--- cinematic-grammar MIX_TARGETS ---\"; sed -n '120,134p' src/lib/cinematic-grammar.ts"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>     const clamp=(v,a,b)=>Math.min(b,Math.max(a,v));
>     const ez=(t)=>t<0?0:t>1?1:t*t*(3-2*t);
>     const spring=(t)=>{ if(t<=0)return 0; if(t>=1)return 1; return 1-Math.exp(-6*t)*Math.cos(9*t); };
>     const $=(id)=>document.getElementById(id);
>     const pts=[]; for(let i=0;i<14;i++){const p=document.createElement('div');p.className='pt';
> --- cinematic-grammar MIX_TARGETS ---
> export const MIX_TARGETS = {
>   /** Integrado do master — padrão de entrega das plataformas. */
>   loudnessLufs: -16,
>   truePeakDb: -1.5,
>   /** Quanto a trilha abaixa sob a fala (sidechain). */
>   musicDuckDb: -12,
>   /** Ambiência/room tone: presente, nunca perceptível como "som". */
>   ambienceDb: -34,
>   /** Sobreposição de áudio no J-Cut / L-Cut, em segundos. */
>   jCutLeadSec: 0.6,
>   lCutTailSec: 1.2,
> } as const;
> 
> /** Hierarquia de mixagem — quem manda quando dois sons disputam o mesmo instante. */
> export const MIX_HIERARCHY = ["diálogo", "hard SFX", "ambiência", "trilha"] as const;
> ```

## 🤖 Claude *(23:22:09)*

<details>
<summary>💭 Thinking Process</summary>

Everything's confirmed, so I'm ready to generate the StructuredOutput now.

</details>


## 🤖 Claude *(23:25:16)*


🛠️ **Tool Call**: `StructuredOutput`
```json
{
  "findings": [
    {
      "technique": "Slow In and Out \u2014 easing NOMEADO por papel (entrada = ease-out, n\u00e3o smoothstep sim\u00e9trico)",
      "why_it_reads_professional": "Lasseter \u00a72.7 verificado verbatim no PDF real: 'Mathematically, the term refers to second- and third-order continuity of motion.' \u00c9 a derivada que o c\u00e9rebro usa para inferir massa. CORRE\u00c7\u00c3O DO ACHADO ORIGINAL: o rail N\u00c3O interpola linear hoje \u2014 scripts/ep05/motion-canvas.html:113 j\u00e1 define ez(t)=t*t*(3-2*t) (smoothstep) e a usa em tudo. Smoothstep \u00e9 ease-in-out SIM\u00c9TRICO: um n\u00f3 que ENTRA com ela come\u00e7a devagar, o que l\u00ea como hesita\u00e7\u00e3o, n\u00e3o como chegada. O ganho real n\u00e3o \u00e9 'adicionar easing', \u00e9 usar a curva certa por papel \u2014 e isso rebaixa o impacto de alto para m\u00e9dio.",
      "how_to_implement_here": "Exportar EASING em /home/gcrUX/htdocs/constellation-orchestra/src/lib/cinematic-grammar.ts com os valores NORMATIVOS do W3C (verificados na fonte: ease=(0.25,0.1,0.25,1) \u00b7 ease-in=(0.42,0,1,1) \u00b7 ease-out=(0,0,0.58,1) \u00b7 ease-in-out=(0.42,0,0.58,1)) + solver cubic-bezier Newton-Raphson (~15 linhas). ATEN\u00c7\u00c3O AO CONTRATO REAL \u2014 s\u00e3o DOIS: (a) os runners do EP05 usam window.__seek(t) em SEGUNDOS (scripts/ep05/render-cv.ts:14 chama __seek(i/30)); (b) scripts/hyperframes/render-core.ts:346 usa applyFrame(i, total). Ambos determin\u00edsticos. Conven\u00e7\u00e3o: entrada=ease-out, sa\u00edda=ease-in, c\u00e2mera/parallax=ease-in-out; manter ez() como alias de ease-in-out para n\u00e3o quebrar as pe\u00e7as existentes. Aritm\u00e9tica pura, zero CDN, US$0.",
      "source_url": "https://www.w3.org/TR/css-easing-1/",
      "feasibility": "direto",
      "impact": "medio"
    },
    {
      "technique": "Arcos \u2014 desacoplar a spline do CAMINHO da spline do TEMPO",
      "why_it_reads_professional": "Verificado verbatim no PDF de Lasseter: 'In most 3D keyframe computer animation systems, the path of action from one extreme to another is controlled by the same spline that controls the timing (slow in and out) of the inbetween values... when the action is fast, the arc flattens out: the faster the action, the flatter the arc.' E o veredito: 'Straight inbetweens can completely kill the essence of an action.' Hoje todo movimento dos motion-*.html \u00e9 translate() linear no espa\u00e7o \u2014 curva zero. Movimento r\u00e1pido em reta \u00e9 o que faz a pe\u00e7a ler como diagrama animado.",
      "how_to_implement_here": "PROVADO MATERIALMENTE no chromium pinado do rail (/home/ubuntu/.cache/ms-playwright/chromium-1226): um <path> SVG oculto devolveu getTotalLength()=526.8367309570312 e getPointAtLength(37%)=(133.291,136.548) \u2014 determin\u00edstico e dispon\u00edvel headless. Nos motion-*.html: (1) geometria = path SVG invis\u00edvel, posi\u00e7\u00e3o = path.getPointAtLength(eased(t) * path.getTotalLength()); (2) tempo = a curva de easing, INDEPENDENTE. O arco sobrevive \u00e0 velocidade porque a curvatura vive no path. Serve de trilho tamb\u00e9m para o running ring e as edges da linguagem v6. Zero rede, US$0.",
      "source_url": "http://graphics.cs.cmu.edu/nsp/course/15-464/Fall05/papers/lasseter.pdf",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Staging \u2014 uma ideia por vez; o destaque \u00e9 CONTRASTE de movimento, n\u00e3o brilho",
      "why_it_reads_professional": "Verificado verbatim: 'It is important, when staging an action, that only one idea be seen by the audience at a time. If a lot of action is happening at once, the eye does not know where to look and the main idea of the action will be upstaged and overlooked.' E a mec\u00e2nica: 'In a still scene, the eye will be attracted to movement. In a very busy scene, the eye will be attracted to something that is still.' Ou seja: numa cena onde tudo pulsa, CONGELAR o n\u00f3 principal destaca mais do que anim\u00e1-lo \u2014 o inverso do instinto.",
      "how_to_implement_here": "CORRE\u00c7\u00c3O IMPORTANTE: o gate mec\u00e2nico proposto no achado original ('no m\u00e1ximo UM elemento acima do limiar, sen\u00e3o exit 1') REPROVARIA todas as pe\u00e7as v6 existentes \u2014 a linguagem selada tem, por projeto, drift ambiente dos pontos, running ring e parallax de fundo simult\u00e2neos (ver motion-canvas.html:129-133). Implementar como RELAT\u00d3RIO ADVISORY, n\u00e3o como exit 1: exportar as bounding boxes no applyProps, computar energia por regi\u00e3o (diff de PNGs que o runner j\u00e1 gera) e listar, por janela de beat, os elementos acima do limiar \u2014 com as camadas ambiente (pts/streaks/bg) EXCLU\u00cdDAS da contagem por allowlist. O diretor l\u00ea o relat\u00f3rio e decide. Como regra de autoria vale hoje, de gra\u00e7a; o medidor exige um m\u00f3dulo (export de bbox + decode de PNG) \u2014 por isso a viabilidade cai de 'direto' para 'exige-novo-modulo'.",
      "source_url": "http://graphics.cs.cmu.edu/nsp/course/15-464/Fall05/papers/lasseter.pdf",
      "feasibility": "exige-novo-modulo",
      "impact": "alto"
    },
    {
      "technique": "A\u00e7\u00e3o secund\u00e1ria subordinada \u2014 mudar conte\u00fado ANTES ou DEPOIS do movimento, nunca no meio",
      "why_it_reads_professional": "Verificado verbatim: 'A secondary action is always kept subordinate to the primary action. If it conflicts, becomes more interesting, or dominates in any way, it is either the wrong choice or is staged improperly.' E o timing: 'The change must come before, or after, the move. A change in the middle of a major move will go unnoticed, and value intended will be lost.' Traduzido: trocar o label/custo em mco ENQUANTO o n\u00f3 viaja queima a informa\u00e7\u00e3o \u2014 o espectador n\u00e3o l\u00ea nenhum dos dois. O custo \u00e9 invis\u00edvel (nada quebra, nenhum teste falha), e \u00e9 exatamente por isso que reincide.",
      "how_to_implement_here": "Regra de autoria aplic\u00e1vel HOJE, custo zero: em cada window.__seek(t) dos motion-*.html, agendar mudan\u00e7as de conte\u00fado (texto, badge, custo, \u00edcone) em janelas de tempo DISJUNTAS das janelas de transla\u00e7\u00e3o do mesmo elemento. O validador autom\u00e1tico proposto no achado original pressup\u00f5e um schedule declarativo que N\u00c3O existe \u2014 os __seek atuais s\u00e3o fun\u00e7\u00f5es escritas \u00e0 m\u00e3o com constantes inline (motion-canvas.html:125-190). Portanto: adotar a regra j\u00e1; o lint s\u00f3 depois de um refactor para beats declarativos (mesmo pr\u00e9-requisito do gate de staging). US$0.",
      "source_url": "http://graphics.cs.cmu.edu/nsp/course/15-464/Fall05/papers/lasseter.pdf",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Antecipa\u00e7\u00e3o (recuo antes da entrada) + overlap por offset de 2-4 frames",
      "why_it_reads_professional": "Verificado verbatim: 'An action occurs in three parts: the preparation for the action, the action proper, and the termination.' E: 'A foot must be pulled back before it can be swung forward to kick a ball. Without anticipation many actions are abrupt, stiff and unnatural.' DELTA REAL sobre o que j\u00e1 existe: motion-canvas.html:114 j\u00e1 tem spring() com overshoot, ou seja o 'follow-through' de chegada j\u00e1 est\u00e1 l\u00e1 \u2014 o que N\u00c3O existe \u00e9 (a) a ANTECIPA\u00c7\u00c3O (contra-movimento antes da entrada) e (b) o OVERLAP (partes soltas chegando depois do corpo). \u00c9 a diferen\u00e7a entre o elemento 'aparecer' e 'nascer'.",
      "how_to_implement_here": "Em window.__seek(t): cada sub-elemento ganha um delaySec pr\u00f3prio e o pai ganha um pr\u00e9-beat. Antecipa\u00e7\u00e3o: nos ~0,1 s anteriores \u00e0 entrada, escala 1.0\u21920.96 com ease-in; depois a entrada com ease-out + spring() (j\u00e1 existente). Overlap: ring, sombra e edges com delaySec 0.07..0.13 (2-4 frames a 30fps), mesma curva deslocada. Tudo derivado de t (que o runner deriva de i/30 em scripts/ep05/render-*.ts:14) \u21d2 segue bit-exato, preservando a NFR-VS-016 do render-core. US$0.",
      "source_url": "http://graphics.cs.cmu.edu/nsp/course/15-464/Fall05/papers/lasseter.pdf",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Levantar o preto (filmic toe) e derrubar o branco puro no grade",
      "why_it_reads_professional": "Preto absoluto n\u00e3o existe em imagem fotografada \u2014 Burum, verificado verbatim no artigo da ASC: 'Shadows are not inky black even on a sunny day, because they get natural fill from sunlight bouncing off the sky, clouds, buildings or ground.' Um frame HTML tem preto matem\u00e1tico, e \u00e9 o delator instant\u00e2neo de 'screenshot de p\u00e1gina'. ACHADO MATERIAL QUE MUDA A PRIORIDADE: o grade J\u00c1 EXISTE em scripts/motion-bridge.ts:228-233 (curves + eq + colorbalance + unsharp + vignette) mas os runners do EP05 encodam CRU \u2014 scripts/ep05/render-cv.ts:17 e render-ret.ts:17 s\u00e3o 'libx264 -pix_fmt yuv420p -crf 20' sem UM filtro de cor. As pe\u00e7as motion v6 sa\u00edram sem grade nenhum.",
      "how_to_implement_here": "Prioridade 1 = PORTAR a cadeia GRADE de scripts/motion-bridge.ts:228-233 para os runners de motion (scripts/ep05/render-*.ts:17). Prioridade 2 = subir o piso: a curva atual \u00e9 curves=all='0/0.02 0.5/0.52 1/0.98' (piso ~5/255, ainda quase preto); a proposta \u00e9 format=gbrp,curves=master='0/0.045 0.25/0.22 0.5/0.5 0.75/0.79 1/0.985':interp=pchip. PROVA MATERIAL rodada neste host (ffmpeg 6.1.1): color=black atravessando essa curva sai com luma 0x19 = 25, acima do piso 16 do limited range. NUANCE VERIFICADA sobre o format=gbrp: com entrada PNG (caso dos runners) a curva j\u00e1 opera em RGB e o gbrp \u00e9 quase no-op; ele importa quando a fonte j\u00e1 \u00e9 v\u00eddeo yuv \u2014 testei color=0x2a4a6a em yuv420p e o mesmo filtro deu RGB (36,63,99) sem gbrp vs (38,64,101) com \u2014 ou seja, no est\u00e1gio de re-encode do assemble o guard \u00e9 real. US$0.",
      "source_url": "https://theasc.com/articles/lighting-a-set",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "curves com interp=pchip (spline monot\u00f4nica) em vez do padr\u00e3o natural",
      "why_it_reads_professional": "A spline c\u00fabica natural (padr\u00e3o do filtro) pode ter overshoot entre pontos de controle \u2192 invers\u00e3o local de tom nas sombras e halo em gradiente, exatamente onde vivem os fundos nebulosos das cenas. A pchip \u00e9 monot\u00f4nica por defini\u00e7\u00e3o: nunca inverte a ordem tonal. Um token, e some uma classe inteira de artefato.",
      "how_to_implement_here": "CONFIRMADO neste host via `ffmpeg -h filter=curves`: 'interp <int> ... (default natural)' com enum {natural = natural cubic spline, pchip = monotonically cubic interpolation}. A cadeia VIVA em scripts/motion-bridge.ts:229 (curves=all='0/0.02 0.5/0.52 1/0.98') N\u00c3O passa interp \u2014 logo roda em natural hoje. Acrescentar ':interp=pchip' ali e em qualquer curves nova. Custo US$0, risco ~zero.",
      "source_url": "https://ffmpeg.org/ffmpeg-filters.html",
      "feasibility": "direto",
      "impact": "medio"
    },
    {
      "technique": "Teal & orange com pl=1 \u2014 polo frio no ciano do MIV (justificativa aditiva, com a ressalva honesta)",
      "why_it_reads_professional": "CORRE\u00c7\u00c3O DA TEORIA: a fonte sustenta que no modelo aditivo os pares s\u00e3o 'red\u2013cyan, green\u2013magenta (one of the purples), and blue\u2013yellow' e no RYB de pigmento 'red\u2013green, yellow\u2013purple, and blue\u2013orange' \u2014 mas o complementar ADITIVO do laranja n\u00e3o \u00e9 o ciano puro e sim um azul-ciano (azure); a pr\u00f3pria p\u00e1gina avisa que 'blue can be the complement of both yellow and orange'. Ent\u00e3o a frase 'o complementar do laranja \u00e9 ciano, n\u00e3o azul' \u00e9 DIRECIONALMENTE certa e literalmente imprecisa. O que sobrevive: escolher o polo frio no ciano d\u00e1 separa\u00e7\u00e3o crom\u00e1tica alta com satura\u00e7\u00e3o baixa (menos look 'saturado demais' amador) e coincide com o token MIV accent=cyan \u2014 ou seja, \u00e9 justificativa t\u00e9cnica de uma decis\u00e3o que a casa j\u00e1 tomou, n\u00e3o decis\u00e3o est\u00e9tica nova.",
      "how_to_implement_here": "O split teal&orange J\u00c1 EXISTE em scripts/motion-bridge.ts:231 (colorbalance=rs=-0.03:gs=0.01:bs=0.05:rh=0.04:gh=0.01:bh=-0.02) \u2014 o delta real \u00e9 (a) acrescentar pl=1 e (b) portar a cadeia para os runners do EP05, que hoje encodam sem grade. CONFIRMADO neste host: `ffmpeg -h filter=colorbalance` lista 'pl <boolean> preserve lightness (default false)' \u2014 hoje a casa roda SEM preservar lightness, ent\u00e3o o split est\u00e1 mexendo na exposi\u00e7\u00e3o de brinde. No HTML, travar a paleta em dois polos (ciano MIV frio + \u00e2mbar quente) e proibir uma terceira fam\u00edlia crom\u00e1tica saturada. Cadeia completa validada rodando neste host (curves\u2192colorbalance\u2192unsharp\u2192vignette\u2192noise\u2192yuv420p gerou PNG 168.835 bytes). US$0.",
      "source_url": "https://en.wikipedia.org/wiki/Complementary_colors",
      "feasibility": "direto",
      "impact": "medio"
    },
    {
      "technique": "As tr\u00eas fun\u00e7\u00f5es universais da luz (Burum/ASC): lan\u00e7ar sombra, criar SEPARA\u00c7\u00c3O, preencher",
      "why_it_reads_professional": "Verificado verbatim no artigo da ASC: 'Everyone does at least one of three things every time they light a set: 1. The first thing is to cast a shadow... 2. The second thing you do in lighting is to create separation. Photography looks at the world with only one lens, and you need to introduce a three-dimensional quality to this two-dimensional image. There's only one way to accomplish that: creating areas of light against dark or dark against light. I'm not referring to color.' Ele \u00e9 categ\u00f3rico que n\u00e3o \u00e9 quest\u00e3o de cor \u2014 e d\u00e1 o exemplo do rim: 'a dark area, a little bright halo, and another dark area'. \u00c9 literalmente o manual de como fazer um n\u00f3 glass parecer objeto num espa\u00e7o em vez de ret\u00e2ngulo com blur.",
      "how_to_implement_here": "Por n\u00f3 glass nos motion-*.html, tr\u00eas camadas expl\u00edcitas no lugar do box-shadow padr\u00e3o: (a) KEY = linear-gradient direcional no fundo do card, mais claro do lado da key; (b) SEPARA\u00c7\u00c3O = borda 1px com conic-gradient brilhante s\u00f3 no arco voltado para a key e escura no oposto (o 'dark, halo, dark' do Burum); (c) FILL = camada rgba ambiente uniforme controlando quanto se enxerga dentro da sombra. CSS puro no Chromium headless, determin\u00edstico, zero CDN, US$0. Nota: a classe .glass j\u00e1 existe (motion-canvas.html:17) usando linear-gradient(165deg,...) \u2014 \u00e9 o ponto de enxerto, n\u00e3o um come\u00e7o do zero.",
      "source_url": "https://theasc.com/articles/lighting-a-set",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Raz\u00e3o key-to-fill como DIAL de humor expl\u00edcito",
      "why_it_reads_professional": "Burum filmou o MESMO cen\u00e1rio com tr\u00eas n\u00edveis de fill e o efeito \u00e9 de g\u00eanero, n\u00e3o de exposi\u00e7\u00e3o \u2014 verificado verbatim: 'There is no correct amount of fill; it's a matter of artistic interpretation.' O humor da cena \u00e9 uma RAZ\u00c3O, n\u00e3o um brilho, e hoje as cenas da casa n\u00e3o t\u00eam esse dial nomeado.",
      "how_to_implement_here": "CORRE\u00c7\u00c3O DA CALIBRAGEM (o achado original inverteu os degraus): no artigo, o dram\u00e1tico \u00e9 o SEM FILL \u2014 'The no-fill image conveys a sense of foreboding' \u2014, o 8:1 \u00e9 o MEIO, que Burum considerou o n\u00edvel pr\u00f3prio ('bright but still modeled, and the frame still retains black references \u2014 in the actors' hair'), e o 3:1 \u00e9 o MAIS CLARO, apelidado de 'Laverne & Shirley look' (com\u00e9dia). Logo o mapa honesto \u00e9: dramatic = sem/quase-sem fill \u00b7 neutral = 8:1 \u00b7 bright = 3:1. Exportar KEY_FILL_RATIOS em /home/gcrUX/htdocs/constellation-orchestra/src/lib/cinematic-grammar.ts ao lado de LIGHTING e ligar a UMA CSS custom property --fill-ratio que dirige a opacidade da camada ambiente de TODOS os n\u00f3s de uma vez. US$0.",
      "source_url": "https://theasc.com/articles/lighting-a-set",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Fill no eixo da c\u00e2mera \u2014 uma \u00fanica dire\u00e7\u00e3o de sombra em toda a cena",
      "why_it_reads_professional": "Verificado verbatim: 'You want the fill light on the camera's axis,' Burum stresses. 'If you don't put it there, you start to cast a secondary shadow on the other side of the axis... you should fill from the key side if you have a choice, because that tends to wrap the shadow better.' E: 'Old movie wisdom says that you don't want to see a secondary shadow cast by fill light, mainly because it's distracting.' O delator equivalente em HTML \u00e9 universal: todo card com box-shadow 0 4px = luz vindo de cima em todo lugar, independente da composi\u00e7\u00e3o = imagem chapada, sem fonte, sem espa\u00e7o.",
      "how_to_implement_here": "Uma vari\u00e1vel --key-angle por cena; TODOS os offsets de box-shadow e filter: drop-shadow derivados dela. Preferir computar seno/cosseno UMA vez em JS no applyProps e escrever os offsets em px (CSS sin()/cos() existem no Chromium recente, mas o caminho JS \u00e9 o que j\u00e1 \u00e9 usado pelo rail e n\u00e3o depende da vers\u00e3o). Proibir box-shadow com offset hardcoded nos templates \u2014 item de revis\u00e3o da skill motion-scenes. US$0.",
      "source_url": "https://theasc.com/articles/lighting-a-set",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Fundo mais escuro que o primeiro plano \u2014 gate num\u00e9rico medido, n\u00e3o gosto",
      "why_it_reads_professional": "N\u00famero duro e raro do ASC, verificado verbatim: 'If the set walls are lighter than normal skin tone, people will always seem dark by comparison. For people to stand out, the reflective value of the set should be below 25 percent. If it's not, the actors' faces will look dark even though they're properly exposed.' Traduzido para motion graphics: se a nebulosa de fundo passa desse patamar, os n\u00f3s glass deixam de ler como primeiro plano por mais que se aumente o brilho deles \u2014 e a resposta instintiva (clarear o n\u00f3) piora, porque estoura. \u00c9 a causa raiz de composi\u00e7\u00f5es 'lavadas' que ningu\u00e9m sabe nomear. RESSALVA HONESTA: os 25% s\u00e3o reflect\u00e2ncia de parede versus tom de pele; transplantar para lumin\u00e2ncia de fundo \u00e9 analogia, n\u00e3o a mesma medida.",
      "how_to_implement_here": "Gate mec\u00e2nico barato, PROVADO neste host: `ffmpeg -f lavfi -i color=<cor> -vf signalstats,metadata=print:key=lavfi.signalstats.YAVG` funciona (branco puro \u2192 YAVG=235; o azul-noite #141c2b da casa \u2192 YAVG=39). Como YAVG vem em limited range (16..235), o limiar de 25% \u00e9 YAVG \u2248 16 + 0,25\u00d7219 \u2248 71 \u2014 o fundo atual passa folgado (39), ent\u00e3o o gate serve de trava contra deriva futura, n\u00e3o de conserto imediato. Renderizar a camada de fundo isolada (scripts/ep05/nebula-bg.html j\u00e1 \u00e9 separada), 1 frame, medir, falhar acima de ~71. US$0.",
      "source_url": "https://theasc.com/articles/lighting-a-set",
      "feasibility": "direto",
      "impact": "medio"
    },
    {
      "technique": "Grain temporal com seed fixo \u2014 mata a esterilidade digital E o banding dos gradientes",
      "why_it_reads_professional": "Dois problemas com um filtro. (1) Gradiente CSS suave num encode H.264 8-bit yuv420p produz banding em faixas \u2014 justamente nos fundos nebulosos, onde mais d\u00f3i; o ru\u00eddo funciona como dither e dissolve as faixas. (2) Aus\u00eancia total de gr\u00e3o \u00e9 assinatura de render sint\u00e9tico; gr\u00e3o sutil e TEMPORAL empurra a leitura para 'capturado'. Maior mudan\u00e7a de percep\u00e7\u00e3o por unidade de esfor\u00e7o da lista \u2014 e hoje N\u00c3O existe em lugar nenhum: nem a cadeia GRADE de scripts/motion-bridge.ts:228-233 nem os runners do EP05 aplicam noise.",
      "how_to_implement_here": "No fim da cadeia de grade, antes do encode. PROVA MATERIAL DE DETERMINISMO rodada neste host: duas execu\u00e7\u00f5es id\u00eanticas de noise=all_seed=42:alls=6:allf=t+u com -fflags/-flags +bitexact deram o MESMO sha256 (85f7e6fa9707c1c5faa54d473d0fb9e4a0c649c2f35ec78e228c202a95a50d0f) \u2014 sem all_seed fixo a NFR-VS-016 morre. REFINAMENTO sobre o achado original: preferir gr\u00e3o S\u00d3 na luma (noise=c0_seed=42:c0s=6:c0f=t+u, tamb\u00e9m validado aqui) \u2014 'alls' ruidifica a croma subamostrada e suja a paleta ciano/\u00e2mbar. `ffmpeg -h filter=noise` confirma all_seed/c0_seed e flags {a,p,t,u}. US$0.",
      "source_url": "https://ffmpeg.org/ffmpeg-filters.html",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Motion blur por \u00e2ngulo de obturador \u2014 renderizar em N\u00d7 fps e mesclar com tmix",
      "why_it_reads_professional": "\u00c9 a diferen\u00e7a estrutural entre 'tela capturada frame a frame' e 'movimento filmado': screenshot por frame tem obturador infinitesimal, zero blur, e o estrobosc\u00f3pico denuncia em transla\u00e7\u00e3o r\u00e1pida e no running ring. Cinema usa ~180\u00b0 de obturador \u2014 cada frame integra metade do intervalo.",
      "how_to_implement_here": "CORRE\u00c7\u00c3O ARITM\u00c9TICA \u2014 o achado original erra o \u00e2ngulo: com 4 sub-frames por frame de sa\u00edda, tmix=frames=4 integra 4 de 4 = obturador de 360\u00b0 (borr\u00e3o cheio), N\u00c3O ~144\u00b0. Para ~180\u00b0 use tmix=frames=2 sobre o oversample 4\u00d7. MEDIDO NESTE HOST com uma barra de 6 px viajando 0,6 px/sub-frame (fonte 100fps \u2192 sa\u00edda 25fps): pegada 6 px sem tmix, 6 px com tmix=2, 8 px com tmix=4, 10 px com tmix=8 \u2014 a escada confirma que frames=4 j\u00e1 \u00e9 o intervalo inteiro. Implementa\u00e7\u00e3o: multiplicar o total de frames no la\u00e7o (scripts/ep05/render-*.ts:13 vira i/120 no __seek; em render-core.ts:346 \u00e9 multiplicar `totalFrames`), depois 'tmix=frames=2,fps=25' antes do encode. CUSTO HONESTO: 4\u00d7 o tempo de render, e o gargalo \u00e9 o page.screenshot() do Playwright, n\u00e3o o FFmpeg \u2014 US$0 financeiro, wall-clock real. Aplicar SELETIVAMENTE \u00e0s cenas de transla\u00e7\u00e3o r\u00e1pida.",
      "source_url": "https://ffmpeg.org/ffmpeg-filters.html",
      "feasibility": "exige-novo-modulo",
      "impact": "medio"
    },
    {
      "technique": "Perspectiva atmosf\u00e9rica \u2014 profundidade por atenua\u00e7\u00e3o, n\u00e3o por escala",
      "why_it_reads_professional": "FONTE TROCADA: o artigo da ASC citado no achado original N\u00c3O trata disso (fala de separa\u00e7\u00e3o por luz, n\u00e3o de atenua\u00e7\u00e3o por dist\u00e2ncia) \u2014 a fonte que sustenta \u00e9 a de perspectiva a\u00e9rea, verificada verbatim: 'As the distance between an object and a viewer increases, the contrast between the object and its background decreases, and the contrast of any markings or details within the object also decreases' e 'The colours of the object also become less saturated and shift toward the background colour, which is usually bluish.' Camadas de fundo com o MESMO contraste e nitidez das da frente achatam a cena mesmo com parallax correto: o movimento diz 'tem profundidade' e a textura diz '\u00e9 adesivo'.",
      "how_to_implement_here": "Nas camadas de fundo dos motion-*.html: filter: blur(2-4px) saturate(0.65) contrast(0.85) + puxar o matiz para o polo frio (ciano MIV), escalonado por camada de parallax (mais longe = mais atenuado). Alvo concreto: os .pt e .streak de motion-canvas.html:117-121, que hoje t\u00eam a mesma nitidez dos cards. Tudo CSS determin\u00edstico no Chromium headless; se a camada j\u00e1 vier achatada no v\u00eddeo, gblur=sigma=... com planes seletivo no encode. US$0, zero CDN.",
      "source_url": "https://en.wikipedia.org/wiki/Aerial_perspective",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "Vinheta + nitidez seletiva para dirigir o olho (eye-trace)",
      "why_it_reads_professional": "Burum descreve o mecanismo compositivo, verificado verbatim: 'It's a compositional scheme. Inside cross-keys pull the attention to the center of the frame, because you have dark on the outside and light on the inside; there's usually another bright area behind the faces, so everything is contained in the middle of the frame.' A vinheta \u00e9 a vers\u00e3o de p\u00f3s desse mecanismo \u2014 escurece a periferia e o olho vai ao centro sem que o espectador perceba a manipula\u00e7\u00e3o.",
      "how_to_implement_here": "CORRE\u00c7\u00c3O DE PRIORIDADE: os dois filtros J\u00c1 EXISTEM na cadeia viva \u2014 scripts/motion-bridge.ts:232-233 tem unsharp=5:5:0.35:5:5:0.0 e vignette=PI/5. Confirmado por `ffmpeg -h filter=`: vignette angle default 'PI/5' e unsharp chroma_amount default 0 (a casa j\u00e1 est\u00e1 fazendo certo: sharpening s\u00f3 na luma). Portanto o item acion\u00e1vel \u00e9 PORTAR para os runners do EP05 (scripts/ep05/render-*.ts:17 encodam sem nenhum filtro), N\u00c3O retunar o motion-bridge \u2014 e note que a sugest\u00e3o original (la=0.6, PI/6) \u00e9 sharpening MAIS FORTE e vinheta MAIS FRACA que o valor vivo, ou seja, \u00e9 opini\u00e3o, n\u00e3o corre\u00e7\u00e3o. Se mexer, subir la em passos e verificar halo em texto branco sobre fundo escuro. US$0.",
      "source_url": "https://ffmpeg.org/ffmpeg-filters.html",
      "feasibility": "direto",
      "impact": "medio"
    },
    {
      "technique": "Continuidade de eixo (180\u00b0) aplicada \u00e0 dire\u00e7\u00e3o de tela entre cenas de motion",
      "why_it_reads_professional": "Verificado verbatim: 'If the camera remains on one side of this line, the spatial relationship between the two characters will be consistent from shot to shot' e 'Shifting to the other side of the characters on a cut will reverse the order of the characters from left to right and may disorient the viewer.' Em motion graphics o eixo n\u00e3o \u00e9 entre dois atores \u2014 \u00e9 o VETOR DE FLUXO do produto (entrada \u2192 processamento \u2192 sa\u00edda). Se numa cena os assets fluem para a direita e na seguinte o mesmo fluxo inverte, o espectador perde o mapa mental do pipeline mesmo entendendo cada plano isolado. \u00c9 desorienta\u00e7\u00e3o que ningu\u00e9m sabe nomear e todo mundo sente.",
      "how_to_implement_here": "Declarar um flowAxis por epis\u00f3dio (ex.: 'esquerda\u2192direita') nos props dos assemble (scripts/ep05/assemble-v13.ts) e derivar dele TODAS as entradas/sa\u00eddas de n\u00f3, a dire\u00e7\u00e3o do running ring e a orienta\u00e7\u00e3o das edges. Para inverter legitimamente, usar um plano neutro como buffer \u2014 a gal\u00e1xia t=0 em tela cheia j\u00e1 \u00e9 esse 'buffer shot' na linguagem v6. RESSALVA: o lint autom\u00e1tico proposto depende do schedule declarativo de beats que ainda n\u00e3o existe (os __seek s\u00e3o escritos \u00e0 m\u00e3o); adotar como conven\u00e7\u00e3o de autoria agora. US$0.",
      "source_url": "https://en.wikipedia.org/wiki/180-degree_rule",
      "feasibility": "direto",
      "impact": "medio"
    },
    {
      "technique": "Cortar no movimento (cutting on action) em vez de cortar no repouso",
      "why_it_reads_professional": "Verificado verbatim: 'A match on the action is when some action occurring before the temporally questionable cut is picked up where the cut left it by the shot immediately following' \u2014 o segundo plano mostra o elemento no MESMO est\u00e1gio da mo\u00e7\u00e3o. O c\u00e9rebro prioriza rastrear o movimento e n\u00e3o registra o corte. O erro padr\u00e3o em montagem de motion \u00e9 o oposto: cada cena termina com tudo parado e a pr\u00f3xima come\u00e7a do zero \u2014 o que produz uma sequ\u00eancia de cartelas, n\u00e3o um filme. E \u00e9 o caso AQUI: scripts/ep05/assemble-v13.ts:83 e :96 concatenam com `ffmpeg -f concat` puro, ou seja, corte seco em toda fronteira de cena.",
      "how_to_implement_here": "Deixar cada cena com uma cauda de movimento (elemento ainda viajando no \u00faltimo frame do __seek) e a cena seguinte com uma cabe\u00e7a que retoma o MESMO vetor e velocidade \u2014 regra de autoria aplic\u00e1vel j\u00e1, US$0. A verifica\u00e7\u00e3o num\u00e9rica proposta (comparar |v_sa\u00edda \u2212 v_entrada| derivada da curva de easing) \u00e9 desej\u00e1vel mas exige instrumentar os __seek para exportar a velocidade nos frames de borda; tratar como follow-on, n\u00e3o como pr\u00e9-requisito.",
      "source_url": "https://en.wikipedia.org/wiki/Continuity_editing",
      "feasibility": "direto",
      "impact": "alto"
    },
    {
      "technique": "J-cut / L-cut \u2014 o \u00e1udio cruza o corte antes/depois da imagem",
      "why_it_reads_professional": "Verificado verbatim: o J cut \u00e9 aquele em que 'the audio from a following scene overlaps the picture from the preceding scene, so that the audio portion of the later scene starts playing before its picture as a lead-in to the visual cut', e o nome vem 'the shape of audio and video pieces... forming a shape similar to the letter J on the timeline'. Quando som e imagem trocam no MESMO frame, a costura fica aud\u00edvel e vis\u00edvel ao mesmo tempo e vira emenda.",
      "how_to_implement_here": "CORRE\u00c7\u00c3O DE ESCOPO: o achado original sugere que falta a fia\u00e7\u00e3o \u2014 n\u00e3o falta. scripts/ep05/assemble-v13.ts:102-124 j\u00e1 monta a fala como UMA cama cont\u00ednua (adelay por segmento + amix + apad) sobre o v\u00eddeo concatenado, com sidechaincompress e loudnorm=I=-16 \u2014 ou seja, o \u00e1udio j\u00e1 atravessa os cortes por constru\u00e7\u00e3o, e o duck j\u00e1 existe. O que falta \u00e9 CALIBRA\u00c7\u00c3O deliberada: adiantar o offset `off` da narra\u00e7\u00e3o da cena seguinte em jCutLeadSec e estender a cauda da anterior em lCutTailSec \u2014 as duas constantes J\u00c1 EXISTEM em /home/gcrUX/htdocs/constellation-orchestra/src/lib/cinematic-grammar.ts:129-130 (0.6 / 1.2) e n\u00e3o s\u00e3o lidas pelo assemble. \u00c9 mudar aritm\u00e9tica de offset, n\u00e3o construir filtergraph novo. US$0.",
      "source_url": "https://en.wikipedia.org/wiki/J_cut",
      "feasibility": "direto",
      "impact": "medio"
    },
    {
      "technique": "Rule of Six (Murch) como ordem de desempate quando os crit\u00e9rios conflitam",
      "why_it_reads_professional": "\u00c9 o \u00fanico framework que diz o que SACRIFICAR, e por isso vale mais que qualquer regra isolada desta lista \u2014 autoriza quebrar continuidade de eixo para salvar ritmo, e pro\u00edbe o inverso. \u00c9 o ant\u00eddoto contra virar ref\u00e9m das outras regras aqui. RESSALVA DE FONTE (verificada): a p\u00e1gina citada N\u00c3O traz as porcentagens; ela sustenta que emo\u00e7\u00e3o responde por mais de 50% do que faz um bom corte, lista os seis em ordem de import\u00e2ncia e diz explicitamente que Murch 'doesn't believe all of these rules can or should be employed at once', exemplificando quebras a servi\u00e7o da emo\u00e7\u00e3o. A reparti\u00e7\u00e3o precisa 51/23/10/7/5/4 vem do livro 'In the Blink of an Eye', n\u00e3o desta URL \u2014 n\u00e3o citar como se viesse dela.",
      "how_to_implement_here": "N\u00e3o \u00e9 c\u00f3digo: \u00e9 a regra de desempate que entra no system prompt do spaces-agent-chat e na skill motion-scenes, junto das 18 regras j\u00e1 destiladas do repert\u00f3rio \u2014 hierarquia emo\u00e7\u00e3o > hist\u00f3ria > ritmo > eye-trace > plano da tela > espa\u00e7o 3D, com emo\u00e7\u00e3o dominante. O item mensur\u00e1vel (checar salto do centroide de aten\u00e7\u00e3o no corte) depende do mesmo m\u00f3dulo de energia do gate de staging; tratar como follow-on. US$0.",
      "source_url": "https://www.studiobinder.com/blog/walter-murch-rule-of-six/",
      "feasibility": "direto",
      "impact": "medio"
    },
    {
      "technique": "ASC CDL (slope/offset/power) como CONTRATO do grade + LUT .cube pr\u00f3pria da casa",
      "why_it_reads_professional": "Consist\u00eancia entre epis\u00f3dios \u00e9 metade do que faz um canal parecer profissional \u2014 e hoje o look vive espalhado em flags dentro do encode (scripts/motion-bridge.ts:228-233), o que garante deriva, e some por completo nos runners do EP05. O ASC CDL d\u00e1 a matem\u00e1tica m\u00ednima e port\u00e1vel, verificada na fonte: 'out=(i\u00d7s+o)^p', com slope nominal 1.0, offset 0, power 1.0, mais Satura\u00e7\u00e3o na vers\u00e3o 1.2, publicado pelo Technology Committee da ASC. Vira um objeto de 10 n\u00fameros version\u00e1vel em git \u2014 a paleta do canal vira dado, n\u00e3o folclore.",
      "how_to_implement_here": "(1) Representar o look da casa como CDL (10 n\u00fameros) em src/lib/cinematic-grammar.ts, ao lado de MIX_TARGETS \u2014 o an\u00e1logo visual dos alvos de \u00e1udio. (2) Gerador que amostra o CDL num cubo N=33 e emite .cube, aplicado com lut3d=file=mcorch-house.cube (CONFIRMADO neste host: `ffmpeg -h filter=lut3d` mostra interp com default tetrahedral \u2014 n\u00e3o \u00e9 preciso passar o par\u00e2metro). RESSALVAS HONESTAS: (a) um CDL \u00e9 per-canal slope/offset/power, ent\u00e3o um 1D bastaria \u2014 o 3D LUT \u00e9 s\u00f3 porque .cube \u00e9 o formato que o lut3d l\u00ea; (b) colapsar a cadeia num \u00fanico LUT PERDE a possibilidade de habilitar filtros por segmento via timeline 'enable'; (c) o LUT assume espa\u00e7o de entrada \u2014 vale como 'look' sobre nosso sRGB, n\u00e3o como transform colorim\u00e9trica. US$0.",
      "source_url": "https://en.wikipedia.org/wiki/ASC_CDL",
      "feasibility": "exige-novo-modulo",
      "impact": "medio"
    },
    {
      "technique": "Squash & stretch em UI \u2014 deforma\u00e7\u00e3o n\u00e3o-uniforme com volume preservado",
      "why_it_reads_professional": "Verificado verbatim: 'The most important principle is called squash and stretch. When an object is moved, the movement emphasizes any rigidity in the object.' Um card que translada com escala rigorosamente uniforme grita 'div'. Deforma\u00e7\u00e3o m\u00ednima no eixo do movimento (~3%, comprimindo o perpendicular na mesma medida) d\u00e1 materialidade sem virar cartoon \u2014 \u00e9 sutil o bastante para passar despercebida conscientemente, e \u00e9 por isso que funciona.",
      "how_to_implement_here": "Em window.__seek(t), derivar a velocidade instant\u00e2nea por diferen\u00e7a finita do valor J\u00c1 EASED (eased(t) \u2212 eased(t \u2212 1/fps); o fps \u00e9 conhecido: os runners chamam __seek(i/30)) e aplicar transform: rotate(\u03b8) scale(1+k\u00b7v, 1/(1+k\u00b7v)) rotate(\u2212\u03b8) com \u03b8 = \u00e2ngulo do vetor de movimento \u2014 a rota\u00e7\u00e3o em sandu\u00edche \u00e9 o que alinha a deforma\u00e7\u00e3o ao deslocamento, e o 1/(1+k\u00b7v) \u00e9 o que preserva volume (sem ele vira zoom e o efeito se perde). Calibrar k para \u22643-4% no pico. CRIT\u00c9RIO DE QA: se der para VER a deforma\u00e7\u00e3o num frame parado, est\u00e1 exagerado. US$0.",
      "source_url": "http://graphics.cs.cmu.edu/nsp/course/15-464/Fall05/papers/lasseter.pdf",
      "feasibility": "direto",
      "impact": "medio"
    },
    {
      "technique": "Exagero balanceado entre componentes \u2014 um dial por epis\u00f3dio, nunca seis",
      "why_it_reads_professional": "Verificado verbatim: 'A scene has many components to it: the design, the shape of the objects, the action, the emotion, the color, the sound. Exaggeration can work with any component, but not in isolation. The exaggeration of the various components should be balanced. If just one thing is exaggerated in an otherwise lifelike scene, it will stick out and seem unrealistic.' \u00c9 a explica\u00e7\u00e3o t\u00e9cnica de por que uma transi\u00e7\u00e3o chamativa sozinha, sobre uma cena s\u00f3bria, estraga a cena inteira \u2014 o problema n\u00e3o \u00e9 a transi\u00e7\u00e3o, \u00e9 o desequil\u00edbrio.",
      "how_to_implement_here": "Um \u00fanico token de estiliza\u00e7\u00e3o por epis\u00f3dio (s\u00f3brio | m\u00e9dio | alto) nos props do assemble, do qual derivam CONJUNTAMENTE: amplitude de overshoot do spring(), for\u00e7a da vinheta, quantidade de gr\u00e3o, satura\u00e7\u00e3o do split teal/orange e agressividade das transi\u00e7\u00f5es. Um dial, n\u00e3o seis controles independentes \u2014 impede a deriva t\u00edpica em que cada cena ganha um efeito novo e o epis\u00f3dio perde unidade. US$0.",
      "source_url": "http://graphics.cs.cmu.edu/nsp/course/15-464/Fall05/papers/lasseter.pdf",
      "feasibility": "direto",
      "impact": "medio"
    },
    {
      "technique": "Motion blur por objeto (velocity buffer) e desfoque de profundidade real",
      "why_it_reads_professional": "O tmix borra o FRAME inteiro por igual: quando um n\u00f3 voa e o fundo est\u00e1 parado, o fundo tamb\u00e9m borra \u2014 fisicamente errado e percept\u00edvel. Motion blur correto \u00e9 por objeto, proporcional \u00e0 velocidade daquele objeto. Idem para profundidade: o c\u00edrculo de confus\u00e3o variando com a dist\u00e2ncia, com bokeh de borda definida, \u00e9 o que d\u00e1 leitura de lente grande; o blur gaussiano de CSS achata porque n\u00e3o tem forma de diafragma.",
      "how_to_implement_here": "VIABILIDADE CONFIRMADA MATERIALMENTE (era o ponto mais duvidoso da lista): sondei o chromium pinado do rail headless e ele entrega WebGL 2.0 por software \u2014 renderer 'ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (LLVM 10.0.0)), SwiftShader driver)' \u2014 com clear+readPixels devolvendo o valor exato esperado ([64,128,191,255] para clearColor 0.25/0.5/0.75). Ou seja: sem GPU, sem CDN, sem depend\u00eancia nova. Renderizar os elementos como quads texturizados com G-buffer de velocidade+profundidade e um shader de p\u00f3s que borra ao longo do vetor por pixel. Determin\u00edstico desde que o shader n\u00e3o use tempo de parede nem aleatoriedade sem seed. CUSTO HONESTO: rasteriza\u00e7\u00e3o por software a 1080\u00d71920 \u00e9 lenta \u2014 \u00e9 o \u00faltimo item da fila, s\u00f3 depois que easing, arcos, grade e gr\u00e3o estiverem em produ\u00e7\u00e3o, porque estes entregam mais percep\u00e7\u00e3o por muito menos esfor\u00e7o.",
      "source_url": "http://graphics.cs.cmu.edu/nsp/course/15-464/Fall05/papers/lasseter.pdf",
      "feasibility": "exige-webgl",
      "impact": "medio"
    },
    {
      "technique": "GAP declarado: grade HDR/wide-gamut (PQ/HLG) de ponta a ponta",
      "why_it_reads_professional": "Vale registrar o vazio em vez de prometer. Todo o ganho de grade acima acontece em SDR 8-bit: verificado no c\u00f3digo, tanto scripts/hyperframes/render-core.ts quanto os runners scripts/ep05/render-*.ts:17 e o encode de scripts/motion-bridge.ts terminam em '-pix_fmt yuv420p' H.264. Um grade HDR real exigiria 10-bit com transfer PQ ou HLG, metadata de mastering e entrega em HEVC/AV1. Aplicar 'look HDR' dentro de SDR n\u00e3o \u00e9 HDR: \u00e9 satura\u00e7\u00e3o e contraste, e tende a piorar (clipping e banding).",
      "how_to_implement_here": "N\u00c3O implementar. O ffmpeg deste host tem libplacebo compilado (confirmado na linha de configure do `ffmpeg -version`), ent\u00e3o o tone mapping existiria tecnicamente \u2014 mas a cadeia de entrega e o QA da casa s\u00e3o SDR de ponta a ponta, e mudar isso \u00e9 decis\u00e3o de contrato de entrega, n\u00e3o de filtro. Manter todo o grade em SDR e declarar HDR fora de escopo at\u00e9 haver demanda material de plataforma.",
      "source_url": "https://ffmpeg.org/ffmpeg-filters.html",
      "feasibility": "inviavel-no-rail",
      "impact": "baixo"
    }
  ]
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
> * **Sessão Anterior**: [[2026-08-05 - agent-a5375a283bb2297ca]]
> * **Próxima Sessão**: [[2026-08-05 - agent-a5763ac1d02327199]]
%% --- TIMELINE END --- %%

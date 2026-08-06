# SOP — A Trupe Criativa do Spaces (Dramaturgo · Encenador · Diretor de Fotografia)

> **Lei 2 (Processo Antecipado).** Como três especialistas criativos produzem **uma** cena motion
> executável, sob o maestro (`spaces-agent-chat`), sem que nenhum deles escreva letra morta.
> **Lei 1 (Materialidade)** governa o veredito: uma partitura só está pronta quando um **frame
> renderizado** prova que ela foi **encenada**, não apenas escrita.
>
> **Agentes irmãos:** `.claude/agents/dramaturgo.md` · `.claude/agents/encenador.md` ·
> `.claude/agents/diretor-fotografia.md` (skills homônimas em `.claude/skills/`).
> **Perícia que originou tudo:** `.claude/context/motion-engine-forensics-2026-08-05.md`.
> **Motor:** `scripts/motion/scene-template.ts` · `scripts/motion-bridge.ts` ·
> `supabase/functions/motion-render/index.ts`.

**ORO desta disciplina:**
- **Operator** — a trupe (3 subagentes L2 sob `artisan`), orquestrada pelo `creative-director` ou
  pelo maestro do Spaces.
- **Reviewer** — Sovereign, por **parecer ocular sobre frames**, nunca sobre texto de partitura.
- **Owner** — Sovereign (marca, canal, e o tempo de máquina que o render consome).

---

## 0. O defeito que criou a trupe (e a armadilha que a trupe pode recriar)

A perícia de 2026-08-05, com frames do EP06 na mesa, tem um veredito de uma frase:

> **O motor imprime o roteiro em vez de encená-lo.**

Um campo `description` servia a dois senhores: era **nota de direção** ("um pacote 3D cristaliza com
focus pull") e era **despejado na tela** como legenda truncada em 240 caracteres, no meio da palavra,
enquanto o narrador lia outro texto. E metade do vocabulário que a direção pedia **não existia no
motor e sumia sem erro**.

**A armadilha que este documento existe para fechar:** se a trupe entregar **prosa bonita**,
recriamos o bug com três agentes a mais e três custos a mais. Prosa que o motor não sabe executar
**não é direção — é decoração que some sem erro**.

Por isso a trupe escreve **PARTITURA ESTRUTURADA com vocabulário FECHADO** (§2), e cada token ou é
executado hoje, ou vem com **Pedido de Vocabulário aberto + fallback declarado** (§6).

---

## 1. Operator

| Papel | Quem | Ferramentas |
|---|---|---|
| **Dramaturgo** | subagente `dramaturgo` | `Read`, `Grep`, `Bash` (ffprobe/whisper para medir a narração) |
| **Encenador** | subagente `encenador` | `Read`, `Grep`, `Bash` (ffmpeg para medir ocupação de zona) |
| **Diretor de Fotografia** | subagente `diretor-fotografia` | `Read`, `Grep`, `Bash` (bench ms/frame, ffprobe) |
| **Maestro** | `spaces-agent-chat` (edge fn) OU o MCORCH Master Agent | `create_node` / `update_node` / `connect_nodes` |
| **Produção** | `creative-director` (skill `motion-scenes`) | render, mix, Biblioteca, QA A/V |
| **Engenharia** | `engineer-spaces` | atende Pedidos de Vocabulário; **único** que toca o motor |

**Regra de convocação:** a trupe **nunca** é convocada para uma cena sem narração medida. Sem
`ffprobe` na fala, não há relógio, e sem relógio a partitura é ficção (Gate G3).

---

## 2. A cadeia — o que atravessa cada seta, e o que volta

```
  pauta/narração (mp3 + texto)
        │  ffprobe → D (segundos)          ← Produção mede. Ninguém estima.
        ▼
  ┌─────────────┐   PARTITURA-TEATRO
  │ DRAMATURGO  │   { intent, stakes, beats[{anchorWord, action, onScreen, turn}] }
  └─────────────┘
        │  ▲ devolve: "beat sem turn" · "onScreen > 6 palavras" · "anchorWord fora da narração"
        ▼  │
  ┌─────────────┐   + PARTITURA-ESPAÇO
  │ ENCENADOR   │   staging{ grid, planes{fg,mid,bg}, focal[], entrances, exits, negativeSpace }
  └─────────────┘
        │  ▲ devolve: "dois focais no mesmo beat" · "n cards estouram a geometria" · "vazio sem intenção"
        ▼  │
  ┌─────────────┐   + PARTITURA-CINEMA
  │ DoP         │   camera[{atBeat,move,ease}] · light{key,fill,rim,motivation} · lens{focusPull,dof}
  │             │   transitions{in,out} · grade · RELÓGIO (n) · ORÇAMENTO (ms/frame)
  └─────────────┘
        │  ▲ devolve: "efeito sem preço medido" · "luz sem motivação" · "beat cai 20 frames fora da palavra"
        ▼  │
  ┌─────────────┐   COMPILAÇÃO (§3.3) — só 6 coisas sobrevivem até o nó
  │ MAESTRO     │   title · description · beats[].word · beats[].event · elements[] · background
  └─────────────┘   (+ data_patch.series quando há comparação · durationSec vem da voz)
        │  ▲ devolve: "verbo fora do VOCAB" · "elemento que o motor não lê" · "sem Pedido aberto"
        ▼  │
  ┌─────────────┐   render → frames → GATE DE HONESTIDADE (§5) → mix → Biblioteca
  │ PRODUÇÃO    │
  └─────────────┘
        │  ▲ devolve: "o frame do beat 3 não mostra o que a partitura prometeu"
        ▼
     Sovereign (parecer ocular por peça)
```

### 2.1 Os objetos exatos (contrato de passagem)

**Dramaturgo → Encenador** — objeto `teatro`:

```json
{
  "id": "ep06-c04-kimi-bench",
  "durationSec": 14.4,
  "aspect": "16:9",
  "intent": "fazer o espectador sentir que um modelo aberto encostou no fechado",
  "stakes": "se ele não vir a diferença, o episódio vira fofoca de benchmark",
  "beats": [
    { "anchorWord": "benchmark", "action": "nasce",   "onScreen": "SWE Marathon", "turn": "revela" },
    { "anchorWord": "76,8",      "action": "compara", "onScreen": "K3 76,8%",     "turn": "escala" },
    { "anchorWord": "sistema",   "action": "carimba", "onScreen": "",             "turn": "contraria" }
  ]
}
```

**Encenador → DoP** — acrescenta `staging`. **Contrato:** cada `focal` é a promessa de que existe
**UM** alvo para a lente naquele beat. Dois focais no mesmo beat = o DoP não tem onde pousar o foco,
e o defeito sai no master, não no texto.

**DoP → Maestro** — acrescenta `camera`/`light`/`lens`/`transitions`/`grade`, **e mais duas coisas
que só ele produz**: o **relógio** (`n`, o número de beats, com a conta colada) e o **orçamento**
(ms/frame medido). Sem esses dois, o maestro recusa.

### 2.2 O direito de rejeição (quem pode devolver o quê)

| Quem devolve | Para quem | Motivo válido | Motivo INVÁLIDO |
|---|---|---|---|
| Encenador | Dramaturgo | `onScreen` > 6 palavras; beat sem `turn`; `anchorWord` ausente da narração real | "não gostei do texto" — ele **não reescreve** o beat |
| DoP | Dramaturgo | beat cuja âncora medida cai >15 frames (0,5 s) fora do instante que a grade uniforme produz | "queria outro ritmo" sem a conta de `n` colada |
| DoP | Encenador | dois focais no mesmo beat; `fg` pedido sem Pedido aberto | preferência de composição |
| Maestro | qualquer lente | token fora do VOCAB v1 sem Pedido + fallback | "prefiro outro verbo" |
| Produção | qualquer lente | o frame do beat não mostra o que a partitura prometeu (§5) | impressão sem frame colado |
| **Qualquer um** | **todos** | a cena não tem `stakes`, ou não tem virada | — |

**Empate vai para o Dramaturgo:** manda a `intent`. Tempo e espaço servem ao sentido.

---

## 3. O VOCABULÁRIO FECHADO v1

> **Estado material verificado em 2026-08-05**, HEAD `e0fef7f` **+ working tree** (há mudanças não
> commitadas em `scene-template.ts`, `motion-bridge.ts`, `motion-render/index.ts`,
> `useCanvasPipeline.ts`). **O motor é alvo móvel:** mudou **três vezes** no dia em que esta doutrina
> foi escrita (`f731080` selos · `852dc08` a tela cala + anel · `e0fef7f` barras com dado declarado).
>
> **Nenhum documento — nem este — é fonte de verdade sobre o estado do motor.** Antes de assinar uma
> partitura, rode o §3.6.

**Legenda:** ✅ executa · ⚠️ executa **sob condição** (a condição é load-bearing) · ⛔ **não executa
— é pedido de obra para o `engineer-spaces`** (§6).

### 3.1 `action` — o verbo do Dramaturgo (VOCAB-ACT v1)

Cada `action` é um **verbo de mudança** amarrado a um mecanismo que o motor executa de fato.

| `action` | O que MUDA no quadro | Elemento | Estado |
|---|---|---|---|
| `nasce` | card glass vem do fundo: `z −190→0`, `blur 7→0`, `scale .94→1` em **25,5 frames** | `nodes` | ✅ |
| `conecta` | bezier liga o card ao **anterior**, endpoints recalculados por frame | `edges` | ⚠️ exige ≥2 cards vivos; liga só **consecutivos** (i → i+1) |
| `conta` | contador sobe até o número **ancorado no texto** e trava | `counter` | ⚠️ o número precisa existir no texto da cena (§3.7) |
| `acende` | disco de ícone 3D entra no beat (`rotateY ±9°`) | `contextIcons` | ⚠️ até 3; **eleitos por keyword**, você não escolhe qual (§3.7) |
| `ergue` | ícone-herói grande assume o palco (`rotateY ±11°`) | `heroIcon` | ⚠️ **força a grade em coluna** — avise o Encenador |
| `impacta` | onda de choque de **21 frames** no instante do beat | `shockwave` | ⚠️ sempre no **centro geométrico**; não é posicionável |
| `carimba` | selo entra com **spring** (overshoot) e **PERMANECE** | `badges` | ⚠️ exige gatilho + aspas (§3.7) |
| `percorre` | anel corre o **perímetro** do herói e fecha em emerald | `runningRing` | ⚠️ **só com `heroIcon` junto** (§3.7) |
| `compara` | barras com draw-in escalonado, rótulo e valor legíveis | `chart` + `series` | ⚠️ o motor desenha; **a autoria não existe na UI** (§3.7) |
| `respira` | **nada entra** — o quadro sustenta o que já está | (ausência) | ✅ |

**⛔ Verbos que a trupe quer e o motor não executa — o pedido de obra:**

| `action` desejado | Elemento | Prova material | Pedido |
|---|---|---|---|
| `digita` (prompt datilografado) | `typewriter` | **0 ocorrências** no motor; oferecido em `MotionElement:1061` | VOC-DRA-002 |
| `exibe` (thumb real do projeto) | `assets` | **0 ocorrências**; oferecido em `MotionElement:1062` | VOC-DRA-003 |
| `corta` (flash-bloom de saída) | `#bloom` | existe (`:578-582`) mas dispara no **nascimento de card**, nunca no fim da cena | VOC-DOP-004 |
| `traça` (curva de tendência) | — | **removido de propósito** em `e0fef7f`: a curva antiga era exponencial fixa, sem relação com o dado. **Não readmitir** — comparação sem dado declarado é mentira gráfica | — |

> **Regra do número:** se o número importa, ele vai para `conta` ou para `onScreen`. **Nunca** confie
> num gráfico como único portador de um dado.

### 3.2 `turn` — a virada (Dramaturgo)

| Token | Significado |
|---|---|
| `revela` | mostra o que ainda não se sabia |
| `contraria` | vira a expectativa que o beat anterior criou |
| `escala` | sobe a aposta na mesma direção |
| `resolve` | fecha o loop que a cena abriu |

> ⚠️ **`turn` NÃO COMPILA para campo nenhum do nó.** É um **gate editorial**: cena sem nenhuma
> virada é ilustração, não drama (Gate G2). Ele existe para ser cobrado, não renderizado.

### 3.3 `grid` · `planes` · `focal` · `entrances` · `exits` (Encenador)

| Campo | Tokens | Estado |
|---|---|---|
| `grid` | `centro` · `tercos` · `diagonal` | ⛔ **não honrado** — `layout = seed % 3` (`scene-template.ts:208`), derivado do hash de título+descrição. **VOC-STG-001** |
| `planes.bg` | `galaxia` · `grid64` · `particulas` · `keylight` | ✅ (parallax real: o fundo translada **menos** que os cards) |
| `planes.mid` | `card` · `iconDisc` · `hero` · `chart` · `counter` · `titulo` · `legenda` · `shockwave` | ✅ (mas tudo no mesmo Z depois de nascer) |
| `planes.fg` | — | ⛔ **não existe plano de frente dramático**. Vinheta/grão/aberração são **compositor**, não encenação. **VOC-STG-002** |
| `focal[]` | `[{ atBeat, who }]` — **um `who` por beat, sempre** | ⚠️ declarativo: o motor dá ênfase de **nascimento**, mas **não rebaixa os demais**. **VOC-STG-003** |
| `entrances` | `nasce-em-profundidade` · `ja-em-cena` | ✅ |
| | `entra-esquerda` · `entra-direita` · `entra-baixo` · `entra-topo` · `desdobra-do-irmao` | ⛔ **VOC-STG-004** |
| `exits` | `permanece` (**declaração obrigatória**, nunca default silencioso) | ✅ |
| | `recua-em-profundidade` · `sai-esquerda` · `sai-direita` · `dissolve` | ⛔ **VOC-STG-004** |
| `negativeSpace` | `{ zones: ["z11".."z33"], why, resolvedAtBeat }` | ✅ como declaração (grade 3×3, 1-indexada do topo-esquerda). `why` genérico = vazio esquecido → Gate G4 |

> **A única alavanca honesta de grade hoje:** `heroIcon` presente ⇒ coluna lateral **garantida**
> (`if(hasHero || L===1)`, `:400`), independente do seed. Mudar o título para "re-sortear" o layout
> é **efeito colateral**, não controle — e qualquer ajuste de copy re-sorteia tudo de novo.

### 3.4 `camera` · `light` · `lens` · `transitions` · `grade` (DoP)

| Campo | Tokens | Estado |
|---|---|---|
| `camera[].move` | `hold` | ✅ — **é o estado nativo** (locked-off) |
| | `push` · `pull` · `whip` | ⛔ **não há câmera** no motor. **VOC-DOP-001** |
| `camera[].ease` | `outCubic` (`1-(1-x)³`) · `spring` (`1-e^(-6x)·cos(9x)`) | ✅ — as duas curvas seladas da v6 |
| | `linear` · `inOutSine` | ⛔ |
| `light.key` | `galaxia-ambiente` · `estudio-lateral-quente` (âmbar a **112°**) · `limpo-sem-key` | ✅ — **é o campo `background`, o único controle de luz** |
| | `chiaroscuro` · `contraluz` · `top-light` · `underlight` | ⛔ **VOC-DOP-002** |
| `light.fill` / `light.rim` | — | ⛔ **não existem como aparato**. O que existe é **emissão pelo objeto** (glow/box-shadow) — emissão não modela volume, e é por isso que o quadro lê chapado |
| `light.motivation` | texto livre **OBRIGATÓRIO** | ✅ como gate (G5): tem que nomear uma fonte **dentro da ficção da cena** |
| `lens.focusPull` | `true` | ✅ — automático em **todo** card, 25,5 frames |
| | `false` | ⛔ — não há como desligar |
| `lens.dof` | `profundo` | ✅ — é o estado atual |
| | `raso` | ⛔ **VOC-STG-003** (mesma capacidade do rebaixamento focal — **um pedido só, duas assinaturas**) |
| `transitions.in` | `ja-em-cena` (galáxia viva desde t=0 — regra selada) · `bloom-nascimento` (13,5 frames) | ✅ |
| | `preto-para-luz` | ⛔ **VOC-DOP-004** |
| `transitions.out` | `corte-seco` | ✅ — **e é o único**: o montador usa `concat` puro |
| | `flash-bloom` | ⚠️ o `#bloom` existe, mas só dispara em nascimento de card |
| | `dissolve` · `dip-to-black` | ⛔ **VOC-DOP-004** |
| `grade` | `teal-orange` | ✅ — **e é o único**; cadeia fixa em `motion-bridge.ts:228-234` |
| | `frio` · `quente` | ⛔ **VOC-DOP-005** |

> ⚠️ **`grade` é GLOBAL.** A cadeia roda em toda cena motion de todo episódio. Mexer nela depois de
> cenas renderizadas **quebra a continuidade de cor do master**, e se o episódio passou por **Picture
> Lock** invalida mixagem e legendagem em cascata. Proposta de mudança = **GO explícito do Sovereign
> + plano de re-render**, nunca ajuste no meio da produção.

### 3.5 As condições load-bearing (leia antes de assinar qualquer partitura)

Estas cinco condições são a diferença entre um verbo que encena e um verbo que some sem erro.

1. **`carimba` (badges)** — o selo só nasce se o `beats[].event` **casar** `/badge|selo|carimb/i`
   **E** trouxer o texto **entre aspas**. Sem aspas não há selo — inventar o texto seria pôr na tela
   uma palavra que ninguém escreveu (Lei 1). Tom **âmbar** (ressalva) se o `event` disser
   `ressalva|alerta|cuidado|âmbar`; senão ciano.
   → Escrita correta: `badge '1M DE CONTEXTO' acende ao lado`.

2. **`percorre` (runningRing)** — `if(heroEl && …runningRing)` (`:478`). **O anel exige `heroIcon`.**
   E o herói só nasce se alguma keyword da `ICON_LIBRARY` (`:67-89`) casar com o texto da cena.
   ⚠️ **`MOTION_DEFAULT_ELEMENTS` (`src/types/canvas.ts:1180`) = `["nodes","runningRing","edges",
   "contextIcons","shockwave"]` — pede anel SEM herói. No nó default, o anel NUNCA desenha.**
   → Pedir `percorre` obriga a pedir `ergue` junto, **e avisar o Encenador** (o herói re-arquiteta o
   quadro para coluna lateral).

3. **`compara` (chart + series)** — o motor desenha barras reais, mas a **autoria não existe**:
   `series` **não está** em `MotionSceneData` (`:1069-1093`), **não** é criado por
   `makeDefaultMotionScene` (`:1657`), **não** é editável no `MotionSceneInspector`, e por isso
   **não aparece no catálogo do agente** (`buildAgentCatalog` deriva os campos da *factory*).
   Pior: **o botão "Renderizar" do inspector não envia `series`** (`MotionSceneInspector.tsx:68-81`)
   enquanto o Run All envia (`useCanvasPipeline.ts:43`) — **dois caminhos, um perde o dado**.
   → Hoje `compara` só chega à tela por `data_patch: { series: [...] }` **e** execução pelo Run All.
   Declare isso na partitura. **VOC-STG-005** (fiação) + **VOC-STG-005b** (paridade dos dois botões).

4. **`conta` (counter)** — o número é **extraído do texto** (`title + description + beats` unidos por
   `" | "`), não declarado. Regra: número **com** unidade de escala vence número solto; número solto
   só entra se **≥ 100** (senão "K3", "v2", "GPT-5" viram contador e mentem na tela).
   → A trupe não escolhe o número: ela escolhe **escrever o número certo no texto**.
   Anticorpo vivo: `src/test/motion-scene-number.test.ts` reprova qualquer valor ≥ 1e15.

5. **`acende`/`ergue` (ícones)** — o ícone é eleito por **keyword pt-BR** da `ICON_LIBRARY`, na ordem
   de aparição no texto. **A trupe não escolhe o ícone — escolhe a PALAVRA.** Sem casamento,
   `hero = null` e o layout volta ao sorteio do seed.

### 3.6 Re-verificação obrigatória (o motor é alvo móvel)

Antes de assinar qualquer partitura:

```bash
cd /home/gcrUX/htdocs/constellation-orchestra
git log --oneline -6 -- scripts/motion scripts/motion-bridge.ts supabase/functions/motion-render
git status --porcelain -- scripts/motion scripts/motion-bridge.ts src/types/canvas.ts   # working tree ≠ HEAD?
grep -nE "indexOf\('|has\(\"" scripts/motion/scene-template.ts    # elements REALMENTE lidos
grep -n "MOTION_DEFAULT_ELEMENTS" -A1 src/types/canvas.ts         # o default ainda pede anel sem herói?
grep -n "series" src/types/canvas.ts src/components/canvas/RightPanel/inspectors/MotionSceneInspector.tsx
```

**Anticorpo da casa (perícia §Armadilha):** se um `grep` recursivo devolver **zero** num arquivo que
você tem razão para achar que casa, rode `file` nele **antes de acreditar no zero** — um byte NUL faz
o `grep` pular o arquivo **em silêncio**, e uma auditoria inteira conclui que a capacidade não existe.
Foi exatamente assim que o fundo `estudio` quase foi declarado inexistente.

### 3.7 Sanidade do vocabulário — o que qualquer lente pode recusar de imediato

- Token que não está nas tabelas §3.1-§3.4 → **RECUSA**, não improviso.
- Token ⛔ sem **Pedido aberto + fallback declarado** → **RECUSA**.
- `elements[]` com `typewriter` ou `assets` → **RECUSA**: o elemento some sem erro.
- `runningRing` sem `heroIcon` → **RECUSA**: nasce morto.
- `chart` ligado sem `series` → **RECUSA**: hoje isso **muda o layout** (sobe o contador para
  `0,5·H` e a legenda para o topo) **e não desenha gráfico nenhum**.

---

## 4. Como o maestro convoca a trupe

### 4.1 Quando chamar cada lente

| Situação | Lente | Por quê |
|---|---|---|
| "faça um motion do que a narração fala" | **as três, em ordem** | é a cadeia inteira (§2) |
| "essa cena não diz nada / ficou ilustrativa" | **Dramaturgo** | falta `intent`/`stakes`/virada |
| "o que aparece escrito na tela?" | **Dramaturgo** | `onScreen` é dele, e é ≤6 palavras ou vazio |
| "onde eu ponho isso / o quadro está vazio / não sei o que olhar" | **Encenador** | é espaço e hierarquia focal |
| "tudo no mesmo plano / dois elementos brigando" | **Encenador** | planos e foco |
| "está chapado / de onde vem a luz / como entra e sai" | **DoP** | luz, lente, transição |
| "o evento não cai na palavra" · "isso ficou caro de renderizar" | **DoP** | relógio (`n`) e orçamento (ms/frame) |
| "quero um verbo que não existe" | **qualquer uma → `engineer-spaces`** | Pedido de Vocabulário (§6) |
| "já pode publicar?" | **Produção + Sovereign** | Gate de honestidade (§5) |

**Convocação mínima aceitável:** para **uma** cena isolada, o maestro pode consolidar Encenador e DoP
numa passada só — **jamais** dispensar o Dramaturgo. Cena sem `intent`/`stakes` é arranjo arbitrário:
bonito e vazio (Gate G2).

### 4.2 Como as três respostas viram os campos do nó (a COMPILAÇÃO)

Esta é a tabela mais importante do documento. **Tudo que não estiver aqui não chega à tela.**

| Campo da Partitura | Campo do nó `motionScene` | Observação |
|---|---|---|
| `beats[].anchorWord` | `beats[i].word` | **vai à tela** como rótulo do card (`.lab`) |
| `beats[].action` + `beats[].onScreen` | `beats[i].event` | **vai à tela** como corpo do card (`.body`) — e é de onde saem os **selos** (texto entre aspas) |
| conjunto dos `action` | `elements[]` | só os tokens que o motor lê (§3.1) |
| `light.key` | `background` | `galaxia` · `limpo` · `estudio` |
| (título editorial) | `title` | **vai à tela**, topo, entra em 21 frames |
| (frase de sustentação) | `description` | **só vai à tela se NÃO houver narração**. Mesmo calada, alimenta seed, ícones, contador e layout |
| dados de `compara` | `data_patch.series` | canal existe; catálogo não anuncia (§3.5-3) |
| `aspect` | `aspect` | `16:9` (1280×720 CSS, rasterizado 1,5× ⇒ 1920×1080) · `9:16` |
| `durationSec` | `durationSec` | **sobrescrito pela narração** quando há voz conectada |
| `intent` · `stakes` · `turn` · `staging.*` · `camera` · `lens` · `light.motivation` · `transitions` · `grade` | **nenhum** | **NÃO COMPILAM.** São a **memória da decisão** (§4.4) |

> ⛔ **REGRA DE OURO — NINGUÉM ESCREVE NOTA DE DIREÇÃO NUM CAMPO DE TEXTO DO NÓ.**
> `title`, `description`, `word` e `event` **são impressos na tela**. Uma nota de direção dentro de
> `event` vira legenda no documentário — que é o **defeito #2 da perícia, agora com a sua
> assinatura**. A partitura **documenta** a decisão; o que ela **compila** é a lista acima.

### 4.3 O relógio (é aritmética, não gosto)

O motor distribui os beats **uniformemente**:

```
t_i = ((i + 0,6) / (n + 0,6)) · D          (scene-template.ts:218)
```

- `D` vem da narração: `D = ceil(dur_voz × 10)/10`, clamp 2..120 s (`motion-bridge.ts:173-185`).
- `n` (número de beats) é o **único** parâmetro de tempo. Para pousar o beat `i` na âncora medida `T`:
  `n = ((i + 0,6)·D / T) − 0,6`.
- **Limiar de percepção:** até ~3 frames (0,1 s) é imperceptível · 3-10 frames é aceitável se o gesto
  for suave (o nascimento tem 25 frames de rampa e mascara desvio) · **acima de ~15 frames (0,5 s) o
  espectador sente** que a imagem está atrasada em relação à palavra.
- **`n` é compartilhado:** com `nodes` ligado, **cada beat vira um card** — mexer em `n` mexe na
  composição do Encenador, e o veto dele vence.
- **Escape hatch verificado:** os `beatTimes` vêm das *cues*, não dos cards (`:436`). Se a cena
  **não usa `nodes`**, aumentar `n` afina o relógio **sem custar espaço nenhum** (os beats passam a
  reger só ícones, shockwaves, selos e o anel).
- **Cole a conta na partitura.** Sem ela, Gate G3 recusa.

### 4.4 Onde a partitura mora (enquanto o nó não a carrega)

Hoje o nó **não tem campo** para a partitura. Guardá-la só no chat é perdê-la no primeiro `/handoff`.

**Regra:** `.claude/context/partituras/<projeto>/<cena-id>.partitura.json`, com o path citado no
Record do HANDOFF (doutrina `scratchpad-harvest`). É a **memória da decisão** — o que responde
"por que esta cena é assim?" seis semanas depois.

**Pedido aberto:** **VOC-DRA-001** — campo `score` (jsonb) em `MotionSceneData`, para a partitura
viajar **com** o nó e o gate de honestidade poder ser mecânico (§5.4).

### 4.5 O que injetar no maestro (ESPECIFICAÇÃO — não implementar aqui)

O `spaces-agent-chat` hoje **não sabe nada** sobre a Cena Motion: `SYSTEM_PROMPT`
(`supabase/functions/spaces-agent-chat/index.ts:31-98`) não menciona `motionScene`, beats ou
elements; e `FIELD_HINTS` (`src/lib/spaces-agent-actions.ts:24-32`) **não tem entrada** para
`motionScene` — o modelo só vê os nomes dos campos derivados da factory.

Consequência material: o maestro escreve beats sem gatilho de selo, liga `runningRing` sem herói
(é o **default** do nó) e nunca autoria `series`. **Ele reproduz o defeito por ignorância, não por
descuido.**

**Injeção 1 — `src/lib/spaces-agent-actions.ts`, dentro de `FIELD_HINTS`:**

```ts
  motionScene:
    "description = NOTA DE DIREÇÃO (só vai à tela se NÃO houver narração conectada) · " +
    "beats[i].word = a palavra EXATA da narração que dispara o beat · " +
    "beats[i].event = o que acontece na tela (aparece no card) · " +
    "elements: nodes|edges|counter|chart|contextIcons|heroIcon|shockwave|badges|runningRing " +
    "(typewriter e assets NÃO existem no motor — não use) · " +
    "runningRing SÓ funciona junto com heroIcon · " +
    "badge = escreva no event a palavra 'badge' + o texto ENTRE ASPAS · " +
    "chart exige data_patch.series:[{label,value,unit,highlight}] · " +
    "background: galaxia|limpo|estudio · aspect: 16:9|9:16 · " +
    "durationSec é sobrescrito pela narração conectada",
```

**Injeção 2 — `SYSTEM_PROMPT` do `spaces-agent-chat`, bloco novo após "REPERTÓRIO PROFISSIONAL":**

```
A CENA MOTION TEM TRÊS CANAIS SEPARADOS (nunca misture)
Direção (o que deve acontecer) · Texto de tela (o signo, 2 a 6 palavras) · Narração (só áudio).
Com narração conectada a TELA CALA — o narrador carrega o sentido e legendar por cima rouba a
imagem. Nunca escreva nota de direção dentro de um campo que vai à tela: title, description,
beats[].word e beats[].event SÃO IMPRESSOS.

VERBOS QUE O MOTOR ENCENA (use só estes)
nasce (card) · conecta (aresta, precisa de 2+ cards) · conta (contador — o número tem que estar
ESCRITO no texto da cena) · acende (ícone, eleito por palavra-chave) · ergue (ícone herói, força
coluna lateral) · impacta (shockwave no centro) · carimba (selo: escreva "badge" e o texto ENTRE
ASPAS no event) · percorre (anel — SÓ com heroIcon junto) · compara (barras — exige
data_patch.series) · respira (nada entra; o quadro sustenta).
NÃO EXISTEM: typewriter, assets, e nenhuma câmera (push/pull/whip). Pedir isso é pedir um nó que
nasce morto — o elemento some sem erro nenhum.

COMO ESCREVER OS BEATS
Um beat = uma palavra da narração + um verbo acima. Cada beat vira um card quando 'nodes' está
ligado — 5 beats são 5 cards, e 5 cards não cabem no quadro. Diga o custo (0 mco) e o que a cena
FAZ com quem assiste, não o que ela ilustra.
```

> **Restrição de orçamento:** `MAX_CONTEXT` é 16k e o catálogo é fatiado em 6k
> (`spaces-agent-actions.ts:92`). A Injeção 2 tem ~1,4k caracteres — cabe. Injeção maior que isso
> exige medir o prompt final antes de subir (Lei 1).

**Gate:** as duas injeções são mudança de comportamento de produto — passam por `engineer-spaces`
(o maestro é edge function + lib da UI, **não** território da trupe), com witness do agente montando
uma cena e o Gate de Honestidade (§5) rodando sobre o resultado.

---

## 5. Verification gates — o GATE DE HONESTIDADE (Lei 1 aplicada à trupe)

> **A pergunta que este gate responde:** a partitura foi **ENCENADA** ou apenas **ESCRITA**?
> A resposta é **um frame**, nunca uma frase.

### 5.1 Por que frame, e por que por beat

O motor é **determinístico** (`window.__seek(t)` puramente matemático, NFR-VS-016): o frame no
instante `t` é idêntico em qualquer máquina. Logo, **um frame no instante de cada beat** é prova
reproduzível — e é **de graça** (probe headless, sem render completo, sem mco).

Frame "do meio da cena" **não serve**: os defeitos da perícia (selo que não nasce, anel que não
desenha, gráfico vazio) são **eventos de beat**. Um frame genérico os esconde.

### 5.2 A prova por verbo — o que olhar em `frame(t_i)`

| `action` no beat `i` | O que **TEM** que estar visível em `t_i + 0,3 s` | Ausência significa |
|---|---|---|
| `nasce` | um card novo, nítido (blur já resolvido), com o `word` no rótulo ciano | `nodes` fora de `elements` |
| `conecta` | fio bezier entre o card novo e o anterior, com tracejado animado | menos de 2 cards vivos, ou `edges` ausente |
| `conta` | contador com o **número certo**, subindo | número não estava no texto, ou < 100 sem unidade |
| `acende` | disco de ícone novo, com o pictograma do assunto | nenhuma keyword da `ICON_LIBRARY` casou |
| `ergue` | ícone grande central + **cards migrados para coluna à esquerda** | keyword não casou ⇒ `hero=null` |
| `impacta` | anel de choque expandindo a partir do centro | `shockwave` fora de `elements` |
| `carimba` | pílula com o texto **exato entre aspas**, ciano (ou âmbar) | faltou aspas, ou faltou a palavra-gatilho |
| `percorre` | arco correndo o perímetro do herói (emerald ao completar) | **`heroIcon` ausente** — o caso do default |
| `compara` | barras com rótulo **e** valor legíveis, a destacada em ciano | `series` não trafegou (inspector vs Run All) |
| `respira` | **nada novo** — e o quadro **não** está morto (galáxia viva) | — |

### 5.3 O ritual (comandos exatos)

```bash
cd /home/gcrUX/htdocs/constellation-orchestra
# 1) Reproduza o HTML da cena com o MESMO builder do worker (zero divergência):
#    (um script de 15 linhas que importa buildSceneHtml e escreve /tmp/.../scene.html)
# 2) Probe por beat — NÃO existe ainda: crie na primeira execução e promova
#    para scripts/motion/probe-beats.mjs (doutrina scratchpad-harvest).
node scripts/motion/probe-beats.mjs /tmp/scene.html /tmp/probe 14.4 "2.1,5.4,8.7,12.0" 1280 720 1.5
```

`probe-beats.mjs` (espelho fiel de `render-frames.mjs`, que já resolve o Chromium do host):

```js
import { chromium } from "playwright";
import { existsSync } from "fs";
const [,, html, outDir, , tsArg, wArg, hArg, sArg] = process.argv;
const ts = tsArg.split(",").map(Number);
const CHROME = process.env.PLAYWRIGHT_CHROMIUM
  ?? "/home/ubuntu/.cache/ms-playwright/chromium-1226/chrome-linux/chrome";
const browser = await chromium.launch({ headless: true, ...(existsSync(CHROME) ? { executablePath: CHROME } : {}) });
const page = await (await browser.newContext({
  viewport: { width: Number(wArg) || 1280, height: Number(hArg) || 720 },
  deviceScaleFactor: Number(sArg) || 1.5,
})).newPage();
await page.goto(`file://${html}`, { waitUntil: "load", timeout: 30_000 });
await page.waitForFunction(() => window.__ready, null, { timeout: 15_000 });
for (const t of ts) {
  await page.evaluate((x) => window.__seek(x), t);
  await page.screenshot({ path: `${outDir}/beat_t${t}.png`, animations: "disabled" });
}
await browser.close();
```

> **Por que `deviceScaleFactor` e não viewport maior:** as posições da cena são px absolutos —
> aumentar o viewport **recomporia** o quadro. O `scale` mantém o layout em CSS px e só rasteriza em
> mais pixels (a correção do borrão de 2026-08-05).

**Depois do probe, os quatro gates ordenados:**

| Gate | O que prova | Como falha |
|---|---|---|
| **G-H1 — Encenação** | cada `action` produziu o sinal de §5.2 no seu frame | qualquer linha da tabela sem prova visual |
| **G-H2 — Ocupação** | zonas vazias ≤ **4/9 (44%) em 16:9** / **5/9 (55%) em 9:16**, ou `negativeSpace` completo | medição de zona (grade 3×3, densidade de borda, **auto-calibrada contra um frame só de fundo**) |
| **G-H3 — Sincronia** | cada evento cai **≤15 frames (0,5 s)** da sua palavra | `whisper.cpp` timestampado × `t_i` calculado |
| **G-H4 — Vision QA ocular** | o quadro lê como documentário, não como slide | parecer do `creative-director` sobre os probes, **antes** de qualquer render longo |

**Só depois dos quatro** vale render completo. Erro de composição que escapa aqui reaparece no
master — com a mixagem já pendurada na duração.

### 5.4 O que este gate ainda NÃO consegue provar (declarar o vazio, não prometer)

- **Não é mecânico.** Enquanto a partitura não viaja no nó (**VOC-DRA-001**), nada compara
  automaticamente "o que foi prometido" com "o que apareceu". Hoje é conferência humana com
  tabela na mão.
- **Não prova `intent`.** Nenhum frame prova que a cena **fez** o que se propôs a fazer com o
  espectador. Isso é parecer do Sovereign, e continua sendo.
- **Não prova o master.** A cena passa por **duas** compressões (cena `-crf 18 -preset slow`, master
  `-crf 19 -preset medium`): textura fina de 1 px que sobrevive ao probe pode morrer no segundo passe.

---

## 6. Recovery path (falha por etapa)

| Sintoma | Causa provável | Ação exata |
|---|---|---|
| Elemento pedido **não aparece** no frame | token ⛔ (`typewriter`/`assets`) ou condição não satisfeita | §3.5; se for ⛔, abrir Pedido (§7) + aplicar o fallback declarado |
| **Anel não desenha** | `runningRing` sem `heroIcon` — **o default do nó** | acrescentar `heroIcon` a `elements` **e** garantir keyword no texto; avisar o Encenador (a grade vira coluna) |
| **Gráfico vazio** e o layout mudou (contador subiu, legenda no topo) | `chart` ligado sem `series` trafegando | desligar `chart` **ou** enviar `data_patch.series` **e** executar pelo Run All (o botão do inspector perde o dado) |
| **Selo não nasce** | falta a palavra-gatilho ou as aspas no `event` | reescrever o `event`: `badge 'TEXTO' acende` |
| **Contador com número errado / faltando** | número ausente do texto, ou solto e < 100 | escrever o número no `description`/`event`; conferir contra `src/test/motion-scene-number.test.ts` |
| **Nota de direção apareceu na tela** | cena **sem narração conectada** ⇒ `description` vira legenda | conectar a narração (a tela cala) **ou** reescrever `description` como frase de sustentação |
| Evento **fora da palavra** (>15 frames) | grade uniforme não encaixa a narração | recalcular `n` (§4.3); se dois beats exigirem `n` incompatíveis, encaixar o **payload**, declarar o desvio **em frames** e abrir VOC-DOP-006 |
| **Render lento demais** (>400 ms/frame) | efeito de rasterização caro | bench A/B do DoP; precedente: um único `blur(70px)` custava **711 ms/frame** = 65% do render |
| **Ícone errado** | keyword casou com outro verbete | trocar a **palavra** no texto (não o ícone — não há como escolher) |
| **Layout re-sorteou sozinho** após ajuste de copy | `layout = seed % 3`, seed = hash(título+descrição) | esperado, não é bug. Única âncora: `heroIcon`. **VOC-STG-001** |
| Cena "pronta" **sem frame** | violação de Lei 1 | *"Cérebro sem mãos"*: declarar que não pode validar e pedir o probe. **Nunca** declarar pronto |

---

## 7. Onde a trupe termina e a engenharia começa

### 7.1 A fronteira, em uma frase

**A trupe escreve o que o motor sabe encenar. O `engineer-spaces` muda o que o motor sabe.**
Nenhuma lente toca `scripts/motion/scene-template.ts`, `scripts/motion-bridge.ts`,
`supabase/functions/motion-render/`, `src/types/canvas.ts` ou os inspectors. Falta de capacidade
**nunca** vira patch improvisado — vira **Pedido de Vocabulário**.

| Território | Dono | Fronteira |
|---|---|---|
| Partitura (o que a cena faz, onde, como é vista) | **trupe** | escreve; não implementa |
| Campos do nó, motor, fila, custo, catálogo, system prompt do maestro | **`engineer-spaces`** | implementa; não dirige |
| Beats→HTML→render→mix→Biblioteca, QA A/V | **`creative-director`** (skill `motion-scenes`) | produz; não muda vocabulário |
| Custo em mco, escolha motion × Veo × Nano, entrega | **`creative-director`** | o custo da trupe é **tempo de máquina**, não dinheiro |
| GO de mudança global (`grade`, Picture Lock) | **Sovereign** | — |

### 7.2 O formato do Pedido de Vocabulário

**Onde:** `.claude/proposals/vocab-motion-<ID>.md` · **Para:** agente `engineer-spaces`
**Referência na partitura:** `"vocabRequests": ["VOC-STG-005"]`
**Numeração (reserva por lente, sem colisão):** `VOC-DRA-###` Dramaturgo · `VOC-STG-###` Encenador ·
`VOC-DOP-###` DoP. **Nunca duplique o pedido de outra lente — assine junto.**

```markdown
# <ID> — <nome curto do verbo/capacidade>
**Pedido por:** <lente> · **Data:** <AAAA-MM-DD> · **Cena(s):** <projeto/cena>
**Necessidade dramática/encenacional/cinematográfica:** o que a cena PRECISA fazer, em uma frase.
**Contrato proposto:** o campo e a forma exatos (`elements:["barChart"]` + `bars:[{label,value,…}]`),
no vocabulário do motor — não em prosa.
**Por que não dá com o que existe:** a prova material (file:line ou frame) de que a capacidade falta.
**Custo estimado:** classe de rasterização (compositor/layout/filtro) — MEDIR antes de aceitar (Lei 1).
**Fallback declarado enquanto o pedido não fecha:** o que a trupe encena HOJE, e o que se perde com isso.
**Impacto se ignorado:** o que continua saindo errado na tela do canal.
```

**Três regras invioláveis do pedido:**

1. **Fallback é obrigatório.** Pedido sem fallback = cena travada. A trupe **sempre** entrega algo
   executável hoje, com a perda declarada.
2. **O pedido não autoriza escrever o token.** Até o `engineer-spaces` fechar, o token continua ⛔ na
   partitura. Escrevê-lo "porque o pedido está aberto" é exatamente o nó que nasce morto.
3. **Motor material sem BoK para.** Capacidade nova que muda o produto → Amendment BoK +
   Pattern Conformance (Closed-Loop Step 3.5), não um patch no template.

### 7.3 Pedidos abertos (estado material de 2026-08-05)

| ID | O que falta | Consequência hoje |
|---|---|---|
| **VOC-DRA-001** | campo `score` (jsonb) em `MotionSceneData` — a partitura viaja com o nó | gate de honestidade não pode ser mecânico; a decisão vive fora do nó |
| VOC-DRA-002 | `typewriter` no motor | oferecido na UI, descartado em silêncio |
| VOC-DRA-003 | `assets` (thumb real) no motor | idem |
| VOC-STG-001 | `staging.grid` honrado (hoje `layout = seed % 3`) | o Encenador **não escolhe** a grade |
| VOC-STG-002 | plano `fg` com parallax e desfoque por camada | quadro chapado, sem volume |
| VOC-STG-003 | rebaixamento dos não-focais (`dof: raso`) — **DoP assina junto** | tudo em foco = tudo sem hierarquia |
| VOC-STG-004 | `entrances`/`exits` dirigidos | blocking inexistente |
| **VOC-STG-005** | `series` no tipo do nó + inspector + catálogo do agente | `compara` só chega à tela por `data_patch` cru |
| **VOC-STG-005b** | paridade do botão do inspector com o Run All (`series` perdido em `MotionSceneInspector.tsx:68-81`) | **dois caminhos, um perde o dado — falso-sucesso silencioso** |
| VOC-STG-007 | contador secundário / rótulo de contraponto | cena com 2+ números só encena 1 |
| VOC-DOP-001 | câmera de cena (`push`/`pull`/`whip`) por beat | todo motion do canal é plano fixo |
| VOC-DOP-002 | key/rim direcionais com motivação (aparato, não emissão) | quadro chapado (perícia §8) |
| VOC-DOP-003 | `focusPull` dirigível por beat | não se redireciona o olho sem cortar |
| VOC-DOP-004 | transição entre cenas (`dissolve`/`dip-to-black`) no montador | **toda** emenda do episódio é corte seco |
| VOC-DOP-005 | `grade` por cena em `MotionComposition` | uma paleta só para toda a obra |
| VOC-DOP-006 | `beats[].atSec` explícito (âncora medida, não grade uniforme) | evento cai fora da palavra |
| VOC-DOP-007 | cor de acento por elemento (tudo é `#00f2ff` hardcoded) | "acende em vermelho" não existe |
| VOC-DOP-008 | frames em JPEG q95 em vez de PNG | −22% de render medido, sem perda visível após CRF 18 |
| **VOC-ENG-001** | as duas injeções do maestro (§4.5) | o agente reproduz o defeito por ignorância |
| **VOC-ENG-002** | `MOTION_DEFAULT_ELEMENTS` pede `runningRing` **sem** `heroIcon` (`canvas.ts:1180`) | **todo nó novo nasce com um anel que nunca desenha** |

> ⚠️ **Pedidos já FECHADOS** (não reabrir): `badges` instanciado (`f731080`) · a tela cala com
> narração + anel de progresso existe (`852dc08`) · barras com dado declarado (`e0fef7f`) ·
> fundo `estudio` honrado + 1080p nativo (`5763a5e`). Versões antigas dos agentes ainda listam
> alguns destes como abertos — **recência vence** (Lei 1, corolário).

---

## 8. Sequence — o passo a passo, com critério material

| # | Passo | Operator | Critério de sucesso **material** |
|---|---|---|---|
| 0 | Re-verificar o motor (§3.6) | quem for assinar | `git log` + `git status` colados; tabela §3 confirmada ou emendada |
| 1 | Medir a narração | Produção | `ffprobe … format=duration` → `D` colado (nunca estimado) |
| 2 | Ancorar as palavras | Produção | SRT do `whisper.cpp` com as fronteiras das `anchorWord` |
| 3 | **Partitura-TEATRO** | Dramaturgo | `intent` + `stakes` + `beats[]`; todo `anchorWord` presente no SRT; todo `onScreen` ≤6 palavras |
| 4 | **Partitura-ESPAÇO** | Encenador | `staging` completo; **um** focal por beat; `negativeSpace` se acima do teto |
| 5 | **Partitura-CINEMA + relógio + orçamento** | DoP | `n` com a conta colada; `light.motivation` nomeia fonte da ficção; ms/frame medido |
| 6 | Reconciliar vocabulário | as três | zero token ⛔ sem Pedido + fallback (§3.7) |
| 7 | **Compilar** para o nó | Maestro | só os campos de §4.2; nenhuma nota de direção em campo de tela |
| 8 | **Probe por beat** | Produção | frames em `t_i` para **todos** os beats |
| 9 | **Gates G-H1..G-H4** | Produção + Sovereign | tabela §5.2 preenchida com prova visual; medição de zona colada |
| 10 | Render + mix | Produção (`motion-scenes`) | MP4 ≥ 20 KB; narração **audível** (mix acontece no encode) |
| 11 | Biblioteca + Record | Produção | asset id de `register_creative_asset`; partitura arquivada (§4.4) e citada no HANDOFF |

**Exemptions:** ajuste de uma palavra do `onScreen` sem mudar `action`/`turn` dispensa passos 4-6,
**mas nunca** os passos 8-9. Frame é inegociável.

---

## 9. Success signal

Uma cena está **encenada** (não apenas escrita) quando, na mesma mesa:

1. **A partitura existe** em `.claude/context/partituras/<projeto>/<cena>.partitura.json`, com zero
   token fora do VOCAB v1 e todo ⛔ acompanhado de Pedido + fallback.
2. **Existe um frame por beat**, e a tabela §5.2 está preenchida **linha por linha com prova
   visual** — nenhum `action` sem o seu sinal na tela.
3. **G-H2** (ocupação) e **G-H3** (sincronia ≤15 frames) estão medidos, com o output colado.
4. **O MP4 fala**: o clipe sai com a narração mixada, não mudo.
5. **O Sovereign aprovou pelo olho** — sobre os frames, não sobre o texto da partitura.
6. **O Record do HANDOFF cita**: o path da partitura, os IDs dos Pedidos abertos, e o asset id.

**Sinal de FRACASSO — a assinatura do defeito original, e ele é reconhecível:**
uma partitura bonita, aprovada em texto, cujo frame do beat 3 **não mostra nada do que ela prometeu**
— e ninguém percebeu porque nada quebrou, nada deu erro, o render saiu "normal".

> **MATE A POESIA. ENTREGUE ENGENHARIA.**

---

## Anexo — Estado material verificado nesta sessão (Lei 1)

| Fato | Prova |
|---|---|
| HEAD `e0fef7f`; motor mudou 3× em 2026-08-05 | `git log --oneline -8 -- scripts/motion/scene-template.ts` |
| 4 arquivos do rail motion com mudanças **não commitadas** | `git status --porcelain` → `M scripts/motion-bridge.ts`, `M scripts/motion/scene-template.ts`, `M src/hooks/useCanvasPipeline.ts`, `M supabase/functions/motion-render/index.ts` |
| `typewriter` e `assets` = **0 ocorrências** no motor | `grep -c` em `scene-template.ts` |
| `badges`=5 · `runningRing`=2 · `chart`=12 ocorrências (**vivos**) | idem |
| anel exige herói | `scene-template.ts:478` `if(heroEl && SPEC.elements.indexOf('runningRing')>=0)` |
| default do nó pede anel **sem** herói | `src/types/canvas.ts:1180` |
| `series` trafega edge→worker→template | `motion-render/index.ts:87,140` · `motion-bridge.ts:205` · `scene-template.ts:335,686` |
| `series` **não** existe no tipo do nó / factory / inspector | `grep -n series src/types/canvas.ts …/MotionSceneInspector.tsx` → sem resultado |
| botão do inspector **não** envia `series`; Run All envia | `MotionSceneInspector.tsx:68-81` × `useCanvasPipeline.ts:43` |
| maestro não conhece `motionScene` | `grep -n motionScene supabase/functions/spaces-agent-chat/index.ts` → sem resultado |
| `data_patch` arbitrário passa (só `kind/label/status/output/error` são estruturais) | `spaces-agent-actions.ts:34` |
| relógio uniforme | `scene-template.ts:218` |
| grade fixa no encode | `motion-bridge.ts:228-234` · `FPS=30` · `RENDER_SCALE=1.5` |
| portas do nó | `NODE_HANDLES.motionScene` = entra[`input_voice`,`input_asset`] sai[`output_video`] |

**Arquivos de referência (leia, não presuma):**
`.claude/context/motion-engine-forensics-2026-08-05.md` ·
`.claude/agents/{dramaturgo,encenador,diretor-fotografia}.md` ·
`.claude/skills/motion-scenes/SKILL.md` ·
`docs/processes/repertorio-producao-profissional.md` ·
`src/lib/cinematic-grammar.ts` (`MIX_TARGETS`, `STAGE_GATE`, `MANDATORY_NEGATIVES`) ·
`docs/processes/engineer-spaces-node-authoring.md`.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

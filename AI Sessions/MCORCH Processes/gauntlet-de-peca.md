# SOP — Gauntlet de Peça (torneio de variações + par atômico + acervo versionado)

> **Lei 2 (Processo Antecipado).** Nasceu do defeito medido em 2026-08-15: o gauntlet sobrescrevia
> as peças e produziu um par onde o texto descrevia uma imagem e o arquivo era outra.
> Runner: [`scripts/ep07/gauntlet-piece.ts`](../../scripts/ep07/gauntlet-piece.ts) ·
> Guard de provedor: [`scripts/qa/guard-image-provider.sh`](../../scripts/qa/guard-image-provider.sh)

---

## O que é

Em vez de aceitar a primeira imagem que o modelo devolve, a peça entra num **torneio**: N variações
do mesmo assunto sob o mesmo contrato de fotografia, todas recortadas com alpha pelo `matte.py`, e
um **contact sheet** sobre o fundo do canal para o julgamento humano. Só a vencedora vira camada de
cena. A régua da Higgsfield mede a mesma disciplina do outro lado: 473.214 gerações para aprovar 600
assets (~0,13%) — o que separa não é o modelo, é o funil.

**Doutrina do Sovereign:** *"variação é acervo, não descarte."* As perdedoras não são lixo — são
objetos dramáticos disponíveis para outra cena.

---

## O defeito que este SOP existe para não repetir

| Evidência | Medida |
|---|---|
| `microfone-v4-cut.png` | **1024×1024**, 330.565 B, gravado **12/08 10:28:59** |
| irmãs `v1/v2/v3` | **2048×2048**, ~1,8-2,0 MB, gravadas **12/08 18:47-18:48** |
| `microfone-v4.prompt.txt` | gravado **18:48:06** — **8h19m07s DEPOIS** da imagem que diz descrever |
| os outros 18 pares do kit | PNG sempre **15-46 s DEPOIS** do prompt (geração + matte) |

**Causa raiz:** o `.prompt.txt` era escrito **antes** do `try` que gera a imagem. Quando a variação
falhava, sobrava prompt novo ao lado de imagem velha — e o `catch` só imprimia no console. O guard
`if (!cuts.length) exit(1)` só dispara quando **todas** falham, nunca quando **uma** falha.

**Causa agravante:** aquela execução saiu pelo OpenRouter, que descarta o `imageSize` nativo — daí
a única peça a 1024² num kit de 2048².

**Causa de identidade:** `Date.now()` era chamado em dois pontos da mesma execução (254 ms de
diferença medidos), então o asset da Biblioteca não casava com a pasta que o produziu.

---

## Operator

Quem executa hoje: o **MCORCH Master Execution Agent** (ou o Sovereign, pela CLI). O julgamento da
peça vencedora é **sempre humano** — nenhum gate deste SOP julga qualidade.

## Sequence

| # | Passo | Comando | Critério de sucesso material |
|---|---|---|---|
| 1 | Ver o catálogo de peças | `bun run scripts/ep07/gauntlet-piece.ts --list` | a peça alvo aparece com `slug → layerId (bloco)` |
| 2 | **Ensaio hermético** (sempre antes de gastar) | `GAUNTLET_DRY=1 bun run scripts/ep07/gauntlet-piece.ts <slug> 4` | `exit 0`, N variações, "execuções coexistindo: ≥1", **nada na Biblioteca** |
| 3 | Torneio real | `bun run scripts/ep07/gauntlet-piece.ts <slug> 4` | N linhas `<tag>: <bytes> B · 2048×2048 → recorte ok`; contact sheet na Biblioteca |
| 4 | Conferir os pares | `bun run scripts/ep07/gauntlet-piece.ts --verify <slug>` | `N execução(ões) · 0 problema(s)`, `exit 0` |
| 5 | Julgamento (**humano**) | abrir o contact sheet em `/dashboard/spaces/assets` | o Sovereign nomeia a variação vencedora |
| 6 | Guard de provedor | `bash scripts/qa/guard-image-provider.sh` | `✅ … scripts/ep07/: 0 ocorrência(s)` |
| — | Reparar metadado de execução antiga (**custo 0**) | `… --reparar <slug> <runId>` | recalcula formato/dimensão/sha do disco, corrige extensão que mente e republica o ponteiro se `latest` apontar para ela |

### Quanto custa (medido na tabela oficial do Google, 2026-08-15)

Geração de imagem **não tem free tier em nenhum modelo Gemini** — a crença de que seria gratuita é
falsa e já orientou decisão nesta casa.

| modelo | por imagem | observação |
|---|---|---|
| `gemini-2.5-flash-image` (Nano Banana) | **US$ 0,039** · **0,0195 em Batch** | metade do preço pela Batch API |
| `gemini-3.1-flash-image` (Nano Banana 2) — **default** | **US$ 0,101 a 2K** (0,067 a 1K · 0,151 a 4K) | melhor aderência a prompt multi-restrição |
| `gemini-3-pro-image` | US$ 0,134 (1K/2K) · 0,24 (4K) | |

Logo: um torneio de 4 variações a 2K custa **US$ 0,404**, e o kit de 19 peças custou ~US$ 1,9. É
barato, mas **não é zero** — e é por isso que o passo 2 (`GAUNTLET_DRY=1`) vem antes, sempre.

> **Regra do Sovereign (2026-08-15): nunca várias variações para VÍDEO.** Torneio é para imagem,
> onde a variação custa centavos. Em vídeo, gera-se uma; se não servir, gera-se outra.

## Verification gates

- **G1 · par atômico** — o `.prompt.txt` só existe se o `-cut.png` existir. Variação que falha tem
  os três arquivos removidos (`resíduo removido` no log). Nunca sobra meio par.
- **G2 · resolução homogênea** — duas resoluções na mesma execução = `exit 1` com a mensagem
  nomeando o precedente. É o gate que teria barrado o `microfone-v4`.
- **G3 · procedência no arquivo** — todo `.prompt.txt` abre com `execução`, `modelo`, `imageSize`,
  **resolução real lida do IHDR do PNG** (não a pedida) e `sha256` da imagem.
- **G4 · acervo versionado** — a verdade mora em `<slug>/<RUN_ID>/`; execuções **coexistem**.
- **G5 · ponteiro íntegro** — `<slug>/` reflete **uma** execução inteira, reescrita por completo a
  cada publicação. Rodar com N menor **não** deixa as sobras da execução anterior para trás.
- **G6 · manifesto reconferível** — `--verify` recomputa sha256 dos três arquivos de cada variação
  contra o `manifest.json`. Não depende de mtime, que qualquer `cp`/`rsync` reescreve.

> **Por que sha256 e não mtime:** o defeito original foi *achado* por mtime, mas mtime é frágil —
> uma cópia do kit apagaria a evidência. O manifesto sobrevive à cópia.

## Recovery path

| Falha | O que fazer |
|---|---|
| `RESOLUÇÕES MISTAS` (G2) | Não publique. Confira `IMAGE_MODEL`/`IMAGE_SIZE` e rode de novo — houve troca de rail no meio do torneio. |
| `--verify` acusa `sha ≠ manifesto` | O par foi adulterado depois da geração. A execução íntegra está em `<slug>/<RUN_ID>/`; republique com uma nova execução, **nunca** conserte o arquivo à mão. |
| `nenhuma variação sobreviveu` | Rode o passo 2 (`GAUNTLET_DRY=1`). Se o DRY passa, o problema é rede/credencial, não o runner — veja `scripts/qa/probe-google-key.ts`. |
| Peça publicada por engano | `<slug>/<RUN_ID>/` da execução anterior continua intacto: rode de novo apontando para ela, ou refaça o hardlink. Nada foi destruído. |
| Guard de provedor vermelho | Migre o runner para `generateImage` do helper. **Não** acrescente o arquivo à lista `LEGADO` sem GO do Sovereign — a lista não cresce. |

## Success signal

```
N execução(ões) · 0 problema(s)          ← --verify
execuções coexistindo em disco: ≥2       ← acervo, não sobrescrita
✅ … scripts/ep07/: 0 ocorrência(s)      ← guard de provedor
```
mais o contact sheet aberto na Biblioteca com a vencedora escolhida **por um olho humano**.

---

## Notas de campo

- **`GAUNTLET_DIR` default** deixou de ser um scratchpad `/tmp` (que já estava morto e recriava a
  árvore a cada execução, para morrer de novo no reboot) e passou a ser
  `repurpose-inbox/<uid>/ep07-kit/gauntlet`, que sobrevive à sessão. Mesma família do achado que
  encontrou o benchmark aprovado `fcf91d44` vivendo só num `/tmp` de sessão encerrada.
- **O ponteiro `<slug>/` é sagrado.** O único consumidor do layout é a escada de resolução de
  `scene-estrutura-pilha.ts:93-102`, e ela resolve com `find(existsSync)` — ou seja, **cai em
  silêncio**. Se o caminho antigo sumisse, a cena não falharia: renderizaria com a peça velha sem
  avisar. Trocar um `exit 2` honesto por asset stale invisível é pior que o bug original.
- **Hardlink, não cópia.** O ponteiro compartilha inode com a execução (link count 2): zero byte
  duplicado, e apagar o ponteiro não toca no acervo. Em volumes distintos há fallback para `cp`.
- **O DRY não julga qualidade.** Ele prova encanamento (coexistência, par, cabeçalho, gate de
  resolução) a US$ 0. Peça bonita continua sendo decisão de olho humano sobre imagem real.
- **O Google devolve JPEG, não PNG.** Medido em 2026-08-15: `gemini-3.1-flash-image` respondeu
  `ffd8ffe0 … JFIF` a um pedido de imagem. A primeira versão do gate presumiu PNG e leu os bytes
  16..23 como IHDR — num JPEG eles são a densidade JFIF (`012c 012c` = 300 DPI), e a "resolução"
  saiu **19660800×4293597064**. O gate escrito para pegar resolução errada leu a resolução errado:
  a mesma família de defeito que ele existe para combater. Hoje o formato é discriminado por
  **magic number**, e o arquivo recebe a extensão do que ele realmente é — extensão que mente é a
  semente do próximo diagnóstico errado. O `-cut.png` é sempre PNG de verdade: o `matte.py` grava
  RGBA, e é ele que vira camada de cena.
- **Reparar é melhor que regerar.** Quando o defeito está no *metadado* e não na imagem, `--reparar`
  recalcula tudo do arquivo a custo zero. Regerar seria pagar de novo por um erro de leitura — e
  jogar fora a variação que o modelo já entregou.

## Ver também

- [`build-deploy-materiality.md`](build-deploy-materiality.md) — a mesma disciplina de "não declare
  sucesso sem olhar o artefato servido"
- [`docs/roadmap/regua-de-cinema-higgsfield-2026-08-14.md`](../roadmap/regua-de-cinema-higgsfield-2026-08-14.md) §L7 — a lacuna que originou este SOP
- [`scripts/lib/gemini-image.ts`](../../scripts/lib/gemini-image.ts) — o rail de imagem canônico

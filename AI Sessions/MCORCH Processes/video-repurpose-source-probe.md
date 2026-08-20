# SOP — Decode-probe do master antes de cortar (video-repurpose) (Lei 2)

> **Feature:** gate de duas fases que prova, **antes** de qualquer re-encode, que o master do `video-repurpose` (a) tem container legível e (b) **decodifica de verdade** em cada ponto que o render vai tocar.
> **BoK SSOT:** `docs/bok/video-repurpose/00-deepsearch-blueprint.md` §Pilar II (FR-VR-003/004/005) — o probe é guarda de pré-condição do mesmo pilar, não feature nova de produto.
> **Motivo (incidente 2026-07-20):** um master foi **reescrito no meio de um experimento A/B** (mtime `2026-07-20 00:36:12`). Os dois `ffmpeg exit 69` foram atribuídos ao motor `caption_mode:beats`; o motor estava íntegro — o **arquivo** não estava. O worker gastou minutos de CPU, falhou no meio, e o `rmSync` do `finally` **destruiu a evidência**. O probe transforma "falha opaca no meio do render" em "recusa imediata com o corte e o timestamp exatos".

## ORO triplet
- **Operator:** MCORCH Master Execution Agent (constrói/prova); na operação, o worker `video-repurpose-bridge` executa sozinho.
- **Reviewer:** Sovereign + `/security-review` (o probe recebe caminho de arquivo → `spawn` com **array** de args, nunca string de shell).
- **Owner:** Sovereign. Custo mcoCoins = **0** (rail FFmpeg é grátis); o custo é CPU: **0,089 s** por `ffprobe` + o decode **integral** das janelas de corte (medido 1080p: **2,8 s por 60 s** de janela, contra dezenas de segundos para re-encodar os mesmos 60 s a `preset medium` ⇒ o gate custa ~10% do render que protege). Janelas sobrepostas são fundidas e decodificadas uma única vez; `-xerror` aborta no primeiro pacote ruim, então **master corrompido falha rápido** — o custo cheio só é pago em master saudável.

## Operator — manual equivalente
Hoje, para saber se um master está íntegro antes de cortar, o operador roda à mão:

```bash
# Fase 1 — container (duração plausível?)
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 master.mp4

# Fase 2 — decode real da JANELA INTEIRA do corte (saída descartada). Aqui: corte 42s→72s.
ffmpeg -v error -xerror -ss 42 -i master.mp4 -t 30 -f null -
```

E lê o **stderr**, não só o exit code — porque o exit code mente (ver Achados abaixo).

## Achados materiais que definem o veredito (não re-derivar)
| # | Achado | Consequência de design |
|---|--------|------------------------|
| A1 | `ffprobe` **não** detecta a corrupção tipo EP02 (chunk duplicado): reporta duração plausível e **exit 0**. | A Fase 1 sozinha é insuficiente — serve só para a duração e para o gate de janela. |
| A2 | `ffmpeg -xerror` sozinho **também não basta**: na fixture corrompida, em `t=20 s` o erro apareceu no **stderr com exit 0**. | O veredito honesto é **FALHA se `exit !== 0` OU `stderr` não-vazio**. |
| A3 | Em arquivo íntegro o `stderr` vem **vazio** em todos os pontos sondados (zero falso-positivo medido). | O critério A2 é utilizável sem ruído. |
| A4 | `-ss` além do EOF retorna **exit 0 com stderr vazio** — um **passe vacuoso** (o probe "passa" porque não decodificou nada). | A Fase 1 (ffprobe → duração) vem **ANTES** e rejeita janela fora de faixa: `cut_window_exceeds_source`. |
| A6 | **Amostrar as pontas da janela NÃO basta — foi medido aprovando um master corrompido.** A 1ª versão do gate sondava 2 s em cada `in_sec` + 1 ponto perto de `max(out_sec)`. Fixture de 60 s corrompida em `t=15 s`, cortes `[(0,20),(40,60)]` ⇒ `assertSourceDecodable` retornou **verde** (`{probedAt:[0,40,58]}`) enquanto `-ss 15` no mesmo arquivo cuspia **2093 bytes** de erro de decoder. O corte #1 seria renderizado com frames-lixo (A5). | A Fase 2 decodifica a **janela inteira** de cada corte (janelas sobrepostas fundidas). Cobertura parcial é **pior que nenhum gate**: dá falsa segurança sobre exatamente o dano que ele existe para pegar. Travado por **G7**. |
| A5 | **O render sobre master corrompido nem sempre falha — às vezes tem FALSO-VERDE.** Medido 2026-07-20 na fixture: `segmentVideo` sobre o master corrompido saiu **exit 0 em 1,78 s** e produziu um MP4 **estruturalmente válido** (4,000 s, 120 frames — idêntico ao íntegro) porém com **24.987 bytes contra 231.779** do íntegro: frames lixo. | O probe **não é só economia de CPU** — é o único ponto que impede **publicar um asset quebrado**. Nenhuma checagem a jusante pega isso: duração ✓, contagem de frames ✓, MP4 válido ✓. O probe rejeitou o mesmo arquivo em **259 ms**. |

## Sequence — ordem (cada passo com critério material)
| # | Passo | Executor | Sucesso material |
|---|-------|----------|------------------|
| 1 | Worker resolve o `inputPath` do master (host inbox `repurpose-inbox/<uid>/` ou download do bucket privado owner-scoped). | `video-repurpose-bridge` | caminho existe em disco. |
| 2 | **Fase 1 — container:** `probeContainer(path)` → `{ durationSec }`. Exit ≠ 0 ou duração não-finita/≤0 ⇒ `source_container_unreadable`. | `probe-core.ts` | duração numérica > 0. |
| 3 | **Gate de janela:** para cada corte, `out_sec > durationSec + 0,5 s` ⇒ `cut_window_exceeds_source` (nomeia o corte e os timestamps). Fecha o passe vacuoso A4. | `probe-core.ts` | nenhuma janela além do EOF. |
| 4 | **Fase 2 — decode:** decodifica a **janela inteira** (`in_sec`→`out_sec`) de **cada** corte, com janelas sobrepostas/contíguas fundidas num único passe e clampadas à duração real. Slide de carrossel (janela de span 0) vira uma janela mínima de `probeSec`. Falha se `exit ≠ 0` **ou** `stderr` não-vazio. Amostrar só as pontas **não** é aceitável (A6). | `probe-core.ts` | todos os trechos com exit 0 e stderr vazio; `decodedSec` ≈ soma das janelas fundidas. |
| 5 | Só então o worker chama `segmentVideo`/`buildCarousel`. | `video-repurpose-bridge` | render prossegue. |
| 6 | Em falha (2/3/4), o worker finaliza `video_renders` como `failed` com a mensagem específica, loga em `infra_health_logs` (`repurpose_failed`) e **PRESERVA o workDir** (`/tmp/repurpose-<render_id>`), logando o caminho. | `video-repurpose-bridge` | linha `failed` + `metadata.work_dir_preserved` no log. |

## Verification gates
- **G1 `cut_window_exceeds_source`:** janela com `out_sec` além da duração é recusada **sem** rodar decode-probe (senão passaria vacuosamente — A4).
- **G2 stderr-é-veredito:** arquivo corrompido cujo `ffmpeg` sai com **exit 0** mas escreve no stderr ⇒ **FALHA** (A2).
- **G3 zero falso-positivo:** arquivo íntegro passa em todos os pontos (A3).
- **G4 anti-injection:** todo `spawn` recebe **array** de args (`spawn('ffmpeg', [...])`), nunca string concatenada com o path — um master chamado `a.mp4; rm -rf /` não vira comando.
- **G5 mensagem honesta:** o erro nomeia **o corte e o timestamp** ("o corte #3 em 00:42:10 não decodifica"), nunca um genérico "erro no vídeo".
- **G6 evidência preservada:** após falha, `/tmp/repurpose-<render_id>` **existe** (não foi apagado) e o caminho está no log.
- **G7 cobertura integral:** corrupção no **miolo** de uma janela (longe de `in_sec` e de `out_sec`) é pega. Trava a regressão de A6 — se alguém voltar a amostrar pontas para ganhar latência, este gate fica vermelho.

Anticorpo re-executável: `scripts/qa/smoke-repurpose-guards.ts` (G1..G7 do rail + os guards de enqueue). **Rodar antes de mexer no probe ou nos guards de janela.**

## Recovery path
| Falha | Diagnóstico | Ação exata |
|-------|-------------|------------|
| `source_container_unreadable` | Upload truncado/incompleto, ou master reescrito durante o upload. | `ls -la` no master (conferir `mtime` e tamanho) → re-subir o arquivo completo → re-enfileirar. **Nunca** re-tentar o mesmo render: a fonte é a mesma. |
| `cut_window_exceeds_source` | O cut-spec veio de um master mais longo (ex.: trocaram o arquivo mantendo o nome). | Re-rodar `detect-viral-moments` **sobre o master atual** e reenfileirar com o novo cut-spec. |
| `source_decode_failed` | Master corrompido (chunk duplicado/truncado) — o caso EP02. | Reconstruir o master a partir da origem. Reparo best-effort: `ffmpeg -err_detect ignore_err -i ruim.mp4 -c copy bom.mp4` e **re-rodar o probe** antes de aceitar. |
| Suspeita de A/B contaminado | Dois renders falharam "no mesmo motor". | `stat` no master: se o `mtime` cai **entre** os dois renders, o experimento é **inválido** — o arquivo mudou, não o motor. Foi exatamente o que aconteceu em 2026-07-20. |

## Success signal
`video_renders` do dono em `state='done'` com N clipes registrados — **e**, no caminho de falha, uma linha `failed` cuja mensagem nomeia o corte/timestamp e cujo `workDir` ainda existe para perícia. O sinal de que o SOP está vivo é duplo: o **tempo até o diagnóstico** (259 ms de recusa em vez de minutos de re-encode terminando em `exit 69` opaco) e — mais importante, por A5 — **nenhum clipe de frames-lixo chega ao bucket**.

## Notas de design
- **Duas fases, nessa ordem, não-negociável.** Container antes de decode porque o decode-probe **passa vacuosamente** além do EOF (A4). Inverter a ordem reintroduz o falso-verde.
- **`stderr` não-vazio = falha** é deliberadamente estrito. A alternativa (allowlist de mensagens "benignas") foi rejeitada: exigiria enumerar o que não conhecemos, e o custo de um falso-positivo (re-subir o master) é muito menor que o de um falso-verde (minutos de CPU + asset publicado quebrado).
- **`probeSec = 2` por padrão.** Medido: 0,25 s por janela. Aumentar cobre mais bytes, mas o ganho decai — a corrupção tipo EP02 é regional, não pontual.
- **Tolerância de 0,5 s no gate de janela** absorve o arredondamento de duração de container MP4; não é folga para janela realmente fora de faixa.
- **Por que não `-c copy` para checar:** `-c copy` não decodifica — não veria a corrupção. O probe **precisa** decodificar (`-f null -` descarta a saída, custo só de CPU).

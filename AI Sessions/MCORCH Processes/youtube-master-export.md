# SOP — Exportar o master para o YouTube (Amendment 41 · FR-SPACES-145/146/147/148)

> **Lei 2 (Processo Antecipado).** Este é o processo MANUAL que a automação reproduz. Se o operador
> humano não consegue executá-lo sem erro, a automação também não — só vai errar mais rápido.
>
> **BoK:** `docs/bok/spaces-evolution/41-amendment-youtube-export.md` (SSOT — números, gates, OTDs).
> **Doutrina:** `docs/bok/spaces-evolution/40-amendment-motion-doctrine-v3.md` (Lei 5, Fase 1).

**ORO** — Operator: MCORCH Agent (engineer-spaces) · Reviewer: Sovereign (parecer OCULAR sobre o
frame, não sobre o log) · Owner: Sovereign (é o arquivo que o público vê, e são dezenas de minutos
de fila serial por clique).

---

## 1. Operator — quem executa hoje, e com o quê

| Papel | Ferramenta |
|---|---|
| **Sovereign** (dono da decisão) | `/dashboard/spaces/<id>` → nó **Montar Master** → assiste o master → botão **Exportar para YouTube (1080p)** |
| **Worker do host** (executa) | `motion-bridge.service` (systemd --user) → `scripts/motion-bridge.ts` `processAssemble` |
| **Fila** | `video_renders` (`engine='assemble'`, `composition.output_profile='youtube'`, `charged_mco:0`) |
| **Verificação** | `ffprobe` / `ffmpeg -af ebur128` sobre o MP4 baixado do bucket privado |

**Custo:** US$ 0 · 0 mcoCoins. O que se paga é **relógio**: 4-8× tempo real (medido 2026-08-05).

---

## 2. Sequence — a ordem, com critério material de sucesso em cada passo

| # | Passo | Critério de sucesso (material) |
|---|-------|-------------------------------|
| 1 | **Montar master** (perfil `iteration`) e **assistir** | `d.output.videoUrl` presente; o Sovereign viu o corte inteiro |
| 2 | **Aprovar** — "está perfeito" | Decisão humana. Sem ela o botão de export fica **desabilitado** por construção |
| 3 | Clicar **Exportar para YouTube (1080p)** e **confirmar** no diálogo | Diálogo mostra a estimativa (`~X a Y min`), "fila ocupada", "R$ 0", "pode fechar a aba" |
| 4 | Edge fn `assemble-master` enfileira | HTTP **202** `{ status:"queued", render_id, profile:"youtube" }` |
| 5 | Worker reivindica e grava o orçamento | linha `video_renders` em `running` com `qa.budget_ms` e `qa.heartbeat_at` avançando |
| 6 | 1º passe do loudnorm (só áudio) | log do worker sem `loudnorm 1º passe não mediu` |
| 7 | Encode (grade unificada + grão + crf 14) | processo `ffmpeg` vivo; `qa.heartbeat_at` continua avançando |
| 8 | Upload + spine + finalize | asset **`MASTER 1080p · <projeto>`** na Biblioteca; key `<uid>/masters/<renderId>.mp4` |
| 9 | Reconciliação na UI | card mostra **`1080p pronto`**; inspector abre o player do export |

**Regra que não se negocia:** o export **nunca** entra no "Executar tudo". A diretiva é literal —
*"APÓS validação humana"*. Automatizar isto queima dezenas de minutos de fila em material que
ninguém aprovou.

---

## 3. Verification gates — o que provar antes de dizer "pronto"

Nenhum "ficou melhor". Cada gate é medida ou frame.

| Gate | Comando | Esperado |
|---|---|---|
| **G1 tagging** | `ffprobe -v error -select_streams v:0 -show_entries stream=color_range,color_space,color_transfer,color_primaries -of csv=p=0 <export>` | `tv,bt709,bt709,bt709` — e no master de **iteração**, `unknown` (os perfis são distintos de verdade) |
| **G2 dado entregue** | `ffprobe -show_entries format=bit_rate` nos DOIS masters do mesmo projeto | export **≥ 2×** a iteração |
| **G3 banding** | mesmo frame de gradiente dos dois (`-vf "select='eq(n,K)'"`), contar lumas distintos | export **maior**; Vision QA no par lado a lado |
| **G4 grade unificada** | `signalstats` (YAVG/SATAVG) em 2 frames na fronteira motion↔Veo | diferença **menor** que na iteração |
| **G5 sem vinheta tripla** | `bun run scripts/qa/smoke-assemble-graph.ts` | `vignette` = 0 nas entradas marcadas, 1 nas cruas |
| **G6 áudio** | `ffmpeg -i <export> -af ebur128=peak=true -f null -` · `ffprobe stream=sample_rate` | true peak ≤ −1,0 dBFS · LUFS ±0,5 do alvo · **48000** |
| **G7 relógio real** | `time` de um export de master REAL | dentro da faixa estimada; > 40 min para 5 min ⇒ prancheta |
| **G8 não-regressão** | mesmo projeto, perfil `iteration`, antes/depois | **sha256 idêntico** (o filtergraph legado é fixado em `scripts/motion/master-export.test.ts`) |
| **G9 reversibilidade** | Biblioteca | **dois** assets distinguíveis (`MASTER ·` e `MASTER 1080p ·`), duas keys |
| **G10 tipos/testes** | `npx tsc -p tsconfig.app.json --noEmit` · `bun run test` · smoke | 0 erros · suíte verde · 12/12 gates do smoke |
| **G11 worker no ar** | `systemctl --user show motion-bridge.service -p ExecMainStartTimestamp` vs `stat -c %y scripts/motion-bridge.ts` | serviço iniciado **DEPOIS** do arquivo — senão o teste roda contra código velho e "passa" mentindo |

---

## 4. Recovery path — falha no passo N

| Sintoma | Causa provável | Recuperação exata |
|---|---|---|
| 422 `invalid_output_profile` | cliente mandou perfil fora da allowlist | nada a fazer no servidor: é o fail-closed funcionando |
| 422 `export_already_running` | já existe export deste projeto na fila | esperar, ou cancelar no console (✕) e clicar de novo |
| Botão de export desabilitado | não há master de iteração concluído | montar e **assistir** o master primeiro (passo 1-2) |
| Export gira e nunca acaba na tela | reconciliação perdida | o poll de PÁGINA (`useMotionRenderSync`) resolve em ~12s; se a linha sumiu, o anticorpo devolve o nó a `idle` |
| `loudnorm 1º passe não mediu` no log | áudio silencioso (`-inf`) ou ffmpeg tropeçou | **não é falha**: o export segue em passe único. Loudness fica adaptativo — reexportar não resolve sozinho |
| Export morre por timeout | master muito longo ou host disputado | o orçamento é `max(30 min, dur × 20 s)`. Estourar isso é sinal de contenção real: checar os workers irmãos (`voice-bridge`, `subtitle-bridge`, `video-bridge`) antes de mexer no orçamento |
| Master de iteração mudou de bytes | regressão no `buildAssembleGraph` | `bun run test scripts/motion/master-export.test.ts` — o filtergraph legado está fixado literal; o teste aponta a divergência |
| Worker rodando código velho | faltou o restart (G11) | `systemctl --user restart motion-bridge.service` e reconferir os timestamps |

**Cancelar** um export em voo: ✕ no console de execução (FR-SPACES-144). O batimento de 15 s
detecta a linha deletada e **mata o ffmpeg** — sem ele o ✕ só teria efeito depois de 20+ minutos.

---

## 5. Success signal

> Na Biblioteca existem **dois** arquivos do mesmo episódio, distinguíveis pelo título; o
> `MASTER 1080p` passa em G1 (BT.709) e G2 (≥2× o bitrate); o Sovereign assistiu e aprovou o
> frame — **e o master de iteração continua exatamente como estava** (G8).

---

## 6. O que este SOP NÃO cobre (declarar o vazio é doutrina da casa)

- **Upload ao YouTube.** O rail existe (`scripts/youtube-upload-bridge.ts`), mas juntar as duas
  coisas transformaria "aprovei o arquivo" em "publiquei". O export **entrega o arquivo**; publicar
  continua sendo outro clique, deliberado (privado-primeiro).
- **10-bit, HDR, 4K.** Fora por medição e por construção — ver §8 da Amendment 41.
- **A vinheta dupla das cenas.** Está queimada no pixel (`scene-template.ts`); é Fase 1 da Doutrina
  v3. O export garante apenas **não somar a terceira**.
- **A primeira geração de perda.** As cenas já nasceram em crf 18; o export re-encoda a partir
  delas. O conserto é OTD-SPACES-049 (intermediário a `-crf 12 -preset veryfast`), e exige bench.

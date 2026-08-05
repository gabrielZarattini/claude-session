<!-- Proveniência: workflow wf_b91935d4-5ba · 4 agentes (CC0/bancos · geração por IA · síntese+DIY · veredito).
     Diretiva Sovereign 2026-08-04: farmar a biblioteca de Hard SFX/Wallah/Foley. Toda licença citada
     foi lida na fonte (URLs no corpo); o que não deu para confirmar está marcado NÃO CONFIRMADO. -->

# Biblioteca de SFX do MCORCH — como farmar

> **ORO desta frente** — Operator: agente de produção (main + `creative-director`) · Reviewer: Sovereign · Owner: Sovereign (blast radius = claim/strike de Content ID num canal monetizado = desmonetização + exposição jurídica).
>
> **Gate de custo:** USD externo = 0 em todas as camadas obrigatórias. Nenhum passo deste guia exige assinatura.

---

## 1. Veredito — a melhor combinação para ESTE canal

**Uma linha:** *base Sonniss + bisturi Freesound CC0 + tudo que tem "instante" sintetizado em FFmpeg no host.* IA generativa entra como **quarta** camada, opcional, e só para ambiência.

O canal é pt-BR, monetizado, **2 vídeos/semana**, **motion-first** (a doutrina selada no EP05: motion scenes > screencast). Isso muda o cálculo em relação a qualquer guia genérico de sound design, por três razões materiais:

1. **Motion-first significa que quase todo SFX precisa cair num beat exato** — o nascimento de um nó, o fechamento de um ring, o corte de narração. Som que erra o frame é pior que silêncio.
2. **2 vídeos/semana significa que a biblioteca é usada dezenas de vezes por mês** — dívida de atribuição por som não escala, e um único ativo NC contamina retroativamente todo o catálogo.
3. **A casa treina/clona voz localmente (Qwen3-TTS)** — cláusulas anti-IA de licença deixam de ser letra morta e viram risco operacional real.

### A pilha, camada a camada

| Camada | Fonte | Licença | Custo | Por que ESTA e não outra |
|---|---|---|---|---|
| **Hard SFX · Foley · Ambiência · Risers de trailer** | **Sonniss GDC Bundle** (2014→2026, 200+ GB) | Proprietária royalty-free, **sem atribuição**, vitalícia | $0 | Único acervo grátis com padrão de biblioteca paga — prova material: WAV `pcm_s24le · 96 kHz · estéreo`. Cobre 4 dos 5 gaps de uma vez. Bulk por torrent oficial |
| **O que o Sonniss não tem (pt-BR, wallah brasileiro, ruído de nicho)** | **Freesound com filtro CC0 travado** (378.896 sons) | CC0 1.0 — domínio público | $0 | Bisturi, nunca espelho: 2.000 req/dia ⇒ clonar levaria ~189 dias. Só o que falta |
| **UI beeps / cliques de game-feel** | **Kenney** (16 packs) | **CC0 1.0** verbatim no `readme.txt` | $0 | 16 zips, sem login, minutos. Mono/OGG/curto — perfeito para UI, inútil para foley |
| **Tudo com "instante": riser, sub-drop, whoosh, impacto, click, beep, glitch, drone, hum, room tone, IR de reverb** | **FFmpeg 6.1.1 do próprio host** | **Obra sua** | $0 | **Determinístico e versionável** — o mesmo comando dá o mesmo WAV amanhã, casado ao beat da narração. É o que a IA estruturalmente não entrega |
| **Foley com identidade do canal (teclado, cabo, obturador, gaveta) + room tone real** | **Gravação caseira** (celular em WAV, à noite) | **Obra sua** | $0 | Zero terceiro na cadeia. É o que separa "canal com SFX de banco" de "canal com som próprio" |
| **Wallah pt-BR** | **Qwen3-TTS local** (já no host, Apache-2.0) + receita de 6 camadas | **Obra sua** | $0 | **Nenhum modelo de SFX gera wallah em português.** Truque que a ElevenLabs não vende |
| *(opcional, Fatia 2)* Ambiência/textura/drone gerada | **Stable Audio 3 Small-SFX** | Stability AI Community License — comercial grátis **até USD 1M/ano** | $0 | Único motor de IA que passa no gate de licença **e** roda em CPU ARM64. Mas resolve ~40% e **nada** de hard SFX |
| *(emergência)* SFX específico que nada resolve | ElevenLabs **Starter pago**, `duration` sempre especificada | Comercial no plano pago | ~US$0,007/efeito | Cartão de crédito, não pipeline. Free tier = **uso comercial proibido no ToS §1(c)** |

### Por que a IA fica em 4º lugar (e não em 1º)

A regra que resume a auditoria inteira: **IA generativa é boa onde não existe um evento a acertar.** Modelos de difusão latente trabalham a ~10,76 Hz — cada token latente cobre **~93 ms**. Um clique de porta tem ataque <2 ms e energia acima de 10 kHz; ele cabe **inteiro dentro de um único latente**. O modelo não tem resolução temporal para colocar o ataque no frame que você quer (41,7 ms @ 24 fps).

| Categoria | IA | Veredito |
|---|---|---|
| Ambiência · room tone · drone · textura | 🟢 Excelente | Sinal estacionário, sem evento |
| Wallah (em inglês) | 🟢 Boa | Mas *"not able to generate realistic vocals"* — e não fala português |
| Foley sem sync | 🟡 Média | "passos numa sala" sai; "passos NESTE ritmo" não |
| Foley com sync de frame | 🔴 Ruim | Resolução latente ≫ precisão de frame |
| **Hard SFX transiente** | 🔴 Ruim | Pré-ringing, cauda de reverb embutida, escala errada |
| **UI beeps** | 🔴 **Pior custo-benefício** | Sinal sintético determinístico pedido a um difusor de 600M — e sai **não-reprodutível** |
| Risers / stingers / sub-drops | 🟡 Inútil na prática | Precisam casar com o beat; IA não dá controle de duração exata nem de curva |

Some-se o custo de re-rolar prompt: gerar um beep na IA custa mais tempo do que os ~5 ms de um `ffmpeg` que você versiona no git.

---

## 2. O que baixar em massa HOJE — licença confirmada

### 🥇 Sonniss GDC Game Audio Bundle — resolve 80% do problema numa tacada

- **Origem canônica:** `https://gdc.sonniss.com/` · licença: `https://sonniss.com/gdc-bundle-license/`
- **Texto exato:** *"Worldwide, non-exclusive, royalty-free license"*; *"may use and modify the licensed sound effects for personal and commercial projects **without attribution**"*; *"unlimited number of projects for the entirety of their life time"*.
- **Volume:** bundle 2026 = 7,47 GB / 347 arquivos; **arquivo histórico 200+ GB** em 9 anos. GDC 2019 sozinho = 331 bibliotecas comerciais.
- **Bulk:** 5 zips split + espelho Drive + **torrent oficial**; anos antigos via `ia download SonnissGameAudioGDC` (9,6 GB / 646 WAVs), `SonnissGameAudioGDCPart2/4/5`, `game-audio-gdcpart-6`.
- **Restrições:** não revender os sons **como vêm** (incorporados ao seu vídeo, pode) · **proibido treinar IA** com eles.
- **Atalho de descoberta:** `gamesounds.xyz` espelha GDC 2015→2023 **já descompactado**, navegável por biblioteca, com `?zip=<dir>`. Use para **descobrir e testar** (pegar 40 whooshes sem puxar 200 GB) — mas **registre no manifesto a origem canônica Sonniss**, porque a licença não autoriza expressamente redistribuição por terceiros. *NÃO CONFIRMADO:* quem opera o mirror.

**Bibliotecas nominais por gap** (para `wget` cirúrgico):

| Gap | Bibliotecas |
|---|---|
| Portas/impactos | `3maze - Doors` · `344 Audio - Practical Doors` · `Soundopolis - Household Doors HD` · `3maze - FINAL IMPACT` · `Baxter Audio - IMPACT` · `Bluezone - Cinematic Metal Impacts` |
| UI | `Airborne Sound - Interface Accents` · `3maze - UI FX` · `344 Audio - Organic User Interface` · `Sonic Bat - Sci-Fi Interface Construction Kit I/II` · `Sound Ex Machina - UI SOUNDS FUTURISTIC` |
| Foley | `Sonic Bat - Videogame Foley Essentials I` · `Systematic-Sound - Modern Cloth Foley 01` · `Studio 23 - Ultimate Footstep Collection` |
| Wallah/multidão | `Matt Script - Airplanes & Airports Walla & Ambience` · `Coll Anderson - The Battle Crowd Collection` · `2496SoundEffects - Ambisonic Crowds` |
| Room tone (61 libs) | `2496SoundEffects - Room Tones and Quiet Places Pack 1` · `344 Audio - UK Residential Room Tones` · `Articulated Sounds - Empty Hotel Quiet Room Tones` |
| Risers/stingers | **`Federico Soler Fernandez - Effective Trailer Risers / Braams / Downers / Booms / Hits & Impacts / Drones / Pings / Alarms`** (uma trailer-house inteira de graça) · `Airborne Sound - Eclectic Whooshes 2/3` · `Sound Spark LLC - Drone Shepard Tones` |

### 🥈 Kenney — CC0 puro, 16 zips, minutos

`https://kenney.nl/assets/category:Audio`. Licença verbatim do `readme.txt`: *"Creative Commons Zero, CC0 … free to use in personal, educational and commercial projects … crediting Kenney (**this is not mandatory**)"*. `Interface Sounds` = 100 arquivos. Prova material: `back_001.ogg` → `vorbis · 44100 Hz · 1 canal · 0,064 s`. **Ótimo para UI, inútil para foley/wallah.**

### 🥉 Freesound com filtro CC0 **hard-coded** — bisturi, não espelho

Acervo (contagem ao vivo 2026-08-05): **CC0 378.896** · CC-BY 258.878 · **CC-BY-NC 82.127** · Sampling+ ~11.412.

O mito do "Freesound é lixo" morre no número: dentro do CC0, 96 kHz = 19.902 · 48 kHz = 110.057 · 44,1 kHz = 239.956 · **lixo (≤22 kHz) = 2.904 (~0,8%)**. O problema real é **curadoria** (ruído de fundo, clipping, gain), não sample rate.

```
filter=license:"Creative Commons 0" samplerate:[44100 TO 96000] type:wav
```

Limites: **60 req/min · 2.000 req/dia** (429 ao estourar); baixar o **original exige OAuth2** (previews .ogg/.mp3 são keyless). Cobertura CC0 dos gaps: ambience 17.394 · door 9.253 · impact 7.001 · footsteps 5.931 · crowd 4.764 · whoosh 2.300 · room tone 1.716 · **walla 1.350** · riser 848 · sub drop 626 · ui click 406.

> ⚠️ **Compliance:** baixar CC0 manualmente é livre (domínio público). **Automatizar via API dentro de um produto comercial** cai no ToS da API (*"Terms for commercial use of the API will be negotiated case by case with UPF"*). Se um dia isso virar nó do Spaces, é item de compliance — não de código.

### Complemento manual (TIER A/B)

- **99Sounds** (`99sounds.org/license/`): *"royalty-free for personal and commercial projects"*, crédito *"not obligatory"*. Packs `Cinematic Sounds` / `Cinematic Sound Effects` / `99 Sound Effects`. Zip por pack, às vezes com e-mail gate. Cobre risers/cinemático se você não quiser sintetizar.
- **OpenGameArt filtro CC0** (892 SFX) — complemento, manual.
- **Pixabay** — funciona, mas é o pior custo/benefício: **não é CC0 desde jan/2019** (é a *Pixabay Content License*), a **API oficial não tem endpoint de áudio**, e o próprio site diz *"Systematic mass downloads are not allowed"*. Além disso há histórico documentado de **claims de Content ID sobre material Pixabay** — eles publicaram guia de como disputar. Último recurso, clique manual.

---

## 3. O que GERAR com IA (e o que jamais gerar)

**Único motor aprovado:** **Stable Audio 3 Small-SFX** — 459M DiT + 108M autoencoder, 44,1 kHz estéreo, até 2 min, **8 passos ping-pong sem CFG** (é por isso que roda em CPU). Licença dos pesos: **Stability AI Community License** — comercial grátis **até USD 1M/ano de receita**, e *"you own your outputs and can distribute and commercialize them freely"*.

O argumento subestimado, e decisivo para canal monetizado: **os dados de treino são declarados e limpos** — 1.278.902 gravações, 806.284 licenciadas da AudioSparx e 472.618 do Freesound (266.324 CC0 · 194.840 CC-BY · 11.454 Sampling+). Procedência auditável, não "scraped".

**Use só para:** ambiência, room tone, field recording, textura, drone, whoosh longo, chuva/vento/multidão-como-textura, camadas de fundo. **Nunca para:** click, beep, impacto, mecanismo, qualquer coisa que precise cair num frame.

**Fallback com trilha ARM pronta:** *Stable Audio Open Small* (341M–500M, até 11 s) tem implementação C++ **Apache-2.0 da própria Arm** (`audiogen.cpp`, LiteRT + XNNPack + KleidiAI). Números da Arm com INT8: 15,3 s → 6,6 s; modelo 5,2 GB → 2,9 GB. Ressalva honesta deles: *"audio degradation—particularly for audio samples with rich high-frequency content"* — a quantização degrada exatamente os agudos do hard SFX. ⚠️ O exemplo mira **Android**; portar para linux/arm64 é trabalho real. **NÃO CONFIRMADO** que builda neste host.

**Realidade do hardware (medida):** `Neoverse-N1 · aarch64 · 4 cores · 23 GB RAM · sem GPU`, com `asimddp` presente mas **`i8mm` e `bf16` ausentes**. Consequência: MOSS-SoundEffect v2 (Apache-2.0 limpo, 48 kHz — a melhor licença da lista) é **inviável** aqui: `device="cuda"`, `bfloat16`, Triton CUDA Graph, **100 passos** num DiT de 1,3B. Guardar na gaveta até haver GPU ou quantização GGUF/ONNX. Estimativa honesta para o SA3 Small-SFX neste host: **20–90 s por clipe de 10 s em fp32** — aceitável para fila assíncrona (molde `video_renders`), inaceitável para interatividade. **Só medindo prova.**

### 🚫 Rejeitados — não gaste uma hora neles

| Motor | Motivo |
|---|---|
| **Meta AudioGen / AudioCraft** | **Pesos CC-BY-NC 4.0** (código MIT — armadilha do badge). E tecnicamente morto: tokenizer EnCodec **16 kHz** ⇒ teto de Nyquist 8 kHz ⇒ **fisicamente incapaz** de brilho de hard SFX |
| **TangoFlux** | *"non-commercial research use only"* |
| **AudioLDM 2** | CC-BY-NC-SA 4.0 |
| **MMAudio** | Código MIT, **pesos CC-BY-NC 4.0** |
| **ThinkSound** | `Apache-2.0` no arquivo **E** *"Commercial use is NOT permitted"* no README ⇒ **rejeição por ambiguidade** (você seria o réu argumentando qual vale) |
| **HunyuanVideo-Foley** | Território exclui UE/UK/Coreia |
| **ElevenLabs free tier** | ToS §1(c): *"Free User … may only use the Services for non-commercial purposes"* |

---

## 4. O que SINTETIZAR em FFmpeg — a camada soberana

`ffmpeg version 6.1.1-3ubuntu5` (aarch64, `--enable-gpl`) — **verificado no host nesta sessão**. Zero dependência nova (`sox` não está instalado, e não precisa).

### A gramática

```
FONTE          →  ENVELOPE        →  FILTRO      →  ESPAÇO   →  NÍVEL
anoisesrc         aeval / volume     highpass       aecho      volume
sine              afade              lowpass        afir       alimiter
aevalsrc          asetrate           acrusher       adelay     loudnorm
```

SFX profissional é **sempre camada + envelope**, nunca fonte pura. A diferença entre "bipe amador" e "UI de produto" é o envelope exponencial e o corte de graves.

### A matemática que quase todo tutorial erra

`sin(2π·f(t)·t)` **não** varre a `f(t)` — a frequência instantânea é a derivada da fase, e o sweep sai com o **dobro** da taxa pretendida.

- **Linear** `f0→f1` em `T`: `phase(t) = 2π( f0·t + ((f1−f0)/(2T))·t² )`
- **Exponencial** `f0→f1` em `T`: `phase(t) = 2π·f0·T/ln(f1/f0)·( (f1/f0)^(t/T) − 1 )` — validado por zero-crossing: pedido 80 Hz→4 kHz, medido **91 → 3548 Hz**.

### Receitas-chave (todas executadas, com medição)

```bash
# SUB-DROP (chirp linear 80→20 Hz) — I: -7.8 LUFS · Peak 0.0 dBFS
ffmpeg -y -f lavfi -i "aevalsrc='0.9*sin(2*PI*(80*t+((20-80)/(2*2.5))*t*t))':d=2.5:s=48000" \
 -af "volume='min(1,t*8)*min(1,(2.5-t)*2)':eval=frame,alimiter=limit=0.9" -c:a pcm_s24le subdrop.wav

# RISER (chirp exponencial + ruído + rampa quadrática) — o pão-com-manteiga do motion
ffmpeg -y -f lavfi -i "anoisesrc=d=4:c=pink:a=0.8:r=48000" \
 -f lavfi -i "aevalsrc='0.4*sin(2*PI*80*4/log(50)*(pow(50,t/4)-1))':d=4:s=48000" \
 -filter_complex "[0:a]highpass=f=200,lowpass=f=1200,afade=t=in:st=0:d=3.8:curve=exp[nz];\
[1:a]volume='0.15+0.85*pow(t/4,2)':eval=frame,highpass=f=120[tn];\
[nz][tn]amix=inputs=2:normalize=0,aecho=0.8:0.7:45:0.25,alimiter=limit=0.9" \
 -ar 48000 -ac 1 -c:a pcm_s24le DESIGNRiser_RiserTension4s_MCORCH_SYNTH.wav

# IMPACTO — 3 camadas obrigatórias: sub (peso) + transiente (ataque) + cauda (espaço)
ffmpeg -y -f lavfi -i "sine=f=55:d=2:r=48000" -f lavfi -i "anoisesrc=d=2:c=white:a=0.9:r=48000" \
 -filter_complex "[0:a]asetrate=48000*0.6,aresample=48000,afade=t=out:st=0.05:d=1.6:curve=exp,volume=2.0[sub];\
[1:a]lowpass=f=1800,afade=t=out:st=0:d=0.28:curve=exp,volume=0.8[tr];\
[sub][tr]amix=inputs=2:duration=longest:normalize=0,alimiter=limit=0.9" \
 -ar 48000 -ac 1 -c:a pcm_s24le DESIGNImpact_ImpactSubHit_MCORCH_SYNTH.wav

# UI CLICK de 12 ms — SÓ sai certo com envelope por amostra (ver achado abaixo)
ffmpeg -y -f lavfi -i "anoisesrc=d=0.05:c=white:r=48000:a=1" \
 -af "aeval='val(0)*exp(-t*450)':c=same,highpass=f=1800,alimiter=limit=0.95" -c:a pcm_s24le click.wav

# DRONE tenso — 55 / 82.5 / 110.3 Hz (o .3 fora do harmônico exato é o que cria o batimento orgânico)
ffmpeg -y -f lavfi -i "sine=f=55:d=20:r=48000" -f lavfi -i "sine=f=82.5:d=20:r=48000" \
 -f lavfi -i "sine=f=110.3:d=20:r=48000" \
 -filter_complex "[0:a][1:a][2:a]amix=inputs=3:normalize=0,volume=0.3,\
chorus=0.6:0.9:50|60|70:0.4|0.32|0.3:0.25|0.4|0.3:2|2.3|1.3,tremolo=f=0.15:d=0.3,lowpass=f=2000,\
afade=t=in:st=0:d=3,afade=t=out:st=17:d=3" -ar 48000 -ac 1 -c:a pcm_s24le AMBDrone_DroneTenseDark_MCORCH_SYNTH.wav

# ROOM TONE (-56 LUFS) — o colchão inaudível que mata o "silêncio digital"
ffmpeg -y -f lavfi -i "anoisesrc=d=10:c=pink:r=48000:a=0.02" \
 -af "highpass=f=45,lowpass=f=7000,volume=-6dB" -c:a pcm_s24le roomtone.wav

# HUM de lab/servidor — Brasil é 60 Hz, não 50
ffmpeg -y -f lavfi -i "sine=f=60:d=30:r=48000" -f lavfi -i "sine=f=180:d=30:r=48000" \
 -f lavfi -i "anoisesrc=d=30:c=pink:a=0.05:r=48000" \
 -filter_complex "[0:a]volume=0.25[a];[1:a]volume=0.08[b];[2:a]lowpass=f=8000[c];[a][b][c]amix=inputs=3:normalize=0,volume=0.6" \
 -ar 48000 -ac 1 -c:a pcm_s24le AMBRoomTone_RoomToneServerHum_MCORCH_SYNTH.wav

# REVERB por convolução — fabrique a própria IR, não baixe nenhuma
ffmpeg -y -f lavfi -i "anoisesrc=d=1.2:c=white:a=1:r=48000" \
 -af "afade=t=out:st=0:d=1.2:curve=exp,lowpass=f=6000,highpass=f=120,volume=0.5" -ac 1 _IR/ir_room.wav
ffmpeg -y -i click.wav -i _IR/ir_room.wav \
 -filter_complex "[0:a]apad=pad_dur=1.5[dry];[dry][1:a]afir=dry=10:wet=10" -c:a pcm_s24le click_inroom.wav
```

Também no repertório: **whoosh** (`anoisesrc c=brown` + envelope assimétrico; versão estéreo com `apulsator`; versão reversa com `areverse` para o "sugar" antes do corte), **beep de confirmação** (2 tons subindo) e **de erro** (2 tons descendo + `acrusher`), **glitch** (`acrusher bits=3:lfo=1`), **tick de typewriter**, **loop perfeito** (`acrossfade=d=2:c1=tri:c2=tri` — 10+10−2 = **18.000 s exatos**).

### 🔬 Achado material: `eval=frame` destrói transiente

| Envelope | Primeiro pico | Pico |
|---|---|---|
| `volume=…:eval=frame` | amostra **1030 → t = 21,46 ms** | −23,25 dBFS |
| `aeval='val(0)*…'` (por amostra) | amostra **130 → t = 2,71 ms** | −18,72 dBFS |

`volume` com `eval=frame` avalia **uma vez por bloco de 1024 amostras** = 21,3 ms @ 48 kHz. **21 ms é meio frame de vídeo a 24 fps.** Para ambiência é invisível; para um click é *flam* audível e erro de sync visível.

> **Regra a codificar em `src/lib/cinematic-grammar.ts`** (hoje o arquivo tem `MIX_TARGETS` e `MIX_HIERARCHY`, mas **nenhuma regra de SFX** — 168 linhas, verificado): *envelope de evento com duração < ~200 ms DEVE usar `aeval` (por amostra); `volume:eval=frame` só para envelope ≥ 200 ms.*

### Gotchas — todos achados executando, não lendo

| Gotcha | Sintoma | Correção |
|---|---|---|
| **`ffmpeg` come o stdin do loop** | Batch processa **1 arquivo** e morre (exit 254) | **`ffmpeg -nostdin`** — obrigatório em todo `while read` |
| `afir` corta a cauda | Reverb some; saída tem a duração do input | `apad=pad_dur=1.5` **antes** do `afir` |
| `loudnorm` TP é **teto**, não alvo | Pedi `TP=-6`, saiu **−8,8 dBFS** | One-shot normaliza **por pico**, nunca por `loudnorm` |
| `amix` normaliza sozinho | Mix fraco ao somar camadas | `amix=…:normalize=0` **sempre** |
| `atempo` mín. 0.5 | `out of range [0.5 - 100]` | Encadeie `atempo=0.7,atempo=0.7` |
| `asetrate` muda a duração | `sine=d=2` + `asetrate*0.6` → **3,33 s** | Compense com `atempo` ou aceite |
| `grep` do `max_volume` pega histograma | multi-linha → `SyntaxError` no awk | `sed -n 's/.*max_volume: \(-\?[0-9.]*\) dB.*/\1/p'` |
| **WAV Sonniss com artwork embutido** | `ffprobe` acusa stream `mjpeg` colado no PCM | **`-map 0:a:0 -vn`** em todo comando que toca o corpus |
| Sub abaixo de 40 Hz | Some no celular e come headroom | Fundamental em **50–70 Hz** |

---

## 5. O que GRAVAR em casa

**O que separa amador de profissional não é o microfone.** O mic do celular moderno é bom. O que mata é (a) processamento de voz do sistema, (b) ruído de manuseio, (c) piso de ruído do ambiente.

| Regra | Por quê |
|---|---|
| **WAV/PCM, nunca o gravador de voz padrão** | O app de voz aplica denoise + AGC e corta em 8–16 kHz — **destrói o transiente**, que é 90% do impacto |
| **Desligue supressão de ruído e ganho automático** | AGC "bombeia" o silêncio entre hits e inutiliza o take em camada |
| **NUNCA segure o celular** | Apoie em pano dobrado/tripé. Ruído de manuseio é irreparável |
| **15–30 cm, levemente fora de eixo** | Evita pop e sibilância |
| **Grave à noite, geladeira/ar desligados** | Piso de ruído cai 10–15 dB — um apartamento às 2h é um estúdio |
| **10–20 takes de tudo, variando força/ângulo/material** | Foley é **seleção**, não gravação. Você usa 2 de 20 — e a variação vira a "família" do som |
| **60 s de room tone ao fim de CADA sessão** | É a cola que faz as camadas soarem do mesmo lugar. **Sem isso a biblioteca não casa** |
| **Pico em −12 a −6 dBFS** | Headroom. Clipar = som morto |
| **Cabine improvisada** (closet com roupa / cobertor) | Você **adiciona** sala depois com `afir` — nunca o contrário |

**Regra de ouro:** o objeto que *parece* certo raramente *soa* certo. Som é abstração, não literalidade.

### Os 20 objetos que mais rendem em canal de tecnologia

Teclado mecânico (→ digitação, "IA processando") · teclado membrana · **mouse click + scroll (→ click de UI)** · trackpad · tampa de laptop (→ abrir/fechar painel) · **cabo USB-C/P2 encaixando (→ "conexão estabelecida")** · obturador de câmera (→ screenshot) · interruptor (→ toggle) · **moedas/chaves (→ shimmer de UI, notificação de valor)** · **fita adesiva puxada (→ riser orgânico)** · papel amassando (→ glitch, deletar) · **zíper (→ whoosh; pitch-down = épico)** · isqueiro (→ spark) · caneta clicker · gaveta (→ impacto médio) · **copo de vidro com unha (→ notificação/"concluído")** · cooler de PC 2 min (→ room tone de lab) · HD externo spin-up (→ boot/processamento) · plug P2 no jack (→ áudio caindo) · **caixa de papelão (→ impacto de logo, com sub por baixo)**. Bônus: sopro perto do mic, estalo de dedos, fricção de tecido, gelo em copo, elástico.

### Cadeia de limpeza (testada — rumble sub-80 Hz caiu de −21,4 para −30,2 dB)

```bash
ffmpeg -nostdin -y -i foley_raw.wav \
 -af "highpass=f=80,afftdn=nr=18:nf=-45:tn=1,deesser=i=0.3,\
      acompressor=threshold=0.15:ratio=3:attack=5:release=120,alimiter=limit=0.95" \
 -ar 48000 -ac 1 -c:a pcm_s24le foley_clean.wav
```

`highpass=80` (40 Hz se o som tem sub real) · `afftdn nr` entre 12–20 (mais que isso soa "aquático") · `alimiter` sempre por último.

> **Por que `afftdn` e não `arnndn`:** o `arnndn` exige um `.rnnn`, e o repositório mais usado (`richardpl/arnndn-models`) **não tem arquivo LICENSE**. `afftdn` não precisa de modelo nenhum: zero dependência, zero risco.

### 🇧🇷 Wallah pt-BR com o Qwen3-TTS que já está no host

**Nenhum modelo de SFX gera wallah em português.** A casa já tem TTS multi-voz local Apache-2.0 rodando em ARM64 (`/home/ubuntu/.mcorch/voice-engine`, `voice-bridge.service`).

**As 5 leis:** (1) ininteligibilidade **é** o objetivo — se dá para entender uma palavra, o ouvido trava nela; (2) delays e pitches **primos entre si**, nunca simétricos, senão vira flanger; (3) pitch ≠ velocidade — compense; (4) três distâncias (perto/médio/longe = volume + lowpass + reverb crescentes); (5) nunca a língua errada — prosódia se percebe mesmo ininteligível.

Matemática: `asetrate=48000*k` → pitch ×k e duração ÷k; `atempo=1/k` restaura. Verificado: `k=1.12` + `atempo=0.892857` em 2,000 s → **1,995 s**.

Receita executada (3 vozes → 6 camadas → **13,53 s, −29,1 LUFS, TP −15,4 dBFS**): `asetrate` k ∈ {0.87, 0.92, 0.95, 1.08, 1.14, 1.21} · `adelay` ∈ {0, 370, 810, 1240, 1730, 2150} ms (primos entre si) · `volume` 0.38–0.50 (camadas agudas mais baixas) · **`lowpass=3200` (o parâmetro mais importante — mata a inteligibilidade)** · `highpass=180` · `aecho 60|110|180 ms` (cola tudo no mesmo espaço) · `loudnorm I=-28`. Para multidão grande: renderize 3 blocos com seeds de delay diferentes, o terceiro com `lowpass=2200` e volume menor = **camada distante** (é isso que dá profundidade).

---

## 6. Organização da biblioteca — e como provar procedência num claim

### Onde cada coisa mora (decisão de arquitetura)

| Acervo | Local | No git? |
|---|---|---|
| **Corpus de terceiros** (Sonniss 200 GB, Kenney, Freesound CC0, 99Sounds) | `/home/ubuntu/.mcorch/sfx-corpus/<fonte>/` — molde do `voice-engine` | ❌ **Nunca** (binário massivo) |
| **Biblioteca própria** (sintetizada + gravada + wallah) — poucos MB | `assets/sfx/` no repo | ✅ Sim |
| **Runners** (geradores + `norm-lib.sh` + indexador) | `scripts/sfx/` | ✅ Sim |
| **Índice + manifesto de licença** | `assets/sfx/LIBRARY.csv` + `sfx-corpus/manifest.jsonl` | ✅ **Sim, sempre** |
| Takes brutos | `assets/sfx/_RAW/` | ❌ gitignored, arquivo local |

### Naming — UCS (Universal Category System, domínio público)

```
CatID_FXName_CreatorID_SourceID_UserData.wav
```

`CatID` obrigatório no início (é o único requisito mandatório do UCS). `CreatorID` = `MCORCH`. `SourceID` = `SYNTH` | `FOLEY01` | `EP05` | `SONNISS` | `FREESOUND` | `KENNEY`.

```
UIClick_ClickSoftBlip_MCORCH_SYNTH.wav
DESIGNImpact_ImpactSubHit_MCORCH_SYNTH.wav
CROWDWalla_WallaMurmurPtBr_MCORCH_SYNTH.wav
FOLYKeyboard_KeyboardMechSingle_MCORCH_FOLEY01_Take07.wav
```

**Rígido:** sem espaço, sem acento, sem `ç`. `_` separa campos, `CamelCase` separa palavras dentro do campo — mantém tudo scriptável sem quoting hell.

### Pastas

```
assets/sfx/
├── AMB/{Drone,RoomTone,Loop}/      # estéreo, loopável
├── CROWD/                          # wallah, plateia
├── DESIGN/{Riser,Impact,Whoosh,SubDrop,Glitch}/
├── FOLY/{Keyboard,Paper,Cloth,Metal,Plastic}/
├── UI/                             # click, beep, notify, error
├── _IR/                            # impulse responses p/ afir
├── _RAW/                           # takes brutos — NUNCA entra no projeto
└── LIBRARY.csv                     # índice + LICENÇA por arquivo
```

### Formato técnico

**48 kHz · 24-bit (`pcm_s24le`) · WAV.** Mono para one-shot (deixa o mixer posicionar), estéreo para ambiência/wallah. 96 kHz só se for fazer pitch-down extremo. **Nunca MP3/AAC como master** — perde transiente e acumula artefato em camada.

Ao ingerir do corpus de terceiros, normalize o container preservando o original:

```bash
ffmpeg -nostdin -y -i "<origem>" -map 0:a:0 -vn -ar 48000 -ac 2 -c:a pcm_s24le "<destino>"
```

### Escada de loudness — a regra que quase todo mundo erra

| Nível | Medida | Alvo | Comando |
|---|---|---|---|
| **One-shot** (click, impacto, whoosh) | **Pico** | **−6,0 dBFS** | `volumedetect` → `volume=<delta>dB` (2 passos) |
| **Ambiência / drone / wallah** (asset) | **LUFS integrado** | **−28 a −30 LUFS** | `loudnorm=I=-28:TP=-6:LRA=7` |
| **Ambiência na mixagem** | dB relativo | **−34 dB** (`MIX_TARGETS.ambienceDb`) | atenuação no mix |
| **Master do episódio** | LUFS integrado | **−16 LUFS · TP −1,5** (`MIX_TARGETS`) | `loudnorm=I=-16:TP=-1.5:LRA=11` |

> ⚠️ **`loudnorm` NÃO normaliza one-shot.** Provado: pedi `TP=-6` num whoosh, saiu **−8,8 dBFS** — TP é teto. Um click de 60 ms tem LUFS integrado absurdamente baixo, e o `loudnorm` o empurraria para o clipping.

Runner idempotente (`scripts/sfx/norm-lib.sh`) — saída real: 4/4 arquivos exatamente a −6,0 dB. **`-nostdin` é o que faz o loop não morrer no primeiro arquivo.**

### 🛡️ Manifesto de licença — como você ganha uma disputa de Content ID

Dois artefatos, ambos versionados:

**`assets/sfx/LIBRARY.csv`** — `filename, category, duration_s, samplerate, channels, license, source_url`. Para material próprio: `license=OWN-SYNTHESIZED` ou `OWN-RECORDED`, com o commit do runner que o gerou.

**`sfx-corpus/manifest.jsonl`** — uma linha por arquivo de terceiro:

```json
{"path":"sonniss/GDC2018/AirborneSound-InterfaceAccents/Accent_UI_Alert.wav",
 "sha256":"…","source_url":"https://gdc.sonniss.com/","license_id":"SONNISS-GDC-RF",
 "license_url":"https://sonniss.com/gdc-bundle-license/","attribution_required":false,
 "retrieved_at":"2026-08-05T…Z"}
```

**Por que isso importa concretamente:** numa disputa de Content ID o YouTube pede prova de direito de uso. Com o manifesto você responde em minutos: *este som veio de X, sob a licença Y (URL), baixado em Z, sha256 W*. Sem ele, daqui a 8 meses a resposta é "não sei" — que numa disputa **equivale a "não tenho direito"**. É a mesma disciplina de proveniência que a casa já roda para AI Act Art. 50 (`provenance_*` / IPTC), aplicada ao áudio.

**Bônus de blindagem:** som **sintetizado e gravado por você é imune por construção** — não existe terceiro na cadeia. É por isso que a camada FFmpeg + foley não é economia, é **seguro**.

---

## 7. Armadilhas de licença que dão claim/strike

1. **"CC" ≠ livre.** No Freesound, **82.127 sons são CC-BY-NC** e a UI mostra tudo junto. **Risco nº 1 desta lista inteira.** Nunca deixe script escolher som sem o filtro de licença **hard-coded**.
2. **"Está no archive.org" ≠ domínio público.** Há **rips completos de bibliotecas comerciais** lá: `SoundIdeasSeries4000`, `hollywoodedgecinematicssoundeffects`, agregados de "Sound Ideas / Hollywood Edge / Skywalker / MGM". São os sons **mais fingerprintados do planeta** (Wilhelm Scream, Castle Thunder, stock da Hanna-Barbera). Baixar só itens cuja licença você leu **no próprio item**.
3. **BBC Sound Effects = 🚫 rejeição automática.** RemArc é **non-commercial**, extraído verbatim do bundle da aplicação: *"Commercial use of this content is not allowed under the RemArc license."* E o FAQ da BBC responde sobre YouTube: *"if you monetise it … that counts as commercial use."* É o acervo mais bonito da lista e é **inutilizável** para você.
4. **Licença do repositório ≠ licença dos pesos.** AudioCraft e MMAudio são **MIT no código e CC-BY-NC nos pesos**. Quem lê o badge do GitHub conclui "pode usar" e põe áudio NC num canal monetizado. **AudioGen é o mais perigoso porque é o mais famoso.**
5. **Licença contraditória = rejeição.** ThinkSound tem `Apache-2.0` no arquivo e "commercial use is NOT permitted" no README. Você seria o réu argumentando qual das duas vale.
6. **CC-BY é dívida operacional, não liberdade.** 200 sons CC-BY = 200 linhas de crédito rastreadas **por vídeo, para sempre**. Trate CC-BY como **custo**. CC0 é a única licença com custo de manutenção zero.
7. **Pixabay não é CC0 desde jan/2019**, não tem API de áudio, proíbe mass download — e tem **histórico documentado de claims de Content ID** (eles publicaram guia de disputa).
8. **ZapSplat:** free = **mp3 + atribuição obrigatória**; §8 *"Automated access (bots, scrapers, scripts) is prohibited"* (rescisão contratual, não rate limit); §10-11 *"licensed, not sold"* + **licença revogável**. Licença revogável em canal monetizado é risco estrutural. **Pule.**
9. **Free To Use Sounds:** o nome mente — o tier gratuito **exige atribuição** por link. Só o bundle pago dispensa (USD > 0 ⇒ fora do gate).
10. **Cláusulas anti-IA (Sonniss, ZapSplat, Free To Use Sounds).** Usar no vídeo: OK. **Alimentar treino/fine-tune de modelo de áudio: violação.** Crítico numa casa que roda Qwen3-TTS local — **mantenha o corpus Sonniss fora de qualquer pipeline de treino/clone**.
11. **FSD50K é armadilha silenciosa:** parece "Freesound empacotado", mas mistura **CC0 + CC-BY + CC-BY-NC + Sampling+** dentro, e é mono 16-bit 44,1 kHz. Não use.
12. **ElevenLabs free tier num canal monetizado = violação de contrato** (ToS §1(c), verbatim).
13. **Modelo sem LICENSE** (`richardpl/arnndn-models`) = não usar em produção monetizada.
14. **Artwork embutido em WAV** (confirmado por `ffprobe` em arquivo Sonniss real: stream `mjpeg` no PCM) — não é jurídico, é operacional: sem `-map 0:a:0 -vn` você carrega lixo ou quebra o mux.

---

## Materialidade (Lei 1) — o que foi verificado nesta rodada

- `ffmpeg version 6.1.1-3ubuntu5` (aarch64, `--enable-gpl`) — confirmado no host.
- `src/lib/cinematic-grammar.ts:120-131` — `MIX_TARGETS` existe (`loudnessLufs -16`, `truePeakDb -1.5`, `ambienceDb -34`); `MIX_HIERARCHY` (l.134) lista `"hard SFX"`. **Não existe nenhuma regra de SFX/`aeval` no arquivo (168 linhas).**
- `scripts/sfx/`, `assets/sfx/` e `docs/processes/sfx-*.md` **não existem** — a biblioteca é greenfield.
- Runners e provas vivem **só no scratchpad volátil**: `…/scratchpad/sfxlab/` (26 entradas + `LIB/{AMB,CROWD?,DESIGN,FOLY,UI}` + `norm-lib.sh` + `ir_room.wav`) e `…/scratchpad/sfx-probe/` (7 WAVs: `subdrop`, `riser`, `impact`, `roomtone`, `beep`, `beep_aeval`, `click`). **Precedente EP05: isso sobreviveu por sorte da última vez.**
- Medições herdadas das sondas: chirp 80 Hz→4 kHz medido 91→3548 Hz · `eval=frame` 21,46 ms vs `aeval` 2,71 ms · wallah −29,1 LUFS / TP −15,4 dBFS · cauda `afir` −17,8 → −50,2 → −91,0 dB · `acrossfade` 10+10−2 = 18,000 s · rumble −21,4 → −30,2 dB · pitch compensado 2,000 → 1,995 s · WAV Sonniss `pcm_s24le 96 kHz` 611.294 B · Kenney `vorbis 44,1 kHz mono` 9.095 B.

**NÃO CONFIRMADO (pendências honestas):** ZapSplat (fetch 403 numa das sondas) · EULA do Adobe Audition SFX · licença de SFX do Mixkit (modal JS) · operador do mirror `gamesounds.xyz` · build LiteRT/KleidiAI em linux/arm64 · desempenho real do Stable Audio 3 Small-SFX neste host · redação exata da atribuição no free tier do ElevenLabs (a **proibição de uso comercial** está confirmada verbatim).


---

## Plano de execução (v1)

1. **Colher o scratchpad ANTES de qualquer coisa** (skill `scratchpad-harvest`, Lei 3/EP05): promover `…/scratchpad/sfxlab/norm-lib.sh` e os geradores para `scripts/sfx/` (`gen-riser.sh`, `gen-subdrop.sh`, `gen-whoosh.sh`, `gen-ui.sh`, `gen-impact.sh`, `gen-drone.sh`, `gen-roomtone.sh`, `gen-ir.sh`, `norm-lib.sh`, `index-lib.sh`), parametrizados por flag e com `-nostdin` em todo loop. Gate: `ls -la scripts/sfx/` mostra os arquivos + `bash scripts/sfx/gen-riser.sh --out /tmp/t.wav && ffprobe /tmp/t.wav` roda limpo. O material vive em /tmp volátil — este passo é o único que não pode esperar.
2. **Selar o SOP `docs/processes/sfx-library-synthesis.md` (Lei 2 — precede qualquer automação):** Operator (quem gera/grava hoje) · Sequence numerada (sintetizar → normalizar por pico → nomear UCS → indexar) · Verification gates (`ffprobe` = 48 kHz/24-bit; `volumedetect` = −6,0 dBFS; linha presente no `LIBRARY.csv`) · Recovery (arquivo fora do alvo → re-rodar `norm-lib.sh`, que é idempotente) · Success signal (`LIBRARY.csv` com N linhas e zero campo `license` vazio). Incluir a tabela de gotchas e a **lista de rejeição automática** (BBC/CC-BY-NC/FSD50K/ZapSplat/rips do archive.org/pesos NC).
3. **Criar a estrutura e o contrato de dados:** `assets/sfx/{AMB/{Drone,RoomTone,Loop},CROWD,DESIGN/{Riser,Impact,Whoosh,SubDrop,Glitch},FOLY/{Keyboard,Paper,Cloth,Metal,Plastic},UI,_IR,_RAW}` + `/home/ubuntu/.mcorch/sfx-corpus/{sonniss,kenney,freesound,99sounds}` (molde do `voice-engine`). Commitar `assets/sfx/` (própria, poucos MB) e o `LIBRARY.csv`; **gitignorar** `_RAW/` e todo o corpus de terceiros. Criar `sfx-corpus/manifest.jsonl` vazio com o schema `{path,sha256,source_url,license_id,license_url,attribution_required,retrieved_at}` documentado no SOP.
4. **Fatia Síntese (2 h, zero download, entrega imediata):** rodar os runners variando parâmetros → ~40 arquivos (5 risers, 5 sub-drops, 8 whooshes, 10 UI click/beep, 5 impactos, 4 drones, 3 glitches) + 3 IRs em `_IR/`. Depois `bash scripts/sfx/norm-lib.sh assets/sfx -6.0` e `bash scripts/sfx/index-lib.sh > assets/sfx/LIBRARY.csv` com `license=OWN-SYNTHESIZED`. Gate: todos a −6,0 dBFS e `wc -l LIBRARY.csv` ≥ 41. **Isso já cobre todo o motion graphics do canal sem baixar um único byte de modelo.**
5. **Codificar a gramática de SFX em `src/lib/cinematic-grammar.ts`** (hoje só tem `MIX_TARGETS`/`MIX_HIERARCHY`, 168 linhas): adicionar `SFX_TARGETS` (`oneShotPeakDb: -6`, `ambienceAssetLufs: -28`, `subFundamentalHz: [50,70]`, `envelopePerSampleBelowMs: 200`) e a **regra materialmente provada**: envelope de evento < ~200 ms DEVE usar `aeval` por amostra — `volume:eval=frame` empurra o ataque para 21,46 ms (meio frame @ 24 fps) contra 2,71 ms do `aeval`. Injetar a regra também na skill `motion-scenes` e no agent `creative-director`, como as 18 regras do repertório já são. Gate: `npx tsc -p tsconfig.app.json --noEmit` comparado ao baseline.
6. **Ingerir o Sonniss (o maior ganho por hora da lista inteira):** puxar o bundle 2026 pelo torrent oficial de `gdc.sonniss.com` + os itens oficiais do archive.org (`ia download SonnissGameAudioGDC`, `…Part2`, `…Part4`, `…Part5`, `game-audio-gdcpart-6`) para `/home/ubuntu/.mcorch/sfx-corpus/sonniss/`. Escrever cada arquivo no `manifest.jsonl` com `license_id=SONNISS-GDC-RF` e `attribution_required=false`. **Não transcodificar os 200 GB** — normalizar (`-map 0:a:0 -vn -ar 48000`) só na hora de puxar um som para o projeto (armadilha do artwork `mjpeg` embutido). Gate: `df -h` antes/depois + `wc -l manifest.jsonl` + `ffprobe` de 3 amostras aleatórias mostrando `pcm_s24le`. Atalho de descoberta: `gamesounds.xyz` para achar a biblioteca certa antes de baixar.
7. **Kenney em seguida (minutos):** baixar os 16 zips de `kenney.nl/assets/category:Audio` (com `Interface Sounds` e `UI Audio` primeiro), descompactar em `sfx-corpus/kenney/`, registrar no manifesto com `license_id=CC0-1.0` e `attribution_required=false`, guardando o `readme.txt` de cada pack como prova primária. Gate: `find sfx-corpus/kenney -name '*.ogg' | wc -l` ≥ 100 e todo pack com seu `readme.txt` presente.
8. **Sessão de Foley (3 h, à noite):** gravar os 20 objetos × 10–20 takes em WAV/PCM sem denoise nem AGC, celular apoiado, pico −12 a −6 dBFS, + **60 s de room tone ao fim** (inegociável — é a cola que faz as camadas casarem). Depois: cadeia `highpass=80,afftdn=nr=18:nf=-45:tn=1,deesser=i=0.3,acompressor,alimiter` (nunca `arnndn` — repo dos modelos sem LICENSE), cortar, nomear UCS (`FOLYKeyboard_KeyboardMechSingle_MCORCH_FOLEY01_Take07.wav`), brutos para `_RAW/`. Gate: ~150 arquivos limpos + queda medida de rumble sub-80 Hz no `volumedetect` antes/depois.
9. **Wallah pt-BR + ambiências (1 h):** gerar 3 vozes distintas de ~2 min no `voice-engine` local (Qwen3-TTS), rodar a receita de 6 camadas (`asetrate` k ∈ {0.87,0.92,0.95,1.08,1.14,1.21} · `adelay` primos {0,370,810,1240,1730,2150} · `lowpass=3200` · `highpass=180` · `aecho 60|110|180` · `loudnorm I=-28`) e o empilhamento de 3 blocos para multidão grande, mais `acrossfade=d=2` em todas as ambiências para loop sem clique. Gate: `ffprobe` + `loudnorm` reportando ≈ −28/−30 LUFS e o loop com duração exata `2N−2`. **Nenhum modelo do mercado entrega isto em português.**
10. **Selar a v1 e só então avaliar IA:** rodar `norm-lib.sh` na lib inteira, regenerar `LIBRARY.csv` (zero campo `license` vazio = gate mecânico), commitar `scripts/sfx/` + `assets/sfx/` + SOP, registrar a entrada na Key Files Reference do CLAUDE.md e um nó de observação na Knowledge Mesh. **Só depois** abrir a Fatia opcional: sondar o Stable Audio 3 Small-SFX em CPU no host e **medir** (estimativa honesta: 20–90 s/clipe de 10 s) — se ≤60 s, virar worker no molde `video-bridge` (fila `video_renders`, `charged_mco: 0`), **exclusivamente para ambiência/textura**, nunca para hard SFX. E manter o corpus Sonniss fora de qualquer pipeline de treino/clone de voz (cláusula anti-IA).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

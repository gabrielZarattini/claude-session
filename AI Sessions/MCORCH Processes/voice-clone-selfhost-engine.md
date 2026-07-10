# SOP — Motor self-host de clone de voz (Qwen3-TTS 0.6B, custo US$ 0)

> **Lei 2 (Anticipated Process)** — este SOP fecha o gate nomeado no FR-SPACES-053
> (Amendment 17, spaces-evolution): *"SOP de hosting (Lei 2) antes de deployar o motor"*.
> Escrito ANTES do deploy durável do motor. Witness test executado 2026-07-09.
>
> **Decisão de motor (fundamentada em witness material):** `Qwen3-TTS-12Hz-0.6B-Base`
> (Apache-2.0 código+pesos, verificado na API HF; clone zero-shot ~3s; pt oficial)
> rodando no engine C `gabriele-mastrapasqua/qwen3-tts` (MIT, NEON+SDOT ARM).
> O VoxCPM2 selado no FR-SPACES-053 revelou-se **2B params** (a memória do projeto
> registrava o 0.5B legacy de 2025) — RTF estimado 15–40 no host CPU-only vs
> **RTF 6,4 medido** do Qwen3 0.6B INT8. VoxCPM2 fica como candidato pós-GPU.
> Emenda BoK correspondente: `docs/bok/spaces-evolution/18-amendment-voice-engine-selfhost.md`.

---

## Witness de referência (Lei 1 — números medidos no host, 2026-07-09)

| Métrica | Valor medido |
|---|---|
| Host | Oracle aarch64 Neoverse-N1, 4 vCPU, sem GPU, 23 GB RAM |
| Build | `make blas` (OpenBLAS via apt) → binário `qwen_tts` 556 KB |
| Modelo | `Qwen/Qwen3-TTS-12Hz-0.6B-Base` BF16, 2,4 GB no disco |
| Clone | referência pt 11,6 s (24 kHz mono WAV) → síntese pt-BR 15,12 s |
| Wall clock | 97,3 s com `--int8` → **RTF 6,4** (1 min de áudio ≈ 6,4 min) |
| RAM pico | 3,15 GB (RSS) |
| Áudio | mean_volume −19,6 dB / max −2,9 dB (sinal real, não silêncio) |

Implicação de produto: **batch/assíncrono apenas** (fila + worker, molde `video-bridge`).
Streaming/realtime = pós-GPU (doutrina paid-pós-renda).

## Operator

Hoje: MCORCH Master Execution Agent (deploy) + Sovereign (veredito auditivo de qualidade).
Futuro: worker `voice-bridge` autônomo no mesmo molde do `video-bridge.ts`.

## Sequence (deploy do motor no host)

1. **Dependências** — `sudo apt-get install -y libopenblas-dev` (ffmpeg já presente).
   *Sucesso:* `ldconfig -p | grep openblas` retorna a lib.
2. **Engine** — clonar `https://github.com/gabriele-mastrapasqua/qwen3-tts` (MIT) em
   `/home/ubuntu/.mcorch/voice-engine/engine/` e compilar: `make blas -j4`.
   *Sucesso:* binário `qwen_tts` existe, `./qwen_tts --help` sai 0.
3. **Modelo** — `./download_model.sh --model base-small` (baixa
   `Qwen/Qwen3-TTS-12Hz-0.6B-Base` → `qwen3-tts-0.6b-base/`, 2,4 GB).
   *Sucesso:* `model.safetensors` presente, `du -sh` ≈ 2,4 G.
4. **Smoke de clone** — converter uma referência para 24 kHz mono
   (`ffmpeg -i ref.ext -ar 24000 -ac 1 ref24k.wav`) e rodar:
   `./qwen_tts -d qwen3-tts-0.6b-base --ref-audio ref24k.wav -l Portuguese --int8 --text "<frase pt-BR>" -o out.wav`.
   *Sucesso:* exit 0 + `ffprobe` mostra duração coerente + `volumedetect` com sinal
   (mean_volume > −40 dB). **Ouvir o áudio** (Vision/ocular auditivo) antes de declarar qualidade.
5. **Perfil de voz portátil (opcional, recomendado p/ produção)** — salvar
   `--save-voice voices/<user>.bin --xvector-only` (8 KB, identidade sem reverb da sala)
   a partir da referência; jobs futuros usam `--load-voice` (pula re-encode da referência).
6. **NUNCA** subir o servidor HTTP (`--serve`) exposto: sem auth nativa e a voz clonada
   é fixada no start (inadequado multi-tenant). Se um servidor local for necessário,
   bind loopback + só via worker/proxy autenticado.

## Verification gates

- **G1 build:** `qwen_tts` linka com `-lopenblas` (ver linha final do make).
- **G2 modelo:** sha/size do `model.safetensors` e `du -sh` ≈ 2,4 G.
- **G3 síntese:** exit 0 + WAV com duração > 0 e volume real (não-silêncio).
- **G4 qualidade:** veredito auditivo humano (Sovereign) OU Vision QA de áudio quando existir.
- **G5 RTF:** wall/duração ≤ 10 no host atual — acima disso, investigar
  (CPU roubada por vizinhos? ver context switches involuntários no `/usr/bin/time -v`).
- **G6 consent (integração produto):** QUALQUER caminho de clone — inclusive grátis —
  passa pelo gate `avatar_consents` purpose=`voice_clone` (LGPD Art. 11, FR-AC-030).
  Motor grátis NÃO dispensa consent: voiceprint é biometria.

## Recovery path

- Build falha por BLAS ausente → passo 1; por flags ARM → `make clean && make blas` (o
  Makefile detecta NEON; nunca editar `-march` na mão).
- Download interrompido → re-rodar `download_model.sh` (retoma via huggingface).
- Síntese sai lixo/ruído → 99% referência com sample rate errado: re-converter a
  24 kHz (G4 do doc oficial: "mismatched sample rate produces bad voice embedding").
- RTF explode (>15) → checar `nproc` disponível e carga (`uptime`); rodar com `nice -n 10`
  se competindo com video-bridge; jobs de voz e vídeo NÃO devem rodar simultâneos no
  host 4-core (serializar na fila).
- OOM (improvável, pico 3,15 GB) → garantir 1 job de voz por vez (lock no worker).

## Success signal

WAV pt-BR clonado audível gerado no host com custo externo US$ 0, exit 0, sinal real
no volumedetect, e RTF ≤ 10 registrado. Para o fluxo de produto completo: linha na fila
processada → WAV no bucket privado → signed URL tocável no nó Clone de Voz → registro
em `creative_assets` — mesmo contrato do rail `video-bridge`.

## Integração de produto (próxima fatia — gates próprios)

- Fila + worker `voice-bridge` (molde `scripts/video-bridge.ts`): claim atômico →
  CLI qwen_tts → upload bucket privado → finalize RPC → poll do nó.
- `generate-voice` ganha provider `qwen3-local` custo **0 mco** (por enquanto — decisão
  Sovereign "tudo grátis"; recalibrar via `mcoin-cost-calibration.md` quando monetizar).
- Migration: alargar CHECK `provider` em `voice_profiles` + guard do RPC
  `store_voice_profile` (**/security-review obrigatório**, FMEA-011).
- O gate BYOK fail-closed ganha bypass EXPLÍCITO só para engines keyless locais.

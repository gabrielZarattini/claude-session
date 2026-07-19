# SOP — ASR self-host: master de vídeo → SRT (whisper.cpp, US$ 0)

> **Por que existe (Lei 2):** o detector de momentos virais (`detect-viral-moments`, FR-VR-010) é transcript-gated — sem SRT, 422. Masters ingeridos crus (ex.: EP01 host-local) não têm transcript. Esta SOP funda o motor ASR self-host que fecha a **OTD-VR-012** (GO Sovereign 2026-07-13: "se você conseguir gerar [as legendas] e colocar junto com os outros"). Doutrina: open-source-first, custo externo US$ 0 ([[feedback_opensource_first_zero_cost_equity]]).
>
> **ORO:** Operator = MCORCH Master Execution Agent (manual hoje; automação = fatia UI/edge posterior) · Reviewer = Sovereign (confere o SRT gerado) · Owner = Sovereign (blast radius: disco/CPU do host; zero custo externo).

## Motor

| Item | Valor |
|---|---|
| Engine | `whisper.cpp` (MIT, ggml-org) — build nativo ARM64 NEON, `make -j4` |
| Local | `/home/ubuntu/.mcorch/asr-engine/whisper.cpp/` (irmão do `voice-engine`, convenção `~/.mcorch/`) |
| Modelo | `ggml-large-v3-turbo-q5_0.bin` (~574 MB, HuggingFace ggerganov/whisper.cpp) — melhor custo/qualidade pt-BR em CPU |
| Custo | US$ 0 (CPU do host; 4 cores Ampere) |

## Operator — quem executa manualmente hoje
O agente (ou o Sovereign) no host, usuário `ubuntu`.

## Sequence (cada passo com critério material)

1. **Extrair áudio 16 kHz mono** (formato que o whisper espera):
   ```bash
   ffmpeg -y -i <master.mp4> -vn -ar 16000 -ac 1 -c:a pcm_s16le /tmp/<ep>-audio.wav
   ```
   ✅ `ffprobe duration` do WAV ≈ duração do master (±0,5s).
2. **Transcrever com timestamps SRT**:
   ```bash
   cd /home/ubuntu/.mcorch/asr-engine/whisper.cpp
   ./build/bin/whisper-cli -m models/ggml-large-v3-turbo-q5_0.bin \
     -f /tmp/<ep>-audio.wav -l pt -osrt -of /tmp/<ep>-pt-BR -t 4
   ```
   ✅ arquivo `/tmp/<ep>-pt-BR.srt` existe, >20 cues, timestamps crescentes, último timestamp ≈ duração.
3. **Depositar na convenção do projeto**: copiar para `video-studio/GabrielAI/legendas/<ep>-pt-BR.srt` (mesmo formato dos SRTs subidos pelo Sovereign).
4. **Semear o asset**: gravar o conteúdo em `creative_assets.metadata.srt.pt` do master correspondente (é o que o `detect-viral-moments` lê).
   ✅ `SELECT length(metadata->'srt'->>'pt')` > 1000.

## Verification gates
- **G1 sanidade**: nº de cues plausível (~1 cue/5-8s de fala) e texto em pt-BR coerente com o episódio.
- **G2 spot-check auditivo/leitura** (Reviewer): Sovereign lê 3 cues aleatórias vs o vídeo — se a transcrição estiver errada em conteúdo, NÃO alimentar o detector (lixo entra, lixo viraliza).
- **G3 detector**: `detect-viral-moments` (ou harness) roda sem 422 e retorna janelas 15-45s.

## Recovery
- **Build falha** (`make` erro): faltam headers → `sudo apt install build-essential`; ARM já é NEON-auto.
- **Transcrição vazia/curta**: conferir WAV (16 kHz mono? duração certa?); re-extrair. Áudio muito música/pouca fala → normal ter poucas cues.
- **pt errado (detectou outro idioma)**: forçar `-l pt` (já no comando); se persistir, modelo corrompido → re-download (sha no HF).
- **OOM/lento**: q5_0 usa ~1 GB RAM; se estourar, cair para `ggml-medium-q5_0`.

## Success signal
`video-studio/GabrielAI/legendas/<ep>-pt-BR.srt` presente + `metadata.srt.pt` do master populado + detector retornando cortes reais do episódio.

## Camada 2 — Reconciliação roteiro-autoritativa (Diretiva Sovereign 2026-07-13)

**Doutrina:** "sempre temos o roteiro original… o áudio pode realmente ser gerado errado — é um gargalo da IA generativa de vídeo. Para a legenda manteremos o original." O Whisper dá o **timing real** do master final; o **roteiro dá o texto**. A reconciliação casa os dois:

1. Obter a narração do episódio do repo `gabrielZarattini/GabrielAI` (privado — acesso via **GitHub MCP** `get_file_contents` em `roteiro/epNN-*.md`; clone https falha sem credencial no host). Extrair as falas (`Brazilian Portuguese: '…'`) na ordem das cenas → JSON lista de strings (ex.: `video-studio/GabrielAI/roteiro-ep01-narracao.json`).
2. Rodar `python3 scripts/video-repurpose/reconcile-srt-roteiro.py <legendas/epNN-pt-BR.srt> <narracao.json>` — alinha palavra-a-palavra (difflib normalizado, molde do `gerar_srt.py` do próprio repo GabrielAI, invertido), **substitui o texto das cues casadas pelo roteiro** e **preserva as cues sem roteiro** (intro/cartelas adicionadas na edição).
3. Re-semear `metadata.srt.pt` do master.

**Prova EP01 (2026-07-13):** 707/752 palavras alinhadas (94%); ~30 cues reescritas (recuperou o `"Incrível."` que o áudio/Whisper perdeu; `Austin→Boston Dynamics`; pontuação canônica); intro "2026 não trouxe carros voadores…" (fora do roteiro — cartela de edição) preservada do Whisper. Episódios do pipeline GabrielAI COM `timings.json`: preferir o `gerar_srt.py` canônico do próprio repo; esta reconciliação cobre os que não têm (ep01) e masters externos.

## Automação prevista (fatias seguintes — só depois desta SOP, Lei 2)
1. **UI (admin front-door `/dashboard/repurpose`)**: campo de upload de SRT junto do master (grava em `metadata.srt`) + botão **"Gerar legendas"** quando não houver SRT.
2. **Rail assíncrono**: fila `video_renders` engine `asr` (molde `qwen3-voice`/`repurpose`) — worker host roda whisper.cpp e semeia `metadata.srt`; edge fn `generate-subtitles` enfileira (JWT, owner-scoped, admin p/ bucket local). `/security-review` obrigatório.
3. EN opcional (`-l en` ou tradução) — fatia posterior.

**Cross-links:** `docs/bok/video-repurpose/10-frd-sdd-viral-quality.md` (OTD-VR-012) · [[project_video_repurpose_engine]] · `docs/processes/voice-clone-selfhost-engine.md` (irmão de engine self-host).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

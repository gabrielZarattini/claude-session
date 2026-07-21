---
type: session-stub
archived: true
original_size_bytes: 1677734
original_size: 1.6 MB
date: 2026-07-16
session_id: d6ec7e6b-7ebd-46be-9065-173b91242b97
full_path: _full-sessions/ClaudeSessions/2026-07-16 - Configurar loop e blueprint do video-repurposeyoutube-studio.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-07-16%20-%20Configurar%20loop%20e%20blueprint%20do%20video-repurposeyoutube-studio.md
---

# Configurar loop e blueprint do video-repurpose/youtube-studio

> [!abstract] Sessao arquivada
> O conteudo completo (**1.6 MB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-07-16%20-%20Configurar%20loop%20e%20blueprint%20do%20video-repurposeyoutube-studio.md)**

- **Data:** 2026-07-16
- **Session ID:** `d6ec7e6b-7ebd-46be-9065-173b91242b97`
- **Tamanho original:** 1.6 MB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-07-16 - Configurar loop e blueprint do video-repurposeyoutube-studio.md`

## Roteiro da sessao

- Execute the ShakeHands /handson ritual for this project.
- otimo pode armar o loop para atacar os próximos passos, além disso me mostre o blueprint e suas recomendações 
- <task-notification>

## Previa

> # Configurar loop e blueprint do video-repurpose/youtube-studio
> **Date:** 2026-07-16 | **Session ID:** `d6ec7e6b-7ebd-46be-9065-173b91242b97`
> 
> ---
> 
> ## 👤 User *(13:07:54)*
> 
> <command-message>handson</command-message>
> <command-name>/handson</command-name>
> 
> ## 👤 User *(13:07:54)*
> 
> # ShakeHands — Session Pick-Up Protocol v3
> 
> Execute the ShakeHands /handson ritual for this project.
> 
> > **v3 (2026-05-08):** Added BoK Gate enforcement per MCORCH Master Execution Protocol — alert when active module work has no sealed BoK suite at `docs/bok/<slug>/`.
> 
> ---
> 
> ## PRE-FLIGHT (execute ALL in parallel before reading anything)
> 
> ```bash
> git log --oneline -7                        # recent history + commit style
> git status --short                          # uncommitted changes
> git diff HEAD --stat                        # change scope
> npx tsc --noEmit 2>&1 | tail -20           # TypeScript strict check
> docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
> docker ps --filter "name=mega-brain" --format "{{.Names}}: {{.Status}}"
> curl -s http://localhost:8001/api/v2/heartbeat  # Chroma API v2 health
> ls docs/bok/ 2>/dev/null                    # BoK suites disponíveis
> wc -l HANDOFF.md                            # total lines — drives the read-from-end offset
> ```
> 
> Read in parallel (HANDOFF.md uses **read-from-end strategy** — SSP-01 v6.5.0; arquivo monolítico newest-first em ~3170+ linhas, leitura completa estoura limite de 25k tokens):

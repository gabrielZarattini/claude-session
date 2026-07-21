---
type: session-stub
archived: true
original_size_bytes: 1807722
original_size: 1.7 MB
date: 2026-07-14
session_id: 3fbbb6af-3584-4892-bd6f-cbd316268334
full_path: _full-sessions/ClaudeSessions/2026-07-14 - Criar loop de vídeos com avatar no Vertex AI.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-07-14%20-%20Criar%20loop%20de%20v%C3%ADdeos%20com%20avatar%20no%20Vertex%20AI.md
---

# Criar loop de vídeos com avatar no Vertex AI

> [!abstract] Sessao arquivada
> O conteudo completo (**1.7 MB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-07-14%20-%20Criar%20loop%20de%20v%C3%ADdeos%20com%20avatar%20no%20Vertex%20AI.md)**

- **Data:** 2026-07-14
- **Session ID:** `3fbbb6af-3584-4892-bd6f-cbd316268334`
- **Tamanho original:** 1.7 MB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-07-14 - Criar loop de vídeos com avatar no Vertex AI.md`

## Roteiro da sessao

- Execute the ShakeHands /handson ritual for this project.
- otimo brand ja pubiicado no google. arme o loop para os proximos passos. Foco total na criacao dos videos com 
- Parse the input below into `[interval] <prompt…>` and schedule it.

## Previa

> # [[2026-07-15 - Criar loop de vídeos com avatar no Vertex AI|Criar loop de vídeos com avatar no Vertex AI]]
> **Date:** 2026-07-14 | **Session ID:** `3fbbb6af-3584-4892-bd6f-cbd316268334`
> 
> ---
> 
> ## 👤 User *(20:29:20)*
> 
> <command-message>handson</command-message>
> <command-name>/handson</command-name>
> 
> ## 👤 User *(20:29:20)*
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

---
type: session-stub
archived: true
original_size_bytes: 709697
original_size: 693 KB
date: 2026-06-03
session_id: cbb758a7-048b-4acb-94aa-db05a445f1e7
full_path: _full-sessions/ClaudeSessions/2026-06-03 - Design agentic marketing framework for universal platforms.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-03%20-%20Design%20agentic%20marketing%20framework%20for%20universal%20platforms.md
---

# Design agentic marketing framework for universal platforms

> [!abstract] Sessao arquivada
> O conteudo completo (**693 KB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-03%20-%20Design%20agentic%20marketing%20framework%20for%20universal%20platforms.md)**

- **Data:** 2026-06-03
- **Session ID:** `cbb758a7-048b-4acb-94aa-db05a445f1e7`
- **Tamanho original:** 693 KB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-06-03 - Design agentic marketing framework for universal platforms.md`

## Roteiro da sessao

- Execute the ShakeHands /handson ritual for this project.
- You are the **MCORCH BoK Scribe Agent** — the Requirements Engineering layer of the MCORCH

## Previa

> # Design agentic marketing framework for universal platforms
> **Date:** 2026-06-03 | **Session ID:** `cbb758a7-048b-4acb-94aa-db05a445f1e7`
> 
> ---
> 
> ## 👤 User *(00:06:38)*
> 
> <command-message>handson</command-message>
> <command-name>/handson</command-name>
> 
> ## 👤 User *(00:06:38)*
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

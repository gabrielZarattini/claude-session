---
type: session-stub
archived: true
original_size_bytes: 670963
original_size: 655 KB
date: 2026-05-20
session_id: 9b35297a-7383-43a7-97d8-76e2e5a5f90a
full_path: _full-sessions/ClaudeSessions/2026-05-20 - Prioritize circadian cycle setup and Ollama configuration.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-05-20%20-%20Prioritize%20circadian%20cycle%20setup%20and%20Ollama%20configuration.md
---

# Prioritize circadian cycle setup and Ollama configuration

> [!abstract] Sessao arquivada
> O conteudo completo (**655 KB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-05-20%20-%20Prioritize%20circadian%20cycle%20setup%20and%20Ollama%20configuration.md)**

- **Data:** 2026-05-20
- **Session ID:** `9b35297a-7383-43a7-97d8-76e2e5a5f90a`
- **Tamanho original:** 655 KB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-05-20 - Prioritize circadian cycle setup and Ollama configuration.md`

## Roteiro da sessao

- Execute the ShakeHands /handson ritual for this project.
- ótimo vamos atar as prioridades primeiro e aproveite para analisar o morning de hoje.:
- You are the **MCORCH BoK Scribe Agent** — the Requirements Engineering layer of the MCORCH

## Previa

> # Prioritize circadian cycle setup and Ollama configuration
> **Date:** 2026-05-20 | **Session ID:** `9b35297a-7383-43a7-97d8-76e2e5a5f90a`
> 
> ---
> 
> ## 👤 User *(12:50:48)*
> 
> <command-message>handson</command-message>
> <command-name>/handson</command-name>
> 
> ## 👤 User *(12:50:48)*
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

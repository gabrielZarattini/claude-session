---
type: session-stub
archived: true
original_size_bytes: 613275
original_size: 599 KB
date: 2026-05-18
session_id: a1af509e-9cda-4561-8133-70c66eaeff56
full_path: _full-sessions/ClaudeSessions/2026-05-18 - Admin JWT validation and system health verification.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-05-18%20-%20Admin%20JWT%20validation%20and%20system%20health%20verification.md
---

# Admin JWT validation and system health verification

> [!abstract] Sessao arquivada
> O conteudo completo (**599 KB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-05-18%20-%20Admin%20JWT%20validation%20and%20system%20health%20verification.md)**

- **Data:** 2026-05-18
- **Session ID:** `a1af509e-9cda-4561-8133-70c66eaeff56`
- **Tamanho original:** 599 KB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-05-18 - Admin JWT validation and system health verification.md`

## Roteiro da sessao

- Execute the ShakeHands /handson ritual for this project.

## Previa

> # Admin JWT validation and system health verification
> **Date:** 2026-05-18 | **Session ID:** `a1af509e-9cda-4561-8133-70c66eaeff56`
> 
> ---
> 
> ## 👤 User *(04:32:34)*
> 
> <command-message>handson</command-message>
> <command-name>/handson</command-name>
> 
> ## 👤 User *(04:32:34)*
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

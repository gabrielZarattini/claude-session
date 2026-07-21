---
type: session-stub
archived: true
original_size_bytes: 640574
original_size: 626 KB
date: 2026-05-19
session_id: 731718a9-4abd-4afd-8801-17d295656326
full_path: _full-sessions/ClaudeSessions/2026-05-19 - Provision ML affiliate token before E2E tests.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-05-19%20-%20Provision%20ML%20affiliate%20token%20before%20E2E%20tests.md
---

# Provision ML affiliate token before E2E tests

> [!abstract] Sessao arquivada
> O conteudo completo (**626 KB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-05-19%20-%20Provision%20ML%20affiliate%20token%20before%20E2E%20tests.md)**

- **Data:** 2026-05-19
- **Session ID:** `731718a9-4abd-4afd-8801-17d295656326`
- **Tamanho original:** 626 KB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-05-19 - Provision ML affiliate token before E2E tests.md`

## Roteiro da sessao

- Execute the ShakeHands /handson ritual for this project.

## Previa

> # Provision ML affiliate token before E2E tests
> **Date:** 2026-05-19 | **Session ID:** `731718a9-4abd-4afd-8801-17d295656326`
> 
> ---
> 
> ## 👤 User *(12:37:41)*
> 
> <command-message>handson</command-message>
> <command-name>/handson</command-name>
> 
> ## 👤 User *(12:37:41)*
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

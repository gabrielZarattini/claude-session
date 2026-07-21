---
type: session-stub
archived: true
original_size_bytes: 1674368
original_size: 1.6 MB
date: 2026-07-14
session_id: 0a229b55-ae24-4239-96c6-b85f48538d9b
full_path: _full-sessions/ClaudeSessions/2026-07-14 - Fix alerts and optimize viral video clips.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-07-14%20-%20Fix%20alerts%20and%20optimize%20viral%20video%20clips.md
---

# Fix alerts and optimize viral video clips

> [!abstract] Sessao arquivada
> O conteudo completo (**1.6 MB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-07-14%20-%20Fix%20alerts%20and%20optimize%20viral%20video%20clips.md)**

- **Data:** 2026-07-14
- **Session ID:** `0a229b55-ae24-4239-96c6-b85f48538d9b`
- **Tamanho original:** 1.6 MB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-07-14 - Fix alerts and optimize viral video clips.md`

## Roteiro da sessao

- Execute the ShakeHands /handson ritual for this project.
- ótimo agora que ja temos os cortes, precisamos fixar todos os alertas antes de começar a melhorar a qualidade 
- Parse the input below into `[interval] <prompt…>` and schedule it.
- Parse the input below into `[interval] <prompt…>` and schedule it.
- Parse the input below into `[interval] <prompt…>` and schedule it.

## Previa

> # [[2026-07-13 - Fix alerts and optimize viral video clips|Fix alerts and optimize viral video clips]]
> **Date:** 2026-07-14 | **Session ID:** `0a229b55-ae24-4239-96c6-b85f48538d9b`
> 
> ---
> 
> ## 👤 User *(12:42:57)*
> 
> <command-message>handson</command-message>
> <command-name>/handson</command-name>
> 
> ## 👤 User *(12:42:57)*
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

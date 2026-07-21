---
type: session-stub
archived: true
original_size_bytes: 1206011
original_size: 1.2 MB
date: 2026-07-08
session_id: 0040fea6-03c6-4785-867c-7c9249855765
full_path: _full-sessions/ClaudeSessions/2026-07-08 - Montar loop para próximos passos.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-07-08%20-%20Montar%20loop%20para%20pr%C3%B3ximos%20passos.md
---

# Montar loop para próximos passos

> [!abstract] Sessao arquivada
> O conteudo completo (**1.2 MB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-07-08%20-%20Montar%20loop%20para%20pr%C3%B3ximos%20passos.md)**

- **Data:** 2026-07-08
- **Session ID:** `0040fea6-03c6-4785-867c-7c9249855765`
- **Tamanho original:** 1.2 MB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-07-08 - Montar loop para próximos passos.md`

## Roteiro da sessao

- Execute the ShakeHands /handson ritual for this project.
- ótimo pode armar o loop para os próximos passsos
- Parse the input below into `[interval] <prompt…>` and schedule it.
- <task-notification>
- <task-notification>
- <task-notification>

## Previa

> # [[2026-07-14 - Montar loop para próximos passos|Montar loop para próximos passos]]
> **Date:** 2026-07-08 | **Session ID:** `0040fea6-03c6-4785-867c-7c9249855765`
> 
> ---
> 
> ## 👤 User *(02:19:55)*
> 
> <command-message>handson</command-message>
> <command-name>/handson</command-name>
> 
> ## 👤 User *(02:19:55)*
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

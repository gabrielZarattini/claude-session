---
type: session-stub
archived: true
original_size_bytes: 930444
original_size: 909 KB
date: 2026-07-09
session_id: 47592365-463d-4669-b674-a8aa2fcecacf
full_path: _full-sessions/ClaudeSessions/2026-07-09 - Configurar API de créditos e testar MCP com TikTok.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-07-09%20-%20Configurar%20API%20de%20cr%C3%A9ditos%20e%20testar%20MCP%20com%20TikTok.md
---

# Configurar API de créditos e testar MCP com TikTok

> [!abstract] Sessao arquivada
> O conteudo completo (**909 KB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-07-09%20-%20Configurar%20API%20de%20cr%C3%A9ditos%20e%20testar%20MCP%20com%20TikTok.md)**

- **Data:** 2026-07-09
- **Session ID:** `47592365-463d-4669-b674-a8aa2fcecacf`
- **Tamanho original:** 909 KB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-07-09 - Configurar API de créditos e testar MCP com TikTok.md`

## Roteiro da sessao

- Execute the ShakeHands /handson ritual for this project.
- Parece que agora ta funcionando o MCP mas só funciona com assinaturas e eu não tenho, tenho somente a API com 
- Parse the input below into `[interval] <prompt…>` and schedule it.

## Previa

> # Configurar API de créditos e testar MCP com TikTok
> **Date:** 2026-07-09 | **Session ID:** `47592365-463d-4669-b674-a8aa2fcecacf`
> 
> ---
> 
> ## 👤 User *(23:38:25)*
> 
> <command-message>handson</command-message>
> <command-name>/handson</command-name>
> 
> ## 👤 User *(23:38:25)*
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

---
type: session-stub
archived: true
original_size_bytes: 1831913
original_size: 1.7 MB
date: 2026-06-10
session_id: 240db21b-cd40-4765-a3f4-345f03d2fc33
full_path: _full-sessions/ClaudeSessions/2026-06-10 - Refactor Core-v2 to Core-Fable.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-10%20-%20Refactor%20Core-v2%20to%20Core-Fable.md
---

# Refactor Core-v2 to Core-Fable

> [!abstract] Sessao arquivada
> O conteudo completo (**1.7 MB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-10%20-%20Refactor%20Core-v2%20to%20Core-Fable.md)**

- **Data:** 2026-06-10
- **Session ID:** `240db21b-cd40-4765-a3f4-345f03d2fc33`
- **Tamanho original:** 1.7 MB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-06-10 - Refactor Core-v2 to Core-Fable.md`

## Roteiro da sessao

- Execute the ShakeHands /handson ritual for this project.
- Refatore todo o nosso Core-v2 para Core-Fable - https://login.mcorch.com/dashboard/core-v2
- [Request interrupted by user]
- Refatore todo o nosso Core-v2 para Core-Fable - https://login.mcorch.com/dashboard/core-v2
- Base directory for this skill: /tmp/claude-1001/bundled-skills/2.1.170/6d19fd6839b2e00e4eeec5033f0cf4df/claude

## Previa

> # Refactor Core-v2 to Core-Fable
> **Date:** 2026-06-10 | **Session ID:** `240db21b-cd40-4765-a3f4-345f03d2fc33`
> 
> ---
> 
> ## 👤 User *(01:40:53)*
> 
> <command-message>handson</command-message>
> <command-name>/handson</command-name>
> 
> ## 👤 User *(01:40:53)*
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

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-10 - Generate security BoK documentation suite]]
> * **Próxima Sessão**: [[2026-06-10 - agent-a01a722fbf80b27c5]]
%% --- TIMELINE END --- %%

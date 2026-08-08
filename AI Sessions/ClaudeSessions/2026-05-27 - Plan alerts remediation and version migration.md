---
type: session-stub
archived: true
original_size_bytes: 375712
original_size: 367 KB
date: 2026-05-27
session_id: ab2023b0-60af-44c6-9667-a2028a514d98
full_path: _full-sessions/ClaudeSessions/2026-05-27 - Plan alerts remediation and version migration.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-05-27%20-%20Plan%20alerts%20remediation%20and%20version%20migration.md
---

# Plan alerts remediation and version migration

> [!abstract] Sessao arquivada
> O conteudo completo (**367 KB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-05-27%20-%20Plan%20alerts%20remediation%20and%20version%20migration.md)**

- **Data:** 2026-05-27
- **Session ID:** `ab2023b0-60af-44c6-9667-a2028a514d98`
- **Tamanho original:** 367 KB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-05-27 - Plan alerts remediation and version migration.md`

## Roteiro da sessao

- Execute the ShakeHands /handson ritual for this project.
- ótimo agora crie um plano robusto para continue atacando todos os alertas e os primeiros passos. E tambem se a

## Previa

> # Plan alerts remediation and version migration
> **Date:** 2026-05-27 | **Session ID:** `ab2023b0-60af-44c6-9667-a2028a514d98`
> 
> ---
> 
> ## 👤 User *(16:55:16)*
> 
> <command-message>handson</command-message>
> <command-name>/handson</command-name>
> 
> ## 👤 User *(16:55:16)*
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
> * **Sessão Anterior**: [[2026-05-27 - Plan JWT refactor and affiliate token migration]]
> * **Próxima Sessão**: [[2026-05-27 - ab2023b0-60af-44c6-9667-a2028a514d98]]
%% --- TIMELINE END --- %%

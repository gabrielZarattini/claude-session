---
type: session-stub
archived: true
original_size_bytes: 439698
original_size: 429 KB
date: 2026-05-27
session_id: cf433bf4-1fe3-4e97-93c9-a8cd46e57779
full_path: _full-sessions/ClaudeSessions/2026-05-27 - Plan JWT refactor and affiliate token migration.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-05-27%20-%20Plan%20JWT%20refactor%20and%20affiliate%20token%20migration.md
---

# [[2026-05-28 - Plan JWT refactor and affiliate token migration|Plan JWT refactor and affiliate token migration]]

> [!abstract] Sessao arquivada
> O conteudo completo (**429 KB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-05-27%20-%20Plan%20JWT%20refactor%20and%20affiliate%20token%20migration.md)**

- **Data:** 2026-05-27
- **Session ID:** `cf433bf4-1fe3-4e97-93c9-a8cd46e57779`
- **Tamanho original:** 429 KB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-05-27 - Plan JWT refactor and affiliate token migration.md`

## Roteiro da sessao

- Execute the ShakeHands /handson ritual for this project.
- Vamos lá defina a melhor ordem e crie o plano robusto e sofisticado.: ⚡ PRÓXIMOS PASSOS (prioridade)

## Previa

> # [[2026-05-28 - Plan JWT refactor and affiliate token migration|Plan JWT refactor and affiliate token migration]]
> **Date:** 2026-05-27 | **Session ID:** `cf433bf4-1fe3-4e97-93c9-a8cd46e57779`
> 
> ---
> 
> ## 👤 User *(20:05:30)*
> 
> <command-message>handson</command-message>
> <command-name>/handson</command-name>
> 
> ## 👤 User *(20:05:30)*
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
> * **Sessão Anterior**: [[2026-05-27 - 98202356-feef-4f6b-9631-acfe0d7e685d]]
> * **Próxima Sessão**: [[2026-05-27 - Plan alerts remediation and version migration]]
%% --- TIMELINE END --- %%

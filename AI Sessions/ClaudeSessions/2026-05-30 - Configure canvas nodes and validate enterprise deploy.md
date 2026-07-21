---
type: session-stub
archived: true
original_size_bytes: 737924
original_size: 721 KB
date: 2026-05-30
session_id: 85f69640-5d2b-4e0a-91fa-c8f92df1818a
full_path: _full-sessions/ClaudeSessions/2026-05-30 - Configure canvas nodes and validate enterprise deploy.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-05-30%20-%20Configure%20canvas%20nodes%20and%20validate%20enterprise%20deploy.md
---

# Configure canvas nodes and validate enterprise deploy

> [!abstract] Sessao arquivada
> O conteudo completo (**721 KB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-05-30%20-%20Configure%20canvas%20nodes%20and%20validate%20enterprise%20deploy.md)**

- **Data:** 2026-05-30
- **Session ID:** `85f69640-5d2b-4e0a-91fa-c8f92df1818a`
- **Tamanho original:** 721 KB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-05-30 - Configure canvas nodes and validate enterprise deploy.md`

## Roteiro da sessao

- Execute the ShakeHands /handson ritual for this project.
- Vamos aos proximos passos sim a chave de ML AFFILIATE TOKEN deve ser per user;
- Continue from where you left off.
- Vamos aos proximos passos sim a chave de ML AFFILIATE TOKEN deve ser per user;

## Previa

> # Configure canvas nodes and validate enterprise deploy
> **Date:** 2026-05-30 | **Session ID:** `85f69640-5d2b-4e0a-91fa-c8f92df1818a`
> 
> ---
> 
> ## 👤 User *(01:30:31)*
> 
> <command-message>handson</command-message>
> <command-name>/handson</command-name>
> 
> ## 👤 User *(01:30:31)*
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
> * **Sessão Anterior**: [[2026-05-30 - 0fb17c7c-3e60-44a1-b426-8966b708f3dc]]
> * **Próxima Sessão**: [[2026-05-30 - Fix API key leak and reconfigure model defaults]]
%% --- TIMELINE END --- %%

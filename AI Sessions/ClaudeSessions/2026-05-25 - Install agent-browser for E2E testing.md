---
type: session-stub
archived: true
original_size_bytes: 565533
original_size: 552 KB
date: 2026-05-25
session_id: 516091c3-851b-4aee-99cf-94d4940c0249
full_path: _full-sessions/ClaudeSessions/2026-05-25 - Install agent-browser for E2E testing.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-05-25%20-%20Install%20agent-browser%20for%20E2E%20testing.md
---

# [[2026-05-26 - Install agent-browser for E2E testing|Install agent-browser for E2E testing]]

> [!abstract] Sessao arquivada
> O conteudo completo (**552 KB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-05-25%20-%20Install%20agent-browser%20for%20E2E%20testing.md)**

- **Data:** 2026-05-25
- **Session ID:** `516091c3-851b-4aee-99cf-94d4940c0249`
- **Tamanho original:** 552 KB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-05-25 - Install agent-browser for E2E testing.md`

## Roteiro da sessao

- Execute the ShakeHands /handson ritual for this project.
- https://github.com/vercel-labs/agent-browser agora preciso que voce instale essea skill para fazer os testes E

## Previa

> # [[2026-05-26 - Install agent-browser for E2E testing|Install agent-browser for E2E testing]]
> **Date:** 2026-05-25 | **Session ID:** `516091c3-851b-4aee-99cf-94d4940c0249`
> 
> ---
> 
> ## 👤 User *(21:41:10)*
> 
> <command-message>handson</command-message>
> <command-name>/handson</command-name>
> 
> ## 👤 User *(21:41:10)*
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
> * **Sessão Anterior**: [[2026-05-25 - Fix OpenClaw cron job display issues]]
> * **Próxima Sessão**: [[2026-05-25 - Resolve alerts and execute OE-661 plan]]
%% --- TIMELINE END --- %%

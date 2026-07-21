---
type: session-stub
archived: true
original_size_bytes: 433391
original_size: 423 KB
date: 2026-06-27
session_id: f23f934d-28f6-402d-a438-cbc319022dfc
full_path: _full-sessions/ClaudeSessions/2026-06-27 - Corrigir erro de configuração TikTok.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-27%20-%20Corrigir%20erro%20de%20configura%C3%A7%C3%A3o%20TikTok.md
---

# Corrigir erro de configuração TikTok

> [!abstract] Sessao arquivada
> O conteudo completo (**423 KB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-27%20-%20Corrigir%20erro%20de%20configura%C3%A7%C3%A3o%20TikTok.md)**

- **Data:** 2026-06-27
- **Session ID:** `f23f934d-28f6-402d-a438-cbc319022dfc`
- **Tamanho original:** 423 KB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-06-27 - Corrigir erro de configuração TikTok.md`

## Roteiro da sessao

- Execute the ShakeHands /handson ritual for this project.
- tiktok_not_configured
- Entendi então eu tenho que criar o app me de o passo a passo e link oficial
- qual melhor opção?
- Description *
- App review
- Upload at least one demo video that shows the complete end-to-end flow of the integration with TikTok. *
- Test event sent
- tentei fazer o login clicando  conectar tiktok em dashboard/social/ ai deu erro na pagina que foi redirecionad
- Parece que para salvar ou enviar precisa do video
- <task-notification>
- Ficou só Products
- pronto agora Products
- video.publish
- pronto agora esta Products
- <task-notification>

## Previa

> # [[2026-06-28 - Corrigir erro de configuração TikTok|Corrigir erro de configuração TikTok]]
> **Date:** 2026-06-27 | **Session ID:** `f23f934d-28f6-402d-a438-cbc319022dfc`
> 
> ---
> 
> ## 👤 User *(17:43:44)*
> 
> <command-message>handson</command-message>
> <command-name>/handson</command-name>
> 
> ## 👤 User *(17:43:44)*
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

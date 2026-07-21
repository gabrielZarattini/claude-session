---
type: session-stub
archived: true
original_size_bytes: 352924
original_size: 345 KB
date: 2026-05-02
session_id: ff001393-c426-4734-b836-2cdbeff63c0f
full_path: _full-sessions/ClaudeSessions/2026-05-02 - Fix TTS bridge and resolve critical production issues.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-05-02%20-%20Fix%20TTS%20bridge%20and%20resolve%20critical%20production%20issues.md
---

# Fix TTS bridge and resolve critical production issues

> [!abstract] Sessao arquivada
> O conteudo completo (**345 KB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-05-02%20-%20Fix%20TTS%20bridge%20and%20resolve%20critical%20production%20issues.md)**

- **Data:** 2026-05-02
- **Session ID:** `ff001393-c426-4734-b836-2cdbeff63c0f`
- **Tamanho original:** 345 KB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-05-02 - Fix TTS bridge and resolve critical production issues.md`

## Roteiro da sessao

- Para fechar o ciclo e eu poder verificar em produção, o Code precisa executar no Oracle:
- O bundle principal tem o mesmo hash de antes (index-DzayATFU.js). O npm run build gerou os arquivos no dist/ m
- Execute the ShakeHands /handoff ritual to seal this session.

## Previa

> # Fix TTS bridge and resolve critical production issues
> **Date:** 2026-05-02 | **Session ID:** `ff001393-c426-4734-b836-2cdbeff63c0f`
> 
> ---
> 
> ## 👤 User *(21:40:43)*
> 
> # META-PROMPT — ShakeHands /handson v2
> # Handoff: AIOS Save Fix + TTS Bridge (v5.2.2)
> # Para: Claude Code / CLI (Braço de Engenharia)
> # Gerado por: Cowork (Usuário Zero) — 2026-05-02
> #
> # INSTRUÇÕES DE USO:
> # Cole este prompt integralmente no Claude Code CLI ao iniciar a sessão.
> # O Code irá executar o pré-voo, validar o handoff e produzir o brief.
> # ─────────────────────────────────────────────────────────────────────
> 
> Execute o protocolo ShakeHands /handson v2 para o projeto constellation-orchestra.
> Esta sessão valida o handoff selado v5.2.2-tts-bridge e incorpora achados críticos
> do agente Cowork (Usuário Zero) que testou em produção após o deploy.
> 
> ---
> 
> ## ETAPA 1 — PRÉ-VOO (execute TODO em paralelo)
> 
> ```bash
> cd /home/gcrUX/htdocs/constellation-orchestra
> 
> # Estado do repositório
> git log --oneline -7
> git status --short
> git diff HEAD --stat
> 
> # Validação de TypeScript
> npx tsc --noEmit 2>&1 | tail -20

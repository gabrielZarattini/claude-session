---
type: session-stub
archived: true
original_size_bytes: 2189691
original_size: 2.1 MB
date: 2026-07-05
session_id: agent-acbbab1d010adc9c5
full_path: _full-sessions/ClaudeSessions/2026-07-05 - agent-acbbab1d010adc9c5.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-07-05%20-%20agent-acbbab1d010adc9c5.md
---

# Session agent-acbbab1d010adc9c5

> [!abstract] Sessao arquivada
> O conteudo completo (**2.1 MB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-07-05%20-%20agent-acbbab1d010adc9c5.md)**

- **Data:** 2026-07-05
- **Session ID:** `agent-acbbab1d010adc9c5`
- **Tamanho original:** 2.1 MB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-07-05 - agent-acbbab1d010adc9c5.md`

## Roteiro da sessao

- Você é um agente de QA E2E validando o app MCORCH como o **Usuário Zero** (um usuário real logado), pós-rebran

## Previa

> # Session agent-acbbab1d010adc9c5
> **Date:** 2026-07-05 | **Session ID:** `agent-acbbab1d010adc9c5`
> 
> ---
> 
> ## 👤 User *(17:35:22)*
> 
> Você é um agente de QA E2E validando o app MCORCH como o **Usuário Zero** (um usuário real logado), pós-rebrand MIV. Dirige um navegador REAL via `agent-browser` contra um preview LOCAL (evita CF). Execute a JORNADA multi-step abaixo de ponta a ponta, tirando screenshots dos estados-chave, e **certifique**: o fluxo funciona E2E · a marca MIV se mantém · o texto é pt-BR · interações respondem · sem erro de console. Retorne objeto estruturado (schema forçado).
> 
> ## AMBIENTE
> - Preview: http://127.0.0.1:4180 · sessão agent-browser ÚNICA: `e2e-j7` · screenshots em /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/969f6e14-bf0b-42c0-9300-8707dcc8eb7f/scratchpad/e2e-shots (mkdir -p)
> - PATH: `export PATH="/home/ubuntu/.nvm/versions/node/v22.22.3/bin:$PATH"`
> 
> ## SETUP (uma vez)
> ```bash
> mkdir -p /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/969f6e14-bf0b-42c0-9300-8707dcc8eb7f/scratchpad/e2e-shots
> export PATH="/home/ubuntu/.nvm/versions/node/v22.22.3/bin:$PATH"
> agent-browser --session e2e-j7 set viewport 1920 1080
> agent-browser --session e2e-j7 open "http://127.0.0.1:4180/"
> B64=$(cat /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/969f6e14-bf0b-42c0-9300-8707dcc8eb7f/scratchpad/session.b64)
> agent-browser --session e2e-j7 eval "localStorage.setItem('sb-bcyvddsykvehvpwstlfa-auth-token', atob('$B64')); 'ok'"
> agent-browser --session e2e-j7 wait 1500
> ```
> (salve screenshots como /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/969f6e14-bf0b-42c0-9300-8707dcc8eb7f/scratchpad/e2e-shots/<nome-do-passo>.png)
> 
> ## ⛔ GUARDRAIL RÍGIDO — NUNCA GASTAR/MUTAR (backend PRODUÇÃO, dinheiro do Sovereign)
> NUNCA clique em ação paga/mutante: Rodar/Run, Gerar/Generate, Executar/Execute, Analisar e Otimizar, Executar Diagnóstico, Orquestrar, Publicar, Renderizar, Exportar, Enviar campanha, Pontuar, Rodar Teste de Estresse, Executar Prompt, Criar (submit), Deletar, Desconectar, Salvar credenciais, Assinar/checkout, Lançar Constelação, SYNC EMBEDDINGS, Zerar, +Tarefa(submit). ⛔ NO Minerador: NÃO clique nos cards (abre diálogo que dispara IA). PERMITIDO: navegar, hover, abrir dropdowns/abas/dialogs-de-ver (fechar com Escape), preencher campos (fill) SEM dar submit, expandir toggles de exibição. Na dúvida: hover + screenshot.
> 
> ## PROTOCOLO POR PASSO
> 1. Navegue/interaja conforme o passo. 2. Após carregar use o wait indicado (3D/canvas = mais longo). 3. Se um passo pede snapshot, use `agent-browser --session e2e-j7 snapshot -i` e ache o @eN pelo texto. 4. Screenshot no nome pedido. 5. `agent-browser --session e2e-j7 eval "location.pathname"` p/ confirmar rota (se caiu em /auth inesperado numa rota protegida = flow_works falso p/ o passo). 6. Ao fim: `agent-browser --session e2e-j7 get console-messages` e `agent-browser --session e2e-j7 close`.
> 
> ## CERTIFICAÇÃO (leia seus screenshots e julgue)
> - **flow_works**: cada passo completou, a rota certa carregou, nada quebrou/travou (canvas 3D mostra conteúdo, não branco/spinner infinito nem freeze).
> - **miv_conformant**: fundo void; acento/hover **cyan** (NÃO violeta — exceto o botão Memória, onde nebula é correto); **gold só em mcoCoins/valor**; Playfair nos títulos; JetBrains Mono no corpo; CTA com glow. Sinalize qualquer violeta genérico, gold decorativo, azul/laranja/rosa off-brand.
> - **ptbr_clean**: todo texto de UI em pt-BR (exceto nomes de marca/produto e identificadores técnicos). Liste strings em inglês achadas.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-07-05 - agent-ac5b74d0153e35024]]
> * **Próxima Sessão**: [[2026-07-05 - agent-adce11e3b05c91a52]]
%% --- TIMELINE END --- %%

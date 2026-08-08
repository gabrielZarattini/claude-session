---
type: session-stub
archived: true
original_size_bytes: 567290
original_size: 554 KB
date: 2026-06-08
session_id: a5c74064-c02c-4534-8380-0219a737b4b6
full_path: _full-sessions/ClaudeSessions/2026-06-08 - Sanitize AI-generated HTML in DashboardHome with DOMPurify.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-08%20-%20Sanitize%20AI-generated%20HTML%20in%20DashboardHome%20with%20DOMPurify.md
---

# [[2026-06-04 - Sanitize AI-generated HTML in DashboardHome with DOMPurify|Sanitize AI-generated HTML in DashboardHome with DOMPurify]]

> [!abstract] Sessao arquivada
> O conteudo completo (**554 KB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-08%20-%20Sanitize%20AI-generated%20HTML%20in%20DashboardHome%20with%20DOMPurify.md)**

- **Data:** 2026-06-08
- **Session ID:** `a5c74064-c02c-4534-8380-0219a737b4b6`
- **Tamanho original:** 554 KB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-06-08 - Sanitize AI-generated HTML in DashboardHome with DOMPurify.md`

## Roteiro da sessao

- In /home/gcrUX/htdocs/constellation-orchestra, src/pages/DashboardHome.tsx around line 677 renders content_lib
- Continue from where you left off.
- ok continue e faça o /handoff  oficial
- Execute the ShakeHands /handoff ritual to seal this session.
- Execute the ShakeHands /handson ritual for this project.

## Previa

> # [[2026-06-04 - Sanitize AI-generated HTML in DashboardHome with DOMPurify|Sanitize AI-generated HTML in DashboardHome with DOMPurify]]
> **Date:** 2026-06-08 | **Session ID:** `a5c74064-c02c-4534-8380-0219a737b4b6`
> 
> ---
> 
> ## 👤 User *(20:59:54)*
> 
> In /home/gcrUX/htdocs/constellation-orchestra, src/pages/DashboardHome.tsx around line 677 renders content_library.body (AI-generated HTML from the orchestrate pipeline) via `dangerouslySetInnerHTML` with no sanitizer. A /security-review flagged this as a pre-existing stored-XSS hardening gap: the field carries raw AI HTML, and if any less-trusted source ever writes content_library.body, the sink becomes exploitable.
> 
> Harden it: sanitize the HTML on render with DOMPurify (add the `dompurify` dep if not present) before passing to dangerouslySetInnerHTML — e.g. `dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(item.body) }}`. Check for any OTHER dangerouslySetInnerHTML usages of content_library.body across src/ (grep) and apply the same sanitization consistently. Keep legitimate article formatting (allow standard tags + the affiliate <a href> links the auto-monetize step inserts — DOMPurify's default allows <a>). Verify tsc passes + the dashboard still renders an article with its affiliate links intact.
> 
> Context: the auto-monetize feature (OTD-ML-CLICKS) now embeds <a href="...process-affiliate-link?link_id=..."> anchors into article HTML, so the sanitizer must NOT strip <a href> (it doesn't by default, but confirm).
> 
> ## 🤖 Claude *(21:00:18)*
> 
> 
> ## 🤖 Claude *(21:00:18)*
> 
> Vou começar declarando o ORO triplet e levantando os fatos materiais antes de tocar em qualquer código.
> 
> **ORO triplet desta task:**
> - **Operator:** AI Agent (MCORCH Master Execution Agent)
> - **Reviewer:** Sovereign (Gabriel)
> - **Owner:** Sovereign — blast radius é stored-XSS no dashboard user-facing (renderização de HTML de IA)
> 
> Enquadramento do BoK Gate: isto é um **patch de hardening de segurança** escopado a uma feature já documentada (content_library / pipeline orchestrate) + bump de dependência — cai nas isenções do Master Protocol (não é módulo/feature/integração nova). Sigo sob as Leis de Sobrevivência (Materialidade + ORO).
> 
> Levantando os fatos em paralelo:
> 
> ## 🤖 Claude *(21:00:18)*
> 
> 
> 🛠️ **Tool Call**: `Read`
> ```json
> {

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-08 - Audit trading bot order status and agent KPI updates]]
> * **Próxima Sessão**: [[2026-06-08 - agent-a0a17aa1b197bcb71]]
%% --- TIMELINE END --- %%

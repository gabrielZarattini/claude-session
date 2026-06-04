# Sanitize AI-generated HTML in DashboardHome with DOMPurify
**Date:** 2026-06-04 | **Session ID:** `a5c74064-c02c-4534-8380-0219a737b4b6`

---

## 👤 User *(20:59:54)*

In /home/gcrUX/htdocs/constellation-orchestra, src/pages/DashboardHome.tsx around line 677 renders content_library.body (AI-generated HTML from the orchestrate pipeline) via `dangerouslySetInnerHTML` with no sanitizer. A /security-review flagged this as a pre-existing stored-XSS hardening gap: the field carries raw AI HTML, and if any less-trusted source ever writes content_library.body, the sink becomes exploitable.

Harden it: sanitize the HTML on render with DOMPurify (add the `dompurify` dep if not present) before passing to dangerouslySetInnerHTML — e.g. `dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(item.body) }}`. Check for any OTHER dangerouslySetInnerHTML usages of content_library.body across src/ (grep) and apply the same sanitization consistently. Keep legitimate article formatting (allow standard tags + the affiliate <a href> links the auto-monetize step inserts — DOMPurify's default allows <a>). Verify tsc passes + the dashboard still renders an article with its affiliate links intact.

Context: the auto-monetize feature (OTD-ML-CLICKS) now embeds <a href="...process-affiliate-link?link_id=..."> anchors into article HTML, so the sanitizer must NOT strip <a href> (it doesn't by default, but confirm).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-04 - Fix click tracking and complete four priority tasks]]
> * **Próxima Sessão**: [[2026-06-04 - agent-a0393d578685593df]]
%% --- TIMELINE END --- %%

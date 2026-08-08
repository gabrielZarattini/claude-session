# Session agent-ac9facaf7dad72b43
**Date:** 2026-06-10 | **Session ID:** `agent-ac9facaf7dad72b43`

---

## 👤 User *(23:34:11)*

Close this research gap for the vision-mcp blueprint (MCORCH native MCP server for vision/deepsearch). Gap: Remote MCP authorization-server implementation path for MCORCH's self-hosted stack is unresolved — only the OAuth 2.1 SPEC was verified, not a buildable recipe. The existing in-house gitnexus MCP server's HTTP transport is unauthenticated/internal, so exposing a protected remote endpoint to external ecosystems (RFC 9728 protected-resource-metadata + RFC 8707 audience + DCR/CIMD + PKCE) is net-new. Sandcastles outsourced this to WorkOS AuthKit; the research never establishes whether MCORCH should adopt WorkOS/Stytch/Auth0, build the AS on Supabase Auth (which does not natively emit RFC 9728/8707/DCR), or rely on PAT-as-Bearer only — the single hardest new build is undecided.
Suggested starting search: WorkOS AuthKit / Stytch / Auth0 as MCP OAuth 2.1 authorization server for self-hosted remote MCP; Supabase Auth + custom RFC 9728 protected-resource-metadata and RFC 8707 audience validation; GitHub/Supabase PAT-as-Bearer fallback patterns.
Use WebSearch/WebFetch.
HARD MATERIALITY RULES (MCORCH Law 1): every claim must cite the URL you actually consulted (WebSearch/WebFetch). If a fact cannot be established from a fetched source, put it in could_not_verify or mark confidence 'low' — NEVER invent product names, versions, benchmarks or URLs. Verify model/product names actually exist via search; do not rely on memory alone. Current date: 2026-06-10. Your final output is raw structured data for a machine pipeline, not prose for a human.

## 🤖 Claude *(23:34:12)*

You've hit your session limit · resets 11:40pm (America/Sao_Paulo)

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-10 - agent-ac73b79fbee6a7123]]
> * **Próxima Sessão**: [[2026-06-10 - agent-acf1b095574c71f85]]
%% --- TIMELINE END --- %%

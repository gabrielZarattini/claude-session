---
type: session-stub
archived: true
original_size_bytes: 341004
original_size: 333 KB
date: 2026-06-01
session_id: 9dfbd984-e929-4692-9617-6d369414f2f2
full_path: _full-sessions/ClaudeSessions/2026-06-01 - Fix tenant isolation in edge functions.md
github: https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-01%20-%20Fix%20tenant%20isolation%20in%20edge%20functions.md
---

# Fix tenant isolation in edge functions

> [!abstract] Sessao arquivada
> O conteudo completo (**333 KB**) foi movido para fora do cofre
> para o Obsidian nao travar na indexacao. Nada foi perdido.

**[Abrir sessao completa no GitHub](https://github.com/gabrielZarattini/claude-session/blob/main/_full-sessions/ClaudeSessions/2026-06-01%20-%20Fix%20tenant%20isolation%20in%20edge%20functions.md)**

- **Data:** 2026-06-01
- **Session ID:** `9dfbd984-e929-4692-9617-6d369414f2f2`
- **Tamanho original:** 333 KB
- **Caminho no repo:** `_full-sessions/ClaudeSessions/2026-06-01 - Fix tenant isolation in edge functions.md`

## Roteiro da sessao

- In `supabase/functions/publish-social/index.ts` (and any sibling functions sharing the pattern), the caller id
- antes de fazer o handoff aqui precisamos de um fallback para o openrouter, usar ele mesmo mas com o melhor fre
- antes de fazer o handoff aqui precisamos de um fallback para o openrouter, usar ele mesmo mas com o melhor fre

## Previa

> # [[2026-05-31 - Fix tenant isolation in edge functions|Fix tenant isolation in edge functions]]
> **Date:** 2026-06-01 | **Session ID:** `9dfbd984-e929-4692-9617-6d369414f2f2`
> 
> ---
> 
> ## 👤 User *(21:59:12)*
> 
> In `supabase/functions/publish-social/index.ts` (and any sibling functions sharing the pattern), the caller identity is resolved as:
> 
> ```ts
> const { data: { user } } = await supabase.auth.getUser();
> let userId;
> if (user) userId = user.id;
> else if (bodyUserId) userId = bodyUserId;  // <-- trusts body.user_id with NO service-role check
> else return 401;
> ```
> 
> Problem: Supabase Edge Functions accept the **public anon/publishable key** as a valid Bearer JWT. With the anon key, `auth.getUser()` returns null, so the code falls back to trusting `body.user_id`. An attacker holding the public publishable key (it ships in the frontend bundle) plus a victim's `user_id` UUID can invoke `publish-social` on the victim's behalf — publishing arbitrary content to the victim's connected LinkedIn/Instagram/Facebook/Twitter accounts (cross-tenant publish). This violates the project's API Tenancy isolation mandate (CLAUDE.md).
> 
> Fix (already applied to the newer `publish-meta/index.ts` as the reference): only trust `body.user_id` when the caller is a genuine service-role caller:
> 
> ```ts
> const isServiceRole = authHeader === `Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}`;
> const userId = user?.id ?? (isServiceRole ? bodyUserId : undefined);
> if (!userId) return 401;
> ```
> 
> Scope: audit ALL edge functions for the `?? bodyUserId` / `body.user_id` fallback pattern (grep `bodyUserId`, `user_id: bodyUserId`, `body.user_id`) and apply the same service-role gate. Known caller `auto-publish` already uses the service-role key, so it stays working. Verify each function still works for its legitimate cron/service-role caller. Redeploy the affected functions with materiality proof (script size + ACTIVE in `supabase functions list`).
> 
> ## 🤖 Claude *(21:59:32)*
> 
> 
> ## 🤖 Claude *(21:59:35)*
> 
> Vou começar auditando o escopo materialmente. Primeiro, deixe-me declarar o enquadramento e mapear o padrão vulnerável em todas as edge functions.

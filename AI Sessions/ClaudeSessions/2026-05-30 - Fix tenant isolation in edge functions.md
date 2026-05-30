# Fix tenant isolation in edge functions
**Date:** 2026-05-30 | **Session ID:** `9dfbd984-e929-4692-9617-6d369414f2f2`

---

## 👤 User *(21:59:12)*

In `supabase/functions/publish-social/index.ts` (and any sibling functions sharing the pattern), the caller identity is resolved as:

```ts
const { data: { user } } = await supabase.auth.getUser();
let userId;
if (user) userId = user.id;
else if (bodyUserId) userId = bodyUserId;  // <-- trusts body.user_id with NO service-role check
else return 401;
```

Problem: Supabase Edge Functions accept the **public anon/publishable key** as a valid Bearer JWT. With the anon key, `auth.getUser()` returns null, so the code falls back to trusting `body.user_id`. An attacker holding the public publishable key (it ships in the frontend bundle) plus a victim's `user_id` UUID can invoke `publish-social` on the victim's behalf — publishing arbitrary content to the victim's connected LinkedIn/Instagram/Facebook/Twitter accounts (cross-tenant publish). This violates the project's API Tenancy isolation mandate (CLAUDE.md).

Fix (already applied to the newer `publish-meta/index.ts` as the reference): only trust `body.user_id` when the caller is a genuine service-role caller:

```ts
const isServiceRole = authHeader === `Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}`;
const userId = user?.id ?? (isServiceRole ? bodyUserId : undefined);
if (!userId) return 401;
```

Scope: audit ALL edge functions for the `?? bodyUserId` / `body.user_id` fallback pattern (grep `bodyUserId`, `user_id: bodyUserId`, `body.user_id`) and apply the same service-role gate. Known caller `auto-publish` already uses the service-role key, so it stays working. Verify each function still works for its legitimate cron/service-role caller. Redeploy the affected functions with materiality proof (script size + ACTIVE in `supabase functions list`).

## 🤖 Claude *(21:59:32)*


## 🤖 Claude *(21:59:35)*

Vou começar auditando o escopo materialmente. Primeiro, deixe-me declarar o enquadramento e mapear o padrão vulnerável em todas as edge functions.

**ORO triplet desta task:**
- **Operator:** MCORCH Master Execution Agent (eu)
- **Reviewer:** Sovereign (Gabriel) — antes do deploy de produção
- **Owner:** Sovereign — blast radius = publicação cross-tenant em contas sociais conectadas de qualquer usuário (risco de integridade de dados + reputação + LGPD)

Isto é hardening de segurança de uma feature já documentada (API Tenancy Model no CLAUDE.md), então não dispara o BoK Gate. Vou começar pela investigação material.

## 🤖 Claude *(21:59:39)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== grep bodyUserId ===\" && grep -rln \"bodyUserId\" supabase/functions/ 2>/dev/null; echo \"=== grep body.user_id (and body?.user_id) ===\" && grep -rln \"body\\.user_id\\|body?\\.user_id\" supabase/functions/ 2>/dev/null; echo \"=== grep user_id: in destructuring/assignment ===\" && grep -rln \"\\.user_id ||\\|user_id ||\\|?? bodyUserId\\|?? body\" supabase/functions/ 2>/dev/null",
  "description": "Grep for the body.user_id fallback pattern across edge functions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === grep bodyUserId ===
> supabase/functions/publish-social/index.ts
> === grep body.user_id (and body?.user_id) ===
> === grep user_id: in destructuring/assignment ===
> supabase/functions/canvas-execute/index.ts
> ```

## 🤖 Claude *(21:59:40)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/worktrees/dreamy-blackburn-2dd6e7/supabase/functions/publish-meta/index.ts"
}
```

> **Tool Result (Read)** - ❌ Error
>
> ```
> File does not exist. Note: your current working directory is /home/gcrUX/htdocs/constellation-orchestra/.claude/worktrees/dreamy-blackburn-2dd6e7.
> ```

## 🤖 Claude *(21:59:40)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/worktrees/dreamy-blackburn-2dd6e7/supabase/functions/publish-social/index.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 2	
> 3	const corsHeaders = {
> 4	  "Access-Control-Allow-Origin": "*",
> 5	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 6	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-user-token, x-supabase-client-platform, x-supabase-client-platform-version, x-supabase-client-runtime, x-supabase-client-runtime-version",
> 7	};
> 8	
> 9	Deno.serve(async (req) => {
> 10	  if (req.method === "OPTIONS") {
> 11	    return new Response("ok", { headers: corsHeaders });
> 12	  }
> 13	
> 14	  try {
> 15	    const authHeader = req.headers.get("Authorization");
> 16	    if (!authHeader?.startsWith("Bearer ")) {
> 17	      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 18	        status: 401,
> 19	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 20	      });
> 21	    }
> 22	
> 23	    const body = await req.json();
> 24	    const { platform, content, social_account_id, scheduled_post_id, user_id: bodyUserId } = body;
> 25	
> 26	    if (!platform || !content) {
> 27	      return new Response(JSON.stringify({ error: "platform and content required" }), {
> 28	        status: 400,
> 29	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 30	      });
> 31	    }
> 32	
> 33	    const adminClient = createClient(
> 34	      Deno.env.get("SUPABASE_URL")!,
> 35	      Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
> 36	    );
> 37	
> 38	    // Resolve caller identity:
> 39	    // - User JWT (frontend): auth.getUser() returns a user
> 40	    // - Service role (auto-publish cron): auth.getUser() returns null; trust user_id from body
> 41	    //   since Supabase infrastructure already validated the JWT signature
> 42	    const supabase = createClient(
> 43	      Deno.env.get("SUPABASE_URL")!,
> 44	      Deno.env.get("SUPABASE_ANON_KEY")!,
> 45	      { global: { headers: { Authorization: authHeader } } }
> 46	    );
> 47	    const { data: { user } } = await supabase.auth.getUser();
> 48	
> 49	    let userId: string;
> 50	    if (user) {
> 51	      userId = user.id;
> 52	    } else if (bodyUserId) {
> 53	      userId = bodyUserId;
> 54	    } else {
> 55	      return new Response(JSON.stringify({ error: "Unauthorized" }), {
> 56	        status: 401,
> 57	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 58	      });
> 59	    }
> 60	
> 61	    let query = adminClient
> 62	      .from("social_accounts")
> 63	      .select("*")
> 64	      .eq("user_id", userId)
> 65	      .eq("platform", platform)
> 66	      .eq("is_active", true);
> 67	
> 68	    if (social_account_id) query = query.eq("id", social_account_id);
> 69	
> 70	    const { data: accounts, error: accError } = await query.limit(1).single();
> 71	    if (accError || !accounts) {
> 72	      return new Response(JSON.stringify({ error: `No active ${platform} account found` }), {
> 73	        status: 404,
> 74	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 75	      });
> 76	    }
> 77	
> 78	    const account = accounts;
> 79	
> 80	    // Refresh token if expired, then re-fetch account to get the new access_token
> 81	    if (account.token_expires_at && new Date(account.token_expires_at) < new Date()) {
> 82	      const refreshRes = await fetch(`${Deno.env.get("SUPABASE_URL")}/functions/v1/refresh-social-token`, {
> 83	        method: "POST",
> 84	        headers: {
> 85	          "Content-Type": "application/json",
> 86	          Authorization: `Bearer ${Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")}`,
> 87	        },
> 88	        body: JSON.stringify({ social_account_id: account.id }),
> 89	      });
> 90	      if (!refreshRes.ok) {
> 91	        return new Response(JSON.stringify({ error: "Token expired and refresh failed" }), {
> 92	          status: 401,
> 93	          headers: { ...corsHeaders, "Content-Type": "application/json" },
> 94	        });
> 95	      }
> 96	      // refresh-social-token updates the DB but does not return the token;
> 97	      // re-fetch to get the updated access_token
> 98	      const { data: refreshedAccount } = await adminClient
> 99	        .from("social_accounts")
> 100	        .select("access_token, refresh_token, token_expires_at")
> 101	        .eq("id", account.id)
> 102	        .single();
> 103	      if (refreshedAccount) {
> 104	        account.access_token = refreshedAccount.access_token;
> 105	        account.token_expires_at = refreshedAccount.token_expires_at;
> 106	      }
> 107	    }
> 108	
> 109	    let result: any;
> 110	
> 111	    if (platform === "linkedin") {
> 112	      const res = await fetch("https://api.linkedin.com/v2/ugcPosts", {
> 113	        method: "POST",
> 114	        headers: {
> 115	          Authorization: `Bearer ${account.access_token}`,
> 116	          "Content-Type": "application/json",
> 117	          "X-Restli-Protocol-Version": "2.0.0",
> 118	        },
> 119	        body: JSON.stringify({
> 120	          author: `urn:li:person:${account.platform_user_id}`,
> 121	          lifecycleState: "PUBLISHED",
> 122	          specificContent: {
> 123	            "com.linkedin.ugc.ShareContent": {
> 124	              shareCommentary: { text: content.text || content },
> 125	              shareMediaCategory: "NONE",
> 126	            },
> 127	          },
> 128	          visibility: { "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC" },
> 129	        }),
> 130	      });
> 131	      result = await res.json();
> 132	      if (!res.ok) {
> 133	        console.error("LinkedIn publish error:", res.status, result);
> 134	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 135	      }
> 136	
> 137	    } else if (platform === "instagram") {
> 138	      const igAccountId = account.platform_user_id;
> 139	      const createRes = await fetch(
> 140	        `https://graph.facebook.com/v19.0/${igAccountId}/media`,
> 141	        {
> 142	          method: "POST",
> 143	          headers: { "Content-Type": "application/json" },
> 144	          body: JSON.stringify({
> 145	            caption: content.text || content,
> 146	            image_url: content.image_url,
> 147	            access_token: account.access_token,
> 148	          }),
> 149	        }
> 150	      );
> 151	      const container = await createRes.json();
> 152	      if (!createRes.ok) {
> 153	        console.error("Instagram media create error:", createRes.status, container);
> 154	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 155	      }
> 156	
> 157	      const pubRes = await fetch(
> 158	        `https://graph.facebook.com/v19.0/${igAccountId}/media_publish`,
> 159	        {
> 160	          method: "POST",
> 161	          headers: { "Content-Type": "application/json" },
> 162	          body: JSON.stringify({
> 163	            creation_id: container.id,
> 164	            access_token: account.access_token,
> 165	          }),
> 166	        }
> 167	      );
> 168	      result = await pubRes.json();
> 169	      if (!pubRes.ok) {
> 170	        console.error("Instagram publish error:", pubRes.status, result);
> 171	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 172	      }
> 173	
> 174	    } else if (platform === "facebook") {
> 175	      const pageId = account.platform_user_id;
> 176	      const res = await fetch(
> 177	        `https://graph.facebook.com/v19.0/${pageId}/feed`,
> 178	        {
> 179	          method: "POST",
> 180	          headers: { "Content-Type": "application/json" },
> 181	          body: JSON.stringify({
> 182	            message: content.text || content,
> 183	            access_token: account.access_token,
> 184	          }),
> 185	        }
> 186	      );
> 187	      result = await res.json();
> 188	      if (!res.ok) {
> 189	        console.error("Facebook publish error:", res.status, result);
> 190	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 191	      }
> 192	
> 193	    } else if (platform === "twitter") {
> 194	      const res = await fetch("https://api.x.com/2/tweets", {
> 195	        method: "POST",
> 196	        headers: {
> 197	          Authorization: `Bearer ${account.access_token}`,
> 198	          "Content-Type": "application/json",
> 199	        },
> 200	        body: JSON.stringify({
> 201	          text: content.text || content,
> 202	        }),
> 203	      });
> 204	      result = await res.json();
> 205	      if (!res.ok) {
> 206	        console.error("Twitter publish error:", res.status, result);
> 207	        throw new Error("PLATFORM_PUBLISH_FAILED");
> 208	      }
> 209	
> 210	    } else {
> 211	      return new Response(JSON.stringify({ error: `Publishing to ${platform} not yet supported` }), {
> 212	        status: 400,
> 213	        headers: { ...corsHeaders, "Content-Type": "application/json" },
> 214	      });
> 215	    }
> 216	
> 217	    if (scheduled_post_id) {
> 218	      await adminClient
> 219	        .from("scheduled_posts")
> 220	        .update({
> 221	          status: "published",
> 222	          published_at: new Date().toISOString(),
> 223	          platform_post_id: result.id || result.data?.id || result["X-RestLi-Id"],
> 224	        })
> 225	        .eq("id", scheduled_post_id);
> 226	    }
> 227	
> 228	    return new Response(JSON.stringify({ success: true, result }), {
> 229	      headers: { ...corsHeaders, "Content-Type": "application/json" },
> 230	    });
> 231	  } catch (err) {
> 232	    console.error("publish-social error:", err);
> 233	    return new Response(
> 234	      JSON.stringify({ error: "Falha ao publicar. Tente novamente em instantes." }),
> 235	      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
> 236	    );
> 237	  }
> 238	});
> 239	
> ```

## 🤖 Claude *(21:59:46)*


## 🤖 Claude *(21:59:48)*

O arquivo de referência `publish-meta/index.ts` não existe nesse path. Deixe-me mapear o diretório de functions inteiro e ampliar a busca pelo padrão — o `auth.getUser()` seguido de fallback pode aparecer com nomes de variável diferentes de `bodyUserId`.

## 🤖 Claude *(21:59:50)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd supabase/functions && echo \"=== ALL functions ===\" && ls -1d */ 2>/dev/null && echo \"\" && echo \"=== anything 'meta' ===\" && ls -1d *meta* 2>/dev/null; echo \"\" && echo \"=== files mentioning publish-meta ===\" && grep -rln \"publish-meta\" . 2>/dev/null",
  "description": "List all edge functions and search for publish-meta references"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === ALL functions ===
> admin-manage-user/
> agent-task-execute/
> aios-chat/
> aios-sql-bridge/
> analyze-node/
> analyze-sem/
> analyze-seo/
> autonomic-action/
> auto-publish/
> award-mco-coins/
> canvas-execute/
> check-subscription/
> check-video-status/
> create-checkout/
> create-portal/
> data-export/
> delete-account/
> design-job-enqueue/
> embed-mcorch-node/
> fetch-trends/
> generate-audio-script/
> generate-content/
> generate-image/
> generate-video/
> generate-video-script/
> get-infra-status/
> handle-ml-postback/
> higgsfield-webhook/
> instagram-webhook/
> list-provider-models/
> openrouter-swarm/
> optimize-schedule/
> orchestrate-content/
> orchestrate-step/
> process-affiliate-link/
> publish-social/
> publish-wordpress/
> refresh-social-token/
> rescue-video/
> search-constellation/
> self-heal/
> self-optimize/
> social-auth-callback/
> social-auth-init/
> stripe-webhook/
> sync-knowledge-mesh/
> trigger-embeddings/
> trigger-ingest/
> tts-speak/
> 
> === anything 'meta' ===
> 
> === files mentioning publish-meta ===
> ```

## 🤖 Claude *(21:59:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd supabase/functions && echo \"=== getUser() usage across functions ===\" && grep -rln \"auth.getUser()\" . 2>/dev/null | sort && echo \"\" && echo \"=== SERVICE_ROLE_KEY comparison (the canonical gate) ===\" && grep -rln \"SERVICE_ROLE_KEY\\`\" . 2>/dev/null | sort && echo \"\" && echo \"=== isServiceRole usage ===\" && grep -rln \"isServiceRole\\|service_role\\|serviceRole\" . 2>/dev/null | sort",
  "description": "Map getUser and service-role gate usage across functions"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === getUser() usage across functions ===
> admin-manage-user/index.ts
> agent-task-execute/index.ts
> aios-chat/index.ts
> analyze-node/index.ts
> analyze-sem/index.ts
> analyze-seo/index.ts
> canvas-execute/index.ts
> check-video-status/index.ts
> create-checkout/index.ts
> create-portal/index.ts
> data-export/index.ts
> delete-account/index.ts
> design-job-enqueue/index.ts
> fetch-trends/index.ts
> generate-audio-script/index.ts
> generate-content/index.ts
> generate-image/index.ts
> generate-video/index.ts
> generate-video-script/index.ts
> list-provider-models/index.ts
> openrouter-swarm/index.ts
> orchestrate-content/index.ts
> process-affiliate-link/index.ts
> publish-social/index.ts
> publish-wordpress/index.ts
> refresh-social-token/index.ts
> rescue-video/index.ts
> social-auth-init/index.ts
> trigger-embeddings/index.ts
> trigger-ingest/index.ts
> tts-speak/index.ts
> 
> === SERVICE_ROLE_KEY comparison (the canonical gate) ===
> 
> === isServiceRole usage ===
> agent-task-execute/index.ts
> aios-sql-bridge/index.ts
> award-mco-coins/index.ts
> data-export/index.ts
> generate-image/index.ts
> generate-video-script/index.ts
> publish-wordpress/index.ts
> refresh-social-token/index.ts
> ```

---

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-05-30 - Fix API key leak and reconfigure model defaults]]
> * **Próxima Sessão**: [[2026-05-30 - Seal meta-api BoK suite and test robustness]]
%% --- TIMELINE END --- %%

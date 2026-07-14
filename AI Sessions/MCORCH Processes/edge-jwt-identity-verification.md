# SOP: Edge Function JWT Identity Verification (verify_jwt=false)

**Status:** ACTIVE · v1.0 · 2026-05-30
**Owner:** Sovereign (Gabriel Zarattini)
**Survival Law 2 compliance:** Escrita ANTES do fix de verificação de assinatura em `check-video-status`, `generate-video`, `generate-video-script`, `list-provider-models` (fecha a impersonação cross-tenant via JWT não-verificado).
**Canonical directive:** `CLAUDE.md > Architecture > "API Tenancy Model — Per-User Credentials"` · `.claude/rules/survival.md > Law 1 (Materiality)`

---

## Context

Funções Edge marcadas com `verify_jwt = false` em `supabase/config.toml` **não passam pela validação de JWT do gateway** (Kong). A razão é material e confirmada: o projeto migrou para **chaves de assinatura assimétricas ES256** (JWKS público em `https://bcyvddsykvehvpwstlfa.supabase.co/auth/v1/.well-known/jwks.json`, P-256, `kid d073a3db-…`), enquanto a `SUPABASE_SERVICE_ROLE_KEY` permanece um JWT **legacy HS256**. O gateway, configurado para o segredo HS256, **rejeita** tokens de sessão ES256 dos usuários → daí `verify_jwt=false` foi adotado como workaround (comentários `"bypass ES256 gateway"`).

Com o gateway desligado, a **resolução de identidade vira responsabilidade exclusiva da própria função**. A implementação original fazia:

```ts
// ANTI-PATTERN (proibido) — decodifica SEM verificar a assinatura
const { data: { user } } = await supabase.auth.getUser();
userId = user?.id || extractUserIdFromJWT(authHeader); // <- atob(payload).sub cego
```

`extractUserIdFromJWT` lê `payload.sub` via `atob` **sem verificar a assinatura**. Como o gateway também não verifica (`verify_jwt=false`), um atacante forja um JWT com 3 partes onde o payload base64 contém `{"sub":"<victim-uuid>"}` e a assinatura é lixo: `getUser()` rejeita (assinatura inválida → null), o fallback retorna o `sub` da vítima, e a função **executa como a vítima** — lendo e gastando `user_api_keys` (gemini/openrouter/replicate/google), mcoCoins e conteúdo de qualquer tenant. As checagens `admin.getUserById(userId)` presentes em 3 das 4 funções só provam que a **vítima existe** (o que o atacante quer) — é teatro de identidade, não gate de identidade.

**Por que importa (multi-tenant readiness):** isolamento de credencial por tenant · atribuição de custo (mcoCoins/quota de API) correta · risco financeiro isolado (credencial de um tenant não vaza para outro) · LGPD. Viola diretamente o "API Tenancy Model" do `CLAUDE.md`.

---

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (fix) + Edge runtime Deno (execução por request)
- **Reviewer:** Sovereign (Gabriel) — aprova o diff + valida a prova local e o exploit test pós-deploy
- **Owner:** Sovereign — blast radius = impersonação cross-tenant em 4 endpoints de vídeo/modelos (roubo de API keys + mcoCoins + leitura de conteúdo)

---

## Operator (quem chama hoje — material)

| Caller | Arquivo | Token enviado |
|--------|---------|---------------|
| Frontend — Video Editor | `src/pages/VideoEditorPage.tsx` | `Bearer ${supabase.auth.getSession().access_token}` (ES256 de sessão) |
| Frontend — Content Library | `src/pages/ContentLibraryPage.tsx` | idem |

**Não existe** chamador server-side, cron, `orchestrate-content`, webhook ou script `~/.openclaw` para estas 4 funções (varredura repo-wide 2026-05-30). O "chamador ES256" é o **browser** com token de sessão Supabase padrão — NÃO um orquestrador soberano mintando tokens próprios.

---

## Resolution order (canonical — para funções verify_jwt=false)

| # | Camada | Fonte | Permitido em |
|---|--------|-------|--------------|
| 1 | **getUser()** | `supabase.auth.getUser()` com `Authorization` do request → `user.id` (GoTrue valida a assinatura server-side) | SEMPRE (caminho primário, fluxo user-facing) |
| 2 | **JWKS verify (fallback)** | `verifyJwtAndGetUserId(authHeader)` → `jwtVerify(token, createRemoteJWKSet(<project>/auth/v1/.well-known/jwks.json))` → confia em `payload.sub` **SOMENTE** após a assinatura ES256 verificar | SEMPRE que (1) retornar null mas o token for legitimamente assinado pelo projeto |
| 3 | **Service-role gate** (padrão irmão) | `authHeader === \`Bearer ${SERVICE_ROLE_KEY}\`` → confia em `body.user_id` | SÓ em funções com chamador server-side/cron real (ex.: `publish-social`, `publish-wordpress`, auto-publish). **N/A** para as 4 funções deste SOP (sem caller server-side). |
| 4 | **Hard failure** | — | HTTP 401 `{ error: "Token inválido" }`. **NUNCA** decodificar `sub` sem verificar assinatura. |

**Regra de ouro:** confiar em um claim `sub` só é permitido depois de **uma** das provas: (a) `getUser()` retornou esse user, OU (b) a assinatura ES256 do token verificou contra o JWKS do projeto, OU (c) o caller provou posse da `SERVICE_ROLE_KEY` (e aí o `user_id` vem do body, não do JWT).

---

## Sequence (fix aplicado — Option 1 cirúrgica)

Em cada uma das 4 funções:

1. Importar `{ jwtVerify, createRemoteJWKSet }` de `https://esm.sh/jose@5.9.6`.
2. Criar `const SUPABASE_JWKS = createRemoteJWKSet(new URL(\`${Deno.env.get("SUPABASE_URL")}/auth/v1/.well-known/jwks.json\`))` em module scope (cacheado entre invocações; fetch lazy no primeiro verify).
3. Substituir o corpo de `extractUserIdFromJWT` por `verifyJwtAndGetUserId(authHeader)` async:
   ```ts
   async function verifyJwtAndGetUserId(authHeader: string | null): Promise<string | null> {
     if (!authHeader) return null;
     const token = authHeader.replace("Bearer ", "").trim();
     if (!token) return null;
     try {
       const { payload } = await jwtVerify(token, SUPABASE_JWKS);
       return typeof payload.sub === "string" ? payload.sub : null;
     } catch {
       return null; // assinatura inválida/expirada/malformada → rejeita
     }
   }
   ```
4. Trocar o call-site `user?.id || extractUserIdFromJWT(authHeader)` por `user?.id || await verifyJwtAndGetUserId(authHeader)` (e o else-branch equivalente em `generate-video-script` / `list-provider-models`).
5. **Manter** `verify_jwt=false` em `config.toml` (o gateway não verifica ES256; a função agora é o gate real) e **manter** `getUser()` como caminho primário.

---

## Verification gates

| Gate | Check | Pass criterion |
|------|-------|----------------|
| **G1 — Local mechanism (jose, Deno)** | `~/.deno/bin/deno run --allow-net scripts/qa/test-es256-jwt-verification.ts` | Token assinado com keypair ES256 local → `sub` retornado; assinatura adulterada → `null`; token forjado base64 (`{sub}` + sig lixo) → `null` |
| **G2 — Real-JWKS negative** | Mesmo teste, ramo que verifica o token forjado contra o **JWKS real do projeto** | `null` (a exploração real é rejeitada) |
| **G3 — Deploy materiality** | `npx supabase functions deploy <name>` + `npx supabase functions list` | VERSION de cada função **incrementa** vs. baseline |
| **G4 — Post-deploy exploit (prod)** | `curl -X POST <fn-url>` com `Authorization: Bearer <forged>` + `apikey: <anon>` | HTTP **401** (antes do fix: 200/202/processa como vítima) |
| **G5 — Positive (prod)** | Frontend logado chama a função OU Sovereign cola um `access_token` fresco para teste | Resposta normal (200/202) — sem regressão para o caller legítimo |

G5 exige um token de sessão válido (não mintável sem credenciais de usuário) → **brain-without-hands** declarado: validar via UI logada em `login.mcorch.com` (Ctrl+Shift+R) ou token colado pelo Sovereign.

---

## Recovery path

- **jose não resolve no deploy** (esm.sh indisponível / build Deno incompatível): G1 já roda o mesmo import localmente antes do deploy → se G1 passou, o import é válido. Se mesmo assim o deploy falhar no bundle, fazer rollback (abaixo) e fixar versão alternativa (`jose@5.x`) ou migrar para `djwt`.
- **JWKS inacessível em runtime** (raro — mesma infra Supabase): `jwtVerify` lança → `verifyJwtAndGetUserId` retorna `null` → 401. **Fail-closed** (nega acesso), nunca fail-open. Caller legítimo seria impactado, mas nenhuma impersonação ocorre. Mitigação: `createRemoteJWKSet` cacheia o JWKS após o primeiro fetch.
- **Rollback de deploy:** `git checkout HEAD~1 -- supabase/functions/<name>/index.ts && npx supabase functions deploy <name>` (re-deploya a versão anterior). Confirmar VERSION na `functions list`.
- **Regressão no caller legítimo (G5 falha):** rollback imediato dos 4; investigar se `getUser()` estava de fato carregando o fluxo e se o token de sessão não verifica contra o JWKS (improvável — JWKS é a chave pública do próprio GoTrue que assinou).

---

## Success signal

- G1+G2 verdes localmente (output literal do `deno run` colado no handoff — Lei 1).
- G3: VERSION das 4 funções incrementada (output literal de `functions list` antes/depois).
- G4: `401` literal no exploit test contra produção para as 4 funções.
- G5: caller legítimo funcionando (UI ou token colado).
- `extractUserIdFromJWT` (atob cego) **não existe mais** em nenhuma das 4 funções (`rg extractUserIdFromJWT supabase/functions` → vazio).

---

## Anti-patterns proibidos

- ❌ `atob(payload).sub` (ou qualquer decode) usado como identidade **sem** verificar a assinatura.
- ❌ `admin.getUserById(sub)` tratado como prova de identidade (só prova existência da vítima).
- ❌ Fail-open: em erro de verificação, assumir uma identidade default ou seguir sem `userId`.
- ❌ Expor `SERVICE_ROLE_KEY` ao browser para usar o gate da camada 3 (catastrófico — o caller destas 4 funções é o browser).
- ❌ Setar `verify_jwt=true` no gateway para estas funções (rejeitaria os tokens ES256 legítimos → quebra o frontend).

---

## Sibling reference

- Service-role gate correto (camada 3): `supabase/functions/publish-wordpress/index.ts` (linhas ~26-47) e `supabase/functions/publish-social/index.ts` — usados por callers server-side/cron reais (auto-publish). Padrão diferente, mesma diretiva (API Tenancy).

# SOP — TikTok Login (Login Kit v2) OAuth → Supabase session

> **Lei 2 (Processo Antecipado).** O processo humano equivalente do "Entrar com TikTok" ANTES de qualquer automação. Fonte da verdade: BoK `docs/bok/tiktok-login/` (seal `299b9f36`) + mapa `.claude/context/tiktok-login-map-2026-07-08.md`. Gate CLAUDE.md §1.
>
> **ORO:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign + `/security-review` independente · Owner = Sovereign (sink privilegiado de auth; ações de console do TikTok; USD 0).

---

## Operator — quem executa manualmente hoje?

O **Sovereign** no TikTok Developer Portal + o **usuário final** no browser. Hoje, sem esta feature, o "login social" existe só via Google (`Auth.tsx` `handleOAuthLogin('google')`). O connect do TikTok que existe (`social-auth-init`/`-callback`) é para **publicação** (pressupõe usuário já logado) — NÃO cria usuário nem minta sessão. Este SOP cobre o fluxo NOVO de **login/identidade**.

## Pré-condições (ações Sovereign no console — BLOQUEANTES, paralelizáveis ao código)

| # | Ação | Critério de sucesso material |
|---|------|------------------------------|
| P1 | Registrar o **`redirect_uri` do login** no TikTok console — path **SEPARADO** do publish (TikTok proíbe query-params na URI registrada, então não dá `?intent=login`). Valor: `https://<edge-host>/functions/v1/tiktok-login-callback` (https absoluto, sem query/fragment). | A URI aparece na lista "Redirect URI" do app (≤10 total, ≤512 chars). |
| P2 | Adicionar a **conta TikTok de teste** como *sandbox target-user* (o app está unaudited → `user.info.basic` só loga usuários-sandbox registrados). | A conta aparece em Sandbox → Target users. |
| P3 | Provisionar secrets no vault das edge fns: `TIKTOK_CLIENT_KEY`, `TIKTOK_CLIENT_SECRET` (do ambiente que será demonstrado — sandbox `sb…` vs prod diferem). | `npx supabase secrets list` mostra as duas chaves. |

> Sem P1–P3 o fluxo **não completa** — o código pode ser deployado e testado até o ponto do redirect, mas o consent/callback falha. Isso é o teto honesto (Lei 1).

## Sequence — em que ordem? (cada passo com critério material)

| # | Passo | Ator | Critério de sucesso material |
|---|-------|------|------------------------------|
| S1 | Usuário abre `/auth?devLogin` e clica **"Entrar com TikTok"** | Usuário | Botão visível SÓ com `?devLogin` (público não vê); clique chama `handleTikTokLogin` → invoca `tiktok-login-init`. |
| S2 | `tiktok-login-init` monta a authorize URL e retorna `{ url }` | Edge fn | `https://www.tiktok.com/v2/auth/authorize/?client_key=…&scope=user.info.basic&response_type=code&redirect_uri=<P1>&state=<HMAC>`; scope **vírgula-separado**; `state=signState({intent:'login',nonce,return_to,ts})` (nonce, **não** userId). |
| S3 | Browser redireciona ao TikTok; usuário consente | Usuário + TikTok | TikTok redireciona a `<P1>?code=…&state=…`. |
| S4 | `tiktok-login-callback` valida state + troca code por token | Edge fn | `verifyState(maxAge 10min)` **fail-closed**; POST `https://open.tiktokapis.com/v2/oauth/token/` form-encoded (`client_key,client_secret,code,grant_type=authorization_code,redirect_uri`) → resposta com `open_id`. |
| S5 | Find-or-create identidade + mint sessão | Edge fn | `tiktok_identities` lookup por `open_id`; se ausente → `admin.createUser` (email sintético `tiktok_<open_id>@tiktok-login.mcorch.local`, password-less) + insert. Sessão via `admin.generateLink({type:'magiclink'})` → `verifyOtp({token_hash})` → `{access_token,refresh_token}`. |
| S6 | Hand-off SEM token na URL | Edge fn | Gera código single-use (`tiktok_login_codes`, TTL ~60s, `code_hash`), redireciona a `/auth/tiktok/callback?code=<one_time>`. **Nenhum access/refresh token na URL.** |
| S7 | SPA resgata o código → `setSession` | `TikTokLoginCallback.tsx` | POST do código a `tiktok-login-session` → retorna sessão UMA vez (invalida/consumed_at) → `supabase.auth.setSession(...)`. |
| S8 | Sessão ativa → bounce | `useAuth` + `safeReturnTo` | `onAuthStateChange` dispara SIGNED_IN; `safeReturnTo()` (allowlist) ou `/dashboard`. |

## Verification gates (como o operator confirma cada passo)

- **G1 (regressão-zero):** login público (email/senha) e Google intactos — `?devLogin` ausente NÃO mostra o botão TikTok. Prova: browser em `/auth` (sem param) só mostra email/senha.
- **G2 (state fail-closed):** `tiktok-login-callback` com `state` forjado/expirado/ausente → **rejeita** (nunca minta sessão). Prova: smoke `smoke-tiktok-login.ts` cenário state-forjado → 4xx, zero linha em `tiktok_identities`.
- **G3 (no-token-in-URL):** nenhuma URL do fluxo contém `access_token`/`refresh_token`. Prova: inspeção do redirect S6 (só `?code=<opaco>`).
- **G4 (replay-proof):** resgatar o código single-use 2× → 2ª vez **410/consumido**. Prova: smoke replay.
- **G5 (anti-grafting):** login TikTok NUNCA linka a conta email existente — `open_id` novo = conta nova isolada. Prova: 2 open_ids distintos → 2 `user_id` distintos; nenhum match por email.
- **G6 (RLS):** `tiktok_identities`/`tiktok_login_codes` default-deny; cliente anon/autenticado **não** lê os códigos. Prova: `/security-review` + SELECT anon → 0 rows.
- **G7 (security-review):** `/security-review` independente **SAFE** na migration + 3 edge fns ANTES do deploy (FMEA-011). Bloqueante. **Achado fechado 2026-07-08:** login-CSRF/session-fixation HIGH (código de hand-off não ligado ao browser iniciador) → **browser-binding** `src/lib/tiktok-login-binding.ts` (segredo por-tentativa em `sessionStorage`; hash assinado no state → gravado em `tiktok_login_codes.binding_hash` NOT NULL → exigido no resgate atômico `eq('binding_hash')`). Só o browser iniciador resgata; código capturado por atacante falha no browser da vítima. Re-verificado FIX_CONFIRMED.
- **G9 (browser-binding anti-CSRF):** resgatar um código num browser SEM o `binding` (sessionStorage de outra origem/tab) → **410** (0 rows no consume). Prova: smoke cenário binding-mismatch.
- **G8 (E2E sandbox):** com P1–P3 feitos, a conta-sandbox loga ponta-a-ponta e cai autenticada em `/dashboard`; sessão material em `auth.sessions` + linha em `tiktok_identities`. Prova: screen-record + UUID da sessão + Vision QA da tela logada.

## Recovery path — falha no passo N?

- **S2/S3 consent falha (`redirect_uri mismatch`):** P1 não registrado OU host divergente → registrar a URI EXATA no console (não improvisar path). Re-tentar.
- **S3 `scope not authorized` / usuário barrado:** conta não é sandbox target-user (P2) OU app não audited → adicionar a conta em Sandbox; para user público, aguardar audit (teto honesto). Toast PT-BR `not_authorized`.
- **S4 state inválido:** `verifyState` fail-closed → redireciona a `/auth?tiktok_error=state_expired` → usuário re-inicia (state fresco). **NUNCA** retry silencioso que aceite state velho.
- **S4 token exchange falha (client_key/secret errado ou ambiente trocado):** conferir P3 (sandbox vs prod). `/auth?tiktok_error=exchange_failed`; telemetria `infra_health_logs service='tiktok-login' event='error'`.
- **S5 createUser colide (email sintético):** improvável (namespaced por `open_id` único); se colidir, é sinal de bug de chave — abortar, NÃO reusar conta alheia (G5). Investigar `open_id`.
- **S7 código expirado/consumido:** `/auth?tiktok_error=expired` → re-login. Códigos expiram por TTL + `consumed_at`.
- **Rollback total:** remover o botão de `Auth.tsx` (feature some da UI) — as edge fns/migration ficam inertes (nenhum caller). Zero impacto no login existente.

## Success signal — sinal materialmente observável do flow completo

A conta TikTok-sandbox clica "Entrar com TikTok" em `/auth?devLogin`, consente no TikTok, e **cai autenticada em `/dashboard`** com: (a) linha nova em `tiktok_identities(open_id→user_id)`; (b) sessão válida em `auth.sessions`; (c) `infra_health_logs service='tiktok-login' event='success'`; (d) Vision QA APROVADO da tela logada; (e) nenhum token em URL em nenhum passo. Para o **App Review**: screen-record desse fluxo ponta-a-ponta prova o scope `user.info.basic` funcionando.

## Anti-patterns proibidos

- ❌ Reusar `handleOAuthLogin('google'|'apple')` — TikTok não é provider nativo Supabase.
- ❌ `signInWithIdToken` — TikTok não retorna `id_token`/OIDC.
- ❌ Token em query string / hash da URL de redirect.
- ❌ Auto-link de login TikTok a conta email existente (grafting cross-tenant).
- ❌ Scope espaço-separado (o consent do TikTok falha silencioso — usar vírgula).
- ❌ `redirect_uri` com query-param, ou o MESMO path do publish.
- ❌ `deduct_mco_coins` no fluxo (login é zero-coin por invariante).
- ❌ Deploy antes de `/security-review` SAFE (G7).

## Referências
- BoK: `docs/bok/tiktok-login/` (FR-TL / OTD-TL / FM-TL / DD-TL).
- Mapa material: `.claude/context/tiktok-login-map-2026-07-08.md`.
- Reuso: `supabase/functions/_shared/oauth-state.ts`, `src/lib/sso-cookie.ts`, `src/hooks/useAuth.ts`, `scripts/qa/gen-user-jwt.ts` (padrão generateLink→verifyOtp), precedente `social-auth-init`/`-callback`.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

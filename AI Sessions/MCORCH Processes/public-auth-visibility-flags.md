# SOP — Visibilidade pública da tela de login (flags de admin)

> **Lei 2 (Processo Antecipado).** Escrito ANTES do código. Descreve como um humano faria
> manualmente aquilo que a flag automatiza, com gates materiais em cada passo.
>
> **Origem (2026-07-30):** o app do TikTok foi reprovado 4× no App Review. Na 4ª, o revisor escreveu
> *"Your externally facing website must be fully developed and cannot be a landing or login page.
> If it is a login page, you must provide a test account and password."* Ao provisionar a conta de
> teste, o `agent-browser` mediu a tela pública e achou o problema real: em `https://login.mcorch.com/auth`
> os únicos controles visíveis são `Entrar` / `Esqueceu a senha?`. Os botões **"Entrar com TikTok"** e
> **"Continuar com Google"** — e a aba **Cadastrar** — estavam atrás do query param `?devLogin`
> (`src/pages/Auth.tsx`, gate temporário de 2026-06). **O revisor do TikTok nunca viu o Login Kit**,
> porque ele não existia na URL que consta no formulário do app.

---

## 1. O problema que a flag resolve

O gate `?devLogin` é **invisível e não-descobrível**: só quem sabe do param consegue ver os botões.
Isso é adequado para um teste do Sovereign, e **inadequado** para:

- um revisor externo (TikTok / Meta / Google) que abre a URL cadastrada e precisa ver o produto;
- qualquer decisão de produto do tipo "hoje eu quero login social ligado para todo mundo".

A flag troca "param secreto na URL" por **estado explícito, auditado e reversível em 1 clique** em
`/dashboard/admin` → aba **Acesso**.

## 2. Operator — quem executa manualmente hoje?

| Papel | O que faz hoje (sem a flag) |
|-------|------------------------------|
| **Sovereign (admin)** | Abre `https://login.mcorch.com/auth?devLogin` na própria máquina para ver Google/TikTok/Cadastrar. Para expor isso a um terceiro, teria de **editar `Auth.tsx` + `bun run build`** (deploy) e reverter depois. |
| **Revisor externo** | Abre `https://login.mcorch.com/auth` e vê **apenas** e-mail/senha. Não descobre o param. |

Com a flag, o Operator continua sendo o **Sovereign (papel `admin`)** — mas o ato vira um toggle de UI,
sem build e sem deploy.

## 3. Sequence — a ordem exata (cada passo com critério material)

| # | Passo | Critério de sucesso material |
|---|-------|------------------------------|
| 1 | Entrar em `/dashboard/admin` com uma conta `admin` | A página renderiza (não redireciona para `/dashboard`) — `useIsAdmin` verdadeiro |
| 2 | Abrir a aba **Acesso** | O card "Visibilidade da tela de login" lista os 2 switches com o estado ATUAL vindo do banco |
| 3 | Ligar **"Botões de login social (Google · TikTok)"** | O toast confirma; o `useQuery` reinvalida e o switch persiste ligado após F5 |
| 4 | (opcional) Ligar **"Aba de cadastro"** | Idem. Este é um switch SEPARADO de propósito — ver §7 |
| 5 | Abrir `https://login.mcorch.com/auth` em **janela anônima** (sem sessão, sem o param) | Os botões "Continuar com Google" e "Entrar com TikTok" aparecem para um visitante anônimo |
| 6 | Desligar o switch e repetir o passo 5 | Os botões somem — **sem rebuild**, só um refresh |

## 4. Verification gates

| Gate | Comando / observação | Esperado |
|------|----------------------|----------|
| **G1 — leitura anônima funciona** | `curl` PostgREST sem JWT (só apikey publishable) em `public_app_settings` | HTTP 200 com as linhas de flag. Se der `401/permission denied`, a policy/GRANT de `anon` está errada e a tela de login volta ao default fechado |
| **G2 — escrita anônima bloqueada** | mesmo `curl`, agora `PATCH` | HTTP 401/403. **Nunca** 200 |
| **G3 — escrita de usuário comum bloqueada** | JWT de um `viewer` (`scripts/qa/gen-user-jwt.ts`) fazendo `PATCH` | 0 linhas afetadas / erro de RLS |
| **G4 — escrita de admin permitida** | JWT de admin fazendo `PATCH` | 1 linha afetada, `updated_by` = uid do admin |
| **G5 — allowlist de chaves** | `INSERT` de uma chave fora da allowlist como admin | violação do CHECK (`23514`). A tabela é **world-readable**: só chaves declaradas podem existir nela |
| **G6 — fail-closed** | Simular falha da query (rede caída / RLS negando) | A tela de login renderiza **escondendo** os botões. O default nunca é "expor" |
| **G7 — o param continua vivo** | Abrir `/auth?devLogin` com a flag **desligada** | Botões aparecem. O override do Sovereign não regride |
| **G8 — auditoria** | Após um toggle, ler `audit_logs` | 1 linha `action='update_public_app_setting'` com `details.key`, `details.old`, `details.new` |

## 5. Recovery path — falha no passo N

| Falha | Recuperação exata |
|-------|-------------------|
| A tela de login **não muda** depois do toggle | É cache do TanStack Query no browser do visitante ou do Cloudflare no `index.html`. Hard-refresh (`Ctrl+Shift+R`). A flag é lida em runtime — **não** exige `bun run build` |
| G1 falha (anon não lê) | A tela cai no default fechado (nada quebra). Reaplicar o `GRANT SELECT ... TO anon` + a policy `FOR SELECT USING (true)` da migration `20260730120000` |
| Toggle não persiste | Verificar `has_role('admin')` do usuário em `user_roles`. Sem o papel, a policy de escrita nega em silêncio (0 linhas) — o painel mostra erro no toast |
| Ligou por engano e expôs cadastro público | Desligar o switch **"Aba de cadastro"**. Contas criadas nesse intervalo: varrer com `scripts/qa/sweep-smoke-users.ts` (dry-run primeiro) e/ou `/dashboard/admin` → Usuários |
| Precisa reverter TUDO sem UI | `UPDATE public.public_app_settings SET value='false'::jsonb WHERE key LIKE 'auth_%';` com a service key |

## 5-bis. Ordem de deploy (migration ANTES do build)

A tela pública `/auth` passa a ler `public_app_settings` em runtime. A ordem segura é:

1. `npx supabase db push --linked` — aplica a migration `20260730120000` (cria a tabela + seed).
2. Confirmar a leitura anônima (gate **G1** do §4) — o `curl` sem JWT deve devolver as 2 linhas.
3. **Só então** `bun run build` (no repo principal, build = deploy imediato via nginx).

A ordem inversa (build antes da migration) **não derruba o login** — `fetchRows` lança, o `useQuery`
captura (não há `throwOnError` nem ErrorBoundary), `flags` cai no default all-false e a tela renderiza
exatamente como hoje. O único custo é 1 requisição 404 por carregamento do `/auth` enquanto a tabela
não existir (a query usa `retry: false` justamente para não dobrar esse ruído no console do visitante).
Aplicar a migration faz o 404 sumir sozinho no próximo carregamento.

## 5-ter. O guard de regressão é consciente da flag

`scripts/qa/verify-tiktok-login-button.ts` (gate G1 da BoK tiktok-login) valida o invariante
**"o /auth público mostra o botão social ⟺ (`?devLogin` OU a flag ligada)"** — ele lê a flag real de
`public_app_settings` via anon e ajusta a expectativa. Portanto ele fica **verde tanto com a flag
desligada quanto ligada**. Se você vir esse guard RED depois de ligar a flag, o bug é no guard (ou no
env sem anon key), **não** na feature — nunca desligue a flag "para o guard passar".

## 6. Success signal

Um visitante **anônimo**, em janela privada, em `https://login.mcorch.com/auth` **sem query params**,
vê os botões de login social — e o admin consegue tirá-los do ar em 1 clique, sem deploy, com
o evento registrado em `audit_logs`.

## 7. Por que DOIS switches e não um

O `?devLogin` liga três coisas de uma vez: botão Google, botão TikTok **e a aba "Cadastrar"**.
Elas têm consequências diferentes:

- **Login social** — superfície de *autenticação* de quem já existe. Ligar = o que o revisor precisa ver.
- **Cadastro** — superfície de *criação de conta*. Ligar = abrir a porta para qualquer pessoa criar conta
  na plataforma (spam, contas descartáveis, ruído no `/dashboard/admin`).

Fundir as duas num toggle só significaria que ligar o Login Kit para o revisor do TikTok **abre cadastro
público como efeito colateral silencioso**. Os switches são separados para que essa decisão seja
deliberada. O param `?devLogin` continua ligando ambos (comportamento legado preservado).

## 8. Superfícies

| Camada | Arquivo |
|--------|---------|
| Migration (tabela + RLS + allowlist + auditoria) | `supabase/migrations/20260730120000_public_app_settings.sql` |
| SSOT de chaves e defaults (fail-closed) | `src/lib/public-app-settings.ts` |
| Leitura anônima (`/auth`) + leitura/escrita admin | `src/hooks/usePublicAppSettings.ts` |
| Painel de admin | `src/components/admin/AuthVisibilityPanel.tsx` |
| Aba "Acesso" | `src/pages/AdminPage.tsx` |
| Consumo na tela pública | `src/pages/Auth.tsx` |
| Testes unitários | `src/test/public-app-settings.test.ts` |
| Guard E2E (flag-aware) | `scripts/qa/verify-tiktok-login-button.ts` |

## 9. Regra permanente

`public_app_settings` é **legível pelo mundo inteiro por design**. Nunca colocar segredo, chave, token,
endpoint interno ou PII nela. A allowlist do `CHECK` existe justamente para tornar isso impossível por
acidente: uma chave nova exige uma migration — e a migration exige `/security-review`.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

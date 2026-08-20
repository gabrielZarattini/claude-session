# SOP — Runbook de rotação de credenciais expostas

**Status:** ACTIVE · v1.0 · 2026-07-20
**Survival Laws:** Lei 1 (Materialidade) + Lei 2 (Processo Antecipado) + Lei 4 (ORO).
**Nasce de:** o `HANDOFF.md` cita "rotacionar credenciais expostas" como pendência Sovereign em **5 Records
consecutivos** (2026-07-14 → 2026-07-19/20) sem nunca dizer **como**. `docs/bok/crm-inbox/08-quality-metrics.md`
§3.2 nomeia o buraco explicitamente em **`FM-CRM-16`** (RPN 126): *"Rotação COORDENADA como runbook"*. Este
documento é esse runbook.

---

## ⚠️ Regra absoluta deste documento

> **Este runbook NUNCA contém o valor de um segredo.** Ele lista apenas **nomes** — nome do secret no vault,
> nome da coluna, nome do arquivo, nome da variável — e o procedimento. Ao executar:
>
> - **Nunca** `cat`, `echo`, `grep` ou `jq` que **imprima** o valor de um segredo no terminal, no chat ou num log.
> - Ao colar um valor num comando, use uma variável de ambiente lida sem eco (`read -rs NEW_KEY`) e
>   **limpe o histórico** depois (`history -d`), ou cole direto na UI do console (preferido).
> - Um segredo que apareceu no chat de uma sessão de IA **já está exposto** — a rotação não é opcional.
> - Se você precisou ver o valor para conferir, ele acabou de ser exposto de novo. **Não confira: substitua.**

---

## ORO

| Papel | Quem |
|-------|------|
| **Operator** | **Sovereign (Gabriel)** — todo passo aqui exige console externo, senha ou acesso ao host. O Agent pode preparar comandos e **verificar gates**, mas não roda a rotação. |
| **Reviewer** | Sovereign (confirma cada gate de verificação antes de seguir para a próxima credencial) |
| **Owner** | Sovereign — blast radius = rails de produção do Usuário Zero (inbox WhatsApp, geração de vídeo, malha semântica, briefing noturno) |

---

## Inventário das credenciais (ordenado por risco)

Cada linha foi confirmada materialmente antes de entrar aqui — a coluna *Evidência* aponta o `file:line` ou
o comando que provou que a credencial existe e onde vive. **Nada aqui é inventado.**

| # | Credencial (NOME) | Onde vive | Consumidores | Risco se comprometida | Evidência |
|---|-------------------|-----------|--------------|-----------------------|-----------|
| **R1** | Segredo do app Meta — **3 superfícies** (ver ⚠️ abaixo): env `META_APP_SECRET` · env `INSTAGRAM_APP_SECRET` · linha `social_app_config` (provider `instagram`) | (1)+(2) secrets do **vault de Edge Functions** (`Deno.env`) · (3) linha no banco, cifrada no Vault, tier admin global (`/dashboard/admin`) | `whatsapp-webhook` (prefere `META_APP_SECRET`) · `instagram-webhook` (prefere **`INSTAGRAM_APP_SECRET`**) · `meta-privacy` (prefere a **linha do banco**) | **Máximo.** É a **fronteira de confiança** dos webhooks `verify_jwt=false`. Quem tem o secret forja HMAC válido e **injeta mensagens falsas** na inbox de qualquer tenant. | `supabase/functions/whatsapp-webhook/index.ts:110` · `instagram-webhook/index.ts:32` · `meta-privacy/index.ts:25-38` · `_shared/social-app-config.ts:42` |
| **R2** | Service account Vertex (`gabrielai-veo`) — chave privada JSON | Linha cifrada no **Vault** via `user_provider_keys` (`provider='google'`, `api_key` = referência Vault) | `canvas-execute` (branch `veo`, `authType='vertex-sa'`), `veo-poll` | **Alto — financeiro direto.** Chave de SA do GCP = geração de vídeo Veo cobrada em USD real na conta do Sovereign, e alcance a qualquer API que o SA tenha role. | `supabase/migrations/20260714030000_user_provider_keys_pool.sql:16-28` · `supabase/functions/canvas-execute/index.ts:1124-1136` · lembrete `rotate-vertex-sa` (`severity='critical'`) |
| **R3** | Token de usuário Meta de longa duração (**EAA**) | Coluna `meta_config.long_lived_token` (per-user, RLS `auth.uid()`) | `whatsapp-templates` (list/create/delete/send), rails Meta | **Alto.** Envia WhatsApp/publica em nome do tenant → risco de **ban da conta de plataforma** + custo per-message real. Expira sozinho em 60d (`token_expires_at`). | `supabase/migrations/20260530210000_meta_api_foundation.sql:31,39` · `src/components/settings/MetaConfigCard.tsx:53` |
| **R4** | Token do Instagram (**IGAA**) | Coluna `social_accounts.access_token` (cifrada; leitura server-side via `decrypted_social_accounts`) | `connect-instagram-token`, `publish-social`/IG rails | **Alto.** Publica no perfil do tenant. `IGAA` ≠ `EAA` — é token de Instagram Login e o `graph.facebook.com` rejeita. | `supabase/migrations/20260402014040_*.sql:82` · `src/components/social/InstagramTokenCard.tsx` · `src/hooks/useConnectInstagramToken.ts:14` |
| **R5** | Chave Gemini / Google AI Studio | (a) Coluna per-user `user_api_keys.google_api_key` (Vault) · (b) secret de sistema `MESH_EMBED_GEMINI_KEY` no vault de Edge Functions | (a) rails BYOK de geração · (b) `embed-mcorch-node`, `search-constellation` | **Médio-alto.** Consumo faturado na conta Google do Sovereign + esgotamento de quota do embedding da malha (o embedding de **todo nó novo** para de funcionar). | `src/pages/SettingsPage.tsx:336` · `supabase/functions/embed-mcorch-node/index.ts` · lembrete `rotate-gemini-key` (`severity='critical'`) |
| **R6** | Token do bot Telegram | Arquivo do host `/home/ubuntu/.openclaw/secrets.json`, campo `.keys.telegramBotToken` (chmod 600) | `scripts/lib/notify-telegram.sh`, `scripts/morning-briefing.sh` (guardião MAPE-K + briefing 03:30) | **Médio.** Quem tem o token **lê e escreve** no canal do Sovereign — pode se passar pelo guardião (mensagens falsas de "tudo saudável"). Não custa dinheiro. | `scripts/lib/notify-telegram.sh:17` · `scripts/morning-briefing.sh:67-68` · lembrete `rotate-telegram-token` (`severity='warning'`) |

**Lembretes já semeados no banner do `/dashboard/admin`** (`admin_reminders`, slugs `rotate-vertex-sa`,
`rotate-gemini-key`, `rotate-telegram-token`) —
`supabase/migrations/20260716210000_global_app_credentials_admin_tier.sql:120-129`. **R1/R3/R4 (Meta) NÃO têm
lembrete semeado** — a pendência deles só vive na prosa do `HANDOFF.md`. Semear (ou fechar) faz parte do §Fechamento.

---

## Sequence — procedimento por credencial

Cada bloco segue: **(a) onde vive → (b) console de emissão → (c) comando de atualização → (d) gate de
verificação material → (e) blast radius durante a janela → (f) rollback.**

---

### R1 — `META_APP_SECRET`

**(a) Onde vive — ⚠️ TRÊS superfícies, não uma.** O app Meta é **um só** ("UM app, DUAS APIs"), mas o mesmo
segredo é lido de três lugares independentes. **Redefinir no console invalida o segredo para os três ao mesmo
tempo** — atualizar só um deixa os outros dois defasados e **silenciosamente surdos**:

| # | Superfície | Quem prefere ela | Evidência |
|---|-----------|------------------|-----------|
| S1 | env `META_APP_SECRET` | `whatsapp-webhook` (`META_APP_SECRET \|\| INSTAGRAM_APP_SECRET`) | `whatsapp-webhook/index.ts:110` |
| S2 | env `INSTAGRAM_APP_SECRET` | `instagram-webhook` (`INSTAGRAM_APP_SECRET ?? META_APP_SECRET` — **o IG prefere ESTE**) | `instagram-webhook/index.ts:32` |
| S3 | linha `social_app_config` (provider `instagram`, `user_id IS NULL` = global admin), `client_secret` cifrado no Vault | `meta-privacy` — a ordem de candidatos é **banco → `INSTAGRAM_APP_SECRET` → `META_APP_SECRET`**, ou seja **a linha do banco VENCE os dois envs** | `meta-privacy/index.ts:25-38` · `_shared/social-app-config.ts:8-9,42` |

> **Por que isso importa (modo de falha real, não hipotético):** se você rotacionar apenas `META_APP_SECRET`,
> o gate de verificação abaixo (mensagem de WhatsApp → inbox) fica **VERDE** — porque `whatsapp-webhook`
> prefere exatamente a superfície que você atualizou. Enquanto isso `instagram-webhook` continua validando
> contra um `INSTAGRAM_APP_SECRET` morto e **rejeita todo inbound do Instagram**, e `meta-privacy` valida
> contra uma linha de banco morta e **falha os callbacks de deauth/deleção** (obrigação LGPD/Meta). Ambos
> falham em silêncio, com o gate verde na sua frente. **Rotacione as três, ou não rotacionou.**

**(b) Console:** [developers.facebook.com](https://developers.facebook.com) → o app MCORCH →
**Configurações → Básico → Chave Secreta do Aplicativo** → *Redefinir*. **Copie o novo valor direto do console
para a UI do Supabase** (não passe pelo terminal, não cole no chat).

**(c) Comando de atualização:**

```bash
# Preferido: Supabase Dashboard → Edge Functions → Secrets → editar os DOIS nomes (cola direta, zero eco).
# Alternativa CLI — o MESMO valor novo vai para as duas superfícies de env (S1 e S2):
read -rs NEW_META_SECRET
npx supabase secrets set META_APP_SECRET="$NEW_META_SECRET"
npx supabase secrets set INSTAGRAM_APP_SECRET="$NEW_META_SECRET"   # S2 — NÃO pule: o IG prefere este
unset NEW_META_SECRET
history -d $((HISTCMD-1)) 2>/dev/null || true
```

> ⚠️ **Nota de exposição do `secrets set`:** `read -rs` mantém o valor fora do histórico, mas ele aparece no
> **argv do processo** (visível por `ps` a outros usuários do host durante a chamada). Em host compartilhado,
> **prefira o Dashboard**.

**S3 — a linha do banco (não esqueça):** `/dashboard/admin` → tier global de credenciais de app → provider
**Instagram** → colar o mesmo segredo novo em `client_secret` → salvar. A UI escreve cifrado no Vault. Se
essa linha existir e ficar defasada, `meta-privacy` continua quebrado **mesmo com os dois envs corretos**
(ela vence os envs). Se o Sovereign **não usa** o tier global, confirme que não há linha ativa:

```sql
-- Existe linha global de app Instagram? (só metadado — nunca selecione o segredo)
select provider, user_id is null as is_global, is_active, updated_at
  from social_app_config where provider = 'instagram';
-- 0 linhas ⇒ S3 não se aplica; ≥1 linha ativa ⇒ S3 é OBRIGATÓRIA.
```

> Secrets do vault são lidos por `Deno.env` **no start do worker**. Após o `secrets set`, force um redeploy
> das 3 funções consumidoras para garantir que peguem o valor novo:
> `npx supabase functions deploy whatsapp-webhook` (idem `meta-privacy`, `instagram-webhook`).
> **Não use `deploy` em bulk** — o projeto está no cap de ~99 funções e o bulk devolve **402**; deploy single é isento.

**(d) Gate de verificação (material):** o Sovereign envia **uma mensagem real do celular** para o número
WhatsApp e ela **aparece em `/dashboard/inbox`**. Esse é o gate porque o modo de falha histórico foi
exatamente esse: com o app secret defasado, a Meta entregava o webhook e o MCORCH devolvia
`invalid_signature` em **todo** inbound — a inbox ficava silenciosamente surda (Record 2026-07-18 do `HANDOFF.md`).

⚠️ **Este gate sozinho é INSUFICIENTE** — ele exercita apenas S1 (`whatsapp-webhook` prefere `META_APP_SECRET`).
Um WhatsApp que chega **não prova nada** sobre S2/S3. Os três gates, um por superfície:

| Superfície | Gate | PASS |
|-----------|------|------|
| **S1** | Sovereign envia mensagem real do celular → `/dashboard/inbox` | mensagem aparece na thread |
| **S2** | Enviar um **DM/comentário real no Instagram** conectado (ou reenviar o evento de teste do painel de Webhooks do app Meta para o campo do IG) | o evento é aceito; **nenhuma** linha `invalid_signature` do lado do IG |
| **S3** | Só se `social_app_config` tiver linha ativa: disparar o callback de **deauthorize/data-deletion** pelo painel do app Meta | `meta-privacy` responde 200, não 401 |

Gate secundário consolidado, do lado do servidor (o `event` é o sinal específico — `pulse("degraded",
"invalid_signature")` em `whatsapp-webhook/index.ts:78,117`):

```sql
-- Nenhuma falha de assinatura nos 10 minutos após a rotação, em NENHUM webhook.
select service, event, count(*)
  from infra_health_logs
 where created_at > now() - interval '10 minutes'
   and (event ilike '%signature%' or status <> 'healthy')
   and service in ('crm-inbox', 'instagram-webhook', 'meta-privacy')
 group by 1, 2;
-- Esperado: 0 linhas
```

**(e) Blast radius durante a janela:** entre *Redefinir* no console da Meta e o redeploy das funções, **todo
inbound do WhatsApp/Instagram é rejeitado por HMAC**. Mensagens nesse intervalo dependem do retry da Meta —
**não conte com elas**. Janela típica: segundos a poucos minutos. Rotacione **fora do horário comercial**.

**(f) Rollback:** o valor antigo é **irrecuperável** depois do *Redefinir* (a Meta não mostra o anterior). Não
há rollback — só *roll-forward*: se o gate falhar, redefina de novo no console e repita (c)+(d). **Por isso R1
vai primeiro e sozinho, com o Sovereign na frente do celular para testar.**

---

### R2 — Service account Vertex (`gabrielai-veo`)

**(a) Onde vive:** `user_provider_keys` (`provider='google'`), com o JSON da SA cifrado no Vault; o
`metadata` carrega `vertex_project`/`vertex_location`. Superfície: **Configurações → Conectores → pool de
chaves BYOK** (`ProviderKeysCard`).

**(b) Console:** [console.cloud.google.com](https://console.cloud.google.com) → **IAM e administrador → Contas
de serviço** → a SA do Veo → **Chaves → Adicionar chave → Criar nova chave (JSON)**. Baixe o JSON.
**Não abra o arquivo no editor nem cole o conteúdo no chat.**

**(c) Comando de atualização — atenção, é *adicionar + remover*, não editar:**
o hook `useProviderKeys` **não expõe update de `api_key`** (só `is_active`/`priority`/`label` —
`src/hooks/useProviderKeys.ts:62-67`). Portanto:

1. `/dashboard/settings` → **Conectores** → adicionar nova credencial `google`, label novo
   (ex.: `vertex-sa-2026-07`), colando o JSON no campo (a UI aceita o SA JSON — `ImageToVideoInspector`
   já lê `authType='vertex-sa'`), com `priority` **menor** que a antiga (menor = preferida).
2. Rodar o gate (d) com a nova.
3. Só então **desativar** (`is_active=false`) e **excluir** a credencial antiga na mesma tela.
4. **Voltar ao console do GCP e DESABILITAR/EXCLUIR a chave antiga** — este passo é o que de fato
   revoga o acesso. Trocar a linha no banco sem revogar no Google **não rotacionou nada**.

**(d) Gate de verificação:** mint de token OAuth a partir da SA — **zero custo**, não gera vídeo:

Espelha em bash o que `supabase/functions/_shared/google-sa-auth.ts` faz em produção (JWT RS256 →
`https://oauth2.googleapis.com/token`). **Não imprime o token** — só o status e a presença do campo.

```bash
# Uso: ./mint-sa-token.sh /caminho/da/sa.json     (requer openssl + jq + curl)
set -euo pipefail
SA="$1"
b64url() { openssl base64 -A | tr '+/' '-_' | tr -d '='; }
now=$(date +%s); exp=$((now+3600))
hdr=$(printf '{"alg":"RS256","typ":"JWT"}' | b64url)
iss=$(jq -r .client_email "$SA"); aud=$(jq -r .token_uri "$SA")
cls=$(printf '{"iss":"%s","scope":"https://www.googleapis.com/auth/cloud-platform","aud":"%s","exp":%s,"iat":%s}' \
      "$iss" "$aud" "$exp" "$now" | b64url)
sig=$(printf '%s.%s' "$hdr" "$cls" | openssl dgst -sha256 -sign <(jq -r .private_key "$SA") | b64url)
resp=$(curl -s -w '\n%{http_code}' -X POST "$aud" \
  -d grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer \
  --data-urlencode "assertion=${hdr}.${cls}.${sig}")
echo "HTTP=$(tail -n1 <<<"$resp")"
echo "access_token_present=$(jq -e 'has("access_token")' <<<"$(sed '$d' <<<"$resp")" >/dev/null 2>&1 && echo yes || echo no)"
echo "error=$(jq -r '.error // "none"' <<<"$(sed '$d' <<<"$resp")" 2>/dev/null)"
```

**Como ler o resultado:**

| Saída | Significado |
|-------|-------------|
| `HTTP=200` · `access_token_present=yes` | ✅ Gate verde — a chave nova assina e o Google a aceita. |
| `HTTP=400` · `error=invalid_grant` | A requisição está bem-formada, mas **esta SA/chave não é válida** (revogada, SA excluída, ou chave errada). |
| `HTTP=400` · `error=invalid_request` / `unsupported_grant_type` | Problema no **script/JSON**, não na credencial — confira que o `$SA` é o JSON da SA. |

> **Materialidade da mecânica deste script (Lei 1):** as linhas acima foram **executadas nesta sessão** contra
> uma SA **descartável, gerada localmente** (`openssl genpkey`, projeto inexistente) e devolveram
> `HTTP=400 · access_token_present=no · error=invalid_grant`. `invalid_grant` — e não `invalid_request` —
> prova que o Google **parseou e verificou a forma do JWT**, ou seja o script está correto; o único motivo da
> recusa foi a SA falsa. **Nenhuma credencial real foi usada nesta verificação.** O caminho `HTTP=200` só pode
> ser observado pelo Sovereign com a SA verdadeira.

Gate de aplicação (o que prova o rail vivo, mas **custa dinheiro real**): submeter uma geração Veo pelo nó
Imagem→Vídeo e ver `engine=veo-vertex` + débito exato. **Só faça isso se o mint de token não for suficiente
para o Reviewer** — uma geração Vertex custa 267 mco. Sinal de falha inequívoco: `canvas-execute` devolve
**HTTP 402 `vertex_auth_failed`** (`supabase/functions/canvas-execute/index.ts:1136,1176-1177`).

**(e) Blast radius:** enquanto a nova não estiver ativa, o caminho Veo/Vertex fica em 402
`vertex_auth_failed`. Nenhum job em voo é perdido — o `veo-poll` **re-resolve a MESMA chave do submit** por
`(provider_key_id, key_source)`. **⚠️ Consequência material: não exclua a credencial antiga enquanto houver
job Veo em `running`** — o poll perderia a chave e o job seria estornado apesar de o vídeo existir.

**Query da pré-condição — jobs Veo em voo.** Os jobs Veo vivem em **`generations`** (`veo-poll/index.ts:83-84`
lê dali; `canvas-execute/index.ts:1301` grava o `operation_id` ali; schema em
`20260702190000_spaces_generations_ledger.sql:31-45`). **Não é `video_renders`** — essa é a fila do HyperFrames,
outro trilho, e a coluna lá nem se chama `status`. Consultar a tabela errada devolve um `0` falso e leva
exatamente ao estorno descrito acima:

```sql
-- Jobs assíncronos de vídeo (LRO) ainda em voo. Precisa ser 0 antes de excluir a credencial antiga.
select count(*) from generations
 where status = 'running' and operation_id is not null;
-- Esperado: 0
```

**(f) Rollback:** trivial e seguro — reative a credencial antiga (`is_active=true`) **desde que ainda não
tenha sido excluída no console do GCP**. Por isso a ordem é: banco primeiro, console do GCP **por último**.

---

### R3 — Token Meta de longa duração (EAA)

**(a) Onde vive:** `meta_config.long_lived_token` (uma linha por tenant, `UNIQUE (user_id)`).

**(b) Console:** [developers.facebook.com](https://developers.facebook.com) → **Ferramentas → Explorador da
API Graph** → gerar token de usuário com os escopos do WhatsApp/Business → **trocar por token de longa
duração (60d)**. Gotcha material já pago em sessão anterior: tem de ser **`EAA`** (token do Meta/Facebook).
Um **`IGAA`** (Instagram Login) é rejeitado pelo `graph.facebook.com`.

**(c) Comando de atualização:** `/dashboard/settings` → aba **Social** → card Meta → campo
**"Token de Longa Duração (User Token)"** → colar → salvar (`MetaConfigCard.tsx:112-118`). Sem CLI, sem SQL.

**(d) Gate de verificação:**

1. Na UI: `/dashboard/settings` → Social → o card deixa de mostrar `requires_reauth`.
2. Material, custo zero: **Configurações → WhatsApp → listar templates** (`whatsapp-templates` action `list`)
   retorna **200 com a lista de templates aprovados**. Uma listagem vazia por erro de auth vem como 4xx, não
   como lista vazia — leia o status, não a UI.
3. Opcional (também zero custo): `GET /me` da Graph API com o `phone_number_id` deve anunciar o número como
   `CLOUD_API` / `LIVE` — foi assim que o rail foi provado na primeira vez.

**(e) Blast radius:** durante a troca, **envio** de WhatsApp falha (`whatsapp-templates` sem token válido).
**Inbound continua funcionando** — o inbound depende do `META_APP_SECRET` (R1), não deste token. O composer
bloqueia sozinho com `meta_config.requires_reauth=true` + CTA (`FR-CRM-021`), então o usuário vê um erro
honesto em vez de uma mensagem perdida.

**(f) Rollback:** o token antigo continua válido no lado da Meta até expirar ou até você o invalidar
explicitamente no console. Se guardou o anterior **num gerenciador de senhas** (nunca no chat), re-cole. Caso
contrário: roll-forward, gerando outro.

---

### R4 — Token Instagram (IGAA)

**(a) Onde vive:** `social_accounts.access_token` (cifrada; edge fns leem por `decrypted_social_accounts`).

**(b) Console:** o token IGAA sai do fluxo de **Instagram Login** do app Meta (ou do Explorador da API Graph
apontando para `graph.instagram.com`).

**(c) Comando de atualização:** `/dashboard/social` → card **"Conectar Instagram por token"**
(`InstagramTokenCard`) → colar → a edge fn `connect-instagram-token` **valida server-side** em
`graph.instagram.com/me` antes de persistir. A identidade gravada é sempre `auth.uid()` — o cliente não
escolhe o dono.

**(d) Gate de verificação:** o próprio card **é** o gate: se o token for inválido, a fn recusa e **nada é
gravado** (fail-closed). Sucesso = o card passa a exibir a conta conectada, com `is_active=true`.
**Não use o relógio de expiração como sinal de saúde** — o sinal canônico de conexão viva é `is_active`, não
o TTL do token.

**(e) Blast radius:** publicação no Instagram falha entre a revogação e a reconexão. Posts **agendados** que
caírem nessa janela vão para `failed` — verifique `scheduled_posts` depois.

**(f) Rollback:** reconectar. Se quiser começar limpo, `disconnect_social(p_account_id)`
(`src/hooks/useSocialAccounts.ts:48`) apaga a linha **e revoga o segredo órfão no Vault** — é o caminho
correto, `.delete()` cru deixa segredo órfão.

---

### R5 — Chave Gemini / Google AI Studio

**(a) Onde vive — duas superfícies distintas, rotacione as duas:**
- per-user BYOK: `user_api_keys.google_api_key` (Vault) — **Configurações → IA (API Keys)**, campo
  *"Google API Key (Gemini)"* (`SettingsPage.tsx:336`);
- sistema: secret `MESH_EMBED_GEMINI_KEY` no vault de Edge Functions, consumido por `embed-mcorch-node` e
  `search-constellation` (fluxos sem `auth.uid()`).

**(b) Console:** [aistudio.google.com](https://aistudio.google.com) → **API keys** → criar nova → **excluir a
antiga** (a exclusão é o que revoga).

**(c) Comandos de atualização:**

```bash
# Superfície de sistema (malha semântica):
read -rs NEW_GEMINI && npx supabase secrets set MESH_EMBED_GEMINI_KEY="$NEW_GEMINI" && unset NEW_GEMINI
npx supabase functions deploy embed-mcorch-node
npx supabase functions deploy search-constellation      # single, nunca bulk (cap de fns → 402)
```

Superfície per-user: pela UI (Configurações → IA). ⚠️ **Gotcha conhecido:** a view `user_api_keys` é
**mascarada** — salvar um campo vazio **não limpa** a chave. Para trocar, escreva o valor novo; para remover,
use o caminho de disconnect da coluna (ver `docs/processes/credential-disconnect-clear.md`).

**(d) Gate de verificação:**

1. **Malha (sistema):** inserir um nó qualquer em `mcorch_nodes` e confirmar que o `embedding` foi
   preenchido (768 dims). É o teste definitivo — se a chave estiver quebrada, o nó nasce sem embedding.
   ```sql
   select id, (embedding is not null) as embedded
     from mcorch_nodes order by created_at desc limit 1;
   ```
2. **BYOK (per-user):** gerar **uma imagem barata** no Canvas/Spaces com motor Google. Um 402/401 do
   provider prova chave inválida; um asset gerado prova chave válida.

**(e) Blast radius:** com a chave antiga revogada e a nova não propagada, **todo nó novo da malha nasce sem
embedding** (busca semântica degrada silenciosamente) e os rails BYOK Google devolvem 402. Nada quebra de
forma barulhenta — por isso o gate (d.1) é obrigatório, não opcional.

**(f) Rollback:** nenhum (chave excluída no AI Studio não volta). Roll-forward: gere outra e repita.
**Mitigação:** crie a chave nova **antes** de excluir a antiga, e só exclua depois do gate verde.

---

### R6 — Token do bot Telegram

**(a) Onde vive:** `/home/ubuntu/.openclaw/secrets.json`, campo `.keys.telegramBotToken` (chmod 600, mesmo
owner do processo). **Não** está no Supabase.

**(b) Console:** **@BotFather** no Telegram → `/revoke` → escolher o bot → ele devolve um token novo e
**invalida o antigo imediatamente**.

**(c) Comando de atualização:** editar o JSON **sem imprimir o conteúdo**:

```bash
# Edição in-place preservando o resto do arquivo. NUNCA `cat` este arquivo.
read -rs NEW_TG_TOKEN
jq --arg t "$NEW_TG_TOKEN" '.keys.telegramBotToken = $t' /home/ubuntu/.openclaw/secrets.json \
  > /home/ubuntu/.openclaw/secrets.json.new \
  && chmod 600 /home/ubuntu/.openclaw/secrets.json.new \
  && mv /home/ubuntu/.openclaw/secrets.json.new /home/ubuntu/.openclaw/secrets.json
unset NEW_TG_TOKEN
```

**(d) Gate de verificação (custo zero, e o script já é honesto):**

```bash
bash scripts/lib/notify-telegram.sh "rotação de token: teste de sanidade"
echo "exit=$?"     # 0 = entregue (HTTP 200) · 1 = Telegram recusou · 2 = token ausente
```

O `notify-telegram.sh` foi escrito com códigos de saída materiais **de propósito** (`:9` — *"uma notificação
que não saiu NUNCA pode parecer enviada"*). Confirme também a chegada da mensagem no canal — exit 0 + mensagem
visível = gate verde.

**(e) Blast radius:** entre o `/revoke` e a escrita do arquivo, o **briefing matinal (03:30 BRT)** e os alertas
do guardião MAPE-K não são entregues. Se a janela cruzar 03:30, o briefing daquele dia **se perde**
silenciosamente. Rotacione fora dessa faixa.

**(f) Rollback:** nenhum — `/revoke` é irreversível. Roll-forward: `/revoke` de novo. Risco baixo (o bot é
interno, sem custo).

---

## Verification gates (consolidado — nenhum "rotacionado" sem TODOS os verdes da linha)

| Credencial | Gate obrigatório | Sinal de PASS |
|------------|------------------|---------------|
| R1 segredo do app Meta | **os 3**: (S1) mensagem real do celular → `/dashboard/inbox` · (S2) evento real do Instagram aceito · (S3) callback deauth → `meta-privacy` 200 | os três verdes **+** 0 linhas na query consolidada de `infra_health_logs`. **S1 verde sozinho NÃO fecha R1.** |
| R2 SA Vertex | script `mint-sa-token.sh` (R2 §(d) — mecânica provada em sessão) | `HTTP=200` **e** `access_token_present=yes` (valor **nunca** impresso); ausência de 402 `vertex_auth_failed` |
| R3 Token EAA | `whatsapp-templates` action `list` | HTTP 200 com lista; `meta_config.requires_reauth = false` |
| R4 Token IGAA | `connect-instagram-token` aceita e persiste | card mostra conta conectada, `is_active = true` |
| R5 Chave Gemini | nó novo na malha nasce embedado | `embedding is not null` no `SELECT` do nó mais recente (768 dims) |
| R6 Token Telegram | `notify-telegram.sh` | `exit=0` **e** mensagem visível no canal |

---

## Recovery path

| Sintoma após a rotação | Causa provável | Ação |
|------------------------|----------------|------|
| Inbox parou de receber | `META_APP_SECRET` novo no vault mas funções não redeployadas | `npx supabase functions deploy whatsapp-webhook` (single) e re-testar o gate R1 |
| `HTTP 402` no deploy de function | tentativa de deploy em **bulk** com o projeto no cap de funções | deployar **uma função por vez** (`deploy <fn>`) — single é isento do cap |
| Veo devolve `vertex_auth_failed` | credencial nova inativa, `priority` maior que a velha, ou chave revogada no GCP antes do gate | reativar a antiga (se ainda existir no GCP), corrigir `priority`, re-rodar o gate R2 |
| Job Veo em voo foi estornado | credencial antiga excluída com job em `running` — o `veo-poll` perdeu a chave do submit | não há recuperação do job; **prevenir**: nunca excluir credencial com job em `running` |
| Nós novos sem embedding | `MESH_EMBED_GEMINI_KEY` defasada ou funções não redeployadas | re-set do secret + `deploy embed-mcorch-node` + re-rodar gate R5 |
| Briefing matinal não chegou | token do Telegram revogado e arquivo não atualizado a tempo | corrigir `secrets.json` + gate R6; o briefing daquele dia não é recuperável |
| Salvei campo vazio para "limpar" e a chave continua lá | `user_api_keys` é **view mascarada** — vazio não limpa | usar o caminho de disconnect (`docs/processes/credential-disconnect-clear.md`) |

---

## Success signal

Todas as 6 linhas da tabela de gates verdes **na mesma janela**, mais:

1. `admin_reminders` com `resolved_at`/`resolved_by` preenchidos para `rotate-vertex-sa`, `rotate-gemini-key`
   e `rotate-telegram-token` — o banner do `/dashboard/admin` **some sozinho** quando resolvidos. Banner ainda
   visível = rotação **não** concluída, independentemente do que o relatório diga.
2. Uma linha nova no `HANDOFF.md` registrando **data, quais credenciais** foram rotacionadas e **qual gate
   provou cada uma** — sem valores, só nomes.

---

## Ordem recomendada de execução pelo Sovereign

Ordenada por risco decrescente, com as dependências e as janelas de indisponibilidade já consideradas.
Cada passo termina no seu gate: **não avance com um gate vermelho.**

| Ordem | Credencial | Por que aqui | Pré-condição |
|:-----:|------------|--------------|--------------|
| **1º** | **R1 `META_APP_SECRET`** | Maior blast radius (forja de inbound cross-tenant) e o único cuja falha é **silenciosa**. Vai primeiro e **sozinho**. | Sovereign **com o celular na mão** para enviar a mensagem de teste. Fora do horário comercial. |
| **2º** | **R2 SA Vertex** | Risco financeiro direto em USD. | **Nenhum job Veo em `running`** — ver a query exata em R2 §(e). ⚠️ É a tabela **`generations`**, não `video_renders`. Criar a nova **antes** de excluir a antiga no GCP. |
| **3º** | **R3 Token EAA** | Depende de R1 estar verde — trocar os dois juntos torna impossível saber qual quebrou. | R1 com gate verde. |
| **4º** | **R4 Token IGAA** | Mesma família Meta, superfície menor. Agrupado com R3 na mesma sessão de console. | R3 concluída. Checar `scheduled_posts` depois. |
| **5º** | **R5 Chave Gemini** | Duas superfícies (BYOK + malha); a degradação é silenciosa, então exige o gate do embedding. | Criar a chave nova **antes** de excluir a antiga no AI Studio. |
| **6º** | **R6 Token Telegram** | Menor risco, sem custo. Por último **de propósito**: se algo acima quebrar, o canal de alerta do guardião ainda está vivo para avisar. | **Não** executar entre 03:00 e 04:00 BRT (janela do briefing). |

**Fechamento (após o 6º):** marcar os 3 `admin_reminders` como resolvidos, semear (ou dispensar
explicitamente) lembretes para R1/R3/R4 — que hoje **não têm linha em `admin_reminders`** — e registrar o
resultado no `HANDOFF.md`.

---

## Anti-patterns proibidos

- ❌ Imprimir, colar ou logar o **valor** de qualquer segredo — inclusive "só para conferir".
- ❌ Rotacionar duas credenciais da mesma família (Meta) **na mesma janela** sem gate intermediário: quando
  quebra, não dá para saber qual foi.
- ❌ Declarar "rotacionado" sem o gate material da linha correspondente. Trocar a linha no banco **não é**
  rotação — rotação só existe quando a credencial antiga foi **revogada no console de origem**.
- ❌ Excluir a credencial antiga **antes** do gate verde da nova (vale para R2 e R5 especialmente).
- ❌ `npx supabase functions deploy` em bulk — o cap de funções devolve **402** e o deploy inteiro morre.
- ❌ Confiar no relógio de expiração como sinal de saúde de conexão social — o sinal é `is_active`.
- ❌ **Rotacionar só `META_APP_SECRET` e declarar R1 fechada.** São 3 superfícies (env `META_APP_SECRET`, env
  `INSTAGRAM_APP_SECRET`, linha `social_app_config`) e o gate do WhatsApp fica **verde** exercitando apenas a
  primeira — o Instagram e o `meta-privacy` morrem em silêncio. Cada superfície tem gate próprio.
- ❌ Consultar `video_renders` para saber se há job Veo em voo — o ledger do Veo é **`generations`**. Tabela
  errada ⇒ `0` falso ⇒ credencial excluída com job vivo ⇒ estorno de um vídeo que existe.
- ❌ Rodar qualquer passo deste runbook **sem o Sovereign**: o Operator aqui é ele, não o Agent.

---

## Connection to Survival Laws

**Lei 1:** a prova de rotação é o **gate material** (mensagem que chega, `SELECT` que retorna, exit 0 do
script) — nunca o comando que rodou. **Lei 2:** este SOP existe porque o `HANDOFF.md` repetiu "rotacionar
credenciais" cinco vezes sem processo — obstáculo recorrente vira processo. **Lei 4:** o Operator é o
Sovereign; o Agent prepara e verifica, não executa.

## Cross-references

| Recurso | Caminho |
|---------|---------|
| Modo de falha que origina este runbook (`FM-CRM-16`, RPN 126) | `docs/bok/crm-inbox/08-quality-metrics.md` §3.2 |
| View mascarada / limpeza de credencial | `docs/processes/credential-disconnect-clear.md` |
| Resolução per-user de credenciais Meta | `docs/processes/meta-credential-resolution.md` |
| Tier global de credenciais de app (admin) | `docs/processes/admin-global-app-credentials.md` |
| Materialidade de build/deploy (gates de deploy de function) | `docs/processes/build-deploy-materiality.md` |
| Banner de lembretes | `src/components/admin/AdminRemindersBanner.tsx` · `src/hooks/useAdminReminders.ts` |

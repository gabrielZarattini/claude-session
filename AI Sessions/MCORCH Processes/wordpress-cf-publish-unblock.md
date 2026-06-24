# SOP — Desbloqueio do publish WordPress atrás do Cloudflare managed challenge

> **Slug:** `wordpress-cf-publish-unblock` · **Criado:** 2026-06-22 · **Lei 2 (Processo Antecipado)**
> **Origem:** diagnóstico material 2026-06-22 — `https://www.mcorch.com/wp-json/*` retorna **HTTP 403 `cf-mitigated: challenge`** em toda requisição (GET+POST, www+apex, auth+anon). A edge function `publish-wordpress` faz `fetch` server-to-server (Deno, sem engine JS) e **não resolve** o desafio JS do Cloudflare → todo POST a `/wp-json/wp/v2/posts` morre em 403 → nenhum post criado → a função devolve 502 ao chamador (`orchestrate-content` / Viral Autopilot). Este é o **blocker de saída visível** do flywheel de conteúdo.

## Modelo da solução (defense-in-depth)

Não basta "abrir o `/wp-json` no Cloudflare" — isso exporia enumeração (`/wp-json/wp/v2/users`) e brute-force de Basic Auth sem o atrito do challenge. A solução é um **Skip gated por segredo compartilhado**:

1. A edge function envia o header `X-MCORCH-Publish: <segredo>` **apenas** quando o host de destino bate com `WP_PUBLISH_SECRET_HOST` (fail-closed — nunca envia para um `wp_site_url` arbitrário de tenant; ver `supabase/functions/publish-wordpress/index.ts`, gate de host adicionado 2026-06-22 + `/security-review` HIGH fechado na mesma sessão).
2. Uma regra WAF Custom do Cloudflare faz **Skip** do managed challenge **somente** quando o path é `/wp-json/*` **E** o header bate com o segredo. Sem o header correto, o challenge continua valendo para o resto do mundo.

## ORO

- **Operator:** Sovereign (Gabriel) — ações no painel Cloudflare + `supabase secrets` (valores de segredo não estão no alcance do agente).
- **Reviewer:** `/security-review` (já passou SAFE sobre a edge function); o próprio gate de verificação abaixo.
- **Owner:** Sovereign — blast radius = superfície `/wp-json` do site de produção + a saída visível do conteúdo monetizado.

## Sequence (passos numerados, cada um com critério material)

### Step 1 — Gerar o segredo compartilhado (Operator: Sovereign)
```bash
openssl rand -hex 32     # copie o valor (64 chars hex)
```
**Sucesso:** uma string hex de 64 chars na mão.

### Step 2 — Provisionar os secrets na edge function (Operator: Sovereign)
```bash
npx supabase secrets set \
  WP_PUBLISH_SECRET=<o-hex-do-step-1> \
  WP_PUBLISH_SECRET_HOST=www.mcorch.com \
  --project-ref bcyvddsykvehvpwstlfa
```
> `WP_PUBLISH_SECRET_HOST` deve ser **exatamente** o host canônico do `wp_site_url` do tenant (hoje `www.mcorch.com`). O gate da função é match exato de `new URL(apiBase).hostname` — sem isso, o header **nunca** é anexado (fail-closed).

**Verificação material:**
```bash
npx supabase secrets list --project-ref bcyvddsykvehvpwstlfa | grep -E "WP_PUBLISH_SECRET(_HOST)?"
```
**Sucesso:** as duas linhas aparecem (valor mostrado como digest).

### Step 3 — Criar a regra WAF Custom no Cloudflare (Operator: Sovereign)
Painel Cloudflare → zona `mcorch.com` → **Security → WAF → Custom rules → Create rule**:

- **Rule name:** `MCORCH publish-wordpress Skip (header-gated)`
- **Expression (Edit expression):**
  ```
  (http.host eq "www.mcorch.com" and starts_with(http.request.uri.path, "/wp-json/") and http.request.headers["x-mcorch-publish"][0] eq "<o-hex-do-step-1>")
  ```
- **Action:** `Skip` → marcar (o **Nível de segurança** é o que mais escapa — ver nota abaixo):
  - ✅ All managed rules (Todas as regras gerenciadas)
  - ✅ Super Bot Fight Mode (Todas as regras do modo Super Bot Fight)
  - ✅ **Nível de segurança (Security Level)** — **IMPRESCINDÍVEL quando a edge function egressa de um IP de _datacenter_** (Oracle/AWS/GCP). O CF emite **Managed Challenge por reputação de IP** via *Security Level*, que **não** é coberto por "managed rules" nem por "Super Bot Fight". Sem marcar esta, o `curl` com header continua **403 mesmo com a regra de Skip disparando** (o Events mostra dois eventos no mesmo request: a nossa regra com ação `Ignorar` **e** o `Nível de segurança` com `Desafio gerenciado`).
  - ❌ **NÃO** marque "Verificação da integridade do navegador" (Browser Integrity Check) — o challenge é **cego ao User-Agent** (provado: UA de Chrome → ainda 403), logo BIC não é a fonte; marcá-la só amplia o skip à toa.
- **Place at:** topo da ordem de execução (First).

> 📌 **Achado material 2026-06-22 (verificado):** a fonte real do challenge era o **Nível de segurança** emitindo `Desafio gerenciado` ao IP `137.131.243.179` (AS31898 **Oracle Corporation**) — o IP de datacenter onde a edge/QA roda. `All managed rules` + `Super Bot Fight` sozinhos **não** resolviam; só ao adicionar **Nível de segurança** ao Skip é que o `curl` com header saiu do 403 (→ 200 + JSON real do WP) e o `publish-wordpress` E2E retornou `{"success":true,"post_id":18}`. Defense-in-depth preservado: sem o header, segue 403.
- Save + Deploy.

> ⚠️ **Caveat de plano:** em planos onde o **Bot Fight Mode global** não é "skippável" por regra, ele pode reintroduzir o challenge mesmo com o Skip de WAF. Se o Step 4 ainda der 403, revisar **Security → Bots** e desligar/ajustar o Bot Fight Mode global para esse path, ou subir de plano.

### Step 4 — Validação material end-to-end
**4a — Header correto passa, sem header não passa (zero-cost, via curl):**
```bash
# COM o header → deve ser 200 (ou 401 do WP por auth, mas NUNCA 403 do CF)
curl -sS -o /dev/null -w "%{http_code}\n" \
  -H "X-MCORCH-Publish: <o-hex-do-step-1>" \
  https://www.mcorch.com/wp-json/wp/v2/types
# Esperado: 200 (e SEM header `cf-mitigated: challenge`)

# SEM o header → o mundo continua barrado (challenge intacto)
curl -sS -o /dev/null -w "%{http_code}\n" https://www.mcorch.com/wp-json/wp/v2/types
# Esperado: 403 (cf-mitigated: challenge)
```
**4b — Confirmar ausência do challenge no header:**
```bash
curl -sS -D - -o /dev/null -H "X-MCORCH-Publish: <o-hex-do-step-1>" \
  https://www.mcorch.com/wp-json/ | grep -i "cf-mitigated"
# Esperado: NENHUMA linha (challenge removido para o caminho gated)
```

**Success signal (flow completo):** um run de `orchestrate-content` (ou do Viral Autopilot) com publish WordPress habilitado retorna `{ success: true, post_url, post_id }` em vez do 502 `no_post_returned` — e o post aparece como rascunho no WP admin.

## Recovery path (falha no step N)

- **Step 4a dá 403 mesmo COM o header:** **diagnóstico definitivo primeiro** → Cloudflare → **Security → Events**, clica num request 403 pra `/wp-json/`, lê o campo **"Service" / "Ação realizada"**. Ele **nomeia o culpado exato**:
  - `Regras personalizadas` + `Ignorar` apontando pra nossa regra ⇒ a regra **casou e disparou** (header/expressão/hex OK); o 403 vem de **outro** componente não-skippado — olhe o(s) outro(s) evento(s) do mesmo request.
  - `Nível de segurança` + `Desafio gerenciado` ⇒ **marque "Nível de segurança"** no Skip (causa #1 para IPs de datacenter — ver Step 3).
  - `Bot Fight Mode` (sem "Super") ⇒ tier **não-skippável**; ajuste em Security → Bots (ou suba pra Super Bot Fight).
  - Nenhum evento da nossa regra (0 matches) ⇒ aí sim o Skip não casou: conferir (i) header em **lowercase** na expressão (CF normaliza), (ii) valor byte-a-byte com `WP_PUBLISH_SECRET`, (iii) regra no topo (First), (iv) regra **Deployed** (não rascunho).
- **Step 4a dá 200 SEM o header:** a regra está aberta demais (não exige o header) — `/wp-json` ficou exposto. **Corrigir imediatamente** adicionando a cláusula do header à expressão; é uma regressão de segurança.
- **Step 4 com header correto mas publish ainda 502:** não é mais o CF — investigar Basic Auth do WP (`wp_app_password` válido?) ou a resposta do WP REST (a função já distingue 403-CF de array-por-redirect; ler `wp_http_status` no corpo do 502).
- **Rollback total:** remover a CF rule + `npx supabase secrets unset WP_PUBLISH_SECRET WP_PUBLISH_SECRET_HOST`. A função volta ao comportamento fail-closed (sem header) — sem regressão, só sem publish (estado pré-fix).

## Referências
- Edge function: `supabase/functions/publish-wordpress/index.ts` (gate de host, deployado 2026-06-22 script 106.3kB)
- FMEA security FM-04/FM-08 (credencial/identidade), `docs/bok/security/04-fmea-security.md`
- Memória relacionada: flywheel de conteúdo (`project_orchestrate_pipeline_repair`) — o #3 wp_site_url não-www já estava resolvido; o CF challenge é o blocker remanescente.

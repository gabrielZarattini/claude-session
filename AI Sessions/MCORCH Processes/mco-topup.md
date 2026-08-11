# SOP — Recarga avulsa de mcoCoins (top-up) · Lei 2 (Processo Antecipado)

**Status:** ACTIVE · v1 · 2026-08-11
**Escopo:** o processo **humano** de vender mcoCoins avulsos e creditá-los na conta certa, pelo valor certo, **uma vez só**. É a pré-condição da Lei 2 para o código da recarga.
**SSOT de design (suíte `monetization`, IDs `MR/BR/PR/FR/NFR/OTD/FM-MON-`):** `docs/bok/monetization/05-sdd.md` — **AINDA NÃO EXISTE** (`ls docs/bok/` de 2026-08-11 não lista `monetization/`). Enquanto não existir, **este SOP é o documento vinculante**; o código não arranca sem a suíte BoK 5/5 + Pattern Conformance (CLAUDE.md §1, Steps 1-3.5).
**Nome canônico do arquivo:** `docs/processes/mco-topup.md`. O rascunho da SDD cita `mcoin-topup.md` — ao selar a suíte, corrigir a referência para este path (não criar o segundo arquivo).

## ORO triplet

- **Operator (hoje, manual):** Sovereign (Gabriel), pelo painel `/dashboard/admin` + painel do Stripe.
- **Operator (quando automatizado):** MCORCH Master Execution Agent (edge functions `create-checkout` + `stripe-webhook`).
- **Reviewer:** Sovereign.
- **Owner:** Sovereign — dinheiro real de terceiros. Blast radius = confiança das duas primeiras usuárias pagantes (não-técnicas), que não têm repertório para diagnosticar um saldo errado.

## Lei 1 — o que este SOP aceita como prova

Nenhum passo abaixo se declara concluído por "deu certo". Cada um tem um **artefato**: um número lido do banco, um `HTTP status`, um id `cs_…`/`evt_…` copiado do painel do Stripe, ou uma linha de `mcoin_transactions`. O sinal de sucesso do fluxo inteiro é o **saldo no banco** — **nunca** o `200` do webhook (§7, FM-MON-001).

---

## Contexto — por que a recarga precisa de um SOP antes de código

O caminho de dinheiro atual **não sabe** receber uma compra avulsa, e os quatro fatos abaixo foram lidos no código em 2026-08-11:

| # | Fato | Prova (file:line) |
|---|------|-------------------|
| 1 | Não existe compra avulsa: o checkout é `mode: "subscription"` fixo, com `subscription_data.trial_period_days: 14` | `supabase/functions/create-checkout/index.ts:57` e `:60-62` |
| 2 | O webhook só age se a sessão tiver assinatura — `if (session.subscription)`. Uma sessão `mode:'payment'` cai no vazio e a função responde **200** | `supabase/functions/stripe-webhook/index.ts:115-122` e `:129-132` |
| 3 | O crédito de plano **SETA** o saldo (`.update({ mco_balance: mcoCoins })`), não soma — e não escreve linha de ledger | `supabase/functions/stripe-webhook/index.ts:76` |
| 4 | Verificação de assinatura é **condicional**: sem header, o corpo vira evento confiável, num endpoint `verify_jwt = false` | `stripe-webhook/index.ts:95-105` (`else { event = JSON.parse(body) }` na `:103`) + `supabase/config.toml:104-105` |

E as duas RPCs de crédito existentes **não servem** para recarga:

- `add_mco_coins` — corpo lido em `supabase/migrations/20260505100000_add_pref_ai_model_and_rpc.sql:11-40`: guarda `p_amount <= 0`, `UPDATE public.profiles SET mco_balance = mco_balance + p_amount`, `RAISE 'User profile not found'`, `RETURN`. **Nenhum `INSERT`** — credita sem deixar rastro.
- `award_mco_coins` — escreve a linha (`20260508100000_mcoin_transactions.sql:47-48`), mas recusa qualquer valor acima de 1000: `IF p_amount > 1000 THEN RAISE EXCEPTION 'Single award cannot exceed 1000 mcoCoins'` (`:40-42`). Menor que o próprio plano Pro (2000).

E `mcoin_transactions` **não tem chave de idempotência**: a única `PRIMARY KEY` é `id UUID DEFAULT gen_random_uuid()` (`20260508100000_mcoin_transactions.sql:6`), que por construção nunca conflita. Creditar por webhook sobre isto, sem âncora externa, é **cunhar dinheiro a cada reentrega** — e o Stripe reentrega por design.

---

## Operator — quem executa hoje, e como erra

Hoje **não há venda de recarga**. O crédito acontece à mão, pelo Sovereign, por quatro caminhos — todos verificados:

| Caminho | Onde | O que faz | Prova |
|---------|------|-----------|-------|
| **A** | `/dashboard/admin` → card "mcoCoins — Saldo Soberano" | Só a conta do próprio admin. Calcula `balance + delta` no cliente e envia o **absoluto** | `src/App.tsx:151` (rota) · `src/components/admin/SovereignBalancePanel.tsx:26` |
| **B** | `/dashboard/admin` → lista de usuários → menu → "Ajustar saldo mcoCoins" | Campo rotulado **"Novo saldo"** — valor **ABSOLUTO**, digitado à mão | `src/components/admin/UserActionsMenu.tsx:182-183` (título/descrição), `:186` (label "Novo saldo") e `:207` (`new_balance: n` cru) |
| **C** | Edge fn `admin-manage-user`, action `adjust_balance` | Gate `has_role('admin')` (`:41-46`) → lê saldo (`:90-91`) → **SETA** `mco_balance` (`:96-97`) → tenta inserir `action:'admin_adjustment'` com o delta | `supabase/functions/admin-manage-user/index.ts:85-111` |
| **D** | SQL editor / `PATCH /rest/v1/profiles` com a service key | Escreve o saldo cru. **Zero** linha de ledger | padrão em uso pelos smokes: `scripts/qa/smoke-vision-analyze-video.ts:53` |

### Os cinco modos de erro deste processo manual

1. **O campo é o saldo FINAL, não o valor a somar.** Creditar 150 mco para quem tem 1.351 exige digitar **1.501**. Digitar `150` **destrói 1.201 mco** — e a plataforma não reclama: grava a linha `admin_adjustment` com `amount = -1201`, o número certo do efeito errado (`admin-manage-user/index.ts:94-95`).
2. **A trilha é best-effort.** Se o `INSERT` no ledger falhar, o erro vai só para o console e o saldo já mudou: `if (ledgerErr) console.error(...)` (`admin-manage-user/index.ts:107`). Saldo sem trilha = drift novo.
3. **Nada amarra o crédito ao pagamento.** Não existe campo para `session_id`/`payment_intent`: o vínculo recibo↔crédito vive fora do sistema (mensagem, planilha, memória). Sem ele, **não há como provar** que uma segunda solicitação não é a mesma compra.
4. **O caminho D não passa por nada** — nem gate de admin, nem ledger.
5. **Não há trava contra a segunda vez.** Se a usuária reenviar o comprovante ou o Sovereign repetir a operação, credita de novo. **A idempotência hoje é a memória do operador.**

> Isto é exatamente o que o código vai automatizar — e é por isso que a âncora de idempotência **não é opcional**: um humano atento erra pouco; um webhook que reentrega erra sempre.

---

## Sequence — o fluxo manual completo (o que o código vai substituir)

| # | Passo | Critério de sucesso **material** |
|---|-------|----------------------------------|
| 1 | **Registrar o pedido.** A usuária pede recarga (WhatsApp/Telegram). Anotar: e-mail da conta, pacote escolhido (mco + preço) e data | Uma linha de controle com `email · pacote · mco · R$ · data`. Sem isto não há como fechar a conta depois |
| 2 | **Conferir o ambiente do Stripe.** Painel Stripe → confirmar se está em **Test** ou **Live** e que a chave do vault é do MESMO modo | Prefixo da chave conferido no painel. **Bloqueante** — OTD-MON-001: `grep -oE '^[A-Z_]+=' .env` (2026-08-11) não retorna nenhuma variável `STRIPE_*`; os segredos vivem só no vault, que expõe apenas o digest |
| 3 | **Criar o cobrador avulso.** Painel Stripe → Payment Links (ou Invoice) com `mode: payment`, valor em **BRL**, do pacote acordado. **Não** usar o checkout do produto: ele é assinatura fixa (`create-checkout/index.ts:57`) | Link aberto no painel com valor e moeda corretos; URL copiada |
| 4 | **Enviar o link** e aguardar | Confirmação de recebimento pela usuária |
| 5 | **Confirmar o pagamento na FONTE.** Painel Stripe → Payments → status `succeeded`. Copiar `checkout session id` (`cs_…`), `payment_intent` (`pi_…`), `amount_total` e o `Customer` | Print/anotação com os quatro valores. **Nunca creditar por captura de tela enviada pela usuária** |
| 6 | **Resolver o UUID do dono.** Do e-mail do Customer → UUID em `auth.users`/`profiles`. Conferir letra por letra | UUID copiado **e** confirmado contra o e-mail. Ver G3 |
| 7 | **Ler o saldo ANTES** e anotar: `curl -s "$SUPABASE_URL/rest/v1/profiles?id=eq.<uid>&select=mco_balance" -H "apikey: $SB_SECRET_KEY" -H "Authorization: Bearer $SB_SECRET_KEY"` | Número anotado como `saldo_antes` (padrão de consulta em uso: `scripts/qa/smoke-vision-analyze-video.ts:49`) |
| 8 | **Verificar que esta compra ainda não foi creditada** — procurar o `cs_…` no controle e no `context` das últimas linhas de `mcoin_transactions` do usuário | Zero ocorrência do `session_id`. **Se aparecer, PARAR**: já foi creditada |
| 9 | **Creditar.** `/dashboard/admin` → usuário → "Ajustar saldo mcoCoins" → digitar **`saldo_antes + mco_do_pacote`** (o absoluto), nunca só o mco do pacote | Toast "Saldo atualizado." **e** o passo 10 confirmando |
| 10 | **Ler o saldo DEPOIS** e calcular a diferença | `saldo_depois − saldo_antes == mco_do_pacote`, **exato e inteiro**. Ver G1 |
| 11 | **Conferir a trilha:** `curl -s "$SUPABASE_URL/rest/v1/mcoin_transactions?user_id=eq.<uid>&order=created_at.desc&limit=3&select=action,amount,context,created_at" -H "apikey: $SB_SECRET_KEY" -H "Authorization: Bearer $SB_SECRET_KEY"` | Existe linha `action='admin_adjustment'` com `amount = mco_do_pacote`. Se **não** existir (fail-soft do `:107`), inserir manualmente antes de seguir |
| 12 | **Amarrar o recibo ao crédito.** Registrar `cs_… · pi_… · uid · mco · amount_total · data` no controle | O par pagamento↔crédito existe fora da cabeça do operador. **É o substituto humano da tabela `mco_topups`** |
| 13 | **Fechar com a usuária.** Pedir que ela recarregue a página e confirme o saldo no header | A usuária lê o número novo (HUD: `src/components/dashboard/DashboardLayout.tsx:155`; leitura + alerta de saldo baixo em `:75-82`) |

> **Nota de expectativa (FM-MON-017):** a home mostra um KPI **"Créditos de IA"** que vem de outra tabela (`credits`) e **não** muda com esta operação — `src/pages/DashboardHome.tsx:409` lê `credits?.balance`, enquanto o header lê `profiles.mco_balance` (`useDashboardData.ts:30` × `:38`). Avisar a usuária de que o número que vale é o do **topo**, até a aposentadoria de `credits` (FR-MON-017).

---

## Verification gates

### Gates de dinheiro (os quatro que a diretiva exige)

| Gate | Pergunta | Como confirmar | Veredito |
|------|----------|----------------|----------|
| **G1 — valor exato** | O saldo subiu exatamente o combinado? | Passo 7 e 10: `saldo_depois − saldo_antes` | `== mco_do_pacote`, inteiro. Qualquer outra coisa = **falha**, inclusive "subiu mais" |
| **G2 — não credita duas vezes** | Uma reentrega/repetição da MESMA compra move o saldo? | Manual: passo 8 (procurar o `cs_…`). Automatizado: reenviar o mesmo `evt_…` e reler saldo + `count(*)` | Saldo **idêntico** e **zero** linha nova. §"O teste que prova que não cunhamos dinheiro" |
| **G3 — usuário certo** | O crédito caiu no dono do pagamento? | Passo 6: e-mail do Customer no Stripe × e-mail do UUID creditado, conferidos na fonte | Igualdade exata. **Proibido** resolver por varredura de lista — o caminho atual `listUsers().find(u => u.email === email)` com saída silenciosa `if (!user) return;` (`stripe-webhook/index.ts:28-30`) não pagina e descarta o pagamento sem erro |
| **G4 — bate com o Stripe** | O que foi cobrado é o que foi creditado? | `amount_total` do passo 5 × preço do pacote do passo 1; e mco creditado × mco do pacote | Os dois pares batem. **Nunca** derivar mco de reais no ato do crédito: o pacote define o mco, o preço só confirma |

### Gates de integridade

| Gate | Comando | Veredito |
|------|---------|----------|
| **G5 — o ledger não piora** | `drift = mco_balance − COALESCE(SUM(mcoin_transactions.amount), 0)` para o usuário, antes e depois | O drift **não aumenta**. O invariante-alvo é `0` (SOP irmão: [`mcoins-ledger-reconciliation.md`](./mcoins-ledger-reconciliation.md)) |
| **G6 — trilha existe** | Passo 11 | Linha presente com o valor certo. Saldo sem linha = drift fabricado nesta operação |
| **G7 — telemetria** (só na versão automatizada) | `curl "$SUPABASE_URL/rest/v1/infra_health_logs?service=eq.stripe-webhook&order=last_seen_at.desc&limit=5..."` | Um evento por caminho: `topup_credited` · `topup_duplicate` · `topup_orphan` · `topup_price_mismatch` · `signature_missing` (colunas `event`/`metadata` existem desde `supabase/migrations/20260615170000_infra_health_logs_metadata.sql`) |
| **G8 — assinatura fail-closed** (automatizado) | `curl -X POST "$SUPABASE_URL/functions/v1/stripe-webhook" -d '{"id":"evt_probe"}'` **sem** header `stripe-signature` | Deve ser `HTTP 400`/`501`. **Hoje devolve 200 e processa o corpo** (`stripe-webhook/index.ts:102-104`) — este gate é RED até FR-MON-005 |

---

## Recovery path

Cada linha traz o **diagnóstico exato** e o **conserto**. Nenhuma diz "tente de novo".

### 1. O pagamento aconteceu e o crédito não

- **Diagnóstico:** painel Stripe → Payments → o `pi_…` está `succeeded`? → então o dinheiro entrou. Depois: `curl ".../rest/v1/mcoin_transactions?user_id=eq.<uid>&order=created_at.desc&limit=10&select=action,amount,context,created_at"` e procurar o `cs_…` no `context`.
- **Causa provável (automatizado):** a sessão era `mode:'payment'` e o handler só age em `if (session.subscription)` — resposta 200, entrega marcada como bem-sucedida no Stripe e **nenhuma reentrega** (`stripe-webhook/index.ts:115-122`). É a falha que **não gera erro nenhum**.
- **Conserto:** creditar pelos passos 6→12, registrando `cs_…` no controle. Depois abrir/atualizar o item de correção (FR-MON-006/007).
- **Nunca:** creditar "por garantia" sem antes rodar o passo 8.

### 2. Creditou duas vezes

- **Diagnóstico:** duas linhas com o mesmo `session_id` no `context`, ou uma diferença de saldo igual a `2 × mco_do_pacote`.
- **Conserto:** **debitar de volta o excedente**, até o limite do saldo disponível — nunca deixar saldo negativo. Pelo painel: novo saldo = `saldo_atual − mco_excedente` (se `saldo_atual < mco_excedente`, zerar e **registrar a diferença** como não recuperada; ver §5).
- **Registrar:** a linha de acerto precisa dizer no `context` qual `session_id` originou a duplicata. Sem isso, a próxima auditoria lê o débito como cobrança.
- **Prevenção:** é exatamente o que a âncora `session_id` `PRIMARY KEY` + `ON CONFLICT DO NOTHING` faz sozinha (molde da casa: `supabase/migrations/20260624140000_autopilot_video_enqueue_refund.sql:73-83`).

### 3. Creditou o usuário errado

- **Diagnóstico:** conferir o e-mail do Customer no Stripe contra o e-mail do UUID que recebeu. Se divergirem, o crédito está na conta errada.
- **Conserto, nesta ordem:** (a) **primeiro** creditar quem pagou (o cliente não pode ficar esperando); (b) depois estornar de quem recebeu por engano, até o saldo disponível; (c) se o errado já gastou, a diferença é **perda** — registrar, não esconder.
- **Causa-raiz a eliminar:** resolução por e-mail. O e-mail é mutável no Stripe e sensível a caixa; a identidade tem de ser o **UUID gravado na própria sessão** (`client_reference_id` + `metadata.supabase_user_id`) — FR-MON-003/011.

### 4. Digitou o valor absoluto errado (o erro mais provável do processo manual)

- **Sintoma:** saldo despencou depois de um crédito.
- **Diagnóstico:** `mcoin_transactions` última linha `admin_adjustment` com `amount` **negativo** e `context.prev_balance` mostrando o valor destruído (`admin-manage-user/index.ts:105`).
- **Conserto:** novo ajuste para `prev_balance + mco_do_pacote` — o `context` da linha errada guarda o `prev_balance` correto, então **a informação para consertar existe**. Conferir por G1 depois.

### 5. Chargeback / estorno

- **Diagnóstico:** painel Stripe → Payments → status `refunded` ou `disputed`; anotar `pi_…`.
- **Conserto:** debitar de volta `min(mco_da_compra, saldo_atual)`. **Nunca negativar o saldo.**
- **A parte irrecuperável, sem eufemismo:** o mco já gasto virou trabalho consumido — chamada de provedor, CPU do host, storage, vídeo publicado. Não existe des-gerar. O débito reverso recupera **saldo**, não **custo**. A diferença tem de ser **registrada** (campo `unrecovered_mco` na versão automatizada; anotação no controle na versão manual), jamais arredondada para zero.
- **Congelar a conta é decisão do Sovereign, manual.** Disputa legítima (cobrança duplicada do banco, por exemplo) existe, e com duas usuárias reais e conhecidas o falso positivo custa mais que a fraude.

### 6. Usuário deletado depois de pagar

- **Diagnóstico:** `curl ".../rest/v1/profiles?id=eq.<uid>&select=id"` retorna `[]`.
- **O que se perde:** `mcoin_transactions.user_id` é `REFERENCES auth.users(id) ON DELETE CASCADE` (`20260508100000_mcoin_transactions.sql:7`) — apagar o usuário **apaga junto a trilha de um pagamento real**. E `soft_reset_account` executa `DELETE FROM mcoin_transactions WHERE user_id = p_user_id` (`supabase/migrations/20260527005036_soft_reset_account_rpc_v2.sql:52`), com o mesmo efeito sem apagar a conta.
- **Conserto:** a verdade fiscal sobrevive **no Stripe** (`cs_…`/`pi_…`/Customer). Reconciliar por lá, e — se a conta voltar — recreditar pelos passos 6→12 citando o `session_id` original.
- **Consequência de design:** por isso o marcador de compra deve usar `ON DELETE SET NULL` e guardar `stripe_customer_id`, e não desaparecer com a conta (FR-MON-025).

### 7. O saldo mudou e a linha de ledger não

- **Diagnóstico:** G6 falhou (passo 11 sem a linha) → `drift` do usuário aumentou pelo valor creditado.
- **Conserto:** inserir a linha faltante com `action='admin_adjustment'` e `context` contendo `session_id`, `prev_balance` e `new_balance`, na **mesma sessão** em que se detectou. Nunca deixar para depois: sem a linha, a operação some do histórico e o drift vira permanente.

### 8. O webhook nunca chegou (versão automatizada)

- **Diagnóstico:** painel Stripe → Developers → Events → localizar o `evt_…` e ler o status da entrega (2xx/4xx/5xx/sem tentativa).
- **Leitura:** `200` com saldo inalterado = a função **engoliu** o evento (caso 1). `5xx` = a Stripe vai reentregar sozinha e a idempotência protege. **Sem tentativa** = endpoint não cadastrado ou tipo de evento não inscrito (OTD-MON-002).
- **Conserto:** reenviar o evento pelo painel **depois** de confirmar que a idempotência está ativa. Antes disso, creditar à mão pelos passos 6→12.

---

## Success signal

O fluxo inteiro funcionou quando, **simultaneamente**:

1. `saldo_depois − saldo_antes == mco_do_pacote`, exato e inteiro (G1);
2. existe **uma** — e só uma — linha em `mcoin_transactions` para aquela compra, com o `session_id` no `context` (G2, G6);
3. o UUID creditado é o do e-mail do Customer que pagou (G3);
4. `amount_total` do Stripe bate com o preço do pacote (G4);
5. o `drift` do usuário não aumentou (G5);
6. a usuária **lê o número novo** no header, sem precisar de explicação.

> **O sinal é o saldo no banco.** Um `HTTP 200` do webhook não é sinal de nada — o handler atual devolve 200 inclusive quando não faz absolutamente nada (`stripe-webhook/index.ts:129-132`).

---

## O teste que prova que não cunhamos dinheiro

Objetivo: em ambiente de **teste**, disparar a **mesma** `checkout.session.completed` **duas vezes** e provar que o saldo subiu **uma vez só**.

### Pré-condições (bloqueantes)

1. Stripe em modo **Test**, e a `STRIPE_SECRET_KEY` do vault sendo a de test (OTD-MON-001).
2. Endpoint de webhook cadastrado no painel apontando para `${SUPABASE_URL}/functions/v1/stripe-webhook`, com `checkout.session.completed` inscrito, e o `whsec_…` **daquele endpoint** no vault como `STRIPE_WEBHOOK_SECRET` (OTD-MON-002).
3. Um usuário de teste descartável com UUID conhecido.
4. **`stripe` CLI não está instalado neste host** — `which stripe` (2026-08-11) → `command not found`. Use o Caminho A só depois de instalar; o Caminho B roda hoje, sem instalar nada.

### Passo 0 — a fotografia inicial (sem ela, nada é prova)

```bash
UID=<uuid-do-usuario-de-teste>
H=(-H "apikey: $SB_SECRET_KEY" -H "Authorization: Bearer $SB_SECRET_KEY")

# saldo antes
curl -s "${H[@]}" "$SUPABASE_URL/rest/v1/profiles?id=eq.$UID&select=mco_balance"
# contagem de linhas do ledger antes  (Prefer: count=exact devolve o total no header Content-Range)
curl -sI "${H[@]}" -H "Prefer: count=exact" \
  "$SUPABASE_URL/rest/v1/mcoin_transactions?user_id=eq.$UID&select=id&limit=1" | grep -i content-range
```

Anotar `saldo_antes` e `linhas_antes`. **Os dois** — o teste falha tanto por saldo dobrado quanto por linha duplicada com saldo certo.

### Passo 1 — a compra real (1ª entrega)

Pagar o Payment Link de teste com o cartão de teste `4242 4242 4242 4242` (qualquer data futura / CVC). Copiar do painel: `cs_test_…`, `evt_…`, `amount_total`.

Reler saldo e contagem. **Esperado:** `saldo = saldo_antes + mco_do_pacote`; `linhas = linhas_antes + 1`.

### Passo 2 — a segunda entrega do MESMO evento

**Caminho A — painel (a reentrega mais fiel):** Stripe Dashboard → Developers → Events → abrir o `evt_…` do passo 1 → reenviar (*Resend*) para o endpoint. É literalmente o que a Stripe faz sozinha quando não recebe 2xx. *(Se o botão não existir na sua conta/versão do painel, use o Caminho B — este ponto é NÃO VERIFICADO aqui.)*

**Caminho A' — CLI, se instalado:**
```bash
stripe listen --forward-to "$SUPABASE_URL/functions/v1/stripe-webhook"
stripe events resend evt_...
```

**Caminho B — replay assinado, sem CLI e sem painel (roda hoje):** capturar o corpo cru do evento (Dashboard → Events → o `evt_…` → payload JSON), salvar em `/tmp/evt.json`, e reassinar com o `whsec_…` do endpoint. A `constructEvent` valida `t=<unix>,v1=<hmac_sha256("<t>.<payload>", whsec)>` dentro de uma janela de tolerância, então o timestamp tem de ser **agora**:

```bash
cat > /tmp/replay.ts <<'TS'
const secret = Deno.env.get("WHSEC")!;            // whsec_... do endpoint de TEST
const url    = Deno.env.get("HOOK_URL")!;         // $SUPABASE_URL/functions/v1/stripe-webhook
const body   = await Deno.readTextFile("/tmp/evt.json");
const t      = Math.floor(Date.now() / 1000);
const key    = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret),
                 { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
const mac    = await crypto.subtle.sign("HMAC", key, new TextEncoder().encode(`${t}.${body}`));
const v1     = [...new Uint8Array(mac)].map((b) => b.toString(16).padStart(2, "0")).join("");
const post   = () => fetch(url, { method: "POST",
                 headers: { "Content-Type": "application/json", "stripe-signature": `t=${t},v1=${v1}` },
                 body }).then((r) => r.status);
// as DUAS entregas em PARALELO — é o caso que a PRIMARY KEY precisa vencer
console.log(await Promise.all([post(), post()]));
TS
WHSEC=whsec_... HOOK_URL="$SUPABASE_URL/functions/v1/stripe-webhook" bun /tmp/replay.ts
```

> **Por que em paralelo:** duas entregas sequenciais também são checadas por um `SELECT … IF NOT EXISTS` mal escrito. Só o par **simultâneo** distingue a âncora real (`INSERT … ON CONFLICT (session_id) DO NOTHING` + `GET DIAGNOSTICS ROW_COUNT`, molde `20260624140000:73-83`) de uma verificação que perde a corrida. Este passo é o coração do teste.

### Passo 3 — o veredito

Reler saldo e contagem com os mesmos comandos do passo 0:

| Medida | Valor exigido | Se divergir |
|--------|---------------|-------------|
| `mco_balance` | **`saldo_antes + mco_do_pacote`** — idêntico ao do passo 1 | Cunhamos dinheiro. **Bloquear a venda.** |
| linhas em `mcoin_transactions` | **`linhas_antes + 1`** | Trilha duplicada: a auditoria vai contar a compra duas vezes |
| linhas em `mco_topups` (versão automatizada) | **1**, com `status='credited'` | A âncora não segurou |
| resposta HTTP das duas entregas | `200` nas duas — a 2ª deve ser um **no-op idempotente**, não um erro | Um `5xx` na 2ª faz a Stripe reentregar em laço |

**Aritmética que fecha o teste:** `saldo_final − saldo_antes == mco_do_pacote` **e** `linhas_final − linhas_antes == 1`, com **três** entregas totais (1 real + 2 paralelas) do mesmo evento.

### Limpeza

Zerar o usuário de teste e registrar o resultado. Se este teste não estiver **verde**, a recarga **não vai a produção** — é o gate G2 da §Verification, e ele é bloqueante.

---

## Anti-patterns proibidos

- ❌ Creditar por captura de tela / comprovante enviado pela usuária. A fonte é o painel do Stripe.
- ❌ Digitar o valor do pacote no campo "Novo saldo" (ele é o saldo **final**).
- ❌ Creditar sem antes procurar o `session_id` (passo 8) — é a única defesa manual contra pagar duas vezes.
- ❌ Derivar a quantidade de mco a partir do valor em reais no momento do crédito. O pacote define o mco; o valor só **confirma**.
- ❌ Usar `PATCH /rest/v1/profiles` direto para creditar cliente pagante (caminho D): sem gate, sem trilha, sem recibo.
- ❌ Tratar `HTTP 200` do webhook como prova de crédito.
- ❌ Responder `5xx` a um pagamento órfão: vira laço infinito de reentrega de um problema que reentrega não conserta.
- ❌ Creditar via `add_mco_coins` sem `INSERT` no ledger na **mesma transação** — é o furo que gera drift silencioso.

---

## Referências

- **SOP irmão (invariante do ledger):** [`mcoins-ledger-reconciliation.md`](./mcoins-ledger-reconciliation.md) — ⚠️ **stale em dois pontos**: o §Contexto não menciona `add_mco_coins` (que credita sem trilha) e o passo 7 prescreve `scripts/mcoins-reconcile.ts`, que **não existe** (`ls` de 2026-08-11 → *No such file or directory*). Emendar ao entregar FR-MON-026.
- **SOP de preço:** [`mcoin-cost-calibration.md`](./mcoin-cost-calibration.md) — modelo 4×-floor; a recalibração BYOK entra como emenda, não como duplicata.
- **Precedente de webhook de dinheiro fail-closed:** [`ml-postback-signature-validation.md`](./ml-postback-signature-validation.md) + `supabase/functions/handle-ml-postback/index.ts:100-110` (`501` estruturado + pulse `degraded` quando o segredo falta).
- **Molde de idempotência da casa:** `supabase/migrations/20260624140000_autopilot_video_enqueue_refund.sql` (PK como âncora `:22`, RESTRICTIVE no-delete `:36-37`, `ON CONFLICT DO NOTHING` + `ROW_COUNT` `:73-76`, `REVOKE … GRANT service_role` `:87-88`).
- **Ledger canônico:** `supabase/migrations/20260508100000_mcoin_transactions.sql` · `20260505100000_add_pref_ai_model_and_rpc.sql` (`add_mco_coins`).
- **Superfícies tocadas:** `supabase/functions/create-checkout/index.ts` · `supabase/functions/stripe-webhook/index.ts` · `supabase/functions/admin-manage-user/index.ts` · `src/pages/BillingPage.tsx` (âncora de preço: R$147/500 `:26,:30`; R$397/2000 `:43,:47`; R$997/10000 `:62,:66`) · `src/components/dashboard/DashboardLayout.tsx:155`.
- **Governança:** este SOP é pré-condição da Lei 2 para o código da recarga; o gate Closed-Loop (CLAUDE.md §1) continua exigindo `docs/bok/monetization/` 5/5 + Pattern Conformance antes da primeira linha.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

# SOP — CRM Inbox media ingest (WhatsApp inbound rich media)

> **Lei 2 (Processo Antecipado).** Este SOP descreve o fluxo humano equivalente ANTES de qualquer
> código de automação. O worker `crm-media-bridge` é a automação deste processo.
> BoK SSOT: `docs/bok/crm-inbox/10-amendment-rich-media-omnichannel.md` (§5 data model, FR-CRM rich media).
> Fatia A = **ingest** (pull dos bytes de mídia inbound). A marcação/erasure LGPD é fatia posterior.

## Contexto / porquê

O webhook `whatsapp-webhook` recebe a notificação inbound da Meta Cloud API. Uma mensagem de mídia
(imagem/áudio/vídeo/documento/figurinha) **NÃO carrega os bytes** — carrega apenas um ponteiro:
`message.<tipo>.id` (media id), `mime_type` e `sha256`. Para exibir a mídia na Caixa de Entrada é
preciso um **download em 2 passos** contra a Graph API, autenticado com o token per-tenant. Esse
download:

- É **latente** (2 round-trips HTTP + upload no Storage) — não pode acontecer no caminho síncrono do
  webhook (a Meta desativa webhooks lentos / que dão timeout).
- Envia `Authorization: Bearer <token Meta>` — classe **SSRF** se a URL de download for seguida
  cegamente através de redirects (o token pode vazar cross-host; a rede interna pode ser alcançada).
- Grava um objeto num **bucket privado owner-scoped** (`crm-media`) — a chave DEVE ser derivada do
  `user_id` **confiável** da linha (nunca de payload da Meta).

Decisão de arquitetura (travada): **worker no host** (não edge function). O cap de edge functions
está batido (101 → deploy 402) e o download precisa de um runtime Bun/Node com o guard anti-SSRF
que revalida cada redirect. O webhook só **ENFILEIRA** (grava o ponteiro + `media_status='pending'`)
e responde 200 imediato; o worker faz o pull assíncrono.

## ORO triplet

- **Operator:** worker `crm-media-bridge` (systemd `--user`) — humano equivalente: um operador que,
  ao ver uma mensagem de mídia na inbox, pega o media id, chama a Graph API 2×, baixa o arquivo,
  confere que é mídia de verdade e o arquiva na pasta do próprio tenant.
- **Reviewer:** Sovereign (Gabriel) — habilita o systemd, executa o witness E2E com mídia real,
  roda `/security-review` na migration.
- **Owner:** Sovereign até multi-tenant hardening — risco = vazamento de token cross-tenant ou
  SSRF; blast radius isolado por `user_id` (owner-scoped storage + token per-user).

## Operator — quem executa manualmente hoje

Um atendente humano que, ao ver "[Imagem]" na conversa, teria que: abrir o Business Manager, achar
o media id, autenticar, baixar o arquivo, verificar que abriu (não é um erro), e salvar na pasta do
cliente. O worker automatiza exatamente isso, um job por vez.

## Sequence (numerada, cada passo com critério de sucesso material)

1. **Enqueue (webhook).** Ao inserir a mensagem inbound em `public.messages`, se `message.type` é
   mídia (`image|audio|video|document|sticker`): gravar `content_type=<tipo real>`, `body=caption||NULL`,
   `media_mime=<mime>`, `media_status='pending'`, `metadata.wa_media={id,mime,sha256}`.
   **Sucesso material:** `SELECT media_status,metadata->'wa_media'->>'id' FROM messages WHERE id=…`
   retorna `pending` + o media id. Dedup por `provider_message_id` preservado (redelivery da Meta
   não duplica).

2. **Sweep (worker).** `SELECT … FROM messages WHERE media_status='pending' ORDER BY created_at ASC
   LIMIT N` (usa o índice parcial `messages_media_pending_idx`). Um job por iteração.
   **Sucesso material:** o worker loga `processing <message_id>` para cada linha pendente.

3. **Resolver token per-tenant.** `SELECT long_lived_token FROM decrypted_meta_config WHERE
   user_id = <row.user_id>` (molde `whatsapp-templates`). Sem token → **falha da linha** (passo 8),
   NUNCA fallback global (API Tenancy Model).
   **Sucesso material:** token resolvido (nunca logado).

4. **Passo-1 Graph (metadata).** `GET https://graph.facebook.com/v21.0/{media_id}` com
   `Authorization: Bearer <token>` → `{ url, mime_type, file_size }`.
   **Sucesso material:** HTTP 200 + `url` presente. `file_size` acima do teto por família → falha.

5. **Passo-2 Graph (bytes).** `GET <url>` com `Authorization: Bearer <token>` **via o guard
   anti-SSRF** (`fetchPublicUrl`), que segue redirects à mão revalidando cada salto e **só anexa o
   Bearer em host da allowlist Meta** (`graph.facebook.com`, `*.fbsbx.com`, `lookaside.fbsbx.com`).
   **Sucesso material:** resposta binária (não `application/json`).

6. **Validar ANTES do upload.** Rejeita stub/erro:
   - `Content-Type` da resposta não pode ser `application/json`/`text/html`;
   - **magic-bytes** conferem com a família do `content_type` (imagem/áudio/vídeo/documento);
   - **mime allowlist** (o mime resolvido deve estar na lista permitida da família);
   - **teto de tamanho** por família + piso mínimo (rejeita stub, molde do piso 100KB do
     `rescue-video`).
   **Sucesso material:** `sniff(bytes)` == família esperada; tamanho dentro dos limites.

7. **Upload + flip.** Upload em `crm-media/{row.user_id}/{conversation_id}/{message_id}.{ext}` —
   `user_id` da **linha confiável**, nunca de payload. Depois
   `UPDATE messages SET media_asset_path=<key>, media_mime=<mime>, media_status='stored' WHERE id=…`.
   **Sucesso material:** `SELECT media_status,media_asset_path FROM messages WHERE id=…` → `stored`
   + a chave; objeto existe no bucket (`storage.from('crm-media').download(key)` retorna bytes).

8. **Fail-soft por linha.** Qualquer erro na linha → `UPDATE messages SET media_status='failed'` +
   `infra_health_logs (service='crm-inbox', status='degraded', event='media_ingest_failed')`.
   O índice parcial só pega `pending`, logo **`failed` não é re-tentado** (sem retry infinito) e o
   loop **não cai** (uma linha ruim não derruba as outras).
   **Sucesso material:** `SELECT media_status FROM messages WHERE id=…` → `failed`; 1 linha degraded
   em `infra_health_logs`.

## Verification gates

| Gate | Comando / observação | Critério |
|------|----------------------|----------|
| G1 SSRF | `bun run test scripts/lib/fetch-public-url.test.ts` | privado/loopback/link-local/`302→169.254.169.254` bloqueados; **Bearer nunca vaza** em redirect fora da allowlist |
| G2 Storage tenancy | `bun run scripts/qa/smoke-crm-media-ingest.ts` (gate 2) | owner assina `crm-media/{uid}/…` = 200; atacante assinando path do owner = BLOCKED |
| G3 Queue predicate | idem (gate 3, GATED na migration) | throwaway sem token → `failed` (não retry) + health degraded; não-mídia intocada |
| G4 Idempotência | idem (gate 4, GATED na migration) | `stored` nunca é re-selecionado por `fetchPending` |
| G5 /security-review | migration `20260718240000` + worker | NO FINDINGS antes do apply/enable |

## Invariantes de segurança (não-negociáveis)

1. **Bearer só em host Meta.** O `Authorization: Bearer <token>` é anexado **por salto**, só quando o
   host do salto atual está na allowlist Meta; um redirect cross-host **DROPA** o header. Nunca
   repassar headers cegamente em todos os hops.
2. **Path do `row.user_id` confiável.** A chave do bucket é montada do `user_id` da linha de
   `messages` (server-truth), nunca de campo do payload da Meta.
3. **Validar antes de armazenar.** magic-bytes + mime allowlist + teto/piso de tamanho **antes** do
   upload — rejeita stub JSON de erro da Graph.
4. **Token nunca logado.** Nenhum `console.log` inclui o token nem headers de auth.
5. **Dedup preservado.** O `messages_provider_dedup_uniq (user_id, provider_message_id)` continua a
   defesa contra redelivery da Meta.

## Recovery path

- **Passo 3 falha (sem token):** linha → `failed`. Recovery = tenant configura Meta em
  Settings → Meta; re-ingest manual = `UPDATE messages SET media_status='pending' WHERE id=…` e o
  worker repega. (Não há re-tentativa automática — evita retry infinito de linha sem token.)
- **Passo 4/5 falha (429/5xx da Graph):** linha → `failed` + degraded. Recovery = re-marcar
  `pending` (a mídia da Meta expira em ~30 dias; após isso o media id é irrecuperável — documentar
  como perda aceitável, OTD-CRM-016).
- **Passo 6 falha (stub/mismatch):** linha → `failed`. Recovery = investigar via `infra_health_logs`
  (`event='media_ingest_failed'`, metadata com o motivo); geralmente token expirado (reautenticar).
- **Worker morto/loop travado:** `systemctl --user restart crm-media-bridge.service`; o índice
  parcial garante que só o backlog `pending` é reprocessado (idempotente).

## Success signal

Uma conversa em `/dashboard/inbox` que recebeu uma imagem mostra a **imagem renderizada** (URL
assinada owner-scoped), não o placeholder "[Imagem]" nem "recebendo mídia…". Materialmente:
`SELECT media_status,media_asset_path FROM messages WHERE content_type='image' AND direction='inbound'`
→ `stored` + uma chave `crm-media/<uid>/<conv>/<msg>.jpg`; a chave assina para HTTP 200 pelo dono.

## Gates Sovereign (ações do Reviewer, não do Operator)

- [ ] `/security-review` na migration `20260718240000` + no worker `crm-media-bridge.ts` → NO FINDINGS.
- [ ] Aplicar a migration (`supabase db push` / bridge) — só depois do review.
- [ ] Regenerar `src/integrations/supabase/types.ts` (coluna `media_status` nova).
- [ ] Deploy single-fn do `whatsapp-webhook` (`npx supabase functions deploy whatsapp-webhook`).
- [ ] Habilitar o systemd: `systemctl --user enable --now crm-media-bridge.service` (molde
      `provenance-bridge.service`, que nasceu desabilitado por gate Sovereign).
- [ ] **Witness E2E:** enviar uma imagem real de um WhatsApp para o número do tenant e ver a imagem
      renderizar na inbox (Lei 1 — prova física, ação Sovereign).
- [ ] **OTD-CRM-015 (diferido):** retenção LGPD / erasure física dos objetos `crm-media/<uid>/` no
      `erase_lead()` estendido (o cascade apaga as linhas de `messages`, mas objetos de Storage não
      são FK — remoção via Storage API numa fatia seguinte).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

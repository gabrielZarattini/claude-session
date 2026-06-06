# SOP — Canvas Video Async Execution

**Versão:** v1 · **Selada:** 2026-05-17 · **Lei 2 (Processo Antecipado)** · **Phase 4.2c**

## ORO triplet

- **Operator:** end user (gera vídeo no Canvas Studio); admin (override manual em job stuck)
- **Reviewer:** Sovereign (aprova consumo de hf credits + valida saldo Higgsfield no dashboard)
- **Owner:** Sovereign (Pillar 3 cost discipline + dono dos ~30 hf credits pagos)

## Contexto

A geração de vídeo via Higgsfield (DoP / Kling / Seedance) leva 20–120s — excede o teto de 90s do polling síncrono dentro de Edge Function. Para Phase 4.2c, o `canvas-execute` dispatcha jobs de `image_to_video` num caminho **async fire-and-forget**: insere row em `vm_canvas_executions` com `status='queued'`, submete à Higgsfield com `?hf_webhook=<callback>` query param, retorna imediatamente; a Higgsfield POSTa de volta no `higgsfield-webhook` quando o vídeo termina; o webhook baixa o vídeo (≥100 KB + video/* content-type), upload pro `canvas-assets` bucket, debita mcoCoins **só após upload OK**, INSERT em `vm_canvas_assets`. `useCanvasJobsRealtime` faz a UI re-renderizar via Supabase Realtime sem refresh.

**Por que existe:** Sem este pipeline, o Canvas não consegue produzir vídeo end-to-end → bloqueia validação do flywheel Higgsfield → bloqueia revenue via afiliados ML. Phase 4.2c foi desbloqueada por OE04 (v6.6.0) que subiu Cost Discipline para 4/5 + SOP para 5/5.

**Catálogo conservador (Sovereign decidiu 2026-05-17):** apenas `dop-standard-5s` (9 hf credits ≈ $0.56) está clicável. Lite / Turbo / Kling / Seedance ficam disabled no inspector com tooltip "Aguardando validação tier — Phase 4.3" até endpoint mapping ser confirmado contra `cloud.higgsfield.ai`.

## Resposta HTTP do canvas-execute para image_to_video

```json
HTTP 200 OK
{
  "execution_id": "<uuid>",
  "status": "queued",
  "webhook_token": "<64 hex>",
  "operation_id": "<higgsfield request_id>"
}
```

Em falha de submit Higgsfield (não-2xx upstream): row vira `status='failed'`, resposta HTTP 502.

## Sequence — fluxo happy path

| # | Action | Output esperado | Verification gate |
|---|--------|-----------------|-------------------|
| 1 | User conecta upstream image (GenerateImage/SceneCompose/CharacterReference) ao nó ImageToVideo e clica Run | POST `canvas-execute` HTTP 200 com `{execution_id, status:'queued', operation_id}` | Network HAR: response body tem 3 campos não-vazios |
| 2 | Backend insere row em `vm_canvas_executions` + UPDATE com `operation_id` | Row visível via REST | `SELECT id, status, operation_id, webhook_token FROM vm_canvas_executions WHERE id=<uuid>` → status=`queued`, operation_id NOT NULL, webhook_token 64 hex |
| 3 | Higgsfield processa job (eta `30–60s` DoP Standard) | `GET /requests/<operation_id>/status` Higgsfield retorna `completed` | curl Higgsfield API → status JSON com `video.url` |
| 4 | Higgsfield POSTa em `${SUPABASE_URL}/functions/v1/higgsfield-webhook?token=<webhook_token>` | Webhook 200 OK em <2min | `webhook_received_at IS NOT NULL`, `status='success'` |
| 5 | Webhook baixa vídeo, valida (≥100 KB + video/*), upload `canvas-assets`, gera signed URL 7d | `output_url` populado, `vm_canvas_assets` row criado | `SELECT file_size_bytes, mime_type FROM vm_canvas_assets WHERE storage_key='<project>/<exec>.mp4'` → ≥100 KB, video/mp4 |
| 6 | Webhook chama `deduct_mco_coins(action='canvas_video_spend')` SOMENTE após upload OK | Linha negativa em `mcoin_transactions` | `SELECT amount, action, context FROM mcoin_transactions WHERE context->>'execution_id'=<uuid>` → amount=-125, action match |
| 7 | Supabase Realtime emite UPDATE evt no canal `canvas_jobs_<user_id>` | useCanvasJobsRealtime invalida queries + atualiza Zustand store via callback | DevTools → Network → WS → frame UPDATE com status='success'; UI swap badge queued → success sem refresh |

## Verification gates (Lei 1 — Materiality)

Comandos reproduzíveis a serem citados no `/handoff`:

```bash
# Gate 2 — row inserted
psql "$DATABASE_URL" -c "SELECT id, status, operation_id, started_at, webhook_token
                          FROM vm_canvas_executions WHERE id = '<uuid>';"

# Gate 3 — Higgsfield in-flight
curl -H "Authorization: Key $HIGGSFIELD_API_KEY:$HIGGSFIELD_API_KEY_SECRET" \
     "https://platform.higgsfield.ai/requests/<operation_id>/status"

# Gate 4-5 — webhook finalize
psql "$DATABASE_URL" -c "SELECT status, output_url, webhook_received_at, completed_at,
                                response_payload->>'request_id' AS hf_req
                          FROM vm_canvas_executions WHERE id = '<uuid>';"

# Gate 6 — atomic deduct
psql "$DATABASE_URL" -c "SELECT amount, action, context FROM mcoin_transactions
                          WHERE context->>'execution_id' = '<uuid>'
                          ORDER BY created_at DESC LIMIT 1;"
```

## Recovery path

| Falha | Detecção | Ação | Resultado |
|-------|----------|------|-----------|
| **Webhook nunca chega** (Higgsfield down, network blip, token corrupted) | `vm_canvas_executions.status IN ('queued','running') AND created_at < now() - interval '10 min'` | Cron `*/5 * * * *` em `scripts/canvas-video-watchdog.sh` faz GET no Higgsfield status_url | Se completed → invoca webhook URL manualmente (idempotente via HTTP 409). Se failed → marca status='failed'. |
| **Higgsfield retorna failed/nsfw** | Status no poll é `failed`/`nsfw`/`cancelled` | Watchdog PATCH PostgREST `status='failed'` + `error_message` | Sem deduct (nunca aconteceu). Higgsfield auto-refunda hf credits. |
| **Job stuck > 60min** | `started_at < now() - interval '60 min'` ainda em queued/running | Watchdog PATCH `status='timeout'` | Sem deduct. Sovereign decide manual refund se necessário. |
| **Webhook chega mas upload falha** | Catch block em higgsfield-webhook | UPDATE status='failed' + error_message | Sem deduct (atomic ordering protege). Higgsfield auto-refunda. |
| **Webhook idempotência (retry)** | Higgsfield reenvia mesmo callback (até 2h) | webhook query `WHERE webhook_token = ?` + check `status IN ('queued','running')` | HTTP 409 → no-op. Ledger e asset não duplicam. |
| **Operator override (job órfão)** | Sovereign decisão manual | `UPDATE vm_canvas_executions SET status='cancelled', error_message='<motivo>' WHERE id=<uuid>` | Sem deduct. Documentar em decision node se >5/mês (sinal de bug). |

### Install do watchdog cron

```bash
# Verify script executável
chmod +x scripts/canvas-video-watchdog.sh

# Dry-run (sem in-flight jobs):
bash scripts/canvas-video-watchdog.sh
# Esperado: "0 jobs to check" + insert em infra_health_logs

# Install em crontab:
crontab -l > /tmp/cron.bak
(crontab -l; echo "*/5 * * * * /home/gcrUX/htdocs/constellation-orchestra/scripts/canvas-video-watchdog.sh >> /var/log/mcorch-canvas-watchdog.log 2>&1") | crontab -

# Verify:
crontab -l | grep canvas-video-watchdog
```

## Success signal

- `canvas-execute` retorna 200 `{status:'queued'}` em <2s para image_to_video.
- `vm_canvas_executions` row com `operation_id` IS NOT NULL em <5s.
- `webhook_received_at` populado em <2min (DoP Standard) ou <3min (Kling/Seedance quando habilitados).
- `vm_canvas_assets` row com `file_size_bytes >= 100*1024` + `mime_type LIKE 'video/%'`.
- `mcoin_transactions` linha negativa com `action='canvas_video_spend'`.
- Browser: `<video>` element renderizado no `ImageToVideoNode` sem refresh manual.
- `infra_health_logs` health pulse para `service IN ('canvas-execute','higgsfield-webhook','canvas-video-watchdog')` com `status='healthy'` no happy path.

## Anti-patterns

- ❌ **Polling síncrono dentro de canvas-execute para video** — excede 90s edge function timeout, queima crédito sem entregar URL.
- ❌ **Deduzir mcoCoins antes do upload OK** — quebra invariante "atomic só-após-upload-OK"; se download falha, user paga por nada.
- ❌ **Webhook token reutilizado entre executions** — quebra defesa contra replay; migration garante `UNIQUE INDEX` em `webhook_token`.
- ❌ **Skip do health pulse em failure paths** — observabilidade quebrada; SSP-01 OE03 Pillar 4 requer best-effort pulse mesmo em erro.
- ❌ **Run-All bloqueante esperando vídeo terminar** — UX morre. Fire-and-forget: submit retorna, Realtime atualiza depois.
- ❌ **Habilitar Lite/Turbo/Kling/Seedance sem confirmar endpoint** — gasta hf credits em 404. Manter `dop-standard-5s` único até Phase 4.3.

## Referências

- `supabase/functions/canvas-execute/index.ts` (async submit branch — Step 2)
- `supabase/functions/higgsfield-webhook/index.ts` (já deployed v6.4.0 — finalização atômica)
- `supabase/migrations/20260516224542_vm_canvas_executions_async_video.sql` (already applied — colunas async)
- `src/hooks/useCanvasJobsRealtime.ts` (subscribe + onUpdate callback — Step 3)
- `src/pages/CanvasEditorPage.tsx` (wiring Realtime + isRunnable — Step 4)
- `src/components/canvas/RightPanel/inspectors/ImageToVideoInspector.tsx` (Run button enable — Step 5)
- `scripts/canvas-video-watchdog.sh` (cron defesa-em-profundidade — Step 6)
- `.claude/context/higgsfield-api-validation-2026-05-15.md` (API spec canônica + webhook idempotency)
- `.claude/proposals/vm-canvas-jobs-async-video-v1.md` (proposal base de Phase 4.2b)
- `docs/processes/canvas-daily-cap-handling.md` (cap aplicado upstream — não conflita com fluxo async)

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

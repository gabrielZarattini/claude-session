# SOP — YouTube Studio: painel de gestão do canal (Fatia 1: leitura + métricas)

> **Lei 2 (Processo Antecipado).** Descreve o processo humano equivalente ANTES do código. SSOT da superfície:
> [`docs/bok/youtube-studio/11-api-surface-map.md`](../bok/youtube-studio/11-api-surface-map.md) (verificado contra docs oficiais Google 2026-07-12) +
> [`youtube-api-registry.json`](../bok/youtube-studio/youtube-api-registry.json). Blueprint-mãe:
> [`docs/bok/youtube-studio/00-deepsearch-blueprint.md`](../bok/youtube-studio/00-deepsearch-blueprint.md) (Pilar III / Fatia 5).
>
> **Escopo desta Fatia:** LEITURA — listar os vídeos do canal conectado + métricas, numa tabela CRUD read-only.
> Ações de escrita (Fatia 2) e destrutivas (Fatia 3) têm SOPs/gates próprios (§7 do surface-map).

---

## Operator — quem executa hoje, manualmente?

O próprio dono do canal, dentro do **YouTube Studio** oficial (`studio.youtube.com`): abre a aba **Conteúdo** para ver a lista de vídeos e a aba **Análises** para as métricas (views, tempo de exibição, retenção, tráfego, demografia). Ele lê; não há automação. O painel MCORCH replica essa leitura para o canal **já conectado via OAuth** (`social_accounts`, `platform='youtube'`), sem sair do ecossistema.

## Pré-condição de credencial (UNBREAKABLE — API Tenancy Model)

O token é resolvido **per-user** de `social_accounts` (via `decrypted_social_accounts`, service-role, nunca devolvido ao cliente). **Gap material conhecido:** a conexão inicial foi consentida só com `youtube.upload`, que **não lê** vídeos nem métricas. A Fatia 1 exige, no mínimo, `youtube.readonly` + `yt-analytics.readonly`. Resolução:

1. `social-auth-init` (branch `youtube`) pede o **conjunto completo** de escopos (decisão Sovereign 2026-07-12): `youtube.readonly`, `youtube.upload`, `youtube.force-ssl`, `yt-analytics.readonly`, `yt-analytics-monetary.readonly` — uma reconexão cobre leitura + métricas + receita + ações futuras (o Google força re-auth total ao adicionar escopo depois).
   > ⚠️ **SUPERSEDED (2026-07-16):** a lista de 5 escopos acima é o plano original; o shipado pede **4** (`youtube.readonly` + `youtube` + `youtube.force-ssl` + `yt-analytics-monetary.readonly` — `social-auth-init:151-156`; o monetário é superset do não-monetário, e `youtube.upload` saiu do consent do painel). Concedidos e provados vivos em 2026-07-15 — estado datado em [`01-mrd.md §2.3`](../bok/youtube-studio/01-mrd.md).
2. **Pré-requisito Sovereign-side (Google Cloud Console):** habilitar **YouTube Data API v3** + **YouTube Analytics API**; adicionar os 4 escopos na tela de consentimento OAuth; **Publishing status "In production"** (mesmo *unverified* — a tela "app não verificado" é normal para o próprio canal) para evitar a expiração do refresh-token em 7 dias do modo "Testing".
3. O usuário reconecta (`/dashboard/social` → YouTube → Reconectar) e passa pela tela do Google. O `scope` concedido é gravado em `social_accounts.scopes` — é o sinal de verdade do gap.

## Sequence — ordem de execução (cada passo com critério material)

| # | Passo | Ação | Sucesso material |
|---|-------|------|------------------|
| 1 | Detectar conexão + escopo | Cliente lê `social_accounts` (safe columns, inclui `scopes`) via `useYouTubeConnection` | Se não conectado → CTA conectar. Se conectado sem `youtube.readonly`/`yt-analytics.readonly` → banner "Reconectar" (fail-closed, não chama a API) |
| 2 | Resumo do canal | `youtube-data { action:'channel_summary' }` → `channels.list?mine=true&part=snippet,statistics,contentDetails,status,brandingSettings` (1 unidade) | HTTP 200 + `channel.id` do canal conectado; cards de inscritos/views/nº de vídeos |
| 3 | Listar vídeos | `youtube-data { action:'list_videos' }` → `channels.list?part=contentDetails` (uploads playlist) → `playlistItems.list` (1 un/página de 50) → `videos.list?part=snippet,contentDetails,status,statistics` (1 un/lote) | HTTP 200 + `videos[]` com ≥1 item; paginação via `nextPageToken` ("Carregar mais") |
| 4 | Métricas do canal | `youtube-data { action:'video_metrics' }` → Analytics v2 `reports.query` `ids=channel==MINE` (janela 28d default) | HTTP 200 + `rows` com ≥1 linha; card de views/watch-time/retenção/subs |
| 5 | Render da tabela CRUD | Página display-only renderiza colunas do recurso `videos` (§2.1 do surface-map) com scroll horizontal; read-only nesta fatia | Screenshot 1920×1080 da grade com dados reais + Vision QA APROVADO |

**Economia de quota (§5.1 do surface-map):** preferir `playlistItems.list` (1 un) a `search.list?forMine` (100 un + teto 100/dia). Refresh completo do painel (≤50 vídeos) ≈ **4 unidades** da Data API; das 10.000/dia cabe ~2.500 refreshes. Leitura é praticamente gratuita.

## Verification gates (output esperado — Lei 1)

- **G1 — token per-user resolve:** `youtube-data` lê `decrypted_social_accounts` filtrando `user_id = auth.uid()` + `platform='youtube'`; nunca devolve o token; refresh automático quando `token_expires_at` perto de expirar (reusa `refresh-social-token`).
- **G2 — fail-closed de escopo:** ação de leitura com `scopes` sem `youtube.readonly` → HTTP 403 `youtube_scope_missing` (não tenta a chamada que daria 403 do Google).
- **G3 — cross-tenant:** um usuário só resolve o próprio `social_accounts` (filtro `user_id`); RLS default-deny + `access_token` REVOKE do cliente.
- **G4 — prova de dados reais:** `curl`/invoke real de `list_videos` retorna ≥1 vídeo do canal (HTTP 200 + `items[].id`) **E** `video_metrics` retorna ≥1 linha (HTTP 200) **E** screenshot 1920×1080 Vision-QA-APROVADO. Sem os 3 → não declarar Fatia 1 pronta.
- **G5 — telemetria:** cada path (healthy/degraded) emite `infra_health_logs` `service='youtube-studio'`.

## Recovery path — falha no passo N

- **Re-consent não concedeu `youtube.readonly`** (usuário desmarcou): detectar via `scopes` do token → banner de reconexão, fail-closed (não chamar `videos.list`/`search` que dariam 403).
- **Token expirado / refresh quebrado:** `ensureFreshToken` invoca `refresh-social-token`; se o refresh falha (sem `refresh_token` ou 400 do Google) → `is_active=false` (self-heal) → banner "Reconectar". Nunca sobrescrever um `refresh_token` bom com null.
- **Quota 403 (`quotaExceeded`):** retornar `youtube_quota_exceeded` com mensagem acionável (reset à meia-noite Pacific); backoff no cliente. Evitar `search.list` (bucket de 100/dia).
- **API 5xx do Google:** retry idempotente 1×; senão `youtube_api_error` estruturado.

## Success signal — sinal observável de fluxo completo

O Sovereign abre `/dashboard/youtube`, vê o **cabeçalho do canal** (título/inscritos/views reais), a **tabela de vídeos** do canal com todas as propriedades preenchidas, e o **card de métricas** dos últimos 28 dias — tudo do canal Gabriel AI real, provado por screenshot Vision-QA-APROVADO + linhas materiais (`videos[].id`, `reports rows`).

## Pattern Conformance

Ver [`11-api-surface-map.md §6`](../bok/youtube-studio/11-api-surface-map.md) — placar do módulo: yes 12 · deferred 6 · n-a 5 (gate Closed-Loop Step 3.5 satisfeito).

## Mesh Connection Mandate

Sync bem-sucedido → nó de observação em `mcorch_nodes` (`node_type='observation'`, `service='youtube-studio'`) na primeira leitura de um canal; falhas → `infra_health_logs`; traceability → FR/Fatia deste SOP + Pattern Conformance.

# SOP — Publicar vídeo do ecossistema como Reel (Meta IG + FB)

> Lei 2 (Processo Antecipado). Fatia 2 do ecossistema criativo bidirecional: a saída do Studio/Canvas
> (vídeo 9:16) vira **distribuição real** (IG Reel + FB video). Estende `publish-meta` (BoK meta-api).
> Débito de emenda BoK: **FR-META-REELS** a selar na suíte `docs/bok/meta-api/` (override consciente —
> diretiva Sovereign "comece a Fatia 2 agora").

## Operator
Hoje: o Usuário Zero (ou Usuário 00 operando) abre a **Biblioteca de Assets** (`/dashboard/canvas/assets`),
clica num asset de **vídeo** → diálogo → escreve a legenda → **Publicar Reel**. Amanhã: o Autopilot chama
`publish-meta` com `video_url` no fim do ciclo.

## Pré-requisitos (Sovereign-gated — sem isto, fail-closed 402)
1. **Meta conectado** em `/dashboard/settings`: `meta_config` com `long_lived_token` válido +
   `instagram_business_account_id` (conta IG **Business/Creator**) + pelo menos 1 `page` (FB). Sem a linha
   `meta_config`, `publish-meta` retorna `402 meta_not_configured`.
2. **Vídeo acessível pela Meta:** `video_url` precisa ser uma URL que o servidor da Meta consiga buscar —
   bucket público (URL direta) **ou** signed URL válida durante o processamento do container. Buckets privados
   sem signed URL **falham** (a Meta não autentica).
3. **Specs do Reel:** MP4 H.264/AAC, 9:16 (1080×1920 ok), 3s–90s. Nosso motor HyperFrames entrega isso.

## Sequence (cada step com critério material)
1. Cliente resolve a URL do asset (`resolveAssetUrl` — pública direta ou signed 1h) → **não-null**.
2. `supabase.functions.invoke("publish-meta", { caption, video_url, platforms:["instagram","facebook"] })`
   com o **JWT do usuário** (identidade = dono).
3. `publish-meta` resolve `decrypted_meta_config` por `user_id` (fail-closed 402 se ausente) + gate de reauth
   (402 se `requires_reauth`/expirado).
4. **IG:** `POST /{ig-id}/media` `{media_type:"REELS", video_url, caption}` → `creation_id` → poll
   `status_code` até `FINISHED` (até ~90s; transcode async) → `POST /{ig-id}/media_publish {creation_id}` →
   `id` do Reel. **FB:** `POST /{page-id}/videos {file_url, description}` → `id`.
5. Insere linha em `meta_posts` (`status=published`, `media_url=video_url`, `post_url`) + nó `observation` na malha.
6. Resposta `{ results: [{platform, status:"published", post_url}] }` → toast "Reel publicado em instagram + facebook".

## Verification gates
- `meta_posts` tem a linha `status=published` com `post_url` (SELECT real).
- `post_url` IG = `instagram.com/reel/<id>`; FB = `facebook.com/<id>` → abre o Reel publicado.
- `infra_health_logs service=publish-meta status=healthy` no tick.
- Sem Meta conectado: `402 meta_not_configured` (prova o fail-closed, zero publicação).

## Recovery path (falha no step N)
- **402 meta_not_configured / meta_requires_reauth:** conectar/repastar token em `/dashboard/settings`. Re-publicar.
- **`ig_reels_container_failed` / specs:** vídeo fora de spec (codec/duração/aspect) → re-render no motor (9:16 ≤90s).
- **Timeout de transcode (>90s):** container ainda processando quando o poll esgota → `media_publish` falha; a
   linha `meta_posts status=failed` registra; **retry** a publicação (o vídeo já está no container da Meta).
   ⚠️ Limitação V1: o `creation_id` não é exposto no timeout → o retry recria o container (re-fetch da URL). Vídeos
   curtos (≤10s) transcodam <30s, então o teto de 90s cobre o caso real; async-job é débito V2.
- **`fb_video_failed`:** página FB sem permissão de publish de vídeo → revisar escopos do token.

## Success signal (materialmente observável)
Um **Reel real publicado** no IG/FB do tenant (URL abre o vídeo), linha `meta_posts status=published`, e o nó
`observation` `meta_publish` na malha. Loop criação→fluxo→**distribuição** fechado.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

# SOP: Content Asset History & Two-Phase Video Cockpit

**Status:** ACTIVE · v1.0 · 2026-05-31
**Owner:** Sovereign (Gabriel Zarattini)
**Survival Law 2 compliance:** Escrita ANTES do código (persistência + histórico de assets + split do picker no Cockpit de Vídeo).
**Trigger:** Diretiva Sovereign 2026-05-31 — vídeo gerado "some" ao reabrir o conteúdo; precisa de histórico de assets por conteúdo; fase 1 (roteiro) não deve oferecer modelos de vídeo.

---

## Context

O **Cockpit de Vídeo IA** (`/dashboard/content` → "Gerar Vídeo"; editor em `/dashboard/content/video-editor/:id`) tem dois estágios:

1. **Cérebro — Roteiro (LLM, texto):** `generate-video-script` → endpoint de **chat/`generateContent`**. Precisa de um modelo de **texto**.
2. **Cinema — Render (VLM, vídeo):** `generate-video` → Veo/Seedance (fire-and-forget) → `operation_id` → `check-video-status` (polling/Watcher) baixa o mp4, sobe ao Storage e grava `content_library.media_url`.

**Três defeitos materiais observados (registro `81a487b3`: `media_url=null`, `operation_id=null`, `status=draft`):**

1. **Picker compartilhado (bug do 400):** os dois blocos usam o mesmo `videoModel` (populado por `list-provider-models`, que filtra **vídeo**). Selecionar Veo/Seedance no estágio 1 → `generate-video-script` manda modelo de vídeo ao endpoint de texto → **400** (visto em produção: `seedance/seedance-video-1` → `Erro no provedor openrouter: 400`).
2. **Vídeo "some":** o mp4 finalizado só vivia no estado do browser (`videoUrl`). O registro editado não recebeu `media_url`/`operation_id` (race entre múltiplos registros criados por `autoSaveScript`, e `handleSaveVideo` só grava `media_url` se `videoUrl` já existir em memória). Ao reabrir o editor, `media_url=null` → nada renderiza.
3. **Sem histórico:** `content_library` tem **uma** coluna `media_url`. Imagem e vídeo (e regenerações) sobrescrevem-na. Não há coleção de assets por conteúdo.

---

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (fix) + Edge runtime (`check-video-status`) + frontend (Content/VideoEditor)
- **Reviewer:** Sovereign (Gabriel) — valida na UI (roteiro gera, vídeo persiste ao reabrir, galeria mostra histórico)
- **Owner:** Sovereign — blast radius = Content Studio (geração e persistência de assets pagos por crédito real)

---

## Data model — `content_library.metadata.assets[]` (sem migration)

A coluna `metadata` (jsonb, já existente) ganha um array `assets`. Cada asset finalizado anexa uma entrada (append-only):

```jsonc
metadata.assets = [
  {
    "kind": "video" | "image" | "script",
    "url": "https://…/generated-videos/…mp4",   // null p/ script
    "model": "openrouter/seedance/seedance-video-1",
    "operation_id": "models/veo-…/operations/…", // quando aplicável
    "provider": "gemini" | "openrouter",
    "prompt": "<=200 chars",
    "created_at": "2026-05-31T01:46:39Z"
  }
]
```

`media_url` continua sendo o **asset primário** (último vídeo pronto) p/ compat; `assets[]` é o **histórico completo** (nunca sobrescreve).

---

## Operator (fluxo correto)

| Estágio | Operador | Modelo | Edge | Persistência |
|---------|----------|--------|------|--------------|
| 1. Roteiro | usuário digita tema + escolhe **modelo de TEXTO** | `gemini-2.x-flash` / `openrouter/auto` / llama | `generate-video-script` (stream) | `body` (roteiro) |
| 2. Salvar | "Salvar na Biblioteca" | — | — | INSERT `content_library` (type=video, status=draft) → `contentId` |
| 3. Render | usuário escolhe **modelo de VÍDEO** | Veo / Seedance | `generate-video` (`content_id` obrigatório) | grava `operation_id` + `status=processing` no `contentId` |
| 4. Watcher | polling automático | — | `check-video-status` (`content_id`) | em `completed`: grava `media_url` + `status=ready` **+ append `metadata.assets[]`** |
| 5. Reabrir | editor carrega `id` | — | — | lê `media_url` + `metadata.assets[]` → player + **galeria de histórico**; se `status=processing` → retoma Watcher |

---

## Sequence (fix)

1. **Split do picker (frontend):** estágio 1 ganha `scriptProvider`/`scriptModel` (lista **TEXT_MODELS** curada — sem modelos de vídeo); estágio 2 mantém `videoProvider`/`videoModel` (modelos de vídeo via `list-provider-models`). `handleVideoGenerate` usa `scriptModel`; `handleVideoRender` usa `videoModel`.
2. **Persistência server-side (edge `check-video-status`):** ao `completed`, além de `update({media_url, status:'ready'})`, fazer read-modify-write de `metadata` anexando a entrada `assets[]` (kind=video). Vale p/ ambos os branches (gemini + openrouter). `content_id` continua obrigatório p/ persistir.
3. **Render (frontend):** `VideoEditorPage` carrega `metadata` no on-mount e renderiza uma **galeria de assets** (todos os vídeos do conteúdo) + player do `media_url`. `ContentLibraryPage` exibe contagem/thumb de assets no card.
4. `operation_id` já é persistido por `generate-video` quando `content_id` é passado; garantir que o `content_id` editado é o mesmo do render (sem criar registro órfão).

---

## Verification gates

| Gate | Check | Pass |
|------|-------|------|
| G1 — tsc | `npx tsc --noEmit` | 0 erros |
| G2 — picker | Estágio 1 lista só texto; gerar roteiro com `openrouter/auto` ou `gemini-*-flash` | roteiro streama (sem 400) |
| G3 — persistência edge | `check-video-status` redeployado; após render completo, `GET content_library?id=eq.<id>&select=media_url,metadata` | `media_url` setado **e** `metadata.assets[]` com ≥1 entrada video |
| G4 — reabrir | reabrir `/content/video-editor/<id>` após render | player mostra o vídeo + galeria lista o(s) asset(s) |
| G5 — exploit regressão | re-rodar exploit forjado contra `check-video-status` | 401 (auth ES256 intacta após o re-deploy) |
| G6 — deploy frontend | build via `build-deploy-guardian` (worktree trap) | env baked + chunk novo servido pelo nginx |

---

## Recovery path

- **Race read-modify-write em `metadata`** (duas conclusões simultâneas p/ mesmo content): improvável (1 operação/conteúdo). Se ocorrer, último write vence no `media_url`; `assets[]` pode perder 1 entrada — aceitável p/ v1. v2: RPC atômica `append_content_asset(content_id, asset jsonb)`.
- **`check-video-status` re-deploy quebrar auth:** re-rodar G5 (exploit→401). Rollback: `git checkout HEAD~1 -- supabase/functions/check-video-status/index.ts && npx supabase functions deploy check-video-status`.
- **Frontend build no worktree (armadilha):** seguir `docs/processes/build-deploy-materiality.md` — `cp <main>/.env <wt>/.env && (cd <wt> && bun run build) && rsync -a <wt>/dist/ <main>/dist/` + verificar materialmente.

---

## Success signal

- G1 verde; G2 roteiro gera sem 400; G3 `media_url` + `metadata.assets[]` materialmente no banco; G4 vídeo reaparece ao reabrir + galeria; G5 exploit→401; G6 chunk novo servido.

---

## Out of scope (v1 → fast-follow)

- Histórico de **imagens** (append em `generate-image`/frontend) — v1 cobre vídeo; imagem fica como fast-follow.
- RPC atômica de append; deleção/pin de assets na galeria.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

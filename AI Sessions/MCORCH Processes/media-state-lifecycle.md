# SOP — `media_state`: o estado técnico da mídia (separado do editorial)

> **Status:** ativo desde 2026-07-29 · **Coluna:** `content_library.media_state` (migration `20260729230000`)
> **Gate:** `content_library_media_state_check` (`processing | ready | failed | NULL`)

---

## O obstáculo que gerou este SOP

O pipeline de vídeo escrevia o estado da mídia na coluna `status`, que é o enum **editorial**
`content_status` (`draft | approved | published | archived`). "processing", "ready" e "failed" **não
são membros** desse enum — o Postgres rejeitava o `UPDATE` **inteiro** (22P02), e o `error` nunca era
inspecionado. Consequências reais em produção, verificadas em 2026-07-29:

| Escrita | O que se perdia junto |
|---|---|
| `generate-video` → `{operation_id, status:"processing"}` | **o `operation_id` nunca era gravado** — e o Protocolo de Resgate de Vídeo depende dele para achar a operação |
| `rescue-video` (sucesso) → `{media_url, status:"ready", operation_id}` | **o `media_url` do vídeo recuperado** — e a função ainda devolvia `{status:"success"}` |
| `rescue-video` (desistência) → `{status:"failed", metadata}` | o `rescue_attempts` do mesmo comando → o teto de 5 tentativas nunca engatava |

Duas dimensões ortogonais estavam espremidas numa coluna só. **Um vídeo pode estar `draft`
(editorialmente) e `processing` (tecnicamente) ao mesmo tempo** — com uma coluna, um estado apaga o outro.

---

## O modelo

| Coluna | Pergunta que responde | Domínio |
|---|---|---|
| `status` (`content_status`) | Em que ponto do fluxo **editorial** está? | draft · approved · published · archived |
| `media_state` (text + CHECK) | Qual o estado **técnico** da mídia anexada? | processing · ready · failed · **NULL = sem mídia** |

`NULL` é significativo: conteúdo de texto puro não tem mídia e **não** deve receber um estado
inventado (Lei 1). O backfill marcou `ready` apenas quem já tinha `media_url`.

**Por que `media_state` e não `video_state`/`node_state`/`spaces_state`:** pareia com a coluna irmã
`media_url` da mesma tabela; `content_library` guarda `text|image|video`, então `video_state` nasceria
estreito; e `node_*`/`spaces_*` pertencem a outros domínios (nós do canvas, Spaces) — reusar o
vocabulário criaria colisão com `useCanvasStore` e `video_renders`.

**Por que `text` + `CHECK` e não um enum novo:** é a lição que gerou tudo isto. Enum no Postgres só
aceita `ADD VALUE`; remover exige recriar o tipo e reapontar toda coluna/default/índice dependente.
Um `CHECK` evolui com `DROP CONSTRAINT` + `ADD CONSTRAINT` numa migration reversível. Segue o
precedente da casa: `video_renders.state` é `text NOT NULL DEFAULT 'queued'`.

---

## Operator — quem escreve cada transição

| Transição | Quem executa | Onde |
|---|---|---|
| `NULL → processing` | `generate-video`, ao enfileirar a operação | grava junto com `operation_id` |
| `processing → ready` | `rescue-video` (recuperação) ou a UI ao salvar o vídeo pronto | grava junto com `media_url` |
| `processing → failed` | `rescue-video`, ao estourar o teto de tentativas | grava junto com `metadata.rescue_failed` |
| `* → ready` | operador humano, se salvar mídia manualmente pela Biblioteca | `ContentLibraryPage` |

**Regra inviolável:** nunca escreva `media_state` no mesmo `UPDATE` que carrega o dado que importa
(`media_url`/`operation_id`) **sem checar o `error`**. O supabase-js **não lança** em erro de banco —
ignorar o `error` é como este defeito sobreviveu meses.

---

## Sequence — o ciclo completo

1. Usuário pede geração de vídeo → `generate-video` cria a operação no provedor.
2. `generate-video` grava `operation_id` + `media_state='processing'` (erro logado se falhar).
3. A UI mostra o item na **aba "Em processamento"** da Biblioteca.
4. Se o cliente cair / a operação demorar, o Protocolo de Resgate usa o `operation_id` persistido.
5. `rescue-video` baixa o MP4 (piso de 100 KB), sobe ao bucket e grava `media_url` + `media_state='ready'`.
6. Estourou 5 tentativas → `media_state='failed'` + `metadata.rescue_failed=true`.

---

## Verification gates

| Gate | Comando | Esperado |
|------|---------|----------|
| **G1 — CHECK ativo** | `INSERT ... media_state='banana'` | rejeitado (23514) |
| **G2 — nenhum órfão** | `SELECT count(*) FROM content_library WHERE media_url IS NOT NULL AND media_state IS NULL` | `0` |
| **G3 — a aba enxerga** | filtro "Em processamento" na Biblioteca | lista as linhas `processing`/`failed` do próprio usuário |
| **G4 — RLS intacta** | `media_state` herda as policies owner-scoped de `content_library` | nenhuma policy nova |
| **G5 — erro checado** | grep por `.update({` seguido de `media_state` sem `error` | zero ocorrências |

---

## Recovery path

| Falha | Recuperação |
|---|---|
| Item preso em `processing` sem operação viva | rodar `rescue-video` com o `operation_id` da linha; se não houver, marcar `failed` à mão e regerar |
| `media_state` divergindo do `media_url` (ex.: `ready` sem URL) | `UPDATE content_library SET media_state='failed' WHERE media_url IS NULL AND media_state='ready'` |
| Precisa de um estado novo (ex.: `queued`) | `ALTER TABLE ... DROP CONSTRAINT content_library_media_state_check` + `ADD CONSTRAINT` com a lista nova — **reversível**, ao contrário de um enum |

## Success signal

A aba "Em processamento" fica **vazia** quando não há geração em curso, e um vídeo gerado aparece
nela e sai dela sozinho ao ficar pronto — sem ninguém tocar no banco.

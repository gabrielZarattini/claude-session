# SOP — Ciclo de vida da publicação de asset (Spaces → redes)

> **Lei 2 (Processo Antecipado).** Escrito ANTES do código. Descreve como um humano faria manualmente
> o que a fatia automatiza, com gates materiais em cada passo.
>
> **Origem (2026-07-30):** teste real da conta `tiktok.review@mcorch.com` durante o preparo do App
> Review do TikTok. Sequência que gerou o incidente:
> 1. Clicou Publicar num asset de vídeo → `publish-space-asset` upsertou `space_publish_variants` +
>    inseriu `scheduled_posts`. O cron `auto-publish` postou no TikTok como `SELF_ONLY`.
> 2. O usuário achou que **não** tinha postado (não havia sinal visual pós-clique) e apagou o vídeo
>    manualmente do TikTok e o card do calendário (`scheduled_posts` deletado).
> 3. Nova tentativa → `publish-space-asset:208` devolveu `409 already_enqueued` porque
>    `space_publish_variants.status='scheduled'` e `scheduled_post_id` continuavam apontando para
>    uma linha que não existia mais. Sem cascade. Ficou preso.
>
> Este SOP fecha o loop em 3 frentes: (a) trigger de reconciliação garante que apagar do calendário
> volta a variant a `draft`; (b) o modal do asset ganha aba **Publicações** — o usuário vê exatamente
> onde cada post está antes de sair apagando das redes; (c) o botão Publicar deixa de ser silencioso —
> o pós-clique diz o que aconteceu e direciona para a aba.

---

## 1. Modelo de dados envolvido

```
creative_assets (spine, RLS own)
  └── source_asset_id ──→ space_publish_variants (1 por asset × canal × surface)
                              │  status: draft → scheduled → published
                              │                             ↘ failed / skipped
                              └── scheduled_post_id ──→ scheduled_posts (fila do cron)
                                                          status: queued → publishing → published
                                                                                     ↘ failed / cancelled
```

**Invariante crítico** (o que este SOP protege): *Se `space_publish_variants.status = 'scheduled'`
então `scheduled_post_id` PRECISA apontar para uma linha viva de `scheduled_posts`. Se a
`scheduled_posts` morrer, a variant não pode ficar com referência pendurada.*

**Reconciliação ao apagar do calendário (migration `20260730190000`, revisa a `…180000`):**
apagar a `scheduled_posts` (calendário OU aba Publicações) reconcilia a variant vinculada por status:

| Status da variant | Ação | Racional |
|---|---|---|
| `scheduled` | **DELETE a variant** — some de toda superfície | Era um publish que foi cancelado. A variant nasceu como efeito colateral do "Publicar", não de um "Salvar rascunho" — desfazer o publish deve fazê-la desaparecer. "Apaguei num lugar → sumiu de todos." |
| `published` / `failed` | **Mantém, limpa `scheduled_post_id`** | Um post realmente foi (ou tentou ir) para a rede — é registro histórico. O usuário remove manualmente pela aba (botão **Remover**) se quiser. |
| `draft` / `skipped` | Intocado | `draft` intencional ("Salvar rascunho") nunca teve `scheduled_post_id`, então o trigger nunca o casa. |

**Controle bidirecional na aba Publicações:** toda linha tem uma ação para sair da lista —
**Cancelar** (quando há linha viva na fila: deleta a `scheduled_posts`, o trigger cuida da variant)
ou **Remover** (qualquer outro estado: deleta a variant diretamente via RLS DELETE own). Assim
"apagar de um lugar atualiza em todos" vale nas duas direções (calendário ↔ aba).

## 2. Por que enfileira (não posta síncrono)

Design deliberado: `publish-space-asset` insere em `scheduled_posts` com `scheduled_at = publish_at ??
now()`. O cron `auto-publish` (a cada N minutos) processa os `queued` cujo `scheduled_at <= now()`,
chama `publish-social`, faz o Direct Post na rede real. Motivos: (a) o mesmo pipeline serve "publicar
agora" e "agendar para 3ª às 9h"; (b) upload de vídeo grande não pode travar UI/edge fn; (c) retry
sobrevive a falhas transitórias.

**Trade-off que este SOP endereça:** "publicar agora" fica assincronamente invisível — o usuário
clica, não vê nada, e conclui que não postou. Solução aqui NÃO é remover o async; é dar VISIBILIDADE
canônica (aba Publicações) e feedback pós-clique claro.

## 3. Operator — quem faz manualmente hoje

| Papel | O que faz hoje sem esta fatia |
|-------|-------------------------------|
| **Criador** | Clica Publicar. Vê toast. Não sabe onde ver o estado. Vai olhar diretamente na rede. Se não vê lá "na hora", assume falha e apaga do calendário. |
| **Sovereign** | Precisa rodar SQL manual (destrave) sempre que alguém apaga do calendário sem saber que fica órfã em variants. |

Com esta fatia, ambos ganham observabilidade: o criador vê "Enviado — verifique na aba Publicações"
+ a aba lista status por canal. O trigger elimina o SQL manual do Sovereign.

## 4. Sequence — passo a passo com critério material

| # | Passo | Critério de sucesso material |
|---|-------|------------------------------|
| 1 | Usuário abre um asset em `/dashboard/spaces/assets` | Modal `AssetDetailDialog` abre com duas abas: **Publicar** e **Publicações** |
| 2 | Seleciona canal/formato, escreve caption, clica **Publicar** | `publish-space-asset` retorna 200 `{ok:true, space_publish_variant_id, scheduled_post_id, status:'scheduled'}`. Toast direcional aparece: "Enviado — acompanhe na aba Publicações". |
| 3 | Modal muda para a aba **Publicações** automaticamente | O card do canal recém-publicado aparece com badge **Na fila** + horário-alvo + botão "Cancelar" |
| 4 | Cron `auto-publish` processa (janela `scheduled_at ≤ now()`) → chama `publish-social` → API da rede | Refresh da aba mostra badge **Publicado** + timestamp `published_at` + link para o post na rede |
| 5 | (opcional) Usuário clica **Cancelar** enquanto está `queued` | `DELETE FROM scheduled_posts WHERE id=...` (RLS own) → trigger `trg_reset_variant_on_scheduled_delete` volta a variant a `draft` + limpa `scheduled_post_id` → aba Publicações mostra "Rascunho novamente" → botão Publicar da aba de config volta a funcionar |

## 5. Verification gates

| Gate | Comando / observação | Esperado |
|------|----------------------|----------|
| **G1 — trigger cascade** | `DELETE FROM scheduled_posts WHERE id=<id>` (via cliente com RLS own) | `SELECT status, scheduled_post_id FROM space_publish_variants WHERE scheduled_post_id=<id>` retorna 0 linhas (o campo foi limpo); a variant existe com `status='draft'`. |
| **G2 — não sobrescreve estado histórico** | Se `status='published'` antes do delete, apagar do calendário NÃO regride para `draft` | `status` permanece `published`; só o `scheduled_post_id` vira NULL. Verdade histórica não é reescrita. |
| **G3 — cross-tenant** | Um user B tenta apagar um `scheduled_posts` de user A | A RLS já bloqueia o próprio DELETE (own). O trigger, se acionado por service_role, só atua sobre a variant `WHERE scheduled_post_id=OLD.id AND user_id=OLD.user_id` — nunca cruza tenant. |
| **G4 — idempotente** | Deletar o mesmo `scheduled_posts` 2x | 2º delete afeta 0 linhas (RLS + linha inexistente); trigger não dispara. |
| **G5 — RLS write da variant** | A variant tem `NO INSERT/UPDATE policy` para authenticated (só service-role). O trigger é `SECURITY DEFINER`. | Um user autenticado não consegue setar `status='published'` sozinho. `\dp public.space_publish_variants` confirma. |
| **G6 — visibilidade UX** | Após clique em Publicar, o usuário vê algo mudar em ≤ 1s | Aba muda para "Publicações" automaticamente; card com badge "Na fila" visível; botão Publicar da aba de config fica desabilitado com texto "Já na fila para este formato". |
| **G7 — refresh** | Depois que o cron postar, o usuário volta ao modal | Aba Publicações mostra "Publicado em HH:MM" e (quando o `publish-social` populou) o link para o post na rede. |

## 6. Recovery path — falha no passo N

| Falha | Recuperação exata |
|-------|-------------------|
| Variant ficou órfã (estado antigo, pré-migration) | 1 linha SQL: `UPDATE space_publish_variants SET status='draft', scheduled_post_id=NULL WHERE id=<uuid>`. **A migration NÃO faz backfill** — não temos como saber se um variant `scheduled` antigo teve o post cancelado ou se ainda está em voo com dado histórico perdido. Reconciliar sob demanda é seguro; reconciliar em massa poderia reprogramar posts que o usuário já considerou concluídos. |
| Cron `auto-publish` está parado (fila cresce) | Aba Publicações mostra "Na fila há Nmin". Investigar: `SELECT status, count(*) FROM scheduled_posts GROUP BY 1` e checar se o pg_cron está `active`. |
| `publish-social` falhou (API da rede rejeitou) | `scheduled_posts.status='failed'` + `error_message` populado. Aba Publicações mostra badge "Falhou" + mensagem. Usuário pode Cancelar e refazer. |
| Trigger não disparou (upgrade concorrente?) | `\d+ scheduled_posts` mostra o trigger listado. Fallback manual = mesma linha SQL do primeiro caso. |

## 7. Success signal

Um criador clica Publicar num asset, vê o card do canal aparecer na aba Publicações com "Na fila",
tem certeza de que a operação foi registrada, sabe onde acompanhar, pode Cancelar em 1 clique
enquanto está na fila — e quando o cron publica, o mesmo card vira "Publicado" com timestamp e link.
Não precisa mais abrir a rede social para conferir se aconteceu.

## 8. Superfícies (arquivos)

| Camada | Arquivo |
|--------|---------|
| Migration (trigger cascade tenant-safe) | `supabase/migrations/20260730180000_space_publish_variants_reset_on_scheduled_delete.sql` |
| Hook (variants + posts do asset) | `src/hooks/useAssetPublications.ts` |
| Aba Publicações | `src/components/creative/AssetPublicationsPanel.tsx` |
| Modal reestruturado com Tabs + toast direcional | `src/components/creative/AssetDetailDialog.tsx` |
| Testes | `src/test/asset-publications.test.ts` |

## 9. O que este SOP NÃO faz (escopo negativo)

- **Não muda `publish-space-asset` para síncrono.** O async é decisão arquitetural (§2). A cura é UX
  + reconciliação, não reescrita do transporte.
- **Não substitui o calendário.** A aba Publicações é uma vista focada no asset. O calendário
  continua sendo a vista focada no tempo. Um post existe em ambas as vistas — e as ações de
  Cancelar em qualquer uma delas se propagam pela mesma FK via o trigger.
- **Não muda o comportamento do `auto-publish` cron.** Só a UI de acompanhamento.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

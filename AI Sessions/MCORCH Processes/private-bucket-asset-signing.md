# SOP — Private-Bucket Asset Signing (owner-scoped display across the ecosystem)

> Lei 2 (Processo Antecipado). Nasce do incidente **Fix Assets 2026-07-03**: depois que os buckets
> de mídia viraram PRIVADOS + owner-scoped (fechando o furo de enumeração cross-tenant OTD-SPACES-001,
> migration `20260702230000`), **a maioria das mídias do Usuário Zero sumiu** de todas as superfícies —
> porque o app ainda resolvia URL **pública** (`/object/public/...`) em bucket privado (GET 400) e o
> cliente não conseguia nem **assinar** objetos cujo prefixo não é o `uid` (owner NULL nos uploads
> service-role). Este SOP é a forma correta de **exibir mídia de bucket privado só pro dono**, sem
> reabrir acesso de terceiro.

## Fatos materiais que fundam o processo (provados 2026-07-03, Lei 1)

- Buckets **privados**: `canvas-assets`, `generated-images`, `video-studio-assets`, `video-studio-projects`,
  `vision-artifacts`. Público: `generated-videos` (usado por publish IG/WP que exige URL pública durável).
- `getPublicUrl` em bucket privado → **HTTP 400** (morto). `createSignedUrl` (assinada) funciona.
- Objetos de canvas têm `owner = NULL` (upload service-role) e prefixo `<uid>/`, `<project_id>/` ou `<space_id>/`.
  A policy owner-scoped `canvas_assets_select` só casa `folder[1]=auth.uid()` OU `owner=auth.uid()` ⇒
  o **cliente não assina** objetos project/space-prefixed → nem o dono vê.
- `creative_assets` é o registro canônico de posse (user_id), **sem policy INSERT/UPDATE** (default-deny;
  só `register_creative_asset` service-role escreve) ⇒ ninguém "reivindica" objeto alheio via join.

## Operator (quem executa hoje, manualmente)

MCORCH Master Execution Agent (ou dev). Para servir uma mídia privada a um usuário logado:
resolve `(bucket, key)` do asset → verifica que o usuário **possui** o objeto → gera **signed URL** curta.

## Sequence (ordem, cada passo com critério material)

1. **Capacidade de assinar (server-truth):** o **dono** precisa poder `createSignedUrl` nos PRÓPRIOS objetos.
   Como o prefixo pode ser `uid`/`project_id`/`space_id` e `owner` é NULL, a posse é derivada por **4 rotas**,
   todas `= auth.uid()` (nunca cross-tenant):
   - `folder[1] = auth.uid()` (uploads uid-prefixed);
   - `EXISTS creative_assets (bucket,key) user_id=auth.uid()` (registrados — vídeo project-prefixed);
   - `EXISTS spaces id=folder[1] owner_id=auth.uid()` (voz/vídeo space-prefixed);
   - `EXISTS vm_canvas_projects id=folder[1] user_id=auth.uid()` (saídas de canvas project-prefixed).
   Critério: com o JWT do dono, `createSignedUrl` retorna URL → GET **200**; com JWT de terceiro → **falha**.
2. **Resolução no cliente (display-only, durável):** toda superfície que exibe mídia chama um **normalizador**
   (`src/lib/asset-url.ts`) que: (a) detecta bucket público → `getPublicUrl`; (b) bucket privado → `createSignedUrl`
   FRESCA a cada render. Ele **re-assina** — nunca confia numa URL assada (pública morta **ou** assinada expirada)
   guardada em `graph`/`output_url`. Critério: `<img>/<video>` recebem `/object/sign/...?token=` válido.
3. **Higiene de dado:** `creative_assets.is_public` deve refletir o flag REAL do bucket. Produtores que escrevem
   em bucket privado passam `p_is_public=false`. Critério: `select count(*) from creative_assets where is_public
   and storage_bucket in (<privados>)` = **0**.
4. **Nunca assar URL durável:** `graph`/`output_url` podem conter URL por legado, mas o display SEMPRE re-resolve
   pelo normalizador (passo 2). Publicação server-side (`auto-publish`) já assina no publish-time (provider baixa na hora).

## Verification gates

- **G1 (assinar):** probe com JWT do dono assina os N prefixos distintos do bucket → todos GET 200; JWT alheio → 0.
- **G2 (sem público morto):** nenhuma superfície de display usa `getPublicUrl` em bucket privado (grep + render real).
- **G3 (is_public):** `count(is_public em bucket privado) = 0` pós data-fix.
- **G4 (produtor):** todo `register_creative_asset` para bucket privado passa `p_is_public:false` (grep nos call-sites).
- **G5 (E2E browser):** Biblioteca de Assets + projeto do Canvas Studio + Space renderizam a mídia (sem spinner infinito
  / sem `<img>` quebrada), verificado no dist servido com sessão do Usuário Zero + **Vision-QA**.
- **G6 (cross-tenant):** toda cláusula de posse é `= auth.uid()`; `/security-review` confirma zero rota que exponha
  objeto de outro tenant (o furo que a `20260702230000` fechou permanece fechado).

## Recovery path

- Signed URL falha p/ um prefixo → falta uma rota de posse: adicionar a cláusula `EXISTS` da tabela dona
  (owner-scoped `=auth.uid()`) na policy — **nunca** afrouxar pra `USING (true)` nem reabrir `public`.
- Mídia ainda 400 no browser → a superfície não passa pelo normalizador: rotear aquele `src` pelo `useDisplayUrl`.
- Regressão de novo dado morto → um produtor voltou a passar `is_public:true` em bucket privado: corrigir o call-site.

## Success signal

Usuário Zero abre Biblioteca, Canvas Studio (projeto salvo) e um Space e **vê todas as mídias** (imagens/vídeos/áudio),
com URLs `/object/sign/...` (nunca `/object/public/...` em bucket privado), e um segundo tenant **não** consegue
assinar/ver os objetos do primeiro (G6). Provado por browser real + Vision-QA + probe de assinatura cross-tenant.

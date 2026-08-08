# SOP — Vídeo com avatar (Veo 3.1) no Spaces

> **Lei 2 (Processo Antecipado).** SSOT de espec: `docs/bok/spaces-evolution/25-amendment-veo-avatar-video.md` (FR-SPACES-086..091).
> Contrato do provedor provado materialmente: `.claude/context/veo-31-contract-probe-2026-07-14.md`.
> Este SOP descreve o processo **humano** equivalente — o que um operador faria à mão — e os gates que
> a automação tem de reproduzir. Nasceu ANTES do witness pago (o código já existe; o witness é o gate final).

## Operator

**Quem faz hoje, à mão:** o Sovereign (Usuário Zero), no navegador.
1. Abre `/dashboard/spaces/<projeto>`, seleciona um nó **Imagem→Vídeo**.
2. Escolhe o motor **Google Veo 3.1** (Lite/Fast/Premium) — a opção só aparece se ele tiver chave Google.
3. Conecta um nó **Personagem** (mood board) ao nó de vídeo: cada foto do board vira referência facial.
4. Escreve o prompt de movimento/cena, escolhe duração (4–8s), resolução e proporção.
5. Clica **Gerar vídeo**; espera 1–3 min; o vídeo aparece no próprio nó.

**Equivalente manual sem o MCORCH** (o que a automação substitui): abrir o AI Studio, subir as fotos,
montar o JSON de `predictLongRunning` à mão, pollar a operação, baixar o MP4 com a chave no header, e
guardar o arquivo em algum lugar. O MCORCH faz isso com cobrança, estorno e proveniência.

## Sequence (cada passo com critério de sucesso material)

| # | Passo | Onde | Sucesso material |
|---|-------|------|------------------|
| 1 | Resolver a fila de chaves do tenant | `listProviderKeyCandidates(admin, uid, 'google', keyId?)` | ≥1 candidata; **zero** chave de outro tenant (todas filtradas por `user_id`) |
| 2 | Validar o contrato ANTES de cobrar | `canvas-execute` (guards) | 422 para duração ∉ 4..8, 1080p com duração ≠ 8, modelo fora do catálogo, prompt vazio — **sem débito** |
| 3 | Precificar pela tabela, nunca pelo payload | `veoCost(tier,res,dur)` | custo = âncora declarada (fast·720p·8s = **178 mco**); campo `cost` forjado no body é ignorado |
| 4 | Debitar (ledger-first) | RPC `begin_space_generation` | linha `generations` `running` + débito atômico na MESMA transação |
| 5 | Baixar as referências (≤3) | `fetchVeoImage` → `fetchPublicUrl` | cada URL revalidada a CADA salto 3xx; `image/*`; ≤15 MB; falha de uma referência **degrada**, não derruba |
| 6 | Submeter a operação | `POST models/<tier>:predictLongRunning` | 200 com `name` da operação → gravado em `generations.operation_id` |
| 6b | **Failover por exaustão** | mesmo laço | 429 → tenta a PRÓXIMA chave (429 não cobra no provedor); todas exaustas → passo 8 |
| 7 | Pollar até `done` | `veo-poll` (JWT do dono), chamado pelo **poller de PÁGINA** `useVeoRenderSync` (montado 1× em `CanvasEditorPage`) | `done:true` → MP4 ≥100 KB → bucket **privado** `canvas-assets/<uid>/veo/<gen>.mp4` → `register_creative_asset` → `finalize_space_generation('done')` |
| 7b | **Guardar a alça da geração** | `runSingleNode` / `handleExecute` gravam `veoGenerationId` = `execution_id` pelo store do cliente (o autosave persiste) | o nó sobrevive a reload com a alça; sem ela ninguém consegue pollar/estornar depois |
| 8 | Estornar em qualquer falha | `finalize_space_generation(status='error', refund=mco_charged)` | saldo volta EXATO; a linha vira `error`; o estorno é único (guard `status IN (pending,running)`) |

## Verification gates

| Gate | Como provar | Ferramenta |
|------|-------------|-----------|
| G1 | 402 `google_not_configured` sem chave — zero débito | `scripts/qa/smoke-veo-video.ts` (V1) |
| G2 | 422 pré-débito nos 4 casos de contrato | smoke (V2a–V2d) |
| G3 | saldo intacto após todos os 402/422 | smoke (V3) |
| G4 | preço = âncora; payload não forja | smoke (V4/V5) |
| G5 | `veo-poll` owner-scoped: 401 sem JWT · 404 cross-tenant · 422 sem id · 422 não-Veo | smoke (V6/V7) |
| G6 | **anti-SSRF**: redirect para IP interno é bloqueado, não seguido | `supabase/functions/_shared/public-url.test.ts` (9 testes) |
| G7 | paridade de custo cliente↔servidor (estimativa == cobrança) | `src/test/veo-cost-parity.test.ts` (12 testes) |
| G8 | **witness pago**: vídeo real do avatar, débito exato, Vision QA ocular no MP4 | manual + `scripts/qa/vision-qa.ts` |

## Recovery path

| Falha | Recuperação |
|-------|-------------|
| Submit falhou (rede/502) | estorno imediato na própria resposta (`video_submit_failed`) |
| Todas as chaves com 429 | estorno integral + erro nomeando cada rótulo → o Sovereign recarrega em `ai.studio/projects` ou adiciona chave em `/dashboard/settings` |
| **Ninguém polla (inspector fechado / Run All)** | **RESOLVIDO 2026-08-05** pelo poller de PÁGINA `src/hooks/useVeoRenderSync.ts` (molde `useMotionRenderSync`): varre os `imageToVideo` ocupados, chama `veo-poll` a cada 12s e reconcilia o nó. Nó ocupado **sem** `veoGenerationId` (grafo antigo) é re-atado pela geração viva do ledger (`adoptVeoGenerations`). Paliativo manual: `bun run scripts/qa/recover-stuck-veo.ts <project_id>` |
| Poll com `done:false` para sempre | a varredura de runs travados (`self-heal-spaces`) estorna a linha `running` antiga — o resgate já existe |
| `done` **sem** `video_url` (assinatura falhou) | o sweep NÃO marca sucesso nem falha (não mente sobre um vídeo pago) — segue pollando; se persistir, re-assinar/investigar o `storage_key` da linha |
| Operação sumiu no provedor (404/403 no poll) | estorno (não há job em voo) |
| Download do URI falhou | o poll seguinte re-tenta (o URI do Veo vive ~2 dias; o resgate age em <24h) |
| Poll com a chave ERRADA | **impossível por construção**: a linha guarda `(provider_key_id, key_source)` e o poll re-resolve por esse par (`resolveStoredKey`) |

## Success signal

Um MP4 no bucket privado sob `<uid>/veo/<generation>.mp4`, com linha `generations` `done`, `creative_assets`
registrado, saldo debitado **exatamente** pelo valor da âncora — e o rosto do vídeo é o do mood board
(veredito **ocular**, via Vision QA: métrica estrutural não prova identidade facial).

## Anticorpos desta fatia (Obstáculo → Síntese)

1. **Guard de URL só vale se sobreviver ao redirect.** `assertPublicHttpUrl` + `fetch` (que segue 3xx) = guard inútil.
   Use SEMPRE `fetchPublicUrl` em URL vinda do caller. Teste permanente em `_shared/public-url.test.ts`.
2. **Nó novo no ledger exige o `node_run_id` no cliente.** Sem ele, `canvas-execute` despacha para a branch
   legada — a feature nasce morta em 422. O gate vive em `needsLedgerRun()` (`useCanvasStudio.ts`).
3. **Bucket privado ⇒ `StorageImg`/`StorageVideo`, nunca `<img src>` cru.** Foi pego por prova ocular, não por teste.
4. **Pool de chaves sem failover é pool de mentira.** Se o topo esgota, tudo cai. 429 é grátis → tente a próxima.
5. **Probe de role no caminho SA NÃO é o poison-pill.** Testemunhado 2026-07-15: `durationSeconds=999` num
   `predictLongRunning` via service account retorna `200`+LRO (não o `403` do gate de *API key* do caminho
   Gemini) → enfileira uma operação real (custo). Para provar a role sem gastar, usar **IAM
   `testIamPermissions`** (read-only) ou o próprio `canvas-execute` 403→refund. Nunca um submit poison-pill no SA.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

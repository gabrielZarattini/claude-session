# SOP — Smart-Delete Remoto (verify-existence + delete opcional na rede)

> Lei 2 (Processo Antecipado). Feature: ao remover uma publicação no MCORCH, verificar se ainda existe online e, opcionalmente, deletá-la na plataforma. **Delete remoto é IRREVERSÍVEL** — este SOP define a sequência, os gates de confirmação e o recovery ANTES do código. BoK: `docs/bok/post-engine/15-amendment-smart-delete.md`. SSOT de viabilidade: `.claude/context/smart-delete-feasibility-2026-06-30.md`.

## Operator
Quem executa hoje **manualmente**: o Sovereign, que (a) abre o post na UI da rede (LinkedIn/IG/X/etc.), (b) confirma que é o post certo, (c) clica excluir na rede, (d) volta ao MCORCH e remove o registro. O smart-delete automatiza (a)+(c) para as redes que a API permite, mantendo (b) como confirmação humana.

## Sequence (cada step com critério de sucesso material)
1. **Resolver alvo** — do registro local (`scheduled_posts` OU `meta_posts`), extrair `(platform, remote_id)`. ✅ = `remote_id` não-nulo encontrado numa das 2 fontes. ❌ (nenhum id guardado) → pular direto pro delete local com aviso "sem id remoto guardado".
2. **Resolver credencial per-user** (`auth.uid()`) para a plataforma. ✅ = credencial ativa. ❌ = HTTP 501 `<svc>_not_configured` → oferecer só delete local.
3. **Verificar existência** (`check-post-existence`) com o **sinal correto da Matriz**: WP 200/404 · X `data` vs `errors[]` (HTTP sempre 200!) · YT `items.length` (não 404) · FB/IG `error.code 100` · Pinterest 200/404 · TikTok ausência no array. ✅ = resposta parseada em `{exists, deletable_via_api}`.
4. **Decisão humana (HITL — gate obrigatório):** apresentar o estado real e pedir confirmação explícita. Nunca deletar remoto sem clique. Ramos: deletável+existe → oferecer [Rede+local]/[Só local]; não-deletável → informar + só local; não-existe → só local.
5. **Delete remoto** (`delete-remote-post`, só se o operador escolheu e a Matriz permite) — DELETE idempotente. ✅ = 204/`{deleted:true}`/`{success:true}` OU already-deleted (idempotente). WP `force=false` (Trash).
6. **Delete local** — só APÓS `remote_deleted=true` (ou escolha "só local"). ✅ = linha removida.

## Verification gates (output esperado)
- Verify: `check-post-existence` retorna JSON com `exists` ∈ {true,false,"unknown"} + `deletable_via_api` boolean derivado NO SERVIDOR (não do cliente).
- Delete remoto: status terminal da API (204/success) OU sinal idempotente de already-gone. Registrado em `infra_health_logs service="smart-delete-delete"`.
- Materialidade (Lei 1): após "Rede+local", um `check-post-existence` repetido deve retornar `exists=false` (WP 404 / X `errors[]` / YT `items=[]`). O smoke prova isso.

## Recovery path (falha no step N)
- **Verify falha (rede/timeout):** FAIL-OPEN de conveniência — não travar; oferecer delete local com aviso "não consegui confirmar o estado remoto". (NÃO fail-open de credencial — ausência de credencial é fail-closed 501.)
- **Delete remoto falha (não-idempotente, ex. 403/500):** NÃO apagar o local. Retornar erro claro ("não consegui remover de `<rede>`; o registro local foi mantido — tente de novo ou remova manual"). O post local permanece como âncora para nova tentativa (não vira órfão).
- **Delete remoto sucesso mas delete local falha:** o remoto já foi (irreversível) — retry só do local delete; o `remote_id` já não resolve (idempotente), então re-tentar é seguro.
- **Delete errado (post que não era pra deletar):** WP MVP usa Trash (`force=false`) → recuperável no WP admin. X/Pinterest/IG/etc. **não têm undo** — por isso o gate HITL (step 4) mostra `remote_url` + plataforma + horário ANTES de confirmar. Sem confirmação = sem delete.

## Success signal (materialmente observável)
Fluxo completo confirmado quando: (1) o operador clicou remover; (2) para uma rede deletável, escolheu "Rede+local" e um `check-post-existence` pós-delete retorna `exists=false`; (3) a linha local sumiu; (4) `infra_health_logs` tem os 2 eventos (verify+delete) success; (5) nó de observação na Mesh no 1º delete remoto. Para redes não-deletáveis: o registro local sumiu E a UI mostrou o aviso honesto (nenhuma promessa falsa de delete remoto).

## Anti-patterns proibidos
- ❌ Confiar em flag `deletable`/`confirm` do cliente para executar DELETE (re-derivar no servidor — golden rule intent-execute).
- ❌ Apagar o local ANTES de confirmar o remoto (vira órfão invertido — perde a âncora do retry).
- ❌ Prometer delete remoto em TikTok/IG(conexão atual)/LinkedIn-sem-verify — honestidade obrigatória (FR-SD-004).
- ❌ Checar só HTTP status no X (sempre 200) ou esperar 404 no YT (retorna items=[]) — usar o sinal da Matriz.
- ❌ WP `force=true` (permanente) no MVP sem confirmação reforçada — usar Trash.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

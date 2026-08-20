# SOP — Catálogo do HyperFrames Studio (registry LOCAL curado)

> **Lei 2 (Processo Antecipado).** Capability nova: o host do Video Studio passa a servir um catálogo de
> blocos. Este SOP descreve o processo humano equivalente ANTES do código — quem homologa um bloco, em que
> ordem, como se verifica materialmente, como se reverte, e qual é o sinal de sucesso.
>
> **SSOT correlatas:** `docs/processes/video-studio-editor-deploy-and-provision.md` (deploy do vhost/serviço)
> · SDD §VS-UI-B/§VS-UI-C (contrato do `StudioApiAdapter`) · `scripts/hyperframes/render-core.ts:90`
> (`VALID_TEMPLATES` — a allowlist do motor de render).

---

## 0. Problema que este processo resolve

A aba **catalog** de `/dashboard/spaces/video` exibia `Failed to load catalog`.

Causa-raiz material (não é 404 de rota, não é drift de versão, não é nginx):

```
GET /api/registry/blocks  →  HTTP 501 {"error":"Registry not available"}
```

`createStudioApi` só serve o catálogo quando o adapter implementa o método **opcional**
`listRegistryCatalog()` (`node_modules/@hyperframes/studio-server/dist/index.js:4150-4155`). O
`mcorchAdapter` o omitia **deliberadamente** por risco de supply-chain. O SPA de terceiro não distingue
501 de erro de rede — ele faz `if (!res.ok) throw new Error("Failed to load catalog")` — logo a recusa
correta aparecia ao Sovereign como se fosse um defeito.

**Decisão Sovereign:** OPÇÃO A — catálogo **LOCAL curado**, versionado no repo, **zero egress novo**.

---

## 1. Postura anti-supply-chain (seção normativa)

A recusa registrada no código estava **certa** e permanece válida naquilo que ela de fato protegia: o
*install remoto*. O que muda é apenas que o catálogo deixa de ser vazio — e ele é lido do **disco do
repo**, nunca da rede.

### 1.1 O que ENTRA no catálogo

Um bloco só entra se satisfizer **todos** os critérios abaixo:

| # | Critério | Verificação |
|---|----------|-------------|
| C1 | **É nosso.** O HTML é código soberano versionado no repo (hoje: `scripts/hyperframes/templates/`). | `git log --follow <arquivo>` mostra autoria MCORCH |
| C2 | **O motor sabe rodá-lo.** O nome consta em `VALID_TEMPLATES` (`scripts/hyperframes/render-core.ts:90`). | `grep -n VALID_TEMPLATES scripts/hyperframes/render-core.ts` |
| C3 | **O arquivo existe em disco** no caminho declarado no `registry-item.json`. | o loader dropa o item se não existir (fail-closed) |
| C4 | **Zero fetch externo em runtime** dentro do HTML (fontes self-hosted, sem CDN). | `grep -nE 'https?://' <arquivo>` — só comentários/licença |
| C5 | **Metadados verdadeiros** — `dimensions` e `duration` conferem com o HTML/`RenderSpec`. | leitura do `html,body{width:…;height:…}` |

### 1.2 O que NÃO entra — nunca

- Bloco baixado de registry remoto (`hyperframes.heygen.com` ou qualquer outro host) em runtime **ou**
  em build. Nesta fatia **nada foi baixado de fora**.
- Bloco cujo HTML faça `fetch`/`<script src>` para domínio externo.
- Bloco que o `render-core` não saiba executar (catálogo que promete o que o motor não entrega mente
  para o Sovereign — Lei 1).

### 1.3 Por que o INSTALL remoto continua proibido

`installRegistryBlock` **permanece não implementado** no `mcorchAdapter`. A rota
`POST /api/projects/:id/registry/install` responde `501 {"error":"Registry install not available"}` —
falha limpa e honesta, sem tocar a rede. Razão: instalar um bloco significa **escrever arquivo novo dentro
do diretório de projeto que o sandbox de render executa**. Isso transforma o registry num vetor de
execução de código arbitrário no host de render (que mint JWT do Usuário Zero e fala com o chokepoint de
billing). Um catálogo *read-only* de itens que já vivem no repo não tem essa propriedade: ele apenas
descreve o que já está lá.

**Adicionar um bloco é um ato de commit no repo, revisado — não um clique num botão de terceiro.**

### 1.3-bis Consequência de UI conhecida e ACEITA — o botão "Add" morto

Consequência direta e **esperada** da decisão acima, registrada aqui para que nunca seja reportada como
regressão nova: cada card do catálogo no SPA de terceiro traz um botão **"Add"** que chama
`POST /api/projects/:id/registry/install`. Como o install permanece recusado, **todo clique falha** e o
SPA exibe um toast com o texto do corpo do 501 — em **inglês**, `Registry install not available`
(string do bundle de terceiro `@hyperframes/studio`, ver `NC()` em
`packages/video-studio-host-ui/node_modules/@hyperframes/studio/dist/assets/index-B4h4u7eW.js`; **não é
copy nosso e não é editável sem patchear o vendor**).

Trade-off explícito: antes desta fatia a aba mostrava `Failed to load catalog` (nenhum card, nenhuma
promessa). Agora ela mostra 4 blocos reais **e** um botão que não cumpre — o que roça a doutrina
"UI não promete o que o rail não entrega" (`src/lib/format-specs.ts:9`).

Caminhos possíveis, **todos gated no Sovereign** (nenhum implementado nesta fatia):

1. **Manter como está** — o catálogo é vitrine/documentação; o Sovereign sabe que instalar é via commit.
2. **Implementar `installRegistryBlock` LOCAL-only** — copiar o HTML **do próprio repo** para o dir do
   projeto, sem rede, com allowlist = `VALID_TEMPLATES`. Note que isso é materialmente diferente do
   install remoto recusado em §1.3 (a origem é o repo revisado, não um registry de terceiro), **mas
   continua escrevendo no diretório que o sandbox de render executa** — logo é decisão de postura de
   segurança do Sovereign, não do agente.
3. **Esconder a ação no SPA** — exigiria patchear/forkar o bundle de terceiro (custo de manutenção a cada
   bump de versão).

### 1.4 Quem homologa

| Papel | Quem | Responsabilidade |
|-------|------|------------------|
| **Operator** | Agente MCORCH / engenheiro | escreve o `registry-item.json`, roda os gates |
| **Reviewer** | Sovereign (Gabriel) | aprova o commit que adiciona o item |
| **Owner** | Sovereign | absorve o risco: o bloco roda dentro do sandbox de render |

---

## 2. Operator — quem executa manualmente hoje

Hoje (antes desta automação) o operador humano que quisesse saber "quais blocos o Studio pode oferecer"
teria de: abrir `scripts/hyperframes/templates/`, ler `VALID_TEMPLATES` no `render-core.ts`, e abrir cada
HTML para descobrir dimensão e duração. O catálogo é a **materialização em JSON** desse processo manual —
nada mais.

---

## 3. Sequence — passos numerados (adicionar um bloco ao catálogo)

| # | Passo | Comando / ação | Critério de sucesso material |
|---|-------|----------------|------------------------------|
| S1 | Confirmar C1/C2 | `grep -n VALID_TEMPLATES scripts/hyperframes/render-core.ts` | o nome aparece na allowlist |
| S2 | Ler dimensão real | `grep -nE 'html,\s*body' scripts/hyperframes/templates/<name>.html` | `width:<W>px;height:<H>px` literal |
| S3 | Criar o item | `packages/video-studio-registry/blocks/<name>/registry-item.json` | arquivo existe, JSON válido |
| S4 | Registrar no manifesto | acrescentar `{name,type}` em `packages/video-studio-registry/registry.json` | `jq '.items\|length'` incrementa |
| S5 | Verificar o loader | `bun run scripts/video-studio-host/registry-catalog.ts` (self-check) | imprime N itens, 0 dropados |
| S6 | Reiniciar o host | `systemctl --user restart video-studio.service` | `is-active` = `active` |
| S7 | Provar pela API | `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:3210/api/registry/blocks` | **200** (não 501) |
| S8 | Provar o conteúdo | `curl -s http://127.0.0.1:3210/api/registry/blocks \| jq '.\|length, .[].name'` | N e os nomes esperados |

---

## 4. Verification gates

| Gate | O que prova | Comando | Esperado |
|------|-------------|---------|----------|
| **G1** | A rota deixou de ser 501 | `curl -s -o /dev/null -w "%{http_code}\n" .../api/registry/blocks` | `200` |
| **G2** | O payload é um array de itens tipados | `curl -s … \| jq 'type, (.[0]\|keys)'` | `"array"` + `name/title/type/files/dimensions/duration` |
| **G3** | Fail-closed: item sem arquivo em disco é DROPADO | renomear temporariamente um template → recarregar | o item some do payload (não aparece quebrado) |
| **G4** | Install remoto continua recusado | `curl -s -X POST .../api/projects/<id>/registry/install -d '{"blockName":"x"}'` | `501 {"error":"Registry install not available"}` |
| **G5** | Zero egress novo | `grep -rnE 'fetch\(|https?://' scripts/video-studio-host/registry-catalog.ts` | nenhuma chamada de rede |
| **G6** | Paridade catálogo ↔ motor | nomes do catálogo ⊆ `VALID_TEMPLATES` | conjunto contido |
| **G7** | Manifesto hostil não derruba a rota | montar um `registry.json` de teste em `$TMP` com `{"type":"toString"}`, um `name` duplicado e uma entrada não-objeto → `STUDIO_REGISTRY_ROOT=$TMP bun run scripts/video-studio-host/registry-catalog.ts` | **exit 0**; 3 linhas `skipping …`; os itens válidos seguem servidos (nunca `TypeError`/500) |

> **Por que G7 existe (achado de revisão adversarial, 2026-07-20).** O lookup de tipo era um objeto
> literal, logo `{"type":"toString"}` resolvia para uma **função herdada de `Object.prototype`** — valor
> *truthy* que passava direto pelo guard `if (!typeDir)` e estourava `TypeError` dentro de `join()`. O
> throw escapava do loader → adapter → hono (sem `onError` em `server.ts`) → **HTTP 500 no catálogo
> inteiro**, quebrando o invariante documentado no próprio módulo ("nunca lança por item ruim"). Corrigido
> com mapa de **protótipo nulo** + checagem `typeof typeDir === 'string'` + `try/catch` por entrada +
> dedupe por `type/name`. Um guard que parece total mas tem furo é pior que nenhum: dá falsa segurança.

---

## 5. Recovery path

| Falha no passo | Sintoma | Recuperação exata |
|----------------|---------|-------------------|
| S5 | loader dropa item | o `registry-item.json` aponta `files[].path` para arquivo inexistente — corrigir o caminho relativo (é relativo ao **diretório do próprio `registry-item.json`**) |
| S6 | serviço não sobe | `journalctl --user -u video-studio.service -n 50` → erro de import/JSON. Reverter o commit do item e `systemctl --user restart video-studio.service` |
| S7 | continua **501** | o método não foi reconhecido pelo `createStudioApi`. Reler a assinatura em `node_modules/@hyperframes/studio-server/dist/index.d.ts:156` (`listRegistryCatalog?(): Promise<RegistryItem[]>`) — o nome do método precisa ser **exato** e existir como propriedade própria do objeto adapter |
| S7 | **500** | exceção dentro do loader (JSON malformado). `journalctl --user -u video-studio.service -n 50`; o loader é fail-soft por item, mas `registry.json` inválido derruba a leitura |
| S8 | array vazio `[]` | `registry.json` sem itens **ou** todos dropados por C3. Rodar S5 e ler o motivo do drop no stderr |
| Rollback total | — | `git revert` do commit; o adapter volta a omitir o método e a rota volta ao 501 honesto (estado anterior, sem perda) |

---

## 6. Success signal

**Sinal materialmente observável do fluxo completo:**

1. `curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:3210/api/registry/blocks` → **`200`**
2. O payload lista os blocos homologados com `name`, `dimensions` e `duration` conferindo com o HTML.
3. A aba **catalog** em `/dashboard/spaces/video` renderiza os blocos em vez de `Failed to load catalog`.
4. `POST …/registry/install` segue respondendo `501` — a recusa de supply-chain permanece intacta.

---

## 7. Cadência de manutenção

- **Gatilho obrigatório:** toda vez que `VALID_TEMPLATES` (`render-core.ts:90`) mudar, o catálogo DEVE ser
  revisto na **mesma sessão** (mesma regra do "hotfix vira migration na mesma sessão").
- Template removido do motor → item removido do `registry.json` no mesmo commit.
- O gate C3 (fail-closed por existência de arquivo) é a rede de segurança, não a fonte da verdade.

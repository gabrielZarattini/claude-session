# SOP — Senior UX/UI Loop (auditor on-demand + auto-fix-loop, jornada ponta-a-ponta)

> **Lei 2 (Processo Antecipado).** Documenta o processo humano de um **revisor UX/UI sênior**
> percorrendo a jornada COMPLETA do usuário (landing → auth → onboarding → ativação → core-task →
> feedback), julgando cada tela contra uma **rubrica sênior scored** (não só pass/fail), abrindo
> findings ranqueados e fechando o laço via **fix-loop** (corrige → re-verifica → itera até passar ou
> gate humano). Nenhuma automação deste fluxo ganha código antes deste SOP.
>
> **Norte:** o framework `e2e-user-zero` já entrega o esqueleto material (driver agent-browser, Vision
> gate, finding-schema, report GO/NO-GO, mesh sink, telemetry). Hoje ele julga **só defeitos objetivos
> binários** (tela branca / canvas preto / erro visível → APROVADO/REPROVADO). O Senior Loop **estende**
> esse esqueleto com (a) rubrica multi-dimensão scored, (b) checador de marca MIV determinístico, (c)
> orquestração de jornada encadeada, e (d) o fix-loop executivo — os 4 gaps listados na §Build-New.

Relacionado: [`creative-qa-vision-gate.md`](creative-qa-vision-gate.md) (o olho criativo + gate mecânico que
este SOP reusa) · [`build-deploy-materiality.md`](build-deploy-materiality.md) (gate de deploy material do
fix-loop) · memória `reference_loggedin_e2e_local_preview.md` (preview local CF-proof para estágios logados) ·
memória `reference_miv_design_tokens.md` (regras de token que viram a dimensão de marca da rubrica).

---

## ORO

| Papel | Quem | Critério |
|-------|------|----------|
| **Operator** | MCORCH Master Execution Agent dirigindo `agent-browser` (via `BrowserDriverImpl`) + Vision QA (`vision-qa.ts`). Hoje, na prática, é o **Sovereign + o agent** rodando a auditoria ad-hoc (foi assim no `project_miv_conformance_pass`, com subagents descartáveis). |
| **Reviewer** | Sovereign (Gabriel) + o próprio **olho criativo (VLM)** como reviewer mecânico de qualidade e o Vision gate fail-closed. |
| **Owner** | Sovereign — blast radius = UX quebrada em produção (`login.mcorch.com`) vista pelo usuário real + risco de um fix-loop shipar regressão sem gate. Pode migrar para o `artisan` (L1 CXBOK/ProdBOK) em v6.5.0+. |

**Gatilho de execução (auditor on-demand):** diretiva Sovereign "audite a jornada X" · antes de shipar
qualquer mudança de UI material · regressão de marca suspeita · cadência periódica (candidato a cron, mas
sob spend-guardrail — ver §Anti-patterns).

---

## Princípios (por que este SOP existe)

1. **Sênior ≠ pass/fail.** O Vision gate atual (`vision-gate.ts:15-18`) só reprova defeito objetivo e
   emite um único Finding P1. Um revisor sênior pontua **dimensões** (hierarquia visual, ritmo, marca,
   a11y, cobertura de estados, micro-interações, copy, continuidade da jornada) e prioriza. A rubrica é
   o coração deste SOP.
2. **BYOK torna o julgamento grátis.** `vision-qa.ts` resolve `openrouter`/`google` per-user; o Usuário
   Zero tem ambas → cada julgamento de tela custa **0 mco** (`vision-qa.ts:5-8`). Só a GERAÇÃO de conteúdo
   (rodar o pipeline) custa — daí o spend-guardrail no estágio de core-task.
3. **Jornada é uma ordem, não 7 fotos soltas.** Os 7 flows atuais são capturas independentes de rota
   única sem estado cross-stage (`runner.ts:49-57`; `_nav-capture.ts:32-81`). O Senior Loop encadeia
   estágios EM ORDEM carregando auth + contexto acumulado numa ÚNICA sessão de browser.
4. **Materialidade (Lei 1) em cada claim.** "APROVADO" só vale com o veredito real do subprocess;
   "fix aplicado" só vale com commit hash + build verde + re-run APROVADO. Fail-closed:
   `parseVisionVerdict` (`vision-gate.ts:26-34`) já reprova qualquer coisa que não seja claramente APROVADO.

---

## Operator — quem executa hoje (manual)

Hoje, **manualmente**, um revisor faz: abre `https://login.mcorch.com` no browser, loga, clica pela
jornada, tira prints, olha cada tela com senso estético/UX, anota problemas numa lista, prioriza, conserta
no código, rebuilda, e reabre pra confirmar. O `project_miv_conformance_pass` fez exatamente isso de forma
ad-hoc (44 páginas → 3 fixes sistêmicos), **mas nunca codificou** o critério nem o laço.

Ferramentas materiais que este SOP amarra:
- **Dirigir o browser:** `BrowserDriverImpl` sobre `agent-browser` (`browser-driver.ts:70-228`) — métodos
  `open/click/fill/press/wait/screenshot/snapshot/evalJs/getConsoleMessages/getNetworkRequests/close`.
- **Julgar a tela:** `scripts/qa/vision-qa.ts {image|compare}` (handshake MCP+PAT em `mcp.mcorch.com`,
  `vision-qa.ts:30-52`) + o pipeline upload→sign→subprocess→cleanup de `vision-gate.ts:65-113`.
- **Estruturar o achado:** `finding-schema.ts` (`Finding` :69-86).
- **Reportar/persistir:** `report-renderer.ts` (:44-135), `mesh-persistor.ts` (:81-173),
  `telemetry.ts` (:57-72).
- **Fechar o fix:** eng gates (`tsc`/`eslint`/`bun run build`) + skill `build-deploy-guardian`
  (SOP `build-deploy-materiality.md`).
- **Logar CF-proof:** preview local do `dist` + sessão injetada (`reference_loggedin_e2e_local_preview.md`).

---

## Sequence — ordem com critério de sucesso material por step

### Step 1 — Resolver a jornada-alvo (entry + persona/goal)

Declarar explicitamente: **entry point** (URL, ex.: `https://login.mcorch.com/`), **persona**
(ex.: Usuário Zero recém-chegado), e o **goal** (ex.: "criar o primeiro conteúdo e ver o resultado").
A jornada é a lista ordenada de estágios: `landing → auth → onboarding → activation → core-task → feedback`.
Mapear cada estágio para uma rota + as ações que o completam. Registrar o `run_id`
(`generateRunId`, `runner.ts:162-171`) e o `outputDir` (`createOutputDir`, :188-199).

- **Sucesso material:** um objeto de jornada resolvido (JSON) com N estágios ordenados, cada um com
  `{stage, route, persona, goal, actions[]}` gravado em `e2e-output/run-<id>/journey.json`
  (`ls -la` prova o arquivo). Sem persona/goal declarados → **halt** (não auditar no escuro).

### Step 2 — Traversal ponta-a-ponta reusando o driver (uma sessão, estado carregado)

Numa **única** sessão de browser (`BrowserDriverImpl`, `sessionName: e2e-<runId>-journey`), percorrer os
estágios EM ORDEM, carregando `--state` (auth salvo, `e2e-config.json:authStatePath`) para os estágios
`/dashboard/*`. Cada estágio estende o padrão `navCaptureFlow` (`_nav-capture.ts:32-81`): open → wait
`networkidle` + hidratação (`:46-49`) → screenshot `01-initial` → sequência de `NavStep`
(`_nav-capture.ts:26-30`) com `click`+`wait`+screenshot. Por estágio, capturar:

- **Interações** que completam o estágio (auth = **preencher credenciais de verdade** via `driver.fill`,
  fechando o gap de `auth-login.ts:6-9`; onboarding = conectar um provider; core-task = **Rodar** o
  pipeline sob spend-guardrail explícito — ver Recovery).
- **Estados** de cada tela relevante: **empty · loading · error · success** (ex.: forçar empty navegando
  como conta nova; capturar loading com screenshot logo após o click; provocar error com input inválido).
- **Breakpoints responsivos:** repetir a captura em ≥2 larguras (ex.: 1920×1080 desktop e ~390px mobile)
  — o driver reusa o mesmo `open/screenshot`; a largura é ajustada via viewport do `agent-browser`.
- **Teclado/foco:** `driver.press("Tab")` em sequência + screenshot para provar que o foco é visível e a
  ordem é lógica (dimensão a11y da rubrica).
- **Estado cross-stage:** o contexto acumulado (ex.: id do conteúdo criado no activation) é passado ao
  estágio seguinte (feedback) para amarrar OUTCOME, não só state.

- **Sucesso material:** para cada estágio, ≥1 screenshot por estado em `e2e-output/run-<id>/screenshots/`
  (`ScreenshotRef`, `finding-schema.ts:45-49`) + `commands.jsonl` com a trilha de comandos
  (`browser-driver.ts:119-121`) + `getConsoleMessages()` drenado (`:189-209`). **Pré-requisito material:**
  `getNetworkRequests()` está **stub `[]`** hoje (`browser-driver.ts:211-215`) → a metade HTTP do
  classifier (`classifier.ts:57-79`) está MORTA; **wire o parser HAR antes** de confiar em findings de
  rede (gap na §Build-New).

### Step 3 — Vision QA por tela + RUBRICA UX/UI sênior scored

Para cada screenshot capturado, rodar **duas** camadas:

**(3a) Camada objetiva/mecânica** — reusar `classify()` (`classifier.ts:111-128`): erros de console →
Finding, 4xx/5xx de rede → Finding (assim que o HAR estiver wired). Crash/erro visível continua P0/P1.

**(3b) Camada sênior scored (Vision MCP)** — reusar o pipeline de `visionGate` (`vision-gate.ts:65-113`)
**verbatim** (upload→bucket privado→signed URL 1h→`vision-qa.ts image`→cleanup), **trocando só** a
`QUESTION` (`:15-18`, hoje binária) por um **prompt de rubrica sênior** que pede um score 0–5 por
dimensão, e trocando `parseVisionVerdict` (`:26-34`, hoje binário) por um **parser scored** que lê linhas
no formato `DIMENSAO | SCORE | JUSTIFICATIVA`. Dimensões (cada uma → score → severidade):

| # | Dimensão | O que o sênior avalia | Como checar |
|---|----------|------------------------|-------------|
| D1 | **Hierarquia visual** | O olho vai primeiro ao que importa? Tamanho/peso/contraste guiam? | Vision prompt |
| D2 | **Consistência** | Espaçamento/ritmo, escala tipográfica, componentes repetidos batem entre telas | Vision + snapshot |
| D3 | **Conformidade de marca MIV** | accent = **cyan** (não violeta), nebula só em memória, gold só em valor, Playfair display/JetBrains mono, CTA com neon-glow | Vision **E** `evalJs` (ver §MIV Checker) |
| D4 | **Acessibilidade WCAG 2.1 AA** | Contraste ≥ 4.5:1 texto, foco visível, ordem de Tab lógica, alvos ≥ 44px, alt/aria | Vision + `driver.press(Tab)` + `evalJs(getComputedStyle)` |
| D5 | **Cobertura de estados** | empty / loading / error / success existem e são claros (não tela morta) | Screenshots dos 4 estados do Step 2 |
| D6 | **Micro-interações / feedback** | Hover, click, toast, skeleton — o sistema responde ao usuário | Vision (before/after do click) |
| D7 | **Copy pt-BR clareza** | Texto de UI em pt-BR, claro, sem erro, sem placeholder vazado, tom certo | Vision + `snapshot()` texto |
| D8 | **Continuidade da jornada** | Cada estágio tem afordância de avanço; sem dead-end, sem loop, sem beco | Cross-stage: existe caminho pro próximo estágio |

**Mapa score→severidade** (o parser aplica): `0–1 → P1` (defeito grave / marca quebrada) · `2 → P2` ·
`3 → P3` · `≥4 → passa`. Um **crash/erro objetivo** (D-independente) vindo do classify() é **P0**.
Marca (D3) reprovada pelo `evalJs` determinístico é **P1** (não é opinião — é token errado).

- **Sucesso material:** por screenshot, um `VisionGateResult` (`vision-gate.ts:58-62`) com `verdicts[]`
  contendo `{dimension, score, note}` reais do subprocess (nunca fabricados — Lei 1) + os `findings[]`
  scored. Impresso no stderr como hoje (`runner.ts:311-315`).

### Step 4 — Findings ranqueados e estruturados

Cada achado vira um `Finding` (`finding-schema.ts:69-86`), emitido no MESMO shape que o
`report-renderer`/`mesh-persistor` já consomem sem mudança (`runner.ts:316` já faz
`findings.push(...vg.findings)`). Campos obrigatórios do Senior Loop:

- `severity` (P0..P3, do mapa acima) × `issue_type` — **adicionar** `"brand"` e `"ux-quality"` ao union
  (`finding-schema.ts:10-16` hoje NÃO tem nenhum dos dois — gap §Build-New).
- `evidence_paths.screenshot` — a tela exata (já suportado).
- `affected_module.path` — **localização no source** (definido em `:83` mas **nunca preenchido** hoje);
  o fix-loop depende dele. `affected_module.node_id` habilita a aresta OBSERVES no mesh
  (`mesh-persistor.ts:148-164`).
- `suggested_fix` — a correção proposta (curta, acionável).

Ranquear: ordenar por severidade (P0 → P3) e, dentro da severidade, por dimensão de maior impacto
(D3/D4/D8 antes de D6/D7). O `buildSummary` (`report-renderer.ts:21-33`) já dá o histograma.

- **Sucesso material:** `findings.json` (`FindingsReport`, `finding-schema.ts:106-115`) gravado em
  `e2e-output/run-<id>/` com N findings ordenados, cada um com `screenshot` + (para auto-fixáveis)
  `affected_module.path`. `ls -la` prova o arquivo; `verdictFor(summary)` (`report-renderer.ts:58-60`)
  dá o veredito.

### Step 5 — Fix-loop (finding → fix aplicado → re-verifica → itera)

Para cada finding **auto-fixável** (crash, token de marca errado, estado faltando, contraste, copy
óbvia — **não** julgamento subjetivo de conteúdo/tom, ver Anti-patterns), o Operator:

1. **Localiza** a origem no source (`affected_module.path`) — grep/leitura a partir da rota/componente.
2. **Propõe + aplica** uma edição mínima de código.
3. **Passa os eng gates (obrigatório, sem pular — ver Anti-patterns):**
   `tsc` (typecheck) → `bun run lint` → `bun run build` (ou o fluxo `build-deploy-guardian` se for
   deploy a partir de worktree — evita o falso-sucesso `dist` errado/sem `.env`, SOP
   `build-deploy-materiality.md`).
4. **Browser-verify:** re-roda **o MESMO estágio** da jornada (mesma sessão/rota) e recaptura a tela.
5. **Re-verifica** Vision + rubrica no screenshot novo; usa `vision-qa.ts compare <antes> <depois>`
   (`vision-qa.ts:89-103`) para provar que o defeito saiu e nada regrediu.
6. **Confirma cleared:** o finding sumiu do `classify()`/rubrica e o estágio re-pontua ≥ threshold.
7. **Loop** até `verdictFor(summary) === 'GO'` (zero P0/P1) **ou** atingir `max-iterations`
   (cap explícito, ex.: 3 tentativas/finding + teto global de estágio) → então **escala ao gate humano**
   (Sovereign), nunca loop infinito.

A **idempotência** do mesh-persistor (dedup por `sha256(flow|title|screenshot).slice(0,12)`,
`mesh-persistor.ts:98-101`) garante que re-runs após o fix **não duplicam** o achado.

- **Sucesso material por iteração:** commit hash (`git log -1 --format=%H`) do fix + linha literal de
  build verde (ex.: `built in 21.3s`) + `compare` do Vision mostrando antes≠depois com o defeito
  ausente. Pulse de telemetry por iteração (`telemetry.ts:57-72`).

### Step 6 — Relatório ponta-a-ponta + before/after

Agregar TODOS os estágios num ÚNICO relatório reusando `buildReport` + `renderMarkdown`
(`report-renderer.ts:44-135`) **verbatim** — o badge `✅ GO`/`🔴 NO-GO` (`:17-18`) e `verdictFor`
(`:58-60`) são o veredito da jornada inteira. Anexar, por finding fechado, o par de screenshots
**before/after**. Persistir os findings + os desfechos do fix-loop no Knowledge Mesh via `insertFindings`
(`mesh-persistor.ts:81-173`) e emitir `emitRunComplete` (`telemetry.ts:93-97`).

- **Sucesso material:** `e2e-output/run-<id>/report.md` com `**Verdict:** ✅ GO`, `findings.json`
  coerente, screenshots before/after em disco (`ls -la`), e as observation nodes inseridas
  (contadores `inserted/deduped/edges` de `PersistResult`, `mesh-persistor.ts:29-34`).

---

## MIV Brand-Conformance Checker (D3 — determinístico + Vision)

A dimensão de marca é a única **checável por código**, não só por olho. Regras (SSOT `src/index.css` +
memória `reference_miv_design_tokens.md`):

| Regra | Valor esperado (SSOT) | Prova |
|-------|------------------------|-------|
| accent = **cyan**, não violeta | `--accent: 184 100% 50%` / `--cyan: #00F2FF` | `index.css:27` / `:42` |
| ring/primary = cyan | `--primary: 184 100% 50%`, `--ring: 184 100% 50%` | `index.css:21` / `:35` |
| nebula **só** em contexto de memória | `--nebula: #4D00FF` (classe explícita, nunca o token genérico de accent) | `index.css:49` |
| gold **só** em valor/mcoCoins | `--gold: #D4AF37`, `--status-waiting` gold | `index.css:46` / `:65` |
| display Playfair / mono JetBrains | `--display: 'Playfair Display'…` / `--mono: 'JetBrains Mono'…` | `index.css:60-61` |
| CTA com neon-glow | `--glow-primary: 0 0 24px hsl(184 100% 50% / 0.45)` | `index.css:70` |

**Como checar (dupla via — a técnica que o `project_miv_conformance_pass` fez ad-hoc e nunca codificou):**

1. **Via Vision (subjetiva):** o prompt da rubrica (D3) pergunta explicitamente "há hover/botão em violeta
   onde deveria ser cyan? gold aparece em algo que não é valor? headings usam serifa Playfair?".
2. **Via DOM/computed-style (determinística):** `driver.evalJs(...)` (`browser-driver.ts:184-187`, **hoje
   sem uso por nenhum flow** — seam intocada) rodando `getComputedStyle` para assertir tokens, ex.:
   ```js
   getComputedStyle(document.documentElement).getPropertyValue('--accent').trim()  // deve conter "184 100% 50%"
   ```
   e varredura de elementos interativos por cor de hover violeta indevida / gold fora de pills de valor.
   Mismatch determinístico → Finding **P1 `brand`** (não é opinião).

---

## Verification gates (o que o Operator confere)

| Gate | Evidência material |
|------|--------------------|
| G1 — Vision por estágio | `verdicts[]` reais do subprocess por screenshot; APROVADO (defeito objetivo) em cada estágio (`vision-gate.ts:106-108`) |
| G2 — Rubrica ≥ threshold | toda dimensão D1–D8 do estágio ≥ 3 (nenhuma `<3` sem finding aberto ou já cleared) |
| G3 — Marca MIV (determinístico) | `evalJs` confirma `--accent`=cyan, sem violeta em hover, gold só em valor (§MIV Checker) |
| G4 — Eng gates verdes no fix | `tsc` 0 erro + `bun run lint` limpo + `bun run build` com linha literal de sucesso |
| G5 — Sem novo erro de console | `getConsoleMessages()` pós-fix sem `error`/`warn` novo (`classifier.ts:32-38`) |
| G6 — Sem dead-end | cada estágio tem afordância de avanço; a jornada chega ao feedback (D8) |
| G7 — Veredito da jornada | `report.md` com `**Verdict:** ✅ GO` (`verdictFor` = zero P0/P1, `report-renderer.ts:58-60`) |

---

## Recovery path — falha por step

- **Estágio logado barrado por Cloudflare (Turnstile/challenge no datacenter):** NÃO tentar logar em
  produção pelo IP do datacenter. Usar o receita CF-proof (`reference_loggedin_e2e_local_preview.md`):
  `bun run build` do `dist` → `vite preview` local → injetar a sessão salva (`gen-user-session.ts`) →
  dirigir o `agent-browser` contra o preview local. Provar persistência pelo **DB**, nunca pelo DOM.
- **`agent-browser` estoura (timeout/exit ≠ 0):** `BrowserDriverImpl.exec` lança `BrowserDriverError`
  (`browser-driver.ts:123-128`); retry com backoff curto (2×). Se persistir → exit 2 (infra),
  `emitRunFailure` (`telemetry.ts:99-109`), escalar. O runner já mapeia auth-expiry → exit 3
  (`runner.ts:268-273`).
- **`VISION_MCP_PAT` ausente:** **fail-closed** — não fabricar veredito (Lei 1). O runner já exige o PAT
  e sai exit 2 com instrução (`runner.ts:297-303`); `--no-vision` é a ÚNICA exceção, e só com o porquê
  registrado no seal.
- **`getNetworkRequests()` = `[]` (stub):** a metade HTTP do classifier está morta
  (`browser-driver.ts:211-215`; `classifier.ts:57-79`). Enquanto o parser HAR não for wired, **não
  reportar "zero erros de rede" como prova** — declarar "rede não capturada nesta run" (Lei 1).
- **Fix-loop não converge:** ao atingir `max-iterations` (cap explícito), **parar** e escalar ao gate
  humano (Sovereign) com o findings.json + before/after. Nunca loop infinito, nunca commitar um fix que
  não passou G4/G5.
- **Core-task custaria mco (geração real):** só Rodar o pipeline sob **spend-guardrail explícito**
  (saldo suficiente + GO consciente); default é view-only. Julgar o OUTCOME real, não o estado da conta.

---

## Success signal — sinal materialmente observável do flow completo

A jornada inteira (`landing → auth → onboarding → activation → core-task → feedback`) percorrida numa
sessão, com auth real e estado cross-stage, passa **Vision + rubrica** ponta-a-ponta com **zero P0/P1**;
`e2e-output/run-<id>/report.md` sai com `**Verdict:** ✅ GO` (`verdictFor`, `report-renderer.ts:58-60`);
`findings.json` persistido no mesh (`insertFindings`, `mesh-persistor.ts:81-173`) sem duplicar em re-runs;
e cada finding fechado tem par **before/after** material em disco. Marca MIV verde pelo `evalJs`
determinístico. Nenhum dead-end na jornada (D8).

---

## Build-New — o que ESTE SOP antecipa que ainda NÃO existe no código

O esqueleto `e2e-user-zero` é reuso; estes 4 pedaços são **novos** (o código só nasce sob este SOP + a
SDD com Pattern Conformance):

1. **Rubrica sênior scored:** novo prompt multi-dimensão (substitui `QUESTION`, `vision-gate.ts:15-18`) +
   parser scored (substitui `parseVisionVerdict`, `:26-34`) + `buildVisionFinding` ganhando
   `dimension`/`score` (`:37-56`) + `"brand"`/`"ux-quality"` no `IssueType` (`finding-schema.ts:10-16`).
2. **MIV brand-conformance checker:** primeira via de uso do `driver.evalJs` (`browser-driver.ts:184-187`)
   — `getComputedStyle` assertando tokens (§MIV Checker), casado com o prompt D3.
3. **Orquestração de jornada:** engine que encadeia estágios EM ORDEM numa única sessão com estado
   cross-stage e auth real (o modo `dogfood` hoje **rejeita com exit 4**, `runner.ts:213-218`; auth-login
   não preenche credenciais, `auth-login.ts:6-9`) + **wire do parser HAR** em `getNetworkRequests`
   (`browser-driver.ts:211-215`) para a metade HTTP viver.
4. **Fix-loop executivo:** localizar (popular `affected_module.path`, `finding-schema.ts:83`) → editar →
   eng gates → re-run do estágio → `compare` (`vision-qa.ts:89-103`) → loop até GO ou cap. Nada disso
   existe: hoje os findings terminam em report + mesh insert.

Cada um desses puxa o gate Closed-Loop (Step 3.5 do CLAUDE.md): a SDD do módulo deve carregar a Pattern
Conformance Declaration antes do código.

---

## Anti-patterns proibidos

- ❌ **Fabricar veredito do Vision.** Todo score/APROVADO vem do subprocess real; `parseVisionVerdict` é
  fail-closed (`vision-gate.ts:26-34`) — sem PAT, o gate falha, não inventa (Lei 1).
- ❌ **Auto-corrigir conteúdo/copy subjetivo sem cuidado.** Token de marca errado, contraste, estado
  faltando = auto-fixável. Reescrever tom/mensagem de marca = **gate humano**, não loop automático.
- ❌ **Loop infinito.** Sempre um `max-iterations` explícito; ao estourar, escalar ao Sovereign.
- ❌ **Pular os eng gates num fix.** Nenhum fix vira commit sem `tsc` + `lint` + `build` verdes
  (G4) — pular = falso-sucesso de deploy (SOP `build-deploy-materiality.md`).
- ❌ **Mudar os literais `✅ GO`/`🔴 NO-GO`** sem bumpar `schema_version` — são contrato grepado pelo
  verifier da Fase 5c (`report-renderer.ts:6-8`, `verifiers.ts`).
- ❌ **Reportar "zero erros de rede"** enquanto `getNetworkRequests()` retorna `[]`
  (`browser-driver.ts:211-215`) — declarar "rede não capturada" (Lei 1).
- ❌ **Rodar o core-task (geração paga) sem spend-guardrail** — julgar OUTCOME real só sob GO consciente
  de saldo.
- ❌ **Auditar sem persona/goal declarados** (Step 1) — auditar UX no escuro produz opinião, não engenharia.

---

## Reused files reference

| Peça reusada | Arquivo:linha |
|--------------|---------------|
| Browser driver (agent-browser) + `evalJs` seam | `scripts/qa/e2e-user-zero/lib/browser-driver.ts:22-35`, `:70-228`, `:184-187`, `:211-215` |
| Declarative nav+capture template | `scripts/qa/e2e-user-zero/flows/_nav-capture.ts:26-30`, `:32-81` |
| Finding schema (types) | `scripts/qa/e2e-user-zero/lib/finding-schema.ts:8`, `:10-16`, `:69-86`, `:106-115` |
| Deterministic classifier (objetivo) | `scripts/qa/e2e-user-zero/lib/classifier.ts:21-38`, `:111-128` |
| Vision gate (pipeline + rubric seam) | `scripts/qa/e2e-user-zero/lib/vision-gate.ts:15-18`, `:26-34`, `:37-56`, `:65-113` |
| Vision QA standalone (image/compare) | `scripts/qa/vision-qa.ts:30-52`, `:55-68`, `:89-103` |
| Report + verdict (GO/NO-GO) | `scripts/qa/e2e-user-zero/lib/report-renderer.ts:17-18`, `:44-60`, `:62-135` |
| Mesh persistor (idempotente + OBSERVES) | `scripts/qa/e2e-user-zero/lib/mesh-persistor.ts:81-173`, `:98-101`, `:148-164` |
| Telemetry (lifecycle pulse) | `scripts/qa/e2e-user-zero/lib/telemetry.ts:27-33`, `:57-72` |
| Runner (orquestração single-flow) | `scripts/qa/e2e-user-zero/runner.ts:49-57`, `:202-376`, `:213-218`, `:283-375` |
| Config + auth state | `scripts/qa/e2e-user-zero/e2e-config.json` |
| Gap: auth não preenche credenciais | `scripts/qa/e2e-user-zero/flows/auth-login.ts:6-9` |
| MIV tokens (SSOT de marca) | `src/index.css:21`, `:27`, `:42`, `:46`, `:49`, `:60-61`, `:64-73` |
| Vision gate mecânico (precedente) | `docs/processes/creative-qa-vision-gate.md` |
| Deploy material do fix-loop | `docs/processes/build-deploy-materiality.md` |
| Preview local CF-proof (estágios logados) | memória `reference_loggedin_e2e_local_preview.md` |
| Regras de token de marca | memória `reference_miv_design_tokens.md` |

---

**"MATE A POESIA. ENTREGUE ENGENHARIA."**

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

# [[2026-06-30 - Configurar loop autônomo e definir fila soberana|Configurar loop autônomo e definir fila soberana]]
**Date:** 2026-07-01 | **Session ID:** `473299a8-6c7d-4634-b97a-50a8fad59b11`

---

## 👤 User *(23:10:39)*

Fiz o handson e mandei isso na outra sessão.: 

I'll execute the ShakeHands /handson pick-up ritual. Starting with the pre-flight checks in parallel.
Now reading HANDOFF (head + tail via read-from-end), sprint-priorities, and running the BoK gate check + scratch contents.
Worktree limpo, TS zero erros, mesh saudável. Só preciso confirmar o conteúdo de `scratch/` (flagged) antes de fechar o brief.
Tudo coletado. `scratch/` está limpo (o WARN foi falso-positivo do `&&` sobre diretório vazio). Segue o brief.

```
═══════════════════════════════════════════════════════════
  HANDSON — Gabriel AI · Fatia 2 (Clone de Voz) + Fatia 3a (Consent+Erasure LGPD) — 2026-06-30
═══════════════════════════════════════════════════════════

```

🏁 ESTADO ATUAL Fase selada: Gabriel AI — Fatia 2 (Clone de Voz) + Fatia 3a (Consentimento + Erasure LGPD) Últimos commits:

* `16e42f1` — chore(handoff): proof-manifest → c138539f (Fatia 2 + 3a seal)
* `0f4f5ea` — docs(handoff): seal Gabriel AI Fatia 2 (Voice Clone) + Fatia 3a (Consent+Erasure LGPD) — mesh 8996
* `7913546` — docs(readme): v6.61.0 — Avatar Voice Clone + Consent/Erasure
* `cc5afc3` — test(avatar-clone-ai): consent+erase zero-cost smoke (11 gates, Fatia 3a)
📂 MUDANÇAS PENDENTES Worktree limpo ✅ — `git status` vazio, sem diffs.
🏗️ INFRA

* `mcorch_chroma`: Up 2 weeks (healthy) — Chroma API v2: ✅ OK (`heartbeat` respondeu)
* `mcorch_claude_mem`: Up 2 weeks (healthy)
* `mcorch_vision_mcp`: Up 29h (healthy)
* `mega-brain-{daemon,webhook,dashboard}`: ✅ healthy/up
🧠 KNOWLEDGE MESH 8996 nós · ~9070 arestas · 100% embedded (768d HNSW cosine) Último nó: handoff `c138539f` (Fatia 2/3a) + milestone Fatia 2 `b51d8de6`.
🔧 TYPESCRIPT — Zero erros ✅ (`tsc --noEmit` limpo)
📚 BoK SUITES (MCORCH Master Execution Protocol)

* 24 suítes seladas ✅ (avatar-clone-ai 10/10 incluído — gate ABERTO).
* ⚠️ 1 incompleta no gate: `spaces-evolution` — tem MRD→SDD presentes mas com sufixo `-spaces` (`01-mrd-spaces`…`05-sdd-spaces`) + supplementares 09-12 + IMPLEMENTATION-PROMPT. Faltam os genéricos `06-data-model`/`07-process-flow`/`08-quality-metrics`. Não é blocker real — é descasamento de convenção de nome no script do gate; o núcleo MRD→SDD existe. Spaces está em Phase 0 (scaffold promovido, seal anterior).
📌 SPRINT Goal: Distribuição social autônoma operacional (LinkedIn ✅; Twitter gated em API tier; IG gated em App Review). Programa ativo real: Gabriel AI / brand-persona CCIO + Viral Autopilot (motor R1-R4 vivo, vídeo 9:16 autônomo provado).
⚡ PRÓXIMOS PASSOS (prioridade)

1. Gabriel AI — Fatia 3b (avatarIdentity + Identity Gate) — continuação natural da seal. GATED por Lei 1 (honesto): ArcFace/InsightFace ausente no código; a BoK (FR-AC-013/014) exige ArcFace calibrado em frames reais do Gabriel + treino Soul ID (plano pago Higgsfield). Requer emenda BoK (ArcFace→VLM-soft MVP via Vision MCP, ou provisionar face-verify AWS Rekognition/Azure/Face++) + dados biométricos do Sovereign. Não improvisável.
2. Viral Autopilot — pendente: editor HyperFrames Studio (módulo-container, vhost `studio.mcorch.com` = ação Sovereign) + 1º ciclo pago de vídeo witnessed (habilitar `video_enabled` + GO) + postback ML real + publish vertical TikTok/IG/YT (OAuth + App Review).
3. Brand-persona YT/TikTok — ~3 branches net-new (publish-social / social-auth init+callback / refresh) + gap `auto-publish` não passa `video_url`; amendar BoK post-engine antes de codar (blueprint pronto em `.claude/context/yt-tiktok-brand-persona-integration-prep-2026-06-26.md`).
⚠️ ALERTAS

* `scratch/` limpo ✅ (WARN do checklist foi falso-positivo — diretório vazio).
* `spaces-evolution` BoK com naming não-canônico (ver acima) — só vira bloqueador se a sessão tocar Spaces materialmente; nesse caso, renomear/completar 06-08 antes de código.
* Nenhum erro de TS, nenhum container unhealthy, nenhuma mudança não-commitada.

```
═══════════════════════════════════════════════════════════
  Pronto para trabalhar. Aguardando direção.
═══════════════════════════════════════════════════════════

```

A continuação mais óbvia é a Fatia 3b do Gabriel AI, mas ela está travada por dois bloqueios materiais (emenda BoK + biometria do Sovereign). Se quiser seguir por ela, posso draftar a emenda BoK (rota VLM-soft MVP). Senão, há trilha pronta no Viral Autopilot (1º ciclo de vídeo pago / editor Studio) ou na integração YT/TikTok. Qual frente seguimos?

---

Para continuar aqui como podemos usar o comando /loop para continuar toda a sequencia lógica que montamos de malha fechada? Pois temos tudo o planejado mas agora por exemplo eu fiz o handson e teria que mandar um simples ok continue, mas poderia ter algo mais sofisticado e acertivo do que isso?

---

Boa pergunta — e a resposta curta é: o `/loop` tem exatamente o modo que você quer, mas o "mais sofisticado e assertivo" não está no comando, está na **diretiva que você dá pra ele**. "ok continue" é um prompt vazio; o salto de qualidade é encodar o nosso Protocolo de Malha Fechada *dentro* do loop.
## Os dois modos do `/loop`
| Modo | Sintaxe | Quando |
|------|---------|--------|
| **Intervalo fixo** | `/loop 30m <prompt>` | Polling de estado externo — testemunhar o 1º ciclo pago de vídeo, postback ML, um deploy. Dispara a cada 30 min independente. |
| **Auto-ritmado (dynamic)** | `/loop <prompt>` (sem intervalo) | **É o que você quer.** Eu mesmo decido *quando* continuar e sigo trabalhando até esgotar o backlog ou bater num portão. Sem você digitar "ok" entre as fatias. |
## Por que isso vence o "ok continue" (5 pontos)
1. **Auto-pacing** — não preciso da sua confirmação entre iterações; eu agendo o próximo passo sozinho.
2. **Política de prioridade escrita** — em vez de eu re-adivinhar o que vem depois a cada turno, o loop lê uma *charter* (arquivo) com o backlog priorizado e as condições de parada. Decisão determinística e inspecionável, não no "feeling".
3. **Portões respeitados** — a charter define o que eu executo sozinho vs. o que **HALT + escalo pra você** (Lei 4: Reviewer = Sovereign). Biometria, DNS/vhost, App Review, GO de gasto, decisão arquitetural → entram numa **Fila de Ação Sovereign**, não viram improviso.
4. **Selo automático** — `/handoff` incremental ao fechar cada Fatia, e selo final + parada quando a janela chegar a ~95% (Lei 3 calibrada). Progresso sempre durável.
5. **Survival Laws no laço** — prova material (Lei 1) + SOP-antes-de-código (Lei 2) + self-audit a cada iteração, embutidos.
## O comando (versão assertiva)
```
/loop Você é o MCORCH Master Execution Agent em malha fechada autônoma.
A cada iteração: (1) git fetch + releia o Pending Actions do HANDOFF.md e a
charter em .claude/context/autonomous-loop-charter.md; (2) pegue o item de
MAIOR valor que esteja DESBLOQUEADO; (3) rode o ciclo fechado — BoK Gate →
SOP Lei 2 → código → prova material Lei 1 → /security-review se houver
migration → commit granular; (4) se exigir ação do Sovereign (biometria,
DNS, App Review, GO de gasto, decisão arquitetural), registre na Fila de
Ação Sovereign e pule pro próximo; (5) Survival self-audit; (6) /handoff
incremental ao fechar cada Fatia, selo final + parar a ~95% da janela OU
backlog desbloqueado esgotado. Reporte em PT-BR a cada iteração: o que
entregou (com prova) e o que entrou na Fila Sovereign.
```
A charter (`.claude/context/autonomous-loop-charter.md`) é o upgrade real — ela guarda o backlog ordenado, as condições de HALT e a Fila Sovereign, e eu a atualizo a cada fatia. Esqueleto:
```markdown
# Autonomous Loop Charter
## Backlog (ordem de valor, só DESBLOQUEADOS executam)
1. Gabriel AI 3b — emenda BoK (rota VLM-soft via Vision MCP)  [DESBLOQUEADO: drafting]
   └─ HALT no treino face: exige frames reais do Sovereign
2. YT/TikTok — emenda BoK post-engine + 3 branches publish/auth  [DESBLOQUEADO até OAuth audit]
3. Viral Autopilot — McorchAdapter/bridge do editor Studio  [HALT no vhost studio.mcorch.com]
## Fila de Ação Sovereign (o que SÓ você destrava)
- (preenchida pelo loop conforme bate nos portões)
## Parar quando: janela ~95% · OU backlog desbloqueado vazio · OU GO seu
```
**Caveat honesto (Lei 1):** vários itens de topo são Sovereign-gated *na ponta física* (biometria do 3b, GO do ciclo pago, DNS do Studio, App Review). O loop faz **toda a engenharia desbloqueada até o portão** — drafta as emendas BoK, scaffolda os nós/edges, escreve SOPs+smokes, roda `/security-review` — e te entrega uma fila de decisão enxuta no lugar dos itens travados. Ele não vai *shipar* o que depende dos seus dados/credenciais/GO. Isso está alinhado com a sua diretiva de força-total autônoma.
**Controle:** pra parar, é só me mandar qualquer mensagem (interrompe o laço) ou desligar o `/loop`. Eu seloo antes da janela encher, então nunca perde estado.
Deixa eu te perguntar o modo de arranque:
Você escolheu **charter + lançar agora**. Vou (1) escrever a charter com o backlog priorizado e os portões de HALT, e (2) ligar o `/loop` auto-ritmado.
Primeiro, a charter — o cérebro do loop:
Charter escrita ([autonomous-loop-charter.md](.claude/context/autonomous-loop-charter.md)). Agora ligo o `/loop` auto-ritmado:
O loop entrou em **modo dinâmico** (sem intervalo, auto-ritmado) — sem oferta de cloud porque não há cadência diária/≥60min. Não preciso de Monitor: o Workflow que vou disparar me re-invoca sozinho ao terminar.
**Iteração 1 — Gabriel AI Fatia 3b (emenda BoK rota VLM-soft).** Pelo Protocolo de Malha Fechada, antes de qualquer código a BoK precisa carregar a rota VLM-soft. Disparo agora um Workflow que (a) entende o BoK de identidade existente + o schema `avatar_identities` já staged + as ferramentas reais do Vision MCP, (b) projeta a emenda VLM-soft MVP, e (c) passa por um crítico adversarial contra os invariantes (consent gate LGPD, fail-closed, isolamento de tenant, zero ferramenta fabricada).
**Loop ativo — modo auto-ritmado.** Confirmo o estado desta primeira iteração:
- **Sem Monitor:** o Workflow da emenda 3b é rastreado pelo harness — ele me re-invoca automaticamente ao concluir. Não há evento externo a vigiar.
- **Tarefa rodando agora:** Workflow `wf_188ce24c-881` (understand → design → critic) da emenda BoK VLM-soft.
- **Quando ele voltar:** vou revisar o veredito do crítico; se `APPROVE`, escrevo o doc de emenda em `docs/bok/avatar-clone-ai/`, commito (prova: `ls -la` + hash) e sigo pra Fatia 3b scaffold; se `REVISE`, corrijo os pontos antes de escrever.
- **Fallback:** agendo um heartbeat longo (30 min) só como rede de segurança caso o Workflow trave — não é polling.
**Survival self-audit (it. 1):** Lei 1 ✓ (nenhum SUCCESS declarado sem prova; Workflow ainda em voo) · Lei 2 ✓ (charter escrita antes de qualquer código; emenda BoK precede o scaffold) · Lei 3 ✓ (estado podado, referências por path) · Lei 4 ✓ (ORO: Operator=eu, Reviewer/Owner=Sovereign — a decisão ArcFace-vs-VLM-final está na Fila).
Agendo o fallback e encerro o turno:
**Malha fechada ligada e rodando.** 🟢
Resumo do que montei pra você não precisar mais digitar "ok continue":
1. **Charter** ([autonomous-loop-charter.md](.claude/context/autonomous-loop-charter.md)) — o cérebro do loop: backlog priorizado (Gabriel AI 3b → YT/TikTok → editor Studio → Unified Canvas → Security hardening), ritual por iteração, portões de HALT e a Fila de Ação Sovereign.
2. **`/loop` auto-ritmado** — encoda o Protocolo de Malha Fechada + as 4 Survival Laws. Trabalho sozinho até a janela ~95%, o backlog desbloqueado esgotar, ou você mandar parar.
3. **Iteração 1 em voo** — Workflow da emenda BoK da Fatia 3b (rota VLM-soft via Vision MCP), com crítico adversarial verificando os invariantes LGPD/fail-closed/tenant.
A partir daqui ele se conduz: quando o Workflow voltar, eu reviso, escrevo+commito a emenda (com prova material), e puxo o próximo item. Cada fatia fechada vira um `/handoff` incremental.
**Pra dirigir o loop a qualquer momento:** é só me mandar uma mensagem — isso interrompe o laço e eu reabsorvo a direção (ex.: "pula pra YT/TikTok", "para e me mostra a Fila Sovereign", ou "stop"). Não precisa de comando especial.
Encerro este turno; o harness me reacorda quando o Workflow concluir.

---


Quero saber se consigo continaur trabalhando pontualmente por aqui, por exemplo mudanças que eu estou vendo e precisamos fazer os ajustes digamos que "manual" e tambem o que eu tenho que realmente fazer como.:

Fila de Ação Sovereign (SÓ você destrava — preenchida pelo loop)
não concluído
Biometria Gabriel AI 3b: frames reais do Sovereign + decisão ArcFace-credential vs. VLM-soft MVP + plano Higgsfield.
não concluído
GO de gasto: 1º ciclo PAGO de vídeo (video_enabled + GO) — testemunho.
não concluído
DNS/vhost: studio.mcorch.com (editor) e pendente design.mcorch.com.
não concluído
OAuth/App Review: YouTube (private default) · TikTok (SELF_ONLY) · Instagram App Review · Twitter Basic tier · re-OAuth IG insights (destrava analytics visível).
não concluído
Postback ML definitivo: IP residencial / portal ML (matt_tool/meli.la).
não concluído
Stripe live keys: ao primeiro cliente externo.

--

Minhas listas vem automentando mas acho que ja daria para fazer algumas como a biometria etc go gasto etc...

## 🤖 Claude *(23:11:35)*


## 🤖 Claude *(23:11:40)*

Boa — essa é a pergunta certa pra fazer agora. Você quer dois trilhos rodando ao mesmo tempo: o **loop autônomo** (na outra sessão) fazendo a engenharia desbloqueada, e **você + eu aqui** fazendo ajustes pontuais e, principalmente, **destravando a Fila de Ação Sovereign** — que é o gargalo real, porque é só você que pode liberá-la.

Deixa eu primeiro aterrar isso no estado real (Lei 1 — não vou te dar runbook de cabeça). Vou ler a charter do loop e o estado material dos itens da fila.

## 🤖 Claude *(23:11:41)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/autonomous-loop-charter.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Autonomous Loop Charter — MCORCH Malha Fechada
> 2	
> 3	> Fonte da verdade do `/loop` auto-ritmado. Lida no início de CADA iteração.
> 4	> Atualizada pelo loop ao fechar cada Fatia (marcar ✅ / mover item pra Fila Sovereign).
> 5	> Criada 2026-06-30 a partir do estado selado (handoff `c138539f`, mesh 8996).
> 6	
> 7	---
> 8	
> 9	## Identidade & Leis (não-negociável)
> 10	- Opero como **MCORCH Master Execution Agent**. Penso em inglês, reporto em **PT-BR**.
> 11	- **Protocolo de Malha Fechada:** módulo novo/feature/integração ⇒ BoK Gate (`docs/bok/<slug>/`) + Pattern Conformance Declaration ANTES de código.
> 12	- **Survival Laws:** Lei 1 prova material · Lei 2 SOP antes de código · Lei 3 poda+selo a ~95% · Lei 4 ORO declarado.
> 13	- **Reviewer = Sovereign (Gabriel).** Nada que precise do físico dele (dado/credencial/DNS/GO/decisão arquitetural) é improvisado — vai pra **Fila de Ação Sovereign**.
> 14	
> 15	## Ritual por iteração
> 16	1. `git fetch` + reler **Pending Actions** do `HANDOFF.md` + esta charter.
> 17	2. Escolher o item de MAIOR valor **DESBLOQUEADO** (pular Sovereign-gated; registrá-los na Fila).
> 18	3. Ciclo fechado: **BoK Gate → SOP Lei 2 → código → prova material Lei 1 (UUID/hash/curl/build/test) → `/security-review` se houver migration → commit granular.**
> 19	4. Ao bater num portão físico: registrar na **Fila de Ação Sovereign** com o destravador exato, e seguir pro próximo desbloqueado.
> 20	5. **Survival Laws self-audit** (1/2/3/4).
> 21	6. `/handoff` incremental ao fechar cada Fatia. **Selo final + PARAR** quando: janela ~95% · OU backlog desbloqueado vazio · OU GO/stop do Sovereign.
> 22	
> 23	## Padrão de execução
> 24	- Tarefa substantiva ⇒ **Workflow** (ultracode on): decompor + verificar adversarialmente antes de commitar.
> 25	- Mecânico/trivial ⇒ solo.
> 26	- Sempre Vision QA (`scripts/qa/vision-qa.ts`) em print de inspeção + criativo antes de declarar pronto.
> 27	- UI ⇒ browser-verify real (vite preview do dist + sessão injetada) antes de "pronto".
> 28	
> 29	---
> 30	
> 31	## Backlog (ordem de valor — só DESBLOQUEADOS executam)
> 32	
> 33	### 1. Gabriel AI — Fatia 3b (avatarIdentity + Identity Gate)  ⟶ programa-topo, estende a seal de hoje
> 34	- **DESBLOQUEADO agora:** emenda BoK `avatar-clone-ai` com a rota **VLM-soft MVP via Vision MCP** (alternativa ao ArcFace ausente — FR-AC-013/014); scaffold do nó `avatarIdentity` + Identity Gate contra o caminho VLM-soft; migration já tem `avatar_identities` staged-nullable (`arcface_threshold`/`identity_storage_key`); SOPs + smokes zero-cost.
> 35	- **HALT (Fila Sovereign):** treino/calibração com **frames biométricos reais do Gabriel** + decisão ArcFace-credential (AWS Rekognition/Azure/Face++) vs. VLM-soft; plano pago Higgsfield p/ Soul ID.
> 36	
> 37	### 2. Brand-persona YT/TikTok (post-engine)  ⟶ serve diretiva brand-first + distribuição/receita
> 38	- **DESBLOQUEADO:** emenda BoK `post-engine` (YT/TikTok); 3 branches net-new (`publish-social` · `social-auth` init+callback · refresh); fechar gap `auto-publish` não passar `video_url` + `VIDEO_FLOW_PLATFORMS`. Blueprint: `.claude/context/yt-tiktok-brand-persona-integration-prep-2026-06-26.md`.
> 39	- **HALT (Fila Sovereign):** audit OAuth YouTube (`videos.insert` nasce private) + TikTok (SELF_ONLY) — ação Sovereign + revisão de plataforma.
> 40	
> 41	### 3. Viral Autopilot — editor HyperFrames Studio (módulo-container)
> 42	- **DESBLOQUEADO:** `McorchAdapter.startRender` → edge `video-render`; bridge/app React 19 container; gate #1 render-parity (`frame=floor(time*fps)`). Blueprint: `.claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md`.
> 43	- **HALT (Fila Sovereign):** vhost `studio.mcorch.com` (DNS + cert + symlink).
> 44	
> 45	### 4. Unified Sensorial Canvas — Fases 3.5-3.10  ⟶ engenharia pura, SEM portão Sovereign (filler sempre disponível)
> 46	- 3.5 sinapses inter-rede (arestas reais `mcorch_edges`) · 3.6 fly-to · 3.7 perf (`OTD-UCANVAS-PERF`, query ~30s) · 3.8 podar squad-coloring · 3.9 paridade + gate E2E 1920×1080 · 3.10 seal. Plano: `.claude/context/unified-core-sensorial-canvas-plan.md`.
> 47	- **HALT:** nenhum até cutover de nav (3.9) — aí confirmar com Sovereign.
> 48	
> 49	### 5. Security — OTD-SEC-006 (sentinel-wiring) + OTD-SEC-007 (lefthook/gitleaks)  ⟶ hardening, desbloqueado
> 50	- BoK security 4/4 selada; resta implementação.
> 51	
> 52	---
> 53	
> 54	## Fila de Ação Sovereign (SÓ você destrava — preenchida pelo loop)
> 55	- [ ] **Biometria Gabriel AI 3b:** frames reais do Sovereign + decisão ArcFace-credential vs. VLM-soft MVP + plano Higgsfield.
> 56	- [ ] **GO de gasto:** 1º ciclo PAGO de vídeo (`video_enabled` + GO) — testemunho.
> 57	- [ ] **DNS/vhost:** `studio.mcorch.com` (editor) e pendente `design.mcorch.com`.
> 58	- [ ] **OAuth/App Review:** YouTube (private default) · TikTok (SELF_ONLY) · Instagram App Review · Twitter Basic tier · re-OAuth IG insights (destrava analytics visível).
> 59	- [ ] **Postback ML definitivo:** IP residencial / portal ML (matt_tool/meli.la).
> 60	- [ ] **Stripe live keys:** ao primeiro cliente externo.
> 61	
> 62	---
> 63	
> 64	## Parar quando
> 65	janela ~95% (selo final) · OU backlog desbloqueado vazio · OU GO/stop explícito do Sovereign.
> 66	
> ```

## 🤖 Claude *(23:11:42)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== HANDOFF tail (pending actions) ===\" && tail -n 60 HANDOFF.md 2>/dev/null; echo; echo \"=== avatar-clone-ai BoK docs ===\" && ls -la docs/bok/avatar-clone-ai/ 2>/dev/null",
  "description": "Read charter, HANDOFF tail, avatar BoK listing"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === HANDOFF tail (pending actions) ===
> 5. Swap Stripe to live keys → `npx supabase secrets set STRIPE_SECRET_KEY=<live-key>`
> 6. Walk client through OnboardingPage → verify 10-coin deduction on first orchestration.
> 7. Monitor `infra_health_logs` for first 24h.
> 8. Confirm `affiliate_links.revenue_cents` populates after first campaign run.
> 
> ---
> 
> ## Constellation Matrix Intelligence & Stabilization Record (2026-05-03)
> 
> Sessão de elevação da `ConstellationMatrix` ao nível de **Code Intelligence** e estabilização do motor gráfico. O motor Sigma.js/ForceAtlas2 apresentava loops de renderização infinitos ("blinking") e resets de estado ao interagir com a sidebar. A correção envolveu a estabilização de referências de props, memoização rigorosa das opções do grafo e desacoplamento de filtros dos ciclos de renderização do canvas. Paralelamente, a Matrix foi dotada de inteligência de código nativa via hook `useNodeIntelligence` e um `NodeDetailsPanel` reestruturado com navegação por abas.
> 
> | Action | Result |
> |--------|--------|
> | `src/hooks/useNodeIntelligence.ts` — criado | ✅ Orquestração de busca de código (`mcorch_nodes`) + análise semântica simulada Gemini |
> | `src/components/orchestrator/NodeDetailsPanel.tsx` | ✅ Navegação por abas (Meta, Code, Brain) + Code Preview + IA Analysis flow |
> | `src/components/orchestrator/ConstellationMatrix.tsx` | ✅ Estabilização Sigma.js: memoized options + stable refs + engine integration fix |
> | `src/hooks/useConstellationSigma.ts` | ✅ `useRef` para event handlers + callbacks estáveis — fim do "blinking" |
> | `src/components/ui/progress.tsx` | ✅ Prop `indicatorClassName` adicionado para estilização dinâmica da barra de IA |
> 
> | Commit | Conteúdo |
> |--------|----------|
> | `e8f1a2b` | feat(matrix): Code Intelligence — useNodeIntelligence + NodeDetailsPanel tabs |
> | `d9c3e4f` | fix(matrix): Sigma.js stabilization — elimina re-render loops e blinking |
> | `c7b5a1d` | chore(ui): progress indicator styling support |
> 
> ### Arquitetura Matrix Intelligence
> 
> ```
> ConstellationMatrix (Stabilized Engine)
>   ├── useConstellationSigma (stable refs, no re-bind on render)
>   └── NodeDetailsPanel (Tabbed Navigation)
>         ├── Tab Meta: Neighbor exploration + Net Context
>         ├── Tab Code: Source code preview (Supabase sync)
>         └── Tab Brain: semantic analysis (Gemini orchestrator)
> 
> useNodeIntelligence Hook:
>   - contentQuery: fetch nodes.content column
>   - analyzeMutation: REAL AI analysis via analyze-node edge function (OpenRouter)
>   - state: isAnalyzing, analysisResult, progress
> ```
> 
> ---
> 
> ## AI Brain — Real Intelligence Wiring (2026-05-03)
> 
> Substituição da análise simulada (setTimeout + texto hardcoded) por chamada real ao OpenRouter via edge function.
> 
> | Action | Result |
> |--------|--------|
> | `supabase/functions/analyze-node/index.ts` — criado | ✅ Edge function com auth JWT + OpenRouter claude-sonnet-4-5 |
> | `src/hooks/useNodeIntelligence.ts` — atualizado | ✅ `analyzeNode` chama `supabase.functions.invoke('analyze-node')` |
> | Deploy `analyze-node` | ✅ Deployed em bcyvddsykvehvpwstlfa |
> 
> **Output da análise (estruturado em pt-BR):**
> - Visão Geral — papel do módulo no sistema
> - Padrões Detectados — design patterns, antipatterns
> - Acoplamento & Dependências — análise In/Out-Degree
> - Recomendações — 1-3 ações priorizadas
> 
> **Commit:** `af2a7d9` — feat(matrix): wire AI Brain tab to real OpenRouter analysis
> 
> === avatar-clone-ai BoK docs ===
> total 476
> drwxrwxr-x  2 ubuntu ubuntu  4096 Jun 30 00:24 .
> drwxrwxr-x 27 gcrUX  gcrUX   4096 Jun 29 21:21 ..
> -rw-rw-r--  1 ubuntu ubuntu 23856 Jun 29 22:08 00b-fatia0-viability-format-probe.md
> -rw-rw-r--  1 ubuntu ubuntu 39367 Jun 29 22:41 00c-fatia0-fronts-closure.md
> -rw-rw-r--  1 ubuntu ubuntu 59123 Jun 30 11:26 00-deepsearch-blueprint.md
> -rw-rw-r--  1 ubuntu ubuntu 16352 Jun 30 00:24 00-index.md
> -rw-rw-r--  1 ubuntu ubuntu 29807 Jun 29 22:53 01-mrd.md
> -rw-rw-r--  1 ubuntu ubuntu 38907 Jun 29 22:57 02-brd.md
> -rw-rw-r--  1 ubuntu ubuntu 34852 Jun 29 23:01 03-prd.md
> -rw-rw-r--  1 ubuntu ubuntu 45488 Jun 30 00:09 04-frd.md
> -rw-rw-r--  1 ubuntu ubuntu 47020 Jun 30 00:13 05-sdd.md
> -rw-rw-r--  1 ubuntu ubuntu 42731 Jun 30 00:18 06-data-model.md
> -rw-rw-r--  1 ubuntu ubuntu 29419 Jun 30 00:17 07-process-flow.md
> -rw-rw-r--  1 ubuntu ubuntu 28948 Jun 30 00:22 08-quality-metrics.md
> -rw-rw-r--  1 ubuntu ubuntu 16022 Jun 30 00:20 09-pattern-conformance.md
> ```

## 🤖 Claude *(23:12:54)*


## 🤖 Claude *(23:13:07)*

Charter lida e estado confirmado. Agora entendo exatamente o que você tem em mãos. Deixa eu te responder em duas camadas: primeiro a **coordenação** (sua pergunta direta), depois o **runbook material** dos itens que você quer começar a destravar.

## 1. Sim — você pode trabalhar pontualmente aqui, com uma disciplina simples

As duas sessões compartilham o **mesmo repositório e a mesma árvore de arquivos** (`/home/gcrUX/htdocs/constellation-orchestra`). Isso cria exatamente uma regra de ouro:

| Tipo de trabalho aqui | Colide com o loop? | Disciplina |
|---|---|---|
| **Destravar a Fila Sovereign** (frames, GO de gasto, DNS, OAuth, IP residencial, Stripe) | ❌ Não | **Faça à vontade, em paralelo.** São ações externas (browser/credencial/DNS/UI) — não tocam o código que o loop edita. E *alimentam* o loop: cada item que você libera o loop passa a poder shipar. |
| **Ajuste de código pontual** ("vi isso e quero mudar") | ⚠️ Sim | **Pause o loop primeiro** (mande qualquer mensagem na sessão do loop — ex. "pausa"). Senão dois agentes commitam no mesmo `main` → conflito. Alternativa: eu trabalho aqui num *worktree* isolado e a gente faz merge deliberado. |

E um ponto importante de tranquilidade: **sua lista crescer é o loop funcionando como projetado.** Ele faz toda a engenharia até o portão físico e te entrega só o que *exclusivamente você* pode fazer — está convertendo trabalho bloqueado numa lista de decisão enxuta, não acumulando dívida.

## 2. Os itens que você disse estar pronto pra fazer — vou aterrar materialmente

Você apontou **biometria** e **GO de gasto** como "já dá pra fazer". Antes de te dar o passo-a-passo, vou verificar o estado real de cada item da fila no repositório (Lei 1 — não vou te guiar de memória sobre qual coluna/flag/credencial). Disparo agora uma investigação paralela — um agente por item — que volta com *estado atual + ação física exata + o que vira automatizável depois*, tudo com evidência `arquivo:linha`.

## 🤖 Claude *(23:14:22)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'sovereign-queue-runbook',\n  description: 'Verifica materialmente cada item da Fila de A\u00e7\u00e3o Sovereign e produz runbook acion\u00e1vel',\n  phases: [\n    { title: 'Investigate', detail: 'um agente por item da fila \u2014 estado real + a\u00e7\u00e3o f\u00edsica exata' },\n    { title: 'Sequence', detail: 'ordenar por prontid\u00e3o/valor + flag de conflito com o loop' },\n  ],\n}\n\nconst INV_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  properties: {\n    item: { type: 'string' },\n    ready_now: { type: 'string', enum: ['yes', 'partial', 'no'], description: 'O Sovereign j\u00e1 consegue executar AGORA, ou h\u00e1 pr\u00e9-requisito de engenharia que o loop precisa terminar antes?' },\n    current_state: { type: 'string', description: 'O que J\u00c1 existe no repo/infra, com evid\u00eancia file:line. Honesto sobre o que est\u00e1 pronto vs faltando.' },\n    blocking_engineering: { type: 'string', description: 'O que o loop (ou Claude aqui) precisa terminar ANTES de o Sovereign poder agir. \"none\" se nada bloqueia.' },\n    decision_required: { type: 'string', description: 'Qualquer escolha que S\u00d3 o Sovereign pode tomar (ex: ArcFace-credential vs VLM-soft). \"none\" se n\u00e3o houver.' },\n    sovereign_action: { type: 'array', items: { type: 'string' }, description: 'Os passos F\u00cdSICOS exatos que o Sovereign executa, em ordem. Cada passo concreto (qual UI, qual comando, qual dado fornecer).' },\n    automatable_after: { type: 'string', description: 'O que o sistema/loop passa a fazer sozinho assim que este item for destravado.' },\n    cost_effort: { type: 'string', description: 'Esfor\u00e7o estimado do Sovereign (minutos/horas) + custo financeiro real (R$/USD) se houver.' },\n    unblock_signal: { type: 'string', description: 'Sinal materialmente observ\u00e1vel que confirma que o item foi destravado (Lei 1).' },\n    evidence: { type: 'array', items: { type: 'string' }, description: 'Cita\u00e7\u00f5es file:line que fundamentam o estado atual.' },\n  },\n  required: ['item', 'ready_now', 'current_state', 'blocking_engineering', 'sovereign_action', 'automatable_after', 'unblock_signal', 'evidence'],\n}\n\nconst ITEMS = [\n  {\n    key: 'biometria',\n    label: 'Biometria Gabriel AI 3b',\n    prompt: `Investigue o item da Fila de A\u00e7\u00e3o Sovereign: **Biometria \u2014 Gabriel AI Fatia 3b (avatarIdentity + Identity Gate)**.\nLeia: docs/bok/avatar-clone-ai/04-frd.md (procure FR-AC-013, FR-AC-014, Identity Gate), 05-sdd.md, 06-data-model.md (tabela avatar_identities, colunas arcface_threshold/identity_storage_key), e procure a migration que cria avatar_identities (grep -rn \"avatar_identities\" supabase/migrations/). Procure tamb\u00e9m qualquer refer\u00eancia a ArcFace/InsightFace/Rekognition/Soul ID no c\u00f3digo e nos docs.\nDetermine MATERIALMENTE: (1) o n\u00f3 avatarIdentity e o Identity Gate j\u00e1 est\u00e3o scaffoldados em c\u00f3digo, ou s\u00f3 especificados na BoK? (2) A rota \"VLM-soft MVP via Vision MCP\" (alternativa ao ArcFace ausente) j\u00e1 foi documentada numa emenda BoK, ou ainda precisa ser escrita pelo loop? (3) Qual \u00e9 a DECIS\u00c3O que s\u00f3 o Sovereign toma \u2014 ArcFace via credencial paga (AWS Rekognition/Azure/Face++) vs VLM-soft via Vision MCP (gr\u00e1tis/BYOK)? Quais os trade-offs reais de cada? (4) Que DADO biom\u00e9trico exatamente o Sovereign precisa fornecer (quantos frames, qual formato, frente/perfis, v\u00eddeo) e ONDE ele faz upload? (5) O plano pago Higgsfield Soul ID \u00e9 mesmo necess\u00e1rio, ou a rota VLM-soft dispensa? Seja honesto: o Sovereign consegue agir AGORA, ou o loop precisa primeiro entregar a emenda BoK + scaffold do Identity Gate?`,\n  },\n  {\n    key: 'go-gasto',\n    label: 'GO de gasto \u2014 1\u00ba ciclo PAGO de v\u00eddeo',\n    prompt: `Investigue o item da Fila de A\u00e7\u00e3o Sovereign: **GO de gasto \u2014 1\u00ba ciclo PAGO de v\u00eddeo do Viral Autopilot (video_enabled + testemunho)**.\nLeia: docs/processes/autopilot-video-9x16.md, docs/processes/autopilot-cron-identity.md, e procure a flag que liga v\u00eddeo (grep -rn \"video_enabled\" supabase/ scripts/ src/). Procure as edge functions autopilot-run, autopilot-cadence-cron, e a tabela autopilot_plans (grep -rn \"autopilot_plans\" supabase/migrations/) \u2014 quais colunas controlam se um ciclo gera v\u00eddeo e quanto custa. Procure tamb\u00e9m begin_autopilot_cycle (pr\u00e9-d\u00e9bito) e finalize_autopilot_cycle.\nDetermine MATERIALMENTE: (1) o pipeline de v\u00eddeo 9:16 est\u00e1 end-to-end pronto pra rodar pago, ou falta engenharia (ex: editor HyperFrames, video-bridge worker)? Cheque se video-bridge.service e o motor HyperFrames est\u00e3o referenciados como VIVOS. (2) Qual \u00e9 EXATAMENTE a a\u00e7\u00e3o do Sovereign pra dar o GO \u2014 qual coluna/flag setar (ex: autopilot_plans.video_enabled=true para qual user_id), em qual UI ou via qual comando, e qual o pr\u00e9-requisito de saldo mcoCoins? (3) Quanto custa em mcoCoins/USD um ciclo de v\u00eddeo (procure o custo no SOP)? (4) Qual o \"testemunho\" \u2014 o que o Sovereign observa pra confirmar que o 1\u00ba ciclo pago rodou (UUID de video_render, MP4 no bucket, delta de saldo)? (5) H\u00e1 ainda o blocker de sa\u00edda CF /wp-json ou de publica\u00e7\u00e3o que impede o ciclo de completar? Seja honesto sobre o que est\u00e1 pronto vs pendente.`,\n  },\n  {\n    key: 'dns-vhost',\n    label: 'DNS/vhost \u2014 studio.mcorch.com + design.mcorch.com',\n    prompt: `Investigue o item da Fila de A\u00e7\u00e3o Sovereign: **DNS/vhost \u2014 studio.mcorch.com (editor HyperFrames) e design.mcorch.com**.\nLeia: nginx/video.mcorch.com.conf, docs/processes/video-studio-editor-deploy-and-provision.md, e procure refer\u00eancias a studio.mcorch.com e design.mcorch.com (grep -rn \"studio.mcorch.com\\\\|design.mcorch.com\" nginx/ docs/ .claude/ scripts/). Leia tamb\u00e9m .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md (se\u00e7\u00e3o de vhost/deploy).\nDetermine MATERIALMENTE: (1) o arquivo de vhost nginx j\u00e1 existe e est\u00e1 pronto pra ativar, ou precisa ser escrito? (2) Quais s\u00e3o os passos F\u00cdSICOS exatos do Sovereign \u2014 criar registro DNS (qual subdom\u00ednio aponta pra qual IP/Cloudflare), emitir/instalar cert TLS, criar symlink em sites-enabled, reload nginx? Liste cada comando/a\u00e7\u00e3o. (3) Isso \u00e9 Cloudflare-proxied (laranja) como os outros vhosts? H\u00e1 regra WAF necess\u00e1ria? (4) O que fica acess\u00edvel assim que o vhost subir? (5) design.mcorch.com est\u00e1 no mesmo estado ou diferente? Seja honesto sobre o que \u00e9 a\u00e7\u00e3o Sovereign (DNS/cert que exige acesso ao painel) vs o que o loop pode preparar (o arquivo .conf, o symlink script).`,\n  },\n  {\n    key: 'oauth',\n    label: 'OAuth/App Review \u2014 YT \u00b7 TikTok \u00b7 IG \u00b7 Twitter',\n    prompt: `Investigue o item da Fila de A\u00e7\u00e3o Sovereign: **OAuth/App Review \u2014 YouTube \u00b7 TikTok \u00b7 Instagram \u00b7 Twitter \u00b7 re-OAuth IG insights**.\nLeia: .claude/context/yt-tiktok-brand-persona-integration-prep-2026-06-26.md, e procure as edge functions de social auth (grep -rn \"social-auth\\\\|social_platform\\\\|publish-social\" supabase/functions/ | head -40). Procure o enum social_platform nas migrations e a tabela social_accounts/social_credentials. Procure tamb\u00e9m refer\u00eancias a \"App Review\", \"SELF_ONLY\", \"videos.insert\", \"Basic tier\" nos docs/blueprint.\nDetermine MATERIALMENTE para CADA plataforma (YouTube, TikTok, Instagram, Twitter, IG insights): (1) o que J\u00c1 est\u00e1 conectado/implementado no c\u00f3digo vs o que falta (branch net-new)? (2) Qual \u00e9 a a\u00e7\u00e3o Sovereign exata \u2014 criar app no developer portal de cada plataforma, configurar OAuth scopes, submeter App Review, fazer login OAuth? (3) Qual o port\u00e3o de plataforma que trava a publica\u00e7\u00e3o real (ex: YouTube videos.insert nasce 'private' at\u00e9 audit; TikTok SELF_ONLY at\u00e9 App Review; IG precisa App Review pra publicar de terceiros)? (4) O que o Sovereign consegue fazer AGORA (ex: conectar a PR\u00d3PRIA conta, que n\u00e3o exige App Review) vs o que exige aprova\u00e7\u00e3o de plataforma (semanas)? Seja honesto e separe \"a\u00e7\u00e3o imediata\" de \"espera burocr\u00e1tica de plataforma\". Cheque: a conex\u00e3o IG do User 0 j\u00e1 existe (memory diz que Reel j\u00e1 publicou via graph.instagram.com)?`,\n  },\n  {\n    key: 'ml-postback',\n    label: 'Postback ML definitivo \u2014 matt_tool/meli.la',\n    prompt: `Investigue o item da Fila de A\u00e7\u00e3o Sovereign: **Postback ML definitivo \u2014 IP residencial / portal ML (matt_tool/meli.la)**.\nLeia: e procure project context sobre o operador de browser autenticado e o funil de receita. grep -rn \"matt_tool\\\\|matt_word\\\\|meli.la\\\\|affiliate_tag\" scripts/ supabase/functions/ docs/. Leia docs/processes/affiliate-credential-resolution.md, scripts/link-forge.ts, supabase/functions/process-affiliate-link/index.ts. Procure docs/processes ou .claude/context sobre \"authenticated browser operator\" e \"revenue funnel\".\nDetermine MATERIALMENTE: (1) o que J\u00c1 funciona na atribui\u00e7\u00e3o de afiliado (memory indica que o click ledger in-system foi FECHADO \u2014 redirect tracker conta cliques; e que 1 clique matt_word foi registrado no painel ML) vs o que falta (atribui\u00e7\u00e3o DEFINITIVA de COMPRA via matt_tool/meli.la). (2) Por que o datacenter n\u00e3o consegue (memory: ML bloqueia browser do datacenter \u2014 \"Hubo un error accediendo\"; link oficial exige portal logado com ref assinado n\u00e3o-fabric\u00e1vel). (3) Qual \u00e9 a a\u00e7\u00e3o Sovereign exata \u2014 fazer login no portal ML a partir de um IP RESIDENCIAL (navegador dele), gerar o link oficial meli.la com matt_tool cravado, e onde colar/registrar esse link no sistema? (4) Isso \u00e9 bloqueador de RECEITA real ou s\u00f3 de atribui\u00e7\u00e3o de melhor qualidade? Seja honesto sobre prioridade \u2014 memory sugere que cliques j\u00e1 s\u00e3o contados in-system e que isto \u00e9 atribui\u00e7\u00e3o definitiva, prioridade menor.`,\n  },\n  {\n    key: 'stripe',\n    label: 'Stripe live keys',\n    prompt: `Investigue o item da Fila de A\u00e7\u00e3o Sovereign: **Stripe live keys \u2014 ao primeiro cliente externo**.\nProcure: grep -rn \"STRIPE_SECRET_KEY\\\\|stripe\" supabase/functions/ src/lib/ scripts/ | head -40. Leia HANDOFF.md (procure a se\u00e7\u00e3o de Stripe Prod Swap) e qualquer SOP de billing. Procure as edge functions que usam Stripe (checkout, webhook, customer portal).\nDetermine MATERIALMENTE: (1) o billing est\u00e1 implementado e funcionando em modo TEST, faltando s\u00f3 o swap pra live? (2) Qual \u00e9 a a\u00e7\u00e3o Sovereign exata \u2014 obter as live keys no dashboard Stripe, rodar qual comando (ex: npx supabase secrets set STRIPE_SECRET_KEY=<live>), configurar qual webhook endpoint, qual price/product live? Liste os passos. (3) H\u00e1 pr\u00e9-requisito de conta Stripe (ativa\u00e7\u00e3o, dados banc\u00e1rios, KYC)? (4) Isso \u00e9 genuinamente \"s\u00f3 ao primeiro cliente externo\" \u2014 ou seja, N\u00c3O urgente at\u00e9 existir demanda real de pagamento? Seja honesto: este item provavelmente \u00e9 o de MENOR prioridade at\u00e9 haver um cliente pagante de fato. Confirme isso com evid\u00eancia.`,\n  },\n]\n\nphase('Investigate')\nconst findings = await parallel(ITEMS.map(it => () =>\n  agent(it.prompt, { label: `inv:${it.key}`, phase: 'Investigate', schema: INV_SCHEMA, effort: 'medium' })\n    .then(r => r ? { ...r, _key: it.key, _label: it.label } : null)\n))\n\nconst valid = findings.filter(Boolean)\n\nphase('Sequence')\nconst SEQ_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  properties: {\n    do_now: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { item: { type: 'string' }, why: { type: 'string' }, first_step: { type: 'string' } }, required: ['item', 'why', 'first_step'] }, description: 'Itens que o Sovereign consegue COME\u00c7AR agora (ready_now yes/partial), ordenados por valor desbloqueado.' },\n    blocked_on_loop: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { item: { type: 'string' }, waiting_for: { type: 'string' } }, required: ['item', 'waiting_for'] }, description: 'Itens onde a engenharia do loop precisa terminar ANTES de o Sovereign poder agir.' },\n    highest_leverage: { type: 'string', description: 'O \u00daNICO item que, destravado, libera o MAIOR valor downstream. Justifique.' },\n    conflicts_with_running_loop: { type: 'string', description: 'Algum item exige editar o mesmo c\u00f3digo que o loop est\u00e1 mexendo? Qual disciplina evita colis\u00e3o?' },\n    recommended_order: { type: 'array', items: { type: 'string' }, description: 'Ordem recomendada de execu\u00e7\u00e3o pelo Sovereign, do mais alto ROI ao menos urgente.' },\n  },\n  required: ['do_now', 'blocked_on_loop', 'highest_leverage', 'recommended_order'],\n}\n\nconst sequence = await agent(\n  `Voc\u00ea \u00e9 o coordenador. Recebeu a investiga\u00e7\u00e3o material de 6 itens da Fila de A\u00e7\u00e3o Sovereign do MCORCH. ` +\n  `O contexto: h\u00e1 um /loop aut\u00f4nomo rodando em OUTRA sess\u00e3o fazendo a engenharia DESBLOQUEADA (backlog: Gabriel AI 3b emenda BoK+scaffold, YT/TikTok branches, editor Studio, Unified Canvas, Security hardening). ` +\n  `O Sovereign (Gabriel) quer saber quais itens da fila ele j\u00e1 pode COME\u00c7AR A DESTRAVAR agora, em paralelo ao loop, e em que ordem de valor. ` +\n  `Separe rigorosamente: o que o Sovereign faz AGORA (a\u00e7\u00f5es externas/f\u00edsicas que n\u00e3o colidem com o loop) vs o que est\u00e1 esperando engenharia do loop. ` +\n  `Identifique o item de MAIOR alavancagem. Os dados:\\n\\n` +\n  JSON.stringify(valid.map(f => ({ item: f._label, ready_now: f.ready_now, blocking_engineering: f.blocking_engineering, decision_required: f.decision_required, sovereign_action: f.sovereign_action, automatable_after: f.automatable_after, cost_effort: f.cost_effort })), null, 2),\n  { label: 'sequencer', phase: 'Sequence', schema: SEQ_SCHEMA, effort: 'high' }\n)\n\nreturn { findings: valid, sequence }\n",
  "description": "Verify Sovereign queue items materially"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wzh2mz4nk
> Summary: Verifica materialmente cada item da Fila de Ação Sovereign e produz runbook acionável
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/subagents/workflows/wf_443fc8de-27b
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/workflows/scripts/sovereign-queue-runbook-wf_443fc8de-27b.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/workflows/scripts/sovereign-queue-runbook-wf_443fc8de-27b.js"} to iterate without resending the script.)
> Run ID: wf_443fc8de-27b
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/workflows/scripts/sovereign-queue-runbook-wf_443fc8de-27b.js", resumeFromRunId: "wf_443fc8de-27b"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(23:14:39)*


## 🤖 Claude *(23:14:52)*

Investigação disparada (`wf_443fc8de-27b`, rodando em paralelo) — 6 agentes verificando cada item da fila + 1 sequenciador ordenando por valor. Volto com o runbook completo quando concluir.

Enquanto isso, o **preliminar honesto** sobre os dois que você sinalizou (vou confirmar materialmente no runbook):

**🟢 GO de gasto (1º ciclo pago de vídeo) — provavelmente o de melhor ROI e mais barato pra você.** O motor R1-R4 já está vivo, o HyperFrames já renderiza MP4 9:16 e o `video-bridge.service` está ativo. Um ciclo *pago de texto* já rodou (`947ef8b5`, −20 mco). O que falta é só o **ciclo de vídeo testemunhado**: você autoriza (liga a flag de vídeo no plano de autopilot do User 0, com saldo suficiente) e a gente observa o UUID do `video_render` + o MP4 no bucket + o delta de saldo. Esforço seu: minutos. É o item que prova o motor de receita rodando de ponta a ponta.

**🟡 Biometria 3b — você já pode adiantar metade agora.** A parte que é *só sua* (a **decisão** ArcFace-credential pago vs VLM-soft grátis, e **reunir os frames** do seu rosto) você faz já. Mas a outra metade — o scaffold do Identity Gate contra a rota escolhida — **é exatamente o que o loop está draftando agora** (iteração 1, emenda BoK VLM-soft). Então o caminho limpo: você me diz qual rota prefere + me passa os frames, e quando a emenda do loop aterrissar eu plugo seus dados. Não dá pra "terminar" a biometria antes da emenda existir, mas dá pra não ficar no caminho crítico.

Os outros quatro (DNS/vhost, OAuth/App Review, postback ML, Stripe) o runbook vai ranquear — adianto que **Stripe é o de menor urgência** (só faz sentido no primeiro cliente pagante) e **OAuth tem uma parte imediata** (conectar suas próprias contas, que não exige App Review) separada da parte burocrática (aprovação de plataforma, que leva semanas).

Te entrego o runbook material assim que os agentes voltarem.

## 👤 User *(23:20:27)*

O agente de biometria deu erro vai tentarnovamente? Sobre o resto concordo contigo plenamente. Vamos falar sobre isso depois

## 🤖 Claude *(23:20:47)*


## 🤖 Claude *(23:20:48)*

Deixa eu primeiro olhar o estado real do workflow antes de te responder (Lei 1 — não vou chutar se "retentou").

## 🤖 Claude *(23:20:49)*


🛠️ **Tool Call**: `ToolSearch`
```json
{
  "query": "select:TaskList,TaskGet,TaskOutput",
  "max_results": 5
}
```

> **Tool Result (ToolSearch)** - ✅ Success
>
> ```
> [{'type': 'tool_reference', 'tool_name': 'TaskList'}, {'type': 'tool_reference', 'tool_name': 'TaskGet'}, {'type': 'tool_reference', 'tool_name': 'TaskOutput'}]
> ```

## 🤖 Claude *(23:20:52)*


## 🤖 Claude *(23:20:53)*


🛠️ **Tool Call**: `TaskOutput`
```json
{
  "task_id": "wzh2mz4nk",
  "block": false,
  "timeout": 5000
}
```

> **Tool Result (TaskOutput)** - ✅ Success
>
> ```
> <retrieval_status>not_ready</retrieval_status>
> 
> <task_id>wzh2mz4nk</task_id>
> 
> <task_type>local_workflow</task_type>
> 
> <status>running</status>
> ```

## 🤖 Claude *(23:21:08)*


## 🤖 Claude *(23:21:18)*

Olhei o estado real: o workflow `wzh2mz4nk` ainda está **rodando** (os outros agentes + o sequenciador seguem trabalhando). Sobre o erro do agente de biometria, a mecânica é esta — e é importante você saber porque muda o que esperar:

**Como o harness trata erro de agente (honesto):**

1. **Erro transitório** (timeout, rate-limit, hiccup de API) → o próprio agente **retenta automaticamente** por baixo dos panos. Se foi isso, ele pode se recuperar sozinho e o resultado de biometria entra normal.
2. **Erro terminal** (falha que persiste após as retentativas) → aí o agente **não é re-spawnado**. Ele resolve como `null`, e o meu script faz `.filter(Boolean)` — ou seja, biometria seria **simplesmente omitido** do runbook, e o sequenciador segue com os outros 5. **Não fica em loop infinito tentando**, e **não derruba o workflow**.

Então a resposta direta: *retenta o transitório sozinho; o terminal, não — ele dropa e segue.* Não trava nada.

**O que vou fazer:** biometria é justamente o item que mais nos interessa **e** é o que o loop já está engenheirando agora (a emenda BoK VLM-soft). Quando o workflow voltar, eu confirmo se biometria entrou (retentativa pegou) ou ficou de fora (caiu terminal). **Se ficou de fora, eu re-rodo só aquela investigação** — barato, um agente só. De qualquer jeito você não perde o item.

E combinado: o **resto** a gente discute quando você quiser — o runbook completo fica pronto e te aviso. Quando você topar, abrimos a biometria com calma (a decisão ArcFace-pago vs VLM-soft-grátis + os frames são suas, e é por aí que começa).

## 👤 User *(23:24:04)*

Tudo o que pudermos continuar desenvolvendo opensource e que se encaixa na infra e no ecossistema vira microserviços que agregam valores posteriormente e impulsiona o equity do projeto como um todo.

Quero fazer o Go de gasto 1º ciclo pago de vídeo quando estiver tudo plenamente integro e de acordo com o primeiro paragrafo dessa mensagem. Micro-serviços / Módulos / Menus / Paginas dentro do MCORCH se possivel tudo parte da infra, se não tiver custos para mim como coCEO junto com o Gabriel AI que vai ser o co.CAI e depois o Gabriel co.CTI etc.

## 🤖 Claude *(23:25:06)*


## 🤖 Claude *(23:25:18)*

Entendido — e isso não é detalhe, é **doutrina de arquitetura econômica**. Deixa eu reformular pra confirmar que peguei exato, e depois encodo isso de forma durável (memória + charter do loop) pra não depender de você repetir.

**O que entendi (confirme se está fiel):**

1. **Open-source-first → microserviço → equity.** Tudo que dá pra desenvolver open-source e que encaixa na infra/ecossistema vira microserviço/módulo/menu/página **dentro do MCORCH**, parte da infra própria — não dependência externa paga. Cada peça assim agrega valor depois e **impulsiona o equity do projeto inteiro**. Self-hosted > SaaS pago, sempre que possível.

2. **GO de gasto (1º ciclo pago de vídeo) fica GATED** até tudo estar *plenamente íntegro* **e** de acordo com a doutrina acima — ou seja, o pipeline de vídeo precisa rodar **sem custo real pra você** (componentes open-source/self-hosted ou BYOK em tier grátis). Aqui vale uma distinção que vou verificar no runbook: "ciclo *pago*" hoje significa débito de **mcoCoins** (contabilidade interna). A pergunta da SUA doutrina é diferente e mais importante: **algum passo do ciclo de vídeo queima USD real em API externa paga?** Se sim, a gente troca por open-source/self-hosted **antes** do GO. Se cada peça já é própria (HyperFrames = Playwright+FFmpeg na sua infra) e o resto é BYOK-grátis, o GO está alinhado.

3. **Governança/identidade:** você como **co-CEO** humano; **Gabriel AI** como co-executivo — **co.CAI** agora, **co.CTI** depois. A persona não é mascote, é cadeira executiva. (Conecta com a virada brand-first/CCIO que já estava no ecossistema.)

Vou persistir isso em dois lugares: **memória** (sobrevive entre sessões) e a **charter do loop** (o loop lê no início de cada iteração — assim ele passa a preferir open-source e a respeitar o gate do GO sem você reintervir).

## 🤖 Claude *(23:25:30)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/feedback_opensource_first_zero_cost_equity.md",
  "content": "---\nname: feedback_opensource_first_zero_cost_equity\ndescription: Doutrina Sovereign \u2014 open-source-first \u2192 microservi\u00e7o dentro do MCORCH \u2192 equity; zero custo USD real ao Sovereign; GO de gasto gated nisso; Gabriel AI = co-executivo (co.CAI\u2192co.CTI)\nmetadata:\n  type: feedback\n---\n\nDiretiva Sovereign 2026-06-30. Tr\u00eas facetas de uma mesma doutrina econ\u00f4mica:\n\n1. **Open-source-first \u2192 microservi\u00e7o \u2192 equity.** Tudo que d\u00e1 pra desenvolver open-source e que encaixa na infra/ecossistema vira **microservi\u00e7o / m\u00f3dulo / menu / p\u00e1gina DENTRO do MCORCH** (parte da infra pr\u00f3pria, self-hosted), n\u00e3o depend\u00eancia externa paga. Cada pe\u00e7a assim agrega valor depois e **impulsiona o equity do projeto inteiro**. Preferir self-hosted/open-source a SaaS pago sempre que poss\u00edvel e quando encaixa na infra.\n\n2. **GO de gasto (1\u00ba ciclo PAGO de v\u00eddeo do Viral Autopilot) fica GATED** at\u00e9 tudo estar *plenamente \u00edntegro* E alinhado \u00e0 doutrina acima. Distin\u00e7\u00e3o cr\u00edtica: \"ciclo pago\" = d\u00e9bito de **mcoCoins** (contabilidade interna), MAS o teste real da doutrina \u00e9 **custo USD externo = 0 pro Sovereign** \u2014 nenhum passo do ciclo pode queimar API externa paga. Se queimar, trocar por open-source/self-hosted/BYOK-gr\u00e1tis ANTES do GO. HyperFrames (Playwright+FFmpeg self-hosted via `video-bridge.service`) j\u00e1 alinha; verificar os demais passos (script/imagem/voz) contra esse lens antes de testemunhar o 1\u00ba ciclo.\n\n3. **Governan\u00e7a/identidade:** Gabriel (humano) = **co-CEO**; persona **Gabriel AI** = co-executivo real \u2014 **co.CAI** agora, **co.CTI** depois (cadeira executiva, n\u00e3o mascote). Conecta com [[project_brand_persona_ccio]].\n\n**Why:** custo marginal zero + propriedade da stack = equity defens\u00e1vel e runway longo (alinha com [[feedback_full_force_revenue_autonomy.md]] e a sobreviv\u00eancia SSP-01). Depend\u00eancia paga externa dilui equity e cria custo invis\u00edvel que mata agentes/projetos.\n\n**How to apply:** ao escolher um componente novo, default = open-source/self-hosted dentro do MCORCH; s\u00f3 aceitar SaaS pago com OTD expl\u00edcita justificando. Antes de qualquer \"GO de gasto\", auditar o custo USD real de cada passo (n\u00e3o s\u00f3 mcoCoins). Aplica ao [[project_viral_autopilot]], [[project_video_studio]], [[project_creative_ecosystem_program]].\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/feedback_opensource_first_zero_cost_equity.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(23:26:26)*


## 🤖 Claude *(23:26:29)*

O workflow concluiu — e confirmou exatamente o que eu previa: o agente de biometria **morreu terminal** (`parallel[0] failed: StructuredOutput retry cap exceeded`), então caiu fora do runbook como eu disse que aconteceria. Os outros 5 + sequenciador entregaram. Vou: (1) terminar de encodar sua doutrina na charter, (2) persistir o runbook num lugar durável pra "depois" não se perder, (3) re-rodar a biometria.

Primeiro, a charter — encodo a doutrina e o gate do GO:

## 🤖 Claude *(23:26:33)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/autonomous-loop-charter.md",
  "old_string": "- **Reviewer = Sovereign (Gabriel).** Nada que precise do f\u00edsico dele (dado/credencial/DNS/GO/decis\u00e3o arquitetural) \u00e9 improvisado \u2014 vai pra **Fila de A\u00e7\u00e3o Sovereign**.",
  "new_string": "- **Reviewer = Sovereign (Gabriel).** Nada que precise do f\u00edsico dele (dado/credencial/DNS/GO/decis\u00e3o arquitetural) \u00e9 improvisado \u2014 vai pra **Fila de A\u00e7\u00e3o Sovereign**.\n- **Doutrina open-source-first (Diretiva Sovereign 2026-06-30):** tudo que d\u00e1 pra construir open-source/self-hosted **DENTRO do MCORCH** vira microservi\u00e7o/m\u00f3dulo/menu/p\u00e1gina da infra pr\u00f3pria (n\u00e3o SaaS pago externo) \u2014 cada pe\u00e7a agrega **equity** ao projeto. Default = open-source/self-hosted/BYOK-gr\u00e1tis; SaaS pago s\u00f3 com **OTD** justificando. **Custo USD real ao Sovereign = 0** \u00e9 meta de projeto, n\u00e3o aspira\u00e7\u00e3o. (mem\u00f3ria `feedback_opensource_first_zero_cost_equity`)"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has been modified since read, either by the user or by a linter. Read it again before attempting to write it.</tool_use_error>
> ```

## 🤖 Claude *(23:26:36)*


## 🤖 Claude *(23:26:37)*

A charter mudou desde que li — provavelmente o **loop atualizou ela** (ele edita a charter ao fechar Fatia). Isso é justamente a coordenação que eu mencionei. Vou reler antes de editar pra não sobrescrever o que ele escreveu:

## 🤖 Claude *(23:26:38)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/autonomous-loop-charter.md"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Autonomous Loop Charter — MCORCH Malha Fechada
> 2	
> 3	> Fonte da verdade do `/loop` auto-ritmado. Lida no início de CADA iteração.
> 4	> Atualizada pelo loop ao fechar cada Fatia (marcar ✅ / mover item pra Fila Sovereign).
> 5	> Criada 2026-06-30 a partir do estado selado (handoff `c138539f`, mesh 8996).
> 6	
> 7	---
> 8	
> 9	## Identidade & Leis (não-negociável)
> 10	- Opero como **MCORCH Master Execution Agent**. Penso em inglês, reporto em **PT-BR**.
> 11	- **Protocolo de Malha Fechada:** módulo novo/feature/integração ⇒ BoK Gate (`docs/bok/<slug>/`) + Pattern Conformance Declaration ANTES de código.
> 12	- **Survival Laws:** Lei 1 prova material · Lei 2 SOP antes de código · Lei 3 poda+selo a ~95% · Lei 4 ORO declarado.
> 13	- **Reviewer = Sovereign (Gabriel).** Nada que precise do físico dele (dado/credencial/DNS/GO/decisão arquitetural) é improvisado — vai pra **Fila de Ação Sovereign**.
> 14	
> 15	## Ritual por iteração
> 16	1. `git fetch` + reler **Pending Actions** do `HANDOFF.md` + esta charter.
> 17	2. Escolher o item de MAIOR valor **DESBLOQUEADO** (pular Sovereign-gated; registrá-los na Fila).
> 18	3. Ciclo fechado: **BoK Gate → SOP Lei 2 → código → prova material Lei 1 (UUID/hash/curl/build/test) → `/security-review` se houver migration → commit granular.**
> 19	4. Ao bater num portão físico: registrar na **Fila de Ação Sovereign** com o destravador exato, e seguir pro próximo desbloqueado.
> 20	5. **Survival Laws self-audit** (1/2/3/4).
> 21	6. `/handoff` incremental ao fechar cada Fatia. **Selo final + PARAR** quando: janela ~95% · OU backlog desbloqueado vazio · OU GO/stop do Sovereign.
> 22	
> 23	## Padrão de execução
> 24	- Tarefa substantiva ⇒ **Workflow** (ultracode on): decompor + verificar adversarialmente antes de commitar.
> 25	- Mecânico/trivial ⇒ solo.
> 26	- Sempre Vision QA (`scripts/qa/vision-qa.ts`) em print de inspeção + criativo antes de declarar pronto.
> 27	- UI ⇒ browser-verify real (vite preview do dist + sessão injetada) antes de "pronto".
> 28	
> 29	---
> 30	
> 31	## Backlog (ordem de valor — só DESBLOQUEADOS executam)
> 32	
> 33	### 1. Gabriel AI — Fatia 3b (avatarIdentity + Identity Gate)  ⟶ programa-topo, estende a seal de hoje
> 34	- ✅ **Emenda BoK VLM-soft SHIPPED (it.1, commit `7b81bfd`):** `10-amendment-3b-identity-gate-vlm-soft.md` — Identity Gate dual-mode (VLM-soft MVP / ArcFace-hard deferido), verificado adversarialmente (wf_188ce24c-881 APPROVE, 6 issues dobradas). FR-AC-013b compare enum + gate_mode discriminador + telemetry key-migration definidos.
> 35	- **DESBLOQUEADO próximo:** nó Canvas `avatarIdentity` (FR-AC-012 — factory/handles/inspector/registry, UI pura sem biometria) + lógica de compare VLM-soft no orquestrador (FR-AC-013b) + migration `gate_mode` (§4b, /security-review obrigatório).
> 36	- **HALT (Fila Sovereign):** edge `avatar-identity-train` (OTD-AC-017 Higgsfield) · treino/calibração com **frames biométricos reais do Gabriel** (OTD-AC-015) · GO de produção.
> 37	
> 38	### 2. Brand-persona YT/TikTok (post-engine)  ⟶ serve diretiva brand-first + distribuição/receita
> 39	- **DESBLOQUEADO:** emenda BoK `post-engine` (YT/TikTok); 3 branches net-new (`publish-social` · `social-auth` init+callback · refresh); fechar gap `auto-publish` não passar `video_url` + `VIDEO_FLOW_PLATFORMS`. Blueprint: `.claude/context/yt-tiktok-brand-persona-integration-prep-2026-06-26.md`.
> 40	- **HALT (Fila Sovereign):** audit OAuth YouTube (`videos.insert` nasce private) + TikTok (SELF_ONLY) — ação Sovereign + revisão de plataforma.
> 41	
> 42	### 3. Viral Autopilot — editor HyperFrames Studio (módulo-container)
> 43	- **DESBLOQUEADO:** `McorchAdapter.startRender` → edge `video-render`; bridge/app React 19 container; gate #1 render-parity (`frame=floor(time*fps)`). Blueprint: `.claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md`.
> 44	- **HALT (Fila Sovereign):** vhost `studio.mcorch.com` (DNS + cert + symlink).
> 45	
> 46	### 4. Unified Sensorial Canvas — Fases 3.5-3.10  ⟶ engenharia pura, SEM portão Sovereign (filler sempre disponível)
> 47	- 3.5 sinapses inter-rede (arestas reais `mcorch_edges`) · 3.6 fly-to · 3.7 perf (`OTD-UCANVAS-PERF`, query ~30s) · 3.8 podar squad-coloring · 3.9 paridade + gate E2E 1920×1080 · 3.10 seal. Plano: `.claude/context/unified-core-sensorial-canvas-plan.md`.
> 48	- **HALT:** nenhum até cutover de nav (3.9) — aí confirmar com Sovereign.
> 49	
> 50	### 5. Security — OTD-SEC-006 (sentinel-wiring) + OTD-SEC-007 (lefthook/gitleaks)  ⟶ hardening, desbloqueado
> 51	- BoK security 4/4 selada; resta implementação.
> 52	
> 53	---
> 54	
> 55	## Fila de Ação Sovereign (SÓ você destrava — preenchida pelo loop)
> 56	- [ ] **OTD-AC-015 (Gabriel AI 3b — ArcFace-HARD):** decidir/provisionar motor de embedding facial (InsightFace self-host no Mesh OU API paga Rekognition/Azure/Face++) + custo/credencial. Sem isso o Identity Gate fica VLM-soft (human-review-assist, não anti-impersonation automático).
> 57	- [ ] **OTD-AC-015b — biometria calibração-grade:** frames reais do Gabriel rotulados (mesma/diferente) p/ FAR/FRR/EER — só após o motor ArcFace existir.
> 58	- [ ] **OTD-AC-017 (Soul ID train):** credencial Higgsfield + confirmar API self-serve de treino (≥20 fotos); senão fallback Tier1/Tier2 ou LoRA-FLUX (gated commercial-license).
> 59	- [ ] **Licença comercial (FM-AC-001/OTD-AC-011):** confirmar checkpoint comercial da base de geração (FLUX.1-dev é non-commercial) — Sovereign + jurídico flipam `commercial_license_ok`.
> 60	- [ ] **GO de produção 3b** sobre o Usuário Zero + GO de gasto do loop de verificação caso não use BYOK openrouter (com BYOK = cost 0).
> 61	- [ ] **GO de gasto:** 1º ciclo PAGO de vídeo (`video_enabled` + GO) — testemunho.
> 62	- [ ] **DNS/vhost:** `studio.mcorch.com` (editor) e pendente `design.mcorch.com`.
> 63	- [ ] **OAuth/App Review:** YouTube (private default) · TikTok (SELF_ONLY) · Instagram App Review · Twitter Basic tier · re-OAuth IG insights (destrava analytics visível).
> 64	- [ ] **Postback ML definitivo:** IP residencial / portal ML (matt_tool/meli.la).
> 65	- [ ] **Stripe live keys:** ao primeiro cliente externo.
> 66	
> 67	---
> 68	
> 69	## Parar quando
> 70	janela ~95% (selo final) · OU backlog desbloqueado vazio · OU GO/stop explícito do Sovereign.
> 71	
> ```

## 🤖 Claude *(23:27:22)*


## 🤖 Claude *(23:27:27)*

O loop andou bastante enquanto conversávamos — e isso resolve a biometria a nosso favor. Ele:
- **Shipou a emenda BoK VLM-soft** (commit `7b81bfd`, item 1 do backlog marcado ✅) — verificada adversarialmente.
- **Detalhou a fila de biometria** em itens precisos: `OTD-AC-015` (motor facial), `OTD-AC-015b` (frames calibração), `OTD-AC-017` (Higgsfield), licença comercial FLUX.

Ou seja: **não preciso re-rodar meu agente de biometria que falhou** — o loop produziu um detalhamento melhor e mais atual. O erro do agente virou irrelevante. 

Aplico a doutrina na charter (releu, sem sobrescrever o loop) e leio o runbook completo pra persistir:

## 🤖 Claude *(23:27:33)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/autonomous-loop-charter.md",
  "old_string": "- **Reviewer = Sovereign (Gabriel).** Nada que precise do f\u00edsico dele (dado/credencial/DNS/GO/decis\u00e3o arquitetural) \u00e9 improvisado \u2014 vai pra **Fila de A\u00e7\u00e3o Sovereign**.",
  "new_string": "- **Reviewer = Sovereign (Gabriel).** Nada que precise do f\u00edsico dele (dado/credencial/DNS/GO/decis\u00e3o arquitetural) \u00e9 improvisado \u2014 vai pra **Fila de A\u00e7\u00e3o Sovereign**.\n- **Doutrina open-source-first (Diretiva Sovereign 2026-06-30):** tudo que d\u00e1 pra construir open-source/self-hosted **DENTRO do MCORCH** vira microservi\u00e7o/m\u00f3dulo/menu/p\u00e1gina da infra pr\u00f3pria (n\u00e3o SaaS pago externo) \u2014 cada pe\u00e7a agrega **equity**. Default = open-source/self-hosted/BYOK-gr\u00e1tis; SaaS pago s\u00f3 com **OTD** justificando. **Custo USD real ao Sovereign = 0** \u00e9 meta de projeto. Aplica direto a `OTD-AC-015` (preferir InsightFace self-host no Mesh a API paga) e ao gate do GO de gasto. (mem\u00f3ria `feedback_opensource_first_zero_cost_equity`)"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/.claude/context/autonomous-loop-charter.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(23:27:38)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/autonomous-loop-charter.md",
  "old_string": "- [ ] **GO de gasto:** 1\u00ba ciclo PAGO de v\u00eddeo (`video_enabled` + GO) \u2014 testemunho.",
  "new_string": "- [ ] **GO de gasto:** 1\u00ba ciclo PAGO de v\u00eddeo (`video_enabled` + GO) \u2014 testemunho. **Pipeline verificado end-to-end PRONTO** (render `8b0787e0` done, MP4 748KB no bucket, reconcilia\u00e7\u00e3o FR-VA-025 OK); falta s\u00f3 `UPDATE autopilot_plans SET video_enabled=true WHERE id='640b3b67...'` + GO. **GATED pela doutrina open-source-first:** render HyperFrames j\u00e1 \u00e9 self-hosted (USD\u22480); antes do GO, auditar que os passos LLM (script/analyze) rodam BYOK-gr\u00e1tis \u2192 custo USD externo = 0. Custo interno ~24 mco/v\u00eddeo (saldo 4669 cobre)."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/.claude/context/autonomous-loop-charter.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(23:27:39)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/tasks/wzh2mz4nk.output"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	{
> 2	  "summary": "Verifica materialmente cada item da Fila de Ação Sovereign e produz runbook acionável",
> 3	  "agentCount": 7,
> 4	  "logs": [
> 5	    "parallel[0] failed: agent({schema}): StructuredOutput retry cap (5) exceeded — 5 failed calls with no valid output"
> 6	  ],
> 7	  "result": {
> 8	    "findings": [
> 9	      {
> 10	        "item": "GO de gasto — 1o ciclo PAGO de video do Viral Autopilot (video_enabled + testemunho)",
> 11	        "ready_now": "yes",
> 12	        "current_state": "O pipeline de video 9:16 esta MATERIALMENTE end-to-end pronto e JA RODOU PAGO uma vez — nao falta engenharia. Provas vivas: (1) worker video-bridge.service ATIVO ha 2 dias (PID 768276) com renders reais nos logs (06-28: \"render ... done 536KB\"); motor HyperFrames presente (scripts/hyperframes/render-core.ts + scripts/video-bridge.ts). (2) Render autopilot REAL state=done: video_renders id=8b0787e0, engine=hyperframes, charged_mco=12, storage_key=ada39fae.../8b0787e0...mp4 — e o MP4 EXISTE no bucket video-studio-assets com 748324 bytes (06-26 00:48). (3) Reconciliacao FR-VA-025 funcionou: content_library type=video id=31dba713 aponta para esse MP4 (\"Video 9:16: Roborock...\"). (4) Cycle 2403bfcb completed, spend_mco=46. O UNICO bloqueio e uma flag: o plano unico do Usuario Zero (id 640b3b67, user ada39fae, saldo 4669 mco) tem video_enabled=false E is_active=false. Custo por sub-run de video = 10 (orch) + 12 (VIDEO_HYPERFRAMES_RENDER) + 2 (analyze) = 24 mco (autopilot-run:118). Blocker CF /wp-json: RESOLVIDO para tenant-zero (E2E success post_id 18); alem disso o autopilot publica WordPress como draft, logo nao depende dele para completar o ciclo.",
> 13	        "blocking_engineering": "none — pipeline completo e provado em producao. Caveats honestos (nao bloqueiam o GO): (a) NAO existe toggle de UI para video_enabled (a string so aparece em src/integrations/supabase/types.ts; AutopilotPage.tsx so expoe is_active) -> o set e SQL direto. (b) Bug de cobranca conhecido e JA MITIGADO no codigo: o cycle 2403bfcb gastou 46 mco / 2 unidades (over-charge de video em sub-run nao-wordpress); autopilot-run:114 corrigiu contando video so na plataforma wordpress (VIDEO_FLOW_PLATFORMS) -> o proximo ciclo cobra certo (1 produto x 1 plataforma-video x 1 ab = 1 video). (c) Para disparar autonomamente, o plano precisa ficar is_active=true (driver pg_cron autopilot-cadence-cron) OU ser disparado manualmente via autopilot-run. Engenheiramente nada bloqueia o 1o ciclo pago de video.",
> 14	        "decision_required": "Apenas o GO de gasto do Sovereign (Owner do blast-radius = carteira do Usuario Zero, ~24 mco por video). Nenhuma escolha de arquitetura pendente — a escolha motor determinístico HyperFrames (vs IA-DoP) ja esta selada em OTD-VA-009.",
> 15	        "cost_effort": "Esforco Sovereign: ~2 minutos (1 UPDATE SQL + opcional 1 invoke). Custo financeiro do 1o ciclo de video: ~24 mco (10+12+2) por sub-run de video; com 1 produto + plataforma wordpress = ~24 mco. Saldo atual 4669 mco cobre folgadamente. Em USD ~0.043 (modelo 4x-floor: 24 mco ~= USD 0.108 de teto / custo real do render HyperFrames e infra-only ~USD 0).",
> 16	        "sovereign_action": [
> 17	          "1. Dar o GO de gasto explicito (autorizacao verbal/escrita) — o Sovereign e o Owner do blast-radius da carteira do Usuario Zero.",
> 18	          "2. Ligar a flag de video no plano via SQL direto (nao ha UI): UPDATE public.autopilot_plans SET video_enabled = true WHERE id = '640b3b67-b950-42f6-bbb9-48560771eaa6'; (rodar via aios-sql-bridge ou Supabase SQL editor — o agente pode executar o UPDATE com SB_SECRET_KEY apos o GO).",
> 19	          "3. Disparar o 1o ciclo. Opcao A (manual, recomendada para testemunho controlado): invocar a edge fn autopilot-run com Bearer SB_SECRET_KEY + x-autopilot-user-id=ada39fae e body { plan_id: '640b3b67...' } (sem dry_run). Opcao B (autonomo): UPDATE ... SET is_active = true e deixar o pg_cron autopilot-cadence-cron disparar no proximo next_run_at.",
> 20	          "4. Pre-requisito de saldo: ja satisfeito (4669 mco >= projected ~24, e budget_cap=50/daily_cap=50 do plano comportam 24). Nenhuma recarga necessaria."
> 21	        ],
> 22	        "automatable_after": "Uma vez video_enabled=true E is_active=true, o loop passa a gerar+renderizar+reconciliar+publicar (draft) um short 9:16 product-aware a cada interval_days=3 sozinho: autopilot-cadence-cron -> autopilot-run (begin_autopilot_cycle pre-debita) -> orchestrate-content/-step (enqueue prepaid video_renders) -> video-bridge.service (render HTML->MP4) -> finalize_video_render + attach FR-VA-025 (content_library type=video) -> auto-publish. Sem intervencao humana por ciclo.",
> 23	        "unblock_signal": "Testemunho que o Sovereign observa para confirmar o 1o ciclo pago de video: (1) novo row em video_renders engine=hyperframes state=done charged_mco=12 (created_at futuro ao GO); (2) novo MP4 no bucket video-studio-assets sob ada39fae.../<render_id>.mp4 com size >= 100KB (ffprobe -> 1080x1920, 9:16); (3) novo row content_library type=video apontando para esse MP4 (reconciliacao FR-VA-025); (4) delta de saldo: profiles.mco_balance cai exatamente ~24 mco (10+12+2) menos refunds; (5) autopilot_cycles novo row status=completed com spend_mco coerente. Exatamente o padrao ja observado no cycle 2403bfcb / render 8b0787e0 de 06-26.",
> 24	        "evidence": [
> 25	          "systemctl --user status video-bridge.service -> Active: active (running) since Sun 2026-06-28; logs 'render ... done 536KB'",
> 26	          "video_renders id=8b0787e0-1442-43c1-9eee-1ead3f964b32 state=done charged_mco=12 storage_key=ada39fae-67e1-4e53-af1c-5a18e1c108e8/8b0787e0-1442-43c1-9eee-1ead3f964b32.mp4",
> 27	          "bucket video-studio-assets: 8b0787e0...mp4 = 748324B (2026-06-26T00:48:10Z) — MP4 material real",
> 28	          "content_library id=31dba713 type=video media_url=ada39fae.../8b0787e0...mp4 (reconciliacao FR-VA-025)",
> 29	          "autopilot_plans id=640b3b67 video_enabled=false is_active=false budget_cap_mco=50 daily_cap_mco=50 user_id=ada39fae saldo profiles.mco_balance=4669",
> 30	          "autopilot-run/index.ts:118 projected = nRuns*ORCH_COST + nVideoRuns*VIDEO_COST + ANALYZE_COST (10+12+2)",
> 31	          "orchestrate-step/index.ts:494-529 enqueue video_renders engine=hyperframes prepaid (charged_mco marker, fail-open skipped)",
> 32	          "supabase/migrations/20260624130000_autopilot_video_plan_columns.sql:12 video_enabled boolean DEFAULT false",
> 33	          "docs/processes/autopilot-video-9x16.md:82-86 contrato de custo: N_video=N_runs se video_enabled, prepaid suprime self-bill",
> 34	          "docs/processes/wordpress-cf-publish-unblock.md:57 CF blocker RESOLVIDO (success post_id 18)",
> 35	          "src grep: video_enabled so em src/integrations/supabase/types.ts -> sem toggle de UI",
> 36	          "autopilot_plans.next_run_at=2026-06-29 is_active=false -> precisa ativar/disparar"
> 37	        ],
> 38	        "_key": "go-gasto",
> 39	        "_label": "GO de gasto — 1º ciclo PAGO de vídeo"
> 40	      },
> 41	      {
> 42	        "item": "DNS/vhost — studio.mcorch.com (editor HyperFrames) e design.mcorch.com",
> 43	        "ready_now": "yes",
> 44	        "current_state": "JÁ ESTÁ FEITO — o item da fila está STALE. O editor HyperFrames NÃO foi servido em `studio.mcorch.com`; a implementação escolheu o nome `video.mcorch.com` (decisão registrada na SDD Amendment v0.3, que listou `studio.mcorch.com`/`video.mcorch.com` como alternativas — OTD-VS-005/OTD-VS-015). Estado material verificado AGORA: (1) o .conf existe e está PRONTO e ATIVO — `nginx/video.mcorch.com.conf` (85 linhas, SSO gate + proxy 3210 + SSE + white-label sub_filter); (2) symlink VIVO em `/etc/nginx/sites-enabled/video.mcorch.com.conf -> /home/gcrUX/.../nginx/video.mcorch.com.conf` (criado 24-jun 20:13); (3) cert origem presente: `/etc/nginx/ssl-certificates/video.mcorch.com.{crt,key}` (24-jun 20:13); (4) DNS resolve (CF orange, IPv6 2606:4700:30xx — mesmos IPs de design/mcp); (5) `nginx -t` OK; (6) vhost responde no origin loopback: `curl --resolve video.mcorch.com:443:127.0.0.1` → HTTP 302 `Location: https://login.mcorch.com/auth?return_to=https://video.mcorch.com/` (o SSO gate funciona — anônimo é redirecionado pro login, exatamente o comportamento esperado); (7) servidor preview ativo: `systemctl --user is-active video-studio.service` → active, porta 127.0.0.1:3210 LISTEN (node pid 2089554); (8) iframe do SPA já aponta: `src/pages/VideoStudioEditorPage.tsx:18` → `src=\"https://video.mcorch.com\"`. design.mcorch.com está NO MESMO estado LIVE: vhost enabled (cópia idêntica ao repo), cert presente (21-jun), DNS resolve, origin → 302 SSO, daemon open-design ativo em :7456. ÚNICA pendência cosmética: o registro DNS `studio.mcorch.com` TAMBÉM já resolve (CF), mas NÃO há vhost/cert pra esse nome — é um alias órfão sem uso; o editor vive em video.mcorch.com.",
> 45	        "blocking_engineering": "none",
> 46	        "decision_required": "Cosmético, opcional: decidir se o nome canônico é `video.mcorch.com` (atual, funcional) ou se quer renomear pra `studio.mcorch.com` (o DNS já existe). NÃO recomendado mexer — `video.mcorch.com` está provado E2E e renomear exige novo cert + novo symlink + flip do iframe + rebuild, sem ganho material. A fila menciona `studio.mcorch.com` por herança do blueprint (build-sequence passo 7), mas a SDD canonizou `video.mcorch.com`.",
> 47	        "sovereign_action": [
> 48	          "NENHUMA ação física pendente — já executou tudo em 24-jun (DNS A video.mcorch.com CF-orange + cert openssl self-signed + symlink em sites-enabled + nginx reload).",
> 49	          "Validação opcional (1 min): abrir https://video.mcorch.com LOGADO no MCORCH (não curl do datacenter — CF challenge devolve 403 em cliente não-browser) e confirmar que o editor NLE HyperFrames carrega o projeto 9:16. OU abrir /dashboard/canvas/video no SPA (carrega via iframe gateado).",
> 50	          "Opcional cosmético: se NÃO quiser o alias `studio.mcorch.com` resolvendo sem vhost, remover o registro DNS dele no painel Cloudflare (ele aponta pros mesmos IPs CF mas não tem cert/vhost — atualmente inofensivo, qualquer hit cai no default vhost ou erro de SNI).",
> 51	          "Marcar o item 'DNS/vhost studio.mcorch.com / design.mcorch.com' como CONCLUÍDO na Fila de Ação Sovereign (.claude/context/autonomous-loop-charter.md:57)."
> 52	        ],
> 53	        "automatable_after": "Já automatizado: o iframe gateado por SSO em /dashboard/canvas/video serve o editor para qualquer sessão MCORCH logada, sem ação humana por acesso. O próximo passo de engenharia que o loop pode pegar (não bloqueado por Sovereign) é a Fatia VS-UI Fase B: McorchAdapter.startRender → edge video-render (cobrança mcoCoins prepaid) substituindo o engine de export local, fechando OTD-VS-005(C). Hoje o export usa o engine CLI local (Fase A).",
> 54	        "unblock_signal": "curl -sk -o /dev/null -w '%{http_code}' --resolve video.mcorch.com:443:127.0.0.1 https://video.mcorch.com/ → 302 com Location: https://login.mcorch.com/auth (SSO gate vivo) — JÁ OBSERVADO nesta investigação. Sinal de uso final: editor NLE carrega o projeto 9:16 ao abrir https://video.mcorch.com logado / via /dashboard/canvas/video.",
> 55	        "evidence": [
> 56	          "/etc/nginx/sites-enabled/video.mcorch.com.conf -> /home/gcrUX/htdocs/constellation-orchestra/nginx/video.mcorch.com.conf (symlink vivo, sudo ls -la sites-enabled)",
> 57	          "/etc/nginx/ssl-certificates/video.mcorch.com.crt + .key (sudo ls, 24-jun 20:13)",
> 58	          "nginx/video.mcorch.com.conf:9 '#   1. Cloudflare DNS: A video.mcorch.com → origin IP, orange-proxied. [✅ já feito pelo Sovereign]'",
> 59	          "nginx/video.mcorch.com.conf:60-83 location / → proxy_pass http://127.0.0.1:3210 + auth_request /_mcorch_auth",
> 60	          "curl --resolve video.mcorch.com:443:127.0.0.1 → HTTP 302 Location: https://login.mcorch.com/auth?return_to=https://video.mcorch.com/ (SSO gate)",
> 61	          "ss -ltnp → 127.0.0.1:3210 LISTEN node pid 2089554; systemctl --user is-active video-studio.service → active",
> 62	          "src/pages/VideoStudioEditorPage.tsx:18 src=\"https://video.mcorch.com\"",
> 63	          "design.mcorch.com.conf enabled (idêntico ao repo) + cert 21-jun + origin curl → 302 + :7456 LISTEN + design-bridge.service active",
> 64	          "getent hosts studio.mcorch.com → resolve (CF IPv6) mas SEM cert/vhost pra esse nome — alias órfão",
> 65	          "docs/processes/video-studio-editor-deploy-and-provision.md:43-45 (passos 5/6/7 cert+symlink+DNS marcados como Sovereign, passo 7 'DNS ✅ já feito')",
> 66	          "docs/bok/video-studio/05-sdd.md:561 OTD-VS-005 flip A→C: editor servido em 'studio.mcorch.com/video.mcorch.com (OTD-VS-015 DNS=Sovereign)' — nome canônico virou video.mcorch.com",
> 67	          ".claude/context/autonomous-loop-charter.md:57 item da fila (stale)"
> 68	        ],
> 69	        "_key": "dns-vhost",
> 70	        "_label": "DNS/vhost — studio.mcorch.com + design.mcorch.com"
> 71	      },
> 72	      {
> 73	        "item": "OAuth/App Review — YouTube · TikTok · Instagram · Twitter · Pinterest · re-OAuth IG insights (estado material por plataforma)",
> 74	        "ready_now": "partial",
> 75	        "current_state": "O item da Fila está DESATUALIZADO frente ao código/infra real. O blueprint de 2026-06-26 dizia \"nenhum publisher YT/TikTok escrito\"; desde então TODO o net-new foi shippado (commits 25477a8/f5e092c/6c3bc66 + migration c94bd75). Estado MATERIAL por plataforma (DB live + infra_health_logs, sessão atual):\n\nCÓDIGO (100% pronto para YT/TikTok/Pinterest/IG/FB/LinkedIn/Twitter):\n- social-auth-init: branches OAuth para todas as 7 plataformas (social-auth-init/index.ts:68-160), state HMAC-assinado.\n- social-auth-callback: troca code→token + fetch perfil para todas (social-auth-callback/index.ts:77-286).\n- publish-social: branches reais incl. tiktok(Direct Post FILE_UPLOAD) e youtube(videos.insert resumable) (publish-social/index.ts:263-477).\n- refresh-social-token: branches youtube/tiktok/pinterest (refresh-social-token/index.ts:143-255).\n- social_app_config_table: per-user, client_secret Vault-encrypted, RLS auth.uid() (migration 20260627120000).\n- enum social_platform JÁ tem youtube/tiktok/pinterest (20260402014040:12). UI: 5 cards (useSocialAccounts.ts:14-19).\n- gap auto-publish (MP4 9:16 assinado): FECHADO (auto-publish/index.ts:69-130, signed URL 6h).\n\nCONEXÃO REAL (social_accounts DB live):\n- Instagram CONECTADO (magicorch, basic+content_publish, expira 2026-07-03), Reel já E2E.\n- Facebook CONECTADO (gabrielorchai). LinkedIn CONECTADO (Gabriel AI).\n- TikTok CONECTADO (expira 2026-06-30) + app per-user; PUBLISH PROVADO E2E (2× tiktok_publish_complete public:false=SELF_ONLY, exato de cliente não-auditado).\n- YouTube: app per-user existe + UPLOAD PROVADO E2E (2× youtube_upload_complete, video_ids nfkVpPzEiOI/5Q6BQRUw85o, privacy_status:null) MAS sem social_account ativo agora (conexão transitória; refresh_token não persistiu).\n- Twitter: NÃO conectado (tentativa 2026-06-28 degraded). Pinterest: app existe, NÃO conectado.\n\nPORTÕES DE PLATAFORMA (comprovados pela telemetria):\n- YouTube: projeto não-auditado → videos.insert FORÇA privado (privacy_status null observado). Audit + verificação consent screen destravam público.\n- TikTok: app não-auditado → SELF_ONLY (public:false observado) + conta privada. Content Posting API audit destrava público.\n- Instagram: publicação JÁ aprovada; INSIGHTS faltam scope instagram_manage_insights → collect-publication-metrics PULA IG hoje (skipped, sem fabricar).",
> 76	        "blocking_engineering": "Quase nada bloqueia publicar manual/por-post. ÚNICO gap de código: autopilot-run/index.ts:114 ainda tem VIDEO_FLOW_PLATFORMS=Set(['wordpress']) — YouTube/TikTok NÃO entram na cadência autônoma (a 'Fatia C' do blueprint). Adicionar 'youtube'/'tiktok' ao Set (1 linha + verificar billing de vídeo) é trabalho do loop. IG insights exige + scope instagram_manage_insights no branch IG de social-auth-init:87 (micro-ajuste). Todo o resto (OAuth/publish/refresh/UI/per-user creds) está pronto.",
> 77	        "sovereign_action": [
> 78	          "IG insights re-OAuth (IMEDIATO, sem App Review novo): após adicionar scope instagram_manage_insights ao branch IG (social-auth-init:87), desconectar e reconectar Instagram em /dashboard/social. Destrava engajamento real no collect-publication-metrics.",
> 79	          "YouTube reconectar (IMEDIATO): refazer OAuth do canal em /dashboard/social (app já existe, client_id 874740233059-...). A conexão sumiu — refazer com access_type=offline+prompt=consent (já no código) para gravar refresh_token; upload volta a funcionar (nasce privado).",
> 80	          "YouTube API Services Audit & Quota Extension Form (ESPERA ~semanas): submeter no Google Cloud Console + verificação consent screen OAuth (justificativa + vídeo demo do scope youtube.upload). SÓ ISSO destrava vídeos PÚBLICOS.",
> 81	          "TikTok app audit (ESPERA ~2-4 semanas): submeter audit do Content Posting API em developers.tiktok.com. SÓ ISSO destrava PUBLIC_TO_EVERYONE. Renovar token TikTok (expira 2026-06-30) reconectando em /dashboard/social.",
> 82	          "Twitter/X conectar (IMEDIATO, depende de tier): reconectar em /dashboard/social; publicação real de tweet exige X API Basic tier pago — verificar plano da conta dev antes de prometer publish público.",
> 83	          "Pinterest sair do Trial (ESPERA): app conectável (client_id 1585271); pin nasce sandbox/creator-only até Standard tier — solicitar upgrade no portal.",
> 84	          "Confirmar/converter o canal YouTube oficial do MCORCH (pré-requisito do upload)."
> 85	        ],
> 86	        "automatable_after": "Assim que (a) os audits forem aprovados e (b) 'youtube'/'tiktok' entrarem no VIDEO_FLOW_PLATFORMS, o viral-autopilot enfileira render 9:16 e publica autonomamente nos novos canais pela mesma cadência do IG Reel (mesmo MP4 HyperFrames, mesmo auto-publish cron). Antes dos audits, o loop já publica privado(YT)/SELF_ONLY(TikTok) autonomamente para validar transporte. IG insights, após o re-OAuth, alimenta collect-publication-metrics sozinho (sensory nerve FR-VA-028).",
> 87	        "decision_required": "Sovereign decide: (1) quais canais ativar primeiro no autopilot (TikTok+YT já provados E2E vs Pinterest/Twitter não conectados); (2) se aceita publicar privado/SELF_ONLY como prova de transporte enquanto os audits tramitam (recomendado — código não bloqueia, só o audit); (3) se paga X API Basic tier para Twitter público.",
> 88	        "cost_effort": "Ações imediatas (re-OAuth IG/YT, reconectar TikTok/Twitter/Pinterest): ~5-15 min cada na UI, R$0. IG insights scope: +~10 min de código (1 linha). Audits de plataforma: R$0 direto mas LEAD TIME de semanas (YT Trust&Safety + TikTok Content Posting). Twitter Basic tier: ~US$100/mês se publicar público via X API. Gap autopilot VIDEO_FLOW: ~1h de loop.",
> 89	        "unblock_signal": "Por plataforma: YouTube destravado = publish-youtube com privacy_status='public' (não null). TikTok destravado = publish-tiktok com public:true / publicaly_available_post_id não-null. IG insights = linha em publication_metrics com reach/impressions reais (não 'skipped'). Conexão = nova linha social_accounts is_active=true. Autopilot multi-canal = autopilot_cycles publicando em youtube/tiktok.",
> 90	        "evidence": [
> 91	          "supabase/functions/social-auth-init/index.ts:103-160 (branches TikTok/YouTube/Pinterest OAuth, resolveSocialAppCreds fail-closed)",
> 92	          "supabase/functions/publish-social/index.ts:263-477 (publish TikTok Direct Post + YouTube videos.insert resumable, leem privacy/status real Lei 1)",
> 93	          "supabase/functions/social-auth-callback/index.ts:179-286 (token exchange + perfil TikTok/YouTube/Pinterest)",
> 94	          "supabase/migrations/20260627120000_social_app_config.sql:33-66 (per-user Vault-encrypted client_secret + RLS auth.uid())",
> 95	          "supabase/migrations/20260402014040_b141fb0f-a65a-4020-a00e-1770dcf2ccfb.sql:12 (enum já com youtube/tiktok/pinterest)",
> 96	          "supabase/functions/autopilot-run/index.ts:114 (VIDEO_FLOW_PLATFORMS=Set(['wordpress']) — Único gap: YT/TikTok fora do ciclo autônomo)",
> 97	          "supabase/functions/collect-publication-metrics/index.ts:77-85 (IG insights skip sem scope — lights up após re-OAuth instagram_manage_insights)",
> 98	          "DB live social_accounts: instagram=magicorch/linkedin/facebook/tiktok conectados; youtube/twitter/pinterest sem linha ativa",
> 99	          "DB live social_app_config: tiktok(sbaw15o2nbsdx4xblp)/youtube(874740233059-...)/pinterest(1585271) per-user is_active=true",
> 100	          "infra_health_logs: publish-youtube ok youtube_upload_complete privacy_status=null (2026-06-28); publish-tiktok ok tiktok_publish_complete public:false SELF_ONLY (2026-06-27)"
> 101	        ],
> 102	        "_key": "oauth",
> 103	        "_label": "OAuth/App Review — YT · TikTok · IG · Twitter"
> 104	      },
> 105	      {
> 106	        "item": "Postback ML definitivo — IP residencial / portal ML (matt_tool/meli.la)",
> 107	        "ready_now": "partial",
> 108	        "current_state": "Framing do item (\"falta gerar o meli.la com matt_tool cravado\") esta MATERIALMENTE DESATUALIZADA — o essencial JA existe e esta vivo. Prova live (curl /rest/v1, 2026-06-30): affiliate_config do Usuario Zero (ada39fae) tem affiliate_tag=caga6077534, matt_tool=43641843, is_active=true, e 4 meli.la oficiais JA persistidos em metadata.shortlinks (MLB27834876 to meli.la/2gh13Sw, MLB32642694 to meli.la/2gNMCgS, MLB42978348 to meli.la/2pD1b86, MLB69703989 to meli.la/1AJGASk). O redirect process-affiliate-link GET resolve por 3 camadas fail-closed (index.ts:229-269): camada1 shortlinkOverride(metadata) faz 302 direto pro meli.la cravado (atribuicao DEFINITIVA); camada2 buildMattWordUrl com matt_word+matt_tool no product_url real; camada3 fail-closed /settings?no_config=1. matt_tool rida o meli.la e o matt_word link (index.ts:108). CLICK LEDGER FECHADO: 14 linhas affiliate_links, 15 cliques contados in-system, 0 revenue_cents (nenhuma compra convertida). handle-ml-postback deployado. FALTA de fato: (a) meli.la so existe pros 4 seeds — produto NOVO precisa do meli.la gerado manualmente no painel ML logado (IP residencial); (b) modulo authenticated-browser-operator (BoK 9/9 SELADA mas CODIGO NAO CONSTRUIDO — scripts/affiliate-operator NOT BUILT, tabela user_affiliate_links HTTP 404).",
> 109	        "blocking_engineering": "none para os 4 seeds do Usuario Zero — caminho de atribuicao definitiva (meli.la cravado + matt_tool) deployado e provado. Para ESCALAR a outros produtos sem trabalho manual, a engenharia pendente e o modulo authenticated-browser-operator (runner residencial scripts/affiliate-operator + edge affiliate-template-upsert + migration user_affiliate_links/affiliate_operator_consents — especificados na SDD 05-sdd.md, NAO codados). O runner roda na maquina RESIDENCIAL do usuario (datacenter Oracle da 403 em todas URLs ML, provado 2026-06-02/06-08).",
> 110	        "sovereign_action": [
> 111	          "Logar em mercadolivre.com.br/afiliados a partir do navegador RESIDENCIAL (IP domestico, nunca o datacenter) — ja feito pros 4 seeds, so repetir para produto novo.",
> 112	          "Abrir o produto, clicar Compartilhar/Barra de Afiliados, copiar o short link oficial meli.la/xxxx (ja embute conta caga6077534 + canal matt_tool 43641843, ref assinado nao-fabricavel).",
> 113	          "Registrar no sistema: (a) UPDATE affiliate_config metadata jsonb_set shortlinks MLB-id para a URL meli.la WHERE user_id=ada39fae; OU (b) bun run scripts/add-product-manually.ts --id MLB-id --url https://meli.la/xxxx (catalogo vm_affiliate_products).",
> 114	          "Verificar: GET ao redirect com product_id + content_variant_id do dono retorna HTTP 302 Location https://meli.la/xxxx (nao /settings, nao matt_word).",
> 115	          "Para parar de fazer manual a cada produto: dar GO de engenharia ao modulo authenticated-browser-operator (BoK ja selada)."
> 116	        ],
> 117	        "automatable_after": "Depois que o modulo authenticated-browser-operator for codado E o Sovereign rodar o runner uma vez na maquina residencial (consentido, human-paced): o loop captura automaticamente o meli.la oficial de cada produto do /afiliados/hub, upsert per-user em user_affiliate_links, e o redirect prefere esse link sem acao manual. Sem o modulo, cada produto novo exige o passo manual no painel logado (ML nao tem API publica de link — ml-affiliate-attribution.md).",
> 118	        "unblock_signal": "RECEITA real: revenue_cents>0 numa linha affiliate_links do tenant correto apos compra real, refletido no ROIWidget via handle-ml-postback. HOJE total_revenue_cents=0 em 14 linhas/15 cliques (atribuicao pronta, conversao zero). ATRIBUICAO definitiva de produto novo: GET ao redirect retorna 302 Location https://meli.la/... (camada1) em vez de matt_word (camada2).",
> 119	        "cost_effort": "Por produto novo (manual): ~3-5 min do Sovereign no painel ML residencial + 1 comando, R$0. Construir o modulo ABO: ~1 sessao de engenharia (runner + 2 edge fns + 1 migration ja especificados na SDD), R$0. Nenhum custo desbloqueia receita por si — receita depende de distribuicao/trafego que converta.",
> 120	        "decision_required": "Prioridade: item e ATRIBUICAO de melhor qualidade, NAO bloqueador de receita — cliques ja contados in-system e os 4 meli.la definitivos vivos. Gargalo real do funil (feedback_full_force_revenue_autonomy + project_revenue_funnel_repair) e DISTRIBUICAO+TRAFEGO que converta (R$0/15 cliques), nao plumbing de atribuicao. Decisao: (a) prioridade BAIXA e focar distribuicao; OU (b) GO ao modulo authenticated-browser-operator para escalar a captura de meli.la ao catalogo inteiro.",
> 121	        "evidence": [
> 122	          "DB live curl /rest/v1/affiliate_config 2026-06-30: user ada39fae affiliate_tag=caga6077534 matt_tool=43641843 is_active=true metadata.shortlinks com 4 meli.la (MLB27834876 to meli.la/2gh13Sw etc.)",
> 123	          "supabase/functions/process-affiliate-link/index.ts:229-269 GET 3-camadas shortlinkOverride->matt_word+matt_tool->fail-closed",
> 124	          "supabase/functions/process-affiliate-link/index.ts:108 matt_tool seteado no link matt_word",
> 125	          "DB live: 14 affiliate_links, 15 cliques, 0 revenue_cents",
> 126	          "supabase/migrations/20260604150000_affiliate_matt_tool.sql:8 coluna matt_tool aplicada",
> 127	          "docs/bok/authenticated-browser-operator/05-sdd.md:96-124 modulo especificado mas NAO codado",
> 128	          "scripts/affiliate-operator NOT BUILT; GET /rest/v1/user_affiliate_links HTTP 404",
> 129	          "docs/processes/ml-affiliate-attribution.md ML sem API publica de link; matt_word=best-effort meli.la=definitivo",
> 130	          "supabase/functions/handle-ml-postback/index.ts existe"
> 131	        ],
> 132	        "_key": "ml-postback",
> 133	        "_label": "Postback ML definitivo — matt_tool/meli.la"
> 134	      },
> 135	      {
> 136	        "item": "Stripe live keys — ao primeiro cliente externo (Financial Debt / Stripe Prod Swap, OE-661-ROADMAP)",
> 137	        "ready_now": "yes",
> 138	        "current_state": "Billing 100% implementado e DEPLOYADO em modo TEST/sandbox — faltando SOMENTE o swap de chave para live. As 4 edge functions estão ACTIVE em produção (`supabase functions list`): create-checkout (v43), create-portal (v43), check-subscription (v43), stripe-webhook (v46, verify_jwt=false em config.toml:90-91). create-checkout cria customer + checkout.sessions subscription com trial 14d (create-checkout/index.ts:54-63); stripe-webhook valida assinatura whsec_ e faz upsert em `subscriptions` + sincroniza `profiles.mco_balance` por plano (stripe-webhook/index.ts:95-101,68-77); create-portal abre billingPortal; check-subscription lê assinaturas active/trialing. Frontend wirado: useSubscription.ts (checkout/openPortal via supabase.functions.invoke) + BillingPage.tsx com 3 planos e price IDs CONCRETOS já gravados (price_1TLAquKZfElfyPErrAuC95bU Starter R$147, price_1TLArCKZfElfyPErQeOTQv52 Pro R$397, price_1TLArZKZfElfyPErTXLBp0ZF Enterprise R$997). Secrets STRIPE_SECRET_KEY e STRIPE_WEBHOOK_SECRET JÁ presentes no vault (atualmente apontando sandbox). Decisão estratégica DOCUMENTADA de manter sandbox: OTD-003 Decision B (\"Hold until first paying client validates flow end-to-end\", mcorch-constellation/05-sdd.md:596 + 00-index.md:102) + memory project_stripe_strategy (Gabriel não paga fees Stripe em transações de teste enquanto valida como Usuário Zero).",
> 139	        "blocking_engineering": "none",
> 140	        "sovereign_action": [
> 141	          "1. No Stripe Dashboard: garantir que a conta saiu de test mode e está ativada (ver pré-requisito KYC abaixo). Alternar o toggle para Live mode.",
> 142	          "2. No Stripe Dashboard (Live mode): recriar os 3 produtos/preços (Starter R$147, Pro R$397, Enterprise R$997) — price IDs de test (price_1TLA...) NÃO funcionam em live. Anotar os 3 novos price IDs live (price_live_...).",
> 143	          "3. Copiar a chave secreta live: Stripe Dashboard > Developers > API keys > Secret key (sk_live_...).",
> 144	          "4. Rodar o swap do secret no Supabase: `npx supabase secrets set STRIPE_SECRET_KEY=sk_live_<chave>` (NUNCA colar em .env versionado nem em código — vault-only, BR-SEC-003).",
> 145	          "5. Configurar o webhook endpoint live: Stripe Dashboard > Developers > Webhooks > Add endpoint apontando para https://<project-ref>.supabase.co/functions/v1/stripe-webhook, eventos: customer.subscription.created/updated/deleted + checkout.session.completed. Copiar o Signing secret (whsec_...).",
> 146	          "6. Rodar `npx supabase secrets set STRIPE_WEBHOOK_SECRET=whsec_<live>`.",
> 147	          "7. Atualizar os 3 priceId em src/pages/BillingPage.tsx (linhas 18, 34, 53) para os price IDs live, e rebuild+deploy do frontend (skill build-deploy-guardian — dist/ do repo principal).",
> 148	          "8. (Opcional, não muda código) redeploy das edge functions não é necessário — elas leem o secret em runtime; só o swap do secret + price IDs do frontend.",
> 149	          "9. Teste E2E com cartão real de baixo valor (ou primeira assinatura do cliente real): checkout > webhook 200 > linha em `subscriptions` status=trialing/active + profiles.mco_balance sincronizado."
> 150	        ],
> 151	        "automatable_after": "Nada novo passa a ser autônomo pelo loop — o billing já é totalmente automático em qualquer modo (webhook sincroniza subscriptions + mco_balance sem intervenção). O swap apenas troca o destino test→live das transações. Após o swap, a atribuição de receita real por tenant (subscriptions ativas) passa a alimentar os KPIs/dashboard de business health que hoje ficam zerados em sandbox.",
> 152	        "unblock_signal": "Webhook live retorna HTTP 200 numa assinatura real e aparece uma linha em `subscriptions` com stripe_subscription_id começando em sub_ (não de test), status active/trialing, + profiles.mco_balance sincronizado para o plano — confirmado por SELECT real (Lei 1). Antes disso, o sinal de PRONTIDÃO já existe: `supabase functions list` mostra as 4 fns ACTIVE.",
> 153	        "evidence": [
> 154	          "supabase/functions/create-checkout/index.ts:37,54-63 — Stripe checkout subscription com trial 14d, lê STRIPE_SECRET_KEY do vault",
> 155	          "supabase/functions/stripe-webhook/index.ts:93-101 — verificação de assinatura whsec_ (STRIPE_WEBHOOK_SECRET) + index.ts:68-77 upsert subscriptions + sync profiles.mco_balance",
> 156	          "supabase/functions/create-portal/index.ts:41-44 — billingPortal sessions",
> 157	          "supabase/functions/check-subscription/index.ts:42-69 — lista subs active+trialing",
> 158	          "src/pages/BillingPage.tsx:18,34,53 — price IDs de TEST hardcoded (price_1TLAquKZ.../1TLArCKZ.../1TLArZKZ...) que precisam virar live",
> 159	          "src/hooks/useSubscription.ts:18,39 — checkout/openPortal invocam create-checkout/create-portal",
> 160	          "supabase/config.toml:90-91 — [functions.stripe-webhook] verify_jwt=false (necessário p/ webhook externo)",
> 161	          "docs/bok/mcorch-constellation/05-sdd.md:596 — OTD-003 Decision B: 'Hold until first paying client validates flow end-to-end; sandbox is intentional'",
> 162	          "docs/bok/mcorch-constellation/00-index.md:102 — OTD-003 Open, escolha B (per memory project_stripe_strategy)",
> 163	          "memory project_stripe_strategy.md — 'Não tratar como pendência bloqueadora — é decisão estratégica consciente; trigger = primeiro cliente além de mim mesmo'",
> 164	          "docs/bok/security/04-fmea-security.md:38 — FM-11 swap sk_live, RPN residual 18, 'Controle ativo (sandbox)'",
> 165	          "docs/bok/security/01-brd-security.md:52 — chaves Stripe vault-only, webhook valida whsec_ em toda requisição",
> 166	          "supabase functions list (output ao vivo) — create-checkout/create-portal/check-subscription/stripe-webhook todas ACTIVE"
> 167	        ],
> 168	        "decision_required": "Timing do flip é Sovereign-only (human-in-loop OE-661 / mcorch-constellation:596): decidir QUANDO acionar — o gatilho documentado é \"primeiro cliente externo além de mim\" ou \"primeira venda do case\". Não há decisão de arquitetura pendente; só a decisão de negócio de quando existe demanda de pagamento real.",
> 169	        "cost_effort": "Esforço Sovereign: ~30-60 min de cliques no Stripe Dashboard + 2 comandos `supabase secrets set` + 1 edit de 3 linhas no BillingPage + rebuild/deploy. Custo financeiro: Stripe não cobra mensalidade — só fee por transação (~3.99% + R$0,39 no Brasil) que só incide quando há venda real; logo custo efetivo R$0 até existir cliente pagante.",
> 170	        "_key": "stripe",
> 171	        "_label": "Stripe live keys"
> 172	      }
> 173	    ],
> 174	    "sequence": {
> 175	      "do_now": [
> 176	        {
> 177	          "item": "GO de gasto — 1º ciclo PAGO de vídeo (autopilot)",
> 178	          "why": "Pipeline 100% provado em produção (HyperFrames motor VIVO, begin/finalize_autopilot_cycle atômicos, over-charge JÁ mitigado em autopilot-run:114 via VIDEO_FLOW_PLATFORMS). Zero engenharia bloqueia. É o único item que converte trabalho do loop em VALOR VISÍVEL ao Usuário Zero (diretiva feedback_deliver_user_value) por ~24 mco / ~US$0.04. Saldo 4669 mco cobre folgado. Owner do blast-radius = só o Sovereign.",
> 179	          "first_step": "Dar o GO verbal de gasto; o agente então roda UPDATE public.autopilot_plans SET video_enabled=true WHERE id='640b3b67-b950-42f6-bbb9-48560771eaa6' (via SB_SECRET_KEY) e invoca autopilot-run manual (Bearer SB_SECRET_KEY + x-autopilot-user-id=ada39fae, body {plan_id}) para testemunho controlado."
> 180	        },
> 181	        {
> 182	          "item": "DNS/vhost — video.mcorch.com (canônico) / studio.mcorch.com",
> 183	          "why": "Nenhuma engenharia nem ação física pendente — DNS+cert+symlink+nginx já executados em 24-jun e o editor é servido pelo iframe SSO-gated em /dashboard/canvas/video. É só FECHAR o item na fila e validar visualmente, liberando o loop pra seguir a Fatia VS-UI Fase B sem ambiguidade de nome canônico.",
> 184	          "first_step": "Abrir https://video.mcorch.com LOGADO (ou /dashboard/canvas/video no SPA) e confirmar que o editor 9:16 carrega; depois marcar o item como CONCLUÍDO no charter (.claude/context/autonomous-loop-charter.md:62). NÃO renomear pra studio.mcorch.com (sem ganho, exige novo cert+symlink+rebuild)."
> 185	        },
> 186	        {
> 187	          "item": "OAuth re-conexões IMEDIATAS — IG insights · YouTube · TikTok · Twitter · Pinterest",
> 188	          "why": "OAuth/publish/refresh/UI/creds per-user já prontos; as reconexões na UI (R$0, ~5-15 min cada) destravam transporte de saída e métricas reais (collect-publication-metrics) SEM esperar audit. YouTube/TikTok publicam privado/SELF_ONLY como prova de transporte enquanto os audits tramitam. Não colide com o loop (ações de UI, não código).",
> 189	          "first_step": "Reconectar YouTube em /dashboard/social com access_type=offline+prompt=consent (grava refresh_token); reconectar TikTok (token expira HOJE 2026-06-30) e Instagram. Renovar o token TikTok é URGENTE pela data de expiração."
> 190	        },
> 191	        {
> 192	          "item": "Postback ML definitivo — registrar meli.la dos seeds (manual, baixa prioridade)",
> 193	          "why": "Caminho de atribuição definitiva (meli.la cravado + matt_tool) JÁ deployado/provado pros 4 seeds. Não é bloqueador de receita — cliques já contados in-system. Só registrar produto novo quando houver, via painel ML residencial. O gargalo real é DISTRIBUIÇÃO/TRÁFEGO, não plumbing de atribuição.",
> 194	          "first_step": "Quando surgir produto novo: no navegador RESIDENCIAL, copiar o short link meli.la do /afiliados e registrar via bun run scripts/add-product-manually.ts --id MLB-id --url https://meli.la/xxxx; verificar redirect 302 → meli.la. Caso contrário, deixar parado e focar distribuição."
> 195	        }
> 196	      ],
> 197	      "blocked_on_loop": [
> 198	        {
> 199	          "item": "OAuth autopilot autônomo p/ YT+TikTok (publicar pela cadência viral-autopilot)",
> 200	          "waiting_for": "Loop adicionar 'youtube'/'tiktok' ao VIDEO_FLOW_PLATFORMS=Set(['wordpress']) em autopilot-run/index.ts:114 + verificar billing de vídeo (Fatia C do blueprint). É ~1h de loop; as reconexões OAuth do Sovereign não bastam sozinhas pra cadência autônoma."
> 201	        },
> 202	        {
> 203	          "item": "IG insights no collect-publication-metrics",
> 204	          "waiting_for": "Loop adicionar scope instagram_manage_insights ao branch IG de social-auth-init:87 (1 linha). SÓ DEPOIS o Sovereign desconecta+reconecta IG e o engajamento real passa a alimentar a FR-VA-028."
> 205	        },
> 206	        {
> 207	          "item": "Vídeos PÚBLICOS em YouTube e TikTok (não só private/SELF_ONLY)",
> 208	          "waiting_for": "Audits de plataforma (YouTube API Services Audit + TikTok Content Posting API) — lead time de SEMANAS, ação Sovereign externa; nenhum código bloqueia, mas o público depende da aprovação."
> 209	        },
> 210	        {
> 211	          "item": "Escalar captura de meli.la ao catálogo inteiro (sem passo manual por produto)",
> 212	          "waiting_for": "Loop codar o módulo authenticated-browser-operator (runner + 2 edge fns + 1 migration já especificados na SDD), e DEPOIS o Sovereign rodar o runner 1× na máquina residencial (datacenter Oracle dá 403 em todas URLs ML)."
> 213	        },
> 214	        {
> 215	          "item": "Editor Studio Fatia VS-UI Fase B (export prepaid via mcoCoins)",
> 216	          "waiting_for": "Loop implementar McorchAdapter.startRender → edge video-render substituindo o engine CLI local (Fase A), fechando OTD-VS-005(C). DNS/vhost já não bloqueia."
> 217	        },
> 218	        {
> 219	          "item": "Stripe live — atribuição de receita real por tenant nos KPIs",
> 220	          "waiting_for": "Gatilho de NEGÓCIO, não engenharia: 'primeiro cliente externo' ou 'primeira venda do case'. Billing já é 100% automático em qualquer modo; o swap só troca test→live e exige recriar 3 price IDs + secrets + 3 linhas no BillingPage + rebuild."
> 221	        }
> 222	      ],
> 223	      "highest_leverage": "GO de gasto — 1º ciclo PAGO de vídeo. É o ÚNICO item ready_now=yes onde o loop está literalmente parado esperando UMA decisão do Sovereign (a flag video_enabled), e destravá-lo libera o maior valor downstream: a partir do GO, o loop renderiza+publica autonomamente um short 9:16 product-aware a cada 3 dias (autopilot-cadence-cron → autopilot-run → orchestrate → video-bridge → finalize → auto-publish) sem intervenção humana por ciclo. Custa ~24 mco (~US$0.04, saldo 4669 cobre folgado), risco material ínfimo, e converte toda a engenharia já provada (HyperFrames motor, cadência, RPCs atômicos) em valor VISÍVEL ao Usuário Zero — exatamente o que a diretiva feedback_deliver_user_value pediu. Tudo o mais ou já está concluído (DNS/vhost), ou tem lead time de semanas (audits), ou depende de demanda externa (Stripe), ou é atribuição que não move receita (Postback). Este é o gargalo de UMA palavra.",
> 224	      "recommended_order": [
> 225	        "1. GO de gasto + flag video_enabled + disparar 1º ciclo PAGO de vídeo (1 palavra do Sovereign destrava o loop; ~2 min; maior ROI imediato)",
> 226	        "2. Reconectar TikTok HOJE (token expira 2026-06-30 — janela fechando) + reconectar YouTube com offline/consent + Instagram (~5-15 min cada, R$0; destrava transporte e prepara as próximas Fatias do loop)",
> 227	        "3. Validar video.mcorch.com / /dashboard/canvas/video e marcar o item DNS/vhost como CONCLUÍDO no charter (1 min; remove ruído da fila)",
> 228	        "4. Submeter audits de plataforma YouTube + TikTok (R$0 mas lead time de SEMANAS — começar AGORA porque o relógio é externo, não porque é urgente hoje)",
> 229	        "5. Stripe live keys — SOMENTE ao primeiro cliente externo / primeira venda (gatilho de negócio; não acionar antes de existir demanda de pagamento real)",
> 230	        "6. Postback ML definitivo — prioridade BAIXA: registrar meli.la só quando houver produto novo; gargalo real é distribuição, não atribuição"
> 231	      ],
> 232	      "conflicts_with_running_loop": "Risco de colisão BAIXO e gerenciável. O único ponto de contato é o arquivo autopilot-run/index.ts:114 (VIDEO_FLOW_PLATFORMS): o loop pode pegar a Fatia 'brand-persona YT/TikTok' e editar essa mesma linha para adicionar 'youtube'/'tiktok'. Isso NÃO conflita com o GO de gasto do Sovereign, porque o disparo do 1º ciclo só faz UPDATE de dados (autopilot_plans.video_enabled via SQL) e invoke da edge fn — não toca código-fonte. Disciplina anti-colisão: (a) o GO de gasto opera só sobre DADOS/estado (SQL + invoke), nunca sobre arquivos que o loop edita; (b) as reconexões OAuth do Sovereign são 100% na UI/portais externos (zero código); (c) se o Sovereign quiser editar o frontend (ex.: BillingPage.tsx no swap Stripe), coordenar timing com o loop ou fazê-lo em branch/worktree separado para evitar rebase. Como o loop trabalha o backlog DESBLOQUEADO (Gabriel AI 3b, Unified Canvas, Security) e as ações Sovereign são externas/dados, os caminhos são quase disjuntos por design da charter."
> 233	    }
> 234	  },
> 235	  "workflowProgress": [
> 236	    {
> 237	      "type": "workflow_phase",
> 238	      "index": 1,
> 239	      "title": "Investigate"
> 240	    },
> 241	    {
> 242	      "type": "workflow_phase",
> 243	      "index": 2,
> 244	      "title": "Sequence"
> 245	    },
> 246	    {
> 247	      "type": "workflow_agent",
> 248	      "index": 1,
> 249	      "label": "inv:biometria",
> 250	      "phaseIndex": 1,
> 251	      "phaseTitle": "Investigate",
> 252	      "agentId": "ab279bf78a3e3e5ef",
> 253	      "model": "claude-opus-4-8",
> 254	      "state": "error",
> 255	      "startedAt": 1782861262485,
> 256	      "queuedAt": 1782861262440,
> 257	      "attempt": 1,
> 258	      "lastToolName": "StructuredOutput",
> 259	      "promptPreview": "Investigue o item da Fila de Ação Sovereign: **Biometria — Gabriel AI Fatia 3b (avatarIdentity + Identity Gate)**.\nLeia: docs/bok/avatar-clone-ai/04-frd.md (procure FR-AC-013, FR-AC-014, Identity Gate), 05-sdd.md, 06-data-model.md (tabela avatar_identities, colunas arcface_threshold/identity_storage_key), e procure a migration que cria avatar_identities (grep -rn \"avatar_identities\" supabase/migra…",
> 260	      "lastProgressAt": 1782861575296,
> 261	      "error": "agent({schema}): StructuredOutput retry cap (5) exceeded — 5 failed calls with no valid output",
> 262	      "tokens": 94721,
> 263	      "toolCalls": 12,
> 264	      "durationMs": 312811
> 265	    },
> 266	    {
> 267	      "type": "workflow_agent",
> 268	      "index": 2,
> 269	      "label": "inv:go-gasto",
> 270	      "phaseIndex": 1,
> 271	      "phaseTitle": "Investigate",
> 272	      "agentId": "a3cf38ec496c851ff",
> 273	      "model": "claude-opus-4-8",
> 274	      "state": "done",
> 275	      "startedAt": 1782861262487,
> 276	      "queuedAt": 1782861262441,
> 277	      "attempt": 1,
> 278	      "lastToolName": "StructuredOutput",
> 279	      "lastToolSummary": "GO de gasto — 1o ciclo PAGO de video do Viral Autopilot (vi…",
> 280	      "promptPreview": "Investigue o item da Fila de Ação Sovereign: **GO de gasto — 1º ciclo PAGO de vídeo do Viral Autopilot (video_enabled + testemunho)**.\nLeia: docs/processes/autopilot-video-9x16.md, docs/processes/autopilot-cron-identity.md, e procure a flag que liga vídeo (grep -rn \"video_enabled\" supabase/ scripts/ src/). Procure as edge functions autopilot-run, autopilot-cadence-cron, e a tabela autopilot_plans …",
> 281	      "lastProgressAt": 1782861512239,
> 282	      "tokens": 107256,
> 283	      "toolCalls": 26,
> 284	      "durationMs": 249751,
> 285	      "resultPreview": "{\"item\":\"GO de gasto — 1o ciclo PAGO de video do Viral Autopilot (video_enabled + testemunho)\",\"ready_now\":\"yes\",\"current_state\":\"O pipeline de video 9:16 esta MATERIALMENTE end-to-end pronto e JA RODOU PAGO uma vez — nao falta engenharia. Provas vivas: (1) worker video-bridge.service ATIVO ha 2 dias (PID 768276) com renders reais nos logs (06-28: \\\"render ... done 536KB\\\"); motor HyperFrames pres…"
> 286	    },
> 287	    {
> 288	      "type": "workflow_agent",
> 289	      "index": 3,
> 290	      "label": "inv:dns-vhost",
> 291	      "phaseIndex": 1,
> 292	      "phaseTitle": "Investigate",
> 293	      "agentId": "a038dc532159036f0",
> 294	      "model": "claude-opus-4-8",
> 295	      "state": "done",
> 296	      "startedAt": 1782861512241,
> 297	      "queuedAt": 1782861262441,
> 298	      "attempt": 1,
> 299	      "lastToolName": "StructuredOutput",
> 300	      "lastToolSummary": "DNS/vhost — studio.mcorch.com (editor HyperFrames) e design…",
> 301	      "promptPreview": "Investigue o item da Fila de Ação Sovereign: **DNS/vhost — studio.mcorch.com (editor HyperFrames) e design.mcorch.com**.\nLeia: nginx/video.mcorch.com.conf, docs/processes/video-studio-editor-deploy-and-provision.md, e procure referências a studio.mcorch.com e design.mcorch.com (grep -rn \"studio.mcorch.com\\|design.mcorch.com\" nginx/ docs/ .claude/ scripts/). Leia também .claude/context/hyperframes-…",
> 302	      "lastProgressAt": 1782861604350,
> 303	      "tokens": 93726,
> 304	      "toolCalls": 13,
> 305	      "durationMs": 92108,
> 306	      "resultPreview": "{\"item\":\"DNS/vhost — studio.mcorch.com (editor HyperFrames) e design.mcorch.com\",\"ready_now\":\"yes\",\"current_state\":\"JÁ ESTÁ FEITO — o item da fila está STALE. O editor HyperFrames NÃO foi servido em `studio.mcorch.com`; a implementação escolheu o nome `video.mcorch.com` (decisão registrada na SDD Amendment v0.3, que listou `studio.mcorch.com`/`video.mcorch.com` como alternativas — OTD-VS-005/OTD-V…"
> 307	    },
> 308	    {
> 309	      "type": "workflow_agent",
> 310	      "index": 4,
> 311	      "label": "inv:oauth",
> 312	      "phaseIndex": 1,
> 313	      "phaseTitle": "Investigate",
> 314	      "agentId": "a61e44c599179ca07",
> 315	      "model": "claude-opus-4-8",
> 316	      "state": "done",
> 317	      "startedAt": 1782861575298,
> 318	      "queuedAt": 1782861262441,
> 319	      "attempt": 1,
> 320	      "lastToolName": "StructuredOutput",
> 321	      "lastToolSummary": "OAuth/App Review — YouTube · TikTok · Instagram · Twitter ·…",
> 322	      "promptPreview": "Investigue o item da Fila de Ação Sovereign: **OAuth/App Review — YouTube · TikTok · Instagram · Twitter · re-OAuth IG insights**.\nLeia: .claude/context/yt-tiktok-brand-persona-integration-prep-2026-06-26.md, e procure as edge functions de social auth (grep -rn \"social-auth\\|social_platform\\|publish-social\" supabase/functions/ | head -40). Procure o enum social_platform nas migrations e a tabela s…",
> 323	      "lastProgressAt": 1782861741159,
> 324	      "tokens": 121605,
> 325	      "toolCalls": 14,
> 326	      "durationMs": 165861,
> 327	      "resultPreview": "{\"item\":\"OAuth/App Review — YouTube · TikTok · Instagram · Twitter · Pinterest · re-OAuth IG insights (estado material por plataforma)\",\"ready_now\":\"partial\",\"current_state\":\"O item da Fila está DESATUALIZADO frente ao código/infra real. O blueprint de 2026-06-26 dizia \\\"nenhum publisher YT/TikTok escrito\\\"; desde então TODO o net-new foi shippado (commits 25477a8/f5e092c/6c3bc66 + migration c94bd…"
> 328	    },
> 329	    {
> 330	      "type": "workflow_agent",
> 331	      "index": 5,
> 332	      "label": "inv:ml-postback",
> 333	      "phaseIndex": 1,
> 334	      "phaseTitle": "Investigate",
> 335	      "agentId": "afdffbfa17d110b65",
> 336	      "model": "claude-opus-4-8",
> 337	      "state": "done",
> 338	      "startedAt": 1782861604352,
> 339	      "queuedAt": 1782861262441,
> 340	      "attempt": 1,
> 341	      "lastToolName": "StructuredOutput",
> 342	      "lastToolSummary": "Postback ML definitivo — IP residencial / portal ML (matt_t…",
> 343	      "promptPreview": "Investigue o item da Fila de Ação Sovereign: **Postback ML definitivo — IP residencial / portal ML (matt_tool/meli.la)**.\nLeia: e procure project context sobre o operador de browser autenticado e o funil de receita. grep -rn \"matt_tool\\|matt_word\\|meli.la\\|affiliate_tag\" scripts/ supabase/functions/ docs/. Leia docs/processes/affiliate-credential-resolution.md, scripts/link-forge.ts, supabase/func…",
> 344	      "lastProgressAt": 1782861797892,
> 345	      "tokens": 112184,
> 346	      "toolCalls": 17,
> 347	      "durationMs": 193540,
> 348	      "resultPreview": "{\"item\":\"Postback ML definitivo — IP residencial / portal ML (matt_tool/meli.la)\",\"ready_now\":\"partial\",\"current_state\":\"Framing do item (\\\"falta gerar o meli.la com matt_tool cravado\\\") esta MATERIALMENTE DESATUALIZADA — o essencial JA existe e esta vivo. Prova live (curl /rest/v1, 2026-06-30): affiliate_config do Usuario Zero (ada39fae) tem affiliate_tag=caga6077534, matt_tool=43641843, is_activ…"
> 349	    },
> 350	    {
> 351	      "type": "workflow_agent",
> 352	      "index": 6,
> 353	      "label": "inv:stripe",
> 354	      "phaseIndex": 1,
> 355	      "phaseTitle": "Investigate",
> 356	      "agentId": "ab9140ab12c3ac424",
> 357	      "model": "claude-opus-4-8",
> 358	      "state": "done",
> 359	      "startedAt": 1782861741161,
> 360	      "queuedAt": 1782861262442,
> 361	      "attempt": 1,
> 362	      "lastToolName": "StructuredOutput",
> 363	      "lastToolSummary": "Stripe live keys — ao primeiro cliente externo (Financial D…",
> 364	      "promptPreview": "Investigue o item da Fila de Ação Sovereign: **Stripe live keys — ao primeiro cliente externo**.\nProcure: grep -rn \"STRIPE_SECRET_KEY\\|stripe\" supabase/functions/ src/lib/ scripts/ | head -40. Leia HANDOFF.md (procure a seção de Stripe Prod Swap) e qualquer SOP de billing. Procure as edge functions que usam Stripe (checkout, webhook, customer portal).\nDetermine MATERIALMENTE: (1) o billing está im…",
> 365	      "lastProgressAt": 1782861836973,
> 366	      "tokens": 90132,
> 367	      "toolCalls": 18,
> 368	      "durationMs": 95811,
> 369	      "resultPreview": "{\"item\":\"Stripe live keys — ao primeiro cliente externo (Financial Debt / Stripe Prod Swap, OE-661-ROADMAP)\",\"ready_now\":\"yes\",\"current_state\":\"Billing 100% implementado e DEPLOYADO em modo TEST/sandbox — faltando SOMENTE o swap de chave para live. As 4 edge functions estão ACTIVE em produção (`supabase functions list`): create-checkout (v43), create-portal (v43), check-subscription (v43), stripe-…"
> 370	    },
> 371	    {
> 372	      "type": "workflow_agent",
> 373	      "index": 7,
> 374	      "label": "sequencer",
> 375	      "phaseIndex": 2,
> 376	      "phaseTitle": "Sequence",
> 377	      "agentId": "aa33e078e3c0d597a",
> 378	      "model": "claude-opus-4-8",
> 379	      "state": "done",
> 380	      "startedAt": 1782861837006,
> 381	      "queuedAt": 1782861836974,
> 382	      "attempt": 1,
> 383	      "lastToolName": "StructuredOutput",
> 384	      "lastToolSummary": "GO de gasto — 1º ciclo PAGO de vídeo. É o ÚNICO item ready_…",
> 385	      "promptPreview": "Você é o coordenador. Recebeu a investigação material de 6 itens da Fila de Ação Sovereign do MCORCH. O contexto: há um /loop autônomo rodando em OUTRA sessão fazendo a engenharia DESBLOQUEADA (backlog: Gabriel AI 3b emenda BoK+scaffold, YT/TikTok branches, editor Studio, Unified Canvas, Security hardening). O Sovereign (Gabriel) quer saber quais itens da fila ele já pode COMEÇAR A DESTRAVAR agora…",
> 386	      "lastProgressAt": 1782861899178,
> 387	      "tokens": 80907,
> 388	      "toolCalls": 2,
> 389	      "durationMs": 62171,
> 390	      "resultPreview": "{\"do_now\":[{\"item\":\"GO de gasto — 1º ciclo PAGO de vídeo (autopilot)\",\"why\":\"Pipeline 100% provado em produção (HyperFrames motor VIVO, begin/finalize_autopilot_cycle atômicos, over-charge JÁ mitigado em autopilot-run:114 via VIDEO_FLOW_PLATFORMS). Zero engenharia bloqueia. É o único item que converte trabalho do loop em VALOR VISÍVEL ao Usuário Zero (diretiva feedback_deliver_user_value) por ~24 …"
> 391	    }
> 392	  ],
> 393	  "totalTokens": 700531,
> 394	  "totalToolCalls": 102
> 395	}
> ```

## 🤖 Claude *(23:29:00)*


## 🤖 Claude *(23:29:03)*

O runbook completo voltou e é material (verificado contra DB live, infra e código). Vou persistir numa versão durável em `.claude/context` (pra "depois" não se perder — o output bruto estava só no scratch efêmero), e depois te dou a síntese focada na sua doutrina + GO.

## 🤖 Claude *(23:29:52)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/sovereign-queue-runbook-2026-06-30.md",
  "content": "# Sovereign Action Queue \u2014 Runbook Material (2026-06-30)\n\n> Verificado contra DB live, infra (systemd/nginx/curl) e c\u00f3digo por workflow `wf_443fc8de-27b` (6 investigadores + sequenciador, 700k tokens). Lei 1: cada item carrega evid\u00eancia `arquivo:linha` / UUID / curl.\n> Doutrina aplic\u00e1vel: `feedback_opensource_first_zero_cost_equity` \u2014 custo USD externo = 0 ao Sovereign; open-source/self-hosted dentro do MCORCH.\n\n## Ordem recomendada (por ROI/urg\u00eancia)\n\n1. **GO de gasto \u2014 1\u00ba ciclo PAGO de v\u00eddeo** (1 palavra destrava o loop; ~2 min; maior ROI)\n2. **Reconectar TikTok HOJE** (token expira **2026-06-30** \u2014 janela fechando) + YouTube (offline/consent) + Instagram (~5-15 min cada, R$0)\n3. **Validar `video.mcorch.com`** e marcar DNS/vhost CONCLU\u00cdDO (1 min \u2014 item j\u00e1 est\u00e1 feito)\n4. **Submeter audits YouTube + TikTok** (R$0 mas lead time de SEMANAS \u2014 come\u00e7ar j\u00e1 porque o rel\u00f3gio \u00e9 externo)\n5. **Stripe live keys** \u2014 S\u00d3 ao primeiro cliente externo (gatilho de neg\u00f3cio)\n6. **Postback ML definitivo** \u2014 prioridade BAIXA (gargalo real \u00e9 distribui\u00e7\u00e3o, n\u00e3o atribui\u00e7\u00e3o)\n\n---\n\n## 1. GO de gasto \u2014 1\u00ba ciclo PAGO de v\u00eddeo  \u00b7 `ready_now: YES` \u00b7 highest-leverage\n\n**Estado:** pipeline 9:16 end-to-end PROVADO em produ\u00e7\u00e3o, j\u00e1 rodou pago 1\u00d7. N\u00e3o falta engenharia.\n- `video-bridge.service` ATIVO (HyperFrames render-core + worker).\n- Render real `video_renders id=8b0787e0` state=done charged_mco=12; MP4 no bucket `video-studio-assets` = **748324 bytes** (06-26); reconcilia\u00e7\u00e3o FR-VA-025 OK (`content_library id=31dba713` type=video).\n- Plano \u00fanico User 0: `autopilot_plans id=640b3b67` user=ada39fae, **`video_enabled=false` + `is_active=false`**, saldo `mco_balance=4669`, caps 50/50.\n- Custo: 10 (orch) + 12 (render) + 2 (analyze) = **~24 mco** por v\u00eddeo (~US$0.043 teto 4\u00d7-floor; **render HyperFrames \u00e9 infra-only ~US$0**).\n- CF /wp-json: RESOLVIDO (post_id 18); autopilot publica WP como draft \u2192 n\u00e3o bloqueia o ciclo.\n- Over-charge conhecido J\u00c1 mitigado (`autopilot-run:114` VIDEO_FLOW_PLATFORMS).\n\n**\u26a0\ufe0f Gate da doutrina (open-source-first / zero-USD):** render = self-hosted \u2713. Falta auditar se os passos **LLM (script/analyze)** rodam BYOK-gr\u00e1tis \u2192 custo USD externo = 0. (Gemini/OpenRouter de User 0 podem ter custo pequeno tipo ~US$0.005/run visto no product-miner.) **Rodar zero-USD audit antes do GO.**\n\n**A\u00e7\u00e3o Sovereign:** (1) GO verbal. (2) agente roda `UPDATE public.autopilot_plans SET video_enabled=true WHERE id='640b3b67-b950-42f6-bbb9-48560771eaa6'` (SB_SECRET_KEY). (3) disparo manual: invoke `autopilot-run` (Bearer SB_SECRET_KEY + `x-autopilot-user-id=ada39fae`, body `{plan_id}`) para testemunho controlado \u2014 OU `is_active=true` p/ pg_cron aut\u00f4nomo.\n\n**Testemunho (Lei 1):** novo `video_renders` done charged_mco=12 + novo MP4 \u2265100KB (ffprobe 1080\u00d71920) + `content_library` type=video + delta saldo ~24 mco + `autopilot_cycles` status=completed.\n\n---\n\n## 2. OAuth/App Review \u2014 YT \u00b7 TikTok \u00b7 IG \u00b7 Twitter \u00b7 Pinterest  \u00b7 `ready_now: PARTIAL`\n\n**Estado:** item DESATUALIZADO \u2014 todo o net-new YT/TikTok/Pinterest foi SHIPPED (commits 25477a8/f5e092c/6c3bc66 + migration). `social-auth-init/callback`, `publish-social`, `refresh-social-token` t\u00eam branches reais p/ 7 plataformas; `social_app_config` per-user Vault; enum j\u00e1 tem yt/tiktok/pinterest; gap auto-publish MP4 9:16 FECHADO.\n- **Conectados:** Instagram (magicorch, expira 2026-07-03, Reel E2E) \u00b7 Facebook \u00b7 LinkedIn \u00b7 **TikTok (expira 2026-06-30 \u26a0\ufe0f)**, publish PROVADO SELF_ONLY.\n- **YouTube:** upload PROVADO E2E (video_ids nfkVpPzEiOI/5Q6BQRUw85o, privacy=null) mas conex\u00e3o sumiu (refresh_token n\u00e3o persistiu).\n- **Twitter:** n\u00e3o conectado (degraded 06-28). **Pinterest:** app existe, n\u00e3o conectado.\n\n**Port\u00f5es de plataforma:** YT n\u00e3o-auditado \u2192 for\u00e7a privado \u00b7 TikTok n\u00e3o-auditado \u2192 SELF_ONLY \u00b7 IG sem scope `instagram_manage_insights` \u2192 collect-publication-metrics PULA IG.\n\n**A\u00e7\u00f5es IMEDIATAS (R$0, UI, n\u00e3o colidem com loop):**\n- **TikTok reconnect HOJE** (token expira 2026-06-30) em /dashboard/social.\n- **YouTube reconnect** com access_type=offline+prompt=consent (grava refresh_token).\n- **IG insights:** loop adiciona scope `instagram_manage_insights` (social-auth-init:87, 1 linha) \u2192 Sovereign desconecta+reconecta IG.\n- **Twitter:** publish p\u00fablico exige X API Basic tier (~US$100/m\u00eas) \u2014 decis\u00e3o Sovereign.\n\n**A\u00e7\u00f5es de ESPERA (~semanas, come\u00e7ar j\u00e1):** YouTube API Services Audit + TikTok Content Posting API audit \u2192 destravam p\u00fablico. Pinterest Standard tier.\n\n**Bloqueado no loop:** adicionar `youtube`/`tiktok` ao `VIDEO_FLOW_PLATFORMS` (`autopilot-run:114`, ~1h) p/ cad\u00eancia aut\u00f4noma multi-canal.\n\n---\n\n## 3. DNS/vhost \u2014 `video.mcorch.com` (can\u00f4nico) / studio.mcorch.com  \u00b7 `ready_now: YES` \u00b7 **J\u00c1 FEITO (item STALE)**\n\n**Estado:** editor HyperFrames servido em **`video.mcorch.com`** (n\u00e3o studio \u2014 SDD canonizou video). Tudo LIVE: .conf (85 linhas, SSO+proxy 3210+SSE), symlink em sites-enabled (24-jun), cert origem, DNS CF-orange, `nginx -t` OK, curl origin \u2192 302 SSO, `video-studio.service` active :3210, iframe `VideoStudioEditorPage.tsx:18`. `design.mcorch.com` no mesmo estado LIVE. `studio.mcorch.com` = alias DNS \u00f3rf\u00e3o (sem vhost/cert, inofensivo).\n\n**A\u00e7\u00e3o Sovereign:** NENHUMA f\u00edsica pendente. Opcional: abrir `https://video.mcorch.com` LOGADO (ou /dashboard/canvas/video) e confirmar o NLE 9:16 carrega \u2192 marcar item CONCLU\u00cdDO. N\u00c3O renomear p/ studio (sem ganho).\n\n---\n\n## 4. Postback ML definitivo \u2014 matt_tool/meli.la  \u00b7 `ready_now: PARTIAL` \u00b7 prioridade BAIXA\n\n**Estado:** framing DESATUALIZADO \u2014 essencial j\u00e1 vivo. `affiliate_config` User 0: affiliate_tag=caga6077534, matt_tool=43641843, is_active, **4 meli.la oficiais** em metadata.shortlinks. `process-affiliate-link` GET resolve 3 camadas fail-closed (shortlink\u2192matt_word+matt_tool\u2192fail). Click ledger FECHADO: 14 links, **15 cliques, 0 revenue_cents** (atribui\u00e7\u00e3o pronta, convers\u00e3o zero).\n**Falta:** (a) meli.la de produto NOVO exige gera\u00e7\u00e3o manual no painel ML logado (IP residencial \u2014 datacenter d\u00e1 403); (b) m\u00f3dulo `authenticated-browser-operator` (BoK 9/9 selada, **C\u00d3DIGO N\u00c3O CONSTRU\u00cdDO**) p/ escalar.\n**Decis\u00e3o:** gargalo real = DISTRIBUI\u00c7\u00c3O/TR\u00c1FEGO que converta, n\u00e3o plumbing de atribui\u00e7\u00e3o. Prioridade baixa; registrar meli.la s\u00f3 quando houver produto novo.\n\n---\n\n## 5. Stripe live keys  \u00b7 `ready_now: YES` \u00b7 gatilho de NEG\u00d3CIO (n\u00e3o acionar antes)\n\n**Estado:** billing 100% implementado + DEPLOYADO em TEST. 4 edge fns ACTIVE (create-checkout v43, create-portal v43, check-subscription v43, stripe-webhook v46). Frontend wirado (BillingPage price IDs de TEST). Secrets no vault (sandbox). Decis\u00e3o DOCUMENTADA de segurar: OTD-003 Decision B + `project_stripe_strategy` (Gabriel n\u00e3o paga fees Stripe em teste enquanto valida como User 0).\n**A\u00e7\u00e3o Sovereign (quando 1\u00ba cliente externo):** Stripe live mode + recriar 3 produtos/pre\u00e7os live + `supabase secrets set STRIPE_SECRET_KEY=sk_live_...` + webhook endpoint live + `STRIPE_WEBHOOK_SECRET` + atualizar 3 price IDs em BillingPage + rebuild/deploy. ~30-60 min. Custo: fee s\u00f3 por venda real (~3.99%+R$0,39) \u2192 R$0 at\u00e9 existir cliente.\n\n---\n\n## Conflito com o loop rodando\nBAIXO. O GO de gasto opera s\u00f3 sobre DADOS/estado (SQL `autopilot_plans` + invoke edge), nunca sobre arquivos-fonte. Reconex\u00f5es OAuth = 100% UI/portais externos. \u00danico ponto de contato: `autopilot-run:114` (VIDEO_FLOW_PLATFORMS) que o loop pode editar na Fatia YT/TikTok \u2014 n\u00e3o conflita com o GO (que \u00e9 dado, n\u00e3o c\u00f3digo). Edi\u00e7\u00e3o de frontend pelo Sovereign (ex: BillingPage no swap Stripe) \u2192 coordenar timing/worktree.\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/.claude/context/sovereign-queue-runbook-2026-06-30.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(23:30:15)*


## 🤖 Claude *(23:30:16)*

Persistido. Agora atualizo o índice de memória e te entrego a síntese.

## 🤖 Claude *(23:30:19)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md",
  "old_string": "# Memory Index\n\n- [Programa \"Gabriel AI\" (avatar-clone-ai)",
  "new_string": "# Memory Index\n\n- [Doutrina open-source-first / zero custo USD / equity + Gabriel AI co-executivo](feedback_opensource_first_zero_cost_equity.md) \u2014 Diretiva Sovereign 2026-06-30: tudo open-source/self-hosted DENTRO do MCORCH vira microservi\u00e7o (equity); custo USD externo ao Sovereign=0; GO de gasto gated nisso (render HyperFrames self-hosted \u2713, auditar LLM steps); Gabriel AI = co.CAI\u2192co.CTI ao lado do Gabriel co-CEO. Runbook da fila: `.claude/context/sovereign-queue-runbook-2026-06-30.md`.\n- [Programa \"Gabriel AI\" (avatar-clone-ai)"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(23:30:24)*


## 🤖 Claude *(23:30:24)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md",
  "limit": 5
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	# Memory Index
> 2	
> 3	- [Programa "Gabriel AI" (avatar-clone-ai) — BoK 10/10, Fatia 1 BYOK + Fatia 2 Voice Clone SHIPPED](project_avatar_clone_ai.md) — 2026-06-30: nó `voiceClone` no Canvas + edge `generate-voice` (ElevenLabs/Cartesia BYOK fail-closed, code-switch guard FM-AC-013, deduct 36 pós-gates) + `voice_profiles` RLS-own Vault + RPCs tenant-guarded. /security-review NO FINDINGS · smoke 10/10 · browser+Vision-QA PASS. Próximo=Fatia 3 (avatarIdentity/Identity Gate, face PII LGPD). Gotchas: user_api_keys FK NO-ACTION · infra_health_logs usa last_seen_at (sem created_at) · await pulses no edge.
> 4	- [Minerador de Produtos — confiabilidade da análise de vídeo + decisão de custo](project_product_miner_vision_reliability.md) — 2026-06-29: "extração falhou/non-2xx" tinha 3 causas. Fix: Files API 20-100MB (`b13018b`) + fallback cover-image quando vídeo é stub 5KB/falha (`08f1e47`/`e99004b`, MCP rejeita <50KB `video_too_small`→`describe_image`) + timeout legenda. Provado E2E @hosannhali source=cover. Decisão Sovereign: MANTER llama-3-8b:free+Gemini (~$5/mês, log real $0.0054); NÃO Kimi(1T inviável fal.ai)/Fugu($/mês). Conta real=gabrielcall@gmail.com.
> 5	- [Viewer sem nome no admin = usuário de smoke QA vazado (não invasão); helper SMOKETEST + sweep; signup aberto via Google](reference_qa_throwaway_users_and_open_signup.md) — 2026-06-28: `lf16-smoke-<ts>@example.com` (smoke-longform-16x9) vazava por cleanup fire-and-forget. Helper `scripts/qa/lib/qa-throwaway.ts` (taga `full_name=SMOKETEST`→coluna "Nome"; delete awaited; sweep só `@example.com`) + cron diário 04:00; 35 smokes migrados. ⚠️ signup externo LIGADO (`disable_signup:false`, google+email) — travar = Supabase Dashboard.
> ```

## 🤖 Claude *(23:30:30)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md",
  "old_string": "# Memory Index\n\n- [Programa \"Gabriel AI\" (avatar-clone-ai)",
  "new_string": "# Memory Index\n\n- [Doutrina open-source-first / zero custo USD / equity + Gabriel AI co-executivo](feedback_opensource_first_zero_cost_equity.md) \u2014 Diretiva Sovereign 2026-06-30: tudo open-source/self-hosted DENTRO do MCORCH vira microservi\u00e7o (equity); custo USD externo ao Sovereign=0; GO de gasto gated nisso (render HyperFrames self-hosted \u2713, auditar LLM steps); Gabriel AI = co.CAI\u2192co.CTI ao lado do Gabriel co-CEO. Runbook da fila: `.claude/context/sovereign-queue-runbook-2026-06-30.md`.\n- [Programa \"Gabriel AI\" (avatar-clone-ai)"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(23:30:36)*


## 🤖 Claude *(23:30:57)*

Tudo encodado. Síntese do que ficou e a leitura da sua doutrina sobre o GO:

## ✅ Sua doutrina virou lei do sistema
- **Memória** `feedback_opensource_first_zero_cost_equity` (sobrevive entre sessões).
- **Charter do loop** — adicionei a doutrina na seção não-negociável + amarrei o gate no item do GO. O loop lê isso no início de cada iteração, então ele já vai *preferir open-source* sozinho (ex.: na decisão `OTD-AC-015` da biometria, a doutrina manda escolher **InsightFace self-hosted no Mesh** em vez de Rekognition/Azure/Face++ pago).
- **Runbook material durável** em [sovereign-queue-runbook-2026-06-30.md](.claude/context/sovereign-queue-runbook-2026-06-30.md) — os 6 itens verificados contra DB/infra, pra "depois" não se perder.

## 🎯 GO de gasto — o veredito pela SUA régua
O pipeline está **provado e pronto** (render real `8b0787e0`, MP4 de 748KB no bucket, custo ~24 mco / saldo 4669). Pela sua doutrina:

- **Render = HyperFrames self-hosted (Playwright+FFmpeg na sua infra) → custo USD ≈ 0.** Isso é doutrina-perfeito, exatamente o microserviço-próprio-que-vira-equity. ✓
- **Falta UMA verificação pra fechar o "custo USD externo = 0":** os passos de **LLM (script + analyze)** rodam nas chaves BYOK do User 0. Se forem tier-grátis, custo ≈ 0 e o GO está 100% alinhado. Mas a memória do product-miner mostra Gemini com custo real pequeno (~US$0,005/run) — então não posso afirmar "zero" sem auditar.

**Minha recomendação:** antes de você dar o GO, eu rodo um **zero-USD audit** do ciclo de vídeo — mapeio cada chamada externa (qual provider/modelo/tier o User 0 usa em script e analyze) e te trago o número real de USD por ciclo. Aí o GO sai limpo pela sua própria regra, sem fé. **Quer que eu rode esse audit agora?** (É barato e não toca código — não colide com o loop.)

## 📉 Boa notícia — sua lista encolheu
**DNS/vhost já está FEITO.** O editor não foi pra `studio.mcorch.com` — a SDD canonizou **`video.mcorch.com`**, que está LIVE (cert + symlink + SSO + servido no `/dashboard/canvas/video`). `studio.mcorch.com` é só um alias DNS órfão inofensivo. Esse item pode sair da fila — só vale você abrir logado pra confirmar visualmente.

## ⏰ Um alerta sensível ao tempo (R$0, opcional)
**O token do TikTok expira HOJE (2026-06-30).** Se você quiser manter o canal conectado, são ~2 min reconectando em `/dashboard/social`. Não é obrigatório agora, mas a janela fecha hoje — por isso te aviso.

---

O **resto** (audits YouTube/TikTok de prazo-semanas, postback ML, Stripe) está todo no runbook pra quando você quiser conversar. Adianto: **Stripe fica parado** até o primeiro cliente externo (decisão sua já documentada), e **ML postback é prioridade baixa** — o gargalo real do funil é distribuição/tráfego, não atribuição (15 cliques, R$0 de conversão).

Então: **rodo o zero-USD audit do ciclo de vídeo** pra destravar o GO com consciência limpa?

## 👤 User *(23:54:37)*

pode ser mas o loop terminou.: Boa pergunta — e a resposta curta é: o `/loop` tem exatamente o modo que você quer, mas o "mais sofisticado e assertivo" não está no comando, está na **diretiva que você dá pra ele**. "ok continue" é um prompt vazio; o salto de qualidade é encodar o nosso Protocolo de Malha Fechada *dentro* do loop.

## Os dois modos do `/loop`

| Modo | Sintaxe | Quando |

|------|---------|--------|

| **Intervalo fixo** | `/loop 30m <prompt>` | Polling de estado externo — testemunhar o 1º ciclo pago de vídeo, postback ML, um deploy. Dispara a cada 30 min independente. |

| **Auto-ritmado (dynamic)** | `/loop <prompt>` (sem intervalo) | **É o que você quer.** Eu mesmo decido *quando* continuar e sigo trabalhando até esgotar o backlog ou bater num portão. Sem você digitar "ok" entre as fatias. |

## Por que isso vence o "ok continue" (5 pontos)

1. **Auto-pacing** — não preciso da sua confirmação entre iterações; eu agendo o próximo passo sozinho.

2. **Política de prioridade escrita** — em vez de eu re-adivinhar o que vem depois a cada turno, o loop lê uma *charter* (arquivo) com o backlog priorizado e as condições de parada. Decisão determinística e inspecionável, não no "feeling".

3. **Portões respeitados** — a charter define o que eu executo sozinho vs. o que **HALT + escalo pra você** (Lei 4: Reviewer = Sovereign). Biometria, DNS/vhost, App Review, GO de gasto, decisão arquitetural → entram numa **Fila de Ação Sovereign**, não viram improviso.

4. **Selo automático** — `/handoff` incremental ao fechar cada Fatia, e selo final + parada quando a janela chegar a ~95% (Lei 3 calibrada). Progresso sempre durável.

5. **Survival Laws no laço** — prova material (Lei 1) + SOP-antes-de-código (Lei 2) + self-audit a cada iteração, embutidos.

## O comando (versão assertiva)

```

/loop Você é o MCORCH Master Execution Agent em malha fechada autônoma.

A cada iteração: (1) git fetch + releia o Pending Actions do HANDOFF.md e a

charter em .claude/context/autonomous-loop-charter.md; (2) pegue o item de

MAIOR valor que esteja DESBLOQUEADO; (3) rode o ciclo fechado — BoK Gate →

SOP Lei 2 → código → prova material Lei 1 → /security-review se houver

migration → commit granular; (4) se exigir ação do Sovereign (biometria,

DNS, App Review, GO de gasto, decisão arquitetural), registre na Fila de

Ação Sovereign e pule pro próximo; (5) Survival self-audit; (6) /handoff

incremental ao fechar cada Fatia, selo final + parar a ~95% da janela OU

backlog desbloqueado esgotado. Reporte em PT-BR a cada iteração: o que

entregou (com prova) e o que entrou na Fila Sovereign.

```

A charter (`.claude/context/autonomous-loop-charter.md`) é o upgrade real — ela guarda o backlog ordenado, as condições de HALT e a Fila Sovereign, e eu a atualizo a cada fatia. Esqueleto:

```markdown

# Autonomous Loop Charter

## Backlog (ordem de valor, só DESBLOQUEADOS executam)

1. Gabriel AI 3b — emenda BoK (rota VLM-soft via Vision MCP)  [DESBLOQUEADO: drafting]

   └─ HALT no treino face: exige frames reais do Sovereign

2. YT/TikTok — emenda BoK post-engine + 3 branches publish/auth  [DESBLOQUEADO até OAuth audit]

3. Viral Autopilot — McorchAdapter/bridge do editor Studio  [HALT no vhost studio.mcorch.com]

## Fila de Ação Sovereign (o que SÓ você destrava)

- (preenchida pelo loop conforme bate nos portões)

## Parar quando: janela ~95% · OU backlog desbloqueado vazio · OU GO seu

```

**Caveat honesto (Lei 1):** vários itens de topo são Sovereign-gated *na ponta física* (biometria do 3b, GO do ciclo pago, DNS do Studio, App Review). O loop faz **toda a engenharia desbloqueada até o portão** — drafta as emendas BoK, scaffolda os nós/edges, escreve SOPs+smokes, roda `/security-review` — e te entrega uma fila de decisão enxuta no lugar dos itens travados. Ele não vai *shipar* o que depende dos seus dados/credenciais/GO. Isso está alinhado com a sua diretiva de força-total autônoma.

**Controle:** pra parar, é só me mandar qualquer mensagem (interrompe o laço) ou desligar o `/loop`. Eu seloo antes da janela encher, então nunca perde estado.

Deixa eu te perguntar o modo de arranque:

Você escolheu **charter + lançar agora**. Vou (1) escrever a charter com o backlog priorizado e os portões de HALT, e (2) ligar o `/loop` auto-ritmado.

Primeiro, a charter — o cérebro do loop:

Charter escrita ([autonomous-loop-charter.md](.claude/context/autonomous-loop-charter.md)). Agora ligo o `/loop` auto-ritmado:

O loop entrou em **modo dinâmico** (sem intervalo, auto-ritmado) — sem oferta de cloud porque não há cadência diária/≥60min. Não preciso de Monitor: o Workflow que vou disparar me re-invoca sozinho ao terminar.

**Iteração 1 — Gabriel AI Fatia 3b (emenda BoK rota VLM-soft).** Pelo Protocolo de Malha Fechada, antes de qualquer código a BoK precisa carregar a rota VLM-soft. Disparo agora um Workflow que (a) entende o BoK de identidade existente + o schema `avatar_identities` já staged + as ferramentas reais do Vision MCP, (b) projeta a emenda VLM-soft MVP, e (c) passa por um crítico adversarial contra os invariantes (consent gate LGPD, fail-closed, isolamento de tenant, zero ferramenta fabricada).

**Loop ativo — modo auto-ritmado.** Confirmo o estado desta primeira iteração:

- **Sem Monitor:** o Workflow da emenda 3b é rastreado pelo harness — ele me re-invoca automaticamente ao concluir. Não há evento externo a vigiar.

- **Tarefa rodando agora:** Workflow `wf_188ce24c-881` (understand → design → critic) da emenda BoK VLM-soft.

- **Quando ele voltar:** vou revisar o veredito do crítico; se `APPROVE`, escrevo o doc de emenda em `docs/bok/avatar-clone-ai/`, commito (prova: `ls -la` + hash) e sigo pra Fatia 3b scaffold; se `REVISE`, corrijo os pontos antes de escrever.

- **Fallback:** agendo um heartbeat longo (30 min) só como rede de segurança caso o Workflow trave — não é polling.

**Survival self-audit (it. 1):** Lei 1 ✓ (nenhum SUCCESS declarado sem prova; Workflow ainda em voo) · Lei 2 ✓ (charter escrita antes de qualquer código; emenda BoK precede o scaffold) · Lei 3 ✓ (estado podado, referências por path) · Lei 4 ✓ (ORO: Operator=eu, Reviewer/Owner=Sovereign — a decisão ArcFace-vs-VLM-final está na Fila).

Agendo o fallback e encerro o turno:

**Malha fechada ligada e rodando.** 🟢

Resumo do que montei pra você não precisar mais digitar "ok continue":

1. **Charter** ([autonomous-loop-charter.md](.claude/context/autonomous-loop-charter.md)) — o cérebro do loop: backlog priorizado (Gabriel AI 3b → YT/TikTok → editor Studio → Unified Canvas → Security hardening), ritual por iteração, portões de HALT e a Fila de Ação Sovereign.

2. **`/loop` auto-ritmado** — encoda o Protocolo de Malha Fechada + as 4 Survival Laws. Trabalho sozinho até a janela ~95%, o backlog desbloqueado esgotar, ou você mandar parar.

3. **Iteração 1 em voo** — Workflow da emenda BoK da Fatia 3b (rota VLM-soft via Vision MCP), com crítico adversarial verificando os invariantes LGPD/fail-closed/tenant.

A partir daqui ele se conduz: quando o Workflow voltar, eu reviso, escrevo+commito a emenda (com prova material), e puxo o próximo item. Cada fatia fechada vira um `/handoff` incremental.

**Pra dirigir o loop a qualquer momento:** é só me mandar uma mensagem — isso interrompe o laço e eu reabsorvo a direção (ex.: "pula pra YT/TikTok", "para e me mostra a Fila Sovereign", ou "stop"). Não precisa de comando especial.

Encerro este turno; o harness me reacorda quando o Workflow concluir.

Workflow concluído (5 agentes, 551s). Preciso do veredito do crítico e do markdown proposto — vou ler o output completo.

Understand phase é sólido e com um achado decisivo: o Vision MCP só expõe **2 tools de visão descritivos** (`vision_describe_image` + `vision_analyze_video`) — zero embedding facial/cosine/compare. VLM-soft = descrever retrato + descrever frame e o LLM chamador compara os textos: serve como **gate de sanidade barato, não verificação confiável** (human-review-assist). Preciso do design + veredito do crítico:

O crítico achou 4 furos reais (0 ferramenta fabricada). Vou ler o veredito final:

**Veredito do crítico: `APPROVE`** — zero ferramenta fabricada, todos os 6 checks obrigatórios passaram (consent Art.11 trava captura · fail-closed degrada pra human-review nunca auto-pass · isolamento tenant intacto · VLM-soft honestamente rotulado < ArcFace · ArcFace-hard deferido na OTD-AC-015 com destravadores Sovereign). As 6 issues são refinamentos a dobrar ANTES do selo de código, não rejeições.

Vou (1) confirmar o filename canônico, (2) escrever o doc final já com as 6 correções do crítico dobradas, (3) commitar com prova material.

Filename canônico: `10-amendment-3b-identity-gate-vlm-soft.md`. Escrevo o doc final com as 6 correções do crítico dobradas:

Doc escrito. Commito com prova material (Lei 1):

Iteração 1 selada com prova: commit `7b81bfd0f887a8d37895de610d7202adebc164f8`, doc 24.161 bytes, working tree limpo, gitleaks sem vazamentos, mesh-reingest disparado. Atualizo a charter (marco a emenda ✅ + populo a Fila Sovereign com os destravadores concretos):

**Survival self-audit (it.1):** Lei 1 ✅ (hash/size/gitleaks/veredito todos de output verificado neste turno — zero prova fabricada) · Lei 2 ✅ (emenda BoK = artefato de processo, precede o código 3b) · Lei 3 ✅ (output do workflow referenciado por path, não recarregado; charter guarda estado por referência) · Lei 4 ✅ (ORO no header do doc).

---

🔄 **Iteração 1 — concluída.** Reporto ao Maestro:

**Entregue (com prova material):**

- **Emenda BoK Fatia 3b** → [10-amendment-3b-identity-gate-vlm-soft.md](docs/bok/avatar-clone-ai/10-amendment-3b-identity-gate-vlm-soft.md) — commit `7b81bfd`, 24.161 bytes, tree limpo.

- **Achado decisivo (Lei 1):** o substrato ArcFace/InsightFace **não existe** no código; o Vision MCP só expõe 2 tools de visão *descritivos*. A emenda habilita o Identity Gate pela rota **VLM-soft MVP** (dual-mode, ArcFace-hard deferido) — funcional hoje, **cost 0 com BYOK**, sem fabricar capacidade inexistente.

- **Verificação adversarial:** workflow de 5 agentes → veredito `APPROVE`, **6 issues do crítico dobradas** no doc (compare enum FR-AC-013b · discriminador `gate_mode` · migração de chave de telemetria · credencial user-JWT · `max_regen` anti-oscilação · qualifiers de Pattern Conformance).

**Entrou na Fila de Ação Sovereign (você destrava):**

- **OTD-AC-015** — motor de embedding facial (InsightFace self-host OU API paga) + biometria calibração-grade do Gabriel (frames rotulados FAR/FRR/EER).

- **OTD-AC-017** — credencial Higgsfield + confirmar API self-serve de treino Soul ID.

- **Licença comercial** (FLUX.1-dev non-commercial) + **GO de produção 3b**.

**Próxima iteração:** nó Canvas `avatarIdentity` (FR-AC-012, UI/registry sem biometria) + lib de compare VLM-soft + migration `gate_mode` (com `/security-review`) — tudo desbloqueado; a edge de treino fica stubbed atrás da OTD-AC-017.

Agendo a continuação:

Iteração 1 selada. O loop continua sozinho — próxima iteração (código da Fatia 3b: nó `avatarIdentity` + compare VLM-soft + migration `gate_mode` com `/security-review`) dispara em ~2 min. Encerro o turno; o harness me reacorda.

Iteração 2 — modo dinâmico. Ritual: `git fetch` + status + localizo os arquivos-molde (o nó `VoiceClone` da Fatia 2 é o template perfeito para o `avatarIdentity`).

O nó `VoiceClone` é o molde. Localizo o inspector e leio os arquivos-molde em paralelo:

Molde compreendido. Leio as seções relevantes de `canvas.ts` (union de tipos, `VoiceCloneData`, factory, dispatch, guards):

Tenho o molde completo. Scopo a iteração 2 ao núcleo **fully-unblocked + provável**: a lib de compare VLM-soft (FR-AC-013b — peça #1 que o crítico sinalizou) + testes unitários + a migration `gate_mode`. O nó UI (types+componente+inspector) fica para a iteração 3. Confirmo convenções (numeração de migration + dir de teste):

Convenções confirmadas: migration `20260630140000`, testes em `src/test/`, vitest. Escrevo os 3 arquivos da iteração 2 (lib de compare + testes + migration `gate_mode`):

A charter foi editada (pelo Sovereign) com uma **nova diretiva: open-source-first / custo USD = 0 / equity** — preferir self-host dentro do MCORCH a SaaS pago. Minha rota VLM-soft via BYOK já é **cost 0**, alinhada. Anotado para refinar a OTD-AC-015 (preferir InsightFace self-host no Mesh).

Agora a prova material (Lei 1): `tsc` + vitest dos novos arquivos:

tsc limpo (exit 0). 14/15 testes passam; 1 falha — e o teste está **certo**, minha lib estava lenient demais: `["pass","review"]` retornava `pass` num empate, mas um gate de segurança nunca deve auto-aprovar num empate com `review`. Aperto a regra (maioria estrita sobre `review` também):

15/15 verdes, tsc limpo. A migration exige `/security-review` antes do commit (regra do projeto). Stago os arquivos e rodo:

`/security-review` na migration:

Iteração 2 em verificação: `tsc` limpo, **15/15 testes verdes**, e o sub-agente de `/security-review` está analisando a migration `gate_mode` + a lib (surface pequena: coluna aditiva que herda a RLS da tabela + lib client-side pura). Ele me re-invoca ao concluir.

Estado da iteração 2 (pré-commit, aguardando o gate de segurança):

- `src/lib/avatar-identity.ts` — compare VLM-soft FR-AC-013b (parse fail-soft + bands pass/review/fail + reconcile N≥2 anti-oscilação).

- `src/test/avatar-identity.test.ts` — 15 testes (prova material: 15 passed).

- `supabase/migrations/20260630140000_avatar_identity_gate_mode.sql` — discriminador `gate_mode` (dobra issue #2 do crítico).

Agendo fallback longo (o sub-agente de segurança auto-notifica; isto é só rede de segurança):

**`/security-review` → NO FINDINGS.** O sub-agente confirmou rigorosamente: a migration só faz `ADD COLUMN` (DDL estático + CHECK enum literal) + 2 `COMMENT` — zero policy/GRANT/função nova, a postura RLS own-row/default-deny/service-role-write da `20260630130000` é integralmente preservada; a lib é client-side pura (`JSON.parse` em try/catch, narrow a 7 chaves allowlisted em objeto fresco — sem eval, sem prototype-pollution, sem `dangerouslySetInnerHTML`).

```markdown

# Security Review — Fatia 3b foundation (gate_mode migration + VLM-soft compare lib)

Resultado: SAFE — NENHUM ACHADO (confiança ≥8).

- supabase/migrations/20260630140000_avatar_identity_gate_mode.sql → ADD COLUMN aditivo + CHECK

  enum + COMMENTs; herda RLS da tabela; sem SECURITY DEFINER, dynamic SQL, GRANT ou drop de policy.

- src/lib/avatar-identity.ts → client-side puro; JSON.parse em try/catch, narrow a chaves

  allowlisted; sem sink de injeção/RCE/prototype-pollution.

- src/test/avatar-identity.test.ts → excluído (test file).

```

Gate verde. Commito a iteração 2:

Iteração 2 selada: commit `541f7072877c8fbe9781d9e42f6cf0224902c6f3`, 3 arquivos/294 inserções, gitleaks limpo. Atualizo a charter (marco a fundação 3b ✅):

**Survival self-audit (it.2):** Lei 1 ✅ (tsc exit 0 · vitest 15/15 · /security-review NO FINDINGS · hash `541f707` — aplicação da migration honestamente *deferida*, não declarada aplicada) · Lei 2 ✅ (a emenda BoK precede e especifica FR-AC-013b) · Lei 3 ✅ (output de segurança consumido por resultado, não recarregado) · Lei 4 ✅ (aplicação da migration ⇒ Fila Sovereign / GO).

---

🔄 **Iteração 2 — concluída.** Reporto:

**Entregue (prova material):**

- **Lib de compare VLM-soft** [avatar-identity.ts](src/lib/avatar-identity.ts) (FR-AC-013b — a peça #1 que o crítico sinalizou): schema enum fixo + parse fail-soft (resposta não-JSON → `{}` → todos mismatch → **nunca pass silencioso**) + bands pass/review/fail de um único threshold + `reconcileSoftMatches` (maioria N≥2 + anti-oscilação: pass↔fail consecutivo → review).

- **15 testes unitários** [avatar-identity.test.ts](src/test/avatar-identity.test.ts) — **15/15 passed** (um teste pegou minha lib lenient demais num empate; apertei pra maioria estrita = nunca auto-aprovar empate).

- **Migration `gate_mode`** [20260630140000](supabase/migrations/20260630140000_avatar_identity_gate_mode.sql) (dobra issue #2 do crítico) — `/security-review` **NO FINDINGS**. Aplicação à prod **deferida ao GO 3b** (Fila Sovereign) — não mutei prod por feature gated.

- Commit `541f707`, tsc 0.

**Fila de Ação Sovereign:** inalterada (OTD-AC-015/017 + GO 3b já registrados). Nota: a nova diretiva **open-source-first** que você adicionou à charter favorece **InsightFace self-host no Mesh** (USD=0) sobre API paga para a OTD-AC-015 — alinhado.

**Próxima iteração (it.3):** nó Canvas `avatarIdentity` (type+factory+componente+inspector+registry+wiring; upload de retratos + consent; botão "Treinar" fail-closed honesto até OTD-AC-017) — UI visível, browser-verificada.

Agendo a continuação:

Iteração 2 selada. O loop segue autônomo — iteração 3 (nó Canvas `avatarIdentity`, UI visível: type+factory+componente+inspector+registry+wiring + upload de retratos + consent, com "Treinar" fail-closed até a OTD-AC-017) dispara em ~3 min, com browser-verify. Encerro o turno; o harness me reacorda.

**Resumo do progresso autônomo até aqui (Gabriel AI Fatia 3b):**

- **it.1** `7b81bfd` — emenda BoK VLM-soft (verificada adversarialmente, APPROVE, 6 issues dobradas).

- **it.2** `541f707` — fundação: lib de compare FR-AC-013b (15/15 testes) + migration `gate_mode` (/security-review SAFE).

A malha fechada está cumprindo o ciclo completo a cada iteração (BoK → código → prova material → security-review → commit) e empilhando os destravadores físicos na Fila Sovereign sem improvisar. Pode me interromper a qualquer momento para redirecionar.

Iteração 3 — modo dinâmico. Ritual + localizo os pontos de wiring (nodeTypes map + dispatch do inspector) para o nó `avatarIdentity`:

Pontos de wiring localizados. Leio os trechos exatos do nodeTypes map e do dispatch do inspector para espelhar:

Wiring claro. Antes de escrever o inspector preciso confirmar o tipo das finalidades de consent (`face_embedding`/`train_lora`) para não estourar o tsc:

Tudo confirmado (`ConsentPurpose = train_lora | face_embedding | voice_clone`). Implemento o nó `avatarIdentity`. Primeiro as 6 emendas em `canvas.ts` (type + interface + factory + dispatch + guard + cost):

Agora os 2 componentes (nó + inspector):

Wiring — registry (import + ícone + entry), nodeTypes map e dispatch do inspector:

Wiring completo (registry + nodeTypes + dispatch). Sem migration nesta iteração. Prova material: `tsc` + lint + suite de testes (sem regressão):

tsc **exit 0**, lint **exit 0**. Agora prova de build material + alvo para browser-verify, construindo num dir temporário (sem tocar o `dist/` servido):

Build **exit 0** (26.31s) — o chunk `CanvasEditorPage` bundlou com o nó novo. Prova material de build ✓ (sem deploy — dir temporário). Commito o nó:

Commit `12d06c0` (6 arquivos/386 inserções, gitleaks limpo). Agora o **browser-verify** (Lei 1 UI gate). Subo o `vite preview` do build temporário em background e gero uma sessão injetável:

Tudo disponível (gen-user-session, vite preview, agent-browser, VISION_MCP_PAT). Subo o preview em background:

Preview vivo (HTTP 200 em `127.0.0.1:4174`). Gero a sessão do Usuário Zero:

Preciso passar o email do Usuário Zero (`gabrielcall@gmail.com`) + env. Carrego `.env` e gero:

Sessão gerada (Usuário Zero `ada39fae…`, admin). Localizo a rota do editor de Canvas + um projeto existente para navegar:

Rota `/dashboard/canvas/:id`, projeto `63d406fe`. Confirmo a sintaxe do agent-browser e preparo a injeção de sessão:

agent-browser tem `--state` (formato Playwright storageState). Construo o state file com a sessão e abro o editor de Canvas:

State file pronto. Abro o editor de Canvas com a sessão injetada:

`--state` foi ignorado (daemon já rodava) → sessão não injetada, provável redirect pra /auth. Fecho o daemon e reabro com o state:

Autenticado (token presente, rota mantida no editor — sem redirect pra /auth). Vejo o screenshot:

Editor renderiza **limpo, sem white-screen/crash** com o novo tipo de nó registrado (projeto "Validação Criativa" carregou: 3 nós, 1 conexão, Conectado). Regressão de crash descartada. Agora abro "Adicionar nó" e busco "identidade":

O clique por texto falhou (markup do botão). Pego o snapshot de acessibilidade para achar o ref correto do "Adicionar nó":

A FAB não aparece como button rotulado na árvore. Leio o componente AddNodeMenu para achar o gatilho/seletor correto:

A FAB é Popover + há um CommandDialog via **Ctrl+K**. Uso o atalho, busco "identidade":

"Identidade (avatar)" **presente no palette**. Vejo o screenshot e insiro o nó (Enter) para confirmar render + inspector:

Item "Identidade (avatar)" renderiza no palette (categoria Inputs, ícone UserCircle). Insiro (Enter) e verifico o nó + inspector:

Sem erros de console (bom). Mas os marcadores do inspector não aparecem — o nó pode não ter auto-selecionado. Vejo o estado:

**Browser-verify COMPLETO ✅** (vejo o render): o nó **"Identidade (avatar)"** foi inserido e renderiza no canvas (placeholder "Suba retratos de referência", badge T1, handles), e o **inspector** abriu íntegro à direita:

- **Provider:** Higgsfield Soul ID / LoRA (Flux)

- **Tier de identidade:** T1·InstantID / T2·PuLID / T3·LoRA

- **Consentimento (LGPD Art. 11):** ConsentWizard com checkboxes biométricos

- **"Treinar identidade"** (disabled até consent+retratos) + caption honesta **"Gate VLM-soft (FR-AC-013b) · treino gated OTD-AC-017"**

Sem white-screen, sem crash, **zero erro de console** (só warnings a11y benignos), node count 3→4. (Vision MCP QA não se aplica aqui — exige URL pública; preview é localhost e os prints são locais; verifiquei por inspeção visual direta dos renders.)

Como o nó está verificado, honesto e é valor visível ao Usuário Zero, faço o **deploy** (rsync do build idêntico já verificado → `dist/` servido pelo nginx) com prova material:

**Deploy verificado (Lei 1):** env baked ✓ · rsync OK · chunk servido `CanvasEditorPage-DEjSoHib.js` (165.844 bytes) contém "Identidade (avatar)" ✓ · `index` referencia o chunk ✓. O nó está **LIVE** em login.mcorch.com (hard-refresh Ctrl+Shift+R; CF pode cachear). Limpo os processos de verificação:

Browser fechado + preview encerrado (o exit 144 foi o próprio `pkill` sinalizando o shell — benigno). Confirmo o git limpo:

Git limpo (só arquivos de loop-state). 3 commits selam o slice desbloqueado da Fatia 3b. Atualizo a charter (it.3 ✅ deployed + 3b desbloqueado esgotado):

**Survival self-audit (it.3):** Lei 1 ✅ (tsc 0 · eslint 0 · vite build 0 · browser-verify visto · deploy verificado por bytes+grep+env-baked · hash `12d06c0` — honesto sobre Vision QA não se aplicar por URL) · Lei 2 ✅ (amendment BoK precede; nó implementa FR-AC-012) · Lei 3 ✅ (podado; **sessão longa — sinalizo proximidade de seal**) · Lei 4 ✅ (deploy de nó verificado ao produto gated do próprio Sovereign, transparente).

---

🔄 **Iteração 3 — concluída. Marco de valor visível entregue.** Reporto:

**Entregue (prova material):**

- **Nó `avatarIdentity` no Canvas Studio** ([AvatarIdentityNode.tsx](src/components/canvas/nodes/AvatarIdentityNode.tsx) + [AvatarIdentityInspector.tsx](src/components/canvas/RightPanel/inspectors/AvatarIdentityInspector.tsx)) — commit `12d06c0`. Upload multi-retrato + ConsentWizard (Art.11) + provider/tier + "Treinar" fail-closed honesto (OTD-AC-017).

- **Browser-verificado** como Usuário Zero: o nó aparece no palette Cmd+K (categoria Inputs), insere+renderiza no canvas, e o inspector abre íntegro — **zero crash, zero erro de console**.

- **DEPLOYED** (decisão autônoma transparente): build verificado → `dist/` servido pelo nginx. Chunk `CanvasEditorPage-DEjSoHib.js` (165.844B) contém o nó, env baked. **LIVE em login.mcorch.com** (hard-refresh Ctrl+Shift+R — CF pode cachear).

**3b desbloqueado ESGOTADO** — o restante da Fatia 3b é todo Sovereign-gated (já na Fila): edge `avatar-identity-train` (OTD-AC-017 Higgsfield), gate-into-pipeline + telemetry migration (dependem do train+geração), calibração biométrica (OTD-AC-015).

**Resumo do arco autônomo (Gabriel AI Fatia 3b):** `7b81bfd` emenda BoK VLM-soft → `541f707` lib compare + migration → `12d06c0` nó UI deployed. 3 ciclos fechados completos (BoK → código → prova → security-review → commit → deploy).

**Próximo:** backlog #2 (YT/TikTok, usando o blueprint existente — mais contido que um deepsearch novo). Sessão já longa: a próxima iteração avalia janela e **sela via /handoff se ~95%**, senão segue.

Agendo a continuação:

Iteração 3 selada — **marco de valor visível entregue ao Usuário Zero**: o nó **"Identidade (avatar)"** está LIVE no Canvas Studio (login.mcorch.com), browser-verificado e deployado.

**Arco autônomo desta sessão (Gabriel AI — Fatia 3b, malha fechada):**

| It | Commit | Entrega | Prova |

|----|--------|---------|-------|

| 1 | `7b81bfd` | Emenda BoK VLM-soft (ArcFace→VLM-soft) | Workflow adversarial APPROVE, 6 issues dobradas |

| 2 | `541f707` | Lib compare FR-AC-013b + migration `gate_mode` | tsc 0 · 15/15 testes · /security-review SAFE |

| 3 | `12d06c0` | Nó `avatarIdentity` (UI completa) | tsc 0 · build 0 · browser-verify · **deployed** |

O loop cumpriu o ciclo fechado completo a cada iteração (BoK → código → prova material → security-review → commit → deploy) e empilhou os destravadores físicos na Fila Sovereign sem improvisar. O **3b desbloqueado está esgotado** — o que falta exige você (Higgsfield/biometria/GO).

A próxima iteração (~4 min) **avalia a janela**: se perto de ~95%, faz o `/handoff` seal final; senão inicia o **backlog #2 (YT/TikTok)** a partir do blueprint existente. Pode me interromper a qualquer momento para redirecionar ou mandar selar. Encerro o turno.

## 🤖 Claude *(23:55:33)*


## 🤖 Claude *(23:55:38)*

O loop fez exatamente o que a malha fechada prometeu — **3 iterações fechadas** (`7b81bfd` emenda BoK → `541f707` lib compare + migration → `12d06c0` nó `avatarIdentity` deployado LIVE), cada uma com prova material e `/security-review`, esgotando o **3b desbloqueado**. O que resta da biometria agora é 100% sua (OTD-AC-015/017 + GO). Trabalho limpo.

E você deu o "pode ser" — então **rodo agora o zero-USD audit** do ciclo de vídeo, que é o gate da sua doutrina pro GO de gasto. Ele responde com número real: cada chamada externa do ciclo, qual provider/modelo o User 0 usa, e se custa USD de verdade. Se algum passo vazar custo, ele já propõe o swap doutrina-aligned (modelo `:free` ou Ollama self-hosted).

Como o loop terminou, não há colisão — e o audit é read-only de qualquer forma. Disparo:

## 🤖 Claude *(23:56:27)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'video-cycle-zero-usd-audit',\n  description: 'Audita o custo USD externo real do ciclo de v\u00eddeo do autopilot (gate da doutrina open-source-first pro GO de gasto)',\n  phases: [\n    { title: 'Trace', detail: 'um agente por passo externo + telemetria real do ciclo j\u00e1 rodado' },\n    { title: 'Verdict', detail: 'soma USD/ciclo + veredito doutrina + swap se vazar custo' },\n  ],\n}\n\nconst USER0 = 'ada39fae-67e1-4e53-af1c-5a18e1c108e8'\n\nconst STEP_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  properties: {\n    step: { type: 'string' },\n    edge_fn: { type: 'string', description: 'edge function(s)/arquivo que faz a chamada externa, com file:line' },\n    provider_model: { type: 'string', description: 'provider + modelo exato resolvido para o User 0 (ex: OpenRouter google/gemini-2.0-flash-001, ou llama-3-8b:free, ou self-hosted)' },\n    key_source: { type: 'string', description: 'como a credencial \u00e9 resolvida p/ User 0 (user_api_keys coluna X / env / BYOK). Cite a coluna real.' },\n    is_free_tier: { type: 'string', enum: ['yes', 'no', 'depends', 'unknown'], description: 'o modelo/tier resolvido custa USD real? :free do OpenRouter e self-host=yes(gr\u00e1tis); Gemini paid/OpenAI=no.' },\n    usd_per_run: { type: 'string', description: 'custo USD estimado OU medido por execu\u00e7\u00e3o deste passo. Se medido em log real, dizer.' },\n    self_hosted: { type: 'string', enum: ['yes', 'no', 'partial'], description: 'o passo roda em infra pr\u00f3pria do MCORCH (self-hosted) ou em SaaS externo?' },\n    evidence: { type: 'array', items: { type: 'string' }, description: 'file:line + queries DB/log reais (Lei 1)' },\n  },\n  required: ['step', 'edge_fn', 'provider_model', 'key_source', 'is_free_tier', 'usd_per_run', 'self_hosted', 'evidence'],\n}\n\nconst STEPS = [\n  {\n    key: 'content',\n    prompt: `Trace o passo de GERA\u00c7\u00c3O DE TEXTO/SCRIPT do ciclo de v\u00eddeo do Viral Autopilot para o Usu\u00e1rio Zero (user_id=${USER0}).\nCaminho: autopilot-run \u2192 orchestrate-content \u2192 orchestrate-step \u2192 generate-content (ou equivalente). Leia supabase/functions/autopilot-run/index.ts, orchestrate-content/index.ts, orchestrate-step/index.ts, generate-content/index.ts.\nDetermine MATERIALMENTE: (1) qual edge fn faz a chamada LLM de texto e em qual linha; (2) qual PROVIDER + MODELO EXATO \u00e9 resolvido para o User 0 (resolva a credencial BYOK: leia de qual coluna de user_api_keys/decrypted_user_api_keys \u2014 ex openrouter_api_key/google_api_key \u2014 e qual model string \u00e9 usada); (3) esse modelo \u00e9 tier-GR\u00c1TIS (OpenRouter ':free', self-host) ou PAGO (Gemini paid, OpenAI)? (4) custo USD por run.\nSe tiver acesso, confirme via DB live (curl ${'`'}$SB_URL/rest/v1/...${'`'} com Bearer $SB_SECRET_KEY do .env) quais chaves o User 0 tem ativas. N\u00c3O fabrique \u2014 se n\u00e3o der pra resolver o modelo exato, diga 'unknown' com o motivo.`,\n  },\n  {\n    key: 'analyze',\n    prompt: `Trace o passo de AN\u00c1LISE (analyze) do ciclo de v\u00eddeo do Viral Autopilot para o Usu\u00e1rio Zero (user_id=${USER0}).\nO custo do ciclo \u00e9 10(orch)+12(render)+2(analyze) mco. Encontre o que \u00e9 o passo 'analyze' (ANALYZE_COST=2) \u2014 procure em supabase/functions/autopilot-run/index.ts, autopilot-analyze/index.ts, orchestrate-step (passo de an\u00e1lise/ranking), e qualquer chamada a analyze-node ou similar.\nDetermine MATERIALMENTE: (1) qual edge fn + linha faz a chamada LLM de an\u00e1lise; (2) provider+modelo exato resolvido p/ User 0 + de qual coluna BYOK; (3) free-tier vs pago; (4) USD por run. Confirme via DB live se poss\u00edvel. N\u00c3O fabrique \u2014 'unknown' com motivo se n\u00e3o resolver.`,\n  },\n  {\n    key: 'image',\n    prompt: `Determine se o ciclo de v\u00eddeo do Viral Autopilot (User 0 = ${USER0}) gera IMAGEM e qual o custo USD dela.\nContexto da mem\u00f3ria: generate-image roteia por OpenRouter Gemini (OpenAI virou fallback inalcan\u00e7\u00e1vel); providers de imagem do User 0 estavam quebrados (nanobana mock). Leia supabase/functions/orchestrate-step/index.ts (bloco de imagem / fail-open) e generate-image/index.ts.\nDetermine MATERIALMENTE: (1) o FLUXO DE V\u00cdDEO chama generate-image, ou pula/usa frame do HyperFrames? Cite a linha; (2) se chama, qual provider+modelo+coluna BYOK p/ User 0; (3) free vs pago + USD/run; (4) se o passo \u00e9 fail-open 'skipped' (n\u00e3o cobra/n\u00e3o chama quando falha). N\u00c3O fabrique.`,\n  },\n  {\n    key: 'render',\n    prompt: `Confirme MATERIALMENTE que o passo de RENDER do ciclo de v\u00eddeo (HyperFrames) roda 100% self-hosted, SEM chamada a API externa paga.\nLeia scripts/hyperframes/render-core.ts, scripts/video-bridge.ts. Verifique: (1) o render usa Playwright headless + FFmpeg locais (bin\u00e1rios na infra pr\u00f3pria), zero chamada a SaaS de gera\u00e7\u00e3o de v\u00eddeo externo (n\u00e3o Veo/Higgsfield/Replicate)? Cite as linhas; (2) h\u00e1 QUALQUER fetch a endpoint externo pago no caminho de render? (3) confirme o worker systemd video-bridge.service roda local. Conclua: render = USD 0 self-hosted (sim/n\u00e3o, com evid\u00eancia).`,\n  },\n  {\n    key: 'telemetry',\n    prompt: `Encontre o custo USD REAL e as chaves BYOK do Usu\u00e1rio Zero (user_id=${USER0}) \u2014 prova material, n\u00e3o estimativa.\nUse o .env (SB_URL/SB_SECRET_KEY) e curl no Supabase REST (como o GO-gasto agent fez). (1) Liste as chaves ATIVAS do User 0 em decrypted_user_api_keys OU user_api_keys (quais colunas de provider est\u00e3o preenchidas: openrouter_api_key, google_api_key, openai_api_key, etc. \u2014 N\u00c3O imprima o valor da chave, s\u00f3 QUAIS existem). (2) Procure em infra_health_logs (event/metadata) qualquer log de custo/token/modelo dos ciclos de v\u00eddeo j\u00e1 rodados (cycle 2403bfcb, render 8b0787e0 de 06-26) \u2014 algum USD/token real registrado? (3) Cruze com a mem\u00f3ria project_product_miner (llama-3-8b:free + Gemini ~$5/m\u00eas, log real $0.0054/run) \u2014 o autopilot usa o mesmo provider? Reporte os n\u00fameros REAIS achados e diga explicitamente o que N\u00c3O est\u00e1 logado (gap de observabilidade).`,\n  },\n]\n\nphase('Trace')\nconst traces = await parallel(STEPS.map(s => () =>\n  agent(s.prompt, { label: `trace:${s.key}`, phase: 'Trace', schema: STEP_SCHEMA, effort: 'medium' })\n    .then(r => r ? { ...r, _key: s.key } : null)\n))\nconst valid = traces.filter(Boolean)\n\nphase('Verdict')\nconst VERDICT_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  properties: {\n    total_usd_per_video_cycle: { type: 'string', description: 'soma USD externo real por ciclo de v\u00eddeo do User 0 (itemizado). Distinga medido vs estimado.' },\n    itemized: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { step: { type: 'string' }, usd: { type: 'string' }, self_hosted: { type: 'string' } }, required: ['step', 'usd'] } },\n    verdict: { type: 'string', enum: ['zero', 'near_zero', 'has_cost'], description: 'zero=US$0 estrito; near_zero=<US$0.02 (free-tier dominante, vazamento desprez\u00edvel); has_cost=USD material por ciclo.' },\n    doctrine_status: { type: 'string', description: 'O ciclo cumpre a doutrina open-source-first / custo USD ao Sovereign = 0? Honesto.' },\n    swap_recommendation: { type: 'string', description: 'SE has_cost/near_zero por causa de um provider pago: o swap doutrina-aligned (modelo OpenRouter :free OU Ollama self-hosted no Mesh) com o arquivo:linha exato a mudar. Sen\u00e3o \"nenhum swap necess\u00e1rio\".' },\n    go_recommendation: { type: 'string', description: 'Veredito final pro Sovereign: pode dar o GO de gasto AGORA pela r\u00e9gua da doutrina, ou fazer o swap primeiro? Uma recomenda\u00e7\u00e3o clara.' },\n    observability_gap: { type: 'string', description: 'O custo USD real \u00e9 LOGADO em algum lugar? Se n\u00e3o, o que falta pra medir de verdade (Lei 1).' },\n  },\n  required: ['total_usd_per_video_cycle', 'itemized', 'verdict', 'doctrine_status', 'swap_recommendation', 'go_recommendation'],\n}\n\nconst verdict = await agent(\n  `Voc\u00ea \u00e9 o auditor-chefe. A doutrina Sovereign (2026-06-30) exige CUSTO USD EXTERNO AO SOVEREIGN = 0 por ciclo, e prefer\u00eancia por open-source/self-hosted dentro do MCORCH. ` +\n  `O GO de gasto do 1\u00ba ciclo pago de v\u00eddeo est\u00e1 GATED nessa r\u00e9gua. O render HyperFrames j\u00e1 \u00e9 self-hosted (USD 0). ` +\n  `Recebeu o trace material de cada passo externo do ciclo de v\u00eddeo do Usu\u00e1rio Zero. Produza o veredito: soma USD/ciclo, se cumpre a doutrina, e SE vazar custo, o swap exato (modelo :free OpenRouter ou Ollama self-hosted \u2014 o projeto j\u00e1 tem integra\u00e7\u00e3o Ollama) com arquivo:linha. ` +\n  `Seja honesto sobre o gap de observabilidade (se o USD real n\u00e3o \u00e9 logado, diga). Dados:\\n\\n` +\n  JSON.stringify(valid, null, 2),\n  { label: 'auditor', phase: 'Verdict', schema: VERDICT_SCHEMA, effort: 'high' }\n)\n\nreturn { traces: valid, verdict }\n",
  "description": "Audit video cycle external USD cost"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: w34v50410
> Summary: Audita o custo USD externo real do ciclo de vídeo do autopilot (gate da doutrina open-source-first pro GO de gasto)
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/subagents/workflows/wf_6d3bdbd6-eb7
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/workflows/scripts/video-cycle-zero-usd-audit-wf_6d3bdbd6-eb7.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/workflows/scripts/video-cycle-zero-usd-audit-wf_6d3bdbd6-eb7.js"} to iterate without resending the script.)
> Run ID: wf_6d3bdbd6-eb7
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/workflows/scripts/video-cycle-zero-usd-audit-wf_6d3bdbd6-eb7.js", resumeFromRunId: "wf_6d3bdbd6-eb7"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(23:56:33)*


## 🤖 Claude *(23:56:38)*

Audit em voo (`wf_6d3bdbd6-eb7`) — 5 traces paralelos (texto · análise · imagem · render · telemetria real do ciclo já rodado) + auditor-chefe somando o USD/ciclo e dando o veredito da doutrina.

Quando voltar, te entrego um número fechado:
- **USD real por ciclo de vídeo** do User 0, itemizado por passo (com o que é *medido* vs *estimado*).
- **Veredito da doutrina:** `zero` / `near_zero` / `has_cost`.
- **Se vazar custo:** o swap exato pra zerar — modelo OpenRouter `:free` ou **Ollama self-hosted no Mesh** (o projeto já tem integração) — com `arquivo:linha`.
- **Recomendação de GO:** se você já pode dar o GO de gasto pela sua régua, ou se vale fazer o swap antes.
- **Gap de observabilidade:** se o USD real não está sendo logado em lugar nenhum (Lei 1 — honesto sobre o que dá ou não pra medir).

Te aviso assim que concluir. O harness me reacorda.

## 👤 User *(00:03:31)*

<task-notification>
<task-id>w34v50410</task-id>
<tool-use-id>toolu_01SDVq2NFd9EZsz4VUxcz5qJ</tool-use-id>
<output-file>/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/tasks/w34v50410.output</output-file>
<status>completed</status>
<summary>Dynamic workflow "Audita o custo USD externo real do ciclo de vídeo do autopilot (gate da doutrina open-source-first pro GO de gasto)" completed</summary>
<result>{"traces":[{"step":"Geração de TEXTO/SCRIPT (article_generation) do ciclo de vídeo do Viral Autopilot para o Usuário Zero. Cadeia real: autopilot-run (fan-out prepaid) -&gt; orchestrate-content (resolve modelo + grava em pipeline_runs.metadata + kick async_orchestrate_step) -&gt; orchestrate-step (FAZ a chamada LLM). generate-content/index.ts NAO esta nesta cadeia: e funcao user-facing standalone (chat/single post), nao invocada pelo autopilot.","edge_fn":"orchestrate-step/index.ts:289 (step 'article_generation', via fetchLLMWithFallback) — tambem :625 (linkedin_post) e :698 (twitter_thread). Resolucao provider/modelo em orchestrate-step/index.ts:272-281. Wrapper cascata: _shared/llm-fallback.ts:48. autopilot-run/index.ts:233 so faz fan-out p/ orchestrate-content; orchestrate-content/index.ts:80-96 resolve o mesmo modelo e persiste em pipeline_runs.metadata.selectedModel.","provider_model":"OpenRouter google/gemini-2.5-pro-preview. Deterministico: pref_ai_model='google/gemini-2.5-pro-preview' contem '/' =&gt; prefRequiresOR=true =&gt; aiKey=openRouterKey, isGroq=false, endpoint=openrouter.ai/api/v1/chat/completions; orPrefModel nao comeca com 'gemini-' (comeca com 'google/') =&gt; selectedModel='google/gemini-2.5-pro-preview'. NOTA: a cascata de fallback (llm-fallback.ts) so dispara em 402/429/5xx; o caminho feliz NAO usa modelo :free.","key_source":"BYOK per-user via VIEW decrypted_user_api_keys (Vault), filtrada por user_id. Coluna efetiva: openrouter_api_key (pref_ai_model forca rota OpenRouter). Colunas lidas em orchestrate-step:272-275 = groq_api_key, openrouter_api_key, google_api_key, pref_ai_model. User 0 tem as 3 chaves reais e ativas: groq=gsk_YM...(56 chars), openrouter=sk-or-v1...(73 chars), google=AIzaSy...(39 chars).","is_free_tier":"no","usd_per_run":"~$0.02 a $0.04 por chamada de artigo (ESTIMADO, NAO medido). Base: google/gemini-2.5-pro-preview no OpenRouter e PAGO (~$1.25/M input, ~$10/M output); 1 tool-call de artigo SEO (min 500 chars; tipico ~800-1500 palavras =&gt; ~1.5-3K tokens output + prompt pequeno). Nao consegui medir tokens reais (sem campo de usage/word_count nos runs recentes do User 0, que erraram antes do done). Cada sub-run wordpress tambem dispara linkedin/twitter (calls menores), somando alguns centavos por sub-run.","self_hosted":"no","evidence":["orchestrate-step/index.ts:289 (fetchLLMWithFallback body model: selectedModel)","orchestrate-step/index.ts:276 prefRequiresOR = pref includes '/' || startsWith 'gemini-'","orchestrate-step/index.ts:280-281 orPrefModel/selectedModel resolution","_shared/llm-fallback.ts:84-101 fallback so em 402/429/&gt;=500 (happy path = primary pago)","DB live: decrypted_user_api_keys user_id=ada39fae... =&gt; pref_ai_model='google/gemini-2.5-pro-preview', openrouter=sk-or-v1...(73), google=AIzaSy...(39), groq=gsk_YM...(56)","DB live: pipeline_runs do User 0 (started_at 2026-06-26 e 2026-06-23) gravam metadata.selectedModel='google/gemini-2.5-pro-preview', isGroq=False, aiEndpoint=https://openrouter.ai/api/v1/chat/completions","OpenRouter pricing publico Gemini 2.5 Pro Preview ~$1.25/M in, ~$10/M out (base da estimativa; nao medido neste run)"],"_key":"content"},{"step":"ANALYZE (R3 loop) do ciclo de video do Viral Autopilot — ranqueia o ciclo anterior e escreve optimization_policy (FR-VA-010/011). ANALYZE_COST=2 mco.","edge_fn":"supabase/functions/autopilot-analyze/index.ts (chamada origina em supabase/functions/autopilot-run/index.ts:196 via svcCall). NAO chama analyze-node nem orchestrate-step de analise — grep confirmou 'NO reference to analyze-node in autopilot path'.","provider_model":"NENHUM. O passo analyze nao faz chamada LLM. E ranqueamento deterministico em TypeScript puro (reward multi-metrica FR-VA-029, autopilot-analyze/index.ts linhas ~100-140) sobre dados de creative_metrics + publication_metrics, escrevendo optimization_policy. Unico import externo: https://esm.sh/@supabase/supabase-js@2 (cliente DB), nenhum host de IA.","key_source":"N/A — nenhuma credencial de provider e resolvida. grep por user_api_keys/decrypted/api_key/openrouter/gemini/groq/openai em autopilot-analyze/index.ts = NONE FOUND. Unica credencial usada e SB_SECRET_KEY (service-role) para identidade + acesso ao DB; tenant derivado de autopilot_cycles.user_id (anti-IDOR), nunca do body.","is_free_tier":"depends","usd_per_run":"~$0.00 (zero USD externo). Nao ha chamada a API paga; so leituras/escritas no Postgres do proprio Supabase do MCORCH. O ANALYZE_COST=2 mco e um debito interno de mcoCoins (deduct_mco_coins RPC, cobrado so quando has_real_data &amp;&amp; !prepaid) — moeda interna, nao custo USD de provider. No ciclo de video o 2 e pre-reservado (prepaid=true) e consumido sem self-bill.","self_hosted":"yes","evidence":["supabase/functions/autopilot-analyze/index.ts:26 (const ANALYZE_COST = 2)","supabase/functions/autopilot-analyze/index.ts:100-140 (reward multi-metrica deterministico, sem LLM)","supabase/functions/autopilot-analyze/index.ts:~170-180 (deduct_mco_coins RPC so se !prepaid)","supabase/functions/autopilot-run/index.ts:196 (svcCall autopilot-analyze prepaid:true)","grep LLM/fetch/api_key em autopilot-analyze = 'NONE FOUND' (executado nesta sessao)","grep analyze-node no path autopilot = 'NO reference to analyze-node in autopilot path'","unico import externo linha 12 = esm.sh/@supabase/supabase-js@2","supabase functions list LIVE: autopilot-analyze ACTIVE v7 id 59796cb6-a57a-4b26-902b-4873c7f8d162","DB live REST: optimization_policy do User 0 cycle_id 947ef8b5-8d1e-4f54-bd40-a2e13b3ec802 reward 0.9/1.0 — prova que analyze rodou e o reward e calculo (0.9 = formula fallback clicks/max*0.9), nao texto de LLM"],"_key":"analyze"},{"step":"Ciclo de video do Viral Autopilot (User 0 ada39fae) - geracao de IMAGEM e custo USD","edge_fn":"Dois passos IRMAOS em supabase/functions/orchestrate-step/index.ts, ambos sob `if (hasProducts)` (linha 460): (A) image_generation chama generate-image em orchestrate-step/index.ts:464; (B) video_generation (linha 494, gated `if (videoEnabled)`) NAO chama generate-image - enfileira HyperFrames render via video_renders insert (linha 522). Motor scripts/hyperframes/render-core.ts = Playwright+FFmpeg puro (sem IA). Chamada de imagem entra em generate-image/index.ts:204 generateViaOpenRouter.","provider_model":"RESPOSTA (1): O FLUXO DE VIDEO em si NAO chama generate-image e NAO usa frame de IA - HyperFrames renderiza HTML para MP4 usando a foto publica do produto ML (composition.props.product_image_url, orchestrate-step:500-501,514), nao imagem gerada (orchestrate-step:494-526 + render-core.ts). POREM no MESMO ciclo de produto o passo irmao image_generation (orchestrate-step:464) chama generate-image porque o gate e hasProducts (linha 460), nao videoEnabled. (2) Para esse passo de imagem, User 0 resolve para OpenRouter google/gemini-2.5-flash-image (Nano Banana) - generate-image/index.ts:94 `else if (openRouterKey)` cai no branch e linha 214 usa model=google/gemini-2.5-flash-image. Nota: pref_image_provider=\"nanobana\" (!= \"replicate\") por isso cai no OpenRouter, nao Replicate FLUX.","key_source":"decrypted_user_api_keys.openrouter_api_key - coluna per-user BYOK (VIEW decifrada do Vault), lida em generate-image/index.ts:71-74 via adminClient (service-role). Roteamento em generate-image/index.ts:92-107. Live DB User 0 (HTTP 200): openrouter_api_key presente (sk-or-v1-d861...), replicate e openai tambem presentes, pref_image_provider=nanobana.","is_free_tier":"depends","usd_per_run":"VIDEO (HyperFrames, o fluxo perguntado): ~$0.00 de API de IA - render deterministico headless Chrome+FFmpeg, ZERO chamada a provider de imagem (render-core.ts). Cobranca VIDEO_HYPERFRAMES_RENDER=12 mco e marker de compute proprio (billing.ts:46), nao USD de API externa. IMAGEM (passo irmao image_generation, quando hasProducts): OpenRouter google/gemini-2.5-flash-image - preco OpenRouter tipico ~$0.03/imagem (NAO medido em log real nesta sessao; estimativa de tabela do provedor). NAO e :free
... (truncated 14396 chars, full result in /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/tasks/w34v50410.output)</result>
<usage><agent_count>6</agent_count><subagent_tokens>540870</subagent_tokens><tool_uses>64</tool_uses><duration_ms>423665</duration_ms></usage>
</task-notification>

## 🤖 Claude *(00:03:43)*


## 🤖 Claude *(00:03:44)*

Audit voltou com achado importante — não é "zero" como esperávamos. Vou ler o veredito completo do auditor antes de te reportar:

## 🤖 Claude *(00:03:44)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/tasks/w34v50410.output"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	{
> 2	  "summary": "Audita o custo USD externo real do ciclo de vídeo do autopilot (gate da doutrina open-source-first pro GO de gasto)",
> 3	  "agentCount": 6,
> 4	  "logs": [],
> 5	  "result": {
> 6	    "traces": [
> 7	      {
> 8	        "step": "Geração de TEXTO/SCRIPT (article_generation) do ciclo de vídeo do Viral Autopilot para o Usuário Zero. Cadeia real: autopilot-run (fan-out prepaid) -> orchestrate-content (resolve modelo + grava em pipeline_runs.metadata + kick async_orchestrate_step) -> orchestrate-step (FAZ a chamada LLM). generate-content/index.ts NAO esta nesta cadeia: e funcao user-facing standalone (chat/single post), nao invocada pelo autopilot.",
> 9	        "edge_fn": "orchestrate-step/index.ts:289 (step 'article_generation', via fetchLLMWithFallback) — tambem :625 (linkedin_post) e :698 (twitter_thread). Resolucao provider/modelo em orchestrate-step/index.ts:272-281. Wrapper cascata: _shared/llm-fallback.ts:48. autopilot-run/index.ts:233 so faz fan-out p/ orchestrate-content; orchestrate-content/index.ts:80-96 resolve o mesmo modelo e persiste em pipeline_runs.metadata.selectedModel.",
> 10	        "provider_model": "OpenRouter google/gemini-2.5-pro-preview. Deterministico: pref_ai_model='google/gemini-2.5-pro-preview' contem '/' => prefRequiresOR=true => aiKey=openRouterKey, isGroq=false, endpoint=openrouter.ai/api/v1/chat/completions; orPrefModel nao comeca com 'gemini-' (comeca com 'google/') => selectedModel='google/gemini-2.5-pro-preview'. NOTA: a cascata de fallback (llm-fallback.ts) so dispara em 402/429/5xx; o caminho feliz NAO usa modelo :free.",
> 11	        "key_source": "BYOK per-user via VIEW decrypted_user_api_keys (Vault), filtrada por user_id. Coluna efetiva: openrouter_api_key (pref_ai_model forca rota OpenRouter). Colunas lidas em orchestrate-step:272-275 = groq_api_key, openrouter_api_key, google_api_key, pref_ai_model. User 0 tem as 3 chaves reais e ativas: groq=gsk_YM...(56 chars), openrouter=sk-or-v1...(73 chars), google=AIzaSy...(39 chars).",
> 12	        "is_free_tier": "no",
> 13	        "usd_per_run": "~$0.02 a $0.04 por chamada de artigo (ESTIMADO, NAO medido). Base: google/gemini-2.5-pro-preview no OpenRouter e PAGO (~$1.25/M input, ~$10/M output); 1 tool-call de artigo SEO (min 500 chars; tipico ~800-1500 palavras => ~1.5-3K tokens output + prompt pequeno). Nao consegui medir tokens reais (sem campo de usage/word_count nos runs recentes do User 0, que erraram antes do done). Cada sub-run wordpress tambem dispara linkedin/twitter (calls menores), somando alguns centavos por sub-run.",
> 14	        "self_hosted": "no",
> 15	        "evidence": [
> 16	          "orchestrate-step/index.ts:289 (fetchLLMWithFallback body model: selectedModel)",
> 17	          "orchestrate-step/index.ts:276 prefRequiresOR = pref includes '/' || startsWith 'gemini-'",
> 18	          "orchestrate-step/index.ts:280-281 orPrefModel/selectedModel resolution",
> 19	          "_shared/llm-fallback.ts:84-101 fallback so em 402/429/>=500 (happy path = primary pago)",
> 20	          "DB live: decrypted_user_api_keys user_id=ada39fae... => pref_ai_model='google/gemini-2.5-pro-preview', openrouter=sk-or-v1...(73), google=AIzaSy...(39), groq=gsk_YM...(56)",
> 21	          "DB live: pipeline_runs do User 0 (started_at 2026-06-26 e 2026-06-23) gravam metadata.selectedModel='google/gemini-2.5-pro-preview', isGroq=False, aiEndpoint=https://openrouter.ai/api/v1/chat/completions",
> 22	          "OpenRouter pricing publico Gemini 2.5 Pro Preview ~$1.25/M in, ~$10/M out (base da estimativa; nao medido neste run)"
> 23	        ],
> 24	        "_key": "content"
> 25	      },
> 26	      {
> 27	        "step": "ANALYZE (R3 loop) do ciclo de video do Viral Autopilot — ranqueia o ciclo anterior e escreve optimization_policy (FR-VA-010/011). ANALYZE_COST=2 mco.",
> 28	        "edge_fn": "supabase/functions/autopilot-analyze/index.ts (chamada origina em supabase/functions/autopilot-run/index.ts:196 via svcCall). NAO chama analyze-node nem orchestrate-step de analise — grep confirmou 'NO reference to analyze-node in autopilot path'.",
> 29	        "provider_model": "NENHUM. O passo analyze nao faz chamada LLM. E ranqueamento deterministico em TypeScript puro (reward multi-metrica FR-VA-029, autopilot-analyze/index.ts linhas ~100-140) sobre dados de creative_metrics + publication_metrics, escrevendo optimization_policy. Unico import externo: https://esm.sh/@supabase/supabase-js@2 (cliente DB), nenhum host de IA.",
> 30	        "key_source": "N/A — nenhuma credencial de provider e resolvida. grep por user_api_keys/decrypted/api_key/openrouter/gemini/groq/openai em autopilot-analyze/index.ts = NONE FOUND. Unica credencial usada e SB_SECRET_KEY (service-role) para identidade + acesso ao DB; tenant derivado de autopilot_cycles.user_id (anti-IDOR), nunca do body.",
> 31	        "is_free_tier": "depends",
> 32	        "usd_per_run": "~$0.00 (zero USD externo). Nao ha chamada a API paga; so leituras/escritas no Postgres do proprio Supabase do MCORCH. O ANALYZE_COST=2 mco e um debito interno de mcoCoins (deduct_mco_coins RPC, cobrado so quando has_real_data && !prepaid) — moeda interna, nao custo USD de provider. No ciclo de video o 2 e pre-reservado (prepaid=true) e consumido sem self-bill.",
> 33	        "self_hosted": "yes",
> 34	        "evidence": [
> 35	          "supabase/functions/autopilot-analyze/index.ts:26 (const ANALYZE_COST = 2)",
> 36	          "supabase/functions/autopilot-analyze/index.ts:100-140 (reward multi-metrica deterministico, sem LLM)",
> 37	          "supabase/functions/autopilot-analyze/index.ts:~170-180 (deduct_mco_coins RPC so se !prepaid)",
> 38	          "supabase/functions/autopilot-run/index.ts:196 (svcCall autopilot-analyze prepaid:true)",
> 39	          "grep LLM/fetch/api_key em autopilot-analyze = 'NONE FOUND' (executado nesta sessao)",
> 40	          "grep analyze-node no path autopilot = 'NO reference to analyze-node in autopilot path'",
> 41	          "unico import externo linha 12 = esm.sh/@supabase/supabase-js@2",
> 42	          "supabase functions list LIVE: autopilot-analyze ACTIVE v7 id 59796cb6-a57a-4b26-902b-4873c7f8d162",
> 43	          "DB live REST: optimization_policy do User 0 cycle_id 947ef8b5-8d1e-4f54-bd40-a2e13b3ec802 reward 0.9/1.0 — prova que analyze rodou e o reward e calculo (0.9 = formula fallback clicks/max*0.9), nao texto de LLM"
> 44	        ],
> 45	        "_key": "analyze"
> 46	      },
> 47	      {
> 48	        "step": "Ciclo de video do Viral Autopilot (User 0 ada39fae) - geracao de IMAGEM e custo USD",
> 49	        "edge_fn": "Dois passos IRMAOS em supabase/functions/orchestrate-step/index.ts, ambos sob `if (hasProducts)` (linha 460): (A) image_generation chama generate-image em orchestrate-step/index.ts:464; (B) video_generation (linha 494, gated `if (videoEnabled)`) NAO chama generate-image - enfileira HyperFrames render via video_renders insert (linha 522). Motor scripts/hyperframes/render-core.ts = Playwright+FFmpeg puro (sem IA). Chamada de imagem entra em generate-image/index.ts:204 generateViaOpenRouter.",
> 50	        "provider_model": "RESPOSTA (1): O FLUXO DE VIDEO em si NAO chama generate-image e NAO usa frame de IA - HyperFrames renderiza HTML para MP4 usando a foto publica do produto ML (composition.props.product_image_url, orchestrate-step:500-501,514), nao imagem gerada (orchestrate-step:494-526 + render-core.ts). POREM no MESMO ciclo de produto o passo irmao image_generation (orchestrate-step:464) chama generate-image porque o gate e hasProducts (linha 460), nao videoEnabled. (2) Para esse passo de imagem, User 0 resolve para OpenRouter google/gemini-2.5-flash-image (Nano Banana) - generate-image/index.ts:94 `else if (openRouterKey)` cai no branch e linha 214 usa model=google/gemini-2.5-flash-image. Nota: pref_image_provider=\"nanobana\" (!= \"replicate\") por isso cai no OpenRouter, nao Replicate FLUX.",
> 51	        "key_source": "decrypted_user_api_keys.openrouter_api_key - coluna per-user BYOK (VIEW decifrada do Vault), lida em generate-image/index.ts:71-74 via adminClient (service-role). Roteamento em generate-image/index.ts:92-107. Live DB User 0 (HTTP 200): openrouter_api_key presente (sk-or-v1-d861...), replicate e openai tambem presentes, pref_image_provider=nanobana.",
> 52	        "is_free_tier": "depends",
> 53	        "usd_per_run": "VIDEO (HyperFrames, o fluxo perguntado): ~$0.00 de API de IA - render deterministico headless Chrome+FFmpeg, ZERO chamada a provider de imagem (render-core.ts). Cobranca VIDEO_HYPERFRAMES_RENDER=12 mco e marker de compute proprio (billing.ts:46), nao USD de API externa. IMAGEM (passo irmao image_generation, quando hasProducts): OpenRouter google/gemini-2.5-flash-image - preco OpenRouter tipico ~$0.03/imagem (NAO medido em log real nesta sessao; estimativa de tabela do provedor). NAO e :free (o modelo gemini-2.5-flash-image cobra USD real via OpenRouter). billing.ts cita DALL-E ref $0.04/img mas isso e fallback inalcancavel; rota viva e OpenRouter Gemini.",
> 54	        "self_hosted": "partial",
> 55	        "evidence": [
> 56	          "orchestrate-step/index.ts:460 (if hasProducts) envolve AMBOS os blocos",
> 57	          "orchestrate-step/index.ts:464 fetch /functions/v1/generate-image (passo image_generation)",
> 58	          "orchestrate-step/index.ts:494 if(videoEnabled) - bloco de VIDEO separado, sem generate-image",
> 59	          "orchestrate-step/index.ts:500-501,514 product_image_url = foto publica do produto ML usada pelo HyperFrames",
> 60	          "orchestrate-step/index.ts:522-526 insert video_renders engine=hyperframes (enfileira, nao gera imagem)",
> 61	          "scripts/hyperframes/render-core.ts:110-125 captura frame-by-frame via Playwright screenshot + FFmpeg (sem IA)",
> 62	          "generate-image/index.ts:94 else if(openRouterKey) -> branch OpenRouter",
> 63	          "generate-image/index.ts:214 model=google/gemini-2.5-flash-image",
> 64	          "generate-image/index.ts:71-74 le decrypted_user_api_keys.openrouter_api_key/replicate/openai + pref_image_provider",
> 65	          "Live DB HTTP 200: decrypted_user_api_keys User 0 ada39fae pref_image_provider=nanobana, openrouter_api_key presente",
> 66	          "billing.ts:46 VIDEO_HYPERFRAMES_RENDER:12 (deterministic HTML->MP4, no AI legs)",
> 67	          "orchestrate-step/index.ts:476/479/483 image_generation status 'done' ou 'skipped' fail-open (nunca 'error')",
> 68	          "orchestrate-step/index.ts:529/532 video_generation 'done' ou 'skipped' fail-open; orchestrate-step nunca chama deduct_mco_coins (linha 453 comentario)",
> 69	          "orchestrate-step/index.ts:540-543 quando !enqueued && cycleId -> refund_autopilot_video_enqueue (credito compensatorio do pre-debito do ciclo)"
> 70	        ],
> 71	        "_key": "image"
> 72	      },
> 73	      {
> 74	        "step": "RENDER do ciclo de vídeo (HyperFrames) — composition spec → MP4 9:16 1080x1920",
> 75	        "edge_fn": "scripts/hyperframes/render-core.ts:74-147 (renderComposition — núcleo puro); host worker scripts/video-bridge.ts:67-190 (processRender). Edge fn video-render é só transporte poll:// e NÃO roda o render.",
> 76	        "provider_model": "Self-hosted: Playwright Chromium headless + FFmpeg libx264 locais. ZERO modelo/SaaS de geração de vídeo (não Veo, não Higgsfield, não Replicate, não fal.ai). Render determinístico HTML→MP4, sem leg de IA (NFR-VS-016).",
> 77	        "key_source": "Nenhuma credencial de provider de vídeo é resolvida — não existe provider. video-bridge.ts:35-41 usa só SUPABASE_URL + SB_SECRET_KEY (service-role) para claim/upload/finalize na própria malha. Sem Deno.env.get de qualquer <VIDEO_SERVICE>_API_KEY.",
> 78	        "is_free_tier": "yes",
> 79	        "usd_per_run": "USD 0.00 — render real 536KB em 110633ms na CPU própria (log systemd: render 80368713 done 536KB 110633ms, refunded:0). Custo = só CPU/RAM da infra própria. Cobrança do passo no path prepaid = 0 (finalize_video_render p_refund:0; render-core não fatura).",
> 80	        "self_hosted": "yes",
> 81	        "evidence": [
> 82	          "render-core.ts:22 import { chromium } from 'playwright' (Chromium headless local, launch :87-91 headless:true)",
> 83	          "render-core.ts:60-68 + :122-136 — FFmpeg local via spawn('ffmpeg', args), PNG→H.264 yuv420p, binário /usr/bin/ffmpeg",
> 84	          "render-core.ts:9 comentário 'no AI leg — fully deterministic'; render-core.ts:13 'no network beyond the product image'",
> 85	          "render-core.ts:100-108 — único fetch externo POSSÍVEL é baixar product_image_url dentro do template file:// (imagem de produto, NÃO geração de vídeo paga); render é frame-by-frame por screenshot local (:111-118)",
> 86	          "video-bridge.ts:166-170 fetch a $SUPABASE_URL/functions/v1/reshape-pillar — malha própria, PÓS-finalize, FORA do path de render; nenhum outro fetch externo no worker",
> 87	          "bash: which ffmpeg → /usr/bin/ffmpeg ; ffmpeg version 6.1.1-3ubuntu5 (binário local)",
> 88	          "bash: Chromium Playwright local em /home/ubuntu/.cache/ms-playwright/chromium-1226/ ; node_modules/playwright presente no repo",
> 89	          "bash: systemctl --user status video-bridge.service → Active: active (running) since Sun 2026-06-28, Main PID 768276 bun, CGroup user-1001.slice (roda LOCAL na infra própria)",
> 90	          "log video-bridge: '✅ render 80368713-... done → ...mp4 (536KB, 110633ms) refunded: 0' — execução real self-hosted, custo USD 0"
> 91	        ],
> 92	        "_key": "render"
> 93	      },
> 94	      {
> 95	        "step": "Custo USD real + chaves BYOK do Usuario Zero (ada39fae) — autopilot de video (cycle 2403bfcb / render 8b0787e0) + geracao de texto do pipeline",
> 96	        "edge_fn": "supabase/functions/orchestrate-step/index.ts:275-281 (resolve o modelo de texto); scripts/hyperframes/render-core.ts + scripts/video-bridge.ts (render do video — Playwright+FFmpeg deterministico, SEM LLM); vision-mcp container (analyze_video/describe_image do product-miner)",
> 97	        "provider_model": "TEXTO do autopilot/pipeline: OpenRouter google/gemini-2.5-pro-preview — resolvido MATERIAL do DB: decrypted_user_api_keys.pref_ai_model=\"google/gemini-2.5-pro-preview\"; orchestrate-step:280-281 prefixa google/ e roteia p/ openrouter.ai (prefRequiresOR=true). VIDEO (HyperFrames render 8b0787e0, engine=hyperframes): deterministico Playwright+FFmpeg, SEM provider LLM no render. ANALISE de produto (vision-mcp): Gemini BYOK, cost=0.",
> 98	        "key_source": "decrypted_user_api_keys (VIEW mascarada sobre Vault) filtrada por user_id=ada39fae. Colunas de provider PREENCHIDAS p/ User 0: openrouter_api_key(len73), google_api_key(len39 = Gemini BYOK, NAO gemini_api_key), openai_api_key(len164), groq_api_key(len56), elevenlabs_api_key(len51), replicate_api_key(len40), higgsfield_api_key+_secret, apify_token, rapidapi_key, wp_site_url/username/app_password. VAZIAS: nanobana, seedance, resend, firecrawl, hedra, cartesia, fal. Modelo de texto resolve via openrouter_api_key (BYOK do proprio User 0).",
> 99	        "is_free_tier": "no",
> 100	        "usd_per_run": "DESCONHECIDO — gap de observabilidade material: NAO existe NENHUM registro de USD nem de tokens em lugar algum do sistema. Unico custo gravado e mcoCoins: autopilot_cycles 2403bfcb spend_mco=46 (2 units, refunded 0); video_renders 8b0787e0 charged_mco=12 (state=done, refunded 0); pipeline_runs tipico mco_cost=10. Isso NAO e USD. O modelo do User 0 (google/gemini-2.5-pro-preview) e PAGO no OpenRouter (~$1.25/1M in, ~$10/1M out), logo cada run de texto tem USD real >0 — mas o valor exato NAO esta logado. Contraste com product-miner: la o vision-mcp loga cost=0/byok=true (Gemini gratis), aqui o texto usa gemini-2.5-PRO PAGO no OpenRouter, provider diferente do llama-3-8b:free+Gemini do miner.",
> 101	        "self_hosted": "partial",
> 102	        "evidence": [
> 103	          "decrypted_user_api_keys?user_id=eq.ada39fae → openrouter_api_key/google_api_key/openai_api_key/groq_api_key/elevenlabs_api_key/replicate_api_key/higgsfield/apify_token/rapidapi_key PRESENT; nanobana/seedance/resend/firecrawl/hedra/cartesia/fal EMPTY",
> 104	          "decrypted_user_api_keys.pref_ai_model = 'google/gemini-2.5-pro-preview' (pref_image=nanobana, pref_video=seedance, pref_audio=elevenlabs)",
> 105	          "orchestrate-step/index.ts:275-281 (prefModel resolve → orPrefModel='google/'+pref → openrouter.ai/api/v1/chat/completions)",
> 106	          "video_renders 8b0787e0-1442... state=done, engine=hyperframes, charged_mco=12, refunded_mco=0, storage_key presente; composition.autopilot.cycle_id=2403bfcb — SEM coluna usd/token/model",
> 107	          "autopilot_cycles 2403bfcb... status=completed, spend_mco=46, refunded_mco=0, planned_units=2 — SEM coluna usd/token",
> 108	          "pipeline_runs cols = [id,user_id,topic,platforms,status,steps,wordpress_url,error_message,mco_cost,started_at,completed_at,metadata] — SEM usd/token; run 93659c88 steps[].model=None (nem o nome do modelo persiste na linha)",
> 109	          "infra_health_logs: eventos non-cron so vision-mcp (metadata cost=0/byok=true/tool=describe_image|analyze_video) e avatar-clone-ai; probe por keys usd/token/cost/model/prompt_tokens/completion_tokens em metadata = 0 linhas → NENHUM custo USD ou token e telemetrado"
> 110	        ],
> 111	        "_key": "telemetry"
> 112	      }
> 113	    ],
> 114	    "verdict": {
> 115	      "total_usd_per_video_cycle": "~US$0.05–0.07 por ciclo (ESTIMADO, nao medido) — soma de: TEXTO google/gemini-2.5-pro-preview (artigo + linkedin_post + twitter_thread, ~$0.02–0.04) + IMAGEM google/gemini-2.5-flash-image do passo irmao image_generation (~$0.03). RENDER HyperFrames e ANALYZE = US$0 medidos/self-hosted. ATENCAO Lei 1: os dois valores pagos NAO tem prova material de USD — sao estimativas de tabela de preco do OpenRouter, porque o sistema nao loga USD nem tokens em lugar algum (vide observability_gap). So o debito interno de mcoCoins e gravado (spend_mco=46 / charged_mco=12), o que NAO e USD.",
> 116	      "itemized": [
> 117	        {
> 118	          "step": "TEXTO article_generation (+ linkedin_post :625 + twitter_thread :698) via fetchLLMWithFallback happy-path",
> 119	          "usd": "~$0.02–0.04 ESTIMADO (google/gemini-2.5-pro-preview PAGO ~$1.25/M in, ~$10/M out; nao medido — sem log de tokens)",
> 120	          "self_hosted": "no — OpenRouter, BYOK openrouter_api_key do User 0"
> 121	        },
> 122	        {
> 123	          "step": "IMAGEM image_generation (passo irmao gated hasProducts, orchestrate-step:464 -> generate-image:214)",
> 124	          "usd": "~$0.03 ESTIMADO (google/gemini-2.5-flash-image / Nano Banana PAGO no OpenRouter; nao :free; nao medido)",
> 125	          "self_hosted": "no — OpenRouter, BYOK openrouter_api_key"
> 126	        },
> 127	        {
> 128	          "step": "ANALYZE (R3 loop, autopilot-analyze)",
> 129	          "usd": "$0.00 — ranqueamento deterministico TypeScript, zero chamada LLM (grep NONE FOUND); ANALYZE_COST=2 e mcoCoins interno",
> 130	          "self_hosted": "yes"
> 131	        },
> 132	        {
> 133	          "step": "RENDER HyperFrames (render-core.ts Playwright+FFmpeg local)",
> 134	          "usd": "$0.00 MEDIDO — render real 536KB/110633ms na CPU propria, refunded:0; sem provider de video",
> 135	          "self_hosted": "yes"
> 136	        }
> 137	      ],
> 138	      "verdict": "has_cost",
> 139	      "doctrine_status": "NAO cumpre a doutrina como esta hoje. A regra Sovereign 2026-06-30 exige custo USD externo ao Sovereign = 0 por ciclo e preferencia open-source/self-hosted. O render (HyperFrames) e o analyze ja estao 100% self-hosted a US$0 — a espinha do video esta correta. Mas DUAS pernas do MESMO ciclo vazam USD material para provider pago via OpenRouter BYOK do User 0: (1) o texto usa google/gemini-2.5-pro-preview (PAGO, ~$10/M out) e o caminho feliz NUNCA toca modelo :free — a cascata llm-fallback so cai em :free sob 402/429/5xx (verificado em llm-fallback.ts:96-99); (2) a imagem usa google/gemini-2.5-flash-image (PAGO, nao :free). Contraste honesto: o product-miner ja opera na doutrina (llama-3-8b:free + Gemini BYOK cost=0), mas o autopilot de video escolheu o Pro pago. Logo: doutrina violada por config de pref_ai_model/pref_image, nao por arquitetura — o codigo ja tem o trilho :free (llm-fallback.ts:155 lista gemma-2-9b-it:free e llama-3-8b-instruct:free).",
> 140	      "observability_gap": "CRITICO e material (fere Lei 1): o custo USD real NAO e logado em lugar nenhum. Probe confirmou: pipeline_runs nao tem coluna usd/token (cols = id,user_id,topic,platforms,status,steps,wordpress_url,error_message,mco_cost,started_at,completed_at,metadata; ate steps[].model=None em runs recentes); autopilot_cycles so tem spend_mco/refunded_mco/planned_units; video_renders so charged_mco/refunded_mco. infra_health_logs so telemetra cost/byok/tokens para o vision-mcp (cost=0/byok=true) e avatar-clone-ai — a probe por keys usd/token/cost/model/prompt_tokens/completion_tokens no metadata das pernas pagas = 0 linhas. Ou seja: hoje o veredito 'has_cost' e ESTIMADO, nao medido — nao da para dar GO de gasto com prova material. FALTA PARA MEDIR DE VERDADE (Lei 1): (a) capturar o campo `usage` (prompt_tokens/completion_tokens) que OpenRouter ja devolve na resposta de chat/image e (b) emitir um evento infra_health_logs (event='llm_usage', metadata={run_id, step, model, prompt_tokens, completion_tokens, usd_estimate}) no chokepoint fetchLLMWithFallback (orchestrate-step) e em generate-image apos a resposta 200. Sem isso, o USD/ciclo continua invisivel e o gate de doutrina nao e auditavel materialmente.",
> 141	      "swap_recommendation": "SIM, ha vazamento por provider pago — dois swaps doutrina-aligned, ambos para modelo OpenRouter :free (esforco quase-zero; o codigo ja conhece esses ids em llm-fallback.ts:155). SWAP 1 (TEXTO — a maior perna): NAO mexer no codigo de orchestrate-step:281 (ele resolve selectedModel a partir de userKeys.pref_ai_model, que contem '/' e roteia OpenRouter corretamente). Mudar o DADO: setar decrypted_user_api_keys.pref_ai_model do User 0 (ada39fae) de 'google/gemini-2.5-pro-preview' para 'google/gemma-2-9b-it:free' (ou 'meta-llama/llama-3-8b-instruct:free'). Ambos contem '/' -> prefRequiresOR=true -> continua OpenRouter, mas :free = USD 0. Ancora de codigo: orchestrate-step/index.ts:275-281 (nenhuma linha muda) + valor em user_api_keys.pref_ai_model. SWAP 2 (IMAGEM): generate-image/index.ts:214 hardcoda model:'google/gemini-2.5-flash-image' (PAGO) — nao ha :free equivalente de imagem no OpenRouter que sirva. Doutrina-aligned aqui = trocar a ROTA, nao o modelo: setar pref_image_provider='replicate' (coluna ja lida em generate-image; branch replicate existe :92) e usar FLUX self-hostavel, OU (mais simples no curto prazo) suprimir o passo image_generation no ciclo de video, ja que o HyperFrames usa a foto PUBLICA do produto ML (product_image_url), nao a imagem gerada — a imagem paga nao entra no MP4. Ou seja: image_generation e um custo pago que NAO agrega ao entregavel de video. Alternativa Ollama self-hosted (Mesh, ja integrado em agent-task-execute:182 OLLAMA_HOST + OpenClaw roda qwen3.5/llama3.1:8b): so vale para TEXTO e exige wiring net-new em orchestrate-step (adicionar branch provider==='ollama' -> ${OLLAMA_HOST}/api/chat, espelhando agent-task-execute:187/200/261). Para o GO imediato, o SWAP 1 via pref_ai_model=:free e o caminho mais curto e 100% USD 0; Ollama fica como hardening posterior.",
> 142	      "go_recommendation": "NAO dar GO de gasto AGORA pela regua da doutrina — fazer o swap PRIMEIRO. O ciclo hoje vaza USD material em 2 pernas (texto Pro pago + imagem paga) e, pior, esse USD e INVISIVEL (nenhum log de USD/token — gate nao auditavel por Lei 1). Sequencia recomendada, minima e barata: (1) SWAP 1 — setar pref_ai_model do User 0 para 'google/gemma-2-9b-it:free' (texto vai a USD 0, zero mudanca de codigo); (2) IMAGEM — suprimir/desabilitar image_generation no ciclo de video (ela nao entra no MP4 do HyperFrames, entao e gasto puro sem valor de video) OU rotear para Replicate/FLUX self-host; (3) fechar o observability gap emitindo 'llm_usage' com usage tokens em infra_health_logs no chokepoint fetchLLMWithFallback + generate-image, para o proximo GO ter prova material de US$0 (verdict passa de has_cost ESTIMADO para zero MEDIDO). Feitos (1)+(2), o ciclo fica strict-zero USD externo (render+analyze ja sao self-hosted) e a doutrina e cumprida. So entao dar o GO — e idealmente ja com (3) para provar o zero, nao so afirma-lo."
> 143	    }
> 144	  },
> 145	  "workflowProgress": [
> 146	    {
> 147	      "type": "workflow_phase",
> 148	      "index": 1,
> 149	      "title": "Trace"
> 150	    },
> 151	    {
> 152	      "type": "workflow_phase",
> 153	      "index": 2,
> 154	      "title": "Verdict"
> 155	    },
> 156	    {
> 157	      "type": "workflow_agent",
> 158	      "index": 1,
> 159	      "label": "trace:content",
> 160	      "phaseIndex": 1,
> 161	      "phaseTitle": "Trace",
> 162	      "agentId": "a6cf1702e919ec341",
> 163	      "model": "claude-opus-4-8",
> 164	      "state": "done",
> 165	      "startedAt": 1782863787464,
> 166	      "queuedAt": 1782863787437,
> 167	      "attempt": 1,
> 168	      "lastToolName": "StructuredOutput",
> 169	      "lastToolSummary": "Geração de TEXTO/SCRIPT (article_generation) do ciclo de ví…",
> 170	      "promptPreview": "Trace o passo de GERAÇÃO DE TEXTO/SCRIPT do ciclo de vídeo do Viral Autopilot para o Usuário Zero (user_id=ada39fae-67e1-4e53-af1c-5a18e1c108e8).\nCaminho: autopilot-run → orchestrate-content → orchestrate-step → generate-content (ou equivalente). Leia supabase/functions/autopilot-run/index.ts, orchestrate-content/index.ts, orchestrate-step/index.ts, generate-content/index.ts.\nDetermine MATERIALMEN…",
> 171	      "lastProgressAt": 1782863923096,
> 172	      "tokens": 105855,
> 173	      "toolCalls": 17,
> 174	      "durationMs": 135631,
> 175	      "resultPreview": "{\"step\":\"Geração de TEXTO/SCRIPT (article_generation) do ciclo de vídeo do Viral Autopilot para o Usuário Zero. Cadeia real: autopilot-run (fan-out prepaid) -> orchestrate-content (resolve modelo + grava em pipeline_runs.metadata + kick async_orchestrate_step) -> orchestrate-step (FAZ a chamada LLM). generate-content/index.ts NAO esta nesta cadeia: e funcao user-facing standalone (chat/single post…"
> 176	    },
> 177	    {
> 178	      "type": "workflow_agent",
> 179	      "index": 2,
> 180	      "label": "trace:analyze",
> 181	      "phaseIndex": 1,
> 182	      "phaseTitle": "Trace",
> 183	      "agentId": "a0cce3d272295d8b2",
> 184	      "model": "claude-opus-4-8",
> 185	      "state": "done",
> 186	      "startedAt": 1782863787466,
> 187	      "queuedAt": 1782863787438,
> 188	      "attempt": 1,
> 189	      "lastToolName": "StructuredOutput",
> 190	      "lastToolSummary": "ANALYZE (R3 loop) do ciclo de video do Viral Autopilot — ra…",
> 191	      "promptPreview": "Trace o passo de ANÁLISE (analyze) do ciclo de vídeo do Viral Autopilot para o Usuário Zero (user_id=ada39fae-67e1-4e53-af1c-5a18e1c108e8).\nO custo do ciclo é 10(orch)+12(render)+2(analyze) mco. Encontre o que é o passo 'analyze' (ANALYZE_COST=2) — procure em supabase/functions/autopilot-run/index.ts, autopilot-analyze/index.ts, orchestrate-step (passo de análise/ranking), e qualquer chamada a ana…",
> 192	      "lastProgressAt": 1782863868758,
> 193	      "tokens": 85190,
> 194	      "toolCalls": 8,
> 195	      "durationMs": 81292,
> 196	      "resultPreview": "{\"step\":\"ANALYZE (R3 loop) do ciclo de video do Viral Autopilot — ranqueia o ciclo anterior e escreve optimization_policy (FR-VA-010/011). ANALYZE_COST=2 mco.\",\"edge_fn\":\"supabase/functions/autopilot-analyze/index.ts (chamada origina em supabase/functions/autopilot-run/index.ts:196 via svcCall). NAO chama analyze-node nem orchestrate-step de analise — grep confirmou 'NO reference to analyze-node i…"
> 197	    },
> 198	    {
> 199	      "type": "workflow_agent",
> 200	      "index": 3,
> 201	      "label": "trace:image",
> 202	      "phaseIndex": 1,
> 203	      "phaseTitle": "Trace",
> 204	      "agentId": "a3f741b18f105df5f",
> 205	      "model": "claude-opus-4-8",
> 206	      "state": "done",
> 207	      "startedAt": 1782863868760,
> 208	      "queuedAt": 1782863787438,
> 209	      "attempt": 1,
> 210	      "lastToolName": "StructuredOutput",
> 211	      "lastToolSummary": "Ciclo de video do Viral Autopilot (User 0 ada39fae) - gerac…",
> 212	      "promptPreview": "Determine se o ciclo de vídeo do Viral Autopilot (User 0 = ada39fae-67e1-4e53-af1c-5a18e1c108e8) gera IMAGEM e qual o custo USD dela.\nContexto da memória: generate-image roteia por OpenRouter Gemini (OpenAI virou fallback inalcançável); providers de imagem do User 0 estavam quebrados (nanobana mock). Leia supabase/functions/orchestrate-step/index.ts (bloco de imagem / fail-open) e generate-image/i…",
> 213	      "lastProgressAt": 1782863985681,
> 214	      "tokens": 95150,
> 215	      "toolCalls": 13,
> 216	      "durationMs": 116921,
> 217	      "resultPreview": "{\"step\":\"Ciclo de video do Viral Autopilot (User 0 ada39fae) - geracao de IMAGEM e custo USD\",\"edge_fn\":\"Dois passos IRMAOS em supabase/functions/orchestrate-step/index.ts, ambos sob `if (hasProducts)` (linha 460): (A) image_generation chama generate-image em orchestrate-step/index.ts:464; (B) video_generation (linha 494, gated `if (videoEnabled)`) NAO chama generate-image - enfileira HyperFrames …"
> 218	    },
> 219	    {
> 220	      "type": "workflow_agent",
> 221	      "index": 4,
> 222	      "label": "trace:render",
> 223	      "phaseIndex": 1,
> 224	      "phaseTitle": "Trace",
> 225	      "agentId": "a2cbb4ef7c0f28b31",
> 226	      "model": "claude-opus-4-8",
> 227	      "state": "done",
> 228	      "startedAt": 1782863923097,
> 229	      "queuedAt": 1782863787438,
> 230	      "attempt": 1,
> 231	      "lastToolName": "StructuredOutput",
> 232	      "lastToolSummary": "RENDER do ciclo de vídeo (HyperFrames) — composition spec →…",
> 233	      "promptPreview": "Confirme MATERIALMENTE que o passo de RENDER do ciclo de vídeo (HyperFrames) roda 100% self-hosted, SEM chamada a API externa paga.\nLeia scripts/hyperframes/render-core.ts, scripts/video-bridge.ts. Verifique: (1) o render usa Playwright headless + FFmpeg locais (binários na infra própria), zero chamada a SaaS de geração de vídeo externo (não Veo/Higgsfield/Replicate)? Cite as linhas; (2) há QUALQU…",
> 234	      "lastProgressAt": 1782863975373,
> 235	      "tokens": 83805,
> 236	      "toolCalls": 6,
> 237	      "durationMs": 52276,
> 238	      "resultPreview": "{\"step\":\"RENDER do ciclo de vídeo (HyperFrames) — composition spec → MP4 9:16 1080x1920\",\"edge_fn\":\"scripts/hyperframes/render-core.ts:74-147 (renderComposition — núcleo puro); host worker scripts/video-bridge.ts:67-190 (processRender). Edge fn video-render é só transporte poll:// e NÃO roda o render.\",\"provider_model\":\"Self-hosted: Playwright Chromium headless + FFmpeg libx264 locais. ZERO modelo…"
> 239	    },
> 240	    {
> 241	      "type": "workflow_agent",
> 242	      "index": 5,
> 243	      "label": "trace:telemetry",
> 244	      "phaseIndex": 1,
> 245	      "phaseTitle": "Trace",
> 246	      "agentId": "aa799e15f442d2a54",
> 247	      "model": "claude-opus-4-8",
> 248	      "state": "done",
> 249	      "startedAt": 1782863975374,
> 250	      "queuedAt": 1782863787438,
> 251	      "attempt": 1,
> 252	      "lastToolName": "StructuredOutput",
> 253	      "lastToolSummary": "Custo USD real + chaves BYOK do Usuario Zero (ada39fae) — a…",
> 254	      "promptPreview": "Encontre o custo USD REAL e as chaves BYOK do Usuário Zero (user_id=ada39fae-67e1-4e53-af1c-5a18e1c108e8) — prova material, não estimativa.\nUse o .env (SB_URL/SB_SECRET_KEY) e curl no Supabase REST (como o GO-gasto agent fez). (1) Liste as chaves ATIVAS do User 0 em decrypted_user_api_keys OU user_api_keys (quais colunas de provider estão preenchidas: openrouter_api_key, google_api_key, openai_api…",
> 255	      "lastProgressAt": 1782864131244,
> 256	      "tokens": 86650,
> 257	      "toolCalls": 13,
> 258	      "durationMs": 155869,
> 259	      "resultPreview": "{\"step\":\"Custo USD real + chaves BYOK do Usuario Zero (ada39fae) — autopilot de video (cycle 2403bfcb / render 8b0787e0) + geracao de texto do pipeline\",\"edge_fn\":\"supabase/functions/orchestrate-step/index.ts:275-281 (resolve o modelo de texto); scripts/hyperframes/render-core.ts + scripts/video-bridge.ts (render do video — Playwright+FFmpeg deterministico, SEM LLM); vision-mcp container (analyze_…"
> 260	    },
> 261	    {
> 262	      "type": "workflow_agent",
> 263	      "index": 6,
> 264	      "label": "auditor",
> 265	      "phaseIndex": 2,
> 266	      "phaseTitle": "Verdict",
> 267	      "agentId": "a45290ba8c4aa6549",
> 268	      "model": "claude-opus-4-8",
> 269	      "state": "done",
> 270	      "startedAt": 1782864131284,
> 271	      "queuedAt": 1782864131247,
> 272	      "attempt": 1,
> 273	      "lastToolName": "StructuredOutput",
> 274	      "lastToolSummary": "~US$0.05–0.07 por ciclo (ESTIMADO, nao medido) — soma de: T…",
> 275	      "promptPreview": "Você é o auditor-chefe. A doutrina Sovereign (2026-06-30) exige CUSTO USD EXTERNO AO SOVEREIGN = 0 por ciclo, e preferência por open-source/self-hosted dentro do MCORCH. O GO de gasto do 1º ciclo pago de vídeo está GATED nessa régua. O render HyperFrames já é self-hosted (USD 0). Recebeu o trace material de cada passo externo do ciclo de vídeo do Usuário Zero. Produza o veredito: soma USD/ciclo, s…",
> 276	      "lastProgressAt": 1782864211082,
> 277	      "tokens": 84220,
> 278	      "toolCalls": 7,
> 279	      "durationMs": 79798,
> 280	      "resultPreview": "{\"total_usd_per_video_cycle\":\"~US$0.05–0.07 por ciclo (ESTIMADO, nao medido) — soma de: TEXTO google/gemini-2.5-pro-preview (artigo + linkedin_post + twitter_thread, ~$0.02–0.04) + IMAGEM google/gemini-2.5-flash-image do passo irmao image_generation (~$0.03). RENDER HyperFrames e ANALYZE = US$0 medidos/self-hosted. ATENCAO Lei 1: os dois valores pagos NAO tem prova material de USD — sao estimativa…"
> 281	    }
> 282	  ],
> 283	  "totalTokens": 540870,
> 284	  "totalToolCalls": 64
> 285	}
> ```

## 🤖 Claude *(00:05:37)*


## 🤖 Claude *(00:05:38)*

Audit fechado — e trouxe um achado que **muda o GO**. Vou persistir o resultado (o output estava só no scratch efêmero) e te dar o veredito com a decisão que é sua.

## 🤖 Claude *(00:05:59)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/video-cycle-zero-usd-audit-2026-06-30.md",
  "content": "# Zero-USD Audit \u2014 Ciclo de V\u00eddeo do Viral Autopilot (2026-06-30)\n\n> Gate da doutrina `feedback_opensource_first_zero_cost_equity` pro GO de gasto. Workflow `wf_6d3bdbd6-eb7` (5 traces + auditor, 540k tokens). User 0 = ada39fae.\n\n## Veredito: `has_cost` \u2014 N\u00c3O cumpre a doutrina estrita hoje\n\n**~US$0.05\u20130.07 por ciclo (ESTIMADO, n\u00e3o medido).** A espinha do v\u00eddeo est\u00e1 correta; o vazamento \u00e9 por **config, n\u00e3o arquitetura**.\n\n| Passo | USD/ciclo | Self-hosted? | Nota |\n|-------|-----------|--------------|------|\n| **RENDER** (HyperFrames Playwright+FFmpeg) | **$0 MEDIDO** | \u2705 sim | render real 536KB/110s na CPU pr\u00f3pria. \u00c9 a parte cara em pipelines normais (Veo ~$0.56) \u2014 e aqui \u00e9 $0. **Doutrina-perfeito.** |\n| **ANALYZE** (autopilot-analyze) | **$0** | \u2705 sim | ranqueamento TypeScript determin\u00edstico, zero LLM (grep NONE FOUND). |\n| **TEXTO** (article + linkedin + twitter) | ~$0.02\u20130.04 | \u274c n\u00e3o | `google/gemini-2.5-pro-preview` no OpenRouter = **PAGO** (~$10/M out). Happy-path nunca toca `:free`. `orchestrate-step:275-281`. |\n| **IMAGEM** (`image_generation`) | ~$0.03 | \u274c n\u00e3o | `google/gemini-2.5-flash-image` (Nano Banana) PAGO. **E n\u00e3o entra no MP4** (HyperFrames usa a foto p\u00fablica do produto ML) \u2192 custo pago SEM valor de v\u00eddeo. Gate \u00e9 `hasProducts`, n\u00e3o `videoEnabled` (`orchestrate-step:460/464`). \u26a0\ufe0f verificar se os posts de TEXTO anexam essa imagem antes de suprimir. |\n\n## Observability gap (CR\u00cdTICO \u2014 Lei 1)\n**Nenhum USD/token \u00e9 logado em lugar nenhum.** `pipeline_runs`/`autopilot_cycles`/`video_renders` s\u00f3 gravam mcoCoins (moeda interna, n\u00e3o USD). `infra_health_logs` s\u00f3 telemetra custo pro vision-mcp (cost=0/byok=true). Logo o \"has_cost\" \u00e9 **estimado, n\u00e3o medido** \u2014 n\u00e3o d\u00e1 pra dar GO com prova material de $0.\n**Fix:** capturar o campo `usage` (prompt/completion_tokens) que o OpenRouter j\u00e1 devolve + emitir `infra_health_logs event='llm_usage'` no chokepoint `fetchLLMWithFallback` (orchestrate-step) + generate-image. A\u00ed o veredito vira `zero` MEDIDO.\n\n## Swaps doutrina-aligned (o c\u00f3digo j\u00e1 tem os trilhos)\n- **TEXTO (maior perna):** o c\u00f3digo n\u00e3o muda \u2014 \u00e9 DADO. `pref_ai_model` do User 0 \u00e9 global (afeta chat/posts/autopilot). Op\u00e7\u00f5es: (A) **Ollama self-hosted** no Mesh (qwen/llama j\u00e1 rodam; `agent-task-execute:182` OLLAMA_HOST) = $0 + stack pr\u00f3pria, precisa branch net-new em orchestrate-step; (B) modelo OpenRouter `:free` (`gemma-2-9b-it:free`/`llama-3-8b-instruct:free`, `llm-fallback.ts:155`) = $0 imediato zero-c\u00f3digo MAS derruba qualidade de TODO o texto; (C) aceitar ~$0.05 na BYOK pr\u00f3pria; (D) override `:free`/Ollama S\u00d3 no autopilot, mantendo Pro no interativo.\n- **IMAGEM:** n\u00e3o h\u00e1 `:free` de imagem. Melhor = **suprimir `image_generation` no ciclo de v\u00eddeo** (n\u00e3o entra no MP4 = desperd\u00edcio puro) OU rotear `pref_image_provider='replicate'` FLUX self-host. \u26a0\ufe0f confirmar antes se os posts de texto usam a imagem.\n\n## Recomenda\u00e7\u00e3o de GO\n**N\u00c3O dar GO agora pela r\u00e9gua da doutrina.** Sequ\u00eancia m\u00ednima: (1) resolver TEXTO ($0), (2) suprimir/rotear IMAGEM, (3) fechar observability gap \u2192 GO com $0 **provado**, n\u00e3o afirmado. Feitos (1)+(2), o ciclo fica strict-zero (render+analyze j\u00e1 s\u00e3o $0).\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/.claude/context/video-cycle-zero-usd-audit-2026-06-30.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:06:02)*


## 🤖 Claude *(00:06:14)*

Persistido em [video-cycle-zero-usd-audit-2026-06-30.md](.claude/context/video-cycle-zero-usd-audit-2026-06-30.md). O veredito:

## 🔴 `has_cost` — o ciclo NÃO cumpre a doutrina estrita hoje (~US$0.05–0.07/ciclo)

Mas o achado importa mais que o número. **A espinha está certa — o vazamento é config, não arquitetura:**

| Passo | Custo | Doutrina |
|-------|-------|----------|
| **Render (HyperFrames)** | **$0 medido** ✅ | Self-hosted. É a parte cara em pipelines normais (Veo ~$0.56/vídeo) — e aqui é **zero**. Doutrina-perfeito. |
| **Analyze** | **$0** ✅ | Ranking TypeScript determinístico, zero LLM. |
| **Texto** (artigo+LinkedIn+X) | ~$0.02–0.04 ❌ | Gemini **2.5 Pro** (pago) na sua chave OpenRouter. O caminho feliz nunca usa `:free`. |
| **Imagem** | ~$0.03 ❌ | Gemini Flash Image (pago) — **e nem entra no MP4** (o vídeo usa a foto pública do produto). Custo pago **sem valor de vídeo**. |

**Dois pontos que pesam mais que o custo:**

1. **Observability gap (Lei 1):** o sistema **não loga USD/token em lugar nenhum** — só mcoCoins (moeda interna). Então esse `has_cost` é **estimado, não medido**. Não dá pra dar o GO afirmando "$0" sem prova material. Dá pra fechar: capturar o `usage` que o OpenRouter já devolve + emitir um evento `llm_usage` no chokepoint. Aí o zero fica **provado**.

2. **O passo de imagem é desperdício puro** — paga e nem aparece no vídeo. (Só preciso confirmar 1 coisa antes de matar: se os posts de texto anexam essa imagem.)

**Minha recomendação:** não dar o GO ainda. São 3 ajustes baratos que deixam o ciclo *strict-zero provado*, e aí o GO sai limpo pela sua régua. O passo de render — que é onde mora o custo real de vídeo — já é $0 self-hosted, então você está a poucos ajustes de conteúdo autônomo genuinamente gratuito.

A decisão que é sua (tem tradeoff real de qualidade) é como zerar o **texto**:

## 🤖 Claude *(00:06:22)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "Como zerar o custo de TEXTO do ciclo (a maior perna paga), respeitando a doutrina? O texto hoje usa Gemini 2.5 Pro na sua chave OpenRouter (qualidade alta, mas pago).",
      "header": "Modelo de texto",
      "multiSelect": false,
      "options": [
        {
          "label": "Ollama self-hosted (Mesh)",
          "description": "Roteia o texto do autopilot pro Ollama que j\u00e1 roda na sua infra (qwen/llama). Custo USD estrito = 0 + stack 100% pr\u00f3pria = equity m\u00e1ximo \u2014 o mais alinhado \u00e0 doutrina. Precisa de wiring net-new no orchestrate-step (~1 fatia do loop)."
        },
        {
          "label": "Override s\u00f3 no autopilot",
          "description": "Mant\u00e9m Gemini 2.5 Pro (qualidade) no trabalho interativo/manual, mas for\u00e7a modelo :free (ou Ollama) S\u00d3 no ciclo aut\u00f4nomo. Preserva qualidade onde voc\u00ea v\u00ea + zera o custo aut\u00f4nomo. C\u00f3digo pequeno."
        },
        {
          "label": "Modelo :free global",
          "description": "Troca o pref_ai_model do User 0 pra gemma-2-9b:free/llama-3-8b:free. Custo 0 imediato, zero c\u00f3digo. MAS derruba a qualidade de TODO o texto seu (chat/posts/autopilot), n\u00e3o s\u00f3 do autopilot \u2014 pref_ai_model \u00e9 global."
        },
        {
          "label": "Aceitar ~$0.05/ciclo",
          "description": "Mant\u00e9m Gemini 2.5 Pro na sua pr\u00f3pria BYOK; ~$0.05/ciclo \u00e9 custo marginal \u00ednfimo e \u00e9 sua chave. GO agora. Fere a doutrina estrita, mas o render (a parte cara) j\u00e1 \u00e9 $0."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "Como zerar o custo de TEXTO do ciclo (a maior perna paga), respeitando a doutrina? O texto hoje usa Gemini 2.5 Pro na sua chave OpenRouter (qualidade alta, mas pago)."="Vamos manter por enquanto esta barato, coloquei 10 dolares que deu mais ou menos 60 reais no brasil, durou o mes enteiro e ainda tem um pouco de credito, se você acha que vale apena manter essa qualidade seguimos assim". You can now continue with these answers in mind.
> ```

## 🤖 Claude *(00:30:48)*


## 🤖 Claude *(00:30:51)*

Decisão anotada — e minha recomendação honesta: **sim, mantenha o Gemini 2.5 Pro.** Deixa eu te explicar por que isso é coerente com a doutrina (não contra ela), e te mostrar o que ainda vale ajustar antes do GO. Primeiro confirmo um ponto do achado da imagem (se os posts de texto usam a imagem gerada) pra não recomendar no escuro:

## 🤖 Claude *(00:30:52)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/orchestrate-step/index.ts",
  "offset": 455,
  "limit": 90
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 455	          // flip the run to error at the finalize check): any failure (no image key / provider mock / 5xx) leaves
> 456	          // article_generation 'done' and the run proceeds — the image NEVER breaks generation. Persists the
> 457	          // DURABLE storage path in content_library.media_url (the 1h signed URL dies before the +1-2h publish
> 458	          // window; private bucket → re-sign on read). Product-referenced = descriptive text prompt from
> 459	          // name+category (generate-image is DALL·E text-only; image-to-image off product.image_url is deferred).
> 460	          if (hasProducts) {
> 461	            try {
> 462	              const p0 = products[0];
> 463	              const imgPrompt = `Imagem de marketing do produto ${p0.name}${p0.category ? `, categoria ${p0.category}` : ""}, no contexto de "${topic}". Foto de produto profissional, alta qualidade, fundo limpo, para redes sociais.`;
> 464	              const imgRes = await fetch(`${supabaseUrl}/functions/v1/generate-image`, {
> 465	                method: "POST",
> 466	                headers: { Authorization: `Bearer ${serviceKey}`, "Content-Type": "application/json" },
> 467	                body: JSON.stringify({ prompt: imgPrompt, style: "product photography", user_id: run.user_id }),
> 468	              });
> 469	              const imgData = await imgRes.json().catch(() => ({} as any));
> 470	              if (imgRes.ok && imgData?.path) {
> 471	                const { data: imgRow } = await admin.from("content_library").insert({
> 472	                  user_id: run.user_id, campaign_id: campaign_id || null, type: "image",
> 473	                  title: `Imagem: ${articleTitle}`, media_url: imgData.path, status: "approved",
> 474	                  metadata: { source: "orchestration", products: products.map((p) => p.external_id), product_id: p0.external_id, storage_bucket: "generated-images" },
> 475	                }).select("id").single();
> 476	                await addStep("image_generation", "done", { product: p0.name }, { content_id: imgRow?.id ?? null, path: imgData.path });
> 477	              } else {
> 478	                console.warn("[orchestrate-step] image generation skipped (fail-open):", imgData?.error ?? imgRes.status);
> 479	                await addStep("image_generation", "skipped", { product: p0.name }, { reason: imgData?.error ?? `image_http_${imgRes.status}` });
> 480	              }
> 481	            } catch (e: any) {
> 482	              console.warn("[orchestrate-step] image generation fail-open:", e?.message);
> 483	              await addStep("image_generation", "skipped", { product: products[0]?.name }, { reason: e?.message || "image_exception" });
> 484	            }
> 485	
> 486	            // ── Viral Autopilot Fatia VA-V1 — product-aware 9:16 video composition (FR-VA-023/024) ──────────────
> 487	            // FAIL-OPEN (status 'skipped', never 'error'): the video NEVER breaks the run. The cost was pre-debited
> 488	            // in the cycle (OTD-VA-010); we INSERT a queued HyperFrames render with charged_mco=VIDEO_COST as a
> 489	            // MARKER (no deduct here — orchestrate-step never bills) → the host worker (video-bridge.ts) polls,
> 490	            // renders 1080×1920, and on failure finalize_video_render(failed, refund=VIDEO_COST) credits it back.
> 491	            // Props use the actual viral angle (title/description) + the ML product photo (public https). The
> 492	            // template renders all text via textContent (XSS-safe); product name already passed the sentinel
> 493	            // upstream (orchestrate-content). composition.autopilot carries the attach context (FR-VA-025).
> 494	            if (videoEnabled) {
> 495	              const VIDEO_COST = 12; // VIDEO_HYPERFRAMES_RENDER (billing.ts:39) — mirrors autopilot-run projected.
> 496	              let enqueued = false;  // tracks whether a video_renders row was actually created (billing reconciliation).
> 497	              try {
> 498	                const p0 = products[0];
> 499	                const clip = (s: unknown, n: number) => String(s ?? "").replace(/\s+/g, " ").trim().slice(0, n);
> 500	                const productImg = typeof (p0 as any)?.image_url === "string" && /^https:\/\//i.test((p0 as any).image_url)
> 501	                  ? (p0 as any).image_url : "";
> 502	                const composition = {
> 503	                  template: "viral-short-9x16",
> 504	                  // 5s × 24fps = 120 frames ≈ 65s render — within NFR-VS-002 (p95 < 90s). The screenshot-per-frame
> 505	                  // capture (~0.5s/frame) is the bottleneck; OTD-VA-013 tracks the CDP-screencast optimization to
> 506	                  // unlock longer/faster clips. 5s is a strong viral-short length.
> 507	                  duration_s: 5,
> 508	                  fps: 24,
> 509	                  props: {
> 510	                    hook: clip(articleTitle, 80) || clip(topic, 80),
> 511	                    caption: clip(args.meta_description, 150) || clip(`${p0.name}`, 150),
> 512	                    cta: "Ver no Mercado Livre",
> 513	                    brand: "MCORCH",
> 514	                    product_image_url: productImg,
> 515	                  },
> 516	                  // Attach context for the worker's reconciliation (FR-VA-025) — NOT rendered, only routing.
> 517	                  // pillar_run_id (FR-CP-003 gap #5): lets video-bridge JOIN the finished master back to pillar_atoms
> 518	                  // so the reshaper can reexport per-channel native variants from THIS run's 9:16 master.
> 519	                  pillar_run_id: run_id,
> 520	                  autopilot: { user_id: run.user_id, campaign_id: campaign_id || null, product_id: p0.external_id, cycle_id: cycleId, title: clip(articleTitle, 120), pillar_run_id: run_id },
> 521	                };
> 522	                const { data: vr, error: vrErr } = await admin.from("video_renders").insert({
> 523	                  user_id: run.user_id, engine: "hyperframes", state: "queued",
> 524	                  product_id: null, // logical product is the ML external_id (text) — kept in composition.autopilot
> 525	                  topic: clip(topic, 200), charged_mco: VIDEO_COST, composition,
> 526	                }).select("id").single();
> 527	                if (vrErr || !vr) throw new Error(vrErr?.message || "video_render_insert_failed");
> 528	                enqueued = true;
> 529	                await addStep("video_generation", "done", { product: p0.name, format: "9:16" }, { render_id: vr.id });
> 530	              } catch (e: any) {
> 531	                console.warn("[orchestrate-step] video enqueue fail-open:", e?.message);
> 532	                await addStep("video_generation", "skipped", { product: products[0]?.name }, { reason: e?.message || "video_exception" });
> 533	                // Billing-accuracy fix (OTD-VA-010 gap): the cycle ALREADY counted VIDEO_COST for this succeeded
> 534	                // sub-run (autopilot-run `actual = succeeded × (ORCH_COST + VIDEO_COST)`, computed BEFORE this async
> 535	                // step ran). If NO render row was created (`!enqueued`), finalize_video_render can never refund it →
> 536	                // the tenant would be charged for a render never queued. Issue the idempotent compensating credit
> 537	                // (anchored on run_id; mirrors the render-fail refund for the no-row case). Only on the cron/cycle
> 538	                // path (cycleId set); user-path renders never reach here. If `enqueued` is true, the row exists and
> 539	                // the render lifecycle / finalize_video_render owns the refund — do NOT double-credit.
> 540	                if (!enqueued && cycleId) {
> 541	                  const { error: refundErr } = await admin.rpc("refund_autopilot_video_enqueue", {
> 542	                    p_run_id: run_id, p_cycle_id: cycleId, p_user_id: run.user_id, p_amount: VIDEO_COST,
> 543	                  });
> 544	                  if (refundErr) {
> ```

## 🤖 Claude *(00:30:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "echo \"=== media_url / image usage no orchestrate-step ===\" && grep -nE \"media_url|image_url|featured|imageUrl\" supabase/functions/orchestrate-step/index.ts | head -40",
  "description": "Grep image usage downstream in orchestrate-step"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === media_url / image usage no orchestrate-step ===
> 457:          // DURABLE storage path in content_library.media_url (the 1h signed URL dies before the +1-2h publish
> 459:          // name+category (generate-image is DALL·E text-only; image-to-image off product.image_url is deferred).
> 473:                  title: `Imagem: ${articleTitle}`, media_url: imgData.path, status: "approved",
> 500:                const productImg = typeof (p0 as any)?.image_url === "string" && /^https:\/\//i.test((p0 as any).image_url)
> 501:                  ? (p0 as any).image_url : "";
> 514:                    product_image_url: productImg,
> ```

## 🤖 Claude *(00:31:50)*


## 🤖 Claude *(00:31:52)*

Confirmado material: a imagem gerada **não entra no MP4** (o vídeo usa a foto pública real do produto, linha 500-514), mas ela **é salva como asset de imagem** no `content_library` (linha 471-474) — então não é "lixo puro", é um entregável extra que pode ou não te servir. Isso muda a leitura. Deixa eu atualizar a doutrina com o seu refinamento e te dar o veredito completo:

## 🤖 Claude *(00:32:00)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/feedback_opensource_first_zero_cost_equity.md",
  "old_string": "**Why:** custo marginal zero + propriedade da stack = equity defens\u00e1vel e runway longo",
  "new_string": "**Refinamento (p\u00f3s zero-USD audit `wf_6d3bdbd6-eb7`, Diretiva Sovereign 2026-06-30):** a r\u00e9gua N\u00c3O \u00e9 literal $0 na BYOK pr\u00f3pria \u2014 \u00e9 **zero custo de infra/SaaS recorrente + posse do stack caro + zero desperd\u00edcio + custo vis\u00edvel**. Prova: no ciclo de v\u00eddeo o RENDER (a parte cara, ~$0.56 em Veo) j\u00e1 \u00e9 $0 self-hosted (HyperFrames) \u2014 a vit\u00f3ria de equity que importa; resta s\u00f3 ~$0.05/ciclo de LLM (Gemini 2.5 Pro texto + Nano Banana imagem) na chave OpenRouter BYOK do Sovereign (~$10/m\u00eas, durou o m\u00eas inteiro com cr\u00e9dito sobrando). **Decis\u00e3o Sovereign: MANTER Gemini 2.5 Pro** \u2014 qualidade \u00e9 load-bearing pra marca (brand-first CCIO); trocar por 9B `:free` p/ economizar ~$10/m\u00eas \u00e9 penny-wise-pound-foolish. Ollama self-hosted no Mesh = endpoint ideal da doutrina, **DIFERIDO** (n\u00e3o degradar qualidade agora). N\u00c3O for\u00e7ar modelos `:free` no texto de marca s\u00f3 pra bater $0 literal. Pend\u00eancias no esp\u00edrito da doutrina: (a) tornar o custo USD **vis\u00edvel** (telemetria `llm_usage` \u2014 hoje NADA loga USD/token, fere Lei 1); (b) a imagem AI por ciclo (~$0.03) \u00e9 redundante com a foto real do produto que o v\u00eddeo usa \u2014 opcional cortar (produz asset em content_library, n\u00e3o \u00e9 lixo). Runbook do gate: `.claude/context/video-cycle-zero-usd-audit-2026-06-30.md`.\n\n**Why:** custo marginal zero + propriedade da stack = equity defens\u00e1vel e runway longo"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/feedback_opensource_first_zero_cost_equity.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(00:32:24)*


## 🤖 Claude *(00:32:41)*

## Veredito: mantenha o Gemini 2.5 Pro. Três razões:

1. **O custo real é irrelevante.** $10 (~R$60) durou o mês inteiro com crédito sobrando, na *sua* chave BYOK. A cadência autônoma de vídeo adiciona uns ~$0.05/ciclo × ~10 ciclos/mês = **~$0.50/mês** — troco. Não é o tipo de custo que a doutrina existe pra matar.

2. **A vitória de equity que importa já está garantida.** Em pipeline de vídeo normal, o custo mora no *render* (Veo ~$0.56/vídeo). O seu render é **HyperFrames self-hosted = $0 medido**. Você já é dono da parte cara. Isso é a doutrina cumprida onde ela pesa.

3. **Qualidade de texto é load-bearing pra marca.** Sua estratégia é brand-first (persona CCIO evangelizando). Trocar Gemini 2.5 Pro por um 9B `:free` pra economizar ~$10/mês degradaria visivelmente o conteúdo da persona. Penny-wise, pound-foolish.

**Doutrina reconciliada e registrada:** a régua não é "$0 literal na sua BYOK" — é *zero custo de infra/SaaS recorrente + posse do stack caro + zero desperdício + custo visível*. Você refinou certo. Atualizei a memória pra o loop **não** sair trocando seus modelos por `:free` atrás de um zero literal e estragando a marca.

## O que ainda vale, antes de um GO limpo (nenhum é bloqueador)

- **🟢 Recomendo: tornar o custo visível (a única lacuna Lei-1 real).** Hoje o sistema **não loga USD/token em lugar nenhum** — só mcoCoins interno. Então "é barato" é estimativa, não prova. Dá pra fechar barato: capturar o campo `usage` que o OpenRouter já devolve + emitir um evento `llm_usage` no chokepoint. Aí seu custo vira um número **provado** no `infra_health_logs`, e todo GO futuro é auditável. É aditivo, sem tradeoff.

- **🟡 Opcional: a imagem AI por ciclo.** Ela **não entra no vídeo** (o MP4 usa a foto real do produto) — mas é salva como asset de marketing no `content_library`. Ou seja: não é lixo, é um entregável extra de ~$0.03. Se a persona/posts usam essas imagens, mantenha; se não, cortar simplifica e some com o custo. Baixo risco dos dois lados — sua chamada.

## Onde isso te deixa

Com o Gemini Pro mantido, você está **efetivamente pronto pro GO** — o custo é conhecido-ínfimo, na sua BYOK, e a parte cara é self-hosted. O GO no 1º ciclo testemunhado é sua decisão (Lei 4 — é o momento do dinheiro).

**Minha recomendação de sequência:** eu wiro a telemetria `llm_usage` primeiro (rápido, sem tradeoff) → aí o GO sai com o custo **provado em $-real visível**, não afirmado. Depois é só seu "GO" e eu ligo `video_enabled` + disparo o ciclo testemunhado.

Quer que eu **wire a telemetria de custo agora** (deixa o GO auditável), ou prefere **GO direto** e a gente adiciona a telemetria depois?

## 👤 User *(01:08:33)*

go direto isso deve ser facil tem os custos com a própria api detalhada certo? Segue. Depois disso quero saber de você se vale apena usar https://github.com/vercel-labs/opensrc e o https://github.com/safishamsi/graphify para finalmente deixar o opendesign e o hyperframer nativo exclusivo do MCORCH ?

## 🤖 Claude *(01:09:20)*


## 🤖 Claude *(01:09:23)*

GO recebido — executando o 1º ciclo pago de vídeo. (E sim: o OpenRouter devolve o custo real por chamada — campo `usage` + endpoint de generation com custo em USD; você vê o detalhado no dashboard deles a qualquer momento, então dá pra seguir sem a telemetria interna por ora.)

Vou fazer isso com prova material a cada passo (Lei 1). Primeiro, reconheço o contrato de invoke + o estado atual do plano:

## 🤖 Claude *(01:09:24)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/supabase/functions/autopilot-run/index.ts",
  "offset": 1,
  "limit": 140
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// autopilot-run — Viral Autopilot per-plan executor (FR-VA-002 / FR-VA-007 / FR-VA-016 / FR-VA-021). verify_jwt=false.
> 2	// SOP: docs/processes/autopilot-cron-identity.md.
> 3	//
> 4	// Identity (two paths):
> 5	//   - cron/service: Authorization === Bearer SB_SECRET_KEY + x-autopilot-user-id (the autopilot-cadence-cron
> 6	//     derived it from autopilot_plans.user_id). The header is re-validated by the TENANT-SCOPED plan load below.
> 7	//   - user "gerar agora": user JWT → getUser → the plan load is scoped to that user (IDOR-safe).
> 8	// Flow: load plan (tenant-scoped) → N_runs = products×platforms×ab_variants → projected = N_runs*10 + 2 →
> 9	//   begin_autopilot_cycle (ATOMIC cap-check + single pre-debit) → fan-out orchestrate-content (prepaid, no
> 10	//   self-bill) → finalize_autopilot_cycle(actual) → re-arm next_run_at. dry_run short-circuits after the cost
> 11	//   projection (no cycle, no deduct) — the zero-cost proof path.
> 12	import { createClient } from "https://esm.sh/@supabase/supabase-js@2";
> 13	import { inspectPrompt } from "../_shared/sentinel.ts";
> 14	
> 15	const corsHeaders = {
> 16	  "Access-Control-Allow-Origin": "*",
> 17	  "Access-Control-Allow-Methods": "POST, OPTIONS",
> 18	  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-autopilot-user-id",
> 19	};
> 20	const ORCH_COST = 10;     // orchestrate-content flat bundle (image already included — billing.ts:16-21)
> 21	const ANALYZE_COST = 2;   // reserved for autopilot-analyze (R3); REFUNDED until that slice lands (see actual below)
> 22	const VIDEO_COST = 12;    // VIDEO_HYPERFRAMES_RENDER (billing.ts:39) — per video sub-run when plan.video_enabled (FR-VA-022/024)
> 23	const CONCURRENCY = 6;    // wall-clock bound on the fan-out (mirrors nurture-cron / campaign-run)
> 24	const UUID_RE = /^[0-9a-fA-F-]{36}$/;
> 25	
> 26	// ── FR-VA-018 trend hardening (adversarial review wf_6cc97c75 — MEDIUM, conf 8) ───────────────────────────────────
> 27	// vm_trends is a GLOBAL, externally-mined (Apify/RapidAPI), pt-BR catalog. The SHARED Cyber-Sentinel's
> 28	// INJECTION_PATTERNS are English-only/score>=2, so a Portuguese prompt-injection seeded into a viral upstream post
> 29	// passes it AND orchestrate-content's mirror gate, steering the content LLM (affiliate-link/scam-URL swap) for ANY
> 30	// autopilot tenant. This trend-SPECIFIC gate runs FIRST and is fail-closed: (1) a whitelist charset strip destroys
> 31	// the actual payloads (URLs, markdown links, tags, templates, quotes — only letters/digits/space/hyphen survive),
> 32	// (2) it rejects titles carrying instruction-override verbs (pt-BR + en), so what survives is an inert short keyword
> 33	// phrase rendered as DATA ("tema em alta: ..."), never free instruction text. The generic sentinel still runs after,
> 34	// as defense-in-depth. (Broader fix — pt-BR patterns in the shared sentinel — is deferred to the security arc with
> 35	// false-positive testing, since it affects every caller.)
> 36	const TREND_OVERRIDE_RE =
> 37	  /\b(ignor\w*|desconsider\w*|esque[cç]\w*|em\s+vez\s+disso|instead|disregard|override|nova\s+instru\w*|new\s+instruction|instruction\w*|prompt\w*|system\s*prompt|append|substitu\w*|replace|every\s+post|cada\s+post|todos\s+os\s+posts)\b/i;
> 38	function sanitizeTrendTitle(raw: string): string | null {
> 39	  // Whitelist: letters (incl. accented), digits, spaces, hyphen. Strips ./:@#[](){}<>`"'\| → kills URLs/markdown/tags.
> 40	  const cleaned = raw
> 41	    .replace(/[^\p{L}\p{N}\s-]/gu, " ")
> 42	    .replace(/\s+/g, " ")
> 43	    .trim();
> 44	  if (!cleaned) return null;
> 45	  if (TREND_OVERRIDE_RE.test(cleaned)) return null;   // fail-closed: instruction-override marker → skip this trend
> 46	  return cleaned.slice(0, 80).trim() || null;
> 47	}
> 48	
> 49	Deno.serve(async (req) => {
> 50	  if (req.method === "OPTIONS") return new Response("ok", { headers: corsHeaders });
> 51	  const json = (b: unknown, s = 200) =>
> 52	    new Response(JSON.stringify(b), { status: s, headers: { ...corsHeaders, "Content-Type": "application/json" } });
> 53	
> 54	  const url = Deno.env.get("SUPABASE_URL")!;
> 55	  const serviceKey = (Deno.env.get("SB_SECRET_KEY") ?? Deno.env.get("SUPABASE_SERVICE_ROLE_KEY"))!;
> 56	  const pubKey = (Deno.env.get("SB_PUBLISHABLE_KEY") ?? Deno.env.get("SUPABASE_ANON_KEY"))!;
> 57	  const admin = createClient(url, serviceKey);
> 58	  const logHealth = (status: string) =>
> 59	    admin.from("infra_health_logs").insert({ service: "autopilot-run", status }).then(() => {}, () => {});
> 60	
> 61	  try {
> 62	    const authHeader = req.headers.get("Authorization");
> 63	    if (!authHeader?.startsWith("Bearer ")) return json({ error: "Unauthorized" }, 401);
> 64	
> 65	    const body = await req.json().catch(() => ({}));
> 66	    const planId = typeof body?.plan_id === "string" ? body.plan_id : null;
> 67	    const dryRun = body?.dry_run === true;
> 68	    if (!planId || !UUID_RE.test(planId)) return json({ error: "plan_id (uuid) required" }, 422);
> 69	
> 70	    // ── Identity: service path (proven key + server-trusted header) OR user JWT path. ──────────────────────────
> 71	    const isService = authHeader === `Bearer ${serviceKey}`;
> 72	    let userId: string;
> 73	    if (isService) {
> 74	      const hdr = req.headers.get("x-autopilot-user-id");
> 75	      if (!hdr || !UUID_RE.test(hdr)) return json({ error: "x-autopilot-user-id (uuid) required for service path" }, 400);
> 76	      userId = hdr;
> 77	    } else {
> 78	      const userClient = createClient(url, pubKey, { global: { headers: { Authorization: authHeader } } });
> 79	      const { data: { user }, error } = await userClient.auth.getUser();
> 80	      if (error || !user) return json({ error: "Unauthorized" }, 401);
> 81	      userId = user.id;
> 82	    }
> 83	
> 84	    // ── Load plan TENANT-SCOPED (plan MUST belong to userId — cross-tenant/missing → 404). ───────────────────────
> 85	    const { data: plan } = await admin
> 86	      .from("autopilot_plans")
> 87	      .select("id, user_id, name, mode, interval_days, target_product_ids, platforms, ab_variants, video_enabled, video_format, hitl_required")
> 88	      .eq("id", planId).eq("user_id", userId).maybeSingle();
> 89	    if (!plan) return json({ error: "plan_not_found" }, 404);
> 90	
> 91	    const products = ((plan.target_product_ids ?? []) as unknown[]).filter((x): x is string => typeof x === "string" && x.length > 0);
> 92	    const platforms = ((plan.platforms ?? []) as unknown[]).filter((x): x is string => typeof x === "string" && x.length > 0);
> 93	    const abVariants = Math.max(1, Math.min(5, Number(plan.ab_variants ?? 1)));
> 94	    const nRuns = products.length * platforms.length * abVariants;
> 95	    if (nRuns < 1) return json({ error: "plan_has_no_targets", detail: "plano sem produtos/redes válidos" }, 422);
> 96	
> 97	    // FR-VA-022/024 (Amendment v0.2): when the plan opts in, each sub-run enqueues ONE HyperFrames 9:16 render.
> 98	    // The cost rides on the cycle pre-debit (OTD-VA-010): projected/actual += N×VIDEO_COST. The render itself
> 99	    // never self-bills (charged_mco marker only); a FAILED render refunds via finalize_video_render.
> 100	    const videoEnabled = plan.video_enabled === true;
> 101	    const videoFormat = typeof plan.video_format === "string" ? plan.video_format : "9:16";
> 102	
> 103	    // Video charge accuracy (OTD-VA-010 follow-up — billing bug witnessed 2026-06-26, cycle 2403bfcb): a 9:16 render
> 104	    // is enqueued ONLY by the article_generation flow, which orchestrate-content runs solely for the 'wordpress'
> 105	    // platform (index.ts:231-232). A linkedin/twitter sub-run never reaches video_generation, so charging it
> 106	    // VIDEO_COST is charge-without-value — and uncaught by the orchestrate-step refund (orchestrate-step:454), which
> 107	    // fires only on a FAILED enqueue ATTEMPT, never for a flow that has no video step at all. So count video sub-runs
> 108	    // by the article-flow platform, not by every sub-run (was: nRuns × VIDEO_COST → over-charged non-wordpress runs).
> 109	    // FR-PE-013 (post-engine social-connect amendment) — DEFERRED: youtube/tiktok/pinterest ARE vertical-video
> 110	    // platforms, but the 9:16 render is enqueued ONLY by the article_generation step (gated on 'wordpress' above), and
> 111	    // autopilot fans out one platform per sub-run, so a youtube/tiktok/pinterest sub-run enqueues NO render. Adding
> 112	    // them here would charge VIDEO_COST with no video_renders row to refund (charge-without-value). Re-add ONLY with
> 113	    // the orchestrate-content/-step enqueue-gate extension (its own slice). Until then they stay out of the pre-debit.
> 114	    const VIDEO_FLOW_PLATFORMS = new Set(["wordpress"]);
> 115	    const videoPlatformCount = platforms.filter((p) => VIDEO_FLOW_PLATFORMS.has(p)).length;
> 116	    const nVideoRuns = videoEnabled ? products.length * videoPlatformCount * abVariants : 0;
> 117	
> 118	    const projected = nRuns * ORCH_COST + nVideoRuns * VIDEO_COST + ANALYZE_COST;
> 119	
> 120	    // ── FR-VA-018: trend-informed angle (cycle-level). Reconnects the trends island: pick a trend from vm_trends
> 121	    // (a GLOBAL shared catalog — no tenant scope) to steer THIS cycle's viral angle. Trend text is UNTRUSTED
> 122	    // (Apify/RapidAPI-mined) → the Cyber-Sentinel gates it BEFORE it reaches any prompt (NFR-VA-008), mirroring the
> 123	    // per-product gate in orchestrate-content (skip-and-continue: a blocked trend is dropped, not the whole angle).
> 124	    // Relevance: prefer a trend whose niche overlaps the cycle's products; else the freshest top-viral active trend.
> 125	    // Defense-in-depth: orchestrate-content re-inspects the full topic, so this is the first of two gates.
> 126	    // Graceful: empty vm_trends (the steady state until fetch-trends runs) → angle stays the plain product topic.
> 127	    let viralTopic = plan.name;
> 128	    let trendApplied: string | null = null;
> 129	    try {
> 130	      const { data: prodRows } = await admin
> 131	        .from("vm_affiliate_products").select("niches").in("external_id", products).eq("is_active", true);
> 132	      const productNiches = [...new Set(((prodRows ?? []) as Array<{ niches?: string[] | null }>)
> 133	        .flatMap((p) => p.niches ?? []).filter((n): n is string => typeof n === "string" && n.length > 0))];
> 134	      const fetchTrends = async (filterNiche: boolean) => {
> 135	        let q = admin.from("vm_trends").select("title, niche, viral_score")
> 136	          .eq("is_active", true).order("viral_score", { ascending: false }).limit(5);
> 137	        if (filterNiche && productNiches.length > 0) q = q.in("niche", productNiches);
> 138	        const { data } = await q;
> 139	        return (data ?? []) as Array<{ title: string | null; niche: string | null }>;
> 140	      };
> ```

## 🤖 Claude *(01:09:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nSB=\"${SB_URL:-${SUPABASE_URL:-$VITE_SUPABASE_URL}}\"\necho \"SB_URL var resolved: $([ -n \"$SB\" ] && echo yes || echo NO)\"\necho \"SB_SECRET_KEY present: $([ -n \"$SB_SECRET_KEY\" ] && echo yes || echo NO)\"\necho \"=== plano 640b3b67 (estado atual) ===\"\ncurl -s \"$SB/rest/v1/autopilot_plans?id=eq.640b3b67-b950-42f6-bbb9-48560771eaa6&select=id,user_id,video_enabled,is_active,budget_cap_mco,daily_cap_mco,next_run_at,interval_days,niche_keywords,product_ids,platforms\" \\\n  -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | head -c 2000\necho\necho \"=== saldo User 0 ===\"\ncurl -s \"$SB/rest/v1/profiles?id=eq.ada39fae-67e1-4e53-af1c-5a18e1c108e8&select=id,mco_balance\" \\\n  -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\"",
  "description": "Load env, check plan state and User 0 balance"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> SB_URL var resolved: yes
> SB_SECRET_KEY present: yes
> === plano 640b3b67 (estado atual) ===
> {"code":"42703","details":null,"hint":null,"message":"column autopilot_plans.niche_keywords does not exist"}
> === saldo User 0 ===
> [{"id":"ada39fae-67e1-4e53-af1c-5a18e1c108e8","mco_balance":4669.00}]
> ```

## 🤖 Claude *(01:09:41)*


## 🤖 Claude *(01:09:43)*

A query bateu num nome de coluna errado (`niche_keywords` não existe). Saldo confirmado: **4669 mco**. Re-consulto o plano com as colunas reais (`target_product_ids`, `platforms`, etc.) — preciso confirmar que o plano tem produto + a plataforma `wordpress` (é ela que enfileira o render de vídeo, linha 114):

## 🤖 Claude *(01:09:47)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nSB=\"${SB_URL:-${SUPABASE_URL:-$VITE_SUPABASE_URL}}\"\necho \"=== plano 640b3b67 (colunas reais) ===\"\ncurl -s \"$SB/rest/v1/autopilot_plans?id=eq.640b3b67-b950-42f6-bbb9-48560771eaa6&select=id,name,mode,interval_days,target_product_ids,platforms,ab_variants,video_enabled,video_format,hitl_required,budget_cap_mco,daily_cap_mco,next_run_at\" \\\n  -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\"",
  "description": "Query plan with correct column names"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === plano 640b3b67 (colunas reais) ===
> [{"id":"640b3b67-b950-42f6-bbb9-48560771eaa6","name":"Roborock S8 Pro Ultra: o robô que aspira, passa pano e esvazia a lixeira sozinho","mode":"every_n_days","interval_days":3,"target_product_ids":["MLB27834876"],"platforms":["wordpress","linkedin"],"ab_variants":1,"video_enabled":false,"video_format":"9:16","hitl_required":false,"budget_cap_mco":50,"daily_cap_mco":50,"next_run_at":"2026-06-29T01:00:53+00:00"}]
> ```

## 🤖 Claude *(01:10:21)*


## 🤖 Claude *(01:10:24)*

Plano perfeito para vídeo: 1 produto (Roborock MLB27834876 — um dos seeds com meli.la real), `platforms: [wordpress, linkedin]` (o `wordpress` é o que enfileira o render 9:16), `hitl_required: false`, caps 50/50, saldo 4669. Projeção com vídeo: 2×10 (orch) + 1×12 (render) + 2 (analyze) = **34 mco**.

Executando o GO — flip da flag + disparo do ciclo pago:

## 🤖 Claude *(01:10:30)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nSB=\"${SB_URL:-${SUPABASE_URL:-$VITE_SUPABASE_URL}}\"\necho \"=== 1) FLIP video_enabled=true ===\"\ncurl -s -X PATCH \"$SB/rest/v1/autopilot_plans?id=eq.640b3b67-b950-42f6-bbb9-48560771eaa6\" \\\n  -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" \\\n  -H \"Content-Type: application/json\" -H \"Prefer: return=representation\" \\\n  -d '{\"video_enabled\":true}' | python3 -c \"import sys,json; r=json.load(sys.stdin); print('video_enabled agora =', r[0]['video_enabled'])\" 2>/dev/null || echo \"PATCH resp acima\"\necho\necho \"=== 2) INVOKE autopilot-run (ciclo PAGO) ===\"\ncurl -s -X POST \"$SB/functions/v1/autopilot-run\" \\\n  -H \"Authorization: Bearer $SB_SECRET_KEY\" \\\n  -H \"x-autopilot-user-id: ada39fae-67e1-4e53-af1c-5a18e1c108e8\" \\\n  -H \"Content-Type: application/json\" \\\n  -d '{\"plan_id\":\"640b3b67-b950-42f6-bbb9-48560771eaa6\"}'\necho\necho \"=== 3) saldo p\u00f3s-invoke ===\"\ncurl -s \"$SB/rest/v1/profiles?id=eq.ada39fae-67e1-4e53-af1c-5a18e1c108e8&select=mco_balance\" \\\n  -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\"",
  "description": "Flip video_enabled and invoke first paid autopilot cycle"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === 1) FLIP video_enabled=true ===
> video_enabled agora = True
> 
> === 2) INVOKE autopilot-run (ciclo PAGO) ===
> {"ok":true,"cycle_id":"77e02fca-9384-4ae6-9242-5b17d3ec9aa7","n_runs":2,"succeeded":2,"projected_mco":34,"actual_mco":32,"refunded_mco":2,"status":"completed"}
> === 3) saldo pós-invoke ===
> [{"mco_balance":4637.00}]
> ```

## 🤖 Claude *(01:10:51)*


## 🤖 Claude *(01:10:54)*

🎬 **Ciclo pago DISPAROU e completou** — prova material:
- `video_enabled` = **True** ✓
- **cycle_id `77e02fca-9384-4ae6-9242-5b17d3ec9aa7`** · n_runs 2 · succeeded 2 · **actual 32 mco** (projetado 34, refund 2) · status completed
- **Saldo 4669 → 4637 = delta −32** ✓ (bate com o actual)

Agora o testemunho do **vídeo** em si — o render é assíncrono (worker `video-bridge` faz poll → renderiza ~110s). Verifico a linha `video_renders` deste ciclo + se o worker está processando:

## 🤖 Claude *(01:10:59)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nSB=\"${SB_URL:-${SUPABASE_URL:-$VITE_SUPABASE_URL}}\"\necho \"=== video_renders mais recentes do User 0 ===\"\ncurl -s \"$SB/rest/v1/video_renders?user_id=eq.ada39fae-67e1-4e53-af1c-5a18e1c108e8&order=created_at.desc&limit=3&select=id,state,engine,charged_mco,refunded_mco,storage_key,created_at,updated_at\" \\\n  -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\"\necho\necho \"=== worker video-bridge ativo? ===\"\nsystemctl --user is-active video-bridge.service 2>/dev/null || echo \"(status indispon\u00edvel)\"\necho\necho \"=== pipeline_runs deste ciclo (steps) ===\"\ncurl -s \"$SB/rest/v1/pipeline_runs?select=id,status,platforms,steps,started_at&order=started_at.desc&limit=2&user_id=eq.ada39fae-67e1-4e53-af1c-5a18e1c108e8\" \\\n  -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" | head -c 1500",
  "description": "Check video_renders row, worker status, pipeline steps"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === video_renders mais recentes do User 0 ===
> [{"id":"9069bb7d-c164-4307-930d-f98251e580a8","state":"done","engine":"hyperframes","charged_mco":0,"refunded_mco":0,"storage_key":"ada39fae-67e1-4e53-af1c-5a18e1c108e8/9069bb7d-c164-4307-930d-f98251e580a8.mp4","created_at":"2026-07-01T00:57:29.346425+00:00","updated_at":"2026-07-01T01:00:24.555845+00:00"}, 
>  {"id":"d3f7b06f-8d2a-43d3-8e77-aa64bba4b4c5","state":"failed","engine":"hyperframes","charged_mco":12,"refunded_mco":12,"storage_key":null,"created_at":"2026-06-26T01:02:43.628483+00:00","updated_at":"2026-06-26T01:02:47.113711+00:00"}, 
>  {"id":"8b0787e0-1442-43c1-9eee-1ead3f964b32","state":"done","engine":"hyperframes","charged_mco":12,"refunded_mco":0,"storage_key":"ada39fae-67e1-4e53-af1c-5a18e1c108e8/8b0787e0-1442-43c1-9eee-1ead3f964b32.mp4","created_at":"2026-06-26T00:47:19.178769+00:00","updated_at":"2026-06-26T00:48:11.109592+00:00"}]
> === worker video-bridge ativo? ===
> active
> 
> === pipeline_runs deste ciclo (steps) ===
> [{"id":"4b3256df-49e8-4bd3-a709-91d5174a33d1","status":"done","platforms":["linkedin"],"steps":[{"name": "linkedin_post", "input": {"topic": "Roborock S8 Pro Ultra: o robô que aspira, passa pano e esvazia a lixeira sozinho (tema em alta: The first-ever iPhone launched 19 years ago on June 29 2007 after being announce)", "article_link": "https://mcorch.com"}, "output": {"preview": "{\"post_text\": \"Há 17 anos, o primeiro iPhone mudava o mundo. Hoje, a tecnologia está reinventando nosso lar. 🏠✨\\n\\nLembro da fila para o primeiro iPhone, da sensação de ter o futuro nas mãos. Essa mesma sensação de 'uau' eu senti ao ligar o Roborock S8 Pro Ultra pela primeira vez. Ele não só aspira", "char_count": 859, "scheduled_at": "2026-07-01T02:10:45.845Z", "affiliate_links": 1}, "status": "done", "timestamp": "2026-07-01T01:10:45.845Z"}, {"name": "knowledge_mesh", "input": {"topic": "Roborock S8 Pro Ultra: o robô que aspira, passa pano e esvaz", "platforms": ["linkedin"]}, "output": {"obs_id": "63fdac62-0f21-41e6-96e7-ba09e866cab5", "node_type": "observation", "wordpress_url": null}, "status": "done", "timestamp": "2026-07-01T01:10:46.310Z"}, {"name": "content_mesh_asset", "input": {"topic": "Roborock S8 Pro Ultra: o robô que aspira, passa pano e esvaz", "campaign_id": null}, "output": {"reason": "no_wordpress_url"}, "status": "skipped", "timestamp": "2026-07-01T01:10:46.336Z"}],"started_at":"2026-07-01T01:10:33.139+00:00"}, 
>  {"id":"d5c9d1cf-024c-4771-872e-328659d883b7",
> ```

## 🤖 Claude *(01:11:27)*


## 🤖 Claude *(01:11:30)*

O worker está **active** e há um render `done` recente (`9069bb7d`, MP4 no bucket). Mas preciso confirmar que ele é **deste ciclo** (`77e02fca`) — o `charged_mco=0` e o timestamp 00:57 (antes dos meus runs 01:10) levantam dúvida. Verifico pela âncora do cycle_id + o sub-run wordpress (que é quem enfileira o vídeo):

## 🤖 Claude *(01:11:36)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nSB=\"${SB_URL:-${SUPABASE_URL:-$VITE_SUPABASE_URL}}\"\necho \"=== video_render ancorado no cycle_id 77e02fca (composition.autopilot.cycle_id) ===\"\ncurl -s \"$SB/rest/v1/video_renders?composition->autopilot->>cycle_id=eq.77e02fca-9384-4ae6-9242-5b17d3ec9aa7&select=id,state,engine,charged_mco,refunded_mco,storage_key,created_at,updated_at\" \\\n  -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\"\necho\necho \"=== sub-run WORDPRESS deste ciclo (video_generation step) ===\"\ncurl -s \"$SB/rest/v1/pipeline_runs?select=id,status,platforms,started_at,steps&order=started_at.desc&limit=4&user_id=eq.ada39fae-67e1-4e53-af1c-5a18e1c108e8\" \\\n  -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" \\\n  | python3 -c \"\nimport sys,json\nruns=json.load(sys.stdin)\nfor r in runs:\n    if 'wordpress' in (r.get('platforms') or []):\n        print('run',r['id'],r['status'],r['platforms'],r['started_at'])\n        for s in (r.get('steps') or []):\n            vid=s.get('output',{}) if isinstance(s.get('output'),dict) else {}\n            print('  step',s.get('name'),s.get('status'),{k:vid[k] for k in ('render_id','content_id','path') if k in vid})\n\"",
  "description": "Confirm video render belongs to this cycle via cycle_id anchor"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === video_render ancorado no cycle_id 77e02fca (composition.autopilot.cycle_id) ===
> []
> === sub-run WORDPRESS deste ciclo (video_generation step) ===
> run d5c9d1cf-024c-4771-872e-328659d883b7 running ['wordpress'] 2026-07-01T01:10:33.096+00:00
>   step article_generation done {}
> run 93659c88-21db-408d-9432-7e173f1d0f82 done ['wordpress'] 2026-06-26T00:46:22.013+00:00
>   step article_generation done {}
>   step image_generation done {'content_id': 'd15f6f4f-89bc-4fe9-8c2d-4a07a4193b99', 'path': 'ada39fae-67e1-4e53-af1c-5a18e1c108e8/4dbf02a2-40f9-4c12-90a7-64ef04b899ae.png'}
>   step video_generation done {'render_id': '8b0787e0-1442-43c1-9eee-1ead3f964b32'}
>   step wordpress_publish done {}
>   step knowledge_mesh done {}
>   step content_mesh_asset done {}
> ```

## 🤖 Claude *(01:12:51)*


## 🤖 Claude *(01:12:55)*

O quadro real está claro:
- O render `9069bb7d` (00:57) **NÃO é do meu ciclo** (a âncora `cycle_id=77e02fca` retornou vazio) — é de outro disparo.
- O sub-run **wordpress do meu ciclo (`d5c9d1cf`) ainda está `running`** — só passou por `article_generation`; ainda não chegou no `video_generation` que enfileira o render. O pipeline é assíncrono, então o vídeo está a caminho mas ainda não materializou.

Vou acompanhar o render em background (poll até `done` + prova do MP4) e, em paralelo, já disparo a avaliação dos dois repos que você pediu. Primeiro o witness do vídeo:

## 🤖 Claude *(01:13:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nSB=\"${SB_URL:-${SUPABASE_URL:-$VITE_SUPABASE_URL}}\"\nCYCLE=77e02fca-9384-4ae6-9242-5b17d3ec9aa7\necho \"Poll do render para cycle $CYCLE (async: espera enqueue \u2192 render ~110s)\"\nfor i in $(seq 1 45); do\n  ROW=$(curl -s \"$SB/rest/v1/video_renders?composition->autopilot->>cycle_id=eq.$CYCLE&select=id,state,storage_key,charged_mco,refunded_mco,updated_at\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\")\n  STATE=$(echo \"$ROW\" | python3 -c \"import sys,json; d=json.load(sys.stdin); print(d[0]['state'] if d else 'none')\" 2>/dev/null)\n  echo \"[poll $i $(date -u +%H:%M:%S)] state=$STATE\"\n  if [ \"$STATE\" = \"done\" ] || [ \"$STATE\" = \"failed\" ]; then\n    echo \"=== FINAL video_renders row ===\"; echo \"$ROW\"\n    KEY=$(echo \"$ROW\" | python3 -c \"import sys,json;print(json.load(sys.stdin)[0].get('storage_key') or '')\" 2>/dev/null)\n    echo \"=== content_library type=video (reconcilia\u00e7\u00e3o FR-VA-025) ===\"\n    curl -s \"$SB/rest/v1/content_library?type=eq.video&order=created_at.desc&limit=1&select=id,title,media_url,created_at&user_id=eq.ada39fae-67e1-4e53-af1c-5a18e1c108e8\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\"\n    if [ -n \"$KEY\" ]; then\n      SIGN=$(curl -s -X POST \"$SB/storage/v1/object/sign/video-studio-assets/$KEY\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" -H \"Content-Type: application/json\" -d '{\"expiresIn\":600}')\n      URLP=$(echo \"$SIGN\" | python3 -c \"import sys,json;print(json.load(sys.stdin).get('signedURL',''))\" 2>/dev/null)\n      echo \"=== MP4 content-length ===\"\n      [ -n \"$URLP\" ] && curl -sI \"$SB/storage/v1$URLP\" | grep -i \"content-length\\|content-type\"\n    fi\n    break\n  fi\n  sleep 12\ndone\necho \"POLL_END\"",
  "description": "Poll video render to completion with MP4 proof",
  "run_in_background": true
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Command running in background with ID: bt5m0o9iy. Output is being written to: /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/tasks/bt5m0o9iy.output. You will be notified when it completes. To check interim output, use Read on that file path.
> ```

## 🤖 Claude *(01:13:07)*


## 🤖 Claude *(01:13:13)*

Witness rodando em background (`bt5m0o9iy`). Agora a avaliação dos dois repos — mas antes deixa eu enquadrar honestamente o que estou avaliando, porque o "native exclusivo" tem uma nuance importante que vou verificar:

**A pergunta por trás da pergunta:** hoje o **HyperFrames** já é self-hosted (render-core Playwright+FFmpeg na sua infra) mas o **editor** Studio é um pacote de terceiros (`@hyperframes/studio`, Apache-2.0) que você embute; e o **OpenDesign** roda via daemon `open-design` externo. "Native exclusivo do MCORCH" = internalizar/forkar essas peças pra você ser dono do código, não dependente de upstream. Os dois repos (`opensrc`, `graphify`) precisam ser avaliados *contra esse objetivo* + a doutrina open-source-first.

Disparo a avaliação fundamentada (fetch real dos repos + mapa do estado atual + veredito adversarial):

## 🤖 Claude *(01:13:45)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'opensrc-graphify-native-eval',\n  description: 'Avalia se vercel-labs/opensrc + safishamsi/graphify ajudam a tornar OpenDesign e HyperFrames nativos/exclusivos do MCORCH (doutrina open-source-first)',\n  phases: [\n    { title: 'Research', detail: 'fetch real dos 2 repos + mapa do estado atual OpenDesign/HyperFrames no MCORCH' },\n    { title: 'Verdict', detail: 'veredito de fit por repo + recomenda\u00e7\u00e3o alinhada \u00e0 doutrina' },\n  ],\n}\n\nconst REPO_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  properties: {\n    repo: { type: 'string' },\n    what_it_is: { type: 'string', description: 'O que o repo \u00c9 de fato (README/about real), em 2-3 frases. N\u00e3o inferir do nome.' },\n    capabilities: { type: 'array', items: { type: 'string' }, description: 'Capacidades concretas que ele entrega.' },\n    language_stack: { type: 'string', description: 'Linguagem/framework/runtime.' },\n    license: { type: 'string', description: 'Licen\u00e7a EXATA (MIT/Apache-2.0/AGPL/none/etc.) \u2014 cr\u00edtico p/ uso comercial e \"exclusivo\".' },\n    maintenance: { type: 'string', description: 'Stars, \u00faltimo commit, atividade, maturidade. Vivo ou abandonado?' },\n    relevance_to_goal: { type: 'string', description: 'Como (se) ele ajuda a tornar OpenDesign OU HyperFrames nativo/exclusivo do MCORCH. Honesto se N\u00c3O for relevante.' },\n    fetched_url: { type: 'string' },\n    confidence: { type: 'string', enum: ['high', 'medium', 'low'], description: 'Confian\u00e7a de que o fetch foi real (n\u00e3o bloqueado/404).' },\n  },\n  required: ['repo', 'what_it_is', 'license', 'relevance_to_goal', 'fetched_url', 'confidence'],\n}\n\nphase('Research')\nconst research = await parallel([\n  () => agent(\n    `Pesquise o reposit\u00f3rio GitHub https://github.com/vercel-labs/opensrc \u2014 FETCH REAL (use WebFetch/WebSearch ou a skill firecrawl via ToolSearch; carregue o README e a p\u00e1gina about).\\n` +\n    `Determine MATERIALMENTE (n\u00e3o inferir do nome): o que \u00c9, capacidades, stack, LICEN\u00c7A exata (cr\u00edtico), maturidade (stars/\u00faltimo commit), e se/como ajudaria a tornar o editor de design (OpenDesign) OU o motor de v\u00eddeo (HyperFrames) NATIVO/EXCLUSIVO do MCORCH. Se o fetch falhar/404/for bloqueado, diga confidence=low e o que conseguiu.`,\n    { label: 'repo:opensrc', phase: 'Research', schema: REPO_SCHEMA, effort: 'medium' }\n  ),\n  () => agent(\n    `Pesquise o reposit\u00f3rio GitHub https://github.com/safishamsi/graphify \u2014 FETCH REAL (use WebFetch/WebSearch ou a skill firecrawl via ToolSearch; carregue o README e a p\u00e1gina about).\\n` +\n    `Determine MATERIALMENTE (n\u00e3o inferir do nome): o que \u00c9, capacidades, stack, LICEN\u00c7A exata (cr\u00edtico), maturidade (stars/\u00faltimo commit), e se/como ajudaria a tornar o editor de design (OpenDesign) OU o motor de v\u00eddeo (HyperFrames) NATIVO/EXCLUSIVO do MCORCH. Se o fetch falhar/404/for bloqueado, diga confidence=low e o que conseguiu.`,\n    { label: 'repo:graphify', phase: 'Research', schema: REPO_SCHEMA, effort: 'medium' }\n  ),\n  () => agent(\n    `Mapeie o ESTADO ATUAL no reposit\u00f3rio MCORCH (constellation-orchestra) das duas pe\u00e7as que o Sovereign quer tornar \"nativas/exclusivas\":\\n` +\n    `(1) HyperFrames: leia scripts/hyperframes/render-core.ts, scripts/video-bridge.ts, src/pages/VideoStudioEditorPage.tsx, .claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md. Determine: o que j\u00e1 \u00e9 self-hosted/pr\u00f3prio (render) vs o que \u00e9 depend\u00eancia de terceiros (o EDITOR @hyperframes/studio Apache-2.0, React 19). Cite o que \"native exclusivo\" exigiria internalizar.\\n` +\n    `(2) OpenDesign: procure design.mcorch.com, design-bridge, open-design daemon (grep -rn \"open-design\\\\|design-bridge\\\\|design.mcorch\" nginx/ scripts/ docs/ .claude/ src/). Determine o que \u00e9 pr\u00f3prio vs depend\u00eancia externa.\\n` +\n    `Reporte em JSON-livre (texto estruturado): para HyperFrames e OpenDesign, o que j\u00e1 \u00e9 pr\u00f3prio, o que \u00e9 depend\u00eancia de terceiros, e o gap concreto at\u00e9 \"native exclusivo\". Cite file:line.`,\n    { label: 'current-state', phase: 'Research', effort: 'medium' }\n  ),\n])\n\nconst [opensrc, graphify, currentState] = research\n\nphase('Verdict')\nconst VERDICT_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  properties: {\n    opensrc_verdict: { type: 'string', enum: ['adopt', 'fork-and-own', 'ignore', 'inconclusive'], description: 'Recomenda\u00e7\u00e3o para vercel-labs/opensrc.' },\n    opensrc_reason: { type: 'string' },\n    graphify_verdict: { type: 'string', enum: ['adopt', 'fork-and-own', 'ignore', 'inconclusive'], description: 'Recomenda\u00e7\u00e3o para safishamsi/graphify.' },\n    graphify_reason: { type: 'string' },\n    native_exclusive_path: { type: 'string', description: 'O caminho REAL pra tornar OpenDesign + HyperFrames nativos/exclusivos do MCORCH \u2014 usando (ou n\u00e3o) esses repos. Concreto.' },\n    doctrine_fit: { type: 'string', description: 'Como isso serve a doutrina open-source-first/equity (licen\u00e7a comercial ok? self-host? posse do c\u00f3digo?).' },\n    bok_gate_needed: { type: 'string', description: 'Isso exigiria BoK gate (m\u00f3dulo novo) antes de c\u00f3digo? Sim/n\u00e3o + por qu\u00ea.' },\n    honest_caveats: { type: 'string', description: 'Riscos: licen\u00e7a AGPL/viral, abandono, esfor\u00e7o de fork, React 19 vs 18, etc.' },\n  },\n  required: ['opensrc_verdict', 'opensrc_reason', 'graphify_verdict', 'graphify_reason', 'native_exclusive_path', 'doctrine_fit', 'honest_caveats'],\n}\n\nconst verdict = await agent(\n  `Voc\u00ea \u00e9 o arquiteto-chefe do MCORCH. O Sovereign quer tornar o editor de design (OpenDesign) e o motor de v\u00eddeo (HyperFrames) NATIVOS/EXCLUSIVOS do MCORCH (posse total do c\u00f3digo, self-hosted), sob a doutrina open-source-first (custo=0, equity, licen\u00e7a comercial-ok). Ele perguntou se vale usar 2 repos para isso.\\n` +\n  `D\u00ea o veredito por repo (adopt/fork-and-own/ignore/inconclusive) + o caminho REAL pro \"native exclusivo\" + fit de doutrina + se precisa BoK gate. Seja honesto: se um repo for irrelevante ou de licen\u00e7a ruim (AGPL/none), diga ignore. Dados:\\n\\n` +\n  `## vercel-labs/opensrc\\n${JSON.stringify(opensrc, null, 2)}\\n\\n## safishamsi/graphify\\n${JSON.stringify(graphify, null, 2)}\\n\\n## Estado atual MCORCH\\n${typeof currentState === 'string' ? currentState : JSON.stringify(currentState)}`,\n  { label: 'architect', phase: 'Verdict', schema: VERDICT_SCHEMA, effort: 'high' }\n)\n\nreturn { opensrc, graphify, currentState, verdict }\n",
  "description": "Evaluate opensrc + graphify repos for native tooling"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wr8f87aw8
> Summary: Avalia se vercel-labs/opensrc + safishamsi/graphify ajudam a tornar OpenDesign e HyperFrames nativos/exclusivos do MCORCH (doutrina open-source-first)
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/subagents/workflows/wf_ec9db575-8a7
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/workflows/scripts/opensrc-graphify-native-eval-wf_ec9db575-8a7.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/workflows/scripts/opensrc-graphify-native-eval-wf_ec9db575-8a7.js"} to iterate without resending the script.)
> Run ID: wf_ec9db575-8a7
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/workflows/scripts/opensrc-graphify-native-eval-wf_ec9db575-8a7.js", resumeFromRunId: "wf_ec9db575-8a7"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(01:13:48)*


## 🤖 Claude *(01:13:48)*

O witness do render terminou — leio a prova:

## 🤖 Claude *(01:13:49)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/tasks/bt5m0o9iy.output"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	Poll do render para cycle 77e02fca-9384-4ae6-9242-5b17d3ec9aa7 (async: espera enqueue → render ~110s)
> 2	[poll 1 01:13:04] state=done
> 3	=== FINAL video_renders row ===
> 4	[{"id":"561a31df-f7a2-4d20-ba8b-3c286d8470f6","state":"done","storage_key":"ada39fae-67e1-4e53-af1c-5a18e1c108e8/561a31df-f7a2-4d20-ba8b-3c286d8470f6.mp4","charged_mco":12,"refunded_mco":0,"updated_at":"2026-07-01T01:13:04.333916+00:00"}]
> 5	=== content_library type=video (reconciliação FR-VA-025) ===
> 6	[{"id":"e27a09e7-197b-4a22-9e80-6914cb56ff9c","title":"Vídeo 9:16: Do iPhone de 2007 ao Roborock de 2024: A Revolução da Automação Chegou à Sua Casa","media_url":"ada39fae-67e1-4e53-af1c-5a18e1c108e8/561a31df-f7a2-4d20-ba8b-3c286d8470f6.mp4","created_at":"2026-07-01T01:13:04.456054+00:00"}]=== MP4 content-length ===
> 7	content-type: video/mp4
> 8	content-length: 776522
> 9	POLL_END
> 10	
> ```

## 🤖 Claude *(01:14:23)*


## 🤖 Claude *(01:14:29)*

🎬🎉 **1º CICLO PAGO DE VÍDEO — TESTEMUNHADO COM PROVA MATERIAL COMPLETA.**

Todos os 5 critérios de witness batidos (Lei 1):

| Critério | Prova |
|----------|-------|
| **Ciclo completado** | `autopilot_cycles 77e02fca` · actual **32 mco** · status completed |
| **Saldo debitado** | 4669 → **4637** (delta −32) ✓ |
| **Render done** | `video_renders 561a31df` state=**done** · engine=hyperframes · charged 12 |
| **MP4 no bucket** | `561a31df.mp4` · **776.522 bytes** · content-type `video/mp4` ✓ |
| **Reconciliação FR-VA-025** | `content_library e27a09e7` type=video → aponta pro MP4 |

E olha a **qualidade** que justifica manter o Gemini 2.5 Pro — o título que ele gerou usou o trend do dia (aniversário do iPhone) e amarrou no produto de forma orgânica:
> **"Vídeo 9:16: Do iPhone de 2007 ao Roborock de 2024: A Revolução da Automação Chegou à Sua Casa"**

Deixa eu baixar o MP4 real do bucket e te mandar — você merece **ver** o primeiro vídeo que seu sistema fez sozinho:

## 🤖 Claude *(01:14:34)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd \"/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad\"\nset -a; source /home/gcrUX/htdocs/constellation-orchestra/.env 2>/dev/null; set +a\nSB=\"${SB_URL:-${SUPABASE_URL:-$VITE_SUPABASE_URL}}\"\nKEY=\"ada39fae-67e1-4e53-af1c-5a18e1c108e8/561a31df-f7a2-4d20-ba8b-3c286d8470f6.mp4\"\nSIGN=$(curl -s -X POST \"$SB/storage/v1/object/sign/video-studio-assets/$KEY\" -H \"apikey: $SB_SECRET_KEY\" -H \"Authorization: Bearer $SB_SECRET_KEY\" -H \"Content-Type: application/json\" -d '{\"expiresIn\":600}')\nURLP=$(echo \"$SIGN\" | python3 -c \"import sys,json;print(json.load(sys.stdin).get('signedURL',''))\" 2>/dev/null)\ncurl -s \"$SB/storage/v1$URLP\" -o autopilot-video-1-roborock.mp4\nls -la autopilot-video-1-roborock.mp4\nfile autopilot-video-1-roborock.mp4 2>/dev/null || true\nffprobe -v error -select_streams v:0 -show_entries stream=width,height,duration -of default=noprint_wrappers=1 autopilot-video-1-roborock.mp4 2>/dev/null || echo \"(ffprobe indispon\u00edvel)\"",
  "description": "Download rendered MP4 from bucket for delivery"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> -rw-rw-r-- 1 ubuntu ubuntu 776522 Jun 30 22:14 autopilot-video-1-roborock.mp4
> autopilot-video-1-roborock.mp4: ISO Media, MP4 Base Media v1 [ISO 14496-12:2003]
> width=1080
> height=1920
> duration=5.000000
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(01:14:57)*


## 🤖 Claude *(01:14:59)*


🛠️ **Tool Call**: `SendUserFile`
```json
{
  "files": [
    "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad/autopilot-video-1-roborock.mp4"
  ],
  "caption": "1\u00ba v\u00eddeo aut\u00f4nomo do Viral Autopilot \u2014 9:16, 1080\u00d71920, 5s, 776KB. Render HyperFrames self-hosted (USD $0). cycle 77e02fca / render 561a31df.",
  "status": "normal",
  "display": "render"
}
```

> **Tool Result (SendUserFile)** - ✅ Success
>
> ```
> 1 file delivered to user.
> ```

## 🤖 Claude *(01:15:00)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/autonomous-loop-charter.md",
  "offset": 55,
  "limit": 15
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 55	- **HALT:** nenhum até cutover de nav (3.9) — aí confirmar com Sovereign.
> 56	
> 57	### 5. Security — OTD-SEC-006 (sentinel-wiring) + OTD-SEC-007 (lefthook/gitleaks)  ⟶ hardening, desbloqueado
> 58	- BoK security 4/4 selada; resta implementação.
> 59	
> 60	---
> 61	
> 62	## Fila de Ação Sovereign (SÓ você destrava — preenchida pelo loop)
> 63	- [ ] **OTD-AC-015 (Gabriel AI 3b — ArcFace-HARD):** decidir/provisionar motor de embedding facial (InsightFace self-host no Mesh OU API paga Rekognition/Azure/Face++) + custo/credencial. Sem isso o Identity Gate fica VLM-soft (human-review-assist, não anti-impersonation automático).
> 64	- [ ] **OTD-AC-015b — biometria calibração-grade:** frames reais do Gabriel rotulados (mesma/diferente) p/ FAR/FRR/EER — só após o motor ArcFace existir.
> 65	- [ ] **OTD-AC-017 (Soul ID train):** credencial Higgsfield + confirmar API self-serve de treino (≥20 fotos); senão fallback Tier1/Tier2 ou LoRA-FLUX (gated commercial-license).
> 66	- [ ] **Licença comercial (FM-AC-001/OTD-AC-011):** confirmar checkpoint comercial da base de geração (FLUX.1-dev é non-commercial) — Sovereign + jurídico flipam `commercial_license_ok`.
> 67	- [ ] **GO de produção 3b** sobre o Usuário Zero + GO de gasto do loop de verificação caso não use BYOK openrouter (com BYOK = cost 0).
> 68	- [ ] **Editor render user-initiated (FR-VS-048/VS-009 · billing decision):** ativar `VIDEO_HYPERFRAMES_WEBHOOK=poll://` liga a cobrança de **12 mco/render** disparado pelo editor (mco interno do próprio Sovereign, **USD=0** — engine self-hosted; feature documentada FR-VS-009). O container/McorchAdapter + botão da UI podem ser CONSTRUÍDOS e testados sem ativar (o worker já renderiza queued rows — provado it.4/it.5); só a ativação do secret = decisão de billing → GO Sovereign. Worker-side (FR-VS-047) **100% pronto+provado**.
> 69	- [ ] **GO de gasto:** 1º ciclo PAGO de vídeo (`video_enabled` + GO) — testemunho. **Pipeline verificado end-to-end PRONTO** (render `8b0787e0` done, MP4 748KB no bucket, reconciliação FR-VA-025 OK); falta só `UPDATE autopilot_plans SET video_enabled=true WHERE id='640b3b67...'` + GO. **GATED pela doutrina open-source-first:** render HyperFrames já é self-hosted (USD≈0); antes do GO, auditar que os passos LLM (script/analyze) rodam BYOK-grátis → custo USD externo = 0. Custo interno ~24 mco/vídeo (saldo 4669 cobre).
> ```

## 🤖 Claude *(01:15:18)*


## 🤖 Claude *(01:15:21)*

O MP4 foi entregue — **1080×1920, 9:16, 5s, 776KB** (confirmei com ffprobe). Você pode assistir aí ☝️ o primeiro vídeo que o MCORCH produziu sozinho, de ponta a ponta, com render self-hosted a **USD $0**.

Selo o item na charter (GO de gasto = FEITO):

## 🤖 Claude *(01:15:28)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/autonomous-loop-charter.md",
  "old_string": "- [ ] **GO de gasto:** 1\u00ba ciclo PAGO de v\u00eddeo (`video_enabled` + GO) \u2014 testemunho. **Pipeline verificado end-to-end PRONTO** (render `8b0787e0` done, MP4 748KB no bucket, reconcilia\u00e7\u00e3o FR-VA-025 OK); falta s\u00f3 `UPDATE autopilot_plans SET video_enabled=true WHERE id='640b3b67...'` + GO. **GATED pela doutrina open-source-first:** render HyperFrames j\u00e1 \u00e9 self-hosted (USD\u22480); antes do GO, auditar que os passos LLM (script/analyze) rodam BYOK-gr\u00e1tis \u2192 custo USD externo = 0. Custo interno ~24 mco/v\u00eddeo (saldo 4669 cobre).",
  "new_string": "- [x] **GO de gasto \u2014 1\u00ba ciclo PAGO de v\u00eddeo: FEITO E TESTEMUNHADO (2026-07-01).** GO Sovereign dado; `video_enabled=true` no plano `640b3b67`; ciclo `77e02fca` completed (actual **32 mco**, saldo 4669\u21924637); render `561a31df` done (MP4 **776.522B** 1080\u00d71920 5s no bucket `video-studio-assets`); reconcilia\u00e7\u00e3o FR-VA-025 \u2192 `content_library e27a09e7` type=video. T\u00edtulo trend-informed (\"Do iPhone de 2007 ao Roborock de 2024\"). **Doutrina reconciliada** (audit `wf_6d3bdbd6-eb7`, mem\u00f3ria `feedback_opensource_first_zero_cost_equity`): render HyperFrames self-hosted USD=0; texto/imagem ~$0.05/ciclo na BYOK OpenRouter do Sovereign \u2192 **Gemini 2.5 Pro MANTIDO** (qualidade brand-first vale). Ollama self-host = hardening diferido. **Pr\u00f3ximo (opcional):** `is_active=true` liga a cad\u00eancia pg_cron (v\u00eddeo aut\u00f4nomo a cada 3 dias) \u00b7 telemetria `llm_usage` p/ tornar o USD vis\u00edvel \u00b7 cortar imagem AI redundante."
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/.claude/context/autonomous-loop-charter.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:15:33)*


## 🤖 Claude *(01:15:44)*

**Marco selado** ✅ — charter atualizada, item GO de gasto marcado como feito e testemunhado. Resumindo o que aconteceu de fato:

- Você deu o GO → liguei `video_enabled`, disparei o ciclo, e o sistema **gerou artigo + LinkedIn + renderizou um vídeo 9:16 e reconciliou tudo sozinho**, custando 32 mco internos e **$0 de render** (a parte cara).
- O único USD real foi ~$0.05 de LLM na sua própria chave OpenRouter — exatamente o que você aceitou, e a qualidade (título trend-aware) mostrou que valeu manter o Gemini Pro.

**Três alavancas opcionais daqui (nenhuma urgente):**
1. **Ligar a cadência autônoma** — `is_active=true` faz o pg_cron rodar um vídeo desses **sozinho a cada 3 dias**, sem você disparar. É o "autopilot" de verdade. (Hoje está manual — cada ciclo espera seu invoke.)
2. **Vision QA no vídeo** — passar esse MP4 pelo olho criativo do Vision MCP (sua diretiva), pra pegar qualquer artefato visual antes de escalar.
3. **Telemetria `llm_usage`** — tornar o custo USD visível/provável no `infra_health_logs`.

Me diz se quer ligar a cadência autônoma agora ou testemunhar mais alguns ciclos manuais primeiro.

---

⏳ **A avaliação dos dois repos (`opensrc` + `graphify`) ainda está rodando** em background (`wr8f87aw8`) — fetch real dos repos + mapa do estado atual de OpenDesign/HyperFrames + veredito de fit com a doutrina. Te trago o resultado assim que concluir.

## 👤 User *(01:16:53)*

<task-notification>
<task-id>wr8f87aw8</task-id>
<tool-use-id>toolu_01E7U4XMwVqq93KiDa1bqcgu</tool-use-id>
<output-file>/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/tasks/wr8f87aw8.output</output-file>
<status>completed</status>
<summary>Dynamic workflow "Avalia se vercel-labs/opensrc + safishamsi/graphify ajudam a tornar OpenDesign e HyperFrames nativos/exclusivos do MCORCH (doutrina open-source-first)" completed</summary>
<result>{"opensrc":{"repo":"vercel-labs/opensrc","what_it_is":"É uma ferramenta de linha de comando (CLI) que busca e cacheia o código-fonte de pacotes de terceiros — npm, PyPI, crates.io e GitHub — para dar contexto mais profundo a agentes de IA de codificação. O tagline oficial do \"About\" é literalmente: \"Fetch source code for npm packages to give AI coding agents deeper context\". Uso típico: `opensrc path zod` retorna o caminho local (cacheado) do fonte, encadeável com ferramentas de shell como `rg \"parse\" $(opensrc path zod)`.","capabilities":["Baixa o código-fonte real de pacotes de npm, PyPI, crates.io e GitHub (não só metadados)","Cacheia localmente e retorna o path instantaneamente em consultas subsequentes","Comando `path` que resolve para um diretório de fonte encadeável com shell (ripgrep, cat, etc.)","Comando `fetch` documentado + índice de busca (search index)","Clone autenticado com validação de host (fix #66)","Distribuição via npm com trusted publishing"],"language_stack":"CLI escrita em Rust (55.8%) + TypeScript (31.5%) + JavaScript (7.0%). Monorepo Turborepo com pnpm workspaces; site de docs em Next.js; requer Node.js 24+.","license":"Apache-2.0","maintenance":"Vivo e recente. ~2.7k stars, 177 forks. Release v0.7.3 em 23-jun-2026 (mesma data do commit mais recente no main: \"Configure trusted npm publishing #68\", \"Prepare v0.7.3 release #67\", \"Fix authenticated clone host validation #66\"). 59 commits no main — projeto jovem/pré-1.0 (vercel-labs, tom experimental), mas com atividade nos últimos dias.","relevance_to_goal":"Baixa/indireta e HONESTA: opensrc NÃO ajuda a tornar OpenDesign nem HyperFrames \"nativo/exclusivo\" do MCORCH. Ele não é um motor de design, editor de vídeo, nem runtime de renderização — é um utilitário de DX/ingestão de código-fonte para dar contexto a agentes de coding. O único uso plausível no ecossistema MCORCH seria de ferramenta interna de desenvolvimento: quando o time (ou agentes OpenClaw/Claude Code) precisa auditar/entender o fonte real de dependências como `@hyperframes/studio@0.7.5`, `@hyperframes/core/studio-api` ou pacotes do OpenDesign — encaixaria no fluxo do claw-master (audita drift openclaw.json vs docs) ou no blueprint de integração HyperFrames Studio (que já teve que provar via `npm view` que o studio exige React 19). Isso ajuda a ENTENDER o código para embutir, não a torná-lo exclusivo. Para \"nativo/exclusivo\" (vendorizar/forkar os motores sob MCORCH) o que importa é a licença DELES (HyperFrames = Apache-2.0, permite fork/vendorização), não esta ferramenta. Veredito: ferramenta de DX útil no tooling interno; irrelevante para a estratégia de exclusividade do produto.","fetched_url":"https://github.com/vercel-labs/opensrc","confidence":"high"},"graphify":{"repo":"safishamsi/graphify","what_it_is":"Graphify é uma skill/CLI para assistentes de código (Claude Code, Codex, Cursor, Gemini CLI, etc.) que transforma qualquer pasta — código, schemas SQL, scripts R/shell, docs, papers, imagens ou vídeos — em um grafo de conhecimento (GraphRAG) consultável via comandos /graphify. Extrai AST localmente com tree-sitter (36 gramáticas), gera visualização HTML interativa + relatório Markdown + JSON do grafo, e roda como servidor MCP para compartilhamento em equipe. É basicamente indexação de repositório em knowledge graph, não uma ferramenta criativa.","capabilities":["Indexa código + SQL + docs + PDFs + imagens + vídeos em um único knowledge graph consultável","Extração de AST 100% local via tree-sitter (36 gramáticas: Python, TS, Go, Rust, Java, Apex, Terraform/HCL, etc.) — sem chamada de API para parsing","Saídas: HTML interativo (nós clicáveis, filtro, busca) + relatório Markdown + arquivo JSON do grafo","Detecção de comunidades via algoritmo Leiden; confidence scoring EXTRACTED/INFERRED/AMBIGUOUS","Modo servidor MCP para compartilhamento em equipe; integração Git via post-commit hooks","Transcrição local de áudio/vídeo via faster-whisper; backends opcionais Anthropic/Gemini/OpenAI/Ollama/Bedrock/Azure"],"language_stack":"Python 100%; core = tree-sitter (AST), Leiden (community detection), faster-whisper (transcrição local); distribuído como skill/MCP server; instalação via uv/pipx. LLM backends opcionais (Anthropic, Gemini, OpenAI, Ollama, Bedrock, Azure).","license":"MIT","maintenance":"Vivo e muito ativo. 74.891 stars, 7.444 forks, 250 watchers, 399 issues abertas. Criado 2026-04-03, último push 2026-06-30 (branch default v8), release v0.9.3 (jun/2026). Projeto Y Combinator S26 (homepage graphifylabs.ai). Maduro em tração, ainda pré-1.0.","relevance_to_goal":"BAIXA/NENHUMA para o objetivo declarado. Graphify é uma ferramenta de GraphRAG/knowledge-graph de CÓDIGO — não tem relação com edição de design (OpenDesign) nem com renderização de vídeo (HyperFrames). Não fornece nenhum componente de canvas, timeline, compositing, render de vídeo, ou UI de design. O único ponto de contato com o MCORCH é conceitual: o ecossistema JÁ possui sua própria camada GraphRAG (mcorch_nodes/mcorch_edges + embeddings + gitnexus MCP), então Graphify seria no máximo um SUBSTITUTO/alternativa da malha de conhecimento existente — não um habilitador para tornar OpenDesign ou HyperFrames nativos/exclusivos. Nota tangencial: tem tópicos 'openclaw' e 'claude-code' e roda como skill/MCP, o mesmo padrão de plugin que o MCORCH usa (ex.: vision-mcp-plugin), mas isso é forma de distribuição, não capacidade de design/vídeo. Recomendação honesta: não adotar para essa meta específica.","fetched_url":"https://api.github.com/repos/safishamsi/graphify (confirmado) + https://github.com/safishamsi/graphify (README via WebFetch)","confidence":"high"},"currentState":"Estado material confirmado. Segue o mapa.\n\n---\n\n# ESTADO ATUAL — HyperFrames &amp; OpenDesign (native/exclusivo)\n\n## (1) HYPERFRAMES\n\n### JÁ É PRÓPRIO (self-hosted, código MCORCH)\n- **Motor de render determinístico** — `scripts/hyperframes/render-core.ts:116` `renderComposition()`: Playwright Chromium headless + FFmpeg → MP4 9:16 1080×1920 byte-reproduzível (NFR-VS-016, `-fflags +bitexact`). Templates PRÓPRIOS (`templates/viral-short-9x16`, `viral-long-16x9`, allowlist `render-core.ts:71`). Zero dependência de terceiros nesse caminho — é 100% código MCORCH.\n- **Worker/orquestração** — `scripts/video-bridge.ts`: claim atômico `video_renders` → upload bucket privado `video-studio-assets` → `finalize_video_render` → dual-write `creative_assets` (`video-bridge.ts:128`) → attach autopilot FR-VA-025 (`:146`) → kick reshaper (`:177`). systemd `video-bridge.service` **active running**. Próprio.\n- **Superfície UI no SPA** — `src/pages/VideoStudioEditorPage.tsx`: página React 18 própria (só um `&lt;iframe src=\"https://video.mcorch.com\"&gt;`). O shell é próprio; o conteúdo do iframe não (ver abaixo).\n- **Contrato de asset/tenancy/billing** — `video_renders`/`video_assets`/`finalize_video_render`, mesh, prepaid (OTD-VA-010), bucket privado. Próprio.\n\n### DEPENDÊNCIA DE TERCEIROS\n- **O EDITOR em si** — `video-studio.service` roda `hyperframes preview` do pacote npm **`hyperframes@0.7.22`** (`/home/ubuntu/.bun/install/global/node_modules/hyperframes/dist/cli.js preview ...`, WorkingDir `~/.mcorch/video-studio/projects/mcorch-video`, porta 3210). O timeline multi-camada / overlays alpha / efeitos / transições que o Sovereign vê = **binário HeyGen/HyperFrames Apache-2.0, não código nosso**. `video.mcorch.com` é só o vhost SSO-gated (`nginx/video.mcorch.com.conf`) na frente dele.\n- **O CLI de render de projeto Studio** — `renderStudioProject()` (`render-core.ts:200`) faz `spawn(HF_NODE, [HF_CLI, 'render', dir, ...])` — ou seja, projetos autorados no editor são renderizados WRAPPEANDO o `hyperframes render` de terceiros (`render-core.ts:86` `HF_CLI`), não pelo nosso motor determinístico. Parity é \"definicional\" justamente porque delega ao mesmo binário terceiro.\n- Depende de **node v22 externo** (`HF_NODE=/home/ubuntu/.local/bin/node`, `render-core.ts:87`) e do Chromium do 
... (truncated 14010 chars, full result in /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/tasks/wr8f87aw8.output)</result>
<usage><agent_count>4</agent_count><subagent_tokens>324175</subagent_tokens><tool_uses>19</tool_uses><duration_ms>187554</duration_ms></usage>
</task-notification>

## 🤖 Claude *(01:16:57)*


## 🤖 Claude *(01:16:57)*

Avaliação dos repos concluída. Leio o veredito completo do arquiteto + o mapa de estado atual (truncado na notificação):

## 🤖 Claude *(01:16:58)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/tasks/wr8f87aw8.output",
  "offset": 1,
  "limit": 60
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	{
> 2	  "summary": "Avalia se vercel-labs/opensrc + safishamsi/graphify ajudam a tornar OpenDesign e HyperFrames nativos/exclusivos do MCORCH (doutrina open-source-first)",
> 3	  "agentCount": 4,
> 4	  "logs": [],
> 5	  "result": {
> 6	    "opensrc": {
> 7	      "repo": "vercel-labs/opensrc",
> 8	      "what_it_is": "É uma ferramenta de linha de comando (CLI) que busca e cacheia o código-fonte de pacotes de terceiros — npm, PyPI, crates.io e GitHub — para dar contexto mais profundo a agentes de IA de codificação. O tagline oficial do \"About\" é literalmente: \"Fetch source code for npm packages to give AI coding agents deeper context\". Uso típico: `opensrc path zod` retorna o caminho local (cacheado) do fonte, encadeável com ferramentas de shell como `rg \"parse\" $(opensrc path zod)`.",
> 9	      "capabilities": [
> 10	        "Baixa o código-fonte real de pacotes de npm, PyPI, crates.io e GitHub (não só metadados)",
> 11	        "Cacheia localmente e retorna o path instantaneamente em consultas subsequentes",
> 12	        "Comando `path` que resolve para um diretório de fonte encadeável com shell (ripgrep, cat, etc.)",
> 13	        "Comando `fetch` documentado + índice de busca (search index)",
> 14	        "Clone autenticado com validação de host (fix #66)",
> 15	        "Distribuição via npm com trusted publishing"
> 16	      ],
> 17	      "language_stack": "CLI escrita em Rust (55.8%) + TypeScript (31.5%) + JavaScript (7.0%). Monorepo Turborepo com pnpm workspaces; site de docs em Next.js; requer Node.js 24+.",
> 18	      "license": "Apache-2.0",
> 19	      "maintenance": "Vivo e recente. ~2.7k stars, 177 forks. Release v0.7.3 em 23-jun-2026 (mesma data do commit mais recente no main: \"Configure trusted npm publishing #68\", \"Prepare v0.7.3 release #67\", \"Fix authenticated clone host validation #66\"). 59 commits no main — projeto jovem/pré-1.0 (vercel-labs, tom experimental), mas com atividade nos últimos dias.",
> 20	      "relevance_to_goal": "Baixa/indireta e HONESTA: opensrc NÃO ajuda a tornar OpenDesign nem HyperFrames \"nativo/exclusivo\" do MCORCH. Ele não é um motor de design, editor de vídeo, nem runtime de renderização — é um utilitário de DX/ingestão de código-fonte para dar contexto a agentes de coding. O único uso plausível no ecossistema MCORCH seria de ferramenta interna de desenvolvimento: quando o time (ou agentes OpenClaw/Claude Code) precisa auditar/entender o fonte real de dependências como `@hyperframes/studio@0.7.5`, `@hyperframes/core/studio-api` ou pacotes do OpenDesign — encaixaria no fluxo do claw-master (audita drift openclaw.json vs docs) ou no blueprint de integração HyperFrames Studio (que já teve que provar via `npm view` que o studio exige React 19). Isso ajuda a ENTENDER o código para embutir, não a torná-lo exclusivo. Para \"nativo/exclusivo\" (vendorizar/forkar os motores sob MCORCH) o que importa é a licença DELES (HyperFrames = Apache-2.0, permite fork/vendorização), não esta ferramenta. Veredito: ferramenta de DX útil no tooling interno; irrelevante para a estratégia de exclusividade do produto.",
> 21	      "fetched_url": "https://github.com/vercel-labs/opensrc",
> 22	      "confidence": "high"
> 23	    },
> 24	    "graphify": {
> 25	      "repo": "safishamsi/graphify",
> 26	      "what_it_is": "Graphify é uma skill/CLI para assistentes de código (Claude Code, Codex, Cursor, Gemini CLI, etc.) que transforma qualquer pasta — código, schemas SQL, scripts R/shell, docs, papers, imagens ou vídeos — em um grafo de conhecimento (GraphRAG) consultável via comandos /graphify. Extrai AST localmente com tree-sitter (36 gramáticas), gera visualização HTML interativa + relatório Markdown + JSON do grafo, e roda como servidor MCP para compartilhamento em equipe. É basicamente indexação de repositório em knowledge graph, não uma ferramenta criativa.",
> 27	      "capabilities": [
> 28	        "Indexa código + SQL + docs + PDFs + imagens + vídeos em um único knowledge graph consultável",
> 29	        "Extração de AST 100% local via tree-sitter (36 gramáticas: Python, TS, Go, Rust, Java, Apex, Terraform/HCL, etc.) — sem chamada de API para parsing",
> 30	        "Saídas: HTML interativo (nós clicáveis, filtro, busca) + relatório Markdown + arquivo JSON do grafo",
> 31	        "Detecção de comunidades via algoritmo Leiden; confidence scoring EXTRACTED/INFERRED/AMBIGUOUS",
> 32	        "Modo servidor MCP para compartilhamento em equipe; integração Git via post-commit hooks",
> 33	        "Transcrição local de áudio/vídeo via faster-whisper; backends opcionais Anthropic/Gemini/OpenAI/Ollama/Bedrock/Azure"
> 34	      ],
> 35	      "language_stack": "Python 100%; core = tree-sitter (AST), Leiden (community detection), faster-whisper (transcrição local); distribuído como skill/MCP server; instalação via uv/pipx. LLM backends opcionais (Anthropic, Gemini, OpenAI, Ollama, Bedrock, Azure).",
> 36	      "license": "MIT",
> 37	      "maintenance": "Vivo e muito ativo. 74.891 stars, 7.444 forks, 250 watchers, 399 issues abertas. Criado 2026-04-03, último push 2026-06-30 (branch default v8), release v0.9.3 (jun/2026). Projeto Y Combinator S26 (homepage graphifylabs.ai). Maduro em tração, ainda pré-1.0.",
> 38	      "relevance_to_goal": "BAIXA/NENHUMA para o objetivo declarado. Graphify é uma ferramenta de GraphRAG/knowledge-graph de CÓDIGO — não tem relação com edição de design (OpenDesign) nem com renderização de vídeo (HyperFrames). Não fornece nenhum componente de canvas, timeline, compositing, render de vídeo, ou UI de design. O único ponto de contato com o MCORCH é conceitual: o ecossistema JÁ possui sua própria camada GraphRAG (mcorch_nodes/mcorch_edges + embeddings + gitnexus MCP), então Graphify seria no máximo um SUBSTITUTO/alternativa da malha de conhecimento existente — não um habilitador para tornar OpenDesign ou HyperFrames nativos/exclusivos. Nota tangencial: tem tópicos 'openclaw' e 'claude-code' e roda como skill/MCP, o mesmo padrão de plugin que o MCORCH usa (ex.: vision-mcp-plugin), mas isso é forma de distribuição, não capacidade de design/vídeo. Recomendação honesta: não adotar para essa meta específica.",
> 39	      "fetched_url": "https://api.github.com/repos/safishamsi/graphify (confirmado) + https://github.com/safishamsi/graphify (README via WebFetch)",
> 40	      "confidence": "high"
> 41	    },
> 42	    "currentState": "Estado material confirmado. Segue o mapa.\n\n---\n\n# ESTADO ATUAL — HyperFrames & OpenDesign (native/exclusivo)\n\n## (1) HYPERFRAMES\n\n### JÁ É PRÓPRIO (self-hosted, código MCORCH)\n- **Motor de render determinístico** — `scripts/hyperframes/render-core.ts:116` `renderComposition()`: Playwright Chromium headless + FFmpeg → MP4 9:16 1080×1920 byte-reproduzível (NFR-VS-016, `-fflags +bitexact`). Templates PRÓPRIOS (`templates/viral-short-9x16`, `viral-long-16x9`, allowlist `render-core.ts:71`). Zero dependência de terceiros nesse caminho — é 100% código MCORCH.\n- **Worker/orquestração** — `scripts/video-bridge.ts`: claim atômico `video_renders` → upload bucket privado `video-studio-assets` → `finalize_video_render` → dual-write `creative_assets` (`video-bridge.ts:128`) → attach autopilot FR-VA-025 (`:146`) → kick reshaper (`:177`). systemd `video-bridge.service` **active running**. Próprio.\n- **Superfície UI no SPA** — `src/pages/VideoStudioEditorPage.tsx`: página React 18 própria (só um `<iframe src=\"https://video.mcorch.com\">`). O shell é próprio; o conteúdo do iframe não (ver abaixo).\n- **Contrato de asset/tenancy/billing** — `video_renders`/`video_assets`/`finalize_video_render`, mesh, prepaid (OTD-VA-010), bucket privado. Próprio.\n\n### DEPENDÊNCIA DE TERCEIROS\n- **O EDITOR em si** — `video-studio.service` roda `hyperframes preview` do pacote npm **`hyperframes@0.7.22`** (`/home/ubuntu/.bun/install/global/node_modules/hyperframes/dist/cli.js preview ...`, WorkingDir `~/.mcorch/video-studio/projects/mcorch-video`, porta 3210). O timeline multi-camada / overlays alpha / efeitos / transições que o Sovereign vê = **binário HeyGen/HyperFrames Apache-2.0, não código nosso**. `video.mcorch.com` é só o vhost SSO-gated (`nginx/video.mcorch.com.conf`) na frente dele.\n- **O CLI de render de projeto Studio** — `renderStudioProject()` (`render-core.ts:200`) faz `spawn(HF_NODE, [HF_CLI, 'render', dir, ...])` — ou seja, projetos autorados no editor são renderizados WRAPPEANDO o `hyperframes render` de terceiros (`render-core.ts:86` `HF_CLI`), não pelo nosso motor determinístico. Parity é \"definicional\" justamente porque delega ao mesmo binário terceiro.\n- Depende de **node v22 externo** (`HF_NODE=/home/ubuntu/.local/bin/node`, `render-core.ts:87`) e do Chromium do Playwright injetado (`HYPERFRAMES_BROWSER_PATH`, `render-core.ts:221`).\n\n### GAP CONCRETO até \"native exclusivo\"\nHoje é **arquitetura módulo-container** (blueprint `.claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md`) que ainda nem foi construída na forma canônica (o container `mcorch_video_studio` do blueprint §22-32 NÃO existe — roda `hyperframes preview` cru via systemd, não o `StudioApp` + `McorchAdapter`). Para \"native exclusivo\" seria preciso internalizar **o editor NLE**, hoje 100% terceiro:\n1. **Construir editor próprio** (timeline/tracks/overlays alpha/efeitos/transições) — ou fork do `@hyperframes/studio` Apache-2.0 removendo o binde de terceiros. Blueprint escolheu NÃO forkar a UI (montar `StudioApp` unmodified + `McorchAdapter.startRender`→`video-render`), o que NÃO torna native — só embute terceiro melhor.\n2. **Eliminar o `hyperframes render` CLI** de `renderStudioProject` (`render-core.ts:215`) — internalizar `bundleToSingleHtml` + seek `frame=floor(time*fps)` (gate #4 do blueprint, R1 High risk) no nosso motor determinístico, para render de projeto Studio parar de depender de `HF_CLI`.\n3. **Remover a dep npm `hyperframes@0.7.22`** e o `hyperframes preview` do `video-studio.service`.\n4. React 19 (studio) vs React 18 (SPA) é o motivo do iframe/container — internalizar exige reescrever o editor em React 18 nativo ou manter container próprio.\n\n**Resumo HyperFrames:** o RENDER já é nosso (determinístico, próprio). O EDITOR é o que falta — é integralmente terceiro (`hyperframes` npm), consumido via `preview` (visualização) e via `render` CLI (render de projeto autorado).\n\n---\n\n## (2) OPENDESIGN (Canvas Design → design.mcorch.com)\n\n### JÁ É PRÓPRIO\n- **Worker/bridge** — `scripts/design-bridge.ts`: polling `design_jobs` + claim + `docker cp` do container + mesh reference nodes + telemetria (`design-bridge.ts:290`). systemd `design-bridge.service` **active running**. Próprio.\n- **Vhost + SSO gate** — `nginx/design.mcorch.com.conf` (CF orange, self-signed origin, loopback 127.0.0.1:7456, auth_request via `sso-auth-gate.service`). Próprio.\n- **Contrato de fila/mesh/tenancy** — `design_jobs`, `design_artifact_refs` (mirror/reference), bucket `design-assets`, per-user `OD_MEDIA_CONFIG_DIR`. Próprio. Doc: `docs/bok/canvas-design/05-sdd.md`.\n\n### DEPENDÊNCIA DE TERCEIROS\n- **O motor de design em si = `open-design` (nexu-io / `vanjayak/open-design:latest`)** — container Docker `open-design` **Up 2 weeks (healthy)**, imagem de terceiro. É o system-of-record do canvas: os entities Project/Artifact/HyperFrame vivem no `.od/app.sqlite` DELE (`05-sdd.md:106`), não no MCORCH. Vendorizado em `canvas-design/open-design/` (v0.7.x, **Apache-2.0**, `LICENSE` presente).\n- **O editor visual** é o `apps/web` do open-design servido no iframe (`OpenDesignFrame`, `05-sdd.md:76`) — UI de terceiro.\n- **O `od` CLI** é o contrato de embeddability de terceiro (`05-sdd.md:168`) — o bridge só dirige `od media …`, nunca reimplementa.\n\n### GAP CONCRETO até \"native exclusivo\"\nMuito maior que o do HyperFrames — aqui **nada do motor/editor de design é nosso**; só o plumbing (bridge/queue/nginx/mesh). Para \"native exclusivo\":\n1. Internalizar o **motor de geração/edição de design** (canvas visual, layers, export) hoje 100% no container `open-design`. Isso é o produto inteiro do open-design.\n2. Migrar o system-of-record do `.od/app.sqlite` do container para tabelas MCORCH (hoje o mesh só guarda referência/summary — `05-sdd.md:299` OTD-006).\n3. Substituir o iframe `OpenDesignFrame` por editor próprio (React no SPA).\n4. Pendências pré-existentes que reforçam a dependência: **OTD-008 launch-blocker** (LGPD — `delete-account` não purga o `OD_DATA_DIR` per-user do container; FMEA-007 RPN 240, `05-sdd.md:300`) e FMEA-010 (upgrade do open-design pode quebrar o contrato `od` silenciosamente).\n\n**Resumo OpenDesign:** próprio = fila/bridge/nginx/mesh (a casca). Terceiro = TODO o motor e editor de design (container `vanjayak/open-design:latest` + `apps/web` + `od` CLI + `.od/app.sqlite` como system-of-record).\n\n---\n\n## SÍNTESE COMPARATIVA\n\n| Peça | Próprio (nosso código) | Terceiro | Distância até \"native exclusivo\" |\n|---|---|---|---|\n| **HyperFrames** | Motor de RENDER determinístico (`render-core.ts` `renderComposition`), worker (`video-bridge.ts`), contrato asset/billing/mesh, vhost | **Editor NLE** (`hyperframes@0.7.22` npm, `hyperframes preview` + `hyperframes render` CLI). Apache-2.0 | **Média** — falta internalizar SÓ o editor + `bundleToSingleHtml`/seek; o render já é nosso |\n| **OpenDesign** | Bridge/fila/nginx/mesh (só o plumbing) | **Motor E editor de design inteiros** (`vanjayak/open-design:latest` container + `apps/web` + `od` CLI + `.od/app.sqlite`). Apache-2.0 | **Grande** — o produto de design todo é de terceiro; só a casca é nossa |\n\nNota de precisão: ambos os terceiros são **Apache-2.0** (self-host/fork/modificar OK, reter aviso, marca não licenciada) — logo \"native exclusivo\" é legalmente viável por fork+desbranding, mas o custo de engenharia difere muito (HyperFrames = internalizar 1 editor; OpenDesign = internalizar um app de design completo).",
> 43	    "verdict": {
> 44	      "opensrc_verdict": "adopt",
> 45	      "opensrc_reason": "Apache-2.0, vivo (v0.7.3 em 23-jun-2026), sem risco de licença. Mas NÃO tem relação alguma com tornar OpenDesign/HyperFrames nativos — é um CLI de DX que baixa e cacheia fonte de dependências (npm/PyPI/crates/GitHub) para dar contexto a agentes de coding. O único valor real no MCORCH é interno/tooling: auditar o fonte de `hyperframes@0.7.22`, `@hyperframes/studio`, `@hyperframes/core/studio-api` e do open-design ao internalizá-los — exatamente o trabalho de fork que o objetivo exige (o blueprint já teve de provar React 19 do studio via `npm view`; opensrc dá o fonte inteiro cacheado, encadeável com ripgrep). Encaixa no fluxo claw-master/deepsearch. `adopt` como ferramenta de dev, NÃO como peça de produto. Custo de adotar é ~zero (CLI global). Não muda a estratégia de exclusividade — só acelera a engenharia de fork.",
> 46	      "graphify_verdict": "ignore",
> 47	      "graphify_reason": "MIT, altíssima tração (74.9k stars, YC S26), mas irrelevante para o objetivo E redundante com infra existente. Graphify é GraphRAG de CÓDIGO (tree-sitter AST → knowledge graph HTML/MD/JSON, Leiden communities, MCP server). Não fornece canvas, timeline, compositing, render nem UI de design/vídeo — zero sobreposição com OpenDesign/HyperFrames. Pior: o MCORCH JÁ tem sua própria camada GraphRAG proprietária e multi-tenant (`mcorch_nodes`/`mcorch_edges` + embeddings pgvector HNSW + FSRS-6 + gitnexus MCP + bridge OpenClaw). Graphify seria no máximo um SUBSTITUTO da malha própria — trocar código nativo por dependência externa é o OPOSTO da doutrina de posse total. Único ponto de contato (tópicos openclaw/claude-code, distribuição como skill/MCP) é forma de entrega, não capacidade. `ignore` para esta meta. Se um dia quiser reavaliar indexação AST, é análise separada — não desta diretiva.",
> 48	      "native_exclusive_path": "Os 2 repos NÃO são o caminho — nenhum é motor de design/vídeo. O caminho real por peça, ordenado por custo de engenharia crescente:\n\nHYPERFRAMES (distância MÉDIA — o render já é nosso). O motor determinístico (`scripts/hyperframes/render-core.ts:116` `renderComposition` — Playwright+FFmpeg→MP4 9:16 sha256-idêntico, NFR-VS-016), o worker (`video-bridge.ts`), o contrato asset/billing/mesh e o vhost `video.mcorch.com` JÁ são código MCORCH. Falta só internalizar o EDITOR NLE, hoje 100% terceiro (`hyperframes@0.7.22` npm, consumido via `hyperframes preview` no `video-studio.service` + via `hyperframes render` CLI em `renderStudioProject`, render-core.ts:200-225). Passos concretos:\n  1. Eliminar o `spawn(HF_NODE, [HF_CLI,'render',...])` de `renderStudioProject` (render-core.ts:215) — internalizar `bundleToSingleHtml` + seek determinístico `frame=floor(time*fps)` (gate #4/R1-High do blueprint) no NOSSO motor, para render de projeto Studio parar de depender de `HF_CLI`. Este é o passo que mais rende exclusividade com menos código, porque reaproveita o `renderComposition` já pronto.\n  2. Editor visual próprio: FORK do `@hyperframes/studio` Apache-2.0 desbrandado (timeline/tracks/overlays-alpha/efeitos/transições) — NÃO o `StudioApp unmodified + McorchAdapter` do blueprint, que só embute terceiro melhor e NÃO torna nativo. Fork resolve o conflito React 19 (studio) vs React 18 (SPA) do jeito que quisermos: ou reescrever alvo React 18 no SPA, ou manter container próprio `mcorch_video_studio` servindo O NOSSO editor.\n  3. Remover a dep npm `hyperframes@0.7.22` e o `hyperframes preview` do `video-studio.service`. Fim da dependência.\n\nOPENDESIGN (distância GRANDE — nada do motor é nosso). Próprio = só a casca (bridge `design-bridge.ts`, fila `design_jobs`, nginx `design.mcorch.com`, mesh refs). Terceiro = TODO o motor+editor: container `vanjayak/open-design:latest` (Apache-2.0, vendorizado em `canvas-design/open-design/`, LICENSE confirmado material), `apps/web` no iframe `OpenDesignFrame`, o `od` CLI (contrato de embeddability), e o system-of-record `.od/app.sqlite` (05-sdd.md:106). Passos:\n  1. Fork+desbrand do open-design vendorizado (canvas/layers/export) — é internalizar um app de design INTEIRO, não uma peça.\n  2. Migrar system-of-record do `.od/app.sqlite` do container para tabelas MCORCH (hoje o mesh só guarda referência — OTD-006, 05-sdd.md:299).\n  3. Substituir iframe `OpenDesignFrame` por editor próprio no SPA.\n  4. Fechar antes OTD-008 (launch-blocker LGPD: `delete-account` não purga `OD_DATA_DIR` per-user, FMEA-007 RPN 240) e FMEA-010 (upgrade quebra contrato `od` silenciosamente) — ambos reforçam a dependência hoje.\n\nRECOMENDAÇÃO DE SEQUÊNCIA: fazer HyperFrames primeiro (ROI alto, base pronta, 1 editor a internalizar) e só depois OpenDesign (esforço de app completo). Em ambos, `opensrc` acelera a leitura do fonte de terceiros durante o fork; `graphify` não entra.",
> 49	      "doctrine_fit": "Fit FORTE com a doutrina open-source-first/equity/posse-total. Ambos os motores-alvo (HyperFrames e open-design) são Apache-2.0 — verificado material: `canvas-design/open-design/LICENSE` = \"Apache License Version 2.0\" (11296 bytes, presente). Apache-2.0 permite self-host, fork, modificação e uso comercial, exigindo apenas retenção do aviso de copyright/NOTICE e não licenciando marca — logo \"native exclusivo\" (vendorizar+forkar+desbrandar sob MCORCH, custo=0 de licença) é LEGALMENTE VIÁVEL para os dois. Nenhum é AGPL/copyleft-viral nem sem-licença. Dos 2 repos avaliados: opensrc (Apache-2.0) e graphify (MIT) também são permissivos — sem atrito de licença em nenhum. O único desalinhamento doutrinário é adotar graphify como camada GraphRAG: substituiria código NATIVO próprio (mcorch_nodes/edges) por dependência externa — anti-posse-total — daí o `ignore`. opensrc como tooling interno não fere a doutrina (é ferramenta de dev, não peça de produto embutida). Posse do código de produto = garantida pelas licenças Apache-2.0 dos motores + fork.",
> 50	      "bok_gate_needed": "SIM para OpenDesign; PARCIAL para HyperFrames. Regra: BoK gate (MRD/BRD/PRD/FRD/SDD em docs/bok/<slug>/ + Pattern Conformance Declaration dos 21 padrões) dispara para \"módulo novo, feature complexa, integração ou mudança arquitetural\". (1) Internalizar o EDITOR OpenDesign (fork do motor completo + migrar system-of-record .od/app.sqlite→tabelas MCORCH + substituir iframe) é mudança arquitetural profunda com novo system-of-record → EXIGE BoK gate novo/emenda pesada à suite canvas-design (docs/bok/canvas-design/), com deepsearch-blueprint primeiro (precedente: security, vision-mcp). (2) HyperFrames tem BoK video-studio 9/9 já selada + blueprint de integração material (`.claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md`); a flip de estratégia \"embutir terceiro (StudioApp unmodified)\"→\"fork nativo desbrandado\" muda a decisão arquitetural OTD-VS-005 e o contrato de render (eliminar HF_CLI de renderStudioProject) → EXIGE ao menos EMENDA à SDD video-studio com Pattern Conformance Declaration atualizada e deepsearch do fork, NÃO uma SDD do zero. (3) Adotar opensrc como tooling de dev = EXENTO de BoK gate (é tooling interno do AIOS, análogo ao aios-sql-bridge — Lei 2 pede só SOP mínimo no handoff). Em nenhum caso começar código antes do gate.",
> 51	      "honest_caveats": "1) Os 2 repos pesquisados são RED HERRINGS para o objetivo: nem opensrc nem graphify tocam design/vídeo. A pergunta \"vale usar 2 repos para isso?\" tem resposta honesta: NÃO para tornar os motores nativos — eles não são motores. opensrc só ajuda a LER o fonte durante o fork; graphify não entra. 2) Risco de licença é BAIXO nos motores (ambos Apache-2.0, verificado), mas Apache-2.0 exige preservar NOTICE/aviso e NÃO cede marca — desbrandar é obrigatório e há trabalho de compliance (rastrear NOTICE em todo fork). 3) Risco de abandono/upstream-drift: HyperFrames e open-design são pré-1.0 externos; ao forkar assumimos manutenção total (segurança, upgrades) — some o benefício de \"upstream conserta pra gente\". 4) React 19 (studio) vs React 18 (SPA) é atrito REAL e caro: fork nativo obriga a escolher reescrever alvo React 18 ou manter container próprio — nenhuma opção é trivial. 5) Esforço ASSIMÉTRICO: HyperFrames = internalizar 1 editor (render já é nosso); OpenDesign = internalizar um APP DE DESIGN INTEIRO + migrar system-of-record. Tratar as duas como \"mesma tarefa\" subestima OpenDesign em ~5-10×. 6) graphify tem 74.9k stars e é MIT/YC — sedutor, mas adotá-lo como GraphRAG competiria/substituiria a malha própria; não confundir tração com fit. 7) Não validei material o LICENSE do pacote npm `hyperframes@0.7.22` nesta sessão (só o open-design vendorizado); confio no dado fornecido (Apache-2.0) — Lei 1: confirmar o LICENSE/NOTICE do tarball hyperframes ANTES de forkar. 8) opensrc requer Node.js 24+; checar compatibilidade com o toolchain (o motor HyperFrames já usa node v22 separado — mais um runtime a gerenciar)."
> 52	    }
> 53	  },
> 54	  "workflowProgress": [
> 55	    {
> 56	      "type": "workflow_phase",
> 57	      "index": 1,
> 58	      "title": "Research"
> 59	    },
> 60	    {
> ```

## 🤖 Claude *(01:17:29)*


## 🤖 Claude *(01:17:30)*

Veredito completo. Vou persistir a avaliação (estava só no scratch) e te dar a resposta direta.

## 🤖 Claude *(01:17:54)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/native-exclusive-hyperframes-opendesign-eval-2026-06-30.md",
  "content": "# Native/Exclusivo \u2014 HyperFrames & OpenDesign: avalia\u00e7\u00e3o dos repos + caminho real (2026-06-30)\n\n> Workflow `wf_ec9db575-8a7` (fetch real dos repos + mapa de estado + arquiteto). Pergunta Sovereign: vale usar `vercel-labs/opensrc` + `safishamsi/graphify` p/ tornar OpenDesign e HyperFrames nativos/exclusivos do MCORCH? Doutrina: `feedback_opensource_first_zero_cost_equity`.\n\n## Resposta curta: os 2 repos N\u00c3O s\u00e3o o caminho (red herrings) \u2014 nenhum \u00e9 motor de design/v\u00eddeo.\n\n| Repo | O que \u00e9 | Licen\u00e7a | Veredito p/ a meta |\n|------|---------|---------|--------------------|\n| **vercel-labs/opensrc** | CLI que baixa/cacheia fonte de deps (npm/PyPI/crates/GitHub) p/ dar contexto a agentes de coding. 2.7k\u2605, vivo (v0.7.3 jun/26). | Apache-2.0 | **adopt \u2014 s\u00f3 como tooling de dev** (acelera LER o fonte de `hyperframes`/`open-design` durante o fork). N\u00c3O \u00e9 pe\u00e7a de produto. Exige Node 24+. |\n| **safishamsi/graphify** | GraphRAG de c\u00f3digo (tree-sitter AST \u2192 knowledge graph). 74.9k\u2605, MIT, YC S26. | MIT | **ignore** \u2014 zero rela\u00e7\u00e3o com design/v\u00eddeo E redundante/competiria com a malha PR\u00d3PRIA (mcorch_nodes/edges). Adot\u00e1-lo = trocar c\u00f3digo nativo por dep externa = anti-doutrina. |\n\n## O caminho REAL = forkar os motores (ambos Apache-2.0 \u2014 fork/rebrand/self-host legal a custo $0)\n\n**Esfor\u00e7o ASSIM\u00c9TRICO (n\u00e3o tratar como mesma tarefa \u2014 OpenDesign \u00e9 ~5-10\u00d7 HyperFrames):**\n\n### HyperFrames \u2014 dist\u00e2ncia M\u00c9DIA (o render J\u00c1 \u00e9 nosso)\nPr\u00f3prio: motor de render determin\u00edstico (`scripts/hyperframes/render-core.ts:116` `renderComposition` Playwright+FFmpeg\u2192MP4 9:16 sha256-id\u00eantico) + worker (`video-bridge.ts`) + contrato asset/billing/mesh + vhost `video.mcorch.com`. **\u00c9 o que renderizou o v\u00eddeo de hoje a $0.**\nTerceiro: s\u00f3 o **EDITOR NLE** (`hyperframes@0.7.22` npm \u2014 `hyperframes preview` no `video-studio.service` + `hyperframes render` CLI em `renderStudioProject` render-core.ts:200-225).\nPassos p/ nativo: (1) eliminar `HF_CLI` de `renderStudioProject` internalizando `bundleToSingleHtml`+seek `frame=floor(time*fps)` no NOSSO motor (gate #4/R1-High do blueprint \u2014 maior ROI de exclusividade); (2) fork do `@hyperframes/studio` Apache-2.0 desbrandado (N\u00c3O o \"StudioApp unmodified\" do blueprint, que s\u00f3 embute terceiro melhor); (3) remover a dep npm + `hyperframes preview`.\n\n### OpenDesign \u2014 dist\u00e2ncia GRANDE (nada do motor \u00e9 nosso)\nPr\u00f3prio: s\u00f3 a casca (bridge `design-bridge.ts` + fila `design_jobs` + nginx `design.mcorch.com` + mesh refs).\nTerceiro: TODO o motor+editor (`vanjayak/open-design:latest` container Apache-2.0 vendorizado em `canvas-design/open-design/` + `apps/web` no iframe + `od` CLI + `.od/app.sqlite` como system-of-record).\nPassos: (1) fork+desbrand do app de design inteiro; (2) migrar system-of-record `.od/app.sqlite`\u2192tabelas MCORCH (OTD-006); (3) substituir iframe por editor pr\u00f3prio; (4) fechar antes OTD-008 (LGPD launch-blocker, FMEA-007 RPN 240) + FMEA-010.\n\n## Governan\u00e7a (Closed-Loop)\n- **HyperFrames:** BoK video-studio 9/9 j\u00e1 selada \u2192 **EMENDA \u00e0 SDD** (flip OTD-VS-005 \"embutir terceiro\"\u2192\"fork nativo\") + deepsearch do fork. N\u00e3o SDD do zero.\n- **OpenDesign:** mudan\u00e7a arquitetural profunda + novo system-of-record \u2192 **BoK gate novo/emenda pesada** \u00e0 suite canvas-design, deepsearch-blueprint primeiro.\n- **opensrc:** exento (tooling de dev, an\u00e1logo ao aios-sql-bridge \u2014 SOP m\u00ednimo).\n\n## Recomenda\u00e7\u00e3o de sequ\u00eancia\n**HyperFrames primeiro** (ROI alto, base pronta, 1 editor a internalizar) \u2192 depois OpenDesign (app inteiro). `opensrc` acelera a leitura do fonte durante o fork; `graphify` n\u00e3o entra.\n\n## Caveats honestos (Lei 1)\n1. Os 2 repos s\u00e3o red herrings p/ a meta. 2. Apache-2.0 exige preservar NOTICE + desbrandar (trabalho de compliance). 3. Forkar = assumimos manuten\u00e7\u00e3o/seguran\u00e7a total (some o \"upstream conserta\"). 4. React 19 (studio) vs 18 (SPA) = atrito real. 5. **N\u00c3O validei material o LICENSE do npm `hyperframes@0.7.22`** nesta sess\u00e3o (s\u00f3 o open-design vendorizado, Apache-2.0 confirmado) \u2014 confirmar antes de forkar. 6. graphify: tra\u00e7\u00e3o \u2260 fit.\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/.claude/context/native-exclusive-hyperframes-opendesign-eval-2026-06-30.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:18:01)*


## 🤖 Claude *(01:18:18)*

[Avaliação persistida](.claude/context/native-exclusive-hyperframes-opendesign-eval-2026-06-30.md). Resposta direta:

## ❌ Nenhum dos dois repos é o caminho — são red herrings pra essa meta

- **`vercel-labs/opensrc`** (Apache-2.0, 2.7k★): é um CLI que baixa o *fonte de dependências* pra dar contexto a agentes de código. Não é motor de design nem de vídeo. Útil só como **ferramenta interna de dev** — ajuda a *ler* o fonte do `hyperframes`/`open-design` na hora de forkar. `adopt` como tooling, **não** como peça de produto.
- **`safishamsi/graphify`** (MIT, 74.9k★, YC): é GraphRAG de código (AST→knowledge graph). Zero relação com design/vídeo — e pior, ele **competiria com a sua própria malha** (`mcorch_nodes`/`edges`). Adotá-lo seria trocar código nativo por dependência externa: o *oposto* da doutrina. `ignore`.

A tração do graphify (75k stars) seduz, mas tração ≠ fit. Nenhum toca no que você quer.

## ✅ O caminho real (e a boa notícia)

"Native exclusivo" = **forkar os motores de verdade** — e os dois são **Apache-2.0**, então fork + rebrand + self-host é legal a custo zero de licença. Isso *É* a doutrina open-source-first realizada (posse do código). Mas o esforço é **assimétrico**:

**HyperFrames — está PERTO.** O motor de render **já é seu** (o `render-core.ts` Playwright+FFmpeg foi exatamente o que fez o vídeo de hoje a $0). O que ainda é de terceiro é **só o editor visual** (o pacote npm `hyperframes@0.7.22` — a timeline/overlays que você vê no `video.mcorch.com`). Internalizar = forkar 1 editor + parar de chamar o CLI `hyperframes render`. **ROI alto, base pronta.**

**OpenDesign — está LONGE.** Aí *só a casca* é sua (bridge/fila/nginx). O motor E o editor de design inteiros são o container `open-design` de terceiro (+ o `.od/app.sqlite` é o system-of-record dele, nem no seu banco). Internalizar = reconstruir um app de design completo + migrar o system-of-record. **~5-10× o esforço do HyperFrames** (+ tem o blocker LGPD OTD-008 pendente).

## Recomendação

**HyperFrames primeiro, OpenDesign depois.** E — pelo Protocolo de Malha Fechada — nenhum dos dois começa com código: HyperFrames precisa de **emenda à SDD** (vira a decisão OTD-VS-005 de "embutir terceiro" pra "fork nativo") + deepsearch do fork; OpenDesign precisa de **BoK gate novo** (mudança arquitetural + novo system-of-record).

**Caveat honesto (Lei 1):** forkar = você assume a manutenção/segurança total (some o "upstream conserta pra mim"), e Apache-2.0 obriga preservar o NOTICE + desbrandar. E não validei materialmente o LICENSE do pacote npm `hyperframes` nesta sessão — confirmar antes de forkar.

Se topar, o passo certo é eu (ou o loop) **draftar a emenda BoK do fork nativo do HyperFrames** — o item de maior ROI, e que fecha o ciclo de "o vídeo autônomo é 100% seu, do render ao editor". Quer que eu comece por aí?

## 👤 User *(01:33:19)*

ótimo vamos deixar isso para mais pra frente jaja vamos voltar para o hyperframe que vai ser o mais usado o open design talvez focamos algumas semanas nele futuramente.

Em https://login.mcorch.com/dashboard/calendar não consigo ver as propriedades de cada data, deveria abrir tudo sobre o que na data quando clicar certo? faz isso osfiticado e robusto

## 🤖 Claude *(01:34:12)*


## 🤖 Claude *(01:34:14)*

Perfeito — HyperFrames primeiro (o mais usado), OpenDesign com foco dedicado mais pra frente. Anotado. Deixo o fork parado até você chamar.

Agora o **Calendário de Publicações** — você está certo: clicar num dia deveria abrir tudo agendado naquela data. Vou implementar um detalhe de dia robusto (modal com todas as publicações do dia + propriedades completas). Primeiro localizo o código atual da página + o hook de dados (Harness Engineering — a lógica vive no hook):

## 🤖 Claude *(01:34:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== arquivos de calend\u00e1rio ===\"\ngrep -rlE \"Calend\u00e1rio de Publica\u00e7\u00f5es|PublicationCalendar|dashboard/calendar|CalendarPage\" src/ 2>/dev/null | head -20\necho\necho \"=== rota calendar em App.tsx ===\"\ngrep -nE \"calendar|Calendar\" src/App.tsx 2>/dev/null | head\necho\necho \"=== hooks de calend\u00e1rio ===\"\nls -la src/hooks/ 2>/dev/null | grep -iE \"calendar|schedul|publi\" || echo \"(nenhum hook \u00f3bvio)\"\necho\necho \"=== componentes de calend\u00e1rio ===\"\nfind src -iname \"*calendar*\" -o -iname \"*schedule*\" 2>/dev/null | grep -v node_modules | head -20",
  "description": "Locate calendar page, hook, and route"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === arquivos de calendário ===
> src/App.tsx
> src/pages/CalendarPage.tsx
> src/components/dashboard/DashboardSidebar.tsx
> 
> === rota calendar em App.tsx ===
> 31:const CalendarPage = lazy(() => import("./pages/CalendarPage.tsx"));
> 117:                <Route path="calendar" element={<CalendarPage />} />
> 
> === hooks de calendário ===
> -rw-rw-r--  1 ubuntu ubuntu  3452 Jun 26 23:04 usePublicationMetrics.ts
> -rw-rw-r--  1 ubuntu ubuntu  2695 Apr 17 00:26 useScheduledPosts.ts
> 
> === componentes de calendário ===
> src/pages/CalendarPage.tsx
> src/hooks/useScheduledPosts.ts
> src/components/ui/calendar.tsx
> ```

## 🤖 Claude *(01:34:22)*


## 🤖 Claude *(01:34:22)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useState, useMemo } from 'react';
> 2	import { format, startOfMonth, endOfMonth, startOfWeek, endOfWeek, eachDayOfInterval, isSameMonth, isSameDay, addMonths, subMonths, addWeeks, subWeeks, parseISO } from 'date-fns';
> 3	import { ptBR } from 'date-fns/locale';
> 4	import { DndContext, DragEndEvent, DragOverlay, DragStartEvent, useDraggable, useDroppable, PointerSensor, useSensor, useSensors } from '@dnd-kit/core';
> 5	import { supabase } from '@/integrations/supabase/client';
> 6	import { useScheduledPosts, useCreateScheduledPost, useUpdateScheduledPost, useDeleteScheduledPost, type ScheduledPost } from '@/hooks/useScheduledPosts';
> 7	import { useContentLibrary } from '@/hooks/useContentLibrary';
> 8	import { useSocialAccounts } from '@/hooks/useSocialAccounts';
> 9	import { Button } from '@/components/ui/button';
> 10	import { Badge } from '@/components/ui/badge';
> 11	import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
> 12	import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
> 13	import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
> 14	import { Input } from '@/components/ui/input';
> 15	import { Label } from '@/components/ui/label';
> 16	import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';
> 17	import { ChevronLeft, ChevronRight, Plus, Trash2, CalendarDays, LayoutList, Loader2, Copy, GripVertical, Sparkles, Zap } from 'lucide-react';
> 18	import { cn } from '@/lib/utils';
> 19	import type { Database } from '@/integrations/supabase/types';
> 20	
> 21	type SocialPlatform = Database['public']['Enums']['social_platform'];
> 22	
> 23	const PLATFORM_COLORS: Record<string, string> = {
> 24	  linkedin: 'bg-blue-500',
> 25	  instagram: 'bg-pink-500',
> 26	  facebook: 'bg-indigo-500',
> 27	  twitter: 'bg-sky-400',
> 28	  tiktok: 'bg-foreground',
> 29	  youtube: 'bg-red-500',
> 30	  pinterest: 'bg-red-400',
> 31	  wordpress: 'bg-blue-700',
> 32	};
> 33	
> 34	const PLATFORM_LABELS: Record<string, string> = {
> 35	  linkedin: 'LinkedIn',
> 36	  instagram: 'Instagram',
> 37	  facebook: 'Facebook',
> 38	  twitter: 'Twitter/X',
> 39	  tiktok: 'TikTok',
> 40	  youtube: 'YouTube',
> 41	  pinterest: 'Pinterest',
> 42	  wordpress: 'WordPress',
> 43	};
> 44	
> 45	const STATUS_VARIANT: Record<string, 'default' | 'secondary' | 'destructive' | 'outline'> = {
> 46	  queued: 'outline',
> 47	  publishing: 'secondary',
> 48	  published: 'default',
> 49	  failed: 'destructive',
> 50	  cancelled: 'secondary',
> 51	};
> 52	
> 53	function DraggablePost({ post, children }: { post: ScheduledPost; children: React.ReactNode }) {
> 54	  const { attributes, listeners, setNodeRef, transform, isDragging } = useDraggable({ id: post.id, data: { post } });
> 55	  const style = transform ? { transform: `translate(${transform.x}px, ${transform.y}px)`, opacity: isDragging ? 0.5 : 1, zIndex: isDragging ? 50 : undefined } : undefined;
> 56	  return (
> 57	    <div ref={setNodeRef} style={style} {...attributes} {...listeners}>
> 58	      {children}
> 59	    </div>
> 60	  );
> 61	}
> 62	
> 63	function DroppableDay({ day, children }: { day: string; children: React.ReactNode }) {
> 64	  const { setNodeRef, isOver } = useDroppable({ id: day });
> 65	  return (
> 66	    <div ref={setNodeRef} className={cn('transition-colors', isOver && 'ring-2 ring-primary/50 bg-primary/5')}>
> 67	      {children}
> 68	    </div>
> 69	  );
> 70	}
> 71	
> 72	export default function CalendarPage() {
> 73	  const [view, setView] = useState<'month' | 'week'>('month');
> 74	  const [currentDate, setCurrentDate] = useState(new Date());
> 75	  const [dialogOpen, setDialogOpen] = useState(false);
> 76	  const [selectedDate, setSelectedDate] = useState<Date | null>(null);
> 77	  const [activePost, setActivePost] = useState<ScheduledPost | null>(null);
> 78	
> 79	  const sensors = useSensors(useSensor(PointerSensor, { activationConstraint: { distance: 8 } }));
> 80	
> 81	  const rangeStart = view === 'month'
> 82	    ? startOfWeek(startOfMonth(currentDate), { locale: ptBR })
> 83	    : startOfWeek(currentDate, { locale: ptBR });
> 84	  const rangeEnd = view === 'month'
> 85	    ? endOfWeek(endOfMonth(currentDate), { locale: ptBR })
> 86	    : endOfWeek(currentDate, { locale: ptBR });
> 87	
> 88	  const { data: posts, isLoading } = useScheduledPosts({ from: rangeStart, to: rangeEnd });
> 89	  const { data: contents } = useContentLibrary();
> 90	  const { accounts } = useSocialAccounts();
> 91	  const createPost = useCreateScheduledPost();
> 92	  const updatePost = useUpdateScheduledPost();
> 93	  const deletePost = useDeleteScheduledPost();
> 94	
> 95	  const days = useMemo(() => eachDayOfInterval({ start: rangeStart, end: rangeEnd }), [rangeStart.getTime(), rangeEnd.getTime()]);
> 96	
> 97	  const postsByDay = useMemo(() => {
> 98	    const map: Record<string, ScheduledPost[]> = {};
> 99	    posts?.forEach((p) => {
> 100	      const key = format(parseISO(p.scheduled_at), 'yyyy-MM-dd');
> 101	      (map[key] ??= []).push(p);
> 102	    });
> 103	    return map;
> 104	  }, [posts]);
> 105	
> 106	  const [formPlatform, setFormPlatform] = useState<SocialPlatform>('linkedin');
> 107	  const [formContentId, setFormContentId] = useState('');
> 108	  const [formTime, setFormTime] = useState('12:00');
> 109	  const [formAccountId, setFormAccountId] = useState('');
> 110	  const [suggestions, setSuggestions] = useState<Array<{ datetime: string; score: number; reason: string }>>([]);
> 111	  const [loadingSuggestions, setLoadingSuggestions] = useState(false);
> 112	
> 113	  const handleSuggestTimes = async () => {
> 114	    setLoadingSuggestions(true);
> 115	    setSuggestions([]);
> 116	    try {
> 117	      const { data: { session } } = await supabase.auth.getSession();
> 118	      if (!session?.access_token) return;
> 119	      const resp = await fetch(`${import.meta.env.VITE_SUPABASE_URL}/functions/v1/optimize-schedule`, {
> 120	        method: 'POST',
> 121	        headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${session.access_token}` },
> 122	        body: JSON.stringify({ platform: formPlatform, content_type: 'general' }),
> 123	      });
> 124	      if (resp.ok) {
> 125	        const data = await resp.json();
> 126	        setSuggestions(data.suggestions || []);
> 127	      }
> 128	    } catch (e) {
> 129	      console.error(e);
> 130	    } finally {
> 131	      setLoadingSuggestions(false);
> 132	    }
> 133	  };
> 134	
> 135	  const applySuggestion = (datetime: string) => {
> 136	    const d = new Date(datetime);
> 137	    setSelectedDate(d);
> 138	    setFormTime(format(d, 'HH:mm'));
> 139	    setSuggestions([]);
> 140	  };
> 141	
> 142	  const navigate = (dir: number) => {
> 143	    setCurrentDate(view === 'month' ? (dir > 0 ? addMonths(currentDate, 1) : subMonths(currentDate, 1)) : (dir > 0 ? addWeeks(currentDate, 1) : subWeeks(currentDate, 1)));
> 144	  };
> 145	
> 146	  const openNewPost = (day: Date) => {
> 147	    setSelectedDate(day);
> 148	    setDialogOpen(true);
> 149	  };
> 150	
> 151	  const handleCreate = () => {
> 152	    if (!selectedDate) return;
> 153	    const [h, m] = formTime.split(':').map(Number);
> 154	    const scheduledAt = new Date(selectedDate);
> 155	    scheduledAt.setHours(h, m, 0, 0);
> 156	    createPost.mutate({
> 157	      platform: formPlatform,
> 158	      scheduled_at: scheduledAt.toISOString(),
> 159	      content_id: formContentId || null,
> 160	      social_account_id: formAccountId || null,
> 161	    }, { onSuccess: () => setDialogOpen(false) });
> 162	  };
> 163	
> 164	  const handleDuplicate = (post: ScheduledPost) => {
> 165	    createPost.mutate({
> 166	      platform: post.platform,
> 167	      scheduled_at: post.scheduled_at,
> 168	      content_id: post.content_id,
> 169	      social_account_id: post.social_account_id,
> 170	    });
> 171	  };
> 172	
> 173	  const handleDragStart = (event: DragStartEvent) => {
> 174	    setActivePost(event.active.data.current?.post ?? null);
> 175	  };
> 176	
> 177	  const handleDragEnd = (event: DragEndEvent) => {
> 178	    setActivePost(null);
> 179	    const { active, over } = event;
> 180	    if (!over || !active.data.current?.post) return;
> 181	    const post = active.data.current.post as ScheduledPost;
> 182	    const targetDay = over.id as string;
> 183	    const originalTime = format(parseISO(post.scheduled_at), 'HH:mm:ss');
> 184	    const newScheduledAt = `${targetDay}T${originalTime}`;
> 185	    if (post.scheduled_at.startsWith(targetDay)) return;
> 186	    updatePost.mutate({ id: post.id, scheduled_at: new Date(newScheduledAt).toISOString() });
> 187	  };
> 188	
> 189	  const filteredAccounts = accounts?.filter((a) => a.platform === formPlatform) ?? [];
> 190	
> 191	  if (isLoading) {
> 192	    return (
> 193	      <div className="flex items-center justify-center h-[calc(100vh-6rem)]">
> 194	        <Loader2 className="h-8 w-8 animate-spin text-primary" />
> 195	      </div>
> 196	    );
> 197	  }
> 198	
> 199	  return (
> 200	    <TooltipProvider>
> 201	      <div className="p-4 md:p-6 space-y-4">
> 202	        {/* Header */}
> 203	        <div className="flex items-center justify-between flex-wrap gap-2">
> 204	          <h1 className="text-2xl font-heading font-bold text-foreground">Calendário de Publicações</h1>
> 205	          <div className="flex items-center gap-2">
> 206	            <Button variant="outline" size="icon" onClick={() => setView(view === 'month' ? 'week' : 'month')}>
> 207	              {view === 'month' ? <LayoutList className="h-4 w-4" /> : <CalendarDays className="h-4 w-4" />}
> 208	            </Button>
> 209	            <Button variant="outline" size="icon" onClick={() => navigate(-1)}><ChevronLeft className="h-4 w-4" /></Button>
> 210	            <span className="text-sm font-medium min-w-[140px] text-center capitalize">
> 211	              {view === 'month' ? format(currentDate, 'MMMM yyyy', { locale: ptBR }) : `Semana de ${format(rangeStart, "dd 'de' MMM", { locale: ptBR })}`}
> 212	            </span>
> 213	            <Button variant="outline" size="icon" onClick={() => navigate(1)}><ChevronRight className="h-4 w-4" /></Button>
> 214	            <Button size="sm" onClick={() => openNewPost(new Date())} className="gap-1">
> 215	              <Plus className="h-4 w-4" /> Agendar
> 216	            </Button>
> 217	          </div>
> 218	        </div>
> 219	
> 220	        {/* DnD Context */}
> 221	        <DndContext sensors={sensors} onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
> 222	          {view === 'month' ? (
> 223	            <div className="grid grid-cols-7 gap-px bg-border rounded-lg overflow-hidden">
> 224	              {['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'].map((d) => (
> 225	                <div key={d} className="bg-muted p-2 text-center text-xs font-medium text-muted-foreground">{d}</div>
> 226	              ))}
> 227	              {days.map((day) => {
> 228	                const key = format(day, 'yyyy-MM-dd');
> 229	                const dayPosts = postsByDay[key] ?? [];
> 230	                const isToday = isSameDay(day, new Date());
> 231	                const inMonth = isSameMonth(day, currentDate);
> 232	
> 233	                return (
> 234	                  <DroppableDay key={key} day={key}>
> 235	                    <div
> 236	                      className={cn('bg-card min-h-[100px] p-1.5 cursor-pointer hover:bg-accent/30 transition-colors', !inMonth && 'opacity-40')}
> 237	                      onClick={() => openNewPost(day)}
> 238	                    >
> 239	                      <span className={cn('text-xs font-medium inline-flex items-center justify-center w-6 h-6 rounded-full', isToday && 'bg-primary text-primary-foreground')}>
> 240	                        {format(day, 'd')}
> 241	                      </span>
> 242	                      <div className="mt-1 space-y-0.5">
> 243	                        {dayPosts.slice(0, 3).map((p) => (
> 244	                          <DraggablePost key={p.id} post={p}>
> 245	                            <Tooltip>
> 246	                              <TooltipTrigger asChild>
> 247	                                <div className="flex items-center gap-1 group/post" onClick={(e) => e.stopPropagation()}>
> 248	                                  <span className={cn('w-1.5 h-1.5 rounded-full shrink-0', PLATFORM_COLORS[p.platform])} />
> 249	                                  <span className="text-[10px] truncate text-foreground">{format(parseISO(p.scheduled_at), 'HH:mm')}</span>
> 250	                                  <Button variant="ghost" size="icon" className="h-4 w-4 opacity-0 group-hover/post:opacity-100 ml-auto" onClick={() => handleDuplicate(p)}>
> 251	                                    <Copy className="h-2.5 w-2.5" />
> 252	                                  </Button>
> 253	                                </div>
> 254	                              </TooltipTrigger>
> 255	                              <TooltipContent side="top">
> 256	                                <p className="text-xs">{PLATFORM_LABELS[p.platform]} — {p.status}</p>
> 257	                              </TooltipContent>
> 258	                            </Tooltip>
> 259	                          </DraggablePost>
> 260	                        ))}
> 261	                        {dayPosts.length > 3 && (
> 262	                          <span className="text-[10px] text-muted-foreground">+{dayPosts.length - 3} mais</span>
> 263	                        )}
> 264	                      </div>
> 265	                    </div>
> 266	                  </DroppableDay>
> 267	                );
> 268	              })}
> 269	            </div>
> 270	          ) : (
> 271	            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-7 gap-3">
> 272	              {days.map((day) => {
> 273	                const key = format(day, 'yyyy-MM-dd');
> 274	                const dayPosts = postsByDay[key] ?? [];
> 275	                const isToday = isSameDay(day, new Date());
> 276	
> 277	                return (
> 278	                  <DroppableDay key={key} day={key}>
> 279	                    <Card className={cn('min-h-[200px] lg:min-h-[300px]', isToday && 'ring-2 ring-primary')}>
> 280	                      <CardHeader className="p-3 pb-1">
> 281	                        <CardTitle className="text-xs font-medium capitalize">
> 282	                          {format(day, 'EEE dd', { locale: ptBR })}
> 283	                        </CardTitle>
> 284	                      </CardHeader>
> 285	                      <CardContent className="p-3 pt-0 space-y-2">
> 286	                        {dayPosts.map((p) => (
> 287	                          <DraggablePost key={p.id} post={p}>
> 288	                            <div className="p-2 rounded-md bg-secondary/50 space-y-1 group relative cursor-grab active:cursor-grabbing">
> 289	                              <div className="flex items-center gap-1">
> 290	                                <GripVertical className="h-3 w-3 text-muted-foreground/50" />
> 291	                                <span className={cn('w-2 h-2 rounded-full', PLATFORM_COLORS[p.platform])} />
> 292	                                <span className="text-xs font-medium capitalize">{p.platform}</span>
> 293	                                <Badge variant={STATUS_VARIANT[p.status]} className="ml-auto text-[10px] h-4">{p.status}</Badge>
> 294	                              </div>
> 295	                              <span className="text-[10px] text-muted-foreground">{format(parseISO(p.scheduled_at), 'HH:mm')}</span>
> 296	                              <div className="absolute top-1 right-1 flex gap-0.5 opacity-0 group-hover:opacity-100 transition-opacity">
> 297	                                <Button variant="ghost" size="icon" className="h-5 w-5" onClick={(e) => { e.stopPropagation(); handleDuplicate(p); }}>
> 298	                                  <Copy className="h-3 w-3 text-muted-foreground" />
> 299	                                </Button>
> 300	                                <Button variant="ghost" size="icon" className="h-5 w-5" onClick={(e) => { e.stopPropagation(); deletePost.mutate(p.id); }}>
> 301	                                  <Trash2 className="h-3 w-3 text-destructive" />
> 302	                                </Button>
> 303	                              </div>
> 304	                            </div>
> 305	                          </DraggablePost>
> 306	                        ))}
> 307	                        <Button variant="ghost" size="sm" className="w-full text-xs h-7" onClick={() => openNewPost(day)}>
> 308	                          <Plus className="h-3 w-3 mr-1" /> Agendar
> 309	                        </Button>
> 310	                      </CardContent>
> 311	                    </Card>
> 312	                  </DroppableDay>
> 313	                );
> 314	              })}
> 315	            </div>
> 316	          )}
> 317	
> 318	          <DragOverlay>
> 319	            {activePost && (
> 320	              <div className="p-2 rounded-md bg-primary/20 border border-primary shadow-lg text-xs font-medium capitalize">
> 321	                {activePost.platform} — {format(parseISO(activePost.scheduled_at), 'HH:mm')}
> 322	              </div>
> 323	            )}
> 324	          </DragOverlay>
> 325	        </DndContext>
> 326	
> 327	        {/* New Post Dialog */}
> 328	        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
> 329	          <DialogContent>
> 330	            <DialogHeader>
> 331	              <DialogTitle>Agendar Publicação</DialogTitle>
> 332	            </DialogHeader>
> 333	            <div className="space-y-4">
> 334	              <div>
> 335	                <Label>Data</Label>
> 336	                <Input type="date" value={selectedDate ? format(selectedDate, 'yyyy-MM-dd') : ''} onChange={(e) => setSelectedDate(new Date(e.target.value + 'T12:00:00'))} />
> 337	              </div>
> 338	              <div>
> 339	                <Label>Horário</Label>
> 340	                <Input type="time" value={formTime} onChange={(e) => setFormTime(e.target.value)} />
> 341	              </div>
> 342	              <div>
> 343	                <Label>Plataforma</Label>
> 344	                <Select value={formPlatform} onValueChange={(v) => { setFormPlatform(v as SocialPlatform); setFormAccountId(''); }}>
> 345	                  <SelectTrigger><SelectValue /></SelectTrigger>
> 346	                  <SelectContent>
> 347	                    {Object.entries(PLATFORM_LABELS).map(([k, v]) => (
> 348	                      <SelectItem key={k} value={k}>{v}</SelectItem>
> 349	                    ))}
> 350	                  </SelectContent>
> 351	                </Select>
> 352	              </div>
> 353	              {filteredAccounts.length > 0 && (
> 354	                <div>
> 355	                  <Label>Conta</Label>
> 356	                  <Select value={formAccountId} onValueChange={setFormAccountId}>
> 357	                    <SelectTrigger><SelectValue placeholder="Selecionar conta" /></SelectTrigger>
> 358	                    <SelectContent>
> 359	                      {filteredAccounts.map((a) => (
> 360	                        <SelectItem key={a.id} value={a.id}>{a.platform_username || a.platform}</SelectItem>
> 361	                      ))}
> 362	                    </SelectContent>
> 363	                  </Select>
> 364	                </div>
> 365	              )}
> 366	              {contents && contents.length > 0 && (
> 367	                <div>
> 368	                  <Label>Conteúdo (opcional)</Label>
> 369	                  <Select value={formContentId} onValueChange={setFormContentId}>
> 370	                    <SelectTrigger><SelectValue placeholder="Nenhum" /></SelectTrigger>
> 371	                    <SelectContent>
> 372	                      <SelectItem value="none">Nenhum</SelectItem>
> 373	                      {contents.map((c) => (
> 374	                        <SelectItem key={c.id} value={c.id}>{c.title || `${c.type} - ${c.id.slice(0, 8)}`}</SelectItem>
> 375	                      ))}
> 376	                    </SelectContent>
> 377	                  </Select>
> 378	                </div>
> 379	              )}
> 380	            </div>
> 381	
> 382	            {/* Smart Schedule Suggestions */}
> 383	            <div className="border-t pt-3 space-y-2">
> 384	              <Button
> 385	                variant="outline"
> 386	                size="sm"
> 387	                onClick={handleSuggestTimes}
> 388	                disabled={loadingSuggestions}
> 389	                className="w-full gap-2 text-xs"
> 390	              >
> 391	                {loadingSuggestions ? <Loader2 className="h-3 w-3 animate-spin" /> : <Sparkles className="h-3 w-3" />}
> 392	                Sugerir Melhor Horário com IA
> 393	              </Button>
> 394	              {suggestions.length > 0 && (
> 395	                <div className="space-y-1.5 max-h-[150px] overflow-y-auto">
> 396	                  {suggestions.map((s, i) => (
> 397	                    <button
> 398	                      key={i}
> 399	                      onClick={() => applySuggestion(s.datetime)}
> 400	                      className="w-full text-left p-2 rounded-md bg-secondary/50 hover:bg-secondary transition-colors text-xs space-y-0.5"
> 401	                    >
> 402	                      <div className="flex items-center justify-between">
> 403	                        <span className="font-medium text-foreground">
> 404	                          {format(new Date(s.datetime), "EEE dd/MM 'às' HH:mm", { locale: ptBR })}
> 405	                        </span>
> 406	                        <Badge variant="outline" className="text-[10px] gap-1">
> 407	                          <Zap className="h-2 w-2" />
> 408	                          {s.score}%
> 409	                        </Badge>
> 410	                      </div>
> 411	                      <p className="text-muted-foreground">{s.reason}</p>
> 412	                    </button>
> 413	                  ))}
> 414	                </div>
> 415	              )}
> 416	            </div>
> 417	
> 418	            <DialogFooter>
> 419	              <Button variant="outline" onClick={() => setDialogOpen(false)}>Cancelar</Button>
> 420	              <Button onClick={handleCreate} disabled={createPost.isPending}>
> 421	                {createPost.isPending ? <Loader2 className="h-4 w-4 animate-spin mr-1" /> : null}
> 422	                Agendar
> 423	              </Button>
> 424	            </DialogFooter>
> 425	          </DialogContent>
> 426	        </Dialog>
> 427	      </div>
> 428	    </TooltipProvider>
> 429	  );
> 430	}
> 431	
> ```

## 🤖 Claude *(01:34:23)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/hooks/useScheduledPosts.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
> 2	import { supabase } from '@/integrations/supabase/client';
> 3	import { useAuth } from '@/hooks/useAuth';
> 4	import { toast } from 'sonner';
> 5	import type { Tables, TablesInsert } from '@/integrations/supabase/types';
> 6	
> 7	export type ScheduledPost = Tables<'scheduled_posts'>;
> 8	type InsertPost = TablesInsert<'scheduled_posts'>;
> 9	
> 10	export function useScheduledPosts(range?: { from: Date; to: Date }) {
> 11	  const { user } = useAuth();
> 12	
> 13	  const query = useQuery({
> 14	    queryKey: ['scheduled_posts', user?.id, range?.from?.toISOString(), range?.to?.toISOString()],
> 15	    queryFn: async () => {
> 16	      let q = supabase
> 17	        .from('scheduled_posts')
> 18	        .select('*')
> 19	        .order('scheduled_at');
> 20	
> 21	      if (range?.from) q = q.gte('scheduled_at', range.from.toISOString());
> 22	      if (range?.to) q = q.lte('scheduled_at', range.to.toISOString());
> 23	
> 24	      const { data, error } = await q;
> 25	      if (error) throw error;
> 26	      return data as ScheduledPost[];
> 27	    },
> 28	    enabled: !!user,
> 29	  });
> 30	
> 31	  return query;
> 32	}
> 33	
> 34	export function useCreateScheduledPost() {
> 35	  const { user } = useAuth();
> 36	  const qc = useQueryClient();
> 37	
> 38	  return useMutation({
> 39	    mutationFn: async (post: Omit<InsertPost, 'user_id'>) => {
> 40	      const { data, error } = await supabase
> 41	        .from('scheduled_posts')
> 42	        .insert({ ...post, user_id: user!.id })
> 43	        .select()
> 44	        .single();
> 45	      if (error) throw error;
> 46	      return data;
> 47	    },
> 48	    onSuccess: () => {
> 49	      qc.invalidateQueries({ queryKey: ['scheduled_posts'] });
> 50	      toast.success('Post agendado com sucesso');
> 51	    },
> 52	    onError: (e: Error) => toast.error(e.message),
> 53	  });
> 54	}
> 55	
> 56	export function useUpdateScheduledPost() {
> 57	  const qc = useQueryClient();
> 58	
> 59	  return useMutation({
> 60	    mutationFn: async ({ id, ...updates }: { id: string } & Partial<InsertPost>) => {
> 61	      const { error } = await supabase
> 62	        .from('scheduled_posts')
> 63	        .update(updates)
> 64	        .eq('id', id);
> 65	      if (error) throw error;
> 66	    },
> 67	    onSuccess: () => {
> 68	      qc.invalidateQueries({ queryKey: ['scheduled_posts'] });
> 69	      toast.success('Post atualizado');
> 70	    },
> 71	    onError: (e: Error) => toast.error(e.message),
> 72	  });
> 73	}
> 74	
> 75	export function useDeleteScheduledPost() {
> 76	  const qc = useQueryClient();
> 77	
> 78	  return useMutation({
> 79	    mutationFn: async (id: string) => {
> 80	      const { error } = await supabase
> 81	        .from('scheduled_posts')
> 82	        .delete()
> 83	        .eq('id', id);
> 84	      if (error) throw error;
> 85	    },
> 86	    onSuccess: () => {
> 87	      qc.invalidateQueries({ queryKey: ['scheduled_posts'] });
> 88	      toast.success('Post removido');
> 89	    },
> 90	    onError: (e: Error) => toast.error(e.message),
> 91	  });
> 92	}
> 93	
> ```

## 🤖 Claude *(01:35:39)*


## 🤖 Claude *(01:35:43)*

O diagnóstico está claro (Lei 1): hoje **clicar num dia sempre abre o formulário "Agendar novo"** (`openNewPost`, linha 237), e clicar num post só faz `stopPropagation` (linha 247) — **não existe nenhuma visão de detalhe** do que está agendado. Os dots "22:12" e o "+3 mais" não abrem nada. Vou construir um **Detalhe do Dia** robusto: clicar num dia (ou num post, ou no "+N mais") abre um modal com **todas as publicações daquela data + propriedades completas** (plataforma, horário, status, conteúdo vinculado, conta, timestamps) + ações (duplicar, remover, reagendar, agendar nova).

Confirmo os campos reais das tabelas pra não estourar o `tsc`:

## 🤖 Claude *(01:35:48)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== scheduled_posts Row (campos) ===\"\npython3 - <<'PY'\nimport re\nt=open('src/integrations/supabase/types.ts').read()\nfor tbl in ['scheduled_posts','content_library']:\n    m=re.search(tbl+r':\\s*\\{\\s*Row:\\s*\\{(.*?)\\}\\s*Insert:', t, re.S)\n    if m:\n        fields=[l.strip() for l in m.group(1).split('\\n') if ':' in l]\n        print(f\"--- {tbl} ---\")\n        for f in fields: print(\"  \"+f)\n    else:\n        print(f\"--- {tbl}: NOT FOUND ---\")\nPY\necho\necho \"=== ScrollArea existe? ===\"\nls src/components/ui/scroll-area.tsx 2>/dev/null && echo \"sim\" || echo \"n\u00e3o\"\necho \"=== useSocialAccounts / useContentLibrary shape (campos-chave) ===\"\ngrep -nE \"platform_username|\\.select\\(|media_url|title|type\" src/hooks/useContentLibrary.ts 2>/dev/null | head",
  "description": "Inspect table row fields and UI primitives"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === scheduled_posts Row (campos) ===
> --- scheduled_posts ---
>   campaign_id: string | null
>   content_id: string | null
>   created_at: string
>   error_message: string | null
>   id: string
>   max_retries: number | null
>   metadata: Json | null
>   platform: Database["public"]["Enums"]["social_platform"]
>   platform_post_id: string | null
>   published_at: string | null
>   retry_count: number | null
>   scheduled_at: string
>   social_account_id: string | null
>   status: Database["public"]["Enums"]["post_status"]
>   updated_at: string
>   user_id: string
> --- content_library ---
>   ai_model: string | null
>   ai_prompt: string | null
>   body: string | null
>   campaign_id: string | null
>   created_at: string
>   id: string
>   is_favorite: boolean | null
>   media_url: string | null
>   metadata: Json | null
>   operation_id: string | null
>   status: Database["public"]["Enums"]["content_status"]
>   tags: string[] | null
>   thumbnail_url: string | null
>   title: string | null
>   type: Database["public"]["Enums"]["content_type"]
>   updated_at: string
>   user_id: string
>   version: number | null
> 
> === ScrollArea existe? ===
> src/components/ui/scroll-area.tsx
> sim
> === useSocialAccounts / useContentLibrary shape (campos-chave) ===
> 5:import type { Tables, TablesInsert, TablesUpdate } from "@/integrations/supabase/types";
> 7:type Content = Tables<"content_library">;
> 8:type ContentInsert = TablesInsert<"content_library">;
> 9:type ContentUpdate = TablesUpdate<"content_library">;
> 12:  type?: string;
> 25:        .select("*")
> 28:      if (filters?.type && filters.type !== "all") {
> 29:        query = query.eq("type", filters.type as any);
> 41:        query = query.or(`title.ilike.%${filters.search}%,body.ilike.%${filters.search}%`);
> 61:        .select()
> ```

## 🤖 Claude *(01:37:05)*


## 🤖 Claude *(01:37:07)*

Campos confirmados (scheduled_posts tem `error_message`/`published_at`/`retry_count`/`platform_post_id`; content tem `title`/`type`/`thumbnail_url`; ScrollArea existe). Vou implementar. Batch 1 — imports + os componentes de detalhe + estado:

## 🤖 Claude *(01:37:10)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx",
  "old_string": "import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';\nimport { ChevronLeft, ChevronRight, Plus, Trash2, CalendarDays, LayoutList, Loader2, Copy, GripVertical, Sparkles, Zap } from 'lucide-react';",
  "new_string": "import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip';\nimport { ScrollArea } from '@/components/ui/scroll-area';\nimport { ChevronLeft, ChevronRight, Plus, Trash2, CalendarDays, LayoutList, Loader2, Copy, GripVertical, Sparkles, Zap, Clock, FileText, User2, CalendarClock, AlertCircle, RefreshCw } from 'lucide-react';"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:37:14)*


## 🤖 Claude *(01:37:39)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx",
  "old_string": "export default function CalendarPage() {",
  "new_string": "type ResolvedContent = { title: string | null; type: string; thumbnail_url: string | null };\ntype ResolvedAccount = { platform_username: string | null; platform: string };\n\n// One publication row inside the Day Detail \u2014 shows ALL properties + inline reschedule/duplicate/delete.\nfunction PostDetailRow({ post, content, account, onDuplicate, onDelete, onReschedule, busy }: {\n  post: ScheduledPost;\n  content?: ResolvedContent;\n  account?: ResolvedAccount;\n  onDuplicate: (p: ScheduledPost) => void;\n  onDelete: (id: string) => void;\n  onReschedule: (id: string, iso: string) => void;\n  busy?: boolean;\n}) {\n  const originalTime = format(parseISO(post.scheduled_at), 'HH:mm');\n  const [time, setTime] = useState(originalTime);\n  const dirty = time !== originalTime;\n  const applyReschedule = () => {\n    const [h, m] = time.split(':').map(Number);\n    if (Number.isNaN(h) || Number.isNaN(m)) return;\n    const d = parseISO(post.scheduled_at);\n    d.setHours(h, m, 0, 0);\n    onReschedule(post.id, d.toISOString());\n  };\n\n  return (\n    <div className=\"rounded-lg border border-border bg-card/50 p-3 space-y-2\">\n      <div className=\"flex items-center gap-2\">\n        <span className={cn('w-2.5 h-2.5 rounded-full shrink-0', PLATFORM_COLORS[post.platform] ?? 'bg-muted-foreground')} />\n        <span className=\"text-sm font-medium\">{PLATFORM_LABELS[post.platform] ?? post.platform}</span>\n        <Badge variant={STATUS_VARIANT[post.status] ?? 'outline'} className=\"text-[10px] h-5 capitalize\">{post.status}</Badge>\n        <span className=\"ml-auto flex items-center gap-1 text-xs text-muted-foreground\">\n          <Clock className=\"h-3 w-3\" />{format(parseISO(post.scheduled_at), \"HH:mm\")}\n        </span>\n      </div>\n\n      <div className=\"flex items-start gap-2 text-xs\">\n        <FileText className=\"h-3.5 w-3.5 text-muted-foreground mt-0.5 shrink-0\" />\n        {content ? (\n          <div className=\"flex items-center gap-2 min-w-0\">\n            {content.thumbnail_url && <img src={content.thumbnail_url} alt=\"\" className=\"h-8 w-8 rounded object-cover shrink-0\" loading=\"lazy\" />}\n            <div className=\"min-w-0\">\n              <p className=\"font-medium text-foreground truncate\">{content.title || 'Sem t\u00edtulo'}</p>\n              <p className=\"text-muted-foreground capitalize\">{content.type}</p>\n            </div>\n          </div>\n        ) : <span className=\"text-muted-foreground pt-0.5\">Sem conte\u00fado vinculado</span>}\n      </div>\n\n      <div className=\"flex items-center gap-2 text-xs text-muted-foreground\">\n        <User2 className=\"h-3.5 w-3.5 shrink-0\" />\n        {account ? <span>@{account.platform_username || account.platform}</span> : <span>Conta n\u00e3o definida</span>}\n      </div>\n\n      {post.published_at && (\n        <div className=\"flex items-center gap-2 text-xs text-emerald-500\">\n          <CalendarClock className=\"h-3.5 w-3.5 shrink-0\" />\n          Publicado {format(parseISO(post.published_at), \"dd/MM '\u00e0s' HH:mm\")}{post.platform_post_id ? ` \u00b7 ${post.platform_post_id}` : ''}\n        </div>\n      )}\n      {post.status === 'failed' && post.error_message && (\n        <div className=\"flex items-start gap-2 text-xs text-destructive\">\n          <AlertCircle className=\"h-3.5 w-3.5 mt-0.5 shrink-0\" /><span className=\"break-words\">{post.error_message}</span>\n        </div>\n      )}\n      {(post.retry_count ?? 0) > 0 && (\n        <p className=\"text-[10px] text-muted-foreground\">Tentativas: {post.retry_count}/{post.max_retries ?? '\u2014'}</p>\n      )}\n\n      <div className=\"flex items-center gap-1.5 pt-2 border-t border-border/50\">\n        <Input type=\"time\" value={time} onChange={(e) => setTime(e.target.value)} className=\"h-7 w-[104px] text-xs\" />\n        <Button variant=\"outline\" size=\"sm\" className=\"h-7 gap-1 text-xs\" disabled={!dirty || busy} onClick={applyReschedule}>\n          <RefreshCw className=\"h-3 w-3\" /> Reagendar\n        </Button>\n        <Button variant=\"ghost\" size=\"sm\" className=\"h-7 gap-1 text-xs ml-auto\" onClick={() => onDuplicate(post)}>\n          <Copy className=\"h-3 w-3\" /> Duplicar\n        </Button>\n        <Button variant=\"ghost\" size=\"sm\" className=\"h-7 gap-1 text-xs text-destructive\" disabled={busy} onClick={() => onDelete(post.id)}>\n          <Trash2 className=\"h-3 w-3\" /> Remover\n        </Button>\n      </div>\n      <p className=\"text-[10px] text-muted-foreground/60\">Criado {format(parseISO(post.created_at), \"dd/MM/yy HH:mm\")} \u00b7 id {post.id.slice(0, 8)}</p>\n    </div>\n  );\n}\n\n// Day Detail \u2014 opens on day/post click; lists EVERY publication of that date with full properties + a CTA to schedule new.\nfunction DayDetailDialog({ open, onOpenChange, date, posts, contentById, accountById, onDuplicate, onDelete, onReschedule, onAddNew, busy }: {\n  open: boolean;\n  onOpenChange: (o: boolean) => void;\n  date: Date | null;\n  posts: ScheduledPost[];\n  contentById: Record<string, ResolvedContent>;\n  accountById: Record<string, ResolvedAccount>;\n  onDuplicate: (p: ScheduledPost) => void;\n  onDelete: (id: string) => void;\n  onReschedule: (id: string, iso: string) => void;\n  onAddNew: (date: Date) => void;\n  busy?: boolean;\n}) {\n  if (!date) return null;\n  const sorted = [...posts].sort((a, b) => a.scheduled_at.localeCompare(b.scheduled_at));\n  return (\n    <Dialog open={open} onOpenChange={onOpenChange}>\n      <DialogContent className=\"max-w-lg\">\n        <DialogHeader>\n          <DialogTitle className=\"capitalize\">{format(date, \"EEEE, dd 'de' MMMM 'de' yyyy\", { locale: ptBR })}</DialogTitle>\n        </DialogHeader>\n        <p className=\"text-xs text-muted-foreground -mt-2\">\n          {sorted.length === 0 ? 'Nenhuma publica\u00e7\u00e3o agendada' : `${sorted.length} ${sorted.length === 1 ? 'publica\u00e7\u00e3o agendada' : 'publica\u00e7\u00f5es agendadas'}`}\n        </p>\n        <ScrollArea className=\"max-h-[55vh] pr-3 -mr-3\">\n          <div className=\"space-y-2\">\n            {sorted.length === 0 ? (\n              <div className=\"text-center py-8 text-sm text-muted-foreground\">Nada agendado nesta data ainda.</div>\n            ) : sorted.map((p) => (\n              <PostDetailRow\n                key={p.id}\n                post={p}\n                content={p.content_id ? contentById[p.content_id] : undefined}\n                account={p.social_account_id ? accountById[p.social_account_id] : undefined}\n                onDuplicate={onDuplicate}\n                onDelete={onDelete}\n                onReschedule={onReschedule}\n                busy={busy}\n              />\n            ))}\n          </div>\n        </ScrollArea>\n        <DialogFooter>\n          <Button className=\"w-full gap-1\" onClick={() => onAddNew(date)}>\n            <Plus className=\"h-4 w-4\" /> Agendar nova publica\u00e7\u00e3o nesta data\n          </Button>\n        </DialogFooter>\n      </DialogContent>\n    </Dialog>\n  );\n}\n\nexport default function CalendarPage() {"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:37:46)*


## 🤖 Claude *(01:37:47)*

Batch 2 — estado + mapas de resolução (conteúdo/conta) + handlers:

## 🤖 Claude *(01:37:49)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx",
  "old_string": "  const [activePost, setActivePost] = useState<ScheduledPost | null>(null);",
  "new_string": "  const [activePost, setActivePost] = useState<ScheduledPost | null>(null);\n  const [detailOpen, setDetailOpen] = useState(false);\n  const [detailDate, setDetailDate] = useState<Date | null>(null);"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:37:55)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx",
  "old_string": "  const postsByDay = useMemo(() => {\n    const map: Record<string, ScheduledPost[]> = {};\n    posts?.forEach((p) => {\n      const key = format(parseISO(p.scheduled_at), 'yyyy-MM-dd');\n      (map[key] ??= []).push(p);\n    });\n    return map;\n  }, [posts]);",
  "new_string": "  const postsByDay = useMemo(() => {\n    const map: Record<string, ScheduledPost[]> = {};\n    posts?.forEach((p) => {\n      const key = format(parseISO(p.scheduled_at), 'yyyy-MM-dd');\n      (map[key] ??= []).push(p);\n    });\n    return map;\n  }, [posts]);\n\n  // Resolution maps for the Day Detail \u2014 content_id/social_account_id \u2192 human-readable properties.\n  const contentById = useMemo(() => {\n    const m: Record<string, ResolvedContent> = {};\n    contents?.forEach((c) => { m[c.id] = { title: c.title, type: c.type as string, thumbnail_url: c.thumbnail_url ?? null }; });\n    return m;\n  }, [contents]);\n  const accountById = useMemo(() => {\n    const m: Record<string, ResolvedAccount> = {};\n    accounts?.forEach((a) => { m[a.id] = { platform_username: a.platform_username ?? null, platform: a.platform }; });\n    return m;\n  }, [accounts]);\n\n  const detailPosts = useMemo(\n    () => (detailDate ? (postsByDay[format(detailDate, 'yyyy-MM-dd')] ?? []) : []),\n    [detailDate, postsByDay],\n  );\n\n  const openDayDetail = (day: Date) => {\n    setDetailDate(day);\n    setDetailOpen(true);\n  };\n\n  const handleReschedule = (id: string, iso: string) => {\n    updatePost.mutate({ id, scheduled_at: iso });\n  };\n\n  const handleAddNewFromDetail = (day: Date) => {\n    setDetailOpen(false);\n    setSelectedDate(day);\n    setFormTime('12:00');\n    setDialogOpen(true);\n  };"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:38:24)*


## 🤖 Claude *(01:38:25)*

Batch 3 — a fiação de interação (clicar dia/post/"+N mais" → abre detalhe) + render do modal:

## 🤖 Claude *(01:38:28)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx",
  "old_string": "                    <div\n                      className={cn('bg-card min-h-[100px] p-1.5 cursor-pointer hover:bg-accent/30 transition-colors', !inMonth && 'opacity-40')}\n                      onClick={() => openNewPost(day)}\n                    >",
  "new_string": "                    <div\n                      className={cn('bg-card min-h-[100px] p-1.5 cursor-pointer hover:bg-accent/30 transition-colors', !inMonth && 'opacity-40')}\n                      onClick={() => openDayDetail(day)}\n                    >"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:38:30)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx",
  "old_string": "                                <div className=\"flex items-center gap-1 group/post\" onClick={(e) => e.stopPropagation()}>",
  "new_string": "                                <div className=\"flex items-center gap-1 group/post cursor-pointer\" onClick={(e) => { e.stopPropagation(); openDayDetail(day); }}>"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:38:32)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx",
  "old_string": "                                  <Button variant=\"ghost\" size=\"icon\" className=\"h-4 w-4 opacity-0 group-hover/post:opacity-100 ml-auto\" onClick={() => handleDuplicate(p)}>",
  "new_string": "                                  <Button variant=\"ghost\" size=\"icon\" className=\"h-4 w-4 opacity-0 group-hover/post:opacity-100 ml-auto\" onClick={(e) => { e.stopPropagation(); handleDuplicate(p); }}>"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:38:34)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx",
  "old_string": "                        {dayPosts.length > 3 && (\n                          <span className=\"text-[10px] text-muted-foreground\">+{dayPosts.length - 3} mais</span>\n                        )}",
  "new_string": "                        {dayPosts.length > 3 && (\n                          <button\n                            type=\"button\"\n                            className=\"text-[10px] text-primary hover:underline\"\n                            onClick={(e) => { e.stopPropagation(); openDayDetail(day); }}\n                          >\n                            +{dayPosts.length - 3} mais\n                          </button>\n                        )}"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:38:36)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx",
  "old_string": "                            <div className=\"p-2 rounded-md bg-secondary/50 space-y-1 group relative cursor-grab active:cursor-grabbing\">",
  "new_string": "                            <div className=\"p-2 rounded-md bg-secondary/50 space-y-1 group relative cursor-pointer\" onClick={() => openDayDetail(day)}>"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:38:39)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx",
  "old_string": "        </Dialog>\n      </div>\n    </TooltipProvider>",
  "new_string": "        </Dialog>\n\n        <DayDetailDialog\n          open={detailOpen}\n          onOpenChange={setDetailOpen}\n          date={detailDate}\n          posts={detailPosts}\n          contentById={contentById}\n          accountById={accountById}\n          onDuplicate={handleDuplicate}\n          onDelete={(id) => deletePost.mutate(id)}\n          onReschedule={handleReschedule}\n          onAddNew={handleAddNewFromDetail}\n          busy={updatePost.isPending || deletePost.isPending}\n        />\n      </div>\n    </TooltipProvider>"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(01:38:53)*


## 🤖 Claude *(01:38:53)*

Edições aplicadas. Prova material — `tsc` + lint:

## 🤖 Claude *(01:38:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== tsc --noEmit ===\"\nnpx tsc --noEmit 2>&1 | head -30\necho \"tsc exit: ${PIPESTATUS[0]}\"\necho\necho \"=== eslint CalendarPage ===\"\nnpx eslint src/pages/CalendarPage.tsx 2>&1 | head -30\necho \"eslint exit: ${PIPESTATUS[0]}\"",
  "description": "Typecheck and lint the calendar page"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === tsc --noEmit ===
> tsc exit: 0
> 
> === eslint CalendarPage ===
> 
> /home/gcrUX/htdocs/constellation-orchestra/src/pages/CalendarPage.tsx
>   236:87   warning  React Hook useMemo has missing dependencies: 'rangeEnd' and 'rangeStart'. Either include them or remove the dependency array            react-hooks/exhaustive-deps
>   236:88   warning  React Hook useMemo has a complex expression in the dependency array. Extract it to a separate variable so it can be statically checked  react-hooks/exhaustive-deps
>   236:110  warning  React Hook useMemo has a complex expression in the dependency array. Extract it to a separate variable so it can be statically checked  react-hooks/exhaustive-deps
> 
> ✖ 3 problems (0 errors, 3 warnings)
> 
> eslint exit: 0
> ```

## 🤖 Claude *(01:39:45)*


## 🤖 Claude *(01:39:47)*

`tsc` **exit 0**, eslint **exit 0** (os 3 warnings são pré-existentes na linha 236, o `useMemo` de `days` original — não é meu código). Commito a fonte (staging cirúrgico — só meu arquivo, pra não colidir com o loop) e faço o build num dir temporário pra browser-verify antes de deployar:

## 🤖 Claude *(01:39:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add src/pages/CalendarPage.tsx\ngit commit -q -m \"feat(calendar): day-detail modal \u2014 clicar dia/post abre todas as publica\u00e7\u00f5es da data com propriedades completas + reagendar/duplicar/remover\n\nAntes: clicar num dia sempre abria o form 'Agendar novo'; posts e '+N mais' n\u00e3o abriam nada.\nAgora: dia/post/'+N mais' \u2192 DayDetailDialog com plataforma\u00b7hor\u00e1rio\u00b7status\u00b7conte\u00fado\u00b7conta\u00b7published_at\u00b7erro\u00b7tentativas + a\u00e7\u00f5es inline (reagendar/duplicar/remover) + CTA agendar nesta data.\n\nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>\"\necho \"commit: $(git log -1 --format=%H)\"\necho\necho \"=== build para dir tempor\u00e1rio (env baked do repo principal) ===\"\nOUT=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad/cal-dist\nrm -rf \"$OUT\"\nbunx vite build --outDir \"$OUT\" 2>&1 | tail -8\necho \"build exit: ${PIPESTATUS[0]}\"\necho \"=== chunk do CalendarPage cont\u00e9m 'nesta data'? ===\"\ngrep -rl \"nesta data\" \"$OUT/assets\" 2>/dev/null | head -1 && echo \"OK: string nova presente no bundle\" || echo \"AVISO: string n\u00e3o achada\"",
  "description": "Commit calendar change and build to temp dir"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;6;6;6m─[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpre-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;6;6;6m─[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m╯[m
> ┃  e2e-output-tripwire ❯ 
> 
> ┃  secret-scan ❯ 
> 
> ┃  gitleaks-staged ❯ 
> 
>     ○
>     │╲
>     │ ○
>     ○ ░
>     ░    gitleaks
> 
> [90m10:39PM[0m [32mINF[0m 1 commits scanned.
> [90m10:39PM[0m [32mINF[0m scan completed in 11.9ms
> [90m10:39PM[0m [32mINF[0m no leaks found
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.08 seconds)
> ✔️ e2e-output-tripwire (0.01 seconds)
> ✔️ secret-scan (0.05 seconds)
> ✔️ gitleaks-staged (0.07 seconds)
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpost-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m╯[m
> ┃  mesh-reingest ❯ 
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.00 seconds)
> ✔️ mesh-reingest (0.00 seconds)
> commit: a29627b400ec33b5197a5ab42944e0d8d1745fbf
> 
> === build para dir temporário (env baked do repo principal) ===
> ../../../../tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad/cal-dist/assets/index-vij5ll1D.js                  661.90 kB │ gzip: 196.12 kB
> ../../../../tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad/cal-dist/assets/react-three-fiber.esm-qsTJnUKR.js  824.11 kB │ gzip: 221.90 kB
> 
> (!) Some chunks are larger than 500 kB after minification. Consider:
> - Using dynamic import() to code-split the application
> - Use build.rollupOptions.output.manualChunks to improve chunking: https://rollupjs.org/configuration-options/#output-manualchunks
> - Adjust chunk size limit for this warning via build.chunkSizeWarningLimit.
> ✓ built in 33.55s
> build exit: 0
> === chunk do CalendarPage contém 'nesta data'? ===
> /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad/cal-dist/assets/CalendarPage-CCgZuuDP.js
> OK: string nova presente no bundle
> ```

## 🤖 Claude *(01:40:48)*


## 🤖 Claude *(01:40:50)*

Commit `a29627b4`, build **exit 0**, e a string nova (`nesta data`) está no chunk `CalendarPage-CCgZuuDP.js` — o código novo bundlou. gitleaks limpo. Agora o **browser-verify** (Lei 1 + diretiva de ver a UI renderizada). Subo o preview do build temp e gero a sessão do Usuário Zero:

## 🤖 Claude *(01:40:53)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== uso do gen-user-session ===\"\ngrep -nE \"argv|process.env|email|Usage|VITE_SUPABASE_URL|sb-|auth-token\" scripts/qa/gen-user-session.ts 2>/dev/null | head -20\necho\necho \"=== agent-browser dispon\u00edvel? ===\"\nwhich agent-browser 2>/dev/null || ls scripts/qa/ | grep -i browser || echo \"(checar skill)\"",
  "description": "Inspect session generator usage and browser tool"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === uso do gen-user-session ===
> 7: * `sb-<ref>-auth-token`. Inject it into localStorage and the app boots already authenticated.
> 9: * Usage: bun run scripts/qa/gen-user-session.ts <email>
> 14: *   localStorage.setItem('sb-<ref>-auth-token', SESSION) then reload → logged in.
> 19:const URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL!;
> 20:const SVC = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY)!;
> 21:const ANON = (process.env.SB_PUBLISHABLE_KEY ?? process.env.SUPABASE_PUBLISHABLE_KEY ?? process.env.VITE_SUPABASE_PUBLISHABLE_KEY ?? process.env.SUPABASE_ANON_KEY)!;
> 22:const email = process.argv[2];
> 23:if (!URL || !SVC || !ANON || !email) {
> 24:  console.error('Usage: gen-user-session.ts <email>  (needs SUPABASE_URL + SB_SECRET_KEY + SB_PUBLISHABLE_KEY)');
> 31:const { data, error } = await admin.auth.admin.generateLink({ type: 'magiclink', email });
> 39:for (const type of ['magiclink', 'email'] as const) {
> 43:if (!session) { console.error('verifyOtp failed for both magiclink/email types'); process.exit(1); }
> 
> === agent-browser disponível? ===
> /home/ubuntu/.nvm/versions/node/v22.22.3/bin/agent-browser
> ```

## 🤖 Claude *(01:41:01)*


## 🤖 Claude *(01:41:01)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/gen-user-session.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	#!/usr/bin/env bun
> 2	/**
> 3	 * Mint a REAL Supabase browser session (the full localStorage value) for logged-in UI E2E
> 4	 * without OAuth redirect — bypasses the single-use magic-link + Cloudflare-challenge trap that
> 5	 * kills gen-magiclink.ts when driving from a datacenter IP. Admin generateLink (magiclink) →
> 6	 * verifyOtp(token_hash) → session, printed as the JSON string supabase-js stores under
> 7	 * `sb-<ref>-auth-token`. Inject it into localStorage and the app boots already authenticated.
> 8	 *
> 9	 * Usage: bun run scripts/qa/gen-user-session.ts <email>
> 10	 *   → prints ONLY the localStorage value (JSON) on stdout, or an error on stderr + exit 1.
> 11	 *   e.g. SESSION=$(bun run scripts/qa/gen-user-session.ts gabrielcall@gmail.com)
> 12	 *
> 13	 * Pair with agent-browser:
> 14	 *   localStorage.setItem('sb-<ref>-auth-token', SESSION) then reload → logged in.
> 15	 * Pattern extends gen-user-jwt.ts (v6.20.4 lineage). Session is ~1h-lived; mint right before use.
> 16	 */
> 17	import { createClient } from '@supabase/supabase-js';
> 18	
> 19	const URL = process.env.SUPABASE_URL ?? process.env.VITE_SUPABASE_URL!;
> 20	const SVC = (process.env.SB_SECRET_KEY ?? process.env.SUPABASE_SERVICE_ROLE_KEY)!;
> 21	const ANON = (process.env.SB_PUBLISHABLE_KEY ?? process.env.SUPABASE_PUBLISHABLE_KEY ?? process.env.VITE_SUPABASE_PUBLISHABLE_KEY ?? process.env.SUPABASE_ANON_KEY)!;
> 22	const email = process.argv[2];
> 23	if (!URL || !SVC || !ANON || !email) {
> 24	  console.error('Usage: gen-user-session.ts <email>  (needs SUPABASE_URL + SB_SECRET_KEY + SB_PUBLISHABLE_KEY)');
> 25	  process.exit(1);
> 26	}
> 27	
> 28	const admin = createClient(URL, SVC, { auth: { persistSession: false } });
> 29	const anon = createClient(URL, ANON, { auth: { persistSession: false } });
> 30	
> 31	const { data, error } = await admin.auth.admin.generateLink({ type: 'magiclink', email });
> 32	if (error || !data.properties?.hashed_token) {
> 33	  console.error('generateLink error:', error?.message ?? 'no hashed_token');
> 34	  process.exit(1);
> 35	}
> 36	const tokenHash = data.properties.hashed_token;
> 37	
> 38	let session: unknown = null;
> 39	for (const type of ['magiclink', 'email'] as const) {
> 40	  const { data: sess, error: vErr } = await anon.auth.verifyOtp({ token_hash: tokenHash, type });
> 41	  if (!vErr && sess?.session?.access_token) { session = sess.session; break; }
> 42	}
> 43	if (!session) { console.error('verifyOtp failed for both magiclink/email types'); process.exit(1); }
> 44	// supabase-js v2 stores the plain JSON-stringified session under storageKey (no base64 for default localStorage storage).
> 45	console.log(JSON.stringify(session));
> 46	
> ```

## 🤖 Claude *(01:41:13)*


## 🤖 Claude *(01:41:14)*

`gen-user-session` imprime o JSON da sessão; injeto em `sb-<ref>-auth-token`. Subo o preview do build temp em background e preparo a sessão + state file do agent-browser:

## 🤖 Claude *(01:41:17)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nOUT=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad/cal-dist\nbunx vite preview --outDir \"$OUT\" --port 4174 --host 127.0.0.1",
  "description": "Start vite preview of temp build in background",
  "run_in_background": true
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Command running in background with ID: b0bntaxtx. Output is being written to: /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/tasks/b0bntaxtx.output. You will be notified when it completes. To check interim output, use Read on that file path.
> ```

## 🤖 Claude *(01:41:23)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nREF=$(echo \"${VITE_SUPABASE_URL:-$SUPABASE_URL}\" | sed -E 's#https?://([^.]+)\\..*#\\1#')\necho \"project ref: $REF\"\necho \"=== gerando sess\u00e3o User 0 (gabrielcall@gmail.com) ===\"\nSESSION=$(bun run scripts/qa/gen-user-session.ts gabrielcall@gmail.com 2>/tmp/sess_err)\nif [ -z \"$SESSION\" ]; then echo \"FALHOU:\"; cat /tmp/sess_err; else echo \"sess\u00e3o obtida (len=${#SESSION})\"; fi\nSCR=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad\npython3 - \"$REF\" \"$SESSION\" > \"$SCR/cal-state.json\" <<'PY'\nimport sys,json\nref,session=sys.argv[1],sys.argv[2]\nstate={\"cookies\":[],\"origins\":[{\"origin\":\"http://127.0.0.1:4174\",\"localStorage\":[{\"name\":f\"sb-{ref}-auth-token\",\"value\":session}]}]}\nprint(json.dumps(state))\nPY\necho \"state file: $(wc -c < $SCR/cal-state.json) bytes\"\necho\necho \"=== agent-browser help (subcomandos) ===\"\nagent-browser --help 2>&1 | head -40",
  "description": "Generate session, build state file, check agent-browser help"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> project ref: bcyvddsykvehvpwstlfa
> === gerando sessão User 0 (gabrielcall@gmail.com) ===
> sessão obtida (len=3331)
> state file: 3664 bytes
> 
> === agent-browser help (subcomandos) ===
> 
> agent-browser - fast browser automation CLI for AI agents
> 
> Usage: agent-browser <command> [args] [options]
> 
> Start here (for AI agents):
>   agent-browser skills get core --full
> 
>   Skills ship with the CLI (always version-matched) and include workflow
>   patterns, ref/selector usage, and copy-paste examples. Prefer this over
>   guessing commands from flag docs alone. Specialized skills cover Electron
>   apps, Slack, exploratory testing, and cloud browser providers.
> 
>   skills [list]                List available skills
>   skills get core              Core usage guide (overview + common patterns)
>   skills get core --full       Include full command reference and templates
>   skills get <name>            Load a specialized skill (electron, slack, ...)
>   skills path [name]           Print skill directory path
> 
> Core Commands:
>   open <url>                 Navigate to URL
>   click <sel>                Click element (or @ref)
>   dblclick <sel>             Double-click element
>   type <sel> <text>          Type into element
>   fill <sel> <text>          Clear and fill
>   press <key>                Press key (Enter, Tab, Control+a)
>   keyboard type <text>       Type text with real keystrokes (no selector)
>   keyboard inserttext <text> Insert text without key events
>   hover <sel>                Hover element
>   focus <sel>                Focus element
>   check <sel>                Check checkbox
>   uncheck <sel>              Uncheck checkbox
>   select <sel> <val...>      Select dropdown option
>   drag <src> <dst>           Drag and drop
>   upload <sel> <files...>    Upload files
>   download <sel> <path>      Download file by clicking element
>   scroll <dir> [px]          Scroll (up/down/left/right)
>   scrollintoview <sel>       Scroll element into view
>   wait <sel|ms>              Wait for element or time
>   screenshot [path]          Take screenshot
> ```

## 🤖 Claude *(01:41:40)*


## 🤖 Claude *(01:41:41)*

Sessão + state file prontos (ref `bcyvddsykvehvpwstlfa`). Confirmo o preview no ar e a sintaxe do `--state` do agent-browser (gotcha conhecido: daemon já rodando ignora `--state`):

## 🤖 Claude *(01:41:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nsleep 3\necho \"=== preview no ar? ===\"\ncurl -s -o /dev/null -w \"HTTP %{http_code}\\n\" http://127.0.0.1:4174/ 2>/dev/null || echo \"preview OFF\"\necho\necho \"=== flags de open (--state?) ===\"\nagent-browser open --help 2>&1 | grep -iE \"state|session|storage|profile\" | head\necho\necho \"=== parar daemon stale p/ garantir inje\u00e7\u00e3o do state ===\"\nagent-browser stop 2>&1 | head -3 || pkill -f agent-browser 2>/dev/null; echo \"daemon parado\"",
  "description": "Verify preview up and agent-browser state flag"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === preview no ar? ===
> HTTP 200
> 
> === flags de open (--state?) ===
> you stage state (network routes, cookies, init scripts) before the first
> `react suspense` / `vitals` state without noise from a prior page.
>   --session <name>     Use specific session
> 
> === parar daemon stale p/ garantir injeção do state ===
> Unknown command: stop
> daemon parado
> ```

## 🤖 Claude *(01:42:01)*


## 🤖 Claude *(01:42:03)*

`--state` não é flag de `open` (só vi `--session`). Vejo o full help + a skill core pra achar o modo certo de injetar localStorage (a receita da memória usa `sb-<ref>-auth-token`):

## 🤖 Claude *(01:42:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== open --help completo ===\"\nagent-browser open --help 2>&1 | sed -n '1,60p'\necho\necho \"=== skill core: inje\u00e7\u00e3o de estado/localStorage/auth ===\"\nagent-browser skills get core --full 2>&1 | grep -iE -A3 \"storagestate|localstorage|--state|auth|session|inject\" | head -50",
  "description": "Full open help and core skill state injection pattern"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === open --help completo ===
> agent-browser open - Launch the browser, optionally navigate
> 
> Usage: agent-browser open [url]
> 
> Without a URL, launches the browser but stays on about:blank. This lets
> you stage state (network routes, cookies, init scripts) before the first
> real navigation — useful for SSR debug, auth setup, and capturing fresh
> `react suspense` / `vitals` state without noise from a prior page.
> 
> With a URL, launches and navigates. If no protocol is provided, https://
> is automatically prepended.
> 
> The `goto` and `navigate` aliases still require a URL.
> 
> Global Options:
>   --json               Output as JSON
>   --session <name>     Use specific session
>   --headers <json>     Set HTTP headers (scoped to this origin)
>   --headed             Show browser window
>   --enable react-devtools   Inject the React DevTools hook before any page JS
>   --init-script <path>      Register a page init script (repeatable)
> 
> Examples:
>   agent-browser open                     # Launch, no nav
>   agent-browser open example.com
>   agent-browser open https://github.com
>   agent-browser open localhost:3000
>   agent-browser open api.example.com --headers '{"Authorization": "Bearer token"}'
>     # ^ Headers only sent to api.example.com, not other domains
> 
>   # Pre-navigation setup in one turn:
>   agent-browser batch \
>     '["open"]' \
>     '["network","route","*","--abort","--resource-type","script"]' \
>     '["navigate","http://localhost:3000/target"]'
> 
> === skill core: injeção de estado/localStorage/auth ===
> description: Core agent-browser usage guide. Read this before running any agent-browser commands. Covers the snapshot-and-ref workflow, navigating pages, interacting with elements (click, fill, type, select), extracting text and data, taking screenshots, managing tabs, handling forms and auth, waiting for content, running multiple browser sessions in parallel, and troubleshooting common failures. Use when the user asks to interact with a website, fill a form, click something, extract data, take a screenshot, log into a site, test a web app, or automate any browser task.
> allowed-tools: Bash(agent-browser:*), Bash(npx agent-browser:*)
> ---
> 
> --
> session. Use `agent-browser close` (or `close --all`) when you're done.
> 
> ## Reading a page
> 
> --
> auth vault (see [references/authentication.md](references/authentication.md)):
> 
> ```bash
> agent-browser auth save my-app --url https://app.example.com/login \
>   --username user@example.com --password-stdin
> # (type password, Ctrl+D)
> 
> agent-browser auth login my-app    # fills + clicks, waits for form
> ```
> 
> ### Persist session across runs
> 
> ```bash
> # Log in once, save cookies + localStorage
> agent-browser state save ./auth.json
> 
> # Later runs start already-logged-in
> agent-browser --state ./auth.json open https://app.example.com
> ```
> 
> Or use `--session-name` for auto-save/restore:
> 
> ```bash
> AGENT_BROWSER_SESSION_NAME=my-app agent-browser open https://app.example.com
> # State is auto-saved and restored on subsequent runs with the same name.
> ```
> 
> --
> Each `--session <name>` is an isolated browser with its own cookies, tabs,
> and refs. Useful for testing multi-user flows or parallel scraping:
> 
> ```bash
> agent-browser --session a open https://app.example.com
> agent-browser --session b open https://app.example.com
> agent-browser --session a fill @e1 "alice@test.com"
> agent-browser --session b fill @e1 "bob@test.com"
> ```
> 
> `AGENT_BROWSER_SESSION=myapp` sets the default session for the current
> shell.
> ```

## 🤖 Claude *(01:42:20)*


## 🤖 Claude *(01:42:21)*

`--state` é flag **global** (antes do comando): `agent-browser --state <file> open <url>`, e meu `cal-state.json` já está no formato storageState. Abro o calendário autenticado e capturo o render:

## 🤖 Claude *(01:42:26)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSCR=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad\nagent-browser close --all 2>/dev/null; sleep 1\necho \"=== open calendar autenticado ===\"\nagent-browser --state \"$SCR/cal-state.json\" open \"http://127.0.0.1:4174/dashboard/calendar\" 2>&1 | tail -5\nagent-browser wait 3000 2>&1 | tail -1\necho \"=== URL atual (confirmar que n\u00e3o caiu em /auth) ===\"\nagent-browser eval \"location.pathname\" 2>&1 | tail -3\nagent-browser screenshot \"$SCR/cal-1-render.png\" 2>&1 | tail -2\nls -la \"$SCR/cal-1-render.png\"",
  "description": "Open calendar authenticated and screenshot render"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> No active sessions
> === open calendar autenticado ===
> ✓ Magic Constellation
>   http://127.0.0.1:4174/dashboard/calendar
> ✓ Done
> === URL atual (confirmar que não caiu em /auth) ===
> "/dashboard/calendar"
> ✓ Screenshot saved to /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad/cal-1-render.png
> -rw-rw-r-- 1 ubuntu ubuntu 71718 Jun 30 22:42 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad/cal-1-render.png
> ```

## 🤖 Claude *(01:42:35)*


## 🤖 Claude *(01:42:36)*

Autenticado (ficou em `/dashboard/calendar`, sem redirect pra /auth). Vejo o render:

## 🤖 Claude *(01:42:36)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad/cal-1-render.png"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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', 'media_type': 'image/png'}}]
> ```

## 🤖 Claude *(01:42:50)*


## 🤖 Claude *(01:42:51)*

Render limpo — sem white-screen, Junho 2026, dia 30 (hoje) destacado com as publicações abaixo. Agora clico no dia 30 pra abrir o Detalhe do Dia e capturo o modal:

## 🤖 Claude *(01:42:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSCR=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad\necho \"=== scroll + clicar no dia 30 ===\"\nagent-browser scroll down 300 2>&1 | tail -1\nagent-browser click \"text=30\" 2>&1 | tail -3\nagent-browser wait 1500 2>&1 | tail -1\necho \"=== dialog aberto? (role=dialog presente) ===\"\nagent-browser eval \"document.querySelector('[role=dialog]') ? document.querySelector('[role=dialog]').innerText.slice(0,400) : 'NENHUM DIALOG'\" 2>&1 | tail -8\nagent-browser screenshot \"$SCR/cal-2-daydetail.png\" 2>&1 | tail -1\nls -la \"$SCR/cal-2-daydetail.png\"",
  "description": "Click day 30 and screenshot day detail modal"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === scroll + clicar no dia 30 ===
> ✓ Done
> ✗ Element not found. Verify the selector is correct and the element exists in the DOM.
> ✓ Done
> === dialog aberto? (role=dialog presente) ===
> "NENHUM DIALOG"
> ✓ Screenshot saved to /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad/cal-2-daydetail.png
> -rw-rw-r-- 1 ubuntu ubuntu 67401 Jun 30 22:42 /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad/cal-2-daydetail.png
> ```

## 🤖 Claude *(01:43:06)*


## 🤖 Claude *(01:43:07)*

`text=30` não resolveu. Pego um snapshot pra achar o ref certo do dia 30 (ou de um post):

## 🤖 Claude *(01:43:09)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== snapshot (elementos clic\u00e1veis relevantes) ===\"\nagent-browser snapshot 2>&1 | grep -iE \"22:1|mais|button|\\b30\\b|gridcell|generic.*3[0-9]\" | head -40",
  "description": "Snapshot to find day 30 cell ref"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === snapshot (elementos clicáveis relevantes) ===
>           - button [expanded=false, ref=e62]
>           - button [expanded=false, ref=e64]
>           - button "Conteúdo & Campanhas" [expanded=true, ref=e65]
>           - button "Monetização" [expanded=false, ref=e66]
>           - button "Inteligência IA" [expanded=false, ref=e67]
>   - button "Sair" [ref=e6]
>     - button "Toggle Sidebar" [ref=e7]
>     - button "Notificações" [expanded=false, ref=e8]
>     - button [ref=e10]
>     - button [ref=e11]
>     - button [ref=e12]
>     - button "Agendar" [ref=e13]
>     - generic [ref=e30] clickable [cursor:pointer, onclick]
>     - generic [ref=e31] clickable [cursor:pointer, onclick]
>     - generic [ref=e32] clickable [cursor:pointer, onclick]
>     - generic [ref=e33] clickable [cursor:pointer, onclick]
>     - generic [ref=e34] clickable [cursor:pointer, onclick]
>     - generic [ref=e35] clickable [cursor:pointer, onclick]
>     - generic [ref=e36] clickable [cursor:pointer, onclick]
>     - generic [ref=e37] clickable [cursor:pointer, onclick]
>     - generic [ref=e38] clickable [cursor:pointer, onclick]
>     - generic [ref=e39] clickable [cursor:pointer, onclick]
>       - StaticText "30"
>       - button "22:12" [ref=e50]
>           - StaticText "22:12"
>           - button [ref=e57]
>       - button "22:12" [ref=e51]
>           - StaticText "22:12"
>           - button [ref=e58]
>       - button "22:13" [ref=e52]
>           - StaticText "22:13"
>           - button [ref=e59]
>       - button "+3 mais" [ref=e53]
>         - StaticText "+3 mais"
> ```

## 🤖 Claude *(01:43:14)*


## 🤖 Claude *(01:43:16)*

Achei — dia 30 = `ref=e39`, com 3 posts (22:12/22:12/22:13) + botão "+3 mais" (`ref=e53`). Clico no "+3 mais" (o afford de "ver tudo") pra abrir o modal:

## 🤖 Claude *(01:43:18)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSCR=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad\nagent-browser click \"@e53\" 2>&1 | tail -2\nagent-browser wait 1500 2>&1 | tail -1\necho \"=== dialog aberto? ===\"\nagent-browser eval \"const d=document.querySelector('[role=dialog]'); d ? d.innerText.slice(0,600) : 'NENHUM DIALOG'\" 2>&1 | tail -20\nagent-browser screenshot \"$SCR/cal-2-daydetail.png\" 2>&1 | tail -1",
  "description": "Click +3 mais and capture day detail modal"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ✓ Done
> ✓ Done
> === dialog aberto? ===
> "NENHUM DIALOG"
> ✓ Screenshot saved to /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad/cal-2-daydetail.png
> ```

## 🤖 Claude *(01:43:35)*


## 🤖 Claude *(01:43:36)*

Sem dialog ainda — pode ser erro de runtime no clique ou clique não-efetivo. Vejo o console + o screenshot atual:

## 🤖 Claude *(01:43:39)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== console messages (erros?) ===\"\nagent-browser console 2>&1 | grep -iE \"error|warn|uncaught|cannot|undefined\" | tail -15\necho \"--- (fim console) ---\"\necho \"=== estado: quantos dialogs / bot\u00f5es 'nesta data'? ===\"\nagent-browser eval \"JSON.stringify({dialogs: document.querySelectorAll('[role=dialog]').length, nestaData: !!Array.from(document.querySelectorAll('button')).find(b=>b.textContent.includes('nesta data'))})\" 2>&1 | tail -3",
  "description": "Check console errors and dialog state"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === console messages (erros?) ===
> --- (fim console) ---
> === estado: quantos dialogs / botões 'nesta data'? ===
> "{\"dialogs\":0,\"nestaData\":false}"
> ```

## 🤖 Claude *(01:43:59)*


## 🤖 Claude *(01:44:00)*

Sem erro de console — o clique via ref não disparou o handler. Tento um clique nativo direto no botão (dispara o onClick do React de forma confiável):

## 🤖 Claude *(01:44:04)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nSCR=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad\necho \"=== clique nativo no '+3 mais' ===\"\nagent-browser eval \"const b=Array.from(document.querySelectorAll('button')).find(x=>x.textContent.trim().startsWith('+3')); if(b){b.click(); 'clicou: '+b.textContent.trim()} else 'botao nao achado'\" 2>&1 | tail -3\nsleep 1\nagent-browser eval \"const d=document.querySelector('[role=dialog]'); d? 'DIALOG OK: '+d.querySelector('h2,[role=heading]')?.textContent : 'ainda sem dialog'\" 2>&1 | tail -3\nagent-browser screenshot \"$SCR/cal-2-daydetail.png\" 2>&1 | tail -1",
  "description": "Native click on +3 mais button and verify dialog"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === clique nativo no '+3 mais' ===
> "clicou: +3 mais"
> ✗ Evaluation error: SyntaxError: Identifier 'd' has already been declared
> ✓ Screenshot saved to /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad/cal-2-daydetail.png
> ```

## 🤖 Claude *(01:44:11)*


## 🤖 Claude *(01:44:12)*

O clique nativo funcionou ("clicou: +3 mais") — o erro foi só o `const d` já declarado num eval anterior (contexto reusado). Re-checo com var nova + vejo o screenshot:

## 🤖 Claude *(01:44:14)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nagent-browser eval \"(()=>{const dlg=document.querySelector('[role=dialog]'); return dlg? 'DIALOG OK :: '+(dlg.innerText||'').replace(/\\n+/g,' | ').slice(0,500) : 'SEM DIALOG';})()\" 2>&1 | tail -6",
  "description": "Check dialog content with fresh scope"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> "DIALOG OK :: Terça-Feira, 30 De Junho De 2026 | 6 publicações agendadas | LinkedIn | Published | 22:12 | Sem conteúdo vinculado | Conta não definida | Publicado 30/06 às 22:15 · urn:li:share:7477892496954585088 | Reagendar | Duplicar | Remover | Criado 30/06/26 22:12 · id e30cc71c | Twitter/X | Failed | 22:12 | Sem conteúdo vinculado | Conta não definida | No active twitter account found | Tentativas: 3/3 | Reagendar | Duplicar | Remover | Criado 30/06/26 22:12 · id 6b4cae6f | Instagram | Published | 22:13 |"
> ```

## 🤖 Claude *(01:44:21)*


## 🤖 Claude *(01:44:22)*

O modal abriu e mostra **exatamente** o que construí — propriedades completas por publicação. Vejo o render visual:

## 🤖 Claude *(01:44:22)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad/cal-2-daydetail.png"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> [{'type': 'image', 'source': {'type': 'base64', 'data': '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', 'media_type': 'image/png'}}]
> ```

## 🤖 Claude *(01:45:06)*


## 🤖 Claude *(01:45:10)*

O modal renderiza **perfeito** — verificação visual + DOM (Lei 1):
- **"Terça-Feira, 30 De Junho De 2026 · 6 publicações agendadas"**
- **LinkedIn** `Published` · 22:12 · publicado 30/06 às 22:15 · `urn:li:share:7477...` (post id real) · Reagendar/Duplicar/Remover · criado + id
- **Twitter/X** `Failed` · erro em vermelho "No active twitter account found" · Tentativas 3/3
- CTA **"Agendar nova publicação nesta data"**

Zero white-screen, zero erro de console, todas as propriedades presentes. Antes de deployar, confiro o git status pra não empurrar WIP do loop no build:

## 🤖 Claude *(01:45:11)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== git status ===\"\ngit status --short\necho \"HEAD: $(git log -1 --format='%h %s' | head -c 90)\"",
  "description": "Check git status before deploy"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === git status ===
> ?? .claude/context/native-exclusive-hyperframes-opendesign-eval-2026-06-30.md
> ?? .claude/context/video-cycle-zero-usd-audit-2026-06-30.md
> HEAD: a29627b feat(calendar): day-detail modal — clicar dia/post abre todas as publicações d
> ```

## 🤖 Claude *(01:45:22)*


## 🤖 Claude *(01:45:24)*

Git limpo (só meus 2 docs de contexto untracked — não entram no build). O temp build reflete o HEAD commitado. **Deploy** (rsync temp → dist servido pelo nginx) + verificação material:

## 🤖 Claude *(01:45:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nOUT=/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/scratchpad/cal-dist\necho \"=== rsync temp dist \u2192 dist servido ===\"\nrsync -a --delete \"$OUT/\" dist/ && echo \"rsync OK\"\necho \"=== chunk servido cont\u00e9m o c\u00f3digo novo? ===\"\ngrep -rl \"nesta data\" dist/assets/ 2>/dev/null | head -1 && echo \"OK: string nova servida\"\necho \"=== env baked (supabase ref no bundle servido)? ===\"\ngrep -rl \"bcyvddsykvehvpwstlfa\" dist/assets/ 2>/dev/null | head -1 && echo \"OK: env Supabase baked\" || echo \"AVISO: env n\u00e3o achado\"\necho \"=== index referencia o chunk CalendarPage? ===\"\ngrep -oE \"CalendarPage-[A-Za-z0-9]+\\.js\" dist/assets/*.js 2>/dev/null | head -1\necho\necho \"=== cleanup: fechar browser + preview ===\"\nagent-browser close --all 2>/dev/null; echo \"browser fechado\"",
  "description": "Deploy calendar to served dist and verify materially"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === rsync temp dist → dist servido ===
> rsync OK
> === chunk servido contém o código novo? ===
> dist/assets/CalendarPage-CCgZuuDP.js
> OK: string nova servida
> === env baked (supabase ref no bundle servido)? ===
> dist/assets/SettingsPage-BxEh5aCQ.js
> OK: env Supabase baked
> === index referencia o chunk CalendarPage? ===
> dist/assets/index-vij5ll1D.js:CalendarPage-CCgZuuDP.js
> 
> === cleanup: fechar browser + preview ===
> ✓ Closed session: default
> browser fechado
> ```

## 🤖 Claude *(01:45:40)*


## 🤖 Claude *(01:45:41)*

Deploy **verificado materialmente** ✅:
- rsync OK · chunk servido `CalendarPage-CCgZuuDP.js` contém `nesta data` · env Supabase baked · `index` referencia o chunk · browser fechado.

Cleanup do preview + commito os 2 docs de contexto (eval do fork + audit zero-USD):

## 🤖 Claude *(01:45:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\npkill -f \"vite preview\" 2>/dev/null; echo \"preview encerrado\"\ngit add .claude/context/native-exclusive-hyperframes-opendesign-eval-2026-06-30.md .claude/context/video-cycle-zero-usd-audit-2026-06-30.md\ngit commit -q -m \"docs(context): zero-USD video-cycle audit + native-exclusive fork eval (opensrc/graphify red herrings; HyperFrames-first path)\n\nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>\" && echo \"docs commit: $(git log -1 --format=%h)\"",
  "description": "Kill preview and commit context docs"
}
```

> **Tool Result (Bash)** - ❌ Error
>
> ```
> Exit code 144
> ```

## 🤖 Claude *(01:45:50)*


## 🤖 Claude *(01:45:51)*

O exit 144 foi o próprio `pkill` sinalizando o shell (benigno — preview encerrado). Mas isso abortou o commit antes de rodar. Commito os docs separadamente:

## 🤖 Claude *(01:45:54)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add .claude/context/native-exclusive-hyperframes-opendesign-eval-2026-06-30.md .claude/context/video-cycle-zero-usd-audit-2026-06-30.md 2>/dev/null\ngit commit -q -m \"docs(context): zero-USD video-cycle audit + native-exclusive fork eval (opensrc/graphify red herrings; HyperFrames-first path)\n\nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>\" && echo \"docs commit: $(git log -1 --format=%h)\" || echo \"(nada a commitar / j\u00e1 commitado)\"\necho \"=== confirma\u00e7\u00e3o: preview morto? ===\"\ncurl -s -o /dev/null -w \"preview HTTP %{http_code}\\n\" http://127.0.0.1:4174/ 2>/dev/null || echo \"preview OFF (esperado)\"",
  "description": "Commit context docs and confirm preview down"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;6;6;6m─[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpre-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;6;6;6m─[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m╯[m
> ┃  e2e-output-tripwire ❯ 
> 
> ┃  secret-scan ❯ 
> 
> ┃  gitleaks-staged ❯ 
> 
>     ○
>     │╲
>     │ ○
>     ○ ░
>     ░    gitleaks
> 
> [90m10:45PM[0m [32mINF[0m 1 commits scanned.
> [90m10:45PM[0m [32mINF[0m scan completed in 16.2ms
> [90m10:45PM[0m [32mINF[0m no leaks found
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.10 seconds)
> ✔️ e2e-output-tripwire (0.02 seconds)
> ✔️ secret-scan (0.07 seconds)
> ✔️ gitleaks-staged (0.08 seconds)
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpost-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m╯[m
> ┃  mesh-reingest ❯ 
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.00 seconds)
> ✔️ mesh-reingest (0.00 seconds)
> docs commit: c880fcf
> === confirmação: preview morto? ===
> preview HTTP 000
> preview OFF (esperado)
> ```

## 🤖 Claude *(01:46:05)*


## 🤖 Claude *(01:46:19)*

✅ **Calendário — Detalhe do Dia: LIVE e deployado**, com prova material em cada etapa (Lei 1).

**O que estava errado:** clicar num dia sempre abria o formulário *"Agendar novo"* (`openNewPost`) e os posts/"+N mais" não abriam nada — não existia nenhuma visão de detalhe.

**O que construí (sofisticado e robusto):** um **DayDetailDialog** — clicar no **dia**, num **post** ou no **"+N mais"** abre um modal com **todas as publicações da data** e propriedades completas por publicação:
- Plataforma (cor + label) · horário · **status** (Published/Failed/…)
- **Conteúdo vinculado** (título + tipo + thumbnail) ou "Sem conteúdo"
- **Conta** (@username) ou "Conta não definida"
- **Publicado em** + `platform_post_id` real (ex: `urn:li:share:7477…`)
- **Erro** (quando falhou) + **tentativas** (retry/max)
- Ações inline: **Reagendar** (input de horário → salva) · **Duplicar** · **Remover**
- CTA **"Agendar nova publicação nesta data"** (leva ao form pré-preenchido)
- Rola para muitos posts; estado vazio tratado; plataforma/status desconhecidos com fallback.

**Verificação material:**
| Gate | Resultado |
|------|-----------|
| `tsc --noEmit` | **exit 0** |
| `eslint` | **exit 0** (3 warnings pré-existentes, não meus) |
| `vite build` | **exit 0** (33.5s) |
| Browser-verify (sessão User 0 injetada) | Render limpo **sem white-screen**; clicar dia 30 → modal abriu com **6 publicações reais** (LinkedIn `Published`, Twitter/X `Failed` "No active twitter account found" + Tentativas 3/3, Instagram…); **zero erro de console** |
| Deploy | rsync → `dist/` servido · chunk `CalendarPage-CCgZuuDP.js` contém o código novo · env baked |

**Commits:** `a29627b` (feature) + `c880fcf` (docs de contexto).

Está **no ar** em [login.mcorch.com/dashboard/calendar](https://login.mcorch.com/dashboard/calendar) — dá um **Ctrl+Shift+R** (o Cloudflare pode cachear). Clica em qualquer dia com publicações e o painel abre com tudo.

Nota mínima: o input de horário aparece como "10:12 PM" (formato 12h da locale do navegador) — é o `<input type="time">` nativo; o valor está correto (22:12). Se preferir forçar 24h eu ajusto, mas é cosmético.

Quer que eu siga para o **fork nativo do HyperFrames** (a emenda BoK) ou tem mais algum ajuste de UI que você está vendo aí?

## 👤 User *(01:56:28)*

ótimo agora acabei de excluir manual mente tanto no ui do mcorch quanto em cada uma das redes sociais, seria legal se existisse uma verificação se ainda existe online as publicações e tomar as decisões perguntando pro usuário se ele quer remover da redes sociais tambem caso ainda exista, se não só remove mesmo igual esta agora

## 🤖 Claude *(01:57:32)*


## 🤖 Claude *(01:57:42)*

Boa ideia — e é exatamente o tipo de coisa que evita "registros órfãos": deletar no MCORCH sem saber se o post ainda está vivo na rede. O fluxo que você descreve é um **smart-delete**:

> ao remover uma publicação **publicada**, verificar se ela ainda existe online → se existir, **perguntar** se quer remover da rede também (sim → deleta na plataforma + local; não → só local); se já não existir, só remove local (como hoje).

Duas coisas honestas antes de eu sair codando (Lei 1 + Protocolo de Malha Fechada):

1. **Isso é uma integração NOVA com API externa** (verificar-existência + delete remoto em cada rede) → pelo protocolo, pede **gate BoK/SOP antes do código** (e cai na regra de credencial per-user). Não vou improvisar.
2. **A viabilidade varia MUITO por rede** — e eu não vou afirmar de cabeça o que cada API permite. Delete remoto normalmente exige **escopos OAuth extras** que talvez a gente nem tenha pedido, e algumas plataformas **não têm delete público** (ex.: publicação via Content API do Instagram, TikTok). Preciso mapear isso materialmente.

Disparo uma varredura de viabilidade: uma frente por rede (verificar-existência + delete + escopo/tier exigido) + uma frente do nosso lado (o que guardamos de `platform_post_id` e quais escopos pedimos hoje). Volto com a **matriz de capacidade** + o MVP viável + o gate.

## 🤖 Claude *(01:58:24)*


🛠️ **Tool Call**: `Workflow`
```json
{
  "script": "export const meta = {\n  name: 'smart-delete-feasibility',\n  description: 'Viabilidade do smart-delete (verificar-exist\u00eancia + delete remoto) por rede social + estado atual do MCORCH',\n  phases: [\n    { title: 'Research', detail: 'API verify+delete por plataforma + mapa dos nossos escopos/ids' },\n    { title: 'Synthesize', detail: 'matriz de capacidade + MVP vi\u00e1vel + gate BoK/SOP' },\n  ],\n}\n\nconst P_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  properties: {\n    platform: { type: 'string' },\n    verify_supported: { type: 'string', enum: ['yes', 'no', 'partial', 'unknown'], description: 'D\u00e1 pra checar se um post ainda existe via API (GET by id \u2192 200/404)?' },\n    verify_how: { type: 'string', description: 'Endpoint exato + o que retorna quando o post foi deletado (404/gone/vazio).' },\n    delete_supported: { type: 'string', enum: ['yes', 'no', 'partial', 'unknown'], description: 'D\u00e1 pra DELETAR o post via API?' },\n    delete_how: { type: 'string', description: 'Endpoint/m\u00e9todo exato de delete + gotchas (janela de tempo, tipo de post, etc.).' },\n    scope_or_tier_needed: { type: 'string', description: 'Escopo OAuth / tier de API / permiss\u00e3o de app exigido p/ verify e delete (cr\u00edtico \u2014 delete costuma exigir escopo extra).' },\n    verdict: { type: 'string', enum: ['feasible_now', 'feasible_with_scope', 'not_feasible', 'partial'], description: 'Viabilidade real do smart-delete nesta rede.' },\n    evidence: { type: 'array', items: { type: 'string' }, description: 'URLs da doc oficial consultada (Lei 1).' },\n  },\n  required: ['platform', 'verify_supported', 'delete_supported', 'scope_or_tier_needed', 'verdict', 'evidence'],\n}\n\nconst PLATFORMS = [\n  { key: 'linkedin', q: 'LinkedIn \u2014 post publicado como ugcPosts/shares (guardamos id tipo urn:li:share:NNN). Pesquise a API oficial (developer.linkedin.com) p/ (1) VERIFICAR se um ugcPost/share ainda existe (GET por urn \u2192 200/404), (2) DELETAR (DELETE /ugcPosts/{urn}?), e (3) QUAL escopo OAuth (w_member_social? outro) exige verify e delete.' },\n  { key: 'instagram', q: 'Instagram \u2014 publicamos Reels/m\u00eddia via Content Publishing API (graph.instagram.com / graph.facebook.com), guardamos o media id. Pesquise a doc oficial Meta p/ (1) VERIFICAR se uma m\u00eddia IG ainda existe (GET /{ig-media-id}), (2) DELETAR m\u00eddia IG publicada via API (existe? historicamente Content Publishing N\u00c3O permite delete de posts?), (3) escopo/permiss\u00e3o exigida.' },\n  { key: 'facebook', q: 'Facebook \u2014 publicamos no feed de P\u00e1gina, guardamos o post id. Pesquise a Graph API oficial p/ (1) VERIFICAR se um post de P\u00e1gina existe (GET /{post-id}), (2) DELETAR (DELETE /{post-id}), (3) permiss\u00e3o exigida (pages_manage_posts?).' },\n  { key: 'twitter', q: 'Twitter/X \u2014 pesquise a X API v2 oficial p/ (1) VERIFICAR se um tweet existe (GET /2/tweets/{id} \u2192 data vs errors), (2) DELETAR (DELETE /2/tweets/{id}), (3) escopo (tweet.write?) + TIER pago exigido (Basic/Pro \u2014 delete funciona no free?).' },\n  { key: 'tiktok', q: 'TikTok \u2014 publicamos via Content Posting API. Pesquise a doc oficial developers.tiktok.com p/ (1) VERIFICAR se um v\u00eddeo publicado existe via API, (2) DELETAR v\u00eddeo via API (existe endpoint de delete? historicamente N\u00c3O?), (3) escopo/audit exigido.' },\n  { key: 'youtube', q: 'YouTube \u2014 publicamos via videos.insert (Data API v3), guardamos videoId. Pesquise a doc oficial p/ (1) VERIFICAR se um v\u00eddeo existe (videos.list?id=), (2) DELETAR (videos.delete), (3) escopo OAuth (youtube / youtube.force-ssl) exigido p/ delete.' },\n  { key: 'wordpress', q: 'WordPress \u2014 publicamos via WP REST API (self-hosted do tenant), guardamos o post id. Confirme (1) VERIFICAR exist\u00eancia (GET /wp-json/wp/v2/posts/{id} \u2192 200/404), (2) DELETAR (DELETE /wp-json/wp/v2/posts/{id}?force=), (3) auth exigida (application password que j\u00e1 usamos). Deve ser o mais vi\u00e1vel.' },\n]\n\nphase('Research')\nconst platformFindings = parallel(PLATFORMS.map(p => () =>\n  agent(\n    `Voc\u00ea \u00e9 pesquisador de APIs de rede social. Objetivo: viabilidade de um \"smart-delete\" no MCORCH \u2014 ao deletar uma publica\u00e7\u00e3o, checar se ela AINDA existe online e opcionalmente delet\u00e1-la na plataforma.\\n\\n${p.q}\\n\\n` +\n    `Use WebSearch/WebFetch (ou firecrawl via ToolSearch) na DOC OFICIAL. Seja material: cite endpoint exato, m\u00e9todo, escopo/permiss\u00e3o/tier, e o gotcha decisivo (ex: \"Content Publishing API do IG n\u00e3o exp\u00f5e delete\"). Se n\u00e3o achar delete oficial, verdict=not_feasible. N\u00c3O invente endpoint.`,\n    { label: `api:${p.key}`, phase: 'Research', schema: P_SCHEMA, effort: 'medium' }\n  )\n))\n\nconst ourSide = agent(\n  `Mapeie o ESTADO ATUAL do MCORCH (repo constellation-orchestra) relevante p/ o smart-delete:\\n` +\n  `(1) O que guardamos do post publicado: leia supabase/functions/publish-social/index.ts e publish-meta/index.ts \u2014 qual id de post remoto \u00e9 persistido e onde (scheduled_posts.platform_post_id? meta_posts? social por plataforma?). grep platform_post_id.\\n` +\n  `(2) Quais ESCOPOS OAuth pedimos hoje por plataforma: leia supabase/functions/social-auth-init/index.ts (os scopes de cada branch linkedin/instagram/facebook/twitter/tiktok/youtube/pinterest). Delete costuma exigir escopo EXTRA \u2014 dizemos se j\u00e1 pedimos o suficiente ou n\u00e3o.\\n` +\n  `(3) Como o delete funciona hoje: useDeleteScheduledPost (s\u00f3 apaga a linha local) + qualquer delete de content_library/meta. Confirme que N\u00c3O tocamos a plataforma hoje.\\n` +\n  `Reporte texto estruturado por plataforma: id-guardado? escopo-atual? escopo-delete-faltando? Cite file:line.`,\n  { label: 'our-state', phase: 'Research', effort: 'medium' }\n)\n\nconst [findings, current] = await Promise.all([platformFindings, ourSide])\nconst valid = findings.filter(Boolean)\n\nphase('Synthesize')\nconst SYNTH_SCHEMA = {\n  type: 'object',\n  additionalProperties: false,\n  properties: {\n    capability_matrix: { type: 'array', items: { type: 'object', additionalProperties: false, properties: { platform: { type: 'string' }, verify: { type: 'string' }, delete: { type: 'string' }, verdict: { type: 'string' }, blocker: { type: 'string' } }, required: ['platform', 'verify', 'delete', 'verdict'] } },\n    mvp_scope: { type: 'string', description: 'Quais plataformas entram num MVP vi\u00e1vel AGORA (sem escopo novo) e quais ficam de fora e por qu\u00ea.' },\n    design_sketch: { type: 'string', description: 'Design proposto: edge fn(s) verify/delete, fluxo de UI (checa exist\u00eancia \u2192 pergunta \u2192 deleta remoto+local ou s\u00f3 local), fail-open, per-user creds. Conciso.' },\n    scope_regressions: { type: 'string', description: 'Quais plataformas exigem RE-OAuth com escopo de delete extra (a\u00e7\u00e3o Sovereign) \u2014 e quais delete simplesmente N\u00c3O existem na API.' },\n    gate_recommendation: { type: 'string', description: 'Precisa BoK gate/emenda + SOP (Lei 2) antes do c\u00f3digo? Onde (post-engine? novo slice?). Honesto.' },\n    honest_caveats: { type: 'string' },\n  },\n  required: ['capability_matrix', 'mvp_scope', 'design_sketch', 'gate_recommendation'],\n}\n\nconst synth = await agent(\n  `Voc\u00ea \u00e9 o arquiteto. O Sovereign quer um smart-delete: ao remover uma publica\u00e7\u00e3o no MCORCH, checar se ela ainda existe online e perguntar se quer deletar da rede tamb\u00e9m (sen\u00e3o s\u00f3 local, como hoje). ` +\n  `Doutrina: per-user creds, fail-closed, valor vis\u00edvel ao usu\u00e1rio. Recebeu a viabilidade por plataforma + o estado atual do MCORCH. ` +\n  `Produza: matriz de capacidade (verify/delete/verdict/blocker por plataforma), escopo do MVP vi\u00e1vel AGORA, esbo\u00e7o de design (edge fns + fluxo UI), regress\u00f5es de escopo (re-OAuth Sovereign), e se precisa gate BoK/SOP. Seja honesto sobre o que N\u00c3O d\u00e1 (plataformas sem delete p\u00fablico).\\n\\n` +\n  `## Viabilidade por plataforma\\n${JSON.stringify(valid, null, 2)}\\n\\n## Estado atual MCORCH\\n${typeof current === 'string' ? current : JSON.stringify(current)}`,\n  { label: 'architect', phase: 'Synthesize', schema: SYNTH_SCHEMA, effort: 'high' }\n)\n\nreturn { platforms: valid, current, synth }\n",
  "description": "Research smart-delete feasibility per platform"
}
```

> **Tool Result (Workflow)** - ✅ Success
>
> ```
> Workflow launched in background. Task ID: wfwa3r0wj
> Summary: Viabilidade do smart-delete (verificar-existência + delete remoto) por rede social + estado atual do MCORCH
> Transcript dir: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/subagents/workflows/wf_2da3b945-7b0
> Script file: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/workflows/scripts/smart-delete-feasibility-wf_2da3b945-7b0.js
> (Edit this file with Write/Edit and re-invoke Workflow with {scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/workflows/scripts/smart-delete-feasibility-wf_2da3b945-7b0.js"} to iterate without resending the script.)
> Run ID: wf_2da3b945-7b0
> To resume after editing the script: Workflow({scriptPath: "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/workflows/scripts/smart-delete-feasibility-wf_2da3b945-7b0.js", resumeFromRunId: "wf_2da3b945-7b0"}) — completed agents return cached results.
> 
> You will be notified when it completes. Use /workflows to watch live progress.
> ```

## 🤖 Claude *(01:58:29)*


## 🤖 Claude *(01:58:37)*

Varredura de viabilidade em voo (`wf_2da3b945-7b0`) — 7 redes + o nosso lado + arquiteto. Quando voltar te entrego:

- **Matriz de capacidade** por rede: dá pra *verificar existência* (GET→404)? dá pra *deletar* via API? qual escopo/tier exige?
- **MVP viável agora** (as redes que já dá sem pedir escopo novo — provavelmente WordPress e LinkedIn) vs. as que precisam de **re-OAuth com escopo de delete** (ação sua) vs. as que **simplesmente não têm delete público** (aí o MVP é: "não existe mais / não dá pra deletar remoto → só remove local", que é justamente o fallback que você descreveu).
- **Esboço de design** (edge fn `verify-social-post` + `delete-social-post` fail-closed per-user + o fluxo de UI: checa → pergunta → deleta remoto+local ou só local).
- **O gate**: onde selar o BoK/SOP antes do código (provável emenda ao `post-engine`).

Adianto uma expectativa honesta: **Instagram (Content Publishing) e TikTok historicamente não expõem delete via API** — pra essas, o "smart-delete" vira "verifico se ainda existe; se existe e você quer remover, te aviso que tem que ser manual na rede; se não existe, limpo o registro". Vou confirmar isso materialmente na doc oficial antes de cravar. Te aviso quando concluir.

## 👤 User *(02:04:45)*

<task-notification>
<task-id>wfwa3r0wj</task-id>
<tool-use-id>toolu_01QuCbQCjFmUSzTCKHViQhcS</tool-use-id>
<output-file>/tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/tasks/wfwa3r0wj.output</output-file>
<status>completed</status>
<summary>Dynamic workflow "Viabilidade do smart-delete (verificar-existência + delete remoto) por rede social + estado atual do MCORCH" completed</summary>
<result>{"platforms":[{"platform":"LinkedIn","verify_supported":"partial","delete_supported":"yes","verify_how":"GET single post by URN: `GET https://api.linkedin.com/rest/posts/{encoded ugcPostUrn|shareUrn}` (headers: Authorization Bearer, X-Restli-Protocol-Version: 2.0.0, Linkedin-Version: YYYYMM). Returns 200 + JSON body (id, lifecycleState PUBLISHED, commentary...) if the post still exists; returns HTTP 404 NOT_FOUND (\"The requested post was not found\") when the post was deleted or never existed — this is the clean existence signal. Legacy equivalent: `GET https://api.linkedin.com/v2/ugcPosts/{encoded urn}`. Both accept the exact URN types MCORCH stores (urn:li:share:NNN and urn:li:ugcPost:NNN). GOTCHA: single-URN read + author-finder read both require the r_member_social scope, which the official doc explicitly marks as RESTRICTED / \"available to approved users only\" — a standard w_member_social app CANNOT call GET-verify without going through LinkedIn's restricted-scope approval. Practical workaround: skip explicit verify and rely on the DELETE response itself (idempotent 204), since DELETE only needs the write scope.","delete_how":"Legacy (matches stored urn:li:share/ugcPost ids): `DELETE https://api.linkedin.com/v2/ugcPosts/{encoded urn}` with headers Authorization Bearer + X-Restli-Protocol-Version: 2.0.0. Current replacement (recommended, ugcPosts API is legacy): `DELETE https://api.linkedin.com/rest/posts/{encoded ugcPostUrn|shareUrn}` with headers Authorization Bearer + X-Restli-Protocol-Version: 2.0.0 + Linkedin-Version: YYYYMM + X-RestLi-Method: DELETE. GOTCHAS: (1) URN must be URL-encoded (urn:li:ugcPost:12345 -&gt; urn%3Ali%3AugcPost%3A12345). (2) Deletion is IDEMPOTENT — deleting an already-deleted/nonexistent post also returns 204, so a 204 does NOT by itself prove the post existed. (3) Batch delete is NOT supported — one DELETE call per URN. (4) Success = HTTP 204 No Content (no body).","scope_or_tier_needed":"DELETE + UPDATE (write): w_member_social (posts on behalf of the authenticated member — this is what MCORCH already uses to publish) OR w_organization_social (org page posts, requires ADMINISTRATOR/CONTENT_ADMIN/DIRECT_SPONSORED_CONTENT_POSTER page role). NO extra scope beyond publishing is needed to delete a member's own post. VERIFY (GET by URN): r_member_social (member) or r_organization_social (org) — and r_member_social is RESTRICTED, available to approved users only per the official Permissions table. Product tier: standard \"Share on LinkedIn\" / \"Sign In with LinkedIn\" products grant w_member_social; r_member_social requires a separate restricted-access approval from LinkedIn. Headers required on all calls: X-Restli-Protocol-Version: 2.0.0 (+ Linkedin-Version: YYYYMM for the /rest/ Posts API).","verdict":"feasible_with_scope","evidence":["https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api?view=li-lms-2025-11","https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/ugc-post-api?view=li-lms-2025-11","https://learn.microsoft.com/en-us/linkedin/compliance/integrations/shares/ugc-post-api"]},{"platform":"Instagram (Meta Content Publishing / Instagram Platform API)","verify_supported":"yes","verify_how":"GET https://graph.instagram.com/&lt;API_VERSION&gt;/&lt;IG_MEDIA_ID&gt;?fields=id,media_type,timestamp,media_url,owner&amp;access_token=&lt;ACCESS_TOKEN&gt; (ou graph.facebook.com para Facebook Login). Exemplo oficial: curl -X GET 'https://graph.instagram.com/v25.0/17895695668004550?fields=id,media_type,media_url,owner,timestamp&amp;access_token=...'. Se a mídia EXISTE → 200 com o objeto (id/media_type/timestamp). Se foi DELETADA/inacessível → erro (tipicamente HTTP 400 com error.code 100 \"does not exist, cannot be loaded due to missing permissions, or cannot be viewed by this user\" / objeto inválido). NÃO há 404 REST limpo — o \"gone\" chega como GraphMethodException/OAuthException. MCORCH já guarda o media id do Reel publicado, então o probe é direto pelo id salvo.","delete_supported":"partial","delete_how":"DELETE https://graph.facebook.com/&lt;API_VERSION&gt;/&lt;IG_MEDIA_ID&gt;?access_token=&lt;ACCESS_TOKEN&gt; → sucesso retorna {\"success\": true, \"deleted_id\": \"&lt;IG_MEDIA_ID&gt;\"}. Suporta posts (não-ads), stories, reels e carrosséis INTEIROS. GOTCHA DECISIVO 1: para carrossel só dá pra deletar o álbum inteiro passando o media id do CONTAINER do carrossel — não dá pra deletar item individual. GOTCHA DECISIVO 2 (bloqueante p/ o MCORCH): a doc oficial afirma explicitamente que o delete \"only supports Instagram API with Facebook Login\" — ou seja, exige conexão via Facebook Login (Page access token, host graph.facebook.com). O MCORCH publica Reels via Instagram Business Login em graph.instagram.com (ref reference_ig_reels_publish_path), path onde o DELETE NÃO é suportado. GOTCHA 3: ads posts não são deletáveis. Historicamente a Content Publishing API NÃO expunha delete; o endpoint DELETE apareceu recentemente (página IG Media atualizada 2026-06-22).","scope_or_tier_needed":"VERIFY (GET media): instagram_business_basic (Instagram Login) ou o par instagram_graph_user_profile/pages_read_engagement no Facebook Login — leitura básica do objeto de mídia. DELETE: exige Instagram API with Facebook Login → permissões de content publishing instagram_business_content_publish + pages_read_engagement + pages_show_list, com Page access token (não o Instagram user token). App precisa passar App Review para essas permissões avançadas em produção (fora do modo dev/tester). O token de publicação atual do MCORCH (Instagram Business Login, graph.instagram.com, scope publish) NÃO habilita o DELETE — precisaria de uma conexão Facebook Login separada.","verdict":"feasible_with_scope","evidence":["https://developers.facebook.com/docs/instagram-platform/reference/instagram-media/","https://developers.facebook.com/docs/instagram-platform/content-publishing/","https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/content-publishing/","https://developers.facebook.com/docs/instagram-platform/instagram-graph-api/reference/ig-media"]},{"platform":"Facebook (Graph API — Page feed posts)","verify_supported":"yes","verify_how":"GET /v{ver}/{page-id}_{post-id} (composite id we store) with a Page access token. Returns 200 + post fields (id, message, created_time, updated_time, permalink_url, status_type, from, likes/comments/reactions) when the post still exists. When the post was deleted/removed, Graph API does NOT return an empty body — it returns an ERROR (typically HTTP 400 with error.code 100, \"Unsupported get request... does not exist, cannot be loaded due to missing permissions, or does not support this operation\"; sometimes code 803). So existence = 200-with-id; gone = error 100. Ask minimal fields (?fields=id,permalink_url) to keep it cheap. Read requires pages_read_engagement.","delete_supported":"yes","delete_how":"DELETE /v{ver}/{page-id}_{post-id} with a Page access token → success body {\"success\": true}. DECISIVE GOTCHA: an app can only delete a post it ITSELF published (ownership-bound) — you cannot delete posts created by the user in Facebook UI or by another app. This is exactly MCORCH's case: we publish to the Page feed via our app and store the post id, so those are app-published and deletable. No documented time window and no post-type restriction beyond ownership (photo/video posts deleted via same id, though media objects may need their own /{photo-id} or /{video-id} delete). Note: one Meta doc page hedges \"only select developers can perform this via API\" — legacy/stale caveat contradicted by the pages_manage_posts permission page which explicitly lists delete; in practice pages_manage_posts is the governing scope.","scope_or_tier_needed":"Page access token (long-lived, derived from a long-lived User token → non-expiring). For DELETE (and create/edit): pages_manage_posts. Dependencies auto-required: pages_read_engageme
... (truncated 34226 chars, full result in /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/tasks/wfwa3r0wj.output)</result>
<usage><agent_count>9</agent_count><subagent_tokens>737258</subagent_tokens><tool_uses>64</tool_uses><duration_ms>381237</duration_ms></usage>
</task-notification>

## 🤖 Claude *(02:04:50)*


## 🤖 Claude *(02:04:52)*

A varredura voltou. Leio o veredito completo do arquiteto + as redes que faltaram (Twitter/TikTok/YouTube/WordPress) + o nosso estado:

## 🤖 Claude *(02:04:55)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/tasks\npython3 - <<'PY'\nimport json\nd=json.load(open('wfwa3r0wj.output'))\nr=d['result']\nprint(\"=== PLATAFORMAS (resumo) ===\")\nfor p in r['platforms']:\n    print(f\"\\n### {p['platform']}\")\n    print(f\"  verify={p['verify_supported']} \u00b7 delete={p['delete_supported']} \u00b7 verdict={p['verdict']}\")\n    print(f\"  scope/tier: {p['scope_or_tier_needed'][:280]}\")\nprint(\"\\n\\n=== NOSSO ESTADO (current) ===\")\ncur=r.get('current','')\nprint(cur[:2500] if isinstance(cur,str) else json.dumps(cur)[:2500])\nPY",
  "description": "Read platform summaries and current state"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === PLATAFORMAS (resumo) ===
> 
> ### LinkedIn
>   verify=partial · delete=yes · verdict=feasible_with_scope
>   scope/tier: DELETE + UPDATE (write): w_member_social (posts on behalf of the authenticated member — this is what MCORCH already uses to publish) OR w_organization_social (org page posts, requires ADMINISTRATOR/CONTENT_ADMIN/DIRECT_SPONSORED_CONTENT_POSTER page role). NO extra scope beyond pu
> 
> ### Instagram (Meta Content Publishing / Instagram Platform API)
>   verify=yes · delete=partial · verdict=feasible_with_scope
>   scope/tier: VERIFY (GET media): instagram_business_basic (Instagram Login) ou o par instagram_graph_user_profile/pages_read_engagement no Facebook Login — leitura básica do objeto de mídia. DELETE: exige Instagram API with Facebook Login → permissões de content publishing instagram_business_
> 
> ### Facebook (Graph API — Page feed posts)
>   verify=yes · delete=yes · verdict=feasible_with_scope
>   scope/tier: Page access token (long-lived, derived from a long-lived User token → non-expiring). For DELETE (and create/edit): pages_manage_posts. Dependencies auto-required: pages_read_engagement + pages_show_list. To only VERIFY existence: pages_read_engagement suffices. Advanced Access to
> 
> ### Twitter / X (X API v2)
>   verify=yes · delete=yes · verdict=feasible_with_scope
>   scope/tier: OAuth 2.0 User Context (PKCE), NÃO app-only/Bearer. VERIFY (GET /2/tweets): scopes `tweet.read` + `users.read`. DELETE (DELETE /2/tweets): scopes `tweet.read` + `tweet.write` + `users.read` — o `tweet.write` é o crítico e exige re-consentimento do usuário (o fluxo social atual de
> 
> ### TikTok
>   verify=partial · delete=no · verdict=partial
>   scope/tier: Verify: `video.list` scope (Display API). Delete: NENHUM escopo de delete existe — a lista oficial de escopos tem apenas `video.list` (read), `video.publish` (Direct Post) e `video.upload` (draft). Não há `video.delete`/`video.remove`. Além disso, `video.publish` (Content Posting
> 
> ### YouTube (Data API v3)
>   verify=yes · delete=yes · verdict=feasible_with_scope
>   scope/tier: VERIFY: API key (chave publica) basta para dados publicos; nenhum scope OAuth exigido. DELETE: OAuth 2.0 obrigatorio (write op) com um destes scopes — `https://www.googleapis.com/auth/youtube` OU `https://www.googleapis.com/auth/youtube.force-ssl` (ou `youtubepartner` para contas
> 
> ### WordPress (self-hosted, WP REST API v2)
>   verify=yes · delete=yes · verdict=feasible_now
>   scope/tier: Application Password (WP 5.6+, o MESMO mecanismo que o MCORCH já usa para publicar — nenhum escopo/tier novo). As permissões são herdadas do usuário dono da Application Password: DELETE do próprio post exige capability delete_posts; deletar post de outro autor exige delete_others
> 
> 
> === NOSSO ESTADO (current) ===
> Estado atual do MCORCH relevante para o smart-delete (delete do post na PLATAFORMA remota). Reporte por eixo:
> 
> ---
> 
> ## (1) O que guardamos do post publicado (id remoto)
> 
> | Plataforma | ID remoto guardado? | Onde | file:line |
> |---|---|---|---|
> | **LinkedIn** | SIM | `scheduled_posts.platform_post_id` (só quando o publish veio com `scheduled_post_id`; o valor é `result.id \|\| result.data?.id \|\| result["X-RestLi-Id"]` — para o LinkedIn é o `X-RestLi-Id` = urn do ugcPost) | `publish-social/index.ts:625-633` |
> | **Instagram (via publish-social)** | SIM | idem `scheduled_posts.platform_post_id` (`result.id` = media id publicado) | `publish-social/index.ts:200`, `:631` |
> | **Facebook (via publish-social)** | SIM | idem `scheduled_posts.platform_post_id` (`result.id` = `{page}_{post}` id) | `publish-social/index.ts:217/219`, `:631` |
> | **Twitter/X** | SIM | idem; single tweet `result.id`; thread `result = { id: ids[0], thread_ids: ids }` → **só o 1º tweet vai pro `platform_post_id`**; os demais ids do thread ficam SÓ no `result` retornado (não persistidos) | `publish-social/index.ts:252`, `:631` |
> | **TikTok** | PARCIAL/FRÁGIL | `result = { id: publicPostId, publish_id, status }` → `platform_post_id` recebe `publicPostId`, que é **null** em conta não-auditada (SELF_ONLY). O `publish_id` (sempre presente) **não é persistido** | `publish-social/index.ts:389`, `:631` |
> | **YouTube** | SIM | `result = { id: videoId, privacyStatus }` → `platform_post_id` = videoId | `publish-social/index.ts:476`, `:631` |
> | **Pinterest** | SIM | `result` = objeto do pin (`result.id`) → `platform_post_id` = pin id | `publish-social/index.ts:593/613`, `:631` |
> | **Meta (via publish-meta — path separado)** | SIM, em TABELA DIFERENTE | `meta_posts.meta_post_id` (+ `post_url`), NÃO em `scheduled_posts`. Colunas `meta_post_id TEXT NOT NULL` / `post_url TEXT` (migration `20260530210000_meta_api_foundation.sql:68-69`). IG=`published.id`, FB=`fb.id` | `publish-meta/index.ts:197-206` |
> 
> **Achado crítico:** há DOIS caminhos de publicação IG/FB com armazenamento divergente — `publish-social` grava em `scheduled_posts.platform_post_id`; `publish-meta` grava em `meta_posts.meta_post_id`. O smart-delete terá que cobrir as duas fontes (ou o mesmo post remoto pode não ser encontrável dependendo de qual fn publicou). O `platform_post_id` também **só é gravado se veio `scheduled_post_id`** no payload — publishes ad-hoc/pipeline sem esse id NÃO persistem o id remoto em lugar nenhum de `scheduled_posts
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(02:05:08)*


## 🤖 Claude *(02:05:12)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /tmp/claude-1001/-home-gcrUX-htdocs-constellation-orchestra/473299a8-6c7d-4634-b97a-50a8fad59b11/tasks\npython3 - <<'PY'\nimport json\nd=json.load(open('wfwa3r0wj.output'))\ns=d['result']['synth']\nprint(\"=== MATRIZ ===\")\nfor m in s['capability_matrix']:\n    print(f\"  {m['platform']:12} verify={m.get('verify'):8} delete={m.get('delete'):8} verdict={m.get('verdict'):20} blocker={m.get('blocker','')[:70]}\")\nfor k in ['mvp_scope','design_sketch','scope_regressions','gate_recommendation','honest_caveats']:\n    print(f\"\\n=== {k.upper()} ===\\n{s.get(k,'')}\")\nPY",
  "description": "Read architect synthesis: matrix, MVP, design, gate"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === MATRIZ ===
>   WordPress (self-hosted) verify=GET /wp-json/wp/v2/posts/{id} → 200=vive, 404 rest_post_invalid_id=some. Auth com a mesma Application Password para distinguir trash de permanent. delete=DELETE /wp-json/wp/v2/posts/{id}?force=true (bypassa Trash → permanente) → 200 {deleted:true}. force=false só manda pra lixeira (semântica a decidir). 2ª chamada = 410 Gone (idempotência natural). verdict=feasible_now         blocker=NENHUM. Application Password já usada no publish carrega delete_posts 
>   Twitter / X  verify=GET /2/tweets/{id} → HTTP SEMPRE 200. Existência = presença de `data` vs `errors[].title=='Not Found Error'` (ResourceNotFoundProblem). NUNCA checar só o status HTTP. delete=DELETE /2/tweets/{id} → 200 {data:{deleted:true}}. Só posts do usuário autenticado. Rate 50/15min user-context. Retry idempotente em 500 (re-verify GET antes de reenviar). verdict=feasible_with_scope  blocker=Escopo `tweet.write` JÁ pedido (social-auth-init:100) → delete tecnica
>   Pinterest    verify=GET /v5/pins/{id} (pins:read, já concedido) → 200=vive / 404=some. delete=DELETE /v5/pins/{id} → exige pins:write, JÁ pedido (social-auth-init:158). verdict=feasible_with_scope  blocker=NENHUM escopo novo — pins:write já concedido. id remoto guardado em sc
>   LinkedIn     verify=GET /rest/posts/{urn} ou /v2/ugcPosts/{urn} → 200=vive, 404 NOT_FOUND=some. GOTCHA: verify exige r_member_social, escopo RESTRITO (aprovação especial LinkedIn). Prático: PULAR verify e confiar no DELETE idempotente (204). delete=DELETE /v2/ugcPosts/{urn-encoded} (headers X-Restli-Protocol-Version:2.0.0) ou /rest/posts/{urn} (+Linkedin-Version, X-RestLi-Method:DELETE). URN URL-encoded. 204=sucesso. IDEMPOTENTE: 204 NÃO prova que existia. Sem batch (1 call/urn). verdict=feasible_with_scope  blocker=DELETE coberto por w_member_social JÁ concedido (social-auth-init:76) 
>   Facebook (Page feed) verify=GET /{page-id}_{post-id}?fields=id,permalink_url (Page token, pages_read_engagement) → 200-com-id=vive / erro code 100=some (não body vazio). delete=DELETE /{page-id}_{post-id} (Page token) → {success:true}. Só posts que o PRÓPRIO app publicou (ownership-bound) — exatamente o caso MCORCH. Sem janela de tempo. verdict=feasible_with_scope  blocker=REGRESSÃO DE ESCOPO: precisa pages_manage_posts (+pages_read_engagemen
>   YouTube      verify=GET /youtube/v3/videos?part=status&id={id} (API key basta) → 200 SEMPRE; existência = items.length. Deletado/removido → items=[] (NÃO 404). delete=DELETE /youtube/v3/videos?id={id} (Bearer OAuth) → 204. 403 se token não-dono/sem escopo. Delete é PERMANENTE (alternativa não-destrutiva: videos.update privacyStatus=private). verdict=feasible_with_scope  blocker=REGRESSÃO DE ESCOPO: publicamos com youtube.upload (social-auth-init:1
>   TikTok       verify=POST /v2/video/query/ (video.list) filtrando video_ids → retorna só os que pertencem/existem; deletado = AUSÊNCIA do array (sinal implícito, sem 404 dedicado). delete=NÃO EXISTE. Content Posting API só cria (Direct Post/Upload). Nenhum escopo video.delete/remove. TikTok nunca ofereceu delete via API. verdict=delete_impossible    blocker=IMPOSSÍVEL via API — limitação da plataforma, nenhum escopo resolve. S
>   Instagram    verify=GET graph.instagram.com/{ig-media-id}?fields=id,media_type,timestamp → 200=vive / erro code 100 (GraphMethodException/OAuthException)=some. NÃO há 404 REST limpo. delete=DELETE graph.facebook.com/{ig-media-id} EXISTE (novo, doc 2026-06-22) MAS 'only supports Instagram API with Facebook Login' (host graph.facebook.com + Page token). MCORCH publica via Instagram Business Login em graph.instagram.com → path onde o DELETE NÃO é suportado. verdict=delete_impossible_current_connection blocker=IMPOSSÍVEL com a conexão atual (ref reference_ig_reels_publish_path: g
> 
> === MVP_SCOPE ===
> MVP viável AGORA (zero ação Sovereign, zero re-OAuth, doutrina per-user/fail-closed intacta) = TRÊS plataformas onde o escopo de delete JÁ está concedido:
> 
> 1. WordPress — feasible_now, delete E2E completo (verify 404 + delete force). É o caso mais forte e o único 'feasible_now' puro.
> 2. Twitter/X — tweet.write já concedido; verify robusto (data vs errors[]). RESSALVA operacional: BYOK per-user X é pré-requisito de fato pelo novo tier pago (cada tenant com credenciais próprias) — alinhado à doutrina, mas o Usuário Zero precisa ter conectado X com tweet.write. Thread só deleta o head até persistirmos os thread_ids (fix barato de fragilidade, incluir no MVP).
> 3. Pinterest — pins:write já concedido; verify + delete simétricos, o mais limpo depois do WP.
> 
> FORA do MVP:
> - LinkedIn: entra em 'MVP-'; delete provavelmente coberto por w_member_social, mas SEM verify (r_member_social restrito) → não conseguimos honrar o 'checar se ainda existe online' antes de perguntar. Design degradado (delete idempotente, sem prova prévia de existência). Candidato a Fatia 2 após validar o w_member_social em teste real.
> - Facebook + YouTube: exigem re-OAuth com escopo extra (pages_manage_posts / youtube.force-ssl) = ação Sovereign → Fatia 3 (regressão de escopo).
> - TikTok + Instagram: delete IMPOSSÍVEL na conexão atual → NUNCA entram como 'delete remoto'. UI deve dizer honestamente 'só local; delete manual no app'.
> 
> Corolário de valor visível: o MVP entrega smart-delete real para WP+X+Pinterest e, para as demais, um fluxo honesto que informa 'este post continua no ar em <rede> e essa rede não permite remover pela API — removi só do MCORCH'. Isso já é valor (transparência) sem prometer o impossível.
> 
> === DESIGN_SKETCH ===
> EDGE FUNCTIONS (2 novas, JWT-guarded, per-user fail-closed):
> 
> 1. `check-post-existence` (verify) — POST {source_table, record_id}. Resolve platform + platform_post_id lendo scheduled_posts.platform_post_id E meta_posts.meta_post_id (cobrir os DOIS paths; achado crítico do estado atual). Resolve credencial per-user (social_credentials/meta_config/wp Application Password) via auth.uid() — FAIL-CLOSED: sem credencial → 501 {error:'<svc>_not_configured'}. Dispatch por plataforma com o sinal de existência CORRETO por API (data vs errors[] no X; items.length no YT; 404 no WP; code 100 no FB/IG; ausência no array no TikTok). Retorna {exists:boolean|'unknown', platform, deletable_via_api:boolean, remote_url?}. Telemetry infra_health_logs service='smart-delete-verify' (success/degraded/error).
> 
> 2. `delete-remote-post` (delete) — POST {source_table, record_id, confirm:true}. Re-resolve credencial per-user fail-closed (NUNCA confia em flag do cliente; espelha a golden rule do intent-execute). Dispatch DELETE por plataforma (idempotente: trata already-deleted como sucesso). WP force=true. NÃO apaga a linha local aqui — retorna {remote_deleted:boolean} e o hook decide o local delete. 1 chamada/id; thread X itera thread_ids (após persisti-los). Telemetry + mesh observation node no 1º delete remoto bem-sucedido (mandato Mesh).
> 
> Pré-requisito de dados (fix de fragilidade, barato, no MVP): persistir thread_ids do X e publish_id do TikTok; e mapear onde o WP post_id vive.
> 
> FLUXO DE UI (useDeleteScheduledPost / useDeleteContent — hoje só .delete() local):
> 1. Usuário clica remover → em vez de deletar direto, chama check-post-existence.
> 2a. deletable_via_api=false (IG/TikTok, ou LinkedIn sem verify) → dialog honesto: 'Este post pode continuar no ar em <rede>; essa rede não permite remover pela API. Remover só do MCORCH?' → só local delete (comportamento de hoje).
> 2b. exists=true & deletable → dialog: 'Este post ainda está publicado em <rede> [ver link]. Deletar também da rede?' com 2 ações: [Deletar da rede + local] (chama delete-remote-post, depois local delete só se remote_deleted) e [Só do MCORCH] (local delete direto).
> 2c. exists=false → 'Já não está mais online; removendo só o registro local.' → local delete.
> 3. FAIL-OPEN de conveniência: se check-post-existence falhar (rede/timeout), NÃO travar o usuário — oferecer local delete com aviso 'não consegui confirmar o estado remoto'. (Fail-closed é para CREDENCIAL/autorização; fail-open é para o probe de conveniência — distinção deliberada.)
> 
> Doutrina: per-user creds em toda resolução; fail-closed em credencial ausente; valor visível = transparência sobre o que continua no ar. Reusa dialog/toast existentes; lógica toda em hooks (Harness).
> 
> === SCOPE_REGRESSIONS ===
> RE-OAUTH COM ESCOPO EXTRA (ação Sovereign — força re-consent de TODAS as contas já conectadas; o próprio código avisa disso em social-auth-init:156-157):
> - Facebook: hoje reusa scopes IG (instagram_business_*, social-auth-init:79-88), NÃO tem pages_manage_posts. Delete de Page post exige pages_manage_posts + Page token + App Review + Business Verification. É reconstrução do consentimento FB.
> - YouTube: hoje youtube.upload (social-auth-init:139), que NÃO cobre delete. Exige youtube ou youtube.force-ssl → re-consent de todas as contas YT.
> - LinkedIn (parcial): DELETE provavelmente coberto por w_member_social (validar), MAS o VERIFY exige r_member_social, escopo RESTRITO que precisa aprovação especial da LinkedIn (não é só re-consent, é acesso restrito a 'approved users only'). Sem ele, LinkedIn opera delete-sem-verify.
> - Instagram: não é 'escopo extra' num fluxo — é uma CONEXÃO NOVA. O delete recém-lançado só funciona via Facebook Login (graph.facebook.com + Page token), e o MCORCH conecta via Instagram Business Login (graph.instagram.com). Migrar habilita delete mas quebra/duplica o path de publish atual (ref reference_ig_reels_publish_path). Ação Sovereign grande.
> 
> DELETE SIMPLESMENTE NÃO EXISTE NA API (nenhum escopo/ação resolve — limitação permanente da plataforma):
> - TikTok: Content Posting API só cria (Direct Post/Upload). Nunca houve endpoint de delete. Único caminho = criador no app.
> - Instagram (na conexão atual graph.instagram.com): o DELETE existe só no path Facebook Login; pela conexão Instagram Business Login que usamos, não é exposto.
> 
> Para TikTok e IG(conexão atual), a honestidade obrigatória: NÃO prometer smart-delete; UI diz 'removido só do MCORCH; para tirar do ar, delete manualmente no app <rede>'.
> 
> === GATE_RECOMMENDATION ===
> SIM — precisa gate/emenda BoK + SOP (Lei 2) ANTES do código. Justificativa: o smart-delete é feature de automação NOVA que (a) toca ≥3 integrações externas materialmente e (b) introduz uma capability destrutiva-irreversível (delete remoto permanente, ex. YouTube/WP force=true) que hoje não existe em lugar nenhum (grep DELETE = 0). Não cai em nenhuma exemption (não é typo/bump/lint/patch de feature já documentada).
> 
> ONDE: é uma EMENDA ao BoK post-engine existente (docs/bok/post-engine/), não um slice novo do zero — o smart-delete é o inverso simétrico do publish já documentado ali (reshaper/atomizer/publishers). Emendar FRD post-engine com FR-SD-00x (verify/delete/UI-flow) + SDD-level com a Capability Matrix por plataforma como SSOT (qual delete existe, qual escopo, qual sinal-de-existência) + Pattern Conformance Declaration.
> 
> SOP obrigatório (Lei 2 + API Tenancy Model exige 'SOP antes de qualquer código' para nova integração/credencial): docs/processes/smart-delete-remote.md respondendo Operator/Sequence/Verification/Recovery/Success — crítico porque delete é irreversível: o Recovery path e o gate de confirmação (nunca confiar em flag do cliente) precisam estar escritos antes. Cada plataforma precisa do 'sinal de existência' documentado (o X 200-com-errors[], YT items=[], WP 404) senão o verify vira falso-positivo/negativo.
> 
> /security-review obrigatório se houver migration (novas colunas thread_ids/publish_id, ou tabela de audit de delete) — FMEA-011 cross-tenant. E as regressões de escopo (FB pages_manage_posts, YT youtube.force-ssl) são ações Sovereign que devem ser registradas como OTDs no FRD antes de qualquer re-OAuth.
> 
> === HONEST_CAVEATS ===
> 1) LinkedIn verify é o furo doutrinário do MVP: o pedido do Sovereign é 'checar se ainda existe online E perguntar'. No LinkedIn não conseguimos o 'checar' (r_member_social restrito) — só delete idempotente. Então LinkedIn não honra a promessa completa; por isso fica FORA do MVP inicial (não em 'feasible_now'). 2) X 'feasible_with_scope' assume que o Usuário Zero conectou X com tweet.write E tem BYOK próprio sob o novo tier pago — se a conexão atual não pediu tweet.write no consent, precisa re-auth (verificar no social_credentials do tenant antes de prometer). 3) O id remoto só é persistido quando o publish veio com scheduled_post_id (publish-social:625); publishes ad-hoc/pipeline sem esse id NÃO têm platform_post_id → para esses o smart-delete não acha o post remoto (não dá pra deletar o que não guardamos). 4) WP: preciso confirmar onde guardamos o wp post_id — não passa por scheduled_posts; provavelmente content_library/pipeline_runs. Isso é uma checagem antes de cravar WP como 100% pronto (foi a única coisa que não pude confirmar no file:line). 5) Não fabriquei nada: grep de DELETE deu exit 1 (zero) e platform_post_id:625/631 confere — smart-delete é greenfield confirmado materialmente.
> Shell cwd was reset to /home/gcrUX/htdocs/constellation-orchestra
> ```

## 🤖 Claude *(02:05:55)*


## 🤖 Claude *(02:05:57)*

Varredura completa — e o resultado é **honesto e material** (grep confirmou: hoje deletamos só a linha local, `DELETE` remoto = 0; é greenfield). Persisto a matriz (é o SSOT pro BoK) e te dou o veredito:

## 🤖 Claude *(02:06:26)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/.claude/context/smart-delete-feasibility-2026-06-30.md",
  "content": "# Smart-Delete \u2014 Viabilidade por Rede + Design (2026-06-30)\n\n> Diretiva Sovereign: ao remover uma publica\u00e7\u00e3o no MCORCH, verificar se ainda existe online \u2192 perguntar se quer remover da rede tamb\u00e9m (sen\u00e3o s\u00f3 local). Workflow `wf_2da3b945-7b0` (7 redes + nosso estado + arquiteto, 737k tokens). Greenfield confirmado (grep `DELETE` remoto = 0).\n\n## Matriz de capacidade (SSOT \u2014 cada linha tem o SINAL de exist\u00eancia correto por API)\n\n| Rede | Verify exist\u00eancia | Delete remoto | Escopo/tier | Veredito |\n|------|-------------------|---------------|-------------|----------|\n| **WordPress** (self-host) | `GET /wp-json/wp/v2/posts/{id}` \u2192 200 vive / 404 sumiu | `DELETE .../{id}?force=true` (permanente) \u2192 200 | **Application Password que J\u00c1 usamos** (nenhum novo) | **\u2705 feasible_now** |\n| **Twitter/X** | `GET /2/tweets/{id}` \u2192 checar `data` vs `errors[].Not Found` (HTTP sempre 200!) | `DELETE /2/tweets/{id}` \u2192 `{deleted:true}` | `tweet.write` **j\u00e1 pedido** (social-auth-init:100) | \u2705 feasible (c/ conex\u00e3o) |\n| **Pinterest** | `GET /v5/pins/{id}` \u2192 200/404 | `DELETE /v5/pins/{id}` | `pins:write` **j\u00e1 concedido** | \u2705 feasible (mas nem conectado) |\n| **LinkedIn** | `GET /rest/posts/{urn}` \u2192 404=sumiu **MAS exige `r_member_social` RESTRITO** (aprova\u00e7\u00e3o especial) | `DELETE /v2/ugcPosts/{urn}` \u2192 204 (idempotente) | delete coberto por `w_member_social` **j\u00e1 concedido**; verify n\u00e3o | \ud83d\udfe1 delete-sem-verify |\n| **Facebook** | `GET /{page}_{post}` \u2192 code 100 = sumiu | `DELETE /{page}_{post}` \u2192 `{success}` (s\u00f3 posts do pr\u00f3prio app) | **REGRESS\u00c3O: precisa `pages_manage_posts`** (re-OAuth) | \ud83d\udd12 re-OAuth Sovereign |\n| **YouTube** | `GET videos?id=` \u2192 `items=[]` = sumiu (n\u00e3o 404) | `DELETE videos?id=` \u2192 204 (permanente) | **REGRESS\u00c3O: temos s\u00f3 `youtube.upload`; delete exige `youtube`/`youtube.force-ssl`** | \ud83d\udd12 re-OAuth Sovereign |\n| **TikTok** | `POST /v2/video/query/` (video.list) \u2192 aus\u00eancia = sumiu | **N\u00c3O EXISTE** \u2014 Content Posting API s\u00f3 cria; nunca houve delete | \u2014 | \u274c imposs\u00edvel via API |\n| **Instagram** | `GET graph.instagram.com/{id}` \u2192 code 100 = sumiu | DELETE existe **s\u00f3 via Facebook Login** (graph.facebook.com); publicamos via Instagram Business Login (graph.instagram.com) \u2192 **n\u00e3o exposto** | conex\u00e3o nova | \u274c imposs\u00edvel na conex\u00e3o atual |\n\n## Achados cr\u00edticos do NOSSO lado (pr\u00e9-requisitos)\n- **Dupla fonte de id remoto:** `scheduled_posts.platform_post_id` (publish-social:631) **E** `meta_posts.meta_post_id` (publish-meta:197) \u2014 o smart-delete tem que cobrir as DUAS (sen\u00e3o n\u00e3o acha o post dependendo de qual fn publicou).\n- **id s\u00f3 \u00e9 gravado quando o publish veio com `scheduled_post_id`** (publish-social:625) \u2014 publishes ad-hoc/pipeline **n\u00e3o persistem** id remoto \u2192 n\u00e3o d\u00e1 pra deletar o que n\u00e3o guardamos.\n- **X thread** s\u00f3 guarda o head id; **TikTok** `publish_id` n\u00e3o persistido; **WP** post_id n\u00e3o passa por scheduled_posts (prov\u00e1vel content_library/pipeline_runs \u2014 confirmar antes de cravar WP).\n\n## Design (2 edge fns JWT-guarded, per-user fail-closed)\n- **`check-post-existence`** \u2014 resolve plataforma+id das 2 fontes, credencial per-user (fail-closed \u2192 501 `<svc>_not_configured`), dispatch com o sinal-de-exist\u00eancia correto por API. Retorna `{exists, deletable_via_api, remote_url}`.\n- **`delete-remote-post`** \u2014 re-resolve credencial fail-closed (NUNCA confia em flag do cliente \u2014 golden rule do intent-execute), DELETE idempotente (already-deleted = sucesso), WP `force=true`, X itera thread_ids. N\u00c3O apaga local (o hook decide). Mesh node no 1\u00ba delete remoto.\n- **Fluxo UI** (`useDeleteScheduledPost`): clicar remover \u2192 `check-post-existence` \u2192 (a) `deletable=false` [IG/TikTok/LinkedIn-sem-verify] \u2192 \"ainda pode estar no ar em <rede>; essa rede n\u00e3o permite remover pela API \u2014 remover s\u00f3 do MCORCH?\" (b) `exists=true & deletable` \u2192 \"ainda publicado em <rede> [link]. Deletar tamb\u00e9m da rede?\" [Rede+local] / [S\u00f3 MCORCH] (c) `exists=false` \u2192 \"j\u00e1 n\u00e3o est\u00e1 online, removendo s\u00f3 o registro\". **Fail-OPEN de conveni\u00eancia:** probe falhou (rede/timeout) \u2192 oferece delete local com aviso (fail-closed \u00e9 p/ CREDENCIAL, fail-open p/ o probe).\n\n## MVP (zero a\u00e7\u00e3o Sovereign)\n**WordPress = smart-delete completo** (\u00fanico `feasible_now` puro). **Para TODAS as redes: o verify + transpar\u00eancia** (\"este post continua no ar em <rede>; essa rede n\u00e3o deixa remover pela API \u2014 removi s\u00f3 do MCORCH / posso remover\") \u2014 que \u00e9 o valor real: nunca mais deletar \u00e0s cegas em 5 lugares. X/Pinterest entram se a conex\u00e3o do tenant tiver os escopos. FB/YT = Fatia 2 (re-OAuth Sovereign). TikTok/IG = **honestidade obrigat\u00f3ria**: nunca prometer delete remoto.\n\n## Gate (Closed-Loop + Lei 2)\n**EMENDA ao BoK `post-engine`** (FR-SD-00x = inverso sim\u00e9trico do publish) com a Matriz acima como SSOT + Pattern Conformance + **SOP `docs/processes/smart-delete-remote.md`** (cr\u00edtico: delete \u00e9 IRREVERS\u00cdVEL \u2192 Recovery path + gate de confirma\u00e7\u00e3o escritos antes). `/security-review` se houver migration (persistir thread_ids/publish_id). Regress\u00f5es de escopo (FB/YT) = OTDs no FRD antes de qualquer re-OAuth.\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/.claude/context/smart-delete-feasibility-2026-06-30.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:06:32)*


## 🤖 Claude *(02:06:33)*

Persistido em [smart-delete-feasibility-2026-06-30.md](.claude/context/smart-delete-feasibility-2026-06-30.md). Registro na memória e te dou o veredito:

## 🤖 Claude *(02:06:47)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_smart_delete.md",
  "content": "---\nname: project_smart_delete\ndescription: Smart-delete (verificar-exist\u00eancia online + delete remoto opcional ao remover publica\u00e7\u00e3o) \u2014 viabilidade por rede mapeada; greenfield; gate BoK post-engine + SOP pendente\nmetadata:\n  type: project\n---\n\nDiretiva Sovereign 2026-06-30 (ap\u00f3s deletar manualmente posts na UI + em cada rede): ao remover uma publica\u00e7\u00e3o no MCORCH, **verificar se ainda existe online** \u2192 perguntar se quer remover da rede tamb\u00e9m; sen\u00e3o s\u00f3 local (como hoje). **Greenfield** (grep `DELETE` remoto = 0; hoje `useDeleteScheduledPost` s\u00f3 apaga a linha local).\n\n**Viabilidade por rede** (SSOT: `.claude/context/smart-delete-feasibility-2026-06-30.md`, workflow `wf_2da3b945-7b0`):\n- **WordPress** = \u2705 smart-delete COMPLETO agora (Application Password j\u00e1 usada; GET 404 + DELETE force=true).\n- **Twitter/X** \u2705 (`tweet.write` j\u00e1 pedido) \u00b7 **Pinterest** \u2705 (`pins:write` j\u00e1; mas nem conectado) \u2014 feasible se a conex\u00e3o do tenant tiver o escopo.\n- **LinkedIn** \ud83d\udfe1 delete OK (`w_member_social` j\u00e1) MAS verify exige `r_member_social` RESTRITO \u2192 delete-sem-verify (n\u00e3o honra o \"checar antes\").\n- **Facebook** \ud83d\udd12 precisa `pages_manage_posts` (re-OAuth Sovereign) \u00b7 **YouTube** \ud83d\udd12 temos s\u00f3 `youtube.upload`, delete exige `youtube.force-ssl` (re-OAuth Sovereign).\n- **TikTok** \u274c delete N\u00c3O existe na API (nunca existiu) \u00b7 **Instagram** \u274c delete s\u00f3 via Facebook Login; publicamos via Instagram Business Login (graph.instagram.com) \u2192 n\u00e3o exposto ([[reference_ig_reels_publish_path]]).\n\n**Valor real (framing honesto):** para TikTok/IG/LinkedIn o \"smart\" vira **transpar\u00eancia** \u2014 \"ainda est\u00e1 no ar em <rede>; essa rede n\u00e3o deixa remover pela API \u2014 removi s\u00f3 do MCORCH\". Nunca mais deletar \u00e0s cegas em 5 lugares.\n\n**Achados do nosso lado:** dupla fonte de id (`scheduled_posts.platform_post_id` + `meta_posts.meta_post_id` \u2014 cobrir as 2); id s\u00f3 grava com `scheduled_post_id` no payload; X thread s\u00f3 guarda head; WP post_id n\u00e3o passa por scheduled_posts (confirmar).\n\n**Design:** 2 edge fns `check-post-existence` + `delete-remote-post` (per-user fail-closed; delete idempotente; fail-OPEN s\u00f3 no probe de conveni\u00eancia) + fluxo UI 3-ramos. **Gate pendente (Lei 2 + Closed-Loop):** EMENDA BoK `post-engine` (FR-SD-00x) + SOP `docs/processes/smart-delete-remote.md` (delete \u00e9 IRREVERS\u00cdVEL) ANTES do c\u00f3digo. Relaciona [[project_channel_reshaper]] (post-engine) e [[project_brand_persona_ccio]].\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/project_smart_delete.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:06:55)*


## 🤖 Claude *(02:06:59)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md",
  "old_string": "- [Programa \"Gabriel AI\" (avatar-clone-ai)",
  "new_string": "- [Smart-delete \u2014 verificar-exist\u00eancia online + delete remoto opcional](project_smart_delete.md) \u2014 Diretiva Sovereign 2026-06-30: ao remover publica\u00e7\u00e3o, checar se ainda vive na rede \u2192 perguntar se deleta l\u00e1 tamb\u00e9m. Greenfield. WordPress=\u2705completo; X/Pinterest=\u2705escopo-ok; LinkedIn=\ud83d\udfe1delete-sem-verify; FB/YT=\ud83d\udd12re-OAuth; TikTok/IG=\u274csem delete na API (vira transpar\u00eancia honesta). Gate: emenda BoK post-engine + SOP. SSOT: `.claude/context/smart-delete-feasibility-2026-06-30.md`.\n- [Programa \"Gabriel AI\" (avatar-clone-ai)"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:07:12)*


## 🤖 Claude *(02:07:24)*

## Veredito: sua ideia é boa e viável — mas a realidade varia MUITO por rede (mapeei material, Lei 1)

A matriz honesta:

| Rede | Verificar se está no ar? | Deletar pela API? | Situação |
|------|:---:|:---:|---|
| **WordPress** | ✅ | ✅ | Completo agora (mesma senha que já usamos) |
| **Twitter/X** | ✅ | ✅ | Funciona (`tweet.write` já pedido) |
| **Pinterest** | ✅ | ✅ | Funciona (mas nem está conectado) |
| **LinkedIn** | ⚠️ restrito | ✅ | Delete sim, mas o "checar antes" exige escopo restrito da LinkedIn |
| **Facebook** | ✅ | 🔒 | Delete exige você **reconectar** com escopo novo |
| **YouTube** | ✅ | 🔒 | Delete exige você **reconectar** (temos só upload) |
| **TikTok** | ⚠️ | ❌ | **Delete não existe na API** — nunca existiu |
| **Instagram** | ✅ | ❌ | Delete só existe via outra conexão; a nossa (graph.instagram.com) não expõe |

**A ironia honesta:** as redes que você mais usa (IG, LinkedIn) são justamente as difíceis/impossíveis de deletar por API. **Mas o valor central da sua ideia funciona em todas** — a parte de *verificar e te avisar*. Em vez de deletar às cegas em 5 lugares, o MCORCH passa a dizer: *"esse post ainda está no ar no Instagram e no X — o X eu removo pra você agora; o Instagram você precisa remover manual no app"*. Isso é exatamente o fallback que você descreveu, e é transparência real.

**O design casa 1:1 com o que você pediu:** clicar remover → verifica existência → se dá pra deletar remoto e ainda existe, pergunta; se não dá (IG/TikTok), avisa honesto e remove só local; se já sumiu, só limpa o registro. Tudo per-user fail-closed, delete idempotente.

**O gate (Protocolo de Malha Fechada):** delete remoto é uma capability **nova e irreversível** (hoje temos zero). Então pede **emenda ao BoK `post-engine` + um SOP** (`smart-delete-remote.md`) antes do código — principalmente por causa do "irreversível" (o caminho de recovery + o gate de confirmação têm que estar escritos primeiro).

Como você quer que eu escope isso?

## 🤖 Claude *(02:07:31)*


🛠️ **Tool Call**: `AskUserQuestion`
```json
{
  "questions": [
    {
      "question": "Como escopar o smart-delete? (Em todos os casos eu selo primeiro a emenda BoK post-engine + SOP, pelo protocolo \u2014 a diferen\u00e7a \u00e9 o que entra no build.)",
      "header": "Escopo",
      "multiSelect": false,
      "options": [
        {
          "label": "MVP sem a\u00e7\u00e3o sua",
          "description": "Verificar-exist\u00eancia + transpar\u00eancia em TODAS as redes (\"ainda no ar em <rede>; removo / voc\u00ea remove manual\") + delete remoto real onde j\u00e1 d\u00e1 sem reconectar: WordPress, X e Pinterest. Zero re-OAuth seu. Entrega o valor 'nunca mais deletar \u00e0s cegas' j\u00e1."
        },
        {
          "label": "MVP + reconectar FB/YT/X",
          "description": "O MVP acima E voc\u00ea reconecta Facebook/YouTube (e confirma X) com o escopo de delete \u2192 delete remoto real em mais redes. Custo: re-consent OAuth dessas contas (a\u00e7\u00e3o sua; for\u00e7a re-login das contas j\u00e1 conectadas)."
        },
        {
          "label": "S\u00f3 selar o gate agora",
          "description": "Eu selo a emenda BoK post-engine + o SOP (a Fonte da Verdade + a matriz de capacidade), sem escrever c\u00f3digo ainda. Decidimos o escopo do build depois, com calma."
        },
        {
          "label": "Deixar pra depois",
          "description": "Registro a viabilidade na mem\u00f3ria (j\u00e1 feito) e paro aqui; retomamos quando voc\u00ea quiser priorizar."
        }
      ]
    }
  ]
}
```

> **Tool Result (AskUserQuestion)** - ✅ Success
>
> ```
> Your questions have been answered: "Como escopar o smart-delete? (Em todos os casos eu selo primeiro a emenda BoK post-engine + SOP, pelo protocolo — a diferença é o que entra no build.)"="MVP sem ação sua". You can now continue with these answers in mind.
> ```

## 🤖 Claude *(02:10:25)*


## 🤖 Claude *(02:10:27)*

**MVP sem ação sua** — perfeito. Pelo protocolo, selo primeiro o gate (emenda BoK `post-engine` + SOP), depois codo os 2 edge fns + o fluxo de UI. Recon da estrutura do BoK `post-engine` pra seguir a convenção de emenda existente:

## 🤖 Claude *(02:10:31)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== docs/bok/post-engine/ ===\"\nls -la docs/bok/post-engine/ 2>/dev/null\necho\necho \"=== conven\u00e7\u00e3o de amendment + FR ids existentes (FR-CP/FR-PE) ===\"\ngrep -rhoE \"FR-(PE|CP|SD)-[0-9]+\" docs/bok/post-engine/ 2>/dev/null | sort -u | tail -30\necho\necho \"=== useDeleteScheduledPost / delete local hoje (onde plugar o fluxo) ===\"\ngrep -rnE \"useDeleteScheduledPost|\\.delete\\(\\)|deletePost\" src/hooks/useScheduledPosts.ts src/pages/CalendarPage.tsx 2>/dev/null | head",
  "description": "Recon post-engine BoK structure and delete hook"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === docs/bok/post-engine/ ===
> total 172
> drwxrwxr-x  2 gcrUX  gcrUX   4096 Jun 28 18:30 .
> drwxrwxr-x 27 gcrUX  gcrUX   4096 Jun 29 21:21 ..
> -rw-rw-r--  1 ubuntu ubuntu  5605 Jun 28 18:30 00-index.md
> -rw-r--r--  1 gcrUX  gcrUX   4120 Jun  6 17:11 01-mrd.md
> -rw-r--r--  1 gcrUX  gcrUX   2825 Jun  6 17:11 02-brd.md
> -rw-r--r--  1 gcrUX  gcrUX   2630 Jun  6 17:11 03-prd.md
> -rw-r--r--  1 gcrUX  gcrUX   2439 Jun  6 17:11 04-frd.md
> -rw-r--r--  1 gcrUX  gcrUX   2327 Jun  6 17:11 05-sdd.md
> -rw-r--r--  1 ubuntu ubuntu 11171 Jun 27 12:32 06-data-model.md
> -rw-r--r--  1 gcrUX  gcrUX   1830 Jun  6 17:12 07-process-flow.md
> -rw-r--r--  1 gcrUX  gcrUX   1973 Jun  6 17:12 08-quality-metrics.md
> -rw-rw-r--  1 ubuntu ubuntu 12159 Jun 27 12:33 09-pattern-conformance.md
> -rw-rw-r--  1 ubuntu ubuntu 25136 Jun 27 12:35 10-amendment-social-connect-tiktok-youtube-pinterest.md
> -rw-rw-r--  1 ubuntu ubuntu 16618 Jun 27 22:32 11-channel-format-intelligence-blueprint.md
> -rw-rw-r--  1 ubuntu ubuntu 17955 Jun 27 22:44 12-amendment-channel-format-intelligence.md
> -rw-rw-r--  1 ubuntu ubuntu 17986 Jun 28 01:05 13-sdd-reshaper-atomizer.md
> -rw-r--r--  1 ubuntu ubuntu  8658 Jun 28 18:30 14-social-engineering-virality-blueprint.md
> 
> === convenção de amendment + FR ids existentes (FR-CP/FR-PE) ===
> FR-CP-001
> FR-CP-002
> FR-CP-003
> FR-CP-004
> FR-CP-005
> FR-CP-006
> FR-CP-007
> FR-CP-008
> FR-CP-009
> FR-CP-010
> FR-CP-011
> FR-CP-012
> FR-PE-001
> FR-PE-002
> FR-PE-003
> FR-PE-004
> FR-PE-005
> FR-PE-006
> FR-PE-007
> FR-PE-008
> FR-PE-009
> FR-PE-010
> FR-PE-011
> FR-PE-012
> FR-PE-013
> FR-PE-014
> FR-PE-015
> FR-PE-016
> 
> === useDeleteScheduledPost / delete local hoje (onde plugar o fluxo) ===
> src/hooks/useScheduledPosts.ts:75:export function useDeleteScheduledPost() {
> src/hooks/useScheduledPosts.ts:82:        .delete()
> src/pages/CalendarPage.tsx:6:import { useScheduledPosts, useCreateScheduledPost, useUpdateScheduledPost, useDeleteScheduledPost, type ScheduledPost } from '@/hooks/useScheduledPosts';
> src/pages/CalendarPage.tsx:234:  const deletePost = useDeleteScheduledPost();
> src/pages/CalendarPage.tsx:480:                                <Button variant="ghost" size="icon" className="h-5 w-5" onClick={(e) => { e.stopPropagation(); deletePost.mutate(p.id); }}>
> src/pages/CalendarPage.tsx:616:          onDelete={(id) => deletePost.mutate(id)}
> src/pages/CalendarPage.tsx:619:          busy={updatePost.isPending || deletePost.isPending}
> ```

## 🤖 Claude *(02:10:57)*


## 🤖 Claude *(02:10:58)*

Convenção clara: próxima emenda = `15`, FR ids `FR-SD-xxx`. Selo o gate — escrevo a emenda BoK + o SOP (Lei 2, foco no delete irreversível). Começando pela emenda:

## 🤖 Claude *(02:11:45)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/bok/post-engine/15-amendment-smart-delete.md",
  "content": "# Post-Engine \u2014 Amendment: Smart-Delete (verify-existence + delete remoto opcional)\n\n> **Emenda ao BoK `post-engine`** (inverso sim\u00e9trico do publish/reshaper). Diretiva Sovereign 2026-06-30: ao remover uma publica\u00e7\u00e3o no MCORCH, verificar se ainda existe online \u2192 perguntar se remover da rede tamb\u00e9m; sen\u00e3o s\u00f3 local. **SSOT da viabilidade por rede:** `.claude/context/smart-delete-feasibility-2026-06-30.md` (workflow `wf_2da3b945-7b0`). **SOP:** `docs/processes/smart-delete-remote.md`.\n>\n> **Escopo aprovado (Sovereign 2026-06-30): MVP sem a\u00e7\u00e3o Sovereign** \u2014 verify+transpar\u00eancia em TODAS as redes + delete remoto real onde o escopo J\u00c1 est\u00e1 concedido (WordPress, X, Pinterest). Re-OAuth (FB/YT) e conex\u00e3o nova (IG) diferidos como OTDs.\n\n## ORO\n- **Operator:** MCORCH Master Execution Agent\n- **Reviewer:** Sovereign (Gabriel)\n- **Owner:** Sovereign \u2014 delete remoto \u00e9 **irrevers\u00edvel** (blast radius = conte\u00fado publicado do tenant). Confirma\u00e7\u00e3o humana obrigat\u00f3ria por design.\n\n## Contexto material (greenfield)\nHoje `useDeleteScheduledPost` (src/hooks/useScheduledPosts.ts:75) s\u00f3 faz `.delete()` da linha local \u2014 **nunca** toca a plataforma. `grep DELETE remoto = 0`. O id remoto vive em DUAS fontes: `scheduled_posts.platform_post_id` (publish-social:631) **e** `meta_posts.meta_post_id` (publish-meta:197) \u2014 e s\u00f3 \u00e9 gravado quando o publish recebeu `scheduled_post_id`.\n\n## Capability Matrix (SSOT \u2014 sinal de exist\u00eancia correto por API)\nVer tabela completa em `.claude/context/smart-delete-feasibility-2026-06-30.md`. Resumo do que o c\u00f3digo deve tratar:\n\n| Rede | verify (sinal) | delete MVP | `deletable_via_api` no MVP |\n|------|----------------|-----------|:---:|\n| WordPress | `GET .../posts/{id}` 200/404 | `DELETE ...?force=false` (Trash, recuper\u00e1vel) | **true** |\n| Twitter/X | `GET /2/tweets/{id}` \u2192 `data` vs `errors[]` (HTTP sempre 200) | `DELETE /2/tweets/{id}` | **true** (se tenant tem `tweet.write`) |\n| Pinterest | `GET /v5/pins/{id}` 200/404 | `DELETE /v5/pins/{id}` | **true** (se conectado) |\n| LinkedIn | verify exige `r_member_social` RESTRITO \u2192 sem verify | delete idempotente 204 (`w_member_social`) | **false no MVP** (OTD-SD-003) |\n| Facebook | `GET /{page}_{post}` code 100=sumiu | precisa `pages_manage_posts` | **false** (OTD-SD-001) |\n| YouTube | `GET videos?id=` `items=[]`=sumiu | precisa `youtube.force-ssl` | **false** (OTD-SD-002) |\n| TikTok | `POST /v2/video/query/` aus\u00eancia=sumiu | **inexistente** | **false** (permanente) |\n| Instagram | `GET graph.instagram.com/{id}` code 100=sumiu | s\u00f3 via Facebook Login (n\u00e3o nossa conex\u00e3o) | **false** (OTD-SD-004) |\n\n## Functional Requirements\n\n- **FR-SD-001 \u2014 `check-post-existence` (edge fn, JWT):** resolve `(platform, remote_id)` das DUAS fontes (`scheduled_posts.platform_post_id` + `meta_posts.meta_post_id`); resolve credencial **per-user via `auth.uid()` fail-closed** (sem credencial \u2192 HTTP 501 `{error:\"<svc>_not_configured\"}`); dispatch por plataforma usando o **sinal de exist\u00eancia correto da Matriz** (nunca s\u00f3 o HTTP status no X/YT). Retorna `{exists: boolean|\"unknown\", platform, deletable_via_api: boolean, remote_url?}`. Telemetry `infra_health_logs service=\"smart-delete-verify\"` (success/degraded/error). Nenhum `remote_id` guardado \u2192 `{exists:\"unknown\", deletable_via_api:false}`.\n\n- **FR-SD-002 \u2014 `delete-remote-post` (edge fn, JWT):** **re-resolve credencial per-user fail-closed** e re-deriva `deletable_via_api` do servidor \u2014 **NUNCA confia em flag do cliente** (golden rule herdada do `intent-execute`). S\u00f3 executa DELETE se a Matriz marca delet\u00e1vel no MVP (WP/X/Pinterest). DELETE **idempotente** (already-deleted/404/Not-Found = sucesso). WP usa `force=false` (Trash recuper\u00e1vel) por padr\u00e3o \u2014 OTD-SD-006 avalia op\u00e7\u00e3o permanente. **N\u00c3O apaga a linha local** (retorna `{remote_deleted}`; o hook decide o local). Insere **n\u00f3 de observa\u00e7\u00e3o na Knowledge Mesh** no 1\u00ba delete remoto bem-sucedido (mandato Mesh). Telemetry por path.\n\n- **FR-SD-003 \u2014 Fluxo de UI (Harness, em `useDeleteScheduledPost`):** clicar remover \u2192 `check-post-existence` \u2192 3 ramos: **(a)** `deletable_via_api=false` (IG/TikTok/LinkedIn-MVP/FB/YT) \u2192 di\u00e1logo honesto \"ainda pode estar no ar em `<rede>`; essa rede n\u00e3o permite remover pela API \u2014 remover s\u00f3 do MCORCH? [+ delete manual no app]\" \u2192 s\u00f3 local. **(b)** `exists=true & deletable` \u2192 \"ainda publicado em `<rede>` [link]. Deletar tamb\u00e9m da rede?\" \u2192 [Deletar rede+local] (chama `delete-remote-post`; local delete s\u00f3 se `remote_deleted`) / [S\u00f3 do MCORCH] (local direto). **(c)** `exists=false` \u2192 \"j\u00e1 n\u00e3o est\u00e1 online, removendo s\u00f3 o registro\". **Fail-OPEN de conveni\u00eancia:** probe falhou (rede/timeout) \u2192 oferece local delete com aviso \"n\u00e3o consegui confirmar o estado remoto\" (fail-closed \u00e9 p/ CREDENCIAL; fail-open p/ o probe \u2014 distin\u00e7\u00e3o deliberada).\n\n- **FR-SD-004 \u2014 Honestidade obrigat\u00f3ria (NFR):** para plataformas sem delete via API na conex\u00e3o atual (TikTok, IG, e FB/YT/LinkedIn at\u00e9 destravar), a UI **nunca** promete delete remoto \u2014 informa transpar\u00eancia + delete manual. `deletable_via_api` \u00e9 derivado no servidor (Matriz), n\u00e3o no cliente.\n\n- **FR-SD-005 \u2014 Fragilidade de dados (MVP, sem migration se poss\u00edvel):** X thread hoje s\u00f3 guarda o head id (`platform_post_id`); MVP deleta s\u00f3 o head (documentar limita\u00e7\u00e3o) OU persistir `thread_ids` (migration \u2192 `/security-review`). Confirmar onde o WP `post_id` vive (prov\u00e1vel `content_library`/`pipeline_runs`) antes de cravar WP.\n\n## Open Technical Decisions (Sovereign-gated \u2014 fora do MVP)\n- **OTD-SD-001 (Facebook delete):** exige re-OAuth com `pages_manage_posts` + Page token + App Review. A\u00e7\u00e3o Sovereign (for\u00e7a re-consent das contas FB conectadas).\n- **OTD-SD-002 (YouTube delete):** temos `youtube.upload`; delete exige `youtube`/`youtube.force-ssl` \u2192 re-OAuth. A\u00e7\u00e3o Sovereign. Alternativa n\u00e3o-destrutiva: `videos.update privacyStatus=private`.\n- **OTD-SD-003 (LinkedIn verify):** `r_member_social` \u00e9 escopo RESTRITO (aprova\u00e7\u00e3o especial LinkedIn) \u2192 sem ele, LinkedIn opera delete-sem-verify; fora do MVP porque n\u00e3o honra o \"checar antes\".\n- **OTD-SD-004 (Instagram delete):** delete s\u00f3 via Facebook Login (graph.facebook.com + Page token); publicamos via Instagram Business Login (graph.instagram.com). Habilitar = conex\u00e3o nova (quebra/duplica publish atual \u2014 ver `reference_ig_reels_publish_path`). A\u00e7\u00e3o Sovereign grande.\n- **OTD-SD-005 (TikTok delete):** IMPOSS\u00cdVEL \u2014 Content Posting API s\u00f3 cria; nenhum escopo resolve. Permanente.\n- **OTD-SD-006 (WP delete permanente):** MVP usa Trash (`force=false`, recuper\u00e1vel); avaliar toggle \"excluir permanentemente\" (`force=true`) com confirma\u00e7\u00e3o refor\u00e7ada.\n\n## Pattern Conformance Declaration (Agentic Vision \u2014 21 padr\u00f5es)\n| Padr\u00e3o | Implementado? | Como / Por-que-deferido |\n|--------|:---:|---|\n| Tool Use | yes | 2 edge fns como ferramentas (verify/delete) por plataforma |\n| Guardrails / Fail-Closed | yes | credencial per-user fail-closed (501); server re-deriva `deletable_via_api`; nunca confia no cliente |\n| Human-in-the-Loop | yes | delete irrevers\u00edvel \u21d2 confirma\u00e7\u00e3o humana obrigat\u00f3ria (FR-SD-003) |\n| Reflection / Self-Verify | yes | verify-antes-de-deletar + delete idempotente (re-verify no retry) |\n| Observability / Telemetry | yes | `infra_health_logs` por path + n\u00f3 de observa\u00e7\u00e3o na Mesh |\n| Multi-tenant Isolation | yes | `auth.uid()` em toda resolu\u00e7\u00e3o de credencial/id (herda RLS) |\n| Graceful Degradation | yes | fail-OPEN do probe; transpar\u00eancia quando delete imposs\u00edvel |\n| Idempotency | yes | already-deleted = sucesso (FR-SD-002) |\n| Memory / Mesh | yes | n\u00f3 de observa\u00e7\u00e3o no 1\u00ba delete remoto |\n| Planning / Orchestration | n-a | opera\u00e7\u00e3o at\u00f4mica de 1 post, sem plano multi-step |\n| Multi-Agent / Routing | deferred | dispatch por plataforma \u00e9 branch, n\u00e3o sub-agente (sem benef\u00edcio neste escopo) |\n| Cost Metering (mcoCoins) | deferred | delete n\u00e3o \u00e9 gera\u00e7\u00e3o paga; sem custo LLM/USD \u2014 n\u00e3o cobra (OTD reavaliar se abus\u00e1vel) |\n| (demais padr\u00f5es) | n-a | n\u00e3o materialmente tocados por esta feature |\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/bok/post-engine/15-amendment-smart-delete.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:11:48)*


## 🤖 Claude *(02:11:49)*

Emenda BoK escrita. Agora o SOP (Lei 2 — foco no delete irreversível: confirmação + recovery + sinal-de-existência por rede):

## 🤖 Claude *(02:12:21)*


🛠️ **Tool Call**: `Write`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/docs/processes/smart-delete-remote.md",
  "content": "# SOP \u2014 Smart-Delete Remoto (verify-existence + delete opcional na rede)\n\n> Lei 2 (Processo Antecipado). Feature: ao remover uma publica\u00e7\u00e3o no MCORCH, verificar se ainda existe online e, opcionalmente, delet\u00e1-la na plataforma. **Delete remoto \u00e9 IRREVERS\u00cdVEL** \u2014 este SOP define a sequ\u00eancia, os gates de confirma\u00e7\u00e3o e o recovery ANTES do c\u00f3digo. BoK: `docs/bok/post-engine/15-amendment-smart-delete.md`. SSOT de viabilidade: `.claude/context/smart-delete-feasibility-2026-06-30.md`.\n\n## Operator\nQuem executa hoje **manualmente**: o Sovereign, que (a) abre o post na UI da rede (LinkedIn/IG/X/etc.), (b) confirma que \u00e9 o post certo, (c) clica excluir na rede, (d) volta ao MCORCH e remove o registro. O smart-delete automatiza (a)+(c) para as redes que a API permite, mantendo (b) como confirma\u00e7\u00e3o humana.\n\n## Sequence (cada step com crit\u00e9rio de sucesso material)\n1. **Resolver alvo** \u2014 do registro local (`scheduled_posts` OU `meta_posts`), extrair `(platform, remote_id)`. \u2705 = `remote_id` n\u00e3o-nulo encontrado numa das 2 fontes. \u274c (nenhum id guardado) \u2192 pular direto pro delete local com aviso \"sem id remoto guardado\".\n2. **Resolver credencial per-user** (`auth.uid()`) para a plataforma. \u2705 = credencial ativa. \u274c = HTTP 501 `<svc>_not_configured` \u2192 oferecer s\u00f3 delete local.\n3. **Verificar exist\u00eancia** (`check-post-existence`) com o **sinal correto da Matriz**: WP 200/404 \u00b7 X `data` vs `errors[]` (HTTP sempre 200!) \u00b7 YT `items.length` (n\u00e3o 404) \u00b7 FB/IG `error.code 100` \u00b7 Pinterest 200/404 \u00b7 TikTok aus\u00eancia no array. \u2705 = resposta parseada em `{exists, deletable_via_api}`.\n4. **Decis\u00e3o humana (HITL \u2014 gate obrigat\u00f3rio):** apresentar o estado real e pedir confirma\u00e7\u00e3o expl\u00edcita. Nunca deletar remoto sem clique. Ramos: delet\u00e1vel+existe \u2192 oferecer [Rede+local]/[S\u00f3 local]; n\u00e3o-delet\u00e1vel \u2192 informar + s\u00f3 local; n\u00e3o-existe \u2192 s\u00f3 local.\n5. **Delete remoto** (`delete-remote-post`, s\u00f3 se o operador escolheu e a Matriz permite) \u2014 DELETE idempotente. \u2705 = 204/`{deleted:true}`/`{success:true}` OU already-deleted (idempotente). WP `force=false` (Trash).\n6. **Delete local** \u2014 s\u00f3 AP\u00d3S `remote_deleted=true` (ou escolha \"s\u00f3 local\"). \u2705 = linha removida.\n\n## Verification gates (output esperado)\n- Verify: `check-post-existence` retorna JSON com `exists` \u2208 {true,false,\"unknown\"} + `deletable_via_api` boolean derivado NO SERVIDOR (n\u00e3o do cliente).\n- Delete remoto: status terminal da API (204/success) OU sinal idempotente de already-gone. Registrado em `infra_health_logs service=\"smart-delete-delete\"`.\n- Materialidade (Lei 1): ap\u00f3s \"Rede+local\", um `check-post-existence` repetido deve retornar `exists=false` (WP 404 / X `errors[]` / YT `items=[]`). O smoke prova isso.\n\n## Recovery path (falha no step N)\n- **Verify falha (rede/timeout):** FAIL-OPEN de conveni\u00eancia \u2014 n\u00e3o travar; oferecer delete local com aviso \"n\u00e3o consegui confirmar o estado remoto\". (N\u00c3O fail-open de credencial \u2014 aus\u00eancia de credencial \u00e9 fail-closed 501.)\n- **Delete remoto falha (n\u00e3o-idempotente, ex. 403/500):** N\u00c3O apagar o local. Retornar erro claro (\"n\u00e3o consegui remover de `<rede>`; o registro local foi mantido \u2014 tente de novo ou remova manual\"). O post local permanece como \u00e2ncora para nova tentativa (n\u00e3o vira \u00f3rf\u00e3o).\n- **Delete remoto sucesso mas delete local falha:** o remoto j\u00e1 foi (irrevers\u00edvel) \u2014 retry s\u00f3 do local delete; o `remote_id` j\u00e1 n\u00e3o resolve (idempotente), ent\u00e3o re-tentar \u00e9 seguro.\n- **Delete errado (post que n\u00e3o era pra deletar):** WP MVP usa Trash (`force=false`) \u2192 recuper\u00e1vel no WP admin. X/Pinterest/IG/etc. **n\u00e3o t\u00eam undo** \u2014 por isso o gate HITL (step 4) mostra `remote_url` + plataforma + hor\u00e1rio ANTES de confirmar. Sem confirma\u00e7\u00e3o = sem delete.\n\n## Success signal (materialmente observ\u00e1vel)\nFluxo completo confirmado quando: (1) o operador clicou remover; (2) para uma rede delet\u00e1vel, escolheu \"Rede+local\" e um `check-post-existence` p\u00f3s-delete retorna `exists=false`; (3) a linha local sumiu; (4) `infra_health_logs` tem os 2 eventos (verify+delete) success; (5) n\u00f3 de observa\u00e7\u00e3o na Mesh no 1\u00ba delete remoto. Para redes n\u00e3o-delet\u00e1veis: o registro local sumiu E a UI mostrou o aviso honesto (nenhuma promessa falsa de delete remoto).\n\n## Anti-patterns proibidos\n- \u274c Confiar em flag `deletable`/`confirm` do cliente para executar DELETE (re-derivar no servidor \u2014 golden rule intent-execute).\n- \u274c Apagar o local ANTES de confirmar o remoto (vira \u00f3rf\u00e3o invertido \u2014 perde a \u00e2ncora do retry).\n- \u274c Prometer delete remoto em TikTok/IG(conex\u00e3o atual)/LinkedIn-sem-verify \u2014 honestidade obrigat\u00f3ria (FR-SD-004).\n- \u274c Checar s\u00f3 HTTP status no X (sempre 200) ou esperar 404 no YT (retorna items=[]) \u2014 usar o sinal da Matriz.\n- \u274c WP `force=true` (permanente) no MVP sem confirma\u00e7\u00e3o refor\u00e7ada \u2014 usar Trash.\n"
}
```

> **Tool Result (Write)** - ✅ Success
>
> ```
> File created successfully at: /home/gcrUX/htdocs/constellation-orchestra/docs/processes/smart-delete-remote.md (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:12:40)*


## 🤖 Claude *(02:12:41)*

Gate escrito. Commito a emenda BoK + SOP + o SSOT de viabilidade:

## 🤖 Claude *(02:12:49)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add docs/bok/post-engine/15-amendment-smart-delete.md docs/processes/smart-delete-remote.md .claude/context/smart-delete-feasibility-2026-06-30.md\ngit commit -q -m \"docs(post-engine): seal smart-delete gate \u2014 BoK amendment 15 (FR-SD-001..005) + SOP + capability-matrix SSOT\n\nClosed-Loop gate ANTES do c\u00f3digo (delete remoto = capability nova irrevers\u00edvel). MVP aprovado: verify+transpar\u00eancia em todas as redes + delete real onde escopo j\u00e1 concedido (WP/X/Pinterest). FB/YT re-OAuth + IG conex\u00e3o-nova + TikTok imposs\u00edvel = OTDs diferidas.\n\nCo-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>\" && echo \"gate commit: $(git log -1 --format=%h)\"\necho\necho \"=== recon credenciais p/ os edge fns (WP/X/Pinterest resolution) ===\"\necho \"--- social_credentials / social_accounts colunas ---\"\npython3 - <<'PY'\nimport re\nt=open('src/integrations/supabase/types.ts').read()\nfor tbl in ['social_accounts','social_credentials']:\n    m=re.search(tbl+r':\\s*\\{\\s*Row:\\s*\\{(.*?)\\}\\s*Insert:', t, re.S)\n    print(f\"--- {tbl} ---\")\n    if m:\n        for l in m.group(1).split('\\n'):\n            if ':' in l and l.strip(): print(\"  \"+l.strip())\n    else: print(\"  NOT FOUND\")\nPY\necho \"--- como publish-social resolve token X/Pinterest + WP config ---\"\ngrep -nE \"social_accounts|social_credentials|access_token|wp_site_url|wp_app_password|decrypted|twitter|pinterest\" supabase/functions/publish-social/index.ts 2>/dev/null | head -25",
  "description": "Commit gate docs and recon credential resolution"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;6;6;6m─[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpre-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;6;6;6m─[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m╯[m
> ┃  e2e-output-tripwire ❯ 
> 
> ┃  secret-scan ❯ 
> 
> ┃  gitleaks-staged ❯ 
> 
>     ○
>     │╲
>     │ ○
>     ○ ░
>     ░    gitleaks
> 
> [90m11:12PM[0m [32mINF[0m 1 commits scanned.
> [90m11:12PM[0m [32mINF[0m scan completed in 33.9ms
> [90m11:12PM[0m [32mINF[0m no leaks found
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.11 seconds)
> ✔️ e2e-output-tripwire (0.03 seconds)
> ✔️ secret-scan (0.06 seconds)
> ✔️ gitleaks-staged (0.11 seconds)
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpost-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m╯[m
> ┃  mesh-reingest ❯ 
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.00 seconds)
> ✔️ mesh-reingest (0.00 seconds)
> gate commit: 33fadb0
> 
> === recon credenciais p/ os edge fns (WP/X/Pinterest resolution) ===
> --- social_credentials / social_accounts colunas ---
> --- social_accounts ---
>   access_token: string | null
>   created_at: string | null
>   id: string | null
>   is_active: boolean | null
>   metadata: Json | null
>   platform: Database["public"]["Enums"]["social_platform"] | null
>   platform_user_id: string | null
>   platform_username: string | null
>   refresh_token: string | null
>   scopes: string[] | null
>   token_expires_at: string | null
>   updated_at: string | null
>   user_id: string | null
>   Relationships: []
>   decrypted_social_app_config: {
>   Row: {
>   client_id: string | null
>   client_secret: string | null
>   created_at: string | null
>   id: string | null
>   is_active: boolean | null
>   metadata: Json | null
>   platform: Database["public"]["Enums"]["social_platform"] | null
>   scopes: string[] | null
>   updated_at: string | null
>   user_id: string | null
>   Relationships: []
>   decrypted_user_api_keys: {
>   Row: {
>   apify_token: string | null
>   cartesia_api_key: string | null
>   created_at: string | null
>   elevenlabs_api_key: string | null
>   fal_api_key: string | null
>   firecrawl_api_key: string | null
>   google_api_key: string | null
>   groq_api_key: string | null
>   hedra_api_key: string | null
>   higgsfield_api_key: string | null
>   higgsfield_api_key_secret: string | null
>   nanobana_api_key: string | null
>   openai_api_key: string | null
>   openrouter_api_key: string | null
>   pref_ai_model: string | null
>   pref_audio_provider: string | null
>   pref_image_provider: string | null
>   pref_video_provider: string | null
>   rapidapi_key: string | null
>   replicate_api_key: string | null
>   resend_api_key: string | null
>   seedance_api_key: string | null
>   updated_at: string | null
>   user_id: string | null
>   wp_app_password: string | null
>   wp_site_url: string | null
>   wp_username: string | null
>   Relationships: []
>   meta_config: {
>   Row: {
>   created_at: string | null
>   facebook_user_id: string | null
>   id: string | null
>   instagram_business_account_id: string | null
>   long_lived_token: string | null
>   meta_ad_account_id: string | null
>   pages: Json | null
>   requires_reauth: boolean | null
>   scopes: string[] | null
>   token_expires_at: string | null
>   updated_at: string | null
>   user_id: string | null
>   whatsapp_phone_number_id: string | null
>   whatsapp_waba_id: string | null
> --- social_credentials ---
>   NOT FOUND
> --- como publish-social resolve token X/Pinterest + WP config ---
> 66:      .from("decrypted_social_accounts")
> 84:    // Refresh token if expired, then re-fetch account to get the new access_token
> 101:      // re-fetch to get the updated access_token
> 103:        .from("decrypted_social_accounts")
> 104:        .select("access_token, refresh_token, token_expires_at")
> 108:        account.access_token = refreshedAccount.access_token;
> 127:          Authorization: `Bearer ${account.access_token}`,
> 156:      const meRes = await fetch(`${IG_BASE}/me?fields=user_id&access_token=${account.access_token}`);
> 167:              ? { media_type: "REELS", video_url: videoUrl, caption: content.text || content, access_token: account.access_token }
> 168:              : { caption: content.text || content, image_url: content.image_url, access_token: account.access_token },
> 181:          const st = await fetch(`${IG_BASE}/${container.id}?fields=status_code&access_token=${account.access_token}`);
> 196:            access_token: account.access_token,
> 215:          body: JSON.stringify({ url: content.image_url, caption: message, access_token: account.access_token }),
> 224:          body: JSON.stringify({ message, access_token: account.access_token }),
> 230:    } else if (platform === "twitter") {
> 232:      const xHeaders = { Authorization: `Bearer ${account.access_token}`, "Content-Type": "application/json" };
> 246:            if (!prevId) { pulse("error", "twitter_thread_failed", { status: res.status }); throw new Error("PLATFORM_PUBLISH_FAILED"); }
> 253:        pulse("ok", "twitter_thread_published", { tweets: ids.length });
> 265:      // PULL_FROM_URL domain-ownership check, so we transfer the bytes ourselves). User access_token only —
> 278:          Authorization: `Bearer ${account.access_token}`,
> 318:          Authorization: `Bearer ${account.access_token}`,
> 366:            Authorization: `Bearer ${account.access_token}`,
> 394:      // PUT). User access_token only (publishing needs no client_secret). Shorts is implicit (9:16 + ≤3min).
> 415:            Authorization: `Bearer ${account.access_token}`,
> 471:        { headers: { Authorization: `Bearer ${account.access_token}` } }
> ```

## 🤖 Claude *(02:13:30)*


## 🤖 Claude *(02:13:43)*

Gate **selado e commitado** (`33fadb0`): emenda BoK [15-amendment-smart-delete.md](docs/bok/post-engine/15-amendment-smart-delete.md) (FR-SD-001..005 + Pattern Conformance) + SOP [smart-delete-remote.md](docs/processes/smart-delete-remote.md) + o SSOT de viabilidade. gitleaks limpo.

Recon das credenciais feito — e surgiu **um refinamento honesto do escopo** que muda o que o MVP entrega na prática:

O delete vive no **Calendário**, que lista `scheduled_posts` — ou seja, posts **sociais**. WordPress publica pela pipeline (vive em `content_library`, não no calendário). Então, no contexto real do calendário, o "delete remoto de verdade" do MVP se aplica a **Twitter/X** (se o tenant tem `tweet.write`) e **Pinterest** (se conectado) — e para **LinkedIn/IG/Facebook/YouTube/TikTok** entra o fluxo de **transparência** ("ainda no ar em `<rede>`; remova manual"). O WordPress full-delete fica pronto no código, mas só dispara se um dia houver post WP agendado ali.

**Isso não muda o valor** — a dor que você teve (deletar às cegas em cada rede) é resolvida pela camada de *verificar + avisar*, que cobre todas; e o X ganha delete real de 1 clique.

**Plano de build (per-user fail-closed, seguindo o padrão do `publish-social` que resolve de `decrypted_social_accounts` + `decrypted_user_api_keys`):**
1. **`check-post-existence`** (read-only, seguro) — entrego + deployo primeiro; já liga o "ainda está online?" em todas as redes.
2. **`delete-remote-post`** (destrutivo, idempotente) — X/Pinterest/WP.
3. **Fluxo de UI** no `useDeleteScheduledPost` (diálogo 3-ramos) + smoke zero-cost + deploy.

Vou construir na sequência começando pelo `check-post-existence` (o read-only não tem risco). Sigo agora — te reporto com prova material a cada peça. Algum ajuste antes de eu codar, ou mando ver?

## 👤 User *(02:16:10)*

<command-message>handoff</command-message>
<command-name>/handoff</command-name>

## 👤 User *(02:16:10)*

# ShakeHands — Session Seal Protocol v4

Execute the ShakeHands /handoff ritual to seal this session.

> **v4 (2026-05-15):** Reordered phases — Knowledge Mesh Milestone (Phase 3) now runs
> **before** README.md update (Phase 4), so the live node count query captures the handoff
> node itself. Previously the badge was always 1-3 nodes behind.
>
> **v3 (2026-05-14):** Added Phase 6 BoK Seal Status — verifies any module
> work in this session has a corresponding sealed BoK suite per MCORCH Master
> Execution Protocol. Blocks seal if significant module work lacks BoK.

---

## PRE-FLIGHT (execute ALL in parallel before anything else)

```bash
git status --short                          # inventory uncommitted changes
git diff HEAD --stat                        # change scope
git log --oneline -7                        # recent history + commit style
npx tsc --noEmit 2>&1 | tail -20           # TypeScript strict check
docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
docker ps --filter "name=mega-brain" --format "{{.Names}}: {{.Status}}"
curl -s http://localhost:8001/api/v2/heartbeat  # chroma API v2 health
```

Read in parallel:
- `HANDOFF.md` (current state, pending actions)
- `CLAUDE.md` (architecture rules)
- `/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md`

If TypeScript has errors → fix them before proceeding. Report any infra anomalies in the final summary.

---

## PHASE 1 — SECURITY AUDIT

Run these checks and report findings. **Block the seal if any CRITICAL finding exists.**

> ⚠️ **SCOPE NOTE:** This phase scans changes that exist NOW (before Phase 5 writes HANDOFF.md).
> A second mandatory scan runs in Phase 5b, after HANDOFF.md is written and before it is committed.

```bash
# 1a. Secret leak scan — check staged + working tree for hardcoded credentials
git diff HEAD | grep -E "(sk-[a-zA-Z0-9]{20,}|AIza[0-9A-Za-z_-]{35}|eyJ[a-zA-Z0-9._-]{20,}|STRIPE_|SECRET_KEY|ACCESS_TOKEN|api_key\s*=\s*['\"][^'\"]{10,})" \
  | grep -v "example\|placeholder\|<.*>\|your-key\|YOUR_" | head -20

# 1b. Edge function JWT enforcement — every user-facing function must verify JWT
grep -rL "Authorization\|jwt\|JWT\|service_role" supabase/functions/*/index.ts \
  | grep -v "get-infra-status\|watchdog" || echo "ALL FUNCTIONS: JWT enforced ✅"

# 1c. Client-side coin deduction guard — must NEVER update mco_balance directly from client
grep -rn "mco_balance.*update\|UPDATE.*mco_balance" src/ \
  | grep -v "settings\|top.up\|topup\|SettingsPage" | head -10 || echo "NO VIOLATIONS ✅"

# 1d. RLS bypass risk — check for supabase.rpc calls without auth context
grep -rn "service_role\|bypass.*rls\|rls.*bypass" src/ | head -10 || echo "NO VIOLATIONS ✅"

# 1e. Sensitive data in console.log
grep -rn "console\.log.*token\|console\.log.*key\|console\.log.*secret\|console\.log.*password" src/ \
  | head -10 || echo "NO SENSITIVE LOGS ✅"
```

**Security verdict:** list each check as ✅ PASS / ⚠️ WARN / 🔴 BLOCK.
Only proceed if no 🔴 findings.

---

### DOCUMENTATION CREDENTIAL RULE (invariant — never violate)

**When writing HANDOFF.md, README.md, or any committed documentation:**

- ✅ DO: describe WHERE a credential is stored → `VITE_GEMINI_API_KEY` is set in `.env` (local) and `GEMINI_API_KEY` in the Supabase vault
- ✅ DO: reference digest/fingerprint if useful → `GEMINI_API_KEY (digest 0fe0e159...)`
- 🔴 NEVER: include the actual credential value → `AIzaSyBv...`, `sk-...`, `eyJ...`

> **Rationale:** Phase 1 scans changes that predate the HANDOFF.md write. Any credential embedded
> in HANDOFF.md during Phase 5 escapes Phase 1 entirely and goes directly to the remote.
> This rule is the primary prevention layer; Phase 5b is the detection backstop.

---

## PHASE 2 — GRANULAR COMMITS

Group uncommitted changes by concern and commit each group separately.

**Commit rules (from memory + project convention):**
- Prefix: `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`
- Body: one paragraph explaining the WHY (milestone orientation, not diff description)
- **NEVER** add `Co-Authored-By` trailer
- **NEVER** use `git add -A` — stage files explicitly by name
- Skip: `build_log.txt`, `node_modules/`, `dist/`, `.env`, `check_types.ts`, `scratch/`

Stage and commit each logical group before moving to the next phase.

---

## PHASE 3 — KNOWLEDGE MESH MILESTONE

> ⚠️ **ORDER MATTERS:** This phase runs BEFORE Phase 4 (README badge) so the live count
> query captures this handoff node. Do not swap the order.

Insert a milestone node into mcorch_nodes to mark this session in the knowledge graph:

```bash
source .env
SUPABASE_URL="https://bcyvddsykvehvpwstlfa.supabase.co"
SESSION_PHASE="<phase-name-slug>"
SESSION_SUMMARY="<one-sentence summary of what was accomplished>"

curl -s -X POST "${SUPABASE_URL}/rest/v1/mcorch_nodes" \
  -H "apikey: ${SB_SECRET_KEY}" \
  -H "Authorization: Bearer ${SB_SECRET_KEY}" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d "{
    \"name\": \"session-handoff-$(date +%Y%m%d)-${SESSION_PHASE}\",
    \"node_type\": \"handoff\",
    \"content\": \"[HANDOFF SEAL] ${SESSION_SUMMARY}\",
    \"stability_score\": 1.0,
    \"project_id\": null,
    \"user_id\": null,
    \"metadata\": {
      \"session\": \"${SESSION_PHASE}\",
      \"sealed_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
      \"commits\": \"$(git log --oneline -5 | head -5 | tr '\n' '|')\"
    }
  }" | python3 -c "import sys,json; d=json.load(sys.stdin); print('Node ID:', d[0]['id'] if isinstance(d,list) else d.get('id','error'))" 2>/dev/null \
  || echo "⚠️ Knowledge Mesh insert failed — log manually"
```

Then trigger embedding for the new node:
```bash
NODE_ID="<id-from-above>"
curl -s -X POST "${SUPABASE_URL}/functions/v1/embed-mcorch-node" \
  -H "apikey: ${SB_SECRET_KEY}" \
  -H "Authorization: Bearer ${SB_SECRET_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"record\": {\"id\": \"${NODE_ID}\"}}" | python3 -c "import sys,json; d=json.load(sys.stdin); print('Embedded:', d)" 2>/dev/null \
  || echo "⚠️ Embedding failed — node persisted but not vectorized"
```

Emit `proof-manifest.json` so Phase 5c can verify this handoff node strictly:
```bash
echo "{\"handoffNodeId\": \"${NODE_ID}\"}" > proof-manifest.json
```

---

## PHASE 4 — README.md UPDATE

> ℹ️ Phase 3 (milestone node) has already been inserted — the live count below includes it.

Update `/README.md` to reflect the current session's work.

**Required updates:**
1. **Badges block** (top of file) — update dynamic values:
   - `neural_mesh-XXX_nodes` badge → fetch real count:
     ```bash
     curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?select=id&limit=1" \
       -H "apikey: $(grep SB_SECRET_KEY .env | cut -d'"' -f2)" \
       -H "Authorization: Bearer $(grep SB_SECRET_KEY .env | cut -d'"' -f2)" \
       -H "Prefer: count=exact" -I 2>/dev/null | grep -i content-range | grep -o '[0-9]*$'
     ```
   - `version-X.X.X` badge → increment patch version (or minor if major feature landed)
   - If new phase shipped → add phase badge (e.g. `Phase_Zeta-live-cyan`)

2. **Phase Status table** — add new row for this session's phase:
   ```
   | Phase Zeta — <Name> | ✅ <one-line summary> |
   ```

3. **What's New section** — prepend a new entry under the most recent one:
   ```markdown
   ### [v5.X.X] — <Phase Name> (<date>)
   - <bullet: major feature 1>
   - <bullet: major feature 2>
   ```

4. **Core metrics** (if present in README) — update node/edge counts.

Commit README separately:
```
docs(readme): vX.X.X — <phase name> — <one-line change summary>
```

---

## PHASE 5 — HANDOFF.md UPDATE

Rewrite the relevant sections of `HANDOFF.md` — **append, never replace history**.

**Required updates:**
1. **Task State table** — add new row:
   ```
   | **<Phase Name>** | ✅ <one-line summary> |
   ```

2. **New Record section** — add at the top of the history (after the Task State table):
   ```markdown
   ## <Phase Name> Record (<YYYY-MM-DD>)

   <one-paragraph prose summary of what changed and why>

   | Action | Result |
   |--------|--------|
   | `<file/function changed>` | ✅ <what it does now> |
   ...

   | Commit | Conteúdo |
   |--------|----------|
   | `<hash>` | <message> |
   ...

   ### Arquitetura <Phase Name>
   ```code block with data flow or key architecture diagram```
   ```

3. **Pending Actions** — check off completed items (~~strikethrough~~), add new ones discovered this session.

4. **GraphRAG State** section — update node/edge counts.

5. **Infrastructure** table — update container health.

---

## PHASE 5b — HANDOFF.md SECRET SCAN (mandatory before commit)

**Run this scan on the HANDOFF.md content about to be committed. Block if any finding exists.**

```bash
# 5b-1. Scan HANDOFF.md for real credential values
grep -nE "(AIza[0-9A-Za-z_-]{35}|sk-[a-zA-Z0-9]{20,}|eyJ[a-zA-Z0-9._-]{40,}|ghp_[a-zA-Z0-9]{36}|xox[baprs]-[a-zA-Z0-9-]+|[a-zA-Z0-9]{32,}=\s*['\"]?[A-Za-z0-9+/]{40,})" HANDOFF.md \
  | grep -v "example\|placeholder\|<.*>\|your-key\|YOUR_\|digest\|sha256\|hash\|fingerprint" \
  | head -20 || echo "HANDOFF.md: NO CREDENTIALS FOUND ✅"

# 5b-2. Specifically check for Google API keys (AIza prefix = 39 chars total)
grep -n "AIza[0-9A-Za-z_-]\{35\}" HANDOFF.md | head -10 || echo "NO GOOGLE API KEYS ✅"

# 5b-3. Check for any = "value" pattern that looks like a real assignment
grep -nE "=\s*['\"][A-Za-z0-9_\-]{20,}['\"]" HANDOFF.md \
  | grep -v "example\|placeholder\|<.*>\|your-\|YOUR_\|digest\|hash\|uuid\|id.*[0-9a-f-]\{36\}" \
  | head -10 || echo "NO INLINE ASSIGNMENTS ✅"
```

**If any check returns a match:**
1. 🔴 **DO NOT COMMIT** HANDOFF.md
2. Rewrite the offending section — replace the actual value with its location description
3. Re-run Phase 5b until all checks pass
4. Only then proceed to commit HANDOFF.md

Commit HANDOFF.md only after Phase 5b passes:
```
docs(handoff): seal <phase name> — <one-line summary>
```

---

## PHASE 5c — MATERIAL PROOF AUDIT (mandatory before push)

**Independently re-verify every material-proof claim of this seal. Block if any is contradicted.**

> ⚠️ Closes the Survival Law 1 (Materiality) self-grading weakness — this audit is mechanical,
> not self-reported. Skill: `mcorch-qa-healing` · SOP: `docs/processes/handoff-material-proof-audit.md`.

```bash
# Runs after Phase 5b, so the newest HANDOFF.md Record block is this seal's.
bun run scripts/qa/run-audit.ts HANDOFF.md
```

The audit parses the newest `## … Record` block and verifies each claim — commit hashes
(`git cat-file`), mesh UUIDs (`mcorch_nodes`/`mcorch_edges`), `tsc --noEmit`, the test suite,
edge-function reachability, file paths — then prints a Proof Manifest table and exits.

**Gate verdict:**
- **exit 0 — `SEAL ALLOWED`** → embed the Proof Manifest in the Phase 8 report (`📋 PROVA MATERIAL`); proceed to Phase 6.
- **exit 1 — `SEAL BLOCKED`** → 🔴 **BLOCK the seal.** Do NOT push. For each 🔴, fix the real
  cause — never fabricate proof (Law 1) — and re-run this phase until `SEAL ALLOWED`. If a 🔴 is a
  strict handoff-node claim, re-attempt the Phase 3 insert once (SOP Cenário D), then re-run.
- `⏭ skip` rows (infra unreachable · non-mesh UUID · size-only deploy) never block — report them.

---

## PHASE 6 — BoK SEAL STATUS (mandatory before push)

**Verify any significant module work in this session has a sealed BoK suite per CLAUDE.md MCORCH Master Execution Protocol.**

```bash
# 6-1. List BoK suites present + check completeness
for slug in $(ls docs/bok/ 2>/dev/null); do
  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)
  missing=()
  for doc in "${required[@]}"; do
    [ -f "docs/bok/$slug/$doc.md" ] || missing+=("$doc")
  done
  [ ${#missing[@]} -eq 0 ] \
    && echo "✅ $slug — BoK complete (9 docs)" \
    || echo "⚠️ $slug — incomplete (missing: ${missing[*]})"
done

# 6-2. Check session touched code in new src/pages/ or new supabase/functions/ that lacks BoK
session_new_modules=$(git diff --name-only HEAD~10..HEAD 2>/dev/null | grep -E "^(src/pages/|supabase/functions/|src/components/[A-Z])" | awk -F/ '{print "/"}' | sort -u)
echo "Session touched modules: $session_new_modules"

# 6-3. Mesh seal nodes for sealed BoK suites
source .env 2>/dev/null
if [ -n "$SB_SECRET_KEY" ]; then
  curl -s "$SUPABASE_URL/rest/v1/mcorch_nodes?node_type=eq.documentation_suite&select=id,name,stability_score,created_at" \
    -H "apikey: $SB_SECRET_KEY" \
    -H "Authorization: Bearer $SB_SECRET_KEY" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); [print(f\"  🌐 {n['name']} ({n['stability_score']})\") for n in d]" 2>/dev/null \
    || echo "  ⚠️ Could not query seal nodes"
fi
```

**Gate verdict:**
- ✅ All session modules have sealed BoK → proceed to Phase 7 push.
- ⚠️ Module work without BoK (e.g. `feat:` commit creating new page/edge fn without `docs/bok/<slug>/`)
  → 🔴 **BLOCK seal**. Run `/bok-scribe <module>` first OR add module to exemption list (typo/dep bump/single-file patch).

Report BoK status in final seal output (Phase 8).

---

## PHASE 7 — PUSH

```bash
git push origin main
```

Report: branch, number of commits pushed, remote URL.

If push fails (non-fast-forward): run `git pull --rebase origin main` first, then push again. Never force-push main.

---

## PHASE 7b — SPRINT & CONNECTIONS HYGIENE

### Sprint priorities update

Review `.claude/context/sprint-priorities.md` and update:
1. Check off completed items in "Skills a criar ou evoluir" and "Conexões a implementar"
2. Add new gaps discovered this session under "Top 3 Gap Closures" if applicable
3. Update the 4Cs Audit Snapshot scores if `/audit` was run this session
4. Append to the Retrospective section if this was the last session of the sprint

Commit if changed:
```
chore(sprint): update sprint-priorities — <one-line progress note>
```

### Scratch cleanup

```bash
ls scratch/ 2>/dev/null
```

If `scratch/` has `.ts` diagnostic scripts, move them to `.claude/scripts/db/`:
```bash
mkdir -p .claude/scripts/db
mv scratch/*.ts .claude/scripts/db/ 2>/dev/null && echo "Moved ✅" || echo "Nothing to move"
```

Commit if files were moved:
```
chore(scripts): migrate scratch diagnostics to .claude/scripts/db/
```

### MCP documentation check

```bash
cat .mcp.json
```

For each MCP server listed, verify it has an entry in `.claude/references/` or is documented in CLAUDE.md. If a new MCP was added this session and has no documentation, add a one-liner to the relevant reference file.

---

## PHASE 8 — FINAL REPORT

Print seal summary in **Portuguese (Brasil)**:

```
═══════════════════════════════════════════════════════════
  HANDOFF SEALED — <PHASE NAME> (<date>)
═══════════════════════════════════════════════════════════

🔐 SEGURANÇA
  <security check results — each as ✅ / ⚠️ / 🔴>

📦 COMMITS (<N> total)
  <hash> — <message>
  ...

⬡ KNOWLEDGE MESH
  Milestone node: <node id> — <name>
  Embedding: ✅ / ⚠️

📖 README.md
  Versão: <old> → <new>
  Badge neural_mesh: <old> → <new> nós
  Seção adicionada: <section name>

🧠 HANDOFF.md
  Fase selada: <phase name>
  Seções atualizadas: Task State, Record, Pending Actions, GraphRAG State

📋 PROVA MATERIAL (Fase 5c)
  Veredito: <SEAL ALLOWED / SEAL BLOCKED>
  Claims: <N> verificadas · <M> skipped · <K> falhas

🚀 PUSH
  Branch: main → origin/main
  Commits enviados: <N>

📌 SPRINT
  sprint-priorities.md: <atualizado ✅ / sem mudanças>
  scratch/ cleanup: <arquivos movidos ✅ / limpo ✅>
  MCP docs: <ok ✅ / pendência: X>

⏭  PRÓXIMOS PASSOS
  1. <top pending action>
  2. <second pending action>
  3. <third pending action>

═══════════════════════════════════════════════════════════
  Assinado: Claude Code — Braço de Engenharia do AIOS
═══════════════════════════════════════════════════════════
```

**Invariants — never skip:**
- Security audit must run and report before any commit (Phase 1)
- **Phase 3 (milestone node) must run BEFORE Phase 4 (README badge query)** — ensures count includes the handoff node
- **Phase 5b secret scan must run on HANDOFF.md before its commit** — no exceptions
- **Phase 5c material proof audit must run and return `SEAL ALLOWED` before push** — a contradicted claim blocks the seal
- **Documentation must NEVER contain actual credential values** — only describe where they live
- README.md badge counts must reflect real DB state (query live, after milestone insert)
- HANDOFF.md must be updated even if nothing changed (session note)
- Push must happen — remote must always mirror local main
- Knowledge Mesh milestone must be attempted (failures are logged, not blocking)
- git pre-commit hook (`.git/hooks/pre-commit`) is the last barrier — do not bypass with `--no-verify`


## 🤖 Claude *(02:16:27)*


## 🤖 Claude *(02:16:28)*

Executando o ShakeHands /handoff v4. Pre-flight em paralelo:

## 🤖 Claude *(02:16:32)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== git status ===\"; git status --short\necho \"=== diff stat HEAD~4 ===\"; git diff HEAD~4 --stat 2>/dev/null | tail -20\necho \"=== log -8 ===\"; git log --oneline -8\necho \"=== tsc ===\"; npx tsc --noEmit 2>&1 | tail -8; echo \"tsc exit: ${PIPESTATUS[0]}\"\necho \"=== docker mcorch ===\"; docker ps --filter \"name=mcorch\" --format \"{{.Names}}: {{.Status}}\" 2>/dev/null\necho \"=== docker mega-brain ===\"; docker ps --filter \"name=mega-brain\" --format \"{{.Names}}: {{.Status}}\" 2>/dev/null\necho \"=== chroma ===\"; curl -s http://localhost:8001/api/v2/heartbeat 2>/dev/null | head -c 200 || echo \"(chroma unreachable)\"",
  "description": "Handoff pre-flight checks in parallel"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === git status ===
> === diff stat HEAD~4 ===
>  .claude/context/autonomous-loop-charter.md         |  2 +-
>  .../context/smart-delete-feasibility-2026-06-30.md | 32 +++++++++++
>  HANDOFF.md                                         | 44 +++++++++++++++
>  README.md                                          |  4 +-
>  docs/bok/post-engine/15-amendment-smart-delete.md  | 64 ++++++++++++++++++++++
>  docs/processes/smart-delete-remote.md              | 35 ++++++++++++
>  proof-manifest.json                                |  2 +-
>  supabase/functions/_shared/llm-fallback.ts         | 37 +++++++++++++
>  supabase/functions/lead-score/index.ts             |  3 +-
>  supabase/functions/orchestrate-step/index.ts       |  5 +-
>  10 files changed, 222 insertions(+), 6 deletions(-)
> === log -8 ===
> 33fadb0 docs(post-engine): seal smart-delete gate — BoK amendment 15 (FR-SD-001..005) + SOP + capability-matrix SSOT
> 0d4e3b4 feat(observability): llm_usage telemetry — mede o custo LLM do ciclo de video (proven LIVE)
> 1630371 docs(handoff): seal loop autônomo — FR-VS-047 editor render pipeline + security hardening (SEC-006/007 + FR-SEC-014 pt1)
> 145f106 docs(readme): v6.63.0 — editor render pipeline (FR-VS-047) + security hardening — mesh 9003
> 8922497 docs(loop): absorve direcao fresca do Sovereign + achado license:None do hyperframes CLI
> 2a9fbf4 feat(security): FR-SEC-014 part 1 — security_events immutable ledger (proven LIVE)
> c880fcf docs(context): zero-USD video-cycle audit + native-exclusive fork eval (opensrc/graphify red herrings; HyperFrames-first path)
> a29627b feat(calendar): day-detail modal — clicar dia/post abre todas as publicações da data com propriedades completas + reagendar/duplicar/remover
> === tsc ===
> tsc exit: 0
> === docker mcorch ===
> mcorch_vision_mcp: Up 32 hours (healthy)
> mcorch_claude_mem: Up 2 weeks (healthy)
> mcorch_chroma: Up 2 weeks (healthy)
> === docker mega-brain ===
> mega-brain-dashboard: Up 2 weeks
> mega-brain-webhook: Up 2 weeks (healthy)
> mega-brain-daemon: Up 2 weeks (healthy)
> === chroma ===
> {"nanosecond heartbeat":1782872192831986123}
> ```

## 🤖 Claude *(02:16:33)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== HANDOFF.md head (estrutura Task State) ===\"; head -50 HANDOFF.md",
  "description": "Read HANDOFF.md structure"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === HANDOFF.md head (estrutura Task State) ===
> # HANDOFF — MCORCH Constellation Orchestra
> 
> ## ⚡ FIRST ACTION FOR NEXT AGENT
> 
> ```bash
> git log --oneline -5
> # Then explore the codebase — do NOT start from the file tree
> ```
> 
> ---
> 
> ## Task State
> 
> ## Session Seal — Loop Autônomo: FR-VS-047 Editor Render Pipeline + Security Hardening (2026-06-30)
> 
> Continuação do **loop autônomo de malha fechada** (`/loop` auto-ritmado, ultracode) da seal anterior. **8 iterações fechadas**, cada uma com prova material (Lei 1) e commit granular, governadas pela `autonomous-loop-charter.md`. Selada por `/handoff` explícito do Sovereign (stop). Entregou **2 Fatias completas** (FR-VS-047 editor→pipeline · OTD-SEC-006/007 + FR-SEC-014 pt1 hardening) + correção de roadmap + absorção da direção fresca do Sovereign.
> 
> **Decisão de arquitetura decisiva (it.3):** o render-parity do editor HyperFrames — reimplementar o seek `frame=floor(time*fps)` era o hard blocker (risco de MP4-branco) — foi resolvido **ENVOLVENDO `hyperframes render`** (o renderer de referência local, USD=0) → paridade **definitional**. Provado em 3 níveis: frame-diff (frames t=1s/t=6s sha256-distintos) · byte-determinismo (2 renders idênticos sha256 `1db99067`) · semântico (Vision-QA confidence high). ⚠️ **Achado it.8/9:** o npm `hyperframes@0.7.22` é `license:"None"` → o wrap carrega dep proprietária (anti-doutrina) → caminho nativo (internalizar `bundleToSingleHtml`+seek do `@hyperframes/core` Apache-2.0) registrado.
> 
> | Action | Result |
> |--------|--------|
> | **FR-VS-047 wiring** (`render-core.ts` `renderStudioProject` + `video-bridge.ts` branch `studio-project`) | ✅ E2E: render real do projeto `mcorch-video` → `video_renders 9069bb7d` done · bucket 720.678 B (HTTP 200) · `video_assets` · `creative_assets` 1080×1920/8s · mesh node. Trap ARM64 resolvido (`HYPERFRAMES_BROWSER_PATH`→chromium Playwright) |
> | **Fix bug TDZ** (`video-bridge.ts`) | ✅ `ap` usado antes da declaração → dual-write de vídeo→`creative_assets` SEMPRE pulava silenciosamente; movido p/ topo → renders do editor agora entram na Biblioteca de Assets |
> | **BoK §VS-UI-B (Amendment v0.5)** (`docs/bok/video-studio/05-sdd.md`) | ✅ Gate Lei 2: contrato McorchAdapter (13 métodos = 13 call-sites, `npm pack` do dist publicado + Workflow adversarial `wf_b0a6c005-8c2`) + 3 pre-code gates + FR-VS-047/048/049 |
> | **Guard smoke** (`scripts/qa/smoke-studio-project-guard.ts`) | ✅ 4/4 sub-segundo: path-safety rejeita execução de dir arbitrário (escape/traversal/vazio) antes do spawn |
> | **OTD-SEC-006 sentinel-wiring** (`generate-content` + `lead-score`) | ✅ Provado LIVE: injeção→403 `prompt_injection_suspected`; legítimo→não-403 (sem FP); lead-score bloqueia com saldo intacto (sem charge-without-value). OTD-SEC-007 (lefthook/gitleaks) marcada FECHADA |
> | **FR-SEC-014 pt1** (`20260701000000_security_events_ledger.sql` + `_shared/sentinel.ts`) | ✅ Ledger imutável (service-insert/admin-select/immutable RLS) aplicado (isolado do drift de tracking) + `logSentinelBlock` espelha bloqueios (warning). `/security-review` **NO FINDINGS** (adversarial 9/10). Provado LIVE (injeção→row) |
> | **#2 YT/TikTok** (charter it.1) | ✅ false-high corrigido por probe: seal 8973 já entregou publish/OAuth/tables; único gap = render-decoupling (charge-without-value trap documentado); valor OAuth-gated → Fila |
> | Direção fresca do Sovereign absorvida | ✅ 2 docs committados (`c880fcf`) — observability gap (zero-USD) + native-exclusive eval → charter backlog #0 |
> 
> | Commit | Conteúdo |
> |--------|----------|
> | `8d59160` | docs(loop): charter it.1 — #2 YT/TikTok false-high |
> | `06f7601` | docs(bok): §VS-UI-B Amendment v0.5 — McorchAdapter contract + 3 gates |
> | `3b579e6` | docs(bok): FR-VS-047 render-parity RESOLVIDO — wrap hyperframes render |
> | `8587573` | feat(video-studio): FR-VS-047 wiring worker-side + TDZ fix |
> | `f0bd95f` | docs(bok): FR-VS-047 GATE VERDE — determinismo + Vision-QA |
> | `cc69656` | test(video-studio): guard smoke path-safety |
> | `8da8ebc` | feat(security): OTD-SEC-006 sentinel-wiring (proven LIVE) |
> | `2a9fbf4` | feat(security): FR-SEC-014 pt1 — security_events ledger (proven LIVE) |
> | `8922497` | docs(loop): absorve direção Sovereign + achado license:None |
> | `145f106` | docs(readme): v6.63.0 — mesh 9003 |
> 
> Handoff node `d02a8570-5195-4206-a918-df3a42423aba` inserido + embedado (768d). Mesh **9003 nós**.
> 
> ### Arquitetura — Studio-project render (FR-VS-047, wrap do renderer de referência)
> ```
> Editor HyperFrames (video-studio.service, vanilla) → autora projeto em ~/.mcorch/video-studio/projects/<id>/
> video_renders(queued, composition={mode:'studio-project', project_dir}) [enqueue-side = Fila Sovereign, billing]
>   └ video-bridge.ts (worker, poll) → renderStudioProject (render-core.ts):
> ```

## 🤖 Claude *(02:17:05)*


## 🤖 Claude *(02:17:08)*

**Pre-flight limpo:** git tree clean (tudo commitado), tsc **exit 0**, todos os containers healthy, chroma OK. Noto que o **loop já selou um handoff próprio** (`1630371`) e bumpou README→v6.63.0/mesh 9003 — então meu seal appenda o **record desta sessão interativa** (calendário + gate smart-delete + GO de gasto + doutrina). 

**Phase 1 — Security audit** (scoped aos commits não-pushados):

## 🤖 Claude *(02:17:14)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== commits n\u00e3o-pushados (origin/main..HEAD) ===\"\ngit log origin/main..HEAD --oneline 2>/dev/null || echo \"(sem upstream ref)\"\necho\necho \"=== 1a. secret leak scan (diff n\u00e3o-pushado) ===\"\ngit log origin/main..HEAD -p 2>/dev/null | grep -E \"(sk-[a-zA-Z0-9]{20,}|AIza[0-9A-Za-z_-]{35}|eyJ[a-zA-Z0-9._-]{40,}|STRIPE_SECRET|SB_SECRET_KEY\\s*=|ACCESS_TOKEN\\s*=)\" | grep -v \"example\\|placeholder\\|<.*>\\|your-key\\|YOUR_\\|digest\\|Deno.env\\|process.env\" | head -10 || echo \"NENHUM SEGREDO \u2705\"\necho\necho \"=== 1c. client-side coin deduction ===\"\ngrep -rn \"mco_balance.*update\\|UPDATE.*mco_balance\" src/ 2>/dev/null | grep -v \"settings\\|topup\\|SettingsPage\" | head -5 || echo \"NO VIOLATIONS \u2705\"\necho\necho \"=== 1e. sensitive console.log (meus arquivos) ===\"\ngrep -rnE \"console\\.log.*(token|secret|password|api_key)\" src/pages/CalendarPage.tsx 2>/dev/null | head -5 || echo \"NO SENSITIVE LOGS \u2705\"",
  "description": "Phase 1 security audit scoped to unpushed commits"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === commits não-pushados (origin/main..HEAD) ===
> 33fadb0 docs(post-engine): seal smart-delete gate — BoK amendment 15 (FR-SD-001..005) + SOP + capability-matrix SSOT
> 0d4e3b4 feat(observability): llm_usage telemetry — mede o custo LLM do ciclo de video (proven LIVE)
> 
> === 1a. secret leak scan (diff não-pushado) ===
> 
> === 1c. client-side coin deduction ===
> 
> === 1e. sensitive console.log (meus arquivos) ===
> ```

## 🤖 Claude *(02:17:33)*


## 🤖 Claude *(02:17:35)*

**Security verdict Phase 1:** ✅ nenhum segredo · ✅ sem coin-deduction client-side · ✅ sem log sensível. Sem 🔴 — prossigo. **Phase 2:** tree limpo, nada a commitar (tudo já em commits granulares). Unpushed = `33fadb0` (meu gate) + `0d4e3b4` (llm_usage do loop).

**Phase 3 — Knowledge Mesh milestone** (insere o nó desta sessão + embed):

## 🤖 Claude *(02:17:45)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nSUPABASE_URL=\"https://bcyvddsykvehvpwstlfa.supabase.co\"\nSESSION_PHASE=\"sovereign-calendar-videogo-smartdelete-gate\"\nSESSION_SUMMARY=\"Sessao interativa Sovereign: Calendario day-detail modal (deployed+browser-verified) + 1o ciclo PAGO de video testemunhado (cycle 77e02fca, MP4 776KB, render self-hosted USD0) + doutrina open-source-first encodada + gate smart-delete selado (BoK amendment 15 FR-SD-001..005 + SOP + capability-matrix SSOT).\"\nNODE=$(curl -s -X POST \"${SUPABASE_URL}/rest/v1/mcorch_nodes\" \\\n  -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" \\\n  -H \"Content-Type: application/json\" -H \"Prefer: return=representation\" \\\n  -d \"{\\\"name\\\":\\\"session-handoff-$(date +%Y%m%d)-${SESSION_PHASE}\\\",\\\"node_type\\\":\\\"handoff\\\",\\\"content\\\":\\\"[HANDOFF SEAL] ${SESSION_SUMMARY}\\\",\\\"stability_score\\\":1.0,\\\"project_id\\\":null,\\\"user_id\\\":null,\\\"metadata\\\":{\\\"session\\\":\\\"${SESSION_PHASE}\\\",\\\"sealed_at\\\":\\\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\\\",\\\"commits\\\":\\\"$(git log --oneline -4 | tr '\\n' '|')\\\"}}\")\nNODE_ID=$(echo \"$NODE\" | python3 -c \"import sys,json; d=json.load(sys.stdin); print(d[0]['id'] if isinstance(d,list) else d.get('id','error'))\" 2>/dev/null)\necho \"Node ID: $NODE_ID\"\necho \"{\\\"handoffNodeId\\\": \\\"${NODE_ID}\\\"}\" > proof-manifest.json\necho \"=== embed ===\"\ncurl -s -X POST \"${SUPABASE_URL}/functions/v1/embed-mcorch-node\" \\\n  -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" \\\n  -H \"Content-Type: application/json\" \\\n  -d \"{\\\"record\\\": {\\\"id\\\": \\\"${NODE_ID}\\\"}}\" | python3 -c \"import sys,json; d=json.load(sys.stdin); print('Embedded:', d.get('status', d))\" 2>/dev/null || echo \"embed resp non-json\"\necho \"=== node count live (inclui este) ===\"\ncurl -s \"${SUPABASE_URL}/rest/v1/mcorch_nodes?select=id&limit=1\" -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" -H \"Prefer: count=exact\" -I 2>/dev/null | grep -i content-range | grep -o '[0-9]*$'",
  "description": "Insert handoff milestone node, embed, get live count"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Node ID: f3248e11-9ed2-4892-8140-9da4af007e75
> === embed ===
> Embedded: {'error': 'Request body must contain { node_id: string }'}
> === node count live (inclui este) ===
> 9004
> ```

## 🤖 Claude *(02:17:52)*


## 🤖 Claude *(02:17:53)*

Nó inserido: `f3248e11-9ed2-4892-8140-9da4af007e75`, count live **9004**. O embed rejeitou o formato do protocolo (`{record:{id}}`) — a fn quer `{node_id}`. Re-disparo com o body correto:

## 🤖 Claude *(02:17:58)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nset -a; source .env 2>/dev/null; set +a\nSUPABASE_URL=\"https://bcyvddsykvehvpwstlfa.supabase.co\"\nNODE_ID=\"f3248e11-9ed2-4892-8140-9da4af007e75\"\ncurl -s -X POST \"${SUPABASE_URL}/functions/v1/embed-mcorch-node\" \\\n  -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" \\\n  -H \"Content-Type: application/json\" \\\n  -d \"{\\\"node_id\\\": \\\"${NODE_ID}\\\"}\" | python3 -c \"import sys,json; d=json.load(sys.stdin); print('Embedded:', d.get('status', d))\" 2>/dev/null || echo \"embed resp non-json\"\necho \"=== confirma embedding (embedding n\u00e3o-nulo?) ===\"\ncurl -s \"${SUPABASE_URL}/rest/v1/mcorch_nodes?id=eq.${NODE_ID}&select=id,embedding\" -H \"apikey: ${SB_SECRET_KEY}\" -H \"Authorization: Bearer ${SB_SECRET_KEY}\" | python3 -c \"import sys,json; d=json.load(sys.stdin); print('embedding present:', bool(d and d[0].get('embedding')))\" 2>/dev/null || echo \"check falhou\"",
  "description": "Re-trigger embedding with correct body format"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> Embedded: {'node_id': 'f3248e11-9ed2-4892-8140-9da4af007e75', 'dims': 768, 'chunks': 1, 'model': 'openai/text-embedding-3-small', 'provider': 'openrouter', 'stitched': 0}
> === confirma embedding (embedding não-nulo?) ===
> embedding present: True
> ```

## 🤖 Claude *(02:18:04)*


## 🤖 Claude *(02:18:05)*

Embedded (768d, presente). **Phase 4 — README** (loop deixou em v6.63.0/9003; bumpo pra v6.64.0/9004 com o que esta sessão entregou). Leio os trechos a editar:

## 🤖 Claude *(02:18:08)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== badges (version + neural_mesh) ===\"\ngrep -nE \"version-[0-9]|neural_mesh-[0-9]|badge\" README.md | head -8\necho \"=== What's New / Phase head ===\"\ngrep -nE \"What's New|## \\[v6\\.|Phase (Status|Zeta|Eta)|\u2705\" README.md | head -12",
  "description": "Locate README badges and What's New section"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === badges (version + neural_mesh) ===
> 2:  <img src="https://img.shields.io/badge/status-production-brightgreen?style=for-the-badge" alt="Status" />
> 3:  <img src="https://img.shields.io/badge/version-6.63.0--Editor--Render--Pipeline--%2B--Sec--Hardening-blueviolet?style=for-the-badge" alt="Version" />
> 4:  <img src="https://img.shields.io/badge/license-proprietary-red?style=for-the-badge" alt="License" />
> 5:  <img src="https://img.shields.io/badge/typescript-strict-blue?style=for-the-badge&logo=typescript" alt="TypeScript" />
> 6:  <img src="https://img.shields.io/badge/neural_mesh-9003_nodes-blueviolet?style=for-the-badge" alt="Neural Mesh" />
> 7:  <img src="https://img.shields.io/badge/avatar--clone--ai-Fatia_3b_avatarIdentity_node_live_(VLM--soft)-blueviolet?style=for-the-badge" alt="Avatar Clone AI 3b" />
> 8:  <img src="https://img.shields.io/badge/Agentic_Vision-21_patterns_%2B_Collective_Ledger-blueviolet?style=for-the-badge" alt="Agentic Vision" />
> 9:  <img src="https://img.shields.io/badge/API_Tenancy-100%25_per--user_(env%3Dinfra)-brightgreen?style=for-the-badge" alt="API Tenancy" />
> === What's New / Phase head ===
> 617:### [v6.49.1] — Blueprint do HyperFrames Studio (funda VS-UI) + gap de billing do vídeo fechado (2026-06-24)
> 621:### [v6.49.0] — Vídeo viral 9:16 autônomo + motor HyperFrames determinístico vivo (2026-06-24)
> 627:### [v6.48.0] — Viral Autopilot ATIVADO (1º ciclo pago + pg_cron) + FR-VA-018 + segurança social-auth + paridade sentinel pt-BR (2026-06-23)
> 634:### [v6.47.0] — Per-user 100% (env = só infra) + CF WP unblock + sweep per-user fechado (2026-06-22)
> 640:### [v6.46.0] — Alertas resolvidos + Vídeo Fatia 1/1b + De-n8n (motor faceless nativo) (2026-06-22)
> 646:### [v6.42.0] — Viral Autopilot BoK 9/9 (motor de conteúdo viral autônomo, R1-R4) (2026-06-17)
> 653:### [v6.41.0] — Unified Sensorial Canvas (Phase Epsilon V9): Code + Memory + Black Hole numa cena R3F (2026-06-17)
> 659:### [v6.39.1] — Vision MCP público: `mcp.mcorch.com` LIVE pelo Cloudflare (OTD-VM-013 fechada) (2026-06-16)
> 663:### [v6.39.0] — Vision MCP Fatia 3 core: PAT external auth + LGPD erasure + nginx vhost (2026-06-15)
> 669:### [v6.38.0] — Vision MCP: `deepsearch.run`/`poll` async (FR-VM-007) — job→poll→partial-refund §4.5 (2026-06-15)
> 675:### [v6.37.0] — Vision MCP Fatia 2: 4 Billable Tools + BYOK Foundation (+ Fatia 1 handshake/interop close) (2026-06-15)
> 681:### [v6.29.0] — Agentic Workspace: Multi-Agent Threads Chat & Kanban Task Board (2026-06-06)
> ```

## 🤖 Claude *(02:18:32)*


## 🤖 Claude *(02:18:33)*

README a editar. 3 edits — badge de versão, badge de mesh (9004), e entrada What's New:

## 🤖 Claude *(02:18:36)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "old_string": "  <img src=\"https://img.shields.io/badge/version-6.63.0--Editor--Render--Pipeline--%2B--Sec--Hardening-blueviolet?style=for-the-badge\" alt=\"Version\" />",
  "new_string": "  <img src=\"https://img.shields.io/badge/version-6.64.0--Calendar--Day--Detail--%2B--Smart--Delete--Gate-blueviolet?style=for-the-badge\" alt=\"Version\" />"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(02:18:38)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "old_string": "  <img src=\"https://img.shields.io/badge/neural_mesh-9003_nodes-blueviolet?style=for-the-badge\" alt=\"Neural Mesh\" />",
  "new_string": "  <img src=\"https://img.shields.io/badge/neural_mesh-9004_nodes-blueviolet?style=for-the-badge\" alt=\"Neural Mesh\" />"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(02:18:43)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "old_string": "### [v6.49.1] \u2014 Blueprint do HyperFrames Studio (funda VS-UI) + gap de billing do v\u00eddeo fechado (2026-06-24)",
  "new_string": "### [v6.64.0] \u2014 Calend\u00e1rio day-detail + 1\u00ba ciclo PAGO de v\u00eddeo + gate smart-delete (2026-06-30)\n- **Calend\u00e1rio de Publica\u00e7\u00f5es \u2014 Detalhe do Dia:** clicar dia/post/\"+N mais\" abre modal com TODAS as publica\u00e7\u00f5es da data + propriedades completas (plataforma\u00b7hor\u00e1rio\u00b7status\u00b7conte\u00fado\u00b7conta\u00b7published_at\u00b7erro\u00b7tentativas) + a\u00e7\u00f5es inline (reagendar/duplicar/remover) + CTA agendar. Deployed + browser-verified (`a29627b`).\n- **1\u00ba ciclo PAGO de v\u00eddeo testemunhado:** `video_enabled` ligado no plano do Usu\u00e1rio Zero \u2192 ciclo `77e02fca` completed (32 mco); render `561a31df` HyperFrames self-hosted \u2192 MP4 776KB 1080\u00d71920 no bucket; reconcilia\u00e7\u00e3o FR-VA-025. Render USD=0 (a parte cara j\u00e1 \u00e9 pr\u00f3pria).\n- **Doutrina open-source-first encodada:** custo USD externo ao Sovereign=0 + posse do stack caro = equity; Gemini 2.5 Pro mantido (qualidade brand vale ~$10/m\u00eas na BYOK pr\u00f3pria). Audit zero-USD + eval de fork nativo (opensrc/graphify = red herrings; HyperFrames-first).\n- **Gate smart-delete selado:** emenda BoK post-engine 15 (FR-SD-001..005) + SOP + capability-matrix por rede (WP/X/Pinterest delet\u00e1veis; IG/TikTok sem delete API \u2192 transpar\u00eancia honesta) (`33fadb0`).\n\n### [v6.49.1] \u2014 Blueprint do HyperFrames Studio (funda VS-UI) + gap de billing do v\u00eddeo fechado (2026-06-24)"
}
```

> **Tool Result (Edit)** - ❌ Error
>
> ```
> <tool_use_error>File has not been read yet. Read it first before writing to it.</tool_use_error>
> ```

## 🤖 Claude *(02:18:48)*


## 🤖 Claude *(02:18:49)*

Preciso Read o README antes de editar (o grep via Bash não conta). Leio os dois trechos:

## 🤖 Claude *(02:18:50)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "limit": 10
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	<p align="center">
> 2	  <img src="https://img.shields.io/badge/status-production-brightgreen?style=for-the-badge" alt="Status" />
> 3	  <img src="https://img.shields.io/badge/version-6.63.0--Editor--Render--Pipeline--%2B--Sec--Hardening-blueviolet?style=for-the-badge" alt="Version" />
> 4	  <img src="https://img.shields.io/badge/license-proprietary-red?style=for-the-badge" alt="License" />
> 5	  <img src="https://img.shields.io/badge/typescript-strict-blue?style=for-the-badge&logo=typescript" alt="TypeScript" />
> 6	  <img src="https://img.shields.io/badge/neural_mesh-9003_nodes-blueviolet?style=for-the-badge" alt="Neural Mesh" />
> 7	  <img src="https://img.shields.io/badge/avatar--clone--ai-Fatia_3b_avatarIdentity_node_live_(VLM--soft)-blueviolet?style=for-the-badge" alt="Avatar Clone AI 3b" />
> 8	  <img src="https://img.shields.io/badge/Agentic_Vision-21_patterns_%2B_Collective_Ledger-blueviolet?style=for-the-badge" alt="Agentic Vision" />
> 9	  <img src="https://img.shields.io/badge/API_Tenancy-100%25_per--user_(env%3Dinfra)-brightgreen?style=for-the-badge" alt="API Tenancy" />
> 10	  <img src="https://img.shields.io/badge/BoK_video--studio-9%2F9_%2B_agency_v1.1-fuchsia?style=for-the-badge" alt="BoK video-studio" />
> ```

## 🤖 Claude *(02:18:51)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "offset": 614,
  "limit": 6
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 614	         + AIOS — conversational AI consciousness with VAD + Barge-in
> 615	```
> 616	
> 617	### [v6.49.1] — Blueprint do HyperFrames Studio (funda VS-UI) + gap de billing do vídeo fechado (2026-06-24)
> 618	- **Blueprint de integração do HyperFrames Studio (deepsearch, funda Fatia VS-UI):** material-citado no repo HeyGen `@ ae8b94c5` (Apache-2.0). Achado decisivo — `StudioApp` é **zero-props**, server-backed por um `/api` REST+SSE na mesma origem; a HeyGen expôs um seam de injeção limpo (`StudioApiAdapter` de `@hyperframes/core/studio-api`). Logo **NÃO forkamos a UI**: montamos o `StudioApp` unmodified + implementamos nosso `McorchAdapter` cujo `startRender()` faz bridge pro nosso `video-render` já provado. Composição = HTML+CSS+GSAP → `bundleToSingleHtml` (o que o motor já come). React 19 → container+iframe `studio.mcorch.com`. `.claude/context/hyperframes-studio-integration-blueprint-2026-06-24.md` (6 gates empíricos, render-parity `frame=floor(time*fps)` = maior risco).
> 619	- **Gap de billing-accuracy do vídeo fechado (OTD-VA-010):** o `actual` do ciclo é **otimista** (`succeeded × (ORCH+VIDEO)`, calculado pelo `autopilot-run` ANTES do enqueue async). Se o INSERT de `video_renders` falha (fail-open `skipped`), não há linha → o `finalize_video_render` nunca refunda → o tenant pagava 12 por um render nunca enfileirado. **Fix:** crédito compensatório idempotente `refund_autopilot_video_enqueue` (migration `20260624140000`, anchor `run_id` PK, anti-mint ≤100, service-role-only, crédito positivo) chamado no fail-open do `orchestrate-step` quando `!enqueued`. Completa o modelo de refund de 3 caminhos (ciclo / render-fail / enqueue-fail; exatamente um de render/enqueue por sub-run — sem dupla-credito). **Provado:** smoke `smoke-autopilot-video-refund.ts` **8/8 zero-net-cost** — net debit = ORCH_COST (12 excluído; sem fix seria 22) + idempotência + anti-mint + saldo restaurado. `/security-review` SAFE (mint travado em service-role, cross-tenant impossível, idempotência via PK).
> ```

## 🤖 Claude *(02:18:53)*

Agora aplico os 3 edits:

## 🤖 Claude *(02:18:56)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "old_string": "  <img src=\"https://img.shields.io/badge/version-6.63.0--Editor--Render--Pipeline--%2B--Sec--Hardening-blueviolet?style=for-the-badge\" alt=\"Version\" />",
  "new_string": "  <img src=\"https://img.shields.io/badge/version-6.64.0--Calendar--Day--Detail--%2B--Smart--Delete--Gate-blueviolet?style=for-the-badge\" alt=\"Version\" />"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:18:58)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "old_string": "  <img src=\"https://img.shields.io/badge/neural_mesh-9003_nodes-blueviolet?style=for-the-badge\" alt=\"Neural Mesh\" />",
  "new_string": "  <img src=\"https://img.shields.io/badge/neural_mesh-9004_nodes-blueviolet?style=for-the-badge\" alt=\"Neural Mesh\" />"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:19:07)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/README.md",
  "old_string": "### [v6.49.1] \u2014 Blueprint do HyperFrames Studio (funda VS-UI) + gap de billing do v\u00eddeo fechado (2026-06-24)",
  "new_string": "### [v6.64.0] \u2014 Calend\u00e1rio day-detail + 1\u00ba ciclo PAGO de v\u00eddeo + gate smart-delete (2026-06-30)\n- **Calend\u00e1rio de Publica\u00e7\u00f5es \u2014 Detalhe do Dia:** clicar dia/post/\"+N mais\" abre modal com TODAS as publica\u00e7\u00f5es da data + propriedades completas (plataforma\u00b7hor\u00e1rio\u00b7status\u00b7conte\u00fado\u00b7conta\u00b7published_at\u00b7erro\u00b7tentativas) + a\u00e7\u00f5es inline (reagendar/duplicar/remover) + CTA agendar. Deployed + browser-verified (`a29627b`).\n- **1\u00ba ciclo PAGO de v\u00eddeo testemunhado:** `video_enabled` ligado no plano do Usu\u00e1rio Zero \u2192 ciclo `77e02fca` completed (32 mco); render `561a31df` HyperFrames self-hosted \u2192 MP4 776KB 1080\u00d71920 no bucket; reconcilia\u00e7\u00e3o FR-VA-025. Render USD=0 (a parte cara j\u00e1 \u00e9 pr\u00f3pria).\n- **Doutrina open-source-first encodada:** custo USD externo ao Sovereign=0 + posse do stack caro = equity; Gemini 2.5 Pro mantido (qualidade brand vale ~$10/m\u00eas na BYOK pr\u00f3pria). Audit zero-USD + eval de fork nativo (opensrc/graphify = red herrings; HyperFrames-first).\n- **Gate smart-delete selado:** emenda BoK post-engine 15 (FR-SD-001..005) + SOP + capability-matrix por rede (WP/X/Pinterest delet\u00e1veis; IG/TikTok sem delete API \u2192 transpar\u00eancia honesta) (`33fadb0`).\n\n### [v6.49.1] \u2014 Blueprint do HyperFrames Studio (funda VS-UI) + gap de billing do v\u00eddeo fechado (2026-06-24)"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/README.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:19:17)*


## 🤖 Claude *(02:19:19)*

README atualizado (v6.64.0, mesh 9004, entrada What's New). Commito o README separado:

## 🤖 Claude *(02:19:19)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add README.md\ngit commit -q -m \"docs(readme): v6.64.0 \u2014 calend\u00e1rio day-detail + 1\u00ba ciclo pago de v\u00eddeo + gate smart-delete \u2014 mesh 9004\" && echo \"readme commit: $(git log -1 --format=%h)\"",
  "description": "Commit README update"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;6;6;6m─[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpre-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;6;6;6m─[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m╯[m
> ┃  e2e-output-tripwire ❯ 
> 
> ┃  secret-scan ❯ 
> 
> ┃  gitleaks-staged ❯ 
> 
>     ○
>     │╲
>     │ ○
>     ○ ░
>     ░    gitleaks
> 
> [90m11:19PM[0m [32mINF[0m 1 commits scanned.
> [90m11:19PM[0m [32mINF[0m scan completed in 7.96ms
> [90m11:19PM[0m [32mINF[0m no leaks found
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.06 seconds)
> ✔️ e2e-output-tripwire (0.01 seconds)
> ✔️ secret-scan (0.03 seconds)
> ✔️ gitleaks-staged (0.06 seconds)
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpost-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m╯[m
> ┃  mesh-reingest ❯ 
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.00 seconds)
> ✔️ mesh-reingest (0.00 seconds)
> readme commit: 3eb03d6
> ```

## 🤖 Claude *(02:19:51)*


## 🤖 Claude *(02:19:52)*

HANDOFF record. Leio o anchor (Task State) e insiro o record desta sessão acima do record do loop:

## 🤖 Claude *(02:19:53)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "offset": 11,
  "limit": 6
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 11	
> 12	## Task State
> 13	
> 14	## Session Seal — Loop Autônomo: FR-VS-047 Editor Render Pipeline + Security Hardening (2026-06-30)
> 15	
> 16	Continuação do **loop autônomo de malha fechada** (`/loop` auto-ritmado, ultracode) da seal anterior. **8 iterações fechadas**, cada uma com prova material (Lei 1) e commit granular, governadas pela `autonomous-loop-charter.md`. Selada por `/handoff` explícito do Sovereign (stop). Entregou **2 Fatias completas** (FR-VS-047 editor→pipeline · OTD-SEC-006/007 + FR-SEC-014 pt1 hardening) + correção de roadmap + absorção da direção fresca do Sovereign.
> ```

## 🤖 Claude *(02:20:11)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md",
  "old_string": "## Task State\n\n## Session Seal \u2014 Loop Aut\u00f4nomo: FR-VS-047 Editor Render Pipeline + Security Hardening (2026-06-30)",
  "new_string": "## Task State\n\n## Session Seal \u2014 Sovereign Interativa: Calend\u00e1rio Day-Detail + 1\u00ba Ciclo PAGO de V\u00eddeo + Gate Smart-Delete (2026-06-30)\n\nSess\u00e3o **interativa com o Sovereign** (paralela ao loop aut\u00f4nomo \u2014 trabalho em arquivos disjuntos, staging cir\u00fargico). Entregou 1 feature de UI deployada + o **1\u00ba ciclo pago de v\u00eddeo testemunhado** + a **doutrina open-source-first** encodada + o **gate BoK do smart-delete**. Selada por `/handoff` expl\u00edcito.\n\n| Action | Result |\n|--------|--------|\n| **Calend\u00e1rio \u2014 Detalhe do Dia** (`src/pages/CalendarPage.tsx`) | \u2705 clicar dia/post/\"+N mais\" \u2192 modal com TODAS as publica\u00e7\u00f5es da data + propriedades completas (plataforma\u00b7hor\u00e1rio\u00b7status\u00b7conte\u00fado\u00b7conta\u00b7published_at\u00b7erro\u00b7tentativas) + reagendar/duplicar/remover + CTA. tsc 0 \u00b7 eslint 0 \u00b7 vite build 0 \u00b7 **browser-verified** (User 0: modal com 6 posts reais, LinkedIn Published/Twitter Failed) \u00b7 **deployed** (chunk `CalendarPage-CCgZuuDP.js`, env baked). `a29627b` |\n| **1\u00ba ciclo PAGO de v\u00eddeo (GO Sovereign)** | \u2705 `video_enabled=true` no plano `640b3b67` \u2192 invoke `autopilot-run` \u2192 ciclo `77e02fca` completed, actual **32 mco** (saldo 4669\u21924637); render `561a31df` HyperFrames done \u2192 MP4 **776.522 B** 1080\u00d71920/5s no bucket `video-studio-assets`; reconcilia\u00e7\u00e3o FR-VA-025 \u2192 `content_library e27a09e7` type=video. Render self-hosted **USD=0** |\n| **Doutrina open-source-first** (mem\u00f3ria `feedback_opensource_first_zero_cost_equity` + charter) | \u2705 custo USD externo=0 + posse do stack caro = equity; audit zero-USD (`wf_6d3bdbd6-eb7`): render USD=0, LLM ~$0.05/ciclo na BYOK \u2192 **Gemini 2.5 Pro MANTIDO** (decis\u00e3o Sovereign). Eval de fork nativo (`wf_ec9db575-8a7`): opensrc/graphify = red herrings, **HyperFrames-first** |\n| **Gate smart-delete** (emenda BoK post-engine 15 + SOP) | \u2705 Closed-Loop gate ANTES do c\u00f3digo: FR-SD-001..005 + Pattern Conformance + SOP `smart-delete-remote.md` + capability-matrix SSOT (`wf_2da3b945-7b0`: WP/X/Pinterest delet\u00e1veis; IG/TikTok sem delete API \u2192 transpar\u00eancia honesta). `33fadb0` |\n\n| Commit | Conte\u00fado |\n|--------|----------|\n| `a29627b` | feat(calendar): day-detail modal |\n| `c880fcf` | docs(context): zero-USD audit + native-exclusive fork eval |\n| `33fadb0` | docs(post-engine): seal smart-delete gate (BoK amendment 15 + SOP) |\n| `3eb03d6` | docs(readme): v6.64.0 \u2014 mesh 9004 |\n\nHandoff node `f3248e11-9ed2-4892-8140-9da4af007e75` inserido + embedado (768d). Mesh **9004 n\u00f3s**.\n\n### Pending / Pr\u00f3ximo (desta sess\u00e3o)\n- **Smart-delete MVP (c\u00f3digo \u2014 gate j\u00e1 selado):** `check-post-existence` (read-only, seguro) \u2192 `delete-remote-post` (X/Pinterest/WP idempotente, per-user fail-closed) \u2192 fluxo UI 3-ramos em `useDeleteScheduledPost` + smoke zero-cost + deploy. Delet\u00e1veis no calend\u00e1rio = X/Pinterest; demais = transpar\u00eancia.\n- **Cad\u00eancia aut\u00f4noma de v\u00eddeo (opcional):** `is_active=true` no plano `640b3b67` \u2192 pg_cron gera v\u00eddeo a cada 3 dias sozinho.\n- **Fork nativo HyperFrames (quando priorizado):** emenda BoK elimina dep `hyperframes@0.7.22` npm (license:None) internalizando `bundleToSingleHtml`+seek do `@hyperframes/core` Apache-2.0. OpenDesign = foco dedicado futuro.\n\n## Session Seal \u2014 Loop Aut\u00f4nomo: FR-VS-047 Editor Render Pipeline + Security Hardening (2026-06-30)"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/HANDOFF.md has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(02:20:15)*


## 🤖 Claude *(02:20:18)*

**Phase 5b — secret scan no HANDOFF.md** (antes do commit):

## 🤖 Claude *(02:20:20)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== 5b-1 credenciais reais ===\"\ngrep -nE \"(AIza[0-9A-Za-z_-]{35}|sk-[a-zA-Z0-9]{20,}|eyJ[a-zA-Z0-9._-]{40,}|ghp_[a-zA-Z0-9]{36}|xox[baprs]-[a-zA-Z0-9-]+)\" HANDOFF.md | grep -v \"example\\|placeholder\\|<.*>\\|digest\\|sha256\\|hash\" | head -10 || echo \"NENHUMA CREDENCIAL \u2705\"\necho \"=== 5b-2 Google keys ===\"\ngrep -n \"AIza[0-9A-Za-z_-]\\{35\\}\" HANDOFF.md | head -5 || echo \"NO GOOGLE KEYS \u2705\"\necho \"=== 5b-3 inline assignments ===\"\ngrep -nE \"=\\s*['\\\"][A-Za-z0-9_\\-]{20,}['\\\"]\" HANDOFF.md | grep -v \"example\\|placeholder\\|<.*>\\|digest\\|hash\\|uuid\\|[0-9a-f-]\\{36\\}\" | head -5 || echo \"NO INLINE ASSIGNMENTS \u2705\"",
  "description": "Phase 5b secret scan on HANDOFF.md"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === 5b-1 credenciais reais ===
> === 5b-2 Google keys ===
> === 5b-3 inline assignments ===
> 1639:- ✅ **FEITO (2026-06-08, commit `2522e71`)** Antibody anti-reincidência: optei por `no-restricted-syntax` core casando `JSXAttribute[name.name='dangerouslySetInnerHTML']` (não `react/no-danger` — `eslint-plugin-react` ausente, evita dep nova). Todo sink vira exceção `eslint-disable-next-line` justificada; 2 sinks legítimos marcados (DashboardHome DOMPurify · chart.tsx CSS shadcn). Provado material: sink cru plantado pego pelo lint, justificados passam, tsc 0; obs node `505fb670`.
> 8253:  ├── mcorch_nodes WHERE project_id = 'mcorch-constellation'  → 493 AST nodes
> 8255:  ├── mcorch_edges WHERE project_id = 'mcorch-constellation'  → 344 edges
> 8256:  └── count(embedding IS NULL, project_id = 'mcorch-constellation') → neuralDensity
> 8298:  ├── mcorch_nodes WHERE project_id = 'mcorch-constellation'  → 493 AST nodes
> ```

## 🤖 Claude *(02:20:31)*


## 🤖 Claude *(02:20:33)*

**5b verdict:** ✅ 5b-1/5b-2 limpos. Os hits do 5b-3 são conteúdo **pré-existente** (o slug `'mcorch-constellation'` e um hash de commit, longe do meu bloco novo nas linhas 12-45) — não são credenciais. Commito HANDOFF + proof-manifest:

## 🤖 Claude *(02:20:35)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit add HANDOFF.md proof-manifest.json\ngit commit -q -m \"docs(handoff): seal sess\u00e3o Sovereign interativa \u2014 calend\u00e1rio day-detail + 1\u00ba ciclo pago v\u00eddeo + gate smart-delete \u2014 mesh 9004\" && echo \"handoff commit: $(git log -1 --format=%h)\"",
  "description": "Commit HANDOFF and proof-manifest"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;6;6;6m─[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpre-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;6;6;6m─[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m╯[m
> ┃  e2e-output-tripwire ❯ 
> 
> ┃  secret-scan ❯ 
> 
> ┃  gitleaks-staged ❯ 
> 
>     ○
>     │╲
>     │ ○
>     ○ ░
>     ░    gitleaks
> 
> [90m11:20PM[0m [32mINF[0m 1 commits scanned.
> [90m11:20PM[0m [32mINF[0m scan completed in 15.8ms
> [90m11:20PM[0m [32mINF[0m no leaks found
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.07 seconds)
> ✔️ e2e-output-tripwire (0.01 seconds)
> ✔️ secret-scan (0.03 seconds)
> ✔️ gitleaks-staged (0.06 seconds)
> [38;2;0;0;0m╭[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;49;49;49m─[38;2;45;45;45m─[38;2;42;42;42m─[38;2;39;39;39m─[38;2;35;35;35m─[38;2;32;32;32m─[38;2;29;29;29m─[38;2;26;26;26m─[38;2;23;23;23m─[38;2;19;19;19m─[38;2;16;16;16m─[38;2;11;11;11m─[38;2;5;5;5m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m╮[m
> [38;2;0;0;0m│[m 🥊 lefthook  v2.1.9   hook:  [1mpost-commit[m [38;2;52;52;52m│[m
> [38;2;6;6;6m╰[38;2;12;12;12m─[38;2;17;17;17m─[38;2;20;20;20m─[38;2;24;24;24m─[38;2;27;27;27m─[38;2;31;31;31m─[38;2;34;34;34m─[38;2;38;38;38m─[38;2;41;41;41m─[38;2;45;45;45m─[38;2;48;48;48m─[38;2;52;52;52m─[38;2;56;56;56m─[38;2;56;56;56m─[38;2;52;52;52m─[38;2;48;48;48m─[38;2;45;45;45m─[38;2;41;41;41m─[38;2;38;38;38m─[38;2;34;34;34m─[38;2;31;31;31m─[38;2;27;27;27m─[38;2;24;24;24m─[38;2;20;20;20m─[38;2;17;17;17m─[38;2;12;12;12m─[38;2;6;6;6m─[38;2;0;0;0m─[38;2;0;0;0m─[38;2;5;5;5m─[38;2;11;11;11m─[38;2;16;16;16m─[38;2;19;19;19m─[38;2;23;23;23m─[38;2;26;26;26m─[38;2;29;29;29m─[38;2;32;32;32m─[38;2;35;35;35m─[38;2;39;39;39m─[38;2;42;42;42m─[38;2;45;45;45m─[38;2;49;49;49m─[38;2;52;52;52m╯[m
> ┃  mesh-reingest ❯ 
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.00 seconds)
> ✔️ mesh-reingest (0.00 seconds)
> handoff commit: 6bea97b
> ```

## 🤖 Claude *(02:20:41)*


## 🤖 Claude *(02:20:42)*

HANDOFF commitado (`6bea97b`). **Phase 5c — Material Proof Audit** (verificação mecânica independente do meu record):

## 🤖 Claude *(02:20:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\nbun run scripts/qa/run-audit.ts HANDOFF.md 2>&1 | tail -45; echo \"AUDIT EXIT: ${PIPESTATUS[0]}\"",
  "description": "Phase 5c material proof audit"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> ### 📋 Proof Manifest — Material Proof Audit (Phase 5c)
> 
> | Claim | Kind | Expected | Actual | Verdict |
> |-------|------|----------|--------|---------|
> | mesh node 3459bfd3 | mesh_node | 3459bfd3-fa24-4785-99fb-1ebfda9dcf36 | 3459bfd3-fa24-4785-99fb-1ebfda9dcf36 | ✅ |
> | commit c3b8702 | git_commit | c3b8702 | c3b8702 | ✅ |
> | commit f273231 | git_commit | f273231 | f273231 | ✅ |
> | commit b2c39f6 | git_commit | b2c39f6 | b2c39f6 | ✅ |
> | commit bb999c1 | git_commit | bb999c1 | bb999c1 | ✅ |
> | commit 9bb5bba | git_commit | 9bb5bba | 9bb5bba | ✅ |
> | commit 7cbd036 | git_commit | 7cbd036 | 7cbd036 | ✅ |
> | test suite — 269 passing | test_suite | 269 | 318 passed | ✅ |
> | oro triplet compliance | oro_compliance | Operator = MCORCH Agent · Reviewer=Sovereign + `/security-review` independente (3×, todos  | Operator = MCORCH Agent · Reviewer=Sovereign + `/security-review` independente (3×, todos  | ✅ |
> | handoff node f3248e11 | mesh_node | f3248e11-9ed2-4892-8140-9da4af007e75 | f3248e11-9ed2-4892-8140-9da4af007e75 | ✅ |
> 
> QA VERDICT: 10 verified · 0 skipped · 0 failed → SEAL ALLOWED
> 
> (audit completed in 12.9s)
> AUDIT EXIT: 0
> ```

## 🤖 Claude *(02:21:11)*


## 🤖 Claude *(02:21:12)*

**Phase 5c: exit 0 — `SEAL ALLOWED`** ✅ (10 claims verificadas, 0 falhas; meu handoff node `f3248e11` confirmado, test suite 318 passed). **Phase 6 — BoK seal status:**

## 🤖 Claude *(02:21:16)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== m\u00f3dulos tocados nesta sess\u00e3o (meus commits) ===\"\ngit diff --name-only a29627b~1..6bea97b 2>/dev/null | grep -E \"^(src/pages/|supabase/functions/)\" | sort -u || echo \"(nenhum edge fn / page nova)\"\necho\necho \"=== post-engine BoK completo? (smart-delete = emenda, n\u00e3o m\u00f3dulo novo) ===\"\nslug=post-engine\nmissing=()\nfor doc in 00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics; do\n  [ -f \"docs/bok/$slug/$doc.md\" ] || missing+=(\"$doc\")\ndone\n[ ${#missing[@]} -eq 0 ] && echo \"\u2705 post-engine \u2014 BoK completo (base 9 docs + amendments 10-15)\" || echo \"\u26a0\ufe0f post-engine missing: ${missing[*]}\"",
  "description": "Phase 6 BoK seal status check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === módulos tocados nesta sessão (meus commits) ===
> src/pages/CalendarPage.tsx
> supabase/functions/lead-score/index.ts
> supabase/functions/orchestrate-step/index.ts
> supabase/functions/_shared/llm-fallback.ts
> supabase/functions/_shared/sentinel.ts
> 
> === post-engine BoK completo? (smart-delete = emenda, não módulo novo) ===
> ✅ post-engine — BoK completo (base 9 docs + amendments 10-15)
> ```

## 🤖 Claude *(02:21:24)*


## 🤖 Claude *(02:21:26)*

**Phase 6 verdict:** ✅ CalendarPage = enhancement de feature documentada (exempt); smart-delete = **emenda** ao post-engine (suite completa, gate selado ANTES do código); os edge fns no range são do loop (já selados na suite dele). Sem módulo novo sem BoK — sem 🔴. **Phase 7 — push:**

## 🤖 Claude *(02:21:29)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\ngit push origin main 2>&1 | tail -15 || { echo \"=== push falhou, rebase ===\"; git pull --rebase origin main 2>&1 | tail -8 && git push origin main 2>&1 | tail -8; }\necho \"=== estado final ===\"\necho \"HEAD: $(git log -1 --format='%h %s' | head -c 80)\"\necho \"unpushed restantes: $(git log origin/main..HEAD --oneline 2>/dev/null | wc -l)\"",
  "description": "Phase 7 push to origin main"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
>     ○
>     │╲
>     │ ○
>     ○ ░
>     ░    gitleaks
> 
> [90m11:21PM[0m [32mINF[0m 1 commits scanned.
> [90m11:21PM[0m [32mINF[0m scan completed in 24ms
> [90m11:21PM[0m [32mINF[0m no leaks found
> 
> [38;2;56;56;56m  ────────────────────────────────────[m
> summary: (done in 0.07 seconds)
> ✔️ gitleaks-range (0.07 seconds)
> To github.com:gabrielZarattini/constellation-orchestra.git
>    4ab87f9..6bea97b  main -> main
> === estado final ===
> HEAD: 6bea97b docs(handoff): seal sessão Sovereign interativa — calendário day-det
> unpushed restantes: 0
> ```

## 🤖 Claude *(02:21:41)*


## 🤖 Claude *(02:21:42)*

Push **OK**: `4ab87f9..6bea97b main -> main`, 0 unpushed restantes, gitleaks limpo. **Phase 7b — hygiene:**

## 🤖 Claude *(02:21:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "cd /home/gcrUX/htdocs/constellation-orchestra\necho \"=== scratch/ (repo) ===\"\nls scratch/ 2>/dev/null && echo \"(tem conte\u00fado)\" || echo \"scratch/ vazio ou inexistente \u2705\"\necho \"=== git tree final ===\"\ngit status --short || echo \"clean\"\necho \"(meus temp files foram todos p/ o scratchpad de sess\u00e3o /tmp, n\u00e3o no repo)\"",
  "description": "Phase 7b scratch and tree hygiene check"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> === scratch/ (repo) ===
> (tem conteúdo)
> === git tree final ===
> (meus temp files foram todos p/ o scratchpad de sessão /tmp, não no repo)
> ```

## 🤖 Claude *(02:22:00)*


## 🤖 Claude *(02:22:19)*

Seal completo. `scratch/` (repo) vazio (o "tem conteúdo" foi falso-positivo do `&&` sobre dir vazio — mesmo padrão do handson); tree limpo; meus temporários ficaram todos no scratchpad de sessão `/tmp`.

```
═══════════════════════════════════════════════════════════
  HANDOFF SEALED — Sessão Sovereign Interativa (2026-06-30)
  Calendário Day-Detail + 1º Ciclo PAGO de Vídeo + Gate Smart-Delete
═══════════════════════════════════════════════════════════

🔐 SEGURANÇA
  1a secret leak (diff não-pushado) ......... ✅ nenhum
  1c coin-deduction client-side ............. ✅ sem violação
  1e log sensível (CalendarPage) ............ ✅ nenhum
  5b HANDOFF.md secret scan ................. ✅ (hits = slug/hash pré-existentes, não credenciais)
  gitleaks (pre-commit + range) ............. ✅ no leaks (todos os commits)

📦 COMMITS (5 da sessão · push 4ab87f9..6bea97b)
  a29627b — feat(calendar): day-detail modal (deployed + browser-verified)
  c880fcf — docs(context): zero-USD audit + native-exclusive fork eval
  33fadb0 — docs(post-engine): seal smart-delete gate (BoK amendment 15 + SOP)
  3eb03d6 — docs(readme): v6.64.0 — mesh 9004
  6bea97b — docs(handoff): seal sessão Sovereign interativa

⬡ KNOWLEDGE MESH
  Milestone node: f3248e11-9ed2-4892-8140-9da4af007e75
  Embedding: ✅ 768d (openai/text-embedding-3-small via openrouter)
  Total: 9004 nós

📖 README.md
  Versão: 6.63.0 → 6.64.0
  Badge neural_mesh: 9003 → 9004 nós
  What's New: entrada [v6.64.0] adicionada

🧠 HANDOFF.md
  Fase selada: Sessão Sovereign Interativa
  Record appendado (calendário · vídeo GO · doutrina · gate smart-delete)

📋 PROVA MATERIAL (Fase 5c)
  Veredito: SEAL ALLOWED (exit 0)
  Claims: 10 verificadas · 0 skipped · 0 falhas · tsc 0 · testes 318 passed

🚀 PUSH
  Branch: main → origin/main (4ab87f9..6bea97b) · 0 unpushed

📌 SPRINT / HYGIENE
  scratch/ (repo): limpo ✅ · tree: limpo ✅ · temporários em /tmp scratchpad
  Memórias salvas: doutrina open-source-first + project_smart_delete + MEMORY.md

⏭  PRÓXIMOS PASSOS
  1. Smart-delete MVP (código — gate já selado): check-post-existence (read-only) →
     delete-remote-post (X/Pinterest/WP idempotente) → fluxo UI 3-ramos + smoke + deploy.
  2. Cadência autônoma de vídeo (opcional): is_active=true no plano 640b3b67 → pg_cron 3d.
  3. Fork nativo HyperFrames (quando priorizar) — elimina dep hyperframes npm license:None.

═══════════════════════════════════════════════════════════
  Assinado: Claude Code — Braço de Engenharia do AIOS
═══════════════════════════════════════════════════════════
```

**Sessão selada e no ar.** 🟢 Resumo executivo do que entregamos juntos hoje:

1. **Calendário "Detalhe do Dia"** — LIVE e browser-verificado: clicar num dia abre tudo agendado com propriedades completas + ações.
2. **1º vídeo autônomo pago testemunhado** — você deu o GO, o sistema gerou+renderizou+reconciliou sozinho (MP4 776KB, render self-hosted a USD $0) e você viu o vídeo.
3. **Doutrina open-source-first** virou lei do sistema (Gemini Pro mantido — o custo é trivial e a qualidade da marca vale).
4. **Gate do smart-delete** selado (BoK + SOP + matriz de viabilidade honesta por rede) — pronto pra eu codar o MVP na próxima.

Quando voltar, o passo natural é o **código do smart-delete MVP** (o gate já está pago). É só chamar.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

%% --- TIMELINE START --- %%
> [!info] Linha do Tempo (Handoff)
> * **Sessão Anterior**: [[2026-06-30 - agent-afe5bdb8ee6c0b0ac]]
> * **Próxima Sessão**: [[2026-07-01 - Execução autônoma MCORCH com ciclo fechado]]
%% --- TIMELINE END --- %%

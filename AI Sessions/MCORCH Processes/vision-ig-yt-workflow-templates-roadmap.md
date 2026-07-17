---
type: roadmap
status: draft
tags:
  - hub/mcorch
  - vision
  - roadmap
  - workflow-templates
  - lead/high-ticket
created: 2026-07-17
resume-env: ssh (Claude Code)
branch: claude/mcp-vision-capability-m0ec9m
related:
  - "[[vision-mcp-connector-install]]"
  - "[[MCORCH]]"
---

# 🎯 Roadmap — Vision IG · Vision YT · Workflow Templates (mcorch)

> [!warning] RETOMAR AMANHÃ — no host com SSH
> Este doc nasceu numa sessão do **Claude Code Web** (ambiente remoto isolado, **sem acesso ao servidor
> mcorch e sem PAT** — só alcança `mcp.mcorch.com` via HTTPS, retorna `401` sem token). Nada de Vision MCP
> foi executado aqui.
> **Amanhã:** retomar no **host com SSH** onde o Vision MCP soberano já roda (`/mcp` lista as 7 tools).
> Fluxo: `git pull` desta branch → seguir a **§4 Próximas ações**.

---

## 0. Objetivo (North Star)

Adicionar **workflow templates** ao ecossistema **mcorch**. O objetivo real não é analisar um perfil isolado —
é transformar o raciocínio "sinal → nicho → oferta → campanha" num **template reutilizável e automatizável**
dentro do mcorch, alimentado por percepção visual fundamentada (Vision MCP).

Para isso precisamos de **duas novas capabilities de percepção** (Vision IG + Vision YT) que hoje **não existem**
no Vision MCP soberano (que expõe 7 tools genéricas: `mesh_search`, `vision_describe_image`,
`vision_analyze_video`, `deepsearch_scrape`, `deepsearch_run`, `deepsearch_poll`, `mesh_consolidate_reference`).

> [!note] Lei 1 — Materialidade
> Tudo abaixo marcado **`PROPOSTO`** ainda **não** foi construído/validado. Não afirmar que existe até o
> handshake (`/mcp`) provar. As tools atuais são as 7 genéricas acima.

---

## 1. Capabilities a construir

### 1.1 Vision IG — analisador de conteúdo do Instagram `PROPOSTO (FR-VM-020)`

Analisador de conteúdo do Instagram, **principalmente vídeos**, cobrindo **todas as superfícies** do IG:

- **Superfícies:** feed (imagem/vídeo/carrossel), **reels**, **stories** (somente se **públicos**), bio/perfil,
  destaques, legendas, comentários públicos.
- **Transcrição:** áudio → texto dos vídeos/reels/stories (fala + texto on-screen quando viável).
- **Saída estruturada:** por post → tipo, gancho (primeiros 3s), tema/episódio, CTA, sinais de marca,
  proveniência (URL + timestamp). Consolidável na malha via `mesh_consolidate_reference`.
- **Tools propostas** (novas, a desenhar): `vision_ig_scrape` (coleta perfil/posts), `vision_ig_analyze_video`
  (percepção de reel/vídeo), `vision_ig_transcribe` (fala + OCR on-screen). *(nomes provisórios)*
- **Guardrails:** stories só se públicos; respeitar login-wall (a tool recusa conteúdo logado, como
  `/competitive-vision` já faz); Lei 1 — nunca inventar métrica/legenda que a coleta não retornou.

### 1.2 Vision YT — analisador de conteúdo do YouTube `PROPOSTO (FR-VM-030)` ⚠️ sensível a custo

> [!danger] Constraint de custo (decisão de arquitetura)
> Vídeo longo processado **frame-a-frame** fica **caríssimo**. O YT NÃO pode usar o mesmo caminho "denso"
> do IG. Tem que ser **sob demanda**, por um **agente específico e único, reservado só para isso**.

Estratégia de custo (transcript-first, visão cirúrgica):

1. **Transcript primeiro** — captions/ASR é barato e cobre ~80% do conteúdo semântico. Roda sempre.
2. **Visão só sob demanda** — nunca frame fixo. Usar **keyframe / scene-change sampling** (amostra por corte
   de cena) e/ou frames que o agente pede **por timestamp** com base no transcript.
3. **Agente dedicado com teto de budget** — fila reservada, ceiling de mcoCoins/frames por job; recusa/parcial
   se estourar. Nada de long-video denso disparado por engano.
4. **Cache agressivo** — `mesh_consolidate_reference` grava o resultado; reprocessar o mesmo vídeo = cache hit.
- **Tools propostas:** `vision_yt_transcribe` (barato, default), `vision_yt_keyframe_analyze` (on-demand,
  budget-guarded), orquestradas pelo agente dedicado. *(nomes provisórios)*

---

## 2. Workflow Template semente — "Modelagem de Oferta a partir de Nicho"

O mapa mental GLP-1 (Anexo A) e o vídeo (Anexo B) **são o primeiro template**. Extrair a estrutura como
pipeline reutilizável que o mcorch executa/automatiza:

| Etapa | Pergunta que responde | Insumo (via Vision/DeepSearch) |
|---|---|---|
| 1. Sinal de nicho | O que está explodindo agora? | deepsearch + Vision IG/YT sobre criadores/anúncios |
| 2. Por que agora | Qual o gatilho/timing? (dado duro) | deepsearch_run + fontes citadas |
| 3. Dor (ranqueada) | Qual dor vale mais $? | análise de conteúdo + comentários |
| 4. Já vende lá fora? | Validação de mercado maduro | deepsearch (Gumroad/Etsy/apps) |
| 5. Barreira de entrada | Por que ninguém subiu? (compliance) | políticas Meta 2026 |
| 6. Sub-nichos | Front-end vs back-end, ticket | síntese |
| 7. Oferta modelada | Front / order bump / upsell / recorrência | template de copy |
| 8. Métricas-alvo | Ticket médio, CPA, CPM | benchmark |
| 9. Ativos | Página de vendas + criativos | design + creative gen |

O exemplo **preenchido** (GLP-1 "canetas emagrecedoras") está no Anexo A — usar como caso de referência do
template. Este é o entregável que os leads da §3 pagariam para automatizar.

---

## 3. Prospects high-ticket (leads)

Dois criadores que **já faturam alto** (conforme seus canais/redes) → candidatos a **high ticket** para
workflow templates automatizados no mcorch.

- **Lead A — `@drogarthas` (Instagram).** Criador produzindo **"episódios"** (formato série). Objetivo original
  deste thread: analisar os episódios e montar roadmap de conteúdo. **Bloqueio atual:** IG me deu `HTTP 429`
  (login-wall) via WebFetch; é exatamente o caso de uso do **Vision IG (§1.1)**. → analisar amanhã no SSH.
- **Lead B — criador de YouTube (marketing digital), autor da transcrição (Anexo B).** Afirma ter feito
  **1M+ de faturamento** em nichos (Free Fire, atividades escolares); no vídeo destrincha o nicho GLP-1 e monta
  oferta + sobe Facebook Ads. → analisar canal com **Vision YT (§1.2)**, respeitando o teto de custo.
- **Ângulo comercial:** ambos operam no eixo "modelagem de oferta"; o template da §2 automatiza o que eles
  fazem à mão → dor real + capacidade de pagar.

---

## 4. Próximas ações (amanhã, no host SSH)

- [ ] `git pull` desta branch no host com SSH (Vision MCP ativo, `/mcp` = 7 tools).
- [ ] **Lead A / Vision IG:** rodar coleta do perfil `@drogarthas` (feed + reels + stories públicos) →
      transcrever → mapear os "episódios" (tema, gancho, CTA, cadência) → roadmap de conteúdo.
- [ ] **Lead B / Vision YT:** transcript-first do canal do criador; visão só sob demanda (keyframes) → validar
      o ângulo GLP-1 e o padrão de oferta.
- [ ] **Design das tools §1** (`vision_ig_*`, `vision_yt_*`): definir contratos, escopos do PAT, custo por tool,
      e o **agente dedicado de YT** com teto de budget.
- [ ] **Template §2:** materializar "Modelagem de Oferta a partir de Nicho" como workflow template no mcorch,
      usando o GLP-1 (Anexo A) como fixture de referência.
- [ ] Consolidar achados na malha (`mesh_consolidate_reference`) para reuso.

---

## 5. Compliance / guardrails (não negociável)

- **Política Meta 2026 (emagrecimento):** só 18+; sem antes/depois idealizado; sem citar quantidade de peso;
  sem promessa com prazo; sem gerar autopercepção corporal negativa. Meta apertou "atributos pessoais
  implícitos" — frases tipo "você não consegue emagrecer" caem fácil.
- **Produto de exemplo:** não substitui acompanhamento médico, **não indica nem vende medicamento**, e tem
  **nutricionista registrado assinando** — em letra grande na página. (Protege e converte melhor.)
- **Lei 1 — Materialidade:** só afirmar fato que veio de fonte retornada pela pesquisa/coleta. Nunca fabricar
  legenda, métrica ou fonte.

---

## Anexo A — Mapa mental (fonte bruta, colada pelo usuário)

> Material de aula · julho de 2026 · "O mar azul das canetas emagrecedoras" (nicho de suporte a GLP-1).

**Tese:** o remédio (caneta GLP-1) resolve a fome, mas não resolve *o que comer*, *como não perder músculo*
e *como não recuperar tudo ao parar*. O nicho é **o manual de instruções que a farmácia não entrega** —
não vender remédio, não vender emagrecimento.

- **01 · Por que agora (janela abriu em 2026):** R$ 13,3 bi movimentados (Mounjaro/Wegovy/Ozempic, mai/25–mai/26);
  Mounjaro sozinho R$ 8,5 bi. Mounjaro: 208.508 → 4.524.183 unidades/ano (~+2.070%). Projeção R$ 20 bi em 2026,
  ~924 redes / 13 mil+ farmácias. Gatilho: patente da semaglutida caiu em **20/03/2026** (STJ negou extensão à
  Novo Nordisk). Ozivy (EMS) chegou em **15/06/2026** a R$ 498/caneta (vs. R$ 929–1.308/mês do Ozempic).
  IQVIA/BTG projetam queda de 50–60% no preço em até 2 anos; Anvisa analisa ~20 canetas novas. Preço caindo =
  usuários multiplicando (12–24 meses); cada novo usuário é alguém perdido sobre o que fazer.
- **02 · A dor (ranqueada por $):** (1) **Reganho ao parar** — recupera ~2/3 do peso em 1 ano; Oxford: reganho
  4x mais rápido; food noise volta mais forte (a mais monetizável). (2) **Perda de massa magra** — até 40% do
  peso perdido é massa magra sem proteína/treino; recomendação 1,2–1,6 g/kg. (3) **"O que como agora?"** —
  náusea, constipação, queda de cabelo, aversão a comida. Medo que abre a carteira: "gastei R$ 10 mil, emagreci
  20kg, e agora vou perder tudo."
- **03 · Já vende lá fora:** Gumroad ("The Fat Jab Cookbook"; "GLP Reset – The After Plan", 132 pág., US$ 37);
  Etsy (trackers de injeção, journals, Google Sheets); apps ("Weightly – Mounjaro Tracker"). Modelagem pronta,
  só traduzir/adaptar ao BR.
- **04 · Por que ninguém subiu:** espaço ocupado por clínica/nutricionista/telemedicina/blog — **zero player de
  marketing digital**. Barreira = política Meta (ver §5). Mata o infoprodutor médio (só sabe criativo antes/depois).
- **05 · Sub-nichos:** A) Manutenção pós-caneta (dor: medo de recuperar; ticket R$ 197–497; concorrência ZERO) —
  *back-end*. B) Cardápio na caneta (dor: "o que como?"; R$ 27–47; quase zero) — *front-end*. C) Treino
  antissarcopenia (dor: perder músculo/flacidez; R$ 97–197; zero).
- **Oferta exemplo — "Protocolo Caneta Inteligente":** promessa sem número/prazo/antes-depois. Front R$ 37
  (30 cardápios porção pequena alta proteína + lista de compras mercado/iFood + protocolo antináusea + tracker).
  Order bump R$ 27 (40 receitas proteicas 5 min). Upsell 1 R$ 197 (Fase 2: desmame, como o apetite volta,
  segurar peso 12 meses). Recorrência R$ 47/mês (comunidade + updates). **Ticket médio projetado R$ 90–130;
  CPA alvo R$ 25–40 (público frio, CBO, 18+).**
- **Fontes citadas no material:** Close-Up International Brasil · InfoPrice · Brazil Journal/BTG/IQVIA · Anvisa ·
  Meta Transparency Center · Gumroad · Etsy.

---

## Anexo B — Transcrição do vídeo (fonte bruta, colada pelo usuário)

> Vídeo de um criador de marketing digital (YouTube) apresentando o nicho GLP-1 e montando oferta + Facebook Ads.
> Preservado na íntegra como fonte para o Vision YT (§1.2) e o template (§2).

Rolou uma época aqui no marketing digital que você vender qualquer produto do nicho de games, como por exemplo de Free Fire, era lucro na certa. Eu mesmo embarquei nessa oportunidade e fiz mais de 1 milhão de faturamento na época, vendendo o aplicativo de Free Fire. Rolou também a época das atividades escolares, aonde qualquer um, até mesmo iniciante, que subia a oferta nesse nicho, ganhava dinheiro. Eu acho que eu encontrei um novo nicho tão promissor quanto esse, ou até mais. Vou explicar o porquê e junto a gente vai criar uma oferta na prática desse nicho. Vamos também subir o Facebook Ads.

O nicho é o de **canetas emagrecedoras**. Estava no Paraguai e lá se fala muito sobre isso — toda esquina tem anúncio — e não vejo tanta oferta assim para o digital. Fiz um mapa mental para mostrar e passar uma oferta de graça. É um nicho onde a indústria farmacêutica gasta muito com marketing, o pessoal abraça, e ninguém no digital está aproveitando o hype. A oferta mais parecida que lembro era o "Monjaro de Pobre". Deixo claro: **não é golpe** — não vende a caneta e não entrega, não vende Nutra (farinha disfarçada de remédio). É legal, para pessoas que de fato usam essas substâncias com receita. É um nicho de **suporte** para quem usa as canetas — não vende remédio, não vende Nutra, não vende nem emagrecimento; vende o "manual de instrução"/a bula que a pessoa pula.

Pesquisei e juntei as informações relevantes (não fui no Google, usei IA). A quantidade de dinheiro movimentado com Monjaro/Ozempic (evoluções uma da outra) é insana. A dor: as canetas dão resultado, mas a pessoa **para de usar e volta a engordar tudo**, porque não estava comendo por não sentir fome; quando volta a sentir, volta a comer. Perde massa magra/músculo, e fica sem saber o que comer. Entendo um pouco do nicho porque minha mãe é nutricionista (não atua mais) e tenho gente na família que usou.

Validei porque **já achei essas ofertas lá fora** (não no Brasil): uma no "Gun Road" (Gumroad) de receitas; um PDF sobre apetite pós-caneta; outra em Google Sheets (planilhas/PDFs); e apps/microSaaS. Funciona vendendo ebook, entregável em vídeo, ou nível app (o melhor, mas exige mais tempo). **Por que ninguém subiu:** nutricionistas e médicos falam, mas a galera do digital fica na bolha (vê games escalando, roda games; vê atividades, roda atividades), sem perceber nichos novos surgindo — como Copa do Mundo, mas esse é bem mais "low profile".

Três sub-nichos/ofertas: manutenção pós-caneta (dor de perder o que conquistou); receitas/cardápio na caneta (sempre funciona com hype novo); e treino **antissarcopenia** (para quem perde massa magra). Joguei os tickets alto porque é o que essa galera pagaria (não é barato tomar as canetas), mas a ideia é rodar low ticket, geralmente com dois planos (ex.: começo por ~R$ 10 e outro por ~R$ 47).

Oferta montada — front-end: 30 cardápios para quem come pouco, alta densidade proteica em porção pequena; lista de compras (mercado e iFood); protocolo antináusea; tracker de aplicação (mais voltado a microSaaS). Dica: reduzir o "bafo" (quem usa fica com bafo). Order bump: uma receitinha. Upsell/recorrência: comunidade no Telegram ("network dos monjareiros"). Ticket médio projetado ~R$ 90–130 (mais realista que os valores altos do mapa). CPA viável ~R$ 20–25 (duas ofertas); CPM projetado ~R$ 40–50.

Prática: vou na **Biblioteca de Anúncios do Facebook** e pesquiso por "emagreça" (nicho parecido). Acho uma clínica com bastante anúncio e página bonita, copio o link e uso um prompt de IA para analisar a página (cores, design, componentes) e gerar um MD de design — dá para fazer isso de graça no Claude. Depois: "com base nesse MD de design, cria agora uma página de vendas para essa oferta" + colo a oferta. Peço dois planos (em vez de um), substituir todas as imagens, e deixar 100% responsivo (mobile/PC/tablet). Ele gera a página de vendas completa, com feedbacks, degradê, dois planos. Dá para publicar como artefato no Claude e copiar o link (não é o melhor host — dá para hospedar em Netlify/Vercel).

Campanha: Gerenciador de Anúncios do Facebook → criar campanha de **vendas**; orçamento de campanha (ex.: US$ 8/dia, conta em dólar para não pagar imposto); conjunto único de site; "obter conversões de todos os públicos"; selecionar o pixel; evento de conversão **sempre "Comprar"** (nunca inicializar/finalização). Estratégia de lance: limite de lance (bid) ~metade entre R$ 37 e R$ 10 (~R$ 25); rodar de madrugada; público Brasil (tirar EUA); manter Advantage e posicionamentos automáticos. Criativo (não é o foco do vídeo): recomendo vídeos formato TikTok — pesquisar sintomas de quem tomou (pele flácida, náusea, dificuldade de exercício), recortar, narrar por cima (voz IA, ex.: ElevenLabs), CTA "clica no link para saber mais".

Por que compartilho o nicho em vez de rodar sozinho: não dá para abranger todos os públicos (homem/mulher/idoso/jovem/medo de reganho/ganho de massa) — vou pegar uma nutricionista/médica e explorar um ângulo (ex.: homens que emagreceram mas ficaram com "pochete", ensinar a entrar em shape). Quem for rodar, me chama no Instagram para trocar ideia. Tenho cursos na descrição.

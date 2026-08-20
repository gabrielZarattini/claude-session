# SOP — MCORCH Model Specialist Factory (`mcorch_model`)

> **Lei 2 (Processo Antecipado) + spec de engenharia.** Este documento é a Fonte da Verdade do
> pipeline que destila o conhecimento da Sovereign (Knowledge Mesh + Handoffs + BoK + AST) num LLM
> especialista self-host, `mcorch_model`, servido no rail Ollama já provado no host.
>
> **Classificação de governança:** **TOOLING INTERNO DO AIOS** (Lei 2, exceção de tooling), não módulo
> tenant-facing. O pipeline **lê** a mesh (PostgREST read-only), **não** escreve em produção, **não**
> toca RLS/mcoCoins/edge-functions no caminho do usuário, e o modelo resultante é um ativo de dev/ops
> interno. Por isso o gate Closed-Loop (MRD/BRD/PRD/FRD/SDD em `docs/bok/`) **não** é pré-requisito —
> este SOP satisfaz o gate de processo. Se a Sovereign quiser promover a suíte BoK completa (ex.: se o
> modelo virar produto tenant-facing), aciona-se `bok-curator`/`deepsearch-blueprint` antes desse salto.

- **Slug:** `mcorch-model-pipeline`
- **Status:** SOP selado · Fase 3 (extrator) e Fase 4 (inferência) implementadas · ativação do container GATED (ação Sovereign)
- **Autor:** MCORCH Master Execution Agent · **Data:** 2026-08-17
- **SSOT de código:** `scripts/ai/build-mcorch-sft-dataset.ts` (extrator) · `docker-compose.yml` serviço `mcorch-model-inference` · `docker/mcorch-model/Modelfile`

---

## 0. ORO triplet

| Papel | Quem | Critério |
|-------|------|----------|
| **Operator** | MCORCH Master Execution Agent (ou `engineer` L1) | executa extração, treino remoto, quantização, registro no Ollama |
| **Reviewer** | Sovereign (Gabriel) | aprova o dataset sanitizado, o gasto RunPod, e a ativação do container |
| **Owner** | Sovereign | risco material: (a) vazamento de segredo no dataset, (b) colisão de porta com prod, (c) custo GPU externo |

---

## 1. Realidade material do ambiente (auditoria 2026-08-17 — Fase 1)

> Números medidos por prova material (Lei 1), não estimados. Fonte: `docker ps`, PostgREST count exato, `ollama /api/tags`.

### 1.1 Knowledge Mesh (cloud `bcyvddsykvehvpwstlfa`)

| Métrica | Valor medido |
|---------|--------------|
| `mcorch_nodes` (total) | **21.091** |
| `mcorch_edges` (total) | **25.587** |
| Nós **sem** embedding (`embedding is.null`) | **1.193** (cobertura 94,3%) |
| `node_type` distintos | **25** |

**Distribuição por `node_type`** (coluna real é `node_type`, **não** `type`):

| # | node_type | count | Camada do corpus |
|---|-----------|-------|------------------|
| 1 | `ast_variable` | 12.328 | 20% código (tier-2: path+assinatura+200c) |
| 2 | `observation` | 2.700 | 40% dialética/MAPE-K (lições operacionais) |
| 3 | `ast_function` | 1.889 | 20% código |
| 4 | `ast_arrow_function` | 1.035 | 20% código |
| 5 | `ast_file` | 1.010 | 20% código |
| 6 | `ast_interface` | 760 | 20% código (contratos TS) |
| 7 | `ast_type_alias` | 435 | 20% código |
| 8 | `handoff` | 230 | 30% arquitetura/handoffs |
| 9 | `documentation_suite` | 139 | 30% arquitetura (índice das suítes BoK) |
| 10 | `conversation` | 117 | 40% dialética |
| 11 | `vault_note` | 95 | 40% dialética |
| 12 | `news_pulse` | 89 | (excluído — ruído externo) |
| 13 | `crew_agent` | 79 | 10% tool-calling / papéis |
| 14 | `markdown_file` | 77 | 30% arquitetura |
| 15 | `milestone` | 39 | 30% arquitetura/decisão |
| — | `ast_class` 21 · `content_mesh_asset` 14 · `decision` 12 · `architecture` 7 · `design_artifact` 5 · `feature` 4 · `ui-ux` 2 · `system` 2 · `requirement` 1 · `bugfix_milestone` 1 | | cauda |

**Achado que reorienta a Fase 3:** os nós puramente arquiteturais tipados (`decision`+`architecture`+`milestone`+`feature`+`requirement` ≈ **63 nós**) são escassos — o conhecimento de arquitetura vive de fato nos **230 handoffs**, nas **39 suítes `docs/bok/`** e nos **119 SOPs `docs/processes/`**, não nos nós `decision`. Logo o extrator **combina mesh + filesystem** para atingir a fatia de 30% de arquitetura.

### 1.2 Rail de inferência já existente (host)

- **Ollama nativo do host** em `127.0.0.1:11434` — já serve 3 modelos GGUF `Q4_K_M` on-CPU:
  `gemma4:latest` (8.0B, 9,6 GB), `llama3.1:8b` (4,9 GB), `qwen3.5:latest` (9,7B, 6,6 GB).
- **`ollama-proxy`** em `127.0.0.1:11435` (container).
- **Fato decisivo:** o host já roda modelos 8B Q4_K_M em CPU. Um `mcorch_model` 7–8B Q4_K_M herda esse rail **sem custo novo** — é só um `Modelfile` novo no daemon existente.

### 1.3 Docker Sovereign Mesh — portas em uso (Fase 4 não pode colidir)

| Porta (loopback) | Serviço |
|---|---|
| 80/443 | CloudPanel / nginx (**PROD — intocável**) |
| 3000 | `mega-brain-dashboard` (0.0.0.0) |
| 3100 | `mcorch_gitnexus` (definido no compose) |
| 3200 | `mcorch_vision_mcp` |
| 5432 | `n8n-postgres` · 3306 `tradeux-db` (mysql) |
| 5678 | `n8n` · 7456 `open-design` · 8001 `mcorch_chroma` |
| 8000 | `mega-brain-webhook` (0.0.0.0) · 8090/8095 tradeux/studio |
| **11434** | **Ollama host nativo** · **11435** `ollama-proxy` |

Rede: `constellation-orchestra_mcorch-sovereign-net` (bridge). **Porta livre escolhida para o container dedicado: `127.0.0.1:11436`** (mapeia →11434 interno do container). Zero colisão.

### 1.4 Restrição de hardware (governa o topology)

- **Oracle Cloud ARM64 Ampere A1, CPU-only (sem GPU).** Treino QLoRA **não roda aqui** → GPU alugada (RunPod).
- **Host memory-constrained** — precedente de OOM (`docs/.../host-capacity-and-oom-2026-08-05.md`): um agente inchou a 15,6 GB e derrubou o host. Um 2º daemon Ollama sempre-ligado disputa RAM com 15 containers. → **topology primário = registrar no Ollama host** (carrega/descarrega sob demanda); container dedicado é opção isolada, ativação gated.

---

## 2. Taxonomia de treino (distribuição do corpus)

Mistura-alvo do dataset SFT, mapeada às fontes materiais medidas na §1.1:

| Fatia | Peso | Fonte material | Como vira par de treino |
|-------|------|----------------|--------------------------|
| **Dialética MaaS/SaaS/TaaS + MAPE-K** | **40%** | `observation` (2.700) + `conversation` (117) + `vault_note` (95) | Q: sintoma/dilema operacional → A: a síntese/anticorpo (lição do nó). Reforça o loop Monitor→Analyze→Plan→Execute→Knowledge. |
| **Decisões de arquitetura + Handoffs** | **30%** | `handoff` (230) + `docs/bok/**` (39 suítes) + `docs/processes/**` (119 SOPs) + `milestone`/`decision`/`architecture` | Q: "qual a arquitetura/decisão de X?" → A: o SDD/SOP/seal correspondente, com IDs de FR/OTD. |
| **Contratos Edge/TS/SQL RLS** | **20%** | `src/hooks/**` (112) + `supabase/functions/**` (107) + `supabase/migrations/**` + AST tier-2 (17k nós como índice) | Q: "escreva/explique o contrato do hook/edge/migration X" → A: o código real (sanitizado). |
| **Tool-calling MCP** | **10%** | `crew_agent` (79) + `.claude/agents/**` + `.claude/skills/**` + contratos MCP (`packages/vision-mcp-core`, gitnexus) | Q: "quando/como chamar a tool/agente Y?" → A: o gatilho + assinatura + gates de recusa. |

**Regras de balanceamento:** downsampling de `ast_variable` (12k é ruído se não filtrado — manter só os exportados/assinaturas ricas); `news_pulse` **excluído** (ruído externo, não é doutrina MCORCH); dedup por hash de conteúdo; teto de tokens por par (§5).

---

## 3. Protocolo de Sanitização Zero-Trust (FMEA-SEC)

> **Fail-closed:** um par que dispara qualquer regra de segredo é **redigido** (`⟨REDACTED:tipo⟩`) ou, se o segredo for o corpo inteiro, **descartado** — nunca incluído "na dúvida". A prova material (Lei 1) exige **0 hits** de um re-scan adversarial sobre o JSONL final.

### 3.1 Prior art reaproveitada

- `supabase/functions/_shared/sentinel.ts` — Cyber-Sentinel: prior art de **injeção de prompt** (7 famílias EN + 7 pt-BR). É reusada como camada L2 (não injetar amostra hostil no dataset), **mas não faz redação de segredo** — por isso o extrator adiciona uma **camada de redação nova** abaixo.
- `.claude/scripts/scan-supply-chain-iocs.ts` — scanner de IoC (supply-chain), referência estrutural.

### 3.2 Famílias de segredo (regex — construídas sobre os formatos REAIS do `.env` + provedores)

| FM-SEC | Alvo | Padrão (regex, `g`) |
|--------|------|---------------------|
| FM-SEC-01 | Supabase secret key | `sb_secret_[A-Za-z0-9_-]{20,}` |
| FM-SEC-02 | Supabase publishable | `sb_publishable_[A-Za-z0-9_-]{20,}` |
| FM-SEC-03 | JWT (legacy service_role/anon, PAT) | `eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}` |
| FM-SEC-04 | literal `service_role` em contexto de credencial | `\bservice_role\b(?=["'\s:=].{0,40}(key\|token\|secret))` |
| FM-SEC-05 | Stripe secret/restricted | `\b(sk\|rk)_(live\|test)_[A-Za-z0-9]{20,}` |
| FM-SEC-06 | OpenAI/OpenRouter | `sk-(or-v1-)?[A-Za-z0-9]{20,}` |
| FM-SEC-07 | Replicate | `\br8_[A-Za-z0-9]{20,}` |
| FM-SEC-08 | Apify | `apify_api_[A-Za-z0-9]{20,}` |
| FM-SEC-09 | Google API key | `AIza[0-9A-Za-z_-]{35}` |
| FM-SEC-10 | Higgsfield / genérico `*_API_KEY=` valor | `(?i)(higgsfield\|api[_-]?key\|secret\|token)["'\s:=]{1,4}[A-Za-z0-9_\-]{24,}` |
| FM-SEC-11 | SSH/PEM private key | `-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----` |
| FM-SEC-12 | AWS access key | `\bAKIA[0-9A-Z]{16}\b` |
| FM-SEC-13 | GitHub token | `\bgh[pousr]_[A-Za-z0-9]{30,}` |
| FM-SEC-14 | Telegram bot token | `\b\d{8,10}:AA[A-Za-z0-9_-]{30,}` |
| FM-SEC-15 | PII e-mail (exceto allowlist da casa) | `[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}` → redige se **não** ∈ {`gabrielcall@gmail.com`, `gabrielcallr@icloud.com`, domínios `@mcorch.com`, `@example.com`} |
| FM-SEC-16 | UUID de usuário real (tenant) | `[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}` → **pseudonimizado** para `⟨USER:hash8⟩` (preserva co-referência sem vazar o tenant) |
| FM-SEC-17 | Connection string Postgres | `postgres(ql)?://[^\s"'<>]+` |
| FM-SEC-18 | Bearer/Authorization header com valor | `(?i)(authorization\|bearer)["'\s:=]{1,4}[A-Za-z0-9._\-]{20,}` |

### 3.3 Regras estruturais (além do regex)

1. **Nunca ler `.env`, `.env.*`, `*.pem`, `id_rsa*`, `supabase/.temp/`, `**/secrets/**`** — allowlist de diretórios de fonte, não blocklist.
2. **Entropia:** qualquer token contíguo `[A-Za-z0-9_\-]{40,}` com entropia de Shannon > 4,0 bits/char → redige (`⟨REDACTED:high-entropy⟩`) mesmo sem casar família nomeada. Rede de segurança contra chave de formato desconhecido.
3. **Descartar o par inteiro** se, após redação, o conteúdo ficar < 40 chars úteis (era essencialmente o segredo).
4. **Re-scan adversarial obrigatório (gate G-SANITIZE):** após gerar o JSONL, roda-se todas as famílias §3.2 + a heurística de entropia sobre o arquivo final. **Exit 1 se ≥ 1 hit.** Sem isso, não se declara "dataset pronto".

---

## 4. Unit Economics & FinOps

| Item | Especificação |
|------|---------------|
| **Método** | QLoRA 4-bit (NF4) via **Unsloth** (2× throughput, 70% menos VRAM) |
| **Base model** | `Qwen2.5-7B-Instruct` (Apache-2.0, tool-calling forte → serve a fatia 10% MCP) — fallback `Llama-3.1-8B-Instruct` (já provado no host como `llama3.1:8b`). Ambos suportados pelo Unsloth. |
| **GPU alvo** | RunPod **RTX 4090** (24 GB, ~US$ 0,34–0,44/h) ou **L40S** (48 GB, ~US$ 0,86/h) |
| **Orçamento** | **< US$ 4,00** — ex.: 4090 por ~3 epochs sobre ~5–15k pares SFT ≈ 1,5–3 h ≈ **US$ 0,60–1,30**; teto folgado de US$ 4 cobre re-runs |
| **Hiperparâmetros** | LoRA r=16, α=16, dropout=0, `lr=2e-4`, cosine, `max_seq_len=4096`, epochs 2–3, grad-accum p/ batch efetivo 16 |
| **Quantização de saída** | export GGUF **`q4_k_m`** (via `llama.cpp convert` + `quantize`, ou export nativo do Unsloth) → herda o rail Q4_K_M do host |
| **Registro** | `ollama create mcorch_model -f docker/mcorch-model/Modelfile` (o Modelfile aponta o `.gguf` local) |
| **Custo de inferência** | **US$ 0** — CPU do host, sob demanda (Ollama descarrega ocioso). Alinhado à doutrina open-source-first / USD=0. |

---

## 5. Sequência operacional (o fluxo humano — Lei 2)

| # | Step | Comando / ação | Gate de verificação (critério material) |
|---|------|----------------|------------------------------------------|
| 1 | **Extrair dataset** | `bun run scripts/ai/build-mcorch-sft-dataset.ts --limit 200` (sample) então full | JSONL gerado em `scratch/dataset_mcorch_sft_v1.jsonl`; log imprime contagem de pares + distribuição por fatia |
| 2 | **Sanitizar (gate G-SANITIZE)** | o próprio script roda o re-scan §3.4 no fim | **exit 0 + "0 secret hits"** no stdout; senão exit 1 e **não** subir |
| 3 | **Validar higiene JSONL** | script valida cada linha `JSON.parse` + shape ChatML/ShareGPT + token count | "N/N linhas válidas", tokens dentro do teto |
| 4 | **Revisão humana** | Sovereign lê uma amostra do JSONL | GO explícito da Sovereign p/ gastar GPU |
| 5 | **Treino remoto** | RunPod: notebook Unsloth QLoRA (§4) sobre o JSONL | loss decrescente; checkpoint salvo; custo < US$ 4 (fatura RunPod) |
| 6 | **Quantizar** | export GGUF `q4_k_m` | `ls -la mcorch_model.q4_k_m.gguf` (size ~4–5 GB) |
| 7 | **Registrar no Ollama host** | `ollama create mcorch_model -f docker/mcorch-model/Modelfile` | `ollama list \| grep mcorch_model` + `ollama run mcorch_model "..."` responde no registro MCORCH |
| 8 | **(Opcional) Container dedicado** | `docker compose up -d mcorch-model-inference` | `docker ps \| grep mcorch_model_inference` healthy; `curl 127.0.0.1:11436/api/tags` lista o modelo. **GATED — ação Sovereign** |
| 9 | **Nó na malha** | inserir `milestone` node "mcorch_model v1 trained" | UUID retornado do INSERT (Mesh Connection Mandate) |

### Recovery path

- **Step 1 falha (PostgREST 401/PGRST):** `SB_SECRET_KEY` rotacionada → reler `.env`; ver `reference_supabase_secret_key_rotation_silent_kill`.
- **Step 2 exit 1 (segredo detectado):** o script imprime o **tipo + linha + hash** (nunca o segredo cru). Endurecer a família em §3.2, re-extrair. **Nunca** commitar/subir o JSONL sujo.
- **Step 5 estoura orçamento:** matar o pod; RTX 4090 spot < L40S; reduzir epochs p/ 2.
- **Step 7 OOM no host:** o modelo compete com 15 containers; rodar em janela de baixa carga (o `load-sentinel */1` avisa); preferir Qwen2.5-7B (menor) a 8B.

### Success signal

`ollama run mcorch_model "Qual a Lei 1 do SSP-01 e como se prova materialidade?"` responde citando **Materialidade + prova física (UUID/commit/ls/curl)** no registro executivo pt-BR da casa — provando que a destilação pegou a doutrina, não só o formato.

---

## 6. Pattern Conformance (mini-declaração — tooling)

Como tooling interno, a declaração é leve (não os 21 padrões cheios). Padrões agênticos que o pipeline materializa:

| Padrão | Impl.? | Como |
|--------|--------|------|
| Knowledge Retrieval (RAG-source) | yes | lê a mesh como corpus de destilação |
| Tool Use / Function Calling | yes | fatia 10% ensina o modelo a chamar tools/agentes MCORCH |
| Guardrails / Safety | yes | Sanitização Zero-Trust §3 (fail-closed) |
| Self-Reflection / Evaluation | deferred | eval harness do `mcorch_model` fica p/ v2 (OTD-MODEL-EVAL) |
| Memory | yes | destila `observation`/`handoff` (memória de longo prazo da casa) |

---

## 7. Conexão com a malha (Mesh Connection Mandate)

- Nó de observação/milestone inserido no primeiro treino bem-sucedido (Step 9).
- Falha em qualquer step → entrada em `infra_health_logs` (`service='mcorch-model-pipeline'`).
- Rastreabilidade: este SOP ↔ `scripts/ai/build-mcorch-sft-dataset.ts` ↔ `docker/mcorch-model/Modelfile`.

---

## 8. Lições materiais do primeiro treino (2026-08-18/19 — anticorpos permanentes)

O primeiro ciclo completo (5 runs, ~US$ 3 total, RTX 4090 RunPod) produziu o `mcorch_model` v5 VIVO no
Ollama do host (`sha256:93490c73858a3908` · ollama ID `dea709c1ea87`) e quatro anticorpos:

| FM | Lição | Anticorpo |
|----|-------|-----------|
| **FM-TRAIN-01** | `save_pretrained_merged` da **Unsloth 2026.5.9 CORROMPE o merge** — provado por A/B: v3 E v4 coerentes in-training, salada pós-merge; merge peft do MESMO adapter saiu limpo. | NUNCA usar o merge da Unsloth. Treino salva SÓ o adapter (`mcorch_lora/`); merge canônico via `scripts/ai/merge-lora.py` (transformers+peft `merge_and_unload`, base fp16). |
| **FM-TRAIN-02** | Gate pós-merge no MESMO processo do treino quebra (`'Qwen2Attention' has no attribute 'apply_qkv'`) — o monkey-patch da Unsloth vaza para o load do transformers. | O sanity do artefato final SEMPRE roda em **processo separado e limpo** (o merge-lora.py já embute). |
| **FM-TRAIN-03** | **SFT = VOZ, não enciclopédia.** O fato derivou em TODAS as receitas (v1 "self-healing", v2 "LGPD", v3 drift de definição); e o cram de fato (flashcards 15× + r=32 + 2 epochs, v3) causou **overfit catastrófico**. A receita que serve é a SUAVE: r=16/α=16, 1 epoch, doutrina leve (~4×), sem cram. | Fatos vêm do **SYSTEM prompt** (cânone no Modelfile — o teste da Lei 1 passou por isso) e do **RAG da mesh** (fase 2). O fine-tune entrega registro, formato e comportamento. |
| **FM-TRAIN-04** | `save_pretrained_gguf` da Unsloth roda `sudo apt-get` e TRAVA em imagem sem sudo (prendeu a v1 no prompt de senha). | Export GGUF desacoplado: `scripts/ai/export-gguf.sh` (build userspace do llama.cpp, `convert_hf_to_gguf.py` + `llama-quantize`). |

Fluxo selado do treino: `train-mcorch-qlora.py` (adapter-only) → `merge-lora.py` (peft, processo limpo, sanity no artefato) → `export-gguf.sh <merged_dir>` → `runpodctl send` → host `ollama create`. Aviso `fix_mistral_regex` do tokenizer = cosmético (testado: não era a causa de nada).

## 9. RAG da Knowledge Mesh (fase 2 do "Ambos" — fato vem da malha, voz vem do fine-tune)

**Ferramenta:** `scripts/ai/mcorch-ask.ts` — pergunta → embedding da query (OpenRouter
`openai/text-embedding-3-small` `dimensions:768`, o MESMO espaço em que a mesh foi embedada) →
RPC `match_mcorch_nodes` (threshold **0.3** — calibração selada; 0.45 zerava tudo) → top-K nós
injetados como CONTEXTO no prompt → `mcorch_model` responde na voz treinada citando as fontes.

```bash
bun run scripts/ai/mcorch-ask.ts "Por que o EP07 foi reprovado?"
bun run scripts/ai/mcorch-ask.ts --k 6 --show-context "<pergunta>"   # inspeciona o contexto
bun run scripts/ai/mcorch-ask.ts --no-rag "<pergunta>"               # baseline sem mesh (A/B)
```

Regras de projeto (aprendidas em teste live no host):
- **Transporte = curl subprocess, nunca fetch do Bun:** no CPU a prompt-eval leva minutos sem emitir
  byte, e o fetch do Bun tem idle-timeout interno (~300s) que mata a conexão antes do 1º token.
- **`keep_alive: "30m"`** na chamada — evita recarregar 4,7 GB do disco entre perguntas.
- **Contexto enxuto** (K=4 × 800 chars default) — cada token de contexto custa prompt-eval no CPU;
  `num_ctx=4096` do Modelfile é o teto duro.
- **Fallback keyword** (`ilike` PostgREST) quando o embedding falhar — degrada, não quebra.
- O prompt declara o contexto como fonte da verdade que **vence a memória do modelo** — é isso que
  corrige o drift factual residual do SFT (FM-TRAIN-03).

## 10. Referências

- Auditoria material Fase 1: esta sessão (2026-08-17).
- `docs/architecture/agentic-vision.md` — 21 padrões (SSOT da Pattern Conformance).
- `.claude/rules/survival.md` — Leis 1–4.
- `supabase/functions/_shared/sentinel.ts` — prior art de injeção.
- Precedente de OOM: `.claude/context/host-capacity-and-oom-2026-08-05.md`.

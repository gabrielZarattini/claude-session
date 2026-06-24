# SOP — Creative QA Vision Gate (olho criativo antes do crédito real)

> **Lei 2 (Processo Antecipado).** Documenta o processo humano de validar um creative visual com um "olho
> criativo" (VLM via Vision MCP) e o **portão de consistência** que precede QUALQUER gasto de crédito pago de
> vídeo (Higgsfield DoP/Kling). Nenhuma automação deste fluxo ganha código antes deste SOP.
>
> **Origem (Diretiva Sovereign 2026-06-21):** "sem criativo a única coisa que funciona é texto… quando gerar
> os vídeos principalmente os com frame inicial e frame final precisa estar consistente para usar os créditos
> reais que coloquei no Higgsfield." + "Lembre-se de sempre salvar os assets reais desde sempre."

Relacionado: [`canvas-node-consistency.md`](canvas-node-consistency.md) (reference threading + seed lock) ·
[`canvas-video-async-execution.md`](canvas-video-async-execution.md) (DoP async + webhook) ·
[`vision-mcp-pat-and-erasure.md`](vision-mcp-pat-and-erasure.md) (PAT do tenant).

---

## ORO

| Papel | Quem |
|-------|------|
| **Operator** | MCORCH Master Execution Agent (ou o humano operando o Canvas Studio) |
| **Reviewer** | Sovereign + o próprio olho criativo (VLM) como reviewer mecânico de qualidade/consistência |
| **Owner** | Sovereign — blast radius = crédito Higgsfield real queimado + asset publicado |

---

## Princípio nº1 — sempre persistir o asset real (Lei 1)

Todo creative gerado (imagem ou vídeo) **DEVE** terminar como um arquivo material em storage com row em
`vm_canvas_assets` (bucket `canvas-assets`). `canvas-execute` já faz isso: baixa os bytes do provider, faz
upload no bucket e grava `public_url` + `storage_key`. **Nunca** confiar na URL efêmera do provider — ela
expira. A prova de sucesso é a row `vm_canvas_assets` + o objeto no bucket, nunca o retorno da API do provider.

## Princípio nº2 — BYOK torna o QA grátis

`vision_describe_image` resolve a chave `openrouter` per-user; `vision_analyze_video` resolve `google`
per-user. O Usuário Zero tem ambas → **QA custa 0 mco**. O olho criativo pode rodar quantas vezes for
preciso sem gastar; só a GERAÇÃO (imagem ~10 mco, vídeo DoP ~125 mco) custa.

---

## Operator — quem executa hoje

O operador gera creatives no Canvas Studio (`/dashboard/canvas/:id`) ou via `scripts/canvas-campaign-build.ts`,
e roda o olho criativo via `scripts/qa/vision-qa.ts` (handshake MCP+PAT contra `mcp.mcorch.com`).

Ferramentas:
- **Geração:** `canvas-execute` edge fn (precisa de user-JWT — mintar com `scripts/qa/gen-user-jwt.ts`).
- **Olho criativo:** `scripts/qa/vision-qa.ts {image|video|compare}` (precisa de `VISION_MCP_PAT` no `.env`).

---

## Sequence — ordem com critério de sucesso material por step

1. **Gerar frame-inicial (imagem).** `canvas-execute` `node_type=generate_image`, seed travado
   (`parameters.seed=<S>`), provider que funciona (OpenRouter `google/gemini-2.5-flash-image` ou Replicate
   `flux-1.1-pro`). **Sucesso:** HTTP 200 + `output_url` público + row `vm_canvas_assets` (asset A).
2. **Gerar frame-final (imagem) consistente.** Mesmo `seed=<S>` + `reference_image_urls:[<output_url do A>]`
   (reference threading) + prompt que descreve o MESMO produto/sujeito noutra pose/momento. **Sucesso:** row
   `vm_canvas_assets` (asset B) com `public_url`.
3. **Portão de consistência (olho criativo).** `vision-qa.ts compare <url_A> <url_B>`. O VLM descreve ambos
   com a mesma pergunta estruturada (produto/cores/ângulo/iluminação/estilo). O Operator (ou um juiz VLM
   dedicado) compara: **mesmo produto? mesmas cores dominantes? mesma identidade visual?**
   **Sucesso (GATE):** os dois descritivos batem nos atributos-chave → consistente. **Custo:** 0 (BYOK).
4. **SÓ SE o gate passar — gerar vídeo DoP (crédito real).** `canvas-execute` `node_type=image_to_video`,
   `input_asset_url=<url do frame escolhido>`, `model=dop-standard`. Path async → `higgsfield-webhook`
   finaliza (download → upload → `deduct_mco_coins` → row asset). **Sucesso:** `vm_canvas_executions`
   status `success` + asset vídeo ≥ 100 KB no bucket + ledger `canvas_video_spend`.
5. **QA do vídeo (olho criativo).** `vision-qa.ts video <signed_url do vídeo> "o vídeo é coerente com o
   produto/cena? há artefatos?"`. **Sucesso:** `confidence` ≥ medium + descrição coerente com os frames.
6. **Persistir o veredito na malha (opcional, 1 mco).** `mesh_consolidate_reference` grava o verdict de QA
   como nó `observation` tenant-scoped (rastreabilidade).

---

## Verification gates (o que o operador confere)

| Gate | Evidência material |
|------|--------------------|
| G1 — asset persistido | row `vm_canvas_assets` com `public_url` + objeto no bucket (`storage_key`) |
| G2 — frame-inicial OK (olho) | `vision_describe_image` `confidence ≥ medium` + descrição bate com o prompt |
| G3 — **consistência** (PORTÃO) | `compare` → mesmos atributos-chave (produto/cores/identidade) nos 2 frames |
| G4 — débito atômico | row `mcoin_transactions` `action=canvas_video_spend` com `amount` correto |
| G5 — vídeo material | asset vídeo ≥ 100 KB + `vm_canvas_executions.status=success` |
| G6 — vídeo coerente (olho) | `vision_analyze_video` descreve cena coerente com os frames |

---

## Recovery path — falha por step

- **Step 1/2 falha (provider error / texto em vez de imagem):** o prompt parece instrução ou está longo
  demais — reformular como descrição visual (ou usar Magic Prompt). Se for endpoint morto, ver
  `generate-image` (reparo do path de provider). Sem débito em path de erro (canvas-execute só debita no
  sucesso para imagem).
- **Step 3 reprova (frames inconsistentes):** **NÃO prosseguir pro vídeo.** Regenerar o frame-final com o
  MESMO seed e reference threading mais forte (passar a imagem upstream como `reference_image_urls`), ou
  ajustar o prompt para repetir os atributos-chave (cor/material/ângulo). Repetir o compare. Custo de cada
  re-tentativa de imagem ~10 mco; o gate evita o desperdício de 125 mco de vídeo sobre frames ruins.
- **Step 4 falha (Higgsfield 402/credenciais/timeout):** o webhook marca `failed` e **não debita**
  (deduct só pós-upload-OK). Reentrada: re-submeter; órfão → watchdog/poll de status. Crédito real só sai
  com vídeo material no bucket.
- **Step 5 reprova (vídeo incoerente):** o crédito já foi gasto (irreversível) — registrar o verdict na
  malha (step 6) como aprendizado e ajustar prompt/motion_strength na próxima. Este é exatamente o
  desperdício que o gate G3 existe para minimizar ANTES do gasto.

---

## Success signal — sinal materialmente observável do flow completo

Cadeia frame-inicial → frame-final **consistente** (G3 verde) → vídeo DoP material no bucket (G5) →
olho criativo confirma coerência (G6), com o débito de 125 mco gasto **uma única vez** e **somente** sobre
frames que passaram pelo portão de consistência. Assets reais persistidos em `vm_canvas_assets` (Lei 1).

---

## Anti-patterns proibidos

- ❌ Gastar crédito Higgsfield (vídeo) sem o portão G3 de consistência ter passado.
- ❌ Reportar "vídeo gerado" sem o asset ≥ 100 KB no bucket + row de execução `success` (Lei 1).
- ❌ Confiar na URL efêmera do provider em vez de re-hospedar no bucket.
- ❌ Rodar o olho criativo sobre uma signed URL expirada (re-assinar antes; ou usar `public_url`).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

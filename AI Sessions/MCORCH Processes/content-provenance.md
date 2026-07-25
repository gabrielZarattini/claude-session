# SOP — Content Provenance (AI Act Art. 50) · Pipeline de marcação end-to-end · Lei 2

> **Status:** ATIVA v1.0 · 2026-07-23 · Lei 2 (Processo Antecipado). **BoK SSOT:** `docs/bok/content-provenance/` (FR-CP-001..013 · PROC-CP-001..005 · OTD-CP-001..016).
> **O que este SOP é:** a **SOP-processo canônica** que o gate Closed-Loop referencia (`docs/bok/content-provenance/00-index.md §9`) — o processo humano/sistema completo geração→detectar-origem→embed(C1/C2/C3)→verify-before-claim→`register_creative_asset`→nó observação→fail-soft, com critério material por passo, gates, recovery e ORO. Fecha o pré-requisito Lei 2 que trava QUALQUER código de marcação.
> **Runbook operacional irmão:** `docs/processes/content-provenance-marking.md` — instalação (ExifTool/`c2patool` no host aarch64), contrato empírico do `c2patool 0.27`, estratégia de cert, habilitar o daemon, e as testemunhas E2E (`bc03a65a`/`d57e3341`). **Este SOP modela o PROCESSO; o runbook detalha a OPERAÇÃO.** Os dois são complementares e cruzam-referência; nenhum substitui o outro.
> **Deadline regulatório:** AI Act Art. 50(2) vigora **2026-08-02** (multa Art. 99 até €15M ou 3% do faturamento mundial — https://artificialintelligenceact.eu/article/99/).
> **Convenção MCORCH:** identificadores/lógica/tooling/logs/estados em inglês (`provenance-bridge`, `claim`, `verify`, `embedded`, `preserved`, `failed`, `trainedAlgorithmicMedia`); texto de UI/disclosure/validação em PT-BR ("Conteúdo gerado por IA").

---

## ORO triplet

- **Operator:** MCORCH Master Execution Agent (autoria) + o host-worker `provenance-bridge` (runtime).
- **Reviewer:** Sovereign.
- **Owner:** **Sovereign** — blast radius material: **sanção AI Act Art. 99 até €15M/3%** *e* o falso-sucesso de declarar "marcado" um asset que saiu **sem manifest/watermark** (FM-CP-01, RPN 378). O consumidor último é o Usuário Zero, cujo conteúdo sintético precisa ser **detectável como IA-gerado** pelas plataformas e reguladores da UE.

## Operator

| Papel | Quem (hoje) | Ferramenta |
|---|---|---|
| Motor de geração (produz o asset) | `generate-image`/`canvas-execute` (imagem, edge) · `video-bridge`/`veo-poll` (vídeo, host) · `voice-bridge` (voz, host) | asset aterrissa no bucket privado com `provenance_status='pending'` |
| Marcador (runtime) | host-worker `provenance-bridge` (systemd-user, molde `video-bridge`, 1-job/vez) | `scripts/provenance-bridge.ts` + `exiftool` (`libimage-exiftool-perl`) + `c2patool` (cert-gated, dormente) |
| Writer único do estado | `register_creative_asset` (RPC, SECURITY DEFINER, `search_path=''`, service-role) | grava `provenance_*` na spine `creative_assets` (DG-8/NFR-CP-007) |
| Owner | Sovereign | absorve a sanção Art. 99 e o falso-`embedded` (FM-CP-01) |

## Maturidade por Fatia (honestidade Lei 1 — VIVO vs GATED)

| Fatia | Camada | Estado material | FR-CP | Gate externo (Sovereign) |
|---|---|---|---|---|
| **0** | Colunas `provenance_*` + writer estendido + enum IPTC | 🟢 **VIVO** — migration `20260716230000` aplicada (`/security-review` NO FINDINGS, FMEA-011); `src/lib/provenance.ts` = enum SSOT | 012, 013 | — |
| **1** ⭐ | **C3 metadata IPTC/XMP** (imagem+vídeo) | 🟢 **VIVO** — motor `embed-iptc-core.ts` (ExifTool `XMP-iptcExt:DigitalSourceType`, verify-before-claim); worker sweep `pending`; witness E2E 2026-07-16 (`bc03a65a` img + `d57e3341` vídeo) | 005, 006, 007, 009, 010 | — |
| **2** | **C1 C2PA** (imagem+vídeo+**voz**) | 🟡 **CÓDIGO VIVO, MOTOR DORMENTE (safe-by-default)** — `embed-c2pa-core.ts` cert-gated: sem `C2PA_SIGN_CERT`/`C2PA_PRIVATE_KEY` retorna `{skipped:'no_cert'}`, prod inalterada (C3-only) | 001, 002, 003, 004 | **OTD-CP-003** (cert C2PA) · **OTD-CP-012** (revisão jurídica do self-signed) · **OTD-CP-004** (sondar origem `gemini-2.5-flash-image` antes de preservar-e-anexar) |
| **3** | **C2 watermark invisível** (TrustMark/VideoSeal/AudioSeal) | 🔴 **GATED — sem código** | 008 | **OTD-CP-009** (compute PyTorch/GPU) · **OTD-CP-014** (robustez OmniSealBench antes de SLA) |
| **4** | **Disclosure humano Art. 50(4)** server-side | 🔴 **GATED — sem código** (`[GATED]` na FRD) | 011 | **OTD-CP-002** (enquadramento provider-vs-deployer — **decisão jurídica do Sovereign**) · OTD-CP-011 |

> **Gate de código (Lei 1):** este SOP autoriza continuar as Fatias 0-1 (já vivas) e destrava a Fatia 2 **apenas na dimensão de processo** — o **código** da Fatia 2 permanece dormente até o cert (OTD-CP-003) + jurídico (OTD-CP-012); Fatia 3/4 continuam **sem código** até seus OTDs fecharem. Nenhuma linha de código de watermark (Fatia 3) ou disclosure (Fatia 4) nasce deste documento.

## Sequence (PROC-CP-001 — marcar um asset sintético, por asset)

Ponto de injeção invariante (DG-1): **marcar no momento da geração, após o asset no bucket privado**, sem tocar na distribuição. O worker é fail-soft e verify-before-claim.

1. **Claim / sweep** — `SELECT creative_assets WHERE provenance_status='pending'`, `kind IN ('image','video')` quando C1 dormente OU `('image','video','audio')` quando C1 ativo (áudio só entra com C1 — IPTC não cobre áudio, OTD-CP-007); **exclui** `source_module='external'` (o MCORCH não gerou → marcar seria FABRICAR proveniência, Lei 1) e `storage_bucket='local'` (masters de host, não baixáveis do Storage). *Critério material:* N linhas pendentes retornadas; job idempotente (re-run não duplica).
2. **Download** do objeto do bucket privado (service-role — RLS bypass; objeto owner-scoped). *Critério:* bytes no temp path.
3. **Detect-origin (preservar-e-anexar — FR-CP-004)** — antes de tocar bytes, `readC2paManifest`/probe detecta assinatura de origem (C2PA/SynthID de Nano Banana Pro/Vertex/Veo). Se presente, o original é passado como `-p <parent>` ⇒ vira `ingredient parentOf` (nunca re-encode cego — FM-CP-02/G4). *Critério:* origem detectada e classificada `signed`|`mcorch`. ⚠️ Cobertura de origem de `gemini-2.5-flash-image` **não confirmada** (OTD-CP-004) — na dúvida, tratar como `mcorch` e embutir (redundância grátis é bônus, não premissa).
4. **Route layers (PROC-CP-001 gateway `origin`/`kind`)** — `routeLayers(kind, origin)`: `image/video → [C1 c2patool, C3 ExifTool]`; `audio → [C1 c2patool]` (C3 impossível — OTD-CP-007). *Critério:* cadeia determinística selecionada.
5. **Vocabulário honesto (FR-CP-010/G5)** — `source_type = trainedAlgorithmicMedia` (100% IA) OU `compositeWithTrainedAlgorithmicMedia` (AI-editado: reshape/inpaint/outpaint via `open-design`/`hyperframes`). *Critério:* enum resolvido dentro do CHECK do schema (mentir o vocabulário é rejeitado por construção — FM-CP-12).
6. **Embed C1 (C2PA — cert-gated)** — `embedC2paMarker`: assina para um **output temp** (c2patool nunca assina in-place), manifesto com `c2pa.actions→c2pa.created→digitalSourceType=<URI>` + assertion `org.mcorch.asset={asset_id}` (**só uuid opaco**, nunca PII — FR-CP-008/OTD-CP-013). Dormente sem cert ⇒ `{skipped:'no_cert'}`, aditivo, não bloqueia C3. *Critério:* `c1.ok` OU `c1.skipped` (dormente é estado honesto, não falha).
7. **Embed C3 (IPTC — imagem/vídeo)** — `embedIptcMarker`: `exiftool -overwrite_original -XMP-iptcExt:DigitalSourceType=<URI>`. Voz pula (OTD-CP-007). *Critério:* `c3.ok`.
8. **VERIFY-before-claim (FR-CP-005 — o gate anti-falso-sucesso, DG-3)** — cada camada relê o que escreveu: C1 = `readC2paManifest(output)` confirma `digitalSourceType` round-trip (ancorado na assertion, não na confiança da CA — `untrusted-issuer` é esperado em dev, gate de prod OTD-CP-003); C3 = `exiftool -s3` relê a mesma URI. **`provenance_layers` = a UNIÃO REAL das camadas que VERIFICARAM.** *Critério:* ≥1 camada verificada; se zero ⇒ passo 10 (failed). **Nenhuma transição a `embedded` sem output de verify (FM-CP-01 RPN 378).**
9. **Re-upload in-place** (`upsert`, mesma key → signed URLs seguem válidas). O `rename` sobre o original só ocorre **pós-verify** (o bucket permanece intacto se o verify falha). *Critério:* upload sem erro.
10. **Flip terminal via writer único** — `register_creative_asset`/`UPDATE` service-role grava `provenance_status='embedded'|'preserved'`, `provenance_layers` (união real), `provenance_source_type`, `provenance_embedded_at=now()`, `c2pa_sidecar_key` (só se o motor produziu sidecar — FLAC/OGG, hoje NULL). *Critério:* linha em estado terminal com prova de verify.
11. **Nó observação na malha** (`mcorch_nodes` `observation` + `embed-mcorch-node`, best-effort fail-soft — FR-CP-012 §4/#8 Memory Management). *Critério:* nó inserido (ou fail-soft silencioso — a marcação é o money-path, não o nó).
12. **Telemetria** — `infra_health_logs service='content-provenance'` (`provenance_embedded` | `provenance_failed`), 1 linha por path. *Critério:* linha registrada.

**Sub-processos:**
- **PROC-CP-002 (re-embed C3 pós-transformação — FR-CP-007):** o reframe do `reshape-pillar` reescreve o arquivo e **DROPA o XMP** (FM-CP-03 RPN 294) ⇒ a transformação reseta `provenance_status='pending'` e o sweep re-marca; variante AI-editada usa `compositeWithTrainedAlgorithmicMedia`; verify **no publicado** (não no intermediário).
- **PROC-CP-003 (preserve-and-attach):** sub-fluxo do gateway `origin='signed'` do passo 3 — anexa assertion sem re-encode; verify confirma origem **intacta** + assertion presente ⇒ `status='preserved'`.
- **PROC-CP-004 (disclosure Art. 50(4) — GATED):** hook no publish de deepfake/texto de interesse público; rótulo "Conteúdo gerado por IA" montado **server-side** (nunca via prompt do LLM), exceção HITL editorial/artística. **Não codificado — gated por OTD-CP-002.**
- **PROC-CP-005 (orphan sweep — recovery):** cron re-enfileira/marca `failed` jobs `pending` além do budget; **fail-open, jamais promove a `embedded` sem verify** (Lei 1/FM-CP-01).

## Verification gates

| Gate | Prova material | FR/PROC |
|---|---|---|
| **G1** verify-before-claim | worker só marca `embedded`/`preserved` com o output de verify (C1 `c2patool verify` round-trip da `digitalSourceType` + C3 `exiftool -s3` relê a URI); sem verify ⇒ `failed` | FR-CP-005 · FM-CP-01 |
| **G2** objeto REAL carrega o marcador | baixar fresco do bucket → `exiftool -s3 -XMP-iptcExt:DigitalSourceType <obj>` = a URI (provado 2026-07-16, `bc03a65a` img + `d57e3341` vídeo); C1 → `c2patool <obj>` exibe manifesto `Valid` | FR-CP-006 · G2 runbook |
| **G3** DB terminal honesto | `SELECT provenance_status, provenance_layers` = estado terminal com a **união real** das camadas que verificaram | FR-CP-012 |
| **G4** sem falso-positivo | arquivo virgem → `readIptcMarker`/`readC2paManifest` = null/`hasManifest:false` (smoke) | FR-CP-005 |
| **G5** zero PII no payload | manifesto/watermark carrega SÓ `asset_id` (uuid opaco); `smoke-provenance-pii-reject.ts` FALHA se aparecer `user_id`/email/`project_id` | FR-CP-008 · OTD-CP-013 |
| **G6** não marca o que o MCORCH não gerou | `source_module='external'` e `storage_bucket='local'` excluídos do sweep (marcar seria fabricar proveniência) | Lei 1 · passo 1 |
| **G7** dormência C1 segura | sem cert → `{skipped:'no_cert'}` com log; prod C3-only INALTERADA; restart do daemon **não** liga C2PA | OTD-CP-003 · C2-G3 runbook |
| **G8** smoke hermético re-executável | `bun run scripts/qa/smoke-provenance-iptc.ts` 6/6 (gera PNGs próprios; zero DB/bucket/rede); C1 = `smoke-provenance-c2pa.ts` (gera cert dev + PNG/WAV) | AT-CP-001/005/006 |
| **G9** licença comercial-safe | tooling só MIT/Apache/Artistic (ExifTool/c2patool); GO recusa non-commercial | NFR-CP-005/G8 · FM-CP-15 |

## Recovery path

- **Embed/verify falha** (formato exótico, binário OOM/timeout) → `provenance_status='failed'` (fail-soft) + `infra_health_logs` degraded; o asset **permanece publicável**; NUNCA declara marcado sem verify. Re-tentar: `UPDATE creative_assets SET provenance_status='pending' WHERE id=<id>` (service-role) — o sweep re-pega `pending`, não `failed` (evita loop).
- **Objeto corrompido pós-embed** → o verify-before-claim bloqueia ANTES do re-upload (o `rename`/upsert só ocorre pós-verify); o original no bucket permanece intacto.
- **C1 falha mas C3 verifica** (imagem/vídeo) → `provenance_layers=['iptc']`, `embedded` honesto (C1 é aditivo). **C1 falha e é a única camada** (áudio) → `failed` fail-soft; re-tentar após corrigir cert/formato.
- **XMP dropado por transformação** (reshape/inpaint) → PROC-CP-002: a transformação reseta para `pending` e o sweep re-marca; verify **no asset publicado**.
- **Origem seria corrompida pela anexação** (PROC-CP-003) → **abortar** a anexação, `status='failed'`; **jamais** re-encodar cego (preservar-e-anexar > marcar — FM-CP-02/G4).
- **Worker morto (job pendurado em `pending`)** → PROC-CP-005 (orphan sweep) re-enfileira (asset ainda no bucket) ou marca `failed` (`event='orphan_reaped'`, asset sumiu) — fail-open, nunca falso `embedded`.
- **Backlog dos ~90 assets legados** (todos nasceram `pending` com a migration) → `bun run scripts/provenance-bridge.ts --once --limit N` em lotes, OU habilitar o daemon (systemd — **gate Sovereign**; habilitar re-uploada objetos legados = mutação de produção).

## Success signal

Um asset de imagem/vídeo **REAL**, baixado do bucket, carrega `XMP-iptcExt:DigitalSourceType` = a URI IPTC — legível por qualquer verificador (ExifTool, Meta, LinkedIn, X). Provado E2E 2026-07-16 (`bc03a65a` imagem + `d57e3341` vídeo). Para C1 (Fatia 2, pós-cert): `c2patool <obj>` exibe manifesto assinado `c2pa.created → digitalSourceType=<URI>`, `validation_state: Valid` — **witness em prod = ação Sovereign pós-gate de cert** (não marcamos prod com cert ligado sem GO). O sinal regulatório final é o **rótulo VISÍVEL** que a plataforma exibe pós-upload — a validar por **upload-teste** material (confiança MEDIUM: Meta re-encoda e pode strip metadata — §10 blueprint).

---

## O que ainda TRAVA o código das Fatias 2/3/4 (OTDs do Sovereign — não decidíveis pelo agente)

Estes gates são **externos** e **jurídicos/de-infra** — pertencem ao Sovereign, não ao bok-curator (Lei 1 — o agente não inventa enquadramento jurídico nem provisiona cert):

- **OTD-CP-002 — enquadramento provider-vs-deployer (Art. 3):** decisão **jurídica** que determina QUAL obrigação recai (Art. 50(2) machine-readable do provider vs 50(4) disclosure do deployer). Erro = obrigação errada (FM-CP-09). **Bloqueia a selagem de FR-CP-011 / toda a Fatia 4.**
- **OTD-CP-003 — estratégia de cert C2PA:** self-signed dev → CA na C2PA trust list. Sem isso, C1 fica dormente. **Bloqueia a Fatia 2 em prod.**
- **OTD-CP-012 — revisão jurídica do self-signed** (aceitar "untrusted-but-valid" no beachhead?). Acompanha OTD-CP-003.
- **OTD-CP-004 — sondar C2PA/SynthID de origem em `gemini-2.5-flash-image`:** P0 de integridade do preserve-and-attach (não assumir `signed`).
- **OTD-CP-009 — orçamento de compute** dos watermarkers PyTorch (VideoSeal GPU). **Bloqueia a Fatia 3.**
- **OTD-CP-014 — robustez sem benchmark:** validar OmniSealBench antes de prometer qualquer SLA de robustez. **Bloqueia SLA da Fatia 3.**
- **OTD-CP-015 — nome/versão/licença de `c2pa-node`** (confirmar antes de pinar) · **OTD-CP-010 — timeline Digital Omnibus** (núcleo 2-ago-2026 vale; não desenhar assumindo delay).

## Lineage & cross-reference

- **BoK SSOT:** `docs/bok/content-provenance/` (00-index §9 gate status · 04-frd FR-CP · 07-process-flow PROC-CP).
- **Runbook operacional irmão:** `docs/processes/content-provenance-marking.md` (instalação · contrato empírico c2patool 0.27 · cert · daemon · witnesses).
- **Código VIVO (Fatia 0-1) / DORMENTE (Fatia 2):** migration `supabase/migrations/20260716230000_content_provenance_columns.sql` · `src/lib/provenance.ts` · `scripts/provenance/embed-iptc-core.ts` · `scripts/provenance/embed-c2pa-core.ts` (cert-gated) · `scripts/provenance-bridge.ts` · `scripts/systemd/provenance-bridge.service` (NÃO habilitado = gate Sovereign) · `scripts/qa/smoke-provenance-iptc.ts`.
- **Doutrina:** SSP-01 Lei 1 (Materialidade) + Lei 2 (Processo Antecipado); MCORCH Master Execution Protocol §1 (Closed-Loop) + §3.5 (Pattern Conformance).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

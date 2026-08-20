# SOP — Marcação de Proveniência (AI Act Art. 50) · content-provenance Fatia 0-1

> **Status:** ATIVA v1.0 · 2026-07-16 · Lei 2. **BoK SSOT:** `docs/bok/content-provenance/` (FR-CP-006/007/009/010/012/013).
> **Escopo desta SOP:** camada **C3 (IPTC/XMP)** — o marcador machine-readable "gerado por IA" que Meta/LinkedIn/X leem, embutido em imagem/vídeo via ExifTool, USD=0, zero cert/modelo — **e** camada **C1 (C2PA Content Credentials)** — Fatia 2 (§Fatia 2 abaixo), embutida via `c2patool`, cobre imagem/vídeo **e voz** (áudio), **dormente sem cert** (safe-by-default). C2 (watermark) é Fatia 3 (gated).
> **Deadline regulatório:** AI Act Art. 50(2) vigora **2026-08-02** (multa Art. 99 até €15M/3%).

---

## Operator

| Papel | Quem | Ferramenta |
|---|---|---|
| Marcador (runtime) | host worker `provenance-bridge` | `scripts/provenance-bridge.ts` + `exiftool` (host binary, `libimage-exiftool-perl`) |
| Owner | Sovereign | blast radius: falso-sucesso de declarar "marcado" um asset que saiu sem o tag (FM-CP-01) |

## Sequence (o worker, por asset)

1. **Sweep** `creative_assets WHERE provenance_status='pending' AND kind IN ('image','video')` (usa o index parcial da migration `20260716230000`; áudio excluído — IPTC não cobre áudio, OTD-CP-007). Critério: N linhas pendentes.
2. **Download** do objeto do bucket privado (service-role — RLS bypass; objeto owner-scoped). Critério: bytes no temp.
3. **Embed + verify** (`embed-iptc-core`): `exiftool -XMP-iptcExt:DigitalSourceType=<URI>` → **lê de volta** e só segue se o round-trip bate (verify-before-claim, DG-3). URI = `http://cv.iptc.org/newscodes/digitalsourcetype/{trainedAlgorithmicMedia|compositeWithTrainedAlgorithmicMedia}`. Critério: `res.ok === true`.
4. **Re-upload** in-place (`upsert`, mesma key → signed URLs seguem válidas). Critério: sem erro de upload.
5. **Flip** `provenance_status='embedded'`, `provenance_layers={iptc}`, `provenance_source_type`, `provenance_embedded_at=now()`, `file_size_bytes` (service-role). Critério: linha atualizada.
6. **Observação na malha** (`mcorch_nodes` observation + `embed-mcorch-node`, best-effort fail-soft) — FR-CP-012 §4.
7. **Telemetria** `infra_health_logs service='content-provenance'` (`provenance_embedded` | `provenance_failed`).

Falha em qualquer passo → `provenance_status='failed'` (fail-soft) + telemetria degraded; NUNCA declara marcado sem verify.

## Verification gates

| Gate | Prova material |
|---|---|
| **G1** round-trip | worker só marca `embedded` se `exiftool` relê o mesmo URI que escreveu |
| **G2** objeto real carrega o tag | baixar fresco do bucket + `exiftool -s3 -XMP-iptcExt:DigitalSourceType <obj>` = a URI (provado 2026-07-16 no asset `bc03a65a`: roadmap-master PNG 2480×8474 íntegro) |
| **G3** DB terminal | `SELECT provenance_status, provenance_layers` = `embedded, {iptc}` |
| **G4** sem falso-positivo | arquivo virgem → `readIptcMarker` = null (smoke P3) |
| **G5** vídeo | MP4 também aceita o XMP (provado 2026-07-16 no asset `d57e3341`) |
| **G6** hermético re-executável | `bun run scripts/qa/smoke-provenance-iptc.ts` 6/6 (gera PNGs próprios; zero DB/bucket/rede) |

## Recovery path

- **Embed falha** (formato exótico) → status `failed`; re-rodar após corrigir o formato; o sweep re-pega `pending`, não `failed` (evita loop). Para re-tentar um `failed`: `UPDATE creative_assets SET provenance_status='pending' WHERE id=<id>` (service-role).
- **Objeto corrompido pós-embed** → o verify-before-claim bloqueia antes do re-upload; o original no bucket permanece intacto.
- **Backlog** (todos os assets nasceram `pending` com a migration) → `bun run scripts/provenance-bridge.ts --once --limit N` em lotes, OU habilitar o daemon (systemd, gate Sovereign).
- **Re-embed após transformação** (reshape dropa XMP, OTD-CP-008) → a transformação deve resetar `provenance_status='pending'`; o sweep re-marca. (wire-up = fatia futura.)

## Success signal

Um asset de imagem/vídeo REAL, baixado do bucket, carrega `XMP-iptcExt:DigitalSourceType` = a URI IPTC — legível por qualquer verificador (ExifTool, Meta, LinkedIn, X). Provado E2E 2026-07-16 (`bc03a65a` imagem + `d57e3341` vídeo).

## Operational: habilitar o daemon (GATE SOVEREIGN)

O worker roda on-demand (`--once`) hoje. Para marcação contínua (backfill dos ~90 assets legados + todo novo asset):
```bash
systemctl --user enable --now provenance-bridge.service   # unit em ~/.config/systemd/user/ (ação Sovereign)
```
O unit file de referência está versionado em `scripts/systemd/provenance-bridge.service`. **Não habilitado nesta sessão** — habilitar re-uploada todos os objetos legados (mutação de produção), decisão do Owner.

---

## Fatia 2 — C1 (C2PA Content Credentials)

> **Status:** CÓDIGO VIVO, MOTOR DORMENTE (safe-by-default) · Lei 2. **Camada C1** = manifesto C2PA criptograficamente assinado embutido no arquivo (o padrão CAI que Adobe/LinkedIn/TikTok/câmeras leem). Cobre **imagem, vídeo E voz** (áudio — onde o IPTC não chega, OTD-CP-007). Deadline AI Act Art. 50(2): **2026-08-02**.

### Por que C1 além do C3

O C3 (IPTC/XMP) é o marcador que as **plataformas sociais** auto-lêem para rotular; o C1 (C2PA) é a **credencial assinada e à prova de adulteração** — carrega a cadeia de proveniência (parent/ingredient) e sobrevive à verificação criptográfica (Content Credentials / `contentcredentials.org`). São camadas complementares na mesma spine `creative_assets`; `provenance_layers` é a **união real** das que verificaram (ex.: `['c2pa','iptc']` numa imagem, `['c2pa']` numa voz).

### Instalação (aarch64) — FEITO

`c2patool 0.27.0` instalado via cargo em `/home/ubuntu/.cargo/bin/c2patool` (host aarch64; binário nativo, não há edge-fn que o invoque — mesmo motivo do ExifTool). Prova: `c2patool --version` → `c2patool 0.27.0` (c2pa-rs 0.90.0).

### Contrato REAL de assinatura do c2patool 0.27 (descoberto empiricamente)

- Credenciais vão **no próprio manifest JSON** (`-m <file>`): campos `alg:"es256"`, `private_key:"<path>"`, `sign_cert:"<path>"`. (O `-c '<json>'` string também funciona; usamos arquivo temp para não vazar nada em `ps`.)
- **C2PA v2 (default do 0.27) EXIGE `digitalSourceType` na action `c2pa.created`** — sem ele o validador retorna `assertion.action.malformed` ("c2pa.created action must have a digitalSourceType"). O `digitalSourceType` é o **mesmo vocabulário IPTC** que o C3 usa (`iptcSourceTypeUri()` — SSOT único em `src/lib/provenance.ts`).
- c2patool **não assina in-place**: exige `-o <output>` distinto do input. In-place = assinar num temp irmão e `rename` sobre o original.
- **Preservar-e-anexar** (FR-CP-004): re-assinar um arquivo que já tem manifesto **sem** `-p` **DROPA** o manifesto de origem. Com `-p <original>` o manifesto de origem vira **ingredient `parentOf`** (store cresce p/ 2 manifestos), preservando a cadeia. Detectar origem = rodar `c2patool <file>`: exit 0 + JSON = tem manifesto; `Error: No claim found` / exit 1 = virgem.
- **`signingCredential.untrusted`** aparece no `validation_status` quando não há trust list — **esperado em dev** (o `validation_state` global ainda sai `Valid`; a confiança de cadeia é o gate de prod OTD-CP-003). O verify-before-claim ancora na **assertion `digitalSourceType` que releu**, não na confiança da CA.
- Sidecar `.c2pa` (`-s`) só para formatos sem container p/ JUMBF (FLAC/OGG) — **não produzimos** esses → `c2pa_sidecar_key` permanece NULL (coluna = fallback defensivo).

### Estratégia de cert: self-signed dev → trust list prod (GATE)

- **Dev (agora):** cadeia ES256/P-256 de 2 certs (root CA self-signed + leaf com EKU `emailProtection` + KeyUsage `digitalSignature` — requisitos C2PA) gerada **fora do repo** em `/home/ubuntu/.mcorch/provenance/dev-es256.{pem,key}` (`.pem` = leaf+root chain; `.key` = leaf key). **NUNCA commitada.** Os paths são resolvidos por env `C2PA_SIGN_CERT` / `C2PA_PRIVATE_KEY`.
- **Prod (gate OTD-CP-003 + revisão jurídica OTD-CP-012):** o Sovereign provisiona um cert de uma CA na **C2PA trust list** (ou aceita o self-signed como "untrusted-but-valid" para o beachhead, decisão jurídica). Até lá, C1 fica **dormente**.

### Cert-gating dormente (INVARIANTE DE SEGURANÇA)

O daemon `provenance-bridge` **roda em prod** fazendo C3. O motor C1 (`embed-c2pa-core`) é **cert-gated**: se `C2PA_SIGN_CERT`/`C2PA_PRIVATE_KEY` estiverem **ausentes** (ou os arquivos não existirem), ele retorna `{skipped:true, reason:'no_cert'}` **com um log** e o worker segue com C3 — comportamento de prod **INALTERADO**. Nem o `.env` nem o systemd unit carregam as envs de cert; assim, **um restart acidental do daemon NÃO liga C2PA**. C1 só acende quando o Owner provisiona o cert (ação Sovereign explícita).

### Seam no provenance-bridge (cadeia por modalidade)

`markAsset` roteia camadas por `kind`:

| kind | cadeia |
|---|---|
| image | `[C1 c2patool, C3 ExifTool]` |
| video | `[C1 c2patool, C3 ExifTool]` |
| audio (voz) | `[C1 c2patool]` apenas (IPTC não cobre áudio — OTD-CP-007) |

`provenance_layers` = **união REAL das camadas que VERIFICARAM**. Se C1 for `skipped-no_cert`: imagem/vídeo marcam `embedded` com `['iptc']`; **áudio sem nenhuma camada verificada permanece `pending`** (nunca `embedded` falso — Lei 1). O sweep passa a **incluir `audio`**; mantém as exclusões `source_module='external'` e `storage_bucket='local'` (invariantes de honestidade Lei 1).

### Verification gates (Fatia 2)

| Gate | Prova material |
|---|---|
| **C2-G1** round-trip | motor só reporta `ok` se `c2patool` relê a `digitalSourceType` que escreveu no **output assinado** (não no input) |
| **C2-G2** preservar-e-anexar | arquivo já assinado + re-sign → store com 2 manifestos, origem como `ingredient parentOf` (detectada ANTES de tocar bytes) |
| **C2-G3** dormente | sem cert → `{skipped:true,reason:'no_cert'}`, prod inalterada |
| **C2-G4** zero PII | manifesto carrega SÓ o `asset_id` (uuid opaco) — smoke `smoke-provenance-pii-reject.ts` falha se aparecer user_id/email/project_id |
| **C2-G5** voz | WAV assinado in-place, `digitalSourceType` round-trips, sem sidecar |
| **C2-G6** hermético | `bun run scripts/qa/smoke-provenance-c2pa.ts` (gera PNG+WAV próprios + cert dev; zero DB/bucket/rede) |

### Recovery path (Fatia 2)

- **C1 falha mas C3 verifica** (imagem/vídeo) → `provenance_layers=['iptc']`, `embedded` honesto (C1 é aditivo, não bloqueia C3).
- **C1 falha e é a única camada** (áudio) → `provenance_status='failed'` fail-soft; re-tentar via `UPDATE ... SET provenance_status='pending'` após corrigir cert/formato.
- **Verify-before-claim bloqueia** → o temp assinado é descartado, o objeto no bucket permanece intacto (o `rename` só ocorre pós-verify).

### Success signal (Fatia 2)

Um asset REAL (imagem/vídeo/voz) baixado do bucket, quando lido por `c2patool` (ou `contentcredentials.org`), exibe um manifesto C2PA assinado com `c2pa.actions → c2pa.created → digitalSourceType = <URI IPTC>` e `validation_state: Valid`. **Witness E2E em asset real = ação Sovereign pós-gate de cert** (não executado nesta sessão — não marcamos prod com cert ligado).

---

## Known debt / gates

- **Fatia 2 (C2PA)** cobre a **voz** (IPTC não cobre áudio) — **código VIVO**, motor **dormente** até o cert de prod (OTD-CP-003) + revisão jurídica do self-signed (OTD-CP-012).
- **Fatia 3 (watermark)** embute o `creative_assets.id` opaco (nunca PII, OTD-CP-013) — gated em OTD-CP-009 (compute).
- **Upload-teste Meta/LinkedIn/X** que prova o rótulo VISÍVEL (não só embutido) = próximo witness quando as contas estiverem conectadas (o rótulo IPTC→auto-label é MEDIUM confidence, §10 blueprint — validar por upload real).
- **Injection point ideal** (marcar ANTES de `register_creative_asset` finalizar) vs o sweep atual (marca pós-registro): o sweep é o MVP; o inline no render é hardening.

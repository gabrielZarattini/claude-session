# SOP — predictive-swarm Fatia 1: Tier 1 sensory gates (0 mco, determinístico)

**Feature slug:** `predictive-swarm` (Fatia 1 — Tier 1 puro)
**Law 2 (Anticipated Process) gate for:** `loudnessGate` + `contrastGate` + `verdictFor` + o **caminho Tier 1** da tool `vision.parse_sensory_gate`.
**SSOT (Lei 1):** `docs/bok/predictive-swarm/05-sdd.md` (§2.1/2.2/2.3/§4.2/§5/§9) · `04-frd.md` (FR-PSW-002/004/005/011/012) · `07-process-flow.md` (PROC-PSW-003 G1–G9) · `08-quality-metrics.md` (KPI-PSW-001/006/008, FM-PSW-01). Nada aqui inventa fora do BoK; ambiguidade vira TODO citando o FR (nunca improviso).
**ORO triplet:** Operator = MCORCH Master Execution Agent · Reviewer = Sovereign · Owner = Sovereign (absorve o blast-radius: score errado que desperdiça mco ou informa mal a decisão de escala de criativo).
**Escopo (SDD §9 "Fatia 1 ⭐"):** SÓ o Tier 1 puro 0 mco. **NÃO** Tier 2/VLM · **NÃO** `swarm.initialize`/fan-out/job store (Fatia 2) · **NÃO** `mesh.consolidate` (Fatia 3) · **NÃO** migration/DDL (Fatia 1 é in-container). Convenção MCORCH: **código/lógica/vars/logs em inglês; UI/toasts/mensagens de validação em PT-BR**.

---

## 0. Contexto — por que este SOP existe (Lei 2)

O `predictive-swarm` é um módulo MCP molde `vision-mcp` (0 edge fns, 3 blocos `server.tool()` no container `mcorch_vision_mcp`). A Fatia 1 é o **pé-de-apoio material**: um gate objetivo que reprova loudness fora do alvo e contraste ilegível **antes** de publicar, 100% determinístico, FOSS, USD=0, sem depender de ciência não-provada. Se o Tier 1 não nascer FREE e determinístico, o módulo vira "mais uma chamada VLM cara" (blueprint §2, gap #1). Este SOP é o processo humano equivalente que precede o código.

**Operador humano hoje (o que a Fatia 1 automatiza):** um revisor sênior de criativo que, antes de publicar, (a) roda `ffmpeg loudnorm` no áudio e compara IL/LRA/TP com o alvo social (~−14 LUFS), e (b) confere o contraste texto/fundo do projeto contra WCAG 2.1 AA (4.5:1). Se qualquer um reprova, o criativo é NO-GO. A Fatia 1 é exatamente esse revisor, mecanizado e determinístico.

---

## 1. Operator — quem executa

| Papel | Quem | Ferramentas |
|---|---|---|
| Operator | MCORCH Master Execution Agent (código) | `packages/vision-mcp-core/src/tier1/{loudness,contrast}.ts` + o caminho Tier 1 de `parse-sensory-gate.ts`; `ffmpeg` (host, já presente — HyperFrames); `verdictFor` reusado de `report-renderer.ts:58` |
| Reviewer | Sovereign | `/security-review` (não há migration na Fatia 1, mas o smoke roda contra prod VIVO) + GO |
| Owner | Sovereign | absorve o custo de um veredito errado |

---

## 2. Sequence — a ordem exata (cada step com critério material)

> Espelha o caminho Tier 1 do **Use Case A** do SDD (§3) e **PROC-PSW-003** do process-flow. Padrões VIVOS a **espelhar, não reinventar**: `server.tool()` com zodSchema (`server.ts:72`), `verifyBearer`+`requireScope` **antes** do handler (`server.ts:61`, herdado), `logHealth` allowlist default-deny (`telemetry.ts:24`), molde de tool `describe-image.ts:65` (SSRF-guard → … — MAS Tier 1 é **0 mco**, sem `deductOnEntry`/`refund`).

### Step 1 — Registrar a tool `vision.parse_sensory_gate` (scope `swarm:read`)
- Adicionar `swarm:read` ao vocabulário fechado `ALL_SCOPES` em `auth/identity.ts:14` (+ allowlist do PAT). JWT interno → `ALL_SCOPES`; PAT → subset selado.
- Adicionar 1 bloco `server.tool("vision_parse_sensory_gate", <desc PT-BR>, <zodSchema>, handler)` em `createMcpServer` (`server.ts:68`). Handler: `const sub = currentSub(); const denied = requireScope("swarm:read"); if (denied) return denied;` **antes** de qualquer trabalho (idêntico aos blocos existentes).
- Anunciar a tool no array de `/health` (`server.ts:340`).
- **Critério material:** `curl http://127.0.0.1:3200/health` retorna `"vision_parse_sensory_gate"` na lista `tools`. `git diff --stat` mostra `identity.ts` + `server.ts` + os novos `tier1/*.ts` — e **0** arquivos em `supabase/functions/` (NFR-PSW-011).

### Step 2 — `tier1/loudness.ts` → `loudnessGate` (FR-PSW-004)
- Rodar `ffmpeg -i <asset> -af loudnorm=print_format=json -f null -` (1 chamada, host `ffmpeg`, 0 mco). Parsear o bloco JSON final: `input_i` (IL, LUFS), `input_lra` (LRA, LU), `input_tp` (TP, dBTP).
- Comparar com os alvos EBU R128 / social e emitir `Finding[]` (severidade por threshold — tabela §4 abaixo).
- Asset sem trilha de áudio (imagem) → **skip** (nenhum `Finding` de loudness; não é P0).
- **Critério material:** fixture de áudio a −6 LUFS → ≥1 `Finding` com `severity ≤ 'P1'` + `verdict:'NO-GO'` + `SELECT mco_balance` delta = 0 (AT-PSW-004 · PROC-PSW-003 G2).

### Step 3 — `tier1/contrast.ts` → `contrastGate` (FR-PSW-005)
- **Função PURA de 2 cores** `(fg, bg) → Finding | null`: WCAG 2.x **certifica** (razão de contraste, 4.5:1 texto normal / 3:1 texto grande — conformidade legal), APCA Lc **pontua** (perceptual, size/weight-aware — apoio à decisão).
- As 2 cores vêm **SÓ das layer colors do tenant** (`channel_profiles`), **nunca** de extração sobre `asset_url` renderizado (isso é OTD-PSW-013 → Fatia 2).
- **Critério material:** par fg/bg <4.5:1 → `Finding` persistido no output + 0 mco (AT-PSW-005 · PROC-PSW-003 G3).

### Step 4 — Compor o caminho Tier 1 de `parse-sensory-gate.ts`
- Orquestra: SSRF-guard `asset_url` (`assertSafeImageUrl`, `describe-image.ts:41`) → roda `loudnessGate` + `contrastGate` (0 mco) → agrega `Finding[]` + `dimensions` → `verdictFor` → monta a `ParseSensoryGateResponse` com `drift_label:'proxy'` **obrigatório**, `tier_reached:1`, `escalated:false`.
- **Na Fatia 1 NUNCA escalar ao Tier 2** (sem VLM, sem `deductOnEntry`): mesmo com `tier=2` no input, o caminho VLM é Fatia 2 — Fatia 1 responde só com sinais Tier 1 objetivos (fail-closed é o comportamento nativo).
- `logHealth("healthy","tool_ok",{tool:"parse_sensory_gate", tier:1, escalated:false})` — chaves `tier`/`escalated` **entram no allowlist** de `telemetry.ts:24` (default-deny; **sem** `user_id`/UUID/valor per-tenant).
- **Critério material:** output carrega `drift_label:'proxy'` em 100% das saídas (PROC-PSW-003 G6 · NFR-PSW-010).

### Step 5 — `verdictFor` (FR-PSW-012 — reuso, não reescrever)
- Reusar `verdictFor(summary)` de `scripts/qa/e2e-user-zero/lib/report-renderer.ts:58`: **GO sse `p0_count===0 && p1_count===0`**. Construir o `RunSummary` (histograma de severidade) a partir do `Finding[]` do gate e chamar `verdictFor`.
- **Critério material:** `Finding[]` com 1×P1 → `verdict:'NO-GO'`; `Finding[]` só com P2/P3 → `verdict:'GO'` (AT-PSW-012).

### Step 6 — Verificação (§3 abaixo)
- Rodar o smoke Fatia 1. GO Sovereign após verde.

---

## 3. Verification gates (material — Lei 1)

Smoke re-executável (throwaway user, zero-custo): `scripts/qa/smoke-predictive-swarm.ts` (Fatia 1 subset). Herda o padrão de gate de `smoke-deepsearch-run.ts` / `smoke-vision-pat-erase.ts` (LIVE contra `mcp.mcorch.com` ou `127.0.0.1:3200`).

| Gate | Sinal material esperado | Fonte |
|---|---|---|
| G-tier1-zero | `SELECT mco_balance` antes/depois de `tier=1` → **delta = 0** | NFR-PSW-002 · PROC-PSW-003 G1 |
| G-loudness | fixture −6 LUFS → `Finding`≥P1 + `verdict:'NO-GO'` + 0 mco | FR-PSW-004 · AT-PSW-004 · G2 |
| G-contrast | fg/bg <4.5:1 (layer colors do tenant) → `Finding` persistido, 0 mco | FR-PSW-005 · AT-PSW-005 · G3 |
| G-proxy-label | 100% das saídas com `drift_label:'proxy'` | NFR-PSW-010 · FM-PSW-01 · G6 |
| G-verdict | 0×P0 E 0×P1 → `GO`; senão `NO-GO` | FR-PSW-012 · AT-PSW-012 |
| G-scope | Bearer sem `swarm:read` → 403 `scope_insufficient` **antes** de qualquer trabalho, `mco_balance` inalterado | NFR-PSW-005 |
| G-ssrf | `asset_url` loopback/privado → rejeição; requisição interna nunca emitida | NFR-PSW-006 |
| G-zero-edge | `ls supabase/functions` sem função nova; `/health` lista a tool | NFR-PSW-011 · AT-PSW-014 |
| G-determinism | mesmo input → **mesmo** `Finding[]` em 2 runs (byte-idêntico) | NFR (determinístico) |
| G-folclore | `grep` dos 22 itens da blocklist (`08-quality-metrics.md §8`) em BoK+copy+código = 0 | KPI-PSW-008 |

---

## 4. Thresholds materiais (loudness → severidade)

> Alvo social ~−14 LUFS (SDD §2.2 / FR-PSW-004). Os limiares abaixo são a operacionalização determinística; a magnitude do desvio mapeia a severidade P0..P3 do `finding-schema.ts` (`P0` pior → `P3` menor). **Onde o BoK não fixa o número absoluto de cada faixa, é TODO explícito citando FR-PSW-004 — não inventar.**

| Métrica (`ffmpeg loudnorm` JSON) | Alvo | Regra → severidade |
|---|---|---|
| `input_i` (IL, LUFS) | ~−14 LUFS | dentro de ±1 LU → sem finding; fora → `Finding` (severity cresce com \|desvio\|; ≥P1 quando fora do alvo — FR-PSW-004) |
| `input_tp` (TP, dBTP) | ≤ −1 dBTP | > −1 dBTP (clipping/true-peak) → `Finding` (risco de distorção) |
| `input_lra` (LRA, LU) | faixa de range saudável | LRA fora da faixa → `Finding` de flag |

> **TODO (FR-PSW-004):** o BoK fixa o alvo (~−14 LUFS) e o gate de aceite (−6 LUFS → ≥P1), mas **não** tabela os cortes exatos de cada faixa P0/P1/P2/P3. Definir a função `severityForLoudness(deviationLU)` como constante nomeada no código com os cortes citando FR-PSW-004; qualquer corte não derivável do BoK é decisão a levar ao Sovereign, não improviso.

**contrast → severidade (WCAG 2.x):**

| Razão de contraste (fg/bg) | Regra |
|---|---|
| < 3:1 | `Finding` P1 (falha AA dura para texto normal e grande) |
| ≥ 3:1 e < 4.5:1 | `Finding` P2 (passa texto grande, falha texto normal) — APCA Lc pontua o quão perceptualmente ruim |
| ≥ 4.5:1 | sem `Finding` (certifica AA texto normal); APCA Lc segue como score informativo |

---

## 5. Recovery path — falha no step N

| Step | Falha | Recovery exato |
|---|---|---|
| 1 (tool) | tool não aparece em `/health` | `systemctl --user restart` do container Vision MCP; reconferir `curl /health`. Build stale = restart obrigatório (padrão do container) |
| 2 (loudness) | `ffmpeg loudnorm` não emite JSON / asset sem áudio | asset sem trilha → **skip** (não é erro; nenhum finding de loudness). `ffmpeg` ausente no host → `501 {error:'loudness_not_configured'}` fail-closed (nunca cobra — mas Tier 1 é 0 mco de qualquer modo) |
| 3 (contrast) | layer colors do tenant ausentes | responder sem o `Finding` de contraste (não fabricar cores); registrar a lacuna. **NÃO** extrair cor de `asset_url` renderizado (isso é OTD-PSW-013/Fatia 2) |
| 4 (compose) | qualquer exceção interna | `logHealth("degraded","tool_error",{tool:"parse_sensory_gate",code})` + `toolError({error:'internal_error'})` (transport 200, erro in-band — padrão `server.ts:54`) |
| 5 (verdict) | histograma mal montado | reusar `buildSummary`+`verdictFor` (não reescrever a lógica GO/NO-GO) |
| 6 (smoke) | qualquer gate RED | **halt** — não declarar Fatia 1 pronta; cada RED é item de trabalho real (Lei 1) |

**Regra-mãe:** Tier 1 é **0 mco** — não há `deductOnEntry`/`refund` no caminho Fatia 1. Qualquer branch que precise cobrar já é Tier 2 (Fatia 2). Se aparecer débito no delta de `mco_balance` de um run `tier=1`, é bug (bloqueia).

---

## 6. Success signal — sinal materialmente observável do flow completo

Fatia 1 está **pronta** quando, TODOS provados no MESMO turno (Lei 1):

1. `curl /health` lista `vision_parse_sensory_gate` (HTTP 200 body literal).
2. `smoke-predictive-swarm.ts` (subset Fatia 1) sai **verde** em todos os gates de §3 (output literal do runner).
3. `git log -1 --format=%H` do commit + `git diff --stat` provando **0** arquivos em `supabase/functions/` (NFR-PSW-011).
4. Run de fixture defeituoso (−6 LUFS OU contraste <4.5:1) retorna `verdict:'NO-GO'` com `drift_label:'proxy'` e `mco_balance` delta = 0.
5. GO explícito do Sovereign.

---

## 7. Anti-patterns proibidos (Fatia 1)

- ❌ Escalar ao Tier 2/VLM ou chamar `deductOnEntry` no caminho Fatia 1 (Tier 1 é 0 mco por construção).
- ❌ Extrair cor de `asset_url` renderizado no `contrastGate` (OTD-PSW-013 → Fatia 2; Fatia 1 usa **só** layer colors do tenant).
- ❌ Reescrever `verdictFor` (reuso literal de `report-renderer.ts:58`).
- ❌ Emitir `perception_drift` sem `drift_label:'proxy'` (FM-PSW-01, RPN 270).
- ❌ Criar edge function ou migration/DDL (Fatia 1 é in-container).
- ❌ Mandar `user_id`/UUID/valor per-tenant para `logHealth` (allowlist default-deny; per-tenant vive só em RLS SELECT-own — Fatia 3).
- ❌ Ancorar qualquer número/capacidade nos 22 itens de folclore da blocklist (`08-quality-metrics.md §8`).
- ❌ Inventar cortes de severidade não derivados do BoK — vira TODO citando FR-PSW-004, levado ao Sovereign.

---

_Law 2 SOP para a Fatia 1 do `predictive-swarm`. SSOT: `docs/bok/predictive-swarm/{04-frd,05-sdd,07-process-flow,08-quality-metrics}.md`. Nenhum passo, custo, threshold ou superfície inventado fora do BoK selado (Lei 1). Código só começa após este SOP + BoK 9/9 selada + GO Sovereign._

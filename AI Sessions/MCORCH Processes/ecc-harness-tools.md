# SOP — Ferramentas de Harness ECC-alinhadas (SSP-01)

> **Lei 2 (Processo Antecipado).** Utilitários de harness adaptados **sob medida** (não clonados) do
> ecossistema [`affaan-m/ECC`](https://github.com/affaan-m/ECC) para a arquitetura soberana do MCORCH.
> Conceito portado, código próprio. Cada ferramenta ancora numa Survival Law.
>
> **Origem:** diretiva Sovereign 2026-07-04 — o Passo 4 do `/handson` (Antigravity) marcou o alinhamento
> ECC "para verificar posteriormente"; após o rebrand MIV, chegou o momento de materializá-lo.

---

## Inventário

| Ferramenta | Caminho | Lei | Auto-muta? |
|-----------|---------|-----|-----------|
| **mcorch-doctor** | `.claude/scripts/mcorch-doctor.sh` | Lei 1 (Materialidade) | ❌ diagnostica + prescreve |
| **supply-chain sentinel** | `.claude/scripts/scan-supply-chain-iocs.ts` | Lei 1 · Cyber-Sentinel | ❌ só reporta |
| **session-inspect** | `.claude/scripts/session-inspect.ts` | Lei 3 (Poda) | ❌ só mede |

**Princípio comum:** nenhuma ferramenta muta o sistema. Reparar é decisão do operador (Lei 1/Lei 4) —
o `doctor` imprime o comando exato de remediação; não o executa. (Divergência consciente do
`repair.js` do ECC, que restaura arquivos — no MCORCH o self-heal é do daemon/watchdog, não de um script de sessão.)

---

## 1 · mcorch-doctor — diagnóstico consolidado do ecossistema

- **Operator:** MCORCH Master Execution Agent (ou o Sovereign) no pickup de sessão ou antes de um deploy.
- **Sequence:**
  1. `bash .claude/scripts/mcorch-doctor.sh` (rápido) ou `--deep` (inclui `tsc --noEmit` + sentinel `--home`).
  2. Checa em ordem: Git (branch/limpo/vs-origin) · Docker Sovereign Mesh (chroma/claude_mem/vision_mcp/mega-brain-*) · Chroma heartbeat :8001 · chaves de infra no `.env` (presença, **nunca valor**) · `dist/` (existe + env baked no bundle) · integridade do harness (CLAUDE.md/survival.md/HANDOFF.md/agentic-vision.md) · suítes BoK completas · supply-chain sentinel.
- **Verification gate:** cada linha é `✓ PASS` / `▲ WARN` / `✗ FAIL`. Exit code = **nº de FAILs** (0 = saudável).
- **Recovery path:** cada FAIL imprime `↳ remediar: <comando exato>` (ex: `docker restart mcorch_chroma`, `git checkout -- <arquivo>`). O operador executa; nunca o script.
- **Success signal:** `🩺 Ecossistema saudável — 0 fail` + exit 0.

## 2 · supply-chain sentinel — IoC scanner (família Shai-Hulud)

- **Operator:** agente/Sovereign antes de instalar/atualizar dependências, no CI de segurança, e no `doctor`.
- **Sequence:**
  1. `bun run .claude/scripts/scan-supply-chain-iocs.ts` (repo) — lockfiles/manifests, node_modules, source rastreado.
  2. `--home` inclui persistência no host (systemd user units, `~/.local/bin` droppers, LaunchAgents, `/tmp`, configs do Claude/editor envenenados).
- **Detecção (4 superfícies):** (a) pacote comprometido@versão-maliciosa em qualquer lockfile → CRITICAL; nome-comprometido em outra versão → WARN; (b) filename de payload de worm dentro de `node_modules/` → CRITICAL; (c) marcador textual de worm + domínio hostil de exfiltração no source → CRITICAL/HIGH; metadata-IP/exfil-sink → WARN (com supressão heurística de contexto defensivo/SSRF); (d) artefato de persistência no host → CRITICAL.
- **Verification gate:** exit **0** = limpo (sem critical/high) · **1** = comprometido · **2** = args ruins. `--json` p/ pipeline.
- **Recovery path:** CRITICAL → remover o pacote/arquivo, **rotacionar todos os segredos** (npm/GitHub/cloud tokens), auditar `git log` e histórico de instalação, isolar a máquina se houver dropper de runtime.
- **Success signal:** `✅ Nenhum IoC de supply-chain detectado` + exit 0.
- **Manutenção (honestidade Lei 1):** as blocklists de pacotes são um **seed curado e documentado**, não uma lista "completa". Ao surgir uma nova onda (CISA / GitHub Advisory), estenda `BAD_PACKAGES`/`WORM_MARKERS`/`HOSTILE_*` e registre o diff aqui. As checagens estruturais (persistência/payload/marcador/domínio) são o núcleo robusto e independem da completude da lista. Supressão de referência legítima: comentário `// ioc-scan:allow` na linha.

## 3 · session-inspect — medidor de orçamento de contexto (Lei 3)

- **Operator:** agente ao longo da sessão, especialmente perto do gate de seal.
- **Sequence:** `bun run .claude/scripts/session-inspect.ts [--session <id>] [--top <N>] [--json]`. Sem args → sessão ativa (jsonl top-level mais recente do projeto).
- **Cálculo:** lê o transcript e soma `input + cache_read + cache_creation` do **último** turno assistant = tamanho **exato** da janela (dado da API, não estimativa). Budget = 1M. Reserva ~5% (~50k) p/ o `/handoff`.
- **Verification gate / veredito:**
  - `< 45%` → cedo p/ selar; probe-first (puxe o próximo pendente).
  - `45–90%` → janela saudável, continue.
  - `90–95%` → prepare o seal.
  - `≥ 95%` → **SELAR AGORA** (exit 10, script-friendly).
- **Recovery path (poda):** usa "Maiores tool-results em contexto" para escolher o que podar (referenciar por path/hash, não recarregar) — [[feedback_context_budget_calibration]].
- **Success signal:** o veredito e o % batem com o que o Sovereign vê na UI; a decisão de selar deixa de ser um chute.

---

## Integração no `/handson`

O `mcorch-doctor` engloba git/Docker/Chroma/BoK/sentinel → substitui/consolida os comandos avulsos do Passo 1.
O `session-inspect` calibra o orçamento de contexto ao longo da sessão. Ambos referenciados no
Passo 4 de `.agents/workflows/handson.md`.

# SOP — Vision MCP: emissão de PAT + instalação do conector (Claude Code / hosts MCP)

> **Lei 2 (Processo Antecipado).** Operador / Sequência / Gates de verificação / Recovery / Success do fluxo
> de conectar um host MCP externo ao Vision MCP soberano (`mcp.mcorch.com`). Cobre FR-VM-003 (PAT) + FR-VM-011
> (Plugin Zip). Complementa `vision-mcp-pat-and-erasure.md` (emissão/verify do PAT no servidor).

## Operator — quem executa

- **Hoje (Usuário Zero / Sovereign):** o próprio dono da conta, via UI `/dashboard/settings → Connectors`,
  OU via script de ops `scripts/qa/mint-vision-pat.ts` (service-role) quando precisa do plaintext fora do
  browser (ex.: wirar o `.mcp.json` do Claude Code).
- **Tenant externo (futuro):** o usuário gera o PAT na UI e cola no seu host MCP.

## Sequence — ordem com critério material de sucesso

1. **Emitir o PAT.**
   - **UI:** Settings → Connectors → "Gerar token" (nome + escopos + validade ≤365d) → o plaintext aparece
     **uma única vez** (copie na hora). Critério: a linha aparece na lista com badge "Ativo".
   - **Ops (Sovereign):** `set -a; source .env; set +a; bun run scripts/qa/mint-vision-pat.ts <email> --days 365`
     → imprime `mcorch_pat_…` na última linha do stdout (detalhes em stderr). Critério: `✓ PAT minted` +
     `id=<uuid>` em stderr.
   - **Escopos** (allowlist fechada, sem credencial/billing — FM-VM-06): `mesh:read`, `vision:read`,
     `deepsearch:run`, `mesh:write`. PAT só consome tools.

2. **Disponibilizar o segredo no ambiente do host** — NUNCA num arquivo versionado.
   - Claude Code expande `${VISION_MCP_PAT}` do ambiente do processo (não lê `.env` automático).
   - `export VISION_MCP_PAT=mcorch_pat_…` no shell (ou `~/.bashrc`/`~/.zshrc` para persistir). No repo, o
     script de ops já grava em `.env` (gitignored) para reuso por scripts.

3. **Instalar o conector.**
   - **Manual:** o `.mcp.json` do projeto já tem o bloco `vision-mcp` (`type:http` · `url:
     https://mcp.mcorch.com/mcp` · `Authorization: Bearer ${VISION_MCP_PAT}`). Recarregue o Claude Code.
   - **Plugin Zip:** Settings → Connectors → "Baixar Plugin Zip" → descompacte como plugin do Claude Code
     (`.claude-plugin/plugin.json` + `.mcp.json` + skills `/vision-essence` `/reference-brief`
     `/competitive-vision`). Rebuild do zip: `bash scripts/build-vision-mcp-plugin.sh`.

## Verification gates — como confirmar (output esperado)

- **G1 — PAT autentica pela URL pública:**
  `VISION_MCP_PAT=… VISION_MCP_URL=https://mcp.mcorch.com/mcp bun run scripts/qa/handshake-vision-pat.ts`
  → `✅ initialize` + `✅ tools/list — 7 tools` + `✅ tools/call mesh_search — isError=false` com
  `scope: user:<sub>+system`. (Prova o caminho PAT pelo Cloudflare — o mesmo do Claude Code.)
- **G2 — no host:** após reload, `/mcp` no Claude Code lista `vision-mcp` com 7 tools.
- **G3 — escopo respeitado:** um PAT sem `mesh:read` chamando `mesh_search` → `403 scope_insufficient`.
- **⚠️ Gotcha (não é erro de deploy):** `curl` direto da URL pública pode voltar **403 `text/html`** — é o
  **bot challenge do Cloudflare** (browser/SDK MCP passam; `curl` cru não). Confirme o artefato pela origem
  (`--resolve login.mcorch.com:443:127.0.0.1`) ou pelo handshake MCP (G1), nunca por um `curl` cru.

## Recovery — falha no step N

- **Plaintext perdido (não copiou):** não há como recuperar (só o hash persiste). Revogue o token órfão na
  UI (ou deixe expirar) e **gere um novo**.
- **Host não conecta:** confirme `echo ${VISION_MCP_PAT:0:11}` = `mcorch_pat_` no ambiente do host; rode G1
  para isolar (PAT vs. config do host). Se G1 passa e G2 não → problema é env/reload do host, não do servidor.
- **Suspeita de vazamento do PAT:** revogue imediatamente (Settings → Connectors → lixeira → confirma; ou
  `UPDATE mcp_access_tokens SET revoked_at=now()`); o servidor filtra `revoked_at IS NULL` → 401 imediato.
  Gere um novo e re-wire o host.
- **Cap diário atingido** (`daily_cap_reached`): aguarde o reset UTC ou configure BYOK `google_api_key` em
  Settings (BYOK bypassa o cap da chave-plataforma).

## Success signal — materialmente observável

Handshake MCP real pela URL pública (G1) retorna `tools/list` com 7 tools **e** um `mesh_search`
`isError=false` tenant-scoped autenticado **pelo PAT** — provando que qualquer host MCP externo conecta com
a credencial do usuário, sem expor segredo em arquivo versionado.

## Key Files

| Item | Path |
|------|------|
| Hook de PAT (gen/list/revoke) | `src/hooks/useMcpTokens.ts` |
| Hook de estado do conector | `src/hooks/useVisionMcp.ts` |
| Card Settings → Connectors | `src/components/settings/McpConnectorsCard.tsx` |
| Plugin Zip (fonte) | `packages/vision-mcp-plugin/` |
| Build do Plugin Zip | `scripts/build-vision-mcp-plugin.sh` |
| Mint de PAT (ops) | `scripts/qa/mint-vision-pat.ts` |
| Handshake de prova (G1) | `scripts/qa/handshake-vision-pat.ts` |
| Verify do PAT no servidor | `packages/vision-mcp-core/src/auth/pat.ts` · SOP `vision-mcp-pat-and-erasure.md` |

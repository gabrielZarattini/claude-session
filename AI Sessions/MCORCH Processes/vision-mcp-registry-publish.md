# SOP — Vision MCP: publicar no MCP Registry oficial (`com.mcorch/vision-mcp`)

> **Lei 2 (Processo Antecipado).** Runbook para publicar o conector remoto no MCP Registry oficial sob o
> namespace DNS-verificado `com.mcorch/*` (FR-VM-011, metade "MCP Registry"). O manifesto já está autorado e
> validado: `packages/vision-mcp-core/server.json`. **O publish em si é GATED**: exige um registro DNS TXT em
> `mcorch.com` (ação Sovereign) — o agente não controla DNS.

## Operator — quem executa

- **Sovereign** (controla o DNS `mcorch.com` + decide expor publicamente no registry). O agente prepara o
  manifesto + os comandos; o Sovereign executa o challenge DNS + o publish.

## Pré-condições materiais

- `packages/vision-mcp-core/server.json` válido (schema `2025-12-11`, `remotes[0].type=streamable-http`,
  `url=https://mcp.mcorch.com/mcp`, header `Authorization` required+secret). Validado: `python3 -m json.tool`
  + required `[$schema,name,description,version,remotes]` presentes.
- `mcp.mcorch.com` LIVE (OTD-VM-013 fechada) — handshake MCP real provado pela URL pública.
- Repo `repository.url` deve estar **público** no GitHub OU ser removido do manifesto antes do publish
  (campo opcional para namespaces DNS). Hoje o remote é privado — decidir antes de publicar.

## Sequence — comandos exatos (fonte: registry oficial modelcontextprotocol)

1. **Instalar o `mcp-publisher`** (Sovereign): `brew install mcp-publisher` (ou binário/source do repo
   `modelcontextprotocol/registry`).
2. **Gerar a keypair Ed25519** do challenge DNS:
   ```bash
   openssl genpkey -algorithm Ed25519 -out key.pem
   openssl pkey -in key.pem -pubout -outform DER | tail -c 32 | base64   # → <BASE64_PUBLIC_KEY>
   ```
3. **🔒 GATE DNS (ação Sovereign no Cloudflare):** criar o TXT em `mcorch.com`:
   ```
   mcorch.com.  IN  TXT  "v=MCPv1; k=ed25519; p=<BASE64_PUBLIC_KEY>"
   ```
   Critério material: `dig +short TXT mcorch.com` mostra o registro `v=MCPv1; k=ed25519; p=…`.
4. **Login DNS:**
   ```bash
   mcp-publisher login dns --domain mcorch.com --private-key "$(cat key.pem)"
   ```
   Critério: login bem-sucedido (token de publicação emitido para o namespace `com.mcorch/*`).
5. **Publicar** (a partir de `packages/vision-mcp-core/`, onde está o `server.json`):
   ```bash
   cd packages/vision-mcp-core && mcp-publisher publish
   ```

## Verification gates

- **G1 — manifesto válido:** `python3 -m json.tool packages/vision-mcp-core/server.json` sem erro + required
  fields presentes (já verde).
- **G2 — DNS TXT propagado:** `dig +short TXT mcorch.com` contém `v=MCPv1; k=ed25519`.
- **G3 — entrada no registry:** após `publish`, a busca do registry retorna `com.mcorch/vision-mcp` com o
  remote `streamable-http` apontando `https://mcp.mcorch.com/mcp`.
- **G4 — instalável de ponta a ponta:** um host MCP que resolve a entrada do registry conecta com um PAT
  (mesmo handshake do `scripts/qa/handshake-vision-pat.ts`).

## Recovery

- **DNS não propaga / login falha:** confirme o TXT exato (sem aspas extras), aguarde a propagação
  (TTL Cloudflare), re-rode `mcp-publisher login dns`. Não publique sem G2 verde.
- **Schema rejeitado no publish:** valide contra `https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json`;
  corrija o `server.json`; re-publish (idempotente por `name`+`version` — bump a `version` se já existir).
- **Repo privado:** se o registry recusar `repository` privado, remova o bloco `repository` do `server.json`
  (opcional p/ DNS namespace) e re-publish, OU torne o repo público primeiro.

## Success signal

`com.mcorch/vision-mcp` aparece no MCP Registry oficial com o remote Streamable HTTP público — descobrível por
hosts MCP de terceiros (Claude Desktop/Code, VS Code), fechando a metade "registry" da FR-VM-011.

## Caveat (Lei 1)

O MCP Registry está em **preview**; o formato/fluxo pode mudar. A sintaxe exata do `mcp-publisher` deve ser
reconferida contra a doc oficial (`github.com/modelcontextprotocol/registry`) no momento do publish. Este
runbook reflete o fluxo documentado em 2026-06 (schema `2025-12-11`).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

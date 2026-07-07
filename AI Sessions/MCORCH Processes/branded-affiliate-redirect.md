# SOP — Branded Affiliate Redirect (`login.mcorch.com/go/<link_id>`)

> **Lei 2 (Processo Antecipado).** Documenta o processo manual ANTES da automação.
> Fecha o top-gap "branded redirect domain" (sprint v6.28.0): links de afiliado publicados
> devem sair com o domínio confiável `login.mcorch.com` em vez da URL crua do Supabase.

## Por quê
O click-ledger (OTD-ML-CLICKS) roteia cliques por `…/functions/v1/process-affiliate-link?link_id=<uuid>`,
que registra o clique (`record_affiliate_click*`) e 302 pro Mercado Livre. Publicar essa URL crua do
Supabase em redes sociais parece spam/sketchy e reduz CTR. O alias branded resolve isso **sem mudar**
o ledger: `login.mcorch.com/go/<uuid>` → 302 nginx → a mesma função → 302 ML. O clique é contado igual.

## Operator
Quem executa hoje: **Engenheiro de Infra (MCORCH Agent / Sovereign)** com `sudo nginx` no host que serve
`login.mcorch.com` (nginx, `/etc/nginx/sites-enabled/www.mcorch.com.conf`, server block `server_name login.mcorch.com`).

## Sequence (cada passo com critério material)
1. **Backup do conf** — `sudo cp www.mcorch.com.conf www.mcorch.com.conf.bak-<YYYYMMDD>`.
   Sucesso: `ls` mostra o `.bak` com size == original.
2. **Inserir a location** no server block de `login.mcorch.com`, ANTES da `location /` (regex tem precedência):
   ```nginx
   # Branded affiliate redirect — UUID-constrained (no open redirect)
   location ~ "^/go/([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})$" {
     return 302 https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/process-affiliate-link?link_id=$1;
   }
   ```
   Cópia versionada no repo: `infra/nginx/affiliate-go.location.conf`.
   Sucesso: `sudo grep -c "location ~ \"^/go/" <conf>` == 1.
3. **Validar config** — `sudo nginx -t`. Critério: `syntax is ok` + `test is successful`.
   **Se falhar → restaurar o `.bak` e PARAR (não recarregar).**
4. **Recarregar** — `sudo nginx -s reload` (graceful; conexões em voo não caem).
5. **Emitir o link branded** no pipeline — `_shared/affiliate.ts` e `scripts/link-forge.ts` montam o alvo via
   `AFFILIATE_REDIRECT_BASE` (env). Setar o segredo: `npx supabase secrets set AFFILIATE_REDIRECT_BASE=https://login.mcorch.com/go`
   e redeployar `orchestrate-content` + `orchestrate-step`. **Fail-safe:** se a env não estiver setada, o código
   cai pro alvo Supabase direto de antes (zero regressão).

## Verification gates (material)
- **G1 (regex/302):** `curl -sI "https://login.mcorch.com/go/<uuid-qualquer>"` → `HTTP/.* 302` + header
  `location: https://bcyvddsykvehvpwstlfa.supabase.co/functions/v1/process-affiliate-link?link_id=<uuid>`.
- **G2 (open-redirect bloqueado):** `curl -sI "https://login.mcorch.com/go/../etc"` ou path não-UUID → **NÃO** 302
  pro destino (cai na SPA `location /`, 200 index.html). A regex só casa UUID exato.
- **G3 (E2E ledger):** `curl -sIL "https://login.mcorch.com/go/<link_id-REAL>"` segue 302→302 e termina em
  `mercadolivre.com.br` (ou `meli.la`); `affiliate_links.clicks` do link incrementa.
- **G4 (emit):** após redeploy, o `content_mesh_asset`/artigo gerado embute `https://login.mcorch.com/go/<id>`
  (não a URL Supabase). Verificável no próximo run de `orchestrate-content`.

## Recovery path
- **nginx -t falha (passo 3):** `sudo cp www.mcorch.com.conf.bak-<data> www.mcorch.com.conf` → `sudo nginx -t` → reload. Site volta ao estado anterior.
- **Reload quebrou o serve do login (G1 da SPA falha):** restaurar `.bak`, reload, confirmar `curl -sI https://login.mcorch.com/` == 200.
- **Branded base ruim em produção:** `npx supabase secrets unset AFFILIATE_REDIRECT_BASE` + redeploy → pipeline volta a emitir a URL Supabase direta (fail-safe), sem tocar nginx.

## Success signal
`curl -sIL https://login.mcorch.com/go/<link_id-real>` termina em domínio Mercado Livre **E** o clique aparece em
`affiliate_links.clicks`/`affiliate_clicks` — provando que o alias branded preserva o ledger fim-a-fim.

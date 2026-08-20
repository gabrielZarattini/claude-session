# SOP — landing-bundler (FR-LF-002 · P0 centerpiece da landing-factory)

> Lei 2 (Anticipated Process) — selado ANTES do código, 2026-07-16.
> SSOT técnico: `docs/bok/landing-factory/05-sdd.md` §2.3/§3.1 · `04-frd.md` FR-LF-002/003.
> Por quê existe: o Open Design v0.10.0 (pinado) exporta HTML com CSS/JS de topo inlinados,
> mas deixa EXTERNO tudo que importa para uma landing self-contained — `<img>`, fontes,
> `url()`, `@import`, ESM. Single-file export NÃO existe upstream (#368). Sem o bundler,
> a landing publicada no WordPress do tenant referencia assets do nosso container → morre.

## Operator (quem executa manualmente hoje)

Sovereign (ou o agente em sessão), no host, via CLI:
`bun run scripts/landing-bundler/cli.ts <input.html> <output.html>`.
No estado-alvo (fatia posterior), o worker `useLandingFactory → design-bridge → landing-bundler`
executa o mesmo core sem humano no loop.

## Sequence (ordem exata + critério de sucesso material por step)

1. **Obter o HTML de entrada** (export do Open Design ou fixture).
   ✓ Sucesso: arquivo existe, `file` reporta HTML/text, tamanho > 0.
2. **Extrair refs externas** — DOM (`img/source/video/audio/iframe/link[stylesheet]/script[src]`)
   + CSS (`url(...)`, `@import`) em `<style>` e atributos `style`.
   ✓ Sucesso: lista de refs impressa; cada ref é URL absoluta https (relativas resolvidas contra `--base`).
3. **Fetch guardado por ref** — `fetchPublicUrl` host-side (anti-SSRF: https-only, porta 443,
   sem IP privado/loopback/link-local, DNS check best-effort, **re-validação de CADA salto 3xx**),
   timeout por asset, teto de tamanho por asset, piso anti-stub, magic-bytes por tipo declarado.
   ✓ Sucesso: bytes ≥ piso e ≤ teto; MIME confirmado por magic-bytes (não pelo header do server).
4. **Inlinar** cada ref em `data:` URI e reescrever o documento.
   ✓ Sucesso: `grep -c 'data:image' output.html ≥ 1` e `grep -c 'https://' <refs originais>` = 0 remanescentes bundláveis.
5. **Injetar `<head>`** (seam `injectHead`): tokens.css MIV + snippet posthog (SÓ `phc_`) + NOTICE
   Apache-2.0/MIT — a INJEÇÃO dos dados do tenant é da fatia do worker; o core expõe o seam.
   ✓ Sucesso: fragmento presente exatamente 1× dentro de `<head>…</head>`.
6. **Render-parity offline** — abrir o output SEM rede (browser com cache/network off) e comparar
   visualmente com o original (Vision QA nos dois prints).
   ✓ Sucesso: Vision aprova paridade; zero requests de rede no load (HAR/network log vazio).

## Verification gates

- **G1 (anti-SSRF):** ref `https://host-público` que responde `302 → http://169.254.169.254/…`
  é BLOQUEADA (erro `media_url_private_address`), e a requisição interna NUNCA é emitida (teste unit com fetch mock).
- **G2 (teto):** asset acima de `MAX_ASSET_BYTES` → ref mantida intacta + warning (fail-open por ref,
  documento nunca corrompe) — contabilizado no relatório final.
- **G3 (magic-bytes):** server que responde HTML de challenge (CF) para uma URL `.png` NÃO vira
  `data:image/png` — magic-bytes rejeitam, ref mantida + warning.
- **G4 (idempotência):** rodar o bundler sobre o próprio output → zero mudanças (refs já são `data:`).
- **G5 (prova material):** ≥1 imagem real inlinada num run real (`grep 'data:image/'` no output + byte-size do output > input).

## Recovery path

- Falha de fetch de UMA ref (timeout/DNS/teto/magic-bytes): **fail-open por ref** — mantém a URL
  original, registra warning `{ref, reason}` no relatório; o documento sai válido. O operador decide
  re-rodar (transiente) ou corrigir a ref na origem.
- Falha estrutural (HTML não-parseável, output vazio): **fail-closed** — exit ≠ 0, NENHUM output
  parcial escrito (write é atômico via tmp+rename). Re-rodar após corrigir o input.
- No worker (fatia posterior): falha estrutural → `refundMco` (FR-LF-005) + `infra_health_logs`
  `landing_build` status error; SSRF block → evento `landing_bundle_ssrf_block`.

## Success signal (flow completo)

`output.html` self-contained: (a) `grep -c 'data:'` ≥ nº de refs bundláveis; (b) zero refs externas
bundláveis remanescentes; (c) render offline idêntico (Vision QA); (d) relatório JSON
`{inlined:N, kept:[{ref,reason}], bytes_in, bytes_out}` impresso — números reais, não estimados.

## Anti-patterns proibidos

- ❌ `fetch` cru em URL vinda do documento (SSRF por redirect — usar SEMPRE o guard com re-validação por salto).
- ❌ Confiar no `Content-Type` do server para o `data:` URI (magic-bytes mandam).
- ❌ Corromper o documento por falha de UMA ref (fail-open por ref, fail-closed estrutural).
- ❌ Puxar `guizang-ppt` do upstream (AGPL) — NOTICE cobre só o vendorizado MIT (OTD-LF-010).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

# SOP — Amazon affiliate credential resolution (per-user, fail-closed, own-tag-only)

**Feature slug:** `product-opportunity-engine` (Fatia 1) · **Lei 2 gate:** SDD §0 G-0.5 · **SSOT:** `docs/bok/product-opportunity-engine/05-sdd.md`
**Anchors:** API Tenancy Model (CLAUDE.md) · mirror of `affiliate-credential-resolution.md` (ML) · anti-cloaking OTD-POE-002 · FM-POE-03/04/08.

> **Why this exists (Lei 2):** before any code resolves an Amazon affiliate tag, the manual human process must be documented. If a human can't do it without error, the machine can't either. Amazon differs from ML in three ToS-load-bearing ways: (a) the link is a pure `?tag=` string-append (no API, no login, no server fetch to amazon.*), (b) it attributes **SALE** (24h cookie + 90d cart), (c) routing the click through our `/go` redirect is a **ToS violation** (cloaking) → Amazon links are returned RAW, never cloaked.

## Operator — who does this manually today?

The **tenant** (User 0 first) is an approved Amazon Associate. They:
1. Get their **Tracking ID** (store/associate tag, e.g. `mystore-20`) from the Amazon Associates portal (`affiliate-program.amazon.*/home` → account → Tracking IDs). This is **not a secret** (it appears in every affiliate link) but is **per-user** (attributes the sale to that tenant).
2. Take a genuine Amazon **product URL** (no UTM/tag), and append `?tag=<Tracking ID>` (or `&tag=` if the URL has a query). That is the official **Special Link** format — it attributes the sale to them.

## Sequence (each step has a material success criterion)

| # | Step | Success criterion (material) |
|---|------|------------------------------|
| 1 | Tenant saves their Amazon Tracking ID in **Settings → Amazon** (BYOK) | Row `affiliate_config.amazon_tag` populated for `user_id = auth.uid()` (masked in UI after save) |
| 2 | Tenant pastes a product URL into **Paste-Link** card | `resolve-affiliate-link` receives `{ product_url }` with the tenant JWT |
| 3 | `detectNetwork(url)` classifies by host allowlist (`affiliate_network_contract.host_allowlist`) | Returns `'amazon'` for `amazon.com.br`/`amazon.com`/`amzn.to`; `'mercadolivre'` for ML; `null` otherwise |
| 4 | `resolve-affiliate-link` resolves the tenant's tag: `SELECT amazon_tag FROM affiliate_config WHERE user_id = auth.uid()` | Tag present → continue; **absent → HTTP 402** `{ error:"amazon_not_configured", action:"/dashboard/settings" }` (own-tag-only, fail-closed) |
| 5 | `buildAmazonProductUrl(product_url, tag)`: validate host is `amazon.*`, **strip any pre-existing `tag`**, append `?tag=<tenant tag>` | Returns the raw affiliate URL; `cloaked:false`; **no `/go` wrapping** (anti-cloaking invariant) |
| 6 | Response `{ status:'ok', network:'amazon', affiliate_url, attribution:'sale', cloaked:false }` | Tenant copies THEIR own attributable link |

## Verification gates

- **Own-tag-only:** the tag comes ONLY from `affiliate_config` scoped by `auth.uid()`. **Zero** `Deno.env.get('AMAZON_*')` in the user-facing path (grep must be 0). Missing tag ⇒ 402, never a shared/global tag (fraud-by-design, FM-POE-04/08).
- **Anti-cloaking (Critical, FM-POE-03):** the Amazon path never produces a `/go` / `process-affiliate-link` URL. `grep -c '/go\|process-affiliate-link'` in the Amazon branch = **0**. `cloaked` is a return invariant `false`.
- **No server-side scrape (FM-POE-02):** `resolve-affiliate-link` performs **no fetch against `amazon.*`** — it is pure string manipulation.
- **Host validation:** `buildAmazonProductUrl` rejects a URL whose host is not in the Amazon allowlist (prevents appending a tag to a non-Amazon host).

## Recovery path (failure at step N)

- Step 1 missing (no tag): UI routes to Settings → Amazon; edge returns 402 with the exact `action` URL. **No fallback to a global tag.**
- Step 3 unknown host: return `{ error:"unsupported_network" }` (not an Amazon/ML host) — no tag appended.
- Step 5 malformed URL: return `{ error:"invalid_product_url" }`; never emit a partial/cloaked link.
- Ledger unavailable: **fail-open on the ledger** (link generation never blocks on telemetry) but **fail-closed on the credential** (no tag ⇒ 402).

## Success signal (materially observable)

`resolve-affiliate-link` returns **HTTP 200** with `affiliate_url` carrying `?tag=<tenant's own Tracking ID>`, `attribution:'sale'`, `cloaked:false`, and a `SELECT` confirms the tag came from that tenant's `affiliate_config` row — proven by the smoke `scripts/qa/smoke-amazon-tag-append.ts` (own-tag-only 402, `?tag=` present, 0 `/go`, host-validated, tenant-bound).

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

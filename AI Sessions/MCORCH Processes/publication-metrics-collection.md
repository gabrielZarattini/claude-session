# SOP: Coletor de métricas de publicação — nervo sensorial fail-soft (`publication-metrics-collection`)

**Status:** ACTIVE · v1.0 · 2026-06-26
**Owner:** Sovereign (Gabriel Zarattini)
**Survival Law 2 compliance:** Escrito **ANTES** do código do `collect-publication-metrics` + `publication_metrics`. Abre o gate **OTD-VA-014** (`docs/bok/viral-autopilot/05-sdd.md` Amendment v0.3) + cobre FR-VA-027/028. Fecha o lado sensorial de **OTD-AG-002** (doutrina `agentic-vision.md`).
**Canonical directive:** `docs/architecture/agentic-vision.md` §5 (princípios) · `.claude/rules/survival.md > Law 1 (Materiality)` · `CLAUDE.md > API Tenancy Model` (token per-user).
**Sibling SOPs:** `meta-credential-resolution.md` (resolução token Meta) · `autopilot-cron-identity.md` (identidade cron service-role) · `collective-efficiency-ledger.md` (o medidor que consome o reward).

---

## Context

O loop de Learning & Adaptation aprende sobre um **placar em branco** (diagnóstico `wob2d279d`): `creative_metrics` impressions/engagements sempre 0 porque **nada puxa o desfecho social de volta**. O coletor fecha esse nervo: lê insights reais (views/likes/comentários/shares/saves/reach) de cada post publicado e os grava em `publication_metrics` (time-series). Esse dado alimenta o reward multi-métrica → a realocação de esforço → **gasto autônomo de mco**. Dois riscos materiais nascem:

1. **Credencial social cross-tenant (SEC).** O coletor roda service-role (sem JWT de user) e lê token per-user. Confiar num `user_id` do body deixaria o coletor puxar métricas (e mais tarde dirigir gasto) com a credencial errada. **Regra:** o `user_id` vem SEMPRE da **linha confiável do post** (`scheduled_posts.user_id`/`meta_posts.user_id`), nunca do request; token resolvido por `decrypted_social_accounts`/`decrypted_meta_config` filtrado por esse `user_id`.

2. **Fabricação de desfecho (Lei 1).** A tentação fatal é preencher reach/likes com estimativa quando a plataforma não dá (LinkedIn pessoal não expõe; IG sem o escopo de insights). Isso **envenena o reward** com número inventado. **Regra:** o coletor é **fail-soft por plataforma** — grava só o que a API retorna; o que falta vira evento `skipped_no_scope`/`unsupported_platform` em `infra_health_logs` (sem PII), **NUNCA uma linha fabricada**. O reward degrada honestamente sobre os sinais reais.

**Regra-mãe:** o coletor **lê e registra verdade, ou registra ausência** — jamais inventa. Per-tenant por linha confiável; sem PII de terceiros (só agregados numéricos do post próprio).

---

## ORO triplet
- **Operator:** MCORCH Master Execution Agent (autoria) + `pg_cron` (snapshot diário, `Bearer SB_SECRET_KEY`) + on-demand do painel.
- **Reviewer:** Sovereign — aprova a migration (`/security-review`) + valida que IG real retorna número (pós re-OAuth) e que LinkedIn registra `skipped` honesto (não fabrica).
- **Owner:** Sovereign — blast radius = reward envenenado (número falso) → realocação de mco errada; ou token cross-tenant.

---

## Operator (equivalente manual — material)

O ritual que o Sovereign faria à mão para "ver o resultado de cada post":

| # | Passo manual | Sucesso material |
|---|--------------|------------------|
| 1 | Listar posts publicados (LinkedIn/IG) com seu id de plataforma | `external_post_id` por post |
| 2 | Abrir o painel de insights de cada plataforma (IG Professional Dashboard / etc.) | números reais visíveis |
| 3 | Anotar views/likes/comentários/shares/saves/reach de cada post | linha de métrica por post |
| 4 | Repetir dias depois (a métrica cresce) | série temporal |
| 5 | Quando a plataforma não dá o número (LinkedIn pessoal), anotar "indisponível" — **não chutar** | ausência registrada, não inventada |

O coletor automatiza 1–5. **O gate Lei 2 existe porque o passo 5 errado (chutar) envenena a decisão de gasto autônomo.**

---

## Sequence (gates materiais)

1. **Migration `publication_metrics`** (06-data-model §v0.3) — RLS SELECT-own + service-role write + `meta_posts.content_id` + índice reverso. **G1:** DDL com RLS SELECT-own + `security`/`REVOKE` corretos.
2. **`/security-review`** SAFE. **G2.**
3. **Resolução de identidade:** o coletor deriva `user_id` da linha do post (`scheduled_posts`/`meta_posts`), resolve token via `decrypted_*` filtrado por esse `user_id`. **G3:** grep — zero leitura de `user_id` do request body.
4. **Pull fail-soft:** por plataforma suportada (IG, FB), puxa insights por `external_post_id`; grava snapshot. Plataforma sem suporte/escopo → `infra_health_logs` event `skipped_no_scope`/`unsupported_platform` (metadata `{platform, post_ref}` sem PII), zero linha em `publication_metrics`. **G4:** nenhuma linha com número não-retornado pela API.
5. **Cron + on-demand:** `pg_cron` diário (`Bearer SB_SECRET_KEY`) + invoke do painel. **G5:** job ativo.
6. **Prova material:** com IG re-autenticado, um post real → linha `publication_metrics` com likes/reach NÃO-zero batendo o painel nativo do IG; LinkedIn pessoal → `skipped` honesto (sem linha fabricada). **G6.**

---

## Verification gates

| Gate | Critério | Esperado |
|------|----------|----------|
| G1 | RLS SELECT-own na migration | presente |
| G2 | `/security-review` | SAFE |
| G3 | `user_id` da linha confiável, não do body | grep limpo |
| G4 | sem linha fabricada | só dado retornado pela API |
| G5 | `pg_cron` snapshot | job ativo |
| G6 | IG real ≠ 0 (pós re-OAuth) · LinkedIn `skipped` honesto | material |

---

## Recovery path

- **G2 leak:** corrigir RLS/escopo antes de aplicar; nunca aplicar `publication_metrics` sem SELECT-own.
- **Pull falha (token expirado/escopo ausente):** registrar `skipped_no_scope` + telemetria; **não** bloquear o ciclo (fail-soft). Re-OAuth = ação Sovereign.
- **Suspeita de número inventado:** auditar a origem da linha; toda linha de `publication_metrics` deve rastrear a um `external_post_id` real + resposta da API. Linha órfã = bug → drop + corrigir o coletor.
- **Rate limit:** backoff + snapshot diário (não por-minuto); telemetria de degradação.

---

## Success signal (material)

O flow fecha quando: (1) um post IG real (pós re-OAuth) tem linha `publication_metrics` com likes/comentários/reach reais batendo o dashboard nativo; (2) o painel por publicação renderiza esses números em browser real (Vision QA aprovado); (3) LinkedIn pessoal aparece como `skipped`/click-only **sem número fabricado**; (4) o reward `R()` passa a consumir esses sinais (não mais `totalClicks`). Só então o motor **vê** o que publica — o nervo sensorial está vivo.

---

_Generated by MCORCH Master Execution Agent — SOP Lei 2 antes do código (OTD-VA-014 / OTD-AG-002)._

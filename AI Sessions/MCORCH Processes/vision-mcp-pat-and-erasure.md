# SOP — Vision MCP Fatia 3 core: PAT (external auth) + LGPD erasure + retention sweep

> **Lei 2 (Processo Antecipado):** precede o código de `auth/pat.ts`, o scope-gate do `mcp/server.ts`,
> `jobs/retention-sweep.ts` e as 3 migrations. Descreve o processo humano equivalente antes de automatizar.
>
> **BoK SSOT:** `04-frd.md` FR-VM-002/003/009 · `05-sdd.md` §5.2 (RLS) · §5.3 (identity JWT+PAT) · §7 (migration
> stubs 1/4/5) · `06-data-model.md` §2.1/§2.3 + §6 (retention/erasure). **OTD-VM-020:** acesso externo v1 =
> **PAT-first** (OAuth 2.1 browser-flow completo gated no 1º tenant externo que exigir; PRM já publicado).

---

## ORO

| Papel | Quem |
|-------|------|
| **Operator** | MCORCH Vision MCP container; manualmente, um admin que emite/revoga PATs e atende pedidos de erasure LGPD |
| **Reviewer** | Sovereign + `/security-review` independente das 3 migrations (FM-VM-06 PAT-leak = dreno de carteira; LGPD) |
| **Owner** | Sovereign — PAT é credencial que gasta mcoCoins; erasure incompleta = risco LGPD |

---

## Parte A — PAT (Personal Access Token) external auth (FR-VM-003)

### Operator — equivalente manual
Um admin que emite uma chave de API escopada a um cliente externo ("este cliente só pode rodar deepsearch e ler a
malha, por 90 dias"), guarda só o **hash** (nunca o segredo), e revoga quando comprometida.

### Sequence
| # | Passo | Critério material |
|---|-------|-------------------|
| 1 | **Emissão** (dashboard/edge — fora deste slice): gerar plaintext `mcorch_pat_<rand>`, `INSERT mcp_access_tokens(user_id=auth.uid(), token_hash=sha256hex(plaintext), token_prefix, scopes⊆{vision:read,deepsearch:run,mesh:read,mesh:write}, expires_at≤created_at+365d)`. **Mostrar o plaintext ao usuário UMA vez**; o DB só guarda o hash | linha com `token_hash` char(64), scopes na allowlist (CHECK), expiry ≤365d (CHECK) |
| 2 | **Verificação (container, este slice):** request com `Authorization: Bearer mcorch_pat_…` → `verifyBearer` detecta o prefixo → `verifyPat`: `sha256hex(token)` → SELECT service-role `token_hash=eq.<hash> AND revoked_at IS NULL`; rejeita se ausente / `expires_at ≤ now()` → **401 `identity_unverified`** | 401 sem PAT válido; identidade = `{sub=user_id, scopes}` do token |
| 3 | **Scope-gate por tool:** cada tool exige um scope (mesh_search→`mesh:read`, vision_*→`vision:read`, deepsearch_*→`deepsearch:run`, consolidate→`mesh:write`). Scope ausente → **403 `scope_insufficient`** ANTES de custo/leg. JWT interno (sessão Supabase) = todos os scopes (é o próprio tenant) | 403 quando o PAT não tem o scope; 200 quando tem |
| 4 | **`last_used_at`** atualizado fire-and-forget pelo container (auditoria; nunca bloqueia) | coluna avança |
| 5 | **Revogação:** `UPDATE revoked_at=now()` (RLS own; sem DELETE exposto) → próxima verificação 401 | 401 pós-revogação |

### Verification gates (PAT)
- **G-PAT-1** sem token / token inválido → 401. **G-PAT-2** PAT válido → tool roda; identidade = dono do PAT.
- **G-PAT-3** PAT com scope X chamando tool que exige Y → 403 `scope_insufficient`, zero custo.
- **G-PAT-4** PAT revogado/expirado → 401. **G-PAT-5** PAT é **tenant-bound**: só alcança recursos do próprio `user_id` (mesh.search scope filter; vision_jobs/poll user_id).
- **G-PAT-6** scope fora do vocabulário fechado → rejeitado na escrita pelo CHECK `scopes_allowed` (DB, não só app-gate — FM-VM-06).

### Recovery path (PAT)
- Lookup REST falha (rede) → **fail-closed 401** (nunca processa sem identidade verificada).
- Vazamento de PAT: revogação (`revoked_at`) corta imediato; scopes fechados (sem `credentials:*`/`billing:*`) limitam o blast a consumo de tools do próprio tenant; teto de validade 365d limita a janela.

---

## Parte B — LGPD erasure + retention (FR-VM-009)

### Operator — equivalente manual
Um DPO que, a pedido do titular (art. 18 LGPD), apaga TODO o rastro de um artefato de visão — a linha, os nós
de malha derivados + embeddings + edges, e os objetos no Storage — provando **zero resíduo**, e que diariamente
expira artefatos cujo prazo de retenção venceu (art. 16).

### Sequence
| # | Passo | Critério material |
|---|-------|-------------------|
| 1 | **Erasure sob demanda:** `erase_vision_artifacts(content_ref)` (SECURITY DEFINER, `search_path=''`, EXECUTE só authenticated/service_role) — guard `user_id=auth.uid() OR service_role`; cascade DELETE re-escopado por `user_id` em CADA passo (edges → nodes+embedding → storage.objects → a linha) | retorno `{erased:true, nodes, storage_objects}`; `SELECT count` de nodes/edges/objetos = **0** depois |
| 2 | **Tenant-guard defense-in-depth:** SECURITY DEFINER bypassa RLS → re-escopar `user_id=v_artifact.user_id` em cada DELETE impede que um `node_ids[]` poisoned vire primitiva de deleção cross-tenant (NFR-VM-009) | ataque cross-tenant não apaga nada alheio |
| 3 | **Retention sweep (diário, in-container):** `jobs/retention-sweep.ts` busca `vision_artifacts WHERE retention_until < now()` e chama `erase_vision_artifacts(content_ref)` por linha (service-role) | artefatos vencidos somem; telemetria `retention_sweep` em infra_health_logs |
| 4 | **Retention clock:** `retention_until` default 90d, teto 365d (DD-VM-004); tenant pode encurtar, nunca exceder | CHECK/app-side |

### Verification gates (erasure)
- **G-ERA-1** `erase_vision_artifacts(ref)` do dono → cascade completo, `{erased:true}`, **zero resíduo** (count nodes/edges/storage = 0).
- **G-ERA-2** ref de outro tenant → `artifact_not_found` (não apaga nada alheio).
- **G-ERA-3** EXECUTE revogado de PUBLIC/anon (só authenticated/service_role).
- **G-ERA-4** sweep expira `retention_until<now()` e é no-op quando vazio.

### Recovery path (erasure)
- **Limite honesto (FM-VM-11):** cópias já transmitidas a providers US dependem do DPA/SCC (OTD-VM-005) — o
  registro `provider_copies` existe p/ tornar essa deleção **solicitável e auditável**, retornado no payload.
- Sweep falha numa linha → loga `degraded`, continua as demais (uma erasure ruim não trava o lote).

### Success signal
Um PAT válido roda só as tools dos seus scopes (403 nos demais), é tenant-bound, e morre na revogação/expiry;
`erase_vision_artifacts` prova zero-resíduo material; o sweep expira artefatos vencidos diariamente. Smoke
`smoke-vision-pat-erase.ts` fecha verde contra o container servido.

---

## Parte C — nginx vhost `mcp.mcorch.com` (OTD-VM-013)

A vhost SSE-tuned (`nginx/mcp.mcorch.com.conf`) faz `proxy_pass` p/ `127.0.0.1:3200` com `proxy_buffering off`
+ timeouts longos (jobs de minutos) + heartbeat ≤25s sob o idle ~100s do Cloudflare. **Ativação depende de ação
Sovereign** (root tem o agente, mas o DNS é da conta Cloudflare): ver runbook no fim de `nginx/mcp.mcorch.com.conf`.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

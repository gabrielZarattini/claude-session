# SOP: Great Reset — Sovereign Account (Soft Reset)

**Status:** ACTIVE · v1.0 · 2026-05-27
**Owner:** MCORCH Master Execution Agent (Operator) · Sovereign (Reviewer + Owner)
**Survival Law 2 compliance:** SOP written BEFORE code execution.

---

## Context

Sovereign requested a "Great Reset" of his admin account (`ada39fae-67e1-4e53-af1c-5a18e1c108e8`) in order to run a clean ecosystem-wide E2E validation as Usuário Zero. The reset must behave **as if the user had self-deleted via LGPD `delete_account` RPC**, but preserves operational configuration so the user can continue working with the same integrations afterward.

This is **NOT a LGPD deletion**. The auth user, profile row, OAuth credentials, API keys, and Canvas Studio portfolio remain intact. Only generated content, conversational history, ledger, and constellation observations are wiped.

---

## Operator

- **Primary:** MCORCH Master Execution Agent (Claude Code session)
- **Verification gate executor:** Sovereign clicks `/dashboard` post-reset and confirms login + integrations work
- **Recovery executor:** Sovereign (if rollback needed via `.claude/context/backups/great-reset-2026-05-27/*.json`)

---

## Pre-conditions (must ALL be true before executing)

| # | Check | Material proof |
|---|---|---|
| 1 | `npx tsc --noEmit` zero errors | Empty stdout |
| 2 | `bun run test` 189/189 pass | Test runner output |
| 3 | Ledger reconciled: `mco_balance ≡ SUM(mcoin_transactions.amount)` | drift=0 from REST query |
| 4 | All 5 Docker containers healthy | `docker ps` snapshot |
| 5 | BoK suites 9/9 complete | `for slug in docs/bok/*; do … done` loop |
| 6 | Backup snapshots written to `.claude/context/backups/great-reset-2026-05-27/` | `ls -la` shows N JSON files |
| 7 | Sovereign explicit green-light recorded | Conversation transcript reference |

---

## Sequence (numbered, atomic ordering)

### Step 1 — Snapshot backup (READ-ONLY)
Dump JSON of every table whose rows will be deleted:
- `pipeline_runs` (2 rows)
- `content_library` (3 rows)
- `content_mesh_asset` (4 rows)
- `mcorch_nodes` user-owned (115 rows: 111 conversation + 3 observation + 1 content_mesh_asset)
- `aios_conversations` (116 rows)
- `mcoin_transactions` (40 rows)
- `scheduled_posts` (8 rows)
- `mcorch_edges` user-owned (via REST filter)

**Storage:** `.claude/context/backups/great-reset-2026-05-27/<table>.json` (committed to git for irreversibility audit trail).

**Success signal:** Each file contains valid JSON array · `wc -l` returns >0 · `jq length` matches REST count.

### Step 2 — Author RPC `soft_reset_account(p_user_id uuid)`
Clone `delete_account()` (migration `20260508025933_delete_account_rpc.sql`) into new migration `<timestamp>_soft_reset_account_rpc.sql` with:

**Adds (vs delete_account):**
- `DELETE FROM mcoin_transactions WHERE user_id = p_user_id`
- `DELETE FROM content_mesh_asset WHERE user_id = p_user_id`
- `DELETE FROM affiliate_links WHERE user_id = p_user_id` (defensive — already 0)

**Removes (vs delete_account):**
- ❌ `DELETE FROM social_accounts` → **PRESERVE** (OAuth tokens reused)
- ❌ `DELETE FROM user_api_keys` → **PRESERVE** (per-user vault reused)
- ❌ `DELETE FROM profiles` → **PRESERVE** (only UPDATE `mco_balance=p_new_balance, score=0`)

**Signature:** `soft_reset_account(p_user_id uuid, p_new_balance int DEFAULT 10000)` returns `jsonb` with audit summary.

**Security:** SECURITY DEFINER · REVOKE ALL FROM PUBLIC · GRANT EXECUTE TO service_role only (NOT authenticated — this is admin-only since it preserves login).

**Idempotency:** Safe to re-run; subsequent calls will report 0 rows affected for already-empty tables.

### Step 3 — Apply migration
```bash
npx supabase db push
```
**Success signal:** `Applied migration <timestamp>_soft_reset_account_rpc.sql` in stdout.

### Step 4 — Execute reset via RPC
```sql
SELECT public.soft_reset_account('ada39fae-67e1-4e53-af1c-5a18e1c108e8', 10000);
```
Invoke via REST `/rest/v1/rpc/soft_reset_account` with service-role key.

**Expected output (JSONB):**
```json
{
  "reset": true,
  "user_id": "ada39fae-...",
  "new_balance": 10000,
  "tables_affected": {
    "content_library": 3,
    "pipeline_runs": 2,
    "mcorch_nodes": 115,
    "mcorch_edges": "<dynamic>",
    "aios_conversations": 116,
    "scheduled_posts": 8,
    "mcoin_transactions": 40,
    "content_mesh_asset": 4,
    "affiliate_links": 0
  }
}
```

### Step 5 — Migrate API keys per-user (Gemini + Replicate + Higgsfield)
For each global vault key that has a NULL counterpart in `user_api_keys`, populate via UPDATE. **Sovereign must run this MANUALLY via `npx supabase secrets list` paired with a service-role REST PATCH** because we cannot read vault secrets from this session (vault values are write-only via `supabase secrets set`).

**Alternative:** Sovereign passes keys directly in conversation OR retrieves from `.env` (Higgsfield is in `.env` already).

**Success signal:** REST GET `user_api_keys?user_id=eq.<sovereign>` returns all 6 keys SET.

### Step 6 — Verification gates (must ALL pass before declaring success)

| Gate | Check | Pass criterion |
|---|---|---|
| G1 | Sovereign can still log in | `/auth` → success → `/dashboard` |
| G2 | Profile row intact | `profiles?id=eq.<sovereign>` returns row with `mco_balance=10000, score=0` |
| G3 | All target tables empty | Each Sovereign-filtered query returns 0 rows |
| G4 | OAuth integrations intact | `social_accounts?user_id=eq.<sovereign>&is_active=eq.true` returns 3+ rows |
| G5 | Per-user vault preserved + expanded | `user_api_keys?user_id=eq.<sovereign>` returns row with all keys SET |
| G6 | Canvas Studio portfolio intact | `vm_canvas_executions?user_id=eq.<sovereign>` returns 85 rows |
| G7 | Audit trail intact | `mcorch_nodes?user_id=is.null&node_type=in.(handoff,milestone,decision)` count unchanged |
| G8 | Ledger empty | `mcoin_transactions?user_id=eq.<sovereign>` returns [] |
| G9 | TS still clean | `npx tsc --noEmit` zero errors |
| G10 | Tests still pass | `bun run test` 189/189 |

---

## Recovery path (rollback)

**If Step 4 RPC fails mid-transaction:**
- RPC is wrapped in implicit transaction (`LANGUAGE plpgsql` body runs atomic). Postgres rolls back automatically. No action needed.

**If Step 4 succeeds but a downstream gate (G1–G10) fails:**
1. Stop. Do NOT proceed to Phase 2 (E2E).
2. Restore from backups in `.claude/context/backups/great-reset-2026-05-27/`:
   ```bash
   for f in .claude/context/backups/great-reset-2026-05-27/*.json; do
     table=$(basename "$f" .json)
     # Bulk INSERT via REST or Supabase CLI seed
   done
   ```
3. Reset `mco_balance` to backed-up value via PATCH `profiles?id=eq.<sovereign>`.
4. Open incident report in `infra_health_logs` with `service=great-reset-rollback`.

**If verification gate G1 (login) fails:**
- Sovereign manually re-authenticates via OAuth (Google). Profile row preserved means auth works; only `last_seen_at` may reset.

---

## Success signal (whole protocol)

All 10 verification gates pass + Sovereign confirms via `/dashboard` UI that:
1. Login works
2. Balance shows 10000 mcoCoins
3. LinkedIn/Instagram/Facebook integration icons still green
4. Canvas Studio shows existing portfolio
5. `/dashboard/orchestration` canvas is empty (no prior pipeline runs)
6. `/dashboard/constellation` shows clean state (no Sovereign-owned conversation nodes)

Then proceed to Phase 2 (Health Sweep).

---

## Anti-patterns prohibited

- ❌ Skipping Step 1 (backup) "because it's a small dataset" — Lei 1 requires material recovery path.
- ❌ Running DELETEs ad-hoc via separate REST calls instead of atomic RPC — increases blast radius if interrupted mid-flight.
- ❌ Skipping `npx tsc --noEmit` + `bun run test` post-reset (G9 + G10) — schema drift might break code silently.
- ❌ Hardcoding `mco_balance` value in migration — use parameter `p_new_balance` so future resets are configurable.
- ❌ Granting EXECUTE to `authenticated` role — this is admin-only operation; LGPD `delete_account` is the user-facing self-service.

---

## Audit observation (post-execution requirement)

Insert observation node in `mcorch_nodes` with `user_id IS NULL` (system-owned) and metadata:
```json
{
  "kind": "great-reset",
  "target_user_id": "ada39fae-...",
  "executed_at": "<ISO timestamp>",
  "tables_affected": { "...": "..." },
  "operator": "MCORCH Master Execution Agent",
  "reviewer": "Sovereign",
  "owner": "Sovereign",
  "session_seal": "v6.10.0"
}
```

---

## Connection to Survival Laws

- **Lei 1 (Materialidade):** Every step has explicit material proof (JSON dumps, REST counts, JSONB return). No "reset succeeded" claim is allowed without paired evidence.
- **Lei 2 (Anticipated Process):** This SOP is written BEFORE code execution (gate enforced).
- **Lei 3 (Pruning):** Backup files are kept in `.claude/context/backups/`, NOT loaded into active context after dump.
- **Lei 4 (ORO):** Triplet declared in header.

---

%% --- PROJECT METADATA START --- %%
> [!meta] Informações do Projeto
> * **Projeto**: [[MCORCH]]
%% --- PROJECT METADATA END --- %%

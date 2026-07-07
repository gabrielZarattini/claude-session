# SOP — Schema Drift Audit (deployed ↔ migrations)

> **Lei 2 (Processo Antecipado).** The automation (`scripts/qa/audit-schema-drift.sh`) exists because this
> manual process exists first. Born from the 2026-06-03 flywheel post-mortem: a prod hotfix renamed an RPC
> parameter (`async_orchestrate_step`: `p_service_key`→`p_service_jwt_legacy`) **without a migration**, so the
> live definition silently diverged from version control → pg_net no-op → every `pipeline_run` stuck `running`
> for 2 days with no visible error. Drift is invisible until it breaks something — this SOP makes it visible on demand.

## Operator
- **Human:** Sovereign or any engineer with `supabase login` done (token at `~/.supabase/access-token`) or
  `SUPABASE_ACCESS_TOKEN` exported. The audit is **read-only** against prod (Management API `/database/query`
  + Functions API). No DB password needed.
- **Agent:** MCORCH Master Execution Agent runs `bash scripts/qa/audit-schema-drift.sh`.

## When to run
- After ANY prod hotfix (SQL editor / Management API change) — to confirm it was back-filled as a migration.
- At the start of a `/handson` when the last session touched DB objects out-of-band.
- Before a `db reset` / new-environment bootstrap (drift means the fresh env won't match prod).
- Periodically (candidate cron) — drift is silent; don't wait for the next incident.

## Sequence (each step has a material success criterion)
| # | Step | Material success criterion |
|---|------|----------------------------|
| 1 | **Capability gate** | Script resolves `project_id` from `supabase/config.toml` + a token. No token → exits **2** with a "Cérebro sem mãos" message (Lei 1 — not a false pass). |
| 2 | **L0 ledger parity** | `schema_migrations` (prod) set == `migrations/*.sql` set. Mismatch = a hotfix applied without a file, or a file never pushed. |
| 3 | **L1 function existence** | Every live non-extension `public` function is declared in a migration. A live-but-undeclared function = out-of-band creation (the canonical drift). |
| 4 | **L2 RPC caller-contract** | Every `.rpc('name')` in `src/`+`supabase/functions/` resolves to a live function. A miss = PGRST202 risk (the async class). *Arg-KEY drift is spot-checked manually — see Recovery.* |
| 5 | **Edge `verify_jwt`** | Deployed `verify_jwt` (Functions API) == `config.toml` `[functions.*]`. A pg_net-invoked function defaulting to `verify_jwt=true` = 401 on the opaque service key (root-cause #1 of the incident). |
| 6 | **Edge existence** | `supabase/functions/` dirs (minus `_shared`) == deployed slugs. |
| 7 | **Triggers** | Every live non-internal trigger is migration-declared (regex handles `CREATE OR REPLACE TRIGGER`); none `DISABLED`. |
| 8 | **ADVISORY** | SECURITY DEFINER functions all have a locked `search_path`; every public table has RLS enabled. *Advisory: security posture, NOT pure drift — does not flip the exit code.* |

## Verification gates
- **Exit 0** = no deployed↔migration drift. **Exit 1** = drift found (see the `❌` lines). **Exit 2** = could not run
  (no token / no project ref) — treat as UNKNOWN, never as PASS.
- The advisory section (`⚠️`) is informational; resolve via a hardening OTD, not an emergency.

## Recovery path (drift found)
1. **L0 / L1 / triggers (out-of-band object):** capture the live definition into an **idempotent** migration
   (`pg_get_functiondef(oid)` / `pg_get_triggerdef(oid)` verbatim; `CREATE OR REPLACE` for functions,
   `DROP … IF EXISTS` + re-create for event triggers). Run `/security-review`, then `supabase db push`. Re-run the
   audit → must be green. Decide explicitly *capture vs drop* (is the object wanted?). Reference: the F1/F3 migrations
   of 2026-06-03.
2. **L2 arg-KEY drift (param rename, the async bug):** compare the call-site object keys against
   `pg_get_function_arguments(oid)`; realign the function signature to the **callers' contract** (callers invoke by
   name — never rename a param without updating every `.rpc()`/`PERFORM`), `GRANT` to the correct role, migration +
   `/security-review` + push. Reference: `20260603190000_fix_async_orchestrate_step_param_drift.sql`.
3. **Edge `verify_jwt`:** add/fix the `[functions.<name>]` block in `config.toml` and redeploy the function.
   pg_net-invoked functions MUST be `verify_jwt=false`. Reference: `20260603190000` + the orchestrate-step fix.
4. **NEVER** "fix" by editing prod directly again — that re-creates drift. The migration is the only durable fix.

## Success signal
`bash scripts/qa/audit-schema-drift.sh` prints **`✅ NO deployed↔migration DRIFT detected`** and exits **0**.
First green: 2026-06-03 post-remediation (8 checks green; ledger 96==96).

## Root governance rule
**Any prod hotfix MUST be back-filled as a migration in the same session.** The async incident was a hotfix that
skipped this — that omission, not the rename itself, is what let the divergence persist silently. If you can't write
the migration now, you can't make the hotfix now.

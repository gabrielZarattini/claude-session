# SOP — agent-browser CLI Install & Smoke Test

> **Survival Law 2 (Anticipated Process) anchor.** This SOP documents the human-equivalent procedure that the AI must mirror when (re)installing or verifying the [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) CLI on a MCORCH host. It is the prerequisite SOP behind any AI-driven E2E "Usuário Zero" run that uses agent-browser instead of (or alongside) the existing Playwright-based `scripts/qa/audit-canvas-ui.ts`.
>
> Status: Sealed v6.8.4 — 2026-05-25.

---

## Why this exists

The existing E2E gate enforced by Survival Law 1 (`scripts/qa/audit-canvas-ui.ts`) is a Playwright script tightly coupled to the Canvas Studio surface (1920×1080, 22-node assertion, hardcoded selectors). The Vercel Labs `agent-browser` CLI gives the AI a generic, snapshot-and-ref browser primitive that lets it explore *any* surface (landing page, dashboard, orchestrator canvas, settings, billing flow) on demand — closer to how a real Usuário Zero would dogfood the product. The `dogfood` skill bundled with the CLI captures that exploratory testing workflow verbatim.

This SOP keeps the install reproducible so we can rebuild the environment on any other MCORCH host (laptop, VM, sandbox) without rediscovering the steps.

---

## Operator

Default: **Sovereign (Gabriel Zarattini)** running on the host where the AI executes (`ubuntu` user under `/home/ubuntu/.nvm`). Secondary: any L1/L2 agent with shell access for a verification check.

The AI is allowed to run the verification steps unattended (read-only). The AI is **not** allowed to invoke `npm install -g` or `agent-browser install` without an explicit Sovereign green light — those touch the global node_modules and download a Chromium payload.

---

## Sequence

### Step 1 — Pre-flight: detect existing install

```bash
command -v agent-browser && agent-browser --version
ls -la $(command -v agent-browser) 2>/dev/null
```

**Expected success output:**

```
/home/ubuntu/.nvm/versions/node/v22.22.3/bin/agent-browser
agent-browser 0.27.0
lrwxrwxrwx ... -> .../lib/node_modules/agent-browser/bin/agent-browser-linux-arm64
```

If the binary is already present at v0.27.0 (or newer) → **skip to Step 4**.

### Step 2 — Install the CLI (only if missing)

```bash
# Global install via npm — bun is fine too; never pnpm in the repo root.
npm install -g agent-browser
```

**Verification:** repeat Step 1; the symlink and `--version` must now resolve.

### Step 3 — Download bundled Chromium (only if missing)

```bash
agent-browser install
```

This drops Chromium under `~/.cache/agent-browser` or reuses an existing Playwright Chromium at `~/.cache/ms-playwright/`. On the current host (2026-05-25), Playwright Chromium already exists (`chromium-1224` + `chromium_headless_shell-1224`) and `agent-browser` reuses it — so this step is a no-op here.

**Verification:** `ls ~/.cache/ms-playwright/chromium-* 2>/dev/null || ls ~/.cache/agent-browser/ 2>/dev/null` must list at least one Chromium revision.

### Step 4 — Smoke test against the production landing

```bash
mkdir -p /tmp/agent-browser-smoke
agent-browser batch \
  "open https://login.mcorch.com" \
  "wait --load networkidle" \
  "wait 2000" \
  "screenshot /tmp/agent-browser-smoke/login-mcorch.png" \
  "get title" \
  "close"
```

The trailing `wait 2000` is required because the MCORCH landing is a Vite SPA — without an extra 2-second cushion past `networkidle`, the screenshot lands on a black canvas (React not yet hydrated). This is documented in the dogfood skill template too.

### Step 5 — List bundled skills

```bash
agent-browser skills list
```

The CLI ships with 6 first-party skills: `agentcore`, `core`, `dogfood`, `electron`, `slack`, `vercel-sandbox`. For E2E Usuário Zero work, only `core` (always) and `dogfood` (when bug-hunting) are relevant. Load with `agent-browser skills get <name>` and feed the markdown into the AI's working context.

---

## Verification gates

Each gate is *materially observable* — a tool output, not a self-declaration. Skipping any of them violates Survival Law 1.

| Gate | Material check | Pass criterion |
|------|----------------|----------------|
| **G1 — Binary on PATH** | `command -v agent-browser` | Absolute path printed; non-empty exit code 0 |
| **G2 — Version pinned** | `agent-browser --version` | `agent-browser 0.27.0` or higher |
| **G3 — Native arch** | `ls -la $(command -v agent-browser)` | Symlink resolves to `agent-browser-linux-arm64` on this host (or `-linux-x64` on x86 hosts) |
| **G4 — Chromium available** | `ls ~/.cache/ms-playwright/chromium-*` (reuse) **OR** `ls ~/.cache/agent-browser/` (native) | At least one revision directory |
| **G5 — Smoke screenshot valid** | `file /tmp/agent-browser-smoke/login-mcorch.png` | `PNG image data`, ≥ 50 KB (a black-canvas regression sits around 3.7 KB) |
| **G6 — Page title correct** | `get title` output in Step 4 | Exactly `MCORCH · Sovereign Intelligence · Pare de ser variável.` |
| **G7 — Bundled skills enumerated** | `agent-browser skills list` | Lists at least `core` and `dogfood` |

Material proofs from the 2026-05-25 seal:

- G1+G2: `/home/ubuntu/.nvm/versions/node/v22.22.3/bin/agent-browser`, `agent-browser 0.27.0`.
- G3: symlink → `agent-browser-linux-arm64` (Oracle ARM64 host).
- G4: `~/.cache/ms-playwright/chromium-1224` present (Playwright reuse confirmed).
- G5: `/tmp/agent-browser-smoke/login-mcorch-v2.png` — 116 KB · `PNG image data, 1280 x 633, 8-bit/color RGB`.
- G6: title returned literally `MCORCH · Sovereign Intelligence · Pare de ser variável.`.
- G7: 6 skills listed (`agentcore`, `core`, `dogfood`, `electron`, `slack`, `vercel-sandbox`).

---

## Recovery path

| Failure mode | Symptom | Recovery |
|--------------|---------|----------|
| **F1 — `agent-browser: command not found`** | Step 1 fails empty | Re-run Step 2. If Node ≠ v22.x, `nvm use 22 && npm install -g agent-browser` (v22.22.3 is the project canonical). |
| **F2 — `agent-browser-linux-arm64: not found`** | Symlink dead despite `npm install -g` succeeding | Wrong architecture detection at install time. `npm uninstall -g agent-browser && npm cache clean --force && npm install -g agent-browser`. |
| **F3 — Chromium missing on first `open`** | `Failed to launch browser` error mentioning `chrome`/`chromium` not found | Run `agent-browser install`. If still failing, force download: `PLAYWRIGHT_BROWSERS_PATH=$HOME/.cache/ms-playwright npx playwright install chromium`. |
| **F4 — Black-canvas screenshot (≤ 5 KB)** | Step 4 PNG is uniformly black | Increase the trailing `wait` from 2000 ms to 5000 ms; the SPA hadn't hydrated. Re-run Step 4. |
| **F5 — `Browser launch timeout`** | First `open` hangs > 30 s | Kill any orphan Chrome: `pkill -f "chrome.*--remote-debugging-port"`. Then `agent-browser close --all`. Retry Step 4. |
| **F6 — Stale session collides with new run** | Same `--session` name returns wrong tab | `agent-browser close --all` to nuke every session. Restart Step 4. |
| **F7 — `npm install -g` denied (EACCES)** | Permission error on the global prefix | Configure user-local prefix once: `mkdir -p ~/.npm-global && npm config set prefix ~/.npm-global && export PATH=~/.npm-global/bin:$PATH`. Re-run Step 2. **Never** sudo into the system npm prefix on this host. |

Destructive operations (`pkill`, `npm uninstall -g`, `npm cache clean`) require explicit Sovereign approval if executed by the AI — they are reversible but cross the "shared system state" line of the project's executing-actions-with-care rule.

---

## Success signal

A green Step 4 batch run **plus** an inspectable 116 KB-class PNG that visibly renders the MCORCH landing copy ("O futuro opera sozinho. Para que você volte a viver.") confirms the install is operational. This is the single observable that downstream Usuário Zero E2E flows (dogfood skill, custom audits) must produce on cold-start before claiming readiness.

---

## Integration notes — how this fits the project

- **Coexists with Playwright.** `scripts/qa/audit-canvas-ui.ts` stays the gate for Canvas Studio (Survival Law 1's E2E gate clause). `agent-browser` is the *general-purpose* exploratory tool — use it for landing/auth/dashboard/orchestrator/settings flows where Playwright would be over-engineered.
- **Skill `dogfood`** is the recommended workflow for full Usuário Zero passes: it produces a structured report under `dogfood-output/` with per-finding screenshots + repro steps, ready to file as Knowledge Mesh `observation` nodes.
- **AI Gateway is optional.** `agent-browser` *can* talk to an `AI_GATEWAY_API_KEY` for natural-language find/chat commands, but the snapshot-and-ref workflow does not require it. Do **not** wire the AI Gateway key in this repo until BoK suite + per-user resolution model is sealed (API Tenancy Model directive 2026-05-19 — see `CLAUDE.md > Architecture > "API Tenancy Model — Per-User Credentials"`).
- **Auth flow when needed.** For dashboard-side E2E, store auth state with `agent-browser --session <name> state save <path>.json` after a manual login pass, then reuse via `--state` on subsequent runs. Never commit auth state JSON to the repo — keep under `/tmp/` or `~/.claude/` (gitignored).
- **Knowledge Mesh tie-in.** Every dogfood run that surfaces an actionable issue must insert one `observation` node into `mcorch_nodes` (mesh mandate, CLAUDE.md §3 Mesh Connection Mandate). Repro evidence path goes in `metadata.evidence_path`.

---

## Quick reference — minimal cold-start commands

```bash
# Idempotent verify (safe to run anytime)
command -v agent-browser && agent-browser --version && agent-browser skills list

# Smoke (re-prove the install works against prod landing)
mkdir -p /tmp/agent-browser-smoke
agent-browser batch \
  "open https://login.mcorch.com" \
  "wait --load networkidle" \
  "wait 2000" \
  "screenshot /tmp/agent-browser-smoke/login-mcorch.png" \
  "get title" \
  "close"

# Begin a dogfood pass (loads the structured exploration playbook)
agent-browser skills get dogfood --full
```

---

**SOP authored 2026-05-25 by MCORCH Master Execution Agent under Sovereign directive.**
Material proofs of the first install verification are pinned in the v6.8.4 `/handoff` seal (when sealed).

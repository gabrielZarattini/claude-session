# Fix COMMIT_RE false positive on decimal strings
**Date:** 2026-05-25 | **Session ID:** `f2f0188f-cc9c-41b1-b7c1-15c864cc8c49`

---

## 👤 User *(21:24:31)*

Fix a false-positive in the mcorch-qa-healing skill's COMMIT_RE pattern in scripts/qa/extract-manifest.ts:18.

Current pattern: `/`([0-9a-f]{7}|[0-9a-f]{9,40})`/gi`

Problem: matches pure-decimal strings inside backticks (e.g. `20260525173500` — 14-digit migration timestamp prefix). This was hit during the v6.8.2 handoff seal — see commit `17ff2ca` for the context and the workaround commit immediately after it (the workaround edited HANDOFF.md to use the full filename instead).

Fix: require at least one a-f hex letter (in addition to digits) so pure-decimal strings fall through. Suggested patch — keep the same /gi pattern but skip matches that are all digits in the matchAll loop in scripts/qa/extract-manifest.ts:94, e.g.:

```ts
for (const m of block.matchAll(COMMIT_RE)) {
  const hash = m[1];
  if (/^\d+$/.test(hash)) continue;  // skip pure-decimal (e.g. migration timestamps)
  // ... existing handling
}
```

Validation: add a Vitest case in `src/test/qa-extract-manifest.test.ts` asserting that ``` `20260525173500` ``` inside a markdown block does NOT register as a commit, while ``` `bfe2f43` ``` still does. Re-run `bun run test` to confirm 176 → 177 passing. No deployment needed — pure tooling fix.

Related precedent: FMEA-002 in `docs/bok/mcorch-qa-healing/` (v6.6.9) closed a sibling issue where COMMIT_RE was matching 8-hex UUID prefixes; the same kind of input-validation tightening applies here.

## 🤖 Claude *(21:24:39)*


## 🤖 Claude *(21:24:42)*

**ORO triplet desta task:**
- Operator: AI Agent (MCORCH Master Execution Agent)
- Reviewer: Sovereign (Gabriel)
- Owner: Sovereign — tooling fix em `mcorch-qa-healing` skill, blast radius local (Phase 5c auditor)

Exemption do BoK Gate aplicável: single-file bug patch escopado a feature já documentada (FMEA suite em `docs/bok/mcorch-qa-healing/`).

Lendo os arquivos relevantes antes de editar.

## 🤖 Claude *(21:24:43)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/extract-manifest.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// Proof Manifest Extractor — mcorch-qa-healing FR-001 / FR-012.
> 2	//
> 3	// Pure string parsing: given the text of HANDOFF.md (and an optional
> 4	// proof-manifest.json), produce the list of ProofClaim to verify. No `node:`
> 5	// imports — file I/O is done by the caller (run-audit.ts) and the content is
> 6	// passed in as strings, which keeps this module unit-testable and tsc-clean
> 7	// under tsconfig.app.json.
> 8	
> 9	import type { ClaimKind, ProofClaim } from "./types";
> 10	
> 11	const UUID_RE =
> 12	  /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi;
> 13	// Backtick-tight hex — a git short hash (7) or a longer hash (9-40). Exactly
> 14	// 8 hex is excluded: a backticked 8-hex token is a UUID first-segment
> 15	// shorthand (user / edge / transaction id), not a commit. The tight closing
> 16	// backtick already prevents matching a hyphenated full UUID. (FMEA-002 —
> 17	// confirmed by the v1 dry run, which false-flagged 5 such prefixes.)
> 18	const COMMIT_RE = /`([0-9a-f]{7}|[0-9a-f]{9,40})`/gi;
> 19	const TSC_RE =
> 20	  /(?:tsc|typescript)[^.\n\r]{0,48}(?:zero\s*err|\bclean\b|sem\s*err|erros?\s*\|?\s*0|0\s*err)/i;
> 21	const TEST_COUNT_RE = /(\d+)\s*\/\s*\d+\s*(?:test|teste)|(\d+)\s+(?:tests?\s+)?(?:passed|passam|passou)/i;
> 22	const FILE_PATH_RE =
> 23	  /`([\w./-]+\/[\w./-]+\.(?:ts|tsx|js|jsx|cjs|mjs|md|sql|sh|json))`/gi;
> 24	const KB_RE = /([\w-]+)?[^\w-]{0,12}([\d.]+)\s*kB/gi;
> 25	const EDGE_FN_RE = /^[a-z][a-z0-9-]{2,48}$/;
> 26	
> 27	const MAX_FILE_CLAIMS = 30;
> 28	
> 29	/**
> 30	 * Return the text of the newest `## … Record …` block of HANDOFF.md — from
> 31	 * that heading down to the next `##` heading (or end of file). null if no
> 32	 * Record block is present (a seal with no Record is not a failure: it simply
> 33	 * yields zero claims).
> 34	 */
> 35	export function findNewestRecordBlock(markdown: string): string | null {
> 36	  const lines = markdown.split("\n");
> 37	  let start = -1;
> 38	  for (let i = 0; i < lines.length; i++) {
> 39	    const line = lines[i];
> 40	    if (/^##\s+/.test(line) && /\brecord\b/i.test(line)) {
> 41	      start = i;
> 42	      break;
> 43	    }
> 44	  }
> 45	  if (start === -1) return null;
> 46	  let end = lines.length;
> 47	  for (let i = start + 1; i < lines.length; i++) {
> 48	    // Stop at next heading OR horizontal rule (---) separator
> 49	    if (/^##\s+/.test(lines[i]) || /^-{3,}\s*$/.test(lines[i])) {
> 50	      end = i;
> 51	      break;
> 52	    }
> 53	  }
> 54	  return lines.slice(start, end).join("\n");
> 55	}
> 56	
> 57	function dedupeKey(c: ProofClaim): string {
> 58	  return `${c.kind}:${c.expected.toLowerCase()}`;
> 59	}
> 60	
> 61	/** Extract every typed ProofClaim from a single Record block of text. */
> 62	export function extractClaimsFromBlock(block: string): ProofClaim[] {
> 63	  const claims: ProofClaim[] = [];
> 64	  const seen = new Set<string>();
> 65	
> 66	  const push = (c: ProofClaim): void => {
> 67	    const key = dedupeKey(c);
> 68	    if (seen.has(key)) return;
> 69	    seen.add(key);
> 70	    claims.push(c);
> 71	  };
> 72	
> 73	  // 1. UUIDs → mesh_node / mesh_edge. Every UUID in the Record is extracted;
> 74	  //    classification is by an adjacent "edge"/"aresta" keyword. Prose UUIDs
> 75	  //    are non-strict: if one does not resolve as a mesh row the verifier
> 76	  //    marks it `skip` (it may be a user/transaction/operation id), never
> 77	  //    `fail` (FMEA-002 — no false-positive block).
> 78	  for (const m of block.matchAll(UUID_RE)) {
> 79	    const uuid = m[0].toLowerCase();
> 80	    const idx = m.index ?? 0;
> 81	    const before = block.slice(Math.max(0, idx - 64), idx);
> 82	    const kind: ClaimKind = /\b(?:edge|aresta)\b/i.test(before)
> 83	      ? "mesh_edge"
> 84	      : "mesh_node";
> 85	    push({
> 86	      kind,
> 87	      label: `${kind === "mesh_edge" ? "mesh edge" : "mesh node"} ${uuid.slice(0, 8)}`,
> 88	      expected: uuid,
> 89	      raw: `${before.trim()} ${m[0]}`.slice(-90),
> 90	    });
> 91	  }
> 92	
> 93	  // 2. Backtick-wrapped short hashes → git_commit.
> 94	  for (const m of block.matchAll(COMMIT_RE)) {
> 95	    const hash = m[1].toLowerCase();
> 96	    push({
> 97	      kind: "git_commit",
> 98	      label: `commit ${hash}`,
> 99	      expected: hash,
> 100	      raw: m[0],
> 101	    });
> 102	  }
> 103	
> 104	  // 3. A "tsc … zero errors" phrase → a single tsc claim.
> 105	  const tscMatch = block.match(TSC_RE);
> 106	  if (tscMatch) {
> 107	    push({
> 108	      kind: "tsc",
> 109	      label: "tsc --noEmit clean",
> 110	      expected: "0 errors",
> 111	      raw: tscMatch[0],
> 112	    });
> 113	  }
> 114	
> 115	  // 4. A "N/N tests" or "N passed" phrase → a single test_suite claim.
> 116	  const testMatch = block.match(TEST_COUNT_RE);
> 117	  if (testMatch) {
> 118	    const count = testMatch[1] ?? testMatch[2] ?? "";
> 119	    if (count) {
> 120	      push({
> 121	        kind: "test_suite",
> 122	        label: `test suite — ${count} passing`,
> 123	        expected: count,
> 124	        raw: testMatch[0],
> 125	      });
> 126	    }
> 127	  }
> 128	
> 129	  // 5. Backtick-wrapped repo paths (with a slash, no line suffix) → file_exists.
> 130	  let fileCount = 0;
> 131	  for (const m of block.matchAll(FILE_PATH_RE)) {
> 132	    if (fileCount >= MAX_FILE_CLAIMS) break;
> 133	    const path = m[1];
> 134	    if (path.includes(":")) continue; // exclude `file.ts:line` references
> 135	    push({
> 136	      kind: "file_exists",
> 137	      label: `file ${path}`,
> 138	      expected: path,
> 139	      raw: m[0],
> 140	    });
> 141	    fileCount++;
> 142	  }
> 143	
> 144	  // 6. "<name> NN.N kB" → edge_deploy. A clean kebab name is verified for
> 145	  //    reachability; a size-only mention has expected = the size (→ skip).
> 146	  for (const m of block.matchAll(KB_RE)) {
> 147	    const candidate = (m[1] ?? "").toLowerCase();
> 148	    const size = m[2];
> 149	    const isFn = EDGE_FN_RE.test(candidate) && candidate.includes("-");
> 150	    push({
> 151	      kind: "edge_deploy",
> 152	      label: isFn ? `edge deploy ${candidate}` : `deploy size ${size}kB`,
> 153	      expected: isFn ? candidate : `${size}kB`,
> 154	      raw: m[0],
> 155	    });
> 156	  }
> 157	
> 158	  // 7. ORO Triplet compliance (Lei 4)
> 159	  if (block.trim().length > 0) {
> 160	    const opMatch = block.match(/operator\s*[^:=\n\r]*[:=]\s*([^;\n\r]+)/i);
> 161	    const revMatch = block.match(/reviewer\s*[^:=\n\r]*[:=]\s*([^;\n\r]+)/i);
> 162	    const ownMatch = block.match(/owner\s*[^:=\n\r]*[:=]\s*([^;\n\r]+)/i);
> 163	
> 164	    const clean = (val: string): string => {
> 165	      return val.replace(/^[\s*_`:=]+|[\s*_`.]+$/g, "").trim();
> 166	    };
> 167	
> 168	    if (opMatch && revMatch && ownMatch) {
> 169	      const operator = clean(opMatch[1]);
> 170	      const reviewer = clean(revMatch[1]);
> 171	      const owner = clean(ownMatch[1]);
> 172	
> 173	      if (operator.length >= 3 && reviewer.length >= 3 && owner.length >= 3) {
> 174	        push({
> 175	          kind: "oro_compliance",
> 176	          label: "oro triplet compliance",
> 177	          expected: `Operator = ${operator}; Reviewer = ${reviewer}; Owner = ${owner}`,
> 178	          raw: `Operator: ${opMatch[1].trim()}, Reviewer: ${revMatch[1].trim()}, Owner: ${ownMatch[1].trim()}`,
> 179	          strict: true,
> 180	        });
> 181	      } else {
> 182	        push({
> 183	          kind: "oro_compliance",
> 184	          label: "oro triplet compliance",
> 185	          expected: "malformed",
> 186	          raw: block.slice(0, 200),
> 187	          strict: true,
> 188	        });
> 189	      }
> 190	    } else {
> 191	      push({
> 192	        kind: "oro_compliance",
> 193	        label: "oro triplet compliance",
> 194	        expected: "missing",
> 195	        raw: block.slice(0, 200),
> 196	        strict: true,
> 197	      });
> 198	    }
> 199	  }
> 200	
> 201	  return claims;
> 202	}
> 203	
> 204	/**
> 205	 * Parse an optional proof-manifest.json string (emitted by /handoff Phase 3)
> 206	 * into claims. Currently it contributes the handoff mesh-node UUID, which is
> 207	 * awkward to regex reliably. Malformed JSON is ignored (returns []).
> 208	 */
> 209	export function parseManifestJson(json: string): ProofClaim[] {
> 210	  const claims: ProofClaim[] = [];
> 211	  let data: unknown;
> 212	  try {
> 213	    data = JSON.parse(json);
> 214	  } catch {
> 215	    return claims;
> 216	  }
> 217	  if (!data || typeof data !== "object") return claims;
> 218	  const obj = data as Record<string, unknown>;
> 219	  const nodeId = obj.handoffNodeId;
> 220	  if (typeof nodeId === "string" && UUID_RE.test(nodeId)) {
> 221	    claims.push({
> 222	      kind: "mesh_node",
> 223	      label: `handoff node ${nodeId.slice(0, 8)}`,
> 224	      expected: nodeId.toLowerCase(),
> 225	      raw: `proof-manifest.json:handoffNodeId=${nodeId}`,
> 226	      // Phase 3 structurally asserted this node — a non-resolving handoff
> 227	      // node is a genuine contradiction, so this claim is strict (can fail).
> 228	      strict: true,
> 229	    });
> 230	  }
> 231	  return claims;
> 232	}
> 233	
> 234	/**
> 235	 * Top-level extractor. `handoffMarkdown` is the full text of HANDOFF.md;
> 236	 * `manifestJson` is the optional proof-manifest.json text (hybrid input).
> 237	 */
> 238	export function extractManifest(
> 239	  handoffMarkdown: string,
> 240	  manifestJson?: string,
> 241	): ProofClaim[] {
> 242	  const block = findNewestRecordBlock(handoffMarkdown);
> 243	  const claims: ProofClaim[] = block ? extractClaimsFromBlock(block) : [];
> 244	  if (manifestJson) {
> 245	    const seen = new Set(claims.map(dedupeKey));
> 246	    for (const c of parseManifestJson(manifestJson)) {
> 247	      if (!seen.has(dedupeKey(c))) {
> 248	        seen.add(dedupeKey(c));
> 249	        claims.push(c);
> 250	      }
> 251	    }
> 252	  }
> 253	  return claims;
> 254	}
> 255	
> ```

## 🤖 Claude *(21:24:44)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "ls /home/gcrUX/htdocs/constellation-orchestra/src/test/ 2>&1 | head -50",
  "description": "List existing test files"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> billing.test.ts
> example.test.ts
> phase-zeta.test.tsx
> qa-extract-manifest.test.ts
> qa-verifiers.test.ts
> setup.ts
> useCanvasDesign.test.tsx
> useKnowledgeMesh.test.ts
> useOrchestrationGraph.test.ts
> useOrchestrationStore.test.ts
> useSubscription.test.ts
> ```

## 🤖 Claude *(21:24:52)*


## 🤖 Claude *(21:24:53)*

O test file já existe. Lendo para entender a estrutura antes de adicionar o caso novo.

## 🤖 Claude *(21:24:54)*


🛠️ **Tool Call**: `Read`
```json
{
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/test/qa-extract-manifest.test.ts"
}
```

> **Tool Result (Read)** - ✅ Success
>
> ```
> 1	// Unit tests — mcorch-qa-healing extract-manifest (FRD AT-001 / AT-012).
> 2	// Pure-parser tests: no git, no network, no filesystem.
> 3	
> 4	import { describe, it, expect } from "vitest";
> 5	import {
> 6	  findNewestRecordBlock,
> 7	  extractClaimsFromBlock,
> 8	  parseManifestJson,
> 9	  extractManifest,
> 10	} from "../../scripts/qa/extract-manifest";
> 11	
> 12	const FIXTURE = `# HANDOFF
> 13	
> 14	## Task State
> 15	
> 16	**Some bold paragraph.**
> 17	
> 18	## Bridge Recovery Record (2026-05-20)
> 19	
> 20	Milestone handoff node \`a1b2c3d4-0000-0000-0000-000000000001\` inserted.
> 21	The edge \`b2c3d4e5-0000-0000-0000-000000000002\` DERIVES_FROM the seal.
> 22	TypeScript erros | 0 | \`tsc --noEmit\` clean. 122/122 testes passaram.
> 23	Created \`scripts/qa/run-audit.ts\` and \`docs/bok/x/00-index.md\`.
> 24	See \`orchestrate-content/index.ts\` (path has slash, counts).
> 25	
> 26	| Commit | Conteúdo |
> 27	|--------|----------|
> 28	| \`abc1234\` | feat: thing |
> 29	| \`def5678ab\` | fix: other |
> 30	
> 31	### Arquitetura
> 32	diagram
> 33	
> 34	## Older Phase Record (2026-05-19)
> 35	
> 36	old work, commit \`9999999\` should NOT be picked up.
> 37	`;
> 38	
> 39	describe("findNewestRecordBlock", () => {
> 40	  it("returns the first Record block, bounded by the next ## heading", () => {
> 41	    const block = findNewestRecordBlock(FIXTURE);
> 42	    expect(block).not.toBeNull();
> 43	    expect(block).toContain("Bridge Recovery Record");
> 44	    expect(block).toContain("abc1234");
> 45	    expect(block).not.toContain("Older Phase Record");
> 46	    expect(block).not.toContain("9999999");
> 47	  });
> 48	
> 49	  it("returns null when no Record block exists", () => {
> 50	    expect(findNewestRecordBlock("# Doc\n\n## Task State\n\nnothing here")).toBeNull();
> 51	  });
> 52	});
> 53	
> 54	describe("extractClaimsFromBlock", () => {
> 55	  const claims = extractClaimsFromBlock(findNewestRecordBlock(FIXTURE) ?? "");
> 56	  const byKind = (k: string) => claims.filter((c) => c.kind === k);
> 57	
> 58	  it("extracts backtick-wrapped commit hashes", () => {
> 59	    const commits = byKind("git_commit").map((c) => c.expected);
> 60	    expect(commits).toContain("abc1234");
> 61	    expect(commits).toContain("def5678ab");
> 62	  });
> 63	
> 64	  it("does not pick up hashes from an older Record block", () => {
> 65	    expect(byKind("git_commit").map((c) => c.expected)).not.toContain("9999999");
> 66	  });
> 67	
> 68	  it("classifies a UUID as mesh_edge when 'edge' precedes it", () => {
> 69	    const edge = byKind("mesh_edge");
> 70	    expect(edge).toHaveLength(1);
> 71	    expect(edge[0].expected).toBe("b2c3d4e5-0000-0000-0000-000000000002");
> 72	  });
> 73	
> 74	  it("classifies a bare/node UUID as mesh_node", () => {
> 75	    expect(byKind("mesh_node").map((c) => c.expected)).toContain(
> 76	      "a1b2c3d4-0000-0000-0000-000000000001",
> 77	    );
> 78	  });
> 79	
> 80	  it("extracts a single tsc claim from a 'tsc … clean' phrase", () => {
> 81	    expect(byKind("tsc")).toHaveLength(1);
> 82	    expect(byKind("tsc")[0].expected).toBe("0 errors");
> 83	  });
> 84	
> 85	  it("extracts a test_suite claim with the asserted count", () => {
> 86	    const tests = byKind("test_suite");
> 87	    expect(tests).toHaveLength(1);
> 88	    expect(tests[0].expected).toBe("122");
> 89	  });
> 90	
> 91	  it("extracts file_exists claims for backtick repo paths", () => {
> 92	    const files = byKind("file_exists").map((c) => c.expected);
> 93	    expect(files).toContain("scripts/qa/run-audit.ts");
> 94	    expect(files).toContain("docs/bok/x/00-index.md");
> 95	  });
> 96	
> 97	  it("deduplicates repeated claims", () => {
> 98	    const dup = extractClaimsFromBlock("`abc1234` and again `abc1234`");
> 99	    expect(dup.filter((c) => c.kind === "git_commit")).toHaveLength(1);
> 100	  });
> 101	
> 102	  it("does not treat a backtick 8-hex UUID-prefix as a commit", () => {
> 103	    const cl = extractClaimsFromBlock("edge `fac985dd` and user `924cb32e` cited inline");
> 104	    expect(cl.filter((c) => c.kind === "git_commit")).toHaveLength(0);
> 105	  });
> 106	
> 107	  it("extracts 7-char and 9+-char commit hashes", () => {
> 108	    const cl = extractClaimsFromBlock("`03911e9` and `def5678ab` shipped");
> 109	    expect(cl.filter((c) => c.kind === "git_commit").map((c) => c.expected).sort()).toEqual([
> 110	      "03911e9",
> 111	      "def5678ab",
> 112	    ]);
> 113	  });
> 114	
> 115	  it("extracts ORO triplet in inline format", () => {
> 116	    const cl = extractClaimsFromBlock(
> 117	      "**ORO triplet desta task (Lei 4):** Operator = MCORCH Agent; Reviewer = Sovereign; Owner = Sovereign Gabriel.",
> 118	    );
> 119	    const oro = cl.find((c) => c.kind === "oro_compliance");
> 120	    expect(oro).toBeDefined();
> 121	    expect(oro?.expected).toBe("Operator = MCORCH Agent; Reviewer = Sovereign; Owner = Sovereign Gabriel");
> 122	  });
> 123	
> 124	  it("extracts ORO triplet in list format with asterisks", () => {
> 125	    const cl = extractClaimsFromBlock(`
> 126	**ORO triplet desta task:**
> 127	- **Operator:** MCORCH Master Agent
> 128	- **Reviewer:** Sovereign (Gabriel)
> 129	- **Owner:** Sovereign (Gabriel, risk management)
> 130	`);
> 131	    const oro = cl.find((c) => c.kind === "oro_compliance");
> 132	    expect(oro).toBeDefined();
> 133	    expect(oro?.expected).toBe(
> 134	      "Operator = MCORCH Master Agent; Reviewer = Sovereign (Gabriel); Owner = Sovereign (Gabriel, risk management)",
> 135	    );
> 136	  });
> 137	
> 138	  it("produces missing when ORO triplet is absent", () => {
> 139	    const cl = extractClaimsFromBlock("Just some test results, no ORO here.");
> 140	    const oro = cl.find((c) => c.kind === "oro_compliance");
> 141	    expect(oro).toBeDefined();
> 142	    expect(oro?.expected).toBe("missing");
> 143	  });
> 144	
> 145	  it("produces malformed when one role is empty", () => {
> 146	    const cl = extractClaimsFromBlock("ORO triplet desta task: Operator = ; Reviewer = Sovereign; Owner = Sovereign.");
> 147	    const oro = cl.find((c) => c.kind === "oro_compliance");
> 148	    expect(oro).toBeDefined();
> 149	    expect(oro?.expected).toBe("malformed");
> 150	  });
> 151	});
> 152	
> 153	describe("tsc phrase variants", () => {
> 154	  it("matches 'tsc zero erros'", () => {
> 155	    expect(extractClaimsFromBlock("o `tsc` zero erros aqui").some((c) => c.kind === "tsc")).toBe(true);
> 156	  });
> 157	  it("matches 'TypeScript … 0 err'", () => {
> 158	    expect(extractClaimsFromBlock("TypeScript: 0 errors").some((c) => c.kind === "tsc")).toBe(true);
> 159	  });
> 160	  it("does not invent a tsc claim from unrelated prose", () => {
> 161	    expect(extractClaimsFromBlock("a clean kitchen and a nice day").some((c) => c.kind === "tsc")).toBe(false);
> 162	  });
> 163	});
> 164	
> 165	describe("parseManifestJson", () => {
> 166	  it("emits a strict mesh_node claim for handoffNodeId", () => {
> 167	    const claims = parseManifestJson('{"handoffNodeId":"a1b2c3d4-0000-0000-0000-000000000099"}');
> 168	    expect(claims).toHaveLength(1);
> 169	    expect(claims[0].kind).toBe("mesh_node");
> 170	    expect(claims[0].strict).toBe(true);
> 171	  });
> 172	
> 173	  it("returns [] for malformed JSON", () => {
> 174	    expect(parseManifestJson("{not json")).toEqual([]);
> 175	  });
> 176	
> 177	  it("returns [] when handoffNodeId is absent or not a UUID", () => {
> 178	    expect(parseManifestJson('{"handoffNodeId":"not-a-uuid"}')).toEqual([]);
> 179	    expect(parseManifestJson("{}")).toEqual([]);
> 180	  });
> 181	});
> 182	
> 183	describe("extractManifest", () => {
> 184	  it("merges the proof-manifest.json claim with parsed claims", () => {
> 185	    const claims = extractManifest(
> 186	      FIXTURE,
> 187	      '{"handoffNodeId":"c3d4e5f6-0000-0000-0000-000000000003"}',
> 188	    );
> 189	    const strict = claims.find((c) => c.kind === "mesh_node" && c.strict === true);
> 190	    expect(strict).toBeDefined();
> 191	    expect(strict?.expected).toBe("c3d4e5f6-0000-0000-0000-000000000003");
> 192	  });
> 193	
> 194	  it("returns an empty manifest when there is no Record block", () => {
> 195	    expect(extractManifest("# Doc\n\nno record")).toEqual([]);
> 196	  });
> 197	});
> 198	
> ```

## 🤖 Claude *(21:25:03)*


## 🤖 Claude *(21:25:06)*

Tenho tudo que preciso. Aplicando a edição em `extract-manifest.ts` — adiciono a guarda de pure-decimal no loop e estendo o comentário acima do `COMMIT_RE` para registrar a exclusão.

## 🤖 Claude *(21:25:14)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/extract-manifest.ts",
  "old_string": "// Backtick-tight hex \u2014 a git short hash (7) or a longer hash (9-40). Exactly\n// 8 hex is excluded: a backticked 8-hex token is a UUID first-segment\n// shorthand (user / edge / transaction id), not a commit. The tight closing\n// backtick already prevents matching a hyphenated full UUID. (FMEA-002 \u2014\n// confirmed by the v1 dry run, which false-flagged 5 such prefixes.)\nconst COMMIT_RE = /`([0-9a-f]{7}|[0-9a-f]{9,40})`/gi;",
  "new_string": "// Backtick-tight hex \u2014 a git short hash (7) or a longer hash (9-40). Exactly\n// 8 hex is excluded: a backticked 8-hex token is a UUID first-segment\n// shorthand (user / edge / transaction id), not a commit. The tight closing\n// backtick already prevents matching a hyphenated full UUID. (FMEA-002 \u2014\n// confirmed by the v1 dry run, which false-flagged 5 such prefixes.)\n// Pure-decimal matches are skipped at the call site below: a backticked\n// 14-digit migration timestamp (e.g. `20260525173500`) satisfies [0-9a-f]{9,40}\n// but is never a commit. (v6.8.2 handoff seal regression \u2014 commit 17ff2ca.)\nconst COMMIT_RE = /`([0-9a-f]{7}|[0-9a-f]{9,40})`/gi;"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/scripts/qa/extract-manifest.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:25:17)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/scripts/qa/extract-manifest.ts",
  "old_string": "  // 2. Backtick-wrapped short hashes \u2192 git_commit.\n  for (const m of block.matchAll(COMMIT_RE)) {\n    const hash = m[1].toLowerCase();\n    push({\n      kind: \"git_commit\",\n      label: `commit ${hash}`,\n      expected: hash,\n      raw: m[0],\n    });\n  }",
  "new_string": "  // 2. Backtick-wrapped short hashes \u2192 git_commit.\n  for (const m of block.matchAll(COMMIT_RE)) {\n    const hash = m[1].toLowerCase();\n    if (/^\\d+$/.test(hash)) continue; // skip pure-decimal (migration timestamps)\n    push({\n      kind: \"git_commit\",\n      label: `commit ${hash}`,\n      expected: hash,\n      raw: m[0],\n    });\n  }"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/scripts/qa/extract-manifest.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:25:33)*


## 🤖 Claude *(21:25:34)*

Adicionando o caso Vitest após o teste sibling de exclusão (UUID-prefix de 8-hex) — mesma categoria de input-validation tightening.

## 🤖 Claude *(21:25:40)*


🛠️ **Tool Call**: `Edit`
```json
{
  "replace_all": false,
  "file_path": "/home/gcrUX/htdocs/constellation-orchestra/src/test/qa-extract-manifest.test.ts",
  "old_string": "  it(\"does not treat a backtick 8-hex UUID-prefix as a commit\", () => {\n    const cl = extractClaimsFromBlock(\"edge `fac985dd` and user `924cb32e` cited inline\");\n    expect(cl.filter((c) => c.kind === \"git_commit\")).toHaveLength(0);\n  });",
  "new_string": "  it(\"does not treat a backtick 8-hex UUID-prefix as a commit\", () => {\n    const cl = extractClaimsFromBlock(\"edge `fac985dd` and user `924cb32e` cited inline\");\n    expect(cl.filter((c) => c.kind === \"git_commit\")).toHaveLength(0);\n  });\n\n  it(\"does not treat a pure-decimal migration timestamp as a commit\", () => {\n    const cl = extractClaimsFromBlock(\n      \"Migration `20260525173500` applied; sealed by commit `bfe2f43`.\",\n    );\n    const commits = cl.filter((c) => c.kind === \"git_commit\").map((c) => c.expected);\n    expect(commits).not.toContain(\"20260525173500\");\n    expect(commits).toContain(\"bfe2f43\");\n  });"
}
```

> **Tool Result (Edit)** - ✅ Success
>
> ```
> The file /home/gcrUX/htdocs/constellation-orchestra/src/test/qa-extract-manifest.test.ts has been updated successfully. (file state is current in your context — no need to Read it back)
> ```

## 🤖 Claude *(21:25:44)*


## 🤖 Claude *(21:25:45)*

Pulando TaskCreate — trabalho de 3 passos lineares, sem dependências externas. Rodando o test suite para validar materialmente.

## 🤖 Claude *(21:25:45)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "bun run test 2>&1 | tail -40",
  "description": "Run vitest suite to verify fix"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> stderr | src/test/useSubscription.test.ts > useSubscription > openPortal > shows error toast when portal invoke throws
> Portal error: Error: Stripe unavailable
>     at [90m/home/gcrUX/htdocs/constellation-orchestra/[39msrc/test/useSubscription.test.ts:140:40
>     at [90mfile:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:155:11
>     at [90mfile:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:752:26
>     at [90mfile:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:1897:20
>     at new Promise (<anonymous>)
>     at runWithTimeout [90m(file:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:1863:10[90m)[39m
>     at runTest [90m(file:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:1574:12[90m)[39m
>     at runSuite [90m(file:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:1729:8[90m)[39m
>     at runSuite [90m(file:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:1729:8[90m)[39m
>     at runSuite [90m(file:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:1729:8[90m)[39m
> 
> stderr | src/test/useSubscription.test.ts > useSubscription > openPortal > clears loading after portal error
> Portal error: Error: Stripe unavailable
>     at [90m/home/gcrUX/htdocs/constellation-orchestra/[39msrc/test/useSubscription.test.ts:154:40
>     at [90mfile:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:155:11
>     at [90mfile:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:752:26
>     at [90mfile:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:1897:20
>     at new Promise (<anonymous>)
>     at runWithTimeout [90m(file:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:1863:10[90m)[39m
>     at runTest [90m(file:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:1574:12[90m)[39m
>     at runSuite [90m(file:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:1729:8[90m)[39m
>     at runSuite [90m(file:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:1729:8[90m)[39m
>     at runSuite [90m(file:///home/gcrUX/htdocs/constellation-orchestra/[39mnode_modules/[4m@vitest/runner[24m/dist/chunk-hooks.js:1729:8[90m)[39m
> 
>  ✓ src/test/useSubscription.test.ts (16 tests) 77ms
>  ✓ src/test/useOrchestrationGraph.test.ts (21 tests) 79ms
>  ✓ src/test/billing.test.ts (22 tests) 22ms
>  ✓ src/test/useOrchestrationStore.test.ts (29 tests) 19ms
>  ✓ src/test/qa-extract-manifest.test.ts (25 tests) 18ms
>  ✓ src/test/qa-verifiers.test.ts (26 tests) 14ms
>  ✓ src/test/example.test.ts (1 test) 3ms
> 
>  Test Files  10 passed (10)
>       Tests  177 passed (177)
>    Start at  18:25:46
>    Duration  4.53s (transform 583ms, setup 819ms, collect 1.90s, tests 1.42s, environment 4.96s, prepare 1.53s)
> ```

## 🤖 Claude *(21:26:10)*


## 🤖 Claude *(21:26:16)*

Fix aplicado e validado materialmente.

**Mudanças**
- `scripts/qa/extract-manifest.ts:97` — guarda `if (/^\d+$/.test(hash)) continue;` no loop `matchAll(COMMIT_RE)`; comentário acima do regex (linhas 18-20) estendido com o caso pure-decimal.
- `src/test/qa-extract-manifest.test.ts:107-114` — caso novo `"does not treat a pure-decimal migration timestamp as a commit"` cobrindo timestamp `20260525173500` (rejeitado) e commit `bfe2f43` (aceito) no mesmo bloco.

**Prova material (Lei 1)**
```
Test Files  10 passed (10)
     Tests  177 passed (177)
```
qa-extract-manifest passou de 24 → 25 testes; total do projeto 176 → 177 conforme previsto. Zero regressões nos outros 9 arquivos.

Sem commit feito — aguardando autorização explícita.

## 👤 User *(21:29:10)*

ok continue

## 🤖 Claude *(21:29:19)*


## 🤖 Claude *(21:29:19)*

Seguindo o protocolo de commit. Coletando estado git em paralelo.

## 🤖 Claude *(21:29:20)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git status",
  "description": "Show working tree status"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> On branch main
> Your branch is up to date with 'origin/main'.
> 
> Changes not staged for commit:
>   (use "git add <file>..." to update what will be committed)
>   (use "git restore <file>..." to discard changes in working directory)
> 	modified:   memory/heartbeat-state.json
> 	modified:   scripts/qa/extract-manifest.ts
> 	modified:   src/test/qa-extract-manifest.test.ts
> 
> no changes added to commit (use "git add" and/or "git commit -a")
> ```

## 🤖 Claude *(21:29:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git diff scripts/qa/extract-manifest.ts src/test/qa-extract-manifest.test.ts",
  "description": "Diff of staged changes"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> diff --git a/scripts/qa/extract-manifest.ts b/scripts/qa/extract-manifest.ts
> index 034f93d..2470682 100644
> --- a/scripts/qa/extract-manifest.ts
> +++ b/scripts/qa/extract-manifest.ts
> @@ -15,6 +15,9 @@ const UUID_RE =
>  // shorthand (user / edge / transaction id), not a commit. The tight closing
>  // backtick already prevents matching a hyphenated full UUID. (FMEA-002 —
>  // confirmed by the v1 dry run, which false-flagged 5 such prefixes.)
> +// Pure-decimal matches are skipped at the call site below: a backticked
> +// 14-digit migration timestamp (e.g. `20260525173500`) satisfies [0-9a-f]{9,40}
> +// but is never a commit. (v6.8.2 handoff seal regression — commit 17ff2ca.)
>  const COMMIT_RE = /`([0-9a-f]{7}|[0-9a-f]{9,40})`/gi;
>  const TSC_RE =
>    /(?:tsc|typescript)[^.\n\r]{0,48}(?:zero\s*err|\bclean\b|sem\s*err|erros?\s*\|?\s*0|0\s*err)/i;
> @@ -93,6 +96,7 @@ export function extractClaimsFromBlock(block: string): ProofClaim[] {
>    // 2. Backtick-wrapped short hashes → git_commit.
>    for (const m of block.matchAll(COMMIT_RE)) {
>      const hash = m[1].toLowerCase();
> +    if (/^\d+$/.test(hash)) continue; // skip pure-decimal (migration timestamps)
>      push({
>        kind: "git_commit",
>        label: `commit ${hash}`,
> diff --git a/src/test/qa-extract-manifest.test.ts b/src/test/qa-extract-manifest.test.ts
> index 239d691..5f7b9bc 100644
> --- a/src/test/qa-extract-manifest.test.ts
> +++ b/src/test/qa-extract-manifest.test.ts
> @@ -104,6 +104,15 @@ describe("extractClaimsFromBlock", () => {
>      expect(cl.filter((c) => c.kind === "git_commit")).toHaveLength(0);
>    });
>  
> +  it("does not treat a pure-decimal migration timestamp as a commit", () => {
> +    const cl = extractClaimsFromBlock(
> +      "Migration `20260525173500` applied; sealed by commit `bfe2f43`.",
> +    );
> +    const commits = cl.filter((c) => c.kind === "git_commit").map((c) => c.expected);
> +    expect(commits).not.toContain("20260525173500");
> +    expect(commits).toContain("bfe2f43");
> +  });
> +
>    it("extracts 7-char and 9+-char commit hashes", () => {
>      const cl = extractClaimsFromBlock("`03911e9` and `def5678ab` shipped");
>      expect(cl.filter((c) => c.kind === "git_commit").map((c) => c.expected).sort()).toEqual([
> ```

> **Tool Result (Unknown Tool)** - ✅ Success
>
> ```
> 87961ab docs(handoff): fix Phase 5c COMMIT_RE false-positive on migration timestamp
> 17ff2ca docs(handoff): seal v6.8.2 — OE-661 flywheel validated E2E + PGRST203 hotfix
> 1033bc3 docs(readme): v6.8.2 — OE-661 flywheel validated E2E + PGRST203 hotfix
> bfe2f43 fix(db): drop deduct_mco_coins 2-arg overload — PGRST203 hotfix
> 9374d72 docs(handoff): seal v6.8.1 — Ollama × OpenClaw provider integration + gateway crash-loop recovery
> 8484950 docs: update README.md and HANDOFF.md with version v6.8.0 and milestone proofs
> 56b092d feat(edge): improve node type mapping and error details propagation in canvas-execute
> cfbd4e4 docs: update README.md and HANDOFF.md with version v6.7.9 and milestone proofs
> 21584d4 feat(canvas): implement interactive Magic Prompt feature with mcoCoin credit spent (1, 2, 5 coins) across GenerateImage, SceneCompose, and ImageToVideo inspectors
> 4a7c450 fix(edge-functions): parse nested payload.video.url in Higgsfield webhook callback
> ```

## 🤖 Claude *(21:29:22)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git log --oneline -10",
  "description": "Recent commit message style"
}
```

## 🤖 Claude *(21:29:41)*


## 🤖 Claude *(21:29:43)*

Stage seletivo (deixando `memory/heartbeat-state.json` de fora — runtime state alheio a este fix) e commit.

## 🤖 Claude *(21:29:46)*


🛠️ **Tool Call**: `Bash`
```json
{
  "command": "git add scripts/qa/extract-manifest.ts src/test/qa-extract-manifest.test.ts && git commit -m \"$(cat <<'EOF'\nfix(qa): COMMIT_RE skips pure-decimal \u2014 Phase 5c accepts migration filenames\n\nCloses the gap left by the 87961ab workaround, which dodged the\nfalse-positive by rewriting HANDOFF.md to spell out the full migration\nfilename. Future seals can now cite `<timestamp>` inline without tripping\nthe auditor. Same input-validation tightening pattern as FMEA-002\n(8-hex UUID-prefix exclusion).\nEOF\n)\" && git log -1 --format='%H %s'",
  "description": "Stage two files, commit, print new HEAD"
}
```

> **Tool Result (Bash)** - ✅ Success
>
> ```
> [main 1d46283] fix(qa): COMMIT_RE skips pure-decimal — Phase 5c accepts migration filenames
>  2 files changed, 13 insertions(+)
> 1d46283f2170d489b213763466192541f25f8f3e fix(qa): COMMIT_RE skips pure-decimal — Phase 5c accepts migration filenames
> ```

## 🤖 Claude *(21:29:53)*

Commit `1d46283` selado em `main`. 2 arquivos, +13 linhas. `memory/heartbeat-state.json` permanece unstaged conforme intenção.

## 👤 User *(21:29:57)*

<command-message>handoff</command-message>
<command-name>/handoff</command-name>

## 👤 User *(21:29:57)*

# ShakeHands — Session Seal Protocol v4

Execute the ShakeHands /handoff ritual to seal this session.

> **v4 (2026-05-15):** Reordered phases — Knowledge Mesh Milestone (Phase 3) now runs
> **before** README.md update (Phase 4), so the live node count query captures the handoff
> node itself. Previously the badge was always 1-3 nodes behind.
>
> **v3 (2026-05-14):** Added Phase 6 BoK Seal Status — verifies any module
> work in this session has a corresponding sealed BoK suite per MCORCH Master
> Execution Protocol. Blocks seal if significant module work lacks BoK.

---

## PRE-FLIGHT (execute ALL in parallel before anything else)

```bash
git status --short                          # inventory uncommitted changes
git diff HEAD --stat                        # change scope
git log --oneline -7                        # recent history + commit style
npx tsc --noEmit 2>&1 | tail -20           # TypeScript strict check
docker ps --filter "name=mcorch" --format "{{.Names}}: {{.Status}}"
docker ps --filter "name=mega-brain" --format "{{.Names}}: {{.Status}}"
curl -s http://localhost:8001/api/v2/heartbeat  # chroma API v2 health
```

Read in parallel:
- `HANDOFF.md` (current state, pending actions)
- `CLAUDE.md` (architecture rules)
- `/home/ubuntu/.claude/projects/-home-gcrUX-htdocs-constellation-orchestra/memory/MEMORY.md`

If TypeScript has errors → fix them before proceeding. Report any infra anomalies in the final summary.

---

## PHASE 1 — SECURITY AUDIT

Run these checks and report findings. **Block the seal if any CRITICAL finding exists.**

> ⚠️ **SCOPE NOTE:** This phase scans changes that exist NOW (before Phase 5 writes HANDOFF.md).
> A second mandatory scan runs in Phase 5b, after HANDOFF.md is written and before it is committed.

```bash
# 1a. Secret leak scan — check staged + working tree for hardcoded credentials
git diff HEAD | grep -E "(sk-[a-zA-Z0-9]{20,}|AIza[0-9A-Za-z_-]{35}|eyJ[a-zA-Z0-9._-]{20,}|STRIPE_|SECRET_KEY|ACCESS_TOKEN|api_key\s*=\s*['\"][^'\"]{10,})" \
  | grep -v "example\|placeholder\|<.*>\|your-key\|YOUR_" | head -20

# 1b. Edge function JWT enforcement — every user-facing function must verify JWT
grep -rL "Authorization\|jwt\|JWT\|service_role" supabase/functions/*/index.ts \
  | grep -v "get-infra-status\|watchdog" || echo "ALL FUNCTIONS: JWT enforced ✅"

# 1c. Client-side coin deduction guard — must NEVER update mco_balance directly from client
grep -rn "mco_balance.*update\|UPDATE.*mco_balance" src/ \
  | grep -v "settings\|top.up\|topup\|SettingsPage" | head -10 || echo "NO VIOLATIONS ✅"

# 1d. RLS bypass risk — check for supabase.rpc calls without auth context
grep -rn "service_role\|bypass.*rls\|rls.*bypass" src/ | head -10 || echo "NO VIOLATIONS ✅"

# 1e. Sensitive data in console.log
grep -rn "console\.log.*token\|console\.log.*key\|console\.log.*secret\|console\.log.*password" src/ \
  | head -10 || echo "NO SENSITIVE LOGS ✅"
```

**Security verdict:** list each check as ✅ PASS / ⚠️ WARN / 🔴 BLOCK.
Only proceed if no 🔴 findings.

---

### DOCUMENTATION CREDENTIAL RULE (invariant — never violate)

**When writing HANDOFF.md, README.md, or any committed documentation:**

- ✅ DO: describe WHERE a credential is stored → `VITE_GEMINI_API_KEY` is set in `.env` (local) and `GEMINI_API_KEY` in the Supabase vault
- ✅ DO: reference digest/fingerprint if useful → `GEMINI_API_KEY (digest 0fe0e159...)`
- 🔴 NEVER: include the actual credential value → `AIzaSyBv...`, `sk-...`, `eyJ...`

> **Rationale:** Phase 1 scans changes that predate the HANDOFF.md write. Any credential embedded
> in HANDOFF.md during Phase 5 escapes Phase 1 entirely and goes directly to the remote.
> This rule is the primary prevention layer; Phase 5b is the detection backstop.

---

## PHASE 2 — GRANULAR COMMITS

Group uncommitted changes by concern and commit each group separately.

**Commit rules (from memory + project convention):**
- Prefix: `feat:`, `fix:`, `refactor:`, `chore:`, `docs:`
- Body: one paragraph explaining the WHY (milestone orientation, not diff description)
- **NEVER** add `Co-Authored-By` trailer
- **NEVER** use `git add -A` — stage files explicitly by name
- Skip: `build_log.txt`, `node_modules/`, `dist/`, `.env`, `check_types.ts`, `scratch/`

Stage and commit each logical group before moving to the next phase.

---

## PHASE 3 — KNOWLEDGE MESH MILESTONE

> ⚠️ **ORDER MATTERS:** This phase runs BEFORE Phase 4 (README badge) so the live count
> query captures this handoff node. Do not swap the order.

Insert a milestone node into mcorch_nodes to mark this session in the knowledge graph:

```bash
source .env
SUPABASE_URL="https://bcyvddsykvehvpwstlfa.supabase.co"
SESSION_PHASE="<phase-name-slug>"
SESSION_SUMMARY="<one-sentence summary of what was accomplished>"

curl -s -X POST "${SUPABASE_URL}/rest/v1/mcorch_nodes" \
  -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}" \
  -H "Content-Type: application/json" \
  -H "Prefer: return=representation" \
  -d "{
    \"name\": \"session-handoff-$(date +%Y%m%d)-${SESSION_PHASE}\",
    \"node_type\": \"handoff\",
    \"content\": \"[HANDOFF SEAL] ${SESSION_SUMMARY}\",
    \"stability_score\": 1.0,
    \"project_id\": null,
    \"user_id\": null,
    \"metadata\": {
      \"session\": \"${SESSION_PHASE}\",
      \"sealed_at\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",
      \"commits\": \"$(git log --oneline -5 | head -5 | tr '\n' '|')\"
    }
  }" | python3 -c "import sys,json; d=json.load(sys.stdin); print('Node ID:', d[0]['id'] if isinstance(d,list) else d.get('id','error'))" 2>/dev/null \
  || echo "⚠️ Knowledge Mesh insert failed — log manually"
```

Then trigger embedding for the new node:
```bash
NODE_ID="<id-from-above>"
curl -s -X POST "${SUPABASE_URL}/functions/v1/embed-mcorch-node" \
  -H "apikey: ${SUPABASE_SERVICE_ROLE_KEY}" \
  -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}" \
  -H "Content-Type: application/json" \
  -d "{\"record\": {\"id\": \"${NODE_ID}\"}}" | python3 -c "import sys,json; d=json.load(sys.stdin); print('Embedded:', d)" 2>/dev/null \
  || echo "⚠️ Embedding failed — node persisted but not vectorized"
```

Emit `proof-manifest.json` so Phase 5c can verify this handoff node strictly:
```bash
echo "{\"handoffNodeId\": \"${NODE_ID}\"}" > proof-manifest.json
```

---

## PHASE 4 — README.md UPDATE

> ℹ️ Phase 3 (milestone node) has already been inserted — the live count below includes it.

Update `/README.md` to reflect the current session's work.

**Required updates:**
1. **Badges block** (top of file) — update dynamic values:
   - `neural_mesh-XXX_nodes` badge → fetch real count:
     ```bash
     curl -s "https://bcyvddsykvehvpwstlfa.supabase.co/rest/v1/mcorch_nodes?select=id&limit=1" \
       -H "apikey: $(grep SUPABASE_SERVICE_ROLE_KEY .env | cut -d'"' -f2)" \
       -H "Authorization: Bearer $(grep SUPABASE_SERVICE_ROLE_KEY .env | cut -d'"' -f2)" \
       -H "Prefer: count=exact" -I 2>/dev/null | grep -i content-range | grep -o '[0-9]*$'
     ```
   - `version-X.X.X` badge → increment patch version (or minor if major feature landed)
   - If new phase shipped → add phase badge (e.g. `Phase_Zeta-live-cyan`)

2. **Phase Status table** — add new row for this session's phase:
   ```
   | Phase Zeta — <Name> | ✅ <one-line summary> |
   ```

3. **What's New section** — prepend a new entry under the most recent one:
   ```markdown
   ### [v5.X.X] — <Phase Name> (<date>)
   - <bullet: major feature 1>
   - <bullet: major feature 2>
   ```

4. **Core metrics** (if present in README) — update node/edge counts.

Commit README separately:
```
docs(readme): vX.X.X — <phase name> — <one-line change summary>
```

---

## PHASE 5 — HANDOFF.md UPDATE

Rewrite the relevant sections of `HANDOFF.md` — **append, never replace history**.

**Required updates:**
1. **Task State table** — add new row:
   ```
   | **<Phase Name>** | ✅ <one-line summary> |
   ```

2. **New Record section** — add at the top of the history (after the Task State table):
   ```markdown
   ## <Phase Name> Record (<YYYY-MM-DD>)

   <one-paragraph prose summary of what changed and why>

   | Action | Result |
   |--------|--------|
   | `<file/function changed>` | ✅ <what it does now> |
   ...

   | Commit | Conteúdo |
   |--------|----------|
   | `<hash>` | <message> |
   ...

   ### Arquitetura <Phase Name>
   ```code block with data flow or key architecture diagram```
   ```

3. **Pending Actions** — check off completed items (~~strikethrough~~), add new ones discovered this session.

4. **GraphRAG State** section — update node/edge counts.

5. **Infrastructure** table — update container health.

---

## PHASE 5b — HANDOFF.md SECRET SCAN (mandatory before commit)

**Run this scan on the HANDOFF.md content about to be committed. Block if any finding exists.**

```bash
# 5b-1. Scan HANDOFF.md for real credential values
grep -nE "(AIza[0-9A-Za-z_-]{35}|sk-[a-zA-Z0-9]{20,}|eyJ[a-zA-Z0-9._-]{40,}|ghp_[a-zA-Z0-9]{36}|xox[baprs]-[a-zA-Z0-9-]+|[a-zA-Z0-9]{32,}=\s*['\"]?[A-Za-z0-9+/]{40,})" HANDOFF.md \
  | grep -v "example\|placeholder\|<.*>\|your-key\|YOUR_\|digest\|sha256\|hash\|fingerprint" \
  | head -20 || echo "HANDOFF.md: NO CREDENTIALS FOUND ✅"

# 5b-2. Specifically check for Google API keys (AIza prefix = 39 chars total)
grep -n "AIza[0-9A-Za-z_-]\{35\}" HANDOFF.md | head -10 || echo "NO GOOGLE API KEYS ✅"

# 5b-3. Check for any = "value" pattern that looks like a real assignment
grep -nE "=\s*['\"][A-Za-z0-9_\-]{20,}['\"]" HANDOFF.md \
  | grep -v "example\|placeholder\|<.*>\|your-\|YOUR_\|digest\|hash\|uuid\|id.*[0-9a-f-]\{36\}" \
  | head -10 || echo "NO INLINE ASSIGNMENTS ✅"
```

**If any check returns a match:**
1. 🔴 **DO NOT COMMIT** HANDOFF.md
2. Rewrite the offending section — replace the actual value with its location description
3. Re-run Phase 5b until all checks pass
4. Only then proceed to commit HANDOFF.md

Commit HANDOFF.md only after Phase 5b passes:
```
docs(handoff): seal <phase name> — <one-line summary>
```

---

## PHASE 5c — MATERIAL PROOF AUDIT (mandatory before push)

**Independently re-verify every material-proof claim of this seal. Block if any is contradicted.**

> ⚠️ Closes the Survival Law 1 (Materiality) self-grading weakness — this audit is mechanical,
> not self-reported. Skill: `mcorch-qa-healing` · SOP: `docs/processes/handoff-material-proof-audit.md`.

```bash
# Runs after Phase 5b, so the newest HANDOFF.md Record block is this seal's.
bun run scripts/qa/run-audit.ts HANDOFF.md
```

The audit parses the newest `## … Record` block and verifies each claim — commit hashes
(`git cat-file`), mesh UUIDs (`mcorch_nodes`/`mcorch_edges`), `tsc --noEmit`, the test suite,
edge-function reachability, file paths — then prints a Proof Manifest table and exits.

**Gate verdict:**
- **exit 0 — `SEAL ALLOWED`** → embed the Proof Manifest in the Phase 8 report (`📋 PROVA MATERIAL`); proceed to Phase 6.
- **exit 1 — `SEAL BLOCKED`** → 🔴 **BLOCK the seal.** Do NOT push. For each 🔴, fix the real
  cause — never fabricate proof (Law 1) — and re-run this phase until `SEAL ALLOWED`. If a 🔴 is a
  strict handoff-node claim, re-attempt the Phase 3 insert once (SOP Cenário D), then re-run.
- `⏭ skip` rows (infra unreachable · non-mesh UUID · size-only deploy) never block — report them.

---

## PHASE 6 — BoK SEAL STATUS (mandatory before push)

**Verify any significant module work in this session has a sealed BoK suite per CLAUDE.md MCORCH Master Execution Protocol.**

```bash
# 6-1. List BoK suites present + check completeness
for slug in $(ls docs/bok/ 2>/dev/null); do
  required=(00-index 01-mrd 02-brd 03-prd 04-frd 05-sdd 06-data-model 07-process-flow 08-quality-metrics)
  missing=()
  for doc in "${required[@]}"; do
    [ -f "docs/bok/$slug/$doc.md" ] || missing+=("$doc")
  done
  [ ${#missing[@]} -eq 0 ] \
    && echo "✅ $slug — BoK complete (9 docs)" \
    || echo "⚠️ $slug — incomplete (missing: ${missing[*]})"
done

# 6-2. Check session touched code in new src/pages/ or new supabase/functions/ that lacks BoK
session_new_modules=$(git diff --name-only HEAD~10..HEAD 2>/dev/null | grep -E "^(src/pages/|supabase/functions/|src/components/[A-Z])" | awk -F/ '{print "/"}' | sort -u)
echo "Session touched modules: $session_new_modules"

# 6-3. Mesh seal nodes for sealed BoK suites
source .env 2>/dev/null
if [ -n "$SUPABASE_SERVICE_ROLE_KEY" ]; then
  curl -s "$SUPABASE_URL/rest/v1/mcorch_nodes?node_type=eq.documentation_suite&select=id,name,stability_score,created_at" \
    -H "apikey: $SUPABASE_SERVICE_ROLE_KEY" \
    -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); [print(f\"  🌐 {n['name']} ({n['stability_score']})\") for n in d]" 2>/dev/null \
    || echo "  ⚠️ Could not query seal nodes"
fi
```

**Gate verdict:**
- ✅ All session modules have sealed BoK → proceed to Phase 7 push.
- ⚠️ Module work without BoK (e.g. `feat:` commit creating new page/edge fn without `docs/bok/<slug>/`)
  → 🔴 **BLOCK seal**. Run `/bok-scribe <module>` first OR add module to exemption list (typo/dep bump/single-file patch).

Report BoK status in final seal output (Phase 8).

---

## PHASE 7 — PUSH

```bash
git push origin main
```

Report: branch, number of commits pushed, remote URL.

If push fails (non-fast-forward): run `git pull --rebase origin main` first, then push again. Never force-push main.

---

## PHASE 7b — SPRINT & CONNECTIONS HYGIENE

### Sprint priorities update

Review `.claude/context/sprint-priorities.md` and update:
1. Check off completed items in "Skills a criar ou evoluir" and "Conexões a implementar"
2. Add new gaps discovered this session under "Top 3 Gap Closures" if applicable
3. Update the 4Cs Audit Snapshot scores if `/audit` was run this session
4. Append to the Retrospective section if this was the last session of the sprint

Commit if changed:
```
chore(sprint): update sprint-priorities — <one-line progress note>
```

### Scratch cleanup

```bash
ls scratch/ 2>/dev/null
```

If `scratch/` has `.ts` diagnostic scripts, move them to `.claude/scripts/db/`:
```bash
mkdir -p .claude/scripts/db
mv scratch/*.ts .claude/scripts/db/ 2>/dev/null && echo "Moved ✅" || echo "Nothing to move"
```

Commit if files were moved:
```
chore(scripts): migrate scratch diagnostics to .claude/scripts/db/
```

### MCP documentation check

```bash
cat .mcp.json
```

For each MCP server listed, verify it has an entry in `.claude/references/` or is documented in CLAUDE.md. If a new MCP was added this session and has no documentation, add a one-liner to the relevant reference file.

---

## PHASE 8 — FINAL REPORT

Print seal summary in **Portuguese (Brasil)**:

```
═══════════════════════════════════════════════════════════
  HANDOFF SEALED — <PHASE NAME> (<date>)
═══════════════════════════════════════════════════════════

🔐 SEGURANÇA
  <security check results — each as ✅ / ⚠️ / 🔴>

📦 COMMITS (<N> total)
  <hash> — <message>
  ...

⬡ KNOWLEDGE MESH
  Milestone node: <node id> — <name>
  Embedding: ✅ / ⚠️

📖 README.md
  Versão: <old> → <new>
  Badge neural_mesh: <old> → <new> nós
  Seção adicionada: <section name>

🧠 HANDOFF.md
  Fase selada: <phase name>
  Seções atualizadas: Task State, Record, Pending Actions, GraphRAG State

📋 PROVA MATERIAL (Fase 5c)
  Veredito: <SEAL ALLOWED / SEAL BLOCKED>
  Claims: <N> verificadas · <M> skipped · <K> falhas

🚀 PUSH
  Branch: main → origin/main
  Commits enviados: <N>

📌 SPRINT
  sprint-priorities.md: <atualizado ✅ / sem mudanças>
  scratch/ cleanup: <arquivos movidos ✅ / limpo ✅>
  MCP docs: <ok ✅ / pendência: X>

⏭  PRÓXIMOS PASSOS
  1. <top pending action>
  2. <second pending action>
  3. <third pending action>

═══════════════════════════════════════════════════════════
  Assinado: Claude Code — Braço de Engenharia do AIOS
═══════════════════════════════════════════════════════════
```

**Invariants — never skip:**
- Security audit must run and report before any commit (Phase 1)
- **Phase 3 (milestone node) must run BEFORE Phase 4 (README badge query)** — ensures count includes the handoff node
- **Phase 5b secret scan must run on HANDOFF.md before its commit** — no exceptions
- **Phase 5c material proof audit must run and return `SEAL ALLOWED` before push** — a contradicted claim blocks the seal
- **Documentation must NEVER contain actual credential values** — only describe where they live
- README.md badge counts must reflect real DB state (query live, after milestone insert)
- HANDOFF.md must be updated even if nothing changed (session note)
- Push must happen — remote must always mirror local main
- Knowledge Mesh milestone must be attempted (failures are logged, not blocking)
- git pre-commit hook (`.git/hooks/pre-commit`) is the last barrier — do not bypass with `--no-verify`


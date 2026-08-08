# CLAUDE.md — Obsidian Sessions Agent Guidelines

You are working in the **AI Sessions** workspace (`c:\Users\gabri\Documents\dev\MCORCH_CLAUDE\AI Sessions`), which is an Obsidian Vault containing transcripts and logs of AI pair programming sessions.

Follow these strict rules for syntax, properties, organization, and semantic link building. Refer to the reference documents under `.agents/obsidian_docs/` for specific specifications.

---

## 🛠️ Build and Test Commands
Since this is an Obsidian Vault:
*   There are no traditional compiler/build tools.
*   "Validation" means parsing YAML frontmatter of any edited notes to verify they conform to the YAML specification and that all internal `[[wikilinks]]` target actual or intended files.
*   To test if formatting is correct, verify that no Markdown tags or markdown-style links `[Text](Note.md)` are used for internal files.

---

## 🔗 Obsidian Linking Protocol
Your primary task when writing or editing notes is to construct a **rich, clean, and connected knowledge graph**.
1.  **Prefer Wikilinks**: Always use `[[Note Name]]` for notes inside this vault. Never use standard Markdown links `[Text](path/to/Note.md)` for internal vault files.
2.  **Display Aliases**: Use `[[Note Name|Display Text]]` to integrate links seamlessly into normal prose sentences.
3.  **Semantic Link Scanning**: When creating or updating a note:
    *   Scan the text for concepts or keywords that exist as other notes in [ClaudeSessions](file:///c:/Users/gabri/Documents/dev/MCORCH_CLAUDE/AI%20Sessions/ClaudeSessions) or [GeminiSessions](file:///c:/Users/gabri/Documents/dev/MCORCH_CLAUDE/AI%20Sessions/GeminiSessions).
    *   Link to those existing notes immediately.
    *   If you refer to a specific discussion topic or action item inside another note, link to its section: `[[Note Name#Specific Header]]` or block: `[[Note Name#^block-id]]`.
4.  **Avoid Orphan Notes**: Never leave a newly created note disconnected. Link it from at least one parent note, session MOC, or log list.

---

## 📝 Properties (Frontmatter) Schema
Every session note must begin with a valid YAML frontmatter block containing consistent properties. Keep property keys lowercase:

```yaml
---
type: session
date: YYYY-MM-DD
tags:
  - feat/some-feature
  - bug/some-bug
  - infra/supabase
session_id: uuid-or-hash
status: success
summary: "A brief one-sentence description of the session's core achievement."
---
```

### Allowed Property Fields:
*   `type`: (Text) Always `session` for conversation logs.
*   `date`: (Date) The date of the session in `YYYY-MM-DD` format.
*   `tags`: (List) Hierarchical tags categorizing the topics. Format as `category/sub-category` (e.g., `feat/jwt-bridge`, `bug/token-leak`, `infra/supabase`).
*   `session_id`: (Text) The conversation UUID or agent run ID.
*   `status`: (Text) One of: `success`, `failure`, `in-progress`.
*   `summary`: (Text) A concise description of the changes or fixes made.

---

## 🗺️ Maps of Content (MOC) and Index Updates
We maintain structural index files (Maps of Content or MOCs) to categorize sessions by topic.
1.  When creating a session log that touches a key component (e.g., Supabase, JWT Bridge, Watchdogs, TTS), search the vault for a corresponding MOC file (e.g., `Supabase MOC.md`).
2.  Add a link to the new session under the appropriate date or category header in that MOC.
3.  If no MOC exists for a rapidly expanding topic, create one in the root of the vault (e.g. `Auth MOC.md`) and link the relevant sessions.

---

## 🎨 Spatial Canvas Rules
When requested to create or modify a `.canvas` file:
*   Always load and calculate node coordinates programmatically to ensure elements do not overlap.
*   Maintain a grid spacing of 50px to 100px between nodes.
*   Use edges with directional side anchors (`fromSide`/`toSide`) to represent progression or flow.
*   Color code nodes according to their state (e.g. green for success, yellow for planning, red for errors).

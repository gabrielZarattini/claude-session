# Obsidian MOCs and Knowledge Graph Reference Guide

Obsidian works best when notes are not just stored in a folder structure, but connected in a logical **Knowledge Graph**. This document provides guidelines for organizing notes using Maps of Content (MOCs) and hierarchical tagging.

---

## 1. Map of Content (MOC) Pattern
A Map of Content (MOC) is a specialized hub note that links to and organizes related notes on a specific topic. It acts as a curated entry point to your knowledge graph.

### Suggested MOC Layout:
```markdown
---
type: MOC
tags:
  - hub/mcorch
  - index
---

# MCORCH & Constellation Orchestra MOC

This map organizes all sessions, specifications, and issues related to the MCORCH agent orchestration system.

## 🌟 Core Architecture
*   [[Core V2 Architecture Specification]] - Core agent execution model.
*   [[AIOS Constelação MCORCH system updates]] - System prompt and routing updates.

## 📅 Session Logs
### May 2026
*   [[2026-05-30 - Fix API key leak and reconfigure model defaults]] - Resolved security leak and reset defaults.
*   [[2026-05-28 - Update context and continue antigravity handoff]] - Handoff process description.
*   [[2026-05-27 - Plan JWT refactor and affiliate token migration]] - JWT authentication refactor plan.

### April 2026
*   [[2026-04-26 - Fix layout issues and synchronize mesh node data]] - Mesh node rendering fixes.
```

---

## 2. Link-Building Heuristics (Connection Rules)
To maintain a high-quality graph, any agent modifying notes in this vault should follow these principles:

1.  **No Orphan Notes**: Every newly created session log or document must link back to at least one MOC or index page.
2.  **Explicit Cross-Referencing**: If Session B builds directly upon a solution implemented in Session A, Session B's notes must explicitly link to Session A in its context or frontmatter:
    *   *Example*: `This work continues the JWT authentication bridge started in [[2026-05-17 - Complete aios-sql-bridge with JWT validation]].`
3.  **Red Links (Placeholders)**: If you mention a related concept that has no dedicated note yet but is highly relevant, write it as a wikilink `[[New Note Title]]` to create a placeholder. This registers the node on the graph, allowing it to be easily populated later.

---

## 3. Hierarchical Tag Hierarchy
Tags should be categorized using hierarchical (nested) structures rather than flat tags. This avoids tag pollution and groups related items.

### Recommended Hierarchy:
*   `#feat/` - Feature development (e.g. `#feat/jwt-auth`, `#feat/tts-voice`).
*   `#bug/` - Bug fixing (e.g. `#bug/token-limit`, `#bug/canvas-render`).
*   `#infra/` - Server, databases, cron, and APIs (e.g. `#infra/supabase`, `#infra/docker`, `#infra/cron`).
*   `#audit/` - Security reviews, code audits, compliance (e.g. `#audit/security`, `#audit/lgpd`).
*   `#hub/` - MOCs and index entry points (e.g. `#hub/sessions`, `#hub/constellation`).

---

## 4. Maintenance Protocol
Whenever the agent creates a note:
1.  Verify the note has a `type` property in the frontmatter.
2.  Check for existing MOCs matching the note's tags.
3.  Update those MOCs by inserting a bullet point with a link to the new note under the relevant date or section.

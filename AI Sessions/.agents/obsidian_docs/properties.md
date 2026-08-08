# Obsidian Properties (Frontmatter) Reference Guide

Properties allow you to store structured metadata (YAML) at the very top of a note. Obsidian reads and index these properties for search, graph styling, and plugins (e.g., Dataview).

---

## 1. Frontmatter Syntax
The frontmatter block must start on the **very first line** of the file and be enclosed by three dashes `---`.

```yaml
---
title: "Fix OpenRouter multimodal error"
date: 2026-05-26
tags:
  - bug/api-limits
  - provider/openrouter
aliases:
  - "OpenRouter API limits fix"
cssclasses:
  - wide-layout
completed: true
---
```

### Critical YAML Syntax Rules:
1.  **Colon Spacing**: Keys must be followed by a colon and a space (e.g. `key: value`, not `key:value`).
2.  **String Quotes**: If a string contains special YAML characters like colons `:`, brackets `[]`, braces `{}`, or quotes `"`, wrap the string in double quotes:
    *   *Incorrect*: `summary: Fix: Authentication error`
    *   *Correct*: `summary: "Fix: Authentication error"`
3.  **List Syntax**: Lists can be formatted using YAML array style or inline brackets:
    ```yaml
    tags:
      - tag1
      - tag2
    # OR
    tags: [tag1, tag2]
    ```

---

## 2. Supported Property Types in Obsidian

| Type | YAML Format | Description |
|---|---|---|
| **Text** | `summary: "Short description"` | Standard single-line or multi-line string. |
| **List** | `aliases: [Alias1, Alias2]` | An array of strings. |
| **Number** | `tokens: 154000` | Integer or floating point number. |
| **Checkbox** | `active: true` | Boolean value (`true` or `false`). |
| **Date** | `date: 2026-05-30` | Date string in ISO format `YYYY-MM-DD`. |
| **Date & Time** | `due: 2026-05-30T14:30:00` | ISO date-time string `YYYY-MM-DDTHH:MM:SS`. |

---

## 3. Obsidian Built-in Properties
These properties have built-in behaviors inside the Obsidian application:
*   `tags`: Automatically registers tags inside the tags database (identical to writing inline `#tags`). Enables autocomplete and shows up in the tag pane and search.
*   `aliases`: Alternative names for the note. If you link to an alias (e.g. `[[Alternative Name]]`), it will resolve to the original file.
*   `cssclasses`: Applies specific CSS classes to the note container, allowing custom styling of that specific note using your vault's theme.

---

## 4. Hierarchy and Tag Formats
*   **Case Sensitivity**: Tags in Obsidian are case-insensitive, but casing is preserved for display.
*   **Characters**: Tags can contain letters, numbers, underscores `_`, hyphens `-`, and forward slashes `/`. They cannot start with a number.
*   **Hierarchical (Nested) Tags**: Use slashes `/` to group related categories:
    ```yaml
    tags:
      - feat/voice-bridge   # Nested tag: parent is 'feat', child is 'voice-bridge'
      - bug/auth/jwt        # Multi-nested tag
    ```
    This creates a collapsible tag tree in Obsidian's Tag Pane, helping to keep notes organized.

# Obsidian Linking Reference Guide

This document defines the official syntax and best practices for creating links and connections inside an Obsidian Vault.

---

## 1. Internal Links (Wikilinks)
Obsidian uses `[[Wikilinks]]` for internal connections. By default, Obsidian resolves notes by their **filename** without requiring their relative paths.

### Standard Wikilink
```markdown
[[2026-05-30 - Fix API key leak and reconfigure model defaults]]
```
*   **Best Practice**: Do not include `.md` in internal note names.
*   **Collision Handling**: If two files have the same name in different folders, Obsidian will automatically add the minimal path required to distinguish them: `[[Folder A/Note Name]]` and `[[Folder B/Note Name]]`.

### Links with Custom Display Text (Aliases)
To make links blend naturally into writing, use a pipe `|` character:
```markdown
We resolved this in the [[2026-05-30 - Fix API key leak and reconfigure model defaults|API key leak fix session]].
```

---

## 2. Linking to Specific Targets (Headings and Blocks)

### Linking to a Section Heading
You can link directly to any header in a note using the hash `#` symbol:
```markdown
See the details on the [[2026-05-18 - Admin JWT validation and system health verification#JWT Validation Schema|validation schema]].
```
*   Obsidian matches headings case-insensitively.

### Linking to a Specific Block (Paragraph, Item, Quote)
You can link to any specific text block (such as a paragraph, list item, or blockquote) by defining a **Block ID** at the end of that block.
1.  **Define the block** by appending a space and `^your-unique-id` at the end of the block:
    ```markdown
    The user was authenticated successfully using the temporary OAuth bypass script. ^auth-bypass-event
    ```
2.  **Link to the block** from another note:
    ```markdown
    The bypass occurred during the previous sprint (see [[2026-05-16 - Execute OpenClaw Soberania Total#^auth-bypass-event]]).
    ```

*   **Block ID Syntax**: Block IDs can contain alphanumeric characters and hyphens.
*   **Lists and Quotes**: For lists, bullet points, or blockquotes, place the block ID on a new line immediately following the block:
    ```markdown
    > This is a quote.
    
    ^quote-block-id
    ```

---

## 3. Embedding Media and Attachments
Prefix a wikilink with an exclamation mark `!` to embed the file content directly inside the note (transclusion).

### Note Embeds
Embed a section or an entire note inline:
```markdown
![[2026-05-30 - Fix API key leak and reconfigure model defaults#What was tested]]
```

### Image and PDF Embeds
```markdown
![[architecture-diagram.png]]
![[architecture-diagram.png|300]]  <!-- Specifies width in pixels -->
![[specification.pdf#page=4]]      <!-- Embeds a specific page of a PDF -->
```

---

## 4. External Links
For any links pointing outside the Obsidian vault (e.g., GitHub, websites), use the standard Markdown link syntax:
```markdown
Refer to the [GitHub Issue #451](https://github.com/gabrielZarattini/claude-session/issues/451) for the log.
```
*   **Rule**: Never use wikilinks `[[https://github.com...]]` for external URLs.

# Obsidian Callouts Reference Guide

Callouts are visual blocks that draw attention to key details, examples, warnings, or tips. They use the blockquote syntax `>` combined with a specific identifier `[!type]`.

---

## 1. Standard Syntax
To create a callout, start the first line with `> [!type]` followed by an optional custom title. Every line of the callout content must begin with the blockquote character `>`.

```markdown
> [!info] Session Details
> This session focused on refactoring the Supabase integrations.
> It was executed on the secondary staging server.
```

### Formatting Rules:
*   **Space**: There must be a space between `> [!type]` and the title/content.
*   **Empty Lines**: To add a blank line inside a callout, you must include the `>` on that line:
    ```markdown
    > [!tip] Title
    > Line one
    >
    > Line two after an empty line.
    ```

---

## 2. Foldable Callouts (Collapsible)
You can make a callout foldable (expanded or collapsed by default) by appending a plus `+` or minus `-` sign immediately after the type bracket (no space).

### Collapse by Default (`-`)
The callout will render closed, requiring the user to click to expand it:
```markdown
> [!faq]- Click here to see the prompt log
> This contains the raw prompt string sent to the LLM api...
```

### Expand by Default (`+`)
The callout will render open but can be collapsed manually:
```markdown
> [!example]+ Code Snippet
> ```javascript
> console.log("Visible by default");
> ```
```

---

## 3. Supported Callout Types
Obsidian includes a rich set of built-in callout types, each with its own color and icon.

| Type Key | Alternative Aliases | Visual Color |
|---|---|---|
| `[!note]` | None | Blue |
| `[!info]` | None | Blue |
| `[!todo]` | None | Blue |
| `[!tip]` | `[!hint]`, `[!important]` | Green/Cyan |
| `[!success]` | `[!check]`, `[!done]` | Green |
| `[!question]` | `[!help]`, `[!faq]` | Yellow/Orange |
| `[!warning]` | `[!caution]`, `[!attention]` | Yellow/Orange |
| `[!failure]` | `[!fail]`, `[!missing]` | Red |
| `[!danger]` | `[!error]` | Red |
| `[!bug]` | None | Red |
| `[!example]` | None | Purple |
| `[!quote]` | `[!cite]` | Grey |

---

## 4. Nesting Callouts
Callouts can be nested inside list items or other callouts by adding additional indentation and blockquote prefixes:

```markdown
> [!info] Parent Callout
> This is part of the parent callout content.
>
> > [!warning] Nested Callout
> > This is a warning callout nested *inside* the info callout.
```
*   *Note*: Ensure that nested callouts have the double blockquote character `> >` at the beginning of each line.

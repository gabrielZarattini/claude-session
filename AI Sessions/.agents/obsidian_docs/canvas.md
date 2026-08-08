# Obsidian Canvas Reference Guide

Obsidian Canvas (`.canvas`) is an open spatial canvas format for visual notes, mind maps, and workflow diagrams. It is written as a JSON file consisting of `nodes` and `edges`.

---

## 1. Top-Level Structure
A canvas file is a single JSON object:
```json
{
  "nodes": [],
  "edges": []
}
```

---

## 2. Nodes Array
Nodes are visual cards placed on the canvas. The order in the array determines the z-index (elements later in the array render on top).

### Generic Node Attributes:
Every node object must have these basic coordinates and size values:
*   `id`: (string) A unique 16-character hexadecimal identifier (e.g., `"a47f02d5cee4eec3"`).
*   `x`: (integer) X-coordinate on the infinite grid.
*   `y`: (integer) Y-coordinate on the infinite grid.
*   `width`: (integer) Width of the card in pixels.
*   `height`: (integer) Height of the card in pixels.
*   `color`: (string, optional) Preset color code (`"1"` to `"6"`) or a custom hex color code (e.g. `"#ff0000"`).

### Node Types:

#### A. Text Node
Contains written text that supports Markdown.
```json
{
  "id": "node_text_001",
  "type": "text",
  "text": "### Session MOC\nThis is a *markdown* formatted description inside a text node card.",
  "x": 100,
  "y": 100,
  "width": 300,
  "height": 200
}
```

#### B. File Node
Embeds an existing note or file from the vault.
```json
{
  "id": "node_file_001",
  "type": "file",
  "file": "ClaudeSessions/2026-05-28 - Update context and continue antigravity handoff.md",
  "x": 450,
  "y": 100,
  "width": 400,
  "height": 500
}
```
*   `file`: The full relative path to the note or asset from the vault root.

#### C. Link Node (URL)
Embeds an external website or web page.
```json
{
  "id": "node_link_001",
  "type": "link",
  "url": "https://github.com/gabrielZarattini/claude-session",
  "x": 900,
  "y": 100,
  "width": 400,
  "height": 400
}
```

#### D. Group Node
A background container card used to visually group multiple nodes together.
```json
{
  "id": "group_001",
  "type": "group",
  "label": "Sprint 4 - Core V2 Fixes",
  "x": 50,
  "y": 50,
  "width": 850,
  "height": 600,
  "color": "2"
}
```
*   *Note*: Coordinates of cards inside a group are absolute (relative to the grid origin, not relative to the group).

---

## 3. Edges Array
Edges represent arrows and connections between nodes.

### Edge Attributes:
*   `id`: (string) Unique identifier for the connection line.
*   `fromNode`: (string) The `id` of the source node.
*   `fromSide`: (string, optional) Connection anchor side on the source node: `"top"`, `"right"`, `"bottom"`, or `"left"`.
*   `toNode`: (string) The `id` of the target node.
*   `toSide`: (string, optional) Connection anchor side on the target node: `"top"`, `"right"`, `"bottom"`, or `"left"`.
*   `color`: (string, optional) Preset color code (`"1"` to `"6"`) or a custom hex code.
*   `label`: (string, optional) Inline text to display along the connection line.

### Example Edge Object:
```json
{
  "id": "edge_001",
  "fromNode": "node_file_001",
  "fromSide": "right",
  "toNode": "node_link_001",
  "toSide": "left",
  "color": "4",
  "label": "pushes to"
}
```

---

## 4. Preset Colors List
Standard numeric preset mappings inside Obsidian Canvas:
*   `"1"`: Red
*   `"2"`: Orange
*   `"3"`: Yellow
*   `"4"`: Green
*   `"5"`: Cyan
*   `"6"`: Purple

---

## 5. Spatial Layout and Positioning Rules
To keep canvases clean, readable, and structured, the agent must compute node positions using programmatic algorithms:
1.  **Prevent Overlapping**: Always leave at least `50px` to `100px` of horizontal or vertical gap between card boundaries.
2.  **Horizontal Flow Layout**: When building a chronological pipeline (like a sequence of debugging sessions), align nodes on the Y-axis and increment the X-coordinate:
    *   $x_{n+1} = x_n + width_n + spacing$
    *   $y_{n+1} = y_n$
3.  **Vertical Stack Layout**: When list logging sub-tasks or sub-agents:
    *   $x_{n+1} = x_n$
    *   $y_{n+1} = y_n + height_n + spacing$

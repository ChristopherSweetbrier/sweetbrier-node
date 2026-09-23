# Sweetbrier VS Code Extension Architecture
**The "Digital Quipu" Integration**

This document outlines the architecture for turning VS Code and Mermaid.js into a live IDE for deterministic AI constraint mapping.

---

## 1. System Topology

The extension operates across two distinct layers: the **VS Code Client** (TypeScript/Node.js) handling the user interface, and the **Sweetbrier Language Server** (Python) handling the mathematical DAG evaluation.

```mermaid
graph TD;
    subgraph VS Code Extension (TypeScript)
        A[Text Editor .md / .mmd] -->|OnSave / OnType| B(Extension Core);
        B -->|Diagnostic Highlighting| A;
        B -->|Sends Mermaid String| C{Inter-Process Bridge};
    end
    subgraph Sweetbrier Core (Python)
        C -->|JSON Payload| D[mermaid_compiler.py];
        D -->|NetworkX DAG| E[sweetbrier_engine.py];
        E -->|Validation Verdict| C;
    end
```

## 2. Core Components

### A. The Language Server Bridge (IPC)
Because VS Code runs on Node.js and the Sweetbrier engine requires Python's `networkx`, we use a lightweight standard input/output bridge (or local FastAPI instance).
1. When a user types a Mermaid flowchart, the extension bundles the text.
2. It sends a request to the Python backend: `validate(mermaid_string)`.
3. The Python backend returns a JSON payload detailing Node/Edge validity.

### B. VS Code Diagnostics (The "Linter")
Instead of linting for syntax errors, we are linting for **causal logic errors**.
* **Red Squiggly Lines:** If `sweetbrier_engine.py` returns a `REJECTED_RUPTURE` (e.g., a paradox or cycle), the extension maps the failing nodes back to the exact line in the editor and underlines it in red.
* **Hover Text:** Hovering over the red line displays the Sweetbrier Engine output: *"Collision Detected: Proposed higher-order principle lacks historical provenance."*

### C. CodeLens & Live Compilation
In `.md` files, VS Code will inject a "CodeLens" button directly above any ` ```mermaid ` code block.
* `▶ Run Sweetbrier Validation`
* Clicking this button executes the compilation and provides immediate visual feedback.

## 3. Implementation Steps (Tonight's Sprint)

To get this working as a proof-of-concept for your GitHub and Dr. Johnson Li:

1. **The Python CLI Wrapper:** 
   Update `mermaid_demo.py` to accept raw strings via `sys.stdin` and output *pure JSON*. This makes it instantly consumable by Node.js.
2. **The VS Code Scaffolding:** 
   Run `yo code` to generate a boilerplate VS Code extension.
3. **The Child Process Call:** 
   Write the TypeScript logic that calls `python sweetbrier_cli.py`, reads the JSON stdout, and maps it to the `vscode.Diagnostic` API.

## 4. Why this matters for the Pitch
By showing this to your boss or Big Tech:
1. You aren't just pitching an "idea." You are pitching an **integrated developer environment**.
2. You demonstrate that Sweetbrier is language/platform agnostic. The engine sits underneath standard enterprise tools (VS Code + Markdown).
3. It visualizes the abstract math. People don't understand DAGs, but they *do* understand a red squiggly line under a bad idea.

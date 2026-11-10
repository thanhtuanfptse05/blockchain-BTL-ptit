---
name: codegraph
description: "Pre-indexed semantic code intelligence graph. Use for exploring architecture, tracing cross-file call graphs, finding symbol callers/callees, calculating change impact/blast radius, and identifying affected tests across 20+ languages."
---

# CodeGraph: Semantic Code Intelligence

CodeGraph provides pre-indexed knowledge graphs of codebases using a compiled Rust tree-sitter engine, storing symbols, edges, calls, definitions, and framework routes in a local SQLite database (`.codegraph/codegraph.db`).

## When to Use

Reach for CodeGraph **before** using slow `grep`, `glob`, or sequential file-reading loops whenever:
1. You need to understand repository architecture or how a specific flow/subsystem works.
2. Tracing call paths from entry points to core logic (including dynamic dispatch, callbacks, and framework routing).
3. Analyzing the impact or blast radius of modifying a function, class, or interface.
4. Finding test files affected by code changes before running test suites.
5. Searching for symbols across multi-language projects.

---

## 1. Primary MCP Tool: `codegraph_explore`

When connected via MCP (`codegraph serve --mcp`), CodeGraph exposes the unified `codegraph_explore` tool:
- Returns verbatim code of relevant symbols grouped by file.
- Traces call paths (including dynamic dispatch hops like React props, callbacks, and interfaces).
- Summarizes the blast radius of potential changes.
- Name a specific file or symbol in the query to get line-numbered source.

---

## 2. CLI Commands Reference

You can also run CodeGraph directly from the terminal via `codegraph`:

### Exploration & Architecture
```bash
# Explore a query (returns source snippets, call paths, blast radius in one shot)
codegraph explore "<symbol or question>"

# View single symbol details or read a file with line numbers
codegraph node <symbol|file>

# Search symbols across the codebase (FTS5)
codegraph query <search_term>
```

### Dependency & Call Graph Analysis
```bash
# Find all functions/methods calling a symbol
codegraph callers <symbol>

# Find all functions/methods called by a symbol
codegraph callees <symbol>

# Analyze the multi-lateral blast radius / impact of modifying a symbol
codegraph impact <symbol> --depth 3

# List implementations of an interface or subclasses of a class
codegraph implementations <symbol>

# Detect circular imports
codegraph cycles
```

### Test Impact Analysis (`affected`)
```bash
# Identify test files affected by modified source files
codegraph affected src/utils.ts src/api.ts

# Run with git diff to only test what changed
git diff --name-only | codegraph affected --stdin
```

### Project Lifecycle & Synchronization
```bash
# Initialize a project and build the index (.codegraph/)
codegraph init

# Check index statistics, pending file syncs, and database health
codegraph status

# Incrementally sync recent changes (auto-sync usually handles this in MCP)
codegraph sync

# Force a full re-index
codegraph index --force
```


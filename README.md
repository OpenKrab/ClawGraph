# 🦞 ClawGraph

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

> Interactive Knowledge Graph for ClawMemory with natural language queries

[English](README.md) | [ไทย](README-th.md)

**ClawGraph** solves the classic memory system pain point: **"I remember it but can't find it"**

It transforms **ClawMemory** into an **interactive Knowledge Graph** showing relationships between data (project ↔ deadline ↔ client ↔ task ↔ expense from ClawReceipt etc.) + **natural language queries** (e.g. "Which projects have deadlines this month with Thai clients?")

Automatically builds on ClawSelfImprove (the graph gets smarter with every feedback)

## Table of Contents

- [Features](#features)
- [Demo](#demo)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Local Graph Database**: Built on ClawMemory (SQLite + vector embeddings)
- **Interactive Visualization**: Node-edge graph with zoom, drag, click functionality
- **Natural Language Queries**: Automatic translation of Thai/English queries to graph queries
- **Self-Improving**: Learns from user feedback patterns via ClawSelfImprove integration
- **Privacy First**: 100% local execution, zero cost, no data leaves your machine

## Demo

![ClawGraph Demo](demo.gif)

*Type Thai query → Instant interactive graph with highlighted relationship paths*

## How It Works

### 1. Capture Relationships (from ClawMemory)
- Every event (task, receipt, reminder) → Automatically create nodes + edges
- Example: "Project X" → "deadline March 15" → "client ABC" → "expense 4,200 THB"

### 2. Build Graph
- Uses NetworkX + optional local Neo4j (or SQLite with recursive CTE)
- Vector embeddings from ClawMemory connect semantic edges (e.g. "similar to previous project")

### 3. Natural Language Query
- Type: "Summarize projects nearing deadline related to Thai clients"
- LLM translates → Graph query → Retrieve nodes/edges → Display + visual graph

### 4. Visualize
- Interactive graph (zoom, drag, click nodes)
- Highlight paths (e.g. "client → project → expense")
- Export to PNG or Mermaid code

### 5. Self-Improve Loop
- Tell it "This is important" or "This is irrelevant" → ClawSelfImprove adjusts edge weights
- Next time prioritizes relevant nodes automatically

## Tech Stack (100% Free + Local)

- **Core Graph**: NetworkX (Python) + PyVis (interactive HTML generation)
- **Query Engine**: Llama3/Ollama (natural language → graph query translation)
- **Storage**: Direct integration with ClawMemory (SQLite + Chroma vector DB)
- **Dashboard**: Extends ClawMemory UI (Next.js) or standalone web view
- **Integration**: ClawFlow (install), ClawSelfImprove (feedback learning), ClawReceipt (expense edge pull)

## Installation

1. Install ClawFlow
2. Run `clawflow install openkrab/claw-graph`
3. Configure in ClawMemory dashboard

## Usage

1. **Build Graph**: `python scripts/build_graph.py`
2. **Query**: Enter natural language in the UI
3. **Visualize**: View the interactive graph

## Examples

See [examples/queries-thai.md](examples/queries-thai.md) for sample Thai queries.

## Contributing

Contributions welcome! Please see our [issues](https://github.com/openkrab/claw-graph/issues) for current tasks.

## License

MIT 

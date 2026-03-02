#!/usr/bin/env python3
"""
ClawGraph Query Script
Translates natural language queries to graph queries using Ollama
"""

import sys
import networkx as nx
import ollama
import yaml
from pathlib import Path

def load_config():
    config_path = Path(__file__).parent.parent / 'config.yaml'
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def load_graph(config):
    graph_path = config['database']['graph_db']
    if not Path(graph_path).exists():
        raise FileNotFoundError(f"Graph not found at {graph_path}. Run build_graph.py first.")
    return nx.read_gpickle(graph_path)

def load_prompt():
    prompt_path = Path(__file__).parent.parent / 'templates' / 'graph_prompt.md'
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read()

def query_graph(G, query, config, prompt_template):
    # Replace {query} in prompt
    prompt = prompt_template.replace('{query}', query)

    # Query Ollama
    try:
        response = ollama.chat(
            model=config['ollama']['model'],
            messages=[{'role': 'user', 'content': prompt}]
        )
        code = response['message']['content'].strip()

        # Clean up the code (remove markdown if present)
        if code.startswith('```python'):
            code = code[9:]
        if code.endswith('```'):
            code = code[:-3]
        code = code.strip()

        print(f"Generated query code:\n{code}\n")

        # Execute the code in a restricted environment
        # Note: This is a security risk in production, but for MVP it's acceptable
        local_vars = {'G': G, 'result': None}
        global_vars = {
            'nx': nx,
            'datetime': __import__('datetime'),
            '__builtins__': __builtins__
        }

        exec(code, global_vars, local_vars)
        result = local_vars.get('result')

        return result

    except Exception as e:
        print(f"Error querying graph: {e}")
        return None

def format_result(result):
    if result is None:
        return "No results found"

    if isinstance(result, list):
        if not result:
            return "No results found"
        # Format list of nodes
        formatted = []
        for item in result[:10]:  # Limit to 10 results
            if isinstance(item, str) and item in G.nodes:
                node_data = G.nodes[item]
                formatted.append(f"- {item}: {node_data.get('name', item)} ({node_data.get('type', 'unknown')})")
            else:
                formatted.append(f"- {item}")
        if len(result) > 10:
            formatted.append(f"... and {len(result) - 10} more")
        return "\n".join(formatted)

    elif isinstance(result, dict):
        return "\n".join(f"{k}: {v}" for k, v in result.items())

    else:
        return str(result)

def main():
    if len(sys.argv) < 2:
        print("Usage: python query_graph.py 'natural language query'")
        return 1

    query = sys.argv[1]

    try:
        config = load_config()
        G = load_graph(config)
        prompt_template = load_prompt()

        result = query_graph(G, query, config, prompt_template)

        print("Query:", query)
        print("Result:")
        print(format_result(result))

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0

if __name__ == '__main__':
    exit(main())

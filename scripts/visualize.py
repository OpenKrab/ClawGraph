#!/usr/bin/env python3
"""
ClawGraph Visualize Script
Creates interactive HTML visualization of the knowledge graph
"""

import networkx as nx
import yaml
from pyvis.network import Network
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

def create_visualization(G, config):
    # Create PyVis network
    net = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="#000000")

    # Configure physics
    net.set_options("""
    {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08
        },
        "maxVelocity": 50,
        "solver": "forceAtlas2Based",
        "timestep": 0.35,
        "stabilization": {
          "enabled": true,
          "iterations": 1000
        }
      }
    }
    """)

    # Color mapping for node types
    color_map = {
        'project': '#FF6B6B',
        'client': '#4ECDC4',
        'task': '#45B7D1',
        'expense': '#FFA07A',
        'deadline': '#98D8C8',
        'reminder': '#F7DC6F'
    }

    # Add nodes
    for node_id, node_data in G.nodes(data=True):
        node_type = node_data.get('type', 'unknown')
        color = color_map.get(node_type, '#CCCCCC')

        # Create label
        name = node_data.get('name', node_data.get('text', str(node_id)))
        if len(name) > 20:
            name = name[:17] + "..."

        # Size based on type or connections
        size = 20
        if node_type == 'project':
            size = 25
        elif node_type == 'client':
            size = 25

        net.add_node(
            node_id,
            label=name,
            color=color,
            size=size,
            title=f"Type: {node_type}\n{chr(10).join(f'{k}: {v}' for k, v in node_data.items() if k not in ['type', 'name', 'text'])}"
        )

    # Add edges
    for source, target, edge_data in G.edges(data=True):
        relation = edge_data.get('relation', 'related')
        weight = edge_data.get('weight', 1.0)

        # Edge color based on relation
        edge_color = '#666666'
        if relation == 'belongs_to_client':
            edge_color = '#4ECDC4'
        elif relation == 'has_deadline':
            edge_color = '#FF6B6B'
        elif relation == 'has_task':
            edge_color = '#45B7D1'
        elif relation == 'has_expense':
            edge_color = '#FFA07A'

        net.add_edge(
            source,
            target,
            color=edge_color,
            width=max(1, weight * 3),
            title=f"Relation: {relation}\nWeight: {weight}"
        )

    return net

def main():
    try:
        config = load_config()
        G = load_graph(config)

        print(f"Loaded graph with {len(G.nodes)} nodes and {len(G.edges)} edges")

        net = create_visualization(G, config)

        # Save HTML
        output_path = "graph_visualization.html"
        net.save_graph(output_path)

        print(f"Visualization saved to {output_path}")
        print("Open the HTML file in a web browser to view the interactive graph")

    except Exception as e:
        print(f"Error creating visualization: {e}")
        return 1

    return 0

if __name__ == '__main__':
    exit(main())

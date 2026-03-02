#!/usr/bin/env python3
"""
ClawGraph Build Script
Builds the knowledge graph from ClawMemory data
"""

import sqlite3
import networkx as nx
import yaml
import os
from pathlib import Path

def load_config():
    config_path = Path(__file__).parent.parent / 'config.yaml'
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def connect_db(db_path):
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"ClawMemory database not found at {db_path}")
    return sqlite3.connect(db_path)

def build_graph(db_conn, config):
    G = nx.Graph()

    # Query projects
    projects = db_conn.execute('''
        SELECT id, name, deadline, client_id
        FROM projects
        WHERE name IS NOT NULL
    ''').fetchall()

    # Query clients
    clients = db_conn.execute('''
        SELECT id, name
        FROM clients
        WHERE name IS NOT NULL
    ''').fetchall()

    # Query tasks
    tasks = db_conn.execute('''
        SELECT id, name, project_id
        FROM tasks
        WHERE name IS NOT NULL
    ''').fetchall()

    # Query expenses
    expenses = db_conn.execute('''
        SELECT id, amount, description, project_id, client_id
        FROM expenses
        WHERE amount > 0
    ''').fetchall()

    # Query reminders
    reminders = db_conn.execute('''
        SELECT id, text, date
        FROM reminders
        WHERE text IS NOT NULL
    ''').fetchall()

    # Create nodes
    for proj in projects:
        proj_id, name, deadline, client_id = proj
        node_id = f"project_{proj_id}"
        G.add_node(node_id,
                  type='project',
                  name=name,
                  deadline=deadline,
                  client_id=client_id)

        # Add deadline node
        if deadline:
            deadline_node = f"deadline_{proj_id}"
            G.add_node(deadline_node,
                      type='deadline',
                      date=deadline)
            G.add_edge(node_id, deadline_node,
                      relation='has_deadline',
                      weight=config['edge_types']['has_deadline']['weight'])

    for client in clients:
        client_id, name = client
        node_id = f"client_{client_id}"
        G.add_node(node_id,
                  type='client',
                  name=name)

    for task in tasks:
        task_id, name, project_id = task
        node_id = f"task_{task_id}"
        G.add_node(node_id,
                  type='task',
                  name=name,
                  project_id=project_id)

    for expense in expenses:
        exp_id, amount, description, project_id, client_id = expense
        node_id = f"expense_{exp_id}"
        G.add_node(node_id,
                  type='expense',
                  amount=amount,
                  description=description or '',
                  project_id=project_id,
                  client_id=client_id)

    for reminder in reminders:
        rem_id, text, date = reminder
        node_id = f"reminder_{rem_id}"
        G.add_node(node_id,
                  type='reminder',
                  text=text,
                  date=date)

    # Create edges based on relationships
    for proj in projects:
        proj_id, _, _, client_id = proj
        proj_node = f"project_{proj_id}"
        if client_id:
            client_node = f"client_{client_id}"
            if client_node in G:
                G.add_edge(proj_node, client_node,
                          relation='belongs_to_client',
                          weight=config['edge_types']['belongs_to_client']['weight'])

    for task in tasks:
        task_id, _, project_id = task
        task_node = f"task_{task_id}"
        if project_id:
            proj_node = f"project_{project_id}"
            if proj_node in G:
                G.add_edge(proj_node, task_node,
                          relation='has_task',
                          weight=config['edge_types']['has_task']['weight'])

    for expense in expenses:
        exp_id, _, _, project_id, client_id = expense
        exp_node = f"expense_{exp_id}"
        if project_id:
            proj_node = f"project_{project_id}"
            if proj_node in G:
                G.add_edge(proj_node, exp_node,
                          relation='has_expense',
                          weight=config['edge_types']['has_expense']['weight'])
        if client_id:
            client_node = f"client_{client_id}"
            if client_node in G:
                G.add_edge(client_node, exp_node,
                          relation='has_expense',
                          weight=config['edge_types']['has_expense']['weight'])

    # TODO: Add vector similarity edges using Chroma

    return G

def main():
    config = load_config()
    db_path = config['database']['claw_memory_db']

    try:
        conn = connect_db(db_path)
        G = build_graph(conn, config)
        conn.close()

        # Save graph
        graph_path = config['database']['graph_db']
        nx.write_gpickle(G, graph_path)

        print(f"Graph built with {len(G.nodes)} nodes and {len(G.edges)} edges")
        print(f"Saved to {graph_path}")

    except Exception as e:
        print(f"Error building graph: {e}")
        return 1

    return 0

if __name__ == '__main__':
    exit(main())

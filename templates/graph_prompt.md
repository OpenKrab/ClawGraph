Translate the following natural language query to a graph query in NetworkX Python code.

Node types: project, client, task, expense, deadline, reminder
Edge types: has_deadline, belongs_to_client, has_task, has_expense, related_to, precedes

Node attributes:
- project: name, deadline, client_id
- client: name
- task: name, project_id
- expense: amount, description, project_id, client_id
- deadline: date
- reminder: text, date

Edge attributes: relation

The graph G is a NetworkX graph.

Natural Language Query: {query}

Output only the Python code that queries G and assigns the result to a variable 'result'. Do not include imports or execution.

Example:
For query "projects with deadlines this month":
result = [node for node in G.nodes if G.nodes[node].get('type') == 'project' and G.nodes[node].get('deadline_month') == datetime.now().month]

For query "clients with expenses over 10000":
result = [node for node in G.nodes if G.nodes[node].get('type') == 'client' and sum(G.nodes[edge[1]].get('amount', 0) for edge in G.edges(node) if G.edges[edge].get('relation') == 'has_expense') > 10000]

Graph Query (Python code):

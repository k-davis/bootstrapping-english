# Demo: Force-directed graph with networkx and matplotlib (with colors and variable edge weights)

import networkx as nx
import matplotlib.pyplot as plt

# Create a simple graph
G = nx.Graph()
edges = [
    ('Alice', 'Rabbit', 30),
    ('Alice', 'Sister', 20),
    ('Rabbit', 'Watch', 50),
    ('Rabbit', 'Waistcoat', 20),
    ('Sister', 'Book', 40),
    ('Book', 'Pictures', 20),
    ('Book', 'Conversations', 30),
    ('Waistcoat', 'Conversations', 1)
]
G.add_weighted_edges_from(edges)

# Assign colors to nodes
node_colors = []
color_map = {
    'Alice': 'lightcoral',
    'Rabbit': 'gold',
    'Sister': 'lightgreen',
    'Book': 'skyblue',
    'Watch': 'violet',
    'Waistcoat': 'orange',
    'Pictures': 'plum',
    'Conversations': 'lightgray'
}
for node in G.nodes():
    node_colors.append(color_map.get(node, 'gray'))

# Get edge weights for thickness
edge_weights = [G[u][v]['weight'] for u, v in G.edges()]

pos = nx.spring_layout(G, seed=42)

# Draw the graph
plt.figure(figsize=(8, 6))
nx.draw(
    G, pos, with_labels=True,
    node_color=node_colors,
    edge_color='gray',
    width=edge_weights,
    node_size=2000,
    font_size=12
)



import networkx as nx
import matplotlib.pyplot as plt

# ============================================
# Tech-SEDA Dialogic Coding Network
# ============================================

G = nx.DiGraph()

# --------------------------------------------
# Add Tech-SEDA core dialogic codes
# --------------------------------------------

codes = {
    "IB": "Invitation to Build on Ideas",
    "B": "Building on Ideas",
    "CH": "Challenge",
    "IR": "Invitation for Reasoning",
    "R": "Reasoning",
    "IC": "Invitation for Co-ordination",
    "SC": "Simple Co-ordination",
    "RC": "Reasoned Co-ordination",
    "II": "Inquiry Invitation",
    "RB": "Reference Back",
    "RW": "Reference to Wider Context",
    "F": "Focusing",
    "RD": "Reflect on Dialogue/Activity"
}

for code, label in codes.items():
    G.add_node(code, label=label)

# --------------------------------------------
# Add theoretically grounded dialogic relations
# --------------------------------------------

edges = [

    # Building and elaboration
    ("IB", "B", 5),
    ("B", "R", 4),
    ("B", "SC", 3),

    # Challenge and reasoning
    ("CH", "R", 5),
    ("CH", "RC", 4),

    # Reasoning invitations
    ("IR", "R", 5),
    ("IR", "RC", 3),

    # Coordination processes
    ("IC", "SC", 5),
    ("SC", "RC", 4),
    ("R", "RC", 5),

    # Inquiry processes
    ("II", "IR", 4),
    ("II", "CH", 3),
    ("II", "R", 3),

    # Reflection and contextualisation
    ("RB", "B", 3),
    ("RB", "R", 2),

    ("RW", "R", 4),
    ("RW", "RC", 3),

    # Dialogic guidance
    ("F", "IR", 3),
    ("F", "B", 2),

    # Metacognitive reflection
    ("RD", "RC", 4),
    ("RD", "R", 3),
]

for source, target, weight in edges:
    G.add_edge(source, target, weight=weight)

# --------------------------------------------
# Visualisation
# --------------------------------------------

plt.figure(figsize=(16, 12))

pos = nx.spring_layout(
    G,
    seed=42,
    k=1.8
)

# Nodes
nx.draw_networkx_nodes(
    G,
    pos,
    node_size=4000
)

# Labels
nx.draw_networkx_labels(
    G,
    pos,
    labels={n: n for n in G.nodes()},
    font_size=12,
    font_weight="bold"
)

# Edges
weights = [G[u][v]["weight"] for u, v in G.edges()]

nx.draw_networkx_edges(
    G,
    pos,
    width=weights,
    arrows=True,
    arrowsize=25
)

# Edge labels
edge_labels = {
    (u, v): G[u][v]["weight"]
    for u, v in G.edges()
}

nx.draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=edge_labels,
    font_size=10
)

plt.title(
    "Tech-SEDA Dialogic Interaction Network",
    fontsize=18,
    fontweight="bold"
)

plt.axis("off")
plt.tight_layout()
plt.show()

# --------------------------------------------
# Export network (optional)
# --------------------------------------------

nx.write_gexf(G, "tech_seda_dialogic_network.gexf")

print("Tech-SEDA dialogic network created successfully.")
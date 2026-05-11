import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from collections import defaultdict
from itertools import combinations

def generate_graph(coded_dialogue):
    G, edge_weights = build_empirical_network(coded_dialogue)
    return G, edge_weights
# ==========================================================
# TECH-SEDA DIALOGIC NETWORK ENGINE
# ==========================================================
# Combines:
#
# 1. Empirical co-occurrence network
# 2. Theoretical pedagogical network
# 3. Visualisation
# 4. Explainable dialogic analytics
#
# ==========================================================


# ----------------------------------------------------------
# TECH-SEDA CODEBOOK
# ----------------------------------------------------------

TECH_SEDA_CODES = {
    "IB": "Invitation to build on ideas",
    "B": "Building on ideas",
    "CH": "Challenge",
    "IR": "Invitation for reasoning",
    "R": "Reasoning",
    "IC": "Invitation for coordination",
    "SC": "Simple coordination",
    "RC": "Reasoned coordination",
    "II": "Inquiry invitation",
    "RB": "Reference back",
    "RW": "Reference to wider context",
    "F": "Focusing",
    "RD": "Reflect on dialogue/activity"
}


# ==========================================================
# EMPIRICAL CO-OCCURRENCE NETWORK
# ==========================================================

def build_empirical_network(
    coded_units,
    binary=True,
    include_self_loops=False
):

    edge_weights = defaultdict(int)

    for unit in coded_units:

        if binary:
            unit = list(set(unit))

        unit = [c for c in unit if c in TECH_SEDA_CODES]

        if len(unit) == 0:
            continue

        if include_self_loops:
            for code in unit:
                edge_weights[(code, code)] += 1

        for code_a, code_b in combinations(sorted(unit), 2):

            edge = tuple(sorted([code_a, code_b]))

            edge_weights[edge] += 1

    # ------------------------------------------------------
    # BUILD GRAPH
    # ------------------------------------------------------

    G = nx.Graph()

    for code, label in TECH_SEDA_CODES.items():
        G.add_node(code, label=label)

    for (a, b), weight in edge_weights.items():
        G.add_edge(a, b, weight=weight)

    return G, edge_weights


# ==========================================================
# THEORETICAL PEDAGOGICAL NETWORK
# ==========================================================

def build_theoretical_network():

    G = nx.DiGraph()

    for code, label in TECH_SEDA_CODES.items():
        G.add_node(code, label=label)

    theoretical_edges = [

        ("IB", "B", 5),
        ("B", "R", 4),
        ("B", "SC", 3),

        ("CH", "R", 5),
        ("CH", "RC", 4),

        ("IR", "R", 5),
        ("IR", "RC", 3),

        ("IC", "SC", 5),
        ("SC", "RC", 4),
        ("R", "RC", 5),

        ("II", "IR", 4),
        ("II", "CH", 3),
        ("II", "R", 3),

        ("RB", "B", 3),
        ("RB", "R", 2),

        ("RW", "R", 4),
        ("RW", "RC", 3),

        ("F", "IR", 3),
        ("F", "B", 2),

        ("RD", "RC", 4),
        ("RD", "R", 3),
    ]

    for source, target, weight in theoretical_edges:
        G.add_edge(source, target, weight=weight)

    return G


# ==========================================================
# VISUALISATION
# ==========================================================

def visualise_network(
    G,
    title="Tech-SEDA Dialogic Network",
    directed=False
):

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

    # Edge weights
    weights = [G[u][v]["weight"] for u, v in G.edges()]

    # Edges

    nx.draw_networkx_edges(G, pos, arrows=True)

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
        title,
        fontsize=18,
        fontweight="bold"
    )

    plt.axis("off")
    plt.tight_layout()
    plt.show()


# ==========================================================
# EXAMPLE EMPIRICAL DIALOGIC DATA
# ==========================================================

coded_dialogue = [

    ["IB", "B", "R"],

    ["CH", "R"],

    ["IR", "R", "B"],

    ["IC", "SC", "RC"],

    ["II", "IR"],

    ["RB", "B"],

    ["RW", "R"],

    ["F", "IB"],

    ["RD", "SC"],

    ["B", "R", "SC"]

]


# ==========================================================
# BUILD NETWORKS
# ==========================================================

empirical_graph, empirical_edges = build_empirical_network(
    coded_dialogue
)

theoretical_graph = build_theoretical_network()


# ==========================================================
# OUTPUT EMPIRICAL EDGE WEIGHTS
# ==========================================================

print("\n================ EMPIRICAL EDGE WEIGHTS ================\n")

for edge, weight in sorted(empirical_edges.items()):
    print(f"{edge}: {weight}")


# ==========================================================
# VISUALISE NETWORKS
# ==========================================================

visualise_network(
    empirical_graph,
    title="Empirical Tech-SEDA Co-occurrence Network",
    directed=False
)

visualise_network(
    theoretical_graph,
    title="Theoretical Tech-SEDA Dialogic Network",
    directed=True
)


# ==========================================================
# EXPORT NETWORKS
# ==========================================================

nx.write_gexf(
    empirical_graph,
    "empirical_tech_seda_network.gexf"
)

nx.write_gexf(
    theoretical_graph,
    "theoretical_tech_seda_network.gexf"
)

print("\nTech-SEDA networks exported successfully.")
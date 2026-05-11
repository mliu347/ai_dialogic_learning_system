from pyvis.network import Network
import networkx as nx


# -----------------------------
# Tech-SEDA dialogic categories
# -----------------------------
TECH_SEDA_CODES = {
    "IB": {
        "label": "Invitation to Build on Ideas",
        "color": "#1f77b4",
        "description": (
            "Inviting elaboration, clarification, evaluation, "
            "or improvement of previous contributions."
        )
    },

    "B": {
        "label": "Building on Ideas",
        "color": "#2ca02c",
        "description": (
            "Extending, clarifying, reformulating, or commenting "
            "on previous ideas."
        )
    },

    "CH": {
        "label": "Challenge",
        "color": "#d62728",
        "description": (
            "Questioning, disagreeing with, doubting, "
            "or challenging ideas."
        )
    },

    "IR": {
        "label": "Invitation for Reasoning",
        "color": "#9467bd",
        "description": (
            "Inviting explanation, justification, prediction, "
            "or speculation."
        )
    },

    "R": {
        "label": "Reasoning",
        "color": "#8c564b",
        "description": (
            "Providing explanations, evidence, justification, "
            "or grounded speculation."
        )
    },

    "IC": {
        "label": "Invitation for Coordination",
        "color": "#e377c2",
        "description": (
            "Inviting synthesis, comparison, evaluation, "
            "or consensus."
        )
    },

    "SC": {
        "label": "Simple Coordination",
        "color": "#7f7f7f",
        "description": (
            "Summarising or comparing multiple perspectives."
        )
    },

    "RC": {
        "label": "Reasoned Coordination",
        "color": "#bcbd22",
        "description": (
            "Reasoned comparison or resolution between multiple ideas."
        )
    },

    "II": {
        "label": "Inquiry Invitation",
        "color": "#17becf",
        "description": (
            "Inviting inquiry, investigation, or new questions."
        )
    },

    "RB": {
        "label": "Reference Back",
        "color": "#ff7f0e",
        "description": (
            "Referring back to shared prior knowledge, "
            "experience, or discussion."
        )
    },

    "RW": {
        "label": "Reference to Wider Context",
        "color": "#aec7e8",
        "description": (
            "Connecting dialogue to external knowledge, "
            "contexts, or resources."
        )
    },

    "F": {
        "label": "Focusing",
        "color": "#98df8a",
        "description": (
            "Guiding or scaffolding discussion toward key issues."
        )
    },

    "RD": {
        "label": "Reflection on Dialogue/Activity",
        "color": "#ff9896",
        "description": (
            "Reflecting metacognitively on dialogue or learning."
        )
    }
}


# ----------------------------------------------------
# Example co-occurrence relationships for ENA-style graph
# (You can replace these with your real ENA output)
# ----------------------------------------------------
dialogic_connections = [
    ("IB", "B", 12),
    ("IR", "R", 15),
    ("CH", "R", 8),
    ("IC", "SC", 10),
    ("SC", "RC", 6),
    ("II", "IR", 7),
    ("RB", "B", 5),
    ("RW", "R", 9),
    ("F", "IR", 4),
    ("RD", "SC", 3),
]


# -----------------------------
# Build NetworkX graph
# -----------------------------
G = nx.Graph()

# Add nodes
for code, info in TECH_SEDA_CODES.items():

    G.add_node(
        code,
        label=info["label"],
        title=(
            f"<b>{code}</b><br>"
            f"{info['description']}"
        ),
        color=info["color"],
        size=25
    )

# Add edges
for source, target, weight in dialogic_connections:

    G.add_edge(
        source,
        target,
        weight=weight,
        value=weight,
        title=f"Co-occurrence Frequency: {weight}"
    )


# -----------------------------
# Visualisation function
# -----------------------------
def visualize_tech_seda_graph(
        graph,
        output_file="tech_seda_ena_graph.html"
):
    from pyvis.network import Network

    net = Network(
        height="750px",
        width="100%",
        notebook=False,  # IMPORTANT
        cdn_resources="in_line"  # IMPORTANT FIX
    )

    # Import NetworkX graph
    net.from_nx(graph)

    # Physics settings
    net.barnes_hut(
        gravity=-25000,
        central_gravity=0.2,
        spring_length=180,
        spring_strength=0.03,
        damping=0.09
    )

    # Improve edge appearance
    for edge in net.edges:
        edge["color"] = "#999999"
        edge["width"] = edge.get("value", 1)

    # Improve node appearance
    for node in net.nodes:
        node["font"] = {
            "size": 18,
            "face": "Arial"
        }

    # Add interaction controls
    net.show_buttons(filter_=["physics"])

    # Generate HTML
    net.write_html(output_file)
    import webbrowser
    webbrowser.open(output_file)

    print(f"Graph saved to: {output_file}")


# -----------------------------
# Run visualisation
# -----------------------------
visualize_tech_seda_graph(G)
import numpy as np
from collections import defaultdict
from itertools import combinations


# ==========================================================
# TECH-SEDA DIALOGIC CO-OCCURRENCE NETWORK CONSTRUCTION
# ==========================================================
# Purpose:
# Build a weighted co-occurrence matrix for Tech-SEDA dialogic
# codes occurring within the same analytical unit
# (turn / sequence / episode).
#
# The implementation follows Tech-SEDA coding principles:
# ----------------------------------------------------------
# • Multiple codes may co-exist in one unit.
# • Coding is binary within each unit:
#     repeated occurrence of same code counted once.
# • Co-occurrence indicates dialogic relational structure.
# • Windows may represent:
#       - turns
#       - interaction sequences
#       - episodes
#       - temporally bounded discourse segments
#
# Example window:
# ["IB", "B", "R"]
#
# indicates:
# Invitation to build on ideas +
# Building on ideas +
# Reasoning
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


# ----------------------------------------------------------
# BUILD CO-OCCURRENCE EDGE WEIGHTS
# ----------------------------------------------------------

def build_cooccurrence_matrix(
    coded_units,
    binary=True,
    include_self_loops=False
):
    """
    Build Tech-SEDA co-occurrence network.

    Parameters
    ----------
    coded_units : list[list[str]]
        Each inner list represents one analytical unit
        (turn / sequence / episode) containing Tech-SEDA codes.

    binary : bool
        If True:
            repeated codes inside one unit counted once.
        Recommended by Tech-SEDA coding rules.

    include_self_loops : bool
        Whether to count same-code repetition
        (e.g., R-R).

    Returns
    -------
    edge_weights : dict
        Dictionary of weighted edges.

    adjacency_matrix : np.ndarray
        Symmetric co-occurrence matrix.

    labels : list
        Ordered code labels.
    """

    edge_weights = defaultdict(int)

    # ------------------------------------------------------
    # PROCESS EACH ANALYTICAL UNIT
    # ------------------------------------------------------

    for unit in coded_units:

        # Binary coding rule
        if binary:
            unit = list(set(unit))

        # Remove uncoded or invalid labels
        unit = [c for c in unit if c in TECH_SEDA_CODES]

        # Skip empty units
        if len(unit) == 0:
            continue

        # --------------------------------------------------
        # SELF-LOOPS
        # --------------------------------------------------

        if include_self_loops:
            for code in unit:
                edge_weights[(code, code)] += 1

        # --------------------------------------------------
        # CODE CO-OCCURRENCES
        # --------------------------------------------------

        for code_a, code_b in combinations(sorted(unit), 2):

            edge = tuple(sorted([code_a, code_b]))

            edge_weights[edge] += 1

    # ------------------------------------------------------
    # CREATE ADJACENCY MATRIX
    # ------------------------------------------------------

    labels = sorted(TECH_SEDA_CODES.keys())

    index = {label: i for i, label in enumerate(labels)}

    matrix = np.zeros((len(labels), len(labels)), dtype=int)

    for (a, b), weight in edge_weights.items():

        i = index[a]
        j = index[b]

        matrix[i, j] = weight
        matrix[j, i] = weight

    return edge_weights, matrix, labels


# ==========================================================
# EXAMPLE DATA
# ==========================================================
# Each list = one coded interaction unit
#
# Example interpretations:
#
# ["IB", "B", "R"]
# -> invitation to build
# -> building on peer idea
# -> explicit reasoning
#
# ["CH", "R"]
# -> challenge + justification
#
# ["IC", "SC", "RC"]
# -> coordination sequence
#
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
# RUN NETWORK CONSTRUCTION
# ==========================================================

edges, adjacency_matrix, labels = build_cooccurrence_matrix(
    coded_dialogue,
    binary=True,
    include_self_loops=False
)


# ==========================================================
# OUTPUT
# ==========================================================

print("\n================ EDGE WEIGHTS ================\n")

for edge, weight in sorted(edges.items()):
    print(f"{edge}: {weight}")

print("\n================ ADJACENCY MATRIX ================\n")

print("Labels:")
print(labels)

print("\nMatrix:")
print(adjacency_matrix)
"""
app/research/ena/statistics.py

Research-grade statistical and network analytics utilities for
Tech-SEDA-informed ENA (Epistemic Network Analysis).

This module operationalises dialogic interaction categories derived from
Tech-SEDA coding principles, including:

IB  = Invitation to Build on Ideas
B   = Building on Ideas
CH  = Challenge
IR  = Invitation for Reasoning
R   = Reasoning
IC  = Invitation for Coordination
SC  = Simple Coordination
RC  = Reasoned Coordination
II  = Inquiry Invitation
RB  = Reference Back
RW  = Reference to Wider Context
F   = Focusing
RD  = Reflect on Dialogue / Activity

The module supports:
- ENA adjacency construction
- weighted discourse networks
- graph density
- centrality analysis
- modularity / community detection
- discourse cohesion
- teacher-student balance
- temporal dialogic flow analysis
- binary and weighted coding schemes

The implementation follows Tech-SEDA coding assumptions:
- multiple codes per turn are permitted
- uncoded turns may exist
- coding can be binary or frequency-based
- turns, sequences, or episodes may be units of analysis
- dialogic relations are contextual and sequential

Dependencies:
    pip install networkx numpy scipy pandas python-louvain
"""

from __future__ import annotations

from dataclasses import dataclass
from collections import defaultdict, Counter
from itertools import combinations
from typing import Dict, List, Tuple, Optional

import numpy as np
import pandas as pd
import networkx as nx
from scipy.sparse import csr_matrix

try:
    import community as community_louvain
except ImportError:
    community_louvain = None


# ============================================================
# TECH-SEDA CODEBOOK
# ============================================================

TECH_SEDA_CODES = {
    "IB": "Invitation to Build on Ideas",
    "B": "Building on Ideas",
    "CH": "Challenge",
    "IR": "Invitation for Reasoning",
    "R": "Reasoning",
    "IC": "Invitation for Coordination",
    "SC": "Simple Coordination",
    "RC": "Reasoned Coordination",
    "II": "Inquiry Invitation",
    "RB": "Reference Back",
    "RW": "Reference to Wider Context",
    "F": "Focusing",
    "RD": "Reflect on Dialogue / Activity",
}


INVITATION_CODES = {
    "IB",
    "IR",
    "IC",
    "II",
}

REASONING_CODES = {
    "R",
    "RC",
}

COORDINATION_CODES = {
    "SC",
    "RC",
    "IC",
}

DIALOGIC_EXPANSION_CODES = {
    "IB",
    "B",
    "IR",
    "R",
    "II",
}

CRITICALITY_CODES = {
    "CH",
    "RC",
}


# ============================================================
# DATA STRUCTURES
# ============================================================

@dataclass
class DialogueTurn:
    """
    Represents a single unit of dialogic interaction.

    Parameters
    ----------
    speaker : str
        Participant identifier.

    role : str
        e.g. teacher / student / AI / group.

    utterance : str
        Original dialogue contribution.

    codes : List[str]
        Tech-SEDA dialogic codes.

    timestamp : Optional[float]
        Temporal index.

    sequence_id : Optional[int]
        Episode or activity sequence identifier.
    """

    speaker: str
    role: str
    utterance: str
    codes: List[str]
    timestamp: Optional[float] = None
    sequence_id: Optional[int] = None


# ============================================================
# ENA CO-OCCURRENCE MATRIX
# ============================================================

class ENAStatistics:
    """
    Statistical and network analytics for Tech-SEDA-coded dialogue.
    """

    def __init__(self, turns: List[DialogueTurn]):
        self.turns = turns
        self.graph = nx.Graph()

    # --------------------------------------------------------
    # CO-OCCURRENCE MATRIX
    # --------------------------------------------------------

    def build_cooccurrence_matrix(self) -> pd.DataFrame:
        """
        Build symmetric co-occurrence matrix from Tech-SEDA codes.

        Multiple codes within the same turn contribute to weighted
        co-occurrence relationships.
        """

        codes = list(TECH_SEDA_CODES.keys())
        matrix = pd.DataFrame(
            0,
            index=codes,
            columns=codes,
            dtype=int,
        )

        for turn in self.turns:
            valid_codes = [c for c in turn.codes if c in codes]

            for c1, c2 in combinations(sorted(set(valid_codes)), 2):
                matrix.loc[c1, c2] += 1
                matrix.loc[c2, c1] += 1

            for code in valid_codes:
                matrix.loc[code, code] += 1

        return matrix

    # --------------------------------------------------------
    # BUILD NETWORK GRAPH
    # --------------------------------------------------------

    def build_network(
        self,
        min_weight: int = 1,
    ) -> nx.Graph:
        """
        Construct weighted discourse graph.
        """

        matrix = self.build_cooccurrence_matrix()

        G = nx.Graph()

        for code in matrix.index:
            G.add_node(
                code,
                label=TECH_SEDA_CODES[code],
            )

        for i in matrix.index:
            for j in matrix.columns:
                weight = matrix.loc[i, j]

                if i != j and weight >= min_weight:
                    G.add_edge(i, j, weight=weight)

        self.graph = G
        return G

    # --------------------------------------------------------
    # GRAPH DENSITY
    # --------------------------------------------------------

    def graph_density(self) -> float:
        """
        Estimate dialogic connectivity density.

        Higher density suggests richer integration between
        dialogic functions.
        """

        if len(self.graph.nodes) == 0:
            self.build_network()

        return nx.density(self.graph)

    # --------------------------------------------------------
    # CENTRALITY ANALYSIS
    # --------------------------------------------------------

    def centrality_metrics(self) -> pd.DataFrame:
        """
        Compute weighted centrality indicators.

        Metrics:
        - degree centrality
        - betweenness centrality
        - eigenvector centrality
        """

        if len(self.graph.nodes) == 0:
            self.build_network()

        degree = nx.degree_centrality(self.graph)
        betweenness = nx.betweenness_centrality(
            self.graph,
            weight="weight",
        )

        try:
            eigenvector = nx.eigenvector_centrality_numpy(
                self.graph,
                weight="weight",
            )
        except Exception:
            eigenvector = {n: 0.0 for n in self.graph.nodes}

        return pd.DataFrame({
            "degree": degree,
            "betweenness": betweenness,
            "eigenvector": eigenvector,
        })

    # --------------------------------------------------------
    # MODULARITY / COMMUNITY DETECTION
    # --------------------------------------------------------

    def modularity_analysis(self) -> Dict:
        """
        Detect dialogic communities / discourse clusters.

        Useful for identifying whether discourse separates into:
        - reasoning clusters
        - inquiry clusters
        - coordination clusters
        - challenge clusters
        """

        if len(self.graph.nodes) == 0:
            self.build_network()

        if community_louvain is None:
            raise ImportError(
                "python-louvain package is required for modularity analysis"
            )

        partition = community_louvain.best_partition(
            self.graph,
            weight="weight",
        )

        modularity = community_louvain.modularity(
            partition,
            self.graph,
            weight="weight",
        )

        return {
            "partition": partition,
            "modularity": modularity,
        }

    # --------------------------------------------------------
    # DISCOURSE COHESION
    # --------------------------------------------------------

    def discourse_cohesion(self) -> float:
        """
        Estimate discourse cohesion.

        Operationalisation:
        Ratio of connected dialogic transitions relative to
        total possible transitions.

        High cohesion indicates sustained dialogic uptake,
        elaboration, reasoning, and coordination.
        """

        connected = 0
        total = 0

        for i in range(len(self.turns) - 1):
            current_codes = set(self.turns[i].codes)
            next_codes = set(self.turns[i + 1].codes)

            total += 1

            if current_codes.intersection(next_codes):
                connected += 1
                continue

            if (
                current_codes & DIALOGIC_EXPANSION_CODES
                and next_codes & REASONING_CODES
            ):
                connected += 1

        if total == 0:
            return 0.0

        return connected / total

    # --------------------------------------------------------
    # TEACHER-STUDENT BALANCE
    # --------------------------------------------------------

    def teacher_student_balance(self) -> Dict:
        """
        Analyse dialogic participation balance.

        Indicators:
        - turn distribution
        - code distribution
        - invitation dominance
        - reasoning contribution balance
        """

        role_turns = Counter()
        role_codes = defaultdict(Counter)

        for turn in self.turns:
            role_turns[turn.role] += 1

            for code in turn.codes:
                role_codes[turn.role][code] += 1

        total_turns = sum(role_turns.values())

        role_distribution = {
            role: count / total_turns
            for role, count in role_turns.items()
        }

        invitation_distribution = {}
        reasoning_distribution = {}

        for role, counter in role_codes.items():
            invitation_distribution[role] = sum(
                counter[c] for c in INVITATION_CODES
            )

            reasoning_distribution[role] = sum(
                counter[c] for c in REASONING_CODES
            )

        return {
            "turn_distribution": role_distribution,
            "invitation_distribution": invitation_distribution,
            "reasoning_distribution": reasoning_distribution,
        }

    # --------------------------------------------------------
    # DIALOGIC TRAJECTORY ANALYSIS
    # --------------------------------------------------------

    def dialogic_trajectory(self) -> pd.DataFrame:
        """
        Temporal sequence analysis of dialogic progression.

        Identifies how discourse develops from:
        invitation -> reasoning -> coordination -> reflection.
        """

        trajectories = []

        for i in range(len(self.turns) - 1):
            current_turn = self.turns[i]
            next_turn = self.turns[i + 1]

            for c1 in current_turn.codes:
                for c2 in next_turn.codes:
                    trajectories.append({
                        "from": c1,
                        "to": c2,
                        "speaker_from": current_turn.speaker,
                        "speaker_to": next_turn.speaker,
                    })

        return pd.DataFrame(trajectories)

    # --------------------------------------------------------
    # TRANSITION MATRIX
    # --------------------------------------------------------

    def transition_matrix(self) -> pd.DataFrame:
        """
        Build first-order Markov transition matrix.

        Useful for:
        - sequential discourse analysis
        - hidden Markov modelling
        - process mining
        - temporal ENA extensions
        """

        codes = list(TECH_SEDA_CODES.keys())

        matrix = pd.DataFrame(
            0,
            index=codes,
            columns=codes,
            dtype=int,
        )

        for i in range(len(self.turns) - 1):
            current_codes = self.turns[i].codes
            next_codes = self.turns[i + 1].codes

            for c1 in current_codes:
                for c2 in next_codes:
                    if c1 in codes and c2 in codes:
                        matrix.loc[c1, c2] += 1

        return matrix

    # --------------------------------------------------------
    # EXPORT EDGE LIST
    # --------------------------------------------------------

    def export_edge_list(self) -> pd.DataFrame:
        """
        Export ENA weighted edge list.

        Compatible with:
        - Gephi
        - Cytoscape
        - rENA
        - network visualisation pipelines
        """

        if len(self.graph.nodes) == 0:
            self.build_network()

        edges = []

        for u, v, data in self.graph.edges(data=True):
            edges.append({
                "source": u,
                "target": v,
                "weight": data.get("weight", 1),
            })

        return pd.DataFrame(edges)


# ============================================================
# EXAMPLE USAGE
# ============================================================

if __name__ == "__main__":

    sample_turns = [
        DialogueTurn(
            speaker="Teacher",
            role="teacher",
            utterance="Can anyone build on that idea?",
            codes=["IB", "IR"],
        ),
        DialogueTurn(
            speaker="Student_A",
            role="student",
            utterance="I think the design solves some problems because...",
            codes=["B", "R"],
        ),
        DialogueTurn(
            speaker="Student_B",
            role="student",
            utterance="But it cannot solve every social problem.",
            codes=["CH", "R"],
        ),
        DialogueTurn(
            speaker="Teacher",
            role="teacher",
            utterance="Can we compare both perspectives?",
            codes=["IC"],
        ),
        DialogueTurn(
            speaker="Student_C",
            role="student",
            utterance="Maybe design helps gradually rather than completely.",
            codes=["RC", "R"],
        ),
    ]

    stats = ENAStatistics(sample_turns)

    print("\n=== CO-OCCURRENCE MATRIX ===")
    print(stats.build_cooccurrence_matrix())

    print("\n=== GRAPH DENSITY ===")
    print(stats.graph_density())

    print("\n=== CENTRALITY ===")
    print(stats.centrality_metrics())

    print("\n=== DISCOURSE COHESION ===")
    print(stats.discourse_cohesion())

    print("\n=== TEACHER-STUDENT BALANCE ===")
    print(stats.teacher_student_balance())

    print("\n=== TRANSITION MATRIX ===")
    print(stats.transition_matrix())

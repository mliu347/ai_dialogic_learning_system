# ============================================================
# Tech-SEDA Windowing + Dialogic Coding Infrastructure
# Research-grade implementation for ENA / discourse analytics
# ============================================================

from collections import defaultdict
from typing import List, Dict, Any


# ============================================================
# Official Tech-SEDA Coding Framework
# ============================================================

TECH_SEDA_CODES = {
    "IB": {
        "name": "Invitation to Build on Ideas",
        "definition": (
            "Invite building on, elaboration, clarification, "
            "evaluation, reformulation, or commenting on own "
            "or others’ ideas/contributions."
        )
    },

    "B": {
        "name": "Building on Ideas",
        "definition": (
            "Build on, elaborate, clarify, reformulate, extend, "
            "or comment on previous ideas/contributions."
        )
    },

    "CH": {
        "name": "Challenge",
        "definition": (
            "Question, doubt, disagree with, challenge, "
            "or reject an idea."
        )
    },

    "IR": {
        "name": "Invitation for Reasoning",
        "definition": (
            "Invite explanation, justification, speculation, "
            "prediction, hypothesising, or evidence-based reasoning."
        )
    },

    "R": {
        "name": "Reasoning",
        "definition": (
            "Provide explanation, justification, evidence, "
            "prediction, speculation, analogy, categorisation, "
            "or explicit reasoning."
        )
    },

    "IC": {
        "name": "Invitation for Coordination",
        "definition": (
            "Invite synthesis, comparison, evaluation, "
            "consensus, summary, or resolution across "
            "multiple contributions."
        )
    },

    "SC": {
        "name": "Simple Coordination",
        "definition": (
            "Summarise, synthesise, compare, evaluate, "
            "or coordinate multiple ideas without extended reasoning."
        )
    },

    "RC": {
        "name": "Reasoned Coordination",
        "definition": (
            "Coordinate, compare, evaluate, or resolve "
            "multiple contributions using explicit reasoning "
            "or counter-argument."
        )
    },

    "II": {
        "name": "Inquiry Invitation",
        "definition": (
            "Invite inquiry, investigation, question posing, "
            "or collaborative exploration."
        )
    },

    "RB": {
        "name": "Reference Back",
        "definition": (
            "Refer to prior shared knowledge, earlier lessons, "
            "previous discussions, or collective experiences."
        )
    },

    "RW": {
        "name": "Reference to Wider Context",
        "definition": (
            "Connect dialogue to external knowledge, wider contexts, "
            "experts, real-world examples, or outside resources."
        )
    },

    "F": {
        "name": "Focusing",
        "definition": (
            "Guide, scaffold, redirect, or focus dialogue "
            "towards salient aspects of the task or discussion."
        )
    },

    "RD": {
        "name": "Reflect on Dialogue or Activity",
        "definition": (
            "Reflect metacognitively on dialogue processes, "
            "learning activity, participation, or shifts in understanding."
        )
    }
}


# ============================================================
# Core Window Constructor
# ============================================================

def create_windows(
    coded_turns: List[Dict[str, Any]],
    window_size: int = 3,
    binary_codes: bool = True
) -> List[Dict[str, Any]]:
    """
    Create sliding dialogic windows for ENA / discourse analysis.

    Parameters
    ----------
    coded_turns : List[Dict]

        Example format:
        {
            "turn_id": 1,
            "speaker": "Teacher",
            "utterance": "...",
            "codes": ["IB", "IR"]
        }

    window_size : int
        Number of consecutive turns inside each window.

    binary_codes : bool
        If True:
            each code appears once per window
            (recommended for ENA).

        If False:
            preserve repeated frequencies.

    Returns
    -------
    List[Dict]
    """

    windows = []

    # --------------------------------------------------------
    # Sliding-window iteration
    # --------------------------------------------------------

    for i in range(len(coded_turns) - window_size + 1):

        current_window = coded_turns[i:i + window_size]

        # ----------------------------------------------------
        # Metadata
        # ----------------------------------------------------

        turn_ids = [t["turn_id"] for t in current_window]

        speakers = [t["speaker"] for t in current_window]

        utterances = [t["utterance"] for t in current_window]

        # ----------------------------------------------------
        # Collect Tech-SEDA codes
        # ----------------------------------------------------

        all_codes = []

        for turn in current_window:
            all_codes.extend(turn.get("codes", []))

        # ----------------------------------------------------
        # Binary coding rule (Tech-SEDA recommendation)
        # ----------------------------------------------------

        if binary_codes:
            all_codes = sorted(list(set(all_codes)))

        # ----------------------------------------------------
        # Frequency distribution
        # ----------------------------------------------------

        code_frequency = defaultdict(int)

        for code in all_codes:
            code_frequency[code] += 1

        # ----------------------------------------------------
        # Detect dialogic patterns
        # ----------------------------------------------------

        interaction_patterns = []

        # ---- Dialogic uptake
        if "IB" in all_codes and "B" in all_codes:
            interaction_patterns.append(
                "dialogic_uptake"
            )

        # ---- Reasoning chain
        if "IR" in all_codes and "R" in all_codes:
            interaction_patterns.append(
                "reasoning_chain"
            )

        # ---- Productive disagreement
        if "CH" in all_codes and (
            "R" in all_codes or
            "RC" in all_codes or
            "B" in all_codes
        ):
            interaction_patterns.append(
                "productive_disagreement"
            )

        # ---- Inquiry trajectory
        if "II" in all_codes:
            interaction_patterns.append(
                "dialogic_inquiry"
            )

        # ---- Coordination sequence
        if "IC" in all_codes and (
            "SC" in all_codes or
            "RC" in all_codes
        ):
            interaction_patterns.append(
                "collective_coordination"
            )

        # ---- Knowledge integration
        if "RB" in all_codes or "RW" in all_codes:
            interaction_patterns.append(
                "knowledge_connection"
            )

        # ---- Metacognitive reflection
        if "RD" in all_codes:
            interaction_patterns.append(
                "metacognitive_reflection"
            )

        # ---- Guided scaffolding
        if "F" in all_codes:
            interaction_patterns.append(
                "dialogic_scaffolding"
            )

        # ----------------------------------------------------
        # Construct structured window
        # ----------------------------------------------------

        windows.append({

            "window_id": i,

            "turn_range": (
                turn_ids[0],
                turn_ids[-1]
            ),

            "window_size": window_size,

            "speakers": speakers,

            "utterances": utterances,

            "codes": all_codes,

            "code_frequency": dict(code_frequency),

            "interaction_patterns": interaction_patterns
        })

    return windows


# ============================================================
# Example Dataset
# ============================================================

dialogue_data = [

    {
        "turn_id": 1,
        "speaker": "Teacher",
        "utterance": (
            "Can anyone build on Zoe's idea?"
        ),
        "codes": ["IB"]
    },

    {
        "turn_id": 2,
        "speaker": "Student_A",
        "utterance": (
            "She looks more confident because "
            "of her posture."
        ),
        "codes": ["B", "R"]
    },

    {
        "turn_id": 3,
        "speaker": "Student_B",
        "utterance": (
            "But paintings may exaggerate rulers."
        ),
        "codes": ["CH", "R"]
    },

    {
        "turn_id": 4,
        "speaker": "Teacher",
        "utterance": (
            "Why do you think that?"
        ),
        "codes": ["IR"]
    },

    {
        "turn_id": 5,
        "speaker": "Student_B",
        "utterance": (
            "Artists often idealised monarchs "
            "in historical portraits."
        ),
        "codes": ["R", "RW"]
    },

    {
        "turn_id": 6,
        "speaker": "Teacher",
        "utterance": (
            "How does this connect to our "
            "previous lesson on propaganda?"
        ),
        "codes": ["RB", "F"]
    },

    {
        "turn_id": 7,
        "speaker": "Student_C",
        "utterance": (
            "Maybe portraits were used to shape "
            "public opinion."
        ),
        "codes": ["R", "B"]
    },

    {
        "turn_id": 8,
        "speaker": "Teacher",
        "utterance": (
            "Can your group investigate another "
            "historical example for next lesson?"
        ),
        "codes": ["II"]
    }
]


# ============================================================
# Generate Windows
# ============================================================

windows = create_windows(
    coded_turns=dialogue_data,
    window_size=3,
    binary_codes=True
)


# ============================================================
# Display Results
# ============================================================

for window in windows:

    print("=" * 80)

    print(f"WINDOW ID: {window['window_id']}")
    print(f"TURN RANGE: {window['turn_range']}")

    print("\nSPEAKERS:")
    print(window["speakers"])

    print("\nCODES:")
    print(window["codes"])

    print("\nINTERACTION PATTERNS:")
    print(window["interaction_patterns"])

    print("\nUTTERANCES:")

    for utt in window["utterances"]:
        print(f"- {utt}")


# ============================================================
# Optional ENA Export Preparation
# ============================================================

def prepare_ena_vectors(
    windows: List[Dict[str, Any]]
) -> List[Dict[str, int]]:
    """
    Convert windows into binary ENA vectors.
    """

    ena_rows = []

    all_possible_codes = list(
        TECH_SEDA_CODES.keys()
    )

    for window in windows:

        row = {}

        for code in all_possible_codes:

            row[code] = (
                1 if code in window["codes"] else 0
            )

        ena_rows.append(row)

    return ena_rows


# ============================================================
# Generate ENA-ready binary vectors
# ============================================================

ena_vectors = prepare_ena_vectors(windows)

print("\n")
print("=" * 80)
print("ENA BINARY VECTORS")
print("=" * 80)

for row in ena_vectors:
    print(row)
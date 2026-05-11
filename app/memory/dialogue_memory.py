# app/memory/dialogue_memory.py

"""
Tech-SEDA Dialogue Memory System
--------------------------------

Purpose:
Store sequential dialogic interaction turns for:
- ENA (Epistemic Network Analysis)
- sequential discourse analysis
- trajectory modelling
- dialogic learning analytics
- AI-mediated classroom interaction research

Important:
ENA is computed across temporal interaction trajectories,
NOT isolated utterances.

This module therefore stores:
    - sequential turns
    - speaker information
    - timestamps
    - utterances
    - multimodal metadata
    - Tech-SEDA dialogic codes
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from collections import Counter
import uuid
import time


# ============================================================
# TECH-SEDA CODE DEFINITIONS
# ============================================================

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
    "RD": "Reflect on dialogue/activity",
    "U": "Uncoded"
}


# ============================================================
# DIALOGUE TURN OBJECT
# ============================================================

@dataclass
class DialogueTurn:
    """
    Represents one interactional turn.

    A turn may include:
        - verbal utterance
        - multimodal interaction
        - symbolic interaction
        - digital contribution
    """

    speaker: str
    utterance: str

    codes: List[str]

    timestamp: float = field(default_factory=time.time)

    turn_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    modality: str = "speech"
    # speech / gesture / emoji / digital / multimodal

    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:

        return {
            "turn_id": self.turn_id,
            "speaker": self.speaker,
            "utterance": self.utterance,
            "codes": self.codes,
            "timestamp": self.timestamp,
            "modality": self.modality,
            "metadata": self.metadata
        }


# ============================================================
# DIALOGUE MEMORY
# ============================================================

class DialogueMemory:
    """
    Sequential storage of dialogic interaction trajectories.

    Supports:
        - ENA window construction
        - temporal discourse analysis
        - co-occurrence analysis
        - Tech-SEDA analytics
        - classroom trajectory modelling
    """

    def __init__(self):

        self.turns: List[DialogueTurn] = []

    # ========================================================
    # ADD TURN
    # ========================================================

    def add_turn(
        self,
        speaker: str,
        utterance: str,
        codes: List[str],
        modality: str = "speech",
        metadata: Optional[Dict[str, Any]] = None
    ):

        """
        Add one interactional turn.

        Notes:
        - Binary coding principle:
          repeated same code inside one turn counted once.

        - Multiple different codes ARE allowed.

        - Unknown codes are automatically filtered.
        """

        validated_codes = []

        for code in codes:

            if code in TECH_SEDA_CODES:
                validated_codes.append(code)

        # binary coding rule
        validated_codes = list(set(validated_codes))

        if not validated_codes:
            validated_codes = ["U"]

        turn = DialogueTurn(
            speaker=speaker,
            utterance=utterance,
            codes=validated_codes,
            modality=modality,
            metadata=metadata or {}
        )

        self.turns.append(turn)

    # ========================================================
    # GET ALL TURNS
    # ========================================================

    def get_turns(self) -> List[Dict[str, Any]]:

        return [turn.to_dict() for turn in self.turns]

    # ========================================================
    # GET ALL CODES
    # ========================================================

    def get_all_codes(self) -> List[str]:

        all_codes = []

        for turn in self.turns:
            all_codes.extend(turn.codes)

        return all_codes

    # ========================================================
    # CODE FREQUENCY
    # ========================================================

    def get_code_frequency(self) -> Dict[str, int]:

        return dict(Counter(self.get_all_codes()))

    # ========================================================
    # ENA SLIDING WINDOWS
    # ========================================================

    def build_ena_windows(self, window_size: int = 4):

        """
        Build sequential ENA windows.

        Example:
            window_size = 4

            Turn1
            Turn2
            Turn3
            Turn4

        -> one ENA stanza
        """

        windows = []

        for i in range(len(self.turns) - window_size + 1):

            window = self.turns[i:i + window_size]

            windows.append(window)

        return windows

    # ========================================================
    # CODE CO-OCCURRENCE
    # ========================================================

    def build_co_occurrence_network(
        self,
        window_size: int = 4
    ) -> Dict[tuple, int]:

        """
        Construct ENA-style co-occurrence edges.
        """

        from itertools import combinations

        edge_counter = Counter()

        windows = self.build_ena_windows(window_size)

        for window in windows:

            window_codes = []

            for turn in window:
                window_codes.extend(turn.codes)

            window_codes = list(set(window_codes))

            for edge in combinations(sorted(window_codes), 2):
                edge_counter[edge] += 1

        return dict(edge_counter)

    # ========================================================
    # FILTER BY CODE
    # ========================================================

    def filter_by_code(self, code: str):

        return [
            turn.to_dict()
            for turn in self.turns
            if code in turn.codes
        ]

    # ========================================================
    # FILTER BY SPEAKER
    # ========================================================

    def filter_by_speaker(self, speaker: str):

        return [
            turn.to_dict()
            for turn in self.turns
            if turn.speaker == speaker
        ]

    # ========================================================
    # EXPORT FOR ENA / R / CSV
    # ========================================================

    def export_for_ena(self):

        rows = []

        for idx, turn in enumerate(self.turns):

            row = {
                "turn_index": idx,
                "speaker": turn.speaker,
                "utterance": turn.utterance,
                "timestamp": turn.timestamp
            }

            for code in TECH_SEDA_CODES.keys():
                row[code] = int(code in turn.codes)

            rows.append(row)

        return rows

    # ========================================================
    # SUMMARY
    # ========================================================

    def summary(self):

        return {
            "total_turns": len(self.turns),
            "code_frequency": self.get_code_frequency(),
            "unique_speakers": len(
                set(turn.speaker for turn in self.turns)
            )
        }


# ============================================================
# EXAMPLE USAGE
# ============================================================

if __name__ == "__main__":

    memory = DialogueMemory()

    # --------------------------------------------------------
    # Example 1: Invitation for reasoning
    # --------------------------------------------------------

    memory.add_turn(
        speaker="Teacher",
        utterance="Why do you think the character behaved this way?",
        codes=["IR"]
    )

    # --------------------------------------------------------
    # Example 2: Reasoning + Building
    # --------------------------------------------------------

    memory.add_turn(
        speaker="Student_A",
        utterance=(
            "I think she behaved this way because "
            "she felt excluded from the group."
        ),
        codes=["R", "B"]
    )

    # --------------------------------------------------------
    # Example 3: Challenge
    # --------------------------------------------------------

    memory.add_turn(
        speaker="Student_B",
        utterance=(
            "But could it also be because "
            "she misunderstood the situation?"
        ),
        codes=["CH", "IR"]
    )

    # --------------------------------------------------------
    # Example 4: Reasoned Coordination
    # --------------------------------------------------------

    memory.add_turn(
        speaker="Teacher",
        utterance=(
            "So we now have two possible interpretations: "
            "social exclusion and misunderstanding."
        ),
        codes=["RC", "SC"]
    )

    print(memory.summary())

    print("\nENA WINDOWS:")
    windows = memory.build_ena_windows(window_size=2)

    for w in windows:
        print([t.utterance for t in w])

    print("\nCO-OCCURRENCE NETWORK:")
    print(memory.build_co_occurrence_network())
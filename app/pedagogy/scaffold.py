from typing import Dict, List, Optional


TECH_SEDA_CODES = {
    "IB": "invitation_building",
    "B": "building_on_ideas",
    "CH": "challenge",
    "IR": "invitation_reasoning",
    "R": "reasoning",
    "IC": "invitation_coordination",
    "SC": "simple_coordination",
    "RC": "reasoned_coordination",
    "II": "inquiry_invitation",
    "RB": "reference_back",
    "RW": "reference_wider_context",
    "F": "focusing",
    "RD": "reflection_dialogue_activity"
}


def scaffold_decision(
    tech_seda: Dict,
    curriculum: Optional[Dict] = None
) -> Dict:
    """
    Research-interpretable pedagogical scaffolding engine
    ----------------------------------------------------
    Converts Tech-SEDA dialogic discourse signals into
    adaptive pedagogical actions.

    Assumptions:
    - Binary coding:
        1 = present
        0 = absent
    - Multiple codes may co-occur.
    - Decision logic prioritises higher-order dialogicity.
    """

    features = tech_seda.get("tech_seda_features", {})

    # ---------- Extract Tech-SEDA signals ----------
    IB = features.get("IB", 0)
    B  = features.get("B", 0)
    CH = features.get("CH", 0)
    IR = features.get("IR", 0)
    R  = features.get("R", 0)
    IC = features.get("IC", 0)
    SC = features.get("SC", 0)
    RC = features.get("RC", 0)
    II = features.get("II", 0)
    RB = features.get("RB", 0)
    RW = features.get("RW", 0)
    F  = features.get("F", 0)
    RD = features.get("RD", 0)

    cognitive_load = tech_seda.get("cognitive_load", 0)

    pedagogical_action = None
    scaffold_level = None
    rationale = []

    # =========================================================
    # HIGHER-ORDER DIALOGIC REASONING
    # =========================================================

    if RC == 1:
        pedagogical_action = "facilitate_reasoned_synthesis"
        scaffold_level = "minimal_support"

        rationale.append(
            "Reasoned coordination detected: learners are comparing "
            "and resolving multiple perspectives using explicit reasoning."
        )

    elif SC == 1 or IC == 1:
        pedagogical_action = "prompt_collective_synthesis"
        scaffold_level = "low_support"

        rationale.append(
            "Co-ordination discourse detected: learners are synthesising "
            "or comparing multiple contributions."
        )

    # =========================================================
    # REASONING & EXPLANATION
    # =========================================================

    elif R == 1:
        pedagogical_action = "extend_reasoning_dialogue"
        scaffold_level = "low_support"

        rationale.append(
            "Explicit reasoning or justification detected."
        )

    elif IR == 1:
        pedagogical_action = "prompt_evidence_based_explanation"
        scaffold_level = "medium_support"

        rationale.append(
            "Invitation for reasoning detected; scaffolding explanation "
            "and justification is required."
        )

    # =========================================================
    # CHALLENGE & DIALOGIC TENSION
    # =========================================================

    elif CH == 1:
        pedagogical_action = "mediate_dialogic_challenge"
        scaffold_level = "adaptive_support"

        rationale.append(
            "Challenge or disagreement detected; pedagogical mediation "
            "should sustain productive dialogic tension."
        )

    # =========================================================
    # BUILDING ON IDEAS
    # =========================================================

    elif B == 1:
        pedagogical_action = "encourage_elaboration"
        scaffold_level = "light_support"

        rationale.append(
            "Learners are building on prior contributions."
        )

    elif IB == 1:
        pedagogical_action = "invite_peer_expansion"
        scaffold_level = "moderate_support"

        rationale.append(
            "Invitation to build on ideas detected."
        )

    # =========================================================
    # INQUIRY-ORIENTED DIALOGUE
    # =========================================================

    elif II == 1:
        pedagogical_action = "support_dialogic_inquiry"
        scaffold_level = "open_inquiry_support"

        rationale.append(
            "Inquiry invitation detected; learners are engaging "
            "in exploratory or problem-posing dialogue."
        )

    # =========================================================
    # CONTEXTUAL LINKING
    # =========================================================

    elif RB == 1:
        pedagogical_action = "activate_prior_shared_knowledge"
        scaffold_level = "contextual_support"

        rationale.append(
            "Reference back detected; learners are connecting "
            "current discussion to shared prior experience."
        )

    elif RW == 1:
        pedagogical_action = "extend_to_authentic_context"
        scaffold_level = "transfer_support"

        rationale.append(
            "Reference to wider context detected; learners are linking "
            "dialogue to external knowledge or real-world contexts."
        )

    # =========================================================
    # DIALOGIC FOCUSING
    # =========================================================

    elif F == 1:
        pedagogical_action = "redirect_or_focus_discussion"
        scaffold_level = "directive_support"

        rationale.append(
            "Focusing move detected; dialogue requires conceptual "
            "or task-related guidance."
        )

    # =========================================================
    # REFLECTION & METACOGNITION
    # =========================================================

    elif RD == 1:
        pedagogical_action = "facilitate_metacognitive_reflection"
        scaffold_level = "reflective_support"

        rationale.append(
            "Metacognitive reflection on dialogue or learning detected."
        )

    # =========================================================
    # LOW DIALOGICITY / MINIMAL ENGAGEMENT
    # =========================================================

    elif cognitive_load == 0:
        pedagogical_action = "prompt_dialogic_engagement"
        scaffold_level = "high_support"

        rationale.append(
            "Low dialogic activity detected; teacher prompting required "
            "to stimulate participation and elaboration."
        )

    # =========================================================
    # DEFAULT ADAPTIVE STATE
    # =========================================================

    else:
        pedagogical_action = "acknowledge_and_continue"
        scaffold_level = "adaptive_monitoring"

        rationale.append(
            "No strong dialogic indicators detected; maintain monitoring."
        )

    # =========================================================
    # CURRICULUM ALIGNMENT (OPTIONAL)
    # =========================================================

    curriculum_alignment = None

    if curriculum:

        curriculum_alignment = {
            "learning_goal": curriculum.get("learning_goal"),
            "dialogic_alignment": True,
            "recommended_focus": pedagogical_action
        }

    # =========================================================
    # OUTPUT
    # =========================================================

    return {
        "pedagogical_action": pedagogical_action,
        "scaffold_level": scaffold_level,
        "cognitive_load": cognitive_load,
        "dialogic_profile": {
            code: value
            for code, value in features.items()
            if value == 1
        },
        "rationale": rationale,
        "curriculum_alignment": curriculum_alignment
    }
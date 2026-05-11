# app/research/tech_seda/extractor.py

from typing import Dict, List


def tech_seda_analyze(text: str, speaker: str = "student") -> Dict:

    """
    Tech-SEDA rule-based dialogic coding extractor.

    Output format:
    {
        "speaker": "student",
        "codes": ["R", "CH"],
        "raw_text": "..."
    }

    Codes:
        IB  = Invitation to build on ideas
        B   = Building on ideas
        CH  = Challenge
        IR  = Invitation for reasoning
        R   = Reasoning
        IC  = Invitation for co-ordination
        SC  = Simple co-ordination
        RC  = Reasoned co-ordination
        II  = Inquiry invitation
        RB  = Reference back
        RW  = Reference to wider context
        F   = Focusing
        RD  = Reflect on dialogue/activity
    """

    text_lower = text.lower().strip()

    codes: List[str] = []

    # ---------------------------------------------------
    # IB — Invitation to Build on Ideas
    # ---------------------------------------------------

    ib_patterns = [
        "what do you think",
        "can you explain more",
        "can you add",
        "can you build on",
        "do you agree",
        "do you disagree",
        "any other thoughts",
        "can anyone add",
        "who wants to add",
        "improve this idea",
        "comment on",
        "respond to",
        "build on"
    ]

    if any(p in text_lower for p in ib_patterns):
        codes.append("IB")

    # ---------------------------------------------------
    # B — Building on Ideas
    # ---------------------------------------------------

    b_patterns = [
        "also",
        "in addition",
        "another example",
        "building on",
        "i agree because",
        "this connects to",
        "that means",
        "for example",
        "adding to",
        "extending",
        "similar to"
    ]

    if any(p in text_lower for p in b_patterns):
        codes.append("B")

    # ---------------------------------------------------
    # CH — Challenge
    # ---------------------------------------------------

    ch_patterns = [
        "i disagree",
        "that's wrong",
        "i don't think",
        "however",
        "but",
        "are you sure",
        "why would",
        "that cannot",
        "i doubt",
        "how can",
        "really?"
    ]

    if any(p in text_lower for p in ch_patterns):
        codes.append("CH")

    # ---------------------------------------------------
    # IR — Invitation for Reasoning
    # ---------------------------------------------------

    ir_patterns = [
        "why",
        "how do you know",
        "what evidence",
        "can you justify",
        "can you explain",
        "what makes you think",
        "what is the reason",
        "how did you get",
        "can you prove",
        "what caused"
    ]

    if any(p in text_lower for p in ir_patterns):
        codes.append("IR")

    # ---------------------------------------------------
    # R — Reasoning
    # ---------------------------------------------------

    r_patterns = [
        "because",
        "therefore",
        "this means",
        "the reason is",
        "for instance",
        "for example",
        "evidence",
        "if...then",
        "so that",
        "as a result",
        "which suggests",
        "due to"
    ]

    if any(p in text_lower for p in r_patterns):
        codes.append("R")

    # ---------------------------------------------------
    # IC — Invitation for Co-ordination
    # ---------------------------------------------------

    ic_patterns = [
        "compare these",
        "summarise",
        "what conclusion",
        "how are these similar",
        "how are these different",
        "can we combine",
        "what consensus",
        "which idea is better",
        "evaluate these ideas"
    ]

    if any(p in text_lower for p in ic_patterns):
        codes.append("IC")

    # ---------------------------------------------------
    # SC — Simple Co-ordination
    # ---------------------------------------------------

    sc_patterns = [
        "both ideas",
        "in summary",
        "overall",
        "together",
        "similarly",
        "the group thinks",
        "we concluded",
        "our conclusion",
        "these ideas show"
    ]

    if any(p in text_lower for p in sc_patterns):
        codes.append("SC")

    # ---------------------------------------------------
    # RC — Reasoned Co-ordination
    # ---------------------------------------------------

    rc_patterns = [
        "on the one hand",
        "on the other hand",
        "although",
        "while",
        "even though",
        "partly true",
        "however",
        "despite",
        "a better explanation",
        "after comparing"
    ]

    if any(p in text_lower for p in rc_patterns):
        codes.append("RC")

    # ---------------------------------------------------
    # II — Inquiry Invitation
    # ---------------------------------------------------

    ii_patterns = [
        "investigate",
        "research this",
        "find out",
        "explore",
        "what questions",
        "let's inquire",
        "look into",
        "discover",
        "test this idea"
    ]

    if any(p in text_lower for p in ii_patterns):
        codes.append("II")

    # ---------------------------------------------------
    # RB — Reference Back
    # ---------------------------------------------------

    rb_patterns = [
        "last lesson",
        "previously",
        "earlier",
        "remember when",
        "before",
        "as we discussed",
        "from yesterday",
        "last time",
        "you said earlier"
    ]

    if any(p in text_lower for p in rb_patterns):
        codes.append("RB")

    # ---------------------------------------------------
    # RW — Reference to Wider Context
    # ---------------------------------------------------

    rw_patterns = [
        "in real life",
        "in society",
        "research shows",
        "scientists say",
        "outside school",
        "in the real world",
        "according to",
        "experts",
        "online",
        "in another country"
    ]

    if any(p in text_lower for p in rw_patterns):
        codes.append("RW")

    # ---------------------------------------------------
    # F — Focusing
    # ---------------------------------------------------

    f_patterns = [
        "focus on",
        "pay attention",
        "let's return",
        "the important point",
        "look carefully",
        "think about",
        "consider this",
        "stay on topic",
        "notice that"
    ]

    if any(p in text_lower for p in f_patterns):
        codes.append("F")

    # ---------------------------------------------------
    # RD — Reflect on Dialogue/Activity
    # ---------------------------------------------------

    rd_patterns = [
        "what did we learn",
        "how did your thinking change",
        "reflect on",
        "looking back",
        "i learned",
        "my understanding changed",
        "we improved",
        "this discussion helped",
        "what worked well"
    ]

    if any(p in text_lower for p in rd_patterns):
        codes.append("RD")

    # ---------------------------------------------------
    # Deduplicate codes
    # ---------------------------------------------------

    codes = list(dict.fromkeys(codes))

    # ---------------------------------------------------
    # Return structured symbolic output
    # ---------------------------------------------------

    return {
        "speaker": speaker,
        "codes": codes,
        "raw_text": text
    }
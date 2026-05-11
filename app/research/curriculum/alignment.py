def curriculum_align(text: str) -> dict:

    grade_level = "Grade 8"

    vocab_targets = ["because", "think", "important", "should"]
    grammar_targets = ["why questions", "cause-effect"]

    matched_vocab = [w for w in vocab_targets if w in text.lower()]

    return {
        "grade": grade_level,
        "vocab_match": matched_vocab,
        "alignment_score": len(matched_vocab) / len(vocab_targets)
    }
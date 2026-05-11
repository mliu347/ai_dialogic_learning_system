import time

from app.research.tech_seda.extractor import tech_seda_analyze
from app.pedagogy.scaffold import scaffold_decision

from app.memory.dialogue_memory import DialogueMemory

from app.research.ena.windowing import create_windows
from app.research.ena.ena_builder import build_cooccurrence_matrix
from app.research.ena.graph_generator import generate_graph


# ==========================================
# GLOBAL MEMORY INSTANCE
# ==========================================

memory = DialogueMemory()


# ==========================================
# MOCK LLM
# ==========================================

def call_llm(prompt: str) -> str:

    return f"[MOCK LLM RESPONSE]: {prompt}"


# ==========================================
# MAIN DIALOGUE ENGINE
# ==========================================

def generate_response(student_input: str) -> dict:

    start_time = time.time()

    # ======================================
    # 1. LLM RESPONSE
    # ======================================

    llm_output = call_llm(student_input)

    # ======================================
    # 2. TECH-SEDA ANALYSIS
    # ======================================

    analysis = tech_seda_analyze(student_input)

    # ======================================
    # 3. STORE IN MEMORY
    # ======================================

    memory.add_turn(analysis)

    # ======================================
    # 4. GET FULL CODE HISTORY
    # ======================================

    codes = memory.get_all_codes()

    # ======================================
    # 5. CREATE ENA WINDOWS
    # ======================================

    windows = create_windows(codes)

    # ======================================
    # 6. BUILD CO-OCCURRENCE MATRIX
    # ======================================

    edge_weights = build_cooccurrence_matrix(windows)

    # ======================================
    # 7. GENERATE ENA GRAPH
    # ======================================

    G = generate_graph(edge_weights)

    # ======================================
    # 8. PEDAGOGICAL DECISION
    # ======================================

    pedagogy = scaffold_decision(analysis)

    # ======================================
    # 9. FINAL OUTPUT
    # ======================================

    result = {

        "input": student_input,

        "response": llm_output,

        "analysis": analysis,

        "pedagogy": pedagogy,

        "ena": {
            "windows": windows,
            "edge_weights": dict(edge_weights),
            "num_nodes": len(G.nodes),
            "num_edges": len(G.edges)
        },

        "metadata": {
            "latency": round(time.time() - start_time, 4),
            "stage": "dialogue_engine_v3"
        }
    }

    return result
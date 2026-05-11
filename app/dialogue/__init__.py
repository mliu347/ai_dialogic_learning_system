import time

def call_llm(prompt: str) -> str:
    return f"[LLM RESPONSE]: {prompt}"


def generate_response(student_input: str) -> dict:
    start_time = time.time()

    response = call_llm(student_input)

    return {
        "input": student_input,
        "response": response,
        "latency": round(time.time() - start_time, 4)
    }
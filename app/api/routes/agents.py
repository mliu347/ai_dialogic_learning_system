from fastapi import APIRouter

router = APIRouter()

@router.post("/agents/respond")
def agent_response(input_text: str):
    return {
        "agent_reply": "I am dialogic agent responding...",
        "confidence": 0.8
    }
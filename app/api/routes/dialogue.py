from fastapi import APIRouter

router = APIRouter()

@router.post("/dialogue/generate")
def generate_dialogue(input_text: str):
    return {
        "response": f"AI response to: {input_text}",
        "tech_seda_features": []
    }
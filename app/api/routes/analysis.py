from fastapi import APIRouter

router = APIRouter()

@router.post("/analysis/tech_seda")
def analyze_dialogue(text: str):
    return {
        "features": {
            "challenge": 0.5,
            "uptake": 0.7,
            "reasoning": 0.6
        }
    }
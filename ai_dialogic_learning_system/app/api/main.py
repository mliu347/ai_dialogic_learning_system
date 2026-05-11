from fastapi import FastAPI

app = FastAPI(
    title="AI Dialogic Learning System",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "message": "AI-Mediated Dialogic Learning System Running"
    }

from fastapi import FastAPI
from app.api.routes import dialogue, agents, analysis

app = FastAPI()

app.include_router(dialogue.router)
app.include_router(agents.router)
app.include_router(analysis.router)

@app.get("/")
def root():
    return {"status": "AI Dialogic System running"}
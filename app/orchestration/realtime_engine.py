import sys
import fastapi

print(sys.executable)
print(fastapi.__version__)


from fastapi import APIRouter, WebSocket

router = APIRouter()

@router.websocket("/ws/dialogue")
async def dialogue_socket(websocket: WebSocket):

    await websocket.accept()

    while True:

        student_text = await websocket.receive_text()

        response = engine.process(student_text)

        await websocket.send_text(response["response"])
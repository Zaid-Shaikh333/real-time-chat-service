from fastapi import FastAPI, WebSocket
from pydantic import BaseModel
import json

app = FastAPI()

class Message(BaseModel):
    sender: str
    message: str

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            try:
                parsed_data = json.loads(data) 
                message = Message(**parsed_data)
                await websocket.send_text(f"Message from {message.sender}: {message.message}")
            except Exception as e:
                await websocket.send_text(f"Invalid message format: {str(e)}")
    except Exception:
        pass

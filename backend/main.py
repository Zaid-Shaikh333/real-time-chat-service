from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List

app = FastAPI()

active_connections: List[WebSocket] = []

class Message(BaseModel):
    sender: str
    message: str

@app.get("/")
def read_root():
    return {"message": "Backend is running"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        active_connections.add(websocket)
        while True:
            data = await websocket.receive_json()
            parsed_data = Message(**data)
            for connection in active_connections:
                await connection.send_json(parsed_data.dict())
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        await websocket.close()
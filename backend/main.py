from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

active_connections = set()

@app.get("/")
def read_root():
    return {"message": "Backend is running"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        active_connections.add(websocket)
        while True:
            data = await websocket.receive_text()
            for connection in active_connections:
                await connection.send_text(data)
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        await websocket.close()
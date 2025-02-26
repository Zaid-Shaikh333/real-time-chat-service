import asyncio
import websockets
import json

async def test_websocket():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        message = json.dumps({"sender": "Zaid", "message": "Hello from Python WebSocket!"})
        await websocket.send(message)
        response = await websocket.recv()
        print(f"Response: {response}")

asyncio.run(test_websocket())

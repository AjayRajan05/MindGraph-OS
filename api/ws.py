from fastapi import APIRouter, WebSocket

router = APIRouter()

clients = []

@router.websocket("/ws")

async def websocket_endpoint(ws: WebSocket):

    await ws.accept()

    clients.append(ws)

    while True:
        await ws.receive_text()

async def notify_clients(message):

    for c in clients:
        await c.send_json(message)
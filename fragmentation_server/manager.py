import asyncio
import os
from starlette.websockets import WebSocket
from dotenv import load_dotenv
import websockets
import json

load_dotenv()


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, server_ip: str):
        await websocket.accept()
        self.active_connections[server_ip] = websocket

    def disconnect(self, server_ip: str):
        if server_ip in self.active_connections:
            del self.active_connections[server_ip]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send(message)

    async def connect_to_external_ws(self, destination_ip: str, server_ip: str):
        url = f"ws://{destination_ip}:8000/ws/{server_ip}"

        external_ws = await websockets.connect(url, timeout=60)
        self.active_connections[server_ip] = external_ws
        print(f"Connected to external WebSocket at {url}")
        print(dir(external_ws))
        return external_ws

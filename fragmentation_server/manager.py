import websockets
from starlette.websockets import WebSocket
from websockets import WebSocketClientProtocol


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, server_ip: str):
        await websocket.accept()
        self.active_connections[server_ip] = websocket

    async def disconnect(self, server_ip: str = ""):
        websocket = self.active_connections[server_ip]
        await websocket.close()
        del self.active_connections[server_ip]

    @staticmethod
    async def send_personal_message(message: str, websocket: WebSocket):
        if isinstance(websocket, WebSocketClientProtocol):
            await websocket.send(message)
        else:
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            if isinstance(connection, WebSocketClientProtocol):
                await connection.send(message)
            else:
                await connection.send_text(message)

    async def connect_to_external_ws(self, destination_ip: str, server_ip: str, port: int = 8000):
        url = f"ws://{destination_ip}:{port}/ws/{server_ip}"

        external_ws = await websockets.connect(url)
        self.active_connections[server_ip] = external_ws
        print(f"Connected to external WebSocket at {url}")
        return external_ws

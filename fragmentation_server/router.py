from dotenv import load_dotenv
from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from .manager import ConnectionManager
import os
import json


load_dotenv()
router = APIRouter()
manager = ConnectionManager()


async def handle_command(command: dict, websocket: WebSocket):
    if command["command"] == "Check files":
        response = {
            "type": "fragmentation",
            "status": "end checking files",
            "File transferred": True
        }
        await manager.send_personal_message(f"{json.dumps(response)}", websocket)
    elif command["command"] == "Start fragmentation":
        response = {
            "type": "fragmentation",
            "status": "end fragmentation"
        }
        await manager.send_personal_message(f"{json.dumps(response)}", websocket)
    elif command["command"] == "Send files to fragments server":
        response = {
            "type": "fragmentation",
            "status": "end transferring files",
            "film list": [" "],
            "destination_ip": command["destination_ip"]
        }
        await manager.send_personal_message(f"{json.dumps(response)}", websocket)


#бляяяяяяяяяяяяяяяяяя


# @router.websocket("/ws/{server_ip}")
# async def websocket_endpoint(websocket: WebSocket, server_ip: str):
#     await manager.connect(websocket, server_ip)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             command = json.loads(data)
#             await handle_command(command, websocket)
#     except Exception as e:
#         print(f"Error: {e}")
#     finally:
#         await manager.disconnect(server_ip)


@router.get("/trigger_websocket_connection")
async def trigger_websocket_connection():
    websocket = await manager.connect_to_external_ws(os.getenv("DESTINATION_IP"), os.getenv("MY_IP"), 8000)
    manager.active_connections[os.getenv("DESTINATION_IP")] = websocket
    response = {
        "type": "fragmentation",
        "status": "waiting for films"
    }

    await manager.send_personal_message(f"{response}", websocket)
    try:
        while True:
            data = await websocket.recv()
            data = data.replace("'", '"')
            print(data)
            command = json.loads(data)
            await handle_command(command, websocket)
            print(f"Client #{os.getenv('DESTINATION_IP')} says {data}")
    except WebSocketDisconnect:
        await manager.disconnect(os.getenv("DESTINATION_IP"))
        print(f"Client #{os.getenv('DESTINATION_IP')} left the websocket connection")
from fastapi import APIRouter, WebSocket
from .manager import ConnectionManager
import os
import json

router = APIRouter()
manager = ConnectionManager()


async def handle_command(command: dict, websocket: WebSocket):
    if command["command"] == "Check files":
        response = {
            "type": "fragmentation",
            "status": "waiting for films"
        }
        await manager.send_personal_message(response, websocket)
    elif command["command"] == "Start fragmentation":
        response = {
            "type": "fragmentation",
            "status": "end checking files",
            "File transferred": True
        }
        await manager.send_personal_message(response, websocket)
    elif command["command"] == "Send files to fragments server":
        response = {
            "type": "fragmentation",
            "status": "end fragmentation"
        }
        await manager.send_personal_message(response, websocket)
    elif command["command"] == "Send files fragmentation":
        response = {
            "type": "fragmentation",
            "status": "end transferring files",
            "film list": [" "],
            "destination_ip": os.getenv("DESTINATION_IP")
        }
        await manager.send_personal_message(response, websocket)

#бляяяяяяяяяяяяяяяяяя


@router.websocket("/ws/{server_ip}")
async def websocket_endpoint(websocket: WebSocket, server_ip: str):
    await manager.connect(websocket, server_ip)
    try:
        while True:
            data = await websocket.receive_text()
            command = json.loads(data)
            await handle_command(command, websocket)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        manager.disconnect(server_ip)


@router.get("/trigger_websocket_connection")
async def trigger_websocket_connection():
    destination_ip = os.getenv("DESTINATION_IP")
    server_ip = os.getenv("SERVER_IP")
    print(f"Connecting to {destination_ip} from {server_ip}")
    websocket = await manager.connect_to_external_ws(os.getenv("DESTINATION_IP"), os.getenv("SERVER_IP"))
    manager.active_connections["DESTINATION_IP"] = websocket
    response = {
        "type": "fragmentation",
        "status": "waiting for films"
    }

    await manager.send_personal_message(f"{response}", websocket)
    try:
        while True:
            data = await websocket.receive_text()
            print(data)
            command = json.loads(data)
            await handle_command(command, websocket)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        manager.disconnect(server_ip)
# manager.py - handles websocket connections for chat
from typing import List, Dict
from fastapi import WebSocket

# this class keeps track of all active connections
class ConnectionManager:
    def __init__(self):
        # store connections like: { room_id: [ws1, ws2] }
        self.active_connections: Dict[int, List[WebSocket]] = {}

    # when user connects to a room
    async def connect(self, websocket: WebSocket, room_id: int):
        await websocket.accept()
        # if room not present, create it
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        # add user connection to room
        self.active_connections[room_id].append(websocket)

    # when user disconnects
    def disconnect(self, websocket: WebSocket, room_id: int):
        if room_id in self.active_connections:
            if websocket in self.active_connections[room_id]:
                self.active_connections[room_id].remove(websocket)
            # if no users left in room, remove the room
            if not self.active_connections[room_id]:
                del self.active_connections[room_id]

    # send message to all users in same room
    async def broadcast(self, message: dict, room_id: int):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_json(message)

# create one global manager to use everywhere
manager = ConnectionManager()
import asyncio
from fastapi import WebSocket
from typing import List, Dict
from Service.common.data.user_data import UserData

# WebSocketManager to manage WebSocket connections and store user-specific data
class WebSocketManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []  # List of active connections
        self.user_queues: Dict[WebSocket, asyncio.Queue] = {}  # Mapping of WebSocket to receive queues
        self.user_data: Dict[WebSocket, UserData] = {}  # Mapping of WebSocket to user data

    async def connect(self, websocket: WebSocket):
        """Accept a new WebSocket connection and associate a queue and user data."""
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_queues[websocket] = asyncio.Queue()  # Queue for receiving data
        self.user_data[websocket] = UserData()  # Initialize user data for processing

    def disconnect(self, websocket: WebSocket):
        """Remove a WebSocket connection and its associated resources."""
        self.active_connections.remove(websocket)
        del self.user_queues[websocket]  # Remove the receiving queue
        del self.user_data[websocket]  # Remove user-specific data

    def get_user_queue(self, websocket: WebSocket) -> asyncio.Queue:
        """Return the queue for receiving data for a specific WebSocket."""
        return self.user_queues.get(websocket)

    def get_user_data(self, websocket: WebSocket) -> UserData:
        """Return the user data (buffer, pointer, etc.) for a specific WebSocket."""
        return self.user_data.get(websocket)

    async def send_personal_message(self, websocket: WebSocket, message: str):
        """Send a message to a specific WebSocket."""
        await websocket.send_json(message)


# Create the WebSocket manager instance
websocket_manager = WebSocketManager()
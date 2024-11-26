import logging
from fastapi import WebSocket
from Service.common.data.websockets_managment import websocket_manager


def handle_disconnection(websocket: WebSocket):
    """
    Handle the disconnection of a WebSocket client.

    This function removes the specified WebSocket connection from the
    active connections set and logs the disconnection event.

    Parameters:
        websocket (WebSocket): The WebSocket instance representing the 
        client that has disconnected.

    Returns:
        None
    """
    # websocket_manager.websockets.remove(websocket)
    logging.info(f"Client disconnected")
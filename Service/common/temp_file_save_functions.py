import os
import tempfile
from fastapi import WebSocket
import logging
from typing import Optional
from Service.common.data.websockets_managment import websocket_manager

def save_temp_audio_file(data: bytes, save_to_path: Optional[str] = None, online_streaming_path: Optional[str] = None, online_correction_path: Optional[str] = None) -> Optional[str]:
    """
    Save audio data to a temporary WAV file.

    This function creates a temporary file to store audio data. If a path is provided,
    it will save the file in the specified directory; otherwise, it will use the default
    temporary directory.

    Args:
        data (bytes): The audio data to be saved.
        save_to_path (Optional[str]): The directory path where the file should be saved.
                                       If None, the file will be saved in the default
                                       temporary directory.

    Returns:
        Optional[str]: The path to the saved temporary file, or None if an error occurred.
    """
    try:
        if save_to_path:
            # Ensure the entire directory structure exists
            full_dir_path = os.path.dirname(save_to_path)
            os.makedirs(full_dir_path, exist_ok=True)

            # Create a temporary file in the specified directory
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir=full_dir_path) as temp_file:
                temp_file.write(data)
                return temp_file.name
        elif online_correction_path:
            # Ensure the entire directory structure exists
            online_corr_path = os.path.dirname(online_correction_path)
            os.makedirs(online_corr_path, exist_ok=True)
            # Create a temporary file in the default temp directory
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir = online_corr_path) as temp_file:
                temp_file.write(data)
                return temp_file.name
        elif online_streaming_path:
            # Ensure the entire directory structure exists
            online_str_path = os.path.dirname(online_streaming_path)
            os.makedirs(online_str_path, exist_ok=True)
            # Create a temporary file in the default temp directory
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir = online_str_path) as temp_file:
                temp_file.write(data)
                return temp_file.name
    except Exception as e:
        logging.error(f"Failed to save temporary file: {e}")
        return None

async def send_transcription_to_clients(message: str, source: str, websocket: WebSocket):
    """
    Send a transcription message to all connected clients via WebSocket.

    This function structures the message and sends it to each WebSocket client that is connected.

    Args:
        message (str): The transcription message to send.
        source (str): The source of the transcription message (e.g., "Instant Transcription").
    """
    structured_message = {
        "source": source,
        "content": message
    }

    await websocket_manager.send_personal_message(websocket, structured_message)

async def send_corrected_transcription_to_clients(message: list[str], source: str, websocket,indexing_pointer_position:int = 0, final_sentence_pointer_position: int = 0, new_sentence_indexing_pointer: int = 0):
    """
    Send corrected transcription messages to all connected clients.

    This function structures the corrected transcription message with additional indexing information
    and sends it to each WebSocket client that is connected.

    Args:
        message (list[str]): The list of corrected transcription messages to send.
        source (str): The source of the corrected transcription message (e.g., "Final Transcription").
        indexing_pointer_position (int): The current indexing pointer position for the transcription.
        final_sentence_pointer_position (int): The final position of the sentence in the transcription.
    """
    structured_message = {
        "source": source,
        "content": message,
        "indexing_pointer_position":indexing_pointer_position,
        "final_sentence_pointer_position":final_sentence_pointer_position,
        "new_sentence_indexing_pointer": new_sentence_indexing_pointer
        
    }
    # print("Instant Message", structured_message,"Index: " ,index)

    await websocket_manager.send_personal_message(websocket, structured_message)

async def remove_temp_file(file_path: str):
    """
    Remove a temporary file from the filesystem.

    This function attempts to delete a specified file and logs an error if the deletion fails.

    Args:
        file_path (str): The path to the file to be deleted.
    """
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
        except Exception as e:
            logging.error(f"Failed to remove temporary file: {e}")
import logging
import asyncio
import time
import numpy as np
from fastapi import WebSocket, WebSocketDisconnect
from Service.common.data.websockets_managment import websocket_manager
from Service.common.audio_transcription_processor import process_transcription_offline
from Service.common.audio_transcription_processor import AudioProcessor
from Service.logging.logging import logger
from Service.common.data.context_logic import ContextLogic
from Service.common.temp_file_save_functions import *
from Service.config import *

async def transcription_logic(websocket: WebSocket):
    logger.info(f"New WebSocket connection from {websocket.client}")
    await websocket_manager.connect(websocket)
    audio_processor = AudioProcessor(websocket)
    logger.info(f"WebSocket connected: {websocket.client}")
    try:
        while True:
            data = await websocket.receive_bytes()
            logger.info(f"Received {len(data)} bytes of audio data from {websocket.client}")
            await websocket_manager.get_user_queue(websocket).put(data)
            asyncio.create_task(audio_processor.process_audio_queue())      
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
    
    except Exception as e:
        logging.error(f"WebSocket error: {e}")
        await websocket.close()

async def create_context_logic(audio_url: str) -> ContextLogic:
    try:
        url='https://112.124.48.213:443/file/audio/12345_abcde_ABCDE.wav'
        start_time = time.time()
        summarized_message = await process_transcription_offline(url)
        end_time = start_time - time.time()
        print(f"Total Time: {end_time}")
        return ContextLogic(summarized_message =summarized_message.message, subject_conversation = summarized_message.subject_conversation)
    except Exception as e:
        logger.error(f"Error in create_context_logic: {e}", exc_info=True)
        return ContextLogic(summarized_message ="Error generation Message", subject_conversation = "Error generation Subject Conversation")
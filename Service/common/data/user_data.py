import asyncio
from Service.common.data.audio_buffer import AudioBuffer
from Service.common.data.pointers_position import PointerPosition
from Service.common.data.transcribed_text_store import TranscribedTextStore
from Service.common.data.buffer_length import BufferLength

class UserData:
    def __init__(self):
        self.audio_buffer = AudioBuffer()  # Stores audio buffer for processing
        self.buffer_length = BufferLength()  # Stores buffer length information
        self.pointer_info = PointerPosition()  # Stores pointer positions
        self.transcribed_text  = TranscribedTextStore()  # Stores transcribed text
        self.buffer_processing_queue = asyncio.Queue()  # Separate queue for audio buffer processing
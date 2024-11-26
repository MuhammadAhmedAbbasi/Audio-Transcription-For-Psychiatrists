from pydantic import BaseModel

class BufferLength(BaseModel):
    """
    A class to represent the configuration of audio buffer lengths.

    Attributes:
        minimum_stored_buffer_length (int): The minimum length of the stored audio buffer (default is 4).
        maximum_stored_buffer_length (int): The maximum length of the stored audio buffer (default is 6).
        audio_chunk_start_index (int): The starting index for the audio chunk (default is 0).
        audio_chunk_end_index (int): The ending index for the audio chunk (default is 4).
    """
    minimum_stored_buffer_length: int = 4
    maximum_stored_buffer_length: int = 6
    audio_chunk_start_index: int = 0
    audio_chunk_end_index: int = 4

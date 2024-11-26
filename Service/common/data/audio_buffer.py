from asyncio.queues import Queue
class AudioBuffer:
    """
    A class to handle audio data storage and processing within different contexts.

    Attributes:
    -----------
    audio_for_context_store : bytearray
        Stores audio data for context processing and analysis.
    
    transcription_correction_audio_store : bytearray
        Stores audio data specifically used for transcription correction purposes.
    
    saved_audio_data : list
        A list to store references to or data of previously saved audio data for future retrieval.
    """
    
    def __init__(self):
        self.audio_for_context_store: bytearray = bytearray()
        self.transcription_correction_audio_store: bytearray = bytearray()
        self.saved_audio_data: list = []
        

# Creating an instance of the AudioBuffer class
audio_buffer_instance = AudioBuffer()

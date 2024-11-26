from pydantic import BaseModel
from typing import Optional

class AudioModels(BaseModel):
    """
    A class to represent audio models used for various processing tasks.

    Attributes:
        non_streaming_model (Optional[None]): A model for processing audio in a non-streaming manner.
        streaming_model (Optional[None]): A model for processing audio in a streaming manner.
        full_transcription_model (Optional[None]): A model for providing full transcription of audio input.
    """
    non_streaming_model: Optional[None] = None
    streaming_model: Optional[None] = None
    full_transcription_model: Optional[None] = None

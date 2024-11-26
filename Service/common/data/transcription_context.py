from pydantic import BaseModel

class TranscriptionContext(BaseModel):
    """
    A class to represent the context of a transcription.

    Attributes:
        transcription (str): The transcription text, which can be an empty string by default.
    """
    transcription: str = ''

# Creating an instance of TranscriptionContext
transcription_context = TranscriptionContext()

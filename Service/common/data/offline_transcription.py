from pydantic import BaseModel
from typing import List

class OfflineTranscription(BaseModel):
    """
    A class to represent offline transcription data.

    Attributes:
        message (str): The transcription message or text.
        subject_conversation (List[str]): A list of strings representing the subjects of the conversation.
    """
    message: str
    subject_conversation: List[str]

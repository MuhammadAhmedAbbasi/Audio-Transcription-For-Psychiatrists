from pydantic import BaseModel
from typing import List

class TranscribedTextStore(BaseModel):
    """
    A class to store and manage transcribed text messages.

    Attributes:
        old_message (List[str]): A list of strings representing previously transcribed messages.
        new_message (List[str]): A list of strings representing newly transcribed messages.
        total_message (List[str]): A list of strings representing all transcribed messages,
        combining both old and new messages.
    """
    old_message: List[str] = []
    new_message: List[str] = []
    total_message: List[str] = []

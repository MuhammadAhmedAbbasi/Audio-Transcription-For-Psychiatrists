from pydantic import BaseModel
from typing import List

class ContextLogic(BaseModel):
    summarized_message: str
    subject_conversation: List[str]
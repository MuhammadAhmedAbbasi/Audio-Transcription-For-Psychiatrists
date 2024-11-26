from pydantic import BaseModel
from typing import List

class ContextResponse(BaseModel):
    Summarized_message: str
    response_text: List[str]

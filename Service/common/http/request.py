from pydantic import BaseModel
from typing import List

class Request(BaseModel):
    query: str
    context:str
    prompt: str
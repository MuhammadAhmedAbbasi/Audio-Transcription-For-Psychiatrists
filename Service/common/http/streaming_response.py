from pydantic import BaseModel

class StreamingResponse(BaseModel):
    streaming_response: str
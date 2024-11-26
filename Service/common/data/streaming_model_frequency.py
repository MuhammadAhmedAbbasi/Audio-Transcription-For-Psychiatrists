from pydantic import BaseModel

class StreamingModelFrequency(BaseModel):
    """
    A class to represent frequency settings for a streaming model.

    Attributes:
        low_freq (int): The lower frequency limit for the streaming model in Hertz (default is 350 Hz).
        high_freq (int): The upper frequency limit for the streaming model in Hertz (default is 3500 Hz).
    """
    low_freq: int = 350
    high_freq: int = 3500

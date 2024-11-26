from pydantic import BaseModel

class FrequencySettings(BaseModel):
    low_frequency: int = 400
    high_frequency: int = 3400
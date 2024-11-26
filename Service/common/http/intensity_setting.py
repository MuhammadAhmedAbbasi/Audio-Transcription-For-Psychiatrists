from pydantic import BaseModel

class IntensitySetting(BaseModel):
    intensity_value: float = 3.0
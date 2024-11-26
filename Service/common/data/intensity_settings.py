from pydantic import BaseModel

class IntensitySettings(BaseModel):
    """
    A class to represent settings for intensity levels.

    Attributes:
        intensity_value (float): The intensity value, which represents the level of intensity 
        (default is 0).
    """
    intensity_value: float = 3.0

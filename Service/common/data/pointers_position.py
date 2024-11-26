from pydantic import BaseModel

class PointerPosition(BaseModel):
    """
    A class to represent the position of a pointer in a given context.

    Attributes:
        total_pointer_position (int): The total position of the pointer, indicating its
        overall location (default is 0).
        indexed_pointer_position (int): The indexed position of the pointer, representing its 
        specific index in a sequence (default is 0).
    """
    total_pointer_position: int = 0
    indexed_pointer_position: int = 0

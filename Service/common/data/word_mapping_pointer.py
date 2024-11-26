from pydantic import BaseModel

class WordMappingPointer(BaseModel):
    """
    A class to represent pointers for word mapping between text chunks.

    Attributes:
        old_chunk_unmapped_pointer (int): The pointer indicating the position in the 
        old chunk that has not yet been mapped.
        new_chunk_unmapped_pointer (int): The pointer indicating the position in the 
        new chunk that has not yet been mapped.
    """
    old_chunk_unmapped_pointer: int
    new_chunk_unmapped_pointer: int

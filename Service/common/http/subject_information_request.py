from pydantic import BaseModel

class SubjectInformationRequest(BaseModel):
    subject_id: str
    subject_name: str
    subject_age: int
    subject_gender: str
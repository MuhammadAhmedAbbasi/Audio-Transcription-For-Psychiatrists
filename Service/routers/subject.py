import logging

from fastapi import APIRouter
from Service.common.http.subject_information_request import SubjectInformationRequest
from Service.common.data.student_info import StudentInfo
from Service.services.subject_information_service import subject_info_logic


student_information = StudentInfo()
router = APIRouter()

@router.post("/subject-information", response_model=SubjectInformationRequest)
async def student_info(info: SubjectInformationRequest):
    await subject_info_logic(info)
    return info

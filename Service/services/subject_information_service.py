import logging

from Service.common.http.subject_information_request import SubjectInformationRequest
from Service.common.data.student_info import StudentInfo

student_information = StudentInfo()

async def subject_info_logic(info: SubjectInformationRequest):
    student_information.id = info.subject_id
    logging.info(f"Received student info: {info.subject_id}")
    student_information.data[student_information.id] = {
        "Student Name": info.subject_name,
        "Student Age": info.subject_age,
        "Student Gender": info.subject_gender,
    }
    return None
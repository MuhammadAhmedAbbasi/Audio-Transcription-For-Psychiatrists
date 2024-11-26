from fastapi import APIRouter
from Service.common.http.request import Request
from Service.common.http.response import Response
from Service.services.chatbot_service import chatbot_service_logic

router = APIRouter()

@router.post("/chatbot", response_model=Response)
async def chat_model(request: Request):
    try:
        answer = await chatbot_service_logic(request)
        return Response(response=answer)
    except:
        return Response(response="Error in chatbot api")

from langchain_core.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatZhipuAI

from Service.config import *
from Service.api_key import *
from Service.common.http.response import Response
from typing import List

def chatbot(query: str, context: str, prompt: str) -> str:
    # Initialize the ChatZhipuAI model
    chat_model = ChatZhipuAI(
        model=chatbot_model,
        temperature=temprature,
    )
    prompt = ChatPromptTemplate.from_template(template = prompt)
    formatted_prompt = prompt.format(context=context, input=query)
    # Get the response from the chatbot
    response = chat_model.invoke(formatted_prompt)
    
    return response.content

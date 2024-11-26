import os
import sys
import asyncio
from typing import Set

from funasr import AutoModel
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from Service.routers import audio, chatbot, subject, audio_settings
from Service.common.audio_transcription_processor import *
from Service.common.data.audio_models import AudioModels
from Service.common.data.intensity_settings import IntensitySettings  
from Service.config import *

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))

app = FastAPI()

app.include_router(audio.router)
app.include_router(chatbot.router)
app.include_router(subject.router)
app.include_router(audio_settings.router)

@app.get("/")
async def get():
    demo_html = os.path.join(os.path.dirname(os.path.abspath(__file__)), "demo.html")
    with open(demo_html, encoding="utf-8") as file:
        content = file.read()
    return HTMLResponse(content)

# 其他启动和事件处理逻辑

# Start audio queue processing on startup
@app.on_event("startup")
async def startup_event():
    AudioModels.streaming_model = AutoModel(model=streaming_model, model_revision=streaming_model_revision)

    AudioModels.non_streaming_model = AutoModel(model=non_streaming_model,kwargs=kwargs, 
                                                vad_model=vad_model, vad_kwargs=vad_kwargs,spk_model=spk_model, 
                                                     spk_model_revision=spk_model_revision,punc_model =punc_model)
    
    AudioModels.full_transcription_model = AutoModel(model=non_streaming_model,kwargs=kwargs,punc_model =punc_model, vad_model=vad_model, 
                                                     vad_kwargs=vad_kwargs,spk_model=spk_model, 
                                                     spk_model_revision=spk_model_revision)
    IntensitySettings.intensity_value = 0.0
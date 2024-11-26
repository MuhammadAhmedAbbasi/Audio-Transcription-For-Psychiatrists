from fastapi import APIRouter
from Service.common.http.frequency_setting import FrequencySettings
from Service.common.data.streaming_model_frequency import StreamingModelFrequency
import logging

from Service.common.http.intensity_setting import IntensitySetting
from Service.common.data.intensity_settings import IntensitySettings

router = APIRouter(prefix="/audio-setting", tags=["AudioSetting"])

@router.post("/frequency")
async def set_frequency(settings: FrequencySettings):
    
    StreamingModelFrequency.low_freq = settings.low_frequency
    StreamingModelFrequency.high_freq = settings.high_frequency
    logging.info(f"Low Freq Range: {settings.low_frequency}, High Freq Range: {settings.high_frequency} ")

@router.post("/intensity")
async def set_frequency(settings: IntensitySetting):
     IntensitySettings.intensity_value = settings.intensity_value
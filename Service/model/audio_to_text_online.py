import librosa
import logging
from funasr import AutoModel
from pydub import AudioSegment
import scipy.signal
import numpy as np
from Service.config import *
from Service.common.noise_filter import *
from Service.common.data.streaming_model_frequency import StreamingModelFrequency
from Service.common.http.streaming_response import StreamingResponse

# Apply the band-pass filter

def audio_to_text_model_online(audio_file_path,model: AutoModel) -> StreamingResponse:
    try:
        transcribed_text = []
        cache = {}
        logging.info("Trying Librosa")
        speech, sampling_rate = librosa.load(audio_file_path, sr=None)
        logging.info("Audio Loaded")
        speech = librosa.resample(speech, orig_sr=sampling_rate, target_sr=model_sampling_rate)

        # Set your low and high cut-off frequencies (in Hz)
        lowcut = StreamingModelFrequency.low_freq
        highcut = StreamingModelFrequency.high_freq
        
        # Apply the band-pass filter
        filtered_speech = bandpass_filter(speech, lowcut, highcut, model_sampling_rate)
        chunk_stride = audio_data_processed_partition[1] * Samples_in_one_second  
        total_chunk_num = int(len((filtered_speech) - 1) / chunk_stride + 1)

        for i in range(total_chunk_num):
            speech_chunk = filtered_speech[i * chunk_stride:(i + 1) * chunk_stride]
            is_final = i == total_chunk_num - 1
            res = model.generate(input=speech_chunk, cache=cache, is_final=is_final, chunk_size=audio_data_processed_partition,
                                encoder_chunk_look_back=encoder_chunk_look_back,
                                decoder_chunk_look_back=decoder_chunk_look_back)
            for entry in res:
                text = entry['text']
                filtered_text = ' '.join([word for word in text.split() if word not in selected_stopwords])
                transcribed_text.append(filtered_text)

        # Post-process the transcription
        text = ''.join(transcribed_text)
        # Return the transcription
        return StreamingResponse(streaming_response = text)

    except Exception as e:
        print(f"An error occurred: {e}")
        return " "
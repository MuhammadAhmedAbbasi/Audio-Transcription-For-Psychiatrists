import os
import json

# 获取当前文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(current_dir, 'config.json')

with open(config_path, encoding = "utf-8") as f:
    confrigations = json.load(f)


chatbot_confrigations = confrigations['chatbot_confrigations']
audio_to_text_transcriber = confrigations['audio_to_text_transcriber']
database_information = confrigations['database_information']
streaming_configrations = audio_to_text_transcriber['streaming_configrations']

# ChatBot Confrigations
chatbot_model = chatbot_confrigations['model'] # Name code for other models: glm-4-plus, glm-4-0520, glm-4, glm-4-air, glm-4-airx, glm-4-long, glm-4-flash
temprature = chatbot_confrigations['temprature']
text_speaker_identification = chatbot_confrigations['text_speaker_identification']

# Audio Transcription Confrigations(Streaming)
streaming_model = audio_to_text_transcriber['streaming_model']
streaming_model_revision = audio_to_text_transcriber['streaming_model_revision']
audio_data_processed_partition = streaming_configrations['audio_data_processed_partition']
encoder_chunk_look_back = streaming_configrations['encoder_chunk_look_back']
decoder_chunk_look_back = streaming_configrations['decoder_chunk_look_back']
Samples_in_one_second = streaming_configrations['Samples_in_one_second']
selected_stopwords = streaming_configrations['stopwords']
online_streaming_files = audio_to_text_transcriber['online_streaming_files']

# Audio Transcription Confrigations(Non-Streaming)
non_streaming_audio_gathering_time = audio_to_text_transcriber['non_streaming_audio_gathering_time']
non_streaming_model = audio_to_text_transcriber['non_streaming_model']
kwargs = audio_to_text_transcriber['kwargs']
online_correction_files = audio_to_text_transcriber['online_correction_files']

# Audio Transcription Confrigations(Other)
model_sampling_rate = audio_to_text_transcriber['model_sampling_rate']
audio_transcription_files = audio_to_text_transcriber['Audio_transcription_files']
vad_model = audio_to_text_transcriber['vad_model']
vad_kwargs = audio_to_text_transcriber['vad_kwargs']
punc_model = audio_to_text_transcriber['punc_model']
spk_model = audio_to_text_transcriber['spk_model']
spk_model_revision = audio_to_text_transcriber['spk_model_revision']

# Database Info Confrigations
client_uri = database_information['client_uri']
database_name = database_information['database_name']
collection = database_information['collection']
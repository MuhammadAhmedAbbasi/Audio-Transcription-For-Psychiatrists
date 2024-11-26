# Backend-Algorithm-LLM

Python version: Python 3.12.2

There are Two main Models Running
1) Audio Transcription
2) Text Generation

**1) Audio Transcritption Model**
   a) Paraformer-zh (Non Streaming) --> Correction and offline Subject Identification. 
   b) Parafomer-zh (Streaming) --> Real Time Transcription

Download Link: https://huggingface.co/funasr/paraformer-zh

**2) Text Generation Model(Question answering Chatbot):**

 Zhipu AI: [ZHIPU AI OPEN PLATFORM (bigmodel.cn)](https://bigmodel.cn/dev/howuse/model)

How to Run Fast Api Service (DEMO):
   uvicorn Service.main:app --reload


**Confrigation Settings:**

**1) ChatBot Confrigations:**

   a) **Model**: Model used for question answering
   
   b) **Temprature**: Tell how much model deviate from original question context, 1 mean greater deviation while 0 is no deviation
   
   c) **session_kwargs**: Those words which if present in the context provided to model than it will answer the question if not present then it will not response
   
   d) **session_specific_prompt**, generic_non_session_prompt, text_speaker_identification: These are the prompt according to which model can behave 

**2) Audio Transcriber Settings:**
   a) **streaming_model**, non_streaming_model: Names of main model used to transcription
   
   b)**streaming_model_revision**: The version of model used, change if new version come
   
   c)**streaming_configrations**: Model standard confrigations, for these detailed analysis visit website: https://modelscope.cn/models/iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-online/summary
   
   d) **kwargs**: device: cpu or cuda
   
   e)**vad_model**: To identify the starting and ending point of audio and also give time stamps
   
   f)**vad_kwargs**: max_single_segment_time: it tells how much audio can be given to paraformer at one time
   
   g) **punc_model**: correct the punctuation
   
   h)**spk_model**: Subject Identification
   
   I)**Audio_transcription_files**, online_streaming_files, online_correction_files: Files to store the temporary audio files
   
   j) **model_sampling_rate**: Model accepted Sampling rate 

**3) Docker Uploading Issue:**
When uploading on docker usually soundfile or librosa give error of ffmpeg, this is due to missing library which cannot be installed through docker-requirement file. After creating the docker image and running container, following linux commands are used to download

**docker exec -it <container_id_or_name> /bin/bash**

After entering the container, write following command

**apt-get update && \
apt-get install -y ffmpeg && \
apt-get clean && \
rm -rf /var/lib/apt/lists/***

**Chinese Language******

**Python 版本: Python 3.12.2**

有两个主要模型运行：

音频转录
文本生成
**1) 音频转录模型**

 a) Paraformer-zh（非流式）--> 校正和离线主题识别。
 
 b) Paraformer-zh（流式）--> 实时转录。

下载链接: https://huggingface.co/funasr/paraformer-zh

**2) 文本生成模型（问答聊天机器人）**

Zhipu AI: ZHIPU AI 开放平台 (bigmodel.cn)

**如何运行 FastAPI 服务（演示）:**

uvicorn Service.main:app --reload

**配置设置：**

1) 聊天机器人配置：

a) **模型**: 用于问答的模型

b) **温度**: 指示模型在回答问题时的偏差程度，1表示较大偏差，而0表示没有偏差。

c) **session_kwargs**: 如果上下文中包含这些词，模型将回答问题；否则将不会响应。

d) **session_specific_prompt, generic_non_session_prompt, text_speaker_identificatio**n: 根据这些提示，模型的行为会有所不同。

2) **音频转录器设置**：

 a) **streaming_model, non_streaming_model:** 用于转录的主要模型名称。

b) **streaming_model_revision**: 使用的模型版本，如有新版本可更改。

c) **streaming_configrations**: 模型标准配置，详细分析请访问：模型信息。

d) **kwargs**: 设备：cpu 或 cuda。

e) **vad_model**: 用于识别音频的起始和结束点，并提供时间戳。

f) **vad_kwargs**: max_single_segment_time: 指定一次性提供给 Paraformer 的最大音频时长。

g) **punc_model**: 修正标点符号。

h) **spk_model**: 主题识别。

i) **Audio_transcription_files**, **online_streaming_files**, **online_correction_files**: 存储临时音频文件的文件。

j) **model_sampling_rate**: 模型接受的采样率。

**3) Docker 上传问题：**

 在 Docker 中上传时，通常 soundfile 或 librosa 会出现 ffmpeg 的错误，这是由于缺少无法通过 Docker 需求文件安装的库。创建 Docker 镜像并运行容器后，使用以下 Linux 命令进行下载：

**docker exec -it <container_id_or_name> /bin/bash**

进入容器后，输入以下命令：

**apt-get update && \
apt-get install -y ffmpeg && \
apt-get clean && \
rm -rf /var/lib/apt/lists/**

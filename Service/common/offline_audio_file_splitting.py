import numpy as np

from funasr import AutoModel
from Service.config import model_sampling_rate
from funasr.utils.postprocess_utils import rich_transcription_postprocess


def text_generator(model: AutoModel, audio_sample):
    """
    Generate text transcription from an audio sample using the specified model.

    This function takes an audio sample and generates its text transcription
    using the provided AutoModel instance. It leverages various options
    for transcription generation.

    Parameters:
        model (AutoModel): The pre-trained model instance used for transcription.
        audio_sample (np.ndarray): The audio data to be transcribed.

    Returns:
        str: The generated text transcription from the audio sample.
    """
    text = model.generate(
            input=audio_sample,
            cache={},
            language="auto",
            use_itn=True,
            batch_size_s=60,
            merge_vad=15
        )
    return text

def audio_file_splitting(model: AutoModel, audio_array: np.ndarray, sampling_rate: int = model_sampling_rate) -> str:
    """
    Split an audio array into chunks and generate transcriptions for each chunk.

    This function processes the input audio data by splitting it into smaller
    chunks of a specified length and generating transcriptions for each chunk.
    The resulting transcriptions are concatenated into a single string.

    Parameters:
        model (AutoModel): The pre-trained model instance used for transcription.
        audio_array (np.ndarray): The audio data to be transcribed.
        sampling_rate (int, optional): The sampling rate of the audio data (default is taken from model_sampling_rate).

    Returns:
        str: The concatenated text transcriptions from all processed audio chunks.
    """
    transcriptions = []
    sample_length = int(30 * sampling_rate)
    
    for start in range(0, len(audio_array), sample_length):
        end = min(start + sample_length, len(audio_array))
        chunk = audio_array[start:end]
        generated_text = text_generator(model, chunk)
        text = rich_transcription_postprocess(generated_text[0]["text"])
        transcriptions.append(text)
    
    return " ".join(transcriptions)
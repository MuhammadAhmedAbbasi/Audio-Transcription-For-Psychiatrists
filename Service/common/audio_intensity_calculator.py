import numpy as np
from Service.config import model_sampling_rate
from Service.logging.logging import *


def filter_audio_by_intensity(audio_data, threshold, frame_length=22050, hop_length=22050):
    """
    Filter audio based on RMS intensity for each frame.
    
    Parameters:
        audio_data: The audio data array (1D).
        threshold: The intensity threshold to keep audio (scaled to original RMS).
        frame_length: The number of samples in each frame (default 1 second if sr=22050).
        hop_length: The number of samples to shift between consecutive frames.
    """
    threshold = threshold/1000
    # Split the audio data into frames manually (no overlap)
    frames = split_audio_into_frames(audio_data, frame_length, hop_length)
    
    # Initialize a list to hold the filtered frames
    filtered_audio = []

    # Iterate over each frame and calculate its RMS
    for i, frame in enumerate(frames):
        rms = np.mean(np.abs(frame))  
        if rms > threshold:  # Only keep frames above the threshold
            filtered_audio.extend(frame)
    return np.array(filtered_audio)

def compute_intensity(audio_segment: np.ndarray) -> float:

    return np.mean(np.abs(audio_segment) ** 2)

def split_audio_into_frames(audio_data, frame_length, hop_length):
    frames = []
    for start in range(0, len(audio_data) - frame_length + 1, hop_length):
        frame = audio_data[start:start + frame_length]
        frames.append(frame)
    return frames

import asyncio

class AudioReceiveQueue:
    def __init__(self):
        self.audio_queue = asyncio.Queue()

audio_receive_queue = AudioReceiveQueue()



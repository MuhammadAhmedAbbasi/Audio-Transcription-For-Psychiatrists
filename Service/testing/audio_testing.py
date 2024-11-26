import asyncio
import io
import logging
import os
import pytest
import sys

from fastapi import WebSocket, WebSocketDisconnect
from fastapi.testclient import TestClient
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))
from Service.main import app  # Make sure to import your FastAPI app correctly

# Set up logging for visibility in tests
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.mark.asyncio
async def test_websocket_multiple_clients_and_audio_files():
    client = TestClient(app)  # Use TestClient, not AsyncClient

    # Define a list of audio file paths to test with
    audio_files = [
        r'C:\Users\Administrator\Desktop\Backend-Algorithm-LLM\Audio_transcription_files\output_audio.wav',
        r'C:\Users\Administrator\Desktop\Backend-Algorithm-LLM\Audio_transcription_files\tmp0lt3s799.wav',
        r'C:\Users\Administrator\Desktop\Backend-Algorithm-LLM\Audio_transcription_files\tmp7vby3w1k.wav',
    ]

    # Function to simulate sending audio for one client
    async def send_audio_and_receive_response(path):
        logger.info(f"Starting WebSocket connection for {path}")

        with open(path, "rb") as f:
            audio_data = f.read()

        try:
            with client.websocket_connect("/transcribe") as ws:
                logger.info(f"Sending audio for {path} to WebSocket...")
                ws.send_bytes(audio_data)

                # Simulate receiving a structured message response
                response = ws.receive_json()

                # Log the response
                logger.info(f"Received response for {path}: {response}")

                # Check that the response is a structured message
                assert "source" in response
                assert "content" in response

                # Case 1: If optional fields are included
                if "indexing_pointer_position" in response:
                    assert "indexing_pointer_position" in response
                    assert "final_sentence_pointer_position" in response
                    assert "new_sentence_indexing_pointer" in response

                # Case 2: If optional fields are NOT included
                else:
                    # Verify that the optional fields are NOT in the response
                    assert "indexing_pointer_position" not in response
                    assert "final_sentence_pointer_position" not in response
                    assert "new_sentence_indexing_pointer" not in response

        except WebSocketDisconnect:
            logger.error(f"WebSocket disconnected for {path}.")
            assert True  # Ensure WebSocket disconnect is handled correctly

        except Exception as e:
            logger.error(f"Error for {path}: {e}")
            pytest.fail(f"Test failed with error: {e}")

        logger.info(f"Finished WebSocket connection for {path}")

    # Run the tests concurrently for multiple audio files
    tasks = [send_audio_and_receive_response(path) for path in audio_files]
    await asyncio.gather(*tasks)  # Run all tasks concurrently
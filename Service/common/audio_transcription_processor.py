import asyncio
import requests
import re
from fastapi import WebSocket
import logging
from Service.model.audio_to_text_online import audio_to_text_model_online
from Service.model.audio_to_text_offline import audio_to_text_model_offline
from Service.common.temp_file_save_functions import *
from Service.config import *
from Service.common.data.audio_models import AudioModels
from Service.common.data.websockets_managment import websocket_manager
from Service.common.audio_word_mapping import word_mapping
from Service.common.data.intensity_settings import IntensitySettings
from Service.common.data.offline_transcription import OfflineTranscription


class AudioProcessor:
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        # Get user-specific data from WebSocketManager
        self.user_data = websocket_manager.get_user_data(websocket)
        # Access user-specific data for processing
        self.audio_buffer = self.user_data.audio_buffer
        self.buffer_length = self.user_data.buffer_length
        self.pointer_info = self.user_data.pointer_info
        self.transcribedtextstore = self.user_data.transcribed_text 
        self.buffer_processing_queue = self.user_data.buffer_processing_queue

    async def process_audio_queue(self):
        """
        Continuously processes incoming audio data from the audio queue.

        This function retrieves audio data from the audio queue, manages audio buffering,
        and triggers transcription processes based on the length of the buffered audio data.
        It filters audio segments based on predefined thresholds for segment length and processes them accordingly.

        The function performs the following steps:
        1. Extends the audio buffer with incoming audio data.
        2. Saves incoming audio data to a temporary file for transcription.
        3. If the audio buffer reaches specific thresholds, it prepares and processes segments for transcription.
        4. Triggers processing of current audio buffers asynchronously.
        """
        user_queue = websocket_manager.get_user_queue(self.websocket)  # Get the queue for this WebSocket

        while True:
            data = await user_queue.get()
            self.audio_buffer.audio_for_context_store.extend(data)  # Add incoming data to the buffer

            # audio_buffer_instance.transcription_correction_audio_store.extend(data)
            self.audio_buffer.saved_audio_data.append((data))
            temp_file_path = save_temp_audio_file(data, online_streaming_path = online_streaming_files)

            if temp_file_path:
                asyncio.create_task(self.process_streaming_transcription(temp_file_path,AudioModels.streaming_model, self.websocket))
            
            #when length of audio is greater than 8 second and less than 30 second
            if self.buffer_length.minimum_stored_buffer_length<= len(self.audio_buffer.saved_audio_data)< self.buffer_length.maximum_stored_buffer_length:
                # Clear the audio stream so new one will come
                self.audio_buffer.transcription_correction_audio_store.clear()
                # Start the index from 0 to end_correction_length
                for chunk in self.audio_buffer.saved_audio_data[self.buffer_length.audio_chunk_start_index:self.buffer_length.audio_chunk_end_index]:
                    # Put the data in Byte array so it become one data stream
                    self.audio_buffer.transcription_correction_audio_store.extend(chunk)  
                # Increase the end data length so new time data will come 
                self.buffer_length.audio_chunk_end_index += 1 
                current_buffer = self.audio_buffer.transcription_correction_audio_store
                asyncio.create_task(self.buffer_processing_queue.put(current_buffer))
                # Finally put in the buffer for process
                asyncio.create_task(self.process_current_buffer_queue())
                        
            # After 15 chunks below condition will be applicable
            if len(self.audio_buffer.saved_audio_data) >= self.buffer_length.maximum_stored_buffer_length:
                self.audio_buffer.transcription_correction_audio_store.clear()
                for chunk in self.audio_buffer.saved_audio_data[self.buffer_length.audio_chunk_start_index:self.buffer_length.audio_chunk_end_index]:  # Set the Minimun and Naximum chunks length, start from o to 15 
                    # Making a long stream of audio byte for transcription
                    self.audio_buffer.transcription_correction_audio_store.extend(chunk)
                    # Giving whole 15 Second of chunk as current Buffer and using it for transcription
                self.buffer_length.audio_chunk_start_index += 1
                self.buffer_length.audio_chunk_end_index += 1 
                asyncio.create_task(self.buffer_processing_queue.put(self.audio_buffer.transcription_correction_audio_store))
                asyncio.create_task(self.process_current_buffer_queue())
                

                

    async def process_current_buffer_queue(self):
        """
        Continuously processes the current audio buffer from the buffer processing queue.
        """
        while True: 
            current_buffer =  await self.buffer_processing_queue.get()
            await self.check_and_process_buffers(current_buffer)
            self.buffer_processing_queue.task_done()


    async def check_and_process_buffers(self,current_buffer):
        """
        Check and process the provided audio buffer for transcription.

        This function saves the current buffer to a temporary file and triggers the transcription process.
        
        Parameters:
            current_buffer (bytes): The audio buffer to be processed.

        Returns:
            None
        """
        combined_temp_path = save_temp_audio_file(current_buffer, online_correction_path = online_correction_files)
        if combined_temp_path:
            await self.corrected_transcription_online(combined_temp_path, AudioModels.non_streaming_model)


    async def corrected_transcription_online(self, temp_file_path: str,model):
        """
        Process the audio file for online transcription and manage the transcribed output.

        This function handles the transcription of audio files, updates the stored messages,
        and sends the transcribed results to clients.

        Parameters:
            temp_file_path (str): The path to the temporary audio file for transcription.
            model: The model used for transcription.

        Returns:
            None
        """
        try:
            message,_ = audio_to_text_model_offline(temp_file_path,model, intensity_threshold = IntensitySettings.intensity_value)
            # message  = message.split()
            print(f"Message {message}")
            split_message = re.findall(r"\b\w+\'?\w*|[^\w\s]", message)
            print(f"Split Message  {message}")
            cleaned_message = [word for word in split_message if re.match(r'^[a-zA-Z\u4e00-\u9fff]+$|^\.$', word)]
            print(f'Corrected Message: {split_message}')
            # This will check if the message is first message or not,
            if len(self.audio_buffer.saved_audio_data) <= self.buffer_length.maximum_stored_buffer_length:
                # Put the first message in old_message and total message list for furture processing
                self.transcribedtextstore.old_message = cleaned_message
                self.transcribedtextstore.total_message = cleaned_message
                self.pointer_info.total_pointer_position = len(self.transcribedtextstore.old_message)
                self.pointer_info.indexed_pointer_position = len(self.transcribedtextstore.old_message)
                await send_corrected_transcription_to_clients(self.transcribedtextstore.total_message,"final_Transcription",self.websocket ,self.pointer_info.indexed_pointer_position, self.pointer_info.total_pointer_position)
                await send_corrected_transcription_to_clients(self.transcribedtextstore.total_message,"corrected_transcription",self.websocket,self.pointer_info.indexed_pointer_position, self.pointer_info.total_pointer_position)

            else:
                # Receive and make list of new message
                self.transcribedtextstore.new_message = cleaned_message
                self.pointer_info.indexed_pointer_position = self.pointer_info.total_pointer_position
                mapped_pointer= await word_mapping(self.transcribedtextstore.old_message, self.transcribedtextstore.new_message)
                old_chunk_unmapped_pointer, new_chunk_unmapped_pointer = mapped_pointer.old_chunk_unmapped_pointer, mapped_pointer.new_chunk_unmapped_pointer
                old_chunk_mapped_pointer = len(self.transcribedtextstore.old_message[old_chunk_unmapped_pointer:])
                self.transcribedtextstore.old_message = self.transcribedtextstore.new_message[new_chunk_unmapped_pointer:]
                self.pointer_info.indexed_pointer_position = self.pointer_info.indexed_pointer_position - old_chunk_mapped_pointer
                self.transcribedtextstore.total_message = self.transcribedtextstore.total_message[:self.pointer_info.indexed_pointer_position]  + self.transcribedtextstore.new_message[new_chunk_unmapped_pointer:]
                self.pointer_info.total_pointer_position = self.pointer_info.indexed_pointer_position + len(self.transcribedtextstore.new_message[new_chunk_unmapped_pointer:])
                await send_corrected_transcription_to_clients(self.transcribedtextstore.new_message,"corrected_transcription",self.websocket ,self.pointer_info.indexed_pointer_position, self.pointer_info.total_pointer_position, new_chunk_unmapped_pointer)
                await send_corrected_transcription_to_clients(self.transcribedtextstore.total_message,"final_Transcription",self.websocket ,self.pointer_info.indexed_pointer_position, self.pointer_info.total_pointer_position)
                self.pointer_info.total_pointer_position = len(self.transcribedtextstore.total_message)
                
                
        except Exception as e:
            logging.error(f"Error processing audio: {e}")
            
        finally:
            await remove_temp_file(temp_file_path)



    async def process_streaming_transcription(self, temp_file_path: str,model, websocket: WebSocket):
        """
        Process audio for streaming transcription and send results to clients.

        This function handles audio data for online transcription and sends
        the resulting transcription to clients.

        Parameters:
            temp_file_path (str): The path to the temporary audio file for transcription.
            model: The model used for transcription.

        Returns:
            None
        """
        try:
            message = audio_to_text_model_online(temp_file_path,model)
            message_list = message.streaming_response
            message_list = message_list.split()
            await send_transcription_to_clients(message_list,"instant_transcription", websocket)
        except Exception as e:
            logging.error(f"Error processing audio: {e}")
        finally:
            await remove_temp_file(temp_file_path)


async def process_transcription_offline(audio_url: str)-> OfflineTranscription:
    """
    Process audio for offline transcription and return the result.

    This function saves the buffered audio to a temporary file,
    performs offline transcription, and organizes the transcribed results.

    Returns:
        OfflineTranscription: An object containing the transcribed message and identified subjects.

    Raises:
        Exception: If there is an error during audio processing or transcription.
    """
    try:
        audio_bytes = requests.get(audio_url, verify=False)
        audio_file = save_temp_audio_file(audio_bytes.content, save_to_path = audio_transcription_files)
        identified_subject = []
        message,generated_result = audio_to_text_model_offline(audio_file, AudioModels.full_transcription_model, intensity_active= False)
        
        for mess in generated_result:
            for info in mess['sentence_info']:
                identified_subject.append(f'Speaker {info['spk']}: {info['text']}')
                logging.info(f"Audio And Trascibed Info Saved!!! ")
        return OfflineTranscription(message = message, subject_conversation = identified_subject)
    except Exception as e:
        logging.error(f"Error processing audio: {e}")
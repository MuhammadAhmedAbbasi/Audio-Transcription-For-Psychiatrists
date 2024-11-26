import os
import pandas as pd

def audio_transcription_save(temp_file_path, full_transcription, audio_save_path):
    """
    Save the audio transcription data to an Excel file.

    This function takes the path of a temporary audio file and its corresponding transcription text,
    then saves this information into an Excel file. If the Excel file already exists, it appends 
    the new transcription data to the existing file.

    Parameters:
        temp_file_path (str): The file path of the temporary audio file.
        full_transcription (str): The transcription text corresponding to the audio file.
        audio_save_path (str): The path where the audio files are saved, used to determine the location of the Excel file.

    Returns:
        None
    """
    data = {
            "File Path": [temp_file_path],
            "Transcription": [full_transcription]
        }
    excel_file_path = os.path.join(os.path.dirname(audio_save_path), "transcriptions.xlsx")
    if os.path.exists(excel_file_path):
            # Load existing data and append new data
            df = pd.read_excel(excel_file_path)
            new_row = pd.DataFrame(data)
            df = pd.concat([df, new_row], ignore_index=True)
    else:
            # Create a new DataFrame if the file doesn't exist
            df = pd.DataFrame(data)

        # Save the DataFrame to Excel
    df.to_excel(excel_file_path, index=False)

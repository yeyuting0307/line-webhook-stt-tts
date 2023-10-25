import os
from google.cloud import speech

# Instantiates a client
client = speech.SpeechClient()

def recognize_audio(gcs_uri:str):
    ''' STT : transcribe speech from audio file stored on GCS to text
    language_code list : https://cloud.google.com/speech-to-text/docs/speech-to-text-supported-languages
    '''
    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=int(os.environ.get('STT_SAMPLE_RATE_HERTZ', 24000)),
        language_code=os.environ.get('STT_LANGUAGE_CODE', "zh-TW"),
        model=os.environ.get('STT_MODEL', 'default'),
        audio_channel_count=int(os.environ.get('STT_AUDIO_CHANNEL_COUNT', 1)),
        enable_word_confidence=os.environ.get('STT_ENABLE_WORD_CONFIDENCE', True),
        enable_word_time_offsets=os.environ.get('STT_ENABLE_WORD_TIME_OFFSETS', True),
    )

    # Detects speech in the audio file
    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    return response
    
  # %%

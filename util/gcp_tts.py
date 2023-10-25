import os
from typing import Literal
from google.cloud import texttospeech
client = texttospeech.TextToSpeechClient()

def synthesize_text(text, voice_gender : Literal["male", "female"] = "male"):
    """Synthesizes speech from the input string of text."""

    input_text = texttospeech.SynthesisInput(text=text)

    if voice_gender == "male":
        TTS_SSML_VOICE_GENDER = texttospeech.SsmlVoiceGender.MALE
    elif voice_gender == "female":
        TTS_SSML_VOICE_GENDER = texttospeech.SsmlVoiceGender.FEMALE
    else:
        raise ValueError(
            "voice_gender should be either 'male' or 'female' "
            " 'neutral' not support yet"
        )

    # Note: the voice can also be specified by name.
    # Names of voices can be retrieved with client.list_voices().
    # https://cloud.google.com/text-to-speech/docs/voices?hl=zh-cn
    voice = texttospeech.VoiceSelectionParams(
        language_code=os.environ.get("TTS_LANGUAGE_CODE", "cmn-TW"),
        name= os.environ.get("TTS_NAME", "cmn-TW-Wavenet-B"),
        ssml_gender=TTS_SSML_VOICE_GENDER,
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        request={"input": input_text, "voice": voice, "audio_config": audio_config}
    )
    return response
    

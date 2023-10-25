import os
import tempfile
import ffmpeg
from linebot.v3.messaging import TextMessage, AudioMessage

from util.gcp_storage import GcpStorage
from util.gcp_stt import recognize_audio
from util.gcp_palm2 import palm2_chat
from util.gcp_tts import synthesize_text
from util.audio_segment import get_audio_duration

project = os.environ.get('GCP_PROJECT_ID')
bucket_name = os.environ.get('GCP_BUCKET_NAME')
gs = GcpStorage(project)

def audio_analysis(event, line_bot_api, line_bot_api_blob):
    # LINE chatbot responses
    Responses = []

    # Get audio message(m4a) from LINE
    # https://developers.line.biz/en/reference/messaging-api/#audio-message
    user_id = event.source.user_id
    message_id = event.message.id
    message_duration = event.message.duration
    audio_bytes = line_bot_api_blob.get_message_content(message_id)

    # Convert m4a to wav, save to GCS
    with tempfile.NamedTemporaryFile(suffix=".m4a", delete=True) as tmp_input, \
        tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmp_output:
        tmp_input.write(audio_bytes)
        tmp_input.flush()

        ffmpeg.input(tmp_input.name)\
            .output(tmp_output.name, acodec='pcm_s16le', ac=1, ar='24000')\
            .run(overwrite_output = True)
        
        gs_path = f"{bucket_name}/{user_id}/tmp_{message_id}_{message_duration}.wav"
        gs.toStorage(remote_path = gs_path, local_path = tmp_output.name, make_public=True)

    # STT : speech(wav) to text
    gs_url = f"gs://{gs_path}"
    res_stt = recognize_audio(gs_url)

    stt_text = ""
    if res_stt.results:
        for result in res_stt.results:
            print('transcript: ', result.alternatives[0].transcript)
            stt_text += result.alternatives[0].transcript
        Responses.append(TextMessage(text = f"語音輸入: {stt_text}"))
    else:
        Responses.append(TextMessage(text = f"語音輸入: [無法辨識]"))
        return Responses
    
    # LLM : text to text
    ai_reply = palm2_chat(stt_text)
    Responses.append(TextMessage(text = f"AI回覆: {ai_reply}"))

    # TTS : text to speech(mp3)
    tts_response = synthesize_text(ai_reply)

    # Convert mp3 to m4a, save to GCS
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as tmp_input_ai,\
        tempfile.NamedTemporaryFile(suffix=".m4a", delete=True) as tmp_output_ai:
        tmp_input_ai.write(tts_response.audio_content)
        tmp_input_ai.flush()

        ffmpeg.input(tmp_input_ai.name)\
            .output(tmp_output_ai.name, acodec='aac', ac=1, ar='24000')\
            .run(overwrite_output = True)
        
        duration_ms =  get_audio_duration(tmp_output_ai.name) 
        gs_path_ai = f"{bucket_name}/{user_id}/tmp_ai_{message_id}_{duration_ms}.m4a"
        gs.toStorage(remote_path = gs_path_ai, local_path = tmp_output_ai.name, make_public=True)

    # Get audio url and duration (in millisecond)
    audio_url = f"https://storage.googleapis.com/{gs_path_ai}"
    try:
        audio_duration = int(duration_ms)
    except:
        audio_duration = 10000

    Responses.append(
        AudioMessage(
            original_content_url = audio_url,
            duration = audio_duration # required
        )
    )
    return Responses
from pydub import AudioSegment

def get_audio_duration(file_path:str, in_seconds:bool = False) -> int:
    '''Get audio duration in milli-seconds(ms) by default'''
    sounds = AudioSegment.from_file(file_path)
    duration_ms = len(sounds)
    if in_seconds:
        return duration_ms // 1000 + 1
    return duration_ms 
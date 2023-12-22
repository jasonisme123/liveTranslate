from faster_whisper import WhisperModel
import os
from pydub import AudioSegment


def get_model():
    return WhisperTranscriber()


class WhisperTranscriber:
    def __init__(self):
        self.audio_model = WhisperModel('base.en', compute_type='int8')

    def get_transcription(self, wav_file_path):
        try:
            segments, info = self.audio_model.transcribe(wav_file_path)
            total_text = ''
            end_time = 0.0
            for segment in segments:
                total_text += segment.text.strip()
                end_time = segment.end
        except Exception as e:
            print(e)
            return ''
        return total_text, end_time

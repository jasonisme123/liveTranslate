import wave
import os
import tempfile
import io
from datetime import timedelta
import pyaudiowpatch as pyaudio
from googletranslatepy import Translator
translator = Translator(proxies='http://127.0.0.1:7890')

PHRASE_TIMEOUT = 0.2


class AudioTranscriber:
    def __init__(self, speaker_source, model):
        self.audio_model = model
        self.audio_sources = {
            "Speaker": {
                "sample_rate": speaker_source.SAMPLE_RATE,
                "sample_width": speaker_source.SAMPLE_WIDTH,
                "channels": speaker_source.channels,
                "last_sample": bytes(),
                "last_spoken": None,
                "last_time": 0,
                "process_data_func": self.process_speaker_data
            }
        }

    def transcribe_audio_queue(self, audio_queue):
        while True:
            who_spoke, data, time_spoken = audio_queue.get()
            self.update_last_sample_and_phrase_status(
                who_spoke, data, time_spoken)
            source_info = self.audio_sources[who_spoke]

            text = ''
            try:
                fd, path = tempfile.mkstemp(suffix=".wav")
                os.close(fd)
                source_info["process_data_func"](
                    source_info["last_sample"], path)
                text, duration_time = self.audio_model.get_transcription(path)
                source_info["last_time"] = timedelta(
                    seconds=duration_time)+source_info["last_spoken"]
            except Exception as e:
                print(e)
            finally:
                os.unlink(path)

            if text != '':
                self.update_transcript(who_spoke, text, time_spoken)

    def update_last_sample_and_phrase_status(self, who_spoke, data, time_spoken):
        source_info = self.audio_sources[who_spoke]

        if not source_info["last_spoken"] or time_spoken - source_info["last_time"] > timedelta(seconds=PHRASE_TIMEOUT):
            source_info["last_sample"] = bytes()
            source_info["last_sample"] = data
            source_info["last_spoken"] = time_spoken
        else:
            source_info["last_sample"] += data

    def process_speaker_data(self, data, temp_file_name):
        with wave.open(temp_file_name, 'wb') as wf:
            wf.setnchannels(self.audio_sources["Speaker"]["channels"])
            p = pyaudio.PyAudio()
            wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.audio_sources["Speaker"]["sample_rate"])
            wf.writeframes(data)

    def update_transcript(self, who_spoke, text, time_spoken):
        print(who_spoke+": "+text)
        print(translator.translate(text))

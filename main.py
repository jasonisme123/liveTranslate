import threading
from AudioTranscriber import AudioTranscriber
import AudioRecorder
import queue
import time
import torch
import sys
import TranscriberModels
import subprocess


def main():
    try:
        subprocess.run(["ffmpeg", "-version"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("ERROR: The ffmpeg library is not installed. Please install ffmpeg and try again.")
        return

    audio_queue = queue.Queue()
    time.sleep(2)
    speaker_audio_recorder = AudioRecorder.DefaultSpeakerRecorder()
    speaker_audio_recorder.record_into_queue(audio_queue)
    model = TranscriberModels.get_model()

    transcriber = AudioTranscriber(speaker_audio_recorder.source, model)
    # while True:
    transcriber.transcribe_audio_queue(audio_queue)


if __name__ == "__main__":
    main()

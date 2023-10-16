import argparse
import io
import os
import speech_recognition as sr
import torch

from datetime import datetime, timedelta
from queue import Queue
from tempfile import NamedTemporaryFile
from time import sleep

from faster_whisper import WhisperModel

audio_model = WhisperModel("medium.en", device="cuda", compute_type="float16")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--energy_threshold", default=500,
                        help="Energy level for mic to detect.", type=int)
    parser.add_argument("--record_timeout", default=1,
                        help="How real-time the recording is in seconds.", type=float)
    parser.add_argument("--phrase_timeout", default=0.5,
                        help="How much empty space between recordings before we "
                             "consider it a new line in the transcription.", type=float)
    args = parser.parse_args()
    
    phrase_time = None
    last_sample = bytes()
    data_queue = Queue()
    recorder = sr.Recognizer()
    recorder.energy_threshold = args.energy_threshold
    recorder.dynamic_energy_threshold = False

    source = sr.Microphone(sample_rate=16000)
        
    record_timeout = args.record_timeout
    phrase_timeout = args.phrase_timeout

    temp_file = NamedTemporaryFile().name
    transcription = ['']
    
    with source:
        recorder.adjust_for_ambient_noise(source)

    def record_callback(_, audio: sr.AudioData) -> None:
        data = audio.get_raw_data()
        data_queue.put(data)

    recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

    print("Model loaded.\n")

    while True:
        try:
            now = datetime.utcnow()
            if not data_queue.empty():
                phrase_complete = False
                if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                    last_sample = bytes()
                    phrase_complete = True
                phrase_time = now

                while not data_queue.empty():
                    data = data_queue.get()
                    last_sample += data

                audio_data = sr.AudioData(last_sample, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
                wav_data = io.BytesIO(audio_data.get_wav_data())

                with open(temp_file, 'w+b') as f:
                    f.write(wav_data.read())

                text = transcribe_audio(temp_file)
                
                if phrase_complete:
                    transcription.append(text)
                else:
                    transcription[-1] = text

                os.system('cls')
                for line in transcription:
                    print(line)
                print('', end='', flush=True)

                sleep(0.25)
        except KeyboardInterrupt:
            break

    print("\n\nTranscription:")
    for line in transcription:
        print(line)


def transcribe_audio(audio_file):
    segments, _ = audio_model.transcribe(audio_file)
    segments = list(segments)  # The transcription will actually run here.
    
    label_text = ""
    for segment in segments:
        label_text += segment.text + " "
    
    return label_text

if __name__ == "__main__":
    main()

import pyaudio
import threading
import keyboard
from faster_whisper import WhisperModel
import io
import numpy as np
import soundfile as sf

COMPUTE_TYPE = "float16"

class Transcriber:
    def __init__(self, model_name, device_type):
        self.model = WhisperModel(model_name, device=device_type, compute_type=COMPUTE_TYPE)
        self.recording = False
        self.predicted_text = ""
        self.frames = []
        self.transcription_done = threading.Event()

    def capture_audio(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        while self.recording:
            data = stream.read(256)
            self.frames.append(np.frombuffer(data, dtype=np.int16))
        stream.stop_stream()
        stream.close()
        audio.terminate()

    def record_audio(self):
        self.frames = []
        self.capture_audio()
        audio_data = np.concatenate(self.frames, axis=0)
        audio_buffer = io.BytesIO()
        sf.write(audio_buffer, audio_data, 16000, format='wav')
        audio_buffer.seek(0)
        transcription = self.transcribe_audio(audio_buffer)
        self.predicted_text = transcription
        self.transcription_done.set()

    def start_recording(self):
        self.recording = True
        self.predicted_text = "" 
        recording_thread = threading.Thread(target=self.record_audio)
        recording_thread.start()

    def stop_recording(self):
        self.recording = False

    def get_predicted_text(self):
        self.transcription_done.wait() 
        return self.predicted_text
    
    def transcribe_audio(self, audio_buffer):
        segments, _ = self.model.transcribe(audio_buffer)
        segments = list(segments)
        transcription = " ".join([segment.text for segment in segments])
        return transcription


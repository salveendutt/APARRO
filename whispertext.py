import os
import wave
import time
import keyboard
import threading
import pyaudio
from faster_whisper import WhisperModel

COMPUTE_TYPE = "float16"

class whisperTest:
    def __init__(self, model_name, device_type):
        self.model = WhisperModel(model_name, device=device_type, compute_type=COMPUTE_TYPE)
        self.recording = False
        self.predicted_text = ""

    def capture_audio(self):
        frames = []
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)

        while self.recording:
            data = stream.read(1024)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        return frames

    def save_audio(self, frames):
        sound_file = wave.open("recording.wav", "wb")
        sound_file.setnchannels(1)
        sound_file.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
        sound_file.setframerate(44100)
        sound_file.writeframes(b"".join(frames))
        sound_file.close()

    def record_audio(self):
            frames = self.capture_audio()
            self.save_audio(frames)

            transcription = self.transcribe_audio("recording.wav")
            self.predicted_text = transcription

    def start_recording(self):
        self.recording = True
        self.predicted_text = "" 

        recording_thread = threading.Thread(target=self.record_audio)
        recording_thread.start()

    def stop_recording(self):
        self.recording = False

    def get_predicted_text(self):
        return self.predicted_text
    
    def delete_audio(self):
        try:
            os.remove("recording.wav")
        except FileNotFoundError:
            print("Recording file not found.")

    def transcribe_audio(self, audio_file):
        segments, _ = self.model.transcribe(audio_file)
        segments = list(segments)
        transcription = " ".join([segment.text for segment in segments])
        return transcription

def main():
    whisper_instance = whisperTest(model_name="medium.en", device_type="cuda")
    
    print("Press 'O' to start recording...\n")
    keyboard.wait("o")
    
    whisper_instance.start_recording()
    
    print("Recording... Press 'O' again to stop recording.\n")
    keyboard.wait("o")

    whisper_instance.stop_recording()
    

    time.sleep(3)


    text = whisper_instance.get_predicted_text()
    print("Predicted Text:", text)

    whisper_instance.delete_audio()
if __name__ == "__main__":
    main()

"""
This module contains the Transcriber class for transcribing audio input using the Whisper model.
"""

import io
import threading
import time
import numpy as np
import pyaudio
import soundfile as sf
from faster_whisper import WhisperModel
import keyboard
import time

COMPUTE_TYPE_GPU = "float16"
COMPUTE_TYPE_CPU = "float32"
# Whisper is able to handle only up to 30 seconds, so we need to cut the string
# after some period of time the same way as in live transcibe. Or is it handled in transcribe_audio?
# pylint: disable=R0903

class Transcriber:
    """
    This class is responsible for transcribing audio input using the Whisper model.
    It captures audio from the microphone, processes it,
    and uses the model to transcribe it into text.
    """
    def __init__(self, model_name: str, device_type: str):
        """
        Initializes the Transcriber with a Whisper model and settings.

        Args:
        model_name (str): Name of the Whisper model to use for transcription.
        device_type (str): Type of device to use for the Whisper model.
        """
        try:
            if device_type == "cpu":
                self._model = WhisperModel(model_name, device=device_type, compute_type=COMPUTE_TYPE_CPU)
            else:
                self._model = WhisperModel(model_name, device=device_type, compute_type=COMPUTE_TYPE_GPU)
        except Exception as e:
            raise RuntimeError("Error initializing WhisperModel") from e

        self._is_recording = False
        self._is_paused = False
        self._predicted_text = ""
        self._frames = []
        self._transcription_done = threading.Event()

    def _capture_audio(self):
        """
        Captures audio from the microphone and stores it in frames.
        """
        audio = pyaudio.PyAudio()
        stream = None
        try:
            while self._is_recording or self._is_paused:
                if self._is_recording:
                    if stream is None:
                        stream = audio.open(format=pyaudio.paInt16, channels=1,
                                            rate=16000, input=True, frames_per_buffer=1024)

                    data = stream.read(256, exception_on_overflow=False)
                    self._frames.append(np.frombuffer(data, dtype=np.int16))
                elif stream is not None:
                    stream.stop_stream()
                    stream.close()
                    stream = None
        except IOError as e:
            raise RuntimeError("Error capturing audio") from e
        finally:
            if stream is not None:
                stream.stop_stream()
                stream.close()
            audio.terminate()

    def _record_audio(self):
        """
        Records audio, processes it, and transcribes it into text.
        """
        self._frames = []
        try:
            self._capture_audio()
            if len(self._frames) == 0:
                self._predicted_text = "No audio data captured."
                self._transcription_done.set()
                return
            audio_data = np.concatenate(self._frames, axis=0)
            audio_buffer = io.BytesIO()
            sf.write(audio_buffer, audio_data, 16000, format='wav')
            audio_buffer.seek(0)
            transcription = self._transcribe_audio(audio_buffer)
            self._predicted_text = transcription
            self._transcription_done.set()
        except Exception as e:
            raise RuntimeError("Error recording and transcribing audio: " + str(e)) from e

    def _start_recording(self):
        """
        Starts the audio recording process.
        """
        self._is_recording = True
        self._predicted_text = ""
        recording_thread = threading.Thread(target=self._record_audio)
        recording_thread.start()

    def _stop_recording(self):
        """
        Stops the audio recording process.
        """
        self._is_recording = False
        self._is_paused = False

    def _pause_recording(self):
        """
        Pauses the audio recording process.
        """
        self._is_paused = True
        self._is_recording = False

    def _resume_recording(self):
        """
        Resumes the audio recording process.
        """
        self._is_paused = False
        self._is_recording = True

    def _get_predicted_text(self) -> str:
        """
        Waits for transcription to complete and returns the predicted text.

        Returns:
        str: The transcribed text.
        """
        t0 = time.time()
        self._transcription_done.wait()
        t1 = time.time()
        print(f"Transcription took {t1 - t0} seconds")
        return self._predicted_text

    def _transcribe_audio(self, audio_buffer) -> str:
        """
        Transcribes audio data from the provided audio buffer.

        Args:
        audio_buffer (io.BytesIO): Buffer containing audio data.

        Returns:
        str: The transcribed text.
        """
        try:
            segments, _ = self._model.transcribe(audio_buffer)
            segments = list(segments)
            transcription = " ".join([segment.text for segment in segments])
            return transcription
        except Exception as e:
            raise RuntimeError("Error transcribing audio") from e

    def transcribe(self):
        """
        Perform audio recording and transcription.

        This method handles the entire process of recording audio, stopping recording,
        and transcribing the recorded audio.

        Returns:
        str: The transcribed text.
        """
        try:
            input("Press Enter to start recording...")
            self._start_recording()
            print("Recording... (Press 'p' to pause, 'r' to resume, 's' to stop)")
            last_press_time = 0
            debounce_int = 0.5  # 500 milliseconds

            while True:
                current_time = time.time()

                if keyboard.is_pressed('p') and current_time - last_press_time > debounce_int:
                    self._pause_recording()
                    print("Recording paused. Press 'r' to resume or 's' to stop.")
                    last_press_time = current_time

                elif keyboard.is_pressed('r') and current_time - last_press_time > debounce_int:
                    self._resume_recording()
                    print("Recording resumed. Press 'p' to pause or 's' to stop.")
                    last_press_time = current_time

                elif keyboard.is_pressed('s') and current_time - last_press_time > debounce_int:
                    self._stop_recording()
                    print("Recording stopped. Transcribing...\n")
                    break

                time.sleep(0.1)  # Small sleep to prevent high CPU usage

            return self._get_predicted_text()
        except RuntimeError as e:
            raise RuntimeError("Error during audio recording and transcription: ") from e
            
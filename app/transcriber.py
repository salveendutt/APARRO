import pyaudio
import threading
from faster_whisper import WhisperModel
import io
import numpy as np
import soundfile as sf
COMPUTE_TYPE = "float16"
# Whisper is able to handle only up to 30 seconds, so we need to cut the string 
# after some period of time the same way as in live transcibe. Or is it handled in transcribe_audio?
class Transcriber:
    def __init__(self, model_name: str, device_type: str):
        """
        Initializes the Transcriber with a Whisper model and settings.

        Args:
        model_name (str): Name of the Whisper model to use for transcription.
        device_type (str): Type of device to use for the Whisper model.
        """
        try:
            self._model = WhisperModel(model_name, device=device_type, compute_type=COMPUTE_TYPE)
        except Exception as e:
            raise Exception("Error initializing WhisperModel: " + str(e))

        self._is_recording = False
        self._predicted_text = ""
        self._frames = []
        self._transcription_done = threading.Event()

    def _capture_audio(self):
        """
        Captures audio from the microphone and stores it in frames.
        """
        audio = pyaudio.PyAudio()
        stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        try:
            while self._is_recording:
                data = stream.read(256)
                self._frames.append(np.frombuffer(data, dtype=np.int16))
        except Exception as e:
            raise Exception("Error capturing audio: " + str(e))
        finally:
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
            raise Exception("Error recording and transcribing audio: " + str(e))

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

    def _get_predicted_text(self) -> str:
        """
        Waits for transcription to complete and returns the predicted text.

        Returns:
        str: The transcribed text.
        """
        self._transcription_done.wait()
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
            raise Exception("Error transcribing audio: " + str(e))

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
            input("Recording... Press Enter again to stop recording.")
            self._stop_recording()
            print("Recording Complete. Transcribing...\n")
            return self._get_predicted_text()
        except Exception as e:
            raise Exception("Error during audio recording and transcription: " + str(e))

import unittest
import io
import os
import sys
import soundfile as sf
from unittest.mock import patch, MagicMock
import time

app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_dir not in sys.path:
    sys.path.append(app_dir)

import transcriber as tr  # Import the Transcriber class from your implementation

class TestTranscriber(unittest.TestCase):
    def setUp(self):
        self.transcriber = tr.Transcriber(model_name="medium.en", device_type="cuda")

    def test_init_with_exception(self):
        # Use invalid model name or device type to trigger an exception
        invalid_model_name = "invalid_model"
        invalid_device_type = "invalid_device"

        with self.assertRaises(RuntimeError):
            tr.Transcriber(model_name=invalid_model_name, device_type="cuda")  # Should raise RuntimeError for invalid model name

        with self.assertRaises(RuntimeError):
            tr.Transcriber(model_name="medium.en", device_type=invalid_device_type)  # Should raise RuntimeError for invalid device type

    def test_transcribe_audio(self):
        audio_path = os.path.join(os.path.dirname(__file__), "testdata", "jfk.wav")
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
        audio_buffer = io.BytesIO(audio_data)
        transcription = self.transcriber._transcribe_audio(audio_buffer)  # Use private method
        self.assertIsInstance(transcription, str)
        self.assertNotEqual(transcription, "")

    def test_transcribe_audio_with_exception(self):
        # Create a mock audio buffer that will cause the transcription to fail
        audio_buffer = io.BytesIO(b'invalid audio data')
        with self.assertRaises(RuntimeError):
            self.transcriber._transcribe_audio(audio_buffer)  # Should raise RuntimeError

    def test_start_recording_and_stop_recording(self):
        self.transcriber._start_recording()  # Use private method
        self.assertTrue(self.transcriber._is_recording)  # Use private attribute
        self.transcriber._stop_recording()  # Use private method
        self.assertFalse(self.transcriber._is_recording)  # Use private attribute

    def test_get_predicted_text(self):
        self.transcriber._transcription_done.set()  # Use private attribute
        predicted_text = self.transcriber._get_predicted_text()  # Use private method
        self.assertIsInstance(predicted_text, str)

if __name__ == '__main__':
    unittest.main()


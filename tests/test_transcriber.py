import unittest
import io
import os
import sys
import numpy as np
import soundfile as sf
from unittest.mock import MagicMock, patch

app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
if app_dir not in sys.path:
    sys.path.append(app_dir)

import transcriber as tr  # Import the Transcriber class from your implementation

class TestTranscriber(unittest.TestCase):

    def setUp(self):
        self.transcriber = tr.Transcriber(model_name="medium.en", device_type="cuda")

    # def infinite_audio_stream():
    # # Provide 10 chunks of mock data, then infinite empty data
    #     for _ in range(10):
    #         yield b'\x00\x01' * 256
    #     while True:
    #         yield b''

    # @patch('pyaudio.PyAudio', autospec=True)
    # def test_capture_audio(self, mock_pyaudio):
    #     # Setup the mock
    #     mock_audio_instance = mock_pyaudio.return_value
    #     mock_stream = mock_audio_instance.open.return_value
    #     mock_stream.read.side_effect = self.infinite_audio_stream()  # Use the infinite generator

    #     # Start the test
    #     self.transcriber._is_recording = True
    #     self.transcriber._capture_audio()

    #     # Assertions
    #     mock_audio_instance.open.assert_called_once()
    #     mock_stream.read.assert_called()
    #     mock_stream.stop_stream.assert_called()
    #     mock_stream.close.assert_called()
    #     mock_audio_instance.terminate.assert_called()

    # @patch.object(tr.Transcriber, '_transcribe_audio', return_value="Mocked transcription")
    # def test_record_audio(self, mock_transcribe_audio):
    #     # Setting up the state
    #     self.transcriber._is_recording = True
    #     self.transcriber._frames = [np.array([1, 2, 3])]  # Example frame data

    #     # Call the method under test
    #     self.transcriber._record_audio()

    #     # Assert if _transcribe_audio was called
    #     mock_transcribe_audio.assert_called()


    def test_transcribe_audio(self):
        audio_path = os.path.join(os.path.dirname(__file__), "testdata", "jfk.wav")
        with open(audio_path, 'rb') as f:
            audio_data = f.read()
        audio_buffer = io.BytesIO(audio_data)
        transcription = self.transcriber._transcribe_audio(audio_buffer)  # Use private method
        self.assertIsInstance(transcription, str)
        self.assertNotEqual(transcription, "")

    def test_start_recording_and_stop_recording(self):
        self.transcriber._start_recording()  # Use private method
        self.assertTrue(self.transcriber._is_recording)  # Use private attribute
        self.transcriber._stop_recording()  # Use private method
        self.assertFalse(self.transcriber._is_recording)  # Use private attribute

    def test_get_predicted_text(self):
        self.transcriber._transcription_done.set()  # Use private attribute
        predicted_text = self.transcriber._get_predicted_text()  # Use private method
        self.assertIsInstance(predicted_text, str)

    def test_pause_and_resume_recording(self):
        self.transcriber._start_recording()
        self.assertTrue(self.transcriber._is_recording)
        self.assertFalse(self.transcriber._is_paused)

        self.transcriber._pause_recording()
        self.assertFalse(self.transcriber._is_recording)
        self.assertTrue(self.transcriber._is_paused)

        self.transcriber._resume_recording()
        self.assertTrue(self.transcriber._is_recording)
        self.assertFalse(self.transcriber._is_paused)

    @patch('transcriber.WhisperModel.transcribe', side_effect=Exception("Mock exception"))
    def test_transcribe_audio_exception_handling(self, mock_transcribe):
        audio_buffer = io.BytesIO(b"dummy audio data")
        with self.assertRaises(RuntimeError) as context:
            self.transcriber._transcribe_audio(audio_buffer)
        self.assertIn("Error transcribing audio", str(context.exception))

    @patch('transcriber.keyboard')
    @patch('transcriber.time')
    def test_transcribe_method(self, mock_time, mock_keyboard):
        # Initialize time mock
        mock_time_values = [0, 0.6, 1.2, 1.8, 2.4, 3.0]  # Simulates time passing
        mock_time.time.side_effect = lambda: mock_time_values.pop(0)

        # Initialize keyboard mock for 'p' (pause) and 'r' (resume)
        mock_keyboard.is_pressed.side_effect = lambda key: {
            'p': [False, True, False, False, False][len(mock_time_values) - 1],
            'r': [False, False, True, False, False][len(mock_time_values) - 1],
            's': [False, False, False, True, False][len(mock_time_values) - 1]
        }[key]

        # Initialize Transcriber
        tr = self.transcriber

        # Mocking the recording process methods
        tr._start_recording = MagicMock()
        tr._pause_recording = MagicMock()
        tr._resume_recording = MagicMock()
        tr._stop_recording = MagicMock()
        tr._get_predicted_text = MagicMock(return_value="Mocked transcription")

        # Test the transcribe method
        result = tr.transcribe()

        # Assertions
        tr._start_recording.assert_called_once()
        tr._pause_recording.assert_called_once()
        tr._resume_recording.assert_called_once()
        tr._stop_recording.assert_called_once()
        tr._get_predicted_text.assert_called_once()
        self.assertEqual(result, "Mocked transcription")

    @patch('transcriber.Transcriber._start_recording', side_effect=RuntimeError("Mocked recording error"))
    def test_transcribe_exception_handling(self, mock_start_recording):
        tr = self.transcriber

        with self.assertRaises(RuntimeError) as context:
            tr.transcribe()
        self.assertIn("Error during audio recording and transcription:", str(context.exception))


if __name__ == '__main__':
    unittest.main()

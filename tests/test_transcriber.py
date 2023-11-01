import unittest
import io
import os
import sys
import soundfile as sf
# TODO Fix the path. Right now it gives warning, but something has to be done in order
# for it to not show warning
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
sys.path.append(app_dir)
import transcriber as tr  # Import the Transcriber class from your implementation

class TestTranscriber(unittest.TestCase):
    def setUp(self):
        self.transcriber = tr.Transcriber(model_name="medium.en", device_type="cuda")

    # TODO need to load from wav/flac file bytes and then using these bytes make a test
    # from https://github.com/openai/whisper/tree/main/tests 
    # def test_transcribe_audio(self):
        # audio_path = os.path.join(os.path.dirname(__file__), r"testdata\jfk.wav")
        # audio_data, _ = sf.read(audio_path)
        # audio_buffer = io.BytesIO(audio_data)
        # transcription = self.transcriber.transcribe_audio(audio_buffer)
        # self.assertIsInstance(transcription, str)

    def test_start_recording_and_stop_recording(self):
        self.transcriber.start_recording()
        self.assertTrue(self.transcriber.recording)

        self.transcriber.stop_recording()
        self.assertFalse(self.transcriber.recording)

    def test_get_predicted_text(self):
        self.transcriber.transcription_done.set()  # Simulate transcription completion
        predicted_text = self.transcriber.get_predicted_text()
        self.assertIsInstance(predicted_text, str)

if __name__ == '__main__':
    unittest.main()

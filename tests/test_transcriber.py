import unittest
import io
import os
import sys
# TODO Fix the path. Right now it gives warning, but something has to be done in order
# for it to not show warning
app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'app'))
sys.path.append(app_dir)
import transcriber as tr  # Import the Transcriber class from your implementation

class TestTranscriber(unittest.TestCase):
    def setUp(self):
        self.transcriber = tr.Transcriber(model_name="medium.en", device_type="cuda")

    def tearDown(self):
        pass

    # TODO need to load from wav/flac file bytes and then using these bytes make a test 
    # def test_transcribe_audio(self):
    #     audio_data = b'\x00\x01\x02\x03'
    #     audio_buffer = io.BytesIO(audio_data)
    #     transcription = self.transcriber.transcribe_audio(audio_buffer)
    #     self.assertIsInstance(transcription, str)

    # TODO Right now this returns OK, and then error. 
    # This needs to be fixed: The problem is in record_audio(self)
    # If self.Frame (I think at least) is empty it returns error, 
    # Speaking human language, we start and stop recording vary fast, 
    # and there isn't any info to be processed, hence an error. If user
    # will press enter twice the same error will appera
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

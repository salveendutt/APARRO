from faster_whisper import WhisperModel

model = WhisperModel("medium.en", device="cuda", compute_type="float16")

def transcribe_audio(audio_file):
    segments, _ = model.transcribe(audio_file)
    segments = list(segments)  # The transcription will actually run here.
    
    label_text = ""
    for segment in segments:
        label_text += segment.text + " "
    
    return label_text

def main():
    print(transcribe_audio("y2mate.com - Martin Luther King Jr I have a dream Audio Clip.mp3"))


if __name__ == "__main__":
    main()

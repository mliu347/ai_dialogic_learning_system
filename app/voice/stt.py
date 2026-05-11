import os
from faster_whisper import WhisperModel

model = WhisperModel("base")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
audio_path = os.path.join(BASE_DIR, "audio.wav")

print("Checking:", audio_path)
print("Exists:", os.path.exists(audio_path))

segments, info = model.transcribe(audio_path)

for segment in segments:
    print(segment.text)
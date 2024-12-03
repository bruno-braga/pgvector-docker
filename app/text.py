from TTS.api import TTS

tts = TTS(model_name="tts_models/en/vctk/vits")
tts.tts_to_file(text="Hello! This is an example.", file_path="output.wav")

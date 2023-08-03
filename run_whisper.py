import whisper



# using whisper to 
def run_whisper():
    model = whisper.load_model("base")
    result = model.transcribe("audio.mp3")
    return result["text"]




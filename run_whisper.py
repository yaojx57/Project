import whisper



# using whisper to 
def run_whisper(file, model):
    # model = whisper.load_model("base")
    result = model.transcribe(file)
    return result["text"]




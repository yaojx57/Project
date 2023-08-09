import whisper



# using whisper to 
def run_whisper(file, model):
    #TODO 调整参数适配
    # model = whisper.load_model("base")
    result = model.transcribe(file)
    return result["text"]




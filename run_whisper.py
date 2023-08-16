import whisper



# using whisper to 
def file_name(listener, system, signal):
    file_name = signal + '_' + listener + '_' + system
    return file_name


def run_whisper(file, model):
    #TODO 调整参数适配
    # model = whisper.load_model("base")
    result = model.transcribe(file)
    return result["text"]




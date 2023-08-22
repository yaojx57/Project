import whisper
import os



# using whisper to 
def file_name(listener, system, signal):
    file_name = signal + '_' + listener + '_' + system
    return file_name


def run_whisper(file, model):
    # model = whisper.load_model("base")
    result = model.transcribe(file)
    return result["text"]

def uniquify(path):
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename + "__" + str(counter) + extension
        counter += 1

    return path




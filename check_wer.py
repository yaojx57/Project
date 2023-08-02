import whisper
import argparse


from jiwer import wer
from clarity.utils.audiogram import Audiogram
from clarity.evaluator.msbg.msbg import Ear
from clarity.utils.file_io import read_signal, write_signal

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', action="store_true", help='test mode', default=True)
parser.add_argument('-i', '--input', type=str, help='input folder', required=True)
parser.add_argument('-o', '--output', type=str, help='out folder')
parser.add_argument('')
# parser.add_argument('')
args = vars(parser.parse_args())


def get_prompt(test):
    if test:
        return "i don't want us to apportion blame she said"
    else:
        # TODO 
        pass

# get lisentner's
def get_response(test):
    if test:
        return "i don't want to have to report he said"
    else:
        # TODO 
        pass

# get listener's audiogram to msbg
def get_audiogram(test):
    if test:
        return Audiogram(
            levels=[30,25,25,50,65,75,75,90],
            frequencies=[250,500,1000,2000,3000,4000,6000,8000],)
    else:
        # TODO 
        pass

# get speech infomation from json file
def speech_info():
    pass

# get listener infomation from json file
def listener_info():
    pass

# using msbg to imitate listening of 
def run_msbg(audiogram, input, output):
    # TODO 可以修改
    # The sampling rate to use
    sample_rate = 44100  

    # Read signal from wav file
    signal = read_signal(input, sample_rate)

    # The audiogram for the listener
    audiogram = audiogram

    # Initialize the ear and process the signal
    ear = Ear(equiv_0db_spl=80)
    ear.set_audiogram(audiogram)
    out = ear.process(signal)

    # Write the processed signal to a wav file
    if output is not None:
        write_signal(output, out[0], sample_rate)
    return out[0]

# using whisper to 
def run_whisper():
    model = whisper.load_model("base")
    result = model.transcribe("audio.mp3")
    return result["text"]


def check_wer(reference, hypothesis):
    error = wer(reference, hypothesis)
    return error


def main():
    test = args['test']
    input = args['input']
    output = args['output']

    prompt = get_prompt(test)

    response = get_response(test)

    audiogram = get_audiogram(test)

    output_speech = run_msbg(audiogram, input, output)

    result = run_whisper()

    wer = check_wer(prompt, result)
# import jiwer 
import os
import whisper
import json

from speech_info import result_json
from read_json import read_json
from run_msbg import run_msbg, out_file, get_file
from run_whisper import run_whisper


def read_info(prompt, signal, response, whisper_signal, whisper_msbg, correctness_resp, correctness_whisper):
    result = result_json(prompt, signal, response, whisper_signal, whisper_msbg, correctness_resp, correctness_whisper)
    return result


def main():
    speeches = read_json('json_data/CEC1.train.1.json')
    model = whisper.load_model("base")
    signals = []
    infos = []
    results = {}
    outputs = []
    for speech in speeches:
        # print(speech.signal)
        signals.append(speech.signal)
    if not os.path.isfile(out_file(speech.signal)):
        run_msbg(signals)
    for speech in speeches:
        file = get_file(speech.signal)
        output = out_file(speech.signal)
        whisper_signal = run_whisper(file, model)
        whisper_msbg = run_whisper(output, model)
        result = read_info(speech.prompt, speech.signal, speech.response, 
                           whisper_signal, whisper_msbg, speech.correctness, 0)
        print(result.__dict__)
        results[speech.signal] = result.__dict__
    with open('output.json','w') as json_file:
        json.dump(results, json_file)
    
    

    


if __name__=='__main__':
    main()
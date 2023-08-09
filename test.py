# import jiwer 
import os
import whisper
import json

from speech_info import result_json, listener, Speech
from read_json import read_speeches, read_listeners
from run_msbg import run_msbg, out_file, get_file
from run_whisper import run_whisper


def read_info(prompt, signal, response, whisper_signal, whisper_msbg, correctness_resp, correctness_whisper):
    result = result_json(prompt, signal, response, whisper_signal, whisper_msbg, correctness_resp, correctness_whisper)
    return result

def store_results(speeches: list[Speech], li_name, model):
    results = {}
    for speech in speeches:
        file = get_file(speech.signal)
        output = out_file(speech.signal, li_name)
        whisper_signal = run_whisper(file, model)
        whisper_msbg = run_whisper(output, model)
        result = read_info(speech.prompt, speech.signal, speech.response, 
                        whisper_signal, whisper_msbg, speech.correctness, 0)
        print(result.__dict__)
        results[speech.signal] = result.__dict__
    with open(li_name+'output.json','w') as json_file:
        json.dump(results, json_file)




def main():
    # speeches = read_json('')

    # create dict of listener
    speeches = []
    listeners = read_listeners()
    for li in listeners:
        speeches = read_speeches(li.name)
        li.set_speech(speeches)
    



    # run msbg
    for li in listeners:
        if not os.path.isfile(out_file(li.speeches[0].signal, li.name)):
            run_msbg(li.signals, li.name)

        # run whisper store results
        model = whisper.load_model("base")
        store_results(li.speeches, li.name, model)
        
    
    

if __name__=='__main__':
    main()
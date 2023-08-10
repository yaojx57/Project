# import jiwer 
import os
import whisper
import json

from score import check_wer, cal_RMSE
from speech_info import result_json, listener, Speech
from read_json import read_speeches, read_listeners
from run_msbg import run_msbg, out_file, get_file
from run_whisper import run_whisper


def read_info(signal, prompt,  response, whisper_signal, whisper_msbg, correctness_resp, correctness_whisper, score_signal, score_msbg):
    result = result_json(signal, prompt, response, whisper_signal, whisper_msbg, correctness_resp, correctness_whisper, score_signal, score_msbg)
    return result


def store_results(speeches: list[Speech], li_name, model):
    #TODO seperate system and listener
    #results = {li_name+li.speech.system:{}}

    actual_scores = []
    pre_scores = []
    results = {}
    for speech in speeches:
        file = get_file(speech.signal)
        output = out_file(speech.signal, li_name)
        
        whisper_signal = run_whisper(file, model)
        whisper_msbg = run_whisper(output, model)

        score_signal = check_wer(speech.prompt, whisper_signal)
        score_msbg = check_wer(speech.signal, whisper_msbg)

        result = read_info(speech.signal, speech.prompt, speech.response, 
                        whisper_signal, whisper_msbg, speech.correctness, 0, score_signal, score_msbg)
        
        print(speech.signal+' whisper process success')
        results[speech.signal] = result.__dict__

        pre_scores.append(score_msbg)
        actual_scores.append(speech.correctness)
    
    cal_RMSE(actual_scores, pre_scores)
    with open('output/'+li_name+'_output.json','w') as json_file:
        json.dump(results, json_file)




def main():
    # speeches = read_json('')

    # create dict of listener
    speeches = []
    listeners = read_listeners()

    # split system and doing whisper 
    for li in listeners:
        # print(li)
        speeches = read_speeches(li.name)
        li.set_speech(speeches)
    



    # run msbg
    for li in listeners:
        if len(li.speeches)>0:
            if not os.path.isfile(out_file(li.speeches[0].signal, li.name)):
                run_msbg(li.signals, li)

        # run whisper store results
        if not os.path.isfile('output/'+li.name+'_output.json'):
            model = whisper.load_model("base")
            store_results(li.speeches, li.name, model)
            
    
    

if __name__=='__main__':
    main()
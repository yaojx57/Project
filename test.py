# import jiwer 
import os
import whisper
import json
import logging

from score import check_wer, cal_RMSE
from speech_info import result_json, listener, Speech, System
from read_json import read_speeches, read_listeners
from run_msbg import run_msbg, out_file, get_file
from run_whisper import run_whisper

logging.basicConfig(filename='log.txt')
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG) 



def read_info(signal, prompt,  response, whisper_signal, whisper_msbg, correctness_resp, correctness_whisper, score_signal, score_msbg):
    result = result_json(signal, prompt, response, whisper_signal, whisper_msbg, correctness_resp, correctness_whisper, score_signal, score_msbg)
    return result


def store_results(speeches: list[Speech], name, model):
    #TODO seperate system and listener
    #results = {li_name+li.speech.system:{}}

    actual_scores = []
    pre_scores = []
    results = {}
    for speech in speeches:
        file = get_file(speech.signal)
        output = out_file(speech.signal)
        
        whisper_signal = run_whisper(file, model)
        whisper_msbg = run_whisper(output, model)

        score_signal = check_wer(speech.prompt, whisper_signal)
        score_msbg = check_wer(speech.signal, whisper_msbg)
        actual_score = check_wer(speech.prompt, speech.response)

        result = read_info(speech.signal, speech.prompt, speech.response, 
                        whisper_signal, whisper_msbg, speech.correctness, 0, score_signal, score_msbg)
        
        print(speech.signal+' whisper process success')
        results[speech.signal] = result.__dict__

        pre_scores.append(score_msbg)
        actual_scores.append(actual_score)
    
    rmse = cal_RMSE(actual_scores, pre_scores)
    logger.info(name+' RMSE score is: '+str(rmse))
    with open('output/'+name+'_output.json','w') as json_file:
        json.dump(results, json_file)



# run msbg according to listners' audiogram
def msbg():
    # speeches = read_json('')

    # create dict of listener
    speeches = []
    listeners = read_listeners()

    # split system and doing whisper 
    for li in listeners:
        # print(li)
        speeches = read_speeches(li.name, None, type='l')
        li.set_speech(speeches)
    
    # run msbg
    for li in listeners:
        if len(li.speeches)>0:
            # if not os.path.isfile(out_file(li.speeches[0].signal)):
            run_msbg(li.signals, li)
    
    return listeners



def sort_listeners():
    speeches = []
    listeners = read_listeners()
    for li in listeners:
        # print(li)
        speeches = read_speeches(li.name, None, type='l')
        li.set_speech(speeches)
        

    for li in listeners:
    # run whisper store results
        if not os.path.isfile('output/'+li.name+'_output.json'):
            model = whisper.load_model("base.en")
            name = 'Listener-----'+ li.name
            store_results(li.speeches, name, model)



def sort_system():

    speeches = read_speeches(None, None, None)
    names = {}
    systems = []

    for speech in speeches:
        if speech.system in names.keys():
            names[speech.system].append(speech)
        else:
            names[speech.system] = [speech]
    
    for k,v in names.items():
        # print(k)
        temp = System(k)
        temp.set_speeches(v)
        systems.append(temp)
    
    for system in systems:
        if not os.path.isfile('output/'+system.system+'_output.json'):
            model = whisper.load_model('base')
            name = 'System-----'+ system.system
            store_results(system.speeches, name, model)


def main():
    sort_system()
    # sort_listeners()
    # msbg()

            
    
    

if __name__=='__main__':
    main()
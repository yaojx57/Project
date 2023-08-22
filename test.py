# import jiwer 
import os
import whisper
import json
import logging
import random

from datetime import datetime
from score import check_wer, cal_RMSE, avg
from speech_info import result_json, listener, Speech, System
from read_json import read_speeches, read_listeners
from run_msbg import run_msbg, out_file, get_file
from run_whisper import run_whisper, uniquify

# time = time.asctime()
time = './log_file/{:%m-%d_%H-%M}.log'.format(datetime.now())

source_file = open(uniquify('./output/output.txt'), 'w')
print('{:^10}{:^15}{:^15}{:^15}{:^15}{:^15}'.format('System', 'RMSE', 'AVG Actual', 'AVG Pre', 'AVG Match','AVG Whisper'), file=source_file)


logging.basicConfig(filename=time, format='%(asctime)s - %(levelname)s ------- %(message)s')
logger=logging.getLogger() 
logger.setLevel(logging.INFO) 


def random_sample(l: list, ratio: float=0.5):
    length = len(l)
    random.shuffle(l)
    l = l[ : int(ratio*length) ]
    return l


def read_info(signal, prompt,  response, whisper_signal, whisper_msbg, correctness_resp, correctness_whisper, score_signal, score_msbg, match_correction):
    result = result_json(signal, prompt, response, whisper_signal, whisper_msbg, correctness_resp, correctness_whisper, score_signal, score_msbg, match_correction)
    return result


def store_results(speeches: list[Speech], name, model, ratio, path: str=None):
    #TODO seperate system and listener
    #results = {li_name+li.speech.system:{}}
    speeches = random_sample(speeches, ratio)

    actual_scores = []
    pre_scores = []
    whispers = []

    matchs = []
    results = {}
    for speech in speeches:
        file = get_file(speech.signal, path)
        output = out_file(speech.signal, path)
        
        whisper_signal = run_whisper(file, model)
        whisper_msbg = run_whisper(output, model)

        score_signal = check_wer(speech.prompt, whisper_signal)# Score of whisper prediction and Signal
        
        score_msbg = check_wer(speech.prompt, whisper_msbg)# Score of Signal and Prediction

        actual_score = check_wer(speech.prompt, speech.response)# Score of Listner's response and signal

        match_correction = check_wer(speech.response, whisper_msbg)# Score of Listener and Prediction

        result = read_info(speech.signal, speech.prompt, speech.response, 
                        whisper_signal, whisper_msbg, speech.correctness, 0, score_signal, score_msbg, match_correction)
        
        logging.info(speech.signal+' whisper process success')
        logging.info('Actual score is: {} and Score msbg is: {}'.format(actual_score, score_msbg))
        results[speech.signal] = result.__dict__

        whispers.append(score_signal)
        pre_scores.append(score_msbg)
        actual_scores.append(actual_score)
        matchs.append(match_correction)
        
    
    rmse = cal_RMSE(actual_scores, pre_scores)
    avg_whisper = avg(whispers)
    avg_prediction = avg(pre_scores)
    avg_correction = avg(matchs)
    avg_actual = avg(actual_scores)
    
    print('{:^10}{:^15}{:^15}{:^15}{:^15}{:^15}'.format(name, rmse, avg_actual, avg_prediction, avg_correction,avg_whisper), file=source_file)

    logger.info(name+ ' RMSE score is: '+ str(rmse))
    logger.info(name+ ' Average Correct score is: '+ str(avg_correction))

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
            run_msbg(li.signals, li)
    
    return listeners



def sort_listeners(model: str=None, ratio: float=0.5, path: str=None):
    speeches = []
    listeners = read_listeners()


    for li in listeners:
        speeches = read_speeches(li.name, None, type='l')
        li.set_speech(speeches)
        
    
    flag = 0
    for li in listeners:
        flag += 1
    # run whisper store results
        if not os.path.isfile('output/'+li.name+'_output.json'):
            model = whisper.load_model("base.en" if model==None else model)
            name = 'Listener-'+ li.name
            store_results(li.speeches, name, model, ratio, path)



def sort_system(model: str=None, ratio: float=0.5, path: str=None):

    speeches = read_speeches(None, None, None)
    names = {}
    systems = []

    for speech in speeches:
        if speech.system in names.keys():
            names[speech.system].append(speech)
        else:
            names[speech.system] = [speech]
    
    for k,v in names.items():
        temp = System(k)
        temp.set_speeches(v)
        systems.append(temp)
    
    for system in systems:
        if not os.path.isfile('output/'+system.system+'_output.json'):
            model = whisper.load_model('base' if model==None else model)
            name = 'System-'+ system.system
            store_results(system.speeches, name, model, ratio, path)


def main():
    # if args['']:
    #     pass
    # sort_system()
    # sort_listeners()
    # msbg()
    return 1
            
    
    

if __name__=='__main__':
    main()
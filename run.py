# import jiwer 
import os
import whisper
import json
import logging
import random

from datetime import datetime
from score import check_wer, cal_RMSE, avg
from speech_info import result_json, listener, Speech, System
from read_json import read_speeches, read_listeners, print_now
from run_msbg import run_msbg, out_file, get_file
from run_whisper import run_whisper, uniquify

# time = time.asctime()
time = './log_file/{:%m-%d_%H-%M}.log'.format(datetime.now())

source_file = open(uniquify('./output/output.txt'), 'w')

logging.basicConfig(filename=time, format='%(asctime)s - %(levelname)s ------- %(message)s')
logger=logging.getLogger() 
logger.setLevel(logging.INFO) 


def random_sample(l: list, ratio: float=0.5):
    length = len(l)
    random.shuffle(l)
    l = l[ : int(ratio*length) ]
    return l


def read_info(signal, prompt, response, whisper_signal, whisper_msbg, correctness_resp, correctness_pred, score_signal, score_msbg, match_msbg, match_whisper):
    result = result_json(signal, prompt, response, whisper_signal, whisper_msbg, correctness_resp, correctness_pred, score_signal, score_msbg, match_msbg, match_whisper)
    return result


def store_results(speeches: list[Speech], name, model, ratio, path: str=None, level: str='l'):
    #results = {li_name+li.speech.system:{}}
    speeches = random_sample(speeches, ratio)
    print('Start Process '+name)

    actual_scores = []
    scores_whisper = []
    scores_pred = []
    matchs_pred = []
    matchs_whisper = []

    results = {}
    for speech in speeches:
        file = get_file(speech.signal, path)
        output = out_file(speech.signal, path, level)
        
        whisper_signal = run_whisper(file, model)
        whisper_msbg = run_whisper(output, model)
        
        score_pred = check_wer(speech.prompt, whisper_msbg)# Score of Signal and Prediction

        score_whisper = check_wer(speech.prompt, whisper_signal)# Score of whisper prediction and Signal


        # score_listen = check_wer(speech.prompt, speech.response)# Score of Listner's response and signal

        match_pred = check_wer(speech.response, whisper_msbg)# Score of Listener and Prediction

        match_whisper = check_wer(speech.response, whisper_signal)# Score of Prediction without MSBG and Whisper

        result = read_info(speech.signal, speech.prompt, speech.response, 
                        whisper_signal, whisper_msbg, speech.correctness, score_pred, score_whisper, score_pred, match_pred, match_whisper)
        
        logging.info(speech.signal+' whisper process success')
        logging.info('Actual score is: {} and Score msbg is: {}'.format(speech.correctness, score_pred))
        results[speech.signal] = result.__dict__

        actual_scores.append(speech.correctness)

        scores_pred.append(score_pred)
        scores_whisper.append(score_whisper)
        matchs_pred.append(match_pred)
        matchs_whisper.append(match_whisper)
        
    
    rmse = cal_RMSE(actual_scores, scores_pred)
    rmse_whisper = cal_RMSE(actual_scores, scores_whisper)

    avg_actual = avg(actual_scores)
    avg_whisper = avg([a - b for a,b in zip(matchs_pred,matchs_whisper)])
    avg_prediction = avg(scores_pred)
    avg_correction = avg(matchs_pred)
    
    print_now(source_file, '{:^10}{:^15.2f}{:^15.2f}{:^15.2f}{:^15.2f}{:^15.2f}{:^15.2f}'.format(name, rmse, rmse_whisper, avg_whisper, avg_actual, avg_prediction, avg_correction, ))

    logger.info(name+ ' RMSE score is: '+ str(rmse))
    logger.info(name+ ' Average Correct score is: '+ str(avg_correction))

    with open('json_output/'+name+'_output.json','w') as json_file:
        json.dump(results, json_file)



# run msbg according to listners' audiogram
def msbg(path: str=None, level: str='l'):
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
            run_msbg(li.signals, li, path, level)
            print(1)
    
    return listeners



def sort_listeners(model_name: str=None, ratio: float=0.5, path: str=None, level: str='l'):

    print_now(source_file, 'Argument: Ratio: {},  Model: {}, Level: {}\n'.format(ratio, model_name, level))
    print_now(source_file, '{:^10}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}'.format('System', 'RMSE', 'RMSE_whisper','AVG Whisper' 'AVG Actual', 'AVG Pre', 'AVG Match'))


    speeches = []
    listeners = read_listeners()


    for li in listeners:
        speeches = read_speeches(li.name, None, type='l')
        li.set_speech(speeches)
        
    
    flag = 0
    for li in listeners:
        flag += 1
    # run whisper store results
        if not os.path.isfile('json_output/'+li.name+'_'+level+'_output.json'):
            model = whisper.load_model(model_name)
            name = li.name+'_'+level
            if len(li.speeches)>0:
                store_results(li.speeches, name, model, ratio, path, level)
            else:
                continue
        else:
            print('pass process' + li.name)


def sort_system(model_name: str=None, ratio: float=0.5, path: str=None, level: str='l'):

    print_now(source_file, 'Argument: Ratio: {},  Model: {}, Level: {}\n'.format(ratio, model_name, level))
    print_now(source_file, '{:^10}{:^15}{:^15}{:^15}{:^15}{:^15}{:^15}'.format('System', 'RMSE', 'RMSE_whisper','AVG Whisper', 'AVG Actual', 'AVG Pre', 'AVG Match'))


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
        if not os.path.isfile('json_output/'+system.system+'_'+level+'_output.json'):
            model = whisper.load_model(model_name)
            name = system.system+'_'+level
            if len(system.speeches)>0:
                store_results(system.speeches, name, model, ratio, path, level)
            else:
                continue
        else:
            print('pass process' + system.system)


def main():
    # if args['']:
    #     pass
    # sort_system()
    # sort_listeners()
    # msbg()
    print('{:^10.4f}'.format(0.3143712923799367), file=source_file)
    return 1
            
    
    

if __name__=='__main__':
    main()
import json
import os
from speech_info import Speech, listener, result_json

def read_result(filename):
    x = []
    y = []
    with open(filename) as json_data:
        json_dict = json.load(json_data)
        json_data.close()
    for i in json_dict.keys():
        x.append(json_dict[i]['correctness_pred'])
        y.append(json_dict[i]['correctness_resp'])
    return x,y


def get_train_data(type: str='l', level: str='l'):
    X = []
    Y = []
    if type == 'l':
        listener_list = ['L0200','L0201','L0202','L0206','L0208','L0209','L0212','L0215','L0216','L0217','L0218','L0219','L0220','L0221','L0222','L0224','L0225','L0227','L0229','L0231','L0235','L0236','L0239','L0240','L0241','L0242','L0243']
        for li in listener_list:
            filename = 'past_output/{}_{}_output.json'.format(li, level)
            x,y = read_result(filename)
            X.extend(x)
            Y.extend(y)
        return X,Y
    elif type == 's':
        system_list = ['E001','E003','E005','E007','E009','E010','E013','E018','E019','E021']
        for li in system_list:
            filename = 'past_output/{}_{}_output.json'.format(li, level)
            x,y = read_result(filename)
            X.extend(x)
            Y.extend(y)
        return X,Y
    else:
        return False


def read_speech(prompt, scene, n_words, hits, listener, system, correctness, response, volume, signal):
    speech = Speech(prompt, scene, n_words, hits, listener, system, correctness, response, volume, signal)
    return speech


def read_listeners():
    listeners = []
    with open('json_data/listeners.json') as listener_data:
        json_data = json.load(listener_data)
    for k,v in json_data.items():
        l = listener(v['name'], v['audiogram_cfs'], v['audiogram_levels_l'], v['audiogram_levels_r'])   
        listeners.append(l)
    # print(listeners)
    return listeners


def read_speeches(listener_id, system_id, type):
    speeches = []
    with open('json_data/train.json') as json_data:
        json_list = json.load(json_data)
        json_data.close()
    for i in json_list:
        prompt = i['prompt']
        scene = i['scene']
        n_words = i['n_words']
        hits = i['hits']
        listener = i['listener']
        if type == 'l' and listener != listener_id:
            continue
        system = i['system']
        if type == 's' and system != system_id:
            continue
        correctness = i['correctness']
        response = i['response']
        volume = i['volume']
        signal = i['signal']
        speech = read_speech(prompt, scene, n_words, hits, listener, system, correctness, response, volume, signal)
        # print(speech.__dict__)
        speeches.append(speech)
    
    return speeches


def write_now(filep, msg):
    """Write msg to the file given by filep, forcing the msg to be written to the filesystem immediately (now).

    Without this, if you write to files, and then execute programs
    that should read them, the files will not show up in the program
    on disk.
    """
    filep.write(msg)
    filep.flush()
    # The above call to flush is not enough to write it to disk *now*;
    # according to https://stackoverflow.com/a/41506739/257924 we must
    # also call fsync:
    os.fsync(filep)


def print_now(filep, msg):
    """Call write_now with msg plus a newline."""
    write_now(filep, msg + '\n')
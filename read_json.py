import json
import os
from speech_info import Speech, listener


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
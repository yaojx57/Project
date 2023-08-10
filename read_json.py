import json
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


def read_speeches(listener_id):
    speeches = []
    with open('json_data/CEC1.train.1.json') as json_data:
        json_list = json.load(json_data)
        json_data.close()
    for i in json_list:
        prompt = i['prompt']
        scene = i['scene']
        n_words = i['n_words']
        hits = i['hits']
        listener = i['listener']
        if listener != listener_id:
            continue
        system = i['system']
        # if system != "E001":
        #     continue
        correctness = i['correctness']
        response = i['response']
        volume = i['volume']
        signal = i['signal']
        speech = read_speech(prompt, scene, n_words, hits, listener, system, correctness, response, volume, signal)
        # print(speech.__dict__)
        speeches.append(speech)
    
    return speeches
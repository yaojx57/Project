import json
from speech_info import Speech, listeners


def read_speech(prompt, scene, n_words, hits, listener, system, correctness, response, volume, signal):
    speech = Speech(prompt, scene, n_words, hits, listener, system, correctness, response, volume, signal)
    return speech


def read_listeners(name, cfs, l, r):
    with open('json_data/listeners.json') as listener_data:
        json_data = json.loads(listener_data)

    # listener = listeners(name, cfs, l, r)   
    return json_data


def read_json(file):
    speeches = []
    with open(file) as json_data:
        json_list = json.load(json_data)
        json_data.close()
    for i in json_list:
        prompt = i['prompt']
        scene = i['scene']
        n_words = i['n_words']
        hits = i['hits']
        listener = i['listener']
        if listener != "L0200":
            continue
        system = i['system']
        if system != "E001":
            continue
        correctness = i['correctness']
        response = i['response']
        volume = i['volume']
        signal = i['signal']
        speech = read_speech(prompt, scene, n_words, hits, listener, system, correctness, response, volume, signal)
        print(speech.__dict__)
        speeches.append(speech)
    
    return speeches
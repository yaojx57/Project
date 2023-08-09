# "prompt": "i don't want us to apportion blame she said",
#     "scene": "S08547",
#     "n_words": 9,
#     "hits": 4,
#     "listener": "L0239",
#     "system": "E001",
#     "correctness": 44.4444444444,
#     "response": "i don't want to have to report he said",
#     "volume": 56,
#     "signal": "S08547_L0239_E001"

class Speech:
    def __init__(self, prompt, scene, n_words, hits, listener, system, correctness, response, volume, signal) -> None:
        self.prompt = prompt
        self.scene = scene
        self.n_words = n_words
        self.hits = hits
        self.listener = listener
        self.system = system
        self.correctness = correctness
        self.response = response
        self.volume = volume
        self.signal = signal


class listeners:
    def __init__(self, name, audiogram_cfs, audiogram_levels_l, audiogram_levels_r) -> None:
        self.listener = name
        self.freq = audiogram_cfs
        self.level_l = audiogram_levels_l
        self.level_r = audiogram_levels_r


class scene:
    def __init__(self, room_name) -> None:
        pass


class result_json:
    def __init__(self, prompt, signal, response, whisper_signal, whisper_msbg, correctness_resp, correctness_whisper) -> None:
        self.prompt = prompt
        self.signal = signal
        self.response = response
        self.whisper_signal = whisper_signal
        self.whisper_msbg = whisper_msbg
        self.correctness_resp = correctness_resp
        self.correctness_whisper = correctness_whisper
    
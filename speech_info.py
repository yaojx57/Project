from clarity.utils.audiogram import Audiogram

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


class listener:
    def __init__(self, name, audiogram_cfs, audiogram_levels_l, audiogram_levels_r) -> None:
        self.name = name
        self.freq = audiogram_cfs
        self.level_l = audiogram_levels_l
        self.level_r = audiogram_levels_r
        self.signals = []
        self.speeches = []
    
    def get_audiogram(self):
        audiogram = Audiogram(

            #TODO average listener level
            levels = self.level_l,
            frequencies = self.freq
        )
        return audiogram


    def set_speech(self, speeches: list[Speech]):
        for speech in speeches:
            self.signals.append(speech.signal)
        self.speeches = speeches
    

    def create_signals():
         
        pass


    @classmethod
    def avg_level(self):
        pass


class scene:
    def __init__(self, room_name) -> None:
        pass


class result_json:
    def __init__(self, signal, prompt, response, whisper_signal, whisper_msbg, correctness_resp, correctness_whisper, score_signal, score_msbg) -> None:
        self.signal = signal
        
        self.prompt = prompt
        self.response = response

        self.whisper_signal = whisper_signal # using whisper on signal
        self.whisper_msbg = whisper_msbg # using msbg and whisper on signal

        self.correctness_resp = correctness_resp
        self.correctness_whisper = correctness_whisper # difference between prompt and whisper_msbg

        self.score_signal = score_signal # difference between prompt and whisper signal
        self.score_msbg = score_msbg # difference between response and msbg_whisper
        
    
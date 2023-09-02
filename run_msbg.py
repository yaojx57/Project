import argparse
import os

from speech_info import listener

from os import listdir
from os.path import isfile, join

from clarity.utils.audiogram import Audiogram
from clarity.evaluator.msbg.msbg import Ear
from clarity.utils.file_io import read_signal, write_signal


# get input files name 
def get_file(signal, path: str=None):
    if path:
        filename = path+'/clarity_CPC2_data/clarity_data/HA_outputs/signals/CEC1/'+signal+'.wav'
    else:
        filename = '../../data/clarity_CPC2_data/clarity_data/HA_outputs/signals/CEC1/'+signal+'.wav'
    return filename


# output files generate
def out_file(signal, path: str=None, level: str='l'):
    if path:
        folder = path + '/output_' + level +'/'
    else:
        folder = '../../data/output_{}/'.format(level)
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = folder + '/' + signal + '_output.wav'
    return filename


def msbg(input, output, audiogram):
    sample_rate = 44100  # The sampling rate to use


    # Read signal from wav file
    signal = read_signal(input, sample_rate)

    # The audiogram for the listener
    # audiogram = Audiogram(
    #     levels=[40, 40, 45, 50, 55, 60, 65, 70],
    #     frequencies=[250, 500, 1000, 2000, 3000, 4000, 6000, 8000],
    # )

    # Initialize the ear and process the signal
    ear = Ear(equiv_0db_spl=80)
    ear.set_audiogram(audiogram)
    out = ear.process(signal)

    # Write the processed signal to a wav file
    write_signal(output, out[0], sample_rate)


def run_msbg(signals, li: listener, path: str=None, level: str='l'):
    audiogram = li.get_audiogram(level)
    for signal in signals:
        file = get_file(signal, path)
        output = out_file(signal, path, level)
        if not os.path.isfile(out_file(signal, path, level)):
            msbg(file, output, audiogram)
            print(signal+' transfer msbg success')




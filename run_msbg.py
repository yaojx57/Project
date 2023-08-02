import argparse
from os import listdir
from os.path import isfile, join

from clarity.utils.audiogram import Audiogram
from clarity.evaluator.msbg.msbg import Ear
from clarity.utils.file_io import read_signal, write_signal


# get input files name 
def get_files(infile):
    pass


# output files generate
def out_files(infile):
    pass


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("infile")
    parser.add_argument("outfile")
    args = parser.parse_args()

    sample_rate = 44100  # The sampling rate to use

    files = [f for f in list(args.infile) if isfile(join(args.infile, f))]


    # Read signal from wav file
    for i in range()
    signal = read_signal(args.infile, sample_rate)

    # The audiogram for the listener
    audiogram = Audiogram(
        levels=[40, 40, 45, 50, 55, 60, 65, 70],
        frequencies=[250, 500, 1000, 2000, 3000, 4000, 6000, 8000],
    )

    # Initialize the ear and process the signal
    ear = Ear(equiv_0db_spl=80)
    ear.set_audiogram(audiogram)
    out = ear.process(signal)

    # Write the processed signal to a wav file
    write_signal(args.outfile, out[0], sample_rate)


if __name__ == "__main__":
    main()

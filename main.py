from run_msbg import run_msbg
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', action="store_true", help='test mode', default=True)
parser.add_argument('-msbg', '--msbg', action="run_msbg", help='run msbg', required=True)
parser.add_argument('-whisper', '--whisper', action='run_whisper', help='run_whisper', required=True)
parser.add_argument('-i', '--input', type=str, help='input folder', required=True)
parser.add_argument('-o', '--output', type=str, help='out folder')
parser.add_argument('')
args = vars(parser.parse_args())

def main():
    if args['msbg']:
        run_msbg()
    pass

if __name__ == "__main__":
    main()
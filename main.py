import argparse

from test import sort_listeners, sort_system, msbg


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', help='test mode', default=True)
parser.add_argument('-msbg', '--msbg', help='run msbg', type=bool)
parser.add_argument('-whisper', '--whisper', help='run_whisper')
parser.add_argument('-ratio', '--ratio', help='set ratio',default=0.5, type=float)
parser.add_argument('-model', '--model', help='set model', default='base.en')
parser.add_argument('-level', '--level', help='set audiogram level',default='l')
parser.add_argument('-path', '--path', help='file path')
args = vars(parser.parse_args())

def main():
    print(args)
    if args['path']:
        path = args['path']
    else:
        path = None

    if args['test']:
        sample_rate = 0.5
        model = 'base.en'
        level = 'l'
    
    if args['model']:
        model = args['model']

    if args['level']:
        level = args['level']

    if args['ratio']:
        sample_rate = args['ratio']

    if args['msbg'] and not args['whisper']:
        print('MSBG processing!')
        msbg(path, level)
    elif not args['msbg'] and args['whisper']:
        if args['whisper'] == 'l':
            print('Whisper Listener processing!')
            sort_listeners(model, sample_rate, path)
        elif args['whisper'] == 's':
            print('Whisper System processing!')
            sort_system(model, sample_rate, path)
    
    return 0
    

if __name__ == "__main__":
    main()
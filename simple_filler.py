#!/usr/bin/python3

MESSAGE = 'Error Block!!: This is my original error pattern'

import argparse 
import os.path
import subprocess
import shlex
import time


def simple_timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print('Took {} seconds to complete'.format(end_time - start_time))
        return result
    return wrapper


@simple_timer
def main():

    parser = argparse.ArgumentParser(description='Fill something with simple text message along block size')
    parser.add_argument('target', help='Target device file')
    parser.add_argument('--blocksize', default=512, type=int, help='Block size. Default=512')
    args = parser.parse_args()


    spaces = args.blocksize - len(MESSAGE) - 1 
    
    error_txt = MESSAGE
    for i in range(spaces):
        error_txt += ' '

    cmd_1 = 'yes "{}"'.format(error_txt)
    cmd_2 = 'sudo dd of={} bs={}'.format(os.path.abspath(args.target), args.blocksize)
    
    process_1 = subprocess.Popen(shlex.split(cmd_1), stdout=subprocess.PIPE)
    process_2 = subprocess.Popen(shlex.split(cmd_2), stdin=process_1.stdout)
    
    process_2.wait()


if __name__ == '__main__':
    main()

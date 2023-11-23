#!/usr/bin/python3

# -----------------------------------------------------------------------------
# TODO
# - デバイスのサイズを調べてして書ききれるか確認する
# -----------------------------------------------------------------------------


MESSAGE = 'Error Block!!: This is my original error pattern'
SECTOR_SIZE = 512


import argparse 
import os.path
import subprocess
import shlex
import time
import sys



# ddコマンドが時間も出してくれるのであまり意味がない
def simple_timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print('Took {0:.1f} seconds to complete'.format(end_time - start_time))
        return result
    return wrapper



@simple_timer
def main():

    parser = argparse.ArgumentParser(description='Fill something with simple text message along block size')
    parser.add_argument('target', help='Target device file')
    parser.add_argument('--blocksize', default=512, type=int, help='Block size used in dd command. Default=512')
    args = parser.parse_args()


    spaces = SECTOR_SIZE - len(MESSAGE) 
    
    error_txt = MESSAGE
    for i in range(spaces):
        error_txt += ' '

    q, r = divmod(args.blocksize, SECTOR_SIZE)
    if r != 0:
        print('Invalid parameter: input blocksize is not aligned to sector size{}'.format(SECTOR_SIZE))
        sys.exit()

    error_block = ''
    for i in range(q):
        error_block += error_txt


    cmd_1 = 'yes "{}"'.format(error_txt)
    cmd_2 = 'tr -d "\n"'
    cmd_3 = 'sudo dd of={} bs={} status=progress'.format(os.path.abspath(args.target), args.blocksize)
    
    process_1 = subprocess.Popen(shlex.split(cmd_1), stdout=subprocess.PIPE)
    process_2 = subprocess.Popen(shlex.split(cmd_2), stdin=process_1.stdout, stdout=subprocess.PIPE)
    process_3 = subprocess.Popen(shlex.split(cmd_3), stdin=process_2.stdout)
    
    process_3.wait()

    print('\nFilling has been done!!')

if __name__ == '__main__':
    main()

#!/usr/bin/python3


DEFAULT_MESSAGE = 'Error Block!!: This is my original error pattern'


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

    parser = argparse.ArgumentParser(description='Fill a disk with a simple text message per sector. Filling a partition or a single file is not supported.')
    parser.add_argument('target', help='Target device file. Please specify like /dev/sda')
    parser.add_argument('--blocksize', default=512, type=int, help='Block size used in dd command. Default=512')
    parser.add_argument('--message', default=DEFAULT_MESSAGE, help='Message written to a sector. Default={}'.format(DEFAULT_MESSAGE))
    args = parser.parse_args()


    disk_name = args.target.split('/')[-1]
    if not disk_name in os.listdir('/sys/block'):
        print('[Invalid parameter]: Disk name was not found under /sys/block. Please specify disk name as /dev/sda.')
        sys.exit()


    with open('/sys/block/{}/queue/hw_sector_size'.format(disk_name)) as f:
        sector_size = int( f.read().strip() )

    with open('/sys/block/{}/size'.format(disk_name)) as g:
        block_count = int( g.read().strip() )


    disk_size_in_byte = sector_size * block_count


    if disk_size_in_byte % args.blocksize != 0:
        print('[Invalid parameter]: Specified blocksize is not aligned to disk size.')
        print('sector size = {}'.format(sector_size))
        print('block count = {}'.format(block_count))
        sys.exit()


    spaces = sector_size - len(args.message) 
    if spaces < 0:
        print('[Invalid parameter]: Too long message. Specified messgae is longer than secotr size.')
        sys.exit()


    pattern_txt = args.message + ' ' * spaces

    q, r = divmod(args.blocksize, sector_size)
    if r != 0:
        print('[Invalid parameter]: Specified blocksize is not aligned to sector size')
        print('sector size = {}'.format(sector_size))
        sys.exit()

    pattern_block = pattern_txt * q   


    cmd_1 = 'yes "{}"'.format(pattern_txt)
    cmd_2 = 'tr -d "\n"'
    cmd_3 = 'sudo dd of={} bs={} status=progress'.format(os.path.abspath(args.target), args.blocksize)
    
    process_1 = subprocess.Popen(shlex.split(cmd_1), stdout=subprocess.PIPE)
    process_2 = subprocess.Popen(shlex.split(cmd_2), stdin=process_1.stdout, stdout=subprocess.PIPE)
    process_3 = subprocess.Popen(shlex.split(cmd_3), stdin=process_2.stdout)
    
    process_3.wait()

    print('\nFilling has been done!!')




if __name__ == '__main__':
    main()

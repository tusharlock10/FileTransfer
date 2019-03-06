import json
import os
import random
import sys
import time
import zlib
from socket import *

import tj

os.chdir(os.path.dirname(sys.argv[0]))

DIRECTORY = 'Received'

os.makedirs(DIRECTORY, exist_ok=1)


class Receiver:
    global DIRECTORY

    def __init__(self):
        print('  ** RECEIVER **')
        print('This module will Receive files ...\n')

        self.host = self.__get_host()
        self.port = self.__get_port()
        print('\nEnter both of these correctly in the sender...')
        self.addr = (self.host, self.port)
        self.buff = 8 * 1024  # Its buffer is a little more than sender, to avoid the files getting corrupt
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(self.addr)
        self.files = self.get_info()
        self.wait_buffer = 0.3

    @staticmethod
    def __get_host():
        host = gethostname()
        ip = gethostbyname(host)
        print('The IP Address of Receiver is: %s' % ip)
        return ip

    @staticmethod
    def __get_port():
        port = random.choice(list(range(3000, 30001)))
        print('The port number is: %s' % port)
        return port

    def get_info(self):
        '''Gets the files metadata from sender'''
        data, addr = self.socket.recvfrom(self.buff)  # Here files is in cmp, bin, json
        print('Got the metadata...')
        data = zlib.decompress(data)  # bin, json
        # print(data)
        data = data.decode()  # json left
        files = json.loads(data)  # files dictionary {file_1 : size_1,   file_2 : size_2 ...}

        return files

    def __get_file(self, file):

        tt = time.time()
        file_new = DIRECTORY + file
        dirname = os.path.dirname(file_new)
        os.makedirs(dirname, exist_ok=1)

        f = open(file_new, 'wb')
        while 1:
            data, addr = self.socket.recvfrom(self.buff)
            f.write(data)
            if data == b'':
                break
        f.close()

        tt = (time.time() - tt)
        size = self.files[file]

        try:
            speed = tj.convert_bytes(size // tt)
            tt = round(tt, 3)
            s = 'took %ss, avg. speed - %s/s' % (tt, speed)
        except:
            s = "file was small, didn't do measurements! "

        if os.path.getsize(file_new) != self.files[file]:
            error = '  THE RECEIVED FILE WAS CORRUPT, RETRY FOR THIS FILE...'
            error = tj.color_text(error, text_color='RED')
        else:
            error = '  File is successfully received...'
            error = tj.color_text(error, text_color='GREEN')

        print(' | Received, %s' % s, end='\n')
        print('%s' % error)

    def get_files(self):
        for file in self.files:
            print('Receiving file: %s' % (DIRECTORY + file), end='')
            self.__get_file(file)

    def close(self):
        print('\nFiles received, Closing the connection and quitting!')
        self.socket.close()
        input('Enter to quit...')


R = Receiver()
R.get_files()
R.close()

import json
import os
import sys
import time
import zlib
from random import randint
from socket import *

import tj

dirname = os.path.dirname(sys.argv[0])
if dirname != '': os.chdir(dirname)

DIRECTORY = 'Received'
os.makedirs(DIRECTORY, exist_ok=True)


class Receiver:
    def __init__(self):
        self.host = self.__get_host()  # To get the ip address of the Receiver (server)
        self.port = 12345  # self.__get_port()  # To get a random port number
        self.buffer = 1300  # Buffer is set to 1300 to save file from corruption

        self.socket = socket(AF_INET, SOCK_STREAM)  # Made TCP socket
        self.socket.bind((self.host, self.port))  # Binded the socket
        self.socket.listen(1)  # Only 1 user will connect

        self.partner, self.partner_addr = self.socket.accept()  # Waiting for client to accept
        print(f'{gethostbyaddr(self.partner_addr[0])[0]} ({self.partner_addr[0]}) is now connected')
        self.partner.settimeout(0.05)

    @staticmethod
    def __get_host():
        '''Function to get the IP address of the Receiver'''
        host = gethostname()
        ip = gethostbyname(host)
        print('The IP Address of Receiver is: %s' % ip)
        return ip

    @staticmethod
    def __get_port():
        '''Gives a random number for port'''
        port = randint(4000, 25000)
        print('The port number of Receiver is: %s' % port)
        return port

    @staticmethod
    def convert_to_percent(num, total):
        '''Converts to percentage'''
        percent = num * 100 / total
        return int(percent)

    @staticmethod
    def show_progress(percent, time_elapsed=0, got_data=0):
        '''Display progress of percentage out of 50'''

        if percent != 100:
            try:
                speed = got_data // time_elapsed  # Gets the speed in the "Fancy" format
                speed = tj.convert_bytes(speed) + r'/s'  # Adds /s to speed
            except:
                speed = 'N/A'
            print('  --  %-50s %s | Speed: %s' % ('#' * (percent // 2), f'{percent}%', speed), end='\r')
        else:
            print('%s' % ' ' * 85, end='\r')
        return percent

    @staticmethod
    def convert_D(D):
        '''Converts the file paths of D, in the correct format'''
        D_new = {}
        for i in D:
            value = D[i]

            # not using os.path.join as it gives incorrect results
            if 'win32' in sys.platform:
                filename = os.path.abspath(DIRECTORY + '\\' + i)
            else:
                filename = DIRECTORY + i
            temp = {filename: value}
            D_new.update(temp)
        return D_new

    def get_files_metadata(self):
        data_compressed = b''
        self.partner.settimeout(None)
        run = True
        while run:
            try:
                i = self.partner.recv(self.buffer)
            except:
                run = False
            self.partner.settimeout(0.05)
            if i == b'': run = False
            data_compressed += i

        try:
            data = zlib.decompress(data_compressed).decode()
            print('Metadata is intact')
            error = b'CONFIRMED'
        except:
            print('Metadata is corrupt')
            error = b'CORRUPT'
            data = '{}'
        self.partner.send(error)
        D = json.loads(data)

        D_new = self.convert_D(D)
        return D_new

    def get_buffer(self, size_remaining):
        '''Gives, how huch buffer we need to give to the socket.recv function.
        Instead of waiting and depending on the Sender, we keep the track of
        the data which is sent.'''
        b = self.buffer
        if size_remaining < b:
            return size_remaining
        else:
            return b

    def get_file(self, filename, size):
        '''This function gets the file data from the sender'''
        dirname = os.path.dirname(filename)  # To make the directory of the file
        os.makedirs(dirname, exist_ok=True)  # Makes the directory of the file

        size_remaining = size
        print(os.path.abspath(filename))
        f = open(filename, 'wb')

        done = 0
        done_percent = None
        t = time.time()
        got_data = 0

        while size_remaining:
            var_buffer = self.get_buffer(size_remaining)
            data = self.partner.recv(var_buffer)

            l = len(data)
            done += l
            got_data += l
            percent = self.convert_to_percent(done, size)

            if percent != done_percent:
                time_elapsed = time.time() - t
                self.show_progress(percent, time_elapsed, got_data)

                done_percent = percent
                got_data = 0
                t = time.time()

            f.write(data)
            f.flush()
            size_remaining -= var_buffer

        f.close()
        self.show_progress(100)
        print('I got', done, 'bytes')
        if done == size:
            return True
        else:
            return False

    def get_files(self, D):
        n = len(D)
        self.partner.settimeout(None)
        for i, file in enumerate(list(D.keys())):

            size = D[file]
            size_fancy = tj.convert_bytes(size)
            print(f'\n Receiving file {i + 1}/{n}\n\t{file} - ({size_fancy})')
            result = self.get_file(file, size)

            if result:
                print(' Received file successfully')
            else:
                print(' --- FILE RECEIVED IS CORRUPT ---')

    def close(self):
        self.partner.close()


R = Receiver()
D = R.get_files_metadata()
R.get_files(D)
R.close()

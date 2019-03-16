import json
import os
import sys
import time
import zlib
from socket import *

import tj

try:
    dirname = os.path.dirname(sys.argv[0])
    os.chdir(dirname)
except:
    pass

DIRECTORY = 'Send'
os.makedirs(DIRECTORY, exist_ok=True)


def help_sending():
    clear = "cls"
    if 'win32' not in sys.platform.lower(): clear = 'clear'

    help_string = '''
    
    * SENDER *
    
 -- HELP FOR SENDER --
    
This option will send files to the receiver.

 Please make sure that -
 * First the receiver is read to receive files.
 * Files will be send over LAN, so no internet will be used.
 * You and the Receiver are connect to the same network, either 
    to the same Wifi or using Ethernet.
 
 It is very easy and straight forward to send files, Just 3 steps:
     %s'''

    msg1 = '''
    (1/3) - You will be asked to enter the IP address and Port number
     of the receiver. Enter them carefully. Both, the IP and port no.
     will be shown on the Receiver's computer, enter it by seeing from 
     there!
     
     Enter to go to next step...'''

    msg2 = f'''
    (2/3) - You will now have to select which files to send. Its pretty
    easy, just copy paste the files/folder which you want to send, in the 
    Send folder which have been created just now in the same directory as
    this program (here - {dirname}).
                     ALTERNATEVLY\
    If the file/folder you want to send is very large, then instead of \
    copy pasting it, type its path when asked.\

    * Also, when the files have been send, please delete the Send\
    folder. Otherwise when you will use this program for the next time, \
    these files will also be send.\

    Enter to go to the next step...'''

    msg3 = '''
    (3/3) - Thats it, just after you have selected the files you want to send,
    hit send and those files will be send to the Receiver!
    
    Enter to start Sending the files...'''

    L = [msg1, msg2, msg3]
    for msg in L:
        os.system(clear)
        input(help_string % msg)
        os.system(clear)


class Sender:
    def __init__(self):
        self.server_host = '192.168.225.24'  # self.__get_server_host()
        self.port = 12345  # self.__get_port()
        pass
        self.buffer = 1300

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.server_host, self.port))
        self.files_to_send = None
        print(f'Connected to {gethostbyaddr(self.server_host)[0]} ({self.server_host})')

    @staticmethod
    def __validate_ip(ip):
        L = ip.split('.')
        if len(L) != 4:
            msg = 'IP address should contain exactly 4 dots (.): '
            return False, msg

        for i in L:
            msg = ''
            if not i.isdigit():
                msg = 'Enter only digits in IP address: '
                return False, msg

            if not 0 <= int(i) <= 225:
                msg = 'IP address numbers should be between 0 and 225'
                return False, msg
        return True, msg

    @staticmethod
    def __validate_port(port):
        try:
            port = int(port)
        except:
            msg = 'Port number should only contain digits, enter again: '
            return False, msg

        if not 4000 <= port <= 25000:
            msg = 'INVALID port number, enter again: '
            return False, msg
        return True, ''

    def __get_server_host(self):
        msg = 'Enter the IP address of the Receiver: '
        while True:
            ip = input(msg)
            check, msg = self.__validate_ip(ip)
            if check:
                return ip

    def __get_port(self):
        msg = 'Enter the port number of the Receiver: '
        while True:
            port = input(msg)
            check, msg = self.__validate_port(port)
            if check:
                return int(port)

    def get_files_to_send(self):
        L_send = os.listdir(DIRECTORY)
        dirname = os.path.abspath(DIRECTORY)
        if L_send:
            L = tj.get_files_in_folder(DIRECTORY)

        else:
            msg = 'Enter the full path of the file/ folder to send: '
            dirname = None
            while True:
                path = input(msg)
                if path.lower() in ['e', 'q', 'exit', 'quit']:
                    break
                if os.path.isdir(path):
                    L = tj.get_files_in_folder(path)
                    dirname = os.path.dirname(path)
                    break

                elif os.path.isfile(path):
                    L = [path]
                    dirname = os.path.dirname(path)
                    break
                else:
                    msg = 'Invalid path, Enter again (q to quit): '

        D = {}
        for i in L:
            D.update({i.replace(dirname, ''): os.path.getsize(i)})
        self.files_to_send = L

        return D

    @staticmethod
    def convert_to_percent(num, total):
        percent = num * 100 / total
        return int(percent)

    @staticmethod
    def show_progress(percent, time_elapsed=0.0, got_data=0):
        '''Display progress of percentage out of 50'''

        if percent != 100:
            try:
                speed = got_data // time_elapsed
                speed = tj.convert_bytes(speed) + r'/s'
            except:
                speed = 'N/A'
            print('  --  %-50s %s | Speed: %s' % ('#' * (percent // 2), f'{percent}%', speed), end='\r')
        else:
            print('%s' % ' ' * 85, end='\r')

        return percent

    @staticmethod
    def split_string(string, buffer):
        L = []
        i, j = 0, buffer
        s = '1'
        while s:
            s = string[i:j]
            L += [s]
            i += buffer
            j += buffer
        return L

    def send_files_metadata(self, D):

        data = json.dumps(D)  # Converted D to json data
        data_compressed = zlib.compress(data.encode())  # Compressed the data
        L = self.split_string(data_compressed, self.buffer)

        for i in L:
            self.socket.send(i)

        confirm = self.socket.recv(self.buffer)  # To confirm that metadata is received
        if confirm == b'CONFIRMED':
            print('Receiver got the metadata correctly...\n')
            return True
        else:
            print('''Receiver says that the metadata received is incorrect,
    so apparently, the Receiver doesn't know what files I am sending to him,
    this might lead to some corrupt data...\n''')
            return False

    def get_buffer(self, size_remaining):
        b = self.buffer
        if size_remaining < b:
            return size_remaining
        else:
            return b

    def send_file(self, filename, size):
        print(' -- HERE --')

        size_remaining = size
        done = 0
        f = open(filename, 'rb')

        t = time.time()
        got_data = 0
        done_percent = 0

        while size_remaining:
            var_buffer = self.get_buffer(size_remaining)
            data = f.read(var_buffer)
            self.socket.send(data)

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
            size_remaining -= var_buffer

        f.close()
        return True

    def send_files(self):
        n = len(self.files_to_send)
        for i, file in enumerate(self.files_to_send):
            size = os.path.getsize(file)
            size_fancy = tj.convert_bytes(size)
            print(f'\n Transferring file {i + 1}/{n} \n\t{file} - ({size_fancy})...')

            self.send_file(file, size)

    def close(self):
        self.socket.close()

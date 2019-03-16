import json
import os
import sys
import zlib, time
from socket import *

import tj

try:
    os.chdir(os.path.dirname(sys.argv[0]))
except:
    pass

DIRECTORY = 'Send'
os.makedirs(DIRECTORY, exist_ok=True)


class Sender:
    def __init__(self):
        self.server_host = gethostbyname(gethostname())  # '192.168.225.56'  # IP of this server
        # self.server_host = '192.168.225.24'
        self.port = 12345  # Port number
        self.buffer = 1400

        self.socket = socket(AF_INET, SOCK_STREAM)
        self.socket.connect((self.server_host, self.port))
        self.files_to_send = None
        print(f'Connected to {gethostbyaddr(self.server_host)[0]} ({self.server_host})')

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
        percent=num*100/total
        return int(percent)

    @staticmethod
    def show_progress(percent, time_elapsed=0, got_data=0):
        '''Display progress of percentage out of 50'''

        if percent!=100:
            try:
                speed=got_data//time_elapsed
                speed=tj.convert_bytes(speed)+r'/s'
            except:
                speed='N/A'
            print('  --  %-50s %s | Speed: %s' % ('#'*(percent//2), f'{percent}%', speed), end='\r')
        else:
            print('%s' % ' '*85, end='\r')

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

        size_remaining = size
        done=0
        f = open(filename, 'rb')

        t=time.time()
        got_data=0
        done_percent=0

        while size_remaining:
            #time.sleep(0.005)
            var_buffer = self.get_buffer(size_remaining)
            data = f.read(var_buffer)
            #print(f'NEED TO SEND: {var_buffer} , SENT: {len(data)}')
            self.socket.send(data)

            l=len(data)
            done+=l
            got_data+=l
            percent=self.convert_to_percent(done, size)

            if percent != done_percent:
                time_elapsed = time.time()-t
                self.show_progress(percent, time_elapsed, got_data)

                done_percent = percent
                got_data=0
                t=time.time()

            '''received = self.socket.recv(4)

            while received == b'CORR':
                # This means Receiver got a corrupt package
                # Now I have to send this package again
                print(f' At {done}/{size}, Receiver got corrupt package, sending again...')
                self.socket.send(data)
                # Package is send again
                received = self.socket.recv(4)
                # Lets see if the receiver got this package correctly'''

            size_remaining -= var_buffer

        f.close()
        return True

    def send_files(self):
        n = len(self.files_to_send)
        for i, file in enumerate(self.files_to_send):
            size = os.path.getsize(file)
            size_fancy = tj.convert_bytes(size)
            print(f'\n Transferring file {i + 1}/{n} \n\t{file} - ({size})...')
            result = self.send_file(file, size)
            if result:
                print(' File transferred successfully!')
            else:
                print(' --- FILE TRANSFER FAILED ---')

            # time.sleep(0.03)

    def close(self):
        self.socket.close()


S = Sender()
D = S.get_files_to_send()
S.send_files_metadata(D)
S.send_files()
S.close()

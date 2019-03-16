import json
import os
import sys
import time
import zlib
from random import randint
from socket import *

import tj

__version__='1.0'

dirname = os.path.dirname(sys.argv[0])
if dirname != '': os.chdir(dirname)

DIRECTORY = 'Received'
os.makedirs(DIRECTORY, exist_ok=True)

c = tj.color_text  # Making c as tj.color_text
last_speed='0 MB/s'

clear = "cls"
if 'win32' not in sys.platform.lower():
    clear = 'clear'
    clr='OLIVE'
    is_bold=True
else:
    clr='BLACK'
    is_bold=False

def help_receiving():
    

    help_string = f'''
        {c("                  ", background_color='WHITE')}
        {c("   * RECEIVER *   ", text_color=clr, background_color='WHITE', bold=True)}
        {c("                  ", background_color='WHITE')}
 -- HELP FOR RECEIVER --

This option will receive files from the sender.

 Please make sure that -
 {c(f"""

 * Files will be received over LAN, so no internet will be used.
 * You and the Sender are connect to the same network, either 
    to the same Wifi or using Ethernet.
 * You have to tell your IP address and Port number to the Sender,
    by yourself.
 * All files received will be saved in the Received folder which have
    been created in the same director as this program.
    (here - {dirname})""", text_color='YELLOW', bold=True)}

 It is very easy and straight forward to receive files, Just 3 steps:
     %s'''

    msg1 = '''
    (1/3) - The program will show you your IP address and the 
    Port number. Tell both these things to the Sender, who will 
    enter both of these in his computer.

    Enter to go to next step...'''

    msg2 = f'''
    (2/3) - When the Sender has been connected, files will start 
    Receiving automatically, without any interference from you.
    They will be saved in the Received folder as stated above.

    Enter to go to the next step...'''

    msg3 = '''
    (3/3) - Thats it, all files/folders will be received and saved.

    Enter to start Receiving the files...'''

    L = [msg1, msg2, msg3]
    for msg in L:
        os.system(clear)
        input(help_string % msg)
        os.system(clear)



class Receiver:
    def __init__(self):
        self.host = self.__get_host()  # To get the ip address of the Receiver (server)
        self.port = 12345#self.__get_port()  # To get a random port number
        self.buffer = 1300  # Buffer is set to 1300 to save file from corruption

        self.socket = socket(AF_INET, SOCK_STREAM)  # Made TCP socket
        self.socket.bind((self.host, self.port))  # Binded the socket
        self.socket.listen(1)  # Only 1 user will connect

        print('\n Receiver is READY TO RECEIVE FILES')
        print('     Waiting for the Sender to join...')
        self.partner, self.partner_addr = self.socket.accept()  # Waiting for client to accept
        print(f'''{gethostbyaddr(self.partner_addr[0])[0]} ({self.partner_addr[0]}) is now connected''')
        self.partner.settimeout(0.05)

    @staticmethod
    def __get_host():
        '''Function to get the IP address of the Receiver'''
        host = gethostname()
        ip = gethostbyname(host)
        print('The IP Address of Receiver is: %s' % c(ip, text_color=clr, background_color='WHITE', bold=is_bold))
        return ip

    @staticmethod
    def __get_port():
        '''Gives a random number for port'''
        port = randint(4000, 25000)
        print('\nThe port number of Receiver is: %s' % c(str(port), text_color=clr, background_color='WHITE', bold=is_bold))
        return port

    @staticmethod
    def convert_to_percent(num, total):
        '''Converts to percentage'''
        percent = num * 100 / total
        return int(percent)

    @staticmethod
    def show_progress(percent, time_elapsed=0, got_data=0):
        '''Display progress of percentage out of 50'''
        global last_speed

        if percent != 100:
            try:
                speed = got_data // time_elapsed  # Gets the speed in the "Fancy" format
                speed = tj.convert_bytes(speed) + r'/s'  # Adds /s to speed
                last_speed=speed
            except:
                speed = last_speed
            text=' '*((percent+1)//2)
            colored=c(text, text_color='WHITE', background_color='WHITE')
            print('      %-64s %s | Speed: %s' % (colored, f'{percent}%', speed), end='\r')
        else:
            pass
            print('%s' % ' ' * 95, end='\r')
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
        if done == size:
            return True
        else:
            return False

    def get_files(self, D):
        n = len(D)
        self.partner.settimeout(None)
        failed = []
        for i, file in enumerate(list(D.keys())):

            size = D[file]
            size_fancy = tj.convert_bytes(size)
            print(f'\n Receiving file {i + 1}/{n}\n\t{file} - ({size_fancy})')
            tt=time.time()
            result = self.get_file(file, size)
            print(f'\tTime Taken to receive: {tj.convert_time(round(time.time()-tt,1))}')

            if not result:
                failed += [[file, size_fancy]]

        if failed:
            print('\n THERE WAS SOME ERROR IN RECEIVING THESE FILES - ')
            for i in failed:
                print(f' {i[0]} , Size: {i[1]}')

    def close(self):
        self.partner.close()
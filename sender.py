import os, tj, zlib, sys, json, time
from socket import *

os.chdir(os.path.dirname(sys.argv[0]))

DIRECTORY='Send'

os.makedirs(DIRECTORY, exist_ok=1)

class Sender:
    global DIRECTORY

    def __init__(self, files=None):
        print('  ** SENDER **')
        print('This module will send files to the receiver...\n')
        self.host=self.__get_host()
        self.port=self.__get_port()
        self.files=self.get_files(files)    # A dictionary with names of all the files : file_size
        self.addr=(self.host, self.port)
        self.buff=8*1000    # Buffer, it should be 2*1024, but I found that 2*1000 in sender.py give less corrupt files
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.wait_buffer=0.3

    @staticmethod
    def __validate_ip(address):
        try:
            host_bytes = address.split('.')
            valid = [int(b) for b in host_bytes]
            valid = [b for b in valid if b >= 0 and b<=255]
            return len(host_bytes) == 4 and len(valid) == 4
        except:
            return False

    def __get_host(self):
        msg='Enter the IP Address of the receiver: '
        while True:
            host=input(msg)
            if host.upper() in ['Q','QUIT','E','EXIT']:
                input('\n -- PRESS ENTER TO QUIT --')
                sys.exit()

            if not self.__validate_ip(host):
                msg=f'{host} is not a correct IP Address, enter again carefully (enter Q to quit): '
                continue
            break
        print(f'{host} seems to be a valid IP Address, connecting to it...\n')
        return host

    @staticmethod
    def __get_port():
        msg='Enter the port number: '
        while True:
            port=input(msg)
            if port.upper() in ['Q','QUIT','E','EXIT']:
                input('\n -- PRESS ENTER TO QUIT --')
                sys.exit()

            if not port.isdigit():
                msg=='Enter only numbers (enter Q to quit): '
                continue

            port=int(port)
            if not 3000<port<30000:
                msg='Port number is invalid, enter correct port number (enter Q to quit): '
                continue
            break

        print(f'{port} seems to be a valid port number, connecting to it...\n')
        return port


    def get_files(self, files):
        if files!=None:
            return {files:os.path.getsize(file)}

        L=tj.get_files_in_folder(DIRECTORY)
        D={}
        for i in L:
            file=i
            size=os.path.getsize(file)
            file=file.strip(os.path.dirname(DIRECTORY))
            D.update({file:size})
        return D

    def send_info(self):
        '''Sends the files metadata to the receiver'''

        D={}
        for file in self.files:
            x=file
            dirname=os.path.dirname(sys.argv[0])
            to_remove=os.path.join(dirname,DIRECTORY)
            #print('\n',to_strip,x)
            x=x.replace(to_remove,'')
            temp={x:self.files[file]}
            #print(temp,'\n')
            D.update(temp)


        data=json.dumps(D)
        data=data.encode()
        data=zlib.compress(data)
        print('Starting transfer -')

        time.sleep(self.wait_buffer)
        self.socket.sendto(data, self.addr)
        print('Metadata sent...')
        time.sleep(self.wait_buffer)

        if len(data)>512:time.sleep(self.wait_buffer*3)  # To make sure that the receiver had processed the metadata

        if len(data)>1024:time.sleep(self.wait_buffer*6)


    def __send_file(self, file):
        '''A helper function for send_files'''
        f=open(file,'rb')
        t=time.time()
        while True:
            data=f.read(self.buff)  # data here will be binary, already
            self.socket.sendto(data, self.addr)
            if data==b'':
                break
        f.close()

        tt=(time.time()-t)
        size=self.files[file]

        try:
            speed=tj.convert_bytes(size//tt)
            tt=round(tt,3)
            s=f'took {tt}s, avg. speed - {speed}/s'
        except:
            s="file was small, didn't do measurements! "
        
        print(f' | Transferred, {s}', end='\n\n')

        time.sleep(self.wait_buffer) # Wait between each new file call

    def send_files(self):
        for file in self.files:
            print(f'Transferring file: {file}',end='')
            self.__send_file(file)


    def close(self):
        print('Transfer complere, Closing the connection!')
        self.socket.close()
        input('Enter to quit...')


S=Sender()
S.send_info()
S.send_files()
S.close()




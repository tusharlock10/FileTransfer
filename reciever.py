import os, random, zlib, json, tj, sys, time
from socket import *

os.chdir(os.path.dirname(sys.argv[0]))

DIRECTORY='Received'

os.makedirs(DIRECTORY, exist_ok=1)


class Receiver:
    global DIRECTORY

    def __init__(self):
        print('  ** RECEVIER **')
        print('This module will Receive files ...\n')

        self.host=self.__get_host()
        self.port=self.__get_port()
        print('\nEnter both of these correctly in the sender...')
        self.addr=(self.host, self.port)
        self.buff=8*1024    # Its buffer is a little more than sender, to avoid the files getting corrupt
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket.bind(self.addr)
        self.files=self.get_info()
        self.wait_buffer=0.3

    @staticmethod
    def __get_host():
        host=gethostname()
        ip=gethostbyname(host)
        print(f'The IP Address of Receiver is: {ip}')
        return ip

    @staticmethod
    def __get_port():
        port=random.choice(list(range(3000,30001)))
        print(f'The port number is: {port}')
        return port

    def get_info(self):
        '''Gets the files metadata from sender'''
        data, addr = self.socket.recvfrom(self.buff)   # Here files is in cmp, bin, json
        print('Got the metadata...')
        data = zlib.decompress(data)   # bin, json
        #print(data)
        data=data.decode()  # json left
        files=json.loads(data)  # files dictionary {file_1 : size_1,   file_2 : size_2 ...}

        return files

    def __get_file(self, file):
        dirname=os.path.dirname(file)
        os.makedirs(dirname, exist_ok=1)

        tt=time.time()
        f=open(file,'wb')
        while 1:
            data, addr = self.socket.recvfrom(self.buff)
            f.write(data)
            if data==b'':
                break
        f.close()

        tt=(time.time()-tt)
        size=self.files[file]

        try:
            speed=tj.convert_bytes(size//tt)
            tt=round(tt,3)
            s=f'took {tt}s, avg. speed - {speed}/s'
        except:
            s="file was small, didn't do measurements! "

        if os.path.getsize(file)==self.files[file]:
            error='  THE RECIEVED FILE WAS CORRUPT, RETRY FOR THIS FILE...'
            error= tj.color_text(error, text_color='RED')
        else:
            error='  File is successfully recieved...'
            error= tj.color_text(error, text_color='GREEN')

        print(f' | Received, {s}', end='\n')
        print(f'{error}')


    def get_files(self):
        for file in self.files:
            print(f'Receiveing file: {file}',end='')
            self.__get_file(file)

    def close(self):
        print('Files recieved, Closing the connection!')
        self.socket.close()



R=Receiver()
R.get_files()
R.close()



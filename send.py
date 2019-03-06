# File Sender

import os, sys,time,tj, json
from socket import *



os.chdir(os.path.dirname(sys.argv[0]))

buf=1000
tar='Transfer'

def get_files():
    global tar
    D={}
    L=os.listdir(tar)
    for i in L:
        temp={i:os.path.getsize(os.path.join(tar,i))}
        D.update(temp)
    return D

host=''
while True:
    host = input('Enter IP Address of the reciever :')#gethostbyname(gethostname()) # set to IP address of target computer
    if host in ['Q', 'q', 'QUIT','quit','exit','e']:break
    port = 13000
    addr = (host, port)
    try:
        inet_aton(host)
        break
    except:print('The IP Address entered by you isnt correct...\nTry again\n\n')
t=time.time()
UDPSock = socket(AF_INET, SOCK_DGRAM)


## SEND FILE INFORMATION ##
files=get_files()
files_data=json.dumps(files).encode()



UDPSock.sendto(files_data, addr)
total_size=sum([files[x] for x in files])



for x in files:
    FILE=os.path.join(tar, x)

    print('TRANSFERRING FILE:',FILE)
    time.sleep(0.35)
    f=open(FILE, 'rb')

    while True:
        data=f.read(buf)

        UDPSock.sendto(data, addr)
        if data==b'':break
    f.close()

UDPSock.close()
tt=time.time()-t
speed=total_size//round(tt-(0.35*len(files)),2)
speed=tj.convert_bytes(speed)
input(f'Total time taken: {tt} sec, average transfer speed was: {speed}/s')
os._exit(0)

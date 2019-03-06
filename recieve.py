# File Receiver
import os,sys, json
from socket import *


os.chdir(os.path.dirname(sys.argv[0]))

tar='Recieved'

host = gethostname()

print('Your IP address is :',gethostbyname(host))
print("Enter this IP address correctly in the sender's system")

port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)

files_data, addr = UDPSock.recvfrom(buf)
files_data=files_data.decode()
files=json.loads(files_data)
print(files)
not_trans=[]

for x in files:
    FILE=os.path.join(tar, x)

    print('\nIN THE FILE:',FILE)
    f=open(FILE, 'wb')
    while True:
        (data, addr) = UDPSock.recvfrom(buf)
        f.write(data)
        if data==b'':
            break
    f.close()
    size=files[x]
    if size!=os.path.getsize(FILE):
        print(f'{FILE} is not transferred properly, please redo tranfer for this file...')
        not_trans+=[FILE]
    else:
        print(f'{FILE} is transferred successfuly...')


UDPSock.close()
input('\n\n\n------------- TRANSFER COMPLETE -----------------')
if not_trans:
    input('These files are not transferred correctly->')
    for i in not_trans:print(i)
else:
    print('All files transferred correctly...')
input()
os._exit(0)
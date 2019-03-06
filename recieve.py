# File Receiver
import json
import os
import sys
from socket import *

os.chdir(os.path.dirname(sys.argv[0]))

tar = 'Recieved'

host = gethostname()

print('Your IP address is :', gethostbyname(host))
print("Enter this IP address correctly in the sender's system")

port = 13000
buf = 1024
addr = (host, port)
UDPSock = socket(AF_INET, SOCK_DGRAM)
UDPSock.bind(addr)

files_data, addr = UDPSock.recvfrom(buf)
files_data = files_data.decode()
files = json.loads(files_data)
print(files)
not_trans = []

for x in files:
    FILE = os.path.join(tar, x)

    print('\nIN THE FILE:', FILE)
    f = open(FILE, 'wb')
    while True:
        (data, addr) = UDPSock.recvfrom(buf)
        f.write(data)
        if data == b'':
            break
    f.close()
    size = files[x]
    if size != os.path.getsize(FILE):
        print('%s is not transferred properly, please redo tranfer for this file...' % FILE)
        not_trans += [FILE]
    else:
        print('%s is transferred successfuly...' % FILE)

UDPSock.close()
input('\n\n\n------------- TRANSFER COMPLETE -----------------')
if not_trans:
    input('These files are not transferred correctly->')
    for i in not_trans: print(i)
else:
    print('All files transferred correctly...')
input()
os._exit(0)

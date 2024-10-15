# Echo client program
import socket

HOST = '127.0.0.1'    # The remote host
PORT = 50007              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    i=0
    while i<10:
        try:
            s.connect((HOST, PORT))
            s.sendall(b'150;210')
            data = s.recv(1024)
            break
        except:
            i+=1
print('Received', data.decode(encoding="utf8"))
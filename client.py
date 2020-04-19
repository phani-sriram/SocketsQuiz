import socket
import sys
import select

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

PORT = 1234
IP = "127.0.0.1"

c.connect((IP, PORT))

while True:

    list_of_inputs = [sys.stdin, c]
    read_sockets, write_socket, error_socket = select.select(list_of_inputs,[],[])

    for socks in read_sockets:
        if(socks == c):
            msg = c.recv(2048)
            print(msg)
        else:
            msg = sys.stdin.readline()
            c.send(msg)
            sys.stdout.flush()

c.close()
sys.exit()

import socket
from threading import Thread
import time
import sys

IP = "127.0.0.1"
PORT = 1234
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP,PORT))

def send():
    msg = input()
    client.send(msg.encode("utf-8"))
    if msg == "exit":
        client.close()
        exit()
    send()


def recv():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            print(message)
        except OSError:
            break    
          
Thread(target = recv).start()
Thread(target = send).start()


    




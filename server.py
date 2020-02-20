import socket
from threading import Thread

def messages(x,y):
    name = x.recv(1024).decode("utf-8")
    Hello = "Hello {0}. Send private messages with /pm [person] [message]".format(name)
    x.send(bytes(Hello,"utf-8"))
    clientAddress[x] = name
    while True:
        msg = x.recv(1024)   
        if bytes("/pm","utf-8") in msg:                     #private messages        
            ukko = msg.decode("utf-8").split()[1]
            viesti = msg[5+len(ukko):]
            for i in clientAddress:
                if clientAddress[i] == ukko:
                    i.send(bytes(name+"(pm): ","utf-8")+viesti)
                    print(name+" send private message to "+ukko)
                               
        elif msg != bytes("exit", "utf8"):                  #messages
            for i in clientAddress:
                if i != x:                    
                    i.send(bytes(name+": ","utf-8")+msg)
                    print(name+" send message to all")
       
        else:                                               #exiting chat room
            x.close()
            del clientAddress[x]
            for i in clientAddress:
                i.send(bytes("{0} has left the chat room.".format(name),"utf8"))
            
            print("{0} has logged out.".format(y))
            break

def start():
    while True:
        servu, address = server.accept()
        print("{0} Connected".format(address))
        servu.send(bytes("Your Username:","utf-8"))
        Thread(target=messages, args=(servu,address)).start()

IP = "127.0.0.1"
PORT = 1234

clientAddress = {}
clientName = {}


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PORT))
server.listen(5)
a = Thread(target=start)
a.start()


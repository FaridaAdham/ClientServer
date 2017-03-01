# serverfinal.py

import socket
from threading import Thread
from SocketServer import ThreadingMixIn

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

class ClientThread_GET(Thread):

    def __init__(self,ip,port,sock,filename):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock 
        self.filename = filename
        print "\n  New Thread Started For "+ip+":"+str(port)

    def run(self):
        #filename='mytext.txt'
        #print filename
        #print 'hbygbygbybybygb'
        try:
            f = open(self.filename,'rb')
            while True:
                reply = 'exist'
                self.sock.send(reply)
                #read the received file from the client.
                l = f.read(BUFFER_SIZE)
                while (l):
                    #send the read data using the socket.
                    self.sock.send(l)
                    #print('Sent ',repr(l))
                    l = f.read(BUFFER_SIZE)
                if not l:
                    f.close()
                    self.sock.close()
                    break
        except IOError as e:
            error = 'notexist'
            self.sock.send(error)
            self.sock.close()

class ClientThread_POST(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock 
        print "\n  New Thread Started For "+ip+":"+str(port)

    def run(self):
        #filename='mytext.txt'
        #print filename
        #print 'hbygbygbybybygb'
        with open('received_file_from_client', 'wb') as f:
            print '  File Opened '
            while True:
                #print('receiving data...')
                data = self.sock.recv(BUFFER_SIZE)
                if not data:
                    f.close()
                    print '  File Closed'
                    break
                # write data to a file
                print '  Data :', (data)
                f.write(data)
        f.close()
        self.sock.close()

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    print "\n  ***Waiting For Incoming Connections ...."
    #listening for any connections coming from the client with 
    #IP address = 'localhost' and Portnum = 9001.
    tcpsock.listen(5)
    #when recieving connection from the client ,It accepts it.
    (conn, (ip,port)) = tcpsock.accept()
    print '\n  ***Got Connection From ', (ip,port)
    #recieving the request from the client
    data = conn.recv(BUFFER_SIZE)
    #split function is used to divide the incoming data into seperate
    #values . 
    data = data.split()
    spaces = '\n   ***Client Request : '
    #printing out the Request.
    #lw el data feeha 4 kalemat .
    if len(data) == 4:
        req = data[0]
        filename = data[1]
        hostname = data[2]
        portnumber = data[3]
        print spaces,req,filename,hostname,portnumber

    #lw el data feeha 3 kalemat .
    elif len(data) == 3:
        req = data[0]
        filename = data[1]
        hostname = data[2]
        print spaces,req,filename,hostname

    #checking whether the request method is get or post.
    if req == 'GET' or req == 'get':
        #opens a thread for the get method as It gets the file of this 
        #filename.
        newthread = ClientThread_GET(ip,port,conn,filename)
        newthread.start()
        threads.append(newthread)
    elif req == 'POST' or req == 'post':
        #opens a thread for the post method as It receives the file 
        #from the client.   
        newthread = ClientThread_POST(ip,port,conn)
        newthread.start()
        threads.append(newthread)
for t in threads:
    t.join()

input()
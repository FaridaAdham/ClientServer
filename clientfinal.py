# clientfinal.py

import socket

TCP_IP = 'localhost'
TCP_PORT = 9001
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((TCP_IP, TCP_PORT))
flag = True
print '  ****The Commands Syntax should be as follows :'
print '             GET file-name host-name (port-number)'
print '             POST file-name host-name (port-number)'
while flag == True:
    #accepting requests from the client.
    request = raw_input("  Request :  ")
    request_array = request.split()
    req = request_array[0]
    if  len(request_array) == 4 or len(request_array) == 3:
        #checks if the request method is only post or get nothing else.
        if req == 'GET' or req == 'get' or req == 'POST' or req == 'post':        
            if req == 'GET' or req == 'get':
                #sends the request to server
                s.send(request)
                #accepts the reply from the server
                reply = s.recv(100)
                reply = reply.split()
                reply = reply[0]
                if reply == 'exist':
                    #if the file is found and sent to the client 
                    print '\n  HTTP/1.0 200 OK\r\n'
                    with open('received_file_from_server', 'wb') as f:
                        print '\n  File Opened'
                        reply = 'HTTP/1.0 200 OK \r \n'
                        f.write(reply)
                        while True:
                            #print('receiving data...')
                            data = s.recv(BUFFER_SIZE)
                            if not data:
                                f.close()
                                print '\n  File Closed'
                                break
                            # write data to a file
                            print '\n  Data :', (data) 
                            f.write(data)
                    f.close()     
                    print '\n  Successfully Get The File From The Server.\n'
                elif reply == 'notexist':
                    print '\n  HTTP/1.0 404 Not Found \r \n' 
                flag = False
            elif req == 'POST' or req == 'post':
                s.send(request)
                filename = request_array[1]
                f = open(filename,'rb')
                while True:
                    l = f.read(BUFFER_SIZE)
                    while (l):
                        s.send(l)
                        #print('Sent ',repr(l))
                        l = f.read(BUFFER_SIZE)
                    if not l:
                        f.close()
                        s.close()
                        break
                f.close()    
                print'\n  Successfully Post The File To The Server.\n'
                flag = False
            elif len(request_array) == 4 or len(request_array) == 3:
                #if the number of needed parameters in the entered
                #request isn't correct.
                print '\n  ***Invalid Request Method !!***\n' 
        else:
            #if the Requuest Method isn't get or post
            print '\n  ***Invalid Request Method !!***\n'   
    else:
        print '\n  ***Invalid Request Method !!***\n'
s.close()
print '  Connection Closed'
input()
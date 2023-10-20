
import socket
import sys
import time
from datetime import datetime
from _thread import*

count =0
ThreadCount = 0 

#Creating Socket
try:
    socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #parameters(socketFamily, tcp=SOCK_STREAM and etc)
    print("socket connected")

except socket.error as err:
    print("Failed to create a socket")
    print("Reason" + str(err))
    sys.exit()

#Socket check with port 
try:
    target_host = socket.gethostname()
    traget_port = 1234
    socket_server.bind((target_host, traget_port))
    print("Socket connect to %s on port %s"%(target_host,traget_port))
    

except socket.error as err:
    print("Failed to connect to %s on port %d"%(target_host,traget_port))
    print("Reason: %s" %str(err))
    sys.exit()

socket_server.listen(5) 


def client_thread(connection):
    count =0

    while True:
        # get current datetime
        today = datetime.now()
        # Get current ISO 8601 datetime in string format (YYYY-MM-DDTHH:MM:SS.mmmmmm)
        iso_date = today.isoformat()
        today = datetime.now()
        iso_date = today.isoformat()
        connection.send(str.encode("ISO DateTime: "+ iso_date))
        count = count+1
        if count == 10:
            print("Socket secession is ended")
            connection.close()
        time.sleep(5)


          


while True:
    client,address=socket_server.accept()
    print("Connected to "+address[0]+str(address[1]))
    start_new_thread(client_thread,(client,))
    ThreadCount+=1
    print("ThreadNumber"+str(ThreadCount))

socket_server.close()




















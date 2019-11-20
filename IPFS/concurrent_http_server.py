import socket, sys,requests
import os
import random
import time
from datetime import datetime

import ipfscluster
import ipfshttpclient

from _thread import *
import threading 

print_lock = threading.Lock() 


def threaded(conn, client, addr):
    # Creates a unique text file - necessary for concurrent writes
    file_name = str(addr[0]) + str(datetime.now().time()) + ".txt"
    print(file_name)
    f = open(file_name, 'a+')

    message_sent = False

    # Creates a random number and send to client - to indicate end of file
    connection_secret = str(random.random())
    conn.sendall(str.encode(connection_secret))

    while True:

        data = conn.recv(1024) 
        
        # When client closes the connection before end of file received
        if not data:
            # TO DO change this 
            hash = ipfs_add(client, file_name) 
            conn.sendall(str.encode(hash))
            print('Bye') 
 
            break
        else:

            input = data.decode("utf-8")
            print(input)

            # Look for end of file
            finish = "This is the end of the file: " + connection_secret
            end = input.find(finish)
            if(end != -1):
                message_sent = True

                print("\n End of File Found \n\n")
                
                input = input[:end]
            f.write(input)

        if message_sent:
            f.close()
            
            # Add the file to IPFS Cluster
            hash = ipfs_add(client, file_name) 

            # Returns the hash to the client
            conn.sendall(str.encode(hash + "\n"))
            print('Bye') 
        
            break  
    conn.close()


def ipfs_add(client, file_name):
    print(file_name)
    hash = client.add_files(file_name)['cid']['/']

    # Delete the file after adding to IPFS
    if os.path.exists(file_name):
        os.remove(file_name)
    else:
        print("The file does not exist")
    print("Hash: " + str(hash))
    return hash

def ipfs_get(mainclient, hash):
    mainclient.cat()
  
  
def Main(): 
    
    # Creates connection to IPFS Cluster
    client = ipfscluster.connect(session=True)
    # mainclient = ipfshttpclient.connect()

    host = ''
    port = 7147

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to host IP and port
    try:
        s.bind((host,int(port)))
        print('listening on', (host, port))
    except socket.error as e:
        print(str(e))
        
    
    s.listen(5)  
    print("Waiting for connection...")

    # Constantly look for connections on host IP and port
    while True:
        conn, addr = s.accept()
        print('Connected by', addr)

        # Create a new thread to handle the connection
        start_new_thread(threaded, (conn, client, addr))
            
    s.close()

  
  
if __name__ == '__main__': 
    Main() 


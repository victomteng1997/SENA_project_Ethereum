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


def threaded(conn, mainclient, addr):
    inputs = conn.recv(1024)
    inputs = inputs.decode('utf-8')
    split_inputs = inputs.split(" ")
    print(split_inputs)

    end_of_file = "This is the end of the file: " + split_inputs[0]

    data = ipfs_get(mainclient, split_inputs[1])  kllm,9-'pj9p l'
    conn.sendall(data)
    conn.sendall(str.encode(end_of_file))  
    conn.close()


def ipfs_get(mainclient, hash):
    result = mainclient.cat(hash)
    return result
  
  
def Main(): 
    
    # Creates connection to IPFS Cluster
    # client = ipfscluster.connect(session=True)
    mainclient = ipfshttpclient.connect()

    host = ''
    port = 7417

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
        start_new_thread(threaded, (conn, mainclient, addr))
            
    s.close()

  
  
if __name__ == '__main__': 
    Main() 


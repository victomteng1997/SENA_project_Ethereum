import socket, sys,requests
import os
import random

import ipfscluster
import ipfshttpclient

from _thread import *
import threading 

print_lock = threading.Lock() 

# thread fuction 
def threaded(conn, client):

    message_sent = False

    # Send client a secret to be used to indicate end of file
    connection_secret = str(random.random())
    conn.sendall(str.encode(connection_secret))
    while True:
        # create file that will be inserted into IPFS
        f = open('socket_file.txt', 'a+')

        # Take in data from client 
        data = conn.recv(1024) 
        print(data)

        # If connection closed by client add file to IPFS -- CHANGE to handle as ARTC want -- potentially delete file and connection
        if not data:
            h = ipfs_add(client) 
            conn.sendall(str.encode(h))
            print('Bye') 
              
            # lock released on exit 
            print_lock.release() 
            break
        else:
            # Server has recieved data
            # Convert Data from Bytes to String
            input = data.decode("utf-8")

            # Check recieved data to see if the end of file has been sent.
            finish = "This is the end of the file: " + connection_secret
            end = input.find(finish)
            if(end != -1):
                message_sent = True
                print("\n\n\n")

                # Remove the end of file indicator from the data being added to the file
                data = print(input[:end])
                input = input[:end]

            # Add recieved data to the file
            f.write(input)
        
        # If end of message from client add the file to IPFS and close connection
        if message_sent:
            h = ipfs_add(client) 
            
            #Send the client the Hash of their file in IPFS
            conn.sendall(str.encode(h + "\n"))
            print('Bye') 
        
            # lock released on exit 
            print_lock.release() 
            break  
    # connection closed 
    conn.close()


# Add file to IPFS cluster and return the hash
def ipfs_add(client):
    h = client.add_files('socket_file.txt')['cid']['/']

    if os.path.exists("socket_file.txt"):
        os.remove("socket_file.txt")
    else:
        print("The file does not exist")
    print("Hash: " + str(h))
    return h
  
 
  
  
def Main(): 
    # client - For IPFS Cluster
    # mainclient - For IPFS only
     
    client = ipfscluster.connect(session=True)
    # mainclient = ipfshttpclient.connect()

    # Set the IP and Port for the Server
    host = '10.217.135.233'
    port = 7147
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        s.bind((host,int(port)))
        print('listening on', (host, port))
    except socket.error as e:
        print(str(e))
        
    
    s.listen(5)  # Basically a que, number of incoming connections at a time
    print("Waiting for connection...")
    while True:
        conn, addr = s.accept()
        print('Connected by', addr)

        print_lock.acquire()
        start_new_thread(threaded, (conn, client))
            
    s.close()

  
  
if __name__ == '__main__': 
    Main()
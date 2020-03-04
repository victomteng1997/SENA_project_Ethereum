import socket
import sys
import random
from config import *

def main(hash):
    '''
    Download file from IPFS system
    :return: None
    '''
    output = ''
    #Open the file containing the data to be sent to IPFS
    #hash = sys.argv[1]

    # Set the IP and Port for the Server
    host = IPFS_host
    port = IPFS_file_port

    # Connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        connection_secret = str(random.random())

        hash_entry = connection_secret + " " + hash
        s.sendall(str.encode(hash_entry))

        while True:

            message_sent = False
            data = s.recv(2048) 
            
            # When client closes the connection before end of file received
            if not data:
    
                break
            else:

                input = data.decode("utf-8")
                # print(input)

                # Look for end of file
                finish = "This is the end of the file: " + connection_secret
                end = input.find(finish)
                if(end != -1):
                    message_sent = True

                    # print("\n End of File Found \n\n")
                    
                    input = input[:end]
                print("input", input)
                output += input
            if message_sent:
                print('Bye') 
            
                break  
        s.close()
        print("Done")
        return output
    


if __name__ == "__main__":
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv[1]))
    main(str(sys.argv[1]))

import socket
import sys

def main():

    #Open the file containing the data to be sent to IPFS
    file_name = sys.argv[1]
    f = open(file_name, 'r')

    # Set the IP and Port for the Server
    host = "10.217.135.233"
    port = 7147

    # Connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        #Server sends a random number to client this is used to indicate the end of the file that is being sent to the server.
        random_secret = s.recv(1024)
        random_secret = random_secret.decode('utf-8')
        print(random_secret)

        # Send all the data to the server.
        for file_line in f:
            s.sendall(str.encode(file_line))

        # Send back the random number to indicate finish
        finish = "This is the end of the file: " + random_secret
        s.sendall(str.encode(finish))

        # Recieve the Hash from the Server this will be used to access the file in IPFS
        data = s.recv(1024)
        print("Hash: " + data.decode('utf-8'))
    


if __name__ == "__main__":
    print('Number of arguments:', len(sys.argv), 'arguments.')
    print('Argument List:', str(sys.argv[1]))
    main()
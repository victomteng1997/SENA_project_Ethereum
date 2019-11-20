# IPFS HTTP Implementation

## Introduction

This is currently discribed as our final attempt in Implementing IPFS as a file storage Method for ARTC.
We have 2 parts to this implementation a IPFS Cluster Server and IPFS Cluster Client.

### IPFS Cluster Server
The Script begins by connecting to the IPFS Cluster but it can be set to only connect to IPFS and not the Cluster by uncommenting the line 

> \# mainclient = ipfshttpclient.connect()

and commenting the line 
> client = ipfscluster.connect(session=True)

you will also have to replace client in the line below with mainclient

> start_new_thread(threaded, (conn, client))

The IP address and Port for the Server is currently set to:
**IP:** 10.217.135.233
**Port:** 7147

These can both be changed to whatever match your configuration.

The Server can handle multiple connections however I have implemented a lock which essentially only allows one Client to use the Server at a time this is due to the fact that each Client would be writing to one file called: 
> socket_file.txt

**TO DO** However if we changed the file name to say the IP and time of connection then you may get rid of the lock as each connection would write to a different file and the writes could all happen concurrently. 

When a Client connects the Server sends the client a random number. Upon recieving the random number the client will begin to send the Influx Data which is to be stored in IPFS. When the Client has sent all the Data it will send:

> "This is the end of the file: " + random_number

Once the Server recieves this the Server will add all the data it has recieved to IPFS and then send back it's Hash to the Client, release the lock on the file and close the connection with the Client.


### IPFS Cluster Client
The client requires that you add the name of the file that is to be added to IPFS as a Command Line arguement. For example:

> http_client.py input.txt

The client will then attempt to connect to the host on the specified IP address and Port. In this case we have used:

**IP:** 10.217.135.233
**Port:** 7147

Once connected the client waits to recieve a random number from the Server, this is used to indicate the end of the message. After recieving the number the Client will append.

>"This is the end of the file: " + random_number

To the end of the file and sends the contents to the server to be added to IPFS. The Client then waits for the Server to send the Hash back before the connection is closed.


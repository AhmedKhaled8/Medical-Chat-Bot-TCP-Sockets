import socket
import threading
import errno
import sys

# * DEFINING STANDARDS OF THE TCP STREAM CLIENT SOCKET CONNECTION
HEADER = 64 # * Define a constant size of the header
PORT = 5050 # * Define a port for the socket that client access
FORMAT = 'utf-8' # * A decoding/encoding format of the messages
DISCONNECT_MESSAGE = '!DISCONNECT' # * A defined disconnect message
SERVER = socket.gethostbyname(socket.gethostname()) # * Define the IPv4 address the client will connect to. 
ADDRESS = (SERVER, PORT) # * The address to which the client will connect
idle_status = False


 
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # * defining a socket object for the client
client.connect(ADDRESS) # * connecting the client socket to the server socket

def recieve_status_message():
    connected = True
    while connected:
        status_length = int(client.recv(HEADER).decode(FORMAT)) # * recieve the length of the status message sent from the server
        status = client.recv(status_length).decode(FORMAT) # * recieve the status message itself from the server
        print(status)
        if status == DISCONNECT_MESSAGE:
            global idle_status
            idle_status = True
            connected = False
            print("[IDLE] Connection was closed please open the UI again")
            sys.exit()

        



def send(msg):
    """send: a function that sends a message "msg" to the server.

    Args:
        msg (str): The message to be sent
    """
    if not idle_status:
        message = msg.encode(FORMAT) # * encode the message
        msg_length = f"{len(message):<{HEADER}}".encode(FORMAT) # * create the header of the message
        client.send(msg_length) # * send the header first
        client.send(message) # * send the message
    else:
        print("[IDLE] Connection was closed please open the UI again")
        
        
    # client.settimeout(5.0)
    # status_lenght = ""
    # try:
    #     status_lenght = client.recv(HEADER).decode(FORMAT)
    # except socket.timeout as e:
    #     print("[TIME OUT] Timed out after 5 seconds")
    #     client.send(DISCONNECT_MESSAGE)
    # print(status_lenght)
    # if status_lenght:
    #     status_lenght = int(status_lenght)
    #     status = client.recv(status_lenght).decode(FORMAT)
    #     print(status)
    # else:
    #     print("Didn't recieve a message")
    
thread = threading.Thread(target=recieve_status_message) # * execute client handling in a new thread
thread.start()
send("YES")
input()
send("YES")
input()
send("What")
input()
send("YES")
input()
send("YES")
input()
send("NO")
input()
send("YES")
input()
send("YES")
input()
send("NO")
send(DISCONNECT_MESSAGE)
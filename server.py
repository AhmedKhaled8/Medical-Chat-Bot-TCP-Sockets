import socket
import threading
import respond


# * DEFINING STANDARDS OF THE TCP STREAM SOCKET CONNECTION
HEADER = 64  # * Define a constant size of the header
PORT = 5050  # * Define a port for the socket
# * Define the IPv4 address the socket will bind to. Here we use the local host
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS = (SERVER, PORT)  # * Address tuple to use for the binding
FORMAT = 'utf-8'  # * A decoding/encoding format of the messages
DISCONNECT_MESSAGE = '!DISCONNECT'  # * A defined disconnect message
IDLE_MESSAGE = 'IDLE'

# * Defining a socket object with address family of IPv4 and socket type for TCP using SOCK_STREAM
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)  # * Associate the socket to a specific network and port

clients_database = {}  # * A dictionary holds the answers of each client


def handle_client(conn, addr):
    """handle_client: a function that is executed in a separate thread for each client. it assigns a list for each unique client that contains the answers of the clients,
    responds with a status message to the client socket, when recieving a DISCONNECT_MESSAGE, it closes the connection.

    Args:
        conn (socket.socket): the client socket
        addr (tuple): the address of the client
    """
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True  # ! setting the connection status to True
    # ! assigning a new list in the clients dictionary
    clients_database[addr[1]] = []
    while connected:
        try:
            conn.settimeout(20.0)
            # * Recieve the header of the message
            msg_length = conn.recv(HEADER).decode(FORMAT)
            conn.settimeout(None)
            if msg_length:  # ? if the message isn't empty
                # * Get the actual length of the message
                msg_lenght = int(msg_length)
                msg = conn.recv(msg_lenght).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    print(f"[DISCONNECTED] {addr} has disconnected")
                    # ! setting the connection status to False, exit the loop and close the connection
                    connected = False
                    continue
                print(f"[{addr}] sent a message : {msg}")
                
                
                if msg == 'Yes':
                    # ? If the message is "YES", append a 1 to the list of the answers
                    clients_database[addr[1]].append(1)
                    # * Send a status message to the client confirming recieving a valid response
                    conn.send(create_status_message(addr[1], "VALID"))
                elif msg == 'No':
                    # ? If the message is "NO", append a 0 to the list of the answers
                    clients_database[addr[1]].append(0)
                    # * Send a status message to the client confirming recieving a valid response
                    conn.send(create_status_message(addr[1], "VALID"))
                else:
                    # * Send a status message to the client confirming recieving an invalid response
                    conn.send(create_status_message(addr[1], "INVALID"))
                    
        except socket.timeout as e:
            print("[TIME OUT] Timed out after 20 seconds")
            conn.send(create_status_message(addr[1], "IDLE"))
            print(f"[DISCONNECTED] {addr} has disconnected")
            connected = False

        except ConnectionResetError:
            print("[FORCED CLOSED] Connection to the socket was forcedly closed by the client ... ")
            connected = False


    conn.close()  # ! Closing the connection when exiting the stream or recieving an IDLE


def create_status_message(label, condition):
    """create_status_message: a function create a socket-encoded message include the status of the format of the message recieved by the server socket

    Args:
        label (int): the address of the client to access the clients database
        condition (str): VALID if the response is valid, INVALID if the response is invalid, IDLE if the connection is IDLE

    Returns:
        str: encoded status message
    """
    status_message = ""
    if len(clients_database[label]) != 9:
        if condition == "VALID":
            # ? If valid, create a confirmation message with the number of questions left
            status_message = f'[CONFIRMED] {9 - len(clients_database[label])} questions left'
        elif condition == "INVALID":
            # ? If not valid, create a confirmation of invalidaty message
            status_message = f'[UNVALID] Please send an appropiate response'
            # ? If the status is IDLE
        elif condition == "IDLE":
            status_message = DISCONNECT_MESSAGE
    elif len(clients_database[label]) == 9:
        status_message = respond.respond(clients_database[label])
        clients_database[label] = []
        

    # * Encoding the status message
    status_header = len(status_message)
    status = f"{status_header:<{HEADER}}"+status_message
    status_encoded = status.encode(FORMAT)
    return status_encoded


def start():
    """starting the server
    """
    print("[STARTING] server is starting ...")
    server.listen()  # * start the server on the network to which it was binded
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()  # * accept clients and take their sockets and addresses
        # * execute client handling in a new thread
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1} clients have connected ...")


start()

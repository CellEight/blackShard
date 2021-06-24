import socket
from Connection import Connection

class Network:
    def __init__(self, config, server_ip = "127.0.0.1", port = 54321):
        self.config = config
        self.server_ip = server_ip 
        self.port = port 
        self.create_socket()
   
    def listen_for_client(self):
        self.socket.listen()
        return Connection(self.config, *self.socket.accept(), self.server_ip, self.port)

    def create_socket(self):
        """ Creates a socket object and binds it to specified port and ip (interface). """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.server_ip, self.port))
        except Exception as e:
            self.socket = None
            print(f"[!] Failed to listen for clients on {self.server_ip}:{self.port}")
            print(e)
            exit(1)
            return False
        print(f"[*] Successfully created socket at {self.server_ip}:{self.port}")
        return True


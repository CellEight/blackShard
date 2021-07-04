import socket
import ssl
from Connection import Connection

class Network:
    def __init__(self, config, server_ip = "127.0.0.1", port = 54321, cert="../../certs/test_key_cert.pem"):
        self.config = config
        self.server_ip = self.config.server_ip 
        self.port = self.config.server_port
        # generate context
        self.ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self.ssl_context.load_cert_chain(certfile=cert)
        self.ssl_context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1  
        self.ssl_context.set_ciphers('EECDH+AESGCM:EDH+AESGCM:AES256+EECDH:AES256+EDH')
        self.create_socket()
   
    def listen_for_client(self):
        self.socket.listen()
        connection, client_ip = self.socket.accept()
        try:
            connection = self.ssl_context.wrap_socket(connection, server_side=True)
        except ssl.SSLError as e:
            print(e)
            print("[!] Could not establish a secure connection to the client.")
        return Connection(self.config, connection, client_ip , self.server_ip, self.port)

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


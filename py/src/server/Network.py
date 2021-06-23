import socket

class Network:
    def __init__(self, config, ip = "127.0.0.1", port = 54321):
        self.config = config
        self.server_ip = ip 
        self.server_port = port 
   
    def listen_for_client(self):
        try:
            return self.create_socket()
        except Exception as e:
            self.socket = None
            print(f"[!] Failed to listen for clients on {server_ip}:{server_port}")
            print(e)
            return False
        self.listen()
        self.client_conn, self.client_ip = s.accept()
        self.client_conn.sendall(self.config.header)
        print(f"[*] Successfully connected to client at {client_ip}")

    def create_socket():
        """ Creates a socket object and binds it to specified port and ip (interface). """
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.server_ip, self.server_port))
            print(f"[*] Successfully created socket at {server_ip}:{server_port}")
            return True

    def get_cmd(self):
        """ Listens for a command client and returns it as an ascii string. """
        cmd = self.client_conn.recv(1024).decode('ascii') #may not be a byte string?
        return cmd

    def get_data(self):
        pass

    def send_response(self):
        pass

    def send_data(self):
        pass

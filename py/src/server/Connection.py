
class Connection():
    def __init__(self, config, connection, client_ip, server_ip, server_port):
        self.config = config
        self.connection = connection
        self.client_ip = client_ip 
        self.server_ip = server_ip 
        self.server_port = server_port 
        self.send_data(self.config.header)
        print(f"[*] Successfully connected to client at {self.client_ip}")

    def get_cmd(self):
        """ Listens for a command client and returns it as an ascii string. """
        cmd = self.connection.recv(1024).decode('ascii') #may not be a byte string?
        return cmd

    def get_data(self):
        pass

    def send_response(self, response):
        if response:
            self.connection.sendall("True".encode('ascii'))
        else:
            self.connection.sendall("False".encode('ascii'))


    def send_data(self, data):
        self.connection.sendall(data.encode('ascii'))


class Connection():
    def __init__(self, config, connection, client_ip, server_ip, server_port):
        self.config = config
        self.connection = connection
        self.client_ip = client_ip 
        self.server_ip = server_ip 
        self.server_port = server_port 
        self.send_data(self.config.header)
        print(f"[*] Successfully connected to client at {self.client_ip}")

#Several of these functions need exception handling as well as debug messages

    def get_cmd(self):
        """ Listens for a command client and returns it as an ascii string. """
        cmd = self.connection.recv(1024).decode('ascii') #may not be a byte string?
        return cmd

    def send_data(self, data):
        """ Send a large block of data to the server such as a public key (send_cmd redundant?))"""
        try:
            self.connection.sendall(data.encode('ascii'))
            return True
        except Exception as e:
            print(e)
            return False

    def get_data(self):
        data = self.connection.recv(16384).decode('ascii')
        print(data)
        return data

    def send_response(self, response):
        if response:
            self.connection.sendall("True".encode('ascii'))
        else:
            self.connection.sendall("False".encode('ascii'))


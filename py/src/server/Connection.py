
class Connection():
    def __init__(self, config, connection, client_ip, server_ip, server_port):
        self.config = config
        self.connection = connection
        self.client_ip = client_ip 
        self.server_ip = server_ip 
        self.server_port = server_port 
        self.send_str_data(self.config.header)
        print(f"[*] Successfully connected to client at {self.client_ip}")

#Several of these functions need exception handling as well as debug messages

    def get_cmd(self):
        """ Listens for a command client and returns it as an ascii string. """
        cmd = self.connection.recv(1024).decode('ascii') #may not be a byte string?
        return cmd
    
    def send_str_data(self, data):
        return self.send_byte_data(data.encode('ascii'))

    def send_byte_data(self, data):
        """ Send a large block of data to the server such as a public key (send_cmd redundant?))"""
        print(data)
        try:
            self.connection.send(data)
            return True
        except Exception as e:
            print(e)
            return False

    def get_str_data(self):
        return self.get_byte_data().decode('ascii')

    def get_byte_data(self):
        data = self.connection.recv(16384)
        print(data)
        return data

    def send_response(self, response):
        if response:
            self.connection.send("True".encode('ascii'))
        else:
            self.connection.send("False".encode('ascii'))


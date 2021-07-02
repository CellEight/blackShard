
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
        try:
            cmd = self.connection.recv(1024).decode('ascii') #may not be a byte string?
        except Exception as e:
            print("[!] ***The user vomits nonsense at the sever***")
            return None
        return cmd
    
    def send_str_data(self, data):
        return self.send_byte_data(data.encode('ascii'))

    def send_byte_data(self, data):
        """ Send a large block of data to the server such as a public key (send_cmd redundant?))"""
        data_len = len(data)
        print("Data is of length ",data_len)
        n_blocks = int(data_len//1024 if data_len//1024 == data_len/1024 else data_len//1024 + 1) # get rid of 1024, magic number
        print("Data is ",n_blocks," blocks in length")
        try:
            self.connection.send(str(n_blocks).encode('ascii'))
            for i in range(n_blocks):
                self.connection.send(data[i*1024:(i+1)*1024])
            return True
        except Exception as e:
            print(e)
            return False

    def get_str_data(self):
        return self.get_byte_data().decode('ascii')

    def get_byte_data(self):
        # add exception handling
        print("Getting data")
        n_blocks = int(self.connection.recv(1024).decode('ascii'))
        print("Data is ", n_blocks, " blocks in length.")
        data = b''
        for i in range(n_blocks): 
            data += self.connection.recv(1024)
        print(data)
        return data

    def send_response(self, response):
        if response:
            self.connection.send("True".encode('ascii'))
        else:
            self.connection.send("False".encode('ascii'))


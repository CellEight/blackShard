import socket

class Network:
    def __init__(self):
        self.server_ip = None
        self.server_port = None
        self.socket = None
        self.user = None
        self.pwd = '/'
   
    def connect(self, server):
        """ Handles the logical flow of connecting to the server"""
        server = server.split(':')
        # Add more input validation
        if len(server) != 2:
            print("[!] Invalid address format, use <server-ip>:<server-port>.")
            return False
        else:
            self.server_ip = server[0]
            self.server_port = int(server[1])
        try:
            return self.create_socket()
        except Exception as e:
            self.server_ip = None
            self.server_port = None
            self.socket = None
            print(e)
            print(f"[!] Failed to connect to {server_ip}:{server_port}")
            return False

    def create_socket(self):
        """ Create a new socket connection to the server """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server_ip, self.server_port))
        header = repr(self.socket.recv(1024))
        print(f"[*] Successfully Connected to {server_ip}:{server_port}")
        print(header)
        return True

    def get_login_cipher(self, user):
        """ Contacts the server to initalize login process and receives cipher 
            text encoded using users public key in order to verify user identity. """
        cipher = self.get_data() 
        print("[*] Login Challenge Received. Decoding and Responding")
        return cipher

    def send_login_response(self, response):
        """ Sends the deciphered challenge back to the server and 
            verifies response was valid. """
        self.send_data()
        if self.get_response():
            print("[*] Response Validated.")
            return True
        else:
            print("[!] Response Invalid.")
            return False

    def register(self, user, public_key):
        """ Sends newly generated public key of candidate user to the server 
            and gets confirmation of registration. """
        if self.send_cmd(f"register {user}", public_key):
            self.user = user
            return True
        else:
            return False

    def unregister(self):
        if not self.socket:
            print("[!] You are not yet connected to a sever!")
            return False
        elif not self.socket:
            print("[!] You are not yet logged into a sever!")
            return False
        return self.send_cmd(f'unregister')

    def logout(self):
        if not self.socket:
            print("[!] You are not yet connected to a sever!")
            return False
        elif not self.socket:
            print("[!] You are not yet logged into a sever!")
            return False
        return self.send_cmd(f'logout')


    def ls(self):
        if not self.socket:
            print("[!] You are not yet connected to a sever!")
            return False
        elif not self.socket:
            print("[!] You are not yet logged into a sever!")
            return False
        return self.send_cmd(f'ls', get_reply=True)

    def cd(self, directory):
        if not self.socket:
            print("[!] You are not yet connected to a sever!")
            return False
        elif not self.socket:
            print("[!] You are not yet logged into a sever!")
            return False
        if self.send_cmd(f'cd {directory}'):
            self.pwd = directory
        else:
            print("[!] Failed to change directory.")

    def create_note(self, note_id):
        return self.send_cmd(f'create {note_id}')

    def get_note(self, note_id):
        return self.send_cmd(f'update {note_id}', get_reply = True)

    def update_note(self, note_id, cipher):
        return self.send_cmd(f'update {note_id}', cipher)

    def delete_note(self, note_id):
        return self.send_cmd(f'del {note_id}')

    def check_note_exist(self, note_id):
        return self.send_cmd(f'exists note {note_id}')

    def check_priv(self, note_id, operation):
        return self.send_cmd(f'priv {note_id} {operation}')

    def send_cmd(self, cmd, data = None, get_reply = False):
        """ Send a command to the server along with an optional data 
            and optionally get data from the server"""
        try:
            self.socket.sendall(cmd.encode('ascii'))
            if data:
                self.socket.sendall(data.encode('ascii'))
            response = repr(self.socket.recv(1024))
            if self.get_reply():
                reply = repr(self.socket.recv(1024)) # May need to increase from 1024 to something larger
                if response == "yes":
                    return True, reply
                elif response == "no":
                    return False, None
                else:
                    raise Exception("[!] Error! Received Garbage response form server.")
            else:
                if response == "yes":
                    return True
                elif response == "no":
                    return False
                else:
                    raise Exception("[!] Error! Received Garbage response form server.")
        except Exception as e:
            print(e)
            if get_reply:
                return False, None
            else:
                return False
    def send_data(self, data):
        pass

    def get_response(self):
        response = repr(self.socket.recv(1024)).decode("ascii")
        if response == "True":
            return True
        else:
            return False

import socket
import ssl
import json
import re

class Network:
    def __init__(self):
        self.server_ip = None
        self.server_port = None
        self.socket = None
        self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        # not optional, TLS1.0/1 are not secure, do not use them
        self.context.options |= ssl.OP_NO_TLSv1 | ssl.OP_NO_TLSv1_1
        self.context.load_verify_locations('../../certs/test_cert.pem')
  
    # Connection Methods

    def connect(self, server):
        """ Handles the logical flow of connecting to the server"""
        server = server.split(':')
        if len(server) != 2:
            print("[!] Invalid address format, use <server-ip>:<server-port>.")
            return None
        elif not self.is_valid_ip_address(server[0]):
            print(f"[!] {server[0]} is not a valid IPv4 address.")
            return None
        self.server_ip = server[0]
        self.server_port = int(server[1])
        try:
            if self.create_socket():
                return self.get_str_data()
            else:
                return None
        except Exception as e:
            self.server_ip = self.server_port = self.socket = None
            print(e)
            print(f"[!] Failed to connect to {self.server_ip}:{self.server_port}")
            return False

    def disconnect(self):
        """ Coordinate disconnect of the client from the server. """
        try:
            # Tell the server we're leaving
            #self.send_cmd("disconnect")
            self.socket.close()
            # Return everything to its default state
            self.socket = None
            self.server_ip = None
            self.server_port = None
            return True
        except Exception as e:
            print(e)
            return False

    def create_socket(self):
        """ Create a new socket connection to the server """
        self.socket = self.context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM),server_hostname=self.server_ip)
        try:
            self.socket.connect((self.server_ip, self.server_port))
            header = self.socket.recv(1024).decode("ascii")
        except Exception as e:
            print(e)
            print("[!] Could not establish connection.")
            self.socket = None
            return False
        print(f"[*] Successfully Connected to {self.server_ip}:{self.server_port}")
        print(header)
        return True

    def is_valid_ip_address(self, addr):
        """ Check using a regex that the supplied string is a valid ip address """
        ip_exp = "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        if re.match(ip_exp,addr):
            return True
        else:
            return False

    # User Management Methods

    def get_login_cipher(self, user):
        """ Contacts the server to initialize login process and receives cipher 
            text encoded using users public key in order to verify user identity. """
        cipher = self.get_raw_data() 
        print("[*] Login Challenge Received. Decoding and Responding")
        return cipher

    def send_login_response(self, response):
        """ Sends the deciphered challenge back to the server and 
            verifies response was valid. """
        self.send_raw_data(response)
        if self.get_response():
            print("[*] Response Validated.")
            return True
        else:
            print("[!] Response Invalid.")
            return False

    def register(self, user, public_key):
        """ Sends newly generated public key of candidate user to the server 
            and gets confirmation of registration. """
        if self.send_cmd(f"register {user}"):
            self.send_str_data(public_key)
            if self.get_response():
                return True
            else:
                print("[!] Failed to create new user.")
                return False
        else:
            return False

    def unregister(self, username):
        return self.send_cmd(f'unregister {username}')

    def logout(self):
        """ Instruct the server to logout current user. """
        if self.send_cmd(f'logout') and self.get_response():
            return True
        else:
            return False

    # Directory Methods
    
    def mkdir(self, dir_name, pwd_id):
        """ Ask the server to create a directory in the specified pwd. """
        if self.send_cmd(f'mkdir {dir_name} {pwd_id}') and self.get_response():
            print(f"[*] Directory {dir_name} created in present working directory.")
            return True
        else:
            print(f"[!] Could not create directory {dir_name}.")
            return False

    def get_dir(self, dir_id):
        """ Ask the server for a directories dictionary. """
        try:
            if self.send_cmd(f'get_dir {dir_id}') and self.get_response():
                return json.loads(self.get_str_data())
            else:
                print("[!] Could not retrieve directory information. Does it really exist?")
                return None
        except Exception as e:
            print(e)
            print("[!] Could not retrieve directory information.")
            return None

    def rename_directory(self, dir_id, new_dim_name):
        pass

    def rm_dir(self, dir_id):
        """ Ask the server to delete the directory with the given id. """
        try:
            if self.send_cmd(f'rm_dir {dir_id}') and self.get_response():
                print(f"[*] Deleted directory with id {dir_id}.")
                return True
            else:
                print(f"[!] Could not delete directory with id {dir_id}.")
                return False
        except Exception as e:
            print(e)
            print(f"[!] Could not delete directory with id {dir_id}.")
            return False
        

    # Note Methods

    def create_note(self, note_name, enc_aes_key, dir_id):
        """ Ask the server to create a new note in the specified directory 
            with the specified name. """
        if self.send_cmd(f'create_note {note_name} {dir_id}') and self.get_response():
            self.send_raw_data(enc_aes_key)
            if self.get_response():
                return self.get_str_data() # get the note_id
            else:
                return None
        else:
            return None

    # Maybe change this up so notes are dicts/lists and are sent as json objects?
    def get_note(self, note_id):
        """ Ask the server to retrieve a specific note. """
        if self.send_cmd(f'get_note {note_id}') and self.get_response():
            cipher = self.get_raw_data()
            enc_aes_key = self.get_raw_data()
            iv = self.get_raw_data()
            print(type(cipher),cipher)
            return cipher, enc_aes_key, iv
        else:
            return None, None

    def update_note(self, note_id, cipher, iv):
        """ Ask the server to update the contents of a note. """
        if self.send_cmd(f'update_note {note_id}') and self.get_response():
            self.send_raw_data(cipher)
            self.send_raw_data(iv)
            if self.get_response():
                return True
            else:
                return False
            
    def rm_note(self, note_id):
        """ Ask the sever to delete specific note. """
        if self.send_cmd(f'rm_note {note_id}') and self.get_response():
            return True
        else:
            return False

    # Transmission Methods
    
    # Could I add another get response that verifies the success or failure of the command 
    # or even just if you have permissions require for an action? Could allow for better 
    # error messages to the user.
    def send_cmd(self, cmd):
        """ Send a command to the server and get response confirming validity.
            Return True if sever confirms validity of command and False otherwise."""
        try:
            self.socket.send(cmd.encode('ascii'))
            if self.get_response():
                return True
            else:
                print("[!] Server reported invalid command.")
                return False 
        except Exception as e:
            print(e)
            return False

    def send_str_data(self, data):
        return self.send_raw_data(data.encode('ascii'))

    def send_raw_data(self, data):
        """ Send a large block of data to the server such as a public key (send_cmd redundant?))"""
        try:
            print(data)
            self.socket.send(data)
            return True
        except Exception as e:
            print(e)
            return False

    # All of these functions need exception handling as well as debug messages

    def get_str_data(self):
        return self.get_raw_data().decode('ascii')

    def get_raw_data(self):
        data = self.socket.recv(16384)
        #print(data)
        return data

    def get_response(self):
        response = self.socket.recv(1024).decode("ascii")
        if response == "True":
            return True
        else:
            return False


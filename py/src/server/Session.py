from Crypt import Crypt
from bson import ObjectId
import json

class Session():
    def __init__(self, config, connection, db):
        self.config = config
        self.connection = connection 
        self.db = db
        self.crypto = Crypt()
        self.user = None

    def listen_for_cmd(self):
        """ Listens for commands from clients and hands them off to be parsed. """
        cmd = self.connection.get_cmd()
        return self.parse_cmd(cmd)

    def parse_cmd(self,cmd):
        """ Parse command acquired by listen_for_cmd and extract arguments and 
            call appropriate function to execute it. """
        cmd = cmd.lower().split()
        if len(cmd) == 1:
            if cmd[0] == "logout":
                return self.logout()
            elif cmd[0] == "ls":
                return self.ls()
        elif len(cmd) == 2:
            if cmd[0] == "login":
                return self.login(cmd[1])
            elif cmd[0] == "register":
                return self.register(cmd[1])
            elif cmd[0] == "unregister":
                return self.unregister(cmd[1])
            elif cmd[0] == "cd":
                return self.cd(cmd[1])
            elif cmd[0] == "get_dir":
                return self.get_dir(cmd[1])
            elif cmd[0] == "rm_dir":
                return self.rm_dir(cmd[1])
            elif cmd[0] == "get_note":
                return self.get_note(cmd[1])
            elif cmd[0] == "update_note":
                return self.update_note(cmd[1])
            elif cmd[0] == "rm_note":
                return self.update_note(cmd[1])
            elif cmd[0] == "check_priv":
                return self.check_priv(cmd[1])
        elif len(cmd) == 3:
            if cmd[0] == "mkdir":
                return self.mkdir(cmd[1], cmd[2])
            elif cmd[0] == "create_note":
                return self.create_note(cmd[1], cmd[2])
        return self.invalid_command()
    
    #implement a disconnect method

    def invalid_command(self):
        """ Handles response to the client in the event of gibberish command. """
        try:
            self.connection.send_response(False) 
            return True
        except Exception as e:
            print(e)
            return False

    def valid_command(self):
        """ Informs the client that the received command was indeed valid. """
        try:
            self.connection.send_response(True) 
            return True
        except Exception as e:
            print(e)
            return False

    def login(self, username):
        """ Handles the process of user login and verification. The users identify 
            is verified using their RSA key pair via a similar technique that used 
            by SSH for user authentication. See this link for an outline of the 
            algorithm https://www.digitalocean.com/community/tutorials/understanding-the-ssh-encryption-and-connection-process#authenticating-the-user-39-s-access-to-the-server"""
        if not self.valid_command():
            return True
        print(f"[*] Got a login request for account {username}")
        user = self.db.get_user(username) # user is an abstract object yet to be defined
        if not user:
            print("[!] User does not exist.")
            self.connection.send_response(False)
            return True 
        else:
            self.connection.send_response(True)
        self.crypto.load_user_public_key(user)
        challenge, cipher = self.crypto.generate_login_cipher()
        self.connection.send_raw_data(cipher)
        data = self.connection.get_raw_data()
        if challenge == data:
            self.user = user
            print(f"[*] User {user['username']} logged in.")
            self.connection.send_response(True)
            return True 
        else:
            print(f"[!] User {user['username']} failed to logged in.")
            self.connection.send_response(False) 
            return True 

    def logout(self):
        if not self.valid_command():
            return True
        print(f"[*] Logging user {self.user['username']} out of the server.")
        self.user = None
        self.connection.send_response(True)
        print(f"[*] Annnnd they're gone.")
        return True

    def register(self, username):
        # add exception handling
        if not self.valid_command():
            return True
        public_key = self.connection.get_str_data()
        self.connection.send_response(self.db.create_user(username, public_key))
        self.user = self.db.get_user(username)
        return True

    def unregister(self, username):
        """ Remove the user with the specified username form the database. """
        # May need to add additional code to clean up all the notes they own?
        if not self.valid_command():
            return True
        try:
            if self.db.delete_user(username):
                self.connection.send_response(True)
                print(f"[*] User {username} has been deleted.")
                return True
            else:
                self.connection.send_response(False)
                print(f"[!] Could not delete user {username} from the database.")
                return False
        except Exception as e:
            print(e)
            self.connection.send_response(False)
            print(f"[!] Could not delete user {username}.")
            return False

    # Directory Management Methods

    def mkdir(self, dir_name, pwd_id):
        """ Instruct the DB to create a new directory. """
        pwd_id = ObjectId(pwd_id)
        if not self.valid_command():
            return True
        # verify privs
        # verify that file/folder not already present
        if self.db.mkdir(dir_name, pwd_id, self.user['_id']):
            self.connection.send_response(True)
            print(f"[*] Created new directory {dir_name} in {pwd_id}.")
            return True
        else:
            self.connection.send_response(False)
            print(f"[!] Failed to create new directory {dir_name} in {pwd_id}.")
            return True

    def get_dir(self, dir_id):
        """ Ask the DB for directory and send it back to the user. """
        dir_id = ObjectId(dir_id)
        if not self.valid_command():
            return True
        # maybe verify privs?
        _dir = self.db.get_dir(dir_id)
        _dir['_id'] = str(_dir['_id'])
        if _dir:
            self.connection.send_response(True)
            self.connection.send_str_data(json.dumps(_dir))
            return True
        else:
            self.connection.send_response(False)
            return True

    def rm_dir(self, dir_id):
        """ Ask the database to delete the specified directory. """
        dir_id = ObjectId(dir_id)
        if not self.valid_command():
            return True
        if self.db.rm_dir(dir_id):
            # add verification of priv here
            self.connection.send_response(True)
            print(f"[*] Deleted directory with id {dir_id}")
            return True
        else:
            self.connection.send_response(False)
            print(f"[*] Database would not delete directory.")
            return True

    # Note Management Methods 

    def create_note(self, note):
        if not self.valid_command():
            return True
        pass

    def get_note(self, note):
        if not self.valid_command():
            return True
        pass

    def update_note(self, note):
        if not self.valid_command():
            return True
        pass

    def delete_note(self, note):
        if not self.valid_command():
            return True
        pass

    def check_priv(self, obj):
        if not self.valid_command():
            return True
        pass

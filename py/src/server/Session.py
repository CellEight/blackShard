from Crypt import Crypt

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
            elif cmd[0] == "get_note":
                return self.get_note(cmd[1])
            elif cmd[0] == "update_note":
                return self.update_note(cmd[1])
            elif cmd[0] == "delete_note":
                return self.update_note(cmd[1])
            elif cmd[0] == "create_note":
                return self.create_note(cmd[1])
            elif cmd[0] == "check_priv":
                return self.check_priv(cmd[1])
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
        """ Informs the client that the recived command was indeed valid. """
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
        self.valid_command()
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
        print(data)
        if challenge == data:
            self.user = user
            self.connection.send_response(True)
            return True 
        else:
            self.connection.send_response(False) 
            return True 

    def logout(self):
        print(f"[*] Logging user {self.user['username']} out of the server.")
        self.user = None
        self.connection.send_response(True)
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

    def ls(self):
        pass
    
    def cd(self, directory):
        pass

    def create_note(self, note):
        pass

    def get_note(self, note):
        pass

    def update_note(self, note):
        pass

    def delete_note(self, note):
        pass

    def check_priv(self, obj):
        pass

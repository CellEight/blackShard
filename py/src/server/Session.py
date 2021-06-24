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
            elif cmd[0] == "unregister":
                return self.unregister()
            elif cmd[0] == "ls":
                return self.ls()
        elif len(cmd) == 2:
            if cmd[0] == "login":
                return self.login(cmd[1])
            elif cmd[0] == "register":
                return self.register(cmd[1])
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

    def invalid_command(self):
        """ Handles response to the server in the event of gibberish command. """
        pass

    def login(self, username):
        """ Handles the process of user login and verification. """
        print(f"[*] Got a login request for account {username}")
        user = self.db.get_user(username) # user is an abstract object yet to be defined
        if not user:
            print("[!] User does not exist.")
            self.connection.send_response(False)
            return True 
        else:
            self.connection.send_response(True)
        self.crypto.load_user_public_key(user)
        self.connection.send_data(self.crypto.generate_login_cipher())
        data = self.connection.get_data()
        if self.crypto.validate_login_cipher_data(data):
            self.user = user
            self.connection.send_response(True)
            return True 
        else:
            self.connection.send_response(False) 
            return True 

    def logout(self):
        self.user = None
        return True

    def register(self, user):
        pass

    def unregister(self):
        pass

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

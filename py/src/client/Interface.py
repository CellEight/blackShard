# Libraries
# ---------
import os, signal
from termcolor import colored
from Crypt import Crypt
from Network import Network
from Config import Config


# This class is called terminal rather than interface as I intend to add a second class to handel
# the use of the application directly from the unix command line
class Terminal:
    """ Provides methods that provide command line functionality to let the user 
    load and run additional modules and provides the interface to let them interface
    with those modules """
    def __init__(self, motd=True):
        self.net = Network()
        self.config = Config()
        self.crypto = Crypt('nopasswordyet')
        if motd:
            self.showMotd()
    
    def showMotd(self):
        """ print motd banner """
        buff='    __    __           __   _____ __                   __\n'
        buff+='   / /_  / /___ ______/ /__/ ___// /_  ____ __________/ /\n'
        buff+='  / __ \\/ / __ `/ ___/ //_/\\__ \\/ __ \\/ __ `/ ___/ __  / \n'
        buff+=' / /_/ / / /_/ / /__/ ,<  ___/ / / / / /_/ / /  / /_/ /  \n'
        buff+='/_.___/_/\\__,_/\\___/_/|_|/____/_/ /_/\\__,_/_/   \\__,_/   \n'
        buff+='                                                         \n'
        print(buff,'\n')
        buff='                                   .---._\n'
        buff+='                                  /==----\\_\n'
        buff+='                 |\\              |8=---()-\\|   |\\\n'
        buff+='         /|      ::\\             |8=-/|\\(_)>_   \\\\\n'
        buff+='         |:\\     `::\\_            \\=/:\\= (_)\\|   |\\\n'
        buff+='         `::|     |::::.            \\;:\\=\\(_)>_  |\\\\\n'
        buff+='          |b\\\\_,_ \\`::::\\             \\:\\=\\( \\/  \\_(\n'
        buff+="          `\\88b`\\|/|'`:::\\   .-----   :8:\\=|`=>_  [d[\n"
        buff+='           \\;\\88b.\\=|///::`-/::;;;;:\\ |8;|=\\( )/   [8[\n'
        buff+="      __    ||/`888b.\\_\\/\\:/:;/'/-\\::\\/( \\|=(=)>_  [d|\n"
        buff+='     //):.. `::|/|\\"96.\\|//;/|\'| /-\\::+\\|-\\=(. )/  [8[\n'
        buff+='    |(/88e::.. `\'.|| "min;/\\\\/8|\\.-|::|8|||=|`=\'_  `[d|\n'
        buff+='     `-|8888ee::,,,`\\/88utes8P//8|-|::|8||\\=|( )/   ]8[\n'
        buff+='      |:`"|####b:::/8pq8e/::\'`;q8|/::dP\'|\\|=|`=\'_   [d|\n'
        buff+=' .=-. \\::..`""##Gst:q| e|:/..\\:|8|.:/|\'/\\/|/|(_)/   ]8[\n'
        buff+="/(,:;:, \\::::.\\#/88q;`;'\\||.:/-//.;/<8\\\\\\^\\||./>    `]d[\n"
        buff+='`8888b::,,_ ::/88q;.`;|d8/`-.]/|./  |8|\\|:|;/.d|     [8|\n'
        buff+='  `"88###n::-/d8P.\\e/-|d/ _//;;|/   |8(|::(/).8/     ]d[\n'
        buff+='    `"###o2:1dP;`q./=/d/_//|8888\\   ;8|^\\/`-\'8/      [8\\\n'
        buff+='       `"v7|9q8e;./=/d//=/\\|eeeb|  /dP= =<ee8/       ]d-\n'
        buff+="          \\|9; qe/-d/ .|/=/888|:\\ `--=- =88p'        [8[\n"
        buff+='          (d5b;,/ d/.|/=-\\Oo88|:/                   ,8_\\\n'
        buff+="         _|\\q88| d/ /'=q8|888/:/                    ]d|\n"
        buff+='        _\\\\\\/q8/|8\\_""/////eb|/_                    [8_\\\n'
        buff+='        \\|\\\\<==_(;d888b,.////////--._               ]8|\n'
        buff+='       _/\\\\\\/888p |=""";;;;`eee.////.;-._          ,8p\\\n'
        buff+='      /,\\\\\\/88p\\ /==/8/.\'88`""""88888eeee`.        ]8|\n'
        buff+='    .d||8,\\/p   /-dp_d8|:8:.d\\=\\    `""""|=\\\\     .[8_\\\n'
        buff+="    |8||8||8.-/'d88/8p/|:8:|8b\\=\\        /|\\\\|    ]8p|\n"
        buff+="    |8||8||8b''d.='8p//|:8:'`88b`\\       |||||)   [8'\\\n"
        buff+="    `8b:qb.\\888:e8P/'/P'8:|:8:`888|      |'\\||'  /8p|\n"
        buff+="     q8q\\\\qe---_P;'.'P|:8:|:8:|`q/\\\\     '_///  /8p_\\\n"
        buff+="     _|88b-:==:-d6/P' |8::'|8:| ,|\\||    '-=' .d8p/\n"
        buff+="    |__8Pdb-q888P-'  .:8:| |8:| |/\\||\\     .-e8p/\\|\n"
        buff+="     .-\\888b.__      |:8/' |8:| \\ _|;|,-eee8\\8\\|\n"
        buff+="     \\.-\\'88/88/e.e.e|8/|\\_--.-.-e8|8|88\\8p\\|\n"
        buff+="       .'`-;88]88|8|/':|:\\ `q|8|8|8'-\\| \\|\n"
        buff+="        `' || || |_/(/|;\\)`-\\\\`--,\\|\n"
        buff+='              `\' /v"""\' `""""""vVV\\\n'
        print(buff)
    
    def commandLine(self):
        """ Show the command line and take input """
        while True:
            if self.net.server_ip != None:
                if self.net.user:
                    cmd = input(f'blackShard~{self.net.user}@{self.net.server_ip}-{self.net.pwd}# ')
                else:
                    cmd = input(f'blackShard~anonymous@{self.net.server_ip}-{self.net.pwd}# ')
            else:
                cmd = input(f'blackShard~# ')
            self.run_command(cmd)
    
    def is_connected(self):
        """ Just checks if a connection to a server has yet been made. """
        if not self.net.socket:
            print(f"[!] You are not yet connected to a server!")
            return False
        else:
            return True

    def is_logged_in(self):
        """ Just checks if the client is logged in. """
        if not self.net.user:
            print(f"[!] You are not yet logged in!")
            return False
        else:
            return True

    # Add better error and failure handling to all of these methods

    def read(self, note_id):
        """ Download a local copy of note decrypt and open in text editor """
        if not self.net.user:
            print(f"[!] You are not yet logged into a server!") 
            return False
        elif not self.net.note_exists(note_id):
            print(f"[*] No note of this name exist at current location.")
            return False
        elif not self.net.check_privilages(note_id, 'r'):
            print(f"[*] You lack the privileges required to read this file")
            return False
        response, cipher = self.net.get(note_id)
        if cipher:
            note = self.crypto.decrypt(cipher)
            with open(f'/tmp/{note_id}.txt', 'w') as f:
                f.write(note)
            os.system(f"{self.config.text_editor} /tmp/{note_id}.txt")
        return True
    
    def edit(self, note_id):
        """ Read a file with read() and then send any updates back to the server. """
        if not self.net.user:
            print(f"[!] You are not yet logged into a server!") 
            return False
        elif not self.net.note_exists(note_id):
            print(f"[*] No note of this name exist at current location.")
            return False
        elif not self.net.check_privilages(note_id, 'e'):
            print(f"[*] You lack the privileges required to edit this note.")
            return False
        self.read(note_id)
        with open(f'/tmp/{note_id}.txt', 'r') as f:
            note = f.read()
        cipher = self.crypto.encrypt(note)
        if self.net.update(note_id, cipher):
            print(f"[*] Note '{note_id}' was successfully updated.")
            return True
        else:
            print(f"[*] Note '{note_id}' could not be updated.")
            return False 

    def create_note(self, note_name): 
        """ Create a new note with the specified id and edit. """
        if not self.net.user:
            print(f"[!] You are not yet logged into a server!") 
            return False
        elif not self.net.check_privilages(note_name, 'c'):
            print(f"[*] You lack the privileges required to create a file in this location.")
            return False
        elif self.net.note_exists(note_id):
            print(f"[*] A note of the same name already exists at this location.")
            return False
        self.net.create(note_id)
        return self.edit(note_id)
       
    def delete(self, note_id):
        """ Delete a specified note """
        if not self.net.user:
            print(f"[!] You are not yet logged into a server!") 
            return False
        elif not self.net.note_exists(note_id):
            print(f"[*] No note of this name exist at current location.")
            return False
        elif not self.net.check_privilages(note_id, 'd'):
            print(f"[*] You lack the privileges required to delete this note.")
            return False
        return self.net.delete(note_id)

    def login(self, user):
        """ Login to the server as the specified user"""
        if not self.is_connected():
            return False
        self.net.send_cmd(f"login {user}")
        if not self.net.get_response():
            print("[!] User does not exist on this server.")
            return False
        try:
            cipher = self.net.get_login_cipher(user)
            self.crypto.load_keypair(self.net.server_ip, user)
            response = self.crypto.decrypt_bytes(cipher)
            if self.net.send_login_response(response):
                self.net.user = user
                print(f"[*] Login Successful. Welcome {user}.")
                return True
            else:
                print(f"[!] Login Failed. Are you sure you're in the right place son?")
                return False
        except Exception as e:
            print(e)
            print(f"[!] Login Failed.")
            return False
    
    def logout(self):
        """ Logs the user out of the server. """
        if not self.is_connected():
            return False
        if not self.is_logged_in():
            return False
        if self.net.logout():
            self.crypto.current_keypair = None
            print("[*] You have been logged out.")
            return True
        else:
            print("[!] Failed to logout!")
            return False

    def register(self, user):
        """ Asks server to create a new account and, if possible, it creates a 
            new key pair and communicates the public key to the server ."""
        if not self.is_connected():
            return False
        if self.net.check_privilages(None, 'g'): # g for reGister, I am deeply sorry
            if self.crypto.generate_keypair(self.net.server_ip, user):
                public_key = self.crypto.current_keypair.publickey().exportKey().decode('ascii')
                if self.net.register(user, public_key):
                    print(f"[*] Registration complete. Welcome to the server {user}.")
                    return True
                else:
                    self.crypto.current_key = None
                    print("[!] Registration failed. Try again?")
                    return False
            else:
                return False
        else:
            print("[!] You are not permitted to perform this action.")
            return False

    def unregister(self, username):
        """ Instructs the server to delete the active user and if success purges 
            their keys from the key database """
        # Add check that the user has the privileges to do this
        if not self.is_connected():
            return False
        elif self.net.unregister(username):
            self.net.user = None
            if self.crypto.delete_keypair(f'{self.net.server_ip}-{user}'):
                print("[*] User deleted from server and keys purged form key database.")
                return True 
            else:
                print("[~] User deleted from server but could not purge keys form key db.")
                return False
        else:
            print("[!] Failed to delete user from server. Try again or contact Admin.")

    def connect(self,ip_port):
        """ Silly yes, but I am aesthetically uncomfortable with  run_command calling 
            functions from the network class"""
        return self.net.connect(ip_port)

    def disconnect(self):
        """ Tells the network class to close the connection to the server """
        if not self.is_connected():
            return False
        elif self.net.disconnect():
            print("[*] Disconnected form the server.")
            return True
        else:
            print("[!] Failed to disconnect. Maybe time from CTRL-C?")
            return False


    def run_command(self, cmd):
        """ Parses command and performs the specified action or prints error if malformed"""
        cmd = cmd.strip().split(' ')
        # refactor these silly if statments
        if len(cmd) == 1:
            if cmd[0] == 'disconnect':
                return self.disconnect()
            elif cmd[0] == 'logout':
                return self.logout()
            elif cmd[0] == 'ls':
                return self.net.ls()
            elif cmd[0] == 'list-keys':
                return self.crypto.list_keypairs()
            elif cmd[0] == "help":
                # Display help
                return self.help()
            elif cmd[0] == "motd":
                # Print banner
                return self.showMotd()
            elif cmd[0] == "quit":
                # Exit to command line
                return self.quit()
        elif len(cmd) == 2:
            if cmd[0] == 'connect':
                return self.connect(cmd[1])
            elif cmd[0] == 'login':
                return self.login(cmd[1])
            elif cmd[0] == 'register':
                return self.register(cmd[1])
            elif cmd[0] == 'unregister':
                return self.net.unregister(cmd[1])
            elif cmd[0] == 'cd':
                return self.net.cd(cmd[1])
            elif cmd[0] == 'read':
                return self.read(cmd[1])
            elif cmd[0] == 'edit':
                return self.edit(cmd[1])
            elif cmd[0] == 'delete':
                return self.delete(cmd[1])
            # will implement later
            #elif cmd[0] == 'import-keys':
            #    return self.crypto.import_keypair(cmd[1])
        elif len(cmd) == 3:
            if cmd[0] == 'create' and cmd[1] == 'note':
                return self.create_note(cmd[1])
            elif cmd[0] == 'create' and cmd[1] == 'note':
                return self.create_dir(cmd[1])
        print('[!] Not a valid command! Type "help" for a list of commands')

    def help(self):
        """ Print help information """
        # Need to add disconnect
        print("----------Commands----------")
        print("connect <ip>:<port> - establish a connection to remote blackShard server.")
        print("disconnect - disconnect from the current server")
        print("login <user> - attempt to login to connected server as a given user.")
        print("logout - logout of current server.")
        print("register <user> - attempt to register a user on the connected server.")
        print("unregister <user> - attempt to delete user from the connected server.")
        print("ls - List contents of current directory on server.")
        print("cd <dir> - Change current directory to specified.")
        print("read <note> - read specified note.")
        print("edit <note> - edit specified note.")
        print("create note <note> - create a new note.")
        print("create dir <dir> - create a new note.")
        print("delete <note> - delete specified note.")
        # will implement later
        #print("import-keys <path> [<ip> <user>]- import the key pair from file optionally specifying server and user")
        print("list-keys - show a list of saved keys.")
        print("help - Prints this very message to the console.")
        print("motd - Displays the message of the day banner.")
        print("quit - Exits the program.")

    def isValidIpAddr(self, addr):
        """ Check using a regex that the supplied string is a valid ip address """
        return True

    def quit(self):
        """ Exit the program and return to the shell """
        exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda signum, stack : exit(1))
    term = Terminal("127.0.0.1")
    term.commandLine()

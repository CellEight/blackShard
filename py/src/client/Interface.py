# Libraries
# ---------
import os, subprocess, signal
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
        self.user = None
        self.pwd = None # maybe set this to None and init on connection? Should be a tuple or object really
    
    # Add better error and failure handling to all of these methods that need it

    # CLI Methods

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
                # update pwd
                self.pwd = self.net.get_dir(self.pwd['_id'])
                if self.user:
                    cmd = input(f'blackShard~{self.user}@{self.net.server_ip}-{self.pwd["dir_name"]}# ')
                else:
                    cmd = input(f'blackShard~anonymous@{self.net.server_ip}-{self.pwd["dir_name"]}# ')
            else:
                cmd = input(f'blackShard~# ')
            self.run_command(cmd)

    def run_command(self, cmd):
        """ Parses command and performs the specified action or prints error if malformed"""
        cmd = cmd.strip().split(' ')
        # refactor these silly if statments
        if len(cmd) == 1:
            if cmd[0] == 'disconnect':
                return self.disconnect()
            elif cmd[0] == 'logout':
                return self.logout()
            elif cmd[0] == 'pwd':
                return self.print_pwd()
            elif cmd[0] == 'ls':
                return self.ls()
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
            elif cmd[0] == 'mkdir':
                return self.mkdir(cmd[1])
            elif cmd[0] == 'cd':
                return self.cd(cmd[1])
            elif cmd[0] == 'create_note':
                return self.create_note(cmd[1])
            elif cmd[0] == 'read':
                return self.read_note(cmd[1])
            elif cmd[0] == 'edit':
                return self.edit_note(cmd[1])
            elif cmd[0] == 'rm':
                return self.rm(cmd[1])
            # will implement later
            #elif cmd[0] == 'import-keys':
            #    return self.crypto.import_keypair(cmd[1])
        elif len(cmd) == 3:
            if cmd[0] == "rm" and cmd[1] == "recursive":
                return self.rm(cmd[2],recursive=True)
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

    def quit(self):
        """ Exit the program and return to the shell """
        exit(0)


    # Connection Management Methods

    def is_connected(self):
        """ Just checks if a connection to a server has yet been made. """
        if not self.net.socket:
            print(f"[!] You are not yet connected to a server!")
            return False
        else:
            return True
   
    def connect(self,ip_port):
        """ Silly yes, but I am aesthetically uncomfortable with  run_command calling 
            functions from the network class"""
        # maybe move more logic here? Seems a bit sparse?
        init_pwd_id = self.net.connect(ip_port)
        if init_pwd_id:
            self.pwd = self.net.get_dir(init_pwd_id)
            return True
        else:
            return False

    def disconnect(self):
        """ Tells the network class to close the connection to the server """
        if not self.is_connected():
            return False
        elif self.net.disconnect():
            self.user = None
            self.pwd = None 
            print("[*] Disconnected form the server.")
            return True
        else:
            print("[!] Failed to disconnect. Maybe time from CTRL-C?")
            return False

    # User Management Methods

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
            response = self.crypto.rsa_decrypt_bytes(cipher)
            if self.net.send_login_response(response):
                self.user = user
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
        if (not self.is_connected()) or (not self.is_logged_in()):
            return False
        if self.net.logout():
            self.user = None
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
                    self.user = user
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
        if (not self.is_connected()) or (not self.is_logged_in()):
            return False
        elif self.net.unregister(username):
            self.user = None
            if self.crypto.delete_keypair(f'{self.net.server_ip}-{user}'):
                print("[*] User deleted from server and keys purged form key database.")
                return True 
            else:
                print("[~] User deleted from server but could not purge keys form key db.")
                return False
        else:
            print("[!] Failed to delete user from server. Try again or contact Admin.")

    def is_logged_in(self):
        """ Just checks if the client is logged in. """
        if not self.user:
            print(f"[!] You are not yet logged in!")
            return False
        else:
            return True

    # Note all path based functionality is very simple atm, cba to make it more 
    # complex yet as this will require me actually using my brain.

    # Common Note and Directory Methods

    # Add checks that user is logged in

    def rm(self, item):
        """ Delete a note or a directory in the present working directory. """
        if (not self.is_connected()) or (not self.is_logged_in()):
            return False
        if item in self.pwd['notes']:
            return self.rm_note(self.pwd['notes'][item]) 
        elif item in self.pwd['subdirs']:
            return self.rm_dir(self.pwd['subdirs'][item]) 
        else:
            print("[!] No such note or directory exists in present location.")
            return False

    def rename(self, item, new_item_name):
        """ Rename a note or a directory in the present working directory. """
        if (not self.is_connected()) or (not self.is_logged_in()):
            return False
        if item in self.pwd['notes']:
            return self.rename_note(self.pwd['notes'][item], new_item_name) 
        elif item in self.pwd['subdirs']:
            return self.rename_directory(self.pwd['subdirs'][item], new_item_name) 
        else:
            print("[!] No such note or directory exists in present location.")
            return False

    # Directory Methods
    #
    # These methods all assume that the local copy of the pwd is a true representation
    # of it's state on the server. This of course need not be the case. I should implement
    # a method to check for existence etc. before attempting an action as well as adding
    # code on the server side to prevent the users doing impossible or unauthorized actions.

    def mkdir(self, dir_name):
        """ Create a new directory in the present working directory. """
        if (not self.is_connected()) or (not self.is_logged_in()):
            return False
        if (not dir_name in self.pwd['subdirs']) and (not dir_name in self.pwd['users']): 
            # priv check here
            return self.net.mkdir(dir_name, self.pwd['_id'])
        else:
            print("[!] Directory already exists in present location.")
            return False
    
    def print_pwd(self):
        """ Print the present working directory. """
        if self.is_connected():
            print(self.pwd['dir_name'])
            return True
        else:
            return False

    def ls(self):
        """ Print a list of all the notes and directories in the present 
            working directory, along with details, in alphabetical order."""
        # just going to write a very simple implementation without any of the
        # algorithmic foibles for now.
        if (not self.is_connected()) or (not self.is_logged_in()):
            return False
        print('')
        print("Notes")
        print("--------------------")
        for note in self.pwd['notes'].values():
            print(note)
        print('')
        print("Directories")
        print("--------------------")
        for subdir in self.pwd['subdirs'].items():
            print(subdir[0],'\t',subdir[1])
        print('')
        return True
    

    def cd(self, dir_name):
        """ Move to another directory. """
        if (not self.is_connected()) or (not self.is_logged_in()):
            return False
        # priv check here?
        if  dir_name == "..":
            new_dir = self.net.get_dir(self.pwd['parent_id'])
        elif dir_name in self.pwd['subdirs']:
            new_dir = self.net.get_dir(self.pwd['subdirs'][dir_name])
        elif dir_name in self.pwd['notes']:
            print(f"[!] {dir_name} is not a directory.")
            return False
        else:
            print("[!] No such directory exists in present location.")
            return False
        if new_dir:
            self.pwd = new_dir
            return True
        else:
            print(f"[!] Could not change directory to {dir_name}.")
            return False

    def rename_dir(self, dir_id, new_dir_name):
        """ Update the name of a directory. """
        if (not self.is_connected()) or (not self.is_logged_in()):
            return False
        # priv check here
        return self.net.rename_dir(dir_id, new_dir_name)

    
    def rm_dir(self, dir_id, recursive=False):
        # I was drunk when I wrote this this please review with great care
        # Recursive potion is UNTESTED
        # check priv
        # existence check
        _dir = self.net.get_dir(dir_id)
        if recursive and (not _dir['subdirs'] == {}):
            # loop over all subdirs make recursive call and if they all return True return True, else False
            # This is a kinda non pythonic way of doing this
            for subdir in _dir['subdirs']:
                if not self.rm_dir(_dir['subdirs'][subdir], recursive=True):
                    return False
            return True
        elif _dir['subdirs'] == {} and _dir['notes'] == {}:
            return self.net.rm_dir(dir_id)
        else:
            print("[!] Directory is not empty.")
            return False

    # Note Methods

    def create_note(self, note_name): 
        """ Create a new note with the specified id and edit. """
        if (not self.is_connected()) or (not self.is_logged_in()):
            return False
        # priv check here
        elif note_name in self.pwd['notes'] or note_name in self.pwd['subdirs']:
            print("[*] A note or directory of the same name already exists at this location.")
            return False
        note_path = self.create_temp()  
        self.edit_local_note(note_path)
        enc_aes_key = self.crypto.rsa_encrypt_str(self.crypto.generate_aes_key())
        note_id = self.net.create_note(note_name, enc_aes_key, self.pwd['_id'])
        if note_id and self.update_note(note_id, note_path, aes_key):
            print(f"[*] Created note {note_name} in {self.pwd['dir_name']}.")
            return True
        else:
            print(f"[!] Could not create note {note_name} in {self.pwd['dir_name']}.")
            return False

    def read_note(self, note_name):
        """ Download a local copy of note decrypt and open in text editor """
        if (not self.is_connected()) or (not self.is_logged_in()):
            return None 
        #check priv
        elif not note_name in self.pwd['notes']:
            print(f"[*] No note of this name exist at current location.")
            return None
        note_path = self.get_note(self.pwd['notes'][note_name])
        if note_path:
            with open(note_path, 'w') as note_fd:
                note_fd.write(note)
            os.system(f"{self.config.text_editor} {note_path}")
            print(f"[*] Read note {note_name}.")
            return note_path, aes_key 
        else:
            print(f"[!] Could not get note {note_name} from server.")
            return None 
    
    def edit_note(self, note_id):
        """ Read a file with read() and then send any updates back to the server. """
        if (not self.is_connected()) or (not self.is_logged_in()):
            return False
        # priv check here
        elif not note_id in self.pwd['notes']:
            print(f"[*] No note of this name exist at current location.")
            return False
        note_path, aes_key = self.read(note_id)
        if self.update_note(note_path, aes_key):
            print(f"[*] Note '{note_id}' was successfully updated.")
            return True
        else:
            print(f"[*] Note '{note_id}' could not be updated.")
            return False 

    # save this till later, not very important 
    def rename_note(self, note_id, new_note_name):
        """ Change the name of a note stored on the server. """
        if (not self.is_connected()) or (not self.is_logged_in()):
            return False
        pass

    def rm_note(self, note_name):
        """ Delete a specified note on the server. """
        if (not self.is_connected()) or (not self.is_logged_in()):
            return False
        # check priv
        elif not note_name in self.pwd['notes']:
            print(f"[*] No note of this name exist at current location.")
            return False
        elif self.net.rm_note(self.pwd['notes'][note_name]):
            print("[*] Note {note_name} deleted.")
            return True
        else:
            print("[!] Could not delete note {note_name}.")
    
    def get_note(self, note_id):
        """ Get note from server, decrypt and save in temp file. """
        cipher, enc_aes_key, iv = self.net.get_note(note_id)
        if cipher and enc_aes_key and iv:
            aes_key = self.crypto.rsa_decrypt_str(enc_aes_key)
            note = self.crypto.aes_decrypt(cipher, aes_key, iv)
            note_path = self.create_temp()
            with open(note_path, 'w') as note_fd:
                note_fd.write(note)
            return note_path
        else:
            return None


    def edit_local_note(self, note_path):
        """ Open local copy of a note in the system text editor. """
        os.system(f'{self.config.text_editor} {note_path}]')
        

    def update_note(note_id, note_path, aes_key):
        """ Encrypt note using AES and send to server. """
        with open(note_path, 'r') as note_fd:
            note =  note_fd.read()
        cipher, iv = self.crypto.aes_encrypt_str(note, aes_key)
        if self.net.update_note(note_id, cipher, iv):
            print(f"[*] Note was saved to server with id {note_id}.")
            return True
        else:
            print(f"[!] Failed to save note to server.")
            return False

    def create_temp(self):
        """ Create a temporary file in the systems /tmp directory """
        temp_path = subprocess.run(['mktemp'], stdout=subprocess.PIPE).stdout
        return temp_path


if __name__ == "__main__":
    signal.signal(signal.SIGINT, lambda signum, stack : exit(1))
    term = Terminal("127.0.0.1")
    term.commandLine()

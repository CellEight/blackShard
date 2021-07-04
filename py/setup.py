# Inputs
#    - Server Ip
#    - Server Port 
#    - Mongodb Ip
#    - Mongodb port 
#    - Sever Header
# Process
#    - Get server details from user
#    - Create admin key
#    - Check if keydict exists and if it does load it and add new key to key dict other wise create and do the same
#    - Ask user for mongodb details
#    - check if mongodb is running and start if not
#    - connect to mongodb 
#    - create new db with name blackshard-<32 byte token>
#    - create admin account using generated public key
#    - create root dir
#    - ask user for remianing details required to set up config file
# Ouputs
#    - Properly configured mongo db database
#    - Server config file
#    - Local key dict in ./.config/blackShard
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from os import mkdir
from os.path import isfile, isdir, expanduser
import secrets
import pickle
import pymongo
import yaml
import re
# a couple of useful functions...
def choice(question, choices):
    selection = None 
    while selection not in choices:
        selection = input(f"[?] {question} [{','.join(choices)}]: ").lower()
    return selection

def is_valid_ip(addr):
    """ Check using a regex that the supplied string is a valid ip address """
    ip_exp = "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
    if re.match(ip_exp,addr):
        return True
    else:
        return False

# Print Vanity Header
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
print(buff,'')
# Get server details
print('-------------------------------------------------------------------------')
print('-------------------------->Basic Server Config<--------------------------')
print('-------------------------------------------------------------------------\n')
# IP
server_ip = ''
while not is_valid_ip(server_ip):
    server_ip = input('> Please Enter IP address for server to listen on: ')
    if not is_valid_ip(server_ip):
        print('[!] Not a valid IPV4 address, try again.')
# Port
server_port = 0
while not server_port in range(1,65536):
    try:
        server_port = input('> Please Enter port for server to listen on: [Default:1729] ')
        server_port = int(server_port)
    except ValueError as e:
        if server_port == '':
            server_port = 1729
        else:
            print('[!] That is not a number.')
    if not server_port in range(65536):
        print('[!] Not a valid port (must be a number between 1 and 65535), try again.')
print('')
# Generate Key and configure database
print('-------------------------------------------------------------------------')
print('------------------------->Database Configuration<------------------------')
print('-------------------------------------------------------------------------\n')
# IP
db_ip= ''
while not is_valid_ip(db_ip):
    db_ip = input('> Please Enter IP address mongodb server is listening on: ')
    if not is_valid_ip(db_ip):
        print('[!] Not a valid IPV4 address, try again.')
# Port
db_port = 0
while not db_port in range(1,65536):
    try:
        db_port = input('> Please Enter port mongodb is listening on to listen on: [Default:27017] ')
        db_port = int(db_port)
    except ValueError as e:
        if db_port == '':
            db_port = 27017
        else:
            print('[!] That is not a number.')
    if not db_port in range(65536) and db_port:
        print('[!] Not a valid port (must be a number between 1 and 65535), try again.')
# Get mongodb creds from user
db_user = input("> Please enter username of mongodb admin: [Leave Blank if no authentication] ")
db_password = ""
if db_user:
    db_password = input("> Please enter password: ") 
# Attempt to connect to server and error out here if a connection cannot be established
print('Attempting to connect to Database')
if db_user:
    client = pymongo.MongoClient(f"mongodb://{db_user}:{db_password}@{db_ip}:{db_port}/?authSource=admin")
else:
    client = pymongo.MongoClient(f"mongodb://{db_ip}:{db_port}/?authSource=admin")
try:
    client.server_info()
except pymongo.errors.ServerSelectionTimeoutError as e:
    print('[!] Could not connect to mongodb.')
    exit(1)
print('Connection established!')
# Generate key pair
print('Generating admin key pair. Be patient this could take a sec...')
keypair = RSA.generate(4096)
print('Done!')
# Create new database and set up admin and root
print('Setting up the database....')
db_name = "blackshard-" + secrets.token_hex(16)
while db_name in client.list_database_names():
    db_name = "blackshard-" + secrets.token_hex(16)
db = client.get_database(db_name)
print('Creating admin user account...')
admin = {"username":'admin', "public_key":keypair.publickey().export_key().decode('ascii')}
result = db.users.insert_one(admin)
print('Creating root directory...')
root = {"dir_name":'/',"parent_id":None,"subdirs":{},"notes":{},"owners":['admin'],"users":[]}
result = db.dirs.insert_one(root)
print('Done! That\'s the database all setup.')
print('')
# Save private key to key store and get basic config from user
print('-------------------------------------------------------------------------')
print('-------------------------->Local Configuration<--------------------------')
print('-------------------------------------------------------------------------\n')
# Attempt to create or add to key_db
print('Checking for pre-existing key_db.pkl file in ~/.config/blackshard')
if isfile('~/.config/blackshard/key_db.pkl'):
    print('Key-chain found! Using that one.')
    with open(expanduser("~/.config/blackshard"),'rb') as key_db_fd:
        key_db = pickle.load(key_db_fd)
else:
    print('No key-chain found. Creating one now...')
    if not isdir(expanduser("~/.config")):
        mkdir(expanduser("~/.config"))
    if not isdir(expanduser("~/.config/blackshard")):
        mkdir(expanduser("~/.config/blackshard"))
    key_db = {}
key_id = f'{server_ip}-admin'
if key_id in key_db:
        if choice("[~] A key already exists for this user. Overwrite?", {"y", "n"}) == "n":
            print("[!] Aborting")
            # drop newly created db
            print('Deleting created database {db_name}.')
            client.drop_database(db_name)
            exit(1)
key_db[key_id] = keypair.export_key().decode('ascii')
with open(expanduser("~/.config/blackshard/key_db.pkl"),'wb') as key_db_fd:
    pickle.dump(key_db,key_db_fd)
# Ask for any config options from the user
print('Key-chain saved.')
print('Generating config file...')
with open(expanduser("~/.config/blackshard/bs_server_conf.yaml"),'w') as config_fd:
    # author config
    config = {'server_ip':server_ip,'server_port':server_port,
              'db_ip':db_ip,'db_port':db_port,'db_user':db_user,
              'db_password':db_password,'db_name':db_name,'header':f'Welcome to {db_name}!'}
    yaml.dump(config, config_fd)
print('All done! Just Fire up the server and you\'re good to go...')

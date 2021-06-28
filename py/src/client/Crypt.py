from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import pickle
from os.path import isfile
from Util import choice

class Crypt():
    """ Crypt handles all application layer encryption for blackShard. """
    def __init__(self, password, key_db_location="./key_db.pkl"):
        self.current_keypair = None
        self.key_len = 4096
        self.key_db_location = key_db_location 
        self.load_key_db(password)

    def create_key_db(self,):
        """ Create a empty key db file """
        self.key_db = {}
        self.save_key_db()

    def load_key_db(self, password):
        """ Load the encrypted pickle file containing a serialized python 
            dictionary of 2-tuples of RSA key-pairs and associated sever labled by key id"""
        if not isfile(self.key_db_location):
            self.create_key_db()
        # exception handling needed
        # add some form of encryption
        with open(self.key_db_location, 'rb') as key_db_file:
            self.key_db = pickle.load(key_db_file)
        
    def save_key_db(self):
        """ Save the current key_db as a serialized pickle object """
        # exception handling needed
        # add some form of encryption
        with open(self.key_db_location, 'wb') as key_db_file:
            pickle.dump(self.key_db, key_db_file)


    def generate_keypair(self, server_ip, user): 
        """ Creates a new key pair and returns the new key_id of the generated pair """
        # is the source of entropy here solid?
        keypair = RSA.generate(self.key_len)
        key_id = f'{server_ip}-{user}'
        if key_id in self.key_db:
            if choice("[~] A key already exists for this user. Overwrite?", {"y", "n"}) == "n":
                print("[!] Aborting")
                return False
        if self.add_keypair_to_db(key_id,  keypair):
            print("[*] New keypair generated.")
            self.load_keypair(server_ip,user)
            return True
        else:
            print("[!] Could not add keypair to db.")
            return False

    def load_keypair(self, server_ip, user):
        """ Attempts to load the key pair for the specified user on the specified server, 
            returns true if key found and loaded successfully, and false if it is not """
        try:
            keypair = RSA.importKey(self.key_db[f'{server_ip}-{user}'])
            print(f"[*] Key-Pair {server_ip}-{user} active.")
        except Exception as e:
            # Clean up error handling here
            print("[!] Could not load key. ")
            print(e)
            return False
        self.current_keypair = keypair
        return True

    def encrypt(self, text):
        """ Encrypt text using current RSA keypair """
        text = text.encode('utf-8')
        encryptor = PKCS1_OAEP.new(self.current_keypair.publickey())
        cipher = binascii.hexlify(encryptor.encrypt(text)).decode('ascii') # might wish to keep as bytes
        return cipher

    def decrypt(self, cipher):
        """ Decrypt cipher text using the current RSA keypair """
        print(cipher)
        print(len(cipher))
        cipher = cipher.encode('ascii')
        decryptor = PKCS1_OAEP.new(self.current_keypair)
        text = decryptor.decrypt(cipher)
        return text.decode('ascii')

    def decrypt_bytes(self, cipher):
        """ Decrypt cipher text using the current RSA keypair """
        print(cipher)
        print(len(cipher))
        cipher = cipher
        decryptor = PKCS1_OAEP.new(self.current_keypair)
        text = decryptor.decrypt(cipher)
        return text

    def add_keypair_to_db(self, key_id, key):
        """ Adds a key to the db """
        # add some more error handling
        self.key_db[key_id] = key.exportKey('PEM').decode('ascii')
        self.save_key_db()
        return True

    def delete_keypair(self, key_id):
        """ Remove the keypair with the specified id form the key_db. """
        if key_id in self.key_db:
            del self.key_db[key_id]
            self.save_key_db()
            print("[*] Key-Pair {key_id} deleted.")
            return True
        else:
            print("[!] Key-Pair '{key_id}' does not exist.")

    def export_keypair(self, key_id, location):
        """ Write specified public-private key pair to file in standard format """
        # maybe think about some exception handling here
        with open(Path(location)/f"{key_id}.pub", 'w') as pub:
            pub.write(self.key_db[key_id].publickey().exportKey().decode('ascii'))
            print(f"[*] Public Key saved at '{Path(location)}/{key-id}.pub'")
        with open(Path(location)/f"{key_id}.priv", 'w') as priv:
            priv.write(self.key_db[key_id].exportKey().decode('ascii'))
            print(f"[*] Private Key saved at '{Path(location)}/{key-id}.priv'")
         
    def import_keypair(self, keypair_location):
        """ Read public private key pair from file in standard format and add to db """
        pass

    def list_keypairs(self,):
        """ Print out a list of keypairs in the key_db """
        print("\t Server IP   User ")
        print("\t------------------")
        for key_id in self.key_db:
            ip, user = key_id.split('-',1)
            print(f"\t{ip} , {user}")

#    def retrive_keypair(self, key_id):
#        pass


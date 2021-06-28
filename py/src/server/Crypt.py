from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import pickle
import secrets
import string

class Crypt():
    """ Crypt handles all application layer encryption for blackShard. """
    def __init__(self, key_db_location=None, key_len=4096):
        self.current_key = None
        # Probably should have the server communicate the choice of key length to the client
        self.key_len = key_len 

    def load_user_public_key(self, user):
        self.current_key = RSA.importKey(user['public_key'].encode('ascii'))

    def encrypt(self, text):
        """ Encrypt text using current RSA keypair """
        if type(text) == str:
            text = text.encode('ascii')
            print("[*] Sending ASCII.")
        else:
            print("[*] Sending Bytes.")
        print(repr(self.current_key))
        encryptor = PKCS1_OAEP.new(self.current_key)
        cipher = binascii.hexlify(encryptor.encrypt(text)).decode('ascii') # might wish to keep as bytes
        return cipher

    def encrypt_bytes(self, text):
        """ Encrypt text using current RSA keypair """
        if type(text) == str:
            text = text.encode('ascii')
            print("[*] Sending ASCII.")
        else:
            print("[*] Sending Bytes.")
        print(repr(self.current_key))
        encryptor = PKCS1_OAEP.new(self.current_key)
        cipher = encryptor.encrypt(text)
        return cipher

    def generate_login_cipher(self):
        """ Generates a cryptographically secure 4096 character alphanumeric 
            string as a challenge, encodes it using the current public key and 
            returns the plain and cipher text to the calling function """
        # Add error check for the case that the current key is not set!
        # Okay so I have to use 470 bytes for the challenge as for some strange
        # reason the Crypto library only lets you encrypt strings of length 
        # n - "hash length"/2. It doesn't tell you what the hash length is
        # or how to find it. Not even stated in the RFC they use.
        # could probably have found it somewhere in the morass of their code base
        # but in the end just brute forced. It was 84 so "hash length"/2 is 42.
        # Go figure.
        # Fuck I hate this brain dead library.
        chalange =  secrets.randbits(170*8).to_bytes(170,byteorder='big')
        cipher = self.encrypt_bytes(chalange)
        print(len(cipher))
        return chalange, cipher 

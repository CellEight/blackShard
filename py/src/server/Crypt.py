from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import pickle

class Crypt():
    """ Crypt handles all application layer encryption for blackShard. """
    def __init__(self, key_db_location=None):
        self.current_key = None
        self.key_len = 4096

    def load_user_public_key(self, user):
        self.current_key = user['public_key']

    def encrypt(self, text):
        """ Encrypt text using current RSA keypair """
        text = text.encode('utf-8')
        encryptor = PKCS1_OAEP.new(self.current_keypair.publickey())
        cipher = binascii.hexlify(encryptor.encrypt(text)).decode('ascii') # might wish to keep as bytes

    def generate_login_cipher(self):
        pass

    def valdiate_login_cipher_data(self, data):
        pass

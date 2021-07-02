import datetime
from pymongo import MongoClient
from bson import ObjectId
# URGENT: Need to implement permissions and prevent non empty directory deletion
# as well as recursive delete. Want to focus on getting basics working but will come
# back to this.
# Less urgent: Add some docstrings

class Database():
    def __init__(self, ip="127.0.0.1", port=27017):
        self.connect_to_db(ip, port)

    def connect_to_db(self, ip, port):
        self.client = MongoClient(ip, port)
        self.db = self.client.blackShard
        self.users = self.db.users
        self.dirs = self.db.dirs
        self.notes = self.db.notes

    # User Management Methods 
    
    def create_user(self,username,public_key):
        user = {"username":username, "public_key":public_key}
        try:
            self.users.insert_one(user)
            print("[*] Created user.")
            return user
        except Exception as e:
            print(e)
            print("[!] Failed to create user.")
            return None

    def get_user(self, username):
        """ Queries the database for a given user. Returns user object 
            if user exists or None if they do not. """
        return self.users.find_one({"username":username})

    def delete_user(self, username):
        """ Ask the database to delete the with the specified username."""
        try:
            self.users.delete_one({'username':username})
            print(f"[*] Deleted User {username}.")
            return True
        except Exception as e:
            print(e)
            print(f"[!] Failed to delete user {username}.")
            return False

    # Note Management Methods

    def create_note(self, note_name, enc_aes_key, dir_id, username):
        """ Created a new empty note with the creators encrypted aes key stored within. """
        now  = datetime.datetime.utcnow()
        note = {"note_name":note_name,"dir_id":dir_id,"enc_aes_keys":{username:enc_aes_key},"iv":"","cipher":"","created":now,"last_updated":now} 
        try:
            # add more verification of success
            note_id = str(self.notes.insert_one(note).inserted_id)
            self.dirs.update_one({'_id':dir_id}, {'$set':{'notes.'+note_name:note_id}})
            return note_id
        except Exception as e:
            print(e)
            return None

    def get_note(self, note_id):
        """ Queries the database for a given note. Returns note dictionary
            if note exists or None if it does not."""
        return self.notes.find_one({"_id":note_id})

    def update_note(self, note_id, cipher, iv):
        """ Update the cipher text, iv and timestamp of the specified note. """
        now  = datetime.datetime.utcnow()
        try:
            # maybe get the returned object here to see if it really worked?
            self.notes.update_one({'_id':note_id}, {'$set':{'cipher':cipher, 'iv':iv, 'last_updated':now}})
            return True
        except Exception as e:
            print(e)
            return False
    
    def rename_note(self, note_id, new_note_name):
        """ Instruct the database to change the note_name field of a note. """
        try:
            note = self.get_note(note_id)
            result_1 = self.notes.update_one({'_id':note_id},{'$set':{'note_name':new_note_name}})
            result_2 = self.dirs.update_one({'_id':note['dir_id']},{'$unset':{'notes.'+note['note_name']:''}})
            result_2 = self.dirs.update_one({'_id':note['dir_id']},{'$set':{'notes.'+new_note_name:str(note['_id'])}})
            return True
        except Exception as e:
            print(e)
            print(f"[!] Failed to rename note {note_id}. The database may have been corrupted.")
            return False

    def rm_note(self, note_id):
        """ Delete the specified note form database """
        try:
            note = self.get_note(note_id)
            result_1 = self.dirs.update_one({'_id':note['dir_id']},{'$unset':{'notes.'+note['note_name']:''}})
            result_2 = self.notes.delete_one({'_id':note_id})
            print("Dir update: ",result_1.modified_count)
            print("Delted: ",result_2.deleted_count)
            print(f"[*] Deleted note {note_id}.")
            return True
        except Exception as e:
            print(e)
            print("[!] Failed to delete note {note_id}.")
            return False

    # Directory Management Methods
    
    def mkdir(self, dir_name, parent_id, user_id):
        # should owners/users be lists or a dicts
        new_dir = {"dir_name":dir_name,"parent_id":str(parent_id),"subdirs":{},"notes":{},"owners":[str(user_id)],"users":[]}
        try:
            new_dir_id = self.dirs.insert_one(new_dir).inserted_id
            self.dirs.update_one({'_id':parent_id}, {'$set':{'subdirs.'+dir_name:str(new_dir_id)}})
            print("[*] Created directory.")
            return True
        except Exception as e:
            print(e)
            print("[!] Failed to create directory.")
            return False

    def get_dir(self, dir_id):
        """ Queries the database for a given directory. Returns directory dictionary 
            if directory exists or None if it does not."""
        _dir = self.dirs.find_one({"_id":dir_id})
        if _dir:
            print(f"[*] Got directory {_dir['dir_name']} from database.")
            return _dir
        else:
            print(f"[*] Could not get directory with id {dir_id}, from database.")
            return None

    def get_init_pwd_id(self):
        """ Get the id of the root directory of the servers file structure. """
        init_pwd = self.dirs.find_one({"dir_name":"/"})
        if init_pwd:
            print("[*] Got init pwd.")
            return init_pwd['_id']
        else:
            print("[!] Oh dear! You don't seem to have a root directory. Did you set up the Database?")
            return None
    
    def rename_dir(self, dir_id, new_dir_name):
        """ Instruct the database to change the dir_name field of a directory. """
        try:
            _dir = self.get_dir(dir_id)
            parent_id = ObjectId(_dir['parent_id'])
            result_1 = self.dirs.update_one({'_id':dir_id},{'$set':{'dir_name':new_dir_name}})
            result_2 = self.dirs.update_one({'_id':parent_id},{'$unset':{'subdirs.'+_dir['dir_name']:''}})
            result_2 = self.dirs.update_one({'_id':parent_id},{'$set':{'subdirs.'+new_dir_name:str(_dir['_id'])}})
            return True
        except Exception as e:
            print(e)
            print("[!] Failed to rename directory {dir_id}. The database may have been corrupted.")
            return False


    def rm_dir(self, dir_id):
        try:
            #might need to look at the returned object here to verify success?
            _dir = self.get_dir(dir_id)
            if not _dir:
                print("[!] Could not retrieve directory for deletion.")
                return False
            parent_id = ObjectId(_dir['parent_id'])
            result_1 = self.dirs.update_one({'_id':parent_id},{'$unset':{'subdirs.'+_dir['dir_name']:''}})
            result_2 = self.dirs.delete_one({'_id':dir_id})
            print(result_1)
            print(result_2)
            print(f"[*] Deleted directory {dir_id}.")
            return True
        except Exception as e:
            print(e)
            print("[!] Failed to delete directory {dir_id}.")
            return False

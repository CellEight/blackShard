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

    # Crud for user, note and location objects
    
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

    def create_note(self, note_name ,note_content, dir_id):
        now  = datetime.datetime.utcnow()
        note = {"note_name":note_name,"note_content":note_content,"dir_id":dir_id,"created":now,"last_updated":now} 
        try:
            self.notes.insert_one(note)
            print("[*] Created note.")
            return True
        except Exception as e:
            print(e)
            print("[!] Failed to create note.")
            return False
    
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

    def get_user(self, username):
        """ Queries the database for a given user. Returns user object 
            if user exists or None if they do not. """
        return self.users.find_one({"username":username})

    def get_note(self, note_id):
        """ Queries the database for a given note. Returns note dictionary
            if note exists or None if it does not."""
        return self.notes.find_one({"_id":note_id})

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

    def delete_user(self, username):
        try:
            self.users.delete_one({'username':username})
            print(f"[*] Deleted User {username}.")
            return True
        except Exception as e:
            print(e)
            print(f"[!] Failed to delete user {username}.")
            return False

    def delete_note(self, note_id):
        try:
            self.notes.delete_one(note_id)
            print(f"[*] Deleted note {note_id}.")
            return True
        except Exception as e:
            print(e)
            print("[!] Failed to delete note {note_id}.")
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

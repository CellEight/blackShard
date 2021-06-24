from pymongo import MongoClient
# URGENT: Need to implement permissions and prevent non empty directory deletion
# as well as recursive delete. Want to focus on getting basics working but will come
# back to this.
# Less urgent: Add some docstrings

class Database():
    def __init__(self, ip="127.0.0.1", port=27017):
        connect_to_db(ip, port)

    def connect_to_db(self):
        self.client = MongoClient(ip, port)
        self.db = self.client.blackShard
        self.users = self.db.users
        self.dir = self.db.dir
        self.notes = self.db.notes

    # Crud for user, note and location objects
    
    def create_user(self,username,public_key):
        user = {"username":username, "public_key":public_key}
        try:
            self.users.insert_one(post)
            print("[*] Created user.")
            return user
        except Exception e:
            print("[!] Failed to create user.")
            return None

    def create_note(self, note_name ,note_content, dir_id):
        now  = datetime.datetime.utcnow()
        note = {"note_name":note_name"note_content":note_content,"dir_id":dir_id,"created":now,"last_updated":now} 
        try:
            self.notes.insert_one(note)
            print("[*] Created note.")
            return True
        except Exception e:
            print("[!] Failed to create note.")
            return False
    
    def create_dir(self, dir_name, parent_dir_id):
        _dir = {"dir_name":dir_name,"parent_dir_id":parent_dir_id,"children_ids":{}}
        try:
            self.dir.insert_one(_dir)
            print("[*] Created directory.")
            return True
        except Exception e:
            print("[!] Failed to create directory.")
            return False

    def get_user(self, username):
        """ Queries the database for a given user. Returns user object 
            if user exists or None if they do not. """
        return self.users.findOne({"username":username})

    def get_note(self, note_id):
        """ Queries the database for a given note. Returns note dictionary
            if note exists or None if it does not."""
        return self.notes.findOne({"_id":note_id})

    def get_dir(self, dir_id):
        """ Queries the database for a given directory. Returns directory dictionary 
            if directory exists or None if it does not."""
        return self.dir.findOne({"_id":dir_id})

    def delete_user(self, user_id):
        try:
            self.users.delete_one(user_id)
            print(f"[*] Deleted User {user_id}.")
            return True
        except Exception e:
            print(f"[!] Failed to delete user {user_id}.")
            return False

    def delete_note(self, note_id):
        try:
            self.notes.delete_one(note_id)
            print(f"[*] Deleted note {note_id}.")
            return True
        except Exception e:
            print("[!] Failed to delete note {note_id}.")
            return False

    def delete_dir(self, dir_id):
        try:
            self.dir.delete_one(dir_id)
            print(f"[*] Deleted directory {dir_id}.")
            return True
        except Exception e:
            print("[!] Failed to delete directory {dir_id}.")
            return False

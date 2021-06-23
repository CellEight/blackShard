class Database():
    def __init__(self):
        pass

    def db_connect(self):
        pass

    def db_request(self):
        pass
    
    # Crud for user, note and location objects

    def get_user(self, username):
        """ Queries the database for a given user. Returns User object 
            if user exists or None if they do not. """
        pass

    def get_note(self):
        pass

    def get_location(self):
        pass

    def create_note(self):
        pass
    
    def create_location(self):
        pass

    def create_user(self):
        pass

    def delete_note(self):
        pass

    def delete_location(self):
        pass

    def delete_user(self):
        pass

class User():
    def __init__(self, user_json):
        self.username = ""
        self.public_key = ""
        self.populate_fields(user_json)

    def populate_fields(self, user_json):
        """ Parses json object retrieved from database and uses result 
            to populate the fields of class """
        pass

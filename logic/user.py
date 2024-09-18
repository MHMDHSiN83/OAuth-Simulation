class User:
    def __init__(self, username, password, email, phone=None, name=None):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.name = name

    @staticmethod
    def authenticate(users_db, username, password):
        user = users_db.get(username)
        if user and user.password == password:
            return user
        return None

    def get_email(self):
        return self.email

    def get_phone(self):
        return self.phone
    
    def get_name(self):
        return self.name
    
    def set_phone(self, phone):
        self.phone = phone
    
    def set_name(self, name):
        self.name = name

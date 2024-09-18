import requests

from user import User

class Client:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.logged_user = None
        self.users = [
            User(username="user1", password="password1", email="user1@example.com"),
            User(username="user2", password="password2", email="user2@example.com")
        ]

    def get_client_id(self):
        return self.client_id

    def get_redirect_uri(self):
        return self.redirect_uri
    
    def get_logged_user(self):
        return self.logged_user

    def get_token(self, code, scope):
        response = requests.post(
            'http://localhost:5000/token',
            data={
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'code': code,
                'scope': scope
            }
        )
        return response.json()

    def get_user_info(self, access_token, scope):
        response = requests.post(
            'http://localhost:5000/user_info',
            headers={'Authorization': f'Bearer {access_token}'},
            data={'scope': scope}
        )
        return response.json()

    def login(self, email):
        for i in self.users:
            if(i.get_email() == email):
                self.logged_user = i

    def set_name_and_phone(self, name, phone):
        self.logged_user.set_name(name)
        self.logged_user.set_phone(phone)

    def logout(self):
        self.logged_user = None

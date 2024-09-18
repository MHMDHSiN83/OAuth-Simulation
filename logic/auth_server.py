import uuid
from datetime import datetime, timedelta
from user import User

class AuthServer:

    # Simulated databases
    clients = {
        "client_id_123": {
            "client_secret": "secret_abc",
            "redirect_uri": "http://localhost:5001/callback"
        }
    }
    users = {
        "09102713631": User(username="user1", password="12345", email="user1@example.com", phone="09102713631", name="محمدحسین"),
        "9876543210": User(username="user2", password="54321", email="user2@example.com", phone="9876543210", name="رضا")
    }
    scopes = {
        'online_shopping' : ['email', 'phone', 'name'],
        'online_news' : ['phone'],
    }

    authorization_codes = {}
    access_tokens = {}
    token_expiry_times = {}
    authorization_code_to_user = {}

    @classmethod
    def issue_authorization_code(cls, client_id, username):
        auth_code = str(uuid.uuid4())
        cls.authorization_codes[auth_code] = client_id
        cls.authorization_code_to_user[auth_code] = username
        return auth_code

    @classmethod
    def validate_client(cls, client_id, client_secret):
        client = cls.clients.get(client_id)
        return client and client['client_secret'] == client_secret

    @classmethod
    def validate_authorization_code(cls, code, client_id):
        return code in cls.authorization_codes and cls.authorization_codes[code] == client_id

    @classmethod
    def generate_access_token(cls, auth_code, expires_in=3600):
        access_token = str(uuid.uuid4())
        username = cls.authorization_code_to_user.get(auth_code)
        if username:
            cls.access_tokens[access_token] = username
            cls.token_expiry_times[access_token] = datetime.utcnow() + timedelta(seconds=expires_in)
        return access_token

    @classmethod
    def validate_access_token(cls, access_token):
        if access_token in cls.token_expiry_times:
            if datetime.utcnow() < cls.token_expiry_times[access_token]:
                return True
            else:
                # Token has expired
                del cls.access_tokens[access_token]
                del cls.token_expiry_times[access_token]
        return False

    @classmethod
    def get_username_from_token(cls, access_token):
        if cls.validate_access_token(access_token):
            return cls.access_tokens.get(access_token)
        return None

    @classmethod
    def authenticate_user(cls, username, password):
        user = cls.users.get(username)
        return user if user and user.password == password else None
    
    def get_user_data(cls, user, scope):
        user_info = {}
        if scope in cls.scopes:
            for i in cls.scopes[scope]:
                if(i == 'email'):
                    user_info['email'] = user.get_email()
                if(i == 'name'):
                    user_info['name'] = user.get_name()
                if(i == 'phone'):
                    user_info['phone'] = user.get_phone()      
        return user_info
            

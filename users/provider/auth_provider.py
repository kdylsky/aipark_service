import re
import jwt
import bcrypt
from datetime           import datetime

from django.conf        import settings

from users.exceptions   import FormatEmailError, FormatPasswordError
from users.models       import User

class AuthProvider:
    def __init__(self)-> None:
        self.key        = settings.JWT_KEY
        self.expire_sec = settings.JWT_EXPIRE_TIME
    
    def hashpw(self, password: str)-> str:
        password = password.encode("utf8")
        hashed   = bcrypt.hashpw(password, bcrypt.gensalt())
        return hashed.decode("utf8")

    def check_password(self, password: str, user_password: str)-> bool:
        hash_pw = user_password.encode("utf8")
        return bcrypt.checkpw(password.encode("utf8"), hash_pw)

    def create_token(self, user_id: int, is_expired: bool = False)-> dict:
        exp = 0 if is_expired else self.get_curr_sec() + self.expire_sec
        access_encoded_jwt = jwt.encode(
            {"id": user_id, "exp": exp},
            self.key,
            algorithm="HS256",
        ) 
        return {"access": access_encoded_jwt}

    def get_curr_sec(self):
        return datetime.now().timestamp()

    def check_password_format(self, password: str)-> bool:
        REGEX_PASSWORD = '^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$'
        if not re.match(REGEX_PASSWORD, password):
            raise FormatPasswordError()

    def check_email(self, email: str)-> bool:
        REGEX_EMAIL = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(REGEX_EMAIL, email):
            raise FormatEmailError()

auth_provider = AuthProvider()
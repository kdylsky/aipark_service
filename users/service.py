from users.models import User
from users.repository import SignUpRepo
from users.exceptions import CheckPasswordError, UserDoesNotError
from users.provider.auth_provider import auth_provider

class SignService:
    def __init__(self):
        self.signup_repo = SignUpRepo()
    
    def create(self, email: str, password: str)-> dict:
        auth_provider.check_email(email)
        auth_provider.check_password_format(password)
        password = auth_provider.hashpw(password)
        create_user =self.signup_repo.create(
            email       = email,
            password    = password,
        )
        return create_user

class LoginService:
    def login(self, email: str, password: str)-> str:
        try:
            user = User.objects.get(email=email)    
            if not auth_provider.check_password(password, user.password):
                raise CheckPasswordError()
            token = auth_provider.create_token(user.id)
            return token
        except User.DoesNotExist:
            raise UserDoesNotError()
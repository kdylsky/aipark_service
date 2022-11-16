from users.models       import User
from users.serializers  import SignUpSchema

class SignUpRepo():
    def __init__(self):
        self.model      = User
        self.serializer = SignUpSchema

    def create(self, email, password):
        serializer = self.serializer(
            data={
                "email":email,
                "password":password
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data
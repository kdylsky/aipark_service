from rest_framework import status

class CustomBaseExecption(Exception):
    is_custom_execption = True


class NotAuthorizedError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Login Required"
        self.status = status.HTTP_403_FORBIDDEN

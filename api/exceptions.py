from rest_framework import status
from exceptions     import CustomBaseExecption

class NotFoundObject(CustomBaseExecption):
    def __init__(self):
        self.msg = "DoesNotFoundObject"
        self.status = status.HTTP_400_BAD_REQUEST
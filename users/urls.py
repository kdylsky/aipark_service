from django.urls import path
from users.views import SingUpAPI, LoginAPI

urlpatterns = [
    path("/signup", SingUpAPI.as_view()),
    path("/login", LoginAPI.as_view()),
]
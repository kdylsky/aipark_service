from django.urls import path
from api.views import AiParkAPI

urlpatterns = [
    path('/test', AiParkAPI.as_view()),
]

from django.urls import path
from api.views import AiParkView, AddionAiParkView

urlpatterns = [
    path('/project', AiParkView.as_view()),
    path('/project/<int:project_id>', AiParkView.as_view()),
    path('/project/<int:project_id>/index/<int:index>', AddionAiParkView.as_view()),
]

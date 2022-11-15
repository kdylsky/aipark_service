from django.urls import path
from api.views import AiParkView, TextUpdateView

urlpatterns = [
    path('/project', AiParkView.as_view()),
    path('/project/<int:project_id>', AiParkView.as_view()),
    path('/project/<int:project_id>/index/<int:index>', TextUpdateView.as_view()),
]

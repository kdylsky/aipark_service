from django.urls import path
from api.views import AiParkView, TextUpdateView

urlpatterns = [
    path('/test', AiParkView.as_view()),
    path('/test/<int:project_id>', AiParkView.as_view()),
    path('/test/<int:project_id>/<int:index>', TextUpdateView.as_view()),
]

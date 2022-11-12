from django.urls import path
from api.views import AiParkView, TextUpdateView

urlpatterns = [
    path('/test', AiParkView.as_view()),
    path('/test/<int:project_id>', AiParkView.as_view()),
    path('/test/<int:project_id>/<int:text_id>', TextUpdateView.as_view()),
]

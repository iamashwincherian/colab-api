from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProjectView.as_view(), name="projects_view"),
    path('<str:id>', views.GetProject.as_view(), name="get_project"),
]

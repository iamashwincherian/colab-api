from django.urls import path
from . import views

urlpatterns = [
    path('<str:id>', views.GetProject.as_view(), name="get_project"),
    path('', views.GetAllProjects.as_view(), name="get_all_projects"),
]

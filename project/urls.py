from django.urls import path
from . import views

urlpatterns = [
    path('', views.GetAllProjects.as_view(), name="get_all_projects")
]

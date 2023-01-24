from django.urls import path
from . import views

urlpatterns = [
    path('', views.FetchUser.as_view(), name="fetch_user")
]
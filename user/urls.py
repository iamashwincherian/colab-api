from django.urls import path
from . import views

urlpatterns = [
    path('', views.GetUserList.as_view(), name="fetch_user")
]

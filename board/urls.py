from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name="board_view"),
    path('<str:id>/lists', include('list.urls')),
]

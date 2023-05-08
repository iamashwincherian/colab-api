from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.BoardListView.as_view(), name="board_list_view"),
    path('<str:id>', views.BoardDetailView.as_view(), name="board_detail_view"),
]

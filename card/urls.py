from django.urls import path

from . import views

urlpatterns = [
    path('', views.CardListView.as_view(), name='cards_list_view')
]

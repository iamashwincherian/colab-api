"""CollabBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

prepend = 'api'

urlpatterns = [
    path(f'{prepend}/auth/', include('authentication.urls')),
    path(f'{prepend}/users/', include('user.urls')),
    path(f'{prepend}/projects/', include('project.urls')),
    path(f'{prepend}/boards/', include('board.urls')),
    path(f'{prepend}/boards/<str:board_id>/lists/', include('list.urls')),
    path(f'{prepend}/boards/<str:board_id>/lists/<str:list_id>/cards/',
         include('card.urls')),
]

if settings.DEBUG:
    urlpatterns.append(path('admin/', admin.site.urls))

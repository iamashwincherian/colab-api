from rest_framework import generics
from rest_framework.serializers import ModelSerializer

from .serializers import UserSerializer
from .models import User


class GetUserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

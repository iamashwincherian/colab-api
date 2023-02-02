from rest_framework import serializers
from django.contrib.auth import authenticate

from user.serializers import UserSerializer


class GoogleTokenSerializer(serializers.Serializer):
    id_token = serializers.CharField()


class CredentialSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

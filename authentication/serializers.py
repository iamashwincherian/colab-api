from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenObtainSerializer
from rest_framework import serializers
from django.contrib.auth import authenticate

from user.serializers import UserSerializer


class GoogleTokenSerializer(serializers.Serializer):
    id_token = serializers.CharField()


class NewUserTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def check_existing_user(self, email, password):
        user = authenticate(email=email, password=password)
        if user:
            raise serializers.ValidationError("User already exists")
        return False

    def validate(self, data):
        email = data.get("email", "")
        password = data.get("password", "")

        self.check_existing_user(email, password)
        return data

    def serialize_user(self, user):
        serialized_user = UserSerializer(instance=user).data
        token = user.get_token()
        serialized_user["token"] = token
        return serialized_user

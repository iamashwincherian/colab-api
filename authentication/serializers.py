from rest_framework import serializers
from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport import requests


class GoogleTokenSerializer(serializers.Serializer):
    id_token = serializers.CharField()

    def get_user_data(self, token):
        user = verify_oauth2_token(token, requests.Request())
        if not user:
            raise Exception("Google id_token is invalid")
        return user

    def validate(self, attrs):
        super().validate(attrs)
        attrs["user"] = self.get_user_data(attrs['id_token'])
        return attrs


class CredentialSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    first_name = serializers.CharField(allow_blank=False)
    last_name = serializers.CharField(allow_blank=True)

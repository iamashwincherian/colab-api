from rest_framework import views, generics
from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport import requests
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import authenticate

from user.models import User
from user.serializers import UserSerializer


class ValidateGoogleToken(views.APIView):
    serializer_class = None

    def get_google_user(self, token):
        return verify_oauth2_token(token, requests.Request())

    def create_user(self, user):
        new_user = User.objects.create(
            username=user["email"], email=user["email"], first_name=user["name"])
        social_account = SocialAccount(user=new_user, provider="google")
        social_account.uid = user["sub"]
        social_account.save()
        return new_user

    def check_existing_user(self, google_user):
        user = User.objects.filter(email=google_user["email"])
        if not user.exists():
            return False
        return user[0]

    def serialize_user(self, user):
        data = {}
        serialized_user = UserSerializer(instance=user)
        token = user.get_token()
        data["user"] = serialized_user.data
        data["token"] = token
        return data


class Authenticate(generics.GenericAPIView):
    def check_if_user_exists(self, email, password):
        user = User.objects.filter(email=email)
        if not user:
            return False

        user = authenticate(email=email, password=password)
        return user if user else False

    def create_user(self, email, password, first_name="", last_name=""):
        user = User.objects.create_user(
            username=email, email=email, password=password, first_name=first_name, last_name=last_name)
        return user

    def create_social_account(self, user):
        social_account = SocialAccount(user=user, provider="google")
        social_account.uid = user.sub
        social_account.save()

    def get_or_create_user(self, email, password):
        user = self.check_if_user_exists(email, password)
        if (user):
            return user

        new_user = self.create_user(email, password)
        return new_user

    def serialize_user(self, user):
        serialized_user = UserSerializer(instance=user).data
        serialized_user['token'] = user.get_token()
        return serialized_user

from rest_framework import views, generics

from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import authenticate

from user.models import User
from user.serializers import UserSerializer


class Authenticate(generics.GenericAPIView):
    def check_if_user_exists(self, email):
        users = User.objects.filter(email=email)
        if not len(users):
            return False
        return users[0]

    def create_user(self, email, password=None, first_name="", last_name=""):
        user = User.objects.create_user(
            username=email, email=email, password=password, first_name=first_name, last_name=last_name)
        return user

    def create_social_account(self, user, google_user):
        social_account = SocialAccount(user=user, provider="google")
        social_account.uid = google_user["sub"]
        social_account.save()

    def authenticate_user(self, email, password):
        return authenticate(email=email, password=password)

    def serialize_user(self, user):
        serialized_user = UserSerializer(instance=user).data
        serialized_user['token'] = user.get_token()
        return serialized_user

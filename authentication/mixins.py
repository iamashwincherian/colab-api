from rest_framework import views
from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport import requests
from allauth.socialaccount.models import SocialAccount
from rest_framework_simplejwt.tokens import RefreshToken

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

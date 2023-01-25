from rest_framework import views, status, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from google.oauth2.id_token import verify_oauth2_token
from google.auth.transport import requests

from user.models import User
from .serializers import UserSerializer


class RegisterView(generics.CreateAPIView):
    queryset = None
    serializer_class = UserSerializer


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data["access"]
        user = {**serializer.user, token: token}
        return Response(user, status=status.HTTP_200_OK)


class PasswordResetView(views.APIView):
    def post(self, request):
        user_data = request.data

        try:
            user = User.objects.get(username=user_data["username"])
            user.set_password(user_data["password"])
            user.save()

        except Exception:
            raise Exception("Something went wrong!")

        return Response(status=status.HTTP_201_CREATED)


class UserListView(views.APIView):
    def post(self, request):
        users = User.objects.all()
        for user in users:
            print(user.username)

        return Response({})


class GoogleLogin(views.APIView):
    def post(self, request):
        data = request.data
        id_token = data["id_token"]

        token = verify_oauth2_token(id_token, requests.Request())
        user = User.objects.create(
            username=token["email"], email=token["email"], first_name=token["name"])
        social_account = SocialAccount(user=user, provider="google")
        social_account.uid = token["sub"]
        social_account.save()

        refresh = RefreshToken.for_user(user)
        user = {**user, token: str(refresh.access_token)}
        return Response(data, status=status.HTTP_200_OK)

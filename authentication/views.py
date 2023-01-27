from rest_framework import views, status, generics
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.models import User
from user.serializers import UserSerializer
from .serializers import GoogleTokenSerializer
from .mixins import ValidateGoogleToken


class RegisterView(generics.CreateAPIView):
    queryset = None
    serializer_class = UserSerializer


class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request):
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


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()


class GoogleAuthentication(ValidateGoogleToken):
    serializer_class = GoogleTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data["id_token"]
        google_user = self.get_google_user(token)
        user = self.check_existing_user(google_user)
        if not user:
            user = self.create_user(google_user)

        data = self.serialize_user(user)
        return Response(data, status=status.HTTP_200_OK)

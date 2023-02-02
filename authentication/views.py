from rest_framework import views, status, generics
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from user.serializers import UserSerializer
from .serializers import GoogleTokenSerializer, CredentialSerializer
from .mixins import ValidateGoogleToken, Authenticate


class RegisterView(Authenticate):
    serializer_class = CredentialSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            new_user = self.create_user(email=email, password=password)
            user = self.serialize_user(new_user)
        except Exception as error:
            return Response({"error": "User already exists"}, status=status.HTTP_409_CONFLICT)

        return Response(user, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    # TODO: Create a custom serializer
    serializer_class = TokenObtainPairSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        token = serializer.validated_data["access"]
        serializer = UserSerializer(instance=serializer.user)

        data = {**serializer.data, "token": token}
        return Response(data, status=status.HTTP_200_OK)


class GoogleAuthentication(ValidateGoogleToken):
    # TODO: Do validation in serializer
    serializer_class = GoogleTokenSerializer

    def post(self, request):
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

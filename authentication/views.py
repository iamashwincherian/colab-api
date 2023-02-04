from rest_framework import status
from rest_framework.response import Response
from django.db import IntegrityError

from .serializers import GoogleTokenSerializer, CredentialSerializer
from .mixins import Authenticate


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
        except IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                return Response({"error": "User already exists"}, status=status.HTTP_409_CONFLICT)
            else:
                return Response(e, status=status.HTTP_400_BAD_REQUEST)

        return Response(user, status=status.HTTP_201_CREATED)


class LoginView(Authenticate):
    serializer_class = CredentialSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        user = self.serialize_user(self.authenticate_user(email, password))

        return Response(user, status=status.HTTP_200_OK)


class GoogleAuthentication(Authenticate):
    serializer_class = GoogleTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        google_user = serializer.validated_data["user"]
        user = self.check_if_user_exists(google_user["email"])
        if not user:
            name = google_user["name"].split()
            user = self.create_user(
                email=google_user["email"], first_name=name[0], last_name=name[-1])
            self.create_social_account(user, google_user)

        data = self.serialize_user(user)
        return Response(data, status=status.HTTP_200_OK)

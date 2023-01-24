from django.http import JsonResponse
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from .models import User

class FetchUser(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = User.objects.filter()
        for user in users:
            print(user.gender)

        return JsonResponse({"user": {
            "name": "user.username"
        }}, safe=False)
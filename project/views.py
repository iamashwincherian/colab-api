from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Project
from .serializers import ProjectSerializer


class GetAllProjects(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = Project.objects.filter(owner=request.user)
        serialized_projects = ProjectSerializer(
            instance=projects, many=True).data
        return Response(serialized_projects, status=status.HTTP_200_OK)

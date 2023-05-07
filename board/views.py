from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Board


class BoardListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Board.objects.filter(owner=self.request.user)
        return queryset

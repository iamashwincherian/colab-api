from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Board
from .serializers import BoardSerializer
from list.models import List


class BoardListView(generics.ListAPIView, generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BoardSerializer

    def get_queryset(self):
        board = Board.objects.filter(owner=self.request.user)
        return board

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        return super().perform_create(serializer)


class BoardDetailView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        board = Board.objects.get(
            owner=self.request.user, id=self.request.query_params.get('board_id'))
        list = List.objects.filter(board=board)
        return list

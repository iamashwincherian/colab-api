from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from .models import List
from .serializers import ListSerializer
from board.models import Board


class ListView(generics.ListAPIView, generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = List.objects.all()
    serializer_class = ListSerializer

    def find_board(self, board_id):
        boards = Board.objects.filter(id=board_id)
        if not len(boards):
            raise NotFound({"message": "Board not found"})

        return boards.first()

    def get_queryset(self):
        board = self.find_board(self.kwargs.get('board_id'))
        queryset = self.queryset.filter(board=board)
        return queryset

    def perform_create(self, serializer):
        board = self.find_board(self.kwargs.get('board_id'))
        serializer.save(board=board)
        return super().perform_create(serializer)

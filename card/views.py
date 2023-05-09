from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from .serializers import CardListSerializer
from .models import Card
from board.models import Board
from list.models import List


class CardListView(generics.ListAPIView, generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CardListSerializer
    queryset = Card.objects.all()

    def find_board(self, board_id):
        boards = Board.objects.filter(id=board_id)
        if not len(boards):
            raise NotFound({"message": "Board not found"})

        return boards.first()

    def find_list(self, list_id):
        lists = List.objects.filter(id=list_id)
        if not len(lists):
            raise NotFound({"message": "List not found"})

        return lists.first()

    def get_queryset(self):
        board = self.find_board(self.kwargs.get('board_id'))
        queryset = self.queryset.filter(board=board)
        return queryset

    def perform_create(self, serializer):
        board = self.find_board(self.kwargs.get('board_id'))
        list = self.find_list(self.kwargs.get('list_id'))
        serializer.save(board=board, list=list)
        return super().perform_create(serializer)

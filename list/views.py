from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from .models import List
from .serializers import ListSerializer
from board.models import Board


class ListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = List.objects.all()
    serializer_class = ListSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        board_id = self.request.query_params.get('board_id')
        boards = Board.objects.filter(id=board_id)
        if not len(boards):
            raise NotFound({"message": "Board not found"})

        board = boards.first()
        queryset = self.queryset.filter(board=board)
        return queryset

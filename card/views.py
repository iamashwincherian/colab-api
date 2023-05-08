from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import CardListSerializer
from .models import Card


class CardListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CardListSerializer
    queryset = Card.objects.all()

    def get_queryset(self):
        queryset = self.queryset.filter(self.request.query_params)
        return queryset

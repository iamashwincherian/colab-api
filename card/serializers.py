from rest_framework.serializers import ModelSerializer

from .models import Card


class CardListSerializer(ModelSerializer):
    class Meta:
        model = Card
        fields = '__all__'

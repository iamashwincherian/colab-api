from django.db import models

from shared.models import TimeStampedModel
from board.models import Board
from list.models import List


class Card(TimeStampedModel):
    title = models.CharField(max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    list = models.ForeignKey(List, on_delete=models.CASCADE)

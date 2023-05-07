from django.db import models

from shared.models import TimeStampedModel
from board.models import Board


class List(TimeStampedModel):
    name = models.CharField(max_length=255)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, null=False)

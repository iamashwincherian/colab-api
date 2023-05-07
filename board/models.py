from django.db import models

from shared.models import TimeStampedModel
from user.models import User


class Board(TimeStampedModel):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

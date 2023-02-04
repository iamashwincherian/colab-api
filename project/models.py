from django.db import models

from user.models import User
from shared.models import TimeStampedModel


class Project(TimeStampedModel):
    name = models.CharField(max_length=255)
    owner_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

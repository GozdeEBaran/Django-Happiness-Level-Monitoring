import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from localflavor.ca.ca_provinces import PROVINCE_CHOICES

from hindex.utils.models import BaseModel
from .managers import TeamManager


class Team(BaseModel):
    label = models.CharField(max_length=128, unique=True)
    province = models.TextField(choices=PROVINCE_CHOICES, max_length=2, null=True, blank=True)

    objects = models.Manager()
    with_related = TeamManager()

    def __str__(self):
        return self.label

    class Meta:
        db_table = 'team'


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="users")

    def __str__(self) -> str:
        return self.username

    class Meta:
        db_table = 'user'

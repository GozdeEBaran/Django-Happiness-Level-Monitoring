from django.db import models
from django.utils import timezone

from hindex.utils.models import BaseModel
from hindex.users.models import User
from hindex.happiness_levels.validators import validate_level_limit


class HappinessLevel(BaseModel):

    class HappinessLevelFactor(models.TextChoices):
        HEALTH = "Health"
        FINANCIAL = "Financial Situation"
        FAMILY = "Family Relationships"
        WORK = "Work"
        FRIENDS = "Community and Friends"
        PERSONAL = "Personal Value"
        FREEDOM = "Personal Freedom"
        OTHER = "Other"

    created_at = models.DateField(default=timezone.now)
    level = models.IntegerField(validators=[validate_level_limit],
                                help_text="Level one to ten. One means unhappiest, ten means happiest")
    factor = models.CharField(choices=HappinessLevelFactor.choices, max_length=256)
    notes = models.TextField(help_text="Optional notes for happiness level factor", blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="happiness_levels")

from django.core.exceptions import ValidationError
from django.utils import timezone

from rest_framework.exceptions import ValidationError as DRFValidationError


def validate_level_limit(value):
    if value < 0 or value > 10:
        # this can be used for admin etc, serializer is already being validated
        raise ValidationError("Please enter the level 1-10")


def validate_user_for_current_date(user):
    from hindex.happiness_levels.models import HappinessLevel

    today = timezone.now().date()
    level = HappinessLevel.objects.filter(user=user, created_at=today)

    if level:
        raise DRFValidationError("You already inserted happiness for the current day")


def validate_from_and_to_date(from_date, to_date):
    if from_date > to_date:
        raise DRFValidationError("From date cannot be greater than to date.")

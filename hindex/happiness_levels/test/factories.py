import factory

from hindex.happiness_levels.models import HappinessLevel
from hindex.users.test.factories import UserFactory


class HappinessLevelFactory(factory.django.DjangoModelFactory):
    level = 5
    factor = HappinessLevel.HappinessLevelFactor.OTHER
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = HappinessLevel
        django_get_or_create = ['level', 'factor', 'user']

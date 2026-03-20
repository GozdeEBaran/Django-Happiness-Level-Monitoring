import factory

from hindex.users.models import User, Team


class TeamFactory(factory.django.DjangoModelFactory):
    label = "Base Team"

    class Meta:
        model = Team
        django_get_or_create = ['label']


class UserFactory(factory.django.DjangoModelFactory):
    username = "base user"
    team = factory.SubFactory(TeamFactory)

    class Meta:
        model = User
        django_get_or_create = ['username']

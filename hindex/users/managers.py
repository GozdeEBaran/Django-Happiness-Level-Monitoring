from django.db.models import Manager


class TeamManager(Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related('users', 'users__happiness_levels')

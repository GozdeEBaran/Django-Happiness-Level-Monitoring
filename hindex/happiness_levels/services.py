from django.db.models.query_utils import Q
from django.db.models import Avg

from hindex.users.models import Team
from .models import HappinessLevel
from .serializers import HappinessAverageTeamSerializer, HappinessAverageTeamDetailSerializer


class HappinessStatService:
    def __init__(self, authenticated, date_from=None, date_to=None):
        self.date_from = date_from
        self.date_to = date_to
        self.authenticated = authenticated

        self.happiness_levels = HappinessLevel.objects.all()

        if self.date_from and not self.date_to:
            self.happiness_levels = self.happiness_levels.filter(
                created_at__gte=self.date_from
            )
        if self.date_to and not self.date_from:
            self.happiness_levels = self.happiness_levels.filter(
                created_at__lte=self.date_to
            )
        if self.date_to and self.date_from:
            self.happiness_levels = self.happiness_levels.filter(
                Q(created_at__gte=self.date_from) & Q(created_at__lte=self.date_to)
            )
        self.happiness_level_uuids = self.happiness_levels.values_list('uuid', flat=True)

        # Annotate teams to get the average for each team dynamically based on the given date
        team_qs = Team.with_related.all()
        self.teams = team_qs.annotate(
            avg_happiness_level=Avg('users__happiness_levels__level',
                                    filter=Q(users__happiness_levels__uuid__in=self.happiness_level_uuids))
        )

    def get_stats(self):
        if not self.authenticated:
            return self._average_team_happiness()
        return self._detail_average_team_happiness()

    def _average_team_happiness(self):
        serializer = HappinessAverageTeamSerializer(self.teams, many=True)
        return serializer.data

    def _detail_average_team_happiness(self):
        # send happiness level uuids as context to filter the result in the serializer
        serializer = HappinessAverageTeamDetailSerializer(
            self.teams, many=True, context=self.happiness_level_uuids)
        return serializer.data

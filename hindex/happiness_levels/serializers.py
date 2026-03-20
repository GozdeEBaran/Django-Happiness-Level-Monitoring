from django.db.models import Count, Q
from rest_framework import serializers

from hindex.users.models import Team
from .models import HappinessLevel
from .validators import validate_user_for_current_date, validate_from_and_to_date


class HappinessLevelGetSerializer(serializers.ModelSerializer):
    level = serializers.IntegerField(max_value=10)

    class Meta:
        model = HappinessLevel
        exclude = ('id', 'updated_at')


class HappinessPatchSerializer(serializers.ModelSerializer):
    level = serializers.IntegerField(max_value=10)

    class Meta:
        model = HappinessLevel
        exclude = ('id', 'user', 'created_at')


class HappinessLevelCreateSerializer(HappinessPatchSerializer):

    def validate(self, data):
        user = self.context['request'].user
        validate_user_for_current_date(user)
        data["user"] = user
        return data


class HappinessStatisticRequestSerializer(serializers.Serializer):
    date_from = serializers.DateField(
        required=False, allow_null=True, format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])
    date_to = serializers.DateField(required=False, allow_null=True,
                                    format="%d-%m-%Y", input_formats=['%d-%m-%Y', 'iso-8601'])

    def validate(self, data):
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        if date_from and date_to:
            validate_from_and_to_date(date_from, date_to)
        return data


class HappinessAverageTeamSerializer(serializers.ModelSerializer):
    team = serializers.CharField(source='label')
    avg = serializers.SerializerMethodField()

    def get_avg(self, obj):
        average = obj.avg_happiness_level
        return average if not average else round(average, 1)

    class Meta:
        model = Team
        fields = ('team', 'avg')


class HappinessAverageDetailAvgSerializer(serializers.Serializer):
    level = serializers.IntegerField(source="happiness_levels__level")
    number_of_people = serializers.IntegerField(source="count")


class HappinessAverageTeamDetailSerializer(HappinessAverageTeamSerializer):
    detail = serializers.SerializerMethodField()

    def get_detail(self, obj):
        subquery = obj.users.values(
            'happiness_levels__level'
        ).annotate(count=Count('id', filter=Q(happiness_levels__uuid__in=self.context))).\
            order_by('happiness_levels__level')

        return HappinessAverageDetailAvgSerializer(subquery, many=True).data

    class Meta:
        model = Team
        fields = ('team', 'avg', 'detail')

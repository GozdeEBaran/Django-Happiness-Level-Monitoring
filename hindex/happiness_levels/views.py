from rest_framework import viewsets
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


from hindex.utils.swagger_doc import get_available_responses_with_auth_fail
from hindex.users.services import get_user_is_authorized
from .models import HappinessLevel
from .services import HappinessStatService
from .serializers import (HappinessLevelGetSerializer,
                          HappinessLevelCreateSerializer,
                          HappinessPatchSerializer,
                          HappinessStatisticRequestSerializer)
from .swagger_doc import (health_index_list_responses,
                          health_index_list_description,
                          health_index_post_description,
                          health_index_post_responses,
                          health_index_partial_update_description,
                          health_index_partial_update_responses,
                          health_index_retrieve_description,
                          health_index_retrieve_responses,
                          health_stat_list_description,
                          health_stat_list_responses)


class HappinessLevelsViewSet(viewsets.ModelViewSet):
    lookup_field = 'uuid'
    lookup_url_kwarg = 'uuid'
    http_method_names = ['get', 'post', 'patch']

    queryset = HappinessLevel.objects.all().order_by('id')
    serializer_class = HappinessLevelGetSerializer

    serializer_action_classes = {
        'create': HappinessLevelCreateSerializer,
        'partial_update': HappinessPatchSerializer
    }

    @extend_schema(
        responses=get_available_responses_with_auth_fail(
            health_index_list_responses
        ),
        description=health_index_list_description)
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @extend_schema(
        responses=get_available_responses_with_auth_fail(
            health_index_post_responses
        ),
        description=health_index_post_description)
    def create(self, *args, **kwargs):
        return super().create(*args, **kwargs)

    @extend_schema(
        responses=get_available_responses_with_auth_fail(
            health_index_retrieve_responses
        ),
        description=health_index_retrieve_description)
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        responses=get_available_responses_with_auth_fail(
            health_index_partial_update_responses
        ),
        description=health_index_partial_update_description)
    def partial_update(self, *args, **kwargs):
        return super().partial_update(*args, **kwargs)

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):  # noqa
            return super().get_serializer_class()

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class HappinessStatViewSet(viewsets.GenericViewSet):
    authentication_classes = []
    permission_classes = []

    queryset = HappinessLevel.objects.all()
    http_method_names = ['get']

    serializer_action_classes = {
        'list': HappinessStatisticRequestSerializer
    }
    pagination_class = None

    def get_serializer_class(self):
        return self.serializer_action_classes[self.action]

    @extend_schema(
        parameters=[HappinessStatisticRequestSerializer],
        responses=health_stat_list_responses,
        description=health_stat_list_description)
    def list(self, request, *args, **kwargs):
        user_is_authenticated = get_user_is_authorized(request)

        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        service = HappinessStatService(user_is_authenticated, **serializer.validated_data)
        return Response(service.get_stats())

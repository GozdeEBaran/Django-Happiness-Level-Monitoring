from rest_framework import status
from drf_spectacular.utils import OpenApiResponse, OpenApiTypes, OpenApiExample

from hindex.happiness_levels.serializers import HappinessLevelGetSerializer

health_index_list_description = """
Returns requested user's happiness levels
"""  # noqa

health_index_list_responses = {
    status.HTTP_200_OK: OpenApiResponse(
        HappinessLevelGetSerializer(many=True),
        "Successfully received all happiness levels"
    )
}

health_index_retrieve_description = """
Returns requested user's happiness level
"""  # noqa

health_index_retrieve_responses = {
    status.HTTP_200_OK: OpenApiResponse(
        HappinessLevelGetSerializer(many=True),
        "Successfully received individual happiness level"
    )
}


health_index_post_description = """
Creates happiness index for current date and requested user, factor enum can be reached through /api/v1/utils/enums
"""  # noqa

health_index_post_responses = {
    status.HTTP_201_CREATED: OpenApiResponse(
        HappinessLevelGetSerializer(many=True),
        "Successfully created happiness level"
    )
}


health_index_partial_update_description = """
Updates existing happiness level
"""  # noqa

health_index_partial_update_responses = {
    status.HTTP_200_OK: OpenApiResponse(
        HappinessLevelGetSerializer(many=True),
        "Successfully updated happiness level"
    )
}


health_stat_list_description = """
Returns stats
- Detail response for authenticated user
- Only average team happiness level for anonymous user
"""  # noqa

authenticated_res = [
    {
        "team": "TEST-Kingston Frontenacs",
        "avg": 5,
        "detail": [
            {
                "level": 5,
                "number_of_people": 3
            }
        ]
    },
    {
        "team": "TEST-Barrie Colts",
        "avg": 2,
        "detail": [
            {
                "level": 2,
                "number_of_people": 3
            }
        ]
    },
]

unauthenticated_res = [
    {
        "team": "TEST-Kingston Frontenacs",
        "avg": 5,

    },
    {
        "team": "TEST-Barrie Colts",
        "avg": 2,

    },
]

health_stat_list_responses = {
    status.HTTP_200_OK: OpenApiResponse(
        response=OpenApiTypes.OBJECT,
        description="Successfully received stats",
        examples=[
            OpenApiExample('Authenticated',
                           authenticated_res, status_codes=["200"]),
            OpenApiExample('Unauthenticated',
                           unauthenticated_res, status_codes=["200"]),
        ]
    )
}

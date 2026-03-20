from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiResponse
from rest_framework import status


def get_available_responses_with_auth_fail(response):
    default_expired_token_response = {
        "detail": "Given token not valid for any token type",
        "code": "token_not_valid",
        "messages": [
            {
                "tokenClass": "AccessToken",
                "tokenType": "access",
                "message": "Token is invalid or expired"
            }
        ]
    }
    default_invalid_token_response = {
        "details": "Authentication credentials were not provided."
    }

    response.update(
        {
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Invalid or Expired token.",
                examples=[
                    OpenApiExample('Invalid', default_invalid_token_response, status_codes=["401"]),
                    OpenApiExample('Expired', default_expired_token_response, status_codes=["401"])
                ]
            ),
        }
    )

    return response

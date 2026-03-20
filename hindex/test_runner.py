from rest_framework.test import APIClient as Client

from hindex.users.services import get_tokens_for_user


class APIClient(Client):
    def force_authenticate(self, user):
        token = get_tokens_for_user(user)
        super().credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

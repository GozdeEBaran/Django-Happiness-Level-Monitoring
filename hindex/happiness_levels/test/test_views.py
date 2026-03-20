from django.test.testcases import TestCase
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from hindex.test_runner import APIClient
from hindex.users.test.factories import UserFactory
from hindex.happiness_levels.models import HappinessLevel
from .factories import HappinessLevelFactory


class HappinessLevelViewsetTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)

        self.today = timezone.now().date()
        self.index_1 = HappinessLevelFactory(
            level=2, user=self.user, created_at=self.today - timezone.timedelta(days=1))
        self.index_2 = HappinessLevelFactory(
            level=8, user=self.user, created_at=self.today - timezone.timedelta(days=2))
        self.index_3 = HappinessLevelFactory(
            level=9, user=self.user, created_at=self.today - timezone.timedelta(days=3))

        self.url = reverse('happiness-level-list')

    def test_get_success(self):
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_retrieve_success(self):
        response = self.client.get(f"{self.url}{str(self.index_1.uuid)}/")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_patch_success(self):
        body = {
            "level": 4
        }
        response = self.client.patch(f"{self.url}{str(self.index_1.uuid)}/", body)
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_post_date_fail(self):
        HappinessLevelFactory(
            level=7, user=self.user, created_at=self.today)
        body = {
            "level": 5,
            "factor": "Health",
            "notes": "Something"
        }
        response = self.client.post(self.url, body)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You already inserted", str(response.data))

    def test_post_validate_user(self):
        body = {
            "level": 5,
            "factor": "Health",
            "notes": "Something"
        }
        response = self.client.post(self.url, body)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        h = HappinessLevel.objects.get(uuid=response.data.get('uuid'))
        self.assertEquals(h.user.id, self.user.id)


class HappinessLevelStatsTestCase(TestCase):
    def setUp(self):
        today = timezone.now().date()
        HappinessLevelFactory(
            level=2, user=UserFactory(username="test_1"), created_at=today - timezone.timedelta(days=1))
        HappinessLevelFactory(
            level=8, user=UserFactory(username="test_2"), created_at=today - timezone.timedelta(days=2))
        HappinessLevelFactory(
            level=9, user=UserFactory(username="test_3"), created_at=today - timezone.timedelta(days=3))

        self.client = APIClient()
        self.url = reverse('happiness-stats-list')

    def test_unauthenticated_user(self):
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data[0]), 2)

    def test_authenticated_user(self):
        user = UserFactory()
        self.client.force_authenticate(user=user)
        response = self.client.get(self.url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(response.data[0]), 3)

    def test_param_fail(self):
        response = self.client.get(f"{self.url}?date_from=2022-01-10&date_to=2022-01-01")
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("From date cannot be", str(response.data))

    def test_param_passes(self):
        response1 = self.client.get(f"{self.url}?date_to=2022-01-01")
        response2 = self.client.get(f"{self.url}?date_from=2022-01-10")
        response3 = self.client.get(f"{self.url}?date_from=2022-01-01&date_to=2022-01-10")
        self.assertEquals(response1.status_code, status.HTTP_200_OK)
        self.assertEquals(response2.status_code, status.HTTP_200_OK)
        self.assertEquals(response3.status_code, status.HTTP_200_OK)

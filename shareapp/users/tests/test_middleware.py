import pytest
from django.urls import reverse

from shareapp.users.models import UserAgent

pytestmark = pytest.mark.django_db


class TestUserAgentLoggerMiddleware:
    url = reverse("main:home")

    def test_no_user_agent_logged_for_anonymous_user(self, client):
        client.get(self.url)
        assert UserAgent.objects.count() == 0

    def test_user_agent_logged_for_authenticated_users(self, auto_login_user):
        client, user = auto_login_user()
        for _ in range(3):
            client.get(self.url)
        assert UserAgent.objects.count() == 1
        assert UserAgent.objects.first().user == user

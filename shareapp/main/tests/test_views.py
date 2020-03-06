import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

pytestmark = pytest.mark.django_db


class TestHomeView:
    url = reverse("main:home")

    def test_login_required(self, client):
        response = client.get(self.url)
        assert response.status_code == 302
        assert "accounts/login" in response.url

    def test_template_used(self, auto_login_user):
        client, user = auto_login_user()
        response = client.get(self.url)
        assert response.status_code == 200
        assertTemplateUsed(response, "main/home.html")


class TestFaviconFixView:
    def test_favicon_redirect(self, client):
        response = client.get("/favicon.ico")
        assert response.status_code == 301
        assert "/static/images/favicons/favicon.ico" in response.url

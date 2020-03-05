import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

pytestmark = pytest.mark.django_db


class TestHomeView:
    def test_template_used(self, client):
        url = reverse("main:home")
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, "main/home.html")


class TestFaviconFixView:
    def test_favicon_redirect(self, client):
        response = client.get("/favicon.ico")
        assert response.status_code == 301
        assert "/static/images/favicons/favicon.ico" in response.url

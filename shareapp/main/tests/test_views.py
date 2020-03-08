from io import BytesIO

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


def test_favicon_redirect(client):
    response = client.get("/favicon.ico")
    assert response.status_code == 301
    assert "/static/images/favicons/favicon.ico" in response.url


def test_add_url_view(auto_login_user, fake):
    client, user = auto_login_user()
    url = fake.uri()
    response = client.post(reverse("main:new_url"), {"url": url}, follow=True)
    assert response.status_code == 200
    assert url.encode() in response.content


def test_add_file_view(auto_login_user, fake):
    client, user = auto_login_user()
    file = BytesIO(fake.binary(length=512))
    file.name = fake.file_name()
    response = client.post(reverse("main:new_file"), {"file": file}, follow=True)
    assert response.status_code == 200
    assert file.name.encode() in response.content

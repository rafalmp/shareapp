import uuid

import pytest
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

pytestmark = pytest.mark.django_db


@pytest.fixture
def test_password():
    return "strong-test-password-1"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = uuid.uuid4().hex
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user

    return make_auto_login


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

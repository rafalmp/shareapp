from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class UserAgent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_agent")
    user_agent = models.TextField(_("Last User-Agent string"))

    def __str__(self):
        return f"User-Agent ({self.user.username})"

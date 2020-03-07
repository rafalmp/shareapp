import random
import string
from datetime import datetime, timedelta
from time import time

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from hashid_field import HashidAutoField

from shareapp.users.views import User


def make_file_path(instance, filename: str) -> str:
    return f"{instance.owner.username}/{int(time())}/{filename}"


def make_random_password() -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(random.sample(alphabet, 8))


def make_expire_timestamp() -> datetime:
    return now() + timedelta(seconds=settings.SHARED_ITEM_EXPIRE_TIME)


class SharedItem(models.Model):
    id = HashidAutoField(primary_key=True)
    owner = models.ForeignKey(
        User,
        verbose_name=_("Owner"),
        on_delete=models.CASCADE,
        related_name="shared_items",
    )
    url = models.TextField(_("URL"), blank=True)
    file = models.FileField(_("File"), upload_to=make_file_path, blank=True)
    password = models.CharField(
        _("Password"), default=make_random_password, max_length=254
    )
    created = models.DateTimeField(_("Created"), auto_now_add=True)
    expires = models.DateTimeField(_("Expires"), default=make_expire_timestamp)
    views = models.IntegerField(_("Number of views"), default=0)

    def __str__(self):
        return self.url or self.file.name.rsplit("/")[-1]

    class Meta:
        verbose_name = _("Shared item")
        verbose_name_plural = _("Shared items")

import random
import string
from datetime import datetime, timedelta
from time import time

from django.conf import settings
from django.db import models, transaction
from django.dispatch import Signal, receiver
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _
from hashid_field import HashidAutoField

from shareapp.users.models import User


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

    @property
    def is_expired(self):
        return self.expires < now()

    def __str__(self):
        return self.url or self.file.name.rsplit("/")[-1]

    def save(self, *args, **kwargs):
        if self.pk is None:
            Retrieval.objects.get_or_create(user=self.owner, created=now().date())
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Shared item")
        verbose_name_plural = _("Shared items")


class Retrieval(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="retrievals")
    created = models.DateField(_("Created"))
    files = models.IntegerField(_("File downloads"), default=0)
    links = models.IntegerField(_("URL views"), default=0)

    def __str__(self):
        return f"{self.user.username} - {self.created}"

    class Meta:
        verbose_name = _("Retrieval")
        verbose_name_plural = _("Retrievals")
        unique_together = ["user", "created"]


item_retrieved = Signal(providing_args=["item_id"])


# noinspection PyUnusedLocal
@receiver(item_retrieved)
def update_retrieval_statistics(sender, item_id, **kwargs):
    with transaction.atomic():
        item = SharedItem.objects.select_for_update().get(id=item_id)
        item.views += 1
        item.save()
    if item.views == 1:
        update_daily_retrievals(item)


def update_daily_retrievals(item: SharedItem):
    with transaction.atomic():
        retrieval = Retrieval.objects.select_for_update().get(
            user=item.owner, created=item.created.date()
        )
        if item.url:
            retrieval.links += 1
        else:
            retrieval.files += 1
        retrieval.save()

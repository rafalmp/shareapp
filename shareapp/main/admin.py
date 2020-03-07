from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from shareapp.main.models import SharedItem


@admin.register(SharedItem)
class SharedItemAdmin(admin.ModelAdmin):
    readonly_fields = ["views", "created"]
    list_display = ["owner", "item_title", "id", "password", "expires"]

    def item_title(self, instance):
        return str(instance)

    item_title.short_description = _("Item")

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from shareapp.users.forms import UserChangeForm, UserCreationForm
from shareapp.users.models import UserAgent

User = get_user_model()


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    readonly_fields = ("last_user_agent",)
    fieldsets = (
        (_("User"), {"fields": ("name", "last_user_agent")}),
    ) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]

    def last_user_agent(self, instance):
        try:
            return UserAgent.objects.get(user=instance).user_agent
        except UserAgent.DoesNotExist:
            return _("User did not log in yet!")

    last_user_agent.short_description = _("Last User-Agent string")

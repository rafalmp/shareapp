from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.validators import URLValidator
from django.utils.translation import ugettext_lazy as _

from shareapp.main.models import SharedItem
from shareapp.users.models import User


class UrlForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", _("Submit")))

    url = forms.CharField(label=_("URL"), validators=[URLValidator()])

    def save(self, user: User) -> SharedItem:
        return SharedItem.objects.create(url=self.cleaned_data["url"], owner=user)

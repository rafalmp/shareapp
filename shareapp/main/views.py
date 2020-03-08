from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, ListView

from shareapp.main.forms import UrlForm, FileForm
from shareapp.main.models import SharedItem


class HomeView(LoginRequiredMixin, ListView):
    model = SharedItem
    ordering = "-created"
    context_object_name = "shared_items"
    template_name = "main/home.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(owner=self.request.user)


home_view = HomeView.as_view()


class AddItemView(LoginRequiredMixin, FormView):
    def form_valid(self, form):
        item: SharedItem = form.save(self.request.user)
        message = _("Successfully added '%(item)s' to your Shared Items.") % {
            "item": item
        }
        messages.success(self.request, message)
        return super().form_valid(form)


class AddUrlView(AddItemView):
    template_name = "main/add_url.html"
    form_class = UrlForm
    success_url = reverse_lazy("main:home")


add_url_view = AddUrlView.as_view()


class AddFileView(AddItemView):
    template_name = "main/add_file.html"
    form_class = FileForm
    success_url = reverse_lazy("main:home")


add_file_view = AddFileView.as_view()

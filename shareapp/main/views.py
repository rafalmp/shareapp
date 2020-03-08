from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, ListView

from shareapp.main.forms import UrlForm
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


class UrlView(LoginRequiredMixin, FormView):
    template_name = "main/add_url.html"
    form_class = UrlForm
    success_url = reverse_lazy("main:home")

    def form_valid(self, form):
        item: SharedItem = form.save(self.request.user)
        message = _("Successfully added '%(url)s' to your Shared Items.") % {
            "url": item.url
        }
        messages.success(self.request, message)
        return super().form_valid(form)


new_url_view = UrlView.as_view()

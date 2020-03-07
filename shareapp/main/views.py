from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

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

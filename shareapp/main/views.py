from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, FormView, ListView

from shareapp.main.forms import FileForm, PasswordForm, UrlForm
from shareapp.main.models import SharedItem, item_retrieved


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


class RetrieveItemView(DetailView):
    template_name = "main/get_item.html"
    model = SharedItem
    context_object_name = "item"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PasswordForm()
        return context

    def post(self, request, **kwargs):
        password = request.POST.get("password", "").strip()
        item: SharedItem = self.get_object()

        if password != item.password:
            messages.error(
                request, _("The password you provided is incorrect. Access denied.")
            )
            return redirect(request.path_info)
        elif item.is_expired:
            return redirect(request.path_info)
        else:
            return self.handle_retrieval(item)

    def handle_retrieval(self, item: SharedItem):
        item_retrieved.send(sender=self.__class__, item_id=item.id)
        if item.url:
            return redirect(item.url)
        else:
            return FileResponse(item.file, as_attachment=True)


retrieve_item_view = RetrieveItemView.as_view()

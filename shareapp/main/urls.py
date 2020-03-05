from django.urls import path
from django.views.generic import TemplateView, RedirectView

app_name = "main"
urlpatterns = [
    path("", TemplateView.as_view(template_name="main/home.html"), name="home"),
    path(
        "favicon.ico",
        RedirectView.as_view(url="/static/images/favicons/favicon.ico", permanent=True),
        name="favicon",
    ),
]

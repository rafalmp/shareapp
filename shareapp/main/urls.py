from django.urls import path
from django.views.generic import RedirectView

from shareapp.main.views import home_view

app_name = "main"
urlpatterns = [
    path("", view=home_view, name="home"),
    path(
        "favicon.ico",
        RedirectView.as_view(url="/static/images/favicons/favicon.ico", permanent=True),
        name="favicon",
    ),
]

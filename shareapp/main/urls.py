from django.urls import path

from shareapp.main.views import home_view

app_name = "main"
urlpatterns = [
    path("", view=home_view, name="home"),
]

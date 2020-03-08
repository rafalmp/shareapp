from django.urls import path

from shareapp.main.views import home_view, new_url_view

app_name = "main"
urlpatterns = [
    path("", view=home_view, name="home"),
    path("new-url", view=new_url_view, name="new_url"),
]

from django.urls import path

from shareapp.main.views import (
    home_view,
    add_url_view,
    add_file_view,
    retrieve_item_view,
)

app_name = "main"
urlpatterns = [
    path("", view=home_view, name="home"),
    path("new-url", view=add_url_view, name="new_url"),
    path("new-file", view=add_file_view, name="new_file"),
    path("<pk>", view=retrieve_item_view, name="get_item"),
]

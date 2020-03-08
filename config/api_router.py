from rest_framework.routers import DefaultRouter

from shareapp.main.api.views import SharedItemViewSet
from shareapp.users.api.views import UserViewSet

router = DefaultRouter()

router.register("users", UserViewSet)
router.register("shared", SharedItemViewSet, basename="shared_items")


app_name = "api"
urlpatterns = router.urls

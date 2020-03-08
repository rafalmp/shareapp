from rest_framework.routers import DefaultRouter

from shareapp.main.api.views import SharedItemViewSet


router = DefaultRouter()
router.register("shared", SharedItemViewSet, basename="shared_items")


app_name = "api"
urlpatterns = router.urls

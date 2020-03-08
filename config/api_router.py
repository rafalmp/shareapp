from rest_framework.routers import DefaultRouter

from shareapp.main.api.views import SharedItemViewSet, SharedItemRetrieveViewSet

router = DefaultRouter()
router.register("shared", SharedItemViewSet, basename="shared_items")
router.register("retrieve", SharedItemRetrieveViewSet, basename="retrieve")


app_name = "api"
urlpatterns = router.urls

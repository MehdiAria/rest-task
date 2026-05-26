from rest_framework.routers import DefaultRouter
from .views import PremiumGiftJobViewSet

router = DefaultRouter()
router.register("jobs", PremiumGiftJobViewSet, basename="gift-jobs")
urlpatterns = router.urls

from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('create', views.UserViewSet)

urlpatterns = router.urls

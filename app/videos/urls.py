from django.urls import path, include
from rest_framework import routers
from .views import VideosViewSet

router = routers.SimpleRouter()
router.register("", VideosViewSet)
urlpatterns = [path("", include(router.urls))]

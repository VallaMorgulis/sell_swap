from django.urls import include, path
from rest_framework import routers
from .views import PageViewViewSet

router = routers.DefaultRouter()
router.register('pageviews', PageViewViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
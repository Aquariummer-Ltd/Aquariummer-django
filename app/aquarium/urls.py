from django.urls import path, include
from rest_framework.routers import DefaultRouter

from aquarium import views


router = DefaultRouter()
router.register('fishes', views.FishViewSet)

app_name = 'aquarium'

urlpatterns = [
    path('', include(router.urls))
]

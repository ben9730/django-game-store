from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, PlatformViewSet

router = DefaultRouter()
router.register(r'games', GameViewSet)
router.register(r'platforms', PlatformViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('games/<int:pk>/upload-image/', GameViewSet.as_view({'post': 'upload_image'}), name='game-upload-image'),
]

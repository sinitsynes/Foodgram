from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import FollowCreateViewSet, FollowRetrieveViewSet

router = DefaultRouter()
router.register(r'users/subscriptions', FollowRetrieveViewSet,
                basename='follows')
router.register(r'users/(?P<author_id>\d+)/subscribe',
                FollowCreateViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

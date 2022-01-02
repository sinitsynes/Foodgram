from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet



# router_v1 = DefaultRouter()
# router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    # path('', include(router_v1.urls)),
    path(
        r'^users/$',
        CustomUserViewSet.as_view({'get': 'list'}),
        name='user-list',
    ),
    path('', include('djoser.urls')),
]


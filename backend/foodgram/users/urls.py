from django.urls import include, path
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh


urlpatterns = [
    path('', include('djoser.urls')),
    path('/auth/token/login/', token_obtain_pair, name='token_obtain'),
    path('/auth/token/refresh/', token_refresh, name='token_refresh')
]

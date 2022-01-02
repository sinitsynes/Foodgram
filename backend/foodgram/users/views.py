from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework.permissions import AllowAny

# from .serializers import SignUpSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    permission_classes = [AllowAny]

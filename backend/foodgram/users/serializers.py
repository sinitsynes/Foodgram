from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer, UserCreateSerializer
from rest_framework import serializers
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, 
from rest_framework.validators import UniqueTogetherValidator
from .models import User

User = get_user_model()

# class BaseUserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = User
#         fields = (
#             'email',
#             'id',
#             'username',
#             'first_name',
#             'last_name',
#         )

#         validators = [
#             UniqueTogetherValidator(
#                 queryset=User.objects.all(),
#                 fields=('username', 'email')
#             )
#         ]

#     def validate_username(self, value):
#         if value == 'me':
#             raise serializers.ValidationError(
#                 'Нельзя использовать username «me»'
#             )
#         return


# class FullUserSerializer(BaseUserSerializer):
    
#     class Meta(BaseUserSerializer.Meta):
#         read_only_fields = None


class SignUpSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class ProfileViewSerializer(UserSerializer):
    
    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name')



# class SignUpSerializer(BaseUserSerializer):
#     email = serializers.EmailField()
#     username = serializers.CharField()
#     first_name = serializers.CharField()
#     last_name = serializers.CharField()
#     password = serializers.CharField()

#     class Meta:
#         model = User
#         fields = (
#             'email',
#             'username',
#             'first_name',
#             'last_name',
#             'password',
#         )
#         validators = []

#     def validate(self, data):
#         try:
#             User.objects.get(
#                 username=data.get('username'),
#             )
#         except User.DoesNotExist:
#             serializer = BaseUserSerializer(data=data)
#             serializer.is_valid(raise_exception=True)
#         return data



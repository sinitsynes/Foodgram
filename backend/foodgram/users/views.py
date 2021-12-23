from django.contrib.auth import get_user_model
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from .serializers import SignUpSerializer

User = get_user_model()

# @api_view(['POST'])
# def signup(request):
#     serializer = SignUpSerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)
#     User.objects.get_or_create(**serializer.data)
#     return Response(serializer.data, status=status.HTTP_200_OK)


# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     lookup_field = 'username'
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('=username',)

#     def get_serializer_class(self):
#         if self.request.user.is_admin:
#             return FullUserSerializer
#         return BaseUserSerializer

# class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
#     pass

# class SignUpViewSet(CreateViewSet):
#     serializer_class = SignUpSerializer

#     def perform_create(self, request, serializer):
#         user = User.objects.create(**serializer.data)
#         serializer.save()




from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Follow
from .serializers import FollowCreateSerializer, FollowRetrieveSerializer

User = get_user_model()


class FollowViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FollowCreateSerializer
        if self.request.method == 'GET':
            return FollowRetrieveSerializer

    def get_queryset(self):
        if self.request.method == 'POST':
            return Follow.objects.filter(user=self.request.user)
        if self.request.method == 'GET':
            return User.objects.filter(
                following__user=self.request.user)

    @action(detail=True, methods=['POST'],
            url_path='subscribe')
    def subscribe(self, request, pk):
        user = request.user.id
        data = {'user': user, 'author': pk}
        context = {'request': request}
        serializer = FollowCreateSerializer(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscription(self, request, pk):
        subscription = get_object_or_404(Follow, author__id=pk)
        subscription.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['GET'],
            url_path='subscriptions')
    def subscriptions(self, request):
        user = request.user.id
        queryset = User.objects.filter(following__user=user)
        serializer = FollowRetrieveSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

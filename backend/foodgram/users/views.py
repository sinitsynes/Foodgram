from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Follow, User
from .serializers import FollowCreateSerializer, FollowRetrieveSerializer


@action(methods=['delete'], detail=False)
class FollowCreateViewSet(viewsets.ModelViewSet):
    serializer_class = FollowCreateSerializer
    queryset = Follow.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        author_id = self.kwargs['author_id']
        author = get_object_or_404(User, id=author_id)
        user = request.user
        Follow.objects.filter(user=user, author=author).delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class FollowRetrieveViewSet(viewsets.ModelViewSet):
    serializer_class = FollowRetrieveSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return User.objects.filter(following__user=self.request.user)

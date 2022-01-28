from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.validators import UniqueTogetherValidator

from .models import Follow, User
from recipes.models import Recipe


class UserCreateSerializer(UserCreateSerializer):

    class Meta(UserCreateSerializer.Meta):
        fields = ('username', 'email', 'first_name', 'last_name', 'password')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username', 'email')
            )
        ]


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta(UserSerializer.Meta):
        fields = (
            'id', 'username', 'email',
            'first_name', 'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        user = request.user
        return Follow.objects.filter(author=obj, user=user).exists()


class FollowRetrieveSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('author', 'recipes', 'recipes_count',)

    def get_recipes(self, obj):
        from recipes.serializers import ShortRecipeListSerializer

        queryset = Recipe.objects.filter(author=obj)
        return ShortRecipeListSerializer(queryset, many=True).data

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()

    def get_author(self, obj):
        return CustomUserSerializer(obj).data


class FollowCreateSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ('author',)

    def create(self, validated_data):
        author_id = self.context['view'].kwargs['author_id']
        author = User.objects.get(id=author_id)
        user = self.context.get('request').user
        Follow.objects.get_or_create(author=author, user=user)
        return author

    def validate(self, data):
        author_id = self.context['view'].kwargs['author_id']
        author = User.objects.get(id=author_id)
        user = self.context.get('request').user
        if author == user:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя'
            )
        if Follow.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError(
                'Нельзя подписаться на одного автора дважды'
            )
        return data
    
    def to_representation(self, instance):
        return FollowRetrieveSerializer(instance).data
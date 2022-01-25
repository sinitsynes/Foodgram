from django.db import models
from django.db.models import F, Q
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER = 'Пользователь'
    ADMIN = 'Администратор'

    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (ADMIN, 'Администратор')
    )

    username = models.CharField(
        max_length=20,
        verbose_name='Username',
        unique=True
    )

    first_name = models.CharField(
        max_length=10,
        verbose_name='Имя пользователя'
    )
    last_name = models.CharField(
        max_length=20,
        verbose_name='Фамилия пользователя'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Email'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    role = models.CharField(
        max_length=16,
        choices=ROLE_CHOICES,
        default=USER,
        verbose_name='Роль'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-id',)

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser


class Follow(models.Model):
    user = models.ForeignKey(User, 'Подписчик', related_name='follower')
    author = models.ForeignKey(User, 'Инфлюенсер', related_name='following')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'), name='unique_following'
            ),
            models.CheckConstraint(
                check=~Q(user=F('author')), name='no_self_following'
            )
        )

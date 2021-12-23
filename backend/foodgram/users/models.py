from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLES = (
        ('user', 'Пользователь'),
        ('admin', 'Администратор')
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
    role = models.CharField(
        max_length=16,
        choices=ROLES,
        default='user',
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
        return self.role == 'user'

    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    По сигналу 'post_save' создает токен для нового пользователя.
    """
    if created:
        Token.objects.create(user=instance)


class UserManager(BaseUserManager):
    """
    Создает пользователя с имэйлом и паролем.
    """
    use_in_migrations = True

    def create_user(self, email, password):
        if email is None:
            raise TypeError('Введите email адрес.')
        user = self.model(email=email, password=password)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Создает пользователя со статусом админа.
        """
        if password is None:
            raise TypeError('Введите пароль.')
        user = self.create_user(email=email, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Модель кастомного юзера с нужными полями.
    """
    class SexChoices(models.TextChoices):
        MALE = 'ML'
        FEMALE = 'FL'

    avatar = models.ImageField(upload_to='avatars/')
    sex = models.CharField(max_length=2, choices=SexChoices.choices)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    lat = models.FloatField(default=59.7914)
    lon = models.FloatField(default=30.1650)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email


class Match(models.Model):
    """
    Модель лайков юзера.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='liked_to')
    user_like = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                                  related_name='was_liked')

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"

        constraints = [models.UniqueConstraint(fields=['user', 'user_like'],
                                               name='unique_match')]

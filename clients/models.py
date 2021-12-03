from django.db import models
from django.contrib.auth.models import (AbstractBaseUser,
                                        BaseUserManager,
                                        PermissionsMixin)


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password):
        user = self.model(email=email, password=password)
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    class SexChoices(models.TextChoices):
        MALE = 'ML'
        FEMALE = 'FL'

    avatar = models.ImageField(upload_to='avatars')
    sex = models.CharField(max_length=2, choices=SexChoices.choices)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

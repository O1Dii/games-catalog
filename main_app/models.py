from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, username, email, first_name, last_name, birthday, password):
        user = self.model(
            is_superuser=True,
            is_staff=True,
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            birthday=birthday
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class UserModel(PermissionsMixin, AbstractBaseUser):
    id = models.AutoField(primary_key=True, blank=True)
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=120, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=50, default=" ")
    last_name = models.CharField(max_length=100, default=" ")
    birthday = models.DateField()

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'birthday']

    objects = MyUserManager()

    def __str__(self):
        return self.email

from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, username, email, first_name, last_name, birthday, gender, password):
        user = self.model(
            is_superuser=True,
            is_staff=True,
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            birthday=birthday,
            gender=gender
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class UserModel(PermissionsMixin, AbstractBaseUser):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    id = models.AutoField(primary_key=True, blank=True)
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=120, unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=50, default=" ")
    last_name = models.CharField(max_length=100, default=" ")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birthday = models.DateField()

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'birthday', 'gender']

    objects = MyUserManager()

    def __str__(self):
        return self.email


class Game(models.Model):
    class Meta:
        ordering = ['rating']

    name = models.CharField(max_length=250, unique=True)
    rating = models.DecimalField(decimal_places=5, max_digits=8, null=True)
    version_title = models.CharField(max_length=100, null=True)
    aggregated_rating = models.DecimalField(decimal_places=5, max_digits=8, null=True)
    summary = models.CharField(max_length=10000, null=True)
    first_release_date = models.DateField(null=True)
    rating_count = models.DecimalField(decimal_places=0, max_digits=7, null=True)
    aggregated_rating_count = models.DecimalField(decimal_places=0, max_digits=7, null=True)


class Must(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='musts')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='musts')
    is_deleted = models.BooleanField(default=False)

    def delete(self, force=False, *args, **kwargs):
        if force:
            super().delete(*args, **kwargs)
        self.is_deleted = True
        self.save()

    def __str__(self):
        return f"{self.user.username} {self.game.id}"


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    games = models.ManyToManyField(Game, related_name="genres")


class Platform(models.Model):
    name = models.CharField(max_length=100, unique=True)
    games = models.ManyToManyField(Game, related_name="platforms")


class Cover(models.Model):
    url = models.URLField()
    game = models.ForeignKey(Game, related_name="cover", on_delete=models.CASCADE)


class Screenshot(models.Model):
    url = models.URLField()
    game = models.ForeignKey(Game, related_name="screenshots", on_delete=models.CASCADE)

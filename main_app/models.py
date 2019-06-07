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


class MustModel(models.Model):
    game_id = models.IntegerField()
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} {self.game_id}"


class GameModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    rating = models.DecimalField(decimal_places=0, max_digits=3)
    version_title = models.CharField(max_length=50)
    aggregated_rating = models.DecimalField(decimal_places=0, max_digits=3)
    summary = models.CharField(max_length=500)
    first_release_date = models.DateField()
    rating_count = models.DecimalField(decimal_places=0, max_digits=3)
    aggregated_rating_count = models.DecimalField(decimal_places=0, max_digits=3)


class GenreModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


class PlatformModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)


class ImageModel(models.Model):
    id = models.AutoField(primary_key=True)
    url = models.URLField()


class GenreGameModel(models.Model):
    game_id = models.ForeignKey(GameModel, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(GenreModel, on_delete=models.CASCADE)


class PlatformGameModel(models.Model):
    game_id = models.ForeignKey(GameModel, on_delete=models.CASCADE)
    platform_id = models.ForeignKey(PlatformModel, on_delete=models.CASCADE)


class CoverGameModel(models.Model):
    game_id = models.ForeignKey(GameModel, on_delete=models.CASCADE)
    cover_id = models.ForeignKey(ImageModel, on_delete=models.CASCADE)


class ScreenshotGameModel(models.Model):
    game_id = models.ForeignKey(GameModel, on_delete=models.CASCADE)
    screenshot_id = models.ForeignKey(ImageModel, on_delete=models.CASCADE)

from django.db import models


class GameImage(models.Model):
    image = models.ImageField(upload_to='')

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'
